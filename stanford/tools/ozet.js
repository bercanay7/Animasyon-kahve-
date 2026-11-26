// Kurgu özeti: her plandan bir kare (planın %55'i), küçük boy, ızgara sayfa. node tools/ozet.js ÇIKTI_KLASÖRÜ [ilk-id] [son-id] [--tam]
const { chromium } = require('playwright'); const { serve } = require('./sunucu'); const fs = require('fs'), path = require('path');
(async () => {
  const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
  const tam = process.argv.includes('--tam'); const args = process.argv.slice(3).filter(a => !a.startsWith('--'));
  const srv = await serve(), port = srv.address().port, b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('HATA', e.message)); p.on('console', m => { if (/yok|bozuk|iki kez|Error/.test(m.text())) console.log('k:', m.text()); });
  await p.goto(`http://127.0.0.1:${port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
  let L = await p.evaluate(() => window.shotList());
  if (args[0]) { const i0 = L.findIndex(s => s.id === args[0]), i1 = args[1] ? L.findIndex(s => s.id === args[1]) : i0; L = L.slice(i0, i1 + 1); }
  const kare = [];
  for (const s of L) {
    const t = s.at + (s.end - s.at) * .55, t0 = Date.now();
    const url = await p.evaluate(([t, w]) => { const c = window.renderAt(t, 1); const o = document.createElement('canvas'); o.width = w; o.height = w * 9 / 16; o.getContext('2d').drawImage(c, 0, 0, o.width, o.height); return o.toDataURL('image/jpeg', .85); }, [t, tam ? 1920 : 480]);
    const f = path.join(out, `${s.id}.jpg`); fs.writeFileSync(f, Buffer.from(url.split(',')[1], 'base64')); kare.push({ ...s, f, ms: Date.now() - t0 });
  }
  // ızgara sayfası
  if (!tam) { const cols = 4, html = `<body style="margin:0;background:#222;color:#eee;font:14px sans-serif"><div style="display:grid;grid-template-columns:repeat(${cols},480px);gap:4px">${kare.map(k => `<div><img src="file://${k.f}" width=480><br>${k.id} ${k.at.toFixed(1)}–${k.end.toFixed(1)} ${k.tr}</div>`).join('')}</div></body>`;
    fs.writeFileSync(path.join(out, 'ozet.html'), html); const q = await b.newPage({ viewport: { width: cols * 484, height: 300 } }); await q.goto('file://' + path.join(out, 'ozet.html')); await q.screenshot({ path: path.join(out, 'ozet.png'), fullPage: true }); }
  console.log(kare.map(k => `${k.id} ${k.ms}ms`).join(' | '));
  await b.close(); srv.close();
})();
