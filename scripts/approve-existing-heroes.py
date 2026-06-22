#!/usr/bin/env python3
"""Copy existing hero WebP → approved/ and mark manifest approved (reuse site assets).

⚠️ QA 2026-06-23: Do NOT run blindly — verify each file matches omar-image-table prompt
(still-life, 1200×750, on-brand). Placeholders were falsely approved for H-07→H-12.
"""
from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "assets/images"
APPROVED = IMAGES / "approved"
MANIFEST = IMAGES / "image-manifest.json"

BATCH = {
    "investment-basics-beginners": {
        "alt_ar": "جرّة عملات ونبتة صغيرة ودفتر استثمار وآلة حاسبة على مكتب خشبي بإضاءة دافئة",
        "alt_en": "A coin jar, a small plant, an investing notebook and a calculator on a warm wooden desk",
    },
    "rent-vs-buy-gulf-family": {
        "alt_ar": "مجسّم منزل خشبي ومفتاح ودفتر مقارنة وآلة حاسبة على طاولة بإضاءة دافئة",
        "alt_en": "A wooden house model, a key, a comparison notebook and a calculator on a warm table",
    },
    "daily-walking-benefits": {
        "alt_ar": "حذاء مشي وزجاجة ماء على ممر حديقة عند الفجر بإضاءة دافئة",
        "alt_en": "Walking shoes and a water bottle on a park path at sunrise in warm light",
    },
    "pregnancy-week-by-week": {
        "alt_ar": "حذاء طفل صغير وبطانية ناعمة ودليل حمل على طاولة بإضاءة دافئة",
        "alt_en": "Tiny baby booties, a soft blanket and a pregnancy guide on a warm table",
    },
    "preconception-checkups": {
        "alt_ar": "سماعة طبية وقائمة فحص وكوب ماء على مكتب عيادة هادئ",
        "alt_en": "A stethoscope, a checklist and a glass of water on a calm clinic desk",
    },
    "umrah-with-kids": {
        "alt_ar": "فناء مسجد عند الغروب الذهبي وحقيبة عائلية صغيرة في المقدمة",
        "alt_en": "A mosque courtyard at golden sunset with a small family bag in the foreground",
    },
}


def main() -> None:
    APPROVED.mkdir(parents=True, exist_ok=True)
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_slug = {e["article_slug"]: e for e in data.get("entries", [])}
    today = date.today().isoformat()
    copied = 0
    for slug, meta in BATCH.items():
        src = IMAGES / f"hero-{slug}.webp"
        dest = APPROVED / f"hero-{slug}.webp"
        if not src.is_file():
            print(f"SKIP missing: {src.name}")
            continue
        shutil.copy2(src, dest)
        copied += 1
        entry = by_slug.get(slug) or {
            "article_slug": slug,
            "image": f"assets/images/approved/hero-{slug}.webp",
            "alt_ar": meta["alt_ar"],
            "alt_en": meta["alt_en"],
        }
        entry["image"] = f"assets/images/approved/hero-{slug}.webp"
        entry["alt_ar"] = meta["alt_ar"]
        entry["alt_en"] = meta["alt_en"]
        entry["visual_director"] = "approved"
        entry["by"] = "Cursor (reuse hero · alt من جدول عمر)"
        entry["date"] = today
        entry["model"] = "existing_site_asset"
        by_slug[slug] = entry
        print(f"OK {slug}")
    order = [e["article_slug"] for e in data.get("entries", [])]
    for slug in BATCH:
        if slug not in order:
            order.append(slug)
    data["entries"] = [by_slug[s] for s in order if s in by_slug]
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nCopied {copied} → approved/ · manifest updated")


if __name__ == "__main__":
    main()
