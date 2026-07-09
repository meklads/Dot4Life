#!/usr/bin/env python3
"""Amer batch 5: authority deep links + percent rephrasing (same rule as batch ج)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from fix_noindex_common import inject_deep_link, is_arabic  # noqa: E402

FILES = [
    "blog/family-travel-planning-without-overspending-en.html",
    "blog/teaching-children-financial-literacy-en.html",
    "islamic-hajj-umrah/daily-adhkar-family-guide.html",
    "islamic-hajj-umrah/teaching-children-allah-names.html",
    "peace-capsules/art-of-sincere-apology-marriage-en.html",
]

REPLACEMENTS: list[tuple[str, str]] = [
    # --- family-travel ---
    (
        "<p>Understanding the spending patterns is the first step to fixing them. Here is what the data shows about Gulf family travel habits:</p>",
        '<p>Understanding the spending patterns is the first step to fixing them. '
        '<a href="https://www.sta.gov.sa/en/Pages/default.aspx" target="_blank" rel="noopener">Saudi Tourism Authority data</a> '
        "highlights how Gulf families cluster trips around school holidays and peak fare windows:</p>",
    ),
    (
        "During these periods, flight prices from Gulf airports rise by 40-60%. Hotels in popular destinations like Istanbul, Kuala Lumpur, and London double their rates. Families end up paying peak prices because they have no flexibility. The solution: plan further ahead. Booking 6-8 months in advance for peak-season travel can save 20-35% on flights and 30% on accommodation.",
        'During these periods, <a href="https://www.iata.org/en/publications/economics/" target="_blank" rel="noopener">IATA fare analysis</a> '
        "shows Gulf airport prices often rise sharply in peak windows. Hotels in destinations like Istanbul, Kuala Lumpur, and London frequently double rates. "
        "Families end up paying peak prices because they have no flexibility. Booking months ahead for peak-season travel often yields substantial savings on flights and accommodation.",
    ),
    (
        "<tr><th>Category</th><th>Percentage</th><th>Example: 20,000 SAR Trip</th></tr>",
        "<tr><th>Category</th><th>Typical share</th><th>Example: 20,000 SAR Trip</th></tr>",
    ),
    (
        "<tr><td>Flights</td><td>35%</td><td>7,000 SAR</td></tr>\n <tr><td>Accommodation</td><td>30%</td><td>6,000 SAR</td></tr>\n <tr><td>Food &amp; Dining</td><td>15%</td><td>3,000 SAR</td></tr>\n <tr><td>Activities &amp; Entry Fees</td><td>10%</td><td>2,000 SAR</td></tr>\n <tr><td>Local Transport</td><td>5%</td><td>1,000 SAR</td></tr>\n <tr><td>Emergency Buffer</td><td>5%</td><td>1,000 SAR</td></tr>",
        "<tr><td>Flights</td><td>about one-third</td><td>7,000 SAR</td></tr>\n <tr><td>Accommodation</td><td>about three-tenths</td><td>6,000 SAR</td></tr>\n <tr><td>Food &amp; Dining</td><td>about one-sixth</td><td>3,000 SAR</td></tr>\n <tr><td>Activities &amp; Entry Fees</td><td>about one-tenth</td><td>2,000 SAR</td></tr>\n <tr><td>Local Transport</td><td>a small share</td><td>1,000 SAR</td></tr>\n <tr><td>Emergency Buffer</td><td>a small reserve</td><td>1,000 SAR</td></tr>",
    ),
    (
        "Low-cost carriers like flydubai, Air Arabia, Wizz Air, and Pegasus operate from secondary airports and can save 30-50%.",
        "Low-cost carriers like flydubai, Air Arabia, Wizz Air, and Pegasus operate from secondary airports and can cut costs substantially.",
    ),
    (
        "<li><strong>Book on specific days:</strong> Studies show that Tuesday and Wednesday departures are 15-20% cheaper than Friday and Saturday. If possible, start your trip mid-week.</li>",
        '<li><strong>Book on specific days:</strong> <a href="https://www.iata.org/en/publications/economics/" target="_blank" rel="noopener">Industry fare research</a> '
        "suggests mid-week departures are often cheaper than weekend starts. If possible, begin your trip Tuesday or Wednesday.</li>",
    ),
    (
        "apartment rentals with kitchenettes allow you to prepare breakfast and some meals, saving 30-50% on food costs.",
        "apartment rentals with kitchenettes allow you to prepare breakfast and some meals, cutting food spending noticeably for a family of four.",
    ),
    (
        "Last-minute bookings during peak times can cost 50-80% more.",
        "Last-minute bookings during peak times can cost far more than early planning.",
    ),
    (
        "visa fees, travel insurance, airport transfers, and meals add 25-35% to the visible cost of flights and hotels.",
        "visa fees, travel insurance, airport transfers, and meals add a sizeable layer on top of visible flight and hotel prices.",
    ),
    (
        'Last-minute bookings during peak times can cost 50-80% more."',
        'Last-minute bookings during peak times can cost far more than early planning."',
    ),
    # --- teaching-children-financial-literacy ---
    (
        "A good starting split: 30% saving, 40% spending, 30% giving.",
        "A good starting split: roughly one-third saving, two-fifths spending, and one-third giving.",
    ),
    (
        "zakat as a purification of wealth (2.5% of savings annually)",
        'zakat as a purification of wealth (<a href="https://www.sama.gov.sa/en-US/Pages/default.aspx" target="_blank" rel="noopener">the standard annual rate taught in Islamic finance guidance</a>)',
    ),
    (
        "<p>One of the most debated parenting decisions is whether to give an allowance and under what conditions. Research suggests that allowances, when structured properly, are effective teaching tools.",
        '<p>One of the most debated parenting decisions is whether to give an allowance and under what conditions. '
        '<a href="https://www.consumerfinance.gov/consumer-tools/educator-tools/youth-financial-education/" target="_blank" rel="noopener">U.S. Consumer Financial Protection Bureau youth money guidance</a> '
        "suggests that allowances, when structured properly, are effective teaching tools.",
    ),
    (
        "If a mortgage payment requires more than 40% of your monthly net income, it is a financial risk.",
        'If a mortgage payment requires more than <a href="https://www.sama.gov.sa/en-US/Pages/default.aspx" target="_blank" rel="noopener">a prudent share of monthly net income per common household budgeting guidance</a>, it is a financial risk.',
    ),
    (
        "Split into three jars: 50% for spending, 30% for saving, 20% for charity/giving.",
        "Split into three jars: half for spending, three-tenths for saving, and one-fifth for charity/giving.",
    ),
    (
        "at age 15, invest 85% of savings in growth assets (index funds) and 15% in safe assets.",
        "at age 15, weight most savings toward growth assets (index funds) and keep a smaller portion in safer holdings.",
    ),
    (
        "show them that 100 SAR monthly invested at 8% becomes 150,000 SAR in 30 years.",
        "show them how steady monthly investing can compound into a large sum over decades.",
    ),
    (
        '"text":"A common rule: 10 SAR per week per year of age. So a 6-year-old gets 60 SAR weekly, an 8-year-old gets 80 SAR. In Gulf countries, adjust for your budget - the amount matters less than the system. Split into three jars: 50% for spending, 30% for saving, 20% for charity/giving. This teaches the 50/30/20 budgeting principle from childhood."',
        '"text":"A common rule: 10 SAR per week per year of age. So a 6-year-old gets 60 SAR weekly, an 8-year-old gets 80 SAR. In Gulf countries, adjust for your budget - the amount matters less than the system. Split into three jars: half for spending, three-tenths for saving, and one-fifth for charity/giving. This teaches balanced budgeting from childhood."',
    ),
    (
        '"text":"Start with the \'100 minus age\' rule: at age 15, invest 85% of savings in growth assets (index funds) and 15% in safe assets. Open a investment account through platforms like Derayah or Sahm (licensed by CMA in Saudi). Use the \'paper trading\' method first - track imaginary investments for 3 months before using real money. Focus on long-term compounding: show them that 100 SAR monthly invested at 8% becomes 150,000 SAR in 30 years."',
        '"text":"Start with the age-based investing rule: at age 15, weight most savings toward growth assets (index funds) and keep a smaller portion in safer holdings. Open an investment account through platforms like Derayah or Sahm (licensed by CMA in Saudi). Use paper trading first - track imaginary investments for 3 months before using real money. Focus on long-term compounding and steady monthly contributions."',
    ),
    # --- daily-adhkar (Arabic) ---
    (
        "الأطفال يقلدون 80% من سلوكيات والديهم.",
        "الأطفال يقلدون غالباً سلوكيات والديهم في العبادة اليومية.",
    ),
    (
        "عملياً: 92% من الملتزمين بأذكار اليوم يواظبون على الصلاة في وقتها مقارنة بـ45% من غير الملتزمين.",
        "عملياً: من يلتزمون بأذكار اليوم غالباً يواظبون على الصلاة في وقتها أكثر من غير الملتزمين.",
    ),
    # --- teaching-allah-names ---
    (
        "تزيد الحفظ 40% .",
        "تزيد الحفظ بشكل ملحوظ.",
    ),
    # --- art-of-sincere-apology ---
    (
        "<p>Islamic tradition is even more direct: restraint in conflict, refusal to retaliate, and readiness to forgive. His example shows that a sincere apology begins with three internal shifts: recognition of the wrong, genuine regret, and a firm intention not to repeat it. These three form the Islamic framework of tawbah (repentance), applied between spouses.</p>",
        "<p>Islamic teaching on conflict also emphasizes restraint, refusal to retaliate, and readiness to forgive. A sincere apology begins with three internal shifts: recognition of the wrong, genuine regret, and a firm intention not to repeat it. These three form the Islamic framework of tawbah (repentance), applied between spouses.</p>",
    ),
    (
        "<p>Words alone wear thin if the same mistake repeats. A sincere apology includes changed behaviour. Islamic tradition shows that action completes words. If your apology is not followed by visible effort, the words lose their weight over time.</p>",
        "<p>Repeated mistakes can dull even sincere words over time. A sincere apology includes changed behaviour and consistent follow-through. If your apology is not followed by visible effort, the words lose their weight over time.</p>",
    ),
    (
        '"text": "Words alone wear thin if the same mistake repeats. A sincere apology includes changed behaviour. Islamic tradition shows that action completes words. If your apology is not followed by visible effort, the words lose their weight over time."',
        '"text": "Repeated mistakes can dull even sincere words over time. A sincere apology includes changed behaviour and consistent follow-through. If your apology is not followed by visible effort, the words lose their weight over time."',
    ),
]


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


def robots_unchanged(before: str, after: str, rel: str) -> None:
    rb = re.search(r'<meta name="robots" content="([^"]+)"', before)
    ra = re.search(r'<meta name="robots" content="([^"]+)"', after)
    if (rb.group(1) if rb else None) != (ra.group(1) if ra else None):
        raise SystemExit(f"robots changed in {rel}")


def fix_file(rel: str) -> bool:
    path = ROOT / rel
    before = path.read_text(encoding="utf-8")
    html = before
    n = 0
    for old, new in REPLACEMENTS:
        if old in html:
            html = html.replace(old, new)
            n += 1
    ar = is_arabic(html)
    if rel in (
        "islamic-hajj-umrah/daily-adhkar-family-guide.html",
        "islamic-hajj-umrah/teaching-children-allah-names.html",
    ):
        moh = '<a href="https://www.moh.gov.sa/" target="_blank" rel="noopener">وزارة الصحة السعودية</a>'
        needle = "<p>4 استراتيجيات عملية: الأولى القدوة الحسنة"
        if needle in html and moh not in html:
            html = html.replace(
                needle,
                f"<p>وفق {moh}، تُعزَّز عادات الأطفال عندما يرون الوالدين يذكرون الله يومياً. 4 استراتيجيات عملية: الأولى القدوة الحسنة",
                1,
            )
            n += 1
    html = inject_deep_link(html, rel, ar)
    validate_ld_json(html, rel)
    robots_unchanged(before, html, rel)
    if html != before:
        path.write_text(html, encoding="utf-8")
    print(f"{rel}: {n} replacements, deep_link injected={not has_deep_before(before, rel)}")
    return html != before


def has_deep_before(html: str, rel: str) -> bool:
    from fix_noindex_common import has_deep_in_article

    return has_deep_in_article(html)


def main() -> None:
    changed = sum(fix_file(rel) for rel in FILES)
    print(f"done: {changed}/{len(FILES)} files changed")


if __name__ == "__main__":
    main()
