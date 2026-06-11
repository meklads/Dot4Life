/**
 * DOTFORLIFE, universal tool share bar
 * Auto-detects a tool's result card and injects "Share on WhatsApp" + "Save / Print"
 * buttons. Bilingual (reads <html data-lang>). Non-breaking: if no result card is
 * found, nothing is injected. The share message includes the tool name, a short
 * result summary, and the page URL.
 */
(function () {
  'use strict';

  var RESULT_SELECTORS = [
    '#resultsCard', '#resultsSection', '#results-section', '#resultCard',
    '#results', '.results-card', '.results-section', '.result-section',
    '.result-box', '.result-card'
  ];
  var VISIBLE_CLASSES = ['show', 'active', 'visible', 'is-visible'];

  function findResult() {
    for (var i = 0; i < RESULT_SELECTORS.length; i++) {
      var el = document.querySelector(RESULT_SELECTORS[i]);
      if (el) return el;
    }
    return null;
  }

  function isVisible(el) {
    if (!el) return false;
    for (var i = 0; i < VISIBLE_CLASSES.length; i++) {
      if (el.classList.contains(VISIBLE_CLASSES[i])) return true;
    }
    // fall back to computed visibility / size
    var r = el.getBoundingClientRect();
    var st = window.getComputedStyle(el);
    return st.display !== 'none' && st.visibility !== 'hidden' && r.height > 8;
  }

  function lang() {
    return document.documentElement.getAttribute('data-lang') === 'ar' ? 'ar' : 'en';
  }

  function toolName() {
    var h1 = document.querySelector('h1');
    if (h1) {
      var ar = h1.querySelector('.ar'), en = h1.querySelector('.en');
      if (lang() === 'ar' && ar && ar.textContent.trim()) return ar.textContent.trim();
      if (en && en.textContent.trim()) return en.textContent.trim();
      return h1.textContent.replace(/\s+/g, ' ').trim();
    }
    return (document.title || 'DOTFORLIFE').split('|')[0].split(',')[0].trim();
  }

  function resultSummary(card) {
    // collect visible result rows (label: value), capped for a tidy WhatsApp message
    var parts = [];
    var rows = card.querySelectorAll('.result-row, .results-divider ~ *, .result-value, .result-number, .kpi-value, .stat-number, .result-main');
    if (rows.length) {
      card.querySelectorAll('.result-row').forEach(function (row) {
        var t = row.textContent.replace(/\s+/g, ' ').trim();
        if (t) parts.push(t);
      });
    }
    if (!parts.length) {
      var txt = card.textContent.replace(/\s+/g, ' ').trim();
      if (txt) parts.push(txt);
    }
    var msg = parts.join('\n');
    if (msg.length > 320) msg = msg.slice(0, 317) + '…';
    return msg;
  }

  function injectStyles() {
    if (document.getElementById('dfl-share-css')) return;
    var s = document.createElement('style');
    s.id = 'dfl-share-css';
    s.textContent =
      '.dfl-share-bar{display:flex;gap:.6rem;flex-wrap:wrap;justify-content:center;margin:1.4rem auto 0;}' +
      '.dfl-share-bar button{display:inline-flex;align-items:center;gap:.5rem;border:0;cursor:pointer;' +
      'font:600 .95rem/1 inherit;padding:.7rem 1.15rem;border-radius:999px;transition:transform .15s ease,filter .15s ease;}' +
      '.dfl-share-bar button:hover{transform:translateY(-1px);filter:brightness(1.05);}' +
      '.dfl-share-wa{background:#25D366;color:#fff;}' +
      '.dfl-share-print{background:transparent;color:#054241;border:2px solid #054241 !important;}' +
      '.dfl-share-bar svg{width:18px;height:18px;flex:0 0 auto;}' +
      '@media print{.dfl-share-bar,#navbar,#dfl-navbar,nav,footer,.dfl-footer{display:none !important;}}';
    document.head.appendChild(s);
  }

  function makeBar(card) {
    if (card.querySelector('.dfl-share-bar') || document.querySelector('.dfl-share-bar')) return;
    var ar = lang() === 'ar';
    var bar = document.createElement('div');
    bar.className = 'dfl-share-bar';

    var wa = document.createElement('button');
    wa.type = 'button';
    wa.className = 'dfl-share-wa';
    wa.innerHTML =
      '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.82 11.82 0 018.413 3.488 11.824 11.824 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.86 9.86 0 001.51 5.26l-.999 3.648 3.477-.917zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>' +
      (ar ? '<span>شارك على واتساب</span>' : '<span>Share on WhatsApp</span>');
    wa.addEventListener('click', function () {
      var msg = toolName() + '\n' + resultSummary(card) + '\n\n' + location.href;
      window.open('https://wa.me/?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    });

    var pr = document.createElement('button');
    pr.type = 'button';
    pr.className = 'dfl-share-print';
    pr.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>' +
      (ar ? '<span>حفظ / طباعة PDF</span>' : '<span>Save / Print PDF</span>');
    pr.addEventListener('click', function () { window.print(); });

    bar.appendChild(wa);
    bar.appendChild(pr);
    card.appendChild(bar);
  }

  function watch() {
    var card = findResult();
    if (!card) return;
    injectStyles();
    if (isVisible(card)) makeBar(card);
    var mo = new MutationObserver(function () {
      if (isVisible(card)) makeBar(card);
    });
    mo.observe(card, { attributes: true, attributeFilter: ['class', 'style'], childList: true, subtree: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', watch);
  } else {
    watch();
  }
})();
