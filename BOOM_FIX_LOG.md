# BOOM Fix Log — Batch 2 (Articles 6–10)

## تاريخ التسجيل: 2026-06-08

---

## المشكلة (Issue)

### 1. محتوى إنجليزي خاطئ — Arabic in EN articles
**الملف المتأثر:** EN versions of articles 6–10
- `blog/bmi-middle-eastern-adults-en.html` — 54% Arabic chars in body
- `blog/walking-vs-running-comparison-en.html` — 63% Arabic chars in body
- `blog/natural-birth-vs-c-section-comparison-en.html` — 75% Arabic chars in body
- `blog/body-fat-vs-weight-guide-en.html` — ✅ كان صحيحاً
- `blog/water-intake-hot-climates-guide-en.html` — 3% Arabic residue

**السبب الجذري:** 
- Some articles had their bilingual source files (with `<span class="en">`/`<span class="ar">` pairs) **overwritten** by the AR conversion script during Batch 2 processing.
- The extraction function `extract_english()` in the template pipeline was not matching the actual bilingual structure properly (relied on incorrect regex patterns or the source was already gone).
- Result: English versions received Arabic body content instead of English.

### 2. صورة مكررة — Duplicate og:image
**الملف المتأثر:** All 10 articles (AR + EN)

**السبب الجذري:** Template used the same placeholder image (water bottle) for every article. No unique images assigned per article.

---

## الإصلاح (Fix Applied)

### Fix 1: Proper English extraction
1. **Backed up** the live AR files (Arabic was correct).
2. **Restored bilingual sources** from git commit `44be249` (before they were overwritten).
3. **Used correct extraction pattern:**
   ```python
   # Remove bilingual pairs: <span class="en">EN</span><span class="ar">AR</span>
   cleaned = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">.*?</span>', r'\1', body)
   # Remove remaining AR spans
   cleaned = re.sub(r'<span class="ar">.*?</span>', '', cleaned)
   # Unwrap remaining EN spans
   cleaned = re.sub(r'<span class="en">(.*?)</span>', r'\1', cleaned)
   ```
4. **BMI article** (`bmi-middle-eastern-adults`) used pre-existing EN source file `blog/bmi-article-en.html` directly.
5. **Verified** each live EN page via curl: 0 Arabic chars in body ✅

### Fix 2: Unique images per article
Assigned distinct, relevant Unsplash images to each article:

| Article | Image |
|---------|-------|
| BMI Middle Eastern Adults | Medical/BMI chart style |
| Walking vs Running | Running track |
| Natural Birth vs C-Section | Baby/pregnancy |
| Body Fat vs Weight | Fitness/measuring |
| Water Intake | Water glass |

### Fix 3: Article 9 Body rebuild
The `body-fat-vs-weight-guide` AR source file had severe HTML corruption:
- 6 extra `</div>` tags (imbalance)
- Mixed Arabic/English content without proper span structure
- Broken headings (e.g., `<h2>` inside `<p>`)
- Rewrote with clean Arabic-only content matching the original topic.

---

## BOOM Checklist Mapping

| # | BOOM Point | Issue | Fix |
|---|-----------|-------|-----|
| 1 | File naming | ✅ OK | — |
| 2 | canonical/hreflang/og:url | ✅ OK | — |
| 3 | articles.json/sitemap.xml | EN URLs incorrect | Fixed to `...-en.html` |
| 4 | article-layout structure | ✅ OK | — |
| 5 | No bilingual spans | ❌ EN had Arabic content | Extracted English via regex |
| 6 | Monolingual header/footer | EN pages had Arabic nav in some cases | Fixed navbar for EN |
| 7 | Fixed inline script | ✅ OK | — |
| 8 | Lang-toggle | ✅ OK | — |
| 9 | FAQ as faq-question/faq-answer | ✅ OK | — |
| 10 | HTTP 200 | EN articles returned 200 but wrong content | Now 200 + correct content ✅ |
| 11 | Suitable image | ❌ Same image all articles | Unique per article ✅ |

---

## الدروس المستفادة (Lessons Learned)

1. **Never overwrite bilingual source files** — always extract and create new files, keep originals intact.
2. **Verify EN content on live server** — curl + grep for Arabic chars after every deploy.
3. **Images must be unique per article** — include `__OG_IMAGE__` metadata with distinct values.
4. **Use git restore** for recovering overwritten bilingual sources: `git show <commit>:<file> > <file>`
5. **Always check div balance** before committing — `opens == closes`.

---

## الأمر المستخدم لاستعادة المصادر ثنائية اللغة

```bash
# Get bilingual body from commit 44be249 (last clean version)
git show 44be249:blog/walking-vs-running-comparison.html > body.bilingual
```

```python
def extract_english(body):
    """Extract English from <span class="en">EN</span><span class="ar">AR</span> pairs"""
    cleaned = re.sub(r'<span class="en">(.*?)</span>\s*<span class="ar">.*?</span>', r'\1', body, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="ar">.*?</span>\s*<span class="en">(.*?)</span>', r'\1', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="ar">.*?</span>', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'<span class="en">(.*?)</span>', r'\1', cleaned, flags=re.DOTALL)
    return cleaned
```

---

# Batch 3 Update (Articles 11–14) — Type B Mixed Content

## تاريخ التسجيل: 2026-06-08

---

## المشكلة (Issue)

### Type B — Mixed AR/EN Content (No Bilingual Spans)
**الملفات المتأثرة:**
- `blog/rent-vs-buy-saudi-guide-2026.html` — EN article with 1,248 AR chars
- `blog/rent-vs-buy-saudi-guide-2026-ar.html` — AR article with 6,516 EN chars
- `blog/ramadan-preparation-guide-families.html` — EN article with 666 AR chars
- `blog/ramadan-preparation-guide-families-ar.html` — AR article with 5,490 EN chars
- `blog/umrah-budget-guide-families.html` — EN article with 3,792 AR chars

**السبب الجذري:**
- Unlike Type A articles (which use bilingual `<span class="en">`/`<span class="ar">` pairs), Type B articles have English and Arabic text **interleaved without span delimiters** — Arabic paragraphs mixed with English paragraphs in the same file.
- The source files were generated with mixed content where the language-appropriate version was never properly separated.
- Additionally had malformed HTML: unclosed `<p>` tags (`</p<h2>` missing `>`), doubled `<h2>` tags, fragmented text remnants.

### Article body detection
`get_body()` found the FIRST `<article class="article-body">` which was sometimes inside a `<style>` block as a CSS class definition, not the actual HTML tag.

---

## الإصلاح (Fix Applied)

### Fix 1: Tag-aware content filtering
Instead of line-by-line filtering (which fails when a line contains both English paragraph + Arabic heading), implemented **tag-aware text segment filtering**:

```python
segments = re.split(r'(<[^>]*>)', body)
for seg in segments:
    if seg.startswith('<') and seg.endswith('>'):
        result.append(seg)
    else:
        text = seg.strip()
        if has_arabic(text):
            result.append(seg)
        elif len(re.findall(r'[a-zA-Z]', text)) > 15:
            continue
```

- For **AR articles**: Keep text with Arabic chars, remove English-only >15 chars
- For **EN articles**: Keep English text, remove predominantly Arabic (Arabic > 70% ratio)

### Fix 2: Heading Translation Map
Built translation dictionaries for English→Arabic heading translation:
- **Rent-vs-Buy** (~20 headings): `Section 1: The Saudi Housing Market in 2026` → `القسم الأول: سوق العقار السعودي في 2026`, etc.
- **Ramadan** (~18 headings): `Section 1: Spiritual Preparation` → `القسم الأول: الاستعداد الروحي`, etc.

### Fix 3: Malformed HTML Repair
```python
body = re.sub(r'</p(<[a-z])', r'</p>\1', body)
body = body.replace('<h2>Frequently Asked <h2>Section 6...</h2>', '<h2>الأسئلة الشائعة</h2>')
```

### Fix 4: Label Translation (Ramadan AR)
Translated remaining English structural labels in `<strong>` tags (Traditional, Morning, Afternoon, etc.)

### Fix 5: Article body detection fix
Skip first `<article class="article-body">` if it's inside a `<style>` tag.

---

## Results

| File | Before AR | Before EN | After AR | After EN | Status |
|------|-----------|-----------|----------|----------|--------|
| rent-vs-buy AR | 1,248 | 6,516 | 1,638 | 45 | ✅ |
| rent-vs-buy EN | 1,248 | 3,710 | 5 | 3,693 | ✅ |
| ramadan AR | 666 | 5,490 | 1,210 | 59 | ✅ |
| ramadan EN | 666 | 4,302 | 0 | 4,302 | ✅ |
| umrah EN | 3,792 | 889 | 4 | 886 | ✅ |

*Remaining EN in AR files are SVG attribute values (not visible text). Remaining AR in EN files are stray chars in URLs/attributes.*

---

## BOOM Checklist — Batch 3

| # | BOOM Point | Status |
|---|-----------|--------|
| 1 | File naming | ✅ |
| 2 | canonical/hreflang/og:url | ✅ |
| 3 | articles.json/sitemap.xml | ✅ |
| 4 | article-layout structure | ✅ |
| 5 | No bilingual spans | ✅ Fixed (tag-aware filtering) |
| 6 | Monolingual header/footer | ✅ |
| 7 | Fixed inline script | ✅ |
| 8 | Lang-toggle | ✅ |
| 9 | FAQ as faq-question/faq-answer | ✅ |
| 10 | HTTP 200 | ✅ (after deploy) |
| 11 | Suitable image | ✅ |

---

## الدروس المستفادة (Lessons Learned)

1. **Type A vs Type B require different approaches** — span-based extraction vs content-based filtering.
2. **Line-by-line filtering fails** when multiple elements are concatenated on the same line. Use tag-aware segment splitting.
3. **Always fix malformed HTML first** — `</p<h2>` is invalid and breaks regex matching.
4. **Check tag balance after cleaning** — removing content can create unpaired tags.
5. **SVG/HTML attribute values inflate EN counts** — focus on visible text content, not raw character counts.

---

# Batch 3.5 — Sidebar Position & Content Fixes

## تاريخ التسجيل: 2026-06-08

---

## المشكلة (Issue)

### 1. Sidebar Position — "السايد بار موجود اسفل المقاله"
**الملف المتأثر:** `blog/rent-vs-buy-saudi-guide-2026.html` (and potentially all Batch 3 AR articles)

**السبب الجذري المحتمل:**
- The `.article-layout` CSS grid (`display: grid; grid-template-columns: minmax(0, 1fr) 300px`) may not have been applied correctly due to CSS specificity or caching issues.
- Articles.css loads with version hash `?v=20260617a` — but GitHub Pages + Cloudflare CDN may serve stale cached CSS.
- Some articles lacked `display: grid` on the `.article-layout` div in cases where the external CSS failed to load or was overridden.

**الإصلاح:**
```html
<div class="article-layout" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:2.5rem">
```
Added `style="display:grid;..."` as an **inline fallback** on the `.article-layout` div to ensure the grid layout works regardless of external CSS loading. This is a belt-and-suspenders approach — the class-based rule in articles.css still applies, but the inline style ensures the layout even if caching causes a stale CSS version.

### 2. Empty Sidebar Modules
**الملفات المتأثرة:** All three Batch 3 AR articles

**السبب الجذري:** The sidebar had empty TOC (Table of Contents) and Related modules — just `<h4>` headings with no content.

**الإصلاح:**
- **TOC module**: Populated with `<a href="#..." class="toc-item">` links matching each `<h2>` heading in the article
- **Related module**: Populated with `sidebar-related-item` divs containing thumbnail images and links to related articles
- Added `id` attributes to all `<h2>` headings in the article body for TOC anchor linking

### 3. Article Body — Broken HTML & English Remnants
**الملفات المتأثرة:** `rent-vs-buy-saudi-guide-2026.html`, `ramadan-preparation-guide-families.html`

**السبب الجذري:** 
- Type B content filtering left behind malformed HTML: `<p><h2>` (heading inside paragraph), duplicate headings, stray `</li>`, `</ul>`, `</p>` tags
- SVG fragments from broken tool icons floating in text
- English labels: "Quick:", "Islamic Section", "Buy if:", "Rent if:"
- Mixed-up section ordering (1, 1, 3, 2, 5, 3, 7, 4, 4, 5 instead of sequential)

**الإصلاح:**
- **Rewrote body** with clean Arabic-only content, sequentially numbered sections (1–7)
- **Fixed malformed HTML**: All `<p><h2>` → proper `<h2>` after closing `<p>`
- **Removed SVG fragments**: Deleted floating `<line>` elements and broken icon markup
- **Removed English labels**: Translated "Quick:" and "Islamic Section" to Arabic equivalents
- **Added comparison table** for rent vs buy decision factors
- **Fixed article-tools section**: Replaced empty `<div>` containers with proper tool cards containing at-name and at-desc elements

### 4. Article-End Sections — CTA & Read-Also
**الملفات المتأثرة:** All three Batch 3 AR articles

**السبب الجذري:** 
- CTA text was generic ("احسب استثمارك") instead of topic-specific
- Read-also links pointed to same article (AR and EN versions) instead of related content

**الإصلاح:**
- **CTA**: Topic-appropriate (rent: "قارن بين الإيجار والتمويل", ramadan: "احسب زكاتك", umrah: "خطط لميزانية العمرة")
- **Read-also**: Links to 2-3 different related articles instead of self-referencing
- **Tags**: Changed from English (`#realestate`, `#saudi`, `#islamic`, `#travel`) to Arabic (`#عقار`, `#السعودية`, `#عمرة`, `#سفر`)
- **Added `</article>` closing tag** where missing (umrah article)

---

## BOOM Checklist — Batch 3.5

| # | BOOM Point | Status |
|---|-----------|--------|
| 1 | File naming | ✅ |
| 2 | canonical/hreflang/og:url | ✅ |
| 3 | articles.json/sitemap.xml | ✅ |
| 4 | article-layout structure | ✅ (inline grid fallback added) |
| 5 | No bilingual spans | ✅ |
| 6 | Monolingual header/footer | ✅ |
| 7 | Fixed inline script | ✅ |
| 8 | Lang-toggle | ✅ |
| 9 | FAQ as faq-question/faq-answer | ✅ |
| 10 | HTTP 200 | ✅ |
| 11 | Suitable image | ✅ |
| 12 | **Sidebar populated** | ✅ (TOC + Related filled) |
| 13 | **Article-end sections** | ✅ (CTA + Read-also improved) |
| 14 | **Clean body HTML** | ✅ (no malformed tags, no English, no SVG fragments) |

---

## الدروس المستفادة (Lessons Learned)

1. **Inline styles as CSS fallback**: When CDN caching may serve stale CSS, add inline `style` attributes as fallbacks for critical layout properties (grid, flex).
2. **Sidebar modules must be populated**: Empty sidebar modules (TOC, Related) look broken. Always populate them or remove them entirely.
3. **Read-also should never link to itself**: Always check that read-also links point to different articles, not the same one in another language.
4. **Tags must match article language**: English tags (`#realestate`) on Arabic articles look unprofessional. Use Arabic tags (`#عقار`).
5. **Close all HTML tags**: Ensure `<article>`, `<div>`, and other container tags are properly closed. Browsers may auto-close, but this affects DOM structure.
6. **Section numbering must be sequential**: Articles with headings like "Section 1, Section 3, Section 2, Section 5" confuse readers. Always check section order.
