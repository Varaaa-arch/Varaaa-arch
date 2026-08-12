#!/usr/bin/env python3
"""
ZENITH.SYS — Neon Contribution Heatmap SVG
Generates a cyberpunk-themed GitHub contribution graph with:
  - Neon cyan/green color palette with glowing cells
  - Diagonal cascade reveal animation (left-to-right + top-to-bottom)
  - Stats footer with streak data
  - HUD-style frame and corner brackets

Run by .github/workflows/update-profile.yml after fetch_contributions.py
"""
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "assets", "contrib-heatmap.svg")

# Neon cyberpunk palette: empty -> low -> max activity
PALETTE = [
    "#0a1520",  # 0: empty (dark navy)
    "#003d2e",  # 1: low (dark green)
    "#00704a",  # 2: medium-low
    "#00b86e",  # 3: medium  
    "#00ff9d",  # 4: high (neon green)
    "#a0ffd6",  # 5: max (bright near-white green)
]

GLOW_COLORS = [
    None,
    "#003d2e",
    "#00704a40",
    "#00b86e60",
    "#00ff9d80",
    "#00ff9daa",
]

CELL = 12
GAP  = 3
STEP = CELL + GAP
PAD  = 22
LEFT_LABEL_W = 30
TOP_LABEL_H  = 22
TITLEBAR_H   = 30

BG      = "#050a0f"
BG2     = "#07111a"
FRAME   = "#00fff540"
CYAN    = "#00fff5"
GREEN   = "#00ff9d"
MAGENTA = "#ff00c8"
YELLOW  = "#f5e642"
MUTED   = "#2a5050"
SOFT    = "#6ab8a8"
WHITE   = "#e0ffff"

# Reveal timing — diagonal cascade (column + row weight)
COL_W  = 0.016
ROW_W  = 0.042
CELL_DUR = 0.38


def level_for(count):
    if count == 0: return 0
    if count <= 3: return 1
    if count <= 8: return 2
    if count <= 18: return 3
    if count <= 35: return 4
    return 5


def build_grid(days):
    if not days:
        return []
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # sunday=0
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data):
    days = data["days"]
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    # Month labels
    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = PAD + LEFT_LABEL_W + art_w + PAD
    stats_h = 96
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
@keyframes cellin {{
  0%   {{ opacity: 0; transform: scale(0.3) translateY(-4px); }}
  60%  {{ opacity: 1; transform: scale(1.1) translateY(0); }}
  100% {{ opacity: 1; transform: scale(1) translateY(0); }}
}}
.c {{
  opacity: 0;
  transform-box: fill-box;
  transform-origin: center;
  animation: cellin {CELL_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both;
}}
@keyframes pulseglow {{
  0%,100% {{ filter: brightness(1); }}
  50% {{ filter: brightness(1.4); }}
}}
.c5 {{ animation: cellin {CELL_DUR:.2f}s cubic-bezier(.2,.8,.2,1) both,
       pulseglow 2.5s ease-in-out infinite 1s; }}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>'
        f'<linearGradient id="hmbg" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="{BG2}"/>'
        f'<stop offset="100%" stop-color="{BG}"/>'
        f'</linearGradient>'
        f'<filter id="cellglow4">'
        f'<feGaussianBlur stdDeviation="1.5" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f'</filter>'
        f'<filter id="cellglow5">'
        f'<feGaussianBlur stdDeviation="2.5" result="b"/>'
        f'<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        f'</filter>'
        f'</defs>',
        
        # Background
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="10" fill="url(#hmbg)"/>',
        # Cyan border
        f'<rect x="0.5" y="0.5" width="{canvas_w-1}" height="{canvas_h-1}" rx="10" '
        f'fill="none" stroke="{CYAN}" stroke-width="1" stroke-opacity="0.35"/>',
        # Titlebar separator
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" '
        f'stroke="{CYAN}" stroke-opacity="0.3" stroke-width="1"/>',
    ]

    # Traffic lights
    for i, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{col}"/>')
    
    # Titlebar text
    parts.append(
        f'<text x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="11.5" '
        f'text-anchor="middle">Varaaa-arch@github: ~/contributions --neon-graph</text>'
    )
    
    # HUD brackets
    bs, bw = 12, 1.5
    for (x1,y1,x2,y2,x3,y3) in [
        (bs,1, 1,1, 1,bs),
        (canvas_w-bs,1, canvas_w-1,1, canvas_w-1,bs),
        (bs,canvas_h-1, 1,canvas_h-1, 1,canvas_h-bs),
        (canvas_w-bs,canvas_h-1, canvas_w-1,canvas_h-1, canvas_w-1,canvas_h-bs),
    ]:
        parts.append(
            f'<polyline points="{x1},{y1} {x2},{y2} {x3},{y3}" '
            f'fill="none" stroke="{CYAN}" stroke-width="{bw}" stroke-opacity="0.6"/>'
        )

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    # Month labels
    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(
            f'<text x="{x}" y="{TITLEBAR_H + 15}" fill="{MUTED}" font-size="10">{label}</text>'
        )

    # Day labels
    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(
            f'<text x="{PAD}" y="{y:.1f}" fill="{MUTED}" font-size="9">{wname}</text>'
        )

    # Cells
    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_W + ri * ROW_W
            plural = "s" if count != 1 else ""
            
            # Extra filter for high-activity cells
            extra = ""
            cell_class = "c5" if lvl == 5 else "c"
            if lvl >= 4:
                extra = f' filter="url(#cellglow{lvl})"'
            elif lvl == 3:
                extra = f' filter="url(#cellglow4)"'
            
            parts.append(
                f'<rect class="{cell_class}" x="{gx}" y="{gy}" '
                f'width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{PALETTE[lvl]}"{extra} '
                f'style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title>'
                f'</rect>'
            )

    # Legend
    leg_y = grid_top + art_h + 8
    leg_x = canvas_w - PAD - (len(PALETTE) * (CELL) + 55)
    parts.append(
        f'<text x="{leg_x - 4}" y="{leg_y + CELL*0.82:.1f}" fill="{MUTED}" '
        f'font-size="10" text-anchor="end">Less</text>'
    )
    lx = leg_x
    for lvl, color in enumerate(PALETTE):
        parts.append(
            f'<rect x="{lx}" y="{leg_y}" width="{CELL-1}" height="{CELL-1}" '
            f'rx="2.5" fill="{color}"/>'
        )
        lx += CELL
    parts.append(
        f'<text x="{lx + 4}" y="{leg_y + CELL*0.82:.1f}" fill="{MUTED}" font-size="10">More</text>'
    )

    # Stats separator
    sep_y = leg_y + CELL + 16
    parts.append(
        f'<line x1="0" y1="{sep_y}" x2="{canvas_w}" y2="{sep_y}" '
        f'stroke="{CYAN}" stroke-opacity="0.15" stroke-width="1"/>'
    )

    # Stats
    cs  = data["current_streak"]["length"]
    ls  = data["longest_streak"]["length"]
    tot = data["total_contributions"]
    best = data["best_day"]
    rng  = data["range"]
    gen  = data.get("generated_at", "")[:10]

    sy = sep_y + 22
    parts.append(
        f'<text x="{PAD}" y="{sy}" font-size="12.5">'
        f'<tspan fill="{GREEN}" font-weight="700">{tot:,}</tspan>'
        f'<tspan fill="{SOFT}"> contributions in the last year</tspan>'
        f'</text>'
        f'<text x="{canvas_w - PAD}" y="{sy}" font-size="11" fill="{MUTED}" text-anchor="end">'
        f'{rng["start"]} → {rng["end"]}'
        f'</text>'
    )
    sy += 22
    parts.append(
        f'<text x="{PAD}" y="{sy}" font-size="12">'
        f'<tspan fill="{SOFT}">streak </tspan>'
        f'<tspan fill="{CYAN}" font-weight="700">{cs}d</tspan>'
        f'<tspan fill="{MUTED}"> current  ·  </tspan>'
        f'<tspan fill="{CYAN}" font-weight="700">{ls}d</tspan>'
        f'<tspan fill="{MUTED}"> longest</tspan>'
        f'</text>'
        f'<text x="{canvas_w - PAD}" y="{sy}" font-size="11" fill="{MUTED}" text-anchor="end">'
        f'peak <tspan fill="{YELLOW}" font-weight="700">{best["count"]}</tspan> on {best["date"]}'
        f'</text>'
    )
    sy += 20
    parts.append(
        f'<text x="{PAD}" y="{sy}" font-size="10" fill="{MUTED}">auto-refreshed daily · last sync {gen}</text>'
    )

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    if not os.path.exists(IN_PATH):
        print(f"ERROR: {IN_PATH} not found. Run fetch_contributions.py first.", file=sys.stderr)
        import sys; sys.exit(1)
    
    data = json.load(open(IN_PATH))
    svg = render(data)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH} ({len(svg):,} bytes)")
