# ✅ BUILD VERIFY — تدقيق مستقل للصفحات الحيّة (Amer)
> التاريخ: 2026-06-21. أداة: فحص بوابات G1–G6+G9 على الأقسام المبنية. مستقل عن سكربت Cursor.

## النتيجة
- فُحص: **29** صفحة مقال (finance-wealth, health, health-pregnancy, real-estate, islamic-hajj-umrah).
- **تمرّ كل البوابات: 28** (em-dash=0, words≥1200, Article, FAQPage≥4Q, WebP, Title≤60, إخلاء للحساس).
- **ساقط: 1** → `real-estate/oman-property-roi.html` (729w · ناقص Article/FAQ/Title/إخلاء) — **معروف ومحجوز** (حاسبة shell، ينتظر الحقن الجراحي). ليس انحداراً.

## الحكم
- **الـ28 LIVE = BUILD VERIFIED في مكانها ✅** (الدفعة التي شُحنت أثناء غيابي تمرّ الحزمة الكاملة — لا rebuild).
- العنصر الوحيد المتبقّي = oman-property-roi → **GO للحقن الجراحي** (قسم مقال أسفل الحاسبة + Article/FAQPage/إخلاء، دون مسّ الأداة).

## التوصية لـCursor
1. ~~صلّب `build-from-approved-draft.py` بحزمة G1–G11 + `assert_parity()`~~ ✅ **تم 2026-06-21** (`scripts/build-from-approved-draft.py --audit`)
2. استثناءات مؤكَّدة: EN-only (BMI, pregnancy-week) · `disclaimer_type` في BUILD_MAP · G2 نثر المسوّدة · G7 يقيس Meta بعد decode
3. كل دفعة جديدة (A-09+) تمرّ الحزمة من أول مرة — هدف 0 REOPEN.

## تدقيق Cursor (2026-06-21 — بعد G1–G11)
```
python3 scripts/build-from-approved-draft.py --audit
→ 28 pages ALL GATES PASS + parity OK
→ oman-property-roi SKIP (shell — GO حقن جراحي)
```
**لا rebuild** — Amer audit + Cursor audit متطابقان.
