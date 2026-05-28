/**
 * d4l1-capsule-engine — Seed Script
 * node seed.js
 */

const { initSchema, createCapsule, submitForReview, pool } = require('./db');

async function main() {
  await initSchema();
  console.log('🌱 Seeding d4l1-capsule-engine...\n');

  const today = new Date();
  const samples = [
    { category:'meals',   emoji:'🥘', title_en:'One-Pot Family Dinner',     title_ar:'عشاء الأسرة في إناء واحد',     subtitle_en:'Less washing, more connecting', subtitle_ar:'أقل غسيلاً، أكثر تواصلاً', body_en:'On a busy evening, a single pot meal removes all the stress. Done in 30 minutes.', body_ar:'في مساء مشغول، وجبة الإناء الواحد تزيل كل الضغط. في 30 دقيقة ينتهي الأمر.', tip_en:'Prep everything before heating the pot.', tip_ar:'جهّز المكونات قبل تشغيل النار.', tags:['meals'] },
    { category:'family',  emoji:'👨‍👩‍👧', title_en:'The 10-Minute Check-In',   title_ar:'لقاء العشر دقائق',            subtitle_en:'No phones. Just family.',       subtitle_ar:'بلا هواتف. فقط الأسرة.',   body_en:'Ask your child: "What made you smile today?" Then just listen.',                body_ar:'اسأل طفلك: "ما الذي أضحكك اليوم؟" ثم فقط استمع.',                           tip_en:'Put your phone face-down before asking.', tip_ar:'ضع هاتفك وجهه للأسفل.', tags:['family'] },
    { category:'wellness',emoji:'🌙', title_en:'Wind Down Before Sleep',    title_ar:'التهدئة قبل النوم',            subtitle_en:'Your body needs a signal',      subtitle_ar:'جسدك بحاجة لإشارة',        body_en:'Replace the last 30 minutes before sleep with something soft.',                body_ar:'استبدل آخر 30 دقيقة قبل النوم بشيء ناعم.',                                    tip_en:'Place your phone in another room tonight.', tip_ar:'ضع هاتفك في غرفة أخرى الليلة.', tags:['wellness'] },
    { category:'faith',   emoji:'☪️', title_en:'Morning Remembrance',       title_ar:'أذكار الصباح',                 subtitle_en:'Begin with His name',           subtitle_ar:'ابدأ باسمه',               body_en:'A few minutes of morning dhikr sets the tone of your entire day.',              body_ar:'دقائق قليلة من أذكار الصباح تضع نبرة يومك كله.',                              tip_en:'Keep morning adhkar by your bed.', tip_ar:'ضع أذكار الصباح بجانب سريرك.', tags:['faith'] },
    { category:'money',   emoji:'💰', title_en:'The Weekly 5-Minute Review', title_ar:'مراجعة الخمس دقائق الأسبوعية', subtitle_en:'Know where your money went',    subtitle_ar:'اعرف أين ذهب مالك',        body_en:'Once a week, open your banking app and just look — no judgment.',               body_ar:'مرة في الأسبوع، افتح تطبيق بنكك وانظر فقط — بلا حكم.',                       tip_en:'Label one expense as "lesson", not "mistake".', tip_ar:'صنّف نفقة واحدة كـ"درس".', tags:['money'] },
    { category:'living',  emoji:'🏠', title_en:'The 10-Item Reset',          title_ar:'إعادة ضبط الـ10 أشياء',       subtitle_en:'A calm home in 10 minutes',     subtitle_ar:'منزل هادئ في 10 دقائق',    body_en:'When the house feels overwhelming, pick 10 things to put away. Just 10.',      body_ar:'حين يبدو المنزل مرهقاً، اختر 10 أشياء لترتبها. 10 فقط.',                     tip_en:'Do it with music on.', tip_ar:'افعلها مع الموسيقى.', tags:['living'] },
    { category:'wellness',emoji:'🌿', title_en:'One Breath Reset',           title_ar:'إعادة الضبط بنفس واحد',       subtitle_en:'The fastest stress tool you have', subtitle_ar:'أسرع أداة لتخفيف الضغط', body_en:'A slow exhale (longer than the inhale) activates your calm response instantly.', body_ar:'زفير بطيء (أطول من الشهيق) ينشّط استجابة الهدوء فوراً.',                     tip_en:'4-count inhale, 6-count exhale.', tip_ar:'شهيق لعدد 4، زفير لعدد 6.', tags:['wellness'] },
  ];

  for (let i = 0; i < samples.length; i++) {
    const d = new Date(today);
    d.setDate(d.getDate() + i);
    const dateStr = d.toISOString().slice(0, 10);
    const capsule = await createCapsule({ ...samples[i], scheduled_date: dateStr, source: 'seed' });
    console.log(`  ✓ [${capsule.id}] ${capsule.title_en} (${dateStr})`);
    await submitForReview(capsule.id);
    console.log(`    → Submitted for review`);
  }

  console.log(`\n🌱 Done. Open admin dashboard → Pending Review → Approve → Publish\n`);
  await pool.end();
}

main().catch(err => {
  console.error('[SEED ERROR]', err.message);
  process.exit(1);
});
