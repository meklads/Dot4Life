#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild recipe detail pages — Budget Bytes article layout (phase 3)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from recipe_site_chrome import (  # noqa: E402
    LANG_BOOT,
    MOBILE_DROPDOWN,
    RECIPE_HEAD_ASSETS,
    site_footer,
    site_header,
)

RECIPES_DIR = ROOT / "library" / "recipes"
DATA = json.loads((RECIPES_DIR / "recipes.json").read_text(encoding="utf-8"))

KCAL: dict[str, int] = {
    "avocado-egg-toast": 380,
    "baked-salmon-veg": 420,
    "chickpea-rice-bowl": 350,
    "chicken-shawarma-bowl": 450,
    "date-nut-smoothie": 320,
    "egg-tomato-skillet": 280,
    "family-vegetable-stew": 220,
    "friday-family-pasta": 380,
    "grilled-chicken-salad": 320,
    "iron-oats-breakfast": 340,
    "lentil-koshari-bowl": 400,
    "lentil-spinach-soup": 250,
    "one-pot-chicken-rice": 450,
    "tuna-wrap-quick": 310,
    "veg-pasta-budget": 300,
    "yogurt-fruit-parfait": 280,
}

BUDGET_LABEL = {
    "low": ("Low budget", "ميزانية منخفضة"),
    "medium": ("Medium budget", "ميزانية متوسطة"),
}

CAT_BY_ID = {c["id"]: c for c in DATA["categories"]}
RECIPES_BY_SLUG = {r["slug"]: r for r in DATA["recipes"]}

SCHEMA_META: dict[str, dict[str, str]] = {
    "veg-pasta-budget": {
        "name": "Budget Vegetable Pasta",
        "meta": "Budget vegetable pasta with frozen mixed vegetables: pantry-friendly Gulf dinner in 26 minutes. Kid-friendly meal with step-by-step guide and nutrition estimate.",
        "category": "Dinner",
        "keywords": "vegetable pasta, budget dinner, frozen vegetables, gulf family recipe",
        "protein": "10 g",
    },
    "tuna-wrap-quick": {
        "name": "5-Minute Tuna Wrap",
        "meta": "Five-minute tuna wrap with yogurt and vegetables: no-cook Gulf lunch for busy weekdays, high protein, ready in 5 minutes with nutrition estimate.",
        "category": "Lunch",
        "keywords": "tuna wrap, no cook lunch, quick meal, gulf family recipe",
        "protein": "22 g",
    },
}


def clean(text: str) -> str:
    return text.replace("—", ", ").replace("–", ", ")


def esc_attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;")


def extract_ldjson(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    m = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', html, re.S)
    if m and m.group(1).strip():
        return clean(m.group(1).strip())
    return ""


def iso_duration(minutes: int) -> str:
    return f"PT{minutes}M"


def build_ldjson(recipe: dict) -> str:
    slug = recipe["slug"]
    prep = recipe["prepMinutes"]
    cook = recipe["cookMinutes"]
    total = prep + cook
    kcal = KCAL.get(slug, 300)
    sm = SCHEMA_META.get(slug, {})
    name = sm.get("name") or clean(recipe["title"]["en"])
    desc = sm.get("meta") or clean(recipe["intro"]["en"])
    category = sm.get("category") or "Dinner"
    keywords = sm.get("keywords", "gulf family recipe")
    protein = sm.get("protein", "12 g")
    data = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": name,
        "image": [f"https://dotforlife.com/assets/images/recipes/hero-{slug}.webp"],
        "author": {"@type": "Organization", "name": "DOTFORLIFE"},
        "datePublished": "2026-07-08",
        "dateModified": "2026-07-09",
        "description": desc[:220],
        "prepTime": iso_duration(prep),
        "cookTime": iso_duration(cook),
        "totalTime": iso_duration(total),
        "recipeYield": f"{recipe['servings']} servings",
        "recipeCategory": category,
        "recipeCuisine": "Middle Eastern",
        "keywords": keywords,
        "recipeIngredient": [clean(x) for x in recipe["ingredients"]["en"]],
        "recipeInstructions": [
            {"@type": "HowToStep", "text": clean(x)} for x in recipe["steps"]["en"]
        ],
        "nutrition": {
            "@type": "NutritionInformation",
            "calories": f"{kcal} kcal",
            "proteinContent": protein,
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def extract_meta_desc(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    return m.group(1) if m else ""


def ul_items(items: list[str]) -> str:
    return "".join(f"<li>{clean(x)}</li>" for x in items)


def list_block(recipe: dict, field: str) -> str:
    en = ul_items(recipe[field]["en"])
    ar = ul_items(recipe[field]["ar"])
    return f'<div class="rcp-lang-block"><span class="en"><ul>{en}</ul></span><span class="ar"><ul>{ar}</ul></span></div>'


def related_cards(recipe: dict) -> str:
    rows = []
    for slug in recipe.get("related", []):
        rel = RECIPES_BY_SLUG.get(slug)
        if not rel:
            continue
        img = f"/assets/images/recipes/hero-{slug}.webp"
        rows.append(
            f"""        <a href="/library/recipes/{slug}.html" class="rcp-bb-recipe-more-card">
          <div class="rcp-bb-recipe-more-img"><img src="{img}" alt="" width="400" height="300" loading="lazy"/></div>
          <span class="rcp-bb-recipe-more-title"><span class="en">{clean(rel['title']['en'])}</span><span class="ar">{clean(rel['title']['ar'])}</span></span>
        </a>"""
        )
    return "\n".join(rows)


def related_footer(recipe: dict) -> str:
    cards = related_cards(recipe)
    if not cards:
        return ""
    tool_href = recipe["relatedArticle"]
    tool_en = recipe["relatedArticleLabel"]["en"]
    tool_ar = recipe["relatedArticleLabel"]["ar"]
    return f"""
  <section class="rcp-bb-recipe-more" aria-labelledby="rcp-more-heading">
    <h2 id="rcp-more-heading" class="rcp-bb-recipe-more-heading"><span class="en">You may also like</span><span class="ar">قد يعجبك أيضاً</span></h2>
    <div class="rcp-bb-recipe-more-grid">
{cards}
    </div>
    <p class="rcp-bb-recipe-tool">
      <span class="en">Related tool:</span><span class="ar">أداة مرتبطة:</span>
      <a href="{tool_href}"><span class="en">{tool_en}</span><span class="ar">{tool_ar}</span></a>
    </p>
  </section>"""


def build_page(recipe: dict) -> str:
    slug = recipe["slug"]
    cat = CAT_BY_ID[recipe["category"]]
    path = RECIPES_DIR / f"{slug}.html"
    ld = extract_ldjson(path) or build_ldjson(recipe)
    meta_desc = clean(extract_meta_desc(path) or recipe["desc"]["en"])
    if slug in SCHEMA_META:
        meta_desc = clean(SCHEMA_META[slug]["meta"])
    prep = recipe["prepMinutes"]
    cook = recipe["cookMinutes"]
    total = prep + cook
    servings = recipe["servings"]
    kcal = KCAL.get(slug, 300)
    bud_en, bud_ar = BUDGET_LABEL.get(recipe["budget"], BUDGET_LABEL["medium"])
    img = f"/assets/images/recipes/hero-{slug}.webp"
    title_en = clean(recipe["title"]["en"])
    title_ar = clean(recipe["title"]["ar"])
    desc_en = clean(recipe["desc"]["en"])
    desc_ar = clean(recipe["desc"]["ar"])
    intro_en = clean(recipe["intro"]["en"])
    intro_ar = clean(recipe["intro"]["ar"])
    benefit_en = clean(recipe["benefit"]["en"])
    benefit_ar = clean(recipe["benefit"]["ar"])

    disclaimer = ""
    if recipe["category"] == "pregnancy":
        disclaimer = """
    <div class="rcp-disclaimer rcp-bb-disclaimer">
      <span class="en">General guidance only, not medical advice. Consult your clinician for pregnancy diets.</span>
      <span class="ar">إرشاد عام فقط وليس نصيحة طبية. استشيري طبيبك لأنظمة الحمل.</span>
    </div>"""

    header_html = site_header()
    footer_html = site_footer()
    related_html = related_footer(recipe)

    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="light" data-lang="en">
<head>
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<meta charset="UTF-8"/>
{LANG_BOOT}
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta id="dfl-page-title" data-en="{esc_attr(title_en)}" data-ar="{esc_attr(title_ar)}"/>
<title>{title_en} | DOTFORLIFE</title>
<meta name="description" content="{esc_attr(meta_desc)}"/>
<meta name="robots" content="noindex,nofollow"/>
<link rel="canonical" href="https://dotforlife.com/library/recipes/{slug}.html"/>
<link rel="alternate" hreflang="ar" href="https://dotforlife.com/library/recipes/{slug}.html?lang=ar" />
<link rel="alternate" hreflang="en" href="https://dotforlife.com/library/recipes/{slug}.html?lang=en" />
<script src="/scripts/lang-redirect.js?v=20260625"></script>
{RECIPE_HEAD_ASSETS}
<script src="/scripts/global.js?v=20260625" defer></script>
<script type="application/ld+json">
{ld}
</script>
</head>
<body class="index-page recipes-page rcp-bb-recipe no-subnav">

{header_html}
{MOBILE_DROPDOWN}

<div class="rcp-bb-wrap rcp-bb-recipe-wrap">
  <nav class="rcp-crumb rcp-bb-crumb" aria-label="Breadcrumb">
    <a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a>
    <span aria-hidden="true">/</span>
    <a href="/library/recipes/"><span class="en">Recipes</span><span class="ar">الوصفات</span></a>
    <span aria-hidden="true">/</span>
    <a href="/library/recipes/{recipe['category']}.html"><span class="en">{cat['title']['en']}</span><span class="ar">{cat['title']['ar']}</span></a>
    <span aria-hidden="true">/</span>
    <span><span class="en">{title_en}</span><span class="ar">{title_ar}</span></span>
  </nav>

  <header class="rcp-bb-recipe-header">
    <p class="rcp-bb-recipe-kicker"><span class="en">{cat['title']['en']}</span><span class="ar">{cat['title']['ar']}</span></p>
    <h1 class="rcp-bb-recipe-title"><span class="en">{title_en}</span><span class="ar">{title_ar}</span></h1>
    <p class="rcp-bb-recipe-deck"><span class="en">{desc_en}</span><span class="ar">{desc_ar}</span></p>
    <div class="rcp-bb-recipe-meta">
      <span class="rcp-bb-meta-item"><span class="en">Prep {prep}m</span><span class="ar">تحضير {prep} د</span></span>
      <span class="rcp-bb-meta-item"><span class="en">Cook {cook}m</span><span class="ar">طبخ {cook} د</span></span>
      <span class="rcp-bb-meta-item"><span class="en">Total {total}m</span><span class="ar">الإجمالي {total} د</span></span>
      <span class="rcp-bb-meta-item"><span class="en">{recipe['difficulty']['en']}</span><span class="ar">{recipe['difficulty']['ar']}</span></span>
      <span class="rcp-bb-meta-item rcp-bb-meta-item--gold"><span class="en">{bud_en}</span><span class="ar">{bud_ar}</span></span>
      <span class="rcp-bb-meta-item"><span class="en">Serves {servings}</span><span class="ar">تكفي {servings}</span></span>
      <span class="rcp-bb-meta-item"><span class="en">~{kcal} kcal</span><span class="ar">~{kcal} سعرة</span></span>
    </div>
    <p class="rcp-bb-recipe-benefit"><span class="en">{benefit_en}</span><span class="ar">{benefit_ar}</span></p>
    <p class="rcp-bb-recipe-intro"><span class="en">{intro_en}</span><span class="ar">{intro_ar}</span></p>
    <p class="rcp-bb-jump-row">
      <a href="#recipe-card" class="rcp-bb-jump-btn"><span class="en">Jump to recipe</span><span class="ar">انتقل إلى الوصفة</span></a>
    </p>
  </header>

  <figure class="rcp-bb-recipe-hero">
    <img src="{img}" alt="{esc_attr(title_en)}" width="1200" height="675" loading="eager" fetchpriority="high" class="rcp-bb-recipe-hero-img"/>
    <figcaption class="rcp-bb-recipe-hero-cap"><span class="en">Pin-friendly hero image. Vertical Pinterest crop coming soon.</span><span class="ar">صورة هيرو مناسبة للحفظ. نسخة عمودية لبنترست قريباً.</span></figcaption>
  </figure>

  <article class="rcp-bb-recipe-article" id="recipe-card">
    <section class="rcp-bb-recipe-block">
      <h2><span class="en">Ingredients</span><span class="ar">المكوّنات</span></h2>
      {list_block(recipe, "ingredients")}
    </section>
    <section class="rcp-bb-recipe-block">
      <h2><span class="en">Steps</span><span class="ar">الخطوات</span></h2>
      {list_block(recipe, "steps")}
    </section>
    <section class="rcp-bb-recipe-block">
      <h2><span class="en">Tips &amp; variations</span><span class="ar">نصائح وتنويعات</span></h2>
      {list_block(recipe, "tips")}
    </section>
{disclaimer}
    <p class="rcp-disclaimer rcp-bb-disclaimer rcp-bb-disclaimer--small"><span class="en">Estimated nutrition and costs are general guides only.</span><span class="ar">التغذية والتكاليف تقديرات إرشادية فقط.</span></p>
  </article>
{related_html}
</div>

{footer_html}

</body>
</html>
"""


def main() -> None:
    for recipe in DATA["recipes"]:
        slug = recipe["slug"]
        out = RECIPES_DIR / f"{slug}.html"
        if not out.exists():
            print(f"SKIP {slug} (missing)")
            continue
        out.write_text(build_page(recipe), encoding="utf-8")
        print(f"Wrote {slug}.html")


if __name__ == "__main__":
    main()
