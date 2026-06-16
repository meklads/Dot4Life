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

  var FEED_VERSION = 2;  // bump to invalidate all caches on deploy

  var CONFIG = {
    jsonUrl: '/articles.json',
    containerSelector: '#latest-articles .hl-article-grid',
    maxItems: 6,
    blogListMax: 50,
    sectionFeedMax: 3,
    cacheKey: 'dfl-feed-cache-v' + FEED_VERSION,
    cacheTTL: 600000
  };

  var articles = [];
  var isAr = document.documentElement.getAttribute('data-lang') === 'ar';
  var currentPage = window.location.pathname;

  /* Clear any stale old-version caches */
  try { localStorage.removeItem('dfl-feed-cache'); } catch(e){}
  try { localStorage.removeItem('dfl-feed-cache-v1'); } catch(e){}

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
            console.warn('feed.js: empty articles array');
            callback();
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
          console.warn('feed.js: fetch error on', bustUrl, e);
          /* Clear stale cache on error */
          try { localStorage.removeItem(CONFIG.cacheKey); } catch(ce){}
          try { callback(); } catch(ce2){}
        }
      } else {
        console.warn('feed.js: HTTP ' + xhr.status + ' fetching', bustUrl);
        /* Clear stale cache on HTTP error */
        try { localStorage.removeItem(CONFIG.cacheKey); } catch(ce){}
        callback();
      }
    };
    xhr.onerror = function() {
      console.warn('feed.js: network error (cannot reach server)');
      /* Clear stale cache on network error */
      try { localStorage.removeItem(CONFIG.cacheKey); } catch(ce){}
      callback();
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

  /** Filter articles by `section` field for homepage section feeds */
  function getSectionArticles(sectionName) {
    return articles
      .filter(function(a) { return a.section === sectionName; })
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

  /* ═══ Homepage Section Feeds ═══
     Renders each [data-feed-section] block with its latest articles
     (featured-stories · comparisons · peace-capsules) */

  function renderSectionFeeds() {
    var containers = document.querySelectorAll('[data-feed-section]');
    if (!containers.length) {
      console.log('feed.js v2: no [data-feed-section] found');
      return;
    }

    var renderedCount = 0;
    for (var j = 0; j < containers.length; j++) {
      var section = containers[j].getAttribute('data-feed-section');
      if (!section) continue;
      var sectionArticles = getSectionArticles(section);
      var grid = containers[j].querySelector('.hl-feed-grid');
      if (!grid) {
        console.log('feed.js v2: no .hl-feed-grid inside', section);
        continue;
      }
      var html = '';
      var limit = Math.min(sectionArticles.length, CONFIG.sectionFeedMax);
      for (var i = 0; i < limit; i++) {
        html += buildCardHTML(sectionArticles[i]);
      }
      grid.innerHTML = html;
      renderedCount++;
      console.log('feed.js v2: rendered ' + limit + ' cards to [' + section + ']');
    }

    /* Verify rendering actually happened */
    if (renderedCount > 0) {
      var totalCards = document.querySelectorAll('[data-feed-section] .hl-art-card').length;
      console.log('feed.js v2: section feed verification — ' + totalCards + ' total cards in ' + renderedCount + ' sections');
      if (totalCards === 0) {
        console.warn('feed.js v2: section feeds look empty despite render attempt — triggering re-render');
        setTimeout(function(){ renderSectionFeeds(); }, 500);
      }
    }
  }

  /* ═══ Main Render ═══ */

  function render() {
    var pageType = getPageType();
    var filtered = getFilteredArticles(pageType);
    console.log('feed.js v2: render() start | pageType=' + pageType + ' | articles=' + articles.length + ' | filtered=' + filtered.length);

    // Homepage → render 3 section feeds above general latest
    if (pageType === 'home') {
      renderSectionFeeds();
    }

    // General latest-articles grid (homepage + all section pages)
    var grid = document.querySelector(CONFIG.containerSelector);
    if (grid && pageType !== 'blog' && pageType !== 'archive') {
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
      if (list) {
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
    console.log('feed.js v2: bootstrap check | grid=' + hasGrid + ' blog=' + hasBlog + ' archive=' + hasArchive + ' sections=' + hasSectionFeeds);

    if (hasGrid || hasBlog || hasArchive || hasSectionFeeds) {
      console.log('feed.js v2: bootstrap OK → fetching articles');
      fetchArticles(render);
    } else {
      console.warn('feed.js v2: no containers found on this page — retrying in 1s');
      setTimeout(function() {
        var retryGrid = !!document.querySelector(CONFIG.containerSelector);
        var retrySec = !!document.querySelector('[data-feed-section]');
        if (retryGrid || retrySec) {
          console.log('feed.js v2: containers found on retry → fetching');
          fetchArticles(render);
        } else {
          console.warn('feed.js v2: still no containers after retry');
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
