// Hareket ölçümü (render gerektirmez): her adımda t ile t+1/15 sn karelerinin 320×180 gri ortalama farkı
// (çizimlerin çoğu 15 fps "ikişerli" olduğundan bir kare sonrası değil, iki kare sonrası karşılaştırılır).
// node tools/hareket.js [adım=0.5] [t0=0] [t1=DUR] → en durgun anlar ve çekim başına ortalama
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [step = .5, a0, a1] = process.argv.slice(2).map(Number);
  const browser = await chromium.launch({ args: ['--disable-web-security'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.log('[err]', e.message));
  await page.goto('file://' + path.resolve(__dirname, '..', 'film.html') + '?render=1');
  await page.evaluate(() => window.ready);
  const res = await page.evaluate(({ step, a0, a1 }) => {
    const sm = document.createElement('canvas'); sm.width = 320; sm.height = 180; const g = sm.getContext('2d', { willReadFrequently: true });
    const grab = t => { renderFrame(t); g.drawImage(document.getElementById('c'), 0, 0, 320, 180); const d = g.getImageData(0, 0, 320, 180).data; const o = new Float32Array(320 * 180); for (let i = 0; i < o.length; i++) o[i] = .299 * d[4 * i] + .587 * d[4 * i + 1] + .114 * d[4 * i + 2]; return o; };
    const out = [], t1 = isNaN(a1) ? window.DUR - .1 : a1;
    for (let t = isNaN(a0) ? 0 : a0; t < t1; t += step) {
      const x = grab(t), y = grab(t + 1 / 15); let s = 0; for (let i = 0; i < x.length; i++) s += Math.abs(x[i] - y[i]);
      out.push([+t.toFixed(2), s / x.length]);
    }
    return out;
  }, { step, a0, a1 });
  await browser.close();
  const v = res.map(r => r[1]).sort((a, b) => a - b);
  console.log(`örnek ${res.length}; kare farkı medyan ${v[v.length >> 1].toFixed(2)}, %10 ${v[Math.floor(v.length * .1)].toFixed(2)}, en düşük ${v[0].toFixed(2)}`);
  console.log('en durgun 15 an:', res.slice().sort((a, b) => a[1] - b[1]).slice(0, 15).map(r => `${r[0]}(${r[1].toFixed(2)})`).join(' '));
  require('fs').writeFileSync(process.env.OUT || '/dev/null', JSON.stringify(res));
})();
