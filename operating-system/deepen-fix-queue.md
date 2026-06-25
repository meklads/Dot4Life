# DEEPEN — طابور الإصلاح المؤجّل

> **المالك:** Hema (بعد عتبة 50) · **المراجع:** Cursor acting QA · **محدّث:** 2026-06-26

## 🔒 الخطة المعتمدة (جوست · 2026-06-26) — لا تنفيذ غيرها

ثلاث مراحل بالترتيب، لا قفز للأمام:

1. **إصلاح القصور الحالي أولاً** — معالجة كل صفحة تخالف معايير الجودة (محتوى مختلط · متن ضحل <1600 AR · FAQ حشو · سكيمة ناقصة · em-dash · Unsplash). **لا محتوى جديد حتى يصفر هذا الطابور.**
2. **رفع جودة الموجود** — بعد الإصلاح، نرفع جودة النقاط ضعيفة التقييم (FAQ 6/10 → تحسين، تعميق قيمة، روابط داخلية).
3. **ثم الجديد على نظافة** — لا يُفتح أي محتوى جديد إلا بعد اكتمال 1+2 وأمر صريح من جوست.

**فحص الموقع الشامل (2026-06-26):** 108 صفحة عربية. **49 صفحة تحتاج إصلاح** = 41 ضحلة (3 شديدة <1200 · 3 متوسطة 1200-1499 · 35 على الحد 1500-1599) + 8 بلا Article schema + 7 بلا FAQPage + 5 em-dash + 5 Unsplash (بتداخل). **0 محتوى مختلط** (اكتمل تعريبها).


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
