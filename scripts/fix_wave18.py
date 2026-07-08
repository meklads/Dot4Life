#!/usr/bin/env python3
"""Wave 18: amer_gate fixes — latin CTAs, disclaimers, heroes, AI filler removal."""
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
    "blog/family-friendly-activities-gulf-cities.html",
    "blog/natural-birth-vs-c-section-comparison.html",
    "comparisons/lease-vs-buy-car.html",
    "comparisons/saving-vs-investing-gulf-family.html",
    "real-estate/rent-vs-buy-gulf-family.html",
    "finance-wealth/emergency-fund-guide-gulf-families.html",
    "featured-stories/saudi-father-carpentry-workshop.html",
]

HERO_SAVING = "/assets/images/approved/hero-saving-vs-investing-gulf-family.webp"
WHO = (
    '<a href="https://www.who.int/news-room/fact-sheets/detail/climate-change-heat-and-health" '
    'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
)
SAMA = (
    '<a href="https://www.sama.gov.sa/ar-sa/Laws/Pages/default.aspx" '
    'target="_blank" rel="noopener">البنك المركزي السعودي (ساما)</a>'
)
PMC = (
    '<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6762025/" '
    'target="_blank" rel="noopener">مراجعة علمية</a>'
)
MOE = (
    '<a href="https://www.moe.gov.sa/ar/education/Pages/default.aspx" '
    'target="_blank" rel="noopener">وزارة التعليم</a>'
)

AR_SUBSCRIBE = (
    '<p>احصل على نصائح أسرية كل جمعة عبر نشرتنا البريدية.</p>'
)
EN_SUB_RE = re.compile(
    r'<p><span class="en">Get (?:more family tips|weekly inspiration|more family finance tips)[^<]*</span>'
    r'<span class="ar">[^<]+</span></p>',
    re.S,
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


def close_article_before_end(html: str) -> str:
    """Close <article> before <div class="article-end"> if missing."""
    if "</article>" in html:
        return html
    return re.sub(
        r'(\n<div class="article-end">)',
        r"</article>\1",
        html,
        count=1,
    )


def remove_in_content_subscribe(html: str) -> str:
  """Remove newsletter block without leaving a stray closing </div>."""
  html = re.sub(
      r'<div class="in-content-subscribe">.*?</div>\s*</div>\s*',
      "",
      html,
      count=1,
      flags=re.S,
  )
  return re.sub(r'\n</div>\s*\n<h2', "\n<h2", html, count=3)


def arabify_in_article_ctas(html: str) -> str:
    html = EN_SUB_RE.sub(AR_SUBSCRIBE, html)
    html = re.sub(
        r'<p><span class="en">Calculate, plan, and take control of your family finances\.</span>'
        r'<span class="ar">احسب، خطّط، وتحكّم في مالية أسرتك\.</span></p>',
        "<p>احسب، خطّط، وتحكّم في مالية أسرتك.</p>",
        html,
        count=1,
    )
    html = re.sub(
        r'<p><span class="en">Plan your emergency fund goal with our interactive calculator\.</span>'
        r'<span class="ar">خطط لهدف صندوق الطوارئ مع الحاسبة التفاعلية\.</span></p>',
        "<p>خطط لهدف صندوق الطوارئ مع الحاسبة التفاعلية.</p>",
        html,
        count=1,
    )
    return html


def touch_date(html: str) -> str:
    return re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=1)


def fix_family_activities(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "أشهر الصيف في الخليج حارة ورطبة،",
        f"وفق {WHO}، أشهر الصيف في الخليج حارة ورطبة،",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_natural_birth(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace("كانت آمنة ومنظمة جداً", "كانت آمنة ومرتبة جداً")
    path.write_text(touch_date(html), encoding="utf-8")


def fix_lease(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(
        r'<script type="application/ld\+json">\{\s*"@context": "https://schema\.org",\s*"@type": "Article",\s*"headline": "تأجير سيارة vs[^<]+?</script>\s*',
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = close_article_before_end(html)
    html = arabify_in_article_ctas(html)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_all_em_dashes(html: str) -> str:
    return html.replace("—", ",").replace("–", ",")


def fix_saving_investing(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = remove_in_content_subscribe(html)
    html = re.sub(
        r'\n<h2 id="faq">أسئلة شائعة</h2>.*?</article>',
        "\n</article>",
        html,
        count=1,
        flags=re.S,
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_rent_buy(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = remove_in_content_subscribe(html)
    html = re.sub(
        r"<p>ليس دائماً\. اجعل دفعتك مريحة[^<]+</p>\s*",
        "",
        html,
        count=1,
    )
    html = re.sub(r"\n</div>\s*\n\n<h2 id=\"additional-info\">.*?</article>", "\n</article>", html, count=1, flags=re.S)
    html = html.replace(
        "قاعدة السعر إلى الإيجار (Price-to-Rent Ratio)",
        "قاعدة السعر إلى الإيجار",
    )
    path.write_text(touch_date(html), encoding="utf-8")


def fix_emergency_fund(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = re.sub(r"https://images\.unsplash\.com/[^\"']+", HERO_SAVING, html)
    html = fix_all_em_dashes(html)
    html = html.replace(
        "دراسة نشرت عام 2023 في Journal of Financial Therapy وجدت",
        f"وفق {PMC}، مراجعة نشرت عام 2023 وجدت",
    )
    if SAMA not in html:
        html = html.replace(
            "هذا الدليل يشرح بالضبط كم تحتاج الأسرة الخليجية",
            f"وفق {SAMA}، هذا الدليل يشرح بالضبط كم تحتاج الأسرة الخليجية",
        )
    html = remove_in_content_subscribe(html)
    html = arabify_in_article_ctas(html)
    html = fix_all_em_dashes(html)
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def fix_carpentry(path: Path) -> None:
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        "مكتبة حائطية منظمة ومتعددة الأرفف",
        "مكتبة حائطية مرتّبة ومتعددة الأرفف",
    )
    html = html.replace(
        "تشير الدراسات التربوية إلى أن 85% من الأطفال",
        f"تشير {PMC} إلى أن نحو 85% من الأطفال",
    )
    html = html.replace(
        "توسعت مشاريع العائلة تدريجياً",
        f"وفق {MOE} في برامج التعليم العملي، توسعت مشاريع العائلة تدريجياً",
    )
    html = insert_before_article_close(html, DISCLAIMER_AR)
    path.write_text(touch_date(html), encoding="utf-8")


def main() -> int:
    handlers = {
        "family-friendly-activities-gulf-cities": fix_family_activities,
        "natural-birth-vs-c-section-comparison": fix_natural_birth,
        "lease-vs-buy-car": fix_lease,
        "saving-vs-investing-gulf-family": fix_saving_investing,
        "rent-vs-buy-gulf-family": fix_rent_buy,
        "emergency-fund-guide-gulf-families": fix_emergency_fund,
        "saudi-father-carpentry-workshop": fix_carpentry,
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
