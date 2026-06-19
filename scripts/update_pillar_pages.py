#!/usr/bin/env python3
"""Update pillar category pages to homepage editorial design."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CSS_LINKS = """  <link rel="stylesheet" href="/styles/global.css?v=20260626b"/>
  <link rel="stylesheet" href="/styles/home.css?v=20260619c"/>
  <link rel="stylesheet" href="/styles/home-secondary.css?v=20260619e"/>
  <link rel="stylesheet" href="/styles/home-refined.css?v=20260622c"/>
  <link rel="stylesheet" href="/styles/home-vision.css?v=20260623b"/>
  <link rel="stylesheet" href="/styles/pillar-pages.css?v=20260626a"/>
"""

PILLARS = {
    "health.html": {
        "cat": "cat-health",
        "nav_href": "health.html",
        "hero_img": "/health-hero.webp",
        "eyebrow_en": "Health & Wellbeing",
        "eyebrow_ar": "الصحة والعافية",
        "headline_en": "Your family's health,<br>understood and supported.",
        "headline_ar": "صحة أسرتك،<br>مفهومة ومدعومة.",
        "sub_en": "BMI, pregnancy, nutrition, and hydration — free tools built for Gulf climate and family life.",
        "sub_ar": "BMI والحمل والتغذية والترطيب — أدوات مجانية صُممت لمناخ الخليج وحياة الأسرة.",
        "ribbon_en": "Free calculators · Private · Bilingual",
        "ribbon_ar": "حاسبات مجانية · خاص · ثنائي اللغة",
        "cta2_en": "All tools",
        "cta2_ar": "كل الأدوات",
        "cta2_href": "/library.html?cat=health",
    },
    "finance.html": {
        "cat": "cat-finance",
        "nav_href": "finance.html",
        "hero_img": "/finance-hero.webp",
        "eyebrow_en": "Finance & Wealth",
        "eyebrow_ar": "المالية والثروة",
        "headline_en": "Your money decisions,<br>clear and confident.",
        "headline_ar": "قراراتك المالية،<br>واضحة وواثقة.",
        "sub_en": "Mortgage, Zakat, savings, and budget tools — practical calculators for Gulf families.",
        "sub_ar": "التمويل والزكاة والادخار والميزانية — حاسبات عملية للعائلات الخليجية.",
        "ribbon_en": "Sharia-aware · Free · No sign-up",
        "ribbon_ar": "متوافق شرعاً · مجاني · بدون تسجيل",
        "cta2_en": "All tools",
        "cta2_ar": "كل الأدوات",
        "cta2_href": "/library.html?cat=finance",
    },
    "real-estate.html": {
        "cat": "cat-real-estate",
        "nav_href": "real-estate.html",
        "hero_img": "/realestate-hero.webp",
        "eyebrow_en": "Real Estate",
        "eyebrow_ar": "العقار",
        "headline_en": "Home and property,<br>decisions made simple.",
        "headline_ar": "المنزل والعقار،<br>قرارات ببساطة.",
        "sub_en": "Rent vs buy, ROI, rental yield, and mortgage — guides and calculators for Gulf property.",
        "sub_ar": "إيجار أم شراء، العائد، الإيجار، والتمويل — أدلة وحاسبات للعقار في الخليج.",
        "ribbon_en": "GCC cities · Free tools · Bilingual",
        "ribbon_ar": "مدن الخليج · أدوات مجانية · ثنائي اللغة",
        "cta2_en": "All tools",
        "cta2_ar": "كل الأدوات",
        "cta2_href": "/library.html?cat=real-estate",
    },
    "travel.html": {
        "cat": "cat-travel",
        "nav_href": "travel.html",
        "hero_img": "/travel-hero.webp",
        "eyebrow_en": "Travel",
        "eyebrow_ar": "السفر",
        "headline_en": "Every journey,<br>planned with confidence.",
        "headline_ar": "كل رحلة،<br>مخطّطة بثقة وراحة.",
        "sub_en": "Packing lists, budgets, currency, and hotel cards — travel tools for family trips and Umrah.",
        "sub_ar": "قوائم الحقيبة والميزانيات والعملات وبطاقات الفندق — أدوات سفر للرحلات العائلية والعمرة.",
        "ribbon_en": "Family trips · Umrah ready · Free",
        "ribbon_ar": "رحلات عائلية · جاهز للعمرة · مجاني",
        "cta2_en": "All tools",
        "cta2_ar": "كل الأدوات",
        "cta2_href": "/library.html?cat=travel",
    },
    "islamic.html": {
        "cat": "cat-islamic",
        "nav_href": "islamic.html",
        "hero_img": "/islamic-hero.webp",
        "eyebrow_en": "Islamic Life",
        "eyebrow_ar": "الحياة الإسلامية",
        "headline_en": "Your faith, supported<br>through every day.",
        "headline_ar": "إيمانك حاضر،<br>في تفاصيل يومك.",
        "sub_en": "Prayer times, Qibla, Hijri dates, Zakat, and inheritance — daily tools for spiritual life.",
        "sub_ar": "أوقات الصلاة والقبلة والتاريخ الهجري والزكاة والميراث — أدوات يومية للحياة الروحية.",
        "ribbon_en": "Accurate · Private · Bilingual",
        "ribbon_ar": "دقيق · خاص · ثنائي اللغة",
        "cta2_en": "All tools",
        "cta2_ar": "كل الأدوات",
        "cta2_href": "/library.html?cat=islamic",
    },
}


def hero_html(p: dict) -> str:
    return f"""  <section id="hero" class="hero-editorial hero-pillar" aria-label="Hero section">
    <div class="hero-inner">
      <div class="hero-left">
        <p class="hero-eyebrow"><span class="en">{p['eyebrow_en']}</span><span class="ar">{p['eyebrow_ar']}</span></p>
        <h1 class="hero-headline">
          <span class="en">{p['headline_en']}</span>
          <span class="ar">{p['headline_ar']}</span>
        </h1>
        <p class="hero-sub">
          <span class="en">{p['sub_en']}</span>
          <span class="ar">{p['sub_ar']}</span>
        </p>
        <div class="hero-cta-row">
          <a href="#tools" class="btn-primary">
            <span class="en">Explore tools</span>
            <span class="ar">استكشف الأدوات</span>
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
          </a>
          <a href="{p['cta2_href']}" class="btn-outline">
            <span class="en">{p['cta2_en']}</span>
            <span class="ar">{p['cta2_ar']}</span>
          </a>
        </div>
        <p class="hero-trust-line" aria-hidden="true">
          <span><span class="en">Free forever</span><span class="ar">مجاني دائماً</span></span>
          <span><span class="en">Bilingual</span><span class="ar">عربي · English</span></span>
          <span><span class="en">Private by design</span><span class="ar">خصوصيتك محفوظة</span></span>
        </p>
      </div>
      <div class="hero-right" aria-hidden="true">
        <div class="hero-circle-wrap">
          <div class="hero-badge" aria-hidden="true">
            <div class="hero-badge-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            <div>
              <div class="hero-badge-label"><span class="en">Always with you</span><span class="ar">دائماً معك</span></div>
              <div class="hero-badge-value"><span class="en">Free · Private</span><span class="ar">مجاني · خاص</span></div>
            </div>
          </div>
          <div class="hero-circle">
            <img src="{p['hero_img']}" alt="DOTFORLIFE" width="900" height="900" loading="eager" fetchpriority="high" decoding="async"/>
          </div>
        </div>
      </div>
    </div>
    <div class="pillar-hero-ribbon">
      <div class="pillar-hero-ribbon-inner">
        <span class="en">{p['ribbon_en']}</span>
        <span class="ar">{p['ribbon_ar']}</span>
      </div>
    </div>
  </section>"""


def update_file(name: str, p: dict) -> None:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")

    # CSS links
    text = re.sub(
        r'  <link rel="stylesheet" href="/styles/global\.css[^"]*"/>\s*\n\s*<link rel="stylesheet" href="/styles/home\.css[^"]*">',
        CSS_LINKS.strip(),
        text,
        count=1,
    )

    # Body class
    text = re.sub(
        r'<body class="index-page category-page cat-[^"]+">',
        f'<body class="index-page category-page has-subnav {p["cat"]}">',
        text,
    )

    # Nav active + lang toggle fix
    nav_items = [
        ("health.html", "Health", "الصحة"),
        ("finance.html", "Finance", "المالية"),
        ("real-estate.html", "Real Estate", "العقار"),
        ("travel.html", "Travel", "السفر"),
        ("islamic.html", "Islamic", "الإسلامية"),
    ]
    for href, en, ar in nav_items:
        pattern = rf'<li><a href="{re.escape(href)}"[^>]*><span class="en">{en}</span><span class="ar">{ar}</span></a></li>'
        if href == p["nav_href"]:
            repl = f'<li><a href="{href}" aria-current="page"><span class="en">{en}</span><span class="ar">{ar}</span></a></li>'
        else:
            repl = f'<li><a href="{href}"><span class="en">{en}</span><span class="ar">{ar}</span></a></li>'
        text = re.sub(pattern, repl, text)

    text = re.sub(
        r'<button class="nav-btn" id="lang-toggle"[^>]*><span class="en">English</span><span class="ar">عربي</span></button>',
        '<button class="nav-btn" id="lang-toggle" aria-label="Switch language"><span class="en">عربي</span><span class="ar">English</span></button>',
        text,
    )

    # Replace hero section
    text = re.sub(
        r'  <!-- ═══════════════════════════════════════\s*\n       HERO\s*\n  ═══════════════════════════════════════ -->\s*\n  <section id="hero"[^>]*>.*?</section>',
        hero_html(p),
        text,
        count=1,
        flags=re.DOTALL,
    )

    # Remove inline style block after hero (PAGE design system)
    text = re.sub(
        r'<style>\s*/\* ═+[\s\S]*?PAGE — BODY DESIGN SYSTEM[\s\S]*?</style>\s*',
        '',
        text,
        count=1,
    )

    path.write_text(text, encoding="utf-8")
    print(f"Updated {name}")


def main():
    for name, cfg in PILLARS.items():
        update_file(name, cfg)


if __name__ == "__main__":
    main()
