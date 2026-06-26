# DEEPEN — طابور الإصلاح المؤجّل

> **المالك:** Hema (بعد عتبة 50) · **المراجع:** Cursor acting QA · **محدّث:** 2026-06-26

## 🔒 الخطة المعتمدة (جوست · 2026-06-26) — لا تنفيذ غيرها

ثلاث مراحل بالترتيب، لا قفز للأمام:

1. **إصلاح القصور الحالي أولاً** — معالجة كل صفحة تخالف معايير الجودة (محتوى مختلط · متن ضحل <1600 AR · FAQ حشو · سكيمة ناقصة · em-dash · Unsplash). **لا محتوى جديد حتى يصفر هذا الطابور.**
2. **رفع جودة الموجود** — بعد الإصلاح، نرفع جودة النقاط ضعيفة التقييم (FAQ 6/10 → تحسين، تعميق قيمة، روابط داخلية).
3. **ثم الجديد على نظافة** — لا يُفتح أي محتوى جديد إلا بعد اكتمال 1+2 وأمر صريح من جوست.

**فحص الموقع الشامل (2026-06-26):** 108 صفحة عربية. **49 صفحة تحتاج إصلاح** = 41 ضحلة (3 شديدة <1200 · 3 متوسطة 1200-1499 · 35 على الحد 1500-1599) + 8 بلا Article schema + 7 بلا FAQPage + 5 em-dash + 5 Unsplash (بتداخل). **0 محتوى مختلط** (اكتمل تعريبها).


## D19-FIX — إغلاق بوابة الإصلاح · 2026-06-26 18:30

**✅ 7/7 LIVE** (آخر مخالفات بعد D18):
`bmi-calculator-women` (صور related خاطئة) · `managing-screen-time-children` (خاتمة إنجليزية) · `preconception-checkups` · `life-insurance-gulf-families` · `choosing-right-school-child-gulf` · `expat-vs-national-finance` · `pregnancy-nutrition-first-trimester`.

**فحص الموقع بعد D19:** 83 صفحة حية في `articles.json` → **0 مخالفة بوابة إصلاح.**

**→ المرحلة 2:** `operating-system/reports/quality-phase-2-plan.md`

## Q-01 — FAQ 8+/10 · مفعّلة 2026-06-26 19:00

**الأسبوع 1 · 15 صفحة · هيما:** إعادة FAQ بأرقام/خطوات/أمثلة خليجية.
التقرير: `operating-system/reports/quality-batch-q01.md` · تذاكر `Q-01-01N`→`15N`.

| # | الملف |
|---:|------|
| 01 | `islamic-hajj-umrah/umrah-with-kids.html` |
| 02 | `islamic-hajj-umrah/hijri-new-year-children.html` |
| 03 | `islamic-hajj-umrah/daily-adhkar-family-guide.html` |
| 04 | `featured-stories/featured-story-gulf-family-home.html` |
| 05 | `blog/family-friendly-activities-gulf-cities.html` |
| 06 | `blog/daily-islamic-habits-guide.html` |
| 07 | `islamic-hajj-umrah/teaching-children-allah-names.html` |
| 08 | `blog/hydration-guide.html` |
| 09 | `peace-capsules/beat-summer-boredom-without-screens.html` |
| 10 | `finance-wealth/investment-basics-beginners.html` |
| 11 | `featured-stories/saudi-father-carpentry-workshop.html` |
| 12 | `featured-stories/featured-story-saudi-mother.html` |
| 13 | `comparisons/gold-vs-real-estate-gulf-family.html` |
| 14 | `comparisons/domestic-vs-international-travel-family.html` |
| 15 | `blog/umrah-with-kids-guide.html` |

**الأسبوع 2 (مُجدول):** D-01 تعميق قيمة — لا يُطلَق قبل إغلاق Q-01.

## Q-01 — رفع جودة FAQ · بدأ 2026-06-26 18:20

**الهدف:** 15 صفحة LIVE، تحسين FAQ من مقبول تقنياً إلى 8+/10.

**القائمة:** `teaching-children-allah-names` · `umrah-with-kids` · `zakat-investment-portfolios` · `gold-vs-real-estate-gulf-family` · `bmi-calculator-women` · `salalah-oman` · `hydration-guide` · `featured-story-gulf-family-home` · `family-friendly-activities-gulf-cities` · `daily-walking-benefits` · `featured-story-saudi-mother` · `saudi-father-carpentry-workshop` · `ramadan-preparation-guide-families` · `pregnancy-week-by-week` · `family-nutrition-on-budget`.

**التقرير:** `operating-system/reports/quality-q01-faq.md`.

## D18-Hema — مكتمل 20/20 LIVE · 2026-06-26 18:10

**الموجة الأولى (7):** `makkah-hotels-guide` · `salalah-khareef` · `family-nutrition-on-budget` · `mindful-living-gulf-heat` · `building-personal-savings-system` · `comparisons-ready-vs-build-home` · `comparisons-public-vs-private-education`.

**الموجة الثانية (13 RETURN → LIVE):** بعد إصلاح هيما + 3 لمسات Cursor قبل النشر:
`body-fat-vs-weight-guide` (+ stub `-ar`) · `salalah-travel-guide-2025` · `hajj-umrah-guide-2025` · `featured-story-arab-father-teens` · `peace-at-home-5-steps` · `summer-camps-vs-home` · `best-family-destinations-gulf` · `organize-life-daily-systems` · `teaching-children-financial-literacy` · `children-sleep-summer` · `calm-corner-small-space` · `teaching-children-prayer-with-love` · `family-time-management`.

**D18 الكامل:** 20 هيما + 6 Cursor تقنية = **26/26 LIVE.**

## D18-Hema QA — 7 LIVE + 13 RETURN · 2026-06-26 17:45 (مُغلق)

**✅ نُشرت LIVE بعد PASS كامل:**
`makkah-hotels-guide` · `salalah-khareef` · `family-nutrition-on-budget` · `mindful-living-gulf-heat` · `building-personal-savings-system` · `comparisons-ready-vs-build-home` · `comparisons-public-vs-private-education`.

**↩️ RETURN إلى هيما (13):**

| الصفحة | سبب الرفض |
|--------|-----------|
| `blog/body-fat-vs-weight-guide-ar.html` | 3 فقرات English داخل الصفحة العربية |
| `blog/salalah-travel-guide-2025.html` | FAQ/content filler: «بشكل عام» داخل سلسلة مترادفات طويلة |
| `blog/hajj-umrah-guide-2025.html` | FAQ/content filler: «بشكل عام» + «متوازن ومعتدل» وسلاسل مترادفات |
| `featured-stories/featured-story-arab-father-teens.html` | FAQPage ناقصة وFAQ=0 في السكيما |
| `peace-capsules/peace-at-home-5-steps.html` | FAQPage ناقصة وFAQ=0 في السكيما |
| `peace-capsules/summer-camps-vs-home.html` | FAQPage ناقصة + URL إنجليزي التقطه فحص mixed |
| `travel/best-family-destinations-gulf.html` | FAQPage ناقصة وFAQ=0 في السكيما |
| `blog/organize-life-daily-systems.html` | FAQ=3 فقط + FAQ/content filler |
| `blog/teaching-children-financial-literacy.html` | FAQ=3 فقط + FAQ/content filler |
| `health/children-sleep-summer.html` | FAQPage ناقصة + FAQ/content filler |
| `peace-capsules/calm-corner-small-space.html` | FAQPage ناقصة + FAQ/content filler + Article description حشو |
| `islamic-hajj-umrah/teaching-children-prayer-with-love.html` | FAQPage ناقصة + FAQ/content filler |
| `productivity/family-time-management.html` | FAQ/content filler: «متوازن ومعتدل» وسلاسل مترادفات |

## D17 RETURN — أصلحها Cursor (استثناء) ونُشرت LIVE · 2026-06-26 15:05

بأمر جوست، أصلح Cursor الثلاثة استثناءً (هيما مشغول بـ20 صفحة D18):

| الصفحة | الإصلاح | النتيجة |
|--------|---------|---------|
| `guides/saudi-tourism` | تعريب 30 بطاقة/فقرة + حذف المكرر + `lang=ar dir=rtl` | ✅ LIVE — AR≈2279 · 0 مختلط |
| `guides/mecca-medina` | تعريب 34 بطاقة/فقرة + حذف المكرر + `lang=ar dir=rtl` | ✅ LIVE — AR≈2548 · 0 مختلط |
| `blog/choosing-right-school-child-gulf` | هيرو مخصّص مولّد + alt + تسجيل مانيفست (FAQ/سكيمة/الطول كانت سليمة) | ✅ LIVE — AR≈1797 |

**طابور RETURN الآن: صفر.** هيما يكمل صفحات D18 العشرين فقط.

## D18 Cursor Tech — مُنجز · 2026-06-26 13:57

**✅ الستة التقنية على Cursor صارت PASS ونُشرت:**
`hydration-guide` · `zakat-guide-2025` · `gcc-family-budget-2025` · `featured-story-gulf-family-home` · `arab-mother-startup` · `evening-rituals`.

**ملاحظة:** الثلاثة RETURN المذكورة سابقاً أُغلقت لاحقاً بواسطة Cursor استثناءً في سجل 15:05.

## D18-FIX — تقسيم مسؤوليات · 2026-06-26 13:50

**بعد 3 RETURN الحالية:**

- **هيما:** 20 صفحة كتابة/جودة (mixed language · نقص كلمات · FAQ filler · تعميق عملي).
- **Cursor:** 6 إصلاحات تقنية فقط (schema · Unsplash/hero · em-dash).

الستة على Cursor: `hydration-guide` · `zakat-guide-2025` · `gcc-family-budget-2025` · `featured-story-gulf-family-home` · `arab-mother-startup` · `evening-rituals`.

التقرير الحاكم: `operating-system/reports/deepen-batch-18.md`.

## D17-FIX — مراجعة نهائية + إطلاق D18 · 2026-06-26 11:59

**النتيجة:** 27/30 LIVE بعد مراجعة Cursor. **3 RETURN باقية:**

| slug | حالة | ملاحظة |
|------|------|--------|
| `guides/saudi-tourism` | ↩️ RETURN | 6 فقرات/بطاقات bilingual تبدأ بالإنجليزية |
| `guides/mecca-medina` | ↩️ RETURN | 13 فقرة/بطاقة bilingual تبدأ بالإنجليزية |
| `blog/choosing-right-school-child-gulf` | ↩️ RETURN | FAQ حشو واحد يحتاج رقم/خطوة/مثال |

**المتبقي العام:** 29 مهمة إصلاح نشطة = 3 RETURN D17 + 26 صفحة D18-FIX.

**D18-FIX أُطلقت ثم وُسّعت بعد فحص FAQ filler:** `operating-system/reports/deepen-batch-18.md` — 20 صفحة موجودة فقط، لا محتوى جديد.

## D17-FIX — مراجعة الموجة الأولى (01→10) · 2026-06-26 06:52

**✅ 7 نُشرت LIVE** + **↩️ 3 RETURN لهيما** (محتوى مختلط ع/en في المتن — يجب تعريبه بالكامل):

| slug | حالة | ملاحظة |
|------|------|--------|
| `guides/saudi-tourism` | ↩️ RETURN | 7 فقرات/بطاقات إنجليزية + disclaimer إنجليزي |
| `blog/managing-screen-time-children` | ↩️ RETURN | 6 أقسام إنجليزية كاملة (WHO/AAP، أدوات الرقابة، القدوة، المقاومة، الخاتمة) |
| `guides/mecca-medina` | ↩️ RETURN | 14 بطاقة/فقرة إنجليزية + disclaimer إنجليزي |

> صُمّمت 4 هيرو مخصصة جديدة (end-of-service · umrah-budget · hotel-near-haram · walking-vs-running) بدل الصور المستعارة.

## D17-FIX — تفعيل 30 صفحة إصلاح · 2026-06-26 01:18

**الحالة:** 🆕 مفعّلة لهيما.

- النطاق: 30 صفحة موجودة فقط من أصل 49 صفحة متبقية تحتاج إصلاح.
- الاختيار: أسوأ 30 حسب فحص Cursor الحالي (الأقل كلمات أولاً + FAQ/سكيمة/Unsplash/em-dash عند وجودها).
- قانون الراحة: 5 دقائق بعد كل 5 صفحات، ثم يكمل هيما دون انتظار تكليف جديد.
- تقرير الدفعة: `operating-system/reports/deepen-batch-17.md`.
- دور Cursor: QA بالتوازي، ثم صور/سكيمة/بناء/نشر بعد PASS.

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
| مؤجَّل للإصلاح | 0 ✅ جُمع الإصلاح (جميع D16-01→35 + احتياطي + RETURN-FAQ 6/6) |
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
| 7 | D16-FAQ | body-fat-vs-weight-guide-ar | ✅ 1836 AR w, 4 FAQ محددة بأرقام (نسبة دهون 10-20% للرجال، WHtR <0.5). | ✅ مُصلَح |
| 8 | D16-FAQ | end-of-service-saudi | ✅ 1862 AR w, 4 FAQ بقانون العمل (المادة 84-87، حاسبة منصة قوى). | ✅ مُصلَح |
| 9 | D16-FAQ | saving-for-education-gulf | ✅ 1807 AR w, 4 FAQ بأرقام الادخار (10-15% دخل، قاعدة 72، 240K بعد 18 سنة). | ✅ مُصلَح |
| 10 | D16-FAQ | family-time-management | ✅ FAQ محدثة بأرقام (ساعتين شاشة، 20 دقيقة اجتماع، 30 دقيقة تفاعل) + سكيما مطابقة. | ✅ مُصلَح |
| 11 | D16-FAQ | oman-property-roi | ✅ 1614→1685 AR w, Article+FAQPage schema، FAQ 6 أسئلة بأرقام عوائد إيجارية وأمثلة حسابية. | ✅ مُصلَح |
| 12 | D16-FAQ | rent-vs-buy-gulf-family | ✅ 1845 AR w, 4 FAQ بنسب Price-to-Rent (15-22) وأرقام تمويل. | ✅ مُصلَح |
| 13 | D16-FIT | calorie/ramadan/fitness-women | ✅ FAQPage schema محدثة لتطابق عدد الأسئلة المرئية (7/6/6). | ✅ مُصلَح |
| 14 | D16-RETURN-FAQ | digital-minimalism-families | ✅ 2781 AR w, 4 FAQ بأرقام وقت الشاشات (6.5h متوسط، 42% تخفيض، Family Link). | ✅ مُصلَح |
| 15 | D16-RETURN-FAQ | family-budget-planning | ✅ 1847 AR w, 4 FAQ بقاعدة 50/30/20، أرقام دخل وميزانية. | ✅ مُصلَح |
| 16 | D16-RETURN-FAQ | family-travel-without-overspending | ✅ 1754 AR w, 4 FAQ بنسب توزيع الميزانية (30-40% تذاكر، 25-35% إقامة). | ✅ مُصلَح |
| 17 | D16-RETURN-FAQ | masjid-nabawi-guide | ✅ 2164 AR w, 4 FAQ بأرقام التوسعات (1,050m²→384,000m²، 1.6M مصلٍ). | ✅ مُصلَح |
| 18 | D16-RETURN-FAQ | umrah-visa-gulf-residents | ✅ 2122 AR w, 4 FAQ بتكاليف التأشيرة (250-1,500 ريال)، 5 خطوات تطبيق. | ✅ مُصلَح |
| 19 | D16-RETURN-FAQ | oman-property-roi | ✅ 1685 AR w, 6 FAQ بأرقام عوائد (5.5-7.5%) وأمثلة حسابية. | ✅ مُصلَح |

## نشر D16 — الموجة الأولى · 2026-06-25 17:45

**✅ نُشر LIVE — 17 صفحة نظيفة** (عمق ≥الحد · FAQ≥4 في السكيما · Article+FAQPage · 0 em-dash · 0 Unsplash · og:image معتمد):
ashura-family-traditions-gulf · daily-islamic-habits-guide · family-nutrition-on-budget · gcc-family-budget-2025 · hydration-guide · medina-hotels-near-masjid-nabawi · peaceful-road-trip-kids-guide · pregnancy-and-umrah-guide · pregnancy-nutrition-first-trimester · umrah-with-kids-guide · gold-vs-real-estate-gulf-family · government-vs-private-school-gulf · saving-vs-investing-gulf-family · investment-basics-beginners · family-time-management-en · jeddah-mortgage-calculator · riyadh-rental-yield.

## نشر D16 — الموجة الرابعة · 2026-06-25 22:15

**✅ D16-RETURN-FAQ منجز 6/6 — جاهز لإعادة فحص Cursor وإغلاق D16.**
جميع ملفات RETURN الـ 6: FAQ بأرقام وخطوات وأمثلة واقعية (0 حشو) · FAQPage سكيما مطابقة · Article+FAQPage · ≥1600 AR · 0 em-dash · 0 Unsplash.

**✅ جميع الإصلاحات منجزة.**

## ملاحظات جودة دائمة (Cursor يعالجها آلياً قبل النشر)

| # | العيب | المعالجة | الحالة |
|---|-------|----------|--------|
| Q1 | **سايدبار TOC عربي في النسخة الإنجليزية** (نص عربي + روابط `#عربية` لا تطابق عناوين H2 الإنجليزية) — موروث في التعميق المباشر. | `python3 scripts/fix_en_toc.py` يعيد بناء TOC إنجليزي ويضيف `id` إنجليزي لكل H2. عولج 49 ملفاً (14 blog + 35 عبر الموقع). | ✅ مُعالَج · فحص دائم قبل كل نشر |

> **تنبيه لهيما:** عند تعميق النسخة الإنجليزية، احرص أن سايدبار «Contents» إنجليزي وروابطه تطابق عناوين H2 الإنجليزية — لا تنسخ سايدبار العربية.

---

*Cursor يحدّث هذا الملف عند كل RETURN أو عند بلوغ العتبة 50.*
