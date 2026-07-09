#!/usr/bin/env node
/** BMI range gauge — 3 values must move marker to distinct positions */
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const baseUrl = process.env.BMI_TEST_URL || 'http://127.0.0.1:8765/tools/bmi-calculator.html';
const shots = path.join(__dirname, '..', 'operating-system', 'screenshots');
fs.mkdirSync(shots, { recursive: true });

const CASES = [
  { name: 'underweight', h: '175', w: '50', minPct: 3, maxPct: 10 },
  { name: 'normal', h: '175', w: '75', minPct: 32, maxPct: 44 },
  { name: 'obese', h: '175', w: '100', minPct: 65, maxPct: 76 },
];

(async () => {
  const chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox'],
    ...(fs.existsSync(chrome) ? { executablePath: chrome } : {}),
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  await page.goto(baseUrl, { waitUntil: 'networkidle0' });

  const positions = [];
  for (const c of CASES) {
    await page.evaluate(() => {
      const sel = document.getElementById('bm-unit');
      if (sel) { sel.value = 'metric'; }
    });
    await page.evaluate(() => { if (typeof toggleUnit === 'function') toggleUnit(); });
    await page.$eval('#bm-height', (el, v) => { el.value = v; el.dispatchEvent(new Event('input')); }, c.h);
    await page.$eval('#bm-weight', (el, v) => { el.value = v; el.dispatchEvent(new Event('input')); }, c.w);
    await page.evaluate(() => { if (typeof calculate === 'function') calculate(); });
    await new Promise(r => setTimeout(r, 300));

    const data = await page.evaluate(() => {
      const marker = document.querySelector('#bmi-gauge .tool-gauge-marker');
      const gauge = document.getElementById('bmi-gauge');
      const track = document.querySelector('#bmi-gauge .tool-gauge-track');
      if (!marker || !track || !gauge || gauge.hidden) return null;
      const trackRect = track.getBoundingClientRect();
      const markerRect = marker.getBoundingClientRect();
      const center = markerRect.left + markerRect.width / 2;
      const pct = ((center - trackRect.left) / trackRect.width) * 100;
      return {
        pct: Math.round(pct * 10) / 10,
        bmi: document.getElementById('res-bmi')?.textContent,
        label: document.getElementById('bmi-gauge-label')?.textContent,
        visible: gauge.classList.contains('is-active'),
      };
    });

    if (!data) {
      console.error('FAIL: gauge not visible for', c.name);
      process.exit(1);
    }

    const ok = data.pct >= c.minPct && data.pct <= c.maxPct;
    console.log(`${ok ? 'PASS' : 'FAIL'}: ${c.name} — BMI ${data.bmi}, marker ${data.pct}% (expect ${c.minPct}-${c.maxPct}%) · ${data.label}`);
    positions.push({ case: c.name, pct: data.pct });
    await page.screenshot({ path: path.join(shots, `bmi-gauge-${c.name}.png`) });
  }

  const distinct = new Set(positions.map(p => Math.round(p.pct))).size === 3;
  console.log(distinct ? 'PASS: marker moves to 3 distinct positions' : 'FAIL: marker positions not distinct', positions);

  await browser.close();
  process.exit(distinct && CASES.every((c, i) => {
    const p = positions[i].pct;
    return p >= c.minPct && p <= c.maxPct;
  }) ? 0 : 1);
})().catch(err => { console.error(err); process.exit(1); });
