# 🏡 دوت فور لايف — DotForLife

> **"Your trusted daily life platform for families. One calm place for life's everyday decisions."**

---

## 📁 هيكل المشروع — Project Structure

```
Dot4Life/
├── .github/workflows/deploy.yml    ← GitHub Actions → ينشر من site/
├── .gitignore
├── README.md
│
├── site/                           ← 🎯 ALL published website files
│   ├── index.html                  ← الصفحة الرئيسية
│   ├── blog.html                   ← المدونة
│   ├── about.html, contact.html    ← صفحات تعريفية
│   ├── CNAME, robots.txt           ← تكوين الاستضافة
│   ├── sitemap.xml                 ← خريطة الموقع
│   │
│   ├── featured-stories/           ← قصص مميزة
│   ├── comparisons/                ← مقارنات وقرارات
│   ├── peace-capsules/             ← السلام يبدأ من البيت
│   ├── health-pregnancy/           ← الصحة والعافية
│   ├── finance-wealth/             ← المالية والثروة
│   ├── islamic-hajj-umrah/         ← الإسلامية
│   │
│   ├── tools/, guides/, blog/      ← الأدوات والأدلة
│   ├── assets/                     ← الصور والملفات
│   ├── styles/                     ← CSS
│   ├── scripts/                    ← JavaScript
│   │
│   └── system/                     ← 🔒 Internal workflow
│       ├── review.html             ← لوحة المراجعة
│       ├── sec1.html - sec6.html   ← صفحات الأقسام
│       ├── brand-guide.html        ← دليل العلامة التجارية
│       └── *.md                    ← خطط العمل
│
└── legacy/                         ← 🗑️ ملفات مرجعية سابقة
    ├── _docs/
    └── _manus-reference/
```

---

## 🧠 Skills — فريق المهارات المتخصصة

📍 الموقع: `/Users/ghousemac/Desktop/Turriva/skills/`

```
📁 skills/
└── Team Skills – Graphics House/
    ├── index.html
    ├── README.md
    ├── 01-omar-graphic-designer.md       ← 🎨 عمر — Graphic Designer
    ├── 02-amer-programmer.md             ← ⚙️ عامر — Web Developer
    ├── 03-moni-content-writer.md         ← ✍️ موني — Content Writer
    ├── 04-medo-seo-developer.md          ← 🔍 ميدو — SEO Developer
    ├── 05-hema-video-editor.md           ← 🎬 هيما — Video Editor
    ├── 06-samer-social-media-manager.md  ← 📊 سمير — Social Media Manager
    └── 07-claude-strategic-director.md   ← 🧠 كلود — Strategic Director
```

> كل سكيل هو خبير مستقل، جاهز للاستدعاء عند الطلب لأي مشروع.

---

## 🚀 النشر — Deployment

يتم النشر تلقائياً عبر GitHub Actions:
1. Push على فرع `main`
2. GitHub Actions ينفذ `peaceiris/actions-gh-pages`
3. ينشر محتويات `site/` إلى `gh-pages` branch
4. الموقع يصبح متاحاً على `https://dotforlife.com`

---

*آخر تحديث: 15 يونيو 2026*  
*بإشراف كلود — المدير الاستراتيجي*
