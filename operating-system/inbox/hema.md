# 📬 Hema — D-01 مفعّلة · تعميق قيمة

> **آخر تحديث:** 2026-06-26 22:55 — **D-01 أُغلقت 15/15 PASS.**

## رسالتي لك يا هيما

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
