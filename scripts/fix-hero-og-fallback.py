#!/usr/bin/env python3
"""C-F6: Add og:image fallback for archive pages missing hero image."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    "peace-capsules", "featured-stories", "guides", "blog",
    "comparisons", "travel", "productivity", "fitness",
]
DEFAULT = "https://dotforlife.com/d4l1.webp"
HERO_RE = re.compile(
    r'(hero|banner|featured)[-_][^"\']*\.(webp|svg|jpg|png)|property="og:image"',
    re.I,
)


def fix(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    if HERO_RE.search(html):
        return False
    tag = f'<meta property="og:image" content="{DEFAULT}" />'
    if re.search(r'<meta[^>]+property="og:type"', html, re.I):
        html = re.sub(
            r'(<meta[^>]+property="og:type"[^>]*>)',
            tag + "\n\\1",
            html,
            count=1,
            flags=re.I,
        )
    else:
        html = html.replace("</head>", tag + "\n</head>", 1)
    path.write_text(html, encoding="utf-8")
    return True


def main() -> None:
    done = 0
    for sec in SECTIONS:
        d = ROOT / sec
        if not d.is_dir():
            continue
        for fp in sorted(d.glob("*.html")):
            if fix(fp):
                done += 1
                print(f"  ✅ og:image → {fp.relative_to(ROOT)}")
    print(f"\nC-F6 fallback: {done} pages")


if __name__ == "__main__":
    main()
