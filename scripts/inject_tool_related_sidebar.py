#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inject category-related tool sidebar beside calculator workspace."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "scripts" / "tools_catalog.json"
FLAGSHIP_VER = "20260709a"
MAX_RELATED = 6


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def slug_from_path(path: Path) -> str:
    return path.stem


def find_category(slug: str, catalog: dict) -> str | None:
    for cat, data in catalog["categories"].items():
        if any(t["slug"] == slug for t in data["tools"]):
            return cat
    return None


def related_tools(slug: str, category: str, catalog: dict) -> list[dict]:
    tools = catalog["categories"][category]["tools"]
    out = [t for t in tools if t["slug"] != slug]
    return out[:MAX_RELATED]


def render_sidebar(slug: str, category: str, catalog: dict) -> str:
    meta = catalog["categories"][category]
    links = related_tools(slug, category, catalog)
    if not links:
        return ""
    items = "\n".join(
        f'      <a href="/tools/{t["slug"]}.html" class="tool-related-link">'
        f'<span class="en">{t["en"]}</span><span class="ar">{t["ar"]}</span></a>'
        for t in links
    )
    return f"""  <aside class="tool-related-aside" aria-label="Related tools">
    <div class="tool-related-module">
      <h3 class="tool-related-h"><span class="en">{meta["heading_en"]}</span><span class="ar">{meta["heading_ar"]}</span></h3>
      <nav class="tool-related-links">
{items}
      </nav>
      <a href="/library.html#{meta["library_anchor"]}" class="tool-related-all"><span class="en">All tools →</span><span class="ar">← كل الأدوات</span></a>
    </div>
  </aside>"""


def extract_div_block(html: str, start: int) -> tuple[str, int]:
    """Return (block including outer div, end index) starting at `<div`."""
    tag_end = html.find(">", start) + 1
    depth = 1
    pos = tag_end
    while depth > 0 and pos < len(html):
        next_open = html.find("<div", pos)
        next_close = html.find("</div>", pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    return html[start:pos], pos


def remove_existing_layout(html: str) -> str:
    """Idempotent: strip prior wrapper if re-running."""
    if "tool-calc-layout" not in html:
        return html
    pattern = re.compile(
        r'<div class="tool-calc-layout">\s*'
        r'(<div class="tool-workspace[^"]*">.*?</div>)\s*'
        r'<aside class="tool-related-aside".*?</aside>\s*'
        r"</div>",
        re.S,
    )
    return pattern.sub(r"\1", html)


def inject_sidebar(html: str, sidebar: str) -> str:
    if not sidebar:
        return html
    html = remove_existing_layout(html)
    if "tool-related-aside" in html:
        return html
    idx = html.find('<div class="tool-workspace')
    if idx == -1:
        return html
    block, end = extract_div_block(html, idx)
    wrapped = f'<div class="tool-calc-layout">\n{block}\n{sidebar}\n</div>'
    return html[:idx] + wrapped + html[end:]


def bump_flagship_css(html: str) -> str:
    return re.sub(
        r"/styles/tools-flagship\.css\?v=[^\"']+",
        f"/styles/tools-flagship.css?v={FLAGSHIP_VER}",
        html,
        count=1,
    )


def patch_file(path: Path, catalog: dict) -> bool:
    slug = slug_from_path(path)
    category = find_category(slug, catalog)
    if not category:
        return False
    sidebar = render_sidebar(slug, category, catalog)
    html = path.read_text(encoding="utf-8")
    new_html = inject_sidebar(html, sidebar)
    new_html = bump_flagship_css(new_html)
    if new_html != html:
        path.write_text(new_html, encoding="utf-8")
        return True
    return False


def main() -> None:
    catalog = load_catalog()
    changed = 0
    for cat in catalog["categories"].values():
        for tool in cat["tools"]:
            path = ROOT / "tools" / f"{tool['slug']}.html"
            if not path.exists():
                print(f"SKIP missing {path.name}")
                continue
            if patch_file(path, catalog):
                changed += 1
                print(f"OK {path.name}")
            else:
                print(f"-- {path.name} (no change)")
    print(f"Done: {changed} files updated")


if __name__ == "__main__":
    main()
