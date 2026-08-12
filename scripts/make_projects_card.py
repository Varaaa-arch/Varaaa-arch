#!/usr/bin/env python3
"""
ZENITH.SYS — Featured Projects Card SVG
Cyberpunk terminal-style grid of pinned projects.
Each card: name + one-liner + language dot + star count.
No gradients per-card — just clean dark panels with neon accents.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "..", "assets", "projects-card.svg")
STATIC = bool(os.environ.get("STATIC"))

# ── Projects data — edit this section ─────────────────────────────────────────
PROJECTS = [
    {
        "name":  "nexus-api",
        "desc":  "High-throughput REST/gRPC gateway with rate limiting & JWT auth",
        "lang":  "Go",
        "lang_color": "#00ADD8",
        "stars": 142,
        "tags":  ["backend", "grpc"],
    },
    {
        "name":  "phantom-ui",
        "desc":  "Minimal component library with dark-by-default design system",
        "lang":  "TypeScript",
        "lang_color": "#3178C6",
        "stars": 89,
        "tags":  ["frontend", "oss"],
    },
    {
        "name":  "vaultd",
        "desc":  "Self-hosted secret manager — AES-256 encrypted, CLI-first",
        "lang":  "Rust",
        "lang_color": "#CE412B",
        "stars": 67,
        "tags":  ["security", "cli"],
    },
    {
        "name":  "recon-suite",
        "desc":  "Passive OSINT & subdomain enumeration toolkit for bug bounty",
        "lang":  "Python",
        "lang_color": "#3776AB",
        "stars": 210,
        "tags":  ["security", "osint"],
    },
    {
        "name":  "k8s-shim",
        "desc":  "Lightweight sidecar for injecting secrets into K8s pods at runtime",
        "lang":  "Go",
        "lang_color": "#00ADD8",
        "stars": 54,
        "tags":  ["devops", "k8s"],
    },
    {
        "name":  "Varaaa-arch",
        "desc":  "This GitHub profile — pure SVG, zero external services",
        "lang":  "Python",
        "lang_color": "#3776AB",
        "stars": 33,
        "tags":  ["meta", "oss"],
    },
]

# ── Layout constants ───────────────────────────────────────────────────────────
COLS       = 2
CARD_W     = 400
CARD_H     = 108
GAP        = 12
H_PAD      = 24          # outer horizontal padding
V_PAD      = 20          # outer vertical padding (top/bottom)
TB_H       = 30          # titlebar

ROWS       = -(-len(PROJECTS) // COLS)   # ceil div
TOTAL_W    = COLS * CARD_W + (COLS - 1) * GAP + H_PAD * 2
TOTAL_H    = TB_H + V_PAD + ROWS * CARD_H + (ROWS - 1) * GAP + V_PAD

# Colors
BG         = "#050a0f"
BG2        = "#07111a"
CARD_BG    = "#070e17"
CARD_BG2   = "#060c14"
CYAN       = "#00fff5"
GREEN      = "#00ff9d"
MAGENTA    = "#ff00c8"
YELLOW     = "#f5e642"
WHITE      = "#e0ffff"
MUTED      = "#2a5555"
DIM        = "#0d1e1e"
SOFT       = "#7ab8b0"
TAG_BG     = "#0a1a1a"

# Tag color per label
TAG_COLORS = {
    "backend":  "#00fff5",
    "frontend": "#a78bfa",
    "security": "#ff00c8",
    "devops":   "#f5e642",
    "osint":    "#ff6b6b",
    "grpc":     "#00fff5",
    "cli":      "#00ff9d",
    "k8s":      "#60a5fa",
    "oss":      "#00ff9d",
    "meta":     "#f5e642",
}
DEFAULT_TAG = "#6ab8a8"


def esc(s): return html.escape(str(s))


def star_icon(x, y, color):
    """Simple 5-point star SVG at (x,y), size ~10px."""
    # Precomputed 5-star path centered at 0,0 r_outer=5 r_inner=2.5
    pts = "0,-5 1.5,-1.8 5,-1.5 2.5,1.2 3.1,5 0,3 -3.1,5 -2.5,1.2 -5,-1.5 -1.5,-1.8"
    return (
        f'<polygon points="{pts}" fill="{color}" opacity="0.8" '
        f'transform="translate({x},{y}) scale(0.85)"/>'
    )


def render_card(proj, cx, cy, idx):
    """Render a single project card at (cx, cy)."""
    delay  = 0.15 + idx * 0.07
    name   = esc(proj["name"])
    desc   = esc(proj["desc"])
    lang   = esc(proj["lang"])
    lc     = proj["lang_color"]
    stars  = proj["stars"]
    tags   = proj["tags"]

    inner = []

    # Card background
    inner.append(
        f'<rect x="{cx}" y="{cy}" width="{CARD_W}" height="{CARD_H}" rx="7" '
        f'fill="{CARD_BG}" stroke="{CYAN}" stroke-width="0.75" stroke-opacity="0.3"/>'
    )

    # Left accent bar
    inner.append(
        f'<rect x="{cx}" y="{cy + 14}" width="3" height="{CARD_H - 28}" rx="1.5" fill="{CYAN}" opacity="0.5"/>'
    )

    # Project name
    inner.append(
        f'<text x="{cx + 16}" y="{cy + 26}" font-size="13.5" font-weight="700" '
        f'fill="{WHITE}" letter-spacing="0.3">{name}</text>'
    )

    # Description — wrap at ~52 chars
    words    = proj["desc"].split()
    line1    = ""
    line2    = ""
    for w in words:
        candidate = (line1 + " " + w).strip()
        if len(candidate) <= 52:
            line1 = candidate
        else:
            line2 = (line2 + " " + w).strip()

    line1_esc = esc(line1)
    line2_esc = esc(line2)

    inner.append(
        f'<text x="{cx + 16}" y="{cy + 46}" font-size="11" fill="{SOFT}">{line1_esc}</text>'
    )
    if line2_esc:
        inner.append(
            f'<text x="{cx + 16}" y="{cy + 59}" font-size="11" fill="{SOFT}">{line2_esc}</text>'
        )

    # Tags (bottom left)
    tag_x = cx + 16
    tag_y = cy + CARD_H - 18
    for tag in tags[:3]:
        tc   = TAG_COLORS.get(tag, DEFAULT_TAG)
        tw   = len(tag) * 6.5 + 12
        inner.append(
            f'<rect x="{tag_x:.1f}" y="{tag_y - 11}" width="{tw:.0f}" height="14" '
            f'rx="7" fill="{TAG_BG}" stroke="{tc}" stroke-width="0.5" stroke-opacity="0.7"/>'
        )
        inner.append(
            f'<text x="{tag_x + tw/2:.1f}" y="{tag_y:.1f}" fill="{tc}" font-size="9.5" '
            f'text-anchor="middle" opacity="0.9">{esc(tag)}</text>'
        )
        tag_x += tw + 5

    # Language dot + name (bottom right)
    meta_x  = cx + CARD_W - 14
    meta_y  = cy + CARD_H - 12
    # Stars
    inner.append(star_icon(meta_x - 48, meta_y - 3, YELLOW))
    inner.append(
        f'<text x="{meta_x - 38}" y="{meta_y:.1f}" font-size="10.5" fill="{MUTED}">{stars}</text>'
    )
    # Lang dot
    inner.append(
        f'<circle cx="{meta_x - 8}" cy="{meta_y - 3}" r="4" fill="{lc}"/>'
    )
    inner.append(
        f'<text x="{meta_x}" y="{meta_y:.1f}" font-size="10.5" fill="{MUTED}" '
        f'text-anchor="end">{lang}</text>'
    )

    card_svg = "".join(inner)

    if STATIC:
        return card_svg

    # Animate: fade + gentle rise
    return (
        f'<g opacity="0" transform="translate(0,8)">'
        f'{card_svg}'
        f'<animate attributeName="opacity" from="0" to="1" '
        f'begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 8" to="0 0" begin="{delay:.2f}s" dur="0.4s" fill="freeze" '
        f'calcMode="spline" keySplines="0.25 0.8 0.25 1"/>'
        f'</g>'
    )


# ── Assemble SVG ──────────────────────────────────────────────────────────────
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{TOTAL_W}" height="{TOTAL_H}" '
    f'viewBox="0 0 {TOTAL_W} {TOTAL_H}" '
    f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',

    '<defs>'
    f'<linearGradient id="pcbg" x1="0" y1="0" x2="1" y2="1">'
    f'<stop offset="0%" stop-color="{BG2}"/>'
    f'<stop offset="100%" stop-color="{BG}"/>'
    f'</linearGradient>'
    '</defs>',

    # Outer background
    f'<rect width="{TOTAL_W}" height="{TOTAL_H}" rx="10" fill="url(#pcbg)"/>',
    f'<rect x=".5" y=".5" width="{TOTAL_W-1}" height="{TOTAL_H-1}" rx="10" '
    f'fill="none" stroke="{CYAN}" stroke-width="1" stroke-opacity="0.3"/>',

    # Titlebar divider
    f'<line x1="0" y1="{TB_H}" x2="{TOTAL_W}" y2="{TB_H}" '
    f'stroke="{CYAN}" stroke-opacity="0.2" stroke-width="1"/>',
]

# Traffic lights
for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{H_PAD + i*16}" cy="{TB_H/2}" r="4.5" fill="{c}"/>')

# Titlebar label
parts.append(
    f'<text x="{TOTAL_W/2}" y="{TB_H/2 + 4}" fill="{MUTED}" font-size="11" text-anchor="middle">'
    f'Varaaa-arch@github: ~$ ls ./projects/</text>'
)

# Prompt prefix (left accent)
parts.append(
    f'<text x="{TOTAL_W - H_PAD}" y="{TB_H/2 + 4}" fill="{MUTED}" font-size="10" '
    f'text-anchor="end">{len(PROJECTS)} repos</text>'
)

# HUD corner brackets
B = 12
for (px, py, dx, dy) in [(1,1,B,B),(TOTAL_W-1,1,-B,B),(1,TOTAL_H-1,B,-B),(TOTAL_W-1,TOTAL_H-1,-B,-B)]:
    parts.append(
        f'<polyline points="{px+dx},{py} {px},{py} {px},{py+dy}" '
        f'fill="none" stroke="{CYAN}" stroke-width="1.5" stroke-opacity="0.45"/>'
    )

# Cards grid
for i, proj in enumerate(PROJECTS):
    row = i // COLS
    col = i % COLS
    cx  = H_PAD + col * (CARD_W + GAP)
    cy  = TB_H + V_PAD + row * (CARD_H + GAP)
    parts.append(render_card(proj, cx, cy, i))

parts.append("</svg>")
svg = "".join(parts)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg):,} bytes), {TOTAL_W}x{TOTAL_H}")
