#!/usr/bin/env python3
"""Single-pass HTML slug index — shared by autopilot and team-board refresh."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    "outputs",
    "node_modules",
    ".git",
    "scripts",
    "legacy",
    "operating-system",
    "capsule-engine",
    "system",
    ".tmp_amer",
}

_slug_index_cache: dict[str, list[Path]] | None = None


def build_slug_index() -> dict[str, list[Path]]:
    from image_manifest import article_slug_from_path

    index: dict[str, list[Path]] = {}
    for p in ROOT.rglob("*.html"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        slug = article_slug_from_path(p)
        index.setdefault(slug, []).append(p)
    return index


def html_pages_for_slug(slug: str) -> list[Path]:
    global _slug_index_cache
    if _slug_index_cache is None:
        _slug_index_cache = build_slug_index()
    return sorted(set(_slug_index_cache.get(slug, [])))


def clear_slug_index_cache() -> None:
    global _slug_index_cache
    _slug_index_cache = None
