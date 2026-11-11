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
// o: {cx, cy, sy (aydınlığın yassılığı), r0 (temiz kâğıt yarıçapı), r1 (siyaha varış), v (hedef tonu), k (zemin çizgisinin kavsi, 1/px), kollar: [kol...], lt (çekim içi zaman: kolların yavaş dönüşü)}
function kao_bosluk(t, o = {}) {
  const { tx, px, tone } = GR, cx = o.cx ?? 960, cy = o.cy ?? 540, sy = o.sy ?? .62;
  tx.fillStyle = tone(.02); tx.fillRect(-1600, -1600, W + 3200, H + 3200);
  px.fillStyle = GR.hatch({ type: 'bend', ox: cx, oy: cy, a: o.a ?? 0, k: o.k ?? -1 / 2400, id: 2 }); px.fillRect(-1600, -1600, W + 3200, H + 3200);
  const r0 = o.r0 ?? 120, r1 = o.r1 ?? 1100, v = o.v ?? 1;
  tx.save(); tx.translate(cx, cy); tx.scale(1, sy); tx.translate(-cx, -cy);
  const g = tx.createRadialGradient(cx, cy, 0, cx, cy, r1);
  const f0 = r0 / r1; g.addColorStop(0, tone(v)); g.addColorStop(f0, tone(v * .97)); g.addColorStop(f0 + (1 - f0) * .25, tone(v * .62)); g.addColorStop(f0 + (1 - f0) * .55, tone(v * .34)); g.addColorStop(f0 + (1 - f0) * .8, tone(.12)); g.addColorStop(1, tone(.02));
  tx.fillStyle = g; tx.fillRect(cx - r1, cy - r1, r1 * 2, r1 * 2); tx.restore();
  return (o.kollar || []).map((K, i) => kao_kol(o.lt ?? 0, K, i, [cx, cy]));
}
// kol: {ox, oy (yay merkezi), R, a0 (başlangıç açısı), span (yay, radyan; işaret yönü verir), wd (kalınlık), nb (yumru sayısı), bump (yumru boyu, wd oranı),
//       lit (kenar ışığı 0..1), seed, rot (dönüş hızı), skew}
function kao_kol(t, K, i = 0, L = null) {
  const { tx, px, tone } = GR, q = rng((K.seed || 1) * 37 + i), m = 64, inner = [], outer = [];
  const a0 = K.a0 + (K.rot ?? .005) * t * Math.sign(K.span), ph = q() * TAU, ph2 = q() * TAU, R = K.R, wd = K.wd, nb = K.nb ?? 5, bp = K.bump ?? .3;
  const bph = q();
  for (let k = 0; k <= m; k++) {
    const u = k / m, a = a0 + K.span * u, yr = K.yirtik || 0, e = Math.pow(Math.sin(PI * Math.pow(u, K.skew ?? .7)), lerp(.6, .3, yr));
    const Rr = R * (1 + (K.spiral ?? .05) * u + .02 * Math.sin(u * 4.5 + ph));
    const lobe = .5 - .5 * Math.cos(TAU * (u * nb + bph));       // iç kenarda yuvarlak yumrular
    const rag = yr ? (noise1(u * 7 + (K.seed || 1) * 3.1, 3) - .5) * .5 + (noise1(u * 19 + (K.seed || 1), 5) - .5) * .18 : 0;   // yırtık duman kenarı
    const wi = wd * .45 * e * (1 + bp * lobe + yr * rag), wo = wd * .55 * e * (1 + .12 * Math.sin(u * 3.3 + ph2) + yr * (noise1(u * 6 + (K.seed || 1) * 7, 4) - .5) * .45);
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
    const flush = () => { if (seg.length > 3) gol_vurus(tx, seg, (K.rimW ?? 11) * lit, .97, .35); seg = []; };
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
    const pts = inner.filter((_, k) => k % 3 === 0 && k > m * .15 && k < m * .85), dir = [outer[m >> 1][0] - inner[m >> 1][0], outer[m >> 1][1] - inner[m >> 1][1]];
    PR.cuts(pts, dir, { len: [50, 90 + wd * .55 * (K.cutL ?? 1)], gap: [110, 260], w: 7, v: .95, seed: (K.seed || 1) * 7 + 3, clip: P, bend: (K.bend ?? .3) * Math.sign(K.span) });
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
  PR.flameBank(X - 340 * s, X + 340 * s, Y + 80, 280 * s * e, t, 117, { n: 7, wr: .42, curl: .4, speed: .55, solidBelow: 500, strokeAbove: 90, strip: .3, frags: false, env: f => .3 + .7 * Math.sin(f * PI) });
  const L = [[-80, Y - 230 * s], [X - 720 * s, Y - 170 * s], [X - 560 * s, Y - 110 * s], [X - 450 * s, Y - 50 * s], [X - 380 * s, Y + 20 * s], [X - 330 * s, Y + 110 * s], [X - 310 * s, H + 60], [-80, H + 60]];
  const R = [[W + 80, Y - 200 * s], [X + 740 * s, Y - 160 * s], [X + 600 * s, Y - 104 * s], [X + 480 * s, Y - 52 * s], [X + 400 * s, Y + 16 * s], [X + 340 * s, Y + 104 * s], [X + 310 * s, H + 60], [W + 80, H + 60]];
  const RP1 = PR.rock(L, { lit: [.75, -.66], hi: .05, mid: .03, lo: .02, seed: 3, th: -.6, rim: 6, facets: 7 });
  PR.cuts(L.slice(1, 6), [-.45, .9], { len: [14, 120], gap: [44, 120], w: 6, seed: 8, clip: RP1, bend: .3 });
  const RP2 = PR.rock(R, { lit: [-.75, -.66], hi: .05, mid: .03, lo: .02, seed: 6, th: .6, rim: 6, facets: 7 });
  PR.cuts(R.slice(1, 6), [.45, .9], { len: [14, 120], gap: [44, 120], w: 6, seed: 9, clip: RP2, bend: -.3 });
}
const KAO_P003 = [
  { ox: 980, oy: 1150, R: 560, a0: -3.05, span: 1.15, wd: 170, nb: 4, seed: 1 },
  { ox: 820, oy: 1120, R: 780, a0: -.05, span: -1.2, wd: 210, nb: 6, seed: 2, bump: .22 },
  { ox: 1040, oy: 1260, R: 1180, a0: -2.75, span: 1.05, wd: 260, nb: 8, seed: 3, bump: .2 },
  { ox: 860, oy: 1220, R: 1380, a0: -.55, span: -1.0, wd: 280, nb: 8, seed: 4, bump: .2 },
];
// ince, soluk zincir: halkalı kâğıt çizgisi (3–4 px), sarkma sag, k: halka boyu çarpanı (0 → söner), len: 0..1 görünen uzunluk (üstten)
function kao_inceZincir(x0, y0, x1, y1, sag, k = 1, len = 1) {
  if (k <= .05 || len <= 0) return;
  const { tx, tone } = GR, D = Math.hypot(x1 - x0, y1 - y0), n = Math.floor(D / 15);
  const pos = f => [lerp(x0, x1, f), lerp(y0, y1, f) + Math.sin(f * PI) * sag];
  tx.save(); tx.strokeStyle = tone(.95); tx.lineWidth = 3.5 * Math.min(1, k + .2); tx.lineCap = 'round';
  for (let i = 0; i < n; i++) { const f = (i + .5) / n; if (f > len) break;
    const p = pos(f), q = pos(Math.min(1, f + .01)), a = Math.atan2(q[1] - p[1], q[0] - p[0]);
    tx.beginPath(); if (i % 2) { tx.moveTo(p[0] - Math.cos(a) * 8 * k, p[1] - Math.sin(a) * 8 * k); tx.lineTo(p[0] + Math.cos(a) * 8 * k, p[1] + Math.sin(a) * 8 * k); }
    else tx.ellipse(p[0], p[1], 9 * k, 4.5 * k, a, 0, TAU);
    tx.strokeStyle = tone(.02); tx.lineWidth = 8 * Math.min(1, k + .2); tx.stroke();          // koyu ayırma: açık zeminde de okunur
    tx.strokeStyle = tone(.97); tx.lineWidth = 3.5 * Math.min(1, k + .2); tx.stroke(); }
  tx.restore();
}
function kao_p003(t) {
  const t0 = S('A03'), tT = Wd('A03', 'tutan'), X = 900, Y = 1020;
  // yükseliş: ağızdan hızla çıkar; "tutan"da zincir gerilir ve yükselişi keser
  const tc = Math.min(t, tT + .3), u = E.out2(sav_u(tc, t0 - .4, tT + 1.4)), hov = sav_u(t, tT, tT + 1.5);
  const grow = E.io2(sav_u(t, t0 - .4, tT + .5));                         // figür kameraya yaklaşır gibi büyür (yörünge öne gelir)
  kao_bosluk(t, { cx: X, cy: Y + 30, r0: 40, r1: 1350, sy: .7, v: .8, kollar: KAO_P003, lt: t - t0 });
  kao_agiz(t, X, Y, { e: lerp(1, .7, u) });
  const tug = Math.exp(-Math.pow((t - tT - .4) / .18, 2)) * 16;             // gerilme anında aşağı çekiş
  const x = lerp(860, 990, E.io2(u)), y = lerp(960, 600, u) + tug + Math.sin(t * 1.6) * 5 * hov, h = lerp(22, 46, grow);
  const fl = Math.sin(t * lerp(5.5, 2.4, hov)) * lerp(.5, .28, hov);
  const J = kao_figur(t, { x, y, h, lean: lerp(-.12, .02, u), head: lerp(.3, .05, hov) - .1 * tug / 16, open: .95, lift: .62, flap: fl, lum: .1, lit: [0, 1], seed: 7,
    legN: [.05, -.12], legF: [-.06, -.22], armN: [-.25, .2], armF: [-.15, .25] }, 1, 1.4);
  // zincir: "tutan"da ayak bileğinden ağza iner, gerilir, söner (halkalar küçülerek)
  const ap = E.out2(sav_u(t, tT - .15, tT + .25)), taut = E.io2(sav_u(t, tT + .1, tT + .45)), off = sav_u(t, tT + 1.0, tT + 1.9);
  if (ap > 0 && off < 1) kao_inceZincir(J.anN[0], J.anN[1] + h * .1, X + 20, Y - 10, lerp(70, 0, taut), 1 - off, ap);
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
  // kasa: kanatlardan biraz geniş koyu çerçeve; kanatla kasa arasından ışık taşar
  const fr = shape(30, 30); tx.fillStyle = tone(.025); tx.fill(fr); px.fillStyle = GR.hatch({ th: PI / 2, id: 0 }); px.fill(fr);
  // kanatların arkasından taşan ışık: kanatla kasa arasındaki ince temiz kâğıt aralık
  const halo = shape(6 + 4 * a, 6 + 4 * a); tx.fillStyle = tone(1); tx.fill(halo); px.fillStyle = GR.hatch({ th: PI / 2, id: 7 }); px.fill(halo);
  const leaf = shape(0, 0); tx.fillStyle = tone(.025); tx.fill(leaf); px.fillStyle = GR.hatch({ th: PI / 2, id: 0 }); px.fill(leaf);
  // ortadaki aralık (kanatlar kapalı): ince, dibe doğru biraz açılan ışık
  const gap = 4 + 4 * a;
  tx.fillStyle = tone(1); tx.beginPath(); tx.moveTo(X - gap * .35, Y - ar * .85); tx.lineTo(X + gap * .35, Y - ar * .85); tx.lineTo(X + gap * .6, Y + h); tx.lineTo(X - gap * .6, Y + h); tx.closePath(); tx.fill();
}
const KAO_P138 = [
  { ox: 1330, oy: 760, R: 960, a0: -2.9, span: 1.2, wd: 150, nb: 9, seed: 11, bump: .18 },
  { ox: 980, oy: 300, R: 780, a0: -.62, span: 1.35, wd: 170, nb: 9, seed: 14, bump: .18 },
  { ox: 1300, oy: 260, R: 1080, a0: 3.12, span: -.8, wd: 120, nb: 8, seed: 15, bump: .2 },
];
function kao_p138(t) {
  const tG = Wd('L08', 'gururu'), tK = Wd('L08', 'kapı');
  const a = E.io2(sav_u(t, tK - .3, tK + 1.8)), g = E.io2(sav_u(t, tG - .2, tG + 1.2));
  const DX = 1220, DY = 120, DW = 210, DH = 400, GY = DY + DH;
  kao_bosluk(t, { lt: (t - S('L08')) * .5, k: -1 / 9000, cx: DX, cy: DY + DH * .55, r0: 200 + 40 * a, r1: 1350 + 100 * a, sy: .8, kollar: KAO_P138 });
  // kapının sekisi: koyu kaya; üst yüzüne eşikten ışık vurur
  const SK = [[DX - 160, GY + 8], [DX - 60, GY - 1], [DX + 90, GY - 1], [DX + 165, GY + 10], [DX + 175, GY + 60], [DX + 215, GY + 120], [DX + 205, GY + 210], [DX + 260, GY + 330], [DX + 300, H + 60], [DX - 290, H + 60], [DX - 230, GY + 380], [DX - 200, GY + 250], [DX - 215, GY + 140], [DX - 180, GY + 60]];
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
    open: -.45, lift: -.3, wingK: .55, cloak: 1.7 });
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

// ═════════ P038 (D09): dokuz günlük düşüş ═════════
// Zifiri karanlık. Sol üstte cennetin kıyısındaki yarık: oradan inen geniş, sönük ışık kaması (çizgiler düşüş doğrultusunda: akış izi).
// Bedenler kamanın içinde çapraz düşer: baş aşağı, kanatlar yukarı savrulmuş koyu siluetler; ışık yukarıdan (üst kenarlarında kenar ışığı).
// Uzaktakiler küçük ve yavaş, yakındakiler büyük ve hızlı. "ağzını açıp"ta altta cehennem ağzı açılır (içi alev, temiz kâğıt): bedenler ona karşı siluet;
// "yuttu"dan sonra yeni beden gelmez, "kapandı"da ağız kapanır, yarığın ışığı söner, kare siyaha döner.
const SAV_DUS = (() => {
  const r = rng(909), L = [];
  for (let i = 0; i < 15; i++) {
    const z = Math.pow(r(), 1.6), h = lerp(13, 62, z);            // derinlik: 0 uzak … 1 yakın
    L.push({ h, z, off: (r() - .5) * 2, s0: r(), sp: lerp(.16, .42, z) * (.85 + r() * .3), rot0: PI * (.62 + r() * .5), spin: (r() - .5) * .5,
      pose: r(), seed: 300 + i, wing: r() < .8 });
  }
  return L.sort((a, b) => a.z - b.z);                               // uzak önce
})();
function sav_dusen(t, x, y, h, rot, B) {
  const tum = Math.sin(t * 1.3 + B.seed) * .25;
  const J = SF.rig({ x, y, h, facing: B.pose < .5 ? 1 : -1, twist: .3, lean: rot, head: -.3 + tum * .5, shTilt: tum * .3,
    armN: [lerp(-2.6, -1.6, B.pose) + tum, .5], armF: [lerp(-2.2, -.9, B.pose) - tum, .7], legN: [lerp(.2, .7, B.pose), -lerp(.3, 1.2, B.pose)], legF: [-lerp(.1, .5, B.pose), -lerp(.6, .2, B.pose)] });
  const LIT = [0, -1];
  // kanatlar: düşüşte yukarı savrulmuş (gövdenin dönüşünden bağımsız V); sade koyu kütle, üst kenarda ince ışık
  if (B.wing) for (const side of [-1, 1]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    cen_kanatKoyu(sh[0], sh[1], side, h * (side < 0 ? 5.6 : 5) * (.9 + .2 * B.pose), { lift: .8 + .15 * Math.sin(t * 2.1 + B.seed + side), open: .95, seed: B.seed + side, t, L: { x: sh[0], y: sh[1] - 900 } });
  }
  SF.draw(J, { lum: .04, lit: LIT, t, legs: true, skirt: false, armor: false, eye: 0, wind: 1.2, cloak: h > 30 ? .9 : false, halo: 0, lines: 0, seed: B.seed });
}
function sav_p038(t) {
  const { tx, px, tone } = GR, t0 = S('D09'), tA = Wd('D09', 'ağzını'), tY = Wd('D09', 'yuttu'), tK = Wd('D09', 'kapandı');
  const m = E.out3(sav_u(t, tA - .25, tA + .9)) * (1 - E.in3(sav_u(t, tK - .35, tK + .45)));
  const son = 1 - E.io2(sav_u(t, tY, tK + .4));                     // yarığın ışığı söner
  const th = 1.15, d = [Math.cos(th), Math.sin(th)], n = [-d[1], d[0]], SX = 560, SY = -20;
  // ışık kaması: yarıktan cehennem ağzına
  const K = new Path2D(); poly(K, [[SX - 60, SY], [SX + 70, SY], [SX + d[0] * 1300 + n[0] * -440, SY + d[1] * 1300 + n[1] * -440], [SX + d[0] * 1300 + n[0] * 440, SY + d[1] * 1300 + n[1] * 440]], true);
  const g = tx.createLinearGradient(SX, SY, SX + d[0] * 1250, SY + d[1] * 1250);
  g.addColorStop(0, tone(.72 * son + .02)); g.addColorStop(.3, tone(.5 * son + .02)); g.addColorStop(.65, tone(.3 * son + .02)); g.addColorStop(1, tone(.12 * son + .02));
  GR.fill(K, g, { th: th, id: 7 });
  if (son > .02) { const Y = new Path2D(); poly(Y, [[SX - 110, -30], [SX - 70, 6 * son], [SX - 10, 14 * son], [SX + 50, 9 * son], [SX + 120, -30]], true); tx.fillStyle = tone(.98 * son + .02); tx.fill(Y); }
  // cehennem ağzı: içi alev ışığı (temiz kâğıt); kırık, koyu dudak
  const MX = 1240, MY = 1130;
  let MP = null, pts = [];
  if (m > .01) {
    PR.glow(MX, MY - 60, 40, 560 * m, 1, .45 * m);
    MP = new Path2D(); const q = rng(77);
    for (let i = 0; i < 44; i++) { const a = PI + i / 43 * PI, j = .84 + .16 * q(); pts.push([MX + Math.cos(a) * 560 * m * j, MY + Math.sin(a) * 230 * m * (.72 + .28 * q())]); }
    pts.push([MX + 620 * m, MY + 100], [MX - 620 * m, MY + 100]);
    poly(MP, pts, true);
    const gi = tx.createLinearGradient(0, MY - 230 * m, 0, MY + 40); gi.addColorStop(0, tone(.75)); gi.addColorStop(.5, tone(.4)); gi.addColorStop(1, tone(.12));
    GR.fill(MP, gi, { th: 0, id: 3 });
  }
  // düşen bedenler (ağza girenler ağzın içinde küçülür; alevler önlerine biner)
  const span = 1500, inMouth = [];
  for (const B of SAV_DUS) {
    const lt = t - t0 + 1.2, raw = B.s0 + B.sp * lt * (1 + .4 * B.z), cyc = Math.floor(raw), cycY = Math.floor(B.s0 + B.sp * (tY - t0 + 1.2) * (1 + .4 * B.z));
    if (cyc > cycY) continue;                                       // "yuttu"dan sonra yeni beden yok
    const u = raw - cyc, sp = -250 + u * span, w = B.off * clamp(40 + .25 * sp, 30, 330), x = SX + d[0] * sp + n[0] * w, y = SY + d[1] * sp + n[1] * w;
    const rot = B.rot0 + B.spin * (t - t0);
    if (MP && y > MY - 230 * m * .55 && Math.abs(x - MX) < 520 * m) { const k = clamp(1 - (y - (MY - 230 * m * .55)) / 200); if (k > .15) inMouth.push([x, y, B.h * k, rot, B]); continue; }
    if (t > tK - .2) continue;
    sav_dusen(t, x, y, B.h, rot, B);
  }
  if (MP) {
    tx.save(); px.save(); tx.clip(MP); px.clip(MP);
    for (const [x, y, h, rot, B] of inMouth) sav_dusen(t, x, y, h, rot, B);
    PR.flameBank(MX - 560 * m, MX + 560 * m, MY + 30, 330 * m, t, 131, { n: 9, wr: .42, curl: .4, speed: .6, solidBelow: 500, strokeAbove: 70, strip: .25, frags: false, env: f => .45 + .55 * Math.sin(f * PI) });
    tx.restore(); px.restore();
    // dudak: ağzın çevresinde kırık koyu kaya kuşağı, içe bakan kenarında ince ışık
    const R = [];
    for (let i = 0; i < pts.length - 2; i++) R.push(pts[i]);
    const out = R.map(([x, y], i) => { const a = PI + i / 43 * PI; return [x + Math.cos(a) * 70 * m, y + Math.sin(a) * 60 * m - 10 * m * (i % 3 === 0)]; });
    const LP = new Path2D(); poly(LP, [...R, ...out.reverse()], true);
    GR.fill(LP, tone(.02), { th: 0, id: 4 });
    tx.save(); tx.clip(LP); gol_vurus(tx, R.filter((_, i) => i % 2 === 0).map(([x, y]) => [x, y - 2]), 9 * m, .97, .25); tx.restore();
  }
}
plan('P038', (ctx, st) => {
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => sav_p038(st.t), [.02, 0, 1]);
}, { tr: { type: 'cut' }, mb: 3,
  over: (ctx, st) => {
    if (NOTEXT) return;
    const t0 = st.at, tY = Wd('D09', 'yuttu'), k = clamp((st.t - t0) / (tY - t0)) * 9, i = Math.min(8, Math.floor(k));
    const RN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'], tK = Wd('D09', 'kapandı');
    const a = clamp((st.t - t0) / .4) * (1 - clamp((st.t - tK) / .6));
    if (a <= 0) return;
    const fr = k - Math.floor(k), pop = i < 8 ? clamp(fr / .15) : 1;
    txt(ctx, RN[i], 1600, 220, { px: 120, ls: 6, a: a * (.55 + .45 * pop) });
    txt(ctx, 'dokuz gün', 1600, 320, { font: FONT.alinti(54), px: 54, a: a * .9 });
  } });

// ═════════ Cennetteki savaş: ortak ═════════
// Geçiş tarifi: gök açık (ışık merkezi temiz kâğıt, dışa seyrek ışınsal tarama); ortada savaş dumanı: koyu, sakin bulut bankı (cen_bank);
// önde açık teras. Beyaz figürler koyu bankın önünde; Şeytan'ın ışığı plandaki lum ile azalır (kanadı ve bedeni giderek koyulaşır).
// Kılıç: elden çıkan düz, sivri bıçak; kabza ve balçak. v: bıçak tonu (koyu zeminde 1 kâğıt, açık zeminde 0 mürekkep)
function sav_kilic(x, y, ang, L, v = 1, w = 6) {
  const { tx, px, tone } = GR, c = Math.cos(ang), s = Math.sin(ang), nx = -s, ny = c;
  const B = new Path2D(); poly(B, [[x + nx * w * .5, y + ny * w * .5], [x + c * L * .82 + nx * w * .5, y + s * L * .82 + ny * w * .5], [x + c * L, y + s * L], [x + c * L * .82 - nx * w * .5, y + s * L * .82 - ny * w * .5], [x - nx * w * .5, y - ny * w * .5]], true);
  const G = new Path2D(); poly(G, [[x + c * w * .3 + nx * w * 2.4, y + s * w * .3 + ny * w * 2.4], [x + c * w * 1.1 + nx * w * 2.4, y + s * w * 1.1 + ny * w * 2.4], [x + c * w * 1.1 - nx * w * 2.4, y + s * w * 1.1 - ny * w * 2.4], [x + c * w * .3 - nx * w * 2.4, y + s * w * .3 - ny * w * 2.4]], true);
  if (v > .5) { tx.save(); tx.lineWidth = 5; tx.strokeStyle = tone(.02); tx.stroke(B); tx.restore(); }   // açık bıçak: ince koyu ayırma (açık zeminde de okunsun)
  tx.fillStyle = tone(v); tx.fill(B); tx.fillStyle = tone(v > .5 ? .02 : 0); tx.fill(G);
  px.fillStyle = GR.hatch({ th: ang, id: 9 }); px.fill(B);
}
// eli kılıçlı figür: J.wr* noktasında, ön kol doğrultusuna off açısı eklenerek
function sav_eldenKilic(J, k = 'N', off = 0, L = 5, v = 1) {
  const el = J['el' + k], wr = J['wr' + k], a = Math.atan2(wr[1] - el[1], wr[0] - el[0]) + off * J.f;
  sav_kilic(wr[0] + Math.cos(a) * J.h * .3, wr[1] + Math.sin(a) * J.h * .3, a, L * J.h, v, Math.max(3, J.h * .09));
}
// Şeytan (cennette): lum ile kararan figür. lum ≥ .6: açık beden (mürekkep kontur ve vuruşlar; Abdiel'in düz kâğıdından ayrılır), kanat açık ama taralı;
// lum azaldıkça kanat ve beden koyulaşır. p: {x, y (kalça), h, facing, lum, L, t, head, lean, twist, armN, armF, legN, legF, open, lift, wingS, cloak, kilic: {k, off, len}}
function sav_seytan(p) {
  const h = p.h, t = p.t || 0, lum = p.lum ?? .75;
  const J = SF.rig({ x: p.x, y: p.y, h, facing: p.facing ?? 1, twist: p.twist ?? .3, lean: p.lean ?? 0, head: p.head ?? .1, shTilt: p.shTilt ?? -.03,
    armN: p.armN || [.2, .3], armF: p.armF || [-.1, .2], legN: p.legN || [.12, -.05], legF: p.legF || [-.1, -.03] });
  let lx = p.L.x - J.shC[0], ly = p.L.y - J.shC[1]; { const l = Math.hypot(lx, ly) || 1; lx /= l; ly /= l; }
  const LIT = [lx, ly], dk = clamp((.8 - lum) / .45);           // kanadın koyuluğu: .75 → .1, .5 → .67
  for (const [side, P] of [[-1, { span: (p.wingS ?? 8.2) * h, seed: 51, root: .1, rot: -.08 }], [1, { span: (p.wingS ?? 8.2) * .9 * h, seed: 52, root: .12, rot: .1 }]]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    GR.frame(sh[0] - side * h * .25, sh[1] + h * .15, P.rot + (p.lean || 0) * J.f, side, 1);
    KN.feathered({ span: P.span, open: p.open ?? .7, lift: p.lift ?? .5, droop: p.droop ?? .3, ruin: .15 + .4 * dk, dark: lerp(.08, .85, dk), rim: .7, t, seed: P.seed, root: P.root, lit: [LIT[0] * side, LIT[1]] });
    GR.unframe();
  }
  const kl = p.kilic;
  if (kl && kl.k === 'F') sav_eldenKilic(J, 'F', kl.off || 0, kl.len || 5, kl.v ?? 1);
  SF.draw(J, { lum, lit: LIT, t, legs: true, skirt: true, eye: 0, wind: .5, cloak: p.cloak ?? .9, halo: 0, lines: 1.5, seed: p.seed || 9 });
  if (kl && kl.k !== 'F') sav_eldenKilic(J, 'N', kl.off || 0, kl.len || 5, kl.v ?? 1);
  return J;
}
// beyaz melek (Abdiel, Mikail): cen_basmelek (düz kâğıt siluet + beyaz kanat) + kılıç
function sav_melek(p) {
  const kl = p.kilic;
  const J = cen_basmelek(Object.assign({ spear: false, cloak: .6 }, p, { mid: kl && kl.k === 'F' ? (J) => sav_eldenKilic(J, 'F', kl.off || 0, kl.len || 5, kl.v ?? 1) : null }));
  if (kl && kl.k !== 'F') sav_eldenKilic(J, 'N', kl.off || 0, kl.len || 5, kl.v ?? 1);
  return J;
}
// savaş levhası zemini: gök, savaş dumanı bankı, ön teras. o: {L, by (bank üst kenarı), ty (teras), dark (bankın üstünde ikinci koyu küme: 0..1), seed}
function sav_zemin(t, o) {
  const L = o.L;
  cen_gok(L, { r0: o.r0 ?? 230, r1: o.r1 ?? 1300, v: o.v ?? .66, n: 96 });
  if (o.ust) for (const U of o.ust) cen_bank(Object.assign({ L, cuts: .7, ends: true, drift: t * 4 }, U));
  const B = cen_bank({ x0: -160 + (o.bx0 || 0), x1: W + 160 + (o.bx1 || 0), y: o.by ?? 300, amp: o.amp ?? 70, wl: o.wl ?? 430, yb: (o.ty ?? 780) + 30, seed: o.seed || 31, L, cuts: .8, ends: false, drift: t * 6 });
  const T = o.ty != null ? cen_teras({ x0: -160 + (o.bx0 || 0), x1: W + 160 + (o.bx1 || 0), y: o.ty, d: 46, seed: (o.seed || 31) + 1, L, cuts: .6 }) : null;
  return { B, T };
}

function sav_kart(ctx, title, lt, d, o = {}) {
  if (NOTEXT) return;
  const a = clamp(lt / .6) * clamp((d - lt) / .6); if (a <= 0) return;
  const x = o.x ?? W / 2, y = o.y ?? 250, px = o.px || 96;
  ctx.save(); ctx.globalAlpha *= E.sine(a);
  const u = E.out3(clamp(lt / 1.1)), lw = 240 * u;
  ctx.strokeStyle = INK_CSS; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x - lw, y - px * .82); ctx.lineTo(x + lw, y - px * .82); ctx.stroke();
  txt(ctx, title, x, y, { px, ls: 12, col: INK_CSS });
  ctx.restore();
}

// ═════════ P030 (D01): bölüm kartı "DOKUZ GÜN"; kınından çıkan kılıç sıraları ışığı yakalar ═════════
// Üç saf kütlesi (koyu, uzaklaştıkça küçülür); "kılıçlar"da soldan sağa bir dalga: her kılıç kınından çıkıp dikilir, dikildiği an ışığı yakalar (kalınlaşan kâğıt bıçak).
const SAV_P030 = (() => { const r = rng(303), R = [];
  for (const [y, h, n, sd] of [[660, 11, 16, 1], [790, 16, 12, 2], [970, 24, 9, 3]]) { const L = []; for (let i = 0; i < n; i++) { const x = -60 + (i + .5 + (r() - .5) * .7) / n * 2040; L.push({ x, ph: r(), lean: (r() - .5) * .16, L: 7 + r() * 2.5 }); } R.push({ y, h, L, sd }); }
  return R; })();
function sav_p030(t) {
  const L = { x: 960, y: 120 }, tK = Wd('D01', 'kılıçlar');
  cen_gok(L, { r0: 420, r1: 1500, v: .7, n: 96 });
  cen_bulutKat({ x0: -300, x1: W + 300, y: 520, h: 220, yb: H + 100, seed: 41, L, t, n: 7 });
  for (const R of SAV_P030) {
    GR.tx.save(); GR.tx.translate(0, -5); cen_safKutle({ x0: -80, x1: W + 80, y: R.y, h: R.h, seed: 40 + R.sd, v: .9, nSp: 0, folds: 0 }); GR.tx.restore();   // üst kenar ışığı: sıralar birbirinden ayrılır
    cen_safKutle({ x0: -80, x1: W + 80, y: R.y, h: R.h, seed: 40 + R.sd, v: .03, nSp: 0 });
    // kılıçlar: dalga soldan sağa; derin sıra biraz geç
    for (const k of R.L) {
      const t0 = tK - .2 + (k.x + 60) / 2040 * 1.6 + R.sd * .15 + k.ph * .2, u = E.out3(sav_u(t, t0, t0 + .55));
      if (u <= 0) continue;
      const len = k.L * 1.3 * R.h * u, base = [k.x + R.h * .8, R.y - 4.6 * R.h], a = -PI / 2 + k.lean + (1 - u) * .5;
      const flash = Math.exp(-Math.pow((t - t0 - .55) / .35, 2));
      sav_kilic(base[0], base[1], a, len, 1, Math.max(3, R.h * (.16 + .12 * flash)));
    }
  }
}
plan('P030', (ctx, st) => levha(ctx, { cx: 960, cy: 540, z: 1 }, () => sav_p030(st.t)),
  { tr: { type: 'black', dur: 1.4, end: true }, over: (ctx, st) => sav_kart(ctx, 'DOKUZ GÜN', st.lt - 1.0, st.d + .3 - 1.0, { y: 260 }) });   // önceki levhanın yazısı söndükten ≥ 0,3 sn sonra belirir

// ═════════ P036 (D07): solda duman püskürten toplar (asilerin icadı); sağda kökünden sökülüp fırlatılan dağlar ═════════
// 17. yüzyıl gravür dili: dökme namlu (halkalı), tahta kundak, parmaklı tekerlek; namludan koyu, kenarı ışıklı duman. Dağlar: havada koyu kaya kütleleri, altında sarkan kök çizgileri.
function sav_top(x, y, s, a, fire, t, seed) {
  const { tx, px, tone } = GR, c = Math.cos(a), sn = Math.sin(a), P = (u, v) => [x + c * u * s - sn * v * s, y + sn * u * s + c * v * s];
  // kundak
  const K = new Path2D(); poly(K, [P(-1.25, .08), P(.15, .12), P(.25, .34), P(-1.1, .52), P(-1.45, .4)], true); GR.fill(K, tone(.03), { th: a, id: 4 });
  // namlu: kuyruktan ağza incelen, halkalı
  const N = new Path2D(); poly(N, [P(-1.05, -.13), P(-.95, -.2), P(1.15, -.12), P(1.18, -.15), P(1.25, -.15), P(1.25, .1), P(1.18, .1), P(1.15, .07), P(-.95, .14), P(-1.05, .08)], true);
  GR.fill(N, tone(.04), { th: a, id: 9 });
  tx.save(); tx.clip(N); gol_vurus(tx, [P(-.9, -.15), P(.2, -.12), P(1.15, -.09)], s * .045, .92, .3); for (const u of [-.6, .1, .8]) gol_vurus(tx, [P(u, -.18), P(u + .02, -.03), P(u, .12)], s * .03, .85, .2); tx.restore();
  // tekerlek: parmaklı
  const wx = P(-.45, .5), R = s * .36; tx.save(); tx.lineWidth = s * .07; tx.strokeStyle = tone(.03); tx.beginPath(); tx.arc(wx[0], wx[1], R, 0, TAU); tx.stroke();
  tx.lineWidth = s * .035; for (let k = 0; k < 6; k++) { const aa = k / 6 * PI + .2; tx.beginPath(); tx.moveTo(wx[0] - Math.cos(aa) * R, wx[1] - Math.sin(aa) * R); tx.lineTo(wx[0] + Math.cos(aa) * R, wx[1] + Math.sin(aa) * R); tx.stroke(); }
  tx.restore();
  // ağız ateşi ve duman
  if (fire > 0) {
    const m = P(1.3, -.02);
    for (let i = 0; i < 4; i++) { const f = clamp(fire * 1.4 - i * .14); if (f <= 0) continue;
      sav_duman(m[0] + c * s * (.7 + i * 1.0) * f, m[1] + sn * s * (.7 + i * 1.0) * f - i * s * .32 * f, s * (.36 + i * .2) * Math.sqrt(f), seed * 7 + i, t); }
    const fl = Math.exp(-Math.pow((fire - .08) / .08, 2));
    if (fl > .05) { const F = new Path2D(); poly(F, [m, P(1.3 + .9 * fl, -.3), P(1.3 + 1.5 * fl, -.02), P(1.3 + .9 * fl, .26)], true); tx.fillStyle = tone(1); tx.fill(F); }
  }
}
// duman öbeği: birkaç yuvarlak yumrudan koyu kütle; üst (ışık) kenarında ince kâğıt hilal
function sav_duman(x, y, r, seed, t) {
  const { tx, px, tone } = GR, q = rng(seed), P = new Path2D();
  for (let i = 0; i < 5; i++) { const a = q() * TAU, d = r * .55 * q(), rr = r * (.45 + .35 * q()), cx = x + Math.cos(a) * d * 1.3, cy = y + Math.sin(a) * d * .7 + Math.sin(t * .8 + i) * 2; P.moveTo(cx + rr, cy); P.arc(cx, cy, rr, 0, TAU); }
  tx.save(); tx.translate(0, -Math.max(3, r * .06)); tx.fillStyle = tone(.95); tx.fill(P); tx.restore();
  tx.fillStyle = tone(.03); tx.fill(P); px.fillStyle = GR.hatch({ th: 0, id: 2 }); px.fill(P);
}
function sav_dag(x, y, s, rot, seed, t) {
  // kökünden sökülmüş dağ: tepesi yukarıda sivri, altı yırtık toprak; koyu kaya, üst kenarında ışık; alttan sarkan kökler
  const { tx } = GR, q = rng(seed), c = Math.cos(rot), sn = Math.sin(rot), W2 = ([u, v]) => [x + (u * c - v * sn) * s, y + (u * sn + v * c) * s];
  const pts = [[-1.3, .2], [-1.05, -.05], [-.82, -.22], [-.6, -.5], [-.45, -.42], [-.25, -.66], [-.05, -.82], [.12, -.62], [.3, -.7], [.5, -.45], [.75, -.3], [1, -.08], [1.3, .2]];
  for (let i = 0; i <= 8; i++) { const u = 1 - i / 8 * 2; pts.push([u * 1.25, .25 + .3 * (1 - u * u) + (q() - .5) * .12]); }
  const RP = PR.rock(pts.map(W2), { lit: [.3, -.95], hi: .5, mid: .08, lo: .03, seed, th: rot, rim: 6, facets: 5 });
  for (let k = 0; k < 7; k++) { const u = -.7 + k * .23 + (q() - .5) * .08, v0 = .25 + .3 * (1 - u * u), L = .25 + q() * .35, sw = Math.sin(t * 2 + k) * .08;
    gol_vurus(tx, [W2([u, v0 - .04]), W2([u + .04, v0 + L * .5]), W2([u - .06 - sw, v0 + L])], s * .045, .03, .9); }
}
function sav_p036(t) {
  const L = { x: 1350, y: 0 }, tT = Wd('D07', 'topu'), tD = Wd('D07', 'dağları');
  cen_gok(L, { r0: 380, r1: 1500, v: .66, n: 120 });
  cen_bulutKat({ x0: 1560, x1: 3400, y: 520, h: 380, yb: H + 100, seed: 72, L, t, n: 4 });     // sadıkların arkası: koyu bulut (beyaz saf onun önünde)
  for (const [x0, y0, sz, sd, dl] of [[1980, 930, 130, 81, 0], [2330, 950, 105, 82, .35], [2600, 920, 150, 83, .7]]) {
    const u = sav_u(t, tD - .4 + dl * .6, tD + 2.0 + dl * .6), up = E.out2(clamp(u * 2.5)), fl = E.in2(clamp((u - .3) / .7));
    sav_dag(x0 - 1300 * fl, y0 - 560 * up - 120 * fl + 300 * fl * fl, sz, -.35 * fl, sd, t);
  }
  cen_safKutle({ x0: -300, x1: 520, y: 880, h: 17, seed: 74, v: .03, nSp: 7, spV: 0 });        // asiler: açık göğün önünde koyu kütle
  cen_bulutKat({ x0: -500, x1: 3400, y: 990, h: 230, yb: H + 100, seed: 73, L, t, n: 12 });      // zemin: bulut terası
  [[720, 692, 190, -.13, 0], [1320, 680, 210, -.1, .3]].forEach(([x, y, sz, a, dl], i) => sav_top(x, y, sz, a, sav_u(t, tT - .3 + dl, tT + 2.6 + dl), t, 80 + i));
  cen_safKutle({ x0: 1780, x1: 3200, y: 880, h: 17, seed: 75, v: .985, nSp: 0 });
}
plan('P036', (ctx, st) => levha(ctx, camLerp({ cx: 860, cy: 540, z: 1 }, { cx: 1700, cy: 540, z: 1 }, sav_u(st.t, Wd('D07', 'icat') - .5, Wd('D07', 'dağları') + 1.0), E.io2), () => sav_p036(st.t)),
  { tr: { type: 'cut' }, mb: 3 });

// ═════════ P060 (F05): kapı kanatları ayrılır; arkada Kaos ═════════
// Kapının kendisi KAP grubunun; burada yalnız aralanan iki koyu kütle (kanatların iç yüzü) ve aradan görünen Kaos.
// Eşikte, sırtı bize dönük küçük koyu siluet: Kaos'un aydınlığına karşı okunur.
const KAO_P060 = [
  { ox: 900, oy: 760, R: 560, a0: -2.9, span: 1.3, wd: 150, nb: 6, seed: 61, bump: .22, yirtik: 1, bend: .6 },
  { ox: 1040, oy: 700, R: 720, a0: -.35, span: -1.2, wd: 190, nb: 7, seed: 62, bump: .2, yirtik: 1, bend: .6 },
  { ox: 960, oy: 640, R: 1050, a0: 2.65, span: -.9, wd: 230, nb: 6, seed: 63, bump: .2, yirtik: 1, bend: .6 },
];
function kao_p060(t) {
  const { tx, px, tone } = GR, tA = Wd('F05', 'açar'), o = E.io3(sav_u(t, tA - .3, tA + 2.6));
  kao_bosluk(t, { lt: t - S('F05'), cx: 960, cy: 600, r0: 90, r1: 1250, sy: .65, kollar: KAO_P060 });
  // eşik ve figür (sırtı bize dönük; kanatlar yarı açık)
  const TH = new Path2D(); poly(TH, [[-100, 930], [W + 100, 930], [W + 100, H + 50], [-100, H + 50]], true); GR.fill(TH, tone(.03), { th: 0, id: 4 });
  GR.tx.save(); GR.tx.clip(TH); gol_vurus(GR.tx, [[960 - 700 * o, 934], [960, 937], [960 + 700 * o, 934]], 10 * o + 1, .97, .4); GR.tx.restore();
  kiy_seytan(t, { x: 960, gy: 932, h: 44, facing: 1, twist: 0, head: .05, lean: 0, armN: [.15, .15], armF: [-.15, .15], lum: .06, lit: [0, -1], open: lerp(-.2, .25, o), lift: lerp(-.1, .3, o), wingK: .75, cloak: 1.5 });
  // kanatlar: düz siyah, iç kenarda ince ışık; dönerek açılır (iç kenar dışa kayar, boyca hafif uzar)
  for (const sd of [-1, 1]) {
    const xi = 960 + sd * (4 + 760 * o), xo = 960 + sd * 1300, gr = 30 * o, P = new Path2D();
    poly(P, [[xi, -60 - gr], [xo, -200], [xo, H + 200], [xi, H + 60 + gr]], true);
    GR.fill(P, tone(.025), { th: PI / 2, id: 0 });
    tx.save(); tx.clip(P); gol_vurus(tx, [[xi + sd * 4, -20], [xi + sd * 5, 540], [xi + sd * 4, H + 20]], 9 + 6 * o, .95, .1); tx.restore();
  }
}
plan('P060', (ctx, st) => levha(ctx, { cx: 960, cy: 540, z: 1 }, () => kao_p060(st.t)), { tr: { type: 'cut' },
  over: (ctx, st) => etiket(ctx, 'KAOS', 960, 150, st.t - Wd('F05', 'kaos') + .1, st.end - Wd('F05', 'kaos') + .5, { px: 64, ls: 14, panel: .7 }) });

// ═════════ P061 (F06): uçuş, düşüş, rüzgâr ═════════
const KAO_P061 = [
  { ox: 1150, oy: 560, R: 520, a0: -2.7, span: 1.45, wd: 230, nb: 6, seed: 71, bump: .22, yirtik: 1, bend: .6 },
  { ox: 1000, oy: 470, R: 700, a0: .25, span: 1.25, wd: 200, nb: 7, seed: 72, bump: .2, yirtik: 1, bend: .6 },
  { ox: 1160, oy: 420, R: 980, a0: -.65, span: -1.0, wd: 230, nb: 6, seed: 73, bump: .2, yirtik: 1, bend: .6 },
];
function kao_p061(t) {
  const tU = Wd('F06', 'uçar'), tD = Wd('F06', 'düşer'), tR = Wd('F06', 'rüzgar'), tF = Wd('F06', 'fırlatmasa');
  kao_bosluk(t, { lt: t - S('F06'), cx: 1050, cy: 420, r0: 90, r1: 1000, sy: .7, kollar: KAO_P061 });
  // yol: uçuş (sağa süzülür) → düşüş (aşağı, hızlanır, küçülür) → rüzgâr (yukarı fırlar) → yeniden süzülür
  const fly = E.io2(sav_u(t, tU - .5, tD)), fall = E.io2(sav_u(t, tD - .1, tR + .1)), gust = E.out3(sav_u(t, tR + .1, tF + .6));
  let x = lerp(640, 900, fly) + 140 * fall - 260 * gust, y = lerp(470, 430, fly) + 560 * fall - 640 * gust;
  const h = lerp(30, 17, fall) + 8 * gust, tumble = fall * (1 - gust) * (2.2 + Math.sin(t * 2) * .3);
  // rüzgâr: aşağıdan dönerek yükselen beyaz akış vuruşları (yalnız esinti süresince)
  const gw = Math.sin(PI * sav_u(t, tR - .2, tF + 1.2));
  if (gw > .02) { const q = rng(616); for (let i = 0; i < 4; i++) { const x0 = 760 + (q() - .5) * 420, ph = q() * TAU, L = 380 + q() * 260, pts = [];
      for (let k = 0; k <= 8; k++) { const u = k / 8; pts.push([x0 + Math.sin(u * 3.2 + ph + t * .8) * 90 - u * 160, 1120 - u * L * gw - (1 - gw) * 200]); }
      gol_vurus(GR.tx, pts, 11 * gw, .95, .5); } }
  const sp = fly * (1 - fall) + gust;
  kao_ucan(t, { x, y, h, lean: tumble + lerp(.1, -.2, gust) * (1 - fall), head: .1, open: lerp(.95, .5, fall) + .4 * gust, lift: lerp(.55, .9, fall * (1 - gust)), droop: lerp(.15, .7, fall * (1 - gust)),
    flap: Math.sin(t * 3) * .25 * sp, lum: .1, lit: [.3, -1], seed: 7, legN: [.05, -.2], legF: [-.1, -.3] });
}
plan('P061', (ctx, st) => levha(ctx, { cx: 960, cy: 540, z: 1 }, () => kao_p061(st.t)), { tr: { type: 'fade', dur: .8 } });

// ═════════ P062 (F07): uzakta, ışıktan ince altın zincirle sarkan küçük dünya; yanında ay ═════════
const KAO_P062 = [
  { ox: 980, oy: -60, R: 600, a0: 2.65, span: -1.0, wd: 260, nb: 6, seed: 81, bump: .2, yirtik: 1, bend: .6 },
  { ox: 900, oy: -100, R: 840, a0: .25, span: 1.0, wd: 230, nb: 7, seed: 82, bump: .2, yirtik: 1, bend: .6 },
  ];
function kao_p062(t) {
  const { tx, tone } = GR;
  kao_bosluk(t, { lt: t - S('F07'), cx: 1000, cy: 40, r0: 160, r1: 1250, sy: .75, kollar: KAO_P062 });
  // zincir: yukarıdaki ışıktan inen ince kâğıt çizgi, küçük halkalar
  const X = 1010, Y1 = 600, sw = Math.sin(t * .4) * 6;
  gol_vurus(tx, [[X, -10], [X + sw * .4, Y1 * .5], [X + sw, Y1 - 22]], 4, .97, .05);
  for (let k = 1; k < 28; k++) { const u = k / 28, y = u * (Y1 - 22), x = X + sw * u * u; tx.fillStyle = tone(.97); tx.beginPath(); tx.ellipse(x, y, 3.2, 5.5, 0, 0, TAU); tx.fill(); }
  // dünya: küçük küre; üstten aydınlık (kâğıt hilal), altı koyu
  const R = 20, cx = X + sw, cy = Y1;
  PR.glow(cx, cy, R, R * 5, 1, .35);
  const D = new Path2D(); D.arc(cx, cy, R, 0, TAU); GR.fill(D, tone(.03), { th: 0, id: 0 });
  tx.save(); tx.clip(D); tx.fillStyle = tone(1); tx.beginPath(); tx.arc(cx - 3, cy - 8, R * .95, 0, TAU); tx.fill(); tx.fillStyle = tone(.03); tx.beginPath(); tx.arc(cx + 6, cy + 6, R * .9, 0, TAU); tx.fill(); tx.restore();
  // ay: yanında biraz büyük, ince hilal
  const MX = 1210, MY = 500, MR = 38, M = new Path2D(); M.arc(MX, MY, MR, 0, TAU);
  tx.save(); tx.clip(M); tx.fillStyle = tone(1); tx.fill(M); tx.fillStyle = tone(.05); tx.beginPath(); tx.arc(MX + 16, MY - 6, MR * .92, 0, TAU); tx.fill(); tx.restore();
  // önde, sol altta: ona bakan küçük koyu figür (havada asılı, kanatlar açık)
  kao_ucan(t, { x: 600, y: 700 + Math.sin(t * 1.2) * 5, h: 36, lean: .25, head: .3, open: .9, lift: .5, flap: Math.sin(t * 1.6) * .15, lum: .08, lit: [.6, -.8], seed: 9, legN: [-.1, -.4], legF: [-.25, -.6] });
}
plan('P062', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 960, cy: 540, z: 1.08 }, st.p, E.io2), () => kao_p062(st.t)), { tr: { type: 'fade', dur: .8 } });

function cen_yazi_sav(ctx, s, x, y, lt, d) { const a = clamp(lt / .5) * clamp((d - lt) / .5); if (a <= 0 || NOTEXT) return; txt(ctx, s, x, y, { px: 48, ls: 10, a: E.sine(a), font: FONT.baslik(48, 600) }); }

// ═════════ P096 (I02): yedi gece: dünyanın gece yanında, karanlıkla birlikte dönen küçük figür ═════════
// Küre: sağdan aydınlık (temiz kâğıttan koyuya), solu gece (düz siyah). Kıtalar dönerek kayar; figür hep sol kenarda, gece yanında,
// arkasındaki Kaos aydınlığına karşı koyu siluet. Sayaç I–VII (kelimeye bağlı değil, "yedi"den "sekizinci"ye yayılır); "sızar"da geceye süzülür.
const KAO_KITA = (() => { const r = rng(96), K = []; for (let i = 0; i < 7; i++) K.push({ lon: r() * TAU, lat: (r() - .5) * 1.6, rx: .25 + r() * .35, ry: .18 + r() * .25, seed: 960 + i }); return K; })();
function kao_p096(t) {
  const { tx, px, tone } = GR, t7 = Wd('I02', 'yedi'), t8 = Wd('I02', 'sekizinci'), tZ = Wd('I02', 'sızar');
  kao_bosluk(t, { lt: t - S('I02'), cx: 640, cy: 540, r0: 120, r1: 950, sy: .9, kollar: [
    { ox: 700, oy: 560, R: 620, a0: -2.2, span: 1.3, wd: 150, nb: 6, seed: 97, bump: .2 }, { ox: 820, oy: 520, R: 760, a0: 1.0, span: 1.3, wd: 190, nb: 6, seed: 98, bump: .2 }] });
  const CX = 1060, CY = 560, R = 300, rot = (t - S('I02')) * .9;
  const D = new Path2D(); D.arc(CX, CY, R, 0, TAU);
  const g = tx.createLinearGradient(CX + R, CY, CX - R * .2, CY); g.addColorStop(0, tone(.98)); g.addColorStop(.45, tone(.8)); g.addColorStop(.8, tone(.25)); g.addColorStop(1, tone(.03));
  GR.fill(D, g, { th: .35, id: 9 });
  tx.save(); tx.clip(D);
  for (const k of KAO_KITA) { const a = k.lon - rot, ca = Math.cos(a); if (ca < .05) continue;
    const x = CX + Math.sin(a) * R * Math.cos(k.lat * .8) , y = CY + Math.sin(k.lat * .8) * R, P = new Path2D(); P.ellipse(x, y, R * k.rx * ca, R * k.ry, 0, 0, TAU);
    tx.fillStyle = tone(.12 + .2 * clamp((x - CX) / R + .3)); tx.fill(P); }
  // gece yanı: sol yarı düz siyah, sınır yumuşak değil (alacakaranlık kuşağı ince)
  const N = new Path2D(); N.rect(CX - R - 10, CY - R - 10, R * .95, 2 * R + 20); tx.fillStyle = tone(.03); tx.fill(N);
  tx.restore();
  // figür: sol kenarda, küreyi gece yanından saran yay üstünde salınır; "sızar"da geceye iner
  const sw = Math.sin((t - t7) * 1.6) * .18, z = E.io2(sav_u(t, tZ - .6, tZ + 1));
  const a = PI + sw, fx = CX + Math.cos(a) * (R + 70 - 60 * z), fy = CY + Math.sin(a) * (R + 70 - 60 * z) - 20;
  kao_ucan(t, { x: fx, y: fy, h: 22, lean: -.6 + sw * .5, head: .2, open: .85, lift: .5, flap: Math.sin(t * 2.2) * .2, lum: .06, lit: [.8, -.6], seed: 11, legN: [-.2, -.3], legF: [-.35, -.4] });
}
plan('P096', (ctx, st) => levha(ctx, { cx: 960, cy: 540, z: 1 }, () => kao_p096(st.t)), { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => {
    if (NOTEXT) return;
    const t7 = Wd('I02', 'yedi'), t8 = Wd('I02', 'sekizinci'), k = clamp((st.t - t7) / (t8 - t7)) * 7, i = Math.min(6, Math.floor(k));
    const a = clamp((st.t - t7 + .2) / .4) * clamp((st.end - st.t) / .5); if (a <= 0) return;
    txt(ctx, ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'][i], 1640, 200, { px: 110, ls: 6, a: a * (.55 + .45 * (i < 6 ? clamp((k % 1) / .15) : 1)) });
    txt(ctx, 'yedi gece', 1640, 295, { font: FONT.alinti(50), px: 50, a: a * .9 });
  } });

// ═════════ Savaş v2 (yönetmen düzeltme turu): cennetin yeni diliyle ters ışık ═════════
// Düello karesi ikiye bölünür: bir yanda açık gök + önünde koyu, ters ışıkta Şeytan (büyük KN kanat, ruin 0: henüz düşmedi);
// öbür yanda koyu bulut kütlesi (cen_bulutKat) + önünde ışıklı, çizgili sadık melek (cen_aydin). Zemin bulut terası.
// Kılıç: Şeytan'da mürekkep (açık gök önünde), melekte kâğıt (koyu bulut önünde).
function sav_aydinKilic(p, kl) {
  const v = kl.v ?? (p.back ? 0 : 1);
  const J = cen_aydin(Object.assign({ spear: false }, p, { mid: kl.k === 'F' ? (J) => sav_eldenKilic(J, 'F', kl.off || 0, kl.len || 4, v) : p.mid }));
  if (kl.k !== 'F') sav_eldenKilic(J, 'N', kl.off || 0, kl.len || 4, v);
  return J;
}
// düello zemini: L ışık (sol üst), koyu bulut sağda; ayak çizgisi GY
function sav_duello(t, o = {}) {
  const L = o.L || (o.ayna ? { x: 1540, y: 60 } : { x: 380, y: 60 });
  cen_gok(L, { r0: o.r0 ?? 300, r1: o.r1 ?? 1500, v: .7, n: 110 });
  if (o.ayna) cen_bulutKat({ x0: -580, x1: 1220, y: o.by ?? 380, h: o.bh ?? 480, yb: H + 100, seed: o.seed || 131, L, t, n: 3 });
  else cen_bulutKat({ x0: o.bx0 ?? 700, x1: 2500, y: o.by ?? 380, h: o.bh ?? 480, yb: H + 100, seed: o.seed || 131, L, t, n: 3 });
  cen_bulutKat({ x0: -400, x1: 2400, y: 1010, h: 230, yb: H + 100, seed: (o.seed || 131) + 1, L, t, n: 9 });
  return L;
}
const SAV_GY = 900;

// ═════════ P031 (D02): Abdiel ile Şeytan karşı karşıya ═════════
plan('P031', (ctx, st) => {
  const t = st.t, cam = camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 960, cy: 530, z: 1.07 }, st.p, E.sine);
  levha(ctx, cam, () => {
    const L = sav_duello(t, { seed: 131 }), br = Math.sin(t * .6) * 1.5, h = 56;
    sav_aydinKilic({ x: 560, y: SAV_GY - 3.95 * h + br * .3, h, facing: 1, L, t, back: true, head: .08, twist: .35, armN: [1.75, .5], armF: [.4, .5], legN: [.3, -.1], legF: [-.25, -.05], lift: .55, open: .85, wingS: 7.2, seed: 5 },
      { k: 'N', off: .25, len: 4 });
    sav_aydinKilic({ x: 1360, y: SAV_GY - 3.95 * h - br * .3, h, facing: -1, L, t, head: .15, twist: .35, armN: [.25, .4], armF: [1.8, .45], legN: [.28, -.08], legF: [-.22, -.04], lift: .6, open: .85, wingS: 7.2, seed: 7 },
      { k: 'F', off: .25, len: 4 });
  });
}, { tr: { type: 'fade', dur: .8 },
  // alıntı koyu bulut kütlesinin üstünde, kâğıt renginde, iki satır; 'sen'den 1 sn önce belirir (≥ 4,2 sn görünür)
  over: (ctx, st) => quote(ctx, '“Sen de özgür değilsin;\nkendi kendinin tutsağısın.”', 1330, 250, st.t - (Wd('D02', 'sen') - 1.0), { px: 72, maxW: 1100, per: .55, panel: false }) });

// ═════════ P032 (D03): Abdiel yakın planı: ışıklı çizgili baş-omuz-kanat; arkasında koyu bulut ═════════
plan('P032', (ctx, st) => {
  const t = st.t, L = { x: 200, y: 40 };
  levha(ctx, camLerp({ cx: 990, cy: 540, z: 1 }, { cx: 950, cy: 540, z: 1 }, st.p, E.sine), () => {
    cen_gok(L, { r0: 260, r1: 1200, v: .7, n: 110 });
    cen_bulutKat({ x0: -300, x1: 2400, y: 330, h: 520, yb: H + 200, seed: 141, L, t, n: 4 });
    cen_bulutKat({ x0: -400, x1: 1300, y: 640, h: 600, yb: H + 200, seed: 142, L, t, n: 3 });
    const br = Math.sin(t * .7) * 2, h = 128;
    cen_aydin({ x: 1440, y: 1010 + br, h, facing: -1, L, t, head: .1, twist: .25, lean: -.02, armN: [.3, .3], armF: [.1, .3], legs: false, lift: .8, open: .7, wingS: 4.2, cloak: .8, lines: 2, seed: 7, spear: false });
  });
}, { tr: { type: 'cut' },
  over: (ctx, st) => quote(ctx, '“…krallık değil, zincir bekle.”', 600, 700, st.t - Wd('D03', 'ama') + .9, { px: 72, maxW: 1000, panel: false, per: .3 }) });

// ═════════ P033 (D04): kılıç iner; Şeytan on adım geriler, onuncu adımda dizinin üstüne çöker ═════════
function sav_p033(t) {
  const tI = Wd('D04', 'iner'), tO = Wd('D04', 'onuncu'), tC = Wd('D04', 'çöker');
  const L = sav_duello(t, { seed: 151 }), h = 54, gy = SAV_GY;
  const sw = E.in3(sav_u(t, tI - .28, tI));
  const back = E.out2(sav_u(t, tI, tO + .4)), x = lerp(760, 420, back), ph = back * 10 * PI;
  const kn = E.io2(sav_u(t, tC - .35, tC + .35)), rec = Math.exp(-Math.pow((t - tI - .15) / .25, 2));
  const step = Math.sin(ph) * (1 - kn), lift = Math.max(0, Math.cos(ph)) * (1 - kn);
  sav_aydinKilic({ x, y: gy - 3.95 * h + kn * 1.25 * h, h, facing: 1, L, t, back: true, head: lerp(.05, -.3, kn) - .2 * rec, lean: -.12 * rec + lerp(-.04, .22, kn), twist: .35,
    armN: [lerp(1.1, .35, kn) - .5 * rec, .5], armF: [lerp(.3, -.3, kn), .4], legN: [lerp(.32 * step, 1.45, kn), lerp(-.15 - .5 * lift, -1.5, kn)], legF: [lerp(-.32 * step, -.15, kn), lerp(-.15 - .5 * (1 - lift), -1.7, kn)],
    lift: lerp(.55, .3, kn), open: .8, droop: .15 + .35 * kn, wingS: 7, seed: 5 }, { k: 'N', off: lerp(.3, 1.0, kn), len: 3.6 });
  const ax = lerp(1360, 1260, E.io2(sav_u(t, tI, tI + 1.2)));
  sav_aydinKilic({ x: ax, y: gy - 3.95 * h, h, facing: -1, L, t, head: lerp(.2, -.05, sw), lean: lerp(-.06, .14, sw), twist: .35, armN: [.2, .4], armF: [lerp(2.8, .9, sw), lerp(.3, .1, sw)], legN: [.32, -.1], legF: [-.24, -.05],
    lift: .6, open: .85, wingS: 7, seed: 7 }, { k: 'F', off: .1, len: 4 });
}
plan('P033', (ctx, st) => {
  const tI = Wd('D04', 'iner'), sh = st.t > tI ? Math.exp(-(st.t - tI) * 7) : 0;
  levha(ctx, { cx: 960 + Math.sin(st.t * 61) * 7 * sh, cy: 540 + Math.cos(st.t * 47) * 5 * sh, z: 1 }, () => sav_p033(st.t));
}, { tr: { type: 'cut' }, mb: 3 });
// darbe yakın planı (orta-yakın): Abdiel'in kılıcı sağ üstten kadraja iner; Şeytan (büyük, belden yukarı) geri savrulur
function sav_p033y(t) {
  const tI = Wd('D04', 'iner'), L = { x: 380, y: 60 }, h = 120;
  cen_gok(L, { r0: 300, r1: 1500, v: .7, n: 110 });
  cen_bulutKat({ x0: 900, x1: 2500, y: 360, h: 620, yb: H + 100, seed: 157, L, t, n: 3 });
  const sw = E.in3(sav_u(t, tI - .25, tI)), rec = E.out3(sav_u(t, tI, tI + .7));
  sav_aydinKilic({ x: 760 - 120 * rec, y: 1040 + 30 * rec, h, facing: 1, L, t, back: true, head: .1 - .5 * rec, lean: -.05 - .35 * rec, twist: .35, legs: false,
    armN: [lerp(1.4, 2.4, rec), lerp(.6, .2, rec)], armF: [.3 + .4 * rec, .6], lift: .55 + .25 * rec, open: .85, wingS: 6, seed: 5 }, { k: 'N', off: .25, len: 3.2 });
  // Abdiel'in kolu ve kılıcı: sağ kenardan; ışıklı, koyu bulutun önünde
  sav_aydinKilic({ x: 1680, y: 1080, h, facing: -1, L, t, twist: .35, legs: false, head: .1, lean: lerp(-.1, .2, sw), armN: [.2, .3], armF: [lerp(2.9, 1.25, sw), lerp(.3, .1, sw)], lift: .6, open: .8, wingS: 5.5, seed: 7 }, { k: 'F', off: .05, len: 3.6 });
  const fl = Math.exp(-Math.pow((t - tI) / .12, 2));   // çarpma parıltısı: kılıçların kesiştiği yerde kısa kâğıt yıldız
  if (fl > .05) cen_yildiz(980, 470, 120 * fl, 1);
}
shot(S('D04') + .02, (ctx, st) => { const tI = Wd('D04', 'iner'), sh   /* cümle başından: 0,6 sn'lik ara plan kalmasın (başkan) */ = st.t > tI ? Math.exp(-(st.t - tI) * 8) : 0;
  levha(ctx, { cx: 960 + Math.sin(st.t * 61) * 10 * sh, cy: 540 + Math.cos(st.t * 47) * 7 * sh, z: 1 }, () => sav_p033y(st.t)); }, { id: 'P033y', tr: { type: 'cut' }, mb: 3 });
shot(Wd('D04', 'iner') + .9, (ctx, st) => levha(ctx, { cx: 960, cy: 540, z: 1 }, () => sav_p033(st.t)), { id: 'P033g', tr: { type: 'cut' } });

// ═════════ P034 (D05): başmeleğin kılıcı Şeytan'ın sağ yanını yarar ═════════
// Ters ışıkta koyu Şeytan: yarık, kenar ışığında bir kopukluk ve kılıcın kâğıt izi; yarıktan açık göğe koyu duman sızar (kan yok). Figür öne bükülür.
function sav_p034(t) {
  // ters açı: Mikail solda (koyu bulut önünde, ışıklı), Şeytan sağda açık gök önünde; plan, önceki kesmenin sonundaki diz çöküşüyle açılır, Şeytan dizinden doğrulur
  const tY = Wd('D05', 'yarar'), tA = Wd('D05', 'acıyı'), t0 = S('D05');
  const L = sav_duello(t, { seed: 161, ayna: true }), h = 56, gy = SAV_GY;
  const kn = 1 - E.io2(sav_u(t, t0 + .2, t0 + 1.3));                       // diz çökmüşken açılır, kalkar
  const sw = E.in3(sav_u(t, tY - .35, tY)), bend = E.out3(sav_u(t, tY, tY + .9)), pain = E.io2(sav_u(t, tA - .2, tA + 1.2)), wd = E.io2(sav_u(t, tY + .5, tY + 1.6));
  const J = sav_aydinKilic({ x: 1260, y: gy - 3.95 * h + 22 * bend + kn * 1.25 * h, h, facing: -1, L, t, back: true, head: lerp(.12, -.45, bend) - .12 * pain - .3 * kn, lean: lerp(-.05, .5, bend) + .22 * kn, twist: .35,
    armN: [lerp(lerp(1.6, .7, bend), .35, kn), lerp(.4, 1.2, bend)], armF: [lerp(.3, .9, bend), 1.2 * bend], legN: [lerp(.32 + .1 * bend, 1.45, kn), lerp(-.15 - .3 * bend, -1.5, kn)], legF: [lerp(-.28, -.15, kn), lerp(-.05 - .2 * bend, -1.7, kn)],
    lift: lerp(lerp(.6, .35, bend), .3, kn), open: .85, droop: .15 + .3 * bend + .3 * kn, wingS: 7, seed: 5 }, { k: 'N', off: lerp(.3, 1.0, kn), len: 3.6 });
  const P = (al, sd) => [J.shC[0] - J.up[0] * al * h + J.rt[0] * sd * J.f * h, J.shC[1] - J.up[1] * al * h + J.rt[1] * sd * J.f * h];
  const cut = sav_u(t, tY - .05, tY + .25), fade = 1 - sav_u(t, tY + .2, tY + 1.2);
  if (cut > 0 && fade > 0) gol_vurus(GR.tx, [P(.3, .9), P(1.0, .3), P(1.8, -.4)].map((p, i, A) => i === 0 ? p : [lerp(A[0][0], p[0], cut), lerp(A[0][1], p[1], cut)]), 9 * fade, 1, .5);
  const ooze = sav_u(t, tY + .1, tA + 2);
  if (ooze > 0) for (let i = 0; i < 4; i++) {
    const o0 = P(.9 + i * .22, -.45), L2 = h * (1.2 + .6 * (i % 2)) * ooze, sx = -J.f * h * (.6 + .3 * i);
    gol_vurus(GR.tx, [o0, [o0[0] + sx * .4, o0[1] + L2 * .3 + Math.sin(t * 1.3 + i) * 6], [o0[0] + sx, o0[1] + L2 * .6]], h * .14, .02, .8);
  }
  sav_aydinKilic({ x: 600 - 40 * wd, y: gy - 3.95 * h, h, facing: 1, L, t, head: lerp(.2, -.05, sw), lean: lerp(-.05, .16, sw) * (1 - wd), twist: .35, armN: [.15, .4], armF: [lerp(lerp(2.9, 1.15, sw), .5, wd), lerp(.2, .15, sw)],
    legN: [.36, -.1], legF: [-.28, -.05], lift: .7, open: .9, wingS: 7.4, seed: 8 }, { k: 'F', off: .1, len: 4.6 });
}
plan('P034', (ctx, st) => levha(ctx, camLerp({ cx: 990, cy: 540, z: 1 }, { cx: 940, cy: 540, z: 1 }, st.p, E.sine), () => sav_p034(st.t)), { tr: { type: 'cut' }, mb: 3 });

// ═════════ P035 (D06): Şeytan orta planı; göğüs zırhında tek parlak kenar ışığı; "lekelidir"de kararıp kopar ═════════
// Belden yukarı koyu siluet, ters ışık (açık gök arkada). Işık önden-yukarıdan zırhın göğüs kenarına tek parlak şerit bırakır.
// "lekelidir"de şerit kısalır, incelir, ikiye kopar (alfa yok); kanat ucundaki birkaç tüy koyulaşıp sarkar.
function sav_p035(t) {
  const tP = Wd('D06', 'parlayan'), tL = Wd('D06', 'lekelidir'), L = { x: 1500, y: 60 };
  cen_gok(L, { r0: 320, r1: 1400, v: .7, n: 110 });
  cen_bulutKat({ x0: -400, x1: 520, y: 260, h: 520, yb: H + 100, seed: 171, L, t, n: 3 });
  cen_bulutKat({ x0: 1300, x1: 2400, y: 780, h: 420, yb: H + 100, seed: 172, L, t, n: 3 });
  cen_bulutKat({ x0: -400, x1: 2400, y: 1040, h: 220, yb: H + 100, seed: 173, L, t, n: 8 });
  const k = E.io2(sav_u(t, tL - .4, tL + .9)), br = Math.sin(t * .6) * 2, h = 120;
  const J = cen_aydin({ x: 860, y: 1060 + br, h, facing: 1, L, t, back: true, head: lerp(.05, -.12, k), twist: .3, armN: [.25, .5], armF: [.1, .4], legs: false, lift: .5, open: .8, droop: .15 + .45 * k, wingS: 5.4, cloak: .9, seed: 5 });
  // göğüs zırhının kenar ışığı: göğüs önünden bele inen tek şerit
  const P = (al, sd) => [J.shC[0] - J.up[0] * al * h + J.rt[0] * sd * J.f * h, J.shC[1] - J.up[1] * al * h + J.rt[1] * sd * J.f * h];
  const a = E.io2(sav_u(t, tP - .3, tP + .5));
  const seg = (u0, u1, w) => { const pts = []; for (let i = 0; i <= 6; i++) { const u = lerp(u0, u1, i / 6), al = lerp(.15, 1.75, u); pts.push(P(al, .5 - .12 * Math.pow(u - .4, 2) * 3)); } gol_vurus(GR.tx, pts, w, .99, .4); };
  if (a > 0) {
    if (k < .02) seg(0, a, 12);
    else { seg(0, lerp(.55, .22, k), lerp(12, 5, k)); seg(lerp(.65, .5, k), lerp(1, .62, k), lerp(12, 3, k)); }   // kopan, kısalan, incelen şerit
  }
}
plan('P035', (ctx, st) => levha(ctx, camLerp({ cx: 990, cy: 540, z: 1 }, { cx: 950, cy: 540, z: 1 }, st.p, E.sine), () => sav_p035(st.t)), { tr: { type: 'fade', dur: .6 } });

// ═════════ P037 (D08): Oğul yalnız ışık: bulutların arasından açılan geniş kâğıt kama; koyu asi safları cennetin kenarına sıkışır, boşluğa atlar ═════════
// Figür, yüz, el, hale, haç, araba gövdesi yok. Kama soldan, iki koyu bulut kütlesinin arasından açılır; kenarları bulut kıvrımlarıyla kesilir;
// çevresinde seyrek ışınsal tarama. Sağda koyu saflar (kütle + mızrak) geri çekilip uçurum kenarına sıkışır.
const SAV_P037 = (() => { const r = rng(370), F = [], R = [];
  for (let i = 0; i < 8; i++) F.push({ dx: r() * 240, dl: i * .14 + r() * .1, h: 26 + r() * 10, f: r() < .5 ? 1 : -1, sp: (r() - .5) * 2, seed: 900 + i });
  for (let i = 0; i < 9; i++) R.push({ x: 960 + i * 58 + r() * 24, h: 34 + r() * 8, sp: .3 + r() * .25, seed: 950 + i, ph: r() });   // ön saf: tek tek okunan figürler
  return { F, R }; })();
function sav_p037(t) {
  // Oğul yalnız ışık: koyu bulut örtüsünü sol üstten çapraz yaran geniş huzme demeti (figür, yüz, el, hale, haç, araba gövdesi yok).
  // Huzme sağ alttaki asi saflarına vurur: ön saflar (tek tek koyu figürler, mızraklı) geri savrulur, kıyıdan boşluğa dökülür.
  const { tx, px, tone } = GR, tO = Wd('D08', 'savaş'), tG = Wd('D08', 'gelir'), tS = Wd('D08', 'sürülür'), tA = Wd('D08', 'atarlar');
  const op = E.io2(sav_u(t, tO - .5, tG + .8)), push = E.io2(sav_u(t, tG, tS + .9)), EDGE = 1520, GY = 840;
  const O = { x: 160, y: -120 }, T = { x: 1300, y: GY - 60 }, th = Math.atan2(T.y - O.y, T.x - O.x), d = [Math.cos(th), Math.sin(th)], n = [-d[1], d[0]];
  // koyu bulut örtüsü (savaşın karanlığı)
  tx.fillStyle = tone(.025); tx.fillRect(-400, -400, W + 800, H + 800); px.fillStyle = GR.hatch({ th: 0, id: 0 }); px.fillRect(-400, -400, W + 800, H + 800);
  // boşluk: kıyının ötesi, huzmenin ışığıyla aşağı doğru açılan
  const V = new Path2D(); V.rect(EDGE - 10, GY, 800, 600); const gv = tx.createLinearGradient(0, GY, 0, H); gv.addColorStop(0, tone(.75 * op + .05)); gv.addColorStop(1, tone(.05)); GR.fill(V, gv, { th: 0, id: 1 });
  // huzme demeti: kökte dar, vurduğu yerde geniş; 5 şerit, aralarında ince koyu boşluk; ışığın çevresinde seyrek ışınsal tarama
  if (op > 0) {
    const Lb = 1500, wid = 520 * op;
    const halo = new Path2D(); poly(halo, [[O.x - 60, O.y], [O.x + 60, O.y], [O.x + d[0] * Lb + n[0] * wid, O.y + d[1] * Lb + n[1] * wid], [O.x + d[0] * Lb - n[0] * wid, O.y + d[1] * Lb - n[1] * wid]], true);
    const gh = tx.createLinearGradient(O.x, O.y, O.x + d[0] * Lb, O.y + d[1] * Lb); gh.addColorStop(0, tone(.7)); gh.addColorStop(1, tone(.45));
    GR.fill(halo, gh, { type: 'ray', cx: O.x, cy: O.y, n: 160, id: 10, w: 3 });
    const q = rng(37);
    for (let i = 0; i < 5; i++) { const f0 = -1 + i * .42 + q() * .08, f1 = f0 + .3 + q() * .06, B = new Path2D();
      poly(B, [[O.x + n[0] * f0 * 30, O.y + n[1] * f0 * 30], [O.x + n[0] * f1 * 30, O.y + n[1] * f1 * 30], [O.x + d[0] * Lb + n[0] * f1 * wid * .82, O.y + d[1] * Lb + n[1] * f1 * wid * .82], [O.x + d[0] * Lb + n[0] * f0 * wid * .82, O.y + d[1] * Lb + n[1] * f0 * wid * .82]], true);
      tx.fillStyle = tone(1); tx.fill(B); }
  }
  // huzmenin kenarlarını kesen bulut kıvrımları (ışık bulutların arasından açılır)
  for (let i = 0; i < 5; i++) { const u = .1 + i * .2, c = [O.x + d[0] * 1500 * u, O.y + d[1] * 1500 * u], w = (40 + 520 * op * u) * .95;
    cen_bulutKat({ x0: c[0] + n[0] * w - 200, x1: c[0] + n[0] * w + 200, y: c[1] + n[1] * w + 40, h: 170, seed: 371 + i, L: O, t, n: 2 });
    cen_bulutKat({ x0: c[0] - n[0] * w - 200, x1: c[0] - n[0] * w + 200, y: c[1] - n[1] * w - 40, h: 170, seed: 381 + i, L: O, t, n: 2 }); }
  // cennetin kıyısı: bulut terası, sağda uçurum
  cen_bulutKat({ x0: 820, x1: EDGE + 100, y: GY + 110, h: 230, yb: H + 100, seed: 391, L: O, t, n: 4 });
  // arka saflar (kütle + mızrak) ve ön saf (tek tek, büyük): ışığın vurduğu yerde koyu, geri savrulur
  const mx = 360 * push;
  tx.save(); px.save(); const CL = new Path2D(); CL.rect(-400, -400, EDGE + 440, 2000); tx.clip(CL); px.clip(CL);
  cen_safKutle({ x0: 1180 + mx * .8, x1: 1700 + mx * .8, y: GY - 6, h: 20, seed: 83, v: .03, nSp: 8, spV: 0, spAng: () => .35 + .3 * push });
  tx.restore(); px.restore();
  for (const R of SAV_P037.R) {
    const x = R.x + mx * (1 + R.sp * .6), fall = Math.max(0, x - EDGE) / 140;
    if (fall > 4) continue;
    const y = GY + 40 + 120 * fall * fall, J = SF.rig({ x, y: y - 3.95 * R.h, h: R.h, facing: -1, twist: .4, lean: -.25 * push - .3 * fall - .15 * Math.sin(t * 3 + R.ph * 6) * push, head: .2 * push, armN: [.4 + 1.2 * push, .3], armF: [1.2 + .6 * push, .4], legN: [.2 + .4 * push * Math.sin(t * 6 + R.ph * 9), -.2], legF: [-.3, -.2] });
    cen_mizrak(J.wrN[0], J.wrN[1], -.5 - .6 * push - fall * .4, R.h * 7, .7, Math.max(2, R.h * .06), R.h, 0);
    SF.draw(J, { lum: .05, lit: [-.9, -.4], t, legs: true, skirt: true, eye: 0, wind: .8, cloak: .7, halo: 3, lines: 1, seed: R.seed });
  }
  // "atarlar": kıyıdan dökülenler okunur boyda
  for (const F of SAV_P037.F) { const u = t - (tA - .5 + F.dl); if (u < 0) continue; const x = EDGE + 30 + F.dx * .5 + u * 90, y = GY - 20 + 300 * u * u;
    if (y > H + 120) continue; cen_melek({ x, y, h: F.h, f: F.f, v: .03, spear: null, seed: F.seed, wing: .7, lx: -.9, ly: -.4 }); }
}
plan('P037', (ctx, st) => levha(ctx, { cx: 960, cy: 540, z: 1 }, () => sav_p037(st.t)), { tr: { type: 'cut' } });

// ═════════ P063 (F08): güneş; Uriel ve genç melek kılığındaki Şeytan ═════════
// Güneş: temiz kâğıt disk; ışınsal tarama diskin kenarından başlar (çember yok). Uriel diskin önünde büyük, koyu, ters ışıkta; kanatlar açık, kolu yolu gösterir.
// Sağda küçük, ışıklı çizgili "genç melek" (sahte parlaklık); arkasında kendi koyu bulutu, önünde koyu, kanatlı gölgesi.
function kao_p063(t) {
  const { tx, tone } = GR, tG = Wd('F08', 'gösterir'), S0 = { x: 760, y: 420 }, R = 270;
  cen_gok(S0, { r0: R * .85, r1: 1300, v: .66, n: 96 });
  { const g = tx.createRadialGradient(S0.x, S0.y, R, S0.x, S0.y, R + 230); g.addColorStop(0, tone(.5)); g.addColorStop(1, tone(1));
    tx.save(); tx.globalCompositeOperation = 'darken'; tx.fillStyle = g; tx.fillRect(S0.x - R - 240, S0.y - R - 240, (R + 240) * 2, (R + 240) * 2); tx.restore();
    const D = new Path2D(); D.arc(S0.x, S0.y, R, 0, TAU); tx.fillStyle = tone(1); tx.fill(D); }
  cen_bulutKat({ x0: 1300, x1: 2300, y: 560, h: 420, yb: H + 100, seed: 191, L: S0, t, n: 3 });
  cen_bulutKat({ x0: -400, x1: 2400, y: 1010, h: 230, yb: H + 100, seed: 192, L: S0, t, n: 9 });
  const pt = E.io2(sav_u(t, tG - .7, tG + .5)), h = 66;
  cen_aydin({ x: 820, y: 900 - 3.95 * h, h, facing: 1, L: S0, t, back: true, head: .1 + .08 * pt, twist: .35, armN: [lerp(.2, 1.5, pt), lerp(.3, .05, pt)], armF: [-.1, .3], legN: [.12, -.05], legF: [-.1, -.03],
    lift: .7, open: .95, wingS: 7.4, spear: { grip: 'F', ang: -.04, len: 8, up: .62 }, seed: 9 });
  // kılık: küçük, ışıklı çizgili figür; arkasında koyu bulut, önünde koyu kanatlı gölgesi (ışık soldan → gölge sağa yatar)
  const x = 1520, gy = 900;
  { const ax = [Math.cos(.12), Math.sin(.12)], nx = [-ax[1], ax[0]], Pt = (u, v) => [x + ax[0] * u + nx[0] * v, gy + 8 + ax[1] * u + nx[1] * v], P = new Path2D(), len = 330, wd = 12;
    poly(P, [Pt(0, -wd * .5), Pt(len * .3, -wd), Pt(len * .85, -wd * .7), Pt(len, 0), Pt(len * .85, wd * .7), Pt(len * .3, wd), Pt(0, wd * .5)], true);
    for (const sd of [-1, 1]) poly(P, [Pt(len * .35, 0), Pt(len * .42, sd * wd * 3), Pt(len * .52, sd * wd * 2.3), Pt(len * .6, sd * wd * 4.2), Pt(len * .68, sd * wd * 2.6), Pt(len * .8, sd * wd * 4.6), Pt(len * .82, sd * wd * 1.2), Pt(len * .7, 0)], true);
    tx.fillStyle = tone(.02); tx.fill(P); }
  cen_aydin({ x, y: gy - 3.95 * 34, h: 34, facing: -1, L: S0, t, head: .05, twist: .3, armN: [.05, .3], armF: [-.05, .2], legN: [.08, -.05], legF: [-.06, -.02], lift: .5, open: .7, wingS: 4.4, spear: false, cloak: .4, seed: 11 });
}
plan('P063', (ctx, st) => levha(ctx, { cx: 960, cy: 540, z: 1 }, () => kao_p063(st.t)), { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => etiket(ctx, 'URIEL', 1180, 170, st.t - Wd('F08', 'uriyele') + .2, st.end - Wd('F08', 'uriyele') + .4, { px: 48, ls: 10, panel: false, col: INK_CSS }) });
