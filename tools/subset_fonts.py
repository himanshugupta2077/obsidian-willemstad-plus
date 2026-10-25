"""Subsets the theme's embedded text fonts to Latin scripts, punctuation and symbols, in place.

Upstream embeds full-coverage fonts (Inter alone has ~1,900 Cyrillic, Greek and other non-Latin
characters), which pushes theme.css past Obsidian Sync's 5 MB per-file limit, so the theme never
reaches other devices. Weights, variable axes and OpenType features are kept; characters outside the
subset fall back to a system font. Icon, math and monospace fonts are left whole.
"""
import base64
import io
import re
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

FAMILIES = {'"Inter 4.1"', "Manrope", '"DM Sans"', '"Crimson Pro"'}
UNICODES = [
	*range(0x0000, 0x0250),  # Basic Latin, Latin-1, Latin Extended-A/B
	*range(0x02B0, 0x0370),  # spacing modifiers, combining diacritics
	*range(0x1E00, 0x1F00),  # Latin Extended Additional
	*range(0x2000, 0x2C00),  # punctuation, currency, letterlike, arrows, math, shapes, dingbats
	*range(0xFB00, 0xFB07),  # ligatures
	0xFEFF, 0xFFFD,
]

FACE = re.compile(r"@font-face\s*\{[^}]*\}")
DATA = re.compile(r"(data:font/woff2?;(?:charset=[^;,]+;)?base64,)([A-Za-z0-9+/=]+)")


def shrink(b64: str) -> str:
	font = TTFont(io.BytesIO(base64.b64decode(b64)))
	options = subset.Options()
	options.layout_features = ["*"]
	options.name_IDs = ["*"]
	options.name_languages = ["*"]
	options.notdef_outline = True
	options.flavor = "woff2"
	subsetter = subset.Subsetter(options)
	subsetter.populate(unicodes=UNICODES)
	subsetter.subset(font)
	out = io.BytesIO()
	font.flavor = "woff2"
	font.save(out)
	return base64.b64encode(out.getvalue()).decode()


def face(match: re.Match) -> str:
	block = match.group(0)
	family = re.search(r"font-family:\s*([^;]+);", block)
	if not family or family.group(1).strip() not in FAMILIES:
		return block
	return DATA.sub(lambda d: "data:font/woff2;base64," + shrink(d.group(2)), block)


path = sys.argv[1]
css = open(path, encoding="utf-8").read()
before = len(css)
css = FACE.sub(face, css)
open(path, "w", encoding="utf-8").write(css)
print(f"subset fonts: {before / 1e6:.2f} MB → {len(css) / 1e6:.2f} MB")
