#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix Group B HTML structural bugs (12 files) — re-runnable."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GROUP_B = [
    "blog/notification-cost-productivity-en.html",
    "blog/notification-cost-productivity.html",
    "blog/organize-life-daily-systems.html",
    "blog/stress-management-working-parents.html",
    "blog/zakat-guide-2025.html",
    "featured-stories/mother-built-online-business-home.html",
    "finance-wealth/teaching-children-savings.html",
    "featured-stories/saudi-father-carpentry-workshop-en.html",
    "featured-stories/saudi-father-carpentry-workshop.html",
    "fitness/fitness-for-women-saudi.html",
    "guides/saudi-mortgage-guide.html",
    "health-pregnancy/preconception-checkups.html",
]


def collapse_nested_anchors(html: str) -> str:
    prev = None
    while prev != html:
        prev = html
        html = re.sub(
            r"(<a\s[^>]*>)\s*(<a\s[^>]*>)\s*(<a\s[^>]*>)",
            r"\3",
            html,
            flags=re.I,
        )
        html = re.sub(
            r"(<a\s[^>]*>)\s*(<a\s[^>]*>)",
            r"\2",
            html,
            flags=re.I,
        )
    prev = None
    while prev != html:
        prev = html
        html = re.sub(r"(</a>)\s*(</a>)\s*(</a>)", r"\1", html, flags=re.I)
        html = re.sub(r"(</a>)\s*(</a>)", r"\1", html, flags=re.I)
    return html


def fix_escaped_hrefs(html: str) -> str:
    return html.replace('href=\\"', 'href="').replace('target=\\"', 'target="').replace(
        'rel=\\"', 'rel="'
    )


def fix_width_auto(html: str) -> str:
    return re.sub(
        r'width="auto"(?=\s+loading="lazy")',
        'width="56" height="56"',
        html,
    )


def fix_td_typo(html: str) -> str:
    return html.replace("<td->", "<td>").replace("<th->", "<th>")


def flip_index(html: str) -> str:
    return html.replace('content="noindex,nofollow"', 'content="index,follow"')


def fix_organize_life(html: str) -> str:
    html = html.replace(
        "</p> Schedule a reset day: a Saturday or Sunday where you review each system, "
        "identify what is working and what is not, make adjustments, and restart. "
        "This quarterly maintenance keeps your systems aligned with your changing life "
        "circumstances.<p></p>",
        "</p>\n<p>خصّص يوم إعادة ضبط: سبت أو أحد تراجع فيه كل نظام، تحدد ما ينجح وما لا "
        "ينجح، تعدّل ثم تعيد البدء. هذا الصيانة الربع سنوية تبقي أنظمتك متوافقة مع تغيّر "
        "ظروف حياتك.</p>",
    )
    html = re.sub(
        r'<div class="callout">\s*<div class="callout-label"><svg width="16" height="16" '
        r'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        r'stroke-linecap="round" stroke-linejoin="round">\s*</div>',
        '<div class="callout">\n'
        ' <div class="callout-label"><svg width="16" height="16" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 '
        '13 2"></polygon></svg> ابدأ بنظام واحد</div>\n'
        ' <p>لا تحاول تطبيق كل هذه الأنظمة دفعة واحدة. اختر نظاماً واحداً (روتين الصباح، '
        'أو المراجعة المالية، أو ترتيب المنزل) والتزم به 30 يوماً. عندما يصبح تلقائياً، '
        'أضف النظام التالي.</p>\n</div>',
        html,
        count=1,
    )
    broken_tools = re.search(
        r'<div><div class="at-name">Top 3 Tasks</div>.*?'
        r'<a href="/tools/pomodoro.html"><div class="at-icon">⏱️</div>.*?</a>\s*\n\s*</div>',
        html,
        flags=re.S,
    )
    if broken_tools:
        replacement = """<div class="related-articles" style="margin-top:3rem;padding-top:2rem;border-top:2px solid var(--border);">
 <a href="/daily-planner.html"><div class="at-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg></div><div><div class="at-name">مخطط اليوم</div><div class="at-desc">خطط يومك بفعالية</div></div></a>
 <a href="/tools/bmi-calculator.html"><div class="at-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="22"></line><polyline points="17 7 12 2 7 7"></polyline></svg></div><div><div class="at-name">حاسبة BMI</div><div class="at-desc">تابع مؤشرات صحتك</div></div></a>
 <a href="/blog/stress-management-working-parents.html"><div class="at-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10h16"></path><path d="M4 14h16"></path><rect x="2" y="6" width="20" height="12" rx="2"></rect></svg></div><div><div class="at-name">إدارة التوتر للآباء</div><div class="at-desc">وازن بين العمل والعائلة</div></div></a>
 <a href="/tools/pomodoro.html"><div class="at-icon">⏱️</div><div><div class="at-name">مؤقت التركيز</div><div class="at-desc">تقنية إدارة الوقت</div></div></a>
</div>"""
        html = html[: broken_tools.start()] + replacement + html[broken_tools.end() :]
    return html


def fix_saudi_mortgage(html: str) -> str:
    junk = re.search(
        r"<!-- ═+\s*\n\s*HERO\s*\n\s*═+ -->.*?<span class=\"en\"><svg width=\"16\" height=\"16\" "
        r"viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" "
        r"stroke-linecap=\"round\" stroke-linejoin=\"round\">\s*\n",
        html,
        flags=re.S,
    )
    if junk:
        html = html[: junk.start()] + html[junk.end() :]
    broken_cta = re.search(
        r'<div class="tool-cta-card">\s*<h3><span class="en"><svg width="16" height="16" '
        r'viewBox="0 0 24 24"[^>]*>\s*<p class="ar">',
        html,
        flags=re.S,
    )
    if broken_cta:
        html = html.replace(
            broken_cta.group(0),
            '<div class="tool-cta-card">\n'
            '          <h3><span class="en">🏠 Calculate Your Mortgage Payment</span>'
            '<span class="ar">🏠 احسب قسط التمويل العقاري</span></h3>\n'
            '          <p class="en">Estimate your monthly payment, total interest, REDF savings, '
            'and full amortization schedule using current Saudi bank rates.</p>\n'
            '          <p class="ar">',
            1,
        )
    return html


def fix_fitness_faq(html: str) -> str:
    return html.replace(
        '<p>According to <a href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" '
        'target="_blank" rel="noopener">WHO</a>, نعم، يؤثر النوم بشكل مباشر على عملية الأيض وحرق السعرات '
        'الحرارية. أظهرت <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3769102/" target="_blank" '
        'rel="noopener">sleep and metabolism research (PMC)</a> أن قلة النوم',
        '<p>وفق <a href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" '
        'target="_blank" rel="noopener">منظمة الصحة العالمية</a>، نعم، يؤثر النوم بشكل مباشر على عملية '
        'الأيض وحرق السعرات الحرارية. أظهرت <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3769102/" '
        'target="_blank" rel="noopener">دراسات النوم والأيض (PMC)</a> أن قلة النوم',
    )


def fix_preconception_table(html: str) -> str:
    if "<thead>" in html and "جدول الفحوصات قبل الحمل" in html:
        return html
    old = """<div class="table-wrap"><table>
<tr><th>الفحص</th><th>لماذا يهمّ</th><th>متى يُجرى</th></tr>
<tr><td>تحليل الدم الكامل (CBC)</td>"""
    new = """<div class="table-wrap"><table>
<thead><tr><th>الفحص</th><th>لماذا يهمّ</th><th>متى يُجرى</th></tr></thead>
<tbody>
<tr><td>تحليل الدم الكامل (CBC)</td>"""
    html = html.replace(old, new)
    html = html.replace(
        "<tr><td>فحوص الأمراض المنقولة جنسياً</td><td>كشف ومعالجة أي عدوى قبل الحمل</td>"
        "<td>بحسب توصية الطبيب</td></tr>\n</table></div>",
        "<tr><td>فحوص الأمراض المنقولة جنسياً</td><td>كشف ومعالجة أي عدوى قبل الحمل</td>"
        "<td>بحسب توصية الطبيب</td></tr>\n</tbody>\n</table></div>",
    )
    dup = (
        "<h3 id=\"هل-أحتاج-تكرار-الفحوصات-في-كل-حمل\">هل أحتاج تكرار الفحوصات في كل حمل؟</h3>"
        "<p>بعضها يُجرى مرة واحدة مثل فصيلة الدم، وبعضها قد يُعاد مع كل حمل أو حسب تغيّر "
        "حالتكِ الصحية، ويحدد الطبيب ذلك.</p>\n"
        "<p>بعضها يُجرى مرة واحدة مثل فصيلة الدم، وبعضها قد يُعاد مع كل حمل أو حسب تغيّر "
        "حالتكِ الصحية، ويحدد الطبيب ذلك.</p>"
    )
    fixed = dup.replace("\n<p>بعضها يُجرى مرة واحدة", "\n", 1)
    html = html.replace(dup, fixed.replace("\n\n", "\n"))
    return html


def process_file(rel: str) -> bool:
    path = ROOT / rel
    original = path.read_text(encoding="utf-8")
    html = original
    html = collapse_nested_anchors(html)
    html = fix_escaped_hrefs(html)
    html = fix_td_typo(html)
    html = fix_width_auto(html)
    if rel == "blog/organize-life-daily-systems.html":
        html = fix_organize_life(html)
    if rel == "guides/saudi-mortgage-guide.html":
        html = fix_saudi_mortgage(html)
    if rel == "fitness/fitness-for-women-saudi.html":
        html = fix_fitness_faq(html)
    if rel == "health-pregnancy/preconception-checkups.html":
        html = fix_preconception_table(html)
    html = flip_index(html)
    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = [f for f in GROUP_B if process_file(f)]
    print(f"Group B: {len(changed)}/{len(GROUP_B)} files updated")
    for f in changed:
        print(f"  ✓ {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
