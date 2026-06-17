#!/usr/bin/env python3
"""
Article Template Migration Script — v3 (Final Template)
=======================================================
Full spec: progress bar → header → container(banner → two-column
layout with body + sidebar) → article-end → footer.

Idempotent: checks for data-template="article" marker before modifying.
Safe to run multiple times.

Usage:
  python3 scripts/migrate-article-template.py
"""

import os, re, json, sys
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_MARKER = 'data-template="article"'
CACHE_BUSTER = 'v=20260617a'

DIRS = ['peace-capsules']  # ⚠️ TEMP: experimental folder only

# ── Category → tools mapping ──────────────────────────────
CATEGORY_TOOLS = {
    'family':   [{'url':'/tools/savings-calculator.html','label_en':'Savings Calculator','label_ar':'حاسبة الادخار'},
                 {'url':'/tools/budget-planner.html','label_en':'Budget Planner','label_ar':'مخطّط الميزانية'}],
    'finance':  [{'url':'/tools/mortgage-calculator.html','label_en':'Mortgage Calculator','label_ar':'حاسبة التمويل'},
                 {'url':'/tools/savings-calculator.html','label_en':'Savings Calculator','label_ar':'حاسبة الادخار'},
                 {'url':'/tools/zakat-calculator.html','label_en':'Zakat Calculator','label_ar':'حاسبة الزكاة'}],
    'health':   [{'url':'/tools/bmi-calculator.html','label_en':'BMI Calculator','label_ar':'حاسبة BMI'},
                 {'url':'/tools/water-calculator.html','label_en':'Water Intake Calculator','label_ar':'حاسبة الماء'}],
    'islamic':  [{'url':'/tools/zakat-calculator.html','label_en':'Zakat Calculator','label_ar':'حاسبة الزكاة'},
                 {'url':'/tools/hijri-converter.html','label_en':'Hijri Converter','label_ar':'محوّل التاريخ'}],
    'real-estate': [{'url':'/tools/mortgage-calculator.html','label_en':'Mortgage Calculator','label_ar':'حاسبة التمويل'},
                    {'url':'/tools/rent-vs-buy-calculator.html','label_en':'Rent vs Buy','label_ar':'إيجار أم شراء'}],
    'travel':   [{'url':'/tools/budget-planner.html','label_en':'Budget Planner','label_ar':'مخطّط الميزانية'},
                 {'url':'/tools/water-calculator.html','label_en':'Water Intake Calculator','label_ar':'حاسبة الماء'}],
}
DEFAULT_TOOLS = [{'url':'/tools/bmi-calculator.html','label_en':'BMI Calculator','label_ar':'حاسبة BMI'}]

# ── Category → tags ────────────────────────────────────────
CATEGORY_TAGS = {
    'family':     ['family', 'parenting', 'kids', 'education', 'gulf-family', 'values'],
    'finance':    ['finance', 'savings', 'investment', 'budget', 'gulf-economy'],
    'health':     ['health', 'wellness', 'nutrition', 'fitness', 'gulf-health'],
    'islamic':    ['islamic', 'faith', 'worship', 'spirituality', 'muslim-family'],
    'real-estate':['real-estate', 'property', 'housing', 'mortgage', 'gulf-property'],
    'travel':     ['travel', 'gulf-travel', 'family-trips', 'tourism', 'vacation'],
}

# ── Load partials ─────────────────────────────────────────────
with open(os.path.join(BASE, 'partials', 'header.html')) as f:
    HEADER_HTML = f.read()
with open(os.path.join(BASE, 'partials', 'footer.html')) as f:
    FOOTER_HTML = f.read()

# ── Load articles.json for metadata ───────────────────────────
def load_articles_meta():
    path = os.path.join(BASE, 'articles.json')
    if not os.path.exists(path): return {}
    with open(path) as f:
        data = json.load(f)
    meta = {}
    for a in data:
        url = a.get('url', '') or ''
        fname = url.split('/')[-1] if '/' in url else url
        meta[fname] = a
        meta[fname.replace('.html', '')] = a
        # Also index by EN url
        url_en = a.get('url_en', '') or ''
        if url_en:
            fname_en = url_en.split('/')[-1] if '/' in url_en else url_en
            meta[fname_en] = a
            meta[fname_en.replace('.html', '')] = a
    return meta

ARTICLES_META = load_articles_meta()
print(f"📖 Loaded metadata for {len(ARTICLES_META)} article keys from articles.json")

# ── Helpers ───────────────────────────────────────────────────

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def has_template(content):
    return TEMPLATE_MARKER in content

def get_html_attrs(content):
    """Extract lang, dir, data-lang from html tag."""
    lang = 'en'
    dir_ = 'ltr'
    data_lang = 'en'
    m = re.search(r'<html[^>]*\blang="([^"]+)"', content, re.IGNORECASE)
    if m: lang = m.group(1)
    m = re.search(r'<html[^>]*\bdir="([^"]+)"', content, re.IGNORECASE)
    if m: dir_ = m.group(1)
    m = re.search(r'data-lang="([^"]+)"', content)
    if m: data_lang = m.group(1)
    else: data_lang = lang
    return lang, dir_, data_lang

def get_head_section(content):
    """Extract content inside <head>."""
    m = re.search(r'<head[^>]*>(.*?)</head>', content, re.IGNORECASE | re.DOTALL)
    if m: return m.group(1).strip()
    return ''

def get_title(content):
    m = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else ''

def get_og_image(content):
    m = re.search(r'<meta\s+property="og:image"[^>]*content="([^"]+)"', content, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'<meta\s+name="og:image"[^>]*content="([^"]+)"', content, re.IGNORECASE)
    if m: return m.group(1)
    return ''

def remove_script_tags(text):
    """Remove <script>...</script> blocks."""
    return re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)

def remove_style_tags(text):
    """Remove <style>...</style> blocks."""
    return re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.IGNORECASE | re.DOTALL)

def extract_article_body(content):
    """
    Extract the main article body content from the source file.
    """
    def clean_body(t):
        """Remove known structural/wrapper elements from text."""
        t = re.sub(r'<nav[^>]*id="navbar".*?</nav>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<nav[^>]*class="dfl-mobile-nav".*?</nav>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<nav[^>]*aria-label="breadcrumb"[^>]*>.*?</nav>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<header[^>]*>', '', t, flags=re.IGNORECASE)
        t = re.sub(r'</header>', '', t, flags=re.IGNORECASE)
        t = re.sub(r'<main[^>]*>', '', t, flags=re.IGNORECASE)
        t = re.sub(r'</main>', '', t, flags=re.IGNORECASE)
        t = re.sub(r'<footer[^>]*class="site-footer".*?</footer>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<section[^>]*id="hero".*?</section>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<section[^>]*class="hero-story".*?</section>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<section[^>]*class="article-banner".*?</section>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="hero-wrap".*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*id="sub-nav"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="lang-switch".*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="meta"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="share"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="article-credibility".*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="footer-art".*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="cta"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="article-cta"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="article-footer"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="disclaimer"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove any existing in-content subscribe (we add our own)
        # Note: subscribe block has nested <div class="sub-input-wrap">, so we
        # must match both closing </div> tags to keep div balance
        t = re.sub(r'<div[^>]*class="in-content-subscribe"[^>]*>.*?</div>\s*</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<!--\s*SEO_PROFILE.*?-->', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<!--\s*DFL CANONICAL NAVBAR.*?-->', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<!--\s*Author / Updated block.*?-->', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<!--\s*═══ UNIFIED (HEADER|FOOTER).*?═══\s*-->', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<!--\s*═══ UNIFIED MOBILE NAV.*?═══\s*-->', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<!--\s*Navbar content will be dynamically.*?-->', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<script[^>]*>.*?</script>', '', t, flags=re.IGNORECASE | re.DOTALL)
        # Remove structural HTML comments
        t = re.sub(r'<!--\s*═══════════════════════════════════════*\s*-->', '', t)
        t = re.sub(r'\n{4,}', '\n\n', t)
        return t.strip()

    def find_innermost_article_body(text):
        pattern = r'<article\s+class="article-body"[^>]*>'
        end_pattern = r'</article>'
        starts = [m.end() for m in re.finditer(pattern, text, re.IGNORECASE)]
        if not starts: return None, text
        ends = [m.start() for m in re.finditer(end_pattern, text, re.IGNORECASE)]
        if not ends: return None, text
        if len(starts) == 1:
            return text[starts[0]:ends[-1]].strip(), text
        if len(starts) > 1:
            inner_start = starts[-1]
            for end_pos in ends:
                if end_pos > inner_start:
                    return text[inner_start:end_pos].strip(), text
        return None, text

    m = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
    if not m: return ''
    body = m.group(1)
    inner, _ = find_innermost_article_body(body)
    if inner and len(inner) > 50:
        result = clean_body(inner)
        if len(result) > 50: return result
    elif inner and len(inner) > 0:
        result = clean_body(inner)
        if len(result) > 50: return result
    return clean_body(body)


def get_meta_from_json(filename, lang):
    """Look up article metadata from articles.json."""
    key = filename
    if key in ARTICLES_META: return ARTICLES_META[key]
    key = filename.replace('.html', '')
    if key in ARTICLES_META: return ARTICLES_META[key]
    return None

# ── JSON‑LD handling ──────────────────────────────────────────
def heal_corrupted_jsonld(head_text):
    def wrap_match(m):
        json_content = m.group(1).strip()
        return f'<script type="application/ld+json">\n{json_content}\n</script>'
    return re.sub(
        r'(?:^|\n)\s*(\{"@context":\s*"[^"]*".*?)\s*</script>',
        wrap_match, head_text, flags=re.IGNORECASE | re.DOTALL)

def extract_jsonld_blocks(head_text):
    return re.findall(
        r'<script\s+type="application/ld\+json"[^>]*>.*?</script>',
        head_text, re.IGNORECASE | re.DOTALL)

def normalize_jsonld_blocks(blocks):
    cleaned = []
    for block in blocks:
        raw = re.sub(r'<script[^>]*>', '', block, flags=re.IGNORECASE)
        raw = re.sub(r'</script>', '', raw, flags=re.IGNORECASE)
        raw = raw.strip()
        if raw:
            cleaned.append(f'<script type="application/ld+json">\n{raw}\n</script>')
    return cleaned

def clean_head(head_text):
    t = re.sub(r'<script[^>]*>.*?</script>', '', head_text, flags=re.IGNORECASE | re.DOTALL)
    t = re.sub(r'\s*</script>\s*', ' ', t)
    t = re.sub(r'\{"@context":\s*"[^"]*".*?(\}|</)', ' ', t, flags=re.IGNORECASE | re.DOTALL)
    t = re.sub(r'<link[^>]*href="[^"]*(global\.css|home\.css|articles\.css)[^"]*"[^>]*/?>', '', t, flags=re.IGNORECASE)
    t = re.sub(r'<link[^>]*googleapis[^>]*/?>', '', t, flags=re.IGNORECASE)
    t = re.sub(r'<link[^>]*gstatic[^>]*/?>', '', t, flags=re.IGNORECASE)
    t = re.sub(r'<meta\s+charset="UTF-8"[^>]*/?>', '', t, flags=re.IGNORECASE)
    t = re.sub(r'<meta\s+name="viewport"[^>]*/?>', '', t, flags=re.IGNORECASE)
    t = re.sub(r'<link\s+rel="?icon"?[^>]*/?>', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\n{3,}', '\n\n', t)
    return t.strip()

def clean_title(title):
    for suffix in [' | Dot For Life', ' | DOTFORLIFE', ' | DotForLife', ' | Dot4Life', ' | دوت فور لايف',
                   ' - Dot For Life', ' - DOTFORLIFE', ' - DotForLife',
                   ' DOTFORLIFE', ' Dot For Life', ' Dot4Life']:
        if title.endswith(suffix):
            title = title[:-len(suffix)]
            break
    return title.strip()

def look_for_image_in_body(content):
    m = re.search(r'<img[^>]*class="hero-img"[^>]*src="([^"]+)"', content, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'<img[^>]*class="hero-banner-img"[^>]*src="([^"]+)"', content, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'<section[^>]*class="hero-story"[^>]*style="[^"]*background[^"]*url\(([^)]+)\)', content, re.IGNORECASE)
    if m: return m.group(1)
    return ''

# ── NEW: generate_read_time ──────────────────────────────────
def estimate_read_time(article_body, lang='ar'):
    """Estimate reading time based on word count."""
    words = len(re.findall(r'\b\w+\b', article_body))
    wpm = 130 if lang == 'ar' else 200
    mins = max(1, round(words / wpm))
    if lang == 'en':
        return f'{mins} min read'
    mins_ar = ['١','٢','٣','٤','٥','٦','٧','٨','٩','١٠','١١','١٢','١٣','١٤','١٥']
    mins_str = mins_ar[mins-1] if 1 <= mins <= 15 else str(mins)
    return f'{mins_str} دقائق قراءة'

# ── NEW: generate_toc ────────────────────────────────────────
def generate_toc(article_body, dir_='rtl'):
    """Extract H2/H3 from article body and build TOC HTML."""
    toc_items = []
    headings = re.findall(r'<(h2|h3)[^>]*>(.*?)</\1>', article_body, re.IGNORECASE | re.DOTALL)
    for tag, content in headings:
        # Clean HTML tags from heading text for TOC display
        text = re.sub(r'<[^>]+>', '', content).strip()
        if not text: continue
        # Create slug from text
        slug = re.sub(r'[^\w\s-]', '', text)
        slug = re.sub(r'[-\s]+', '-', slug).strip('-').lower()[:60]
        toc_items.append({'tag': tag, 'text': text, 'slug': slug})

    if not toc_items:
        return '', ''

    # Build TOC HTML
    toc_html = '<div class="sidebar-module sidebar-toc">\n'
    toc_html += '  <h4>📑 <span class="en">Contents</span><span class="ar">المحتويات</span></h4>\n'
    for item in toc_items:
        cls = 'toc-item'
        if item['tag'] == 'h3':
            cls += ' toc-item-h3'
        toc_html += f'  <a href="#{item["slug"]}" class="{cls}">{item["text"]}</a>\n'
    toc_html += '</div>'

    # Also annotate the actual headings with IDs
    # Use a simpler approach: rebuild each heading with an id
    def add_heading_id(m):
        full = m.group(0)
        tag = m.group(1)
        attrs = m.group(2) or ''
        content = m.group(3)
        text = re.sub(r'<[^>]+>', '', content).strip()
        slug = re.sub(r'[^\w\s-]', '', text)
        slug = re.sub(r'[-\s]+', '-', slug).strip('-').lower()[:60]
        return f'<{tag} id="{slug}">{content}</{tag}>'

    body_with_ids = re.sub(
        r'<(h2|h3)(\s+[^>]*)?>(.*?)</\1>',
        add_heading_id,
        article_body,
        flags=re.IGNORECASE | re.DOTALL
    )

    return toc_html, body_with_ids


# ── NEW: find_related_articles ────────────────────────────────
def find_related_articles(meta_record, filename, lang='ar', max_items=4):
    """Find related articles from same category, excluding current."""
    if not meta_record: return []
    category = meta_record.get('category', '')
    if not category: return []

    results = []
    current_url = meta_record.get('url', '')
    current_en_url = meta_record.get('url_en', '')

    for a in ARTICLES_META.values():
        if not isinstance(a, dict): continue
        if a.get('category') != category: continue
        url = a.get('url', '')
        url_en = a.get('url_en', '')
        if url == current_url or url_en == current_en_url: continue
        if url == current_en_url or url == current_url: continue
        if url not in results and url_en not in results:
            results.append(a)

    # Remove duplicates by URL
    seen = set()
    unique = []
    for a in results:
        u = a.get('url', '')
        if u not in seen:
            seen.add(u)
            unique.append(a)

    return unique[:max_items]


# ── NEW: find_related_tools ──────────────────────────────────
def find_related_tools(meta_record, lang='ar'):
    """Find tools related to article category."""
    if not meta_record: return DEFAULT_TOOLS
    category = meta_record.get('category', '')
    tools = CATEGORY_TOOLS.get(category, DEFAULT_TOOLS)
    return tools


# ── NEW: generate_sidebar ────────────────────────────────────
def generate_sidebar(toc_html, meta_record, lang, dir_, filename):
    """Build the full sidebar HTML (Team card → TOC → Related → Tools → Friday → Ad)."""
    parts = []

    # 1. Team card (trust/E-E-A-T) — FIRST per user spec
    team_logo = '/assets/images/logo1-footer.webp'
    team_name_en = 'Dot4Life Team'
    team_name_ar = 'فريق دوت فور لايف'
    trust_en = 'Trusted content, carefully edited for Gulf families.'
    trust_ar = 'محتوى موثوق، محرَّر بعناية للأسرة الخليجية.'

    parts.append(f'''<div class="sidebar-module sidebar-team-card">
  <img src="{team_logo}" alt="DOTFORLIFE" width="56" height="56" loading="lazy">
  <div class="team-name"><span class="en">{team_name_en}</span><span class="ar">{team_name_ar}</span></div>
  <div class="team-trust"><span class="en">{trust_en}</span><span class="ar">{trust_ar}</span></div>
  <a href="/editorial-standards.html" class="team-link"><span class="en">Our Standards →</span><span class="ar">معاييرنا التحريرية ←</span></a>
</div>''')

    # 2. TOC (second)
    if toc_html:
        parts.append(toc_html)

    # 3. Related articles
    rel_articles = find_related_articles(meta_record, filename, lang)
    if rel_articles:
        related_html = '<div class="sidebar-module sidebar-related">\n'
        related_html += '  <h4><span class="en">Related</span><span class="ar">ذات صلة</span></h4>\n'
        for a in rel_articles:
            a_url = a.get('url', '#')
            a_title = a.get('title_ar' if lang == 'ar' else 'title_en', '')
            a_img = a.get('img', '')
            if not a_title: continue
            related_html += f'  <a href="{a_url}" class="sidebar-related-item">\n'
            if a_img:
                related_html += f'    <img src="{a_img}" alt="" width="64" height="48" loading="lazy">\n'
            else:
                related_html += '    <img src="/assets/images/hero.webp" alt="" width="64" height="48" loading="lazy">\n'
            related_html += f'    <span class="related-title">{a_title}</span>\n'
            related_html += '  </a>\n'
        related_html += '</div>'
        parts.append(related_html)

    # 4. Related tools
    tools = find_related_tools(meta_record, lang)
    tools_html = '<div class="sidebar-module sidebar-tools">\n'
    tools_html += '  <h4>🛠 <span class="en">Tools</span><span class="ar">أدوات</span></h4>\n'
    for tool in tools:
        label = tool.get('label_ar' if lang == 'ar' else 'label_en', '')
        tools_html += f'  <a href="{tool["url"]}" class="tool-btn">{label}</a>\n'
    tools_html += '</div>'
    parts.append(tools_html)

    # Contextual sidebar = Team card → TOC → Related → Tools ONLY.
    # (Newsletter + Ad intentionally removed per approved spec — no duplication.)
    return '\n\n'.join(parts)


# ── NEW: generate_article_end ────────────────────────────────
def generate_article_end(lang, meta_record, filename, canonical_url):
    """Build article-end sections: share → tool CTA → read-also → friday CTA → tags."""
    parts = []

    # Share icons
    encoded_url = canonical_url.replace('&', '%26').replace('?', '%3F')
    share_title = meta_record.get('title_ar' if lang == 'ar' else 'title_en', 'Article') if meta_record else 'Article'

    parts.append(f'''<div class="article-share">
  <a href="https://wa.me/?text={share_title}%20{encoded_url}" target="_blank" rel="noopener" class="share-btn whatsapp" aria-label="Share on WhatsApp">
    <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
    <span>WhatsApp</span>
  </a>
  <a href="https://twitter.com/intent/tweet?text={share_title}&url={encoded_url}" target="_blank" rel="noopener" class="share-btn x" aria-label="Share on X">
    <svg viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
    <span>X</span>
  </a>
  <a href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank" rel="noopener" class="share-btn facebook" aria-label="Share on Facebook">
    <svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
    <span>Facebook</span>
  </a>
  <button class="share-btn copy-link" onclick="navigator.clipboard.writeText(location.href);var s=this.querySelectorAll('span');if(s.length>1){{s[0].textContent='✓ Copied';s[1].textContent='✓ نُسخ'}}" aria-label="Copy link">
    <svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg>
    <span class="en">Copy</span><span class="ar">نسخ</span>
  </button>
</div>''')

    # Tool CTA
    tools = find_related_tools(meta_record, lang)
    if tools:
        tool = tools[0]
        label = tool.get('label_ar' if lang == 'ar' else 'label_en', 'Tool')
        cta_title_en = f'Try Our {label}'
        cta_title_ar = f'جرّب {label}'
        cta_desc_en = 'Calculate, plan, and take control of your family finances.'
        cta_desc_ar = 'احسب، خطّط، وتحكّم في مالية أسرتك.'
        parts.append(f'''<div class="article-tool-cta">
  <h3><span class="en">{cta_title_en}</span><span class="ar">{cta_title_ar}</span></h3>
  <p><span class="en">{cta_desc_en}</span><span class="ar">{cta_desc_ar}</span></p>
  <a href="{tool['url']}" class="tool-cta-btn"><span class="en">Open Tool →</span><span class="ar">فتح الأداة ←</span></a>
</div>''')

    # Read also grid
    rel_articles = find_related_articles(meta_record, filename, lang, max_items=4)
    if rel_articles:
        read_html = '<div class="article-read-also">\n'
        read_html += '  <h3><span class="en">📖 Read Also</span><span class="ar">📖 اقرأ أيضاً</span></h3>\n'
        read_html += '  <div class="read-also-grid">\n'
        for a in rel_articles:
            a_url = a.get('url', '#')
            a_title = a.get('title_ar' if lang == 'ar' else 'title_en', '')
            a_img = a.get('img', '')
            if not a_title: continue
            read_html += f'    <a href="{a_url}" class="read-also-card">\n'
            if a_img:
                read_html += f'      <img src="{a_img}" alt="" loading="lazy">\n'
            else:
                read_html += '      <img src="/assets/images/hero.webp" alt="" loading="lazy">\n'
            read_html += f'      <span class="read-also-title">{a_title}</span>\n'
            read_html += '    </a>\n'
        read_html += '  </div>\n</div>'
        parts.append(read_html)

    # Friday message CTA
    parts.append(f'''<div class="article-friday-cta">
  <h3>📬 <span class="en">Friday Family Tips</span><span class="ar">نصائح الجمعة للأسرة</span></h3>
  <p><span class="en">Get weekly inspiration delivered to your inbox.</span><span class="ar">احصل على إلهام أسبوعي في بريدك.</span></p>
  <div class="friday-input-wrap">
    <input type="email" placeholder="your@email.com" aria-label="Email">
    <button onclick="alert('🚧 Coming soon — signup integration.')"><span class="en">Join</span><span class="ar">اشترك</span></button>
  </div>
</div>''')

    # Tags
    category = meta_record.get('category', '') if meta_record else ''
    tags = CATEGORY_TAGS.get(category, [category] if category else [])
    if tags:
        tags_html = '<div class="article-tags">\n'
        for t in tags:
            tags_html += f'  <span class="tag">#{t}</span>\n'
        tags_html += '</div>'
        parts.append(tags_html)

    return '\n\n'.join(parts)


# ── NEW: generate_in_content_subscribe ────────────────────────
def generate_in_content_subscribe(lang='ar'):
    return f'''<div class="in-content-subscribe">
  <h3>📬 <span class="en">Enjoying this article?</span><span class="ar">هل يعجبك المقال؟</span></h3>
  <p><span class="en">Get more family tips every Friday — join our newsletter.</span><span class="ar">احصل على نصائح أسرية كل جمعة — اشترك في نشرتنا.</span></p>
  <div class="sub-input-wrap">
    <input type="email" placeholder="your@email.com" aria-label="Email">
    <button onclick="alert('🚧 Coming soon — signup integration.')"><span class="en">Subscribe</span><span class="ar">اشترك</span></button>
  </div>
</div>'''


# ── NEW: insert at mid-article ────────────────────────────────
def insert_subscribe_mid_article(body_html, lang='ar'):
    """Insert in-content subscribe box roughly at the 50% mark."""
    subscribe = generate_in_content_subscribe(lang)
    # Find the second h2, or at 50% by char count
    h2s = list(re.finditer(r'<h2[^>]*>.*?</h2>', body_html, re.IGNORECASE | re.DOTALL))
    if len(h2s) >= 2:
        insert_at = h2s[len(h2s)//2].start()
    else:
        insert_at = len(body_html) // 2
    return body_html[:insert_at] + '\n\n' + subscribe + '\n\n' + body_html[insert_at:]


# ── UPDATED: build_banner_html ────────────────────────────────
def build_banner_html(title, og_image, lang, dir_, meta_record, article_body=''):
    """Build banner inside container with H1 overlay, category, date, reading time."""
    # Image: prefer meta_record img, but override pig images
    img = '/assets/images/hero.webp'
    if meta_record and meta_record.get('img'):
        img = meta_record['img']
    elif og_image:
        img = og_image

    # 🐷 Replace haram piggy-bank images with modest savings images
    # Known piggy-bank Unsplash URLs to replace
    if img and ('photo-1607863680198' in img or 'photo-1560518883' in img):
        img = '/assets/images/articles/featured-stories-gulf-father-money-lessons.webp'
    elif img and any(p in img.lower() for p in ['pig', 'piggy', 'hog', 'swine']):
        img = '/assets/images/articles/featured-stories-gulf-father-money-lessons.webp'

    title = clean_title(title)
    reading_time = estimate_read_time(article_body, lang) if article_body else \
                   ('8 min read' if lang == 'en' else '٨ دقائق قراءة')

    # Date formatting
    date_str = ''
    if meta_record and meta_record.get('date'):
        raw_date = meta_record['date']
        try:
            dt = datetime.strptime(raw_date, '%Y-%m-%d')
            if lang == 'en':
                date_str = dt.strftime('%b %d, %Y')
            else:
                months_ar = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                             'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
                date_str = f"{dt.day} {months_ar[dt.month-1]} {dt.year}"
        except:
            date_str = raw_date

    section = meta_record.get('section', '') if meta_record else ''
    section_ar = meta_record.get('section_ar', section) if meta_record else section
    cat_display = section_ar if lang == 'ar' else section
    if not cat_display:
        cat_display = 'مقال' if lang == 'ar' else 'Article'

    # Alignments are handled by CSS logical properties (text-align:start, justify-content:start)
    return f'''<section class="article-banner" aria-label="Article banner">
  <div class="article-banner-img-wrap">
    <img src="{img}" alt="" class="article-banner-img" width="1200" height="420" loading="eager" fetchpriority="high">
    <div class="article-banner-overlay">
      <div class="article-banner-cat">{cat_display}</div>
      <h1 class="article-banner-title">{title}</h1>
      <div class="article-banner-meta">
        {f'<span>{date_str}</span>' if date_str else ''}
        <span>{reading_time}</span>
      </div>
    </div>
  </div>
</section>'''


# ── Structural safety gate ────────────────────────────────────
def div_balanced(html_fragment):
    """Return (ok, opens, closes) for <div>/</div> balance in a fragment."""
    opens = len(re.findall(r'<div(?:\s[^>]*)?>', html_fragment, re.IGNORECASE))
    closes = len(re.findall(r'</div\s*>', html_fragment, re.IGNORECASE))
    return opens == closes, opens, closes

def structure_valid(full_page):
    """Browser-grade check: <aside class="article-sidebar"> MUST be a direct
    child of <div class="article-layout">. Falls back to div-balance when
    html5lib is unavailable. Returns (ok, reason)."""
    try:
        import html5lib
    except ImportError:
        ok, o, c = div_balanced(full_page)
        return ok, f"div-balance {o}/{c} (install html5lib for full check)"
    doc = html5lib.parse(full_page, treebuilder="dom")
    asides = []
    def walk(n):
        for ch in n.childNodes:
            if ch.nodeType == 1:
                if 'article-sidebar' in (ch.getAttribute('class') or ''):
                    asides.append(ch)
                walk(ch)
    walk(doc)
    if not asides:
        return False, "no .article-sidebar found"
    p = asides[0].parentNode
    if 'article-layout' in (p.getAttribute('class') or ''):
        return True, "ok"
    pc = (p.getAttribute('class') or '').split(' ')[0]
    return False, f"sidebar nested under <{p.tagName.lower()} .{pc}> (source body likely has unbalanced tags)"


# ── MAIN: build_new_page ──────────────────────────────────────
def build_new_page(filename, content):
    """Transform an existing article into the complete unified template."""
    if has_template(content):
        return None  # Already migrated, idempotent

    lang, dir_, data_lang = get_html_attrs(content)
    title = get_title(content)
    og_image = get_og_image(content)
    body_img = look_for_image_in_body(content)
    article_body = extract_article_body(content)

    if not article_body or len(article_body) < 100:
        print(f"  ⚠️  Could not extract sufficient body content ({len(article_body)} chars)")
        return None

    # Safety: refuse to wrap a body whose <div> tags are unbalanced —
    # that is exactly what pushes the sidebar below the article.
    bal, o, c = div_balanced(article_body)
    if not bal:
        print(f"  ⛔ {filename}: source body has UNBALANCED <div> ({o} open / {c} close) — skipped. Fix the article content first.")
        return None

    meta_record = get_meta_from_json(filename, lang)
    html_attrs = f'lang="{lang}" dir="{dir_}" data-lang="{data_lang}" data-theme="light"'

    # ── Head ──
    css_links = f'''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Almarai:wght@300;400;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles/global.css?{CACHE_BUSTER}">
  <link rel="stylesheet" href="/styles/home.css?{CACHE_BUSTER}">
  <link rel="stylesheet" href="/styles/pages/articles.css?{CACHE_BUSTER}">'''

    init_script = '''<script>(function(){var p=new URLSearchParams(location.search),gd=(function(){try{var z=(Intl.DateTimeFormat().resolvedOptions().timeZone||"");return /Riyadh|Dubai|Qatar|Bahrain|Kuwait|Muscat|Baghdad|Amman|Beirut|Damascus|Aden|Cairo|Khartoum/i.test(z)?"ar":"en";}catch(e){return "ar";}})(),h=document.documentElement,l=p.get("lang")||localStorage.getItem("dfl-lang")||h.getAttribute("data-lang")||gd,t=p.get("theme")||localStorage.getItem("dfl-theme")||h.getAttribute("data-theme")||"light";h.setAttribute("data-theme",t);h.setAttribute("data-lang",l);h.setAttribute("lang",l);h.setAttribute("dir",l==="ar"?"rtl":"ltr");if(p.get("lang"))localStorage.setItem("dfl-lang",l);if(p.get("theme"))localStorage.setItem("dfl-theme",t);})()</script>'''

    # JSON-LD handling
    head_content = get_head_section(content)
    jsonld_raw = extract_jsonld_blocks(head_content)
    jsonld_intact = normalize_jsonld_blocks(jsonld_raw)
    head_for_healing = head_content
    for b in jsonld_raw:
        head_for_healing = head_for_healing.replace(b, '')
    healed = heal_corrupted_jsonld(head_for_healing)
    jsonld_new_raw = extract_jsonld_blocks(healed)
    jsonld_new = normalize_jsonld_blocks(jsonld_new_raw)
    preserved_head = clean_head(healed)
    jsonld_blocks = jsonld_intact + jsonld_new
    jsonld_html = '\n'.join(jsonld_blocks)

    new_head = f'''<head>
{init_script}
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
{preserved_head}
{jsonld_html}
{css_links}
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G1XPV4F0G"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-3G1XPV4F0G');</script>
</head>'''

    # ── Banner ──
    best_img = og_image or body_img or ''
    banner_html = build_banner_html(title, best_img, lang, dir_, meta_record, article_body)

    # ── TOC ──
    toc_html, body_with_ids = generate_toc(article_body, dir_)

    # ── In-content subscribe ──
    body_with_subscribe = insert_subscribe_mid_article(body_with_ids, lang)

    # ── Sidebar ──
    sidebar_html = generate_sidebar(toc_html, meta_record, lang, dir_, filename)

    # ── Article end ──
    canonical_url = f'https://dotforlife.com/{filename}' if not filename.startswith('/') else f'https://dotforlife.com{filename}'
    # Fix: get the actual canonical URL from the original page
    canonical_m = re.search(r'<link\s+rel="canonical"[^>]*href="([^"]+)"', content, re.IGNORECASE)
    if canonical_m:
        canonical_url = canonical_m.group(1)
    article_end_html = generate_article_end(lang, meta_record, filename, canonical_url)

    # ── Article-end JS (progress bar + TOC) ──
    # Reading direction for scroll offset
    toc_script = '''<script>
(function(){
  // Reading progress bar
  var bar = document.getElementById('reading-progress');
  if(bar){
    window.addEventListener('scroll',function(){
      var h = document.documentElement;
      var total = h.scrollHeight - h.clientHeight;
      var pct = (h.scrollTop || document.body.scrollTop) / (total || 1) * 100;
      bar.style.width = pct + '%';
    },{passive:true});
  }
  // TOC active highlight
  var tocLinks = document.querySelectorAll('.toc-item');
  if(tocLinks.length){
    var headings = [];
    tocLinks.forEach(function(link){
      var id = link.getAttribute('href').replace('#','');
      var el = document.getElementById(id);
      if(el) headings.push({el:el,link:link});
    });
    window.addEventListener('scroll',function(){
      var scrollY = window.scrollY + 130;
      var current = null;
      headings.forEach(function(h){
        if(h.el.offsetTop <= scrollY) current = h;
      });
      tocLinks.forEach(function(l){ l.classList.remove('is-active'); });
      if(current) current.link.classList.add('is-active');
    },{passive:true});
  }
})();
</script>'''

    # ── Assemble final page ──
    new_page = f'''<!DOCTYPE html>
<html {html_attrs}>
{new_head}
<body {TEMPLATE_MARKER}>

<div id="reading-progress" role="progressbar" aria-label="Reading progress"></div>

{HEADER_HTML}

<div class="article-wrap">

{banner_html}

<div class="article-layout">

<main class="article-main">
<article class="article-body">
{body_with_subscribe}
</article>

<div class="article-end">
{article_end_html}
</div>
</main>

<aside class="article-sidebar">
{sidebar_html}
</aside>

</div><!-- /article-layout -->

</div><!-- /article-wrap -->

{FOOTER_HTML}

<script src="/scripts/global.js?{CACHE_BUSTER}" defer></script>
{toc_script}
</body>
</html>'''

    return new_page


def main():
    base = BASE
    migrated = 0
    skipped = 0
    errors = 0
    total = 0

    for d in DIRS:
        dir_path = os.path.join(base, d)
        if not os.path.isdir(dir_path):
            print(f"⚠️  Directory not found: {d}")
            continue

        files = sorted([f for f in os.listdir(dir_path) if f.endswith('.html')])
        total += len(files)
        print(f"\n📁 {d}/ ({len(files)} files)")

        for fname in files:
            fpath = os.path.join(dir_path, fname)
            try:
                content = read_file(fpath)

                if has_template(content):
                    skipped += 1
                    continue

                result = build_new_page(fname, content)
                if result:
                    ok, why = structure_valid(result)
                    if not ok:
                        errors += 1
                        print(f"  ❌ {fname} — STRUCTURE CHECK FAILED: {why} (NOT written)")
                        continue
                    write_file(fpath, result)
                    verify = read_file(fpath)
                    if has_template(verify) and len(verify) > 500:
                        migrated += 1
                        print(f"  ✅ {fname}")
                    else:
                        errors += 1
                        print(f"  ❌ {fname} — verification failed")
                else:
                    skipped += 1
                    print(f"  ⏭️  {fname} (skipped)")

            except Exception as e:
                errors += 1
                print(f"  ❌ {fname} — {type(e).__name__}: {e}")

    print(f"\n{'='*55}")
    print(f"Total article files: {total}")
    print(f"✅ Migrated:         {migrated}")
    print(f"⏭️  Skipped:          {skipped}")
    print(f"❌ Errors:           {errors}")
    print(f"{'='*55}")


if __name__ == '__main__':
    main()
