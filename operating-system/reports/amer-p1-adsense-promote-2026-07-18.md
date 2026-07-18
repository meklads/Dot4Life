# تقرير تنفيذ أمر عامر P1 — أدسنس noindex + ترقية (2026-07-18)

## 1) إزالة أدسنس من صفحات noindex

- **عدد الصفحات التي أُزيل منها كود الإعلانات:** **50**
- متبقي `noindex` + `adsbygoogle` في الموقع: **0**
- شمل الإزالة: مقالات + أدوات داخل القائمة + `admin.html` + `assets/queue/*` + `system/review.html` + `site/system/review.html`

## 2) التدقيق والترقية

المعيار لكل ملف (باستثناء admin و assets/queue): كلمات `article-body` عبر `amer_gate.body_word_count` ≥ 1350 · أسئلة FAQPage تطابق `.faq-item` حرفياً · صفر فقرة مكررة ≥3 بعد تجريد الأرقام · canonical موجود.

- مرّ التدقيق: **45** ملفاً (39 نظيفة أصلاً + 5 معمّقة + تصحيح FAQ ظاهري لملفين كانا يُحسبان خطأً بسبب زر النسخ)
- **رُقّي فعلياً إلى `index,follow`:** **45** ملفاً (القائمة أدناه)
- لم تُرقَّ: `admin.html` · `assets/queue/*` · `system/review.html` · `site/system/review.html`

### الخمسة — عدد الكلمات النهائي (`amer_gate`)

| الملف | كلمات قبل | كلمات بعد |
|---|---:|---:|
| `blog/hydration-guide.html` | 1303 | **1418** |
| `blog/stress-management-working-parents-en.html` | 1303 | **1453** |
| `health/mindful-family-meal-nutrition-faith.html` | 1305 | **1405** |
| `health/mindful-family-meal-nutrition-faith-en.html` | 1340 | **1471** |
| `islamic-hajj-umrah/hijri-new-year-children.html` | 1314 | **1434** (+ تحويل FAQ إلى `.faq-item` مطابق للـschema) |

### قائمة الملفات المُرقّاة (45)

1. `blog/ashura-family-traditions-gulf.html`
2. `blog/building-personal-savings-system-en.html`
3. `blog/children-education-savings-guide-en.html`
4. `blog/choosing-right-school-child-gulf-en.html`
5. `blog/daily-walking-benefits.html`
6. `blog/family-friendly-activities-gulf-cities-en.html`
7. `blog/family-nutrition-on-budget-en.html`
8. `blog/family-travel-planning-without-overspending-en.html`
9. `blog/hajj-umrah-guide-2025.html`
10. `blog/hydration-guide.html`
11. `blog/life-insurance-gulf-families-en.html`
12. `blog/managing-healthcare-costs-families-en.html`
13. `blog/managing-screen-time-children-en.html`
14. `blog/managing-screen-time-children.html`
15. `blog/medina-hotels-near-masjid-nabawi.html`
16. `blog/organize-life-daily-systems-en.html`
17. `blog/pregnancy-and-umrah-guide.html`
18. `blog/pregnancy-weeks-guide-en.html`
19. `blog/pregnancy-weeks-guide.html`
20. `blog/preparing-for-pregnancy-guide-en.html`
21. `blog/starting-side-business-saudi-uae-en.html`
22. `blog/stress-management-working-parents-en.html`
23. `blog/water-intake-hot-climates-guide-en.html`
24. `blog/zakat-calculator-modern-investments-guide-en.html`
25. `comparisons/government-vs-private-school-gulf.html`
26. `featured-stories/engineer-simplified-family-life.html`
27. `featured-stories/gulf-father-money-lessons.html`
28. `finance-wealth/investment-basics-beginners.html`
29. `fitness/calorie-calculator-saudi.html`
30. `health-pregnancy/preconception-checkups.html`
31. `health/children-sleep-summer.html`
32. `health/daily-walking-benefits.html`
33. `health/mindful-family-meal-nutrition-faith-en.html`
34. `health/mindful-family-meal-nutrition-faith.html`
35. `islamic-hajj-umrah/daily-adhkar-family-guide.html`
36. `islamic-hajj-umrah/hijri-new-year-children.html`
37. `islamic-hajj-umrah/teaching-children-prayer-with-love.html`
38. `islamic-hajj-umrah/umrah-with-kids.html`
39. `peace-capsules/calm-corner-small-space.html`
40. `peace-capsules/calm-morning-routine-family.html`
41. `peace-capsules/family-volunteering-summer.html`
42. `productivity/family-time-management-en.html`
43. `productivity/family-time-management.html`
44. `real-estate/home-as-sanctuary-family-wellbeing.html`
45. `real-estate/jeddah-mortgage-calculator.html`

JSON الخام: `operating-system/reports/amer-p1-adsense-promote-2026-07-18.json`
