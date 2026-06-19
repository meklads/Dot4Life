/*!
 * DOTFORLIFE — Bilingual page redirect
 * When homepage links append ?lang=en, send users to the matching -en.html (or ar twin).
 * Must load synchronously in <head> after hreflang alternate links.
 */
(function () {
  'use strict';
  var p = new URLSearchParams(location.search);
  var req = p.get('lang');
  if (!req) return;

  var path = location.pathname;
  var isEnPage = /-en\.html$/i.test(path);
  var themeQs = p.get('theme') ? '?theme=' + encodeURIComponent(p.get('theme')) : '';

  function go(href) {
    if (!href) return;
    try {
      var target = new URL(href, location.origin);
      if (target.pathname === path) return;
      location.replace(target.pathname + themeQs);
    } catch (e) { /* ignore */ }
  }

  if (req === 'en' && !isEnPage) {
    var enLink = document.querySelector('link[rel="alternate"][hreflang="en"]');
    go(enLink && enLink.getAttribute('href'));
    return;
  }

  if (req === 'ar' && isEnPage) {
    var arLink = document.querySelector('link[rel="alternate"][hreflang="ar"]') ||
      document.querySelector('link[rel="alternate"][hreflang="ar-SA"]');
    go(arLink && arLink.getAttribute('href'));
  }
})();
