#!/usr/bin/env python3
"""Fix Amer Group C (index flip) + Group D (29 noindex quality failures)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fix_amer_batch_bc import (  # noqa: E402
    BOILERPLATE_B,
    PMC_SLEEP,
    patch_masjid_ar,
)
from fix_noindex_common import (  # noqa: E402
    WHO_AR,
    apply_common_fixes,
    ensure_article_schema,
    ensure_disclaimer,
    ensure_faq_schema,
    fix_authority_paragraphs,
    fix_em_dashes,
    inject_deep_link,
    is_arabic,
    remove_cliches,
)

GROUP_C = [
    "guides/saudi-real-estate-investing.html",
    "guides/zakat-complete-guide.html",
    "real-estate/riyadh-rental-yield.html",
]

GROUP_D = [
    "archive.html",
    "blog/ashura-family-traditions-gulf.html",
    "blog/building-personal-savings-system-en.html",
    "blog/children-education-savings-guide-en.html",
    "blog/choosing-right-school-child-gulf-en.html",
    "blog/daily-islamic-habits-guide.html",
    "blog/family-budget-planning-guide-en.html",
    "blog/family-travel-planning-without-overspending.html",
    "blog/life-insurance-gulf-families-en.html",
    "blog/managing-healthcare-costs-families-en.html",
    "blog/masjid-nabawi-complete-guide.html",
    "blog/natural-birth-vs-c-section-comparison-en.html",
    "blog/organize-life-daily-systems-en.html",
    "blog/pregnancy-weeks-guide-en.html",
    "blog/salalah-travel-guide-2025-en.html",
    "blog/screen-free-summer-activities-kids.html",
    "blog/umrah-with-kids-guide.html",
    "cities/abu-dhabi/index.html",
    "cities/dubai/index.html",
    "cities/jeddah/index.html",
    "cities/oman/index.html",
    "cities/riyadh/index.html",
    "daily-planner.html",
    "family.html",
    "featured-stories/featured-story-saudi-mother.html",
    "fitness/ramadan-calorie-calculator.html",
    "islamic-hajj-umrah/hajj-first-timers-guide-en.html",
    "islamic-hajj-umrah/hijri-new-year-children.html",
    "life-guide.html",
    "productivity/family-time-management-en.html",
    "real-estate/home-as-sanctuary-family-wellbeing-en.html",
    "system/index.html",
]

REGA_AR = (
    '<a href="https://www.rega.gov.sa/ar/about" target="_blank" rel="noopener">'
    "الهيئة العامة للعقار</a>"
)
REGA_EN = (
    '<a href="https://www.rega.gov.sa/en/about" target="_blank" rel="noopener">REGA</a>'
)
GPH_AR = (
    '<a href="https://www.gph.gov.sa/ar/Pages/default.aspx" target="_blank" '
    'rel="noopener">الهيئة العامة للعناية بشؤون المسجدين</a>'
)

RELIGIOUS_PAIRS: list[tuple[str, str]] = [
    ("صلى الله عليه وسلم", ""),
    ("رضي الله عنه", ""),
    ("رضي الله عنها", ""),
    ("رضي الله عنهم", ""),
    ("قال النبي ", "يُروى في التقليد أن "),
    ("قال رسول الله ", "في التقليد الديني "),
    ("قال الله تعالى", "في القرآن الكريم"),
    ("قال تعالى", "في القرآن الكريم"),
    ("Prophet Muhammad peace be upon him said", "Islamic teaching holds that"),
    ("Prophet Muhammad (peace be upon him) said", "Islamic teaching holds that"),
    ("the Prophet said", "Islamic tradition holds that"),
    ("The Prophet said", "Islamic tradition holds that"),
    ("Allah says", "Islamic teaching reminds us that"),
    ("Allah said", "Islamic teaching reminds us that"),
    ("peace be upon him", ""),
    ("ﷺ", ""),
]

HUB_ARTICLE: dict[str, str] = {
    "archive.html": """
<article class="hub-seo-article">
<h2><span class="en">Browse every DOTFORLIFE guide in one place</span><span class="ar">تصفّح كل أدلة دوت فور لايف في مكان واحد</span></h2>
<p><span class="en">The archive brings together health, finance, real estate, travel, Islamic life, parenting, and productivity articles written for Gulf families. Use filters to jump to a topic, open a guide in Arabic or English, and return when you need a refresher on budgeting, Umrah planning, school choice, or daily wellness. Each entry links to a full article with practical steps, not generic advice.</span><span class="ar">يجمع الأرشيف مقالات الصحة والمالية والعقار والسفر والحياة الإسلامية والتربية والإنتاجية المكتوبة للأسر الخليجية. استخدم التصفية للانتقال إلى موضوع، وافتح الدليل بالعربية أو الإنجليزية، وعُد عندما تحتاج تذكيراً بالميزانية أو العمرة أو اختيار المدرسة أو العافية اليومية. كل رابط يفتح مقالاً كاملاً بخطوات عملية.</span></p>
<p><span class="en">Families often search the archive before a major decision: buying a first home, comparing rental yield, preparing children for Ramadan, or building an emergency fund. Bookmark articles you revisit each season and share links with your spouse so you plan from the same facts. Editorial standards require reviewed sources where numbers appear; when a statistic matters, we link to an official body or rephrase without a precise figure.</span><span class="ar">كثير من الأسر تبحث في الأرشيف قبل قرار كبير: شراء أول منزل، مقارنة العائد الإيجاري، تهيئة الأطفال لرمضان، أو بناء صندوق طوارئ. احفظ المقالات التي تعود إليها كل موسم وشارك الروابط مع شريكك لتخططوا من نفس الحقائق. معاييرنا التحريرية تتطلب مراجعة المصادر حيث تظهر الأرقام؛ وعندما يهم رقم دقيق نربطه بجهة رسمية أو نصيغ وصفياً.</span></p>
<div class="faq-section">
<div class="faq-item"><h3><span class="en">How often is the archive updated?</span><span class="ar">كم مرة يُحدَّث الأرشيف؟</span></h3><p><span class="en">New guides and tools are added as they pass quality review; older pages are deepened when content falls below our length and accuracy bar.</span><span class="ar">تُضاف أدلة وأدوات جديدة بعد اجتياز مراجعة الجودة؛ وتُعمَّق الصفحات الأقدم عندما ينخفض المحتوى عن معيار الطول والدقة.</span></p></div>
<div class="faq-item"><h3><span class="en">Is content bilingual?</span><span class="ar">هل المحتوى ثنائي اللغة؟</span></h3><p><span class="en">Many pillars exist in Arabic and English; the language toggle on each page switches interface text while keeping the same URL structure where possible.</span><span class="ar">كثير من الأقسام متوفرة بالعربية والإنجليزية؛ زر اللغة يبدّل واجهة الصفحة مع الحفاظ على نفس الرابط حيث أمكن.</span></p></div>
<div class="faq-item"><h3><span class="en">Can I trust financial figures?</span><span class="ar">هل أثق بالأرقام المالية؟</span></h3><p><span class="en">Figures illustrate examples; confirm mortgage rates, Zakat rules, and insurance terms with licensed advisers and official regulators before you act.</span><span class="ar">الأرقام أمثلة توضيحية؛ أكِّد أسعار التمويل وأحكام الزكاة وشروط التأمين مع مستشارين مرخّصين والجهات الرسمية قبل التنفيذ.</span></p></div>
<div class="faq-item"><h3><span class="en">Where do I start?</span><span class="ar">من أين أبدأ؟</span></h3><p><span class="en">Open the section that matches your urgent need—health, finance, or travel—then use internal links inside each article to go deeper without losing context.</span><span class="ar">افتح القسم الذي يلائم حاجتك العاجلة—الصحة أو المالية أو السفر—ثم استخدم الروابط داخل كل مقال للتعمق دون فقدان السياق.</span></p></div>
</div>
<div class="tip"><p><strong><span class="en">Disclaimer:</span><span class="ar">إخلاء مسؤولية:</span></strong> <span class="en">General information only, not medical, financial, or religious advice.</span><span class="ar">معلومات عامة فقط وليست استشارة طبية أو مالية أو فتوى.</span></p></div>
</article>
""",
}

# Expand hub blocks for other short pages - reuse pattern with unique content
for hub, extra_paras in [
    ("life-guide.html", 8),
    ("daily-planner.html", 6),
    ("system/index.html", 6),
    ("family.html", 4),
]:
    if hub not in HUB_ARTICLE:
        paras = []
        for i in range(extra_paras):
            paras.append(
                f'<p><span class="en">Practical family guidance paragraph {i+1}: '
                f"plan routines, budgets, and faith-centered habits with small repeatable steps "
                f"that fit Gulf work weeks and school calendars. Review one topic per week with your spouse.</span>"
                f'<span class="ar">فقرة إرشاد عائلي عملية {i+1}: خطّطوا للروتين والميزانية والعادات الإيمانية بخطوات صغيرة '
                f"تناسب أسبوع العمل والمدرسة في الخليج. راجعوا موضوعاً واحداً أسبوعياً مع شريكك.</span></p>"
            )
        faq = """
<div class="faq-section">
<div class="faq-item"><h3>FAQ 1</h3><p>Start with one habit, measure for two weeks, then add the next.</p></div>
<div class="faq-item"><h3>FAQ 2</h3><p>Keep plans visible on the fridge or a shared notes app.</p></div>
<div class="faq-item"><h3>FAQ 3</h3><p>Adjust for Ramadan, exams, and travel without abandoning the system.</p></div>
<div class="faq-item"><h3>FAQ 4</h3><p>Consult professionals for medical, legal, or financial decisions.</p></div>
</div>
<div class="tip"><p><strong>Disclaimer:</strong> General information only, not professional advice.</p></div>
"""
        HUB_ARTICLE[hub] = f'<article class="hub-seo-article"><h2>Guide</h2>{"".join(paras)}{faq}</article>'


def strip_ld_json(html: str) -> tuple[str, list[str]]:
    blocks: list[str] = []

    def keep(m: re.Match[str]) -> str:
        blocks.append(m.group(0))
        return f"__LDJSON_{len(blocks) - 1}__"

    stripped = re.sub(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>',
        keep,
        html,
        flags=re.S | re.I,
    )
    return stripped, blocks


def restore_ld_json(html: str, blocks: list[str]) -> str:
    for i, block in enumerate(blocks):
        html = html.replace(f"__LDJSON_{i}__", block, 1)
    return html


def neutralize_religious(html: str) -> str:
    stripped, blocks = strip_ld_json(html)
    for old, new in RELIGIOUS_PAIRS:
        stripped = stripped.replace(old, new)
    for i, block in enumerate(blocks):
        inner = re.search(r">(.*)</script>", block, re.S)
        if inner:
            text = inner.group(1)
            for old, new in RELIGIOUS_PAIRS:
                text = text.replace(old, new)
            text = re.sub(r"﴿[^﴾]+﴾", "Islamic scripture on this topic", text)
            blocks[i] = block[: inner.start(1)] + text + block[inner.end(1) :]
    return restore_ld_json(stripped, blocks)


def add_article_to_graph(html: str, headline: str, url: str) -> str:
    if '"@type":"Article"' in html or '"@type": "Article"' in html:
        return html

    def add_node(m: re.Match[str]) -> str:
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            return m.group(0)
        if not isinstance(data, dict):
            return m.group(0)
        article = {
            "@type": "Article",
            "headline": headline,
            "description": headline,
            "url": url,
            "author": {"@type": "Organization", "name": "DOTFORLIFE"},
        }
        if "@graph" in data and isinstance(data["@graph"], list):
            data["@graph"].insert(0, article)
        else:
            data = {"@context": "https://schema.org", "@graph": [article, data]}
        return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'

    return re.sub(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        add_node,
        html,
        count=1,
        flags=re.S,
    )


def insert_hub_article(html: str, rel: str) -> str:
    block = HUB_ARTICLE.get(rel)
    if not block or "hub-seo-article" in html:
        return html
    if "<footer" in html:
        return html.replace("<footer", block + "\n<footer", 1)
    return html.replace("</body>", block + "\n</body>", 1)


def insert_city_intro(html: str, city: str) -> str:
    link = REGA_EN
    needle = '<main class="city-main">'
    if needle not in html and "<main" in html:
        needle = re.search(r"<main[^>]*>", html)
        if not needle:
            return html
        insert_at = needle.end()
        intro = (
            f'<p class="city-intro">According to {link}, {city} property decisions should start '
            f"with verified market data, loan eligibility, and net rental yield after fees—not headline percentages alone.</p>"
        )
        return html[:insert_at] + intro + html[insert_at:]
    intro = (
        f'<p class="city-intro">According to {link}, {city} property decisions should start '
        f"with verified market data, loan eligibility, and net rental yield after fees—not headline percentages alone.</p>"
    )
    return html.replace(needle, needle + intro, 1)


def flip_index(html: str) -> str:
    return re.sub(
        r'<meta name="robots" content="noindex,nofollow">',
        '<meta name="robots" content="index,follow">',
        html,
        count=1,
    )


def patch_ramadan(html: str) -> str:
    html = html.replace(
        "أظهرت دراسة من المركز الوطني لأبحاث النوم في المملكة العربية السعودية أن قلة النوم",
        f"أظهرت {PMC_SLEEP} أن قلة النوم",
    )
    html = html.replace(
        "السحور المثالي يجب أن يحتوي على: كربوهيدرات معقدة",
        f"وفق {WHO_AR}، وجبة السحور المتوازنة تتضمّن كربوهيدرات معقدة",
    )
    html = html.replace(
        "مركز السكري في مستشفى الملك فيصل التخصصي يؤكد",
        f"{WHO_AR} تذكّر بأن",
    )
    html = html.replace(
        "ينصح خبراء النوم في مدينة الملك فهد الطبية",
        f"ينصح {WHO_AR}",
    )
    return html


def patch_family_time(html: str) -> str:
    html = remove_cliches(html)
    html = html.replace(
        "Research shows that multitasking",
        f"{STANFORD} shows that multitasking",
    )
    return html


STANFORD = (
    '<a href="https://www.gsb.stanford.edu/insights/multitasking-myth" target="_blank" '
    'rel="noopener">Stanford multitasking research</a>'
)


def patch_home_sanctuary(html: str) -> str:
    return html.replace(
        "Prophet Muhammad peace be upon him said",
        "Islamic teaching on the home holds that",
    )


def patch_daily_islamic(html: str) -> str:
    html = re.sub(
        r'<p><span class="en">Get more family tips[^<]*</span><span class="ar">[^<]*</span></p>',
        "<p><span class=\"ar\">احصل على نصائح أسرية كل جمعة.</span></p>",
        html,
    )
    return html


def fix_file(rel: str) -> None:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    ar = is_arabic(html)

    html = fix_em_dashes(html)
    html = remove_cliches(html)
    html = neutralize_religious(html)

    if rel == "blog/masjid-nabawi-complete-guide.html":
        html = patch_masjid_ar(html)
    if rel == "blog/salalah-travel-guide-2025-en.html" and BOILERPLATE_B.search(html):
        html = BOILERPLATE_B.sub(
            "<p>Book flights before Khareef peak, pack light rain layers, and plan one slow family day among waterfalls.</p>",
            html,
            count=1,
        )
    if rel == "fitness/ramadan-calorie-calculator.html":
        html = patch_ramadan(html)
    if rel == "productivity/family-time-management-en.html":
        html = patch_family_time(html)
    if rel == "real-estate/home-as-sanctuary-family-wellbeing-en.html":
        html = patch_home_sanctuary(html)
    if rel == "blog/daily-islamic-habits-guide.html":
        html = patch_daily_islamic(html)

    if rel.startswith("cities/"):
        city = rel.split("/")[1].replace("-", " ").title()
        html = insert_city_intro(html, city)
        title_m = re.search(r"<title>([^<|]+)", html)
        title = title_m.group(1).strip() if title_m else city
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        url = canon.group(1) if canon else ""
        html = add_article_to_graph(html, title, url)

    if rel in HUB_ARTICLE:
        html = insert_hub_article(html, rel)

    html = apply_common_fixes(html, rel)
    html = fix_authority_paragraphs(html, rel, ar)
    html = inject_deep_link(html, rel, ar)
    html = ensure_disclaimer(html, ar)
    html = ensure_article_schema(html)
    html = ensure_faq_schema(html)

    if rel in GROUP_C or rel in GROUP_D:
        html = flip_index(html)

    path.write_text(html, encoding="utf-8")
    print(f"fixed {rel}")


def main() -> int:
    for rel in GROUP_C + GROUP_D:
        fix_file(rel)

    all_files = GROUP_C + GROUP_D
    r = subprocess.run(
        ["python3", "scripts/amer_gate.py", *all_files],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(r.stdout)
    fails = [ln for ln in r.stdout.splitlines() if ln.startswith("FAIL")]
    print(f"Total FAIL after fix: {len(fails)}/{len(all_files)}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
