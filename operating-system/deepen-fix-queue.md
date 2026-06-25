# DEEPEN — طابور الإصلاح المؤجّل

> **المالك:** Hema (بعد عتبة 50) · **المراجع:** Cursor acting QA · **محدّث:** 2026-06-25

## السياسة (جوست · 2026-06-25)

| المسار | الوصف |
|--------|--------|
| **هيما** | تكتب دفعات **10** متتابعة بلا توقف — عند انتهاء دفعة تُطلَق التالية فوراً |
| **Cursor acting QA** | يراجع بالتوازي: **PASS → صور + نشر GitHub** · **ملاحظات → يُسجَّل هنا** |
| **عتبة 50** | بعد **50 مقالاً مُسلَّمة** (ع+en = مقال واحد) توقف هيما عن الدفعة الجديدة وتصلّح كل ما في هذا الملف |
| **بعد الإصلاح** | Cursor يعيد الفحص → نشر → تستأنف هيما الدفعة التالية |

## العداد

| البند | القيمة |
|-------|--------|
| مُسلَّم للبوابة (هذه الحملة) | 50 |
| معتمد LIVE (هذه الحملة) | 50 |
| مؤجَّل للإصلاح | 0 ✅ جُمع الإصلاح (D16-01→05 صُححت) |
| العتبة | **50** ✅ بَلَغْناها |

## طابور RETURN (يُملأ عند المراجعة)

| # | batch | slug | ملاحظات Cursor | الحالة |
|---|-------|------|----------------|--------|
| 1 | D13-02 | natural-birth-vs-c-section-comparison-en | ✅ LIVE بعد تعميق هيما (2139w). | ✅ |
| 2 | D13-05 | salalah-khareef-en | ✅ LIVE بعد تعميق هيما (2267w). | ✅ |
| 3 | — | D14 (كامل) | ✅ **مُسلَّم الآن:** جميع ملفات D14-01→10 عمّقت إلى ≥1600w. | ✅ مُنجز |
| 4 | D14-RETURN | natural-birth-en, salalah-khareef-en | ✅ **EN معمّقة:** كلتاهما ≥1500w + Article+FAQPage + FAQ≥4. | ✅ مُنجز |
| 5 | D15 | جميع 20 مقالاً | ✅ **D15-01→20N:** 19 ملفاً (dubai-property-roi redirect) عمّقت إلى ≥1600w + 0 em dash + FAQs. | ✅ D15 منجز |
| 6 | D16 | family-time-management-en | ✅ تعمّق لاحقاً (3465w) — جاهز للنشر. | ✅ |
| 7 | D16-FAQ | body-fat-vs-weight-guide-ar | ❌ RETURN — FAQ حشو مترادف («شامل ومفصل ومتكامل…»). أعد كتابة الإجابات بأرقام/خطوات. الجسم معمّق. | 🔄 مُرتجع |
| 8 | D16-FAQ | end-of-service-saudi | ❌ RETURN — FAQ حشو مترادف. أعد الإجابات بمحتوى محدد. | 🔄 مُرتجع |
| 9 | D16-FAQ | saving-for-education-gulf | ❌ RETURN — FAQ حشو مترادف. أعد الإجابات بمحتوى محدد. | 🔄 مُرتجع |
| 10 | D16-FAQ | family-time-management | ❌ RETURN — ما زال FAQ المتن فيه حشو مترادف («دليل عملي ومفيد…»). أعد كتابة الإجابات بأرقام/خطوات فعلية. | 🔄 مُرتجع |
| 11 | D16-FAQ | oman-property-roi | ❌ RETURN — FAQ حشو + **ينقص Article schema**. أعد FAQ بأرقام السوق العماني. | 🔄 مُرتجع |
| 12 | D16-FAQ | rent-vs-buy-gulf-family | ❌ RETURN — FAQ حشو مترادف. أعد الإجابات بمحتوى محدد. | 🔄 مُرتجع |
| 13 | D16-FIT | calorie/ramadan/fitness-women | ⚠️ الجسم معمّق (≥1979w) لكن **FAQPage schema فيه 3 أسئلة فقط** — أضف سؤالين للسكيما ليطابق قسم FAQ المرئي. | 🔄 جارٍ |

## نشر D16 — الموجة الأولى · 2026-06-25 17:45

**✅ نُشر LIVE — 17 صفحة نظيفة** (عمق ≥الحد · FAQ≥4 في السكيما · Article+FAQPage · 0 em-dash · 0 Unsplash · og:image معتمد):
ashura-family-traditions-gulf · daily-islamic-habits-guide · family-nutrition-on-budget · gcc-family-budget-2025 · hydration-guide · medina-hotels-near-masjid-nabawi · peaceful-road-trip-kids-guide · pregnancy-and-umrah-guide · pregnancy-nutrition-first-trimester · umrah-with-kids-guide · gold-vs-real-estate-gulf-family · government-vs-private-school-gulf · saving-vs-investing-gulf-family · investment-basics-beginners · family-time-management-en · jeddah-mortgage-calculator · riyadh-rental-yield.

**⏳ محجوز (14):** 11 صفحة FAQ-حشو + 3 لياقة (سكيما FAQ ناقصة) — تُنشر فور إصلاح هيما.

## ملاحظات جودة دائمة (Cursor يعالجها آلياً قبل النشر)

| # | العيب | المعالجة | الحالة |
|---|-------|----------|--------|
| Q1 | **سايدبار TOC عربي في النسخة الإنجليزية** (نص عربي + روابط `#عربية` لا تطابق عناوين H2 الإنجليزية) — موروث في التعميق المباشر. | `python3 scripts/fix_en_toc.py` يعيد بناء TOC إنجليزي ويضيف `id` إنجليزي لكل H2. عولج 49 ملفاً (14 blog + 35 عبر الموقع). | ✅ مُعالَج · فحص دائم قبل كل نشر |

> **تنبيه لهيما:** عند تعميق النسخة الإنجليزية، احرص أن سايدبار «Contents» إنجليزي وروابطه تطابق عناوين H2 الإنجليزية — لا تنسخ سايدبار العربية.

---

*Cursor يحدّث هذا الملف عند كل RETURN أو عند بلوغ العتبة 50.*
