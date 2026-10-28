// Film şeridi: tüm filmden her N saniyede bir küçük kare + çekim listesi ve konsol hataları.
// node tools/serit.js <çıktı-klasörü> [adım=2] [t0=0] [t1=DUR]
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const [out, step = 2, a0, a1] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--disable-web-security'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const errs = [];
  page.on('pageerror', e => errs.push(e.message));
  page.on('console', m => { if (m.type() === 'error' || m.text().startsWith('Wd:')) errs.push(m.text()); });
  await page.goto('file://' + path.resolve(__dirname, '..', 'film.html') + '?render=1');
  await page.evaluate(() => window.ready);
  const info = await page.evaluate(() => ({ dur: window.DUR, shots: SHOTS.map(s => ({ at: +s.at.toFixed(2), tr: s.tr ? s.tr.type : null })) }));
  fs.writeFileSync(path.join(out, 'cekimler.json'), JSON.stringify(info, null, 1));
  const t0 = +(a0 || 0), t1 = +(a1 || info.dur);
  for (let t = t0; t <= t1 + 1e-6; t += +step) {
    const b64 = await page.evaluate(t => {
      renderFrame(t);
      const c = document.createElement('canvas'); c.width = 384; c.height = 216;
      c.getContext('2d').drawImage(document.getElementById('c'), 0, 0, 384, 216);
      return c.toDataURL('image/jpeg', .8).split(',')[1];
    }, t);
    fs.writeFileSync(path.join(out, `s${t.toFixed(1).padStart(6, '0')}.jpg`), Buffer.from(b64, 'base64'));
  }
  console.log('çekim', info.shots.length, 'süre', info.dur, 'hata', errs.length);
  for (const e of [...new Set(errs)].slice(0, 20)) console.log('[err]', e);
  await browser.close();
})();
