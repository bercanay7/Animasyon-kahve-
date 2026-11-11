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
function oda_yol(pts, k = .8, closed = true) { const P = new Path2D(); spline(P, pts, closed, k); return P; }
function oda_cok(pts) { const P = new Path2D(); poly(P, pts, true); return P; }
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
  g.addColorStop(0, tone(v)); g.addColorStop(a, tone(v)); g.addColorStop(a + (1 - a) * .2, tone(v * .72)); g.addColorStop(a + (1 - a) * .52, tone(v * .34)); g.addColorStop(a + (1 - a) * .8, tone(v * .1)); g.addColorStop(1, tone(0));
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
function oda_mumAlev(x, y, s = 1, o = {}) { const k = s, top = y - 46 * k - 78 * k * (o.boy ?? 1); return [x, top - 20 * k * (o.alev ?? 1)]; }
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
    const hh = 46 * k * alev * (1 + .06 * Math.sin(t * 2.3) + .05 * fbm1(t * .9, 4)), ww = 16 * k * Math.pow(alev, .7);
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
    const v = o.v ?? .42;
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
    for (const [P, c] of books) oda_kut(P, { L, c, w: 4, R, tn: .03 });
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
  const tilt = -al, head = SF.headPath(HC[0], HC[1], h, f, tilt);
  const loc = (x, y, a) => { const c = Math.cos(a), s = Math.sin(a), X = x * f * h, Y = y * h; return [HC[0] + X * c - Y * s, HC[1] + X * s + Y * c]; };
  const HL = (x, y) => loc(x, y, al * f);
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
  const neck = SF.limb(T([.06, -2.25]), B.HL(-.02, .38), () => .25 * h, () => .25 * h, 4);
  const yaka = oda_yol([[-.4, -2.3], [-.12, -2.48], [.22, -2.47], [.46, -2.3], [.6, -2.02], [.52, -1.9], [.24, -1.96], [-.04, -2.1], [-.38, -2.16]].map(T), .7);
  // yakın kol
  const kol = o.kol || 'kol', S = T([.0, -2.1]);
  let E, Wr, hand;
  if (kol === 'yaz') { E = M(.42, -1.28); Wr = M(1.32, -1.62); hand = [[1.24, -1.74], [1.52, -1.76], [1.66, -1.64], [1.6, -1.52], [1.3, -1.52]]; }
  else if (kol === 'diz') { E = M(.3, -1.18); Wr = M(1.45, -.62); hand = [[1.4, -.74], [1.74, -.68], [1.9, -.5], [1.74, -.42], [1.42, -.5]]; }
  else { E = M(-.24, -1.0); Wr = M(.95, -1.06); hand = [[.88, -1.16], [1.18, -1.15], [1.38, -1.02], [1.44, -.84], [1.32, -.77], [1.14, -.9], [.9, -.94]]; }
  const A = oda_birles(SF.limb(S, E, () => .3 * h, () => .27 * h, 8), oda_daire(E[0], E[1], .25 * h), SF.limb(E, Wr, u => (.25 - .05 * u) * h, u => (.24 - .05 * u) * h, 8));
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
  const neck = SF.limb(T([.04, -2.05]), Bg.HL(-.04, .38), () => .2 * h, () => .2 * h, 4);
  const S = T([.0, -1.9]), kol = o.kol || 'kitap';
  let E, Wr;
  if (kol === 'yaz') { E = M(.42, -1.02); Wr = M(1.25, -1.38 + (o.yazY || 0)); }
  else if (kol === 'kucak') { E = M(.35, -1.0); Wr = M(1.2, -.5); }
  else { E = M(.5, -1.05); Wr = M(1.22, -1.5); }
  const A = oda_birles(SF.limb(S, E, () => .22 * h, () => .2 * h, 8), oda_daire(E[0], E[1], .18 * h), SF.limb(E, Wr, u => (.18 - .05 * u) * h, u => (.17 - .05 * u) * h, 8), oda_daire(Wr[0], Wr[1], .14 * h));
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
  parts.push(SF.limb(T([.04, -5.8]), Bg.HL(-.02, .38), () => .25 * h * g, () => .25 * h * g, 4), Bg.head);
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
    return [oda_birles(SF.limb(S, E, () => .24 * h * g, () => .22 * h * g, 8), oda_daire(E[0], E[1], .2 * h * g), SF.limb(E, Wr, u => (.2 - .05 * u) * h * g, u => (.19 - .05 * u) * h * g, 8), oda_daire(Wr[0], Wr[1], .15 * h)), E, Wr]; };
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

// ═════════════ SET: Milton'ın odası ═════════════
// o: {mum: {x, y, s, alev, boy} | null, L (ışık; verilmezse mumdan), r0, r1, pen (pencere seçenekleri | false), raf (false),
//     sair (oda_sair seçenekleri | false), koltuk (true), masa (true), masaUstu (true), golge, arka (fn), on (fn)}
const ODA_YER = { sx: 700, sh: 74, mx0: 880, mx1: 1190, my: 672, mumX: 985 };
function cizOda(t, o = {}) {
  const { tone } = GR, FL = o.FL ?? ODA_FL, Y = ODA_YER;
  const mum = o.mum === null ? null : Object.assign({ x: Y.mumX, y: Y.my, s: 1, alev: 1, boy: 1 }, o.mum || {});
  const fl = mum ? oda_mumAlev(mum.x, mum.y, mum.s, mum) : null;
  const L = o.L || (fl && mum.alev > .02 ? fl : null), al = mum ? mum.alev : 0;
  const R = o.R ?? 560;
  // taban
  GR.fill(oda_dik(-400, FL, W + 800, H - FL + 400), tone(.03), { th: 0, id: 0 });
  // duvar alt pervazı (lambri): yatay koyu bant, üst kenarı ışıkta
  if (o.lambri !== false) oda_kut(oda_dik(-400, FL - 150, W + 800, 14), { L, c: [L ? L[0] : 960, FL - 143], w: 5, R: R * 1.1 });
  // mum ışığı
  if (L && o.isik !== false) oda_isik(L[0], L[1], (o.r0 ?? 78) * Math.min(1, al * 1.2), (o.r1 ?? 560) * (.35 + .65 * al), o.isikV ?? 1);
  if (o.isikEk) o.isikEk();
  if (o.pen !== false) oda_pencere(t, Object.assign({ x0: 250, y0: 170, x1: 590, y1: 560, mod: 'ay', ay: [356, 248] }, o.pen || {}));
  if (o.raf !== false) oda_raf(1400, 1800, 240, FL - 160, L, { R: 980 });
  if (o.arka) o.arka(L);
  const sa = o.sair === false ? null : Object.assign({ x: Y.sx, y: FL - 2.05 * Y.sh, h: Y.sh, f: 1, bas: .12, fw: -.04, kol: 'kol', L, R: R * 1.05 }, o.sair || {});
  let G = null;
  if (sa) {
    if (o.golge !== false && L) oda_golge(oda_sairGeo(sa).B, L, o.golgeK ?? 1.55, o.golgeV ?? .3, FL - 150);
    if (o.koltuk !== false) oda_koltuk(sa, 'arka', L, R);
    G = oda_sair(Object.assign({}, sa, { kolCiz: false }));
    if (o.koltuk !== false) oda_koltuk(sa, 'on', L, R);
    oda_kut(G.A, { L, c: G.E, w: Math.max(4, .085 * sa.h), R: sa.R }); oda_kut(G.H, { L, c: G.Wr, w: Math.max(3.5, .07 * sa.h), R: sa.R });
  }
  if (o.orta) o.orta(L);
  if (o.masa !== false) oda_masa(Y.mx0, Y.mx1, Y.my, L, { R });
  if (o.masaUstu !== false) oda_masaUstu(1085, Y.my, L, o.masaUstu || {});
  let M = null;
  if (mum) M = oda_mum(t, mum.x, mum.y, mum.s, mum);
  if (o.on) o.on(L);
  return { L, G, M, sa };
}

// Mumun yakın planı (P008, P118): masa kenarı, büyük mum; alev gölün alev diliyle aynı biçim (PR.flame, içinde mürekkep vuruşları).
function cizMumYakin(t, o = {}) {
  const { tone } = GR, x = o.x ?? 1470, y = o.y ?? 930, s = o.s ?? 3.2, alev = o.alev ?? 1;
  const fl = oda_mumAlev(x, y, s, { alev, boy: o.boy ?? .9 }), L = alev > .02 ? fl : null;
  GR.fill(oda_dik(-400, y, W + 800, 400), tone(.03), { th: 0, id: 0 });
  if (L) oda_isik(fl[0], fl[1], 150 * Math.min(1, alev * 1.3), 640 * (.3 + .7 * alev));
  // masa kenarı: üst yüz ışıkta
  const top = oda_cok([[-400, y - 22], [W + 400, y - 22], [W + 400, y], [-400, y]]);
  if (L) { const g = GR.tx.createRadialGradient(x, y, 0, x, y, 620); g.addColorStop(0, tone(1)); g.addColorStop(.35, tone(1)); g.addColorStop(.7, tone(.45)); g.addColorStop(1, tone(.04)); GR.fill(top, g, { th: 0, id: 0 }); }
  else GR.fill(top, tone(.03), { th: 0, id: 0 });
  oda_kut(oda_dik(-400, y, W + 800, 36), { L, c: [x, y + 18], w: 8, R: 700 });
  const M = oda_mum(t, x, y - 22, s, { alev, boy: o.boy ?? .9, seed: 4, L: o.L });
  return { L, M, F: fl };
}

// ═════════════ SET: Londra 1660 ═════════════
// Ev siluetleri (cumbalı, üçgen alınlıklı, bacalı); meydanda kitap yakılan ateş; kalabalık; cellat.
function oda_evler(L, r, list, R) {
  for (const e of list) {
    const { x, w, y, hg } = e, j = 12 + r() * 10, rh = w * (.45 + r() * .3), pts = [[x, y], [x, y - hg * .5], [x - j, y - hg * .5], [x - j, y - hg], [x + w / 2, y - hg - rh], [x + w + j, y - hg], [x + w + j, y - hg * .5], [x + w, y - hg * .5], [x + w, y]];
    const P = oda_cok(pts);
    if (r() < .7) { const cx = x + w * (.2 + r() * .6), ch = 30 + r() * 30; P.rect(cx, y - hg - rh * .6 - ch, 18, ch + rh * .3); }
    oda_kut(P, { L, c: [x + w / 2, y - hg * .6], w: 5, R });
    // ateşe bakan cephede birkaç pencere: ışığı yansıtan kurşun camlar (orta ton, taramalı)
    const lit = 1 - clamp(Math.hypot(x + w / 2 - L[0], y - hg * .5 - L[1]) / R);
    if (lit > .15) {
      for (let k = 0; k < 2; k++) for (const fy of [.3, .72]) {
        if (r() < .35) continue;
        const wx = x + w * (.2 + k * .42), wy = y - hg * fy, ww = w * .2, wh = hg * .14;
        GR.fill(oda_dik(wx, wy - wh, ww, wh), GR.tone(.2 + .5 * lit), { th: 0, id: 1 });
        GR.fill(oda_dik(wx + ww / 2 - 2, wy - wh, 4, wh), GR.tone(.03), { th: 0, id: 0 });
      }
    }
  }
}
// uçuşan sayfa: kâğıt beyazı dörtgen, koyu kenar; kendi ekseninde döner (genişliği kosinüsle daralır: sayfa çevriliyor gibi)
function oda_sayfa(x, y, s, a, flip) {
  const tx = GR.tx, c = Math.cos(a), sn = Math.sin(a), fw = Math.max(.15, Math.abs(Math.cos(flip)));
  const pts = [[-1, -1.3], [1, -1.3], [1, 1.3], [-1, 1.3]].map(([u, v]) => { const X = u * s * fw, Y = v * s; return [x + X * c - Y * sn, y + X * sn + Y * c]; });
  const P = oda_cok(pts); GR.fill(P, GR.tone(1), { th: 0, id: 0 });
  tx.save(); tx.strokeStyle = GR.tone(.03); tx.lineWidth = 2.4; tx.lineJoin = 'round'; tx.stroke(P); tx.restore();
}
// o: {t0 (atış döngüsünün başladığı zaman; atış anı tA), tA (son atışın elden çıkış anı), fire: [x, y]}
function cizLondra(t, o = {}) {
  const { tx, tone } = GR, FX = o.fx ?? 1010, FY = o.fy ?? 812, GY = 740, r = rng(61);
  const fl = 1 + .06 * Math.sin(t * 2.1) + .05 * fbm1(t * .8, 9), L = [FX, FY - 150];
  // gök: ateşle alttan aydınlanan pus; duman sütunu
  oda_isik(FX, FY - 120, 0, 1000 * fl, .62);
  PR.smoke({ x: FX + 10, y: FY - 260, h: 760, r0: 70, r1: 230, sway: 70, n: 9, seed: 5, t, glow: .72, base: .06, rise: .025 });
  // evler (arka sıra küçük, ön sıra büyük)
  oda_evler(L, rng(71), [{ x: -40, w: 200, y: GY, hg: 300 }, { x: 175, w: 170, y: GY, hg: 250 }, { x: 360, w: 220, y: GY, hg: 330 }, { x: 600, w: 150, y: GY - 20, hg: 220 }, { x: 1320, w: 160, y: GY - 20, hg: 230 }, { x: 1490, w: 210, y: GY, hg: 320 }, { x: 1715, w: 230, y: GY, hg: 290 }], 1100);
  // zemin: arnavut kaldırımı; ateşin çevresi aydınlık (yassı ışık)
  const Z = oda_dik(-400, GY, W + 800, H - GY + 400);
  GR.fill(Z, tone(.03), { type: 'persp', y0: GY, D: H - GY, p0: 8, p1: 12, id: 8 });
  tx.save(); tx.clip(Z); tx.translate(FX, FY); tx.scale(1, .3); tx.translate(-FX, -FY); oda_isik(FX, FY, 60, 900 * fl, .95); tx.restore();
  // arka kalabalık (küçük, üst üste binen)
  const kal = (list, Lr) => { for (const k of list) oda_ayakta(Object.assign({ L, R: Lr, rw: Math.max(3.5, k.h * .1), kolN: [.15, .2], kolF: [-.1, .2] }, k)); };
  kal([{ x: 1180, y: GY + 18, h: 30, f: -1, palto: -1.4, sapka: 'yuksek' }, { x: 1235, y: GY + 26, h: 32, f: -1, etek: true, sapka: 'baslik' }, { x: 1300, y: GY + 14, h: 29, f: -1, palto: -1.5, sapka: 'genis' },
    { x: 1365, y: GY + 30, h: 34, f: -1, palto: -1.6, sapka: 'yuksek', bas: .1 }, { x: 1440, y: GY + 20, h: 31, f: -1, palto: -1.3, sapka: 'bere' },
    { x: 470, y: GY + 24, h: 32, f: 1, palto: -1.5, sapka: 'genis' }, { x: 410, y: GY + 16, h: 29, f: 1, etek: true, sapka: 'baslik' }, { x: 350, y: GY + 30, h: 33, f: 1, palto: -1.4, sapka: 'yuksek' }], 1300);
  // ateş: çapraz kütükler + alev öbeği
  const kutuk = oda_birles(...[[-150, -10, 170, -40], [-120, -46, 140, 4], [-60, 0, 90, -70], [-170, -30, 40, -14]].map(([a, b, c, d]) => SF.limb([FX + a, FY + b], [FX + c, FY + d], () => 13, () => 13, 4)));
  oda_kut(kutuk, { L: [FX, FY - 80], c: [FX, FY - 20], w: 6, R: 400 });
  // yanan kitaplar (ateşin dibinde düz ciltler)
  for (const [dx, dy, a] of [[-90, -30, .3], [60, -36, -.4], [-10, -50, .1]]) { const P = oda_cok([[-30, -10], [30, -10], [30, 10], [-30, 10]].map(([u, v]) => [FX + dx + u * Math.cos(a) - v * Math.sin(a), FY + dy + u * Math.sin(a) + v * Math.cos(a)])); oda_kut(P, { L: [FX, FY - 120], c: [FX + dx, FY + dy], w: 5, R: 300 }); }
  PR.flameBank(FX - 190, FX + 190, FY - 10, 330 * fl, t, 21, { n: 6, wr: .5, curl: .7, speed: .6, solidBelow: 500, env: f => .35 + .65 * Math.sin(f * PI) });
  // uçuşan sayfalar: ateşten yükselip savrulur (döngü; büyüklük sınırda sıfır)
  for (let i = 0; i < 7; i++) {
    const q = rng(300 + i), ph = q(), sp = .07 + q() * .05, u = (t * sp + ph) % 1, g = Math.sin(PI * u);
    if (g < .15) continue;
    const x = FX + (q() - .5) * 200 + u * (180 + q() * 260) * (q() < .5 ? 1 : -.6) + Math.sin(t * .8 + i) * 30, y = FY - 180 - u * 560;
    oda_sayfa(x, y, 15 * Math.min(1, g * 1.6), t * (.6 + q()) + i, t * (1.2 + q()) + i);
  }
  // cellat: ateşin solunda; kitap yığınından alır, ateşe atar (döngü; son atış tA'da elden çıkar)
  const CX = o.cx ?? 690, CY = FY + 40, cyc = 3.4, tA = o.tA ?? 0, ph = ((t - tA) % cyc + cyc) % cyc, ch = 60;
  // ph: 0 bırakma anı; .0–1.2 takip ve dönüş, 1.2–2.2 yığından alma (eğilir), 2.2–3.4 kaldırma ve geriye çekme
  const kf2 = (ks) => kf(ph, ks);
  const omuz = kf2([[0, 1.75], [1.0, .4], [1.6, .55], [2.2, .5], [3.0, -2.5, E.io2], [3.4, 1.75, E.in2]]), dirsek = kf2([[0, .1], [1.0, .3], [2.2, .4], [3.0, -.9], [3.4, .1, E.in2]]);
  const egil = kf2([[0, .14], [1.0, .05], [1.6, .32], [2.2, .3], [3.0, -.06], [3.4, .14, E.in2]]);
  const yigin = oda_birles(...[0, 1, 2, 3, 4].map(i => oda_dik(CX - 150 + (i % 2) * 6, CY - 22 - i * 20, 74, 18)));
  oda_kut(yigin, { L, c: [CX - 112, CY - 60], w: 5, R: 900 });
  const Gc = oda_ayakta({ x: CX, y: CY, h: ch, f: 1, gen: 1.25, palto: -2.2, sapka: 'bere', kolN: [omuz, dirsek], kolF: [.35 + egil, .5], fw: egil, L, rw: 6.5 });
  const elde = ph > 1.45 || ph < .02;
  if (elde) { const Wr = Gc.WN, a = omuz + dirsek; const P = oda_cok([[-20, -14], [24, -14], [24, 14], [-20, 14]].map(([u, v]) => [Wr[0] + u * Math.cos(a) - v * Math.sin(a), Wr[1] + u * Math.sin(a) + v * Math.cos(a)])); oda_kut(P, { L, c: Wr, w: 5, R: 900 }); }
  else { // havada uçan kitap: elden ateşe yay
    const u = clamp(ph / .9); if (u < 1) { const x0 = CX + 1.8 * ch, y0 = CY - 6.6 * ch, x = lerp(x0, FX - 20, u), y = lerp(y0, FY - 80, u) - Math.sin(PI * u) * 130, a = u * 5;
      oda_kut(oda_cok([[-22, -15], [22, -15], [22, 15], [-22, 15]].map(([p, q]) => [x + p * Math.cos(a) - q * Math.sin(a), y + p * Math.sin(a) + q * Math.cos(a)])), { L, c: [x, y], w: 5, R: 900 }); } }
  // ön kalabalık: kadrajın altından kesilen büyük sırtlar
  kal([{ x: 150, y: H + 300, h: 92, f: 1, palto: -1.5, sapka: 'yuksek', bas: .05 }, { x: 330, y: H + 360, h: 98, f: 1, etek: true, sapka: 'baslik' },
    { x: 1560, y: H + 330, h: 95, f: -1, palto: -1.4, sapka: 'genis' }, { x: 1760, y: H + 280, h: 90, f: -1, palto: -1.6, sapka: 'yuksek' }, { x: 1890, y: H + 380, h: 100, f: -1, palto: -1.4, sapka: 'bere' }], 1500);
  return { L };
}

// ═════════════ ÇEKİMLER ═════════════
// ODA kamerası: tek yönlü yavaş yaklaşma
const ODA_CAM = { cx: 900, cy: 560, z: 1 };

// P007 (A06): karanlık oda; koltukta kör şair, önünde mum; yüzü ışığa dönük, gözü yok. Yavaş yaklaşma (1 → 1,18).
plan('P007', (ctx, st) => levha(ctx, camLerp(ODA_CAM, { cx: 880, cy: 560, z: 1.18 }, st.p, E.lin), () => {
  cizOda(st.t, { sair: { bas: .16 } });
}, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// P008 (B01): bölüm kartı "KÖR ŞAİR"; mumun yakın planı: alev, gölün alev diliyle aynı biçim.
plan('P008', (ctx, st) => levha(ctx, null, () => { cizMumYakin(st.t, {}); }, [.03, 0, 1]), {
  tr: { type: 'black', dur: 1.4, end: true },
  over: (ctx, st) => { const a = PA('P008'); chapterCard(ctx, 'KÖR ŞAİR', 'Hiçbir şey göremeyen bir adam, cehennemi nasıl bu kadar iyi gördü?', st.t - a + .2, Se('B01') + .5 - a, { x: 700, y: 420 }); } });

// P009 (B02): gece; ay ışığında koltukta şair; başından dize çizgileri yükselir. Kızı mumla gelir, masaya oturur, yazar.
// 'kırk dizeyi'de çizgiler çoğalır, 'yirmiye'de yarısı silinir.
function oda_P009(t) {
  const tK = Wd('B02', 'kızını'), tYz = Wd('B02', 'yazdırırdı'), tKirk = Wd('B02', 'kırk'), tYir = Wd('B02', 'yirmiye'), tD = Wd('B02', 'dizeler');
  // kızın yolu: sağdan girer (mum elinde), masanın sağına oturur
  const yu = oda_u(t, tK - .2, tYz - .1), gel = E.io2(yu), otur = E.io2(oda_u(t, tYz - .2, tYz + .5));
  const kx = lerp(1720, 1300, gel), bob = Math.sin(yu * PI * 5) * 3 * (1 - otur);
  const masada = t > tYz - .15;
  const elMum = masada ? null : oda_mumAlev(kx - 70, 640 + bob, .9, {});
  const mum = masada ? { x: 1150, alev: 1, boy: .95 } : null;
  const L = masada ? oda_mumAlev(1150, ODA_YER.my, 1, { boy: .95 }) : (t > tK - .3 ? elMum : null);
  const ayL = [420, 250];
  return cizOda(t, {
    mum, L: L || ayL, r1: masada ? 520 : 420, isik: !!L, R: L ? 560 : 1200,
    pen: { x0: 250, y0: 170, x1: 590, y1: 560, ay: [356, 248], v: .46 },
    sair: { bas: .2, fw: -.05, L: L || ayL, R: L ? 600 : 1400, rw: L ? 6 : 4, vurus: !!L },
    masaUstu: { hokka: true }, golge: L ? undefined : false,
    on: () => {
      // kız
      if (!masada) {
        const G = oda_ayakta({ x: kx, y: ODA_FL, h: 62, f: -1, etek: true, sapka: 'baslik', kolN: [1.15, .25], kolF: [.9, .4], bas: -.05, L: elMum, rw: 6, fw: .05 });
        oda_mum(t, kx - 70, 640 + bob, .9, { boy: 1 });
      } else {
        const yz = Math.sin((t - tYz) * 7) * .5 + .5;
        GR.fill(oda_cok([[1255, ODA_FL], [1262, 760], [1340, 760], [1348, ODA_FL]]), GR.tone(.03), { th: 0, id: 0 });   // tabure
        oda_kiz({ x: 1300 - 30 * (1 - otur), y: 752 + 30 * (1 - otur), h: 60, f: -1, kol: 'yaz', yazY: t > tYz + .5 ? yz * .08 : 0, bas: -.18, fw: .12, L, R: 560 });
      }
      // dize çizgileri: başın üstünde yükselen yığın; yeni satır alttan girer, eskiler yukarı kayar
      const n0 = (t - tD) / 1.15, nK = (t - tKirk) / .16, n = Math.max(0, Math.min(t < tKirk ? n0 : Math.max(n0, Math.min(n0, 7.5) + nK), 13));
      const base = 445, sp = 27, X0 = 610, sil = oda_u(t, tYir, tYir + .9);
      for (let i = 0; i < Math.ceil(n); i++) {
        const u = clamp(n - i), age = n - i - 1, y = base - Math.max(0, age) * sp - (age > 0 ? 0 : 0), q = rng(500 + i);
        const yy = base - (n - 1 - i) * sp; if (yy < 120) continue;
        const L2 = 170 + q() * 230, sl = (i % 2 === 1) ? clamp((sil * 10 - (i % 10) * .5) / 2) : 0;
        oda_satir(X0 + q() * 40, yy, L2, clamp(u * 1.2), sl, 900 + i, 6.5);
      }
    }
  });
}
plan('P009', (ctx, st) => levha(ctx, { cx: 960, cy: 540, z: 1 }, () => { oda_P009(st.t); }, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// P010 (B03): iki kız masada dev kitaplardan sesli okur; harfler kitaplardan dökülüp babaya doğru süzülür; sonda başları öne düşer.
function oda_P010(t) {
  const tI = Wd('B03', 'ibranice'), tSon = Wd('B03', 'dayanılmaz'), dus = E.io2(oda_u(t, tSon - .2, tSon + .9));
  const mum = { x: 1160, alev: 1, boy: .8 };
  return cizOda(t, {
    mum, r1: 540, pen: { x0: 250, y0: 170, x1: 590, y1: 560, ay: [356, 248], v: .4 },
    sair: { bas: .05, fw: -.06, kol: 'kol' }, masaUstu: false,
    orta: L => {
      // arka kız (masanın arkasında, ayakta değil: yüksek sırada oturur; yalnız üst gövdesi masanın üstünde)
      oda_kiz({ x: 1350, y: 700, h: 56, f: -1, kol: 'kitap', bas: lerp(-.12, -.55, dus), fw: lerp(.12, .3, dus), L, R: 560, etekY: 2.05 });
    },
    on: L => {
      oda_kitapAcik(1255, ODA_YER.my - 14, 150, L, { a: .5 });
      oda_kitapAcik(1060, ODA_YER.my - 14, 130, L, { a: .5 });
      oda_kiz({ x: 1440, y: 760, h: 58, f: -1, kol: 'kitap', bas: lerp(-.1, -.6, dus), fw: lerp(.1, .32, dus), L, R: 560 });
      // harfler: kitaplardan yükselir, babaya doğru süzülür (her harf kendi döngüsünde; dilin sırası anlatıma bağlı)
      const on = oda_u(t, tI - 1.2, tI), sön = 1 - oda_u(t, tSon, tSon + 1.2);
      for (let i = 0; i < 14; i++) {
        const q = rng(700 + i), dil = i % 3, ch = ODA_HARF[dil === 0 ? Math.floor(q() * 10) : dil === 1 ? 10 + Math.floor(q() * 10) : 20 + Math.floor(q() * 10)];
        const sp = .085 + q() * .03, u = ((t - S('B03')) * sp + q()) % 1, g = Math.sin(PI * u);
        const src = q() < .5 ? [1255, 600] : [1060, 610], x = lerp(src[0], 860 - q() * 120, u), y = src[1] - Math.sin(PI * u * .9) * (260 + q() * 140) + u * 40;
        oda_harf(ch, x, y, 50 + q() * 14, (q() - .5) * .5 + u * (q() - .5), clamp(g * 1.8) * on * sön);
      }
    }
  });
}
plan('P010', (ctx, st) => levha(ctx, camLerp({ cx: 1000, cy: 540, z: 1.06 }, { cx: 1040, cy: 540, z: 1.06 }, st.p, E.lin), () => { oda_P010(st.t); }, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// P011 (B04): Londra, 1660: meydanda cellat kitapları ateşe atıyor; kalabalık; sayfalar savrulur.
plan('P011', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 960, cy: 560, z: 1.08 }, st.p, E.lin), () => {
  cizLondra(st.t, { tA: Wd('B04', 'ateşe') + .2 });
}, [.03, 0, 1]), { tr: { type: 'fade', dur: 1.0 }, over: (ctx, st) => etiket(ctx, 'LONDRA, 1660', 330, 130, st.lt - .6, st.d - .4, { px: 44 }) });

// P012 (B04@yazarı): karanlık kapı aralığında saklanan şair; alev ışığı yüzüne vurur, titrer; gözleri boş.
function oda_P012(t) {
  const { tx, tone } = GR, FL = 930, fk = .5 + .5 * noise1(t * 3.1, 3) * .8 + .2 * Math.sin(t * 7.3), L = [2300, 420 + 30 * Math.sin(t * 1.3)];
  // duvar: sağda ateşle aydınlanan sıva + ahşap kirişler; solda kapı
  const g = tx.createLinearGradient(1900, 0, 900, 0); g.addColorStop(0, tone(.82 + .12 * fk)); g.addColorStop(.5, tone(.42 + .14 * fk)); g.addColorStop(1, tone(.08));
  GR.fill(oda_dik(1000, -100, 1200, FL + 100), g, { th: 0, id: 1 });
  GR.fill(oda_dik(-400, FL, W + 800, 400), tone(.03), { th: 0, id: 0 });
  tx.save(); tx.clip(oda_dik(980, FL, 1400, 300)); tx.translate(2100, FL); tx.scale(1, .3); tx.translate(-2100, -FL); oda_isik(2100, FL, 100, 1100, .8 + .15 * fk); tx.restore();
  const kiris = oda_birles(oda_dik(1000, 150, 1100, 30), oda_dik(1000, 560, 1100, 26), oda_dik(1480, 150, 28, 780), oda_cok([[1508, 560], [1530, 560], [1880, 176], [1858, 176]]));
  oda_kut(kiris, { L, c: [1450, 400], w: 6 });
  // kapı kasası ve açık kanat (koyu), içerisi zifiri
  const kasa = oda_birles(oda_dik(930, 170, 74, FL - 170), oda_dik(600, 130, 404, 52));
  oda_kut(kasa, { L, c: [960, 500], w: 9 });
  // şair: kapı aralığında, yüzü ateşe dönük; gövdesinin yarısı kasanın arkasında (önce şair, sonra kasanın ön dikmesi)
  const G = oda_ayaktaGeo({ x: 860, y: FL, h: 84, f: 1, cuppe: true, sac: true, kolN: [.2, .9], kolF: [.1, .3], bas: .05, fw: .02 });
  oda_kut(G.B, { L, c: [1100, 500], w: 9 + 5 * fk });
  oda_kut(G.AN, { L, c: [1100, 500], w: 7 + 4 * fk });
  // yaka: yüzün altında ışığa bakan beyaz
  const yk = oda_yol([[-.38, -5.8], [-.1, -5.98], [.24, -5.96], [.48, -5.8], [.62, -5.5], [.52, -5.4], [.24, -5.48], [-.06, -5.62], [-.36, -5.66]].map(p => G.T(p)), .7);
  oda_acik(yk, { L, c: G.T([.1, -5.7]), w: 10, tn: .97, sv: .04 });
  oda_kut(oda_dik(990, 170, 26, FL - 170), { L, c: [1000, 500], w: 8 });       // kasanın ön dikmesi (gövdeyi keser)
}
plan('P012', (ctx, st) => levha(ctx, null, () => { oda_P012(st.t); }, [.03, 0, 1]), { tr: { type: 'cut' } });

// P013 (B05): masada büyüyen el yazması yığını; mum solda; "1667".
function oda_P013(t) {
  const { tx, tone } = GR, y = 880, t0 = S('B05'), t1 = Wd('B05', 'bitirdi') + .3;
  const fl = oda_mumAlev(470, y - 150, 2.1, { boy: .55 }), L = fl;
  oda_isik(L[0], L[1], 120, 760);
  // masa yüzü (geniş, hafif perspektif): mumun dibinde kâğıt, uzakta karanlık
  const top = oda_cok([[-200, y], [W + 200, y], [W + 200, y - 240], [-200, y - 240]]);
  const g = tx.createRadialGradient(L[0], y - 120, 0, L[0], y - 120, 1200); g.addColorStop(0, tone(1)); g.addColorStop(.3, tone(.95)); g.addColorStop(.62, tone(.45)); g.addColorStop(1, tone(.04));
  GR.fill(top, g, { type: 'persp', y0: y - 240, D: 240, p0: 9, p1: 12, id: 0 });
  GR.fill(oda_dik(-200, y, W + 400, 300), tone(.03), { th: 0, id: 0 });
  oda_kut(oda_dik(-200, y, W + 400, 26), { L, c: [L[0], y + 13], w: 8, R: 1300 });
  // yığın: n sayfa; tepe sayfası düşerek yerine oturur
  const p = oda_u(t, t0 + .3, t1), n = 6 + 30 * E.io2(p), k = Math.floor(n), fu = n - k, th = 5.2, X = 1080, Y = y - 70, w = 330, d = 64;
  const sy = Y - k * th;
  // yan yüz: kâğıt beyazı, sayfa kenarları yatay ince koyu çizgiler (8 px'ten seyrek), ışıktan uzak uç koyu
  const side = oda_cok([[X - w / 2, Y], [X + w / 2, Y], [X + w / 2, sy], [X - w / 2, sy]]);
  const gs = tx.createLinearGradient(X - w / 2, 0, X + w / 2, 0); gs.addColorStop(0, tone(.98)); gs.addColorStop(.7, tone(.86)); gs.addColorStop(1, tone(.5));
  GR.fill(side, gs, { th: 0, id: 0 });
  tx.save(); tx.clip(side); tx.strokeStyle = tone(.03); tx.lineWidth = 2.2; for (let yy = Y - 9; yy > sy + 4; yy -= 11) { const q = rng(Math.round(yy)); tx.beginPath(); tx.moveTo(X - w / 2 + q() * 30, yy + q() * 2); tx.lineTo(X + w / 2 - q() * 40, yy + q() * 2); tx.stroke(); } tx.restore();
  tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 3; tx.stroke(side); tx.restore();
  // üst yüz (yazılı sayfa): ince paralelkenar, el yazısı satırları
  const ust = (yy, dx, a) => { const pts = [[-w / 2, 0], [w / 2, 0], [w / 2 - 34, -d], [-w / 2 - 34, -d]].map(([u, v]) => [X + dx + u * Math.cos(a) - v * Math.sin(a), yy + u * Math.sin(a) + v * Math.cos(a)]);
    const P = oda_cok(pts); GR.fill(P, tone(1), { th: 0, id: 0 }); tx.save(); tx.strokeStyle = tone(.03); tx.lineWidth = 2.6; tx.stroke(P); tx.restore();
    for (let i = 0; i < 4; i++) { const v = -12 - i * 13, q = rng(i + 40); const a0 = pts[0], a1 = pts[1], a3 = pts[3]; const f = -v / d;
      const s0 = [lerp(a0[0], a3[0], f), lerp(a0[1], a3[1], f)], e0 = [lerp(a1[0], pts[2][0], f), lerp(a1[1], pts[2][1], f)];
      oda_cizgi([[lerp(s0[0], e0[0], .12), lerp(s0[1], e0[1], .12)], [lerp(s0[0], e0[0], .5 + q() * .1), lerp(s0[1], e0[1], .5) + 1], [lerp(s0[0], e0[0], .82 - q() * .2), lerp(s0[1], e0[1], .82)]], 3.4, .03, .4); } };
  ust(sy, 0, 0);
  if (p < 1 && fu > .02) { const u = E.out3(fu); ust(sy - th - (1 - u) * 150, (1 - u) * -60, (1 - u) * -.12); }
  // hokka ve tüy (yığının sağında)
  oda_masaUstu(1370, y - 90, L, { hokka: true });
  oda_mum(t, 470, y - 150, 2.1, { boy: .55, seed: 6 });
}
plan('P013', (ctx, st) => levha(ctx, null, () => { oda_P013(st.t); }, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => etiket(ctx, '1667', 1620, 170, st.lt - .5, st.d - .3, { px: 52 }) });

// P014 (B06): şairin profili karanlıkta; arkasındaki pencerede mevsimler geçer (kar, bahar çiçeği, yaz gülü); ışık ona ulaşmaz.
function oda_mevsimDis(t, P, x0, y0, x1, y1, m) {
  // m: {kar, yaprak, cicek, gul, gunes (−1..1 konum; null), gok (gök tonu)}
  const { tx, tone } = GR;
  const sx = m.gunes == null ? null : lerp(x0 + 30, x1 - 30, (m.gunes + 1) / 2), syy = m.gunes == null ? 0 : y1 - 60 - Math.sin((m.gunes + 1) / 2 * PI) * (y1 - y0 - 160);
  GR.fill(P, tone(m.gok), sx != null ? { type: 'rad', cx: sx, cy: syy, id: 1 } : { th: 0, id: 1 });
  if (sx != null) { tx.save(); tx.clip(P); PR.glow(sx, syy, 40, 200, 1, .9); tx.fillStyle = tone(1); tx.fill(oda_daire(sx, syy, 34)); tx.restore(); }
  tx.save(); tx.clip(P);
  // dal: sağ üstten sola inen, incelen koyu dal + iki sürgün
  const dal = [[x1 + 30, y0 + 70], [x1 - 120, y0 + 120], [x1 - 260, y0 + 200], [x0 + 150, y0 + 250], [x0 + 40, y0 + 300]];
  oda_cizgi(dal, 22, .03, .3);
  const s1 = [[x1 - 150, y0 + 110], [x1 - 200, y0 + 40], [x1 - 230, y0 - 10]], s2 = [[x0 + 260, y0 + 240], [x0 + 230, y0 + 330], [x0 + 250, y0 + 400]];
  oda_cizgi(s1, 10, .03, .4); oda_cizgi(s2, 10, .03, .4);
  const dug = [[x1 - 70, y0 + 98], [x1 - 190, y0 + 158], [x1 - 300, y0 + 214], [x0 + 210, y0 + 244], [x0 + 110, y0 + 262], [x1 - 222, y0 + 4], [x0 + 236, y0 + 360], [x0 + 60, y0 + 290]];
  // kar: dalın üst kenarında kâğıt beyazı kapak (ince koyu kontur)
  if (m.kar > .02) for (let i = 0; i < dal.length - 1; i++) { const a = dal[i], b = dal[i + 1], w = 26 * m.kar; const P2 = oda_yol([[a[0], a[1] - 9], [lerp(a[0], b[0], .5), lerp(a[1], b[1], .5) - 9 - w * .5], [b[0], b[1] - 9], [lerp(a[0], b[0], .5), lerp(a[1], b[1], .5) - 6]], .7); tx.fillStyle = tone(1); tx.fill(P2); tx.strokeStyle = tone(.03); tx.lineWidth = 2.4; tx.stroke(P2); }
  dug.forEach(([x, y], i) => {
    const q = rng(80 + i);
    if (m.yaprak > .02) { const s = 22 * m.yaprak * (.8 + q() * .4), a = q() * TAU; const P2 = oda_yol([[0, 0], [s * .5, -s * .35], [s, 0], [s * .5, s * .35]].map(([u, v]) => [x + u * Math.cos(a) - v * Math.sin(a), y + u * Math.sin(a) + v * Math.cos(a)]), .8); GR.fill(P2, tone(.03), { th: 0, id: 0 }); }
    if (m.cicek > .02 && i % 2 === 0) { const s = 17 * m.cicek; for (let k = 0; k < 5; k++) { const a = k / 5 * TAU + q(); const P2 = oda_daire(x + Math.cos(a) * s * .62, y + Math.sin(a) * s * .62, s * .48); tx.fillStyle = tone(1); tx.fill(P2); tx.strokeStyle = tone(.03); tx.lineWidth = 2.4; tx.stroke(P2); } tx.fillStyle = tone(.03); tx.fill(oda_daire(x, y, s * .22)); }
  });
  if (m.gul > .02) { // yaz gülü: tek büyük çiçek, spiral taç yaprakları
    const [x, y] = dug[3], s = 46 * m.gul; tx.fillStyle = tone(1); const P2 = oda_daire(x, y, s); tx.fill(P2); tx.strokeStyle = tone(.03); tx.lineWidth = 3; tx.stroke(P2);
    for (let k = 0; k < 3; k++) { tx.beginPath(); tx.arc(x + (k - 1) * s * .08, y + (k - 1) * s * .06, s * (.78 - k * .24), .4 + k * 1.7, 2.9 + k * 1.7); tx.stroke(); }
  }
  tx.restore();
}
function oda_P014(t) {
  const { tx, tone } = GR, FL = ODA_FL, x0 = 380, y0 = 150, x1 = 880, y1 = 610;
  const tM = Wd('B06', 'mevsimler'), tSab = Wd('B06', 'sabah'), tAk = Wd('B06', 'akşam'), tBah = Wd('B06', 'bahar'), tGul = Wd('B06', 'gülü'), tYuz = Wd('B06', 'yüzü');
  const kar = 1 - oda_u(t, tM, tM + 1.4), yaprak = E.io2(oda_u(t, tM + .8, tM + 2.4)) * (1 - .4 * oda_u(t, tGul + .4, tGul + 1.4));
  const cicek = E.out3(oda_u(t, tBah - .2, tBah + .8)) * (1 - oda_u(t, tGul - .2, tGul + .6)), gul = E.out3(oda_u(t, tGul - .3, tGul + .7));
  const gu = oda_u(t, tSab - .3, tAk + 1.1), gunes = gu > 0 && gu < 1 ? lerp(-1, 1, gu) : null;
  const gok = lerp(.55, .9, oda_u(t, tM, tM + 1.6));
  const isik = lerp(.45, 1, oda_u(t, tM, tM + 1.6)) * (1 - .35 * oda_u(t, tYuz, tYuz + 1.2));
  const L = [(x0 + x1) / 2, y0 + 120];
  // pencereden düşen ışık: tabanda dörtgen leke; şairin ayağına varmadan biter (ışık ona ulaşmaz)
  const leke = oda_cok([[x0 + 20, FL + 2], [x1 - 20, FL + 2], [x1 + 210, H + 10], [x0 + 260, H + 10]]);
  GR.fill(oda_dik(-400, FL, W + 800, H - FL + 400), tone(.03), { th: 0, id: 0 });
  GR.fill(leke, tone(.72 * isik), { th: 0, id: 0 });
  GR.fill(oda_cok([[x0 - 30, y1 + 20], [x1 + 30, y1 + 20], [x1 + 90, FL], [x0 + 30, FL]]), tone(.25 * isik), { th: 0, id: 1 });   // duvarda pervaz altı loş ışık
  oda_pencere(t, { x0, y0, x1, y1, mod: 'dis', dis: P => oda_mevsimDis(t, P, x0, y0, x1, y1, { kar, yaprak, cicek, gul, gunes, gok }), sp: 64, sill: .97 });
  // şair: sağda, profili pencereye dönük ama bakmıyor; ışık yalnız profilinin kenarına değer
  const sa = { x: 1330, y: FL - 2.05 * 90, h: 90, f: -1, bas: .1, fw: -.03, kol: 'kol', L, R: 1600, rw: 4.5, vurus: false, yakaV: 0 };
  oda_koltuk(sa, 'arka', L, 1600);
  const G = oda_sair(Object.assign({}, sa, { kolCiz: false }));
  oda_koltuk(sa, 'on', L, 1600);
  oda_kut(G.A, { L, c: G.E, w: 4.5, R: 1600 }); oda_kut(G.H, { L, c: G.Wr, w: 4, R: 1600 });
}
plan('P014', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 1000, cy: 540, z: 1.06 }, st.p, E.lin), () => { oda_P014(st.t); }, [.03, 0, 1]), {
  tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => quote(ctx, '“…ama bana gün dönmez.”', 1380, 170, st.t - Wd('B06', 'ama'), { px: 66, kaynak: 'KAYIP CENNET · III. 41–42' }) });

// P044 (E04@destan): kısa ara: şair karanlık odada, başı öne eğik; mum kısalmış.
plan('P044', (ctx, st) => levha(ctx, { cx: 860, cy: 600, z: 1.12 }, () => {
  cizOda(st.t, { mum: { boy: .45 }, r1: 470, sair: { bas: -.55, fw: .14 } });
}, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// P067 (G02b): gündüz; genç Milton pencere önünde yazıyor (gözleri görüyor). Açık, aydınlık kare (cennet tarifi).
function oda_P067(t, st) {
  const { tx, tone } = GR, FL = ODA_FL, x0 = 300, y0 = 130, x1 = 760, y1 = 600, dol = E.io2(oda_u(t, S('G02b'), S('G02b') + 2.2));
  const SUN = [(x0 + x1) / 2, y0 + 140];
  // duvar: pencereden yayılan ışınsal tarama; ışık içeri doldukça açılır
  const g = tx.createRadialGradient(SUN[0], SUN[1], 0, SUN[0], SUN[1], 1700);
  g.addColorStop(0, tone(1)); g.addColorStop(.18, tone(lerp(.7, .97, dol))); g.addColorStop(.55, tone(lerp(.4, .72, dol))); g.addColorStop(1, tone(lerp(.2, .5, dol)));
  GR.fill(oda_dik(-400, -400, W + 800, FL + 400), g, { type: 'rad', cx: SUN[0], cy: SUN[1], id: 1 });
  GR.fill(oda_dik(-400, FL, W + 800, 400), tone(lerp(.3, .55, dol)), { th: 0, id: 0 });
  GR.fill(oda_cok([[x0 + 10, FL + 2], [x1 - 10, FL + 2], [x1 + 330, H + 10], [x0 + 330, H + 10]]), tone(lerp(.6, .98, dol)), { th: 0, id: 0 });
  oda_pencere(t, { x0, y0, x1, y1, mod: 'dis', sp: 60, dis: P => { GR.fill(P, tone(.97), { type: 'rad', cx: SUN[0], cy: SUN[1], id: 1 }); tx.save(); tx.clip(P); oda_cizgi([[x1 + 30, y0 + 300], [x1 - 140, y0 + 330], [x0 + 140, y0 + 420]], 18, .03, .3); tx.restore(); } });
  // masa (pencerenin önünde), genç şair sağda oturur, pencereye dönük, başı kâğıda eğik
  const L = SUN, mx0 = 760, mx1 = 1080, my = 690;
  const sa = { x: 1230, y: FL - 2.05 * 76, h: 76, f: -1, bas: -.42, fw: .2, kol: 'yaz', L, R: 3000, rw: 9, vurus: false, yakaV: 1 };
  oda_koltuk(sa, 'arka', L, 3000);
  const G = oda_sairGeo(sa);
  oda_kut(G.B, { L, c: G.c, w: 9, tn: .06, R: 3000 });
  // yüz: ışığa bakan baş açık (kâğıt), saç orta ton; göz: kâğıda bakan ince koyu çizgi
  oda_acik(G.head, { L, c: G.HC, w: 7, tn: .97, sv: .08 });
  GR.fill(G.sac, tone(.32), { th: 1.2, id: 0 }); oda_kut(G.sac, { L, c: G.HC, w: 6, tn: .32, hs: { th: 1.2, id: 0 }, R: 3000 });
  oda_cizgi([G.HL(.18, -.05), G.HL(.25, -.03), G.HL(.32, -.05)], 3.4, .03, .5);
  oda_acik(G.yaka, { L, c: G.T([.1, -2.2]), w: 9, tn: .97, sv: .08 });
  oda_masa(mx0, mx1, my, L, { R: 3000 });
  oda_masaUstu(930, my, L, { hokka: true });
  oda_kut(G.A, { L, c: G.E, w: 8, R: 3000 }); oda_acik(G.H, { L, c: G.Wr, w: 6, tn: .97, sv: .08 });
  // kalem: elde, kâğıda inen ince koyu çizgi
  oda_cizgi([G.M(1.5, -1.95), G.M(1.72, -2.05), G.M(1.95, -2.35)], 4, .03, .5);
}
plan('P067', (ctx, st) => levha(ctx, { cx: 900, cy: 520, z: 1.05 }, () => { oda_P067(st.t, st); }, [.9, 0, 1]), { tr: { type: 'fade', dur: 1.0 } });

// P118 (K04): mum söner; ince duman yükselir; "1674".
function oda_P118(t) {
  const tS = Wd('K04', 'milton'), alev = 1 - E.in2(oda_u(t, tS - .3, tS + .45));
  const R = cizMumYakin(t, { alev, boy: .2, L: [1470, 700] });
  if (alev < .99) { // duman: fitilden yükselen, kıvrılan ince kâğıt rengi şerit; yükseldikçe incelir ve söner
    const u = oda_u(t, tS, tS + 4.5), top = R.M.top, x = 1470 + 1.5 * 3.2, pts = [];
    for (let i = 0; i <= 9; i++) { const f = i / 9, yy = top - 10 - f * (90 + 420 * E.out2(u)); pts.push([x + Math.sin(f * 5 - t * 1.1) * (8 + f * 46) + f * 30, yy]); }
    const w = 7 * (1 - .7 * u); if (w > 2.4) oda_cizgi(pts, w, 1, .7);
  }
}
plan('P118', (ctx, st) => levha(ctx, null, () => { oda_P118(st.t); }, [.03, 0, 1]), { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => etiket(ctx, '1674', 700, 360, st.t - Wd('K04', 'milton') - .4, st.end - Wd('K04', 'milton') - .3, { px: 56 }) });

// P140 (L09): kapanış: zifiri karanlıkta kör şair; "Sen, göksel ışık, içime parla": siluetinin içinde aşağıdan yükselen ışık.
function oda_P140(t) {
  const { tx, px, tone } = GR, FL = ODA_FL, tSen = Wd('L09', 'sen'), tAn = Wd('L09', 'anlatayım');
  const ic = E.io2(oda_u(t, tSen - .2, tAn + .6));
  GR.fill(oda_dik(-400, FL, W + 800, 400), tone(.03), { th: 0, id: 0 });
  const sa = { x: 900, y: FL - 2.05 * 84, h: 84, f: 1, bas: .28, fw: -.06, kol: 'kol' };
  const Lr = [1500, -200];                                   // sönük yukarı ışık: yalnız ince kenar (siluet okunsun)
  oda_koltuk(sa, 'arka', Lr, 1e5);
  const G = oda_sairGeo(sa);
  const U = oda_birles(G.B, G.yaka, G.A, G.H);
  oda_kut(G.B, { L: Lr, c: G.c, w: 3.5 }); oda_kut(G.yaka, { L: Lr, c: G.c, w: 3.5 });
  oda_koltuk(sa, 'on', Lr, 1e5);
  oda_kut(G.A, { L: Lr, c: G.E, w: 3.5 }); oda_kut(G.H, { L: Lr, c: G.Wr, w: 3 });
  if (ic > .005) {
    // iç ışık: merkez kucaktan göğse/başa yükselir; çekirdek temiz kâğıt, çevresi eş merkezli tarama; siluetin kenarı koyu kalır
    const C = G.M(lerp(.3, .25, ic), lerp(-.6, -2.2, ic)), rr = lerp(.4, 4.6, ic) * sa.h;
    tx.save(); px.save(); tx.clip(U); px.clip(U);
    const g = tx.createRadialGradient(C[0], C[1], 0, C[0], C[1], rr); g.addColorStop(0, tone(1)); g.addColorStop(.38, tone(1)); g.addColorStop(.7, tone(.55)); g.addColorStop(1, tone(.03));
    tx.fillStyle = g; tx.fill(U); px.fillStyle = GR.hatch({ type: 'rad', cx: C[0], cy: C[1], id: 7 }); px.fill(U);
    tx.lineJoin = 'round'; tx.strokeStyle = tone(.03); tx.lineWidth = 10; tx.stroke(G.B); tx.lineWidth = 8; tx.stroke(G.A); tx.stroke(G.H); tx.lineWidth = 5; tx.stroke(G.yaka);
    tx.restore(); px.restore();
  }
}
plan('P140', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 560, z: 1 }, { cx: 980, cy: 540, z: 1.2 }, st.p, E.lin), () => { oda_P140(st.t); }, [.03, 0, 1]), {
  tr: { type: 'fade', dur: 1.0 },
  over: (ctx, st) => quote(ctx, '“göksel ışık, içime parla”', 960, 140, st.t - Wd('L09', 'sen') - .3, { px: 66, kaynak: 'KAYIP CENNET · III. 51–52' }) });
