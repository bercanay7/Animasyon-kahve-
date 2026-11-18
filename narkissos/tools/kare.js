// Tek kareler: node tools/kare.js <çıktı_klasörü> [seçenek…] <iş…>
// İş: 12.3 (film zamanı) | ad=12.3 | P053 (planın ortası) | P053:0.2 (plan süresinin %20'si) | ad=P053:0.8
// Seçenek: --mb=4 (hareket bulanıklığı alt karesi; varsayılan 1) --notext (ekran yazısız) --rs=0.5 (yarım çözünürlük) --jpg
// Kare adı verilmezse t012.30.png ya da P053_0.50.png. Çizim süresi her kare için yazılır.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const { serve } = require('./sunucu');
(async () => {
  const args = process.argv.slice(2), out = args.shift();
  const opt = Object.fromEntries(args.filter(a => a.startsWith('--')).map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? true]; }));
  const jobs = args.filter(a => !a.startsWith('--'));
  fs.mkdirSync(out, { recursive: true });
  const srv = await serve(), port = srv.address().port;
  const rs = +(opt.rs || 1), browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: Math.round(1920 * rs), height: Math.round(1080 * rs) } });
  page.on('pageerror', e => console.log('[hata]', e.message));
  page.on('console', m => { const s = m.text(); if (m.type() === 'error' || /yok|bozuk|iki kez/.test(s)) console.log('[konsol]', s); });
  const q = ['render=1', opt.notext ? 'notext=1' : '', rs !== 1 ? 'rs=' + rs : ''].filter(Boolean).join('&');
  await page.goto(`http://127.0.0.1:${port}/film.html?${q}`);
  await page.waitForFunction(() => window.READY, null, { timeout: 120000 });
  const shots = await page.evaluate(() => window.shotList());
  const mb = +(opt.mb || 1), fmt = opt.jpg ? 'jpg' : 'png';
  for (const j of jobs) {
    let [ad, spec] = j.includes('=') ? j.split('=') : [null, j];
    let t;
    const m = spec.match(/^(P\d{3})(?::([\d.]+))?$/);
    if (m) { const s = shots.find(x => x.id === m[1]); if (!s) { console.log('plan yok:', m[1]); continue; } const r = m[2] != null ? +m[2] : .5; t = s.at + (s.end - s.at) * r; ad = ad || `${m[1]}_${r.toFixed(2)}`; }
    else { t = +spec; ad = ad || 't' + t.toFixed(2).padStart(6, '0'); }
    const t0 = Date.now();
    const b64 = await page.evaluate(({ t, mb, f }) => window.renderAt(t, mb).toDataURL(f === 'jpg' ? 'image/jpeg' : 'image/png', .92).split(',')[1], { t, mb, f: fmt });
    const fn = path.join(out, /\.(png|jpe?g)$/i.test(ad) ? ad : `${ad}.${fmt}`);
    fs.writeFileSync(fn, Buffer.from(b64, 'base64'));
    console.log(fn, `t=${t.toFixed(2)}`, ((Date.now() - t0) / 1000).toFixed(2) + ' sn');
  }
  await browser.close(); srv.close();
})();
