#!/usr/bin/env python3
"""Group A: WebApplication + BreadcrumbList + FAQPage for 12 tools; flip index."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools"

TOOLS = [
    "age-calculator",
    "inheritance-calculator",
    "monthly-budget",
    "mortgage-calculator",
    "password-generator",
    "plant-watering",
    "pomodoro",
    "rental-yield-calculator",
    "roi-calculator",
    "salary-calculator",
    "savings-goal",
    "travel-tips",
]

CATEGORIES = {
    "age-calculator": "HealthApplication",
    "inheritance-calculator": "FinanceApplication",
    "monthly-budget": "FinanceApplication",
    "mortgage-calculator": "FinanceApplication",
    "password-generator": "SecurityApplication",
    "plant-watering": "LifestyleApplication",
    "pomodoro": "ProductivityApplication",
    "rental-yield-calculator": "FinanceApplication",
    "roi-calculator": "FinanceApplication",
    "salary-calculator": "FinanceApplication",
    "savings-goal": "FinanceApplication",
    "travel-tips": "TravelApplication",
}

ZAKAT_DISCLAIMER = (
    '  <div class="tip"><p><strong><span class="en">Disclaimer:</span>'
    '<span class="ar">إخلاء مسؤولية:</span></strong> '
    '<span class="en">This calculator provides a general estimate for reference only and is not a '
    "religious ruling (fatwa) or licensed financial advice. Consult a qualified scholar or "
    "licensed advisor for your specific situation.</span>"
    '<span class="ar">هذه الأداة تقدّم تقديراً عاماً للمرجع فقط وليست فتوى ولا استشارة مالية مرخصة. '
    "استشر عالماً مؤهلاً أو مستشاراً مرخصاً لحالتك الخاصة.</span></p></div>\n"
)

NEED_ZAKAT_STYLE_DISCLAIMER = {"inheritance-calculator"}


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def extract_en_span(html: str, pattern: str) -> str:
    m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if not m:
        return ""
    block = m.group(1)
    em = re.search(r'<span class="en">(.*?)</span>', block, re.DOTALL)
    return strip_tags(em.group(1)) if em else strip_tags(block)


def extract_faqs_t(html: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for item in re.finditer(
        r'<div class="t-faq-item">.*?<div class="t-faq-q".*?<span class="en">(.*?)</span>.*?'
        r'<div class="t-faq-a">.*?<span class="en">(.*?)</span>',
        html,
        re.DOTALL,
    ):
        q, a = strip_tags(item.group(1)), strip_tags(item.group(2))
        if q and a:
            out.append((q, a))
    return out


def extract_faqs_pg(html: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for item in re.finditer(
        r'<div class="pg-faq-item">\s*<div class="pg-faq-q".*?<span class="en">(.*?)</span>.*?'
        r'<div class="pg-faq-a">.*?<span class="en">(.*?)</span>',
        html,
        re.DOTALL,
    ):
        q, a = strip_tags(item.group(1)), strip_tags(item.group(2))
        if q and a:
            out.append((q, a))
    return out


def extract_how_this_works(html: str) -> tuple[str, str] | None:
    m = re.search(
        r'<span class="en">How this works</span>.*?<p class="en">(.*?)</p>',
        html,
        re.DOTALL,
    )
    if not m:
        m = re.search(
            r'<span class="en">How this is calculated</span>.*?<p class="en">(.*?)</p>',
            html,
            re.DOTALL,
        )
    if not m:
        return None
    text = strip_tags(m.group(1))
    if not text:
        return None
    return ("How does this tool work?", text)


def extract_travel_tip_faqs(html: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for item in re.finditer(
        r'<div class="tt-gold-tip">.*?<h3><span class="en">(.*?)</span>.*?'
        r'<p><span class="en">(.*?)</span>',
        html,
        re.DOTALL,
    ):
        q, a = strip_tags(item.group(1)), strip_tags(item.group(2))
        if q and a:
            out.append((q, a))
        if len(out) >= 6:
            break
    return out


def extract_pomodoro_faqs(html: str) -> list[tuple[str, str]]:
    faqs = [
        (
            "What is the Pomodoro Technique?",
            "Work in focused blocks (default 25 minutes), take short breaks (5 minutes), "
            "repeat four sessions, then take a longer break (15 minutes).",
        ),
    ]
    for card in re.finditer(
        r'<div class="pomo-how-card">.*?<span class="en">(.*?)</span>.*?'
        r'<span class="en">(.*?)</span>',
        html,
        re.DOTALL,
    ):
        name, body = strip_tags(card.group(1)), strip_tags(card.group(2))
        if name and body and name not in ("Deep Focus", "Short Break"):
            continue
        if name == "Deep Focus":
            faqs.append(("How long is a Pomodoro focus session?", body))
        elif name == "Short Break":
            faqs.append(("How long are Pomodoro breaks?", body))
    faqs.append(
        (
            "Can I customize timer durations?",
            "Yes. Adjust focus, short break, long break, and sessions per cycle in Timer Settings.",
        )
    )
    return faqs[:6]


def extract_plant_faqs(html: str) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    # existing partial schema / seasonal content
    faqs.append(
        (
            "How often should I water plants in Gulf summer?",
            "Most indoor plants need watering every 2-3 days in Gulf summer (40-50°C). "
            "Desert plants like cactus every 7-14 days.",
        )
    )
    how = extract_how_this_works(html)
    if how:
        faqs.append(how)
    for card in re.finditer(
        r'<div class="pw-season-card">.*?<div class="pw-season-name en">(.*?)</div>.*?'
        r'<div class="pw-season-tip en">(.*?)</div>',
        html,
        re.DOTALL,
    ):
        season, tip = strip_tags(card.group(1)), strip_tags(card.group(2))
        if season and tip:
            faqs.append((f"How should I care for plants in {season}?", tip))
    return faqs[:6]


def extract_monthly_budget_faqs(html: str) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    how = extract_how_this_works(html)
    if how:
        faqs.append(how)
    faqs.append(
        (
            "What is Halal Finance Mode?",
            "Replaces interest-based tips with Islamic finance guidance.",
        )
    )
    m = re.search(r'<div class="how-body"><span class="en">(.*?)</span>', html, re.DOTALL)
    if m:
        faqs.append(("What does the budget planner show?", strip_tags(m.group(1))))
    m = re.search(
        r'<p class="en">Enter net monthly income and expenses by category\.(.*?)</p>',
        html,
        re.DOTALL,
    )
    if m:
        faqs.append(("How do I use the monthly budget planner?", strip_tags(m.group(0))))
    return faqs[:6]


def extract_roi_faqs(html: str) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    how = extract_how_this_works(html)
    if how:
        faqs.append(how)
    faqs.append(
        (
            "What costs are included in property ROI?",
            "ROI includes rental income and appreciation minus transfer fees, service costs, "
            "and mortgage payments, compared against stocks, REITs, deposits, and sukuk.",
        )
    )
    return faqs


def extract_rental_yield_faqs(html: str) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    how = extract_how_this_works(html)
    if how:
        faqs.append(how)
    faqs.extend(
        [
            (
                "What is gross rental yield?",
                "Gross yield equals annual rent divided by property value.",
            ),
            (
                "What is net rental yield?",
                "Net yield uses effective gross income minus vacancy and operating expenses (RICS-style).",
            ),
            (
                "Is this rental yield calculator financial advice?",
                "No. It offers general financial estimates for education only; consult a licensed advisor.",
            ),
        ]
    )
    return faqs[:6]


def extract_savings_faqs(html: str) -> list[tuple[str, str]]:
    faqs = extract_faqs_t(html)
    how = extract_how_this_works(html)
    if how:
        faqs.insert(0, how)
    if len(faqs) < 4:
        faqs.append(
            (
                "What are the two savings modes?",
                "Mode 1: enter target, current savings, and monthly contribution to see time needed. "
                "Mode 2: enter a timeframe to see required monthly savings.",
            )
        )
    return faqs[:6]


def collect_faqs(slug: str, html: str) -> list[tuple[str, str]]:
    if slug == "travel-tips":
        return extract_travel_tip_faqs(html)
    if slug == "pomodoro":
        return extract_pomodoro_faqs(html)
    if slug == "plant-watering":
        return extract_plant_faqs(html)
    if slug == "monthly-budget":
        return extract_monthly_budget_faqs(html)
    if slug == "roi-calculator":
        return extract_roi_faqs(html)
    if slug == "rental-yield-calculator":
        return extract_rental_yield_faqs(html)
    if slug == "savings-goal":
        return extract_savings_faqs(html)

    if slug == "password-generator":
        return extract_faqs_pg(html)

    faqs = extract_faqs_t(html) or extract_faqs_pg(html)
    how = extract_how_this_works(html)
    if how and not any(how[0].lower() in q.lower() for q, _ in faqs):
        faqs.append(how)
    return faqs[:6]


def meta_content(html: str, name: str) -> str:
    m = re.search(
        rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"',
        html,
        re.IGNORECASE,
    )
    return unescape(m.group(1)) if m else ""


def tool_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    return strip_tags(m.group(1)) if m else ""


def build_schema(slug: str, html: str) -> dict:
    url = f"https://dotforlife.com/tools/{slug}.html"
    title = tool_title(html)
    name = title.split("|")[0].strip() if "|" in title else title
    desc = meta_content(html, "description") or name
    faqs = collect_faqs(slug, html)
    if not faqs:
        raise ValueError(f"No FAQs extracted for {slug}")

    main_entity = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in faqs
    ]

    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebApplication",
                "name": name,
                "url": url,
                "description": desc,
                "applicationCategory": CATEGORIES.get(slug, "UtilityApplication"),
                "operatingSystem": "Any",
                "offers": {"@type": "Offer", "price": "0", "priceCurrency": "SAR"},
                "inLanguage": ["en", "ar"],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://dotforlife.com"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Library",
                        "item": "https://dotforlife.com/library.html",
                    },
                    {"@type": "ListItem", "position": 3, "name": name, "item": url},
                ],
            },
            {"@type": "FAQPage", "mainEntity": main_entity},
        ],
    }


def replace_ld_json(html: str, schema: dict) -> str:
    block = (
        '<script type="application/ld+json">'
        + json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )
    if re.search(r'<script type="application/ld\+json">', html):
        html = re.sub(
            r'<script type="application/ld\+json">.*?</script>',
            block,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        html = html.replace("</head>", block + "\n</head>", 1)
    return html


def flip_robots(html: str) -> str:
    html = re.sub(
        r'<meta\s+name="robots"\s+content="noindex,nofollow"\s*/?>',
        '<meta name="robots" content="index,follow">',
        html,
        flags=re.IGNORECASE,
    )
    if 'name="robots"' not in html:
        html = html.replace("<head>", '<head>\n<meta name="robots" content="index,follow">', 1)
    return html


def fix_travel_em_dash(html: str) -> str:
    return html.replace("\u2014", " - ")


def add_disclaimer_if_needed(slug: str, html: str) -> str:
    if slug not in NEED_ZAKAT_STYLE_DISCLAIMER:
        return html
    if re.search(r'class="tip"', html) or re.search(r"إخلاء\s+مسؤولية", html):
        return html
    if re.search(r"</main>", html):
        return html.replace("</main>", ZAKAT_DISCLAIMER + "</main>", 1)
    return html.replace("</body>", ZAKAT_DISCLAIMER + "</body>", 1)


def validate_json(schema: dict) -> None:
    json.dumps(schema)  # noqa: JSON serializable
    text = json.dumps(schema)
    json.loads(text)


def amer_ignorable_fails(fails: list[str]) -> list[str]:
    ignore = ("كلمات=", "Article schema مفقود")
    return [f for f in fails if not any(i in f for i in ignore)]


def process(slug: str) -> dict:
    path = TOOLS_DIR / f"{slug}.html"
    html = path.read_text(encoding="utf-8")
    if slug == "travel-tips":
        html = fix_travel_em_dash(html)
    schema = build_schema(slug, html)
    validate_json(schema)
    html = replace_ld_json(html, schema)
    html = add_disclaimer_if_needed(slug, html)
    html = flip_robots(html)
    path.write_text(html, encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "amer_gate.py"), str(path)],
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    fails = [ln.replace("     FAIL: ", "") for ln in out.splitlines() if "FAIL:" in ln]
    warns = [ln.replace("     warn: ", "") for ln in out.splitlines() if "warn:" in ln]
    real_fails = amer_ignorable_fails(fails)
    return {
        "slug": slug,
        "faqs": len(schema["@graph"][2]["mainEntity"]),
        "fails": real_fails,
        "warns": warns,
        "ok": len(real_fails) == 0,
    }


def main() -> int:
    results = [process(slug) for slug in TOOLS]
    ok = sum(1 for r in results if r["ok"])
    print(f"Group A: {ok}/{len(results)} tools clear (ignoring words/Article)")
    for r in results:
        status = "OK" if r["ok"] else "ISSUE"
        print(f"  {status}  {r['slug']}  FAQs={r['faqs']}")
        for f in r["fails"]:
            print(f"         FAIL: {f}")
        for w in r["warns"]:
            print(f"         warn: {w}")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
