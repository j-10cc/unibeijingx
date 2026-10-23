#!/usr/bin/env python3
"""Package the four accepted binaries and the current user manual only."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
CONFIG = json.loads(Path(__file__).with_name('release_config.json').read_text())
RELEASE = ROOT / 'release' / ('UniBeijingX-' + CONFIG['version'])
MANUAL = 'USER_GUIDE_zh-CN.md'


def main():
    names = [*CONFIG['packages'], MANUAL]
    for name, info in CONFIG['packages'].items():
        data = (RELEASE / name).read_bytes()
        if len(data) != info['bytes'] or hashlib.sha256(data).hexdigest() != info['sha256']:
            raise RuntimeError('Unaccepted release binary: ' + name)
    manual = ROOT / 'docs' / MANUAL
    text = manual.read_text()
    for notice in ('Apache License', 'SIL OPEN FONT LICENSE', 'Copyright (c) 2013 Sun Junyi',
                   'Copyright (c) 2016 mozillazg', '-10061'):
        if notice not in text:
            raise RuntimeError('Manual is missing: ' + notice)
    extras = [str(path.relative_to(RELEASE)) for path in RELEASE.iterdir() if path.name not in names and path.name != '.DS_Store']
    if extras:
        raise RuntimeError('Unexpected release files: ' + ', '.join(extras))
    shutil.copyfile(manual, RELEASE / MANUAL)
    archive = RELEASE.parent / (RELEASE.name + '.zip')
    with tempfile.NamedTemporaryFile(dir=archive.parent, suffix='.zip', delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            for name in sorted(names):
                entry = zipfile.ZipInfo(RELEASE.name + '/' + name, date_time=(2026, 10, 23, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                bundle.writestr(entry, (RELEASE / name).read_bytes())
        with zipfile.ZipFile(temporary_path) as bundle:
            if bundle.testzip() is not None:
                raise RuntimeError('Corrupt archive')
            if len(bundle.namelist()) != 5:
                raise RuntimeError('Expected four PKGs and one manual')
        os.replace(temporary_path, archive)
    finally:
        temporary_path.unlink(missing_ok=True)
    print(json.dumps({'archive': str(archive.relative_to(ROOT)), 'files': sorted(names),
                      'sha256': hashlib.sha256(archive.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
