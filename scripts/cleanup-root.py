#!/usr/bin/env python3
"""C-F7: Root cleanup — move backups, strip ads from redirect stubs."""
from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / "outputs" / "backups" / f"root-cleanup-{date.today().strftime('%Y%m%d')}"
ADS_RE = re.compile(
    r'\s*<script async src="https://pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^"]*"[^>]*></script>',
    re.I,
)

# Redirect stubs at repo root (not live section pages under system/)
REDIRECT_STUBS = [
    ROOT / "sec1.html", ROOT / "sec2.html", ROOT / "sec3.html",
    ROOT / "sec4.html", ROOT / "sec5.html", ROOT / "sec6.html",
    ROOT / "privacy.html", ROOT / "brand-guide.html", ROOT / "review.html",
]
MOVE_TO_BACKUP = [
    ROOT / "index-backup-20260615-2245.html",
]


def strip_ads(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new = ADS_RE.sub("", text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    BACKUP.mkdir(parents=True, exist_ok=True)
    log: list[str] = []

    for src in MOVE_TO_BACKUP:
        if src.exists():
            dst = BACKUP / src.name
            shutil.move(str(src), str(dst))
            log.append(f"MOVED {src.name} → {dst.relative_to(ROOT)}")

    for path in REDIRECT_STUBS:
        if path.exists() and strip_ads(path):
            log.append(f"ADS REMOVED {path.relative_to(ROOT)}")

    manifest = BACKUP / "manifest.txt"
    manifest.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"C-F7: {len(log)} actions")
    for line in log:
        print(f"  ✅ {line}")
    print(f"  manifest: {manifest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
