#!/usr/bin/env node
/** Smoke test library.html redesign — desktop 1440 + mobile 390 */
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const ROOT = path.resolve(__dirname, '..');
const baseUrl = process.env.LIBRARY_TEST_URL || 'http://127.0.0.1:8765/library.html';
const fileUrl = baseUrl;
const shots = path.join(ROOT, 'operating-system', 'screenshots');
fs.mkdirSync(shots, { recursive: true });

const EXPECTED = [
  '/tools/bmi-calculator.html', '/tools/calorie-calculator.html', '/tools/water-calculator.html',
  '/tools/body-fat-calculator.html', '/tools/pregnancy-calculator.html', '/tools/age-calculator.html',
  '/tools/one-rep-max.html', '/tools/ramadan-calorie-calculator.html', '/tools/mortgage-calculator.html',
  '/tools/salary-calculator.html', '/tools/savings-goal.html', '/tools/monthly-budget.html',
  '/tools/roi-calculator.html', '/tools/rental-yield-calculator.html', '/tools/prayer-times.html',
  '/tools/qibla.html', '/tools/zakat-calculator.html', '/tools/hijri-converter.html',
  '/tools/inheritance-calculator.html', '/tools/currency-converter.html', '/tools/travel-budget.html',
  '/tools/packing-checklist.html',
];

(async () => {
  const chromePaths = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
  ];
  const executablePath = chromePaths.find(p => fs.existsSync(p));
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox'],
    ...(executablePath ? { executablePath } : {}),
  });
  const page = await browser.newPage();
  const checks = [];
  const pass = (name, ok, detail = '') => {
    checks.push({ name, ok, detail });
    console.log(`${ok ? 'PASS' : 'FAIL'}: ${name}${detail ? ' — ' + detail : ''}`);
  };

  for (const [w, label] of [[1440, 'desktop-1440'], [390, 'mobile-390']]) {
    await page.setViewport({ width: w, height: 900 });
    await page.goto(fileUrl, { waitUntil: 'networkidle0' });
    await page.screenshot({ path: path.join(shots, `library-${label}.png`), fullPage: true });
  }

  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });

  const base = await page.evaluate(() => ({
    noRecipes: !document.querySelector('.lib-mode--recipes'),
    noModeWrap: !document.querySelector('.lib-mode-wrap'),
    cardCount: document.querySelectorAll('.lib-card').length,
    hrefs: [...document.querySelectorAll('.lib-card')].map(a => a.getAttribute('href')),
    cardHeight: Math.round(document.querySelector('.lib-card').getBoundingClientRect().height),
    noDesc: !document.querySelector('.lib-card-desc'),
    hasSearch: !!document.getElementById('lib-search'),
    hasMostUsed: !!document.getElementById('lib-most-used'),
    quickCount: document.querySelectorAll('.lib-quick').length,
  }));

  pass('no recipes tab', base.noRecipes);
  pass('no lib-mode-wrap', base.noModeWrap);
  pass('22 lib-cards', base.cardCount === 22, String(base.cardCount));
  pass('all 22 hrefs', new Set(base.hrefs).size === 22 && EXPECTED.every(h => base.hrefs.includes(h)));
  pass('no .lib-card-desc', base.noDesc);
  pass('card height 44-52px', base.cardHeight >= 44 && base.cardHeight <= 52, String(base.cardHeight));
  pass('search box present', base.hasSearch);
  pass('most-used 6 quick links', base.quickCount === 6, String(base.quickCount));

  await page.click('button[data-filter="health"]');
  await new Promise(r => setTimeout(r, 200));
  const health = await page.evaluate(() => ({
    visible: document.querySelectorAll('.lib-card:not(.is-hidden)').length,
    hiddenSections: document.querySelectorAll('.lib-section.is-hidden').length,
    mostHidden: document.getElementById('lib-most-used').classList.contains('is-hidden'),
  }));
  pass('health filter 8 visible', health.visible === 8, String(health.visible));
  pass('health filter hides 3 sections', health.hiddenSections === 3, String(health.hiddenSections));
  pass('most-used hidden on category filter', health.mostHidden);

  await page.click('button[data-filter="all"]');
  await page.evaluate(() => { document.getElementById('lib-search').value = ''; });
  await page.type('#lib-search', 'zakat', { delay: 15 });
  await new Promise(r => setTimeout(r, 200));
  const search = await page.evaluate(() => ({
    visible: document.querySelectorAll('.lib-card:not(.is-hidden)').length,
    mostHidden: document.getElementById('lib-most-used').classList.contains('is-hidden'),
  }));
  pass('search zakat shows 1', search.visible === 1, String(search.visible));
  pass('most-used hidden on search', search.mostHidden);

  await browser.close();
  const allOk = checks.every(c => c.ok);
  fs.writeFileSync(path.join(shots, 'library-test-report.json'), JSON.stringify({ pass: allOk, checks }, null, 2));
  process.exit(allOk ? 0 : 1);
})().catch(err => { console.error(err); process.exit(1); });
