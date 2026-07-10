#!/usr/bin/env python3
"""Apply health-hub quality pattern to finance / real-estate / travel / islamic."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SUBNAV = """<div id="sub-nav">
  <div class="sub-nav-inner">
    <a href="#start-here"><span class="en">Start here</span><span class="ar">ابدأ من هنا</span></a>
    <a href="#tools"><span class="en">All tools</span><span class="ar">كل الأدوات</span></a>
    <a href="#guides"><span class="en">Guides</span><span class="ar">الأدلة</span></a>
    <a href="#hub-faq"><span class="en">FAQ</span><span class="ar">أسئلة شائعة</span></a>
    <a href="#latest-articles"><span class="en">Articles</span><span class="ar">المقالات</span></a>
  </div>
</div>"""

ICON = {
    "budget": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "salary": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>',
    "fx": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "zakat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
    "pack": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',
    "prayer": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
    "qibla": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
    "hijri": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    "inherit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "tips": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
}


def tool_card(href: str, title_en: str, title_ar: str, desc_en: str, desc_ar: str,
              icon: str, accent: str = "#054241", badge: tuple[str, str] | None = None,
              featured: bool = False) -> str:
    badge_html = ""
    if badge:
        cls = "hh-card-badge"
        if badge[0] == "mint":
            cls += " hh-card-badge--mint"
            label_en, label_ar = badge[1], badge[2] if len(badge) > 2 else badge[1]
        elif badge[0] == "gold":
            cls += " hh-card-badge--gold"
            label_en, label_ar = badge[1], badge[2] if len(badge) > 2 else badge[1]
        else:
            label_en, label_ar = badge[0], badge[1]
        badge_html = f'<span class="{cls}"><span class="en">{label_en}</span><span class="ar">{label_ar}</span></span>'
    feat = " hh-card--featured" if featured else ""
    return f'''            <a href="{href}" class="hl-card hl-card--tool{feat}" style="--hl-accent:{accent}">
              {badge_html}
              <div class="hl-card-icon">{icon}</div>
              <div class="hl-card-title"><span class="en">{title_en}</span><span class="ar">{title_ar}</span></div>
              <div class="hl-card-desc"><span class="en">{desc_en}</span><span class="ar">{desc_ar}</span></div>
              <div class="hl-card-arrow"><span class="en">Open tool →</span><span class="ar">افتح الأداة →</span></div>
            </a>'''


def chooser_card(href: str, title_en: str, title_ar: str, go_en: str, go_ar: str, icon: str) -> str:
    return f'''          <a href="{href}" class="hh-chooser-card">
            <span class="hh-chooser-icon" aria-hidden="true">{icon}</span>
            <span class="hh-chooser-title"><span class="en">{title_en}</span><span class="ar">{title_ar}</span></span>
            <span class="hh-chooser-go"><span class="en">{go_en}</span><span class="ar">{go_ar}</span></span>
          </a>'''


def trust_section(badges: list[tuple[str, str, str]], note_en: str, note_ar: str) -> str:
    rows = []
    for mark, en, ar in badges:
        rows.append(f'''          <div class="hh-trust-badge">
            <span class="hh-trust-mark">{mark}</span>
            <span class="hh-trust-text"><span class="en">{en}</span><span class="ar">{ar}</span></span>
          </div>''')
    return f'''    <section class="hh-trust" aria-label="Trust standards">
      <div class="hl-container">
        <p class="hh-trust-label">
          <span class="en">Built for Gulf families</span>
          <span class="ar">مبنية لعائلات الخليج</span>
        </p>
        <div class="hh-trust-row">
{chr(10).join(rows)}
        </div>
        <p class="hh-trust-note">
          <span class="en">{note_en}</span>
          <span class="ar">{note_ar}</span>
        </p>
      </div>
    </section>'''


def chooser_section(cards: list[str]) -> str:
    return f'''    <section class="hl-section" id="start-here" aria-label="Where to start">
      <div class="hl-container hl-wide">
        <div class="hl-eyebrow">
          <span class="en">New here?</span>
          <span class="ar">زائر جديد؟</span>
        </div>
        <h2 class="hl-h2">
          <span class="en">Not sure where to start?</span>
          <span class="ar">مش عارف تبدأ منين؟</span>
        </h2>
        <p class="hl-sub">
          <span class="en">Pick what fits you today  -  we will point you to the right free tool.</span>
          <span class="ar">اختر ما يناسبك اليوم  -  نوجّهك للأداة المجانية المناسبة.</span>
        </p>
        <div class="hh-chooser">
{chr(10).join(cards)}
        </div>
      </div>
    </section>'''


def tools_section(aria: str, title_en: str, title_ar: str, groups: list[tuple[str, str, list[str]]]) -> str:
    parts = []
    for gen, gar, cards in groups:
        parts.append(f'''        <div class="hh-tool-group">
          <h3 class="hh-tool-group-title"><span class="en">{gen}</span><span class="ar">{gar}</span></h3>
          <div class="hl-grid hl-grid--tools">
{chr(10).join(cards)}
          </div>
        </div>''')
    return f'''    <section class="hl-section hl-section--cream" id="tools" aria-label="{aria}">
      <div class="hl-container hl-wide">
        <div class="hl-eyebrow">
          <span class="en">Free Calculators</span>
          <span class="ar">حاسبات مجانية</span>
        </div>
        <h2 class="hl-h2">
          <span class="en">{title_en}</span>
          <span class="ar">{title_ar}</span>
        </h2>
        <p class="hl-sub">
          <span class="en">Each tool has its own page for deep use and search. Calculations run locally  -  nothing is stored.</span>
          <span class="ar">لكل أداة صفحتها الخاصة للاستخدام العميق والفهرسة. الحسابات محلية  -  لا يُخزَّن شيء.</span>
        </p>
{chr(10).join(parts)}
      </div>
    </section>'''


def guides_section(title_en: str, title_ar: str, columns: list[tuple[str, str, list[tuple[str, str, str]]]]) -> str:
    cols = []
    for cen, car, links in columns:
        lis = "\n".join(
            f'              <li><a href="{href}"><span class="en">{en}</span><span class="ar">{ar}</span></a></li>'
            for href, en, ar in links
        )
        cols.append(f'''          <div class="hl-card hl-card--topic">
            <div class="hl-topic-head">
              <span class="hl-topic-head-icon" aria-hidden="true">{ICON["book"]}</span>
              <h3 class="hl-topic-title"><span class="en">{cen}</span><span class="ar">{car}</span></h3>
            </div>
            <ul class="hl-topic-list">
{lis}
            </ul>
          </div>''')
    return f'''    <section class="hl-section hl-topic-authority" id="guides">
      <div class="hl-container hl-wide">
        <div class="hl-eyebrow">
          <span class="en">Topic Authority</span>
          <span class="ar">مرجعية الموضوع</span>
        </div>
        <h2 class="hl-h2">
          <span class="en">{title_en}</span>
          <span class="ar">{title_ar}</span>
        </h2>
        <p class="hl-sub">
          <span class="en">Evidence-based guides for Gulf families  -  tools live in the catalog above.</span>
          <span class="ar">أدلة قائمة على الأدلة للعائلات الخليجية  -  الأدوات في الكتالوج أعلاه.</span>
        </p>
        <div class="hl-grid hl-grid--topic">
{chr(10).join(cols)}
        </div>
      </div>
    </section>'''


def faq_section(title_en: str, title_ar: str, faqs: list[tuple[str, str, str, str]]) -> str:
    items = []
    for qe, qa, ae, aa in faqs:
        items.append(f'''          <div class="faq-item hh-faq-item">
            <h3><span class="en">{qe}</span><span class="ar">{qa}</span></h3>
            <p><span class="en">{ae}</span><span class="ar">{aa}</span></p>
          </div>''')
    return f'''    <section class="hl-section hl-section--cream" id="hub-faq" aria-label="Frequently asked questions">
      <div class="hl-container">
        <div class="hl-eyebrow">
          <span class="en">FAQ</span>
          <span class="ar">أسئلة شائعة</span>
        </div>
        <h2 class="hl-h2">
          <span class="en">{title_en}</span>
          <span class="ar">{title_ar}</span>
        </h2>
        <p class="hl-sub">
          <span class="en">General guidance for the page  -  each tool also has its own FAQ.</span>
          <span class="ar">إرشاد عام للصفحة  -  ولكل أداة أسئلتها الخاصة أيضاً.</span>
        </p>
        <div class="hh-faq">
{chr(10).join(items)}
        </div>
      </div>
    </section>'''


def faq_jsonld(faqs: list[tuple[str, str, str, str]]) -> str:
    entities = [
        {
            "@type": "Question",
            "name": qe,
            "acceptedAnswer": {"@type": "Answer", "text": ae},
        }
        for qe, _qa, ae, _aa in faqs
    ]
    payload = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    return '<script type="application/ld+json">' + json.dumps(payload, ensure_ascii=False) + "</script>"


def build_finance() -> tuple[str, list]:
    trust = trust_section(
        [
            ("SAMA", "Banking & mortgage context", "سياق البنوك والتمويل"),
            ("Sharia", "Islamic finance aware", "مراعاة المالية الإسلامية"),
            ("Private", "Runs in your browser", "يعمل في متصفحك"),
            ("GCC", "SAR · AED · QAR · more", "ريال · درهم · وأكثر"),
        ],
        "Educational tools for household planning  -  not personalized financial advice.",
        "أدوات تعليمية لتخطيط الأسرة  -  وليست استشارة مالية شخصية.",
    )
    chooser = chooser_section([
        chooser_card("/tools/monthly-budget.html", "My budget feels chaotic", "ميزانيتي فوضى", "Monthly Budget →", "الميزانية الشهرية →", ICON["budget"]),
        chooser_card("/tools/mortgage-calculator.html", "I am buying a home", "أشتري منزلاً", "Mortgage Calculator →", "حاسبة التمويل →", ICON["home"]),
        chooser_card("/tools/zakat-calculator.html", "I need to calculate Zakat", "أحتاج حساب الزكاة", "Zakat Calculator →", "حاسبة الزكاة →", ICON["zakat"]),
        chooser_card("/tools/savings-goal.html", "I am saving for a goal", "أدّخر لهدف", "Savings Goal →", "هدف الادخار →", ICON["target"]),
        chooser_card("/tools/roi-calculator.html", "I want to compare returns", "أبي أقارن العوائد", "ROI Calculator →", "حاسبة العائد →", ICON["chart"]),
        chooser_card("/tools/salary-calculator.html", "I want take-home pay clarity", "أبي وضوح صافي الراتب", "Salary Calculator →", "حاسبة الراتب →", ICON["salary"]),
    ])
    tools = tools_section(
        "Finance tools",
        "All finance tools in one place",
        "كل أدوات المالية في مكان واحد",
        [
            ("Budget & cashflow", "الميزانية والتدفق", [
                tool_card("/tools/monthly-budget.html", "Monthly Budget Planner", "مخطط الميزانية الشهرية",
                          "Track income, fixed expenses, savings, and discretionary spending for Gulf households.",
                          "تتبع الدخل والمصروفات الثابتة والادخار والمصروفات الاختيارية للأسر الخليجية.",
                          ICON["budget"], badge=("Essential", "أساسي"), featured=True),
                tool_card("/tools/salary-calculator.html", "Salary Calculator", "حاسبة الراتب",
                          "Estimate monthly take-home pay after common GCC deductions and contributions.",
                          "قدّر صافي راتبك الشهري بعد الخصومات والمساهمات الشائعة في الخليج.",
                          ICON["salary"], accent="#0a6b63"),
                tool_card("/tools/savings-goal.html", "Savings Goal Planner", "مخطط هدف الادخار",
                          "Set a target and see how much to save monthly for education, travel, or a home.",
                          "حدد هدفاً وشاهد كم تحتاج لتوفر شهرياً للتعليم أو السفر أو منزل.",
                          ICON["target"], accent="#4a8a82"),
            ]),
            ("Home & obligations", "المنزل والالتزامات", [
                tool_card("/tools/mortgage-calculator.html", "Mortgage Calculator", "حاسبة التمويل العقاري",
                          "Monthly payments, total profit, and term comparisons for Islamic home financing.",
                          "الأقساط الشهرية والأرباح الكلية ومقارنة المدد للتمويل العقاري الإسلامي.",
                          ICON["home"], badge=("Sharia", "شرعي")),
                tool_card("/tools/zakat-calculator.html", "Zakat Calculator", "حاسبة الزكاة",
                          "Calculate Zakat on cash, gold, investments, and property with current nisab values.",
                          "احسب الزكاة على النقد والذهب والاستثمارات والعقار بقيم النصاب الحالية.",
                          ICON["zakat"], accent="#0a6b63", badge=("Obligation", "فريضة")),
            ]),
            ("Growth & currency", "النمو والعملات", [
                tool_card("/tools/roi-calculator.html", "ROI Calculator", "حاسبة العائد",
                          "Estimate return on investment and compare opportunities side by side.",
                          "قدّر عائد الاستثمار وقارن الفرص جنباً إلى جنب.",
                          ICON["chart"]),
                tool_card("/tools/currency-converter.html", "Currency Converter", "محول العملات",
                          "Exchange rates for SAR, AED, QAR, KWD, BHD, OMR, EGP, and major world currencies.",
                          "أسعار صرف للريال والدرهم والريال القطري والدينار وغيرها.",
                          ICON["fx"], accent="#3a9d8e"),
            ]),
        ],
    )
    guides = guides_section(
        "Explore Family Finance",
        "استكشف مالية الأسرة",
        [
            ("Core money guides", "أدلة المال الأساسية", [
                ("/comparisons/saving-vs-investing-gulf-family.html", "Saving vs Investing", "ادخار أم استثمار"),
                ("/blog/gold-vs-savings-account-comparison.html", "Gold vs Savings", "ذهب أم ادخار"),
                ("/blog/end-of-service-benefits-expats.html", "End of Service Benefits", "مكافأة نهاية الخدمة"),
            ]),
            ("Family planning", "تخطيط الأسرة", [
                ("/blog/teaching-children-financial-literacy.html", "Teaching Children Financial Literacy", "تعليم الأطفال الثقافة المالية"),
                ("/blog/rent-vs-buy-saudi-guide-2026.html", "Rent vs Buy Guide", "دليل إيجار أم شراء"),
                ("/finance-wealth/family-budget-plan.html", "Family Budget Plan", "خطة ميزانية الأسرة"),
            ]),
            ("Go deeper", "تعمّق أكثر", [
                ("/finance-wealth/investment-basics-beginners.html", "Investment Basics for Beginners", "أساسيات الاستثمار للمبتدئين"),
                ("/library.html?cat=finance", "All finance tools in Library", "كل أدوات المالية في المكتبة"),
                ("/blog.html", "Browse the blog", "تصفّح المدونة"),
            ]),
        ],
    )
    faqs = [
        ("Which finance calculator should I start with?", "أي حاسبة مالية أبدأ بها؟",
         "If your spending feels unstructured, start with the Monthly Budget Planner. Buying a home? Use the Mortgage Calculator. Paying Zakat? Open the Zakat Calculator. Saving for a goal or comparing returns? Use Savings Goal or ROI.",
         "إن كان إنفاقك بلا هيكل فابدأ بمخطط الميزانية الشهرية. تشتري منزلاً؟ استخدم حاسبة التمويل. تدفع زكاة؟ افتح حاسبة الزكاة. تدّخر لهدف أو تقارن عوائد؟ استخدم هدف الادخار أو حاسبة العائد."),
        ("Are these finance tools free and private?", "هل أدوات المالية مجانية وخاصة؟",
         "Yes. All DOTFORLIFE finance calculators are free. Calculations run in your browser  -  we do not store or share your income, balances, or personal numbers.",
         "نعم. كل حاسبات المالية في دوت فور لايف مجانية. الحسابات تعمل في متصفحك  -  لا نخزّن دخلك أو أرصدتك أو أرقامك الشخصية ولا نشاركها."),
        ("Are the tools Sharia-aware?", "هل الأدوات تراعي الجانب الشرعي؟",
         "Yes where it matters. The mortgage calculator supports Islamic financing terms, and the Zakat calculator covers common asset types with current nisab values. Tools are educational aids, not a fatwa or personalized advice.",
         "نعم حيث يلزم. حاسبة التمويل تدعم صيغ التمويل الإسلامي، وحاسبة الزكاة تغطي أنواع أصول شائعة بقيم النصاب الحالية. الأدوات تعليمية وليست فتوى أو استشارة شخصية."),
        ("Do you give personalized financial advice?", "هل تقدّمون استشارة مالية شخصية؟",
         "No. These pages help you run numbers and understand options. For banking products, tax, or investment decisions, consult a licensed advisor or your bank.",
         "لا. هذه الصفحات تساعدك على حساب الأرقام وفهم الخيارات. لمنتجات البنوك أو الضرائب أو قرارات الاستثمار استشر مستشاراً مرخّصاً أو بنكك."),
        ("Which currencies and Gulf contexts are supported?", "أي عملات وسياقات خليجية مدعومة؟",
         "The currency converter covers major GCC currencies plus common world currencies. Budget, salary, and savings tools are written for Gulf household realities such as family obligations and varying city costs.",
         "محول العملات يغطي عملات الخليج الرئيسية بالإضافة لعملات عالمية شائعة. أدوات الميزانية والراتب والادخار مكتوبة لواقع الأسر الخليجية مثل الالتزامات العائلية واختلاف تكلفة المدن."),
        ("Where can I read deeper finance guides?", "أين أقرأ أدلة مالية أعمق؟",
         "Use the guides section on this page for saving vs investing, gold vs savings, end-of-service benefits, rent vs buy, and teaching children financial literacy. Each guide links to matching free tools when useful.",
         "استخدم قسم الأدلة في هذه الصفحة لادخار أم استثمار، ذهب أم ادخار، نهاية الخدمة، إيجار أم شراء، وتعليم الأطفال الثقافة المالية. كل دليل يربط بالأداة المجانية المناسبة عند الحاجة."),
    ]
    faq = faq_section("Questions about this finance hub", "أسئلة عن محور المالية", faqs)
    middle = "\n\n".join([trust, chooser, tools, guides, faq])
    return middle, faqs


def build_real_estate() -> tuple[str, list]:
    trust = trust_section(
        [
            ("SAMA", "Mortgage & DBR context", "سياق التمويل وعبء الدين"),
            ("REGA", "Market education focus", "تركيز تعليمي على السوق"),
            ("Private", "Runs in your browser", "يعمل في متصفحك"),
            ("GCC", "Cities & family homes", "مدن ومنازل أسرية"),
        ],
        "Educational property tools  -  not a valuation, brokerage, or lending offer.",
        "أدوات عقارية تعليمية  -  وليست تقييمًا أو وساطة أو عرض تمويل.",
    )
    chooser = chooser_section([
        chooser_card("/tools/mortgage-calculator.html", "I need monthly payment clarity", "أبي وضوح القسط الشهري", "Mortgage Calculator →", "حاسبة التمويل →", ICON["home"]),
        chooser_card("/tools/rental-yield-calculator.html", "I am checking rental ROI", "أفحص عائد الإيجار", "Rental Yield →", "العائد الإيجاري →", ICON["chart"]),
        chooser_card("/tools/roi-calculator.html", "I want to compare investments", "أبي أقارن الاستثمارات", "ROI Calculator →", "حاسبة العائد →", ICON["chart"]),
        chooser_card("/tools/savings-goal.html", "I am saving a down payment", "أدّخر للدفعة الأولى", "Savings Goal →", "هدف الادخار →", ICON["target"]),
        chooser_card("/tools/salary-calculator.html", "I want income clarity first", "أبي وضوح الدخل أولاً", "Salary Calculator →", "حاسبة الراتب →", ICON["salary"]),
    ])
    tools = tools_section(
        "Real Estate tools",
        "All real estate tools in one place",
        "كل أدوات العقار في مكان واحد",
        [
            ("Buy & finance", "الشراء والتمويل", [
                tool_card("/tools/mortgage-calculator.html", "Islamic Mortgage Calculator", "حاسبة التمويل الإسلامي",
                          "Monthly payments, total profit, and term comparisons for a known financing amount.",
                          "الأقساط الشهرية والأرباح الكلية ومقارنة المدد لمبلغ تمويل معروف.",
                          ICON["home"], badge=("Essential", "أساسي"), featured=True),
                tool_card("/tools/savings-goal.html", "Down Payment Planner", "مخطط الدفعة الأولى",
                          "See how much to save monthly to reach your down payment target on a clear timeline.",
                          "شاهد كم تحتاج لتوفر شهرياً للوصول لهدف الدفعة الأولى بجدول زمني واضح.",
                          ICON["target"], accent="#0a6b63"),
                tool_card("/tools/salary-calculator.html", "Salary Calculator", "حاسبة الراتب",
                          "Clarify take-home pay before you stress-test a mortgage payment.",
                          "وضّح صافي الراتب قبل اختبار قدرة تحمّل قسط التمويل.",
                          ICON["salary"], accent="#4a8a82"),
            ]),
            ("Yield & returns", "العائد والعوائد", [
                tool_card("/tools/rental-yield-calculator.html", "Rental Yield Analyzer", "محلل العائد الإيجاري",
                          "Gross vs net yield style estimates for rental property scenarios in GCC markets.",
                          "تقديرات بأسلوب العائد الإجمالي مقابل الصافي لسيناريوهات الإيجار في أسواق الخليج.",
                          ICON["chart"], badge=("Invest", "استثمار")),
                tool_card("/tools/roi-calculator.html", "ROI Calculator", "حاسبة العائد",
                          "Compare property and non-property opportunities with a simple return estimate.",
                          "قارن فرص العقار وغير العقار بتقدير عائد بسيط.",
                          ICON["chart"], accent="#0a6b63"),
            ]),
        ],
    )
    guides = guides_section(
        "Explore Real Estate",
        "استكشف العقار",
        [
            ("Buying guides", "أدلة الشراء", [
                ("/guides/saudi-real-estate-investing.html", "Saudi Real Estate Investing", "الاستثمار العقاري في السعودية"),
                ("/blog/rent-vs-buy-saudi-guide-2026.html", "Rent vs Buy Guide 2026", "دليل إيجار أم شراء 2026"),
                ("/blog/house-affordability-single-income-guide.html", "House Affordability on One Income", "القدرة على شراء منزل بدخل واحد"),
            ]),
            ("Compare options", "قارن الخيارات", [
                ("/real-estate/rent-vs-buy-gulf-family.html", "Rent vs Buy for Gulf Families", "إيجار أم تملّك للأسر الخليجية"),
                ("/blog/gold-vs-savings-account-comparison.html", "Gold vs Savings", "ذهب أم ادخار"),
                ("/real-estate/oman-property-roi.html", "Oman Property ROI", "عائد العقار في عُمان"),
            ]),
            ("Go deeper", "تعمّق أكثر", [
                ("/library.html?cat=real-estate", "All real estate tools in Library", "كل أدوات العقار في المكتبة"),
                ("/guides/saudi-mortgage-guide.html", "Saudi Mortgage Guide", "دليل التمويل العقاري السعودي"),
                ("/blog.html", "Browse the blog", "تصفّح المدونة"),
            ]),
        ],
    )
    faqs = [
        ("Which real estate tool should I start with?", "أي أداة عقارية أبدأ بها؟",
         "If you already know a loan amount, start with the Mortgage Calculator for monthly payments. Checking a rental? Use Rental Yield. Saving for a down payment? Open Savings Goal. Comparing returns broadly? Use ROI.",
         "إن كنت تعرف مبلغ التمويل فابدأ بحاسبة التمويل للأقساط الشهرية. تفحص إيجاراً؟ استخدم العائد الإيجاري. تدّخر للدفعة الأولى؟ افتح هدف الادخار. تقارن عوائد عامة؟ استخدم حاسبة العائد."),
        ("Do you have a max affordable home or DBR calculator?", "هل لديكم حاسبة أقصى سعر عقار أو عبء الدين؟",
         "Not yet. Our mortgage tool starts from a known financing amount and shows payments and total cost. A debt-burden (DBR) style max-price planner is under study for a future update. Until then, pair Mortgage with Salary and Savings Goal.",
         "ليس بعد. أداة التمويل تبدأ من مبلغ تمويل معروف وتعرض الأقساط والتكلفة الكلية. مخطط أقصى سعر بأسلوب عبء الدين قيد الدراسة لتحديث لاحق. حتى ذلك الحين اجمع بين التمويل والراتب وهدف الادخار."),
        ("Are these property tools free and private?", "هل أدوات العقار مجانية وخاصة؟",
         "Yes. Calculations run locally in your browser. We do not store property prices, incomes, or personal figures you enter.",
         "نعم. الحسابات تعمل محلياً في متصفحك. لا نخزّن أسعار العقار أو الدخول أو الأرقام الشخصية التي تدخلها."),
        ("Is this a valuation or brokerage service?", "هل هذه خدمة تقييم أو وساطة؟",
         "No. DOTFORLIFE provides educational calculators and guides. For appraisals, listings, or loan offers, use licensed professionals and official channels.",
         "لا. دوت فور لايف يقدّم حاسبات وأدلة تعليمية. للتقييم أو العروض أو التمويل استخدم مختصين مرخّصين والقنوات الرسمية."),
        ("How should Gulf families think about rent vs buy?", "كيف تفكّر الأسر الخليجية في إيجار أم شراء؟",
         "Start with cashflow stability, down payment readiness, and how long you expect to stay. Use Rent vs Buy guides on this page, then stress-test payments with the Mortgage Calculator.",
         "ابدأ باستقرار التدفق النقدي وجاهزية الدفعة الأولى ومدة الإقامة المتوقعة. استخدم أدلة إيجار أم شراء في هذه الصفحة، ثم اختبر الأقساط بحاسبة التمويل."),
        ("Where can I read deeper property guides?", "أين أقرأ أدلة عقارية أعمق؟",
         "See Saudi real estate investing, rent vs buy, single-income affordability, and city ROI articles linked in the guides section above.",
         "راجع الاستثمار العقاري السعودي، إيجار أم شراء، القدرة بدخل واحد، ومقالات عائد المدن في قسم الأدلة أعلاه."),
    ]
    faq = faq_section("Questions about this real estate hub", "أسئلة عن محور العقار", faqs)
    return "\n\n".join([trust, chooser, tools, guides, faq]), faqs


def build_travel() -> tuple[str, list]:
    trust = trust_section(
        [
            ("Nusuk", "Official Umrah platform", "منصة العمرة الرسمية"),
            ("Private", "Runs in your browser", "يعمل في متصفحك"),
            ("Bilingual", "Arabic & English", "عربي وإنجليزي"),
            ("Family", "Gulf family trips", "رحلات أسر الخليج"),
        ],
        "Planning aids for travel and Umrah logistics  -  always confirm bookings on official platforms.",
        "مساعدات تخطيط للسفر ولوجستيات العمرة  -  أكّد الحجوزات دائماً على المنصات الرسمية.",
    )
    chooser = chooser_section([
        chooser_card("/tools/travel-budget.html", "I am planning an Umrah budget", "أخطّط لميزانية عمرة", "Travel Budget →", "ميزانية السفر →", ICON["budget"]),
        chooser_card("/tools/packing-checklist.html", "I need a packing list", "أحتاج قائمة حقائب", "Packing Checklist →", "قائمة الحقائب →", ICON["pack"]),
        chooser_card("/tools/prayer-times.html", "I need prayer times on the road", "أحتاج مواقيت الصلاة في الطريق", "Prayer Times →", "مواقيت الصلاة →", ICON["prayer"]),
        chooser_card("/tools/currency-converter.html", "I need exchange rates", "أحتاج أسعار الصرف", "Currency Converter →", "محول العملات →", ICON["fx"]),
        chooser_card("/tools/qibla.html", "I need the Qibla direction", "أحتاج اتجاه القبلة", "Qibla Finder →", "اتجاه القبلة →", ICON["qibla"]),
        chooser_card("/tools/travel-tips.html", "I want practical trip tips", "أبي نصائح عملية للرحلة", "Travel Tips →", "نصائح السفر →", ICON["tips"]),
    ])
    tools = tools_section(
        "Travel tools",
        "All travel tools in one place",
        "كل أدوات السفر في مكان واحد",
        [
            ("Trip planning", "تخطيط الرحلة", [
                tool_card("/tools/travel-budget.html", "Travel Budget Planner", "مخطط ميزانية السفر",
                          "Build a realistic trip budget for flights, stay, food, and family extras.",
                          "ابنِ ميزانية رحلة واقعية للطيران والإقامة والطعام وإضافات الأسرة.",
                          ICON["budget"], badge=("Essential", "أساسي"), featured=True),
                tool_card("/tools/packing-checklist.html", "Packing Checklist", "قائمة الحقائب",
                          "Pack smarter for Umrah, family trips, and Gulf weather without overpacking.",
                          "جهّز حقائبك بذكاء للعمرة ورحلات الأسرة وطقس الخليج دون مبالغة.",
                          ICON["pack"], accent="#0a6b63"),
                tool_card("/tools/travel-tips.html", "Travel Tips", "نصائح السفر",
                          "Practical reminders for smoother family travel days.",
                          "تذكيرات عملية لأيام سفر أسرية أكثر سلاسة.",
                          ICON["tips"], accent="#4a8a82"),
            ]),
            ("Faith on the road", "العبادة في الطريق", [
                tool_card("/tools/prayer-times.html", "Prayer Times", "مواقيت الصلاة",
                          "Prayer times for your location while traveling.",
                          "مواقيت الصلاة حسب موقعك أثناء السفر.",
                          ICON["prayer"], badge=("Daily", "يومي")),
                tool_card("/tools/qibla.html", "Qibla Finder", "اتجاه القبلة",
                          "Find the Qibla direction quickly when you are away from home.",
                          "اعرف اتجاه القبلة بسرعة وأنت بعيداً عن المنزل.",
                          ICON["qibla"], accent="#0a6b63"),
            ]),
            ("Money & FX", "المال والعملات", [
                tool_card("/tools/currency-converter.html", "Currency Converter", "محول العملات",
                          "Convert SAR, AED, and other currencies before and during your trip.",
                          "حوّل الريال والدرهم وغيرهما قبل الرحلة وأثناءها.",
                          ICON["fx"], accent="#3a9d8e"),
            ]),
        ],
    )
    guides = guides_section(
        "Explore Travel & Umrah",
        "استكشف السفر والعمرة",
        [
            ("Destinations", "الوجهات", [
                ("/guides/mecca-medina.html", "Makkah & Madinah Guide", "دليل مكة والمدينة"),
                ("/guides/salalah-oman.html", "Salalah, Oman Guide", "دليل صلالة عُمان"),
                ("/guides/saudi-tourism.html", "Saudi Tourism Guide", "دليل السياحة السعودية"),
            ]),
            ("Umrah & family", "العمرة والأسرة", [
                ("/blog/umrah-packing-checklist-guide.html", "Umrah Packing Checklist Guide", "دليل قائمة حقائب العمرة"),
                ("/islamic-hajj-umrah/umrah-with-kids.html", "Umrah with Kids", "العمرة مع الأطفال"),
                ("/blog/family-friendly-activities-gulf-cities.html", "Family Activities in Gulf Cities", "أنشطة أسرية في مدن الخليج"),
            ]),
            ("Go deeper", "تعمّق أكثر", [
                ("/library.html?cat=travel", "All travel tools in Library", "كل أدوات السفر في المكتبة"),
                ("/blog/makkah-hotels-guide-en.html", "Makkah Hotels Guide", "دليل فنادق مكة"),
                ("/blog.html", "Browse the blog", "تصفّح المدونة"),
            ]),
        ],
    )
    faqs = [
        ("How do I plan an Umrah trip with your tools?", "كيف أخطّط لعمرة بأدواتكم؟",
         "Use Travel Budget for costs, Packing Checklist for bags, and Prayer Times plus Qibla while traveling. Complete official Umrah bookings and permits on Nusuk, the official platform  -  our tools support planning, they do not replace Nusuk.",
         "استخدم ميزانية السفر للتكاليف وقائمة الحقائب للشنط ومواقيت الصلاة والقبلة أثناء السفر. أكمل حجوزات وتصاريح العمرة الرسمية عبر نُسُك  -  أدواتنا تدعم التخطيط ولا تستبدل نُسُك."),
        ("Which travel tool should I open first?", "أي أداة سفر أفتح أولاً؟",
         "Start with Travel Budget if money is the bottleneck. Packing next. If you are already on the road, open Prayer Times or Qibla. Need FX? Use Currency Converter.",
         "ابدأ بميزانية السفر إن كان المال هو العائق. ثم الحقائب. إن كنت في الطريق افتح مواقيت الصلاة أو القبلة. تحتاج صرف؟ استخدم محول العملات."),
        ("Are travel tools free and private?", "هل أدوات السفر مجانية وخاصة؟",
         "Yes. They run in your browser and do not store your trip details or personal data.",
         "نعم. تعمل في متصفحك ولا تخزّن تفاصيل رحلتك أو بياناتك الشخصية."),
        ("Do you book hotels or Umrah packages?", "هل تحجزون فنادق أو باقات عمرة؟",
         "No. We publish planning tools and guides. Book stays and Umrah services through official or licensed providers, including Nusuk where required.",
         "لا. ننشر أدوات وأدلة تخطيط. احجز الإقامة وخدمات العمرة عبر مزوّدين رسميين أو مرخّصين، بما فيها نُسُك حيث يلزم."),
        ("Can families traveling with kids use these tools?", "هل تناسب هذه الأدوات الأسر المسافرة مع أطفال؟",
         "Yes. Pair the budget and packing tools with family guides such as Umrah with kids and Gulf city activities linked on this page.",
         "نعم. اجمع أدوات الميزانية والحقائب مع أدلة أسرية مثل العمرة مع الأطفال وأنشطة مدن الخليج المرتبطة في هذه الصفحة."),
        ("Where can I read deeper travel guides?", "أين أقرأ أدلة سفر أعمق؟",
         "See Makkah and Madinah, Salalah, Saudi tourism, Umrah packing, and family activity guides in the section above.",
         "راجع أدلة مكة والمدينة وصلالة والسياحة السعودية وحقائب العمرة والأنشطة الأسرية في القسم أعلاه."),
    ]
    faq = faq_section("Questions about this travel hub", "أسئلة عن محور السفر", faqs)
    return "\n\n".join([trust, chooser, tools, guides, faq]), faqs


def build_islamic() -> tuple[str, list]:
    trust = trust_section(
        [
            ("Educ.", "Not a fatwa service", "ليست خدمة فتوى"),
            ("Daily", "Prayer · Qibla · Hijri", "صلاة · قبلة · هجري"),
            ("Private", "Runs in your browser", "يعمل في متصفحك"),
            ("Family", "Gulf family life", "حياة الأسرة الخليجية"),
        ],
        "Educational Islamic lifestyle tools  -  confirm rulings with a qualified scholar when needed.",
        "أدوات نمط حياة إسلامي تعليمية  -  أكّد الأحكام مع عالم مؤهّل عند الحاجة.",
    )
    chooser = chooser_section([
        chooser_card("/tools/prayer-times.html", "I need today's prayer times", "أحتاج مواقيت صلاة اليوم", "Prayer Times →", "مواقيت الصلاة →", ICON["prayer"]),
        chooser_card("/tools/zakat-calculator.html", "I need to calculate Zakat", "أحتاج حساب الزكاة", "Zakat Calculator →", "حاسبة الزكاة →", ICON["zakat"]),
        chooser_card("/tools/inheritance-calculator.html", "I want inheritance basics", "أبي أساسيات الميراث", "Inheritance →", "الميراث →", ICON["inherit"]),
        chooser_card("/tools/qibla.html", "I need the Qibla", "أحتاج القبلة", "Qibla Finder →", "اتجاه القبلة →", ICON["qibla"]),
        chooser_card("/tools/hijri-converter.html", "I need a Hijri date", "أحتاج تاريخاً هجرياً", "Hijri Converter →", "المحوّل الهجري →", ICON["hijri"]),
        chooser_card("/tools/ramadan-calorie-calculator.html", "I am planning Ramadan meals", "أخطّط لوجبات رمضان", "Ramadan Calories →", "سعرات رمضان →", ICON["prayer"]),
    ])
    tools = tools_section(
        "Islamic tools",
        "All Islamic tools in one place",
        "كل الأدوات الإسلامية في مكان واحد",
        [
            ("Daily worship", "العبادة اليومية", [
                tool_card("/tools/prayer-times.html", "Prayer Times", "مواقيت الصلاة",
                          "Accurate prayer times for your city  -  essential for daily family rhythm.",
                          "مواقيت صلاة دقيقة لمدينتك  -  أساس إيقاع الأسرة اليومي.",
                          ICON["prayer"], badge=("Daily", "يومي"), featured=True),
                tool_card("/tools/qibla.html", "Qibla Finder", "اتجاه القبلة",
                          "Find the Qibla direction at home or while traveling.",
                          "اعرف اتجاه القبلة في المنزل أو أثناء السفر.",
                          ICON["qibla"], accent="#0a6b63"),
                tool_card("/tools/hijri-converter.html", "Hijri Converter", "المحوّل الهجري",
                          "Convert between Hijri and Gregorian dates for planning and occasions.",
                          "حوّل بين الهجري والميلادي للتخطيط والمناسبات.",
                          ICON["hijri"], accent="#4a8a82"),
            ]),
            ("Zakat & inheritance", "الزكاة والميراث", [
                tool_card("/tools/zakat-calculator.html", "Zakat Calculator", "حاسبة الزكاة",
                          "Estimate Zakat on common assets with current nisab values  -  educational aid.",
                          "قدّر الزكاة على أصول شائعة بقيم النصاب الحالية  -  مساعدة تعليمية.",
                          ICON["zakat"], badge=("Obligation", "فريضة")),
                tool_card("/tools/inheritance-calculator.html", "Inheritance Calculator", "حاسبة الميراث",
                          "Explore basic Islamic inheritance shares for common family scenarios.",
                          "استكشف حصص الميراث الإسلامية الأساسية لسيناريوهات أسرية شائعة.",
                          ICON["inherit"], accent="#0a6b63"),
            ]),
            ("Ramadan & calendar", "رمضان والتقويم", [
                tool_card("/tools/ramadan-calorie-calculator.html", "Ramadan Calorie Calculator", "حاسبة سعرات رمضان",
                          "Plan Suhoor and Iftar nutrition while fasting.",
                          "خطّط تغذية السحور والإفطار أثناء الصيام.",
                          ICON["prayer"], accent="#3a9d8e"),
            ]),
        ],
    )
    guides = guides_section(
        "Explore Islamic Life",
        "استكشف الحياة الإسلامية",
        [
            ("Ramadan & worship", "رمضان والعبادة", [
                ("/blog/ramadan-preparation-guide-families.html", "Ramadan Preparation for Families", "التحضير لرمضان للأسر"),
                ("/islamic-hajj-umrah/daily-adhkar-family-guide.html", "Daily Adhkar Family Guide", "دليل الأذكار اليومية للأسرة"),
                ("/islamic-hajj-umrah/teaching-children-prayer-with-love.html", "Teaching Children Prayer with Love", "تعليم الأطفال الصلاة بمحبة"),
            ]),
            ("Umrah & sacred cities", "العمرة والمدن المقدسة", [
                ("/blog/umrah-budget-guide-families.html", "Umrah Budget for Families", "ميزانية العمرة للأسر"),
                ("/guides/mecca-medina.html", "Makkah & Madinah Guide", "دليل مكة والمدينة"),
                ("/blog/makkah-hotels-guide-en.html", "Makkah Hotels Guide", "دليل فنادق مكة"),
            ]),
            ("Zakat & learning", "الزكاة والتعلّم", [
                ("/blog/zakat-calculator-modern-investments-guide.html", "Zakat on Modern Investments", "زكاة الاستثمارات الحديثة"),
                ("/library.html?cat=islamic", "All Islamic tools in Library", "كل الأدوات الإسلامية في المكتبة"),
                ("/blog.html", "Browse the blog", "تصفّح المدونة"),
            ]),
        ],
    )
    faqs = [
        ("Which Islamic tool should I start with?", "أي أداة إسلامية أبدأ بها؟",
         "For daily use, open Prayer Times. Paying Zakat? Use the Zakat Calculator. Exploring inheritance shares? Open Inheritance. Traveling? Add Qibla. Planning Ramadan meals? Use the Ramadan calorie tool.",
         "للاستخدام اليومي افتح مواقيت الصلاة. تدفع زكاة؟ استخدم حاسبة الزكاة. تستكشف حصص الميراث؟ افتح الميراث. مسافر؟ أضف القبلة. تخطّط لوجبات رمضان؟ استخدم حاسبة سعرات رمضان."),
        ("Does the Zakat calculator support all four madhhabs?", "هل حاسبة الزكاة تدعم المذاهب الأربعة؟",
         "Not as separate madhhab modes yet. The current calculator uses common educational defaults for nisab and asset types. Explicit Hanafi, Maliki, Shafi'i, and Hanbali options are under study. For disputed cases, ask a qualified scholar.",
         "ليس كأوضاع مذاهب منفصلة بعد. الحاسبة الحالية تستخدم افتراضات تعليمية شائعة للنصاب وأنواع الأصول. خيارات صريحة للحنفية والمالكية والشافعية والحنابلة قيد الدراسة. للحالات المختلف فيها اسأل عالماً مؤهّلاً."),
        ("Are these tools a fatwa or religious ruling?", "هل هذه الأدوات فتوى أو حكم شرعي؟",
         "No. They are educational aids for planning and learning. Confirm personal rulings with a qualified scholar or trusted local authority.",
         "لا. هي مساعدات تعليمية للتخطيط والتعلّم. أكّد الأحكام الشخصية مع عالم مؤهّل أو جهة محلية موثوقة."),
        ("Are Islamic tools free and private?", "هل الأدوات الإسلامية مجانية وخاصة؟",
         "Yes. Calculations and lookups run in your browser. We do not store your personal worship or wealth figures.",
         "نعم. الحسابات والاستعلامات تعمل في متصفحك. لا نخزّن أرقام عبادتك أو ثروتك الشخصية."),
        ("Can I use these tools while traveling for Umrah?", "هل أستخدم هذه الأدوات أثناء السفر للعمرة؟",
         "Yes. Prayer Times and Qibla are especially useful on the road. Pair them with travel budget and packing tools on the Travel hub, and complete official Umrah steps on Nusuk.",
         "نعم. مواقيت الصلاة والقبلة مفيدتان جداً في الطريق. اجمعهما مع ميزانية السفر والحقائب في محور السفر، وأكمل خطوات العمرة الرسمية عبر نُسُك."),
        ("Where can I read deeper Islamic guides?", "أين أقرأ أدلة إسلامية أعمق؟",
         "See Ramadan preparation, daily adhkar, teaching children prayer, Umrah budget, Makkah and Madinah, and Zakat on modern investments in the guides section above.",
         "راجع التحضير لرمضان والأذكار اليومية وتعليم الصلاة وميزانية العمرة ومكة والمدينة وزكاة الاستثمارات الحديثة في قسم الأدلة أعلاه."),
    ]
    faq = faq_section("Questions about this Islamic hub", "أسئلة عن المحور الإسلامي", faqs)
    return "\n\n".join([trust, chooser, tools, guides, faq]), faqs


HUBS = {
    "finance": build_finance,
    "real-estate": build_real_estate,
    "travel": build_travel,
    "islamic": build_islamic,
}


def append_hub_css(hub: str) -> None:
    src = (ROOT / "styles/pages/health-hub.css").read_text()
    m = re.search(r"/\* ═══ 2026-07-10 hub quality uplift.*", src, re.S)
    if not m:
        raise SystemExit("uplift CSS block missing in health-hub.css")
    block = m.group(0).replace("body.health-hub-page", f"body.{hub}-hub-page")
    block = block.replace("[data-lang=\"ar\"] body.health-hub-page", f"[data-lang=\"ar\"] body.{hub}-hub-page")
    # dark theme selectors already rewritten by body.health-hub-page replace
    css_path = ROOT / f"styles/pages/{hub}-hub.css"
    css = css_path.read_text()
    if "2026-07-10 hub quality uplift" in css:
        css = re.sub(r"/\* ═══ 2026-07-10 hub quality uplift.*", block.rstrip() + "\n", css, flags=re.S)
    else:
        css = css.rstrip() + "\n\n" + block.rstrip() + "\n"
    css_path.write_text(css)


def uplift_html(hub: str) -> None:
    path = ROOT / f"{hub}.html"
    html = path.read_text()
    middle, faqs = HUBS[hub]()

    # Sub-nav
    html = re.sub(r'<div id="sub-nav">.*?</div>\s*</div>', SUBNAV, html, count=1, flags=re.S)

    # Replace from tools section through guides section (before latest-articles)
    m = re.search(
        r'(<section[^>]*id="tools"[^>]*>.*?)(<section[^>]*id="latest-articles"[^>]*>)',
        html,
        re.S,
    )
    if not m:
        raise SystemExit(f"{hub}: could not find tools→latest-articles span")

    html = html[: m.start(1)] + middle + "\n\n    " + html[m.start(2) :]

    # FAQ JSON-LD
    html = re.sub(
        r'<script type="application/ld\+json">\{"@context":"https://schema\.org","@type":"FAQPage".*?</script>\s*',
        "",
        html,
        flags=re.S,
    )
    html = html.replace("</head>", faq_jsonld(faqs) + "\n</head>", 1)

    # CSS version bump
    html = re.sub(
        rf'/styles/pages/{hub}-hub\.css\?v=[^"]+',
        f"/styles/pages/{hub}-hub.css?v=20260710a",
        html,
    )

    # Soften em-dashes in newly inserted middle only is already avoided; scrub any leftover in middle
    path.write_text(html)
    print(f"updated {hub}.html")


def main() -> None:
    for hub in HUBS:
        append_hub_css(hub)
        uplift_html(hub)

    # Verify tool duplication
    for hub in HUBS:
        t = (ROOT / f"{hub}.html").read_text()
        body = t.split("<body", 1)[1]
        tools = re.findall(r'href="(/tools/[^"#]+)"', body)
        from collections import Counter

        c = Counter(tools)
        dups = {u: n for u, n in c.items() if n > 2}
        print(f"{hub}: unique_tools={len(c)} over2={dups or 'none'}")


if __name__ == "__main__":
    main()
