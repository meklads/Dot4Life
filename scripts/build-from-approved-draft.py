#!/usr/bin/env python3
"""
TECH_BUILD: Inject approved Markdown drafts into live finance-wealth article shells.
Preserves URL/canonical; backs up before write. Adds Article + FAQPage JSON-LD.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

from image_manifest import assert_g5_image, article_slug_from_path, is_approved, lookup, resolve_hero_for_build

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "operating-system" / "reports" / "drafts"
BACKUP = ROOT / "outputs" / "backups" / "tech-build"

BUILD_MAP = [
    {
        "id": "A-01-1",
        "draft_ar": DRAFTS / "task01/investment-basics-beginners.md",
        "draft_en": DRAFTS / "task01/investment-basics-beginners-en.md",
        "out_ar": ROOT / "finance-wealth/investment-basics-beginners.html",
        "out_en": ROOT / "finance-wealth/investment-basics-beginners-en.html",
        "section_ar": "💰 مالية وثروة",
        "section_en": "💰 Finance & Wealth",
        "tool_cta_ar": "/tools/monthly-budget.html",
        "tool_cta_en": "/tools/monthly-budget.html",
        "tool_label_ar": "حاسبة الميزانية الشهرية",
        "tool_label_en": "Monthly Budget Calculator",
        "internal_links_ar": [
            ("/finance-wealth/family-budget-plan.html", "ميزانية الأسرة الخليجية: توزيع الراتب بذكاء"),
            ("/comparisons/saving-vs-investing-gulf-family.html", "الادخار أم الاستثمار لأسرة خليجية؟"),
            ("/comparisons/gold-vs-real-estate-gulf-family.html", "الاستثمار في الذهب أم العقار؟"),
        ],
        "internal_links_en": [
            ("/finance-wealth/family-budget-plan-en.html", "Gulf Family Budget: Smart Salary Split"),
            ("/comparisons/saving-vs-investing-gulf-family-en.html", "Saving vs Investing for Gulf Families"),
            ("/comparisons/gold-vs-real-estate-gulf-family-en.html", "Gold vs Property for Gulf Families"),
        ],
        "hero_webp": "/assets/images/hero-investment-basics-beginners.webp",
        "hero_alt_ar": "رسم توضيحي لادخار واستثمار لأسرة خليجية، جرة عملات ونبتة تنمو",
        "hero_alt_en": "Illustration of saving and investing for Gulf families, coins jar and growing plant",
        "title_seo_ar": "استثمار المبتدئ الخليجي: دليل عملي",
        "title_seo_en": "Gulf Beginner Investing Guide",
    },
    {
        "id": "A-01-2",
        "draft_ar": DRAFTS / "task01/family-budget-plan.md",
        "draft_en": DRAFTS / "task01/family-budget-plan-en.md",
        "out_ar": ROOT / "finance-wealth/family-budget-plan.html",
        "out_en": ROOT / "finance-wealth/family-budget-plan-en.html",
        "section_ar": "💰 مالية وثروة",
        "section_en": "💰 Finance & Wealth",
        "tool_cta_ar": "/tools/monthly-budget.html",
        "tool_cta_en": "/tools/monthly-budget.html",
        "tool_label_ar": "حاسبة الميزانية الشهرية",
        "tool_label_en": "Monthly Budget Calculator",
        "internal_links_ar": [
            ("/finance-wealth/investment-basics-beginners.html", "أساسيات الاستثمار للمبتدئين"),
            ("/tools/savings-calculator.html", "حاسبة الادخار"),
            ("/finance.html", "قسم المالية"),
        ],
        "internal_links_en": [
            ("/finance-wealth/investment-basics-beginners-en.html", "Investment Basics for Beginners"),
            ("/tools/savings-calculator.html", "Savings Calculator"),
            ("/finance.html", "Finance Hub"),
        ],
        "hero_webp": "/assets/images/hero-family-budget-plan.webp",
        "hero_alt_ar": "رسم توضيحي لميزانية الأسرة الخليجية، محفظة ودفتر ميزانية",
        "hero_alt_en": "Illustration of Gulf family budgeting, wallet and budget notebook",
        "title_seo_ar": "ميزانية الأسرة الخليجية: خطة عملية",
        "title_seo_en": "Gulf Family Budget Guide",
    },
    {
        "id": "A-07-1",
        "draft_ar": DRAFTS / "task07/rent-vs-buy-gulf-family.md",
        "draft_en": DRAFTS / "task07/rent-vs-buy-gulf-family-en.md",
        "out_ar": ROOT / "real-estate/rent-vs-buy-gulf-family.html",
        "out_en": ROOT / "real-estate/rent-vs-buy-gulf-family-en.html",
        "section_ar": "🏠 عقار",
        "section_en": "🏠 Real Estate",
        "tool_cta_ar": "/tools/mortgage-calculator.html",
        "tool_cta_en": "/tools/mortgage-calculator.html",
        "tool_label_ar": "حاسبة الرهن العقاري",
        "tool_label_en": "Mortgage Calculator",
        "internal_links_ar": [
            ("/finance-wealth/family-budget-plan.html", "ميزانية الأسرة الخليجية"),
            ("/blog/emergency-fund-calculator-guide.html", "دليل صندوق الطوارئ"),
            ("/finance-wealth/investment-basics-beginners.html", "أساسيات الاستثمار للمبتدئين"),
        ],
        "internal_links_en": [
            ("/finance-wealth/family-budget-plan-en.html", "Gulf Family Budget Guide"),
            ("/blog/emergency-fund-calculator-guide-en.html", "Emergency Fund Guide"),
            ("/finance-wealth/investment-basics-beginners-en.html", "Investment Basics for Beginners"),
        ],
        "hero_webp": "/assets/images/hero-rent-vs-buy-gulf-family.webp",
        "hero_alt_ar": "رسم توضيحي لمقارنة الإيجار والتملك لأسرة خليجية، منزل ومفتاح",
        "hero_alt_en": "Illustration comparing rent vs buy for Gulf families, home and key",
        "title_seo_ar": "إيجار أم تملّك للأسرة الخليجية؟",
        "title_seo_en": "Rent vs Buy for Gulf Families",
    },
    {
        "id": "A-02-1",
        "draft_ar": DRAFTS / "task02/daily-walking-benefits.md",
        "draft_en": DRAFTS / "task02/daily-walking-benefits-en.md",
        "out_ar": ROOT / "health/daily-walking-benefits.html",
        "out_en": ROOT / "health/daily-walking-benefits-en.html",
        "section_ar": "🏥 صحة",
        "section_en": "🏥 Health",
        "tool_cta_ar": "/tools/bmi-calculator.html",
        "tool_cta_en": "/tools/bmi-calculator.html",
        "tool_label_ar": "حاسبة مؤشر كتلة الجسم",
        "tool_label_en": "BMI Calculator",
        "internal_links_ar": [
            ("/health/bmi-calculator-women.html", "حاسبة BMI للنساء"),
            ("/health/children-sleep-summer.html", "نوم الأطفال في الصيف"),
            ("/health.html", "قسم الصحة"),
        ],
        "internal_links_en": [
            ("/health/bmi-calculator-women.html", "BMI Calculator for Women"),
            ("/health/children-sleep-summer-en.html", "Children's Sleep in Summer"),
            ("/health.html", "Health Hub"),
        ],
        "hero_webp": "/assets/images/hero-daily-walking-benefits.webp",
        "hero_alt_ar": "عائلة تمشي في ممشى، نشاط يومي صحي في الخليج",
        "hero_alt_en": "Family walking on a path, daily healthy activity in the Gulf",
        "title_seo_ar": "فوائد المشي اليومي للعائلة",
        "title_seo_en": "Daily Walking Benefits for Families",
    },
    {
        "id": "A-02-2",
        "lang_only": "en",
        "draft_en": DRAFTS / "task02/bmi-calculator-women.md",
        "out_en": ROOT / "health/bmi-calculator-women.html",
        "section_en": "🏥 Health",
        "tool_cta_en": "/tools/bmi-calculator.html",
        "tool_label_en": "BMI Calculator",
        "internal_links_en": [
            ("/health/daily-walking-benefits-en.html", "Daily Walking Benefits"),
            ("/tools/body-fat-calculator.html", "Body Fat Calculator"),
            ("/health.html", "Health Hub"),
        ],
        "hero_webp": "/assets/images/hero-bmi-calculator-women.webp",
        "hero_alt_en": "Bathroom scale and measuring tape, women's health screening",
        "title_seo_en": "BMI Calculator for Women Guide",
    },
    {
        "id": "A-03-1",
        "draft_ar": DRAFTS / "task03/children-sleep-summer.md",
        "draft_en": DRAFTS / "task03/children-sleep-summer-en.md",
        "out_ar": ROOT / "health/children-sleep-summer.html",
        "out_en": ROOT / "health/children-sleep-summer-en.html",
        "section_ar": "🏥 صحة",
        "section_en": "🏥 Health",
        "tool_cta_ar": "/tools/water-calculator.html",
        "tool_cta_en": "/tools/water-calculator.html",
        "tool_label_ar": "حاسبة شرب الماء",
        "tool_label_en": "Water Intake Calculator",
        "internal_links_ar": [
            ("/health/daily-walking-benefits.html", "فوائد المشي اليومي"),
            ("/health-pregnancy/preconception-checkups.html", "فحوصات قبل الحمل"),
            ("/health.html", "قسم الصحة"),
        ],
        "internal_links_en": [
            ("/health/daily-walking-benefits-en.html", "Daily Walking Benefits"),
            ("/health-pregnancy/preconception-checkups-en.html", "Preconception Checkups"),
            ("/health.html", "Health Hub"),
        ],
        "hero_webp": "/assets/images/hero-children-sleep-summer.webp",
        "hero_alt_ar": "غرفة نوم أطفال هادئة، روتين نوم صحي في الصيف",
        "hero_alt_en": "Calm children's bedroom, healthy summer sleep routine",
        "title_seo_ar": "نوم الأطفال في الإجازة الصيفية",
        "title_seo_en": "Children's Sleep in Summer Break",
    },
    {
        "id": "A-03-2",
        "draft_ar": DRAFTS / "task03/pregnancy-week-by-week-ar.md",
        "draft_en": DRAFTS / "task03/pregnancy-week-by-week.md",
        "out_ar": ROOT / "health/pregnancy-week-by-week.html",
        "out_en": ROOT / "health/pregnancy-week-by-week-en.html",
        "section_ar": "🏥 صحة",
        "section_en": "🏥 Health",
        "tool_cta_ar": "/tools/pregnancy-calculator.html",
        "tool_cta_en": "/tools/pregnancy-calculator.html",
        "tool_label_ar": "حاسبة الحمل",
        "tool_label_en": "Pregnancy Due Date Calculator",
        "internal_links_ar": [
            ("/health-pregnancy/preconception-checkups.html", "فحوصات قبل الحمل"),
            ("/pregnancy-journey.html", "رحلة الحمل"),
            ("/health.html", "قسم الصحة"),
        ],
        "internal_links_en": [
            ("/health-pregnancy/preconception-checkups-en.html", "Preconception Checkups"),
            ("/pregnancy-journey.html", "Pregnancy Journey Hub"),
            ("/health.html", "Health Hub"),
        ],
        "hero_webp": "/assets/images/approved/hero-pregnancy-week-by-week.webp",
        "hero_alt_ar": "حذاء طفل صغير وبطانية ناعمة ودليل حمل على طاولة بإضاءة دافئة",
        "hero_alt_en": "Tiny baby booties, a soft blanket and a pregnancy guide on a warm table",
        "title_seo_ar": "الحمل أسبوعاً بأسبوع",
        "title_seo_en": "Pregnancy Week by Week Guide",
    },
    {
        "id": "A-04-1",
        "draft_ar": DRAFTS / "task04/preconception-checkups.md",
        "draft_en": DRAFTS / "task04/preconception-checkups-en.md",
        "out_ar": ROOT / "health-pregnancy/preconception-checkups.html",
        "out_en": ROOT / "health-pregnancy/preconception-checkups-en.html",
        "section_ar": "🤰 صحة الحمل",
        "section_en": "🤰 Pregnancy Health",
        "tool_cta_ar": "/tools/pregnancy-calculator.html",
        "tool_cta_en": "/tools/pregnancy-calculator.html",
        "tool_label_ar": "حاسبة الحمل",
        "tool_label_en": "Pregnancy Calculator",
        "internal_links_ar": [
            ("/health/pregnancy-week-by-week.html", "الحمل أسبوعاً بأسبوع"),
            ("/pregnancy-journey.html", "رحلة الحمل"),
            ("/health.html", "قسم الصحة"),
        ],
        "internal_links_en": [
            ("/health/pregnancy-week-by-week.html", "Pregnancy Week by Week"),
            ("/pregnancy-journey.html", "Pregnancy Journey"),
            ("/health.html", "Health Hub"),
        ],
        "hero_webp": "/assets/images/hero-preconception-checkups.webp",
        "hero_alt_ar": "فحوصات طبية قبل الحمل، دليل الأم الخليجية",
        "hero_alt_en": "Preconception medical checkup guide for mothers",
        "title_seo_ar": "فحوصات ضرورية قبل الحمل",
        "title_seo_en": "Essential Tests Before Pregnancy",
    },
    {
        "id": "A-04-2",
        "draft_ar": DRAFTS / "task04/daily-adhkar-family-guide.md",
        "draft_en": DRAFTS / "task04/daily-adhkar-family-guide-en.md",
        "out_ar": ROOT / "islamic-hajj-umrah/daily-adhkar-family-guide.html",
        "out_en": ROOT / "islamic-hajj-umrah/daily-adhkar-family-guide-en.html",
        "section_ar": "🕌 إسلامي",
        "section_en": "🕌 Islamic",
        "tool_cta_ar": "/islamic.html",
        "tool_cta_en": "/islamic.html",
        "tool_label_ar": "قسم الإسلام",
        "tool_label_en": "Islamic Hub",
        "internal_links_ar": [
            ("/islamic-hajj-umrah/teaching-children-allah-names.html", "تعليم أسماء الله للأطفال"),
            ("/islamic-hajj-umrah/teaching-children-prayer-with-love.html", "تعليم الصلاة بالحب"),
            ("/islamic.html", "قسم الإسلام"),
        ],
        "internal_links_en": [
            ("/islamic-hajj-umrah/teaching-children-allah-names-en.html", "Allah's Names for Children"),
            ("/islamic-hajj-umrah/teaching-children-prayer-with-love-en.html", "Teaching Prayer With Love"),
            ("/islamic.html", "Islamic Hub"),
        ],
        "hero_webp": "/assets/images/hero-daily-adhkar-family-guide.webp",
        "hero_alt_ar": "سبحة ومصحف على سطح دافئ، أذكار صباح ومساء",
        "hero_alt_en": "Prayer beads and Quran on warm surface, morning adhkar",
        "title_seo_ar": "أذكار الصباح والمساء للأسرة",
        "title_seo_en": "Morning and Evening Adhkar Guide",
    },
    {
        "id": "A-05-1",
        "draft_ar": DRAFTS / "task05/umrah-with-kids.md",
        "draft_en": DRAFTS / "task05/umrah-with-kids-en.md",
        "out_ar": ROOT / "islamic-hajj-umrah/umrah-with-kids.html",
        "out_en": ROOT / "islamic-hajj-umrah/umrah-with-kids-en.html",
        "section_ar": "🕌 إسلامي",
        "section_en": "🕌 Islamic",
        "tool_cta_ar": "/islamic.html",
        "tool_cta_en": "/islamic.html",
        "tool_label_ar": "قسم الإسلام",
        "tool_label_en": "Islamic Hub",
        "internal_links_ar": [
            ("/islamic-hajj-umrah/daily-adhkar-family-guide.html", "أذكار الأسرة اليومية"),
            ("/islamic-hajj-umrah/hijri-new-year-children.html", "رأس السنة الهجرية للأطفال"),
            ("/islamic.html", "قسم الإسلام"),
        ],
        "internal_links_en": [
            ("/islamic-hajj-umrah/daily-adhkar-family-guide-en.html", "Daily Adhkar Family Guide"),
            ("/islamic-hajj-umrah/hijri-new-year-children-en.html", "Hijri New Year for Children"),
            ("/islamic.html", "Islamic Hub"),
        ],
        "hero_webp": "/assets/images/hero-umrah-with-kids.webp",
        "hero_alt_ar": "حقيبة سفر عائلية وسبحة، استعداد للعمرة مع الأطفال",
        "hero_alt_en": "Family travel bag and prayer beads, Umrah with kids prep",
        "title_seo_ar": "العمرة مع الأطفال: دليل عملي",
        "title_seo_en": "Umrah With Kids: Family Guide",
    },
    {
        "id": "A-05-2",
        "draft_ar": DRAFTS / "task05/hijri-new-year-children.md",
        "draft_en": DRAFTS / "task05/hijri-new-year-children-en.md",
        "out_ar": ROOT / "islamic-hajj-umrah/hijri-new-year-children.html",
        "out_en": ROOT / "islamic-hajj-umrah/hijri-new-year-children-en.html",
        "section_ar": "🕌 إسلامي",
        "section_en": "🕌 Islamic",
        "tool_cta_ar": "/tools/age-calculator.html",
        "tool_cta_en": "/tools/age-calculator.html",
        "tool_label_ar": "حاسبة العمر",
        "tool_label_en": "Age Calculator",
        "internal_links_ar": [
            ("/islamic-hajj-umrah/umrah-with-kids.html", "العمرة مع الأطفال"),
            ("/islamic-hajj-umrah/teaching-children-allah-names.html", "أسماء الله للأطفال"),
            ("/islamic.html", "قسم الإسلام"),
        ],
        "internal_links_en": [
            ("/islamic-hajj-umrah/umrah-with-kids-en.html", "Umrah With Kids"),
            ("/islamic-hajj-umrah/teaching-children-allah-names-en.html", "Allah's Names for Children"),
            ("/islamic.html", "Islamic Hub"),
        ],
        "hero_webp": "/assets/images/hero-hijri-new-year-children.webp",
        "hero_alt_ar": "تقويم هجري وهلال على خشب دافئ، رأس السنة للأطفال",
        "hero_alt_en": "Hijri calendar and crescent on warm wood, new year for kids",
        "title_seo_ar": "رأس السنة الهجرية للأطفال",
        "title_seo_en": "Hijri New Year for Children",
    },
    {
        "id": "A-06-1",
        "draft_ar": DRAFTS / "task06/teaching-children-allah-names.md",
        "draft_en": DRAFTS / "task06/teaching-children-allah-names-en.md",
        "out_ar": ROOT / "islamic-hajj-umrah/teaching-children-allah-names.html",
        "out_en": ROOT / "islamic-hajj-umrah/teaching-children-allah-names-en.html",
        "section_ar": "🕌 إسلامي",
        "section_en": "🕌 Islamic",
        "tool_cta_ar": "/islamic.html",
        "tool_cta_en": "/islamic.html",
        "tool_label_ar": "قسم الإسلام",
        "tool_label_en": "Islamic Hub",
        "internal_links_ar": [
            ("/islamic-hajj-umrah/teaching-children-prayer-with-love.html", "تعليم الصلاة بالحب"),
            ("/islamic-hajj-umrah/daily-adhkar-family-guide.html", "أذكار الأسرة"),
            ("/islamic.html", "قسم الإسلام"),
        ],
        "internal_links_en": [
            ("/islamic-hajj-umrah/teaching-children-prayer-with-love-en.html", "Teaching Prayer With Love"),
            ("/islamic-hajj-umrah/daily-adhkar-family-guide-en.html", "Daily Adhkar Guide"),
            ("/islamic.html", "Islamic Hub"),
        ],
        "hero_webp": "/assets/images/hero-teaching-children-allah-names.webp",
        "hero_alt_ar": "كتاب أسماء الله الحسنى للأطفال على مكتب دافئ",
        "hero_alt_en": "Children's book of Allah's names on warm desk",
        "title_seo_ar": "تعليم أسماء الله للأطفال",
        "title_seo_en": "Teaching Allah's Names to Children",
    },
    {
        "id": "A-06-2",
        "draft_ar": DRAFTS / "task06/teaching-children-prayer-with-love.md",
        "draft_en": DRAFTS / "task06/teaching-children-prayer-with-love-en.md",
        "out_ar": ROOT / "islamic-hajj-umrah/teaching-children-prayer-with-love.html",
        "out_en": ROOT / "islamic-hajj-umrah/teaching-children-prayer-with-love-en.html",
        "section_ar": "🕌 إسلامي",
        "section_en": "🕌 Islamic",
        "tool_cta_ar": "/islamic.html",
        "tool_cta_en": "/islamic.html",
        "tool_label_ar": "قسم الإسلام",
        "tool_label_en": "Islamic Hub",
        "internal_links_ar": [
            ("/islamic-hajj-umrah/teaching-children-allah-names.html", "أسماء الله للأطفال"),
            ("/islamic-hajj-umrah/daily-adhkar-family-guide.html", "أذكار الأسرة"),
            ("/islamic.html", "قسم الإسلام"),
        ],
        "internal_links_en": [
            ("/islamic-hajj-umrah/teaching-children-allah-names-en.html", "Allah's Names for Children"),
            ("/islamic-hajj-umrah/daily-adhkar-family-guide-en.html", "Daily Adhkar Guide"),
            ("/islamic.html", "Islamic Hub"),
        ],
        "hero_webp": "/assets/images/hero-teaching-children-prayer-with-love.webp",
        "hero_alt_ar": "سجادة صلاة صغيرة ولعبة هادئة، تعليم الصلاة بالحب",
        "hero_alt_en": "Small prayer mat and calm toy, teaching prayer with love",
        "title_seo_ar": "تعليم الصلاة للأطفال بالحب",
        "title_seo_en": "Teaching Children to Love Prayer",
    },
    {
        "id": "A-08-1",
        "draft_ar": DRAFTS / "task08/jeddah-mortgage-calculator.md",
        "draft_en": DRAFTS / "task08/jeddah-mortgage-calculator-en.md",
        "out_ar": ROOT / "real-estate/jeddah-mortgage-calculator.html",
        "out_en": ROOT / "real-estate/jeddah-mortgage-calculator-en.html",
        "section_ar": "🏠 عقار",
        "section_en": "🏠 Real Estate",
        "tool_cta_ar": "/tools/mortgage-calculator.html",
        "tool_cta_en": "/tools/mortgage-calculator.html",
        "tool_label_ar": "حاسبة الرهن العقاري",
        "tool_label_en": "Mortgage Calculator",
        "internal_links_ar": [
            ("/real-estate/rent-vs-buy-gulf-family.html", "إيجار أم تملّك"),
            ("/real-estate/riyadh-rental-yield.html", "العائد الإيجاري في الرياض"),
            ("/real-estate.html", "قسم العقار"),
        ],
        "internal_links_en": [
            ("/real-estate/rent-vs-buy-gulf-family-en.html", "Rent vs Buy Guide"),
            ("/real-estate/riyadh-rental-yield-en.html", "Riyadh Rental Yield"),
            ("/real-estate.html", "Real Estate Hub"),
        ],
        "hero_webp": "/assets/images/hero-jeddah-mortgage-calculator.webp",
        "hero_alt_ar": "مفاتيح منزل وحاسبة على مكتب، تمويل عقاري في جدة",
        "hero_alt_en": "House keys and calculator on desk, Jeddah mortgage",
        "title_seo_ar": "حاسبة التمويل العقاري في جدة",
        "title_seo_en": "Jeddah Mortgage Calculator Guide",
    },
    {
        "id": "A-08-2",
        "draft_ar": DRAFTS / "task08/riyadh-rental-yield.md",
        "draft_en": DRAFTS / "task08/riyadh-rental-yield-en.md",
        "out_ar": ROOT / "real-estate/riyadh-rental-yield.html",
        "out_en": ROOT / "real-estate/riyadh-rental-yield-en.html",
        "section_ar": "🏠 عقار",
        "section_en": "🏠 Real Estate",
        "tool_cta_ar": "/tools/mortgage-calculator.html",
        "tool_cta_en": "/tools/mortgage-calculator.html",
        "tool_label_ar": "حاسبة الرهن العقاري",
        "tool_label_en": "Mortgage Calculator",
        "internal_links_ar": [
            ("/real-estate/jeddah-mortgage-calculator.html", "تمويل عقاري في جدة"),
            ("/real-estate/rent-vs-buy-gulf-family.html", "إيجار أم تملّك"),
            ("/real-estate.html", "قسم العقار"),
        ],
        "internal_links_en": [
            ("/real-estate/jeddah-mortgage-calculator-en.html", "Jeddah Mortgage Guide"),
            ("/real-estate/rent-vs-buy-gulf-family-en.html", "Rent vs Buy Guide"),
            ("/real-estate.html", "Real Estate Hub"),
        ],
        "hero_webp": "/assets/images/hero-riyadh-rental-yield.webp",
        "hero_alt_ar": "مبنى سكني وورقة عائد إيجاري، استثمار عقاري في الرياض",
        "hero_alt_en": "Residential building and rental yield sheet, Riyadh property",
        "title_seo_ar": "حاسبة العائد الإيجاري في الرياض",
        "title_seo_en": "Riyadh Rental Yield Calculator Guide",
    },
    {
        "id": "A-09-1",
        "draft_ar": DRAFTS / "task09/summer-camps-vs-home.md",
        "draft_en": DRAFTS / "task09/summer-camps-vs-home-en.md",
        "out_ar": ROOT / "peace-capsules/summer-camps-vs-home.html",
        "out_en": ROOT / "peace-capsules/summer-camps-vs-home-en.html",
        "section_ar": "🧘 كبسولات السلام",
        "section_en": "🧘 Peace Capsules",
        "tool_cta_ar": "/peace-capsules/beat-summer-boredom-without-screens.html",
        "tool_cta_en": "/peace-capsules/beat-summer-boredom-without-screens-en.html",
        "tool_label_ar": "ترويض ملل الصيف بلا شاشات",
        "tool_label_en": "Summer Boredom Without Screens",
        "internal_links_ar": [
            ("/peace-capsules/family-volunteering-summer.html", "تطوّع عائلي في الصيف"),
            ("/peace-capsules/beat-summer-boredom-without-screens.html", "أنشطة منزلية صيفية"),
            ("/peace-capsules/calm-morning-routine-family.html", "روتين صباحي هادئ"),
        ],
        "internal_links_en": [
            ("/peace-capsules/family-volunteering-summer-en.html", "Family Summer Volunteering"),
            ("/peace-capsules/beat-summer-boredom-without-screens-en.html", "Screen-Free Summer Ideas"),
            ("/peace-capsules/calm-morning-routine-family.html", "Calm Morning Routine"),
        ],
        "hero_webp": "/assets/images/d4l1.webp",
        "hero_alt_ar": "عائلة خليجية تخطط لأنشطة صيفية، مخيم أو برنامج منزلي",
        "hero_alt_en": "Gulf family planning summer activities, camp or home program",
        "title_seo_ar": "مخيمات صيفية أم منزل: دليل القرار",
        "title_seo_en": "Summer Camps vs Home: Kids Guide",
        "disclaimer_type": "none",
    },
    {
        "id": "A-09-2",
        "draft_ar": DRAFTS / "task09/family-volunteering-summer.md",
        "draft_en": DRAFTS / "task09/family-volunteering-summer-en.md",
        "out_ar": ROOT / "peace-capsules/family-volunteering-summer.html",
        "out_en": ROOT / "peace-capsules/family-volunteering-summer-en.html",
        "section_ar": "🧘 كبسولات السلام",
        "section_en": "🧘 Peace Capsules",
        "tool_cta_ar": "/tools/monthly-budget.html",
        "tool_cta_en": "/tools/monthly-budget.html",
        "tool_label_ar": "مخطّط الميزانية العائلية",
        "tool_label_en": "Family Budget Planner",
        "internal_links_ar": [
            ("/peace-capsules/summer-camps-vs-home.html", "مخيمات صيفية أم منزل"),
            ("/peace-capsules/beat-summer-boredom-without-screens.html", "ترويض ملل الصيف"),
            ("/peace-capsules/calm-morning-routine-family.html", "روتين صباحي هادئ"),
        ],
        "internal_links_en": [
            ("/peace-capsules/summer-camps-vs-home-en.html", "Summer Camps vs Home"),
            ("/peace-capsules/beat-summer-boredom-without-screens-en.html", "Beat Summer Boredom"),
            ("/peace-capsules/calm-morning-routine-family.html", "Calm Morning Routine"),
        ],
        "hero_webp": "/assets/images/d4l1.webp",
        "hero_alt_ar": "أسرة خليجية تتطوع معاً في الصيف، عمل عائلي ذو معنى",
        "hero_alt_en": "Gulf family volunteering together in summer",
        "title_seo_ar": "تطوّع عائلي في الصيف",
        "title_seo_en": "Family Summer Volunteering",
        "disclaimer_type": "none",
    },
]

FAQ_MARKERS = (
    "## الأسئلة الشائعة",
    "## أسئلة شائعة",
    "## Frequently Asked Questions",
    "## Common Questions",
    "## FAQ",
)

EM_DASH = "\u2014"
TITLE_SUFFIX = " | DOTFORLIFE"
MAX_TITLE_LEN = 60
MAX_META_LEN = 155
MIN_DRAFT_WORDS = 1200
MIN_FAQ_Q = 4
MIN_INTERNAL_LINKS = 3
DISCLAIMER_KEYS = ("Disclaimer:", "إخلاء مسؤولية", "Sharia Disclaimer", "إخلاء مالي")

DISCLAIMER_BY_ID: dict[str, str] = {
    "A-01-1": "financial", "A-01-2": "financial", "A-07-1": "financial",
    "A-02-1": "medical", "A-02-2": "medical", "A-03-1": "medical", "A-03-2": "medical",
    "A-04-1": "medical", "A-04-2": "sharia", "A-05-1": "sharia", "A-05-2": "sharia",
    "A-06-1": "sharia", "A-06-2": "sharia", "A-08-1": "financial", "A-08-2": "financial",
}

DISCLAIMER_PATTERNS: dict[str, re.Pattern[str] | None] = {
    "medical": re.compile(
        r"Disclaimer|إخلاء مسؤولية|medical advice|not medical|استشارة طبية|ليست استشارة",
        re.I,
    ),
    "financial": re.compile(
        r"Disclaimer|إخلاء مالي|financial advice|investment advice|not financial|ليست استشارة",
        re.I,
    ),
    "sharia": re.compile(
        r"Sharia Disclaimer|إخلاء|fatwa|فتوى|religious guidance|guidance only",
        re.I,
    ),
    "none": None,
}


class BuildGateError(Exception):
    def __init__(self, gate: str, path: Path, detail: str) -> None:
        self.gate = gate
        self.path = path
        self.detail = detail
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        super().__init__(f"BUILD GATE FAIL [{gate}] file={rel} detail={detail}")


def gate_fail(gate: str, path: Path, detail: str) -> None:
    raise BuildGateError(gate, path, detail)


def disclaimer_type_for(cfg: dict, out_path: Path) -> str:
    return cfg.get("disclaimer_type") or DISCLAIMER_BY_ID.get(cfg["id"], "none")


def extract_ldjson_blocks(page: str) -> list[dict]:
    blocks: list[dict] = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            blocks.append(json.loads(m.group(1).strip()))
        except json.JSONDecodeError as e:
            raise BuildGateError("G11", Path("?"), f"invalid JSON-LD: {e}") from e
    return blocks


def visible_word_count(page: str) -> int:
    text = re.sub(r"<script[\s\S]*?</script>", " ", page, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return len(re.findall(r"\w+", text, re.UNICODE))


def draft_word_count(md: str) -> int:
    return len(re.findall(r"\w+", md, re.UNICODE))


def has_disclaimer(page: str, dtype: str) -> bool:
    pat = DISCLAIMER_PATTERNS.get(dtype)
    if not pat:
        return True
    return bool(pat.search(page))


def count_internal_links(page: str) -> int:
    return len(re.findall(r'<a\s+href="/[^"]+"', page))


def assert_build_gates(
    page: str,
    lang: str,
    out_path: Path,
    cfg: dict,
    draft_md: str | None = None,
    *,
    strict_image: bool = False,
) -> list[str]:
    """G1–G11 fail-closed. Returns list of passed gate ids."""
    passed: list[str] = []

    # G1 em-dash
    if EM_DASH in page:
        gate_fail("G1", out_path, f"{page.count(EM_DASH)} em dash(es)")
    passed.append("G1")

    # G2 word count — draft prose (not template chrome)
    if draft_md is not None:
        wc = draft_word_count(draft_md)
        if wc < MIN_DRAFT_WORDS:
            gate_fail("G2", out_path, f"draft words={wc} < {MIN_DRAFT_WORDS}")
    else:
        wc = visible_word_count(page)
        if wc < MIN_DRAFT_WORDS:
            gate_fail("G2", out_path, f"visible words={wc} < {MIN_DRAFT_WORDS}")
    passed.append("G2")

    ld_blocks = extract_ldjson_blocks(page)

    # G11 JSON-LD valid (already parsed)
    passed.append("G11")

    # G3 Article
    article_blocks = [b for b in ld_blocks if b.get("@type") == "Article"]
    if not article_blocks:
        gate_fail("G3", out_path, "Article schema missing")
    passed.append("G3")

    # G4 FAQPage
    faq_blocks = [b for b in ld_blocks if b.get("@type") == "FAQPage"]
    if not faq_blocks:
        gate_fail("G4", out_path, "FAQPage schema missing")
    faq_q = sum(
        len(b.get("mainEntity") or [])
        for b in faq_blocks
    )
    if faq_q < MIN_FAQ_Q:
        gate_fail("G4", out_path, f"FAQ questions={faq_q} < {MIN_FAQ_Q}")
    passed.append("G4")

    # G5 hero — manifest approved (strict) or legacy WebP grandfather (audit)
    assert_g5_image(page, out_path, lang, strict=strict_image, gate_fail=gate_fail)
    passed.append("G5")

    # G6 Title
    tm = re.search(r"<title>(.*?)</title>", page)
    if not tm:
        gate_fail("G6", out_path, "no <title>")
    title = tm.group(1)
    if len(title) > MAX_TITLE_LEN:
        gate_fail("G6", out_path, f"title len={len(title)} > {MAX_TITLE_LEN}")
    if title.endswith(TITLE_SUFFIX) and title[: -len(TITLE_SUFFIX)].endswith(" "):
        gate_fail("G6", out_path, "title truncated mid-token")
    passed.append("G6")

    # G7 Meta (visible chars after entity decode)
    mm = re.search(r'<meta name="description" content="(.*?)"', page)
    if not mm:
        gate_fail("G7", out_path, "meta description missing")
    meta_text = html.unescape(mm.group(1))
    if len(meta_text) > MAX_META_LEN:
        gate_fail("G7", out_path, f"meta len={len(meta_text)} > {MAX_META_LEN}")
    passed.append("G7")

    # G8 hreflang
    lang_only = cfg.get("lang_only")
    if lang_only:
        if f'hreflang="{lang_only}"' not in page:
            gate_fail("G8", out_path, f'hreflang="{lang_only}" missing')
    else:
        if 'hreflang="ar"' not in page or 'hreflang="en"' not in page:
            gate_fail("G8", out_path, "hreflang ar/en pair missing")
    passed.append("G8")

    # G9 disclaimer
    dtype = disclaimer_type_for(cfg, out_path)
    if dtype != "none" and not has_disclaimer(page, dtype):
        gate_fail("G9", out_path, f"disclaimer missing (type={dtype})")
    passed.append("G9")

    # G10 internal links
    nlinks = count_internal_links(page)
    if nlinks < MIN_INTERNAL_LINKS:
        gate_fail("G10", out_path, f"internal links={nlinks} < {MIN_INTERNAL_LINKS}")
    passed.append("G10")

    return passed


def assert_parity(
    ar_page: str,
    en_page: str,
    cfg: dict,
    ar_path: Path,
    en_path: Path,
) -> None:
    if cfg.get("lang_only"):
        return
    ar_ld = extract_ldjson_blocks(ar_page)
    en_ld = extract_ldjson_blocks(en_page)
    ar_types = sorted(b.get("@type", "") for b in ar_ld)
    en_types = sorted(b.get("@type", "") for b in en_ld)
    if ar_types != en_types:
        gate_fail("P1", ar_path, f"schema types ar={ar_types} en={en_types}")
    ar_faq = any(b.get("@type") == "FAQPage" for b in ar_ld)
    en_faq = any(b.get("@type") == "FAQPage" for b in en_ld)
    if ar_faq != en_faq:
        gate_fail("P2", ar_path, "FAQPage parity fail")
    dtype = disclaimer_type_for(cfg, ar_path)
    if dtype != "none":
        if not has_disclaimer(ar_page, dtype):
            gate_fail("P3", ar_path, "disclaimer missing in AR")
        if not has_disclaimer(en_page, dtype):
            gate_fail("P3", en_path, "disclaimer missing in EN")


def seo_page_title(h1: str, cfg: dict, lang: str) -> str:
    key = "title_seo_en" if lang == "en" else "title_seo_ar"
    base = cfg.get(key) or h1
    limit = MAX_TITLE_LEN - len(TITLE_SUFFIX)
    if len(base) > limit:
        chunk = base[:limit]
        if " " in chunk:
            chunk = chunk.rsplit(" ", 1)[0]
        base = chunk.rstrip("?.،,")
    title = f"{base}{TITLE_SUFFIX}"
    if len(title) > MAX_TITLE_LEN:
        raise SystemExit(f"Title gate failed: {len(title)} chars > {MAX_TITLE_LEN}: {title}")
    return title


def assert_title_gate(page: str, out_path: Path) -> None:
    m = re.search(r"<title>(.*?)</title>", page)
    if not m:
        raise SystemExit(f"Title gate failed: no <title> in {out_path.name}")
    t = m.group(1)
    if len(t) > MAX_TITLE_LEN:
        raise SystemExit(f"Title gate failed: {len(t)} chars in {out_path.relative_to(ROOT)}: {t}")
    if t.endswith(TITLE_SUFFIX) and t[:-len(TITLE_SUFFIX)].endswith(" "):
        raise SystemExit(f"Title gate failed: truncated mid-token in {out_path.name}")


def extract_disclaimer_html(md: str) -> str:
    lines = md.splitlines()
    blocks: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith(">") and any(k in lines[i] for k in DISCLAIMER_KEYS):
            paras: list[str] = []
            while i < len(lines) and lines[i].startswith(">"):
                paras.append(lines[i].lstrip("> ").strip())
                i += 1
            blocks.append(f'<div class="tip"><p>{inline_md(" ".join(paras))}</p></div>')
        else:
            i += 1
    return "\n".join(blocks)


def parse_post_faq_html(md: str) -> str:
    """Content after FAQ block (takeaway, etc.) excluding Q&A pairs."""
    _, faq_block = split_at_faq(md)
    if not faq_block:
        return ""
    body = faq_block.split("\n", 1)[1] if "\n" in faq_block else ""
    parts = re.split(r"\n\*\*(.+?)\*\*\n", body)
    tail = parts[-1] if len(parts) >= 3 else ""
    tail = re.split(r"\n---\n|\nSources:", tail)[0].strip()
    if not tail:
        return ""
    out: list[str] = []
    i = 0
    lines = tail.splitlines()
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith(">") and any(k in line for k in DISCLAIMER_KEYS):
            while i < len(lines) and lines[i].startswith(">"):
                i += 1
            continue
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("**") and line.endswith("**"):
            out.append(f"<p><strong>{html.escape(line.strip('*'))}</strong></p>")
            i += 1
            continue
        if not line.startswith(("-", "*", "|")):
            out.append(f"<p>{inline_md(line.strip())}</p>")
        i += 1
    return "\n".join(out)


def assert_cf4_gate(content: str, out_path: Path) -> None:
    """C-F4: built HTML must contain zero em dashes (—)."""
    count = content.count(EM_DASH)
    if count:
        rel = out_path.relative_to(ROOT)
        raise SystemExit(f"C-F4 gate failed: {count} em dash(es) in {rel}")


def validate_build_map() -> None:
    for cfg in BUILD_MAP:
        lo = cfg.get("lang_only")
        if lo not in (None, "ar", "en"):
            raise SystemExit(f"Invalid lang_only in {cfg['id']}")
        if lo != "en" and not cfg.get("draft_ar"):
            raise SystemExit(f"Missing draft_ar in {cfg['id']}")
        if lo != "ar" and not cfg.get("draft_en"):
            raise SystemExit(f"Missing draft_en in {cfg['id']}")
        for key in ("hero_alt_ar", "hero_alt_en"):
            if key not in cfg:
                continue
            alt = cfg.get(key, "")
            if EM_DASH in alt:
                raise SystemExit(f"C-F4 gate failed: em dash in {cfg['id']} {key}")


def config_build_targets(cfg: dict) -> list[tuple[str, Path, Path]]:
    lo = cfg.get("lang_only")
    if lo == "en":
        return [("en", cfg["draft_en"], cfg["out_en"])]
    if lo == "ar":
        return [("ar", cfg["draft_ar"], cfg["out_ar"])]
    return [
        ("ar", cfg["draft_ar"], cfg["out_ar"]),
        ("en", cfg["draft_en"], cfg["out_en"]),
    ]


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s.strip())
    return s[:80] or "section"


def split_at_faq(md: str) -> tuple[str, str | None]:
    for marker in FAQ_MARKERS:
        if marker in md:
            head, tail = md.split(marker, 1)
            return head, marker + tail
    upper = md.upper()
    for marker in FAQ_MARKERS:
        idx = upper.find(marker.upper())
        if idx != -1:
            return md[:idx], md[idx:]
    return md, None


def parse_faq(md: str) -> list[tuple[str, str]]:
    faqs: list[tuple[str, str]] = []
    _, faq_block = split_at_faq(md)
    if not faq_block:
        return faqs
    block = faq_block.split("\n", 1)[1] if "\n" in faq_block else ""
    block = re.split(r"\n## ", block, maxsplit=1)[0]
    parts = re.split(r"\n\*\*(.+?)\*\*\n", block)
    if len(parts) < 3:
        return faqs
    for i in range(1, len(parts), 2):
        q = parts[i].strip()
        a = parts[i + 1].strip().split("\n\n")[0].strip()
        if q and a:
            faqs.append((q, a))
    return faqs


def md_body_html(md: str, lang: str) -> tuple[str, str]:
    """Convert main markdown body (before FAQ) to HTML."""
    cut, _ = split_at_faq(md)
    cut = re.split(r"\n---\n|\nSources:", cut)[0]
    lines = cut.splitlines()
    out: list[str] = []
    i = 0
    title = ""
    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        i = 1
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("## "):
            h = line[3:].strip()
            hid = slugify(h)
            out.append(f'<h2 id="{html.escape(hid)}">{html.escape(h)}</h2>')
            i += 1
            continue
        if line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.startswith("|"):
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].startswith("|"):
                row = [c.strip() for c in lines[i].strip("|").split("|")]
                if not all(re.match(r"^[-:\s]+$", c) for c in row):
                    rows.append(row)
                i += 1
            if rows:
                out.append('<div class="table-wrap"><table>')
                for ri, row in enumerate(rows):
                    tag = "th" if ri == 0 else "td"
                    out.append("<tr>" + "".join(f"<{tag}>{inline_md(c)}</{tag}>" for c in row) + "</tr>")
                out.append("</table></div>")
            continue
        if re.match(r"^\d+\.\s", line):
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i]):
                out.append(f"<li>{inline_md(lines[i].split('.', 1)[1].strip())}</li>")
                i += 1
            out.append("</ol>")
            continue
        if line.startswith("- ") or line.startswith("* "):
            out.append("<ul>")
            while i < len(lines) and (lines[i].startswith("- ") or lines[i].startswith("* ")):
                out.append(f"<li>{inline_md(lines[i][2:].strip())}</li>")
                i += 1
            out.append("</ul>")
            continue
        if line.startswith(">"):
            paras = []
            while i < len(lines) and lines[i].startswith(">"):
                paras.append(lines[i].lstrip("> ").strip())
                i += 1
            out.append(f'<div class="tip"><p>{inline_md(" ".join(paras))}</p></div>')
            continue
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("#", "-", "*", "|", ">")) and not re.match(r"^\d+\.", lines[i]):
            para_lines.append(lines[i])
            i += 1
        out.append(f"<p>{inline_md(' '.join(para_lines))}</p>")
    return title, "\n".join(out)


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text


def faq_html(faqs: list[tuple[str, str]]) -> str:
    if not faqs:
        return ""
    parts = ['<h2 id="faq">أسئلة شائعة</h2>' if any("\u0600" <= c <= "\u06FF" for c in faqs[0][0]) else '<h2 id="faq">FAQ</h2>']
    for q, a in faqs:
        parts.append(f"<h3>{html.escape(q)}</h3><p>{inline_md(a)}</p>")
    return "\n".join(parts)


def schema_json(
    title: str,
    desc: str,
    url: str,
    faqs: list[tuple[str, str]],
    lang: str,
    image_url: str | None = None,
) -> str:
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc[:300],
        "author": {"@type": "Organization", "name": "DOTFORLIFE" if lang == "en" else "دوت فور لايف"},
        "datePublished": date.today().isoformat(),
        "dateModified": date.today().isoformat(),
        "mainEntityOfPage": url,
    }
    if image_url:
        article["image"] = image_url
    blocks = [json.dumps(article, ensure_ascii=False)]
    if faqs:
        fq = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in faqs
            ],
        }
        blocks.append(json.dumps(fq, ensure_ascii=False))
    return "\n".join(f'<script type="application/ld+json">{b}</script>' for b in blocks)


def build_page(cfg: dict, draft_path: Path, out_path: Path, lang: str) -> tuple[str, str]:
    md = draft_path.read_text(encoding="utf-8")
    title, body = md_body_html(md, lang)
    faqs = parse_faq(md)
    if faqs:
        body += "\n" + faq_html(faqs)
    disclaimer = extract_disclaimer_html(md)
    if disclaimer and disclaimer not in body:
        body += "\n" + disclaimer
    post_faq = parse_post_faq_html(md)
    if post_faq:
        body += "\n" + post_faq

    is_en = lang == "en"
    canonical = f"https://dotforlife.com/{out_path.relative_to(ROOT).as_posix()}"
    lang_only = cfg.get("lang_only")
    href_ar = f"https://dotforlife.com/{cfg['out_ar'].relative_to(ROOT).as_posix()}" if cfg.get("out_ar") else canonical
    href_en = f"https://dotforlife.com/{cfg['out_en'].relative_to(ROOT).as_posix()}" if cfg.get("out_en") else canonical
    if lang_only:
        hreflang = f'<link rel="alternate" hreflang="{lang_only}" href="{canonical}">'
    else:
        hreflang = (
            f'<link rel="alternate" hreflang="ar" href="{href_ar}">\n'
            f'<link rel="alternate" hreflang="en" href="{href_en}">'
        )
    desc_raw = re.sub(r"\s+", " ", md.split("\n\n")[1 if md.startswith("#") else 0].strip())
    if len(desc_raw) > MAX_META_LEN:
        chunk = desc_raw[:MAX_META_LEN]
        if " " in chunk:
            chunk = chunk.rsplit(" ", 1)[0]
        desc_raw = chunk.rstrip("?.,")
    desc = desc_raw
    section = cfg.get("section_en" if is_en else "section_ar", cfg.get("section_en", ""))
    lang_link = ""
    lang_label = ""
    if not lang_only:
        lang_link = cfg["out_en" if is_en else "out_ar"].name
        lang_label = "🌐 English" if not is_en else "🌐 عربي"
    elif lang_only == "en":
        lang_link = cfg["out_en"].name
        lang_label = "🌐 English"
    else:
        lang_link = cfg["out_ar"].name
        lang_label = "🌐 عربي"
    links = cfg["internal_links_en" if is_en else "internal_links_ar"]
    tool = cfg["tool_cta_en" if is_en else "tool_cta_ar"]
    tool_label = cfg["tool_label_en" if is_en else "tool_label_ar"]
    read_also = "اقرأ أيضاً:" if not is_en else "Read also:"
    cta_tools = "🧮 أدوات مساعدة:" if not is_en else "🧮 Helpful tools:"
    footer = "© 2026 دوت فور لايف - للمعرفة والعافية" if not is_en else "© 2026 DOTFORLIFE"

    internal_p = " · ".join(f'<a href="{u}">{html.escape(l)}</a>' for u, l in links)
    resolved = resolve_hero_for_build(out_path, lang, cfg)
    hero_img = ""
    og_image = ""
    hero_abs = None
    if resolved:
        hero_img, _web, hero_abs = resolved
    elif cfg.get("hero_webp"):
        web = cfg["hero_webp"]
        alt = cfg.get(f"hero_alt_{lang}") or cfg.get("hero_alt_ar") or cfg.get("hero_alt_en") or ""
        hero_img = (
            f'<figure class="hero"><img src="{web}" alt="{html.escape(alt)}" '
            f'width="1200" height="630" loading="eager"></figure>'
        )
        hero_abs = f"https://dotforlife.com{web}"
    schema = schema_json(title, desc, canonical, faqs, lang, hero_abs)
    page_title = seo_page_title(title, cfg, lang)
    if hero_abs:
        og_image = f'<meta property="og:image" content="{hero_abs}">'
    lang_switch = ""
    if lang_link:
        lang_switch = f'<div class="lang-switch"><a href="{html.escape(lang_link)}">{lang_label}</a></div>'

    page = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{'ltr' if is_en else 'rtl'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(page_title)}</title>
<meta name="description" content="{html.escape(desc[:155])}">
<link rel="canonical" href="{canonical}">
{hreflang}
{og_image}
<script src="/scripts/lang-redirect.js?v=20260625"></script>
{schema}
<style>
body{{font-family:'Almarai','Segoe UI',sans-serif;background:#FAF8F4;color:#222;line-height:1.9;padding:20px}}
.container{{max-width:800px;margin:0 auto;background:#fff;border-radius:18px;padding:2.5rem 2rem;box-shadow:0 2px 20px rgba(5,66,65,.06)}}
h1{{font-size:26px;color:#054241;margin-bottom:.5rem;line-height:1.4}}
h2{{font-size:20px;color:#054241;margin:1.8rem 0 .8rem;border-{'left' if is_en else 'right'}:4px solid #6abfb8;padding-{'left' if is_en else 'right'}:12px}}
h3{{font-size:16px;color:#054241;margin:1.2rem 0 .5rem}}
p{{margin-bottom:1rem;color:#444;font-size:15px}}
ul,ol{{margin:0 1.2rem 1rem;color:#444;font-size:15px}}
li{{margin-bottom:.4rem}}
.tip{{background:#e8f6f5;border-{'left' if is_en else 'right'}:4px solid #6abfb8;padding:1rem 1.2rem;border-radius:10px;margin:1.2rem 0}}
.table-wrap{{overflow-x:auto;margin:1rem 0}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th{{background:#054241;color:#fff;padding:10px 12px}}
td{{padding:10px 12px;border-bottom:1px solid #eee}}
.meta{{font-size:13px;color:#888;margin-bottom:1.5rem;display:flex;gap:12px;flex-wrap:wrap}}
.meta span{{background:#f0f4f3;padding:3px 12px;border-radius:999px}}
.cta{{background:linear-gradient(135deg,#054241,#0a6b63);color:#fff;border-radius:12px;padding:1.2rem 1.5rem;margin:1.5rem 0;text-align:center}}
.cta a{{color:#ffd54f;font-weight:700;text-decoration:none}}
.lang-switch{{text-align:{'right' if is_en else 'left'};margin-bottom:1rem}}
.lang-switch a{{display:inline-block;background:#054241;color:#fff;padding:6px 16px;border-radius:8px;text-decoration:none;font-size:13px;font-weight:700}}
.footer-art{{font-size:12px;color:#999;text-align:center;margin-top:2rem}}
.hero{{margin:0 0 1.5rem;border-radius:14px;overflow:hidden}}
.hero img{{display:block;width:100%;height:auto}}
</style>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
</head>
<body>
<div class="container">
{lang_switch}
<h1>{html.escape(title)}</h1>
<div class="meta"><span>{html.escape(section)}</span><span>📅 {date.today().strftime('%Y-%m-%d')}</span></div>
{hero_img}
{body}
<div class="cta"><strong>{cta_tools}</strong> <a href="{tool}">{html.escape(tool_label)}</a></div>
<p>{read_also} {internal_p}</p>
<div class="footer-art">{footer}</div>
</div>
</body>
</html>
"""
    return page, md


def write_page(page: str, out_path: Path, cfg: dict, lang: str, md: str) -> list[str]:
    strict_image = is_approved(lookup(article_slug_from_path(out_path)))
    gates = assert_build_gates(page, lang, out_path, cfg, md, strict_image=strict_image)
    BACKUP.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        shutil.copy2(out_path, BACKUP / out_path.name)
    out_path.write_text(page, encoding="utf-8")
    wc = draft_word_count(md)
    rel = out_path.relative_to(ROOT)
    print(f"  ✅ ALL GATES PASS {rel} ({', '.join(gates + ['P-ok'])}) ~{wc}w draft")
    return gates


def apply_article_template(out_path: Path) -> None:
    """Wrap TECH_BUILD output in full site shell (header, banner, sidebar, footer)."""
    import importlib.util

    mig_path = ROOT / "scripts" / "migrate-article-template.py"
    spec = importlib.util.spec_from_file_location("d4l_migrate_tpl", mig_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Cannot load migrate-article-template.py for {out_path}")
    mig = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mig)
    content = mig.read_file(str(out_path))
    if mig.has_template(content):
        return
    result = mig.build_new_page(out_path.name, content)
    if not result:
        raise SystemExit(f"Template migration failed: {out_path.relative_to(ROOT)}")
    ok, why = mig.structure_valid(result)
    if not ok:
        raise SystemExit(f"Template structure invalid {out_path.relative_to(ROOT)}: {why}")
    mig.write_file(str(out_path), result)
    print(f"  🎨 TEMPLATE {out_path.relative_to(ROOT)}")


def audit_live() -> int:
    """Audit LIVE HTML from BUILD_MAP — no rebuild unless FAIL."""
    print("=== LIVE GATE AUDIT (G1–G11 + parity) ===\n")
    fails: list[str] = []
    passed = 0
    for cfg in BUILD_MAP:
        built: dict[str, tuple[str, Path, str]] = {}
        for lang, draft_path, out_path in config_build_targets(cfg):
            if not out_path.exists():
                fails.append(f"MISSING {out_path.relative_to(ROOT)}")
                continue
            page = out_path.read_text(encoding="utf-8")
            md = draft_path.read_text(encoding="utf-8") if draft_path.exists() else ""
            try:
                assert_build_gates(page, lang, out_path, cfg, md or None, strict_image=False)
                built[lang] = (page, out_path, md)
                passed += 1
                print(f"  PASS {out_path.relative_to(ROOT)}")
            except BuildGateError as e:
                fails.append(str(e))
                print(f"  FAIL {e}")
        if not cfg.get("lang_only") and "ar" in built and "en" in built:
            try:
                assert_parity(
                    built["ar"][0], built["en"][0], cfg,
                    built["ar"][1], built["en"][1],
                )
                print(f"  PASS parity {cfg['id']}")
            except BuildGateError as e:
                fails.append(str(e))
                print(f"  FAIL {e}")

    oman = ROOT / "real-estate/oman-property-roi.html"
    oman_draft = ROOT / "operating-system/reports/drafts/task07/oman-property-roi.md"
    oman_cfg = {
        "id": "A-07-2",
        "lang_only": "en",
        "disclaimer_type": "financial",
        "out_en": oman,
    }
    if oman.exists() and oman_draft.exists():
        page = oman.read_text(encoding="utf-8")
        md = oman_draft.read_text(encoding="utf-8")
        if "DFL SURGICAL ARTICLE" in page:
            try:
                assert_build_gates(page, "en", oman, oman_cfg, md)
                passed += 1
                print(f"  PASS {oman.relative_to(ROOT)} (surgical inject)")
            except BuildGateError as e:
                fails.append(str(e))
                print(f"  FAIL {e}")
        else:
            print(f"\n  SKIP {oman.relative_to(ROOT)} — calculator shell (surgical inject pending)")

    print(f"\n=== SUMMARY: {passed} pages PASS, {len(fails)} FAIL ===")
    for f in fails:
        print(f"  • {f}")
    return 1 if fails else 0


def main() -> None:
    validate_build_map()
    if len(sys.argv) > 1 and sys.argv[1] == "--audit":
        raise SystemExit(audit_live())
    ids = sys.argv[1:] if len(sys.argv) > 1 else [c["id"] for c in BUILD_MAP]
    for cfg in BUILD_MAP:
        if cfg["id"] not in ids and ids != ["all"]:
            continue
        print(f"Building {cfg['id']}…")
        rendered: list[tuple[str, Path, str, str]] = []
        for lang, draft_path, out_path in config_build_targets(cfg):
            page, md = build_page(cfg, draft_path, out_path, lang)
            rendered.append((lang, out_path, page, md))
        if not cfg.get("lang_only") and len(rendered) == 2:
            ar = next(r for r in rendered if r[0] == "ar")
            en = next(r for r in rendered if r[0] == "en")
            assert_parity(ar[2], en[2], cfg, ar[1], en[1])
        for lang, out_path, page, md in rendered:
            write_page(page, out_path, cfg, lang, md)
            apply_article_template(out_path)


if __name__ == "__main__":
    main()
