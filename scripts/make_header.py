#!/usr/bin/env python3
"""
ZENITH.SYS — Header SVG
Full-width boot-sequence header. Matrix rain background, glitch title,
minimal terminal boot lines. Clean, not noisy.
"""
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "..", "assets", "header.svg")

W, H   = 860, 260
COLS   = 55           # matrix rain columns — keep sparse

BG      = "#050a0f"
CYAN    = "#00fff5"
MAGENTA = "#ff00c8"
GREEN   = "#00ff9d"
YELLOW  = "#f5e642"
MUTED   = "#1a3535"
DIM     = "#0a1a1a"
WHITE   = "#e0ffff"

MATRIX_CHARS = "ｦｧｨｩｪｫｬｭｮｯｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789"

random.seed(7)


def make_rain_col(idx, total):
    x        = (idx / total) * W + W / total / 2
    n        = random.randint(5, 14)
    delay    = random.uniform(0, 5.0)
    dur      = random.uniform(2.8, 6.0)
    spacing  = 16
    chars    = []
    for i in range(n):
        ch  = random.choice(MATRIX_CHARS)
        col = WHITE if i == 0 else (GREEN if i < 2 else MUTED)
        op  = "1" if i == 0 else f"{max(0.05, 1 - i * (0.9/n)):.2f}"
        chars.append(
            f'<text x="{x:.1f}" y="{i * spacing}" fill="{col}" opacity="{op}" font-size="12">{ch}</text>'
        )
    gh = n * spacing
    return (
        f'<g style="animation-delay:{delay:.2f}s;animation-duration:{dur:.2f}s">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 {-gh}" to="0 {H + gh}" '
        f'begin="{delay:.2f}s" dur="{dur:.2f}s" repeatCount="indefinite"/>'
        + "".join(chars) + "</g>"
    )


# 5 tight boot lines — punchy, no fluff
BOOT_LINES = [
    (0.4,  CYAN,    "ZENITH.SYS v3.0 — kernel loaded"),
    (1.0,  GREEN,   "all subsystems nominal  [OK]"),
    (1.7,  YELLOW,  "⚡ compiling dreams...  100%"),
    (2.4,  MAGENTA, "WARNING: creativity overflow"),
    (3.1,  WHITE,   "ready. welcome back, operator."),
]

css = f"""
@keyframes glitch1 {{
  0%,90%,100% {{ clip-path:inset(0 0 100% 0); transform:translate(0,0); }}
  91% {{ clip-path:inset(20% 0 55% 0); transform:translate(-5px,0); }}
  93% {{ clip-path:inset(60% 0 15% 0); transform:translate(5px,0); }}
  95% {{ clip-path:inset(40% 0 35% 0); transform:translate(-3px,0); }}
}}
@keyframes glitch2 {{
  0%,88%,100% {{ clip-path:inset(0 0 100% 0); transform:translate(0,0); }}
  89% {{ clip-path:inset(10% 0 70% 0); transform:translate(5px,0); }}
  91% {{ clip-path:inset(50% 0 25% 0); transform:translate(-5px,0); }}
  93% {{ clip-path:inset(75% 0 5%  0); transform:translate(3px,0); }}
}}
@keyframes blink {{
  0%,49% {{ opacity:1; }} 50%,100% {{ opacity:0; }}
}}
@keyframes typein {{
  from {{ opacity:0; transform:translateX(-6px); }}
  to   {{ opacity:1; transform:translateX(0); }}
}}
.bl  {{ opacity:0; animation: typein 0.35s ease-out forwards; }}
.cur {{ animation: blink 1s step-end infinite; }}
"""

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace">',
    f'<style>{css}</style>',
    '<defs>',
    f'<radialGradient id="vig" cx="50%" cy="50%" r="65%">'
    f'<stop offset="0%" stop-color="{BG}" stop-opacity="0"/>'
    f'<stop offset="100%" stop-color="#000" stop-opacity="0.85"/>'
    f'</radialGradient>',
    f'<filter id="glow">'
    f'<feGaussianBlur stdDeviation="3" result="b"/>'
    f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    f'</filter>',
    f'<clipPath id="clip"><rect width="{W}" height="{H}"/></clipPath>',
    '</defs>',

    # BG
    f'<rect width="{W}" height="{H}" fill="{BG}"/>',
    # Grid (very faint)
    *[f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{MUTED}" stroke-opacity="0.1"/>'
      for y in range(0, H, 24)],
    *[f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{MUTED}" stroke-opacity="0.06"/>'
      for x in range(0, W, 48)],

    # Matrix rain
    f'<g clip-path="url(#clip)" opacity="0.28" font-family="monospace">',
    *[make_rain_col(i, COLS) for i in range(COLS)],
    '</g>',

    # Vignette
    f'<rect width="{W}" height="{H}" fill="url(#vig)"/>',
]

# Top bar
parts += [
    f'<line x1="0" y1="22" x2="{W}" y2="22" stroke="{CYAN}" stroke-opacity="0.25" stroke-width="1"/>',
    f'<text x="16" y="15" fill="{MUTED}" font-size="10">ZENITH.SYS</text>',
    f'<text x="{W//2}" y="15" fill="{MUTED}" font-size="10" text-anchor="middle">SYSTEM ONLINE</text>',
    f'<text x="{W-16}" y="15" fill="{MUTED}" font-size="10" text-anchor="end">[SECURE]</text>',
]

# Corner brackets
B = 18
for (px, py, dx, dy) in [(4,4,B,B),(W-4,4,-B,B),(4,H-4,B,-B),(W-4,H-4,-B,-B)]:
    parts.append(
        f'<polyline points="{px+dx},{py} {px},{py} {px},{py+dy}" '
        f'fill="none" stroke="{CYAN}" stroke-width="2" stroke-opacity="0.7"/>'
    )

# ── ZENITH title — centered in upper half ─────────────────────────────────────
TX, TY = W // 2, 108

# Shadow
parts.append(
    f'<text x="{TX+3}" y="{TY+3}" text-anchor="middle" font-size="76" '
    f'font-weight="900" letter-spacing="16" fill="{MAGENTA}" opacity="0.2">ZENITH</text>'
)
# Glitch 1 (magenta)
parts.append(
    f'<text x="{TX}" y="{TY}" text-anchor="middle" font-size="76" '
    f'font-weight="900" letter-spacing="16" fill="{MAGENTA}" opacity="0.65" '
    f'style="animation:glitch1 5s infinite 1.5s">ZENITH</text>'
)
# Glitch 2 (cyan)
parts.append(
    f'<text x="{TX}" y="{TY}" text-anchor="middle" font-size="76" '
    f'font-weight="900" letter-spacing="16" fill="{CYAN}" opacity="0.65" '
    f'style="animation:glitch2 5s infinite 1.7s">ZENITH</text>'
)
# Main (white + glow)
parts.append(
    f'<text x="{TX}" y="{TY}" text-anchor="middle" font-size="76" '
    f'font-weight="900" letter-spacing="16" fill="{WHITE}" filter="url(#glow)">ZENITH</text>'
)

# Tagline — single sharp line
parts.append(
    f'<text x="{TX}" y="{TY + 26}" text-anchor="middle" '
    f'font-size="12" letter-spacing="5" fill="{CYAN}" opacity="0.75">'
    f'FULL-STACK  ·  SECURITY  ·  OPEN SOURCE'
    f'</text>'
)

# Decorative line flanking tagline
RY = TY - 54
parts += [
    f'<line x1="{TX-240}" y1="{RY}" x2="{TX-80}" y2="{RY}" stroke="{CYAN}" stroke-opacity="0.4" stroke-width="1"/>',
    f'<line x1="{TX+80}"  y1="{RY}" x2="{TX+240}" y2="{RY}" stroke="{CYAN}" stroke-opacity="0.4" stroke-width="1"/>',
    f'<polygon points="{TX-82},{RY} {TX-74},{RY-4} {TX-74},{RY+4}" fill="{CYAN}" opacity="0.5"/>',
    f'<polygon points="{TX+82},{RY} {TX+74},{RY-4} {TX+74},{RY+4}" fill="{CYAN}" opacity="0.5"/>',
]

# ── Boot lines — bottom quarter ────────────────────────────────────────────────
LOG_Y  = 158
LOG_DH = 16

for i, (delay, color, msg) in enumerate(BOOT_LINES):
    y = LOG_Y + i * LOG_DH
    parts.append(
        f'<text class="bl" x="28" y="{y}" font-size="11" '
        f'style="animation-delay:{delay:.1f}s">'
        f'<tspan fill="{GREEN}">›</tspan> '
        f'<tspan fill="{color}">{msg}</tspan>'
        f'</text>'
    )

# Blinking cursor after last line
cursor_y    = LOG_Y + len(BOOT_LINES) * LOG_DH
cursor_delay = BOOT_LINES[-1][0] + 0.5
parts.append(
    f'<text x="28" y="{cursor_y}" font-size="11" fill="{GREEN}" '
    f'style="animation:typein 0.1s {cursor_delay:.1f}s forwards;opacity:0">'
    f'› <tspan fill="{WHITE}" class="cur">█</tspan></text>'
)

# Bottom border
parts.append(
    f'<line x1="0" y1="{H-1}" x2="{W}" y2="{H-1}" '
    f'stroke="{CYAN}" stroke-opacity="0.35" stroke-width="1"/>'
)

# Scanline sweep
parts.append(
    f'<rect width="{W}" height="2" fill="{WHITE}" opacity="0.025">'
    f'<animateTransform attributeName="transform" type="translate" '
    f'from="0 0" to="0 {H}" dur="5s" repeatCount="indefinite"/>'
    f'</rect>'
)

parts.append("</svg>")
svg = "\n".join(parts)

with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg):,} bytes), {W}x{H}")
