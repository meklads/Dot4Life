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

})();
