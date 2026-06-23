#!/usr/bin/env python3
"""Inject lang-redirect.js on split ar/en article pairs missing it."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANG_REDIRECT = '<script src="/scripts/lang-redirect.js?v=20260625"></script>'
GLOBAL_JS_TARGET = 'v=20260625'
DIRS = [
    'health', 'health-pregnancy', 'finance-wealth', 'islamic-hajj-umrah',
    'real-estate', 'peace-capsules', 'featured-stories', 'comparisons', 'guides', 'blog',
]


def is_split_lang(html: str) -> bool:
    ar = re.search(r'<link[^>]+hreflang="ar"[^>]+href="([^"]+)"', html, re.I)
    en = re.search(r'<link[^>]+hreflang="en"[^>]+href="([^"]+)"', html, re.I)
    if not ar or not en:
        return False
    return ar.group(1).rstrip('/') != en.group(1).rstrip('/')


def inject_lang_redirect(html: str) -> str:
    if 'lang-redirect.js' in html:
        return html
    m = re.search(
        r'(<link[^>]+hreflang="en"[^>]+href="[^"]+"[^>]*>\s*)',
        html,
        re.I,
    )
    if m:
        return html[: m.end()] + LANG_REDIRECT + '\n' + html[m.end() :]
    return html


def bump_global_js(html: str) -> str:
    return re.sub(
        r'(/scripts/global\.js\?)v=[^"]+',
        rf'\1{GLOBAL_JS_TARGET}',
        html,
    )


def patch_file(path: Path) -> list[str]:
    text = path.read_text(encoding='utf-8')
    if not is_split_lang(text):
        return []
    changes = []
    new = inject_lang_redirect(text)
    if new != text:
        changes.append('lang-redirect')
        text = new
    bumped = bump_global_js(text)
    if bumped != text:
        changes.append('global.js')
        text = bumped
    if changes:
        path.write_text(text, encoding='utf-8')
    return changes


def main() -> int:
    touched = 0
    for d in DIRS:
        pdir = ROOT / d
        if not pdir.is_dir():
            continue
        for f in sorted(pdir.glob('*.html')):
            changes = patch_file(f)
            if changes:
                touched += 1
                print(f"  {f.relative_to(ROOT)}: {', '.join(changes)}")
    print(f"Patched {touched} file(s)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
