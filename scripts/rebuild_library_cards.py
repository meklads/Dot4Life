#!/usr/bin/env python3
"""One-shot: rebuild library.html compact cards from existing markup."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "library.html"

ICONS = {
    "health": '<svg class="lib-card-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "finance": '<svg class="lib-card-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="6" width="20" height="14" rx="2"/><path d="M2 10h20"/><circle cx="16" cy="14" r="1"/></svg>',
    "islamic": '<svg class="lib-card-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
    "travel": '<svg class="lib-card-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>',
}

CARD_RE = re.compile(
    r'<a href="([^"]+)" class="lib-card" data-cat="([^"]+)">\s*'
    r'<p class="lib-card-kicker">.*?</p>\s*'
    r'(<h3 class="lib-card-title">.*?</h3>)\s*'
    r'<p class="lib-card-desc"><span class="en">([^<]*)</span><span class="ar">([^<]*)</span></p>\s*'
    r'<span class="lib-card-arrow">.*?</span>\s*'
    r'</a>',
    re.DOTALL,
)


def rebuild_card(m: re.Match) -> str:
    href, cat, title_html, tip_en, tip_ar = m.groups()
    icon = ICONS.get(cat, ICONS["health"])
    return (
        f'<a href="{href}" class="lib-card" data-cat="{cat}" '
        f'data-tip-en="{tip_en.strip()}" data-tip-ar="{tip_ar.strip()}">\n'
        f'        {icon}\n'
        f'        {title_html}\n'
        f'      </a>'
    )


def main() -> None:
    text = HTML.read_text(encoding="utf-8")
    new_text, n = CARD_RE.subn(rebuild_card, text)
    if n != 22:
        raise SystemExit(f"Expected 22 cards, rebuilt {n}")
    HTML.write_text(new_text, encoding="utf-8")
    print(f"Rebuilt {n} lib-card entries")


if __name__ == "__main__":
    main()
