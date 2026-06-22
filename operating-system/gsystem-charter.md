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

## ⛔ قاعدة مثبتة — push فوري (Ghost directive، دائمة)
**أي تعديل على الريبو → `git push origin main` مباشرة — بدون طلب من Ghost.**

| | |
|---|---|
| **متى** | نهاية **كل** جلسة فيها تغيير ملف (UI، HTML، CSS، JS، reports، charter، صور…) |
| **من يطلب؟** | **لا أحد** — Ghost لا يقول «ارفع»؛ Cursor **يرفع تلقائياً** |
| **متى أقول «تم»؟** | **بعد** push فقط + **commit hash** في تقرير 👑 جوست |
| **استثناء** | Ghost **FULL STOP** 🔴 فقط |

> Ghost **لا يعمل redeploy يدوي** ظناً أن التحديث رُفع — Cursor مسؤول عن الرفع **دائماً**.

## Principle
**One deep article worth publishing > ten thin pages.** Text APPROVED ≠ LIVE.

## Loop (mandatory)
```
Hema drafts → Self-QA → Amer APPROVED|REVISE|REJECT
→ Cursor TECH_BUILD → Amer BUILD VERIFIED → LIVE (Amer + Cursor، 4–6/wk) → CLOSED
→ Ghost post-review (تقرير فقط — **لا يوقف الحلقة**)
```

## LIVE gate (2026-06-21 — Ghost directive)
**Ghost ليس طرفاً في اعتماد النشر.** يثق بـ Amer + Cursor.
| خطوة | من | شرط |
|------|-----|-----|
| BUILD VERIFIED | **Amer** | بوابات المحتوى/SEO (Title، FAQ، إخلاء، C-F4…) |
| LIVE + deploy | **Cursor** | BUILD VERIFIED + gates تقنية + git push |
| Post-review | **Ghost** | تقرير 👑 جوست — FLAG/PULL اختياري؛ **لا يجمّد الطابور** |

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

## Ghost away mode (2026-06-21) → **Autonomous loop**
**Ghost خارج الحلقة التشغيلية.** لا يوقف ولا ينتظر. يستلم **تقريراً فقط** في 👑 جوست.

| Ghost | النظام (Amer + Cursor + Hema) |
|-------|-------------------------------|
| توجيهات بالكلام (عند الحضور) | Cursor يترجم → ينفّذ **فوراً** |
| تقرير يومي للقراءة | الحلقة **لا تتوقف** بانتظاره |
| post-review اختياري | FLAG/PULL **لا يجمّد** الطابور |

**قواعد التشغيل التلقائي:**
- BUILD VERIFIED → gates السكربت + فحص عامر عند توفره؛ **لا انتظار Ghost**.
- READY → Cursor **push + LIVE** (articles.json + sitemap) **بدون موافقة Ghost**.
- Ghost «انشر» أو غياب = **تفويض كامل** — Cursor يكمل FIFO ويُبلّغ في التقرير.
- **استثناء واحد:** Ghost **FULL STOP** (🔴 PAUSED) — طوارئ فقط.

## Deploy rule — Ghost directive (إلزامي · **قاعدة مثبتة**)
**مرجع:** § «push فوري» أعلاه. **كل تغيير = commit + push في نفس الجلسة** — **لا انتظار طلب Ghost.**

| ❌ ممنوع | ✅ إلزامي |
|---------|---------|
| تعديل ملف وتركه uncommitted | **commit + `git push origin main` في نفس الجلسة** |
| قول «تم الإصلاح» بدون push | ذكر **commit hash** في تقرير 👑 جوست |
| انتظار موافقة Ghost للرفع | push مباشرة — Coolify يبني تلقائياً |

- **UI / board / charter / HTML / CSS / JS / reports** — الكل يُرفع.
- Ghost **لا يعمل redeploy يدوي** ظناً أن Cursor رفع — Cursor **يلتزم بالرفع دائماً**.

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
**حزمة G1–G11 + parity** في `scripts/build-from-approved-draft.py` — `assert_build_gates()` قبل كل write؛ `assert_parity()` للأزواج ع/إن.

| Gate | فحص |
|------|-----|
| G1 | em-dash = 0 |
| G2 | مسوّدة ≥1200 كلمة (نثر المسوّدة، لا القالب) |
| G3–G4 | Article + FAQPage ≥4Q |
| G5 | WebP hero + alt + og:image — **manifest `approved`** على TECH_BUILD؛ grandfather على `--audit` |
| G6 | Title ≤60 |
| G7 | Meta ≤155 (بعد decode) |
| G8 | hreflang (استثناء EN-only) |
| G9 | disclaimer حسب `disclaimer_type` |
| G10 | روابط داخلية ≥3 |
| G11 | JSON-LD valid |
| P1–P3 | parity ع/إن (schema, FAQ, disclaimer) |

**Audit LIVE:** `python3 scripts/build-from-approved-draft.py --audit` — لا rebuild إلا FAIL.

## Image loop (Ghost directive 2026-06-22 — **Image Module** + Higgsfield)
| خطوة | من | ماذا |
|------|-----|------|
| الاشتراك / الأداة | **جوست** | **Higgsfield** — توليد الصور |
| توليد + تنسيق | **كلود** | يشغّل Higgsfield · يدير الدفعات · يكلف عمر بالبرومبتات |
| البرومبتات | **عمر** | كتابة برومبت لكل مقال (احتشام/هوية/قسم) |
| إجازة بصرية + فهرس | **عمر** | `visual_director` · alt ع/إن · صف في `image-manifest.json` |
| استلام + نشر | **Cursor** | WebP → `assets/images/approved/` · `ingest-omar-images.py` · TECH_BUILD · hero في HTML |
| `visual_director` | **عمر** | `approved` \| `rejected` \| `pending` — فقط approved يُبنى |
| G5 fail-closed | **Cursor** | `scripts/image_manifest.py` — لا صورة معتمدة = `BLOCKED_IMAGE` |
| BUILD VERIFY | **Amer** | صفحة مكتملة = صورة معتمدة من الفهرس |

**تقسيم الحارات (لا تداخل):**
- **كلود** = توليد (Higgsfield) · **عمر** = برومبت + إجازة · **Cursor** = استلام + بناء HTML فقط · **لا يختار Cursor صوراً**

- **لا صورة معتمدة = لا TECH_BUILD جديد** (`BLOCKED_IMAGE`).
- المصدر الرسمي = **`image-manifest.json`** + `assets/images/approved/`.

## GSystem Autopilot (2026-06-22 — إلزامي)

**`approved` في الفهرس = أمر بناء. ممنوع انتظار موافقة جوست أو «ابنِ».**

| مكوّن | الوظيفة |
|--------|---------|
| `scripts/gsystem_autopilot.py` | يفحص الفهرس → يبني → `--push` |
| `scripts/gsystem_notify.py` | صناديق `operating-system/inbox/*.md` |
| `.github/workflows/gsystem-autopilot.yml` | CI كل 30 دقيقة + عند push الفهرس |
| `install-gsystem-autopilot-cron.sh` | Mac كل 15 دقيقة |

راجع `operating-system/gsystem-autopilot.md`.


## Modes
| Mode | When | APPROVED | LIVE |
|------|------|----------|------|
| 🟢 GREEN | Amer present | Amer | **Amer + Cursor** |
| 🟡 YELLOW | Amer absent ≤72h | Frozen | Frozen |
| 🔴 PAUSED | Ghost FULL STOP (طوارئ) | — | — |

## Tracks
- **A** New/deepen articles · **B** Thin Live top 20 · **C** AdSense technical
- **Blog campaign (2026-06-22):** Amer = `track-blog-triage.md` + `draft-gate.py` (Markdown only). Cursor = HTML execute **after** triage list approved. **No overlap.**

## v2 (after first CLOSED loop)
- WIP=1 TECH_BUILD · proof bundle per item · Kanban links to A-xx IDs
