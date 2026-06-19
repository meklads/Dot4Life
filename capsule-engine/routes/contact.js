/**
 * Contact Form Route
 * POST /api/contact — receives form data and emails it via Resend
 */

const express = require('express');
const router  = express.Router();

function getResend() {
  const { Resend } = require('resend');
  if (!process.env.RESEND_API_KEY) throw new Error('RESEND_API_KEY not set');
  return new Resend(process.env.RESEND_API_KEY);
}

router.post('/', async (req, res) => {
  try {
    const { name, email, subject, message } = req.body;

    if (!name || !email || !message)
      return res.status(400).json({ error: 'name, email, message are required' });

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      return res.status(400).json({ error: 'Invalid email address' });

    const TO   = process.env.CONTACT_EMAIL || 'dotforlife3@gmail.com';
    const FROM = process.env.RESEND_FROM   || 'Dot4Life <journey@dotforlife.com>';

    const result = await getResend().emails.send({
      from:     FROM,
      to:       TO,
      reply_to: email,
      subject:  `[Dot4Life Contact] ${subject || 'رسالة جديدة'}`,
      html: `
        <div dir="rtl" style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#FAF8F4;padding:32px;border-radius:16px">
          <div style="background:#fff;border:1px solid #E0D8CC;border-radius:12px;padding:28px">
            <div style="font-size:12px;font-weight:700;letter-spacing:.12em;color:#C8706A;margin-bottom:16px">DOT4LIFE · رسالة تواصل</div>
            <h2 style="margin:0 0 20px;font-size:20px;color:#1A1410">${subject || 'رسالة جديدة'}</h2>
            <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
              <tr>
                <td style="padding:8px 12px;background:#F5F0E8;border-radius:6px 0 0 6px;font-size:13px;color:#9A9188;width:100px">الاسم</td>
                <td style="padding:8px 12px;font-size:14px;color:#1A1410">${name}</td>
              </tr>
              <tr>
                <td style="padding:8px 12px;background:#F5F0E8;border-radius:6px 0 0 6px;font-size:13px;color:#9A9188">البريد</td>
                <td style="padding:8px 12px;font-size:14px;color:#1A1410"><a href="mailto:${email}" style="color:#B8861A">${email}</a></td>
              </tr>
            </table>
            <div style="background:#F5F0E8;border-radius:8px;padding:16px 20px">
              <div style="font-size:13px;color:#9A9188;margin-bottom:8px">الرسالة</div>
              <div style="font-size:14px;line-height:1.8;color:#1A1410;white-space:pre-wrap">${message}</div>
            </div>
          </div>
          <div style="text-align:center;margin-top:16px;font-size:12px;color:#9A9188">dotforlife.com</div>
        </div>
      `,
    });

    if (result.error) {
      console.error('[contact] Resend error:', JSON.stringify(result.error));
      return res.status(500).json({ error: 'Failed to send email' });
    }

    console.log(`[contact] ✓ Message from ${email} — id: ${result.data?.id}`);

    // Send thank-you email to sender
    await getResend().emails.send({
      from:    FROM,
      to:      email,
      subject: `شكراً على تواصلك مع Dot4Life 🌿`,
      html: `
        <div dir="rtl" style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;background:#FAF8F4;padding:32px;border-radius:16px">
          <div style="background:#fff;border:1px solid #E0D8CC;border-radius:12px;padding:32px;text-align:center">
            <div style="font-size:42px;margin-bottom:12px">🌿</div>
            <div style="font-size:12px;font-weight:700;letter-spacing:.14em;color:#C8706A;margin-bottom:8px">DOT4LIFE</div>
            <h2 style="margin:0 0 16px;font-size:22px;color:#1A1410">شكراً على رسالتك، ${name}</h2>
            <p style="font-size:14px;line-height:1.8;color:#5C534A;margin:0 0 24px">
              وصلتنا رسالتك بخصوص <strong>${subject || 'استفسار عام'}</strong>.<br/>
              سنراجعها ونرد عليك في أقرب وقت ممكن.
            </p>
            <div style="background:#F5F0E8;border-radius:8px;padding:16px 20px;text-align:right;margin-bottom:24px">
              <div style="font-size:12px;color:#9A9188;margin-bottom:6px">رسالتك</div>
              <div style="font-size:13px;line-height:1.7;color:#1A1410;white-space:pre-wrap">${message}</div>
            </div>
            <a href="https://dotforlife.com" style="display:inline-block;background:#C8706A;color:#fff;text-decoration:none;font-size:14px;font-weight:600;padding:12px 32px;border-radius:8px">
              العودة للموقع ←
            </a>
          </div>
          <div style="text-align:center;margin-top:16px;font-size:12px;color:#9A9188">
            dotforlife.com · الرفيق اليومي الموثوق لكل أسرة
          </div>
        </div>
      `,
    }).catch(err => console.error('[contact] thank-you email failed:', err.message));

    res.json({ ok: true });

  } catch (err) {
    console.error('[contact] error:', err.message);
    res.status(500).json({ error: 'Server error' });
  }
});

module.exports = router;
