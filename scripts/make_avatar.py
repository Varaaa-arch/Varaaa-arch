#!/usr/bin/env python3
"""
ZENITH.SYS — ASCII Block Art SVG Generator
Generates a stylized ASCII block art panel representing a developer avatar.
Uses block drawing characters (░▒▓█ etc) for a unique look compared to
traditional photo-to-ASCII conversion.

The art "prints" itself left-to-right, top-to-bottom like a terminal output.
No photo needed — this is a handcrafted symbolic avatar.
"""
import os
import html

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "avatar.svg")
STATIC = bool(os.environ.get("STATIC"))

# Colors
BG      = "#050a0f"
BG2     = "#070d14"
FRAME   = "#00fff540"
CYAN    = "#00fff5"
GREEN   = "#00ff9d"
MAGENTA = "#ff00c8"
YELLOW  = "#f5e642"
WHITE   = "#e0ffff"
MUTED   = "#1a4a4a"
DIM     = "#0d2a2a"

# ─── The ASCII Block Art (stylized dev avatar) ────────────────────────────────
# Using Unicode block elements for a unique pixel-art style:
# Space = empty, ░ = light, ▒ = medium, ▓ = dark, █ = solid, ═║╔╗╚╝ = box draw
ART_LINES = [
    "                    ╔══════════════════╗                    ",
    "                    ║  ┌────────────┐  ║                    ",
    "                    ║  │  ▓▓▓▓▓▓▓▓  │  ║                    ",
    "                    ║  │ ▓▓      ▓▓ │  ║                    ",
    "                    ║  │ ▓▓  ██  ▓▓ │  ║                    ",
    "                    ║  │ ▓▓      ▓▓ │  ║                    ",
    "                    ║  │  ▓▓▓██▓▓▓  │  ║                    ",
    "                    ║  │   ░░░░░░   │  ║                    ",
    "                    ║  └────────────┘  ║                    ",
    "                    ╚══════════════════╝                    ",
    "                                                            ",
    "   ┌─ SYSTEM IDENTIFICATION ─────────────────────────────┐  ",
    "   │  USER:    Varaaa-arch                                │  ",
    "   │  HOST:    github.com                                 │  ",
    "   │  SHELL:   /bin/code                                  │  ",
    "   │  STATUS:  ● ONLINE — building the future             │  ",
    "   └──────────────────────────────────────────────────────┘  ",
]

# Color rules per line — (start_col, end_col, color) 
# Applied left to right; last matching rule wins per char
# We'll color entire lines for simplicity
LINE_COLORS = [
    CYAN,    # ╔══
    CYAN,    # ║ ┌
    MUTED,   # ║ │ ▓▓▓
    MUTED,   # ║ │ ▓▓  
    WHITE,   # ║ │ ▓▓ ██ (eyes)
    MUTED,   # ║ │ ▓▓  
    MUTED,   # ║ │ smirk
    DIM,     # ║ │ shadow
    CYAN,    # ║ └
    CYAN,    # ╚══
    MUTED,   # blank
    CYAN,    # ┌─ SYSTEM
    GREEN,   # USER
    CYAN,    # HOST
    GREEN,   # SHELL
    YELLOW,  # STATUS ●
    CYAN,    # └────
]

CELL_W = 9.2
CELL_H = 15
PAD = 16
TITLEBAR_H = 30
STATUS_H = 28

n_cols = max(len(l) for l in ART_LINES)
n_rows = len(ART_LINES)
ART_W = int(n_cols * CELL_W)
ART_H = n_rows * CELL_H
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + ART_H + STATUS_H + PAD * 2

# reveal timing
ROW_DUR = 0.09
STAGGER = 0.09

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="avbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
    f'<filter id="cynglow" x="-10%" y="-10%" width="120%" height="120%">'
    f'<feGaussianBlur stdDeviation="1.5" result="b"/>'
    f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    f'</filter>'
    '</defs>',
    
    # Background
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="10" fill="url(#avbg)"/>',
    # Border with cyan glow
    f'<rect x="0.5" y="0.5" width="{CANVAS_W-1}" height="{CANVAS_H-1}" rx="10" '
    f'fill="none" stroke="{CYAN}" stroke-width="1" stroke-opacity="0.4" filter="url(#cynglow)"/>',
    
    # Title bar
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}" '
    f'stroke="{FRAME}" stroke-width="1"/>',
]

# Traffic light dots
for i, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{col}"/>')

# Title bar text
parts.append(
    f'<text x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="11.5" '
    f'text-anchor="middle">Varaaa-arch@github: ~$ cat identity.txt</text>'
)

# Scanline overlay (ultra subtle)
parts.append(
    f'<rect x="0" y="{TITLEBAR_H}" width="{CANVAS_W}" height="{ART_H + STATUS_H + PAD*2}" '
    f'fill="none" rx="0" style="background: repeating-linear-gradient(0deg, transparent, transparent 1px, #00000015 1px, #00000015 2px)"/>'
)

art_top = TITLEBAR_H + PAD

# Render each line
font_size = CELL_H * 0.82
for ry, line in enumerate(ART_LINES):
    y = art_top + ry * CELL_H + CELL_H * 0.78
    row_y = art_top + ry * CELL_H
    delay = ry * STAGGER
    color = LINE_COLORS[ry] if ry < len(LINE_COLORS) else WHITE
    safe = html.escape(line)
    
    text = (
        f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{color}" '
        f'font-size="{font_size:.1f}" letter-spacing="0">{safe}</text>'
    )
    
    if STATIC:
        parts.append(text)
        continue
    
    # Clip wipe reveal (left to right)
    row_w = len(line) * CELL_W
    parts.append(
        f'<clipPath id="ar{ry}"><rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H}" width="0">'
        f'<animate attributeName="width" from="0" to="{row_w:.0f}" '
        f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'</rect></clipPath>'
    )
    parts.append(f'<g clip-path="url(#ar{ry})">{text}</g>')
    
    # Cursor block riding the wipe
    parts.append(
        f'<rect y="{row_y+1:.1f}" width="{CELL_W:.1f}" height="{CELL_H-2}" fill="{CYAN}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD + row_w:.0f}" '
        f'begin="{delay:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.6" begin="{delay:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{delay + ROW_DUR:.3f}s"/>'
        f'</rect>'
    )

# Status bar
status_y_line = art_top + ART_H + PAD * 0.5
status_y_text = status_y_line + 18
finish_delay = n_rows * STAGGER + ROW_DUR + 0.2

parts.append(
    f'<line x1="0" y1="{status_y_line:.1f}" x2="{CANVAS_W}" y2="{status_y_line:.1f}" '
    f'stroke="{FRAME}" stroke-width="1"/>'
)
parts.append(
    f'<text x="{PAD}" y="{status_y_text:.1f}" fill="{MUTED}" font-size="12">'
    f'Varaaa-arch@github:~$ <tspan fill="{GREEN}">whoami</tspan></text>'
)
# Blinking cursor
parts.append(
    f'<rect x="{PAD + 170}" y="{status_y_text - 11:.1f}" width="8" height="13" fill="{CYAN}">'
    f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
    f'dur="1.1s" repeatCount="indefinite"/>'
    f'</rect>'
)

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg):,} bytes), {CANVAS_W}x{CANVAS_H}")
