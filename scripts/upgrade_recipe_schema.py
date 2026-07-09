#!/usr/bin/env python3
"""Upgrade recipe pages: Recipe JSON-LD, hero chips, meta description (shawarma template)."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPES_DIR = ROOT / "library" / "recipes"

# Hand-crafted meta (140–160 chars), yield, nutrition — per recipe slug
RECIPE_META: dict[str, dict] = {
    "avocado-egg-toast": {
        "name": "Avocado Egg Toast",
        "meta": "Avocado egg toast for Gulf mornings: whole-grain bread, mashed avocado, and fried eggs in 15 minutes. High-protein breakfast with steps and nutrition estimate.",
        "category": "Breakfast",
        "keywords": "avocado egg toast, quick breakfast, high protein, gulf family recipe",
        "yield": 2,
        "kcal": 380,
        "protein": "16 g",
    },
    "baked-salmon-veg": {
        "name": "Baked Salmon with Vegetables",
        "meta": "Baked salmon sheet-pan with zucchini and carrots: omega-3 friendly, minimal prep, ready in 32 minutes. Gulf family dinner with steps and nutrition estimate.",
        "category": "Dinner",
        "keywords": "baked salmon, sheet pan dinner, omega-3, pregnancy friendly, gulf recipe",
        "yield": 2,
        "kcal": 420,
        "protein": "32 g",
    },
    "chickpea-rice-bowl": {
        "name": "Chickpea Rice Bowl",
        "meta": "Chickpea rice bowl under 5 SAR per serving: pantry staples with turmeric and cumin, ready in 35 minutes. Budget Gulf lunch with steps and nutrition estimate.",
        "category": "Lunch",
        "keywords": "chickpea rice bowl, budget meal, pantry recipe, gulf family dinner",
        "yield": 4,
        "kcal": 350,
        "protein": "12 g",
    },
    "date-nut-smoothie": {
        "name": "Date Nut Smoothie",
        "meta": "Date nut smoothie for pregnancy: dates, yogurt, almond butter, and banana in 5 minutes. Calorie-dense when appetite is low, with steps and nutrition estimate.",
        "category": "Beverage",
        "keywords": "date smoothie, pregnancy snack, high calorie drink, gulf family recipe",
        "yield": 2,
        "kcal": 320,
        "protein": "14 g",
    },
    "egg-tomato-skillet": {
        "name": "Egg Tomato Skillet",
        "meta": "Egg tomato skillet breakfast: Gulf budget pan with onion, cumin, and bread in 17 minutes. Feeds four with step-by-step guide and nutrition estimate.",
        "category": "Breakfast",
        "keywords": "egg tomato skillet, budget breakfast, gulf kitchen, quick eggs",
        "yield": 4,
        "kcal": 280,
        "protein": "18 g",
    },
    "family-vegetable-stew": {
        "name": "Family Vegetable Stew",
        "meta": "Mild family vegetable stew: potatoes, carrots, zucchini in tomato base, gentle for kids, ready in 47 minutes. Budget Gulf dinner with nutrition estimate.",
        "category": "Dinner",
        "keywords": "vegetable stew, family dinner, kid friendly, budget gulf recipe",
        "yield": 6,
        "kcal": 220,
        "protein": "6 g",
    },
    "friday-family-pasta": {
        "name": "Friday Family Pasta",
        "meta": "Friday family pasta with hidden vegetables: carrot-blended tomato sauce, crowd-pleasing and budget-friendly, ready in 35 minutes. Gulf family dinner with steps and nutrition estimate.",
        "category": "Dinner",
        "keywords": "family pasta, hidden vegetables, friday dinner, gulf family recipe",
        "yield": 6,
        "kcal": 380,
        "protein": "14 g",
    },
    "grilled-chicken-salad": {
        "name": "Grilled Chicken Family Salad",
        "meta": "Grilled chicken family salad platter: crisp greens, cucumber, and lemon dressing for warm Gulf evenings, ready in 30 minutes. Shared light dinner with nutrition estimate.",
        "category": "Dinner",
        "keywords": "grilled chicken salad, family platter, gulf evening meal, light dinner",
        "yield": 4,
        "kcal": 320,
        "protein": "28 g",
    },
    "iron-oats-breakfast": {
        "name": "Iron-Rich Oats Breakfast",
        "meta": "Iron-rich oats breakfast for pregnancy: warm oats with dates and nuts for steady morning energy, ready in 15 minutes. Gentle Gulf recipe with steps and nutrition estimate.",
        "category": "Breakfast",
        "keywords": "iron oats, pregnancy breakfast, dates nuts, gulf family recipe",
        "yield": 2,
        "kcal": 340,
        "protein": "10 g",
    },
    "lentil-koshari-bowl": {
        "name": "Lentil Koshari Bowl",
        "meta": "Simplified lentil koshari bowl at home: lentils, rice, and tangy sauce without deep frying, ready in 45 minutes. High-volume budget Gulf meal with nutrition estimate.",
        "category": "Dinner",
        "keywords": "koshari bowl, lentil rice, budget dinner, gulf family recipe",
        "yield": 4,
        "kcal": 400,
        "protein": "16 g",
    },
    "lentil-spinach-soup": {
        "name": "Lentil & Spinach Soup",
        "meta": "Lentil spinach soup for pregnancy: protein and iron from lentils, folate from spinach, light on the stomach, ready in 45 minutes. Gulf home recipe with nutrition estimate.",
        "category": "Soup",
        "keywords": "lentil spinach soup, pregnancy recipe, iron folate, gulf family meal",
        "yield": 4,
        "kcal": 250,
        "protein": "14 g",
    },
    "one-pot-chicken-rice": {
        "name": "One-Pot Chicken Rice",
        "meta": "One-pot chicken rice: Gulf-family comfort classic with warm spices, single pan cleanup, ready in 55 minutes. Friday-style dinner with step-by-step guide and nutrition estimate.",
        "category": "Dinner",
        "keywords": "one pot chicken rice, gulf comfort food, family dinner, spiced rice",
        "yield": 6,
        "kcal": 450,
        "protein": "30 g",
    },
    "yogurt-fruit-parfait": {
        "name": "Yogurt Fruit Parfait",
        "meta": "Yogurt fruit parfait layered with seasonal fruit and granola, ready in 8 minutes. Quick Gulf breakfast or after-school snack with step-by-step guide and nutrition estimate.",
        "category": "Breakfast",
        "keywords": "yogurt parfait, quick snack, breakfast layers, gulf family recipe",
        "yield": 2,
        "kcal": 280,
        "protein": "12 g",
    },
}

CATEGORY_COLLECTION: dict[str, dict] = {
    "pregnancy": {
        "name": "Pregnancy Recipes",
        "description": "Balanced meals with folate, iron, and gentle digestion in mind.",
        "url": "https://dotforlife.com/library/recipes/pregnancy.html",
        "about": [
            {"@type": "Thing", "name": "Iron-Rich Oats Breakfast"},
            {"@type": "Thing", "name": "Lentil & Spinach Soup"},
            {"@type": "Thing", "name": "Date Nut Smoothie"},
            {"@type": "Thing", "name": "Baked Salmon with Vegetables"},
        ],
    },
    "budget": {
        "name": "Budget-Friendly Recipes",
        "description": "Affordable meals using pantry staples common in Gulf homes.",
        "url": "https://dotforlife.com/library/recipes/budget.html",
        "about": [
            {"@type": "Thing", "name": "Chickpea Rice Bowl"},
            {"@type": "Thing", "name": "Egg Tomato Skillet"},
            {"@type": "Thing", "name": "Lentil Koshari Bowl"},
            {"@type": "Thing", "name": "Vegetable Pasta on a Budget"},
        ],
    },
    "quick": {
        "name": "Quick Recipes",
        "description": "Ready in 30 minutes or less for busy weekdays.",
        "url": "https://dotforlife.com/library/recipes/quick.html",
        "about": [
            {"@type": "Thing", "name": "Avocado Egg Toast"},
            {"@type": "Thing", "name": "Home Chicken Shawarma Bowl"},
            {"@type": "Thing", "name": "5-Minute Tuna Wrap"},
            {"@type": "Thing", "name": "Yogurt Fruit Parfait"},
        ],
    },
    "family": {
        "name": "Family Recipes",
        "description": "Shared meals that work for children and adults at one table.",
        "url": "https://dotforlife.com/library/recipes/family.html",
        "about": [
            {"@type": "Thing", "name": "Friday Family Pasta"},
            {"@type": "Thing", "name": "Family Vegetable Stew"},
            {"@type": "Thing", "name": "Grilled Chicken Family Salad"},
            {"@type": "Thing", "name": "One-Pot Chicken Rice"},
        ],
    },
}


def parse_minutes(label: str) -> int:
    m = re.search(r"(\d+)", label)
    return int(m.group(1)) if m else 0


def parse_hero_times(html: str) -> tuple[int, int, int]:
    prep = cook = total = 0
    for chip in re.findall(r'<span class="rcp-chip">.*?<span class="en">([^<]+)</span>', html, re.DOTALL):
        low = chip.lower()
        if low.startswith("prep"):
            prep = parse_minutes(chip)
        elif low.startswith("cook"):
            cook = parse_minutes(chip)
        elif low.startswith("total"):
            total = parse_minutes(chip)
    return prep, cook, total


def to_iso_duration(minutes: int) -> str:
    return f"PT{minutes}M"


def extract_en_list(html: str, section: str) -> list[str]:
    pattern = (
        rf"<h2>.*?{section}.*?</h2>\s*"
        r'<div class="rcp-lang-block"><span class="en"><ul>(.*?)</ul>'
    )
    m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if not m:
        return []
    return [re.sub(r"<[^>]+>", "", li).strip() for li in re.findall(r"<li>(.*?)</li>", m.group(1), re.DOTALL)]


def extract_lib_sub_en(html: str) -> str:
    m = re.search(r'<p class="lib-sub"><span class="en">([^<]+)</span>', html)
    return m.group(1).strip() if m else ""


def get_robots(html: str) -> str | None:
    m = re.search(r'<meta name="robots" content="([^"]+)"', html)
    return m.group(1) if m else None


def build_recipe_ld(slug: str, html: str, meta: dict) -> str:
    prep, cook, total = parse_hero_times(html)
    ingredients = extract_en_list(html, "Ingredients")
    steps = extract_en_list(html, "Steps")
    sub = extract_lib_sub_en(html)
    url = f"https://dotforlife.com/library/recipes/{slug}.html"

    data = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": meta["name"],
        "image": ["https://dotforlife.com/assets/images/recipes/placeholder.svg"],
        "author": {"@type": "Organization", "name": "DOTFORLIFE"},
        "datePublished": "2026-07-08",
        "dateModified": "2026-07-09",
        "description": sub or meta["meta"][:200],
        "prepTime": to_iso_duration(prep),
        "cookTime": to_iso_duration(cook),
        "totalTime": to_iso_duration(total),
        "recipeYield": f"{meta['yield']} servings",
        "recipeCategory": meta["category"],
        "recipeCuisine": "Middle Eastern",
        "keywords": meta["keywords"],
        "recipeIngredient": ingredients,
        "recipeInstructions": [
            {"@type": "HowToStep", "text": s} for s in steps
        ],
        "nutrition": {
            "@type": "NutritionInformation",
            "calories": f"{meta['kcal']} kcal",
            "proteinContent": meta["protein"],
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def serve_chips(yield_n: int, kcal: int) -> str:
    return (
        f'          <span class="rcp-chip"><span class="en">Serves {yield_n}</span>'
        f'<span class="ar">تكفي {yield_n}</span></span>\n'
        f'          <span class="rcp-chip"><span class="en">~{kcal} kcal</span>'
        f'<span class="ar">~{kcal} سعرة</span></span>'
    )


def upgrade_recipe(slug: str) -> None:
    path = RECIPES_DIR / f"{slug}.html"
    html = path.read_text(encoding="utf-8")
    robots_before = get_robots(html)
    meta = RECIPE_META[slug]

    # meta description
    html = re.sub(
        r'<meta name="description" content="[^"]*"/>',
        f'<meta name="description" content="{meta["meta"]}"/>',
        html,
        count=1,
    )

    # Replace Article (or any) ld+json with Recipe
    recipe_ld = build_recipe_ld(slug, html, meta)
    if re.search(r'<script type="application/ld\+json">', html):
        html = re.sub(
            r'<script type="application/ld\+json">[\s\S]*?</script>',
            f"<script type=\"application/ld+json\">\n{recipe_ld}\n</script>",
            html,
            count=1,
        )
    else:
        html = html.replace(
            '<script src="/scripts/global.js?v=20260625" defer></script>\n</head>',
            f'<script src="/scripts/global.js?v=20260625" defer></script>\n<script type="application/ld+json">\n{recipe_ld}\n</script>\n</head>',
            1,
        )

    # Add Serves + kcal chips after budget chip if missing
    if "Serves " not in html:
        chips = serve_chips(meta["yield"], meta["kcal"])
        html = re.sub(
            r'(<span class="rcp-chip rcp-chip--budget">.*?</span>\n)',
            r"\1" + chips + "\n",
            html,
            count=1,
        )

    robots_after = get_robots(html)
    if robots_before != robots_after:
        raise RuntimeError(f"{slug}: robots changed {robots_before!r} -> {robots_after!r}")

    json.loads(recipe_ld)
    path.write_text(html, encoding="utf-8")
    print(f"OK  {slug}.html")


def upgrade_category(cat: str) -> None:
    path = RECIPES_DIR / f"{cat}.html"
    html = path.read_text(encoding="utf-8")
    info = CATEGORY_COLLECTION[cat]
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": info["name"],
        "description": info["description"],
        "url": info["url"],
        "isPartOf": {"@type": "WebSite", "name": "DOTFORLIFE", "url": "https://dotforlife.com"},
        "about": info["about"],
    }
    block = f'<script type="application/ld+json">\n{json.dumps(data, ensure_ascii=False, indent=2)}\n</script>'
    if re.search(r'<script type="application/ld\+json">', html):
        html = re.sub(
            r'<script type="application/ld\+json">[\s\S]*?</script>',
            block,
            html,
            count=1,
        )
    else:
        html = html.replace(
            '<script src="/scripts/global.js?v=20260625" defer></script>\n</head>',
            f'<script src="/scripts/global.js?v=20260625" defer></script>\n{block}\n</head>',
            1,
        )
    json.loads(block.split(">", 1)[1].rsplit("</", 1)[0])
    path.write_text(html, encoding="utf-8")
    print(f"OK  {cat}.html (CollectionPage)")


def main() -> int:
    batch = sys.argv[1:] if len(sys.argv) > 1 else list(RECIPE_META.keys())
    categories = [a for a in batch if a in CATEGORY_COLLECTION]
    recipes = [a for a in batch if a in RECIPE_META]

    for slug in recipes:
        upgrade_recipe(slug)
    for cat in categories:
        upgrade_category(cat)

    if recipes:
        paths = [str(RECIPES_DIR / f"{s}.html") for s in recipes]
        proc = subprocess.run(
            ["python3", "scripts/amer_gate.py", *paths],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        print(proc.stdout)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
