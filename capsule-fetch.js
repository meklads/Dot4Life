/**
 * d4l1-capsule-engine — Frontend Fetch Layer
 * NON-BREAKING integration with d4l1 stable system.
 *
 * HOW IT WORKS:
 *   1. Tries to fetch today's published capsule from the API
 *   2. If API responds with a capsule → replaces the static capsule on screen
 *   3. If API is down / no capsule today → static d4l1 system remains untouched
 *
 * Add to index.html just before </body>:
 *   <script src="/capsule-fetch.js"></script>
 *
 * The existing static capsule system continues to work as fallback — always.
 */

(function () {
  'use strict';

  // ── CONFIG ─────────────────────────────
  // Change this URL to where your capsule-engine server is running
  const API_URL = 'http://localhost:3030/api/capsule/today';
  const TIMEOUT_MS = 2500; // Give up after 2.5s — never block page load

  // ── ABORT if no capsule container on page ──
  const card = document.querySelector('.capsule-card, [data-capsule]');
  if (!card) return;

  // ── FETCH WITH TIMEOUT ─────────────────
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  const lang = document.documentElement.getAttribute('data-lang') || 'en';
  const today = new Date().toISOString().slice(0, 10);

  fetch(`${API_URL}?date=${today}`, { signal: controller.signal })
    .then(r => { clearTimeout(timer); return r.json(); })
    .then(data => {
      if (!data.found || !data.capsule) return; // No capsule today — keep static
      injectCapsule(data.capsule, lang);
    })
    .catch(() => {
      // API down or timeout — d4l1 static system remains, no error shown
    });

  // ─────────────────────────────────────────
  //  INJECT PUBLISHED CAPSULE INTO EXISTING UI
  //  Matches the DOM structure of d4l1 index.html capsule card
  // ─────────────────────────────────────────
  function injectCapsule(c, lang) {
    const isAr = lang === 'ar';
    const title    = isAr ? c.title_ar    : c.title_en;
    const subtitle = isAr ? c.subtitle_ar : c.subtitle_en;
    const body     = isAr ? c.body_ar     : c.body_en;
    const tip      = isAr ? c.tip_ar      : c.tip_en;

    if (!title) return; // Incomplete capsule — keep static

    // Update emoji
    const emojiEl = card.querySelector('.capsule-emoji, [data-capsule-emoji]');
    if (emojiEl) emojiEl.textContent = c.emoji || '🌿';

    // Update title (handles bilingual .en/.ar spans)
    const titleEn = card.querySelector('.capsule-title .en, [data-capsule-title-en]');
    const titleAr = card.querySelector('.capsule-title .ar, [data-capsule-title-ar]');
    if (titleEn) titleEn.textContent = c.title_en;
    if (titleAr) titleAr.textContent = c.title_ar;

    // Fallback: single title element
    const titleEl = card.querySelector('.capsule-title');
    if (titleEl && !titleEn) titleEl.textContent = title;

    // Update subtitle
    const subEn = card.querySelector('.capsule-subtitle .en, [data-capsule-sub-en]');
    const subAr = card.querySelector('.capsule-subtitle .ar, [data-capsule-sub-ar]');
    if (subEn) subEn.textContent = c.subtitle_en;
    if (subAr) subAr.textContent = c.subtitle_ar;
    const subEl = card.querySelector('.capsule-subtitle');
    if (subEl && !subEn) subEl.textContent = subtitle;

    // Update body if present
    const bodyEn = card.querySelector('.capsule-body .en, [data-capsule-body-en]');
    const bodyAr = card.querySelector('.capsule-body .ar, [data-capsule-body-ar]');
    if (bodyEn) bodyEn.textContent = c.body_en;
    if (bodyAr) bodyAr.textContent = c.body_ar;

    // Update tip if present
    const tipEl = card.querySelector('.capsule-tip, [data-capsule-tip]');
    if (tipEl) tipEl.textContent = tip;

    // Mark card as API-sourced (for debugging only — no visual change)
    card.setAttribute('data-source', 'api');
    card.setAttribute('data-capsule-id', c.id);
  }

})();
