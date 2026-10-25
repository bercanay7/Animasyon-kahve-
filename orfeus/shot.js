// node orfeus/shot.js <çıktı.png> "v=a&font=Anton"  → 1920×1080 PNG
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => {
  const [out, q] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--disable-web-security'] }); const pg = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  pg.on('pageerror', e => console.log('[err]', e.message)); pg.on('console', m => console.log('[page]', m.text()));
  await pg.goto('file://' + path.resolve(__dirname, 'kapak.html') + '?' + (q || '')); await pg.evaluate(() => window.ready);
  const b64 = await pg.evaluate(() => document.getElementById('c').toDataURL('image/png').split(',')[1]);
  fs.writeFileSync(out, Buffer.from(b64, 'base64')); await b.close();
})();
