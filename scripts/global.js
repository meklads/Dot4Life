/*!
 * DOTFORLIFE, Global Scripts
 * Runs on every page. Keep this lean, no framework deps.
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
  var themeBtn = document.getElementById('dfl-theme-btn') || document.getElementById('theme-toggle') || document.getElementById('theme-toggle-mobile');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var h = document.documentElement;
      var next = h.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      h.setAttribute('data-theme', next);
      localStorage.setItem('dfl-theme', next);
      // Update ALL theme buttons on the page
      document.querySelectorAll('#theme-toggle, #theme-toggle-mobile, #dfl-theme-btn').forEach(function(btn) {
        if (btn) {
          var moon = btn.querySelector('.theme-icon-moon');
          var sun = btn.querySelector('.theme-icon-sun');
          if (moon && sun) {
            moon.style.display = next === 'dark' ? 'none' : 'block';
            sun.style.display = next === 'dark' ? 'block' : 'none';
          }
        }
      });
    });

    // Initialise theme icon visibility on page load
    (function initThemeIcons() {
      var h = document.documentElement;
      var current = h.getAttribute('data-theme') || 'light';
      document.querySelectorAll('#theme-toggle, #theme-toggle-mobile, #dfl-theme-btn').forEach(function(btn) {
        if (btn) {
          var moon = btn.querySelector('.theme-icon-moon');
          var sun = btn.querySelector('.theme-icon-sun');
          if (moon && sun) {
            moon.style.display = current === 'dark' ? 'none' : 'block';
            sun.style.display = current === 'dark' ? 'block' : 'none';
          }
        }
      });
    })();
  }

  /* ── 4. Language toggle (legacy + new ID) ───────────────── */
  function applyLanguage(targetLang) {
    var h = document.documentElement;
    h.setAttribute('data-lang', targetLang);
    h.setAttribute('lang', targetLang);
    h.setAttribute('dir', targetLang === 'ar' ? 'rtl' : 'ltr');
    localStorage.setItem('dfl-lang', targetLang);
    try {
      var url = new URL(window.location.href);
      url.searchParams.set('lang', targetLang);
      history.replaceState(null, '', url);
    } catch (e) { /* ignore */ }
    document.dispatchEvent(new CustomEvent('dfl:langchange', { detail: { lang: targetLang } }));
  }

  function getAlternateHref(targetLang) {
    var altLink = document.querySelector('link[rel="alternate"][hreflang="' + targetLang + '"]');
    if (!altLink && targetLang === 'ar') {
      altLink = document.querySelector('link[rel="alternate"][hreflang="ar-SA"]');
    }
    return altLink && altLink.getAttribute('href');
  }

  function hasSplitLangPages() {
    var enHref = getAlternateHref('en');
    var arHref = getAlternateHref('ar');
    if (!enHref || !arHref) return false;
    try {
      var enPath = new URL(enHref, location.origin).pathname;
      var arPath = new URL(arHref, location.origin).pathname;
      return enPath !== arPath;
    } catch (e) { return false; }
  }

  function bindLangToggle(langBtn) {
    if (!langBtn || langBtn.dataset.dflLangBound === '1') return;
    langBtn.dataset.dflLangBound = '1';
    langBtn.addEventListener('click', function () {
      var h = document.documentElement;
      var currentLang = h.getAttribute('data-lang') || 'en';
      var targetLang = currentLang === 'ar' ? 'en' : 'ar';

      // Separate ar.html / -en.html twins: always navigate (nav spans alone are not bilingual body)
      if (hasSplitLangPages()) {
        var twinHref = getAlternateHref(targetLang);
        if (twinHref) {
          window.location.href = twinHref;
          return;
        }
      }

      var hasBilingualSpans = document.querySelector('span.en, span.ar');

      // Bilingual span pages: toggle in-place (no full reload)
      if (hasBilingualSpans) {
        applyLanguage(targetLang);
        return;
      }

      // Legacy pages: navigate via hreflang when available
      var altLink = document.querySelector('link[rel="alternate"][hreflang="' + targetLang + '"]');
      if (!altLink && targetLang === 'ar') {
        altLink = document.querySelector('link[rel="alternate"][hreflang="ar-SA"]');
      }
      if (altLink && altLink.getAttribute('href')) {
        window.location.href = altLink.getAttribute('href');
        return;
      }

      applyLanguage(targetLang);
    });
  }

  document.querySelectorAll('#dfl-lang-btn, #lang-toggle, #lang-toggle-mobile').forEach(bindLangToggle);

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

  /* ── 7. Google Analytics 4, auto events ────────────── */
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

  // ── 8. Mobile hamburger menu toggle ──────────────────────
  (function() {
    var hamburger = document.getElementById('hamburger-btn');
    var dropdown  = document.getElementById('mobile-dropdown');
    if (!hamburger || !dropdown) return;

    function toggleMenu(e) {
      e.stopPropagation();
      var open = dropdown.classList.toggle('open');
      hamburger.classList.toggle('open', open);
      hamburger.setAttribute('aria-expanded', open);
      document.body.classList.toggle('menu-open', open);
    }
    function closeMenu() {
      dropdown.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('menu-open');
    }

    hamburger.addEventListener('click', toggleMenu);
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeMenu();
    });
    dropdown.addEventListener('click', function(e) {
      if (e.target === dropdown) closeMenu();
    });

    // Close menu when a nav link is clicked
    dropdown.querySelectorAll('.md-links a').forEach(function(a) {
      a.addEventListener('click', closeMenu);
    });
  })();

  /* ── 10. Back-to-top button (Medium/Verywell inspired) ─── */
  (function() {
    var btn = document.createElement('button');
    btn.id = 'dfl-back-to-top';
    btn.setAttribute('aria-label', 'Back to top');
    btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>';
    btn.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:999;width:44px;height:44px;border-radius:12px;border:none;background:var(--gold,#b8861a);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;opacity:0;transform:translateY(12px);transition:opacity .3s,transform .3s;box-shadow:0 4px 16px rgba(0,0,0,.15);pointer-events:none;';
    document.body.appendChild(btn);

    var ticking = false;
    window.addEventListener('scroll', function() {
      if (!ticking) {
        requestAnimationFrame(function() {
          if (window.scrollY > 600) {
            btn.style.opacity = '1';
            btn.style.transform = 'translateY(0)';
            btn.style.pointerEvents = 'auto';
          } else {
            btn.style.opacity = '0';
            btn.style.transform = 'translateY(12px)';
            btn.style.pointerEvents = 'none';
          }
          ticking = false;
        });
        ticking = true;
      }
    });

    btn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  })();

  /* ── 12. Scroll-aware navbar (homepage only — hide on scroll down) ────── */
  (function() {
    var body = document.body;
    if (!body.classList.contains('index-page')) return;
    if (body.classList.contains('category-page')) return;
    if (body.classList.contains('about-page')) return;
    if (body.classList.contains('archive-page')) return;

    var nav = document.getElementById('navbar') || document.getElementById('dfl-navbar');
    if (!nav) return;
    var lastScroll = 0;
    var ticking = false;

    window.addEventListener('scroll', function() {
      if (!ticking) {
        requestAnimationFrame(function() {
          var currentScroll = window.scrollY;
          if (currentScroll > 100) {
            if (currentScroll > lastScroll) {
              nav.style.transform = 'translateY(-100%)';
              nav.style.transition = 'transform .3s ease';
            } else {
              nav.style.transform = 'translateY(0)';
            }
          } else {
            nav.style.transform = 'translateY(0)';
          }
          lastScroll = currentScroll;
          ticking = false;
        });
        ticking = true;
      }
    });
  })();

  // ── 9. Broadcast custom event for other scripts ──────────
  // Let other scripts know GA4 events are ready
  document.dispatchEvent(new CustomEvent('dfl:analytics-ready', { detail: { id: 'G-3G1XPV4F0G' } }));

})();
