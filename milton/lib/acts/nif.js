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
  g.addColorStop(0, tone(k(1))); g.addColorStop(.08, tone(k(.95))); g.addColorStop(.22, tone(k(lerp(.86, .9, sf))));
  g.addColorStop(.5, tone(k(lerp(.74, .8, sf)))); g.addColorStop(1, tone(k(lerp(.6, .68, sf))));
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
  const { tone } = GR, hz = o.hz ?? 760, dk = o.dark || 0;
  for (const [dy, amp, v, seed, th] of [[0, 70, .5, 3, -.05], [70, 120, .22, 5, .08]]) {
    const r = rng(seed), P = []; P.push([-400, H + 400]);
    let y = hz + dy;
    for (let x = -400; x <= W + 400; x += 60) { y = hz + dy - amp * (.5 + .5 * Math.sin(x * .0042 + seed)) * (.6 + .4 * noise1(x * .01, seed)) + (r() - .5) * 10; P.push([x, y]); }
    P.push([W + 400, H + 400]);
    const Q = new Path2D(); poly(Q, P, true);
    GR.fill(Q, tone(lerp(v, v * .5, dk)), { th, id: 4 });
  }
}
// Aden: uzakta, aşağıda; açık vadi tabanı ve küçük ağaç tepeleri (kâğıt beyazı yumru, altında mürekkep hilal). E: {x, y, w, s}
function nif_aden(E, t) {
  const { tx, tone } = GR, s = E.s ?? 1, w = E.w ?? 420;
  const V = new Path2D(); V.ellipse(E.x, E.y, w * .62, 48 * s, 0, 0, TAU);
  GR.fill(V, tone(.72), { th: 0, id: 1 });
  const r = rng(77), N = 30;
  const T = [];
  for (let i = 0; i < N; i++) { const a = r() * TAU, d = Math.sqrt(r()); T.push([E.x + Math.cos(a) * d * w * .52, E.y + Math.sin(a) * d * 36 * s, (6 + r() * 9) * s]); }
  T.sort((a, b) => a[1] - b[1]);
  for (const [x, y, rr] of T) {
    tx.fillStyle = tone(.08); tx.beginPath(); tx.ellipse(x + rr * .15, y + rr * .35, rr * 1.02, rr * .8, 0, 0, TAU); tx.fill();
    const C = new Path2D(); C.ellipse(x, y, rr, rr * .82, 0, 0, TAU); GR.fill(C, tone(1), { th: 0, id: 1 });
  }
  // duvar: ince açık çizgi (bahçenin sınırı)
  tx.strokeStyle = tone(.95); tx.lineWidth = 3 * s; tx.beginPath(); tx.ellipse(E.x, E.y + 4 * s, w * .56, 40 * s, 0, .15, PI - .15); tx.stroke();
}
// tepe: koyu kütle, ışık (güneş) yanında kenar ışığı ve içe giren beyaz vuruşlar. P: {x, y (zirve), s, lit: [lx, ly], seed}
const NIF_TEPE = [[-1300, 520], [-1060, 400], [-880, 330], [-720, 250], [-600, 196], [-470, 150], [-350, 96], [-250, 66], [-160, 36], [-96, 14], [-44, 2], [0, 0], [40, 4], [96, 18], [150, 42], [230, 64], [330, 110], [440, 140], [560, 200], [700, 240], [860, 310], [1040, 360], [1300, 520], [1300, 1400], [-1300, 1400]];
function nif_tepe(P) {
  const s = P.s ?? 1, pts = NIF_TEPE.map(([x, y]) => [P.x + x * s, P.y + y * s]);
  const lit = P.lit || [.3, -.95];
  const RP = PR.rock(pts, { lit, hi: .06, mid: .035, lo: .02, seed: P.seed || 3, th: -.6, rim: Math.max(3, 6 * s), facets: 14 });
  // ışık yanındaki sırtlardan içeri giren beyaz vuruşlar (sırtın güneşe bakan yanı)
  const side = lit[0] >= 0 ? 1 : -1, ridge = side > 0 ? pts.slice(11, 23) : pts.slice(0, 12).reverse();
  PR.cuts(ridge, [-.35 * side, .94], { len: [14 * s, 130 * s], gap: [36 * s, 110 * s], w: Math.max(4, 6 * s), seed: (P.seed || 3) + 4, clip: RP, bend: .3 * side });
  return { path: RP, top: [P.x, P.y] };
}
// bütün set: o: {sun: {x,y,r}, hz, tepe: {x,y,s}, aden: {x,y,w,s} | false, dark, soft, beams, fig (tepe) => {}, front: () => {}}
function cizNifates(t, o = {}) {
  const S = o.sun || { x: 1060, y: 430, r: 300 };
  nif_gok(S, o);
  if (o.mid0) o.mid0(S);
  nif_siralar({ hz: o.hz ?? 800, dark: o.dark });
  if (o.aden) nif_aden(o.aden, t);
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
function nif_rig(p) {
  return SF.rig({ x: p.x, y: p.y, h: p.h, facing: p.facing ?? 1, twist: p.twist ?? .4, lean: p.lean ?? 0, head: p.head ?? 0, shTilt: p.shTilt ?? -.04,
    armN: p.armN || [.12, .2], armF: p.armF || [-.1, .15], legN: p.legN || [.1, -.05], legF: p.legF || [-.08, -.03] });
}
function nif_kanat(J, p, mask) {
  const h = J.h, w = p.wings || {}, LIT = p.lit || [.3, -.95], t = p.t || 0;
  for (const [side, P] of [[-1, { span: (w.spanL ?? 8.6) * h, open: w.open ?? .55, lift: w.lift ?? .45, droop: w.droop ?? .5, rot: w.rotL ?? -.06, seed: 31, root: .1 }],
    [1, { span: (w.spanR ?? 7.8) * h, open: (w.open ?? .55) * .94, lift: (w.lift ?? .45) * .8, droop: (w.droop ?? .5) * 1.2, rot: w.rotR ?? .1, seed: 32, root: .12 }]]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    GR.frame(sh[0] - side * h * .25, sh[1] + h * .15, P.rot, side, 1);
    KN.feathered(Object.assign({ dark: .93, rim: mask ? 0 : .75, ruin: .55, t, lit: [LIT[0] * side, LIT[1]] }, P));
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
  PR.glow(X, Y - 6, 40, 520, 1, .55);
  PR.lake(Y, Y + 900, t, { tone: [.12, .02], crests: 10, p0: 9.5, refl: [{ x: X, w: 380, v: .95, len: 320, rows: 12 }, { x: X - 420, w: 140, v: .6, len: 160 }, { x: X + 430, w: 150, v: .6, len: 160 }] });
  PR.flameBank(X - 900, X + 900, Y + 2, 30, t, 1, { env: f => .35 + .65 * Math.pow(Math.sin(f * PI), 2), smoke: false });
  PR.flameBank(X - 560, X + 560, Y + 8, 190 * fh, t, 5, { n: 9, wr: .5, curl: .5, speed: .6, solidBelow: 900, strip: .3, frags: false, env: f => .35 + .65 * Math.pow(Math.sin(f * PI), 1.5) });
}
const NIF_MK = makeCanvas(DW, DH), NIF_mk = NIF_MK.getContext('2d', { willReadFrequently: true });
const NIF_MG = makeCanvas(DW, DH), NIF_mg = NIF_MG.getContext('2d', { willReadFrequently: true });
// kare çekirdekli en büyük/en küçük süzgeç (ayrık iki geçiş), yerinde
function nif_morf(A, w, h, r, mx) {
  if (r < 1) return A;
  const T = new Float32Array(A.length);
  for (let y = 0; y < h; y++) { const o = y * w; for (let x = 0; x < w; x++) { let m = mx ? 0 : 1; const a = Math.max(0, x - r), b = Math.min(w - 1, x + r); for (let k = a; k <= b; k++) { const v = A[o + k]; if (mx ? v > m : v < m) m = v; } T[o + x] = m; } }
  for (let x = 0; x < w; x++) for (let y = 0; y < h; y++) { let m = mx ? 0 : 1; const a = Math.max(0, y - r), b = Math.min(h - 1, y + r); for (let k = a; k <= b; k++) { const v = T[k * w + x]; if (mx ? v > m : v < m) m = v; } A[y * w + x] = m; }
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
  if (window.NIF_DBG == 1) A.fill(1);
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
  GR.frame(at[0] - F[0] * ks, at[1] - F[1] * ks, 0, 1, ks);
  if (o.draw) o.draw(t, kOpen);
  else if (o.full) cizGol(t, Object.assign({ fig: false, chains: false }, o.gol || {}));
  else nif_icGol(t, kOpen);
  GR.unframe();
  GR.restore();
  const T1 = tx.getImageData(R[0], R[1], R[2], R[3]), P1 = px.getImageData(R[0], R[1], R[2], R[3]);
  const a0 = T0.data, a1 = T1.data, p0 = P0.data, p1 = P1.data;
  for (let j = 0, m = a0.length; j < m; j += 4) {
    const a = MD[j + 3] / 255; if (a <= 0) continue;
    a0[j] = a0[j] + (a1[j] - a0[j]) * a; a0[j + 1] = a0[j]; a0[j + 2] = a0[j];
    if (a > .5) { p0[j] = p1[j]; p0[j + 1] = p1[j + 1]; p0[j + 2] = p1[j + 2]; }
  }
  tx.putImageData(T0, R[0], R[1]); px.putImageData(P0, R[0], R[1]);
}

// ═════════ P001 (A01): kanca ═════════
// A02 (cennet grubu) aynı duruş ve aynı kadrajla açılır: bu yerleşim bağlayıcıdır (kalça (860, 560), h 96, facing 1; son kamera {960, 540, 1}).
const NIF_A01 = { x: 860, y: 560, h: 96, facing: 1, twist: .35, lean: -.02, head: .22, shTilt: -.05, armN: [.2, .25], armF: [-.16, .2], legN: [.2, -.06], legF: [-.17, -.02] };
const NIF_A01_KANAT = { open: .55, lift: .5, droop: .45, spanL: 8.6, spanR: 7.8, rotL: -.06, rotR: .1 };
function nif_a01(t, o = {}) {
  return cizNifates(t, {
    sun: { x: 1010, y: 400, r: 330 }, hz: 900, tepe: { x: 880, y: 940, s: 1, seed: 3 }, t,
    clouds: [{ x: 120, y: 120, w: 900, h: 260, seed: 12 }, { x: 1900, y: 40, w: 900, h: 230, seed: 19 }, { x: 1640, y: 230, w: 900, h: 220, seed: 23, n: 3 }],
    fig: () => nif_seytan(Object.assign({}, NIF_A01, { t, lum: .12, wings: NIF_A01_KANAT, lit: [.4, -.92], ic: o.ic === false ? null : Object.assign({ k: 1, wings: true, margin: 6, neck: false }, o.ic) })) });
}
plan('P001', (ctx, st) => {
  const t = st.t, tC = Wd('A01', 'cehennem');
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => nif_a01(t, { ic: { k: lerp(.55, 1, E.io2(nif_u(t, tC - 1, tC + 1.5))) } }), [.5, 0, 1]);
}, { tr: { type: 'cut' },
  over: (ctx, st) => { const t0 = Wd('A01', 'cehennemim') - st.at; quote(ctx, '“Ben cehennemim.”', 1520, 170, st.lt, { t0, px: 76 }); } });
