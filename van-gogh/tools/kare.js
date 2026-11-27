// node van-gogh/tools/kare.js <çıktı klasörü> t1,t2,…  [Q=ss=1]  → kare_<t>.jpg (film.html, yerel sunucu); süre ölçümü yazar
// PLAN=1: her planın ortasından bir kare (kurgu özeti), çıktıya plan kimliğiyle
const { chromium } = require('playwright'); const S = require('../../dorian-gray/tools/sunucu.js'); const fs = require('fs'), path = require('path');
(async () => {
  const [out, ts] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const srv = await S.baslat(), br = await chromium.launch(), p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('[hata]', e.message)); p.on('console', m => { const s = m.text(); if (!/GL Driver|GPU stall/.test(s)) console.log('[c]', s); });
  const t0 = Date.now();
  await p.goto(`http://127.0.0.1:${srv.address().port}/van-gogh/film.html?render=1${process.env.Q ? '&' + process.env.Q : ''}`);
  await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 600000 });
  const h = await p.evaluate(() => window.HATA); if (h) { console.log(h); process.exit(1); }
  console.log('hazır', ((Date.now() - t0) / 1000).toFixed(1), 'sn');
  let list;
  if (process.env.PLAN) { const P = await p.evaluate(() => window.PLANLAR); list = P.filter(q => !process.env.SADECE || process.env.SADECE.split(',').includes(q.id)).map(q => [q.s + q.d * (+process.env.PLAN === 1 ? .5 : +process.env.PLAN), q.id + '_' + q.olcek]); }
  else list = ts.split(',').map(t => [+t, 't' + (+t).toFixed(2)]);
  for (const [t, ad] of list) {
    const r = await p.evaluate(t => { const a = performance.now(); window.renderAt(t); window.BITIR(); return { d: performance.now() - a, u: document.getElementById('c').toDataURL('image/jpeg', .9).split(',')[1] }; }, t);
    fs.writeFileSync(path.join(out, ad + '.jpg'), Buffer.from(r.u, 'base64')); console.log(ad, t.toFixed(2), Math.round(r.d), 'ms');
  }
  await br.close(); srv.close();
})().catch(e => { console.error(e); process.exit(1); });
