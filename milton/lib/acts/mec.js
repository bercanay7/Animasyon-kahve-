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
const MW = { FL: 700, SH: 462, COLX: 650, CR: 60, CTOP: -470, ENT: -610, BZ: 3.95, DZ0: 2.7, DTOP: 400, TZ: 3.72, AIS: 135, CRX: 545, DW: 575 };
const MEC_COLZ = [1.04, 1.38, 1.72, 2.06, 2.4, 2.74, 3.15, 3.55];
let MEC = { K: 1.25, vx: 960, vy: 470, zc: 0 };
// zc: kameranın salona doğru ilerlemesi (orta plan = kamera kürsüye yaklaşır; arkasında kalan sütun ve sıralar çizilmez)
const mec_P = (X, Y, z) => [MEC.vx + MEC.K * X / (z - MEC.zc), MEC.vy + MEC.K * Y / (z - MEC.zc)];
const mec_k = z => MEC.K / (z - MEC.zc);
const mec_on = z => z - MEC.zc > .32;
// kapalı çokgeni ekranda saat yönüne çevir (birleşik yollar 'nonzero' ile deliksiz dolsun)
function mec_yon(pts) { let a = 0; for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; a += p[0] * q[1] - q[0] * p[1]; } return a < 0 ? pts.slice().reverse() : pts; }
function mec_cok(P, pts, sp = 0) { const q = mec_yon(pts); if (sp) spline(P, q, true, sp); else poly(P, q, true); return P; }
const mec_vurus = (pts, w, v = .95, uc = .55) => gol_vurus(GR.tx, pts, w, v, uc);

// ── kalabalık: sıralar (sol ve sağ blok), her sırada düzensiz aralıklı baş-omuz yumruları ──
const MEC_SAF = (() => {
  const r = rng(913), rows = [];
  for (let z = 2.58; z >= .96; z -= .125) for (const sd of [-1, 1]) {
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
  P.rect(x0, yb - 2.8 * k0, x1 - x0, R.z - MEC.zc < (MEC.zc ? .62 : 1.2) ? H : 3.6 * k0);
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
  const ze = R.z - MEC.zc, v = lerp(.24, .02, clamp((2.7 - ze) / 1.4)), rim = .5 + .5 * clamp((ze - 1.2) / 1.4);
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
  const Y0 = MW.DTOP, P = new Path2D(), p = (X, Y) => mec_P(X, Y, z), r = (x0, y0, x1, y1) => mec_cok(P, [p(x0, y0), p(x1, y0), p(x1, y1), p(x0, y1)]);
  mec_cok(P, [p(-96, Y0 - 150), p(-96, Y0 - 540), p(-112, Y0 - 552), p(-104, Y0 - 572), p(104, Y0 - 572), p(112, Y0 - 552), p(96, Y0 - 540), p(96, Y0 - 150)]);   // arkalık
  r(-130, Y0 - 168, 130, Y0 - 118);                                                       // oturak
  r(-140, Y0 - 250, -112, Y0 - 118); r(112, Y0 - 250, 140, Y0 - 118);                     // kol dayanakları
  r(-136, Y0 - 120, -112, Y0); r(112, Y0 - 120, 136, Y0);                                 // ön ayaklar (araları açık: altından ışık görünür)
  for (const sd of [-1, 1]) { const c = p(sd * 104, Y0 - 588), rr = 16 * mec_k(z); P.moveTo(c[0] + rr, c[1]); P.arc(c[0], c[1], rr, 0, TAU); }   // tepe topuzları
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
  g.addColorStop(0, tone(.025 + .8 * Lc)); g.addColorStop(.3, tone(.025 + .5 * Lc)); g.addColorStop(.5, tone(.025)); g.addColorStop(1, tone(.025));
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
  MEC = { K: o.K ?? 1.25, vx: o.vx ?? 960, vy: o.vy ?? 470, zc: o.zc ?? 0 };
  const lt = o.lt ?? 1, gl = o.glow ?? 1, BZ = MW.BZ;
  // arka plan: zifiri
  tx.fillStyle = tone(.025); tx.fillRect(-400, -400, W + 800, H + 800);
  // arka duvar: tahtın arkasında altın ışık (tek büyük parıltı; odak)
  const bw = MW.COLX - MW.CR, [bx0, by0] = mec_P(-bw, MW.ENT, BZ), [bx1, by1] = mec_P(bw, MW.FL, BZ);
  const back = new Path2D(); back.rect(bx0, by0, bx1 - bx0, by1 - by0);
  GR.fill(back, tone(.04), { th: 0, id: 1 });
  const [tgx, tgy] = mec_P(0, MW.DTOP - 330, MW.TZ), gx = o.gx ?? tgx, gy = o.gy ?? tgy, gk = MEC.K / 1.25;
  if (gl > .01) {
    const gR = o.gR ?? 560 * gk;
    tx.save(); if (o.gClip !== false) tx.clip(back);
    PR.glow(gx, gy, 20 * gk, gR * Math.sqrt(gl), 1, Math.min(1, gl));
    PR.glow(gx, gy, 10 * gk, gR * .45 * Math.sqrt(gl), 1, Math.min(1, gl));
    tx.restore();
  }
  // arka duvarın iki köşesinde koyu payeler
  for (const sd of [-1, 1]) { const P = new Path2D(), a = mec_P(sd * bw, MW.ENT, BZ), b = mec_P(sd * (bw - 120), MW.FL, BZ); P.rect(Math.min(a[0], b[0]), a[1], Math.abs(b[0] - a[0]), b[1] - a[1]); GR.fill(P, tone(.03), { th: -PI / 2, id: 9 }); }
  // zemin: perspektifli tarama, tahta yakın yerde parıltının yansıması
  { const yb = mec_P(0, MW.FL, BZ)[1], G = new Path2D(); G.rect(-400, yb, W + 800, H + 600 - yb);
    const g = tx.createRadialGradient(MEC.vx, yb, 0, MEC.vx, yb, 900 * gk); g.addColorStop(0, tone(.1 + .42 * Math.min(1, gl) * lt)); g.addColorStop(.3, tone(.05 + .14 * gl * lt)); g.addColorStop(.75, tone(.03 + .05 * gl * lt)); g.addColorStop(1, tone(.025));
    GR.fill(G, g, { type: 'persp', y0: yb, D: 420, p0: 9.5, p1: 12.5, id: 8 });
    // koridor boyunca yansıma: parlak cilalı zeminde uçları sivrilen yatay kâğıt çizgiler (uzakta uzun ve sık, yakında kısa ve seyrek)
    const q = rng(41); tx.save(); tx.clip(G);
    for (let i = 0; i < 9; i++) { const z = BZ - .08 - i * i * .045 - q() * .03; if (z - MEC.zc < .9) break; const [x, y] = mec_P((q() - .5) * 40, MW.FL, z), L = mec_k(z) * (150 + q() * 110) * Math.min(1, gl + .15) * (1 - i * .07);
      if (L > 6) mec_vurus([[x - L, y], [x, y + 1], [x + L, y]], Math.max(3, 9 - i * .6), .97, .5); }
    tx.restore();
    // koridorda düz kâğıt şerit (cilalı zeminde parıltının yansıması): kürsüden kameraya doğru genişler ve söner; tarama alanı büyümez
    if (o.serit) { const a = mec_P(-70, MW.FL, MW.DZ0), b = mec_P(70, MW.FL, MW.DZ0), zn = MEC.zc + .55, c = mec_P(150, MW.FL, zn), d = mec_P(-150, MW.FL, zn), S = new Path2D(); mec_cok(S, [a, b, c, d]);
      const gg = tx.createLinearGradient(0, a[1], 0, c[1]); gg.addColorStop(0, tone(.98 * o.serit)); gg.addColorStop(.55, tone(.95 * o.serit)); gg.addColorStop(1, tone(.04)); GR.fill(S, gg, { th: 0, id: 8 }); } }
  // saçaklık: iki yanda sütunların üstünde koyu bant, alt kenarında ışık
  for (const sd of [-1, 1]) { const X = sd * (MW.COLX - MW.CR * 1.3), a = mec_P(X, MW.ENT, MEC.zc + .5), b = mec_P(X, MW.ENT, BZ), c = mec_P(X, MW.CTOP, BZ), d = mec_P(X, MW.CTOP, MEC.zc + .5), P = new Path2D(); mec_cok(P, [a, b, c, d]);
    GR.fill(P, tone(.03), { th: 0, id: 9 });
    tx.save(); tx.clip(P); mec_vurus([[lerp(d[0], c[0], .35), lerp(d[1], c[1], .35) - 3], [c[0], c[1] - 2]], 4.5 * lt, .9, .5); tx.restore(); }
  // kandiller: iki sıra, uzaklaştıkça küçülür
  if (o.lamps !== false) for (const X of [-330, 330]) for (const z of [1.55, 1.95, 2.35, 2.75, 3.15, 3.55]) if (mec_on(z)) mec_kandil(X, -300 - (z * 23 % 40), z, lt);
  // derinlik sıralı çizimler: kürsü+taht, figür, sütunlar, kalabalık sıraları, koridordakiler
  const L = [];
  L.push({ z: MW.TZ + .05, d: () => mec_kursu(o) });
  if (o.fig) L.push({ z: o.figZ ?? MW.TZ - .3, d: () => o.fig() });
  for (const z of MEC_COLZ) if (mec_on(z + .25)) for (const sd of [-1, 1]) L.push({ z, d: () => mec_sutun(sd * MW.COLX, z, lt) });
  if (o.crowd) for (const R of MEC_SAF) { if (R.z - MEC.zc < (o.zmin ?? 1.1) || R.z - MEC.zc > (o.zmax ?? 9)) continue;
    L.push({ z: R.z, d: () => { if (o.crowd === 'yilan') { const P = mec_yilanSira(R, t, o); const { tx: T } = GR; T.save(); T.translate(0, -Math.max(2.2, 3.4 * mec_k(R.z))); T.fillStyle = tone(.85 * lt + .05); T.fill(P); T.restore(); GR.fill(P, tone(lerp(.28, .02, clamp((2.7 - R.z + MEC.zc) / 1.2))), { th: 0, id: 8 }); } else mec_siraCiz(R, f => o.crowd(f, R), lt); } }); }
  for (const a of (o.aisle || [])) L.push(a);
  L.sort((a, b) => b.z - a.z);
  for (const e of L) e.d();
  if (o.front) o.front();
}
// kürsü (6 yüksek basamak) ve taht
function mec_kursu(o) {
  const { tx, tone } = GR, n = 6, dz = .06, lt = o.lt ?? 1, gl = Math.min(1, o.glow ?? 1);
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
  { const p = (X, Y) => mec_P(X, Y, MW.TZ), Y0 = MW.DTOP, ww = Math.max(2.6, 4.5 * Math.sqrt(mec_k(MW.TZ))) * (.4 + .6 * gl * lt);
    tx.save(); tx.clip(T);
    mec_vurus([p(-92, Y0 - 535), p(-92, Y0 - 380), p(-90, Y0 - 200)], ww, .95, .25);                  // arkalığın ışık kenarı
    mec_vurus([p(-126, Y0 - 165), p(-30, Y0 - 164), p(80, Y0 - 165)], ww, .93, .3);                    // oturağın ön kenarı
    mec_vurus([p(-100, Y0 - 568), p(0, Y0 - 569), p(90, Y0 - 567)], ww * .9, .93, .2);                 // tepe
    tx.restore(); }
  if (o.thrFig) o.thrFig();
}
// Şeytan kürsüde: dünya konumundan kiy_seytan'a (gol.js) çevirir. p: {X, z, Y (ayak hizası; varsayılan kürsü üstü), hw (dünya baş boyu), ...kiy_seytan seçenekleri}
function mec_seytan(t, p) {
  const z = p.z ?? MW.TZ - .3, [x, gy] = mec_P(p.X ?? 0, p.Y ?? MW.DTOP, z), h = (p.hw ?? 62) * mec_k(z);
  return kiy_seytan(t, Object.assign({ wingK: .85, lum: .25, cloak: 1.2, lit: [.2, -.98] }, p, { x, gy: gy + (p.dy || 0) * h, h }));
}

// tahtta oturan Şeytan (¾ dönük; kanatlar kapalı, pelerinli). Oturuş: uyluk öne, baldır aşağı
const MEC_OTUR = (t, tK) => ({ X: 0, z: MW.TZ - .22, dy: -1.9, twist: .45, legN: [1.45, -1.45], legF: [1.3, -1.35], armN: [.6 + .25 * E.sine(mec_u(t, tK - .4, tK + .8)), -.4], armF: [.4, -.2], head: .05, lum: .22, cloak: 1.3, wings: false });
// kuruluş kadrajı (geniş-orta): az sütun, büyük taht bölgesi; tahttaki figür ≥ 60 px
const MEC_GEN = { K: 2.3, zc: .9, vy: 170, serit: 1 };
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
  levha(ctx, cam, () => mec_salon(t, Object.assign({}, MEC_GEN, { glow: lerp(1, .85, ka), crowd: () => ({}),
    fig: () => mec_seytan(t, MEC_OTUR(t, tK)), figZ: MW.TZ - .02,
    aisle: [{ z: 2.6, d: () => { const [x, y] = mec_P(-330, -40, 2.6); mec_kure(x, y, 44, ka); } }] })));
}, { tr: { type: 'fade', dur: .9 } });

// ═════════ Dönüşüm figürü (J03, J07 ve sonrası) ═════════
// Figür bu çekimlerde SF yerine kendi sade dış hattıyla çizilir: biçim geçişi (ayakta figür → dar "mumya" → yatay kıvrık yılan) sürekli olsun diye.
// Yapı: ayaktan boyna tek omurga (MEC_NS örnek) + iki yanda genişlik profili; insan evresinde ayrı kollar ve bacaklar (birleşince omurga
// kütlesinin içinde kalırlar, sonra çizilmezler); baş 48 açılı kutupsal eğri (insan profili ↔ yılan başı). Parçaların hepsi tek koyu
// kütleye (birleşik yol) basılır: eklem çizgisi yok; kenar ışığı bu yola bir kez uygulanır. Parça sayısı ve sırası hiç değişmez.
const MEC_NS = 40;
const mec_tab = (T, s) => { if (s <= T[0][0]) return T[0][1]; for (let i = 1; i < T.length; i++) if (s <= T[i][0]) { const [a, va] = T[i - 1], [b, vb] = T[i], u = (s - a) / (b - a); return va + (vb - va) * u * u * (3 - 2 * u); } return T[T.length - 1][1]; };
// genişlik (baş boyu biriminde), s: 0 ayak … 1 boyun; F: göğüs (bakış) yanı, B: sırt yanı
// insan evresi (kiy_seytan kütlesi): göğüs yanında zırh eteği (s .48–.6) ve geniş göğüs; sırt yanında omuzdan baldıra inen pelerin
const MEC_INS_F = [[0, 0], [.44, 0], [.48, .62], [.56, .56], [.66, .46], [.8, .66], [.9, .62], [.96, .34], [1, .3]];
const MEC_INS_B = [[0, 0], [.2, 0], [.25, .95], [.36, .92], [.5, .84], [.66, .7], [.8, .7], [.9, .82], [.96, .38], [1, .3]];
const MEC_MUM = [[0, .12], [.15, .32], [.3, .44], [.45, .54], [.6, .62], [.75, .6], [.85, .66], [.93, .58], [.98, .38], [1, .34]];
const MEC_YIL = [[0, .04], [.1, .3], [.28, .66], [.5, .76], [.8, .72], [.92, .56], [1, .48]];
// baş: kutupsal yarıçap (baş boyu biriminde); açı 0 = yüzün baktığı yön, + aşağı (saat yönü)
const MEC_BAS_H = [[-180, .5], [-160, .58], [-148, .74], [-138, .58], [-124, .7], [-110, .57], [-90, .55], [-62, .54], [-36, .46], [-16, .42], [-5, .41], [5, .5], [14, .42], [24, .45], [34, .43], [48, .5], [64, .44], [90, .4], [118, .41], [142, .45], [162, .49], [180, .5]];
const mec_basH = d => mec_tab(MEC_BAS_H, d);
const mec_basS = d => { const a = d * PI / 180, c = Math.cos(a), s = Math.sin(a), ax = c > 0 ? 1.0 : .5, by = s < 0 ? .5 : .44; return 1 / Math.sqrt((c / ax) * (c / ax) + (s / by) * (s / by)); };
const mec_dir = a => [Math.sin(a), Math.cos(a)];          // 0 aşağı, + öne (+x)
// ekran yolu: yoğun örneklenmiş çoklu çizgi ve birikimli uzunluk; at(d) → [x, y]
function mec_yol(pts) {
  const P = []; for (let i = 0; i < pts.length - 1; i++) { const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let k = 0; k < 12; k++) { const t = k / 12, t2 = t * t, t3 = t2 * t; P.push([0, 1].map(j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3))); } }
  P.push(pts[pts.length - 1]); const C = [0]; for (let i = 1; i < P.length; i++) C.push(C[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]));
  const at = d => { if (d <= 0) { const a = P[0], b = P[1], l = C[1]; return [a[0] + (b[0] - a[0]) / l * d, a[1] + (b[1] - a[1]) / l * d]; }
    let lo = 0, hi = C.length - 1; while (hi - lo > 1) { const m = (lo + hi) >> 1; if (C[m] < d) lo = m; else hi = m; }
    if (d >= C[C.length - 1]) { const a = P[P.length - 2], b = P[P.length - 1], l = C[C.length - 1] - C[C.length - 2]; const e = d - C[C.length - 1]; return [b[0] + (b[0] - a[0]) / l * e, b[1] + (b[1] - a[1]) / l * e]; }
    const u = (d - C[lo]) / (C[hi] - C[lo]); return [lerp(P[lo][0], P[hi][0], u), lerp(P[lo][1], P[hi][1], u)]; };
  return { at, L: C[C.length - 1] };
}
// orta plandaki yılan yolu (ekran, K = 3.0): kürsünün üstünde S kıvrımı; uzantısı sağdaki sütunların arasından karanlığa çıkar (J11)
// figürün yeri (orta plan; ayak ekseni ve baş boyu) ve yılan yolu (ekran)
const MEC_J = { px: 641, py: 880, h: 80 };
const MEC_YOL_PTS = [[140, 870], [270, 912], [400, 918], [520, 866], [630, 824], [750, 846], [870, 912], [1000, 922], [1120, 868], [1240, 826], [1370, 840], [1500, 870], [1640, 880], [1800, 880], [2000, 878], [2400, 878]];
const MEC_YOL = mec_yol(MEC_YOL_PTS);
const MEC_YD0 = 1290;   // J07 sonunda başın yol üstündeki konumu (px)
// o: {px, py (ayak; dönme ekseni), h, armN, armF, a, g, f, sn, p, wk, head (insan başı eğimi), fruit: {x, y, r} | null,
//     yd (başın yol konumu), yl (yılan boyu, h biriminde), wave (yaşam salınımı genliği), t, lit, glowRim}
function mec_beden(o) {
  const { tx, tone } = GR, h = o.h, a = clamp(o.a || 0), g = clamp(o.g || 0), sn = E.io2(clamp(o.sn || 0)), p = clamp(o.p || 0), t = o.t || 0;
  const th = o.th ?? 0, cs = Math.cos(th), ss = Math.sin(th), piv = [o.px, o.py];
  const R = ([x, y]) => [piv[0] + x * cs - y * ss, piv[1] + x * ss + y * cs];   // yerel (ayak ekseni, y yukarı eksi) → ekran
  const L0 = 7 * h, Y = o.yol || MEC_YOL, yl = (o.yl ?? 11.4) * h, yd = o.yd ?? MEC_YD0;
  // omurga
  const C = [], WF = [], WB = [], m = s => s >= .6 ? a : s <= .5 ? g : lerp(g, a, (s - .5) / .1);
  for (let i = 0; i <= MEC_NS; i++) {
    const s = i / MEC_NS, lean = .12 * h * Math.sin(PI * s) * (1 - g * .6) * smooth(clamp((s - .4) / .2));
    let q = R([lean * (1 - sn), -s * L0]);
    if (sn > 0) { const d = yd - yl * (1 - s), r2 = Y.at(d), lift = (1 - .9 * (o.down || 0)) * 2.3 * h * Math.pow(clamp((s - .76) / .24), 1.7) + (o.wave || 0) * h * Math.sin(t * 1.3 + s * 9) * s; q = [lerp(q[0], r2[0], sn), lerp(q[1], r2[1] - lift * sn, sn)]; }
    C.push(q);
    const mm = m(s), yw = mec_tab(MEC_YIL, s);
    WF.push(lerp(lerp(mec_tab(MEC_INS_F, s), mec_tab(MEC_MUM, s), mm), yw, sn) * h);
    WB.push(lerp(lerp(mec_tab(MEC_INS_B, s), mec_tab(MEC_MUM, s), mm), yw, sn) * h);
  }
  const TN = C.map((c, i) => { const a2 = C[Math.max(0, i - 1)], b2 = C[Math.min(MEC_NS, i + 1)], dx = b2[0] - a2[0], dy = b2[1] - a2[1], l = Math.hypot(dx, dy) || 1; return [dx / l, dy / l]; });
  const NF = TN.map(([x, y]) => [-y, x]);                                          // göğüs (karın) yanı
  const U = new Path2D(), A = [], B = [];
  for (let i = 0; i <= MEC_NS; i++) { A.push([C[i][0] + NF[i][0] * WF[i], C[i][1] + NF[i][1] * WF[i]]); B.push([C[i][0] - NF[i][0] * WB[i], C[i][1] - NF[i][1] * WB[i]]); }
  mec_cok(U, [...A, ...B.reverse()]);
  // tüp: yerel noktalar dizisi (ayak ekseninde) ve yarı genişlikler
  const tup = (pts, ws) => { const S = pts.map(R), a3 = [], b3 = []; for (let i = 0; i < S.length; i++) { const p0 = S[Math.max(0, i - 1)], p1 = S[Math.min(S.length - 1, i + 1)], dx = p1[0] - p0[0], dy = p1[1] - p0[1], l = Math.hypot(dx, dy) || 1; a3.push([S[i][0] - dy / l * ws[i], S[i][1] + dx / l * ws[i]]); b3.push([S[i][0] + dy / l * ws[i], S[i][1] - dx / l * ws[i]]); } mec_cok(U, [...a3, ...b3.reverse()]); };
  const zincir = (o0, a1, l1, a2, l2, n = 10) => { const P = []; for (let i = 0; i <= n; i++) { const u = i / n; if (u <= .5) { const d = mec_dir(a1); P.push([o0[0] + d[0] * l1 * u * 2, o0[1] - d[1] * l1 * u * 2 * -1]); } else { const d = mec_dir(a1), e = [o0[0] + d[0] * l1, o0[1] + d[1] * l1], d2 = mec_dir(a2); P.push([e[0] + d2[0] * l2 * (u - .5) * 2, e[1] + d2[1] * l2 * (u - .5) * 2]); } } return P; };
  // bacaklar (insan evresi): kalçadan ayağa; g ile açılar sıfıra, aralarındaki açıklık kapanır ve birbirine dolanır
  let feet = [];
  if (g < .999) for (const [sd, an] of [[-1, [-.1, -.03]], [1, [.12, -.08]]]) {
    const hp = [sd * .1 * h * (1 - g), -4 * h], a1 = an[0] * (1 - g), a2 = (an[0] + an[1]) * (1 - g), P = zincir(hp, a1, 2.0 * h, a2, 1.95 * h, 12);
    const tw = Math.sin(PI * g) * .17 * h, P2 = P.map(([x, y], i) => [x + sd * tw * Math.sin(TAU * 1.25 * i / 12 + .4), y]);
    tup(P2, P2.map((_, i) => lerp(lerp(.42, .2, i / 12), .26, g) * h));
    const an2 = P2[12]; feet.push(an2);
    const fw = 1 - g; if (fw > .02) mec_cok(U, [an2, [an2[0] + .1 * h, an2[1] - .2 * h], [an2[0] + .55 * h * fw, an2[1] - .02 * h], [an2[0] + .5 * h * fw, an2[1] + .03 * h], [an2[0] - .12 * h, an2[1] + .03 * h]].map(R));
  }
  // kollar (insan evresi): a ile gövdeye yapışır
  let hand = null;
  if (a < .999) for (const [sd, an] of [[-1, o.armF || [-.15, .2]], [1, o.armN || [.25, .25]]]) {
    const sh = [sd * .12 * h * (1 - a) - .04 * h, -6.35 * h], a1 = lerp(an[0], .03 * sd, a), a2 = lerp(an[0] + an[1], .02 * sd, a), P = zincir(sh, a1, 1.35 * h, a2, 1.05 * h, 10);
    const k = 1 - .35 * a; tup(P, P.map((_, i) => lerp(.3, .19, i / 10) * h * k));
    const w = P[10], d = mec_dir(a2), f = [w[0] + d[0] * .12 * h, w[1] + d[1] * .12 * h], fw = R(f);
    U.moveTo(fw[0] + .17 * h * k, fw[1]); U.arc(fw[0], fw[1], .17 * h * k, 0, TAU);
    if (sd > 0) hand = R([f[0] + d[0] * .2 * h, f[1] + d[1] * .2 * h]);
  }
  // baş
  const E0 = C[MEC_NS], T0 = TN[MEC_NS], N0 = NF[MEC_NS], hb = o.head || 0;
  const phi = lerp(-hb, PI / 2 + .22 * (1 - (o.down || 0)) - .3 * (o.down || 0), sn), ux = [Math.cos(phi) * N0[0] + Math.sin(phi) * T0[0], Math.cos(phi) * N0[1] + Math.sin(phi) * T0[1]], uy = [-ux[1], ux[0]];
  const off = lerp(.44, .3, sn) * h, Hc = [E0[0] + T0[0] * off + N0[0] * .08 * h * (1 - sn), E0[1] + T0[1] * off + N0[1] * .08 * h * (1 - sn)], mix = clamp(p * .7 + .3 * sn);
  const HP = []; for (let k = 0; k < 48; k++) { const dg = -180 + k * 7.5, r = lerp(mec_basH(dg), mec_basS(dg), mix) * h * lerp(1, .95, sn), aa = dg * PI / 180, lx = Math.cos(aa) * r, ly = Math.sin(aa) * r; HP.push([Hc[0] + ux[0] * lx + uy[0] * ly, Hc[1] + ux[1] * lx + uy[1] * ly]); }
  mec_cok(U, HP, .6);
  const HU = new Path2D(); mec_cok(HU, HP, .6);
  // kanatlar (arkada): büzülür, sarkar, söner
  const wk = clamp(o.wk || 0), LIT = o.lit || [-.42, -.91];
  if (wk < .97 && sn <= 0) {
    const shw = R([-.1 * h, -6.3 * h]);
    for (const [side, P] of [[-1, { span: 8.6 * h, open: .5, lift: .42, droop: .5, rot: -.05, seed: 31, root: .1 }], [1, { span: 7.4 * h, open: .45, lift: .3, droop: .7, rot: .1, seed: 32, root: .12 }]]) {
      GR.frame(shw[0] - side * h * .18, shw[1] + h * .2, P.rot + th * .9 + side * .5 * wk, side, 1);
      KN.feathered(Object.assign({ dark: .93, rim: .7, ruin: lerp(.6, .9, wk), t, lit: [LIT[0] * side, LIT[1]] }, P, { span: P.span * (1 - wk), open: lerp(P.open, .1, wk), lift: lerp(P.lift, 0, wk), droop: lerp(P.droop, 1, wk) }));
      GR.unframe();
    }
  }
  // basma: koyu kütle + ışık yanında kenar bandı + kütlenin içine giren vuruşlar
  const lv = o.rimV ?? .96, rw = o.rimW ?? Math.max(3.5, .085 * h);
  const rim = (P) => { GR.fill(P, null, { th: 0, id: 5 }); tx.save(); tx.clip(P); tx.fillStyle = tone(lv); tx.fill(P); tx.translate(-LIT[0] * rw, -LIT[1] * rw); tx.fillStyle = tone(.02); tx.fill(P); tx.restore(); };
  if (sn > 0) {
    // yılan evresi: ADN yılanıyla aynı aile (adn_yilan: daireler birleşimi gövde, ışık yanında kenar ve içe giren kısa vuruşlar); baş ayrıca
    const M = 120, Cc = [], R0 = [];
    for (let j = 0; j <= M; j++) { const u = j / M * MEC_NS, i = Math.min(MEC_NS - 1, Math.floor(u)), f2 = u - i, q = k => lerp(k[i], k[i + 1], f2);
      const cx = lerp(C[i][0], C[i + 1][0], f2), cy = lerp(C[i][1], C[i + 1][1], f2), nf = [lerp(NF[i][0], NF[i + 1][0], f2), lerp(NF[i][1], NF[i + 1][1], f2)], wf = q(WF), wb = q(WB);
      Cc.push([cx + nf[0] * (wf - wb) / 2, cy + nf[1] * (wf - wb) / 2]); R0.push(Math.max(1, (wf + wb) / 2)); }
    adn_yilan(Cc, u => R0[Math.round(clamp(u) * M)], { seg: [[0, .985]], L: o.L || { x: 650, y: 300 }, goz: 0, rim: Math.max(4, .07 * h), kesik: .25 + .75 * sn, t });
    rim(HU);
  } else {
    rim(U);
    tx.save(); tx.clip(U);
    // sargı vuruşları (bacaklar dolandıkça belirir; düşerken söner): sırttan içe giren, uzunluğu düzensiz
    const fade = 1 - clamp(th / (PI / 2) * 1.3);
    for (let k = 0; k < 13; k++) {
      const s0 = .05 + k * .068, vis = (s0 < .52 ? g : s0 < .62 ? Math.min(g, a) : a * .7) * fade;
      if (vis < .03) continue;
      // yerel (ayakta) çerçevede, sırttan göğse doğru inen eğik sargı bandı; sonra düşüşle birlikte döner
      const i0 = Math.round(s0 * MEC_NS), ln = (.55 + .4 * hash(k * 3.7)) * clamp(vis * 1.4), y0 = -s0 * L0, xb = -WB[i0] * .95, xe = lerp(xb, WF[i0] * .9, ln);
      const p0 = R([xb, y0]), q1 = R([xe, y0 + (xe - xb) * .55]), mid = R([(xb + xe) / 2, y0 + (xe - xb) * .3]);
      if (Math.hypot(q1[0] - p0[0], q1[1] - p0[1]) > 6) gol_vurus(tx, [p0, mid, q1], Math.max(3, .1 * h), .95, .6);
    }
    // insan evresi: pelerin kıvrımları ve sırt (biçimi izleyen uzun beyaz vuruşlar), söner
    const hv = 1 - Math.max(a, g * .8);
    if (hv > .05) {
      for (const [sa, sb, k2] of [[.26, .62, .8], [.3, .7, .55], [.5, .86, .72]]) { const pts = []; for (let i = Math.round(sa * MEC_NS); i <= Math.round(sb * MEC_NS); i += 3) pts.push([lerp(C[i][0], B[i][0], k2), lerp(C[i][1], B[i][1], k2)]); if (pts.length > 2) gol_vurus(tx, pts, Math.max(3, .09 * h * hv), .93, .5); }
      for (const sa of [.5, .56]) { const i = Math.round(sa * MEC_NS); gol_vurus(tx, [A[i], [lerp(A[i][0], C[i][0], .5), lerp(A[i][1], C[i][1], .5) + .05 * h]], Math.max(3, .08 * h * hv), .9, .6); }   // etek dilimleri
    }
    tx.restore();
  }
  // göz: küçük ışık (insan → yılan)
  if (o.eye !== false) { const el = [lerp(.2, .36, mix) * h, lerp(-.07, -.1, mix) * h], ec = [Hc[0] + ux[0] * el[0] + uy[0] * el[1], Hc[1] + ux[1] * el[0] + uy[1] * el[1]], ew = lerp(.12, .075, mix) * h;
    const P = new Path2D(); P.ellipse(ec[0], ec[1], ew, Math.max(1.6, ew * .32), Math.atan2(ux[1], ux[0]) + .12, 0, TAU); tx.fillStyle = tone(.97); tx.fill(P); }
  // meyve
  if (o.fruit !== undefined && o.fruit !== null) { const fr = o.fruit === 'el' ? hand : o.fruit; if (fr) { const r = .21 * h, P = new Path2D(); P.arc(fr[0], fr[1] - (o.fruit === 'el' ? r * .6 : r), r, 0, TAU); tx.save(); tx.lineWidth = 4; tx.strokeStyle = tone(.02); tx.stroke(P); tx.fillStyle = tone(.98); tx.fill(P); tx.restore(); } }
  return { U, C, hand, Hc };
}
// J07'nin orta plan seti: K = 3.0, kürsünün üstü; arka parıltı figürün arkasında
const MEC_ORTA = { K: 3.0, vx: 960, vy: 470 };
function mec_orta(t, o = {}) {
  mec_salon(t, Object.assign({ K: 1.5, zc: 1.94, vy: 363, glow: .95, gx: 650, gy: 520, gR: 560, gClip: false, zmin: .7, zmax: .95, crowd: f => ({ n: o.neck ?? 0, bend: f.bd * (.6 + .4 * Math.sin(f.ph)), b: o.bow ?? 0 }) }, o));
}
plan('P109', (ctx, st) => {
  const t = st.t, w = (k, n = 0) => Wd('J07', k, n);
  const arm = E.io2(mec_u(t, w('ama'), w('şaşırır', 1)));
  const wk = E.io2(mec_u(t, w('şaşırır', 1) - .2, w('hisseder') + .2));
  const p = E.io2(mec_u(t, w('sivrildiğini') - .1, w('sivrildiğini') + 1.0));
  const a = E.io2(mec_u(t, w('kolları') - .1, w('yapışır') + .5));
  const g = E.io2(mec_u(t, w('bacakları') - .1, w('dolanır') + .45));
  const fT = mec_u(t, w('yüzüstü') - .05, w('yığılır') + .3), fb = mec_u(t, w('yığılır') + .3, w('yığılır') + .9);
  const th = (PI / 2 - .02) * E.in2(fT) - .07 * Math.sin(PI * fb) * (1 - fb);
  const sn = mec_u(t, w('devasa') - .45, w('yılan') + 1.1);
  // meyve: kollar yapışırken elden düşer, kürsüde sekip yuvarlanır
  const tF = w('kolları') + .45, fu = t - tF;
  levha(ctx, null, () => mec_orta(t, { neck: 1, fig: () => {
    const fr = fu < 0 ? 'el' : (() => { const x0 = 690, y0 = 560, yG = 905, g2 = 1500, tt = Math.min(fu, Math.sqrt(2 * (yG - y0) / g2)); if (fu <= tt) return [x0 + 60 * fu, y0 + .5 * g2 * fu * fu + 0];
      const u2 = fu - tt, b = Math.abs(Math.sin(u2 * 7)) * 30 * Math.exp(-u2 * 3.5); return [x0 + 40 * tt - 150 * (1 - Math.exp(-u2 * 1.2)), yG + 26 * (1 - Math.exp(-u2 * 1.2)) - b]; })();
    mec_beden({ px: MEC_J.px, py: MEC_J.py, h: MEC_J.h, t, armN: [lerp(2.55, .28, arm), lerp(.35, .3, arm)], armF: [-.15, .2], head: lerp(.1, -.18, arm), a, g, p, wk, th, sn, fruit: fr, wave: .06 * mec_u(t, w('yılan') + 1.1, w('yılan') + 3) });
  }, figZ: 3.1, crowd: f => ({ n: .45, bend: f.bd * (.6 + .4 * Math.sin(f.ph)) }) }));
}, { tr: { type: 'cut' },
  over: (ctx, st) => quote(ctx, 'Önünde diz çökülen kral, şimdi karnının üstünde.', 960, 150, st.t - Wd('J07', 'kral') + .2, { px: 66, maxW: 1500, panel: .8 }) });

// ═════════ Yardımcılar: geniş plan yılan yolu, ağaç, yürüyen asker ═════════
// orta plandaki yolu (K 1.5, zc 1.8; kürsü üstü Y = 200) geniş plana taşı
const MEC_ORTA_CAM = { K: 1.5, zc: 1.94, vy: 363 };
function mec_yolGenis() {
  const pts = MEC_YOL_PTS.map(([x, y]) => { const ze = MEC_ORTA_CAM.K * MW.DTOP / (y - MEC_ORTA_CAM.vy), X = (x - 960) * ze / MEC_ORTA_CAM.K; return mec_P(X, MW.DTOP, ze + MEC_ORTA_CAM.zc); });
  const Y = mec_yol(pts), r = Y.L / MEC_YOL.L, ze0 = MEC_ORTA_CAM.K * MW.DTOP / (MEC_J.py - MEC_ORTA_CAM.vy);
  return { Y, r, h: MEC_J.h * mec_k(ze0 + MEC_ORTA_CAM.zc) / (MEC_ORTA_CAM.K / ze0) };
}
// büyük yılan (J07 sonundaki biçim) geniş planda
function mec_buyukYilan(t, o = {}) {
  const G = mec_yolGenis();
  return mec_beden({ px: 0, py: 0, h: G.h, t, a: 1, g: 1, sn: 1, p: 1, wk: 1, yol: G.Y, yd: (o.yd ?? MEC_YD0) * G.r, wave: o.wave ?? .05, down: o.down || 0, eye: o.eye, rimW: 3 });
}
// ağaç (J10): koyu gövde ve taç, beyaz yuvarlak meyveler; yerden yükselerek belirir (gr), meyveler küle döner (ash)
function mec_agac(X, z, sd, t, gr, ash) {
  if (gr <= .005) return;
  const { tx, tone } = GR, k = mec_k(z), [x, yb] = mec_P(X, MW.FL, z), Ht = 520 * k, cy = yb - Ht, R = 190 * k, r = rng(Math.round(X * 7 + z * 100));
  tx.save(); GR.px.save(); { const C = new Path2D(); C.rect(-400, yb - (Ht + R * 1.1) * E.out3(gr) - 10, W + 800, H + 800); tx.clip(C); GR.px.clip(C); }
  const T = new Path2D(); mec_cok(T, [[x - 16 * k, yb], [x - 9 * k, cy + 40 * k], [x - 60 * k, cy - 20 * k], [x - 50 * k, cy - 28 * k], [x, cy + 10 * k], [x + 55 * k, cy - 30 * k], [x + 62 * k, cy - 20 * k], [x + 9 * k, cy + 40 * k], [x + 16 * k, yb]]);
  GR.fill(T, tone(.02), { th: -PI / 2, id: 4 });
  PR.cloud({ x, y: cy - R * .35, w: R * 2.3, h: R * 1.15, seed: 50 + Math.round(z * 10) + (X > 0 ? 3 : 0), lit: [-sd * .7, .7], base: .02, hi: .8, core: .02, n: 3 });
  // meyveler
  for (let i = 0; i < 9; i++) {
    const a = r() * TAU, d = Math.sqrt(r()) * .8, fx = x + Math.cos(a) * R * 1.05 * d, fy = cy - R * .35 + Math.sin(a) * R * .5 * d, fr = Math.max(4, 15 * k), q = rng(i * 31 + 7);
    if (ash <= 0) { const P = new Path2D(); P.arc(fx, fy, fr, 0, TAU); tx.fillStyle = tone(.97); tx.fill(P); continue; }
    const u = clamp(ash * (1 + .25 * q()) - .1 * q()), s0 = fr * (1 - E.out2(clamp(u * 3)));
    if (s0 > 1) { const P = new Path2D(); P.arc(fx, fy, s0, 0, TAU); tx.fillStyle = tone(.97); tx.fill(P); }
    for (let j = 0; j < 4; j++) { const vx = (q() - .5) * 40 * k, dy = u * u * (220 + 160 * q()) * k, rr = Math.max(0, (3.4 + q() * 2.4) * (1 - u)); if (rr < 1.2 || u <= 0) continue;
      const P = new Path2D(); P.arc(fx + vx * u, fy + dy, rr, 0, TAU); tx.fillStyle = tone(.95); tx.fill(P); }
  }
  tx.restore(); GR.px.restore();
}
// sıradan asker: pelerinsiz, kanatsız, küçük koyu siluet; mızrakla yürür. p: {X, z, Y (ayak), hw, ph (adım evresi), walk (0..1), facing}
function mec_asker(t, p) {
  const z = p.z, [x, gy] = mec_P(p.X, p.Y ?? MW.FL, z), h = (p.hw ?? 36) * mec_k(z), s = Math.sin(p.ph), w = p.walk ?? 1;
  const J = SF.rig({ x, y: gy - 3.95 * h, h, facing: p.facing ?? 1, twist: p.twist ?? .15, lean: .04 * w, head: .02, shTilt: 0,
    armN: [-.25 * s * w + .05, .2], armF: [.25 * s * w - .05, .25], legN: [.32 * s * w, -.28 * Math.max(0, -s) * w], legF: [-.32 * s * w, -.28 * Math.max(0, s) * w] });
  SF.draw(J, { lum: .08, lit: [.1, -1], t, legs: true, skirt: true, eye: 0, wind: .2, cloak: false, halo: 4, lines: 0, seed: 21, spear: { grip: 'F', ang: .05, len: 6.5, up: .78 } });
  return J;
}

// ═════════ E14 (P054): yalnız o ayağa kalkar (orta plan) ═════════
plan('P054', (ctx, st) => {
  const t = st.t, u = E.io3(mec_u(t, Wd('E14', 'yalnızca') - .2, Wd('E14', 'gönüllü') + .7)), S0 = MEC_OTUR(t, -99);
  levha(ctx, null, () => mec_orta(t, { gx: 960, gy: 330, gR: 470, bow: .35, neck: 0,
    fig: () => mec_seytan(t, { X: 0, z: MW.TZ - .22, dy: lerp(-1.9, 0, u), twist: lerp(.45, .28, u), legN: [lerp(1.45, .06, u), lerp(-1.45, -.04, u)], legF: [lerp(1.3, -.06, u), lerp(-1.35, -.02, u)],
      armN: [lerp(.6, .15, u), lerp(-.4, .2, u)], armF: [lerp(.4, -.1, u), lerp(-.2, .15, u)], head: lerp(.05, .18, u), lum: .25, cloak: 1.3, wingK: lerp(.03, .85, E.io2(mec_u(t, Wd('E14', 'gönüllü') - .3, Wd('E14', 'olur') + 1.2))), lift: .3 * u }),
    figZ: MW.TZ - .02 }));
}, { tr: { type: 'cut' } });

// ═════════ E15 (P055): bütün salon önünde eğilir (Batı saray selamı: başlar iner, gövdeler hafifçe öne) ═════════
function mec_selam(f, R, t, t0) { const d = t0 + (2.6 - R.z) * .55 + f.dl * .5; return { b: E.io2(mec_u(t, d, d + 1.3)) }; }
plan('P055', (ctx, st) => {
  const t = st.t, tE = Wd('E15', 'eğilir') - .4;
  const cam = camLerp({ cx: 940, cy: 540, z: 1 }, { cx: 990, cy: 540, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => mec_salon(t, { glow: 1.05, crowd: (f, R) => mec_selam(f, R, t, tE),
    fig: () => mec_seytan(t, { X: 0, z: MW.TZ - .3, head: .22, armN: [.25, .2], armF: [-.15, .15], lum: .25, cloak: 1.3, wingK: .85, open: .35, lift: .35 }) }));
}, { tr: { type: 'cut' },
  over: (ctx, st) => quote(ctx, 'Diz çökmeyi reddeden melek…', 960, 150, st.t - Wd('E15', 'reddeden') + .3, { px: 68, panel: .8 }) });

// ═════════ J01 (P104): bölüm kartı ALKIŞ; boş taht ═════════
plan('P104', (ctx, st) => {
  levha(ctx, null, () => mec_orta(st.t, { gx: 960, gy: 360, gR: 380, glow: .42, lt: .6, neck: 0, crowd: null }));
}, { tr: { type: 'black', dur: 1.4, end: true },
  over: (ctx, st) => chapterCard(ctx, 'ALKIŞ', 'Zafer anında, insan ne duymayı bekler?', st.lt, st.d + .4, { y: 220 }) });

// ═════════ J02 (P105): sıradan asker kılığında salondan geçer; tahtta birden belirir (sahte parıltı) ═════════
plan('P105', (ctx, st) => {
  const t = st.t, w = (k, n = 0) => Wd('J02', k, n);
  const tW0 = st.at + .3, tW1 = w('girer') + .3, tC1 = w('çıkar') + .35, tB = w('belirir') - .05;
  const wu = mec_u(t, tW0, tW1), cu = E.io2(mec_u(t, tW1, tC1));
  const fl = mec_u(t, tB, tB + .35), dec = mec_u(t, tB + .35, w('ışıkla') + .3);
  const gl = t < tB ? .45 : lerp(.45, 2.2, E.out3(fl)) * (fl < 1 ? 1 : 0) + (fl >= 1 ? lerp(2.2, .6, E.out3(dec)) : 0);
  const cheer = E.sine(mec_u(t, w('sevinç') - .3, w('sevinç') + .6)) * (1 - .4 * mec_u(t, w('karşılar'), w('karşılar') + 1.5));
  const cam = camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 960, cy: 540, z: 1 }, st.p);
  levha(ctx, cam, () => mec_salon(t, { glow: gl, lt: t < tB ? .7 : lerp(1, .8, dec),
    crowd: (f) => ({ cheer: cheer * Math.abs(Math.sin(t * 5.5 + f.ph * 3)) }),
    fig: t >= tB ? () => {
      const J = mec_seytan(t, { X: 0, z: 3.25, head: .2, armN: [.35, .2], armF: [-.2, .15], lum: .3, cloak: 1.3, wingK: .85 * lerp(.4, 1, E.out3(fl)), open: .5, lift: .45 });
      // soğuk, kısa ışınlar: figürün arkasından çıkar, hemen geri çekilir
      const k = E.out3(clamp(fl * 1.5)) * (1 - E.io2(dec)), c = [J.hd[0], J.hd[1] + J.h * 1.8];
      if (k > .02) for (let i = 0; i < 11; i++) { const an = -PI / 2 + (i - 5) * .27, L = (150 + 110 * ((i * 7) % 3)) * k, r0 = 40; mec_vurus([[c[0] + Math.cos(an) * r0, c[1] + Math.sin(an) * r0], [c[0] + Math.cos(an) * (r0 + L), c[1] + Math.sin(an) * (r0 + L)]], 6, .98, .9); }
    } : null, figZ: 3.25,
    aisle: t < tB ? [{ z: cu > 0 ? 3.0 : lerp(1.25, 2.68, wu), d: () => {
      const z = cu > 0 ? lerp(2.7, 3.2, cu) : lerp(1.25, 2.68, wu), Y = cu > 0 ? lerp(MW.FL, MW.DTOP, cu) : MW.FL;
      mec_asker(t, { X: lerp(0, -10, cu), z, Y, hw: 44, ph: t * 7.5, walk: cu >= 1 ? 0 : 1, twist: cu >= 1 ? lerp(.15, .3, mec_u(t, tC1, tB)) : .15 });
    } }] : [] }));
}, { tr: { type: 'fade', dur: .8 } });

// ═════════ J03 (P106): elinde meyve, kolu havada (orta plan; dönüşüm figürü) ═════════
const MEC_J3 = t => { const tH = Wd('J03', 'hem'), u = E.io2(mec_u(t, tH - .7, tH + .3)); return { armN: [lerp(1.5, 2.55, u), lerp(.5, .35, u)], head: lerp(.0, .1, u) }; };
plan('P106', (ctx, st) => {
  const t = st.t, A = MEC_J3(t);
  levha(ctx, null, () => mec_orta(t, { neck: 0, fig: () => mec_beden({ px: MEC_J.px, py: MEC_J.py, h: MEC_J.h, t, armN: A.armN, armF: [-.15, .2], head: A.head, fruit: 'el' }), figZ: 3.1 }));
}, { tr: { type: 'cut' },
  over: (ctx, st) => quote(ctx, '“Hem de bir elmayla!”', 1390, 250, st.t - Wd('J03', 'hem') + .2, { px: 72, maxW: 700, panel: .82 }) });

// ═════════ J04 (P107): bekleyiş. Geniş salon, tam hareketsizlik ═════════
function mec_bekleyis(t, o = {}) {
  return mec_salon(t, Object.assign({ glow: 1, crowd: () => ({}),
    fig: () => { const J = mec_seytan(t, { X: 0, z: 3.25, head: .2, armN: [2.55, .35], armF: [-.2, .15], lum: .3, cloak: 1.3, wingK: .85, open: .5, lift: .45, wind: 0 });
      const d = mec_dir(2.9), c = [J.wrN[0] + d[0] * .35 * J.h, J.wrN[1] + d[1] * .35 * J.h - .2 * J.h], P = new Path2D(); P.arc(c[0], c[1], Math.max(3.5, .24 * J.h), 0, TAU); GR.tx.fillStyle = GR.tone(.98); GR.tx.fill(P); } }, o));
}
plan('P107', (ctx, st) => {
  const T = Wd('J04', 've');                         // zaman donar: hiçbir şey kıpırdamaz (kanat, pelerin, alev, kalabalık)
  levha(ctx, null, () => mec_bekleyis(T));
}, { tr: { type: 'cut' } });

// ═════════ J05 (P108): boyunlar uzar; salon tıslamayla dolar ═════════
plan('P108', (ctx, st) => {
  const t = st.t, t0 = Wd('J05', 'yandan') - .2, tT = Wd('J05', 'tıslama'), T = Wd('J04', 've');
  const sw = E.io2(mec_u(t, Wd('J05', 'kasvetli') - .5, tT + .5));
  levha(ctx, null, () => mec_bekleyis(T, { crowd: (f, R) => { const d = t0 + (2.6 - R.z) * .9 + f.dl * 1.4; return { n: E.io2(mec_u(t, d, d + 1.8)), bend: f.bd * (.55 + .45 * Math.sin(t * (.5 + .5 * sw) + f.ph)) * (1 + .4 * sw) }; } }));
}, { tr: { type: 'cut' } });

// ═════════ J08 (P110): salon kıvrılan yılanlarla dolu; tahtın önünde büyük yılan ═════════
plan('P110', (ctx, st) => {
  const t = st.t;
  const cam = camLerp({ cx: 990, cy: 540, z: 1 }, { cx: 930, cy: 540, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => mec_salon(t, { glow: .75, lt: .8, crowd: 'yilan', fig: () => mec_buyukYilan(t), figZ: 3.2 }));
}, { tr: { type: 'cut' } });

// ═════════ J10 (P113): meyveli ağaçlar belirir; yılanlar uzanır; meyve kül olur ═════════
const MEC_AGAC = [[-400, 1.4, -1], [400, 1.45, 1], [-330, 1.95, -1], [330, 2.0, 1], [-270, 2.45, -1], [270, 2.5, 1]];
plan('P113', (ctx, st) => {
  const t = st.t, w = k => Wd('J10', k);
  const gr = i => mec_u(t, w('ağaçlar') - .3 + i * .12, w('belirir') + 1.0 + i * .12), reach = E.io2(mec_u(t, w('açlıkla') - .2, w('saldırırlar') + .6)), ash = mec_u(t, w('küle') - .4, w('küle') + 2.2);
  levha(ctx, null, () => mec_salon(t, { glow: .6, lt: .75, crowd: 'yilan', reach, fig: () => mec_buyukYilan(t), figZ: 3.2,
    aisle: MEC_AGAC.map(([X, z, sd], i) => ({ z: z - .06, d: () => mec_agac(X, z, sd, t, gr(i), ash) })) }));
}, { tr: { type: 'cut' } });

// ═════════ J11 (P114): yılan sütunların arasından çıkar; boş, karanlık salon; soru geri gelir ═════════
plan('P114', (ctx, st) => {
  const t = st.t, w = k => Wd('J11', k);
  const go = mec_u(t, w('şeytan') - .2, w('çıkmaz') + .4), yd = MEC_YD0 + 1500 * (go * go * (3 - 2 * go) * .6 + go * .4), dim = E.io2(mec_u(t, w('ama') - .3, w('ortada') + .5));
  levha(ctx, null, () => mec_orta(t, { crowd: null, glow: lerp(.95, .3, dim), lt: lerp(1, .5, dim),
    fig: () => mec_beden({ px: 0, py: 0, h: MEC_J.h, t, a: 1, g: 1, sn: 1, p: 1, wk: 1, yd, wave: .05 }), figZ: 3.1 }));
}, { tr: { type: 'fade', dur: .9 },
  over: (ctx, st) => quote(ctx, 'Onu orada tutan neydi?', 960, 200, st.t - Wd('J11', 'tutan') + .25, { px: 92, maxW: 1400, panel: .85, per: .3 }) });
