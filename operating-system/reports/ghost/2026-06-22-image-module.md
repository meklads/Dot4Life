# 👑 Ghost Report — Image Module (P0)

**من:** Cursor (Build Commander)  
**إلى:** Ghost / عامر / عمر  
**التاريخ:** 2026-06-22  
**القرار:** manifest-driven · fail-closed (قرار جوست)

---

## الحكم

**✅ جاهز** — مستهلك الفهرس + G5 مُصلَّب · ETA البناء: **مُنجَز (جلسة 2026-06-22)**

---

## ما بُني

| مكوّن | المسار | الوظيفة |
|--------|--------|---------|
| مجلد معتمد | `assets/images/approved/` | يضع فيه عمر فقط بعد إجازة المدير البصري |
| الفهرس | `assets/images/image-manifest.json` | `entries[]` فارغ — عمر يملؤه |
| قارئ/مستهلك | `scripts/image_manifest.py` | lookup · hero_block · assert_g5_image |
| TECH_BUILD | `scripts/build-from-approved-draft.py` | `strict_image=True` على الكتابة · legacy على `--audit` |
| Blog triage | `scripts/execute-blog-triage.py` | manifest أولاً · لا تحميل og:image · legacy grandfather |

### G5 (fail-closed)

- **TECH_BUILD** (`write_page`): `visual_director == "approved"` + ملف موجود + hero/alt/og يطابقان الفهرس → وإلا `BLOCKED_IMAGE`.
- **`--audit` LIVE (29 صفحة):** `strict_image=False` — placeholders الحالية (`hero-*.webp`) تمر حتى يعتمد عمر في الفهرس.
- **Blog archive gates:** نفس grandfather للأرشيف المبني سابقاً.

### تحقق

```
python3 scripts/build-from-approved-draft.py --audit
→ 29 pages PASS, 0 FAIL

TECH_BUILD بدون فهرس:
→ G5 BLOCKED_IMAGE: manifest missing for slug=investment-basics-beginners
```

---

## تقسيم الحارات (مُطبَّق)

| العمل | المالك |
|--------|--------|
| اختيار الصورة + alt + `visual_director` + ملء `image-manifest.json` | **عمر** |
| قراءة الفهرس · G5 · حقن hero في HTML | **Cursor** |
| BUILD VERIFY (صفحة مكتملة = صورة معتمدة) | **عامر** |
| النص | **Hema** |

---

## تعليمات عمر (دفعة الإنتاج)

1. ضع WebP في `assets/images/approved/` (مثال: `hero-investment-basics-beginners.webp`).
2. أضف صفاً في `image-manifest.json` → `entries`:

```json
{
  "article_slug": "investment-basics-beginners",
  "image": "assets/images/approved/hero-investment-basics-beginners.webp",
  "alt_ar": "نص بديل عربي وصفي بلا شرطة طويلة",
  "alt_en": "descriptive English alt, no em-dash",
  "visual_director": "approved",
  "by": "عمر",
  "date": "2026-06-22"
}
```

3. `article_slug` = اسم الملف بدون `-en`/`-ar` (مثال: `blog/foo-en.html` → `foo`).
4. لا em-dash في alt (G1/G5).
5. بعد أول دفعة معتمدة: Cursor يعيد TECH_BUILD للمقالات المعنية فقط.

### أولوية الانتظار (صور placeholder حالية)

**Track A LIVE (16 مقال × لغتين — slug واحد لكل زوج):**

`investment-basics-beginners` · `family-budget-plan` · `rent-vs-buy-gulf-family` · `daily-walking-benefits` · `bmi-calculator-women` · `children-sleep-summer` · `pregnancy-week-by-week` · `preconception-checkups` · `daily-adhkar-family-guide` · `umrah-with-kids` · `hijri-new-year-children` · `teaching-children-allah-names` · `teaching-children-prayer-with-love` · `jeddah-mortgage-calculator` · `riyadh-rental-yield` · `oman-property-roi`

**Blog Schema-only (~43 PASS):** كل slug تحت `blog/` بلا لاحقة لغة — راجع `operating-system/reports/blog-triage-execute-log.md`.

---

## عامر — BUILD VERIFY

عند `visual_director: approved` في الفهرس:

1. الملف موجود تحت `approved/`.
2. HTML فيه `<figure class="hero">` بنفس `src` والـ alt من الفهرس.
3. `og:image` يطابق.
4. `--audit` يبقى PASS للـ LIVE حتى الترحيل التدريجي.

---

## ملاحظة تشغيلية

- **لا استبدال تلقائي** للـ ~40–62 placeholder — فقط عند إدخال عمر في الفهرس.
- **إعادة بناء TECH_BUILD** لأي مقال بدون فهرس معتمد = **BLOCKED** (مقصود).

---

*Cursor · Image Module v1 · 2026-06-22*
