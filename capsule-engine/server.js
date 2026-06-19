/**
 * d4l1-capsule-engine — Main Server
 * Listens immediately (Railway healthcheck), then connects to Postgres with retries.
 */

const express = require('express');
const cors    = require('cors');
const cron    = require('node-cron');
const config  = require('./config');
const { initSchema, submitForReview, publishCapsule, getScheduledDate } = require('./db');
const { sendWeeklyToAll } = require('./pregnancy-mailer');
const { generateOne } = require('./generator');

const app = express();
let dbReady = false;

app.use(cors({ origin: config.CORS_ORIGINS, credentials: true }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use((req, _res, next) => {
  const ts = new Date().toISOString().slice(11, 19);
  console.log(`[${ts}] ${req.method} ${req.path}`);
  next();
});

app.get('/', (_req, res) => res.json({
  system: 'd4l1-capsule-engine',
  version: '1.1.0',
  status: dbReady ? 'running' : 'starting',
  db: dbReady ? 'connected' : 'connecting',
  endpoints: {
    public: '/api/capsule/today | /api/capsule/health',
    admin: '/api/admin/login | /api/admin/capsules',
    pregnancy: '/api/pregnancy/subscribe | /api/pregnancy/me/:token',
  },
}));

app.use('/api/capsule', require('./routes/public'));
app.use('/api/admin', require('./routes/admin'));
app.use('/api/pregnancy', require('./routes/pregnancy'));
app.use('/api/contact', require('./routes/contact'));

app.use((_req, res) => res.status(404).json({ error: 'Not found' }));
app.use((err, _req, res, _next) => {
  console.error('[ERROR]', err.message);
  res.status(500).json({ error: err.message });
});

const PORT = config.PORT;

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function startCrons() {
  cron.schedule('0 1 * * *', async () => {
    try {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const dateStr = tomorrow.toISOString().slice(0, 10);
      const existing = await getScheduledDate(dateStr);
      if (existing) return;
      const capsule = await generateOne({ date: dateStr });
      await submitForReview(capsule.id);
      console.log(`[cron] Generated: ${capsule.title_en} (${dateStr})`);
    } catch (err) {
      console.error('[cron] Generation error:', err.message);
    }
  }, { timezone: 'UTC' });

  cron.schedule('0 2 * * 6', async () => {
    try {
      let n = 0;
      for (let i = 0; i < 7; i++) {
        const d = new Date();
        d.setDate(d.getDate() + i);
        const dateStr = d.toISOString().slice(0, 10);
        if (await getScheduledDate(dateStr)) continue;
        const capsule = await generateOne({ date: dateStr });
        await submitForReview(capsule.id);
        n++;
      }
      console.log(`[cron] Week batch: ${n} generated`);
    } catch (err) {
      console.error('[cron] Weekly batch error:', err.message);
    }
  }, { timezone: 'UTC' });

  if (process.env.RESEND_API_KEY) {
    cron.schedule('0 9 * * 0', () => {
      sendWeeklyToAll().catch(err => console.error('[cron] Mailer error:', err.message));
    }, { timezone: 'UTC' });
  }
  console.log('   Cron jobs scheduled ✓');
}

async function connectDatabase() {
  const max = 10;
  for (let i = 1; i <= max; i++) {
    try {
      await initSchema();
      dbReady = true;
      console.log('[DB] Schema ready ✓');
      startCrons();
      return;
    } catch (err) {
      console.error(`[DB] Connect attempt ${i}/${max} failed:`, err.message);
      if (i === max) {
        console.error('[DB] Giving up after max retries — API admin routes may fail until DB is fixed.');
        return;
      }
      await sleep(4000);
    }
  }
}

app.listen(PORT, '0.0.0.0', () => {
  console.log(`\n🧘 d4l1-capsule-engine listening on 0.0.0.0:${PORT}`);
  console.log(`   Health     : /api/capsule/health`);
  console.log(`   Status     : /\n`);
  connectDatabase();
});

module.exports = app;
