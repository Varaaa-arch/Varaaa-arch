#!/usr/bin/env python3
"""
ZENITH.SYS — Quick Setup & Customization Script
Run this FIRST to customize the profile with your own details.
Then run `python scripts/build_all.py` to regenerate all SVGs.

Usage:
    python setup.py

Or set environment variables before running:
    ZENITH_USERNAME=myusername python setup.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def ask(prompt, default=""):
    val = input(f"{prompt} [{default}]: ").strip()
    return val if val else default

def replace_in_file(path, replacements):
    with open(path, "r") as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)
    print(f"  ✓ updated {os.path.relpath(path, HERE)}")

print("\n" + "="*60)
print("  ZENITH.SYS — Profile Setup")
print("="*60 + "\n")

print("Fill in your details (press Enter to keep default):\n")

username    = ask("GitHub username",   "YOUR_USERNAME")
fullname    = ask("Your full name",    "Zenith")
status      = ask("Status/role",       "Student · Software Engineer")
focus       = ask("Focus areas",       "Full-Stack · Security · DevOps")
location    = ask("Location",          "Jakarta, Indonesia")
linkedin    = ask("LinkedIn username", "YOUR_LINKEDIN")
instagram   = ask("Instagram handle", "YOUR_INSTAGRAM")
email       = ask("Email address",     "your@email.com")
portfolio   = ask("Portfolio URL",     "https://yourportfolio.dev")
discord_id  = ask("Discord user ID",   "YOUR_DISCORD_ID")

# Languages / stack
print("\nCustomize your tech stack (comma-separated, or Enter to keep defaults):")
languages   = ask("Languages", "TypeScript, Python, Go, Rust")
frontend    = ask("Frontend",  "Next.js, React, Tailwind CSS")
backend     = ask("Backend",   "FastAPI, Node.js, gRPC, REST")
database    = ask("Database",  "PostgreSQL, Redis, MongoDB")
devops      = ask("DevOps",    "Docker, K8s, GitHub Actions")
security    = ask("Security",  "Burp Suite, Nmap, PenTest")

print("\nApplying your customizations...\n")

# ─── Update info-card.py ───────────────────────────────────────────────────
info_card = os.path.join(HERE, "scripts", "make_info_card.py")
replace_in_file(info_card, [
    ('"user": "zenith"',         f'"user": "{username}"'),
    ('"Student · Software Engineer"', f'"{status}"'),
    ('"Full-Stack · Security · DevOps"', f'"{focus}"'),
    ('"Jakarta, Indonesia"',     f'"{location}"'),
    ('"TypeScript, Python, Go, Rust"', f'"{languages}"'),
    ('"Next.js, React, Tailwind CSS"', f'"{frontend}"'),
    ('"FastAPI, Node.js, gRPC, REST"', f'"{backend}"'),
    ('"PostgreSQL, Redis, MongoDB"',   f'"{database}"'),
    ('"Docker, K8s, GitHub Actions"',  f'"{devops}"'),
    ('"Burp Suite, Nmap, PenTest"',    f'"{security}"'),
])

# ─── Update avatar.py ─────────────────────────────────────────────────────
avatar = os.path.join(HERE, "scripts", "make_avatar.py")
replace_in_file(avatar, [
    ('"USER:    zenith"',   f'"USER:    {username}"'),
    ('"STATUS:  ● ONLINE — building the future"',
     f'"STATUS:  ● ONLINE — building the future"'),  # keep or customize
])

# ─── Update fetch_contributions.py ────────────────────────────────────────
fetch = os.path.join(HERE, "scripts", "fetch_contributions.py")
replace_in_file(fetch, [
    ('"YOUR_USERNAME"', f'"{username}"'),
])

# ─── Update README.md ─────────────────────────────────────────────────────
readme = os.path.join(HERE, "README.md")
replace_in_file(readme, [
    ("YOUR_USERNAME",  username),
    ("YOUR_LINKEDIN",  linkedin),
    ("YOUR_INSTAGRAM", instagram),
    ("YOUR_EMAIL",     email),
    ("YOUR_PORTFOLIO_URL", portfolio),
    ("YOUR_DISCORD_ID", discord_id),
])

# ─── Update header ────────────────────────────────────────────────────────
# Header uses static text, so just update the "ZENITH" references if needed
# (header is mostly static/structural so we don't auto-replace there)

print("\n" + "="*60)
print("  ✅ Setup complete!")
print("="*60)
print()
print("Next steps:")
print("  1. Run: python scripts/build_all.py")
print("     → regenerates all SVG assets with your new settings")
print()
print("  2. Fetch your real contribution data:")
print("     pip install requests beautifulsoup4")
print(f"     GH_PROFILE_USER={username} python scripts/fetch_contributions.py")
print("     python scripts/render_heatmap.py")
print()
print("  3. Push to GitHub:")
print("     git init && git add . && git commit -m 'feat: initialize ZENITH.SYS profile'")
print(f"     git remote add origin https://github.com/{username}/{username}")
print("     git push -u origin main")
print()
print("  4. The GitHub Action will auto-refresh the contribution graph daily.")
print()
print("  Enjoy your cyberpunk profile! 🤖⚡")
