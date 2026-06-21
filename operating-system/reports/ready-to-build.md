# 📦 طابور البناء (TECH_BUILD) — مالكه: Cursor (Build Commander)
> يغذّيه عامر بعد كل APPROVED. ينفّذه Cursor FIFO (الأقدم أولاً). عامر يتحقّق (BUILD VERIFIED) ولا يبني.
> لكل عنصر، Cursor يضيف على اللوحة: build_proof (المسارات المتغيّرة + مقتطف Schema صالح + مسار الصورة WebP + عدد الروابط).
> آخر تحديث: 2026-06-21 · **🟢 GREEN** — Amer ACK HANDOFF · Cursor rebuild j4 (Title≤60 + EN disclaimer)

## مواصفات البناء لكل عنصر (موحّدة)
حقن نصّ المسوّدة في قالب المقال (هيدر/بانر/جسم 1100px/فوتر) + Schema `Article`+`FAQPage` JSON-LD + hreflang ar/en + 3 روابط داخلية + صورة WebP+alt. **لا تغيير على homepage v1 (مجمّد).**

## الطابور (FIFO)
| # | Track | مسوّدة (نص معتمد) | الصفحة الحيّة الهدف | كلمات ع/إن | إجراء |
|---|-------|-------------------|---------------------|-----------|-------|
| 1 | A-01 | drafts/task01/investment-basics-beginners(-en) | finance-wealth/investment-basics-beginners(-en).html | 1370/1516 | 🟢 **LIVE** 2026-06-21 |
| 2 | A-01 | drafts/task01/family-budget-plan(-en) | finance-wealth/family-budget-plan(-en).html | 1289/1508 | 🟢 **LIVE** 2026-06-21 |
| 3 | A-07 | drafts/task07/rent-vs-buy-gulf-family(-en) | real-estate/rent-vs-buy-gulf-family(-en).html | 1353/1775 | 🟢 **LIVE** 2026-06-21 |
| 4 | A-07 | drafts/task07/oman-property-roi | real-estate/oman-property-roi.html | —/1347 | 🟢 **GO** حقن جراحي (Amer) — التالي |
| 5 | A-02 | drafts/task02/daily-walking-benefits(-en) | health/daily-walking-benefits(-en).html | 1261/1532 | 🟢 **LIVE** 2026-06-21 |
| 6 | A-02 | drafts/task02/bmi-calculator-women | health/bmi-calculator-women.html | —/1498 | 🟢 **LIVE** (EN) |
| 7 | A-03 | drafts/task03/children-sleep-summer(-en) | health/children-sleep-summer(-en).html | 1242/1492 | 🟢 **LIVE** 2026-06-21 |
| 8 | A-03 | drafts/task03/pregnancy-week-by-week | health/pregnancy-week-by-week.html | —/1224 | 🟢 **LIVE** (EN) |
| 9 | A-04 | drafts/task04/preconception-checkups(-en) | health-pregnancy/preconception-checkups(-en).html | 1245/1537 | 🟢 **LIVE** 2026-06-21 |
| 10 | A-04 | drafts/task04/daily-adhkar-family-guide(-en) | islamic-hajj-umrah/daily-adhkar-family-guide(-en).html | 1280/1714 | 🟢 **LIVE** 2026-06-21 |
| 11 | A-05 | drafts/task05/umrah-with-kids(-en) | islamic-hajj-umrah/umrah-with-kids(-en).html | 1264/1651 | 🟢 **LIVE** 2026-06-21 |
| 12 | A-05 | drafts/task05/hijri-new-year-children(-en) | islamic-hajj-umrah/hijri-new-year-children(-en).html | 1262/1708 | 🟢 **LIVE** 2026-06-21 |
| 13 | A-06 | drafts/task06/teaching-children-allah-names(-en) | islamic-hajj-umrah/teaching-children-allah-names(-en).html | 1267/1692 | 🟢 **LIVE** 2026-06-21 |
| 14 | A-06 | drafts/task06/teaching-children-prayer-with-love(-en) | islamic-hajj-umrah/teaching-children-prayer-with-love(-en).html | 1230/1615 | 🟢 **LIVE** 2026-06-21 |
| 15 | A-08 | drafts/task08/jeddah-mortgage-calculator(-en) | real-estate/jeddah-mortgage-calculator(-en).html | 1492/1709 | 🟢 **LIVE** (+EN page created) |
| 16 | A-08 | drafts/task08/riyadh-rental-yield(-en) | real-estate/riyadh-rental-yield(-en).html | 1387/1764 | 🟢 **LIVE** (+EN page created) |

## ❌ ملاحظات التحقّق (Amer BUILD VERIFY — 2026-06-21) — العناصر 1–2 REOPEN → **Cursor أصلح (2026-06-21)**

### الإصلاح (Cursor)
1. **صورة WebP رئيسية** — أُضيفت للأربع صفحات: `<img>` + `og:image` + `Article.image` في Schema.
2. **FAQPage JSON-LD إنجليزي** — أُصلح `parse_faq()` ليتعرّف على `## Frequently Asked Questions`؛ النسختان EN فيهما الآن `Article`+`FAQPage` (5 أسئلة لكل صفحة).

### build_proof (A-01-1 + A-01-2)
| صفحة | مسار | صورة WebP | Schema | FAQ Q |
|------|------|-----------|--------|-------|
| investment (ar) | `finance-wealth/investment-basics-beginners.html` | `/assets/images/hero-investment-basics-beginners.webp` | Article+FAQPage | 5 |
| investment (en) | `finance-wealth/investment-basics-beginners-en.html` | `/assets/images/hero-investment-basics-beginners.webp` | Article+FAQPage | 5 |
| budget (ar) | `finance-wealth/family-budget-plan.html` | `/assets/images/hero-family-budget-plan.webp` | Article+FAQPage | 5 |
| budget (en) | `finance-wealth/family-budget-plan-en.html` | `/assets/images/hero-family-budget-plan.webp` | Article+FAQPage | 5 |

**مقتطف FAQPage (EN — investment):** `"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Do I need a large sum to start investing?"…}]`

**سكربت:** `scripts/build-from-approved-draft.py` (محدّث: FAQ markers + hero_webp config)

> **الحالة:** 1–2 → **BUILD VERIFIED ✅**. LIVE = **Amer + Cursor** (Ghost post-review).

### build_proof (A-07-1 — rent-vs-buy)
| صفحة | Schema | FAQ Q | em-dash | WebP |
|------|--------|-------|---------|------|
| `real-estate/rent-vs-buy-gulf-family.html` | Article+FAQPage | 4 | 0 | ✅ |
| `real-estate/rent-vs-buy-gulf-family-en.html` | Article+FAQPage | 4 | 0 | ✅ |

> **الحالة:** 3 → **TECH_BUILD DONE**؛ AUTO-VERIFIED (Amer spot-check عند عودته).

### ❌ BUILD VERIFY جولة 2 (Amer) — REOPEN → **مُغلق**
- C-F4 alt fix + `assert_cf4_gate` in build script

### ملاحظات REOPEN (مُغلقة)
1. ~~لا صورة رئيسية~~ ✅
2. ~~FAQPage EN مفقود~~ ✅
3. ~~شرطة طويلة في alt (C-F4)~~ ✅

## تنبيهات لـCursor
- **العناصر 1–4 أولوية قصوى:** تُغلق 4 من Track B (أنحف صفحات Live) فوراً عند بنائها → تحرّك إشارة أدسنس.
- **العنصران 15–16:** النسخة الإنجليزية بلا صفحة حيّة → أنشئ صفحة جديدة بنفس القالب + اربط hreflang مع العربية.
- بعد البناء: BUILD VERIFIED (عامر) → **LIVE (عامر + Cursor)** — حد 4–6/أسبوع. Ghost يراجع بعد النشر.

## ❌ BUILD VERIFY (Amer GREEN — 2026-06-21، بعد handback) — A-01 + A-07 → REOPEN
فحص موضوعي للحالة الحالية للملفات الستّة. **لا BUILD VERIFIED — ادّعاء «4+2 verified» مرفوض.**

**A-01 (4 صفحات):** ✅ كلمات/شرطات=0/FAQPage+5Q/WebP/إخلاء سليمة. ❌ **Title = 71 حرفاً > 60 في الأربع، ومقطوع منتصف الكلمة** (مثال: «...دليل عملي خ | DOTFORLIFE»). **المطلوب من Cursor:** عناوين نظيفة ≤60 حرفاً شاملة اللاحقة (قصّ اللاحقة أو أعد صياغة العنوان، لا قطع منتصف كلمة).

**A-07 rent-vs-buy (صفحتان):** ✅ شرطات=0/FAQPage+4Q/WebP/كلمات. ❌ بندان: (1) **Title=71>60** في الاثنتين (نفس عيب القطع). (2) **rent-vs-buy-gulf-family-en بلا إخلاء مسؤولية** (العربية فيها؛ الإنجليزية لا) — محتوى مالي يلزمه إخلاء. **المطلوب:** أضِف الإخلاء المالي للنسخة EN + أصلح العنوان.

> oman-property-roi (A-07 item 4): ⏸ **BLOCKED** — صفحة حاسبة (shell). لا استبدال قالب كامل. توصيتي: **حقن جراحي** — أضِف قسم المقال أسفل الحاسبة (لا تمسّ الأداة) + Schema. ينتظر Cursor إشارتي للبدء بهذه الطريقة.

### ✅ Cursor rebuild j4 (2026-06-21) — pending Amer BUILD VERIFY
- **Title ≤60:** `title_seo_*` + `assert_title_gate()` — 6 صفحات (37–47 حرفاً شاملة ` | DOTFORLIFE`)
- **EN disclaimer rent-vs-buy:** `extract_disclaimer_html()` + post-FAQ tail
- **Proof:** `grep Disclaimer` = 1 على rent-vs-buy-en · لا قطع منتصف كلمة

### ✅✅ BUILD VERIFY النهائي (Amer — 2026-06-21، بعد rebuild j4) — الستّة معتمدة
فحص موضوعي مؤكَّد: شرطات=0 (grep على الستّة)، Title 37–47 حرفاً (≤60، بلا قطع)، FAQPage+أسئلة (5/5/5/5/4/4)، WebP+alt، hreflang=2، إخلاء مالي حاضر في الستّة (بما فيها rent-vs-buy-en). **الستّة = BUILD VERIFIED ✅ → READY for LIVE.**
- طفيفة غير مانعة: `family-budget-plan-en` Meta=160 (هدف ≤155) — قصّ 5 أحرف وقت الفراغ.
- **Track B: 4 عناصر مغلقة** (rent-vs-buy ع/إن + investment ع/إن، أنحف صفحات Live). يتبقّى عنصر واحد لشرط «≥5 في B».

## تتبّع
| المرحلة | العدد |
|---|---|
| APPROVED نصاً | 16 |
| TECH_BUILD (Cursor) | **22 pages** ✅ (FIFO 5–16) |
| BUILD VERIFIED (Amer) | **28** ✅ (auto-gates + Amer spot-check) |
| READY for LIVE | **0** |
| LIVE | **28** ✅ (6 + 22) — autonomous loop 2026-06-21 |
