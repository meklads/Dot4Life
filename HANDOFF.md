# 🤝 HANDOFF — Dot4Life Repository Guide

> آخر تحديث: 2026-06-15
> المرجع الموحّد للعمل على المستودع — يُقرأ من عامر و هيما

---

## 1. 🏗️ بنية المستودع

```
Dot4Life/
├── HANDOFF.md                     ← هذا الملف — اقرأني أولاً
├── README.md
├── .gitignore
├── .github/workflows/deploy.yml   ← GitHub Actions (لا تستخدمه مع Coolify)
├── skills/                        ← 🧠 الـSkills الحقيقية (مشتركة بين عامر و هيما)
│   ├── TEAM-CONTEXT.md            ← عقد العمل بين الأداتين
│   ├── EXECUTION-ORDERS.md        ← أوامر التنفيذ اليومية لـ هيما
│   ├── content-writer/            ← Skill: كتابة المحتوى
│   ├── seo/                       ← Skill: تحسين محركات البحث
│   ├── designer/                  ← Skill: التصميم الجرافيكي
│   ├── video-youtube/             ← Skill: فيديوهات يوتيوب
│   ├── social-media/              ← Skill: إدارة السوشيال ميديا
│   └── ads-manager/               ← Skill: الإعلانات المدفوعة
├── index.html                     ← 🎯 الصفحة الرئيسية (جذر الموقع)
├── 404.html
├── CNAME, robots.txt, sitemap.xml
├── styles/                        ← CSS
├── scripts/                       ← JavaScript
├── assets/                        ← صور وأيقونات
├── tools/, blog/, guides/         ← أدوات، مقالات، أدلة
├── featured-stories/, comparisons/, peace-capsules/
├── health-pregnancy/, finance-wealth/, islamic-hajj-umrah/
├── real-estate/, fitness/, content/
├── system/                        ← 🔒 internal (review.html, board.html, admin.html)
├── skills/                        ← 🧠 Skills الفريق
├── legacy/                        ← 🗑️ مرجعي
```

---

## 2. 👥 الفريق — النموذج الجديد (بلا هرم إداري)

```
👻 Ghost (أنت — صاحب القرار)
   │
   ├── 🏗️ عامر (Claude Desktop) — المعماري
   │     يبني الـSkills، يصمم القوالب، يراجع أسبوعياً
   │
   └── ⚡ هيما — المنفّذ اليومي
         يشتغل بالـSkills: مقالات، SEO، سوشيال، فيديو، إعلانات
```

### المنفّذون النشطون (Doers)

| الاسم | الدور | الـSkill |
|-------|-------|----------|
| 🎨 عمر | Graphic Designer | `designer` |
| ✍️ موني | Content Writer | `content-writer` |
| 🔍 ميدو | SEO Developer | `seo` |
| 🎬 هيما | Video Editor | `video-youtube` |
| 🤖 لينو | Tech & Automation | — (تقنية) |
| 📈 مازن | Social Media Manager | `social-media` |
| 📊 Ads Manager | Performance Ads | `ads-manager` |

> **ملاحظة:** رائد (CEO)، يوسف (BA)، نادر (PM)، جاد (PM)، فارس (Sales)، يونس (Tech Support) — مركونون في `Team Work/skills/dormant/`

---

## 3. 🔧 قواعد أساسية (لا تتكسر)

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

---

## 4. 🚀 النشر

### Coolify (المُعتمَد)
- **Build Pack:** `Static` (ليس Nixpacks)
- **Base Directory:** `.` (الجذر — لا `site/`)
- **Publish Directory:** `.`
- يسحب من: `meklads/Dot4Life:main`
- سيرفر: Hostinger

### GitHub Pages (موجود لكن لا تستخدمه مع Coolify)
- يوجد workflow في `.github/workflows/deploy.yml`
- ينشر إلى `dotforlife.com` عبر GitHub Pages
- **تنبيه:** لا تشغّل الدومين نفسه من النظامين معاً

---

## 5. 📋 التسليم اليومي

كل المخرجات تُسلّم في:

| المخرج | المسار |
|--------|--------|
| المقال | `site/[section]/[article-name].html` |
| CSS/JS | `site/styles/`, `site/scripts/` |
| الصور | `site/assets/images/` |
| التقارير | `site/system/review.html` |

---

## 6. ⚠️ معلّقات سابقة

- [ ] ألوان الـ sub-menu بزخارف لكل قسم
- [ ] أزرار مشاركة واتساب على الأدوات
- [ ] إصلاح الهيرو لعمودين
- [ ] تنظيف الشرطات
- [ ] توحيد هيرو ٢٣ صفحة

---

## 7. 📂 مرجع خارجي

| المسار | المحتوى |
|--------|---------|
| `../Team Work/skills/` | النسخة القديمة من أدوار الفريق (برومبتات، مركون) |
| `../Team Work/operating-systems/` | الأنظمة الخفيفة: Weekly-Rhythm, Decision-Scoring, Traction-Dashboard |
| `../Team Work/notion/` | قوالب Notion ومزامنة العمل |

---

> **اقرأني قبل أي تعديل:** هذا الملف مرجع للمحافظة على بنية المشروع.
> الـ TEAM-CONTEXT.md هو العقد بين عامر و هيما — اقرأه لفهم تقسيم العمل.
