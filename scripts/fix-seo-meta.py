#!/usr/bin/env python3
"""C-F5: Fix Title≤60, Meta≤155, hreflang pairs on archive content sections."""
from __future__ import annotations

import html as html_lib
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    "blog", "health", "health-pregnancy", "finance-wealth",
    "islamic-hajj-umrah", "real-estate", "travel", "productivity",
    "fitness", "comparisons", "peace-capsules", "featured-stories", "guides",
]
SITE = "https://dotforlife.com"
MAX_META = 155

spec = importlib.util.spec_from_file_location(
    "build_draft", ROOT / "scripts/build-from-approved-draft.py"
)
build = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(build)


def partner_path(path: Path) -> Path | None:
    name = path.name
    if name.endswith("-en.html"):
        return path.with_name(name.replace("-en.html", ".html"))
    if name.endswith("-ar.html"):
        base = name.replace("-ar.html", ".html")
        en = path.with_name(name.replace("-ar.html", "-en.html"))
        if en.exists():
            return en
        return path.with_name(base)
    en = path.with_name(name.replace(".html", "-en.html"))
    if en.exists():
        return en
    ar = path.with_name(name.replace(".html", "-ar.html"))
    if ar.exists():
        return ar
    return None


def fix_title(raw: str) -> str | None:
    t = raw.strip()
    if not t or len(t) <= build.MAX_TITLE_LEN:
        return None
    suffix = build.TITLE_SUFFIX if t.endswith(build.TITLE_SUFFIX) else ""
    base = t[: -len(suffix)] if suffix else t
    limit = build.MAX_TITLE_LEN - len(build.TITLE_SUFFIX) if suffix else build.MAX_TITLE_LEN
    if len(base) > limit:
        chunk = base[:limit]
        if " " in chunk:
            chunk = chunk.rsplit(" ", 1)[0]
        base = chunk.rstrip("?.،,")
    new = f"{base}{suffix}" if suffix else base
    if len(new) > build.MAX_TITLE_LEN:
        new = new[: build.MAX_TITLE_LEN].rsplit(" ", 1)[0].rstrip("?.،,")
        if suffix and not new.endswith(suffix):
            new = f"{new}{suffix}"[: build.MAX_TITLE_LEN]
    return new if new != t else None


def fix_meta(raw: str) -> str | None:
    d = html_lib.unescape(raw.strip())
    if not d:
        return None
    if len(d) <= MAX_META:
        return None
    chunk = d[:MAX_META]
    if " " in chunk:
        chunk = chunk.rsplit(" ", 1)[0]
    chunk = chunk.rstrip("?.،,")
    return chunk if chunk != raw.strip() else None


def hreflang_block(path: Path, partner: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    prel = partner.relative_to(ROOT).as_posix()
    if rel.endswith("-en.html") or prel.endswith("-en.html"):
        en, ar = (rel, prel) if rel.endswith("-en.html") else (prel, rel)
    elif "lang=\"en\"" in path.read_text(encoding="utf-8")[:800]:
        en, ar = rel, prel
    else:
        ar, en = rel, prel
    return (
        f'<link rel="alternate" hreflang="ar-SA" href="{SITE}/{ar}" />\n'
        f'<link rel="alternate" hreflang="en" href="{SITE}/{en}" />\n'
        f'<link rel="alternate" hreflang="x-default" href="{SITE}/{en}" />'
    )


def inject_hreflang(page: str, block: str) -> str:
    if "hreflang" in page:
        return page
    m = re.search(r'<link rel="canonical"[^>]*>', page, re.I)
    if m:
        return page[: m.end()] + "\n" + block + page[m.end() :]
    m = re.search(r"</head>", page, re.I)
    if m:
        return page[: m.start()] + block + "\n" + page[m.start() :]
    return page


def process(path: Path) -> list[str]:
    changes: list[str] = []
    page = path.read_text(encoding="utf-8")
    orig = page

    mt = re.search(r"<title>(.*?)</title>", page, re.S)
    if mt:
        new_t = fix_title(mt.group(1))
        if new_t:
            page = page.replace(f"<title>{mt.group(1)}</title>", f"<title>{new_t}</title>", 1)
            changes.append(f"title→{len(new_t)}")

    md = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', page, re.I)
    if md:
        new_m = fix_meta(md.group(1))
        if new_m:
            page = page.replace(
                md.group(0),
                re.sub(r'content="[^"]*"', f'content="{new_m}"', md.group(0), count=1),
                1,
            )
            changes.append(f"meta→{len(new_m)}")

    if "hreflang" not in page:
        partner = partner_path(path)
        if partner and partner.exists():
            block = hreflang_block(path, partner)
            page = inject_hreflang(page, block)
            changes.append("hreflang")

    if page != orig:
        path.write_text(page, encoding="utf-8")
    return changes


def main() -> None:
    dry = "--dry-run" in sys.argv
    total = fixed = 0
    for sec in SECTIONS:
        d = ROOT / sec
        if not d.is_dir():
            continue
        for fp in sorted(d.glob("*.html")):
            total += 1
            if dry:
                page = fp.read_text(encoding="utf-8")
                mt = re.search(r"<title>(.*?)</title>", page, re.S)
                tl = len(mt.group(1)) if mt else 0
                if tl > 60 or "hreflang" not in page:
                    print(f"  would fix {fp.relative_to(ROOT)} title={tl}")
                continue
            ch = process(fp)
            if ch:
                fixed += 1
                print(f"  ✅ {fp.relative_to(ROOT)}: {', '.join(ch)}")
    print(f"\nC-F5: {fixed}/{total} files updated")


if __name__ == "__main__":
    main()
