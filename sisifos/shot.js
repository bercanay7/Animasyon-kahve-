// Tek kareler: node shot.js <çıktı-klasörü> t1 t2 ...  (SCENE=... ile sahne seçimi, MB=n)
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const [out, ...ts] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--disable-web-security'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => console.log('[err]', e.message));
  const q = new URLSearchParams({ render: 1, ...(process.env.SCENE ? { scene: process.env.SCENE } : {}) });
  await page.goto('file://' + path.resolve(__dirname, 'film.html') + '?' + q);
  await page.evaluate(() => window.ready);
  const mb = +(process.env.MB || 1);
  for (const t of ts) {
    const t0 = Date.now();
    const b64 = await page.evaluate(({ t, mb }) => { mb > 1 ? renderFrameMB(+t, mb) : renderFrame(+t); return document.getElementById('c').toDataURL('image/png').split(',')[1]; }, { t, mb });
    const fn = path.join(out, `t${String(Number(t).toFixed(2)).padStart(7, '0')}.png`);
    fs.writeFileSync(fn, Buffer.from(b64, 'base64'));
    console.log(fn, Date.now() - t0, 'ms');
  }
  await browser.close();
})();
