/**
 * d4l1-capsule-engine — Capsule Generator
 * Generates draft capsules from templates — all need admin approval before publishing
 */

const { createCapsule, getScheduledDate } = require('./db');

const TEMPLATES = [
  {
    category: 'meals', emoji: '🥘',
    title_en: 'One-Pot Family Dinner',       title_ar: 'عشاء الأسرة في إناء واحد',
    subtitle_en: 'Less washing, more connecting', subtitle_ar: 'أقل غسيلاً، أكثر تواصلاً',
    body_en: 'On a busy evening, a single pot meal removes all the stress. Rice, chicken or lentils, a handful of spices — done in 30 minutes.',
    body_ar: 'في مساء مشغول، وجبة الإناء الواحد تزيل كل الضغط. أرز، دجاج أو عدس، حفنة من التوابل — وفي 30 دقيقة ينتهي الأمر.',
    tip_en: 'Prep everything before heating the pot — it feels calmer.',
    tip_ar: 'جهّز كل المكونات قبل تشغيل النار — ستشعر بهدوء أكبر.',
    tags: ['meals', 'quick-dinner', 'family'],
  },
  {
    category: 'meals', emoji: '🍳',
    title_en: 'Calm Kitchen Morning',         title_ar: 'صباح المطبخ الهادئ',
    subtitle_en: 'Start your day with intention', subtitle_ar: 'ابدأ يومك بنية',
    body_en: 'Before anyone wakes up, the kitchen is yours. A cup of tea, the smell of bread. These quiet minutes are a gift. Protect them.',
    body_ar: 'قبل أن يستيقظ أحد، المطبخ ملكك. كوب شاي، رائحة الخبز. هذه الدقائق الهادئة هديةٌ. احرص عليها.',
    tip_en: 'Prepare breakfast the night before to claim your morning silence.',
    tip_ar: 'جهّز الإفطار الليلة الماضية لتحمي صمت صباحك.',
    tags: ['meals', 'calm-kitchen', 'morning'],
  },
  {
    category: 'family', emoji: '👨‍👩‍👧',
    title_en: 'The 10-Minute Check-In',       title_ar: 'لقاء العشر دقائق',
    subtitle_en: 'No phones. Just family.',   subtitle_ar: 'بلا هواتف. فقط الأسرة.',
    body_en: 'Ask your child one question: "What made you smile today?" Then just listen. Ten minutes of real attention means more than hours of proximity.',
    body_ar: 'اسأل طفلك سؤالاً واحداً: "ما الذي أضحكك اليوم؟" ثم فقط استمع. عشر دقائق من الانتباه الحقيقي تعني أكثر من ساعات من التواجد.',
    tip_en: 'Put your phone face-down before asking.',
    tip_ar: 'ضع هاتفك وجهه للأسفل قبل أن تسأل.',
    tags: ['family', 'connection', 'kids'],
  },
  {
    category: 'family', emoji: '🌅',
    title_en: 'Morning Routine Together',     title_ar: 'روتين الصباح معاً',
    subtitle_en: 'A calm start sets the whole day', subtitle_ar: 'البداية الهادئة تصنع اليوم كله',
    body_en: 'When the morning is chaotic, everyone carries that energy all day. A simple shared ritual — even 5 minutes together before school — anchors the family.',
    body_ar: 'حين يكون الصباح فوضوياً، يحمل كل فرد تلك الطاقة طوال اليوم. طقس مشترك بسيط — حتى 5 دقائق معاً قبل المدرسة — يُثبّت الأسرة.',
    tip_en: 'Agree on one small shared morning ritual this week.',
    tip_ar: 'اتفقوا على طقس صباحي مشترك صغير هذا الأسبوع.',
    tags: ['family', 'routines', 'morning'],
  },
  {
    category: 'wellness', emoji: '🌙',
    title_en: 'Wind Down Before Sleep',       title_ar: 'التهدئة قبل النوم',
    subtitle_en: 'Your body needs a signal',  subtitle_ar: 'جسدك بحاجة لإشارة',
    body_en: 'Your nervous system needs 30 minutes to shift from day mode to sleep mode. Screens make this impossible. Replace the last 30 minutes with something soft.',
    body_ar: 'جهازك العصبي يحتاج 30 دقيقة للانتقال من وضع النهار إلى وضع النوم. الشاشات تجعل هذا مستحيلاً. استبدل آخر 30 دقيقة بشيء ناعم.',
    tip_en: 'Place your phone in another room tonight.',
    tip_ar: 'ضع هاتفك في غرفة أخرى الليلة.',
    tags: ['wellness', 'sleep'],
  },
  {
    category: 'wellness', emoji: '🌿',
    title_en: 'One Breath Reset',             title_ar: 'إعادة الضبط بنفس واحد',
    subtitle_en: 'The fastest stress tool you have', subtitle_ar: 'أسرع أداة لتخفيف الضغط لديك',
    body_en: 'When stress builds — a slow exhale (longer than the inhale) activates your parasympathetic system immediately. Just breathe out slowly for 6 seconds.',
    body_ar: 'حين يتراكم الضغط — زفير بطيء (أطول من الشهيق) ينشّط جهازك العصبي فوراً. ازفر ببطء لمدة 6 ثوانٍ.',
    tip_en: '4-count inhale, 6-count exhale. That\'s it.',
    tip_ar: 'شهيق لعدد 4، زفير لعدد 6. هذا كل شيء.',
    tags: ['wellness', 'stress-relief'],
  },
  {
    category: 'faith', emoji: '☪️',
    title_en: 'Morning Remembrance',          title_ar: 'أذكار الصباح',
    subtitle_en: 'Begin with His name',       subtitle_ar: 'ابدأ باسمه',
    body_en: 'Before the world rushes in — before the phone, before the news — say His name. A few minutes of morning dhikr sets the tone of your entire day.',
    body_ar: 'قبل أن يتدفق العالم — قبل الهاتف، قبل الأخبار — قل اسمه. دقائق قليلة من أذكار الصباح تضع نبرة يومك كله.',
    tip_en: 'Keep a printed card of morning adhkar by your bed.',
    tip_ar: 'ضع بطاقة مطبوعة بأذكار الصباح بجانب سريرك.',
    tags: ['faith', 'morning'],
  },
  {
    category: 'money', emoji: '💰',
    title_en: 'The Weekly 5-Minute Review',   title_ar: 'مراجعة الخمس دقائق الأسبوعية',
    subtitle_en: 'Know where your money went', subtitle_ar: 'اعرف أين ذهب مالك',
    body_en: 'Once a week, open your banking app and just look. No judgment — just awareness. Most overspending happens in the dark.',
    body_ar: 'مرة في الأسبوع، افتح تطبيق بنكك وانظر فقط. لا حكم على النفس — فقط الوعي. معظم الإنفاق الزائد يحدث في الظلام.',
    tip_en: 'Label one unexpected expense as "lesson" not "mistake".',
    tip_ar: 'صنّف نفقة غير متوقعة واحدة كـ"درس" لا "خطأ".',
    tags: ['money', 'budgeting'],
  },
  {
    category: 'living', emoji: '🏠',
    title_en: 'The 10-Item Reset',            title_ar: 'إعادة ضبط الـ10 أشياء',
    subtitle_en: 'A calm home in 10 minutes', subtitle_ar: 'منزل هادئ في 10 دقائق',
    body_en: 'When the house feels overwhelming, pick 10 things to put away. Just 10. Finishing a small task resets your sense of control.',
    body_ar: 'حين يبدو المنزل مرهقاً، اختر 10 أشياء لترتبها. 10 فقط. إنهاء مهمة صغيرة يُعيد إحساسك بالسيطرة.',
    tip_en: 'Do it with music on — it feels completely different.',
    tip_ar: 'افعلها مع الموسيقى — الأمر يختلف كلياً.',
    tags: ['living', 'home-reset'],
  },
];

async function generateBatch(daysAhead = 7, startDate = null) {
  const results = [];
  const base    = startDate ? new Date(startDate) : new Date();

  for (let i = 0; i < daysAhead; i++) {
    const d = new Date(base);
    d.setDate(d.getDate() + i);
    const dateStr = d.toISOString().slice(0, 10);

    const existing = await getScheduledDate(dateStr);
    if (existing) {
      results.push({ date: dateStr, skipped: true, reason: 'already scheduled' });
      continue;
    }

    const template = TEMPLATES[i % TEMPLATES.length];
    const capsule  = await createCapsule({
      ...template, scheduled_date: dateStr, status: 'draft', source: 'generator',
    });
    results.push({ date: dateStr, capsule_id: capsule.id, title: capsule.title_en });
  }
  return results;
}

async function generateOne({ date, category } = {}) {
  const pool     = category ? TEMPLATES.filter(t => t.category === category) : TEMPLATES;
  const template = pool[Math.floor(Math.random() * pool.length)];
  return createCapsule({
    ...template,
    scheduled_date: date || new Date().toISOString().slice(0, 10),
    status: 'draft', source: 'generator',
  });
}

module.exports = { generateBatch, generateOne, TEMPLATES };
