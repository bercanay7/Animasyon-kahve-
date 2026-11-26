// node araclar/manken/alt_bant.js <sahne.html (depo köküne göre)> [adım sn = 0.5] [sorgu]
// Alt bant denetimi (lale-cilginligi/tools/alt_bant.js'in genel hâli): sahne boyunca her adımda bir kare çizilir;
// ekrana basılan her yazının (fillText/strokeText, hangi tuvalde olursa olsun: 2B plakalar dahil) cihaz y'si ölçülür.
// Yazının alt kenarı 880'i aşarsa listelenir (altyazının yeri). Kod taraması değil ölçüm.
const { chromium } = require('playwright'); const S = require('../../dorian-gray/tools/sunucu.js');
const [sahne, adimS = '0.5', sorgu = ''] = process.argv.slice(2);
(async () => {
  const srv = await S.baslat(), br = await chromium.launch();
  try {
    const p = await br.newPage({ viewport: { width: 1920, height: 1080 } });
    await p.goto(`http://127.0.0.1:${srv.address().port}/${sahne}?render=1${sorgu ? '&' + sorgu : ''}`);
    await p.waitForFunction(() => window.READY || window.HATA, null, { timeout: 120000 });
    const out = await p.evaluate(adim => {
      const vur = [], say = { yazi: 0 }; let t = 0;
      for (const ad of ['fillText', 'strokeText']) {
        const f0 = CanvasRenderingContext2D.prototype[ad];
        CanvasRenderingContext2D.prototype[ad] = function (s, x, y, ...r) {
          const m = this.getTransform(), k = 1080 / this.canvas.height, px = +((this.font.match(/([\d.]+)px/) || [0, 30])[1]);
          const yy = (m.b * x + m.d * y + m.f) * k, alt = yy + px * Math.hypot(m.c, m.d) * k * .55;
          if (String(s).trim() && this.globalAlpha > .05) { say.yazi++; if (alt > 880) vur.push({ t: +t.toFixed(2), s: String(s).slice(0, 40), alt: Math.round(alt) }); }
          return f0.call(this, s, x, y, ...r);
        };
      }
      for (t = 0; t <= window.DUR; t += adim) window.renderFrame(t);
      return { vur, say: say.yazi, kare: Math.floor(window.DUR / adim) + 1 };
    }, +adimS);
    console.log(`${out.kare} kare, ${out.say} yazı çağrısı ölçüldü`);
    console.log(out.vur.length ? out.vur.map(h => `${h.t}s alt=${h.alt} "${h.s}"`).join('\n') : 'alt bant temiz (y > 880 yazı yok)');
  } finally { await br.close(); srv.close(); }
})().catch(e => { console.error(e); process.exit(1); });
