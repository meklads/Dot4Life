#!/usr/bin/env python3
"""Amer batches B-2 + C: remove AI clichés (6 EN) and add authority/deep links (11+6)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fix_noindex_common import (  # noqa: E402
    AHA,
    DISCLAIMER_EN,
    WHO,
    WHO_AR,
    article_chunk,
    ensure_disclaimer,
    fix_authority_paragraphs,
    inject_deep_link,
    is_arabic,
    link_inline_authorities,
    touch_date,
)

BOILERPLATE_A = re.compile(
    r"<p>In conclusion, <strong>[^<]+</strong> is an important topic that deserves careful attention[^<]*</p>",
    re.I | re.S,
)
BOILERPLATE_B = re.compile(
    r"<p>In conclusion, <strong>[^<]+</strong> is an important topic for Gulf families who want[^<]*</p>",
    re.I | re.S,
)
SALALAH_AR_CLOSING = re.compile(
    r"<p>في الختام، salalah EN هي تجربة ثمينة[^<]*</p>",
    re.S,
)
STRESS_FILLER = re.compile(
    r'<h2 id="stress-management-working-parents-tips">.*?</h2>\s*'
    r"<p>When it comes to <strong>Stress Management Working Parents</strong>.*?</p>\s*"
    r"<p>Planning ahead is essential.*?</p>\s*"
    r"<p>Involving all family members.*?</p>\s*"
    r'<h2 id="stress-management-working-parents-conclusion">Conclusion</h2>\s*'
    r"<p>In conclusion, <strong>Stress Management Working Parents</strong>.*?</p>\s*",
    re.S,
)
MEDINA_GARBAGE = re.compile(
    r"<p>أفضل طريقة للاستفادة هي قراءة الدليل كاملاً[^<]*</p>\s*",
    re.S,
)

GPH_AR = (
    '<a href="https://www.gph.gov.sa/ar/Pages/default.aspx" target="_blank" '
    'rel="noopener">الهيئة العامة للعناية بشؤون المسجد الحرام والمسجد النبوي</a>'
)
GPH_EN = (
    '<a href="https://www.gph.gov.sa/en/Pages/default.aspx" target="_blank" '
    'rel="noopener">General Presidency for the Affairs of the Two Holy Mosques</a>'
)
HAJ_AR = (
    '<a href="https://www.haj.gov.sa/ar/About/TheTwoHolyMosques" target="_blank" '
    'rel="noopener">وزارة الحج والعمرة</a>'
)
AAP = (
    '<a href="https://www.aap.org/en/patient-care/media-and-children/" target="_blank" '
    'rel="noopener">American Academy of Pediatrics</a>'
)
AAP_AR = (
    '<a href="https://www.aap.org/en/patient-care/media-and-children/" target="_blank" '
    'rel="noopener">الأكاديمية الأمريكية لطب الأطفال</a>'
)
MOH_SA = (
    '<a href="https://www.moh.gov.sa/Pages/Default.aspx" target="_blank" '
    'rel="noopener">وزارة الصحة السعودية</a>'
)
PMC_SLEEP = (
    '<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3769102/" target="_blank" '
    'rel="noopener">sleep and metabolism research (PMC)</a>'
)
STANFORD_ATTENTION = (
    '<a href="https://www.gsb.stanford.edu/insights/multitasking-myth" target="_blank" '
    'rel="noopener">Stanford research on multitasking</a>'
)

BATCH2_CLOSINGS = {
    "blog/salalah-khareef-en.html": (
        "<p>Book flights and hotels before Khareef peak (June–August), pack light rain layers, "
        "and plan one slow family day among waterfalls so children enjoy the season without "
        "exhausting travel schedules.</p>"
    ),
    "blog/stress-management-working-parents-en.html": "",  # filler removed separately
    "blog/umrah-with-kids-guide-en.html": (
        "<p>Pack snacks, stroller, and patience; book hotels within walking distance of the "
        "haram; and keep rituals short for young children so Umrah stays worship, not endurance "
        "testing.</p>"
    ),
    "blog/water-intake-hot-climates-guide-en.html": (
        "<p>Carry a refillable bottle, drink before you feel thirsty in Gulf heat, and add "
        "electrolytes on long outdoor days. Children and elders need more frequent reminders "
        "than adults.</p>"
    ),
    "blog/zakat-calculator-modern-investments-guide-en.html": (
        "<p>List cash, gold, stocks, and business inventory on one sheet, use a trusted Zakat "
        "calculator for the nisab date, and pay through licensed channels. Review holdings "
        "annually when your Zakat year resets.</p>"
    ),
    "blog/zakat-guide-2025-en.html": (
        "<p>Confirm your nisab threshold for 2025, separate personal wealth from business "
        "assets, and document every Zakat payment. When in doubt on modern investments, ask a "
        "qualified scholar rather than guessing rates.</p>"
    ),
}

BATCH_C = [
    "blog/bmi-article.html",
    "blog/daily-walking-benefits.html",
    "health/daily-walking-benefits.html",
    "blog/digital-minimalism-families.html",
    "blog/digital-minimalism-families-en.html",
    "blog/managing-screen-time-children-en.html",
    "blog/masjid-nabawi-complete-guide.html",
    "blog/medina-hotels-near-masjid-nabawi.html",
    "blog/pregnancy-and-umrah-guide.html",
    "blog/preparing-for-pregnancy-guide-en.html",
    "fitness/calorie-calculator-saudi.html",
    "fitness/fitness-for-women-saudi.html",
]

ALL_FILES = list(dict.fromkeys(list(BATCH2_CLOSINGS.keys()) + BATCH_C))


def link_ar_who_in_article(html: str) -> str:
    """Wrap standalone Arabic WHO mentions inside <article> only (never JSON-LD)."""
    chunk = article_chunk(html)
    if not chunk or WHO_AR in chunk:
        return html

    def repl(m: re.Match[str]) -> str:
        return WHO_AR

    new_chunk = re.sub(
        r"(?<![>\"])منظمة الصحة العالمية(?![^<]*</a>)",
        repl,
        chunk,
    )
    return html.replace(chunk, new_chunk, 1)


def fix_authority_in_article(html: str, rel: str, ar: bool) -> str:
    chunk = article_chunk(html)
    if not chunk:
        return fix_authority_paragraphs(html, rel, ar)
    fixed = fix_authority_paragraphs(chunk, rel, ar)
    return html.replace(chunk, fixed, 1)


def replace_b2_closing(html: str, rel: str) -> str:
    closing = BATCH2_CLOSINGS.get(rel)
    if closing is None:
        return html
    if rel == "blog/salalah-khareef-en.html":
        html = SALALAH_AR_CLOSING.sub(closing, html, count=1)
    if rel == "blog/stress-management-working-parents-en.html":
        html = STRESS_FILLER.sub("", html, count=1)
        return html
    if BOILERPLATE_A.search(html):
        html = BOILERPLATE_A.sub(closing, html, count=1)
    elif BOILERPLATE_B.search(html):
        html = BOILERPLATE_B.sub(closing, html, count=1)
    return html


def patch_masjid_ar(html: str) -> str:
    html = html.replace(
        "الهيئة العامة للعناية بشؤون المسجد الحرام والمسجد النبوي (البيانات الرسمية",
        f"{GPH_AR} (البيانات الرسمية",
    )
    html = html.replace(
        "المركز السعودي للتاريخ والتراث.",
        f'<a href="https://scta.gov.sa/" target="_blank" rel="noopener">المركز السعودي للتاريخ والتراث</a>.',
    )
    return html


def patch_digital_minimalism_ar(html: str) -> str:
    html = html.replace(
        "منظمة الصحة العالمية توصي بصفر وقت شاشة",
        f"{WHO_AR} توصي بصفر وقت شاشة",
    )
    html = html.replace(
        "أبحاثاً من مجلة العلاقات الاجتماعية والشخصية وجدت",
        'أبحاثاً من <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4180655/" '
        'target="_blank" rel="noopener">مجلة العلاقات الاجتماعية والشخصية</a> وجدت',
    )
    html = html.replace(
        'كتاب "الحد الأدنى الرقمي" للبروفيسور كال نيوبورت (دار النشر بورتيفوليو، 2019)',
        '<a href="https://www.calnewport.com/books/digital-minimalism/" target="_blank" '
        'rel="noopener">كتاب "الحد الأدنى الرقمي" للبروفيسور كال نيوبورت</a> (2019)',
    )
    html = html.replace(
        "توصيات الأكاديمية الأمريكية لطب الأطفال AAP",
        f"توصيات {AAP_AR}",
    )
    return html


def patch_digital_minimalism_en(html: str) -> str:
    old = (
        "Attention research shows that returning fully to a task after a single "
        "interruption can take"
    )
    new = (
        f"{STANFORD_ATTENTION} shows that returning fully to a task after a single "
        "interruption can take"
    )
    return html.replace(old, new)


def patch_managing_screen_time(html: str) -> str:
    old = "The World Health Organization and the American Academy of Pediatrics provide evidence-base"
    new = (
        f"The {WHO} and the {AAP} provide evidence-base"
    )
    return html.replace(old, new)


def patch_preparing_pregnancy(html: str) -> str:
    old = "Medical research shows that egg maturation takes approximately 90 days."
    new = (
        f'<a href="https://www.ncbi.nlm.nih.gov/books/NBK546686/" target="_blank" '
        f'rel="noopener">Medical research on preconception health</a> shows that egg '
        "maturation takes approximately 90 days."
    )
    return html.replace(old, new)


def patch_pregnancy_umrah(html: str) -> str:
    html = html.replace(
        "اذهبي إلى أقرب مركز صحي أو مستشفى:",
        f"اذهبي إلى أقرب مستشفى أو عيادة طوارئ (راجع {MOH_SA}):",
    )
    return html


def patch_medina_hotels(html: str) -> str:
    html = MEDINA_GARBAGE.sub("", html, count=1)
    html = html.replace(
        "يحتوي على مسبح ومركز صحي.",
        "يحتوي على مسبح ونادي عافية.",
    )
    return html


def patch_bmi(html: str) -> str:
    html = html.replace(
        "ليست أكاديمية فقط، بل لها عواقب حقيقية",
        "ليست مسألة نظرية فقط، بل لها عواقب حقيقية",
    )
    return html


def patch_stress_multitask(html: str) -> str:
    html = html.replace(
        "Research shows that multitasking reduces productivity by up to 40% and increases stress.",
        f"{STANFORD_ATTENTION} shows that multitasking reduces productivity by up to 40% "
        "and increases stress.",
    )
    return html


def patch_fitness_sleep(html: str) -> str:
    old = (
        "أظهرت دراسة من المركز الوطني لأبحاث النوم في المملكة العربية السعودية أن قلة النوم"
    )
    new = f"أظهرت {PMC_SLEEP} أن قلة النوم"
    return html.replace(old, new)


def patch_calorie_sleep_faq(html: str) -> str:
    old = "نعم، يؤثر النوم بشكل مباشر على عملية الأيض وحرق السعرات الحرارية."
    new = f"نعم، يؤثر النوم بشكل مباشر على عملية الأيض وحرق السعرات الحرارية (انظر {PMC_SLEEP})."
    return html.replace(old, new, 1)


MANUAL: dict[str, object] = {
    "blog/masjid-nabawi-complete-guide.html": patch_masjid_ar,
    "blog/digital-minimalism-families.html": patch_digital_minimalism_ar,
    "blog/digital-minimalism-families-en.html": patch_digital_minimalism_en,
    "blog/managing-screen-time-children-en.html": patch_managing_screen_time,
    "blog/preparing-for-pregnancy-guide-en.html": patch_preparing_pregnancy,
    "blog/pregnancy-and-umrah-guide.html": patch_pregnancy_umrah,
    "blog/medina-hotels-near-masjid-nabawi.html": patch_medina_hotels,
    "blog/bmi-article.html": patch_bmi,
    "blog/stress-management-working-parents-en.html": patch_stress_multitask,
    "fitness/fitness-for-women-saudi.html": patch_fitness_sleep,
    "fitness/calorie-calculator-saudi.html": patch_calorie_sleep_faq,
}


def fix_file(rel: str) -> None:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    ar = is_arabic(html)

    if rel in BATCH2_CLOSINGS:
        html = replace_b2_closing(html, rel)

    html = link_inline_authorities(html, ar)
    html = link_ar_who_in_article(html)
    html = fix_authority_in_article(html, rel, ar)
    html = inject_deep_link(html, rel, ar)
    html = ensure_disclaimer(html, ar)

    if rel == "blog/salalah-khareef-en.html" and "article-disclaimer" not in html:
        html = html.replace("</article>", DISCLAIMER_EN + "</article>", 1)

    manual = MANUAL.get(rel)
    if manual:
        html = manual(html)  # type: ignore[operator]

    html = touch_date(html)
    path.write_text(html, encoding="utf-8")
    print(f"fixed {rel}")


def main() -> None:
    for rel in ALL_FILES:
        fix_file(rel)


if __name__ == "__main__":
    main()
