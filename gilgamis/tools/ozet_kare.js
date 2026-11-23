// Her plandan bir kare: node tools/ozet_kare.js <klasör> [oran=0.5] [--notext] [--rs=0.5] [--mb=1] [--sec=P001,P049|regex]
// Kareler <klasör>/<plan>.jpg, liste <klasör>/liste.json [{id, t, at, end, olcek, set, cap, dosya}]. kurgu_ozet.py ve sessiz okuma testi bunu kullanır.
// Plan zamanları sayfanın kendi çekim listesinden (geçiş normalleştirmesinden sonra) alınır.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const { serve } = require('./sunucu');
(async () => {
  const args = process.argv.slice(2), out = args.shift();
  const opt = Object.fromEntries(args.filter(a => a.startsWith('--')).map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? true]; }));
  const oran = +(args.find(a => !a.startsWith('--')) || .5);
  const sec = opt.sec ? (/^[P\d,]+$/.test(opt.sec) ? new RegExp('^(' + opt.sec.split(',').join('|') + ')$') : new RegExp(opt.sec)) : null;
  fs.mkdirSync(out, { recursive: true });
  const srv = await serve(), rs = +(opt.rs || .5), mb = +(opt.mb || 1);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: Math.round(1920 * rs), height: Math.round(1080 * rs) } });
  p.on('pageerror', e => console.log('[hata]', e.message));
  const q = ['render=1', 'rs=' + rs, opt.notext ? 'notext=1' : ''].filter(Boolean).join('&');
  await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?${q}`); await p.waitForFunction(() => window.READY, null, { timeout: 180000 });
  const shots = await p.evaluate(() => window.shotList().map(s => ({ ...s, olcek: (PLAN[s.id] || {}).olcek, set: (PLAN[s.id] || {}).set, cap: (PLAN[s.id] || {}).at })));
  const liste = [];
  for (const s of shots) {
    if (!s.id || (sec && !sec.test(s.id))) continue;
    const t = s.at + (s.end - s.at) * oran, fn = path.join(out, s.id + '.jpg');
    const b64 = await p.evaluate(({ t, mb }) => window.renderAt(t, mb).toDataURL('image/jpeg', .88).split(',')[1], { t, mb });
    fs.writeFileSync(fn, Buffer.from(b64, 'base64')); liste.push({ ...s, t: +t.toFixed(2), dosya: fn });
  }
  fs.writeFileSync(path.join(out, 'liste.json'), JSON.stringify(liste, null, 1));
  console.log(`${liste.length} kare → ${out}`);
  await b.close(); srv.close();
})();
