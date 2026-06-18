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
