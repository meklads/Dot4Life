#!/usr/bin/env python3
"""Build site-sections.json — LIVE articles mapped to editorial pillars."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_OS = ROOT / "operating-system/site-sections.json"
OUT_WEB = ROOT / "system/gsystem-data/site-sections.json"

PLACEMENT_LABELS = {
    "home": "الهوم بيج",
    "tools": "الأدوات",
    "blog": "المدونة",
    "hub": "صفحة القسم",
}

SITE_SECTIONS = [
    {
        "id": "featured-stories",
        "title": "قصص مميزة",
        "order": 1,
        "folder": "/featured-stories/",
        "placements": ["home", "hub"],
        "is_new": False,
    },
    {
        "id": "comparisons",
        "title": "مقارنات وقرارات",
        "order": 2,
        "folder": "/comparisons/",
        "placements": ["home", "hub", "blog"],
        "is_new": False,
    },
    {
        "id": "peace-capsules",
        "title": "كبسولات يومية",
        "order": 3,
        "folder": "/peace-capsules/",
        "placements": ["home", "hub"],
        "is_new": False,
    },
    {
        "id": "health",
        "title": "الصحة والعافية",
        "order": 4,
        "folder": "/health/",
        "placements": ["home", "blog", "tools"],
        "is_new": False,
    },
    {
        "id": "pregnancy",
        "title": "الحمل والولادة",
        "order": 5,
        "folder": "/health-pregnancy/",
        "placements": ["home", "tools", "hub"],
        "is_new": False,
    },
    {
        "id": "islamic-life",
        "title": "الحياة الإسلامية",
        "order": 6,
        "folder": "/islamic-hajj-umrah/",
        "placements": ["hub", "blog", "home"],
        "is_new": False,
    },
    {
        "id": "religious-tourism",
        "title": "السياحة الدينية (مكة والمدينة)",
        "order": 7,
        "folder": "/islamic-hajj-umrah/",
        "placements": ["home", "blog", "tools"],
        "is_new": False,
    },
    {
        "id": "real-estate",
        "title": "العقار",
        "order": 8,
        "folder": "/real-estate/",
        "placements": ["home", "hub", "tools"],
        "is_new": False,
    },
    {
        "id": "muslim-curriculum",
        "title": "منهج المسلم",
        "order": 9,
        "folder": "/guides/",
        "placements": ["hub", "home"],
        "is_new": True,
    },
    {
        "id": "free-books-gifts",
        "title": "كتب وهدايا مجانية",
        "order": 10,
        "folder": "/guides/",
        "placements": ["hub", "home"],
        "is_new": True,
    },
]

PILLAR_TO_SECTION = {
    "1_featured-stories": "featured-stories",
    "2_comparisons": "comparisons",
    "3_peace-capsules": "peace-capsules",
    "4_health": "health",
    "5_islamic": "islamic-life",
    "6_travel": "religious-tourism",
    "7_real-estate": "real-estate",
}

PATH_PREFIX_TO_SECTION = [
    ("/featured-stories/", "featured-stories"),
    ("/comparisons/", "comparisons"),
    ("/peace-capsules/", "peace-capsules"),
    ("/health-pregnancy/", "pregnancy"),
    ("/pregnancy", "pregnancy"),
    ("/health/", "health"),
    ("/islamic-hajj-umrah/", "islamic-life"),
    ("/real-estate/", "real-estate"),
    ("/finance-wealth/", "comparisons"),
]

SLUG_KEYWORDS = [
    (("pregnancy", "trimester", "preconception", "حمل"), "pregnancy"),
    (("umrah", "hajj", "medina", "makkah", "masjid", "عمرة", "المدينة", "مكة"), "religious-tourism"),
    (("prayer", "adhkar", "islamic", "hijri", "allah", "صلاة", "أذكار"), "islamic-life"),
    (("mortgage", "rent-vs", "real-estate", "property", "عقار", "تمويل"), "real-estate"),
    (("nutrition", "walking", "bmi", "health", "sleep", "تغذية", "صحة"), "health"),
    (("evening", "ritual", "capsule", "سلام", "مساء"), "peace-capsules"),
]


def _path(card: dict) -> str:
    if card.get("url"):
        try:
            from urllib.parse import urlparse

            return urlparse(card["url"]).path
        except Exception:
            pass
    return card.get("url_path") or ""


SLUG_SECTION_OVERRIDE = {
    "gold-vs-real-estate-gulf-family": "real-estate",
    "rent-vs-buy-gulf-family": "real-estate",
    "jeddah-mortgage-calculator": "real-estate",
    "riyadh-rental-yield": "real-estate",
    "oman-property-roi": "real-estate",
}


def infer_site_section(card: dict) -> str:
    slug = (card.get("slug") or "").lower()
    if slug in SLUG_SECTION_OVERRIDE:
        return SLUG_SECTION_OVERRIDE[slug]
    if card.get("site_section"):
        return card["site_section"]
    pillar = card.get("pillar") or card.get("batch_pillar") or ""
    if pillar in PILLAR_TO_SECTION:
        return PILLAR_TO_SECTION[pillar]
    path = _path(card)
    for prefix, sec_id in PATH_PREFIX_TO_SECTION:
        if path.startswith(prefix):
            if sec_id == "islamic-life" and any(k in slug for k in ("umrah", "medina", "makkah", "hajj", "visa")):
                return "religious-tourism"
            return sec_id
    if path.startswith("/blog/"):
        for keys, sec_id in SLUG_KEYWORDS:
            if any(k in slug for k in keys):
                return sec_id
        return "health"
    for keys, sec_id in SLUG_KEYWORDS:
        if any(k in slug for k in keys):
            return sec_id
    return "health"


def is_live_card(card: dict) -> bool:
    return card.get("col") == "done" or card.get("stage") == "done"


def article_url(card: dict) -> str:
    if card.get("url"):
        return card["url"]
    path = card.get("url_path") or ""
    if path:
        return "https://dotforlife.com" + path
    slug = card.get("slug") or ""
    if slug:
        return f"https://dotforlife.com/blog/{slug}.html"
    return ""


def pick_live_articles(cards: list[dict]) -> list[dict]:
    """One row per slug — prefer Cursor/build ticket (…C) or latest finished."""
    by_slug: dict[str, dict] = {}
    for card in cards:
        if not is_live_card(card):
            continue
        slug = card.get("slug") or card.get("id", "")
        if not slug:
            continue
        url = article_url(card)
        if not url:
            continue
        prev = by_slug.get(slug)
        if not prev:
            by_slug[slug] = card
            continue
        cid = card.get("id", "")
        pid = prev.get("id", "")
        if cid.endswith("C") and not pid.endswith("C"):
            by_slug[slug] = card
        elif card.get("finished", "") > prev.get("finished", ""):
            by_slug[slug] = card
    return list(by_slug.values())


def article_entry(card: dict, section: dict) -> dict:
    placements = card.get("site_placements") or section.get("placements", [])
    return {
        "ticket": card.get("id", ""),
        "batch": card.get("batch_article", ""),
        "title": card.get("article") or card.get("title") or card.get("slug", ""),
        "slug": card.get("slug", ""),
        "url": article_url(card),
        "live": card.get("finished") or card.get("ts", "")[:10] or "",
        "placements": placements,
    }


def build_site_sections(handoff: dict) -> dict:
    cards = handoff.get("cards", [])
    live = pick_live_articles(cards)
    by_section: dict[str, list[dict]] = {s["id"]: [] for s in SITE_SECTIONS}

    for card in live:
        sec_id = infer_site_section(card)
        if sec_id not in by_section:
            sec_id = "health"
        section = next(s for s in SITE_SECTIONS if s["id"] == sec_id)
        by_section[sec_id].append(article_entry(card, section))

    for sec_id in by_section:
        by_section[sec_id].sort(key=lambda a: a.get("live", ""), reverse=True)

    sections_out = []
    for meta in SITE_SECTIONS:
        sections_out.append(
            {
                **meta,
                "placement_labels": [PLACEMENT_LABELS.get(p, p) for p in meta["placements"]],
                "articles": by_section[meta["id"]],
                "count": len(by_section[meta["id"]]),
            }
        )

    return {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "title": "أقسام الموقع",
        "subtitle": "خريطة النشر — مقالات LIVE حسب القسم ومواضعها (هوم · أدوات · مدونة)",
        "placement_labels": PLACEMENT_LABELS,
        "sections": sections_out,
        "live_total": sum(s["count"] for s in sections_out),
    }


def export_site_sections(handoff: dict | None = None) -> Path:
    if handoff is None:
        handoff = json.loads((ROOT / "operating-system/handoff-tickets.json").read_text(encoding="utf-8"))
    data = build_site_sections(handoff)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    OUT_OS.write_text(text, encoding="utf-8")
    OUT_WEB.parent.mkdir(parents=True, exist_ok=True)
    OUT_WEB.write_text(text, encoding="utf-8")
    return OUT_OS


def main() -> None:
    export_site_sections()
    print(json.dumps({"written": str(OUT_OS), "sections": 10}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
