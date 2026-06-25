#!/usr/bin/env python3
"""D16 delivery monitor — prints a DELIVERY/STALL sentinel as Hema deepens pages.

Watches the 25 D16 pages, reports how many now PASS QA
(AR>=1600w / EN>=1500w, FAQ>=4, Article+FAQPage, 0 em-dash, 0 Unsplash).
Emits a line only when the pass-count changes, so the parent agent can react.
"""
from __future__ import annotations

import html
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    "productivity/family-time-management-en.html",
    "productivity/family-time-management.html",
    "fitness/calorie-calculator-saudi.html",
    "fitness/ramadan-calorie-calculator.html",
    "fitness/fitness-for-women-saudi.html",
    "blog/body-fat-vs-weight-guide-ar.html",
    "blog/peaceful-road-trip-kids-guide.html",
    "blog/end-of-service-saudi.html",
    "blog/saving-for-education-gulf.html",
    "real-estate/rent-vs-buy-gulf-family.html",
    "blog/ashura-family-traditions-gulf.html",
    "real-estate/riyadh-rental-yield.html",
    "finance-wealth/investment-basics-beginners.html",
    "blog/pregnancy-nutrition-first-trimester.html",
    "comparisons/government-vs-private-school-gulf.html",
    "real-estate/jeddah-mortgage-calculator.html",
    "blog/hydration-guide.html",
    "blog/pregnancy-and-umrah-guide.html",
    "blog/umrah-with-kids-guide.html",
    "blog/daily-islamic-habits-guide.html",
    "real-estate/oman-property-roi.html",
    "blog/medina-hotels-near-masjid-nabawi.html",
    "blog/family-nutrition-on-budget.html",
    "blog/gcc-family-budget-2025.html",
    "comparisons/saving-vs-investing-gulf-family.html",
]

TAG = re.compile(r"<[^>]+>")
SCRIPT = re.compile(r"<(script|style|nav|footer|header|aside)\b[^>]*>.*?</\1>", re.I | re.S)


def body_words(s: str) -> int:
    txt = re.sub(r"\s+", " ", html.unescape(TAG.sub(" ", SCRIPT.sub(" ", s)))).strip()
    return len(re.findall(r"[\w\u0600-\u06FF]+", txt))


def passes(path: Path) -> bool:
    s = path.read_text(encoding="utf-8", errors="ignore")
    en = path.stem.endswith("-en")
    need = 1500 if en else 1600
    wc = body_words(s)
    q = s.count('"@type":"Question"') + s.count('"@type": "Question"')
    art = '"@type":"Article"' in s or '"@type": "Article"' in s
    faq = '"@type":"FAQPage"' in s or '"@type": "FAQPage"' in s
    em = s.count("\u2014")
    uns = s.count("images.unsplash.com")
    return wc >= need and q >= 4 and art and faq and em == 0 and uns == 0


def count_pass() -> int:
    n = 0
    for rel in PAGES:
        p = ROOT / rel
        if p.exists() and passes(p):
            n += 1
    return n


def main() -> None:
    last = -1
    while True:
        cur = count_pass()
        if cur != last:
            tag = "DELIVERY" if cur > last and last >= 0 else "STATE"
            print(f"D16 {tag}: {cur}/25 pages now PASS QA", flush=True)
            last = cur
        time.sleep(90)


if __name__ == "__main__":
    main()
