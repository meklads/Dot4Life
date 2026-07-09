#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove em-dash from tool metadata/hero/explanatory text only — keep calculator placeholders."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FILES = [
    "tools/bmi-calculator.html",
    "tools/calorie-calculator.html",
    "tools/currency-converter.html",
    "tools/water-calculator.html",
    "tools/body-fat-calculator.html",
    "tools/packing-checklist.html",
    "tools/prayer-times.html",
    "tools/zakat-calculator.html",
    "tools/ramadan-calorie-calculator.html",
    "tools/salary-calculator.html",
    "tools/inheritance-calculator.html",
    "tools/travel-budget.html",
]


def title_dash(text: str) -> str:
    return re.sub(r"\s*—\s*", " - ", text)


def prose_dash(text: str) -> str:
    return re.sub(r"\s*—\s*", ", ", text)


def patch_meta_attrs(html: str) -> str:
    specs = [
        (r'<meta name="description" content="', prose_dash),
        (r'<meta property="og:title" content="', title_dash),
        (r'<meta property="og:description" content="', prose_dash),
        (r'<meta name="twitter:title" content="', title_dash),
        (r'<meta name="twitter:description" content="', prose_dash),
    ]
    for prefix, fixer in specs:
        pattern = re.escape(prefix) + r'([^"]*)(")'

        def repl(m: re.Match[str], fixer=fixer, prefix=prefix) -> str:
            return prefix + fixer(m.group(1)) + m.group(2)

        html = re.sub(pattern, repl, html)
    return html


def patch_ar_spans(html: str) -> str:
    pattern = r'(<span class="ar">)([^<]*—[^<]*)(</span>)'

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + prose_dash(m.group(2)) + m.group(3)

    return re.sub(pattern, repl, html)


def patch_title_tag(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return "<title>" + title_dash(m.group(1)) + "</title>"

    return re.sub(r"<title>([^<]*)</title>", repl, html, count=1)


def patch_tool_hero_desc(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return prose_dash(m.group(0))

    return re.sub(r'<p class="tool-hero-desc">.*?</p>', repl, html, count=1, flags=re.S)


def patch_instruction_p(html: str) -> str:
    pattern = r'(<p>\s*<span class="(?:en|ar)">)([^<]*—[^<]*)(</span>)'

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + prose_dash(m.group(2)) + m.group(3)

    return re.sub(pattern, repl, html)


def patch_packing_intro(html: str) -> str:
    pattern = r'(<p class="(?:en|ar)">)([^<]*—[^<]*)(</p>)'

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + prose_dash(m.group(2)) + m.group(3)

    return re.sub(pattern, repl, html)


def patch_travel_tip(html: str) -> str:
    pattern = r'(<p class="en"><strong>[^<]*</strong>)([^<]*—[^<]*)(</p>)'

    def repl(m: re.Match[str]) -> str:
        return m.group(1) + prose_dash(m.group(2)) + m.group(3)

    return re.sub(pattern, repl, html, count=1)


def patch_currency_options(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return m.group(1) + m.group(2).replace(" — ", " · ") + m.group(3)

    return re.sub(r'(<option[^>]*>)([^<]*)(</option>)', repl, html)


def patch_zakat_explanatory(html: str) -> str:
    """In-tool helper copy (not FAQ blocks)."""
    patterns = [
        r'(<span class="en">)(Hawl — complete lunar year)(</span>)',
        r'(<span class="ar">)([^<]*—[^<]*)(</span>)',
        r'(<span class="en">)(Choose your nisab[^<]*)(</span>)',
        r'(<div class="zc-h-st ar">)([^<]*)(</div>)',
        r'(<div class="zc-h-st en">)([^<]*)(</div>)',
    ]
    for pat in patterns:
        def repl(m: re.Match[str]) -> str:
            return m.group(1) + prose_dash(m.group(2)) + m.group(3)
        html = re.sub(pat, repl, html)
    return html


def patch_currency_body_tips(html: str) -> str:
    pattern = r'(<p class="(?:en|ar)">)([^<]*—[^<]*)(</p>)'
    def repl(m: re.Match[str]) -> str:
        return m.group(1) + prose_dash(m.group(2)) + m.group(3)
    return re.sub(pattern, repl, html)


def fix_file(rel: str) -> tuple[int, int]:
    path = ROOT / rel
    before = path.read_text(encoding="utf-8").count("—")
    html = before_html = path.read_text(encoding="utf-8")

    html = patch_title_tag(html)
    html = patch_meta_attrs(html)
    html = patch_tool_hero_desc(html)
    html = patch_instruction_p(html)
    html = patch_ar_spans(html)

    if "packing-checklist" in rel:
        html = patch_packing_intro(html)
    if "travel-budget" in rel:
        html = patch_travel_tip(html)
    if "currency-converter" in rel:
        html = patch_currency_options(html)
        html = patch_currency_body_tips(html)
    if "zakat-calculator" in rel:
        html = patch_zakat_explanatory(html)

    after = html.count("—")
    if html != before_html:
        path.write_text(html, encoding="utf-8")
    return before, after


def main() -> None:
    for rel in FILES:
        before, after = fix_file(rel)
        print(f"{rel}: {before} -> {after} em-dash")


if __name__ == "__main__":
    main()
