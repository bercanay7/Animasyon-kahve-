// Kapak kareleri: node kapak/kapak_shot.js <çıktı-klasörü> "v=a&renk=0" "v=b&renk=1&font=bebas" ...
// Her sorgu için 1920×1080 PNG yazar (ad: sorgudan türetilir). Küçültme ve JPG: kapak/jpg.py
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const [out, ...qs] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--disable-web-security'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => console.log('[err]', e.message));
  for (const q of qs) {
    await page.goto('file://' + path.resolve(__dirname, 'kapak.html') + '?render=1&' + q);
    await page.evaluate(() => window.ready);
    const t0 = Date.now();
    const b64 = await page.evaluate(async () => { await window.kapakCiz(); return document.getElementById('c').toDataURL('image/png').split(',')[1]; });
    const name = q.replace(/[&=]/g, '_').replace(/[^\w.-]/g, '') || 'kapak';
    const fn = path.join(out, name + '.png');
    fs.writeFileSync(fn, Buffer.from(b64, 'base64'));
    console.log(fn, Date.now() - t0, 'ms');
  }
  await browser.close();
})();
