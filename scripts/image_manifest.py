#!/usr/bin/env python3
"""Image Module — manifest-driven hero images (owner: عمر · consumer: Cursor)."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "assets/images/image-manifest.json"
APPROVED_DIR = ROOT / "assets/images/approved"

EM_DASH = "\u2014"


def article_slug_from_path(path: Path) -> str:
    """Map HTML path to manifest article_slug (strip -en suffix)."""
    stem = path.stem
    if stem.endswith("-en"):
        stem = stem[:-3]
    elif stem.endswith("-ar"):
        stem = stem[:-3]
    return stem


def load_manifest(path: Path | None = None) -> dict:
    p = path or MANIFEST_PATH
    if not p.exists():
        return {"version": 1, "entries": []}
    data = json.loads(p.read_text(encoding="utf-8"))
    if "entries" not in data:
        data = {"version": 1, "entries": data if isinstance(data, list) else []}
    return data


def entries_by_slug(manifest: dict | None = None) -> dict[str, dict]:
    m = manifest if manifest is not None else load_manifest()
    out: dict[str, dict] = {}
    for e in m.get("entries", []):
        slug = e.get("article_slug")
        if slug:
            out[slug] = e
    return out


def lookup(slug: str, manifest: dict | None = None) -> dict | None:
    return entries_by_slug(manifest).get(slug)


def is_approved(entry: dict | None) -> bool:
    return bool(entry and entry.get("visual_director") == "approved")


def alt_for_lang(entry: dict, lang: str) -> str:
    if lang == "en":
        return (entry.get("alt_en") or entry.get("alt_ar") or "").strip()
    return (entry.get("alt_ar") or entry.get("alt_en") or "").strip()


def image_web_path(entry: dict) -> str:
    """Public URL path e.g. /assets/images/approved/hero-foo.webp"""
    raw = entry.get("image", "").strip()
    if raw.startswith("http"):
        return raw
    if raw.startswith("/"):
        return raw
    if raw.startswith("assets/"):
        return "/" + raw
    return f"/assets/images/approved/{raw}"


def image_disk_path(entry: dict) -> Path:
    raw = entry.get("image", "").strip()
    if raw.startswith("/"):
        return ROOT / raw.lstrip("/")
    if raw.startswith("assets/"):
        return ROOT / raw
    return APPROVED_DIR / raw


def hero_block(entry: dict, lang: str, *, eager: bool = False) -> tuple[str, str, str]:
    """Returns (html figure, web_path, alt)."""
    web = image_web_path(entry)
    alt = alt_for_lang(entry, lang)
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    fig = (
        f'<figure class="hero"><img src="{web}" alt="{html.escape(alt)}" '
        f'width="1200" height="750" {load}></figure>'
    )
    return fig, web, alt


def assert_g5_image(
    page: str,
    out_path: Path,
    lang: str,
    *,
    strict: bool,
    gate_fail,
) -> None:
    """
    G5 image gate.
    strict=True  → manifest approved required (TECH_BUILD fail-closed).
    strict=False → legacy hero .webp OK (LIVE audit grandfather).
    """
    slug = article_slug_from_path(out_path)
    entry = lookup(slug)
    hero_m = re.search(
        r'<figure class="hero"><img[^>]+src="([^"]+)"[^>]+alt="([^"]*)"',
        page,
    )

    if is_approved(entry):
        web = image_web_path(entry)
        disk = image_disk_path(entry)
        if not disk.exists():
            gate_fail("G5", out_path, f"BLOCKED_IMAGE: approved file missing {disk.relative_to(ROOT)}")
        alt = alt_for_lang(entry, lang)
        if EM_DASH in alt:
            gate_fail("G5", out_path, "BLOCKED_IMAGE: alt contains em-dash")
        if not alt:
            gate_fail("G5", out_path, "BLOCKED_IMAGE: alt empty in manifest")
        if not hero_m:
            gate_fail("G5", out_path, "BLOCKED_IMAGE: hero figure missing")
        src = hero_m.group(1)
        if web not in src and src != web:
            gate_fail("G5", out_path, f"BLOCKED_IMAGE: hero src {src!r} != manifest {web!r}")
        if 'property="og:image"' not in page:
            gate_fail("G5", out_path, "og:image missing")
        return

    if strict:
        status = (entry or {}).get("visual_director", "missing")
        gate_fail("G5", out_path, f"BLOCKED_IMAGE: manifest {status} for slug={slug}")

    # Legacy grandfather (LIVE audit / placeholders until عمر approves)
    if not hero_m or not hero_m.group(1).endswith(".webp"):
        gate_fail("G5", out_path, "hero WebP img missing")
    if not hero_m.group(2).strip():
        gate_fail("G5", out_path, "hero alt empty")
    if 'property="og:image"' not in page:
        gate_fail("G5", out_path, "og:image missing")


def resolve_hero_for_build(
    out_path: Path,
    lang: str,
    cfg: dict,
) -> tuple[str, str, str] | None:
    """
    Returns (figure_html, web_path, abs_og_url) or None if BLOCKED.
    Fail-closed: no BUILD_MAP fallback when manifest not approved.
    """
    slug = article_slug_from_path(out_path)
    entry = lookup(slug)
    if not is_approved(entry):
        return None
    fig, web, _alt = hero_block(entry, lang, eager=True)
    abs_url = f"https://dotforlife.com{web}"
    return fig, web, abs_url
