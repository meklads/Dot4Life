#!/usr/bin/env python3
"""Amer site-wide batch B: remove AI clichés from EN blog articles."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BOILERPLATE_A = re.compile(
    r"<p>In conclusion, <strong>[^<]+</strong> is an important topic that deserves careful attention[^<]*</p>",
    re.I | re.S,
)
BOILERPLATE_B = re.compile(
    r"<p>In conclusion, <strong>[^<]+</strong> is an important topic for Gulf families who want[^<]*</p>",
    re.I | re.S,
)

BATCH1_CLOSINGS = {
    "blog/family-budget-planning-guide-en.html": (
        "<h2 id=\"family-budget-planning-guide-conclusion\">Closing thought</h2>\n"
        "<p>Track spending for one full month, set a realistic split for your city (often 55/25/20 in Dubai or Doha), "
        "and schedule a 30-minute family money review on the same date each month. Consistent small habits beat a "
        "perfect spreadsheet you abandon after two weeks.</p>"
    ),
    "blog/family-friendly-activities-gulf-cities-en.html": (
        "<p>Choose one outing each weekend from this list, rotate neighborhoods monthly, and let children pick "
        "every third activity. Gulf cities offer strong free and low-cost options when you plan around heat, "
        "prayer times, and school calendars.</p>"
    ),
    "blog/life-insurance-gulf-families-en.html": (
        "<p>Compare term quotes from at least two licensed providers, cover outstanding debts plus several years of "
        "income, and revisit the policy when you buy a home or welcome another child.</p>"
    ),
    "blog/managing-healthcare-costs-families-en.html": (
        "<p>Keep insurance statements in one folder, request itemized hospital bills before paying, and use "
        "preventive benefits your plan already includes to avoid avoidable emergency costs.</p>"
    ),
    "blog/natural-birth-vs-c-section-comparison-en.html": (
        "<p>Build a flexible birth plan with your obstetrician, attend antenatal classes at your hospital, and "
        "stay open to changes if labor conditions shift. The aim is a healthy mother and baby, not a fixed delivery label.</p>"
    ),
    "blog/pregnancy-weeks-guide-en.html": (
        "<p>Use a week-by-week tracker, write questions before each prenatal visit, and share updates with your partner "
        "early so decisions are made calmly, not under delivery-room pressure.</p>"
    ),
}

FAMILY_BUDGET_JSON_LD = """<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Article","headline":"Family Budget Planning Guide","description":"Complete guide to planning and managing family budget.","author":{"@type":"Organization","name":"DOTFORLIFE"},"publisher":{"@type":"Organization","name":"DOTFORLIFE","logo":{"@type":"ImageObject","url":"https://dotforlife.com/assets/images/logo1-footer.webp"}},"datePublished":"2026-06-22","dateModified":"2026-06-22","image":"https://dotforlife.com/assets/images/hero-family-budget-planning-guide-en.webp","mainEntityOfPage":{"@type":"WebPage","@id":"https://dotforlife.com/blog/family-budget-planning-guide-en.html"}},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What is the best budgeting method for families?","acceptedAnswer":{"@type":"Answer","text":"The best starting point is the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings and debt repayment. In Gulf cities where housing is expensive (Dubai, Doha), adjust to 55/25/20 or 60/20/20. Track actual spending for 2 months before setting your own percentages."}},{"@type":"Question","name":"How much should a family save each month?","acceptedAnswer":{"@type":"Answer","text":"Target 10% of income as a starting point if you are not currently saving, then gradually increase to 15-20%. Priority: first build a 3-month emergency fund, then retirement savings, then children's education. Automate transfers on payday so you never see the money."}},{"@type":"Question","name":"How do I budget with a variable income?","acceptedAnswer":{"@type":"Answer","text":"Use the average income of the last 6 months as your budget base, and build fixed expenses around the lowest-earning month. In higher-earning months, save the surplus. This approach works for freelancers and commission-based workers."}},{"@type":"Question","name":"What percentage of income should go to housing?","acceptedAnswer":{"@type":"Answer","text":"Housing should not exceed 30-35% of net monthly income. In expensive Gulf cities like Dubai and Doha, this may reach 40% realistically. For Saudi citizens with REDF support, housing costs stay below 25%. Include utilities, maintenance, and insurance in your housing budget."}},{"@type":"Question","name":"How often should we review the family budget?","acceptedAnswer":{"@type":"Answer","text":"A monthly 30-minute review is sufficient. Review actual vs projected spending, categories that went over, and set goals for next month. Schedule it on the same day each month and involve all family members who spend."}}]}]}</script>"""

FAMILY_BUDGET_FILLER = re.compile(
    r"\n\n<p>To make the most of this guide on <strong>Family Budget Planning Guide</strong>.*?</p>\n"
    r"<p>One effective approach is to start with small.*?</p>\n"
    r"<p>Another important consideration is seeking support.*?</p>",
    re.S,
)

NATURAL_BIRTH_AR_CLOSING = re.compile(
    r"<p>في الختام، natural birth EN هي تجربة ثمينة[^<]*</p>"
)


def fix_family_budget_json(html: str) -> str:
    html = re.sub(
        r'<script type="application/ld\+json">\{.*?\}</script>\s*'
        r'<script type="application/ld\+json">\{.*?"Get Started Today".*?\}</script>',
        FAMILY_BUDGET_JSON_LD,
        html,
        count=1,
        flags=re.S,
    )
    return html


def replace_closing(html: str, rel: str) -> str:
    closing = BATCH1_CLOSINGS.get(rel)
    if not closing:
        return html
    if BOILERPLATE_A.search(html):
        html = BOILERPLATE_A.sub(closing, html, count=1)
    elif BOILERPLATE_B.search(html):
        html = BOILERPLATE_B.sub(closing, html, count=1)
    if rel == "blog/natural-birth-vs-c-section-comparison-en.html":
        html = NATURAL_BIRTH_AR_CLOSING.sub(closing, html, count=1)
    return html


def fix_file(rel: str) -> None:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    if rel == "blog/family-budget-planning-guide-en.html":
        html = fix_family_budget_json(html)
        html = FAMILY_BUDGET_FILLER.sub("\n", html)
    html = replace_closing(html, rel)
    path.write_text(html, encoding="utf-8")
    print(f"fixed {rel}")


def main() -> None:
    batch = sys.argv[1] if len(sys.argv) > 1 else "1"
    files = list(BATCH1_CLOSINGS.keys()) if batch == "1" else []
    if not files:
        raise SystemExit(f"batch {batch} not defined yet")
    for rel in files:
        fix_file(rel)


if __name__ == "__main__":
    main()
