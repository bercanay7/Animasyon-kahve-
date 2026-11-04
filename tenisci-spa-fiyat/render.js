// Renders index.html to a single-page PDF sized to the content (phone-friendly, 1080 px wide)
// and a PNG preview. Usage: NODE_PATH=$(npm root -g) node tenisci-spa-fiyat/render.js
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(dir, 'index.html'));
  await page.evaluate(() => document.fonts.ready);
  const height = await page.evaluate(() => Math.ceil(document.querySelector('.page').getBoundingClientRect().height));

  await page.emulateMedia({ media: 'screen' });
  await page.pdf({
    path: path.join(dir, 'navitas-tenisci-spa-fiyat-listesi.pdf'),
    width: '1080px',
    height: height + 'px',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
    pageRanges: '1',
  });
  await page.screenshot({ path: path.join(dir, 'onizleme.jpg'), fullPage: true, type: 'jpeg', quality: 88 });
  console.log('height', height);
  await browser.close();
})();
