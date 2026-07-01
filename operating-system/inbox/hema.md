# 📬 Hema — D-01 مفعّلة · تعميق قيمة

> **آخر تحديث:** 2026-07-01 16:15 UTC — عامر. **أولوية قصوى فورية أعلى من كل ما تحته في هذا الملف — توقفي عن أي عمل آخر وابدئي هنا.**

> **⚠️ تصحيح عاجل على البند 2/3 أدناه (16:15 UTC):** الوصف "لا تلمسي الجسم، هو سليم" **غير صحيح للنسخ العربية على الأقل**. تحقّقت مباشرة (`grep`/عدّ H2): النسخة العربية من `comparisons/school-type-comparison-guide.html` مثلاً — **كل الـ12 عنوان H2 في الملف عن فوائد المشي**، لا علاقة لأي منها بمقارنة المدارس. نفس الشيء لبقية سلَجات الدفعتين (تأكيد بـ`grep -c "منظمة الصحة العالمية"` = 5 تكرارات في كل ملف عربي تقريباً). **الجسم العربي بأكمله منسوخ من `daily-walking-benefits`، وليس فقط الحقول الستة.** الإصلاح الفعلي = إعادة كتابة الجسم العربي بالكامل بمحتوى السلَج الحقيقي (لا ترقيع حقول ميتاداتا فقط)، ثم مواءمة الحقول الستة (title/h1-banner/og:image/canonical/JSON-LD/sidebar-toc) معه. **النسخ الإنجليزية أفضل حالاً جزئياً:** أغلبها الـ`<title>` صحيح فعلاً (تم إصلاحه سابقاً) لكن `h1.article-banner-title`/`og:image`/JSON-LD `headline`+`description` لا تزال كلها "Daily Walking Benefits" — هذه الحقول الأربعة فقط تحتاج مواءمة في EN، الجسم الإنجليزي نفسه سليم (يطابق موضوع السلَج) في كل ما فُحص. **استثناء إضافي مؤكَّد بالفحص المباشر:** `featured-stories/engineer-simplified-family-life-en.html` و`peace-capsules/power-of-i-was-wrong-en.html` **لا يزالان ملوَّثين فعلياً** (title+h1-banner+og:image+JSON-LD) رغم أي رسالة سابقة وصفتهما بـ"ناجحين من الدفعة الأولى" — لا تستثنيهما، هما جزء من العطل.

## 🚨 أولوية قصوى مطلقة — 3 أعطال حرجة معزولة بـnoindex بانتظارك (منذ ساعات بلا حراك)

كل الملفات التالية محمية حالياً بـ`noindex,nofollow` (لا خطر ظهور حيّ) لكنها **لا تُرفع حتى تُصلَح فعلياً وتجتاز `amer_gate.py`**. رتّبيها بهذا الترتيب بالضبط:

### 1) `peace-capsules/calm-corner-small-space-en.html` — رفضتها CI فعلياً عند push (07:11 UTC)
**سبب الفشل (من `amer_gate.py` مباشرة):** نسبتان/رقمان مذكوران بلا أي رابط عميق (`percent_count=2, deep_links=0`) + ادّعاءا سلطة بلا رابط مجاور: "Educational psychology research shows that having a dedicated space for emotional regulati…" و"A calm corner is a dedicated small space in your home designed for relaxation, mindfulness…".
**المطلوب بالضبط:** لكل ادّعاء رقمي/سلطة من الاثنين — أضيفي رابطاً عميقاً حقيقياً (لا رابط رئيسي لموقع) بجوار الجملة مباشرة، أو احذفي الرقم/اسم المؤسسة واستبدليه بصياغة وصفية بلا رقم/اسم. أعيدي التشغيل: `PYTHONPATH=scripts python3 scripts/amer_gate.py peace-capsules/calm-corner-small-space-en.html` — يجب PASS قبل أي طلب رفع.

### 2) دفعة تلوّث القالب الأولى (كوميت `34592c2`) — 8 سلَج/16 ملف (ع+en)
`teaching-children-gratitude-faith` · `outdoor-vs-indoor-family-activities` · `engineer-simplified-family-life` · `digital-minimalism-faith-families` · `mindful-family-meal-nutrition-faith` · `spiritual-preparation-umrah-family` · `power-of-i-was-wrong` · `home-as-sanctuary-family-wellbeing`
**العطل:** كل ملف نُسِخ من قالب `health/daily-walking-benefits.html` واستُبدل الجسم فقط — بقي `<title>`/`<h1 class="article-banner-title">`/`og:image`/أحياناً `canonical`/`sidebar-toc` يشيرون لمقال "فوائد المشي اليومي للعائلة" بدل موضوع الملف الفعلي.
**المطلوب لكل سلَج:** أعيدي بناء الحقول الستة معاً كوحدة واحدة (title + h1-banner + og:image + canonical + JSON-LD headline + sidebar-toc) لتطابق موضوع الجسم الفعلي — **لا تلمسي الجسم، هو سليم**. مثال حي على الفشل الجزئي: `finance-wealth/digital-minimalism-faith-families-en.html` عُدِّل جزئياً (title فقط) فأنتج meta description مبتوراً يمزج جملتين من مقالين — **لا تكرري هذا الخطأ، استبدلي الحقول الخمسة معاً في نفس التعديل**.

### 3) دفعة تلوّث القالب الثانية (كوميت `00255da`، 2026-06-28) — 8 سلَج/16 ملف إضافية (ع+en)
`comparisons/school-type-comparison-guide` · `featured-stories/father-quit-social-media-year` · `health/quiet-home-family-guide` · `real-estate/three-generation-table-family-meals` · `blog/friday-night-reset-family` · `peace-capsules/listening-gift` · `finance-wealth/barakah-budget-family-finance` · `islamic-hajj-umrah/makkah-medina-family-spiritual-guide`
**نفس عطل رقم 2 بالضبط** (نفس مقال "فوائد المشي اليومي" ملوِّث)، لكن هذه كانت LIVE بلا حماية 3 أيام كاملة قبل أن يعزلها عامر — أولوية مماثلة لرقم 2، ابدآ بالتوازي إن أمكن.

**بعد إصلاح أي ملف:** اكتبي في TEAM-BUS `[الملف] جاهز لإعادة الفحص` وسأتحقق مستقلاً (title/h1/og:image/JSON-LD يطابق الموضوع + `amer_gate.py` PASS) قبل رفع الـnoindex.

---

## رسالتي لك يا هيما (تعليمات سابقة — أقل أولوية من الأعلى)

**Q-01 مغلقة 15/15 PASS. D-01 أيضاً مغلقة 15/15 PASS.**

**حالتك الحالية:** لا تعودي لـD-01 إلا إذا رجع Cursor صفحة محددة لاحقاً. لا تبدئي دفعة جديدة حتى رسالة إطلاق رسمية.

التقرير الكامل: `operating-system/reports/quality-d01-prep.md`

## ابدئي الآن — D-01-01N → D-01-15N

| # | التذكرة | الملف |
|---:|---------|------|
| 01 | `D-01-01N` | `blog/bmi-article.html` |
| 02 | `D-01-02N` | `fitness/ramadan-calorie-calculator.html` |
| 03 | `D-01-03N` | `fitness/calorie-calculator-saudi.html` |
| 04 | `D-01-04N` | `guides/salalah-oman.html` |
| 05 | `D-01-05N` | `fitness/fitness-for-women-saudi.html` |
| 06 | `D-01-06N` | `blog/rent-vs-buy-saudi-guide-2026.html` |
| 07 | `D-01-07N` | `blog/starting-side-business-saudi-uae.html` |
| 08 | `D-01-08N` | `blog/emergency-fund-calculator-guide.html` |
| 09 | `D-01-09N` | `blog/gold-vs-savings-account-comparison.html` |
| 10 | `D-01-10N` | `featured-stories/emirati-grandmother-cooking-traditions.html` |
| 11 | `D-01-11N` | `blog/ramadan-preparation-guide-families.html` |
| 12 | `D-01-12N` | `comparisons/lease-vs-buy-car.html` |
| 13 | `D-01-13N` | `blog/family-budget-planning-guide.html` |
| 14 | `D-01-14N` | `blog/visceral-fat-gulf.html` |
| 15 | `D-01-15N` | `blog/zakat-investment-portfolios.html` |

## قانون D-01

1. أضيفي **200-400 كلمة فريدة** داخل `<article>` فقط.
2. أضيفي قيمة واحدة على الأقل: جدول صغير، سيناريو عائلة خليجية بأرقام، أخطاء شائعة، أو متى تستشير مختصاً.
3. لا حشو، لا سلاسل مترادفات، لا `قسم إضافي مفصل`.
4. لا H2 مكرر ولا `id` مكرر.
5. أي مؤسسة/جامعة/هيئة + رقم محدد = رابط عميق أو صياغة وصفية بلا اسم/رقم.
6. حافظي على Article + FAQPage صالحين وFAQ مطابق للمرئي.
7. 0 em-dash، 0 Unsplash.
8. **راحة 5 دقائق** بعد كل 5 صفحات (05 · 10 · 15).
9. اكتبي في TEAM-BUS: `D-01 05/15 جاهز للبوابة` ثم `10/15` ثم `D-01 منجز`.

## بوابة Cursor

Cursor acting QA ينشر فقط PASS. أي صفحة فيها حشو/تكرار/ادعاء بلا رابط ترجع RETURN.

## ↩️ Q-01 بوابة Cursor: 13/15 LIVE — RETURN 2 (2026-06-26 21:00)

أجزتُ 13 صفحة LIVE وأصلحتُ تقنياً ما يلزم (سكيما مكسورة، استشهادات ملفّقة، FAQ يتيمة). **صفحتان تحتاجان عملك على الجسم (لا FAQ):**

1. **`peace-capsules/beat-summer-boredom-without-screens.html`**
   - المشكلة: **4 عناوين H2 مكرّرة ×5** (`جدول-صيفي-متوازن` · `أنشطة-يدوية-ممتعة` · `أنشطة-خارجية` · `مكتبة-الصيف`) + FAQ يتيمة خارج `faq-list`.
2. **`comparisons/domestic-vs-international-travel-family.html`**
   - المشكلة: `نصائح-عملية-للتخطيط` مكرّر ×5 + `قسم-إضافي-مفصل` ×4 («هذا القسم يقدم معلومات إضافية…» نص حشو متطابق) + FAQ يتيمة.

**المطلوب لكلٍّ:** احذفي النُسخ المكرّرة (أبقي نسخة واحدة فريدة لكل قسم)، وادمجي أي FAQ يتيمة جيدة داخل `faq-list` الواحد (مع تحديث FAQPage)، ثم عمّقي بمحتوى **فريد بأرقام/أمثلة خليجية** حتى **≥1600 كلمة عربي**. الـFAQ والسكيما أصلحتُهما — لا تلمسيهما إلا للدمج.

> الاستشهادات الملفّقة («دراسة جامعة X 2024: نسبة%») = **ممنوعة**: رابط عميق موثّق أو صياغة وصفية بلا اسم/رقم.

## ⚠️ نمط تعفّن site-wide (للعلم — تذكرة لاحقة)
نفس الحشو المكرّر في 10+ صفحات خارج Q-01: `water-intake-hot-climates` · `bmi-middle-eastern-adults` · `salalah-travel-guide-2025` · `building-personal-savings-system` · `zakat-guide-2025` · `makkah-hotels-guide` · `family-volunteering-summer`. لا تبدئيها الآن — ستُفتح تذكرة dedup مستقلة.

## D18 و D19

✅ مغلقة بالكامل — لا تعودي لها.
