// Cennet seti (CEN): açık anahtar. Cehennem karesinin tersi:
//  - tek, baskın, taramasız ışık merkezi (Tanrı yalnız ışıktır: yüz, el, hale, haç yok);
//  - gök tarama çizgileri bu merkeze göre eş merkezli (GR 'rad'); merkezden uzaklaştıkça koyulaşır;
//  - kâğıt beyazı kütleler (bulut terasları, kanatlar, bedenler) konturla değil arkalarındaki taramanın durmasıyla ayrılır;
//  - koyu çapa: bulut alt yüzleri (gölge hilali, forma sarılan tarama + içe giren mürekkep vuruşları), kanat iç yüzü, ön plan kütlesi.
// Bütün işlevler açık levhaya çizer (GR.begin/engrave çağırmaz). Dünya koordinatı 1920×1080.
'use strict';

// ── ışık merkezi ve gök ──
// L: {x, y} ışık merkezi; o: {r0 (taramasız çekirdek), r1 (en koyu tona ulaşılan uzaklık), v (uzak tonu), mid (orta ton), a (0..1 şiddet; 0 = sönük gök),
//     kama: [{a (açı), w (en geniş yerin yarı açısı), len, at (en geniş yerin oranı)}], dark (0..1 alacakaranlık)}
function cen_gok(L, o = {}) {
  const { tx, px, tone } = GR, a = o.a ?? 1, dk = o.dark || 0;
  const r0 = (o.r0 ?? 110) * (.35 + .65 * a), r1 = (o.r1 ?? 1900) * (1 - .4 * dk);
  const vf = o.v ?? .72, vm = o.mid ?? .88;
  const g = tx.createRadialGradient(L.x, L.y, r0 * .6, L.x, L.y, r1);
  const k = v => clamp(lerp(v, v * .85, dk));
  g.addColorStop(0, tone(1)); g.addColorStop(.08, tone(lerp(k(vm), 1, a * .9)));
  g.addColorStop(.3, tone(lerp(k(vm * .97), k(vm), a))); g.addColorStop(.62, tone(lerp(lerp(vm, vf, .55), .3, dk))); g.addColorStop(.85, tone(lerp(lerp(vm, vf, .85), .06, dk))); g.addColorStop(1, tone(lerp(vf, .02, dk)));
  tx.fillStyle = g; tx.fillRect(-1600, -1600, W + 3200, H + 3200);
  px.fillStyle = GR.hatch({ type: 'rad', cx: L.x, cy: L.y, id: 1, ph: o.ph || 0 }); px.fillRect(-1600, -1600, W + 3200, H + 3200);
  // ışık kamaları: merkezden çıkan, ortada genişleyip ucu sivrilen kâğıt boşlukları (en çok 3)
  if (o.kama && a > 0) {
    tx.save(); tx.globalCompositeOperation = 'lighten';
    for (const K of o.kama) {
      const n = 14, A = [], B = [], at = K.at ?? .35, Lk = K.len * (.55 + .45 * a);
      for (let i = 0; i <= n; i++) {
        const u = i / n, r = 30 + Lk * u, wv = K.w * (u < at ? Math.pow(u / at, .6) : Math.pow(1 - (u - at) / (1 - at), 1.4));
        A.push([L.x + Math.cos(K.a - wv) * r, L.y + Math.sin(K.a - wv) * r]); B.push([L.x + Math.cos(K.a + wv) * r, L.y + Math.sin(K.a + wv) * r]);
      }
      const P = new Path2D(); poly(P, [[L.x, L.y], ...A, ...B.reverse()], true);
      const gg = tx.createRadialGradient(L.x, L.y, 0, L.x, L.y, Lk);
      gg.addColorStop(0, tone(1)); gg.addColorStop(.7, tone(lerp(.9, 1, a))); gg.addColorStop(1, tone(.86));
      tx.fillStyle = gg; tx.fill(P);
    }
    tx.restore();
  }
  // çekirdek: tam kâğıt (karenin en parlak yeri)
  if (a > 0) PR.glow(L.x, L.y, r0 * .5, r0 * 1.6, 1, Math.min(1, a * 1.2));
}

// ── bulut terası ──
// Kâğıt beyazı yumrular; her yumrunun ışıktan uzak yanında koyu bir gölge hilali (forma sarılan eş merkezli tarama,
// alt kenarda düz koyuya varır) ve hilalden yumrunun içine giren, sivrilen birkaç mürekkep vuruşu. Kontur yok:
// yumru üst kenarında yalnız arkasındaki göğün taramasıyla ayrılır.
// o: {x, y, w, h, seed, L (ışık merkezi), sh (gölge şiddeti 0..1; .8), n (yumru sayısı), base (alt düz koyu şerit; true),
//     drift, cuts (vuruş yoğunluğu; 1), flat (alt kenar düzlüğü)}
function cen_bulut(o) {
  const { tx, tone, fill } = GR, r = rng(o.seed || 1), L = o.L || { x: W / 2, y: -200 }, sh = o.sh ?? .8, dr = o.drift || 0;
  const n = o.n || Math.max(3, Math.round(o.w / (o.h * .9))), P = [];
  for (let i = 0; i < n; i++) {
    const f = (i + .5 + (r() - .5) * .8) / n, env = .5 + .5 * Math.sqrt(Math.sin(clamp(f) * PI));
    const R = o.h * (.3 + r() * .62) * env, cx = o.x - o.w / 2 + f * o.w + dr, cy = o.y - R * (.15 + r() * .45) + (r() - .5) * o.h * .2;
    P.push({ x: cx, y: cy, r: R, s: (o.seed || 1) * 131 + i * 17, lay: 0 });
    const m = r() < .35 ? 0 : r() < .7 ? 1 : 2;
    for (let k = 0; k < m; k++) { const a = -PI / 2 + (r() - .5) * 2.2, rr = R * (.3 + r() * .38); P.push({ x: cx + Math.cos(a) * R * .75, y: cy + Math.sin(a) * R * .55, r: rr, s: (o.seed || 1) * 131 + i * 17 + 7 + k, lay: 1 }); }
  }
  // arkadan öne: üstteki küçük yumrular önce (alttakiler onları örter: teras alt kenarı önde kalır)
  P.sort((a, b) => (a.y + a.r * .5) - (b.y + b.r * .5));
  const U = new Path2D();
  // gövde: yumruların altını dolduran kütle (teras/duvar); aşağı doğru koyulaşır
  if (o.len) {
    const xs = P.filter(p => !p.lay).sort((a, b) => a.x - b.x), yb = o.y + o.h * o.len, Bd = new Path2D(), q = rng((o.seed || 1) + 11);
    Bd.moveTo(xs[0].x - xs[0].r * .9, xs[0].y);
    for (const p of xs) Bd.lineTo(p.x, p.y);
    const xe = xs[xs.length - 1]; Bd.lineTo(xe.x + xe.r * .9, xe.y);
    const xa = xs[0].x - xs[0].r * .9, xb = xe.x + xe.r * .9;
    for (let x = xb; x >= xa; x -= 30) { const u = (x - xa) / (xb - xa), e = Math.pow(Math.sin(PI * u), .45);
      Bd.lineTo(x, o.y + (yb - o.y) * e + Math.sin(x * .013 + 2) * o.h * .15 * e + (q() - .5) * o.h * .06); }
    Bd.closePath(); U.addPath(Bd);
    const g = tx.createLinearGradient(0, o.y, 0, yb); g.addColorStop(0, tone(lerp(.985, .45, sh))); g.addColorStop(.5, tone(lerp(.985, .2, sh))); g.addColorStop(1, tone(lerp(.985, .04, sh)));
    fill(Bd, g, { type: 'rad', cx: L.x, cy: L.y, id: 2, ph: .3 });
  }
  const blob = p => { const q = rng(p.s), a1 = q() * TAU, a2 = q() * TAU, k1 = .05 + q() * .05, k2 = .03 + q() * .03, pts = [];
    for (let i = 0; i < 24; i++) { const a = i / 24 * TAU, rr = p.r * (1 + k1 * Math.sin(3 * a + a1) + k2 * Math.sin(5 * a + a2)); pts.push([p.x + Math.cos(a) * rr * 1.2, p.y + Math.sin(a) * rr * (o.flat ?? .78)]); }
    const B = new Path2D(); spline(B, pts, true); return B; };
  for (const p of P) {
    const B = blob(p); U.addPath(B);
    // ışık yönü (yumrudan ışık merkezine)
    let lx = L.x - p.x, ly = L.y - p.y; { const l = Math.hypot(lx, ly) || 1; lx /= l; ly /= l; }
    // gövde: kâğıt; tarama yumrunun çevresinde eş merkezli (gölge hilalinde görünür)
    fill(B, tone(.985), { type: 'bend', ox: p.x, oy: p.y - p.r * .2, a: 0, k: .55 / p.r, id: 2, ph: (p.s % 7) / 7 });
    if (sh > 0) {
      tx.save(); tx.clip(B);
      // gölge hilali: ışığa doğru kaydırılmış elips yumrunun dışında kalan yan; içeri doğru açılan ton
      const vx = lerp(lx, 0, .45), vy = lerp(ly, -1, .45), ox = p.x + vx * p.r * .45, oy = p.y + vy * p.r * .4;
      const g = tx.createRadialGradient(ox, oy, p.r * .5, ox, oy, p.r * 1.45);
      g.addColorStop(0, tone(.985)); g.addColorStop(.42, tone(.985)); g.addColorStop(.7, tone(lerp(.985, .5, sh))); g.addColorStop(1, tone(lerp(.985, .1, sh)));
      tx.fillStyle = g; tx.fillRect(p.x - p.r * 2, p.y - p.r * 2, p.r * 4, p.r * 4);
      tx.restore();
    }
  }
  // alt kenar: teras gövdesinin altını kapatan koyu şerit (çapa); üst kenarı dalgalı
  if (o.base !== false && sh > 0) {
    tx.save(); tx.clip(U);
    const yb = o.y + o.h * (o.by ?? .02), B2 = new Path2D(), q = rng((o.seed || 1) + 3);
    B2.moveTo(o.x - o.w, yb + 600); for (let x = o.x - o.w; x <= o.x + o.w; x += 30) B2.lineTo(x + dr, yb + Math.sin(x * .011 + 1.3) * o.h * .12 + Math.sin(x * .031) * o.h * .05); B2.lineTo(o.x + o.w, yb + 600); B2.closePath();
    const g = tx.createLinearGradient(0, yb - o.h * .1, 0, yb + o.h * .55); g.addColorStop(0, tone(lerp(.985, .55, sh))); g.addColorStop(.35, tone(lerp(.985, .16, sh))); g.addColorStop(1, tone(lerp(.985, .02, sh)));
    tx.fillStyle = g; tx.fill(B2); tx.restore();
  }
  // mürekkep vuruşları: gölge hilalinden yumrunun içine (ışığa doğru) giren, sivrilen kısa çizgiler
  if ((o.cuts ?? 1) > 0 && sh > .3) for (const p of P) {
    if (p.r < 26) continue;
    let lx = L.x - p.x, ly = L.y - p.y; { const l = Math.hypot(lx, ly) || 1; lx /= l; ly /= l; }
    const la = Math.atan2(ly, lx) + PI, q = rng(p.s + 9), pts = [];
    for (let k = -3; k <= 3; k++) { const a = la + k * .32; pts.push([p.x + Math.cos(a) * p.r * 1.12, p.y + Math.sin(a) * p.r * (o.flat ?? .78) * .98]); }
    tx.save(); tx.clip(U);
    PR.cuts(pts, [lx, ly], { len: [p.r * .12, p.r * .55 * (o.cuts ?? 1)], gap: [p.r * .22, p.r * .5], w: Math.max(3.4, p.r * .045), v: .03, seed: p.s, bend: .3 });
    tx.restore();
  }
  return { path: U, puffs: P };
}

// ── küçük melek (uzak ve orta saflar) ──
// Kendi basit biçimi: baş, omuz, bileğe inen uzun giysi, sırtta kapalı kanat, mızrak. Kâğıt beyazı kütle;
// ışıktan uzak yanında koyu gölge kenarı (aynı biçim, ışığın tersine kaydırılmış düz mürekkep kopyası): kontur yok.
// p: {x, y (ayak), h (baş boyu), f (bakış ±1), lx, ly (ışık yönü), bow (0..1 saray selamı: tek diz, baş eğik), spear (açı | null), sl (mızrak boyu, h),
//     v (gövde tonu; uzakta göğe yaklaşır), sh (gölge kenarı kalınlığı, h), wing (kanat 0..1), seed, kneel}
function cen_melekYol(p) {
  const h = p.h, f = p.f, b = clamp(p.bow || 0), q = rng(p.seed || 1);
  const k = 1 - .36 * b, wy = lerp(-4.3, -2.75, b), an = b * .62;            // diz çökünce etek kısalır; bel ekseni öne eğilir
  const ca = Math.cos(an), sa = Math.sin(an);
  const up = (x, y) => { const dy = y + 4.3; return [x * ca - dy * sa, wy + x * sa + dy * ca]; };   // bel üstü: bel çevresinde döner
  const W2 = ([x, y]) => [p.x + x * f * h, p.y + y * h];
  const j = () => (q() - .5) * .08;
  // giysi: belden yere (diz çökünce arka bacak geriye uzanır)
  const LS = [[-.62, -4.3], [-.8, -2.6], [-1.0, -.6], [-1.06, 0], [-.5, .04], [0, -.03], [.5, .05], [.98, 0], [.9, -.8], [.68, -2.66], [.56, -4.3]];
  const LK = [[-.62, -2.75], [-.95, -1.7], [-1.5, -.5], [-1.8, 0], [-.9, .04], [0, -.02], [.9, .04], [1.35, 0], [1.42, -.9], [1.5, -1.85], [.56, -2.75]];
  const lo = LS.map((a, i) => [lerp(a[0], LK[i][0], b) + (i === 3 || i === 7 ? j() : 0), lerp(a[1], LK[i][1], b)]);
  // gövde: bel üstü (döner)
  const tp = [[.56, -4.3], [.74, -5.25], [.78, -5.95], [.25, -6.35], [-.25, -6.35], [-.82, -6.0], [-.86, -5.35], [-.62, -4.3]].map(([x, y]) => up(x, y));
  const P = new Path2D(); spline(P, [...lo, ...tp].map(W2), true, .55);
  // baş: boyunla birlikte biraz daha eğik
  const hd = up(.12 + .25 * b, -6.92 + .15 * b), hb = new Path2D(); hb.ellipse(...W2(hd), .37 * h, .47 * h, an * f * 1.2, 0, TAU); P.addPath(hb);
  // kol: omuzdan dirseğe, dirsekten ele (selamda el göğse)
  const sh = up(.5, -5.95), el = up(.82, -4.75), hn = b > .3 ? up(.45, -5.25) : up(1.32, -4.5);
  const arm = new Path2D(), aw = .21; { const A = [], B = [], seg = [sh, el, hn];
    for (let i = 0; i < 3; i++) { const p0 = seg[Math.max(0, i - 1)], p1 = seg[Math.min(2, i + 1)], dx = p1[0] - p0[0], dy = p1[1] - p0[1], l = Math.hypot(dx, dy) || 1, w = aw * (i === 2 ? .8 : 1);
      A.push([seg[i][0] - dy / l * w, seg[i][1] + dx / l * w]); B.push([seg[i][0] + dy / l * w, seg[i][1] - dx / l * w]); }
    spline(arm, [...A, ...B.reverse()].map(W2), true, .5); }
  // kapalı kanat: sırttan yukarı sivri uç, aşağı eteğe iner
  const wg = (p.wing ?? 1) * (1 - .75 * b); let Wp = null;
  const upW = (x, y) => { const dy = y + 4.3, c2 = Math.cos(an * .55), s2 = Math.sin(an * .55); return [x * c2 - dy * s2 - .3 * b, wy + x * s2 + dy * c2]; };
  if (p.wing !== 0) { Wp = new Path2D(); spline(Wp, [[-.55, -6.0], [-.9, -6.9 - .5 * wg], [-1.12, -7.6 - 1.0 * wg], [-1.5, -6.5], [-1.42, -4.6], [-1.12, -2.4], [-.92, -1.5], [-.8, -3.4], [-.66, -5.2]].map(([x, y]) => W2(upW(x, y))), true, .6); }
  return { P, arm, Wp, hd: W2(hd), hand: W2(hn), top: W2(up(0, -7.4)), hem: [W2([-.95, 0]), W2([.95, 0])], k };
}
function cen_melek(p) {
  const { tx, px, tone } = GR, h = p.h, Y = cen_melekYol(p), d = (p.sh ?? .16) * h, ox = -p.lx * d, oy = -p.ly * d, v = p.v ?? .985;
  const M = new DOMMatrix().translate(ox, oy), S = new Path2D(); S.addPath(Y.P, M); S.addPath(Y.arm, M); if (Y.Wp) S.addPath(Y.Wp, M);
  // gölge kenarı (düz mürekkep), sonra kâğıt kütle; tarama yaması: kanat ve giysi ayrı açıda
  tx.fillStyle = tone(p.shv ?? .02); tx.fill(S);
  px.fillStyle = GR.hatch({ th: PI / 2 + .25 * p.f, id: 9 }); px.fill(S);
  if (Y.Wp) { tx.fillStyle = tone(v * (p.wv ?? .93)); tx.fill(Y.Wp); px.fillStyle = GR.hatch({ th: -1.1 * p.f, id: 6 }); px.fill(Y.Wp); }
  tx.fillStyle = tone(v); tx.fill(Y.P);
  px.fillStyle = GR.hatch({ th: PI / 2 - .1 * p.f, id: 9 }); px.fill(Y.P);
  // kol: gövdenin önünde; gövdeden ince bir gölge çizgisiyle ayrılır (yalnız büyük boyda)
  if (h > 18) { tx.save(); tx.translate(ox * .5, oy * .5); tx.fillStyle = tone(.03); tx.fill(Y.arm); tx.restore(); }
  tx.fillStyle = tone(v); tx.fill(Y.arm);
  // giysi kıvrımları: etekten yukarı giren, sivrilen 1–3 mürekkep vuruşu (gölge yanında)
  if (h > 16) { const q = rng((p.seed || 1) * 7 + 3), sd = (-p.lx * p.f) > 0 ? 1 : -1, nn = h > 30 ? 3 : 2;
    tx.save(); tx.clip(Y.P); tx.fillStyle = tone(.02);
    for (let i = 0; i < nn; i++) { const fx = sd * (.62 - i * (.3 + .1 * q())), L0 = (1.4 + q() * 1.6) * h * Y.k, w0 = Math.max(2.6, h * .09), x0 = p.x + fx * p.f * h, y0 = p.y + 4, bend = (q() - .5) * .3 * h;
      const A = [], B = []; for (let m = 0; m <= 8; m++) { const u = m / 8, cx = x0 + bend * u * u, cy = y0 - L0 * u, hw = Math.max(1.1, w0 * .5 * Math.pow(1 - u, 1.1)); A.push([cx - hw, cy]); B.push([cx + hw, cy]); }
      tx.beginPath(); poly(tx, [...A, ...B.reverse()], true); tx.fill(); }
    tx.restore(); }
  // mızrak: düz mürekkep, ince (≥ 2 px), uçta yaprak biçimli demir
  if (p.spear != null) {
    const a = p.spear, c = Math.sin(a), s = -Math.cos(a), Ls = (p.sl ?? 7.5) * h, w = Math.max(1.15, h * .055), g = Y.hand;
    const b0 = [g[0] - c * Ls * .3, g[1] - s * Ls * .3], t0 = [g[0] + c * Ls * .7, g[1] + s * Ls * .7], n = [-s, c], tl = h * .75;
    const SP = new Path2D(); poly(SP, [[b0[0] + n[0] * w, b0[1] + n[1] * w], [t0[0] + n[0] * w, t0[1] + n[1] * w], [t0[0] + n[0] * w * 2.3 + c * tl * .3, t0[1] + n[1] * w * 2.3 + s * tl * .3], [t0[0] + c * tl, t0[1] + s * tl], [t0[0] - n[0] * w * 2.3 + c * tl * .3, t0[1] - n[1] * w * 2.3 + s * tl * .3], [t0[0] - n[0] * w, t0[1] - n[1] * w], [b0[0] - n[0] * w, b0[1] - n[1] * w]], true);
    tx.fillStyle = tone(0); tx.fill(SP); px.fillStyle = GR.hatch({ th: a - PI / 2, id: 7 }); px.fill(SP);
  }
  return Y;
}
// ── melek safları ──
// Üst üste binen sıralar; uzaklaştıkça küçülür ve soluklaşır (gövde tonu göğe yaklaşır, gölge kenarı incelir), mızrak açısı ve boyu hafif farklı.
// rows: [{y (ayak çizgisi), h, x0, x1, n, facing, gap (düzensizlik), spear (false: yok), spearAng(i, x, t), bow(i, x) (0..1), v, sh, seed, mass}]
// o: {t, L (ışık merkezi)}
function cen_saflar(rows, o = {}) {
  const t = o.t || 0, L = o.L || { x: W / 2, y: -200 };
  for (const R of rows) {
    if (R.mass) { cen_kutle(R, L, t); continue; }
    const q = rng(R.seed || 5), n = R.n, xs = [];
    for (let i = 0; i < n; i++) xs.push(lerp(R.x0, R.x1, (i + .5 + (q() - .5) * (R.gap ?? .7)) / n));
    const F = [];
    for (let i = 0; i < n; i++) {
      const h = R.h * (.9 + q() * .2), x = xs[i], y = R.y + (q() - .5) * R.h * (R.dy ?? .35), fc = R.facing ?? (q() < .5 ? 1 : -1);
      const sa = (q() - .5) * .14, sl = 7 + q() * 1.6, sd = q();
      F.push({ i, h, x, y, fc, sa, sl, sd });
    }
    F.sort((a, b) => a.y - b.y);                              // arkadakiler önce
    for (const G of F) {
      let lx = L.x - G.x, ly = L.y - (G.y - 5 * G.h); { const l = Math.hypot(lx, ly) || 1; lx /= l; ly /= l; }
      cen_melek({ x: G.x, y: G.y, h: G.h, f: G.fc, lx, ly, bow: R.bow ? R.bow(G.i, G.x) : 0, seed: (R.seed || 5) * 31 + G.i, v: R.v, sh: R.sh, shv: R.shv,
        spear: R.spear === false ? null : G.sa + (R.spearAng ? R.spearAng(G.i, G.x, t) : 0), sl: G.sl, wing: R.wing ?? (.6 + .5 * G.sd) });
    }
  }
}
// Uzak saf: tek kütle (başlar dalgalı üst kenar) + mızrak ormanı. Kütle açık gök üstünde orta tonda; mızraklar ince mürekkep.
function cen_kutle(R, L, t) {
  const { tx, tone, fill } = GR, q = rng(R.seed || 9), P = new Path2D(), top = [];
  const h = R.h, y = R.y;
  for (let x = R.x0; x <= R.x1; x += h * .55) top.push([x, y - 6.6 * h + Math.sin(x * .7) * h * .25 + (q() - .5) * h * .5]);
  P.moveTo(R.x0, y);
  for (const p of top) { P.lineTo(p[0] - h * .2, p[1] + h * .4); P.quadraticCurveTo(p[0], p[1] - h * .5, p[0] + h * .2, p[1] + h * .4); }
  P.lineTo(R.x1, y); P.closePath();
  fill(P, tone(R.v ?? .5), { type: 'rad', cx: L.x, cy: L.y, id: 1, ph: .5 });
  // mızrak ormanı
  const n = Math.round((R.x1 - R.x0) / (h * (R.sp ?? .9)));
  tx.save(); tx.fillStyle = tone(0);
  for (let i = 0; i < n; i++) {
    const x = R.x0 + (i + .5 + (q() - .5) * .8) / n * (R.x1 - R.x0), a = (q() - .5) * .12 + (R.spearAng ? R.spearAng(i, x, t) : 0), Ls = h * (9 + q() * 3.5), y0 = y - h * (4 + q() * 1.5);
    const c = Math.sin(a), s = -Math.cos(a), w = Math.max(1.15, h * .07);
    const S = new Path2D(); poly(S, [[x - w, y0], [x + c * Ls - w, y0 + s * Ls], [x + c * (Ls + h * .9), y0 + s * (Ls + h * .9)], [x + c * Ls + w, y0 + s * Ls], [x + w, y0]], true); tx.fill(S);
    GR.px.fillStyle = GR.hatch({ th: a - PI / 2, id: 7 }); GR.px.fill(S);
  }
  tx.restore();
}

// ── başmelek ──
// p: {x, y (kalça), h, facing, lum, L (ışık merkezi), open, lift, armN, armF, head, twist, lean, spear, cloak, t, legs, wing (false: kanat yok), wingSpan}
function cen_basmelek(p) {
  const h = p.h, t = p.t || 0;
  const J = SF.rig({ x: p.x, y: p.y, h, facing: p.facing ?? 1, twist: p.twist ?? .3, lean: p.lean ?? 0, head: p.head ?? .15, shTilt: p.shTilt ?? -.03,
    armN: p.armN || [-.1, .3], armF: p.armF || [.45, .8], legN: p.legN || [.1, -.05], legF: p.legF || [-.08, -.02] });
  let lx = p.L.x - J.shC[0], ly = p.L.y - J.shC[1]; { const l = Math.hypot(lx, ly) || 1; lx /= l; ly /= l; }
  const LIT = p.lit || [lx, ly], lum = p.lum ?? 1, dk = clamp((1 - lum) * 2.2);
  if (p.wing !== false) {
    const S = p.wingSpan ?? 6.6 * h;
    for (const [side, P] of [[-1, { span: S, open: .9, lift: .62, rot: -.12, seed: 11, root: .1 }], [1, { span: S * .92, open: .86, lift: .72, rot: .1, seed: 12, root: .1 }]]) {
      const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
      GR.frame(sh[0] - side * h * .25, sh[1] + h * .12, P.rot + (p.wingRot || 0) * side, side, 1);
      KN.feathered(Object.assign({ dark: dk * .5, rim: .4, ruin: 0, droop: 0, t, lit: [LIT[0] * side, LIT[1]], anchor: p.anchor ?? .55 }, P,
        { open: lerp(P.open, 1, p.open ?? 0) * (p.fold ? 1 - .5 * p.fold : 1), lift: lerp(P.lift, .9, p.lift ?? 0), span: P.span * (p.fold ? 1 - .3 * p.fold : 1) }));
      GR.unframe();
    }
  }
  if (p.mid) p.mid(J);
  const so = { lum, lit: LIT, t, cloak: p.cloak ?? .55, legs: p.legs ?? true, skirt: true, lines: p.lines ?? 0, eye: 0, wind: .5, spear: null, seed: p.seed || 3, armor: p.armor, robe: p.robe, hair: p.hair };
  const sp = p.spear === false ? null : Object.assign({ grip: 'F', ang: .03, len: 7.8, up: .66 }, p.spear || {});
  const spear = () => { const g = J['wr' + sp.grip], a = (sp.ang || 0) * J.f; cen_mizrak(g[0] + J.f * h * .25, g[1] + h * .08, a, sp.len * h, sp.up, Math.max(1.6, h * .05), h); };
  if (sp && sp.grip === 'F') spear();
  if (lum > .6 && p.shade !== false) {   // gölge kenarı: ışığın tersine kaydırılmış düz koyu kopya (açık figürün kontursuz ayrımı)
    const d = (p.shade ?? .13) * h, J2 = SF.rig({ x: p.x - LIT[0] * d, y: p.y - LIT[1] * d, h, facing: p.facing ?? 1, twist: p.twist ?? .3, lean: p.lean ?? 0, head: p.head ?? .15, shTilt: p.shTilt ?? -.03,
      armN: p.armN || [-.1, .3], armF: p.armF || [.45, .8], legN: p.legN || [.1, -.05], legF: p.legF || [-.08, -.02] });
    SF.draw(J2, Object.assign({}, so, { lum: 0, lines: 0, eye: 0, halo: 0 }));
  }
  SF.draw(J, so);
  if (sp && sp.grip !== 'F') spear();
  return J;
}

// Mızrak: düz mürekkep sap, yaprak biçimli demir. (gx, gy) tutulan yer, a dikeyden sapma, L boy, up tutuştan yukarı oranı, w yarı kalınlık
function cen_mizrak(gx, gy, a, L, up, w, h) {
  const { tx, px, tone } = GR, c = Math.sin(a), s = -Math.cos(a), n = [-s, c], tl = h * .8;
  const b0 = [gx - c * L * (1 - up), gy - s * L * (1 - up)], t0 = [gx + c * L * up, gy + s * L * up];
  const SP = new Path2D(); poly(SP, [[b0[0] + n[0] * w, b0[1] + n[1] * w], [t0[0] + n[0] * w, t0[1] + n[1] * w], [t0[0] + n[0] * w * 2.4 + c * tl * .3, t0[1] + n[1] * w * 2.4 + s * tl * .3], [t0[0] + c * tl, t0[1] + s * tl],
    [t0[0] - n[0] * w * 2.4 + c * tl * .3, t0[1] - n[1] * w * 2.4 + s * tl * .3], [t0[0] - n[0] * w, t0[1] - n[1] * w], [b0[0] - n[0] * w, b0[1] - n[1] * w]], true);
  tx.fillStyle = tone(0); tx.fill(SP); px.fillStyle = GR.hatch({ th: a - PI / 2, id: 7 }); px.fill(SP);
}
// Sabah yıldızı: sekiz kollu kâğıt beyazı yıldız; çevresinde kendi küçük eş merkezli halesi (koyu halka taraması, ayırma için)
function cen_yildiz(x, y, r, a = 1) {
  const { tx, px, tone } = GR; if (a <= 0) return;
  const R2 = r * (1.9 + .5 * a), D = new Path2D(); D.arc(x, y, R2, 0, TAU);
  const g = tx.createRadialGradient(x, y, 0, x, y, R2); g.addColorStop(0, tone(.06)); g.addColorStop(.62, tone(.08)); g.addColorStop(.85, tone(.45)); g.addColorStop(1, 'rgba(0,0,0,0)');
  tx.save(); tx.globalAlpha = clamp(a * 1.5); tx.fillStyle = g; tx.fill(D); tx.restore();
  px.fillStyle = GR.hatch({ type: 'rad', cx: x, cy: y, id: 7 }); px.fill(D);
  const S = new Path2D(), n = 8, pts = [];
  for (let i = 0; i < n * 2; i++) { const an = i / (n * 2) * TAU - PI / 2, rr = i % 2 ? r * .2 : (i % 4 === 0 ? r * (1.3 + .5 * a) : r * .8); pts.push([x + Math.cos(an) * rr, y + Math.sin(an) * rr]); }
  poly(S, pts, true); tx.fillStyle = tone(1); tx.fill(S);
}
// İkinci ışık (Oğul): figürsüz kâğıt disk; çevresinde koyulaşan kısa halka taraması (ayrım için). Yüz, el, hale, haç yok.
function cen_isik(x, y, r, a = 1) {
  const { tx, tone } = GR;
  PR.glow(x, y, r, r * 2.6, 1, a * .8);
  const C = new Path2D(); C.arc(x, y, r, 0, TAU); tx.fillStyle = tone(1); tx.fill(C);
}
// Uzak saray: Dor sütunlu, alınlıklı tapınak (kubbe yok). x, y taban ortası; s ölçek (taban genişliği px); lx ışık yanı (±1)
function cen_saray(x, y, s, lx = 1, v = .97) {
  const { tx, px, tone } = GR, u = s / 10, B = new Path2D(), dk = new Path2D();
  B.rect(x - 5 * u, y - .6 * u, 10 * u, .6 * u); B.rect(x - 4.6 * u, y - 1 * u, 9.2 * u, .4 * u);              // basamaklar
  B.rect(x - 4.3 * u, y - 5.4 * u, 8.6 * u, .8 * u);                                                        // arşitrav
  B.moveTo(x - 4.7 * u, y - 5.4 * u); B.lineTo(x, y - 7.3 * u); B.lineTo(x + 4.7 * u, y - 5.4 * u); B.closePath(); // alınlık
  for (let i = 0; i < 6; i++) { const cx = x - 3.8 * u + i * 1.52 * u; B.rect(cx - .32 * u, y - 4.6 * u, .64 * u, 3.6 * u); }
  dk.rect(x - 4.3 * u, y - 4.6 * u, 8.6 * u, 3.6 * u);                                                       // sütun arası gölge
  tx.fillStyle = tone(.08); tx.fill(dk); px.fillStyle = GR.hatch({ th: 0, id: 9 }); px.fill(dk);
  tx.save(); tx.translate(-lx * u * .25, u * .1); tx.fillStyle = tone(.03); tx.fill(B); tx.restore();
  tx.fillStyle = tone(v); tx.fill(B); px.fillStyle = GR.hatch({ th: PI / 2, id: 9 }); px.fill(B);
}
// Açık levhada yazı: arkasında yumuşak kâğıt zemin, mürekkep rengi harf (over katmanında)
function cen_yazi(ctx, s, x, y, a, o = {}) {
  if (NOTEXT || !s || a <= 0) return;
  const px_ = o.px || 56; ctx.save(); ctx.font = o.font || FONT.baslik(px_, 600); if (o.ls) ctx.letterSpacing = o.ls + 'px';
  const wd = ctx.measureText(s).width; ctx.restore();
  const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 1); g.addColorStop(0, `rgba(${GR.PAPER},${.92 * a})`); g.addColorStop(.6, `rgba(${GR.PAPER},${.85 * a})`); g.addColorStop(1, `rgba(${GR.PAPER},0)`);
  ctx.save(); ctx.translate(x, y); ctx.scale(wd * .5 + px_ * 1.4, px_ * 1.25); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 1, 0, TAU); ctx.fill(); ctx.restore();
  txt(ctx, s, x, y, { px: px_, font: o.font || FONT.baslik(px_, 600), ls: o.ls ?? 6, a, col: INK_CSS });
}
// ── kaba eskiz uyumu: cizCennet(t, o) = C02 levhası ──
function cizCennet(t, o = {}) { return cen_c02(t, o); }
function sahneCennet(t, o = {}) { GR.begin(.9, 0, 1, o.cam); cizCennet(t, o); GR.engrave(o.out || ctx); applyPaper(o.out || ctx, .8); applyVignette(o.out || ctx, .25); }
