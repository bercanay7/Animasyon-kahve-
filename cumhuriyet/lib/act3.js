// act3: III · 1908 (D01–D04). Yardımcılar a3_ önekli; act1.js'teki a1_ yardımcılarını da kullanır.
'use strict';

// ═══════════ D01 · Garnizonlar yanar; kuşak şeridi: aynı sıralardan geçmiş genç subaylar ═══════════
const A3_GARRISON = [[28.97, 41.01], [22.94, 40.64], [21.33, 41.03], [21.43, 42.0], [26.56, 41.68], [27.14, 38.42], [20.85, 39.66], [19.5, 42.07], [32.49, 37.87], [37.02, 39.75], [39.5, 39.75], [41.27, 39.9], [37.16, 36.2], [36.3, 33.51], [35.22, 31.78], [43.13, 36.34], [44.4, 33.33], [13.19, 32.89]];
// genç subay kimlikleri (anonim; kuşak şeridi)
const A3_OFF = [
  { mus: 'mk', jaw: 1.0, brow: .1, hair: 'ink', seed: 61, tilt: -.04 }, { mus: 'thin', jaw: 1.06, brow: -.05, hair: 'ink', seed: 62, tilt: .03, WD: 1.14 }, { mus: 'gur', jaw: .96, brow: .25, hair: 'sepia', seed: 63, tilt: -.02 },
  { mus: 'pala', jaw: 1.1, brow: 0, hair: 'ink', seed: 64, tilt: .04, WD: 1.12 }, { mus: 'faint', jaw: .98, brow: .18, hair: 'ink', seed: 65, tilt: -.03, WD: 1.02 }, { mus: 'mk', jaw: 1.04, brow: .05, hair: 'sepia', seed: 66, tilt: .02, HY: 1.04 },
];
function a3_strip(ctx, t, y0, look, o = {}) {
  // kuşak şeridi: altın bant üstünde yan yana büstler (fes, is setre)
  const band = a1_rect(-60, y0, W + 60, H + 60);
  knock(ctx, band); plate(ctx, 'gold', band, { a: .5 });
  ctx.save(); ctx.clip(band);
  A3_OFF.forEach((id, i) => {
    const x = 190 + i * 308, lv = look(i), lk = Array.isArray(lv[0]) ? lv[0] : lv, tl = Array.isArray(lv[0]) ? lv[1] : 0;
    a1_fig(ctx, t + i * .37, { x, y: y0 + 190, s: 1.16, dir: -1, who: 'anon', id, gear: 'fes', coat: 'setre', col: 'ink', age: 24 + (i * 3) % 5, lookAt: lk, len: 420, seed: id.seed, w: .92 + (i % 3) * .05, tilt: (id.tilt || 0) + tl, idle: 1.5 });
  });
  ctx.restore();
  inkStroke(ctx, PL([[-60, y0], [W + 60, y0]], false), 4);
}
shot(S('D01'), (ctx, st) => {
  setReg(301);
  paperBG(ctx);
  const t = st.t, lt = st.lt;
  const Ty = a1_W('D01', 'yüzlerce'), Ts = a1_W('D01', 'subay'), Ta = a1_W('D01', 'sonuca'), Td = a1_W('D01', 'değişim'), Tc = a1_W('D01', 'çöküş');
  const Tst = Math.max(Ts - .35, S('D01') + 3.55), up = E.io3(clamp((t - Tst) / .8));
  const tE = st.t - st.lt + st.d, c = { x: kf(t, [[st.t - st.lt, 960], [Tst, 900, E.out2], [tE, 880]]), y: kf(t, [[st.t - st.lt, 540], [Tst, 520, E.out2], [Tst + .9, 610], [tE, 622, E.lin]]), z: kf(t, [[st.t - st.lt, 1.0], [Tst, 1.05, E.out2], [Tst + .9, 1.06], [tE, 1.075, E.lin]]) };
  ctx.save(); cam(ctx, c, 1);
  a1_drawMap1900(ctx, { topKey: 'a3-map-top', top: { sea: 'teal', seaA: .38 } });
  // garnizonlar birer birer yanar (düz altın halkalar + kırmızı merkez)
  A3_GARRISON.forEach(([lo, la], i) => {
    const ti = S('D01') + .35 + i * (Ty + .6 - S('D01') - .35) / A3_GARRISON.length, k = a1_pop(t, ti, .16) * (t > ti + .2 ? 1 + .08 * hash(Math.floor(t * 15) + i * 7) : 1); if (k <= 0) return;
    const [x, y] = a1_p(lo, la);
    for (const [r, a] of [[30, .35], [19, .6]]) { plate(ctx, 'gold', a1_ell(x, y, r * k, r * k), { a, flat: true }); inkStroke(ctx, a1_ell(x, y, r * k, r * k), 1.4, { a: .8 }); }
    const d = a1_ell(x, y, 7.5 * k, 7.5 * k); knock(ctx, d); plate(ctx, 'red', d); inkStroke(ctx, d, 2.2);
  });
  ctx.restore();
  // kuşak şeridi: "subay" sözünde alttan yükselir; "aynı sonuca" sözünde bakışlar aynı noktada buluşur
  if (up > 0) {
    const y0 = lerp(H + 20, 600, up), c0 = Math.max(Ta - .1, Tst + .8), tq = Math.floor(t * 15) / 15;
    a3_strip(ctx, t, y0, i => {
      const x = 190 + i * 308, ti = c0 + i * .14, on = tq >= ti, e = ramp(t, ti, ti + .3, E.out2);
      return [on ? [lerp(x, 860, .35), y0 - 420] : [x + (i % 2 ? 380 : -380), y0 + 120], -.06 * e];
    });
  }
  // "ya değişim, ya çöküş": Selanik'ten çatallanan çizgiler, şerit kenarında iki izleyici kutusu
  if (!NOTEXT) {
    const [px, py] = a1_p(22.94, 40.64), sx = W / 2 + (px - c.x) * c.z, sy = H / 2 + (py - c.y) * c.z;
    for (const [s_, bx, T] of [['DEĞİŞİM', 470, Td], ['ÇÖKÜŞ', 1450, Tc]]) {
      const q = clamp((t - T + .15) / .3); if (q <= 0) continue;
      const fx = sx, fy = sy + 60, ex = lerp(fx, bx, E.out2(q)), ey = lerp(fy, 556, E.out2(q));
      inkStroke(ctx, PL([[sx, sy], [fx, fy], [ex, ey]], false), 2.6);
      if (q >= 1) { ctx.save(); ctx.font = FONT.mono(48); ctx.letterSpacing = '4px'; const w = ctx.measureText(s_).width; ctx.restore(); stamp(ctx, s_, bx - w / 2, 616, t - T - .15, 9, { size: 48 }); }
    }
    if (t > Td - .15) { const d = a1_ell(sx, sy, 7, 7); knock(ctx, d); inkFill(ctx, a1_ell(sx, sy, 4.5, 4.5)); }
  }
  chapterCard(ctx, 'III', 'MEŞRUTİYET', '1908 · CUMHURİYET\u2019E 15 YIL', lt - .25, Tst - S('D01') + .3);
}, { tr: { type: 'press', dur: .8 } });

// ═══════════ D02a · Makedonya dağları: subaylar dağa çıkar ═══════════
// asker silueti (damga): fes, sırtta tüfek; ph adım evresi
function a3_soldier(g, x, y, s, ph = 0, dir = 1, cap = 'fes') {
  g.save(); g.translate(x, y); g.scale(s * dir, s);
  const b = new Path2D(), st = ph ? 4 : -4;
  b.ellipse(1, -90, 5.4, 6.4, 0, 0, TAU);
  b.moveTo(-9, -82); b.lineTo(10, -82); b.lineTo(13, -46); b.lineTo(10, -40); b.lineTo(7 + st, 0); b.lineTo(2 + st, 0); b.lineTo(1, -36); b.lineTo(-1, -36); b.lineTo(-3 - st, 0); b.lineTo(-8 - st, 0); b.lineTo(-9, -40); b.lineTo(-11, -46); b.closePath();
  inkFill(g, b);
  inkStroke(g, PL([[-12, -40], [10, -112]], false), 2.6); inkStroke(g, PL([[10, -112], [12, -122]], false), 1);
  if (cap === 'kalpak') { inkFill(g, PL([[-5.5, -93], [7.5, -93], [8.5, -107], [-6.5, -107]])); cut(g, PL([[-4.5, -105], [7, -105]], false), .9, { a: .55 }); } // subay: kalpak (kesik koni)
  else { const m = (px, py) => [x + px * s * dir, y + py * s]; g.restore(); const f = PL([m(-4, -95), m(6, -95), m(5.2, -104), m(-3.2, -104)]); knock(g, f); plate(g, 'red', f); inkStroke(g, f, .8); g.save(); g.translate(x, y); g.scale(s * dir, s); } // er: fes
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
  const Tsb = a1_W('D02', 'subaylar'), Tdg = a1_W('D02', 'dağa');
  const c = { x: kf(t, [[S('D02'), 930], [Tsb, 960], [S('D02') + 4.4, 1010]]), y: kf(t, [[S('D02'), 570], [Tsb, 560], [S('D02') + 4.4, 510]]), z: kf(t, [[S('D02'), 1.02], [Tsb - .2, 1.03], [Tsb + .6, 1.07], [S('D02') + 4.4, 1.08]]) };
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
  // kol boyunca aralık: yol üstünde geriye doğru, ekranda öndekilerden en az 90 px uzak konum
  const placed = []; let u = Math.min(.2 + dt * .085, 1);
  const gap = (a, b) => { const sa = lerp(2.5, 1.05, a[3]), sb = lerp(2.5, 1.05, b[3]); return Math.max(70, 26 * (sa + sb)); };
  for (let i = 0; i < 7 && u > 0; i++) {
    let p = [...a3_pathAt(u), u];
    if (i) { u -= .05; p = [...a3_pathAt(u), u]; while (u > 0 && placed.some(q => Math.hypot(p[0] - q[0], p[1] - q[1]) < gap(p, q))) { u -= .006; p = [...a3_pathAt(u), u]; } }
    if (u <= 0) break;
    placed.push(p);
  }
  placed.forEach((p, i) => p.push(i < 2 ? 'kalpak' : 'fes'));
  for (const [x, y, d, uu, cap] of [...placed].reverse()) a3_soldier(ctx, x, y + 4, lerp(2.5, 1.05, uu), (ph + Math.round(uu * 40)) % 2, d, cap);
  // tepeye dikilen sancak ("dağa çıktı")
  const fk = a1_pop(t, Tdg, .2);
  if (fk > 0) {
    const [px, py] = [1520, 420], wv = Math.sin(Math.floor(t * 15) / 15 * 7) * 6;
    ctx.save(); ctx.translate(px, py); ctx.scale(fk, fk);
    inkStroke(ctx, PL([[0, 0], [0, -150]], false), 5);
    const fl = SP([[2, -148], [60, -142 + wv * .4], [110, -150 + wv], [108, -96 + wv], [58, -92 + wv * .4], [2, -100]], true, .6); knock(ctx, fl); plate(ctx, 'red', fl); inkStroke(ctx, fl, 2.4);
    const cr = new Path2D(); cr.arc(46, -122, 15, 0, TAU); cr.arc(51, -124, 12.5, 0, TAU, true); ctx.save(); ctx.fillStyle = P.paper; ctx.fill(cr, 'evenodd'); ctx.restore();
    ctx.restore();
  }
  ctx.restore();
  stamp(ctx, 'MAKEDONYA · TEMMUZ 1908', 114, 112, t - S('D02') - .1, 4.2, { size: 48 });
}, { tr: { type: 'press', dur: .6 } });

// ═══════════ D02b · 1908 "Hürriyet" kartpostalı (belge) ve sevinen kalabalık (23 Temmuz 1908) ═══════════
// kartpostal üç katman: 'back' (gölge + kart), ışınlar (her karede döner), 'front' (güneş, bayraklar, çerçeve, kurdele)
function a3_rays(g, ang) {
  const w = 1000, h = 640, x0 = -w / 2, y0 = -h / 2, cx = 0, cy = 170;
  g.save(); g.clip(a1_rect(x0 + 40, y0 + 40, -x0 - 40, cy));
  for (let k = 0; k < 44; k += 2) { const a0 = ang + k / 44 * TAU, a1 = a0 + PI / 44; plate(g, 'gold', PL([[cx, cy], [cx + Math.cos(a0) * 900, cy + Math.sin(a0) * 900], [cx + Math.cos(a1) * 900, cy + Math.sin(a1) * 900]]), { a: .75 }); }
  g.restore();
}
function a3_postcard(g, part = 'front') {
  const w = 1000, h = 640, x0 = -w / 2, y0 = -h / 2;
  const card = PL(rough([[x0, y0], [-x0, y0], [-x0, -y0], [x0, -y0]], 1.4, 13));
  if (part === 'back') { plate(g, 'ink', a1_rect(x0 + 14, y0 + 18, w / 2 + 14, h / 2 + 18), { a: .4 }); knock(g, card); return; }
  g.save(); g.clip(a1_rect(x0 + 40, y0 + 40, -x0 - 40, -y0 - 40));
  const cx = 0, cy = 170;
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
// Osmanlı bayrağı (dikdörtgen, kırmızı, beyaz ay-yıldız); w: bayrak eni, wv: dalga
function a3_flag(ctx, x, y, w, wv = 0) {
  const h = w * .66, f = SP([[x, y], [x + w * .5, y - 2 + wv * .5], [x + w, y + wv], [x + w, y + h + wv], [x + w * .5, y + h - 2 + wv * .5], [x, y + h]], true, .5);
  knock(ctx, f); plate(ctx, 'red', f); inkStroke(ctx, f, 1.8);
  const cx = x + w * .44, cy = y + h * .5 + wv * .3, r = h * .28, cr = new Path2D(); cr.arc(cx, cy, r, 0, TAU); cr.arc(cx + r * .3, cy - r * .08, r * .82, 0, TAU, true);
  ctx.save(); ctx.fillStyle = P.paper; ctx.fill(cr, 'evenodd'); ctx.restore();
  const sp = []; for (let k = 0; k < 10; k++) { const a = -PI / 2 + k * TAU / 10, rr = k % 2 ? r * .2 : r * .45; sp.push([cx + r * 1.15 + Math.cos(a) * rr, cy + Math.sin(a) * rr]); } knock(ctx, PL(sp));
}
// sevinen kalabalık: başına oturmuş fes, omuzlar; elde bayrak, mendil ya da fes; kollar iki pozlu, 6 fps, kişi başına rastgele faz
function a3_crowd(ctx, t, y0, n = 18, seed = 7, Ti = -1e9) {
  const r = rng(seed), q6 = t * 6;
  for (let row = 0; row < 2; row++) for (let i = 0; i < n; i++) {
    const x = -40 + i * (W + 80) / (n - 1) + (row ? 50 : 0) + (r() - .5) * 30, s = row ? 1.25 : 1.0, y = y0 + (row ? 120 : 0) + (r() - .5) * 10;
    const kind = r(), phs = r(), sway = Math.sin(t * 2 + phs * 6) * 2, tr = Ti + phs * .3, fr = Math.floor((t - tr) * 15);
    const raised = t >= tr && fr >= 2, up = Math.floor(q6 + phs * 7) % 2;
    ctx.save(); ctx.translate(x + sway, y); ctx.scale(s, s);
    // gövde: boyun, omuzlar
    const b = new Path2D(); b.ellipse(0, -62, 16, 19, 0, 0, TAU);
    b.moveTo(-8, -46); b.lineTo(8, -46); b.lineTo(10, -38); b.quadraticCurveTo(38, -36, 46, -18); b.lineTo(52, 60); b.lineTo(-52, 60); b.lineTo(-46, -18); b.quadraticCurveTo(-38, -36, -10, -38); b.closePath();
    inkFill(ctx, b);
    const waveFes = kind > .42 && kind < .62, bare = waveFes;
    if (!bare) { const f = PL([[-15, -74], [15, -74], [12, -98], [-12, -98]]); knock(ctx, f); plate(ctx, 'red', f); inkStroke(ctx, f, 1.8); inkStroke(ctx, SP([[0, -98], [-10, -92], [-16, -80]], false), 2.2); }
    else cut(ctx, SP([[-12, -74], [0, -80], [12, -74]], false), 1.6, { a: .5 });
    // kol: omuzdan yukarı; iki poz
    // kol: sözden önce inik; hazırlık (iki poz: hafif geri, yarıya kalkış), sonra iki pozlu sallama
    const hand = t < tr ? [34, -20] : fr === 0 ? [42, -8] : fr === 1 ? [44, -72] : up ? [30, -132] : [42, -112];
    inkStroke(ctx, SP([[30, -30], [hand[0] > 40 && hand[1] > -30 ? 44 : 40, hand[1] > -30 ? -6 : -70], hand], false), 13); inkFill(ctx, a1_ell(hand[0], hand[1], 8, 9));
    const wv = (up ? 1 : -1) * 6;
    if (!raised) { ctx.restore(); continue; }
    if (kind < .42) { // mendil
      const m = SP([[hand[0] - 2, hand[1] - 6], [hand[0] + 22, hand[1] - 18 + wv], [hand[0] + 38, hand[1] - 6 + wv], [hand[0] + 20, hand[1] + 8 + wv * .5]], true, .6); knock(ctx, m); inkStroke(ctx, m, 1.6);
    } else if (waveFes) { // elde fes
      const f = PL([[hand[0] - 13, hand[1] - 8], [hand[0] + 13, hand[1] - 8], [hand[0] + 10, hand[1] - 30], [hand[0] - 10, hand[1] - 30]]); knock(ctx, f); plate(ctx, 'red', f); inkStroke(ctx, f, 1.8);
    } else if (kind > .74) { // sopalı bayrak
      inkStroke(ctx, PL([[hand[0], hand[1] + 6], [hand[0], hand[1] - 76]], false), 3);
      a3_flag(ctx, hand[0], hand[1] - 74, 52, wv * .7);
    }
    ctx.restore();
  }
}
shot(a1_W('D02', 'sultan'), (ctx, st) => {
  setReg(303);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const Tm = a1_W('D02', 'meşrutiyet'), Tg = a1_W('D02', 'geri'), Ty = a1_W('D02', 'yeniden'), Ti = a1_W('D02', 'ilan');
  const c = { x: 960, y: kf(t, [[st.t - st.lt, 540], [Ti, 520], [Ti + .6, 500]]), z: kf(t, [[st.t - st.lt, 1.0], [Ti - .1, 1.03], [Ti + .5, 1.07]]) };
  const cd = E.out3(clamp((t - Tg + .25) / .5)), cs = settle(t, Tg + .25, .03, 2.2, 6);
  ctx.save(); cam(ctx, c, .5);
  a1_imgM(ctx, a1_cacheM('a3-d02b-bg', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R); plate(g, 'gold', R, { a: .32 });
    g.save(); g.clip(R); const hp = new Path2D(); for (let x = -1400; x < 2400; x += 18) { hp.moveTo(x, -220); hp.lineTo(x + 1400, 1300); } inkStroke(g, hp, 1.2, { a: .14 }); g.restore();
  }));
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  ctx.save(); ctx.translate(960, 440 + (1 - cd) * 760 + noise1(tf * .5, 2) * 3); ctx.rotate(-.025 + (1 - cd) * .25 + cs);
  ctx.translate(-W / 2, -H / 2); a1_imgM(ctx, a1_cacheM('a3-postcard-b', g => { g.translate(W / 2, H / 2); a3_postcard(g, 'back'); }, 40));
  ctx.save(); ctx.translate(W / 2, H / 2); a3_rays(ctx, (t - (st.t - st.lt)) * 2 * PI / 180); ctx.restore();
  a1_imgM(ctx, a1_cacheM('a3-postcard-f', g => { g.translate(W / 2, H / 2); a3_postcard(g, 'front'); }, 40));
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
  // kalabalık sevinir (ön planda): "yeniden" sözünde yükselir, "ilan" sözünde flamalar açılır
  const cu = E.out3(clamp((t - Ty + .1) / .45));
  if (cu > 0) { ctx.save(); ctx.translate(0, (1 - cu) * 320); a3_crowd(ctx, t, 960, 18, 7, Ti); ctx.restore(); }
  stamp(ctx, 'MEŞRUTİYET · 23 TEMMUZ 1908', 114, 112, t - Tm, 9, { size: 48 });
}, { tr: { type: 'cut' } });

// ═══════════ D03a · Hareket Ordusu treni İstanbul'a girer; Yıldız'da ışık söner ═══════════
function a3_skyline(g) {
  const sil = new Path2D();
  sil.moveTo(-220, 600); sil.lineTo(-220, 560);
  // ev çatıları
  const r = rng(4); let x = -220; while (x < 1150) { const w = 40 + r() * 60, h = 20 + r() * 30; sil.lineTo(x, 560 - h); sil.lineTo(x + w * .5, 548 - h); sil.lineTo(x + w, 560 - h); x += w; }
  sil.lineTo(1150, 600); sil.closePath();
  // büyük cami: kubbe, yarım kubbeler, minareler
  const dome = (cx, cy, r0) => { sil.moveTo(cx - r0, cy); sil.arc(cx, cy, r0, PI, 0); sil.closePath(); sil.rect(cx - 2, cy - r0 - 22, 4, 22); };
  sil.rect(260, 470, 340, 100); dome(430, 470, 92); dome(320, 500, 52); dome(540, 500, 52);
  for (const [mx, h] of [[230, 230], [250, 190], [610, 230], [630, 190]]) { sil.rect(mx - 7, 570 - h, 14, h); sil.moveTo(mx - 9, 570 - h); sil.lineTo(mx, 570 - h - 40); sil.lineTo(mx + 9, 570 - h); sil.closePath(); }
  sil.rect(820, 500, 200, 70); dome(920, 500, 70); for (const mx of [800, 1040]) { sil.rect(mx - 6, 380, 12, 190); sil.moveTo(mx - 8, 380); sil.lineTo(mx, 346); sil.lineTo(mx + 8, 380); sil.closePath(); }
  g.save(); plate(g, 'teal', sil, { n: 2 }); plate(g, 'ink', sil, { a: .35 }); g.restore();
}
function a3_train(g, x, y, tf) {
  // x: lokomotif burnu; vagonlar sola uzanır
  const wheel = (cx, cy, r) => { const w = a1_ell(cx, cy, r, r); knock(g, w, P.ink); inkFill(g, w); const a0 = (Math.floor(tf * 15) % 4) * PI / 8; for (let k = 0; k < 4; k++) cut(g, PL([[cx + Math.cos(a0 + k * PI / 4) * (r - 4), cy + Math.sin(a0 + k * PI / 4) * (r - 4)], [cx - Math.cos(a0 + k * PI / 4) * (r - 4), cy - Math.sin(a0 + k * PI / 4) * (r - 4)]], false), 1.6, { a: .6 }); cut(g, a1_ell(cx, cy, r - 3, r - 3), 1.4, { a: .5 }); };
  // vagonlar
  for (let i = 0; i < 5; i++) {
    const x1 = x - 330 - i * 300, x0 = x1 - 280, car = a1_rect(x0, y - 150, x1, y - 30);
    knock(g, car); inkFill(g, car); const roof = PL([[x0 - 8, y - 150], [x1 + 8, y - 150], [x1 - 6, y - 166], [x0 + 6, y - 166]]); inkFill(g, roof);
    for (let k = 0; k < 5; k++) { const wx = x0 + 16 + k * 52, wi = a1_rect(wx, y - 128, wx + 36, y - 92); knock(g, wi); plate(g, 'gold', wi, { a: .55 }); const fz = PL([[wx + 10, y - 96], [wx + 26, y - 96], [wx + 24, y - 112], [wx + 12, y - 112]]); knock(g, fz); plate(g, 'red', fz); inkFill(g, a1_ell(wx + 18, y - 92, 9, 6)); inkStroke(g, wi, 1.6); }
    cut(g, PL([[x0 + 6, y - 74], [x1 - 6, y - 74]], false), 1.6, { a: .45 });
    inkStroke(g, PL([[x1, y - 50], [x1 + 20, y - 50]], false), 5);
    wheel(x0 + 50, y - 20, 22); wheel(x1 - 50, y - 20, 22);
  }
  // kömürlük
  const td = a1_rect(x - 320, y - 120, x - 210, y - 30); inkFill(g, td); wheel(x - 290, y - 18, 20); wheel(x - 240, y - 18, 20);
  // lokomotif: kazan, baca, kabin, mahmuz
  const boiler = a1_rect(x - 170, y - 130, x - 20, y - 50); inkFill(g, boiler); cut(g, PL([[x - 160, y - 116], [x - 30, y - 116]], false), 2.4, { a: .7 });
  const cab = a1_rect(x - 210, y - 190, x - 140, y - 40); inkFill(g, cab); const cw = a1_rect(x - 196, y - 176, x - 156, y - 140); knock(g, cw); plate(g, 'gold', cw, { a: .7 }); inkStroke(g, cw, 1.6);
  inkFill(g, PL([[x - 214, y - 196], [x - 134, y - 196], [x - 134, y - 186], [x - 214, y - 186]]));
  inkFill(g, PL([[x - 60, y - 130], [x - 66, y - 186], [x - 34, y - 186], [x - 40, y - 130]])); inkFill(g, PL([[x - 72, y - 196], [x - 28, y - 196], [x - 34, y - 184], [x - 66, y - 184]]));
  inkFill(g, a1_ell(x - 100, y - 136, 12, 10));
  const buf = a1_rect(x - 22, y - 62, x + 6, y - 44); knock(g, buf); plate(g, 'red', buf); inkStroke(g, buf, 2);
  inkFill(g, PL([[x - 20, y - 44], [x + 26, y - 6], [x - 20, y - 6]]));
  for (const wx of [x - 150, x - 96, x - 44]) wheel(wx, y - 26, wx === x - 44 ? 18 : 28);
  inkStroke(g, PL([[x - 150, y - 26], [x - 44, y - 26]], false), 4);
}
shot(Se('D02') + .55, (ctx, st) => {
  setReg(304);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15, t0 = st.t - st.lt;
  const Th = a1_W('D03', 'hareket'), Ta = a1_W('D03', 'abdülhamidi');
  const c = { x: kf(t, [[t0, 900], [t0 + 5, 1010]]), y: 540, z: 1.05 };
  ctx.save(); cam(ctx, c, .3);
  a1_imgM(ctx, a1_cacheM('a3-d03-sky', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R);
    plate(g, 'teal', a1_rect(-220, -220, W + 220, 160), { a: .38 }); plate(g, 'gold', a1_rect(-220, 160, W + 220, 330), { a: .42 }); plate(g, 'gold', a1_rect(-220, 330, W + 220, 470), { a: .22 });
    radialHT(g, 'teal', 960, -900, 900, 1150, .3, 0, { cell: 12, ang: 15, box: [-220, -220, W + 220, 200] });
  }));
  ctx.restore();
  ctx.save(); cam(ctx, c, .55);
  a1_imgM(ctx, a1_cacheM('a3-d03-city', g => { a3_skyline(g); g.translate(1500, 640); g.scale(.78, .78); g.translate(-1500, -640); a1_yildiz(g); }));
  // Yıldız'da pencere: "Abdülhamid'i" sözünde söner
  const on = 1 - ramp(t, Ta, Ta + .2), wx = 1500 + (1510 - 1500) * .78, wy = 640 + (444 - 640) * .78;
  if (on > 0) { ctx.save(); ctx.globalAlpha = on; for (const [r, a] of [[30, .4], [18, .7]]) plate(ctx, 'gold', a1_ell(wx, wy, r, r * .8), { a }); knock(ctx, a1_rect(wx - 6, wy - 8, wx + 6, wy + 8), '#FFF3D0'); ctx.restore(); }
  // deniz
  const sea = a1_rect(-240, 600, W + 260, 770); knock(ctx, sea); plate(ctx, 'teal', sea); plate(ctx, 'teal', a1_rect(-240, 690, W + 260, 770), { a: .4 });
  const rr = rng(5); for (let i = 0; i < 70; i++) { const y = 610 + rr() * 150, x = -200 + rr() * 2300, L = 16 + rr() * 40; cut(ctx, PL([[x, y], [x + L, y]], false), 1.6, { a: .3 }); }
  ctx.restore();
  // set, ray ve tren
  ctx.save(); cam(ctx, c, 1);
  const emb = PL([[-240, 790], [W + 260, 790], [W + 260, H + 80], [-240, H + 80]]); knock(ctx, emb); plate(ctx, 'teal', emb, { n: 2 }); plate(ctx, 'ink', emb, { a: .45 });
  for (let y = 830; y < H + 60; y += 44) { cut(ctx, PL([[-240, y], [W + 260, y]], false), 1.4, { a: .22 }); for (let x = -240 + ((y / 44) % 2) * 60; x < W + 260; x += 120) cut(ctx, PL([[x, y], [x, y + 44]], false), 1.2, { a: .18 }); }
  for (let x = -240; x < W + 260; x += 34) inkStroke(ctx, PL([[x, 786], [x + 18, 796]], false), 4);
  inkStroke(ctx, PL([[-240, 782], [W + 260, 782]], false), 5); cut(ctx, PL([[-240, 780], [W + 260, 780]], false), 1.4, { a: .6 });
  const tx = lerp(420, 2350, (t - t0) / 5.2);
  // duman: bacadan çıkan, arkaya savrulan yarım tonlu bulutlar
  for (let k = 0; k < 14; k++) {
    const age = ((t - t0) * 3 - k * .5); if (age < 0) continue; const ex = lerp(420, 2350, (t - t0 - k * .17) / 5.2) - 50;
    const px = ex - age * 42, py = 584 - age * 26 - k * 2, r = 18 + age * 13; if (age > 5) continue;
    const pf = SP(rough([[px - r, py], [px - r * .6, py - r * .8], [px, py - r], [px + r * .7, py - r * .7], [px + r, py], [px + r * .5, py + r * .6], [px - r * .4, py + r * .6]], r * .08, k), true, .9);
    knock(ctx, pf); halftone(ctx, 'ink', pf, .1 + .16 * (1 - age / 5), { cell: 11, ang: 45 }); inkStroke(ctx, pf, 1.6, { a: .4 * (1 - age / 5) + .1 });
  }
  a3_train(ctx, tx, 780, tf);
  ctx.restore();
  stamp(ctx, 'İSTANBUL · 24 NİSAN 1909', 114, 112, t - Th, 9, { size: 48 });
}, { tr: { type: 'press', dur: .5 } });

function a3_room() {
  return a1_cacheM('a3-d03b-room', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R); plate(g, 'gold', a1_rect(-220, -220, W + 220, 780), { a: .4 });
    for (let i = 0; i < 9; i++) { const x0 = -180 + i * 270; inkStroke(g, a1_rect(x0, 60, x0 + 220, 520), 2, { a: .6 }); cut(g, a1_rect(x0 + 10, 70, x0 + 210, 510), 1.4, { a: .35 }); inkStroke(g, a1_rect(x0 + 24, 84, x0 + 196, 496), 1.2, { a: .45 }); }
    inkStroke(g, PL([[-220, 560], [W + 220, 560]], false), 2.4); for (let i = 0; i < 9; i++) inkStroke(g, a1_rect(-180 + i * 270, 590, -180 + i * 270 + 220, 760), 1.6, { a: .55 });
    plate(g, 'gold', a1_rect(-220, -220, W + 220, 30), { n: 2 }); inkStroke(g, PL([[-220, 30], [W + 220, 30]], false), 3);
    const win = a1_rect(-100, 80, 160, 640); knock(g, win); plate(g, 'gold', win, { a: .18 }); inkStroke(g, win, 3); inkStroke(g, PL([[30, 80], [30, 640]], false), 4); inkStroke(g, PL([[-100, 360], [160, 360]], false), 4);
    const cur = PL([[150, 40], [340, 40], [328, 330], [292, 420], [352, 712], [168, 712], [196, 420], [168, 330]]); knock(g, cur); plate(g, 'gold', cur, { n: 2 }); plate(g, 'khaki', cur, { a: .4 }); inkStroke(g, PL([[178, 418], [300, 418]], false), 6); inkStroke(g, cur, 2.6); for (let k = 1; k < 4; k++) inkStroke(g, SP([[150 + k * 44, 50], [168 + k * 36, 300], [180 + k * 42, 700]], false), 1.6, { a: .6 });
    const floor = a1_rect(-220, 780, W + 220, H + 220); knock(g, floor); plate(g, 'gold', floor, { a: .55 }); plate(g, 'khaki', floor, { a: .35 }); inkStroke(g, PL([[-220, 780], [W + 220, 780]], false), 3);
    for (let i = 0; i < 12; i++) inkStroke(g, PL([[-220, 800 + i * 26], [W + 220, 800 + i * 26]], false), 1.2, { a: .3 });
  });
}
// ═══════════ D03b · Yıldız'da boş koltuk; ordunun kurmayları: Mustafa Kemal ve Kâzım Karabekir ═══════════
function a3_chair(g, x, y, s) {
  g.save(); g.translate(x, y); g.scale(s, s);
  plate(g, 'ink', a1_ell(10, 250, 210, 36), { a: .3 });
  const back = SP([[-120, 0], [-128, -200], [-100, -300], [0, -330], [100, -300], [128, -200], [120, 0]], true, .8);
  knock(g, back); plate(g, 'gold', back, { n: 2 }); inkStroke(g, back, 4);
  const up = SP([[-96, -10], [-102, -190], [-80, -270], [0, -294], [80, -270], [102, -190], [96, -10]], true, .8); knock(g, up); plate(g, 'sepia', up, { n: 2 }); plate(g, 'ochre', up, { a: .3 }); plate(g, 'sepia', SP([[-96, -10], [-102, -190], [-80, -270], [-30, -290], [-50, -180], [-50, -10]], true), { a: .5 }); inkStroke(g, up, 2.4);
  for (let k = 0; k < 3; k++) for (let j = 0; j < 2; j++) { const bx = -40 + j * 80, by = -220 + k * 70; inkFill(g, a1_ell(bx, by, 4, 4)); }
  const seat = PL([[-150, 10], [150, 10], [170, 70], [-170, 70]]); knock(g, seat); plate(g, 'sepia', seat, { n: 2 }); plate(g, 'ochre', seat, { a: .3 }); plate(g, 'sepia', a1_rect(-170, 50, 170, 70), { a: .5 }); inkStroke(g, seat, 3);
  const apron = SP([[-172, 70], [172, 70], [160, 110], [0, 124], [-160, 110]], true, .8); knock(g, apron); plate(g, 'gold', apron, { n: 2 }); inkStroke(g, apron, 3);
  for (const sd of [-1, 1]) {
    const arm = SP([[sd * 120, -120], [sd * 176, -110], [sd * 186, -86], [sd * 170, 20], [sd * 150, 20], [sd * 140, -90], [sd * 120, -100]], true, .8); knock(g, arm); plate(g, 'gold', arm, { n: 2 }); inkStroke(g, arm, 3);
    const leg = SP([[sd * 150, 110], [sd * 166, 110], [sd * 176, 250], [sd * 158, 250], [sd * 146, 180]], true, .8); knock(g, leg); plate(g, 'gold', leg, { n: 2 }); inkStroke(g, leg, 3);
  }
  cut(g, SP([[-80, -300], [0, -322], [80, -300]], false), 2.4, { a: .5 });
  g.restore();
}
shot(a1_W('D03', 'meclis') + .45, (ctx, st) => {
  setReg(305);
  paperBG(ctx);
  const t = st.t, t0 = st.t - st.lt, Ti = a1_W('D03', 'indirdi');
  const c = { x: kf(t, [[t0, 940], [Ti + .8, 925]]), y: kf(t, [[t0, 545], [Ti + .8, 560]]), z: kf(t, [[t0, 1.0], [Ti - .3, 1.02], [Ti + .8, 1.07]]) };
  ctx.save(); cam(ctx, c, .7); a1_imgM(ctx, a3_room()); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  // pencereden koltuğa düşen ışık ve boş koltuk ("tahttan indirdi")
  const sl = (t - t0) * 38; ctx.save(); ctx.globalAlpha = .4; knock(ctx, PL([[560 + sl, 780], [920 + sl, 780], [1200 + sl, H + 80], [460 + sl, H + 80]])); ctx.restore();
  a3_chair(ctx, 900, 640, 1.08);
  ctx.restore();
}, { tr: { type: 'cut' } });

// ═══════════ D03c · Ordunun kurmayları: Mustafa Kemal (27) ve Kâzım Karabekir (26); lacivert setre, kalpak (Nisan 1909) ═══════════
shot(a1_W('D03', 'ordunun'), (ctx, st) => {
  setReg(308);
  paperBG(ctx);
  const t = st.t, t0 = st.t - st.lt, Tm = a1_W('D03', 'mustafa'), Tk = a1_W('D03', 'kazım');
  const c = { x: kf(t, [[t0, 940], [t0 + 4.7, 985]]), y: kf(t, [[t0, 540], [t0 + 4.7, 528]]), z: kf(t, [[t0, 1.0], [Tm, 1.03, E.out2], [Tk, 1.045], [t0 + st.d, 1.075, E.lin]]) };
  ctx.save(); cam(ctx, c, .45); ctx.translate(-260, -40); a1_imgM(ctx, a3_room());
  // pencereden duvara düşen ışık şeridi yavaşça kayar
  const sl = (t - t0) * 70; ctx.save(); ctx.globalAlpha = .22; knock(ctx, PL([[380 + sl, 40], [620 + sl, 40], [820 + sl, 780], [580 + sl, 780]])); ctx.restore();
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  // başlar kelimeye bağlı olarak koltuğa (kadraj solu) döner: Mustafa Kemal "arasında", Karabekir "Karabekir" sözünde
  const Tar = a1_W('D03', 'arasında'), Tkb = a1_W('D03', 'karabekir'), tq = Math.floor(t * 15) / 15, chair = [-260, 600];
  const mT = tq >= Tar, kT = tq >= Tkb, mE = ramp(t, Tar, Tar + .35, E.out2), kE = ramp(t, Tkb, Tkb + .35, E.out2);
  a1_fig(ctx, t, { x: 1310, y: 330, s: 2.05, dir: -1, who: 'karabekir', gear: 'kalpak', gearCol: 'ink', coat: 'setre', col: 'navy', collarCol: 'red', age: 26, lookAt: kT ? chair : undefined, look: kT ? undefined : [-.45, .1], tilt: -.05 * kE, len: 520, seed: 11, back: true, w: 1.02, idle: 1.4 });
  a1_fig(ctx, t, { x: 700, y: 360, s: 2.05, dir: -1, who: 'mk', gear: 'kalpak', gearCol: 'ink', coat: 'setre', col: 'navy', collarCol: 'red', age: 27, lookAt: mT ? chair : undefined, look: mT ? undefined : [-.5, .12], tilt: -.05 * mE, len: 520, seed: 3, sep: true, w: .96, turn: .2, idle: 1.4 });
  ctx.restore();
  nameTag(ctx, 110, 850, 'MUSTAFA KEMAL', '27 yaşında · Hareket Ordusu kurmayı', t - Tm, 9);
  nameTag(ctx, 1824, 590, 'KÂZIM KARABEKİR', '26 yaşında · Hareket Ordusu kurmayı', t - Tk, 9, { align: 'right' });
}, { tr: { type: 'cut' } });

// ═══════════ D04a · Bölünmüş kare: okullar | Abdülhamid (nötr) | jurnaller ═══════════
shot(S('D04'), (ctx, st) => {
  setReg(306);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const Tj = a1_W('D04', 'jurnalleri'), Ts = a1_W('D04', 'aynı'), Tk = a1_W('D04', 'bu'), Ta = a1_W('D04', 'arasında');
  const c = { x: kf(t, [[st.t - st.lt, 948], [st.t - st.lt + st.d, 976, E.lin]]), y: kf(t, [[Ts, 540], [Ts + 1.4, 505], [Tk, 505], [Tk + .6, 540]]), z: kf(t, [[S('D04'), 1.0], [Ts, 1.01], [Ts + 1.4, 1.05], [Tk, 1.05], [Tk + .6, 1.0], [Ta, 1.01], [Ta + 1.2, 1.05]]) };
  const sw = E.io3(clamp((t - Tk + .05) / .55)), dx = 90 * sw;
  const L = E.out3(clamp((t - S('D04') + .1) / .4)), R = E.out3(clamp((t - Tj + .05) / .4));
  ctx.save(); cam(ctx, c, 1);
  // sol pano: okul planı + açık kitap + rüşdiye noktaları (aydınlık)
  if (L > 0) {
    ctx.save(); ctx.globalAlpha = L; ctx.translate(-dx, (1 - L) * 30);
    const lp = a1_rect(-60, -60, 650, H + 60); knock(ctx, lp); plate(ctx, 'gold', lp, { a: .4 });
    if (!A1_PLAN) a1_planOn(ctx, -2000, -2000, 1, 0, 1, {});
    a1_planOn(ctx, -2000, -2000, .01, 0, 1, {});
    ctx.save(); ctx.translate(70, 200); ctx.rotate(-.05); plate(ctx, 'ink', a1_rect(8, 12, 528, 382), { a: .3 }); ctx.drawImage(A1_PLAN, -10, -10, 540, 383); ctx.restore();
    ctx.save(); ctx.translate(330, 760); ctx.rotate(.04);
    for (const sd of [-1, 1]) { const pg = SP([[0, -90], [sd * 120, -104], [sd * 230, -92], [sd * 236, 90], [sd * 120, 80], [0, 96]], true, .6); knock(ctx, pg); inkStroke(ctx, pg, 2.6); for (let k = 0; k < 6; k++) scriptLine(ctx, sd > 0 ? 210 : -20, -60 + k * 24, 180, 6, 960 + k + (sd > 0 ? 10 : 0), { w: 1.6 }); }
    ctx.restore();
    ctx.restore();
  }
  // sağ pano: jurnal yığınları (karanlık)
  if (R > 0) {
    ctx.save(); ctx.globalAlpha = R; ctx.translate(dx, (1 - R) * 30);
    const rp = a1_rect(1270, -60, W + 60, H + 60); knock(ctx, rp); plate(ctx, 'ink', rp, { a: .55 }); plate(ctx, 'teal', rp, { a: .3 });
    a1_jurnals(ctx, 1600, 520, 14, .9, 0, 9); a1_jurnals(ctx, 1560, 900, 10, 1.0, 0, 13);
    for (let i = 0; i < 4; i++) paperSheet(ctx, 1380 + i * 140, 200 + (i % 2) * 60 + Math.sin(t * 1.6 + i * 1.3) * 4, 150, 110, -.2 + i * .14 + Math.sin(t * 1.1 + i) * .03, 70 + i, { rows: 4 });
    ctx.restore();
  }
  // orta: Abdülhamid, nötr; bakışı izleyiciye
  const cx0 = 650 - dx, cx1 = 1270 + dx;
  knock(ctx, a1_rect(cx0, -60, cx1, H + 60));
  ctx.save(); ctx.beginPath(); ctx.rect(cx0, -60, cx1 - cx0, H + 120); ctx.clip();
  if (sw < 1) a1_fig(ctx, t, { x: 975, y: 370 + sw * 900, s: 1.85, dir: -1, who: 'abdulhamid', gear: 'fes', coat: 'setre', col: 'ink', age: 60, look: [-.5, .12], len: 520, seed: 21, w: .9, idle: 1.2 });
  // "Bu kuşak…": açılıştaki 1893 sınıfının beş çocuğu Abdülhamid'in yerine, okulla jurnalin arasına girer (act0 yardımcıları)
  if (sw > 0 && typeof a0_classKids === 'function') {
    const k = (cx1 - cx0) / W, ty = 560 - 445 * k + (1 - sw) * 760;
    const bg = a0_cache('a0-k93-bg', g => a0_classBG(g, 150, 740));
    // sınıf fotoğrafı paspartusu: kalın kâğıt pafta, iç çerçeve, köşe tutamakları
    const my0 = ty + 150 * k - 150, my1 = ty + 740 * k + 170, mx0 = cx0 + 34, mx1 = cx1 - 34;
    plate(ctx, 'ink', a1_rect(mx0 + 10, my0 + 12, mx1 + 10, my1 + 12), { a: .3 });
    const mount = PL(rough([[mx0, my0], [mx1, my0], [mx1, my1], [mx0, my1]], 1.2, 93)); knock(ctx, mount, P.paperD); plate(ctx, 'sepia', mount, { a: .18 }); inkStroke(ctx, mount, 2.6);
    inkStroke(ctx, a1_rect(cx0 + 4, ty + 150 * k - 6, cx1 - 4, ty + 740 * k + 6), 3);
    for (const [qx, qy, a] of [[cx0 + 4, ty + 150 * k - 6, 0], [cx1 - 4, ty + 150 * k - 6, 1], [cx0 + 4, ty + 740 * k + 6, 3], [cx1 - 4, ty + 740 * k + 6, 2]]) { ctx.save(); ctx.translate(qx, qy); ctx.rotate(a * PI / 2); const tb = PL([[-16, -16], [34, -16], [-16, 34]]); knock(ctx, tb); plate(ctx, 'sepia', tb, { n: 2 }); inkStroke(ctx, tb, 2); ctx.restore(); }
    ctx.save(); ctx.translate(cx0, ty); ctx.scale(k, k);
    ctx.beginPath(); ctx.rect(0, 150, W, 590); ctx.clip(); ctx.drawImage(bg, 0, 0, W, H); a0_classKids(ctx, t, 150, 740);
    ctx.restore();
    scriptLine(ctx, 960 + 160, my1 - 56, 320, 9, 1893, { w: 1.8 }); scriptLine(ctx, 960 + 90, my1 - 28, 180, 7, 1894, { w: 1.4, a: .8 });
    if (!NOTEXT) { ctx.save(); ctx.globalAlpha = clamp((t - Tk - .3) / .3); txt(ctx, '1893', 960, my0 + 92, FONT.title(64), { align: 'center', ls: 4 }); ctx.restore(); }
  }
  ctx.restore();
  for (const x of [cx0, cx1]) { inkStroke(ctx, PL([[x, -60], [x, H + 60]], false), 5); cut(ctx, PL([[x + (x < 960 ? 9 : -9), -60], [x + (x < 960 ? 9 : -9), H + 60]], false), 3, { a: .9 }); }
  ctx.restore();
}, { tr: { type: 'press', dur: .6 } });
