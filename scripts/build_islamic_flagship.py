#!/usr/bin/env python3
"""Generate flagship Islamic tool HTML pages."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
STYLES = ROOT / "styles" / "pages"

sys.path.insert(0, str(ROOT / "scripts"))
import _gen_islamic_flagship as gen  # noqa: E402

ZAKAT_JS = r'''
const GOLD_PRICE_PER_G=230,SILVER_PRICE_PER_G=2.7;
const GOLD_NISAB_G=85,SILVER_NISAB_G=595;
const goldNisabSAR=GOLD_NISAB_G*GOLD_PRICE_PER_G;
const silverNisabSAR=SILVER_NISAB_G*SILVER_PRICE_PER_G;
let nisabMethod='silver';

function getLang(){return document.documentElement.getAttribute('data-lang')||'en';}

function initNisabDisplay(){
  var fmt=function(n){return n.toLocaleString(getLang()==='ar'?'ar-SA':'en');};
  ['goldNisabVal','silverNisabVal','goldNisabDisplay','silverNisabDisplay'].forEach(function(id,i){
    var el=document.getElementById(id);
    if(!el) return;
    var val=i%2?silverNisabSAR:goldNisabSAR;
    if(id.indexOf('Display')>-1) el.innerHTML=fmt(val)+' <span class="en">SAR</span><span class="ar">ريال</span>';
    else el.textContent=fmt(val);
  });
}

function setNisab(m){
  nisabMethod=m;
  document.getElementById('btnGold').classList.toggle('active',m==='gold');
  document.getElementById('btnSilver').classList.toggle('active',m==='silver');
}

function switchSection(id,btn){
  document.querySelectorAll('.calc-section').forEach(function(s){s.classList.remove('active');});
  document.querySelectorAll('.zt-tab').forEach(function(b){b.classList.remove('active');});
  document.getElementById('sec-'+id).classList.add('active');
  if(btn) btn.classList.add('active');
}

function v(id){return parseFloat(document.getElementById(id)?.value)||0;}

function calculateZakat(){
  var nisabSAR=nisabMethod==='gold'?goldNisabSAR:silverNisabSAR;
  var cashBase=v('bankBalance')+v('cashHome')+v('deposits')-v('liabilities');
  var karat=parseFloat(document.getElementById('goldKarat').value)||1;
  var goldBase=(v('goldGrams')*karat)*GOLD_PRICE_PER_G;
  var silverBase=v('silverGrams')*SILVER_PRICE_PER_G;
  var stocksBase=(v('stocksInvest')*0.4)+(v('stocksTrade')*1.0)+(v('funds')*0.4)+v('rentalIncome');
  var tradeBase=v('inventory')+v('receivables')+v('bizCash')-v('bizLiabilities');
  var debtsBase=v('recoverableDebts');
  var totalBase=Math.max(0,cashBase)+Math.max(0,goldBase)+silverBase+Math.max(0,stocksBase)+Math.max(0,tradeBase)+debtsBase;
  var nisabReached=totalBase>=nisabSAR;
  var zakatDue=nisabReached?(totalBase*0.025):0;
  var card=document.getElementById('resultsCard');
  card.classList.add('show');
  card.scrollIntoView({behavior:'smooth',block:'nearest'});
  document.getElementById('zakatAmount').textContent=zakatDue.toLocaleString(getLang()==='ar'?'ar-SA':'en',{maximumFractionDigits:2});
  var lang=getLang();
  var badge=document.getElementById('nisabStatusBadge');
  if(nisabReached){
    badge.textContent='✓ '+(lang==='ar'?'بلغ النصاب، تجب الزكاة':'Nisab reached, Zakat is due');
    badge.className='zr-badge zr-badge--ok';
  }else{
    badge.textContent='ℹ️ '+(lang==='ar'?'لم يبلغ النصاب':'Nisab not reached');
    badge.className='zr-badge zr-badge--no';
  }
  document.getElementById('zakatSub').textContent=lang==='ar'
    ?'وعاء الزكاة: '+totalBase.toLocaleString('ar-SA',{maximumFractionDigits:0})+' ريال | النصاب: '+nisabSAR.toLocaleString()+' ريال'
    :'Zakat base: SAR '+totalBase.toLocaleString(undefined,{maximumFractionDigits:0})+' | Nisab: SAR '+nisabSAR.toLocaleString();
  var rows=[];
  if(cashBase>0) rows.push({ar:'نقود وبنوك',en:'Cash & Banks',base:Math.max(0,cashBase),z:Math.max(0,cashBase)*0.025});
  if(goldBase>0) rows.push({ar:'ذهب',en:'Gold',base:goldBase,z:goldBase*0.025});
  if(silverBase>0) rows.push({ar:'فضة',en:'Silver',base:silverBase,z:silverBase*0.025});
  if(stocksBase>0) rows.push({ar:'أسهم',en:'Stocks',base:Math.max(0,stocksBase),z:Math.max(0,stocksBase)*0.025});
  if(tradeBase>0) rows.push({ar:'تجارة',en:'Trade',base:Math.max(0,tradeBase),z:Math.max(0,tradeBase)*0.025});
  if(debtsBase>0) rows.push({ar:'ديون',en:'Receivables',base:debtsBase,z:debtsBase*0.025});
  document.getElementById('breakdownBody').innerHTML=rows.map(function(r){
    return '<tr><td><span class="en">'+r.en+'</span><span class="ar">'+r.ar+'</span></td><td>'+r.base.toLocaleString(undefined,{maximumFractionDigits:0})+'</td><td>'+(nisabReached?r.z.toLocaleString(undefined,{maximumFractionDigits:2}):'—')+'</td></tr>';
  }).join('');
  document.getElementById('resultsGrid').innerHTML=
    '<div class="t-metric"><div class="t-metric-val">'+totalBase.toLocaleString(undefined,{maximumFractionDigits:0})+'</div><div class="t-metric-lbl"><span class="en">Total Base</span><span class="ar">الوعاء الكلي</span></div></div>'+
    '<div class="t-metric"><div class="t-metric-val">2.5%</div><div class="t-metric-lbl"><span class="en">Zakat Rate</span><span class="ar">نسبة الزكاة</span></div></div>'+
    '<div class="t-metric"><div class="t-metric-val">'+(zakatDue/12).toLocaleString(undefined,{maximumFractionDigits:0})+'</div><div class="t-metric-lbl"><span class="en">Monthly (approx)</span><span class="ar">شهرياً تقريباً</span></div></div>';
  if(window.dflTrack) dflTrack('zakat_calculated',{nisab:nisabMethod,total:Math.round(totalBase)});
}

function copyResult(){
  var lang=getLang();
  var amt=document.getElementById('zakatAmount').textContent;
  navigator.clipboard.writeText(lang==='ar'?'الزكاة المستحقة: '+amt+' ريال':'Zakat due: SAR '+amt);
}
function shareResult(){
  var lang=getLang(), amt=document.getElementById('zakatAmount').textContent;
  if(navigator.share) navigator.share({title:lang==='ar'?'حاسبة الزكاة':'Zakat Calculator',text:amt,url:location.href});
}
function printResult(){window.print();}
function toggleFaq(el){
  var open=el.classList.contains('open');
  document.querySelectorAll('.t-faq-q').forEach(function(q){q.classList.remove('open');q.nextElementSibling.classList.remove('active');});
  if(!open){el.classList.add('open');el.nextElementSibling.classList.add('active');}
}

document.addEventListener('DOMContentLoaded',function(){initNisabDisplay();});
document.addEventListener('dfl:langchange',function(){initNisabDisplay();});
'''


def extract_js(filename, start_marker="// ═"):
    text = (TOOLS / filename).read_text(encoding="utf-8")
    m = re.search(r"<script>\s*(// ═[\s\S]*?)</script>", text)
    if not m:
        m = re.search(r"<script>\s*(// ─[\s\S]*?)</script>", text)
    return m.group(1) if m else ""


def clean_prayer_js(js):
    js = re.sub(r"// ═+\n// THEME / LANG[\s\S]*?// NAVBAR SCROLL[\s\S]*?;\n\n", "", js)
    js = re.sub(r"// Theme icon[\s\S]*?calculate\(\);\n\n", "calculate();\n\n", js)
    js = js.replace("(function init()", "document.addEventListener('DOMContentLoaded', function init()")
    js += "\ndocument.addEventListener('dfl:langchange', function(){ renderTimes(); renderWeek(); renderDateDisplay(); });\n"
    return js


def clean_qibla_js(js):
    js = js.replace("// INIT\ncalculate();", "document.addEventListener('DOMContentLoaded', function(){ calculate(); });")
    js += "\ndocument.addEventListener('dfl:langchange', function(){ renderCompass(); });\n"
    return js


def clean_hijri_js(js):
    js = js.replace(
        "new MutationObserver(function(){ initToday(); }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-lang'] });",
        "document.addEventListener('dfl:langchange', function(){ initToday(); });",
    )
    js = re.sub(
        r"const ro=new IntersectionObserver[\s\S]*?document\.querySelectorAll\('\.reveal'\)\.forEach\(el=>ro\.observe\(el\)\);",
        "",
        js,
    )
    return js


def tickets(cards):
    body = "".join(cards)
    return f'''  <section class="tool-tickets-rail" aria-labelledby="related-tools-title">
    <header class="tool-tickets-head">
      <p class="tool-tickets-eyebrow">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
        <span class="en">Continue Your Journey</span><span class="ar">أكمل رحلتك</span>
      </p>
      <h2 class="tool-tickets-title" id="related-tools-title"><span class="en">Related Islamic Tools</span><span class="ar">أدوات إسلامية ذات صلة</span></h2>
      <p class="tool-tickets-sub"><span class="en">Tools for your daily spiritual practice.</span><span class="ar">أدوات لممارستك الروحية اليومية.</span></p>
    </header>
    <div class="tool-tickets-track">{body}</div>
  </section>'''


def ticket(href, num, cls, en, ar, desc_en, desc_ar):
    return f'''      <a href="{href}" class="tool-ticket tool-ticket--{cls}">
        <div class="tool-ticket-stub"><span class="tool-ticket-num">{num}</span></div>
        <div class="tool-ticket-perforation" aria-hidden="true"></div>
        <div class="tool-ticket-body">
          <span class="tool-ticket-kicker"><span class="en">Islamic</span><span class="ar">إسلامية</span></span>
          <h3><span class="en">{en}</span><span class="ar">{ar}</span></h3>
          <p><span class="en">{desc_en}</span><span class="ar">{desc_ar}</span></p>
          <span class="tool-ticket-cta"><span class="en">Open tool →</span><span class="ar">← افتح الأداة</span></span>
        </div>
      </a>'''


ISLAMIC_TICKETS = [
    ticket("/tools/qibla.html", "01", "water", "Qibla Direction", "اتجاه القبلة", "Great-circle bearing to Mecca.", "اتجاه الدائرة العظمى لمكة."),
    ticket("/tools/zakat-calculator.html", "02", "calories", "Zakat Calculator", "حاسبة الزكاة", "Annual zakat on all assets.", "زكاة سنوية على جميع الأموال."),
    ticket("/tools/hijri-converter.html", "03", "water", "Hijri Converter", "محوّل الهجري", "Hijri ↔ Gregorian dates.", "تحويل هجري ↔ ميلادي."),
    ticket("/guides/zakat-complete-guide.html", "04", "strength", "Zakat Guide", "دليل الزكاة", "Complete zakat reference.", "مرجع شامل للزكاة."),
]


def faq_block(items):
    html = ['    <div class="t-faq">', '      <div class="t-faq-label"><span class="en">FAQ</span><span class="ar">أسئلة شائعة</span></div>',
            '      <div class="t-faq-title"><span class="en">Frequently Asked Questions</span><span class="ar">الأسئلة المتكررة</span></div>']
    for q_en, q_ar, a_en, a_ar in items:
        html.append(f'''      <div class="t-faq-item">
        <div class="t-faq-q" onclick="toggleFAQ(this)"><span><span class="en">{q_en}</span><span class="ar">{q_ar}</span></span><span class="t-faq-arrow">▼</span></div>
        <div class="t-faq-a"><p><span class="en">{a_en}</span><span class="ar">{a_ar}</span></p></div>
      </div>''')
    html.append('    </div>')
    return "\n".join(html)


def toggle_faq_js():
    return """
function toggleFAQ(el) {
  var answer = el.nextElementSibling;
  var isOpen = el.classList.contains('open');
  document.querySelectorAll('.t-faq-q').forEach(function(q) {
    q.classList.remove('open');
    q.nextElementSibling.classList.remove('active');
  });
  if (!isOpen) {
    el.classList.add('open');
    answer.classList.add('active');
  }
}
"""


def write_page(path, content):
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def build_prayer_times():
    src = (TOOLS / "prayer-times.html").read_text(encoding="utf-8")
    # Extract workspace blocks from city-section through info-grid
    city = re.search(r"<section class=\"city-section\">[\s\S]*?</section>", src).group(0)
    main = re.search(r"<!-- NEXT PRAYER BANNER -->[\s\S]*?<!-- INFO GRID -->[\s\S]*?</div>\s*</div>\n</section>", src).group(0)
    city = city.replace('class="city-section"', 'class="tool-panel pt-card"').replace('<div class="container">', '').replace('</div>\n</section>', '</section>')
    main = main.replace('<section style="padding-bottom:40px;">\n  <div class="container">\n\n', '').replace('\n  </div>\n</section>', '')

    body = f'''  <div class="tool-workspace pt-workspace">
    {city}
    <div class="pt-main">{main}</div>
  </div>

  <div class="tool-below">
    <div class="t-section">
      <div class="t-section-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> <span class="en">How prayer times are calculated</span><span class="ar">طريقة حساب أوقات الصلاة</span></div>
      <p><span class="en">Islamic prayer times are determined by the sun's position relative to the horizon. This tool uses the Meeus/USNO solar algorithm with configurable Fajr and Isha angles (Umm al-Qura, MWL, ISNA, Egyptian).</span><span class="ar">أوقات الصلاة الإسلامية تحددها موقع الشمس بالنسبة للأفق. تستخدم هذه الأداة خوارزمية Meeus/USNO مع زوايا الفجر والعشاء (أم القرى، رابطة العالم الإسلامي، إسنا، الهيئة المصرية).</span></p>
    </div>
    {faq_block([
      ("Why do methods differ?", "لماذا تختلف الطرق؟", "Different Fajr/Isha angles produce 2–5 minute differences. Match your local mosque for community prayer.", "زوايا الفجر والعشاء المختلفة تنتج فروقاً 2–5 دقائق. طابق مسجدك المحلي."),
      ("Can I use GPS?", "هل يمكن استخدام GPS؟", "Yes — Auto-Locate uses your coordinates and estimates timezone from longitude.", "نعم — «موقعي» يستخدم إحداثياتك ويقدّر المنطقة الزمنية."),
    ])}
  </div>

{tickets([t for t in ISLAMIC_TICKETS if "qibla" in t or "hijri" in t or "zakat" in t][:3] + [ISLAMIC_TICKETS[3]])}
'''

    js = clean_prayer_js(extract_js("prayer-times.html"))
    js += toggle_faq_js()
    schema = '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"Prayer Times | أوقات الصلاة","url":"https://dotforlife.com/tools/prayer-times.html","applicationCategory":"LifestyleApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"SAR"},"inLanguage":["en","ar"]}
</script>'''

    meta = {
        "title": "Prayer Times | أوقات الصلاة — GCC Cities | Dot For Life",
        "desc": "Accurate Islamic prayer times for GCC cities with countdown, Hijri date, and multiple calculation methods. Bilingual Arabic & English.",
        "css": "/styles/pages/tools_prayer-times.css?v=20260625a",
        "schema": schema,
        "hero": {
            "breadcrumb_en": "Prayer Times", "breadcrumb_ar": "أوقات الصلاة",
            "eyebrow_en": "Islamic Tool · Solar Algorithm", "eyebrow_ar": "أداة إسلامية · خوارزمية شمسية",
            "h1_en": "Prayer Times Calculator", "h1_ar": "حاسبة أوقات الصلاة",
            "desc_en": "Accurate prayer times for GCC cities. Auto-detect your location or select a city with live countdown.",
            "desc_ar": "أوقات صلاة دقيقة لمدن الخليج. اكتشف موقعك تلقائياً أو اختر مدينة مع عدّ تنازلي مباشر.",
            "trust": [("GCC cities", "مدن الخليج"), ("Runs locally", "يعمل محلياً"), ("Free & private", "مجاني وخاص")],
        },
    }
    html = gen.page("prayer-times", "prayer-times.html", body, f"<script>\n{js}\n</script>", meta)
    write_page(TOOLS / "prayer-times.html", html)


def build_qibla():
    src = (TOOLS / "qibla.html").read_text(encoding="utf-8")
    layout = re.search(r'<div class="qibla-layout">[\s\S]*?</div>\s*</div>\s*</div>', src).group(0)
    layout = layout.replace('<div class="container">\n  ', '').replace('\n</div>\n</div>', '')

    body = f'''  <div class="tool-workspace">
    {layout}
  </div>

  <div class="tool-below">
    <div class="t-section">
      <div class="t-section-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M12 12l4-2.5"/></svg> <span class="en">Great-circle method</span><span class="ar">طريقة الدائرة العظمى</span></div>
      <p><span class="en">Qibla is calculated using the shortest path on Earth's surface from your location to the Kaaba (21.4225°N, 39.8262°E). On mobile, enable Live Compass for real-time pointing.</span><span class="ar">يُحسب اتجاه القبلة بأقصر مسار على سطح الأرض من موقعك إلى الكعبة (21.4225°N, 39.8262°E). على الجوال، فعّل البوصلة الحية للإشارة الفورية.</span></p>
    </div>
    {faq_block([
      ("How do I use the compass?", "كيف أستخدم البوصلة؟", "Hold your device flat, away from metal. Calibrate with a figure-8 if unstable.", "أمسك جهازك بشكل مسطح بعيداً عن المعدن. عاير بحركة رقم 8 إذا كانت غير مستقرة."),
      ("Does Qibla change?", "هل يتغير اتجاه القبلة؟", "No — the bearing from any fixed point to Mecca is constant.", "لا — الاتجاه من أي نقطة ثابتة إلى مكة ثابت."),
    ])}
  </div>

{tickets(ISLAMIC_TICKETS[:4])}
'''

    js = clean_qibla_js(extract_js("qibla.html"))
    js += toggle_faq_js()
    meta = {
        "title": "Qibla Direction | اتجاه القبلة — Compass & GPS | Dot For Life",
        "desc": "Find the Qibla direction to Mecca from any GCC city. Great-circle bearing, distance, and live device compass. Bilingual.",
        "css": "/styles/pages/tools_qibla.css?v=20260625a",
        "schema": "",
        "hero": {
            "breadcrumb_en": "Qibla Direction", "breadcrumb_ar": "اتجاه القبلة",
            "eyebrow_en": "Islamic Tool · Great Circle", "eyebrow_ar": "أداة إسلامية · دائرة عظمى",
            "h1_en": "Qibla Direction Finder", "h1_ar": "حاسبة اتجاه القبلة",
            "desc_en": "Find the exact direction of the Kaaba from your location using great-circle calculations and live compass.",
            "desc_ar": "حدد الاتجاه الدقيق للكعبة من موقعك باستخدام حسابات الدائرة العظمى والبوصلة الحية.",
            "trust": [("Great-circle", "دائرة عظمى"), ("Live compass", "بوصلة حية"), ("Free & private", "مجاني وخاص")],
        },
    }
    html = gen.page("qibla", "qibla.html", body, f"<script>\n{js}\n</script>", meta)
    write_page(TOOLS / "qibla.html", html)


def build_zakat():
    src_path = Path("/tmp/zakat_orig.html") if Path("/tmp/zakat_orig.html").exists() else TOOLS / "zakat-calculator.html"
    src = src_path.read_text(encoding="utf-8")
    top = re.search(
        r'(<div class="zi-grid[\s\S]*?</div>\s*\n\s*<!-- ═══ NISAB STATUS)',
        src,
    ).group(1)
    mid = re.search(
        r'(<!-- ═══ NISAB STATUS[\s\S]*?</div>\s*\n\s*<!-- ═══ SECTION TABS[\s\S]*?</div>\s*\n\s*<!-- ═══ THE CALCULATOR)',
        src,
    ).group(1)
    calc = re.search(
        r'(<div class="zc-card[\s\S]*?</div>\s*\n)\s*<!-- ═══ RESULTS',
        src,
    ).group(1).rstrip() + "\n"
    results = re.search(
        r'(<div class="zr-card" id="resultsCard">[\s\S]*?</div>\s*\n\s*</div>)',
        src,
    ).group(1)
    faq_src = re.search(r'(<section class="zf-section[\s\S]*?</section>)', src)
    faq_html = ""
    if faq_src:
        faq_html = faq_src.group(1)
        faq_html = re.sub(r'\s*class="reveal[^"]*"', '', faq_html)
        faq_html = faq_html.replace('class="zf-section"', 'class="t-faq"')
        faq_html = faq_html.replace('class="zf-hdr ar"', 'class="t-faq-title" style="display:none"')
        faq_html = faq_html.replace('class="zf-hdr en"', 'class="t-faq-title"')
        faq_html = faq_html.replace('class="zf-item"', 'class="t-faq-item"')
        faq_html = faq_html.replace('class="zf-q"', 'class="t-faq-q" onclick="toggleFaq(this)"')
        faq_html = faq_html.replace('class="zf-tog">+</span>', 'class="t-faq-arrow">▼</span>')
        faq_html = faq_html.replace('class="zf-a"', 'class="t-faq-a"')
        faq_html = faq_html.replace('<div class="zf-ai">', '<div>')
        faq_html = faq_html.replace('<section class="t-faq"', '<div class="t-faq"')
        faq_html = faq_html.replace('</section>', '</div>', 1)

    workspace = re.sub(r'\s*class="reveal[^"]*"', '', top + "\n" + mid)
    body = f'''  <div class="tool-workspace zc-workspace">
{workspace}
{calc}
{results}
  </div>

  <div class="tool-below">
    <div class="t-section">
      <div class="t-section-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg> <span class="en">How Zakat is calculated</span><span class="ar">طريقة حساب الزكاة</span></div>
      <p><span class="en">Zakat is 2.5% of net assets reaching nisab (85g gold or 595g silver) held for a full lunar year. Gold: SAR 230/g, silver: SAR 2.7/g.</span><span class="ar">الزكاة 2.5% من صافي الأموال التي بلغت النصاب (85 جم ذهب أو 595 جم فضة) وحال عليها الحول. الذهب: 230 ريال/جم، الفضة: 2.7 ريال/جم.</span></p>
    </div>
    {faq_html}
  </div>

{tickets(ISLAMIC_TICKETS[:4])}
'''

    meta = {
        "title": "Zakat Calculator | حاسبة الزكاة — 2.5% Nisab | Dot For Life",
        "desc": "Calculate annual Zakat on cash, gold, silver, stocks, trade goods, and receivables. Gold nisab 85g, silver 595g. Bilingual.",
        "css": "/styles/pages/tools_zakat-calculator.css?v=20260625a",
        "schema": "",
        "hero": {
            "breadcrumb_en": "Zakat Calculator", "breadcrumb_ar": "حاسبة الزكاة",
            "eyebrow_en": "Islamic Tool · Shariah Compliant", "eyebrow_ar": "أداة إسلامية · متوافقة شرعاً",
            "h1_en": "Zakat Calculator", "h1_ar": "حاسبة الزكاة",
            "desc_en": "Calculate your annual Zakat on all asset types with updated 1447 AH gold and silver nisab prices.",
            "desc_ar": "احسب زكاتك السنوية على جميع أنواع الأموال بأسعار نصاب الذهب والفضة 1447هـ.",
            "trust": [("2.5% rate", "نسبة 2.5%"), ("Gold & silver nisab", "نصاب الذهب والفضة"), ("Free & private", "مجاني وخاص")],
        },
    }
    html = gen.page("zakat-calculator", "zakat-calculator.html", body, f"<script>\n{ZAKAT_JS}\n</script>", meta)
    write_page(TOOLS / "zakat-calculator.html", html)


def build_hijri():
    src = (TOOLS / "hijri-converter.html").read_text(encoding="utf-8")
    today = re.search(r'<div class="today-banner"[\s\S]*?</div>\s*\n</div>', src).group(0)
    conv = re.search(r'<div class="tool-cd conv-card[\s\S]*?</div>\s*\n</div>', src).group(0)
    result = re.search(r'<div class="result-card"[\s\S]*?</div>\s*\n</div>', src).group(0)
    events = re.search(r'<section class="events-section[\s\S]*?</section>', src).group(0)
    months = re.search(r'<section class="months-section[\s\S]*?</section>', src).group(0)
    years = re.search(r'<section class="year-table-section[\s\S]*?</section>', src).group(0)
    for block in (conv, events, months, years):
        pass
    blocks = today + "\n" + conv + "\n" + result + "\n" + events + "\n" + months + "\n" + years
    blocks = re.sub(r'\s*class="reveal[^"]*"', '', blocks)

    body = f'''  <div class="tool-workspace hc-workspace">
{blocks}
  </div>

  <div class="tool-below">
    <div class="t-section">
      <div class="t-section-label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> <span class="en">Umm al-Qura algorithm</span><span class="ar">خوارزمية أم القرى</span></div>
      <p><span class="en">Conversions use the Tabular Islamic Calendar (Umm al-Qura standard), accurate to within one day of astronomical observation.</span><span class="ar">التحويل يستخدم التقويم الهجري الجدولي (معيار أم القرى)، دقيق ضمن يوم من الرصد الفلكي.</span></p>
    </div>
    {faq_block([
      ("How accurate is this?", "ما مدى الدقة؟", "Tabular algorithm used across Saudi Arabia and GCC financial institutions.", "خوارزمية جدولية مستخدمة في السعودية ومؤسسات الخليج المالية."),
      ("Why do dates shift?", "لماذا تتغير التواريخ؟", "The Hijri lunar year is ~11 days shorter than Gregorian, so dates shift earlier each year.", "السنة الهجرية أقصر ~11 يوماً، فالتواريخ تتقدم كل عام."),
    ])}
  </div>

{tickets(ISLAMIC_TICKETS[:4])}
'''

    # Extract hijri script from current file (the big script block before dfl-method)
    hijri_js = re.search(r"<script>\n// ═+\n// HIJRI CONVERSION[\s\S]*?</script>", src).group(0)
    hijri_js = hijri_js.replace("<script>\n", "").replace("</script>", "")
    hijri_js = clean_hijri_js(hijri_js)
    hijri_js += toggle_faq_js()

    meta = {
        "title": "Hijri Date Converter | محوّل التاريخ الهجري | Dot For Life",
        "desc": "Convert Hijri and Gregorian dates instantly. Umm al-Qura algorithm, Islamic occasions, and bilingual support.",
        "css": "/styles/pages/tools_hijri-converter.css?v=20260625a",
        "schema": "",
        "hero": {
            "breadcrumb_en": "Hijri Converter", "breadcrumb_ar": "محوّل الهجري",
            "eyebrow_en": "Islamic Tool · Umm al-Qura", "eyebrow_ar": "أداة إسلامية · أم القرى",
            "h1_en": "Hijri Date Converter", "h1_ar": "محوّل التاريخ الهجري",
            "desc_en": "Convert between Hijri and Gregorian dates in seconds. Shows Islamic occasions and today's dual calendar.",
            "desc_ar": "حوّل بين التاريخ الهجري والميلادي في ثوانٍ. يعرض المناسبات الإسلامية وتقويم اليوم المزدوج.",
            "trust": [("Umm al-Qura", "أم القرى"), ("Instant", "فوري"), ("Free & private", "مجاني وخاص")],
        },
    }
    html = gen.page("hijri-converter", "hijri-converter.html", body, f"<script>\n{hijri_js}\n</script>", meta)
    write_page(TOOLS / "hijri-converter.html", html)


def trim_css(name, drop_affiliate=False):
    path = STYLES / name
    css = path.read_text(encoding="utf-8")
    # Strip prior header if re-running
    css = re.sub(r"/\* tools_[^\n]+\n\n\.tool-mn \{ padding-bottom: 0 !important; \}\n\n", "", css)
    lines = css.splitlines()
    out = []
    skip = False
    depth = 0
    lang_rule = re.compile(r"^\s*(\.en|\.ar|\[data-lang|\.en-b|\.ar-b)")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(":root") or (stripped.startswith("[data-theme") and "dark" in stripped):
            if stripped.endswith("{"):
                skip = True
                depth = 1
            continue
        if skip:
            depth += line.count("{") - line.count("}")
            if depth <= 0:
                skip = False
            continue
        if stripped.startswith("body{") or stripped.startswith("body {") or stripped.startswith("html{") or stripped.startswith("html {"):
            continue
        if "padding-top:158px" in line or "padding-top: 158px" in line:
            continue
        if lang_rule.match(stripped):
            continue
        if drop_affiliate and (".qb-affiliate" in line or ".qb-sponsor" in line or ".zk-affiliate" in line or ".zk-sponsor" in line):
            if "{" in line:
                skip = True
                depth = line.count("{") - line.count("}")
            continue
        line = line.replace("var(--accent", "var(--tool-accent")
        line = line.replace("var(--teal", "var(--tool-accent")
        line = line.replace("var(--teal-d", "var(--tool-accent-dark")
        line = line.replace("var(--teal-l", "var(--tool-accent-light")
        line = re.sub(r"#2a9a98\b", "var(--tool-accent)", line)
        line = re.sub(r"rgba\(42,154,152", "color-mix(in srgb, var(--tool-accent)", line)
        out.append(line)
    header = f"/* {name} — flagship page styles | accent via tools-accents.css */\n\n.tool-mn {{ padding-bottom: 0 !important; }}\n\n"
    path.write_text(header + "\n".join(out), encoding="utf-8")
    print(f"Trimmed {path.relative_to(ROOT)}")


def main():
    build_prayer_times()
    build_qibla()
    build_zakat()
    build_hijri()
    trim_css("tools_prayer-times.css")
    trim_css("tools_qibla.css", drop_affiliate=True)
    trim_css("tools_zakat-calculator.css")
    trim_css("tools_hijri-converter.css")


if __name__ == "__main__":
    main()
