/**
 * d4l1-capsule-engine — Main Server
 * Express API server for Dot4Life capsule management
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
const path    = require('path');
const config  = require('./config');

const app = express();

// ─────────────────────────────────────────
//  MIDDLEWARE
// ─────────────────────────────────────────

app.use(cors({
  origin: (origin, cb) => {
    // Allow requests with no origin (curl, Postman, same-server)
    if (!origin) return cb(null, true);
    if (config.CORS_ORIGINS.includes(origin)) return cb(null, true);
    cb(new Error(`CORS: origin ${origin} not allowed`));
  },
  credentials: true,
}));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Simple request logger
app.use((req, _res, next) => {
  const ts = new Date().toISOString().slice(11, 19);
  console.log(`[${ts}] ${req.method} ${req.path}`);
  next();
});

// ─────────────────────────────────────────
//  ROUTES
// ─────────────────────────────────────────

const publicRoutes = require('./routes/public');
const adminRoutes  = require('./routes/admin');

// Public API — called by frontend (index.html)
app.use('/api/capsule', publicRoutes);

// Admin API — called by admin.html dashboard
app.use('/api/admin', adminRoutes);

// ─────────────────────────────────────────
//  ROOT + 404
// ─────────────────────────────────────────

app.get('/', (_req, res) => {
  res.json({
    system: 'd4l1-capsule-engine',
    version: '1.0.0',
    status: 'running',
    endpoints: {
      public:  '/api/capsule/today | /api/capsule/schedule | /api/capsule/health',
      admin:   '/api/admin/login | /api/admin/capsules | /api/admin/generate',
    }
  });
});

app.use((_req, res) => {
  res.status(404).json({ error: 'Not found' });
});

// ─────────────────────────────────────────
//  ERROR HANDLER
// ─────────────────────────────────────────

app.use((err, _req, res, _next) => {
  console.error('[ERROR]', err.message);
  res.status(500).json({ error: 'Server error', message: err.message });
});

// ─────────────────────────────────────────
//  START
// ─────────────────────────────────────────

const PORT = config.PORT;
app.listen(PORT, () => {
  console.log(`\n🧘 d4l1-capsule-engine running on port ${PORT}`);
  console.log(`   Public API : http://localhost:${PORT}/api/capsule/today`);
  console.log(`   Admin API  : http://localhost:${PORT}/api/admin/login`);
  console.log(`   Status     : http://localhost:${PORT}/\n`);
});

module.exports = app;
