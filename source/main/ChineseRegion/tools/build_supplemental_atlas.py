#!/usr/bin/env python3
"""Append the reviewed Taiwan/Hong Kong/Macao data without rewriting mainland data."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]


def render():
    data = json.loads((OUT / 'geodata/supplemental.json').read_text())
    def literal(value):
        if isinstance(value, dict):
            return '{' + ','.join(k + ':' + literal(v) for k, v in value.items()) + '}'
        if isinstance(value, list):
            if not value:
                raise ValueError('Use [""] for no postcode; tntk misencodes quoted empty arrays')
            return '[' + ',\n'.join(map(literal, value)) + ']'
        return json.dumps(value, ensure_ascii=False)
    files = {}
    for index, province in enumerate(data['provinces'], 31):
        files[f'ChinaProvince{index}.newt'] = (
            '// Generated from geodata/supplemental.json; do not edit.\n'
            f"DefGlobalVar('ubxChinaProvince{index},'" + literal(province) + ');\n')
    symbols = ',\n'.join(f'ubxChinaProvince{i}' for i in range(34))
    files['ChinaData.newt'] = (
        '// Generated atlas root.\nDefGlobalVar(\'ubxChinaAtlas,{version:"ChinaPost 2026-10-15 + regional supplement 2026-10-23",'
        'codes:LoadBinary("ChinaCodes.bin"),provinces:[' + symbols + ']});\n')
    return files


def generate():
    for name, text in render().items():
        (OUT / name).write_text(text)


if __name__ == '__main__':
    generate()
