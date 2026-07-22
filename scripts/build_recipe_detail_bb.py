#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild recipe detail pages — Budget Bytes depth (story, tips, nutrition, index)."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from recipe_bb_enrichment import ENRICHMENT  # noqa: E402
from recipe_site_chrome import (  # noqa: E402
    LANG_BOOT,
    MOBILE_DROPDOWN,
    RECIPE_HEAD_ASSETS,
    site_footer,
    site_header,
)

RECIPES_DIR = ROOT / "library" / "recipes"
DATA = json.loads((RECIPES_DIR / "recipes.json").read_text(encoding="utf-8"))

BUDGET_LABEL = {
    "low": ("Low budget", "ميزانية منخفضة"),
    "medium": ("Medium budget", "ميزانية متوسطة"),
}

CAT_BY_ID = {c["id"]: c for c in DATA["categories"]}


def clean(text: str) -> str:
    return text.replace("—", ", ").replace("–", ", ")


def esc_attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;")


def iso_duration(minutes: int) -> str:
    return f"PT{minutes}M"


def merge_recipe(recipe: dict) -> dict:
    """Merge base recipes.json with BB enrichment overrides."""
    merged = copy.deepcopy(recipe)
    extra = ENRICHMENT.get(recipe["slug"], {})
    for key in ("ingredients", "steps"):
        if key in extra:
            merged[key] = extra[key]
    merged["_bb"] = extra
    return merged


def ul_items(items: list[str]) -> str:
    return "".join(f"<li>{clean(x)}</li>" for x in items)


def list_block(items: dict) -> str:
    en = ul_items(items["en"])
    ar = ul_items(items["ar"])
    return (
        f'<div class="rcp-lang-block"><span class="en"><ul>{en}</ul></span>'
        f'<span class="ar"><ul>{ar}</ul></span></div>'
    )


def prose_block(paragraphs: dict) -> str:
    en = "".join(f"<p>{clean(p)}</p>" for p in paragraphs["en"])
    ar = "".join(f"<p>{clean(p)}</p>" for p in paragraphs["ar"])
    return (
        f'<div class="rcp-bb-prose rcp-lang-block">'
        f'<span class="en">{en}</span><span class="ar">{ar}</span></div>'
    )


def para_block(text: dict) -> str:
    return (
        f'<div class="rcp-bb-prose rcp-lang-block">'
        f'<span class="en"><p>{clean(text["en"])}</p></span>'
        f'<span class="ar"><p>{clean(text["ar"])}</p></span></div>'
    )


def nutrition_block(n: dict) -> str:
    rows = [
        ("Calories", "السعرات", n.get("calories", "—")),
        ("Protein", "البروتين", n.get("protein", "—")),
        ("Carbs", "الكربوهيدرات", n.get("carbs", "—")),
        ("Fat", "الدهون", n.get("fat", "—")),
        ("Fiber", "الألياف", n.get("fiber", "—")),
        ("Sodium", "الصوديوم", n.get("sodium", "—")),
    ]
    body = ""
    for en, ar, val in rows:
        body += (
            f'<tr><th><span class="en">{en}</span><span class="ar">{ar}</span></th>'
            f"<td>{clean(str(val))}</td></tr>"
        )
    return (
        f'<div class="rcp-bb-nutrition-wrap">'
        f'<table class="rcp-bb-nutrition"><tbody>{body}</tbody></table>'
        f'<p class="rcp-bb-nutrition-note">'
        f'<span class="en">Per serving, estimated. Not medical advice.</span>'
        f'<span class="ar">للحصة الواحدة، تقديري. ليس نصيحة طبية.</span>'
        f"</p></div>"
    )


def build_ldjson(recipe: dict) -> str:
    slug = recipe["slug"]
    extra = recipe.get("_bb", {})
    prep = recipe["prepMinutes"]
    cook = recipe["cookMinutes"]
    total = prep + cook
    nut = extra.get("nutritionFull", {})
    kcal = nut.get("calories", "300")
    story_en = extra.get("story", {}).get("en", [recipe["intro"]["en"]])
    desc = clean(story_en[0])[:220]
    data = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": clean(recipe["title"]["en"]),
        "image": [f"https://dotforlife.com/assets/images/recipes/hero-{slug}.webp"],
        "author": {"@type": "Organization", "name": "DOTFORLIFE"},
        "datePublished": "2026-07-08",
        "dateModified": "2026-07-22",
        "description": desc,
        "prepTime": iso_duration(prep),
        "cookTime": iso_duration(cook),
        "totalTime": iso_duration(total),
        "recipeYield": f"{recipe['servings']} servings",
        "recipeCategory": recipe.get("tags", {}).get("en", ["Dinner"])[0],
        "recipeCuisine": "Middle Eastern",
        "keywords": ", ".join(recipe.get("tags", {}).get("en", ["gulf family recipe"])),
        "recipeIngredient": [clean(x) for x in recipe["ingredients"]["en"]],
        "recipeInstructions": [
            {"@type": "HowToStep", "text": clean(x)} for x in recipe["steps"]["en"]
        ],
        "nutrition": {
            "@type": "NutritionInformation",
            "calories": f"{kcal} kcal",
            "proteinContent": nut.get("protein", "12 g"),
            "carbohydrateContent": nut.get("carbs", ""),
            "fatContent": nut.get("fat", ""),
            "fiberContent": nut.get("fiber", ""),
            "sodiumContent": nut.get("sodium", ""),
        },
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def category_peers(recipe: dict, limit: int = 3) -> list[dict]:
    cat = recipe["category"]
    slug = recipe["slug"]
    peers = [r for r in DATA["recipes"] if r["category"] == cat and r["slug"] != slug]
    ordered: list[dict] = []
    for s in recipe.get("related", []):
        for p in peers:
            if p["slug"] == s and p not in ordered:
                ordered.append(p)
    for p in peers:
        if p not in ordered:
            ordered.append(p)
    return ordered[:limit]


def build_sidebar(recipe: dict) -> str:
    tool_href = recipe["relatedArticle"]
    tool_en = clean(recipe["relatedArticleLabel"]["en"])
    tool_ar = clean(recipe["relatedArticleLabel"]["ar"])
    related_rows = []
    for rel in category_peers(recipe):
        img = f"/assets/images/recipes/hero-{rel['slug']}.webp"
        title_en = clean(rel["title"]["en"])
        title_ar = clean(rel["title"]["ar"])
        related_rows.append(
            f""" <div class="sidebar-related-item">
 <img src="{img}" alt="" width="64" height="48" loading="lazy">
 <div>
 <div class="related-title"><a href="/library/recipes/{rel['slug']}.html"><span class="en">{title_en}</span><span class="ar">{title_ar}</span></a></div>
 </div>
 </div>"""
        )
    related_html = "\n".join(related_rows)
    return f"""<aside class="article-sidebar">
<div class="sidebar-module sidebar-toc">
 <h4><span class="en">📑 Contents</span><span class="ar">📑 المحتويات</span></h4>
 <a href="#rcp-story" class="toc-item"><span class="en">About this recipe</span><span class="ar">عن الوصفة</span></a>
 <a href="#rcp-ingredients" class="toc-item"><span class="en">Ingredients</span><span class="ar">المكوّنات</span></a>
 <a href="#rcp-steps" class="toc-item"><span class="en">Steps</span><span class="ar">الخطوات</span></a>
 <a href="#rcp-success" class="toc-item"><span class="en">Success tips</span><span class="ar">نصائح النجاح</span></a>
 <a href="#rcp-variations" class="toc-item"><span class="en">Variations</span><span class="ar">تنويعات</span></a>
 <a href="#rcp-serving" class="toc-item"><span class="en">Serving</span><span class="ar">التقديم</span></a>
 <a href="#rcp-storage" class="toc-item"><span class="en">Storage</span><span class="ar">التخزين</span></a>
 <a href="#rcp-nutrition" class="toc-item"><span class="en">Nutrition</span><span class="ar">التغذية</span></a>
</div>

<div class="sidebar-module sidebar-related">
 <h4><span class="en">Related recipes</span><span class="ar">وصفات ذات صلة</span></h4>
{related_html}
</div>

<div class="sidebar-module sidebar-tools">
 <h4><span class="en">🛠 Tools</span><span class="ar">🛠 أدوات</span></h4>
 <a href="{tool_href}" class="tool-btn"><span class="en">{tool_en}</span><span class="ar">{tool_ar}</span></a>
</div>
</aside>"""


def build_page(recipe: dict) -> str:
    recipe = merge_recipe(recipe)
    slug = recipe["slug"]
    extra = recipe.get("_bb", {})
    cat = CAT_BY_ID[recipe["category"]]
    ld = build_ldjson(recipe)
    story_en = extra.get("story", {}).get("en", [recipe["intro"]["en"]])
    meta_desc = clean(story_en[0])[:155]
    prep = recipe["prepMinutes"]
    cook = recipe["cookMinutes"]
    total = prep + cook
    servings = recipe["servings"]
    nut = extra.get("nutritionFull", {})
    kcal = nut.get("calories", "300")
    bud_en, bud_ar = BUDGET_LABEL.get(recipe["budget"], BUDGET_LABEL["medium"])
    img = f"/assets/images/recipes/hero-{slug}.webp"
    title_en = clean(recipe["title"]["en"])
    title_ar = clean(recipe["title"]["ar"])
    desc_en = clean(recipe["desc"]["en"])
    desc_ar = clean(recipe["desc"]["ar"])
    benefit_en = clean(recipe["benefit"]["en"])
    benefit_ar = clean(recipe["benefit"]["ar"])
    cost = extra.get("costNote", {})

    disclaimer = ""
    if recipe["category"] == "pregnancy":
        disclaimer = """
    <div class="rcp-disclaimer rcp-bb-disclaimer">
      <span class="en">General guidance only, not medical advice. Consult your clinician for pregnancy diets.</span>
      <span class="ar">إرشاد عام فقط وليس نصيحة طبية. استشيري طبيبك لأنظمة الحمل.</span>
    </div>"""

    story_html = prose_block(extra["story"]) if extra.get("story") else ""
    cost_html = ""
    if cost:
        cost_html = (
            f'<p class="rcp-bb-cost-note rcp-lang-block">'
            f'<span class="en"><strong>Estimated cost:</strong> {clean(cost["en"])}</span>'
            f'<span class="ar"><strong>التكلفة التقديرية:</strong> {clean(cost["ar"])}</span>'
            f"</p>"
        )

    body_sections = f"""
    <section class="rcp-bb-recipe-block" id="rcp-story">
      <h2><span class="en">About this recipe</span><span class="ar">عن هذه الوصفة</span></h2>
      {story_html}
      {cost_html}
    </section>
    <section class="rcp-bb-recipe-block" id="rcp-ingredients">
      <h2><span class="en">Ingredients</span><span class="ar">المكوّنات</span></h2>
      {list_block(recipe["ingredients"])}
    </section>
    <section class="rcp-bb-recipe-block" id="rcp-steps">
      <h2><span class="en">Steps</span><span class="ar">الخطوات</span></h2>
      {list_block(recipe["steps"])}
    </section>
    <section class="rcp-bb-recipe-block" id="rcp-success">
      <h2><span class="en">Recipe success tips</span><span class="ar">نصائح لنجاح الوصفة</span></h2>
      {list_block(extra["successTips"])}
    </section>
    <section class="rcp-bb-recipe-block" id="rcp-variations">
      <h2><span class="en">Variations to try</span><span class="ar">تنويعات يمكن تجربتها</span></h2>
      {list_block(extra["variations"])}
    </section>
    <section class="rcp-bb-recipe-block" id="rcp-serving">
      <h2><span class="en">Serving suggestions</span><span class="ar">اقتراحات التقديم</span></h2>
      {para_block(extra["serving"])}
    </section>
    <section class="rcp-bb-recipe-block" id="rcp-storage">
      <h2><span class="en">Storage &amp; make ahead</span><span class="ar">التخزين والتحضير المسبق</span></h2>
      {para_block(extra["storage"])}
    </section>
    <section class="rcp-bb-recipe-block" id="rcp-nutrition">
      <h2><span class="en">Nutrition (estimated)</span><span class="ar">القيمة الغذائية (تقديرية)</span></h2>
      {nutrition_block(nut)}
    </section>
{disclaimer}
    <p class="rcp-disclaimer rcp-bb-disclaimer rcp-bb-disclaimer--small"><span class="en">Estimated nutrition and costs are general guides only.</span><span class="ar">التغذية والتكاليف تقديرات إرشادية فقط.</span></p>
"""

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
<meta name="robots" content="index,follow"/>
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

{site_header()}
{MOBILE_DROPDOWN}

<div class="rcp-bb-wrap rcp-bb-recipe-wrap article-wrap">
  <nav class="rcp-crumb rcp-bb-crumb" aria-label="Breadcrumb">
    <a href="/library.html"><span class="en">Tools</span><span class="ar">الأدوات</span></a>
    <span aria-hidden="true">/</span>
    <a href="/library/recipes/"><span class="en">Recipes</span><span class="ar">الوصفات</span></a>
    <span aria-hidden="true">/</span>
    <a href="/library/recipes/{recipe['category']}.html"><span class="en">{cat['title']['en']}</span><span class="ar">{cat['title']['ar']}</span></a>
    <span aria-hidden="true">/</span>
    <span><span class="en">{title_en}</span><span class="ar">{title_ar}</span></span>
  </nav>

  <div class="article-layout rcp-bb-recipe-layout">
  <main class="article-main">

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
    <p class="rcp-bb-jump-row">
      <a href="#rcp-ingredients" class="rcp-bb-jump-btn"><span class="en">Jump to recipe</span><span class="ar">انتقل إلى الوصفة</span></a>
    </p>
  </header>

  <figure class="rcp-bb-recipe-hero">
    <img src="{img}" alt="{esc_attr(title_en)}" width="1200" height="675" loading="eager" fetchpriority="high" class="rcp-bb-recipe-hero-img"/>
  </figure>

  <article class="rcp-bb-recipe-article article-body" id="recipe-card">
{body_sections}
  </article>

  </main>

{build_sidebar(recipe)}

  </div>
</div>

{site_footer()}

</body>
</html>
"""


def main() -> None:
    for recipe in DATA["recipes"]:
        slug = recipe["slug"]
        out = RECIPES_DIR / f"{slug}.html"
        if slug not in ENRICHMENT:
            print(f"WARN no enrichment for {slug}")
        out.write_text(build_page(recipe), encoding="utf-8")
        print(f"Wrote {slug}.html")


if __name__ == "__main__":
    main()
