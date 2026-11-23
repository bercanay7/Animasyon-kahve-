// Shorts kareleri: node shorts-sart/tools/kare.js <proje> <çıktı_klasörü> [--yazisiz] [--mb=4] [--her=1.0 | t1 t2 …]
// --her=s: s saniyede bir kare (ve her kesitin ilk karesi); yoksa verilen Shorts zamanları. Kare çizim süresi yazılır.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
const { serve } = require('./sunucu');
(async () => {
  const args = process.argv.slice(2), proje = args.shift(), out = path.resolve(args.shift());
  const opt = Object.fromEntries(args.filter(a => a.startsWith('--')).map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? true]; }));
  let ts = args.filter(a => !a.startsWith('--')).map(Number);
  fs.mkdirSync(out, { recursive: true });
  const srv = await serve(), port = srv.address().port, br = await chromium.launch();
  const p = await br.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.log('[hata]', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('[konsol]', m.text()); });
  await p.goto(`http://127.0.0.1:${port}/shorts-sart/${path.basename(path.resolve(proje))}/index.html?render=1&notext=1`);
  await p.waitForFunction(() => window.READY, null, { timeout: 180000 });
  if (opt.yazisiz) await p.evaluate(() => { window.SART_YAZISIZ = true; });
  if (opt.her) {
    const S = await p.evaluate(() => ({ D: SHORTS.DUR, K: SHORTS.KES.map(k => k.t0) }));
    ts = []; for (let t = 0; t < S.D; t += +opt.her) ts.push(+t.toFixed(2));
    for (const k of S.K) ts.push(+(k + .05).toFixed(2)); ts = [...new Set(ts)].sort((a, b) => a - b);
  }
  for (const t of ts) {
    const t0 = Date.now();
    const b64 = await p.evaluate(({ t, mb }) => renderShort(t, mb).toDataURL('image/jpeg', .9).split(',')[1], { t, mb: +(opt.mb || 1) });
    const f = path.join(out, `s${t.toFixed(2).padStart(6, '0')}.jpg`); fs.writeFileSync(f, Buffer.from(b64, 'base64'));
    console.log(f, ((Date.now() - t0) / 1000).toFixed(2), 'sn');
  }
  await br.close(); srv.close();
})();
