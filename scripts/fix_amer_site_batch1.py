#!/usr/bin/env python3
"""Amer site-wide audit: disclaimers + em-dash cleanup for tools batches."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DISCLAIMERS = {
    "health": (
        '  <div class="tip"><p><strong><span class="en">Disclaimer:</span>'
        '<span class="ar">إخلاء مسؤولية:</span></strong> '
        '<span class="en">This tool provides general estimates for educational purposes only; '
        "it is not medical advice. Consult a healthcare professional before changing diet, "
        'exercise, or health plans.</span>'
        '<span class="ar">هذه الأداة تقدّم تقديرات عامة لأغراض تثقيفية فقط وليست استشارة طبية. '
        "راجع طبيباً أو مختصاً قبل تغيير نظامك الغذائي أو النشاط أو أي خطة صحية.</span></p></div>\n"
    ),
    "finance": (
        '  <div class="tip"><p><strong><span class="en">Disclaimer:</span>'
        '<span class="ar">إخلاء مسؤولية:</span></strong> '
        '<span class="en">This tool offers general financial estimates for education only; '
        "it is not financial, tax, or Sharia advice. Consult a licensed advisor for your situation.</span>"
        '<span class="ar">هذه الأداة تقدّم تقديرات مالية عامة لأغراض تثقيفية فقط وليست استشارة مالية أو ضريبية أو فتوى. '
        "راجع مستشاراً مرخصاً يناسب وضعك.</span></p></div>\n"
    ),
    "islamic": (
        '  <div class="tip"><p><strong><span class="en">Disclaimer:</span>'
        '<span class="ar">إخلاء مسؤولية:</span></strong> '
        '<span class="en">This tool uses standard calendar or geographic algorithms for general reference; '
        "it is not a religious ruling. For worship and official matters, follow your local authority "
        'and qualified scholars.</span>'
        '<span class="ar">هذه الأداة تستخدم خوارزميات تقويمية أو جغرافية معيارية للمرجع العام فقط وليس فتوى. '
        "للعبادات والأمور الرسمية، اتبع الجهة المحلية وأهل العلم المؤهلين.</span></p></div>\n"
    ),
    "security": (
        '  <div class="tip"><p><strong><span class="en">Disclaimer:</span>'
        '<span class="ar">إخلاء مسؤولية:</span></strong> '
        '<span class="en">Passwords are generated locally in your browser; we do not store them. '
        "Use unique passwords and a reputable password manager for important accounts.</span>"
        '<span class="ar">تُولَّد كلمات المرور محلياً في متصفحك ولا نخزّنها. '
        "استخدم كلمات مرور فريدة ومدير كلمات مرور موثوقاً للحسابات المهمة.</span></p></div>\n"
    ),
    "general": (
        '  <div class="tip"><p><strong><span class="en">Disclaimer:</span>'
        '<span class="ar">إخلاء مسؤولية:</span></strong> '
        '<span class="en">This tool offers general guidance for education only; it is not professional '
        "advice. Adjust schedules, care routines, or habits based on your own needs and qualified "
        'experts when needed.</span>'
        '<span class="ar">هذه الأداة تقدّم إرشاداً عاماً لأغراض تثقيفية فقط وليست استشارة مهنية. '
        "عدّل الجداول أو روتين العناية أو العادات وفق احتياجك وخبراء مؤهلين عند الحاجة.</span></p></div>\n"
    ),
}

BATCH1 = [
    ("tools/age-calculator.html", "health"),
    ("tools/hijri-converter.html", "islamic"),
    ("tools/monthly-budget.html", "finance"),
    ("tools/mortgage-calculator.html", "finance"),
    ("tools/one-rep-max.html", "health"),
    ("tools/password-generator.html", "security"),
]

BATCH2 = [
    ("tools/plant-watering.html", "general"),
    ("tools/pomodoro.html", "general"),
    ("tools/pregnancy-calculator.html", "health"),
    ("tools/qibla.html", "islamic"),
    ("tools/rental-yield-calculator.html", "finance"),
    ("tools/roi-calculator.html", "finance"),
]

DISCLAIMER_AR_STD = (
    '<div class="tip"><p><strong>إخلاء مسؤولية:</strong> معلومات عامة فقط وليست استشارة '
    "طبية أو مالية أو فتوى شرعية. راجع مختصاً مرخصاً عند الحاجة.</p></div>\n"
)
DISCLAIMER_AR_FAMILY = (
    '<div class="tip"><p><strong>إخلاء مسؤولية:</strong> هذه قصة شخصية وتوجيه عام للعائلات '
    "وليست استشارة نفسية أو تربوية أو مهنية. راجعي مختصاً مرخصاً عند الحاجة.</p></div>\n"
)
DISCLAIMER_EN_STD = (
    '<div class="tip"><p><strong>Disclaimer:</strong> General information only, not medical, '
    "financial, or religious advice. Consult a licensed professional when needed.</p></div>\n"
)
DISCLAIMER_EN_TRAVEL = (
    '<div class="tip"><p><strong>Disclaimer:</strong> Travel information for general education '
    "only; verify permits, prices, and schedules with official sources before you book.</p></div>\n"
)
DISCLAIMER_EN_ISLAMIC_GUIDE = (
    '<div class="tip"><p><strong>Disclaimer:</strong> This guide is general travel and historical '
    "information for education only; it is not a religious ruling (fatwa). For worship, permits, "
    "and spiritual matters, follow official Saudi sources and qualified scholars.</p></div>\n"
)

BATCH3 = [
    ("tools/savings-goal.html", "finance", "main"),
    ("featured-stories/featured-story-saudi-mother.html", "family_ar", "article"),
    ("fitness/calorie-calculator-saudi.html", "health_ar", "article"),
    ("fitness/fitness-for-women-saudi.html", "health_ar", "article"),
    ("blog/masjid-nabawi-complete-guide-en.html", "islamic_en", "article"),
    ("blog/salalah-travel-guide-2025-en.html", "travel_en", "article"),
    ("blog/water-intake-hot-climates-guide.html", "health_ar", "article"),
    ("real-estate/oman-property-roi.html", "finance_en", "article"),
]

BATCHES = {"1": BATCH1, "2": BATCH2}


def has_disclaimer(html: str) -> bool:
    return 'class="tip"' in html and (
        "إخلاء مسؤولية" in html or "Disclaimer:" in html
    )


def disclaimer_block(category: str) -> str:
    return {
        "health": DISCLAIMERS["health"],
        "finance": DISCLAIMERS["finance"],
        "islamic": DISCLAIMERS["islamic"],
        "security": DISCLAIMERS["security"],
        "general": DISCLAIMERS["general"],
        "health_ar": DISCLAIMER_AR_STD,
        "finance_ar": DISCLAIMER_AR_STD,
        "family_ar": DISCLAIMER_AR_FAMILY,
        "islamic_en": DISCLAIMER_EN_ISLAMIC_GUIDE,
        "travel_en": DISCLAIMER_EN_TRAVEL,
        "finance_en": (
            '<div class="tip"><p><strong>Disclaimer:</strong> Real-estate figures are general '
            "estimates for education only; not financial, tax, or legal advice. Consult licensed "
            "advisors and official Oman property regulators before investing.</p></div>\n"
        ),
    }[category]


def patch_masjid_en(html: str) -> str:
    gph = (
        '<a href="https://www.gph.gov.sa/en/Pages/default.aspx" target="_blank" '
        'rel="noopener">General Presidency for the Affairs of the Two Holy Mosques</a>'
    )
    haj = (
        '<a href="https://www.haj.gov.sa/en/About/TheTwoHolyMosques" target="_blank" '
        'rel="noopener">Ministry of Hajj and Umrah</a>'
    )
    html = html.replace(
        "Today, Masjid an-Nabawi covers approximately 400,500 square meters and can "
        "accommodate over 1.6 million worshippers during peak times.",
        "Today, Masjid an-Nabawi covers approximately 400,500 square meters and can "
        f"accommodate over 1.6 million worshippers during peak times (capacity figures "
        f"published by the {haj} and {gph}).",
    )
    html = html.replace(
        "increased its capacity to over 1.6 million worshippers.",
        f"increased its capacity to over 1.6 million worshippers (per {gph} expansion data).",
    )
    html = html.replace(
        "The Rawdah covers approximately 330 square meters and is distinguished",
        f"The Rawdah covers approximately 330 square meters (per {haj} visitor guides) and is distinguished",
    )
    return html


def insert_disclaimer(html: str, category: str, target: str) -> str:
    if has_disclaimer(html):
        return html
    block = disclaimer_block(category)
    close = "</main>" if target == "main" else "</article>"
    if close not in html:
        raise SystemExit(f"missing {close}")
    return html.replace(close, block + close, 1)


def fix_file(rel: str, category: str, target: str = "main") -> None:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    html = insert_disclaimer(html, category, target)
    html = html.replace("—", " - ")
    if rel == "blog/masjid-nabawi-complete-guide-en.html":
        html = patch_masjid_en(html)
    path.write_text(html, encoding="utf-8")
    print(f"fixed {rel}")


def run_batch(batch_id: str) -> None:
    if batch_id == "3":
        for rel, cat, target in BATCH3:
            fix_file(rel, cat, target)
        return
    files = BATCHES.get(batch_id)
    if not files:
        raise SystemExit(f"unknown batch {batch_id!r}")
    for rel, cat in files:
        fix_file(rel, cat, "main")


def main() -> None:
    batch_id = sys.argv[1] if len(sys.argv) > 1 else "1"
    if batch_id == "1":
        backup = ROOT / "tools" / "_finance_backup"
        if backup.is_dir():
            for f in sorted(backup.glob("*.html")):
                f.unlink()
                print(f"deleted {f.relative_to(ROOT)}")
    run_batch(batch_id)


if __name__ == "__main__":
    main()
