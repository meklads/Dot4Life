#!/usr/bin/env python3
"""Amer batch د: merge duplicate FAQPage, remove Latin paragraphs, fix zakat JSON-LD."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DUPLICATE_FAQ = [
    "blog/family-travel-planning-without-overspending-en.html",
    "blog/starting-side-business-saudi-uae-en.html",
    "blog/stress-management-working-parents-en.html",
]

LATIN_PARA = [
    "islamic-hajj-umrah/daily-adhkar-family-guide.html",
    "islamic-hajj-umrah/teaching-children-allah-names.html",
    "islamic-hajj-umrah/hijri-new-year-children.html",
    "blog/daily-walking-benefits.html",
]

LATIN_OLD = (
    '<p><span class="en">Get more family tips every Friday - join our newsletter.</span>'
    '<span class="ar">احصل على نصائح أسرية كل جمعة - اشترك في نشرتنا.</span></p>'
)
LATIN_NEW = "<p><span class=\"ar\">احصل على نصائح أسرية كل جمعة - اشترك في نشرتنا.</span></p>"

ZAKAT = "blog/zakat-guide-2025-en.html"
FIN_LIT = "blog/teaching-children-financial-literacy-en.html"


def robots_unchanged(before: str, after: str, rel: str) -> None:
    rb = re.search(r'<meta name="robots" content="([^"]+)"', before)
    ra = re.search(r'<meta name="robots" content="([^"]+)"', after)
    if (rb.group(1) if rb else None) != (ra.group(1) if ra else None):
        raise SystemExit(f"robots changed in {rel}")


def validate_ld_json(html: str, rel: str) -> None:
    for i, m in enumerate(
        re.finditer(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            html,
            re.S | re.I,
        )
    ):
        raw = m.group(1).strip()
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            raise SystemExit(f"{rel}: JSON-LD block {i + 1} invalid: {e}") from e


def count_faqpage(html: str) -> int:
    n = 0
    for m in re.finditer(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.S | re.I,
    ):
        try:
            data = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            if data.get("@type") == "FAQPage":
                n += 1
            for g in data.get("@graph", []) if isinstance(data.get("@graph"), list) else []:
                if isinstance(g, dict) and g.get("@type") == "FAQPage":
                    n += 1
    return n


def merge_duplicate_faq(rel: str) -> bool:
    path = ROOT / rel
    before = path.read_text(encoding="utf-8")
    scripts = list(
        re.finditer(
            r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
            before,
            re.S | re.I,
        )
    )
    faq_idxs = []
    for idx, m in enumerate(scripts):
        try:
            data = json.loads(m.group(2).strip())
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and data.get("@type") == "FAQPage":
            faq_idxs.append(idx)
    if len(faq_idxs) < 2:
        print(f"{rel}: no duplicate FAQPage ({len(faq_idxs)} blocks)")
        return False
    # Drop later duplicates; keep first FAQPage block.
    drop = set(faq_idxs[1:])
    parts = []
    last = 0
    for idx, m in enumerate(scripts):
        if idx in drop:
            last = m.end()
            continue
        parts.append(before[last : m.start()])
        parts.append(m.group(0))
        last = m.end()
    parts.append(before[last:])
    html = "".join(parts)
    validate_ld_json(html, rel)
    robots_unchanged(before, html, rel)
    if count_faqpage(html) != 1:
        raise SystemExit(f"{rel}: expected 1 FAQPage after merge, got {count_faqpage(html)}")
    path.write_text(html, encoding="utf-8")
    print(f"{rel}: removed {len(drop)} duplicate FAQPage script(s)")
    return True


def fix_financial_literacy() -> bool:
    rel = FIN_LIT
    path = ROOT / rel
    before = path.read_text(encoding="utf-8")
    # Remove standalone duplicate FAQPage; keep @graph Article+FAQPage.
    scripts = list(
        re.finditer(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>\n?',
            before,
            re.S | re.I,
        )
    )
    faq_standalone = []
    for m in scripts:
        inner = re.search(r">(.*)</script>", m.group(0), re.S)
        if not inner:
            continue
        try:
            data = json.loads(inner.group(1).strip())
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and data.get("@type") == "FAQPage":
            faq_standalone.append(m)
    if len(faq_standalone) != 1:
        print(f"{rel}: expected 1 standalone FAQPage to remove, found {len(faq_standalone)}")
        return False
    html = before[: faq_standalone[0].start()] + before[faq_standalone[0].end() :]
    validate_ld_json(html, rel)
    robots_unchanged(before, html, rel)
    if count_faqpage(html) != 1:
        raise SystemExit(f"{rel}: expected 1 FAQPage in @graph, got {count_faqpage(html)}")
    path.write_text(html, encoding="utf-8")
    print(f"{rel}: removed duplicate standalone FAQPage (kept @graph)")
    return True


def remove_latin(rel: str) -> bool:
    path = ROOT / rel
    before = path.read_text(encoding="utf-8")
    if LATIN_OLD not in before:
        print(f"{rel}: latin paragraph pattern not found")
        return False
    html = before.replace(LATIN_OLD, LATIN_NEW)
    robots_unchanged(before, html, rel)
    path.write_text(html, encoding="utf-8")
    print(f"{rel}: removed English span from newsletter paragraph")
    return True


def fix_zakat() -> bool:
    rel = ZAKAT
    path = ROOT / rel
    before = path.read_text(encoding="utf-8")
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "How to Calculate Zakat on Money and Gold 2025",
        "description": "Complete guide to calculating Zakat on savings, gold, silver, and investments in 2025",
        "url": "https://dotforlife.com/blog/zakat-guide-2025-en.html",
        "datePublished": "2025-06-01",
        "inLanguage": "en",
        "publisher": {
            "@type": "Organization",
            "name": "DOTFORLIFE",
            "url": "https://dotforlife.com",
        },
        "author": {
            "@type": "Organization",
            "name": "DOTFORLIFE Editorial Team",
            "url": "https://dotforlife.com",
        },
        "image": ["/assets/images/approved/hero-family-budget-plan.webp"],
        "dateModified": "2025-06-01",
        "isAccessibleForFree": True,
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What is the Nisab threshold for Zakat in 2025?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "The Nisab is equivalent to 85 grams of gold. At approximately $60 per gram, the Nisab is around $5,100 USD or 19,000 SAR. This changes with gold prices.",
                },
            },
            {
                "@type": "Question",
                "name": "Is Zakat due on monthly salary?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Zakat is not due on salary at the time of receipt. It is due on savings that have reached the Nisab and been held for a full lunar year (Hawl).",
                },
            },
            {
                "@type": "Question",
                "name": "How do I calculate Zakat on gold?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "If you own 85 grams or more of gold for a full lunar year, you pay 2.5% of its current market value as Zakat.",
                },
            },
            {
                "@type": "Question",
                "name": "Is Zakat due on gold jewelry worn regularly?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Scholars differ on this. The majority opinion holds that Zakat is due on gold jewelry if it reaches the Nisab and a full year passes, regardless of whether it is worn.",
                },
            },
            {
                "@type": "Question",
                "name": "What is the difference between Zakat al-Mal and Zakat al-Fitr?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Zakat al-Mal is an annual 2.5% obligation on wealth above the Nisab held for one lunar year. Zakat al-Fitr is a fixed amount per person paid at the end of Ramadan.",
                },
            },
        ],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://dotforlife.com"},
            {"@type": "ListItem", "position": 2, "name": "Islamic", "item": "https://dotforlife.com/islamic.html"},
            {
                "@type": "ListItem",
                "position": 3,
                "name": "How to Calculate Zakat on Money and Gold 2025, Complete Guide",
                "item": "https://dotforlife.com/blog/zakat-guide-2025-en.html",
            },
        ],
    }

    def script_block(obj: dict) -> str:
        return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'

    schema_block = (
        script_block(article)
        + "\n"
        + script_block(faq)
        + "\n"
        + script_block(breadcrumb)
        + "\n"
    )

    # Replace corrupted head chunk from raw JSON through broken breadcrumb/gtag.
    pattern = re.compile(
        r'<link rel="stylesheet" href="/styles/pages/blog_zakat-guide-2025-en\.css[^"]*">\s*'
        r"\{.*?^\}\s*"
        r"(?:<!-- Google tag \(gtag\.js\) -->.*?^\}\s*)?",
        re.S | re.M,
    )
    if not pattern.search(before):
        raise SystemExit(f"{rel}: corrupted head pattern not found")
    html = pattern.sub(
        '<link rel="stylesheet" href="/styles/pages/blog_zakat-guide-2025-en.css?v=821e658">\n' + schema_block,
        before,
        count=1,
    )
    # Remove any leftover raw JSON-LD / broken gtag fragments after wrapped scripts.
    leftover = re.compile(
        r"(?:^|\n)\{\s*\"@context\":\s*\"https://schema\.org\".*?"
        r"(?:<!-- Google tag \(gtag\.js\) -->.*?^\}\s*)?",
        re.S | re.M,
    )
    html = leftover.sub("\n", html, count=1)
    html = re.sub(
        r"<!-- Google tag \(gtag\.js\) -->\s*"
        r"window\.dataLayer.*?G-3G1XPV4F0G'\);\s*\"@context\":\s*\"https://schema\.org\".*?^\}\s*",
        "",
        html,
        count=1,
        flags=re.S | re.M,
    )
    validate_ld_json(html, rel)
    robots_unchanged(before, html, rel)
    path.write_text(html, encoding="utf-8")
    print(f"{rel}: wrapped Article+FAQPage+BreadcrumbList in script tags")
    return True


def main() -> None:
    changed = 0
    for rel in DUPLICATE_FAQ:
        if merge_duplicate_faq(rel):
            changed += 1
    if fix_financial_literacy():
        changed += 1
    for rel in LATIN_PARA:
        if remove_latin(rel):
            changed += 1
    if fix_zakat():
        changed += 1
    print(f"done: {changed} file groups updated")


if __name__ == "__main__":
    main()
