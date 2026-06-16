/* ═════════════════════════════════════════════════════
   feed.js v2 — Universal Article Feed
   Reads /articles.json and renders:
   · Homepage: 3 section feeds (قصص/مقارنات/السلام) + general latest
   · Section pages: category-filtered cards
   · Blog + Archive: full chronological list
   Auto-updates: any new line in articles.json shows instantly
   ═════════════════════════════════════════════════════ */

(function() {
  'use strict';

  var FEED_VERSION = 6;  // v6: supports type field filter for section feeds

  var CONFIG = {
    jsonUrl: '/articles.json',
    containerSelector: '#latest-articles .hl-article-grid',
    maxItems: 6,
    blogListMax: 50,
    sectionFeedMax: 3,
    cacheKey: 'dfl-cache-v' + FEED_VERSION,
    cacheTTL: 600000
  };

  var articles = [];
  var isAr = document.documentElement.getAttribute('data-lang') === 'ar';
  var currentPage = window.location.pathname;

  /* Clear any stale old-version caches */
  try { localStorage.removeItem('dfl-feed-cache'); } catch(e){}
  try { localStorage.removeItem('dfl-feed-cache-v1'); } catch(e){}
  try { localStorage.removeItem('dfl-feed-cache-v2'); } catch(e){}
  try { localStorage.removeItem('dfl-feed-cache-v3'); } catch(e){}
  try { localStorage.removeItem('dfl-feed-cache-v4'); } catch(e){}

  /* ═══ Page Type ═══ */

  function getPageType() {
    var page = currentPage.replace(/\/$/, '');
    if (page === '' || page.endsWith('index.html')) return 'home';
    if (page.endsWith('blog.html')) return 'blog';
    if (page.endsWith('health.html')) return 'health';
    if (page.endsWith('finance.html')) return 'finance';
    if (page.endsWith('real-estate.html')) return 'real-estate';
    if (page.endsWith('travel.html')) return 'travel';
    if (page.endsWith('islamic.html')) return 'islamic';
    if (page.endsWith('family.html')) return 'family';
    if (page.endsWith('fitness.html')) return 'fitness';
    if (page.endsWith('productivity.html')) return 'productivity';
    if (page.endsWith('plants.html')) return 'plants';
    if (page.endsWith('archive.html')) return 'archive';
    return 'other';
  }

  /* ═══ Data Fetching (XHR + localStorage cache 10 min) ═══ */

  function fetchArticles(callback) {
    try {
      var cached = localStorage.getItem(CONFIG.cacheKey);
      if (cached) {
        var data = JSON.parse(cached);
        if (Date.now() - data.timestamp < CONFIG.cacheTTL) {
          articles = data.articles;
          callback();
          return;
        }
      }
    } catch(e) {}

    /* Add cache-busting to prevent browser from caching JSON */
    var bustUrl = CONFIG.jsonUrl + '?_=' + Date.now();
    var xhr = new XMLHttpRequest();
    xhr.open('GET', bustUrl, true);
    xhr.setRequestHeader('Cache-Control', 'no-cache, must-revalidate');
    xhr.setRequestHeader('Pragma', 'no-cache');
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          articles = JSON.parse(xhr.responseText);
          if (!articles || !articles.length) {
            console.warn('feed.js: empty articles.json - static fallback preserved');
            return;
          }
          try {
            localStorage.setItem(CONFIG.cacheKey, JSON.stringify({
              articles: articles,
              timestamp: Date.now()
            }));
          } catch(e) {}
          try { callback(); } catch(renderErr) {
            console.warn('feed.js: render error', renderErr);
          }
        } catch(e) {
          console.warn('feed.js: invalid JSON - static fallback preserved', bustUrl, e);
          try { localStorage.removeItem(CONFIG.cacheKey); } catch(ce){}
          /* no callback - static fallback stays */
        }
      } else {
        console.warn('feed.js: HTTP ' + xhr.status + ' - static fallback preserved', bustUrl);
        try { localStorage.removeItem(CONFIG.cacheKey); } catch(ce){}
        /* no callback - static fallback stays */
      }
    };
    xhr.onerror = function() {
      console.warn('feed.js: network error - static fallback preserved');
      try { localStorage.removeItem(CONFIG.cacheKey); } catch(ce){}
      /* no callback - static fallback stays */
    };
    xhr.send();
  }

  /* ═══ Article Filtering ═══ */

  /** Filter by page type (category-based for section pages) */
  function getFilteredArticles(pageType) {
    if (pageType === 'blog' || pageType === 'archive') {
      return articles.slice().sort(function(a, b) {
        return new Date(b.date) - new Date(a.date);
      });
    }

    var catMap = {
      health: 'health', finance: 'finance', 'real-estate': 'real-estate',
      travel: 'travel', islamic: 'islamic', family: 'family',
      fitness: 'fitness', productivity: 'productivity', plants: 'plants'
    };

    var cat = catMap[pageType] || '';
    var filtered = articles.filter(function(a) { return a.category === cat; });

    if (filtered.length < 3) {
      filtered = articles.slice().sort(function(a, b) {
        return new Date(b.date) - new Date(a.date);
      });
    } else {
      filtered.sort(function(a, b) {
        return new Date(b.date) - new Date(a.date);
      });
    }
    return filtered;
  }

  /** Filter articles by `section` or `type` field for homepage section feeds */
  function getSectionArticles(sectionName) {
    return articles
      .filter(function(a) { return a.section === sectionName || a.type === sectionName; })
      .sort(function(a, b) { return new Date(b.date) - new Date(a.date); });
  }

  /* ═══ HTML Builders ═══ */

  function buildCardHTML(a) {
    var title = isAr && a.title_ar ? a.title_ar : a.title_en;
    var excerpt = isAr && a.excerpt_ar ? a.excerpt_ar : a.excerpt_en;
    var url = a.url || '#';
    var section = isAr && a.section_ar ? a.section_ar : a.section;
    var img = a.img || '/assets/images/hero.webp';

    return '<a href="' + url + '" class="hl-art-card">' +
      '<img class="hl-art-card-img" src="' + img + '" alt="" width="600" height="340" loading="lazy">' +
      '<div class="hl-art-card-body">' +
      '<span class="hl-art-card-kicker">' + esc(section) + '</span>' +
      '<span class="hl-art-card-title">' + esc(title) + '</span>' +
      (excerpt ? '<span class="hl-art-card-desc">' + esc(excerpt) + '</span>' : '') +
      '<span class="hl-art-card-arrow">' + (isAr ? '→ اقرأ المقال' : 'Read article →') + '</span>' +
      '</div></a>';
  }

  function buildListItemHTML(a) {
    var title = isAr && a.title_ar ? a.title_ar : a.title_en;
    var url = a.url || '#';
    var section = isAr && a.section_ar ? a.section_ar : a.section;
    var img = a.img || '/assets/images/hero.webp';

    return '<a href="' + url + '" class="blog-list-item">' +
      '<span class="blog-list-img" style="background-image:url(' + img + ')"></span>' +
      '<span class="blog-list-body">' +
      '<span class="blog-list-kicker">' + esc(section) + '</span>' +
      '<span class="blog-list-title">' + esc(title) + '</span>' +
      '<span class="blog-list-meta">' + fmtDate(a.date) + '</span>' +
      '</span></a>';
  }

  /* ═══ Utilities ═══ */

  function esc(s) {
    if (!s) return '';
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
                    .replace(/"/g,'&quot;').replace(/'/g,'&#039;');
  }

  function fmtDate(ds) {
    if (!ds) return '';
    var d = new Date(ds);
    if (isNaN(d.getTime())) return ds;
    return d.toLocaleDateString(isAr ? 'ar-SA' : 'en-US', {
      year: 'numeric', month: 'short', day: 'numeric'
    });
  }

  /* ═══ Unified Section Slot Render ═══
     Renders each [data-feed-section] container based on its data-role:
     - hero:     Latest article[0] into the featured card
     - list:     Articles[1..N] into list items (skip article[0] for hero)
     - default:  Articles[0..N-1] into grid cards
     Injects content into EXISTING child elements (static fallback preserved).
     Sorted by date descending.  ═══ */

  function renderHeroSlot(container, a) {
    var title_en = a.title_en || '';
    var title_ar = a.title_ar || title_en;
    var sect_en = a.section || 'Featured';
    var sect_ar = a.section_ar || sect_en;
    var href = isAr && a.url ? a.url : (a.url_en || a.url || '#');
    var img = a.img || '';

    var imgEl = container.querySelector('.sl-featured-img img');
    if (imgEl && img) { imgEl.src = img; imgEl.setAttribute('src', img); }

    var kickerEn = container.querySelector('.sl-featured-kicker .en');
    var kickerAr = container.querySelector('.sl-featured-kicker .ar');
    if (kickerEn) kickerEn.textContent = sect_en;
    if (kickerAr) kickerAr.textContent = sect_ar;

    var titleElEn = container.querySelector('.sl-featured-title .en');
    var titleElAr = container.querySelector('.sl-featured-title .ar');
    if (titleElEn) titleElEn.textContent = title_en;
    if (titleElAr) titleElAr.textContent = title_ar;

    var bylineEn = container.querySelector('.sl-featured-byline .en');
    var bylineAr = container.querySelector('.sl-featured-byline .ar');
    if (bylineEn) bylineEn.textContent = (a.section || 'Family') + ' · Dot4Life';
    if (bylineAr) bylineAr.textContent = (a.section_ar || 'العائلة') + ' · دوت فور لايف';

    container.href = href;
    container.setAttribute('data-en-href', a.url_en || a.url || '#');
    container.setAttribute('data-ar-href', a.url || '#');
  }

  function renderListSlot(container, items) {
    var children = container.children;
    if (!children.length) return;
    for (var i = 0; i < items.length && i < children.length; i++) {
      var el = children[i];
      var a = items[i];
      var url = a.url || '#';
      var url_en = a.url_en || a.url || '#';
      var href = isAr ? url : url_en;
      var byline_ar = (a.section_ar || a.category || '') + ' · دوت فور لايف';
      var byline_en = (a.section || a.category || '') + ' · Dot4Life';

      var titleEn = el.querySelector('.sl-latest-item-title .en');
      var titleAr = el.querySelector('.sl-latest-item-title .ar');
      if (titleEn) titleEn.textContent = a.title_en || '';
      if (titleAr) titleAr.textContent = a.title_ar || a.title_en || '';

      var blEn = el.querySelector('.sl-latest-item-byline .en');
      var blAr = el.querySelector('.sl-latest-item-byline .ar');
      if (blEn) blEn.textContent = byline_en;
      if (blAr) blAr.textContent = byline_ar;

      el.href = href;
      el.setAttribute('data-en-href', url_en);
      el.setAttribute('data-ar-href', url);
    }
  }

  function renderGridSlot(container, items) {
    var children = container.children;
    if (!children.length) return;
    for (var i = 0; i < items.length && i < children.length; i++) {
      var el = children[i];
      var a = items[i];
      var title_en = a.title_en || '';
      var title_ar = a.title_ar || title_en;
      var cat_en = a.section || a.category || '';
      var cat_ar = a.section_ar || a.section || cat_en;
      var url = a.url || '#';
      var url_en = a.url_en || a.url || '#';
      var href = isAr ? url : url_en;
      var img = a.img || '';

      var imgEl = el.querySelector('.dc-item-single img') || el.querySelector('.dc-item-split img');
      if (imgEl && img) { imgEl.src = img; imgEl.setAttribute('src', img); }

      var catElEn = el.querySelector('.dc-item-cat .en');
      var catElAr = el.querySelector('.dc-item-cat .ar');
      if (catElEn) catElEn.textContent = cat_en;
      if (catElAr) catElAr.textContent = cat_ar;

      var titleElEn = el.querySelector('.dc-item-title .en');
      var titleElAr = el.querySelector('.dc-item-title .ar');
      if (titleElEn) titleElEn.textContent = title_en;
      if (titleElAr) titleElAr.textContent = title_ar;

      el.href = href;
      el.setAttribute('data-en-href', url_en);
      el.setAttribute('data-ar-href', url);
    }
  }

  function renderSectionSlots() {
    var containers = document.querySelectorAll('[data-feed-section]');
    if (!containers.length) {
      console.log('feed.js: no [data-feed-section] found');
      return;
    }

    for (var j = 0; j < containers.length; j++) {
      var container = containers[j];
      var section = container.getAttribute('data-feed-section');
      var role = container.getAttribute('data-role');
      var count = parseInt(container.getAttribute('data-count'), 10) || 1;
      if (!section) continue;

      var sectionArticles = getSectionArticles(section);
      if (!sectionArticles.length) continue;

      if (role === 'hero') {
        renderHeroSlot(container, sectionArticles[0]);
      } else if (role === 'list') {
        var listItems = [];
        for (var k = 1; k <= count && k < sectionArticles.length; k++) {
          listItems.push(sectionArticles[k]);
        }
        renderListSlot(container, listItems);
      } else {
        var gridItems = [];
        for (var m = 0; m < count && m < sectionArticles.length; m++) {
          gridItems.push(sectionArticles[m]);
        }
        renderGridSlot(container, gridItems);
      }
    }
  }

  /* ═══ Main Render ═══ */

  function render() {
    var pageType = getPageType();
    var filtered = getFilteredArticles(pageType);
    if (!articles || !articles.length) {
      console.log('feed.js: no articles - skipping render, static fallback preserved');
      return;
    }
    console.log('feed.js v2: render() start | pageType=' + pageType + ' | articles=' + articles.length + ' | filtered=' + filtered.length);

    // Homepage → render dynamic section slots (hero · list · grid)
    if (pageType === 'home') {
      renderSectionSlots();
      // Trigger language-switching script to pick up new [data-en-href] elements
      try { document.dispatchEvent(new Event('dfl:langchange')); } catch(e) {}
    }

    // General latest-articles grid (homepage + all section pages)
    var grid = document.querySelector(CONFIG.containerSelector);
    if (grid && pageType !== 'blog' && pageType !== 'archive' && filtered.length > 0) {
      var html = '';
      for (var i = 0; i < Math.min(filtered.length, CONFIG.maxItems); i++) {
        html += buildCardHTML(filtered[i]);
      }
      grid.innerHTML = html;
      console.log('feed.js v2: rendered ' + Math.min(filtered.length, CONFIG.maxItems) + ' cards to #latest-articles grid');
    } else if (pageType === 'home' && !grid) {
      console.warn('feed.js v2: #latest-articles .hl-article-grid NOT FOUND');
    }

    // Blog + Archive full list
    if (pageType === 'blog' || pageType === 'archive') {
      var list = document.querySelector('#blog-list') || document.querySelector('#archive-list');
      if (list && filtered.length > 0) {
        var html = '';
        for (var i = 0; i < Math.min(filtered.length, CONFIG.blogListMax); i++) {
          html += buildListItemHTML(filtered[i]);
        }
        list.innerHTML = html;
      }
      var count = document.querySelector('#article-count');
      if (count) count.textContent = filtered.length;
    }
  }

  /* ═══ Bootstrap ═══
     Waits for DOM then fetches and renders.
     Uses defer script attribute + DOMContentLoaded for safety. */

  function boot() {
    var hasGrid = !!document.querySelector(CONFIG.containerSelector);
    var hasBlog = !!document.querySelector('#blog-list');
    var hasArchive = !!document.querySelector('#archive-list');
    var hasSectionFeeds = !!document.querySelector('[data-feed-section]');
    console.log('feed.js: bootstrap | grid=' + hasGrid + ' blog=' + hasBlog + ' archive=' + hasArchive + ' sections=' + hasSectionFeeds);

    if (hasGrid || hasBlog || hasArchive || hasSectionFeeds) {
      console.log('feed.js: bootstrap OK → fetching');
      fetchArticles(render);
    } else {
      console.warn('feed.js: no containers — retrying in 1s');
      setTimeout(function() {
        var retryGrid = !!document.querySelector(CONFIG.containerSelector);
        var retrySec = !!document.querySelector('[data-feed-section]');
        if (retryGrid || retrySec) {
          console.log('feed.js: containers found on retry → fetching');
          fetchArticles(render);
        } else {
          console.warn('feed.js: still no containers after retry');
        }
      }, 1000);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

})();
