/**
 * d4l1-capsule-engine, Frontend Fetch Layer
 * Fetches today's published capsule and injects it into the index.html UI.
 * NON-BREAKING: if API fails, the static fallback remains unchanged.
 */

(function () {
  'use strict';

  const API_URL  = 'https://dot4life-production.up.railway.app/api/capsule/today';
  const TIMEOUT  = 10000;

  const lang  = document.documentElement.getAttribute('data-lang') || 'en';
  const today = new Date().toISOString().slice(0, 10);

  fetch(`${API_URL}?date=${today}`, { signal: AbortSignal.timeout(TIMEOUT) })
    .then(r => r.json())
    .then(data => {
      if (!data.found || !data.capsule) return;
      inject(data.capsule);
    })
    .catch(() => { /* API not reachable, static fallback stays */ });

  function inject(c) {
    const isAr = document.documentElement.getAttribute('data-lang') === 'ar';

    // ── 1. TRIGGER BUTTON (mm-capsule) ──────────────────────────
    const trigger = document.getElementById('mm-capsule-trigger');
    if (trigger) {
      const icon = trigger.querySelector('.mm-capsule-icon');
      if (icon) icon.textContent = c.emoji || '🌿';

      const titleEn = trigger.querySelector('.mm-capsule-title .en');
      const titleAr = trigger.querySelector('.mm-capsule-title .ar');
      if (titleEn) titleEn.textContent = c.title_en;
      if (titleAr) titleAr.textContent = c.title_ar;
      if (!titleEn) {
        const t = trigger.querySelector('.mm-capsule-title');
        if (t) t.textContent = isAr ? c.title_ar : c.title_en;
      }
    }

    // ── 2. POPUP CARD ────────────────────────────────────────────
    const card = document.getElementById('capsule-card');
    if (!card) return;

    const popEmoji = card.querySelector('.capsule-img-emoji');
    if (popEmoji) popEmoji.textContent = c.emoji || '🌿';

    const tag = card.querySelector('.capsule-tag');
    if (tag) {
      const catLabels = {
        meals:   {en:'Meals & Nutrition', ar:'التغذية والوجبات'},
        family:  {en:'Family',            ar:'الأسرة'},
        wellness:{en:'Wellness',          ar:'الصحة والعافية'},
        faith:   {en:'Faith',             ar:'الإيمان'},
        money:   {en:'Money',             ar:'المال'},
        living:  {en:'Daily Living',      ar:'الحياة اليومية'},
      };
      const cat = catLabels[c.category] || {en: c.category, ar: c.category};
      const tagEn = tag.querySelector('.en');
      const tagAr = tag.querySelector('.ar');
      if (tagEn) tagEn.textContent = cat.en;
      if (tagAr) tagAr.textContent = cat.ar;
      if (!tagEn) tag.textContent = isAr ? cat.ar : cat.en;
    }

    const titleEn = card.querySelector('.capsule-title .en');
    const titleAr = card.querySelector('.capsule-title .ar');
    if (titleEn) titleEn.textContent = c.title_en;
    if (titleAr) titleAr.textContent = c.title_ar;

    const descEn = card.querySelector('.capsule-desc .en');
    const descAr = card.querySelector('.capsule-desc .ar');
    if (descEn) descEn.textContent = c.subtitle_en || c.body_en || '';
    if (descAr) descAr.textContent = c.subtitle_ar || c.body_ar || '';

    const sections = card.querySelectorAll('.capsule-section');
    sections.forEach(s => s.style.display = 'none');

    if (c.tip_en) {
      const tipSection = document.createElement('div');
      tipSection.className = 'capsule-section';
      tipSection.style.cssText = 'margin-top:12px;padding:12px 14px;background:rgba(42,154,152,.06);border-radius:10px;border-inline-start:3px solid var(--gold,#6abfb8);';
      tipSection.innerHTML = `
        <div class="capsule-section-title" style="margin-bottom:6px;">
          <span class="en">💡 Today's Tip</span><span class="ar">💡 نصيحة اليوم</span>
        </div>
        <p style="font-size:.85rem;color:var(--text-2,#44474D);line-height:1.6;">
          <span class="en">${c.tip_en}</span><span class="ar">${c.tip_ar || c.tip_en}</span>
        </p>`;
      const footer = card.querySelector('.capsule-footer');
      if (footer) card.insertBefore(tipSection, footer);
    }

    const fullBtn = card.querySelector('.capsule-btn-full');
    if (fullBtn) {
      fullBtn.href = `/capsule.html?id=${c.id}`;
      const btnEn = fullBtn.querySelector('.en');
      const btnAr = fullBtn.querySelector('.ar');
      if (btnEn) btnEn.textContent = 'Full Capsule →';
      if (btnAr) btnAr.textContent = '→ التذكرة كاملة';
      if (!btnEn) fullBtn.textContent = isAr ? '→ التذكرة كاملة' : 'Full Capsule →';
    }

    card.setAttribute('data-source', 'api');
    card.setAttribute('data-capsule-id', c.id);
  }

})();
