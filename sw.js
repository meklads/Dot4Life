/* DotForLife service worker — Family Kit companion cache.
 * Conservative:
 *  - Library kit + the seven habit tools, and static versioned assets.
 *  - Everything else passes through (no caching).
 *  - HTML: network-first with cache fallback.
 *  - Assets (?v= versioned): cache-first.
 */
const CACHE = 'dfl-kit-v6';
const TOOL_PAGES = [
  '/library.html',
  '/tools/return-to-hotel.html',
  '/tools/zakat-calculator.html',
  '/tools/mortgage-calculator.html',
  '/tools/salary-calculator.html',
  '/tools/monthly-budget.html',
  '/tools/water-calculator.html',
  '/tools/inheritance-calculator.html',
];
const TOOL_ALIASES = {
  '/library': '/library.html',
  '/tools/return-to-hotel': '/tools/return-to-hotel.html',
  '/tools/zakat-calculator': '/tools/zakat-calculator.html',
  '/tools/mortgage-calculator': '/tools/mortgage-calculator.html',
  '/tools/salary-calculator': '/tools/salary-calculator.html',
  '/tools/monthly-budget': '/tools/monthly-budget.html',
  '/tools/water-calculator': '/tools/water-calculator.html',
  '/tools/inheritance-calculator': '/tools/inheritance-calculator.html',
};
const PRECACHE = [
  '/library.html',
  '/tools/family-kit.webmanifest',
  '/tools/return-to-hotel.html',
  '/tools/return-to-hotel.webmanifest',
  '/tools/zakat-calculator.html',
  '/tools/zakat-calculator.webmanifest',
  '/tools/mortgage-calculator.html',
  '/tools/salary-calculator.html',
  '/tools/monthly-budget.html',
  '/tools/water-calculator.html',
  '/tools/inheritance-calculator.html',
  '/styles/global.css?v=20260624n',
  '/styles/tools-shared.css?v=20260608a',
  '/styles/tools-flagship.css?v=20260626a',
  '/styles/tools-flagship.css?v=20260709f',
  '/styles/tools-accents.css?v=20260625a',
  '/styles/pages/library.css?v=20260903a',
  '/assets/images/kit/cat-health.svg',
  '/assets/images/kit/cat-finance.svg',
  '/assets/images/kit/cat-islamic.svg',
  '/assets/images/kit/cat-travel.svg',
  '/styles/pages/family-kit-visual.css?v=20260902e',
  '/assets/images/kit/inherit-poster.svg',
  '/styles/pages/tools_return-to-hotel.css?v=20260902c',
  '/styles/pages/tools_zakat-calculator.css?v=20260823a',
  '/assets/images/kit/house.svg',
  '/assets/images/kit/house-hero.svg',
  '/assets/images/kit/hotel.svg',
  '/assets/images/kit/zakat.svg',
  '/assets/images/kit/home.svg',
  '/assets/images/kit/salary.svg',
  '/assets/images/kit/month.svg',
  '/assets/images/kit/water.svg',
  '/assets/images/kit/inherit.svg',
  '/assets/icons/family-kit-192.png',
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
    }).catch(() => caches.match('/library.html')))
  );
});
