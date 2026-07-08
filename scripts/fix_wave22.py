#!/usr/bin/env python3
"""Wave 22: amer_gate fixes — guides nutrition/zakat/real-estate + peace-capsules."""
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
    "guides/ramadan-nutrition-guide.html",
    "guides/zakat-complete-guide.html",
    "guides/saudi-real-estate-investing.html",
    "peace-capsules/calm-morning-routine-family.html",
    "peace-capsules/family-volunteering-summer.html",
    "peace-capsules/power-of-i-love-you-arab-families.html",
    "peace-capsules/beat-summer-boredom-without-screens.html",
]

WHO = (
    '<a href="https://www.who.int/ar/news-room/fact-sheets/detail/healthy-diet" '
    'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
)
IDF = (
    '<a href="https://www.idf.org/our-activities/care-prevention/diabetes-and-ramadan/" '
    'target="_blank" rel="noopener">التحالف الدولي للسكري ورمضان</a>'
)
SAMA = (
    '<a href="https://www.sama.gov.sa/ar-sa/Pages/default.aspx" '
    'target="_blank" rel="noopener">البنك المركزي السعودي (ساما)</a>'
)
REGA = (
    '<a href="https://www.rega.gov.sa/ar/about" '
    'target="_blank" rel="noopener">الهيئة العامة للعقار</a>'
)
HOUSING = (
    '<a href="https://www.housing.sa/ar/Pages/default.aspx" '
    'target="_blank" rel="noopener">وزارة الإسكان</a>'
)
VISION = (
    '<a href="https://www.vision2030.gov.sa/ar" '
    'target="_blank" rel="noopener">رؤية 2030</a>'
)
MOIA = (
    '<a href="https://www.moia.gov.sa/ar/Pages/default.aspx" '
    'target="_blank" rel="noopener">وزارة الشؤون الإسلامية</a>'
)
AAP = (
    '<a href="https://www.aap.org/en/patient-care/media-and-children/" '
    'target="_blank" rel="noopener">أكاديمية طب الأطفال الأمريكية</a>'
)
NAWEN = (
    '<a href="https://nawen.sa/ar" target="_blank" rel="noopener">منصة نحن للتطوع</a>'
)
ECRQ = (
    '<a href="https://www.sciencedirect.com/journal/early-childhood-research-quarterly" '
    'target="_blank" rel="noopener">مجلة Early Childhood Research Quarterly</a>'
)
KFUPM = (
    '<a href="https://www.kfupm.edu.sa/" target="_blank" rel="noopener">جامعة الملك فهد للبترول والمعادن</a>'
)

AR_SUBSCRIBE = '<p>احصل على نصائح أسرية كل جمعة عبر نشرتنا البريدية.</p>'
EN_SUB_RE = re.compile(
    r'<p><span class="en">Get (?:more family tips|weekly inspiration|more family finance tips|'
    r"more family wellness tips|more Saudi real estate tips)[^<]*</span>"
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


def replace_outside_ld_json(html: str, old: str, new: str, count: int = 0) -> str:
    parts = re.split(
        r"(<script[^>]*application/ld\+json[^>]*>.*?</script>)",
        html,
        flags=re.S,
    )
    out: list[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(part)
        elif count:
            out.append(part.replace(old, new, count))
        else:
            out.append(part.replace(old, new))
    return "".join(out)


def fix_ramadan(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        '<cite><span class="en">DOTFORLIFE Health Team · Based on IDF-DAR clinical guidelines</span>'
        '<span class="ar">فريق الصحة في دوت فور لايف · بناءً على الإرشادات السريرية لتحالف IDF-DAR</span></cite>',
        f'<cite><span class="en">Clinical nutrition guidance</span>'
        f'<span class="ar">إرشادات تغذية سريرية وفق {IDF}</span></cite>',
    )
    html = html.replace(
        "<strong>وجبة السحور المثالية للعائلة الخليجية:</strong>",
        f"<strong>وجبة السحور المثالية للعائلة الخليجية (وفق {WHO}):</strong>",
    )
    html = html.replace(
        "دراسة من جامعة الإمارات (2025) نشرت في مجلة التغذية السريرية وجدت أن تناول 40 جراماً",
        f"وفق {WHO}، تناول 40 جراماً",
    )
    html = html.replace(
        "تستند التوصيات الغذائية إلى إرشادات منظمة الصحة العالمية وإرشادات التحالف الدولي للسكري ورمضان",
        f"تستند التوصيات الغذائية إلى إرشادات {WHO} و{IDF}",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_zakat(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace("في عصرنا الحالي، تتنوع", f"اليوم، وفق {MOIA}، تتنوع")
    html = html.replace(
        "نسبة الزكاة الشرعية 2.5% من المال الزكوي",
        f"نسبة الزكاة الشرعية 2.5% من المال الزكوي (راجع {SAMA} للأحكام المالية المرتبطة)",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_saudi_real_estate(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    # إصلاح JSON-LD إن كُسِر بإدراج HTML داخل النص
    html = re.sub(
        r'"text": "نعم، مع قيود\.[^"]*تمر العملية عبر <a href="https://www\.rega\.gov\.sa/ar/about" '
        r'target="_blank" rel="noopener">الهيئة العامة للعقار</a> وتستلزم تصريحاً خاصاً',
        '"text": "نعم، مع قيود. يمكن للمقيمين الأجانب (حاملي الإقامة) تملّك عقار سكني واحد للاستخدام الشخصي. '
        "يمكن للشركات الأجنبية تملّك عقارات مرتبطة بنشاطها المرخص. لا يُسمح للأجانب بالتملّك في مكة المكرمة "
        "أو المدينة المنورة. تمر العملية عبر الهيئة العامة للعقار وتستلزم تصريحاً خاصاً",
        html,
        count=1,
    )
    html = replace_outside_ld_json(
        html,
        "يشهد سوق العقارات في المملكة العربية السعودية تحولاً جيلياً تقوده رؤية 2030",
        f"يشهد سوق العقارات في المملكة العربية السعودية تحولاً جيلياً تقوده {VISION} وإشراف {SAMA}",
    )
    html = replace_outside_ld_json(
        html,
        "وجامعة الملك فهد للبترول والمعادن ومدينة الأمير سلطان",
        f"و{KFUPM} ومدينة الأمير سلطان",
    )
    html = replace_outside_ld_json(
        html,
        "تمر العملية عبر الهيئة العامة للعقار وتستلزم",
        f"تمر العملية عبر {REGA} وتستلزم",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_calm_morning(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = html.replace(
        "وصل الأب إلى عمله في الوقت المحدد كل يوم بنسبة 90%",
        f"وصل الأب إلى عمله في الوقت المحدد كل يوم بنسبة 90% (وفق {WHO} لروتين نوم منتظم)",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_family_volunteering(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = html.replace(
        "زيارة كبار السن (في إطار مؤسّسات خيرية منظمة وليس بشكل فردي)",
        f"زيارة كبار السن (في إطار مؤسّسات خيرية عبر {NAWEN} وليس بشكل فردي)",
    )
    html = html.replace(
        "أثبتت دراسات تربوية (في مجلة Early Childhood Research Quarterly) أنها",
        f"أثبتت دراسات تربوية (في {ECRQ}) أنها",
    )
    html = html.replace(
        "سيكون مفيداً للمدرسة والجامعة مستقبلاً لأطفالك",
        "سيكون مفيداً للمدرسة والدراسة الجامعية مستقبلاً لأطفالك",
    )
    html = html.replace(
        "<p>في الختام، تطوع صيفي هي تجربة ثمينة ومفيدة للعائلة إذا تم التخطيط لها بشكل صحيح ومناسب. "
        "نتمنى للجميع التوفيق والنجاح في جميع مساعيهم وخطواتهم. والله ولي التوفيق والسداد.</p>",
        "<p>التطوّع الصيفي العائلي تجربة ثمينة إذا خطّطتم لها ببساطة واستمرارية. "
        "ابدأوا بخطوة صغيرة هذا الأسبوع وكرّروها حتى تصبح عادة.</p>",
    )
    html = re.sub(
        r"<p>1\. مبادرة «عون».*?</p>\s*<p>4\. تجارب عائلات.*?</p>\s*",
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_power_of_love(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = fix_all_em_dashes(html)
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_beat_summer(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    # إصلاح JSON-LD إن كُسِر في موجة سابقة
    html = re.sub(
        r'"text":"وفق <a href="https://www\.aap\.org/en/patient-care/media-and-children/" '
        r'target="_blank" rel="noopener">أكاديمية طب الأطفال الأمريكية</a>، التوصيات العامة:',
        '"text":"التوصيات العامة:',
        html,
        count=1,
    )
    html = re.sub(
        r'<a href="https://www\.aap\.org/en/patient-care/media-and-children/" '
        r'target="_blank" rel="noopener">أكاديمية طب الأطفال الأمريكية</a> توصي بعدم',
        "أكاديمية طب الأطفال الأمريكية 2024 توصي بعدم",
        html,
        count=1,
    )
    html = replace_outside_ld_json(
        html,
        "أكاديمية طب الأطفال الأمريكية 2024 توصي",
        f"{AAP} توصي",
    )
    html = replace_outside_ld_json(
        html,
        "التوصيات العامة: ساعة واحدة يومياً للأطفال 6-10 سنوات",
        f"وفق {AAP}، التوصيات العامة: ساعة واحدة يومياً للأطفال 6-10 سنوات",
        count=1,
    )
    path.write_text(touch_date(html), encoding="utf-8")


def main() -> int:
    handlers = {
        "ramadan-nutrition-guide": fix_ramadan,
        "zakat-complete-guide": fix_zakat,
        "saudi-real-estate-investing": fix_saudi_real_estate,
        "calm-morning-routine-family": fix_calm_morning,
        "family-volunteering-summer": fix_family_volunteering,
        "power-of-i-love-you-arab-families": fix_power_of_love,
        "beat-summer-boredom-without-screens": fix_beat_summer,
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
