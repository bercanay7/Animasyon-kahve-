// Ses efekti işaretlerini dışa aktarır: node tools/export_sfx.js → audio/sfx_events.json
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('pageerror', e => console.log('[err]', e.message));
  await page.goto('file://' + path.resolve(__dirname, '..', 'film.html') + '?render=1');
  await page.evaluate(() => window.ready);
  const ev = await page.evaluate(() => window.SFX);
  const out = path.resolve(__dirname, '..', 'audio', 'sfx_events.json');
  fs.writeFileSync(out, JSON.stringify(ev, null, 0).replace(/},{/g, '},\n{'));
  console.log(ev.length, 'olay →', out);
  await browser.close();
})();
