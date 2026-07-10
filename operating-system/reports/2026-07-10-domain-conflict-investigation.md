# تحقيق تعارض الدومين — 2026-07-10

**الطلب:** أمر عامر (إعادة فتح المرحلة 1)  
**المنفّذ:** كورسر  
**الحالة:** تقني مؤكَّد — جزء الاستضافة/GSC يحتاج جوست

---

## 1) هل الدومين كان لموقع آخر؟ هل الاستضافة ما زالت تخدمه؟

### الحكم: **نعم — الدومين كان موقع WordPress زراعي/حدائق سابقاً. لا — الاستضافة الحالية لا تخدم ذلك المحتوى.**

| فحص | النتيجة |
|-----|---------|
| محتوى الريبو (`grep` vegetable-garden / category/gardening / wp-content) | **صفر** في HTML الحي (عدا `_external-pages/offer.html` خارجي) |
| `curl` مباشر على روابط GSC القديمة | **404** — صفحة `404.html` فقط (لا مقال زراعي) |
| `site:dotforlife.com` (بحث جوجل، 2026-07-10) | **لا يزال يعرض** عناوين زراعية مفهرسة (WordPress slugs طويلة، `/category/gardening/`) |
| DNS/استضافة حالية | Cloudflare → Coolify/static `serve` — **لا WordPress، لا PHP، لا feeds** |

**أمثلة مؤكَّدة (404 حيّاً، لكن ما زالت في فهرس جوجل):**

- `/how-to-create-a-chemical-free-vegetable-garden-your-ultimate-guide-to-organic-gardening-success/`
- `/how-to-create-a-chemical-free-vegetable-garden-.../feed/`
- `/category/gardening/`
- `/sustainable-soil-management-building-healthy-garden-beds-.../`

**الاستنتاج:** المشكلة **ليست** أن DNS يشير لسيرفر قديم. المشكلة أن **جوجل يحتفظ بذاكرة الفهرس** ويعيد الزحف لروابط WordPress القديمة (تواريخ GSC 20–22 يونيو 2026 = إعادة محاولة زحف، ليس محتوى حيّ).

### هل نستخدم «تغيير العنوان» في Search Console؟

**لا.** أداة Change of Address للانتقال **من دومين إلى دومين آخر**. هنا نفس `dotforlife.com` — تغيّر المحتوى بالكامل (استبدال WP بموقع عائلي ثابت).

### ما الذي يحتاج جوست مباشرة (خارج الكود)

1. **Search Console → Removals** (مؤقت) أو **إزالة بادئة URL** لأنماط:
   - `/category/`
   - `/*/feed/`
   - slugs زراعية معروفة (قائمة في القسم 4)
2. **Cloudflare Redirect Rules** (اختياري لكن موصى به): 301 من `/capsule.html?id=*` و`/capsule?id=*` إلى `/life-guide.html?c={id}` — HTTP 301 حقيقي يحفظ query (أفضل من JS فقط).
3. **تأكيد ملكية GSC** على property `https://dotforlife.com/` (ليس www فقط إن وُجد انقسام).
4. **لا حاجة** لتغيير DNS إن كان يشير لـ Coolify الحالي فقط — تحقق من عدم وجود A/CNAME قديم لاستضافة WP.

---

## 2) مصدر الروابط الغريبة (`<h2 id=`, `/.html`, `/mo`, `/yr`)

### فحص شامل على الكود الحي (2026-07-10)

| النمط | `articles.json` | HTML حي (بدون outputs/legacy) | `git grep` تاريخي |
|-------|-----------------|-------------------------------|-------------------|
| `href="<h2` / `h2 id` | 0 | 0 | 0 |
| `href=".html"` / `/.html` | 0 | 0 | 0 |
| `href="/mo"` / `href="/yr"` | 0 | 0 | 0 |
| روابط ≤3 أحرف (`/mo`, `/yr`) | — | 0 | 0 |

**المولّدات المفحوصة:**

- `scripts/feed.js` (أرشيف/مدونة/هوم) — يقرأ `a.url` من `articles.json` سليم
- `scripts/migrate-article-template.py` (`find_related_articles`, read-also)
- `scripts/build-from-approved-draft.py` (`internal_links_*`)

**الحكم:** **لا مصدر حيّ** لهذه الأنماط في الكود الحالي. الأرجح:

1. **بقايا زحف** من نسخ HTML قديمة كانت فيها وسوم مقطوعة (`</a></p><h2 id=` بدون إغلاق `<a>`) — أُصلحت لاحقاً.
2. **Google يستخرج URL خاطئاً** من شذرات HTML في صفحات قديمة مفهرسة.
3. `/.html` و`/mo`/`/yr` قد تكون **تحليل خاطئ** لروابط نسبية أو slugs قديمة — ليس من `sitemap-tools.xml` (مؤكَّد سليم بـ`.html`).

**إجراء وقائي:** تحقق في `feed.js` يرفض `href` فيها `<` أو طول مشبوه.

---

## 3) إعادة توجيه `capsule.html?id=` → `life-guide.html`

| قبل | بعد |
|-----|-----|
| `capsule.html?id=cap_*` → 301 Cloudflare → `/capsule?id=*` → **404** | **`capsule.html`** جديد: `location.replace('/life-guide.html?c=' + id)` |
| `life-guide.html` يقبل `?c=` و`?g=` فقط | يقبل أيضاً **`?id=`** (توافق خلفي) |
| `capsule-fetch.js` | يستخدم `/life-guide.html?c=` — **لا تغيير مطلوب** |

**ملاحظة:** التوجيه الحالي **client-side** (فوري). لـ **301 HTTP** مع query: قاعدة Cloudflare (جوست).

---

## 4) قائمة إجراءات جوست (GSC + Cloudflare)

### Cloudflare — قاعدة redirect مقترحة

```
If: (http.request.uri.path eq "/capsule.html" or http.request.uri.path eq "/capsule")
    and http.request.uri.query contains "id="
Then: 301 to https://dotforlife.com/life-guide.html?c={extract id param}
```

### GSC — بادئات إزالة/تجاهل زحف (WordPress legacy)

```
/category/
/tag/
/author/
/wp-content/
/wp-includes/
/*/feed/
/feed/
/how-to-create-a-chemical-free-vegetable-garden
/sustainable-soil-management
/gardening-101
/ultimate-guide-to-rainwater-harvesting
```

### robots.txt (نُفِّذ في الكود)

أُضيف `Disallow` لمسارات WP و`/category/` و`/*/feed/` لتقليل إهدار crawl budget.

---

## 5) ما لم يُلمَس (حسب الأمر)

- 72 alternate-canonical · 42 redirect · 10 noindex · 5 duplicate · 4 forbidden · 2 soft404 · 1 robots — **لا إجراء** (متوقعة).

---

## 6) علاقة «180 اكتُشفت ولم تُزر»

السبب المرجّح **ثقة/أولوية زحف منخفضة على الدومين** بعد تغيير جذري للمحتوى + ضجيج 404 من WP القديم — ليس عيب صفحة واحدة. الحل تراكمي: إزالة/410 للقديم، 301 للـcapsule، sitemap نظيف، روابط داخلية قوية.

---

**الملفات المُعدَّلة:** `capsule.html` (جديد) · `life-guide.html` · `robots.txt` · `scripts/feed.js` · هذا التقرير
