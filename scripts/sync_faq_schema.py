#!/usr/bin/env python3
"""Re-sync FAQPage JSON-LD from visible .faq-item / FAQ-section microdata only."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fix_noindex_common import extract_visible_faq_pairs, replace_faq_schema  # noqa: E402

SKIP_DIRS = {"outputs", "node_modules", ".git", "scripts", "legacy", "operating-system"}


def iter_targets(argv: list[str]) -> list[Path]:
    if len(argv) > 1:
        return [ROOT / arg for arg in argv[1:]]
    out: list[Path] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        out.append(path)
    return out


def main() -> None:
    fixed = 0
    for path in iter_targets(sys.argv):
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        if "FAQPage" not in html:
            continue
        pairs = extract_visible_faq_pairs(html)
        if not pairs:
            continue
        new_html = replace_faq_schema(html, pairs)
        if new_html != html:
            path.write_text(new_html, encoding="utf-8")
            fixed += 1
            print(f"  synced {path.relative_to(ROOT)} ({len(pairs)} Q)")
    print(f"sync_faq_schema: {fixed} file(s) updated")


if __name__ == "__main__":
    main()
