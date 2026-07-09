#!/usr/bin/env node
/** getComputedStyle verification for tool-calc-layout sidebar fix */
const puppeteer = require('puppeteer');
const fs = require('fs');

const BASE = process.env.TOOL_TEST_BASE || 'http://127.0.0.1:8765';
const WIDTH = 1745;
const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

async function measure(page, url) {
  await page.setViewport({ width: WIDTH, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle0' });
  return page.evaluate(() => {
    const layout = document.querySelector('.tool-calc-layout');
    const ws = document.querySelector('.tool-workspace');
    const aside = document.querySelector('.tool-related-aside');
    if (!layout || !ws || !aside) return { error: 'missing elements' };
    const lc = getComputedStyle(layout);
    const wc = getComputedStyle(ws);
    const ac = getComputedStyle(aside);
    const wr = ws.getBoundingClientRect();
    const ar = aside.getBoundingClientRect();
    return {
      dir: document.documentElement.getAttribute('dir'),
      lang: document.documentElement.getAttribute('lang'),
      layoutGridCols: lc.gridTemplateColumns,
      layoutWidth: Math.round(layout.getBoundingClientRect().width),
      workspaceWidth: Math.round(wr.width),
      asideWidth: Math.round(ar.width),
      workspaceLeft: Math.round(wr.left),
      asideLeft: Math.round(ar.left),
      workspaceComputedWidth: wc.width,
      asideComputedWidth: ac.width,
    };
  });
}

function check(name, m) {
  const wsOk = m.workspaceWidth >= 1000;
  const asideOk = m.asideWidth >= 200 && m.asideWidth <= 240;
  const colsOk = m.layoutGridCols.includes('220px') && m.layoutGridCols.includes('1fr');
  const asideAfterWorkspace = m.dir === 'rtl'
    ? m.asideLeft < m.workspaceLeft
    : m.asideLeft > m.workspaceLeft;
  const pass = wsOk && asideOk && colsOk && asideAfterWorkspace;
  console.log(`\n=== ${name} ===`);
  console.log(JSON.stringify(m, null, 2));
  console.log(`workspaceWidth >= 1000: ${m.workspaceWidth} → ${wsOk ? 'PASS' : 'FAIL'}`);
  console.log(`asideWidth ~220: ${m.asideWidth} → ${asideOk ? 'PASS' : 'FAIL'}`);
  console.log(`gridTemplateColumns unchanged: ${m.layoutGridCols} → ${colsOk ? 'PASS' : 'FAIL'}`);
  console.log(`sidebar on correct side (${m.dir}): ws@${m.workspaceLeft}px aside@${m.asideLeft}px → ${asideAfterWorkspace ? 'PASS' : 'FAIL'}`);
  return pass;
}

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox'],
    ...(fs.existsSync(chrome) ? { executablePath: chrome } : {}),
  });
  const page = await browser.newPage();
  const cases = [
    ['BMI AR', `${BASE}/tools/bmi-calculator.html?lang=ar`],
    ['BMI EN', `${BASE}/tools/bmi-calculator.html?lang=en`],
    ['Body-fat AR', `${BASE}/tools/body-fat-calculator.html?lang=ar`],
    ['Body-fat EN', `${BASE}/tools/body-fat-calculator.html?lang=en`],
  ];
  let all = true;
  for (const [name, url] of cases) {
    const m = await measure(page, url);
    if (!check(name, m)) all = false;
  }
  await browser.close();
  process.exit(all ? 0 : 1);
})().catch(e => { console.error(e); process.exit(1); });
