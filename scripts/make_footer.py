#!/usr/bin/env python3
"""
ZENITH.SYS — Animated Footer SVG
A cyberpunk-style footer with:
  - Animated sine wave / oscilloscope pulse (pure CSS/SVG)
  - System status indicators (ping dots)
  - "Powered by caffeine" terminal output line
  - Subtle scan line sweep
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets", "footer.svg")

W, H = 860, 80

BG      = "#050a0f"
CYAN    = "#00fff5"
GREEN   = "#00ff9d"
MAGENTA = "#ff00c8"
MUTED   = "#1a3535"
DIM     = "#0a1f1f"
WHITE   = "#e0ffff"

# Generate wave path points (sine wave)
def make_wave(amplitude, frequency, phase, n_points=200):
    points = []
    for i in range(n_points + 1):
        x = (i / n_points) * W
        y = H/2 + amplitude * math.sin(2 * math.pi * frequency * i / n_points + phase)
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)

wave1 = make_wave(amplitude=10, frequency=3, phase=0)
wave2 = make_wave(amplitude=6, frequency=5, phase=1.2)
wave3 = make_wave(amplitude=4, frequency=8, phase=2.4)

css = """
@keyframes wave1 {
  0%   { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -860; }
}
@keyframes wave2 {
  0%   { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -860; }
}
@keyframes wave3 {
  0%   { stroke-dashoffset: 0; }
  100% { stroke-dashoffset: -860; }
}
@keyframes ping {
  0%,100% { opacity: 1; r: 3; }
  50% { opacity: 0.4; r: 5; }
}
@keyframes scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
"""

# Scrolling text content
scroll_text = (
    "  ❯ Varaaa-arch@github  ·  full-stack developer  ·  security enthusiast  ·  "
    "open source contributor  ·  coffee dependent  ·  arch linux btw  ·  "
    "building the future one commit at a time  ·  "
    "❯ Varaaa-arch@github  ·  full-stack developer  ·  security enthusiast  ·  "
    "open source contributor  ·  coffee dependent  ·  arch linux btw  ·  "
    "building the future one commit at a time  ·  "
)

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" font-family="ui-monospace, SFMono-Regular, Consolas, monospace">',
    f'<style>{css}</style>',
    f'<defs>'
    f'<clipPath id="ftclip"><rect width="{W}" height="{H}"/></clipPath>'
    f'<linearGradient id="ftbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0%" stop-color="{DIM}"/>'
    f'<stop offset="100%" stop-color="{BG}"/>'
    f'</linearGradient>'
    f'</defs>',
    
    # Background
    f'<rect width="{W}" height="{H}" fill="{BG}"/>',
    # Top border line
    f'<line x1="0" y1="0" x2="{W}" y2="0" stroke="{CYAN}" stroke-opacity="0.4" stroke-width="1"/>',
    
    # Waves (clipped)
    f'<g clip-path="url(#ftclip)">',
    # Wave 1 — main cyan wave
    f'<polyline points="{wave1}" fill="none" stroke="{CYAN}" stroke-width="1.5" '
    f'stroke-opacity="0.6" stroke-dasharray="4 2">'
    f'<animateTransform attributeName="transform" type="translate" '
    f'from="0 0" to="{W} 0" dur="4s" repeatCount="indefinite"/>'
    f'</polyline>',
    # Copy for seamless loop
    f'<polyline points="{wave1}" fill="none" stroke="{CYAN}" stroke-width="1.5" '
    f'stroke-opacity="0.6" stroke-dasharray="4 2">'
    f'<animateTransform attributeName="transform" type="translate" '
    f'from="{-W} 0" to="0 0" dur="4s" repeatCount="indefinite"/>'
    f'</polyline>',
    
    # Wave 2 — magenta accent
    f'<polyline points="{wave2}" fill="none" stroke="{MAGENTA}" stroke-width="1" '
    f'stroke-opacity="0.3">'
    f'<animateTransform attributeName="transform" type="translate" '
    f'from="0 0" to="{W} 0" dur="6s" repeatCount="indefinite"/>'
    f'</polyline>',
    f'<polyline points="{wave2}" fill="none" stroke="{MAGENTA}" stroke-width="1" '
    f'stroke-opacity="0.3">'
    f'<animateTransform attributeName="transform" type="translate" '
    f'from="{-W} 0" to="0 0" dur="6s" repeatCount="indefinite"/>'
    f'</polyline>',
    
    # Wave 3 — green subtle
    f'<polyline points="{wave3}" fill="none" stroke="{GREEN}" stroke-width="0.75" '
    f'stroke-opacity="0.2">'
    f'<animateTransform attributeName="transform" type="translate" '
    f'from="0 0" to="{W} 0" dur="3s" repeatCount="indefinite"/>'
    f'</polyline>',
    f'<polyline points="{wave3}" fill="none" stroke="{GREEN}" stroke-width="0.75" '
    f'stroke-opacity="0.2">'
    f'<animateTransform attributeName="transform" type="translate" '
    f'from="{-W} 0" to="0 0" dur="3s" repeatCount="indefinite"/>'
    f'</polyline>',
    f'</g>',
    
    # Status dots (left side)
    f'<circle cx="20" cy="{H//2}" r="3" fill="{GREEN}">'
    f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/>'
    f'<animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite"/>'
    f'</circle>',
    f'<text x="28" y="{H//2 + 4}" fill="{MUTED}" font-size="10">SYS</text>',
    
    f'<circle cx="72" cy="{H//2}" r="3" fill="{CYAN}">'
    f'<animate attributeName="opacity" values="1;0.3;1" dur="3s" repeatCount="indefinite" begin="0.5s"/>'
    f'</circle>',
    f'<text x="80" y="{H//2 + 4}" fill="{MUTED}" font-size="10">NET</text>',
    
    f'<circle cx="122" cy="{H//2}" r="3" fill="{MAGENTA}">'
    f'<animate attributeName="opacity" values="1;0.3;1" dur="2.5s" repeatCount="indefinite" begin="1s"/>'
    f'</circle>',
    f'<text x="130" y="{H//2 + 4}" fill="{MUTED}" font-size="10">API</text>',
    
    # Scrolling text (bottom strip)
    f'<line x1="0" y1="{H - 20}" x2="{W}" y2="{H - 20}" '
    f'stroke="{MUTED}" stroke-opacity="0.5" stroke-width="0.5"/>',
    f'<clipPath id="scrollclip"><rect x="160" y="{H-20}" width="{W-160}" height="20"/></clipPath>',
    f'<g clip-path="url(#scrollclip)">',
    f'<text y="{H - 6}" fill="{MUTED}" font-size="10" '
    f'style="animation: scroll 30s linear infinite">'
    f'{scroll_text}</text>',
    f'</g>',
    
    # Right side version info
    f'<text x="{W - 14}" y="{H//2 + 4}" fill="{MUTED}" font-size="10" text-anchor="end">'
    f'v2.5.1</text>',
]

parts.append("</svg>")
svg = "\n".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg):,} bytes), {W}x{H}")
