#!/usr/bin/env python3
"""
TECH_BUILD: Inject approved Markdown drafts into live finance-wealth article shells.
Preserves URL/canonical; backs up before write. Adds Article + FAQPage JSON-LD.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "operating-system" / "reports" / "drafts"
BACKUP = ROOT / "outputs" / "backups" / "tech-build"

BUILD_MAP = [
    {
        "id": "A-01-1",
        "draft_ar": DRAFTS / "task01/investment-basics-beginners.md",
        "draft_en": DRAFTS / "task01/investment-basics-beginners-en.md",
        "out_ar": ROOT / "finance-wealth/investment-basics-beginners.html",
        "out_en": ROOT / "finance-wealth/investment-basics-beginners-en.html",
        "section_ar": "💰 مالية وثروة",
        "section_en": "💰 Finance & Wealth",
        "tool_cta_ar": "/tools/monthly-budget.html",
        "tool_cta_en": "/tools/monthly-budget.html",
        "tool_label_ar": "حاسبة الميزانية الشهرية",
        "tool_label_en": "Monthly Budget Calculator",
        "internal_links_ar": [
            ("/finance-wealth/family-budget-plan.html", "ميزانية الأسرة الخليجية: توزيع الراتب بذكاء"),
            ("/comparisons/saving-vs-investing-gulf-family.html", "الادخار أم الاستثمار لأسرة خليجية؟"),
            ("/comparisons/gold-vs-real-estate-gulf-family.html", "الاستثمار في الذهب أم العقار؟"),
        ],
        "internal_links_en": [
            ("/finance-wealth/family-budget-plan-en.html", "Gulf Family Budget: Smart Salary Split"),
            ("/comparisons/saving-vs-investing-gulf-family-en.html", "Saving vs Investing for Gulf Families"),
            ("/comparisons/gold-vs-real-estate-gulf-family-en.html", "Gold vs Property for Gulf Families"),
        ],
        "hero_webp": "/assets/images/hero-investment-basics-beginners.webp",
        "hero_alt_ar": "رسم توضيحي لادخار واستثمار لأسرة خليجية، جرة عملات ونبتة تنمو",
        "hero_alt_en": "Illustration of saving and investing for Gulf families, coins jar and growing plant",
        "title_seo_ar": "استثمار المبتدئ الخليجي: دليل عملي",
        "title_seo_en": "Gulf Beginner Investing Guide",
    },
    {
        "id": "A-01-2",
        "draft_ar": DRAFTS / "task01/family-budget-plan.md",
        "draft_en": DRAFTS / "task01/family-budget-plan-en.md",
        "out_ar": ROOT / "finance-wealth/family-budget-plan.html",
        "out_en": ROOT / "finance-wealth/family-budget-plan-en.html",
        "section_ar": "💰 مالية وثروة",
        "section_en": "💰 Finance & Wealth",
        "tool_cta_ar": "/tools/monthly-budget.html",
        "tool_cta_en": "/tools/monthly-budget.html",
        "tool_label_ar": "حاسبة الميزانية الشهرية",
        "tool_label_en": "Monthly Budget Calculator",
        "internal_links_ar": [
            ("/finance-wealth/investment-basics-beginners.html", "أساسيات الاستثمار للمبتدئين"),
            ("/tools/savings-calculator.html", "حاسبة الادخار"),
            ("/finance.html", "قسم المالية"),
        ],
        "internal_links_en": [
            ("/finance-wealth/investment-basics-beginners-en.html", "Investment Basics for Beginners"),
            ("/tools/savings-calculator.html", "Savings Calculator"),
            ("/finance.html", "Finance Hub"),
        ],
        "hero_webp": "/assets/images/hero-family-budget-plan.webp",
        "hero_alt_ar": "رسم توضيحي لميزانية الأسرة الخليجية، محفظة ودفتر ميزانية",
        "hero_alt_en": "Illustration of Gulf family budgeting, wallet and budget notebook",
        "title_seo_ar": "ميزانية الأسرة الخليجية: خطة عملية",
        "title_seo_en": "Gulf Family Budget Guide",
    },
    {
        "id": "A-07-1",
        "draft_ar": DRAFTS / "task07/rent-vs-buy-gulf-family.md",
        "draft_en": DRAFTS / "task07/rent-vs-buy-gulf-family-en.md",
        "out_ar": ROOT / "real-estate/rent-vs-buy-gulf-family.html",
        "out_en": ROOT / "real-estate/rent-vs-buy-gulf-family-en.html",
        "section_ar": "🏠 عقار",
        "section_en": "🏠 Real Estate",
        "tool_cta_ar": "/tools/mortgage-calculator.html",
        "tool_cta_en": "/tools/mortgage-calculator.html",
        "tool_label_ar": "حاسبة الرهن العقاري",
        "tool_label_en": "Mortgage Calculator",
        "internal_links_ar": [
            ("/finance-wealth/family-budget-plan.html", "ميزانية الأسرة الخليجية"),
            ("/blog/emergency-fund-calculator-guide.html", "دليل صندوق الطوارئ"),
            ("/finance-wealth/investment-basics-beginners.html", "أساسيات الاستثمار للمبتدئين"),
        ],
        "internal_links_en": [
            ("/finance-wealth/family-budget-plan-en.html", "Gulf Family Budget Guide"),
            ("/blog/emergency-fund-calculator-guide-en.html", "Emergency Fund Guide"),
            ("/finance-wealth/investment-basics-beginners-en.html", "Investment Basics for Beginners"),
        ],
        "hero_webp": "/assets/images/hero-rent-vs-buy-gulf-family.webp",
        "hero_alt_ar": "رسم توضيحي لمقارنة الإيجار والتملك لأسرة خليجية، منزل ومفتاح",
        "hero_alt_en": "Illustration comparing rent vs buy for Gulf families, home and key",
        "title_seo_ar": "إيجار أم تملّك للأسرة الخليجية؟",
        "title_seo_en": "Rent vs Buy for Gulf Families",
    },
]

FAQ_MARKERS = (
    "## الأسئلة الشائعة",
    "## أسئلة شائعة",
    "## Frequently Asked Questions",
    "## Common Questions",
    "## FAQ",
)

EM_DASH = "\u2014"
TITLE_SUFFIX = " | DOTFORLIFE"
MAX_TITLE_LEN = 60
DISCLAIMER_KEYS = ("Disclaimer:", "إخلاء مسؤولية", "Sharia Disclaimer", "إخلاء مالي")


def seo_page_title(h1: str, cfg: dict, lang: str) -> str:
    key = "title_seo_en" if lang == "en" else "title_seo_ar"
    base = cfg.get(key) or h1
    limit = MAX_TITLE_LEN - len(TITLE_SUFFIX)
    if len(base) > limit:
        chunk = base[:limit]
        if " " in chunk:
            chunk = chunk.rsplit(" ", 1)[0]
        base = chunk.rstrip("?.،,")
    title = f"{base}{TITLE_SUFFIX}"
    if len(title) > MAX_TITLE_LEN:
        raise SystemExit(f"Title gate failed: {len(title)} chars > {MAX_TITLE_LEN}: {title}")
    return title


def assert_title_gate(page: str, out_path: Path) -> None:
    m = re.search(r"<title>(.*?)</title>", page)
    if not m:
        raise SystemExit(f"Title gate failed: no <title> in {out_path.name}")
    t = m.group(1)
    if len(t) > MAX_TITLE_LEN:
        raise SystemExit(f"Title gate failed: {len(t)} chars in {out_path.relative_to(ROOT)}: {t}")
    if t.endswith(TITLE_SUFFIX) and t[:-len(TITLE_SUFFIX)].endswith(" "):
        raise SystemExit(f"Title gate failed: truncated mid-token in {out_path.name}")


def extract_disclaimer_html(md: str) -> str:
    lines = md.splitlines()
    blocks: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith(">") and any(k in lines[i] for k in DISCLAIMER_KEYS):
            paras: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                paras.append(lines[i].lstrip("> ").strip())
                i += 1
            blocks.append(f'<div class="tip"><p>{inline_md(" ".join(paras))}</p></div>')
        else:
            i += 1
    return "\n".join(blocks)


def parse_post_faq_html(md: str) -> str:
    """Content after FAQ block (takeaway, etc.) excluding Q&A pairs."""
    _, faq_block = split_at_faq(md)
    if not faq_block:
        return ""
    body = faq_block.split("\n", 1)[1] if "\n" in faq_block else ""
    parts = re.split(r"\n\*\*(.+?)\*\*\n", body)
    tail = parts[-1] if len(parts) >= 3 else ""
    tail = re.split(r"\n---\n|\nSources:", tail)[0].strip()
    if not tail:
        return ""
    out: list[str] = []
    i = 0
    lines = tail.splitlines()
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith(">") and any(k in line for k in DISCLAIMER_KEYS):
            while i < len(lines) and lines[i].startswith(">"):
                i += 1
            continue
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("**") and line.endswith("**"):
            out.append(f"<p><strong>{html.escape(line.strip('*'))}</strong></p>")
            i += 1
            continue
        if not line.startswith(("-", "*", "|")):
            out.append(f"<p>{inline_md(line.strip())}</p>")
        i += 1
    return "\n".join(out)


def assert_cf4_gate(content: str, out_path: Path) -> None:
    """C-F4: built HTML must contain zero em dashes (—)."""
    count = content.count(EM_DASH)
    if count:
        rel = out_path.relative_to(ROOT)
        raise SystemExit(f"C-F4 gate failed: {count} em dash(es) in {rel}")


def validate_build_map() -> None:
    for cfg in BUILD_MAP:
        for key in ("hero_alt_ar", "hero_alt_en"):
            alt = cfg.get(key, "")
            if EM_DASH in alt:
                raise SystemExit(f"C-F4 gate failed: em dash in {cfg['id']} {key}")


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s.strip())
    return s[:80] or "section"


def split_at_faq(md: str) -> tuple[str, str | None]:
    for marker in FAQ_MARKERS:
        if marker in md:
            head, tail = md.split(marker, 1)
            return head, marker + tail
    upper = md.upper()
    for marker in FAQ_MARKERS:
        idx = upper.find(marker.upper())
        if idx != -1:
            return md[:idx], md[idx:]
    return md, None


def parse_faq(md: str) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    _, faq_block = split_at_faq(md)
    if not faq_block:
        return faqs
    block = faq_block.split("\n", 1)[1] if "\n" in faq_block else ""
    block = re.split(r"\n## ", block, maxsplit=1)[0]
    parts = re.split(r"\n\*\*(.+?)\*\*\n", block)
    if len(parts) < 3:
        return faqs
    for i in range(1, len(parts), 2):
        q = parts[i].strip()
        a = parts[i + 1].strip().split("\n\n")[0].strip()
        if q and a:
            faqs.append((q, a))
    return faqs


def md_body_html(md: str, lang: str) -> tuple[str, str]:
    """Convert main markdown body (before FAQ) to HTML."""
    cut, _ = split_at_faq(md)
    cut = re.split(r"\n---\n|\nSources:", cut)[0]
    lines = cut.splitlines()
    out: list[str] = []
    i = 0
    title = ""
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        i = 1
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("## "):
            h = line[3:].strip()
            hid = slugify(h)
            out.append(f'<h2 id="{html.escape(hid)}">{html.escape(h)}</h2>')
            i += 1
            continue
        if line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.startswith("|"):
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].startswith("|"):
                row = [c.strip() for c in lines[i].strip("|").split("|")]
                if not all(re.match(r"^[-:\s]+$", c) for c in row):
                    rows.append(row)
                i += 1
            if rows:
                out.append('<div class="table-wrap"><table>')
                for ri, row in enumerate(rows):
                    tag = "th" if ri == 0 else "td"
                    out.append("<tr>" + "".join(f"<{tag}>{inline_md(c)}</{tag}>" for c in row) + "</tr>")
                out.append("</table></div>")
            continue
        if re.match(r"^\d+\.\s", line):
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i]):
                out.append(f"<li>{inline_md(lines[i].split('.', 1)[1].strip())}</li>")
                i += 1
            out.append("</ol>")
            continue
        if line.startswith("- ") or line.startswith("* "):
            out.append("<ul>")
            while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("* ")):
                out.append(f"<li>{inline_md(lines[i][2:].strip())}</li>")
                i += 1
            out.append("</ul>")
            continue
        if line.startswith(">"):
            paras = []
            while i < len(lines) and lines[i].startswith(">"):
                paras.append(lines[i].lstrip("> ").strip())
                i += 1
            out.append(f'<div class="tip"><p>{inline_md(" ".join(paras))}</p></div>')
            continue
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "-", "*", "|", ">")) and not re.match(r"^\d+\.", lines[i]):
            para_lines.append(lines[i])
            i += 1
        out.append(f"<p>{inline_md(' '.join(para_lines))}</p>")
    return title, "\n".join(out)


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text


def faq_html(faqs: list[tuple[str, str]]) -> str:
    if not faqs:
        return ""
    parts = ['<h2 id="faq">أسئلة شائعة</h2>' if any("\u0600" <= c <= "\u06FF" for c in faqs[0][0]) else '<h2 id="faq">FAQ</h2>']
    for q, a in faqs:
        parts.append(f"<h3>{html.escape(q)}</h3><p>{inline_md(a)}</p>")
    return "\n".join(parts)


def schema_json(
    title: str,
    desc: str,
    url: str,
    faqs: list[tuple[str, str]],
    lang: str,
    image_url: str | None = None,
) -> str:
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc[:300],
        "author": {"@type": "Organization", "name": "DOTFORLIFE" if lang == "en" else "دوت فور لايف"},
        "datePublished": date.today().isoformat(),
        "dateModified": date.today().isoformat(),
        "mainEntityOfPage": url,
    }
    if image_url:
        article["image"] = image_url
    blocks = [json.dumps(article, ensure_ascii=False)]
    if faqs:
        fq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faqs
            ],
        }
        blocks.append(json.dumps(fq, ensure_ascii=False))
    return "\n".join(f'<script type="application/ld+json">{b}</script>' for b in blocks)


def build_page(cfg: dict, draft_path: Path, out_path: Path, lang: str) -> None:
    md = draft_path.read_text(encoding="utf-8")
    title, body = md_body_html(md, lang)
    faqs = parse_faq(md)
    if faqs:
        body += "\n" + faq_html(faqs)
    disclaimer = extract_disclaimer_html(md)
    if disclaimer and disclaimer not in body:
        body += "\n" + disclaimer
    post_faq = parse_post_faq_html(md)
    if post_faq:
        body += "\n" + post_faq

    is_en = lang == "en"
    canonical = f"https://dotforlife.com/{out_path.relative_to(ROOT).as_posix()}"
    href_ar = f"https://dotforlife.com/{cfg['out_ar'].relative_to(ROOT).as_posix()}"
    href_en = f"https://dotforlife.com/{cfg['out_en'].relative_to(ROOT).as_posix()}"
    desc = re.sub(r"\s+", " ", md.split("\n\n")[1 if md.startswith("#") else 0][:155])
    section = cfg["section_en" if is_en else "section_ar"]
    lang_link = cfg["out_en" if is_en else "out_ar"].name
    lang_label = "🌐 English" if not is_en else "🌐 عربي"
    links = cfg["internal_links_en" if is_en else "internal_links_ar"]
    tool = cfg["tool_cta_en" if is_en else "tool_cta_ar"]
    tool_label = cfg["tool_label_en" if is_en else "tool_label_ar"]
    read_also = "اقرأ أيضاً:" if not is_en else "Read also:"
    cta_tools = "🧮 أدوات مساعدة:" if not is_en else "🧮 Helpful tools:"
    share = "شارك:" if not is_en else "Share:"
    footer = "© 2026 دوت فور لايف - للمعرفة والعافية" if not is_en else "© 2026 DOTFORLIFE"

    internal_p = " · ".join(f'<a href="{u}">{html.escape(l)}</a>' for u, l in links)
    hero_webp = cfg.get("hero_webp", "")
    hero_alt = cfg.get("hero_alt_en" if is_en else "hero_alt_ar", title)
    hero_abs = f"https://dotforlife.com{hero_webp}" if hero_webp else None
    schema = schema_json(title, desc, canonical, faqs, lang, hero_abs)
    page_title = seo_page_title(title, cfg, lang)
    hero_img = ""
    og_image = ""
    if hero_webp:
        og_image = f'<meta property="og:image" content="{hero_abs}">'
        hero_img = (
            f'<figure class="hero"><img src="{hero_webp}" alt="{html.escape(hero_alt)}" '
            f'width="1200" height="750" loading="eager" fetchpriority="high"></figure>'
        )

    page = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'ltr' if is_en else 'rtl'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(desc[:155])}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ar" href="{href_ar}">
<link rel="alternate" hreflang="en" href="{href_en}">
{og_image}
<script src="/scripts/lang-redirect.js?v=20260620"></script>
{schema}
<style>
body{{font-family:'Almarai','Segoe UI',sans-serif;background:#FAF8F4;color:#222;line-height:1.9;padding:20px}}
.container{{max-width:800px;margin:0 auto;background:#fff;border-radius:18px;padding:2.5rem 2rem;box-shadow:0 2px 20px rgba(5,66,65,.06)}}
h1{{font-size:26px;color:#054241;margin-bottom:.5rem;line-height:1.4}}
h2{{font-size:20px;color:#054241;margin:1.8rem 0 .8rem;border-{'left' if is_en else 'right'}:4px solid #6abfb8;padding-{'left' if is_en else 'right'}:12px}}
h3{{font-size:16px;color:#054241;margin:1.2rem 0 .5rem}}
p{{margin-bottom:1rem;color:#444;font-size:15px}}
ul,ol{{margin:0 1.2rem 1rem;color:#444;font-size:15px}}
li{{margin-bottom:.4rem}}
.tip{{background:#e8f6f5;border-{'left' if is_en else 'right'}:4px solid #6abfb8;padding:1rem 1.2rem;border-radius:10px;margin:1.2rem 0}}
.table-wrap{{overflow-x:auto;margin:1rem 0}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th{{background:#054241;color:#fff;padding:10px 12px}}
td{{padding:10px 12px;border-bottom:1px solid #eee}}
.meta{{font-size:13px;color:#888;margin-bottom:1.5rem;display:flex;gap:12px;flex-wrap:wrap}}
.meta span{{background:#f0f4f3;padding:3px 12px;border-radius:999px}}
.cta{{background:linear-gradient(135deg,#054241,#0a6b63);color:#fff;border-radius:12px;padding:1.2rem 1.5rem;margin:1.5rem 0;text-align:center}}
.cta a{{color:#ffd54f;font-weight:700;text-decoration:none}}
.lang-switch{{text-align:{'right' if is_en else 'left'};margin-bottom:1rem}}
.lang-switch a{{display:inline-block;background:#054241;color:#fff;padding:6px 16px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:700}}
.footer-art{{font-size:12px;color:#999;text-align:center;margin-top:2rem}}
.hero{{margin:0 0 1.5rem;border-radius:14px;overflow:hidden}}
.hero img{{display:block;width:100%;height:auto}}
</style>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="lang-switch"><a href="{html.escape(lang_link)}">{lang_label}</a></div>
<h1>{html.escape(title)}</h1>
<div class="meta"><span>{html.escape(section)}</span><span>📅 {date.today().strftime('%Y-%m-%d')}</span></div>
{hero_img}
{body}
<div class="cta"><strong>{cta_tools}</strong> <a href="{tool}">{html.escape(tool_label)}</a></div>
<p>{read_also} {internal_p}</p>
<div class="footer-art">{footer}</div>
</div>
</body>
</html>
"""
    BACKUP.mkdir(parents=True, exist_ok=True)
    assert_cf4_gate(page, out_path)
    assert_title_gate(page, out_path)
    if out_path.exists():
        shutil.copy2(out_path, BACKUP / out_path.name)
    out_path.write_text(page, encoding="utf-8")
    wc = len(re.findall(r"\w+", md, re.UNICODE))
    print(f"  ✅ {cfg['id']} {lang}: {out_path.name} (~{wc} words draft)")


def main() -> None:
    validate_build_map()
    ids = sys.argv[1:] if len(sys.argv) > 1 else [c["id"] for c in BUILD_MAP]
    for cfg in BUILD_MAP:
        if cfg["id"] not in ids and ids != ["all"]:
            continue
        print(f"Building {cfg['id']}…")
        build_page(cfg, cfg["draft_ar"], cfg["out_ar"], "ar")
        build_page(cfg, cfg["draft_en"], cfg["out_en"], "en")


if __name__ == "__main__":
    main()
