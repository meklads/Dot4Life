const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const BASE = 'https://dotforlife.com';

  /* ═══ TEST 1: Normal path — articles.json loads ═══ */
  console.log('\n═══════════════════════════════════════');
  console.log('TEST 1: Normal path — articles.json loads');
  console.log('═══════════════════════════════════════\n');

  const ctx1 = await browser.createBrowserContext();
  const page1 = await ctx1.newPage();
  page1.on('console', msg => {
    if (msg.type() === 'log' || msg.type() === 'warn') {
      console.log(`  [JS] ${msg.text()}`);
    }
  });
  page1.on('response', resp => {
    const url = resp.url();
    if (url.includes('articles.json')) {
      console.log(`  [NET] articles.json → HTTP ${resp.status()} (${(resp.headers()['content-length'] || '?')} bytes)`);
    }
  });

  await page1.goto(BASE, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));

  // Hero card
  const heroResult = await page1.evaluate(() => {
    const heroLink = document.querySelector('.sl-featured');
    const titleEn = document.querySelector('.sl-featured-title .en');
    const kickerEn = document.querySelector('.sl-featured-kicker .en');
    const img = document.querySelector('.sl-featured-img img');
    return {
      title: titleEn ? titleEn.textContent.trim() : 'NOT FOUND',
      kicker: kickerEn ? kickerEn.textContent.trim() : 'NOT FOUND',
      imgSrc: img ? (img.src || '').substring(0, 60) : 'NOT FOUND',
      href: heroLink ? heroLink.getAttribute('href') : 'NOT FOUND'
    };
  });
  console.log('\n  📌 Hero card (featured-stories):');
  console.log(`     Title: "${heroResult.title}"`);
  console.log(`     Kicker: "${heroResult.kicker}"`);
  console.log(`     Img: ${heroResult.imgSrc}`);
  console.log(`     Link: ${heroResult.href}`);

  // List items
  const listResult = await page1.evaluate(() => {
    const items = document.querySelectorAll('[data-feed-section="featured-stories"][data-role="list"] .sl-latest-item');
    return Array.from(items).map(el => {
      const t = el.querySelector('.sl-latest-item-title .en');
      return t ? t.textContent.trim() : '(no .en)';
    });
  });
  console.log(`\n  📋 List items: ${listResult.length}`);
  listResult.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Comparisons (use the exact data-feed-section container)
  const compResult = await page1.evaluate(() => {
    const container = document.querySelector('[data-feed-section="comparisons"]');
    if (!container) return ['NO CONTAINER'];
    const items = container.querySelectorAll('.dc-item');
    return Array.from(items).map(el => {
      const t = el.querySelector('.dc-item-title .en');
      return t ? t.textContent.trim() : '(no .en)';
    });
  });
  console.log(`\n  📊 Comparisons: ${compResult.length}`);
  compResult.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Peace capsules
  const peaceResult = await page1.evaluate(() => {
    const container = document.querySelector('[data-feed-section="peace-capsules"]');
    if (!container) return ['NO CONTAINER'];
    const items = container.querySelectorAll('.dc-item');
    return Array.from(items).map(el => {
      const t = el.querySelector('.dc-item-title .en');
      return t ? t.textContent.trim() : '(no .en)';
    });
  });
  console.log(`\n  🕊️ Peace capsules: ${peaceResult.length}`);
  peaceResult.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Bottom grid — fix class name (hl-art-card, not hl-article-card)
  const gridResult = await page1.evaluate(() => {
    const cards = document.querySelectorAll('#latest-articles .hl-art-card');
    return Array.from(cards).map(el => {
      const t = el.querySelector('.hl-art-card-title');
      return t ? t.textContent.trim() : '(no title)';
    });
  });
  console.log(`\n  🗂️ Bottom grid: ${gridResult.length} cards`);
  gridResult.forEach((t, i) => console.log(`     ${i+1}. "${t.substring(0, 60)}"`));

  // Empty sections check
  const emptySections = await page1.evaluate(() => {
    const issues = [];
    document.querySelectorAll('[data-feed-section]').forEach(s => {
      const section = s.getAttribute('data-feed-section');
      const role = s.getAttribute('data-role') || 'grid';
      const hasImg = !!s.querySelector('img[src]');
      const hasTitle = !!s.querySelector('.en, .dc-item-title, .sl-featured-title');
      let contentLen = s.textContent.trim().length;
      if (contentLen < 15 && !hasImg) {
        issues.push(`${section} (${role}) EMPTY`);
      }
    });
    return issues;
  });
  console.log(`\n  ${emptySections.length ? '❌ EMPTY: ' + emptySections.join(', ') : '✅ All sections have content'}`);

  await ctx1.close();
  console.log('\n  ✅ TEST 1 DONE — Normal path verified');

  /* ═══ TEST 2: Failure — fresh incognito, articles.json intercepted → 404 ═══ */
  console.log('\n═══════════════════════════════════════');
  console.log('TEST 2: Failure — articles.json blocked (404)');
  console.log('═══════════════════════════════════════\n');

  const ctx2 = await browser.createBrowserContext();
  const page2 = await ctx2.newPage();
  page2.on('console', msg => {
    if (msg.type() === 'log' || msg.type() === 'warn') {
      console.log(`  [JS] ${msg.text()}`);
    }
  });

  let intercepted = false;
  await page2.setRequestInterception(true);
  page2.on('request', request => {
    const url = request.url();
    if (url.includes('articles.json')) {
      intercepted = true;
      console.log(`  [NET] ⛔ Intercepted ${url} → returning 404`);
      request.respond({
        status: 404,
        contentType: 'application/json',
        body: '{"error":"not found"}'
      });
    } else {
      request.continue();
    }
  });

  await page2.goto(BASE, { waitUntil: 'networkidle0', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000));

  console.log(`  [INFO] articles.json intercepted: ${intercepted}`);

  // Check static fallback hero
  const fHero = await page2.evaluate(() => {
    const el = document.querySelector('.sl-featured-title .en');
    return el ? el.textContent.trim() : 'NOT FOUND';
  });
  console.log(`\n  📌 Hero title (STATIC FALLBACK): "${fHero}"`);

  // Check that hero content IS the static placeholder (not dynamic)
  const fListItems = await page2.evaluate(() => {
    const items = document.querySelectorAll('[data-feed-section="featured-stories"][data-role="list"] .sl-latest-item');
    return Array.from(items).map(el => {
      const t = el.querySelector('.sl-latest-item-title .en');
      return t ? t.textContent.trim() : '(no .en)';
    });
  });
  console.log(`\n  📋 List items (STATIC FALLBACK): ${fListItems.length}`);
  fListItems.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Comparisons fallback
  const fComp = await page2.evaluate(() => {
    const container = document.querySelector('[data-feed-section="comparisons"]');
    if (!container) return ['NO CONTAINER'];
    return Array.from(container.querySelectorAll('.dc-item')).map(el => {
      const t = el.querySelector('.dc-item-title .en');
      return t ? t.textContent.trim() : '(no .en)';
    });
  });
  console.log(`\n  📊 Comparisons (STATIC FALLBACK): ${fComp.length}`);
  fComp.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Peace capsules fallback
  const fPeace = await page2.evaluate(() => {
    const container = document.querySelector('[data-feed-section="peace-capsules"]');
    if (!container) return ['NO CONTAINER'];
    return Array.from(container.querySelectorAll('.dc-item')).map(el => {
      const t = el.querySelector('.dc-item-title .en');
      return t ? t.textContent.trim() : '(no .en)';
    });
  });
  console.log(`\n  🕊️ Peace capsules (STATIC FALLBACK): ${fPeace.length}`);
  fPeace.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Bottom grid fallback
  const fBottom = await page2.evaluate(() => {
    const cards = document.querySelectorAll('#latest-articles .hl-art-card');
    return Array.from(cards).map(el => {
      const t = el.querySelector('.hl-art-card-title');
      return t ? t.textContent.trim() : '(no title)';
    });
  });
  console.log(`\n  🗂️ Bottom grid (STATIC FALLBACK): ${fBottom.length} cards`);
  fBottom.forEach((t, i) => console.log(`     ${i+1}. "${t.substring(0, 60)}"`));

  // CRITICAL: Check for empty sections
  const fEmpty = await page2.evaluate(() => {
    const issues = [];
    document.querySelectorAll('[data-feed-section]').forEach(s => {
      const section = s.getAttribute('data-feed-section');
      const role = s.getAttribute('data-role') || 'grid';
      // Check for meaningful content
      const titles = s.querySelectorAll('.en');
      let hasContent = false;
      titles.forEach(t => { if (t.textContent.trim().length > 3) hasContent = true; });
      if (!hasContent) {
        issues.push(`${section} (${role}) EMPTY`);
      }
    });
    const bottomGrid = document.querySelector('#latest-articles .hl-art-grid, #latest-articles .hl-article-grid');
    if (bottomGrid) {
      const cards = bottomGrid.querySelectorAll('.hl-art-card');
      if (cards.length === 0) issues.push('latest-articles grid has ZERO cards');
    }
    return issues;
  });
  console.log(`\n  ${fEmpty.length ? '❌ CRITICAL FAILURE - EMPTY SECTIONS: ' + fEmpty.join(', ') : '✅✅✅ ALL STATIC FALLBACK INTACT — no empty sections, no data loss!'}`);

  // Screenshot of failure page
  await page2.screenshot({ path: '/tmp/feed-failure-test-2.png', fullPage: true });
  console.log('\n  📸 Screenshot: /tmp/feed-failure-test-2.png');

  await ctx2.close();
  await browser.close();

  console.log('\n═══════════════════════════════════════');
  console.log('🏁 BOTH TESTS COMPLETE');
  console.log('═══════════════════════════════════════\n');
})();
