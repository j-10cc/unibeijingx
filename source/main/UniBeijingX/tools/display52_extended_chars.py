#!/usr/bin/env python3
"""Append dev11 Latin/ROM symbols to frozen dev10; keep every old bitmap exact."""
import re
import struct
import unicodedata
from functools import lru_cache
from pathlib import Path

from display52_latin_extension import bitmap_tables, encode, make_cmap, metrics
from font_format import sfnt_tables, unicode_cmap, glyph_record

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'source/main').is_dir())
BASE = ROOT / 'external/fonts/baselines/dev10'
CJK = ROOT / 'external/fonts/NotoSansCJKsc-Regular.otf'
LATIN = ROOT / 'external/fonts/NotoSans-Regular.ttf'


@lru_cache(None)
def sources():
    return {p: unicode_cmap(sfnt_tables(p)) for p in [CJK, LATIN]}


@lru_cache(None)
def roman_codes():
    source = (BASE / 'font-lite/Font.newt').read_text()
    return set(map(int, re.search(r'romanCodes:\[(.*?)\]', source, re.S)[1].replace('\n', '').replace(' ', '').split(',')))


@lru_cache(None)
def targets():
    available = set().union(*sources().values())
    return sorted(cp for cp in available if
        (0xA0 <= cp <= 0x24F or 0x1E00 <= cp <= 0x1EFF or
         0x2010 <= cp <= 0x205E or 0x20A0 <= cp <= 0x20CF or
         cp in roman_codes() or cp in [0x2212, 0xFB01, 0xFB02])
        and unicodedata.category(chr(cp))[0] not in ('C', 'M')
        and unicodedata.category(chr(cp)) not in ('Zl', 'Zp'))


@lru_cache(None)
def font(path, px):
    from PIL import ImageFont
    return ImageFont.truetype(str(path), px)


def raster(cp, px):
    from PIL import Image
    path = LATIN if cp in sources()[LATIN] else CJK
    f = font(path, px)
    mask, (x, y) = f.getmask2(chr(cp), mode='1', anchor='ls')
    image = Image.frombytes('L', mask.size, bytes(mask)); ink = image.getbbox()
    if not ink and not chr(cp).isspace():
        mask, (x, y) = f.getmask2(chr(cp), mode='L', anchor='ls')
        image = Image.frombytes('L', mask.size, bytes(mask))
        peak = max(image.get_flattened_data()); assert peak, hex(cp)
        image = image.point(lambda value: 255 if value >= max(1, peak*3//4) else 0)
        ink = image.getbbox()
    if ink:
        left, top, _, _ = ink; image = image.crop(ink); x += left; y += top
    else:
        assert chr(cp).isspace(); image = Image.new('L', (1, 1)); x = y = 0
    # Only new glyphs: leave room for the last column and synthetic bold.
    advance = max(1, round(f.getlength(chr(cp))), x+image.width+1)
    data = bytearray(struct.pack('>BBbbB', image.height, image.width, x, -y, advance))
    for row in range(image.height):
        for start in range(0, image.width, 8):
            data.append(sum(128 >> bit for bit in range(8)
                if start+bit < image.width and image.getpixel((start+bit, row))))
    return bytes(data)


def extended(variant):
    p = BASE / ('font-'+variant) / 'UniBeijingX.sfnt'
    old = sfnt_tables(p); tables = dict(old); mapping = unicode_cmap(old)
    added = sorted(set(targets())-set(mapping))
    n = struct.unpack_from('>H', old['maxp'], 4)[0]
    for i, cp in enumerate(added): mapping[cp] = n+i
    count = struct.unpack_from('>I', old['bloc'], 4)[0]
    images = []
    for i in range(count):
        px = old['bloc'][8+i*48+44]
        images.append([glyph_record(old,i,g) for g in range(n)]+[raster(cp,px) for cp in added])
    tables['bloc'], tables['bdat'] = bitmap_tables(old['bloc'], images)
    tables['cmap'] = make_cmap(mapping)
    maxp = bytearray(old['maxp']); struct.pack_into('>H', maxp, 4, n+len(added)); tables['maxp'] = bytes(maxp)
    hhea = bytearray(old['hhea']); struct.pack_into('>H', hhea, 34, n+len(added)); tables['hhea'] = bytes(hhea)
    tables['hmtx'] = b''.join(struct.pack('>Hh', *m) for m in metrics(old)+[(1024,0)]*len(added))
    return tables, added


def verify_extension(variant):
    p = ROOT / 'source/main/UniBeijingX' / ('font-'+variant) / 'UniBeijingX.sfnt'
    base = BASE / ('font-'+variant) / 'UniBeijingX.sfnt'
    tables, added = extended(variant)
    assert p.read_bytes() == encode(tables, base.read_bytes()), ('dev11 font differs',variant)
    a, b = sfnt_tables(base), sfnt_tables(p); ca, cb = unicode_cmap(a), unicode_cmap(b)
    assert all(cb[cp]==g for cp,g in ca.items())
    count = struct.unpack_from('>I', a['bloc'], 4)[0]; preserved = 0
    for i in range(count):
        for g in ca.values():
            assert glyph_record(a,i,g)==glyph_record(b,i,g), (variant,i,g)
            preserved += 1
    assert set(cb)-set(ca)==set(added)
    assert roman_codes()-set(cb)=={0xF8FF}, 'All public ROM characters need real bitmap glyphs'
    assert all(cp in cb for cp in range(0x100,0x180)), 'Latin Extended-A incomplete'
    return {'extension':'dev11','base_characters':len(ca),'characters':len(cb),
            'added_codepoints':added,'old_mapped_bitmap_records_preserved':preserved,
            'original_cmap_ids_and_advances_preserved':True,'public_ROM_codes_mapped':True,
            'private_ROM_logo_not_added':'U+F8FF'}


if __name__ == '__main__':
    import json
    result = {}
    for variant in ['lite','full']:
        tables, _ = extended(variant)
        base = BASE / ('font-'+variant) / 'UniBeijingX.sfnt'
        dest = ROOT / 'source/main/UniBeijingX' / ('font-'+variant) / 'UniBeijingX.sfnt'
        dest.write_bytes(encode(tables, base.read_bytes())); result[variant] = verify_extension(variant)
    print(json.dumps(result, ensure_ascii=False, indent=2))
