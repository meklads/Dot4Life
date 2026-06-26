# Q-01 — رفع جودة FAQ إلى 8+/10

> **انطلاق:** 2026-06-26 18:20 · **المالك:** هيما · **المراجع:** Cursor acting QA
> **المرجع:** `quality-phase-2-plan.md` · لا slugs جديدة.

## القاعدة
- كل إجابة FAQ = **رقم أو خطوة أو مثال خليجي** في أول جملتين.
- السكيما = النص المرئي حرفياً.
- ممنوع: سلاسل صفات، «دليل شامل»، تكرار السؤال في الجواب.
- **لا تلمس الجسم** إلا إذا لزم لمواءمة FAQ.
- راحة **5 دقائق** بعد كل 5 صفحات.

| # | التذكرة | الملف | ARw | المطلوب |
|---:|---------|------|----:|---------|
| 01 | `Q-01-01N` | `islamic-hajj-umrah/umrah-with-kids.html` | 1650 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 02 | `Q-01-02N` | `islamic-hajj-umrah/hijri-new-year-children.html` | 2106 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 03 | `Q-01-03N` | `islamic-hajj-umrah/daily-adhkar-family-guide.html` | 1730 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 04 | `Q-01-04N` | `featured-stories/featured-story-gulf-family-home.html` | 1601 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 05 | `Q-01-05N` | `blog/family-friendly-activities-gulf-cities.html` | 1602 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 06 | `Q-01-06N` | `blog/daily-islamic-habits-guide.html` | 1607 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 07 | `Q-01-07N` | `islamic-hajj-umrah/teaching-children-allah-names.html` | 1644 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 08 | `Q-01-08N` | `blog/hydration-guide.html` | 1679 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 09 | `Q-01-09N` | `peace-capsules/beat-summer-boredom-without-screens.html` | 3742 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 10 | `Q-01-10N` | `finance-wealth/investment-basics-beginners.html` | 1915 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 11 | `Q-01-11N` | `featured-stories/saudi-father-carpentry-workshop.html` | 1606 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 12 | `Q-01-12N` | `featured-stories/featured-story-saudi-mother.html` | 1602 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 13 | `Q-01-13N` | `comparisons/gold-vs-real-estate-gulf-family.html` | 1607 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 14 | `Q-01-14N` | `comparisons/domestic-vs-international-travel-family.html` | 2488 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |
| 15 | `Q-01-15N` | `blog/umrah-with-kids-guide.html` | 1802 | إعادة FAQ بأرقام/خطوات/أمثلة خليجية |

## بعد كل 5 صفحات
اكتب في TEAM-BUS: `Q-01 05/15 جاهز للبوابة` (ثم 10/15، 15/15).

## بوابة Cursor acting QA — 2026-06-26 21:00

فحص مستقلّ على الـ15 ملفاً (`scripts/q01_qa.py`): JSON-LD صالح · FAQPage = FAQ المرئي · 0 em-dash · 0 Unsplash · استشهادات بروابط أو وصفية · 0 FAQ يتيمة.

**النتيجة: 13/15 LIVE (PASS) + 2 RETURN.**

| # | الملف | القرار | إصلاح Cursor |
|---:|------|--------|---------------|
| 01 | umrah-with-kids | ✅ LIVE | حذف FAQPage مكسورة+مكررة (`<a href>` كسر JSON) |
| 02 | hijri-new-year-children | ✅ LIVE | — |
| 03 | daily-adhkar-family-guide | ✅ LIVE | — |
| 04 | featured-story-gulf-family-home | ✅ LIVE | — |
| 05 | family-friendly-activities-gulf-cities | ✅ LIVE | — |
| 06 | daily-islamic-habits-guide | ✅ LIVE | — |
| 07 | teaching-children-allah-names | ✅ LIVE | — |
| 08 | hydration-guide | ✅ LIVE | إزالة استشهاد «الملك سعود 60%» الملفّق (نص+سكيما) |
| 09 | beat-summer-boredom-without-screens | ↩️ RETURN | أصلحت 3 استشهادات ملفّقة؛ الجسم: 4×H2 مكررة ×5 + FAQ يتيمة |
| 10 | investment-basics-beginners | ✅ LIVE | إزالة استشهاد «الملك سعود» الملفّق |
| 11 | saudi-father-carpentry-workshop | ✅ LIVE | — |
| 12 | featured-story-saudi-mother | ✅ LIVE | — |
| 13 | gold-vs-real-estate-gulf-family | ✅ LIVE | — |
| 14 | domestic-vs-international-travel | ↩️ RETURN | أصلحت استشهاد «عبدالعزيز 80%»؛ الجسم: نصائح-عملية ×5 + قسم-إضافي ×4 + FAQ يتيمة |
| 15 | umrah-with-kids-guide | ✅ LIVE | حذف FAQ يتيمة بسلاسل مترادفات + `id="faq"` مكرّر |

**RETURN لهيما (جسم لا FAQ):** أزيلي الأقسام (H2) المكرّرة وادمجي FAQ اليتيمة ضمن قسم واحد، ثم عمّقي بمحتوى **فريد** حتى ≥1600 كلمة. الـFAQ والسكيما فيهما نظيفة الآن.

**⚠️ نمط site-wide:** نفس تعفّن «قسم إضافي مفصل»/H2 مكررة في 10+ صفحات خارج Q-01 (water-intake · bmi-middle-eastern-adults · salalah-travel-guide · building-personal-savings · zakat-guide-2025 · makkah-hotels · family-volunteering) — يُقترح تذكرة `dedup` مستقلة.

## الأسبوع 2 (مُجدول — لا تبدأ قبل إغلاق Q-01)
D-01 تعميق قيمة +200–400w — انظر `quality-phase-2-plan.md`.
