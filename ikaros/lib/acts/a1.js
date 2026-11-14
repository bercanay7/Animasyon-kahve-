// Perde 1 (P01–P08): İki uyarı · Havaya kimse sahip değil. Plan listesi: animatik/planlar.json
'use strict';
// ortak dekor: deniz (y'den aşağı), parıltılar, yakın bantlar
function a1_deniz(pr, y, t, o = {}) {
  const c = pr.cam, x0 = c.x - 200, w = W / c.s + 400;
  const sea = new Path2D(); sea.rect(x0, y, w, 1400); pr.ink(sea, 'mid', { sheen: 0 });
  pr.bands('near', y + (o.band ?? 200), y + (o.band ?? 200) + 220, 4, 0, { trap: .2 });
  pr.ink(FG.glints(x0, x0 + w, y + 16, y + (o.gl ?? 300), o.n ?? 26, o.seed ?? 3, t, 50), o.glRole || 'sky1', { sheen: 0, reg: 0 });
}

// P01 — A01: İkaros güneşe bakıyor (kapak karesi). Üslup kapısı yakın planı; halkalar yavaşça genişler (sahne kendi zamanıyla)
plan('P01', (ctx, st) => SCENES.yakin(ctx, st.lt + 2, st));

// P02 — A02@güneşe: dev güneş, küçük kanatlı siluet ona doğru yükselir
plan('P02', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 120, 420, 5);
  const s = FG.sunRings(1180, 470, 210, 3); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'acc');
  a1_deniz(pr, 860, st.lt, { band: 120, gl: 200, n: 18 });
  const u = E.io2(clamp(st.lt / Math.max(3, st.d))), x = lerp(420, 760, u), y = lerp(760, 560, u), fl = Math.sin(st.lt * 3.4);
  const J = FG.rig({ x, y, h: 22, f: 1, lean: .9, head: -.8, legN: [-.1, .3], legF: [-.35, .45] });
  kanatliFigur(pr, J, { w: { ang: -1.7 - fl * .55, bend: -.25, span: 22 * 6.4, chord: 22 * 2.3, side: -1, seed: 4 }, light: [1, -.4], litD: 2, farOff: [6, -4], look: { curls: true } });
}));

// P03 — A03: kanat ucu denize değer; suyun altındaki tüyler görünmez, değdiği yerde halka (unutulan uyarı: aşağıda)
plan('P03', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 80, 320, 4);
  const dip = Math.sin(st.lt * 1.1) * 14;
  const wn = FG.wing({ root: [-180, -260], ang: .62, bend: .32, span: 1500, chord: 470, f: 1, seed: 21 });
  litInk(pr, wn.all, 'lit', 'near', 1, -.6, 9); pr.ink(wn.cov, 'mid', { sheen: .1 });
  // deniz: dalgalı üst kenar (kanadın denize giren kısmını örter)
  const yW = 760 + dip, sea = new Path2D(); sea.moveTo(-50, yW);
  for (let x = -50; x <= 1970; x += 20) sea.lineTo(x, yW + Math.sin(x / 90 + st.lt * 1.6) * 9);
  sea.lineTo(1970, 1200); sea.lineTo(-50, 1200); sea.closePath(); pr.ink(sea, 'mid', { sheen: .2 });
  pr.bands('near', 900, 1100, 4, 0, { trap: .2 });
  { const k = clamp((st.t - Wd('A03', 'sırrı')) / 2.5); if (k > 0) { const tp = new Path2D(); a2_tuy(tp, 900 + k * 120, 600 + k * k * 260, 150, 1.2 + k * 1.4, .14); pr.ink(tp, 'near', { sheen: .2 }); } }
  const tip = wn.tip, cx = clamp(tip[0], 200, 1700);
  for (let k = 0; k < 3; k++) { const r = 60 + ((st.lt * 70 + k * 90) % 270), ring = SK.ringPath(cx, yW + 14, r, r + 6); const p2 = new Path2D(); p2.addPath(ring, new DOMMatrix().translate(cx, yW + 14).scale(1, .22).translate(-cx, -(yW + 14))); pr.ink(p2, 'sky1', { sheen: 0, reg: 0 }); }
}));

// P04 — B02: seyahat afişi: Girit, şafak; başlık göğe, künye bilgi bandına basılır
plan('P04', (ctx, st) => {
  SCENES.manzara(ctx, st.lt + 3, st);
  ctx.save(); baseT(ctx); ctx.fillStyle = PAL[palAt(st.t).cur.pal].near; ctx.fillRect(0, 968, W, 112); ctx.restore();
}, { over: (ctx, st, pal) => {
  basYazi(ctx, 'GİRİT', 1460, 190, st.lt, { px: 200, ls: 22, col: pal.near, t0: .4, dur: .5 });
  basYazi(ctx, 'OVİDİUS · DÖNÜŞÜMLER · VIII. KİTAP', 1460, 300, st.lt, { font: FONT.metin(38, 600), ls: 5, col: pal.near, t0: 1.2, dur: .6 });
} });

// P05 — B02@labirent: labirentin planı tepeden, duvar duvar basılır; girişte küçük bir figür
plan('P05', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('lit');
  const lab = FG.labyrinth(960, 560, 1500, 15, .62, 11, .3);
  const p = clamp(st.lt / Math.min(3.2, st.d * .6));
  pr.ink(lab, 'near', { clip: SK.wipeRegion([0, 0, W, H], 'down', p, 4, 40, 6), sheen: .2 });
  const J = FG.rig({ x: 960 - 1500 / 15 * .5, y: 1040, h: 9, f: 1, armN: [.2, 0], armF: [-.1, 0] });
  const fg = FG.figure(J, { beard: true, long: true }); pr.ink(fg.body, 'near');
}));

// P06 — B03: ada, denizin ortasında: "kendisi de bir labirentteydi"
plan('P06', (ctx, st) => baski(ctx, st, { cx: 960 + st.lt * 10, cy: 540 }, pr => {
  pr.sky('sky2', 'sky1', 60, 300, 4);
  gunes(pr, 1500, 330, 46, 2);
  a1_deniz(pr, 420, st.lt, { band: 420, gl: 520, n: 40, seed: 7 });
  // dalga çizgileri: adayı çevreleyen yatay, düzensiz şeritler (hedef tahtası değil)
  const r = rng(5), wv = new Path2D(); for (let i = 0; i < 26; i++) { const y = 460 + r() * 520, x = 200 + r() * 1700, L = 60 + r() * 160; wv.rect(x + Math.sin(st.lt * .7 + i) * 8, y, L, 3 + (y - 420) / 120); } pr.ink(wv, 'sky2', { sheen: 0, reg: 0 });
  pr.ink(FG.ridge(860, 1180, 700, 590, 70, 34, 5), 'far', { sheen: .1 });
  const isl = FG.ridge(680, 1280, 712, 640, 60, 33, 6); pr.ink(isl, 'near');
}));

// P07 — B03@yıllardır: Daidalos'un başı profilden, ufka bakıyor; ufukta uzak kara (yurt)
plan('P07', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 260, 640, 5);
  pr.ink(FG.ridge(1250, 1960, 700, 640, 30, 41, 5), 'far');
  const sea = new Path2D(); sea.rect(-50, 690, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 });
  pr.ink(FG.glints(1100, 1900, 700, 860, 14, 2, st.lt, 40), 'sky1', { sheen: 0, reg: 0 });
  const J = FG.rig({ x: 640, y: 1260, h: 220, f: 1, lean: .06, head: .02 + Math.sin(st.lt * .6) * .02, armN: [.05, 0], armF: [.05, 0] });
  kanatliFigur(pr, J, { light: [1, -.5], litD: 10, look: { beard: true, long: true, chest: true, face: true } });
}));

// P08 — B04: Daidalos kayalıkta kolunu göğe kaldırır; kamera göğe kayar (boş gök, martılar)
plan('P08', (ctx, st) => {
  const u = E.io2(clamp((st.t - Wd('B04', 'gök')) / 3.5));
  const cam = { cx: 960, cy: lerp(540, 300, u) };
  baski(ctx, st, cam, pr => {
    pr.sky('sky2', 'sky1', -250, 280, 5);
    gunes(pr, 1500, 120, 60, 3);
    const sea = new Path2D(); sea.rect(-50, 720, 2020, 600); pr.ink(sea, 'mid', { sheen: 0 });
    pr.ink(FG.glints(100, 1900, 740, 900, 20, 4, st.lt, 40), 'sky1', { sheen: 0, reg: 0 });
    pr.ink(FG.cliff(-60, 880, 760, 1300, 1, 9), 'near');
    const raise = E.out3(clamp((st.t - Wd('B04', 'gök')) / .8));
    const J = FG.rig({ x: 700, y: 760 - 50 * 3.75, h: 50, f: 1, lean: -.04, head: -.25 - raise * .35, armN: [lerp(.3, 2.75, raise), lerp(-.3, .1, raise)], armF: [-.1, -.2] });
    kanatliFigur(pr, J, { light: [1, -.4], litD: 4, look: { beard: true, long: true, face: true } });
    [[1000, 220, 18, 0], [1100, 160, 13, 1.7], [1240, 250, 11, 3], [820, 120, 9, 2]].forEach(([x, y, s, ph]) => pr.ink(FG.gull(x + st.lt * 14, y + Math.sin(st.lt * 1.3 + ph) * 6, s, st.lt * 5 + ph), 'mid', { sheen: 0 }));
  });
});
