/*!
 * DOTFORLIFE — Global Scripts
 * Runs on every page. Keep this lean — no framework deps.
 *
 * Supports both legacy IDs (theme-toggle, lang-toggle, navbar)
 * and new prefixed IDs (dfl-theme-btn, dfl-lang-btn, dfl-navbar).
 */

(function () {
  'use strict';

  /* ── 1. Scroll-reveal observer ─────────────────────────── */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(function (el) {
      io.observe(el);
    });
  } else {
    // Fallback: show all reveal elements immediately
    document.querySelectorAll('.reveal').forEach(function (el) {
      el.classList.add('visible');
    });
  }

  /* ── 2. Navbar scroll shadow (legacy + new ID) ─────────── */
  var nav = document.getElementById('dfl-navbar') || document.getElementById('navbar');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('scrolled', window.scrollY > 10);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── 3. Theme toggle (legacy + new ID) ──────────────────── */
  var themeBtn = document.getElementById('dfl-theme-btn') || document.getElementById('theme-toggle');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var h = document.documentElement;
      var next = h.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      h.setAttribute('data-theme', next);
      localStorage.setItem('dfl-theme', next);
      // Update button icon — supports emoji and short-text formats
      if (themeBtn.textContent.trim() === '🌙' || themeBtn.textContent.trim() === '☀️') {
        themeBtn.textContent = next === 'dark' ? '☀️' : '🌙';
      }
    });
  }

  /* ── 4. Language toggle (legacy + new ID) ───────────────── */
  var langBtn = document.getElementById('dfl-lang-btn') || document.getElementById('lang-toggle');
  if (langBtn) {
    langBtn.addEventListener('click', function () {
      var h = document.documentElement;
      var next = h.getAttribute('data-lang') === 'ar' ? 'en' : 'ar';
      h.setAttribute('data-lang', next);
      h.setAttribute('lang', next);
      h.setAttribute('dir', next === 'ar' ? 'rtl' : 'ltr');
      localStorage.setItem('dfl-lang', next);
      // Update button text — toggle between language labels
      var txt = langBtn.textContent.trim();
      if (txt === 'العربية' || txt === 'English' || txt === 'AR' || txt === 'EN') {
        langBtn.textContent = next === 'ar' ? 'English' : 'العربية';
      }
    });
  }

  /* ── 5. Active nav item (both main nav + mobile nav) ────── */
  var path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a, .dfl-mnav-item, .sub-nav a').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    if (href && path === href.split('/').pop()) {
      a.classList.add('active');
    }
  });

  /* ── 6. Preserve language across internal links ──────────── */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    // Only intercept internal relative links
    if (href.startsWith('/') || href.startsWith('./') || href.startsWith('../')) {
      var lang = document.documentElement.getAttribute('data-lang');
      if (lang && href.indexOf('lang=') === -1) {
        var sep = href.indexOf('?') > -1 ? '&' : '?';
        a.href = href + sep + 'lang=' + lang;
      }
    }
  });

  /* ── 7. Google Analytics 4 — auto events ────────────── */
  if (typeof gtag === 'function') {
    var pagePath = window.location.pathname;
    var pageTitle = document.title;

    // ── 7a. Language switches ──────────────────────────────
    var langBtn = document.getElementById('dfl-lang-btn') || document.getElementById('lang-toggle');
    if (langBtn) {
      langBtn.addEventListener('click', function () {
        var currentLang = document.documentElement.getAttribute('data-lang') === 'ar' ? 'en' : 'ar';
        gtag('event', 'language_switch', { 'language': currentLang, 'page_path': pagePath });
      });
    }

    // ── 7b. Theme switches ─────────────────────────────────
    var themeBtn = document.getElementById('dfl-theme-btn') || document.getElementById('theme-toggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', function () {
        var nextTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        gtag('event', 'theme_switch', { 'theme': nextTheme, 'page_path': pagePath });
      });
    }

    // ── 7c. Page engagement (time on page) ────────────────
    [30, 60, 120].forEach(function (sec) {
      setTimeout(function () {
        gtag('event', 'engagement', {
          'seconds': sec,
          'page_path': pagePath,
          'page_title': pageTitle
        });
      }, sec * 1000);
    });

    // ── 7d. Scroll depth ────────────────────────────────────
    var scrolledDepths = {};
    window.addEventListener('scroll', function () {
      var pct = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
      [25, 50, 75, 100].forEach(function (d) {
        if (pct >= d && !scrolledDepths[d]) {
          scrolledDepths[d] = true;
          gtag('event', 'scroll_depth', { 'percent': d, 'page_path': pagePath });
        }
      });
    }, { passive: true });

    // ── 7e. Tool/calculator usage ──────────────────────────
    // Detects when a user submits/interacts with calculator forms
    document.addEventListener('submit', function (e) {
      var form = e.target;
      if (form && form.closest('.calculator, .tool-card, [class*="calc"], [class*="tool"]')) {
        gtag('event', 'tool_use', {
          'tool_name': pageTitle,
          'action': 'submit',
          'page_path': pagePath
        });
      }
    });

    // ── 7f. Outbound links ─────────────────────────────────
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a) return;
      var href = a.getAttribute('href') || '';
      if (href.startsWith('http') && !href.includes(window.location.hostname)) {
        gtag('event', 'outbound_click', {
          'link_url': href,
          'link_text': (a.textContent || '').trim().substring(0, 60),
          'page_path': pagePath
        });
      }
    });

    // ── 7g. Save/bookmark interactions ─────────────────────
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[id*="save"], [id*="bookmark"], [class*="save"], [class*="bookmark"]');
      if (btn) {
        gtag('event', 'save_item', {
          'page_path': pagePath,
          'page_title': pageTitle
        });
      }
    });

  }

  // ── 8. Broadcast custom event for other scripts ──────────
  // Let other scripts know GA4 events are ready
  document.dispatchEvent(new CustomEvent('dfl:analytics-ready', { detail: { id: 'G-3G1XPV4F0G' } }));

})();
