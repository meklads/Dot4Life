/* ═════════════════════════════════════════════════════
   feed.js — Universal Article Feed
   Reads /articles.json and renders:
   · Homepage: 3 section feeds (قصص/مقارنات/السلام) + general latest
   · Section pages: category-filtered cards
   · Blog + Archive: full chronological list
   Auto-updates: any new line in articles.json shows instantly
   ═════════════════════════════════════════════════════ */

(function() {
  'use strict';

  var CONFIG = {
    jsonUrl: '/articles.json',
    containerSelector: '#latest-articles .hl-article-grid',
    maxItems: 6,
    blogListMax: 50,
    sectionFeedMax: 3,
    cacheKey: 'dfl-feed-cache',
    cacheTTL: 600000
  };

  var articles = [];
  var isAr = document.documentElement.getAttribute('data-lang') === 'ar';
  var currentPage = window.location.pathname;

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

    var xhr = new XMLHttpRequest();
    xhr.open('GET', CONFIG.jsonUrl, true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        try {
          articles = JSON.parse(xhr.responseText);
          try {
            localStorage.setItem(CONFIG.cacheKey, JSON.stringify({
              articles: articles,
              timestamp: Date.now()
            }));
          } catch(e) {}
          callback();
        } catch(e) {
          console.warn('feed.js: parse error');
          callback();
        }
      } else {
        console.warn('feed.js: fetch error', xhr.status);
        callback();
      }
    };
    xhr.onerror = function() {
      console.warn('feed.js: network error');
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
    if (!containers.length) return;

    for (var j = 0; j < containers.length; j++) {
      var section = containers[j].getAttribute('data-feed-section');
      if (!section) continue;
      var sectionArticles = getSectionArticles(section);
      var grid = containers[j].querySelector('.hl-feed-grid');
      if (!grid) continue;
      var html = '';
      var limit = Math.min(sectionArticles.length, CONFIG.sectionFeedMax);
      for (var i = 0; i < limit; i++) {
        html += buildCardHTML(sectionArticles[i]);
      }
      grid.innerHTML = html;
    }
  }

  /* ═══ Main Render ═══ */

  function render() {
    var pageType = getPageType();
    var filtered = getFilteredArticles(pageType);

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

  /* ═══ Bootstrap ═══ */

  if (document.querySelector(CONFIG.containerSelector) ||
      document.querySelector('#blog-list') ||
      document.querySelector('#archive-list') ||
      document.querySelector('[data-feed-section]')) {
    fetchArticles(render);
  }

})();
