// Yüksek anahtar denemesi: cennet (C02). Tarif, cehennem karesinin tersidir: hafif taralı açık gök üstünde
// kâğıt beyazı kütleler (bulut, kanat, beden); biçimi gölge yanındaki birkaç mürekkep hilali ve ince kontur verir.
// Tanrı ve Oğul yalnız ışık: sağ üstte figürsüz parlaklık ve oradan inen kâğıt beyazı ışık kamaları.
'use strict';
function cizCennet(t, o = {}) {
  const { tx, tone } = GR, FX = 640, FEET = 850, SX = 1560, SY = 40;
  let g = tx.createRadialGradient(SX, SY, 60, SX, SY, 1700);
  g.addColorStop(0, tone(1)); g.addColorStop(.2, tone(.93)); g.addColorStop(.45, tone(.76)); g.addColorStop(1, tone(.6));
  tx.fillStyle = g; tx.fillRect(-200, -200, W + 400, H + 400);
  // ışık kamaları (kâğıt boşluğu)
  tx.save(); tx.globalCompositeOperation = 'lighten';
  for (let i = 0; i < 5; i++) { const a = PI * (.58 + i * .09) + Math.sin(t * .1 + i) * .004, w = .02 + (i % 2) * .014;
    tx.fillStyle = tone(1); tx.beginPath(); tx.moveTo(SX, SY); tx.lineTo(SX + Math.cos(a - w) * 2200, SY + Math.sin(a - w) * 2200); tx.lineTo(SX + Math.cos(a + w) * 2200, SY + Math.sin(a + w) * 2200); tx.closePath(); tx.fill(); }
  tx.restore();
  // uzak bulut terası ve melek safı
  PR.cloud({ x: 1440, y: 700, w: 1000, h: 170, seed: 41, lit: [.3, -.9], base: .98, hi: .5, core: .98, n: 5, depth: .05, back: false });
  for (let i = 0; i < 11; i++) { const x = 1060 + i * 76 + Math.sin(i * 7.3) * 10, hh = 25;
    SF.draw(SF.rig({ x, y: 632 + Math.sin(i * 1.7) * 6 - hh * 4 + 100, h: hh, facing: -1, twist: .4, armN: [.1, .2], armF: [-.1, .2] }), { lum: 1, lit: [.5, -.8], t, lines: 0, armor: false, cloak: false, spear: { grip: 'N', ang: -.03 }, seed: i }); }
  // ön bulut terası
  PR.cloud({ x: 560, y: 990, w: 1500, h: 300, seed: 43, lit: [.5, -.85], base: .98, hi: .45, core: .98, n: 4, depth: .05, back: false, drift: Math.sin(t * .08) * 8 });
  // başmelek: kâğıt beyazı beden ve kanatlar; ışık sağ üstten
  const h = 62, LIT = [.6, -.75];
  const J = SF.rig({ x: FX, y: FEET - 4 * h, h, facing: 1, twist: .32, head: .25, armN: [-.12, .25], armF: [.5, .85] });
  for (const [side, P] of [[-1, { span: 520, open: .95, lift: .62, rot: -.1, seed: 11 }], [1, { span: 480, open: .9, lift: .8, rot: .08, seed: 12 }]]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    GR.frame(sh[0] - side * h * .25, sh[1] + h * .1, P.rot, side, 1);
    KN.feathered(Object.assign({ dark: 0, rim: .4, ruin: 0, droop: 0, t, lit: [LIT[0] * side, LIT[1]] }, P));
    GR.unframe();
  }
  SF.draw(J, { lum: 1, lit: LIT, t, cloak: .9, spear: { grip: 'F', ang: .05 } });
}
function sahneCennet(t, o = {}) { GR.begin(.9, 0, 1, o.cam); cizCennet(t, o); GR.engrave(o.out || ctx); applyPaper(o.out || ctx, .8); applyVignette(o.out || ctx, .25); }
