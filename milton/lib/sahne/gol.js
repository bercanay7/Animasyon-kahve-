// Üslup karesi: yanan göl (A02). Dünya koordinatı 1920×1080.
// Değer planı (göz yormasın diye üç büyük kütle): zifiri tonoz (düz siyah), ufukta figürün arkasında tek parlak leke,
// koyu göl. Tarama yalnız geçişlerde; çizgi doğrultusu az (yatay göl, kavisli duman, ışın).
'use strict';
// cizGol: açık levhaya çizer (GR.begin/engrave çağırmaz). o: {eyes (göz açıklığı 0–1), chains (false: zincir yok), fig (false: figür yok)}
function cizGol(t, o = {}) {
  const { tx, tone, fill } = GR;
  const FX = 880, HZ = 600, WY = 800;                 // figür ekseni, ufuk, su çizgisi (figürün beli)
  // ── gök: zifiri; yalnız ufka yakın dar bir kuşak aydınlık ──
  let g = tx.createLinearGradient(0, 0, 0, HZ);
  g.addColorStop(0, tone(.02)); g.addColorStop(.55, tone(.04)); g.addColorStop(.84, tone(.14)); g.addColorStop(1, tone(.34));
  tx.fillStyle = g; tx.fillRect(0, 0, W, HZ);
  PR.glow(FX + 30, HZ - 10, 30, 660, 1, 1);          // ufuk parıltısı: karenin odağı, figürün arkası
  PR.glow(FX + 30, HZ - 40, 10, 260, 1, .7);
  // yitik cennetin yarığı: sağ üstte ince bir ışık, figüre inen seyrek huzme
  // yitik cennetin yarığı: sağ üstte keskin, dar bir yırtık; oradan başa inen birkaç ince huzme
  PR.rays(1610, 30, 0, 0, 0, 0, { seed: 4, slit: { w: 210, h: 22, a: -.12 } });
  PR.shafts(1590, 44, FX + 120, 500, { n: 6, w: 11, slitW: 70, spread: 560, seed: 6, t, v: .94, len: [.3, .92] });
  // duman tonozu: iki koyu kütle; yalnız ufuk ışığına bakan yumruların kenarında birer ikişer açık hilal; orta açık kalır (odak)
  PR.cloud({ x: 250, y: 330, w: 900, h: 230, seed: 12, lit: [.8, .6], base: .02, hi: .7, core: .02, n: 4, drift: Math.sin(t * .1) * 10 });
  PR.cloud({ x: 1640, y: 350, w: 800, h: 210, seed: 17, lit: [-.8, .6], base: .02, hi: .65, core: .02, n: 4, drift: Math.sin(t * .08 + 1) * 10 });
  // ── göl ──
  PR.lake(HZ, H, t, { tone: [.2, .02], crests: 26, refl: [{ x: FX + 30, w: 300, v: .7, len: 330 }, { x: 330, w: 110, v: .3 }, { x: 1420, w: 130, v: .34 }] });
  PR.flameBank(-60, W + 60, HZ + 2, 30, t, 1, { env: f => .2 + .8 * Math.pow(Math.sin(f * PI), 2) });
  PR.flameBank(1260, 1660, 672, 170, t, 5, { n: 3, wr: .5, curl: 1.6, env: f => .35 + .65 * Math.sin(f * PI) });
  PR.flameBank(170, 520, 704, 180, t, 9, { n: 3, wr: .5, curl: 1.6, env: f => .35 + .65 * Math.sin(f * PI) });
  // ── Şeytan: belden yukarısı gölün üstünde; arkadan aydınlanan koyu kütle, yüzü yarığa dönük ──
  const br = Math.sin(t * .6) * 2, h = 98;
  const J = SF.rig({ x: FX, y: WY + 26 + br * .3, h, facing: 1, twist: .3, lean: .04, head: .42, shTilt: -.06, armN: [-.5, .22], armF: [.55, -.2] });
  const LIT = [.55, -.8];
  // kanatlar suyun üstünde kalan kısmıyla çizilir (uçları suya girer)
  GR.save(); { const C = new Path2D(); C.rect(-4000, -4000, 12000, 4000 + WY); for (const c of [GR.tx, GR.px, GR.ox]) c.clip(C); }
  for (const [side, P] of [[-1, { span: 640, open: .78, lift: .5, droop: .25, rot: -.1, seed: 31, root: .1 }], [1, { span: 560, open: .7, lift: .2, droop: .8, rot: .12, seed: 32, root: .12 }]]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    GR.frame(sh[0] - side * h * .25, sh[1] + h * .15 + br, P.rot, side, 1);
    KN.feathered(Object.assign({ dark: .92, rim: .75, ruin: .65, t, lit: [LIT[0] * side, LIT[1]] }, P));
    GR.unframe();
  }
  GR.restore();
  PR.glow(FX, WY + 10, 6, 170, 1, .2);                 // su çizgisinde ateş ışığı (figürün arkasında kalır)
  SF.draw(J, { lum: 0, lit: LIT, t, legs: false, skirt: false, waterY: WY, eye: o.eyes ?? 1, wind: .6, cloak: 1.2 });
  // zincirler (kırılmaz zincir; I.48): ön kolun suya girdiği noktadan çıkar, su yüzeyinde dışa uzanır
  GR.tx.save(); { const C = new Path2D(); C.rect(-4000, -4000, 12000, 4000 + WY + 16); GR.tx.clip(C); }
  for (const [el, wr, dx] of [[J.elN, J.wrN, -120], [J.elF, J.wrF, 120]]) {
    const u = clamp((WY - 30 - el[1]) / ((wr[1] - el[1]) || 1)), x0 = lerp(el[0], wr[0], u);
    PR.chain(x0, WY - 30, x0 + dx, WY + 46, 34, { sag: -8, v: .9 });
  }
  GR.tx.restore();
  // bel hizası: su çizgisinde ince ışık ve figürü saran alevler (öndeki kütle)
  PR.flameBank(FX - 340, FX - 70, WY + 40, 190, t, 7, { n: 4, env: f => .45 + .55 * (1 - f), wr: .6 });
  PR.flameBank(FX + 80, FX + 370, WY + 38, 170, t, 8, { n: 4, env: f => .45 + .55 * f, wr: .6 });
  // sağ ön: büyük alev dilleri (çerçeve); sol ön: kaya kıyısı (koyu kütle, ışıklı sırt)
  PR.flameBank(1480, W + 120, H + 30, 380, t, 4, { env: f => .5 + .5 * f, wr: .5, base: .3, edge: .4, core: .8, frags: false });
  const RK = [[-20, 560], [70, 582], [130, 640], [205, 662], [236, 730], [300, 770], [318, 860], [386, 915], [404, H + 20], [-20, H + 20]];
  const RP = PR.rock(RK,
    { lit: [.85, -.45], hi: .05, mid: .03, lo: .02, seed: 2, th: -.9, rim: 6, facets: 10 });
  PR.cuts(RK.slice(0, 6), [-.5, .87], { len: [40, 130], gap: [34, 80], w: 5.5, seed: 5, clip: RP, bend: -.35 });
}
// tek başına üslup karesi (uslup.html)
function sahneGol(t, o = {}) {
  GR.begin(.04, 0, 1, o.cam); cizGol(t, o); GR.engrave(o.out || ctx);
  applyPaper(o.out || ctx, .8); applyVignette(o.out || ctx, .45);
}
