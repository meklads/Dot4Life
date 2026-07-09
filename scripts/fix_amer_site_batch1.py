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

BATCHES = {"1": BATCH1, "2": BATCH2}


def has_disclaimer(html: str) -> bool:
    return 'class="tip"' in html and (
        "إخلاء مسؤولية" in html or "Disclaimer:" in html
    )


def fix_file(rel: str, category: str) -> None:
    path = ROOT / rel
    html = path.read_text(encoding="utf-8")
    if not has_disclaimer(html):
        block = DISCLAIMERS[category]
        if "</main>" not in html:
            raise SystemExit(f"no </main> in {rel}")
        html = html.replace("</main>", block + "</main>", 1)
    html = html.replace("—", " - ")
    path.write_text(html, encoding="utf-8")
    print(f"fixed {rel}")


def run_batch(batch_id: str) -> None:
    files = BATCHES.get(batch_id)
    if not files:
        raise SystemExit(f"unknown batch {batch_id!r}")
    for rel, cat in files:
        fix_file(rel, cat)


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
