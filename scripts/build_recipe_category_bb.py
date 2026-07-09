#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Budget Bytes-style recipe category pages (phase 2)."""
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

RECIPES = ROOT / "library" / "recipes"


def esc_attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;")


CATS = {
    "pregnancy": {
        "en": "Pregnancy Recipes",
        "ar": "وصفات للحامل",
        "desc_en": "Balanced meals with folate, iron, and gentle digestion in mind.",
        "desc_ar": "وجبات متوازنة تراعي الحديد والفولات والهضم اللطيف.",
        "banner_img": "hero-iron-oats-breakfast.webp",
        "section_en": "Pregnancy Nourishment",
        "section_ar": "تغذية الحامل",
        "related_href": "/pregnancy-journey.html",
        "related_en": "Pregnancy Journey",
        "related_ar": "رحلة الحمل",
        "disclaimer": True,
        "slugs": ["iron-oats-breakfast", "lentil-spinach-soup", "date-nut-smoothie", "baked-salmon-veg"],
    },
    "budget": {
        "en": "Budget-Friendly Recipes",
        "ar": "وصفات اقتصادية",
        "desc_en": "Filling family meals that respect a Gulf household budget.",
        "desc_ar": "وجبات مشبعة تحترم ميزانية العائلة في الخليج.",
        "banner_img": "hero-chickpea-rice-bowl.webp",
        "section_en": "Budget-Friendly Meals",
        "section_ar": "وجبات اقتصادية",
        "related_href": "/tools/monthly-budget.html",
        "related_en": "Monthly Budget Tool",
        "related_ar": "أداة الميزانية الشهرية",
        "disclaimer": False,
        "slugs": ["chickpea-rice-bowl", "egg-tomato-skillet", "lentil-koshari-bowl", "veg-pasta-budget"],
    },
    "quick": {
        "en": "Quick Recipes",
        "ar": "وصفات سريعة",
        "desc_en": "Ready in 30 minutes or less for busy weekdays.",
        "desc_ar": "جاهزة خلال 30 دقيقة أو أقل لأيام الأسبوع المزدحمة.",
        "banner_img": "hero-chicken-shawarma-bowl.webp",
        "section_en": "Quick Weeknight Meals",
        "section_ar": "وجبات سريعة لأيام الأسبوع",
        "related_href": "/productivity.html",
        "related_en": "Productivity Hub",
        "related_ar": "مركز الإنتاجية",
        "disclaimer": False,
        "slugs": ["avocado-egg-toast", "tuna-wrap-quick", "yogurt-fruit-parfait", "chicken-shawarma-bowl"],
    },
    "family": {
        "en": "Family Recipes",
        "ar": "وصفات للعائلة",
        "desc_en": "One-table meals that work for parents and children.",
        "desc_ar": "وجبات على مائدة واحدة تناسب الآباء والأطفال.",
        "banner_img": "hero-friday-family-pasta.webp",
        "section_en": "Family Table Recipes",
        "section_ar": "وجبات مائدة العائلة",
        "related_href": "/peace-capsules/peace-at-home-5-steps.html",
        "related_en": "Peace at Home",
        "related_ar": "السلام في البيت",
        "disclaimer": False,
        "slugs": ["one-pot-chicken-rice", "family-vegetable-stew", "grilled-chicken-salad", "friday-family-pasta"],
    },
}

CAT_NAV = [
    ("pregnancy", "hero-iron-oats-breakfast.webp", "Pregnancy", "للحامل"),
    ("budget", "hero-chickpea-rice-bowl.webp", "Budget", "اقتصادية"),
    ("quick", "hero-chicken-shawarma-bowl.webp", "Quick", "سريعة"),
    ("family", "hero-friday-family-pasta.webp", "Family", "للعائلة"),
]

META_FALLBACK = {
    "tuna-wrap-quick": ("5 min · Quick lunch", "5 د · غداء سريع"),
    "veg-pasta-budget": ("26 min · 4 servings", "26 د · 4 حصص"),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;")


def parse_recipe(slug: str) -> dict:
    t = (RECIPES / f"{slug}.html").read_text(encoding="utf-8")
    en = re.search(r"<h1[^>]*>.*?<span class=\"en\">([^<]+)</span>", t, re.S)
    ar = re.search(r"<h1[^>]*>.*?<span class=\"ar\">([^<]+)</span>", t, re.S)
    img = re.search(r'/assets/images/recipes/(hero-[^"]+\.webp)', t)
    kcal = re.search(r'~(\d+)\s*kcal', t)
    serves = re.search(r'Serves (\d+)', t)
    if slug in META_FALLBACK:
        meta_en, meta_ar = META_FALLBACK[slug]
    elif kcal and serves:
        meta_en = f"~{kcal.group(1)} kcal · {serves.group(1)} servings"
        meta_ar = f"~{kcal.group(1)} سعرة · {serves.group(1)} حصص"
    else:
        meta_en, meta_ar = "Quick meal", "وجبة سريعة"
    return {
        "slug": slug,
        "en": en.group(1) if en else slug,
        "ar": ar.group(1) if ar else slug,
        "img": img.group(1) if img else f"hero-{slug}.webp",
        "meta_en": meta_en,
        "meta_ar": meta_ar,
    }


def extract_ldjson(cat_id: str) -> str:
    t = (RECIPES / f"{cat_id}.html").read_text(encoding="utf-8")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
    if not m:
        return ""
    return m.group(1).strip()


def cat_nav_html(active: str) -> str:
    items = []
    for cid, img, en, ar in CAT_NAV:
        cls = "rcp-bb-cat is-active" if cid == active else "rcp-bb-cat"
        href = f"/library/recipes/{cid}.html"
        items.append(
            f"""      <li>
        <a href="{href}" class="{cls}"{" aria-current=\"page\"" if cid == active else ""}>
          <span class="rcp-bb-cat-img"><img src="/assets/images/recipes/{img}" alt="" width="120" height="120" loading="lazy"/></span>
          <span class="rcp-bb-cat-label"><span class="en">{en}</span><span class="ar">{ar}</span></span>
        </a>
      </li>"""
        )
    items.append(
        """      <li>
        <a href="/library/recipes/" class="rcp-bb-cat">
          <span class="rcp-bb-cat-img rcp-bb-cat-img--all" aria-hidden="true">→</span>
          <span class="rcp-bb-cat-label"><span class="en">All Recipes</span><span class="ar">كل الوصفات</span></span>
        </a>
      </li>"""
    )
    return "\n".join(items)


def cards_html(recipes: list[dict]) -> str:
    out = []
    for r in recipes:
        out.append(
            f"""        <a href="/library/recipes/{r['slug']}.html" class="rcp-bb-card">
          <div class="rcp-bb-card-img"><img src="/assets/images/recipes/{r['img']}" alt="{esc(r['en'])}" width="1200" height="675" loading="lazy"/></div>
          <h3 class="rcp-bb-card-title"><span class="en">{r['en']}</span><span class="ar">{r['ar']}</span></h3>
          <p class="rcp-bb-card-meta"><span class="en">{r['meta_en']}</span><span class="ar">{r['meta_ar']}</span></p>
        </a>"""
        )
    return "\n".join(out)


def build_page(cat_id: str, cfg: dict) -> str:
    recipes = [parse_recipe(s) for s in cfg["slugs"]]
    ld = extract_ldjson(cat_id)
    disclaimer = ""
    if cfg.get("disclaimer"):
        disclaimer = """    <p class="rcp-disclaimer rcp-bb-disclaimer rcp-bb-disclaimer--banner"><span class="en">General guidance only, not medical advice. Consult your clinician for pregnancy diets.</span><span class="ar">إرشاد عام فقط وليس نصيحة طبية. استشيري طبيبك لأنظمة الحمل.</span></p>
"""

    header_html = site_header()
    footer_html = site_footer()

    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="light" data-lang="en">
<head>
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<meta charset="UTF-8"/>
{LANG_BOOT}
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta id="dfl-page-title" data-en="{esc_attr(cfg['en'])}" data-ar="{esc_attr(cfg['ar'])}"/>
<title>{cfg['en']} | DOTFORLIFE</title>
<meta name="description" content="{cfg['desc_en']}"/>
<meta name="robots" content="noindex,nofollow"/>
<link rel="canonical" href="https://dotforlife.com/library/recipes/{cat_id}.html"/>
<link rel="alternate" hreflang="ar" href="https://dotforlife.com/library/recipes/{cat_id}.html?lang=ar" />
<link rel="alternate" hreflang="en" href="https://dotforlife.com/library/recipes/{cat_id}.html?lang=en" />
<script src="/scripts/lang-redirect.js?v=20260625"></script>
{RECIPE_HEAD_ASSETS}
<script src="/scripts/global.js?v=20260625" defer></script>
<script type="application/ld+json">
{ld}
</script>
</head>
<body class="index-page recipes-page rcp-bb-home rcp-bb-category rcp-{cat_id} no-subnav">

{header_html}
{MOBILE_DROPDOWN}

<div class="rcp-bb-wrap">
  <nav class="rcp-crumb rcp-bb-crumb" aria-label="Breadcrumb">
    <a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a>
    <span aria-hidden="true">/</span>
    <a href="/library/recipes/"><span class="en">Recipes</span><span class="ar">الوصفات</span></a>
    <span aria-hidden="true">/</span>
    <span><span class="en">{cfg['en']}</span><span class="ar">{cfg['ar']}</span></span>
  </nav>

  <header class="rcp-bb-cat-banner">
    <div class="rcp-bb-cat-banner-text">
      <p class="rcp-bb-cat-banner-kicker"><span class="en">Recipes</span><span class="ar">الوصفات</span> · <span class="en">{cfg['en']}</span><span class="ar">{cfg['ar']}</span></p>
      <h1 class="rcp-bb-cat-banner-title"><span class="en">{cfg['en']}</span><span class="ar">{cfg['ar']}</span></h1>
      <p class="rcp-bb-cat-banner-desc"><span class="en">{cfg['desc_en']}</span><span class="ar">{cfg['desc_ar']}</span></p>
{disclaimer}    </div>
    <div class="rcp-bb-cat-banner-img">
      <img src="/assets/images/recipes/{cfg['banner_img']}" alt="" width="280" height="280" loading="eager"/>
    </div>
  </header>

  <nav class="rcp-bb-cats rcp-bb-cats--compact" aria-label="Recipe categories">
    <ul class="rcp-bb-cat-row">
{cat_nav_html(cat_id)}
    </ul>
  </nav>

  <main class="rcp-bb-main">
    <section class="rcp-bb-section" aria-labelledby="rcp-section-heading">
      <div class="rcp-bb-section-head">
        <h2 id="rcp-section-heading" class="rcp-bb-section-title"><span class="en">{cfg['section_en']}</span><span class="ar">{cfg['section_ar']}</span></h2>
        <span class="rcp-bb-rule" aria-hidden="true"></span>
      </div>
      <p class="rcp-bb-related"><span class="en">Related: </span><span class="ar">مرتبط: </span><a href="{cfg['related_href']}"><span class="en">{cfg['related_en']}</span><span class="ar">{cfg['related_ar']}</span></a></p>
      <div class="rcp-bb-grid">
{cards_html(recipes)}
      </div>
      <p class="rcp-bb-more-wide-row"><a href="/library/recipes/" class="rcp-bb-more-wide"><span class="en">Browse all recipes</span><span class="ar">تصفّح كل الوصفات</span></a></p>
    </section>
  </main>
</div>

{footer_html}

</body>
</html>
"""


def main():
    for cat_id, cfg in CATS.items():
        out = RECIPES / f"{cat_id}.html"
        out.write_text(build_page(cat_id, cfg), encoding="utf-8")
        print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
