// nif grubu (NIF: Nifates Dağı): set, figür, "iç cehennem" motifi ve planlar (bkz. lib/acts/KILAVUZ.md)
// Değer planı (geçiş sahnesi, koyu piksel %50–60): dev güneş diski temiz kâğıt (taramasız çekirdek); gök açık ama güneşe göre
// eş merkezli taralı, kenarlara doğru koyulaşır; birkaç ışın kaması içinde çizgi ışın doğrultusunda (cehennemin yatay taramasından ayrışır).
// Dağ ve figür koyu kütle: biçimi ışık yanındaki kenar ışığı ve kütleye giren beyaz vuruşlar verir. Uzakta Aden: küçük, açık.
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const nif_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));

// ═════════ set ═════════
// gök ve güneş (yönetmen notu 1): güneş temiz kâğıt disk + çevresinde tek ince mürekkep çizgisi; çevresi geniş temiz kâğıt;
// dışa doğru seyrek ışınsal tarama (GR 'ray', üslup 10: sabit kalınlıkta çizgi, merkeze yakın kendiliğinden kaybolur). Eş merkezli halka yok.
// S: {x, y, r}; o: {dark (0..1 alacakaranlık), soft (0..1 ışık yumuşar: kamalar söner), beams (en çok iki kama: [açı, yarı genişlik, boy]),
//   clouds (bulut listesi: {x, y, w, h, seed, n}): güneşe bakan kenarı ışıklı koyu bulut kütleleri (yazıların zemini de bunlardır), ring (yalnız çerçeve: true ya da kalınlık; varsayılan yok), tight (false: eski geniş kâğıt çevre)}
function nif_gok(S, o = {}) {
  const { tx, px, tone } = GR, dk = o.dark || 0, sf = o.soft || 0, r = S.r;
  const lo = lerp(.66, .6, dk);   // en koyu gök tonu (.6'nın altına inmez)
  const g = tx.createRadialGradient(S.x, S.y, r, S.x, S.y, r * 4.6);
  if (o.tight !== false) { g.addColorStop(0, tone(.8)); g.addColorStop(.1, tone(.82)); } else { g.addColorStop(0, tone(1)); g.addColorStop(.12, tone(1)); }
  g.addColorStop(.3, tone(lerp(.9, .86, dk))); g.addColorStop(.6, tone(lerp(.76, .7, dk))); g.addColorStop(1, tone(lo));
  tx.fillStyle = g; tx.fillRect(-2000, -2000, W + 4000, H + 4000);
  px.fillStyle = GR.hatch({ type: 'ray', cx: S.x, cy: S.y, n: 96, id: 10, w: 3 }); px.fillRect(-2000, -2000, W + 4000, H + 4000);
  // ışın kamaları (en çok iki): güneşten çıkan, sivrilen temiz kâğıt kamalar
  const B = (o.beams ?? [[-2.45, .05, 1500], [-.55, .045, 1400]]).slice(0, 2);
  const bv = (1 - sf) * (1 - dk * .7);
  if (bv > .02) {
    tx.save(); tx.globalCompositeOperation = 'lighten';
    for (const [a, w, L] of B) {
      const n = 10, A = [], C = [];
      for (let i = 0; i <= n; i++) { const u = i / n, rr = r * .96 + L * u, ww = w * Math.pow(Math.sin(PI * (.08 + .84 * u)), .7) * (1 - .4 * u); A.push([S.x + Math.cos(a - ww) * rr, S.y + Math.sin(a - ww) * rr]); C.push([S.x + Math.cos(a + ww) * rr, S.y + Math.sin(a + ww) * rr]); }
      const P = new Path2D(); poly(P, [...A, ...C.reverse()], true);
      const gg = tx.createRadialGradient(S.x, S.y, r, S.x, S.y, r + L);
      gg.addColorStop(0, tone(1)); gg.addColorStop(.6, tone(lerp(.9, 1, bv))); gg.addColorStop(1, tone(lo));
      tx.fillStyle = gg; tx.fill(P);
    }
    tx.restore();
  }
  const D = new Path2D(); D.arc(S.x, S.y, r, 0, TAU);
  GR.fill(D, tone(1), { th: 0, id: 10 });
  if (o.ring) { const c = GR.ox; c.save(); c.strokeStyle = GR.inkCol; c.lineWidth = o.ring === true ? 3.5 : o.ring; c.stroke(D); c.restore(); }   // yalnız çerçeve olarak (G05): kesintisiz, keskin üst katman
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
  GR.fill(V, tone(.93), { th: 0, id: 10 });
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
    KN.feathered(Object.assign({ dark: .93, rim: mask ? 0 : .75, ruin: w.ruin ?? .15, t, lit: [LIT[0] * sd, LIT[1]] }, P));
    GR.unframe();
  }
}
function nif_sfdraw(J, p, mask) {   // mask: maske geçişi (beyaz vuruş ve kenar ışığı yok: kütle delinmez)
  return SF.draw(J, { lum: mask ? 0 : p.lum ?? .2, lit: p.lit || [.3, -.95], t: p.t || 0, legs: p.legs ?? true, skirt: true, eye: mask ? 0 : p.eye ?? 0, wind: p.wind ?? .5,
    cloak: p.cloak ?? (p.wings && p.wings.prof ? 1.7 : 1.3), halo: mask ? 0 : p.halo ?? 3.5, lines: mask ? 0 : 2, rim: mask ? .001 : undefined, seed: p.seed || 3 });
}
function nif_seytan(p) {
  const J = nif_rig(p);
  if (p.wings !== false && !(p.ic && p.ic.wings)) nif_kanat(J, p);
  if (p.mid) p.mid(J);
  if (p.ic) nif_icCehennem(J, m => { if (p.ic.wings && p.wings !== false) nif_kanat(J, p, m); nif_sfdraw(J, p, m); }, Object.assign({ t: p.t }, p.ic));
  else nif_sfdraw(J, p);
  return J;
}
// yatay sıkıştırma (raster): fn'nin çizdiği her şey, x = ax ekseni çevresinde sx katına iner. Kutu: dünya [x0, y0, x1, y1].
// Önce arka plan saklanır, fn çizilir, değişen pikseller (figür) ayrılır, arka plan geri konur ve figür sıkıştırılarak basılır.
const NIF_SQ = makeCanvas(8, 8), NIF_sq = NIF_SQ.getContext('2d', { willReadFrequently: true });
function nif_sikistir(ax, sx, fn, box) {
  if (sx > .999) { fn(); return; }
  const M = GR.tx.getTransform(), p0 = M.transformPoint(new DOMPoint(box[0], box[1])), p1 = M.transformPoint(new DOMPoint(box[2], box[3]));
  const x0 = Math.max(0, Math.floor(p0.x)), y0 = Math.max(0, Math.floor(p0.y)), w = Math.min(DW, Math.ceil(p1.x)) - x0, h = Math.min(DH, Math.ceil(p1.y)) - y0;
  if (w < 2 || h < 2) { fn(); return; }
  const L = [GR.tx, GR.px, GR.ox], B = L.map(c => c.getImageData(x0, y0, w, h));
  fn();
  const A = L.map(c => c.getImageData(x0, y0, w, h));
  const cx = M.transformPoint(new DOMPoint(ax, 0)).x - x0;
  if (NIF_SQ.width < w || NIF_SQ.height < h) { NIF_SQ.width = Math.max(w, NIF_SQ.width); NIF_SQ.height = Math.max(h, NIF_SQ.height); }
  const ch = new Uint8Array(w * h), bt = B[0].data, at = A[0].data, bp = B[1].data, ap = A[1].data, ba = B[2].data, aa = A[2].data;
  for (let i = 0, j = 0; i < w * h; i++, j += 4) ch[i] = (bt[j] !== at[j] || bp[j] !== ap[j] || bp[j + 1] !== ap[j + 1] || ba[j + 3] !== aa[j + 3]) ? 1 : 0;
  L.forEach((c, k) => {
    const out = B[k], od = out.data, src = A[k].data;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {   // en yakın komşu: tarama kimliği baytları bozulmaz
      const xs = Math.round(cx + (x - cx) / sx); if (xs < 0 || xs >= w) continue;
      const i = y * w + xs; if (!ch[i]) continue;
      const j = (y * w + x) * 4, q = i * 4; od[j] = src[q]; od[j + 1] = src[q + 1]; od[j + 2] = src[q + 2]; od[j + 3] = src[q + 3];
    }
    c.putImageData(out, x0, y0);
  });
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
// iç cehennemin içeriği (yönetmen notu 2–3): siyah iç + alttan yükselen kâğıt beyazı alev dilleri ve birkaç kıvılcım.
// Ufuk, parıltı bandı ve yatay tarama yok. Dünya koordinatında çizilir: taban (bx, by), genişlik bw, boy bh; k: 0..1 boy (pencere açıklığı).
function nif_icAlev(t, bx, by, bw, bh, k = 1) {
  const { tone } = GR, fh = lerp(.3, 1, E.io2(clamp(k)));
  const V = new Path2D(); V.rect(bx - bw * 4, by - bh * 6, bw * 8, bh * 8); GR.fill(V, tone(.02), { th: 0, id: 0 });
  const sc = bw / 400;
  PR.flameBank(bx - bw * .5, bx + bw * .5, by, bh * fh, t, 41, { n: 5, wr: .24, curl: .45, speed: .3, sway: .5, solidBelow: 1e5, strokeAbove: 60 * sc, strip: .06, frags: false, smoke: false,
    env: f => .35 + .65 * Math.pow(Math.sin(f * PI), 1.2) });
  // kıvılcımlar: yavaşça yükselen, sönen küçük beyaz kıymıklar (döngü sınırında boy sıfır: sıçrama yok)
  const r = rng(9);
  for (let i = 0; i < 9; i++) {
    const x0 = bx + (r() - .5) * bw * 1.1, sp = .08 + r() * .06, ph = r(), c = (t * sp + ph) % 1, z = Math.sin(PI * c) * (3 + r() * 3) * Math.max(.6, sc) * fh;
    if (z < .6) continue;
    const x = x0 + Math.sin(c * 5 + i) * 14 * sc, y = by - bh * fh * (.55 + c * .9);
    const P = new Path2D(); P.ellipse(x, y, z * .6, z * 1.6, Math.sin(i) * .4, 0, TAU); GR.fill(P, tone(1), { th: 0, id: 0 });
  }
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
  if (o.full) {
    px.save(); px.setTransform(1, 0, 0, 1, 0, 0); px.fillStyle = GR.hatch({ th: 0, id: 1 }); px.fillRect(R[0], R[1], R[2], R[3]); px.restore();
    GR.frame(at[0] - F[0] * ks, at[1] - F[1] * ks, 0, 1, ks);
    cizGol(t, Object.assign({ fig: false, chains: false }, o.gol || {}));
  } else if (o.draw) { GR.frame(at[0] - F[0] * ks, at[1] - F[1] * ks, 0, 1, ks); o.draw(t, kOpen); }
  else {   // varsayılan: siyah iç + alevler; taban kalçanın biraz altında, alevler göğse ve kanatların içine yükselir
    const fl = o.alev || {};
    if (g > 1.001) GR.frame(G.c[0] * (1 - g), G.c[1] * (1 - g), 0, 1, g);   // içerik maskeyle birlikte büyür: kamera siluetin içine girer
    nif_icAlev(t, fl.x ?? J.hip[0], fl.y ?? (J.hip[1] + (fl.dy ?? .6) * h), (fl.w ?? 3.2) * h, (fl.h ?? 3.4) * h, kOpen);
  }
  GR.unframe();
  GR.restore();
  const T1 = tx.getImageData(R[0], R[1], R[2], R[3]), P1 = px.getImageData(R[0], R[1], R[2], R[3]);
  const a0 = T0.data, a1 = T1.data, p0 = P0.data, p1 = P1.data;
  for (let j = 0, m = a0.length; j < m; j += 4) {
    let a = MD[j + 3] / 255; if (a <= 0) continue; a = clamp((a - .5) * (g > 1.001 ? 16 / g : 16) + .5);
    a0[j] = a0[j] + (a1[j] - a0[j]) * a; a0[j + 1] = a0[j]; a0[j + 2] = a0[j];
    if (a > .5) { p0[j] = p1[j]; p0[j + 1] = p1[j + 1]; p0[j + 2] = p1[j + 2]; }
  }
  tx.putImageData(T0, R[0], R[1]); px.putImageData(P0, R[0], R[1]);
}

// ═════════ Kanca çifti: P001 (A01) ve P002 (A02) ═════════
// İki plan AYNI dış hattı kullanır (nif_kancaYol: aynı işlev, aynı konum, aynı ölçek); değerler terstir:
//  A01: güneşe karşı düz siyah figür, göğsünde tek kâğıt beyazı alev (iç cehennem); 'cehennemim' kelimesinde alev büyür.
//  A02: düz siyah zeminde düz kâğıt beyazı figür; ışığın kaynağı kendisi: dış hattından siyaha giren, sivrilen, boyu düzensiz beyaz ışın vuruşları;
//       kesmeden sonraki ~1 sn'de yarı kapalı kanatlar açılır; cümle sonunda ışın vuruşları kısalıp incelerek söner.
// Figür el yapımı tek siluettir (SF/KN değil): telefon boyunda baş, omuz çizgisi, ayak bileğine inen pelerin ve iki kanat (üstte kemer, uçlar aşağı sivri)
// ayrı ayrı okunsun diye. Yüz, göğüs ayrıntısı, hale yok.
const NIF_KANCA = { x: 860, y: 905, U: 640 };   // ayakların ortası (zirve) ve figür boyu (kanat kemerinin tepesinden ayağa ~ U)
// parçalar ayrı yollar (kanat, pelerin, baş) + birleşik yol. op: 0 yarı kapalı … 1 açık
function nif_kancaYol(op = 0, K = NIF_KANCA) {
  const { x, y, U } = K, P = (px, py) => [x + px * U, y + py * U];
  const o = clamp(op), L = (a, b) => lerp(a, b, E.io2(o));
  const wings = [];
  // kanat noktaları (sağ kanat; sol aynası): yarı kapalı ve açık; aynı sayıda nokta, '!' sivri köşe (tüy ucu)
  const K0 = [[.05, -.74], [.085, -.95], [.165, -1.08], [.265, -1.02], [.3, -.86], [.29, -.6], [.27, -.34],
    [.255, -.02, 1], [.24, -.12], [.228, -.05, 1], [.212, -.15], [.198, -.09, 1], [.183, -.19], [.168, -.13, 1], [.153, -.24], [.14, -.2, 1], [.125, -.36], [.1, -.55], [.08, -.67]];
  const K1 = K0;   // (A02 artık KN.feathered kullanır; op yalnız 0)
  for (const sd of [-1, 1]) {
    let pts = K0.map((k, i) => { const [ax, ay, sh] = k, [bx, by] = K1[i]; return Object.assign(P(sd * L(ax, bx), L(ay, by)), { sh }); });
    // bütün parçalar aynı dönüş yönünde (saat yönünün tersi): birleşik yolda örtüşen parçalar birbirini silmesin (nonzero)
    let ar = 0; for (let i = 0; i < pts.length; i++) { const a = pts[i], b = pts[(i + 1) % pts.length]; ar += a[0] * b[1] - b[0] * a[1]; }
    const ord = ar > 0 ? pts.slice().reverse() : pts;
    const W = new Path2D(); W.moveTo(...ord[0]);
    for (let i = 1; i < ord.length; i++) {
      const a = ord[i - 1], b = ord[i];
      if (b.sh || a.sh) W.lineTo(b[0], b[1]);             // tüy uçları sivri
      else W.quadraticCurveTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2);
    }
    W.closePath();
    wings.push({ path: W, sd, pts });
  }
  // pelerin: omuzlardan ayak bileğine genişleyen, eteği hafif dalgalı; altında iki küçük ayak
  const C = new Path2D();
  C.moveTo(...P(-.035, -.79));
  C.quadraticCurveTo(...P(-.1, -.79), ...P(-.115, -.74));                     // sol omuz
  C.quadraticCurveTo(...P(-.15, -.45), ...P(-.19, -.06));
  C.quadraticCurveTo(...P(-.14, -.01), ...P(-.09, -.04)); C.quadraticCurveTo(...P(-.04, 0), ...P(0, -.035));
  C.quadraticCurveTo(...P(.05, 0), ...P(.1, -.03)); C.quadraticCurveTo(...P(.15, -.005), ...P(.19, -.06));
  C.quadraticCurveTo(...P(.15, -.45), ...P(.115, -.74));
  C.quadraticCurveTo(...P(.1, -.79), ...P(.035, -.79)); C.closePath();
  for (const sd of [-1, 1]) { const f = P(sd * .05, -.012); C.moveTo(f[0] + .032 * U, f[1]); C.ellipse(f[0], f[1], .032 * U, .014 * U, 0, 0, TAU, true); }   // ayak uçları
  // baş: hafif yukarı kalkık (çene öne), kısa boyun
  const Hd = new Path2D(); { const h0 = P(.004, -.855); Hd.moveTo(h0[0] + .043 * U, h0[1]); Hd.ellipse(h0[0], h0[1], .043 * U, .055 * U, -.08, 0, TAU, true); }
  { const a = P(-.024, -.82), b = P(.024, -.78); Hd.moveTo(a[0], a[1]); Hd.lineTo(a[0], b[1]); Hd.lineTo(b[0], b[1]); Hd.lineTo(b[0], a[1]); Hd.closePath(); }   // boyun (saat yönünün tersi)
  const HE = new Path2D(); { const h0 = P(.004, -.855); HE.ellipse(h0[0], h0[1], .043 * U, .055 * U, -.08, 0, TAU); }
  const all = new Path2D(); for (const w of wings) all.addPath(w.path); all.addPath(C); all.addPath(Hd);
  return { wings, cloak: C, head: Hd, headE: HE, all, P };
}
// kanca kanatları (KN.feathered): kök kancaYol'un omuz noktası (x ± .05U, y − .74U); iki yanda ayna.
// q: {span, open, lift, droop, rot, dark, rim, lit, t}
function nif_kancaKanat(q, K = NIF_KANCA) {
  const { x, y, U } = K;
  for (const sd of [-1, 1]) {
    const s7 = U * .001293; GR.frame(x + sd * 80 * s7, y + (430 - 975) * s7, (q.rot ?? 0) * sd, sd, 1);   // kök: v7 figürünün omuz arkası
    KN.feathered({ span: q.span ?? .95 * U, open: q.open, lift: q.lift, droop: q.droop, dark: q.dark, rim: q.rim ?? .75, ruin: 0, root: .1,
      lit: [(q.lit || [0, -1])[0] * sd, (q.lit || [0, -1])[1]], t: q.t || 0, seed: sd < 0 ? 31 : 32 });
    GR.unframe();
  }
}
// sivri uçlu dolgu vuruş (tx'e): pts dünya noktaları, w en kalın yer, v ton
function nif_vurus(pts, w, v) {
  const n = 14, S = [], A = [], B = [], m = pts.length, c = GR.tx;
  const cr = (p0, p1, p2, p3, t) => { const t2 = t * t, t3 = t2 * t; return [0, 1].map(j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)); };
  for (let i = 0; i <= n; i++) { const u = i / n * (m - 1), s = Math.min(m - 2, Math.floor(u)); S.push(cr(pts[Math.max(0, s - 1)], pts[s], pts[s + 1], pts[Math.min(m - 1, s + 2)], u - s)); }
  for (let i = 0; i <= n; i++) {
    const a = S[Math.max(0, i - 1)], b = S[Math.min(n, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
    const ww = Math.max(1.3, w * .5 * Math.pow(1 - i / n, .9) * Math.min(1, .45 + i / n * 4));
    A.push([S[i][0] - dy / L * ww, S[i][1] + dx / L * ww]); B.push([S[i][0] + dy / L * ww, S[i][1] - dx / L * ww]);
  }
  c.fillStyle = GR.tone(v); c.beginPath(); poly(c, [...A, ...B.reverse()], true); c.fill();
}
// kanat içi tüy vuruşları: kemerden aşağı akan birkaç uzun, sivrilen çizgi (A01'de kâğıt rengi, A02'de mürekkep)
function nif_kanatVurus(F, v, w = 7, k = 1) {
  for (const W of F.wings) {
    const p = W.pts, sd = W.sd;
    GR.tx.save(); GR.tx.clip(W.path);
    // kemerin altından üç tüy ucuna doğru akan uzun vuruşlar
    for (const [ai, ti, f] of [[4, 7, .8], [3, 9, .76], [2, 11, .7]]) {
      const a = [lerp(p[ai][0], p[1][0], .25), p[ai][1] + 30 * k], e = [lerp(a[0], p[ti][0], f), lerp(a[1], p[ti][1], f)];
      nif_vurus([a, [lerp(a[0], e[0], .5) + sd * 10 * k, lerp(a[1], e[1], .5)], e], Math.max(4, w * k), v);
    }
    GR.tx.restore();
  }
}
// göğüs alevi (kao_gogusAlev'in akrabası): sivri uçlu kâğıt beyazı dil + iki küçük yan dil; taban (x, y), boy L, yarı genişlik wd
function nif_gogusAlev(x, y, L, wd, t) {
  const fo = { speed: .45, sway: .8, curl: .8, solidBelow: 1e5, strokeAbove: 70, frags: false, inner: .5 };
  PR.flame(x - wd * 1.3, y + wd * .3, L * .5, wd * 1.3, t + 2, 23, Object.assign({ lean: -.25 }, fo));
  PR.flame(x + wd * 1.3, y + wd * .3, L * .56, wd * 1.3, t + 5, 24, Object.assign({ lean: .25 }, fo));
  PR.flame(x, y + wd * .5, L, wd * 2.2, t, 21, fo);
}
// A01: güneşe karşı karanlık figür
// ═════════ kanca figürü v7 (kapak/kapak.js kpk_siluet7'nin film uyarlaması; kapak ile açılış aynı figür) ═════════
// Kapaktaki mutlak ölçüler (eksen 0, ayak hizası y 975) K'ya taşınır: dünya = (K.x + dx·s, K.y + (y − 975)·s), s = U·.001293 (U 640 → .827).
// Parçalar: iki kanat (5 ayrık sivri birincil tüy, boyları farklı), kambur omuzlu pelerin (etek zirveye değer, iki ayak ucu), boyun tabanı
// çevresinde eğik baş + kıvırcık saç (10 bukle). Sabit kontur yok: kenar ışığı yalnız ışığa bakan kenarlarda sivrilen vuruşlarla.
const NIF_EGIM = -.38;   // açılış figürünün baş eğimi (öne ve yana; göğsündeki aleve eğik)
function nif_yol(pts, P = new Path2D()) {   // kapalı yumuşak yol; [x, y, 1] sivri köşe
  const n = pts.length, T = pts.map((p, i) => { if (p[2]) return [0, 0]; const a = pts[(i - 1 + n) % n], b = pts[(i + 1) % n]; return [(b[0] - a[0]) / 6, (b[1] - a[1]) / 6]; });
  P.moveTo(pts[0][0], pts[0][1]);
  for (let i = 0; i < n; i++) { const a = pts[i], b = pts[(i + 1) % n], ta = T[i], tb = T[(i + 1) % n]; P.bezierCurveTo(a[0] + ta[0], a[1] + ta[1], b[0] - tb[0], b[1] - tb[1], b[0], b[1]); }
  P.closePath(); return P;
}
// iki ucu sivrilen dolgu vuruş (en kalın yer 'tepe' oranında)
function nif_vurus2(pts, w, v, tepe = .4, uc = .25) {
  const n = 18, S = [], A = [], B = [], m = pts.length, c = GR.tx;
  const cr = (p0, p1, p2, p3, t) => { const t2 = t * t, t3 = t2 * t; return [0, 1].map(j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)); };
  for (let i = 0; i <= n; i++) { const u = i / n * (m - 1), s = Math.min(m - 2, Math.floor(u)); S.push(cr(pts[Math.max(0, s - 1)], pts[s], pts[s + 1], pts[Math.min(m - 1, s + 2)], u - s)); }
  for (let i = 0; i <= n; i++) {
    const a = S[Math.max(0, i - 1)], b = S[Math.min(n, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, u = i / n;
    const prof = u < tepe ? lerp(uc, 1, E.out2(u / tepe)) : lerp(1, uc * .5, E.in2((u - tepe) / (1 - tepe)));
    const ww = Math.max(.9, w * .5 * prof);
    A.push([S[i][0] - dy / L * ww, S[i][1] + dx / L * ww]); B.push([S[i][0] + dy / L * ww, S[i][1] - dx / L * ww]);
  }
  c.fillStyle = GR.tone(v); c.beginPath(); poly(c, [...A, ...B.reverse()], true); c.fill();
}
// yollar (çizimsiz): {M (kapak → dünya), s, wings, cloak, head (baş + boyun + bukleler), curls, all, fb (alev tabanı), pv}
function nif_yol7(K = NIF_KANCA, th = NIF_EGIM) {
  const s = K.U * .001293, M = (dx, y, sh) => { const q = [K.x + dx * s, K.y + (y - 975) * s]; if (sh) q.push(1); return q; };
  const wings = [-1, 1].map(sd => nif_yol([[70, 412], [92, 300], [118, 196], [152, 138], [206, 140], [256, 208], [286, 318], [292, 460], [284, 600], [276, 720],
    [304, 958, 1], [250, 798], [258, 926, 1], [214, 808], [212, 896, 1], [180, 812], [170, 868, 1], [150, 802], [132, 834, 1],
    [116, 760], [108, 600], [94, 486]].map(([x, y, sh]) => M(sd * x, y, sh))));
  const cloak = nif_yol([[-26, 392], [-72, 408], [-112, 444], [-130, 560], [-150, 760], [-168, 930], [-176, 978], [-110, 972], [-40, 984], [40, 984], [110, 972],
    [176, 978], [166, 930], [146, 760], [126, 560], [108, 432], [70, 402], [26, 392]].map(([x, y]) => M(x, y)));
  for (const sd of [-1, 1]) { const f = M(sd * 44, 986); cloak.moveTo(f[0] + 34 * s, f[1]); cloak.ellipse(f[0], f[1], 34 * s, 13 * s, 0, 0, TAU); }   // ayak uçları (etek zirveye değer)
  const pv = M(0, 398), rot = (x, y) => [pv[0] + (x * Math.cos(th) - y * Math.sin(th)) * s, pv[1] + (x * Math.sin(th) + y * Math.cos(th) + 16) * s];
  const head = new Path2D(); poly(head, [rot(-19, -18), rot(19, -18), M(26, 400), M(-26, 400)], true);
  const hc = rot(0, -72); head.moveTo(hc[0] + 40 * s, hc[1]); head.ellipse(hc[0], hc[1], 40 * s, 50 * s, th, 0, TAU);
  const r = rng(71), curls = [];
  for (let i = 0; i <= 9; i++) { const a = PI * (1.02 + .98 * i / 9), rr = (15 + r() * 6) * s, d = 41 + r() * 4, q = rot(Math.cos(a) * d, -72 + Math.sin(a) * d * 1.12 - 4); curls.push([q[0], q[1], rr]); head.moveTo(q[0] + rr, q[1]); head.arc(q[0], q[1], rr, 0, TAU); }
  const all = new Path2D(); for (const w of wings) all.addPath(w); all.addPath(cloak); all.addPath(head);
  return { M, s, wings, cloak, head, curls, all, fb: M(-8, 712), pv, th };
}
// çizim. a: alev büyüklüğü (0 sakin … 1 'cehennemim'); o: {tilt, beyaz (A02: kâğıt figür, mürekkep vuruş), kanat (false: kanat çizilmez), alev (false)}
function nif_siluet7(t, a, K = NIF_KANCA, o = {}) {
  const F = nif_yol7(K, o.tilt ?? NIF_EGIM), { M, s } = F, tx = GR.tx, B = !!o.beyaz;
  const FILL = GR.tone(B ? 1 : .02), LIT = B ? .05 : 1, w = v => Math.max(3, v * s / .827);
  if (o.kanat !== false) for (const [k, W] of F.wings.entries()) {
    const sd = k ? 1 : -1, X = (dx, y) => M(sd * dx, y);
    GR.fill(W, FILL, { th: 0, id: 0 });
    tx.save(); tx.clip(W);
    for (const [p, q, r, ww] of [[[150, 205], [168, 520], [134, 800], 7], [[196, 190], [222, 520], [170, 845], 8], [[238, 245], [258, 560], [212, 870], 8],
      [[268, 330], [282, 600], [256, 905], 7], [[284, 420], [292, 640], [298, 930], 6]]) nif_vurus2([X(...p), X(...q), X(...r)], w(ww), LIT, .3, .3);
    nif_vurus2([X(84, 420), X(96, 300), X(122, 196), X(160, 140), X(210, 146)], w(9), LIT, .45, .2);   // iç-üst kenar ışığı
    tx.restore();
  }
  GR.fill(F.cloak, FILL, { th: 0, id: 0 });
  tx.save(); tx.clip(F.cloak);
  if (!B) {
    nif_vurus2([M(-34, 398), M(-76, 414), M(-108, 446), M(-124, 520)], w(7), 1, .35, .2);     // omuz üstü kenar ışığı (incelip kalınlaşır)
    nif_vurus2([M(34, 398), M(74, 408), M(104, 436), M(120, 500)], w(6), 1, .35, .2);
    nif_vurus2([M(-126, 540), M(-138, 650), M(-150, 780)], w(6), 1, .3, .2);
    nif_vurus2([M(122, 520), M(134, 640), M(146, 760)], w(5), 1, .3, .2);
  }
  for (const [x0, y0, x1, y1, ww] of [[-62, 770, -80, 975, 7], [-14, 810, -22, 980, 6], [38, 780, 52, 975, 7], [92, 840, 110, 970, 5]])
    nif_vurus2([M(x0, y0), M(lerp(x0, x1, .5) + 6, lerp(y0, y1, .5)), M(x1, y1)], w(ww), LIT, .7, .15);   // pelerin kıvrımları
  tx.restore();
  GR.fill(F.head, FILL, { th: 0, id: 0 });
  if (!B) for (const i of [2, 4, 6, 8]) {   // saçta ışık: birkaç buklenin tepesinde kısa hilal
    const [x, y, rr] = F.curls[i], a0 = -PI / 2 + F.th, q = []; for (let k = 0; k <= 6; k++) { const aa = a0 - .9 + 1.8 * k / 6; q.push([x + Math.cos(aa) * rr * .72, y + Math.sin(aa) * rr * .72]); }
    nif_vurus2(q, Math.max(3, 4 * s / .827), 1, .5, .2);
  }
  if (o.alev !== false && !B) nif_alev7(t, F, a);
  return F;
}
// göğüs alevi (kapak dili): boyları farklı üç dil (orta en uzun), taban düz kesilmez, taramayla karaya erir; yan pençe dili yok
function nif_alev7(t, F, a = 0, kx = 1) {
  const { tx } = GR, s = F.s, fb = F.fb, k = lerp(.8, 1.02, clamp(a, 0, 1.6)) * kx, sw = q => Math.sin(t * 1.1 + q) * 6 * s;   // çok yavaş salınım
  const dil = (bx, by, L, w, ln) => { const P = new Path2D(); P.moveTo(bx, by);
    P.bezierCurveTo(bx - w * 1.15, by - L * .1, bx - w * 1.1, by - L * .52, bx - w * .3 + ln * .45, by - L * .78);
    P.quadraticCurveTo(bx - w * .05 + ln * .85, by - L * .92, bx + ln, by - L);
    P.quadraticCurveTo(bx + w * .4 + ln * .9, by - L * .86, bx + w * .45 + ln * .5, by - L * .68);
    P.bezierCurveTo(bx + w * 1.15, by - L * .45, bx + w * 1.05, by - L * .1, bx, by); P.closePath(); return P; };
  const D = [[-34, -4, 146, 30, -26, 1], [32, -2, 110, 26, 22, 2], [0, 6, 251, 38, 14, 3]].map(([dx, dy, L, w, ln, q]) => [fb[0] + dx * s * k, fb[1] + dy * s, L * s * k, w * s * k, ln * s * k + sw(q)]);
  tx.save(); tx.clip(F.cloak);
  const Lm = 251 * s * k, tg = tx.createLinearGradient(0, fb[1] - Lm * .42, 0, fb[1] - 4 * s); tg.addColorStop(0, GR.tone(1)); tg.addColorStop(.55, GR.tone(.55)); tg.addColorStop(1, GR.tone(.02));
  for (const [bx, by, L, w, ln] of D) {
    GR.fill(dil(bx, by, L, w, ln), tg, { th: PI / 2 + ln * .004 / s, id: 3 });
    nif_vurus2([[bx - w * .45, by - L * .14], [bx - w * .5 + ln * .3, by - L * .42], [bx - w * .15 + ln * .7, by - L * .74]], Math.max(3, w * .2), .04, .35, .2);
    if (L > 200 * s) nif_vurus2([[bx + w * .4, by - L * .2], [bx + w * .32 + ln * .5, by - L * .5], [bx + w * .15 + ln * .8, by - L * .76]], Math.max(3, 5 * s), .04, .4, .2);
  }
  tx.restore();
}
// ═════════ baş-omuz yakın planı: güneşe karşı profil silueti (yüz ayrıntısı yok: dış çizgi + kenar ışığı) ═════════
// Kanca figürünün yakın hâli: kıvırcık saç (bukleler), kısa boyun, kambur omuz, pelerin; omzun arkasında kanadın kemeri yükselir.
// o: {f (bakış: 1 sağa, −1 sola), nx, ny (boyun tabanı, dünya), h (baş boyu px; 450 ≈ kare yüksekliğinin %45'i), bow (baş eğimi: + öne/aşağı, radyan),
//     drop (omuz çöküşü, h biriminde), wing (0..1 kanat kemerinin yüksekliği), sun ({x,y,r}: kenar ışığı bu çevrede)}
function nif_yakinSiluet(t, o) {
  const { tx } = GR, f = o.f ?? 1, h = o.h ?? 450, nx = o.nx, ny = o.ny, bow = o.bow ?? 0, dr = (o.drop ?? 0) * h;
  const R = (x, y, a) => { const c = Math.cos(a), s2 = Math.sin(a); return [x * c - y * s2, x * s2 + y * c]; };
  // baş: boyun tabanı çevresinde döner (f yönünde öne eğilme)
  const hb = (x, y) => { const q = R(x * f * h, y * h, bow * f); return [nx + q[0], ny - dr + q[1]]; };
  const hc = [.1, -.66];   // baş merkezi (boyun tabanına göre, h biriminde)
  const HEAD = [[-.45, -.04], [-.43, -.3], [-.26, -.5], [.02, -.56], [.24, -.47], [.34, -.32], [.37, -.17], [.385, -.1], [.4, -.05], [.475, .1], [.45, .145], [.39, .165],
    [.405, .215], [.39, .245], [.405, .28], [.375, .33], [.395, .41], [.34, .5], [.18, .52], [.02, .44], [-.14, .44], [-.32, .36], [-.44, .2]];
  const Hd = new Path2D(); spline(Hd, HEAD.map(([x, y]) => hb(hc[0] + x * .95, hc[1] + y * .95)), true, .55);
  const Hc = new Path2D(); { const q = hb(hc[0] - .08, hc[1] - .03); Hc.moveTo(q[0] + .36 * h, q[1]); Hc.arc(q[0], q[1], .36 * h, 0, TAU); }   // saç kütlesi (bukle araları dolu; ayrı yol: zıt dönüşle delik açmasın)
  const r = rng(73), curls = [];
  for (let i = 0; i <= 9; i++) { const a = PI * (.95 + .7 * i / 9), d = .36, q = hb(hc[0] - .08 + Math.cos(a) * d * .9, hc[1] - .02 + Math.sin(a) * d * 1.0); curls.push([q[0], q[1], (.095 + r() * .025) * h]); }
  for (const [x, y, rr] of curls) { Hc.moveTo(x + rr, y); Hc.arc(x, y, rr, 0, TAU); }
  // boyun + omuz + pelerin (kambur; ön omuz öne düşük)
  const B = (x, y) => [nx + x * f * h, ny + y * h];
  const Bd = new Path2D(); spline(Bd, [hb(-.22, -.3), hb(.22, -.24), B(.3, .02), B(.62, .16 + dr / h * .6), B(.9, .42 + dr / h), B(1.08, .9), B(1.18, 1.8), B(-1.3, 1.8), B(-1.22, .8), B(-.9, .2), B(-.5, -.02), B(-.26, -.12)], true, .5);
  // kanat: omzun arkasından kemerle yükselir, sırtın gerisine iner
  const wg = o.wing ?? .6, Wg = new Path2D();
  spline(Wg, [B(-.3, .25), B(-.85, -.2 - .5 * wg), B(-1.2, -.5 - .8 * wg), B(-1.6, -.45 - .7 * wg), B(-1.9, -.1 - .3 * wg), B(-2.0, .5), B(-1.9, 1.8), B(-.4, 1.8), B(-.3, .6)], true, .7);
  const INK = GR.tone(.02);
  GR.fill(Wg, INK, { th: 0, id: 6 }); GR.fill(Bd, INK, { th: 0, id: 0 }); GR.fill(Hd, INK, { th: 0, id: 0 }); GR.fill(Hc, INK, { th: 0, id: 0 });
  // kanat içi tüy vuruşları (sivrilen, kesintisiz) ve kenar ışığı
  tx.save(); tx.clip(Wg);
  for (let k = 0; k < 4; k++) { const u = k / 3; nif_vurus2([B(lerp(-.92, -1.7, u), lerp(-.3, -.35, u) - .5 * wg), B(lerp(-1.02, -1.72, u) - .1, .35), B(lerp(-1.1, -1.75, u) - .15 * u, 1.1 + .2 * u)], 9 - k, 1, .3, .2); }
  tx.restore();
  // kenar ışığı: güneşe yakın dış hatta (keskin üst katman), güneşten uzaklaştıkça yok olur
  const S = o.sun, all = new Path2D(); all.addPath(Wg); all.addPath(Bd); all.addPath(Hd);
  nif_kenarIsik([Wg, Bd, Hd, Hc], S, 7);
  // saçta birkaç kısa hilal
  return { all, head: Hd };
}
// birleşik siluetin dış kenarında (iç örtüşme çizgileri olmadan) kâğıt rengi kenar ışığı: maske − 8 yönde kaydırılmış maske.
// Güneş çevresinde tam, uzaklaştıkça söner. P: Path2D (dünya), S: {x, y, r}, d: bant kalınlığı (dünya px)
const NIF_RM = makeCanvas(DW, DH), NIF_rm = NIF_RM.getContext('2d'), NIF_RM2 = makeCanvas(DW, DH), NIF_rm2 = NIF_RM2.getContext('2d');
function nif_kenarIsik(P, S, d = 7) {
  const M = GR.tx.getTransform(), k = Math.hypot(M.a, M.b), dd = d * k;
  NIF_rm.setTransform(1, 0, 0, 1, 0, 0); NIF_rm.clearRect(0, 0, DW, DH); NIF_rm.setTransform(M); NIF_rm.fillStyle = '#fff'; for (const q of (Array.isArray(P) ? P : [P])) NIF_rm.fill(q);   // parça parça (birleşik yolda zıt yönlü parçalar delik açar)
  NIF_rm2.setTransform(1, 0, 0, 1, 0, 0); NIF_rm2.globalCompositeOperation = 'source-over'; NIF_rm2.clearRect(0, 0, DW, DH); NIF_rm2.drawImage(NIF_RM, 0, 0);
  NIF_rm2.globalCompositeOperation = 'destination-in';   // aşındırma: 8 yönde kaydırılmış maskelerin kesişimi
  for (let i = 0; i < 8; i++) { const a = i * TAU / 8; NIF_rm2.drawImage(NIF_RM, Math.cos(a) * dd, Math.sin(a) * dd); }
  NIF_rm.setTransform(1, 0, 0, 1, 0, 0); NIF_rm.globalCompositeOperation = 'destination-out'; NIF_rm.drawImage(NIF_RM2, 0, 0);   // bant = maske − aşınmış
  NIF_rm.globalCompositeOperation = 'source-in'; NIF_rm.setTransform(M);
  const g = NIF_rm.createRadialGradient(S.x, S.y, S.r * .7, S.x, S.y, S.r * 1.9); g.addColorStop(0, GR.paperCol); g.addColorStop(1, 'rgba(230,223,207,0)');
  NIF_rm.fillStyle = g; NIF_rm.fillRect(-4000, -4000, 12000, 12000); NIF_rm.globalCompositeOperation = 'source-over';
  const O = GR.ox; O.save(); O.setTransform(1, 0, 0, 1, 0, 0); O.drawImage(NIF_RM, 0, 0); O.restore();
}
// yakın plan sahnesi: gök + güneş + figür. o: nif_yakinSiluet seçenekleri + {sun, clouds, soft, dark}
function nif_yakin(t, o) {
  nif_gok(o.sun, { beams: [], soft: o.soft, dark: o.dark, clouds: o.clouds || [], t });
  return nif_yakinSiluet(t, o);
}
// eski adla (G01, G02, panolar): kanca figürü
function nif_kancaSiluet(t, a, K = NIF_KANCA, tilt) { return nif_siluet7(t, a, K, { tilt }); }
// o: {K (figür yeri ve boyu; varsayılan NIF_KANCA), sun, clouds, hz, tepe (false: zirve yok), dive (0..1: siyah içe dalış + kareyi dolduran alevler), tilt}
function nif_kancaA01(t, a, o = {}) {   // a: 0..1+ alevin büyüklüğü ('cehennemim')
  const K = o.K || NIF_KANCA, S0 = o.sun || { x: 880, y: 430, r: 330 }, ks = K.U / 640, U = K.U, tx = GR.tx;
  // güneş: temiz kâğıt disk; ışınsal tarama diskin hemen dışında başlar (çizgi çember yok)
  nif_gok(S0, { beams: [], clouds: o.clouds || [{ x: -120, y: 60, w: 640, h: 240, seed: 12, n: 3 }, { x: 1720, y: 130, w: 1100, h: 420, seed: 19, n: 4 }], t });
  nif_siralar({ hz: o.hz ?? 890 });
  if (o.tepe !== false) nif_tepe(o.tepe || { x: K.x, y: K.y + 6 * ks, s: ks, seed: 3, lit: [0, -1] });
  const F = nif_siluet7(t, a, K, { tilt: o.tilt }), c = [F.fb[0], F.fb[1] - 120 * F.s];
  const pw = clamp(o.pencere || 0);
  if (pw > 0) {   // içe dalış: siluet göğüs noktası çevresinde büyür (ve kadraj ortasına kayar); içi yanan göl (aşınmış iç hatla kırpılır),
                  // dışta kalın siyah çerçeve ve ince kenar ışığı; baş, omuzlar ve kanatların dış çizgisi karede kalır
    const g = lerp(1, 1.8, pw), dc = [lerp(0, 960 - c[0], pw), lerp(0, 600 - c[1], pw)];
    const Kg = { x: c[0] + dc[0] + (K.x - c[0]) * g, y: c[1] + dc[1] + (K.y - c[1]) * g, U: U * g }, Fg = nif_yol7(Kg, F.th), parts = [...Fg.wings, Fg.cloak, Fg.head];
    { const O = GR.ox; O.save(); O.globalCompositeOperation = 'destination-out'; for (const P of parts) O.fill(P); O.restore(); }
    // nif_icCehennem için sahte iskelet: kutu köşeleri
    const bb = [Kg.x - 330 * Fg.s, Kg.y - 870 * Fg.s, Kg.x + 330 * Fg.s, Kg.y], hh = Kg.U / 8;
    const Jf = { h: hh, hd: [bb[0], bb[1]], hip: [bb[2], bb[3]], shN: [bb[0], bb[3]], shF: [bb[2], bb[1]], elN: [bb[0], bb[1]], elF: [bb[0], bb[1]], wrN: [bb[0], bb[1]], wrF: [bb[0], bb[1]],
      knN: [bb[0], bb[1]], knF: [bb[0], bb[1]], anN: [bb[0], bb[1]], anF: [bb[0], bb[1]], nk: [Kg.x, bb[1]], shC: [Kg.x, bb[1]] };
    const ks = lerp(.4, 1, pw), cc = [c[0] + dc[0], c[1] + dc[1]];
    nif_icCehennem(Jf, m => { if (m) { GR.fill(Fg.cloak, GR.tone(.02), { th: 0, id: 0 }); return; }   // pencere yalnız gövdede (pelerin); baş ve kanatlar düz siyah kalır
        for (const P of parts) GR.fill(P, GR.tone(.02), { th: 0, id: 0 }); nif_kenarIsik(parts, { x: cc[0], y: cc[1], r: 4000 }, 4); },
      { t, k: 1, neck: false, margin: .3, erode: lerp(8, 30, pw) / hh, full: true, gol: { sway: .02, front: pw > .6 }, scale: ks, at: [cc[0], cc[1] + 40 * pw] });
  }
  const dv = clamp(o.dive || 0);
  if (dv > 0) {   // dalış: göğüsten büyüyen siyah (siluetin içi kareyi doldurur) ve onunla büyüyen alevler
    // siluetin kendisi göğüs noktası çevresinde büyür (maske büyür, kamera değil): içi siyah, içinde alevler
    const g = 1 + 26 * Math.pow(dv, 2.2), Kg = { x: c[0] + (K.x - c[0]) * g, y: c[1] + (K.y - c[1]) * g, U: U * g }, Dk = nif_yol7(Kg, F.th).all;
    GR.fill(Dk, GR.tone(.02), { th: 0, id: 0 });
    { const O = GR.ox; O.save(); O.globalCompositeOperation = 'destination-out'; O.fill(Dk); O.restore(); }
    const kk = 1.6 + 7 * Math.pow(dv, 1.2), by = lerp(c[1], H + 40, E.io2(dv));
    tx.save(); tx.clip(Dk);
    nif_alev7(t, Object.assign({}, F, { fb: [F.fb[0], by], cloak: Dk }), 1, kk / 1.3);
    if (dv > .25) PR.flameBank(-200, W + 200, H + 60, 820 * E.out2((dv - .25) / .75), t, 27, { n: 7, env: f => .55 + .45 * Math.abs(Math.cos(f * PI)), wr: .5, base: .3, edge: .4, core: .8, frags: false, speed: .5, curl: .45, solidBelow: 1e5 });
    tx.restore();
  }
  return F;
}
// A02: aynı baş + pelerin yolu (konum, ölçek aynı), kâğıt beyazı; kanatlar KN.feathered (kök aynı omuz noktasında), yarı kapalıdan açığa.
// Işık figürün arkasından (göğüs) çıkar: az ama güçlü, sivrilen ışın vuruşları; figürle aralarında 30–40 px siyah ayla kalır.
// op: kanat açıklığı 0..1, rl: ışın boyu 0..1
const NIF_A02_KANAT = [{ open: .15, lift: .9, droop: .6, rot: -.15 }, { open: 1, lift: .75, droop: .1, rot: 0 }];
function nif_kancaA02(t, op, rl, tilt = NIF_EGIM) {
  const { tx, tone } = GR, U = NIF_KANCA.U, M = tx.getTransform();
  const BG = new Path2D(); BG.rect(-400, -400, W + 800, H + 800); GR.fill(BG, tone(.02), { th: 0, id: 0 });
  // alçak bulut kütlesi (zirvenin yerinde): katmanlı, kenar ışıklı
  PR.cloud({ x: NIF_KANCA.x - 560, y: NIF_KANCA.y + 150, w: 1300, h: 330, seed: 12, lit: [.35, -1], base: .03, hi: .85, core: .02, n: 4, drift: Math.sin(t * .1) * 6 });
  PR.cloud({ x: NIF_KANCA.x + 620, y: NIF_KANCA.y + 160, w: 1300, h: 330, seed: 19, lit: [-.35, -1], base: .03, hi: .85, core: .02, n: 4, drift: Math.sin(t * .08 + 1) * 6 });
  const A = NIF_A02_KANAT[0], B = NIF_A02_KANAT[1], u = E.io2(clamp(op)), mx = k => lerp(A[k], B[k], u);
  nif_kancaKanat({ open: mx('open'), lift: mx('lift'), droop: mx('droop'), rot: mx('rot'), dark: 0, rim: .75, lit: [0, -1], t });
  const F = nif_siluet7(t, 0, NIF_KANCA, { tilt, beyaz: true, kanat: false }), P = (x, y) => [NIF_KANCA.x + x * U, NIF_KANCA.y + y * U];
  if (rl > .01) {
    // figürün dış hattı: ton katmanında merkezden dışa son açık piksel
    const c = P(0, -.62), cd = M.transformPoint(new DOMPoint(c[0], c[1])), sc = Math.hypot(M.a, M.b);
    const Wd_ = tx.canvas.width, Hd_ = tx.canvas.height, I = tx.getImageData(0, 0, Wd_, Hd_).data;
    const r = rng(5), N = 30;
    for (let i = 0; i < N; i++) {
      const a = -PI / 2 + (i / N - .5) * TAU + (r() - .5) * .12, ca = Math.cos(a), sa = Math.sin(a);
      const Lr = 250 + 550 * Math.pow(r(), 1.4), w0 = 7 + 2 * r();
      if (sa > .35 && r() < .6) continue;   // aşağı yalnız birkaç ışın
      let d = 0;
      for (let s = 1100; s > 0; s -= 4) { const x = (cd.x + ca * s * sc) | 0, y = (cd.y + sa * s * sc) | 0; if (x < 0 || y < 0 || x >= Wd_ || y >= Hd_) continue; if (I[(y * Wd_ + x) * 4] > 150) { d = s; break; } }
      if (!d) continue;
      const g = d + 32 + r() * 8, L = Lr * rl, x0 = c[0] + ca * g, y0 = c[1] + sa * g;
      nif_vurus([[x0, y0], [x0 + ca * L * .5, y0 + sa * L * .5], [x0 + ca * L, y0 + sa * L]], w0 * lerp(.5, 1, rl), 1);
    }
  }
  return F;
}
plan('P001', (ctx, st) => {
  const t = st.t, tC = Wd('A01', 'cehennemim');
  levha(ctx, { cx: lerp(930, 960, E.io2(st.p)), cy: 540, z: 1 }, () => { const u = E.io2(nif_u(t, tC - .2, tC + .9)); nif_kancaA01(t, u, { tilt: NIF_EGIM - .05 * u }); }, NIF_BG);
}, { tr: { type: 'cut' },
  over: (ctx, st) => { const t0 = Wd('A01', 'cehennemim') - st.at; quote(ctx, '“Ben cehennemim.”', 1480, 108, st.lt, { t0, px: 84, panel: false, kaynak: 'KAYIP CENNET · IV. 75' }); } });   // sağ kenar ≤ 1790; P137 ile aynı yerleşim (ayna)
plan('P002', (ctx, st) => {
  const t = st.t, s0 = S('A02'), s1 = Se('A02');
  const op = E.out2(nif_u(t, s0 + .1, s0 + 1.2)), rl = E.out2(nif_u(t, s0, s0 + .5)) * (1 - E.io2(nif_u(t, s1 - .9, s1 + .4)));
  const tl = (NIF_EGIM - .05) * (1 - E.io2(nif_u(t, s0 + .15, s0 + 1.2)));   // kesmede A01'in son eğimi; kanatlar açılırken baş kalkar
  levha(ctx, { cx: lerp(960, 985, E.io2(st.p)), cy: 540, z: 1 }, () => nif_kancaA02(t, op, rl, tl), NIF_BG);
}, { tr: { type: 'cut' } });

// ═════════ ortak ═════════
const NIF_IC = { wings: true, neck: false, margin: 6, erode: .3, alev: { w: 3.6, h: 3.8, dy: 1.1 } };   // iç cehennemin ortak dili (A01, G02, G07)
const NIF_PELERIN = { open: .45, lift: .2, droop: .7, rotL: -1.5, rotR: 1.5, ruin: 0 };   // yarı kapalı, omuzdan pelerin gibi inen kanatlar
const NIF_PROF = { open: .45, lift: 0, droop: 1, spanL: 5, prof: true, ruin: 0 };   // profil: tek kanat sırttan aşağı, pelerin gibi
const NIF_KAPALI = { open: .25, lift: .05, droop: .9, ruin: 0 };   // kanatlar katlı: sırtta pelerin gibi
const NIF_BG = [.5, 0, 1];
// yazı: bulutun koyu kütlesi üstünde, yumuşak zeminle
function nif_soz(ctx, s, x, y, st, wd, o = {}) { quote(ctx, s, x, y, st.lt, Object.assign({ t0: wd - st.at, px: 72, maxW: 900, panel: false }, o)); }

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
  over: (ctx, st) => { const t0 = Wd('F09', 'nifatesin') - st.at; etiket(ctx, 'Nifates Dağı', 330, 130, st.lt - t0, st.d - t0 - .2, { px: 46, panel: false }); } });

// ═════════ P065 (G01): bölüm kartı; geniş plan, tepede yalnız figür ═════════
plan('P065', (ctx, st) => {
  const t = st.t, S0 = { x: 1290, y: 520, r: 360 };
  levha(ctx, camLerp({ cx: 1000, cy: 540, z: 1 }, { cx: 960, cy: 540, z: 1 }, st.p, E.io2), () => cizNifates(t, {
    sun: S0, hz: 860, tepe: { x: 1290, y: 862, s: .6, seed: 7 }, t, aden: { x: 380, y: 850, w: 300, s: .8 },
    clouds: [{ x: 560, y: 250, w: 1600, h: 560, seed: 12, n: 5 }],
    fig: (tp) => nif_kancaSiluet(t, .3, { x: tp[0], y: tp[1] + 3, U: 190 }) }), NIF_BG);
}, { tr: { type: 'black', dur: 1.4, end: true },
  over: (ctx, st) => chapterCard(ctx, 'GÜNEŞE İTİRAF', 'Kimsenin duymadığını sanırken, Şeytan kendine ne söyler?', st.lt - 1.0, st.d - 1.0, { x: 620, y: 290 }) });

// ═════════ P066 (G02): aynı kanca figürü (A01), göğsünde küçük alev: "cehennemi içinde taşıyor" ═════════
// Alev 'cehennemi'de belirir (küçük), 'kaçamıyorsa'da biraz büyür. Kadraj: figür sola, güneş sağda; yatay kaydırma.
plan('P066', (ctx, st) => {
  const t = st.t, tC = Wd('G02', 'cehennemi'), tK = Wd('G02', 'kaçamıyorsa');
  const a = -.7 + .7 * E.io2(nif_u(t, tC - .2, tC + 1.2)) + .35 * E.io2(nif_u(t, tK - .6, tK + 1));
  levha(ctx, { cx: lerp(1000, 970, E.io2(st.p)), cy: 540, z: 1 }, () => nif_kancaA01(t, a, {
    K: { x: 720, y: 930, U: 560 }, sun: { x: 1330, y: 420, r: 300 }, hz: 900,
    clouds: [{ x: -100, y: 60, w: 760, h: 260, seed: 21, n: 3 }] }), NIF_BG);
}, { tr: { type: 'cut' } });

// ═════════ P068 (G03): profil güneşe karşı; eliyle gözünü siper eder (alttan) ═════════
// 'ışınlarından' kelimesinde yakın kol kalkar, el kaşın üstüne gelir; güneşten yüzüne iki ince ışın kaması uzanır.
plan('P068', (ctx, st) => {
  const t = st.t, S0 = { x: 1290, y: 380, r: 320 }, tI = Wd('G03', 'nefret') - .9, h = 104, FX = 1000;
  const up = E.io2(nif_u(t, tI - .6, tI + .9));
  levha(ctx, camLerp({ cx: 990, cy: 540, z: 1 }, { cx: 990, cy: 540, z: 1.08 }, st.p, E.io2), () => {
    const J0 = nif_rig({ x: FX, y: 0, ground: 1030, h, facing: 1, twist: .9, head: .18 });
    const hd = J0.hd, a = Math.atan2(hd[1] - S0.y, hd[0] - S0.x);
    cizNifates(t, {
      sun: S0, hz: 990, tepe: { x: FX, y: 1032, s: 1.3, seed: 11 }, t, clouds: [{ x: 330, y: 170, w: 1150, h: 420, seed: 12, n: 5 }],
      beams: [[a - .025, .03, 1300], [a + .03, .022, 1250], [-1.2, .035, 1300], [-.45, .04, 1200], [-2.2, .03, 1300]],
      fig: () => nif_seytan({ x: FX, y: 0, ground: 1030, h, facing: 1, twist: .9, lean: lerp(0, -.04, up), head: lerp(.18, .02, up), shTilt: lerp(-.03, -.1, up), t,
        armN: [lerp(.14, 1.25, up), lerp(.25, 2.0, up)], armF: [-.15, .2],
        legN: [.18, -.04], legF: [-.14, -.02], lum: .22, lit: nif_isik(S0, hd[0], hd[1]), wings: NIF_PROF }) });
  }, NIF_BG);
}, { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => nif_soz(ctx, '“Ey güneş… ışınlarından nefret ediyorum.”', 380, 150, st, Wd('G03', 'ey'), { maxW: 620 }) });

// ═════════ P069 (G04): baş-omuz yakın planı; güneşin önünde profil; "benden" ile baş öne eğilir, ışık yumuşar ═════════
plan('P069', (ctx, st) => {
  const t = st.t, tB = Wd('G04', 'benden'), tY = Wd('G04', 'beni');
  const bow = E.io2(nif_u(t, tB - .4, tB + 2.2)), soft = E.io2(nif_u(t, tY - 1, tY + 4));
  levha(ctx, { cx: lerp(975, 950, E.io2(st.p)), cy: 540, z: 1 }, () => nif_yakin(t, {
    sun: { x: 1120, y: 420, r: 400 }, soft, clouds: [{ x: 160, y: 120, w: 980, h: 360, seed: 21, n: 4 }],
    f: 1, nx: 1010, ny: 760, h: 470, bow: lerp(-.05, .5, bow), drop: .06 * bow, wing: .55 }), NIF_BG);
}, { tr: { type: 'cut' },
  over: (ctx, st) => nif_soz(ctx, '“Hak etmemişti.”', 370, 150, st, Wd('G04', 'hak'), { px: 76 }) });

// ═════════ P070 (G05): güneş diskinin içinde anı ═════════
// Kadrajı güneş doldurur. İçinde açık (cennet tarifi) saflar: arkasındaki taramayla ayrılan kâğıt beyazı, sade melekler;
// önde, safların arasında bir boşlukta tek, sıradan küçük melek. Anı 'keşke' ile belirir, 'kalırdım' ile söner.
plan('P070', (ctx, st) => {
  const t = st.t, tK = Wd('G05', 'keşke'), tE = Se('G05');
  const a = E.io2(nif_u(t, tK, tK + 1)) * (1 - E.io2(nif_u(t, tE - .2, tE + .6)));
  levha(ctx, { cx: lerp(990, 950, st.p), cy: 540, z: 1 }, () => {
    const { tx, px, tone } = GR, S0 = { x: 960, y: 540, r: 520 };
    nif_gok(S0, { beams: [], ring: 4 });
    if (a <= 0) return;
    const D = new Path2D(); D.arc(S0.x, S0.y, S0.r - 3, 0, TAU);
    // anı diskin içine basılır; görünürlük a: önce ton katmanında karışır (yarıdan sonra tarama da)
    const T0 = tx.getImageData(0, 0, tx.canvas.width, tx.canvas.height);
    GR.save(); for (const c of [tx, px]) c.clip(D);
    // ışık merkezi yukarıda (taramasız), aşağı doğru hafif taralı açık zemin
    const g = tx.createRadialGradient(960, 160, 40, 960, 400, 620); g.addColorStop(0, tone(1)); g.addColorStop(.4, tone(.92)); g.addColorStop(1, tone(.74));
    GR.fill(D, g, { type: 'ray', cx: 960, cy: 160, n: 96, id: 10, w: 3 });
    // koyu bulut bankı (çapa)
    const Bk = new Path2D(); Bk.moveTo(380, 560);
    for (let x = 380; x <= 1540; x += 290) Bk.quadraticCurveTo(x + 145, 470 + 30 * Math.sin(x * .011), x + 290, 540 + 20 * Math.sin(x * .03));
    Bk.lineTo(1540, 1100); Bk.lineTo(380, 1100); Bk.closePath();
    GR.fill(Bk, tone(.03), { th: 0, id: 2 });
    PR.cuts([[420, 540], [670, 500], [960, 510], [1250, 500], [1500, 540]], [0, 1], { len: [10, 46], gap: [40, 110], w: 5, seed: 8, clip: Bk, bend: .2 });
    // melekler: iki yay biçimli küme (düz sıra ve tek yöne dönük saf değil; hassasiyet: "imam ve cemaat" okuması olmasın),
    // farklı yönlere dönük, kanatlı, uzun giysili (robe) kâğıt beyazı figürler. "Sıradan melek" kümenin İÇİNDE, ötekilerle aynı boyda;
    // yalnız arkasında kısa bir kâğıt boşluğu (açık hale değil: kümenin koyu bankında bir aralık) ve hafif öne eğik başıyla ayrılır.
    const rr = rng(11), M = [];
    for (const [cx, cy, n, rx, ry] of [[690, 640, 6, 200, 120], [1240, 650, 6, 210, 120]])
      for (let i = 0; i < n; i++) { const u = i / (n - 1), a = PI * (.15 + .7 * u) + (cx > 960 ? PI : 0); M.push({ x: cx + Math.cos(a) * rx + (rr() - .5) * 30, y: cy + Math.abs(Math.sin(a)) * ry * (cx > 960 ? -1 : 1) * .6 + 60 * u + (rr() - .5) * 20, f: rr() < .5 ? 1 : -1, tw: rr() }); }
    M.push({ x: 1150, y: 690, f: -1, tw: .2, siradan: true });
    for (const m of M) m.h = (22 + (m.y - 560) * .1) * (m.siradan ? .86 : 1);   // derinlik: yakındaki büyük; sıradan melek yarım baş kısa
    M.sort((p, q) => p.y - q.y);
    for (const m of M) {
      const Jm = SF.rig({ x: m.x, y: m.y, h: m.h, facing: m.f, twist: .15 + m.tw * .5, head: m.siradan ? -.25 : (rr() - .5) * .3, armN: [.06, .1], armF: [-.06, .1] });
      if (m.siradan) { const A = new Path2D(); A.ellipse(Jm.hd[0], Jm.hd[1] - 1.1 * m.h, .9 * m.h, .55 * m.h, 0, 0, TAU); GR.fill(A, GR.tone(1), { th: 0, id: 10 }); }   // başının üstünde küçük temiz kâğıt açıklık
      for (const sd of [-1, 1]) { const sh = sd < 0 ? Jm.shN : Jm.shF; GR.frame(Jm.shC[0] + sd * .35 * m.h, Jm.shC[1] + .2 * m.h, sd * -.15, sd, 1);
        KN.feathered({ span: 4.2 * m.h, open: .35, lift: .7, droop: .3, dark: 0, rim: .6, ruin: 0, root: .1, lit: [0, -1], t, seed: 60 + sd }); GR.unframe(); }
      SF.draw(Jm, { lum: 1, lit: [0, -1], t, robe: true, legs: true, eye: 0, lines: 1, seed: 5 + Math.round(m.x) % 7 });
    }
    GR.restore();
    if (a < 1) { const T1 = tx.getImageData(0, 0, tx.canvas.width, tx.canvas.height), d0 = T0.data, d1 = T1.data; for (let i = 0; i < d0.length; i += 4) { const v = d0[i] + (d1[i] - d0[i]) * a; d1[i] = d1[i + 1] = d1[i + 2] = v; } tx.putImageData(T1, 0, 0); }
  }, NIF_BG);
}, { tr: { type: 'fade', dur: .8 } });

// ═════════ P072 (G07): doruk; üç kadraj, kelimeye bağlı ═════════
//  «Vay hâlime!» orta: kanca figürü sağda, güneş solda (G02'nin aynası);
//  «nereye kaçayım?» (P072y) baş-omuz yakın planı: baş kalkar, gözler göğe;
//  «Hangi yana kaçsam cehennem. Ben cehennemim.» (P072z) A01 karesinin birebir geri çağrısı + içe dalış: siluet göğüs noktası çevresinde büyür,
//  içinde yanan göl görünür; itme bittiğinde kanatların ve başın dış çizgisi karenin kenarlarında kalın siyah çerçeve, kenarında ince kenar ışığı.
plan('P072', (ctx, st) => {
  const t = st.t, tV = Wd('G07', 'vay');
  levha(ctx, { cx: lerp(940, 970, E.io2(st.p)), cy: 540, z: 1 }, () => nif_kancaA01(t, .5 + .3 * E.io2(nif_u(t, tV, tV + 2)), {
    K: { x: 1220, y: 930, U: 560 }, sun: { x: 560, y: 420, r: 300 }, hz: 900, tilt: NIF_EGIM * 1.1,
    clouds: [{ x: 1980, y: 70, w: 760, h: 270, seed: 21, n: 3 }] }), NIF_BG);
}, { tr: { type: 'cut' } });
shot(Wd('G07', 'nereye') - .25, (ctx, st) => {
  const t = st.t, u = E.io2(nif_u(t, st.at, st.at + 1.4));
  levha(ctx, { cx: lerp(950, 975, E.io2(st.p)), cy: 540, z: 1 }, () => nif_yakin(t, {
    sun: { x: 420, y: 560, r: 330 }, clouds: [{ x: 1900, y: 100, w: 800, h: 330, seed: 19, n: 4 }],
    f: -1, nx: 900, ny: 820, h: 460, bow: lerp(.15, -.22, u), drop: .03, wing: lerp(.5, .9, u) }), NIF_BG);
}, { id: 'P072y', tr: { type: 'cut' } });
shot(Wd('G07', 'hangi') - .1, (ctx, st) => {
  const t = st.t, tH = Wd('G07', 'hangi'), tB = Wd('G07', 'ben'), dv = E.io2(nif_u(t, tH + .3, tB - .55));
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => nif_kancaA01(t, 1 + .3 * dv, { pencere: dv }), NIF_BG);
}, { id: 'P072z', tr: { type: 'cut' },
  over: (ctx, st) => nif_soz(ctx, '“Ben cehennemim.”', 1480, 108, st, Wd('G07', 'ben'), { px: 84, panel: false, kaynak: 'KAYIP CENNET · IV. 75' }) });   // A01 ile aynı yer
// tam kare iç cehennem (maskenin büyümesi bittikten sonra): yerel çerçeve dünya ile aynı
function nif_icGolTam(t) { cizGol(t, { fig: false, chains: false, sway: .02 }); }

// ═════════ P074–P075 (G09, G09b): diz ışığa doğru bükülür; durur, doğrulur ═════════
// Yandan orta plan, güneş sağda. G09 boyunca yakın diz yavaşça öne bükülür, gövde öne eğilir, baş düşer (izleyici diz çökecek sanır);
// G09b'de 'ama' kelimesine dek bekler, 'gururum' ile doğrulur, baş kalkar. Yazı: "boyun eğmek", 'yasaklıyor' ile zincir halkasıyla kilitlenir.
const NIF_G09_S = { x: 1450, y: 360, r: 300 };
function nif_g09(t, b, hd) {   // b: 0..1 bükülme, hd: baş (−1 eğik … 1 dik, mağrur)
  const S0 = NIF_G09_S, e = E.io2(b);
  return cizNifates(t, {
    sun: S0, hz: 930, tepe: { x: 820, y: 978, s: 1, seed: 17 }, t, soft: .3 * e, clouds: [{ x: 380, y: 180, w: 1200, h: 500, seed: 12, n: 5 }],
    beams: [[Math.atan2(560 - S0.y, 820 - S0.x), .04 + .02 * e, 1100], [-2.0, .03, 1200], [-1.1, .035, 1300], [-.4, .04, 1300]],
    fig: () => nif_seytan({ x: 820, y: 0, ground: 975, h: 96, facing: 1, twist: .85, lean: .22 * e - .03 * hd, head: lerp(-.05, -.42, e) + .25 * Math.max(0, hd), shTilt: lerp(-.03, .04, e), t,
      armN: [lerp(.1, .3, e), lerp(.25, .35, e)], armF: [lerp(-.1, .15, e), lerp(.2, .3, e)],
      legN: [lerp(.12, 1.25, e), lerp(-.05, -1.3, e)], legF: [lerp(-.1, .02, e), lerp(-.03, -1.35, e)],
      lum: .22, lit: nif_isik(S0, 820, 560), wings: NIF_PROF }) });
}
plan('P074', (ctx, st) => {   // G09: baş-omuz yakın planı; 'yumuşar' ile baş ışığa doğru eğilir, omuz düşer (bükülmenin başlangıcı)
  const t = st.t, u = E.io2(nif_u(t, Wd('G09', 'yumuşar') - .3, st.end));
  levha(ctx, { cx: lerp(960, 935, E.io2(st.p)), cy: 540, z: 1 }, () => nif_yakin(t, {
    sun: { x: 1380, y: 380, r: 360 }, soft: .3 * u, clouds: [{ x: 180, y: 110, w: 1000, h: 380, seed: 12, n: 4 }],
    f: 1, nx: 860, ny: 780, h: 440, bow: lerp(.05, .32, u), drop: .1 * u, wing: lerp(.6, .3, u) }), NIF_BG);
}, { tr: { type: 'cut' },
  over: (ctx, st) => nif_soz(ctx, '“Pişmanlığa hiç yer kalmadı mı?”', 420, 160, st, Wd('G09', 'pişmanlığa'), { maxW: 620 }) });
// kilitli söz: italik söz, çevresinde bir zincir halkası kapanır (sağ ucunda dikine ikinci halka). lt: kapanış zamanına göre (−: açık)
function nif_kilitliSoz(ctx, s, x, y, aIn, kap, o = {}) {
  if (NOTEXT || aIn <= 0) return;
  ctx.save(); baseT(ctx); ctx.globalAlpha = aIn;
  const px = o.px || 70; ctx.font = FONT.alinti(px); const wd = ctx.measureText(s).width;
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
  const b = .72 * E.io2(nif_u(t, st.at - .2, st.at + 1.6)) * (1 - E.io2(nif_u(t, tA, tG + .6))), hd = E.io2(nif_u(t, tG - .3, tG + 1.2));   // diz bükülür (G09'un devamı), 'ama'dan doğrulur
  levha(ctx, { cx: lerp(900, 930, E.io2(st.p)), cy: 570, z: 1 }, () => nif_g09(t, b, hd), NIF_BG);
}, { tr: { type: 'cut' },
  over: (ctx, st) => {
    const t = st.t, tB = Wd('G09b', 'boyun'), tY = Wd('G09b', 'yasaklıyor');
    nif_kilitliSoz(ctx, 'boyun eğmek', 420, 160, clamp((t - tB) / .6) * clamp((st.end - t) / .5), nif_u(t, tY - .2, tY + .5));
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
  const c = GR.ox; c.save(); c.fillStyle = GR.paperCol;   // keskin üst katman: kâğıt rengi badem gözler, iç uçları aşağı (çatık bakış)
  for (const e of E2) {
    const op = clamp((a - e.o * .85) / .15); if (op <= 0) continue;
    const w = 15 * e.s, hh = Math.max(2.4, 5.5 * e.s * op), gap = 21 * e.s;
    for (const sd of [-1, 1]) {
      const x = e.x + sd * gap, tilt = sd * .22;
      c.save(); c.translate(x, e.y); c.rotate(tilt); c.beginPath(); c.moveTo(-w, 0); c.quadraticCurveTo(0, -hh * 1.6, w, 0); c.quadraticCurveTo(0, hh * .9, -w, 0); c.fill(); c.restore();
    }
  }
  c.restore();
}
plan('P076', (ctx, st) => {   // G10: baş-omuz yakın, güneşe sırtı dönük; başını omzunun üstünden karanlığa çevirmiş; karanlıkta ordunun gözleri
  const t = st.t, tO = Wd('G10', 'ordunun'), tE = Wd('G10', 'onlara');
  const a = E.io2(nif_u(t, tO - .5, tE + 1)), u = E.io2(nif_u(t, st.at, tO));
  levha(ctx, { cx: lerp(975, 950, E.io2(st.p)), cy: 540, z: 1 }, () => {
    const S0 = { x: 1430, y: 470, r: 330 };
    nif_gok(S0, { beams: [], t });
    PR.cloud({ x: 260, y: 300, w: 1000, h: 520, seed: 33, lit: [1, -.1], base: .03, hi: .8, core: .02, n: 4, drift: Math.sin(t * .06) * 10 });
    PR.cloud({ x: 330, y: 780, w: 1100, h: 520, seed: 35, lit: [1, -.3], base: .03, hi: .75, core: .02, n: 4, drift: Math.sin(t * .05 + 2) * 10 });
    nif_gozler(380, 560, 30, a, t, 7);
    nif_yakinSiluet(t, { sun: S0, f: -1, nx: 1470, ny: 840, h: 430, bow: lerp(.05, .2, u), drop: .05, wing: .7 });
  }, NIF_BG);
}, { tr: { type: 'cut' } });

// ═════════ P079 (G13): güneş ile figür arasındaki mesafe açılır ═════════
// İki kadraj, aralarında kesme ('barışı'): önce orta plan (figür güneşe yakın, güneş büyük), sonra yeni bir geniş kadraj:
// figür küçük, solda; güneş küçük ve uzak, sağda; arada geniş boş gök. Kamera kıpırdamaz (yalnız çok yavaş yatay kaydırma).
plan('P079', (ctx, st) => {   // G13: ters açı (omzunun üstünden güneşe ve aşağıdaki Aden'e), 'barışı'nda geniş plana kesme: figür küçük, güneş uzak
  const t = st.t, cut = t >= Wd('G13', 'barışı') - .15;
  if (!cut) {
    const S0 = { x: 1340, y: 380, r: 190 };
    levha(ctx, { cx: lerp(960, 935, st.p), cy: 540, z: 1 }, () => {
      nif_gok(S0, { beams: [], t, clouds: [{ x: 1900, y: 60, w: 700, h: 230, seed: 19, n: 3 }] });
      nif_siralar({ hz: 640, aden: { x: 1150, y: 690, w: 420, s: 1.2 }, t });
      // yakın koyu yamaç (figürün durduğu zirvenin sırtı), aşağı doğru düşer
      const G = new Path2D(); G.moveTo(-200, 880); G.quadraticCurveTo(500, 800, 1100, 980); G.lineTo(1300, 1300); G.lineTo(-200, 1300); G.closePath(); GR.fill(G, GR.tone(.02), { th: 0, id: 4 });
      // figür: arkadan, sol önde; sırtı ve başı büyük (kanatlar arkada; göğüs alevi görünmez)
      nif_siluet7(t, 0, { x: 380, y: 1620, U: 1450 }, { tilt: -.18, alev: false });
    }, NIF_BG);
  } else {
    const S0 = { x: 1640, y: 360, r: 110 };
    levha(ctx, { cx: lerp(960, 940, st.p), cy: 540, z: 1 }, () => cizNifates(t, {
      sun: S0, hz: 880, tepe: { x: 330, y: 905, s: .5, seed: 21 }, t, dark: .1, beams: [], aden: { x: 1250, y: 885, w: 260, s: .6 },
      clouds: [{ x: 700, y: 60, w: 1500, h: 260, seed: 12, n: 5 }],
      fig: (tp) => nif_kancaSiluet(t, .2, { x: tp[0], y: tp[1] + 3, U: 150 }) }), NIF_BG);
  }
}, { tr: { type: 'cut' } });

// ═════════ P080 (G14): güneşe sırtını döner; gölgesi uzayıp Aden'e ulaşır ═════════
// Dönüş 'sonunda kararını verir' ile (yandan → arkadan → öbür yan); gölge 'elveda' sözleriyle uzar, 'kötülük' kelimesinde Aden'e değer.
plan('P080', (ctx, st) => {   // G14: ayrıntı: zirvedeki ayaklar, pelerin eteği ve kanat uçları; alçak güneş gölgesini vadiye, Aden'e uzatır ('elveda' ile)
  const t = st.t, tE = Wd('G14', 'elveda'), tK = Wd('G14', 'kötülük'), L = E.io2(nif_u(t, tE - .5, tK - .4));
  const S0 = { x: 180, y: 600, r: 150 };
  levha(ctx, { cx: lerp(950, 975, E.io2(st.p)), cy: 540, z: 1 }, () => {
    nif_gok(S0, { beams: [], dark: .2, t, clouds: [{ x: 300, y: 80, w: 900, h: 280, seed: 21, n: 4 }] });
    nif_siralar({ hz: 640, dark: .2 });
    const V = new Path2D(); V.moveTo(-200, 690); for (let x = -200; x <= 2200; x += 80) V.lineTo(x, 690 + 10 * Math.sin(x * .005)); V.lineTo(2200, 1300); V.lineTo(-200, 1300); V.closePath();
    GR.fill(V, GR.tone(.9), { th: 0, id: 10 });
    nif_aden({ x: 1640, y: 760, w: 420, s: 1.1 }, t);
    // zirvenin dar kenarı (alt bant), figür üstünde
    const R = new Path2D(); R.moveTo(-200, 930); R.quadraticCurveTo(500, 905, 1100, 918); R.quadraticCurveTo(1600, 930, 2200, 960); R.lineTo(2200, 1300); R.lineTo(-200, 1300); R.closePath();
    GR.fill(R, GR.tone(.02), { th: 0, id: 4 }); GR.tx.save(); GR.tx.clip(R); GR.tx.strokeStyle = GR.tone(.95); GR.tx.lineWidth = 5; GR.tx.stroke(R); GR.tx.restore();
    // gölge: ayaklardan sağa, ova boyunca ufka (Aden'e) doğru incelerek uzanır
    const fx = 760, fy = 918, ex = lerp(980, 1600, L), ey = lerp(905, 770, L);
    if (L > .01) { const P = new Path2D(); P.moveTo(fx - 60, fy - 2); P.quadraticCurveTo(lerp(fx, ex, .5) - 20, lerp(fy, ey, .5) + 50, ex, ey); P.quadraticCurveTo(lerp(fx, ex, .5) + 80, lerp(fy, ey, .5) - 20, fx + 260, fy - 12); P.closePath(); GR.fill(P, GR.tone(.03), { th: .2, id: 0 }); }
    nif_siluet7(t, 0, { x: fx, y: fy + 2, U: 1400 }, { tilt: -.2, alev: false });
  }, NIF_BG);
}, { tr: { type: 'cut' } });
shot(Wd('G14', 'kötülük') - .3, (ctx, st) => {   // G14 'kötülük': yakın; güneş sırtında (alçak, arkada), baş kalkar, karar
  const t = st.t, u = E.io2(nif_u(t, st.at, st.at + 1.5));
  levha(ctx, { cx: lerp(960, 985, E.io2(st.p)), cy: 540, z: 1 }, () => nif_yakin(t, {
    sun: { x: 520, y: 640, r: 330 }, dark: .25, clouds: [{ x: 1500, y: 120, w: 1100, h: 400, seed: 19, n: 4 }],
    f: 1, nx: 1060, ny: 820, h: 450, bow: lerp(.12, -.1, u), drop: 0, wing: lerp(.5, .95, u) }), NIF_BG);
}, { id: 'P080y', tr: { type: 'cut' },
  over: (ctx, st) => nif_soz(ctx, '“Kötülük: sen benim iyiliğim ol.”', 1560, 130, st, Wd('G14', 'kötülük'), { maxW: 620, px: 66 }) });

// ═════════ P081 (G15): yüz üç kez değişir (üç ton); güneşte küçük bir göz ═════════
// Yüz yakın planı yok: üç duygu duruş ve ışıkla. Öfke (öne eğik, yumruklar, kanatlar kabarık, sert ışık) → kıskançlık (baş Aden'e döner,
// gövde yarı dönük, yan ışık) → umutsuzluk (çöker, kanatlar düşer, ışık söner). 'Uriel' ile güneşin içinde tek bir bakış açılır.
function nif_uriel(S0, a) {   // güneşte ince badem göz: iki ince mürekkep yayı ve küçük koyu bebek; hale, yüz, kaş yok
  if (a <= 0) return;
  const { tx, tone } = GR, w = S0.r * .2, h = w * .3 * E.out2(a), x = S0.x - S0.r * .36, y = S0.y - S0.r * .3;
  tx.save(); tx.fillStyle = tone(.03);
  for (const sd of [-1, 1]) { tx.beginPath(); tx.moveTo(x - w, y); tx.quadraticCurveTo(x, y + sd * h * 2, x + w, y); tx.quadraticCurveTo(x, y + sd * (h * 2 + 9), x - w, y); tx.fill(); }
  if (a > .3) { const k = clamp((a - .3) / .4); tx.beginPath(); tx.ellipse(x - w * .28, y, w * .14 * k, h * .9, 0, 0, TAU); tx.fill(); }   // bebek: sola, figüre bakar
  tx.restore();
}
plan('P081', (ctx, st) => {
  const t = st.t, S0 = { x: 1450, y: 420, r: 300 };
  const k1 = E.io2(nif_u(t, Wd('G15', 'öfkeyle') - .3, Wd('G15', 'öfkeyle') + .5)), k2 = E.io2(nif_u(t, Wd('G15', 'kıskançlıkla') - .2, Wd('G15', 'kıskançlıkla') + .6)),
    k3 = E.io2(nif_u(t, Wd('G15', 'umutsuzlukla') - .2, Wd('G15', 'umutsuzlukla') + .9)), ku = nif_u(t, Wd('G15', 'uriyel') - .6, Wd('G15', 'uriyel') + .6);
  // duruş anahtarları: [lean, head, shTilt, armN, armF, kanat open, lift, droop, gök karanlığı, ışık yumuşaması]
  const K = [[.0, .0, -.03, [.1, .2], [-.08, .2], .45, 0, 1, .05, 0], [.2, -.12, -.1, [.45, 1.6], [.25, 1.5], .8, .6, .3, .3, 0],
    [.06, .1, .02, [.6, .5], [-.15, .25], .5, .1, .8, .15, .3], [.28, -.6, .1, [.02, .1], [-.02, .1], .3, 0, 1, .42, .8]];
  const mx = (i) => { const a = K[0], b = K[1], c = K[2], d = K[3]; const f = (j) => { let v = lerp(a[j], b[j], k1); v = lerp(v, c[j], k2); return lerp(v, d[j], k3); }; return f(i); };
  const ar = (j) => [0, 1].map(q => { let v = lerp(K[0][j][q], K[1][j][q], k1); v = lerp(v, K[2][j][q], k2); return lerp(v, K[3][j][q], k3); });
  levha(ctx, camLerp({ cx: 930, cy: 550, z: 1.08 }, { cx: 930, cy: 550, z: 1 }, st.p, E.io2), () => cizNifates(t, {
    sun: S0, hz: 930, tepe: { x: 760, y: 978, s: 1, seed: 25 }, t, dark: mx(8), soft: mx(9), clouds: [{ x: 60, y: 130, w: 860, h: 340, seed: 12, n: 4 }],
    mid0: (S) => nif_uriel(S, ku),
    fig: () => nif_seytan({ x: 760, y: 0, ground: 975, h: 96, facing: -1, twist: lerp(.35, .7, k2 * (1 - k3)), lean: mx(0), head: mx(1), shTilt: mx(2), t,
      armN: ar(3), armF: ar(4), legN: [.12 + .1 * k1 * (1 - k2), -.05], legF: [-.12 - .08 * k1 * (1 - k2), -.03], lum: .15, lit: nif_isik(S0, 760, 560),
      wings: { open: mx(5), lift: mx(6), droop: mx(7), spanL: 7, prof: true } }) }), NIF_BG);
}, { tr: { type: 'cut' } });

// (P081u 'güneşin içinden göz' ek çekimi başkanca çıkarıldı: ışınlı güneşin içinde tek göz, 'her şeyi gören göz' simgesi gibi okunur; kırmızı çizgi 1'in ruhu)

// ═════════ P082 (G16): tepede küçük, yalnız figür; uzun bekleme ═════════
plan('P082', (ctx, st) => {
  const t = st.t, S0 = { x: 1180, y: lerp(700, 740, st.p), r: 400 };
  levha(ctx, camLerp({ cx: 960, cy: 540, z: 1.08 }, { cx: 960, cy: 540, z: 1 }, st.p, E.io2), () => cizNifates(t, {
    sun: S0, hz: 800, tepe: { x: 900, y: 836, s: .5, seed: 27 }, t, dark: .38, soft: .5,
    clouds: [{ x: 160, y: 120, w: 1300, h: 380, seed: 12, n: 5 }, { x: 1800, y: 80, w: 900, h: 320, seed: 19, n: 4 }],
    fig: (tp) => nif_seytan({ x: tp[0], y: 0, ground: tp[1] + 2, h: 30, facing: 1, twist: .6, head: -.15, shTilt: .03, t, armN: [.05, .15], armF: [-.05, .15],
      legN: [.08, -.04], legF: [-.08, -.03], lum: .15, lit: nif_isik(S0, tp[0], tp[1] - 60), wings: NIF_PROF }) }), NIF_BG);
}, { tr: { type: 'fade', dur: .9 } });

// ═════════ P137 (L07): cevap; açılışın üçüncü geri çağrısı (A01 soru → G07 itiraf → L07 cevap) ═════════
// Kadraj, güneş, zirve ve kanca figürü A01 ile aynı; göğüsteki alev A01'deki sakin hâlinde.
// 'çözülmüştü': ayakların iki yanında, zirvenin koyu zemininde kopuk zincir parçaları belirir.
// 'kendi'den 'vurdu'ya yeni zincir halka halka çizilir ve figürün kendi bedenini sarar: göğüsteki alevden çıkar, pelerinin ve kanatların
// önünden çapraz üç kez dolanır, aleve geri döner; iki ucu da alevde (dışarıda bağlandığı yer yok). Arkadan geçen kısımlar görünmez.
// 'gururu': yazı A01'deki "Ben cehennemim." ile aynı yerde, aynı biçimde; alev bir kez hafifçe büyüyüp döner.
// zincirin önden görünen parçaları (dünya noktaları; aralarındaki arka geçişler çizilmez)
const NIF_L07_ZINCIR = (() => {
  const bz = (a, c, b, n = 16) => Array.from({ length: n + 1 }, (_, i) => { const u = i / n, v = 1 - u; return [v * v * a[0] + 2 * u * v * c[0] + u * u * b[0], v * v * a[1] + 2 * u * v * c[1] + u * u * b[1]]; });
  return [
    bz([1085, 560], [990, 680], [872, 706]),               // sağ omuzdan inen tur, alevin dibine girer (bir uç)
    bz([838, 708], [740, 712], [645, 690]),                // alevin dibinden çıkıp sola (öteki uç)
    bz([1088, 720], [880, 830], [648, 800]),               // ikinci tur (önden yarım tur, çapraz)
    bz([1092, 820], [900, 940], [656, 915])                // üçüncü tur
  ];
})();
function nif_l07(t) {
  const tC = Wd('L07', 'çözülmüştü'), tK = Wd('L07', 'zinciri', 1), tV = Wd('L07', 'vurdu') + .15, tG = Wd('L07', 'gururu', 1);   // 'bu zinciri … kendi eliyle vurdu' boyunca halka halka
  const pulse = Math.sin(PI * clamp((t - tG + .1) / 1.2));
  // her tur sarıldıkça omuzlar çöker (figür ayak hizasında 3–4 px kısalır) ve baş biraz daha eğilir; son halkada kısa bir sarsılma
  const pr = E.io2(nif_u(t, tK, tV)), sh = Math.exp(-Math.pow((t - tV) / .12, 2)) * Math.sin(t * 60) * .015;
  const F = nif_kancaA01(t, .35 * pulse, { K: { x: NIF_KANCA.x, y: NIF_KANCA.y, U: NIF_KANCA.U * (1 - .018 * pr) }, tilt: NIF_EGIM - .1 * pr + sh });
  // kopuk zincirler: ayakların iki yanında, koyu zirvede; kalın, az (3 parça), uçta açılmış kırık halka
  const ca = E.io2(nif_u(t, tC - .3, tC + .9));
  if (ca > 0) {
    for (const [x0, y0, x1, y1, sg] of [[560, 960, 760, 935, 10], [960, 935, 1180, 965, 12], [1240, 1010, 1420, 990, 8]]) {
      const m = lerp(.25, 1, ca); PR.chain(x0, y0, lerp(x0, x1, m), lerp(y0, y1, m), 46, { over: true, sag: sg, lit: [0, -1] });
    }
    const O = GR.ox; O.save(); O.strokeStyle = GR.paperCol; O.lineWidth = 6; O.lineCap = 'butt';   // kırık halkalar: açık yay
    for (const [x, y, r] of [[790, 930, .3], [930, 940, -.4]]) { O.beginPath(); O.ellipse(x, y, 22 * ca, 13 * ca, r, .7, TAU - .7); O.stroke(); }
    O.restore();
  }
  // yeni zincir: görünen parçalar boyunca halka halka (her halka ~37 px adım)
  const step = 36, segs = NIF_L07_ZINCIR, links = [];
  for (const sg of segs) {   // her parçayı eşit adımlı noktalara böl
    let acc = 0; const pts = [sg[0]];
    for (let i = 1; i < sg.length; i++) { const a = sg[i - 1], b = sg[i], d = Math.hypot(b[0] - a[0], b[1] - a[1]); acc += d; while (acc >= step) { acc -= step; const u = 1 - acc / d; pts.push([lerp(a[0], b[0], u), lerp(a[1], b[1], u)]); } }
    for (let i = 1; i < pts.length; i++) links.push([pts[i - 1], pts[i]]);
  }
  const N = links.length, k = t >= tV ? N : Math.floor(clamp(nif_u(t, tK, tV)) * N);
  for (let i = 0; i < k; i++) { const [a, b] = links[i]; PR.chain(a[0], a[1], b[0], b[1], 50, { over: true, lit: [0, -1] }); }
  return F;
}
// L07 üç kadraj (kurgu kurulu): (a) G09b'nin diz bükme karesinin geri çağrısı («bir çıkış görmüştü … boyun eğmek»);
// (b) «Abdiel onu uyarmıştı» D03'teki Abdiel yakın planının geri çağrısı (sav.js P032 çizimi aynen çağrılır, alıntısıyla);
// (c) «Krallığı buldu; zinciri de …»: A01 karesi, kopuk zincirler, kendi bedenini saran zincir, "gururu".
plan('P137', (ctx, st) => levha(ctx, { cx: 915, cy: 570, z: 1 }, () => nif_g09(st.t, .72 * E.io2(nif_u(st.t, Wd('L07', 'boyun') - .6, Wd('L07', 'eğmek') + .4)), 0), NIF_BG),
  { tr: { type: 'fade', dur: .8 } });
shot(Wd('L07', 'abdiyel') - .2, (ctx, st) => {
  const P = SHOTS.find(x => x.id === 'P032'); if (!P) return;
  const m = Wd('D03', 'ama') - .9 - Wd('L07', 'cehennemde') + .2, t2 = st.t + m;   // alıntı 'cehennemde' ile belirir
  P.draw(ctx, { t: t2, lt: st.lt, d: st.d, p: st.p, at: st.at + m, end: st.end + m });
}, { id: 'P137a', tr: { type: 'cut' },
  over: (ctx, st) => { const P = SHOTS.find(x => x.id === 'P032'); if (P && P.over) { const m = Wd('D03', 'ama') - .9 - Wd('L07', 'cehennemde') + .2; P.over(ctx, { t: st.t + m, lt: st.lt, d: st.d, p: st.p, at: st.at + m, end: st.end + m }); } } });
shot(Wd('L07', 'krallığı') - .2, (ctx, st) => levha(ctx, { cx: lerp(930, 960, E.io2(st.p)), cy: 540, z: 1 }, () => nif_l07(st.t), NIF_BG),
  { id: 'P137b', tr: { type: 'cut' },
    over: (ctx, st) => { const t0 = Wd('L07', 'gururu', 1) - st.at; quote(ctx, 'gururu', 1480, 108, st.lt, { t0, px: 84, panel: false }); } });   // P001 ile aynı yerleşim (ayna)
