#!/usr/bin/env python3
"""Amer site-wide batch 1: disclaimers + em-dash cleanup for first 6 tools."""
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
        '<span class="en">This converter uses standard tabular algorithms for general reference; '
        "it is not a religious ruling. For worship dates and official matters, follow your local authority "
        'and qualified scholars.</span>'
        '<span class="ar">هذا المحوّل يستخدم خوارزميات جدولية معيارية للمرجع العام فقط وليس فتوى. '
        "لمواعيد العبادات والأمور الرسمية، اتبع الجهة المحلية وأهل العلم المؤهلين.</span></p></div>\n"
    ),
    "security": (
        '  <div class="tip"><p><strong><span class="en">Disclaimer:</span>'
        '<span class="ar">إخلاء مسؤولية:</span></strong> '
        '<span class="en">Passwords are generated locally in your browser; we do not store them. '
        "Use unique passwords and a reputable password manager for important accounts.</span>"
        '<span class="ar">تُولَّد كلمات المرور محلياً في متصفحك ولا نخزّنها. '
        "استخدم كلمات مرور فريدة ومدير كلمات مرور موثوقاً للحسابات المهمة.</span></p></div>\n"
    ),
}

FILES = [
    ("tools/age-calculator.html", "health"),
    ("tools/hijri-converter.html", "islamic"),
    ("tools/monthly-budget.html", "finance"),
    ("tools/mortgage-calculator.html", "finance"),
    ("tools/one-rep-max.html", "health"),
    ("tools/password-generator.html", "security"),
]


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


def main() -> None:
    backup = ROOT / "tools" / "_finance_backup"
    if backup.is_dir():
        for f in sorted(backup.glob("*.html")):
            f.unlink()
            print(f"deleted {f.relative_to(ROOT)}")
        if not any(backup.iterdir()):
            print("backup dir empty (kept for robots disallow)")

    for rel, cat in FILES:
        fix_file(rel, cat)


if __name__ == "__main__":
    main()
