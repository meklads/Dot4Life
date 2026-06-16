const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const BASE = 'https://dotforlife.com';

  /* ═══ TEST 1: Normal path — JS enabled, articles.json loads ═══ */
  console.log('\n═══════════════════════════════════════');
  console.log('TEST 1: Normal path — articles.json loads');
  console.log('═══════════════════════════════════════\n');

  const page1 = await browser.newPage();
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

  // Check hero card
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

  // Check list items
  const listResult = await page1.evaluate(() => {
    const items = document.querySelectorAll('[data-feed-section="featured-stories"][data-role="list"] .sl-latest-item');
    const titles = [];
    items.forEach(el => {
      const t = el.querySelector('.sl-latest-item-title .en');
      if (t) titles.push(t.textContent.trim());
    });
    return titles;
  });
  console.log(`\n  📋 List items (featured-stories list): ${listResult.length} items`);
  listResult.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Check comparisons grid
  const compResult = await page1.evaluate(() => {
    const items = document.querySelectorAll('[data-feed-section="comparisons"] .dc-item');
    const titles = [];
    items.forEach(el => {
      const t = el.querySelector('.dc-item-title .en');
      if (t) titles.push(t.textContent.trim());
    });
    return titles;
  });
  console.log(`\n  📊 Comparisons grid: ${compResult.length} items`);
  compResult.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Check peace capsules grid
  const peaceResult = await page1.evaluate(() => {
    const items = document.querySelectorAll('[data-feed-section="peace-capsules"] .dc-item');
    const titles = [];
    items.forEach(el => {
      const t = el.querySelector('.dc-item-title .en');
      if (t) titles.push(t.textContent.trim());
    });
    return titles;
  });
  console.log(`\n  🕊️ Peace capsules grid: ${peaceResult.length} items`);
  peaceResult.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  // Check bottom grid
  const gridResult = await page1.evaluate(() => {
    const cards = document.querySelectorAll('#latest-articles .hl-article-card');
    const titles = [];
    cards.forEach(el => {
      const t = el.querySelector('.hl-art-card-title');
      if (t) titles.push(t.textContent.trim());
    });
    return titles;
  });
  console.log(`\n  🗂️ Bottom grid (#latest-articles): ${gridResult.length} cards`);
  gridResult.forEach((t, i) => console.log(`     ${i+1}. "${t.substring(0, 60)}"`));

  // Check no empty sections
  const emptySections = await page1.evaluate(() => {
    const issues = [];
    const allSecs = document.querySelectorAll('[data-feed-section]');
    allSecs.forEach(s => {
      const text = s.textContent.trim().replace(/\s+/g, ' ');
      if (text.length < 10) issues.push(s.getAttribute('data-feed-section') + ' appears EMPTY');
    });
    return issues;
  });
  console.log(`\n  ${emptySections.length ? '❌ EMPTY SECTIONS: ' + emptySections.join(', ') : '✅ No empty sections'}`);

  await page1.close();
  console.log('\n  ✅ TEST 1 COMPLETE: Normal path');

  /* ═══ TEST 2: Failure simulation — intercept articles.json → 404 ═══ */
  console.log('\n═══════════════════════════════════════');
  console.log('TEST 2: Failure — articles.json blocked (404)');
  console.log('═══════════════════════════════════════\n');

  const page2 = await browser.newPage();
  page2.on('console', msg => {
    if (msg.type() === 'log' || msg.type() === 'warn') {
      console.log(`  [JS] ${msg.text()}`);
    }
  });

  // Block articles.json by intercepting and returning 404
  await page2.setRequestInterception(true);
  page2.on('request', request => {
    const url = request.url();
    if (url.includes('articles.json')) {
      console.log(`  [NET] Intercepted ${url} → returning 404`);
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

  // Now verify STATIC FALLBACK is intact
  const fallbackHero = await page2.evaluate(() => {
    const titleEl = document.querySelector('.sl-featured-title .en');
    return titleEl ? titleEl.textContent.trim() : 'NOT FOUND';
  });
  console.log(`\n  📌 Hero title (should be static fallback):`);
  console.log(`     "${fallbackHero}"`);

  const fallbackList = await page2.evaluate(() => {
    const items = document.querySelectorAll('[data-feed-section="featured-stories"][data-role="list"] .sl-latest-item');
    const titles = [];
    items.forEach(el => {
      const t = el.querySelector('.sl-latest-item-title .en');
      if (t) titles.push(t.textContent.trim());
    });
    return titles;
  });
  console.log(`\n  📋 List items (static fallback): ${fallbackList.length} items`);
  fallbackList.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  const fallbackComp = await page2.evaluate(() => {
    const items = document.querySelectorAll('[data-feed-section="comparisons"] .dc-item');
    const titles = [];
    items.forEach(el => {
      const t = el.querySelector('.dc-item-title .en');
      if (t) titles.push(t.textContent.trim());
    });
    return titles;
  });
  console.log(`\n  📊 Comparisons (static fallback): ${fallbackComp.length} items`);
  fallbackComp.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  const fallbackPeace = await page2.evaluate(() => {
    const items = document.querySelectorAll('[data-feed-section="peace-capsules"] .dc-item');
    const titles = [];
    items.forEach(el => {
      const t = el.querySelector('.dc-item-title .en');
      if (t) titles.push(t.textContent.trim());
    });
    return titles;
  });
  console.log(`\n  🕊️ Peace capsules (static fallback): ${fallbackPeace.length} items`);
  fallbackPeace.forEach((t, i) => console.log(`     ${i+1}. "${t}"`));

  const fallbackBottom = await page2.evaluate(() => {
    const cards = document.querySelectorAll('#latest-articles .hl-article-card');
    const titles = [];
    cards.forEach(el => {
      const t = el.querySelector('.hl-art-card-title');
      if (t) titles.push(t.textContent.trim());
    });
    return titles;
  });
  console.log(`\n  🗂️ Bottom grid (static fallback): ${fallbackBottom.length} cards`);
  fallbackBottom.forEach((t, i) => console.log(`     ${i+1}. "${t.substring(0, 60)}"`));

  // Check for ANY empty sections
  const emptyAfterFail = await page2.evaluate(() => {
    const issues = [];
    const allSecs = document.querySelectorAll('[data-feed-section]');
    allSecs.forEach(s => {
      const text = s.textContent.trim().replace(/\s+/g, ' ');
      const children = s.querySelectorAll('.en, .ar');
      let hasContent = false;
      children.forEach(c => {
        if (c.textContent.trim().length > 2) hasContent = true;
      });
      if (!hasContent) issues.push(s.getAttribute('data-feed-section') + ' (' + s.getAttribute('data-role') + ')' + ' appears EMPTY');
    });
    const bottomGrid = document.querySelector('#latest-articles .hl-article-grid');
    if (bottomGrid) {
      const cards = bottomGrid.querySelectorAll('.hl-art-card');
      if (cards.length === 0) issues.push('#latest-articles .hl-article-grid has ZERO cards');
    }
    return issues;
  });
  console.log(`\n  ${emptyAfterFail.length ? '❌ EMPTY SECTIONS: ' + emptyAfterFail.join(', ') : '✅ No empty sections — static fallback fully intact!'}`);

  // Visual check — screenshot for proof
  await page2.screenshot({ path: '/tmp/feed-failure-test.png', fullPage: true });
  console.log('\n  📸 Screenshot saved to /tmp/feed-failure-test.png');

  await page2.close();
  await browser.close();

  console.log('\n═══════════════════════════════════════');
  console.log('✅ TESTS COMPLETE — both paths verified');
  console.log('═══════════════════════════════════════\n');
})();
