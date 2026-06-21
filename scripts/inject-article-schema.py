#!/usr/bin/env python3
"""C-F3: Add Article JSON-LD to pages that have FAQPage but lack Article schema."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    "travel", "productivity", "fitness", "comparisons",
    "peace-capsules", "featured-stories", "guides", "blog",
]
ARTICLE_RE = re.compile(r'"@type"\s*:\s*"Article"|"@type":"Article"')
FAQ_RE = re.compile(r'"@type"\s*:\s*"FAQPage"|"@type":"FAQPage"')


def page_url(path: Path) -> str:
    return f"https://dotforlife.com/{path.relative_to(ROOT).as_posix()}"


def extract_title(html: str, path: Path) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    if m:
        t = m.group(1).strip()
        t = re.sub(r"\s*\|\s*DOTFORLIFE\s*$", "", t)
        return t[:120]
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()[:120]
    return path.stem.replace("-", " ").title()


def extract_desc(html: str) -> str:
    m = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html, re.I)
    if m:
        return m.group(1).strip()[:300]
    return ""


def extract_image(html: str) -> str:
    m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]*)"', html, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r'<img[^>]+src="([^"]+\.(webp|jpg|png))"', html, re.I)
    if m:
        src = m.group(1)
        if src.startswith("/"):
            return f"https://dotforlife.com{src}"
        return src
    return "https://dotforlife.com/d4l1.webp"


def extract_date(html: str) -> str:
    m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"', html)
    if m:
        return m.group(1)
    return date.today().isoformat()


def article_script(path: Path, html: str) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": extract_title(html, path),
        "description": extract_desc(html),
        "author": {"@type": "Organization", "name": "DOTFORLIFE"},
        "datePublished": extract_date(html),
        "dateModified": date.today().isoformat(),
        "image": extract_image(html),
        "mainEntityOfPage": page_url(path),
    }
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def inject(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if ARTICLE_RE.search(html) or not FAQ_RE.search(html):
        return False
    block = article_script(path, html)
    # Insert before first FAQPage script or before </head>
    m = re.search(
        r'(<script type="application/ld\+json">\s*\{[^<]*"@type"\s*:\s*"FAQPage")',
        html,
        re.I,
    )
    if m:
        html = html[: m.start()] + block + "\n" + html[m.start() :]
    else:
        html = html.replace("</head>", block + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")
    return True


def main() -> None:
    dry = "--dry-run" in sys.argv
    done = 0
    for sec in SECTIONS:
        d = ROOT / sec
        if not d.is_dir():
            continue
        for fp in sorted(d.glob("*.html")):
            html = fp.read_text(encoding="utf-8")
            if ARTICLE_RE.search(html) or not FAQ_RE.search(html):
                continue
            if dry:
                print(f"  would inject Article → {fp.relative_to(ROOT)}")
                continue
            if inject(fp):
                done += 1
                print(f"  ✅ Article → {fp.relative_to(ROOT)}")
    print(f"\nC-F3 batch: {done} pages got Article schema")


if __name__ == "__main__":
    main()
