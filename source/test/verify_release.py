#!/usr/bin/env python3
"""Check release contents, accepted binary hashes and all bitmap records."""
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'source/main/UniBeijingX/tools'))
from font_format import sfnt_tables, unicode_cmap, glyph_record
from region_place_extension import required_characters


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    config = json.loads((ROOT / 'source/main/tools/release_config.json').read_text())
    release = ROOT / 'release' / ('UniBeijingX-' + config['version'])
    manual_name = 'USER_GUIDE_zh-CN.md'
    manual = (ROOT / 'docs' / manual_name).read_bytes()
    assert manual == (release / manual_name).read_bytes(), 'Manual copies differ'
    text = manual.decode()
    images = set(re.findall(r'!\[[^\]]*\]\((image/[^)\s]+)\)', text))
    assert images, 'Missing simulator screenshots'
    assert {str(p.relative_to(ROOT / 'docs')) for p in (ROOT / 'docs/image').rglob('*') if p.is_file() and p.name != '.DS_Store'} == images
    for name in images:
        data = (ROOT / 'docs' / name).read_bytes()
        assert data.startswith(b'\x89PNG\r\n\x1a\n'), name
        assert data == (release / name).read_bytes(), name
    expected_names = {*config['packages'], manual_name, *images}
    assert {str(p.relative_to(release)) for p in release.rglob('*') if p.is_file() and p.name != '.DS_Store'} == expected_names
    for notice in ('Apache License 2.0', 'SIL Open Font License 1.1', 'MIT'):
        assert notice in text, notice
    assert 'TERMS AND CONDITIONS FOR USE' not in text, 'Keep full license text outside the user manual'
    for token in ('-10061', 'Permission violation', '具体底层原因仍未查明'):
        assert token in text, token
    for token in ('5.3', 'dev15', 'experiments/', 'packages/', '验收报告', '旧版'):
        assert token not in text, token
    forbidden = ('Einstein:', 'UBXHardwareQA', 'ubxChineseUI', 'ChineseUI.sfnt', 'Translations.zh-CN')
    for name, info in config['packages'].items():
        path = release / name
        assert sha(path) == info['sha256'] and path.stat().st_size == info['bytes'], name
        data = path.read_bytes()
        assert data.startswith((b'package0', b'package1')), name
        for token in forbidden:
            assert not any(token.encode(e) in data for e in ('ascii', 'utf-16-be', 'utf-16-le')), (name, token)
    archive = release.parent / (release.name + '.zip')
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert set(bundle.namelist()) == {release.name + '/' + n for n in expected_names}
        for name in expected_names:
            assert bundle.read(release.name + '/' + name) == (release / name).read_bytes(), name
        notices = bundle.comment.decode('utf-8')
        assert (ROOT / 'LICENSE').read_text() in notices, 'Missing Apache license in ZIP comment'
        assert (ROOT / 'THIRD_PARTY_NOTICES.md').read_text() in notices, 'Missing third-party notices in ZIP comment'
    assert {p.name for p in (ROOT / 'release').iterdir() if p.name != '.DS_Store'} == {release.name, archive.name}
    result = {'release_sha256': sha(archive), 'archive_files': len(expected_names), 'screenshots': len(images), 'fonts': {}}
    for variant, sizes in [('lite', [9, 12, 16]), ('full', [9, 10, 12, 14, 16, 18])]:
        source = ROOT / 'source/main/UniBeijingX' / ('font-' + variant) / 'UniBeijingX.sfnt'
        tables = sfnt_tables(source)
        cmap = unicode_cmap(tables)
        assert len(cmap) == 8416
        assert required_characters() <= cmap.keys(), 'Missing regional place-name glyphs'
        strikes = struct.unpack_from('>I', tables['bloc'], 4)[0]
        assert [tables['bloc'][8 + 48 * i + 44] for i in range(strikes)] == sizes
        for row in range(0xA1, 0xF8):
            for cell in range(0xA1, 0xFF):
                try:
                    char = bytes([row, cell]).decode('gb2312')
                except UnicodeDecodeError:
                    continue
                assert ord(char) in cmap, char
        count = 0
        for i in range(strikes):
            for cp, gid in cmap.items():
                record = glyph_record(tables, i, gid)
                assert len(record) >= 5, (variant, i, cp)
                height, width, x, y, advance = struct.unpack_from('>BBbbB', record)
                assert len(record) == 5 + height * ((width + 7) // 8), (variant, i, cp)
                assert advance > 0, (variant, i, cp)
                if not chr(cp).isspace():
                    assert any(record[5:]), (variant, i, hex(cp))
                count += 1
        assert source.read_bytes() in (release / ('Font-' + variant.title() + '.pkg')).read_bytes()
        result['fonts'][variant] = {'characters': len(cmap), 'bitmap_records': count, 'sizes': sizes}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
