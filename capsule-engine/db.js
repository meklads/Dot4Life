/**
 * d4l1-capsule-engine — Database Layer (PostgreSQL)
 * Uses pg Pool — works with Railway, Supabase, Neon, or any Postgres
 * Set DATABASE_URL environment variable to connect
 */

const { Pool } = require('pg');
const crypto   = require('crypto');

// ─────────────────────────────────────────
//  CONNECTION
// ─────────────────────────────────────────
console.log('[DB] DATABASE_URL:', process.env.DATABASE_URL ? 'SET → ' + process.env.DATABASE_URL.slice(0, 30) + '...' : 'NOT SET — using localhost fallback');

const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgresql://localhost/d4l_capsules',
  ssl: process.env.DATABASE_URL ? { rejectUnauthorized: false } : false,
});

pool.on('error', (err) => {
  console.error('[DB] Unexpected pool error:', err.message);
});

// ─────────────────────────────────────────
//  SCHEMA INIT
// ─────────────────────────────────────────
async function initSchema() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS ce_capsules (
      id            TEXT PRIMARY KEY,
      category      TEXT NOT NULL,
      emoji         TEXT DEFAULT '🌿',
      title_en      TEXT NOT NULL,
      title_ar      TEXT NOT NULL,
      subtitle_en   TEXT,
      subtitle_ar   TEXT,
      body_en       TEXT,
      body_ar       TEXT,
      tags          TEXT DEFAULT '[]',
      tip_en        TEXT,
      tip_ar        TEXT,
      scheduled_date TEXT,
      status        TEXT NOT NULL DEFAULT 'draft',
      source        TEXT DEFAULT 'manual',
      created_at    TIMESTAMPTZ DEFAULT NOW(),
      updated_at    TIMESTAMPTZ DEFAULT NOW(),
      reviewed_at   TIMESTAMPTZ,
      reviewed_by   TEXT,
      admin_notes   TEXT,
      reject_reason TEXT
    );

    CREATE TABLE IF NOT EXISTS ce_schedule (
      date         TEXT PRIMARY KEY,
      capsule_id   TEXT NOT NULL REFERENCES ce_capsules(id),
      published_at TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS ce_admin_sessions (
      token      TEXT PRIMARY KEY,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      expires_at TIMESTAMPTZ NOT NULL,
      note       TEXT
    );

    CREATE TABLE IF NOT EXISTS ce_audit_log (
      id          SERIAL PRIMARY KEY,
      action      TEXT NOT NULL,
      capsule_id  TEXT,
      old_status  TEXT,
      new_status  TEXT,
      note        TEXT,
      created_at  TIMESTAMPTZ DEFAULT NOW()
    );

    CREATE INDEX IF NOT EXISTS idx_capsules_status   ON ce_capsules(status);
    CREATE INDEX IF NOT EXISTS idx_capsules_date     ON ce_capsules(scheduled_date);
    CREATE INDEX IF NOT EXISTS idx_capsules_category ON ce_capsules(category);
    CREATE INDEX IF NOT EXISTS idx_schedule_date     ON ce_schedule(date);

    CREATE TABLE IF NOT EXISTS pj_subscribers (
      id                SERIAL PRIMARY KEY,
      name              TEXT NOT NULL,
      email             TEXT NOT NULL UNIQUE,
      due_date          DATE NOT NULL,
      baby_name         TEXT,
      token             TEXT UNIQUE NOT NULL,
      unsubscribe_token TEXT UNIQUE NOT NULL,
      subscribed_at     TIMESTAMPTZ DEFAULT NOW(),
      last_sent_at      TIMESTAMPTZ,
      last_week_sent    INTEGER,
      is_active         BOOLEAN DEFAULT TRUE
    );

    CREATE INDEX IF NOT EXISTS idx_pj_email  ON pj_subscribers(email);
    CREATE INDEX IF NOT EXISTS idx_pj_token  ON pj_subscribers(token);
    CREATE INDEX IF NOT EXISTS idx_pj_active ON pj_subscribers(is_active);
  `);
  console.log('[DB] Schema ready ✓');
}

// ─────────────────────────────────────────
//  QUERY HELPERS
// ─────────────────────────────────────────
async function one(sql, params = []) {
  const r = await pool.query(sql, params);
  return r.rows[0] || null;
}
async function all(sql, params = []) {
  const r = await pool.query(sql, params);
  return r.rows;
}
async function run(sql, params = []) {
  await pool.query(sql, params);
}

// ─────────────────────────────────────────
//  CAPSULE QUERIES
// ─────────────────────────────────────────
async function getCapsuleById(id) {
  return one('SELECT * FROM ce_capsules WHERE id = $1', [id]);
}

async function getCapsulesByStatus(status) {
  return all('SELECT * FROM ce_capsules WHERE status = $1 ORDER BY created_at DESC', [status]);
}

async function getPendingCapsules() {
  return all(`SELECT * FROM ce_capsules WHERE status = 'pending_review'
              ORDER BY scheduled_date ASC, created_at ASC`);
}

async function getApprovedCapsules() {
  return all(`SELECT * FROM ce_capsules WHERE status = 'approved' ORDER BY scheduled_date ASC`);
}

async function getAllCapsules() {
  return all('SELECT * FROM ce_capsules ORDER BY created_at DESC LIMIT 100');
}

async function getAllPublishedCapsules() {
  return all("SELECT * FROM ce_capsules WHERE status = 'published' ORDER BY scheduled_date DESC NULLS LAST");
}

async function getCapsulesByCategory(category) {
  return all(`SELECT * FROM ce_capsules WHERE category = $1 AND status = 'published'
              ORDER BY scheduled_date DESC LIMIT 20`, [category]);
}

async function getTodayPublished(date) {
  return one(`
    SELECT c.* FROM ce_capsules c
    JOIN ce_schedule s ON s.capsule_id = c.id
    WHERE s.date = $1 AND c.status = 'published'
    LIMIT 1`, [date]);
}

async function getSchedule(limit = 30) {
  return all(`
    SELECT s.date, c.* FROM ce_schedule s
    JOIN ce_capsules c ON c.id = s.capsule_id
    ORDER BY s.date DESC LIMIT $1`, [limit]);
}

async function getScheduledDate(date) {
  return one('SELECT * FROM ce_schedule WHERE date = $1', [date]);
}

// ─────────────────────────────────────────
//  BUSINESS LOGIC
// ─────────────────────────────────────────

function newCapsuleId(date) {
  const d = (date || new Date().toISOString().slice(0, 10)).replace(/-/g, '');
  const rand = crypto.randomBytes(3).toString('hex');
  return `cap_${d}_${rand}`;
}

async function createCapsule(data) {
  const id = newCapsuleId(data.scheduled_date);
  await run(`
    INSERT INTO ce_capsules
      (id, category, emoji, title_en, title_ar, subtitle_en, subtitle_ar,
       body_en, body_ar, tags, tip_en, tip_ar, scheduled_date, status, source)
    VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15)`,
    [
      id,
      data.category || 'meals',
      data.emoji    || '🌿',
      data.title_en || '',
      data.title_ar || '',
      data.subtitle_en || '',
      data.subtitle_ar || '',
      data.body_en  || '',
      data.body_ar  || '',
      JSON.stringify(data.tags || []),
      data.tip_en   || '',
      data.tip_ar   || '',
      data.scheduled_date || null,
      data.status   || 'draft',
      data.source   || 'manual',
    ]
  );
  await logAction('create', id, null, data.status || 'draft', 'Created');
  return getCapsuleById(id);
}

async function updateCapsule(id, data) {
  await run(`
    UPDATE ce_capsules SET
      category=$1, emoji=$2, title_en=$3, title_ar=$4,
      subtitle_en=$5, subtitle_ar=$6, body_en=$7, body_ar=$8,
      tags=$9, tip_en=$10, tip_ar=$11, scheduled_date=$12,
      updated_at=NOW()
    WHERE id=$13`,
    [
      data.category, data.emoji, data.title_en, data.title_ar,
      data.subtitle_en, data.subtitle_ar, data.body_en, data.body_ar,
      JSON.stringify(data.tags || []), data.tip_en, data.tip_ar,
      data.scheduled_date, id
    ]
  );
  return getCapsuleById(id);
}

async function setStatus(id, status, { reviewedBy, adminNotes, rejectReason } = {}) {
  await run(`
    UPDATE ce_capsules SET
      status=$1, reviewed_at=NOW(), reviewed_by=$2,
      admin_notes=$3, reject_reason=$4, updated_at=NOW()
    WHERE id=$5`,
    [status, reviewedBy || null, adminNotes || null, rejectReason || null, id]
  );
}

async function submitForReview(id) {
  const cap = await getCapsuleById(id);
  if (!cap) throw new Error('Capsule not found');
  if (cap.status !== 'draft') throw new Error(`Cannot submit from status: ${cap.status}`);
  await setStatus(id, 'pending_review');
  await logAction('submit', id, cap.status, 'pending_review', null);
  return getCapsuleById(id);
}

async function approveCapsule(id, { adminNote } = {}) {
  const cap = await getCapsuleById(id);
  if (!cap) throw new Error('Capsule not found');
  await setStatus(id, 'approved', { reviewedBy: 'admin', adminNotes: adminNote });
  await logAction('approve', id, cap.status, 'approved', adminNote || null);
  return getCapsuleById(id);
}

async function rejectCapsule(id, { reason, adminNote } = {}) {
  const cap = await getCapsuleById(id);
  if (!cap) throw new Error('Capsule not found');
  await setStatus(id, 'rejected', { reviewedBy: 'admin', adminNotes: adminNote, rejectReason: reason });
  await logAction('reject', id, cap.status, 'rejected', reason || null);
  return getCapsuleById(id);
}

async function publishCapsule(id, date) {
  const cap = await getCapsuleById(id);
  if (!cap) throw new Error('Capsule not found');
  if (cap.status !== 'approved') throw new Error('Only approved capsules can be published');
  const targetDate = date || cap.scheduled_date || new Date().toISOString().slice(0, 10);
  await setStatus(id, 'published', { reviewedBy: 'admin' });
  await run(`INSERT INTO ce_schedule (date, capsule_id) VALUES ($1, $2)
             ON CONFLICT (date) DO UPDATE SET capsule_id=$2, published_at=NOW()`,
    [targetDate, id]);
  await logAction('publish', id, 'approved', 'published', `Published to ${targetDate}`);
  return getCapsuleById(id);
}

async function getTodayCapsule(dateStr) {
  const date = dateStr || new Date().toISOString().slice(0, 10);
  return getTodayPublished(date);
}

// ─────────────────────────────────────────
//  AUDIT
// ─────────────────────────────────────────
async function logAction(action, capsuleId, oldStatus, newStatus, note) {
  await run(`INSERT INTO ce_audit_log (action, capsule_id, old_status, new_status, note)
             VALUES ($1,$2,$3,$4,$5)`,
    [action, capsuleId, oldStatus, newStatus, note]);
}

async function getAuditLog() {
  return all('SELECT * FROM ce_audit_log ORDER BY created_at DESC LIMIT 50');
}

// ─────────────────────────────────────────
//  SESSIONS
// ─────────────────────────────────────────
function newToken() {
  return crypto.randomBytes(32).toString('hex');
}

async function createSession() {
  await run(`DELETE FROM ce_admin_sessions WHERE expires_at < NOW()`);
  const token     = newToken();
  const expiresAt = new Date(Date.now() + 8 * 60 * 60 * 1000);
  await run(`INSERT INTO ce_admin_sessions (token, expires_at, note) VALUES ($1,$2,'admin')`,
    [token, expiresAt.toISOString()]);
  return token;
}

async function validateSession(token) {
  if (!token) return false;
  const s = await one(`SELECT * FROM ce_admin_sessions WHERE token=$1 AND expires_at > NOW()`, [token]);
  return !!s;
}

async function destroySession(token) {
  await run('DELETE FROM ce_admin_sessions WHERE token=$1', [token]);
}

// ─────────────────────────────────────────
//  EXPORTS
// ─────────────────────────────────────────
// ─────────────────────────────────────────
//  PREGNANCY SUBSCRIBERS
// ─────────────────────────────────────────

function calcWeekFromDue(dueDateStr) {
  const due   = new Date(dueDateStr);
  const today = new Date();
  const diffDays = Math.round((due - today) / (1000 * 60 * 60 * 24));
  return Math.max(1, Math.min(40, 40 - Math.round(diffDays / 7)));
}

async function pjSubscribe({ name, email, due_date, baby_name }) {
  const existing = await one('SELECT * FROM pj_subscribers WHERE email=$1', [email]);
  if (existing) {
    // Re-activate if unsubscribed, or return existing token
    if (!existing.is_active) {
      await run(
        'UPDATE pj_subscribers SET is_active=TRUE, due_date=$1, name=$2, baby_name=$3, subscribed_at=NOW() WHERE email=$4',
        [due_date, name, baby_name || null, email]
      );
      return { token: existing.token, isNew: false };
    }
    return { token: existing.token, isNew: false };
  }
  const token      = newToken().slice(0, 24);
  const unsubToken = newToken().slice(0, 24);
  await run(
    `INSERT INTO pj_subscribers (name, email, due_date, baby_name, token, unsubscribe_token)
     VALUES ($1,$2,$3,$4,$5,$6)`,
    [name, email, due_date, baby_name || null, token, unsubToken]
  );
  return { token, isNew: true };
}

async function pjGetByToken(token) {
  return one('SELECT * FROM pj_subscribers WHERE token=$1 AND is_active=TRUE', [token]);
}

async function pjUnsubscribe(unsubToken) {
  await run('UPDATE pj_subscribers SET is_active=FALSE WHERE unsubscribe_token=$1', [unsubToken]);
}

async function pjGetActiveSubscribers() {
  return all('SELECT * FROM pj_subscribers WHERE is_active=TRUE ORDER BY subscribed_at ASC');
}

async function pjMarkSent(id, week) {
  await run('UPDATE pj_subscribers SET last_sent_at=NOW(), last_week_sent=$1 WHERE id=$2', [week, id]);
}

module.exports = {
  pool, initSchema,
  calcWeekFromDue,
  pjSubscribe, pjGetByToken, pjUnsubscribe, pjGetActiveSubscribers, pjMarkSent,
  // capsule CRUD
  getCapsuleById, getCapsulesByStatus, getPendingCapsules,
  getApprovedCapsules, getAllCapsules, getCapsulesByCategory,
  getTodayPublished, getSchedule, getScheduledDate,
  // business logic
  createCapsule, updateCapsule,
  submitForReview, approveCapsule, rejectCapsule, publishCapsule,
  getTodayCapsule,
  // audit
  logAction, getAuditLog,
  // sessions
  createSession, validateSession, destroySession,
  newCapsuleId,
};
