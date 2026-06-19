#!/usr/bin/env python3
"""Build flagship finance tool pages from backups + shared shell."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
BACKUP = TOOLS / "_finance_backup"
sys.path.insert(0, str(TOOLS))
import _gen_finance_flagship as gen  # noqa: E402

BFC = (ROOT / "tools/body-fat-calculator.html").read_text(encoding="utf-8")
FOOTER_FULL = BFC[BFC.index('<footer class="site-footer"'):BFC.index('</footer>') + len('</footer>')]
_mnav = BFC.index('<nav class="dfl-mobile-nav"')
_mend = BFC.index('<script src="/scripts/global.js?v=20260618a" defer></script>', _mnav)
MOBILE_FULL = BFC[_mnav:_mend]


def read_backup(name):
    p = BACKUP / f"{name}.html"
    if not p.exists():
        p = TOOLS / f"{name}.html"
    return p.read_text(encoding="utf-8")


def extract_script(src, *markers):
    """Extract calculation JS, stripping platform bloat."""
    for m in markers:
        idx = src.find(m)
        if idx == -1:
            continue
        rest = src[idx:]
        end = rest.find('</script>')
        if end == -1:
            continue
        js = rest[:end]
        for cut in [
            '// ── SCROLL REVEAL', 'const ro=new IntersectionObserver',
            'const revealObserver', '/* ── Phase 2A Global',
            'function injectSearchStyles', 'function toggleTheme()',
            'function toggleLang()', 'window.addEventListener(\'scroll\'',
            'document.getElementById(\'theme-icon\')',
            'document.getElementById(\'theme-btn\')',
            'document.getElementById(\'lang-btn\')',
        ]:
            if cut in js:
                js = js[:js.index(cut)]
        js = js.replace('.faq-q', '.t-faq-q')
        js = js.replace('.mf-q', '.t-faq-q')
        js = js.replace('.rf-q', '.t-faq-q')
        js = js.replace('.ic-faq-q', '.t-faq-q')
        js = re.sub(r'document\.addEventListener\(\'DOMContentLoaded\'\(\)=>\{[^}]*theme-btn[^}]*\}\);?\n?', '', js)
        js = re.sub(r'document\.addEventListener\(\'DOMContentLoaded\',function\(\)\{[^}]*theme-btn[^}]*\}\);?\n?', '', js)
        return js.strip()
    # fallback: last script with function calculate
    scripts = re.findall(r'<script>\s*(function [\s\S]*?)</script>', src)
    for s in reversed(scripts):
        if 'function calculate' in s or 'function calcROI' in s or 'function calculateMortgage' in s or 'function calculateYield' in s:
            return extract_script(f'<script>{s}</script>', 'function ')
    return ''


def extract_between(src, start, end):
    s = src.index(start)
    e = src.index(end, s)
    return src[s:e].strip()


def faq_section(items):
    parts = ['<div class="tool-below">', '<div class="t-faq">',
             '<div class="t-faq-label"><span class="en">FAQ</span><span class="ar">أسئلة شائعة</span></div>',
             '<div class="t-faq-title"><span class="en">Frequently Asked Questions</span><span class="ar">الأسئلة المتكررة</span></div>']
    for qen, qar, aen, aar in items:
        parts.append(f'''<div class="t-faq-item"><div class="t-faq-q" onclick="toggleFAQ(this)"><span><span class="en">{qen}</span><span class="ar">{qar}</span></span><span class="t-faq-arrow">▼</span></div><div class="t-faq-a"><p><span class="en">{aen}</span><span class="ar">{aar}</span></p></div></div>''')
    parts += ['</div></div>']
    return '\n'.join(parts)


def method_section(en, ar):
    return f'''<div class="tool-below"><div class="t-section"><div class="t-section-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/></svg> <span class="en">How this works</span><span class="ar">كيف تعمل</span></div><p class="en">{en}</p><p class="ar">{ar}</p></div>'''


def assemble_page(meta, main, below, rail, js, init=''):
    lang = '''document.addEventListener('dfl:langchange',function(){
  if(typeof calcROI==='function'&&document.getElementById('resultsWrap')&&document.getElementById('resultsWrap').classList.contains('show'))calcROI();
  if(typeof calculateYield==='function'&&document.getElementById('results-section')&&document.getElementById('results-section').classList.contains('active'))calculateYield();
  if(typeof calculateMortgage==='function'&&document.getElementById('results-section')&&document.getElementById('results-section').classList.contains('active')){if(typeof renderAmortTable==='function'&&typeof fullAmortData!=='undefined'&&fullAmortData&&fullAmortData.length)renderAmortTable(typeof showingAll!=='undefined'&&showingAll);}
  if(typeof calculate==='function'&&document.getElementById('result-card'))calculate(true);
  if(typeof calculate==='function'&&document.getElementById('results-body')&&document.getElementById('results-body').querySelector('.heir-result'))calculate();
  if(typeof autoCalculate==='function'&&document.getElementById('resultFilled')&&document.getElementById('resultFilled').style.display!=='none')calculate();
  if(typeof buildCatList==='function')buildCatList();
});'''
    if 'function toggleFAQ' not in js:
        js += '''
function toggleFAQ(el){
  var answer=el.nextElementSibling;var isOpen=el.classList.contains('open');
  document.querySelectorAll('.t-faq-q').forEach(function(q){q.classList.remove('open');q.nextElementSibling.classList.remove('active');});
  if(!isOpen){el.classList.add('open');answer.classList.add('active');}
}'''
    body = gen.hero(meta) + '\n'
    body += f'<main class="tool-mn">\n{main}\n\n{below}\n\n{rail}\n</main>\n\n'
    body += FOOTER_FULL + '\n\n' + MOBILE_FULL + '\n'
    body += '<script src="/scripts/global.js?v=20260618a" defer></script>\n'
    body += f'<script>\n{js}\n{init}\n{lang}\n</script>\n</body></html>'
    return gen.head(meta) + body


def build_salary():
    html = read_backup('salary-calculator')
    return html.replace(
        "document.addEventListener('dfl:langchange',function(){});",
        "document.addEventListener('dfl:langchange',function(){calculate(true);});",
    )


def build_savings():
    src = read_backup('savings-goal')
    js = extract_script(src, 'function fmt(n)')
    js = js.replace("document.getElementById('result-card').style.display='block';\n  document.getElementById('result-card').scrollIntoView",
                    "document.getElementById('result-card').classList.add('active')")
    js = js.replace("document.getElementById('result-card').style.display='block'", "document.getElementById('result-card').classList.add('active')")
    meta = dict(slug='savings-goal', data_tool='savings-goal',
        title='Savings Goal Calculator | حاسبة هدف الادخار — Dot For Life',
        desc='Plan how long to reach your savings goal or how much to save monthly. Bilingual, free, private.',
        og_title='Savings Goal Calculator | Dot4Life', og_desc='Plan your savings goal with time or monthly contribution modes.',
        schema_name='Savings Goal Calculator',
        bc_en='Savings Goal', bc_ar='هدف الادخار',
        eyebrow_en='Finance Tool · Planning', eyebrow_ar='أداة مالية · التخطيط',
        h1_en='Savings Goal Calculator', h1_ar='حاسبة هدف الادخار',
        desc_en='Enter your target, current savings, and monthly contribution — or set a timeframe.',
        desc_ar='أدخل هدفك ومدخراتك الحالية ومساهمتك الشهرية — أو حدد إطاراً زمنياً.',
        trust='<li><span class="en">Two modes</span><span class="ar">وضعان</span></li><li><span class="en">Progress bar</span><span class="ar">شريط التقدم</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li>')
    main = '''<div class="tool-workspace">
  <div class="tool-panel sg-card"><div class="tool-panel-hdr"><h2><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/></svg> <span class="en">Your Goal</span><span class="ar">هدفك</span></h2><p><span class="en">Results update as you type.</span><span class="ar">النتائج تتحدث أثناء الكتابة.</span></p></div>
  <div class="tool-panel-body t-body"><div class="t-g2">
    <div class="t-fl"><label class="t-fl-l" for="target"><span class="en">Target Amount</span><span class="ar">المبلغ المستهدف</span></label><div class="t-fl-r"><input type="number" id="target" value="50000" min="0"><span class="t-fl-u">SAR</span></div></div>
    <div class="t-fl"><label class="t-fl-l" for="current"><span class="en">Current Savings</span><span class="ar">المدخرات الحالية</span></label><div class="t-fl-r"><input type="number" id="current" value="5000" min="0"><span class="t-fl-u">SAR</span></div></div>
    <div class="t-fl"><label class="t-fl-l" for="monthly"><span class="en">Monthly Contribution</span><span class="ar">المساهمة الشهرية</span></label><div class="t-fl-r"><input type="number" id="monthly" value="2000" min="1"><span class="t-fl-u">SAR</span></div></div>
    <div class="t-fl"><label class="t-fl-l" for="months"><span class="en">Or — Timeframe (months)</span><span class="ar">أو — الإطار الزمني (أشهر)</span></label><div class="t-fl-r"><input type="number" id="months" value="24" min="1"><span class="t-fl-u"><span class="en">mo</span><span class="ar">شهر</span></span></div></div>
  </div><button class="t-btn" type="button" onclick="calculate()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg><span class="en">Calculate</span><span class="ar">احسب</span></button></div></div>
  <div class="tool-panel sg-card" id="result-card"><div class="tool-panel-hdr"><h2><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg> <span class="en">Results</span><span class="ar">النتائج</span></h2></div>
  <div class="tool-panel-body t-body"><div class="sg-res-grid">
    <div class="sg-res-box sg-primary"><div class="sg-res-label"><span class="en">Remaining to Save</span><span class="ar">المتبقي للادخار</span></div><div class="sg-res-value" id="res-remaining">—</div></div>
    <div class="sg-res-box"><div class="sg-res-label"><span class="en">Target Amount</span><span class="ar">المبلغ المستهدف</span></div><div class="sg-res-value" id="res-target">—</div></div>
    <div class="sg-res-box"><div class="sg-res-label"><span class="en">Current Savings</span><span class="ar">المدخرات الحالية</span></div><div class="sg-res-value" id="res-current">—</div></div>
    <div class="sg-res-box"><div class="sg-res-label"><span class="en">Monthly Contribution</span><span class="ar">المساهمة الشهرية</span></div><div class="sg-res-value" id="res-monthly">—</div></div>
    <div class="sg-res-box"><div class="sg-res-label"><span class="en">Time Needed</span><span class="ar">الوقت المطلوب</span></div><div class="sg-res-value" id="res-time">—</div></div>
  </div><div class="sg-progress-wrap"><div class="sg-progress-label"><span><span class="en">Progress</span><span class="ar">التقدم</span></span><span id="res-progress-pct">0%</span></div><div class="sg-progress-bg"><div class="sg-progress-fill" id="res-progress" style="width:0%"></div></div></div></div></div>
</div>'''
    below = method_section('Mode 1: enter target, current savings, and monthly contribution to see time needed. Mode 2: enter a timeframe to see required monthly savings. Simple savings without interest.',
                           'الوضع 1: أدخل الهدف والمدخرات والمساهمة الشهرية. الوضع 2: أدخل الإطار الزمني. ادخار بسيط بدون فوائد.') + faq_section([
        ('Does this include interest?', 'هل تشمل الفوائد?', 'No. Simple savings without interest, returns, or inflation.', 'لا. ادخار بسيط بدون فوائد أو عوائد أو تضخم.')])
    rail = gen.tickets(gen.ticket('/tools/monthly-budget.html','tool-ticket--budget','Finance','مالية','Monthly Budget','الميزانية الشهرية','Plan spending.','خطط مصروفك.')+gen.ticket('/tools/salary-calculator.html','tool-ticket--salary','Finance','مالية','Salary Calculator','حاسبة الراتب','Know net pay.','اعرف صافي راتبك.'))
    init = "document.addEventListener('DOMContentLoaded',function(){['target','current','monthly','months'].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener('input',calculate);});calculate();});"
    return assemble_page(meta, main, below, rail, js, init)


def build_mortgage():
    src = read_backup('mortgage-calculator')
    js = extract_script(src, '// ── SLIDER SYNC', 'function syncSlider')
    main_body = extract_between(src, '<!-- MO-GRID', '<!-- MM-CARD: Method Note')
    main = f'<div class="tool-workspace">\n{main_body}\n</div>'
    below = extract_between(src, '<!-- MM-CARD: Method Note -->', '<!-- MF-SECTION: FAQ -->')
    below = below.replace('mm-card tool-rv tool-rv-3', 't-section').replace('mm-icon', 't-section-label').replace('mm-content', '')
    below += faq_section([
        ('How is the monthly mortgage payment calculated?', 'كيف يُحسب القسط الشهري؟', 'Monthly payment uses the standard PMT formula: P × [r(1+r)^n] / [(1+r)^n − 1].', 'القسط الشهري بمعادلة PMT القياسية.'),
        ('What is REDF and who is eligible?', 'ما هو صندوق التنمية العقاري؟', 'REDF offers interest-free loans up to SAR 500,000 for eligible Saudi first-time buyers.', 'يقدم الصندوق قروضاً بدون فائدة حتى 500,000 ريال للمواطنين المؤهلين.'),
        ('What is the maximum mortgage term?', 'ما أقصى مدة للتمويل؟', 'Most Saudi banks offer 25–30 year terms.', 'معظم البنوك تقدم 25-30 سنة.'),
        ('What is the minimum down payment?', 'ما الدفعة الأولى الدنيا؟', 'SAMA requires 10% minimum for first-time buyers, 20% for subsequent purchases.', 'تشترط ساما 10% للمشتري لأول مرة و20% للاحق.'),
    ])
    meta = dict(slug='mortgage-calculator', data_tool='mortgage-calculator',
        title='Saudi Mortgage Calculator | حاسبة التمويل العقاري — Dot For Life',
        desc='Calculate monthly mortgage payments, total interest, amortization schedule, and REDF support. Saudi bank rate presets.',
        og_title='Saudi Mortgage Calculator | Dot4Life', og_desc='Monthly payments, amortization, REDF support, Saudi bank presets.',
        schema_name='Saudi Mortgage Calculator',
        bc_en='Mortgage Calculator', bc_ar='حاسبة التمويل',
        eyebrow_en='Finance Tool · Real Estate', eyebrow_ar='أداة مالية · عقار',
        h1_en='Saudi Mortgage Calculator', h1_ar='حاسبة التمويل العقاري',
        desc_en='Calculate monthly payments, total interest, and full amortization. Includes REDF support and Saudi bank rate presets.',
        desc_ar='احسب القسط الشهري وإجمالي الفائدة وجدول السداد. يشمل دعم الصندوق وأسعار البنوك.',
        trust='<li><span class="en">REDF support</span><span class="ar">دعم الصندوق</span></li><li><span class="en">Bank presets</span><span class="ar">أسعار البنوك</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li>')
    rail = gen.tickets(gen.ticket('/tools/rental-yield-calculator.html','tool-ticket--yield','Finance','مالية','Rental Yield','العائد الإيجاري','Gross & net yield.','العائد الإجمالي والصافي.')+gen.ticket('/tools/roi-calculator.html','tool-ticket--roi','Finance','مالية','ROI Calculator','حاسبة العائد','Full property ROI.','عائد الاستثمار الكامل.')+gen.ticket('/tools/salary-calculator.html','tool-ticket--salary','Finance','مالية','Salary Calculator','حاسبة الراتب','Affordability check.','تحقق من القدرة.'))
    init = "document.addEventListener('DOMContentLoaded',function(){['property-price','down-pct','loan-amount','interest-rate','loan-term','redf-amount','redf-term'].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener('input',function(){if(typeof syncDownPayment==='function'&&(id==='property-price'||id==='down-pct'))syncDownPayment();});});});"
    return assemble_page(meta, main, below, rail, js, init)


def build_budget():
    src = read_backup('monthly-budget')
    js = extract_script(src, '/* ─── STATE ─', 'var currCode')
    main_inputs = extract_between(src, '<!-- LEFT: INPUTS -->', '<!-- RIGHT: RESULTS -->')
    main_results = extract_between(src, '<!-- RIGHT: RESULTS -->', '</div><!-- /tool-grid -->')
    main = f'''<div class="tool-workspace tool-grid-budget">
  <div class="tool-panel mb-card">{main_inputs.replace('<div>', '<div class="tool-panel-body t-body">', 1)}</div>
  {main_results.replace('result-panel', 'tool-panel mb-card result-panel')}
</div>'''
    below = method_section('Enter net monthly income and expenses by category. See surplus/deficit, category breakdown, and 50/30/20 or Islamic finance guidance.',
                           'أدخل الدخل الصافي والنفقات حسب الفئة. شاهد الفائض/العجز وتفصيل الفئات وإرشادات 50/30/20 أو التمويل الإسلامي.')
    rail = gen.tickets(gen.ticket('/tools/savings-goal.html','tool-ticket--savings','Finance','مالية','Savings Goal','هدف الادخار','Turn surplus into a plan.','حوّل الفائض لخطة.')+gen.ticket('/tools/mortgage-calculator.html','tool-ticket--mortgage','Finance','مالية','Mortgage','التمويل','Fit a home loan.','تمويل يناسبك.')+gen.ticket('/tools/zakat-calculator.html','tool-ticket--zakat','Finance','مالية','Zakat','الزكاة','Annual obligation.','الزكاة السنوية.'))
    meta = dict(slug='monthly-budget', data_tool='monthly-budget',
        title='Monthly Budget Planner | مخطط الميزانية الشهرية — Dot For Life',
        desc='Plan your monthly budget with income, expense categories, surplus tracking, and 50/30/20 or Islamic finance guidance.',
        og_title='Monthly Budget Planner | Dot4Life', og_desc='Track income, expenses, surplus, and budgeting rules.',
        schema_name='Monthly Budget Planner',
        bc_en='Monthly Budget', bc_ar='الميزانية الشهرية',
        eyebrow_en='Finance Tool · Planning', eyebrow_ar='أداة مالية · التخطيط',
        h1_en='Monthly Budget Planner', h1_ar='مخطط الميزانية الشهرية',
        desc_en='Enter income and expenses by category. Instant surplus or deficit with 50/30/20 or halal finance guidance.',
        desc_ar='أدخل الدخل والنفقات حسب الفئة. فائض أو عجز فوري مع إرشادات 50/30/20 أو التمويل الحلال.',
        trust='<li><span class="en">9 categories</span><span class="ar">9 فئات</span></li><li><span class="en">Halal mode</span><span class="ar">وضع حلال</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li>')
    init = "document.addEventListener('DOMContentLoaded',function(){buildCatList();});"
    return assemble_page(meta, main, below, rail, js, init)


def build_roi():
    src = read_backup('roi-calculator')
    js = extract_script(src, 'function v(id)', 'function calcROI')
    form = extract_between(src, '<div class="tool-cd tool-rv tool-rv-1">', '<!-- RESULTS -->')
    results = extract_between(src, '<!-- RESULTS -->', '<div class="related-grid reveal rd2">')
    main = f'<div class="tool-workspace"><div class="tool-panel roi-card">{form}</div>{results}</div>'
    below = method_section('ROI includes rental income and appreciation minus transfer fees, service costs, and mortgage payments. Compared against stocks, REITs, deposits, and sukuk.',
                           'العائد يشمل الإيجار والتقدير ناقص الرسوم والتكاليف والتمويل. مع مقارنة بالأسهم والصناديق والودائع والصكوك.')
    meta = dict(slug='roi-calculator', data_tool='roi-calculator',
        title='Real Estate ROI Calculator | حاسبة العائد على الاستثمار — Dot For Life',
        desc='Calculate real estate ROI with Saudi-specific costs, rental income, appreciation, and investment comparisons.',
        og_title='Real Estate ROI Calculator | Dot4Life', og_desc='Full property ROI with Saudi fees and alternatives.',
        schema_name='Real Estate ROI Calculator',
        bc_en='ROI Calculator', bc_ar='حاسبة العائد',
        eyebrow_en='Finance Tool · Real Estate', eyebrow_ar='أداة مالية · عقار',
        h1_en='Real Estate ROI Calculator', h1_ar='حاسبة العائد على الاستثمار العقاري',
        desc_en='Calculate gross and net yield, cash-on-cash return, and 10-year total return with Saudi market costs.',
        desc_ar='احسب العائد الإجمالي والصافي والعائد على رأس المال وإجمالي 10 سنوات بتكاليف السوق السعودي.',
        trust='<li><span class="en">Saudi fees</span><span class="ar">رسوم سعودية</span></li><li><span class="en">10yr projection</span><span class="ar">توقع 10 سنوات</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li>')
    rail = gen.tickets(gen.ticket('/tools/mortgage-calculator.html','tool-ticket--mortgage','Finance','مالية','Mortgage','التمويل','Monthly payments.','الأقساط الشهرية.')+gen.ticket('/tools/rental-yield-calculator.html','tool-ticket--yield','Finance','مالية','Rental Yield','العائد الإيجاري','Yield analysis.','تحليل العائد.')+gen.ticket('/tools/zakat-calculator.html','tool-ticket--zakat','Finance','مالية','Zakat','الزكاة','On rental assets.','على أصول الإيجار.'))
    init = "document.addEventListener('DOMContentLoaded',function(){['purchasePrice','downPayment','annualRent','occupancy','maintenance','serviceFees','mortgageMonthly','appreciation'].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener('input',function(){if(document.getElementById('resultsWrap').classList.contains('show'))calcROI();});});});"
    return assemble_page(meta, main, below, rail, js, init)


def build_rental_yield():
    src = read_backup('rental-yield-calculator')
    js = extract_script(src, 'function fmt(n){ return Math.round', 'function calculateYield')
    main_body = extract_between(src, '<!-- RY-GRID', '<!-- RM-CARD: Method Note')
    main = f'<div class="tool-workspace">\n{main_body}\n</div>'
    below = method_section('Gross yield = annual rent ÷ property value. Net yield uses effective gross income minus vacancy and operating expenses (RICS-style).',
                           'العائد الإجمالي = الإيجار السنوي ÷ قيمة العقار. الصافي بعد الشغور والنفقات التشغيلية.')
    meta = dict(slug='rental-yield-calculator', data_tool='rental-yield-calculator',
        title='Rental Yield Calculator | حاسبة العائد الإيجاري — Dot For Life',
        desc='Calculate gross and net rental yield with vacancy, expenses, and property comparison for Saudi real estate.',
        og_title='Rental Yield Calculator | Dot4Life', og_desc='Gross & net yield with expense breakdown.',
        schema_name='Rental Yield Calculator',
        bc_en='Rental Yield', bc_ar='العائد الإيجاري',
        eyebrow_en='Finance Tool · Real Estate', eyebrow_ar='أداة مالية · عقار',
        h1_en='Rental Yield Calculator', h1_ar='حاسبة العائد الإيجاري',
        desc_en='Calculate gross and net rental yield with vacancy days, operating expenses, and compare up to 3 properties.',
        desc_ar='احسب العائد الإجمالي والصافي مع أيام الشغور والنفقات وقارن حتى 3 عقارات.',
        trust='<li><span class="en">RICS method</span><span class="ar">طريقة RICS</span></li><li><span class="en">Compare 3</span><span class="ar">قارن 3</span></li><li><span class="en">Free &amp; private</span><span class="ar">مجاني وخاص</span></li>')
    rail = gen.tickets(gen.ticket('/tools/roi-calculator.html','tool-ticket--roi','Finance','مالية','ROI Calculator','حاسبة العائد','Full investment ROI.','عائد الاستثمار الكامل.')+gen.ticket('/tools/mortgage-calculator.html','tool-ticket--mortgage','Finance','مالية','Mortgage','التمويل','Finance your purchase.','موّل شراءك.')+gen.ticket('/tools/inheritance-calculator.html','tool-ticket--inheritance','Islamic','إسلامية','Inheritance','الميراث','Estate planning.','تخطيط التركة.'))
    init = "document.addEventListener('DOMContentLoaded',function(){['prop-value','monthly-rent','vacancy-days','exp-maintenance','exp-management','exp-tax','exp-insurance','exp-utilities','exp-other'].forEach(function(id){var el=document.getElementById(id);if(el)el.addEventListener('input',function(){if(document.getElementById('results-section').classList.contains('active'))calculateYield();});});});"
    return assemble_page(meta, main, below, rail, js, init)


def build_inheritance():
    src = read_backup('inheritance-calculator')
    js = extract_script(src, 'var heirs = {')
    main_body = extract_between(src, '<!-- IN-GRID', '<!-- IM-CARD: Method Note')
    main = f'<div class="tool-workspace">\n{main_body}\n</div>'
    below = extract_between(src, '<!-- IM-CARD: Method Note / Disclaimer -->', '<!-- IC-FAQ -->')
    below = below.replace('im-card tool-rv', 't-section')
    below += faq_section([
        ('How is inheritance distributed in Islam?', 'كيف يُوزَّع الميراث في الإسلام?', 'Faraid distributes the estate per Quran An-Nisa 4:11-12 with fixed shares.', 'الفرائض توزع التركة وفق النساء 4:11-12.'),
        ('What is Asaba in inheritance?', 'ما العصبة؟', 'Residuary heirs receive what remains after fixed-share heirs.', 'العصبة يرثون الباقي بعد أصحاب الفروض.'),
        ('Can a son inherit more than a daughter?', 'هل يرث الابن أكثر؟', 'Generally a son inherits twice a daughter per An-Nisa 4:11.', 'عموماً الابن يرث ضعف البنت.'),
        ('What is Awl?', 'ما العول؟', 'When fixed shares exceed 100%, all shares reduce proportionally.', 'عند تجاوز الفروض 100% تُخفَّض الحصص بالتناسب.'),
    ])
    meta = dict(slug='inheritance-calculator', data_tool='inheritance-calculator',
        title='Islamic Inheritance Calculator | حاسبة الميراث — Dot For Life',
        desc='Calculate Islamic inheritance (Faraid) distribution with Hijb, Awl, and Asaba rules. Bilingual, educational.',
        og_title='Islamic Inheritance Calculator | Dot4Life', og_desc='Quran-based Faraid with blocking and Awl rules.',
        schema_name='Islamic Inheritance Calculator',
        bc_en='Inheritance Calculator', bc_ar='حاسبة الميراث',
        eyebrow_en='Finance Tool · Islamic', eyebrow_ar='أداة مالية · إسلامية',
        h1_en='Islamic Inheritance Calculator', h1_ar='حاسبة الميراث الإسلامية',
        desc_en='Enter estate value and select heirs. Applies Quran verses, Hijb blocking, and Awl reduction automatically.',
        desc_ar='أدخل قيمة التركة واختر الورثة. تطبّق آيات القرآن والحجب والعول تلقائياً.',
        trust='<li><span class="en">An-Nisa 4:11-12</span><span class="ar">النساء 4:11-12</span></li><li><span class="en">Hijb &amp; Awl</span><span class="ar">حجب وعول</span></li><li><span class="en">Educational</span><span class="ar">تعليمي</span></li>')
    rail = gen.tickets(gen.ticket('/tools/zakat-calculator.html','tool-ticket--zakat','Islamic','إسلامية','Zakat Calculator','حاسبة الزكاة','On inherited wealth.','على الميراث.')+gen.ticket('/tools/monthly-budget.html','tool-ticket--budget','Finance','مالية','Monthly Budget','الميزانية','Plan family finances.','خطط مالية.')+gen.ticket('/islamic.html','tool-ticket--islamic','Islamic','إسلامية','Islamic Hub','المركز الإسلامي','More tools.','المزيد من الأدوات.'))
    init = "document.addEventListener('DOMContentLoaded',function(){document.getElementById('results-body').innerHTML=getEmptyState();});"
    return assemble_page(meta, main, below, rail, js, init)


BUILDERS = {
    'salary-calculator': build_salary,
    'savings-goal': build_savings,
    'mortgage-calculator': build_mortgage,
    'monthly-budget': build_budget,
    'roi-calculator': build_roi,
    'rental-yield-calculator': build_rental_yield,
    'inheritance-calculator': build_inheritance,
}


def main():
    written = []
    for slug, fn in BUILDERS.items():
        out = TOOLS / f'{slug}.html'
        html = fn()
        out.write_text(html, encoding='utf-8')
        written.append(str(out.relative_to(ROOT)))
        print(f'Wrote {out.name} ({len(html)} bytes)')
    print('\nFiles written:')
    for w in written:
        print(' ', w)


if __name__ == '__main__':
    main()
