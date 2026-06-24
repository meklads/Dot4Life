#!/usr/bin/env python3
"""Apply manifest-approved heroes to existing HTML (closed-loop — no human GO)."""
from __future__ import annotations

import json
import re
import shutil
import sys
import html as html_lib
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "outputs/backups/approved-heroes"
SITE = "https://dotforlife.com"

from image_manifest import (  # noqa: E402
    article_slug_from_path,
    entries_by_slug,
    hero_block,
    image_web_path,
    is_approved,
    load_manifest,
)

SECTIONS = [
    "blog",
    "travel",
    "guides",
    "comparisons",
    "finance-wealth",
    "health",
    "islamic-hajj-umrah",
    "real-estate",
    "featured-stories",
    "peace-capsules",
]


def page_lang(path: Path) -> str:
    if path.name.endswith("-en.html"):
        return "en"
    if path.name.endswith("-ar.html"):
        return "ar"
    html = path.read_text(encoding="utf-8")
    m = re.search(r'<html[^>]+lang=["\'](ar|en)["\']', html, re.I)
    if m:
        return m.group(1).lower()
    return "ar"


def inject_hero(html: str, figure: str) -> str:
    if re.search(r'<figure class="hero">', html):
        html = re.sub(r'<figure class="hero">.*?</figure>\s*', '', html, count=1, flags=re.S)
    if '<article class="article-body">' in html:
        return html.replace(
            '<article class="article-body">',
            '<article class="article-body">\n' + figure + '\n',
            1,
        )
    if '<main class="article-main">' in html:
        return html.replace(
            '<main class="article-main">',
            '<main class="article-main">\n' + figure + '\n',
            1,
        )
    return html.replace("<body>", "<body>\n" + figure, 1)


def set_og_image(html: str, web: str) -> str:
    abs_url = f"{SITE}{web}"
    tag = f'<meta property="og:image" content="{abs_url}">'
    if 'property="og:image"' in html:
        return re.sub(r'<meta property="og:image" content="[^"]*">', tag, html, count=1)
    return html.replace("</head>", tag + "\n</head>", 1)


def patch_schema_image(html: str, abs_url: str) -> str:
    def repl(m: re.Match) -> str:
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            return m.group(0)
        if data.get("@type") == "Article":
            data["image"] = abs_url
            data["dateModified"] = date.today().isoformat()
            return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'
        return m.group(0)

    return re.sub(
        r'<script type="application/ld\+json">(.*?)</script>',
        repl,
        html,
        flags=re.S,
    )


def patch_banner(page: str, web: str, alt: str) -> str:
    if "article-banner-img" not in page:
        return page
    esc = html_lib.escape(alt, quote=True)

    def repl(m: re.Match) -> str:
        tag = m.group(0)
        tag = re.sub(r'src="[^"]*"', f'src="{web}"', tag, count=1)
        if re.search(r'\balt="', tag):
            tag = re.sub(r'alt="[^"]*"', f'alt="{esc}"', tag, count=1)
        else:
            tag = tag.replace("<img ", f'<img alt="{esc}" ', 1)
        return tag

    return re.sub(r'<img[^>]*class="article-banner-img"[^>]*>', repl, page, count=1)


def apply_path(path: Path, entry: dict) -> bool:
    lang = page_lang(path)
    figure, web, alt = hero_block(entry, lang, eager=True)
    text = path.read_text(encoding="utf-8")
    slug = article_slug_from_path(path)
    if slug != entry["article_slug"]:
        return False
    new = patch_banner(text, web, alt)
    new = inject_hero(new, figure)
    new = set_og_image(new, web)
    new = patch_schema_image(new, f"{SITE}{web}")
    if new == text:
        return False
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, BACKUP / path.name)
    path.write_text(new, encoding="utf-8")
    return True


def main() -> None:
    by_slug = entries_by_slug(load_manifest())
    approved = {k: v for k, v in by_slug.items() if is_approved(v)}
    if not approved:
        print("No approved manifest entries.")
        return
    done: list[str] = []
    for sec in SECTIONS:
        d = ROOT / sec
        if not d.is_dir():
            continue
        for fp in sorted(d.glob("*.html")):
            if ".bak" in fp.name:
                continue
            slug = article_slug_from_path(fp)
            entry = approved.get(slug)
            if not entry:
                continue
            if apply_path(fp, entry):
                done.append(fp.relative_to(ROOT).as_posix())
                print(f"  ✅ {fp.relative_to(ROOT)}")
    print(f"\nApplied approved heroes: {len(done)} pages")
    if "--strict" in sys.argv:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "build", ROOT / "scripts/build-from-approved-draft.py"
        )
        build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build)
        for rel in done:
            p = ROOT / rel
            page = p.read_text(encoding="utf-8")
            lang = page_lang(p)
            build.assert_build_gates(
                page, lang, p, {"id": "hero-apply"}, None, strict_image=True
            )
            print(f"  G5 strict PASS {rel}")


if __name__ == "__main__":
    main()
