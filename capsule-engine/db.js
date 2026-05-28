/**
 * d4l1-capsule-engine — Database Layer
 * SQLite via better-sqlite3 (synchronous, zero-config)
 * All tables prefixed with ce_ to avoid future conflicts
 */

const Database = require('better-sqlite3');
const path = require('path');
const crypto = require('crypto');

const DB_PATH = path.join(__dirname, 'data', 'capsules.db');

// Ensure data directory exists
const fs = require('fs');
fs.mkdirSync(path.join(__dirname, 'data'), { recursive: true });

const db = new Database(DB_PATH);

// Enable WAL mode for better concurrent reads
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

// ─────────────────────────────────────────
//  SCHEMA
// ─────────────────────────────────────────
db.exec(`

  /* ── Core capsule record ── */
  CREATE TABLE IF NOT EXISTS ce_capsules (
    id          TEXT PRIMARY KEY,             -- uuid-like: cap_YYYYMMDD_xxx
    category    TEXT NOT NULL,                -- meals | family | wellness | faith | money | living
    emoji       TEXT DEFAULT '🌿',
    title_en    TEXT NOT NULL,
    title_ar    TEXT NOT NULL,
    subtitle_en TEXT,
    subtitle_ar TEXT,
    body_en     TEXT,                         -- rich text / markdown
    body_ar     TEXT,
    tags        TEXT DEFAULT '[]',            -- JSON array of strings
    tip_en      TEXT,                         -- short action tip
    tip_ar      TEXT,

    -- scheduling
    scheduled_date TEXT,                      -- YYYY-MM-DD: which day to publish

    -- workflow
    status      TEXT NOT NULL DEFAULT 'draft',
    -- values: draft | pending_review | approved | rejected | published | archived

    -- metadata
    source      TEXT DEFAULT 'manual',        -- manual | generator | import
    created_at  TEXT DEFAULT (datetime('now')),
    updated_at  TEXT DEFAULT (datetime('now')),

    -- review
    reviewed_at   TEXT,
    reviewed_by   TEXT,
    admin_notes   TEXT,
    reject_reason TEXT
  );

  /* ── Published capsule schedule ── */
  /* One approved capsule per day maximum */
  CREATE TABLE IF NOT EXISTS ce_schedule (
    date        TEXT PRIMARY KEY,             -- YYYY-MM-DD
    capsule_id  TEXT NOT NULL,
    published_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (capsule_id) REFERENCES ce_capsules(id)
  );

  /* ── Admin sessions (simple token auth) ── */
  CREATE TABLE IF NOT EXISTS ce_admin_sessions (
    token       TEXT PRIMARY KEY,
    created_at  TEXT DEFAULT (datetime('now')),
    expires_at  TEXT NOT NULL,
    note        TEXT
  );

  /* ── Audit log ── */
  CREATE TABLE IF NOT EXISTS ce_audit_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    action      TEXT NOT NULL,               -- create|edit|approve|reject|publish|archive
    capsule_id  TEXT,
    old_status  TEXT,
    new_status  TEXT,
    note        TEXT,
    created_at  TEXT DEFAULT (datetime('now'))
  );

  /* ── Indexes ── */
  CREATE INDEX IF NOT EXISTS idx_capsules_status   ON ce_capsules(status);
  CREATE INDEX IF NOT EXISTS idx_capsules_date     ON ce_capsules(scheduled_date);
  CREATE INDEX IF NOT EXISTS idx_capsules_category ON ce_capsules(category);
  CREATE INDEX IF NOT EXISTS idx_schedule_date     ON ce_schedule(date);
`);

// ─────────────────────────────────────────
//  HELPERS
// ─────────────────────────────────────────

/** Generate a short unique capsule ID */
function newCapsuleId(date) {
  const d = date || new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const rand = crypto.randomBytes(3).toString('hex');
  return `cap_${d}_${rand}`;
}

/** Generate a secure session token */
function newSessionToken() {
  return crypto.randomBytes(32).toString('hex');
}

// ─────────────────────────────────────────
//  CAPSULE QUERIES
// ─────────────────────────────────────────

const q = {

  // ── CREATE ──
  insertCapsule: db.prepare(`
    INSERT INTO ce_capsules
      (id, category, emoji, title_en, title_ar, subtitle_en, subtitle_ar,
       body_en, body_ar, tags, tip_en, tip_ar, scheduled_date, status, source)
    VALUES
      (@id, @category, @emoji, @title_en, @title_ar, @subtitle_en, @subtitle_ar,
       @body_en, @body_ar, @tags, @tip_en, @tip_ar, @scheduled_date, @status, @source)
  `),

  // ── READ ──
  getCapsuleById: db.prepare(`SELECT * FROM ce_capsules WHERE id = ?`),

  getCapsulesByStatus: db.prepare(`
    SELECT * FROM ce_capsules WHERE status = ? ORDER BY created_at DESC
  `),

  getPendingCapsules: db.prepare(`
    SELECT * FROM ce_capsules WHERE status = 'pending_review' ORDER BY scheduled_date ASC, created_at ASC
  `),

  getApprovedCapsules: db.prepare(`
    SELECT * FROM ce_capsules WHERE status = 'approved' ORDER BY scheduled_date ASC
  `),

  getTodayPublished: db.prepare(`
    SELECT c.* FROM ce_capsules c
    JOIN ce_schedule s ON s.capsule_id = c.id
    WHERE s.date = ? AND c.status = 'published'
    LIMIT 1
  `),

  getSchedule: db.prepare(`
    SELECT s.date, c.* FROM ce_schedule s
    JOIN ce_capsules c ON c.id = s.capsule_id
    ORDER BY s.date DESC
    LIMIT ?
  `),

  getAllCapsules: db.prepare(`
    SELECT * FROM ce_capsules ORDER BY created_at DESC LIMIT 100
  `),

  getCapsulesByCategory: db.prepare(`
    SELECT * FROM ce_capsules WHERE category = ? AND status = 'published'
    ORDER BY scheduled_date DESC LIMIT 20
  `),

  // ── UPDATE ──
  updateCapsuleStatus: db.prepare(`
    UPDATE ce_capsules
    SET status = @status, reviewed_at = datetime('now'), reviewed_by = @reviewed_by,
        admin_notes = @admin_notes, reject_reason = @reject_reason,
        updated_at = datetime('now')
    WHERE id = @id
  `),

  updateCapsule: db.prepare(`
    UPDATE ce_capsules
    SET category=@category, emoji=@emoji, title_en=@title_en, title_ar=@title_ar,
        subtitle_en=@subtitle_en, subtitle_ar=@subtitle_ar,
        body_en=@body_en, body_ar=@body_ar, tags=@tags,
        tip_en=@tip_en, tip_ar=@tip_ar,
        scheduled_date=@scheduled_date, updated_at=datetime('now')
    WHERE id = @id
  `),

  // ── SCHEDULE ──
  schedulePublish: db.prepare(`
    INSERT OR REPLACE INTO ce_schedule (date, capsule_id, published_at)
    VALUES (@date, @capsule_id, datetime('now'))
  `),

  getScheduledDate: db.prepare(`SELECT * FROM ce_schedule WHERE date = ?`),

  // ── AUDIT ──
  logAction: db.prepare(`
    INSERT INTO ce_audit_log (action, capsule_id, old_status, new_status, note)
    VALUES (@action, @capsule_id, @old_status, @new_status, @note)
  `),

  getAuditLog: db.prepare(`
    SELECT * FROM ce_audit_log ORDER BY created_at DESC LIMIT 50
  `),

  // ── SESSIONS ──
  insertSession: db.prepare(`
    INSERT INTO ce_admin_sessions (token, expires_at, note)
    VALUES (@token, @expires_at, @note)
  `),

  getSession: db.prepare(`
    SELECT * FROM ce_admin_sessions
    WHERE token = ? AND expires_at > datetime('now')
  `),

  deleteSession: db.prepare(`DELETE FROM ce_admin_sessions WHERE token = ?`),

  cleanExpiredSessions: db.prepare(`
    DELETE FROM ce_admin_sessions WHERE expires_at < datetime('now')
  `),
};

// ─────────────────────────────────────────
//  BUSINESS LOGIC
// ─────────────────────────────────────────

/**
 * Create a new capsule (draft or pending)
 */
function createCapsule(data) {
  const id = newCapsuleId(data.scheduled_date);
  const capsule = {
    id,
    category: data.category || 'meals',
    emoji: data.emoji || '🌿',
    title_en: data.title_en || '',
    title_ar: data.title_ar || '',
    subtitle_en: data.subtitle_en || '',
    subtitle_ar: data.subtitle_ar || '',
    body_en: data.body_en || '',
    body_ar: data.body_ar || '',
    tags: JSON.stringify(data.tags || []),
    tip_en: data.tip_en || '',
    tip_ar: data.tip_ar || '',
    scheduled_date: data.scheduled_date || null,
    status: data.status || 'draft',
    source: data.source || 'manual',
  };
  q.insertCapsule.run(capsule);
  q.logAction.run({ action: 'create', capsule_id: id, old_status: null, new_status: capsule.status, note: 'Created' });
  return q.getCapsuleById.get(id);
}

/**
 * Submit capsule for admin review
 */
function submitForReview(id) {
  const cap = q.getCapsuleById.get(id);
  if (!cap) throw new Error('Capsule not found');
  if (!['draft'].includes(cap.status)) throw new Error(`Cannot submit from status: ${cap.status}`);
  q.updateCapsuleStatus.run({ id, status: 'pending_review', reviewed_by: null, admin_notes: null, reject_reason: null });
  q.logAction.run({ action: 'submit', capsule_id: id, old_status: cap.status, new_status: 'pending_review', note: null });
  return q.getCapsuleById.get(id);
}

/**
 * Admin: approve a capsule
 */
function approveCapsule(id, { adminNote } = {}) {
  const cap = q.getCapsuleById.get(id);
  if (!cap) throw new Error('Capsule not found');
  q.updateCapsuleStatus.run({
    id, status: 'approved',
    reviewed_by: 'admin', admin_notes: adminNote || null, reject_reason: null
  });
  q.logAction.run({ action: 'approve', capsule_id: id, old_status: cap.status, new_status: 'approved', note: adminNote || null });
  return q.getCapsuleById.get(id);
}

/**
 * Admin: reject a capsule
 */
function rejectCapsule(id, { reason, adminNote } = {}) {
  const cap = q.getCapsuleById.get(id);
  if (!cap) throw new Error('Capsule not found');
  q.updateCapsuleStatus.run({
    id, status: 'rejected',
    reviewed_by: 'admin', admin_notes: adminNote || null, reject_reason: reason || null
  });
  q.logAction.run({ action: 'reject', capsule_id: id, old_status: cap.status, new_status: 'rejected', note: reason || null });
  return q.getCapsuleById.get(id);
}

/**
 * Admin: publish an approved capsule to a specific date
 */
function publishCapsule(id, date) {
  const cap = q.getCapsuleById.get(id);
  if (!cap) throw new Error('Capsule not found');
  if (cap.status !== 'approved') throw new Error('Only approved capsules can be published');

  const targetDate = date || cap.scheduled_date || new Date().toISOString().slice(0, 10);

  // Check if date already has a published capsule
  const existing = q.getScheduledDate.get(targetDate);
  if (existing && existing.capsule_id !== id) {
    throw new Error(`Date ${targetDate} already has a published capsule`);
  }

  q.updateCapsuleStatus.run({ id, status: 'published', reviewed_by: 'admin', admin_notes: null, reject_reason: null });
  q.schedulePublish.run({ date: targetDate, capsule_id: id });
  q.logAction.run({ action: 'publish', capsule_id: id, old_status: 'approved', new_status: 'published', note: `Published to ${targetDate}` });
  return q.getCapsuleById.get(id);
}

/**
 * Get today's published capsule (for frontend API)
 */
function getTodayCapsule(dateStr) {
  const date = dateStr || new Date().toISOString().slice(0, 10);
  return q.getTodayPublished.get(date);
}

// ─────────────────────────────────────────
//  SESSION AUTH
// ─────────────────────────────────────────

function createSession() {
  q.cleanExpiredSessions.run();
  const token = newSessionToken();
  const expiresAt = new Date(Date.now() + 8 * 60 * 60 * 1000).toISOString(); // 8h
  q.insertSession.run({ token, expires_at: expiresAt, note: 'admin' });
  return token;
}

function validateSession(token) {
  if (!token) return false;
  const session = q.getSession.get(token);
  return !!session;
}

function destroySession(token) {
  q.deleteSession.run(token);
}

module.exports = {
  db, q,
  createCapsule, submitForReview,
  approveCapsule, rejectCapsule, publishCapsule,
  getTodayCapsule,
  createSession, validateSession, destroySession,
  newCapsuleId,
};
