# 📋 تعليمات العمل اليومية — لمانوس (Manus)

## ⏰ الموعد النهائي: كل يوم الساعة ٩:٠٠ صباحاً

يجب أن تكون جميع مقالات اليوم جاهزة وروابطها موضوعة في `review.html` قبل الساعة ٩ صباحاً.

---

## 🎯 مهامك اليومية

### يومياً (الأحد ← الخميس): ٣ مقالات
| القسم | المقالات |
|-------|:--------:|
| ١. قصص مميزة — Featured Stories | مقالة واحدة |
| ٢. مقارنات وقرارات — Comparisons | مقالة واحدة |
| ٣. السلام يبدأ من البيت — Peace Capsules | مقالة واحدة |

### الإثنين والخميس: ٣ مقالات إضافية
| القسم | المقالات |
|-------|:--------:|
| ٤. الصحة والعافية — Health & Wellness | مقالة واحدة |
| ٥. المالية والثروة — Finance & Wealth | مقالة واحدة |
| ٦. الإسلامية — Islamic | مقالة واحدة |

### يوم الجمعة والسبت: راحة ✌️
لا توجد مقالات جديدة — نُراجع وننشر ما تبقى.

---

## 🔄 خطوات العمل (بالترتيب)

### الخطوة ١: افتح لوحة المراجعة
```
https://dotforlife.com/review.html
```
انظر أي المقالات المطلوبة اليوم.

### الخطوة ٢: اقرأ تفاصيل المقال
افتح صفحة القسم المناسبة:
- `https://dotforlife.com/sec1.html` — قصص مميزة
- `https://dotforlife.com/sec2.html` — مقارنات
- `https://dotforlife.com/sec3.html` — سلام
- `https://dotforlife.com/sec4.html` — صحة
- `https://dotforlife.com/sec5.html` — مالية
- `https://dotforlife.com/sec6.html` — إسلامية

في كل صفحة تجد:
- 📊 جدول بفكرة المقالة، الشخصية، الزاوية، الكلمات المفتاحية
- ✍️ إرشادات خاصة بكتابة هذا النوع من المحتوى
- 🏷️ الـ Meta Data المطلوبة

### الخطوة ٣: صمم صفحة HTML كاملة
لكل مقالة، صمم **ملفين HTML**:

| الملف | المحتوى | مثال |
|-------|---------|------|
| `اسم-المقالة.html` | النسخة العربية | `arab-mother-startup.html` |
| `اسم-المقالة-en.html` | النسخة الإنجليزية | `arab-mother-startup-en.html` |

**ملاحظات مهمة:**
- ✅ الملفان مستقلان تماماً — لا تخلط العربية والإنجليزية في نفس الملف
- ✅ استخدم قالب الموقع (انظر النموذج أدناه)
- ✅ الصور من Unsplash — اختر صوراً دافئة تناسب العائلة الخليجية
- ✅ روابط داخلية لأدوات دوت فور لايف (حاسبة BMI، حاسبة الزكاة، حاسبة الرهن)
- ✅ كل ملف يحتوي على Meta tags منفصلة

### الخطوة ٤: احفظ الملفات
ضع الملفات في المجلد المؤقت:
```
assets/queue/
```

### الخطوة ٥: ضع الروابط في review.html
افتح `review.html` وابحث عن القسم المناسب، ثم أضف روابط المقالات بهذا التنسيق:

```html
<a href="assets/queue/arab-mother-startup.html" target="_blank">🇸🇦 العربية ←</a>
<a href="assets/queue/arab-mother-startup-en.html" target="_blank">🇬🇧 English ←</a>
```

---

## 📐 قالب HTML النهائي (يجب اتباعه)

### ١. هيكل الرأس (Head)

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl" data-theme="light" data-lang="ar">
<head>
<script>(function(){var t=localStorage.getItem("dfl-theme")||"light",h=document.documentElement;h.setAttribute("data-theme",t);})()</script>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>عنوان SEO ≤60 حرف</title>
<meta name="description" content="وصف SEO ≤160 حرف"/>
<meta property="og:title" content="..."/>
<meta property="og:description" content="..."/>
<link rel="canonical" href="https://dotforlife.com/المسار/اسم-الملف.html"/>
<link rel="alternate" hreflang="en" href="https://dotforlife.com/المسار/اسم-الملف-en.html"/>
<link rel="alternate" hreflang="ar" href="https://dotforlife.com/المسار/اسم-الملف.html"/>
<link rel="stylesheet" href="/styles/main.css?v=01c8e28"/>
<link rel="stylesheet" href="/styles/pages/articles.css?v=01c8e28"/>
<!-- Schema.org -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "...",
  "description": "...",
  "author": {"@type": "Organization", "name": "DotForLife"},
  "inLanguage": "ar"
}
</script>
</head>
```

### ٢. هيكل الجسم (Body)

```html
<body class="index-page category-page">
  <!-- NAVBAR (منسوخة من أي صفحة موجودة) -->
  <nav id="navbar">...</nav>

  <!-- HERO SECTION -->
  <section id="hero">
    <h1>عنوان المقال</h1>
    <div class="hero-meta">القسم · تاريخ النشر · وقت القراءة</div>
  </section>

  <!-- CONTENT -->
  <article class="article-body">
    <!-- المحتوى هنا -->
    <p>...</p>
    <h2>...</h2>
    <p>...</p>
    <!-- إلخ -->
  </article>

  <!-- المصداقية -->
  <div class="article-credibility">
    <p>✍️ كتب بواسطة فريق دوت فور لايف — مراجعة وتدقيق لغوي</p>
  </div>

  <!-- CTA -->
  <div class="article-cta">
    <a href="/blog.html">📚 اكتشف المزيد من المقالات</a>
  </div>

  <!-- التبديل بين اللغات -->
  <div class="article-nav">
    <a href="اسم-الملف-en.html">🌐 قراءة بالإنجليزية</a>
  </div>

  <!-- FOOTER -->
  <footer class="site-footer">...</footer>

  <!-- MOBILE NAV -->
  <nav class="dfl-mobile-nav">...</nav>

  <!-- SCRIPTS -->
  <script src="/scripts/global.js" defer></script>
</body>
```

---

## ✅ قائمة التأكد — لكل مقالة

قبل وضع الرابط، تأكد من:

- [ ] **ملفين** منفصلين: عربي + إنجليزي
- [ ] اللغة مضبوطة: `lang="ar" dir="rtl"` للعربي، `lang="en" dir="ltr"` للإنجليزي
- [ ] عنوان SEO ≤ 60 حرفاً
- [ ] وصف SEO ≤ 160 حرفاً
- [ ] الكلمة المفتاحية موجودة في: أول 100 كلمة + H2 واحد + آخر 100 كلمة
- [ ] 3-4 عناوين فرعية H2 داخل المقال
- [ ] صورة من Unsplash مع alt text وصفي
- [ ] رابط داخلي واحد على الأقل لأداة من أدوات الموقع
- [ ] رابط `hreflang` يشير إلى النسخة الأخرى
- [ ] رابط التبديل بين اللغات في `article-nav`
- [ ] الكود خالٍ من أخطاء HTML (يفضل التحقق بـ validator)
- [ ] الصور مضغوطة ولا تتجاوز 200KB

---

## 🏷️ الـ Meta Data Summary

| العنصر | عربي | إنجليزي |
|--------|:----:|:-------:|
| عنوان SEO | ≤60 حرف | ≤60 حرف |
| وصف SEO | ≤160 حرف | ≤160 حرف |
| كلمات مفتاحية | 5 كلمات | 5 كلمات |
| رابط hreflang | → النسخة الإنجليزية | → النسخة العربية |

---

## 🚀 مثال عن روابط في review.html

عند الانتهاء من مقالة، ضع الرابط بهذا الشكل:

```
<a href="assets/queue/arab-mother-startup.html" target="_blank">🇸🇦 أم عربية بنت شركة ناشئة من مطبخها</a>
<a href="assets/queue/arab-mother-startup-en.html" target="_blank">🇬🇧 Arab Mother Built a Startup from Her Kitchen</a>
```

---

## ⚠️ أخطاء شائعة — تجنبها

| ❌ خطأ | ✅ صح |
|--------|------|
| وضع عربي + إنجليزي في نفس الملف | ملفين منفصلين |
| كتابة HTML مباشر في review.html | فقط رابط (a href) |
| نسيان hreflang | أضف `link rel="alternate"` |
| صور كبيرة (أكثر من 300KB) | ضغط الصور أقل من 200KB |
| عدم إضافة Meta description | أضف وصفاً ≤160 حرفاً |
| استخدام "في هذا المقال" | ابدأ مباشرة بالقصة أو المعلومة |

---

**🎯 الهدف:** ٣ مقالات يومياً (الأحد-الخميس) + ٣ إضافية (الإثنين والخميس) = ٢١ مقالة في الأسبوع
**⏰ الموعد النهائي:** كل يوم الساعة ٩:٠٠ صباحاً
**📍 مكان التسليم:** `review.html` — تحت القسم المناسب
