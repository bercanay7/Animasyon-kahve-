// act3: III · 1908 (D01–D04). Yardımcılar a3_ önekli; act1.js'teki a1_ yardımcılarını da kullanır.
'use strict';

// ═══════════ D01 · Garnizonlar yanar; kuşak şeridi: aynı sıralardan geçmiş genç subaylar ═══════════
const A3_GARRISON = [[28.97, 41.01], [22.94, 40.64], [21.33, 41.03], [21.43, 42.0], [26.56, 41.68], [27.14, 38.42], [20.85, 39.66], [19.5, 42.07], [32.49, 37.87], [37.02, 39.75], [39.5, 39.75], [41.27, 39.9], [37.16, 36.2], [36.3, 33.51], [35.22, 31.78], [43.13, 36.34], [44.4, 33.33], [13.19, 32.89]];
// genç subay kimlikleri (anonim; kuşak şeridi)
const A3_OFF = [
  { mus: 'mk', jaw: 1.0, brow: .1, hair: 'ink', seed: 61 }, { mus: 'thin', jaw: 1.06, brow: -.05, hair: 'ink', seed: 62 }, { mus: 'mk', jaw: .96, brow: .25, hair: 'sepia', seed: 63 },
  { mus: 'pala', jaw: 1.08, brow: 0, hair: 'ink', seed: 64 }, { mus: 'thin', jaw: 1.0, brow: .15, hair: 'ink', seed: 65 }, { mus: 'mk', jaw: 1.04, brow: .05, hair: 'sepia', seed: 66 },
];
function a3_strip(ctx, t, y0, look, o = {}) {
  // kuşak şeridi: altın bant üstünde yan yana büstler (fes, is setre)
  const band = a1_rect(-60, y0, W + 60, H + 60);
  knock(ctx, band); plate(ctx, 'gold', band, { a: .5 });
  ctx.save(); ctx.clip(band);
  A3_OFF.forEach((id, i) => {
    const x = 190 + i * 308, lk = look(i);
    a1_fig(ctx, t + i * .37, { x, y: y0 + 190, s: 1.16, dir: i % 2 ? -1 : -1, who: 'anon', id, gear: 'fes', coat: 'setre', col: 'ink', age: 24 + (i * 3) % 5, lookAt: lk, len: 420, seed: id.seed, w: .95 });
  });
  ctx.restore();
  inkStroke(ctx, PL([[-60, y0], [W + 60, y0]], false), 4);
}
shot(S('D01'), (ctx, st) => {
  setReg(301);
  paperBG(ctx);
  const t = st.t, lt = st.lt;
  const Ty = a1_W('D01', 'yüzlerce'), Ts = a1_W('D01', 'subay'), Ta = a1_W('D01', 'sonuca'), Td = a1_W('D01', 'değişim'), Tc = a1_W('D01', 'çöküş');
  const up = E.io3(clamp((t - Ts + .35) / .8));
  const c = { x: kf(t, [[S('D01'), 960], [Ts, 900]]), y: kf(t, [[S('D01'), 540], [Ts - .3, 520], [Ts + .6, 610]]), z: kf(t, [[S('D01'), 1.0], [Ts - .3, 1.05], [Ts + .6, 1.06]]) };
  ctx.save(); cam(ctx, c, 1);
  a1_drawMap1900(ctx, { topKey: 'a3-map-top', top: { sea: 'teal', seaA: .38 } });
  // garnizonlar birer birer yanar (düz altın halkalar + kırmızı merkez)
  A3_GARRISON.forEach(([lo, la], i) => {
    const ti = Ty - .3 + i * .09, k = a1_pop(t, ti, .16); if (k <= 0) return;
    const [x, y] = a1_p(lo, la);
    for (const [r, a] of [[30, .35], [19, .6]]) plate(ctx, 'gold', a1_ell(x, y, r * k, r * k), { a });
    const d = a1_ell(x, y, 7.5 * k, 7.5 * k); knock(ctx, d); plate(ctx, 'red', d); inkStroke(ctx, d, 2.2);
  });
  ctx.restore();
  // kuşak şeridi: "subay" sözünde alttan yükselir; "aynı sonuca" sözünde bakışlar aynı noktada buluşur
  if (up > 0) {
    const y0 = lerp(H + 20, 600, up), conv = ramp(t, Ta - .3, Ta + .5, E.io2);
    a3_strip(ctx, t, y0, i => { const x = 190 + i * 308; return [lerp(x + (i % 2 ? 380 : -380), -300, conv), lerp(y0 + 120, y0 + 60, conv)]; });
  }
  a1_rubber(ctx, 'DEĞİŞİM', 640, 300, t - Td, -.08, 74, { plate: 'teal' });
  a1_rubber(ctx, 'ÇÖKÜŞ', 1280, 330, t - Tc, .07, 74, { plate: 'ink' });
  chapterCard(ctx, 'III', '1908', 'MEŞRUTİYET', lt - .25, 3.6, { y: 60 });
}, { tr: { type: 'press', dur: .8 } });

// ═══════════ D02a · Makedonya dağları: subaylar dağa çıkar ═══════════
// asker silueti (damga): fes, sırtta tüfek; ph adım evresi
function a3_soldier(g, x, y, s, ph = 0, dir = 1) {
  g.save(); g.translate(x, y); g.scale(s * dir, s);
  const b = new Path2D(), st = ph ? 4 : -4;
  b.ellipse(1, -90, 5.4, 6.4, 0, 0, TAU);
  b.moveTo(-9, -82); b.lineTo(10, -82); b.lineTo(13, -46); b.lineTo(10, -40); b.lineTo(7 + st, 0); b.lineTo(2 + st, 0); b.lineTo(1, -36); b.lineTo(-1, -36); b.lineTo(-3 - st, 0); b.lineTo(-8 - st, 0); b.lineTo(-9, -40); b.lineTo(-11, -46); b.closePath();
  inkFill(g, b);
  inkStroke(g, PL([[-12, -40], [10, -112]], false), 2.6); inkStroke(g, PL([[10, -112], [12, -122]], false), 1);
  const f = PL([[-4, -95], [6, -95], [5.2, -104], [-3.2, -104]]); knock(g, f); plate(g, 'red', f); inkStroke(g, f, .8);
  cut(g, PL([[-6, -74], [8, -60]], false), .8, { a: .4 });
  g.restore();
}
const A3_PATH = [[180, 1060], [520, 930], [380, 840], [760, 740], [640, 660], [1000, 590], [900, 530], [1260, 470], [1520, 420]];
function a3_pathAt(u) {
  let tot = 0; const L = []; for (let i = 0; i < A3_PATH.length - 1; i++) { const l = Math.hypot(A3_PATH[i + 1][0] - A3_PATH[i][0], A3_PATH[i + 1][1] - A3_PATH[i][1]); L.push(l); tot += l; }
  let d = clamp(u) * tot, i = 0; while (i < L.length - 1 && d > L[i]) { d -= L[i]; i++; }
  const f = d / L[i], a = A3_PATH[i], b = A3_PATH[i + 1];
  return [lerp(a[0], b[0], f), lerp(a[1], b[1], f), Math.sign(b[0] - a[0]) || 1];
}
shot(S('D02'), (ctx, st) => {
  setReg(302);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const c = { x: kf(t, [[S('D02'), 930], [S('D02') + 4.4, 1000]]), y: kf(t, [[S('D02'), 570], [S('D02') + 4.4, 520]]), z: kf(t, [[S('D02'), 1.04], [S('D02') + 4.4, 1.08]]) };
  // gök ve uzak sıralar (durağan): şafak altını, turkuaz uzak dağlar
  const sky = a1_cacheM('a3-d02-sky', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R);
    plate(g, 'gold', a1_rect(-220, -220, W + 220, 260), { a: .55 }); plate(g, 'gold', a1_rect(-220, 260, W + 220, 380), { a: .3 });
    radialHT(g, 'gold', 1500, 430, 120, 900, .05, .4, { cell: 12, ang: 15, box: [-220, -220, W + 220, 420] });
    const far = SP([[-220, 470], [100, 380], [380, 430], [700, 330], [1000, 410], [1320, 300], [1640, 380], [1900, 320], [2140, 400], [2140, 700], [-220, 700]], true, .7);
    plate(g, 'teal', far, { a: .45 }); inkStroke(g, far, 2, { a: .6 });
    for (const [sp, L] of [[[[640, 360], [700, 332], [760, 360]], 12], [[[1260, 330], [1320, 302], [1390, 336]], 14]]) ridge(g, sp, L, px => px * .8, L);
  });
  ctx.save(); cam(ctx, c, .4); a1_imgM(ctx, sky); ctx.restore();
  // yakın dağ: is tarama, kâğıt patika
  const near = a1_cacheM('a3-d02-near', g => {
    const m = SP([[-220, 640], [200, 560], [560, 600], [900, 480], [1200, 470], [1500, 400], [1800, 470], [2140, 520], [2140, 1300], [-220, 1300]], true, .7);
    knock(g, m); plate(g, 'teal', m, { a: .55 }); plate(g, 'teal', m, { a: .35 });
    g.save(); g.clip(m); const r = rng(8); for (let i = 0; i < 520; i++) { const x = -200 + r() * 2340, y = 420 + r() * 860, L = 8 + r() * 18; inkStroke(g, PL([[x, y], [x - L * .5, y + L]], false), 1.4, { a: .45 }); } g.restore();
    inkStroke(g, m, 3);
    const path = SP(A3_PATH, false, .8); inkStroke(g, path, 30, { col: P.paper }); inkStroke(g, path, 30, { a: .12 }); g.save(); g.setLineDash([3, 9]); inkStroke(g, path, 2, { a: .5 }); g.restore();
    for (const [x, y, s] of [[300, 700, 1], [1700, 560, .8], [120, 900, 1.3], [1100, 640, .9]]) { const tr = new Path2D(); tr.moveTo(x, y); tr.lineTo(x - 26 * s, y + 70 * s); tr.lineTo(x + 26 * s, y + 70 * s); tr.closePath(); inkFill(g, tr); inkStroke(g, PL([[x, y + 70 * s], [x, y + 84 * s]], false), 4 * s); }
  });
  ctx.save(); cam(ctx, c, 1); a1_imgM(ctx, near);
  // subay kolu: patika boyunca tırmanır (pozlar 6 fps)
  const ph = Math.floor(t * 6) % 2, dt = t - S('D02');
  for (let i = 0; i < 9; i++) {
    const u = .12 + dt * .07 - i * .05; if (u < 0 || u > 1) continue;
    const [x, y, d] = a3_pathAt(u), s = lerp(2.5, 1.05, u);
    a3_soldier(ctx, x, y + 4, s, (ph + i) % 2, d);
  }
  ctx.restore();
  stamp(ctx, 'MAKEDONYA · TEMMUZ 1908', 90, 110, t - S('D02') - .1, 4.2, { size: 34 });
}, { tr: { type: 'press', dur: .6 } });

// ═══════════ D02b · 1908 "Hürriyet" kartpostalı (belge) ve sevinen kalabalık ═══════════
function a3_postcard(g) {
  const w = 1000, h = 640, x0 = -w / 2, y0 = -h / 2;
  plate(g, 'ink', a1_rect(x0 + 14, y0 + 18, w / 2 + 14, h / 2 + 18), { a: .4 });
  const card = PL(rough([[x0, y0], [-x0, y0], [-x0, -y0], [x0, -y0]], 1.4, 13)); knock(g, card);
  // güneş ışınları (altın) ve doğan güneş
  g.save(); g.clip(a1_rect(x0 + 40, y0 + 40, -x0 - 40, -y0 - 40));
  const cx = 0, cy = 170;
  for (let k = 0; k < 22; k++) { const a0 = PI + k / 22 * PI, a1 = a0 + PI / 44; if (k % 2) continue; plate(g, 'gold', PL([[cx, cy], [cx + Math.cos(a0) * 900, cy + Math.sin(a0) * 900], [cx + Math.cos(a1) * 900, cy + Math.sin(a1) * 900]]), { a: .75 }); }
  const sun = new Path2D(); sun.arc(cx, cy, 150, PI, 0); sun.closePath(); knock(g, sun); plate(g, 'gold', sun, { n: 2 }); inkStroke(g, sun, 3);
  for (let k = 0; k < 7; k++) cut(g, PL([[-140 + k * 6, cy - 30 - k * 16], [140 - k * 6, cy - 30 - k * 16]], false), 1.6, { a: .45 });
  // çapraz bayraklar
  for (const sd of [-1, 1]) {
    g.save(); g.translate(cx + sd * 30, cy + 40); g.rotate(sd * .62);
    inkStroke(g, PL([[0, 0], [0, -420]], false), 6); inkFill(g, a1_ell(0, -424, 8, 8));
    const fl = SP([[0, -410], [sd * 120, -400], [sd * 230, -414], [sd * 232, -300], [sd * 120, -286], [0, -296]], true, .6);
    knock(g, fl); plate(g, 'red', fl); inkStroke(g, fl, 2.6);
    const cr = new Path2D(); cr.arc(sd * 104, -352, 30, 0, TAU); cr.arc(sd * 104 + sd * 9, -356, 25, 0, TAU, true); g.save(); g.fillStyle = P.paper; g.fill(cr, 'evenodd'); g.restore();
    const sp = []; for (let i = 0; i < 10; i++) { const a = -PI / 2 + i * TAU / 10, r = i % 2 ? 6 : 14; sp.push([sd * 150 + Math.cos(a) * r, -356 + Math.sin(a) * r]); } knock(g, PL(sp));
    g.restore();
  }
  // defne dalları
  for (const sd of [-1, 1]) for (let i = 0; i < 9; i++) { const a = PI / 2 + sd * (.3 + i * .14), r = 210, x = cx + Math.cos(a) * r * sd * -1, y = cy - 40 + Math.sin(a) * r * .55 - i * 14; const lf = a1_ell(sd * (220 + i * 9), cy + 20 - i * 26, 9, 20, sd * (.5 + i * .05)); knock(g, lf); plate(g, 'teal', lf, { a: .9 }); inkStroke(g, lf, 1.6); }
  g.restore();
  // turkuaz çerçeve, köşe süsleri, üst kurdele, alt kartuşlar
  plate(g, 'teal', a1_ring(x0 + 14, y0 + 14, -x0 - 14, -y0 - 14, 22));
  inkStroke(g, a1_rect(x0 + 14, y0 + 14, -x0 - 14, -y0 - 14), 2.2); inkStroke(g, a1_rect(x0 + 36, y0 + 36, -x0 - 36, -y0 - 36), 1.6);
  for (const [px, py] of [[x0 + 25, y0 + 25], [-x0 - 25, y0 + 25], [x0 + 25, -y0 - 25], [-x0 - 25, -y0 - 25]]) { const c = a1_ell(px, py, 15, 15); knock(g, c); plate(g, 'gold', c, { n: 2 }); inkStroke(g, c, 2); }
  const rib = SP([[-330, y0 + 70], [-170, y0 + 54], [0, y0 + 50], [170, y0 + 54], [330, y0 + 70], [326, y0 + 128], [170, y0 + 112], [0, y0 + 108], [-170, y0 + 112], [-326, y0 + 128]], true, .7);
  for (const sd of [-1, 1]) { const tail = PL([[sd * 320, y0 + 84], [sd * 400, y0 + 78], [sd * 380, y0 + 106], [sd * 404, y0 + 134], [sd * 322, y0 + 124]]); knock(g, tail); plate(g, 'teal', tail, { n: 2 }); inkStroke(g, tail, 2.2); }
  knock(g, rib); plate(g, 'teal', rib); inkStroke(g, rib, 2.6);
  scriptLine(g, 240, y0 + 98, 480, 18, 1908, { w: 3.4, col: P.paper });
  for (let i = 0; i < 4; i++) { const bx = -390 + i * 200, b = a1_rect(bx, 236, bx + 180, 280); knock(g, b); plate(g, 'gold', b, { a: .45 }); inkStroke(g, b, 2); scriptLine(g, bx + 166, 266, 150, 10, 1910 + i, { w: 2.4 }); }
  inkStroke(g, card, 3);
}
// sevinen kalabalık: damga siluetler, fesler ve kalkan kollar (2 poz), küçük flamalar
function a3_crowd(ctx, t, y0, n = 18, seed = 7) {
  const r = rng(seed), ph = Math.floor(t * 6) % 2;
  for (let row = 0; row < 2; row++) for (let i = 0; i < n; i++) {
    const x = -40 + i * (W + 80) / (n - 1) + (row ? 50 : 0) + (r() - .5) * 30, s = row ? 1.25 : 1.0, y = y0 + (row ? 120 : 0) + (r() - .5) * 10;
    const up = (i + row + ph) % 2, kind = r();
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    const b = new Path2D(); b.ellipse(0, -60, 18, 21, 0, 0, TAU); b.moveTo(-42, 40); b.quadraticCurveTo(-40, -30, 0, -34); b.quadraticCurveTo(40, -30, 42, 40); b.closePath();
    inkFill(ctx, b);
    // kol
    const hand = up ? [26 + kind * 10, -128] : [34, -96];
    inkStroke(ctx, SP([[24, -22], [34, -60], hand], false), 13); inkFill(ctx, a1_ell(hand[0], hand[1], 8, 9));
    if (kind < .55) { const f = PL([[-15, -76], [15, -76], [12, -104], [-12, -104]]); knock(ctx, f); plate(ctx, 'red', f); inkStroke(ctx, f, 2); }
    else if (kind < .75) { inkFill(ctx, PL([[-24, -74], [24, -74], [24, -78], [14, -78], [14, -104], [-14, -104], [-14, -78], [-24, -78]])); }
    if (kind > .82) { inkStroke(ctx, PL([[hand[0], hand[1]], [hand[0], hand[1] - 70]], false), 3); const pn = PL([[hand[0], hand[1] - 70], [hand[0] + 50 + up * 6, hand[1] - 58], [hand[0], hand[1] - 46]]); knock(ctx, pn); plate(ctx, 'red', pn); inkStroke(ctx, pn, 1.8); }
    ctx.restore();
  }
}
shot(a1_W('D02', 'sultan'), (ctx, st) => {
  setReg(303);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const Tm = a1_W('D02', 'meşrutiyet');
  const c = { x: 960, y: kf(t, [[st.t - st.lt, 540], [Tm + 1.5, 510]]), z: kf(t, [[st.t - st.lt, 1.0], [Tm + 1.5, 1.06]]) };
  ctx.save(); cam(ctx, c, .5);
  a1_imgM(ctx, a1_cacheM('a3-d02b-bg', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R); plate(g, 'gold', R, { a: .32 });
    g.save(); g.clip(R); const hp = new Path2D(); for (let x = -1400; x < 2400; x += 18) { hp.moveTo(x, -220); hp.lineTo(x + 1400, 1300); } inkStroke(g, hp, 1.2, { a: .14 }); g.restore();
  }));
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  ctx.save(); ctx.translate(960, 440 + noise1(tf * .5, 2) * 3); ctx.rotate(-.025);
  ctx.translate(-W / 2, -H / 2); a1_imgM(ctx, a1_cacheM('a3-postcard', g => { g.translate(W / 2, H / 2); a3_postcard(g); }, 40));
  ctx.restore();
  ctx.restore();
  // posta damgası: "Meşrutiyet" sözünde karta basılır
  const pk = a1_pop(t, Tm, .14);
  if (pk > 0) {
    ctx.save(); ctx.translate(1340, 200); ctx.rotate(-.2); ctx.scale(pk, pk);
    inkStroke(ctx, a1_ell(0, 0, 66, 66), 4, { a: .85 }); inkStroke(ctx, a1_ell(0, 0, 50, 50), 1.8, { a: .8 }); scriptLine(ctx, 34, 6, 68, 9, 77, { w: 2.4 });
    for (let k = 0; k < 4; k++) inkStroke(ctx, SP([[80, -30 + k * 20], [130, -38 + k * 20], [180, -30 + k * 20], [230, -38 + k * 20]], false), 3, { a: .8 });
    ctx.restore();
  }
  // kalabalık sevinir (ön planda)
  a3_crowd(ctx, t, 960);
  stamp(ctx, 'MEŞRUTİYET · 24 TEMMUZ 1908', 90, 110, t - Tm, 9, { size: 34 });
}, { tr: { type: 'cut' } });
