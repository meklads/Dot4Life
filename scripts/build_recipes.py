#!/usr/bin/env python3
"""Generate static recipe pages from library/recipes/recipes.json."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "library" / "recipes" / "recipes.json"
OUT_DIR = ROOT / "library" / "recipes"

BUDGET_LABELS = {
    "low": {"en": "Low budget", "ar": "ميزانية منخفضة"},
    "medium": {"en": "Medium budget", "ar": "ميزانية متوسطة"},
    "high": {"en": "High budget", "ar": "ميزانية مرتفعة"},
}

HEAD_COMMON = """<script>(function(){var p=new URLSearchParams(location.search),gd=(function(){try{var z=(Intl.DateTimeFormat().resolvedOptions().timeZone||"");return /Riyadh|Dubai|Qatar|Bahrain|Kuwait|Muscat|Baghdad|Amman|Beirut|Damascus|Aden|Cairo|Khartoum/i.test(z)?"ar":"en";}catch(e){return "ar";}})(),l=p.get("lang")||localStorage.getItem("dfl-lang")||gd,t=p.get("theme")||localStorage.getItem("dfl-theme")||"light",h=document.documentElement;h.setAttribute("data-theme",t);h.setAttribute("data-lang",l);h.setAttribute("lang",l);h.setAttribute("dir",l==="ar"?"rtl":"ltr");if(p.get("lang"))localStorage.setItem("dfl-lang",l);if(p.get("theme"))localStorage.setItem("dfl-theme",t);})()</script>"""

NAV = """
<nav id="navbar" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/index.html" class="nav-logo" aria-label="DOTFORLIFE Home">
      <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="100" height="100" style="height:100px;width:auto;object-fit:contain;" loading="lazy">
    </a>
    <ul class="nav-links">
      <li><a href="/health.html"><span class="en">Health</span><span class="ar">الصحة</span></a></li>
      <li><a href="/finance.html"><span class="en">Finance</span><span class="ar">المالية</span></a></li>
      <li><a href="/real-estate.html"><span class="en">Real Estate</span><span class="ar">العقار</span></a></li>
      <li><a href="/travel.html"><span class="en">Travel</span><span class="ar">السفر</span></a></li>
      <li><a href="/islamic.html"><span class="en">Islamic</span><span class="ar">الإسلامية</span></a></li>
      <li><a href="/about.html"><span class="en">About</span><span class="ar">عنّا</span></a></li>
      <li><a href="/archive.html"><span class="en">Archive</span><span class="ar">الأرشيف</span></a></li>
      <li><a href="/blog.html"><span class="en">Blog</span><span class="ar">المدونة</span></a></li>
      <li><a href="/library.html" aria-current="page"><span class="en">Library</span><span class="ar">المكتبة</span></a></li>
    </ul>
    <div class="nav-controls">
      <button class="nav-btn" id="lang-toggle" aria-label="Switch language"><span class="en">عربي</span><span class="ar">English</span></button>
      <button class="nav-btn" id="theme-toggle" aria-label="Toggle theme"><svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></button>
    </div>
  </div>
</nav>
"""

FOOTER = """
<footer class="site-footer" role="contentinfo">
  <div class="footer-accent" aria-hidden="true"></div>
  <div class="footer-inner">
    <div class="footer-main">
      <div class="footer-brand">
        <a href="/" class="footer-logo" aria-label="DOTFORLIFE">
          <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="auto" loading="lazy">
        </a>
        <p class="footer-tagline"><span class="en">One calm place for your family's everyday decisions. Free, always.</span><span class="ar">مكان هادئ واحد لقرارات عائلتك اليومية. مجاني دائماً.</span></p>
      </div>
      <div class="footer-links-grid">
        <div class="footer-col">
          <h4><span class="en">Life</span><span class="ar">الحياة</span></h4>
          <ul>
            <li><a href="/health.html"><span class="en">Health</span><span class="ar">الصحة</span></a></li>
            <li><a href="/finance.html"><span class="en">Finance</span><span class="ar">المالية</span></a></li>
            <li><a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Recipes</span><span class="ar">الوصفات</span></h4>
          <ul>
            <li><a href="/library/recipes/"><span class="en">Featured Recipes</span><span class="ar">وصفات مميزة</span></a></li>
            <li><a href="/library/recipes/pregnancy.html"><span class="en">Pregnancy</span><span class="ar">للحامل</span></a></li>
            <li><a href="/library/recipes/budget.html"><span class="en">Budget</span><span class="ar">اقتصادية</span></a></li>
            <li><a href="/library/recipes/quick.html"><span class="en">Quick</span><span class="ar">سريعة</span></a></li>
            <li><a href="/library/recipes/family.html"><span class="en">Family</span><span class="ar">للعائلة</span></a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span class="footer-copy">© 2026 DOTFORLIFE · <span class="en">Free for families, always.</span><span class="ar">مجاني للعائلات، دائماً.</span></span>
    </div>
  </div>
</footer>
<script src="/scripts/global.js?v=20260625" defer></script>
"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def bi(field: dict) -> str:
    return (
        f'<span class="en">{esc(field["en"])}</span>'
        f'<span class="ar">{esc(field["ar"])}</span>'
    )


def page_shell(
    *,
    title_en: str,
    title_ar: str,
    desc_en: str,
    desc_ar: str,
    canonical: str,
    body_class: str,
    content: str,
    noindex: bool,
) -> str:
    robots = '<meta name="robots" content="noindex,nofollow"/>' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr" data-theme="light" data-lang="en">
<head>
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<meta charset="UTF-8"/>
{HEAD_COMMON}
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{esc(title_en)} | {esc(title_ar)} | DOTFORLIFE</title>
<meta name="description" content="{esc(desc_en)}"/>
{robots}
<link rel="canonical" href="https://dotforlife.com{canonical}"/>
<link rel="alternate" hreflang="ar" href="https://dotforlife.com{canonical}?lang=ar" />
<link rel="alternate" hreflang="en" href="https://dotforlife.com{canonical}?lang=en" />
<script src="/scripts/lang-redirect.js?v=20260625"></script>
<link rel="stylesheet" href="/styles/global.css?v=20260624n"/>
<link rel="stylesheet" href="/styles/pages/library.css?v=20260708a"/>
<link rel="stylesheet" href="/styles/pages/recipes.css?v=20260708a"/>
<script src="/scripts/global.js?v=20260625" defer></script>
</head>
<body class="library-page recipes-page {body_class}">
{NAV}
{content}
{FOOTER}
</body>
</html>
"""


def recipe_meta_chips(recipe: dict) -> str:
    total = recipe["prepMinutes"] + recipe["cookMinutes"]
    budget = BUDGET_LABELS[recipe["budget"]]
    return f"""
<div class="rcp-meta">
  <span class="rcp-chip"><span class="en">{total} min</span><span class="ar">{total} د</span></span>
  <span class="rcp-chip"><span class="en">{recipe['servings']} servings</span><span class="ar">{recipe['servings']} حصص</span></span>
  <span class="rcp-chip">{bi(recipe['difficulty'])}</span>
  <span class="rcp-chip rcp-chip--budget">{bi(budget)}</span>
</div>"""


def recipe_card(recipe: dict, cat_title: dict) -> str:
    benefit = recipe.get("benefit", {})
    return f"""
<a href="/library/recipes/{esc(recipe['slug'])}.html" class="lib-card lib-card--recipe">
  <p class="lib-card-kicker">{bi(cat_title)}</p>
  <h3 class="lib-card-title">{bi(recipe['title'])}</h3>
  <p class="lib-card-desc">{bi(recipe['desc'])}</p>
  <p class="rcp-benefit">{bi(benefit)}</p>
  {recipe_meta_chips(recipe)}
  <span class="lib-card-arrow"><span class="en">Open →</span><span class="ar">← افتح</span></span>
</a>"""


def recipes_tabs(active: str) -> str:
    tabs = [
        ("hub", "/library/recipes/", "All Recipes", "كل الوصفات"),
        ("pregnancy", "/library/recipes/pregnancy.html", "Pregnancy", "للحامل"),
        ("budget", "/library/recipes/budget.html", "Budget", "اقتصادية"),
        ("quick", "/library/recipes/quick.html", "Quick", "سريعة"),
        ("family", "/library/recipes/family.html", "Family", "للعائلة"),
    ]
    items = []
    for key, href, en, ar in tabs:
        cls = "rcp-tab is-active" if key == active else "rcp-tab"
        items.append(
            f'<a href="{href}" class="{cls}">'
            f'<span class="en">{esc(en)}</span><span class="ar">{esc(ar)}</span></a>'
        )
    return f'<div class="rcp-tabs-wrap"><div class="rcp-tabs-inner">{"".join(items)}</div></div>'


def hero_block(eyebrow_en: str, eyebrow_ar: str, title: dict, sub: dict) -> str:
    return f"""
<header class="lib-hero rcp-hero">
  <div class="lib-hero-inner">
    <nav class="rcp-crumb" aria-label="Breadcrumb">
      <a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a>
      <span aria-hidden="true">/</span>
      <a href="/library/recipes/"><span class="en">Featured Recipes</span><span class="ar">وصفات مميزة</span></a>
    </nav>
    <p class="lib-eyebrow"><span class="en">{esc(eyebrow_en)}</span><span class="ar">{esc(eyebrow_ar)}</span></p>
    <h1 class="lib-title">{bi(title)}</h1>
    <p class="lib-sub">{bi(sub)}</p>
  </div>
</header>
"""


def list_block(items: list[str], lang_key: str) -> str:
    lis = "".join(f"<li>{esc(item)}</li>" for item in items)
    return f"<ul>{lis}</ul>"


def build_index(data: dict, noindex: bool) -> str:
    cats = data["categories"]
    cards = []
    for cat in cats:
        count = sum(1 for r in data["recipes"] if r["category"] == cat["id"])
        cards.append(
            f"""
<a href="/library/recipes/{esc(cat['slug'])}.html" class="lib-card rcp-cat-card">
  <p class="lib-card-kicker"><span class="en">Category</span><span class="ar">فئة</span></p>
  <h3 class="lib-card-title">{bi(cat['title'])}</h3>
  <p class="lib-card-desc">{bi(cat['desc'])}</p>
  <p class="rcp-benefit">{bi(cat['benefit'])}</p>
  <span class="rcp-count"><span class="en">{count} recipes</span><span class="ar">{count} وصفات</span></span>
  <span class="lib-card-arrow"><span class="en">Browse →</span><span class="ar">← تصفّح</span></span>
</a>"""
        )

    content = f"""
<header class="lib-hero rcp-hero">
  <div class="lib-hero-inner">
    <nav class="rcp-crumb" aria-label="Breadcrumb">
      <a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a>
      <span aria-hidden="true">/</span>
      <span><span class="en">Featured Recipes</span><span class="ar">وصفات مميزة</span></span>
    </nav>
    <p class="lib-eyebrow"><span class="en">Library · Lifestyle</span><span class="ar">المكتبة · أسلوب حياة</span></p>
    <h1 class="lib-title"><span class="en">Featured Recipes</span><span class="ar">وصفات مميزة</span></h1>
    <p class="lib-sub"><span class="en">Practical meals for real family needs — pregnancy, budget, speed, and shared tables.</span><span class="ar">وجبات عملية لاحتياجات العائلة الحقيقية — الحمل، الميزانية، السرعة، والمائدة المشتركة.</span></p>
    <p class="rcp-disclaimer"><span class="en">General guidance only — not medical advice. Consult your clinician for pregnancy or health diets.</span><span class="ar">إرشاد عام فقط — ليس نصيحة طبية. استشيري طبيبك لأنظمة الحمل أو الصحة.</span></p>
  </div>
</header>
{recipes_tabs("hub")}
<main class="lib-main">
  <section class="lib-section">
    <div class="lib-section-head">
      <h2 class="lib-section-title"><span class="en">Browse by need</span><span class="ar">تصفّح حسب الحاجة</span></h2>
      <span class="lib-section-count">{len(cats)}</span>
    </div>
    <div class="lib-grid">{''.join(cards)}</div>
  </section>
</main>
"""
    return page_shell(
        title_en="Featured Recipes",
        title_ar="وصفات مميزة",
        desc_en="Practical recipe library for Gulf families — pregnancy, budget, quick, and family meals.",
        desc_ar="مكتبة وصفات عملية للعائلات الخليجية — حمل، ميزانية، سرعة، ووجبات عائلية.",
        canonical="/library/recipes/",
        body_class="rcp-index",
        content=content,
        noindex=noindex,
    )


def build_category(data: dict, cat: dict, noindex: bool) -> str:
    recipes = [r for r in data["recipes"] if r["category"] == cat["id"]]
    cards = "".join(recipe_card(r, cat["title"]) for r in recipes)
    content = f"""
{hero_block("Featured Recipes", "وصفات مميزة", cat["title"], cat["desc"])}
{recipes_tabs(cat["slug"])}
<main class="lib-main">
  <section class="lib-section">
    <div class="lib-section-head">
      <h2 class="lib-section-title">{bi(cat['title'])}</h2>
      <span class="lib-section-count">{len(recipes)}</span>
    </div>
    <p class="rcp-related-link"><span class="en">Related: </span><span class="ar">مرتبط: </span><a href="{esc(cat['relatedLink'])}">{bi(cat['relatedLabel'])}</a></p>
    <div class="lib-grid">{cards}</div>
  </section>
</main>
"""
    return page_shell(
        title_en=cat["title"]["en"],
        title_ar=cat["title"]["ar"],
        desc_en=cat["desc"]["en"],
        desc_ar=cat["desc"]["ar"],
        canonical=f"/library/recipes/{cat['slug']}.html",
        body_class=f"rcp-category rcp-{cat['slug']}",
        content=content,
        noindex=noindex,
    )


def build_recipe(data: dict, recipe: dict, cat: dict, noindex: bool) -> str:
    by_slug = {r["slug"]: r for r in data["recipes"]}
    placeholder = data["meta"]["placeholderImage"]
    total = recipe["prepMinutes"] + recipe["cookMinutes"]
    budget = BUDGET_LABELS[recipe["budget"]]
    tags_html = "".join(
        f'<span class="rcp-tag"><span class="en">{esc(t)}</span></span>'
        for t in recipe["tags"]["en"]
    )
    tags_html += "".join(
        f'<span class="rcp-tag"><span class="ar">{esc(t)}</span></span>'
        for t in recipe["tags"]["ar"]
    )

    related_cards = []
    for slug in recipe.get("related", [])[:3]:
        rel = by_slug.get(slug)
        if rel:
            related_cards.append(
                f'<a href="/library/recipes/{esc(slug)}.html" class="rcp-related-item">{bi(rel["title"])}</a>'
            )

    content = f"""
<header class="rcp-recipe-hero">
  <div class="rcp-recipe-hero-inner">
    <nav class="rcp-crumb" aria-label="Breadcrumb">
      <a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a>
      <span>/</span>
      <a href="/library/recipes/"><span class="en">Recipes</span><span class="ar">وصفات</span></a>
      <span>/</span>
      <a href="/library/recipes/{esc(cat['slug'])}.html">{bi(cat['title'])}</a>
    </nav>
    <div class="rcp-recipe-hero-grid">
      <div class="rcp-recipe-media">
        <img src="{esc(placeholder)}" alt="" width="1200" height="675" loading="eager" class="rcp-hero-img"/>
      </div>
      <div class="rcp-recipe-intro">
        <p class="lib-eyebrow">{bi(cat['title'])}</p>
        <h1 class="lib-title">{bi(recipe['title'])}</h1>
        <p class="lib-sub">{bi(recipe['intro'])}</p>
        <div class="rcp-meta rcp-meta--hero">
          <span class="rcp-chip"><span class="en">Prep {recipe['prepMinutes']}m</span><span class="ar">تحضير {recipe['prepMinutes']} د</span></span>
          <span class="rcp-chip"><span class="en">Cook {recipe['cookMinutes']}m</span><span class="ar">طبخ {recipe['cookMinutes']} د</span></span>
          <span class="rcp-chip"><span class="en">Total {total}m</span><span class="ar">الإجمالي {total} د</span></span>
          <span class="rcp-chip">{bi(recipe['difficulty'])}</span>
          <span class="rcp-chip rcp-chip--budget">{bi(budget)}</span>
        </div>
        <p class="rcp-benefit rcp-benefit--hero">{bi(recipe['benefit'])}</p>
        <div class="rcp-tags">{tags_html}</div>
      </div>
    </div>
  </div>
</header>
<main class="lib-main rcp-recipe-main">
  <div class="rcp-recipe-layout">
    <section class="rcp-block">
      <h2><span class="en">Ingredients</span><span class="ar">المكوّنات</span></h2>
      <div class="rcp-lang-block"><span class="en">{list_block(recipe['ingredients']['en'], 'en')}</span><span class="ar">{list_block(recipe['ingredients']['ar'], 'ar')}</span></div>
    </section>
    <section class="rcp-block">
      <h2><span class="en">Steps</span><span class="ar">الخطوات</span></h2>
      <div class="rcp-lang-block"><span class="en">{list_block(recipe['steps']['en'], 'en')}</span><span class="ar">{list_block(recipe['steps']['ar'], 'ar')}</span></div>
    </section>
    <section class="rcp-block">
      <h2><span class="en">Tips &amp; variations</span><span class="ar">نصائح وتنويعات</span></h2>
      <div class="rcp-lang-block"><span class="en">{list_block(recipe['tips']['en'], 'en')}</span><span class="ar">{list_block(recipe['tips']['ar'], 'ar')}</span></div>
    </section>
    <aside class="rcp-aside">
      <div class="rcp-aside-card">
        <h3><span class="en">Related tool</span><span class="ar">أداة مرتبطة</span></h3>
        <a href="{esc(recipe['relatedArticle'])}">{bi(recipe['relatedArticleLabel'])}</a>
      </div>
      <div class="rcp-aside-card">
        <h3><span class="en">Related recipes</span><span class="ar">وصفات ذات صلة</span></h3>
        <div class="rcp-related-list">{''.join(related_cards)}</div>
      </div>
      <p class="rcp-disclaimer rcp-disclaimer--small"><span class="en">Estimated costs and nutrition are general guides only.</span><span class="ar">التكاليف والتغذية تقديرات إرشادية فقط.</span></p>
    </aside>
  </div>
</main>
"""
    return page_shell(
        title_en=recipe["title"]["en"],
        title_ar=recipe["title"]["ar"],
        desc_en=recipe["desc"]["en"],
        desc_ar=recipe["desc"]["ar"],
        canonical=f"/library/recipes/{recipe['slug']}.html",
        body_class="rcp-detail",
        content=content,
        noindex=noindex,
    )


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    noindex = bool(data["meta"].get("noindex", True))
    cats_by_id = {c["id"]: c for c in data["categories"]}

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    (OUT_DIR / "index.html").write_text(build_index(data, noindex), encoding="utf-8")

    for cat in data["categories"]:
        path = OUT_DIR / f"{cat['slug']}.html"
        path.write_text(build_category(data, cat, noindex), encoding="utf-8")

    for recipe in data["recipes"]:
        cat = cats_by_id[recipe["category"]]
        path = OUT_DIR / f"{recipe['slug']}.html"
        path.write_text(build_recipe(data, recipe, cat, noindex), encoding="utf-8")

    print(f"Built {1 + len(data['categories']) + len(data['recipes'])} recipe pages in {OUT_DIR}")


if __name__ == "__main__":
    main()
