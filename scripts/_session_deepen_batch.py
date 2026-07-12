#!/usr/bin/env python3
"""Deepen + double-audit helpers for Cursor 100-article quality run."""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _session_double_audit import double_audit, SCRIPTURE

def strip_orphans(html: str) -> str:
    aw = html.find('<div class="article-wrap">')
    if aw < 0:
        aw = html.find('<main')
    if aw < 0:
        return html
    head, rest = html[:aw], html[aw:]
    m = re.search(r'id="mobile-dropdown"[\s\S]*?</div>\s*<!-- ═══ END HEADER ═+ -->\s*', head)
    if not m:
        return html
    suffix = head[m.end():]
    suffix = re.sub(r'<div class="md-controls">[\s\S]*?</div>\s*', '', suffix)
    suffix = re.sub(r'</div>\s*<!-- ═══ END HEADER ═+ -->\s*', '', suffix)
    suffix = re.sub(r'<!-- ═══ END HEADER ═+ -->\s*', '', suffix)
    return head[: m.end()] + suffix + rest

def dedupe_h1(html: str) -> str:
    hs = list(re.finditer(r"<h1[^>]*>.*?</h1>", html, re.S))
    for m in reversed(hs[1:]):
        html = html[: m.start()] + html[m.end() :]
    return html

def set_faq_schema(html: str, faqs: list[tuple[str, str]]) -> str:
    entity = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    block = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entity}
    new_script = (
        '<script type="application/ld+json">'
        + json.dumps(block, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )
    out = []
    i = 0
    found = False
    while True:
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html[i:], re.S)
        if not m:
            out.append(html[i:])
            break
        start, end, raw = i + m.start(), i + m.end(), m.group(1)
        out.append(html[i:start])
        if "FAQPage" in raw:
            try:
                data = json.loads(raw)
            except Exception:
                data = None
            if data and isinstance(data, dict) and data.get("@graph"):
                graph = [n for n in data["@graph"] if n.get("@type") != "FAQPage"]
                if graph:
                    data["@graph"] = graph
                    out.append(
                        '<script type="application/ld+json">'
                        + json.dumps(data, ensure_ascii=False)
                        + "</script>\n"
                    )
                if not found:
                    out.append(new_script)
                    found = True
            elif data and data.get("@type") == "FAQPage":
                if not found:
                    out.append(new_script)
                    found = True
            else:
                if not found:
                    out.append(new_script)
                    found = True
        else:
            out.append(html[start:end])
        i = end
    html2 = "".join(out)
    if not found:
        html2 = html2.replace("</head>", new_script + "\n</head>", 1)
    return html2

def ensure_article_schema(html: str, path: str) -> str:
    if re.search(r'"@type"\s*:\s*"Article"', html):
        return re.sub(r'"dateModified"\s*:\s*"[^"]+"', '"dateModified": "2026-07-12"', html)
    title = re.search(r"<title>(.*?)</title>", html, re.I)
    desc = re.search(r'name="description"\s+content="([^"]*)"', html, re.I)
    canon = re.search(r'rel="canonical"\s+href="([^"]+)"', html, re.I)
    img = re.search(r'property="og:image"\s+content="([^"]+)"', html, re.I)
    headline = (title.group(1).split("|")[0].strip() if title else path)
    art = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": desc.group(1) if desc else headline,
        "author": {"@type": "Organization", "name": "DOTFORLIFE"},
        "datePublished": "2026-06-15",
        "dateModified": "2026-07-12",
        "image": img.group(1) if img else "",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canon.group(1) if canon else f"https://dotforlife.com/{path}",
        },
    }
    return html.replace(
        "</head>",
        '<script type="application/ld+json">'
        + json.dumps(art, ensure_ascii=False)
        + "</script>\n</head>",
        1,
    )

def faq_html(faqs: list[tuple[str, str]], lang: str) -> str:
    title = "أسئلة شائعة" if lang == "ar" else "Frequently Asked Questions"
    bits = [f'<h2 id="faq">{title}</h2>']
    for q, a in faqs:
        bits.append(f'<div class="faq-item">\n<h3>{q}</h3>\n<p>{a}</p>\n</div>')
    return "\n".join(bits)

def extract_faqs(html: str) -> list[tuple[str, str]]:
    pairs = re.findall(
        r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>', html, re.S
    )
    out = []
    for q, a in pairs:
        out.append(
            (re.sub(r"<[^>]+>", "", q).strip(), re.sub(r"<[^>]+>", "", a).strip())
        )
    if out:
        return out
    # bare h3 under FAQ heading
    m = re.search(
        r"<h2[^>]*>[^<]*(أسئلة|الأسئلة الشائعة|Frequently Asked|FAQ)[^<]*</h2>([\s\S]*?)(?=</article>)",
        html,
        re.I,
    )
    if not m:
        return []
    chunk = m.group(2)
    pairs = re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", chunk, re.S)
    return [
        (re.sub(r"<[^>]+>", "", q).strip(), re.sub(r"<[^>]+>", "", a).strip())
        for q, a in pairs
    ]

def scrub_scripture(html: str) -> str:
    html = html.replace("—", " - ")
    html = html.replace("هذه الآية تؤكد", "هذا المعنى يؤكد")
    html = html.replace("ﷺ", "")
    # soften common quote patterns without deleting whole paragraphs blindly
    html = re.sub(
        r"النبي\s*قال\s*[:：]?\s*[«\"].*?[»\"]\s*(\([^)]*\))?",
        "من قيمنا أن نبدأ بالرحمة والعدل في البيت.",
        html,
    )
    html = re.sub(r"سورة\s+\w+", "قراءة قصيرة", html)
    return html

def rebuild_faq(html: str, faqs: list[tuple[str, str]], lang: str) -> str:
    html = re.sub(r'<div class="faq-item">[\s\S]*?</div>\s*', "", html)
    html = re.sub(
        r'<h2[^>]*>[^<]*(أسئلة شائعة|الأسئلة الشائعة|Frequently Asked Questions|\bFAQ\b)[^<]*</h2>\s*',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(r'<div class="faq-answer">[\s\S]*?</div>\s*', "", html)
    if "</article>" in html:
        html = html.replace("</article>", faq_html(faqs, lang) + "\n</article>", 1)
    return set_faq_schema(html, faqs)

def insert_before_faq(html: str, block: str) -> str:
    i = html.find('<h2 id="faq">')
    if i >= 0:
        return html[:i] + block + html[i:]
    return html.replace("</article>", block + "</article>", 1)

def amer_status(path: str) -> tuple[bool, str]:
    r = subprocess.run(
        ["python3", "scripts/amer_gate.py", path], capture_output=True, text=True
    )
    line = next(
        (ln for ln in r.stdout.splitlines() if ln.startswith(("PASS", "FAIL", "WARN"))),
        r.stdout.strip()[:200],
    )
    ok = any(ln.startswith(("PASS", "WARN")) for ln in r.stdout.splitlines()) and not any(
        ln.startswith("FAIL") for ln in r.stdout.splitlines()
    )
    return ok, line

def finish(path: str, n: int | None = None) -> None:
    t = Path(path).read_text(encoding="utf-8")
    t = strip_orphans(t)
    t = scrub_scripture(t)
    t = dedupe_h1(t)
    t = ensure_article_schema(t, path)
    Path(path).write_text(t, encoding="utf-8")
    label = f"{n}" if n is not None else "?"
    print(f"\n=== {label} {path}")
    ok, line = amer_status(path)
    print(line)
    if not ok:
        raise SystemExit(f"amer fail: {path}")
    if not double_audit(path):
        raise SystemExit(f"double fail: {path}")
    print(f"LOCKED {label}")

if __name__ == "__main__":
    for a in sys.argv[1:]:
        finish(a)
