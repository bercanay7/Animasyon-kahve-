// Perde 4 (P27–P32): İkaros, neredesin? Gün batımı paleti. Kırmızı çizgi: çarpma ve beden yok, haç pozu yok.
'use strict';
function a4_tuyler(pr, t, n, x0, y0, spread, fall, seed, role = 'near', size = 60) {
  const p = new Path2D(), r = rng(seed);
  for (let i = 0; i < n; i++) { const ph = r() * 6.28, sp = .4 + r() * .8, x = x0 + (r() - .5) * spread + Math.sin(t * sp + ph) * 60, y = y0 + ((t * fall * (.5 + r()) + r() * 400) % 700), a = t * sp * 1.5 + ph; a2_tuy(p, x, y, size * (.6 + r() * .6), a, .14); }
  pr.ink(p, role, { sheen: .2 });
}
// P27 — E01: kanat kökünde mum damlaları akar, tüyler gevşer
plan('P27', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 80, 360, 5);
  const s = FG.sunRings(1500, 300, 160, 3); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'acc');
  const melt = clamp(st.lt / Math.max(2, st.d));
  const wn = FG.wing({ root: [-140, 640], ang: -.32, bend: .22, span: 1500, chord: 470, f: 1, seed: 41, ruin: melt * .35 });
  litInk(pr, wn.all, 'lit', 'near', 1, -.6, 6); pr.ink(wn.cov, 'mid', { sheen: .1 });
  const dr = new Path2D(), r = rng(3);
  for (let i = 0; i < 9; i++) { const u = .15 + i * .085, q = [lerp(-140, wn.wrist[0], u * 1.6), lerp(640, wn.wrist[1], u * 1.6)], ph = r(); const k = ((st.lt * .6 + ph) % 1); FG.ellipseInto(dr, q[0] + 40, q[1] + 60 + k * 260, 9 + 4 * (1 - k), 14 + 10 * k, 0, 14); FG.ellipseInto(dr, q[0] + 40, q[1] + 50, 16, 10, 0, 12); }
  pr.ink(dr, 'acc', { sheen: .5 });
  a4_tuyler(pr, st.lt, Math.round(melt * 6), 1100, 300, 600, 70, 9, 'near', 80);
}));

// P28 — E02: çıplak kollar çırpıyor, tüyler savruluyor; dev güneş (başın arkasında değil)
plan('P28', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 120, 460, 5);
  const s = FG.sunRings(1450, 280, 190, 3); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'acc');
  a3_ucan(pr, st.lt * 2.2, 700, 640, 64, .4, false, { rise: -.15, ruin: .78 });
  a4_tuyler(pr, st.lt, 10, 700, 380, 700, 120, 12, 'near', 70);
}));

// P29 — E03: uzaktan: tüyler sarmal iner; denizde küçük bir halka kapanır (beden yok)
plan('P29', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 60, 420, 6); gunes(pr, 1450, 520, 90, 2);
  const sea = new Path2D(); sea.rect(-50, 620, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 }); pr.bands('near', 860, 1080, 3, 0, { trap: .2 });
  pr.ink(FG.glints(900, 1900, 630, 800, 20, 5, st.lt, 50), 'acc', { sheen: 0, reg: 0 });
  const tS = Wd('E03', 'mavi'), k = clamp((st.t - tS) / 1.6);
  const p = new Path2D(), r = rng(21); for (let i = 0; i < 14; i++) { const ph = r() * 6.28, y = 120 + ((st.lt * 60 + r() * 400) % 460), x = 720 + Math.sin(st.lt * 1.2 + ph) * (40 + (y - 120) * .25); a2_tuy(p, x, y, 26 + r() * 14, st.lt * 2 + ph, .16); } pr.ink(p, 'near', { sheen: .2 });
  if (k > 0 && k < 1) { const rr = 20 + k * 160, ring = SK.ringPath(0, 0, rr, rr + 6), q = new Path2D(); q.addPath(ring, new DOMMatrix().translate(740, 640).scale(1, .2)); pr.ink(q, 'sky1', { sheen: 0, reg: 0 }); }
}));

// P30 — E04: boş gökte Daidalos tek başına döner, aşağıya bakar
plan('P30', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 100, 500, 6); gunes(pr, 1500, 640, 120, 3);
  const sea = new Path2D(); sea.rect(-50, 820, 2020, 300); pr.ink(sea, 'mid', { sheen: 0 });
  const a = st.lt * .5, x = 860 + Math.cos(a) * 260, y = 440 + Math.sin(a) * 60, f = Math.sin(a) > 0 ? -1 : 1;
  a3_ucan(pr, st.lt, x, y, 58, 0, true, { f, rise: -.35 });
}));

// P31 — E05: dalgaların üstünde tüyler
plan('P31', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('mid');
  const wv = new Path2D(); for (let r = 0; r < 6; r++) { const y0 = 140 + r * 160; wv.moveTo(-50, y0 + 26); for (let x = -50; x <= 1970; x += 12) wv.lineTo(x, y0 + Math.sin(x / 140 + st.lt * 1.1 + r * 1.7) * 18); for (let x = 1970; x >= -50; x -= 12) wv.lineTo(x, y0 + 26 + Math.sin(x / 140 + st.lt * 1.1 + r * 1.7) * 18); wv.closePath(); } pr.ink(wv, 'near', { sheen: 0 });
  const p = new Path2D(), r = rng(8); for (let i = 0; i < 9; i++) { const x = 200 + r() * 1500, y = 200 + r() * 700, b = Math.sin(st.lt * 1.1 + x / 140) * 18; a2_tuy(p, x, y + b, 120 + r() * 80, r() * 6.28, .14); }
  litInk(pr, p, 'lit', 'sky1', 1, -1, 4);
}));

// P32 — E05@toprağa: afiş: adanın silueti alacakaranlıkta; başlık basılır (mezar, kasaba yok)
plan('P32', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 120, 560, 6); gunes(pr, 1280, 640, 110, 3);
  const sea = new Path2D(); sea.rect(-50, 680, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 }); pr.ink(FG.glints(1000, 1600, 690, 860, 18, 3, st.lt, 50), 'acc', { sheen: 0, reg: 0 });
  pr.ink(FG.ridge(200, 1100, 700, 520, 120, 81, 6), 'near'); pr.ink(FG.ridge(820, 1350, 700, 610, 60, 82, 5), 'far');
  bant(pr, 968, 1080, 'near');
}), { over: (ctx, st, pal) => {
  basYazi(ctx, 'İKARYA', W / 2, 200, st.t - Wd('E05', 'ikarya'), { px: 200, ls: 22, col: pal.near, dur: .5 });
  basYazi(ctx, 'ADI DENİZDE VE TOPRAKTA KALAN ÇOCUK', W / 2, 1024, st.t - Wd('E05', 'ikarya') - .6, { font: FONT.metin(40, 600), ls: 6, col: pal.paper, dur: .6 });
} });
