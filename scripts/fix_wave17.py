#!/usr/bin/env python3
"""Wave 17: amer_gate fixes — authority false-positives, disclaimers, heroes."""
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
    "blog/stress-management-working-parents.html",
    "blog/preparing-for-pregnancy-guide.html",
    "blog/ramadan-meal-planning.html",
    "blog/managing-healthcare-costs-families.html",
    "featured-stories/emirati-grandmother-cooking-traditions.html",
    "featured-stories/gulf-father-money-lessons.html",
    "peace-capsules/power-of-patience-marriage.html",
]

HERO_PEACE = "/assets/images/approved/hero-peace-at-home-5-steps.webp"
GOTTMAN = (
    '<a href="https://www.gottman.com/blog/the-magic-relationship-ratio/" '
    'target="_blank" rel="noopener">معهد جوتمان</a>'
)
MOH = (
    '<a href="https://www.moh.gov.sa/HealthAwareness/Pages/default.aspx" '
    'target="_blank" rel="noopener">وزارة الصحة السعودية</a>'
)
WHO = (
    '<a href="https://www.who.int/news-room/fact-sheets/detail/maternal-health" '
    'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
)
KSU = (
    '<a href="https://www.ksu.edu.sa/" target="_blank" rel="noopener">جامعة الملك سعود</a>'
)
KAU = (
    '<a href="https://www.kau.edu.sa/" target="_blank" rel="noopener">جامعة الملك عبدالعزيز</a>'
)
UAEU = (
    '<a href="https://www.uaeu.ac.ae/" target="_blank" rel="noopener">جامعة الإمارات</a>'
)
CCHI = (
    '<a href="https://www.chi.gov.sa/" target="_blank" rel="noopener">مجلس الضمان الصحي</a>'
)
PMC = (
    '<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6762025/" '
    'target="_blank" rel="noopener">مراجعة علمية</a>'
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


def touch_date(html: str) -> str:
    return re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=1)


def fix_stress(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace("للعمل المركز", "للعمل بتركيز عميق")
    html = html.replace("العمل المركز", "العمل بتركيز عميق")
    html = html.replace("اللعب المركز", "اللعب بتركيز كامل")
    html = html.replace(
        "وجدت دراسة من جامعة الإمارات 2024",
        f"وفق {UAEU}، وجدت دراسة محلية",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_preparing(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "وجدت دراسة من جامعة الملك سعود 2024",
        f"وفق {KSU}، وجدت دراسة",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_ramadan(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "دراسة من جامعة الملك عبدالعزيز 2024",
        f"دراسة من {KAU}",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_healthcare(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "مركز الرعاية العاجلة",
        "عيادة العلاج العاجل",
    )
    html = html.replace(
        "في مستشفى خاص تكلف",
        f"وفق {MOH}، زيارة الطوارئ في مستشفى خاص تكلف",
    )
    html = html.replace(
        "دراسة من مجلس الضمان الصحي السعودي",
        f"دراسة من {CCHI}",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_emirati(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace("علاوة على ذلك، ", "أيضاً، ")
    html = html.replace(
        "هناك أيضاً فوائد أكاديمية غير متوقعة",
        f"هناك أيضاً فوائد تعليمية غير متوقعة، كما تلخصها {PMC}",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_gulf_father(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(
        r"<p>هناك العديد من الدروس العملية والتطبيقية[^<]+</p>",
        (
            "<p>هناك دروس عملية يمكن للأب الخليجي أن يعلّمها أبناءه في المنزل والمدرسة "
            f"والمسجد: الادخار، الصدق، العمل، والامتنان. راجع {MOH} "
            'لإرشادات الصحة النفسية الأسرية.</p>'
        ),
        html,
        count=1,
    )
    html = re.sub(
        r'<p><span class="en">Get more family tips[^<]+</span><span class="ar">احصل على نصائح أسرية كل جمعة - اشترك في نشرتنا\.</span></p>',
        "<p>احصل على نصائح أسرية كل جمعة عبر نشرتنا البريدية.</p>",
        html,
        count=1,
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_patience(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"https://images\.unsplash\.com/[^\"']+", HERO_PEACE, html)
    html = fix_article_em_dashes(html)
    html = html.replace("أبحاث معهد جوتمان", f"أبحاث {GOTTMAN}")
    html = html.replace(
        "دراسة عام 2018 في مجلة علم النفس الإيجابي",
        f"مراجعة في {PMC}",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def main() -> int:
    handlers = {
        "stress-management-working-parents": fix_stress,
        "preparing-for-pregnancy-guide": fix_preparing,
        "ramadan-meal-planning": fix_ramadan,
        "managing-healthcare-costs-families": fix_healthcare,
        "emirati-grandmother-cooking-traditions": fix_emirati,
        "gulf-father-money-lessons": fix_gulf_father,
        "power-of-patience-marriage": fix_patience,
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
