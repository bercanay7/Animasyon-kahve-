// Lale'den uyarlandı.
// Alt bant denetimi: her planın başı, ortası ve sonu render edilir; ekrana çizilen her yazının (fillText) cihaz y'si ölçülür.
// Yazının alt kenarı 880'i aşarsa listelenir (altyazının yeri). node tools/alt_bant.js
const { chromium } = require('playwright'); const { serve } = require('./sunucu');
(async () => {
  const srv = await serve(), br = await chromium.launch();
  try {
    const p = await br.newPage({ viewport: { width: 1920, height: 1080 } }); await p.goto(`http://127.0.0.1:${srv.address().port}/film.html?render=1`); await p.waitForFunction(() => window.READY, null, { timeout: 120000 });
    const out = await p.evaluate(() => {
      const hits = []; let cur = null; const f0 = CanvasRenderingContext2D.prototype.fillText;
      CanvasRenderingContext2D.prototype.fillText = function (s, x, y, ...r) {
        if (cur && this.canvas.width === DW) { const m = this.getTransform(), px = +((this.font.match(/([\d.]+)px/) || [0, 30])[1]), yy = m.b * x + m.d * y + m.f, sc = Math.hypot(m.c, m.d), alt = yy + px * sc * .55;
          if (alt > 880 && this.globalAlpha > .05 && String(s).trim()) hits.push({ plan: cur.id, t: +cur.t.toFixed(1), s: String(s).slice(0, 40), alt: Math.round(alt) }); }
        return f0.call(this, s, x, y, ...r); };
      shotAt(0); const L = SHOTS.map((s, i) => ({ id: s.id, at: s.at, d: shotState(i, s.at).d }));
      for (const x of L) for (const q of [.15, .5, .9]) { cur = { id: x.id, t: x.at + x.d * q }; renderFrame(cur.t); drawOver(document.getElementById('c').getContext('2d'), cur.t); }
      cur = null; const u = {}; for (const h of hits) { const k = h.plan + '|' + h.s; if (!u[k] || u[k].alt < h.alt) u[k] = h; } return Object.values(u);
    });
    console.log(out.length ? out.map(h => `${h.plan} ${h.t}s alt=${h.alt} "${h.s}"`).join('\n') : 'alt bant temiz');
  } finally { await br.close(); srv.close(); }
})();
