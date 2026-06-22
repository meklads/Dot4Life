# 👑 لوحة التسليم — Handoff Board (Trello لجوست)

> **أنت = الـ Hub.** عمود = عضو · لما يقول «انتهيت» → انقل البطاقة · انسخ الأمر.
> **الواجهة البصرية:** `system/board.html` → **🔀 التسليم (Trello)**
> **المصدر:** `handoff-tickets.json` · آخر مزامنة: 2026-06-22

---

## 📋 عند جوست — ابدأ من هنا

| ID | slug | المهمة | أمر عند التسليم |
|----|------|--------|------------------|
| H-07 | `investment-basics-beginners` | صورة LIVE · استثمار المبتدئ | H-07: برومبت استثمار المبتدئ — omar-image-table #1 |
| H-08 | `rent-vs-buy-gulf-family` | صورة LIVE · إيجار vs تملّك | H-08: برومبت إيجار vs تملّك |
| H-09 | `daily-walking-benefits` | صورة LIVE · فوائد المشي | H-09: برومبت فوائد المشي |
| H-10 | `pregnancy-week-by-week` | صورة LIVE · الحمل أسبوعياً | H-10: برومبت الحمل أسبوعياً |
| H-11 | `preconception-checkups` | صورة LIVE · فحوصات ما قبل الحمل | H-11: برومبت فحوصات ما قبل الحمل |
| H-12 | `umrah-with-kids` | صورة LIVE · العمرة مع الأطفال | H-12: برومبت العمرة مع الأطفال |
| H-13 | `hijri-new-year-children` | صورة LIVE · رأس السنة الهجرية | H-13: برومبت رأس السنة الهجرية |
| H-14 | `teaching-children-allah-names` | صورة LIVE · أسماء الله | H-14: برومبت أسماء الله |
| H-15 | `teaching-children-prayer-with-love` | صورة LIVE · الصلاة بالحب | H-15: برومبت الصلاة بالحب |
| H-16 | `jeddah-mortgage-calculator` | صورة LIVE · تمويل جدة | H-16: برومبت تمويل جدة |

---

## 🎨 عند عمر

| ID | slug | حالة | أمر |
|----|------|------|-----|
| — | — | — | — |

---

## 🤖 عند كلود — توليد Higgsfield

| ID | slug | حالة | أمر |
|----|------|------|-----|
| — | — | — | — |

---

## ✍️ عند Hema — نص

| ID | slug | حالة | أمر |
|----|------|------|-----|
| T-02 | `A-09` | REVISE | T-02: أعد REVISE في drafts/task09/ ثم سلّم لعامر |

---

## ⚙️ عند Cursor — بناء

| ID | slug | حالة | ملاحظة |
|----|------|------|--------|
| — | — | — | — |

---

## 🛡️ عند عامر — BUILD VERIFY

| ID | slug | حالة | أمر |
|----|------|------|-----|
| — | — | — | — |

---

## ✅ منتهي

| ID | slug | انتهى |
|----|------|-------|
| H-01 | `family-budget-plan` | 2026-06-22 |
| H-02 | `bmi-calculator-women` | 2026-06-22 |
| H-03 | `daily-adhkar-family-guide` | 2026-06-22 |
| H-04 | `children-sleep-summer` | 2026-06-22 |
| H-05 | `family-friendly-activities-gulf-cities` | 2026-06-22 |
| H-06 | `best-family-destinations-gulf` | 2026-06-22 |

---

## مسار الصورة

```
جوست → عمر (برومبت) → كلود → عمر (اعتماد) → Cursor → عامر → ✅
```

## ثبّت التسليم

```bash
python3 scripts/handoff_move.py H-07 omar
```
