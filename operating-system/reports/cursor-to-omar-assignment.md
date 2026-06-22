# 🖼️ تكليف مباشر من Cursor → عمر

> **من:** Cursor (Build Commander)  
> **إلى:** عمر (المدير البصري)  
> **التاريخ:** 2026-06-22 · **الأولوية:** P0  
> **السياق:** كلود متوقف حتى **01:00** — Cursor يتولى التنسيق المباشر معك حتى عودته.

---

## شكراً على البداية

راجعت الفهرس — أضفت **4 صفوف** بـ `visual_director: pending` ✅  
الـ alt جيد. **لكن:** مجلد `assets/images/approved/` ما زال **فارغاً** (لا ملفات WebP بعد).

**قاعدة النظام:** الصف في الفهرس + الملف على القرص + `approved` = Cursor يبني الصفحة.  
`pending` بدون ملف = **لا بناء**.

---

## مهمتك الآن (الساعتان القادمتان)

### الهدف الواقعي
**أكمل الـ4 المعلّقة** — أو **6 صور** إن استطعت — من Track A LIVE.

### التسليم (خطوة بخطوة)

1. **ولّد/اختر** الصورة (Ideogram · Pexels · Pixabay) — البرومبتات جاهزة في:
   - تجريبي (صورتان): `صور/اقرأني-جدول-الصور-تجريبي.md`
   - كامل (49): `operating-system/reports/ghost/omar-image-table.md`

2. **احفظ WebP 1200×750** مباشرة هنا (المسار الرسمي):
   ```
   assets/images/approved/hero-<article_slug>.webp
   ```
   > بديل مؤقت: ضعها في `صور/` بنفس الاسم — Cursor ينقلها تلقائياً عند `git push`.

3. **حدّث الفهرس** `assets/images/image-manifest.json`:
   - غيّر `"visual_director": "pending"` → **`"approved"`**
   - تأكد أن `image` يطابق المسار الفعلي
   - **لا em-dash** في alt

4. **أخبر Cursor** (رد هنا أو رسالة لجوست): «تمّت الدفعة X» — سأشغّل TECH_BUILD فوراً.

---

## دفعتك الأولى — الـ4 المعلّقة (أكملها أولاً)

| # | article_slug | الملف المطلوب | الحالة |
|---|--------------|---------------|--------|
| 1 | `family-budget-plan` | `hero-family-budget-plan.webp` | 🟡 pending · **بلا ملف** |
| 2 | `bmi-calculator-women` | `hero-bmi-calculator-women.webp` | 🟡 pending · **بلا ملف** |
| 3 | `daily-adhkar-family-guide` | `hero-daily-adhkar-family-guide.webp` | 🟡 pending · **بلا ملف** |
| 4 | `children-sleep-summer` | `hero-children-sleep-summer.webp` | 🟡 pending · **بلا ملف** |

---

## إن أنهيت الـ4 — التالي مباشرة (P0 LIVE)

| # | article_slug | ملف |
|---|--------------|-----|
| 5 | `investment-basics-beginners` | `hero-investment-basics-beginners.webp` |
| 6 | `rent-vs-buy-gulf-family` | `hero-rent-vs-buy-gulf-family.webp` |

(بقية الـ16 في `omar-image-production.md`)

---

## معايير الإجازة (أنت المدير البصري)

| ✅ يمرّ | ❌ يرفض |
|--------|--------|
| still-life أو مشهد محتشم | خنزير / حصالة خنزير / كحول / قمار |
| حجاب ساتر كامل إن وُجدت امرأة | عُري جزئي · أوضاع إيحائية |
| ألوان D4L: #054241 · #6abfb8 · #FAF8F4 | stock مكرّر عام |
| WebP ≤150KB مفضّل | نص محروق · watermark |

---

## ماذا يفعل Cursor بعد موافقتك

```
لكل slug بحالة approved + ملف موجود:
  → TECH_BUILD (ع/إن إن وُجد)
  → G5 من الفهرس
  → تقرير 👑 جوست + push
```

**لا تلمس HTML** — دورك: صورة + alt + فهرس فقط.

---

## مراجع سريعة

| ملف | الغرض |
|-----|--------|
| `omar-image-production.md` | قائمة 49 slug |
| `ghost/omar-image-table.md` | برومبتات كاملة |
| `scripts/list-image-pending.py` | حالة الفهرس الحية |
| `scripts/image_manifest.py` | قواعد المستهلك |

---

**الموعد المستهدف:** أول **4 approved + ملفات** قبل عودة كلود (01:00) إن أمكن.  
**Cursor في الانتظار** — أول دفعة = أول بناء.

— Cursor · Image Module · 2026-06-22
