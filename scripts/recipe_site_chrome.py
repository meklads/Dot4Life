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
<link href="https://fonts.googleapis.com/css2?family=Almarai:wght@300;400;700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="/styles/global.css?v=20260624t"/>
<link rel="stylesheet" href="/styles/home.css?v=20260624g"/>
<link rel="stylesheet" href="/styles/pages/articles.css?v=20260608u"/>
<link rel="stylesheet" href="/styles/pages/recipes.css?v=20260709i"/>"""

def mobile_dropdown() -> str:
    return (PARTIALS / "mobile-dropdown.html").read_text(encoding="utf-8").strip()


MOBILE_DROPDOWN = mobile_dropdown()


def site_header() -> str:
    return (PARTIALS / "header.html").read_text(encoding="utf-8").strip()


def site_footer() -> str:
    return (PARTIALS / "footer.html").read_text(encoding="utf-8").strip()
