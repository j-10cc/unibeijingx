#!/usr/bin/env python3
"""Append missing regional place-name glyphs; preserve existing glyphs and metrics."""
import hashlib
import json
import struct
from pathlib import Path

from display52_latin_extension import bitmap_tables, encode, make_cmap, metrics
from font_format import sfnt_tables, unicode_cmap, glyph_record

ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'source/main').is_dir())


def required_characters():
    data = json.loads((ROOT / 'source/main/ChineseRegion/geodata/supplemental.json').read_text())
    names = []
    for p in data['provinces']:
        names.append(p['name'])
        for c in p['cities']:
            names.append(c['name'])
            names.extend(a['name'] for a in c['areas'])
    return set(map(ord, ''.join(names)))


def extend(path):
    from build_font import render_glyph
    from PIL import ImageFont
    original = path.read_bytes()
    old = sfnt_tables(path); mapping = unicode_cmap(old)
    added = sorted(required_characters() - mapping.keys())
    count = struct.unpack_from('>H', old['maxp'], 4)[0]
    strikes = struct.unpack_from('>I', old['bloc'], 4)[0]
    if not added:
        return {'characters': len(mapping), 'added': [], 'unchanged': True}
    source = ROOT / 'external/fonts/NotoSansCJKsc-Regular.otf'
    assert not set(added) - unicode_cmap(sfnt_tables(source)).keys()
    images = []
    for i in range(strikes):
        px = old['bloc'][8 + i*48 + 44]
        font = ImageFont.truetype(str(source), px)
        records = [glyph_record(old, i, g) for g in range(count)]
        for cp in added:
            image, x, y, advance = render_glyph(font, chr(cp), px)
            data = bytearray(struct.pack('>BBbbB', image.height, image.width, x, -y, advance))
            for row in range(image.height):
                for start in range(0, image.width, 8):
                    data.append(sum(128 >> bit for bit in range(8)
                        if start+bit < image.width and image.getpixel((start+bit, row))))
            assert any(data[5:]), hex(cp)
            records.append(bytes(data))
        images.append(records)
    for i, cp in enumerate(added):
        mapping[cp] = count + i
    tables = dict(old)
    tables['bloc'], tables['bdat'] = bitmap_tables(old['bloc'], images)
    tables['cmap'] = make_cmap(mapping)
    for tag, offset in [('maxp', 4), ('hhea', 34)]:
        table = bytearray(old[tag]); struct.pack_into('>H', table, offset, count+len(added))
        tables[tag] = bytes(table)
    tables['hmtx'] = b''.join(struct.pack('>Hh', *m) for m in metrics(old)+[(1024,0)]*len(added))
    path.write_bytes(encode(tables, original))
    new = sfnt_tables(path); before = unicode_cmap(old); after = unicode_cmap(new)
    assert all(after[cp] == g for cp, g in before.items())
    assert metrics(new)[:count] == metrics(old)
    for i in range(strikes):
        for g in range(count):
            assert glyph_record(new, i, g) == glyph_record(old, i, g), (i, g)
    return {'characters': len(after), 'added': [f'U+{cp:04X}' for cp in added],
            'added_text': ''.join(map(chr, added)), 'old_glyph_records_preserved': count*strikes,
            'old_ids_and_metrics_preserved': True, 'baseline_sha256': hashlib.sha256(original).hexdigest()}


if __name__ == '__main__':
    paths = {v: ROOT / f'source/main/UniBeijingX/font-{v}/UniBeijingX.sfnt' for v in ['lite', 'full']}
    paths['region'] = ROOT / 'source/main/ChineseRegion/LocalizationUI.sfnt'
    print(json.dumps({v: extend(p) for v, p in paths.items()}, ensure_ascii=False, indent=2))
