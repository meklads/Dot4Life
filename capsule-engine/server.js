/**
 * d4l1-capsule-engine — Main Server
 *
 * Endpoints:
 *   Public:  GET  /api/capsule/today
 *            GET  /api/capsule/schedule
 *            GET  /api/capsule/category/:cat
 *            GET  /api/capsule/health
 *
 *   Admin:   POST /api/admin/login
 *            GET  /api/admin/capsules  ...etc
 *
 *   Pregnancy Journey:
 *            POST /api/pregnancy/subscribe
 *            GET  /api/pregnancy/me/:token
 *            GET  /api/pregnancy/unsubscribe/:token
 *
 * Start: node server.js
 */

const express = require('express');
const cors    = require('cors');
const cron    = require('node-cron');
const config  = require('./config');
const { initSchema } = require('./db');
const { sendWeeklyToAll } = require('./pregnancy-mailer');

const app = express();

// ─────────────────────────────────────────
//  MIDDLEWARE
// ─────────────────────────────────────────
app.use(cors({ origin: '*' }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use((req, _res, next) => {
  const ts = new Date().toISOString().slice(11, 19);
  console.log(`[${ts}] ${req.method} ${req.path}`);
  next();
});

// ─────────────────────────────────────────
//  ROUTES
// ─────────────────────────────────────────
app.use('/api/capsule',   require('./routes/public'));
app.use('/api/admin',     require('./routes/admin'));
app.use('/api/pregnancy', require('./routes/pregnancy'));
app.use('/api/contact',   require('./routes/contact'));

app.get('/', (_req, res) => res.json({
  system: 'd4l1-capsule-engine', version: '1.1.0', status: 'running',
  endpoints: {
    public:    '/api/capsule/today | /api/capsule/health',
    admin:     '/api/admin/login  | /api/admin/capsules',
    pregnancy: '/api/pregnancy/subscribe | /api/pregnancy/me/:token',
  }
}));

app.use((_req, res) => res.status(404).json({ error: 'Not found' }));

app.use((err, _req, res, _next) => {
  console.error('[ERROR]', err.message);
  res.status(500).json({ error: err.message });
});

// ─────────────────────────────────────────
//  START — init schema first, then listen
// ─────────────────────────────────────────
const PORT = config.PORT;

initSchema()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`\n🧘 d4l1-capsule-engine running on port ${PORT}`);
      console.log(`   Public API : http://localhost:${PORT}/api/capsule/today`);
      console.log(`   Admin API  : http://localhost:${PORT}/api/admin/login`);
      console.log(`   Pregnancy  : http://localhost:${PORT}/api/pregnancy/subscribe`);
      console.log(`   Status     : http://localhost:${PORT}/\n`);

      // ─── WEEKLY CRON ───────────────────────────────────────────
      // Every Sunday at 09:00 UTC (= 12:00 noon Saudi/UAE time)
      // Cron: "0 9 * * 0"
      if (process.env.RESEND_API_KEY) {
        cron.schedule('0 9 * * 0', () => {
          console.log('[cron] Sunday 09:00 UTC — sending weekly pregnancy emails');
          sendWeeklyToAll().catch(err =>
            console.error('[cron] Mailer error:', err.message)
          );
        }, { timezone: 'UTC' });
        console.log('   Cron: weekly pregnancy emails → Sunday 09:00 UTC ✓');
      } else {
        console.warn('   Cron: RESEND_API_KEY not set — weekly emails disabled');
      }
    });
  })
  .catch(err => {
    console.error('[FATAL] Could not initialize database:', err.message);
    console.error('Make sure DATABASE_URL is set correctly.');
    process.exit(1);
  });

module.exports = app;
