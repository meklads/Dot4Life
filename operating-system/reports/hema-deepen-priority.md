# Hema — طابور DEEPEN (أولوية)

> **المالك:** Hema · **البوابة:** `scripts/draft-gate.py` · **محدّث:** 2026-06-24  
> **الهدف:** رفع الجودة من **35%** → **60%** (يحتاج ~68 صفحة إضافية سليمة)

## ⛔ تجميد مواد جديدة (جوست · 2026-06-24)

**155 صفحة DEEPEN** — لا Batch 04+ ولا مقالات جديدة بعد انتهاء **Batch 03**.
المرجع: `operating-system/QUALITY-FIRST-POLICY.md` · البوابة: `scripts/deepen_gate.py`

**الأولوية:** (1) إكمال B3 · (2) تقليص الـ155 بـ WRITING-LAW ≥1600w · (3) بعد AN-00 مضاعفة الرابح.

## ✅ تحديث كورسر 2026-07-13
- **Wave5:** كل مقالات LIVE ذات جسم `<article>` تحت 1600 كلمة رُفعت إلى ≥1600 (54 صفحة) — `operating-system/reports/cursor-wave5-to1600-review.json`
- **متبقي LIVE&lt;1600 = 0** (باستثناء HARD_SKIP إن وُجد)
- رقم `deepen_gate` الخام (~68) = stubs `*-ar.html` + redirects `complete-*` — ليس طابور كتابة حي
- **AN-00:** مسودة أساس في `operating-system/reports/an00-traffic-baseline-2026-07-13.md` — بانتظار CSV أداء GSC من جوست

## ⚠️ تصحيح 2026-06-23
`hema-deepen-priority-top25.txt` **قديم وخاطئ** — كان يعدّ صفحات `complete-*` redirects (C-F2) بلا محتوى.  
**لا تستخدمه.** القوائم النشطة:

| تذكرة | الملف | العدد |
|-------|-------|------:|
| **T-03** | `hema-deepen-t03-blog-triage-15.txt` | 15 |
| **T-04** | `hema-deepen-t04-thin-7.txt` | 7 |

**المجموع = 22** صفحة محتوى حقيقي (blog triage FAIL + thin live).

## القاعدة
- **174 صفحة قصيرة** (<1200 كلمة) = DEEPEN طويل الأمد — لا يصلحها السكربت وحده
- بعد التعميق: Self-QA → Amer → Cursor TECH_BUILD
- **≥1300 كلمة** · **FAQ≥4** · **Schema** · **0 em-dash** · **https links**

## T-03 — blog triage FAIL (15)
من `blog-triage-execute-log.md` — FAQ ناقص / G2 / HTML تالف.

## T-04 — thin live (7)
Track B أولوية AdSense: حمل، نهاية خدمة، ادخار تعليم، visceral fat.

## لاحقاً (مخزون جوست T-05…)
Track B أسوأ 20 · باقي blog DEEPEN (84) — `track-blog-triage.md` §3.

## لا تلمس
- **29 LIVE** gated — rebuild فقط بعد manifest عمر
- hub `complete-*` — C-F2 redirects (301 فقط، لا DEEPEN)

---

*Cursor · GSystem · 2026-06-23*
