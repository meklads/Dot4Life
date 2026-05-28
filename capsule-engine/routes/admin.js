/**
 * d4l1-capsule-engine — Admin API Routes
 * All routes require valid session token (Bearer header or cookie)
 * Admin password is stored as SHA-256 hash in config.js
 */

const express = require('express');
const router = express.Router();
const crypto = require('crypto');
const {
  q, createCapsule, submitForReview,
  approveCapsule, rejectCapsule, publishCapsule,
  createSession, validateSession, destroySession
} = require('../db');
const { generateBatch, generateOne } = require('../generator');
const config = require('../config');

// ─────────────────────────────────────────
//  AUTH MIDDLEWARE
// ─────────────────────────────────────────

function requireAuth(req, res, next) {
  const auth = req.headers.authorization || '';
  const token = auth.replace('Bearer ', '') || req.cookies?.admin_token;
  if (!token || !validateSession(token)) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  req.adminToken = token;
  next();
}

// ─────────────────────────────────────────
//  AUTH ROUTES (no auth required)
// ─────────────────────────────────────────

// POST /api/admin/login  { password: "..." }
router.post('/login', (req, res) => {
  const { password } = req.body;
  if (!password) return res.status(400).json({ error: 'Password required' });

  const hash = crypto.createHash('sha256').update(password).digest('hex');
  if (hash !== config.ADMIN_PASSWORD_HASH) {
    return res.status(401).json({ error: 'Invalid password' });
  }

  const token = createSession();
  res.json({ ok: true, token });
});

// POST /api/admin/logout
router.post('/logout', requireAuth, (req, res) => {
  destroySession(req.adminToken);
  res.json({ ok: true });
});

// GET /api/admin/me
router.get('/me', requireAuth, (req, res) => {
  res.json({ ok: true, admin: true });
});

// ─────────────────────────────────────────
//  CAPSULE CRUD
// ─────────────────────────────────────────

// GET /api/admin/capsules?status=pending_review
router.get('/capsules', requireAuth, (req, res) => {
  const { status } = req.query;
  let capsules;
  if (status) {
    capsules = q.getCapsulesByStatus.all(status);
  } else {
    capsules = q.getAllCapsules.all();
  }
  // Parse tags
  capsules = capsules.map(c => ({ ...c, tags: safeParseJSON(c.tags, []) }));
  res.json({ capsules });
});

// GET /api/admin/capsules/pending
router.get('/capsules/pending', requireAuth, (req, res) => {
  const capsules = q.getPendingCapsules.all().map(c => ({
    ...c, tags: safeParseJSON(c.tags, [])
  }));
  res.json({ capsules, count: capsules.length });
});

// GET /api/admin/capsules/:id
router.get('/capsules/:id', requireAuth, (req, res) => {
  const cap = q.getCapsuleById.get(req.params.id);
  if (!cap) return res.status(404).json({ error: 'Not found' });
  res.json({ capsule: { ...cap, tags: safeParseJSON(cap.tags, []) } });
});

// POST /api/admin/capsules  — create new capsule manually
router.post('/capsules', requireAuth, (req, res) => {
  try {
    const capsule = createCapsule({ ...req.body, source: 'manual' });
    res.status(201).json({ capsule });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// PUT /api/admin/capsules/:id  — edit capsule
router.put('/capsules/:id', requireAuth, (req, res) => {
  try {
    const cap = q.getCapsuleById.get(req.params.id);
    if (!cap) return res.status(404).json({ error: 'Not found' });

    const data = req.body;
    q.updateCapsule.run({
      id: req.params.id,
      category: data.category ?? cap.category,
      emoji: data.emoji ?? cap.emoji,
      title_en: data.title_en ?? cap.title_en,
      title_ar: data.title_ar ?? cap.title_ar,
      subtitle_en: data.subtitle_en ?? cap.subtitle_en,
      subtitle_ar: data.subtitle_ar ?? cap.subtitle_ar,
      body_en: data.body_en ?? cap.body_en,
      body_ar: data.body_ar ?? cap.body_ar,
      tags: JSON.stringify(data.tags ?? safeParseJSON(cap.tags, [])),
      tip_en: data.tip_en ?? cap.tip_en,
      tip_ar: data.tip_ar ?? cap.tip_ar,
      scheduled_date: data.scheduled_date ?? cap.scheduled_date,
    });

    q.logAction.run({ action: 'edit', capsule_id: req.params.id, old_status: cap.status, new_status: cap.status, note: 'Edited by admin' });

    const updated = q.getCapsuleById.get(req.params.id);
    res.json({ capsule: { ...updated, tags: safeParseJSON(updated.tags, []) } });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// ─────────────────────────────────────────
//  WORKFLOW ACTIONS
// ─────────────────────────────────────────

// POST /api/admin/capsules/:id/submit
router.post('/capsules/:id/submit', requireAuth, (req, res) => {
  try {
    const cap = submitForReview(req.params.id);
    res.json({ capsule: cap, message: 'Submitted for review' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// POST /api/admin/capsules/:id/approve  { note: "..." }
router.post('/capsules/:id/approve', requireAuth, (req, res) => {
  try {
    const cap = approveCapsule(req.params.id, { adminNote: req.body.note });
    res.json({ capsule: cap, message: 'Capsule approved' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// POST /api/admin/capsules/:id/reject  { reason: "...", note: "..." }
router.post('/capsules/:id/reject', requireAuth, (req, res) => {
  try {
    const cap = rejectCapsule(req.params.id, {
      reason: req.body.reason,
      adminNote: req.body.note
    });
    res.json({ capsule: cap, message: 'Capsule rejected' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// POST /api/admin/capsules/:id/publish  { date: "YYYY-MM-DD" }
router.post('/capsules/:id/publish', requireAuth, (req, res) => {
  try {
    const cap = publishCapsule(req.params.id, req.body.date);
    res.json({ capsule: cap, message: `Published to ${req.body.date || cap.scheduled_date}` });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// ─────────────────────────────────────────
//  GENERATOR
// ─────────────────────────────────────────

// POST /api/admin/generate  { days: 7, start_date: "YYYY-MM-DD" }
router.post('/generate', requireAuth, (req, res) => {
  try {
    const { days, start_date } = req.body;
    const results = generateBatch(days || 7, start_date || null);
    res.json({ generated: results, count: results.filter(r => !r.skipped).length });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/admin/generate/one  { date: "YYYY-MM-DD", category: "meals" }
router.post('/generate/one', requireAuth, (req, res) => {
  try {
    const capsule = generateOne({ date: req.body.date, category: req.body.category });
    res.status(201).json({ capsule });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ─────────────────────────────────────────
//  SCHEDULE & AUDIT
// ─────────────────────────────────────────

// GET /api/admin/schedule?days=14
router.get('/schedule', requireAuth, (req, res) => {
  const days = parseInt(req.query.days) || 14;
  const schedule = q.getSchedule.all(days);
  res.json({ schedule });
});

// GET /api/admin/audit
router.get('/audit', requireAuth, (req, res) => {
  const log = q.getAuditLog.all();
  res.json({ log });
});

// ─────────────────────────────────────────
//  HELPERS
// ─────────────────────────────────────────

function safeParseJSON(str, fallback) {
  try { return JSON.parse(str); } catch { return fallback; }
}

module.exports = router;
