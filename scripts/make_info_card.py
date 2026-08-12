#!/usr/bin/env python3
"""
ZENITH.SYS — Cyberpunk Info Card SVG
Clean neofetch-style panel. No bar graphs — pure key/value rows.
Tight, readable, minimal noise.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "..", "assets", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H    = 460, 330
PAD     = 20
TB_H    = 30          # titlebar height
LINE_H  = 22
KEY_W   = 102         # key column width

BG      = "#050a0f"
BG2     = "#07111a"
CYAN    = "#00fff5"
GREEN   = "#00ff9d"
MAGENTA = "#ff00c8"
YELLOW  = "#f5e642"
WHITE   = "#e0ffff"
MUTED   = "#2a5555"
DIM     = "#0d2020"
SOFT    = "#7ab8b0"

# ── Profile data ──────────────────────────────────────────────────────────────
PROFILE = {
    "user":     "Varaaa-arch",
    "host":     "github.com",
    "os":       "Arch Linux",
    "shell":    "zsh + tmux",
    "editor":   "Neovim",
    "uptime":   "∞ (no sleep)",
}

# Row definitions — (type, key, value)
# Separator = thin rule between sections
ROWS = [
    ("host",),
    ("sep",),
    ("kv", "OS",       "Arch Linux"),
    ("kv", "Shell",    "zsh + tmux"),
    ("kv", "Editor",   "Neovim"),
    ("kv", "WM",       "Hyprland"),
    ("sep",),
    ("kv", "Status",   "Student · SWE"),
    ("kv", "Focus",    "Full-Stack · Security"),
    ("kv", "Location", "Jakarta, Indonesia"),
    ("sep",),
    ("kv", "Lang",     "TypeScript · Python · Go"),
    ("kv", "Web",      "Next.js · React · Tailwind"),
    ("kv", "Infra",    "Docker · PostgreSQL · Redis"),
    ("sep",),
    ("tags", ["open-source", "night-owl", "arch btw", "coffee++"]),
]


def esc(s): return html.escape(str(s))


def row_inner(row, y, idx):
    kind = row[0]

    if kind == "sep":
        return f'<line x1="{PAD}" y1="{y:.1f}" x2="{W - PAD}" y2="{y:.1f}" stroke="{DIM}" stroke-width="1"/>'

    if kind == "host":
        return (
            f'<text x="{PAD}" y="{y:.1f}" font-size="14" font-weight="700" letter-spacing="0.5">'
            f'<tspan fill="{GREEN}">{esc(PROFILE["user"])}</tspan>'
            f'<tspan fill="{MUTED}">@</tspan>'
            f'<tspan fill="{CYAN}">{esc(PROFILE["host"])}</tspan>'
            f'</text>'
        )

    if kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        return (
            f'<text x="{PAD}" y="{y:.1f}" font-size="12">'
            f'<tspan fill="{YELLOW}" font-weight="600">{key}</tspan>'
            f'</text>'
            f'<text x="{PAD + KEY_W}" y="{y:.1f}" fill="{SOFT}" font-size="12">{val}</text>'
        )

    if kind == "tags":
        tags = row[1]
        tx   = PAD
        parts = []
        for tag in tags:
            tw = len(tag) * 7.2 + 16
            parts += [
                f'<rect x="{tx:.1f}" y="{y - 13:.1f}" width="{tw:.0f}" height="16" '
                f'rx="8" fill="{DIM}" stroke="{CYAN}" stroke-width="0.5" stroke-opacity="0.6"/>',
                f'<text x="{tx + tw/2:.1f}" y="{y:.1f}" fill="{CYAN}" font-size="10" '
                f'text-anchor="middle" opacity="0.85">{esc(tag)}</text>',
            ]
            tx += tw + 6
        return "".join(parts)

    return ""


def wrap_animated(inner, idx):
    """Staggered fade + slide in."""
    if STATIC or not inner:
        return f"<g>{inner}</g>"
    delay = 0.10 + idx * 0.05
    return (
        f'<g opacity="0" transform="translate(0,5)">'
        f'{inner}'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{delay:.2f}s" dur="0.3s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 5" to="0 0" begin="{delay:.2f}s" dur="0.3s" fill="freeze" '
        f'calcMode="spline" keySplines="0.25 0.8 0.25 1"/>'
        f'</g>'
    )


# ── Build SVG ─────────────────────────────────────────────────────────────────
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
    f'viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',

    # Defs
    '<defs>'
    f'<linearGradient id="icbg" x1="0" y1="0" x2="1" y2="1">'
    f'<stop offset="0%" stop-color="{BG2}"/>'
    f'<stop offset="100%" stop-color="{BG}"/>'
    f'</linearGradient>'
    '</defs>',

    # Background
    f'<rect width="{W}" height="{H}" rx="10" fill="url(#icbg)"/>',
    # Outer border
    f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="none" '
    f'stroke="{CYAN}" stroke-width="1" stroke-opacity="0.35"/>',

    # Titlebar divider
    f'<line x1="0" y1="{TB_H}" x2="{W}" y2="{TB_H}" '
    f'stroke="{CYAN}" stroke-opacity="0.25" stroke-width="1"/>',
]

# Traffic lights
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TB_H/2}" r="4.5" fill="{c}"/>')

# Titlebar label
parts.append(
    f'<text x="{W/2}" y="{TB_H/2 + 4}" fill="{MUTED}" font-size="11" text-anchor="middle">'
    f'Varaaa-arch@github: ~$ neofetch</text>'
)

# HUD corner brackets (just 4 corners, subtle)
B = 12
for (px, py, dx, dy) in [(1,1,B,B),(W-1,1,-B,B),(1,H-1,B,-B),(W-1,H-1,-B,-B)]:
    parts.append(
        f'<polyline points="{px+dx},{py} {px},{py} {px},{py+dy}" '
        f'fill="none" stroke="{CYAN}" stroke-width="1.5" stroke-opacity="0.5"/>'
    )

# Render rows
y      = TB_H + 28
anim_i = 0
for row in ROWS:
    kind = row[0]

    if kind == "sep":
        inner = row_inner(row, y - 6, anim_i)
        parts.append(inner)          # separators not animated — just render direct
        y += 6
        continue

    if kind == "host":
        inner = row_inner(row, y, anim_i)
        parts.append(wrap_animated(inner, anim_i))
        y     += LINE_H + 2
        anim_i += 1
        continue

    if kind == "kv":
        inner = row_inner(row, y, anim_i)
        parts.append(wrap_animated(inner, anim_i))
        y     += LINE_H
        anim_i += 1
        continue

    if kind == "tags":
        y     += 4
        inner  = row_inner(row, y, anim_i)
        parts.append(wrap_animated(inner, anim_i))
        y     += LINE_H
        anim_i += 1
        continue

parts.append("</svg>")
svg = "".join(parts)

# Auto-adjust height: pad 16px below last element
# (We set H statically above — just ensure it fits)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg):,} bytes), {W}x{H}")
