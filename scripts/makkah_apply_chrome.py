#!/usr/bin/env python3
"""Apply DotForLife global chrome + Makkah subnav to all makkah/*.html pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "partials"
HEADER = (PARTIALS / "makkah-global-header.html").read_text(encoding="utf-8")
SUBNAV = (PARTIALS / "makkah-subnav.html").read_text(encoding="utf-8")
FOOTER = (PARTIALS / "makkah-global-footer.html").read_text(encoding="utf-8")

ACTIVE = {
    "makkah/index.html": "overview",
    "makkah/plan/index.html": "plan",
    "makkah/stay/index.html": "stay",
    "makkah/move/index.html": "move",
    "makkah/experience/index.html": "experience",
    "makkah/tools/index.html": "tools",
    "makkah/guides/index.html": "guides",
    "makkah/tools/makkah-trip-planner/index.html": "tools",
    "makkah/tools/madinah-trip-planner/index.html": "tools",
    "makkah/tools/makkah-to-madinah-planner/index.html": "tools",
    "makkah/tools/hotel-decision/index.html": "tools",
    "makkah/tools/family-elderly-planner/index.html": "tools",
}

SECTION_META = {
    "plan": ("Plan", "خطّط", "Plan your Makkah and Madinah journey with practical guides and trip planners."),
    "stay": ("Stay", "الإقامة", "Decide hotel factors that fit your group before you book."),
    "move": ("Move", "التنقّل", "Organize transfers and getting back to your hotel with less stress."),
    "experience": ("Experience", "التجربة", "Places, presence, and family moments — kept practical."),
    "tools": ("Tools", "الأدوات", "Planners and practical helpers for Makkah and Madinah."),
    "guides": ("Guides", "الأدلة", "Existing DotForLife guides organized for Makkah and Madinah."),
}


def with_active(subnav: str, key: str) -> str:
    pattern = rf'(data-mk="{re.escape(key)}")'
    return re.sub(pattern, rf'\1 aria-current="page"', subnav, count=1)


def ensure_css(html: str) -> str:
    html = re.sub(
        r'makkah-hub\.css\?v=[^"\']+',
        'makkah-hub.css?v=20260917e',
        html,
    )
    # Never inject home.css — its index-nav rules make links white on light pages.
    html = re.sub(
        r'<link rel="stylesheet" href="/styles/home\.css\?v=[^"]+"/>\s*',
        '',
        html,
    )
    html = re.sub(
        r'<link href="https://fonts\.googleapis\.com/css2\?family=Almarai:[^"]+Cormorant[^"]+" rel="stylesheet"/>',
        '<link href="https://fonts.googleapis.com/css2?family=Almarai:wght@400;700;800&display=swap" rel="stylesheet"/>',
        html,
    )
    return html


def set_body(html: str) -> str:
    html = re.sub(
        r'<body class="[^"]*">',
        '<body class="makkah-dest has-subnav">',
        html,
        count=1,
    )
    return html


def replace_chrome(html: str, active: str) -> str:
    header = HEADER
    if active == "overview":
        header = header.replace(
            'href="/makkah/" data-nav="makkah"',
            'href="/makkah/" data-nav="makkah" aria-current="page"',
            1,
        )
    else:
        header = header.replace(
            'href="/makkah/" data-nav="makkah"',
            'href="/makkah/" data-nav="makkah" aria-current="page"',
            1,
        )
    subnav = with_active(SUBNAV, active)

    # Placeholders (hub)
    if "<!--DFL_MAKKAH_HEADER-->" in html:
        html = html.replace("<!--DFL_MAKKAH_HEADER-->", header)
        html = html.replace("<!--DFL_MAKKAH_SUBNAV-->", subnav)
        html = html.replace("<!--DFL_MAKKAH_FOOTER-->", FOOTER)
        return html

    # Remove old mk-topbar + mk-subnav block
    html = re.sub(
        r'<header class="mk-topbar">.*?</header>\s*<nav[^>]*class="mk-subnav"[^>]*>.*?</nav>',
        header + "\n" + subnav,
        html,
        count=1,
        flags=re.S,
    )
    # If only topbar without matching (already replaced partial)
    if 'class="mk-topbar"' in html:
        html = re.sub(r'<header class="mk-topbar">.*?</header>', header, html, count=1, flags=re.S)
    if 'id="mk-subnav"' in html and "mk-subnav-brand" not in html:
        html = re.sub(
            r'<nav[^>]*id="mk-subnav"[^>]*>.*?</nav>',
            subnav,
            html,
            count=1,
            flags=re.S,
        )
    elif 'class="mk-subnav"' in html and "mk-subnav-brand" not in html:
        html = re.sub(
            r'<nav[^>]*class="mk-subnav"[^>]*>.*?</nav>',
            subnav,
            html,
            count=1,
            flags=re.S,
        )

    # Replace mk-footer with global footer (+ contextual)
    if 'class="mk-footer"' in html:
        html = re.sub(r'<footer class="mk-footer">.*?</footer>', FOOTER, html, count=1, flags=re.S)
    elif "<!--DFL_MAKKAH_FOOTER-->" in html:
        html = html.replace("<!--DFL_MAKKAH_FOOTER-->", FOOTER)
    elif 'class="site-footer"' not in html:
        html = html.replace("</body>", FOOTER + "\n</body>")

    return html


def clean_tool_eyebrows(html: str) -> str:
    html = re.sub(
        r'DOTFORLIFE · Makkah · Tool 0[1-5]',
        "Makkah &amp; Madinah",
        html,
    )
    html = re.sub(
        r'دوت فور لايف · مكة · الأداة 0[1-5]',
        "مكة والمدينة",
        html,
    )
    # Footer leftover vertical wording
    html = html.replace("Makkah-vertical tool", "Makkah &amp; Madinah tool")
    html = html.replace("Makkah vertical", "Makkah &amp; Madinah")
    html = html.replace("specialized Makkah-vertical", "Makkah &amp; Madinah")
    html = html.replace("A specialized Makkah-vertical tool inside DOTFORLIFE.", "A Makkah &amp; Madinah tool inside DOTFORLIFE.")
    html = html.replace("أداة ضمن عمود مكة داخل دوت فور لايف.", "أداة ضمن مكة والمدينة داخل دوت فور لايف.")
    html = html.replace("عمود مكة متخصص داخل دوت فور لايف.", "قسم مكة والمدينة داخل دوت فور لايف.")
    html = html.replace("A specialized Makkah vertical inside DOTFORLIFE.", "Makkah &amp; Madinah inside DOTFORLIFE.")
    return html


def inject_breadcrumb(html: str, rel: str) -> str:
    if 'class="mk-breadcrumb"' in html:
        return html
    section = ACTIVE.get(rel)
    if not section or section == "overview":
        return html
    meta = SECTION_META.get(section)
    if not meta:
        return html
    en, ar, _ = meta
    crumb = f'''
<nav class="mk-breadcrumb" aria-label="Breadcrumb">
  <a href="/"><span class="en">Home</span><span class="ar">الرئيسية</span></a>
  <span class="mk-breadcrumb-sep" aria-hidden="true">→</span>
  <a href="/makkah/"><span class="en">Makkah &amp; Madinah</span><span class="ar">مكة والمدينة</span></a>
  <span class="mk-breadcrumb-sep" aria-hidden="true">→</span>
  <span><span class="en">{en}</span><span class="ar">{ar}</span></span>
</nav>
'''
    html = re.sub(
        r'(<main[^>]*>)',
        rf"\1\n{crumb}",
        html,
        count=1,
    )
    return html


def process(path: Path) -> bool:
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    active = ACTIVE.get(rel, "overview")
    original = path.read_text(encoding="utf-8")
    html = original
    html = ensure_css(html)
    html = set_body(html)
    html = replace_chrome(html, active)
    html = clean_tool_eyebrows(html)
    html = inject_breadcrumb(html, rel)
    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main() -> None:
    files = sorted((ROOT / "makkah").rglob("*.html"))
    changed = []
    for f in files:
        if process(f):
            changed.append(str(f.relative_to(ROOT)))
    print(f"updated {len(changed)} files")
    for c in changed:
        print(" -", c)


if __name__ == "__main__":
    main()
