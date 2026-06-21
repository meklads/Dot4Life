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
    },
]


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s.strip())
    return s[:80] or "section"


def parse_faq(md: str) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    if "## الأسئلة الشائعة" in md:
        block = md.split("## الأسئلة الشائعة", 1)[1]
    elif "## FAQ" in md.upper():
        block = md.split("## FAQ", 1)[1]
    else:
        return faqs
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
    cut = md
    for marker in ("## الأسئلة الشائعة", "## FAQ"):
        if marker in cut:
            cut = cut.split(marker, 1)[0]
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


def schema_json(title: str, desc: str, url: str, faqs: list[tuple[str, str]], lang: str) -> str:
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
    schema = schema_json(title, desc, canonical, faqs, lang)

    page = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'ltr' if is_en else 'rtl'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title[:58])} | DOTFORLIFE</title>
<meta name="description" content="{html.escape(desc[:155])}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ar" href="{href_ar}">
<link rel="alternate" hreflang="en" href="{href_en}">
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
</style>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
<div class="lang-switch"><a href="{html.escape(lang_link)}">{lang_label}</a></div>
<h1>{html.escape(title)}</h1>
<div class="meta"><span>{html.escape(section)}</span><span>📅 {date.today().strftime('%Y-%m-%d')}</span></div>
{body}
<div class="cta"><strong>{cta_tools}</strong> <a href="{tool}">{html.escape(tool_label)}</a></div>
<p>{read_also} {internal_p}</p>
<div class="footer-art">{footer}</div>
</div>
</body>
</html>
"""
    BACKUP.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        shutil.copy2(out_path, BACKUP / out_path.name)
    out_path.write_text(page, encoding="utf-8")
    wc = len(re.findall(r"\w+", md, re.UNICODE))
    print(f"  ✅ {cfg['id']} {lang}: {out_path.name} (~{wc} words draft)")


def main() -> None:
    ids = sys.argv[1:] if len(sys.argv) > 1 else [c["id"] for c in BUILD_MAP]
    for cfg in BUILD_MAP:
        if cfg["id"] not in ids and ids != ["all"]:
            continue
        print(f"Building {cfg['id']}…")
        build_page(cfg, cfg["draft_ar"], cfg["out_ar"], "ar")
        build_page(cfg, cfg["draft_en"], cfg["out_en"], "en")


if __name__ == "__main__":
    main()
