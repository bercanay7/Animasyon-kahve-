// Figür ve doğa ilkelleri (İkaros, serigrafi): her şey Path2D döner; basımı pr.ink yapar (çizgi yok, düz mürekkep).
// Birim h = baş boyu. Profil figür; açılar gövde eksenine göre (0 = gövde boyunca aşağı, + = yüzün baktığı yöne).
'use strict';
const FG = (() => {
  const P = () => new Path2D();
  // yönlü kapsül (iki uç yarıçapı): hep aynı dönüş yönünde çizilir → nonzero birleşim iç çizgi bırakmaz
  function capsule(p, a, b, r0, r1) {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1e-6, an = Math.atan2(dy, dx);
    const N = 10, pts = [];
    for (let i = 0; i <= N; i++) { const t = an + Math.PI / 2 + Math.PI * i / N; pts.push([a[0] + Math.cos(t) * r0, a[1] + Math.sin(t) * r0]); }
    for (let i = 0; i <= N; i++) { const t = an - Math.PI / 2 + Math.PI * i / N; pts.push([b[0] + Math.cos(t) * r1, b[1] + Math.sin(t) * r1]); }
    polyInto(p, pts);
  }
  function polyInto(p, pts) {
    // saat yönüne zorla (nonzero birleşim)
    let s = 0; for (let i = 0; i < pts.length; i++) { const q = pts[i], r = pts[(i + 1) % pts.length]; s += (r[0] - q[0]) * (r[1] + q[1]); }
    if (s > 0) pts = pts.slice().reverse();
    pts.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); p.closePath();
  }
  function ellipseInto(p, cx, cy, rx, ry, rot = 0, n = 28) { const pts = []; for (let i = 0; i < n; i++) { const t = i / n * Math.PI * 2; const x = Math.cos(t) * rx, y = Math.sin(t) * ry; pts.push([cx + x * Math.cos(rot) - y * Math.sin(rot), cy + x * Math.sin(rot) + y * Math.cos(rot)]); } polyInto(p, pts); }
  const add2 = (a, b, k = 1) => [a[0] + b[0] * k, a[1] + b[1] * k];

  // ── Poz → eklemler ──
  // o: {x, y (kalça), h, f (1 sağa bakar, -1 sola), lean (gövde eğimi, rad; + öne), head (baş eğimi), armN, armF: [omuz, dirsek], legN, legF: [kalça, diz]}
  function rig(o) {
    const h = o.h || 40, f = o.f || 1, lean = o.lean || 0;
    const dir = a => [Math.sin(a) * f, Math.cos(a)];                 // a: dikeyden (aşağı) açı, + yüz yönü
    const up = dir(Math.PI - lean * 1);                                // gövde yukarı ekseni
    const upv = [Math.sin(lean) * f, -Math.cos(lean)];
    const H = [o.x, o.y], Sh = add2(H, upv, 2.55 * h), N = add2(H, upv, 2.85 * h);
    const ht = lean + (o.head || 0), Hd = add2(N, [Math.sin(ht) * f, -Math.cos(ht)], .55 * h);
    const limb = (root, ang, l1, l2) => { const a1 = ang[0] - lean, k = add2(root, dir(a1), l1), e = add2(k, dir(a1 + ang[1]), l2); return [root, k, e, a1 + ang[1]]; };
    const J = { h, f, lean, H, Sh, N, Hd, ht, upv };
    J.armN = limb(Sh, o.armN || [.1, -.2], 1.45 * h, 1.3 * h); J.armF = limb(Sh, o.armF || [-.1, -.2], 1.45 * h, 1.3 * h);
    J.legN = limb(H, o.legN || [.05, 0], 1.9 * h, 1.85 * h); J.legF = limb(H, o.legF || [-.05, 0], 1.9 * h, 1.85 * h);
    J.wingRoot = add2(Sh, [-f * Math.cos(lean) * .3 * h + upv[0] * -.1 * h, -f * Math.sin(lean) * -.3 * h + upv[1] * -.1 * h]);
    return J;
  }
  // baş profili: kafatası + yüz (alın, burun, çene) + saç (kıvırcık ya da düz) + sakal (yaşlı usta)
  function headInto(p, J, o = {}) {
    const { Hd, h, f, ht } = J, r = .5 * h, c = Math.cos(ht), s = Math.sin(ht);
    const T = (x, y) => [Hd[0] + (x * c - y * s) * f, Hd[1] + (x * s + y * c)];   // x: yüz yönü, y: aşağı
    ellipseInto(p, Hd[0], Hd[1], r * .98, r * 1.04, ht);
    polyInto(p, [T(.2 * r, -.78 * r), T(.78 * r, -.42 * r), T(.88 * r, -.1 * r), T(1.2 * r, .24 * r), T(.92 * r, .36 * r), T(1.0 * r, .5 * r), T(.9 * r, .58 * r),
      T(.97 * r, .68 * r), T(.86 * r, .86 * r), T(.6 * r, 1.0 * r), T(.1 * r, .92 * r), T(-.1 * r, .4 * r)]);
    if (o.beard) { polyInto(p, [T(.66 * r, .5 * r), T(.98 * r, .86 * r), T(.9 * r, 1.22 * r), T(.62 * r, 1.62 * r), T(.36 * r, 1.4 * r), T(.1 * r, 1.2 * r), T(-.15 * r, .5 * r)]); for (let k = 0; k < 5; k++) { const a = Math.PI * (.8 + k * .16); ellipseInto(p, ...T(Math.cos(a) * r * .95 - .1 * r, Math.sin(a) * r * .9 + .05 * r), r * .2, r * .2, 0, 12); } }
    if (o.curls) for (let k = 0; k < 7; k++) { const a = Math.PI * (.78 + k * .12); ellipseInto(p, ...T(Math.cos(a) * r * .84 - .04 * r, Math.sin(a) * r * .86 - .02 * r), r * .19, r * .19, 0, 14); }
    if (o.faceOut) { const fp = P(); polyInto(fp, [T(.32 * r, -.8 * r), T(.78 * r, -.42 * r), T(.86 * r, -.06 * r), T(1.12 * r, .2 * r), T(.9 * r, .34 * r), T(.94 * r, .52 * r), T(.84 * r, .66 * r), T(.86 * r, .8 * r), T(.6 * r, 1.0 * r), T(.4 * r, .88 * r), T(.5 * r, .3 * r), T(.44 * r, -.3 * r)]);
      const ep = P(); ellipseInto(ep, ...T(.66 * r, -.1 * r), r * .11, r * .06, ht, 14); o.faceOut.face = fp; o.faceOut.eye = ep; }
    // boyun
    capsule(p, J.N, add2(Hd, [-f * .1 * h, .25 * h]), .26 * h, .24 * h);
  }
  // gövde + kısa ya da uzun tunik (chiton). İkaros: kısa tunik (çıplaklık yok); Daidalos: uzun.
  function bodyInto(p, J, o = {}) {
    const { H, Sh, h, f, upv, lean } = J, side = [-upv[1] * f, upv[0] * f];   // side: yüz yönüne dik (göğüs önü)
    const fw = [Math.cos(lean) * f, Math.sin(lean)];                            // gövdeye dik, yüz yönü
    const len = o.long ? 3.9 : 2.0, hg = lean < .7 ? 1 - lean / .7 : 0, hd = [lerp(-upv[0], 0, hg), lerp(-upv[1], 1, hg)], hn = Math.hypot(...hd), hem = add2(H, [hd[0] / hn, hd[1] / hn], len * h), fl = o.long ? .78 : .78;
    const sw = o.long ? .4 : .46, wb = o.long ? .4 : .58;
    polyInto(p, [add2(add2(Sh, fw, sw * h), upv, .1 * h), add2(add2(Sh, fw, -.48 * h), upv, .05 * h), add2(add2(H, fw, -wb * h), upv, .45 * h), add2(add2(H, fw, -(wb + .06) * h), upv, .1 * h),
      add2(hem, fw, -fl * h), add2(hem, fw, (fl + .1) * h), add2(add2(H, fw, (wb + .02) * h), upv, .1 * h), add2(add2(H, fw, wb * h), upv, .45 * h), add2(add2(Sh, fw, (sw + .1) * h), upv, -.9 * h)]);
  }
  function limbInto(p, L, r0, r1, r2) { capsule(p, L[0], L[1], r0, r1); capsule(p, L[1], L[2], r1, r2); }
  function footInto(p, L, J, r) { const a = L[3], toe = add2(L[2], [Math.cos(a) * 0 + J.f * Math.cos(a - J.lean * 0) * .55 * J.h, Math.sin(a) * 0 + .05 * J.h]); capsule(p, L[2], toe, r, r * .7); }
  // tam figür: {far, body} Path2D. far = uzak kol ve bacak (bir ton açık basılır), body = gövde, baş, yakın uzuvlar
  function figure(J, o = {}) {
    const h = J.h, far = P(), body = P();
    if (!o.noArmF) limbInto(far, J.armF, .2 * h, .17 * h, .13 * h); limbInto(far, J.legF, .3 * h, .22 * h, .17 * h); footInto(far, J.legF, J, .16 * h);
    const fo = o.face ? {} : null; bodyInto(body, J, o); headInto(body, J, { ...o, faceOut: fo });
    if (o.chest) ellipseInto(body, J.Sh[0] - J.f * .05 * h, J.Sh[1] + .45 * h, .62 * h, .7 * h, J.lean, 24);
    if (!o.noArmN) limbInto(body, J.armN, .21 * h, .18 * h, .14 * h); limbInto(body, J.legN, .31 * h, .23 * h, .17 * h); footInto(body, J.legN, J, .17 * h);
    if (o.hands !== false && !o.noArmN) { ellipseInto(body, J.armN[2][0], J.armN[2][1], .19 * h, .15 * h, J.armN[3], 12); ellipseInto(far, J.armF[2][0], J.armF[2][1], .18 * h, .14 * h, J.armF[3], 12); }
    let belt = null; if (!o.long && o.belt !== false) { belt = P(); const fw = [Math.cos(J.lean) * J.f, Math.sin(J.lean)], c = add2(J.H, J.upv, .55 * h); polyInto(belt, [add2(add2(c, fw, -.66 * h), J.upv, .09 * h), add2(add2(c, fw, .62 * h), J.upv, .09 * h), add2(add2(c, fw, .62 * h), J.upv, -.09 * h), add2(add2(c, fw, -.66 * h), J.upv, -.09 * h)]); }
    return { far, body, face: fo && fo.face, eye: fo && fo.eye, belt };
  }

  // ── Kanat (kuş kanadı; kola bağlı), afiş dili: tek siluet. Ön kenar kökten bileğe, oradan uca; arka kenar tırtıklı
  // (ikinciller sığ yaylar, birinciller derin oyuklu "parmaklar"). İkinci ton: örtü tüyleri (ön kenar boyunca, tırtıklı alt kenar).
  // o: {root, ang (kökten bileğe ekran açısı), bend (bilekte dönüş), span, chord, f (tüylerin ön kenara göre dönüş yönü ±1), ruin, seed}
  function wing(o) {
    const f = o.f || 1, sp = o.span, ch = o.chord ?? sp * .36, bend = o.bend ?? .3, R = o.root, d = a => [Math.cos(a), Math.sin(a)];
    const Wr = add2(R, d(o.ang), sp * .46), T = add2(Wr, d(o.ang + bend), sp * .54);
    const nrm = a => d(a + 1.62 * f);                                            // ön kenardan arkaya
    const lead = []; for (let i = 0; i <= 14; i++) { const u = i / 14; const q = u < .46 ? add2(R, d(o.ang), sp * u) : add2(Wr, d(o.ang + bend), sp * (u - .46)); lead.push(add2(q, nrm(u < .46 ? o.ang : o.ang + bend), -sp * .025 * Math.sin(u * Math.PI))); }
    // arka kenar: kökten uca uç noktaları
    const tips = [], NS = 6, NP = 6, r = rng(o.seed || 3);
    for (let k = 0; k <= NS; k++) { const u = k / NS, b = add2(R, d(o.ang), sp * .46 * u); const miss = o.ruin && hash(k * 3.7 + (o.seed || 0)) < o.ruin; tips.push({ p: add2(b, nrm(o.ang + .1 * u * f), ch * (miss ? .45 : (.84 + .12 * u)) * (1 + (r() - .5) * .05)), deep: false }); }
    for (let k = 1; k <= NP; k++) { const u = k / NP, b = add2(Wr, d(o.ang + bend), sp * .54 * (u * .92)), a = o.ang + bend + 1.62 * f - (.25 + 1.15 * u) * f;
      const miss = o.ruin && hash(k * 5.1 + 9 + (o.seed || 0)) < o.ruin * 1.3; tips.push({ p: add2(b, d(a), ch * (miss ? .35 : (1.0 + .45 * u - .3 * u * u))), deep: true, b }); }
    // arka kenar: her tüy ucu yuvarlak; ikinciller arası sığ çentik, birinciller ("parmaklar") arası derin oyuk
    const trail = [];
    for (let i = 0; i < tips.length; i++) {
      const A = tips[i].p, B = i + 1 < tips.length ? tips[i + 1].p : T, prv = i > 0 ? tips[i - 1].p : R;
      const dx = B[0] - prv[0], dy = B[1] - prv[1], L = Math.hypot(dx, dy) || 1, tg = [dx / L, dy / L], rr = Math.hypot(B[0] - A[0], B[1] - A[1]) * .5;
      const out = [-tg[1] * f, tg[0] * f];                                        // dışa (ön kenardan uzağa)
      for (let k = 0; k <= 6; k++) { const th = -Math.PI / 2 + Math.PI * k / 6; trail.push(add2(add2(A, tg, Math.sin(th) * rr * .9), out, Math.cos(th) * rr * .55)); }
      const m = [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2];
      if (tips[i].deep || (i + 1 < tips.length && tips[i + 1].deep)) { const base = tips[i + 1] && tips[i + 1].b ? tips[i + 1].b : m; trail.push([lerp(m[0], base[0], .45), lerp(m[1], base[1], .45)]); }
      else trail.push(add2(m, out, -rr * .35));
    }
    const all = P(); polyInto(all, [...lead, ...trail.slice().reverse()]);
    // örtü tüyleri: ön kenar boyunca, tırtıklı alt kenar
    const cv = []; for (let i = 0; i <= 10; i++) { const u = i / 10 * .82, q = u < .46 ? add2(R, d(o.ang), sp * u) : add2(Wr, d(o.ang + bend), sp * (u - .46)), a = u < .46 ? o.ang : o.ang + bend; cv.push([q, add2(q, nrm(a), ch * (.42 - .22 * u / .82) * (i % 2 ? .78 : 1))]); }
    const cov = P(); polyInto(cov, [...cv.map(x => x[0]), ...cv.map(x => x[1]).reverse()]);
    return { all, cov, lead, wrist: Wr, tip: T };
  }
  // ── Doğa ──
  // güneş: dolu disk + eş merkezli halkalar (WPA afiş güneşi); halkalar kâğıt boşluklu
  function sunRings(x, y, r, n = 3, gap = .5) { const disk = P(); disk.arc(x, y, r, 0, Math.PI * 2); const rings = []; for (let k = 1; k <= n; k++) { const r0 = r * (1 + k * .55), r1 = r0 + r * .32 * (1 - k * .18); rings.push(SK.ringPath(x, y, r0, r1)); } return { disk, rings }; }
  // sırt / kayalık: x0..x1 arasında yukarıda tepe çizgisi, aşağısı dolu
  function ridge(x0, x1, yBase, yTop, rough, seed, depth = 6) { const pts = SK.ridgeLine([x0, yTop], [x1, yTop + rough * .2], rough, depth, seed); return SK.polyPath([[x0 - 10, yBase], ...pts, [x1 + 10, yBase]]); }
  // yalıyar: dik kıyı; edgeX'te denize iner
  function cliff(x0, edgeX, yTop, yBase, f = 1, seed = 1) {
    const r = rng(seed), pts = [[x0, yBase], [x0, yTop + 20]];
    for (let i = 1; i <= 8; i++) { const u = i / 8; pts.push([lerp(x0, edgeX, u), yTop + (r() - .5) * 18 + u * u * 10]); }
    for (let i = 1; i <= 7; i++) { const u = i / 7; pts.push([edgeX + Math.sin(u * 9 + seed) * 14 * f - u * 30 * f + (r() - .5) * 10, lerp(yTop, yBase, u)]); }
    return SK.polyPath(pts);
  }
  // deniz yüzeyinde parıltı çubukları
  function glints(x0, x1, y0, y1, n, seed, t = 0, len = 60) { const p = P(), r = rng(seed); for (let i = 0; i < n; i++) { const yy = lerp(y0, y1, Math.pow(r(), .8)), k = (yy - y0) / (y1 - y0 + 1e-6), L = len * (.4 + k) * (.5 + r()), xx = lerp(x0, x1, r()) + Math.sin(t * .6 + i) * 6; p.rect(xx, yy, L, 2.5 + 4 * k); } return p; }
  // bulut kümesi: düz alt kenarlı yumrular
  function cloud(x, y, w, hh, seed) { const p = P(), r = rng(seed), n = 5; for (let i = 0; i < n; i++) { const u = (i + .5) / n, rr = hh * (.5 + .5 * Math.sin(u * Math.PI)) * (.8 + .3 * r()); ellipseInto(p, x + (u - .5) * w, y - rr * .45, rr * 1.1, rr * .8); } p.rect(x - w * .55, y - hh * .25, w * 1.1, hh * .25); return p; }
  // martı ya da uzak kuş
  function gull(x, y, s, flap = 0) { const p = P(), a = .35 + .3 * Math.sin(flap); polyInto(p, [[x - s, y - s * a], [x - s * .45, y - s * .15], [x, y + s * .12], [x + s * .45, y - s * .15], [x + s, y - s * a], [x + s * .45, y - s * .02], [x, y + s * .3], [x - s * .45, y - s * .02]]); return p; }
  // labirent: ızgara labirent (belirlenimci), eğik bakışta duvar şeritleri. cx, cy merkez; w genişlik; n hücre; sq dikey basıklık
  function labyrinth(cx, cy, w, n = 9, sq = .38, seed = 5, wall = .22) {
    const r = rng(seed), V = Array.from({ length: n }, () => Array(n).fill(false)), H = Array.from({ length: n + 1 }, () => Array(n).fill(true)), Vw = Array.from({ length: n }, () => Array(n + 1).fill(true));
    const st = [[0, 0]]; V[0][0] = true;
    while (st.length) { const [i, j] = st[st.length - 1], nb = [[1, 0], [-1, 0], [0, 1], [0, -1]].map(([a, b]) => [i + a, j + b, a, b]).filter(([a, b]) => a >= 0 && b >= 0 && a < n && b < n && !V[a][b]);
      if (!nb.length) { st.pop(); continue; } const [a, b, da, db] = nb[Math.floor(r() * nb.length)];
      if (da) Vw[j][Math.max(i, a)] = false; else H[Math.max(j, b)][i] = false; V[a][b] = true; st.push([a, b]); }
    H[0][Math.floor(n / 2)] = false; H[n][Math.floor(n / 2) - 1] = false;
    const c = w / n, tw = c * wall, X = i => cx - w / 2 + i * c, Y = j => cy + (j * c - w / 2) * sq, p = P();
    for (let j = 0; j <= n; j++) for (let i = 0; i < n; i++) if (H[j][i]) p.rect(X(i) - tw / 2, Y(j) - tw * sq * 1.6, c + tw, tw * sq * 1.6 + tw * .9);
    for (let j = 0; j < n; j++) for (let i = 0; i <= n; i++) if (Vw[j][i]) p.rect(X(i) - tw / 2, Y(j) - tw * sq, tw, c * sq + tw * sq + tw * .9);
    return p;
  }
  return { rig, figure, wing, sunRings, ridge, cliff, glints, cloud, gull, labyrinth, capsule, polyInto, ellipseInto, P };
})();
