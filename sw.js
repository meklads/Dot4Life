/* DotForLife service worker — companion cache for habit tools.
 * Conservative:
 *  - Only the hotel + zakat tool pages and static versioned assets.
 *  - Everything else passes through (no caching).
 *  - HTML: network-first with cache fallback.
 *  - Assets (?v= versioned): cache-first.
 */
const CACHE = 'dfl-tools-v3';
const TOOL_PAGES = [
  '/tools/return-to-hotel.html',
  '/tools/zakat-calculator.html',
];
const TOOL_ALIASES = {
  '/tools/return-to-hotel': '/tools/return-to-hotel.html',
  '/tools/zakat-calculator': '/tools/zakat-calculator.html',
};
const PRECACHE = [
  '/tools/return-to-hotel.html',
  '/tools/return-to-hotel.webmanifest',
  '/tools/zakat-calculator.html',
  '/tools/zakat-calculator.webmanifest',
  '/styles/global.css?v=20260624n',
  '/styles/tools-shared.css?v=20260608a',
  '/styles/tools-flagship.css?v=20260626a',
  '/styles/tools-flagship.css?v=20260709f',
  '/styles/tools-accents.css?v=20260625a',
  '/styles/pages/tools_return-to-hotel.css?v=20260822a',
  '/styles/pages/tools_zakat-calculator.css?v=20260823a',
  '/assets/icons/hotel-card-192.png',
  '/assets/icons/zakat-192.png',
  '/favicon.svg',
];

function canonicalTool(pathname) {
  if (TOOL_PAGES.indexOf(pathname) > -1) return pathname;
  return TOOL_ALIASES[pathname] || null;
}

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

  const toolPage = canonicalTool(url.pathname);
  const isAsset = url.pathname.startsWith('/styles/') ||
                  url.pathname.startsWith('/scripts/') ||
                  url.pathname.startsWith('/assets/') ||
                  url.pathname === '/favicon.svg' ||
                  url.pathname.endsWith('.webmanifest');

  if (!toolPage && !isAsset) return;

  if (toolPage) {
    event.respondWith(
      fetch(event.request)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(toolPage, copy));
          return res;
        })
        .catch(() => caches.match(toolPage))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((hit) => hit || fetch(event.request).then((res) => {
      const copy = res.clone();
      caches.open(CACHE).then((c) => c.put(event.request, copy));
      return res;
    }).catch(() => caches.match('/tools/zakat-calculator.html')))
  );
});
