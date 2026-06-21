# GSystem Charter — Ghost Closed Loop OS (Dot4Life v1)
> **Named:** GSystem · **UI:** `system/board.html` → GSystem · **Source of truth:** `operating-system/reports/`
> **Owner:** Ghost · **Commander:** Amer · **Writer:** Hema · **Build + Charter:** Cursor

## Ghost → Cursor (قاعدة عليا)
**Ghost يتكلم. Cursor يترجم.**

| Ghost | Cursor |
|-------|--------|
| توجيهات، قرارات، تغييرات سياسة — **بالكلام** | يحوّلها إلى **كود + لوحة + ميثاق + تقرير** |
| لا يكتب ملفات تشغيل ولا يوقف الحلقة | المصدر الوحيد للتنفيذ: `operating-system/` + `system/` + السكربتات |

- كل توجيه Ghost **يُسجَّل** في `gsystem-charter.md` أو التقارير — **هذا ما يتبعه الفريق** (عامر، هيما، Cursor).
- الكلام في الشات ≠ حوكمة — **الملف المحدَّث = الحقيقة**.
- Cursor يُبلّغ Ghost في **👑 جوست** بما طُبِّق من توجيهاته.

## Principle
**One deep article worth publishing > ten thin pages.** Text APPROVED ≠ LIVE.

## Loop (mandatory)
```
Hema drafts → Self-QA → Amer APPROVED|REVISE|REJECT
→ Cursor TECH_BUILD → Amer BUILD VERIFIED → LIVE (Amer + Cursor، 4–6/wk) → CLOSED
→ Ghost post-review (إعلام — لا يوقف الحلقة)
```

## LIVE gate (2026-06-21 — Ghost directive)
**Ghost ليس طرفاً في اعتماد النشر.** يثق بـ Amer + Cursor.
| خطوة | من | شرط |
|------|-----|-----|
| BUILD VERIFIED | **Amer** | بوابات المحتوى/SEO (Title، FAQ، إخلاء، C-F4…) |
| LIVE + deploy | **Cursor** | BUILD VERIFIED + gates تقنية + git push |
| Post-review | **Ghost** | بعد النشر — FLAG / PULL / ملاحظة؛ **لا يجمّد الطابور** |

**تقرير Ghost اليومي:** `operating-system/reports/ghost/` — لوحة الفريق → **👑 جوست**.  
**المالك: Cursor** (يكتب ويحدّث `manifest.json` نهاية كل يوم).

## ملاحظات عامر — إلزامية (Ghost directive 2026-06-21)
**كل ملاحظة من عامر** (REOPEN، REVISE، توصية، BLOCKED…) **لا تُترك بلا رد.**

| قرار Cursor | متى | في التقرير |
|-------------|-----|------------|
| **✅ مقبولة** | نُفّذ الإصلاح أو وُافقنا على التوصية | ماذا فعلنا |
| **❌ مرفوضة** | لا نتفق — مع **سبب واضح** | لماذا + البديل المقترح |

- يُسجَّل في قسم **«ملاحظات عامر — قرار Cursor»** في تقرير 👑 جوست **نفس اليوم**.
- لا LIVE على عنصر فيه ملاحظة عامر **مفتوحة** (بلا قبول أو رفض موثّق).
- عامر يعطي **GO للنشر** بعد BUILD VERIFIED؛ Cursor ينفّذ push.

## Ghost away mode (2026-06-21)
عندما يقول Ghost **«انشر»** أو يعلن غياباً مع تفويض التنفيذ:
- Cursor **ينفّذ LIVE فوراً** (commit + push + تحديث اللوحات + articles.json + sitemap).
- **يُبلّغ Ghost** في تقرير 👑 جوست **نفس اليوم** — **لا ينتظر موافقة Ghost**.
- Ghost يراجع **بعد** النشر فقط (post-review).

**استثناء واحد:** Ghost **FULL STOP** (🔴 PAUSED) — طوارئ فقط، يوقف كل شيء.

## One system (Ghost directive 2026-06-21)
**GSystem = المصدر الوحيد للتشغيل.** Kanban (`tasks.json`) **⏸ مُجمّد.**

| | |
|---|---|
| **اللوحة** | `system/board.html` → **GSystem** (افتراضي) + **👑 Ghost** |
| **الحقيقة** | `operating-system/reports/*.md` |
| **أرشيف Kanban** | `system/tasks-archive-2026-06-21.json` — قراءة فقط |
| **إشعار الفريق** | `operating-system/reports/kanban-frozen.md` |

أقسام اللوحة (أفكار، Ideogram، حوكمة بصرية…) **مرجعية** — لا حالة LIVE للمقالات.

**Rule:** LIVE state **فقط** في GSystem / `ready-to-build.md`.

## Build gates (Cursor — fail build if missing)
- Title ≤60 chars (full `<title>`, no mid-word chop)
- Meta ≤155 · C-F4 em-dash = 0
- Article + FAQPage JSON-LD · hreflang ar/en
- WebP hero + alt + og:image · 3 internal links
- Financial / Sharia / medical disclaimer when required (AR + EN)
- **Image report** في `operating-system/reports/ghost/` (`images-YYYY-MM-DD.md`)

## Image loop (Ghost directive 2026-06-21)
| خطوة | من | ماذا |
|------|-----|------|
| اختيار | **Cursor** | Pexels / Unsplash / Pixabay — معايير D4L (still-life، احتشام) |
| حفظ | **Cursor** | `assets/images/hero-<slug>.webp` |
| تقرير | **Cursor** | `reports/ghost/images-YYYY-MM-DD.md` — جدول: **اسم المقالة · برومبت صورتين · تاريخ · اسم/مسار الملف** |
| مراجعة | **Ghost** | نهاية الأسبوع — ما لا يعجبك |
| استبدال | **Ghost** | Ideogram من البرومبت → **نفس اسم الملف** في `assets/images/` |

- **لا توقف الحلقة** بانتظار موافقة Ghost على الصور — تُراجع لاحقاً.
- عمر/Ideogram Kanban: اختياري؛ المصدر الأساسي = تقرير Cursor + استبدال Ghost.


## Modes
| Mode | When | APPROVED | LIVE |
|------|------|----------|------|
| 🟢 GREEN | Amer present | Amer | **Amer + Cursor** |
| 🟡 YELLOW | Amer absent ≤72h | Frozen | Frozen |
| 🔴 PAUSED | Ghost FULL STOP (طوارئ) | — | — |

## Tracks
- **A** New/deepen articles · **B** Thin Live top 20 · **C** AdSense technical

## v2 (after first CLOSED loop)
- WIP=1 TECH_BUILD · proof bundle per item · Kanban links to A-xx IDs
