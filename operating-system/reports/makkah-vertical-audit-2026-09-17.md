# Makkah Vertical — Content Audit (Phase 0) · 2026-09-17

> **استثناء جوست:** بناء `/makkah/` فقط · QUALITY-FIRST يبقى على بقية الموقع.  
> **قاعدة هذه المرحلة:** لا نقل ملفات · لا حذف · لا تغيير URL قائم. الـhub يربط للموجود.

## ملخص القرار
| الحكم | العدد | المعنى |
|--------|------:|--------|
| KEEP | 28 | يبقى في مكانه ويُربط من العمود |
| MERGE (منطقي لاحق) | 4 | توائم مكررة — لا تنقل الآن؛ فضّل الكانونيكال |
| REWRITE | 2 | noindex/ضعيف يحتاج إصلاح لاحقاً |
| REDIRECT | 2 | stubs «تم النقل» أصلاً |
| REMOVE | 0 | لا حذف في هذه المرحلة |
| OUT OF SCOPE | 8 | إسلاميات عامة (أذكار/أسماء الله…) ليست عن الحرمين |
| QUEUE ONLY | — | `assets/queue/*` ليست LIVE للنشر |

---

## KEEP — يُربط من `/makkah/` (URL ثابت)

| الصفحة | العمود |
|--------|--------|
| `islamic-hajj-umrah/makkah-medina-family-spiritual-guide(.html/-en)` | Plan / Move |
| `islamic-hajj-umrah/spiritual-preparation-umrah-family(.html/-en)` | Plan |
| `islamic-hajj-umrah/spiritual-benefits-umrah-families(.html/-en)` | Experience |
| `islamic-hajj-umrah/umrah-off-peak-seasons-guide(.html/-en)` | Plan |
| `islamic-hajj-umrah/umrah-with-kids(.html/-en)` | Guides |
| `islamic-hajj-umrah/umrah-with-elderly-parents(.html/-en)` | Guides |
| `islamic-hajj-umrah/hajj-first-timers-guide(.html/-en)` | Guides |
| `islamic-hajj-umrah/cave-of-hira-story(.html/-en)` | Experience |
| `blog/makkah-hotels-guide(.html/-en)` | Stay |
| `blog/medina-hotels-near-masjid-nabawi(.html/-en)` | Stay |
| `blog/hotel-near-haram-vs-budget-umrah(.html/-en)` | Stay |
| `blog/masjid-nabawi-complete-guide(.html/-en)` | Experience |
| `blog/umrah-budget-guide-families(.html/-en)` | Plan |
| `blog/umrah-packing-checklist-guide(.html/-en)` | Plan |
| `blog/umrah-visa-gulf-residents-guide(.html/-en)` | Plan |
| `blog/hajj-umrah-guide-2025(.html/-en)` | Guides |
| `guides/mecca-medina.html` | Experience |
| `tools/return-to-hotel.html` | Tools / Move (**مدمج الآن**) |
| `tools/qibla.html` | Tools / Move |
| `tools/prayer-times.html` | Tools (مساعد) |
| `tools/travel-budget.html` | Tools (مساعد) |
| `tools/packing-checklist.html` | Tools (مساعد) |

---

## MERGE (لاحق — لا تنفيذ نقل الآن)

| الزوج | التوصية |
|--------|---------|
| `blog/umrah-with-kids-guide*` ↔ `islamic-hajj-umrah/umrah-with-kids*` | أبقِ islamic كانونيكال · blog → 301 لاحقاً إن تأكد التكرار |
| `blog/pregnancy-and-umrah-guide.html` (noindex) ↔ `-en` | أصلح AR أو أبقِ EN فقط |

---

## REWRITE (لاحق داخل الجودة العامة)

| الصفحة | السبب |
|--------|--------|
| `blog/pregnancy-and-umrah-guide.html` | noindex |
| `islamic-hajj-umrah/hijri-new-year-children.html` | خارج نية الحرمين + تاريخ جودة |

---

## REDIRECT (موجود أصلاً كـstub)

| الصفحة | ملاحظة |
|--------|--------|
| `blog/hotel-near-haram-vs-budget-umrah-ar.html` | «تم النقل» |
| `blog/umrah-packing-checklist-guide-ar.html` | «تم النقل» |

---

## OUT OF SCOPE لهذا العمود (تبقى في إسلاميات)

- `daily-adhkar-family-guide*`
- `teaching-children-allah-names*`
- `teaching-children-prayer-with-love*`
- أي محتوى إيماني يومي بلا نية حج/عمرة/حرمين

---

## MOVE

**لا شيء في Phase 1.**  
أي MOVE لـ`/makkah/...` يحتاج موافقة ثانية بعد قياس الإعلان، مع 301 إلزامي.

---

## REMOVE

**صفر.**

---

## الهيكل المُنشأ (جديد فقط)

```
/makkah/                 Hub
/makkah/plan/
/makkah/stay/
/makkah/move/
/makkah/experience/
/makkah/tools/           ← Return to Hotel حي + 5 مخططات «قريباً»
/makkah/guides/
```

الأدوات الخمس **بدون منطق** (placeholders معمارية فقط) حسب أمر جوست.
