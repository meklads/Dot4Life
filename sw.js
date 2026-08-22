/* DotForLife service worker — scoped companion for the Return-to-Hotel
 * pilgrim tool. Deliberately minimal and conservative:
 *  - Only the tool page itself and static, versioned assets are handled.
 *  - Everything else passes straight through to the browser (no caching).
 *  - HTML: network-first with cache fallback (so updates flow, offline works).
 *  - Assets (?v= versioned): cache-first (they are immutable by design).
 */
const CACHE = 'dfl-rth-v1';
const TOOL_PAGE = '/tools/return-to-hotel.html';
const PRECACHE = [
  TOOL_PAGE,
  '/styles/global.css?v=20260624n',
  '/styles/tools-shared.css?v=20260608a',
  '/styles/tools-flagship.css?v=20260626a',
  '/styles/tools-accents.css?v=20260625a',
  '/styles/pages/tools_return-to-hotel.css?v=20260626a',
  '/favicon.svg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) return;

  const isToolPage = url.pathname === TOOL_PAGE || url.pathname === '/tools/return-to-hotel';
  const isAsset = url.pathname.startsWith('/styles/') ||
                  url.pathname.startsWith('/scripts/') ||
                  url.pathname.startsWith('/assets/') ||
                  url.pathname === '/favicon.svg';

  if (!isToolPage && !isAsset) return; // pass through — never touch other pages

  if (isToolPage) {
    // network-first, cache fallback → page updates normally, works offline
    event.respondWith(
      fetch(event.request)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(TOOL_PAGE, copy));
          return res;
        })
        .catch(() => caches.match(TOOL_PAGE))
    );
    return;
  }

  // assets: cache-first (versioned URLs are immutable)
  event.respondWith(
    caches.match(event.request).then((hit) => hit || fetch(event.request).then((res) => {
      const copy = res.clone();
      caches.open(CACHE).then((c) => c.put(event.request, copy));
      return res;
    }).catch(() => caches.match(TOOL_PAGE)))
  );
});
