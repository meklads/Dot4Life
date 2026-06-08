/**
 * d4l1-capsule-engine — Public API Routes
 * Returns ONLY published capsules — no drafts, no pending
 */

const express = require('express');
const router  = express.Router();
const db      = require('../db');

// GET /api/capsule/today
router.get('/today', async (req, res) => {
  try {
    const date    = req.query.date || new Date().toISOString().slice(0, 10);
    const capsule = await db.getTodayCapsule(date);
    if (!capsule) return res.json({ found: false, date, capsule: null });

    let tags = [];
    try { tags = JSON.parse(capsule.tags); } catch {}

    res.json({
      found: true,
      date,
      capsule: {
        id:          capsule.id,
        category:    capsule.category,
        emoji:       capsule.emoji,
        title_en:    capsule.title_en,
        title_ar:    capsule.title_ar,
        subtitle_en: capsule.subtitle_en,
        subtitle_ar: capsule.subtitle_ar,
        body_en:     capsule.body_en,
        body_ar:     capsule.body_ar,
        tip_en:      capsule.tip_en,
        tip_ar:      capsule.tip_ar,
        tags,
      }
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/capsule/schedule?days=7
router.get('/schedule', async (req, res) => {
  try {
    const days     = Math.min(parseInt(req.query.days) || 7, 30);
    const schedule = await db.getSchedule(days);
    res.json({
      schedule: schedule.map(r => ({
        date: r.date,
        capsule: { id: r.id, category: r.category, emoji: r.emoji,
                   title_en: r.title_en, title_ar: r.title_ar }
      }))
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/capsule/category/:cat
router.get('/category/:cat', async (req, res) => {
  try {
    const valid = ['meals','family','wellness','faith','money','living'];
    if (!valid.includes(req.params.cat))
      return res.status(400).json({ error: 'Invalid category' });
    const capsules = await db.getCapsulesByCategory(req.params.cat);
    res.json({ category: req.params.cat, capsules });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/capsule/health
router.get('/health', (_req, res) => {
  res.json({ ok: true, system: 'd4l1-capsule-engine', ts: new Date().toISOString() });
});
// GET /api/capsule/:id  — fetch any single published capsule by ID
router.get('/:id', async (req, res) => {
  try {
    const cap = await db.getCapsuleById(req.params.id);
    if (!cap || cap.status !== 'published')
      return res.status(404).json({ found: false, error: 'Capsule not found or not published' });

    let tags = [];
    try { tags = JSON.parse(cap.tags); } catch {}

    res.json({
      found: true,
      capsule: {
        id:             cap.id,
        category:       cap.category,
        emoji:          cap.emoji,
        title_en:       cap.title_en,
        title_ar:       cap.title_ar,
        subtitle_en:    cap.subtitle_en,
        subtitle_ar:    cap.subtitle_ar,
        body_en:        cap.body_en,
        body_ar:        cap.body_ar,
        tip_en:         cap.tip_en,
        tip_ar:         cap.tip_ar,
        tags,
        scheduled_date: cap.scheduled_date,
      }
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


module.exports = router;
