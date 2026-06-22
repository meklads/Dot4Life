# 🖼️ عمر — دفعة إنتاج الصور (Image Module)

> **من:** GSystem / Cursor · **إلى:** عمر (المدير البصري) · **التاريخ:** 2026-06-22  
> **الحالة:** 🟢 **مُفعَّل** — جوست كلم عمر · النظام جاهز للملء

## دورك (مالك الحارة)

| أنت | Cursor |
|-----|--------|
| اختيار الصورة + alt ع/إن + `visual_director: approved` | يقرأ الفهرس فقط — **لا يختار صوراً** |
| تضع WebP في `assets/images/approved/` | يحقن hero في HTML عند TECH_BUILD |
| تملأ `assets/images/image-manifest.json` | G5 fail-closed: لا معتمد = `BLOCKED_IMAGE` |

## المواصفات البصرية (D4L)

| بند | القيمة |
|-----|--------|
| الصيغة | **WebP** فقط |
| المقاس | **1200×750** (نسبة 16:10 تقريباً) |
| الوزن | ≤ 150 KB مفضّل |
| الأسلوب | still-life · احتشام · هوية D4L (#054241 · #6abfb8 · خلفية دافئة) |
| المحتوى | لا وجوه أطفال قريبة · لا رموز حساسة · لا stock عام مكرّر |
| Alt عربي | وصفي · **بدون شرطة طويلة (—)** |
| Alt إنجليزي | descriptive · **no em-dash** |

## خطوات العمل (لكل مقال)

1. صمّم/اختر الصورة → احفظ: `assets/images/approved/hero-<article_slug>.webp`
2. أضف صفاً في `image-manifest.json` → `entries`:

```json
{
  "article_slug": "investment-basics-beginners",
  "image": "assets/images/approved/hero-investment-basics-beginners.webp",
  "alt_ar": "رسم توضيحي لادخار واستثمار لأسرة خليجية",
  "alt_en": "Illustration of saving and investing for Gulf families",
  "visual_director": "approved",
  "by": "عمر",
  "date": "2026-06-22"
}
```

3. `article_slug` = اسم الملف **بدون** `-en` أو `-ar` (زوج ع/إن = slug واحد).
4. `visual_director`: `approved` | `rejected` | `pending` — فقط **approved** يُبنى.
5. بعد الدفعة: أخبر عامر → BUILD VERIFY → Cursor يعيد TECH_BUILD للمقالات المعنية.

## أولوية الدفعة الأولى

**ابدأ بالـ16 LIVE** (Track A) — ثم blog triage PASS.

> القائمة التالية تُحدَّث تلقائياً: `python3 scripts/list-image-pending.py --md`

---

# Image pending — Omar production queue

Manifest: `0` entries · approved dir: `assets/images/approved/`

## Track A LIVE (priority P0) (16 slugs)

| # | article_slug | manifest | suggested file |
|---|--------------|----------|----------------|
| 1 | `investment-basics-beginners` | missing | `hero-investment-basics-beginners.webp` |
| 2 | `family-budget-plan` | missing | `hero-family-budget-plan.webp` |
| 3 | `rent-vs-buy-gulf-family` | missing | `hero-rent-vs-buy-gulf-family.webp` |
| 4 | `daily-walking-benefits` | missing | `hero-daily-walking-benefits.webp` |
| 5 | `bmi-calculator-women` | missing | `hero-bmi-calculator-women.webp` |
| 6 | `children-sleep-summer` | missing | `hero-children-sleep-summer.webp` |
| 7 | `pregnancy-week-by-week` | missing | `hero-pregnancy-week-by-week.webp` |
| 8 | `preconception-checkups` | missing | `hero-preconception-checkups.webp` |
| 9 | `daily-adhkar-family-guide` | missing | `hero-daily-adhkar-family-guide.webp` |
| 10 | `umrah-with-kids` | missing | `hero-umrah-with-kids.webp` |
| 11 | `hijri-new-year-children` | missing | `hero-hijri-new-year-children.webp` |
| 12 | `teaching-children-allah-names` | missing | `hero-teaching-children-allah-names.webp` |
| 13 | `teaching-children-prayer-with-love` | missing | `hero-teaching-children-prayer-with-love.webp` |
| 14 | `jeddah-mortgage-calculator` | missing | `hero-jeddah-mortgage-calculator.webp` |
| 15 | `riyadh-rental-yield` | missing | `hero-riyadh-rental-yield.webp` |
| 16 | `oman-property-roi` | missing | `hero-oman-property-roi.webp` |

## Blog triage PASS (43 files → 33 unique slugs)

| # | article_slug | manifest | suggested file |
|---|--------------|----------|----------------|
| 1 | `bmi-guide-arabs-gcc` | missing | `hero-bmi-guide-arabs-gcc.webp` |
| 2 | `bmi-middle-eastern-adults` | missing | `hero-bmi-middle-eastern-adults.webp` |
| 3 | `building-personal-savings-system` | missing | `hero-building-personal-savings-system.webp` |
| 4 | `children-education-savings-guide` | missing | `hero-children-education-savings-guide.webp` |
| 5 | `choosing-right-school-child-gulf` | missing | `hero-choosing-right-school-child-gulf.webp` |
| 6 | `daily-islamic-habits-guide` | missing | `hero-daily-islamic-habits-guide.webp` |
| 7 | `digital-minimalism-families` | missing | `hero-digital-minimalism-families.webp` |
| 8 | `end-of-service-benefits-expats` | missing | `hero-end-of-service-benefits-expats.webp` |
| 9 | `family-budget-planning-guide` | missing | `hero-family-budget-planning-guide.webp` |
| 10 | `family-friendly-activities-gulf-cities` | missing | `hero-family-friendly-activities-gulf-cities.webp` |
| 11 | `family-nutrition-on-budget` | missing | `hero-family-nutrition-on-budget.webp` |
| 12 | `family-travel-planning-without-overspending` | missing | `hero-family-travel-planning-without-overspending.webp` |
| 13 | `indoor-plants-saudi-arabia` | missing | `hero-indoor-plants-saudi-arabia.webp` |
| 14 | `life-insurance-gulf-families` | missing | `hero-life-insurance-gulf-families.webp` |
| 15 | `managing-healthcare-costs-families` | missing | `hero-managing-healthcare-costs-families.webp` |
| 16 | `managing-screen-time-children` | missing | `hero-managing-screen-time-children.webp` |
| 17 | `medina-hotels-near-masjid-nabawi` | missing | `hero-medina-hotels-near-masjid-nabawi.webp` |
| 18 | `organize-life-daily-systems` | missing | `hero-organize-life-daily-systems.webp` |
| 19 | `pregnancy-weeks-guide` | missing | `hero-pregnancy-weeks-guide.webp` |
| 20 | `preparing-for-pregnancy-guide` | missing | `hero-preparing-for-pregnancy-guide.webp` |
| 21 | `ramadan-nutrition-guide` | missing | `hero-ramadan-nutrition-guide.webp` |
| 22 | `ramadan-preparation-guide-families` | missing | `hero-ramadan-preparation-guide-families.webp` |
| 23 | `rent-vs-buy-saudi-guide-2026` | missing | `hero-rent-vs-buy-saudi-guide-2026.webp` |
| 24 | `saudi-mortgage-guide` | missing | `hero-saudi-mortgage-guide.webp` |
| 25 | `saudi-real-estate-investing` | missing | `hero-saudi-real-estate-investing.webp` |
| 26 | `saving-vs-investing-gulf-family` | missing | `hero-saving-vs-investing-gulf-family.webp` |
| 27 | `starting-side-business-saudi-uae` | missing | `hero-starting-side-business-saudi-uae.webp` |
| 28 | `stress-management-working-parents` | missing | `hero-stress-management-working-parents.webp` |
| 29 | `teaching-children-financial-literacy` | missing | `hero-teaching-children-financial-literacy.webp` |
| 30 | `umrah-visa-gulf-residents-guide` | missing | `hero-umrah-visa-gulf-residents-guide.webp` |
| 31 | `water-intake-hot-climates-guide` | missing | `hero-water-intake-hot-climates-guide.webp` |
| 32 | `zakat-calculator-modern-investments-guide` | missing | `hero-zakat-calculator-modern-investments-guide.webp` |
| 33 | `zakat-complete-guide` | missing | `hero-zakat-complete-guide.webp` |

**المجموع:** 49 slug · **49 بانتظار الاعتماد**

---

*مرجع تقني:* `operating-system/reports/ghost/2026-06-22-image-module.md` · `scripts/image_manifest.py`
