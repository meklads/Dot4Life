#!/usr/bin/env python3
"""Batch site fixes — links, redirects, SEO, assets refs. Skips blog/ and assets/queue/."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'blog', 'assets/queue', 'tools/_finance_backup', '.git', '__pycache__'}

LINK_REPLACEMENTS = [
    ('/tools/savings-calculator.html', '/tools/savings-goal.html'),
    ('tools/savings-calculator.html', 'tools/savings-goal.html'),
    ('/tools/budget-planner.html', '/tools/monthly-budget.html'),
    ('tools/budget-planner.html', 'tools/monthly-budget.html'),
    ('/tools/daily-planner.html', '/daily-planner.html'),
    ('tools/daily-planner.html', 'daily-planner.html'),
    ('/tools/watering-schedule.html', '/tools/plant-watering.html'),
    ('tools/watering-schedule.html', 'tools/plant-watering.html'),
    ('/tools/time-calculator.html', '/tools/pomodoro.html'),
    ('tools/time-calculator.html', 'tools/pomodoro.html'),
    ('/tools/task-manager.html', '/tasks.html'),
    ('tools/task-manager.html', 'tasks.html'),
    ('/tools/productivity-score.html', '/tools/pomodoro.html'),
    ('tools/productivity-score.html', 'tools/pomodoro.html'),
    ('/tools/plant-guide.html', '/guides/indoor-plants-saudi-arabia.html'),
    ('tools/plant-guide.html', 'guides/indoor-plants-saudi-arabia.html'),
    ('/tools/rent-vs-buy-calculator.html', '/real-estate/rent-vs-buy-gulf-family.html'),
    ('tools/rent-vs-buy-calculator.html', 'real-estate/rent-vs-buy-gulf-family.html'),
    ('/comparisons/rent-vs-buy-saudi-guide-2026.html', '/blog/rent-vs-buy-saudi-guide-2026.html'),
    ('/blog/indoor-plants-gulf-guide.html', '/guides/indoor-plants-saudi-arabia.html'),
    ('/blog/outdoor-plants-gulf-climate.html', '/guides/indoor-plants-saudi-arabia.html'),
    ('/blog/time-management-gulf-families.html', '/productivity/family-time-management-en.html'),
    ('/blog/family-routines-gulf.html', '/life-guide.html?g=evening-routine'),
    ('/blog/digital-minimalism-families-en.html', '/blog/digital-minimalism-families.html'),
    ('/islamic-hajj-umrah/dhu-al-hijjah-tips.html', '/islamic-hajj-umrah/daily-adhkar-family-guide.html'),
    ('/islamic-hajj-umrah/children-ramadan-prep.html', '/guides/ramadan-nutrition-guide.html'),
    ('https://www.dotforlife.com/', 'https://dotforlife.com/'),
    ('href="/privacy.html"', 'href="/privacy-policy.html"'),
    ('href="privacy.html"', 'href="/privacy-policy.html"'),
    ('./site/system/sec1.html', './system/sec1.html'),
    ('./site/system/sec2.html', './system/sec2.html'),
    ('./site/system/sec3.html', './system/sec3.html'),
    ('./site/system/sec4.html', './system/sec4.html'),
    ('./site/system/sec5.html', './system/sec5.html'),
    ('./site/system/sec6.html', './system/sec6.html'),
    ('./site/system/brand-guide.html', './system/brand-guide.html'),
    ('https://dotforlife.com/og/d4l1.webp', 'https://dotforlife.com/d4l1.webp'),
    ('https://dotforlife.com/og/og-default.png', 'https://dotforlife.com/d4l1.webp'),
    ('content="https://dotforlife.com/og/plants.jpg"', 'content="https://dotforlife.com/d4l1.webp"'),
]

def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith('blog/'):
        return True
    for s in SKIP_DIRS:
        if rel.startswith(s):
            return True
    return False

def fix_main_css(content: str) -> str:
    # Remove dead main.css link (global.css already loaded on these pages)
    return re.sub(
        r'\s*<link rel="stylesheet" href="/styles/main\.css"[^>]*/>\s*',
        '\n',
        content,
    )

def fix_robots_meta(content: str) -> str:
    return content.replace(
        '<meta name="robots" content="noindex">/>',
        '<meta name="robots" content="noindex, follow"/>',
    )

def fix_plants_noindex(content: str, path: Path) -> str:
    if path.name != 'plants.html':
        return content
    return content.replace(
        '<meta name="robots" content="noindex, nofollow">',
        '<meta name="robots" content="index, follow">',
    )

def main():
    changed = []
    for path in ROOT.rglob('*.html'):
        if should_skip(path):
            continue
        text = path.read_text(encoding='utf-8')
        orig = text
        for old, new in LINK_REPLACEMENTS:
            text = text.replace(old, new)
        text = fix_main_css(text)
        text = fix_robots_meta(text)
        text = fix_plants_noindex(text, path)
        if text != orig:
            path.write_text(text, encoding='utf-8')
            changed.append(path.relative_to(ROOT))
    print(f'Updated {len(changed)} files')
    for p in sorted(changed)[:40]:
        print(f'  {p}')
    if len(changed) > 40:
        print(f'  ... and {len(changed) - 40} more')

if __name__ == '__main__':
    main()
