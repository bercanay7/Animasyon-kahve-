// sav grubu (SAV: cennetteki savaş, dokuz günlük düşüş; KAO: Kaos): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
// Kaos tarifi: ne ışık ne karanlık; ufuksuz, girdaplı boşluk. Yatay tarama yerine büyük, sakin, kavisli (bend) kütleler;
// karede tek küçük parlak hedef (cehennem ağzı, kapıdan sızan ışık, zincire asılı dünya, göğüsteki alev).
'use strict';
const sav_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));

// ═════════ Kaos boşluğu ═════════
// "Ne ışık ne karanlık": ışık hedefinin (cx, cy) çevresinde yassı bir aydınlık alan; çizgileri hedefin çevresinde kemerlenen kavisli akış (bend),
// hedefte temiz kâğıt, dışa doğru kalınlaşıp düz siyaha iner. Üstünde girdap kolları (kao_kol): düz siyah, hilal biçimli bulut kütleleri;
// hedefe bakan iç kenarı kabarık (bulut yumruları), orada sivrilen kâğıt kenar ışığı ve kütleye giren düzensiz beyaz vuruşlar.
// Kolların arası açık alan: koyu figür orada, açık zeminin önünde okunur.
// o: {cx, cy, sy (aydınlığın yassılığı), r0 (temiz kâğıt yarıçapı), r1 (siyaha varış), v (hedef tonu), k (zemin çizgisinin kavsi, 1/px), kollar: [kol...]}
function kao_bosluk(t, o = {}) {
  const { tx, px, tone } = GR, cx = o.cx ?? 960, cy = o.cy ?? 540, sy = o.sy ?? .62;
  tx.fillStyle = tone(.02); tx.fillRect(-1600, -1600, W + 3200, H + 3200);
  px.fillStyle = GR.hatch({ type: 'bend', ox: cx, oy: cy, a: o.a ?? 0, k: o.k ?? -1 / 2400, id: 2 }); px.fillRect(-1600, -1600, W + 3200, H + 3200);
  const r0 = o.r0 ?? 120, r1 = o.r1 ?? 1100, v = o.v ?? 1;
  tx.save(); tx.translate(cx, cy); tx.scale(1, sy); tx.translate(-cx, -cy);
  const g = tx.createRadialGradient(cx, cy, 0, cx, cy, r1);
  const f0 = r0 / r1; g.addColorStop(0, tone(v)); g.addColorStop(f0, tone(v * .97)); g.addColorStop(f0 + (1 - f0) * .25, tone(v * .62)); g.addColorStop(f0 + (1 - f0) * .55, tone(v * .34)); g.addColorStop(f0 + (1 - f0) * .8, tone(.12)); g.addColorStop(1, tone(.02));
  tx.fillStyle = g; tx.fillRect(cx - r1, cy - r1, r1 * 2, r1 * 2); tx.restore();
  return (o.kollar || []).map((K, i) => kao_kol(t, K, i, [cx, cy]));
}
// kol: {ox, oy (yay merkezi), R, a0 (başlangıç açısı), span (yay, radyan; işaret yönü verir), wd (kalınlık), nb (yumru sayısı), bump (yumru boyu, wd oranı),
//       lit (kenar ışığı 0..1), seed, rot (dönüş hızı), skew}
function kao_kol(t, K, i = 0, L = null) {
  const { tx, px, tone } = GR, q = rng((K.seed || 1) * 37 + i), m = 64, inner = [], outer = [];
  const a0 = K.a0 + (K.rot ?? .005) * t * Math.sign(K.span), ph = q() * TAU, ph2 = q() * TAU, R = K.R, wd = K.wd, nb = K.nb ?? 5, bp = K.bump ?? .3;
  const bph = q();
  for (let k = 0; k <= m; k++) {
    const u = k / m, a = a0 + K.span * u, e = Math.pow(Math.sin(PI * Math.pow(u, K.skew ?? .7)), .6);
    const Rr = R * (1 + (K.spiral ?? .05) * u + .02 * Math.sin(u * 4.5 + ph));
    const lobe = Math.pow(Math.abs(Math.sin(PI * (u * nb + bph))), .55);       // iç kenarda yuvarlak yumrular
    const wi = wd * .45 * e * (1 + bp * lobe), wo = wd * .55 * e * (1 + .12 * Math.sin(u * 3.3 + ph2));
    inner.push([K.ox + Math.cos(a) * (Rr - wi), K.oy + Math.sin(a) * (Rr - wi)]);
    outer.push([K.ox + Math.cos(a) * (Rr + wo), K.oy + Math.sin(a) * (Rr + wo)]);
  }
  const P = new Path2D(); spline(P, [...inner, ...outer.slice().reverse()], true, .8);
  GR.fill(P, tone(.02), { type: 'rad', cx: K.ox, cy: K.oy, id: 2 });
  const lit = K.lit ?? 1;
  if (lit > 0) {
    const Lx = L ? L[0] : K.ox, Ly = L ? L[1] : K.oy;
    tx.save(); tx.clip(P);
    // kenar ışığı: iç kenar boyunca, hedefe bakan yerde kalın, teğet yerlerde sivrilerek biter (parça parça)
    let seg = [];
    const flush = () => { if (seg.length > 3) gol_vurus(tx, seg, (K.rimW ?? 9) * lit, .97, .35); seg = []; };
    for (let k = 2; k <= m - 2; k++) {
      const a = inner[k - 1], b = inner[k + 1], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
      let nx = dy / l, ny = -dx / l; const toO = [outer[k][0] - inner[k][0], outer[k][1] - inner[k][1]]; if (nx * toO[0] + ny * toO[1] > 0) { nx = -nx; ny = -ny; }   // dışa (hedefe) normal
      let lx = Lx - inner[k][0], ly = Ly - inner[k][1]; { const ll = Math.hypot(lx, ly) || 1; lx /= ll; ly /= ll; }
      const f = nx * lx + ny * ly;
      if (f < .25) { flush(); continue; }
      seg.push([inner[k][0] - nx * 2.5, inner[k][1] - ny * 2.5]);
    }
    flush();
    tx.restore();
    // içe giren vuruşlar: yumruların ışıklı yanından kütleye
    const pts = inner.filter((_, k) => k % 3 === 0 && k > 3 && k < m - 3), dir = [outer[m >> 1][0] - inner[m >> 1][0], outer[m >> 1][1] - inner[m >> 1][1]];
    PR.cuts(pts, dir, { len: [14, 40 + wd * .45 * (K.cutL ?? 1)], gap: [46, 150], w: 6, v: .95, seed: (K.seed || 1) * 7 + 3, clip: P, bend: (K.bend ?? .3) * Math.sign(K.span) });
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
  const { tx, tone } = GR, h = J.h, [x, y] = kao_alevYer(J);
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
  { ox: 980, oy: 1150, R: 560, a0: -3.05, span: 1.15, wd: 190, nb: 4, seed: 1 },
  { ox: 820, oy: 1120, R: 760, a0: -.05, span: -1.2, wd: 230, nb: 5, seed: 2 },
  { ox: 1040, oy: 1240, R: 1120, a0: -2.75, span: 1.05, wd: 300, nb: 5, seed: 3 },
  { ox: 860, oy: 1200, R: 1300, a0: -.55, span: -1.0, wd: 320, nb: 5, seed: 4 },
];
function kao_p003(t) {
  const t0 = S('A03'), tT = Wd('A03', 'tutan'), X = 900, Y = 1020;
  const u = E.out2(sav_u(t, t0 - .4, tT)), hov = sav_u(t, tT - .6, tT + 1.5);
  kao_bosluk(t, { cx: X, cy: Y + 40, r0: 160, r1: 1250, sy: .7, kollar: KAO_P003 });
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
  { ox: 1250, oy: 320, R: 420, a0: -2.75, span: 1.5, wd: 170, nb: 4, seed: 11 },
  { ox: 1200, oy: 300, R: 560, a0: -.45, span: -1.25, wd: 200, nb: 4, seed: 13 },
  { ox: 1150, oy: 380, R: 900, a0: 1.95, span: 1.2, wd: 300, nb: 5, seed: 14 },
  { ox: 1300, oy: 380, R: 1000, a0: .55, span: -1.0, wd: 280, nb: 4, seed: 15 },
];
function kao_p138(t) {
  const tG = Wd('L08', 'gururu'), tK = Wd('L08', 'kapı');
  const a = E.io2(sav_u(t, tK - .3, tK + 1.8)), g = E.io2(sav_u(t, tG - .2, tG + 1.2));
  const DX = 1220, DY = 120, DW = 210, DH = 400, GY = DY + DH;
  kao_bosluk(t * .5, { cx: DX, cy: DY + DH * .55, r0: 200 + 40 * a, r1: 1350 + 100 * a, sy: .8, kollar: KAO_P138 });
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
  if (g > 0) PR.glow(FX - 8, FY - 34 * 5.3, 2, 34 * 3, 1, .35 * g);
  const J = kiy_seytan(t, { x: FX, gy: FY + br * .2, h: 34, facing: -1, twist: .35, head: lerp(-.1, -.22, g), lean: .04, armN: [.08, .15], armF: [-.05, .12], lum: .06, lit: [.8, -.6],
    open: -.3, lift: -.25, wingK: .8, cloak: 1.6 });
  kao_gogusAlev(J, t, g * .9, .9, false);
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
