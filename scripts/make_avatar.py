#!/usr/bin/env python3
"""
ZENITH.SYS — Photo ASCII Art SVG
Converts source-prepped.png (portrait, bg removed) into a cyberpunk ASCII SVG.
Single neon-cyan ink color — monochrome is cleaner than rainbow.
Terminal typewriter reveal animation.
"""
from PIL import Image, ImageEnhance, ImageFilter
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "assets", "source-prepped.png")
OUT  = os.path.join(HERE, "..", "assets", "avatar.svg")
STATIC = bool(os.environ.get("STATIC"))

# ── ASCII params ───────────────────────────────────────────────────────────────
COLS   = 68          # character columns
ROWS   = 48          # character rows — ~portrait ratio with CELL_W/CELL_H below
CELL_W = 8.5
CELL_H = 15

# Dense → sparse ramp (dark pixels → dense chars, light/bg → spaces)
RAMP = " .`-:+*cs#%@"

CONTRAST   = 1.08
BRIGHTNESS = 1.0
GAMMA      = 1.15    # >1 brightens mids, more face detail in sparse zone
WHITE_FLOOR = 0.82   # lum above this → forced blank (kills bg fringe)

# ── Layout ─────────────────────────────────────────────────────────────────────
PAD        = 18
TB_H       = 30      # titlebar
STATUS_H   = 28
ART_W      = int(COLS * CELL_W)
ART_H      = ROWS * CELL_H
CANVAS_W   = ART_W + PAD * 2
CANVAS_H   = TB_H + ART_H + STATUS_H + PAD

# Reveal timing
ROW_DUR  = 0.10
STAGGER  = 0.10

# ── Colors ─────────────────────────────────────────────────────────────────────
BG      = "#050a0f"
BG2     = "#07111a"
FRAME   = "#00fff540"
CYAN    = "#00fff5"
GREEN   = "#00ff9d"
MUTED   = "#2a5555"
DIM     = "#0d2020"
INK     = "#00e8e0"   # neon cyan ink — the ASCII color
CURSOR  = "#00fff5"

# ── Process image ──────────────────────────────────────────────────────────────
if not os.path.exists(SRC):
    print(f"ERROR: {SRC} not found. Run prep_photo.py first.", file=sys.stderr)
    sys.exit(1)

im = Image.open(SRC).convert("L")
im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
im = ImageEnhance.Contrast(im).enhance(CONTRAST)
im = im.resize((COLS, ROWS), Image.LANCZOS)
px = im.load()

rows_txt = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        lum = px[x, y] / 255.0
        lum = pow(lum, GAMMA)
        if lum >= WHITE_FLOOR:
            chars.append(" ")
            continue
        idx = int((1.0 - lum) * (len(RAMP) - 1) + 0.5)
        idx = max(0, min(len(RAMP) - 1, idx))
        chars.append(RAMP[idx])
    rows_txt.append("".join(chars))

# ── Assemble SVG ───────────────────────────────────────────────────────────────
art_top  = TB_H + PAD * 0.4
font_sz  = CELL_H * 0.86

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" '
    f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',

    '<defs>'
    f'<linearGradient id="avbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    f'</linearGradient>'
    f'<filter id="cynglow">'
    f'<feGaussianBlur stdDeviation="1.2" result="b"/>'
    f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    f'</filter>'
    '</defs>',

    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="10" fill="url(#avbg)"/>',
    f'<rect x=".5" y=".5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="10" '
    f'fill="none" stroke="{CYAN}" stroke-width="1" stroke-opacity="0.35"/>',

    # Titlebar
    f'<line x1="0" y1="{TB_H}" x2="{CANVAS_W}" y2="{TB_H}" '
    f'stroke="{CYAN}" stroke-opacity="0.25" stroke-width="1"/>',
]

# Traffic lights
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TB_H/2}" r="4.5" fill="{c}"/>')

parts.append(
    f'<text x="{CANVAS_W/2}" y="{TB_H/2 + 4}" fill="{MUTED}" font-size="11.5" '
    f'text-anchor="middle">Varaaa-arch@github: ~$ cat identity.txt</text>'
)

# HUD corner brackets
B = 12
for (px, py, dx, dy) in [(1,1,B,B),(CANVAS_W-1,1,-B,B),(1,CANVAS_H-1,B,-B),(CANVAS_W-1,CANVAS_H-1,-B,-B)]:
    parts.append(
        f'<polyline points="{px+dx},{py} {px},{py} {px},{py+dy}" '
        f'fill="none" stroke="{CYAN}" stroke-width="1.5" stroke-opacity="0.5"/>'
    )

# ASCII rows — typewriter reveal
for ry, line in enumerate(rows_txt):
    y      = art_top + ry * CELL_H + CELL_H * 0.74
    row_y  = art_top + ry * CELL_H
    delay  = ry * STAGGER
    safe   = html.escape(line)

    text = (
        f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
        f'font-size="{font_sz:.1f}" textLength="{ART_W}" lengthAdjust="spacing">'
        f'{safe}</text>'
    )

    if STATIC:
        parts.append(text)
        continue

    parts.append(
        f'<clipPath id="r{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{ART_W}" '
        f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'</rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#r{ry})">{text}</g>')

    # Cursor riding the wipe
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W:.1f}" height="{CELL_H-2}" '
        f'fill="{CURSOR}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD+ART_W:.0f}" '
        f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.7" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay+ROW_DUR:.3f}s"/>'
        f'</rect>'
    )

# Status bar
sep_y    = TB_H + ART_H + PAD * 0.4 + 2
status_y = sep_y + 19
parts += [
    f'<line x1="0" y1="{sep_y:.1f}" x2="{CANVAS_W}" y2="{sep_y:.1f}" '
    f'stroke="{CYAN}" stroke-opacity="0.2" stroke-width="1"/>',
    f'<text x="{PAD}" y="{status_y:.1f}" fill="{MUTED}" font-size="12">'
    f'Varaaa-arch@github:~$ <tspan fill="{GREEN}">whoami</tspan></text>',
    # Blinking cursor
    f'<rect x="{PAD + 196}" y="{status_y - 12:.1f}" width="8" height="13" fill="{CYAN}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
    f'dur="1s" repeatCount="indefinite"/>'
    f'</rect>',
]

parts.append("</svg>")
svg = "".join(parts)

with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg):,} bytes), {CANVAS_W}x{CANVAS_H}")
