#!/usr/bin/env python3
"""Double-audit gate for content deepen batches (Cursor session helper)."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

try:
    import html5lib
except ImportError:
    html5lib = None

SCRIPTURE = re.compile(
    r"قال النبي|ﷺ|سورة\s+\w+|حديث\s+(صحيح|شريف)|Qur.?an\s+verse|\bhadith\b|آية\s+",
    re.I,
)

def faq_visible(html: str):
    items = re.findall(r'<div class="faq-item">\s*<h3>(.*?)</h3>', html, re.S)
    return [re.sub(r"<[^>]+>", "", x).strip() for x in items]

def faq_schema(html: str):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        raw = m.group(1)
        if "FAQPage" not in raw:
            continue
        data = json.loads(raw)
        return [e.get("name", "").strip() for e in (data.get("mainEntity") or [])]
    return []

def faq_h2_count(html: str) -> int:
    n = 0
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, re.S):
        title = re.sub(r"<[^>]+>", "", m.group(1))
        if re.search(r"أسئلة شائعة|Frequently Asked|\bFAQ\b", title, re.I):
            n += 1
    return n

def orphan_header_fragments(html: str) -> int:
    # orphan md-controls after first mobile-dropdown END HEADER
    m = re.search(r'(id="mobile-dropdown"[\s\S]*?</div>\n<!-- ═══ END HEADER ═+ -->\n)', html)
    if not m:
        return 0
    tail = html[m.end():]
    return len(re.findall(r'\n  <div class="md-controls">', tail.split('<div class="article-wrap">')[0]))

def html5_errs(html: str) -> int:
    if not html5lib:
        return -1
    p = html5lib.HTMLParser(strict=False)
    p.parse(html)
    return sum(1 for e in p.errors if "named-entity" not in str(e).lower())

def audit_once(path: Path, label: str) -> list[str]:
    html = path.read_text(encoding="utf-8")
    fails = []
    vis, sch = faq_visible(html), faq_schema(html)
    if not vis:
        fails.append("no faq-item visible")
    if len(vis) < 5:
        fails.append(f"faq visible <5 ({len(vis)})")
    if len(vis) != len(sch):
        fails.append(f"faq count mismatch vis={len(vis)} sch={len(sch)}")
    elif vis != sch:
        fails.append("faq question text mismatch vis vs schema")
    if faq_h2_count(html) > 1:
        fails.append(f"duplicate FAQ-like H2 ({faq_h2_count(html)})")
    if re.search(r"—", html):
        fails.append("em-dash present")
    if SCRIPTURE.search(html):
        fails.append("scripture/hadith pattern")
    if len(re.findall(r"<h1\b", html, re.I)) != 1:
        fails.append("H1 count != 1")
    if orphan_header_fragments(html):
        fails.append("orphan mobile header fragments")
    e = html5_errs(html)
    if e > 0:
        fails.append(f"html5lib errs={e}")
    # wrong pregnancy hero on non-pregnancy
    if "pregnancy" not in path.name and "hero-pregnancy-nutrition" in html:
        fails.append("wrong pregnancy hero asset referenced")
    print(f"[{label}] {path} :: {'PASS' if not fails else 'FAIL'}")
    for f in fails:
        print("  -", f)
    if not fails:
        print(f"  faq={len(vis)} h2faq={faq_h2_count(html)} html5={e}")
    return fails

def double_audit(path: str) -> bool:
    p = Path(path)
    a = audit_once(p, "AUDIT-1")
    b = audit_once(p, "AUDIT-2")
    ok = not a and not b
    print("DOUBLE:", "PASS" if ok else "FAIL", path)
    return ok

if __name__ == "__main__":
    sys.exit(0 if all(double_audit(a) for a in sys.argv[1:]) else 1)
