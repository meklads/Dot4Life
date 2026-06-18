#!/usr/bin/env python3
"""
Batch 4: Full BOOM compliance for 6 articles.
These articles lack article-layout, sidebar, article-end sections entirely.
We need to completely restructure them.
"""

import re, os

BLOG = "/Users/ghousemac/Desktop/Turriva/d4l/Dot4Life/blog"

# ─── Helper: extract language from bilingual spans ─────────────
def extract_ar(body):
    """Extract Arabic from <span class="en">EN</span><span class="ar">AR</span> pairs"""
    cleaned = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">(.*?)</span>', r'\2', body, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="ar">(.*?)</span>\s*<span class="en">(.*?)</span>', r'\1', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="en">.*?</span>', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="ar">(.*?)</span>', r'\1', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<p>\s*</p>', '', cleaned)
    cleaned = re.sub(r'<li>\s*</li>', '', cleaned)
    return cleaned.strip()


def extract_en(body):
    """Extract English from <span class="en">EN</span><span class="ar">AR</span> pairs"""
    cleaned = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">.*?</span>', r'\1', body, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="ar">(.*?)</span>\s*<span class="en">(.*?)</span>', r'\2', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="ar">.*?</span>', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="en">(.*?)</span>', r'\1', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<p>\s*</p>', '', cleaned)
    cleaned = re.sub(r'<li>\s*</li>', '', cleaned)
    return cleaned.strip()


def has_bilingual_spans(body):
    return '<span class="en">' in body and '<span class="ar">' in body


# ─── Helper: extract h2 headings and add ids ──────────────────
def get_h2_headings(body):
    """Extract h2 headings and generate ids"""
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', body)
    result = []
    for h in h2s:
        h_clean = re.sub(r'<[^>]+>', '', h).strip()
        h_id = h_clean.replace(' ', '-')
        h_id = re.sub(r'[^؀-ۿ\w-]', '', h_id)
        h_id = re.sub(r'-+', '-', h_id).strip('-')
        if not h_id:
            h_id = f"section-{len(result)+1}"
        result.append((h_clean, h_id))
    return result


def add_ids_to_headings(body, toc_items):
    """Add id attributes to h2 headings"""
    for htext, hid in toc_items:
        # Try various patterns
        for space in ['', ' ']:
            for space2 in ['', ' ']:
                pat = f'<h2>{space}{htext}{space2}</h2>'
                if pat in body:
                    body = body.replace(pat, f'<h2 id="{hid}">{htext}</h2>', 1)
                    break
            else:
                continue
            break
    return body


# ─── Article configuration ────────────────────────────────────
ARTICLES = [
    {
        "name": "saudi-mortgage-guide-2025",
        "title_ar": "أفضل تمويل عقاري في السعودية 2025, مقارنة البنوك والشروط",
        "title_en": "Best Mortgage in Saudi Arabia 2025: Bank Comparison & Requirements",
        "desc_ar": "دليل شامل لأفضل تمويل عقاري في السعودية 2025 — مقارنة البنوك، الشروط، والأهلية.",
        "desc_en": "Complete guide to mortgage financing in Saudi Arabia 2025 — bank comparisons, requirements, eligibility.",
        "tags_ar": ["#تمويل", "#عقار", "#السعودية", "#بنوك"],
        "tags_en": ["#mortgage", "#realestate", "#saudi", "#finance"],
        "cta_ar": {"title": "احسب تمويلك العقاري", "desc": "قارن بين عروض البنوك واحسب أقساطك الشهرية.", "btn": "احسب الآن ←", "link": "/tools/mortgage-calculator.html"},
        "cta_en": {"title": "Calculate Your Mortgage", "desc": "Compare bank offers and calculate monthly payments.", "btn": "Calculate Now →", "link": "/tools/mortgage-calculator.html"},
        "sidebar_tools_ar": [("حاسبة التمويل", "/tools/mortgage-calculator.html"), ("حاسبة الزكاة", "/tools/zakat-calculator.html"), ("محول التاريخ", "/tools/hijri-converter.html")],
        "sidebar_tools_en": [("Mortgage Calculator", "/tools/mortgage-calculator.html"), ("Zakat Calculator", "/tools/zakat-calculator.html"), ("Hijri Converter", "/tools/hijri-converter.html")],
        "read_also_ar": [
            ("دليل شراء المنزل للموظف الوحيد", "/blog/house-affordability-single-income-guide.html"),
            ("محور الحياة المالية للعائلة", "/blog/complete-gulf-family-financial-life-hub-ar.html"),
            ("نظام الميزانية المنزلية", "/blog/complete-household-budget-system-ar.html"),
        ],
        "read_also_en": [
            ("Our Complete Mortgage Guide", "/blog/saudi-mortgage-guide-2025-en.html"),
            ("House Affordability for Single Income", "/blog/house-affordability-single-income-guide.html"),
            ("Gulf Family Finance Hub", "/blog/complete-gulf-family-financial-life-hub.html"),
        ],
    },
    {
        "name": "gcc-family-budget-2025",
        "title_ar": "ميزانية الأسرة الخليجية 2025: دليل شامل",
        "title_en": "GCC Family Budget 2025: Complete Financial Planning",
        "desc_ar": "دليل شامل لميزانية الأسرة في دول الخليج 2025 — تخطيط، إدارة، وتوفير.",
        "desc_en": "Complete GCC family budget guide for 2025 — planning, management, and saving strategies.",
        "tags_ar": ["#ميزانية", "#عائلة", "#مالية", "#توفير"],
        "tags_en": ["#budget", "#family", "#finance", "#savings"],
        "cta_ar": {"title": "خطط لميزانية أسرتك", "desc": "استخدم أدواتنا للتخطيط المالي العائلي.", "btn": "ابدأ التخطيط ←", "link": "/tools/budget-calculator.html"},
        "cta_en": {"title": "Plan Your Family Budget", "desc": "Use our tools for family financial planning.", "btn": "Start Planning →", "link": "/tools/budget-calculator.html"},
        "sidebar_tools_ar": [("حاسبة الميزانية", "/tools/budget-calculator.html"), ("حاسبة الزكاة", "/tools/zakat-calculator.html"), ("محول التاريخ", "/tools/hijri-converter.html")],
        "sidebar_tools_en": [("Budget Calculator", "/tools/budget-calculator.html"), ("Zakat Calculator", "/tools/zakat-calculator.html"), ("Hijri Converter", "/tools/hijri-converter.html")],
        "read_also_ar": [
            ("محور الحياة المالية للعائلة", "/blog/complete-gulf-family-financial-life-hub-ar.html"),
            ("نظام الميزانية المنزلية", "/blog/complete-household-budget-system-ar.html"),
            ("صندوق الطوارئ المالي", "/blog/emergency-fund-calculator-guide.html"),
        ],
        "read_also_en": [
            ("Gulf Family Finance Hub", "/blog/complete-gulf-family-financial-life-hub.html"),
            ("Household Budget System", "/blog/complete-household-budget-system.html"),
            ("Emergency Fund Guide", "/blog/emergency-fund-calculator-guide.html"),
        ],
    },
    {
        "name": "hajj-umrah-guide-2025",
        "title_ar": "دليل الحج والعمرة 2025: رحلة روحانية كاملة",
        "title_en": "Hajj and Umrah Guide 2025: Complete Spiritual Journey",
        "desc_ar": "دليل شامل للحج والعمرة 2025 — المناسك، الإجراءات، والنصائح للعائلات.",
        "desc_en": "Complete Hajj and Umrah guide for 2025 — rituals, procedures, and family tips.",
        "tags_ar": ["#حج", "#عمرة", "#إسلام", "#عبادة"],
        "tags_en": ["#hajj", "#umrah", "#islamic", "#travel"],
        "cta_ar": {"title": "خطط لرحلتك الروحانية", "desc": "احسب ميزانية الحج والعمرة بذكاء.", "btn": "احسب الآن ←", "link": "/tools/travel-budget.html"},
        "cta_en": {"title": "Plan Your Spiritual Journey", "desc": "Calculate your Hajj and Umrah budget wisely.", "btn": "Calculate Now →", "link": "/tools/travel-budget.html"},
        "sidebar_tools_ar": [("حاسبة السفر", "/tools/travel-budget.html"), ("محول التاريخ", "/tools/hijri-converter.html"), ("اتجاه القبلة", "/tools/qibla.html")],
        "sidebar_tools_en": [("Travel Budget", "/tools/travel-budget.html"), ("Hijri Converter", "/tools/hijri-converter.html"), ("Qibla Direction", "/tools/qibla.html")],
        "read_also_ar": [
            ("دليل فنادق مكة", "/blog/makkah-hotels-guide.html"),
            ("ميزانية العمرة للعائلات", "/blog/umrah-budget-guide-families.html"),
            ("دليل الزكاة", "/blog/zakat-guide-2025.html"),
        ],
        "read_also_en": [
            ("Makkah Hotels Guide", "/blog/makkah-hotels-guide-en.html"),
            ("Umrah Budget for Families", "/blog/umrah-budget-guide-families-en.html"),
            ("Zakat Guide", "/blog/zakat-guide-2025-en.html"),
        ],
    },
    {
        "name": "zakat-guide-2025",
        "title_ar": "دليل الزكاة 2025: أحكام ونسب وأمثلة عملية",
        "title_en": "Zakat Guide 2025: Rulings, Rates, and Practical Examples",
        "desc_ar": "دليل شامل لحساب الزكاة 2025 — الأنواع، النسب، والأحكام الشرعية.",
        "desc_en": "Complete Zakat guide for 2025 — types, rates, and Islamic rulings.",
        "tags_ar": ["#زكاة", "#إسلام", "#عبادة", "#صدقة"],
        "tags_en": ["#zakat", "#islamic", "#charity", "#finance"],
        "cta_ar": {"title": "احسب زكاتك بدقة", "desc": "استخدم حاسبة الزكاة لمعرفة المبلغ الواجب عليك.", "btn": "احسب الآن ←", "link": "/tools/zakat-calculator.html"},
        "cta_en": {"title": "Calculate Your Zakat", "desc": "Use the Zakat calculator to find out your due amount.", "btn": "Calculate Now →", "link": "/tools/zakat-calculator.html"},
        "sidebar_tools_ar": [("حاسبة الزكاة", "/tools/zakat-calculator.html"), ("محول التاريخ", "/tools/hijri-converter.html"), ("حاسبة السعرات", "/tools/calorie-calculator.html")],
        "sidebar_tools_en": [("Zakat Calculator", "/tools/zakat-calculator.html"), ("Hijri Converter", "/tools/hijri-converter.html"), ("Calorie Calculator", "/tools/calorie-calculator.html")],
        "read_also_ar": [
            ("دليل الزكاة للاستثمارات الحديثة", "/blog/zakat-investment-portfolios.html"),
            ("دليل الحج والعمرة", "/blog/hajj-umrah-guide-2025.html"),
            ("القسم الإسلامي", "/islamic.html"),
        ],
        "read_also_en": [
            ("Zakat for Investments", "/blog/zakat-investment-portfolios.html"),
            ("Hajj & Umrah Guide", "/blog/hajj-umrah-guide-2025-en.html"),
            ("Islamic Section", "/islamic.html"),
        ],
    },
    {
        "name": "salalah-travel-guide-2025",
        "title_ar": "دليل السفر إلى صلالة 2025: أفضل وجهة عائلية",
        "title_en": "Salalah Travel Guide 2025: Best Family Destination",
        "desc_ar": "دليل شامل للسفر إلى صلالة 2025 — الأماكن، الفنادق، والفعاليات للعائلات.",
        "desc_en": "Complete travel guide to Salalah 2025 — attractions, hotels, and family events.",
        "tags_ar": ["#صلالة", "#سفر", "#عُمان", "#عائلة"],
        "tags_en": ["#salalah", "#travel", "#oman", "#family"],
        "cta_ar": {"title": "خطط لعطلتك في صلالة", "desc": "احسب ميزانية سفرك واستكشف الوجهات.", "btn": "خطط الآن ←", "link": "/tools/travel-budget.html"},
        "cta_en": {"title": "Plan Your Salalah Trip", "desc": "Calculate your travel budget and explore destinations.", "btn": "Plan Now →", "link": "/tools/travel-budget.html"},
        "sidebar_tools_ar": [("حاسبة السفر", "/tools/travel-budget.html"), ("محول التاريخ", "/tools/hijri-converter.html"), ("حاسبة الماء", "/tools/water-calculator.html")],
        "sidebar_tools_en": [("Travel Budget", "/tools/travel-budget.html"), ("Hijri Converter", "/tools/hijri-converter.html"), ("Water Calculator", "/tools/water-calculator.html")],
        "read_also_ar": [
            ("دليل فنادق مكة", "/blog/makkah-hotels-guide.html"),
            ("أنشطة عائلية في مدن الخليج", "/blog/family-friendly-activities-gulf-cities.html"),
            ("دليل ميزانية العمرة", "/blog/umrah-budget-guide-families.html"),
        ],
        "read_also_en": [
            ("Makkah Hotels Guide", "/blog/makkah-hotels-guide-en.html"),
            ("Family Activities in Gulf", "/blog/family-friendly-activities-gulf-cities.html"),
            ("Umrah Budget Guide", "/blog/umrah-budget-guide-families-en.html"),
        ],
    },
    {
        "name": "makkah-hotels-guide",
        "title_ar": "دليل فنادق مكة 2025: أفضل الفنادق القريبة من الحرم",
        "title_en": "Makkah Hotels Guide 2025: Best Hotels Near Haram",
        "desc_ar": "دليل شامل لأفضل فنادق مكة 2025 — قريبة من الحرم، بأسعار مناسبة للعائلات.",
        "desc_en": "Complete guide to Makkah hotels 2025 — near Haram, family-friendly prices.",
        "tags_ar": ["#مكة", "#فنادق", "#عمرة", "#سفر"],
        "tags_en": ["#makkah", "#hotels", "#umrah", "#travel"],
        "cta_ar": {"title": "اختر فندقك في مكة", "desc": "قارن أسعار الفنادق القريبة من الحرم.", "btn": "قارن الأسعار ←", "link": "/tools/travel-budget.html"},
        "cta_en": {"title": "Choose Your Makkah Hotel", "desc": "Compare prices of hotels near the Haram.", "btn": "Compare Prices →", "link": "/tools/travel-budget.html"},
        "sidebar_tools_ar": [("حاسبة السفر", "/tools/travel-budget.html"), ("محول التاريخ", "/tools/hijri-converter.html"), ("اتجاه القبلة", "/tools/qibla.html")],
        "sidebar_tools_en": [("Travel Budget", "/tools/travel-budget.html"), ("Hijri Converter", "/tools/hijri-converter.html"), ("Qibla Direction", "/tools/qibla.html")],
        "read_also_ar": [
            ("دليل الحج والعمرة", "/blog/hajj-umrah-guide-2025.html"),
            ("ميزانية العمرة للعائلات", "/blog/umrah-budget-guide-families.html"),
            ("دليل صلالة", "/blog/salalah-travel-guide-2025.html"),
        ],
        "read_also_en": [
            ("Hajj & Umrah Guide", "/blog/hajj-umrah-guide-2025-en.html"),
            ("Umrah Budget for Families", "/blog/umrah-budget-guide-families-en.html"),
            ("Salalah Travel Guide", "/blog/salalah-travel-guide-2025-en.html"),
        ],
    },
]


def make_article_end(cfg, lang):
    """Generate the article-end HTML block"""
    k = lang  # 'ar' or 'en'
    cta = cfg[f"cta_{k}"]
    tags = cfg.get(f"tags_{k}", [])
    
    share = lang  # 'ar'/'en' controls dir/icon ordering but we keep consistent
    
    share_html = f"""<div class="article-share">
  <a href="#" target="_blank" rel="noopener" class="share-btn wa" aria-label="Share on WhatsApp">
    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  </a>
  <a href="#" target="_blank" rel="noopener" class="share-btn tw" aria-label="Share on X">
    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
  </a>
  <a href="#" target="_blank" rel="noopener" class="share-btn fb" aria-label="Share on Facebook">
    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
  </a>
  <button class="share-btn cp" onclick="navigator.clipboard.writeText(location.href)" aria-label="Copy link">
    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
  </button>
</div>"""
    
    cta_heading = cta['title']
    cta_desc = cta['desc']
    cta_btn = cta['btn']
    cta_link = cta['link']
    
    # Read-also
    read_items = cfg.get(f"read_also_{k}", [])
    read_cards = ""
    for title_text, link in read_items:
        read_cards += f"""    <a href="{link}" class="read-also-card">
      <span class="read-also-title">{title_text}</span>
    </a>
"""
    
    tag_items = '\n  '.join(f'<span class="tag">{t}</span>' for t in tags)
    
    # Friday CTA title depends on language
    fri_title = "📬 نصائح الجمعة العائلية" if k == "ar" else "📬 Friday Family Tips"
    fri_placeholder = "your@email.com"
    fri_alert = "🚧 قريباً — تكامل التسجيل." if k == "ar" else "🚧 Coming soon — integration."
    fri_subscribe = "اشترك" if k == "ar" else "Subscribe"
    
    read_heading = "📖 اقرأ أيضاً" if k == "ar" else "📖 Read Also"
    
    return f"""<div class="article-end">
{share_html}

<div class="article-tool-cta">
  <h3>{cta_heading}</h3>
  <p>{cta_desc}</p>
  <a href="{cta_link}" class="tool-cta-btn">{cta_btn}</a>
</div>

<div class="article-read-also">
  <h3>{read_heading}</h3>
  <div class="read-also-grid">
{read_cards}  </div>
</div>

<div class="article-friday-cta">
  <h3>{fri_title}</h3>
  <p>احصل على إلهام أسبوعي في بريدك.</p>
  <div class="friday-input-wrap">
    <input type="email" placeholder="{fri_placeholder}" aria-label="Email">
    <button onclick="alert('{fri_alert}')">{fri_subscribe}</button>
  </div>
</div>

<div class="article-tags">
  {tag_items}
</div>
</div>"""


def make_sidebar(cfg, lang, toc_items):
    """Generate sidebar HTML"""
    k = lang
    tools = cfg.get(f"sidebar_tools_{k}", [])
    read_items = cfg.get(f"read_also_{k}", [])
    
    tools_html = '\n'.join(f'  <a href="{link}" class="tool-btn">{title}</a>' for title, link in tools)
    
    toc_links = '\n'.join(f'  <a href="#{hid}" class="toc-item">{htext}</a>' for htext, hid in toc_items)
    
    related_html = ""
    for i, (title_text, link) in enumerate(read_items[:3]):
        imgs = [
            "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=64&h=48&q=80",
            "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=64&h=48&q=80",
            "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=64&h=48&q=80",
        ]
        img = imgs[i % 3]
        related_html += f"""  <div class="sidebar-related-item">
    <img src="{img}" alt="" width="64" height="48" loading="lazy">
    <div>
      <div class="related-title"><a href="{link}">{title_text}</a></div>
    </div>
  </div>
"""
    
    return f"""<aside class="article-sidebar">
<div class="sidebar-module sidebar-team-card">
  <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="56" height="56" loading="lazy">
  <div class="team-name">فريق دوت فور لايف</div>
  <div class="team-trust">محتوى موثوق، بعناية للعائلات الخليجية.</div>
  <a href="/editorial-standards.html" class="team-link">معاييرنا التحريرية ←</a>
</div>

<div class="sidebar-module sidebar-toc">
  <h4>📑 المحتويات</h4>
{toc_links}
</div>

<div class="sidebar-module sidebar-related">
  <h4>ذات صلة</h4>
{related_html}</div>

<div class="sidebar-module sidebar-tools">
  <h4>🛠 أدوات</h4>
{tools_html}
</div>
</aside>"""


def process_article(config):
    name = config["name"]
    print(f"\n{'='*60}")
    print(f"📄 Processing: {name}")
    print(f"{'='*60}")
    
    for lang in ["ar", "en"]:
        suffix = "" if lang == "ar" else "-en"
        path = f"{BLOG}/{name}{suffix}.html"
        
        if not os.path.exists(path):
            print(f"  {lang.upper()}: File not found at {path}")
            continue
        
        with open(path, 'r') as f:
            html = f.read()
        
        # ── 1. Extract article-body content ──
        body_match = re.search(r'<article class="article-body">(.*?)</article>', html, re.DOTALL)
        if not body_match:
            print(f"  {lang.upper()}: No article-body found")
            continue
        
        raw_body = body_match.group(1)
        
        # Clean bilingual spans
        if has_bilingual_spans(raw_body):
            clean_body = extract_ar(raw_body) if lang == "ar" else extract_en(raw_body)
        else:
            clean_body = raw_body
        
        # ── 2. Get TOC items and add ids to headings ──
        toc_items = get_h2_headings(clean_body)
        clean_body = add_ids_to_headings(clean_body, toc_items)
        
        # ── 3. Build article-end and sidebar ──
        article_end = make_article_end(config, lang)
        sidebar = make_sidebar(config, lang, toc_items)
        
        # ── 4. Find banner and footer positions ──
        # Structure: <head>...</head><body>...<div class="article-wrap">...banner...<article...>...</article>...</div><footer>...</footer>
        
        # Find the position after banner section and before current </article>
        banner_end_match = re.search(r'</section>', html)
        if not banner_end_match:
            print(f"  {lang.upper()}: No banner section found")
            continue
        
        # Find the end of the current article-body tag
        article_close = html.find('</article>', body_match.start())
        if article_close < 0:
            print(f"  {lang.upper()}: No </article> close tag found")
            continue
        
        # Find the end of the wrapping div (after </article>)
        # Look for the next </div> after </article>
        div_after = html.find('</div>', article_close)
        if div_after < 0:
            div_after = html.find('<footer', article_close)
            if div_after < 0:
                div_after = article_close + len('</article>')
        
        # Determine the content between </section> and the old structure
        banner_end = banner_end_match.end()
        
        # The old structure had: <article>...body...</article></div>
        # New structure: <div class="article-layout" style="..."><main><article>...body...</article><article-end></main><sidebar></div>
        
        new_section = f"""
<div class="article-layout" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:2.5rem">

<main class="article-main">
<article class="article-body">
{clean_body}
</article>
{article_end}
</main>

{sidebar}

</div><!-- /article-layout -->"""
        
        # Find where the old <article class="article-body"> starts
        old_body_open = body_match.start()

        # Find the </div> after </article> - this closes article-wrap, we KEEP it
        wrap_close = html.find('</div>', article_close)

        # Replace from body open to just before the closing </div> of article-wrap
        # This keeps the original closing </div> for article-wrap balance
        new_html = html[:old_body_open] + new_section + html[wrap_close:]
        
        # ── 5. Update meta description / title if needed ──
        # (optional - titles usually match)
        
        # ── 6. Write back ──
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        # Verify
        vbody = re.search(r'<article class="article-body">(.*?)</article>', new_html, re.DOTALL)
        if vbody:
            vtext = re.sub(r'<[^>]+>', ' ', vbody.group(1))
            vtext = re.sub(r'\s+', ' ', vtext)
            ven_words = len(re.findall(r'\b[a-zA-Z]{3,}\b', vtext))
            var_chars = len(re.findall(r'[؀-ۿ]', vtext))
            
            has_grid = 'display:grid' in new_html
            has_toc = 'toc-item' in new_html
            has_related = 'sidebar-related-item' in new_html
            has_cta = 'article-tool-cta' in new_html
            
            status = "✅" if (var_chars > 500 or (lang == "en" and ven_words > 500)) and has_grid and has_toc and has_related else "⚠️"
            print(f"  {lang.upper()}: AR={var_chars}, EN={ven_words} | Grid={has_grid} TOC={has_toc} Related={has_related} CTA={has_cta} {status}")
        
        print(f"  {lang.upper()}: Saved to {path}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target = sys.argv[1]
        for config in ARTICLES:
            if config["name"] == target:
                process_article(config)
                break
        else:
            print(f"Article '{target}' not found")
    else:
        for config in ARTICLES:
            process_article(config)

