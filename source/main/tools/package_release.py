#!/usr/bin/env python3
"""Package accepted binaries, the user manual and its referenced screenshots."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
CONFIG = json.loads(Path(__file__).with_name('release_config.json').read_text())
RELEASE = ROOT / 'release' / ('UniBeijingX-' + CONFIG['version'])
MANUAL = 'USER_GUIDE_zh-CN.md'


def main():
    for name, info in CONFIG['packages'].items():
        data = (RELEASE / name).read_bytes()
        if len(data) != info['bytes'] or hashlib.sha256(data).hexdigest() != info['sha256']:
            raise RuntimeError('Unaccepted release binary: ' + name)
    manual = ROOT / 'docs' / MANUAL
    text = manual.read_text()
    for notice in ('Apache License 2.0', 'SIL Open Font License 1.1', 'MIT', '-10061'):
        if notice not in text:
            raise RuntimeError('Manual is missing: ' + notice)
    images = sorted(set(re.findall(r'!\[[^\]]*\]\((image/[^)\s]+)\)', text)))
    if not images:
        raise RuntimeError('Manual must include simulator screenshots')
    for name in images:
        path = Path(name)
        if len(path.parts) != 2 or path.suffix.lower() != '.png':
            raise RuntimeError('Invalid screenshot path: ' + name)
        if not (ROOT / 'docs' / path).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
            raise RuntimeError('Invalid PNG screenshot: ' + name)
    names = [*CONFIG['packages'], MANUAL, *images]
    extras = [str(path.relative_to(RELEASE)) for path in RELEASE.rglob('*')
              if path.is_file() and str(path.relative_to(RELEASE)) not in names and path.name != '.DS_Store']
    if extras:
        raise RuntimeError('Unexpected release files: ' + ', '.join(extras))
    shutil.copyfile(manual, RELEASE / MANUAL)
    for name in images:
        (RELEASE / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / 'docs' / name, RELEASE / name)
    licenses = ('UniBeijingX 1.0.0 - licenses and attribution\n\n'
                + 'LICENSE\n\n' + (ROOT / 'LICENSE').read_text()
                + '\nTHIRD_PARTY_NOTICES.md\n\n' + (ROOT / 'THIRD_PARTY_NOTICES.md').read_text()).encode('utf-8')
    if len(licenses) > 65535:
        raise RuntimeError('License text exceeds ZIP comment capacity')
    archive = RELEASE.parent / (RELEASE.name + '.zip')
    with tempfile.NamedTemporaryFile(dir=archive.parent, suffix='.zip', delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
            bundle.comment = licenses
            for name in sorted(names):
                entry = zipfile.ZipInfo(RELEASE.name + '/' + name, date_time=(2026, 10, 23, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                bundle.writestr(entry, (RELEASE / name).read_bytes())
        with zipfile.ZipFile(temporary_path) as bundle:
            if bundle.testzip() is not None:
                raise RuntimeError('Corrupt archive')
            if set(bundle.namelist()) != {RELEASE.name + '/' + name for name in names}:
                raise RuntimeError('Expected only accepted packages, manual and screenshots')
            if bundle.comment != licenses:
                raise RuntimeError('Missing license text in archive comment')
        os.replace(temporary_path, archive)
    finally:
        temporary_path.unlink(missing_ok=True)
    print(json.dumps({'archive': str(archive.relative_to(ROOT)), 'files': sorted(names),
                      'sha256': hashlib.sha256(archive.read_bytes()).hexdigest()}, indent=2))


if __name__ == '__main__':
    main()
