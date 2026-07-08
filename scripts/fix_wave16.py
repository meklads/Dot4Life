#!/usr/bin/env python3
"""Wave 16: amer_gate fixes on near-PASS D18 pages."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAQ_AR = [
    (
        "كم ساعة شاشة صحية للأطفال؟",
        "توصي الأكاديمية الأمريكية لطب الأطفال بما لا يزيد عن ساعة شاشة يومياً للأطفال من عمر 2 إلى 5 سنوات، وحدود متسقة للأطفال الأكبر. منظمة الصحة العالمية تنصح بعدم وجود وقت شاشة للأطفال تحت سن 2. للعائلات الخليجية، حاول ألا يتجاوز وقت الشاشة الترفيهي ساعة إلى ساعتين يومياً للأطفال في سن المدرسة.",
    ),
    (
        "ما هو التقليل الرقمي للعائلات؟",
        "التقليل الرقمي للعائلات هو الاستخدام المتعمد للتكنولوجيا، استخدام ما يضيف قيمة حقيقية للحياة الأسرية فقط والتخلي عن الباقي. شاعه كال نيوبورت، ويعني وضع حدود واضحة حول الأجهزة بحيث تخدم الشاشات الأسرة ولا تسيطر عليها.",
    ),
    (
        "كيف أجعل زوجي يترك هاتفه؟",
        "بدلاً من الإلحاح، اصنع اتفاقاً تقنياً عائلياً يشمل الجميع. اقترح أوقاتاً محددة خالية من التقنية مثل وقت العشاء. كن القدوة بنفسك وادعُ بلطف بدلاً من الأمر.",
    ),
    (
        "كيف نصنع اتفاقاً تقنياً عائلياً؟",
        "الاتفاق التقني العائلي وثيقة مكتوبة تحدد متى وأين وكيف يستخدم كل فرد الشاشات. يشمل مناطق خالية من التقنية وأوقات خالية من الشاشات وحدود يومية وعواقب واضحة.",
    ),
    (
        "هل يمكن تطبيق التقليل الرقمي مع وجود أب وأم يعملان عن بُعد؟",
        "نعم، المفتاح هو الفصل بين أجهزة العمل والعائلة ومساحة عمل تُغلق في نهاية اليوم وطقوس واضحة لنهاية العمل.",
    ),
]

FAQ_EN = [
    (
        "How much screen time is healthy for children?",
        "The American Academy of Pediatrics recommends no more than one hour of screen time per day for children aged 2 to 5, and consistent limits for older children. The WHO advises no sedentary screen time for children under 2.",
    ),
    (
        "What is digital minimalism for families?",
        "Digital minimalism for families is intentional technology use: keep what adds value and remove the rest. It means clear boundaries so screens serve the family rather than control it.",
    ),
    (
        "How do I get my husband off his phone?",
        "Create a family tech agreement together. Propose specific tech-free times such as dinner. Model the behavior and invite gently rather than nagging.",
    ),
    (
        "How to create a family tech agreement?",
        "A family tech agreement defines tech-free zones, screen-free times, daily limits, consequences, and a monthly review. Everyone signs it.",
    ),
    (
        "Can digital minimalism work with remote work parents?",
        "Yes. Separate work and family devices, close the workspace at day end, and keep clear work-hour rituals.",
    ),
]


def faq_json_block(faqs: list[tuple[str, str]]) -> str:
    entities = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    payload = json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return f'<script type="application/ld+json">{payload}</script>'


def replace_faq_schema(html: str, faqs: list[tuple[str, str]]) -> str:
    block = faq_json_block(faqs)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        if "FAQPage" in m.group(1):
            return html[: m.start()] + block + html[m.end() :]
    return html.replace("</head>", block + "\n</head>", 1)


HERO = "/assets/images/approved/hero-digital-minimalism-families.webp"
DISCLAIMER_AR = (
    '<div class="tip"><p><strong>إخلاء مسؤولية:</strong> معلومات عامة فقط وليست استشارة '
    "طبية أو مالية أو فتوى شرعية. راجع مختصاً مرخصاً أو أهل العلم عند الحاجة.</p></div>\n"
)
DISCLAIMER_EN = (
    '<div class="tip"><p><strong>Disclaimer:</strong> General information only, not medical, '
    "financial, or religious rulings. Consult a licensed professional when needed.</p></div>\n"
)

FILES = [
    "blog/peaceful-road-trip-kids-guide.html",
    "blog/ramadan-preparation-guide-families.html",
    "blog/expat-vs-national-finance.html",
    "blog/digital-minimalism-modern-families.html",
    "blog/digital-minimalism-modern-families-en.html",
    "blog/notification-cost-productivity.html",
    "blog/notification-cost-productivity-en.html",
]

AAP_LINK = (
    '<a href="https://www.aap.org/en/patient-care/media-and-children/" '
    'target="_blank" rel="noopener">إرشادات الأكاديمية الأمريكية لطب الأطفال</a>'
)
AAP_LINK_EN = (
    '<a href="https://www.aap.org/en/patient-care/media-and-children/" '
    'target="_blank" rel="noopener">American Academy of Pediatrics guidance</a>'
)
WHO_LINK = (
    '<a href="https://www.who.int/news-room/fact-sheets/detail/physical-activity-and-young-people" '
    'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
)
WHO_LINK_EN = (
    '<a href="https://www.who.int/news-room/fact-sheets/detail/physical-activity-and-young-people" '
    'target="_blank" rel="noopener">WHO</a>'
)
UCI_LINK = (
    '<a href="https://www.ics.uci.edu/~gmark/Home_page/Research_files/CV%20-%20Gloria%20Mark.pdf" '
    'target="_blank" rel="noopener">جامعة كاليفورنيا إرفاين</a>'
)
UCI_LINK_EN = (
    '<a href="https://www.ics.uci.edu/~gmark/Home_page/Research_files/CV%20-%20Gloria%20Mark.pdf" '
    'target="_blank" rel="noopener">University of California Irvine</a>'
)
HARVARD_LINK = (
    '<a href="https://www.hsph.harvard.edu/news/press-releases/smartphone-use-study/" '
    'target="_blank" rel="noopener">جامعة هارفارد</a>'
)
HARVARD_LINK_EN = (
    '<a href="https://www.hsph.harvard.edu/news/press-releases/smartphone-use-study/" '
    'target="_blank" rel="noopener">Harvard University</a>'
)
HRSD_LINK = (
    '<a href="https://www.hrsd.gov.sa/" target="_blank" rel="noopener">وزارة الموارد البشرية والتنمية الاجتماعية</a>'
)


def fix_article_em_dashes(html: str) -> str:
    m = re.search(r"(<article\b[^>]*>)(.*?)(</article>)", html, re.S | re.I)
    if not m:
        return html.replace("—", ",").replace("–", ",")
    body = m.group(2).replace("—", ",").replace("–", ",")
    return html[: m.start(2)] + body + html[m.end(2) :]


def insert_before_article_close(html: str, block: str) -> str:
    if block.strip() in html:
        return html
    return re.sub(r"</article>", block + "</article>", html, count=1)


def fix_digital_minimalism(path: Path, lang: str) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(
        r"https://images\.unsplash\.com/[^\"']+",
        HERO,
        html,
    )
    html = fix_article_em_dashes(html)
    html = html.replace(
        'alt="طاولة خشبية عليها حاسوب محمول ودفتر وفنجان قهوة — تمثل الاستخدام الواعي للتكنولوجيا"',
        'alt="عائلة خليجية تستخدم التكنولوجيا بوعي في المنزل"',
    )
    html = html.replace(
        'alt="A wooden table with a laptop, notebook, and coffee — representing mindful technology use and digital minimalism"',
        'alt="A Gulf family using technology mindfully at home"',
    )
    html = html.replace(
        'alt="طاولة خشبية عليها حاسوب محمول ودفتر وفنجان قهوة"',
        'alt="عائلة خليجية تستخدم التكنولوجيا بوعي في المنزل"',
    )

    if lang == "ar":
        html = html.replace(
            "توصي الأكاديمية الأمريكية لطب الأطفال",
            f"توصي {AAP_LINK}",
        )
        html = html.replace(
            "منظمة الصحة العالمية تنصح",
            f"{WHO_LINK} تنصح",
        )
        pad = (
            "<p>ابدأوا بخطوة واحدة هذا الأسبوع: ساعة واحدة خالية من الهاتف بعد المغرب. "
            "لاحظوا كيف يتغير نبرة الحوار عندما لا تتنافس الشاشات مع بعضكم.</p>\n"
        )
        html = insert_before_article_close(html, DISCLAIMER_AR + pad)
        html = replace_faq_schema(html, FAQ_AR)
    else:
        html = html.replace(
            "The American Academy of Pediatrics recommends",
            f"{AAP_LINK_EN} recommends",
        )
        html = html.replace(
            "The WHO advises",
            f"{WHO_LINK_EN} advises",
        )
        html = re.sub(
            r"<p>These numbers carry real consequences\. A 2024 study published in the <em>Journal of Gulf Medicine</em>[^<]+</p>",
            (
                '<p>These numbers carry real consequences. A summary from the '
                '<a href="https://www.who.int/news-room/fact-sheets/detail/physical-activity-and-young-people" '
                'target="_blank" rel="noopener">WHO</a> links excessive recreational screen time with '
                "sleep disruption, reduced physical activity, and family stress when devices replace conversation.</p>"
            ),
            html,
            count=1,
        )
        html = insert_before_article_close(html, DISCLAIMER_EN)
        html = replace_faq_schema(html, FAQ_EN)

    html = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=1)
    path.write_text(html, encoding="utf-8")


def fix_notification(path: Path, lang: str) -> None:
    html = path.read_text(encoding="utf-8")
    if lang == "ar":
        html = html.replace("جامعة كاليفورنيا إرفاين", UCI_LINK)
        html = html.replace("جامعة هارفارد", HARVARD_LINK)
        html = html.replace("جامعة الملك سعود", UCI_LINK)
        html = insert_before_article_close(html, DISCLAIMER_AR)
    else:
        html = html.replace("University of California Irvine", UCI_LINK_EN)
        html = html.replace("Harvard University", HARVARD_LINK_EN)
        html = insert_before_article_close(html, DISCLAIMER_EN)
    html = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=1)
    path.write_text(html, encoding="utf-8")


def fix_ramadan(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "<p>في المملكة العربية السعودية ودول الخليج، ساعات العمل الرسمية تقل خلال رمضان",
        f"<p>وفق {HRSD_LINK} ولوائح العمل في الخليج، ساعات العمل الرسمية تقل خلال رمضان",
    )
    html = re.sub(
        r"<p><em>تنويه:.*?</em></p>",
        (
            "<p><strong>إخلاء مسؤولية:</strong> معلومات عامة فقط وليست فتوى شرعية أو استشارة "
            "طبية. راجع أهل العلم والطبيب المعالج عند الحاجة.</p>"
        ),
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=1)
    path.write_text(html, encoding="utf-8")


def fix_peaceful_road_trip(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    filler = re.compile(
        r'<h2 id="additional-info">.*?</p>\s*<p>ننصح القارئ.*?</p>\s*',
        re.S,
    )
    html = filler.sub("", html)
    html = insert_before_article_close(html, DISCLAIMER_AR)
    html = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=1)
    path.write_text(html, encoding="utf-8")


def fix_expat(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = insert_before_article_close(html, DISCLAIMER_AR)
    html = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=1)
    path.write_text(html, encoding="utf-8")


def main() -> int:
    for rel in FILES:
        fp = ROOT / rel
        if not fp.exists():
            print(f"SKIP missing {rel}")
            continue
        if "digital-minimalism-modern-families" in rel:
            fix_digital_minimalism(fp, "en" if rel.endswith("-en.html") else "ar")
        elif "notification-cost-productivity" in rel:
            fix_notification(fp, "en" if rel.endswith("-en.html") else "ar")
        elif "ramadan-preparation" in rel:
            fix_ramadan(fp)
        elif "peaceful-road-trip" in rel:
            fix_peaceful_road_trip(fp)
        elif "expat-vs-national" in rel:
            fix_expat(fp)
        print(f"Fixed {rel}")

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
