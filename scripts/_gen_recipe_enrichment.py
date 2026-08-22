#!/usr/bin/env python3
"""One-shot generator for scripts/recipe_bb_enrichment.py"""
from __future__ import annotations

import ast
import pprint
import re
from pathlib import Path

REQUIRED = {
    "story", "successTips", "variations", "serving", "storage", "costNote", "nutritionFull"
}
NUTRITION_KEYS = {"calories", "protein", "carbs", "fat", "fiber", "sodium"}
SLUGS = [
    "iron-oats-breakfast",
    "lentil-spinach-soup",
    "date-nut-smoothie",
    "baked-salmon-veg",
    "chickpea-rice-bowl",
    "egg-tomato-skillet",
    "lentil-koshari-bowl",
    "veg-pasta-budget",
    "avocado-egg-toast",
    "tuna-wrap-quick",
    "yogurt-fruit-parfait",
    "chicken-shawarma-bowl",
    "one-pot-chicken-rice",
    "family-vegetable-stew",
    "grilled-chicken-salad",
    "friday-family-pasta",
]

ARABIC_RE = re.compile(r"[\u0600-\u06FF]")

from _gen_recipe_enrichment_data import ENRICHMENT as E1  # noqa: E402
from _gen_recipe_enrichment_data_part2 import PART2  # noqa: E402
from _gen_recipe_enrichment_data_part3 import PART3  # noqa: E402

OUT = Path(__file__).resolve().parent / "recipe_bb_enrichment.py"

FIXES = [
    (re.compile(r"مقرmش"), "مقرمش"),
    (re.compile(r"قرmش"), "قرمش"),
    (re.compile(r"طmاطm"), "طماطم"),
    (re.compile(r"لبn"), "لبن"),
    (re.compile(r"ف counters"), "أكشاك"),
    (re.compile(r"لفائf"), "لفائف"),
    (re.compile(r"منشفة\.rطبة"), "منشفة رطبة"),
    (re.compile(r"القدr"), "القدر"),
    (re.compile(r"العيal"), "العيال"),
    (re.compile(r"يتبّlon"), "يتبّلون"),
    (re.compile(r"المرq"), "المرق"),
    (re.compile(r"مرq"), "مرق"),
    (re.compile(r"ثm"), "ثم"),
    (re.compile(r"فلفl"), "فلفل"),
    (re.compile(r"الحrp"), "الحر"),
    (re.compile(r"سauna"), "سونا"),
    (re.compile(r"الألياf"), "الألياف"),
    (re.compile(r"يذbl"), "يذبل"),
    (re.compile(r"أjuicier"), "أطري"),
    (re.compile(r"الطaولة"), "الطاولة"),
    (re.compile(r"باقi"), "باقي"),
    (re.compile(r"زيada"), "زيادة"),
    (re.compile(r"احتfظي"), "احتفظi"),
    (re.compile(r"قدّmي"), "قدّمي"),
    (re.compile(r"كوستان"), "كوساتان"),
    (re.compile(r"نعna"), "نعna"),
]


def _fix_text(s: str) -> str:
    for pat, repl in FIXES:
        s = pat.sub(repl, s)
    return s


def _fix_obj(obj, in_ar: bool = False):
    if isinstance(obj, str):
        return _fix_text(obj) if in_ar else obj
    if isinstance(obj, dict):
        return {k: _fix_obj(v, in_ar or k == "ar") for k, v in obj.items()}
    if isinstance(obj, list):
        return [_fix_obj(v, in_ar) for v in obj]
    return obj


def build_enrichment() -> dict:
    merged = {**E1, **PART2, **PART3}
    return {slug: _fix_obj(merged[slug]) for slug in SLUGS}


def validate(data: dict) -> None:
    keys = list(data.keys())
    if keys != SLUGS:
        raise SystemExit(f"Key mismatch: got {len(keys)} keys, expected {len(SLUGS)}")
    for slug in SLUGS:
        entry = data[slug]
        missing = REQUIRED - set(entry)
        if missing:
            raise SystemExit(f"{slug} missing fields: {missing}")
        for lang in ("en", "ar"):
            if len(entry["story"][lang]) != 2:
                raise SystemExit(f"{slug} story.{lang} needs 2 paragraphs")
            if len(entry["successTips"][lang]) != 5:
                raise SystemExit(f"{slug} successTips.{lang} needs 5 items")
            if len(entry["variations"][lang]) != 4:
                raise SystemExit(f"{slug} variations.{lang} needs 4 items")
            for field in ("serving", "storage", "costNote"):
                if not entry[field][lang].strip():
                    raise SystemExit(f"{slug} {field}.{lang} empty")
        nf = entry["nutritionFull"]
        if set(nf) != NUTRITION_KEYS:
            raise SystemExit(f"{slug} nutritionFull keys wrong: {set(nf)}")
        _check_no_arabic_in_en(entry, slug)


def _walk_strings(obj, prefix=""):
    if isinstance(obj, str):
        yield prefix, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk_strings(v, f"{prefix}.{k}" if prefix else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_strings(v, f"{prefix}[{i}]")


def _check_no_arabic_in_en(entry, slug):
    for key, val in entry.items():
        if key == "nutritionFull":
            continue
        if isinstance(val, dict) and "en" in val:
            en_val = val["en"]
            if isinstance(en_val, str):
                texts = [en_val]
            elif isinstance(en_val, list):
                texts = en_val
            else:
                continue
            for i, s in enumerate(texts):
                if ARABIC_RE.search(s):
                    loc = f"{slug}.{key}.en[{i}]" if isinstance(en_val, list) else f"{slug}.{key}.en"
                    raise SystemExit(f"{loc} contains Arabic characters")


def main() -> None:
    data = build_enrichment()
    validate(data)
    body = pprint.pformat(data, width=100, sort_dicts=False)
    text = (
        '#!/usr/bin/env python3\n'
        '# -*- coding: utf-8 -*-\n'
        '"""Recipe enrichment — Gulf family context, Budget Bytes depth. Used by recipe build pipeline."""\n\n'
        f"ENRICHMENT = {body}\n"
    )
    OUT.write_text(text, encoding="utf-8")
    ast.parse(text)
    print(f"Wrote {OUT} ({len(data)} recipes)")


if __name__ == "__main__":
    main()
