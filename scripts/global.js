/*!
 * DOTFORLIFE — Global Scripts
 * Runs on every page. Keep this lean — no framework deps.
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

  /* ── 2. Navbar scroll shadow ────────────────────────────── */
  var nav = document.getElementById('dfl-navbar');
  if (nav) {
    var onScroll = function () {
      nav.classList.toggle('scrolled', window.scrollY > 10);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── 3. Theme toggle ─────────────────────────────────────── */
  var themeBtn = document.getElementById('dfl-theme-btn');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var h = document.documentElement;
      var next = h.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      h.setAttribute('data-theme', next);
      localStorage.setItem('dfl-theme', next);
    });
  }

  /* ── 4. Language toggle ──────────────────────────────────── */
  var langBtn = document.getElementById('dfl-lang-btn');
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

  /* ── 5. Active mobile nav item ───────────────────────────── */
  var path = window.location.pathname;
  document.querySelectorAll('.dfl-mnav-item').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    if (href && path.includes(href.replace('/', ''))) {
      a.classList.add('active');
    }
  });

})();
