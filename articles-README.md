# articles.json — دليل إضافة مقال جديد (لـ رواق)

## الخطوات

1. افتح `articles.json`
2. أضف مدخلاً جديداً بنفس تنسيق المدخلات الموجودة
3. اكتب المقال HTML في مجلد القسم المناسب
4. نفّذ `node scripts/build-sitemap.js` (يجدّد خريطة الموقع)
5. `git add articles.json sitemap-content.xml`
6. `git commit -m "new article: TITLE"`
7. `git push`

## الحقول المطلوبة

| الحقل | الشرح | مثال |
|-------|-------|------|
| `section` | القسم بالإنكليزية | `"comparisons"`, `"blog"`, `"guides"` |
| `section_ar` | القسم بالعربية | `"مقارنات"`, `"المدونة"` |
| `title_en` | العنوان بالإنكليزية | `"Saving vs Investing"` |
| `title_ar` | العنوان بالعربية | `"الادخار أم الاستثمار"` |
| `url` | رابط المقال (عربي) | `"/comparisons/saving.html"` |
| `url_en` | رابط المقال (إنجليزي) | `"/comparisons/saving-en.html"` |
| `date` | التاريخ بصيغة YYYY-MM-DD | `"2026-06-08"` |
| `img` | مسار الصورة | `"/assets/images/articles/saving.webp"` |
| `excerpt_en` | وصف قصير إنكليزي | `"A practical comparison..."` |
| `excerpt_ar` | وصف قصير عربي | `"مقارنة عملية..."` |
| `category` | التصنيف (يطابق صفحة القسم) | `"health"`, `"finance"`, `"real-estate"`, `"travel"`, `"islamic"`, `"family"` |

## أين يظهر المقال تلقائياً؟

- الصفحة الرئيسية (`index.html`) — ضمن "أحدث المقالات"
- صفحة القسم حسب `category` — ضمن "أحدث المقالات"
- المدونة (`blog.html`) — القائمة الكاملة
- الأرشيف (`archive.html`) — القائمة الكاملة مع العدد
- خريطة الموقع (`sitemap-content.xml`) — بعد تشغيل `build-sitemap.js`

## ملاحظات

- `url` هو رابط النسخة العربية، `url_en` رابط النسخة الإنجليزية
- الصورة يفضل 600×340 px
- لا حاجة لتعديل أي HTML يدوياً — feed.js يتولّى العرض تلقائياً
- مدة التخزين المؤقت 10 دقائق (localStorage)
