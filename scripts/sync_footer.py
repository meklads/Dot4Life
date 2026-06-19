#!/usr/bin/env python3
"""Replace legacy footers with unified 4-column footer from partials/footer.html."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOOTER = (ROOT / "partials" / "footer.html").read_text(encoding="utf-8").strip()
FOOTER_BLOCK = re.search(r"<footer[\s\S]*?</footer>", FOOTER).group(0)

SKIP_DIRS = {"node_modules", ".git", "tools/_finance_backup", "assets/queue", "__pycache__"}
SKIP_PARTS = (".bak", "index-backup", "batch5_")


def should_skip(path: Path) -> bool:
    s = str(path)
    if path.name.startswith(".") or path.suffix not in {".html", ".htm"}:
        return True
    if path.name == "footer.html" and "partials" in s:
        return True
    for part in SKIP_PARTS:
        if part in path.name:
            return True
    for d in SKIP_DIRS:
        if f"/{d}/" in s or s.endswith(f"/{d}"):
            return True
    return False


def bump_global_css(text: str) -> str:
    return re.sub(
        r"/styles/global\.css\?v=[^\"']+",
        "/styles/global.css?v=20260626c",
        text,
    )


def sync_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if "footer-top" in text or (
        "class=\"site-footer\"" in text
        and "footer-accent" not in text
        and "footer-main" in text
    ):
        if "footer-top" in text:
            text = re.sub(r"<footer class=\"site-footer\"[\s\S]*?</footer>", FOOTER_BLOCK, text, count=1)
        elif "footer-accent" not in text:
            text = text.replace(
                '<footer class="site-footer" role="contentinfo">\n  <div class="footer-inner">',
                '<footer class="site-footer" role="contentinfo">\n  <div class="footer-accent" aria-hidden="true"></div>\n  <div class="footer-inner">',
                1,
            )
            text = text.replace(
                '<footer class="site-footer">\n  <div class="footer-inner">',
                '<footer class="site-footer">\n  <div class="footer-accent" aria-hidden="true"></div>\n  <div class="footer-inner">',
                1,
            )

    if text != original:
        text = bump_global_css(text)
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    updated = 0
    for path in ROOT.rglob("*.html"):
        if should_skip(path):
            continue
        if sync_file(path):
            updated += 1
            print(path.relative_to(ROOT))
    print(f"\nUpdated {updated} files")


if __name__ == "__main__":
    main()
