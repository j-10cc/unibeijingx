#!/usr/bin/env python3
"""Check regional data, regenerated modules and glyph coverage without an emulator."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
REGION = ROOT / 'source/main/ChineseRegion'
sys.path.insert(0, str(REGION / 'tools'))
sys.path.insert(0, str(ROOT / 'source/main/UniBeijingX/tools'))
from build_supplemental_atlas import render
from font_format import sfnt_tables, unicode_cmap, glyph_record
from display52_latin_extension import metrics
from region_place_extension import required_characters


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, help='Optional before-font snapshot directory')
    args = parser.parse_args()
    sha = lambda b: hashlib.sha256(b).hexdigest()
    assert sha(b''.join((REGION / f'ChinaProvince{i}.newt').read_bytes() for i in range(31))) == 'ab23dc3201fb88c78360f9b5df93cedc8cbe47634fa024fe7b3406f536d571d5'
    assert sha((REGION / 'ChinaCodes.bin').read_bytes()) == 'b0e87577637cc67e74ff4a9cfffe40eafae75bb0ba5858b2a76f12d37571c6c5'
    for name, text in render().items():
        assert (REGION / name).read_text() == text, name
    data = json.loads((REGION / 'geodata/supplemental.json').read_text())
    tw, hk, mo = data['provinces']
    assert [p['name'] for p in data['provinces']] == ['台湾省', '香港特别行政区', '澳门特别行政区']
    assert [len(p['cities']) for p in (tw, hk, mo)] == [22, 3, 4]
    flat = lambda p: [a for c in p['cities'] for a in c['areas']]
    assert [len(flat(p)) for p in (tw, hk, mo)] == [371, 18, 8]
    for p in (tw, hk, mo):
        assert len({c['name'] for c in p['cities']}) == len(p['cities'])
        for c in p['cities']:
            assert len({a['name'] for a in c['areas']}) == len(c['areas'])
    codes = [a['postalCodes'][0] for a in flat(tw)]
    # Hsinchu City's three districts share 300; Chiayi City's two share 600.
    assert len(set(codes)) == 368
    assert all(len(z) == 3 and z.isascii() and z.isdigit() for z in codes)
    assert tw['cities'][0]['name'] == '臺北市'
    assert tw['cities'][0]['areas'][0] == {'name': '中正區', 'postalCodes': ['100']}
    assert {'290', '817', '819'} <= set(codes)
    assert all(a['postalCodes'] == [''] for p in (hk, mo) for a in flat(p))
    paths = {v: ROOT / f'source/main/UniBeijingX/font-{v}/UniBeijingX.sfnt' for v in ['lite', 'full']}
    paths['region'] = REGION / 'LocalizationUI.sfnt'
    result = {'mainland_tables_and_packed_codes_unchanged': True, 'regional_areas': [371, 18, 8], 'fonts': {}}
    for v, path in paths.items():
        t = sfnt_tables(path); cmap = unicode_cmap(t)
        assert required_characters() <= cmap.keys(), v
        strikes = struct.unpack_from('>I', t['bloc'], 4)[0]
        for i in range(strikes):
            for cp in required_characters():
                assert any(glyph_record(t, i, cmap[cp])[5:]), (v, i, chr(cp))
        preserved = 0
        if args.baseline:
            old = sfnt_tables(args.baseline / (v+'-before.sfnt')); before = unicode_cmap(old)
            n = struct.unpack_from('>H', old['maxp'], 4)[0]
            assert all(cmap[cp] == g for cp, g in before.items())
            assert metrics(t)[:n] == metrics(old)
            for i in range(strikes):
                for g in range(n):
                    assert glyph_record(old, i, g) == glyph_record(t, i, g), (v, i, g)
                    preserved += 1
        result['fonts'][v] = {'characters': len(cmap), 'strikes': strikes, 'old_records_preserved': preserved}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
