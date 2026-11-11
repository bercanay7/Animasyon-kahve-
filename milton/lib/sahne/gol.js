// Üslup karesi: yanan göl (A02). Dünya koordinatı 1920×1080.
// Değer planı (göz yormasın diye üç büyük kütle): zifiri tonoz (düz siyah), ufukta figürün arkasında tek parlak leke,
// koyu göl. Tarama yalnız geçişlerde; çizgi doğrultusu az (yatay göl, kavisli duman, ışın).
'use strict';
function sahneGol(t, o = {}) {
  const { tx, tone, fill } = GR;
  GR.begin(.04, 0, 1, o.cam);
  const FX = 880, HZ = 600, WY = 800;                 // figür ekseni, ufuk, su çizgisi (figürün beli)
  // ── gök: zifiri; yalnız ufka yakın dar bir kuşak aydınlık ──
  let g = tx.createLinearGradient(0, 0, 0, HZ);
  g.addColorStop(0, tone(.02)); g.addColorStop(.55, tone(.04)); g.addColorStop(.82, tone(.16)); g.addColorStop(1, tone(.42));
  tx.fillStyle = g; tx.fillRect(0, 0, W, HZ);
  PR.glow(FX + 30, HZ - 10, 30, 560, 1, .95);          // ufuk parıltısı: karenin odağı, figürün arkası
  PR.glow(FX + 30, HZ - 40, 10, 260, 1, .7);
  // yitik cennetin yarığı: sağ üstte ince bir ışık, figüre inen seyrek huzme
  // yitik cennetin yarığı: sağ üstte keskin, dar bir yırtık; oradan başa inen birkaç ince huzme
  PR.rays(1610, 30, 0, 0, 0, 0, { seed: 4, slit: { w: 210, h: 22, a: -.12 } });
  PR.shafts(1590, 44, FX + 120, 500, { n: 4, w: 13, slitW: 130, spread: 330, seed: 6, t, v: .92, len: [.28, .62] });
  // duman tonozu: iki koyu kütle; yalnız ufuk ışığına bakan yumruların kenarında birer ikişer açık hilal; orta açık kalır (odak)
  PR.cloud({ x: 250, y: 330, w: 900, h: 230, seed: 12, lit: [.8, .6], base: .02, hi: .55, core: .02, n: 4, drift: Math.sin(t * .1) * 10 });
  PR.cloud({ x: 1640, y: 350, w: 800, h: 210, seed: 17, lit: [-.8, .6], base: .02, hi: .5, core: .02, n: 4, drift: Math.sin(t * .08 + 1) * 10 });
  // ── göl ──
  PR.lake(HZ, H, t, { tone: [.3, .02], refl: [{ x: FX + 30, w: 300, v: .7, len: 330 }, { x: 330, w: 110, v: .3 }, { x: 1420, w: 130, v: .34 }] });
  PR.flameBank(-60, W + 60, HZ + 2, 44, t, 1, { env: f => .2 + .8 * Math.pow(Math.sin(f * PI), 2) });
  PR.flameBank(1180, 1700, 668, 120, t, 5, { env: f => .35 + .65 * Math.sin(f * PI) });
  PR.flameBank(120, 560, 700, 130, t, 9, { env: f => .35 + .65 * Math.sin(f * PI) });
  // ── Şeytan: belden yukarısı gölün üstünde; arkadan aydınlanan koyu kütle, yüzü yarığa dönük ──
  const br = Math.sin(t * .6) * 2, h = 98;
  const J = SF.rig({ x: FX, y: WY + 26 + br * .3, h, facing: 1, twist: .3, lean: .05, head: .35, shTilt: .06,
    armN: [-.42, .3], armF: [.5, -.22], legN: [.05, -.05], legF: [-.05, -.04] });
  const LIT = [.55, -.8];
  for (const [side, P] of [[-1, { span: 640, open: .78, lift: .5, droop: .25, rot: -.1, seed: 31, root: .1 }], [1, { span: 560, open: .7, lift: .2, droop: .8, rot: .12, seed: 32, root: .12 }]]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    GR.frame(sh[0] - side * h * .25, sh[1] + h * .15 + br, P.rot, side, 1);
    KN.feathered(Object.assign({ dark: .92, rim: .75, ruin: .65, t, lit: [LIT[0] * side, LIT[1]] }, P));
    GR.unframe();
  }
  SF.draw(J, { lum: 0, lit: LIT, t, legs: false, skirt: false, waterY: WY, eye: o.eyes ?? 1, wind: .6 });
  // zincirler: bileklerden göle (kırılmaz zincir; I.48)
  PR.chain(J.wrN[0], J.wrN[1], J.wrN[0] - 150, WY + 44, 34, { sag: 14, v: .9 });
  PR.chain(J.wrF[0], J.wrF[1], J.wrF[0] + 170, WY + 40, 34, { sag: 14, v: .9 });
  // bel hizası: su çizgisinde ince ışık ve figürü saran alevler (öndeki kütle)
  PR.glow(FX, WY + 10, 6, 170, 1, .2);
  PR.flameBank(FX - 330, FX - 60, WY + 36, 120, t, 7, { env: f => .4 + .6 * (1 - f), wr: .55 });
  PR.flameBank(FX + 70, FX + 360, WY + 34, 110, t, 8, { env: f => .4 + .6 * f, wr: .55 });
  // sağ ön: büyük alev dilleri (çerçeve); sol ön: kaya kıyısı (koyu kütle, ışıklı sırt)
  PR.flameBank(1480, W + 120, H + 30, 380, t, 4, { env: f => .5 + .5 * f, wr: .5, base: .3, edge: .4, core: .8 });
  PR.rock([[-20, 560], [70, 582], [130, 640], [205, 662], [236, 730], [300, 770], [318, 860], [386, 915], [404, H + 20], [-20, H + 20]],
    { lit: [.85, -.45], hi: .05, mid: .03, lo: .02, seed: 2, th: -.9, rim: 6, facets: 10 });
  GR.engrave(o.out || ctx);
  applyPaper(o.out || ctx, .8);
  applyVignette(o.out || ctx, .6);
}
