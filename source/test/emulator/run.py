#!/usr/bin/env python3
"""Start an isolated emulator using retained dependencies and a new scratch flash."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('profile', help='A new, unique alphanumeric/hyphen profile name')
    args = parser.parse_args()
    if not args.profile.replace('-', '').isalnum():
        parser.error('Invalid profile name')
    directory = ROOT / 'source/test/.runtime' / args.profile
    directory.mkdir(parents=True, exist_ok=False)
    dependencies = ROOT / 'external/emulator'
    app = dependencies / 'runtime/EinsteinDisplay52.app/Contents/MacOS/Einstein'
    rom = dependencies / 'runtime/mp2000-rom/mp2000.rom'
    base = dependencies / 'fixtures/clean-final.flash'
    for path in (app, rom, base):
        if not path.is_file():
            raise FileNotFoundError(path)
    flash = directory / 'clean.flash'
    shutil.copyfile(base, flash)
    settings = ('; FLTK preferences file format 1.0\n; vendor: robowerk.com\n; application: einstein\n'
                '[.]\ndontShow:1\n[./ROM]\npath:' + str(rom) + '\nbuiltInRex:1\n'
                '[./Flash]\npath:' + str(flash) + '\n')
    (directory / 'einstein.prefs').write_text(settings)
    (directory / 'launch.json').write_text(json.dumps({'profile': args.profile, 'rom': str(rom), 'base': str(base), 'app': str(app)}, indent=2)+'\n')
    with (directory / 'environment.lock').open('w') as lock, (directory / 'runtime.log').open('wb', buffering=0) as output:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        process = subprocess.Popen([str(app)], stdout=output, stderr=subprocess.STDOUT,
                                   env={**os.environ, 'UBX_PEN_COMMAND_FILE': str(directory / 'command'),
                                        'UBX_DISPLAY52_PREFS_DIR': str(directory)})
        def stop(signum, frame):
            if process.poll() is None:
                process.terminate()
        signal.signal(signal.SIGTERM, stop)
        signal.signal(signal.SIGINT, stop)
        print(directory, flush=True)
        try:
            process.wait()
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=20)


if __name__ == '__main__':
    main()
