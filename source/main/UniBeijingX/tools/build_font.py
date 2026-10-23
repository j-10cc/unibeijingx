#!/usr/bin/env python3
"""Build a Unicode bitmap SFNT covering every defined GB2312 character."""

from __future__ import annotations

import argparse
import pathlib
import struct
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont
from fontTools.misc.macRes import ResourceReader
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables.DefaultTable import DefaultTable
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable


ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / 'source/main').is_dir())
SOURCE = ROOT / "external/fonts/NotoSansCJKsc-Regular.otf"
SMALL_STRIKE_THRESHOLD = {9: 112, 10: 112}


def render_glyph(font: ImageFont.FreeTypeFont, ch: str, pixels: int) -> tuple[Image.Image, int, int, int]:
    """Rasterize once for both BDF and Newton's bitmap table.

    Small CJK strikes need a little more ink than the default 50% coverage
    cutoff. Sparse 10-pixel Hanzi need a second, lower cutoff: for example,
    the centre stroke of 中 peaks at only 111/255 and otherwise vanishes.
    """
    x0, y0, x1, y1 = font.getbbox(ch, anchor="ls")
    width, height = max(1, x1 - x0), max(1, y1 - y0)
    bitmap = Image.new("L", (width, height))
    ImageDraw.Draw(bitmap).text((-x0, -y0), ch, font=font, fill=255, anchor="ls")
    threshold = SMALL_STRIKE_THRESHOLD.get(pixels, 128) if ord(ch) >= 0x80 else 128
    if pixels == 10 and 0x4E00 <= ord(ch) <= 0x9FFF:
        if sum(value >= threshold for value in bitmap.getdata()) <= 25:
            threshold = 96
    peak = max(bitmap.getdata())
    if not ch.isspace() and peak and peak < threshold:
        # Thin, phase-shifted strokes may never reach the usual cutoff.
        # This affects U+4E28 and GB2312 box-drawing/fullwidth symbols.
        threshold = max(1, peak * 3 // 4)
    bitmap = bitmap.point(lambda value: 255 if value >= threshold else 0, mode="1")
    # Newton stores these glyphs uncompressed. Trim unused rows and columns
    # while keeping the bearings and advance, so the visible design and
    # placement do not change.
    ink = bitmap.getbbox()
    if ink:
        left, top, right, bottom = ink
        bitmap = bitmap.crop(ink)
        x0 += left
        y0 += top
    else:
        bitmap = Image.new("1", (1, 1))
    return bitmap, x0, y0, max(1, round(font.getlength(ch)))


def gb2312_characters() -> list[str]:
    chars = {chr(i) for i in range(32, 127)}
    for row in range(0xA1, 0xF8):
        for cell in range(0xA1, 0xFF):
            try:
                chars.add(bytes((row, cell)).decode("gb2312"))
            except UnicodeDecodeError:
                pass
    return sorted(chars, key=ord)


def make_bdf(path: pathlib.Path, chars: list[str], pixels: int) -> None:
    font = ImageFont.truetype(str(SOURCE), pixels)
    ascent, descent = font.getmetrics()
    with path.open("w", encoding="ascii") as out:
        out.write(
            f"STARTFONT 2.1\n"
            f"FONT -UniBeijingX-UniBeijingX-Medium-R-Normal--{pixels}-{pixels * 10}-75-75-C-{pixels * 10}-ISO10646-1\n"
            f"SIZE {pixels} 75 75\n"
            f"FONTBOUNDINGBOX {pixels + 2} {ascent + descent} 0 -{descent}\n"
            f"STARTPROPERTIES 3\nFONT_ASCENT {ascent}\nFONT_DESCENT {descent}\n"
            "DEFAULT_CHAR 32\nENDPROPERTIES\n"
            f"CHARS {len(chars)}\n"
        )
        for ch in chars:
            cp = ord(ch)
            img, x0, y0, advance = render_glyph(font, ch, pixels)
            width, height = img.size
            y1 = y0 + height
            out.write(
                f"STARTCHAR uni{cp:04X}\nENCODING {cp}\n"
                f"SWIDTH {round(advance * 1000 / pixels)} 0\nDWIDTH {advance} 0\n"
                f"BBX {width} {height} {x0} {-y1}\nBITMAP\n"
            )
            for y in range(height):
                bits = "".join("1" if img.getpixel((x, y)) else "0" for x in range(width))
                bits = bits.ljust((width + 7) // 8 * 8, "0")
                out.write(f"{int(bits, 2):0{(width + 7) // 8 * 2}X}\n")
            out.write("ENDCHAR\n")
        out.write("ENDFONT\n")


def newton_bitmap_tables(font: TTFont, strikes: list[int]) -> tuple[bytes, bytes]:
    """Write the index-format-3/image-format-1 bitmap profile used by Newton."""
    cmap = font.getBestCmap()
    glyph_ids = font.getReverseGlyphMap()
    codepoints = {glyph_ids[name]: cp for cp, name in cmap.items()}
    glyph_count = font["maxp"].numGlyphs
    source_bloc = font.reader["bloc"]
    bloc = bytearray(struct.pack(">II", 0x00020000, len(strikes)))
    bloc.extend(b"\0" * (48 * len(strikes)))
    bdat = bytearray(struct.pack(">I", 0x00020000))

    for strike_index, pixels in enumerate(strikes):
        pil_font = ImageFont.truetype(str(SOURCE), pixels)
        images = []
        for glyph_id in range(glyph_count):
            cp = codepoints.get(glyph_id)
            if cp is None:
                images.append(b"\x01\x01\x00\x01\x01\x00")
                continue
            ch = chr(cp)
            bitmap, x0, y0, advance = render_glyph(pil_font, ch, pixels)
            width, height = bitmap.size
            if not all(0 <= v <= 255 for v in (width, height, advance)):
                raise ValueError(f"Glyph metrics out of range: {ch!r} at {pixels}px")
            if not all(-128 <= v <= 127 for v in (x0, -y0)):
                raise ValueError(f"Glyph bearings out of range: {ch!r} at {pixels}px")
            data = bytearray(struct.pack(">BBbbB", height, width, x0, -y0, advance))
            for y in range(height):
                for byte_x in range((width + 7) // 8):
                    byte = 0
                    for bit in range(8):
                        x = 8 * byte_x + bit
                        if x < width and bitmap.getpixel((x, y)):
                            byte |= 0x80 >> bit
                    data.append(byte)
            images.append(bytes(data))

        # A format-3 subtable uses 16-bit offsets. Keep each run below 60 KiB.
        runs = []
        first = 0
        while first < glyph_count:
            last = first
            total = 0
            while last < glyph_count and total + len(images[last]) <= 60000:
                total += len(images[last])
                last += 1
            if last == first:
                raise ValueError("A bitmap glyph exceeds a format-3 subtable")
            runs.append((first, last))
            first = last

        array_offset = len(bloc)
        subtables = bytearray()
        records = bytearray()
        for first, after in runs:
            relative_offset = len(runs) * 8 + len(subtables)
            records.extend(struct.pack(">HHI", first, after - 1, relative_offset))
            image_base = len(bdat)
            offsets = [0]
            for glyph_id in range(first, after):
                bdat.extend(images[glyph_id])
                offsets.append(len(bdat) - image_base)
            while len(bdat) % 4:
                bdat.append(0)
            subtables.extend(struct.pack(">HHI", 3, 1, image_base))
            subtables.extend(struct.pack(">" + "H" * len(offsets), *offsets))
            while len(subtables) % 4:
                subtables.append(0)
        bloc.extend(records)
        bloc.extend(subtables)
        index_tables_size = len(records) + len(subtables)
        source_size_offset = 8 + strike_index * 48
        line_metrics = source_bloc[source_size_offset + 16 : source_size_offset + 40]
        size_table = (
            struct.pack(">IIII", array_offset, index_tables_size, len(runs), 0)
            + line_metrics
            + struct.pack(">HHBBBB", 0, glyph_count - 1, pixels, pixels, 1, 0)
        )
        bloc[8 + strike_index * 48 : 8 + (strike_index + 1) * 48] = size_table
    return bytes(bloc), bytes(bdat)


def normalize(fontforge_sfnt: bytes, output: pathlib.Path, chars: list[str], strikes: list[int]) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        inp = pathlib.Path(tmp) / "font.sfnt"
        inp.write_bytes(fontforge_sfnt)
        src = TTFont(str(inp), lazy=True)
        raw = {tag: src.reader[tag] for tag in src.reader.tables}
        num_glyphs = struct.unpack_from(">H", raw["maxp"], 4)[0]
        raw["maxp"] = b"\x00\x01\x00\x00" + raw["maxp"][4:]
        head = bytearray(raw.pop("bhed"))
        # Match the bitmap SFNT profile used by Newton's Unicode fonts.
        struct.pack_into(">H", head, 16, 0)  # flags, matching Newton's bitmap font
        struct.pack_into(">H", head, 18, 2048)  # unitsPerEm
        struct.pack_into(">hhhh", head, 36, 0, 0, 2048, 2048)
        struct.pack_into(">HHHHH", head, 44, 0, min(strikes), 1, 1, 1)
        raw["head"] = bytes(head)

        # The bitmap-only FontForge export omits these Newton-required tables.
        # All metrics are expressed in the SFNT's 1024-unit em square.
        hhea_fields = [1602, -445, 0, 2048, 0, 0, 2048, 1, 0, 0, 0, 0, 0, 0, 0, num_glyphs]
        raw["hhea"] = struct.pack(">I16h", 0x00010000, *hhea_fields)
        raw["hmtx"] = struct.pack(">Hh", 2048, 0) * num_glyphs
        raw["post"] = b"\x00\x03\x00\x00" + raw["post"][4:32]
        raw["hsty"] = struct.pack(">I5I", 0x00010000, 0, 0, 0, 0, 0)
        for tag in ("OS/2", "BDF ", "FFTM"):
            raw.pop(tag, None)

        result = TTFont(recalcBBoxes=False, recalcTimestamp=False)
        result.sfntVersion = "\x00\x01\x00\x00"
        for tag, data in raw.items():
            table = DefaultTable(tag)
            table.data = bytes(data)
            result[tag] = table
        result.save(str(output))

    # Newton's example font uses one Unicode cmap (platform 0, encoding 2).
    parsed = TTFont(str(output), recalcBBoxes=False, recalcTimestamp=False)
    mapping = parsed.getBestCmap()
    for codepoint, glyph_name in mapping.items():
        if codepoint < 0x7F:
            parsed["hmtx"].metrics[glyph_name] = (1024, 0)
    unicode_map = CmapSubtable.newSubtable(4)
    unicode_map.platformID = 0
    unicode_map.platEncID = 2
    unicode_map.language = 0
    unicode_map.cmap = mapping
    parsed["cmap"].tables = [unicode_map]
    bloc, bdat = newton_bitmap_tables(parsed, strikes)
    for tag, data in (("bloc", bloc), ("bdat", bdat)):
        table = DefaultTable(tag)
        table.data = data
        parsed[tag] = table
    parsed.save(str(output))

    check = TTFont(str(output), lazy=True)
    missing = [ch for ch in chars if ord(ch) not in check.getBestCmap()]
    if missing:
        raise ValueError(f"Missing {len(missing)} GB2312 glyphs: {missing[:8]!r}")
    required = {"cmap", "head", "hhea", "hmtx", "maxp", "name", "bloc", "bdat"}
    if not required.issubset(check.keys()):
        raise ValueError(f"Missing required SFNT tables: {required - set(check.keys())}")
    print(f"{output}: {len(chars)} Unicode characters, {output.stat().st_size} bytes")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pixels", type=int, default=16)
    parser.add_argument("--strikes", default="9,12,16", help="Comma-separated bitmap strike sizes")
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "release/build/base-GB2312.sfnt")
    args = parser.parse_args()
    chars = gb2312_characters()
    strikes = [int(x) for x in args.strikes.split(",")] if args.strikes else [args.pixels]
    if not strikes or any(x < 6 or x > 32 for x in strikes) or len(set(strikes)) != len(strikes):
        raise ValueError("Bitmap strikes must be unique sizes from 6 to 32 pixels")
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = pathlib.Path(tmp)
        dfont = tmpdir / "font.dfont"
        bdfs = [tmpdir / f"font-{pixels}.bdf" for pixels in strikes]
        for bdf, pixels in zip(bdfs, strikes):
            make_bdf(bdf, chars, pixels)
        script = pathlib.Path(__file__).with_name("fontforge_to_dfont.py")
        subprocess.run(["fontforge", "-script", str(script), str(bdfs[0]), str(dfont), *(str(x) for x in bdfs[1:])], check=True)
        sfnt = ResourceReader(str(dfont))["sfnt"][0].data
        args.output.parent.mkdir(parents=True, exist_ok=True)
        normalize(sfnt, args.output, chars, strikes)


if __name__ == "__main__":
    main()
