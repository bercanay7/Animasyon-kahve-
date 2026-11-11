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
const ODA_KAFA = [[-.46, -.02], [-.44, -.3], [-.27, -.5], [.0, -.57], [.24, -.48], [.34, -.32], [.37, -.16], [.39, -.06], [.47, .1], [.42, .15], [.4, .22], [.41, .28], [.38, .34], [.39, .42], [.32, .5], [.16, .52], [.0, .44], [-.16, .44], [-.33, .36], [-.45, .2]];
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
  const L = o.L, c = o.c, d = Math.max(30, Math.hypot(c[0] - L[0], c[1] - L[1])), k = 1 + o.w / d, R = o.R ?? 1e5, rv = o.rv ?? 1;
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
  g.addColorStop(0, tone(v)); g.addColorStop(a, tone(v)); g.addColorStop(a + (1 - a) * .16, tone(v * .74)); g.addColorStop(a + (1 - a) * .42, tone(v * .36)); g.addColorStop(a + (1 - a) * .7, tone(v * .1)); g.addColorStop(1, tone(0));
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
function oda_mumAlev(x, y, s = 1, o = {}) { const k = s, top = y - 46 * k - 78 * k * (o.boy ?? 1); return [x, top - 24 * k * (o.alev ?? 1)]; }
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
    const hh = (o.ah ?? 58) * k * alev * (1 + .06 * Math.sin(t * 2.3) + .05 * fbm1(t * .9, 4)), ww = (o.aw ?? 19) * k * Math.pow(alev, .7);
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
  const pp = oda_cok([[x - 70, y - 4], [x + 52, y - 4], [x + 64, y - 14], [x - 56, y - 14]]);
  GR.fill(pp, tone(1), { th: 0, id: 0 });
  tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 2.5; tx.stroke(pp); tx.restore();
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
    const v = o.v ?? .28;
    const g = tx.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, tone(v * .8)); g.addColorStop(1, tone(v));
    GR.fill(P, g, { th: 0, id: 1 });
    if (o.ay) {
      tx.save(); tx.clip(P);
      PR.glow(o.ay[0], o.ay[1], 30, 150, 1, .7 * (o.ayV ?? 1));
      tx.fillStyle = tone(1); tx.fill(oda_daire(o.ay[0], o.ay[1], 27));
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
    oda_kut(oda_dik(x0 - 4, yb - 14, x1 - x0 + 8, 14), { L, c: [(x0 + x1) / 2, yb - 7], w: 5, R });
  }
  oda_kut(sides, { L, c: [(x0 + x1) / 2, (y0 + y1) / 2], w: 5, R });
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
  const yaka = oda_yol([[-.4, -2.3], [-.12, -2.48], [.22, -2.47], [.46, -2.3], [.6, -2.02], [.52, -1.9], [.24, -1.96], [-.04, -2.1], [-.38, -2.16]].map(T), .7);
  // yakın kol
  const kol = o.kol || 'kol', S = T([.0, -2.1]);
  let E, Wr, hand;
  if (kol === 'yaz') { E = M(.42, -1.28); Wr = M(1.32, -1.62); hand = [[1.24, -1.74], [1.52, -1.76], [1.66, -1.64], [1.6, -1.52], [1.3, -1.52]]; }
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
function oda_satir(x, y, L, u, sil, seed, w = 6.5) {
  const e = u * (1 - sil); if (e < .02) return;
  const r = rng(seed), n = 8, pts = [], a1 = r() * TAU, a2 = r() * TAU;
  for (let i = 0; i <= n; i++) { const s = i / n * e; pts.push([x + s * L, y + Math.sin(s * L / 38 + a1) * 2.2 + Math.sin(s * L / 17 + a2) * 1.2]); }
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

// ── açık kitap (yan görünüş: iki sayfa yelpazesi) ──
function oda_kitapAcik(x, y, w, L, o = {}) {
  const { tx, tone } = GR, a = o.a ?? .5, hh = w * .62;
  // cilt (koyu) + iki sayfa demeti (kâğıt), sırt dipte
  const cilt = oda_cok([[x - w * .55, y], [x - w * .55 + Math.cos(PI - a) * 0, y], [x - w * .58, y - hh * .9], [x, y + 2], [x + w * .6, y - hh * .9], [x + w * .55, y]]);
  oda_kut(cilt, { L, c: [x, y - hh * .4], w: 4, R: 700 });
  for (const sd of [-1, 1]) {
    const P = oda_yol([[x, y - 3], [x + sd * w * .12, y - hh * .5], [x + sd * w * .5, y - hh * .82], [x + sd * w * .52, y - hh * .76], [x + sd * w * .42, y - hh * .3], [x + sd * w * .06, y - 2]], .5);
    GR.fill(P, tone(.97), { th: 0, id: 0 });
    tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 2.6; tx.stroke(P); tx.restore();
  }
}

