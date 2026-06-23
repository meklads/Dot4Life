# دفعة الصور الرئيسية #1 — برومبتات توليد ملتزمة بالهوية

> **من:** عمر (المدير البصري) · **إلى:** عامر · **التاريخ:** 2026-06-22
> **الحالة:** التوليد الفعلي غير متاح في هذه البيئة (مساحة العمل على خطة مجانية، الرصيد = 0). أداة generate_image متصلة لكنها ترفض التوليد بخطأ "Out of credits".
> لذلك — وفق بروتوكول التكليف — **لم أختلق أي ملف صورة**. أدناه برومبت دقيق لكل slug + صفوف الفهرس بحالة visual_director: "pending".
> كل صورة مطلوبة: **WebP 1200×750**، تُحفظ في assets/images/approved/hero-<slug>.webp، ثم تتحوّل حالتها إلى approved بعد مرورها على بوابة visual-director.

## مواصفات تقنية موحّدة
- نسبة 3:2 عند التوليد ثم قصّ مركزي إلى **1200×750** WebP (جودة ~85).
- toning دافئ كريمي/ذهبي خفيف يتناغم مع لوحة البراند.
- بلا نصّ محروق، بلا شعارات، بلا علامة مائية.
- احتشام حاكم: حجاب كامل ساتر للمرأة (شعر + عنق + صدر)، ملابس فضفاضة، لا عُري ولو جزئي، لا أوضاع إيحائية، لا مكياج صارخ.
- ممنوع: الخنزير/حصّالة الخنزير، الكحول، القمار، أي رمز مخالف للقيم.

---

## 1) family-budget-plan — المالية (لمسة برونزي/ذهبي #b8893c)
Documentary-style warm photograph, family finance theme. A modest Gulf Arab family scene at a wooden home table: a father in a clean white thobe and a mother wearing a full, loose hijab covering hair, neck and chest, calmly planning a household budget together. On the table: a simple notebook, a calculator, a small ceramic coin jar (NOT a piggy bank), some coins, and a small green plant. Soft natural window light, shallow depth of field. Color toning warm and on-brand: deep teal-green #054241 accents, warm cream #FAF8F4 background tones, subtle bronze/gold #b8893c accent detail. Calm, dignified, authentic captured moment, not a stock pose. No alcohol, no gambling, no pig or piggy bank. Modest loose clothing, no exposed skin beyond face and hands. No text, no watermark, no logos. Realistic skin texture, editorial, rule of thirds, breathing negative space.

## 2) bmi-calculator-women — صحة المرأة (لمسة تركوازي #6abfb8)
Documentary-style warm photograph, women's health and wellness theme (BMI / healthy body weight for women), fully modest. A modest scene with NO exposed body: a woman wearing a full loose hijab covering hair, neck and chest, in modest loose clothing, standing respectfully in a calm bright home or clinic setting, looking thoughtfully at a simple wall chart or holding a measuring tape, with a glass of water and fresh fruit on a table. Wide/medium respectful framing, camera never focused on the body. Soft natural light, shallow depth of field. On-brand color toning: deep teal-green #054241, warm cream #FAF8F4 background, calm turquoise #6abfb8 accent details. Dignified, wholesome, authentic captured moment, not a stock pose, no advertising smile. No tight or revealing clothing, no exposed legs/arms/chest, no provocative pose, no heavy makeup. No text, no watermark, no logos. Realistic skin texture, rule of thirds, soft negative space.

## 3) daily-adhkar-family-guide — إسلامي/أسري (لمسة ذهبي هادئ #b8893c)
Documentary-style warm photograph, Islamic daily adhkar family theme. A calm spiritual home scene: an open simple adhkar booklet or prayer beads (misbaha) resting on a clean surface near a window, with warm morning light, a small plant, and a softly blurred modest family presence in the background (a mother in full loose hijab and a child, respectful family interaction, no faces in focus). Quiet, reverent atmosphere. On-brand warm toning: deep teal-green #054241, warm cream #FAF8F4 background, dignified soft gold #b8893c accent (warm light, brass detail). Authentic captured moment, not a stock pose. Respect for religious symbols, dignified placement. Modest clothing only, no exposed skin beyond face and hands, no provocative elements. No Quranic verses rendered as burned-in text, no watermark, no logos. Realistic texture, rule of thirds, gentle negative space.

## 4) children-sleep-summer — نوم الأطفال/أسري (لمسة تركوازي دافئ #6abfb8)
Documentary-style warm photograph, children's sleep in summer theme. A young child sleeping peacefully in a tidy, modest family bedroom on a warm summer night: soft dim bedside lamp, light breathable bedding, a small fan or open window suggesting summer, calm cozy mood. The child wears modest, appropriate sleepwear, framed respectfully and gently, innocent natural moment, privacy preserved (no identifying sensitive details). Optional softly blurred modest parent presence tucking the child in. On-brand toning: deep teal-green #054241, warm cream #FAF8F4 tones, calm warm turquoise #6abfb8 accent detail. Authentic captured moment, not a stock pose, no emotional exploitation, no crying child. No text, no watermark, no logos. Realistic skin texture, shallow depth of field, rule of thirds, soft negative space.

---

## خطوة المعالجة بعد التوليد (لكل صورة)
1. نزّل الصورة الناتجة.
2. قصّ مركزي + إعادة تحجيم إلى **1200×750**، حفظ WebP جودة ~85.
3. احفظ في assets/images/approved/hero-<slug>.webp.
4. مرّر الصورة على بوابة visual-director (الاحتشام/الألوان/الجودة).
5. عند الإجازة: حدّث visual_director إلى approved في image-manifest.json (Python للكتابة الآمنة).
