// sav grubu (SAV: cennetteki savaş, dokuz günlük düşüş; KAO: Kaos): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
// Kaos tarifi: ne ışık ne karanlık; ufuksuz, girdaplı boşluk. Yatay tarama yerine büyük, sakin, kavisli (bend) kütleler;
// karede tek küçük parlak hedef (cehennem ağzı, kapıdan sızan ışık, zincire asılı dünya, göğüsteki alev).
'use strict';
const sav_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));

// ═════════ Kaos boşluğu ═════════
// Zemin düz siyah; ışık hedefinin (cx, cy) çevresinde yassı, yumuşak bir aydınlık: çizgileri hedefin üstünde kemerlenen kavisli akış (bend).
// Girdap kolları (kao_kol): hilal biçimli büyük kütleler; ışığa bakan iç kenarı kâğıda yakın, dışa doğru düz siyaha iner;
// çizgiler kolun kavsini izler (her kolun kendi merkezi: eş merkezli halka okunmaz). İç kenarda sivrilen kâğıt kenar ışığı, kütlenin içinde kavsi izleyen 1–2 beyaz akış vuruşu.
// o: {cx, cy, sy (aydınlığın yassılığı), glow: [r0, r1, a], k (zemin çizgisinin kavsi, 1/px), kollar: [kol...]}
function kao_bosluk(t, o = {}) {
  const { tx, px, tone } = GR, cx = o.cx ?? 960, cy = o.cy ?? 540, sy = o.sy ?? .6;
  tx.fillStyle = tone(.02); tx.fillRect(-1600, -1600, W + 3200, H + 3200);
  px.fillStyle = GR.hatch({ type: 'bend', ox: cx, oy: cy, a: 0, k: o.k ?? -1 / 1500, id: 2 }); px.fillRect(-1600, -1600, W + 3200, H + 3200);
  if (o.glow) { const [g0, g1, ga] = o.glow; tx.save(); tx.translate(cx, cy); tx.scale(1, sy); tx.translate(-cx, -cy); PR.glow(cx, cy, g0, g1, 1, ga); tx.restore(); }
  return (o.kollar || []).map((K, i) => kao_kol(t, K, i));
}
// kol: {ox, oy (yay merkezi), R, a0 (başlangıç açısı), span (yay, radyan; işaret yönü verir), wd (kalınlık), v (iç kenar tonu), lit (iç kenar ışığı 0..1), seed, rot (dönüş hızı), taper ([baş, son] sivrilme üssü)}
function kao_kol(t, K, i = 0) {
  const { tx, px, tone } = GR, q = rng((K.seed || 1) * 37 + i), m = 44, inner = [], outer = [];
  const a0 = K.a0 + (K.rot ?? .006) * t * Math.sign(K.span), ph = q() * TAU, ph2 = q() * TAU, R = K.R, wd = K.wd;
  for (let k = 0; k <= m; k++) {
    const u = k / m, a = a0 + K.span * u, e = Math.pow(Math.sin(PI * Math.pow(u, K.skew ?? .75)), .7);
    const Rr = R * (1 + (K.spiral ?? .06) * u + .025 * Math.sin(u * 4.5 + ph));
    const wi = wd * .45 * e * (1 + .12 * Math.sin(u * 6 + ph2)), wo = wd * .55 * e * (1 + .15 * Math.sin(u * 3.3 + ph));
    inner.push([K.ox + Math.cos(a) * (Rr - wi), K.oy + Math.sin(a) * (Rr - wi)]);
    outer.push([K.ox + Math.cos(a) * (Rr + wo), K.oy + Math.sin(a) * (Rr + wo)]);
  }
  const P = new Path2D(); spline(P, [...inner, ...outer.slice().reverse()], true, .8);
  const v = K.v ?? .7, g = tx.createRadialGradient(K.ox, K.oy, Math.max(1, R - wd * .5), K.ox, K.oy, R + wd * .6);
  g.addColorStop(0, tone(v)); g.addColorStop(.3, tone(v * .62)); g.addColorStop(.62, tone(v * .25)); g.addColorStop(.85, tone(.03)); g.addColorStop(1, tone(.02));
  GR.fill(P, g, { type: 'rad', cx: K.ox, cy: K.oy, id: 2, ph: q() });
  if ((K.lit ?? 1) > 0) {
    tx.save(); tx.clip(P);
    const k0 = Math.round(m * .12), k1 = Math.round(m * .88), rim = [];
    for (let k = k0; k <= k1; k += 2) { const d = [outer[k][0] - inner[k][0], outer[k][1] - inner[k][1]], l = Math.hypot(d[0], d[1]) || 1; rim.push([inner[k][0] + d[0] / l * 2, inner[k][1] + d[1] / l * 2]); }
    gol_vurus(tx, rim, (K.rimW ?? 8) * (K.lit ?? 1), .97, .4);
    // akış vuruşları: kütlenin içinde kavsi izleyen, iki ucu sivri beyaz çizgiler (kenara koşut eko değil: farklı uzunluk ve derinlik)
    for (let j = 0; j < (K.flow ?? 2); j++) {
      const f0 = .15 + q() * .35, f1 = Math.min(.92, f0 + .2 + q() * .35), dep = .18 + q() * .3, pts = [];
      for (let k = Math.round(m * f0); k <= Math.round(m * f1); k += 2) pts.push([lerp(inner[k][0], outer[k][0], dep), lerp(inner[k][1], outer[k][1], dep)]);
      if (pts.length > 3) gol_vurus(tx, pts, (K.flowW ?? 6) * (K.lit ?? 1), .9, .6);
    }
    tx.restore();
  }
  return { path: P, inner, outer };
}

// ═════════ uçan figür (Şeytan, küçük): koyu siluet, açık kanatlar ═════════
// p: {x, y (kalça), h, lean, head, open, lift, flap, lum, lit, seed, facing, legs (bacak açıları), arms}
function kao_ucan(t, p) {
  const h = p.h, f = p.facing ?? 1;
  const J = SF.rig({ x: p.x, y: p.y, h, facing: f, twist: p.twist ?? .25, lean: p.lean ?? .1, head: p.head ?? .1, shTilt: -.04,
    armN: p.armN || [-.35, .25], armF: p.armF || [-.2, .3], legN: p.legN || [-.25, -.35], legF: p.legF || [-.1, -.5] });
  const LIT = p.lit || [0, 1], fl = p.flap || 0;
  for (const [side, P] of [[-1, { span: 9 * h, seed: 41, root: .1, rot: -.05 }], [1, { span: 8.4 * h, seed: 42, root: .12, rot: .05 }]]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    GR.frame(sh[0] - side * h * .25, sh[1] + h * .15, P.rot - side * fl * .25, side, 1);
    KN.feathered({ span: P.span, open: p.open ?? .95, lift: (p.lift ?? .7), droop: p.droop ?? .15, ruin: p.ruin ?? .5, dark: .93, rim: .8, t, seed: P.seed, root: P.root, lit: [LIT[0] * side, LIT[1]] });
    GR.unframe();
  }
  SF.draw(J, { lum: p.lum ?? .1, lit: LIT, t, legs: true, skirt: true, eye: 0, wind: .9, cloak: p.cloak ?? 1.2, halo: 0, lines: 1.2, seed: p.seed || 5 });
  return J;
}
// göğüsteki alev: küçük kâğıt beyazı dil + yumuşak parıltı (karenin en parlak noktası). a: 0..1
function kao_gogusAlev(J, t, a = 1, s = 1) {
  if (a <= 0) return;
  const { tx, tone } = GR, h = J.h, x = J.shC[0] + J.rt[0] * J.f * h * .25 - J.up[0] * .55 * h, y = J.shC[1] - J.up[1] * .55 * h;
  PR.glow(x, y, 2, h * 2.6 * s, 1, .5 * a);
  const L = h * .62 * s * (.9 + .1 * Math.sin(t * 5.3)) * a, wd = h * .2 * s * a, sw = Math.sin(t * 3.1) * wd * .5;
  if (L < 2) return;
  const P = new Path2D(); P.moveTo(x - wd, y + wd * .6);
  P.bezierCurveTo(x - wd * 1.2, y - L * .3, x + sw - wd * .2, y - L * .7, x + sw, y - L);
  P.bezierCurveTo(x + sw + wd * .3, y - L * .6, x + wd * 1.25, y - L * .3, x + wd, y + wd * .6);
  P.quadraticCurveTo(x, y + wd * 1.1, x - wd, y + wd * .6); P.closePath();
  GR.fill(P, tone(1), { th: -PI / 2, id: 3 });
  return [x, y];
}

// ═════════ P003 (A03): kanca: cehennem ağzından kaçan figür; göğsündeki alev onunla gider ═════════
// Girdabın gözü cehennem ağzıdır (kadrajın altı): kollar ağzın üstünde kemer gibi döner, iç kenarları alttan aydınlanır.
// Ağzın arkası koyu (alev dilleri koyunun önünde okunur). Figür kolların aydınlık kenarlarının önünden geçerek yükselir;
// parlak hedef göğsündeki küçük alev. "tutan"da durur, yavaş kanat çırparak asılı kalır.
function kao_agiz(t, X, Y, o = {}) {
  const s = o.s ?? 1, e = o.e ?? 1;
  PR.flameBank(X - 330 * s, X + 330 * s, Y + 70, 230 * s * e, t, 117, { n: 7, wr: .45, curl: .4, speed: .55, solidBelow: 500, strip: .35, frags: false, env: f => .3 + .7 * Math.sin(f * PI) });
  const L = [[-80, Y - 230 * s], [X - 720 * s, Y - 170 * s], [X - 560 * s, Y - 110 * s], [X - 450 * s, Y - 50 * s], [X - 380 * s, Y + 20 * s], [X - 330 * s, Y + 110 * s], [X - 310 * s, H + 60], [-80, H + 60]];
  const R = [[W + 80, Y - 200 * s], [X + 740 * s, Y - 160 * s], [X + 600 * s, Y - 104 * s], [X + 480 * s, Y - 52 * s], [X + 400 * s, Y + 16 * s], [X + 340 * s, Y + 104 * s], [X + 310 * s, H + 60], [W + 80, H + 60]];
  const RP1 = PR.rock(L, { lit: [.75, -.66], hi: .05, mid: .03, lo: .02, seed: 3, th: -.6, rim: 6, facets: 7 });
  PR.cuts(L.slice(1, 6), [-.45, .9], { len: [14, 120], gap: [44, 120], w: 6, seed: 8, clip: RP1, bend: .3 });
  const RP2 = PR.rock(R, { lit: [-.75, -.66], hi: .05, mid: .03, lo: .02, seed: 6, th: .6, rim: 6, facets: 7 });
  PR.cuts(R.slice(1, 6), [.45, .9], { len: [14, 120], gap: [44, 120], w: 6, seed: 9, clip: RP2, bend: -.3 });
}
const KAO_P003 = [
  { ox: 960, oy: 1170, R: 430, a0: -2.85, span: 1.55, wd: 130, v: .82, seed: 1 },
  { ox: 840, oy: 1120, R: 720, a0: -.25, span: -1.75, wd: 180, v: .68, seed: 2 },
  { ox: 1010, oy: 1260, R: 1020, a0: -3.0, span: 1.25, wd: 230, v: .55, seed: 3 },
  { ox: 880, oy: 1220, R: 1380, a0: -.42, span: -1.15, wd: 260, v: .45, seed: 4 },
  { ox: 900, oy: 1320, R: 1560, a0: -2.55, span: .8, wd: 200, v: .32, seed: 5 },
];
function kao_p003(t) {
  const t0 = S('A03'), tT = Wd('A03', 'tutan'), X = 900, Y = 1020;
  const u = E.out2(sav_u(t, t0 - .4, tT)), hov = sav_u(t, tT - .6, tT + 1.5);
  kao_bosluk(t, { cx: X, cy: Y + 60, kollar: KAO_P003 });
  kao_agiz(t, X, Y, { e: lerp(1, .7, u) });
  // yükseliş: ağızdan hızla çıkar, yavaşlar; "tutan"da durur
  const x = lerp(860, 1000, E.io2(u)), y = lerp(960, 470, u) + Math.sin(t * 1.6) * 6 * hov;
  const fl = Math.sin(t * lerp(5.5, 2.4, hov)) * lerp(.5, .28, hov);
  kao_figur(t, { x, y, h: 30, lean: lerp(-.12, .02, u), head: lerp(.3, .05, hov), open: .95, lift: .62, flap: fl, lum: .1, lit: [0, 1], seed: 7,
    legN: [.05, -.12], legF: [-.06, -.22], armN: [-.25, .2], armF: [-.15, .25] }, 1, 1.1);
}
// figür + göğüs alevi: parıltı figürün ARKASINA (siluet ona karşı okunur), alev dili önüne
function kao_figur(t, p, a = 1, s = 1) {
  const pre = SF.rig({ x: p.x, y: p.y, h: p.h, facing: p.facing ?? 1, twist: p.twist ?? .25, lean: p.lean ?? .1, head: p.head ?? .1, shTilt: -.04 });
  const c = kao_alevYer(pre);
  if (a > 0) PR.glow(c[0], c[1], 2, p.h * 3.4 * s, 1, .42 * a);
  const J = kao_ucan(t, p);
  kao_gogusAlev(J, t, a, s);
  return J;
}
const kao_alevYer = J => [J.shC[0] + J.rt[0] * J.f * J.h * .25 - J.up[0] * .55 * J.h, J.shC[1] - J.up[1] * .55 * J.h];
plan('P003', (ctx, st) => {
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => kao_p003(st.t));
}, { tr: { type: 'cut' },
  over: (ctx, st) => quote(ctx, 'Onu orada tutan ne?', 960, 165, st.t - Wd('A03', 'tutan') + .25, { px: 84, panel: .82 }) });

// ═════════ P138 (L08): filmin son sorusu: kapalı ışık kapısı ve ona sırtını dönmüş siluet ═════════
// Kapı: sade, dikdörtgen, hafif kemerli iki kanat; figürsüz; koyu bir kaya sekisinin üstünde. Kanatlar düz siyah;
// ortadaki aralıktan, kenarlardan ve eşiğin altından ışık sızar. Girdabın gözü kapıdır: kollar kapının çevresinde döner.
// Aşağıda, aradaki boşluğun öte yanında, ona sırtını dönmüş küçük koyu siluet; arkasından geçen kolun aydınlık kenarına karşı okunur.
function kao_kapi(X, Y, w, h, a, t) {
  const { tx, px, tone } = GR, ar = w * .1;
  const shape = (dx, dy) => { const P = new Path2D(); P.moveTo(X - w / 2 - dx, Y + h); P.lineTo(X - w / 2 - dx, Y + ar - dy * .4); P.quadraticCurveTo(X, Y - ar - dy * 1.7, X + w / 2 + dx, Y + ar - dy * .4); P.lineTo(X + w / 2 + dx, Y + h); P.closePath(); return P; };
  // kanatların arkasından taşan ışık: kapıyı saran ince temiz kâğıt kenar
  const halo = shape(9 + 5 * a, 9 + 5 * a); tx.fillStyle = tone(1); tx.fill(halo); px.fillStyle = GR.hatch({ th: PI / 2, id: 7 }); px.fill(halo);
  const leaf = shape(0, 0); tx.fillStyle = tone(.025); tx.fill(leaf); px.fillStyle = GR.hatch({ th: PI / 2, id: 0 }); px.fill(leaf);
  // ortadaki aralık (kanatlar kapalı): ince, dibe doğru biraz açılan ışık
  const gap = 4 + 4 * a;
  tx.fillStyle = tone(1); tx.beginPath(); tx.moveTo(X - gap * .35, Y - ar * .85); tx.lineTo(X + gap * .35, Y - ar * .85); tx.lineTo(X + gap * .6, Y + h); tx.lineTo(X - gap * .6, Y + h); tx.closePath(); tx.fill();
  // kanat başına tek çökük tabla: ışık yanında (ortaya bakan) ince kâğıt kenar
  tx.save(); tx.clip(leaf);
  for (const sd of [-1, 1]) {
    const x0 = X + sd * w * .12, x1 = X + sd * w * .4, y0 = Y + h * .16, y1 = Y + h * .86;
    gol_vurus(tx, [[x0, y0], [x0, (y0 + y1) / 2], [x0, y1]], 5, .8, .15);
    gol_vurus(tx, [[x0, y0], [(x0 + x1) / 2, y0], [x1, y0]], 4, .7, .15);
  }
  tx.restore();
}
const KAO_P138 = [
  { ox: 1230, oy: 330, R: 330, a0: -2.6, span: 1.9, wd: 120, v: .78, seed: 11 },
  { ox: 1150, oy: 360, R: 600, a0: 1.05, span: 1.55, wd: 210, v: .72, seed: 12 },
  { ox: 1240, oy: 300, R: 660, a0: -.55, span: -1.6, wd: 190, v: .6, seed: 13 },
  { ox: 1120, oy: 420, R: 1020, a0: 2.05, span: 1.15, wd: 260, v: .5, seed: 14 },
  { ox: 1300, oy: 380, R: 1150, a0: -1.6, span: -1.0, wd: 240, v: .4, seed: 15 },
];
function kao_p138(t) {
  const tG = Wd('L08', 'gururu'), tK = Wd('L08', 'kapı');
  const a = E.io2(sav_u(t, tK - .3, tK + 1.8)), g = E.io2(sav_u(t, tG - .2, tG + 1.2));
  const DX = 1220, DY = 120, DW = 210, DH = 400, GY = DY + DH;
  kao_bosluk(t * .5, { cx: DX, cy: DY + DH * .5, kollar: KAO_P138 });
  PR.glow(DX, DY + DH * .5, DW * .4, DW * (1.5 + .5 * a), 1, .35 + .25 * a);
  // kapının sekisi: koyu kaya; üst yüzüne eşikten ışık vurur
  const SK = [[DX - 290, GY + 4], [DX - 120, GY - 2], [DX + 120, GY - 2], [DX + 300, GY + 6], [DX + 340, GY + 40], [DX + 250, GY + 120], [DX + 90, GY + 170], [DX - 60, GY + 160], [DX - 220, GY + 110], [DX - 320, GY + 46]];
  const SP = PR.rock(SK, { lit: [0, -1], hi: .05, mid: .03, lo: .02, seed: 21, th: .2, rim: 6, facets: 6 });
  PR.cuts(SK.slice(0, 4), [0, 1], { len: [10, 70], gap: [40, 100], w: 5, seed: 22, clip: SP, bend: .2 });
  kao_kapi(DX, DY, DW, DH, a, t);
  GR.tx.save(); GR.tx.clip(SP); gol_vurus(GR.tx, [[DX - DW * .75, GY + 5], [DX, GY + 9], [DX + DW * .75, GY + 5]], 12 + 6 * a, .98, .45); GR.tx.restore();
  // figürün kayası
  const FY = 930, FX = 600;
  const RK = [[FX - 230, FY + 8], [FX - 120, FY - 6], [FX + 20, FY - 10], [FX + 150, FY - 4], [FX + 250, FY + 12], [FX + 300, FY + 60], [FX + 240, FY + 160], [FX - 40, FY + 200], [FX - 260, FY + 150], [FX - 300, FY + 60]];
  const RP = PR.rock(RK, { lit: [.6, -.8], hi: .05, mid: .03, lo: .02, seed: 12, th: .3, rim: 5, facets: 6 });
  PR.cuts(RK.slice(0, 5), [-.2, 1], { len: [10, 60], gap: [40, 100], w: 5, seed: 14, clip: RP, bend: .2 });
  const br = Math.sin(t * .5) * 1.2;
  const J = kiy_seytan(t, { x: FX, gy: FY + br * .2, h: 34, facing: -1, twist: .35, head: lerp(-.1, -.22, g), lean: .04, armN: [.08, .15], armF: [-.05, .12], lum: .06, lit: [.8, -.6],
    open: -.3, lift: -.25, wingK: .8, cloak: 1.6 });
  kao_gogusAlev(J, t, g * .9, .9);
}
plan('P138', (ctx, st) => {
  const cam = camLerp({ cx: 975, cy: 540, z: 1 }, { cx: 945, cy: 540, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => kao_p138(st.t));
}, { tr: { type: 'fade', dur: .9 },
  over: (ctx, st) => {
    const tG = Wd('L08', 'gururu'), tK = Wd('L08', 'kapı');
    quote(ctx, 'gururu mu,', 560, 560, st.t - tG + .1, { px: 76, panel: .75 });
    quote(ctx, 'açılmayan kapı mı?', 1240, 790, st.t - tK + .2, { px: 76, panel: .75 });
  } });
