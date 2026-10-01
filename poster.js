// Story görseli: node poster.js [çıktı.png]  (Playwright gerekir)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const out = process.argv[2] || 'dunya-kahve-gunu-story.png';
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(__dirname, 'animation.html') + '?render=1');
  await page.evaluate(() => window.ready);
  const b64 = await page.evaluate(() => { window.renderPoster(); return document.getElementById('c').toDataURL('image/png').split(',')[1]; });
  fs.writeFileSync(out, Buffer.from(b64, 'base64'));
  await browser.close();
  console.log('Hazır: ' + out);
})();
