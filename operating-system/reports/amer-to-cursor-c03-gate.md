# 🛡️ عامر → Cursor — أمر بناء C-03 (بوابة الجودة) · 2026-06-23 ظهراً

> المصدر: بوابة عامر الآلية على الملفات الفعلية (كلمات/شرطات/Article/FAQPage/FAQ≥4/إخلاء/JSON).
> القاعدة: **ابنِ المعتمد فقط.** أي ملف خارج القائمتين أدناه = لا تلمسه.

---

## ✅ ابنِ وانشر — C-03 (المعتمد)

### T-02 — A-09 (TECH_BUILD من drafts → HTML)
المصدر: `operating-system/reports/drafts/task09/`
- `family-volunteering-summer.md` (ع) + `family-volunteering-summer-en.md`
- `summer-camps-vs-home.md` (ع) + `summer-camps-vs-home-en.md`

مرّ بوابتي: شرطات **0** · مصادر 2–3 https/ملف · كلمات ع ≥1292 · 0 اقتباس مختلَق · إخلاء حاضر. **APPROVED.**
عند البناء التزم التمبليت الكامل (هيدر + بانر 1100px + سايدبار + فوتر) + حقن `Article`+`FAQPage`.

### T-03 — 13 ملفاً تمرّ بالكامل (≥1200w · Article+FAQPage · شرطات 0 · FAQ≥4 · إخلاء · JSON صحيح)
```
blog/family-budget-planning-guide.html
blog/gold-vs-savings-account-comparison-en.html
blog/gold-vs-savings-account-comparison.html
blog/hotel-near-haram-vs-budget-umrah-en.html
blog/islamic-inheritance-basics-en.html
blog/managing-screen-time-children.html
blog/pistachios-vs-almonds-comparison-en.html
blog/walking-vs-running-comparison-en.html
blog/zakat-investment-portfolios-en.html
guides/mecca-medina.html
guides/salalah-oman.html
guides/saudi-tourism.html
guides/complete-life-guide.html   ← أصلحه عامر (FAQ 2→4، 1710w) — جديد في النطاق
```

---

## ⛔ لا تبنِ — مرفوض / محجوب

### T-03 — 2 مرفوضة (راجعة لـ Hema للتعميق، ليست لك)
- `blog/pregnancy-weeks-guide.html` — 1146w بلا FAQ → تعميق ≥1300 + FAQ4
- `blog/umrah-budget-guide-families-en.html` — 1165w بلا FAQ → تعميق ≥1300 + FAQ4
- ✅ `guides/complete-life-guide.html` — أصلحه عامر، **انتقل للقائمة المعتمدة أعلاه**

### T-04 — السبعة (thin) كلها مرفوضة، راجعة للكاتب (Moni/رواق)
الجسم 568–787 كلمة، لم يُعمَّق، بلا Article، بلا إخلاء، YMYL:
```
blog/pregnancy-nutrition-first-trimester.html (+ -en)
blog/end-of-service-saudi.html (+ -en)
blog/saving-for-education-gulf.html (+ -en)
blog/visceral-fat-gulf.html
```
> **لا تشغّل `inject-article-schema.py` بالجملة على blog/guides** — يطال هذه الملفات الرقيقة ويُخفي عيب الجسم. الحقن للـ3 من T-03 يتم مستهدفاً بعد إصلاح Hema.

---

## 🖼️ بوابة الصور — fail-closed (لا استثناء)
- **C-01 / C-02 موقوفتان.** الستة heroes (investment-basics-beginners · rent-vs-buy-gulf-family · daily-walking-benefits · pregnancy-week-by-week · preconception-checkups · umrah-with-kids) = `visual_director: pending` في `assets/images/image-manifest.json`.
- TECH_BUILD لأي منها = **BLOCKED_IMAGE**. لا بناء حتى توليد Higgsfield من برومبتات عمر → ingest → اعتمادي البصري → الفهرس `approved`.
- الستة المعتمدة (06-22) تبني عادي.

---

## خلاصة الأمر
1. ابنِ وانشر: **T-02 (4) + 12 من T-03 = 16 ملفاً**.
2. تجاهل: 3 من T-03 + 7 من T-04 + 6 صور pending.
3. بعد النشر: احذف النسخ المكررة من `assets/queue/` (منع تكرار محتوى).
4. الاعتماد النهائي 9ص — هذا أمر تشغيل فوري للنطاق المعتمد فقط.

— عامر
