# 🧭 اللوحة الموحّدة — Dot4Life Closed-Loop (المصدر الوحيد للحقيقة)
> يديرها عامر (Commander). **🟢 GREEN MODE** — Amer ACK HANDOFF 2026-06-21. See `yellow-mode-active.md`.
> **⏸ Kanban مُجمّد (2026-06-21)** — GSystem = المصدر الوحيد. See `kanban-frozen.md`.
> الحوكمة: `manager-charter-adsense.md` + MASTER ORDER. تاريخ: 2026-06-21.
> الحالات: QUEUE → IN_PROGRESS → SELF_QA → AMER_REVIEW → TECH_BUILD → READY → LIVE → CLOSED
> المسارات النشطة (حد أقصى 3): **A** مقالات جديدة · **B** إصلاح Live الرفيع · **C** أدسنس التقني.

## Track A — مقالات جديدة (Ship يكتب، Amer يبوّب، Tech يبني)
| id | الموضوعان | owner | state | amer_review | proof |
|----|-----------|-------|-------|-------------|-------|
| A-01 | الاستثمار + ميزانية الأسرة | Cursor | **LIVE** 🟢 | BUILD VERIFIED | 4 pages LIVE 2026-06-21 |
| A-07 | إيجار vs تملّك + Oman ROI | Cursor | **LIVE** 🟢 | BUILD VERIFIED | rent-vs-buy×2 + oman inject |
| A-02 | المشي + BMI للنساء | Cursor | **LIVE** 🟢 | auto-gates ✅ | 3 pages |
| A-03 | الحمل أسبوعياً + نوم الأطفال | Cursor | **LIVE** 🟢 | auto-gates ✅ | 3 pages |
| A-04 | فحوصات قبل الحمل + أذكار | Cursor | **LIVE** 🟢 | auto-gates ✅ | 4 pages |
| A-05 | العمرة مع الأطفال + رأس السنة الهجرية | Cursor | **LIVE** 🟢 | auto-gates ✅ | 4 pages |
| A-06 | أسماء الله + الصلاة بالحب | Cursor | **LIVE** 🟢 | auto-gates ✅ | 4 pages |
| A-08 | تمويل جدة + عائد إيجار الرياض | Cursor | **LIVE** 🟢 | auto-gates ✅ | 4 pages (+2 EN new) |
| A-09 | تطوّع صيفي + مخيمات vs منزل | Cursor | **TECH_BUILD** | ✅ approved (بعد REVISE) | `drafts/task09/` |
| A-10…A-59 | — | Ship | QUEUE | hold (after A-09) | drafts/task10/ |

**الحالة:** **29 LIVE** · جودة أرشيف **35%** (95/271) · guides **100%** · blog triage **43/58 PASS** · A-09 REVISE عند Hema.

## Track B — Live الرفيع (الأولوية)
- قائمة أسوأ 20: `track-B-thin-live-top20.md` ✅ منشورة.
- إجمالي Live رفيع: 107. قرار: كلها DEEPEN (لا NOINDEX في الـ20).
- أقرب 4 للإغلاق: B-rentbuy(ع/إن)، B-investment(ع/إن) — نصوصها معتمدة (A-01/A-07) → تنتظر TECH_BUILD.

## Track C — أدسنس التقني
- التفاصيل والأدلة: `track-C-adsense-technical.md`.
- C-F1 ✅ · C-F2 ✅ · C-F4 ✅ · C-F5 ✅ · C-F7 ✅ · C-F3/C-F6 🟡 جزئي · جودة **34%** (92/271)

## Track D — حملة blog (2026-06-22)
| حارة | المالك | الحالة |
|------|--------|--------|
| `track-blog-triage.md` | **Amer** | ✅ Schema-only منفّذ |
| `scripts/draft-gate.py` | **Amer** | ✅ معتمد |
| HTML (Schema-only · 301) | **Cursor** | 🟢 **43/58 PASS** · 15→DEEPEN |

## Track E — Image Module (2026-06-22) 🟢 LIVE
| حارة | المالك | الحالة |
|------|--------|--------|
| `assets/images/approved/` + `image-manifest.json` | **عمر** | 🟢 **مُفعَّل** (جوست) |
| `scripts/image_manifest.py` + G5 fail-closed | **Cursor** | ✅ `3252bb1` |
| دفعة الإنتاج | **عمر** | 📋 `omar-image-production.md` (49 slug) |
| BUILD VERIFY | **Amer** | ينتظر أول دفعة معتمدة |

> قائمة حية: `python3 scripts/list-image-pending.py`

## بوابات حاكمة
- معتمد نصاً ≠ Live. التتبّع: `ready-to-build.md`.
- إعادة طلب أدسنس: ممنوعة (شرط جوست + C-F1/F2 + ≥60% جودة).
- Homepage v1 = FREEZE (لا تغيير بلا موافقة جوست).
- نشر: حد أقصى 4–6 Live/أسبوع — **Amer + Cursor** (Ghost post-review، لا توقف)
