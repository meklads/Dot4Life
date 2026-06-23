# 🧭 لوحة الفريق — Team Kanban

> **الملف الواحد للجميع** — مثل Trello لكن في المستودع.  
> **يُحدّث:** تلقائياً كل **15 دقيقة** (ساعة + دقيقة) + يدوياً عند نقل التذاكر  
> **يُؤرشف:** كل اثنين → `team-board-archive-YYYY-Www.md`

**الأسبوع:** 2026-W25 (٢٠–٢٦ يونيو)

| العضو | الدور | صندوقه السريع |
|-------|------|----------------|
| 👑 جوست | قرار · مراجعة بعد النشر | [`inbox/ghost.md`](inbox/ghost.md) |
| 🎨 عمر | برومبت · اعتماد بصري · الفهرس | [`inbox/omar.md`](inbox/omar.md) |
| 🤖 كلود | توليد Higgsfield | [`inbox/claude.md`](inbox/claude.md) |
| ✍️ Hema | كتابة · DEEPEN · مسودات | [`inbox/hema.md`](inbox/hema.md) |
| 🛡️ عامر | BUILD VERIFY · جودة | [`inbox/amer.md`](inbox/amer.md) |
| ⚙️ Cursor | بناء · أوتوبايلوت · push | [`inbox/cursor.md`](inbox/cursor.md) |

**🔀 تسليم يدوي (Trello لجوست):** [`handoff-board.md`](handoff-board.md) ← انقل البطاقات · أوامر جاهزة

---

<!-- TEAM-BOARD-LIVE-START -->
## 🕐 الحالة الآن — محدّث تلقائياً

**آخر تحديث:** 2026-06-23 **16:18** · مصدر: autopilot + manifest + git

> **اقرأ هنا أولاً** — ثلاث حالات: **✅ تم** · **🔄 جاري** · **⏳ لسه**

| المقياس | القيمة |
|---------|--------|
| صور `approved` | **12** |
| تنتظر بناء HTML | **0** |
| DEEPEN (قصير) | **174** |
| جودة الموقع | **0/271 (0%)** |
| آخر autopilot | `2026-06-23 **16:18**` |

### ✅ تم — آخر ما اكتمل

| الوقت | ماذا | من | الدليل |
|-------|------|-----|--------|
| 2026-06-23 **16:18** | فحص autopilot — كل الصور المعتمدة على الموقع | Cursor | log `[]` |
| 2026-06-23 **16:18** | built 0 slug(s) · ada54db · AUDIT PASS | Cursor | autopilot |
| 2026-06-23 **16:18** | رفع GitHub `ada54db` | Cursor | origin/main |

### 🔄 جاري العمل — الآن

| الوقت | ماذا | من | التالي |
|-------|------|-----|--------|
| — | A-09 REVISE — `drafts/task09/` | Hema | تسليم لعامر بعد draft-gate |
| 2026-06-23 **16:18** | BUILD VERIFY — **12** صور LIVE | عامر | hero + alt + G5 |

### ⏳ لسه — منتظر / مفتوح

| من | ماذا | ملاحظة |
|-----|------|--------|
| عمر + كلود | صور Tier 1 دفعة 2 — **0** slug بلا اعتماد | منذ ٢٢ يونيو |
| Hema | DEEPEN — **174** صفحة قصيرة | `hema-deepen-priority.md` |
| Cursor | وضع النشر المستمر | بانتظار «فعّل» من جوست |

### 📎 آخر سطور الأوتوبايلوت

- `[2026-06-23T16:18:26] === تشغيل جديد / new run ===`
- `[2026-06-23T16:18:27] slugs needing build: []`
- `[2026-06-23T16:18:28] AUDIT PASS`
- `[2026-06-23T16:18:34] git: pushed ada54db`
- `[2026-06-23T16:18:34] inboxes: operating-system/inbox/omar.md, operating-system/inbox/claude.md, operating-system/inbox/hema.md, operating-system/inbox/amer.md, operating-system/inbox/cursor.md, operating-system/inbox/ghost.md`

<!-- TEAM-BOARD-LIVE-END -->
---

## 1 · 📋 تذاكر — مفتوح (يدوي)

| # | المهمة | المالك | الهدف | منذ |
|---|--------|--------|-------|-----|
| T-01 | صور Tier 1 — دفعة 2 | عمر + كلود | 10–15 `approved` في الفهرس + WebP | ٢٢ يونيو |
| T-02 | A-09 — إنهاء REVISE | Hema → عامر → Cursor | مسودة PASS → TECH_BUILD → LIVE | ٢١ يونيو |
| T-03 | DEEPEN — أولوية 25 | Hema | رفع جودة 35% → 60% | ٢٢ يونيو |
| T-04 | BUILD VERIFY — 6 صور منشورة | عامر | hero + alt + G5 | ٢٢ يونيو |
| T-05 | وضع النشر المستمر | Cursor | `draft-gate` PASS → build + push تلقائي | بانتظار «فعّل» |
| T-06 | مراجعة جوست — ما نُشر هذا الأسبوع | جوست | قراءة العمود 2 + التقارير (لا توقف) | مستمر |

---

## 2 · ✅ منجز — انتهى + الدليل

| # | المهمة | المالك | الدليل | متى |
|---|--------|--------|--------|-----|
| T-D01 | Image Module P0 | Cursor + عمر | `ghost/2026-06-22-image-module.md` · `3252bb1` | ٢٢ يونيو |
| T-D02 | 6 صور → 12 صفحة HTML | Cursor (autopilot) | `ce99ade` · log `[]` | ٢٢ يونيو |
| T-D03 | Autopilot + inboxes + cron | Cursor | `ec19c57` · `gsystem-autopilot.log` | ٢٢ يونيو |
| T-D04 | Blog triage 43/58 | Amer → Cursor | `ghost/2026-06-22.md` · `bc4a512` | ٢٢ يونيو |
| T-D05 | guides 10/10 | Cursor | `ghost/2026-06-22.md` | ٢٢ يونيو |
| T-D06 | 29 LIVE AUDIT PASS | Cursor + عامر | autopilot · `--audit` | ٢٢ يونيو |
| T-D07 | تفعيل حلقة Higgsfield | جوست + عمر + كلود | Track E · charter | ٢٢ يونيو |

---

## 3 · 💬 ملاحظات — أي عضو

> اكتب هنا (أو في الشات). Cursor يحوّلها تذكرة `T-xx` في العمود 1.

| التاريخ | من | الملاحظة | الحالة |
|---------|-----|----------|--------|
| ٢١ يونيو | جوست | GSystem فقط — Kanban قديم مجمّد | ✅ |
| ٢٢ يونيو | جوست | publish-first — لا توقف لكل نشر | ✅ autopilot |
| ٢٢ يونيو | جوست | لوحة Kanban للفريق (مو بس جوست) | ✅ هذا الملف |
| — | — | *(ملاحظة جديدة)* | مفتوح |

---

## 4 · 📊 تقارير — روابط (قراءة فقط)

### تقارير جوست (ملخص يومي)
| التاريخ | الملف | خلاصة |
|---------|-------|--------|
| ٢٢ يونيو | [`ghost/2026-06-22.md`](reports/ghost/2026-06-22.md) | triage · جودة 35% |
| ٢٢ يونيو | [`ghost/2026-06-22-image-module.md`](reports/ghost/2026-06-22-image-module.md) | Image Module |
| ٢٢ يونيو | [`ghost/images-2026-06-22-track-e.md`](reports/ghost/images-2026-06-22-track-e.md) | Track E |
| ٢١ يونيو | [`ghost/2026-06-21.md`](reports/ghost/2026-06-21.md) | يومي |

### تقارير تشغيل (حسب المسار)
| المسار | الملف | المالك |
|--------|-------|--------|
| اللوحة التقنية | [`track-board.md`](reports/track-board.md) | عامر |
| جاهز للبناء | [`ready-to-build.md`](reports/ready-to-build.md) | عامر |
| صور عمر | [`omar-image-production.md`](reports/omar-image-production.md) | عمر |
| DEEPEN | [`hema-deepen-priority.md`](reports/hema-deepen-priority.md) | Hema |
| أوتوبايلوت | [`../outputs/logs/gsystem-autopilot.log`](../outputs/logs/gsystem-autopilot.log) | Cursor |

---

## قواعد (للجميع)

1. **افتح الملف → اقرأ «الحالة الآن»** — ✅ تم · 🔄 جاري · ⏳ لسه (محدّث بالساعة والدقيقة).
2. **الأقسام 1–2** = تذاكر يدوية طويلة المدى (Cursor ينقلها عند الإنجاز).
3. **صندوق الوارد** (`inbox/*.md`) = ملخص شخصي — يُحدَّث كل 15 دقيقة.
4. **كل اثنين** — قسم «منجز» يُؤرشف ويبدأ فارغاً.
5. **تذكرة جديدة** — ملاحظة في القسم 3 أو رسالة في الشات.
