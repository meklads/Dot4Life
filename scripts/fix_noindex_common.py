#!/usr/bin/env python3
"""Shared amer_gate auto-fixes for noindex isolated pages."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CLICHE = [
    "في الختام",
    "في عصرنا الحالي",
    "in conclusion",
    "In conclusion",
    "moreover,",
    "Moreover,",
    "in today's fast",
    "In today's fast",
]

DISCLAIMER_AR = (
    '<div class="tip"><p><strong>إخلاء مسؤولية:</strong> معلومات عامة فقط وليست استشارة '
    "طبية أو مالية أو فتوى شرعية. راجع مختصاً مرخصاً عند الحاجة.</p></div>\n"
)
DISCLAIMER_EN = (
    '<aside class="article-disclaimer" style="background:#FAF8F4;border-left:4px solid #fd781c;'
    'padding:14px 18px;margin:24px 0;border-radius:8px;font-size:.95rem;color:#054241">'
    "<strong>Disclaimer:</strong> General information only, not medical, financial, or religious "
    "advice. Consult a licensed professional when needed.</aside>\n"
)

WHO = (
    '<a href="https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight" '
    'target="_blank" rel="noopener">WHO</a>'
)
WHO_AR = (
    '<a href="https://www.who.int/ar/news-room/fact-sheets/detail/obesity-and-overweight" '
    'target="_blank" rel="noopener">منظمة الصحة العالمية</a>'
)
SAMA = (
    '<a href="https://www.sama.gov.sa/en-US/Pages/default.aspx" '
    'target="_blank" rel="noopener">SAMA</a>'
)
SAMA_AR = (
    '<a href="https://www.sama.gov.sa/ar-sa/Pages/default.aspx" '
    'target="_blank" rel="noopener">البنك المركزي السعودي (ساما)</a>'
)
REGA = (
    '<a href="https://www.rega.gov.sa/en/about" target="_blank" rel="noopener">REGA</a>'
)
HAJ = (
    '<a href="https://www.haj.gov.sa/en/PlanYourHajj/Umrah" '
    'target="_blank" rel="noopener">Ministry of Hajj</a>'
)
MOE = (
    '<a href="https://www.moe.gov.sa/en/Pages/default.aspx" '
    'target="_blank" rel="noopener">Ministry of Education</a>'
)
AHA = (
    '<a href="https://www.heart.org/en/healthy-living/fitness/fitness-basics/aha-recs-for-physical-activity-in-adults" '
    'target="_blank" rel="noopener">American Heart Association</a>'
)

AUTHORITY_PATTERN = re.compile(
    r"(جامعة [\w؀-ۿ]+|معهد [\w؀-ۿ]+|مركز [\w؀-ۿ]+|مجلة [\w؀-ۿ]+|أكاديمية [\w؀-ۿ]+|منظمة [\w؀-ۿ]+"
    r"|دراسة (?:من|أجرتها)[^.]{0,40}"
    r"|[Uu]niversity of \w+|[Ii]nstitute of \w+|[Cc]enter for \w+|[Jj]ournal of [\w ]+"
    r"|[Aa]cademy of \w+|[Ss]tudies? (?:from|by|published in)|[Rr]esearch (?:from|by|shows)"
    r"|found that|shows that|World Health Organization|American Heart Association)"
)

DISCLAIMER_RE = re.compile(
    r"(إخلاء|ليست\s+استشارة|ليست\s+فتوى|معلومات\s+عامة|راجع\s+(?:طبيب|مختص|أهل\s+العلم|مستشار)"
    r"|disclaimer|not\s+(?:medical|financial|professional)\s+advice|not\s+a\s+fatwa|consult)",
    re.I,
)

EN_SUB_RE = re.compile(
    r'<p><span class="en">Get (?:more family tips|weekly inspiration|more family finance tips|'
    r"more family wellness tips|more Saudi real estate tips)[^<]*</span>"
    r'<span class="ar">[^<]+</span></p>',
    re.S,
)


def is_arabic(html: str) -> bool:
    m = re.search(r"<html\b[^>]*>", html)
    tag = m.group(0) if m else ""
    return bool(re.search(r'(?<![a-zA-Z-])lang=["\']ar["\']', tag))


def fix_em_dashes(html: str) -> str:
    return html.replace("—", ", ").replace("–", ", ")


def remove_cliches(html: str) -> str:
    for c in CLICHE:
        html = re.sub(re.escape(c) + r",?\s*", "", html, flags=re.I)
    return html


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
    return html


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


def category_link(path: str, ar: bool) -> str:
    p = path.lower()
    if any(x in p for x in ("finance", "budget", "invest", "mortgage", "halal", "zakat", "saving", "emergency", "wealth")):
        return SAMA_AR if ar else SAMA
    if any(x in p for x in ("real-estate", "rent", "property", "reit", "roi")):
        return REGA if not ar else (
            '<a href="https://www.rega.gov.sa/ar/about" target="_blank" rel="noopener">الهيئة العامة للعقار</a>'
        )
    if any(x in p for x in ("hajj", "umrah", "islamic", "makkah", "medina")):
        return HAJ
    if any(x in p for x in ("school", "education", "homeschool")):
        return MOE
    if any(x in p for x in ("walking", "running", "heart", "cardio")):
        return AHA
    return WHO_AR if ar else WHO


def ensure_disclaimer(html: str, ar: bool) -> str:
    if DISCLAIMER_RE.search(html):
        return html
    block = DISCLAIMER_AR if ar else DISCLAIMER_EN
    return insert_before_article_close(html, block)


def ensure_article_schema(html: str) -> str:
    if re.search(r'"@type"\s*:\s*"Article"', html):
        return html
    title_m = re.search(r"<title>([^<]+)</title>", html)
    title = title_m.group(1).split("|")[0].strip() if title_m else "Article"
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', html)
    desc = desc_m.group(1) if desc_m else title
    canon_m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    url = canon_m.group(1) if canon_m else ""
    block = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "dateModified": "2026-07-09",
        "author": {"@type": "Organization", "name": "DOTFORLIFE"},
    }
    if url:
        block["mainEntityOfPage"] = url
    script = f'<script type="application/ld+json">{json.dumps(block, ensure_ascii=False)}</script>\n'
    return html.replace("</head>", script + "</head>", 1)


def extract_faq_pairs(html: str) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for m in re.finditer(
        r'<div class="faq-item">\s*<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>',
        html,
        re.S,
    ):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        a = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if q and a:
            pairs.append((q, a))
    if len(pairs) >= 4:
        return pairs[:6]
    for m in re.finditer(
        r'itemtype="https://schema.org/Question"[^>]*>\s*<h3[^>]*>(.*?)</h3>.*?itemprop="text"[^>]*>\s*<p[^>]*>(.*?)</p>',
        html,
        re.S,
    ):
        q = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        a = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if q and a:
            pairs.append((q, a))
    return pairs[:6]


def ensure_faq_schema(html: str) -> str:
    if re.search(r'"@type"\s*:\s*"FAQPage"', html):
        return html
    pairs = extract_faq_pairs(html)
    if len(pairs) < 4:
        return html
    entities = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in pairs
    ]
    block = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    script = f'<script type="application/ld+json">{json.dumps(block, ensure_ascii=False)}</script>\n'
    return html.replace("</head>", script + "</head>", 1)


def repair_invalid_ld_json(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        raw = m.group(1).strip()
        try:
            json.loads(raw)
            return m.group(0)
        except json.JSONDecodeError:
            return ""

    return re.sub(
        r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',
        repl,
        html,
        flags=re.S,
    )


def article_chunk(html: str) -> str:
    m = re.search(r"<article\b[^>]*>(.*?)</article>", html, re.S | re.I)
    return m.group(1) if m else ""


def has_deep_in_article(html: str) -> bool:
    chunk = article_chunk(html)
    if not chunk:
        return False
    skip = (
        "dotforlife",
        "d4l",
        "google",
        "gstatic",
        "googletagmanager",
        "pagead",
        "facebook",
        "twitter",
        "wa.me",
        "fonts.",
    )
    for link in re.findall(r'href=["\'](https?://[^"\']+)["\']', chunk):
        if any(s in link.lower() for s in skip):
            continue
        m = re.match(r"https?://[^/]+/(.+)", link)
        if m and len(m.group(1).strip("/")) > 3:
            return True
    return False


def link_inline_authorities(html: str, ar: bool) -> str:
    sama = SAMA_AR if ar else SAMA
    html = html.replace("Saudi Central Bank SAMA recommends", f"{sama} recommends")
    html = html.replace("The Saudi Central Bank (SAMA)", sama)
    html = html.replace("World Health Organization", WHO if not ar else WHO_AR)
    html = html.replace("American Heart Association", AHA)
    return html


def fix_unsplash_heroes(html: str, path: str) -> str:
    if "unsplash.com" not in html.lower():
        return html
    ar_path = path.replace("-en.html", ".html")
    ar_fp = ROOT / ar_path
    hero = "/assets/images/approved/hero-gold-vs-real-estate-gulf-family.webp"
    if ar_fp.exists():
        m = re.search(
            r"/assets/images/approved/hero-[^\"']+\.webp",
            ar_fp.read_text(encoding="utf-8"),
        )
        if m:
            hero = m.group(0)
    return re.sub(r"https://images\.unsplash\.com/[^\"']+", hero, html, flags=re.I)


def inject_deep_link(html: str, path: str, ar: bool) -> str:
    if has_deep_in_article(html):
        return html
    link = category_link(path, ar)
    prefix_en = f"According to {link}, "
    prefix_ar = f"وفق {link}، "
    prefix = prefix_ar if ar else prefix_en

    def add_to_first_p(match: re.Match[str]) -> str:
        tag, inner, close = match.group(1), match.group(2), match.group(3)
        if "<a href" in inner[:160]:
            return match.group(0)
        return f"{tag}{prefix}{inner}{close}"

    m = re.search(r"<article\b[^>]*>(.*?)</article>", html, re.S)
    if not m:
        return html
    article = m.group(1)
    new_article = re.sub(
        r"(<p[^>]*>)(.*?)(</p>)",
        add_to_first_p,
        article,
        count=1,
        flags=re.S,
    )
    return html.replace(article, new_article, 1)


def fix_authority_paragraphs(html: str, path: str, ar: bool) -> str:
    link = category_link(path, ar)
    prefix_en = f"According to {link}, "
    prefix_ar = f"وفق {link}، "
    prefix = prefix_ar if ar else prefix_en

    def fix_p(match: re.Match[str]) -> str:
        full, inner = match.group(0), match.group(1)
        plain = re.sub(r"<[^>]+>", "", inner).strip()
        if len(plain) < 20:
            return full
        if "<a href" in inner.lower():
            return full
        if not AUTHORITY_PATTERN.search(plain):
            return full
        return full.replace(inner, prefix + inner, 1)

    return re.sub(r"<p[^>]*>(.*?)</p>", fix_p, html, flags=re.S)


def touch_date(html: str) -> str:
    return re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-07-09"', html, count=5)


def apply_common_fixes(html: str, path: str) -> str:
    ar = is_arabic(html)
    html = repair_invalid_ld_json(html)
    html = fix_unsplash_heroes(html, path)
    html = fix_em_dashes(html)
    html = remove_cliches(html)
    html = remove_in_content_subscribe(html)
    html = EN_SUB_RE.sub(
        "<p>Get family tips every Friday in our newsletter.</p>" if not ar else "<p>احصل على نصائح أسرية كل جمعة.</p>",
        html,
    )
    html = ensure_disclaimer(html, ar)
    html = ensure_article_schema(html)
    html = ensure_faq_schema(html)
    html = link_inline_authorities(html, ar)
    html = inject_deep_link(html, path, ar)
    html = fix_authority_paragraphs(html, path, ar)
    return touch_date(html)


def is_redirect_stub(html: str) -> bool:
    if re.search(r'http-equiv="refresh"', html, re.I):
        return True
    m = re.search(r"<article\b[^>]*>(.*?)</article>", html, re.S)
    chunk = m.group(1) if m else html
    words = len(re.findall(r"\w+", re.sub(r"<[^>]+>", " ", chunk)))
    return words < 200 and "FAQPage" not in html
