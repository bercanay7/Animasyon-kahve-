// nif grubu (NIF: Nifates Dağı): set, figür, "iç cehennem" motifi ve planlar (bkz. lib/acts/KILAVUZ.md)
// Değer planı (geçiş sahnesi, koyu piksel %50–60): dev güneş diski temiz kâğıt (taramasız çekirdek); gök açık ama güneşe göre
// eş merkezli taralı, kenarlara doğru koyulaşır; birkaç ışın kaması içinde çizgi ışın doğrultusunda (cehennemin yatay taramasından ayrışır).
// Dağ ve figür koyu kütle: biçimi ışık yanındaki kenar ışığı ve kütleye giren beyaz vuruşlar verir. Uzakta Aden: küçük, açık.
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const nif_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));

// ═════════ set ═════════
// gök ve güneş. S: {x, y, r}; o: {dark (0..1 alacakaranlık), soft (0..1 ışık yumuşar: kamalar söner), beams (kama listesi: [açı, yarı genişlik, boy]),
//   clouds (false | bulut listesi: {x, y, w, h, seed, n}): güneşe bakan kenarı ışıklı koyu bulut kütleleri (yazıların zemini de bunlardır)}
function nif_gok(S, o = {}) {
  const { tx, px, tone } = GR, dk = o.dark || 0, sf = o.soft || 0, r = S.r;
  const k = v => clamp(lerp(v, v * .6, dk));
  const g = tx.createRadialGradient(S.x, S.y, r * .98, S.x, S.y, r * 5);
  g.addColorStop(0, tone(k(lerp(.86, .9, sf)))); g.addColorStop(.12, tone(k(lerp(.92, .94, sf)))); g.addColorStop(.3, tone(k(lerp(.89, .92, sf))));
  g.addColorStop(.6, tone(k(lerp(.83, .87, sf)))); g.addColorStop(1, tone(k(lerp(.72, .78, sf))));
  tx.fillStyle = g; tx.fillRect(-2000, -2000, W + 4000, H + 4000);
  px.fillStyle = GR.hatch({ type: 'rad', cx: S.x, cy: S.y, id: 1 }); px.fillRect(-2000, -2000, W + 4000, H + 4000);
  // ışın kamaları: güneşten çıkan, sivrilen açık kamalar (temiz kâğıda yakın); içlerinde çizgi ışın doğrultusunda
  const B = o.beams ?? [[-2.5, .045, 1500], [-1.95, .03, 1200], [-1.15, .035, 1300], [-.5, .045, 1500], [-3.05, .03, 1100]];
  const bv = (1 - sf) * (1 - dk * .7);
  if (bv > .02) {
    tx.save(); tx.globalCompositeOperation = 'lighten';
    for (const [a, w, L] of B) {
      const n = 10, A = [], C = [];
      for (let i = 0; i <= n; i++) { const u = i / n, rr = r * .96 + L * u, ww = w * Math.pow(Math.sin(PI * (.08 + .84 * u)), .7) * (1 - .4 * u); A.push([S.x + Math.cos(a - ww) * rr, S.y + Math.sin(a - ww) * rr]); C.push([S.x + Math.cos(a + ww) * rr, S.y + Math.sin(a + ww) * rr]); }
      const P = new Path2D(); poly(P, [...A, ...C.reverse()], true);
      const gg = tx.createRadialGradient(S.x, S.y, r, S.x, S.y, r + L);
      gg.addColorStop(0, tone(k(lerp(.85, 1, bv)))); gg.addColorStop(.6, tone(k(lerp(.75, .9, bv)))); gg.addColorStop(1, tone(k(.6)));
      tx.fillStyle = gg; tx.fill(P);
      px.fillStyle = GR.hatch({ th: a, id: 7 }); px.fill(P);
    }
    tx.restore();
  }
  // disk: temiz kâğıt, keskin kenar
  const D = new Path2D(); D.arc(S.x, S.y, r, 0, TAU);
  GR.fill(D, tone(1), { type: 'rad', cx: S.x, cy: S.y, id: 1 });
  // bulut kütleleri: koyu, güneşe bakan yumrularında ince açık hilal
  for (const c of (o.clouds || [])) {
    const L = [S.x - c.x, S.y - c.y], l = Math.hypot(L[0], L[1]) || 1;
    PR.cloud({ x: c.x, y: c.y, w: c.w, h: c.h, seed: c.seed, lit: [L[0] / l, L[1] / l], base: .03, hi: c.hi ?? .85, core: .02, n: c.n || 4, drift: (o.t ? Math.sin(o.t * .07 + c.seed) * 8 : 0) });
  }
  return D;
}
// uzak sıradağlar (iki kat, güneşe karşı yarı koyu) ve vadi. o: {hz (ufuk), dark}
function nif_siralar(o = {}) {
  const { tone, tx } = GR, hz = o.hz ?? 760, dk = o.dark || 0;
  for (const [dy, amp, v, seed] of [[0, 60, .8, 3], [60, 110, .03, 5]]) {
    if (v < .2 && o.aden) nif_aden(o.aden, o.t || 0);
    const r = rng(seed), P = []; P.push([-400, H + 400]);
    for (let x = -400; x <= W + 400; x += 40) P.push([x, hz + dy - amp * (.5 + .5 * Math.sin(x * .0042 + seed)) * (.6 + .4 * noise1(x * .01, seed)) + (r() - .5) * 8]);
    P.push([W + 400, H + 400]);
    const Q = new Path2D(); poly(Q, P, true);
    GR.fill(Q, tone(lerp(v, v * .7, dk)), { th: 0, id: 1 });
    if (v < .2) { tx.save(); tx.clip(Q); tx.strokeStyle = tone(.9); tx.lineWidth = 5; tx.beginPath(); poly(tx, P.slice(1, -1), false); tx.stroke(); tx.restore(); }
  }
}
// Aden: uzakta, aşağıda; uzak sıranın önünde açık bir vadi tabanı ve küçük ağaç tepeleri (kâğıt beyazı yumru, altında mürekkep hilal),
// çevresinde ince bir duvar çizgisi. Kontur yok: açık kütle arkasındaki taramayla ayrılır. E: {x, y (vadi tabanı), w, s}
function nif_aden(E, t) {
  const { tx, tone } = GR, s = E.s ?? 1, w = E.w ?? 420;
  const V = new Path2D(); V.moveTo(E.x - w * .75, E.y + 30 * s);
  for (let i = 0; i <= 12; i++) { const u = i / 12; V.lineTo(E.x - w * .75 + 1.5 * w * u, E.y - 26 * s * Math.sin(PI * u) - 6 * s * Math.sin(u * 17)); }
  V.lineTo(E.x + w * .75, E.y + 60 * s); V.lineTo(E.x - w * .75, E.y + 60 * s); V.closePath();
  GR.fill(V, tone(.9), { th: 0, id: 1 });
  const r = rng(77), N = 26, T = [];
  for (let i = 0; i < N; i++) { const u = r(); T.push([E.x - w * .6 + 1.2 * w * u, E.y - 22 * s * Math.sin(PI * u) - r() * 10 * s, (5 + r() * 8) * s]); }
  T.sort((a, b) => a[1] - b[1]);
  for (const [x, y, rr] of T) {
    tx.fillStyle = tone(.1); tx.beginPath(); tx.ellipse(x + rr * .2, y + rr * .3, rr * 1.02, rr * .78, 0, 0, TAU); tx.fill();
    const C = new Path2D(); C.ellipse(x - rr * .08, y - rr * .06, rr * .92, rr * .74, 0, 0, TAU); GR.fill(C, tone(1), { th: 0, id: 1 });
  }
}
// tepe: koyu kütle, ışık (güneş) yanında kenar ışığı ve içe giren beyaz vuruşlar. P: {x, y (zirve), s, lit: [lx, ly], seed}
const NIF_TEPE = [[-1300, 520], [-1060, 400], [-880, 330], [-720, 250], [-600, 196], [-470, 150], [-350, 96], [-250, 66], [-160, 36], [-96, 14], [-44, 2], [0, 0], [40, 4], [96, 18], [150, 42], [230, 64], [330, 110], [440, 140], [560, 200], [700, 240], [860, 310], [1040, 360], [1300, 520], [1300, 1400], [-1300, 1400]];
function nif_tepe(P) {
  const s = P.s ?? 1, r = rng((P.seed || 3) * 13 + 1), pts = [];
  // kırık sırt: her kenara düzensiz basamaklar (küçük ölçekte düz eğim cetvel gibi okunmasın); zirvenin yakını sakin
  NIF_TEPE.forEach(([x, y], i) => {
    pts.push([P.x + x * s, P.y + y * s]);
    const nx = NIF_TEPE[i + 1]; if (!nx || i >= NIF_TEPE.length - 3) return;
    const q = Math.min(1, Math.abs(x) / 300);
    for (const u of [.33, .66]) { const ax = lerp(x, nx[0], u), ay = lerp(y, nx[1], u); pts.push([P.x + ax * s + (r() - .5) * 30 * q, P.y + ay * s + (r() - .3) * 46 * q * Math.max(s, .6)]); }
  });
  const lit = P.lit || [.3, -.95];
  const RP = PR.rock(pts, { lit, hi: .06, mid: .035, lo: .02, seed: P.seed || 3, th: -.6, rim: Math.max(3, 6 * s), facets: 14 });
  // ışık yanındaki sırtlardan içeri giren beyaz vuruşlar (sırtın güneşe bakan yanı)
  const side = lit[0] >= 0 ? 1 : -1, ridge = side > 0 ? pts.slice(33, 67) : pts.slice(0, 34).reverse();
  PR.cuts(ridge, [-.35 * side, .94], { len: [14 * s, 130 * s], gap: [36 * s, 110 * s], w: Math.max(4, 6 * s), seed: (P.seed || 3) + 4, clip: RP, bend: .3 * side });
  return { path: RP, top: [P.x, P.y] };
}
// bütün set: o: {sun: {x,y,r}, hz, tepe: {x,y,s}, aden: {x,y,w,s} | false, dark, soft, beams, clouds, mid0 (gökten sonra), mid1 (sıradağlardan sonra), fig (tepe) => {}, front: () => {}}
function cizNifates(t, o = {}) {
  const S = o.sun || { x: 1060, y: 430, r: 300 };
  nif_gok(S, o);
  if (o.mid0) o.mid0(S);
  nif_siralar({ hz: o.hz ?? 800, dark: o.dark, aden: o.aden, t });
  if (o.mid1) o.mid1(S);
  const tp = o.tepe || { x: 900, y: 940, s: 1 };
  const L = [S.x - tp.x, S.y - tp.y], l = Math.hypot(L[0], L[1]) || 1;
  const T = nif_tepe(Object.assign({ lit: [L[0] / l, L[1] / l] }, tp));
  if (o.fig) o.fig(T.top, S);
  if (o.front) o.front(S);
  return { S, top: T.top, rock: T.path };
}

// ═════════ figür ═════════
// Şeytan Nifates'te: koyu siluet, pelerin, kanatlar (mızrak yok). p: SF.rig parametreleri + {wings: {open, lift, droop, spanL, spanR, rotL, rotR} | false,
// lum, lit, t, legs, cloak, ic (iç cehennem seçenekleri; bkz. nif_icCehennem), mid (J) => {} (figürle kanat arasında)}
// iki eklemli kol çözümü: omuz sh'den hedef tg'ye; s: dirseğin yönü (±1). SF.rig'in kol açısı biçiminde [üst kol, büküm] döndürür.
function nif_ik(sh, tg, h, f, lean, s = 1) {
  const L1 = 1.35 * h, L2 = 1.05 * h, dx = (tg[0] - sh[0]) * f, dy = tg[1] - sh[1];
  const D = clamp(Math.hypot(dx, dy), Math.abs(L1 - L2) + 1, L1 + L2 - 1), b = Math.atan2(dx, dy);
  const a1 = b + s * Math.acos(clamp((L1 * L1 + D * D - L2 * L2) / (2 * L1 * D), -1, 1));
  const el = [Math.sin(a1) * L1, Math.cos(a1) * L1], a2 = Math.atan2(dx - el[0], dy - el[1]);
  let bd = a2 - a1; while (bd > PI) bd -= TAU; while (bd < -PI) bd += TAU;
  return [a1 - lean * f, bd];
}
// p.ikN / p.ikF: [x, y, s] bilek hedefi (dünya); p.ground: ayakların bastığı y (kalça buna göre iner ya da kalkar)
function nif_rig(p) {
  if (p.ikN || p.ikF || p.ground != null) {
    let q = Object.assign({}, p, { ikN: null, ikF: null, ground: null }), J = nif_rig(q);
    if (p.ground != null) { const fy = Math.max(J.anN[1], J.anF[1]) + .2 * p.h; q.y = p.y + (p.ground - fy); J = nif_rig(q); }
    const f = p.facing ?? 1, ln = (p.lean ?? 0);
    if (p.ikN) q.armN = nif_ik(J.shN, p.ikN, p.h, f, ln, p.ikN[2] ?? 1);
    if (p.ikF) q.armF = nif_ik(J.shF, p.ikF, p.h, f, ln, p.ikF[2] ?? 1);
    return nif_rig(q);
  }
  return SF.rig({ x: p.x, y: p.y, h: p.h, facing: p.facing ?? 1, twist: p.twist ?? .4, lean: p.lean ?? 0, head: p.head ?? 0, shTilt: p.shTilt ?? -.04,
    armN: p.armN || [.12, .2], armF: p.armF || [-.1, .15], legN: p.legN || [.1, -.05], legF: p.legF || [-.08, -.03] });
}
function nif_kanat(J, p, mask) {
  const h = J.h, w = p.wings || {}, LIT = p.lit || [.3, -.95], t = p.t || 0;
  for (const [side, P] of [[-1, { span: (w.spanL ?? 8.6) * h, open: w.open ?? .55, lift: w.lift ?? .45, droop: w.droop ?? .5, rot: w.rotL ?? -.06, seed: 31, root: .1 }],
    [1, { span: (w.spanR ?? 7.8) * h, open: (w.open ?? .55) * .94, lift: (w.lift ?? .45) * .8, droop: (w.droop ?? .5) * 1.2, rot: w.rotR ?? .1, seed: 32, root: .12 }]]) {
    if (w.prof && side > 0) continue;   // profilde uzak kanat yakın kanadın arkasında kalır
    let sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN), sd = side;
    if (w.prof) { sd = -J.f; sh = [J.shC[0] - J.f * .2 * h + side * .08 * h, J.shC[1] + (side < 0 ? 0 : .1 * h)]; P.rot = ((side < 0 ? -.25 : .08) + -.9) * J.f; }   // profil: iki kanat da sırttan geriye
    GR.frame(sh[0] - sd * h * .25, sh[1] + h * .15, P.rot, sd, 1);
    KN.feathered(Object.assign({ dark: .93, rim: mask ? 0 : .75, ruin: .55, t, lit: [LIT[0] * sd, LIT[1]] }, P));
    GR.unframe();
  }
}
function nif_sfdraw(J, p, mask) {   // mask: maske geçişi (beyaz vuruş ve kenar ışığı yok: kütle delinmez)
  return SF.draw(J, { lum: mask ? 0 : p.lum ?? .2, lit: p.lit || [.3, -.95], t: p.t || 0, legs: p.legs ?? true, skirt: true, eye: mask ? 0 : p.eye ?? 0, wind: p.wind ?? .5,
    cloak: p.cloak ?? 1.3, halo: mask ? 0 : p.halo ?? 3.5, lines: mask ? 0 : 2, rim: mask ? .001 : undefined, seed: p.seed || 3 });
}
function nif_seytan(p) {
  const J = nif_rig(p);
  if (p.wings !== false && !(p.ic && p.ic.wings)) nif_kanat(J, p);
  if (p.mid) p.mid(J);
  if (p.ic) nif_icCehennem(J, m => { if (p.ic.wings && p.wings !== false) nif_kanat(J, p, m); nif_sfdraw(J, p, m); }, Object.assign({ t: p.t }, p.ic));
  else nif_sfdraw(J, p);
  return J;
}
// güneşe doğru ışık yönü (birim)
function nif_isik(S, x, y) { const L = [S.x - x, S.y - y], l = Math.hypot(L[0], L[1]) || 1; return [L[0] / l, L[1] / l]; }

// ═════════ iç cehennem ═════════
// "Cehennemi içinde taşıyor": siluetin içi bir pencere gibi yanan gölü gösterir (filmin görsel anahtarı; A01, G02, G07, L07).
// Yöntem (motora dokunmadan):
//  1) figür (drawFig(true): kanatlar + SF.draw, beyaz vuruşsuz) beyaza boşaltılmış kutuda çizilir; koyu çekirdeği maske olur;
//  2) maske çeyrek çözünürlükte kapanır (beyaz vuruş delikleri dolar) ve kenardan içe aşındırılır: siluetin dış hattında kalın siyah çerçeve kalır;
//  3) kutu eski hâline döner, figür gerçek hâliyle çizilir (drawFig(false));
//  4) içerik (nif_icGol ya da cizGol) ölçekli çerçevede (GR.frame) basılır ve maskeyle karışır: ton katmanı maske alfasıyla,
//     tarama yaması maskenin yarısını geçen yerde içeriğinkiyle. Tarama aralığı dünyaya bağlı olduğundan küçük ölçekte de çizgiler seyrek ve okunur kalır.
// o: {t, k (0..1 pencerenin açıklığı: maske genişler, alevler yükselir), erode (baş boyu biriminde çerçeve kalınlığı; .2), neck (false: baş da pencereye dahil),
//     bot (kalçadan aşağı sınır, baş boyu; yok = sınırsız), margin (kutu payı, baş boyu; kanatlı figürde 6), scale (içerik ölçeği; h/96),
//     at: [x, y] (içeriğin ufuk odağının geleceği dünya noktası; kalçanın biraz üstü),
//     grow: {g (≥ 1, maskenin büyüme katsayısı), c: [x, y] (büyüme merkezi), p (0..1: içeriğin tam kareye (ölçek 1, odak (910, 600)) geçişi)},
//     full (true: içerik onaylı göl karesi cizGol, figürsüz), gol (cizGol ek seçenekleri), draw (t, k) => {} (özel içerik, yerel 1920×1080, odak (910, 600))}
// Başka gruplar: kendi figür çizimlerini drawFig olarak verip aynı işlevi çağırabilir (açık levhada, kamera dönüşümü ne olursa olsun).
function nif_icGol(t, k = 1) {
  const { tone } = GR, X = 910, Y = 600, fh = lerp(.3, 1, E.io2(clamp(k)));
  const V = new Path2D(); V.rect(-3000, -3000, 8000, 3000 + Y); GR.fill(V, tone(.02), { th: 0, id: 1 });
  PR.glow(X, Y - 6, 20, 200, 1, .55);
  PR.lake(Y, Y + 900, t, { tone: [.07, .02], crests: 3, p0: 9.5, refl: [{ x: X, w: 150, v: .95, len: 130, rows: 5 }] });
  PR.flameBank(X - 900, X + 900, Y + 2, 30, t, 1, { env: f => .35 + .65 * Math.pow(Math.sin(f * PI), 2), smoke: false });
  PR.flameBank(X - 560, X + 560, Y + 8, 260 * fh, t, 5, { n: 8, wr: .5, curl: .5, speed: .6, solidBelow: 900, strip: .3, frags: false, env: f => .35 + .65 * Math.pow(Math.sin(f * PI), 1.5) });
}
const NIF_MK = makeCanvas(DW, DH), NIF_mk = NIF_MK.getContext('2d', { willReadFrequently: true });
const NIF_MG = makeCanvas(DW, DH), NIF_mg = NIF_MG.getContext('2d', { willReadFrequently: true });
// yuvarlak köşeli biçim işlemi: kutu bulanıklığı (ayrık, kayan toplam; iki kez) + eşik. mx: genişletme (true) ya da aşındırma (false)
function nif_morf(A, w, h, r, mx) {
  if (r < 1) return A;
  const T = new Float32Array(A.length);
  const pass = () => {
    for (let y = 0; y < h; y++) { const o = y * w; let acc = 0; for (let k = -r; k <= r; k++) acc += A[o + clamp(k, 0, w - 1)];
      for (let x = 0; x < w; x++) { T[o + x] = acc / (2 * r + 1); acc += A[o + Math.min(w - 1, x + r + 1)] - A[o + Math.max(0, x - r)]; } }
    for (let x = 0; x < w; x++) { let acc = 0; for (let k = -r; k <= r; k++) acc += T[clamp(k, 0, h - 1) * w + x];
      for (let y = 0; y < h; y++) { A[y * w + x] = acc / (2 * r + 1); acc += T[Math.min(h - 1, y + r + 1) * w + x] - T[Math.max(0, y - r) * w + x]; } }
  };
  r = Math.max(1, Math.round(r * .62)); pass(); pass();
  const th = mx ? .04 : .96;
  for (let i = 0; i < A.length; i++) A[i] = A[i] > th ? 1 : 0;
  return A;
}
function nif_icCehennem(J, drawFig, o = {}) {
  const { tx, px } = GR, t = o.t || 0, h = J.h, kOpen = clamp(o.k ?? 1);
  const M = tx.getTransform(), sc = Math.hypot(M.a, M.b);
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const q of [J.hd, J.hip, J.shN, J.shF, J.elN, J.elF, J.wrN, J.wrF, J.knN, J.knF, J.anN, J.anF]) {
    const d = M.transformPoint(new DOMPoint(q[0], q[1])); x0 = Math.min(x0, d.x); y0 = Math.min(y0, d.y); x1 = Math.max(x1, d.x); y1 = Math.max(y1, d.y);
  }
  const mg = (o.margin ?? 2.6) * h * sc;
  x0 = Math.max(0, Math.floor(x0 - mg)); y0 = Math.max(0, Math.floor(y0 - mg)); x1 = Math.min(DW, Math.ceil(x1 + mg)); y1 = Math.min(DH, Math.ceil(y1 + mg));
  const bw = x1 - x0, bh = y1 - y0;
  if (bw < 8 || bh < 8 || kOpen <= 0) { drawFig(false); return; }
  // 1) maske: beyaz kutuda figür (çeyrek çözünürlük)
  const S0 = tx.getImageData(x0, y0, bw, bh);
  tx.save(); tx.setTransform(1, 0, 0, 1, 0, 0); tx.fillStyle = '#fff'; tx.fillRect(x0, y0, bw, bh); tx.restore();
  drawFig(true);
  const Bw = tx.getImageData(x0, y0, bw, bh).data;
  tx.putImageData(S0, x0, y0);
  const Q = 4, qw = Math.ceil(bw / Q), qh = Math.ceil(bh / Q), A = new Float32Array(qw * qh);
  const neckY = o.neck === false ? -1e9 : M.transformPoint(new DOMPoint(J.nk[0], J.nk[1] + .2 * h)).y - y0;
  const botY = o.bot == null ? 1e9 : M.transformPoint(new DOMPoint(J.hip[0], J.hip[1] + o.bot * h)).y - y0;
  for (let y = 0; y < qh; y++) { const yy = Math.min(bh - 1, y * Q + 2); for (let x = 0; x < qw; x++) { const v = Bw[(yy * bw + Math.min(bw - 1, x * Q + 2)) * 4]; A[y * qw + x] = v < 90 ? 1 : 0; } }
  const rc = Math.max(1, Math.round(.1 * h * sc / Q));
  nif_morf(A, qw, qh, rc, true); nif_morf(A, qw, qh, rc, false);                       // kapanış: vuruş delikleri dolar
  for (let y = 0; y < qh; y++) { const yy = y * Q; if (yy >= neckY && yy <= botY) continue; for (let x = 0; x < qw; x++) A[y * qw + x] = 0; }
  nif_morf(A, qw, qh, Math.round((o.erode ?? .2) * h * sc * lerp(2.4, 1, E.out2(kOpen)) / Q), false);  // çerçeve
  // 2) figür gerçek hâliyle
  drawFig(false);
  // 3) maske tuvali: küçük maske → tam çözünürlük (yumuşak büyütme), isteğe bağlı büyüme
  const mi = new ImageData(qw, qh); for (let i = 0; i < A.length; i++) { mi.data[i * 4] = mi.data[i * 4 + 1] = mi.data[i * 4 + 2] = 255; mi.data[i * 4 + 3] = A[i] * 255; }
  NIF_mk.setTransform(1, 0, 0, 1, 0, 0); NIF_mk.clearRect(0, 0, qw + 2, qh + 2); NIF_mk.putImageData(mi, 0, 0);
  const G = o.grow, g = G ? Math.max(1, G.g) : 1, c = G ? M.transformPoint(new DOMPoint(G.c[0], G.c[1])) : { x: 0, y: 0 };
  const gm = new DOMMatrix([g, 0, 0, g, c.x * (1 - g), c.y * (1 - g)]).translate(x0, y0).scale(Q, Q);
  const bx0 = Math.max(0, Math.floor(c.x + (x0 - c.x) * g)), by0 = Math.max(0, Math.floor(c.y + (y0 - c.y) * g));
  const bx1 = Math.min(DW, Math.ceil(c.x + (x0 + qw * Q - c.x) * g)), by1 = Math.min(DH, Math.ceil(c.y + (y0 + qh * Q - c.y) * g));
  const R = [bx0, by0, bx1 - bx0, by1 - by0];
  if (R[2] < 2 || R[3] < 2) return;
  NIF_mg.setTransform(1, 0, 0, 1, 0, 0); NIF_mg.clearRect(R[0], R[1], R[2], R[3]);
  NIF_mg.setTransform(gm); NIF_mg.imageSmoothingEnabled = true; NIF_mg.imageSmoothingQuality = 'high'; NIF_mg.drawImage(NIF_MK, 0, 0, qw, qh, 0, 0, qw, qh);
  NIF_mg.setTransform(1, 0, 0, 1, 0, 0);
  const MD = NIF_mg.getImageData(R[0], R[1], R[2], R[3]).data;
  // 4) içerik
  const T0 = tx.getImageData(R[0], R[1], R[2], R[3]), P0 = px.getImageData(R[0], R[1], R[2], R[3]);
  let ks = o.scale ?? h / 96, at = o.at || [J.shC[0], J.shC[1] + .9 * h];
  const F = [910, 600];
  if (G && G.p) { const u = E.io2(clamp(G.p)); ks = lerp(ks, 1, u); at = [lerp(at[0], F[0], u), lerp(at[1], F[1], u)]; }
  GR.save();
  for (const cx of [tx, px, GR.ox]) { cx.save(); cx.setTransform(1, 0, 0, 1, 0, 0); cx.beginPath(); cx.rect(R[0], R[1], R[2], R[3]); cx.restore(); cx.clip(); }
  px.save(); px.setTransform(1, 0, 0, 1, 0, 0); px.fillStyle = GR.hatch({ th: 0, id: 1 }); px.fillRect(R[0], R[1], R[2], R[3]); px.restore();   // içeriğin tarama zemini: yatay (figürün tüy taraması sızmasın)
  GR.frame(at[0] - F[0] * ks, at[1] - F[1] * ks, 0, 1, ks);
  if (o.draw) o.draw(t, kOpen);
  else if (o.full) cizGol(t, Object.assign({ fig: false, chains: false }, o.gol || {}));
  else nif_icGol(t, kOpen);
  GR.unframe();
  GR.restore();
  const T1 = tx.getImageData(R[0], R[1], R[2], R[3]), P1 = px.getImageData(R[0], R[1], R[2], R[3]);
  const a0 = T0.data, a1 = T1.data, p0 = P0.data, p1 = P1.data;
  for (let j = 0, m = a0.length; j < m; j += 4) {
    let a = MD[j + 3] / 255; if (a <= 0) continue; a = clamp((a - .5) * 16 + .5);
    a0[j] = a0[j] + (a1[j] - a0[j]) * a; a0[j + 1] = a0[j]; a0[j + 2] = a0[j];
    if (a > .5) { p0[j] = p1[j]; p0[j + 1] = p1[j + 1]; p0[j + 2] = p1[j + 2]; }
  }
  tx.putImageData(T0, R[0], R[1]); px.putImageData(P0, R[0], R[1]);
}

// ═════════ P001 (A01): kanca ═════════
// A02 (cennet grubu) aynı duruş ve aynı kadrajla açılır: bu yerleşim bağlayıcıdır (kalça (860, 560), h 96, facing 1; son kamera {960, 540, 1}).
const NIF_A01 = { x: 860, y: 560, h: 96, facing: 1, twist: .35, lean: -.02, head: .22, shTilt: -.05, armN: [.2, .25], armF: [-.16, .2], legN: [.2, -.06], legF: [-.17, -.02] };
const NIF_A01_KAMERA = { cx: 960, cy: 540, z: 1.08 };   // son kare
const NIF_A01_KANAT = { open: .55, lift: .5, droop: .45, spanL: 8.6, spanR: 7.8, rotL: -.06, rotR: .1 };
function nif_a01(t, o = {}) {
  return cizNifates(t, {
    sun: { x: 1010, y: 400, r: 330 }, hz: 870, tepe: { x: 880, y: 940, s: 1, seed: 3 }, t,
    clouds: [{ x: -80, y: 120, w: 760, h: 360, seed: 12, n: 4 }, { x: 1830, y: 160, w: 880, h: 340, seed: 19, n: 4 }],
    fig: () => nif_seytan(Object.assign({}, NIF_A01, { t, lum: .12, wings: NIF_A01_KANAT, lit: [.4, -.92], ic: o.ic === false ? null : Object.assign({ k: 1, wings: true, margin: 6, neck: false }, o.ic) })) });
}
plan('P001', (ctx, st) => {
  const t = st.t, tC = Wd('A01', 'cehennem');
  levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, NIF_A01_KAMERA, nif_u(t, st.at, st.end), E.out2), () => nif_a01(t, { ic: { k: lerp(.55, 1, E.io2(nif_u(t, tC - 1, tC + 1.5))) } }), [.5, 0, 1]);
}, { tr: { type: 'cut' },
  over: (ctx, st) => { const t0 = Wd('A01', 'cehennemim') - st.at; quote(ctx, '“Ben cehennemim.”', 1570, 120, st.lt, { t0, px: 74, panel: .55 }); } });

// ═════════ ortak ═════════
const NIF_PROF = { open: .45, lift: 0, droop: 1, spanL: 7, prof: true };   // profil: tek kanat sırttan aşağı, pelerin gibi
const NIF_KAPALI = { open: .25, lift: .05, droop: .9 };   // kanatlar katlı: sırtta pelerin gibi
const NIF_BG = [.5, 0, 1];
// yazı: bulutun koyu kütlesi üstünde, yumuşak zeminle
function nif_soz(ctx, s, x, y, st, wd, o = {}) { quote(ctx, s, x, y, st.lt, Object.assign({ t0: wd - st.at, px: 68, maxW: 900, panel: .55 }, o)); }

// ═════════ P064 (F09): dağın tepesine süzülür ═════════
// Kanatlar açık, sol üstten süzülür; 'konar' kelimesinde ayaklar yere değer, kanatlar kapanır. Işık (melek kılığı) inişte söner.
plan('P064', (ctx, st) => {
  const t = st.t, t0 = S('F09'), tK = Wd('F09', 'konar');
  const S0 = { x: 1300, y: 340, r: 290 }, top = { x: 760, y: 770, s: .8, seed: 5 }, h = 62;
  const u = E.out2(nif_u(t, t0 - .3, tK)), land = nif_u(t, tK - .15, tK + 1.3), lk = E.io2(land);
  const fold = Math.sin(PI * nif_u(t, tK - .15, tK + .6)) * (1 - land);   // dokunuşta dizler kısa bir an bükülür
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => cizNifates(t, {
    sun: S0, hz: 880, tepe: top, t, clouds: [{ x: 120, y: 120, w: 900, h: 300, seed: 41, n: 4 }],
    fig: (tp) => {
      const gy = tp[1] + 4, px0 = [260, 120], px1 = [tp[0], gy - 4 * h];
      const x = lerp(px0[0], px1[0], u), y = lerp(px0[1], px1[1], u) - Math.sin(PI * u) * 60 * (1 - u);
      const fl = 1 - lk;   // uçuş oranı
      nif_seytan({ x, y: y + fold * .35 * h, h, facing: 1, twist: lerp(.55, .4, lk), lean: lerp(.35, 0, lk), head: lerp(-.1, .12, lk), t,
        armN: [lerp(-.5, .15, lk), lerp(.3, .25, lk)], armF: [lerp(-.7, -.12, lk), .2],
        legN: [lerp(-.25, .12 + .4 * fold, lk), lerp(.5, -.05 - .8 * fold, lk)], legF: [lerp(-.45, -.1 + .3 * fold, lk), lerp(.6, -.03 - .6 * fold, lk)],
        lum: lerp(.55, .25, E.io2(nif_u(t, t0, tK + .5))), lit: nif_isik(S0, x, y - 2 * h),
        wings: { open: lerp(1, .3, lk), lift: lerp(.75, .25, lk), droop: lerp(.1, .6, lk), spanL: 8.6, spanR: 7.8 } });
    } }), NIF_BG);
}, { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => { const t0 = Wd('F09', 'nifatesin') - st.at; etiket(ctx, 'Nifates Dağı', 1180, 830, st.lt - t0, st.d - t0 - .2, { px: 46 }); } });

// ═════════ P065 (G01): bölüm kartı; geniş plan, tepede yalnız figür ═════════
plan('P065', (ctx, st) => {
  const t = st.t, S0 = { x: 1290, y: 520, r: 360 };
  levha(ctx, camLerp({ cx: 960, cy: 540, z: 1.06 }, { cx: 960, cy: 540, z: 1 }, st.p, E.io2), () => cizNifates(t, {
    sun: S0, hz: 860, tepe: { x: 1290, y: 862, s: .6, seed: 7 }, t, aden: { x: 380, y: 850, w: 300, s: .8 },
    clouds: [{ x: 520, y: 240, w: 1500, h: 470, seed: 12, n: 5 }],
    fig: (tp) => nif_seytan({ x: tp[0], y: 0, ground: tp[1] + 2, h: 24, facing: 1, twist: .35, head: .1, t, lum: .22, lit: nif_isik(S0, tp[0], tp[1] - 100),
      wings: { open: .3, lift: .25, droop: .6 } }) }), NIF_BG);
}, { tr: { type: 'black', dur: 1.4, end: true },
  over: (ctx, st) => chapterCard(ctx, 'GÜNEŞE İTİRAF', 'Kimsenin duymadığını sanırken, Şeytan kendine ne söyler?', st.lt, st.d, { x: 620, y: 290 }) });

// ═════════ P066 (G02): siluetin göğsünde yanan göl ═════════
// 'cehennemi' kelimesinde göğüste bir kor belirir, 'taşıyor' ile pencere açılır; 'kaçamıyorsa' ile alevler en yüksek.
plan('P066', (ctx, st) => {
  const t = st.t, S0 = { x: 1430, y: 400, r: 300 }, tC = Wd('G02', 'cehennemi'), tK = Wd('G02', 'kaçamıyorsa');
  const k = .55 * E.io2(nif_u(t, tC - .2, tC + 1.4)) + .45 * E.io2(nif_u(t, tK - 1, tK + 1.2));
  const P = { x: 720, y: 0, ground: 980, h: 100, facing: 1, twist: .45, lean: .02, head: .02, shTilt: -.03, armN: [.1, .3], armF: [-.08, .25], legN: [.12, -.05], legF: [-.1, -.03] };
  levha(ctx, camLerp({ cx: 900, cy: 560, z: 1 }, { cx: 770, cy: 470, z: 1.15 }, st.p, E.io2), () => cizNifates(t, {
    sun: S0, hz: 930, tepe: { x: 720, y: 982, s: 1, seed: 9 }, t, clouds: [{ x: 60, y: 120, w: 820, h: 330, seed: 12, n: 4 }],
    fig: () => nif_seytan(Object.assign({}, P, { t, lum: .22, lit: nif_isik(S0, 720, 500), wings: NIF_KAPALI,
      ic: k > .01 ? { k, wings: false, neck: true, margin: 2.6, at: [720, 980 - 4.15 * 100 - .1 * 100], scale: .62 } : null })) }), NIF_BG);
}, { tr: { type: 'cut' } });

// ═════════ P068 (G03): profil güneşe karşı; eliyle gözünü siper eder (alttan) ═════════
// 'ışınlarından' kelimesinde yakın kol kalkar, el kaşın üstüne gelir; güneşten yüzüne iki ince ışın kaması uzanır.
plan('P068', (ctx, st) => {
  const t = st.t, S0 = { x: 1290, y: 380, r: 320 }, tI = Wd('G03', 'nefret') - .9, h = 104, FX = 1000;
  const up = E.io2(nif_u(t, tI - .6, tI + .9));
  levha(ctx, camLerp({ cx: 960, cy: 560, z: 1 }, { cx: 1000, cy: 520, z: 1.08 }, st.p, E.io2), () => {
    const J0 = nif_rig({ x: FX, y: 0, ground: 1030, h, facing: 1, twist: .9, head: .18 });
    const hd = J0.hd, a = Math.atan2(hd[1] - S0.y, hd[0] - S0.x);
    cizNifates(t, {
      sun: S0, hz: 990, tepe: { x: FX, y: 1032, s: 1.3, seed: 11 }, t, clouds: [{ x: 40, y: 160, w: 860, h: 420, seed: 12, n: 5 }],
      beams: [[a - .025, .03, 1300], [a + .03, .022, 1250], [-1.2, .035, 1300], [-.45, .04, 1200], [-2.2, .03, 1300]],
      fig: () => nif_seytan({ x: FX, y: 0, ground: 1030, h, facing: 1, twist: .9, lean: lerp(0, -.04, up), head: lerp(.18, .1, up), shTilt: lerp(-.03, -.1, up), t,
        armN: (() => { const A = nif_ik(J0.shN, [hd[0] + .6 * h, hd[1] + .12 * h], h, 1, 0, -1); return [lerp(.14, A[0], up), lerp(.25, A[1], up)]; })(), armF: [-.15, .2],
        legN: [.18, -.04], legF: [-.14, -.02], lum: .22, lit: nif_isik(S0, hd[0], hd[1]), wings: NIF_PROF }) });
  }, NIF_BG);
}, { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => nif_soz(ctx, '“Ey güneş… ışınlarından nefret ediyorum.”', 360, 190, st, Wd('G03', 'ey'), { maxW: 640 }) });

// ═════════ P069 (G04): baş öne eğilir; ışık yumuşar (arkadan) ═════════
plan('P069', (ctx, st) => {
  const t = st.t, S0 = { x: 1010, y: 400, r: 380 }, tB = Wd('G04', 'benden'), tY = Wd('G04', 'beni');
  const bow = E.io2(nif_u(t, tB - .4, tB + 2.2)), soft = E.io2(nif_u(t, tY - 1, tY + 4));
  levha(ctx, camLerp({ cx: 960, cy: 560, z: 1 }, { cx: 990, cy: 540, z: 1.1 }, st.p, E.io2), () => cizNifates(t, {
    sun: S0, hz: 900, tepe: { x: 1000, y: 902, s: .9, seed: 13 }, t, soft, aden: { x: 1620, y: 900, w: 260, s: .7 },
    clouds: [{ x: 150, y: 190, w: 1050, h: 440, seed: 21, n: 5 }, { x: 1900, y: 110, w: 760, h: 320, seed: 19, n: 4 }],
    fig: (tp) => nif_seytan({ x: tp[0], y: 0, ground: tp[1] + 2, h: 74, facing: 1, twist: .12, lean: lerp(0, .1, bow), head: lerp(.12, -.55, bow), shTilt: lerp(-.03, .06, bow), t,
      armN: [lerp(.12, .05, bow), .2], armF: [lerp(-.1, -.03, bow), .2], legN: [.12, -.04], legF: [-.12, -.02], lum: .22, lit: [0, -1],
      wings: { open: lerp(.25, .2, bow), lift: .05, droop: lerp(.9, 1, bow) } }) }), NIF_BG);
}, { tr: { type: 'cut' },
  over: (ctx, st) => nif_soz(ctx, '“Hak etmemişti.”', 360, 200, st, Wd('G04', 'hak'), { px: 72 }) });

// ═════════ P070 (G05): güneş diskinin içinde anı ═════════
// Kadrajı güneş doldurur. İçinde açık (cennet tarifi) saflar: arkasındaki taramayla ayrılan kâğıt beyazı, sade melekler;
// önde, safların arasında bir boşlukta tek, sıradan küçük melek. Anı 'keşke' ile belirir, 'kalırdım' ile söner.
function nif_melek(x, y, s) {   // sade melek (arkadan): baş, omuzdan yere genişleyen giysi, başın üstüne yükselen sivri katlı kanatlar; kâğıt beyazı
  const { tx, tone } = GR;
  for (const sd of [-1, 1]) {
    const Wg = new Path2D(); Wg.moveTo(x + sd * 5 * s, y - 34 * s); Wg.quadraticCurveTo(x + sd * 22 * s, y - 52 * s, x + sd * 12 * s, y - 88 * s);
    Wg.quadraticCurveTo(x + sd * 30 * s, y - 50 * s, x + sd * 20 * s, y + 4 * s); Wg.quadraticCurveTo(x + sd * 14 * s, y + 22 * s, x + sd * 8 * s, y + 26 * s); Wg.closePath();
    GR.fill(Wg, tone(sd < 0 ? 1 : .96), { th: sd * .5, id: 6 });
  }
  const B = new Path2D(); B.moveTo(x - 8 * s, y - 36 * s); B.quadraticCurveTo(x - 14 * s, y + 10 * s, x - 17 * s, y + 46 * s); B.lineTo(x + 17 * s, y + 46 * s); B.quadraticCurveTo(x + 14 * s, y + 10 * s, x + 8 * s, y - 36 * s); B.closePath();
  GR.fill(B, tone(1), { th: PI / 2, id: 9 });
  const Hd = new Path2D(); Hd.ellipse(x, y - 44 * s, 6.5 * s, 7.5 * s, 0, 0, TAU); GR.fill(Hd, tone(1), { th: 0, id: 5 });
  tx.fillStyle = tone(.05);   // gölge yanı (sağ): sağ kanadın iç kenarı ve giysi kıvrımı (koyu çapa)
  tx.beginPath(); tx.moveTo(x + 13 * s, y - 70 * s); tx.quadraticCurveTo(x + 24 * s, y - 40 * s, x + 18 * s, y + 4 * s); tx.lineTo(x + 14 * s, y + 2 * s); tx.quadraticCurveTo(x + 19 * s, y - 40 * s, x + 13 * s, y - 70 * s); tx.fill();
  tx.beginPath(); tx.moveTo(x + 9 * s, y - 6 * s); tx.quadraticCurveTo(x + 13 * s, y + 20 * s, x + 14 * s, y + 44 * s); tx.lineTo(x + 10 * s, y + 44 * s); tx.quadraticCurveTo(x + 10 * s, y + 18 * s, x + 9 * s, y - 6 * s); tx.fill();
}
plan('P070', (ctx, st) => {
  const t = st.t, tK = Wd('G05', 'keşke'), tE = Se('G05');
  const a = E.io2(nif_u(t, tK, tK + 1)) * (1 - E.io2(nif_u(t, tE - .2, tE + .6)));
  levha(ctx, camLerp({ cx: 960, cy: 560, z: 1.12 }, { cx: 960, cy: 540, z: 1 }, st.p, E.io2), () => {
    const { tx, tone } = GR, S0 = { x: 960, y: 560, r: 560 };
    nif_gok(S0, { beams: [] });
    // diskin içi: anı (açık, hafif taralı zemin; kâğıt beyazı figürler)
    const D = new Path2D(); D.arc(S0.x, S0.y, S0.r - 2, 0, TAU);
    GR.save(); for (const c of [tx, GR.px]) c.clip(D);
    tx.save(); tx.globalAlpha = a; GR.px.save(); GR.px.globalAlpha = a > .5 ? 1 : 0;
    const g = tx.createRadialGradient(960, 300, 40, 960, 560, 640); g.addColorStop(0, tone(1)); g.addColorStop(.3, tone(.82)); g.addColorStop(1, tone(.6));
    GR.fill(D, g, { type: 'rad', cx: 960, cy: 300, id: 1 });
    // bulut terası: safların bastığı açık zemin, altında koyu çapa
    const T = new Path2D(); T.moveTo(300, 800); for (let x = 300; x <= 1620; x += 60) T.lineTo(x, 800 + 18 * Math.sin(x * .02)); T.lineTo(1620, 1200); T.lineTo(300, 1200); T.closePath();
    GR.fill(T, tone(.97), { th: 0, id: 2 });
    tx.fillStyle = tone(.08); tx.beginPath(); tx.moveTo(300, 960); for (let x = 300; x <= 1620; x += 40) tx.lineTo(x, 950 + 22 * Math.sin(x * .013 + 1)); tx.lineTo(1620, 1200); tx.lineTo(300, 1200); tx.fill();
    const r = rng(5);
    for (const [y, s, n, sp] of [[520, 1.25, 9, 96], [610, 1.6, 7, 124], [720, 2.0, 6, 158]]) {
      for (let i = 0; i < n; i++) { const x = 960 + (i - (n - 1) / 2) * sp + (r() - .5) * sp * .25 + (y === 610 ? sp * .5 : 0); if (y === 720 && Math.abs(x - 960) < sp * 1.1) continue; nif_melek(x, y, s); }
    }
    nif_melek(960, 770, 2.3);   // safların arasında, önde, tek başına: sıradan küçük melek
    tx.restore(); GR.px.restore(); GR.restore();
    // önde, sol altta: izleyenin (Şeytan'ın) koyu omuz ve kanat kütlesi: kadrajın çapası
    const Sh = new Path2D(); Sh.moveTo(-40, 1120); Sh.quadraticCurveTo(40, 840, 230, 780); Sh.quadraticCurveTo(330, 760, 400, 860); Sh.quadraticCurveTo(470, 960, 520, 1120); Sh.closePath();
    GR.fill(Sh, tone(.03), { th: .4, id: 6 });
    PR.cuts([[60, 930], [140, 830], [240, 785], [330, 790], [400, 860]], [.3, .95], { len: [14, 70], gap: [30, 70], w: 5, seed: 3, clip: Sh, bend: .2 });
  }, NIF_BG);
}, { tr: { type: 'fade', dur: .8 } });

// ═════════ P072 (G07): doruk; kamera siluetin içine girer, yanan göl kareyi doldurur ═════════
// Siluetin içi baştan yanar (iç cehennem, kanatlar dahil). 'nereye kaçayım' ile baş kalkar; 'hangi yana' ile maske göğüsten büyür
// (kamera değil maske büyür: yakınlaşma sınırı 1,25) ve 'ben' kelimesine kadar kareyi doldurur: yalnız yanan göl kalır.
plan('P072', (ctx, st) => {
  const t = st.t, S0 = { x: 1460, y: 380, r: 290 }, tN = Wd('G07', 'nereye'), tH = Wd('G07', 'hangi'), tB = Wd('G07', 'ben');
  const lift = E.io2(nif_u(t, tN - .3, tN + 1.2)), gp = nif_u(t, tH, tB - .1);
  const P = { x: 860, y: 0, ground: 975, h: 100, facing: 1, twist: .5, lean: lerp(.08, .02, lift), head: lerp(-.25, .15, lift), shTilt: lerp(.07, -.02, lift),
    armN: [.05, .55], armF: [-.05, .5], legN: [.12, -.05], legF: [-.1, -.03] };
  const J0 = nif_rig(P), c = [J0.shC[0], J0.shC[1] + .95 * J0.h];
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => {
    if (gp >= 1) { nif_icGolTam(t); return; }
    cizNifates(t, {
      sun: S0, hz: 930, tepe: { x: 860, y: 977, s: 1, seed: 15 }, t, clouds: [{ x: 40, y: 130, w: 820, h: 340, seed: 12, n: 4 }, { x: 1900, y: 60, w: 700, h: 260, seed: 19, n: 3 }],
      fig: () => nif_seytan(Object.assign({}, P, { t, lum: .2, lit: nif_isik(S0, 860, 500), wings: { open: .42, lift: .3, droop: .7 },
        ic: { k: 1, wings: true, neck: false, margin: 6, full: true, gol: { sway: .02, light: lerp(.25, 1, E.io2(gp)) }, grow: { g: lerp(1, 30, Math.pow(gp, 2.2)), c, p: E.in2(gp) } } })) });
  }, NIF_BG);
}, { tr: { type: 'fade', dur: .6 },
  over: (ctx, st) => nif_soz(ctx, '“Ben cehennemim.”', 470, 150, st, Wd('G07', 'ben'), { px: 80, panel: .4 }) });
// tam kare iç cehennem (maskenin büyümesi bittikten sonra): yerel çerçeve dünya ile aynı
function nif_icGolTam(t) { cizGol(t, { fig: false, chains: false, sway: .02 }); }

// ═════════ P074–P075 (G09, G09b): diz ışığa doğru bükülür; durur, doğrulur ═════════
// Yandan orta plan, güneş sağda. G09 boyunca yakın diz yavaşça öne bükülür, gövde öne eğilir, baş düşer (izleyici diz çökecek sanır);
// G09b'de 'ama' kelimesine dek bekler, 'gururum' ile doğrulur, baş kalkar. Yazı: "boyun eğmek", 'yasaklıyor' ile zincir halkasıyla kilitlenir.
const NIF_G09_S = { x: 1450, y: 360, r: 300 };
function nif_g09(t, b, hd) {   // b: 0..1 bükülme, hd: baş (−1 eğik … 1 dik, mağrur)
  const S0 = NIF_G09_S, e = E.io2(b);
  return cizNifates(t, {
    sun: S0, hz: 930, tepe: { x: 820, y: 978, s: 1, seed: 17 }, t, soft: .3 * e, clouds: [{ x: 60, y: 140, w: 900, h: 360, seed: 12, n: 4 }],
    beams: [[Math.atan2(560 - S0.y, 820 - S0.x), .04 + .02 * e, 1100], [-2.0, .03, 1200], [-1.1, .035, 1300], [-.4, .04, 1300]],
    fig: () => nif_seytan({ x: 820, y: 0, ground: 975, h: 96, facing: 1, twist: .85, lean: .22 * e - .03 * hd, head: lerp(-.05, -.42, e) + .25 * Math.max(0, hd), shTilt: lerp(-.03, .04, e), t,
      armN: [lerp(.1, .3, e), lerp(.25, .35, e)], armF: [lerp(-.1, .15, e), lerp(.2, .3, e)],
      legN: [lerp(.12, 1.25, e), lerp(-.05, -1.3, e)], legF: [lerp(-.1, .02, e), lerp(-.03, -1.35, e)],
      lum: .22, lit: nif_isik(S0, 820, 560), wings: NIF_PROF }) });
}
plan('P074', (ctx, st) => {
  const t = st.t, b = .72 * nif_u(t, Wd('G09', 'yumuşar') - .3, st.end);
  levha(ctx, camLerp({ cx: 960, cy: 560, z: 1 }, { cx: 900, cy: 600, z: 1.06 }, st.p, E.io2), () => nif_g09(t, b, 0), NIF_BG);
}, { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => nif_soz(ctx, '“Pişmanlığa hiç yer kalmadı mı?”', 400, 200, st, Wd('G09', 'pişmanlığa'), { maxW: 600 }) });
// kilitli söz: italik söz, çevresinde bir zincir halkası kapanır (sağ ucunda dikine ikinci halka). lt: kapanış zamanına göre (−: açık)
function nif_kilitliSoz(ctx, s, x, y, aIn, kap, o = {}) {
  if (NOTEXT || aIn <= 0) return;
  ctx.save(); baseT(ctx); ctx.globalAlpha = aIn;
  const px = o.px || 70; ctx.font = FONT.alinti(px); const wd = ctx.measureText(s).width;
  softPanel(ctx, x, y, wd * .5 + 170, 150, .62);
  ctx.fillStyle = PAPER_CSS; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(s, x, y);
  const rx = wd * .5 + 56, ry = px * .82, gap = 1.25 * (1 - E.out3(clamp(kap))), a0 = gap / 2, k = clamp(kap);
  const ring = (cx, cy, rx, ry, rot, g) => {
    for (const [w, col] of [[16, INK_CSS], [9, PAPER_CSS]]) { ctx.lineWidth = w; ctx.strokeStyle = col; ctx.lineCap = 'butt'; ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, rot, g / 2, TAU - g / 2); ctx.stroke(); }
  };
  ring(x, y, rx, ry, 0, gap);
  // ikinci halka: sağ uçtan aşağı sarkan, birinciye geçmiş dikine halka (kilit); kapanınca belirir
  if (k > 0) { ctx.globalAlpha = aIn * E.sine(clamp(k * 1.6)); ring(x + rx, y + ry * .9, 22, 46, 0, 0); ring(x, y, rx, ry, 0, 0); }
  ctx.restore();
}
plan('P075', (ctx, st) => {
  const t = st.t, tA = Wd('G09b', 'ama'), tG = Wd('G09b', 'gururum');
  const b = .72 * (1 - E.io2(nif_u(t, tA, tG + .6))), hd = E.io2(nif_u(t, tG - .3, tG + 1.2));
  levha(ctx, camLerp({ cx: 900, cy: 600, z: 1.06 }, { cx: 900, cy: 560, z: 1.1 }, st.p, E.io2), () => nif_g09(t, b, hd), NIF_BG);
}, { tr: { type: 'cut' },
  over: (ctx, st) => {
    const t = st.t, tB = Wd('G09b', 'boyun'), tY = Wd('G09b', 'yasaklıyor');
    nif_kilitliSoz(ctx, 'boyun eğmek', 420, 230, clamp((t - tB) / .6) * clamp((st.end - t) / .5), nif_u(t, tY - .2, tY + .5));
  } });

// ═════════ P076 (G10): arkasında hayal; onu izleyen ordunun gözleri ═════════
// Figür sağda, güneşe dönük; sırtındaki karanlık (cehennemden taşan duman) 'ordunun' kelimesiyle çift çift ince ışıklarla dolar.
function nif_gozler(cx, cy, n, a, t, seed) {   // karanlık kütlede çift çift ince göz ışıkları; uzaktakiler küçük ve sık. a: 0..1 kaçı açık
  const { tx, tone } = GR, r = rng(seed), E2 = [];
  for (let i = 0; i < n; i++) {
    const row = Math.floor(Math.sqrt(r()) * 5), d = 1 - row / 5;   // 0 en uzak sıra
    E2.push({ x: cx + (r() - .5) * (500 + 900 * d), y: cy - 260 + row * 100 + (r() - .5) * 70, s: .35 + .75 * d, o: r(), row });
  }
  E2.sort((p, q) => p.row - q.row);
  tx.fillStyle = tone(.96);
  for (const e of E2) {
    const op = clamp((a - e.o * .85) / .15); if (op <= 0) continue;
    const w = 20 * e.s, hh = Math.max(2.4, 4.2 * e.s * op), gap = 24 * e.s;
    for (const sd of [-1, 1]) { const x = e.x + sd * gap; tx.beginPath(); tx.moveTo(x - w, e.y + sd * .5); tx.quadraticCurveTo(x, e.y - hh * (sd < 0 ? 1 : .8), x + w, e.y - sd * .5); tx.quadraticCurveTo(x, e.y + hh * .7, x - w, e.y + sd * .5); tx.fill(); }
  }
}
plan('P076', (ctx, st) => {
  const t = st.t, S0 = { x: 1780, y: 330, r: 270 }, tO = Wd('G10', 'ordunun'), tE = Wd('G10', 'onlara');
  const a = E.io2(nif_u(t, tO - .5, tE + 1)), dk = E.io2(nif_u(t, st.at, tO + 1));
  levha(ctx, camLerp({ cx: 960, cy: 540, z: 1.04 }, { cx: 960, cy: 540, z: 1 }, st.p, E.io2), () => cizNifates(t, {
    sun: S0, hz: 940, tepe: { x: 1300, y: 978, s: 1, seed: 19 }, t, dark: .15 * dk, mid0: () => {
      // sırtındaki karanlık: sol yarıyı kaplayan duman kütlesi (güneşe bakan kenarı ince ışıklı); içinde gözler
      PR.cloud({ x: 380, y: 300, w: 1150, h: 420, seed: 33, lit: [1, -.1], base: .03, hi: .8, core: .02, n: 5, drift: Math.sin(t * .06) * 10 });
      PR.cloud({ x: 520, y: 700, w: 1300, h: 460, seed: 35, lit: [1, -.3], base: .03, hi: .75, core: .02, n: 5, drift: Math.sin(t * .05 + 2) * 10 });
      nif_gozler(470, 560, 46, a, t, 7);
    },
    fig: () => nif_seytan({ x: 1300, y: 0, ground: 975, h: 92, facing: 1, twist: .55, lean: .05, head: -.18, shTilt: .03, t, armN: [.08, .2], armF: [-.06, .2],
      legN: [.1, -.04], legF: [-.1, -.03], lum: .2, lit: nif_isik(S0, 1300, 550), wings: NIF_PROF }) }), NIF_BG);
}, { tr: { type: 'cut' } });

// ═════════ P079 (G13): güneş ile figür arasındaki mesafe açılır ═════════
plan('P079', (ctx, st) => {
  const t = st.t, u = E.io2(st.p), S0 = { x: lerp(1330, 1520, u), y: lerp(420, 450, u), r: 270 };
  levha(ctx, camLerp({ cx: 760, cy: 520, z: 1.25 }, { cx: 960, cy: 540, z: 1 }, st.p, E.io2), () => cizNifates(t, {
    sun: S0, hz: 900, tepe: { x: 560, y: 905, s: .85, seed: 21 }, t, dark: .1 * u, aden: { x: 1250, y: 905, w: 300, s: .7 },
    clouds: [{ x: 60, y: 140, w: 820, h: 330, seed: 12, n: 4 }, { x: 1900, y: 60, w: 700, h: 260, seed: 19, n: 3 }],
    fig: (tp) => nif_seytan({ x: tp[0], y: 0, ground: tp[1] + 2, h: 64, facing: 1, twist: .55, head: .04, t, armN: [.08, .2], armF: [-.08, .2],
      legN: [.12, -.04], legF: [-.1, -.03], lum: .18, lit: nif_isik(S0, tp[0], tp[1] - 160), wings: NIF_PROF }) }), NIF_BG);
}, { tr: { type: 'fade', dur: .8 } });

// ═════════ P080 (G14): güneşe sırtını döner; gölgesi uzayıp Aden'e ulaşır ═════════
// Dönüş 'sonunda kararını verir' ile (yandan → arkadan → öbür yan); gölge 'elveda' sözleriyle uzar, 'kötülük' kelimesinde Aden'e değer.
plan('P080', (ctx, st) => {
  const t = st.t, S0 = { x: 1560, y: 560, r: 250 }, tS = Wd('G14', 'sonunda'), tE = Wd('G14', 'elveda'), tK = Wd('G14', 'kötülük');
  const turn = E.io2(nif_u(t, tS + .2, Wd('G14', 'verir') + .8)), L = E.io2(nif_u(t, tE - .5, tK + .3));
  const fc = turn < .5 ? 1 : -1, tw = Math.abs(1 - 2 * turn) * .85;
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => cizNifates(t, {
    sun: S0, hz: 760, tepe: { x: 1120, y: 732, s: .62, seed: 23 }, t, dark: .2,
    clouds: [{ x: 340, y: 150, w: 1150, h: 380, seed: 12, n: 5 }],
    mid1: () => {   // güneşin aydınlattığı geniş vadi (gölgenin düştüğü açık zemin) ve uzakta Aden
      const V = new Path2D(); V.moveTo(-300, 790); for (let x = -300; x <= 2200; x += 80) V.lineTo(x, 790 + 12 * Math.sin(x * .004)); V.lineTo(2200, 1400); V.lineTo(-300, 1400); V.closePath();
      const g = GR.tx.createLinearGradient(0, 790, 0, 1080); g.addColorStop(0, GR.tone(.86)); g.addColorStop(1, GR.tone(.62));
      GR.fill(V, g, { type: 'persp', y0: 790, D: 300, p0: 9, p1: 12, id: 8 });
      nif_aden({ x: 400, y: 890, w: 460, s: 1.7 }, t);
    },
    fig: (tp) => {
      // gölge: ayaklardan güneşin tersine, yamaçtan vadiye inen koyu, sivrilen şerit; ucu Aden'e ulaşır
      const fx = tp[0], fy = tp[1] + 2, ex = lerp(fx - 60, 560, L), ey = lerp(fy + 12, 870, L);
      if (L > .01) {
        const dx = ex - fx, dy = ey - fy, ln = Math.hypot(dx, dy), nx = -dy / ln, ny = dx / ln, P = new Path2D();
        P.moveTo(fx + nx * 8, fy + ny * 8); P.quadraticCurveTo(fx + dx * .5 + nx * 40, fy + dy * .5 + ny * 40, ex + nx * 46, ey + ny * 30);
        P.quadraticCurveTo(ex - dx * .03, ey + 22, ex - nx * 40, ey - ny * 26); P.quadraticCurveTo(fx + dx * .5 - nx * 30, fy + dy * .5 - ny * 30, fx - nx * 8, fy - ny * 8); P.closePath();
        GR.fill(P, GR.tone(.03), { th: Math.atan2(dy, dx), id: 0 });
      }
      nif_seytan({ x: fx, y: 0, ground: fy, h: 46, facing: fc, twist: .1 + tw, head: lerp(.02, -.12, turn), t, armN: [.08, .2], armF: [-.08, .2],
        legN: [.1, -.04], legF: [-.1, -.03], lum: .15, lit: nif_isik(S0, fx, fy - 120), wings: Object.assign({}, NIF_PROF, { spanL: 6 }) });
    } }), NIF_BG);
}, { tr: { type: 'cut' },
  over: (ctx, st) => nif_soz(ctx, '“Kötülük: sen benim iyiliğim ol.”', 380, 130, st, Wd('G14', 'kötülük'), { maxW: 620, px: 66 }) });
