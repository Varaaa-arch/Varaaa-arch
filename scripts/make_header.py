#!/usr/bin/env python3
"""
ZENITH.SYS — Header SVG (v2)
Concept: corrupted signal decoding into clarity.
  - Vertical "signal bars" background (not matrix rain) — cleaner, more dramatic
  - ZENITH title built from stacked horizontal slices that glitch independently
  - RGB chromatic aberration on title (permanent subtle offset, not just on trigger)
  - Typewriter prompt line at bottom with blinking cursor
  - Horizontal noise lines sweep through occasionally
  - Magenta + cyan dual-tone glow
"""
import os
import random
import math

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "..", "assets", "header.svg")

W, H = 860, 260

BG      = "#020810"
CYAN    = "#00fff5"
MAGENTA = "#ff00c8"
GREEN   = "#00ff9d"
YELLOW  = "#f5e642"
WHITE   = "#e0ffff"
MUTED   = "#15302e"
DIM     = "#081818"
SOFT    = "#2a6060"

random.seed(13)


# ── Signal bar background ──────────────────────────────────────────────────────
# Vertical bars of varying heights, like an audio spectrum, pulsing up and down
def make_signal_bars():
    bars = []
    bar_w   = 6
    gap     = 3
    step    = bar_w + gap
    n_bars  = W // step + 1

    for i in range(n_bars):
        x        = i * step
        h_pct    = random.uniform(0.08, 0.55)
        bar_h    = int(H * h_pct)
        bar_y    = H - bar_h
        delay    = random.uniform(0, 3.0)
        dur      = random.uniform(1.5, 4.0)
        h2_pct   = random.uniform(0.05, 0.50)
        bar_h2   = int(H * h2_pct)
        bar_y2   = H - bar_h2

        # Color: mostly muted, occasional cyan/magenta accent
        r = random.random()
        if r > 0.97:
            color   = CYAN
            opacity = "0.5"
        elif r > 0.94:
            color   = MAGENTA
            opacity = "0.4"
        else:
            color   = MUTED
            opacity = f"{random.uniform(0.3, 0.7):.2f}"

        bars.append(
            f'<rect x="{x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" '
            f'fill="{color}" opacity="{opacity}" rx="1">'
            f'<animate attributeName="height" values="{bar_h};{bar_h2};{bar_h}" '
            f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite" '
            f'calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>'
            f'<animate attributeName="y" values="{bar_y};{bar_y2};{bar_y}" '
            f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite" '
            f'calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>'
            f'</rect>'
        )
    return "\n".join(bars)


# ── Horizontal glitch slices (noise lines) ────────────────────────────────────
def make_noise_lines():
    lines = []
    for _ in range(8):
        y      = random.randint(20, H - 20)
        w_pct  = random.uniform(0.1, 0.6)
        x      = random.randint(0, int(W * (1 - w_pct)))
        lw     = int(W * w_pct)
        delay  = random.uniform(2.0, 8.0)
        dur    = random.uniform(3.0, 7.0)
        color  = CYAN if random.random() > 0.5 else MAGENTA
        lines.append(
            f'<rect x="{x}" y="{y}" width="{lw}" height="1" fill="{color}" opacity="0">'
            f'<animate attributeName="opacity" '
            f'values="0;0;0.6;0;0.4;0" '
            f'keyTimes="0;0.3;0.35;0.4;0.42;1" '
            f'dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="x" '
            f'values="{x};{x+random.randint(-20,20)};{x}" '
            f'dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'</rect>'
        )
    return "\n".join(lines)


css = """
@keyframes titlein {
  0%   { opacity: 0; letter-spacing: 40px; filter: blur(8px); }
  60%  { opacity: 1; letter-spacing: 20px; filter: blur(1px); }
  100% { opacity: 1; letter-spacing: 16px; filter: blur(0);   }
}
@keyframes subtitlein {
  0%   { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
@keyframes glitch {
  0%,89%,100% { transform: translate(0,0);     clip-path: inset(0 0 100% 0); }
  90%          { transform: translate(-6px, 0); clip-path: inset(15% 0 60% 0); }
  92%          { transform: translate( 6px, 0); clip-path: inset(55% 0 10% 0); }
  94%          { transform: translate(-3px, 0); clip-path: inset(30% 0 40% 0); }
  96%          { transform: translate( 3px, 0); clip-path: inset(70% 0  5% 0); }
}
@keyframes glitch2 {
  0%,87%,100% { transform: translate(0,0);    clip-path: inset(0 0 100% 0); }
  88%          { transform: translate(6px, 0); clip-path: inset(10% 0 70% 0); }
  90%          { transform: translate(-6px,0); clip-path: inset(60% 0 15% 0); }
  92%          { transform: translate(3px, 0); clip-path: inset(40% 0 30% 0); }
}
@keyframes blink {
  0%,49% { opacity: 1; }
  50%,100% { opacity: 0; }
}
@keyframes promptin {
  from { opacity: 0; transform: translateX(-8px); }
  to   { opacity: 1; transform: translateX(0); }
}
@keyframes scanline {
  0%   { transform: translateY(-4px); opacity: 0.06; }
  50%  { opacity: 0.09; }
  100% { transform: translateY(264px); opacity: 0.06; }
}
"""

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace">',
    f'<style>{css}</style>',
    '<defs>',

    # Vignette — stronger than before, pulls focus to center
    f'<radialGradient id="vig" cx="50%" cy="45%" r="60%">'
    f'<stop offset="0%" stop-color="{BG}" stop-opacity="0"/>'
    f'<stop offset="75%" stop-color="{BG}" stop-opacity="0.4"/>'
    f'<stop offset="100%" stop-color="#000" stop-opacity="0.92"/>'
    f'</radialGradient>',

    # Glow filter — title
    f'<filter id="titleglow" x="-25%" y="-25%" width="150%" height="150%">'
    f'<feGaussianBlur stdDeviation="4" result="b"/>'
    f'<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    f'</filter>',

    # Subtle glow for subtitle
    f'<filter id="subglow" x="-10%" y="-30%" width="120%" height="160%">'
    f'<feGaussianBlur stdDeviation="2" result="b"/>'
    f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    f'</filter>',

    f'<clipPath id="clip"><rect width="{W}" height="{H}"/></clipPath>',
    '</defs>',

    # Background
    f'<rect width="{W}" height="{H}" fill="{BG}"/>',
]

# Signal bars (bottom-anchored, clipped)
parts += [
    f'<g clip-path="url(#clip)" opacity="1">',
    make_signal_bars(),
    '</g>',
]

# Vignette over bars
parts.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')

# Top bar
parts += [
    f'<line x1="0" y1="24" x2="{W}" y2="24" stroke="{CYAN}" stroke-opacity="0.2" stroke-width="1"/>',
    f'<text x="16" y="16" fill="{SOFT}" font-size="10" letter-spacing="1">ZENITH.SYS</text>',
    f'<text x="{W//2}" y="16" fill="{SOFT}" font-size="10" text-anchor="middle" letter-spacing="2">'
    f'◈  SYSTEM ONLINE  ◈</text>',
    f'<text x="{W-16}" y="16" fill="{SOFT}" font-size="10" text-anchor="end" letter-spacing="1">'
    f'[SECURE]</text>',
]

# Corner brackets
B = 20
for (px, py, dx, dy) in [(4,4,B,B),(W-4,4,-B,B),(4,H-4,B,-B),(W-4,H-4,-B,-B)]:
    parts.append(
        f'<polyline points="{px+dx},{py} {px},{py} {px},{py+dy}" '
        f'fill="none" stroke="{CYAN}" stroke-width="1.5" stroke-opacity="0.6"/>'
    )

# Decorative horizontal dividers flanking the title area
CX = W // 2
TY = 118  # title baseline

# Side lines
parts += [
    f'<line x1="30" y1="{TY-60}" x2="{CX-130}" y2="{TY-60}" stroke="{CYAN}" stroke-opacity="0.3" stroke-width="1"/>',
    f'<line x1="{CX+130}" y1="{TY-60}" x2="{W-30}" y2="{TY-60}" stroke="{CYAN}" stroke-opacity="0.3" stroke-width="1"/>',
    # Diamond accents at line ends
    f'<rect x="{CX-132}" y="{TY-64}" width="8" height="8" fill="none" stroke="{CYAN}" stroke-width="1" stroke-opacity="0.5" transform="rotate(45,{CX-128},{TY-60})"/>',
    f'<rect x="{CX+124}" y="{TY-64}" width="8" height="8" fill="none" stroke="{CYAN}" stroke-width="1" stroke-opacity="0.5" transform="rotate(45,{CX+128},{TY-60})"/>',
]

# ── ZENITH title ──────────────────────────────────────────────────────────────
FS = 82  # font size

# Permanent chromatic aberration — red channel left, cyan channel right (subtle)
parts.append(
    f'<text x="{CX-3}" y="{TY}" text-anchor="middle" font-size="{FS}" font-weight="900" '
    f'letter-spacing="16" fill="{MAGENTA}" opacity="0.18">Bizar</text>'
)
parts.append(
    f'<text x="{CX+3}" y="{TY}" text-anchor="middle" font-size="{FS}" font-weight="900" '
    f'letter-spacing="16" fill="{CYAN}" opacity="0.18">Bizar</text>'
)

# Glitch layers (only fire in 88-96% window → looks like random bursts)
parts.append(
    f'<text x="{CX}" y="{TY}" text-anchor="middle" font-size="{FS}" font-weight="900" '
    f'letter-spacing="16" fill="{MAGENTA}" opacity="0.7" '
    f'style="animation: glitch 6s infinite 2s">Bizar</text>'
)
parts.append(
    f'<text x="{CX}" y="{TY}" text-anchor="middle" font-size="{FS}" font-weight="900" '
    f'letter-spacing="16" fill="{CYAN}" opacity="0.7" '
    f'style="animation: glitch2 6s infinite 2.2s">Bizar</text>'
)

# Main title — intro animation (letter-spacing collapse + blur clear)
parts.append(
    f'<text x="{CX}" y="{TY}" text-anchor="middle" font-size="{FS}" font-weight="900" '
    f'letter-spacing="16" fill="{WHITE}" filter="url(#titleglow)" '
    f'style="animation: titlein 1.2s cubic-bezier(0.2,0.8,0.2,1) 0.3s both">'
    f'Bizar</text>'
)

# Tagline
parts.append(
    f'<text x="{CX}" y="{TY+30}" text-anchor="middle" font-size="11.5" '
    f'letter-spacing="5.5" fill="{CYAN}" filter="url(#subglow)" '
    f'style="animation: subtitlein 0.6s ease-out 1.4s both; opacity:0">'
    f'FULL-STACK  ·  SECURITY  ·  OPEN SOURCE'
    f'</text>'
)

# ── Bottom prompt line ─────────────────────────────────────────────────────────
PY = H - 28
parts += [
    f'<line x1="0" y1="{PY - 10}" x2="{W}" y2="{PY - 10}" '
    f'stroke="{CYAN}" stroke-opacity="0.12" stroke-width="1"/>',

    # Prompt
    f'<text x="20" y="{PY}" font-size="12" '
    f'style="animation: promptin 0.4s ease-out 2.0s both; opacity:0">'
    f'<tspan fill="{GREEN}">❯</tspan>'
    f'<tspan fill="{SOFT}"> Varaaa-arch@github</tspan>'
    f'<tspan fill="{MUTED}">:</tspan>'
    f'<tspan fill="{CYAN}">~/profile</tspan>'
    f'<tspan fill="{SOFT}"> git push</tspan>'
    f'</text>',

    # Blinking cursor
    f'<text x="220" y="{PY}" font-size="12" fill="{CYAN}" '
    f'style="animation: promptin 0.1s ease-out 2.4s both, blink 1s step-end 2.5s infinite; opacity:0">'
    f'█</text>',

    # Right side — commit hash style
    f'<text x="{W-20}" y="{PY}" font-size="11" fill="{MUTED}" text-anchor="end">'
    f'on  main  ·  ✓ up to date</text>',
]

# Noise / glitch lines
parts += [
    f'<g clip-path="url(#clip)">',
    make_noise_lines(),
    '</g>',
]

# Scanline sweep
parts.append(
    f'<rect width="{W}" height="4" fill="{WHITE}" opacity="0.06" '
    f'style="animation: scanline 6s linear infinite"/>'
)

# Bottom border
parts.append(
    f'<line x1="0" y1="{H-1}" x2="{W}" y2="{H-1}" '
    f'stroke="{CYAN}" stroke-opacity="0.3" stroke-width="1"/>'
)

parts.append("</svg>")
svg = "\n".join(parts)

with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg):,} bytes), {W}x{H}")
