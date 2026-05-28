/**
 * d4l1-capsule-engine — Public API Routes
 * These endpoints are called by the frontend (index.html)
 * Returns ONLY published capsules — no drafts, no pending, no rejected
 */

const express = require('express');
const router = express.Router();
const { getTodayCapsule, q } = require('../db');

// GET /api/capsule/today
// Returns today's published capsule (or empty if none)
router.get('/today', (req, res) => {
  try {
    const dateParam = req.query.date; // optional: ?date=2026-05-28
    const date = dateParam || new Date().toISOString().slice(0, 10);

    const capsule = getTodayCapsule(date);

    if (!capsule) {
      return res.json({ found: false, date, capsule: null });
    }

    // Parse tags back to array
    let tags = [];
    try { tags = JSON.parse(capsule.tags); } catch {}

    return res.json({
      found: true,
      date,
      capsule: {
        id: capsule.id,
        category: capsule.category,
        emoji: capsule.emoji,
        title_en: capsule.title_en,
        title_ar: capsule.title_ar,
        subtitle_en: capsule.subtitle_en,
        subtitle_ar: capsule.subtitle_ar,
        body_en: capsule.body_en,
        body_ar: capsule.body_ar,
        tip_en: capsule.tip_en,
        tip_ar: capsule.tip_ar,
        tags,
      }
    });

  } catch (err) {
    res.status(500).json({ error: 'Internal error', message: err.message });
  }
});

// GET /api/capsule/schedule?days=7
// Returns the upcoming published schedule (for preview widget)
router.get('/schedule', (req, res) => {
  try {
    const days = Math.min(parseInt(req.query.days) || 7, 30);
    const schedule = q.getSchedule.all(days);

    const result = schedule.map(row => ({
      date: row.date,
      capsule: {
        id: row.id,
        category: row.category,
        emoji: row.emoji,
        title_en: row.title_en,
        title_ar: row.title_ar,
      }
    }));

    res.json({ schedule: result });
  } catch (err) {
    res.status(500).json({ error: 'Internal error' });
  }
});

// GET /api/capsule/category/:cat
// Returns recent published capsules by category
router.get('/category/:cat', (req, res) => {
  try {
    const valid = ['meals', 'family', 'wellness', 'faith', 'money', 'living'];
    const cat = req.params.cat;
    if (!valid.includes(cat)) return res.status(400).json({ error: 'Invalid category' });

    const capsules = q.getCapsulesByCategory.all(cat);
    res.json({ category: cat, capsules });
  } catch (err) {
    res.status(500).json({ error: 'Internal error' });
  }
});

// GET /api/capsule/health
// Simple health check
router.get('/health', (req, res) => {
  res.json({ ok: true, system: 'd4l1-capsule-engine', ts: new Date().toISOString() });
});

module.exports = router;
