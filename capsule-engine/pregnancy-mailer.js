/**
 * Pregnancy Journey — Weekly Mailer
 *
 * Called by the cron job every Sunday at 09:00 UTC.
 * Sends each active subscriber a personalized weekly email.
 *
 * Requires env:  RESEND_API_KEY
 * Requires env:  SITE_URL  (default https://dotforlife.com)
 */

const { Resend } = require('resend');
const db = require('./db');

// Lazy init — avoids crash when RESEND_API_KEY is not yet set
function getResend() {
  if (!process.env.RESEND_API_KEY) throw new Error('RESEND_API_KEY not set');
  return new Resend(process.env.RESEND_API_KEY);
}

const SITE = (process.env.SITE_URL || 'https://dotforlife.com').replace(/\/$/, '');
const FROM = process.env.RESEND_FROM || 'Dot4Life <onboarding@resend.dev>';

// ─────────────────────────────────────────
//  WEEK DATA (mirrors pregnancy-journey.html)
//  Lightweight version — only fields needed for email
// ─────────────────────────────────────────
const WEEK_SUMMARY = [
  // 1–15 hardcoded
  { fruit:'🌱', fruitAr:'بذرة خشخاش', len:'< 1mm', wt:'< 1g',  babyAr:'البويضة المخصبة تنغرس في الرحم. الحمض النووي لطفلك محدد بالفعل.', tipAr:'كل رحلة عظيمة تبدأ بخطوة هادئة. لقد أخذتِ خطوتك.' },
  { fruit:'🌱', fruitAr:'حبة سمسم',    len:'~1mm',  wt:'< 1g',  babyAr:'الجنين يكوّن ثلاث طبقات أساسية. نبضة القلب ستبدأ قريباً.', tipAr:'جسمك يعمل بجهد أكبر مما تتخيلين، حتى لو لم تري شيئاً بعد.' },
  { fruit:'🫐', fruitAr:'حبة توت',     len:'4mm',   wt:'< 1g',  babyAr:'القلب يدق! جميع الأعضاء الرئيسية تبدأ في التطور.', tipAr:'كوني رحيمة مع نفسك. طاقتك ذاهبة لأهم مشروع في العالم.' },
  { fruit:'🫐', fruitAr:'توت العليق',  len:'1.6cm', wt:'~1g',   babyAr:'ملامح الوجه تتشكل — العينان والأذنان والأنف الصغير.', tipAr:'الموعد الأول نقطة تحول. أنتِ تبنين فريقك لهذه الرحلة.' },
  { fruit:'🍓', fruitAr:'فراولة',      len:'2.3cm', wt:'~2g',   babyAr:'أصابع اليدين والقدمين تبدأ في التشكل. الدماغ ينمو بسرعة.', tipAr:'استريحي عندما تحتاجين. لا وسام لمن تتجاهل التعب.' },
  { fruit:'🫑', fruitAr:'بازلاء',      len:'3cm',   wt:'~4g',   babyAr:'الأذنان والعينان واضحتان. الجهاز الهضمي ينمو.', tipAr:'جسمك مكرس الآن لخلق حياة. قدّري ذلك.' },
  { fruit:'🍋', fruitAr:'ليمون',       len:'4cm',   wt:'~7g',   babyAr:'بصمات الأصابع تتشكل. الغضروف يبدأ في التصلب لتكوين العظام.', tipAr:'أنتِ تفعلين شيئاً لا يفعله الجميع. تذكري ذلك.' },
  { fruit:'🥝', fruitAr:'كيوي',        len:'6cm',   wt:'~14g',  babyAr:'الطفل يستطيع سماع الأصوات الآن. تحدثي إليه.', tipAr:'تحدثي إلى طفلك. صوتك هو صوته المفضل.' },
  { fruit:'🍏', fruitAr:'تفاحة خضراء', len:'8cm',   wt:'~28g',  babyAr:'الطفل يتحرك بنشاط. قد تشعرين بأول رفرفة قريباً.', tipAr:'قد تشعرين بالطفل يتحرك قريباً — استمتعي بكل لحظة.' },
  { fruit:'🍎', fruitAr:'تفاحة',       len:'10cm',  wt:'~45g',  babyAr:'الهيكل العظمي يتصلب. تقلصات براكستون هيكس قد تبدأ.', tipAr:'أنتِ في المنتصف تقريباً. احتفلي بكم قطعتِ.' },
  { fruit:'🥑', fruitAr:'أفوكادو',     len:'12cm',  wt:'~70g',  babyAr:'الطفل يمكنه التجشؤ — ستشعرين به كرفرفة إيقاعية.', tipAr:'طفل يتجشأ بداخلك هو من أحلى الأحاسيس. استمتعي به.' },
  { fruit:'🌽', fruitAr:'ذرة',         len:'15cm',  wt:'~100g', babyAr:'الطفل يفتح ويغلق عينيه. الأظافر تنمو.', tipAr:'جسمك يحمل ثقل المستقبل. امشي برفق مع نفسك.' },
  { fruit:'🍆', fruitAr:'باذنجان',     len:'18cm',  wt:'~150g', babyAr:'جميع الحواس الخمس تتطور. الطفل يستطيع الحلم.', tipAr:'طفلك يحلم. يا له من فكر جميل تحمليه اليوم.' },
  { fruit:'🥦', fruitAr:'بروكلي',      len:'21cm',  wt:'~220g', babyAr:'الدماغ يصبح معقداً. الطفل يستجيب للضوء عبر بطنك.', tipAr:'الراحة ليست كسلاً. إنها أكثر شيء منتج الآن.' },
  { fruit:'🥥', fruitAr:'جوز هند',     len:'25cm',  wt:'~340g', babyAr:'الطفل يتدرب على التنفس. الدهون تتراكم للدفء.', tipAr:'أنتِ قريبة جداً من اللحظة التي كنتِ تنتظرينها.' },
  { fruit:'🥭', fruitAr:'مانجو',       len:'28cm',  wt:'~450g', babyAr:'الطفل يبدو بشرياً تماماً. طفلك يعرف صوتك.', tipAr:'صوتك هو صوته المفضل في العالم.' },
  { fruit:'🍍', fruitAr:'أناناس',      len:'30cm',  wt:'~600g', babyAr:'انعكاسات المص والبلع قوية. الطفل ينام 12-14 ساعة.', tipAr:'عندما تشعرين بركلة، اعلمي أن طفلك يقول مرحباً.' },
  { fruit:'🎃', fruitAr:'يقطين',       len:'33cm',  wt:'~820g', babyAr:'الدهون الجبنية تحمي الجلد. الطفل نشيط جداً.', tipAr:'طفلك يتدحرج ويمتد بداخلك، يتدرب على الحياة.' },
  { fruit:'🥕', fruitAr:'قرع العسل',   len:'35cm',  wt:'~1kg',  babyAr:'جميع الأعضاء تعمل. الطفل يتذوق ما تأكلينه.', tipAr:'كل انزعاج الآن له اسم وتاريخ. أنتِ على وشك احتضانه.' },
  { fruit:'🎋', fruitAr:'كرفس',        len:'37cm',  wt:'~1.2kg',babyAr:'الطفل يكتسب وزناً بسرعة. الرئتان تكتملان.', tipAr:'جسمك يعرف ماذا يفعل. ثقي به.' },
  // 21-40 generated
  ...Array.from({ length: 20 }, (_, i) => {
    const w = i + 21;
    const fruits = ['🥥','🍉','🎃','🥭','🍍','🥕','🎋','🍆','🌽','🥦'];
    return {
      fruit: fruits[i % fruits.length],
      fruitAr: 'في نمو مستمر',
      len: `${25 + w}cm`, wt: `~${(0.8 + i * 0.12).toFixed(1)}kg`,
      babyAr: 'طفلك يكبر ويتقوى كل يوم.',
      tipAr: 'الصبر هو قوتك العظمى الآن. أنتِ تفعلين شيئاً رائعاً.',
    };
  }),
];

// ─────────────────────────────────────────
//  NUTRITION TIPS per trimester
// ─────────────────────────────────────────
function getNutritionTips(week) {
  if (week <= 13) return [
    'حمض الفوليك 400 ميكروغرام يومياً ضروري',
    'وجبات صغيرة ومتكررة تخفف الغثيان',
    'اشربي 8-10 أكواب ماء يومياً',
  ];
  if (week <= 26) return [
    'بروتين 70-100 جرام يومياً لنمو طفلك',
    'حديد من السبانخ والعدس والتمر',
    'أوميغا-3 للدماغ — سمك، جوز، بذر كتان',
  ];
  return [
    '6 تمرات يومياً — ثبت علمياً أنها تسهل الولادة',
    'كالسيوم وفيتامين D للعظام في الأشهر الأخيرة',
    'وجبات خفيفة فقط — المعدة مضغوطة',
  ];
}

// ─────────────────────────────────────────
//  HTML EMAIL TEMPLATE
// ─────────────────────────────────────────
function buildEmail({ name, babyName, week, dueDate, token, unsubToken }) {
  const d     = WEEK_SUMMARY[week - 1] || WEEK_SUMMARY[19];
  const tips  = getNutritionTips(week);
  const pageUrl = `${SITE}/pregnancy-journey.html?token=${token}`;
  const unsubUrl = `${SITE.replace('dotforlife.com', 'dot4life-production.up.railway.app')}/api/pregnancy/unsubscribe/${unsubToken}`;

  const trimester = week <= 13 ? 'الثلث الأول'
                  : week <= 26 ? 'الثلث الثاني'
                  : 'الثلث الثالث';

  const greeting = babyName
    ? `أنتِ وصغيرتك ${babyName}`
    : `عزيزتي ${name}`;

  return `<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>رحلة الحمل — الأسبوع ${week}</title>
</head>
<body style="margin:0;padding:0;background:#FAF8F4;font-family:'Segoe UI',Tahoma,Arial,sans-serif;color:#1A1410">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#FAF8F4;padding:32px 16px">
  <tr><td align="center">
  <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">

    <!-- HEADER -->
    <tr>
      <td style="background:linear-gradient(135deg,#FDF8F2 0%,#F5EBD8 100%);border-radius:20px 20px 0 0;padding:40px 40px 32px;text-align:center;border:1px solid #E0D8CC;border-bottom:none">
        <div style="font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#C8706A;margin-bottom:12px">Dot4Life · رحلة الحمل</div>
        <div style="font-size:42px;margin-bottom:8px">${d.fruit}</div>
        <h1 style="margin:0 0 6px;font-size:28px;font-weight:700;color:#1A1410">الأسبوع ${week}</h1>
        <div style="font-size:13px;color:#9A9188;letter-spacing:.06em">${trimester}</div>
      </td>
    </tr>

    <!-- GREETING -->
    <tr>
      <td style="background:#FFFFFF;padding:28px 40px 24px;border-right:1px solid #E0D8CC;border-left:1px solid #E0D8CC">
        <p style="margin:0;font-size:16px;line-height:1.7;color:#1A1410">
          ${greeting}، 🌸<br/>
          هذا الأسبوع طفلك بحجم <strong>${d.fruitAr}</strong> — طوله <strong>${d.len}</strong> ووزنه حوالي <strong>${d.wt}</strong>.
        </p>
      </td>
    </tr>

    <!-- BABY THIS WEEK -->
    <tr>
      <td style="background:#FFFFFF;padding:0 40px 24px;border-right:1px solid #E0D8CC;border-left:1px solid #E0D8CC">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="background:#FDF8F2;border-radius:12px;padding:20px 24px;border:1px solid #EDE6D8">
              <div style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#B8861A;margin-bottom:8px">🌱 طفلك هذا الأسبوع</div>
              <p style="margin:0;font-size:14px;line-height:1.8;color:#3A3228">${d.babyAr}</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- NUTRITION -->
    <tr>
      <td style="background:#FFFFFF;padding:0 40px 24px;border-right:1px solid #E0D8CC;border-left:1px solid #E0D8CC">
        <div style="font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#1B7A4E;margin-bottom:12px">🥗 تغذية هذا الأسبوع</div>
        ${tips.map(t => `
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:8px">
          <tr>
            <td width="6" style="background:#1B7A4E;border-radius:3px">&nbsp;</td>
            <td style="padding-right:12px;font-size:13px;line-height:1.6;color:#3A3228">${t}</td>
          </tr>
        </table>`).join('')}
      </td>
    </tr>

    <!-- TIP -->
    <tr>
      <td style="background:#FFFFFF;padding:0 40px 32px;border-right:1px solid #E0D8CC;border-left:1px solid #E0D8CC">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="background:#FEF9F0;border-radius:12px;padding:20px 24px;border:1px solid #F0E4C8;text-align:center">
              <div style="font-size:20px;margin-bottom:8px">💛</div>
              <p style="margin:0;font-size:14px;line-height:1.8;color:#5C534A;font-style:italic">"${d.tipAr}"</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- CTA -->
    <tr>
      <td style="background:#FFFFFF;padding:0 40px 40px;border-right:1px solid #E0D8CC;border-left:1px solid #E0D8CC;text-align:center">
        <a href="${pageUrl}"
           style="display:inline-block;background:#B8861A;color:#FFFFFF;text-decoration:none;font-size:15px;font-weight:600;padding:14px 36px;border-radius:10px;letter-spacing:.04em">
          افتحي صفحتك الكاملة لهذا الأسبوع ←
        </a>
        <p style="margin:16px 0 0;font-size:12px;color:#9A9188">
          يمكنك حفظ هذا الرابط للعودة إليه في أي وقت
        </p>
      </td>
    </tr>

    <!-- FOOTER -->
    <tr>
      <td style="background:#F5F0E8;border-radius:0 0 20px 20px;padding:24px 40px;text-align:center;border:1px solid #E0D8CC;border-top:none">
        <p style="margin:0 0 8px;font-size:12px;color:#9A9188">
          أنتِ تتلقين هذه الرسالة لأنك سجّلتِ في رحلة الحمل على
          <a href="${SITE}" style="color:#B8861A;text-decoration:none">dotforlife.com</a>
        </p>
        <p style="margin:0;font-size:12px">
          <a href="${unsubUrl}" style="color:#C8706A;text-decoration:none">إلغاء الاشتراك</a>
        </p>
      </td>
    </tr>

  </table>
  </td></tr>
  </table>

</body>
</html>`;
}

// ─────────────────────────────────────────
//  SEND ONE EMAIL
// ─────────────────────────────────────────
async function sendWeeklyEmail(subscriber) {
  const week = db.calcWeekFromDue(subscriber.due_date);

  // Don't resend same week
  if (subscriber.last_week_sent === week) {
    console.log(`[mailer] Skip ${subscriber.email} — already sent week ${week}`);
    return { skipped: true };
  }

  const html = buildEmail({
    name:       subscriber.name,
    babyName:   subscriber.baby_name,
    week,
    dueDate:    subscriber.due_date,
    token:      subscriber.token,
    unsubToken: subscriber.unsubscribe_token,
  });

  const subject = subscriber.baby_name
    ? `${subscriber.baby_name} في الأسبوع ${week} 🌸 — رحلة الحمل`
    : `أنتِ في الأسبوع ${week} من حملك 🌸`;

  try {
    const result = await getResend().emails.send({
      from:    FROM,
      to:      subscriber.email,
      subject,
      html,
    });
    await db.pjMarkSent(subscriber.id, week);
    console.log(`[mailer] ✓ Sent to ${subscriber.email} week ${week} — id: ${result.data?.id}`);
    return { ok: true, week };
  } catch (err) {
    console.error(`[mailer] ✗ Failed ${subscriber.email}:`, err.message);
    return { ok: false, error: err.message };
  }
}

// ─────────────────────────────────────────
//  SEND ALL ACTIVE SUBSCRIBERS
// ─────────────────────────────────────────
async function sendWeeklyToAll() {
  if (!process.env.RESEND_API_KEY) {
    console.warn('[mailer] RESEND_API_KEY not set — skipping');
    return;
  }
  const subscribers = await db.pjGetActiveSubscribers();
  console.log(`[mailer] Starting weekly run — ${subscribers.length} subscribers`);

  let sent = 0, skipped = 0, failed = 0;
  for (const sub of subscribers) {
    const result = await sendWeeklyEmail(sub);
    if (result?.ok)      sent++;
    else if (result?.skipped) skipped++;
    else                 failed++;
    // Small delay between sends to be polite
    await new Promise(r => setTimeout(r, 300));
  }
  console.log(`[mailer] Done — sent:${sent} skipped:${skipped} failed:${failed}`);
}

// ─────────────────────────────────────────
//  WELCOME EMAIL (sent immediately on register)
// ─────────────────────────────────────────
async function sendWelcomeEmail(subscriber) {
  if (!process.env.RESEND_API_KEY) return;

  const week    = db.calcWeekFromDue(subscriber.due_date);
  const pageUrl = `${SITE}/pregnancy-journey.html?token=${subscriber.token}`;
  const unsubUrl = `${SITE.replace('dotforlife.com', 'dot4life-production.up.railway.app')}/api/pregnancy/unsubscribe/${subscriber.unsubscribe_token}`;
  const greeting = subscriber.baby_name
    ? `أهلاً ${subscriber.name} 🌸 ومرحباً بـ${subscriber.baby_name}`
    : `أهلاً ${subscriber.name} 🌸`;

  const html = `<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"/><title>مرحباً برحلتك</title></head>
<body style="margin:0;padding:0;background:#FAF8F4;font-family:'Segoe UI',Tahoma,Arial,sans-serif;color:#1A1410">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#FAF8F4;padding:32px 16px">
  <tr><td align="center">
  <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%">

    <tr>
      <td style="background:linear-gradient(135deg,#FDF8F2 0%,#F5EBD8 100%);border-radius:20px 20px 0 0;padding:40px;text-align:center;border:1px solid #E0D8CC;border-bottom:none">
        <div style="font-size:48px;margin-bottom:12px">🌱</div>
        <div style="font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#C8706A;margin-bottom:8px">Dot4Life · رحلة الحمل</div>
        <h1 style="margin:0 0 8px;font-size:26px;font-weight:700;color:#1A1410">رحلتك بدأت!</h1>
        <div style="font-size:14px;color:#9A9188">الأسبوع ${week} من أصل 40</div>
      </td>
    </tr>

    <tr>
      <td style="background:#FFFFFF;padding:32px 40px;border-right:1px solid #E0D8CC;border-left:1px solid #E0D8CC">
        <p style="margin:0 0 16px;font-size:16px;line-height:1.8">${greeting}</p>
        <p style="margin:0 0 24px;font-size:14px;line-height:1.8;color:#5C534A">
          تم تسجيلك بنجاح في رحلة الحمل على Dot4Life.<br/>
          سيصلك كل <strong>أحد</strong> بريد مخصص لك يحمل تفاصيل أسبوعك الجديد — حجم طفلك، تطوره، نصائح التغذية، وتذكيرة الأسبوع.
        </p>
        <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:24px">
          <tr>
            <td style="background:#FDF8F2;border-radius:12px;padding:20px 24px;border:1px solid #EDE6D8;text-align:center">
              <div style="font-size:13px;color:#9A9188;margin-bottom:6px">رابطك الشخصي — احفظيه</div>
              <a href="${pageUrl}" style="color:#B8861A;font-size:13px;word-break:break-all">${pageUrl}</a>
              <div style="font-size:12px;color:#9A9188;margin-top:6px">يفتح صفحتك دائماً على أسبوعك الحالي</div>
            </td>
          </tr>
        </table>
        <div style="text-align:center">
          <a href="${pageUrl}" style="display:inline-block;background:#C8706A;color:#FFFFFF;text-decoration:none;font-size:15px;font-weight:600;padding:14px 36px;border-radius:10px">
            افتحي صفحتك الآن ←
          </a>
        </div>
      </td>
    </tr>

    <tr>
      <td style="background:#F5F0E8;border-radius:0 0 20px 20px;padding:20px 40px;text-align:center;border:1px solid #E0D8CC;border-top:none">
        <p style="margin:0;font-size:12px;color:#9A9188">
          <a href="${unsubUrl}" style="color:#C8706A;text-decoration:none">إلغاء الاشتراك</a>
          &nbsp;·&nbsp;
          <a href="${SITE}" style="color:#B8861A;text-decoration:none">dotforlife.com</a>
        </p>
      </td>
    </tr>

  </table>
  </td></tr>
  </table>
</body></html>`;

  try {
    const result = await getResend().emails.send({
      from:    FROM,
      to:      subscriber.email,
      subject: `مرحباً ${subscriber.name} 🌱 — رحلة الحمل بدأت!`,
      html,
    });
    if (result.error) {
      console.error(`[mailer] ✗ Welcome email Resend error:`, JSON.stringify(result.error));
    } else {
      console.log(`[mailer] ✓ Welcome email sent to ${subscriber.email} — id: ${result.data?.id}`);
    }
    return result;
  } catch (err) {
    console.error(`[mailer] ✗ Welcome email failed:`, err.message);
    return { error: { message: err.message } };
  }
}

module.exports = { sendWeeklyToAll, sendWeeklyEmail, sendWelcomeEmail, buildEmail };
