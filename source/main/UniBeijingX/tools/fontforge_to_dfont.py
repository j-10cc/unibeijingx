import fontforge
import sys

font = fontforge.open(sys.argv[1])
for bdf in sys.argv[3:]:
    font.importBitmaps(bdf)
font.fontname = "UniBeijingX16"
font.familyname = "UniBeijingX"
font.fullname = "UniBeijingX Regular"
font.copyright = "Noto Sans CJK copyright 2014-2021 Adobe; bitmap derivative 2026 UniBeijingX contributors; SIL Open Font License 1.1"
font.generate(sys.argv[2], bitmap_type="sbit", flags=("apple",))
