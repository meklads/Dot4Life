#!/usr/bin/env python3
"""Ingest Omar's WebP from صور/ → assets/images/approved/ and optionally approve manifest."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "صور"
APPROVED = ROOT / "assets/images/approved"
MANIFEST = ROOT / "assets/images/image-manifest.json"

HERO_RE = re.compile(r"^hero-(.+)\.webp$", re.I)


def slug_from_name(name: str) -> str | None:
    m = HERO_RE.match(name)
    return m.group(1) if m else None


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save_manifest(data: dict) -> None:
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    approve = "--approve" in sys.argv
    if not STAGING.is_dir():
        print(f"No staging dir: {STAGING}")
        return
    manifest = load_manifest()
    by_slug = {e["article_slug"]: e for e in manifest.get("entries", [])}
    moved = 0
    for src in sorted(STAGING.glob("hero-*.webp")):
        slug = slug_from_name(src.name)
        if not slug:
            continue
        dest = APPROVED / src.name
        APPROVED.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        moved += 1
        print(f"  ✅ {src.name} → approved/")
        if approve and slug in by_slug:
            by_slug[slug]["visual_director"] = "approved"
            by_slug[slug]["date"] = __import__("datetime").date.today().isoformat()
    if approve and moved:
        manifest["entries"] = list(by_slug.values()) if by_slug else manifest.get("entries", [])
        # preserve order from original entries list
        order = {e["article_slug"]: e for e in manifest.get("entries", [])}
        manifest["entries"] = [
            order.get(e["article_slug"], e) for e in load_manifest().get("entries", [])
        ]
        for e in manifest["entries"]:
            if (APPROVED / f"hero-{e['article_slug']}.webp").exists() and approve:
                if e.get("visual_director") == "pending":
                    e["visual_director"] = "approved"
        save_manifest(manifest)
        print("  Manifest updated (pending→approved where file exists)")
    print(f"\nIngested: {moved} file(s)")


if __name__ == "__main__":
    main()
