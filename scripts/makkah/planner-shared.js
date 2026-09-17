/**
 * Shared planner helpers for Makkah vertical tools (Tool 01–05).
 * Reuse this layer for every planner — do not fork a second shared copy.
 * Destination-specific rules live in each tool's *-engine.js only.
 * No framework — vanilla ES5-compatible browser JS.
 */
(function (global) {
  'use strict';

  function track(event, params) {
    try {
      if (typeof global.dflTrack === 'function') {
        global.dflTrack(event, params || {});
        return;
      }
      if (typeof global.gtag === 'function') {
        global.gtag('event', event, Object.assign({
          page_path: location.pathname,
          language: document.documentElement.getAttribute('data-lang') || 'en'
        }, params || {}));
      }
    } catch (e) { /* ignore */ }
  }

  function lang() {
    return document.documentElement.getAttribute('data-lang') === 'ar' ? 'ar' : 'en';
  }

  function t(pair) {
    if (!pair) return '';
    if (typeof pair === 'string') return pair;
    return pair[lang()] || pair.en || pair.ar || '';
  }

  function clamp(n, min, max) {
    n = Number(n);
    if (isNaN(n)) return min;
    return Math.max(min, Math.min(max, n));
  }

  function encodeState(obj) {
    try {
      return btoa(unescape(encodeURIComponent(JSON.stringify(obj))))
        .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    } catch (e) {
      return '';
    }
  }

  function decodeState(str) {
    try {
      if (!str) return null;
      str = str.replace(/-/g, '+').replace(/_/g, '/');
      while (str.length % 4) str += '=';
      return JSON.parse(decodeURIComponent(escape(atob(str))));
    } catch (e) {
      return null;
    }
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand('copy');
        resolve();
      } catch (err) {
        reject(err);
      }
      document.body.removeChild(ta);
    });
  }

  global.DFLPlannerShared = {
    track: track,
    lang: lang,
    t: t,
    clamp: clamp,
    encodeState: encodeState,
    decodeState: decodeState,
    copyText: copyText
  };
})(window);
