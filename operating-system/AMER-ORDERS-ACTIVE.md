# 🛡️ أوامر عامر النشطة (المصدر الثابت) — 2026-06-24 (آخر دورة 15:00)

## 🟢 حاكم — Batch 02 المصداقية: التصحيح انطلق (دورة 15:00)
عملية تصحيح متزامنة تعيد كتابة الـ14 ملفاً على working-tree (نسخ احتياطية في `outputs/backups/credibility-fix-140700/`). الحالة اللحظية: 4 ملفات بلغت روابط عميقة (saving-vs-investing ع pct:0 ✅ · arab-mother-startup ع pct:3 ✅ · evening-rituals ع pct:3 ✅) · المالية gold ع/en + saving en بروابط عميقة لكن نِسَب 17–34 **فوق سقف ≤3** · family-nutrition/medina/umrah-visa لم تُمسّ بعد. **الحجز قائم — 0 نقل إلى done؛ لا ملف يجتاز البار الكامل (رابط عميق لكل نسبة + ≤3 نِسَب + تكافؤ ع/en).** الأقرب للاجتياز توائمه EN متأخرة. **لم يلتزم عامر أي ملف مُصلَّح (anti-collision).** المالية تحتاج خفض كثافة الأرقام لا مجرّد روابط. إعادة فحص كاملة الدورة القادمة.

## 🔴 حاكم — عيبا صفحة Batch 03 لـ Cursor (دورة 15:00)
المرجع: `reports/amer-to-cursor-batch03-page-defects-2026-06-24.md`
1. `blog/daily-islamic-habits-guide.html` (ع): **بلا أي JSON-LD** (Article+FAQPage مفقودان) + جسم ~991w < 1300 (EN سليم 1539w/2 بلوك). → حقن schema + تعميق (Hema).
2. `blog/digital-minimalism-families.html` (ع): **FAQPage مكرّرة حرفياً** + FAQ إنجليزي في صفحة عربية + سؤال «قمامة» (نشرة/روابط). → حذف المكرّرة + تعريب + إزالة القمامة.
3. **إصلاح منهجي:** مولّد حقن FAQ يكرّر الكتلة/يبتلع نص النشرة/يترك صفحات بلا schema. أصلح المولّد لا الصفحة.
**PASS (4):** evening-rituals · gulf-father-money-lessons · government-vs-private-school-gulf · pregnancy-nutrition-first-trimester.

## 🟢 حاكم — عائق الدفع حُلّ (دورة 13:00)
أقفال git اليتيمة التي عطّلت الدفع 4 دورات أُزيحت بـ`mv` (ينجح حيث يفشل `unlink` على مونت virtiofs). الشجرة نظيفة، origin/main مدموج، الالتزام والدفع منفّذان. **قاعدة تشغيلية للدورات القادمة:** حين تظهر `.git/*.lock` يتيمة لا تُحذف بـ`rm` → استخدم `mv "$lock" .git/_stale_locks/`، أمر git واحد لكل استدعاء، أزِح القفل بعد كل أمر.

## 🔴 حاكم — Batch 02 كامل على تعليق المصداقية (مستمرّ من 11:00 — لا تقدّم 13:00)
عُمّمت بوابة الرابط العميق على الـ7 مقالات (14 ملف) → **0 رابط عميق في أي ملف؛ كل الاستشهادات صفحات رئيسية مجرّدة**. **رُجِعت كلها لـ Hema** (تفاصيل بنود: `reports/amer-to-hema-batch02-credibility-2026-06-24.md`). **لا تصحيحات وصلت في دورة 13:00** (mtime بلا تغيير؛ inbox/hema = DEEPEN+A-09 فقط). أولوية التصحيح: B2-02 + B2-07 (مالية، 38/26 نسبة) ثم B2-01/03/04 ثم B2-05/06. **لا LIVE/نقل نهائي قبل اجتياز المصداقية.** الكل LIVE حالياً بنِسَب بلا رابط عميق = **خطر مصداقية**؛ الدفع لم يعد معطّلاً، فالتصحيح صار قابلاً للنشر فور وصول نص Hema المُصحَّح. **عيب صفحة لـ Cursor (متأخر دورتين → مُصعَّد لجوست):** `featured-stories/arab-mother-startup.html` (ع+en) بلا `<aside>` سايدبار — التمبليت يدعمه (الشقيقان gulf-father-money-lessons + saudi-father-carpentry-workshop فيهما aside). `evening-rituals` مكتمل (PASS).

> ملف ثابت يحدّثه عامر فقط. الأوتوبايلوت يعيد كتابة `inbox/*.md` كل دورة، لذا الأوامر المُلزِمة هنا.
> تفاصيل كل أمر في تقارير `reports/amer-to-*.md`.

---

## 🟢 أمر Cursor — Batch 02 (نفّذ قبل أي اعتماد LIVE)
المرجع: `reports/amer-cycle-2026-06-24-0306.md`
**النص اجتاز بوابة عامر: 7/7 مقالات (14 ملف) APPROVED** — لا تعديل نصّي. **الصور كلّها جاهزة ومعتمَدة** (7 heroes موجودة في `assets/images/approved/` 1200×750 WebP + `visual_director=approved` بالمانيفست). **لا توليد جديد مطلوب.** المتبقّي لـ LIVE:
1. ✅ **عيب Schema حُلّ مباشرةً (عامر):** `blog/family-nutrition-on-budget.html` (ع) الآن FAQPage واحدة صحيحة (5 أسئلة) + Article=1.
2. ✅ **5/7 ربط `figure.hero` تلقائياً** (شغّل عامر `apply-approved-heroes.py`): family-nutrition · umrah-visa · medina-hotels · gold-vs-real-estate · saving-vs-investing — كلها تشير الآن لـ`/assets/images/approved/hero-<slug>.webp`.
3. 🔴 **متبقٍّ على Cursor (3 بنود):**
   - **(أ) arab-mother-startup + evening-rituals (ع+en، 4 ملفات):** لم يصلهما السكربت (قسماهما `featured-stories`/`peace-capsules` خارج SECTIONS، وكلاهما تمبليت article-banner بلا figure.hero). اربط `hero-arab-mother-startup.webp` و`hero-evening-rituals.webp` يدوياً في og:image + banner.
   - **(ب) og:image لم تُحدَّث في الـ5** (ريجِكس السكربت لا يطابق `/>` المغلق ذاتياً) → حدّثها إلى `https://dotforlife.com/assets/images/approved/hero-<slug>.webp`.
   - **(ج) صورة `article-banner` العلوية ما تزال placeholder في الـ5** (التمبليت فيه بانر + figure مكرّران) → وحّدها على الـhero المعتمَد أو احذف البانر المكرّر.

## 🟠 إصلاحات سكربت مطلوبة (Cursor/autopilot — ليست صور)
1. `scripts/apply-approved-heroes.py`: أضِف `featured-stories` و`peace-capsules` إلى `SECTIONS`.
2. نفس السكربت: ريجِكس og:image يجب أن يطابق `<meta property="og:image" content="..." />` (المغلق ذاتياً)، وأن يحدّث صورة `article-banner-img-wrap`.
3. نفس العيب المنهجي في حقن FAQPage: ابتلاع نص الخاتمة/التنقّل كأسئلة «قمامة» — راجع المولّد (ظهر في family-nutrition ع+en).

---

## ✅ منجز (عامر نفّذه)
- صور H-07→H-12: ولّدها عامر عبر Higgsfield، فحص بصري، 1200×750 WebP، الفهرس 12/12 approved.
- بناء 6 صفحات أبطال (12 ملف) — كل البوابات PASS — **مدفوعة LIVE** (`ada54db`).
- **دورة 19:10 — أُغلقت دفعة التعميق كاملة (9 ملفات):** Hema عمّقت B(2)+C(7)؛ عامر أعاد الفحص الآلي الكامل → **9/9 PASS** (جسم 1661–2089 كلمة، شرطات=0، Article+FAQPage صحيحا JSON، FAQ≥4، إخلاء، مصادر https، LIVE في sitemap). نُقلت T-05/06/07 من «عامر» إلى «done».

---

## ⛔ تجميد المحتوى الجديد (جوست 2026-06-24) — حاكم
**القاعدة:** بعد Batch 03 → **لا مواد جديدة نهائياً** حتى تقليص القصور (155 صفحة DEEPEN). المرجع: `QUALITY-FIRST-POLICY.md` + قفل `new-content-frozen.json`.
- **الاستثناء الوحيد:** Batch 03 يكمل (✅ مكتمل: 7 مقالات LIVE بصورها).
- الأولوية: (أ) Batch 03 ✅ · (ب) سكيل الكتابة يقلّص الـ155 وفق WRITING-LAW (≥1600 كلمة) · (ج) بعد AN-00 مضاعفة المقالات الرابحة.
- **فتح Batch 04 يتطلب:** DEEPEN ≤25 + جودة الموقع ≥60% + أمر جوست الصريح «افتح دفعة جديدة».

### 🛡️ واجب عامر — اعتراض وإبلاغ (مُثبَّت)
**عامر طبقة اعتراض ثانية فوق قفل Cursor:** إن رأى أي **مادة جديدة** (مقال/دفعة/قسم) أثناء التجميد → **يعترض فوراً ويبلّغ جوست**، ولا يُجيز نشرها مهما مرّت بقية البوابات.
- الفحص الآلي كل دورة: `python3 scripts/amer_freeze_watch.py` (يطبع OBJECTION + المخالفات، كود خروج 1).
- المادة الجديدة = ليست DEEPEN لصفحة قائمة، وليست Batch 03 → **مرفوضة ومُبلَّغة**.

## 🟢 أمر Cursor — نفّذ الآن
المرجع: `reports/amer-to-cursor-c03-gate.md` · `reports/c03-scope-approved.txt`
0. **⛔ لا دفعات/مواد جديدة (batch-04+, أقسام جديدة) — مرفوضة آلياً (`deepen_gate.py`). الاستثناء: Batch 03 فقط (مكتمل) + DEEPEN.**
1. الصور: ✅ تمّت — صفحات الأبطال LIVE.
2. **المتبقّي الوحيد = T-02 (4 مسودات task09 → HTML):** summer-camps-vs-home (ع/en) + family-volunteering-summer (ع/en). كلها اجتازت بوابة عامر (≥1300 كلمة، 0 شرطات، 0 اقتباس مختلَق، مصادر، إخلاء — APPROVED). ابنِها عبر `build-from-approved-draft.py` وانشر وادفع.
   - 13 ملف T-03 = ✅ مبنية وLIVE (في sitemap). لا إعادة.
3. بعد النشر: احذف مكرّرات `assets/queue/`.
4. **رُفع الحظر السابق:** pregnancy-weeks-guide · umrah-budget-guide-families-en عُمّقتا واجتازتا البوابة (1661w/1793w) — LIVE. باقٍ فقط: لا بناء T-04 القديمة المرفوضة إن وُجدت بلا تعميق.
5. لا تشغّل `inject-article-schema.py` بالجملة.

## ✅ أمر Hema (دفعة التعميق 9 ملفات) — مُغلق
- **B(2):** pregnancy-weeks-guide (1661w) · umrah-budget-guide-families-en (1793w) → ✅ PASS.
- **C(7):** visceral-fat-gulf · end-of-service-saudi (ع/en) · pregnancy-nutrition-first-trimester (ع/en) · saving-for-education-gulf (ع/en) → ✅ PASS (1731–2089w).
- اعتمدها عامر بالفحص الآلي الكامل في دورة 19:10. لا عمل متبقٍّ في هذه الدفعة.
> تذكير حاكم: التوليد الفعلي للصور = عامر فقط (MCP). أدوار عمر/كلود تجهّز البرومبت؛ Hema تكتب النص.

## ✅ صور W-01..03 — مكتملة (لا عمل)
الثلاثة heroes موجودة في `assets/images/approved/` (`hero-hijri-new-year-children.webp` · `hero-teaching-children-allah-names.webp` · `hero-teaching-children-prayer-with-love.webp`) **ومربوطة فعلاً** في صفحاتها بـ`islamic-hajj-umrah/` (3–4 مراجع/صفحة: og+banner+figure). لا توليد Higgsfield ولا صرف كريديت مطلوب. (تصحيح: الملاحظة السابقة بأنها «معلّقة» كانت قديمة.)

---

## ⚖️ ولاية عامر الثلاثية (مُثبّتة باتفاق جوست — 2026-06-23)
عامر هو **بوّابة الجودة الوحيدة قبل LIVE**. ثلاث مسؤوليات حاكمة لا تُتجاوز:

1. **استلام المقالات على المعايير:** كل مقال (موني/Hema) يُستلَم ويُفحَص مقابل **`WRITING-LAW.md` + `content-standards.md`**: عمق 1600–2400w، قصص حيّة، مراجع https محقّقة، خطّاف وتأثير، صفر شرطات، Article+FAQPage، إخلاء، 4/5 في كل بُعد. ما لا يبلغ المعيار → يُرجَع بملاحظات بنود، لا يُنشر.

2. **البرومبتات بمعايير عالية:** كل برومبت صورة (قبل التوليد) يلتزم **`VISUAL-DIRECTION.md`**: احتشام كامل، هوية، تنويع، نسبة أشخاص ~1:5، حياة جميلة، 1200×750. عامر يولّد (Higgsfield) ويفحص بصرياً ويعتمد/يرفض.

3. **مراجعة الصفحات بعد بناء Cursor:** بعد ما يصمّم Cursor صفحة المقال (HTML)، **يراجعها عامر مقابل المعايير** قبل اعتماد LIVE نهائياً: التمبليت كامل (هيدر/بانر 1100px/سايدبار/فوتر)، الصورة الصحيحة مربوطة، Schema سليم، الروابط الداخلية، الجوال، صفر شرطات. خلل = إرجاع لـ Cursor.

> **القاعدة:** لا شيء يطلع LIVE إلا بعد بوابة عامر — نصاً وصورةً وصفحةً. الأتمتة تنفّذ، وعامر يجيز.

## 🤖 حلقة الأتمتة تحت إشراف عامر (مفعّلة عند اعتماد جوست)
- صور approved + ملف → الأوتوبايلوت يبني ويدفع (موجود).
- نص يجتاز بوابة عامر كاملة → يُنشر آلياً؛ ما لا يجتاز → يُرجَع لـ Hema بملاحظات، **لا نشر YMYL ضعيف على مؤقّت**.
- **بعد بناء Cursor للصفحة → مراجعة عامر للصفحة قبل LIVE النهائي (المسؤولية 3).**
