#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Insert Recipes nav item after Islamic in nav-links and md-links site-wide."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    "outputs",
    "legacy",
    ".git",
    "node_modules",
    "__pycache__",
}

RECIPES_LI = (
    '<li><a href="/library/recipes/"><span class="en">Recipes</span>'
    '<span class="ar">الوصفات</span></a></li>'
)

RECIPES_A = (
    '<a href="/library/recipes/"><span class="en">Recipes</span>'
    '<span class="ar">الوصفات</span></a>'
)

ISLAMIC_LI = re.compile(
    r'<li><a href="[^"]*islamic\.html"[^>]*>.*?</a></li>',
    re.I | re.S,
)

ISLAMIC_A = re.compile(
    r'<a href="[^"]*islamic\.html"[^>]*>.*?</a>',
    re.I | re.S,
)


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def inject_after_islamic_li(nav: str) -> str:
    if "/library/recipes/" in nav:
        return nav
    return ISLAMIC_LI.sub(rf"\g<0>{RECIPES_LI}", nav, count=1)


def inject_after_islamic_a(md: str) -> str:
    if "/library/recipes/" in md:
        return md
    return ISLAMIC_A.sub(rf"\g<0>\n    {RECIPES_A}", md, count=1)


def patch_nav_links(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return "<ul class=\"nav-links\">" + inject_after_islamic_li(m.group(1)) + m.group(2)

    # Closed nav-links or broken pages where </ul> is missing
    pattern = re.compile(
        r'<ul class="nav-links">(.*?)(</ul>|(?=</nav>)|(?=<h1)|(?=<div class="article))',
        re.I | re.S,
    )
    return pattern.sub(repl, text)


def patch_md_links(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return '<div class="md-links">' + inject_after_islamic_a(m.group(1)) + "</div>"

    pattern = re.compile(r'<div class="md-links">(.*?)</div>', re.I | re.S)
    return pattern.sub(repl, text)


def patch_html(text: str) -> str:
    text = patch_nav_links(text)
    text = patch_md_links(text)
    return text


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*.html"):
        if should_skip(path):
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        if "nav-links" not in raw or "islamic.html" not in raw.lower():
            continue
        new = patch_html(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT))
    print(f"Done: {changed} files updated")


if __name__ == "__main__":
    main()
