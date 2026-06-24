# 🛡️ عامر — إطلاق Batch 03 · 2026-06-24 13:35

> **من:** جوست (2026-06-24) — «ابدأ العمل وشغّل الفريق وتوليد الصور»
> **القانون:** `gsystem-charter.md` · `VISUAL-DIRECTION.md` · `batch-03-prompts.md`

## المطلوب الآن — توليد 7 صور (Higgsfield)

| # | تذكرة | slug | الملف | القسم |
|---|--------|------|-------|-------|
| 1 | `B3-01A` | `gulf-father-money-lessons` | `hero-gulf-father-money-lessons.webp` | قصص مميزة |
| 2 | `B3-02A` | `government-vs-private-school-gulf` | `hero-government-vs-private-school-gulf.webp` | مقارنات وقرارات |
| 3 | `B3-03A` | `digital-minimalism-families` | `hero-digital-minimalism-families.webp` | الصحة والعافية |
| 4 | `B3-04A` | `pregnancy-nutrition-first-trimester` | `hero-pregnancy-nutrition-first-trimester.webp` | الحمل والولادة |
| 5 | `B3-05A` | `daily-islamic-habits-guide` | `hero-daily-islamic-habits-guide.webp` | الحياة الإسلامية |
| 6 | `B3-06A` | `umrah-with-kids` | `hero-umrah-with-kids.webp` | السياحة الدينية (مكة والمدينة) |
| 7 | `B3-07A` | `rent-vs-buy-gulf-family` | `hero-rent-vs-buy-gulf-family.webp` | العقار |

## خطوات كل صورة

1. انسخ **Prompt (EN)** من `operating-system/reports/batch-03-prompts.md`
2. Higgsfield → WebP **1200×750** → `assets/images/approved/hero-<slug>.webp`
3. حدّث `assets/images/image-manifest.json` → `visual_director: approved`
4. انقل تذكرة `B3-XXA` إلى **انتهى من عندي** على اللوحة
5. Cursor Autopilot يبني HTML تلقائياً عند `approved` + ملف

## أولوية التوليد (مقترحة)

1. `gulf-father-money-lessons` (B3-01A)
2. `government-vs-private-school-gulf` (B3-02A)
3. `digital-minimalism-families` (B3-03A)
4. `pregnancy-nutrition-first-trimester` (B3-04A)
5. `daily-islamic-habits-guide` (B3-05A)
6. `umrah-with-kids` (B3-06A)
7. `rent-vs-buy-gulf-family` (B3-07A)

## الفريق بالتوازي

| العضو | المسار |
|-------|--------|
| **Hema · تحليل** | AN-00 → B3-XXQ (SEO Briefs) |
| **Hema · نمو** | GR-00 → B3-XXL (بعد Q) |
| **Hema · كتابة** | B3-XXN بعد Q |
| **عامر** | B3-01A…07A — توليد + اعتماد manifest |
| **Cursor** | بناء عند approved — لا انتظار «ابنِ» |

## BUILD VERIFY (بعد كل بناء)

- hero WebP + alt ع/إن + og:image
- `python3 scripts/build-from-approved-draft.py --audit` للصفحة
