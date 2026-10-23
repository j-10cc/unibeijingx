"""Read Newton bitmap SFNT tables and Unicode mappings."""

import struct

def sfnt_tables(path):
    data = path.read_bytes()
    count = struct.unpack_from('>H', data, 4)[0]
    tables = {}
    for index in range(count):
        tag, _, offset, size = struct.unpack_from('>4sIII', data, 12 + 16 * index)
        assert offset + size <= len(data)
        tables[tag.decode('ascii')] = data[offset:offset + size]
    return tables

def unicode_cmap(tables):
    data = tables['cmap']
    count = struct.unpack_from('>H', data, 2)[0]
    candidates = []
    for index in range(count):
        platform, encoding, offset = struct.unpack_from('>HHI', data, 4 + 8 * index)
        form = struct.unpack_from('>H', data, offset)[0]
        if (platform == 3 and encoding == 1 or platform == 0) and form == 4:
            candidates.append((platform == 3, offset))
    assert candidates, 'Expected the Newton font Unicode format-4 cmap'
    _, offset = max(candidates)
    segments = struct.unpack_from('>H', data, offset + 6)[0] // 2
    result = {}
    for index in range(segments):
        end = struct.unpack_from('>H', data, offset + 14 + 2 * index)[0]
        start = struct.unpack_from('>H', data, offset + 16 + 2 * segments + 2 * index)[0]
        delta = struct.unpack_from('>h', data, offset + 16 + 4 * segments + 2 * index)[0]
        range_position = offset + 16 + 6 * segments + 2 * index
        relative = struct.unpack_from('>H', data, range_position)[0]
        for point in range(start, min(end, 65534) + 1):
            if relative:
                glyph = struct.unpack_from('>H', data, range_position + relative + 2 * (point - start))[0]
                if glyph:
                    glyph = (glyph + delta) & 65535
            else:
                glyph = (point + delta) & 65535
            if glyph:
                result[point] = glyph
    return result

def glyph_record(tables, strike, glyph):
    bloc, bdat = tables['bloc'], tables['bdat']
    array, _, count, _ = struct.unpack_from('>IIII', bloc, 8 + 48 * strike)
    for index in range(count):
        first, last, relative = struct.unpack_from('>HHI', bloc, array + 8 * index)
        if first <= glyph <= last:
            table = array + relative
            index_format, image_format, base = struct.unpack_from('>HHI', bloc, table)
            assert (index_format, image_format) == (3, 1)
            start, end = struct.unpack_from('>HH', bloc, table + 8 + 2 * (glyph - first))
            return bdat[base + start:base + end]
    raise AssertionError('Glyph absent from bitmap table')
