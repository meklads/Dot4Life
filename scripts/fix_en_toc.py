#!/usr/bin/env python3
"""Fix English articles whose table-of-contents sidebar inherited Arabic text/anchors.

DEEPEN edits English pages in place, and the `-en.html` sidebar sometimes keeps the
Arabic TOC (Arabic link text + `#arabic` hrefs that never match the English H2 ids).
This guard rebuilds the TOC from the actual English H2 headings and gives each H2 an
ASCII id, matching the convention produced by scripts/migrate-article-template.py.

Usage:
    python3 scripts/fix_en_toc.py                 # scan + fix all live *-en.html
    python3 scripts/fix_en_toc.py --check         # report only, non-zero exit if dirty
    python3 scripts/fix_en_toc.py blog/foo-en.html [...]   # specific files
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = ("outputs/backups",)
TOC_RE = re.compile(r'<div class="sidebar-module sidebar-toc">.*?</div>', re.S)
H2_RE = re.compile(r'<h2([^>]*)>(.*?)</h2>', re.S)


def is_ascii(s: str) -> bool:
    try:
        s.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def has_arabic(s: str) -> bool:
    return any("\u0600" <= ch <= "\u06ff" for ch in s)


def slugify(text: str) -> str:
    t = re.sub(r"<[^>]+>", "", text)
    t = t.replace("'", "").replace("\u2019", "")
    t = re.sub(r"[^0-9A-Za-z]+", "-", t)
    return t.strip("-")


def fix_text(s: str):
    """Return (new_text, changed)."""
    toc = TOC_RE.search(s)
    if not toc or not has_arabic(toc.group(0)):
        return s, False

    items = []

    def repl_h2(m):
        attrs = m.group(1) or ""
        inner = m.group(2)
        idm = re.search(r'id="([^"]*)"', attrs)
        cur_id = idm.group(1) if idm else None
        if not cur_id or not is_ascii(cur_id):
            new_id = slugify(inner)
            if idm:
                attrs = re.sub(r'id="[^"]*"', f'id="{new_id}"', attrs)
            else:
                attrs = (attrs + f' id="{new_id}"') if attrs else f' id="{new_id}"'
            cur_id = new_id
        items.append((cur_id, re.sub(r"<[^>]+>", "", inner).strip()))
        return f"<h2{attrs}>{inner}</h2>"

    s2 = H2_RE.sub(repl_h2, s)
    if not items:
        return s, False

    links = "\n".join(
        f' <a href="#{i}" class="toc-item">{t}</a>' for i, t in items
    )
    new_toc = f'<div class="sidebar-module sidebar-toc"><h4>📑 Contents</h4>{links}</div>'
    s2 = TOC_RE.sub(lambda _: new_toc, s2, count=1)
    return s2, True


def iter_targets(args):
    if args:
        for a in args:
            yield Path(a)
        return
    for p in ROOT.glob("**/*-en.html"):
        rel = p.relative_to(ROOT).as_posix()
        if any(rel.startswith(d) for d in SKIP_DIRS):
            continue
        yield p


def main():
    argv = [a for a in sys.argv[1:] if a != "--check"]
    check_only = "--check" in sys.argv
    dirty = []
    for p in iter_targets(argv):
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8")
        new, changed = fix_text(s)
        if changed:
            dirty.append(p.relative_to(ROOT).as_posix())
            if not check_only:
                p.write_text(new, encoding="utf-8")
    if check_only:
        if dirty:
            print("Arabic TOC in EN files:")
            for d in dirty:
                print(" ", d)
            sys.exit(1)
        print("clean: no Arabic TOC in any live -en.html")
    else:
        if dirty:
            print(f"fixed {len(dirty)} file(s):")
            for d in dirty:
                print(" ", d)
        else:
            print("nothing to fix")


if __name__ == "__main__":
    main()
