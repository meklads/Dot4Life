# Ideogram prompts — Recipe hero images (v2, rewritten by Amer 2026-07-09)

## لماذا أُعيدت الكتابة

الملف السابق كان منظّماً كـ"40 برومبت" (10 لكل فئة × 4 فئات: حمل/اقتصادي/سريع/عائلي). هذا خاطئ بنيوياً:

1. **كل وصفة صورتها واحدة تُستخدم أينما ظهرت.** الوصفة الواحدة (مثل `avocado-egg-toast`) تظهر في أكثر من فئة (حمل + سريع مثلاً) عبر حقل `image` في `recipes.json` — فلا داعي لتوليد صورتين مختلفتين لنفس الطبق. العدد الحقيقي المطلوب = **16 صورة فقط** (عدد ملفات الوصفات الفعلية)، وليس 40. هذا يوفّر أكثر من النصف من تكلفة/وقت التوليد، ويضمن تناسق بصري (نفس الطبق = نفس الصورة في كل مكان يظهر فيه).
2. **الصورة الواحدة يجب أن تكون لقطة واحدة كبيرة، لا شبكة لقطات.** لقطة الشاشة التي أرسلتها (10 صور صغيرة في شبكة) هي على الأرجح **معاينة دفعة (contact sheet)** يعرضها أداة التوليد قبل الاختيار — وليست الملف النهائي. الملف النهائي حسب قاعدة التسمية أدناه هو صورة واحدة كاملة الإطار لكل وصفة، لقطة مغرية للطبق نفسه، بلا تجميع.
3. **التسمية يجب أن تُطابق slug الملف مباشرة** حتى لا يحدث خلط — كل صف في الجدول أدناه يحدد الاسم الدقيق للملف الناتج.

---

## القاعدة العامة (Global style — تُضاف تلقائياً لكل برومبت)

> Soft natural daylight, appetizing food photography, shallow depth of field, warm teal and cream tones, clean modern Gulf family kitchen setting, minimal props, single dish as the hero subject filling most of the frame, 16:9, high detail.

**سلبيات إلزامية (negative / exclude) على كل صورة:**
> No text, no watermark, no logos, no human faces or hands, no alcohol, no pork or pork-derived ingredients, no wine glasses or bar-style props, no collage/grid/multi-panel layout — single full-frame photo only.

**الزاوية الافتراضية:** تصوير علوي (flat-lay) للأطباق المسطحة/الصحون/الأوعية، وزاوية 45° للأطباق ذات العمق (يخنات، أوعية عالية، مقالٍ). محدَّدة لكل صف أدناه.

---

## جدول الصور — 16 وصفة (تطابق 1:1 مع ملفات `library/recipes/*.html`)

| # | Slug (اسم الملف) | العنوان | الزاوية | البرومبت |
|---|---|---|---|---|
| 1 | `avocado-egg-toast` | Avocado Egg Toast | علوي 45° | Whole-grain toast topped with mashed avocado and a soft boiled egg halved on top, sprinkled chili flakes and sesame, small ceramic plate |
| 2 | `baked-salmon-veg` | Baked Salmon with Vegetables | علوي (sheet-pan) | Baked salmon fillet fresh from the oven on a sheet pan with roasted zucchini, carrot rounds, and lemon slices, glossy skin, steam visible |
| 3 | `chicken-shawarma-bowl` | Home Chicken Shawarma Bowl | 45° | Sliced spiced chicken shawarma over rice in a wide bowl, pickles, tomato, and tahini drizzle on top, vibrant colors |
| 4 | `chickpea-rice-bowl` | Chickpea Rice Bowl | علوي | Chickpea and rice bowl with sautéed onions and tomatoes, fresh parsley garnish, rustic wooden table |
| 5 | `date-nut-smoothie` | Date Nut Smoothie | مستوى العين (glass) | Date and nut smoothie in a tall glass with a light yogurt swirl on top, banana slice garnish, condensation on glass, bright morning light |
| 6 | `egg-tomato-skillet` | Egg Tomato Skillet | 45° | Eggs poached in a rustic tomato and pepper sauce in a cast iron skillet, fresh parsley on top, gentle steam rising |
| 7 | `family-vegetable-stew` | Family Vegetable Stew | 45° | Mild vegetable stew with potatoes, carrots, and zucchini in a large deep serving bowl, fresh herbs on top, gentle warm color |
| 8 | `friday-family-pasta` | Friday Family Pasta | علوي (large dish) | Large family-size serving dish of pasta in tomato-carrot sauce, grated cheese dusted on top, wooden table, shared-meal framing |
| 9 | `grilled-chicken-salad` | Grilled Chicken Family Salad | علوي | Grilled chicken slices fanned over a large salad platter with lettuce, cucumber, and tomato, lemon wedge, light dressing sheen |
| 10 | `iron-oats-breakfast` | Iron-Rich Oats Breakfast | علوي | Warm bowl of oatmeal topped with chopped dates, walnuts, and chia seeds, wooden spoon resting beside the bowl, soft morning light |
| 11 | `lentil-koshari-bowl` | Lentil Koshari Bowl | علوي | Koshari-style bowl with rice, lentils, and pasta topped with deeply caramelized onions and tangy tomato sauce drizzle |
| 12 | `lentil-spinach-soup` | Lentil & Spinach Soup | علوي (bowl) | Creamy red lentil and spinach soup in a deep bowl, lemon wedge on the side, visible steam, rustic linen napkin |
| 13 | `one-pot-chicken-rice` | One-Pot Chicken Rice | 45° (large pot) | Golden roasted chicken thighs over spiced rice in a large family pot, cardamom pods visible, Friday-dinner mood |
| 14 | `tuna-wrap-quick` | 5-Minute Tuna Wrap | 45° | Tuna wrap rolled tightly in flatbread with lettuce and cucumber, cut in half showing the filling, quick lunch styling |
| 15 | `veg-pasta-budget` | Budget Vegetable Pasta | علوي | Simple vegetable pasta with frozen mixed vegetables in tomato sauce on a plain white plate, everyday family-portion styling |
| 16 | `yogurt-fruit-parfait` | Yogurt Fruit Parfait | مستوى العين (glass) | Yogurt parfait layered in a clear glass cup with mixed berries and granola, visible distinct layers, fresh natural light |

---

## سير العمل بعد التوليد

1. لكل صف: ولّد صورة واحدة فقط (وليس دفعة/شبكة) — إن أعادت الأداة معاينة شبكية، اختر أفضل لقطة واحدة منها وصدّرها فرداً.
2. صدّر بصيغة **WebP، نسبة 16:9**.
3. احفظ في `assets/images/recipes/` باسم: `hero-{slug}.webp` (مثال: `hero-iron-oats-breakfast.webp`).
4. حدّث حقل `image` في `library/recipes/recipes.json` لكل وصفة (استبدال `placeholder.svg`).
5. شغّل: `python3 scripts/build_recipes.py`
6. تحقق: لا نص/علامة مائية داخل الصورة، لا شبكة/تجميع، الطبق يملأ معظم الإطار.

**ملاحظة:** `tuna-wrap-quick` و`veg-pasta-budget` وصفتان قديمتان لم تُشملا بعد بدفعة Recipe schema (JSON-LD) — هذا خارج نطاق مهمة الصور، سيُعالَج في دفعة منفصلة لاحقاً إن أردت.
