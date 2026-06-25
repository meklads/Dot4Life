# 📬 Cursor — Acting QA + مدير الدفعات · 2026-06-25

## مسار متواصل (جوست)

**المرجع:** `operating-system/DEEPEN-CONTINUOUS-WORKFLOW.md` · **طابور الإصلاح:** `deepen-fix-queue.md`

| الدور | المهمة |
|-------|--------|
| **QA (A)** | راجع فور تسليم كل ملف — PASS أو RETURN (سجّل في fix-queue) |
| **بناء (C)** | صور مؤقتة + manifest + commit + push للمعتمد |
| **مدير** | عند اكتمال دفعة 10 من هيما → أطلق D12 فوراً + رسالة inbox/TEAM-BUS |
| **عتبة 50** | أوقف دفعات جديدة لهيما؛ أرسل طابور الإصلاح |

## DEEPEN Batch 11 — جاري

**التقرير:** `operating-system/reports/deepen-batch-11.md`  
**التذاكر:** `D11-01N`…`D11-10N` · `D11-XXA` · `D11-XXC`

## دور Cursor المؤقت (عامر حتى 30/6)

1. بوابة `D11-XXA` بنفس معايير عامر.
2. PASS → `D11-XXC` + صورة (approved → reuse → ستوك موثق).
3. RETURN → `deepen-fix-queue.md` — **لا توقف هيما**.
4. مراقبة دورية على ملفات D11 + git.

## الصور

- `assets/images/approved/` أولاً
- إعادة استخدام داخلي مناسب
- ستوك مجاني موثق عند الضرورة

## بعد D11

1. `scripts/launch-deepen-10.py` أو سكربت D12 — 10 مقالات تالية من طابور DEEPEN.
2. تحديث inbox/hema + TEAM-BUS برسالة «D12 — ابدئي الآن».
3. تكرار الحلقة.
