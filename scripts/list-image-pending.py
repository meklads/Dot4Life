#!/usr/bin/env python3
"""List articles waiting for Omar's approved image in image-manifest.json."""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAIL_PATHS = {
    "blog/family-budget-planning-guide.html",
    "blog/gold-vs-savings-account-comparison-en.html",
    "blog/gold-vs-savings-account-comparison.html",
    "blog/hotel-near-haram-vs-budget-umrah-en.html",
    "blog/islamic-inheritance-basics-en.html",
    "blog/managing-screen-time-children.html",
    "blog/pistachios-vs-almonds-comparison-en.html",
    "blog/pregnancy-weeks-guide.html",
    "blog/umrah-budget-guide-families-en.html",
    "blog/walking-vs-running-comparison-en.html",
    "blog/zakat-investment-portfolios-en.html",
    "guides/complete-life-guide.html",
    "guides/mecca-medina.html",
    "guides/salalah-oman.html",
    "guides/saudi-tourism.html",
}


def load_build_map_slugs() -> list[str]:
    spec = importlib.util.spec_from_file_location(
        "build", ROOT / "scripts/build-from-approved-draft.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    slugs: list[str] = []
    for cfg in mod.BUILD_MAP:
        for key in ("out_ar", "out_en"):
            p = cfg.get(key)
            if not p:
                continue
            stem = p.stem
            if stem.endswith("-en"):
                stem = stem[:-3]
            if stem not in slugs:
                slugs.append(stem)
    if "oman-property-roi" not in slugs:
        slugs.append("oman-property-roi")
    return slugs


def schema_only_pass_paths() -> list[str]:
    triage = (ROOT / "operating-system/reports/track-blog-triage.md").read_text(
        encoding="utf-8"
    )
    paths: list[str] = []
    for m in re.finditer(r"`((?:blog|guides|comparisons)/[^`]+\.html)`", triage):
        rel = m.group(1)
        if rel.startswith("blog/") or rel.startswith("guides/") or rel.startswith(
            "comparisons/"
        ):
            paths.append(rel)
    # Schema-only section ends before "## 2)"
    section = triage.split("## 2)")[0]
    paths = []
    for m in re.finditer(r"`((?:blog|guides|comparisons)/[^`]+\.html)`", section):
        paths.append(m.group(1))
    return [p for p in paths if p not in FAIL_PATHS]


def slug_from_rel(rel: str) -> str:
    stem = Path(rel).stem
    if stem.endswith("-en"):
        stem = stem[:-3]
    elif stem.endswith("-ar"):
        stem = stem[:-3]
    return stem


def manifest_status(slug: str, by_slug: dict) -> str:
    e = by_slug.get(slug)
    if not e:
        return "missing"
    return e.get("visual_director", "pending")


def main() -> None:
    from image_manifest import entries_by_slug, load_manifest

    manifest = load_manifest()
    by_slug = entries_by_slug(manifest)

    live = load_build_map_slugs()
    blog_pass = sorted({slug_from_rel(p) for p in schema_only_pass_paths()})

    fmt = "md" if "--md" in sys.argv else "text"
    groups = [
        ("Track A LIVE (priority P0)", live),
        ("Blog triage PASS (43 files → unique slugs)", blog_pass),
    ]

    if fmt == "md":
        print("# Image pending — Omar production queue\n")
        print(f"Manifest: `{len(manifest.get('entries', []))}` entries · approved dir: `assets/images/approved/`\n")
        for title, slugs in groups:
            print(f"## {title} ({len(slugs)} slugs)\n")
            print("| # | article_slug | manifest | suggested file |")
            print("|---|--------------|----------|----------------|")
            for i, slug in enumerate(slugs, 1):
                st = manifest_status(slug, by_slug)
                print(
                    f"| {i} | `{slug}` | {st} | `hero-{slug}.webp` |"
                )
            print()
    else:
        for title, slugs in groups:
            print(f"\n=== {title} ({len(slugs)}) ===")
            for slug in slugs:
                print(f"  {slug:45} {manifest_status(slug, by_slug)}")

    pending = sum(
        1 for s in live + blog_pass if manifest_status(s, by_slug) != "approved"
    )
    print(f"\nTotal slugs: {len(live) + len(blog_pass)} · pending approval: {pending}")


if __name__ == "__main__":
    main()
