#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوابة عامر — فحص مستقل على ملفات HTML المنشورة/المرشّحة للنشر.
يطبّق content-standards.md + amer-mandate.md.
"""
import re, sys, json, os

SENSITIVE = re.compile(r"(صحة|طبي|حمل|تغذية|دواء|مال|استثمار|ميزانية|راتب|تقاعد|زكاة|صلاة|عمرة|حج|أذكار|فتوى"
                        r"|health|medical|pregnan|nutrition|financ|invest|budget|salary|prayer|umrah|hajj|islam|retirement|saving)", re.I)
DISCLAIMER = re.compile(r"(إخلاء|ليست\s+استشارة|ليست\s+فتوى|معلومات\s+عامة|راجع\s+(?:طبيب|مختص|أهل\s+العلم|مستشار)"
                         r"|disclaimer|not\s+(?:medical|financial|professional)\s+advice|not\s+a\s+fatwa|consult)", re.I)
CLICHE = ["في الختام", "علاوة على ذلك", "تجدر الإشارة", "في عالمنا السريع",
          "أصبح أولوية لكل عائلة", "في عصرنا الحالي",
          "in conclusion", "moreover,", "in today's fast"]
FABRICATED_QUOTE = re.compile(r"(DOTFORLIFE Research|DOTFORLIFE Health|Islamic Practice Guide|Financial Framework|Key quotable statement|Citation-Ready)", re.I)
AUTHORITY_PATTERN = re.compile(
    r"(جامعة [\w؀-ۿ]+|معهد [\w؀-ۿ]+|مركز [\w؀-ۿ]+|مجلة [\w؀-ۿ]+|أكاديمية [\w؀-ۿ]+|منظمة [\w؀-ۿ]+|دراسة (?:من|أجرتها)[^.]{0,40}"
    r"|[Uu]niversity of \w+|[Ii]nstitute of \w+|[Cc]enter for \w+|[Jj]ournal of [\w ]+|[Aa]cademy of \w+"
    r"|[Ss]tudies? (?:from|by|published in)|[Rr]esearch (?:from|by)|found that|shows that)"
)
# قاعدة عامر 2026-07-02: صفر تسامح مع أي اقتباس ديني مباشر (حديث أو آية)، بأي صياغة،
# منسوب أو غير منسوب. يشمل مؤشرات عربية وإنجليزية بعد اكتشاف أن الفحص العربي وحده
# فوّت اقتباسات إنجليزية مباشرة (zakat-guide-2025-en، masjid-nabawi-complete-guide، إلخ).
RELIGIOUS_QUOTE_PATTERN = re.compile(
    r"(قال\s+النبي|صلى\s+الله\s+عليه\s+وسلم|رسول\s+الله\s+ﷺ|حديث\s+شريف|قال\s+رسول\s+الله"
    r"|قال\s+الله\s+تعالى|قال\s+تعالى|رضي\s+الله\s+عن|﴿[^﴾]{3,}﴾"
    r"|Allah\s+says|Prophet\s+Muhammad.{0,20}said|the\s+Prophet\s+said|Prophet\s+\(peace\s+be\s+upon\s+him\)\s+said"
    r"|Qur'?an\s+\d{1,3}\s*:\s*\d{1,3}|Surah\s+[A-Z][a-z]+\s*\(?\d{1,3}\s*:\s*\d{1,3}"
    r"|\bBukhari\b|\bTirmidhi\b|\bIbn\s+Majah\b|narrated\s+that\s+the\s+Prophet|it\s+was\s+narrated)",
    re.I
)

def text_only(html):
    t = re.sub(r"<script[^>]*application/ld\+json[^>]*>.*?</script>", " ", html, flags=re.S)
    t = re.sub(r"<script.*?</script>", " ", t, flags=re.S)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
    return t

def body_word_count(html):
    t = text_only(html)
    m = re.search(r'<article[^>]*>(.*?)</article>', t, re.S)
    chunk = m.group(1) if m else t
    chunk = re.sub(r"<[^>]+>", " ", chunk)
    chunk = re.sub(r"&\w+;", " ", chunk)
    words = [w for w in re.split(r"\s+", chunk) if w.strip()]
    return len(words)

def em_dash_count(html):
    # Calculator/UI placeholders: sole em-dash in element or JS literal
    cleaned = re.sub(r">(\s*)—(\s*)<", r">\1\2<", html)
    cleaned = re.sub(r"['\"]—['\"]", "''", cleaned)
    t = text_only(cleaned)
    t = re.sub(r"<[^>]+>", " ", t)
    return t.count("—")

def ld_json_blocks(html):
    blocks = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S)
    parsed = []
    for b in blocks:
        try:
            parsed.append(json.loads(b.strip()))
        except Exception as e:
            parsed.append({"__error__": str(e), "__raw__": b[:200]})
    return parsed

def has_type(blocks, t):
    n = 0
    for b in blocks:
        if isinstance(b, dict):
            if b.get("@type") == t:
                n += 1
            if "@graph" in b:
                for g in b["@graph"]:
                    if isinstance(g, dict) and g.get("@type") == t:
                        n += 1
        elif isinstance(b, list):
            for x in b:
                if isinstance(x, dict) and x.get("@type") == t:
                    n += 1
    return n

def faq_count_schema(blocks):
    n = 0
    for b in blocks:
        items = []
        if isinstance(b, dict) and b.get("@type") == "FAQPage":
            items = b.get("mainEntity", [])
        if isinstance(b, dict) and "@graph" in b:
            for g in b["@graph"]:
                if isinstance(g, dict) and g.get("@type") == "FAQPage":
                    items = g.get("mainEntity", [])
        n += len(items) if isinstance(items, list) else 0
    return n

def percent_count(html):
    t = text_only(html)
    t = re.sub(r"<[^>]+>", " ", t)
    return len(re.findall(r"\d+(?:\.\d+)?\s?(?:%|٪)", t))

def deep_links(html):
    links = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
    deep, shallow = [], []
    for l in links:
        if 'dotforlife' in l.lower() or 'd4l' in l.lower():
            continue
        if 'fonts.google' in l or 'fonts.gstatic' in l:
            continue
        m = re.match(r'https?://[^/]+/(.+)', l)
        if m and len(m.group(1).strip('/')) > 3:
            deep.append(l)
        else:
            shallow.append(l)
    return deep, shallow

def unsplash_check(html):
    return len(re.findall(r"unsplash\.com", html, re.I))

def internal_links(html):
    links = re.findall(r'href=["\']([^"\']+\.html)["\']', html)
    internal = [l for l in links if not l.startswith('http')]
    return len(set(internal))

def arabic_page_latin_check(html, is_arabic):
    """فحص فقرات لاتينية داخل جسم المقال فقط — لا nav/footer الموحّدين ثنائيي اللغة."""
    if not is_arabic:
        return 0
    t = text_only(html)
    # استبعد الكروم الثابت حتى لا يُكسر الهيدر/الفوتر الموحّدان من partials
    t = re.sub(r"<nav\b[^>]*>.*?</nav>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<footer\b[^>]*>.*?</footer>", " ", t, flags=re.S | re.I)
    m = re.search(r"<article\b[^>]*>(.*?)</article>", t, re.S | re.I)
    chunk = m.group(1) if m else t
    paras = re.findall(r"<p[^>]*>(.*?)</p>", chunk, re.S)
    bad = 0
    for p in paras:
        p2 = re.sub(r"<[^>]+>", "", p).strip()
        if len(p2) < 20:
            continue
        latin = len(re.findall(r"[A-Za-z]", p2))
        arabic = len(re.findall(r"[؀-ۿ]", p2))
        if latin > arabic and latin > 20:
            bad += 1
    return bad

def authority_no_link(html):
    t = text_only(html)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", t, re.S)
    flags = []
    for p in paras:
        has_authority = AUTHORITY_PATTERN.search(re.sub(r"<[^>]+>", "", p))
        has_link = "<a href" in p.lower() or "href=" in p.lower()
        if has_authority and not has_link:
            snippet = re.sub(r"<[^>]+>", "", p).strip()[:90]
            flags.append(snippet)
    return flags

def religious_quote_check(html):
    """قاعدة عامر المطلقة: صفر اقتباس ديني مباشر (حديث/آية)، عربي أو إنجليزي،
    منسوب أو غير منسوب. يفحص جسم المقال فقط + كتل JSON-LD (FAQ schema يمكن أن
    يحمل الاقتباس أيضاً كما حدث في عدة ملفات هذا الأسبوع)."""
    t = text_only(html)
    m = re.search(r"<article\b[^>]*>(.*?)</article>", t, re.S | re.I)
    body = m.group(1) if m else t
    body = re.sub(r"<[^>]+>", " ", body)
    hits = [s.strip()[:90] for s in RELIGIOUS_QUOTE_PATTERN.findall(body) if s]
    # فحص منفصل داخل نصوص FAQ schema (raw JSON نص، بلا وسوم HTML)
    raw_ld = re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html, re.S)
    for block in raw_ld:
        if RELIGIOUS_QUOTE_PATTERN.search(block):
            hits.append("داخل JSON-LD schema")
    return hits

def hero_image_check(html):
    has_webp_hero = bool(re.search(r'(hero-[\w-]+\.webp|assets/images/[\w/-]+\.webp)', html))
    return has_webp_hero

def sidebar_structure_fail(html):
    """فحص بنيوي: <aside class="article-sidebar"> لازم يكون طفلاً مباشراً لـ
    <div class="article-layout">. لو اتعشّش جوّه أي وسم تاني (بسبب وسم غير مقفول
    في جسم المقال) فالسايدبار هيظهر تحت المقال لا جنبه — وهذا فشل بنيوي.
    يستخدم html5lib (نفس سلوك المتصفّح) لأن فحص توازن الوسوم بالنص يفوته هذا العطل."""
    if 'article-sidebar' not in html:
        return ''  # صفحة بلا سايدبار — لا فحص
    try:
        import html5lib
    except ImportError:
        return ''  # المحلّل غير متاح (الـ workflow يثبّته) — تخطٍّ آمن
    doc = html5lib.parse(html, treebuilder="dom")
    asides = []
    def walk(n):
        for ch in n.childNodes:
            if ch.nodeType == 1:
                if 'article-sidebar' in (ch.getAttribute('class') or ''):
                    asides.append(ch)
                walk(ch)
    walk(doc)
    if not asides:
        return ''
    p = asides[0].parentNode
    if 'article-layout' not in (p.getAttribute('class') or ''):
        pc = (p.getAttribute('class') or '').split(' ')[0] or p.tagName.lower()
        return (f"بنية مكسورة: السايدبار متعشّش تحت <{p.tagName.lower()}.{pc}> بدل "
                f"article-layout — سيظهر تحت المقال لا جنبه (وسم غير مقفول في الجسم)")
    return ''

def run(fp):
    html = open(fp, encoding="utf-8", errors="ignore").read()
    html_tag_m = re.search(r"<html\b[^>]*>", html)
    html_tag = html_tag_m.group(0) if html_tag_m else ""
    is_arabic = bool(re.search(r'(?<![a-zA-Z-])lang=["\']ar["\']', html_tag))
    out = {"file": fp, "fails": [], "warns": [], "info": {}}
    w = body_word_count(html)
    out["info"]["words"] = w
    if w < 1300:
        out["fails"].append(f"كلمات={w} <1300")
    em = em_dash_count(html)
    out["info"]["em_dash"] = em
    if em:
        out["fails"].append(f"شرطات طويلة={em}")
    blocks = ld_json_blocks(html)
    art = has_type(blocks, "Article")
    faqp = has_type(blocks, "FAQPage")
    out["info"]["Article_schema"] = art
    out["info"]["FAQPage_schema"] = faqp
    json_errors = [b for b in blocks if isinstance(b, dict) and "__error__" in b]
    if json_errors:
        out["fails"].append(f"JSON-LD غير صالح: {json_errors[0]['__error__']}")
    if art < 1:
        out["fails"].append("Article schema مفقود")
    if faqp < 1:
        out["fails"].append("FAQPage schema مفقود")
    if faqp > 1:
        out["fails"].append(f"FAQPage مكرّرة ({faqp} كتلة)")
    faqn = faq_count_schema(blocks)
    out["info"]["faq_n"] = faqn
    if faqn and (faqn < 4 or faqn > 6):
        out["warns"].append(f"FAQ عدد={faqn} (المطلوب 4-6)")
    elif faqn == 0:
        out["fails"].append("FAQ=0 في schema")
    cl = [c for c in CLICHE if c.lower() in html.lower()]
    if cl:
        out["fails"].append("كليشيهات AI: " + "، ".join(cl))
    if FABRICATED_QUOTE.search(html):
        out["fails"].append("اقتباس سلطة داخلي مختلَق محتمل")
    if SENSITIVE.search(html) and not DISCLAIMER.search(html):
        out["fails"].append("محتوى حسّاس بلا إخلاء مسؤولية")
    pct = percent_count(html)
    out["info"]["percent_count"] = pct
    deep, shallow = deep_links(html)
    out["info"]["deep_links"] = len(deep)
    out["info"]["shallow_links"] = len(shallow)
    if pct > 3:
        out["warns"].append(f"نِسَب دقيقة={pct} >3 (يلزم فحص يدوي لرابط عميق لكل نسبة)")
    if pct > 0 and len(deep) == 0:
        out["fails"].append(f"نِسَب={pct} بلا أي رابط عميق واحد")
    auth_flags = authority_no_link(html)
    if auth_flags:
        out["fails"].append(f"ادّعاء سلطة بلا رابط مجاور ({len(auth_flags)}): " + " | ".join(auth_flags[:3]))
    if unsplash_check(html):
        out["fails"].append("صورة Unsplash placeholder (يلزم hero معتمد)")
    if not hero_image_check(html):
        out["warns"].append("لا hero webp واضح في assets/images")
    il = internal_links(html)
    out["info"]["internal_links"] = il
    if il < 3:
        out["warns"].append(f"روابط داخلية={il} <3")
    latin_bad = arabic_page_latin_check(html, is_arabic)
    if latin_bad:
        out["fails"].append(f"فقرات لاتينية في صفحة عربية={latin_bad}")
    sb = sidebar_structure_fail(html)
    if sb:
        out["fails"].append(sb)
    rq = religious_quote_check(html)
    if rq:
        out["fails"].append(f"اقتباس ديني مباشر ({len(rq)}): " + " | ".join(rq[:3]))
    return out

def main():
    files = sys.argv[1:]
    results = []
    for fp in files:
        results.append(run(fp))
    for r in results:
        status = "FAIL" if r["fails"] else ("WARN" if r["warns"] else "PASS")
        print(f"{status}  {r['file']}  {r['info']}")
        for f in r["fails"]:
            print(f"     FAIL: {f}")
        for w in r["warns"]:
            print(f"     warn: {w}")
    print()
    n_fail = sum(1 for r in results if r["fails"])
    print(f"الإجمالي: {len(results)} ملف، {n_fail} فاشل، {len(results)-n_fail} ناجح/تحذير")

if __name__ == "__main__":
    main()
