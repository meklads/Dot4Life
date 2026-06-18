#!/usr/bin/env python3
"""Pre-flight analysis for Batch 5: Check all articles and group by type."""
import re, os

BLOG = "/Users/ghousemac/Desktop/Turriva/d4l/Dot4Life/blog"

all_articles = [
    # Type A — clean bilingual spans in body (21 articles)
    # Finance
    "building-personal-savings-system",
    "children-education-savings-guide", 
    "complete-household-budget-system",
    "end-of-service-benefits-expats",
    "life-insurance-gulf-families",
    "starting-side-business-saudi-uae",
    # Family / Parenting
    "choosing-right-school-child-gulf",
    "complete-family-financial-planning",
    "complete-family-systems-productivity-hub",
    "family-nutrition-on-budget",
    "managing-screen-time-children",
    "organize-life-daily-systems",
    "stress-management-working-parents",
    "teaching-children-financial-literacy",
    # Health
    "complete-gulf-family-health-wellness",
    "managing-healthcare-costs-families",
    "preparing-for-pregnancy-guide",
    # Travel / Islamic
    "complete-family-travel-activities-hub",
    "complete-islamic-lifestyle-guide",
    "family-friendly-activities-gulf-cities",
    # Holistic
    "complete-gulf-family-financial-life-hub",
    # Type B — main .html is EN, -ar.html has AR content (4 articles)
    "emergency-fund-calculator-guide",
    "family-budget-planning-guide",
    "house-affordability-single-income-guide",
    "umrah-packing-checklist-guide",
]

for name in all_articles:
    main_path = f"{BLOG}/{name}.html"
    ar_path = f"{BLOG}/{name}-ar.html"
    en_path = f"{BLOG}/{name}-en.html"
    
    issues = []
    
    # Check main file
    if os.path.exists(main_path):
        with open(main_path, 'r') as f:
            main_html = f.read()
        
        body_match = re.search(r'<article class="article-body">(.*?)</article>', main_html, re.DOTALL)
        if body_match:
            body = body_match.group(1)
            text = re.sub(r'<[^>]+>', ' ', body)
            text = re.sub(r'\s+', ' ', text)
            main_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', text))
            main_ar = len(re.findall(r'[؀-ۿ]', text))
            
            en_in_body = len(re.findall(r'<span class="en">', body))
            ar_in_body = len(re.findall(r'<span class="ar">', body))
        else:
            main_en = main_ar = en_in_body = ar_in_body = 0
        
        has_layout = 'article-layout' in main_html
        has_sidebar = 'article-sidebar' in main_html
        
        if has_layout and has_sidebar:
            issues.append("Already BOOM ✅")
        else:
            issues.append("Needs restructuring")
        
        if main_ar > 100 and en_in_body > 0:
            issues.append(f"Type A (spans in body)")
        elif main_en > 100 and main_ar == 0:
            issues.append(f"EN body, check -ar.html for AR")
        elif main_ar > 100 and main_en > 50:
            issues.append(f"Type B mixed content")
        else:
            issues.append(f"AR={main_ar}, EN={main_en}")
    else:
        main_en = main_ar = 0
        issues.append("NO MAIN FILE")
    
    # Check AR file
    has_ar = os.path.exists(ar_path)
    needs_ar_redirect = False
    
    if has_ar:
        with open(ar_path, 'r') as f:
            ar_html = f.read()
        is_redirect = 'refresh' in ar_html
        if not is_redirect:
            ar_body = re.search(r'<article class="article-body">(.*?)</article>', ar_html, re.DOTALL)
            if ar_body:
                ar_text = re.sub(r'<[^>]+>', ' ', ar_body.group(1))
                ar_text = re.sub(r'\s+', ' ', ar_text)
                ar_ar = len(re.findall(r'[؀-ۿ]', ar_text))
                ar_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', ar_text))
                if ar_ar > 100:
                    needs_ar_redirect = True
                    issues.append(f"-ar.html has AR={ar_ar} content (needs to move to .html)")
    
    # Check EN file
    has_en = os.path.exists(en_path)
    
    print(f"{'⚠️' if 'Needs' in issues[0] else '✅' if issues[0]=='Already BOOM ✅' else '❌'} {name:40s} | Main: AR={main_ar:5d} EN={main_en:4d} | AR-file={'✅' if has_ar else '❌'} EN-file={'✅' if has_en else '❌'} | {issues[0]}")
