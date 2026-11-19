// node kapak/cek.js <html> <çıktı.jpg>  — 1280×720 kapak ekran görüntüsü (yerel http)
const { chromium } = require('playwright'); const path = require('path');
const { serve } = require('../tools/sunucu');
(async () => {
  const srv = await serve(), port = srv.address().port;
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  await p.goto(`http://127.0.0.1:${port}/kapak/${path.basename(process.argv[2])}`); await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300); await p.screenshot({ path: process.argv[3], type: 'jpeg', quality: 92 });
  await b.close(); srv.close();
})();
