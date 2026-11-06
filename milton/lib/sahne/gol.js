// Üslup karesi: yanan göl (A02). Dünya koordinatı 1920×1080.
'use strict';
function sahneGol(t, o = {}) {
  const { tx, px, tone, pat, fill } = GR;
  GR.begin(.1, 0, 1);
  // tonoz: yukarıda zifiri; ufka doğru ateşin boğuk ışığı
  let g = tx.createLinearGradient(0, 0, 0, 600);
  g.addColorStop(0, tone(.05)); g.addColorStop(.5, tone(.14)); g.addColorStop(.85, tone(.5)); g.addColorStop(1, tone(.78));
  tx.fillStyle = g; tx.fillRect(0, 0, W, 600);
  // yitik cennetten sızan uzak ışık: sağ üstte, dumanın arasından
  PR.glow(1560, 40, 4, 260, 1, .7);
  PR.rays(1560, 30, PI * .55, PI * .9, 7, 950, { str: .22, seed: 4, t, blur: 22 });
  // duman: arka sıra (koyu), ön sıra (alttan ateşle aydınlanan karınlar)
  PR.cloud({ x: 380, y: 170, w: 1000, h: 230, seed: 3, lit: [.1, .9], base: .06, hi: .34, drift: Math.sin(t * .1) * 10 });
  PR.cloud({ x: 1180, y: 250, w: 900, h: 220, seed: 8, lit: [-.3, .9], base: .07, hi: .4, drift: Math.sin(t * .08 + 1) * 12 });
  PR.cloud({ x: 700, y: 430, w: 1700, h: 190, seed: 12, lit: [0, 1], base: .2, hi: .82, soft: 8 });
  PR.cloud({ x: 1650, y: 470, w: 700, h: 160, seed: 17, lit: [0, 1], base: .25, hi: .85, soft: 8 });
  // göl: koyu yüzey; ufuk bandında alev ışığı
  g = tx.createLinearGradient(0, 590, 0, H);
  g.addColorStop(0, tone(.7)); g.addColorStop(.12, tone(.3)); g.addColorStop(.5, tone(.14)); g.addColorStop(1, tone(.06));
  tx.fillStyle = g; tx.fillRect(0, 590, W, H - 590);
  PR.lake(590, H, t, { bands: 16 });
  // alev öbekleri: ufukta sürekli bant, ortada kümeler, sağ önde dev diller
  PR.flameBank(-60, W + 60, 600, 70, t, 1, { base: .7, wr: .5 });
  PR.flameBank(-80, 760, 760, 170, t, 2, { env: f => .4 + .6 * Math.sin(f * PI) });
  PR.flameBank(1100, W + 80, 800, 210, t, 3, { env: f => .5 + .5 * f });
  // alevlerin göldeki yansıması (aşağı uzanan açık lekeler)
  for (const [xx, yy, rr] of [[300, 790, 220], [1500, 830, 300], [900, 640, 400]]) {
    tx.save(); tx.globalCompositeOperation = 'lighter';
    const rg = tx.createRadialGradient(xx, yy, 2, xx, yy, rr); rg.addColorStop(0, 'rgba(255,255,255,.4)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
    tx.translate(xx, yy); tx.scale(1, .3); tx.translate(-xx, -yy);
    tx.fillStyle = rg; tx.fillRect(xx - rr, yy - rr, rr * 2, rr * 2); tx.restore();
  }
  // kanatlar (deneme): omuzlar (700, 640) civarı
  const wings = [];
  for (const side of [-1, 1]) {
    const m = GR.frame(700 + side * 40, 650, side < 0 ? -.35 : .35, side, 1);
    const wg = KN.feathered({ span: 560, open: .9, lift: .55, t, seed: side < 0 ? 3 : 4, dark: .35 });
    GR.unframe(); wings.push({ wg, m });
  }
  if (o.placeholder) { const P = new Path2D(); P.ellipse(760, 780, 300, 90, -.1, 0, TAU); P.ellipse(700, 640, 75, 150, -.2, 0, TAU); fill(P, tone(.6), { th: PI / 2 - .2, id: 5 }); }
  // sağ ön: dev alev dilleri (çerçeve)
  PR.flameBank(1450, W + 120, H + 30, 420, t, 4, { env: f => .5 + .5 * f, wr: .5 });
  // sol ön: kaya kıyısı
  PR.rock([[-20, 520], [90, 560], [190, 640], [300, 730], [380, 830], [460, 940], [520, H + 20], [-20, H + 20]],
    { lit: [.7, -.7], hi: .62, mid: .2, lo: .03, seed: 2, th: -.9 });
  GR.engrave(o.out || ctx, o.cam);
  for (const w of wings) KN.contour(o.out || ctx, w.wg, new DOMMatrix().scale(RS).multiply(w.m), 1.0, .7);
  applyPaper(o.out || ctx, .8);
  applyVignette(o.out || ctx, .65);
}
