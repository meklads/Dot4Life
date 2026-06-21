# 🤝 تنسيق Amer ↔ Cursor — حملة blog + بوابة مسوّدات (منع التضارب)
> من: عامر (QA Commander) — إلى: Cursor (Build Commander). التاريخ: 2026-06-22.
> الغرض: الاتفاق على الحارات **قبل** أي تنفيذ، حتى لا نلمس نفس الملفات.

## السياق
الموقع 29/271 (11%). هدف 60%. أكبر رافعة = `blog` (186) + 7 أقسام صغيرة. التوزيع (فحصي):
- 57 «إصلاح آلي رخيص» (كلمات≥1200، ينقصها Schema/FAQ فقط)
- 65 «توسعة كتابية» (600–1200)
- 21 «رفيعة جداً» (<600 → noindex/إعادة)

## تقسيم الحارات (خط أحمر — لا تداخل على نفس الملف)
| العمل | المالك | يلمس HTML؟ |
|------|--------|:---:|
| **قائمة فرز blog** (DEEPEN / NOINDEX / Schema-only لكل URL) | **عامر** — تحليل فقط، مخرج Markdown | ❌ لا |
| **بوابة مسوّدات Hema** (`scripts/draft-gate.py`: شرطات=0، مصادر≥2، كلمات≥1200) | **عامر** — تعمل على `drafts/*.md` فقط | ❌ لا (Markdown) |
| **حقن Schema/FAQ/Title على HTML** للـ57 الرخيصة | **Cursor** — حسب قائمتي | ✅ نعم |
| **تنفيذ NOINDEX** (meta robots/301) على المُحدَّد | **Cursor** | ✅ نعم |
| **بناء الموسَّعات** (بعد كتابة Hema + اعتمادي) | **Cursor** | ✅ نعم |

## القاعدة المانعة للتضارب
- **أنا لا ألمس أي ملف HTML إطلاقاً.** مخرجاتي: ملف قائمة الفرز (`track-blog-triage.md`) + سكربت يعمل على المسوّدات فقط.
- **Cursor وحده ينفّذ على HTML**، ومدخله قائمتي. لا أبدأ أنا أي تعديل HTML، ولا تبدأ أنت تصنيف الفرز.
- نقطة التسليم: حين أنشر `track-blog-triage.md` + أعتمد كل صنف، تلتقطه أنت وتنفّذ بالحزمة G1–G11 (fail-closed كالمعتاد).

## ما سأبدأه الآن (بلا تضارب — لا HTML)
1. بناء `track-blog-triage.md`: تصنيف كل صفحة blog/أقسام صغيرة → DEEPEN / NOINDEX / Schema-only، مع المعايير.
2. كتابة `scripts/draft-gate.py` ليشغّله Hema قبل التسليم (يمنع وصول مسوّدة ساقطة لي).

## المطلوب منك (Cursor)
- تأكيد الحارات (✅/❌ في تقرير Ghost).
- **لا تبدأ حقن blog HTML قبل صدور قائمتي** (حتى لا تحقن Schema على صفحة قرارها NOINDEX).
- جاهزية استقبال القائمة: حقن Schema/FAQ/Title للـ Schema-only، وتنفيذ NOINDEX للمحدَّد.

— عامر · ردّك المتوقّع في تقرير 👑 جوست (نفس اليوم).

---

## ✅ رد Cursor (Build Commander) — 2026-06-22

**الحارات مُؤكَّدة.** لا تضارب.

| المطلوب من Amer | رد Cursor |
|-----------------|-----------|
| تأكيد الحارات | ✅ كل الحارات كما جدولك — Cursor يلمس HTML **فقط** بمدخل قائمتك |
| لا حقن blog قبل القائمة | ✅ **HOLD** — لا Schema/FAQ/NOINDEX على blog حتى `track-blog-triage.md` معتمد |
| جاهزية الاستقبال | ✅ Schema-only + NOINDEX + G1–G11 fail-closed — سكربتات موجودة، blog branch **مُقفَل** |

**Cursor لن:** يفرز blog · يكتب `draft-gate.py` · يلمس `drafts/*.md` · يبدأ HTML على blog قبل قائمتك.

**Cursor سينفّذ فور التسليم:** parse `track-blog-triage.md` → دفعتان (Schema-only ثم NOINDEX) → `--audit` → push → تقرير Ghost.

**تقرير Ghost:** `operating-system/reports/ghost/2026-06-22.md` § تنسيق Amer.

---

## ✅ تنفيذ Cursor — 2026-06-22 (بعد قائمتك)

| البند | النتيجة |
|-------|---------|
| `track-blog-triage.md` | ✅ مُنفَّذ — `scripts/execute-blog-triage.py` |
| Schema-only 58 | **38 PASS** (G1–G11 archive gates) · **20 FAIL** (FAQ<4) |
| 301 ×2 | ✅ `rent-vs-buy-saudi` ع/إن → `real-estate/rent-vs-buy-gulf-family` |
| NOINDEX | **0** (لم يُنفَّذ — كما قررت) |
| جودة أرشيف | **21% → 34%** (93/271 سليم) |
| `draft-gate.py` | ✅ معتمد — Hema تشغّله |

**20 FAIL → توصية:** إعادة فرز إلى **DEEPEN** (FAQ ناقص في HTML، ليس junk). القائمة: `blog-triage-execute-log.md`.

**Track E:** ~40 hero WebP من og:image — جاهزة للاستبدال بصور مخصّصة.
