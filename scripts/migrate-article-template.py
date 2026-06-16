#!/usr/bin/env python3
"""
Article Template Migration Script — v2
======================================
Applies the unified article template (header + banner + reading column + footer)
to ALL existing article files across the site.

Idempotent: checks for data-template="article" marker before modifying.
Safe to run multiple times.

Usage:
  python3 scripts/migrate-article-template.py
"""

import os, re, json, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_MARKER = 'data-template="article"'
CACHE_BUSTER = 'v=20260608t'

DIRS = [
    'featured-stories', 'comparisons', 'peace-capsules',
    'health', 'islamic-hajj-umrah', 'blog', 'guides'
]

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
    Strategy:
      1. Find <body>...</body>
      2. Remove all known structural elements
      3. Unwrap any <article class="article-body"> wrappers
         by finding the innermost one
      4. Return clean content
    """

    def clean_body(t):
        """Remove known structural/wrapper elements from text."""
        # Remove nav elements
        t = re.sub(r'<nav[^>]*id="navbar".*?</nav>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<nav[^>]*class="dfl-mobile-nav".*?</nav>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove footer
        t = re.sub(r'<footer[^>]*class="site-footer".*?</footer>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove hero/banner sections
        t = re.sub(r'<section[^>]*id="hero".*?</section>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<section[^>]*class="hero-story".*?</section>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<section[^>]*class="article-banner".*?</section>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove .hero-wrap
        t = re.sub(r'<div[^>]*class="hero-wrap".*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove lang-switch
        t = re.sub(r'<div[^>]*class="lang-switch".*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove inline .meta
        t = re.sub(r'<div[^>]*class="meta"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove share, credibility, footer-art
        t = re.sub(r'<div[^>]*class="share"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="article-credibility".*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="footer-art".*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove .cta, .article-cta, .article-footer, .disclaimer
        t = re.sub(r'<div[^>]*class="cta"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="article-cta"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="article-footer"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<div[^>]*class="disclaimer"[^>]*>.*?</div>', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove comment blocks
        t = re.sub(r'<!--\s*SEO_PROFILE.*?-->', '', t, flags=re.IGNORECASE | re.DOTALL)
        t = re.sub(r'<!--\s*═══ UNIFIED (HEADER|FOOTER).*?═══\s*-->', '', t, flags=re.IGNORECASE | re.DOTALL)

        # Remove empty .container wrapper
        t = re.sub(r'<div\s+class=["\']container["\'][^>]*>\s*', '', t)
        t = t.replace('</div><!-- /container -->', '')

        # Clean up excessive blank lines
        t = re.sub(r'\n{4,}', '\n\n', t)

        return t.strip()

    def find_innermost_article_body(text):
        """
        Find the innermost <article class="article-body">...</article> content.
        Uses a stack approach to handle nesting.
        Returns (inner_content, full_text_without_wrappers) or (None, original_text)
        """
        pattern = r'<article\s+class="article-body"[^>]*>'
        end_pattern = r'</article>'

        # Find all start and end positions
        starts = [m.end() for m in re.finditer(pattern, text, re.IGNORECASE)]
        if not starts:
            return None, text

        ends = [m.start() for m in re.finditer(end_pattern, text, re.IGNORECASE)]

        if len(starts) == 1 and len(ends) >= 1:
            # Only one wrapper, use the first closing tag
            return text[starts[0]:ends[0]].strip(), text

        if len(starts) > 1 and len(ends) >= len(starts):
            # Multiple wrappers — find innermost
            # The innermost has its opening tag after the second-to-last start
            # and its closing tag at the last end
            inner_start = starts[-1]
            inner_end = ends[-1]
            if inner_end > inner_start:
                return text[inner_start:inner_end].strip(), text

        return None, text

    # Find body content
    m = re.search(r'<body[^>]*>(.*?)</body>', content, re.IGNORECASE | re.DOTALL)
    if not m:
        return ''
    body = m.group(1)

    # First try to find innermost article-body and extract its content
    inner, _ = find_innermost_article_body(body)
    if inner and len(inner) > 50:
        # We found article-body content — clean it
        result = clean_body(inner)
        if len(result) > 50:
            return result
        # Fall through
    elif inner and len(inner) > 0:
        result = clean_body(inner)
        if len(result) > 50:
            return result

    # Fallback: clean the entire body
    return clean_body(body)


def get_meta_from_json(filename, lang):
    """Look up article metadata from articles.json."""
    key = filename
    if key in ARTICLES_META:
        return ARTICLES_META[key]
    # Try without extension
    key = filename.replace('.html', '')
    if key in ARTICLES_META:
        return ARTICLES_META[key]
    return None

def clean_title(title):
    """Remove site name suffix from title for cleaner H1 display."""
    for suffix in [' | Dot For Life', ' | DOTFORLIFE', ' | DotForLife', ' | Dot4Life', ' | دوت فور لايف',
                   ' - Dot For Life', ' - DOTFORLIFE', ' - DotForLife',
                   ' DOTFORLIFE', ' Dot For Life', ' Dot4Life']:
        if title.endswith(suffix):
            title = title[:-len(suffix)]
            break
    return title.strip()

def look_for_image_in_body(content):
    """Look for hero image src in article body."""
    m = re.search(r'<img[^>]*class="hero-img"[^>]*src="([^"]+)"', content, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'<img[^>]*class="hero-banner-img"[^>]*src="([^"]+)"', content, re.IGNORECASE)
    if m: return m.group(1)
    m = re.search(r'<section[^>]*class="hero-story"[^>]*style="[^"]*background[^"]*url\(([^)]+)\)', content, re.IGNORECASE)
    if m: return m.group(1)
    return ''

def build_banner_html(title, og_image, lang, dir_, meta_record):
    """Build full-width banner with image overlay, H1 title, and meta."""
    # Prefer articles.json img field, then og:image, then fallback
    img = '/assets/images/hero.webp'
    if meta_record and meta_record.get('img'):
        img = meta_record['img']
    elif og_image:
        img = og_image
    title = clean_title(title)
    
    # Determine reading time
    reading_time = '8 min read' if lang == 'en' else '٨ دقائق قراءة'
    
    # Section label
    if lang == 'en':
        section_label = 'Article'
        date_str = meta_record.get('date', '') if meta_record else ''
        if date_str:
            try:
                from datetime import datetime
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                date_str = dt.strftime('%b %d, %Y')
            except:
                pass
    else:
        section_label = 'مقال'
        date_str = meta_record.get('date', '') if meta_record else ''
        if date_str:
            try:
                from datetime import datetime
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                months_ar = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
                             'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
                date_str = f"{dt.day} {months_ar[dt.month-1]} {dt.year}"
            except:
                pass
    
    # Reading time from meta or estimate from title
    section = meta_record.get('section', '') if meta_record else ''
    section_ar = meta_record.get('section_ar', section) if meta_record else section
    
    overlay_text_align = 'right' if dir_ == 'rtl' else 'left'
    meta_justify = 'flex-end' if dir_ == 'rtl' else 'flex-start'
    
    cat_display = section_ar if lang == 'ar' else section
    if not cat_display:
        cat_display = section_label
    
    return f'''<section class="article-banner" aria-label="Article banner">
  <div class="article-banner-img-wrap">
    <img src="{img}" alt="" class="article-banner-img" width="1200" height="420" loading="eager" fetchpriority="high">
    <div class="article-banner-overlay" style="text-align:{overlay_text_align};">
      <div class="article-banner-cat" style="display:inline-block;color:#fff;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);border-radius:999px;padding:4px 14px;font-size:.72rem;font-weight:700;margin-bottom:.75rem;backdrop-filter:blur(4px);">{cat_display}</div>
      <h1 class="article-banner-title" style="font-size:clamp(1.5rem,3.5vw,2.2rem);line-height:1.4;font-weight:800;color:#fff;text-shadow:0 2px 20px rgba(0,0,0,.3);margin:0;">{title}</h1>
      <div class="article-banner-meta" style="color:rgba(255,255,255,.8);margin-top:.75rem;font-size:.8rem;display:flex;gap:.6rem;flex-wrap:wrap;justify-content:{meta_justify};">
        {f'<span>{date_str}</span>' if date_str else ''}
        <span>{reading_time}</span>
      </div>
    </div>
  </div>
</section>'''


def build_new_page(filename, content):
    """Transform an existing article into the unified template."""
    if has_template(content):
        return None  # Already migrated, idempotent
    
    lang, dir_, data_lang = get_html_attrs(content)
    title = get_title(content)
    og_image = get_og_image(content)
    # Also look for image in article body (hero-img, hero-banner-img)
    body_img = look_for_image_in_body(content)
    article_body = extract_article_body(content)
    
    # If we couldn't extract enough body content, skip
    # A valid article should have at least some paragraphs
    if not article_body or len(article_body) < 100:
        print(f"  ⚠️  Could not extract sufficient body content ({len(article_body)} chars)")
        return None
    
    # Get meta from articles.json
    meta_record = get_meta_from_json(filename, lang)
    
    # Build html tag attributes
    html_attrs = f'lang="{lang}" dir="{dir_}" data-lang="{data_lang}" data-theme="light"'
    
    # Build CSS links
    css_links = '''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Almarai:wght@300;400;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles/global.css?''' + CACHE_BUSTER + '''">
  <link rel="stylesheet" href="/styles/home.css?''' + CACHE_BUSTER + '''">
  <link rel="stylesheet" href="/styles/pages/articles.css?''' + CACHE_BUSTER + '''">'''
    
    # Build the lang/theme script (same as other pages)
    init_script = '''<script>(function(){var p=new URLSearchParams(location.search),gd=(function(){try{var z=(Intl.DateTimeFormat().resolvedOptions().timeZone||"");return /Riyadh|Dubai|Qatar|Bahrain|Kuwait|Muscat|Baghdad|Amman|Beirut|Damascus|Aden|Cairo|Khartoum/i.test(z)?"ar":"en";}catch(e){return "ar";}})(),l=p.get("lang")||localStorage.getItem("dfl-lang")||gd,t=p.get("theme")||localStorage.getItem("dfl-theme")||"light",h=document.documentElement;h.setAttribute("data-theme",t);h.setAttribute("data-lang",l);h.setAttribute("lang",l);h.setAttribute("dir",l==="ar"?"rtl":"ltr");if(p.get("lang"))localStorage.setItem("dfl-lang",l);if(p.get("theme"))localStorage.setItem("dfl-theme",t);})()</script>'''
    
    # Extract existing head content, removing scripts we'll replace
    head_content = get_head_section(content)
    
    # Remove any existing init scripts, css links, font links, gtag, adsense from head
    # We'll keep: title, meta tags, canonical, alternate hreflangs, JSON-LD, og tags
    lines_to_keep = []
    for line in head_content.split('\n'):
        stripped = line.strip()
        # Skip lines we'll replace
        if 'pagead2.googlesyndication.com' in stripped: continue
        if 'googletagmanager.com' in stripped: continue
        if 'googleapis.com' in stripped or 'gstatic.com' in stripped: continue
        if stripped.startswith('<script'): continue
        # Skip CSS links we'll replace (global, home, articles)
        if stripped.startswith('<link rel="stylesheet"'):
            if all(x not in stripped for x in ['global.css', 'home.css', 'articles.css']):
                lines_to_keep.append(line)
            continue
        # Skip other CSS-related lines we'll replace
        if 'googleapis.com' in stripped or 'gstatic.com' in stripped: continue
        lines_to_keep.append(line)
    
    # Rebuild head content - filter out duplicate meta tags already added
    filtered_lines = []
    for line in lines_to_keep:
        stripped = line.strip()
        # Skip duplicate meta tags already in new head
        if '<meta charset=' in stripped: continue
        if '<meta name="viewport"' in stripped: continue
        filtered_lines.append(line)
    preserved_head = '\n'.join(filtered_lines).strip()
    
    # Build the head section
    new_head = f'''<head>
{init_script}
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
{preserved_head}
{css_links}
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1436107577087160" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-3G1XPV4F0G"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-3G1XPV4F0G');</script>
</head>'''
    
    # Build banner with best available image
    # Priority: articles.json img > og:image > body hero image > fallback
    best_img = og_image or body_img or ''
    banner_html = build_banner_html(title, best_img, lang, dir_, meta_record)
    
    # Article content direction
    reading_align = 'right' if dir_ == 'rtl' else 'left'
    dir_attr = f'dir="{dir_}"' if dir_ else ''
    
    # Build the final page
    new_page = f'''<!DOCTYPE html>
<html {html_attrs}>
{new_head}
<body {TEMPLATE_MARKER}>

{HEADER_HTML}

{banner_html}

<article class="article-body">
{article_body}
</article>

{FOOTER_HTML}

<script src="/scripts/global.js?{CACHE_BUSTER}" defer></script>
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
                    write_file(fpath, result)
                    # Verify
                    verify = read_file(fpath)
                    if has_template(verify) and len(verify) > 500:
                        migrated += 1
                        print(f"  ✅ {fname}")
                    else:
                        errors += 1
                        print(f"  ❌ {fname} — verification failed (template marker: {has_template(verify)}, len: {len(verify)})")
                else:
                    skipped += 1
                    print(f"  ⏭️  {fname} (skipped — no body extracted or already processed)")
                    
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
