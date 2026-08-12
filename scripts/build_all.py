#!/usr/bin/env python3
"""
ZENITH.SYS — Build All SVG Assets
Runs all SVG generation scripts in order.

Usage:
    python scripts/build_all.py

Optional flags:
    --static    Emit frozen (non-animated) versions for static preview
    --no-fetch  Skip fetching contribution data (use existing data/contributions.json)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

STATIC = "--static" in sys.argv
NO_FETCH = "--no-fetch" in sys.argv

env = os.environ.copy()
if STATIC:
    env["STATIC"] = "1"
    print("ℹ  Building in STATIC mode (no animations)\n")

scripts = [
    ("Header (boot sequence + matrix rain)", "scripts/make_header.py"),
    ("Avatar (ASCII block art)",             "scripts/make_avatar.py"),
    ("Info card (neofetch-style)",           "scripts/make_info_card.py"),
    ("Projects card (featured repos)",       "scripts/make_projects_card.py"),
    ("Footer (animated wave)",               "scripts/make_footer.py"),
]

if not NO_FETCH:
    scripts.insert(0, ("Fetch contribution data", "scripts/fetch_contributions.py"))
    scripts.append(("Contribution heatmap SVG", "scripts/render_heatmap.py"))
else:
    # Only render heatmap from existing data
    scripts.append(("Contribution heatmap SVG", "scripts/render_heatmap.py"))

print("=" * 50)
print("  ZENITH.SYS — Building all SVG assets")
print("=" * 50 + "\n")

errors = []
for label, script in scripts:
    script_path = os.path.join(ROOT, script)
    if not os.path.exists(script_path):
        print(f"  ⚠  SKIP {label} — script not found: {script}")
        continue
    
    print(f"  ⚙  {label}...")
    result = subprocess.run(
        [sys.executable, script_path],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        out = result.stdout.strip()
        if out:
            print(f"     {out}")
        print(f"  ✓  Done\n")
    else:
        print(f"  ✗  ERROR:\n{result.stderr}\n")
        errors.append(label)

print("=" * 50)
if errors:
    print(f"  ❌ {len(errors)} script(s) failed: {', '.join(errors)}")
    print("     Check the error messages above.")
    sys.exit(1)
else:
    print("  ✅ All assets built successfully!")
    print()
    print("  Assets written to: assets/")
    print("    • header.svg          — boot sequence + glitch title")
    print("    • avatar.svg          — ASCII block art avatar")
    print("    • info-card.svg       — cyberpunk neofetch panel")
    print("    • projects-card.svg   — featured projects grid")
    print("    • contrib-heatmap.svg — neon contribution graph")
    print("    • footer.svg          — animated wave footer")
    print()
    print("  Commit and push to see them live on your GitHub profile!")
print("=" * 50)
