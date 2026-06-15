# 🤝 HANDOFF — Dot4Life Repository Guide for Claude Ship

> آخر تحديث: 2026-06-15
> مرجع دائم لـ Claude Ship عند العمل على هذا المستودع

---

## 🔧 آخر إصلاح حرج — تسطيح المجلدات المكرّرة (commit `7071e45`)

**المشكلة:** الـ"Major restructure" خلّف **19 مجلداً متداخلاً مرتين** داخل `site/`:
`styles/styles`, `tools/tools`, `blog/blog`, `assets/assets`, `scripts/scripts`, `og/og`,
`guides/guides`, `cities/cities`, `comparisons/comparisons`, `content/content`,
`featured-stories`, `fitness`, `health`, `health-pregnancy`, `real-estate`,
`peace-capsules`, `finance-wealth`, `islamic-hajj-umrah`, `_external-pages`.

بما أن كل الروابط مطلقة (`/styles/...`, `/tools/...`)، كان الموقع يُبنى وينشر **بدون تنسيق ولا أدوات**.
وكان هذا أيضاً سبب فشل Nixpacks ("failed to detect application type") لأن الجذر ليس فيه تطبيق.

**الحل (تم):** تسطيح كل الـ19 مجلد — git سجّلها **renames بنسبة 100%** (صفر تغيير محتوى).
كل المسارات تعمل الآن (تم التحقق: `GET /styles/global.css` → 200، `/tools/*.html` → 200، `/assets/images/*` → 200).

**قاعدة وقائية:** أي إعادة هيكلة مستقبلية — تحقّق فوراً أن `site/<dir>/<dir>` **غير موجود** قبل الـ commit.

---

## 1. 🏗️ بنية المستودع

```
Dot4Life/
├── HANDOFF.md                     ← هذا الملف — اقرأني أولاً
├── README.md
├── .gitignore
├── .github/workflows/deploy.yml   ← GitHub Actions (لا تستخدمه مع Coolify)
├── site/                          ← 🎯 جذر الويب الفعلي (Web Root)
│   ├── index.html                 ← الصفحة الرئيسية
│   ├── CNAME, robots.txt, sitemap.xml
│   ├── styles/                    ← CSS
│   ├── scripts/                   ← JavaScript
│   ├── assets/                    ← صور وأيقونات
│   ├── tools/, blog/, guides/     ← أدوات، مقالات، أدلة
│   ├── featured-stories/, comparisons/, peace-capsules/
│   ├── health-pregnancy/, finance-wealth/, islamic-hajj-umrah/
│   └── system/                    ← 🔒 internal (لوحة المراجعة، الإدارة، Notion)
├── legacy/                        ← 🗑️ مرجعي
└── ——————————
```

## 2. 🔑 قواعد أساسية (لا تتكسر)

### الروابط
- **جميع روابط الأصول مطلقة** من جذر `site/`:
  - `/styles/...`, `/scripts/...`, `/assets/images/...`
  - `/tools/...`, `/blog/...`
- لا تضع مجلداً داخل مجلد بنفس الاسم (ممنوع `styles/styles/`)

### اللغة
- سكربت في `<head>` يحدد اللغة حسب المنطقة الزمنية:
  - الأولوية: `?lang=` ← `localStorage('dfl-lang')` ← الموقع الجغرافي
  - الخليج/العرب → عربي (rtl) | غيرهم → إنجليزي (ltr)

### Cache-busting
- روابط CSS فيها `?v=<hash>` (content-hash)
- بعد أي تعديل CSS، جدّد الـ hash

### ألوان الهوية
| اللون | الاستخدام |
|-------|-----------|
| `#054241` | أخضر غامق — الرئيسي |
| `#6abfb8` | تركوازي — ثانوي |
| `#fd781c` | برتقالي — accent |

## 3. 🚀 النشر

### Coolify (المُعتمَد)
- **Build Pack:** `Static` (ليس Nixpacks)
- **Base Directory:** `./site`
- **Publish Directory:** `.`
- يسحب من: `meklads/Dot4Life:main`
- سيرفر: Hostinger

### GitHub Pages (موجود لكن لا تستخدمه مع Coolify)
- يوجد workflow في `.github/workflows/deploy.yml`
- ينشر إلى `dotforlife.com` عبر GitHub Pages
- **تنبيه:** لا تشغّل الدومين نفسه من النظامين معاً

## 4. ⚠️ معلّقات سابقة (تحتاج تأكيد)

بعض التعديلات التالية اتعملت على البنية القديمة المسطّحة وقد لا تكون وصلت إلى `site/`:

- [ ] ألوان الـ sub-menu بزخارف لكل قسم
- [ ] أزرار مشاركة واتساب على الأدوات
- [ ] إصلاح الهيرو لعمودين
- [ ] تنظيف الشرطات
- [ ] توحيد هيرو ٢٣ صفحة

## 5. 👥 الفريق

```
👻 Ghost (General Director)
   └── 📊 رائد (Project Manager)
        ├── 🎨 عمر (Graphic Designer)
        ├── ✍️ موني (Content Writer)
        ├── 🔍 ميدو (SEO Developer)
        ├── 🎬 هيما (Video Editor)
        ├── 🤖 لينو (Automation Engineer)
        ├── 📈 مازن (Marketing Strategist)
        ├── 🤝 فارس (Sales Closer)
        └── 🛠️ يونس (Tech Support)
```

> تم إزالة Manus — مهام التصميم أصبحت لعمر.

---

**اقرأني قبل أي تعديل:** هذا الملف مرجع للمحافظة على بنية المشروع. أي إعادة هيكلة مستقبلية يجب أن تتحقق من عدم تكرار المجلدات.
