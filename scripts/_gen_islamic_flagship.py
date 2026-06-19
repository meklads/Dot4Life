#!/usr/bin/env python3
"""Generate flagship Islamic tool HTML pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

ISLAMIC_TABS = [
    ("prayer-times.html", "Prayer Times", "أوقات الصلاة", "Prayer", "الصلاة"),
    ("qibla.html", "Qibla", "القبلة", "Qibla", "القبلة"),
    ("zakat-calculator.html", "Zakat", "الزكاة", "Zakat", "الزكاة"),
    ("hijri-converter.html", "Hijri", "الهجري", "Hijri", "الهجري"),
    ("inheritance-calculator.html", "Inheritance", "الميراث", "Inherit", "الميراث"),
]

def head(title, desc, slug, page_css, schema_extra=""):
    return f'''<!DOCTYPE html>
<html lang="en" data-theme="light" data-lang="en" dir="ltr">
<head>
<meta charset="UTF-8"/>
<script>(function(){{var p=new URLSearchParams(location.search),gd=(function(){{try{{var z=(Intl.DateTimeFormat().resolvedOptions().timeZone||"");return /Riyadh|Dubai|Qatar|Bahrain|Kuwait|Muscat|Baghdad|Amman|Beirut|Damascus|Aden|Cairo|Khartoum/i.test(z)?"ar":"en";}}catch(e){{return "ar";}}}})(),l=p.get("lang")||localStorage.getItem("dfl-lang")||gd,t=p.get("theme")||localStorage.getItem("dfl-theme")||"light",h=document.documentElement;h.setAttribute("data-theme",t);h.setAttribute("data-lang",l);h.setAttribute("lang",l);h.setAttribute("dir",l==="ar"?"rtl":"ltr");if(p.get("lang"))localStorage.setItem("dfl-lang",l);if(p.get("theme"))localStorage.setItem("dfl-theme",t);}})()</script>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta http-equiv="x-dns-prefetch-control" content="on" />
<link rel="dns-prefetch" href="https://fonts.googleapis.com" />
<link rel="dns-prefetch" href="https://fonts.gstatic.com" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<title>{title}</title>
<meta name="description" content="{desc}"/>
<link rel="canonical" href="https://dotforlife.com/tools/{slug}"/>
<link rel="alternate" hreflang="ar" href="https://dotforlife.com/tools/{slug}?lang=ar" />
<link rel="alternate" hreflang="en" href="https://dotforlife.com/tools/{slug}?lang=en" />
<link rel="alternate" hreflang="x-default" href="https://dotforlife.com/tools/{slug}" />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Almarai:wght@400;700;800&display=swap" onload="this.onload=null;this.rel='stylesheet'"/>
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Almarai:wght@400;700;800&display=swap"/></noscript>
<link rel="stylesheet" href="/styles/global.css?v=20260618f"/>
<link rel="stylesheet" href="/styles/tools-shared.css?v=20260608a">
<link rel="stylesheet" href="/styles/tools-flagship.css?v=20260625b">
<link rel="stylesheet" href="/styles/tools-accents.css?v=20260625a">
<link rel="stylesheet" href="{page_css}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://dotforlife.com/tools/{slug}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://dotforlife.com/og/og-default.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://dotforlife.com/og/og-default.png">
{schema_extra}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G1XPV4F0G"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', 'G-3G1XPV4F0G');
window.dflTrack=function(event,params){{
  gtag('event',event,Object.assign({{
    page_path:location.pathname,
    language:document.documentElement.getAttribute('data-lang')||'en'
  }},params||{{}}));
}};
</script>
</head>'''

NAV = '''<nav id="navbar" class="index-nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/index.html" class="nav-logo" aria-label="DOTFORLIFE Home">
      <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="115" height="115" loading="eager" fetchpriority="high">
    </a>
    <ul class="nav-links">
      <li><a href="/health.html"><span class="en">Health</span><span class="ar">الصحة</span></a></li>
      <li><a href="/finance.html"><span class="en">Finance</span><span class="ar">المالية</span></a></li>
      <li><a href="/real-estate.html"><span class="en">Real Estate</span><span class="ar">العقار</span></a></li>
      <li><a href="/travel.html"><span class="en">Travel</span><span class="ar">السفر</span></a></li>
      <li><a href="/islamic.html"><span class="en">Islamic</span><span class="ar">الإسلامية</span></a></li>
      <li><a href="/about.html"><span class="en">About</span><span class="ar">عنّا</span></a></li>
      <li><a href="/archive.html"><span class="en">Archive</span><span class="ar">الأرشيف</span></a></li>
      <li><a href="/blog.html"><span class="en">blog</span><span class="ar">المدونة</span></a></li>
      <li><a href="/library.html" aria-current="page"><span class="en">Library</span><span class="ar">المكتبة</span></a></li>
    </ul>
    <div class="nav-controls">
      <button class="nav-btn" id="lang-toggle" aria-label="Switch language"><span class="en">عربي</span><span class="ar">English</span></button>
      <button class="nav-btn" id="theme-toggle" aria-label="Toggle theme"><svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg></button>
      <button class="hamburger" id="hamburger-btn" aria-label="Menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>'''

FOOTER = '''<footer class="site-footer" role="contentinfo">
  <div class="footer-accent" aria-hidden="true"></div>
  <div class="footer-inner">
    <div class="footer-main">
      <div class="footer-brand">
        <a href="/index.html" class="footer-logo" aria-label="DOTFORLIFE">
          <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="auto" loading="lazy">
        </a>
        <p class="footer-tagline"><span class="en">One calm place for your family's everyday decisions. Free, always.</span><span class="ar">مكان هادئ واحد لقرارات عائلتك اليومية. مجاني دائماً.</span></p>
        <p class="footer-motto"><span class="en">Life, at ease.</span><span class="ar">الحياة، براحة.</span></p>
      </div>
      <div class="footer-links-grid">
        <div class="footer-col">
          <h4><span class="en">Life</span><span class="ar">الحياة</span></h4>
          <ul>
            <li><a href="/health.html"><span class="en">Health</span><span class="ar">الصحة</span></a></li>
            <li><a href="/finance.html"><span class="en">Finance</span><span class="ar">المالية</span></a></li>
            <li><a href="/real-estate.html"><span class="en">Real Estate</span><span class="ar">العقار</span></a></li>
            <li><a href="/travel.html"><span class="en">Travel</span><span class="ar">السفر</span></a></li>
            <li><a href="/islamic.html"><span class="en">Islamic</span><span class="ar">الإسلامية</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Tools</span><span class="ar">الأدوات</span></h4>
          <ul>
            <li><a href="/tools/prayer-times.html"><span class="en">Prayer Times</span><span class="ar">أوقات الصلاة</span></a></li>
            <li><a href="/tools/qibla.html"><span class="en">Qibla</span><span class="ar">القبلة</span></a></li>
            <li><a href="/tools/zakat-calculator.html"><span class="en">Zakat</span><span class="ar">الزكاة</span></a></li>
            <li><a href="/tools/hijri-converter.html"><span class="en">Hijri Date</span><span class="ar">التاريخ الهجري</span></a></li>
            <li><a href="/library.html"><span class="en">All Tools</span><span class="ar">كل الأدوات</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Discover</span><span class="ar">اكتشف</span></h4>
          <ul>
            <li><a href="/blog.html"><span class="en">Blog</span><span class="ar">المدونة</span></a></li>
            <li><a href="/archive.html"><span class="en">Archive</span><span class="ar">الأرشيف</span></a></li>
            <li><a href="/our-vision.html"><span class="en">Our Vision</span><span class="ar">رؤيتنا</span></a></li>
            <li><a href="/pregnancy-journey.html"><span class="en">Pregnancy Journey</span><span class="ar">رحلة الحمل</span></a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4><span class="en">Company</span><span class="ar">الشركة</span></h4>
          <ul>
            <li><a href="/about.html"><span class="en">About</span><span class="ar">عنّا</span></a></li>
            <li><a href="/contact.html"><span class="en">Contact</span><span class="ar">تواصل</span></a></li>
            <li><a href="/editorial-standards.html"><span class="en">Editorial Standards</span><span class="ar">المعايير التحريرية</span></a></li>
            <li><a href="/privacy-policy.html"><span class="en">Privacy</span><span class="ar">الخصوصية</span></a></li>
            <li><a href="/terms.html"><span class="en">Terms</span><span class="ar">الشروط</span></a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span class="footer-copy">© 2026 DOTFORLIFE · <span class="en">Free for families, always.</span><span class="ar">مجاني للعائلات، دائماً.</span></span>
      <div class="footer-bottom-links">
        <a href="/privacy-policy.html"><span class="en">Privacy</span><span class="ar">الخصوصية</span></a>
        <a href="/terms.html"><span class="en">Terms</span><span class="ar">الشروط</span></a>
        <a href="/contact.html"><span class="en">Contact</span><span class="ar">تواصل</span></a>
      </div>
    </div>
  </div>
</footer>'''

MOBILE = '''<nav class="dfl-mobile-nav" aria-label="Mobile navigation">
  <a href="/index.html" class="dfl-mnav-item" aria-label="Home">
    <svg viewBox="0 0 24 24"><polyline points="3 9 12 2 21 9"/><path d="M5 9v11a1 1 0 001 1h4v-6h4v6h4a1 1 0 001-1V9"/></svg>
    <span class="en">Home</span><span class="ar">الرئيسية</span>
  </a>
  <a href="/library.html" class="dfl-mnav-item active" aria-label="Library">
    <svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg>
    <span class="en">Library</span><span class="ar">المكتبة</span>
  </a>
  <a href="/finance.html" class="dfl-mnav-item" aria-label="Finance">
    <svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
    <span class="en">Finance</span><span class="ar">المالية</span>
  </a>
  <a href="/islamic.html" class="dfl-mnav-item" aria-label="Islamic">
    <svg viewBox="0 0 24 24"><path d="M21 10.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l2.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>
    <span class="en">Islamic</span><span class="ar">الإسلامية</span>
  </a>
  <a href="/travel.html" class="dfl-mnav-item" aria-label="Travel">
    <svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
    <span class="en">Travel</span><span class="ar">السفر</span>
  </a>
</nav>

<div class="mobile-dropdown" id="mobile-dropdown" aria-hidden="true">
  <div class="md-links">
    <a href="/health.html"><span class="en">Health</span><span class="ar">الصحة</span></a>
    <a href="/finance.html"><span class="en">Finance</span><span class="ar">المالية</span></a>
    <a href="/real-estate.html"><span class="en">Real Estate</span><span class="ar">العقار</span></a>
    <a href="/travel.html"><span class="en">Travel</span><span class="ar">السفر</span></a>
    <a href="/islamic.html"><span class="en">Islamic</span><span class="ar">الإسلامية</span></a>
    <a href="/about.html"><span class="en">About</span><span class="ar">عنّا</span></a>
    <a href="/archive.html"><span class="en">Archive</span><span class="ar">الأرشيف</span></a>
    <a href="/blog.html"><span class="en">Blog</span><span class="ar">المدونة</span></a>
    <a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a>
  </div>
  <div class="md-controls">
    <button class="nav-btn" id="lang-toggle-mobile"><span class="en">عربي</span><span class="ar">English</span></button>
    <button class="nav-btn" id="theme-toggle-mobile">
      <svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      <svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
    </button>
  </div>
</div>'''

def tabs(active_file):
    lines = ['<div class="tool-tabs-wrap" role="navigation" aria-label="Islamic tools">', '  <div class="tool-tabs-inner">']
    for href, en, ar, short_en, short_ar in ISLAMIC_TABS:
        cls = ' class="is-active"' if href == active_file else ''
        lines.append(f'    <a href="/tools/{href}"{cls}><span class="en">{short_en}</span><span class="ar">{short_ar}</span></a>')
    lines += ['  </div>', '</div>']
    return '\n'.join(lines)

def hero(breadcrumb_en, breadcrumb_ar, eyebrow_en, eyebrow_ar, h1_en, h1_ar, desc_en, desc_ar, trust):
    trust_li = ''.join(f'<li><span class="en">{t[0]}</span><span class="ar">{t[1]}</span></li>' for t in trust)
    return f'''<div class="tool-hero">
  <div class="tool-hero-inner">
    <nav class="tool-breadcrumb" aria-label="Breadcrumb">
      <a href="/index.html"><span class="en">Home</span><span class="ar">الرئيسية</span></a>
      <span class="tool-breadcrumb-sep" aria-hidden="true">/</span>
      <a href="/islamic.html"><span class="en">Islamic</span><span class="ar">الإسلامية</span></a>
      <span class="tool-breadcrumb-sep" aria-hidden="true">/</span>
      <span><span class="en">{breadcrumb_en}</span><span class="ar">{breadcrumb_ar}</span></span>
    </nav>
    <p class="tool-eyebrow">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l2.4 7.2h7.6l-6 4.8 2.4 7.2-6-4.8-6 4.8 2.4-7.2-6-4.8h7.6z"/></svg>
      <span class="en">{eyebrow_en}</span><span class="ar">{eyebrow_ar}</span>
    </p>
    <h1 id="tool-title"><span class="en">{h1_en}</span><span class="ar">{h1_ar}</span></h1>
    <p class="tool-hero-desc"><span class="en">{desc_en}</span><span class="ar">{desc_ar}</span></p>
    <ul class="tool-trust">{trust_li}</ul>
  </div>
</div>'''

def page(data_tool, active_tab, body_content, script, title_meta):
    slug = active_tab
    h = head(title_meta['title'], title_meta['desc'], slug, title_meta['css'], title_meta.get('schema',''))
    return '\n'.join([
        h,
        f'<body class="tool-flagship-page no-subnav" data-tool="{data_tool}">',
        NAV,
        hero(**title_meta['hero']),
        tabs(active_tab),
        '<main class="tool-mn">',
        body_content,
        '</main>',
        FOOTER,
        MOBILE,
        '<script src="/scripts/global.js?v=20260618a" defer></script>',
        script,
        '</body>',
        '</html>',
    ])

print("Generator loaded — run build functions from main")
