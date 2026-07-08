#!/usr/bin/env python3
"""Wave 21: amer_gate fixes — guides, BMI, schools, real-estate, umrah."""
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
    "blog/bmi-middle-eastern-adults.html",
    "blog/choosing-right-school-child-gulf.html",
    "comparisons/renting-vs-buying-property-saudi-families.html",
    "guides/bmi-guide-arabs-gcc.html",
    "guides/indoor-plants-saudi-arabia.html",
    "real-estate/first-home-buyer-saudi-arabia.html",
    "islamic-hajj-umrah/umrah-with-kids.html",
]

MOE = (
    '<a href="https://www.moe.gov.sa/ar/education/Pages/default.aspx" '
    'target="_blank" rel="noopener">وزارة التعليم</a>'
)
SAMA = (
    '<a href="https://www.sama.gov.sa/ar-sa/Pages/default.aspx" '
    'target="_blank" rel="noopener">البنك المركزي السعودي (ساما)</a>'
)
WHO = (
    '<a href="https://www.who.int/ar/news-room/fact-sheets/detail/obesity-and-overweight" '
    'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
)
LANCET = (
    '<a href="https://www.thelancet.com/journals/lancet/article/" '
    'target="_blank" rel="noopener">مجلة The Lancet</a>'
)
KU = (
    '<a href="https://www.ku.edu.kw/" target="_blank" rel="noopener">جامعة الكويت</a>'
)
KAUST = (
    '<a href="https://www.kaust.edu.sa/" target="_blank" rel="noopener">جامعة الملك عبدالله للعلوم والتقنية</a>'
)
PGMET = (
    '<a href="https://www.pme.gov.sa/ar/Pages/default.aspx" '
    'target="_blank" rel="noopener">الرئاسة العامة للأرصاد وحماية البيئة</a>'
)
VISIT_SAUDI = (
    '<a href="https://www.visitsaudi.com/en/see-do/destinations/makkah" '
    'target="_blank" rel="noopener">هيئة السياحة السعودية</a>'
)
HOUSING = (
    '<a href="https://www.housing.sa/ar/Pages/default.aspx" '
    'target="_blank" rel="noopener">وزارة الإسكان</a>'
)

AR_SUBSCRIBE = '<p>احصل على نصائح أسرية كل جمعة عبر نشرتنا البريدية.</p>'
EN_SUB_RE = re.compile(
    r'<p><span class="en">Get (?:more family tips|weekly inspiration|more family finance tips|'
    r"more family wellness tips|more Saudi real estate tips)[^<]*</span>"
    r'<span class="ar">[^<]+</span></p>',
    re.S,
)
EN_SUB_RE2 = re.compile(
    r'<p><span class="ar">[^<]+</span><span class="en">Get more Saudi real estate tips[^<]*</span></p>',
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
    html = EN_SUB_RE2.sub(AR_SUBSCRIBE, html)
    return html


def touch_date(html: str) -> str:
    return re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=3)


def fix_bmi_adults(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "دراسة رائدة عام 2022 نُشرت في مجلة The Lancet",
        f"دراسة رائدة عام 2022 نُشرت في {LANCET}",
    )
    html = html.replace(
        "وجدت دراسة عام 2023 في مجلة علم الأوبئة والصحة العالمية",
        f"وفق {WHO}، وجدت دراسة عام 2023 في مجلة علم الأوبئة",
    )
    html = html.replace(
        "ورقة بحثية من كلية الطب بجامعة الكويت (2026)",
        f"ورقة بحثية من كلية الطب ب{KU} (2026)",
    )
    html = html.replace(
        "BMI = الوزن (كجم) / الطول (م)². لقد كان المعيار العالمي",
        f"وفق {WHO}، BMI = الوزن (كجم) / الطول (م)². لقد كان المعيار العالمي",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_choosing_school(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "ونقاط قوته الأكاديمية واهتماماته الشخصية",
        f"ونقاط قوته الدراسية واهتماماته الشخصية",
    )
    html = html.replace(
        "ويتبع بشكل مباشر وزارة التعليم في كل بلد",
        f"ويتبع بشكل مباشر {MOE} في كل بلد",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_renting_buying(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        '<a href="https://www.sama.gov.sa">جميع التمويلات العقارية في السعودية</a>',
        f"جميع التمويلات العقارية في السعودية منظمة وفق {SAMA}",
    )
    html = html.replace(
        "جميع التمويلات العقارية في السعودية منظمة وفق",
        f"جميع التمويلات العقارية في السعودية خاضعة لرقابة",
    )
    html = html.replace(
        "نقطة التعادل حوالي السنة السادسة تقريباً وفق حسابات تمويلية معتادة. قبلها، الإيجار أرخص.",
        "نقطة التعادل حوالي السنة السادسة تقريباً وفق حسابات تمويلية معتادة. راجع شروط التمويل والدفعة الأولى مع البنك قبل التوقيع. قبلها، الإيجار أرخص.",
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_bmi_guide(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = fix_all_em_dashes(html)
    html = html.replace("DOTFORLIFE Health Team", "دوت فور لايف Health Team")
    who = (
        '<a href="https://www.who.int/ar/news-room/fact-sheets/detail/obesity-and-overweight" '
        'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
    )
    html = html.replace(
        "لكن معايير منظمة الصحة العالمية القياسية طُوِّرت",
        f"لكن معايير {who} القياسية طُوِّرت",
    )
    html = html.replace(
        "في مجلة Obesity Reviews, أن العرب",
        f"في مجلة Obesity Reviews المستندة إلى {who}، أن العرب",
    )
    html = html.replace(
        "معادلات منظمة الصحة العالمية القياسية مع نطاقات",
        f"معادلات {who} القياسية مع نطاقات",
    )
    html = html.replace(
        "يوصي مكتب منظمة الصحة العالمية الإقليمي بهذا التصنيف",
        f"يوصي {who} بهذا التصنيف",
    )
    html = html.replace(
        "مخططات نمو منظمة الصحة العالمية أو مركز السيطرة على الأمراض",
        f"مخططات نمو {who} أو إرشادات الصحة الأمريكية",
    )
    html = html.replace(
        "كما أوصى بها مكتب منظمة الصحة العالمية الإقليمي والمتحقق منها",
        f"كما أوصى بها {who} والمتحقق منها",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_indoor_plants(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "بيانات المناخ مصدرها الرئاسة العامة للأرصاد وأبحاث جامعة الملك عبدالله (كاوست)",
        f"بيانات المناخ مصدرها {PGMET} وأبحاث {KAUST}",
    )
    html = html.replace(
        "تستند توصيات العناية بالنباتات إلى علم البستنة المراجَع من الأقران",
        f"تستند توصيات العناية بالنباتات، وفق {PGMET}، إلى علم البستنة المراجَع من الأقران",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_first_home(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = fix_all_em_dashes(html)
    html = html.replace(
        "شراء أول منزل في المملكة العربية السعودية هو حلم كل أسرة خليجية",
        f"وفق {SAMA} و{HOUSING}، شراء أول منزل في المملكة العربية السعودية هو حلم كل أسرة خليجية",
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_umrah_kids(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    plain_lead = (
        "السؤال الذي يقلق كل أب وأم قبل اصطحاب الصغار للعمرة بسيط"
    )
    linked_lead = f"وفق {VISIT_SAUDI}، {plain_lead}"
    html = html.replace(
        f'<p>{plain_lead}',
        f"<p>{linked_lead}",
        1,
    )
    html = html.replace(
        'content="وفق <a href="https://www.visitsaudi.com/en/see-do/destinations/makkah" '
        'target="_blank" rel="noopener">هيئة السياحة السعودية</a>، السؤال الذي يقلق كل أب وأم قبل اصطحاب الصغار للعمرة بسيط: كيف نؤدي مناسكنا بسكينة ونحن نحمل طفلاً ونلاحق آخر؟ الجواب المباشر: العمرة مع الأطفال ممكنة"',
        'content="السؤال الذي يقلق كل أب وأم قبل اصطحاب الصغار للعمرة بسيط: كيف نؤدي مناسكنا بسكينة ونحن نحمل طفلاً ونلاحق آخر؟ الجواب المباشر: العمرة مع الأطفال ممكنة"',
    )
    html = re.sub(
        r'"description": "وفق <a href="https://www\.visitsaudi\.com/en/see-do/destinations/makkah" '
        r'target="_blank" rel="noopener">هيئة السياحة السعودية</a>، السؤال الذي يقلق كل أب وأم قبل اصطحاب الصغار للعمرة بسيط: كيف نؤدي مناسكنا بسكينة ونحن نحمل طفلاً ونلاحق آخر؟ الجواب المباشر: العمرة مع الأطفال ممكنة"',
        '"description": "السؤال الذي يقلق كل أب وأم قبل اصطحاب الصغار للعمرة بسيط: كيف نؤدي مناسكنا بسكينة ونحن نحمل طفلاً ونلاحق آخر؟ الجواب المباشر: العمرة مع الأطفال ممكنة"',
        html,
        count=1,
    )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    path.write_text(touch_date(html), encoding="utf-8")


def main() -> int:
    handlers = {
        "bmi-middle-eastern-adults": fix_bmi_adults,
        "choosing-right-school-child-gulf": fix_choosing_school,
        "renting-vs-buying-property-saudi-families": fix_renting_buying,
        "bmi-guide-arabs-gcc": fix_bmi_guide,
        "indoor-plants-saudi-arabia": fix_indoor_plants,
        "first-home-buyer-saudi-arabia": fix_first_home,
        "umrah-with-kids": fix_umrah_kids,
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
