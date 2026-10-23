#!/usr/bin/env python3
"""Deterministic dev10 Latin bitmap extension; never touches formal fonts."""
import struct
import unicodedata
from functools import lru_cache
from pathlib import Path

from font_format import sfnt_tables, unicode_cmap, glyph_record

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'source/main').is_dir())
BASE = ROOT / 'external/fonts/baselines/dev9'
SOURCE = ROOT / 'external/fonts/NotoSansCJKsc-Regular.otf'


@lru_cache(None)
def targets():
    cmap = unicode_cmap(sfnt_tables(SOURCE))
    return sorted(cp for cp in cmap if
        (0xA0 <= cp <= 0x24F or 0x1E00 <= cp <= 0x1EFF or
         0x2010 <= cp <= 0x205E or 0x20A0 <= cp <= 0x20CF or cp == 0x2122)
        and unicodedata.category(chr(cp))[0] not in ('C', 'M')
        and unicodedata.category(chr(cp)) not in ('Zl', 'Zp'))


@lru_cache(None)
def pil_font(px):
    from PIL import ImageFont
    return ImageFont.truetype(str(SOURCE), px)


def raster(cp, px, advance=None):
    from PIL import Image
    # Noto's registered sign is superscript-sized: at 12px its hinted ink is
    # only 5x4, which collapses into a dot. Normalize this newly added symbol
    # to a readable body-size circle without changing any pre-existing width.
    registered = cp == 0xAE
    font = pil_font(px*2 if registered else px)
    mask, (x, y) = font.getmask2(chr(cp), mode='1', anchor='ls')
    image = Image.frombytes('L', mask.size, bytes(mask))
    ink = image.getbbox()
    if not ink and not chr(cp).isspace():
        # A subpixel-height hyphen can disappear in the mono hinter at 9px.
        # Recover only entirely empty non-space masks, never threshold a
        # normally hinted Latin glyph or change any existing CJK bitmap.
        mask, (x, y) = font.getmask2(chr(cp), mode='L', anchor='ls')
        image = Image.frombytes('L', mask.size, bytes(mask))
        peak = max(image.get_flattened_data())
        assert peak, hex(cp)
        cutoff = max(1, peak*3//4)
        image = image.point(lambda value: 255 if value >= cutoff else 0)
        ink = image.getbbox()
    if ink:
        left, top, _, _ = ink
        image = image.crop(ink); x += left; y += top
    else:
        assert chr(cp).isspace(), hex(cp)
        image = Image.new('L', (1, 1)); x = y = 0
    if advance is None:
        advance = max(1, round(font.getlength(chr(cp))))
    if registered:
        assert advance is not None
        y = -max(image.height, -pil_font(px).getbbox('T', anchor='ls')[1])
        advance = max(advance, x+image.width+1)
    data = bytearray(struct.pack('>BBbbB', image.height, image.width, x, -y, advance))
    for row in range(image.height):
        for start in range(0, image.width, 8):
            data.append(sum(128 >> bit for bit in range(8)
                if start + bit < image.width and image.getpixel((start + bit, row))))
    return bytes(data)


def make_cmap(mapping):
    groups = []
    for cp in sorted(mapping):
        if groups and cp == groups[-1][-1] + 1: groups[-1].append(cp)
        else: groups.append([cp])
    n = len(groups) + 1
    search = 2 * (1 << (n.bit_length() - 1))
    end = [g[-1] for g in groups] + [65535]
    start = [g[0] for g in groups] + [65535]
    offsets = []; glyphs = []
    for i, group in enumerate(groups):
        offsets.append(2 * (n - i + len(glyphs)))
        glyphs.extend(mapping[cp] for cp in group)
    body = (struct.pack('>' + 'H'*n, *end) + b'\0\0' +
        struct.pack('>' + 'H'*n, *start) +
        struct.pack('>' + 'H'*n, *([0]*(n-1)+[1])) +
        struct.pack('>' + 'H'*n, *(offsets+[0])) +
        struct.pack('>' + 'H'*len(glyphs), *glyphs))
    length = 14 + len(body); assert length < 65536
    sub = struct.pack('>7H', 4, length, 0, 2*n, search, n.bit_length()-1, 2*n-search) + body
    return struct.pack('>HHHHI', 0, 1, 0, 2, 12) + sub


def bitmap_tables(old, images):
    count = len(images)
    bloc = bytearray(struct.pack('>II', 0x20000, count)+bytes(count*48))
    bdat = bytearray(struct.pack('>I', 0x20000))
    for i, rows in enumerate(images):
        runs = []; first = 0
        while first < len(rows):
            last = first; length = 0
            while last < len(rows) and length+len(rows[last]) <= 60000:
                length += len(rows[last]); last += 1
            runs.append((first, last)); first = last
        array = len(bloc); index = bytearray(); subtables = bytearray()
        for first, last in runs:
            index.extend(struct.pack('>HHI', first, last-1, len(runs)*8+len(subtables)))
            base = len(bdat); offsets = [0]
            for row in rows[first:last]: bdat.extend(row); offsets.append(len(bdat)-base)
            while len(bdat) % 4: bdat.append(0)
            subtables.extend(struct.pack('>HHI', 3, 1, base))
            subtables.extend(struct.pack('>'+'H'*len(offsets), *offsets))
            while len(subtables) % 4: subtables.append(0)
        bloc.extend(index); bloc.extend(subtables)
        size = bytearray(old[8+i*48:8+(i+1)*48])
        struct.pack_into('>IIII', size, 0, array, len(index)+len(subtables), len(runs), 0)
        struct.pack_into('>HH', size, 40, 0, len(rows)-1)
        bloc[8+i*48:8+(i+1)*48] = size
    return bytes(bloc), bytes(bdat)


def metrics(tables):
    count = struct.unpack_from('>H', tables['maxp'], 4)[0]
    long = struct.unpack_from('>H', tables['hhea'], 34)[0]
    result = [struct.unpack_from('>Hh', tables['hmtx'], i*4) for i in range(long)]
    for i in range(long, count):
        result.append((result[-1][0], struct.unpack_from('>h', tables['hmtx'], long*4+(i-long)*2)[0]))
    return result


def extended(variant):
    path = BASE / ('font-'+variant) / 'UniBeijingX.sfnt'
    tables = sfnt_tables(path); old = dict(tables); mapping = unicode_cmap(tables)
    new = sorted(set(targets())-set(mapping)); old_count = struct.unpack_from('>H', tables['maxp'], 4)[0]
    for i, cp in enumerate(new): mapping[cp] = old_count+i
    count = struct.unpack_from('>I', tables['bloc'], 4)[0]
    images = [[glyph_record(tables, i, g) for g in range(old_count)]+[b'']*len(new) for i in range(count)]
    original_map = unicode_cmap(old)
    for i, rows in enumerate(images):
        px = old['bloc'][8+i*48+44]
        for cp in targets():
            advance = rows[original_map[cp]][4] if cp in original_map else None
            rows[mapping[cp]] = raster(cp, px, advance)
    tables['bloc'], tables['bdat'] = bitmap_tables(old['bloc'], images)
    tables['cmap'] = make_cmap(mapping)
    maxp = bytearray(tables['maxp']); struct.pack_into('>H', maxp, 4, old_count+len(new)); tables['maxp'] = bytes(maxp)
    hhea = bytearray(tables['hhea']); struct.pack_into('>H', hhea, 34, old_count+len(new)); tables['hhea'] = bytes(hhea)
    tables['hmtx'] = b''.join(struct.pack('>Hh', *m) for m in metrics(old)+[(1024, 0)]*len(new))
    return tables, new


def encode(tables, header):
    def checksum(data):
        padded = data+bytes((-len(data)) % 4)
        return sum(struct.unpack('>'+'I'*(len(padded)//4), padded)) & 0xffffffff
    tables = dict(tables); head = bytearray(tables['head']); head[8:12] = bytes(4); tables['head'] = bytes(head)
    data = bytearray(header[:12]+bytes(16*len(tables)))
    for i, (tag, table) in enumerate(tables.items()):
        while len(data) % 4: data.append(0)
        offset = len(data); data.extend(table)
        struct.pack_into('>4sIII', data, 12+i*16, tag.encode('ascii'), checksum(table), offset, len(table))
        if tag == 'head': head_offset = offset
    while len(data) % 4: data.append(0)
    struct.pack_into('>I', data, head_offset+8, (0xb1b0afba-checksum(data)) & 0xffffffff)
    assert checksum(data) == 0xb1b0afba
    return bytes(data)


def verify_extension(variant):
    path = ROOT / 'source/main/UniBeijingX' / ('font-'+variant) / 'UniBeijingX.sfnt'
    old_path = BASE / ('font-'+variant) / 'UniBeijingX.sfnt'
    expected, added = extended(variant)
    assert path.read_bytes() == encode(expected, old_path.read_bytes()), ('Non-deterministic font extension', variant)
    before = sfnt_tables(old_path); after = sfnt_tables(path)
    a, b = unicode_cmap(before), unicode_cmap(after)
    assert all(b[cp] == gid for cp, gid in a.items())
    assert set(b)-set(a) == set(added)
    count = struct.unpack_from('>I', before['bloc'], 4)[0]; unchanged = 0; updated = 0
    for i in range(count):
        for cp, gid in a.items():
            old_record, new_record = glyph_record(before, i, gid), glyph_record(after, i, gid)
            if cp not in targets():
                assert old_record == new_record, (variant, i, hex(cp)); unchanged += 1
            else:
                assert old_record[4] == new_record[4]; updated += old_record != new_record
    return {'extension':'dev10', 'base_characters':len(a), 'characters':len(b),
        'added_codepoints':added, 'updated_existing_latin_records':updated,
        'untargeted_records_preserved':unchanged, 'original_cmap_ids_and_advances_preserved':True}


if __name__ == '__main__':
    import json
    result = {}
    for variant in ['lite', 'full']:
        tables, _ = extended(variant)
        base = BASE / ('font-'+variant) / 'UniBeijingX.sfnt'
        dest = ROOT / 'source/main/UniBeijingX' / ('font-'+variant) / 'UniBeijingX.sfnt'
        dest.write_bytes(encode(tables, base.read_bytes()))
        result[variant] = verify_extension(variant)
    print(json.dumps(result, ensure_ascii=False, indent=2))
