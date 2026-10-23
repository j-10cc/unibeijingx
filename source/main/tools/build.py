#!/usr/bin/env python3
"""Compile release components in isolation; never overwrite accepted media."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CONFIG = json.loads(Path(__file__).with_name('release_config.json').read_text())
REFERENCE = ROOT / 'release' / ('UniBeijingX-' + CONFIG['version'])
COMPONENTS = CONFIG['packages']
FORBIDDEN = ('Einstein:', 'UBXHardwareQA', 'ubxChineseUI', 'ChineseUI.sfnt', 'Translations.zh-CN')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def compile_package(name, work):
    info = COMPONENTS[name]
    component, project, output = (info[key] for key in ('component', 'project', 'output'))
    directory = work / name[:-4]
    shutil.copytree(ROOT / 'source/main' / component, directory)
    if name.startswith('Font-'):
        for path in (ROOT / 'source/main/UniBeijingX/shared').glob('*.newt'):
            shutil.copy2(path, directory / path.name)
    for path in directory.rglob('*.newt'):
        for token in FORBIDDEN:
            if token in path.read_text():
                raise RuntimeError(f'Development dependency in product: {path}: {token}')
    run = subprocess.run([str(ROOT / 'external/toolchain/bin/tntk'), '-P',
                          str(ROOT / 'external/toolchain/platform'), '-c', project],
                         cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if run.returncode:
        raise RuntimeError(run.stdout.decode(errors='replace'))
    data = bytearray((directory / output).read_bytes())
    if data[:8] not in (b'package0', b'package1'):
        raise RuntimeError(f'Invalid package: {name}')
    # Newton's build timestamp is the only nondeterministic package header field.
    data[32:36] = info['creation_time'].to_bytes(4, 'big')
    for token in FORBIDDEN:
        if any(token.encode(encoding) in data for encoding in ('ascii', 'utf-16-be', 'utf-16-le')):
            raise RuntimeError(f'Development symbol in product: {name}: {token}')
    return bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Rebuild twice; compare both results with 1.0.0')
    parser.add_argument('--output', type=Path, default=ROOT / 'external/.build/packages')
    args = parser.parse_args()
    if not args.check:
        output = args.output.resolve()
        if output == REFERENCE or REFERENCE in output.parents or output in REFERENCE.parents:
            parser.error('Output must not overwrite the accepted release')
        output.mkdir(parents=True, exist_ok=True)
    result = {}
    for name in COMPONENTS:
        with tempfile.TemporaryDirectory(prefix='ubx-compile-') as directory:
            data = compile_package(name, Path(directory))
        expected = COMPONENTS[name]['sha256']
        if args.check:
            with tempfile.TemporaryDirectory(prefix='ubx-compile-') as directory:
                assert compile_package(name, Path(directory)) == data, f'Non-reproducible: {name}'
            assert digest(data) == expected, f'Source differs from 1.0.0 {name}: {digest(data)} != {expected}'
            assert (REFERENCE / name).read_bytes() == data, f'Release file differs: {name}'
        else:
            (output / name).write_bytes(data)
        result[name] = {'bytes': len(data), 'sha256': digest(data), 'identical_to_1_0_0': digest(data) == expected}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
