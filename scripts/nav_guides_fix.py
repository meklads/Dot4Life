#!/usr/bin/env python3
"""Add Life Guides nav link + fix city logos + unify global.js cache buster."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'blog/', 'assets/queue/', 'tools/_finance_backup/'}

GUIDES_LI = '''      <li><a href="/life-guide.html"><span class="en">Guides</span><span class="ar">الأدلة</span></a></li>
'''
ANCHOR = '''      <li><a href="library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a></li>
'''
ANCHOR_ABS = '''      <li><a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a></li>
'''
INSERT_AFTER = [
    (ANCHOR, ANCHOR + GUIDES_LI),
    (ANCHOR_ABS, ANCHOR_ABS + GUIDES_LI),
]

def skip(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    return any(rel.startswith(s) for s in SKIP)

def main():
    n = 0
    for path in ROOT.rglob('*.html'):
        if skip(path):
            continue
        text = path.read_text(encoding='utf-8')
        orig = text
        if '/life-guide.html"><span class="en">Guides</span>' not in text:
            for old, new in INSERT_AFTER:
                if old in text and new not in text:
                    text = text.replace(old, new, 1)
        text = text.replace('href="../../logo1-footer.webp"', 'href="/assets/images/logo1-footer.webp"')
        text = text.replace('src="../../logo1-footer.webp"', 'src="/assets/images/logo1-footer.webp"')
        text = text.replace('<span class="en">blog</span>', '<span class="en">Blog</span>')
        if 'scripts/global.js?v=' in text:
            import re
            text = re.sub(r'/scripts/global\.js\?v=[^"\']+', '/scripts/global.js?v=20260619e', text)
        elif '<script src="/scripts/global.js" defer></script>' in text:
            text = text.replace(
                '<script src="/scripts/global.js" defer></script>',
                '<script src="/scripts/global.js?v=20260619e" defer></script>',
            )
        if text != orig:
            path.write_text(text, encoding='utf-8')
            n += 1
    print(f'Nav/assets updated in {n} files')

if __name__ == '__main__':
    main()
