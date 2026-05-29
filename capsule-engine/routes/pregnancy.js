/**
 * Pregnancy Journey — Subscriber Routes
 *
 * POST /api/pregnancy/subscribe    — register new subscriber
 * GET  /api/pregnancy/me/:token    — get personalized week data
 * GET  /api/pregnancy/unsubscribe/:token — unsubscribe
 */

const express = require('express');
const router  = express.Router();
const db      = require('../db');
const { sendWelcomeEmail } = require('../pregnancy-mailer');

// ─────────────────────────────────────────
//  POST /api/pregnancy/subscribe
// ─────────────────────────────────────────
router.post('/subscribe', async (req, res) => {
  try {
    const { name, email, due_date, baby_name } = req.body;

    if (!name || !email || !due_date)
      return res.status(400).json({ error: 'name, email, due_date are required' });

    // Basic email validation
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      return res.status(400).json({ error: 'Invalid email address' });

    // Basic date validation
    const dueD = new Date(due_date);
    if (isNaN(dueD.getTime()))
      return res.status(400).json({ error: 'Invalid due_date' });

    const { token, isNew } = await db.pjSubscribe({ name, email, due_date, baby_name });
    const currentWeek = db.calcWeekFromDue(due_date);

    // Send welcome email immediately (non-blocking)
    if (isNew) {
      const sub = await db.pjGetByToken(token);
      sendWelcomeEmail(sub).catch(err =>
        console.error('[pregnancy/subscribe] welcome email failed:', err.message)
      );
    }

    res.json({
      ok: true,
      isNew,
      token,
      currentWeek,
      message: isNew ? 'subscribed' : 'already_subscribed',
      url: `/pregnancy-journey.html?token=${token}`,
    });
  } catch (err) {
    console.error('[pregnancy/subscribe]', err.message);
    res.status(500).json({ error: 'Server error' });
  }
});

// ─────────────────────────────────────────
//  GET /api/pregnancy/me/:token
// ─────────────────────────────────────────
router.get('/me/:token', async (req, res) => {
  try {
    const sub = await db.pjGetByToken(req.params.token);
    if (!sub) return res.status(404).json({ error: 'Not found or unsubscribed' });

    const currentWeek = db.calcWeekFromDue(sub.due_date);
    res.json({
      name:        sub.name,
      babyName:    sub.baby_name,
      dueDate:     sub.due_date,
      currentWeek,
      subscribedAt: sub.subscribed_at,
    });
  } catch (err) {
    console.error('[pregnancy/me]', err.message);
    res.status(500).json({ error: 'Server error' });
  }
});

// ─────────────────────────────────────────
//  GET /api/pregnancy/unsubscribe/:token
// ─────────────────────────────────────────
router.get('/unsubscribe/:token', async (req, res) => {
  try {
    await db.pjUnsubscribe(req.params.token);
    // Return simple HTML page
    res.send(`<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head><meta charset="UTF-8"><title>إلغاء الاشتراك</title>
<style>
  body{font-family:'Segoe UI',sans-serif;background:#FAF8F4;display:flex;align-items:center;
       justify-content:center;min-height:100vh;margin:0;color:#1A1410}
  .box{background:#fff;border:1px solid #E0D8CC;border-radius:16px;padding:48px;text-align:center;max-width:400px}
  h2{font-size:1.5rem;margin-bottom:12px}
  p{color:#5C534A;font-size:.95rem;line-height:1.7}
  a{color:#B8861A;text-decoration:none}
</style></head>
<body>
  <div class="box">
    <div style="font-size:2rem;margin-bottom:16px">🌿</div>
    <h2>تم إلغاء الاشتراك</h2>
    <p>لن تصلك رسائل رحلة الحمل بعد الآن.<br>يمكنك التسجيل مجدداً في أي وقت.</p>
    <p style="margin-top:24px"><a href="/pregnancy-journey.html">← العودة لصفحة الرحلة</a></p>
  </div>
</body></html>`);
  } catch (err) {
    console.error('[pregnancy/unsubscribe]', err.message);
    res.status(500).send('Error processing unsubscribe');
  }
});

// ─────────────────────────────────────────
//  GET /api/pregnancy/test-email
//  Diagnostic: sends a real test email and returns Resend response
// ─────────────────────────────────────────
router.get('/test-email', async (req, res) => {
  const to = req.query.to || 'radwan3@gmail.com';
  const key = process.env.RESEND_API_KEY;

  if (!key) {
    return res.status(500).json({ ok: false, error: 'RESEND_API_KEY is not set in environment' });
  }

  // Show first/last 4 chars of the key for verification without exposing it fully
  const keyPreview = key.slice(0, 6) + '...' + key.slice(-4);

  try {
    const { Resend } = require('resend');
    const resend = new Resend(key);

    const result = await resend.emails.send({
      from: 'onboarding@resend.dev',
      to,
      subject: '✅ Dot4Life — اختبار Resend',
      html: `<p dir="rtl">هذا بريد تجريبي للتحقق من اتصال Resend بـ Railway.<br>إذا وصلك هذا الإيميل، فكل شيء يعمل ✅</p>
             <p style="color:#888;font-size:12px">Key used: ${keyPreview}</p>`,
    });

    console.log('[test-email] Resend response:', JSON.stringify(result));
    res.json({ ok: true, to, keyPreview, resendResponse: result });
  } catch (err) {
    console.error('[test-email] error:', err.message);
    res.status(500).json({ ok: false, error: err.message, keyPreview });
  }
});

module.exports = router;
