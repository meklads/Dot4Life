/**
 * d4l1-capsule-engine — Admin API Routes
 * All routes require valid Bearer token
 */

const express = require('express');
const router  = express.Router();
const crypto  = require('crypto');
const db      = require('../db');
const { generateBatch, generateOne } = require('../generator');
const config  = require('../config');

// ─────────────────────────────────────────
//  AUTH MIDDLEWARE
// ─────────────────────────────────────────
async function requireAuth(req, res, next) {
  const token = (req.headers.authorization || '').replace('Bearer ', '');
  if (!token || !(await db.validateSession(token)))
    return res.status(401).json({ error: 'Unauthorized' });
  req.adminToken = token;
  next();
}

// ─────────────────────────────────────────
//  AUTH
// ─────────────────────────────────────────
router.post('/login', async (req, res) => {
  try {
    const { password } = req.body;
    if (!password) return res.status(400).json({ error: 'Password required' });
    const hash = crypto.createHash('sha256').update(password).digest('hex');
    if (hash !== config.ADMIN_PASSWORD_HASH)
      return res.status(401).json({ error: 'Invalid password' });
    const token = await db.createSession();
    res.json({ ok: true, token });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/logout', requireAuth, async (req, res) => {
  await db.destroySession(req.adminToken);
  res.json({ ok: true });
});

router.get('/me', requireAuth, (_req, res) => {
  res.json({ ok: true, admin: true });
});

// ─────────────────────────────────────────
//  CAPSULE LIST
// ─────────────────────────────────────────
router.get('/capsules', requireAuth, async (req, res) => {
  try {
    const { status } = req.query;
    const capsules = status
      ? await db.getCapsulesByStatus(status)
      : await db.getAllCapsules();
    res.json({ capsules: capsules.map(parseTags) });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get('/capsules/pending', requireAuth, async (_req, res) => {
  try {
    const capsules = await db.getPendingCapsules();
    res.json({ capsules: capsules.map(parseTags), count: capsules.length });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get('/capsules/:id', requireAuth, async (req, res) => {
  try {
    const cap = await db.getCapsuleById(req.params.id);
    if (!cap) return res.status(404).json({ error: 'Not found' });
    res.json({ capsule: parseTags(cap) });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ─────────────────────────────────────────
//  CAPSULE CREATE / EDIT
// ─────────────────────────────────────────
router.post('/capsules', requireAuth, async (req, res) => {
  try {
    const capsule = await db.createCapsule({ ...req.body, source: 'manual' });
    res.status(201).json({ capsule });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.put('/capsules/:id', requireAuth, async (req, res) => {
  try {
    const cap = await db.getCapsuleById(req.params.id);
    if (!cap) return res.status(404).json({ error: 'Not found' });
    const d = req.body;
    const updated = await db.updateCapsule(req.params.id, {
      category:       d.category       ?? cap.category,
      emoji:          d.emoji          ?? cap.emoji,
      title_en:       d.title_en       ?? cap.title_en,
      title_ar:       d.title_ar       ?? cap.title_ar,
      subtitle_en:    d.subtitle_en    ?? cap.subtitle_en,
      subtitle_ar:    d.subtitle_ar    ?? cap.subtitle_ar,
      body_en:        d.body_en        ?? cap.body_en,
      body_ar:        d.body_ar        ?? cap.body_ar,
      tags:           d.tags           ?? safeJSON(cap.tags, []),
      tip_en:         d.tip_en         ?? cap.tip_en,
      tip_ar:         d.tip_ar         ?? cap.tip_ar,
      scheduled_date: d.scheduled_date ?? cap.scheduled_date,
    });
    await db.logAction('edit', req.params.id, cap.status, cap.status, 'Edited by admin');
    res.json({ capsule: parseTags(updated) });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// ─────────────────────────────────────────
//  WORKFLOW
// ─────────────────────────────────────────
router.post('/capsules/:id/submit', requireAuth, async (req, res) => {
  try {
    const cap = await db.submitForReview(req.params.id);
    res.json({ capsule: cap, message: 'Submitted for review' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.post('/capsules/:id/approve', requireAuth, async (req, res) => {
  try {
    const cap = await db.approveCapsule(req.params.id, { adminNote: req.body.note });
    res.json({ capsule: cap, message: 'Approved' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.post('/capsules/:id/reject', requireAuth, async (req, res) => {
  try {
    const cap = await db.rejectCapsule(req.params.id, {
      reason: req.body.reason, adminNote: req.body.note
    });
    res.json({ capsule: cap, message: 'Rejected' });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.post('/capsules/:id/publish', requireAuth, async (req, res) => {
  try {
    const cap = await db.publishCapsule(req.params.id, req.body.date);
    res.json({ capsule: cap, message: `Published to ${req.body.date}` });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// ─────────────────────────────────────────
//  GENERATOR
// ─────────────────────────────────────────
router.post('/generate', requireAuth, async (req, res) => {
  try {
    const results = await generateBatch(req.body.days || 7, req.body.start_date || null);
    res.json({ generated: results, count: results.filter(r => !r.skipped).length });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post('/generate/one', requireAuth, async (req, res) => {
  try {
    const capsule = await generateOne({ date: req.body.date, category: req.body.category });
    res.status(201).json({ capsule });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ─────────────────────────────────────────
//  SCHEDULE + AUDIT
// ─────────────────────────────────────────
router.get('/schedule', requireAuth, async (req, res) => {
  try {
    const schedule = await db.getSchedule(parseInt(req.query.days) || 14);
    res.json({ schedule });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get('/audit', requireAuth, async (_req, res) => {
  try {
    const log = await db.getAuditLog();
    res.json({ log });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ─────────────────────────────────────────
//  HELPERS
// ─────────────────────────────────────────
function safeJSON(str, fallback) {
  try { return JSON.parse(str); } catch { return fallback; }
}
function parseTags(c) {
  return { ...c, tags: safeJSON(c.tags, []) };
}

module.exports = router;
