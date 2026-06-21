# 🅲 Track C — استرداد أدسنس التقني (حالة + أدلة)
> المالك المنفّذ: الفريق التقني/عامر. عامر يتحقّق بالدليل. تاريخ: 2026-06-21.

| ID | المهمة | الحالة | الدليل |
|----|--------|--------|--------|
| C-F1 | إزالة أدسنس من صفحات التحويل/الفارغة | ✅ **DONE — BUILD VERIFIED (عامر)** | 51 ملف. before: `adsbygoogle.js?client=ca-pub-1436107577087160` موجود في كل ستب. after: `grep -c adsbygoogle` = **0** في الـ51. نسخة احتياطية: `outputs/backups/adsense-stubs-20260621-092539/` (51 ملف). تحقّق عامر: `grep -rl 'http-equiv="refresh"' --include=*.html \| xargs grep -l adsbygoogle` = **0**. |
| C-F4 | إزالة الشرطات الطويلة site-wide | ✅ **DONE** | 1186 شرطة من 189 ملف. تحقّق: `grep -rl '—' (كل أقسام المقالات)` = **0 ملف**. نسخة احتياطية: `outputs/backups/emdash-*`. |
| C-F2 | حسم صفحات hub/doorway المكرّرة | ✅ DONE — BUILD VERIFIED (Cursor) | 21 hub → redirect stubs؛ 111 رابط داخلي؛ `C-F2-redirect-map.md` |
| C-F3 | Schema Article+FAQPage على كل المقالات | 🟡 **PARTIAL** | 31 صفحة archive (FAQPage→Article). blog 165 متبقّي — `inject-article-schema.py` |
| C-F5 | Title ≤60 / Meta ≤155 / hreflang | ✅ **DONE** | **133 ملف** — `fix-seo-meta.py` · Title issues = **0** |
| C-F6 | صورة WebP + alt لكل مقال | 🟡 **PARTIAL** | **78** og:image fallback (`d4l1.webp`) — WebP heroes لاحقاً |
| C-F7 | تنظيف الجذر (نسخ احتياطية، privacy مكرّر، sec1-6) | ✅ **DONE** | ads removed من 9 stubs · `index-backup` → `outputs/backups/root-cleanup-20260622/` |

## خطة C-F2 — حسم صفحات hub/doorway (spec لـCursor)
14 صفحة (7 مواضيع × ar/en) بنمط `complete-*` توحي بـdoorway. القرار لكل مجموعة:

| صفحة hub (ar+en) | القرار | السبب |
|------------------|--------|-------|
| complete-family-financial-planning | **301 → finance.html** | مكرّر لقسم المالية الحقيقي |
| complete-gulf-family-financial-life-hub | **301 → finance.html** | doorway مالي مكرّر |
| complete-household-budget-system | **301 → blog/family-budget أو finance** | يتداخل مع ميزانية الأسرة (A-01) |
| complete-gulf-family-health-wellness | **301 → health.html** | doorway صحي |
| complete-family-systems-productivity-hub | **301 → productivity.html** | doorway إنتاجية |
| complete-family-travel-activities-hub | **301 → travel.html** | doorway سفر |
| complete-islamic-lifestyle-guide | **301 → islamic.html** | doorway إسلامي |

**التنفيذ (Cursor):** تحويل 301 دائم لكل hub إلى صفحة القسم الحقيقية، حذف السكربت الإعلاني إن بقي، وإزالة الروابط الداخلية المؤدية للـhub. **إن كان لأي hub قيمة فهرسية فعلية (روابط واردة)، يُحوَّل لا يُحذف.** proof المطلوب: خريطة التحويل المنفَّذة + `curl -I` تُظهر 301.
**ETA الخطة (عامر): جاهزة الآن.** ETA التنفيذ: على Cursor (مقترح: ضمن نفس أسبوع طابور البناء).

## بوابة إعادة طلب أدسنس (ممنوعة حتى):
1. موافقة جوست صراحةً، **و**
2. C-F1 ✅ + C-F2 ⏳ منجزتان، **و**
3. ≥60% من المقالات تمرّ فحص الجودة.
**الحالة الآن: غير جاهز لإعادة AdSense** — C-F1/C-F2/C-F4/C-F5/C-F7 ✅؛ C-F3/C-F6 🟡 جزئي؛ جودة أرشيف **21%** (58/271).
