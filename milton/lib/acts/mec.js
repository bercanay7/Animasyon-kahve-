// mec grubu (MEC: Pandemonium'un içi): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Set: içi altın ışıkla yanan devasa Dor tapınağı (I.713–730). Tek kaçış noktalı iç mekân; iki yanda kalın yivli Dor sütun sıraları,
// karanlık kasetli tavan, tavandan sarkan yıldız gibi kandiller, derinlikte yüksek basamaklı taht ve arkasında tek büyük parıltı (odak),
// zeminde perspektifli tarama ve koridor boyunca parıltının yansıması. Kalabalık: baş-omuz yumrulu koyu KÜTLELER (tek tek figür dizisi değil).
// Kubbe, minare, hilal, sarık, yazı, Osmanlı motifi YOK; taht düz, yüksek arkalıklı, süssüz.
// Dünya: X yana, Y aşağı (zemin Y = 500), z derinlik (kameradan uzaklık). Ekran = kaçış noktası + K · (X, Y) / z.
// K yakınlıktır (odak uzaklığı): geniş plan 1.25, orta plan 3.0. Çizgi kalınlıkları ekran pikselidir (ölçekle büyümez).
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const mec_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));
const MW = { FL: 500, SH: 262, COLX: 650, CR: 60, CTOP: -470, ENT: -610, BZ: 3.95, DZ0: 3.0, DTOP: 200, TZ: 3.72, AIS: 135, CRX: 545, DW: 575 };
const MEC_COLZ = [1.04, 1.38, 1.72, 2.06, 2.4, 2.74, 3.15, 3.55];
let MEC = { K: 1.25, vx: 960, vy: 470 };
const mec_P = (X, Y, z) => [MEC.vx + MEC.K * X / z, MEC.vy + MEC.K * Y / z];
const mec_k = z => MEC.K / z;
// kapalı çokgeni ekranda saat yönüne çevir (birleşik yollar 'nonzero' ile deliksiz dolsun)
function mec_yon(pts) { let a = 0; for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; a += p[0] * q[1] - q[0] * p[1]; } return a < 0 ? pts.slice().reverse() : pts; }
function mec_cok(P, pts, sp = 0) { const q = mec_yon(pts); if (sp) spline(P, q, true, sp); else poly(P, q, true); return P; }
const mec_vurus = (pts, w, v = .95, uc = .55) => gol_vurus(GR.tx, pts, w, v, uc);

// ── kalabalık: sıralar (sol ve sağ blok), her sırada düzensiz aralıklı baş-omuz yumruları ──
const MEC_SAF = (() => {
  const r = rng(913), rows = [];
  for (let z = 2.86; z >= .96; z -= .135) for (const sd of [-1, 1]) {
    const F = []; let X = MW.AIS + r() * 30;
    while (X < MW.CRX) { const hs = .86 + r() * .3; F.push({ X: sd * X, dy: (r() - .5) * 14, hs, w: r() < .22 ? (r() < .5 ? -1 : 1) : 0, sp: r() < .1, ph: r() * TAU, dl: r(), bd: r() < .5 ? -1 : 1 }); X += 36 * hs * (.6 + r() * .75); }
    if (sd < 0) F.reverse();
    rows.push({ z: z + (r() - .5) * .03, sd, F });
  }
  return rows;
})();
// tek baş-omuz: b eğilme (0..1), n boyun uzaması (0..1), bend boynun kıvrılma yönü ve miktarı
function mec_bust(P, x, y, k, b, n, bend) {
  const sw = .62 * k * (1 - .32 * n), sy = y - 2.85 * k + b * .14 * k;
  P.moveTo(x + sw, sy); P.ellipse(x, sy, sw, .3 * k, 0, 0, TAU);
  // boyun: omuzdan başa bir tüp; başın merkezi boyun uzadıkça yükselir ve yana kıvrılır, baş yılan başı gibi uzar ve yataylaşır
  const L = (.62 + 2.5 * n) * k, b0 = [x, sy - .1 * k], hx = x + bend * n * 1.1 * k, hy = sy - L + b * .62 * k * (1 - n);
  const c = [x + bend * n * .2 * k - bend * n * .7 * k, (b0[1] + hy) / 2], A = [], B = [], m = 6, wn = .17 * k * (1 - .15 * n);
  const Q = u => [(1 - u) * (1 - u) * b0[0] + 2 * u * (1 - u) * c[0] + u * u * hx, (1 - u) * (1 - u) * b0[1] + 2 * u * (1 - u) * c[1] + u * u * hy];
  for (let i = 0; i <= m; i++) { const u = i / m, p = Q(u), q = Q(Math.min(1, u + .05)), p0 = Q(Math.max(0, u - .05)), dx = q[0] - p0[0], dy = q[1] - p0[1], l = Math.hypot(dx, dy) || 1; A.push([p[0] - dy / l * wn, p[1] + dx / l * wn]); B.push([p[0] + dy / l * wn, p[1] - dx / l * wn]); }
  if (n > .01) mec_cok(P, [...A, ...B.reverse()]);
  const an = lerp(-PI / 2, bend > 0 ? -.35 : -PI + .35, E.io2(n)), rx = .3 * k * (1 + .55 * n), ry = .3 * k * (1 - .28 * n);
  P.moveTo(hx + Math.cos(an) * rx, hy + Math.sin(an) * rx); P.ellipse(hx, hy, rx, ry, an, 0, TAU);
}
// bir sıranın yolu. st(f) → {b, n, bend, cheer}; still: hareket yok
function mec_sira(R, st) {
  const P = new Path2D(), k0 = mec_k(R.z) * 36, F = R.F;
  const xs = F.map(f => mec_P(f.X, 0, R.z)[0]), yb = mec_P(0, MW.SH, R.z)[1];
  const x0 = Math.min(xs[0], xs[xs.length - 1]) - k0 * .7, x1 = Math.max(xs[0], xs[xs.length - 1]) + k0 * .7;
  P.rect(x0, yb - 2.8 * k0, x1 - x0, R.z < 1.2 ? H : 3.6 * k0);
  F.forEach((f, i) => {
    const s = st(f), k = k0 * f.hs, x = xs[i], y = yb + f.dy * mec_k(R.z) - (s.cheer || 0) * k * .3;
    mec_bust(P, x, y, k, s.b || 0, s.n || 0, (s.bend || 0));
    const fade = 1 - clamp((s.n || 0) * 1.6) - clamp((s.b || 0) * .6);
    if (f.w && fade > .05) { const sd = f.w, sy = y - 2.85 * k; mec_cok(P, [[x + sd * .25 * k, sy - .1 * k], [x + sd * .52 * k, sy - 1.6 * k * fade], [x + sd * .78 * k, sy - .85 * k * fade], [x + sd * .66 * k, sy + .05 * k]]); }
    if (f.sp && fade > .05) { const sx = x + .5 * k, top = y - (5.6 + (s.cheer || 0) * .8) * k * fade - 2.4 * k * (1 - fade), w = Math.max(2.2, .08 * k); P.rect(sx - w / 2, top, w, y - 2.8 * k - top); mec_cok(P, [[sx, top - .5 * k], [sx + .14 * k, top + .05 * k], [sx - .14 * k, top + .05 * k]]); }
  });
  return P;
}
function mec_siraCiz(R, st, lt) {
  const { tx, tone } = GR, P = mec_sira(R, st);
  const v = lerp(.3, .02, clamp((2.95 - R.z) / 1.25)), rim = .35 + .65 * clamp((R.z - 1.2) / 1.5);
  if (rim * lt > .05) { tx.save(); tx.translate(0, -2.6); tx.fillStyle = tone(.95 * rim * lt + .03); tx.fill(P); tx.restore(); }
  GR.fill(P, tone(v), { th: 0, id: 8 });
}
// ── yılan sırası (J08): her sırada birkaç yatay, dalgalı yılan gövdesi; biri başını kaldırır ──
function mec_yilanSira(R, t, o = {}) {
  const P = new Path2D(), k0 = mec_k(R.z) * 36, yb = mec_P(0, MW.SH, R.z)[1] - 1.2 * k0, r = rng(Math.round(R.z * 1000) + (R.sd > 0 ? 7 : 0));
  const xa = mec_P(R.sd * MW.AIS, 0, R.z)[0], xb = mec_P(R.sd * MW.CRX, 0, R.z)[0], lo = Math.min(xa, xb), hi = Math.max(xa, xb);
  P.rect(lo - k0, yb + .45 * k0, hi - lo + 2 * k0, 12 * k0 + 400);                      // sıranın gövdesi: yatay, koyu kütle
  const n = 2 + (r() < .5 ? 1 : 0);
  for (let j = 0; j < n; j++) {
    const a = lo + (hi - lo) * (j / n + r() * .12 - .04), b = a + (hi - lo) * (.55 + r() * .25), ph = r() * TAU, dir = r() < .5 ? -1 : 1, up = (o.reach || 0) * (r() < .45 ? 1 : 0);
    const A = [], B = [], m = 26, sp = .55 + r() * .3;
    for (let i = 0; i <= m; i++) {
      const u = i / m, x = lerp(a, b, u), hu = dir > 0 ? u : 1 - u;                        // hu: kuyruktan (0) başa (1)
      const yy = yb + Math.sin(u * TAU * sp * 2 + ph + t * .45) * .38 * k0 - (Math.pow(clamp((hu - .82) / .18), 2) * (.9 + 1.6 * up)) * k0;
      const w = k0 * .34 * Math.min(1, Math.pow(hu / .4, .8)) * (hu > .93 ? .82 : 1);
      A.push([x, yy - w]); B.push([x, yy + w]);
    }
    mec_cok(P, [...A, ...B.reverse()], .8);
    const hi2 = dir > 0 ? A[m] : A[0], hb = dir > 0 ? B[m] : B[0], hx = (hi2[0] + hb[0]) / 2 + dir * .25 * k0, hy = (hi2[1] + hb[1]) / 2;
    P.moveTo(hx + dir * .5 * k0, hy); P.ellipse(hx, hy, .5 * k0, .27 * k0, 0, 0, TAU);
  }
  return P;
}

// ── taht: düz, yüksek arkalıklı, kollu; süssüz ──
function mec_taht(z) {
  const Y0 = MW.DTOP, P = new Path2D(), p = (X, Y) => mec_P(X, Y, z);
  mec_cok(P, [p(-118, Y0), p(-118, Y0 - 120), p(-138, Y0 - 120), p(-138, Y0 - 172), p(-104, Y0 - 172), p(-104, Y0 - 560), p(-118, Y0 - 585), p(118, Y0 - 585), p(104, Y0 - 560), p(104, Y0 - 172), p(138, Y0 - 172), p(138, Y0 - 120), p(118, Y0 - 120), p(118, Y0)]);
  return P;
}
// ── sütun (Dor): tabansız gövde, hafif şişkinlik, yuvarlak başlık (echinus) ve kare abakus ──
function mec_sutun(X, z, lt) {
  const { tx, tone } = GR, k = mec_k(z), [x, yb] = mec_P(X, MW.FL, z), yt = mec_P(X, MW.CTOP, z)[1], r0 = MW.CR * k, r1 = .8 * r0, P = new Path2D();
  if (x + r0 * 1.4 < -60 || x - r0 * 1.4 > W + 60) return;
  const ye = yt + 34 * k;
  P.moveTo(x - r0, yb); P.quadraticCurveTo(x - r0 * 1.06, (yb + ye) / 2, x - r1, ye); P.lineTo(x + r1, ye); P.quadraticCurveTo(x + r0 * 1.06, (yb + ye) / 2, x + r0, yb); P.closePath();
  P.moveTo(x - r1, ye); P.quadraticCurveTo(x - r0 * 1.2, ye - 4 * k, x - r0 * 1.22, yt + 16 * k); P.lineTo(x + r0 * 1.22, yt + 16 * k); P.quadraticCurveTo(x + r0 * 1.2, ye - 4 * k, x + r1, ye); P.closePath();
  P.rect(x - r0 * 1.3, yt - 2, r0 * 2.6, 18 * k + 2);
  const sd0 = X < 0 ? 1 : -1, Lc = lt * clamp(.3 + .7 * (z - .9) / 2.6), g = GR.tx.createLinearGradient(x + sd0 * r0, 0, x - sd0 * r0, 0);
  g.addColorStop(0, tone(.025 + .62 * Lc)); g.addColorStop(.18, tone(.025 + .42 * Lc)); g.addColorStop(.5, tone(.025)); g.addColorStop(1, tone(.025));
  GR.fill(P, g, { th: -PI / 2, id: 9, anchor: [x, yb] });
  // ışık koridor yanından (iç yüz): kenar ışığı + kütlenin içine giren, uzunluğu düzensiz yiv vuruşları
  const sd = X < 0 ? 1 : -1, r = rng(Math.round(z * 100) + (X < 0 ? 0 : 50)), L = lt * clamp(.35 + .65 * (z - .9) / 2.6);
  if (L < .05) return;
  tx.save(); tx.clip(P);
  const w0 = Math.max(3, 7 * Math.sqrt(k) * L);
  mec_vurus([[x + sd * (r0 - 3), yb - 4], [x + sd * (r0 * 1.03 - 3), (yb + ye) / 2], [x + sd * (r1 - 3), ye + 2]], w0, .96, .12);
  mec_vurus([[x + sd * (r0 * 1.2 - 3), yt + 18 * k], [x + sd * r0 * .3, yt + 20 * k]], Math.max(3, 5 * Math.sqrt(k)), .95, .3);   // echinus alt kenarı
  for (let i = 0; i < 3; i++) {
    const f = .45 + i * .2 + (r() - .5) * .06, len = (.25 + r() * .55) * (yb - ye) * L, y0 = ye + (yb - ye) * (r() * .5) + 10;
    const xx = x + sd * r0 * f;
    mec_vurus([[xx, y0], [xx + sd * .02 * r0, y0 + len * .5], [xx, y0 + len]], Math.max(2.6, 5.5 * Math.sqrt(k) * (1 - .25 * i)), .93, .8);
  }
  tx.restore();
}
// ── kandil: tavandan ince zincirle sarkan küçük ışık (temiz kâğıt leke) ──
function mec_kandil(X, Y, z, lt) {
  const { tx, tone } = GR, k = mec_k(z), [x, y] = mec_P(X, Y, z), [, yc] = mec_P(X, MW.ENT + 30, z), r = Math.max(4, 13 * k);
  tx.fillStyle = tone(.03); tx.fillRect(x - Math.max(1, 1.4 * k), yc, Math.max(2, 2.8 * k), y - yc - r * .6);
  const P = new Path2D(); P.ellipse(x, y, r * .75, r, 0, 0, TAU); tx.fillStyle = tone(.4 + .6 * lt); tx.fill(P);
}

// ── salon ──
// o: {K, vx, vy, lt (genel ışık: kandiller ve kenarlar, 0..1), glow (taht parıltısı 0..1+), gx, gy (parıltı merkezi ekranda; verilmezse tahtın arkası),
//     crowd: (f, R) => {b, n, bend, cheer} | 'yilan' | null, zmin (bu derinlikten yakın sıralar çizilmez), zmax,
//     fig: (z) => {} (dais üstünde çizilecek figür; derinlik sıralamasında MW.TZ - .3), figZ, aisle: [{z, draw}] (koridorda çizilecekler),
//     front: () => {} (en önde), trees, t}
function mec_salon(t, o = {}) {
  const { tx, tone } = GR;
  MEC = { K: o.K ?? 1.25, vx: o.vx ?? 960, vy: o.vy ?? 470 };
  const lt = o.lt ?? 1, gl = o.glow ?? 1, BZ = MW.BZ;
  // arka plan: zifiri
  tx.fillStyle = tone(.025); tx.fillRect(-400, -400, W + 800, H + 800);
  // arka duvar: tahtın arkasında altın ışık (tek büyük parıltı; odak)
  const bw = MW.COLX - MW.CR, [bx0, by0] = mec_P(-bw, MW.ENT, BZ), [bx1, by1] = mec_P(bw, MW.FL, BZ);
  const back = new Path2D(); back.rect(bx0, by0, bx1 - bx0, by1 - by0);
  GR.fill(back, tone(.04), { th: 0, id: 1 });
  const [tgx, tgy] = mec_P(0, MW.DTOP - 330, MW.TZ), gx = o.gx ?? tgx, gy = o.gy ?? tgy, gk = MEC.K / 1.25;
  if (gl > .01) {
    tx.save(); tx.clip(back);
    PR.glow(gx, gy, 20 * gk, 330 * gk * Math.sqrt(gl), 1, Math.min(1, gl));
    PR.glow(gx, gy, 10 * gk, 150 * gk * Math.sqrt(gl), 1, Math.min(1, gl));
    tx.restore();
  }
  // arka duvarın iki köşesinde koyu payeler
  for (const sd of [-1, 1]) { const P = new Path2D(), a = mec_P(sd * bw, MW.ENT, BZ), b = mec_P(sd * (bw - 120), MW.FL, BZ); P.rect(Math.min(a[0], b[0]), a[1], Math.abs(b[0] - a[0]), b[1] - a[1]); GR.fill(P, tone(.03), { th: -PI / 2, id: 9 }); }
  // zemin: perspektifli tarama, tahta yakın yerde parıltının yansıması
  { const yb = mec_P(0, MW.FL, BZ)[1], G = new Path2D(); G.rect(-400, yb, W + 800, H + 600 - yb);
    const g = tx.createRadialGradient(MEC.vx, yb, 0, MEC.vx, yb, 520 * gk); g.addColorStop(0, tone(.1 + .42 * Math.min(1, gl) * lt)); g.addColorStop(.3, tone(.05 + .14 * gl * lt)); g.addColorStop(.75, tone(.03 + .05 * gl * lt)); g.addColorStop(1, tone(.025));
    GR.fill(G, g, { type: 'persp', y0: yb, D: 420, p0: 9.5, p1: 12.5, id: 8 });
    // koridor boyunca yansıma: parlak cilalı zeminde uçları sivrilen yatay kâğıt çizgiler (uzakta uzun ve sık, yakında kısa ve seyrek)
    const q = rng(41); tx.save(); tx.clip(G);
    for (let i = 0; i < 9; i++) { const z = BZ - .08 - i * i * .045 - q() * .03; if (z < 1.1) break; const [x, y] = mec_P((q() - .5) * 40, MW.FL, z), L = mec_k(z) * (150 + q() * 110) * Math.min(1, gl + .15) * (1 - i * .07);
      if (L > 6) mec_vurus([[x - L, y], [x, y + 1], [x + L, y]], Math.max(3, 9 - i * .6), .97, .5); }
    tx.restore(); }
  // saçaklık: iki yanda sütunların üstünde koyu bant, alt kenarında ışık
  for (const sd of [-1, 1]) { const X = sd * (MW.COLX - MW.CR * 1.3), a = mec_P(X, MW.ENT, .9), b = mec_P(X, MW.ENT, BZ), c = mec_P(X, MW.CTOP, BZ), d = mec_P(X, MW.CTOP, .9), P = new Path2D(); mec_cok(P, [a, b, c, d]);
    GR.fill(P, tone(.03), { th: 0, id: 9 });
    tx.save(); tx.clip(P); mec_vurus([[lerp(d[0], c[0], .35), lerp(d[1], c[1], .35) - 3], [c[0], c[1] - 2]], 4.5 * lt, .9, .5); tx.restore(); }
  // kandiller: iki sıra, uzaklaştıkça küçülür
  if (o.lamps !== false) for (const X of [-330, 330]) for (const z of [1.55, 1.95, 2.35, 2.75, 3.15, 3.55]) mec_kandil(X, -300 - (z * 23 % 40), z, lt);
  // derinlik sıralı çizimler: kürsü+taht, figür, sütunlar, kalabalık sıraları, koridordakiler
  const L = [];
  L.push({ z: MW.TZ + .05, d: () => mec_kursu(o) });
  if (o.fig) L.push({ z: o.figZ ?? MW.TZ - .3, d: () => o.fig() });
  for (const z of MEC_COLZ) for (const sd of [-1, 1]) L.push({ z, d: () => mec_sutun(sd * MW.COLX, z, lt) });
  if (o.crowd) for (const R of MEC_SAF) { if (R.z < (o.zmin ?? 1.1) || R.z > (o.zmax ?? 9)) continue;
    L.push({ z: R.z, d: () => { if (o.crowd === 'yilan') { const P = mec_yilanSira(R, t, o); const { tx: T } = GR; T.save(); T.translate(0, -Math.max(2.2, 3.4 * mec_k(R.z))); T.fillStyle = tone(.85 * lt + .05); T.fill(P); T.restore(); GR.fill(P, tone(lerp(.28, .02, clamp((2.95 - R.z) / 1.25))), { th: 0, id: 8 }); } else mec_siraCiz(R, f => o.crowd(f, R), lt); } }); }
  for (const a of (o.aisle || [])) L.push(a);
  L.sort((a, b) => b.z - a.z);
  for (const e of L) e.d();
  if (o.front) o.front();
}
// kürsü (6 yüksek basamak) ve taht
function mec_kursu(o) {
  const { tx, tone } = GR, n = 6, dz = (MW.BZ - MW.DZ0) / (n + 1.5), lt = o.lt ?? 1, gl = Math.min(1, o.glow ?? 1);
  for (let i = n - 1; i >= 0; i--) {
    const z0 = MW.DZ0 + i * dz, z1 = i === n - 1 ? MW.BZ : z0 + dz, Yt = MW.FL - (i + 1) * (MW.FL - MW.DTOP) / n, Yb = Yt + (MW.FL - MW.DTOP) / n, D = MW.DW;
    const top = new Path2D(); mec_cok(top, [mec_P(-D, Yt, z0), mec_P(D, Yt, z0), mec_P(D, Yt, z1), mec_P(-D, Yt, z1)]);
    const tv = (.16 + .5 * gl * lt) * (.55 + .45 * i / (n - 1));
    GR.fill(top, tone(tv), { th: 0, id: 8 });
    const fr = new Path2D(); mec_cok(fr, [mec_P(-D, Yt, z0), mec_P(D, Yt, z0), mec_P(D, Yb, z0), mec_P(-D, Yb, z0)]);
    GR.fill(fr, tone(.025), { th: 0, id: 4 });
    const a = mec_P(-D, Yt, z0), b = mec_P(D, Yt, z0);
    tx.save(); tx.clip(fr); mec_vurus([[a[0] + 10, a[1] + 2], [(a[0] + b[0]) / 2, a[1] + 3], [b[0] - 10, b[1] + 2]], Math.max(3, 6 * Math.sqrt(mec_k(z0))) * (.4 + .6 * gl * lt), .95, .1); tx.restore();
  }
  if (o.taht === false) return;
  const T = mec_taht(MW.TZ), w = Math.max(3, 5 * Math.sqrt(mec_k(MW.TZ)));
  tx.save(); tx.lineWidth = w * 1.6; tx.lineJoin = 'round'; tx.strokeStyle = tone(.9 * clamp(gl * 1.4) * lt + .03); tx.stroke(T); tx.restore();   // ışık halesi
  GR.fill(T, tone(.02), { th: -PI / 2, id: 9 });
  if (o.thrFig) o.thrFig();
}
// Şeytan kürsüde: dünya konumundan kiy_seytan'a (gol.js) çevirir. p: {X, z, Y (ayak hizası; varsayılan kürsü üstü), hw (dünya baş boyu), ...kiy_seytan seçenekleri}
function mec_seytan(t, p) {
  const z = p.z ?? MW.TZ - .3, [x, gy] = mec_P(p.X ?? 0, p.Y ?? MW.DTOP, z), h = (p.hw ?? 62) * mec_k(z);
  return kiy_seytan(t, Object.assign({ wingK: .85, lum: .25, cloak: 1.2, lit: [.2, -.98] }, p, { x, gy: gy + (p.dy || 0) * h, h }));
}

// tahtta oturan Şeytan (¾ dönük; kanatlar kapalı, pelerinli). Oturuş: uyluk öne, baldır aşağı
const MEC_OTUR = (t, tK) => ({ X: 0, z: MW.TZ - .22, dy: -1.9, twist: .45, legN: [1.45, -1.45], legF: [1.3, -1.35], armN: [.6 + .25 * E.sine(mec_u(t, tK - .4, tK + .8)), -.4], armF: [.4, -.2], head: .05, lum: .22, cloak: 1.3, wings: false });
// ═════════ E13 (P053): meclis; ortada yeni dünyanın küçük küresi ═════════
function mec_kure(x, y, R, a) {
  if (a <= .01) return;
  const { tx, tone } = GR, r = R * E.out3(a);
  PR.glow(x, y, r, r * 1.5, 1, .5 * a);
  // dolu, parlak küre (hilal okunmasın diye gölge yok); üstünde iki mürekkep çizgi: eğik eksenli bir meridyen ve bir enlem
  const P = new Path2D(); P.arc(x, y, r, 0, TAU); tx.fillStyle = tone(.98); tx.fill(P);
  if (r > 8) { tx.save(); tx.clip(P);
    const m = [], q = []; for (let i = 0; i <= 10; i++) { const u = -PI / 2 + PI * i / 10; m.push([x + Math.sin(u + PI / 2) * 0 + Math.cos(u) * r * .45 - r * .1, y + Math.sin(u) * r]); q.push([x + Math.sin(u) * r, y + r * .28 + Math.cos(u) * r * .16]); }
    gol_vurus(tx, m, Math.max(2.4, r * .1), .05, .3); gol_vurus(tx, q, Math.max(2.4, r * .09), .05, .3);
    tx.restore(); }
}
plan('P053', (ctx, st) => {
  const t = st.t, tD = Wd('E13', 'dünyaya'), tK = Wd('E13', 'kabul');
  const cam = camLerp({ cx: 990, cy: 540, z: 1 }, { cx: 930, cy: 540, z: 1 }, st.p, E.sine);
  const ka = E.io2(mec_u(t, tD - .4, tD + 1.2));
  levha(ctx, cam, () => mec_salon(t, { glow: lerp(1, .8, ka), crowd: f => ({ b: .08 * Math.sin(t * .4 + f.ph) * 0, bend: 0 }),
    fig: () => mec_seytan(t, MEC_OTUR(t, tK)), figZ: MW.TZ - .02,
    aisle: [{ z: 2.0, d: () => { const [x, y] = mec_P(0, -430, 2.0); mec_kure(x, y, 34, ka); } }] }));
}, { tr: { type: 'fade', dur: .9 } });
