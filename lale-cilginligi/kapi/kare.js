// node kapi/kare.js sahne t çıktı.png
const { chromium } = require('playwright'); const S = require('../tools/sunucu');
(async () => { const [sc, t, out] = process.argv.slice(2); const srv = await S.baslat(); const br = await chromium.launch(); const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('[hata]', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('[konsol]', m.text()); });
  await p.goto(`http://127.0.0.1:${srv.address().port}/lale-cilginligi/kapi/kapi.html?render=1&scene=${sc}`); await p.waitForFunction(() => window.READY || window.HATA);
  const h = await p.evaluate(() => window.HATA); if (h) { console.log(h); process.exit(1); }
  const t0 = Date.now(); const b64 = await p.evaluate(t => window.renderFrame(+t).toDataURL('image/png').split(',')[1], t); console.log(sc, t, (Date.now() - t0) + ' ms');
  require('fs').writeFileSync(out, Buffer.from(b64, 'base64')); await br.close(); srv.close(); })();
