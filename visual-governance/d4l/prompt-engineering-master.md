# 🎨 مرجع كتابة البرومبت الاحترافي — لعمر (D4L Image Prompts Master)
> جمعه عامر من أفضل ممارسات 2026. الهدف: برومبت يولّد صورة ممتازة **من أول مرة** (توفير كريدت).
> القاعدة الذهبية: **التحديد يتفوّق على الحشو.** «highly detailed» كلمة فارغة في نماذج 2026؛ صِف التفاصيل الحقيقية بدلاً منها.

## 1) تشريح البرومبت القوي (الترتيب يهمّ)
اكتب بهذا التسلسل الثابت:
1. **النوع/الاستخدام + الواقعية:** «Photorealistic editorial hero photograph for an article header».
2. **المشهد/البيئة:** أين؟ (طاولة منزل خشبية، مطبخ مضاء، نافذة عند الفجر).
3. **الموضوع الرئيسي:** ما البطل؟ (جرّة عملات + دفتر؛ مسبحة قرب مصحف).
4. **3–6 تفاصيل ملموسة عالية الإشارة:** مواد، ملمس، ألوان محدّدة (نحاس لامع، خشب بحبيبات، بخار خفيف).
5. **الإضاءة:** اتجاهها ونوعها (soft natural window light from upper left, golden hour, diffused).
6. **الكاميرا/العدسة:** بُعد بؤري + فتحة + نوع لقطة (85mm prime, f/2.8, shallow depth of field, three-quarter angle, top-down packshot).
7. **المزاج + الهوية + القيود/السلبيات.**

## 2) روافع الواقعية (لغة المصوّرين المحترفين)
- **العدسة:** 35mm (مشهد واسع) · 50mm (طبيعي) · 85mm (بورتريه/تفاصيل) · 100mm macro (تفاصيل دقيقة).
- **الفتحة:** f/2.8 (خلفية ضبابية ناعمة) · f/8 (وضوح شامل).
- **الإضاءة:** «single softbox at 45 degrees» · «three-point» · «soft window light» · «golden hour backlight».
- **الملمس الواقعي:** «subtle surface texture, fine grain, realistic material reflections, gentle dust motes in light».
- **التدرّج اللوني:** «natural color grading, warm tones» بدل «vivid/saturated».

## 3) التحديد بدل الحشو (الأهم)
- ❌ «highly detailed, 4k, masterpiece, beautiful» (junk tokens).
- ✅ «brass coin jar with visible scratches, woven beige placemat, condensation on a glass of water, soft green leaves catching light».
> صِف **ما تراه العين** لا صفات عامة.

## 4) البرومبت السلبي (Negative — قيود بنيوية)
أرفق دائماً قائمة منع:
`blurry, distorted hands, extra limbs, deformed, low resolution, flat lighting, watermark, signature, text, logo, cartoon, 3d render, oversaturated, plastic skin`
وللهوية أضف منعنا الخاص:
`no exposed skin beyond face and hands, no tight clothing, no pig or piggy bank, no alcohol, no gambling, no Quranic text burned in, no faces in sharp focus when modesty-sensitive`

## 5) وعي النموذج (Higgsfield)
- النماذج الوصفية (Nano Banana / GPT Image): تفضّل **فقرة وصفية متّصلة** غنية (جُمل كاملة).
- النماذج الكلماتية: تفضّل **عبارات قصيرة عالية الإشارة** مفصولة بفواصل.
- ابدأ بالفقرة الوصفية (أأمن للالتزام بالاحتشام)، وإن لزم بدّل للكلمات المفتاحية.

## 6) قيود D4L المدمجة (انسخها في كل برومبت)
- **المقاس/الإطار:** 1200×750، نسبة 16:10، hero header, rule of thirds, breathing negative space.
- **الهوية اللونية:** deep teal-green #054241, warm cream #FAF8F4 background, + لمسة القسم (مالية/إسلاميات ذهبي #b8893c · صحة/عائلة تركوازي #6abfb8 · عقار زيتوني #4a8a82).
- **الاحتشام (حاكم):** أي إنسان = حجاب كامل ساتر + ملابس فضفاضة + لا عُري + لا أوضاع إيحائية. **فضّل still-life/مشاهد بلا أشخاص** كلما أمكن.
- **بلا نصّ محروق، بلا علامة مائية، بلا شعارات.**

## 6.5) الدفء الإنساني (توجّه جوست 2026-06-22 — مهم)
**لا تجعل كل الصور طبيعة صامتة جامدة.** المحتوى العائلي يحتاج **حياة**: أدخِل بشراً محتشمين كلما خدم الموضوع — رجال (ثوب)، **نساء بحجاب كامل ساتر** (يغطّي الشعر والرقبة والصدر)، أطفال، لحظات أسرية دافئة.
- **الاحتشام صارم وحاكم:** لا شعر مكشوف، لا رقبة/صدر/ذراعين/سيقان مكشوفة، ملابس فضفاضة، لا أوضاع إيحائية، مكياج خفيف أو بلا.
- **التوازن:** مشاهد بشرية حيّة للمواضيع التي تستفيد منها (صحة، أسرة، تربية، عمرة)، وطبيعة صامتة للمواضيع التجريدية (مالية، عقار، أدوات).
- **مثبت:** nano_banana ينتج نساءً بحجاب كامل ومشاهد أسرية محتشمة بنجاح (عيّنتا الصحة والأذكار، معتمدتان كمعيار).
- بوابة عامر: تكبير كل وجه/جسم للتأكّد من الاحتشام قبل أي اعتماد.

### المعيار البصري المعتمد (جوست 2026-06-22)
- **الاحتشام:** **كشف الوجه فقط** + حجاب/خمار كامل يغطّي الشعر والرقبة والصدر (نمط: رداء فضفاض + خمار بلون الهوية، كعيّنة السيدة بالرداء الأبيض والخمار الأخضر). الرجال بثوب. الأطفال بلباس محتشم.
- **تنوّع الأماكن (حياة لا جمود):** البيت، المطبخ، المول، البحر (بلباس كامل، لا ملابس سباحة)، الحديقة/المنتزه، المدرسة، السوق، المسجد من الخارج، السيارة العائلية... اختر المكان الذي يخدم الموضوع.
- **الإحساس:** دفء، فرح هادئ، لحظة عفوية أصيلة (candid)، لا بوز إعلاني متكلّف.
- **حاكم:** لا عُري، لا ملابس ضيّقة/كاشفة، لا ملابس سباحة، لا أوضاع إيحائية، لا مكياج ثقيل، لا نصوص.
- **بلا نقاب — الوجه ظاهر (قرار جوست):** المنصة تخاطب الغرب أيضاً، فالنمط **وسطي مقرّب**: حجاب/خمار كامل يغطّي الشعر والرقبة والصدر **مع كشف الوجه**. اكتب صراحةً «face visible, no niqab, no face veil».

## 7) القالب الجاهز (انسخ واملأ)
```
Photorealistic editorial hero photograph, [الاستخدام/الموضوع], 1200x750 16:10.
Scene: [البيئة]. Subject: [البطل]. Details: [3-6 تفاصيل ملموسة].
Lighting: [اتجاه ونوع]. Camera: [عدسة + فتحة + زاوية], shallow depth of field.
Color grading: deep teal-green #054241 accents, warm cream #FAF8F4 background, [لمسة القسم] accent.
Mood: calm, dignified, authentic captured moment, not a stock pose.
Modesty: [إن وُجد إنسان: full loose hijab, modest loose clothing, no exposed skin beyond face and hands].
No text, no watermark, no logo, no pig/piggy bank, no alcohol.
Negative: blurry, distorted hands, extra limbs, flat lighting, watermark, text, cartoon, 3d render, oversaturated, plastic skin.
```

## 8) مثال قبل/بعد (ميزانية الأسرة)
- ❌ ضعيف: «family budget, money, highly detailed, 4k».
- ✅ قوي: «Photorealistic editorial hero photograph, household budgeting theme, 1200x750. Scene: a warm wooden home table near a window. Subject: an open simple notebook, a calculator, a small brass coin jar (not a piggy bank) with a few coins, and a small green plant. Details: visible wood grain, soft brass reflection, condensation on a water glass, woven beige placemat. Lighting: soft natural window light from the upper left, gentle shadows. Camera: 50mm, f/2.8, three-quarter angle, shallow depth of field. Color grading: deep teal-green #054241 accents, warm cream #FAF8F4 background, subtle bronze #b8893c accent. Mood: calm, dignified, authentic. No text, no watermark, no pig/piggy bank, no alcohol. Negative: blurry, distorted hands, flat lighting, watermark, text, cartoon, 3d render, oversaturated.»

> **لماذا يهمّ:** البرومبت القوي = توليد صحيح من أول مرة = صفر إعادة = توفير كريدت. هذا جزء من خطة `higgsfield-credit-plan.md`.
