#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared site chrome for recipe section — matches homepage branding."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "partials"

LANG_BOOT = """<script>(function(){var p=new URLSearchParams(location.search),gd=(function(){try{var z=(Intl.DateTimeFormat().resolvedOptions().timeZone||"");return /Riyadh|Dubai|Qatar|Bahrain|Kuwait|Muscat|Baghdad|Amman|Beirut|Damascus|Aden|Cairo|Khartoum/i.test(z)?"ar":"en";}catch(e){return "ar";}})(),l=p.get("lang")||localStorage.getItem("dfl-lang")||gd,t=p.get("theme")||localStorage.getItem("dfl-theme")||"light",h=document.documentElement;h.setAttribute("data-theme",t);h.setAttribute("data-lang",l);h.setAttribute("lang",l);h.setAttribute("dir",l==="ar"?"rtl":"ltr");if(p.get("lang"))localStorage.setItem("dfl-lang",l);if(p.get("theme"))localStorage.setItem("dfl-theme",t);var pt=document.getElementById("dfl-page-title");if(pt){var tl=l==="ar"?(pt.getAttribute("data-ar")||pt.getAttribute("data-en")):(pt.getAttribute("data-en")||pt.getAttribute("data-ar"));if(tl)document.title=tl+" | DOTFORLIFE";}})()</script>"""

RECIPE_HEAD_ASSETS = """<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Almarai:wght@300;400;700;800&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="/styles/global.css?v=20260624t"/>
<link rel="stylesheet" href="/styles/home.css?v=20260624g"/>
<link rel="stylesheet" href="/styles/pages/recipes.css?v=20260709f"/>"""

MOBILE_DROPDOWN = """<div class="mobile-dropdown" id="mobile-dropdown" aria-hidden="true">
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
    <a href="/life-guide.html"><span class="en">Guides</span><span class="ar">الأدلة</span></a>
  </div>
  <div class="md-controls">
    <button class="nav-btn" id="lang-toggle-mobile"><span class="en">عربي</span><span class="ar">English</span></button>
    <button class="nav-btn" id="theme-toggle-mobile">
      <svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      <svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
    </button>
  </div>
</div>"""


def site_header() -> str:
    return (PARTIALS / "header.html").read_text(encoding="utf-8").strip()


def site_footer() -> str:
    return (PARTIALS / "footer.html").read_text(encoding="utf-8").strip()
