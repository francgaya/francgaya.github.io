#!/usr/bin/env python3
"""
Generate the Open Graph card, one per language, into public/.

Why a script and not a hand-made image: the card has to stay in step with the
visual language (adr-002), and the only way that survives a colour or wording
change is if regenerating it is one command. The PNGs themselves ARE committed,
because they are content of the page, not build output: a social crawler
fetches them by URL and CI has no business producing them.

Why it matters more than it looks: roughly all traffic arrives from a link
pasted on LinkedIn, so og:image is the first thing a reader sees, before a
single line of the site.

Type is the real Space Grotesk shipped in node_modules, decompressed from woff2
in memory. No second copy of the font in the repository, and no font that only
resembles the one the site uses.

Run:  python3 scripts/og_image.py
Needs: pillow, fonttools, brotli
"""
from __future__ import annotations

import io
import pathlib

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

SITE = pathlib.Path(__file__).resolve().parents[1]
FONT_WOFF2 = (
    SITE
    / "node_modules/@fontsource-variable/space-grotesk/files"
    / "space-grotesk-latin-wght-normal.woff2"
)
MARK = SITE / "public/android-chrome-512x512.png"

# Straight from the ramps in src/styles/global.css.
DEEP = "#133232"      # teal-900, the site's deep surface
INK = "#FFFFFF"
MUTED = "#CEF6F4"     # teal-100, ink-on-deep-muted
HIGHLIGHT = "#ABDC4A" # lime-300, deep surfaces only
MARKER = "#FE4C40"    # coral-400, position and identity, once per card

W, H = 1200, 630
PAD = 88

CARDS = {
    "og-en.png": {
        "overline": "FRANC GAYA",
        "title": ["Embedded Systems", "Product Architect"],
        "lead": "Home appliances and professional equipment",
    },
    "og-es.png": {
        "overline": "FRANC GAYA",
        "title": ["Arquitecto de producto", "de sistemas embebidos"],
        "lead": "Electrodomésticos y equipamiento profesional",
    },
}


def load_font(size: int, weight: int) -> ImageFont.FreeTypeFont:
    """Space Grotesk Variable at one weight, straight out of node_modules."""
    buf = io.BytesIO()
    TTFont(FONT_WOFF2).save(buf)  # woff2 in, plain sfnt out
    buf.seek(0)
    font = ImageFont.truetype(buf, size)
    font.set_variation_by_axes([weight])
    return font


def tracked(draw: ImageDraw.ImageDraw, xy, text, font, fill, tracking: float) -> None:
    """Letter-spaced run. Pillow has no tracking, and the overline needs it."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def build(name: str, copy: dict) -> None:
    img = Image.new("RGB", (W, H), DEEP)
    draw = ImageDraw.Draw(img)

    mark = Image.open(MARK).convert("RGBA").resize((132, 132), Image.LANCZOS)
    img.paste(mark, (W - PAD - 132, PAD), mark)

    y = PAD + 14
    draw.rounded_rectangle([PAD, y, PAD + 64, y + 5], radius=3, fill=MARKER)

    y += 42
    tracked(draw, (PAD, y), copy["overline"], load_font(25, 600), HIGHLIGHT, 3.4)

    y += 74
    title_font = load_font(78, 600)
    for line in copy["title"]:
        draw.text((PAD, y), line, font=title_font, fill=INK)
        y += 92

    y += 26
    draw.text((PAD, y), copy["lead"], font=load_font(34, 400), fill=MUTED)

    draw.text((PAD, H - PAD - 34), "francgaya.com", font=load_font(30, 500), fill=MUTED)

    out = SITE / "public" / name
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out.relative_to(SITE)}  {out.stat().st_size // 1024} KB")


for name, copy in CARDS.items():
    build(name, copy)
