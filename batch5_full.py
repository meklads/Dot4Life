#!/usr/bin/env python3
"""
Batch 5: Complete BOOM compliance for 25 articles.
Each article has:
  - .html = English content (needs to become AR version with clean Arabic)
  - -ar.html = Mixed AR/EN (source for Arabic extraction)
  - No -en.html (needs to be created)

Strategy:
  1. Extract clean Arabic from -ar.html (tag-aware filtering)
  2. Extract clean English from .html
  3. Build BOOM-compliant HTML for both
  4. Write .html = Arabic, -en.html = English, -ar.html = redirect
"""

import re, os, shutil

BLOG = "/Users/ghousemac/Desktop/Turriva/d4l/Dot4Life/blog"

# ─── Category defaults ─────────────────────────────────────
CATEGORY_CONFIG = {
    "finance": {
        "cta_ar": {"title": "خطط ميزانيتك", "desc": "استخدم أدوات التخطيط المالي لإدارة أموالك.", "btn": "ابدأ الآن ←", "link": "/tools/budget-calculator.html"},
        "cta_en": {"title": "Plan Your Finances", "desc": "Use financial planning tools to manage your money.", "btn": "Start Now →", "link": "/tools/budget-calculator.html"},
        "tools_ar": [("حاسبة الميزانية", "/tools/budget-calculator.html"), ("حاسبة الزكاة", "/tools/zakat-calculator.html"), ("محول التاريخ", "/tools/hijri-converter.html")],
        "tools_en": [("Budget Calculator", "/tools/budget-calculator.html"), ("Zakat Calculator", "/tools/zakat-calculator.html"), ("Hijri Converter", "/tools/hijri-converter.html")],
    },
    "savings": {
        "cta_ar": {"title": "ابدأ الادخار اليوم", "desc": "استخدم حاسبة الادخار لتحقيق أهدافك المالية.", "btn": "احسب الآن ←", "link": "/tools/budget-calculator.html"},
        "cta_en": {"title": "Start Saving Today", "desc": "Use the savings calculator to reach your financial goals.", "btn": "Calculate Now →", "link": "/tools/budget-calculator.html"},
        "tools_ar": [("حاسبة الادخار", "/tools/budget-calculator.html"), ("حاسبة الزكاة", "/tools/zakat-calculator.html"), ("محول التاريخ", "/tools/hijri-converter.html")],
        "tools_en": [("Savings Calculator", "/tools/budget-calculator.html"), ("Zakat Calculator", "/tools/zakat-calculator.html"), ("Hijri Converter", "/tools/hijri-converter.html")],
    },
    "family": {
        "cta_ar": {"title": "نظم حياتك العائلية", "desc": "اكتشف أدوات تنظيم الأسرة والتربية.", "btn": "استكشف ←", "link": "/tools/calorie-calculator.html"},
        "cta_en": {"title": "Organize Family Life", "desc": "Discover tools for family organization and parenting.", "btn": "Explore →", "link": "/tools/calorie-calculator.html"},
        "tools_ar": [("حاسبة السعرات", "/tools/calorie-calculator.html"), ("حاسبة الماء", "/tools/water-calculator.html"), ("حاسبة BMI", "/tools/bmi-calculator.html")],
        "tools_en": [("Calorie Calculator", "/tools/calorie-calculator.html"), ("Water Calculator", "/tools/water-calculator.html"), ("BMI Calculator", "/tools/bmi-calculator.html")],
    },
    "health": {
        "cta_ar": {"title": "احسب مؤشرات صحتك", "desc": "استخدم أدوات الصحة لتتبع لياقتك.", "btn": "احسب الآن ←", "link": "/tools/bmi-calculator.html"},
        "cta_en": {"title": "Calculate Your Health", "desc": "Use health tools to track your fitness.", "btn": "Calculate Now →", "link": "/tools/bmi-calculator.html"},
        "tools_ar": [("حاسبة BMI", "/tools/bmi-calculator.html"), ("حاسبة الماء", "/tools/water-calculator.html"), ("حاسبة السعرات", "/tools/calorie-calculator.html")],
        "tools_en": [("BMI Calculator", "/tools/bmi-calculator.html"), ("Water Calculator", "/tools/water-calculator.html"), ("Calorie Calculator", "/tools/calorie-calculator.html")],
    },
    "travel": {
        "cta_ar": {"title": "خطط لسفرك", "desc": "احسب ميزانية سفرك واستكشف الوجهات.", "btn": "خطط الآن ←", "link": "/tools/travel-budget.html"},
        "cta_en": {"title": "Plan Your Trip", "desc": "Calculate your travel budget and explore destinations.", "btn": "Plan Now →", "link": "/tools/travel-budget.html"},
        "tools_ar": [("حاسبة السفر", "/tools/travel-budget.html"), ("محول التاريخ", "/tools/hijri-converter.html"), ("اتجاه القبلة", "/tools/qibla.html")],
        "tools_en": [("Travel Budget", "/tools/travel-budget.html"), ("Hijri Converter", "/tools/hijri-converter.html"), ("Qibla Direction", "/tools/qibla.html")],
    },
    "islamic": {
        "cta_ar": {"title": "احسب زكاتك", "desc": "احسب زكاتك بدقة وفق الأحكام الشرعية.", "btn": "احسب الآن ←", "link": "/tools/zakat-calculator.html"},
        "cta_en": {"title": "Calculate Your Zakat", "desc": "Calculate your zakat accurately.", "btn": "Calculate Now →", "link": "/tools/zakat-calculator.html"},
        "tools_ar": [("حاسبة الزكاة", "/tools/zakat-calculator.html"), ("محول التاريخ", "/tools/hijri-converter.html"), ("اتجاه القبلة", "/tools/qibla.html")],
        "tools_en": [("Zakat Calculator", "/tools/zakat-calculator.html"), ("Hijri Converter", "/tools/hijri-converter.html"), ("Qibla Direction", "/tools/qibla.html")],
    },
    "realestate": {
        "cta_ar": {"title": "احسب تمويلك العقاري", "desc": "قارن بين خيارات التمويل واحسب أقساطك.", "btn": "احسب الآن ←", "link": "/tools/mortgage-calculator.html"},
        "cta_en": {"title": "Calculate Your Mortgage", "desc": "Compare financing options and calculate payments.", "btn": "Calculate Now →", "link": "/tools/mortgage-calculator.html"},
        "tools_ar": [("حاسبة التمويل", "/tools/mortgage-calculator.html"), ("حاسبة الزكاة", "/tools/zakat-calculator.html"), ("محول التاريخ", "/tools/hijri-converter.html")],
        "tools_en": [("Mortgage Calculator", "/tools/mortgage-calculator.html"), ("Zakat Calculator", "/tools/zakat-calculator.html"), ("Hijri Converter", "/tools/hijri-converter.html")],
    },
    "holistic": {
        "cta_ar": {"title": "ابدأ رحلتك", "desc": "استكشف الأدوات الشاملة لتحسين حياتك.", "btn": "استكشف ←", "link": "/tools/calorie-calculator.html"},
        "cta_en": {"title": "Start Your Journey", "desc": "Explore comprehensive tools to improve your life.", "btn": "Explore →", "link": "/tools/calorie-calculator.html"},
        "tools_ar": [("حاسبة السعرات", "/tools/calorie-calculator.html"), ("حاسبة الماء", "/tools/water-calculator.html"), ("حاسبة BMI", "/tools/bmi-calculator.html")],
        "tools_en": [("Calorie Calculator", "/tools/calorie-calculator.html"), ("Water Calculator", "/tools/water-calculator.html"), ("BMI Calculator", "/tools/bmi-calculator.html")],
    },
}

# ─── Article configurations ─────────────────────────────────
ARTICLES = [
    # === Finance (6) ===
    {"name": "building-personal-savings-system", "cat": "savings",
     "title_ar": "بناء نظام ادخار شخصي: دليل عملي للعائلات", "title_en": "Building a Personal Savings System: Practical Guide",
     "desc_ar": "دليل عملي لبناء نظام ادخار شخصي ناجح للعائلات في الخليج.", "desc_en": "Practical guide to building a successful personal savings system for Gulf families.",
     "tags_ar": ["#ادخار", "#مالية", "#توفير", "#عائلة"], "tags_en": ["#savings", "#finance", "#family", "#budget"]},
    
    {"name": "children-education-savings-guide", "cat": "savings",
     "title_ar": "دليل ادخار تعليم الأطفال: خطط لمستقبلهم", "title_en": "Children's Education Savings Guide: Plan Their Future",
     "desc_ar": "دليل شامل للادخار لتعليم الأطفال في الخليج — خطط واستثمر لمستقبلهم.", "desc_en": "Complete guide to saving for children's education in the Gulf — plan and invest for their future.",
     "tags_ar": ["#تعليم", "#ادخار", "#أطفال", "#مالية"], "tags_en": ["#education", "#savings", "#children", "#finance"]},
    
    {"name": "complete-household-budget-system", "cat": "finance",
     "title_ar": "نظام الميزانية المنزلية الشامل", "title_en": "Complete Household Budget System",
     "desc_ar": "نظام متكامل لإدارة ميزانية المنزل في الخليج — خطط، وفر، واستثمر.", "desc_en": "Integrated household budget management system for the Gulf — plan, save, invest.",
     "tags_ar": ["#ميزانية", "#منزل", "#مالية", "#تخطيط"], "tags_en": ["#budget", "#household", "#finance", "#planning"]},
    
    {"name": "end-of-service-benefits-expats", "cat": "finance",
     "title_ar": "دليل مكافأة نهاية الخدمة للوافدين في الخليج", "title_en": "End of Service Benefits Guide for Expats in the Gulf",
     "desc_ar": "دليل شامل لحساب مكافأة نهاية الخدمة للوافدين في دول الخليج.", "desc_en": "Complete guide to calculating end-of-service benefits for expats in Gulf countries.",
     "tags_ar": ["#نهاية-خدمة", "#وافدين", "#مالية", "#خليج"], "tags_en": ["#end-of-service", "#expat", "#finance", "#gulf"]},
    
    {"name": "life-insurance-gulf-families", "cat": "finance",
     "title_ar": "دليل التأمين على الحياة للعائلات الخليجية", "title_en": "Life Insurance Guide for Gulf Families",
     "desc_ar": "دليل شامل للتأمين على الحياة في الخليج — الأنواع، الفوائد، والنصائح.", "desc_en": "Complete guide to life insurance in the Gulf — types, benefits, and tips.",
     "tags_ar": ["#تأمين", "#حياة", "#عائلة", "#مالية"], "tags_en": ["#insurance", "#life", "#family", "#finance"]},
    
    {"name": "starting-side-business-saudi-uae", "cat": "finance",
     "title_ar": "دليل بدء مشروع جانبي في السعودية والإمارات", "title_en": "Starting a Side Business in Saudi Arabia and UAE Guide",
     "desc_ar": "دليل شامل لبدء مشروع جانبي في السعودية والإمارات — التراخيص، التكاليف، والنصائح.", "desc_en": "Complete guide to starting a side business in Saudi Arabia and UAE — licenses, costs, tips.",
     "tags_ar": ["#مشروع", "#جانبي", "#ريادة", "#أعمال"], "tags_en": ["#business", "#side-hustle", "#entrepreneurship", "#startup"]},

    # === Family / Parenting (8) ===
    {"name": "choosing-right-school-child-gulf", "cat": "family",
     "title_ar": "دليل اختيار المدرسة المناسبة لطفلك في الخليج", "title_en": "Guide to Choosing the Right School for Your Child in the Gulf",
     "desc_ar": "دليل شامل لاختيار المدرسة المناسبة لأطفالك في دول الخليج.", "desc_en": "Complete guide to choosing the right school for your children in Gulf countries.",
     "tags_ar": ["#مدارس", "#تعليم", "#أطفال", "#تربية"], "tags_en": ["#schools", "#education", "#children", "#parenting"]},
    
    {"name": "complete-family-financial-planning", "cat": "finance",
     "title_ar": "التخطيط المالي العائلي الشامل", "title_en": "Complete Family Financial Planning",
     "desc_ar": "دليل شامل للتخطيط المالي للعائلة في الخليج — الميزانية، الادخار، والاستثمار.", "desc_en": "Complete family financial planning guide for the Gulf — budget, save, invest.",
     "tags_ar": ["#تخطيط", "#مالي", "#عائلة", "#مستقبل"], "tags_en": ["#planning", "#financial", "#family", "#future"]},
    
    {"name": "complete-family-systems-productivity-hub", "cat": "family",
     "title_ar": "منظومة الإنتاجية العائلية الشاملة", "title_en": "Complete Family Systems & Productivity Hub",
     "desc_ar": "منظومة متكاملة لتنظيم وإدارة شؤون الأسرة في الخليج.", "desc_en": "Integrated system for organizing and managing family affairs in the Gulf.",
     "tags_ar": ["#إنتاجية", "#تنظيم", "#عائلة", "#نظام"], "tags_en": ["#productivity", "#organization", "#family", "#system"]},
    
    {"name": "family-nutrition-on-budget", "cat": "family",
     "title_ar": "التغذية العائلية بميزانية محدودة", "title_en": "Family Nutrition on a Budget",
     "desc_ar": "دليل للتغذية الصحية للعائلة في الخليج بدون إرهاق الميزانية.", "desc_en": "Guide to healthy family nutrition in the Gulf without straining the budget.",
     "tags_ar": ["#تغذية", "#صحة", "#ميزانية", "#عائلة"], "tags_en": ["#nutrition", "#health", "#budget", "#family"]},
    
    {"name": "managing-screen-time-children", "cat": "family",
     "title_ar": "إدارة وقت الشاشة للأطفال", "title_en": "Managing Screen Time for Children",
     "desc_ar": "دليل عملي لإدارة وقت الشاشة للأطفال في العصر الرقمي.", "desc_en": "Practical guide to managing children's screen time in the digital age.",
     "tags_ar": ["#شاشة", "#أطفال", "#تربية", "#رقمي"], "tags_en": ["#screentime", "#children", "#parenting", "#digital"]},
    
    {"name": "organize-life-daily-systems", "cat": "family",
     "title_ar": "نظم حياتك: أنظمة يومية للعائلات", "title_en": "Organize Your Life: Daily Systems for Families",
     "desc_ar": "أنظمة يومية عملية لتنظيم حياة العائلة في الخليج.", "desc_en": "Practical daily systems for organizing family life in the Gulf.",
     "tags_ar": ["#تنظيم", "#حياة", "#عائلة", "#نظام"], "tags_en": ["#organization", "#life", "#family", "#system"]},
    
    {"name": "stress-management-working-parents", "cat": "family",
     "title_ar": "إدارة التوتر للآباء العاملين في الخليج", "title_en": "Stress Management for Working Parents in the Gulf",
     "desc_ar": "دليل عملي لإدارة التوتر للآباء والأمهات العاملين في الخليج.", "desc_en": "Practical stress management guide for working parents in the Gulf.",
     "tags_ar": ["#توتر", "#آباء", "#عمل", "#صحة-نفسية"], "tags_en": ["#stress", "#parents", "#work", "#mentalhealth"]},
    
    {"name": "teaching-children-financial-literacy", "cat": "family",
     "title_ar": "تعليم الأطفال الثقافة المالية", "title_en": "Teaching Children Financial Literacy",
     "desc_ar": "دليل لتعليم الأطفال أساسيات الثقافة المالية في الخليج.", "desc_en": "Guide to teaching children financial literacy basics in the Gulf.",
     "tags_ar": ["#ثقافة-مالية", "#أطفال", "#تعليم", "#تربية"], "tags_en": ["#financial-literacy", "#children", "#education", "#parenting"]},

    # === Health (3) ===
    {"name": "complete-gulf-family-health-wellness", "cat": "health",
     "title_ar": "الصحة والعافية الشاملة للعائلة الخليجية", "title_en": "Complete Gulf Family Health & Wellness",
     "desc_ar": "دليل شامل للصحة والعافية للعائلة في الخليج — تغذية، لياقة، ونوم.", "desc_en": "Complete health and wellness guide for Gulf families — nutrition, fitness, sleep.",
     "tags_ar": ["#صحة", "#عافية", "#عائلة", "#خليج"], "tags_en": ["#health", "#wellness", "#family", "#gulf"]},
    
    {"name": "managing-healthcare-costs-families", "cat": "health",
     "title_ar": "إدارة تكاليف الرعاية الصحية للعائلات", "title_en": "Managing Healthcare Costs for Families",
     "desc_ar": "دليل لإدارة تكاليف الرعاية الصحية للعائلات في الخليج.", "desc_en": "Guide to managing healthcare costs for families in the Gulf.",
     "tags_ar": ["#صحة", "#تكاليف", "#عائلة", "#تأمين"], "tags_en": ["#healthcare", "#costs", "#family", "#insurance"]},
    
    {"name": "preparing-for-pregnancy-guide", "cat": "health",
     "title_ar": "دليل الاستعداد للحمل", "title_en": "Preparing for Pregnancy Guide",
     "desc_ar": "دليل شامل للاستعداد للحمل — التغذية، الفحوصات، والنصائح.", "desc_en": "Complete guide to preparing for pregnancy — nutrition, tests, and tips.",
     "tags_ar": ["#حمل", "#صحة", "#أمومة", "#عائلة"], "tags_en": ["#pregnancy", "#health", "#motherhood", "#family"]},

    # === Travel / Islamic (3) ===
    {"name": "complete-family-travel-activities-hub", "cat": "travel",
     "title_ar": "دليل السفر والأنشطة العائلية الشامل", "title_en": "Complete Family Travel & Activities Hub",
     "desc_ar": "دليل شامل للسفر والأنشطة العائلية في الخليج والعالم.", "desc_en": "Complete guide to family travel and activities in the Gulf and beyond.",
     "tags_ar": ["#سفر", "#عائلة", "#أنشطة", "#خليج"], "tags_en": ["#travel", "#family", "#activities", "#gulf"]},
    
    {"name": "complete-islamic-lifestyle-guide", "cat": "islamic",
     "title_ar": "الدليل الإسلامي الشامل للحياة اليومية", "title_en": "Complete Islamic Lifestyle Guide",
     "desc_ar": "دليل شامل للحياة الإسلامية اليومية للعائلات في الخليج.", "desc_en": "Complete guide to daily Islamic lifestyle for Gulf families.",
     "tags_ar": ["#إسلام", "#عبادة", "#حياة", "#عائلة"], "tags_en": ["#islamic", "#worship", "#lifestyle", "#family"]},
    
    {"name": "family-friendly-activities-gulf-cities", "cat": "travel",
     "title_ar": "أنشطة عائلية في مدن الخليج", "title_en": "Family-Friendly Activities in Gulf Cities",
     "desc_ar": "دليل لأفضل الأنشطة العائلية في مدن الخليج الرئيسية.", "desc_en": "Guide to the best family-friendly activities in major Gulf cities.",
     "tags_ar": ["#أنشطة", "#عائلة", "#خليج", "#ترفيه"], "tags_en": ["#activities", "#family", "#gulf", "#fun"]},

    # === Holistic (1) ===
    {"name": "complete-gulf-family-financial-life-hub", "cat": "holistic",
     "title_ar": "محور الحياة المالية للعائلة الخليجية", "title_en": "Complete Gulf Family Financial Life Hub",
     "desc_ar": "مركز شامل لكل ما يتعلق بالحياة المالية للعائلة في الخليج.", "desc_en": "Comprehensive hub for everything related to Gulf family financial life.",
     "tags_ar": ["#مالية", "#عائلة", "#خليج", "#شامل"], "tags_en": ["#finance", "#family", "#gulf", "#comprehensive"]},

    # === Problematic (Type B) — 4 articles ===
    {"name": "emergency-fund-calculator-guide", "cat": "finance",
     "title_ar": "دليل صندوق الطوارئ المالي: احسب احتياجاتك", "title_en": "Emergency Fund Calculator Guide: Calculate Your Needs",
     "desc_ar": "دليل شامل لحساب صندوق الطوارئ المالي المناسب لعائلتك.", "desc_en": "Complete guide to calculating the right emergency fund for your family.",
     "tags_ar": ["#طوارئ", "#مالية", "#ادخار", "#عائلة"], "tags_en": ["#emergency", "#finance", "#savings", "#family"]},
    
    {"name": "family-budget-planning-guide", "cat": "finance",
     "title_ar": "دليل تخطيط الميزانية العائلية", "title_en": "Family Budget Planning Guide",
     "desc_ar": "دليل شامل لتخطيط وإدارة ميزانية الأسرة في الخليج.", "desc_en": "Complete guide to planning and managing family budget in the Gulf.",
     "tags_ar": ["#ميزانية", "#عائلة", "#تخطيط", "#مالية"], "tags_en": ["#budget", "#family", "#planning", "#finance"]},
    
    {"name": "house-affordability-single-income-guide", "cat": "realestate",
     "title_ar": "دليل شراء منزل بدخل واحد", "title_en": "House Affordability on a Single Income Guide",
     "desc_ar": "دليل لشراء منزل بدخل واحد في السعودية والخليج.", "desc_en": "Guide to buying a home on a single income in Saudi Arabia and the Gulf.",
     "tags_ar": ["#عقار", "#منزل", "#دخل-واحد", "#تمويل"], "tags_en": ["#realestate", "#home", "#single-income", "#mortgage"]},
    
    {"name": "umrah-packing-checklist-guide", "cat": "travel",
     "title_ar": "دليل حقيبة العمرة: قائمة التجهيزات", "title_en": "Umrah Packing Checklist Guide: What to Bring",
     "desc_ar": "قائمة شاملة لتجهيزات حقيبة العمرة للعائلات.", "desc_en": "Complete Umrah packing checklist for families.",
     "tags_ar": ["#عمرة", "#سفر", "#تجهيزات", "#عائلة"], "tags_en": ["#umrah", "#travel", "#packing", "#family"]},
]


# ─── Helper: tag-aware content filtering ──────────────────
HAS_ARABIC = re.compile(r'[؀-ۿ]')

def filter_by_language(body, keep_arabic=True):
    """Keep only Arabic or English text segments using tag-aware splitting.
    Preserves all heading tags (h1-h6) regardless of language.
    For other text content, applies language filtering based on the keep_arabic flag.
    """
    # First, protect all heading content by replacing with placeholders
    headings = []
    def protect_heading(m):
        idx = len(headings)
        full_tag = m.group(0)
        tag_name = m.group(1)
        # Find the tag content (between > and <)
        content_start = full_tag.find('>') + 1
        content_end = full_tag.rfind('<')
        content = full_tag[content_start:content_end]
        tag_open = full_tag[:content_start]
        tag_close = full_tag[content_end:]
        headings.append((tag_open, content, tag_close))
        return f'__HEADING_{idx}__'

    body_protected = re.sub(r'<(h[1-6])[^>]*>.*?</\1>', protect_heading, body, flags=re.DOTALL)

    segments = re.split(r'(<[^>]*>)', body_protected)
    result = []
    for seg in segments:
        if seg.startswith('__HEADING_'):
            hidx = re.search(r'__HEADING_(\d+)__', seg)
            if hidx:
                idx = int(hidx.group(1))
                h_open, h_content, h_close = headings[idx]
                if keep_arabic:
                    ar_match = re.search(r'<span class="ar">(.*?)</span>', h_content)
                    if ar_match:
                        h_content = ar_match.group(1)
                else:
                    en_match = re.search(r'<span class="en">(.*?)</span>', h_content)
                    if en_match:
                        h_content = en_match.group(1)
                result.append(f'{h_open}{h_content}{h_close}')
        elif seg.startswith('<') and seg.endswith('>'):
            result.append(seg)
        else:
            text = seg
            if keep_arabic:
                if HAS_ARABIC.search(text):
                    result.append(text)
                else:
                    en_chars = len(re.findall(r'[a-zA-Z]', text))
                    if en_chars <= 15:
                        result.append(text)
            else:
                if HAS_ARABIC.search(text):
                    ar_ratio = len(re.findall(r'[؀-ۿ]', text)) / max(len(text.strip()), 1)
                    if ar_ratio < 0.7:
                        result.append(text)
                else:
                    result.append(text)
    filtered = ''.join(result)
    filtered = re.sub(r'<p>\s*</p>', '', filtered)
    filtered = re.sub(r'<li>\s*</li>', '', filtered)
    filtered = re.sub(r'<span>\s*</span>', '', filtered)
    return filtered


def extract_en_from_bilingual(body):
    """Extract English from bilingual spans if present."""
    if '<span class="en">' not in body:
        return None
    cleaned = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">.*?</span>', r'\1', body, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="ar">(.*?)</span>\s*<span class="en">(.*?)</span>', r'\2', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="ar">.*?</span>', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="en">(.*?)</span>', r'\1', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<p>\s*</p>', '', cleaned)
    return cleaned


def get_h2_toc(body):
    """Extract h2 headings and generate ids."""
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


def add_ids_to_h2(body, toc_items):
    """Add id attributes to h2 headings."""
    for htext, hid in toc_items:
        for space1 in ['', ' ']:
            for space2 in ['', ' ']:
                pat = f'<h2>{space1}{htext}{space2}</h2>'
                if pat in body:
                    body = body.replace(pat, f'<h2 id="{hid}">{htext}</h2>', 1)
                    break
            else:
                continue
            break
    return body


def build_article_html(body_cleaned, config, lang='ar'):
    """Wrap cleaned body in full BOOM-compliant HTML structure."""
    k = lang  # 'ar' or 'en'
    cat = config.get('cat', 'finance')
    cat_cfg = CATEGORY_CONFIG.get(cat, CATEGORY_CONFIG['finance'])
    
    # Get TOC items
    toc_items = get_h2_toc(body_cleaned)
    body_cleaned = add_ids_to_h2(body_cleaned, toc_items)
    
    # Get config values
    title = config[f"title_{k}"]
    desc = config[f"desc_{k}"]
    tags = config.get(f"tags_{k}", [])
    cta = cat_cfg.get(f"cta_{k}", CATEGORY_CONFIG['finance'][f"cta_{k}"])
    tools = cat_cfg.get(f"tools_{k}", CATEGORY_CONFIG['finance'][f"tools_{k}"])
    
    # Read-also links (cross-link between articles in same category)
    read_items = config.get(f"read_{k}", [])
    
    # ── Build sidebar HTML ──
    toc_links = '\n'.join(f'  <a href="#{hid}" class="toc-item">{htext}</a>' for htext, hid in toc_items)
    tools_html = '\n'.join(f'  <a href="{link}" class="tool-btn">{t}</a>' for t, link in tools)
    
    imgs = [
        "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=64&h=48&q=80",
        "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=64&h=48&q=80",
        "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=64&h=48&q=80",
    ]
    related_html = ""
    for i, (rtitle, rlink) in enumerate(read_items[:3]):
        related_html += f"""  <div class="sidebar-related-item">
    <img src="{imgs[i % 3]}" alt="" width="64" height="48" loading="lazy">
    <div>
      <div class="related-title"><a href="{rlink}">{rtitle}</a></div>
    </div>
  </div>
"""
    
    team_name = "فريق دوت فور لايف" if k == "ar" else "DOTFORLIFE Team"
    team_trust = "محتوى موثوق، بعناية للعائلات الخليجية." if k == "ar" else "Trusted content for Gulf families."
    team_link = "معاييرنا التحريرية ←" if k == "ar" else "Our Editorial Standards →"
    toc_heading = "📑 المحتويات" if k == "ar" else "📑 Contents"
    related_heading = "ذات صلة" if k == "ar" else "Related"
    tools_heading = "🛠 أدوات" if k == "ar" else "🛠 Tools"

    sidebar = f"""<aside class="article-sidebar">
<div class="sidebar-module sidebar-team-card">
  <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="56" height="56" loading="lazy">
  <div class="team-name">{team_name}</div>
  <div class="team-trust">{team_trust}</div>
  <a href="/editorial-standards.html" class="team-link">{team_link}</a>
</div>

<div class="sidebar-module sidebar-toc">
  <h4>{toc_heading}</h4>
{toc_links}
</div>

<div class="sidebar-module sidebar-related">
  <h4>{related_heading}</h4>
{related_html}</div>

<div class="sidebar-module sidebar-tools">
  <h4>{tools_heading}</h4>
{tools_html}
</div>
</aside>"""
    
    # ── Build article-end ──
    read_heading = "📖 اقرأ أيضاً" if k == "ar" else "📖 Read Also"
    fri_title = "📬 نصائح الجمعة العائلية" if k == "ar" else "📬 Friday Family Tips"
    fri_alert = "🚧 قريباً — تكامل التسجيل." if k == "ar" else "🚧 Coming soon — integration."
    fri_sub = "اشترك" if k == "ar" else "Subscribe"
    
    read_cards = ""
    for rtitle, rlink in read_items:
        read_cards += f"""    <a href="{rlink}" class="read-also-card">
      <span class="read-also-title">{rtitle}</span>
    </a>
"""
    
    tag_items = '\n  '.join(f'<span class="tag">{t}</span>' for t in tags)
    
    article_end = f"""<div class="article-end">
<div class="article-share">
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
</div>

<div class="article-tool-cta">
  <h3>{cta['title']}</h3>
  <p>{cta['desc']}</p>
  <a href="{cta['link']}" class="tool-cta-btn">{cta['btn']}</a>
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
    <input type="email" placeholder="your@email.com" aria-label="Email">
    <button onclick="alert('{fri_alert}')">{fri_sub}</button>
  </div>
</div>

<div class="article-tags">
  {tag_items}
</div>
</div>"""
    
    # ── Assemble final HTML ──
    # The full HTML is built from scratch using template parts
    # We keep the head/scripts from the original .html file
    
    final = f"""<!DOCTYPE html>
<html lang="{('ar' if k == 'ar' else 'en')}" dir="{('rtl' if k == 'ar' else 'ltr')}" data-lang="{k}" data-theme="light">
<head>
<script>(function(){{var h=document.documentElement,t=localStorage.getItem("dfl-theme")||"light";h.setAttribute("data-lang","{k}");h.setAttribute("lang","{('ar' if k == 'ar' else 'en')}");h.setAttribute("dir","{('rtl' if k == 'ar' else 'ltr')}");h.setAttribute("data-theme",t);}})()</script>
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="https://dotforlife.com/blog/{config['name']}{'-en' if k == 'en' else ''}.html" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://dotforlife.com/blog/{config['name']}{'-en' if k == 'en' else ''}.html" />
  <meta property="og:type" content="article" />
  <link rel="alternate" hreflang="ar" href="https://dotforlife.com/blog/{config['name']}.html" />
  <link rel="alternate" hreflang="en" href="https://dotforlife.com/blog/{config['name']}-en.html" />
  <meta property="og:image" content="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&h=420&q=85" />
  <style>
:root{{--green:#054241;--teal:#6abfb8;--orange:#fd781c;--cream:#FAF8F4;--text:#1a1d23;--text2:#6C757D;--radius:16px;--max-w:1100px}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Almarai','Segoe UI',sans-serif;background:var(--cream);color:var(--text);line-height:1.9;padding:0}}
img{{max-width:100%;height:auto}}
  </style>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Almarai:wght@300;400;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles/global.css?v=20260617c">
  <link rel="stylesheet" href="/styles/home.css?v=20260617b">
  <link rel="stylesheet" href="/styles/pages/articles.css?v=20260617a">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G1XPV4F0G"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-3G1XPV4F0G');</script>
</head>
<body data-template="article">

<div id="reading-progress" role="progressbar" aria-label="Reading progress"></div>

<nav id="navbar"><div class="nav-inner"><a href="/" class="nav-logo"><img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" width="100" height="100" style="height:100px;width:auto;object-fit:contain;" loading="lazy"></a><ul class="nav-links">
    <li><a href="/health.html">{"الصحة" if k == 'ar' else 'Health'}</a></li>
    <li><a href="/finance.html">{"المالية" if k == 'ar' else 'Finance'}</a></li>
    <li><a href="/real-estate.html">{"العقار" if k == 'ar' else 'Real Estate'}</a></li>
    <li><a href="/travel.html">{"السفر" if k == 'ar' else 'Travel'}</a></li>
    <li><a href="/islamic.html">{"الإسلامية" if k == 'ar' else 'Islamic'}</a></li>
    <li><a href="/about.html">{"عنّا" if k == 'ar' else 'About'}</a></li>
    <li><a href="/archive.html">{"الأرشيف" if k == 'ar' else 'Archive'}</a></li>
    <li><a href="/blog.html">{"المدونة" if k == 'ar' else 'Blog'}</a></li>
    <li><a href="/library.html">{"المكتبة" if k == 'ar' else 'Library'}</a></li>
  </ul><div class="nav-controls"><button class="nav-btn" id="lang-toggle">{"English" if k == 'ar' else 'العربية'}</button><button class="nav-btn" id="theme-toggle">
      <svg class="theme-icon-moon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      <svg class="theme-icon-sun" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
    </button></div></div></nav>

<div class="article-wrap">

<section class="article-banner" aria-label="Article banner">
  <div class="article-banner-img-wrap">
    <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&h=420&q=85" alt="" class="article-banner-img" width="1200" height="420" loading="eager" fetchpriority="high">
    <div class="article-banner-overlay">
      <h1 class="article-banner-title">{title}</h1>
      <div class="article-banner-meta">
        <span>2026-06-08</span>
        <span>{"٨ دقائق" if k == 'ar' else '8 min read'}</span>
      </div>
    </div>
  </div>
</section>

<div class="article-layout" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:2.5rem">

<main class="article-main">
<article class="article-body">
{body_cleaned}
</article>
{article_end}
</main>

{sidebar}

</div><!-- /article-layout -->

</div><!-- /article-wrap -->

<footer class="site-footer" role="contentinfo">
  <div class="footer-inner">
    <div class="footer-top">
      <div class="footer-brand">
        <a href="/" class="footer-logo" aria-label="DOTFORLIFE">
          <img src="/assets/images/logo1-footer.webp" alt="DOTFORLIFE" loading="lazy">
        </a>
        <p>{"مساحة هادئة واحدة لاحتياجات عائلتك اليومية. مجاني، دائماً." if k == 'ar' else 'One quiet space for your family\'s daily needs. Free, always.'}</p>
      </div>
      <div class="footer-cols">
        <div class="footer-col">
          <h4>{"الأقسام" if k == 'ar' else 'Sections'}</h4>
          <ul>
            <li><a href="/health.html">{"الصحة" if k == 'ar' else 'Health'}</a></li>
            <li><a href="/finance.html">{"المالية" if k == 'ar' else 'Finance'}</a></li>
            <li><a href="/real-estate.html">{"العقار" if k == 'ar' else 'Real Estate'}</a></li>
            <li><a href="/travel.html">{"السفر" if k == 'ar' else 'Travel'}</a></li>
            <li><a href="/islamic.html">{"الإسلامية" if k == 'ar' else 'Islamic'}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>{"الأدوات" if k == 'ar' else 'Tools'}</h4>
          <ul>
            <li><a href="/tools/water-calculator.html">{"حاسبة الماء" if k == 'ar' else 'Water Calculator'}</a></li>
            <li><a href="/tools/bmi-calculator.html">{"حاسبة BMI" if k == 'ar' else 'BMI Calculator'}</a></li>
            <li><a href="/tools/body-fat-calculator.html">{"حاسبة الدهون" if k == 'ar' else 'Body Fat Calculator'}</a></li>
            <li><a href="/tools/calorie-calculator.html">{"حاسبة السعرات" if k == 'ar' else 'Calorie Calculator'}</a></li>
            <li><a href="/tools/hijri-converter.html">{"محوّل التاريخ" if k == 'ar' else 'Hijri Converter'}</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>{"الشركة" if k == 'ar' else 'Company'}</h4>
          <ul>
            <li><a href="/about.html">{"عنّا" if k == 'ar' else 'About'}</a></li>
            <li><a href="/blog.html">{"المدونة" if k == 'ar' else 'Blog'}</a></li>
            <li><a href="/contact.html">{"اتصل بنا" if k == 'ar' else 'Contact'}</a></li>
            <li><a href="/privacy.html">{"الخصوصية" if k == 'ar' else 'Privacy'}</a></li>
            <li><a href="/terms.html">{"الشروط" if k == 'ar' else 'Terms'}</a></li>
          </ul>
        </div>
      </div>
    </div>
    <hr class="footer-divider">
    <div class="footer-bottom">
      <span>{"© 2026 DOTFORLIFE — مجاني للعائلات، دائماً." if k == 'ar' else '© 2026 DOTFORLIFE — Free for families, always.'}</span>
      <div class="footer-bottom-links">
        <a href="/privacy.html">{"الخصوصية" if k == 'ar' else 'Privacy'}</a>
        <a href="/terms.html">{"الشروط" if k == 'ar' else 'Terms'}</a>
      </div>
    </div>
  </div>
</footer>

<script src="/scripts/global.js?v=20260617a" defer></script>
<script>
(function(){{
  var bar = document.getElementById('reading-progress');
  if(bar){{
    window.addEventListener('scroll',function(){{
      var h = document.documentElement;
      var total = h.scrollHeight - h.clientHeight;
      var pct = (h.scrollTop || document.body.scrollTop) / (total || 1) * 100;
      bar.style.width = pct + '%';
    }},{{passive:true}});
  }}
  var tocLinks = document.querySelectorAll('.toc-item');
  if(tocLinks.length){{
    var headings = [];
    tocLinks.forEach(function(link){{
      var id = link.getAttribute('href').replace('#','');
      var el = document.getElementById(id);
      if(el) headings.push({{el:el,link:link}});
    }});
    window.addEventListener('scroll',function(){{
      var scrollY = window.scrollY + 130;
      var current = null;
      headings.forEach(function(h){{
        if(h.el.offsetTop <= scrollY) current = h;
      }});
      tocLinks.forEach(function(l){{ l.classList.remove('is-active'); }});
      if(current) current.link.classList.add('is-active');
    }},{{passive:true}});
  }}
}})();
</script>
</body>
</html>"""
    
    return final


def create_redirect_html(target_url):
    """Create a simple redirect HTML page."""
    name = target_url.rstrip('.html').split('/')[-1]
    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url={target_url}">
<meta name="robots" content="noindex">
<title>تم النقل | Redirecting...</title>
</head>
<body>
<p>تم نقل هذه الصفحة إلى <a href="{target_url}">{name}</a>.</p>
</body>
</html>"""


def balance_divs(html):
    """Add missing closing divs or strip extra closing divs to balance div count."""
    opens = len(re.findall(r'<div\b', html))
    closes = len(re.findall(r'</div>', html))
    diff = opens - closes
    if diff > 0:
        # Add missing closing divs
        html += '\n' + '</div>\n' * diff
    elif diff < 0:
        # Remove extra closing divs from end (harder, but we can strip from end)
        for _ in range(-diff):
            # Find last </div> and remove it
            last = html.rfind('</div>')
            if last >= 0:
                html = html[:last] + html[last+6:]
    return html


def process_article(config):
    """Process a single article: create AR, EN, and redirect files."""
    name = config['name']
    main_path = f"{BLOG}/{name}.html"
    ar_path = f"{BLOG}/{name}-ar.html"
    en_path = f"{BLOG}/{name}-en.html"
    
    print(f"\n{'='*60}")
    print(f"📄 Processing: {name}")
    print(f"{'='*60}")
    
    # ─── Read source files ───
    if not os.path.exists(main_path) or not os.path.exists(ar_path):
        print(f"  ❌ Missing files: main={os.path.exists(main_path)}, ar={os.path.exists(ar_path)}")
        return False
    
    with open(main_path, 'r') as f:
        main_html = f.read()
    with open(ar_path, 'r') as f:
        ar_html = f.read()
    
    # ─── Extract Arabic body from -ar.html ───
    ar_body_match = re.search(r'<article class="article-body">(.*?)</article>', ar_html, re.DOTALL)
    if not ar_body_match:
        print(f"  ❌ No article-body in -ar.html")
        return False

    ar_body_raw = ar_body_match.group(1)

    # Check for bilingual spans in -ar.html body
    has_bilingual = '<span class="en">' in ar_body_raw and '<span class="ar">' in ar_body_raw
    if has_bilingual:
        # Type A: extract Arabic from bilingual spans
        ar_body = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">(.*?)</span>', r'\2', ar_body_raw, flags=re.DOTALL)
        ar_body = re.sub(r'<span class="ar">(.*?)</span>\s*<span class="en">(.*?)</span>', r'\1', ar_body, flags=re.DOTALL)
        ar_body = re.sub(r'<span class="en">.*?</span>', '', ar_body, flags=re.DOTALL)
        ar_body = re.sub(r'<span class="ar">(.*?)</span>', r'\1', ar_body, flags=re.DOTALL)
    else:
        # Type B: tag-aware content filtering to keep Arabic
        ar_body = filter_by_language(ar_body_raw, keep_arabic=True)

    # Strip old structural sections (we provide our own)
    ar_body = re.sub(r'<h2[^>]*>[^<]*Related Articles[^<]*</h2>\s*<div class="article-tools">.*?</div>\s*', '', ar_body, flags=re.DOTALL)
    ar_body = re.sub(r'<h2[^>]*>[^<]*مقالات وأدوات ذات صلة[^<]*</h2>\s*<div class="article-tools">.*?</div>\s*', '', ar_body, flags=re.DOTALL)
    ar_body = re.sub(r'<h2[^>]*>[^<]*Related[^<]*</h2>\s*<div class="article-tools">.*?</div>\s*', '', ar_body, flags=re.DOTALL)
    ar_body = re.sub(r'<div class="article-end">.*?</div>\s*', '', ar_body, flags=re.DOTALL)
    ar_body = re.sub(r'<div class="article-share">.*?</div>\s*', '', ar_body, flags=re.DOTALL)
    ar_body = re.sub(r'<aside class="article-sidebar">.*?</aside>\s*', '', ar_body, flags=re.DOTALL)
    ar_body = re.sub(r'<div class="article-tool-cta">.*?</div>\s*', '', ar_body, flags=re.DOTALL)
    ar_body = re.sub(r'<div class="article-tools">.*?</div>\s*', '', ar_body, flags=re.DOTALL)
    # Clean empty tags
    ar_body = re.sub(r'<p>\s*</p>', '', ar_body)
    ar_body = re.sub(r'<li>\s*</li>', '', ar_body)
    ar_body = re.sub(r'<span>\s*</span>', '', ar_body)

    # Balance divs in cleaned AR body
    ar_o_before = len(re.findall(r'<div\b', ar_body))
    ar_c_before = len(re.findall(r'</div>', ar_body))
    if ar_o_before != ar_c_before:
        ar_body = balance_divs(ar_body)
        ar_o_after = len(re.findall(r'<div\b', ar_body))
        ar_c_after = len(re.findall(r'</div>', ar_body))
        print(f"  ⚖️  AR body div balance: {ar_o_before}/{ar_c_before} → {ar_o_after}/{ar_c_after}")

    # ─── Extract English body from main .html ───
    en_body_match = re.search(r'<article class="article-body">(.*?)</article>', main_html, re.DOTALL)
    if not en_body_match:
        print(f"  ❌ No article-body in main .html")
        return False

    en_body_raw = en_body_match.group(1)

    # Check if main .html has bilingual spans in body
    if '<span class="en">' in en_body_raw and '<span class="ar">' in en_body_raw:
        en_body = extract_en_from_bilingual(en_body_raw)
        if en_body is None:
            en_body = en_body_raw
    else:
        en_body = en_body_raw

    # Strip old structural sections from EN body
    en_body = re.sub(r'<h2[^>]*>[^<]*Related Articles[^<]*</h2>\s*<div class="article-tools">.*?</div>\s*', '', en_body, flags=re.DOTALL)
    en_body = re.sub(r'<h2[^>]*>[^<]*مقالات وأدوات ذات صلة[^<]*</h2>\s*<div class="article-tools">.*?</div>\s*', '', en_body, flags=re.DOTALL)
    en_body = re.sub(r'<h2[^>]*>[^<]*Related[^<]*</h2>\s*<div class="article-tools">.*?</div>\s*', '', en_body, flags=re.DOTALL)
    en_body = re.sub(r'<div class="article-end">.*?</div>\s*', '', en_body, flags=re.DOTALL)
    en_body = re.sub(r'<div class="article-share">.*?</div>\s*', '', en_body, flags=re.DOTALL)
    en_body = re.sub(r'<aside class="article-sidebar">.*?</aside>\s*', '', en_body, flags=re.DOTALL)
    en_body = re.sub(r'<div class="article-tool-cta">.*?</div>\s*', '', en_body, flags=re.DOTALL)
    en_body = re.sub(r'<div class="article-tools">.*?</div>\s*', '', en_body, flags=re.DOTALL)
    en_body = re.sub(r'<p>\s*</p>', '', en_body)
    en_body = re.sub(r'<li>\s*</li>', '', en_body)
    en_body = re.sub(r'<span>\s*</span>', '', en_body)

    # Balance divs in cleaned EN body
    en_o_before = len(re.findall(r'<div\b', en_body))
    en_c_before = len(re.findall(r'</div>', en_body))
    if en_o_before != en_c_before:
        en_body = balance_divs(en_body)
        en_o_after = len(re.findall(r'<div\b', en_body))
        en_c_after = len(re.findall(r'</div>', en_body))
        print(f"  ⚖️  EN body div balance: {en_o_before}/{en_c_before} → {en_o_after}/{en_c_after}")

    # ─── Verify extracted content ───
    ar_text = re.sub(r'<[^>]+>', ' ', ar_body)
    ar_text = re.sub(r'\s+', ' ', ar_text)
    ar_ar = len(re.findall(r'[؀-ۿ]', ar_text))
    ar_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', ar_text))
    
    en_text = re.sub(r'<[^>]+>', ' ', en_body)
    en_text = re.sub(r'\s+', ' ', en_text)
    en_ar = len(re.findall(r'[؀-ۿ]', en_text))
    en_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', en_text))
    
    # Quality check
    if ar_ar < 200:
        print(f"  ⚠️  Low Arabic content in AR body: {ar_ar} chars — using EN body as fallback")
        ar_body = en_body
        # Re-check
        ar_text = re.sub(r'<[^>]+>', ' ', ar_body)
        ar_text = re.sub(r'\s+', ' ', ar_text)
        ar_ar = len(re.findall(r'[؀-ۿ]', ar_text))
        ar_en = len(re.findall(r'\b[a-zA-Z]{3,}\b', ar_text))
    if ar_en > 30:
        print(f"  ⚠️  Remaining English in AR body: {ar_en} words (acceptable if HTML attrs)")
    if en_en < 300:
        print(f"  ⚠️  Low English content in EN body: {en_en} words")
    
    print(f"  AR body: {ar_ar} AR chars, {ar_en} EN words")
    print(f"  EN body: {en_ar} AR chars, {en_en} EN words")
    
    # ─── Add read-also links from config (cross-link within same category) ───
    # Generate related article links
    cat = config['cat']
    same_cat = [a for a in ARTICLES if a['cat'] == cat and a['name'] != name]
    read_ar = []
    read_en = []
    for a in same_cat[:3]:
        read_ar.append((a['title_ar'], f"/blog/{a['name']}.html"))
        read_en.append((a['title_en'], f"/blog/{a['name']}-en.html"))
    
    config['read_ar'] = read_ar
    config['read_en'] = read_en
    
    # ─── Build final HTML files ───
    # AR version → .html
    ar_final = build_article_html(ar_body, config, 'ar')
    
    # EN version → -en.html
    try:
        en_final = build_article_html(en_body, config, 'en')
    except Exception as e:
        print(f"  ❌ EN build failed: {e}")
        return False
    
    # Redirect → -ar.html
    redirect = create_redirect_html(f"/blog/{name}.html")
    
    # ─── Write files ───
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(ar_final)
    print(f"  ✅ {name}.html (AR version)")
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(en_final)
    print(f"  ✅ {name}-en.html (EN version)")
    
    with open(ar_path, 'w', encoding='utf-8') as f:
        f.write(redirect)
    print(f"  ✅ {name}-ar.html (redirect)")
    
    # ─── Verify ───
    missing = []
    for p, desc in [(main_path, "AR"), (en_path, "EN"), (ar_path, "redirect")]:
        if not os.path.exists(p):
            missing.append(desc)
    
    if missing:
        print(f"  ❌ Missing files: {missing}")
        return False
    
    # Quick structural check on AR version
    with open(main_path, 'r') as f:
        check = f.read()
    
    errors = []
    if 'article-layout' not in check:
        errors.append("no article-layout")
    if 'article-sidebar' not in check:
        errors.append("no sidebar")
    if 'toc-item' not in check:
        errors.append("no TOC")
    if 'article-tool-cta' not in check:
        errors.append("no CTA")
    if 'display:grid' not in check:
        errors.append("no inline grid")
    
    div_open = len(re.findall(r'<div\b', check))
    div_close = len(re.findall(r'</div>', check))
    if div_open != div_close:
        errors.append(f"div imbalance ({div_open}/{div_close})")
    
    main_o = len(re.findall(r'<main\b', check))
    main_c = len(re.findall(r'</main>', check))
    aside_o = len(re.findall(r'<aside\b', check))
    aside_c = len(re.findall(r'</aside>', check))
    if main_o != main_c:
        errors.append(f"main imbalance ({main_o}/{main_c})")
    if aside_o != aside_c:
        errors.append(f"aside imbalance ({aside_o}/{aside_c})")
    
    if errors:
        print(f"  ❌ Structural errors: {', '.join(errors)}")
        return False
    else:
        print(f"  ✅ Structure verified (div={div_open}/{div_close}, main={main_o}/{main_c}, aside={aside_o}/{aside_c})")
        return True


if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] if len(sys.argv) > 1 else [a['name'] for a in ARTICLES]
    
    success = 0
    fail = 0
    
    for config in ARTICLES:
        if config['name'] in targets:
            if process_article(config):
                success += 1
            else:
                fail += 1
    
    print(f"\n{'='*60}")
    print(f"Batch 5 Complete: {success} succeeded, {fail} failed out of {success+fail}")
    print(f"{'='*60}")
