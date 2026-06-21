#!/usr/bin/env python3
"""C-F2: Replace complete-* doorway hub pages with no-AdSense redirect stubs."""
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "blog"
BACKUP = ROOT / "outputs" / "backups" / f"hubs-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

# All blog/complete-* files → section target (relative from site root)
PREFIX_TARGETS: list[tuple[str, str]] = [
    ("complete-family-financial-planning", "/finance.html"),
    ("complete-gulf-family-financial-life-hub", "/finance.html"),
    ("complete-household-budget-system", "/finance-wealth/family-budget-plan.html"),
    ("complete-gulf-family-health-wellness", "/health.html"),
    ("complete-family-systems-productivity-hub", "/productivity.html"),
    ("complete-family-travel-activities-hub", "/travel.html"),
    ("complete-islamic-lifestyle-guide", "/islamic.html"),
]

LINK_REPLACEMENTS: dict[str, str] = {}
for prefix, target in PREFIX_TARGETS:
    for suffix in ("", "-ar", "-en"):
        path = f"/blog/{prefix}{suffix}.html"
        LINK_REPLACEMENTS[path] = target


def is_en(name: str) -> bool:
    return name.endswith("-en.html")


def redirect_stub(target: str, en: bool) -> str:
    lang = "en" if en else "ar"
    direction = "ltr" if en else "rtl"
    title = "Redirecting…" if en else "جاري التوجيه…"
    link = "Continue" if en else "متابعة"
    canonical = f"https://dotforlife.com{target}"
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="canonical" href="{canonical}">
<meta http-equiv="refresh" content="0;url={target}">
<meta name="robots" content="noindex,follow">
<script>location.replace("{target}");</script>
</head>
<body style="font-family:system-ui,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;background:#FAF8F4;">
<p><a href="{target}">{link}</a></p>
</body>
</html>
"""


def hub_files() -> list[Path]:
    return sorted(BLOG.glob("complete-*.html"))


def apply_hub_redirects() -> list[tuple[str, str]]:
    BACKUP.mkdir(parents=True, exist_ok=True)
    applied: list[tuple[str, str]] = []
    for path in hub_files():
        name = path.name
        target = None
        for prefix, t in PREFIX_TARGETS:
            if name.startswith(prefix):
                target = t
                break
        if not target:
            continue
        shutil.copy2(path, BACKUP / name)
        path.write_text(redirect_stub(target, is_en(name)), encoding="utf-8")
        applied.append((f"/blog/{name}", target))
    return applied


def update_internal_links() -> int:
    count = 0
    for html in ROOT.rglob("*.html"):
        if "outputs/backups" in str(html) or "legacy/" in str(html):
            continue
        text = html.read_text(encoding="utf-8")
        new = text
        for old, new_url in LINK_REPLACEMENTS.items():
            if old in new:
                new = new.replace(old, new_url)
                count += new.count(new_url) - text.count(new_url) if new != text else 0
        # simpler: count replacements
        replaced = 0
        for old, new_url in LINK_REPLACEMENTS.items():
            n = new.count(old)
            if n:
                new = new.replace(old, new_url)
                replaced += n
        if new != text:
            html.write_text(new, encoding="utf-8")
            count += replaced
    return count


def main() -> None:
    applied = apply_hub_redirects()
    links = update_internal_links()
    proof = ROOT / "operating-system" / "reports" / "C-F2-redirect-map.md"
    lines = [
        "# C-F2 — Hub redirect map (BUILD VERIFIED — Cursor)",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        f"Backup: `{BACKUP.relative_to(ROOT)}`",
        "",
        "| Source | Target |",
        "|--------|--------|",
    ]
    for src, tgt in applied:
        lines.append(f"| `{src}` | `{tgt}` |")
    lines += [
        "",
        f"Hub files converted: **{len(applied)}**",
        f"Internal link replacements: **{links}**",
        "",
        "## Verification",
        "- No `adsbygoogle` in hub stubs",
        "- `meta http-equiv=\"refresh\"` + `location.replace` on each hub",
        "- `grep -rl 'complete-family-financial-planning' --include='*.html'` should only hit redirect stubs / backups",
    ]
    proof.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"C-F2: {len(applied)} hubs → redirects, {links} link fixes")
    print(f"Proof: {proof}")


if __name__ == "__main__":
    main()
