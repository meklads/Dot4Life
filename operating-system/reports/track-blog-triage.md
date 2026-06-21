# 🗂️ قائمة فرز blog + الأقسام الصغيرة — Track Blog Triage
> يضعها عامر (تحليل/QA، بلا لمس HTML). ينفّذها Cursor على HTML بمدخل هذه القائمة. التاريخ: 2026-06-22.
> **حُكم المدير: لا NOINDEX لمحتوى قيّم.** الذيل الرفيع كله مواضيع بحثية تستحق التعميق لا الإخفاء. الإزالة الوحيدة = مكرّر مؤكّد (301).

## الملخّص
- **Schema-only (حقن آلي): 58**
- **301 redirect (مكرّر): 2**
- **DEEPEN (كتابة Hema): 84**
- **NOINDEX (junk): 0** — لا يوجد محتوى عديم القيمة نخفيه.

## ⚠️ تبعية حاكمة لـCursor
صفحات Schema-only قد ينقصها أيضاً **صورة WebP رئيسية** (G5). حقن Schema وحده لا يكفي للمرور — يلزم hero لكل صفحة. نسّق مع Track E (الصور) قبل توقّع PASS كامل.

## 1) Schema-only → Cursor يحقن Article+FAQPage+Title/Meta (G1–G11 fail-closed)
| # | الملف | كلمات |
|---|------|------:|
| 1 | `blog/bmi-middle-eastern-adults.html` | 1333 |
| 2 | `blog/building-personal-savings-system-en.html` | 1954 |
| 3 | `blog/building-personal-savings-system.html` | 1253 |
| 4 | `blog/children-education-savings-guide-en.html` | 2077 |
| 5 | `blog/choosing-right-school-child-gulf-en.html` | 1800 |
| 6 | `blog/daily-islamic-habits-guide-en.html` | 1336 |
| 7 | `blog/digital-minimalism-families-en.html` | 3072 |
| 8 | `blog/digital-minimalism-families.html` | 3001 |
| 9 | `blog/end-of-service-benefits-expats-en.html` | 1449 |
| 10 | `blog/family-budget-planning-guide-en.html` | 1368 |
| 11 | `blog/family-budget-planning-guide.html` | 2211 |
| 12 | `blog/family-friendly-activities-gulf-cities-en.html` | 1504 |
| 13 | `blog/family-nutrition-on-budget-en.html` | 1776 |
| 14 | `blog/family-nutrition-on-budget.html` | 1429 |
| 15 | `blog/family-travel-planning-without-overspending-en.html` | 2345 |
| 16 | `blog/family-travel-planning-without-overspending.html` | 2310 |
| 17 | `blog/gold-vs-savings-account-comparison-en.html` | 1450 |
| 18 | `blog/gold-vs-savings-account-comparison.html` | 1309 |
| 19 | `blog/hotel-near-haram-vs-budget-umrah-en.html` | 1231 |
| 20 | `blog/islamic-inheritance-basics-en.html` | 1210 |
| 21 | `blog/life-insurance-gulf-families-en.html` | 1645 |
| 22 | `blog/managing-healthcare-costs-families-en.html` | 1511 |
| 23 | `blog/managing-screen-time-children-en.html` | 1835 |
| 24 | `blog/managing-screen-time-children.html` | 1213 |
| 25 | `blog/medina-hotels-near-masjid-nabawi-en.html` | 1572 |
| 26 | `blog/medina-hotels-near-masjid-nabawi.html` | 1806 |
| 27 | `blog/organize-life-daily-systems-en.html` | 2092 |
| 28 | `blog/organize-life-daily-systems.html` | 1375 |
| 29 | `blog/pistachios-vs-almonds-comparison-en.html` | 1212 |
| 30 | `blog/pregnancy-weeks-guide-en.html` | 1299 |
| 31 | `blog/pregnancy-weeks-guide.html` | 1205 |
| 32 | `blog/preparing-for-pregnancy-guide-en.html` | 2140 |
| 33 | `blog/ramadan-preparation-guide-families-en.html` | 1962 |
| 34 | `blog/rent-vs-buy-saudi-guide-2026-en.html` | 1819 |
| 35 | `blog/starting-side-business-saudi-uae-en.html` | 1339 |
| 36 | `blog/stress-management-working-parents-en.html` | 1502 |
| 37 | `blog/teaching-children-financial-literacy-en.html` | 1934 |
| 38 | `blog/teaching-children-financial-literacy.html` | 1334 |
| 39 | `blog/umrah-budget-guide-families-en.html` | 1209 |
| 40 | `blog/umrah-visa-gulf-residents-guide-en.html` | 1545 |
| 41 | `blog/umrah-visa-gulf-residents-guide.html` | 1867 |
| 42 | `blog/walking-vs-running-comparison-en.html` | 1226 |
| 43 | `blog/water-intake-hot-climates-guide-en.html` | 1341 |
| 44 | `blog/water-intake-hot-climates-guide.html` | 1289 |
| 45 | `blog/zakat-calculator-modern-investments-guide-en.html` | 1287 |
| 46 | `blog/zakat-investment-portfolios-en.html` | 1278 |
| 47 | `comparisons/saving-vs-investing-gulf-family-en.html` | 1515 |
| 48 | `comparisons/saving-vs-investing-gulf-family.html` | 1397 |
| 49 | `guides/bmi-guide-arabs-gcc.html` | 1898 |
| 50 | `guides/complete-life-guide.html` | 1439 |
| 51 | `guides/indoor-plants-saudi-arabia.html` | 2479 |
| 52 | `guides/mecca-medina.html` | 2931 |
| 53 | `guides/ramadan-nutrition-guide.html` | 2359 |
| 54 | `guides/salalah-oman.html` | 2236 |
| 55 | `guides/saudi-mortgage-guide.html` | 2085 |
| 56 | `guides/saudi-real-estate-investing.html` | 2257 |
| 57 | `guides/saudi-tourism.html` | 2367 |
| 58 | `guides/zakat-complete-guide.html` | 1741 |

## 2) 301 redirect → Cursor (مكرّر لصفحة مبنية)
| الملف | → الوجهة |
|------|--------|
| `blog/rent-vs-buy-saudi-en.html` | `real-estate/rent-vs-buy-gulf-family.html` |
| `blog/rent-vs-buy-saudi.html` | `real-estate/rent-vs-buy-gulf-family.html` |

## 3) DEEPEN → طابور Hema (الأهزل أولاً، يمرّ draft-gate ثم اعتمادي ثم بناء Cursor)
| # | الملف | كلمات الآن |
|---|------|------:|
| 1 | `travel/best-family-destinations-gulf-en.html` | 233 |
| 2 | `travel/best-family-destinations-gulf.html` | 250 |
| 3 | `productivity/family-time-management-en.html` | 259 |
| 4 | `productivity/family-time-management.html` | 288 |
| 5 | `featured-stories/featured-story-arab-father-teens-en.html` | 387 |
| 6 | `blog/saving-for-education-gulf.html` | 392 |
| 7 | `blog/pregnancy-nutrition-first-trimester.html` | 409 |
| 8 | `featured-stories/featured-story-gulf-family-home-en.html` | 413 |
| 9 | `featured-stories/featured-story-saudi-mother-en.html` | 421 |
| 10 | `blog/end-of-service-saudi.html` | 432 |
| 11 | `blog/saving-for-education-gulf-en.html` | 438 |
| 12 | `blog/pregnancy-nutrition-first-trimester-en.html` | 445 |
| 13 | `featured-stories/featured-story-saudi-mother.html` | 446 |
| 14 | `blog/end-of-service-saudi-en.html` | 480 |
| 15 | `comparisons/comparisons-public-vs-private-education-en.html` | 482 |
| 16 | `featured-stories/featured-story-arab-father-teens.html` | 505 |
| 17 | `blog/body-fat-vs-weight-guide.html` | 512 |
| 18 | `featured-stories/featured-story-gulf-family-home.html` | 535 |
| 19 | `blog/visceral-fat-gulf.html` | 586 |
| 20 | `blog/body-fat-vs-weight-guide-en.html` | 612 |
| 21 | `blog/house-affordability-single-income-guide.html` | 627 |
| 22 | `comparisons/comparisons-ready-vs-build-home-en.html` | 644 |
| 23 | `blog/ramadan-preparation-guide-families.html` | 656 |
| 24 | `comparisons/comparisons-public-vs-private-education.html` | 660 |
| 25 | `blog/visceral-fat-gulf-en.html` | 672 |
| 26 | `featured-stories/arab-mother-startup.html` | 682 |
| 27 | `blog/mindful-living-gulf-heat.html` | 691 |
| 28 | `peace-capsules/peace-at-home-5-steps-en.html` | 709 |
| 29 | `blog/mindful-living-gulf-heat-en.html` | 736 |
| 30 | `peace-capsules/peace-at-home-5-steps.html` | 759 |
| 31 | `blog/rent-vs-buy-saudi-guide-2026.html` | 764 |
| 32 | `featured-stories/arab-mother-startup-en.html` | 783 |
| 33 | `blog/umrah-packing-checklist-guide.html` | 791 |
| 34 | `blog/expat-vs-national-finance.html` | 806 |
| 35 | `blog/ramadan-meal-planning.html` | 811 |
| 36 | `comparisons/lease-vs-buy-car.html` | 812 |
| 37 | `blog/emergency-fund-calculator-guide.html` | 818 |
| 38 | `comparisons/comparisons-ready-vs-build-home.html` | 822 |
| 39 | `comparisons/domestic-vs-international-travel-family-en.html` | 822 |
| 40 | `blog/expat-vs-national-finance-en.html` | 823 |
| 41 | `comparisons/lease-vs-buy-car-en.html` | 868 |
| 42 | `fitness/calorie-calculator-saudi.html` | 876 |
| 43 | `blog/ramadan-meal-planning-en.html` | 893 |
| 44 | `peace-capsules/evening-rituals-en.html` | 894 |
| 45 | `blog/starting-side-business-saudi-uae.html` | 918 |
| 46 | `blog/family-friendly-activities-gulf-cities.html` | 923 |
| 47 | `blog/end-of-service-benefits-expats.html` | 933 |
| 48 | `fitness/ramadan-calorie-calculator.html` | 937 |
| 49 | `blog/rent-vs-buy-comparison-guide.html` | 941 |
| 50 | `blog/bmi-article.html` | 943 |
| 51 | `fitness/fitness-for-women-saudi.html` | 951 |
| 52 | `featured-stories/saudi-father-carpentry-workshop.html` | 961 |
| 53 | `peace-capsules/beat-summer-boredom-without-screens.html` | 962 |
| 54 | `blog/bmi-middle-eastern-adults-en.html` | 963 |
| 55 | `blog/notification-cost-productivity.html` | 970 |
| 56 | `blog/stress-management-working-parents.html` | 997 |
| 57 | `blog/rental-property-vs-reits-comparison.html` | 998 |
| 58 | `blog/bmi-article-en.html` | 1011 |
| 59 | `blog/islamic-inheritance-basics.html` | 1012 |
| 60 | `blog/managing-healthcare-costs-families.html` | 1024 |
| 61 | `blog/house-affordability-single-income-guide-en.html` | 1029 |
| 62 | `blog/umrah-budget-guide-families.html` | 1030 |
| 63 | `blog/notification-cost-productivity-en.html` | 1036 |
| 64 | `blog/rent-vs-buy-comparison-guide-en.html` | 1037 |
| 65 | `blog/children-education-savings-guide.html` | 1039 |
| 66 | `blog/natural-birth-vs-c-section-comparison.html` | 1052 |
| 67 | `peace-capsules/beat-summer-boredom-without-screens-en.html` | 1058 |
| 68 | `peace-capsules/evening-rituals.html` | 1063 |
| 69 | `blog/pistachios-vs-almonds-comparison.html` | 1070 |
| 70 | `blog/salalah-khareef.html` | 1082 |
| 71 | `blog/rental-property-vs-reits-comparison-en.html` | 1095 |
| 72 | `featured-stories/saudi-father-carpentry-workshop-en.html` | 1095 |
| 73 | `blog/daily-islamic-habits-guide.html` | 1096 |
| 74 | `blog/zakat-calculator-modern-investments-guide.html` | 1097 |
| 75 | `blog/emergency-fund-calculator-guide-en.html` | 1103 |
| 76 | `blog/hotel-near-haram-vs-budget-umrah.html` | 1103 |
| 77 | `blog/life-insurance-gulf-families.html` | 1122 |
| 78 | `blog/natural-birth-vs-c-section-comparison-en.html` | 1123 |
| 79 | `blog/zakat-investment-portfolios.html` | 1123 |
| 80 | `blog/preparing-for-pregnancy-guide.html` | 1127 |
| 81 | `blog/walking-vs-running-comparison.html` | 1133 |
| 82 | `blog/salalah-khareef-en.html` | 1172 |
| 83 | `blog/choosing-right-school-child-gulf.html` | 1186 |
| 84 | `blog/umrah-packing-checklist-guide-en.html` | 1192 |