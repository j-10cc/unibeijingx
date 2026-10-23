#!/usr/bin/env python3
"""Check immutable release media, relocated source provenance and all bitmap records."""
import hashlib
import json
from pathlib import Path
import struct
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'source/main/UniBeijingX/tools'))
from font_format import sfnt_tables, unicode_cmap, glyph_record


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def main():
    release = ROOT / 'release/UniBeijingX-1.0.0'
    manifest = json.loads((release / 'MANIFEST.json').read_text())
    migration = json.loads((ROOT / 'docs/source-migration.json').read_text())
    migrated = {row['original']: row for row in migration}
    product = json.loads((ROOT / 'docs/product-inputs.json').read_text())
    for row in product:
        assert sha(ROOT / row['path']) == row['sha256'], row['path']
    for line in (release / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        assert sha(release / name) == expected, name
    archive = ROOT / 'release/UniBeijingX-1.0.0.zip'
    expected, _ = (archive.with_suffix('.zip.sha256')).read_text().strip().split('  ', 1)
    assert sha(archive) == expected
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        expected_names = {release.name + '/' + str(p.relative_to(release)) for p in release.rglob('*') if p.is_file()}
        assert set(bundle.namelist()) == expected_names
        for name in bundle.namelist():
            assert bundle.read(name) == (release / Path(name).relative_to(release.name)).read_bytes(), name
    for name, info in manifest['packages'].items():
        path = release / name
        assert sha(path) == info['sha256'] and path.stat().st_size == info['bytes'], name
    evidence = sorted({s for s in strings(manifest) if s.startswith('experiments/') and s.endswith('.png')})
    for name in evidence:
        assert name in migrated, name
        row = migrated[name]
        assert sha(ROOT / row['path']) == row['sha256'], row['path']
    result = {'release_sha256': sha(archive), 'product_sources': len(product), 'release_evidence_images': len(evidence), 'fonts': {}}
    for variant, sizes in [('lite', [9, 12, 16]), ('full', [9, 10, 12, 14, 16, 18])]:
        source = ROOT / 'source/main/UniBeijingX' / ('font-' + variant) / 'UniBeijingX.sfnt'
        tables = sfnt_tables(source)
        cmap = unicode_cmap(tables)
        assert len(cmap) == 8309
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
