// oda grubu (ODA: Milton'ın odası, LON: Londra 1660): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Filmin çerçevesi: kör bir şair, göremediği ışığı ve cehennemi karanlıkta yazdırıyor.
// cizOda(t, o) ve cizLondra(t, o) AÇIK levhaya çizer (GR.begin/engrave çağırmaz): başka gruplar bölünmüş levhalarda kullanabilir.
// Değer planı "geçiş sahnesi": koyu piksel %50–60; tek odak mumun çevresi (temiz kâğıt çekirdek + kademeli yatay tarama).
// Figürler dönem silueti (gerçek portre yok): omuza inen düz saç, düz beyaz yaka, koyu cüppe; kızlar: beyaz başlık, uzun etek.
// Şairin gözü çizilmez (göz ışığı yok): körlük duruşla okunur (baş ışığa dönük, el koltuğun kolunda).
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';

const ODA_FL = 905;                                   // taban çizgisi (oda)
const oda_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));
function oda_rot(p, a) { const c = Math.cos(a), s = Math.sin(a); return [p[0] * c - p[1] * s, p[0] * s + p[1] * c]; }
// Bütün kapalı yollar aynı yönde (ekranda saat yönü) kurulur: birleşik yollar (addPath) 'nonzero' ile delik bırakmadan dolar.
function oda_yon(pts) { let a = 0; for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; a += p[0] * q[1] - q[0] * p[1]; } return a < 0 ? pts.slice().reverse() : pts; }
function oda_yol(pts, k = .8, closed = true) { const P = new Path2D(); spline(P, closed ? oda_yon(pts) : pts, closed, k); return P; }
function oda_cok(pts) { const P = new Path2D(); poly(P, oda_yon(pts), true); return P; }
// uzuv: p0→p1, iki yanda ayrı genişlik profili (px)
function oda_uzuv(p0, p1, wa, wb, n = 8) {
  const dx = p1[0] - p0[0], dy = p1[1] - p0[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L, A = [], B = [];
  for (let i = 0; i <= n; i++) { const t = i / n, x = p0[0] + dx * t, y = p0[1] + dy * t; A.push([x + nx * wa(t), y + ny * wa(t)]); B.push([x - nx * wb(t), y - ny * wb(t)]); }
  return oda_yol([...A, ...B.reverse()], .8);
}
// baş profili (sağa bakar): sade, portre ayrıntısı yok (alın, burun, çene)
const ODA_KAFA = [[-.46, -.02], [-.44, -.3], [-.27, -.5], [.0, -.57], [.24, -.48], [.34, -.32], [.37, -.17], [.38, -.08], [.5, .1], [.5, .14], [.42, .17], [.43, .24], [.4, .28], [.42, .34], [.4, .42], [.32, .5], [.16, .52], [.0, .44], [-.16, .44], [-.33, .36], [-.45, .2]];
// maske konturu: U'nun yalnız DIŞ kenarında w px'lik bant (iç alt yolların çizgisi çizilmez), ton katmanına basılır
const ODA_MK = {};
function oda_mk(k) { if (!ODA_MK[k]) { const c = makeCanvas(DW, DH); ODA_MK[k] = [c, c.getContext('2d')]; } return ODA_MK[k]; }
function oda_kontur(U, w, v = .03) {
  const tx = GR.tx, T = tx.getTransform(), [A, a] = oda_mk('a'), [B, b] = oda_mk('b'), s = w * Math.hypot(T.a, T.b);
  a.setTransform(1, 0, 0, 1, 0, 0); a.globalCompositeOperation = 'source-over'; a.clearRect(0, 0, DW, DH); a.setTransform(T); a.fillStyle = '#fff'; a.fill(U); a.setTransform(1, 0, 0, 1, 0, 0);
  b.setTransform(1, 0, 0, 1, 0, 0); b.globalCompositeOperation = 'source-over'; b.clearRect(0, 0, DW, DH); b.drawImage(A, 0, 0); b.globalCompositeOperation = 'destination-in';
  for (let k = 0; k < 12; k++) { const an = k / 12 * TAU; b.drawImage(A, Math.cos(an) * s, Math.sin(an) * s); }
  b.globalCompositeOperation = 'source-over';
  a.globalCompositeOperation = 'destination-out'; a.drawImage(B, 0, 0); a.globalCompositeOperation = 'source-in'; a.fillStyle = GR.tone(v); a.fillRect(0, 0, DW, DH); a.globalCompositeOperation = 'source-over';
  tx.save(); tx.setTransform(1, 0, 0, 1, 0, 0); tx.drawImage(A, 0, 0); tx.restore();
}
function oda_dik(x, y, w, h) { const P = new Path2D(); P.rect(x, y, w, h); return P; }
function oda_daire(x, y, r) { const P = new Path2D(); P.arc(x, y, r, 0, TAU); return P; }
function oda_birles(...L) { const P = new Path2D(); for (const q of L) if (q) P.addPath(q); return P; }

// ── ışık ve kütle ──
// Koyu kütle + ışık yanında kâğıt rengi kenar. Nokta ışık: kütle ışıktan uzağa ölçeklenip üstüne basılır, geriye ışığa bakan
// kenarda bant kalır (kalınlığı kenar normaline göre değişir, teğette sivrilir). R: ışığın menzili (daha uzaktaki kenar yanmaz).
// o: {tn, hs (tarama), L: [x, y], c: [x, y] (kütle merkezi), w (bant px), R, rv (kenar tonu)}
function oda_kut(P, o) {
  const { tx, tone } = GR, tn = o.tn ?? .03;
  GR.fill(P, tone(tn), o.hs === undefined ? { th: 0, id: 0 } : o.hs);
  if (!o.L || !(o.w > .5)) return;
  const L = o.L, c = o.c, d = Math.max(o.dMin ?? 30, Math.hypot(c[0] - L[0], c[1] - L[1])), k = 1 + o.w / d, R = o.R ?? 1e5, rv = o.rv ?? 1;
  tx.save(); tx.clip(P);
  if (R < 1e4) { const g = tx.createRadialGradient(L[0], L[1], 0, L[0], L[1], R); g.addColorStop(0, tone(rv)); g.addColorStop(.86, tone(rv)); g.addColorStop(1, tone(tn)); tx.fillStyle = g; }
  else tx.fillStyle = tone(rv);
  tx.fill(P);
  tx.translate(L[0], L[1]); tx.scale(k, k); tx.translate(-L[0], -L[1]);
  tx.fillStyle = tone(tn); tx.fill(P);
  tx.restore();
}
// Açık kütle (cennet tarifi): kâğıt tonu; gölge yanında (ışığın tersi) koyu bant.
function oda_acik(P, o) {
  const { tx, tone } = GR;
  GR.fill(P, tone(o.sv ?? .06), o.hs === undefined ? { th: 0, id: 0 } : o.hs);
  const L = o.L, c = o.c, d = Math.max(30, Math.hypot(c[0] - L[0], c[1] - L[1])), k = Math.max(.2, 1 - o.w / d);
  tx.save(); tx.clip(P); tx.translate(L[0], L[1]); tx.scale(k, k); tx.translate(-L[0], -L[1]); tx.fillStyle = tone(o.tn ?? .97); tx.fill(P); tx.restore();
}
// Mum ışığı: temiz kâğıt çekirdek (r0), sonra kademeli kararan halka (r1'de duvar karası). Ton katmanına 'lighten'.
function oda_isik(x, y, r0, r1, v = 1) {
  if (r1 <= 2 || v <= 0) return;
  const { tx, tone } = GR, g = tx.createRadialGradient(x, y, 0, x, y, r1), a = clamp(r0 / r1, 0, .9);
  g.addColorStop(0, tone(v)); g.addColorStop(a, tone(v)); g.addColorStop(a + (1 - a) * .25, tone(v * .84)); g.addColorStop(a + (1 - a) * .5, tone(v * .52)); g.addColorStop(a + (1 - a) * .76, tone(v * .2)); g.addColorStop(1, tone(0));
  tx.save(); tx.globalCompositeOperation = 'lighten'; tx.fillStyle = g; tx.fillRect(x - r1, y - r1, r1 * 2, r1 * 2); tx.restore();
}
// Duvara düşen gölge: yol ışıktan ölçeklenir (k > 1), duvarı çarpma ile karartır. yMax altına (taban) inmez.
function oda_golge(P, L, k, v, yMax) {
  const tx = GR.tx; tx.save(); tx.clip(oda_dik(-2000, -2000, 6000, yMax + 2000));
  tx.translate(L[0], L[1]); tx.scale(k, k); tx.translate(-L[0], -L[1]);
  tx.globalCompositeOperation = 'multiply'; tx.fillStyle = GR.tone(v); tx.fill(P); tx.restore();
}
// sivri uçlu dolgu çizgi (ton katmanına): pts dünya noktaları, w en kalın yer
function oda_cizgi(pts, w, v, uc = .9) {
  const tx = GR.tx, n = 14, S = [], m = pts.length;
  const cr = (p0, p1, p2, p3, t) => { const t2 = t * t, t3 = t2 * t; return [0, 1].map(j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)); };
  if (m < 2) return;
  for (let i = 0; i <= n; i++) { const u = i / n * (m - 1), s = Math.min(m - 2, Math.floor(u)), tt = u - s; S.push(m === 2 ? [lerp(pts[0][0], pts[1][0], i / n), lerp(pts[0][1], pts[1][1], i / n)] : cr(pts[Math.max(0, s - 1)], pts[s], pts[s + 1], pts[Math.min(m - 1, s + 2)], tt)); }
  const A = [], B = [];
  for (let i = 0; i <= n; i++) {
    const a = S[Math.max(0, i - 1)], b = S[Math.min(n, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
    const hw = Math.max(1.2, w * .5 * Math.pow(Math.sin(PI * (.06 + .88 * i / n)), uc));
    A.push([S[i][0] - dy / L * hw, S[i][1] + dx / L * hw]); B.push([S[i][0] + dy / L * hw, S[i][1] - dx / L * hw]);
  }
  tx.fillStyle = GR.tone(v); tx.beginPath(); poly(tx, [...A, ...B.reverse()], true); tx.fill();
}
// tornalı dikey parça (koltuk ve masa ayağı, mumluk): prof = [[u (0 üst … 1 alt), yarı genişlik oranı], ...]
const ODA_BALUS = [[0, .5], [.05, .5], [.08, .3], [.2, .62], [.32, .34], [.4, .3], [.46, .44], [.52, .3], [.84, .28], [.9, .42], [.95, .3], [1, .34]];
function oda_torna(x, y0, y1, w, prof = ODA_BALUS) {
  const A = [], B = [];
  for (const [u, r] of prof) { const y = lerp(y0, y1, u); A.push([x - r * w, y]); B.push([x + r * w, y]); }
  return oda_yol([...A, ...B.reverse()], .55);
}

// ── mum ──
// x: mumluk tabanının ortası, y: masa yüzü, s: ölçek; o: {alev (0..1; 0 sönük), boy (mumun kalan boyu 0..1), seed, L}
function oda_mumAlev(x, y, s = 1, o = {}) { const k = s, top = y - 46 * k - 78 * k * (o.boy ?? 1); return [x, top - (o.ah ?? 66) * .4 * k * (o.alev ?? 1)]; }
function oda_mum(t, x, y, s = 1, o = {}) {
  const { tx, tone } = GR, k = s, alev = o.alev ?? 1, top = y - 46 * k - 78 * k * (o.boy ?? 1);
  const F = oda_mumAlev(x, y, s, o), L = alev > .05 ? F : (o.L || null);
  const foot = oda_yol([[x - 27 * k, y], [x - 25 * k, y - 5 * k], [x - 10 * k, y - 9 * k], [x + 10 * k, y - 9 * k], [x + 25 * k, y - 5 * k], [x + 27 * k, y]], .45);
  const stem = oda_torna(x, y - 8 * k, y - 41 * k, 10 * k, [[0, .95], [.12, .55], [.3, .85], [.48, .45], [.78, .38], [.9, .55], [1, .7]]);
  const pan = oda_yol([[x - 18 * k, y - 40 * k], [x - 16 * k, y - 47 * k], [x + 16 * k, y - 47 * k], [x + 18 * k, y - 40 * k]], .45);
  oda_kut(oda_birles(foot, stem, pan), { L, c: [x, y - 24 * k], w: 5 * k, R: 300 * k });
  // mum: kâğıt beyazı sütun, ışıktan uzak yanında ince koyu çizgi; tepede eriyen damla
  const wc = 8 * k, C = oda_yol([[x - wc, y - 46 * k], [x - wc, top + 3 * k], [x - wc * .6, top - 1 * k], [x + wc * .3, top + 2 * k], [x + wc, top - 1 * k], [x + wc, y - 46 * k]], .3);
  GR.fill(C, tone(1), { th: 0, id: 0 });
  tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = Math.max(2.4, 2.2 * k); tx.lineJoin = 'round'; tx.stroke(C);
  if (o.damla !== false) { tx.fillStyle = tone(.03); tx.fill(oda_yol([[x + wc - 1 * k, top + 2 * k], [x + wc + 2 * k, top + 10 * k], [x + wc + 1.5 * k, top + 22 * k], [x + wc - 1.5 * k, top + 18 * k]], .6)); }
  tx.restore();
  // fitil
  oda_cizgi([[x, top + 1 * k], [x + .8 * k, top - 5 * k], [x + 1.5 * k, top - 9 * k]], Math.max(3, 2.6 * k), .03);
  let outer = null;
  if (alev > .02) {
    const hh = (o.ah ?? 66) * k * alev * (1 + .06 * Math.sin(t * 2.3) + .05 * fbm1(t * .9, 4)), ww = (o.aw ?? 21) * k * Math.pow(alev, .7);
    outer = PR.flame(x, top - 3 * k, hh, ww, t, o.seed ?? 4, { speed: .6, frags: false, sway: .45, curl: .35, inner: .6, solidBelow: 400 });
    tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = Math.max(2.4, 1.6 * k); tx.lineJoin = 'round'; tx.stroke(outer); tx.restore();
    oda_cizgi([[x, top - 1 * k], [x + .5 * k, top - 6 * k * alev]], Math.max(3, 2.4 * k), .03);   // alevin dibinde koyu fitil
  }
  return { F, outer, top };
}

// ── masa ──
// x0..x1, y: masa yüzü; L ışık; o: {R, FL}
function oda_masa(x0, x1, y, L, o = {}) {
  const { tx, tone } = GR, FL = o.FL ?? ODA_FL, R = o.R ?? 520, c = [(x0 + x1) / 2, (y + FL) / 2];
  // üst yüz (hafif üstten görünür): mumun dibinde temiz kâğıt, uzakta kararır
  const top = oda_cok([[x0 + 12, y - 13], [x1 - 12, y - 13], [x1, y], [x0, y]]);
  if (L) { const g = tx.createRadialGradient(L[0], L[1], 0, L[0], L[1], R * .75); g.addColorStop(0, tone(1)); g.addColorStop(.42, tone(1)); g.addColorStop(.72, tone(.55)); g.addColorStop(1, tone(.04)); GR.fill(top, g, { th: 0, id: 0 }); }
  else GR.fill(top, tone(.03), { th: 0, id: 0 });
  const slab = oda_dik(x0 - 8, y, x1 - x0 + 16, 18), apron = oda_dik(x0 + 10, y + 18, x1 - x0 - 20, 34);
  const legs = oda_birles(oda_torna(x0 + 26, y + 50, FL, 30), oda_torna(x1 - 26, y + 50, FL, 30), oda_dik(x0 + 26, FL - 74, x1 - x0 - 52, 12));
  oda_kut(oda_birles(apron, legs), { L, c, w: 6, R });
  oda_kut(slab, { L, c: [c[0], y + 9], w: 7, R });
}
// kâğıt, hokka, tüy kalem (masa yüzünde)
function oda_masaUstu(x, y, L, o = {}) {
  const { tx, tone } = GR;
  // kâğıt destesi: üstten görülen ince dörtgen (kâğıt beyazı), kenarında koyu çizgi
  if (o.kagit !== false) {
    const pp = oda_cok([[x - 70, y - 4], [x + 52, y - 4], [x + 64, y - 14], [x - 56, y - 14]]);
    GR.fill(pp, tone(1), { th: 0, id: 0 });
    tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 2.5; tx.stroke(pp); tx.restore();
  }
  if (o.hokka !== false) {
    const hx = x + 108, ink = oda_yol([[hx - 15, y], [hx - 17, y - 14], [hx - 10, y - 24], [hx + 10, y - 24], [hx + 17, y - 14], [hx + 15, y]], .6);
    oda_kut(ink, { L, c: [hx, y - 12], w: 4, R: 500 });
    // tüy: hokkadan geriye eğik yükselen, kâğıt beyazı bayrak + koyu sap
    const q = [[hx - 2, y - 22], [hx - 14, y - 60], [hx - 34, y - 104], [hx - 58, y - 140]];
    const vane = oda_yol([[hx - 8, y - 48], [hx - 26, y - 84], [hx - 50, y - 124], [hx - 64, y - 146], [hx - 46, y - 132], [hx - 22, y - 100], [hx - 4, y - 64]], .7);
    GR.fill(vane, tone(.97), { th: 0, id: 6 });
    tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 2.4; tx.stroke(vane); tx.restore();
    oda_cizgi(q, 3.4, .03, .4);
  }
}

// ── pencere ──
// Çok bölmeli kurşun kafesli pencere (eşkenar dörtgen camlar), taş dikme ve kayıt, ışıklı denizlik.
// o: {x0, y0, x1, y1, mod: 'ay' | 'dis', v (cam tonu), ay: [x, y] (ay), dis: fn(P) (dış görünüşü çizer), sill (denizlik tonu)}
function oda_pencere(t, o) {
  const { tx, tone } = GR, { x0, y0, x1, y1 } = o, P = oda_dik(x0, y0, x1 - x0, y1 - y0);
  if (o.mod === 'dis' && o.dis) o.dis(P);
  else {
    const v = o.v ?? .17;
    // camlar karanlık; yalnız ayın çevresi ay ışığıyla açılır (pencere ikinci, sönük ışık kaynağı: odak mumda kalır)
    const am = o.ay || [(x0 + x1) / 2, y0], g = tx.createRadialGradient(am[0], am[1], 0, am[0], am[1], Math.max(x1 - x0, y1 - y0) * 1.1);
    g.addColorStop(0, tone(.75 * (o.ayV ?? 1))); g.addColorStop(.35, tone(.36 * (o.ayV ?? 1) + v * .3)); g.addColorStop(1, tone(v * .5));
    GR.fill(P, g, { th: 0, id: 1 });
    if (o.ay) {
      tx.save(); tx.clip(P);
      PR.glow(o.ay[0], o.ay[1], 30, 150, 1, .7 * (o.ayV ?? 1));
      tx.fillStyle = tone(1); tx.fill(oda_daire(o.ay[0], o.ay[1], 32));
      tx.restore();
    }
  }
  // kurşun kafes
  tx.save(); tx.clip(P); tx.strokeStyle = tone(.03); tx.lineWidth = o.lw ?? 3.6;
  const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, D = Math.hypot(x1 - x0, y1 - y0), sp = o.sp ?? 52;
  for (const a of [1.05, PI - 1.05]) {
    const d = [Math.cos(a), Math.sin(a)], n = [-d[1], d[0]];
    for (let c = -D; c <= D; c += sp) { tx.beginPath(); tx.moveTo(cx + n[0] * c - d[0] * D, cy + n[1] * c - d[1] * D); tx.lineTo(cx + n[0] * c + d[0] * D, cy + n[1] * c + d[1] * D); tx.stroke(); }
  }
  tx.restore();
  // taş çerçeve, orta dikme, kayıt
  const bw = o.bw ?? 15, mx = (x0 + x1) / 2, ty = y0 + (y1 - y0) * .3;
  const fr = oda_birles(oda_dik(x0 - bw, y0 - bw, x1 - x0 + 2 * bw, bw), oda_dik(x0 - bw, y0, bw, y1 - y0), oda_dik(x1, y0, bw, y1 - y0), oda_dik(mx - 8, y0, 16, y1 - y0), oda_dik(x0, ty - 7, x1 - x0, 14));
  GR.fill(fr, tone(.03), { th: 0, id: 0 });
  // denizlik: üst yüzü dış ışıkla aydınlanır
  const sill = oda_cok([[x0 - bw - 14, y1 + 2], [x1 + bw + 14, y1 + 2], [x1 + bw + 22, y1 + 20], [x0 - bw - 22, y1 + 20]]);
  GR.fill(sill, tone(.03), { th: 0, id: 0 });
  GR.fill(oda_dik(x0 - bw - 12, y1 + 2, x1 - x0 + 2 * bw + 24, 7), tone(o.sill ?? .95), { th: 0, id: 0 });
}

// ── kitap rafı ──
function oda_raf(x0, x1, y0, y1, L, o = {}) {
  const { tone } = GR, r = rng(o.seed || 41), R = o.R ?? 900, rows = o.rows ?? 4, rh = (y1 - y0) / rows;
  const sides = oda_birles(oda_dik(x0 - 16, y0 - 26, 18, y1 - y0 + 26), oda_dik(x1 - 2, y0 - 26, 18, y1 - y0 + 26), oda_dik(x0 - 26, y0 - 34, x1 - x0 + 52, 16));
  for (let i = 0; i < rows; i++) {
    const yb = y0 + (i + 1) * rh, books = [];
    let x = x0 + 8 + r() * 10;
    while (x < x1 - 30) {
      const w = 16 + r() * 22, hh = rh * (.6 + r() * .26), tilt = (x > x1 - 80 && r() < .5) ? .22 : 0;
      if (r() < .1) { x += 14 + r() * 30; continue; }                   // boşluk
      const P = new Path2D(), c = Math.cos(tilt), s = Math.sin(tilt);
      const pts = [[0, 0], [w, 0], [w, -hh], [0, -hh]].map(([a, b]) => [x + a * c - b * s, yb - 14 + a * s + b * c]);
      poly(P, pts, true); books.push([P, [x + w / 2, yb - 14 - hh / 2]]);
      x += w + 1 + r() * 2;
    }
    for (const [P, c] of books) oda_kut(P, { L, c, w: 3.5, R: R * .62, tn: .03 });
    oda_kut(oda_dik(x0 - 4, yb - 14, x1 - x0 + 8, 14), { L, c: [(x0 + x1) / 2, yb - 7], w: 4, R: R * .62 });
  }
  oda_kut(sides, { L, c: [(x0 + x1) / 2, (y0 + y1) / 2], w: 4, R: R * .62 });
}

// ── koltuk (yüksek arkalıklı, 17. yy) ──
// Şairin kalça noktasına göre: o: {x, y, h, f}. parca: 'arka' (arkalık, oturak, ayaklar) ya da 'on' (yakın kol dayanağı)
function oda_koltuk(o, parca, L, R) {
  const h = o.h, f = o.f ?? 1, M = (x, y) => [o.x + f * x * h, o.y + y * h], FLy = o.y + 2.05 * h;
  if (parca === 'arka') {
    const back = oda_yol([[-.98, -3.05], [-.72, -3.15], [-.46, -3.1], [-.4, -.2], [-.86, -.15]].map(p => M(...p)), .3);
    const post = oda_yol([[-.98, -3.25], [-.8, -3.25], [-.66, 2.05], [-.86, 2.05]].map(p => M(...p)), .1);
    const fin = oda_birles(oda_daire(...M(-.89, -3.42), .15 * h), oda_yol([[-.97, -3.52], [-.89, -3.78], [-.81, -3.52]].map(p => M(...p)), .5));
    const seat = oda_yol([[-.9, .2], [1.08, .2], [1.1, .4], [-.9, .4]].map(p => M(...p)), .2);
    const fl = oda_torna(M(.94, 0)[0], o.y + .4 * h, FLy, .3 * h), str = oda_yol([[-.75, 1.55], [.95, 1.55], [.95, 1.68], [-.75, 1.68]].map(p => M(...p)), .2);
    oda_kut(oda_birles(back, post, fin), { L, c: M(-.7, -1.5), w: Math.max(4, .07 * h), R });
    oda_kut(oda_birles(seat, fl, str), { L, c: M(.2, 1), w: Math.max(4, .07 * h), R });
  } else {
    const arm = oda_yol([[-.66, -1.12], [.98, -1.12], [1.16, -1.16], [1.24, -1.06], [1.12, -.97], [-.66, -.98]].map(p => M(...p)), .4);
    const ap = oda_torna(M(.98, 0)[0], o.y - 1.0 * h, o.y + .22 * h, .26 * h, [[0, .5], [.1, .3], [.3, .62], [.5, .3], [.7, .55], [.9, .3], [1, .45]]);
    oda_kut(oda_birles(arm, ap), { L, c: M(.4, -.6), w: Math.max(4, .07 * h), R });
  }
}

// ── şair (oturan, profil) ──
// o: {x, y (oturak: kalça), h (baş boyu), f (+1 sağa bakar), fw (gövde öne eğimi, rad), bas (baş: + yukarı, − öne), kol ('kol' | 'yaz' | 'diz')}
// Saç başla döner ama alt uçları yerçekimiyle sarkar (eğik başta öne savrulmaz).
const ODA_SAC = [[.27, -.42], [.12, -.56], [-.1, -.62], [-.34, -.56], [-.5, -.4], [-.57, -.12], [-.57, .22], [-.54, .56], [-.5, .86], [-.4, .95], [-.25, .9], [-.17, .62], [-.1, .32], [-.05, .08], [.03, -.16], [.16, -.32]];
function oda_basGeo(HC, h, f, al, sacPts = ODA_SAC) {
  const loc = (x, y, a) => { const c = Math.cos(a), s = Math.sin(a), X = x * f * h, Y = y * h; return [HC[0] + X * c - Y * s, HC[1] + X * s + Y * c]; };
  const HL = (x, y) => loc(x, y, al * f), head = oda_yol(ODA_KAFA.map(([x, y]) => HL(x, y)), .55);
  const sac = sacPts ? oda_yol(sacPts.map(([x, y]) => loc(x, y, al * f * (1 - .75 * clamp((y - .05) / .8)))), .85) : null;
  return { head, sac, HL };
}
function oda_sairGeo(o) {
  const h = o.h, f = o.f ?? 1, X = o.x, Y = o.y, th = o.fw ?? 0, hu = o.bas ?? 0;
  const M = (x, y) => [X + f * x * h, Y + y * h], T = p => { const q = oda_rot(p, th); return M(q[0], q[1]); };
  const torsoL = [[-.5, .28], [-.6, -.4], [-.62, -1.2], [-.52, -1.85], [-.3, -2.3], [-.04, -2.52], [.26, -2.46], [.5, -2.2], [.6, -1.7], [.54, -1.15], [.62, -.55], [.68, -.15], [.3, .3]];
  const torso = oda_yol(torsoL.map(T), .8);
  const legsL = [[-.4, .32], [.4, -.36], [1.2, -.42], [1.92, -.42], [2.14, -.26], [2.22, 0], [2.24, .6], [2.21, 1.2], [2.26, 1.62], [1.92, 1.72], [1.58, 1.66], [1.5, 1.1], [1.44, .52], [1.2, .34], [.2, .36]];
  const legs = oda_yol(legsL.map(p => M(...p)), .8);
  const shoe = oda_yol([[1.94, 1.55], [2.2, 1.55], [2.24, 1.82], [2.46, 1.9], [2.6, 1.98], [2.6, 2.05], [1.9, 2.05], [1.88, 1.8]].map(p => M(...p)), .55);
  const pv = oda_rot([.1, -2.5], th), al = th - hu, hc = oda_rot([.12, -.55], al), HC = M(pv[0] + hc[0], pv[1] + hc[1]);
  const B = oda_basGeo(HC, h, f, al);
  const neck = oda_uzuv(T([.06, -2.25]), B.HL(-.02, .38), () => .25 * h, () => .25 * h, 4);
  const yaka = oda_yol([[-.34, -2.34], [-.1, -2.48], [.22, -2.47], [.42, -2.32], [.5, -2.12], [.42, -2.06], [.2, -2.14], [-.04, -2.2], [-.3, -2.22]].map(T), .7);
  // yakın kol
  const kol = o.kol || 'kol', S = T([.0, -2.1]);
  let E, Wr, hand;
  if (kol === 'yaz') { E = M(.5, -1.02); Wr = M(1.4, -.9); hand = [[1.34, -1.0], [1.6, -1.0], [1.76, -.9], [1.72, -.8], [1.4, -.8]]; }
  else if (kol === 'diz') { E = M(.3, -1.18); Wr = M(1.45, -.62); hand = [[1.4, -.74], [1.74, -.68], [1.9, -.5], [1.74, -.42], [1.42, -.5]]; }
  else { E = M(-.24, -1.0); Wr = M(.95, -1.06); hand = [[.88, -1.16], [1.18, -1.15], [1.38, -1.02], [1.44, -.84], [1.32, -.77], [1.14, -.9], [.9, -.94]]; }
  const A = oda_birles(oda_uzuv(S, E, () => .3 * h, () => .27 * h, 8), oda_daire(E[0], E[1], .25 * h), oda_uzuv(E, Wr, u => (.25 - .05 * u) * h, u => (.24 - .05 * u) * h, 8));
  const H = oda_yol(hand.map(p => M(...p)), .7);
  const Bd = oda_birles(torso, legs, shoe, neck, B.sac, B.head);
  // ışık yanındaki ön kontur (vuruşların çıktığı kenar): göğüs, kucak, etek önü
  const on = [[.5, -2.2], [.6, -1.7], [.54, -1.15], [.62, -.55]].map(T).concat([[1.0, -.42], [1.6, -.42], [2.2, .2], [2.22, .9]].map(p => M(...p)));
  return { B: Bd, A, H, yaka, HC, HL: B.HL, head: B.head, sac: B.sac, on, c: M(.3, -1.2), M, T, E, Wr, S };
}
// o: + {L (ışık), R, rw (kenar px), yakaV, vurus (false: beyaz vuruş yok), seed, golge: {k, v, yMax}}
function oda_sair(o) {
  const G = oda_sairGeo(o), h = o.h, L = o.L, R = o.R ?? 620, rw = o.rw ?? Math.max(4, .085 * h);
  if (o.golge && L) oda_golge(oda_birles(G.B, G.A, G.H), L, o.golge.k, o.golge.v, o.golge.yMax);
  oda_kut(G.B, { L, c: G.c, w: rw, R });
  if (L && o.vurus !== false) {
    const d = [G.c[0] - L[0], G.c[1] - L[1]], pts = G.on.filter(p => Math.hypot(p[0] - L[0], p[1] - L[1]) < R * .85);
    if (pts.length > 1) PR.cuts(pts, d, { len: [.25 * h, .8 * h], gap: [.3 * h, .7 * h], w: Math.max(3.8, .055 * h), clip: G.B, bend: -.25, seed: o.seed || 7 });
  }
  // yaka: ışıktaysa kâğıt beyazı (ışıktan uzak yanında koyu bant), değilse koyu
  const yd = L ? Math.hypot(G.HC[0] - L[0], G.HC[1] - L[1]) : 1e9, yv = o.yakaV ?? (yd < R * .8 ? 1 : 0);
  if (yv > .5 && L) oda_acik(G.yaka, { L, c: G.T([.1, -2.2]), w: .16 * h, tn: .97, sv: .04 });
  else oda_kut(G.yaka, { L, c: G.T([.1, -2.2]), w: rw * .8, R, tn: .03 });
  if (o.kolCiz !== false) { oda_kut(G.A, { L, c: G.E, w: rw, R }); oda_kut(G.H, { L, c: G.Wr, w: rw * .8, R }); }
  return G;
}

// ── kız (oturan; beyaz başlık, uzun etek) ──
// o: {x, y (oturak), h, f, fw, bas, kol ('kitap' | 'yaz'), L, R}
const ODA_BASLIK = [[.24, -.46], [.04, -.66], [-.28, -.64], [-.52, -.44], [-.62, -.12], [-.6, .22], [-.48, .4], [-.32, .34], [-.24, .1], [-.1, -.14], [.1, -.28], [.24, -.36]];
function oda_kizGeo(o) {
  const h = o.h, f = o.f ?? 1, X = o.x, Y = o.y, th = o.fw ?? .08, hu = o.bas ?? 0;
  const M = (x, y) => [X + f * x * h, Y + y * h], T = p => { const q = oda_rot(p, th); return M(q[0], q[1]); };
  const torso = oda_yol([[-.42, .05], [-.48, -.7], [-.44, -1.5], [-.3, -2.05], [-.04, -2.26], [.22, -2.2], [.42, -1.95], [.46, -1.55], [.34, -1.1], [.36, -.6], [.5, -.3], [.2, .1]].map(T), .8);
  const etek = oda_yol([[-.5, -.55], [-.64, .4], [-.82, 1.4], [-.96, o.etekY ?? 2.05], [1.98, o.etekY ?? 2.05], [1.86, 1.3], [1.76, .5], [1.72, -.08], [1.5, -.32], [.5, -.44]].map(p => M(...p)), .7);
  const pv = oda_rot([.08, -2.28], th), al = th - hu, hc = oda_rot([.1, -.52], al), HC = M(pv[0] + hc[0], pv[1] + hc[1]);
  const Bg = oda_basGeo(HC, h * .96, f, al, null);
  const loc = (x, y) => { const c = Math.cos(al * f), s = Math.sin(al * f), X2 = x * f * h * .96, Y2 = y * h * .96; return [HC[0] + X2 * c - Y2 * s, HC[1] + X2 * s + Y2 * c]; };
  const baslik = oda_yol(ODA_BASLIK.map(([x, y]) => loc(x, y)), .8);
  const neck = oda_uzuv(T([.04, -2.05]), Bg.HL(-.04, .38), () => .2 * h, () => .2 * h, 4);
  const S = T([.0, -1.9]), kol = o.kol || 'kitap';
  let E, Wr;
  if (kol === 'yaz') { E = M(.42, -1.02); Wr = M(1.25, -1.38 + (o.yazY || 0)); }
  else if (kol === 'kucak') { E = M(.35, -1.0); Wr = M(1.2, -.5); }
  else { E = M(.5, -1.05); Wr = M(1.22, -1.5); }
  const A = oda_birles(oda_uzuv(S, E, () => .22 * h, () => .2 * h, 8), oda_daire(E[0], E[1], .18 * h), oda_uzuv(E, Wr, u => (.18 - .05 * u) * h, u => (.17 - .05 * u) * h, 8), oda_daire(Wr[0], Wr[1], .14 * h));
  return { B: oda_birles(torso, etek, neck, Bg.head), baslik, A, HC, E, Wr, c: M(.4, -.6), M, T };
}
function oda_kiz(o) {
  const G = oda_kizGeo(o), h = o.h, L = o.L, R = o.R ?? 600, rw = o.rw ?? Math.max(4, .085 * h);
  oda_kut(G.B, { L, c: G.c, w: rw, R });
  const lit = L && Math.hypot(G.HC[0] - L[0], G.HC[1] - L[1]) < R * .85;
  if (lit) oda_acik(G.baslik, { L, c: G.HC, w: .2 * h, tn: .97, sv: .04 }); else oda_kut(G.baslik, { L, c: G.HC, w: rw, R });
  oda_kut(G.A, { L, c: G.E, w: rw, R });
  return G;
}

// ── ayakta figür (Londra kalabalığı, cellat, kapıdaki şair, mumla gelen kız) ──
// o: {x, y (ayak), h, f, gen (en çarpanı), palto (etek ucu, baş biriminde; −1,6 diz), etek (true: yere kadar), cuppe (true: bileğe kadar cüppe),
//     sapka: 'yuksek' | 'genis' | 'bere' | 'baslik' | null, sac (true: omuza inen saç), kolN: [omuz açısı, dirsek bükümü], kolF, bas, fw, adim (yürürken salınım)}
function oda_ayaktaGeo(o) {
  const h = o.h, f = o.f ?? 1, g = o.gen ?? 1, X = o.x, Y = o.y, th = o.fw ?? 0, hu = o.bas ?? 0;
  const M = (x, y) => [X + f * x * h, Y + y * h], T = p => { const q = oda_rot([p[0] * g, p[1] + 3.7], th); return M(q[0], q[1] - 3.7); };
  const parts = [];
  const ust = [[-.42, -5.95], [-.52, -5.2], [-.42, -4.4], [-.5, -3.7], [-.4, -3.4], [.42, -3.4], [.44, -3.8], [.48, -4.6], [.52, -5.25], [.34, -5.95]];
  parts.push(oda_yol(ust.map(T), .8));
  if (!o.etek && !o.cuppe) parts.push(oda_yol([[-.5, -3.75], [-.44, -3.0], [-.3, -2.0], [-.36, -1.3], [-.2, -.35], [-.28, 0], [.6, 0], [.56, -.16], [.15, -.38], [.2, -1.2], [.26, -1.95], [.38, -2.9], [.44, -3.8]].map(p => M(p[0] * g, p[1])), .8));
  if (o.palto != null && !o.etek) { const hm = o.palto; parts.push(oda_yol([[-.46, -5.9], [-.56, -4.9], [-.52, -3.9], [-.74, hm], [-.2, hm + .06], [.3, hm + .02], [.8, hm], [.58, -3.9], [.52, -4.9], [.42, -5.7]].map(T), .7)); }
  if (o.cuppe) parts.push(oda_yol([[-.46, -5.9], [-.56, -4.9], [-.58, -3.9], [-.72, -.3], [-.62, 0], [.66, 0], [.74, -.3], [.6, -3.9], [.54, -4.9], [.42, -5.7]].map(T), .7));
  if (o.etek) parts.push(oda_yol([[-.44, -4.3], [-.62, -2.6], [-.96, -.02], [.98, -.02], [.74, -2.6], [.5, -4.3]].map(([x, y]) => M(x * g, y)), .7));
  const pv = oda_rot([.06 * g, -6.0 + 3.7], th), al = th - hu, hc = oda_rot([.1, -.55], al), HC = M(pv[0] + hc[0], pv[1] - 3.7 + hc[1]);
  const Bg = oda_basGeo(HC, h, f, al, o.sac ? ODA_SAC : null);
  parts.push(oda_uzuv(T([.04, -5.8]), Bg.HL(-.02, .38), () => .25 * h * g, () => .25 * h * g, 4), Bg.head);
  if (Bg.sac) parts.push(Bg.sac);
  const loc = (x, y) => { const c = Math.cos(al * f), s = Math.sin(al * f), X2 = x * f * h, Y2 = y * h; return [HC[0] + X2 * c - Y2 * s, HC[1] + X2 * s + Y2 * c]; };
  let sapka = null;
  if (o.sapka === 'yuksek') sapka = oda_birles(oda_yol([[-.44, -.36], [-.38, -1.42], [-.2, -1.5], [.22, -1.48], [.36, -1.4], [.44, -.36]].map(p => loc(...p)), .5), oda_yol([[-.92, -.34], [-.82, -.5], [.84, -.5], [.96, -.34], [.84, -.24], [-.8, -.24]].map(p => loc(...p)), .6));
  else if (o.sapka === 'genis') sapka = oda_birles(oda_yol([[-.42, -.36], [-.36, -1.0], [-.1, -1.08], [.26, -1.04], [.42, -.36]].map(p => loc(...p)), .6), oda_yol([[-1.12, -.16], [-.9, -.44], [.92, -.46], [1.16, -.18], [1.0, -.24], [.0, -.32], [-.96, -.24]].map(p => loc(...p)), .6));
  else if (o.sapka === 'bere') sapka = oda_yol([[-.54, -.12], [-.52, -.56], [-.24, -.78], [.14, -.74], [.4, -.5], [.44, -.3], [.0, -.34]].map(p => loc(...p)), .7);
  else if (o.sapka === 'baslik') sapka = oda_yol([[.26, -.46], [.02, -.7], [-.4, -.62], [-.62, -.2], [-.66, .5], [-.44, .8], [-.1, .66], [-.04, .2], [.12, -.16], [.28, -.3]].map(p => loc(...p)), .8);
  if (sapka) parts.push(sapka);
  // kollar: açı 0 aşağı, + bakış yönü
  const kol = (sh, a) => { if (!a) return [null, null, null]; const S = T(sh), d1 = [Math.sin(a[0]) * f, Math.cos(a[0])], E = [S[0] + d1[0] * 1.38 * h, S[1] + d1[1] * 1.38 * h], a2 = a[0] + a[1], d2 = [Math.sin(a2) * f, Math.cos(a2)], Wr = [E[0] + d2[0] * 1.18 * h, E[1] + d2[1] * 1.18 * h];
    return [oda_birles(oda_uzuv(S, E, () => .24 * h * g, () => .22 * h * g, 8), oda_daire(E[0], E[1], .2 * h * g), oda_uzuv(E, Wr, u => (.2 - .05 * u) * h * g, u => (.19 - .05 * u) * h * g, 8), oda_daire(Wr[0], Wr[1], .15 * h)), E, Wr]; };
  const [AF] = kol([.08, -5.75], o.kolF), [AN, EN, WN] = kol([-.02, -5.72], o.kolN);
  return { B: oda_birles(...parts), AF, AN, EN, WN, HC, HL: Bg.HL, c: M(0, -3.8), M, T };
}
function oda_ayakta(o) {
  const G = oda_ayaktaGeo(o), h = o.h, L = o.L, R = o.R ?? 1e5, rw = o.rw ?? Math.max(3.5, .09 * h);
  if (G.AF) oda_kut(G.AF, { L, c: G.c, w: rw, R });
  oda_kut(G.B, { L, c: G.c, w: rw, R });
  if (G.AN) oda_kut(G.AN, { L, c: G.EN, w: rw, R });
  return G;
}

// ── dize çizgileri (soyut el yazısı satırları; okunur yazı değil) ──
// Bir satır: hafif dalgalı, ortası kalın, uçları sivri kâğıt rengi çizgi; u (0..1) yazılmış kısmı, sil (0..1) sağdan silinen kısım.
// satırı (x, y) çevresinde döndürmek için ton katmanı dönüşümü
function px_rot(x, y, a) { const tx = GR.tx; tx.translate(x, y); tx.rotate(a); tx.translate(-x, -y); }
function oda_satir(x, y, L, u, sil, seed, w = 6.5) {
  const e = u * (1 - sil); if (e < .02) return;
  const r = rng(seed), n = 8, pts = [], a1 = r() * TAU, a2 = r() * TAU, ka = .55;
  for (let i = 0; i <= n; i++) { const s = i / n * e; pts.push([x + s * L, y + (Math.sin(s * L / 38 + a1) * 2.2 + Math.sin(s * L / 17 + a2) * 1.2) * ka]); }
  oda_cizgi(pts, w + 10, .03, .5);   // koyu ayırma payı: taralı zeminde de okunur
  oda_cizgi(pts, w, 1, .5);
}

// ── harfler (P010): süs olarak havada; okunur kelime ya da dinî ibare kurmaz ──
// İbranice, Yunanca, Latince tek harfler; Α–Ω, Χ–Ρ ve tanrı adı harf öbekleri bilerek dışarıda.
const ODA_HARF = ['ב', 'ג', 'ד', 'ל', 'מ', 'נ', 'ק', 'ת', 'פ', 'צ', 'Β', 'Γ', 'Δ', 'Θ', 'Λ', 'Ξ', 'Σ', 'Φ', 'Ψ', 'ζ', 'λ', 'ξ', 'R', 'G', 'Q', 'M', 'D', 'V', 'S', 'B'];
function oda_harf(ch, x, y, px, a, k = 1) {
  if (k <= .05) return;
  const tx = GR.tx; tx.save(); tx.translate(x, y); tx.rotate(a); tx.scale(k, k);
  tx.font = `${/[A-Z]/.test(ch) ? '600 ' + px + 'px "Cormorant Garamond"' : px + 'px FreeSerif'}`; tx.textAlign = 'center'; tx.textBaseline = 'middle';
  tx.lineJoin = 'round'; tx.strokeStyle = GR.tone(.03); tx.lineWidth = px * .2; tx.strokeText(ch, 0, 0);
  tx.fillStyle = GR.tone(1); tx.fillText(ch, 0, 0); tx.restore();
}

// ── açık kitap (masada yatan, önden-yandan): iki sayfa kanadı (kâğıt), ince koyu cilt; dış kenarda sayfa kenarı çizgileri ──
function oda_kitapAcik(x, y, w, L, o = {}) {
  const { tx, tone } = GR, hh = w * .5;
  oda_kut(oda_cok([[x - w * .56, y + 2], [x + w * .56, y + 2], [x + w * .54, y - 8], [x - w * .54, y - 8]]), { L, c: [x, y], w: 3, R: 700 });
  for (const sd of [-1, 1]) {
    const P = oda_yol([[x, y - 6], [x + sd * w * .06, y - hh * .36], [x + sd * w * .26, y - hh * .5], [x + sd * w * .5, y - hh * .4], [x + sd * w * .53, y - hh * .1], [x + sd * w * .52, y - 6]], .45);
    GR.fill(P, tone(.97), { th: 0, id: 0 });
    tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 2.6; tx.lineJoin = 'round'; tx.stroke(P);
    tx.beginPath(); for (const f of [.3, .55]) { tx.moveTo(x + sd * w * (.5 - f * .02), y - hh * (.36 * (1 - f) + .1)); tx.lineTo(x + sd * w * .5, y - 8); } tx.lineWidth = 2.2; tx.stroke();
    tx.restore();
  }
}
// elde tutulan dev kitap: koyu cilt (ışık yanında kenar), sayfa bloğunun kenarı kâğıt beyazı
function oda_kitapElde(x, y, a, s, L) {
  const R = (u, v) => [x + u * Math.cos(a) - v * Math.sin(a), y + u * Math.sin(a) + v * Math.cos(a)];
  oda_kut(oda_cok([[-.5, -.7], [.5, -.7], [.5, .7], [-.5, .7]].map(([u, v]) => R(u * s, v * s))), { L, c: [x, y], w: 5, R: 700 });
  GR.fill(oda_cok([[.5, -.64], [.62, -.6], [.62, .64], [.5, .66]].map(([u, v]) => R(u * s, v * s))), GR.tone(.97), { th: 0, id: 0 });
}

// ═════════════ SET: Milton'ın odası ═════════════
// o: {yer: {sx, sh, mx0, mx1, my, mumX} (yerleşim), mum: {x, y, s, alev, boy} | null, L (ışık; verilmezse mumdan), r0, r1, R (kenar ışığı menzili),
//     pen (pencere seçenekleri | false), raf (false), sair (oda_sair seçenekleri | false), koltuk, masa, masaUstu, arka/orta/on (fn(L))}
const ODA_YER = { sx: 700, sh: 74, mx0: 880, mx1: 1190, my: 672, mumX: 985 };
function cizOda(t, o = {}) {
  const { tone } = GR, FL = o.FL ?? ODA_FL, Y = Object.assign({}, ODA_YER, o.yer || {});
  const mum = o.mum === null ? null : Object.assign({ x: Y.mumX, y: Y.my, s: 1, alev: 1, boy: .6 }, o.mum || {});
  const fl = mum ? oda_mumAlev(mum.x, mum.y, mum.s, mum) : null;
  const L = o.L || (fl && mum.alev > .02 ? fl : null), al = mum ? mum.alev : 1, R = o.R ?? 520;
  GR.fill(oda_dik(-400, FL, W + 800, H - FL + 400), tone(.03), { th: 0, id: 0 });                 // taban
  if (o.ayTaban) GR.fill(oda_cok([[160, FL + 2], [470, FL + 2], [660, H + 20], [300, H + 20]]), tone(.5), { th: 0, id: 0 });
  if (L && o.isik !== false) oda_isik(L[0], L[1], (o.r0 ?? 250) * Math.min(1, al * 1.2), (o.r1 ?? 640) * (.35 + .65 * al), o.isikV ?? 1);
  if (o.isikEk) o.isikEk();
  if (o.pen !== false) oda_pencere(t, Object.assign({ x0: 250, y0: 170, x1: 590, y1: 560, mod: 'ay', ay: [356, 248] }, o.pen || {}));
  if (o.raf !== false) oda_raf(1400, 1800, 240, FL - 160, L, { R: o.rafR ?? 760 });
  if (o.arka) o.arka(L);
  const sa = o.sair === false ? null : Object.assign({ x: Y.sx, y: FL - 2.05 * Y.sh, h: Y.sh, f: 1, bas: .12, fw: -.04, kol: 'kol', L, R: R * 1.1 }, o.sair || {});
  let G = null;
  if (sa) {
    if (o.golge && sa.L) oda_golge(oda_sairGeo(sa).B, sa.L, o.golgeK ?? 1.5, o.golgeV ?? .3, FL - 10);
    if (o.koltuk !== false) oda_koltuk(sa, 'arka', sa.L, sa.R);
    G = oda_sair(Object.assign({}, sa, { kolCiz: false }));
    if (o.koltuk !== false) oda_koltuk(sa, 'on', sa.L, sa.R);
    oda_kut(G.A, { L: sa.L, c: G.E, w: sa.rw ?? Math.max(4, .085 * sa.h), R: sa.R }); oda_kut(G.H, { L: sa.L, c: G.Wr, w: (sa.rw ?? Math.max(4, .085 * sa.h)) * .8, R: sa.R });
  }
  if (o.orta) o.orta(L);
  if (o.masa !== false) oda_masa(Y.mx0, Y.mx1, Y.my, L, { R });
  if (o.masaUstu !== false) oda_masaUstu(Y.mx1 - 105, Y.my, L, o.masaUstu || {});
  let M = null;
  if (mum) M = oda_mum(t, mum.x, mum.y, mum.s, mum);
  if (o.on) o.on(L);
  return { L, G, M, sa, Y };
}

// Mumun yakın planı (P008, P118): masa kenarı, büyük mum; alev gölün alev diliyle aynı biçim (PR.flame, içinde mürekkep vuruşları).
function cizMumYakin(t, o = {}) {
  const { tone } = GR, x = o.x ?? 1560, y = o.y ?? 930, s = o.s ?? 3.1, alev = o.alev ?? 1, boy = o.boy ?? .55;
  const fl = oda_mumAlev(x, y - 22, s, { alev, boy, ah: 60 }), L = alev > .02 ? fl : null;
  GR.fill(oda_dik(-400, y, W + 800, 400), tone(.03), { th: 0, id: 0 });
  if (L) oda_isik(fl[0], fl[1], 170 * Math.min(1, alev * 1.3), (o.r1 ?? 820) * (.3 + .7 * alev));
  // masa kenarı: üst yüz ışıkta
  const top = oda_cok([[-400, y - 22], [W + 400, y - 22], [W + 400, y], [-400, y]]);
  if (L) { const g = GR.tx.createRadialGradient(x, y, 0, x, y, 560); g.addColorStop(0, tone(1)); g.addColorStop(.35, tone(1)); g.addColorStop(.7, tone(.45)); g.addColorStop(1, tone(.04)); GR.fill(top, g, { th: 0, id: 0 }); }
  else GR.fill(top, tone(.03), { th: 0, id: 0 });
  oda_kut(oda_dik(-400, y, W + 800, 36), { L, c: [x, y + 18], w: 8, R: 640 });
  const M = oda_mum(t, x, y - 22, s, { alev, boy, seed: 4, L: o.L, ah: 60, aw: 27 });
  return { L, M, F: fl };
}

// ═════════════ SET: Londra 1660 ═════════════
// Ev siluetleri (cumbalı, üçgen alınlıklı, bacalı); meydanda kitap yakılan ateş; kalabalık (baş-omuz kütleleri); cellat.
function oda_evler(L, r, list, R) {
  const U = new Path2D();
  for (const e of list) {
    const { x, w, y, hg } = e, j = 12 + r() * 10, rh = w * (.45 + r() * .3);
    U.addPath(oda_cok([[x, y], [x, y - hg * .5], [x - j, y - hg * .5], [x - j, y - hg], [x + w / 2, y - hg - rh], [x + w + j, y - hg], [x + w + j, y - hg * .5], [x + w, y - hg * .5], [x + w, y]]));
    if (r() < .75) { const cx = x + w * (.18 + r() * .6), ch = 30 + r() * 34; U.addPath(oda_dik(cx, y - hg - rh * .7 - ch, 20, ch + rh * .5)); }
  }
  oda_kut(U, { L, c: [L[0] + 520, L[1] - 260], w: 6, R });
}
// baş-omuz (arkadan): y omuz çizgisi, s baş boyu; gövde aşağı v = alt (baş biriminde) kadar iner
function oda_bust(x, y, s, f, sapka, sd, alt = 4) {
  const r = rng(sd), M = (u, v) => [x + f * u * s, y + v * s], sw = .95 + r() * .3, ln = (r() - .5) * .18, U = new Path2D();
  U.addPath(oda_yol([[-1.2 * sw, alt], [-1.24 * sw, .9], [-1.12 * sw, .3], [-.7, .06], [-.3, .0], [.3, .0], [.7, .06], [1.12 * sw, .3], [1.24 * sw, .9], [1.2 * sw, alt]].map(p => M(...p)), .6));
  U.addPath(oda_cok([[-.2, -.3], [.2, -.3], [.24, .1], [-.24, .1]].map(p => M(...p))));
  const hc = [ln, -.64], H = (u, v) => M(hc[0] + u, hc[1] + v), hp = [];
  for (let k = 0; k < 16; k++) { const a = k / 16 * TAU; hp.push(H(Math.cos(a) * .36, Math.sin(a) * .47)); }
  U.addPath(oda_yol(hp, .9));
  if (sapka === 'yuksek') { U.addPath(oda_yol([[-.42, -.36], [-.35, -1.38], [-.2, -1.46], [.2, -1.46], [.35, -1.38], [.42, -.36]].map(p => H(...p)), .5)); U.addPath(oda_yol([[-.92, -.34], [-.8, -.48], [.8, -.48], [.92, -.34], [.8, -.24], [-.8, -.24]].map(p => H(...p)), .6)); }
  else if (sapka === 'genis') { U.addPath(oda_yol([[-.4, -.36], [-.34, -.98], [.34, -.98], [.4, -.36]].map(p => H(...p)), .6)); U.addPath(oda_yol([[-1.12, -.14], [-.9, -.42], [.9, -.42], [1.12, -.14], [.96, -.22], [-.96, -.22]].map(p => H(...p)), .6)); }
  else if (sapka === 'bere') U.addPath(oda_yol([[-.46, -.12], [-.44, -.52], [0, -.72], [.44, -.52], [.46, -.12]].map(p => H(...p)), .7));
  else if (sapka === 'baslik') U.addPath(oda_yol([[-.52, .3], [-.56, -.22], [-.34, -.62], [0, -.72], [.34, -.62], [.56, -.22], [.52, .3], [.74, .9], [-.74, .9]].map(p => H(...p)), .7));
  return U;
}
function oda_kalabalik(list, L, R, w, alt) { const U = new Path2D(); let cx = 0, cy = 0; for (const k of list) { U.addPath(oda_bust(k.x, k.y, k.s, k.f ?? 1, k.sp, k.sd ?? Math.round(k.x), alt)); cx += k.x / list.length; cy += k.y / list.length; } oda_kut(U, { L, c: [cx, cy], w, R }); }
// uçuşan sayfa: kâğıt beyazı dörtgen, koyu kenar; kendi ekseninde döner (genişliği kosinüsle daralır: sayfa çevriliyor gibi)
function oda_sayfa(x, y, s, a, flip) {
  const tx = GR.tx, c = Math.cos(a), sn = Math.sin(a), fw = Math.max(.2, Math.abs(Math.cos(flip)));
  const pts = [[-1, -1.3], [1, -1.2], [1.05, 1.3], [-1, 1.25]].map(([u, v]) => { const X = u * s * fw, Y = v * s; return [x + X * c - Y * sn, y + X * sn + Y * c]; });
  const P = oda_cok(pts); GR.fill(P, GR.tone(1), { th: 0, id: 0 });
  tx.save(); tx.strokeStyle = GR.tone(.03); tx.lineWidth = 2.6; tx.lineJoin = 'round'; tx.stroke(P); tx.restore();
}
// o: {tA (son atışta kitabın elden çıktığı an)}
function cizLondra(t, o = {}) {
  const { tx, tone } = GR, FX = o.fx ?? 1010, FY = o.fy ?? 830, GY = 690;
  const fl = 1 + .06 * Math.sin(t * 2.1) + .05 * fbm1(t * .8, 9), L = [FX, FY - 140];
  // gök: ateşle alttan aydınlanan pus
  oda_isik(FX, FY - 150, 0, 960 * fl, .68);
  oda_evler(L, rng(71), [{ x: -40, w: 200, y: GY, hg: 290 }, { x: 178, w: 170, y: GY, hg: 240 }, { x: 362, w: 220, y: GY, hg: 320 }, { x: 604, w: 150, y: GY, hg: 210 },
    { x: 1290, w: 160, y: GY, hg: 220 }, { x: 1470, w: 210, y: GY, hg: 310 }, { x: 1700, w: 240, y: GY, hg: 280 }], 1150);
  // zemin: arnavut kaldırımı; ateşin çevresi aydınlık (yassı ışık)
  const Z = oda_dik(-400, GY, W + 800, H - GY + 400);
  GR.fill(Z, tone(.03), { type: 'persp', y0: GY, D: H - GY, p0: 8, p1: 12, id: 8 });
  tx.save(); tx.clip(Z); tx.translate(FX, FY); tx.scale(1, .32); tx.translate(-FX, -FY); oda_isik(FX, FY, 80, 820 * fl, .95); tx.restore();
  // uzak kalabalık (meydanın öbür yanı): sık, üst üste binen baş-omuzlar, ayakları zemine iner
  const uz = [], r = rng(81);
  for (let x = 80; x < 1860; x += 22 + r() * 26) { if (Math.abs(x - FX) < 120) continue; uz.push({ x, y: GY + 6 + r() * 16, s: 13 + r() * 4, f: x < FX ? 1 : -1, sp: ['yuksek', 'genis', 'bere', 'baslik', null][Math.floor(r() * 5)] }); }
  oda_kalabalik(uz.filter(k => k.x < FX), L, 1250, 3.5, 5.6); oda_kalabalik(uz.filter(k => k.x > FX), L, 1250, 3.5, 5.6);
  // orta sıra (iki yanda)
  const or = [], r2 = rng(82);
  for (const [a, b] of [[40, 560], [1380, 1900]]) for (let x = a; x < b; x += 46 + r2() * 40) or.push({ x, y: GY + 60 + r2() * 26, s: 22 + r2() * 5, f: x < FX ? 1 : -1, sp: ['yuksek', 'genis', 'bere', 'baslik'][Math.floor(r2() * 4)] });
  oda_kalabalik(or.filter(k => k.x < FX), L, 1300, 4.5, 5.6); oda_kalabalik(or.filter(k => k.x > FX), L, 1300, 4.5, 5.6);
  // ateş: çapraz kütükler + yanan düz ciltler + alev öbeği
  const kutuk = oda_birles(...[[-150, -10, 170, -40], [-120, -46, 140, 4], [-60, 0, 90, -70], [-170, -30, 40, -14]].map(([a, b, c, d]) => oda_uzuv([FX + a, FY + b], [FX + c, FY + d], () => 13, () => 13, 4)));
  oda_kut(kutuk, { L: [FX, FY - 80], c: [FX, FY - 20], w: 6, R: 400 });
  PR.flameBank(FX - 190, FX + 190, FY - 10, 340 * fl, t, 21, { n: 6, wr: .5, curl: .7, speed: .6, solidBelow: 500, frags: false, env: f => .35 + .65 * Math.sin(f * PI) });
  // uçuşan sayfalar: ateşten yükselip savrulur (döngü; büyüklük döngü sınırında sıfır)
  for (let i = 0; i < 4; i++) {
    const q = rng(300 + i), ph = q(), sp = .07 + q() * .04, u = (t * sp + ph) % 1, g = Math.sin(PI * u);
    if (g < .3) continue;
    const sd = q() < .5 ? 1 : -.7, x = FX + (q() - .5) * 120 + u * (200 + q() * 260) * sd + Math.sin(t * .8 + i) * 26, y = FY - 260 - u * 470;
    oda_sayfa(x, y, 22 * (.65 + .35 * g), t * (.5 + q() * .6) + i, t * (1.1 + q()) + i);
  }
  // cellat: ateşin solunda; yığından kitap alır, ateşe atar (döngü; son atış tA'da elden çıkar)
  const CX = o.cx ?? 790, CY = FY + 36, cyc = 3.4, tA = o.tA ?? 0, ph = ((t - tA) % cyc + cyc) % cyc, ch = 54;
  // ph 0: bırakma; 0–1,0 takip ve dönüş, 1,2–2,2 yığına eğilip alma, 2,2–3,4 kaldırma, geriye çekme, fırlatma
  const k2 = ks => kf(ph, ks);
  const omuz = k2([[0, 1.55], [1.0, .3], [1.6, .55], [2.2, .45], [3.0, -2.6, E.io2], [3.4, 1.55, E.in2]]), dirsek = k2([[0, .1], [1.0, .25], [2.2, .35], [3.0, -.8], [3.4, .1, E.in2]]);
  const egil = k2([[0, .12], [1.0, .03], [1.6, .3], [2.2, .28], [3.0, -.05], [3.4, .12, E.in2]]);
  const yigin = oda_birles(...[0, 1, 2, 3, 4].map(i => oda_dik(CX - 150 + (i % 2) * 7, CY - 20 - i * 19, 72, 17)));
  oda_kut(yigin, { L, c: [CX - 112, CY - 60], w: 5, R: 900 });
  const Gc = oda_ayakta({ x: CX, y: CY, h: ch, f: 1, gen: 1.22, palto: -2.3, sapka: 'bere', kolN: [omuz, dirsek], kolF: [.35 + egil, .45], fw: egil, L, rw: 6 });
  const kit = (x, y, a) => oda_kut(oda_cok([[-22, -15], [22, -15], [22, 15], [-22, 15]].map(([p, q]) => [x + p * Math.cos(a) - q * Math.sin(a), y + p * Math.sin(a) + q * Math.cos(a)])), { L, c: [x, y], w: 5, R: 900 });
  if (ph > 1.45 || ph < .02) kit(Gc.WN[0], Gc.WN[1], omuz + dirsek);
  else { const u = clamp(ph / .9); if (u < 1) { const x0 = CX + 1.6 * ch, y0 = CY - 7.6 * ch; kit(lerp(x0, FX - 30, u), lerp(y0, FY - 90, u) - Math.sin(PI * u) * 120, u * 5); } }
  // ön kalabalık: kadrajın altından kesilen büyük sırtlar (iki köşede, üst üste binen)
  oda_kalabalik([{ x: 120, y: 900, s: 60, f: 1, sp: 'yuksek' }, { x: 290, y: 950, s: 66, f: 1, sp: 'baslik' }, { x: -10, y: 980, s: 64, f: 1, sp: 'genis' }], L, 1600, 7);
  oda_kalabalik([{ x: 1640, y: 930, s: 64, f: -1, sp: 'genis' }, { x: 1810, y: 890, s: 60, f: -1, sp: 'yuksek' }, { x: 1940, y: 960, s: 66, f: -1, sp: 'bere' }], L, 1600, 7);
  return { L };
}

// ═════════════ ÇEKİMLER ═════════════
// P007 (A06): karanlık oda; koltukta kör şair, önünde mum; yüzü ışığa dönük, gözü yok. Yavaş yaklaşma (1 → 1,18).
plan('P007', (ctx, st) => levha(ctx, camLerp({ cx: 900, cy: 560, z: 1 }, { cx: 880, cy: 560, z: 1.18 }, st.p, E.lin), () => {
  cizOda(st.t, { sair: { bas: .16 } });
}, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// P008 (B01): bölüm kartı "KÖR ŞAİR"; mumun yakın planı: alev, gölün alev diliyle aynı biçim.
plan('P008', (ctx, st) => levha(ctx, null, () => { cizMumYakin(st.t, { r1: 660 }); }, [.03, 0, 1]), {
  tr: { type: 'black', dur: 1.4, end: true },
  over: (ctx, st) => { const a = PA('P008'); chapterCard(ctx, 'KÖR ŞAİR', 'Hiçbir şey göremeyen bir adam,\ncehennemi nasıl bu kadar iyi gördü?', st.t - a + .2, Se('B01') + .5 - a, { x: 590, y: 420 }); } });

// P009 (B02): gece; ay ışığında koltukta şair; başından dize çizgileri yükselir. Kızı mumla gelir, masaya oturur, yazar.
// 'kırk dizeyi'de çizgiler çoğalır, 'yirmiye'de yarısı silinir.
function oda_P009(t) {
  const tK = Wd('B02', 'kızını'), tYz = Wd('B02', 'yazdırırdı'), tKirk = Wd('B02', 'kırk'), tYir = Wd('B02', 'yirmiye'), tD = Wd('B02', 'dizeler');
  const yer = { sx: 600, mx0: 820, mx1: 1130, mumX: 1050 };
  // kızın yolu: sağdan girer (mum elinde), masanın sağına oturur
  const yu = oda_u(t, tK - .3, tYz - .1), gel = E.io2(yu), otur = E.io2(oda_u(t, tYz - .25, tYz + .45)), bob = Math.sin(yu * PI * 6) * 3 * (1 - otur);
  const kx = lerp(1760, 1290, gel), masada = t > tYz - .2;
  const elG = oda_ayaktaGeo({ x: kx, y: ODA_FL + bob, h: 60, f: -1, etek: true, kolN: [.75, 1.05], fw: .04 }), elMum = oda_mumAlev(elG.WN[0], elG.WN[1] + 8, .9, { boy: .8 });
  const L = masada ? oda_mumAlev(1050, ODA_YER.my, 1, { boy: .8 }) : (t > tK - .5 ? elMum : null);
  const ayL = [310, 340];
  return cizOda(t, {
    yer, mum: masada ? { boy: .8 } : null, L: L || ayL, isik: !!L, r1: 640, R: L ? 520 : 10, rafR: L ? 640 : 10,
    isikEk: () => { const a = 1 - .55 * (L ? 1 : 0); oda_isik(310, 360, 60, 560, .62 * a); }, ayTaban: true, masaUstu: masada ? {} : false,
    pen: { x0: 150, y0: 170, x1: 470, y1: 540, ay: [250, 248] },
    sair: { bas: .2, fw: -.05, L: L || ayL, R: L ? 600 : 1400, rw: L ? 6 : 4, vurus: !!L },
    on: () => {
      if (!masada) {
        // mumu göğüs hizasında, bükük kolla önünde taşır; mumluk elin içinde
        const G = oda_ayaktaGeo({ x: kx, y: ODA_FL + bob, h: 60, f: -1, etek: true, sapka: 'baslik', kolN: [.75, 1.05], kolF: [.5, .9], bas: -.05, fw: .04 });
        if (L) oda_ayakta({ x: kx, y: ODA_FL + bob, h: 60, f: -1, etek: true, sapka: 'baslik', kolN: [.75, 1.05], kolF: [.5, .9], bas: -.05, L: elMum, R: 600, rw: 6, fw: .04 });
        if (t > tK - .5) oda_mum(t, G.WN[0], G.WN[1] + 8, .9, { boy: .8 });
      } else {
        const yz = Math.sin((t - tYz) * 7) * .5 + .5;
        oda_kut(oda_cok([[1196, ODA_FL], [1204, 768], [1286, 768], [1294, ODA_FL]]), { L, c: [1245, 840], w: 5, R: 520 });   // tabure
        oda_kiz({ x: 1245 + 20 * (1 - otur), y: 758 + 26 * (1 - otur), h: 60, f: -1, kol: 'yaz', yazY: t > tYz + .5 ? yz * .07 : 0, bas: -.2, fw: .14, L, R: 520 });
      }
      // dize çizgileri: başın üstünde yükselen yığın; yeni satır alttan girer, eskiler yukarı kayar
      const n0 = (t - tD) / 1.15, n = Math.max(0, Math.min(t < tKirk ? n0 : Math.min(n0, 8.5) + (t - tKirk) / .17, 12.6));
      // satırlar başın üstünden sağa-yukarı eğik bir sütun hâlinde yükselir (yatay taramadan açıyla ve koyu payla ayrılır)
      const base = 420, sp = 30, X0 = 560, sil = oda_u(t, tYir, tYir + 1.0), tx = GR.tx;
      for (let i = 0; i < Math.ceil(n); i++) {
        const k = n - 1 - i, yy = base - k * sp; if (yy < 108) continue;
        const q = rng(500 + i), L2 = 150 + q() * 190, sl = i % 2 === 1 ? clamp(sil * 2.2 - (i % 6) * .18) : 0, x = X0 + k * 16 + q() * 30;
        tx.save(); px_rot(x, yy, -.16); oda_satir(x, yy, L2, clamp((n - i) * 1.4), sl, 900 + i, 7); tx.restore();
      }
    }
  });
}
plan('P009', (ctx, st) => levha(ctx, null, () => { oda_P009(st.t); }, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// P010 (B03): iki kız masada dev kitaplardan sesli okur; harfler kitaplardan dökülüp babaya doğru süzülür; sonda başları öne düşer.
function oda_P010(t) {
  const tI = Wd('B03', 'ibranice'), tSon = Wd('B03', 'dayanılmaz'), dus = E.io2(oda_u(t, tSon - .2, tSon + .9));
  return cizOda(t, {
    mum: { x: 1010 }, r1: 660, pen: { x0: 250, y0: 170, x1: 590, y1: 560, ay: [356, 248] }, rafR: 600,
    sair: { bas: .05, fw: -.06, kol: 'kol' }, masaUstu: false,
    orta: L => { // arka kız: masanın sağ ucunun arkasında, dev kitabı elinde tutar
      const G = oda_kizGeo({ x: 1420, y: 730, h: 54, f: -1, kol: 'kitap', bas: lerp(-.15, -.62, dus), fw: lerp(.12, .3, dus) });
      oda_kiz({ x: 1420, y: 730, h: 54, f: -1, kol: 'kitap', bas: lerp(-.15, -.62, dus), fw: lerp(.12, .3, dus), L, R: 640 });
      oda_kitapElde(G.Wr[0] - 6, G.Wr[1] - 22, -.35 - .5 * dus, 62, L);
    },
    on: L => {
      oda_kitapAcik(1150, ODA_YER.my - 13, 190, L);
      oda_kiz({ x: 1290, y: 760, h: 60, f: -1, kol: 'kitap', bas: lerp(-.15, -.62, dus), fw: lerp(.12, .32, dus), L, R: 640 });
      // harfler: kitaplardan yükselir, babaya doğru süzülür; aralıklı evreler (üst üste binmez)
      const on = oda_u(t, tI - 1.2, tI), son = 1 - oda_u(t, tSon, tSon + 1.2);
      for (let i = 0; i < 10; i++) {
        const q = rng(700 + i), dil = i % 3, ch = ODA_HARF[dil * 10 + Math.floor(q() * 10)];
        const u = ((t - S('B03')) * .1 + i / 10 + q() * .03) % 1, g = Math.sin(PI * u), k = clamp(g * 4);
        if (k * on * son < .3) continue;
        const src = i % 2 ? [1150, 600] : [1370, 600], x = lerp(src[0], 840 - q() * 80, u), y = src[1] - Math.sin(PI * u) * (230 + q() * 110) + u * 30;
        oda_harf(ch, x, y, 64 + q() * 10, (q() - .5) * .4, k * on * son);
      }
    }
  });
}
plan('P010', (ctx, st) => levha(ctx, camLerp({ cx: 1000, cy: 540, z: 1.06 }, { cx: 1040, cy: 540, z: 1.06 }, st.p, E.lin), () => { oda_P010(st.t); }, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// P011 (B04): Londra, 1660: meydanda cellat kitapları ateşe atıyor; kalabalık; sayfalar savrulur.
plan('P011', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 960, cy: 560, z: 1.08 }, st.p, E.lin), () => {
  cizLondra(st.t, { tA: Wd('B04', 'ateşe') + .2 });
}, [.03, 0, 1]), { tr: { type: 'fade', dur: 1.0 }, over: (ctx, st) => etiket(ctx, 'LONDRA, 1660', 300, 110, st.lt - .6, st.d - .4, { px: 44 }) });

// P012 (B04@yazarı): karanlık odada, aralık kalmış kapının ardında saklanan şair. Kapı aralığından giren ateş ışığı (dikey yarık)
// odaya yelpaze gibi yayılır; yüzünü ve önünü yalayıp titrer. Gözü çizilmez (boş bakış).
function oda_P012(t) {
  const { tx, tone } = GR, FL = 960, fk = clamp(.55 + .3 * noise1(t * 3.1, 3) + .15 * Math.sin(t * 7.3)), SX = 1250, L = [SX, 520];
  // yarıktan yayılan ışık: duvarda yatay yelpaze (yatay tarama), tabanda ince şerit
  tx.save(); tx.clip(oda_dik(-400, -400, SX + 400, 2000)); tx.translate(SX, 540); tx.scale(1.25, .85); tx.translate(-SX, -540); oda_isik(SX, 540, 70 + 20 * fk, 760 + 60 * fk, .82 + .1 * fk); tx.restore();
  GR.fill(oda_dik(-400, FL, W + 800, 400), tone(.03), { th: 0, id: 0 });
  const g = tx.createLinearGradient(0, FL, 0, H); g.addColorStop(0, tone(1)); g.addColorStop(1, tone(.5));
  GR.fill(oda_cok([[SX - 14, FL], [SX + 14, FL], [SX - 260, H + 20], [SX - 520, H + 20]]), g, { th: 0, id: 0 });
  // kapı kasası (yarığın solu) ve aralık kalmış kanat (sağı): koyu, ışığa bakan kenarlarında ince ışık
  oda_kut(oda_birles(oda_dik(SX - 70, 100, 56, FL - 100), oda_dik(SX - 70, 70, 560, 40)), { L, c: [SX - 42, 500], w: 0 });
  oda_kut(oda_cok([[SX + 14, 110], [SX + 420, 60], [SX + 420, FL + 60], [SX + 14, FL]]), { L: [SX - 200, 520], c: [SX + 200, 520], w: 7 + 3 * fk });
  // yarık: temiz kâğıt (karenin en parlak yeri), genişliği alevle titrer
  const yw = 11 + 4 * fk; GR.fill(oda_cok([[SX - yw, 110], [SX + yw * .6, 110], [SX + yw * .6, FL], [SX - yw, FL]]), tone(1), { th: 0, id: 0 });
  // şair: yarığa dönük, öne eğilmiş; eli kasada; ön yüzü yarığın ışığında
  const G = oda_ayaktaGeo({ x: 1040, y: FL + 6, h: 90, f: 1, cuppe: true, sac: true, kolN: [1.75, .55], kolF: [.25, .5], bas: .04, fw: .09 });
  const w = 10 + 6 * fk;
  oda_kut(G.B, { L, c: G.c, w, R: 1200 }); oda_kut(G.AN, { L, c: G.EN, w: w * .8, R: 1200 });
  const yk = oda_yol([[-.34, -5.82], [-.1, -5.98], [.24, -5.96], [.44, -5.82], [.52, -5.62], [.42, -5.56], [.2, -5.64], [-.04, -5.7], [-.3, -5.72]].map(p => G.T(p)), .7);
  oda_acik(yk, { L, c: G.T([.1, -5.75]), w: 9, tn: .97, sv: .04 });
}
plan('P012', (ctx, st) => levha(ctx, null, () => { oda_P012(st.t); }, [.03, 0, 1]), { tr: { type: 'cut' } });

// P013 (B05): masada büyüyen el yazması yığını; mum solda; "1667". Sonda ("bitirdi") şairin eli bitmiş yığının üstüne konur.
function oda_P013(t) {
  const { tx, tone } = GR, y = 860, t0 = S('B05'), t1 = Wd('B05', 'bitirdi');
  const L = oda_mumAlev(430, y - 40, 1.9, { boy: .5 });
  oda_isik(L[0], L[1], 160, 620);
  // masa yüzü: ışıkta temiz kâğıt bandı, uzakta kararır; ön kenar koyu
  const top = oda_cok([[-200, y], [W + 200, y], [W + 200, y - 70], [-200, y - 70]]);
  const g = tx.createLinearGradient(L[0], 0, L[0] + 1200, 0); g.addColorStop(0, tone(1)); g.addColorStop(.3, tone(.95)); g.addColorStop(.62, tone(.4)); g.addColorStop(.85, tone(.05));
  GR.fill(top, g, { th: 0, id: 0 });
  oda_kut(oda_dik(-200, y, W + 400, 300), { L, c: [L[0], y + 60], w: 9, R: 1200 });
  // yığın: n sayfa; tepe sayfası salınarak düşer ve yerine oturur
  const p = oda_u(t, t0 + .3, t1 + .2), n = 8 + 46 * E.io2(p), k = Math.floor(n), fu = n - k, th = 4.6, X = 1170, Y = y - 34, w = 300, sy = Y - k * th;
  const sp = []; for (let yy = Y; yy > sy + 1; yy -= 11) { const q = rng(Math.round(yy * 3)); sp.push([[X - w / 2 + (q() - .5) * 9, yy], [X + w / 2 + (q() - .5) * 11, yy]]); }
  sp.push([[X - w / 2, sy], [X + w / 2, sy]]);
  const side = oda_cok([...sp.map(q => q[1]), ...sp.map(q => q[0]).reverse()]);
  const gs = tx.createLinearGradient(X - w / 2, 0, X + w / 2, 0); gs.addColorStop(0, tone(1)); gs.addColorStop(.7, tone(.97)); gs.addColorStop(1, tone(.8));
  GR.fill(side, gs, { th: 0, id: 0 });
  tx.save(); tx.clip(side); tx.strokeStyle = tone(.03); tx.lineWidth = 2.4; tx.lineCap = 'round';
  for (let yy = Y - 12; yy > sy + 6; yy -= 15) { const q = rng(Math.round(yy)); tx.beginPath(); tx.moveTo(X - w / 2 + 8 + q() * 40, yy + q() * 2); tx.lineTo(X + w / 2 - 10 - q() * 50, yy + q() * 2); tx.stroke(); }
  tx.restore();
  tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 3; tx.lineJoin = 'round'; tx.stroke(side); tx.restore();
  const ustY = (yy) => oda_cok([[X - w / 2, yy], [X + w / 2, yy], [X + w / 2 + 22, yy - 20], [X - w / 2 + 22, yy - 20]]);
  const U = ustY(sy); GR.fill(U, tone(1), { th: 0, id: 0 }); tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 2.6; tx.lineJoin = 'round'; tx.stroke(U); tx.restore();
  // düşen sayfa: el yazısı satırlarıyla, hafif eğik, salınarak iner
  if (p < 1 && fu > .02) {
    const u = E.out3(fu), yy = sy - th - (1 - u) * 170, dx = Math.sin(fu * 5) * 26 * (1 - u), a = (1 - u) * .18 * Math.sin(fu * 4 + 1), d = 20 + 50 * (1 - u);
    const pts = [[-w / 2, 0], [w / 2, 0], [w / 2 + 22, -d], [-w / 2 + 22, -d]].map(([u2, v]) => [X + dx + u2 * Math.cos(a) - v * Math.sin(a), yy + u2 * Math.sin(a) + v * Math.cos(a)]);
    const P = oda_cok(pts); GR.fill(P, tone(1), { th: 0, id: 0 }); tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 2.6; tx.lineJoin = 'round'; tx.stroke(P); tx.restore();
    if (d > 44) for (let i = 0; i < 3; i++) { const f = (i + 1) / 4, s0 = [lerp(pts[0][0], pts[3][0], f), lerp(pts[0][1], pts[3][1], f)], e0 = [lerp(pts[1][0], pts[2][0], f), lerp(pts[1][1], pts[2][1], f)];
      oda_cizgi([[lerp(s0[0], e0[0], .12), lerp(s0[1], e0[1], .12)], [lerp(s0[0], e0[0], .5), lerp(s0[1], e0[1], .5) + 1], [lerp(s0[0], e0[0], .8 - i * .08), lerp(s0[1], e0[1], .8 - i * .08)]], 3.4, .03, .4); }
  }
  oda_masaUstu(1420, y - 34, L, { hokka: true, kagit: false });
  oda_mum(t, 430, y - 40, 1.9, { boy: .5, seed: 6 });
  // şairin eli: "bitirdi"de sağdan gelir, bitmiş yığının üstüne konar
  const e = E.io2(oda_u(t, t1 - .9, t1 + .3));
  if (e > .01) {
    // kol (geniş cüppe yeni), beyaz kolluk, yığının üstüne düz konmuş el; başparmak ön kenardan sarkar
    const Wr = [lerp(W + 160, X + 60, e), sy - 22], Sh = [Wr[0] + 520, Wr[1] - 150];
    const kol = oda_uzuv(Sh, Wr, u => 66 - 20 * u, u => 60 - 18 * u, 10);
    const el = oda_yol([[Wr[0] + 8, Wr[1] - 22], [Wr[0] - 40, Wr[1] - 20], [Wr[0] - 96, Wr[1] - 8], [Wr[0] - 118, Wr[1] - 1], [Wr[0] - 112, Wr[1] + 3], [Wr[0] - 34, Wr[1] + 4], [Wr[0] - 22, Wr[1] + 26], [Wr[0] - 6, Wr[1] + 30], [Wr[0] + 10, Wr[1] + 8]], .7);
    oda_kut(oda_birles(kol, el), { L, c: Wr, w: 12, R: 1300 });
    const ka = Math.atan2(Sh[1] - Wr[1], Sh[0] - Wr[0]), cx = Wr[0] + Math.cos(ka) * 34, cy = Wr[1] + Math.sin(ka) * 34, nx = -Math.sin(ka), ny = Math.cos(ka);
    const kolluk = oda_cok([[cx - nx * 46, cy - ny * 46], [cx + nx * 44, cy + ny * 44], [cx + nx * 44 + Math.cos(ka) * 16, cy + ny * 44 + Math.sin(ka) * 16], [cx - nx * 46 + Math.cos(ka) * 16, cy - ny * 46 + Math.sin(ka) * 16]]);
    oda_acik(kolluk, { L, c: [cx, cy], w: 7, tn: .97, sv: .04 });
  }
}
plan('P013', (ctx, st) => levha(ctx, null, () => { oda_P013(st.t); }, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => etiket(ctx, '1667', 1620, 170, st.lt - .5, st.d - .3, { px: 52 }) });

// P014 (B06): şairin profili karanlıkta; arkasındaki pencerede mevsimler geçer (kar, bahar çiçeği, yaz gülü); ışık ona ulaşmaz.
function oda_mevsimDis(t, P, x0, y0, x1, y1, m) {
  // m: {kar, yaprak, cicek, gul, gunes (−1..1 konum; null), gok (gök tonu)}
  const { tx, tone } = GR;
  const sx = m.gunes == null ? null : lerp(x0 + 40, x1 - 40, (m.gunes + 1) / 2), syy = m.gunes == null ? 0 : y1 - 70 - Math.sin((m.gunes + 1) / 2 * PI) * (y1 - y0 - 200);
  GR.fill(P, tone(m.gok), { th: 0, id: 1 });
  tx.save(); tx.clip(P);
  if (sx != null) { const gg = tx.createRadialGradient(sx, syy, 0, sx, syy, 240); gg.addColorStop(0, tone(1)); gg.addColorStop(.2, tone(1)); gg.addColorStop(.24, tone(m.gok * .7)); gg.addColorStop(1, tone(m.gok)); tx.fillStyle = gg; tx.fillRect(x0, y0, x1 - x0, y1 - y0); }
  // dal: sağdan giren, sola incelen koyu dal + üç sürgün
  const dal = [[x1 + 40, y0 + 90], [x1 - 110, y0 + 130], [x1 - 250, y0 + 200], [x0 + 190, y0 + 236], [x0 + 60, y0 + 300], [x0 - 10, y0 + 330]];
  oda_cizgi(dal, 26, .03, .25);
  const sur = [[[x1 - 140, y0 + 126], [x1 - 190, y0 + 64], [x1 - 214, y0 + 10]], [[x0 + 270, y0 + 226], [x0 + 236, y0 + 316], [x0 + 256, y0 + 392]], [[x1 - 60, y0 + 106], [x1 - 40, y0 + 190], [x1 - 70, y0 + 250]]];
  for (const s2 of sur) oda_cizgi(s2, 12, .03, .4);
  const dug = [[x1 - 74, y0 + 100], [x1 - 196, y0 + 162], [x1 - 300, y0 + 214], [x0 + 210, y0 + 236], [x0 + 110, y0 + 262], [x1 - 214, y0 + 14], [x0 + 254, y0 + 388], [x1 - 70, y0 + 248], [x0 + 236, y0 + 312]];
  if (m.kar > .02) for (let i = 0; i < dal.length - 1; i++) { const a = dal[i], b = dal[i + 1], w2 = 22 * m.kar, mx = lerp(a[0], b[0], .5), my = lerp(a[1], b[1], .5);
    const P2 = oda_yol([[a[0], a[1] - 8], [mx, my - 9 - w2 * .6], [b[0], b[1] - 8], [mx, my - 4]], .7); tx.fillStyle = tone(1); tx.fill(P2); tx.strokeStyle = tone(.03); tx.lineWidth = 2.6; tx.stroke(P2); }
  dug.forEach(([x, y], i) => {
    const q = rng(80 + i);
    if (m.yaprak > .02) for (const sd of [-1, 1]) { const s = 34 * m.yaprak * (.85 + q() * .3), a = (sd < 0 ? -2.2 : .6) + (q() - .5) * .6; const P2 = oda_yol([[0, 0], [s * .5, -s * .3], [s, 0], [s * .5, s * .3]].map(([u, v]) => [x + u * Math.cos(a) - v * Math.sin(a), y + u * Math.sin(a) + v * Math.cos(a)]), .8); GR.fill(P2, tone(.03), { th: 0, id: 0 }); }
    if (m.cicek > .02 && i % 3 !== 2) { const s = 19 * m.cicek; tx.strokeStyle = tone(.03); tx.lineWidth = 2.6; tx.fillStyle = tone(1); for (let k = 0; k < 5; k++) { const a = k / 5 * TAU + q(); const P2 = oda_daire(x + Math.cos(a) * s * .6, y + Math.sin(a) * s * .6, s * .5); tx.fill(P2); tx.stroke(P2); } tx.fillStyle = tone(.03); tx.fill(oda_daire(x, y, s * .22)); }
  });
  if (m.gul > .02) { // yaz gülü: tek büyük çiçek, sarmal taç yaprakları
    const [x, y] = dug[3], s = 46 * m.gul; tx.fillStyle = tone(1); const P2 = oda_daire(x, y, s); tx.fill(P2); tx.strokeStyle = tone(.03); tx.lineWidth = 3.2; tx.stroke(P2);
    for (let k = 0; k < 3; k++) { tx.beginPath(); tx.arc(x + (k - 1) * s * .08, y + (k - 1) * s * .06, s * (.76 - k * .22), .4 + k * 1.7, 2.9 + k * 1.7); tx.stroke(); }
  }
  tx.restore();
}
function oda_P014(t) {
  const { tx, tone } = GR, FL = ODA_FL, x0 = 380, y0 = 150, x1 = 880, y1 = 610;
  const tM = Wd('B06', 'mevsimler'), tSab = Wd('B06', 'sabah'), tAk = Wd('B06', 'akşam'), tBah = Wd('B06', 'bahar'), tGul = Wd('B06', 'gülü'), tYuz = Wd('B06', 'yüzü');
  const kar = 1 - oda_u(t, tM, tM + 1.4), yaprak = E.io2(oda_u(t, tM + .8, tM + 2.4)) * (1 - .3 * oda_u(t, tGul + .4, tGul + 1.4));
  const cicek = E.out3(oda_u(t, tBah - .2, tBah + .8)) * (1 - oda_u(t, tGul - .2, tGul + .6)), gul = E.out3(oda_u(t, tGul - .3, tGul + .7));
  const gu = oda_u(t, tSab - .4, tAk + 1.2), gunes = gu > 0 && gu < 1 ? lerp(-1, 1, gu) : null;
  const gok = lerp(.5, .82, oda_u(t, tM, tM + 1.6));
  const isik = lerp(.55, 1, oda_u(t, tM, tM + 1.6)) * (1 - .3 * oda_u(t, tYuz, tYuz + 1.2));
  const L = [(x0 + x1) / 2, y0 + 140];
  // pencereden düşen ışık: tabanda dörtgen leke; şairin ayağına varmadan biter (ışık ona ulaşmaz)
  tx.save(); tx.translate(630, 420); tx.scale(.74, 1); tx.translate(-630, -420); oda_isik(630, 420, 0, 1050, .5 * isik); tx.restore();   // pencereden duvara sızan loş ışık: şairin silueti bunun önünde okunur
  GR.fill(oda_dik(-400, FL, W + 800, H - FL + 400), tone(.03), { th: 0, id: 0 });
  const leke = oda_cok([[x0 + 30, FL + 2], [x1 - 30, FL + 2], [x1 + 150, H + 20], [x0 + 210, H + 20]]);
  const gl = tx.createLinearGradient(0, FL, 0, H); gl.addColorStop(0, tone(1 * isik)); gl.addColorStop(1, tone(.55 * isik));
  GR.fill(leke, gl, { th: 0, id: 0 });
  oda_pencere(t, { x0, y0, x1, y1, mod: 'dis', dis: P => oda_mevsimDis(t, P, x0, y0, x1, y1, { kar, yaprak, cicek, gul, gunes, gok }), sp: 64, sill: .97 });
  // şair: sağda, profili pencereye dönük ama bakmıyor; ışık yalnız profilinin ince kenarına değer (koltuk karanlıkta)
  const sa = { x: 1330, y: FL - 2.05 * 90, h: 90, f: -1, bas: .1, fw: -.03, kol: 'kol', L, R: 1600, rw: 6, vurus: false, yakaV: 0 };
  oda_koltuk(sa, 'arka', null, 1);
  const G = oda_sair(Object.assign({}, sa, { kolCiz: false }));
  oda_koltuk(sa, 'on', null, 1);
  oda_kut(G.A, { L, c: G.E, w: 4.5, R: 1600 }); oda_kut(G.H, { L, c: G.Wr, w: 4, R: 1600 });
}
plan('P014', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 1000, cy: 540, z: 1.06 }, st.p, E.lin), () => { oda_P014(st.t); }, [.03, 0, 1]), {
  tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => quote(ctx, '“…ama bana gün dönmez.”', 1430, 170, st.t - Wd('B06', 'ama'), { px: 66, kaynak: 'KAYIP CENNET · III. 41–42' }) });

// P044 (E04@destan): kısa ara: şair karanlık odada, başı öne eğik; mum kısalmış.
plan('P044', (ctx, st) => levha(ctx, { cx: 860, cy: 600, z: 1.12 }, () => {
  cizOda(st.t, { mum: { boy: .35 }, r1: 640, sair: { bas: -.55, fw: .14 } });
}, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// P067 (G02b): gündüz; genç Milton pencere önünde yazıyor (gözleri görüyor). Açık, aydınlık kare (cennet tarifi): ışık içeri dolar.
function oda_P067(t) {
  const { tx, tone } = GR, FL = ODA_FL, x0 = 300, y0 = 130, x1 = 760, y1 = 600, dol = E.io2(oda_u(t, S('G02b'), S('G02b') + 2.2));
  const SUN = [(x0 + x1) / 2, y0 + 140];
  const g = tx.createRadialGradient(SUN[0], SUN[1], 0, SUN[0], SUN[1], 1700);
  g.addColorStop(0, tone(1)); g.addColorStop(lerp(.12, .3, dol), tone(1)); g.addColorStop(lerp(.3, .5, dol), tone(.8)); g.addColorStop(.78, tone(.5)); g.addColorStop(1, tone(.3));
  GR.fill(oda_dik(-400, -400, W + 800, FL + 400), g, { type: 'rad', cx: SUN[0], cy: SUN[1], id: 1 });
  GR.fill(oda_dik(-400, FL, W + 800, 400), tone(.22), { th: 0, id: 0 });
  GR.fill(oda_cok([[x0 + 10, FL + 2], [x1 - 10, FL + 2], [x1 + 330, H + 10], [x0 + 330, H + 10]]), tone(lerp(.75, 1, dol)), { th: 0, id: 0 });
  oda_pencere(t, { x0, y0, x1, y1, mod: 'dis', sp: 60, dis: P => { GR.fill(P, tone(.97), { type: 'rad', cx: SUN[0], cy: SUN[1], id: 1 }); tx.save(); tx.clip(P); oda_cizgi([[x1 + 40, y0 + 330], [x1 - 140, y0 + 350], [x0 + 130, y0 + 430], [x0 - 20, y0 + 440]], 20, .03, .25); oda_cizgi([[x1 - 200, y0 + 352], [x1 - 250, y0 + 290], [x1 - 260, y0 + 240]], 9, .03, .4); tx.restore(); } });
  const L = SUN, mx0 = 760, mx1 = 1080, my = 690;
  const sa = { x: 1230, y: FL - 2.05 * 76, h: 76, f: -1, bas: -.42, fw: .2, kol: 'yaz' };
  oda_koltuk(sa, 'arka', L, 3000);
  const G = oda_sairGeo(sa);
  oda_kut(G.B, { L, c: G.c, w: 9, tn: .06, R: 3000 });
  // yüz: ışığa bakan baş açık (kâğıt), saç orta ton; göz: kâğıda bakan ince koyu çizgi (gözleri görüyor)
  oda_acik(G.head, { L, c: G.HC, w: 7, tn: .97, sv: .08 });
  oda_kut(G.sac, { L, c: G.HC, w: 6, tn: .3, hs: { th: 1.2, id: 0 }, R: 3000 });
  oda_cizgi([G.HL(.18, -.05), G.HL(.25, -.03), G.HL(.32, -.05)], 3.4, .03, .5);
  oda_acik(G.yaka, { L, c: G.T([.1, -2.2]), w: 9, tn: .97, sv: .08 });
  oda_masa(mx0, mx1, my, L, { R: 3000 });
  oda_masaUstu(930, my, L, { hokka: true });
  oda_kut(G.A, { L, c: G.E, w: 8, R: 3000 }); oda_acik(G.H, { L, c: G.Wr, w: 6, tn: .97, sv: .08 });
  oda_cizgi([G.M(1.66, -.84), G.M(1.8, -1.1), G.M(1.98, -1.48)], 4, .03, .5);    // kalem
}
plan('P067', (ctx, st) => levha(ctx, { cx: 900, cy: 520, z: 1.05 }, () => { oda_P067(st.t); }, [.9, 0, 1]), { tr: { type: 'fade', dur: 1.0 } });

// P118 (K04): mum söner; ince duman yükselir; "1674".
function oda_P118(t) {
  const tS = Wd('K04', 'milton'), alev = 1 - E.in2(oda_u(t, tS - .3, tS + .45));
  const R = cizMumYakin(t, { alev, boy: .3 });
  if (alev < .99) { // duman: fitilden yükselen, kıvrılan ince kâğıt rengi şerit; yükseldikçe incelir ve söner
    const u = oda_u(t, tS, tS + 4.5), top = R.M.top, x = 1560 + 1.5 * 3.1, pts = [];
    for (let i = 0; i <= 9; i++) { const f = i / 9, yy = top - 10 - f * (90 + 420 * E.out2(u)); pts.push([x + Math.sin(f * 5 - t * 1.1) * (8 + f * 46) - f * 30, yy]); }
    const w = 11 * (1 - .6 * u); if (w > 3) oda_cizgi(pts, w, 1, .7);
  }
}
plan('P118', (ctx, st) => levha(ctx, null, () => { oda_P118(st.t); }, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => etiket(ctx, '1674', 700, 360, st.t - Wd('K04', 'milton') - .4, st.end - Wd('K04', 'milton') - .3, { px: 56 }) });

// P140 (L09): kapanış: zifiri karanlıkta kör şair; "Sen, göksel ışık, içime parla": siluetinin içinde aşağıdan yükselen ışık.
// İç ışık: çekirdek temiz kâğıt, çevresi eş merkezli tarama; siluetin DIŞ kenarı koyu bant olarak kalır (biçim okunur).
function oda_icIsik(U, C, rr, kw) {
  const { tx, px, tone } = GR;
  tx.save(); px.save(); tx.clip(U); px.clip(U);
  const g = tx.createRadialGradient(C[0], C[1], 0, C[0], C[1], rr); g.addColorStop(0, tone(1)); g.addColorStop(.4, tone(1)); g.addColorStop(.72, tone(.5)); g.addColorStop(1, tone(.03));
  tx.fillStyle = g; tx.fill(U); px.fillStyle = GR.hatch({ type: 'rad', cx: C[0], cy: C[1], id: 7 }); px.fill(U);
  tx.restore(); px.restore();
  oda_kontur(U, kw);
}
function oda_P140(t) {
  const { tone } = GR, FL = ODA_FL, tSen = Wd('L09', 'sen'), tAn = Wd('L09', 'anlatayım');
  const ic = E.io2(oda_u(t, tSen - .2, tAn + .6));
  GR.fill(oda_dik(-400, FL, W + 800, 400), tone(.03), { th: 0, id: 0 });
  const sa = { x: 880, y: FL - 2.05 * 92, h: 92, f: 1, bas: .28, fw: -.06, kol: 'kol' };
  const Lr = [1700, 250];                                   // sönük yukarı ışık: yalnız ince kenar (siluet okunsun)
  oda_koltuk(sa, 'arka', Lr, 1e5);
  const G = oda_sairGeo(sa), Ub = oda_birles(G.B, G.yaka), Ua = oda_birles(G.A, G.H);
  oda_kut(Ub, { L: Lr, c: G.c, w: 5 });
  const C = G.M(lerp(.3, .2, ic), lerp(-.5, -2.5, ic)), rr = lerp(.4, 4.4, ic) * sa.h;
  if (ic > .005) oda_icIsik(Ub, C, rr, 9);
  oda_koltuk(sa, 'on', Lr, 1e5);
  oda_kut(Ua, { L: Lr, c: G.E, w: 5 });
  if (ic > .005) oda_icIsik(Ua, C, rr, 7);
}
plan('P140', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 560, z: 1 }, { cx: 980, cy: 540, z: 1.2 }, st.p, E.lin), () => { oda_P140(st.t); }, [.03, 0, 1]), {
  tr: { type: 'fade', dur: 1.0 },
  over: (ctx, st) => quote(ctx, '“göksel ışık, içime parla”', 960, 140, st.t - Wd('L09', 'sen') - .3, { px: 66, kaynak: 'KAYIP CENNET · III. 51–52' }) });
