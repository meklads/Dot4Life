const puppeteer = require('puppeteer');

const tools = [
"age-calculator","bmi-calculator","body-fat-calculator","calorie-calculator",
"currency-converter","hijri-converter","inheritance-calculator","monthly-budget",
"mortgage-calculator","one-rep-max","packing-checklist","password-generator",
"plant-watering","pomodoro","prayer-times","pregnancy-calculator","qibla",
"ramadan-calorie-calculator","rental-yield-calculator","return-to-hotel",
"roi-calculator","salary-calculator","savings-goal","travel-budget",
"travel-tips","water-calculator","zakat-calculator"
];

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/sessions/confident-gracious-einstein/.cache/puppeteer/chrome/linux_arm-150.0.7871.24/chrome-linux64/chrome',
    args: ['--no-sandbox','--disable-setuid-sandbox']
  });
  const results = [];
  for (const slug of tools) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 900 });
    const consoleErrors = [];
    page.on('pageerror', e => consoleErrors.push('JS:'+e.message));
    page.on('console', msg => { if (msg.type()==='error') consoleErrors.push('console:'+msg.text().slice(0,120)); });
    const url = `https://dotforlife.com/tools/${slug}.html?lang=ar`;
    let status = null, errNote = null;
    try {
      const resp = await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
      status = resp ? resp.status() : null;
    } catch (e) {
      errNote = 'NAV_FAIL: ' + e.message.slice(0,150);
    }
    let layout = {};
    if (!errNote) {
      layout = await page.evaluate(() => {
        const cl = document.querySelector('.tool-calc-layout');
        const ws = document.querySelector('.tool-workspace');
        const aside = document.querySelector('.tool-related-aside');
        const btn = document.querySelector('button[onclick], .tool-workspace button, .tool-mn button');
        return {
          hasCalcLayout: !!cl,
          hasAside: !!aside,
          wsWidth: ws ? Math.round(ws.getBoundingClientRect().width) : null,
          asideWidth: aside ? Math.round(aside.getBoundingClientRect().width) : null,
          h1: document.querySelector('h1') ? document.querySelector('h1').innerText.trim().slice(0,60) : null,
          hasCalcButton: !!btn,
          bodyText: document.body.innerText.length
        };
      });
    }
    let bugFlag = 'N/A';
    if (layout.hasCalcLayout && layout.wsWidth != null && layout.asideWidth != null) {
      bugFlag = (layout.wsWidth < layout.asideWidth) ? 'BUG (workspace<aside)' : 'OK';
    }
    results.push({ slug, status, errNote, ...layout, bugFlag, consoleErrors: consoleErrors.slice(0,2) });
    await page.close();
    console.log(slug, '->', status, bugFlag, layout.wsWidth, layout.asideWidth, errNote||'');
  }
  await browser.close();
  require('fs').writeFileSync('audit_results.json', JSON.stringify(results, null, 2));
  console.log('\n=== DONE ===');
})();
