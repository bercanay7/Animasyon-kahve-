// Dorian Gray kapısı: GRAVÜR çizici (milton/lib/gravur.js motoru; ortak SAHNE'yi tarama baskısına çevirir).
'use strict';
(function (g) {
  const SH = g.SAHNE;
  const IDT = { a: 0, k: 1, x: 0, y: 0 };
  // R adaptörü: SAHNE levhalarının çağırdığı fill/line → GR ton + yama katmanları
  const R = {
    fill(pf, o) { const p = new Path2D(); pf(p); GR.fill(p, GR.tone(o.ton != null ? o.ton : SH.lum(o.c)), o.h || { th: 0, id: 0 }); },
    line(pf, c, w, o = {}) {
      const p = new Path2D(); pf(p);
      for (const [cx, st] of [[GR.tx, GR.tone(o.ton != null ? o.ton : SH.lum(c))], [GR.px, GR.hatch(o.h || { th: 0, id: 0 })]]) { cx.lineWidth = w; cx.lineCap = 'round'; cx.strokeStyle = st; cx.stroke(p); }
    },
    tint() {}
  };
  function levha(ad, tr) { const T = tr || IDT; GR.frame(T.x, T.y, T.a || 0, 1, T.k || 1); SH.LEV[ad].draw(R); GR.unframe(); }
  function isik(L, amt = 1) {   // lamba ışığı: ton katmanını açar (screen)
    const tx = GR.tx; tx.save(); tx.globalCompositeOperation = 'screen';
    const gr = tx.createRadialGradient(L.x, L.y, L.r0, L.x, L.y, L.r1);
    gr.addColorStop(0, `rgba(255,255,255,${.85 * amt})`); gr.addColorStop(.25, `rgba(255,255,255,${.42 * amt})`); gr.addColorStop(.6, `rgba(255,255,255,${.12 * amt})`); gr.addColorStop(1, 'rgba(255,255,255,0)');
    tx.fillStyle = gr; tx.fillRect(-100, -100, 2200, 1300); tx.restore();
  }
  function alev(t) {
    const f = SH.alev(t), p = new Path2D(), s = f.s;
    p.moveTo(f.x - 9 * s, f.y + 8); p.bezierCurveTo(f.x - 12 * s, f.y - 10 * s, f.x + f.lean * 60, f.y - 30 * s, f.x + f.lean * 80, f.y - 46 * s);
    p.bezierCurveTo(f.x + 12 * s, f.y - 24 * s, f.x + 11 * s, f.y - 6 * s, f.x + 9 * s, f.y + 8); p.closePath();
    GR.fill(p, GR.tone(1), { th: Math.PI / 2, id: 3 });
  }
  // sahne çizimi; skip: { portre: true } karma aday için (portre alanı ayrıca boyanacak)
  function draw(ctx, t, o = {}) {
    const c = SH.cam(t), z = c.z;
    GR.begin(.12, 0, 0, { x: c.cx - 960 / z, y: c.cy - 540 / z, s: z });
    for (const [ad, fn] of SH.SIRA) {
      if (ad === 'dorian') isik(SH.LEV.oda.light, 1);          // ışık oda, portre ve örtüye; Dorian sırtı lambaya dönük, koyu kalır
      levha(ad, fn ? fn(t) : null);
    }
    alev(t);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 1920, 1080); ctx.restore();
    GR.engrave(ctx);
    applyPaper(ctx, .8); applyVignette(ctx, .9);
  }
  g.GRAVUR = { draw };
})(window);
