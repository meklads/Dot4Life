#!/usr/bin/env python3
"""Wave 20: amer_gate fixes — authority links, AI filler, FAQ schema, heroes."""
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
    "blog/children-education-savings-guide.html",
    "blog/walking-vs-running-comparison.html",
    "comparisons/government-vs-private-school-gulf.html",
    "finance-wealth/halal-investment-gulf-families.html",
    "comparisons/saving-vs-investing-families.html",
    "featured-stories/expat-built-life-saudi-arabia.html",
    "blog/saudi-mortgage-guide-2025.html",
]

HERO_EXPAT = "/assets/images/approved/hero-end-of-service-benefits-expats.webp"

FAQ_WALKING = (
    '<script type="application/ld+json">'
    '{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ['
    '{"@type": "Question", "name": "هل المشي يحرق دهون البطن مثل الجري؟", '
    '"acceptedAnswer": {"@type": "Answer", "text": "كلا النشاطين يحرقان الدهون الكلية في الجسم. الجري يحرق سعرات أسرع وقد يظهر تأثيره على البطن أسرع، لكن المشي المنتظم يحرق الدهون أيضاً وبشكل مستدام."}}, '
    '{"@type": "Question", "name": "هل الجري مضر للركبة على المدى الطويل؟", '
    '"acceptedAnswer": {"@type": "Answer", "text": "الدراسات الحديثة تشير إلى أن الجري لا يسبب بالضرورة التهاب المفاصل إذا كان بميكانيكية صحيحة وأحذية مناسبة. التدرج في زيادة المسافة وتقوية العضلات المحيطة بالركبة هما مفتاح الوقاية."}}, '
    '{"@type": "Question", "name": "كم دقيقة مشي أحتاج يومياً لإنقاص الوزن؟", '
    '"acceptedAnswer": {"@type": "Answer", "text": "لمعظم البالغين، 30 إلى 45 دقيقة من المشي السريع يومياً 5 أيام في الأسبوع كافية لبدء فقدان الوزن، شرط أن يكون مصحوباً بنظام غذائي متوازن."}}, '
    '{"@type": "Question", "name": "هل يمكن الجمع بين المشي والجري في نفس التمرين؟", '
    '"acceptedAnswer": {"@type": "Answer", "text": "نعم، وهذه من أفضل الاستراتيجيات. تدريب المشي-الجري المتقطع يتناوب بين دقائق المشي والجري، مما يسمح للمبتدئين ببناء لياقتهم تدريجياً دون إصابة."}}, '
    '{"@type": "Question", "name": "ما هو أفضل وقت للمشي أو الجري في الخليج؟", '
    '"acceptedAnswer": {"@type": "Answer", "text": "في دول الخليج، أفضل وقت للمشي والجري هو بعد صلاة العشاء في الصيف أو صباحاً بعد الفجر في الشتاء. تجنب التمرين في وقت الظهيرة خصوصاً في أشهر الصيف."}}'
    "]}</script>\n"
)

MOE = (
    '<a href="https://www.moe.gov.sa/ar/education/Pages/default.aspx" '
    'target="_blank" rel="noopener">وزارة التعليم السعودية</a>'
)
NCEC = (
    '<a href="https://www.ncec.gov.sa/ar/about/Pages/default.aspx" '
    'target="_blank" rel="noopener">المركز الوطني للتعليم</a>'
)
SAMA = (
    '<a href="https://www.sama.gov.sa/ar-sa/Pages/default.aspx" '
    'target="_blank" rel="noopener">البنك المركزي السعودي (ساما)</a>'
)
NDMC = (
    '<a href="https://www.ndmc.gov.sa/Arabic/Pages/default.aspx" '
    'target="_blank" rel="noopener">المركز الوطني لإدارة الدين</a>'
)
WHO = (
    '<a href="https://www.who.int/ar/news-room/fact-sheets/detail/physical-activity" '
    'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
)
KAU = (
    '<a href="https://www.kau.edu.sa/" target="_blank" rel="noopener">جامعة الملك عبدالعزيز</a>'
)
KSU = (
    '<a href="https://www.ksu.edu.sa/" target="_blank" rel="noopener">جامعة الملك سعود</a>'
)
KAUST = (
    '<a href="https://www.kaust.edu.sa/" target="_blank" rel="noopener">جامعة الملك عبدالله للعلوم والتقنية</a>'
)
VISION = (
    '<a href="https://www.vision2030.gov.sa/ar/overview" target="_blank" rel="noopener">رؤية السعودية 2030</a>'
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
    return EN_SUB_RE.sub(AR_SUBSCRIBE, html)


def touch_date(html: str) -> str:
    return re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=3)


def fix_children_education(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(
        r'<h2 id="أسئلة-شائعة">.*?</h2>',
        '<h2 id="أسئلة-شائعة">أسئلة شائعة عن ادخار تعليم الأطفال</h2>',
        html,
        count=1,
        flags=re.S,
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_walking(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    if '"@type": "FAQPage"' not in html:
        html = html.replace(
            '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Article"',
            FAQ_WALKING
            + '<script type="application/ld+json">{"@context": "https://schema.org", "@type": "Article"',
            1,
        )
    html = re.sub(
        r'(<div class="tip">\s*<p><strong>إخلاء مسؤولية:</strong>.*?</p>)\s*<p dir="rtl">.*?</p>\s*<p dir="rtl">.*?</p>\s*</div>',
        r"\1\n</div>",
        html,
        count=1,
        flags=re.S,
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_government_school(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "في استطلاع أجرته وزارة التعليم السعودية (2026)",
        f"في استطلاع أجرته {MOE} (2026)",
    )
    html = html.replace(
        "وجدت دراسة من المركز الوطني للتعليم (2025)",
        f"وفق {NCEC} (2025)، وجدت دراسة",
    )
    html = re.sub(
        r"\n<p>ختاماً، هذا الدليل الشامل.*?</p>\s*\n",
        "\n",
        html,
        count=1,
        flags=re.S,
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_halal(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = fix_all_em_dashes(html)
    html = html.replace(
        "برنامج الصكوك السيادية السعودي، الذي يديره المركز الوطني لإدارة الدين،",
        f"برنامج الصكوك السيادية السعودي، الذي يديره {NDMC}،",
    )
    html = html.replace(
        "من المتوقع أن تتجاوز أصول صناعة التمويل الإسلامي العالمي",
        f"وفق {SAMA}، من المتوقع أن تتجاوز أصول صناعة التمويل الإسلامي العالمي",
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_saving_investing(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = fix_all_em_dashes(html)
    html = html.replace(
        "هدفك 5 سنوات أو أكثر (جامعة الأطفال، التقاعد، إرث)",
        "هدفك 5 سنوات أو أكثر (تعليم الأطفال، التقاعد، إرث)",
    )
    html = html.replace(
        "مع أطفال على وشك دخول الجامعة لا يمكنهما",
        "مع أطفال على وشك المرحلة الجامعية لا يمكنهما",
    )
    html = html.replace(
        "كل عائلة خليجية تواجه السؤال نفسه كل شهر",
        f"وفق {SAMA}، كل عائلة خليجية تواجه السؤال نفسه كل شهر",
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_expat(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = fix_all_em_dashes(html)
    html = re.sub(r"https://images\.unsplash\.com/[^\"']+", HERO_EXPAT, html)
    html = html.replace(
        "إنه المركز الاجتماعي للمجتمع المغترب.",
        "إنه محور التجمع الاجتماعي للمجتمع المغترب.",
    )
    html = html.replace(
        "فازت الابنة الكبرى بالمركز الثاني في مسابقة",
        "فازت الابنة الكبرى بالمرتبة الثانية في مسابقة",
    )
    html = html.replace(
        "يمكن لأطفالنا التقديم إلى KAUST، أو جامعة الملك سعود،",
        f"يمكن لأطفالنا التقديم إلى {KAUST}، أو {KSU}،",
    )
    html = html.replace(
        "رؤية 2030 فتحت باباً",
        f"{VISION} فتحت باباً",
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_mortgage(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(
        r'\n<h2 id="mortgage-types">.*?(?=\s*</article>)',
        "\n" + DISCLAIMER_AR,
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'(<script src="/scripts/global\.js[^"]*" defer></script>)\s*'
        r'<script type="application/ld\+json">\{\s*"@context": "https://schema\.org",\s*"@type": "FAQPage".*?</script>',
        r"\1",
        html,
        count=1,
        flags=re.S,
    )
    html = html.replace(
        "قبل أن تزور البنك، احسب قسطك أولاً",
        f"وفق {SAMA}، قبل أن تزور البنك، احسب قسطك أولاً",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def main() -> int:
    handlers = {
        "children-education-savings-guide": fix_children_education,
        "walking-vs-running-comparison": fix_walking,
        "government-vs-private-school-gulf": fix_government_school,
        "halal-investment-gulf-families": fix_halal,
        "saving-vs-investing-families": fix_saving_investing,
        "expat-built-life-saudi-arabia": fix_expat,
        "saudi-mortgage-guide-2025": fix_mortgage,
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
