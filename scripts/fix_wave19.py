#!/usr/bin/env python3
"""Wave 19: amer_gate fixes — Article schema, hydration, homeschool, budget."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DISCLAIMER_AR = (
    '<div class="tip"><p><strong>إخلاء مسؤولية:</strong> معلومات عامة فقط وليست استشارة '
    "طبية أو مالية أو فتوى شرعية. راجع مختصاً مرخصاً عند الحاجة.</p></div>\n"
)

FILES = [
    "comparisons/gold-vs-real-estate-gulf-family.html",
    "finance-wealth/investment-basics-beginners.html",
    "featured-stories/mother-homeschooled-five-children.html",
    "health/hydration-guide-hot-climates-families.html",
    "comparisons/domestic-vs-international-travel-family.html",
    "blog/house-affordability-single-income-guide.html",
    "finance-wealth/family-budget-plan.html",
]

HERO_GOLD = "/assets/images/approved/hero-gold-vs-real-estate-gulf-family.webp"
HERO_INVEST = "/assets/images/approved/hero-investment-basics-beginners.webp"
HERO_HYDRATION = "/assets/images/approved/hero-daily-walking-benefits.webp"
WHO = (
    '<a href="https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health" '
    'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
)
EFSA = (
    '<a href="https://www.efsa.europa.eu/en/topics/topic/dietary-reference-values" '
    'target="_blank" rel="noopener">الهيئة الأوروبية لسلامة الأغذية</a>'
)
SAMA = (
    '<a href="https://www.sama.gov.sa/ar-sa/Laws/Pages/default.aspx" '
    'target="_blank" rel="noopener">البنك المركزي السعودي (ساما)</a>'
)
SAMA_MIZANIYATI = (
    '<a href="https://www.sama.gov.sa/ar-sa/FinancialEducation/Pages/default.aspx" '
    'target="_blank" rel="noopener">تطبيق ميزانيتي من البنك المركزي السعودي</a>'
)
KAU = (
    '<a href="https://www.kau.edu.sa/" target="_blank" rel="noopener">جامعة الملك عبدالعزيز</a>'
)
KFUPM = (
    '<a href="https://www.kfupm.edu.sa/" target="_blank" rel="noopener">جامعة الملك فهد للبترول والمعادن</a>'
)
KSU = (
    '<a href="https://www.ksu.edu.sa/" target="_blank" rel="noopener">جامعة الملك سعود</a>'
)
VISIT_SAUDI = (
    '<a href="https://www.visitsaudi.com/en/see-do/destinations/abha" target="_blank" rel="noopener">هيئة السياحة السعودية</a>'
)
KHAN = (
    '<a href="https://ar.khanacademy.org/" target="_blank" rel="noopener">أكاديمية خان</a>'
)
MOE = (
    '<a href="https://www.moe.gov.sa/ar/education/Pages/default.aspx" '
    'target="_blank" rel="noopener">وزارة التعليم</a>'
)

AR_SUBSCRIBE = '<p>احصل على نصائح أسرية كل جمعة عبر نشرتنا البريدية.</p>'
EN_SUB_RE = re.compile(
    r'<p><span class="en">Get (?:more family tips|weekly inspiration|more family finance tips|more family wellness tips)[^<]*</span>'
    r'<span class="ar">[^<]+</span></p>',
    re.S,
)


def fix_all_em_dashes(html: str) -> str:
    return html.replace("—", ",").replace("–", ",")


def insert_before_article_close(html: str, block: str) -> str:
    if block.strip() in html:
        return html
    return re.sub(r"</article>", block + "</article>", html, count=1)


def remove_in_content_subscribe(html: str) -> str:
    html = re.sub(
        r'<div class="in-content-subscribe">.*?</div>\s*</div>\s*',
        "",
        html,
        count=1,
        flags=re.S,
    )
    return re.sub(r"\n</div>\s*\n<h2", "\n<h2", html, count=3)


def arabify_in_article_ctas(html: str) -> str:
    html = EN_SUB_RE.sub(AR_SUBSCRIBE, html)
    return html


def add_article_schema(html: str, headline: str, description: str, url: str, image: str) -> str:
    if '"@type": "Article"' in html or '"@type":"Article"' in html:
        return html
    block = (
        '<script type="application/ld+json">'
        '{"@context": "https://schema.org", "@type": "Article", '
        f'"headline": "{headline}", "description": "{description}", '
        '"author": {"@type": "Organization", "name": "دوت فور لايف"}, '
        '"datePublished": "2026-06-30", "dateModified": "2026-07-09", '
        f'"mainEntityOfPage": "{url}", '
        f'"image": "https://dotforlife.com{image}"}}'
        "</script>\n"
    )
    return html.replace(
        '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"',
        block + '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"',
        1,
    )


def touch_date(html: str) -> str:
    return re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=1)


def fix_gold(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = add_article_schema(
        html,
        "الاستثمار في الذهب أم العقار للأسرة الخليجية؟",
        "مقارنة كاملة بين الاستثمار في الذهب والعقار للعائلة الخليجية.",
        "https://dotforlife.com/comparisons/gold-vs-real-estate-gulf-family.html",
        HERO_GOLD,
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_investment(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = add_article_schema(
        html,
        "استثمار المبتدئ الخليجي: دليل عملي",
        "دليل عملي لبداية الاستثمار للأسرة الخليجية بمبلغ صغير.",
        "https://dotforlife.com/finance-wealth/investment-basics-beginners.html",
        HERO_INVEST,
    )
    html = remove_in_content_subscribe(html)
    html = re.sub(
        r'\n<h2 id="faq"><span class="en">Frequently Asked Questions</span><span class="ar">الأسئلة الشائعة</span></h2>.*?</article>',
        "\n</article>",
        html,
        count=1,
        flags=re.S,
    )
    html = arabify_in_article_ctas(html)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_homeschool(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = fix_all_em_dashes(html)
    html = html.replace(
        "في جامعة سعودية مرموقة",
        f"في {KSU}",
    )
    html = html.replace(
        "تدرس الدراسات الإسلامية في الجامعة",
        f"تدرس الدراسات الإسلامية في {KSU}",
    )
    html = html.replace(
        "أمّاً تعلّم في المنزل",
        f"أمّاً تعلّم في المنزل، كما تشجعها {MOE}",
    )
    html = html.replace("أكاديمية خان،", f"{KHAN}،")
    html = html.replace("أكاديمية خان للرياضيات،", f"{KHAN} للرياضيات،")
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_hydration(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"https://images\.unsplash\.com/[^\"']+", HERO_HYDRATION, html)
    html = fix_all_em_dashes(html)
    html = html.replace(
        "الهيئة الأوروبية لسلامة الأغذية (EFSA) ومنظمة الصحة العالمية تقدم",
        f"{EFSA} و{WHO} تقدمان",
    )
    html = html.replace(
        "(hyponatremia)",
        "(نقص صوديوم الدم)",
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_domestic_travel(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        'href="https://www.visitsaudi.com/ar"',
        'href="https://www.visitsaudi.com/en/see-do/destinations/abha"',
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_house(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "شراء منزل بدخل واحد يتطلب تخطيطاً مالياً دقيقاً",
        f"وفق {SAMA}، شراء منزل بدخل واحد يتطلب تخطيطاً مالياً دقيقاً",
    )
    html = html.replace(
        "دراسة من جامعة الملك فهد للبترول والمعادن 2024",
        f"دراسة من {KFUPM}",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_family_budget(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "تطبيق ميزانيتي من البنك المركزي السعودي",
        SAMA_MIZANIYATI,
    )
    html = html.replace(
        "وجدت دراسة من جامعة الملك عبدالعزيز 2024",
        f"وفق {KAU}، وجدت دراسة",
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = re.sub(
        r"\n<h2 id=\"budget-plan-steps\">.*?</article>",
        "\n</article>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r"اقرأ أيضاً:.*?</p>\s*\n</div>",
        lambda m: m.group(0).replace("</p>", "").replace(
            "اقرأ أيضاً:",
            "<p>اقرأ أيضاً:",
        ),
        html,
        count=1,
        flags=re.S,
    )
    path.write_text(touch_date(html), encoding="utf-8")


def main() -> int:
    handlers = {
        "gold-vs-real-estate-gulf-family": fix_gold,
        "investment-basics-beginners": fix_investment,
        "mother-homeschooled-five-children": fix_homeschool,
        "hydration-guide-hot-climates-families": fix_hydration,
        "domestic-vs-international-travel-family": fix_domestic_travel,
        "house-affordability-single-income-guide": fix_house,
        "family-budget-plan": fix_family_budget,
    }
    for rel in FILES:
        fp = ROOT / rel
        for key, fn in handlers.items():
            if key in rel:
                fn(fp)
                print(f"Fixed {rel}")
                break

    r = subprocess.run(
        ["python3", "scripts/amer_gate.py", *FILES],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    if r.stderr.strip():
        print(r.stderr, file=sys.stderr)
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
