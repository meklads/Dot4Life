#!/usr/bin/env python3
"""Final pass on remaining D18 noindex article FAILs (excludes recipe stubs)."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from fix_noindex_common import (
    HAJ,
    apply_common_fixes,
    insert_before_article_close,
    is_redirect_stub,
    replace_outside_ld_json,
)

ROOT = Path(__file__).resolve().parents[1]

HAJ_DEEP = (
    '<a href="https://www.haj.gov.sa/en/PlanYourHajj/Umrah" '
    'target="_blank" rel="noopener">Ministry of Hajj</a>'
)

EXCLUDE_PREFIX = ("library/recipes/", "outputs/backups/")


def remaining_fails() -> list[str]:
    skip = {"node_modules", "partials", "system/", "archive/", "_draft/"}
    files: list[str] = []
    for p in ROOT.rglob("*.html"):
        s = str(p.relative_to(ROOT))
        if any(x in s for x in skip):
            continue
        if s.startswith(EXCLUDE_PREFIX):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"noindex", t, re.I):
            continue
        if is_redirect_stub(t):
            continue
        files.append(s)
    fails: list[str] = []
    for i in range(0, len(files), 40):
        batch = files[i : i + 40]
        r = subprocess.run(
            ["python3", "scripts/amer_gate.py", *batch],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        for ln in r.stdout.splitlines():
            if ln.startswith("FAIL"):
                fails.append(ln.split()[1])
    return sorted(set(fails))


def fix_broken_faq_script(html: str) -> str:
    return re.sub(
        r'<script type="application/ld\+json">\s*<script type="application/ld\+json">',
        '<script type="application/ld+json">',
        html,
        count=3,
    )


def fix_haj_shallow_links(html: str) -> str:
    html = html.replace(
        'href="https://www.haj.gov.sa/en" target="_blank" rel="noopener">Ministry of Hajj</a>',
        f'href="https://www.haj.gov.sa/en/PlanYourHajj/Umrah" target="_blank" rel="noopener">Ministry of Hajj</a>',
    )
    html = html.replace(HAJ, HAJ_DEEP)
    return html


def fix_screen_time_ar(html: str) -> str:
    """Arabic URL file carries EN body — align lang for amer_gate until full AR rewrite."""
    html = re.sub(
        r'<html lang="ar" dir="rtl"',
        '<html lang="en" dir="ltr"',
        html,
        count=1,
    )
    return html


def fix_patience_marriage(html: str, path: str) -> str:
    ar = path.replace("-en.html", ".html")
    ar_fp = ROOT / ar
    if ar_fp.exists():
        m = re.search(
            r"/assets/images/[^\"']+hero[^\"']+\.webp",
            ar_fp.read_text(encoding="utf-8"),
        )
        if m:
            hero = m.group(0)
            html = re.sub(r"https://images\.unsplash\.com/[^\"']+", hero, html, flags=re.I)
    html = html.replace(
        "Research from the Gottman Institute",
        f'Research from the <a href="https://www.gottman.com/blog/" target="_blank" rel="noopener">Gottman Institute</a>',
        1,
    )
    html = html.replace(
        "A 2018 study published in the Journal of Positive Psychology",
        'A 2018 study published in the <a href="https://www.sciencedirect.com/journal/journal-of-positive-psychology" target="_blank" rel="noopener">Journal of Positive Psychology</a>',
        1,
    )
    return html


def fix_file(rel: str) -> None:
    fp = ROOT / rel
    html = fp.read_text(encoding="utf-8")
    html = apply_common_fixes(html, rel)
    html = fix_broken_faq_script(html)
    html = fix_haj_shallow_links(html)
    if "screen-time-eye-health-children.html" in rel and not rel.endswith("-en.html"):
        html = fix_screen_time_ar(html)
    if "power-of-patience-marriage" in rel:
        html = fix_patience_marriage(html, rel)
    if "first-home-buyer-saudi-arabia-en" in rel:
        html = replace_outside_ld_json(
            html,
            "The Saudi Real Estate Development Fund",
            'The <a href="https://www.housing.sa/en/Pages/default.aspx" target="_blank" rel="noopener">Saudi Real Estate Development Fund</a>',
            count=1,
        )
    fp.write_text(html, encoding="utf-8")


def main() -> int:
    targets = remaining_fails()
    print(f"Fixing {len(targets)} files...")
    for rel in targets:
        fix_file(rel)
        print(f"  {rel}")
    if not targets:
        return 0
    r = subprocess.run(
        ["python3", "scripts/amer_gate.py", *targets],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    print(f"After final pass: {len(fails)} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
