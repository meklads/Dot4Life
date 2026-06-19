#!/usr/bin/env python3
"""Generate 4 health/fitness/islamic flagship tool HTML pages."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

# Extract BD array from existing pregnancy file
preg_src = (TOOLS / "pregnancy-calculator.html").read_text(encoding="utf-8")
bd_match = re.search(r"(const BD=\[[\s\S]*?\];)", preg_src)
if not bd_match:
    raise SystemExit("BD array not found")
BD_BLOCK = bd_match.group(1)

CALC_BLOCK = preg_src[preg_src.index("function switchTab"):preg_src.index("/* ── ACCORDION & FAQ")]
# Fix for flagship: remove sticky-cta and applyLang lines
CALC_BLOCK = CALC_BLOCK.replace("    document.getElementById('sticky-cta').classList.remove('show');\n", "")
CALC_BLOCK = CALC_BLOCK.replace("    applyLang();\n", "")
CALC_BLOCK = CALC_BLOCK.replace(".c-tab", ".t-tab")
CALC_BLOCK = CALC_BLOCK.replace(".c-panel", ".t-tab-panel")

INIT_SCRIPT = """<script>(function(){var p=new URLSearchParams(location.search),gd=(function(){try{var z=(Intl.DateTimeFormat().resolvedOptions().timeZone||"");return /Riyadh|Dubai|Qatar|Bahrain|Kuwait|Muscat|Baghdad|Amman|Beirut|Damascus|Aden|Cairo|Khartoum/i.test(z)?"ar":"en";}catch(e){return "ar";}})(),l=p.get("lang")||localStorage.getItem("dfl-lang")||gd,t=p.get("theme")||localStorage.getItem("dfl-theme")||"light",h=document.documentElement;h.setAttribute("data-theme",t);h.setAttribute("data-lang",l);h.setAttribute("lang",l);h.setAttribute("dir",l==="ar"?"rtl":"ltr");if(p.get("lang"))localStorage.setItem("dfl-lang",l);if(p.get("theme"))localStorage.setItem("dfl-theme",t);})()</script>"""

CSS_LINKS = """<link rel="stylesheet" href="/styles/global.css?v=20260618f"/>
<link rel="stylesheet" href="/styles/tools-shared.css?v=20260608a">
<link rel="stylesheet" href="/styles/tools-flagship.css?v=20260625b">
<link rel="stylesheet" href="/styles/tools-accents.css?v=20260625a">"""

NAV = """<nav id="navbar" class="index-nav" role="navigation" aria-label="Main navigation">
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
      <button class="hamburger" id="hamburger-btn" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
    </div>
  </div>
</nav>"""

FOOTER = """<footer class="site-footer" role="contentinfo">
  <div class="footer-accent" aria-hidden="true"></div>
  <div class="footer-inner">
    <div class="footer-main">
      <div class="footer-brand">
        <a href="/index.html" class="footer-logo" aria-label="DOTFORLIFE"><img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="auto" loading="lazy"></a>
        <p class="footer-tagline"><span class="en">One calm place for your family's everyday decisions. Free, always.</span><span class="ar">مكان هادئ واحد لقرارات عائلتك اليومية. مجاني دائماً.</span></p>
        <p class="footer-motto"><span class="en">Life, at ease.</span><span class="ar">الحياة، براحة.</span></p>
      </div>
      <div class="footer-links-grid">
        <div class="footer-col"><h4><span class="en">Life</span><span class="ar">الحياة</span></h4><ul>
          <li><a href="/health.html"><span class="en">Health</span><span class="ar">الصحة</span></a></li>
          <li><a href="/finance.html"><span class="en">Finance</span><span class="ar">المالية</span></a></li>
          <li><a href="/real-estate.html"><span class="en">Real Estate</span><span class="ar">العقار</span></a></li>
          <li><a href="/travel.html"><span class="en">Travel</span><span class="ar">السفر</span></a></li>
          <li><a href="/islamic.html"><span class="en">Islamic</span><span class="ar">الإسلامية</span></a></li>
        </ul></div>
        <div class="footer-col"><h4><span class="en">Tools</span><span class="ar">الأدوات</span></h4><ul>
          <li><a href="/tools/bmi-calculator.html"><span class="en">BMI Calculator</span><span class="ar">حاسبة BMI</span></a></li>
          <li><a href="/tools/calorie-calculator.html"><span class="en">Calorie Calculator</span><span class="ar">حاسبة السعرات</span></a></li>
          <li><a href="/tools/water-calculator.html"><span class="en">Hydration</span><span class="ar">الترطيب</span></a></li>
          <li><a href="/tools/pregnancy-calculator.html"><span class="en">Pregnancy</span><span class="ar">الحمل</span></a></li>
          <li><a href="/library.html"><span class="en">All Tools</span><span class="ar">كل الأدوات</span></a></li>
        </ul></div>
        <div class="footer-col"><h4><span class="en">Discover</span><span class="ar">اكتشف</span></h4><ul>
          <li><a href="/blog.html"><span class="en">Blog</span><span class="ar">المدونة</span></a></li>
          <li><a href="/archive.html"><span class="en">Archive</span><span class="ar">الأرشيف</span></a></li>
          <li><a href="/our-vision.html"><span class="en">Our Vision</span><span class="ar">رؤيتنا</span></a></li>
          <li><a href="/pregnancy-journey.html"><span class="en">Pregnancy Journey</span><span class="ar">رحلة الحمل</span></a></li>
        </ul></div>
        <div class="footer-col"><h4><span class="en">Company</span><span class="ar">الشركة</span></h4><ul>
          <li><a href="/about.html"><span class="en">About</span><span class="ar">عنّا</span></a></li>
          <li><a href="/contact.html"><span class="en">Contact</span><span class="ar">تواصل</span></a></li>
          <li><a href="/editorial-standards.html"><span class="en">Editorial Standards</span><span class="ar">المعايير التحريرية</span></a></li>
          <li><a href="/privacy-policy.html"><span class="en">Privacy</span><span class="ar">الخصوصية</span></a></li>
          <li><a href="/terms.html"><span class="en">Terms</span><span class="ar">الشروط</span></a></li>
        </ul></div>
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
</footer>

<nav class="dfl-mobile-nav" aria-label="Mobile navigation">
  <a href="/index.html" class="dfl-mnav-item"><svg viewBox="0 0 24 24"><polyline points="3 9 12 2 21 9"/><path d="M5 9v11a1 1 0 001 1h4v-6h4v6h4a1 1 0 001-1V9"/></svg><span class="en">Home</span><span class="ar">الرئيسية</span></a>
  <a href="/library.html" class="dfl-mnav-item active"><svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/></svg><span class="en">Library</span><span class="ar">المكتبة</span></a>
  <a href="/finance.html" class="dfl-mnav-item"><svg viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg><span class="en">Finance</span><span class="ar">المالية</span></a>
  <a href="/islamic.html" class="dfl-mnav-item"><svg viewBox="0 0 24 24"><path d="M21 10.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l2.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg><span class="en">Islamic</span><span class="ar">الإسلامية</span></a>
  <a href="/travel.html" class="dfl-mnav-item"><svg viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg><span class="en">Travel</span><span class="ar">السفر</span></a>
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
    <button class="nav-btn" id="theme-toggle-mobile"><svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:none"><circle cx="12" cy="12" r="5"/></svg></button>
  </div>
</div>"""

def head(title, desc, slug, page_css, schema=""):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light" data-lang="en" dir="ltr">
<head>
<meta charset="UTF-8"/>
{INIT_SCRIPT}
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
{CSS_LINKS}
<link rel="stylesheet" href="{page_css}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://dotforlife.com/tools/{slug}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://dotforlife.com/og/og-default.png">
<meta name="twitter:card" content="summary_large_image">
{schema}
</head>"""

def tabs_html(items, aria):
    inner = "\n".join(
        f'    <a href="{href}"{" class=\"is-active\"" if active else ""}><span class="en">{en}</span><span class="ar">{ar}</span></a>'
        for href, en, ar, active in items
    )
    return f"""<div class="tool-tabs-wrap" role="navigation" aria-label="{aria}">
  <div class="tool-tabs-inner">
{inner}
  </div>
</div>"""

def faq_block(items):
    qs = ""
    for en, ar, aen, aar in items:
        qs += f"""      <div class="t-faq-item">
        <div class="t-faq-q" onclick="toggleFAQ(this)"><span><span class="en">{en}</span><span class="ar">{ar}</span></span><span class="t-faq-arrow">▼</span></div>
        <div class="t-faq-a"><p><span class="en">{aen}</span><span class="ar">{aar}</span></p></div>
      </div>\n"""
    return qs

def toggle_faq_js():
    return """function toggleFAQ(el){
  var answer=el.nextElementSibling;var isOpen=el.classList.contains('open');
  document.querySelectorAll('.t-faq-q').forEach(function(q){q.classList.remove('open');q.nextElementSibling.classList.remove('active');});
  if(!isOpen){el.classList.add('open');answer.classList.add('active');}
}
function getLang(){return document.documentElement.getAttribute('data-lang')||'en';}"""

print("Part 1 loaded - continuing in part 2")

HEALTH_TABS = [
    ("/tools/bmi-calculator.html", "BMI", "BMI", False),
    ("/tools/calorie-calculator.html", "Calories", "السعرات", False),
    ("/tools/body-fat-calculator.html", "Body Fat", "الدهون", False),
    ("/tools/water-calculator.html", "Water", "الماء", False),
    ("/tools/pregnancy-calculator.html", "Pregnancy", "الحمل", False),
    ("/tools/age-calculator.html", "Age", "العمر", False),
]

FITNESS_TABS = [
    ("/tools/bmi-calculator.html", "BMI", "BMI", False),
    ("/tools/body-fat-calculator.html", "Body Fat", "الدهون", False),
    ("/tools/calorie-calculator.html", "Calories", "السعرات", False),
    ("/tools/one-rep-max.html", "1RM", "الحد الأقصى", False),
    ("/tools/water-calculator.html", "Water", "الماء", False),
]

ISLAMIC_TABS = [
    ("/tools/prayer-times.html", "Prayer", "الصلاة", False),
    ("/tools/qibla.html", "Qibla", "القبلة", False),
    ("/tools/hijri-converter.html", "Hijri", "الهجري", False),
    ("/tools/zakat-calculator.html", "Zakat", "الزكاة", False),
    ("/tools/ramadan-calorie-calculator.html", "Ramadan", "رمضان", False),
    ("/tools/inheritance-calculator.html", "Inherit", "الميراث", False),
]

def gen_age():
    tabs = list(HEALTH_TABS)
    tabs[-1] = (tabs[-1][0], tabs[-1][1], tabs[-1][2], True)
    schema = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebApplication","name":"Age Calculator","url":"https://dotforlife.com/tools/age-calculator.html","applicationCategory":"HealthApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"SAR"},"inLanguage":["en","ar"]}</script>"""
    hero = """<div class="tool-hero"><div class="tool-hero-inner">
    <nav class="tool-breadcrumb" aria-label="Breadcrumb">
      <a href="/index.html"><span class="en">Home</span><span class="ar">الرئيسية</span></a>
      <span class="tool-breadcrumb-sep">/</span>
      <a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a>
      <span class="tool-breadcrumb-sep">/</span>
      <span><span class="en">Age Calculator</span><span class="ar">حاسبة العمر</span></span>
    </nav>
    <p class="tool-eyebrow"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M8 10h8"/></svg> <span class="en">Health Tool · Hijri + Gregorian</span><span class="ar">أداة صحية · هجري + ميلادي</span></p>
    <h1 id="tool-title"><span class="en">Detailed Age Calculator</span><span class="ar">حاسبة العمر التفصيلية</span></h1>
    <p class="tool-hero-desc"><span class="en">Exact age in years, months, and days — Gregorian and Hijri — with birthday countdown and life stats.</span><span class="ar">عمرك بالسنوات والأشهر والأيام — ميلادي وهجري — مع عد تنازلي لعيد الميلاد وإحصائيات.</span></p>
    <ul class="tool-trust"><li><span class="en">ISO 8601 dates</span><span class="ar">تواريخ ISO 8601</span></li><li><span class="en">Runs locally</span><span class="ar">يعمل محلياً</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li></ul>
  </div></div>"""
    workspace = """<main class="tool-mn"><div class="tool-workspace">
    <div class="tool-panel ac-card"><div class="tool-panel-hdr"><h2><span class="en">Your Dates</span><span class="ar">تواريخك</span></h2></div>
      <div class="tool-panel-body t-body">
        <div class="t-g2">
          <div class="t-fl"><label class="t-fl-l" for="dob"><span class="en">Date of birth</span><span class="ar">تاريخ الميلاد</span></label><div class="t-fl-r"><input type="date" id="dob" max="2026-12-31"></div></div>
          <div class="t-fl"><label class="t-fl-l" for="targetDate"><span class="en">Calculate age as of</span><span class="ar">احسب العمر حتى</span></label><div class="t-fl-r"><input type="date" id="targetDate"></div></div>
        </div>
        <button class="t-btn" type="button" onclick="calcAge()"><span class="en">Calculate My Age</span><span class="ar">احسب عمري</span></button>
      </div>
    </div>
    <div class="tool-panel ac-card" id="resultsCard"><div class="tool-panel-hdr"><h2><span class="en">Your Age</span><span class="ar">عمرك</span></h2></div>
      <div class="tool-panel-body t-body">
        <div class="t-hero-result"><div class="t-hero-val" id="ageYears">—</div><div class="t-hero-lbl"><span class="en">years old</span><span class="ar">سنة</span></div></div>
        <div class="t-stats" id="statsGrid"></div>
        <div class="ac-hijri-block"><div class="ac-hijri-title"><span class="en">Your Hijri Age</span><span class="ar">عمرك بالتقويم الهجري</span></div><div class="t-stats" id="hijriGrid"></div></div>
        <div class="ac-bday" id="bdayCountdown"></div>
        <div class="ac-facts" id="factsGrid" style="display:none"></div>
      </div>
    </div>
  </div>
  <div class="tool-below">
    <div class="t-section"><div class="t-section-label"><span class="en">How this is calculated</span><span class="ar">طريقة الحساب</span></div>
      <p class="en">Age in exact years, months, and days using ISO 8601 date arithmetic with leap-year correction. Hijri dates use the Kuwaiti tabular algorithm.</p>
      <p class="ar">العمر بالسنوات والأشهر والأيام الدقيقة باستخدام ISO 8601 مع تصحيح السنة الكبيسة. التواريخ الهجرية بخوارزمية الكويت الجدولية.</p>
    </div>
    <div class="t-faq"><div class="t-faq-label"><span class="en">FAQ</span><span class="ar">أسئلة شائعة</span></div><div class="t-faq-title"><span class="en">Frequently Asked Questions</span><span class="ar">الأسئلة المتكررة</span></div>
""" + faq_block([
        ("How is exact age calculated?", "كيف يتم حساب العمر بالضبط؟", "Exact age subtracts birth date from target date, accounting for leap years and varying month lengths.", "يتم حساب العمر الدقيق بطرح تاريخ الميلاد من التاريخ المستهدف مع مراعاة السنوات الكبيسة."),
        ("Does this account for leap years?", "هل تراعي السنوات الكبيسة؟", "Yes — full Gregorian calendar rules including February 29.", "نعم — قواعد التقويم الميلادي الكامل بما فيها 29 فبراير."),
        ("How is Hijri age calculated?", "كيف يُحتسب العمر الهجري؟", "Both dates convert to Hijri via the Kuwaiti tabular method, then the difference is computed.", "يُحوَّل التاريخان للهجري ثم يُحسب الفرق."),
    ]) + """    </div>
  </div>
  <section class="tool-tickets-rail"><header class="tool-tickets-head"><p class="tool-tickets-eyebrow"><span class="en">Continue Your Journey</span><span class="ar">أكمل رحلتك</span></p><h2 class="tool-tickets-title"><span class="en">Related Tools</span><span class="ar">أدوات ذات صلة</span></h2></header>
    <div class="tool-tickets-track">
      <a href="/tools/hijri-converter.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Hijri Converter</span><span class="ar">محوّل الهجري</span></h3><span class="tool-ticket-cta"><span class="en">Open →</span><span class="ar">← افتح</span></span></div></a>
      <a href="/tools/pregnancy-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Pregnancy Calculator</span><span class="ar">حاسبة الحمل</span></h3><span class="tool-ticket-cta"><span class="en">Open →</span><span class="ar">← افتح</span></span></div></a>
      <a href="/tools/bmi-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">BMI Calculator</span><span class="ar">حاسبة BMI</span></h3><span class="tool-ticket-cta"><span class="en">Open →</span><span class="ar">← افتح</span></span></div></a>
      <a href="/tools/calorie-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Calorie Calculator</span><span class="ar">حاسبة السعرات</span></h3><span class="tool-ticket-cta"><span class="en">Open →</span><span class="ar">← افتح</span></span></div></a>
    </div>
  </section></main>"""
    script = """
<script src="/scripts/global.js?v=20260618a" defer></script>
<script>
var _ageCache=null;
var HM=['محرّم','صفر','ربيع الأول','ربيع الثاني','جمادى الأولى','جمادى الثانية','رجب','شعبان','رمضان','شوال','ذو القعدة','ذو الحجة'];
var HM_EN=['Muharram','Safar','Rabi al-Awwal','Rabi al-Thani','Jumada I','Jumada II','Rajab','Sha\\'ban','Ramadan','Shawwal','Dhu al-Qi\\'dah','Dhu al-Hijjah'];
function gregorianToJulian(y,m,d){if(m<=2){y--;m+=12;}var A=Math.floor(y/100),B=2-A+Math.floor(A/4);return Math.floor(365.25*(y+4716))+Math.floor(30.6001*(m+1))+d+B-1524.5;}
function gregorianToHijri(gy,gm,gd){var jd=Math.floor(gregorianToJulian(gy,gm,gd)+.5);var l=jd-1948440+10632;var n=Math.floor((l-1)/10631);var l2=l-10631*n+354;var j=(Math.floor((10985-l2)/5316))*(Math.floor((50*l2)/17719))+(Math.floor(l2/5670))*(Math.floor((43*l2)/15238));var l3=l2-(Math.floor((30-j)/15))*(Math.floor((17719*j)/50))-(Math.floor(j/16))*(Math.floor((15238*j)/43))+29;var month=Math.floor((24*l3)/709);var day=l3-Math.floor((709*month)/24);var year=30*n+j-30;return{year,month,day};}
function renderAgeDynamic(){if(!_ageCache)return;var lang=getLang(),s=_ageCache.stats;document.getElementById('statsGrid').innerHTML=s.map(function(x){return '<div class="t-stat"><div class="t-stat-val">'+x.val+'</div><div class="t-stat-lbl">'+(lang==='ar'?x.ar:x.en)+'</div></div>';}).join('');var fg=document.getElementById('factsGrid');fg.style.display='grid';fg.innerHTML=_ageCache.facts.map(function(f){return '<div class="ac-fact"><div class="ac-fact-val">'+f.val+'</div><div class="ac-fact-lbl">'+(lang==='ar'?f.ar:f.en)+'</div></div>';}).join('');document.getElementById('bdayCountdown').innerHTML='<div class="ac-bday-num">'+_ageCache.daysToB+'</div><div class="ac-bday-lbl">'+(lang==='ar'?'يوماً حتى عيد ميلادك الق próximo':'days until your next birthday')+'</div>';}
function calcAge(){var dob=new Date(document.getElementById('dob').value);var target=new Date(document.getElementById('targetDate').value);if(!dob||!target||dob>target){alert(getLang()==='ar'?'يرجى إدخال تاريخ ميلاد صحيح':'Please enter a valid birth date.');return;}var lang=getLang();var years=target.getFullYear()-dob.getFullYear();var months=target.getMonth()-dob.getMonth();var days=target.getDate()-dob.getDate();if(days<0){months--;days+=new Date(target.getFullYear(),target.getMonth(),0).getDate();}if(months<0){years--;months+=12;}var totalDays=Math.floor((target-dob)/86400000);var totalHours=totalDays*24;var totalWeeks=Math.floor(totalDays/7);var totalMonths=years*12+months;var heartbeats=Math.round(totalDays*100800);var breaths=Math.round(totalDays*20*60*24);(function(){var el=document.getElementById('ageYears'),t=years,d=700,s=performance.now();function step(n){var p=Math.min((n-s)/d,1),e=1-Math.pow(1-p,3);el.textContent=Math.round(t*e);if(p<1)requestAnimationFrame(step);else el.textContent=t;}requestAnimationFrame(step);})();var stats=[{ar:'الأشهر الكاملة',en:'Total months',val:totalMonths.toLocaleString()},{ar:'الأسابيع',en:'Total weeks',val:totalWeeks.toLocaleString()},{ar:'الأيام',en:'Total days',val:totalDays.toLocaleString()},{ar:'الساعات',en:'Total hours',val:totalHours.toLocaleString()},{ar:'نبضات القلب',en:'Heartbeats',val:heartbeats.toLocaleString()},{ar:'نفَس',en:'Breaths',val:breaths.toLocaleString()}];var hDob=gregorianToHijri(dob.getFullYear(),dob.getMonth()+1,dob.getDate());var hTarget=gregorianToHijri(target.getFullYear(),target.getMonth()+1,target.getDate());var hYears=hTarget.year-hDob.year;var hMonths=hTarget.month-hDob.month;if(hTarget.day<hDob.day)hMonths--;if(hMonths<0){hYears--;hMonths+=12;}document.getElementById('hijriGrid').innerHTML='<div class="t-stat"><div class="t-stat-val">'+hYears+'</div><div class="t-stat-lbl"><span class="en">Hijri years</span><span class="ar">سنة هجرية</span></div></div><div class="t-stat"><div class="t-stat-val">'+hDob.day+' '+(lang==='ar'?HM[hDob.month-1]:HM_EN[hDob.month-1])+' '+hDob.year+'</div><div class="t-stat-lbl"><span class="en">Hijri birth date</span><span class="ar">تاريخ ميلادك هجرياً</span></div></div>';var nextBday=new Date(target.getFullYear(),dob.getMonth(),dob.getDate());if(nextBday<=target)nextBday.setFullYear(target.getFullYear()+1);var daysToB=Math.ceil((nextBday-target)/86400000);var facts=[{ar:'نبضات القلب',en:'Heartbeats',val:heartbeats.toLocaleString()},{ar:'ساعات النوم',en:'Hours slept',val:Math.round(totalDays*8).toLocaleString()},{ar:'وجبات تقريباً',en:'Meals approx.',val:Math.round(totalDays*3).toLocaleString()},{ar:'ليالٍ نمتها',en:'Nights slept',val:totalDays.toLocaleString()}];_ageCache={stats:stats,facts:facts,daysToB:daysToB,years:years,months:months,days:days,totalDays:totalDays};renderAgeDynamic();document.getElementById('resultsCard').classList.add('show');}
""" + toggle_faq_js() + """
document.addEventListener('DOMContentLoaded',function(){var t=new Date();document.getElementById('targetDate').value=t.toISOString().slice(0,10);document.getElementById('dob').value='1990-01-01';});
document.addEventListener('dfl:langchange',renderAgeDynamic);
</script>"""
    return head("Age Calculator | حاسبة العمر — Hijri & Gregorian | Dot For Life", "Calculate exact age in years, months, days — Gregorian and Hijri — with birthday countdown.", "age-calculator.html", "/styles/pages/tools_age-calculator.css?v=20260625a", schema) + f'\n<body class="tool-flagship-page no-subnav" data-tool="age-calculator">\n{NAV}\n{hero}\n{tabs_html(tabs, "Health tools")}\n{workspace}\n{FOOTER}\n{script}\n</body>\n</html>'

print("age fn ok")

def gen_orm():
    tabs = list(FITNESS_TABS)
    for i,t in enumerate(tabs):
        if t[0].endswith('one-rep-max.html'): tabs[i]=(t[0],t[1],t[2],True)
    hero = """<div class="tool-hero"><div class="tool-hero-inner">
    <nav class="tool-breadcrumb" aria-label="Breadcrumb"><a href="/index.html"><span class="en">Home</span><span class="ar">الرئيسية</span></a><span class="tool-breadcrumb-sep">/</span><a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a><span class="tool-breadcrumb-sep">/</span><span><span class="en">One Rep Max</span><span class="ar">الحد الأقصى</span></span></nav>
    <p class="tool-eyebrow"><span class="en">Fitness Tool · 5 Formulas</span><span class="ar">أداة لياقة · 5 معادلات</span></p>
    <h1 id="tool-title"><span class="en">One Rep Max Calculator</span><span class="ar">حاسبة الحد الأقصى للرفع</span></h1>
    <p class="tool-hero-desc"><span class="en">Estimate your 1RM from any weight and rep count. Five formulas averaged — plus a full training zone table.</span><span class="ar">قدّر حدك الأقصى من أي وزن وتكرارات. متوسط 5 معادلات — مع جدول مناطق تدريب.</span></p>
    <ul class="tool-trust"><li><span class="en">5 formulas</span><span class="ar">5 معادلات</span></li><li><span class="en">Runs locally</span><span class="ar">يعمل محلياً</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li></ul>
  </div></div>"""
    ws = """<main class="tool-mn"><div class="tool-workspace">
    <div class="tool-panel orm-card"><div class="tool-panel-hdr"><h2><span class="en">Your Lift</span><span class="ar">رفعتك</span></h2></div>
      <div class="tool-panel-body t-body">
        <div class="t-g2">
          <div class="t-fl"><label class="t-fl-l" for="liftWeight"><span class="en">Weight lifted</span><span class="ar">الوزن المرفوع</span></label><div class="t-fl-r"><input type="number" id="liftWeight" value="100" min="1"><select id="weightUnit" style="border:none;background:transparent;font-weight:700"><option value="kg">kg</option><option value="lbs">lbs</option></select></div></div>
          <div class="t-fl"><label class="t-fl-l" for="reps"><span class="en">Reps performed</span><span class="ar">عدد التكرارات</span></label><div class="t-fl-r"><input type="number" id="reps" value="8" min="1" max="30"><span class="t-fl-u"><span class="en">reps</span><span class="ar">تكرار</span></span></div></div>
        </div>
        <button class="t-btn" type="button" onclick="calcORM()"><span class="en">Calculate 1RM</span><span class="ar">احسب الحد الأقصى</span></button>
      </div>
    </div>
    <div class="tool-panel orm-card" id="resultsSection"><div class="tool-panel-hdr"><h2><span class="en">Estimated 1RM</span><span class="ar">حدك الأقصى المقدَّر</span></h2></div>
      <div class="tool-panel-body t-body">
        <div class="t-hero-result"><div class="t-hero-val" id="ormVal">—</div><div class="t-hero-lbl"><span class="en">One Rep Max</span><span class="ar">الحد الأقصى</span> <span id="ormUnit">kg</span></div>
          <div class="orm-formulas"><div class="orm-formula-pill" id="fp1"></div><div class="orm-formula-pill" id="fp2"></div><div class="orm-formula-pill" id="fp3"></div><div class="orm-formula-pill" id="fp4"></div><div class="orm-formula-pill" id="fp5"></div></div>
        </div>
        <div class="t-step"><span class="en">Training Zone Table</span><span class="ar">جدول الأوزان التدريبية</span></div>
        <div style="overflow-x:auto"><table class="t-table" id="trainingTable"><thead><tr><th><span class="en">Goal</span><span class="ar">الهدف</span></th><th>% 1RM</th><th><span class="en">Reps</span><span class="ar">تكرارات</span></th><th><span class="en">Weight</span><span class="ar">الوزن</span></th></tr></thead><tbody id="tableBody"></tbody></table></div>
      </div>
    </div>
  </div>
  <div class="tool-below"><div class="t-section"><div class="t-section-label"><span class="en">How this is calculated</span><span class="ar">طريقة الحساب</span></div>
    <p class="en"><strong>Epley:</strong> W×(1+r/30) · <strong>Brzycki:</strong> W×36/(37−r) · <strong>Lombardi:</strong> W×r^0.10 · <strong>Lander:</strong> (100×W)/(101.3−2.67123×r) · <strong>O'Conner:</strong> W×(1+r/40). Main 1RM = average of all five.</p>
    <p class="ar"><strong>إيبلي:</strong> W×(1+r/30) · <strong>برزيكي:</strong> W×36/(37−r) · <strong>لومباردي:</strong> W×r^0.10 · <strong>لاندر:</strong> (100×W)/(101.3−2.67123×r) · <strong>أوكونور:</strong> W×(1+r/40). النتيجة = متوسط الخمس.</p>
  </div><div class="t-faq"><div class="t-faq-label"><span class="en">FAQ</span><span class="ar">أسئلة شائعة</span></div><div class="t-faq-title"><span class="en">Frequently Asked Questions</span><span class="ar">الأسئلة المتكررة</span></div>
""" + faq_block([
        ("Which formula is most accurate?", "أي معادلة الأدق؟", "Averaging five formulas reduces error. Epley works well for 1–10 reps; Brzycki for lower reps.", "متوسط المعادلات يقلل الخطأ. إيبلي جيد لـ1–10 تكرارات."),
        ("Is it safe to test true 1RM?", "هل اختبار 1RM الفعلي آمن؟", "Never test maximal singles without a spotter. Use these estimates for programming.", "لا تختبر الحد الأقصى بمفردك. استخدم التقديرات للتخطيط."),
    ]) + """  </div></div>
  <section class="tool-tickets-rail"><header class="tool-tickets-head"><h2 class="tool-tickets-title"><span class="en">Related Tools</span><span class="ar">أدوات ذات صلة</span></h2></header>
    <div class="tool-tickets-track">
      <a href="/tools/body-fat-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Body Fat</span><span class="ar">الدهون</span></h3></div></a>
      <a href="/tools/calorie-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Calories</span><span class="ar">السعرات</span></h3></div></a>
      <a href="/tools/bmi-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">BMI</span><span class="ar">BMI</span></h3></div></a>
      <a href="/tools/water-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Water</span><span class="ar">الماء</span></h3></div></a>
    </div>
  </section></main>"""
    script = """
<script src="/scripts/global.js?v=20260618a" defer></script>
<script>
var ZONES=[{ar:'أقصى قوة',en:'Max Strength',pct:97,reps:'1-2',color:'#991B1B'},{ar:'قوة',en:'Strength',pct:90,reps:'3-4',color:'#DC2626'},{ar:'قوة-ضخامة',en:'Strength-Hypertrophy',pct:85,reps:'5-6',color:'#F97316'},{ar:'ضخامة عضلية',en:'Hypertrophy',pct:75,reps:'8-10',color:'#F59E0B'},{ar:'ضخامة-تحمّل',en:'Hypertrophy-Endurance',pct:67,reps:'12-15',color:'#22C55E'},{ar:'تحمّل عضلي',en:'Muscular Endurance',pct:60,reps:'15-20',color:'#3B82F6'},{ar:'استشفاء نشط',en:'Active Recovery',pct:50,reps:'20+',color:'#8B5CF6'}];
var _ormLast=null;
function v(id){return parseFloat(document.getElementById(id).value)||0;}
function renderORMTable(){if(!_ormLast)return;var lang=getLang(),orm=_ormLast.orm,unit=_ormLast.unit;document.getElementById('tableBody').innerHTML=ZONES.map(function(z){var zw=(orm*z.pct/100).toFixed(1);return '<tr><td><span class="orm-zone-dot" style="background:'+z.color+'"></span>'+(lang==='ar'?z.ar:z.en)+'</td><td>'+z.pct+'%</td><td>'+z.reps+'</td><td><strong>'+zw+' '+unit+'</strong></td></tr>';}).join('');}
function calcORM(){var w=v('liftWeight'),r=v('reps');if(!w||!r){alert(getLang()==='ar'?'أدخل الوزن وعدد التكرارات':'Please enter weight and reps.');return;}var unit=document.getElementById('weightUnit').value;var epley=w*(1+r/30);var brzycki=r===1?w:w*(36/(37-r));var lombardi=w*Math.pow(r,0.10);var lander=(100*w)/(101.3-2.67123*r);var oconner=w*(1+r/40);var orm=(epley+brzycki+lombardi+lander+oconner)/5;document.getElementById('ormUnit').textContent=unit;(function(){var el=document.getElementById('ormVal'),target=parseFloat(orm.toFixed(1)),dur=700,s=performance.now();function step(n){var p=Math.min((n-s)/dur,1),e=1-Math.pow(1-p,3);el.textContent=(target*e).toFixed(1);if(p<1)requestAnimationFrame(step);else el.textContent=orm.toFixed(1);}requestAnimationFrame(step);})();document.getElementById('fp1').textContent='Epley: '+epley.toFixed(1);document.getElementById('fp2').textContent='Brzycki: '+brzycki.toFixed(1);document.getElementById('fp3').textContent='Lombardi: '+lombardi.toFixed(1);document.getElementById('fp4').textContent='Lander: '+lander.toFixed(1);document.getElementById('fp5').textContent="O'Conner: "+oconner.toFixed(1);_ormLast={orm:orm,unit:unit};renderORMTable();document.getElementById('resultsSection').classList.add('show');}
""" + toggle_faq_js() + """
document.addEventListener('dfl:langchange',renderORMTable);
</script>"""
    return head("One Rep Max Calculator | حاسبة 1RM | Dot For Life", "Estimate 1RM using Epley, Brzycki, Lombardi, Lander, and O'Conner formulas.", "one-rep-max.html", "/styles/pages/tools_one-rep-max.css?v=20260625a") + f'\n<body class="tool-flagship-page no-subnav" data-tool="one-rep-max">\n{NAV}\n{hero}\n{tabs_html(tabs, "Fitness tools")}\n{ws}\n{FOOTER}\n{script}\n</body>\n</html>'

print("orm fn ok")

def gen_pregnancy():
    tabs = list(HEALTH_TABS)
    tabs[4] = (tabs[4][0], tabs[4][1], tabs[4][2], True)
    hero = """<div class="tool-hero"><div class="tool-hero-inner">
    <nav class="tool-breadcrumb" aria-label="Breadcrumb"><a href="/index.html"><span class="en">Home</span><span class="ar">الرئيسية</span></a><span class="tool-breadcrumb-sep">/</span><a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a><span class="tool-breadcrumb-sep">/</span><span><span class="en">Pregnancy Calculator</span><span class="ar">حاسبة الحمل</span></span></nav>
    <p class="tool-eyebrow"><span class="en">Health Tool · Naegele's Rule</span><span class="ar">أداة صحية · قاعدة ناغيل</span></p>
    <h1 id="tool-title"><span class="en">Pregnancy Due Date Calculator</span><span class="ar">حاسبة الحمل وموعد الولادة</span></h1>
    <p class="tool-hero-desc"><span class="en">Calculate due date, current week, trimester, and baby size — LMP, conception, or ultrasound methods.</span><span class="ar">احسبي موعد الولادة والأسبوع الحالي والثلث وحجم الجنين — LMP أو الإخصاب أو السونار.</span></p>
    <ul class="tool-trust"><li><span class="en">3 methods</span><span class="ar">3 طرق</span></li><li><span class="en">40-week guide</span><span class="ar">دليل 40 أسبوع</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li></ul>
  </div></div>"""
    ws = """<main class="tool-mn"><div class="tool-workspace">
    <div class="tool-panel pc-card"><div class="tool-panel-hdr"><h2><span class="en">Calculation Method</span><span class="ar">طريقة الحساب</span></h2></div>
      <div class="tool-panel-body t-body">
        <div class="t-tabs" role="tablist">
          <button type="button" class="t-tab active" onclick="switchTab('lmp',this)" role="tab" aria-selected="true"><span class="en">Last Period</span><span class="ar">آخر دورة</span></button>
          <button type="button" class="t-tab" onclick="switchTab('con',this)" role="tab" aria-selected="false"><span class="en">Conception</span><span class="ar">الإخصاب</span></button>
          <button type="button" class="t-tab" onclick="switchTab('us',this)" role="tab" aria-selected="false"><span class="en">Ultrasound</span><span class="ar">السونار</span></button>
        </div>
        <div class="t-tab-panel active" id="panel-lmp" role="tabpanel">
          <div class="t-fl"><label class="t-fl-l" for="lmp-date"><span class="en">First day of last period</span><span class="ar">أول يوم من آخر دورة</span></label><div class="t-fl-r"><input type="date" id="lmp-date"></div></div>
          <div class="t-fl"><label class="t-fl-l" for="cycle-len"><span class="en">Cycle length (days)</span><span class="ar">طول الدورة (يوم)</span></label><div class="t-fl-r"><input type="number" id="cycle-len" value="28" min="21" max="45"></div></div>
          <button class="t-btn" type="button" onclick="calcLMP()"><span class="en">Calculate</span><span class="ar">احسبي</span></button>
        </div>
        <div class="t-tab-panel" id="panel-con" role="tabpanel">
          <div class="t-fl"><label class="t-fl-l" for="con-date"><span class="en">Conception date</span><span class="ar">تاريخ الإخصاب</span></label><div class="t-fl-r"><input type="date" id="con-date"></div></div>
          <button class="t-btn" type="button" onclick="calcConception()"><span class="en">Calculate</span><span class="ar">احسبي</span></button>
        </div>
        <div class="t-tab-panel" id="panel-us" role="tabpanel">
          <div class="t-fl"><label class="t-fl-l" for="us-date"><span class="en">Ultrasound date</span><span class="ar">تاريخ السونار</span></label><div class="t-fl-r"><input type="date" id="us-date"></div></div>
          <div class="t-g2">
            <div class="t-fl"><label class="t-fl-l" for="us-wks"><span class="en">Weeks</span><span class="ar">أسابيع</span></label><div class="t-fl-r"><input type="number" id="us-wks" min="4" max="40" placeholder="0"></div></div>
            <div class="t-fl"><label class="t-fl-l" for="us-days"><span class="en">Days</span><span class="ar">أيام</span></label><div class="t-fl-r"><input type="number" id="us-days" min="0" max="6" placeholder="0"></div></div>
          </div>
          <button class="t-btn" type="button" onclick="calcUltrasound()"><span class="en">Calculate</span><span class="ar">احسبي</span></button>
        </div>
      </div>
    </div>
    <div class="tool-panel pc-card" id="result-card"><div class="tool-panel-hdr"><h2><span class="en">Your Results</span><span class="ar">نتائجك</span></h2></div>
      <div class="tool-panel-body t-body">
        <div class="pc-skeleton" id="skeleton-results"><div class="pc-skel-bar"></div><div class="pc-skel-bar"></div></div>
        <div id="results" style="display:none">
          <div class="t-hero-result"><div class="t-hero-lbl"><span class="en">Estimated Due Date</span><span class="ar">الموعد المتوقع للولادة</span></div><div class="t-hero-val" id="res-due" style="font-size:1.1rem">—</div><div id="res-due-ar" style="font-size:.78rem;color:var(--tool-muted);margin-top:4px"></div></div>
          <div class="t-metrics">
            <div class="t-metric"><div class="t-metric-val" id="res-week">—</div><div class="t-metric-lbl"><span class="en">Current week</span><span class="ar">الأسبوع الحالي</span></div><div id="res-week-sub" style="font-size:.65rem;color:var(--tool-muted)"></div></div>
            <div class="t-metric"><div class="t-metric-val" id="res-tri">—</div><div class="t-metric-lbl"><span class="en">Trimester</span><span class="ar">الثلث</span></div><div id="res-tri-sub" style="font-size:.65rem;color:var(--tool-muted)"></div></div>
            <div class="t-metric"><div class="t-metric-val" id="res-days">—</div><div class="t-metric-lbl"><span class="en">Days left</span><span class="ar">أيام متبقية</span></div><div id="res-days-sub" style="font-size:.65rem;color:var(--tool-muted)"></div></div>
          </div>
          <div class="pc-baby"><div class="pc-baby-emoji" id="res-emoji"></div><div><div class="pc-baby-lbl"><span class="en">Baby is the size of a</span><span class="ar">الجنين بحجم</span></div><div class="pc-baby-fruit" id="res-fruit"></div><div class="pc-baby-meta"><span class="en"><strong id="res-len"></strong> · <strong id="res-wt"></strong></span><span class="ar"><strong id="res-len-ar"></strong> · <strong id="res-wt-ar"></strong></span></div></div></div>
          <div class="t-timeline"><div class="t-timeline-labels"><span><span class="en">Week </span><span class="ar">أسبوع </span><span id="tl-wk-label">0</span><span class="en"> of 40</span><span class="ar"> من 40</span></span><span>40</span></div><div class="t-timeline-bar pc-timeline-wrap"><div class="t-timeline-fill" id="tl-fill" style="width:0%"></div><div class="pc-timeline-thumb" id="tl-thumb" style="left:0%"></div></div></div>
          <a class="t-journey-link" id="journey-banner" href="/pregnancy-journey.html"><span class="en">Follow Week <span id="banner-week">1</span> in detail →</span><span class="ar">← تابعي الأسبوع <span id="banner-week-ar">١</span> بالتفصيل</span></a>
        </div>
      </div>
    </div>
  </div>
  <div class="tool-below"><div class="t-section"><div class="t-section-label"><span class="en">How this is calculated</span><span class="ar">طريقة الحساب</span></div>
    <p class="en"><strong>LMP:</strong> Due date = LMP + 280 days (+ cycle adjustment). <strong>Conception:</strong> +266 days. <strong>Ultrasound:</strong> back-calculate LMP from scan age.</p>
    <p class="ar"><strong>آخر دورة:</strong> الموعد = LMP + 280 يوم. <strong>الإخصاب:</strong> +266 يوم. <strong>السونار:</strong> حساب LMP من عمر الجنين.</p>
  </div><div class="t-faq"><div class="t-faq-label"><span class="en">FAQ</span><span class="ar">أسئلة شائعة</span></div><div class="t-faq-title"><span class="en">Frequently Asked Questions</span><span class="ar">الأسئلة المتكررة</span></div>
""" + faq_block([
        ("How accurate is this calculator?", "ما مدى الدقة؟", "Uses Naegele's Rule — same as most providers. ±5 days for regular cycles.", "تستخدم قاعدة ناغيل — ±5 أيام للدورات المنتظمة."),
        ("Can the due date change?", "هل يمكن تغيير الموعد؟", "Yes — early ultrasound can adjust the date if cycles are irregular.", "نعم — السونار المبكر قد يعدّل الموعد."),
    ]) + """  </div></div>
  <section class="tool-tickets-rail"><header class="tool-tickets-head"><h2 class="tool-tickets-title"><span class="en">Related Tools</span><span class="ar">أدوات ذات صلة</span></h2></header>
    <div class="tool-tickets-track">
      <a href="/pregnancy-journey.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Pregnancy Journey</span><span class="ar">رحلة الحمل</span></h3></div></a>
      <a href="/tools/calorie-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Calories</span><span class="ar">السعرات</span></h3></div></a>
      <a href="/tools/water-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Water</span><span class="ar">الماء</span></h3></div></a>
      <a href="/tools/bmi-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">BMI</span><span class="ar">BMI</span></h3></div></a>
    </div>
  </section></main>"""
    # Patch displayResults to use show/hide on #results
    calc = CALC_BLOCK.replace(
        "document.getElementById('results').classList.remove('show');",
        "document.getElementById('results').style.display='none';"
    ).replace(
        "ra.classList.add('show');",
        "ra.style.display='block';"
    ).replace(
        "document.getElementById('results').classList.remove('show');\n  document.getElementById('skeleton-results').classList.remove('show');",
        "document.getElementById('results').style.display='none';\n  document.getElementById('skeleton-results').classList.remove('show');"
    )
    script = f"""
<script src="/scripts/global.js?v=20260618a" defer></script>
<script>
{BD_BLOCK}
{calc}
""" + toggle_faq_js() + """
document.addEventListener('dfl:langchange',function(){});
</script>"""
    return head("Pregnancy Calculator | حاسبة الحمل | Dot For Life", "Calculate pregnancy due date, week, trimester, and baby development.", "pregnancy-calculator.html", "/styles/pages/tools_pregnancy-calculator.css?v=20260625a") + f'\n<body class="tool-flagship-page no-subnav" data-tool="pregnancy-calculator">\n{NAV}\n{hero}\n{tabs_html(tabs, "Health tools")}\n{ws}\n{FOOTER}\n{script}\n</body>\n</html>'

print("preg fn ok")

def gen_ramadan():
    tabs = list(ISLAMIC_TABS)
    for i,t in enumerate(tabs):
        if 'ramadan' in t[0]: tabs[i]=(t[0],t[1],t[2],True)
    hero = """<div class="tool-hero"><div class="tool-hero-inner">
    <nav class="tool-breadcrumb" aria-label="Breadcrumb"><a href="/index.html"><span class="en">Home</span><span class="ar">الرئيسية</span></a><span class="tool-breadcrumb-sep">/</span><a href="/library.html"><span class="en">Library</span><span class="ar">المكتبة</span></a><span class="tool-breadcrumb-sep">/</span><span><span class="en">Ramadan Calories</span><span class="ar">سعرات رمضان</span></span></nav>
    <p class="tool-eyebrow"><span class="en">Islamic Tool · Fasting-Adapted</span><span class="ar">أداة إسلامية · للصيام</span></p>
    <h1 id="tool-title"><span class="en">Ramadan Calorie Calculator</span><span class="ar">حاسبة السعرات في رمضان</span></h1>
    <p class="tool-hero-desc"><span class="en">Personalised Suhoor and Iftar calorie targets with hydration plan — Mifflin-St Jeor adapted for fasting.</span><span class="ar">أهداف سعرات السحور والإفطار مع خطة ترطيب — ميفلين-سانت جيور للصيام.</span></p>
    <ul class="tool-trust"><li><span class="en">Mifflin-St Jeor</span><span class="ar">ميفلين-سانت جيور</span></li><li><span class="en">35/65 split</span><span class="ar">35/65 توزيع</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li></ul>
  </div></div>"""
    ws = """<main class="tool-mn"><div class="tool-workspace">
    <div class="tool-panel rc-card"><div class="tool-panel-hdr"><h2><span class="en">Your Ramadan Profile</span><span class="ar">ملفك في رمضان</span></h2></div>
      <div class="tool-panel-body t-body">
        <div class="t-g2">
          <div class="t-fl"><label class="t-fl-l" for="age"><span class="en">Age</span><span class="ar">العمر</span></label><div class="t-fl-r"><input type="number" id="age" value="30" min="14" max="90"></div></div>
          <div class="t-fl"><label class="t-fl-l" for="gender"><span class="en">Gender</span><span class="ar">الجنس</span></label><div class="t-fl-r"><select id="gender"><option value="male">Male / ذكر</option><option value="female">Female / أنثى</option></select></div></div>
          <div class="t-fl"><label class="t-fl-l" for="weight"><span class="en">Weight (kg)</span><span class="ar">الوزن (كغ)</span></label><div class="t-fl-r"><input type="number" id="weight" value="75" min="30" max="250"><span class="t-fl-u">kg</span></div></div>
          <div class="t-fl"><label class="t-fl-l" for="height"><span class="en">Height (cm)</span><span class="ar">الطول (سم)</span></label><div class="t-fl-r"><input type="number" id="height" value="170" min="100" max="230"><span class="t-fl-u">cm</span></div></div>
        </div>
        <div class="t-fl"><label class="t-fl-l" for="activity"><span class="en">Activity during Ramadan</span><span class="ar">النشاط في رمضان</span></label><div class="t-fl-r"><select id="activity"><option value="1.2">Sedentary / خامل</option><option value="1.375" selected>Light / خفيف</option><option value="1.55">Moderate / متوسط</option><option value="1.725">Active / نشط</option></select></div></div>
        <div class="t-step"><span class="en">Ramadan Goal</span><span class="ar">هدف رمضان</span></div>
        <div class="rc-goal-grid">
          <button type="button" class="rc-goal" data-goal="lose"><span class="en">Lose Weight</span><span class="ar">خسارة وزن</span></button>
          <button type="button" class="rc-goal active" data-goal="maintain"><span class="en">Maintain</span><span class="ar">ثبات</span></button>
          <button type="button" class="rc-goal" data-goal="gain"><span class="en">Keep Muscle</span><span class="ar">العضلات</span></button>
        </div>
        <button class="t-btn" type="button" id="calcBtn"><span class="en">Calculate Nutrition</span><span class="ar">احسب التغذية</span></button>
      </div>
    </div>
    <div class="tool-panel rc-card" id="results"><div class="tool-panel-hdr"><h2><span class="en">Your Plan</span><span class="ar">خطتك</span></h2></div>
      <div class="tool-panel-body t-body">
        <div class="t-metrics">
          <div class="t-metric"><div class="t-metric-val" id="r-tdee">—</div><div class="t-metric-lbl"><span class="en">Ramadan TDEE</span><span class="ar">السعرات اليومية</span></div></div>
          <div class="t-metric"><div class="t-metric-val" id="r-target">—</div><div class="t-metric-lbl"><span class="en">Target Intake</span><span class="ar">الاستهلاك المستهدف</span></div></div>
          <div class="t-metric"><div class="t-metric-val" id="r-water">—</div><div class="t-metric-lbl"><span class="en">Water (L)</span><span class="ar">الماء (لتر)</span></div></div>
        </div>
        <div class="rc-meals">
          <div class="rc-meal"><div class="t-step"><span class="en">Suhoor (35%)</span><span class="ar">السحور (35%)</span></div><div class="rc-meal-cal" id="r-suhoor">—</div><div class="rc-meal-sub"><span class="en">kcal · slow carbs + protein</span><span class="ar">سعرة · كarb بطيئة + بروتين</span></div></div>
          <div class="rc-meal"><div class="t-step"><span class="en">Iftar (65%)</span><span class="ar">الإفطار (65%)</span></div><div class="rc-meal-cal" id="r-iftar">—</div><div class="rc-meal-sub"><span class="en">kcal · balanced plate</span><span class="ar">سعرة · طبق متوازن</span></div></div>
        </div>
        <div class="t-step"><span class="en">Hydration Plan</span><span class="ar">خطة الترطيب</span></div>
        <div id="waterGlassesLabel" style="font-size:.82rem;color:var(--tool-muted);margin-bottom:8px"></div>
        <div class="rc-water-glasses" id="waterGlasses"></div>
        <p class="t-disclaimer"><span class="en">For informational purposes only. Consult a doctor before dietary changes during fasting.</span><span class="ar">لأغراض معلوماتية فقط. استشر طبيبك قبل تغيير نظامك الغذائي أثناء الصيام.</span></p>
      </div>
    </div>
  </div>
  <div class="tool-below"><div class="t-section"><div class="t-section-label"><span class="en">How this is calculated</span><span class="ar">طريقة الحساب</span></div>
    <p class="en">BMR via Mifflin-St Jeor × activity × 0.87 fasting factor. Goals: lose −18%, gain +5%. Suhoor 35%, Iftar 65%. Water: 35 ml/kg + 300 ml GCC heat.</p>
    <p class="ar">BMR بميفلين-سانت جيور × النشاط × 0.87 للصيام. خسارة −18%، زيادة +5%. سحور 35%، إفطار 65%. ماء: 35 مل/كغ + 300 مل حرارة الخليج.</p>
  </div><div class="t-faq"><div class="t-faq-label"><span class="en">FAQ</span><span class="ar">أسئلة شائعة</span></div><div class="t-faq-title"><span class="en">Frequently Asked Questions</span><span class="ar">الأسئلة المتكررة</span></div>
""" + faq_block([
        ("Why is TDEE lower during Ramadan?", "لماذا TDEE أقل في رمضان?", "Fasting reduces daily expenditure ~13% due to lower activity and circadian changes.", "الصيام يقلل الحرق ~13% بسبب النشاط الأقل."),
        ("Should I skip Suhoor?", "هل أتخطى السحور؟", "No — Suhoor sustains energy and protects muscle mass throughout the fast.", "لا — السحور يحافظ على الطاقة وكتلة العضلات."),
    ]) + """  </div></div>
  <section class="tool-tickets-rail"><header class="tool-tickets-head"><h2 class="tool-tickets-title"><span class="en">Related Tools</span><span class="ar">أدوات ذات صلة</span></h2></header>
    <div class="tool-tickets-track">
      <a href="/tools/calorie-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Calorie Calculator</span><span class="ar">حاسبة السعرات</span></h3></div></a>
      <a href="/tools/water-calculator.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Water Intake</span><span class="ar">حاسبة الماء</span></h3></div></a>
      <a href="/tools/prayer-times.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Prayer Times</span><span class="ar">أوقات الصلاة</span></h3></div></a>
      <a href="/tools/hijri-converter.html" class="tool-ticket"><div class="tool-ticket-body"><h3><span class="en">Hijri Converter</span><span class="ar">الهجري</span></h3></div></a>
    </div>
  </section></main>"""
    script = """
<script src="/scripts/global.js?v=20260618a" defer></script>
<script>
var currentGoal='maintain';
var _rcWater={glasses:0,water:0};
document.querySelectorAll('.rc-goal').forEach(function(btn){btn.addEventListener('click',function(){document.querySelectorAll('.rc-goal').forEach(function(b){b.classList.remove('active');});btn.classList.add('active');currentGoal=btn.dataset.goal;});});
function animateKPI(id,target,suffix){suffix=suffix||'';var el=document.getElementById(id),dur=700,s=performance.now();(function step(n){var p=Math.min((n-s)/dur,1),e=1-Math.pow(1-p,3);el.textContent=Math.round(target*e)+suffix;if(p<1)requestAnimationFrame(step);else el.textContent=target+suffix;})(s);}
function renderWaterLabel(){var el=document.getElementById('waterGlassesLabel');if(!el||!_rcWater.glasses)return;el.innerHTML=getLang()==='ar'?'<span class="ar">اشرب <strong>'+_rcWater.glasses+' كوب</strong> ('+_rcWater.water.toFixed(1)+' لتر)</span>':'<span class="en">Drink <strong>'+_rcWater.glasses+' glasses</strong> ('+_rcWater.water.toFixed(1)+'L)</span>';}
function calculate(){var age=parseFloat(document.getElementById('age').value)||30;var gender=document.getElementById('gender').value;var weight=parseFloat(document.getElementById('weight').value)||75;var height=parseFloat(document.getElementById('height').value)||170;var activity=parseFloat(document.getElementById('activity').value)||1.375;var bmr; if(gender==='male') bmr=10*weight+6.25*height-5*age+5; else bmr=10*weight+6.25*height-5*age-161;var fastingFactor=0.87;var tdee=Math.round(bmr*activity*fastingFactor);var target; if(currentGoal==='lose') target=Math.round(tdee*0.82); else if(currentGoal==='gain') target=Math.round(tdee*1.05); else target=tdee;var suhoor=Math.round(target*0.35);var iftar=Math.round(target*0.65);var water=Math.round((weight*35+300)/100)/10;var glasses=Math.round(water/0.25);animateKPI('r-tdee',tdee);animateKPI('r-target',target);document.getElementById('r-water').textContent=water.toFixed(1);animateKPI('r-suhoor',suhoor,' kcal');animateKPI('r-iftar',iftar,' kcal');var wg=document.getElementById('waterGlasses');wg.innerHTML='';for(var i=0;i<glasses;i++){var sp=document.createElement('span');sp.textContent='🥛';wg.appendChild(sp);setTimeout(function(x){return function(){x.classList.add('filled');};}(sp),(i*60)+200);}_rcWater={glasses:glasses,water:water};renderWaterLabel();document.getElementById('results').classList.add('show');}
""" + toggle_faq_js() + """
document.getElementById('calcBtn').addEventListener('click',calculate);
document.addEventListener('dfl:langchange',renderWaterLabel);
</script>"""
    return head("Ramadan Calorie Calculator | حاسبة سعرات رمضان | Dot For Life", "Ramadan calorie and hydration calculator with Suhoor/Iftar split.", "ramadan-calorie-calculator.html", "/styles/pages/tools_ramadan-calorie-calculator.css?v=20260625a") + f'\n<body class="tool-flagship-page no-subnav" data-tool="ramadan-calorie-calculator">\n{NAV}\n{hero}\n{tabs_html(tabs, "Islamic tools")}\n{ws}\n{FOOTER}\n{script}\n</body>\n</html>'

FILES = {
    'age-calculator.html': gen_age,
    'one-rep-max.html': gen_orm,
    'pregnancy-calculator.html': gen_pregnancy,
    'ramadan-calorie-calculator.html': gen_ramadan,
}

if __name__ == '__main__':
    for name, fn in FILES.items():
        path = TOOLS / name
        content = fn()
        # fix typo
        content = content.replace('الق próximo', 'القادم')
        path.write_text(content, encoding='utf-8')
        print(f'Wrote {path} ({path.stat().st_size:,} bytes)')
