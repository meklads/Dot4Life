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

  var FEED_VERSION = 9;  // v9: blog cards + featured with article images

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
    if (page.endsWith('blog.html') || page.endsWith('/blog')) return 'blog';
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
    var url = isAr ? (a.url || '#') : (a.url_en || a.url || '#');
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

  /** Text-only editorial card for archive grid (no images) */
  function buildArchiveCardHTML(a) {
    var title = isAr && a.title_ar ? a.title_ar : a.title_en;
    var excerpt = isAr && a.excerpt_ar ? a.excerpt_ar : a.excerpt_en;
    var url = isAr ? (a.url || '#') : (a.url_en || a.url || '#');
    var section = isAr && a.section_ar ? a.section_ar : (a.section || a.category || '');
    var cat = a.category || 'general';
    var readLabel = isAr ? '← اقرأ' : 'Read →';

    return '<a href="' + url + '" class="arc-card" data-cat="' + esc(cat) + '">' +
      '<span class="arc-card-kicker">' + esc(section) + '</span>' +
      '<span class="arc-card-title">' + esc(title) + '</span>' +
      (excerpt ? '<span class="arc-card-desc">' + esc(excerpt) + '</span>' : '') +
      '<span class="arc-card-foot">' +
      '<span class="arc-card-date">' + fmtDate(a.date) + '</span>' +
      '<span class="arc-card-link">' + readLabel + '</span>' +
      '</span></a>';
  }

  function setArticleCounts(n) {
    document.querySelectorAll('[data-article-count]').forEach(function(el) {
      el.textContent = n;
    });
    var legacy = document.getElementById('article-count');
    if (legacy) legacy.textContent = n;
  }

  /** Article image for blog cards — per-article img or category fallback */
  var BLOG_CAT_IMG = {
    health: '/assets/images/fit-heart.svg',
    finance: '/assets/images/hero-money-lessons.svg',
    travel: '/assets/images/hero-travel-comparison.jpg',
    'real-estate': '/assets/images/hero-gold-vs-real-estate.svg',
    islamic: '/assets/images/hero-prayer.svg',
    family: '/assets/images/hero-carpentry-workshop.jpg',
    productivity: '/assets/images/hero-morning-routine.svg'
  };

  function getBlogArticleImg(a) {
    if (a && a.img) return a.img;
    var cat = (a && a.category) || 'general';
    return BLOG_CAT_IMG[cat] || '/assets/images/hero-travel-comparison.jpg';
  }

  /** Editorial card with image for blog grid */
  function buildBlogCardHTML(a) {
    var title = isAr && a.title_ar ? a.title_ar : a.title_en;
    var excerpt = isAr && a.excerpt_ar ? a.excerpt_ar : a.excerpt_en;
    var url = isAr ? (a.url || '#') : (a.url_en || a.url || '#');
    var section = isAr && a.section_ar ? a.section_ar : (a.section || a.category || '');
    var cat = a.category || 'general';
    var readLabel = isAr ? '← اقرأ' : 'Read →';
    var img = getBlogArticleImg(a);

    return '<a href="' + url + '" class="bl-card" data-cat="' + esc(cat) + '">' +
      '<span class="bl-card-media">' +
      '<img class="bl-card-img" src="' + img + '" alt="' + esc(title) + '" width="600" height="340" loading="lazy" decoding="async">' +
      '</span>' +
      '<span class="bl-card-body">' +
      '<span class="bl-card-kicker">' + esc(section) + '</span>' +
      '<span class="bl-card-title">' + esc(title) + '</span>' +
      (excerpt ? '<span class="bl-card-desc">' + esc(excerpt) + '</span>' : '') +
      '<span class="bl-card-foot">' +
      '<span class="bl-card-date">' + fmtDate(a.date) + '</span>' +
      '<span class="bl-card-link">' + readLabel + '</span>' +
      '</span></span></a>';
  }

  var blogArticles = [];
  var blogVisibleCount = 12;
  var blogFiltered = [];

  function updateBlogFeatured(a) {
    var el = document.getElementById('blog-featured');
    if (!el || !a) return;
    var title = isAr && a.title_ar ? a.title_ar : a.title_en;
    var excerpt = isAr && a.excerpt_ar ? a.excerpt_ar : a.excerpt_en;
    var url = isAr ? (a.url || '#') : (a.url_en || a.url || '#');
    var section = isAr && a.section_ar ? a.section_ar : (a.section || a.category || '');
    var cat = a.category || '';
    var readLabel = isAr ? '← اقرأ المقال' : 'Read article →';
    var kickerEn = 'Featured · Deep dive';
    var kickerAr = 'مميز · دراسة معمّقة';

    el.href = url;
    var kicker = el.querySelector('.bl-featured-kicker');
    if (kicker) {
      var ke = kicker.querySelector('.en');
      var ka = kicker.querySelector('.ar');
      if (ke) ke.textContent = kickerEn;
      if (ka) ka.textContent = kickerAr;
    }
    var catEl = el.querySelector('.bl-featured-cat');
    if (catEl) {
      var ce = catEl.querySelector('.en');
      var ca = catEl.querySelector('.ar');
      var catLabels = {
        health: ['Health', 'الصحة'],
        finance: ['Finance', 'المالية'],
        travel: ['Travel', 'السفر'],
        'real-estate': ['Real Estate', 'العقار'],
        islamic: ['Islamic', 'الإسلامية'],
        family: ['Family', 'الأسرة'],
        productivity: ['Productivity', 'الإنتاجية']
      };
      var labels = catLabels[cat] || [section, section];
      if (ce) ce.textContent = labels[0];
      if (ca) ca.textContent = labels[1];
    }
    var titleEl = el.querySelector('.bl-featured-title');
    if (titleEl) {
      var te = titleEl.querySelector('.en');
      var ta = titleEl.querySelector('.ar');
      if (te) te.textContent = a.title_en || title;
      if (ta) ta.textContent = a.title_ar || a.title_en || title;
    }
    var exEl = el.querySelector('.bl-featured-excerpt');
    if (exEl) {
      var ee = exEl.querySelector('.en');
      var ea = exEl.querySelector('.ar');
      if (ee) ee.textContent = a.excerpt_en || '';
      if (ea) ea.textContent = a.excerpt_ar || a.excerpt_en || '';
    }
    var dateEl = el.querySelector('.bl-featured-date');
    if (dateEl) dateEl.textContent = fmtDate(a.date);
    var readEl = el.querySelector('.bl-featured-read');
    if (readEl) {
      var re = readEl.querySelector('.en');
      var ra = readEl.querySelector('.ar');
      if (re) re.textContent = 'Read article →';
      if (ra) ra.textContent = '← اقرأ المقال';
    }
    var imgEl = el.querySelector('.bl-featured-img');
    if (imgEl) {
      imgEl.src = getBlogArticleImg(a);
      imgEl.alt = title;
    }
  }

  function renderBlogGrid(items, append) {
    var grid = document.querySelector('#blog-grid');
    var loading = document.querySelector('#blog-loading');
    var loadBtn = document.getElementById('blog-load-more');
    if (!grid) return;

    if (loading) loading.remove();

    if (!items.length) {
      grid.innerHTML = '<p class="bl-empty"><span class="en">No articles match your search.</span><span class="ar">لا توجد مقالات مطابقة.</span></p>';
      if (loadBtn) loadBtn.hidden = true;
      return;
    }

    var slice = items.slice(0, blogVisibleCount);
    var html = '';
    for (var i = 0; i < slice.length; i++) {
      html += buildBlogCardHTML(slice[i]);
    }
    grid.innerHTML = html;
    setArticleCounts(blogArticles.length);

    var statEl = document.querySelector('[data-blog-stat-count]');
    if (statEl) statEl.textContent = blogArticles.length;

    if (loadBtn) {
      loadBtn.hidden = slice.length >= items.length;
    }
  }

  function initBlogPage(allArticles) {
    blogArticles = allArticles.slice();
    blogVisibleCount = 12;
    var activeCat = 'all';
    var query = '';

    if (blogArticles.length > 0) {
      updateBlogFeatured(blogArticles[0]);
    }

    function getFiltered() {
      var q = query.trim().toLowerCase();
      return blogArticles.filter(function(a, idx) {
        if (idx === 0 && activeCat === 'all' && !q) return false;
        if (activeCat !== 'all' && (a.category || '') !== activeCat) return false;
        if (!q) return true;
        var hay = [
          a.title_en, a.title_ar, a.excerpt_en, a.excerpt_ar,
          a.section, a.section_ar, a.category
        ].join(' ').toLowerCase();
        return hay.indexOf(q) !== -1;
      });
    }

    function applyFilters(resetVisible) {
      if (resetVisible) blogVisibleCount = 12;
      blogFiltered = getFiltered();
      if (activeCat !== 'all' || query.trim()) {
        if (blogFiltered.length > 0) updateBlogFeatured(blogFiltered[0]);
      } else if (blogArticles.length > 0) {
        updateBlogFeatured(blogArticles[0]);
      }
      renderBlogGrid(blogFiltered, false);
    }

    var search = document.getElementById('bl-search');
    if (search) {
      search.addEventListener('input', function() {
        query = search.value;
        applyFilters(true);
      });
    }

    document.querySelectorAll('.bl-filter').forEach(function(btn) {
      btn.addEventListener('click', function() {
        document.querySelectorAll('.bl-filter').forEach(function(b) {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        activeCat = btn.getAttribute('data-cat') || 'all';
        applyFilters(true);
      });
    });

    var loadBtn = document.getElementById('blog-load-more');
    if (loadBtn) {
      loadBtn.addEventListener('click', function() {
        blogVisibleCount += 12;
        renderBlogGrid(blogFiltered, false);
      });
    }

    applyFilters(true);
  }

  var archiveArticles = [];

  function renderArchiveGrid(items) {
    var grid = document.querySelector('#archive-grid');
    var empty = document.querySelector('#archive-empty');
    var loading = document.querySelector('#archive-loading');
    if (!grid) return;

    if (loading) loading.hidden = true;

    if (!items.length) {
      grid.innerHTML = '';
      if (empty) empty.hidden = false;
      setArticleCounts(0);
      updateArchiveResultMeta(0, archiveArticles.length);
      return;
    }

    if (empty) empty.hidden = true;
    var html = '';
    for (var i = 0; i < items.length; i++) {
      html += buildArchiveCardHTML(items[i]);
    }
    grid.innerHTML = html;
    setArticleCounts(archiveArticles.length);
    updateArchiveResultMeta(items.length, archiveArticles.length);
  }

  function updateArchiveResultMeta(shown, total) {
    var el = document.querySelector('#arc-result-meta');
    if (!el) return;
    var en = el.querySelector('.en');
    var ar = el.querySelector('.ar');
    if (en) en.innerHTML = 'Showing <strong>' + shown + '</strong> of <strong>' + total + '</strong> articles';
    if (ar) ar.innerHTML = 'عرض <strong>' + shown + '</strong> من <strong>' + total + '</strong> مقال';
  }

  function initArchivePage(allArticles) {
    archiveArticles = allArticles.slice();
    var activeCat = 'all';
    var query = '';

    function applyFilters() {
      var q = query.trim().toLowerCase();
      var filtered = archiveArticles.filter(function(a) {
        if (activeCat !== 'all' && (a.category || '') !== activeCat) return false;
        if (!q) return true;
        var hay = [
          a.title_en, a.title_ar, a.excerpt_en, a.excerpt_ar,
          a.section, a.section_ar, a.category
        ].join(' ').toLowerCase();
        return hay.indexOf(q) !== -1;
      });
      renderArchiveGrid(filtered);
    }

    var search = document.getElementById('arc-search');
    if (search) {
      search.addEventListener('input', function() {
        query = search.value;
        applyFilters();
      });
    }

    document.querySelectorAll('.arc-filter').forEach(function(btn) {
      btn.addEventListener('click', function() {
        document.querySelectorAll('.arc-filter').forEach(function(b) {
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        activeCat = btn.getAttribute('data-cat') || 'all';
        applyFilters();
      });
    });

    applyFilters();
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

    // Blog hub — editorial grid + featured + load more
    if (pageType === 'blog') {
      if (document.querySelector('#blog-grid') && filtered.length > 0) {
        initBlogPage(filtered);
      } else {
        var legacyList = document.querySelector('#blog-list');
        if (legacyList && filtered.length > 0) {
          var listHtml = '';
          for (var j = 0; j < Math.min(filtered.length, CONFIG.blogListMax); j++) {
            listHtml += buildListItemHTML(filtered[j]);
          }
          legacyList.innerHTML = listHtml;
        }
        setArticleCounts(filtered.length);
      }
    }

    // Archive — editorial text grid + search/filter
    if (pageType === 'archive') {
      if (filtered.length > 0) {
        initArchivePage(filtered);
      } else {
        renderArchiveGrid([]);
      }
    }
  }

  /* ═══ Bootstrap ═══
     Waits for DOM then fetches and renders.
     Uses defer script attribute + DOMContentLoaded for safety. */

  function boot() {
    var hasGrid = !!document.querySelector(CONFIG.containerSelector);
    var hasBlog = !!document.querySelector('#blog-grid') || !!document.querySelector('#blog-list');
    var hasArchive = !!document.querySelector('#archive-grid') || !!document.querySelector('#archive-list');
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
        var retryBlog = !!document.querySelector('#blog-grid') || !!document.querySelector('#blog-list');
        var retryArchive = !!document.querySelector('#archive-grid') || !!document.querySelector('#archive-list');
        if (retryGrid || retrySec || retryBlog || retryArchive) {
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
