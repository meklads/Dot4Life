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
 *            GET  /api/admin/capsules
 *            POST /api/admin/capsules
 *            PUT  /api/admin/capsules/:id
 *            POST /api/admin/capsules/:id/approve
 *            POST /api/admin/capsules/:id/reject
 *            POST /api/admin/capsules/:id/publish
 *            POST /api/admin/generate
 *            GET  /api/admin/schedule
 *            GET  /api/admin/audit
 *
 * Start: node server.js
 */

const express = require('express');
const cors    = require('cors');
const config  = require('./config');
const { initSchema } = require('./db');

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
app.use('/api/capsule', require('./routes/public'));
app.use('/api/admin',   require('./routes/admin'));

app.get('/', (_req, res) => res.json({
  system: 'd4l1-capsule-engine', version: '1.0.0', status: 'running',
  endpoints: {
    public: '/api/capsule/today | /api/capsule/health',
    admin:  '/api/admin/login  | /api/admin/capsules',
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
      console.log(`   Status     : http://localhost:${PORT}/\n`);
    });
  })
  .catch(err => {
    console.error('[FATAL] Could not initialize database:', err.message);
    console.error('Make sure DATABASE_URL is set correctly.');
    process.exit(1);
  });

module.exports = app;
