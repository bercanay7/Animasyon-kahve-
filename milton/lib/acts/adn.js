// adn grubu (ADN: Aden bahçesi, CIK: Aden'den çıkış): setler ve planlar burada (bkz. lib/acts/KILAVUZ.md)
// Değer dili: Aden gündüzü AÇIK tarif (cennet.js ile aynı gök: cen_gok); gece KOYU tarif ama cehennem değil (ay: temiz kâğıt disk,
// yatay taramalı ay halesi, zeminde ay lekeleri). Ağaç: düz siyah taç kütlesi + kenarda düzensiz yaprak dişleri + ışık yanında
// içe giren beyaz vuruşlar ve iç yumruların ışıklı kenarları; dallar birkaç kalın çizgi.
// Şeytan'ın biçimleri (Lewis'in "küçülme" okuması): karabatak → kurbağa → yılan; kendi biçiminde kiy_seytan (gol.js).
// Kırmızı çizgi: Âdem ile Havva yalnız uzak, uzun örtülü sade siluet (arkadan), yüz yok; el ele ya da yan yana.
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const adn_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));
const ADN_FADE = { type: 'fade', dur: .8 };

// ═════════ temel yardımcılar ═════════
function adn_doldur(P, v = .02, th = 0, id = 0) { GR.fill(P, GR.tone(v), { th, id }); }
// sivri dolgu çizgi (ton katmanı): iki ucu sivri (uc ~ .55) ya da tek yönlü (adn_sivri)
function adn_cizgi(pts, w, v = .97, uc = .55) { gol_vurus(GR.tx, pts, w, v, uc); }
// kalından inceye vuruş (ilk nokta kalın): kenardan içe giren beyaz vuruş
function adn_sivri(pts, w0, v = .97) {
  const n = pts.length - 1, A = [], B = [];
  for (let i = 0; i <= n; i++) { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, hw = Math.max(1.1, w0 * .5 * Math.pow(1 - i / n, 1.1));
    A.push([pts[i][0] - dy / l * hw, pts[i][1] + dx / l * hw]); B.push([pts[i][0] + dy / l * hw, pts[i][1] - dx / l * hw]); }
  GR.tx.fillStyle = GR.tone(v); GR.tx.beginPath(); poly(GR.tx, [...A, ...B.reverse()], true); GR.tx.fill();
}
const adn_nrm = (x, y) => { const l = Math.hypot(x, y) || 1; return [x / l, y / l]; };
// yoğun çokgen çizgisini dışa doğru yaprak dişleriyle oyar (normal = (dy, -dx)): yavaş yükselen, sivri uçta keskin inen dişler
function adn_dis(pts, closed, o = {}) {
  const q = rng(o.seed || 1), n = pts.length, out = new Array(n), l0 = o.l0 ?? 10, l1 = o.l1 ?? 24, hh = o.h ?? 8;
  let acc = 0, Lk = lerp(l0, l1, q()), hk = hh * (.45 + q() * .9);
  for (let i = 0; i < n; i++) {
    const a = pts[i > 0 ? i - 1 : (closed ? n - 1 : 0)], b = pts[i < n - 1 ? i + 1 : (closed ? 0 : n - 1)];
    const [nx, ny] = adn_nrm(b[1] - a[1], -(b[0] - a[0]));
    if (i > 0) acc += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    while (acc > Lk) { acc -= Lk; Lk = lerp(l0, l1, q()); hk = hh * (.45 + q() * .9); }
    const u = acc / Lk, pr = u < .72 ? Math.pow(u / .72, 1.4) : (1 - u) / .28, m = o.amp ? o.amp(pts[i], nx, ny) : 1;
    out[i] = [pts[i][0] + nx * hk * pr * m, pts[i][1] + ny * hk * pr * m];
  }
  return out;
}
// kenar çizgisi boyunca ışık yanında içe giren beyaz vuruşlar (clip: kütle). o: {gap: [a, b], len: [a, b], w, min (ışık eşiği), seed, v}
function adn_kesik(out, L, P, o = {}) {
  const q = rng(o.seed || 3), n = out.length, [g0, g1] = o.gap || [40, 120], [l0, l1] = o.len || [18, 90];
  const tx = GR.tx; tx.save(); tx.clip(P);
  let acc = 0, s = q() * g1;
  for (let i = 1; i < n - 1; i++) {
    acc += Math.hypot(out[i][0] - out[i - 1][0], out[i][1] - out[i - 1][1]);
    if (acc < s) continue; acc = 0; s = lerp(g0, g1, q());
    const [nx, ny] = adn_nrm(out[i + 1][1] - out[i - 1][1], -(out[i + 1][0] - out[i - 1][0]));
    const [lx, ly] = adn_nrm(L.x - out[i][0], L.y - out[i][1]), f = nx * lx + ny * ly;
    if (f < (o.min ?? .3)) continue;
    const len = lerp(l0, l1, q() * q()) * (.45 + .55 * f), [dx, dy] = adn_nrm(-nx * .75 - lx * .25, -ny * .75 - ly * .25), bd = (q() - .5) * .5, pts = [];
    for (let k = 0; k <= 6; k++) { const u = k / 6, a = Math.atan2(dy, dx) + bd * u; pts.push([out[i][0] - nx * 2 + Math.cos(a) * len * u, out[i][1] - ny * 2 + Math.sin(a) * len * u]); }
    adn_sivri(pts, (o.w ?? 6) * (.7 + .5 * q()), o.v ?? .97);
  }
  tx.restore();
}
// koyu kütlenin ışık yanında ince kâğıt kenar (gece; ışığa bakan kenardan b px içeride, w px genişlikte)
function adn_kenar(P, L, cx, cy, w = 6, b = 2.5) {
  const tx = GR.tx, [lx, ly] = adn_nrm(L.x - cx, L.y - cy);
  tx.save(); tx.clip(P);
  tx.save(); tx.translate(-lx * b, -ly * b); tx.fillStyle = GR.tone(.95); tx.fill(P); tx.restore();
  tx.save(); tx.translate(-lx * (b + w), -ly * (b + w)); tx.fillStyle = GR.tone(.02); tx.fill(P); tx.restore();
  tx.restore();
}

// ═════════ ağaç ═════════
// Taç: birkaç dairenin birleşimi (ışınsal dış çizgi) + yaprak dişleri; düz siyah; ışık yanında içe giren beyaz vuruşlar ve
// iç yumruların ışıklı kenarları (hacim). o: {x, y, r, seed, L, n (yumru), wx, sq, tooth, v, cuts (0..1), lobes (0..1), rim (gece: kenar ışığı px)}
function adn_tac(o) {
  const q = rng((o.seed || 1) * 7 + 2), R = o.r, cx = o.x, cy = o.y, B = [[cx, cy, R * .62]], nb = o.n ?? 7;
  for (let k = 0; k < nb; k++) { const a = -PI / 2 + (k / Math.max(1, nb - 1) - .5) * PI * (o.spread ?? 1.6) + (q() - .5) * .45, d = R * (.4 + q() * .22), r = R * (.3 + q() * .2);
    B.push([cx + Math.cos(a) * d * (o.wx ?? 1.2), cy + Math.sin(a) * d * (o.sq ?? .75), r]); }
  const ext = (th) => { const ux = Math.cos(th), uy = Math.sin(th); let m = R * .3;
    for (const b of B) { const vx = b[0] - cx, vy = b[1] - cy, p = vx * ux + vy * uy, c = vx * vx + vy * vy - b[2] * b[2], D = p * p - c; if (D >= 0) m = Math.max(m, p + Math.sqrt(D)); }
    return m; };
  const N = Math.max(140, Math.round(TAU * R * 1.6 / 3)), pts = [];
  for (let i = 0; i < N; i++) { const th = i / N * TAU, m = ext(th); pts.push([cx + Math.cos(th) * m, cy + Math.sin(th) * m]); }
  const out = adn_dis(pts, true, { seed: (o.seed || 1) * 3 + 1, h: o.tooth ?? 9, l0: 9, l1: 22 });
  const P = new Path2D(); poly(P, out, true);
  adn_doldur(P, o.v ?? .02, PI / 2);
  const L = o.L;
  if (L) {
    if (o.rim) adn_kenar(P, L, cx, cy, o.rim, 2.5);
    // iç yumruların ışıklı kenarları: ışığa bakan yay boyunca hilal biçimli kısa beyaz tarama (yaprak öbeğinin hacmi);
    // yalnız tacın içinde kalan kısım; vuruş boyu yayın ortasında en uzun, uçlarda sıfır
    const lb = o.lobes ?? 1;
    if (lb > 0) {
      const tx = GR.tx; tx.save(); tx.clip(P);
      B.forEach((b, k) => { if (k === 0) return;
        const q2 = rng(k * 31 + (o.seed || 1)), la = Math.atan2(L.y - b[1], L.x - b[0]), span = .85, m = Math.max(4, Math.round(b[2] * span * 2 / 12));
        for (let j = 0; j < m; j++) {
          const a = la - span + 2 * span * (j + .5) / m, p = [b[0] + Math.cos(a) * b[2] * .95, b[1] + Math.sin(a) * b[2] * .95], th = Math.atan2(p[1] - cy, p[0] - cx);
          if (Math.hypot(p[0] - cx, p[1] - cy) > ext(th) - 16) continue;
          const pr = Math.pow(Math.sin(PI * (j + .5) / m), .8), len = (8 + b[2] * .2 * lb * pr) * (.55 + .45 * q2());
          if (len < 9) continue;
          const da = a + PI + (q2() - .5) * .25;
          adn_sivri([p, [p[0] + Math.cos(da) * len * .5, p[1] + Math.sin(da) * len * .5], [p[0] + Math.cos(da) * len, p[1] + Math.sin(da) * len]], o.lw ?? 4.6, .97);
        }
      });
      tx.restore();
    }
    if ((o.cuts ?? 1) > 0) adn_kesik(out, L, P, { seed: (o.seed || 1) + 5, gap: [26, 90 / (o.cuts ?? 1)], len: [12, 70 * (o.cuts ?? 1)], w: o.cw ?? 6, min: .25 });
  }
  return { P, out, B, ext };
}
// gövde: hafif kavisli, dibe doğru genişleyen koyu çizgi; dallar: [[u (yükseklik), açı (0 yukarı), boy, kalınlık]]
function adn_govde(x, yb, yt, w0, w1, o = {}) {
  const n = 12, A = [], Bp = [], bend = o.bend || 0;
  for (let i = 0; i <= n; i++) { const u = i / n, cx = x + bend * Math.sin(u * PI * .9), cy = lerp(yb, yt, u), w = lerp(w0, w1, Math.pow(u, .6)) * (1 + .7 * Math.pow(1 - u, 6));
    A.push([cx - w / 2, cy]); Bp.push([cx + w / 2, cy]); }
  const P = new Path2D(); poly(P, [...A, ...Bp.reverse()], true); adn_doldur(P, o.v ?? .02, PI / 2);
  for (const [u, a, len, w] of (o.dallar || [])) {
    const bx = x + bend * Math.sin(u * PI * .9), by = lerp(yb, yt, u), pts = [];
    for (let k = 0; k <= 6; k++) { const s = k / 6, aa = a + (o.kv ?? .25) * s * Math.sign(a || 1); pts.push([bx + Math.sin(aa) * len * s, by - Math.cos(aa) * len * s]); }
    adn_sivri(pts, w, o.v ?? .02);
  }
  if (o.L) { const sd = o.L.x > x ? 1 : -1, pts = []; for (let i = 1; i < n - 1; i++) { const u = i / n; pts.push([x + bend * Math.sin(u * PI * .9) + sd * (lerp(w0, w1, Math.pow(u, .6)) / 2 - 7), lerp(yb, yt, u)]); }
    GR.tx.save(); GR.tx.clip(P); adn_cizgi(pts, o.rw ?? 5, .96, .4); GR.tx.restore(); }
  return P;
}
// alçak çalı / yaprak bandı: dişli üst kenar, düz siyah gövde. o: {x0, x1, y, amp, wl, seed, yb, tooth, L, cuts, v}
function adn_cali(o) {
  const q = rng((o.seed || 1) * 5 + 3), ph1 = q() * TAU, ph2 = q() * TAU, ph3 = q() * TAU, amp = o.amp ?? 40, wl = o.wl ?? 160, top = [];
  const yb = o.yb ?? H + 300, ew = o.endW ?? 160, ed = o.endD ?? (yb - o.y + 30);
  for (let x = o.x0; x <= o.x1 + .1; x += 3) {
    let y = o.y - amp * (.55 * Math.abs(Math.sin(x / wl * PI + ph1)) + .3 * Math.abs(Math.sin(x / (wl * .47) * PI + ph2)) + .15 * (1 + Math.sin(x / (wl * 2.3) * PI + ph3)));
    if (o.ends !== false) { const e = Math.min(x - o.x0, o.x1 - x) / ew; if (e < 1) y += Math.pow(1 - e, 2.2) * ed; }   // uçlar yuvarlanarak iner (kutu gibi kesilmez)
    top.push([x, y]);
  }
  const tp = adn_dis(top, false, { seed: (o.seed || 1) * 11, h: o.tooth ?? 8, l0: 8, l1: 20 });
  const P = new Path2D(); P.moveTo(o.x0, yb); for (const p of tp) P.lineTo(p[0], p[1]); P.lineTo(o.x1, yb); P.closePath();
  adn_doldur(P, o.v ?? .02, PI / 2);
  if (o.L && o.rim) adn_kenar(P, o.L, (o.x0 + o.x1) / 2, o.y + 200, o.rim, 2.5);
  if (o.L && (o.cuts ?? 1) > 0) adn_kesik(tp, o.L, P, { seed: (o.seed || 1) + 9, gap: [30, 110], len: [12, 60 * (o.cuts ?? 1)], w: 5.5, min: .2 });
  return { P, top: tp };
}
// çiçekler: koyu bandın üst kenarında küçük kâğıt beyazı beş yapraklı çiçekler (koyu kütlenin önünde)
function adn_cicek(top, o = {}) {
  const q = rng(o.seed || 17), tx = GR.tx; tx.fillStyle = GR.tone(.98);
  for (let i = 0; i < top.length; i += 1) {
    if (q() > (o.d ?? .05)) continue;
    const p = top[i], r = (o.r ?? 7) * (.7 + q() * .6), x = p[0] + (q() - .5) * 10, y = p[1] + 4 + q() * (o.depth ?? 40), P = new Path2D(), a0 = q() * TAU;
    for (let k = 0; k < 5; k++) { const a = a0 + k / 5 * TAU; P.moveTo(x, y); P.ellipse(x + Math.cos(a) * r * .55, y + Math.sin(a) * r * .55 * .8, r * .5, r * .3, a, 0, TAU); }
    tx.fill(P);
  }
}
// gündüz zemini: ufuktan öne açık çayır (seyrek perspektif tarama). y0 ufuk
function adn_zemin(y0, o = {}) {
  const { tx, px, tone } = GR, P = new Path2D(); P.rect(-1600, y0, W + 3200, H + 1600);
  const g = tx.createLinearGradient(0, y0, 0, H); g.addColorStop(0, tone(o.v0 ?? .8)); g.addColorStop(.35, tone(o.v1 ?? .92)); g.addColorStop(1, tone(o.v2 ?? .97));
  tx.fillStyle = g; tx.fill(P); px.fillStyle = GR.hatch({ type: 'persp', y0, D: 500, p0: 9.5, p1: 12.5, id: 1 }); px.fill(P);
}
// uzak tepeler: orta ton, yatay seyrek tarama; üst kenar yumuşak dalgalı
function adn_tepe(y, amp, seed, o = {}) {
  const q = rng(seed), ph = q() * TAU, ph2 = q() * TAU, P = new Path2D(); P.moveTo(-1600, y + 400);
  for (let x = -1600; x <= W + 1600; x += 20) P.lineTo(x, y - amp * (.6 + .4 * Math.sin(x / (o.wl ?? 520) * PI + ph)) * (.7 + .3 * Math.sin(x / 190 + ph2)));
  P.lineTo(W + 1600, y + 400); P.closePath();
  GR.fill(P, GR.tone(o.v ?? .62), { th: 0, id: 1 });
}

// ═════════ gece ═════════
// Ay: temiz kâğıt disk; çevresinde yatay taramalı hale (koyu tarif: tarama yatay); birkaç ince kâğıt ışın. M: {x, y, r}
function adn_gece(M, o = {}) {
  const { tx, px, tone } = GR, R = o.R ?? 800;
  const g = tx.createRadialGradient(M.x, M.y, M.r, M.x, M.y, R);
  g.addColorStop(0, tone(.98)); g.addColorStop(.14, tone(.9)); g.addColorStop(.32, tone(.5)); g.addColorStop(.62, tone(.14)); g.addColorStop(1, tone(.04));
  tx.fillStyle = g; tx.fillRect(-1600, -1600, W + 3200, H + 3200);
  px.fillStyle = GR.hatch({ th: 0, id: 1 }); px.fillRect(-1600, -1600, W + 3200, H + 3200);
  const D = new Path2D(); D.arc(M.x, M.y, M.r, 0, TAU); tx.fillStyle = tone(1); tx.fill(D);
  const q = rng(o.seed || 5);
  for (let k = 0; k < (o.rays ?? 7); k++) { const a = (k + q() * .6) / (o.rays ?? 7) * TAU, r0 = M.r * 1.5, len = M.r * (1.3 + q() * 2.2);
    adn_cizgi([[M.x + Math.cos(a) * r0, M.y + Math.sin(a) * r0], [M.x + Math.cos(a) * (r0 + len), M.y + Math.sin(a) * (r0 + len)]], 4.5, .97, .5); }
}
// gece zemini: koyu; ay lekeleri (dişli kenarlı kâğıt lekeler; yaprak gölgesinin arasından düşen ışık)
function adn_geceZemin(y0, o = {}) {
  const P = new Path2D(); P.rect(-1600, y0, W + 3200, H + 1600);
  const g = GR.tx.createLinearGradient(0, y0, 0, y0 + 120); g.addColorStop(0, GR.tone(o.v0 ?? .2)); g.addColorStop(1, GR.tone(.03));
  GR.fill(P, g, { th: 0, id: 1 });
}
function adn_leke(x, y, rx, ry, seed, v = .93) {
  const q = rng(seed * 3 + 1), pts = [], N = Math.round(TAU * Math.max(rx, ry) / 3);
  for (let i = 0; i < N; i++) { const a = i / N * TAU, m = 1 + .18 * Math.sin(a * 3 + q() * 0) * (q() * .3 + .7) + .12 * Math.sin(a * 5 + seed); pts.push([x + Math.cos(a) * rx * m, y + Math.sin(a) * ry * m]); }
  const out = adn_dis(pts, true, { seed: seed + 2, h: 6, l0: 10, l1: 22 }), P = new Path2D(); poly(P, out, true);
  GR.fill(P, GR.tone(v), { type: 'persp', y0: y - ry, D: 400, p0: 9.5, p1: 12.5, id: 8 });
  return P;
}

// ═════════ Âdem ile Havva: arkadan, uzun örtülü sade figür ═════════
// x, y: ayak ortası; h: baş boyu (boy ≈ 7.4 h). o: {v (.985 açık | .02 koyu), el: [x, y] (tutulan elin dünya noktası), kol (±1: hangi yandan),
//   adim (yürüyüş evresi), diz (0..1 diz çökme), egik (0..1 baş eğik), sac (true: omuza dökülen örtü; Havva), seed, kat (kıvrım vuruşu sayısı)}
function adn_insan(x, y, h, o = {}) {
  const { tx } = GR, d = clamp(o.diz || 0), eg = clamp(o.egik || 0), st = o.adim ?? 0, bob = -.07 * Math.abs(Math.sin(st)), dy = 2.6 * d - bob;
  const W2 = (lx, ly) => [x + lx * h, y + ly * h], sw = .12 * Math.sin(st);
  // sağ yarı (yukarıdan aşağı): boyun, omuz, sarkan yen, el, bel girintisi, etek; sol yarı aynası
  const half = sd => [[.24, -6.3], [.9, -6.02 + .2 * eg], [1.16, -5.55 + .15 * eg], [1.22, -4.5], [1.2, -3.55], [1.02, -3.3], [.9, -3.5], [.98, -2.2 + .5 * d], [1.2 + .45 * d, -.6 * (1 - .5 * d)], [1.26 + .5 * d, 0]]
    .map(([a, b2], i) => [a * sd + (i > 6 ? sw * (i - 6) / 3 : 0), b2 < -2.4 ? b2 + dy : b2 * (1 - .55 * d)]);
  const R = half(1), Lf = half(-1).reverse(), body = [...R, [0, .05], ...Lf].map(([a, b2]) => W2(a, b2));
  const P = new Path2D(); spline(P, body, true, .45);
  const hc = W2(0, -6.98 + dy + .7 * eg), Hd = new Path2D(); Hd.ellipse(hc[0], hc[1], .5 * h, (.6 - .1 * eg) * h, 0, 0, TAU); P.addPath(Hd);
  let hair = null;
  if (o.sac) { hair = new Path2D(); spline(hair, [[-.48, -7.2], [.48, -7.2], [.62, -6.4], [.6, -5.0], [.36, -4.35], [-.36, -4.35], [-.6, -5.0], [-.62, -6.4]].map(([a, b2]) => W2(a, b2 + dy + (b2 < -6.6 ? .7 * eg : .25 * eg))), true, .6); P.addPath(hair); }
  if (o.el) {
    const sd = o.kol || 1, sh = W2(1.0 * sd, -5.7 + dy), e = o.el, mx = (sh[0] + e[0]) / 2 + sd * .2 * h, my = (sh[1] + e[1]) / 2 + .25 * h;
    const pts = [sh, [mx, my], e], A = [], Bq = [];
    for (let i = 0; i < 3; i++) { const p0 = pts[Math.max(0, i - 1)], p1 = pts[Math.min(2, i + 1)], [nx, ny] = adn_nrm(p1[1] - p0[1], -(p1[0] - p0[0])), w = [.4, .32, .17][i] * h; A.push([pts[i][0] + nx * w, pts[i][1] + ny * w]); Bq.push([pts[i][0] - nx * w, pts[i][1] - ny * w]); }
    const K = new Path2D(); spline(K, [...A, ...Bq.reverse()], true, .5); P.addPath(K);
    const Hn = new Path2D(); Hn.ellipse(e[0], e[1], .22 * h, .19 * h, 0, 0, TAU); P.addPath(Hn);
  }
  const v = o.v ?? .985;
  adn_doldur(P, v, PI / 2, 10);
  // açık figür: saç ve kolun kenarında ince mürekkep ayrım; etekte kısa kıvrım vuruşları
  if (v > .5 && h >= 9) {
    const q = rng(o.seed || 4); tx.save(); tx.clip(P);
    if (hair) for (const sd of [-1, 1]) adn_cizgi([W2(.56 * sd, -6.2 + dy), W2(.6 * sd, -5.2 + dy), W2(.38 * sd, -4.45 + dy)], Math.max(2.4, h * .13), .03, .5);
    for (const sd of [-1, 1]) adn_cizgi([W2(.98 * sd, -5.0 + dy), W2(.96 * sd, -4.1 + dy), W2(.92 * sd, -3.55 + dy)], Math.max(2.4, h * .12), .03, .5);
    for (let i = 0; i < (o.kat ?? 2); i++) { const fx = (i ? .5 : -.35) + (q() - .5) * .2, L0 = (.9 + q() * .7) * h, p0 = W2(fx + sw * .6, .1);
      adn_sivri([p0, [p0[0] + (q() - .5) * 2, p0[1] - L0 * .5], [p0[0] + (q() - .5) * 3, p0[1] - L0]], Math.max(2.6, h * .13), .03); }
    tx.restore();
  }
  return P;
}

// ═════════ karabatak ═════════
// Tünemiş, dik duruşlu, uzun boyunlu koyu kuş (profil). x, y: tünediği nokta; s: gövde boyu (px); o: {f (±1 bakış), kanat (0 kapalı … 1 açık: kanat kurutma duruşu),
//   bas (baş açısı, + aşağı), don (0..1 başı geri çevirme), goz (0..1), L (ışık), t, alev ({k, seed}: içindeki alev), golge (true: yalnız biçim yolu döner)}
function adn_kus(x, y, s, o = {}) {
  const f = o.f ?? 1, t = o.t || 0, kn = E.io2(clamp(o.kanat || 0)), W2 = (a, b) => [x + a * f * s, y + b * s];
  const body = [[.06, -.02], [.17, -.13], [.25, -.38], [.25, -.58], [.18, -.78], [.07, -.87], [-.05, -.84], [-.14, -.64], [-.18, -.36], [-.15, -.13], [-.2, .08], [-.27, .38], [-.2, .43], [-.1, .14], [-.02, .02]];
  const BP = new Path2D(); spline(BP, body.map(([a, b]) => W2(a, b)), true, .55);
  // boyun: S kavisli tüp; baş ve gaga (baş açısı ve geri dönüş)
  const ba = o.bas || 0, dn = clamp(o.don || 0), hf = Math.cos(PI * dn);       // baş yönü: 1 ileri … −1 geri
  const nc = [[.06, -.8], [.12, -.98], [.08 + .04 * (1 - hf) * 0, -1.12], [.13 * hf + .02, -1.27]];
  const NP = new Path2D(); { const A = [], B = []; for (let i = 0; i < nc.length; i++) { const p0 = nc[Math.max(0, i - 1)], p1 = nc[Math.min(nc.length - 1, i + 1)], [nx, ny] = adn_nrm(p1[1] - p0[1], -(p1[0] - p0[0])), w = [.075, .055, .05, .05][i];
    A.push([nc[i][0] + nx * w, nc[i][1] + ny * w]); B.push([nc[i][0] - nx * w, nc[i][1] - ny * w]); }
    spline(NP, [...A, ...B.reverse()].map(([a, b]) => W2(a, b)), true, .5); }
  const hc = nc[3], c = Math.cos(ba), sn = Math.sin(ba), HW = (a, b) => W2(hc[0] + (a * c - b * sn) * hf, hc[1] + a * sn * Math.abs(hf) + b * c);
  const HP = new Path2D(); spline(HP, [[-.1, -.01], [-.05, -.07], [.06, -.065], [.1, -.03], [.31, -.02], [.335, .0], [.325, .03], [.3, .015], [.1, .035], [.0, .06], [-.09, .04]].map(([a, b]) => HW(a, b)), true, .35);
  // kanatlar: kapalıyken gövdenin üstünde, açıkken dirsek yukarıda, el tüyleri sarkık (kurutma duruşu); uzak kanat öne, yakın kanat arkaya
  const kan = (sd) => {
    const fold = [[0, 0], [-.08, .1], [-.11, .3], [-.13, .55], [-.16, .8], [-.1, .82], [-.06, .55], [-.02, .3], [.02, .12]];
    const open = [[0, 0], [-.42, -.34], [-.64, -.42], [-.92, -.16], [-.9, .1], [-.68, .14], [-.46, .16], [-.24, .16], [-.04, .1]];
    const pts = fold.map((p, i) => [lerp(p[0], open[i][0], kn) * (sd > 0 ? 1 : -.82), lerp(p[1], open[i][1], kn) + (sd > 0 ? 0 : -.05 * kn)]);
    const sh = sd > 0 ? [-.06, -.68] : [.04, -.7], wob = Math.sin(t * 1.3 + sd) * .015 * kn;
    const raw = pts.map(([a, b]) => W2(sh[0] + a, sh[1] + b + wob * a));
    // arka kenar: tüy dişleri (yalnız açıkken belirgin)
    const tr = []; for (let i = 3; i < raw.length; i++) tr.push(raw[i]);
    const dense = []; for (let i = 0; i < tr.length - 1; i++) for (let k = 0; k < 8; k++) dense.push([lerp(tr[i][0], tr[i + 1][0], k / 8), lerp(tr[i][1], tr[i + 1][1], k / 8)]);
    dense.push(raw[0]);
    const dd = adn_dis(dense, false, { seed: sd > 0 ? 41 : 42, h: s * .05 * kn * (f * sd > 0 ? 1 : 1), l0: s * .07, l1: s * .12 });
    const P = new Path2D(); poly(P, [raw[0], raw[1], raw[2], ...dd], true);
    return { P, tr: dd };
  };
  const far = kan(-1), near = kan(1);
  const all = new Path2D(); all.addPath(BP); all.addPath(NP); all.addPath(HP); all.addPath(near.P); if (kn > .05) all.addPath(far.P);
  if (o.golge) return all;
  const L = o.L || { x: x - 400 * f, y: y - 600 }, v = o.v ?? .02;
  if (kn > .05) adn_doldur(far.P, v);
  adn_doldur(BP, v); adn_doldur(NP, v); adn_doldur(HP, v); adn_doldur(near.P, v);
  // iç alev (gövdenin içinde, kenardan payla)
  if (o.alev && o.alev.k > .02) {
    const k = o.alev.k, tx = GR.tx, px = GR.px, bx = W2(.04, -.2), win = new Path2D();
    spline(win, [[.02, -.08], [.12, -.2], [.15, -.42], [.12, -.6], [.04, -.68], [-.06, -.6], [-.09, -.4], [-.07, -.18]].map(([a, b]) => W2(a, b)), true, .6);
    GR.save(); tx.clip(win); px.clip(win);
    adn_alevler(bx[0], bx[1] + s * .1, s * .2, s * .5 * k, t, o.alev.seed || 7, 3);
    GR.restore();
  }
  // ışık yanı: kanat tüy aralarından ve göğüsten içe giren birkaç beyaz vuruş
  if (s > 90) {
    const tx = GR.tx, q = rng(9);
    if (kn > .3) { tx.save(); tx.clip(near.P); for (let i = 2; i < near.tr.length - 6; i += 7) { const p = near.tr[i], pts = []; const ln = s * (.08 + q() * .12) * kn;
      for (let k = 0; k <= 5; k++) pts.push([p[0] + (W2(-.06, -.68)[0] - p[0]) * .0 + f * s * .03 * k / 5 * 0 + (W2(-.3, -1.0)[0] - p[0]) * k / 5 * ln / s, p[1] + (W2(-.3, -1.0)[1] - p[1]) * k / 5 * ln / s]);
      adn_sivri(pts, Math.max(3.5, s * .016), .97); } tx.restore(); }
    tx.save(); tx.clip(BP); const lf = Math.sign((L.x - x) * f);
    if (lf > 0) { adn_cizgi([W2(.22, -.66), W2(.25, -.45), W2(.21, -.2)], Math.max(4, s * .016), .96, .4); }
    else { adn_cizgi([W2(-.12, -.7), W2(-.16, -.4), W2(-.14, -.18)], Math.max(4, s * .016), .96, .4); }
    tx.restore();
  }
  // göz: tek ince ışık
  const g = clamp(o.goz ?? 1);
  if (g > .02) { const e = HW(.03, -.02), tx = GR.tx; tx.fillStyle = GR.tone(1); tx.beginPath(); tx.ellipse(e[0], e[1], Math.max(2.4, s * .022) * Math.abs(hf), Math.max(1.2, s * .008) * g, ba * f, 0, TAU); tx.fill(); }
  return all;
}

// ═════════ kurbağa (sade, çömelmiş profil) ═════════
function adn_kurbaga(x, y, s, o = {}) {
  const f = o.f ?? 1, W2 = (a, b) => [x + a * f * s, y + b * s], br = (o.nefes || 0) * .02;
  const P = new Path2D(); spline(P, [[.5, -.2], [.42, -.33], [.31, -.4 - br], [.24, -.47 - br], [.15, -.43 - br], [-.02, -.38 - br], [-.25, -.33], [-.4, -.22], [-.44, -.08], [-.34, -.01], [-.12, 0], [.06, 0], [.16, -.05], [.26, -.01], [.36, 0], [.38, -.06], [.47, -.11]].map(([a, b]) => W2(a, b)), true, .5);
  adn_doldur(P, .02);
  if (o.L) adn_kenar(P, o.L, x, y - s * .2, Math.max(3, s * .06), 2);
  const e = W2(.25, -.4 - br); GR.tx.fillStyle = GR.tone(1); GR.tx.beginPath(); GR.tx.ellipse(e[0], e[1], Math.max(2, s * .03), Math.max(1.2, s * .014), 0, 0, TAU); GR.tx.fill();
  return P;
}

// ═════════ yılan ═════════
// Merkez çizgisi C (kuyruktan başa, dünya noktaları) ve yarı genişlik w(u). Gövde, daireler birleşimi olarak kurulur (kıvrımda delik olmaz).
// Kıvrımlar: seg [[u0, u1], ...] sırayla çizilir; sonrakiler öncekilerin üstünden geçerken aralarında ince kâğıt ayrım kalır.
// o: {seg, L, t, goz (0..1), alev ({k, u0, u1, seed}), kesik (ışık yanı beyaz vuruş yoğunluğu 0..1), rim (gece kenar ışığı), basK (baş büyüklüğü)}
function adn_ylnTup(C, w, u0, u1, k = 1, pad = 0) {
  const P = new Path2D(), n = C.length - 1, i0 = Math.floor(u0 * n), i1 = Math.ceil(u1 * n);
  for (let i = i0; i <= i1; i++) { const r = Math.max(.5, w(i / n) * k + pad); P.moveTo(C[i][0] + r, C[i][1]); P.arc(C[i][0], C[i][1], r, 0, TAU); }
  return P;
}
function adn_yilan(C, w, o = {}) {
  const { tx, px, tone } = GR, n = C.length - 1, L = o.L || { x: W / 2, y: -200 }, seg = o.seg || [[0, 1]];
  // baş: boyundan belirgin, yassı, yuvarlak burunlu (korkutucu değil: diş, dil yok)
  const hd = C[n], pr = C[Math.max(0, n - 3)], [dx, dy] = adn_nrm(hd[0] - pr[0], hd[1] - pr[1]), hw = w(1) * (o.basK ?? 1.3), a = Math.atan2(dy, dx);
  const HB = (p, q2) => [hd[0] + dx * p - dy * q2, hd[1] + dy * p + dx * q2];
  const HP = new Path2D(); spline(HP, [[-.7, -.78], [.3, -.95], [1.2, -.82], [1.8, -.42], [1.98, .02], [1.75, .42], [1.1, .7], [.2, .8], [-.7, .74]].map(([p, q2]) => HB(p * hw, q2 * hw)), true, .5);
  let acc = null;
  seg.forEach(([u0, u1]) => {
    const P = adn_ylnTup(C, w, u0, u1);
    if (u1 >= 1) P.addPath(HP);
    if (acc) { tx.save(); tx.clip(acc); tx.fillStyle = tone(.95); tx.fill(adn_ylnTup(C, w, Math.max(0, u0 + .004), Math.min(1, u1 - .004), 1, o.ayir ?? 4.5)); if (u1 >= 1) { tx.lineWidth = 9; tx.strokeStyle = tone(.95); tx.stroke(HP); } tx.restore(); }
    adn_doldur(P, o.v ?? .02, a, 0);
    // ışık yanı: kenar ışığı (gece) ve kesitten içe giren kısa beyaz vuruşlar (pul yerine)
    tx.save(); tx.clip(P);
    const i0 = Math.ceil(u0 * n) + 1, i1 = Math.floor(u1 * n) - 1, run = [];
    const flush = () => { if (run.length > 4 && o.rim) adn_cizgi(run.slice(), o.rim, .95, .5); run.length = 0; };
    let last = -1e9, s = 0;
    for (let i = Math.max(1, i0); i <= Math.min(n - 1, i1); i++) {
      const [tx_, ty_] = adn_nrm(C[i + 1][0] - C[i - 1][0], C[i + 1][1] - C[i - 1][1]), r = w(i / n);
      let nx = -ty_, ny = tx_; const [lx, ly] = adn_nrm(L.x - C[i][0], L.y - C[i][1]); if (nx * lx + ny * ly < 0) { nx = -nx; ny = -ny; }
      const fl = nx * lx + ny * ly;
      s += Math.hypot(C[i][0] - C[i - 1][0], C[i][1] - C[i - 1][1]);
      if (fl > .2 && i / n < .97) run.push([C[i][0] + nx * (r - 5), C[i][1] + ny * (r - 5)]); else flush();
      if ((o.kesik ?? 1) > 0 && fl > .35 && i / n < .95 && s - last > r * (2.4 / (o.kesik ?? 1)) * (.8 + .4 * hash(i * 1.7))) {
        last = s; const ln = r * (.5 + .35 * hash(i * 3.1)) * fl, pts = [];
        for (let m = 0; m <= 5; m++) { const u = m / 5; pts.push([C[i][0] + nx * (r - 2) - nx * ln * u - tx_ * r * .45 * u * u, C[i][1] + ny * (r - 2) - ny * ln * u - ty_ * r * .45 * u * u]); }
        adn_sivri(pts, Math.max(3.2, r * .15), .97);
      }
    }
    flush();
    // karın plakaları: yükselen gövdenin karın yanında sık, kısa enine beyaz vuruşlar (yılan okuması)
    const K = o.karin;
    if (K) { let ls = -1e9, ss = 0;
      for (let i = Math.max(1, Math.ceil(Math.max(u0, K.u0) * n)); i <= Math.min(n - 1, Math.floor(Math.min(u1, K.u1) * n)); i++) {
        ss += Math.hypot(C[i][0] - C[i - 1][0], C[i][1] - C[i - 1][1]); if (ss - ls < (K.ara ?? 11)) continue; ls = ss;
        const [tx_, ty_] = adn_nrm(C[i + 1][0] - C[i - 1][0], C[i + 1][1] - C[i - 1][1]); let nx = -ty_, ny = tx_; if (nx * K.d[0] + ny * K.d[1] < 0) { nx = -nx; ny = -ny; }
        const r = w(i / n), e = Math.sin(PI * clamp((i / n - K.u0) / (K.u1 - K.u0))), ln = r * .42 * Math.pow(e, .5);
        if (ln < 4) continue;
        adn_sivri([[C[i][0] + nx * (r - 1), C[i][1] + ny * (r - 1)], [C[i][0] + nx * (r - ln), C[i][1] + ny * (r - ln)]], 4, K.v ?? .9);
      } }
    tx.restore();
    if (!acc) acc = new Path2D(); acc.addPath(P);
  });
  // iç alev: gövdenin en kalın yerinde badem biçimli pencere (siyah iç); alttan yükselen küçük kâğıt beyazı diller
  if (o.alev && o.alev.k > .02) {
    const A = o.alev, i = Math.round(A.u * n), p0 = C[Math.max(0, i - 2)], p1 = C[Math.min(n, i + 2)], [ux, uy] = adn_nrm(p1[0] - p0[0], p1[1] - p0[1]), r = w(A.u);
    const rx = r * (A.rx ?? .62), ry = r * (A.ry ?? 1.7), an = Math.atan2(uy, ux) - PI / 2, win = new Path2D();
    { const pts = []; for (let k = 0; k < 40; k++) { const a2 = k / 40 * TAU, e = Math.pow(Math.abs(Math.cos(a2)), .8) * Math.sign(Math.cos(a2)); pts.push([C[i][0] + Math.cos(an) * rx * Math.sin(a2) * 1 - Math.sin(an) * ry * e, C[i][1] + Math.sin(an) * rx * Math.sin(a2) + Math.cos(an) * ry * e]); }
      poly(win, pts, true); }
    GR.save(); tx.clip(win); px.clip(win);
    const by = C[i][1] + ry * .95;
    adn_alevler(C[i][0], by, rx * 1.9, ry * 1.85 * A.k, o.t || 0, A.seed || 11, A.n ?? 3);
    GR.restore();
  }
  // göz: tek ince ışık
  const g = clamp(o.goz ?? 1);
  if (g > .02) { const sd = o.gozY ?? (dx >= 0 ? -1 : 1), e = HB(hw * 1.05, hw * .4 * sd); tx.fillStyle = tone(1); tx.beginPath(); tx.ellipse(e[0], e[1], Math.max(2.5, hw * .25), Math.max(1.1, hw * .075) * g, a, 0, TAU); tx.fill(); }
  return { HP, head: hd, dir: [dx, dy], hw, HB };
}
// sarmal çizim sırası: arka yarım halkalar (dıştan içe), sonra çağıranın verdiği ara parçalar, sonra ön yarım halkalar (içten dışa)
function adn_sarmalSira(C, n1, after) {
  const n = C.length - 1, cy = C.slice(0, n1 + 1).reduce((a, p) => a + p[1], 0) / (n1 + 1), back = [], front = [];
  let s = 0, fr = C[0][1] > cy;
  for (let i = 1; i <= n1; i++) { const f = C[i][1] > cy; if (f !== fr || i === n1) { (fr ? front : back).push([s / n, i / n]); s = i; fr = f; } }
  return [...back, ...after, ...front.reverse()];
}
// küçük alev öbeği (kâğıt beyazı diller + içinde sivrilen mürekkep vuruşları): taban (x, y), genişlik w, boy h
function adn_alevler(x, y, w, h, t, seed, n = 3) {
  const q = rng(seed);
  for (let i = 0; i < n; i++) { const f = n === 1 ? .5 : i / (n - 1), big = i === Math.floor(n / 2) ? 1 : .62 + q() * .2;
    adn_dil(x + (f - .5) * w * .5, y, h * big, w * (n === 1 ? .8 : .55), (f - .5) * .35, t, seed * 7 + i); }
}
// tek alev dili: tabandan (x, y) ang yönünde (0 yukarı) boy h, genişlik w; uç yavaşça salınır
function adn_dil(x, y, h, w, ang, t, seed) {
  if (h < 3) return;
  const sw = .16 * Math.sin(t * 1.5 + seed * 1.3) + .12 * noise1(t * .5, seed), c = Math.cos(ang), s = Math.sin(ang);
  const T = ([a, b]) => [x + a * c - b * s, y + a * s + b * c];
  const pts = [[-w * .5, 0], [-w * .56, -h * .22], [-w * .38 + sw * h * .12, -h * .5], [-w * .12 + sw * h * .55, -h * .82], [sw * h, -h], [w * .1 + sw * h * .5, -h * .76], [w * .36 + sw * h * .14, -h * .46], [w * .55, -h * .2], [w * .5, 0], [0, h * .08]].map(T);
  const P = new Path2D(); spline(P, pts, true, .45);
  GR.tx.fillStyle = GR.tone(.99); GR.tx.fill(P);
  if (h > 26) { GR.tx.save(); GR.tx.clip(P);
    adn_cizgi([T([w * .04, -h * .04]), T([sw * h * .1, -h * .25]), T([sw * h * .3 - w * .05, -h * .52])], Math.max(3.2, w * .15), .03, .6);
    if (h > 60) adn_cizgi([T([-w * .3, -h * .02]), T([-w * .3 + sw * h * .05, -h * .24])], Math.max(3, w * .1), .03, .6);
    GR.tx.restore(); }
}
// merkez çizgisi yardımcıları
function adn_spl(K, n = 200) { // Catmull-Rom ile yoğun nokta dizisi
  const out = [], m = K.length;
  const cr = (p0, p1, p2, p3, t) => { const t2 = t * t, t3 = t2 * t; return [0, 1].map(j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)); };
  for (let i = 0; i <= n; i++) { const u = i / n * (m - 1), s = Math.min(m - 2, Math.floor(u)); out.push(cr(K[Math.max(0, s - 1)], K[s], K[s + 1], K[Math.min(m - 1, s + 2)], u - s)); }
  return out;
}
// sarmal (yerde kıvrık yılan): merkez (cx, cy), yarıçap r0 → r1, tur, yassılık sq; başlangıç açısı a0
function adn_sarmal(cx, cy, r0, r1, tur, sq, a0 = 0, n = 120) {
  const out = []; for (let i = 0; i <= n; i++) { const u = i / n, a = a0 + u * tur * TAU, r = lerp(r0, r1, u); out.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r * sq]); }
  return out;
}

// ═════════ ortak: yazılar ═════════
// açık levhada alıntı (panel yok, mürekkep harf)
function adn_alintiA(ctx, s, x, y, lt, o = {}) { quote(ctx, s, x, y, lt, Object.assign({ panel: false, col: INK_CSS, px: 68 }, o)); }

// ═════════ ortak setler ═════════
// Aden gündüzü, bahçe içi: gök, uzak tepeler, çayır. L ışık; hz ufuk
function adn_gunduz(L, hz, o = {}) {
  cen_gok(L, { r0: o.r0 ?? 380, r1: o.r1 ?? 1500, v: o.v ?? .72, n: o.n ?? 96 });
  if (o.tepe !== false) adn_tepe(hz + 4, o.tepeA ?? 34, o.tepeS ?? 3, { v: .62 });
  adn_zemin(hz, Object.assign({ v0: .88, v1: .95, v2: .985 }, o.zemin || {}));
}

// ═════════ P099 (I06): sabah; uzakta Havva (arkadan), önde dik duran yılan; içindeki alev bir an söner ═════════
// Yılanın merkez çizgisi: yerde iki halkalı sarmal, iç ucundan yükselen S kavisli gövde, Havva'ya dönük baş.
// yum: 0 dik … 1 yumuşamış (baş iner ve öne eğilir, boyun gevşer). k: ölçek
const ADN_I06_N1 = 110;
function adn_i06Ylan(cx, cy, k, yum) {
  const P = (x, y) => [cx + x * k, cy + y * k];
  const g = adn_spl([P(400, 60), P(290, 84), P(150, 86), P(10, 62), P(-80, 20), P(-60, -26), P(40, -38), P(120, -10), P(100, 18)], ADN_I06_N1), e = g[g.length - 1], hy = 52 * yum * k, hx = -34 * yum * k;
  const rise = adn_spl([e, [e[0] - 12 * k, e[1] - 60 * k], [e[0] + 8 * k, e[1] - 150 * k], [e[0] + 16 * k, e[1] - 240 * k], [e[0] - 8 * k + hx * .25, e[1] - 318 * k + hy * .35],
    [e[0] - 52 * k + hx * .6, e[1] - 366 * k + hy * .75], [e[0] - 102 * k + hx, e[1] - 378 * k + hy], [e[0] - 130 * k + hx * 1.1, e[1] - 370 * k + hy * 1.15]], 90);
  return g.concat(rise.slice(1));
}
// yarı genişlik: kuyruk ince, yerdeki gövde kalın, yükselen gövde yukarı doğru incelir; başın arkasında boyun
const adn_ylnW = (k, n1 = ADN_I06_N1, n = 200) => { const ur = n1 / n; return u => k * (u < ur ? lerp(5, 46, smooth(clamp(u / (ur * .75)))) : lerp(46, 31, smooth(clamp((u - ur) / (1 - ur)))) * (u > .93 ? lerp(1, .8, smooth((u - .93) / .07)) : 1)); };
function adn_i06(t, o = {}) {
  const L = { x: 1190, y: 250 }, HZ = 700;
  adn_gunduz(L, HZ, { r0: 420, tepeA: 26 });
  // sol: Havva'nın arkasındaki koyu ağaç ve çit kütlesi
  adn_govde(250, 700, 400, 44, 22, { dallar: [[.75, -.75, 120, 16], [.88, .65, 105, 12]], L });
  adn_tac({ x: 230, y: 330, r: 245, seed: 4, L, n: 8, wx: 1.25, sq: .7 });
  adn_tac({ x: -130, y: 470, r: 230, seed: 6, L, n: 6 });
  adn_cali({ x0: -200, x1: 860, y: 668, amp: 54, wl: 120, seed: 2, yb: 840, L, cuts: .8, tooth: 9, endW: 150 });
  // uzak sağ: ufukta küçük ağaç öbeği (sağ kenarın çapası)
  adn_tac({ x: 1890, y: 560, r: 150, seed: 9, L, n: 5, cuts: .6 });
  adn_cali({ x0: 1640, x1: 2200, y: 694, amp: 26, wl: 70, seed: 8, yb: 760, L, cuts: .5, tooth: 6, endW: 110 });
  // Havva: uzak, örtülü, arkadan; koyu çitin önünde
  adn_insan(470, 784, 13, { sac: true, seed: 5, kat: 2 });
  // çiçekli ön bant (eteğini örter)
  const cb = adn_cali({ x0: -200, x1: 900, y: 800, amp: 16, wl: 60, seed: 12, yb: 860, L, cuts: .3, tooth: 6, endW: 160, endD: 70 });
  adn_cicek(cb.top.filter(p => p[0] < 820), { seed: 21, d: .07, r: 8, depth: 22 });
  // yılan
  const C = adn_i06Ylan(1380, 940, 1, o.yum || 0), n = C.length - 1, ur = ADN_I06_N1 / n;
  adn_yilan(C, adn_ylnW(1), { L, t, seg: [[0, ur], [ur, 1]], basK: 1.45, alev: { k: o.alev ?? 1, u: ur + .14, seed: 13 },
    goz: o.goz ?? 1, kesik: .7 });
  // ön plan: alçak koyu ot bandı (karenin alt çapası)
  adn_cali({ x0: -200, x1: 2200, y: 1052, amp: 24, wl: 110, seed: 14, yb: 1300, L, cuts: .5, tooth: 7, ends: false });
}
function adn_i06Alev(t) {
  const k = kf(t, [[S('I06'), 1], [Wd('I06', 'nefreti'), 1], [Wd('I06', 'hilesi'), .8], [Wd('I06', 'kıskançlığı'), .64], [Wd('I06', 'intikamı'), .48], [Wd('I06', 'düşer'), .32],
    [Wd('I06', 'sersem'), .24], [Wd('I06', 'iyilik'), 0, E.io2]]);
  return k * (1 + .05 * Math.sin(t * 2.1));
}
plan('P099', (ctx, st) => {
  const t = st.t, yum = E.io2(adn_u(t, Wd('I06', 'kopup'), Wd('I06', 'durur') + .8)) * .7 + .3 * E.io2(adn_u(t, Wd('I06', 'sersem'), Wd('I06', 'donakalır')));
  const cam = camLerp({ cx: 900, cy: 540, z: 1 }, { cx: 1000, cy: 540, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => adn_i06(t, { alev: adn_i06Alev(t), yum, goz: 1 - .45 * yum }), [.8, 0, 1]);
}, { tr: ADN_FADE, over: (ctx, st) => {
  adn_alintiA(ctx, 'sersem bir iyilik', 860, 200, st.t - Wd('I06', 'iyilik') + .25, { px: 80 });
} });

// ═════════ P115 (K01): Aden'den çıkış: kapı ve dönen alev; önde geniş ova, gün doğumu; el ele yürüyen iki küçük figür (arkadan) ═════════
// Filmin en ferah karesi: gök ve ova temiz kâğıda yakın; koyu kütle yalnız sol üstte kapı kemeri (çerçeve) ve altta ince zemin bandı.
// Kapının üstünde dönen alev şeridi (figürsüz "alevli kılıç"): iki ucu sivrilen yatay kâğıt beyazı alev kütlesi; diller şerit boyunca akar,
// şeridin ekseni yavaşça döner (±7°). Koyu kemerin önünde.
function adn_alevKilic(cx, cy, len, t, o = {}) {
  const ang = Math.sin(t * .35) * .1;
  GR.frame(cx, cy, ang, 1, 1);
  PR.flameBank(-len / 2, len / 2, 0, o.h ?? 260, t, o.seed ?? 27, { band: false, n: o.n ?? 6, wr: .5, base: .3, edge: .4, core: .8, frags: false, speed: .5, curl: .45, strip: .25, env: f => .3 + .7 * Math.pow(Math.sin(f * PI), .7) });
  GR.unframe();
}
function adn_k01(t, o = {}) {
  const { tx, tone } = GR, L = { x: 1260, y: 655 }, HZ = 662;
  cen_gok(L, { r0: 560, r1: 1750, v: .74, n: 104 });
  // ufuk: ince koyu tepe şeridi; güneşin altını keser
  { const P = new Path2D(); P.moveTo(-1600, HZ + 30); for (let x = -1600; x <= W + 1600; x += 12) P.lineTo(x, HZ - 6 - 10 * Math.abs(Math.sin(x / 260 + 1.3)) - 6 * Math.abs(Math.sin(x / 97)) - 22 * Math.exp(-Math.pow((x - 600) / 160, 2)) - 14 * Math.exp(-Math.pow((x - 1700) / 120, 2)));
    P.lineTo(W + 1600, HZ + 30); P.closePath(); adn_doldur(P, .03); }
  // ova: ufuktan öne açılan çayır; güneşin önünde uzanan temiz kâğıt yol
  adn_zemin(HZ + 8, { v0: .9, v1: .965, v2: .99 });
  { const P = new Path2D(); P.moveTo(L.x - 24, HZ + 10); P.lineTo(L.x + 24, HZ + 10); P.quadraticCurveTo(1150, 900, 1010, H + 40); P.lineTo(640, H + 40); P.quadraticCurveTo(1010, 860, L.x - 24, HZ + 10); P.closePath();
    tx.save(); tx.globalCompositeOperation = 'lighten'; tx.fillStyle = tone(.99); tx.fill(P); tx.restore(); }
  // uzakta seyrek ağaçlar (ufukta küçük koyu taçlar)
  for (const [x, r, s] of [[420, 34, 51], [470, 22, 52], [1660, 30, 53], [1790, 44, 54]]) { adn_govde(x, HZ + 2, HZ - r * .8, 6, 4); adn_tac({ x, y: HZ - r * 1.3, r, seed: s, L, n: 4, tooth: 4, cuts: 0, lobes: 0 }); }
  // figürler: el ele, arkadan, ışığa doğru yürür; kısa, sivrilen gölgeleri öne düşer
  const w = o.yur ?? 0, ph = o.adim ?? 0, x1 = lerp(975, 1035, w), y1 = lerp(902, 852, w), h1 = lerp(14, 12, w), gap = 2.5 * h1;
  const xa = x1 - gap / 2, xb = x1 + gap / 2 - .3 * h1;
  { // iki gölge tek kütle: ayaklardan öne (ışığın tersine) uzanır, sivrilir
    const dx = (x1 - L.x), dy = (y1 - L.y), l = Math.hypot(dx, dy), ux = dx / l, uy = dy / l, len = 12 * h1, P = new Path2D();
    spline(P, [[xa - h1 * 1.2, y1], [xb + h1 * 1.2, y1], [x1 + ux * len * .6 + h1 * 1.1, y1 + uy * len * .6], [x1 + ux * len, y1 + uy * len], [x1 + ux * len * .6 - h1 * 1.6, y1 + uy * len * .6]], true, .35);
    adn_doldur(P, .03);
    const g = new Path2D(); g.rect(x1 - h1 * .15 + ux * len * .1, y1, h1 * .3, len); }
  const hm = [x1 - .15 * h1, y1 - 3.6 * h1];
  adn_insan(xa, y1, h1, { v: .02, el: hm, kol: 1, adim: ph, egik: o.egik || 0 });
  adn_insan(xb, y1, h1 * .95, { v: .02, el: hm, kol: -1, adim: ph + PI, sac: true, egik: (o.egik || 0) * 1.1 });
  // sol üst: kapının kemeri ve sövesi (koyu çerçeve)
  const G = new Path2D(); G.moveTo(-200, -200); G.lineTo(1060, -200); G.lineTo(1060, -70); G.bezierCurveTo(780, 10, 480, 120, 340, 330); G.lineTo(300, 430); G.lineTo(300, H + 200); G.lineTo(-200, H + 200); G.closePath();
  adn_doldur(G, .02);
  { // kemer alnında ince kenar ışığı; taş derzleri: kenardan içe seyrek beyaz vuruşlar
    tx.save(); tx.clip(G);
    adn_cizgi([[1050, -62], [780, 18], [520, 150], [346, 336], [308, 434], [308, 1080]], 7, .95, .25);
    const q = rng(77); for (let y = 500 + q() * 40; y < 1040; y += 110 + q() * 80) adn_sivri([[302, y], [262 - q() * 50, y + 3]], 6, .96);
    for (let i = 0; i < 5; i++) { const u = .1 + i * .17 + q() * .05, b = [[1050, -62], [780, 18], [520, 150], [346, 336]], k = u * 3, j = Math.min(2, Math.floor(k)), f = k - j, p = [lerp(b[j][0], b[j + 1][0], f), lerp(b[j][1], b[j + 1][1], f)];
      adn_sivri([[p[0] - 4, p[1] - 6], [p[0] - 30 - q() * 30, p[1] - 44 - q() * 30]], 6, .96); }
    tx.restore();
  }
  adn_alevKilic(250, 300, 420, t, { n: 6, h: 250 });
  // ön zemin: sol altta sövenin dibinden uzanan alçak koyu ot bandı; sağ altta ince bant
  adn_cali({ x0: -200, x1: 820, y: 1040, amp: 30, wl: 100, seed: 61, yb: 1300, L, cuts: .5, tooth: 7, endW: 240, endD: 120 });
  adn_cali({ x0: 1440, x1: 2300, y: 1068, amp: 20, wl: 80, seed: 62, yb: 1300, L, cuts: .4, tooth: 6, endW: 220, endD: 60 });
}
plan('P115', (ctx, st) => {
  const t = st.t, t0 = S('K01'), tg = Wd('K01', 'gözyaşı'), ts = Wd('K01', 'sildiler');
  // yürüyüş: sürekli, gözyaşında yavaşlar (adım evresi hız integrali); başlar eğilir, "sildiler"de kalkar
  const slow = u => 1 - .75 * E.sine(adn_u(u, tg - 1.2, tg - .2)) * (1 - E.sine(adn_u(u, ts, ts + 1)));
  let ph = 0; for (let u = t0 - 1.4; u < t; u += .05) ph += .05 * 2.6 * slow(u);
  const eg = .55 * E.io2(adn_u(t, tg - 1, tg + .2)) * (1 - E.io2(adn_u(t, ts - .2, ts + .8)));
  const cam = camLerp({ cx: 930, cy: 540, z: 1 }, { cx: 1000, cy: 540, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => adn_k01(t, { yur: adn_u(t, t0 - 1.4, st.end), adim: ph, egik: eg }), [.8, 0, 1]);
}, { tr: { type: 'black', dur: 1.4, end: true }, over: (ctx, st) => {
  adn_alintiA(ctx, '“Bütün dünya önlerindeydi.”', 1300, 330, st.t - Wd('K01', 'bütün') + .15, { px: 72 });
} });

// ═════════ taş duvar ve kapı (H01, H02) ═════════
// Düz siyah duvar; üstte kâğıt beyazı kapak çizgisi, altında seyrek kırık taş sırası çizgileri (aşağı doğru azalır).
// o: {x0, x1, y (üst), yb, seed, kapi: {x, w, h} (doğudaki tek kapı: kemerli açıklık; ardında bahçe ışığı)}
function adn_duvar(o) {
  const { tx } = GR, q = rng(o.seed || 1), y = o.y, yb = o.yb ?? H + 300, P = new Path2D(), top = [];
  for (let x = o.x0; x <= o.x1 + .1; x += 24) top.push([x, y + (q() - .5) * 3]);
  P.moveTo(o.x0, yb); for (const p of top) P.lineTo(p[0], p[1]); P.lineTo(o.x1, yb); P.closePath();
  let K = null;
  if (o.kapi) { const k = o.kapi; K = new Path2D(); K.moveTo(k.x - k.w / 2, yb); K.lineTo(k.x - k.w / 2, k.y + k.w / 2); K.arc(k.x, k.y + k.w / 2, k.w / 2, PI, 0); K.lineTo(k.x + k.w / 2, yb); K.closePath(); P.addPath(K); }
  GR.fill(P, GR.tone(.02), { th: 0, id: 0 }, 'evenodd');
  tx.save(); tx.clip(P, 'evenodd');
  adn_cizgi(top.map(p => [p[0], p[1] + 9]), 5.5, .95, .15);
  const rows = o.rows ?? 5;
  for (let r = 0; r < rows; r++) { const yy = y + 40 + r * (50 + q() * 16); let x = o.x0 + q() * 120;
    while (x < o.x1) { const len = 70 + q() * 210; if (q() < .55 - r * .07) adn_cizgi([[x, yy], [x + len / 2, yy + (q() - .5) * 2], [x + len, yy]], 4.6 * (1 - r * .1), .94, .3);
      if (q() < .3 - r * .04) adn_sivri([[x + len + 14, yy + 2], [x + len + 16, yy + 30]], 4, .93);
      x += len + 40 + q() * 140; } }
  if (o.kapi) { const k = o.kapi; adn_cizgi([[k.x - k.w / 2 - 12, yb], [k.x - k.w / 2 - 12, k.y + k.w / 2], [k.x - k.w * .36, k.y - k.w * .05], [k.x, k.y - 12]], 6, .95, .2); }
  tx.restore();
  return P;
}
// Aden'in dışından: duvarın ardında ağaç tepeleri. o: {y (duvar üstü), L, kapi, crowns}
function adn_bahceDis(t, o) {
  const L = o.L;
  cen_gok(L, { r0: o.r0 ?? 460, r1: 1600, v: .72, n: 96 });
  for (const c of o.crowns) adn_tac(Object.assign({ L, n: 6 }, c));
  if (o.kapi) { // kapının ardında bahçenin aydınlık zemini ve uzak taçlar
    const k = o.kapi, g = new Path2D(); g.rect(k.x - k.w, k.y + k.h * .55, k.w * 2, 400); GR.fill(g, GR.tone(.97), { th: 0, id: 1 }); }
  return adn_duvar({ x0: -300, x1: W + 300, y: o.y, seed: 11, kapi: o.kapi, rows: 5 });
}

// ═════════ P083 (H01): bölüm kartı "ADEN'DE BİR YABANCI"; bahçenin duvarı ve ağaç tepeleri ═════════
function adn_h01(t) {
  const L = { x: 960, y: 170 };
  adn_bahceDis(t, { L, y: 730, r0: 600, crowns: [{ x: 120, y: 740, r: 200, seed: 21 }, { x: 430, y: 760, r: 150, seed: 22 }, { x: 1480, y: 750, r: 180, seed: 23 }, { x: 1800, y: 730, r: 210, seed: 24 }, { x: 980, y: 800, r: 120, seed: 25, n: 4 }] });
}
plan('P083', (ctx, st) => levha(ctx, camLerp({ cx: 940, cy: 540 }, { cx: 980, cy: 540 }, st.p, E.sine), () => adn_h01(st.t), [.8, 0, 1]),
  { tr: { type: 'black', dur: 1.4, end: true }, over: (ctx, st) => cen_kart(ctx, "ADEN'DE BİR YABANCI", 'Yok etmeye geldiğin bir şeyi, sevebilir misin?', st.lt, st.d) });

// ═════════ P084 (H02): duvarın üstünden tek sıçrayış ═════════
// Kamera kapıdan (sağ) sola kayar; "sıçrayışta" koyu kanatlı siluet ön plandan duvarın üstüne yay çizer, bahçeye iner (duvarın ardında kaybolur).
function adn_h02(t) {
  const L = { x: 1100, y: 200 }, tS = Wd('H02', 'sıçrayışta') - .35, tA = Wd('H02', 'atlar') + .55, u = adn_u(t, tS, tA), WY = 600;
  const crowns = [{ x: 150, y: 600, r: 190, seed: 31 }, { x: 520, y: 640, r: 150, seed: 32 }, { x: 980, y: 590, r: 200, seed: 33 }, { x: 1380, y: 630, r: 150, seed: 34 }, { x: 1900, y: 600, r: 220, seed: 35 }];
  // figür: yay (kalça); öncesinde ön planda hafif çömelmiş bekler
  const x0 = 330, y0 = 1040, x2 = 1180, y2 = 760, ue = E.io2(u), hk = 470;
  const fx = lerp(x0, x2, ue), gy = lerp(y0, y2, ue) - hk * 4 * ue * (1 - ue), h = lerp(44, 34, ue), crouch = (1 - E.out2(adn_u(t, tS - .5, tS))) * 0 + Math.sin(PI * clamp(u * 3)) * 0;
  const fig = () => kiy_seytan(t, { x: fx, gy, h, lum: .15, facing: 1, lit: [-.1, -1], lean: lerp(.05, .35, Math.sin(PI * u)), head: .15 - .2 * u,
    open: E.sine(clamp(u * 2.2)) * (1 - E.sine(adn_u(u, .75, 1))) * .9 + .1, lift: E.sine(clamp(u * 2)) * .8,
    legN: [lerp(.1, .7, Math.sin(PI * u)), lerp(-.05, -1.5, Math.sin(PI * u))], legF: [lerp(-.1, .35, Math.sin(PI * u)), lerp(-.03, -1.3, Math.sin(PI * u))],
    armN: [lerp(.15, -.6, Math.sin(PI * u)), .3], armF: [lerp(-.12, .4, Math.sin(PI * u)), .2] });
  const behind = u > .55;
  const L2 = L;
  cen_gok(L2, { r0: 440, r1: 1600, v: .72, n: 96 });
  for (const c of crowns) adn_tac(Object.assign({ L: L2, n: 6 }, c));
  const k = { x: 1600, w: 150, y: WY + 70, h: 240 };
  { const g = new Path2D(); g.rect(k.x - k.w, k.y + 60, k.w * 2, 400); GR.fill(g, GR.tone(.97), { th: 0, id: 1 }); }
  if (behind && u < 1) fig();
  adn_duvar({ x0: -300, x1: W + 300, y: WY, yb: 880, seed: 12, kapi: k, rows: 4 });
  // dış zemin: duvarın dibinden öne açık çayır; en önde koyu ot bandı
  adn_zemin(880, { v0: .9, v1: .96, v2: .985 });
  if (!behind) fig();
  adn_cali({ x0: -300, x1: W + 300, y: 1050, amp: 26, wl: 110, seed: 36, yb: 1300, L, cuts: .5, tooth: 7, ends: false });
}
plan('P084', (ctx, st) => {
  const t = st.t, p = E.io2(adn_u(t, S('H02'), Wd('H02', 'tek', 1) - .2));
  levha(ctx, camLerp({ cx: 1160, cy: 540 }, { cx: 900, cy: 540 }, p, E.lin), () => adn_h02(t), [.8, 0, 1]);
}, { tr: ADN_FADE, mb: 3 });

// ═════════ P085 (H03): hayat ağacının tepesinde karabatak; kanat toplar, gözü parlar ═════════
function adn_h03(t) {
  const L = { x: 1290, y: 300 }, HZ = 790, tT = Wd('H03', 'tüner'), tK = Wd('H03', 'karabatak');
  adn_gunduz(L, HZ, { r0: 380, tepeA: 24 });
  adn_tac({ x: 260, y: 1010, r: 260, seed: 41, L, n: 7 });
  adn_tac({ x: 1720, y: 1030, r: 280, seed: 42, L, n: 7 });
  // hayat ağacı: en yüksek; geniş, katlı taç; tepede tek dal
  adn_tac({ x: 980, y: 1000, r: 380, seed: 43, L, n: 9, wx: 1.15, sq: .62 });
  adn_tac({ x: 990, y: 720, r: 210, seed: 44, L, n: 7, wx: 1.1, sq: .7 });
  adn_sivri([[992, 600], [1000, 540], [1006, 492]], 16);
  adn_sivri([[1003, 520], [1050, 506], [1080, 508]], 8);
  const kn = 1 - E.io2(adn_u(t, tT - .2, tT + 1.1)), fl = Math.sin(t * 2.2) * .08 * kn;
  adn_kus(1008, 494, 150, { f: -1, kanat: kn * .95 + fl, L, t, goz: .35 + .65 * E.out2(adn_u(t, tK - .1, tK + .5)), bas: -.08 });
}
plan('P085', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540 }, { cx: 1010, cy: 540 }, st.p, E.sine), () => adn_h03(st.t), [.8, 0, 1]), { tr: ADN_FADE });

// ═════════ P086 (H04): ağacın tepesinden bakış: uzakta, yaprakların arasında iki küçük örtülü siluet (arkadan) ═════════
function adn_h04(t) {
  const L = { x: 1130, y: 330 }, HZ = 640;
  adn_gunduz(L, HZ, { r0: 360, tepeA: 22 });
  // uzak açıklık: koyu ağaç kütlesi, önünde yan yana iki küçük açık figür
  adn_tac({ x: 1180, y: 560, r: 170, seed: 51, L, n: 7 });
  adn_tac({ x: 1420, y: 610, r: 120, seed: 52, L, n: 5 });
  adn_cali({ x0: 940, x1: 1600, y: 662, amp: 30, wl: 80, seed: 53, yb: 700, L, cuts: .5, tooth: 6, endW: 120, endD: 50 });
  const hm = [1180, 700 - 3.5 * 8];
  adn_insan(1163, 700, 8, { el: hm, kol: 1, seed: 6, kat: 0 });
  adn_insan(1197, 700, 7.6, { el: hm, kol: -1, sac: true, seed: 7, kat: 0 });
  // ön plan: yaprak kütleleri çerçeve (sol üst, sağ, alt)
  adn_tac({ x: -60, y: 60, r: 330, seed: 54, L, n: 7 });
  adn_tac({ x: 1980, y: 380, r: 300, seed: 55, L, n: 7 });
  adn_cali({ x0: -300, x1: W + 300, y: 960, amp: 80, wl: 170, seed: 56, yb: 1400, L, cuts: .7, tooth: 10, ends: false });
  // karabatağın başı ve boynu (omuz üstü bakış; sol alt)
  adn_kus(260, 1140, 560, { f: 1, kanat: 0, L, t, goz: 1, bas: .25 + Math.sin(t * .4) * .02 });
}
plan('P086', (ctx, st) => levha(ctx, camLerp({ cx: 990, cy: 540 }, { cx: 930, cy: 540 }, st.p, E.sine), () => adn_h04(st.t), [.8, 0, 1]), { tr: ADN_FADE });

// ═════════ P087 (H05): karabatağın gölgesi yerde hâlâ melek biçiminde; “Onları sevebilirim bile.” ═════════
// Alçak güneş solda; ağacın gölgesi çayırda sağa uzar, ucunda kuşun gölgesi kanatlı bir melek biçiminde yatar.
function adn_golgeMelek(X0, Y0, len, k, br) {
  // önden kanatları kalkık melek (yerel: x genişlik, y ayaktan yukarı 0..1) → yere yatırılmış (dünya: X0 + y*len, Y0 + x*len*k)
  const M = ([x, y]) => [X0 + y * len, Y0 + x * len * k];
  const body = [[-.07, 0], [-.1, .32], [-.085, .6], [-.04, .66], [.04, .66], [.085, .6], [.1, .32], [.07, 0]];
  const P = new Path2D(); spline(P, body.map(M), true, .4);
  const Hd = new Path2D(); { const c = M([0, .73]); Hd.ellipse(c[0], c[1], .055 * len, .05 * len * k, 0, 0, TAU); } P.addPath(Hd);
  for (const sd of [-1, 1]) { const w = [[.05, .62], [.2, .8 + br], [.4, .98 + br], [.46, .9 + br], [.4, .72], [.36, .6], [.3, .5], [.22, .42], [.1, .48]].map(([x, y]) => [x * sd, y]);
    const Wp = new Path2D(); spline(Wp, w.map(M), true, .4); P.addPath(Wp); }
  return P;
}
function adn_h05(t) {
  const L = { x: 220, y: 600 }, HZ = 650;
  adn_gunduz(L, HZ, { r0: 330, r1: 1700, tepeA: 22, zemin: { v0: .9, v1: .97, v2: .99 } });
  // gölgeler: gövde gölgesi sağa uzanan sivrilen şerit, taç gölgesi, kuşun melek gölgesi
  const br = Math.sin(t * .5) * .015;
  { const P = new Path2D(); spline(P, [[560, 812], [900, 826], [1130, 840], [1140, 862], [900, 850], [560, 828]], true, .4); adn_doldur(P, .03); }
  { const P = new Path2D(); const pts = []; for (let i = 0; i < 60; i++) { const a = i / 60 * TAU; pts.push([1210 + Math.cos(a) * 130 * (1 + .1 * Math.sin(a * 5)), 852 + Math.sin(a) * 34 * (1 + .1 * Math.cos(a * 4))]); }
    poly(P, adn_dis(pts, true, { seed: 61, h: 6, l0: 8, l1: 16 }), true); adn_doldur(P, .03); }
  adn_doldur(adn_golgeMelek(1320, 858, 470, .36, br), .03);
  // ağaç ve tepede kuş
  adn_govde(520, 820, 470, 34, 18, { dallar: [[.8, .7, 90, 12]], L });
  adn_tac({ x: 520, y: 360, r: 190, seed: 62, L, n: 7 });
  adn_sivri([[525, 205], [532, 160]], 9);
  adn_kus(532, 166, 64, { f: 1, kanat: 0, L, t, goz: 1, bas: .1 });
  adn_tac({ x: -40, y: 520, r: 200, seed: 63, L, n: 6 });
  adn_cali({ x0: -300, x1: W + 300, y: 1056, amp: 22, wl: 100, seed: 64, yb: 1300, L, cuts: .5, tooth: 6, ends: false });
}
plan('P087', (ctx, st) => levha(ctx, camLerp({ cx: 940, cy: 540 }, { cx: 1000, cy: 540 }, st.p, E.sine), () => adn_h05(st.t), [.8, 0, 1]),
  { tr: ADN_FADE, over: (ctx, st) => adn_alintiA(ctx, '“Onları sevebilirim bile.”', 1330, 250, st.t - Wd('H05', 'sevebilirim') + .3, { px: 72 }) });

// ═════════ P088 (H06): içindeki alev küçülür; sonra yeniden büyür ═════════
function adn_h06(t) {
  const L = { x: 560, y: 260 }, tY = Wd('H06', 'yumuşuyor'), tE = Wd('H06', 'ekler'), tI = Wd('H06', 'intikamı');
  cen_gok(L, { r0: 380, r1: 1500, v: .72, n: 96 });
  adn_tac({ x: 1880, y: 520, r: 330, seed: 71, L, n: 7 });
  adn_cali({ x0: -300, x1: W + 300, y: 1030, amp: 70, wl: 160, seed: 72, yb: 1400, L, cuts: .6, tooth: 9, ends: false });
  // kalın dal: sağdan girer
  { const P = new Path2D(); spline(P, [[2000, 820], [1500, 850], [1150, 900], [1050, 930], [1160, 922], [1520, 885], [2000, 870]], true, .4); adn_doldur(P, .02); }
  adn_tac({ x: 1120, y: 960, r: 90, seed: 73, L, n: 4 });
  const k = kf(t, [[S('H06'), 1], [Wd('H06', 'karşısında'), 1], [tY + .6, .22, E.io2], [tE - .2, .22], [tE + .9, 1, E.out2], [tI, 1.05], [tI + 1, 1.32, E.io2]]) * (1 + .05 * Math.sin(t * 2.3));
  const bas = .1 + .18 * E.io2(adn_u(t, tY - .5, tY + .8)) - .26 * E.io2(adn_u(t, tE - .3, tE + .6));
  adn_kus(1290, 880, 430, { f: -1, kanat: 0, L, t, goz: 1, bas, alev: { k, seed: 9 } });
}
plan('P088', (ctx, st) => levha(ctx, camLerp({ cx: 990, cy: 540 }, { cx: 950, cy: 540 }, st.p, E.sine), () => adn_h06(st.t), [.8, 0, 1]), { tr: ADN_FADE });

// ═════════ P090 (H08): iki küçük siluet el ele; ön planda başını çeviren koyu kuş; “Bense… bir cehenneme itildim.” ═════════
function adn_h08(t) {
  const L = { x: 690, y: 330 }, HZ = 690, tN = Wd('H08', 'nefret');
  adn_gunduz(L, HZ, { r0: 400, tepeA: 26 });
  adn_tac({ x: 700, y: 520, r: 190, seed: 81, L, n: 7 });
  adn_tac({ x: 380, y: 560, r: 150, seed: 82, L, n: 6 });
  adn_cali({ x0: 160, x1: 1020, y: 680, amp: 44, wl: 110, seed: 83, yb: 800, L, cuts: .7, tooth: 8, endW: 140 });
  const hm = [708, 780 - 3.5 * 11];
  adn_insan(684, 780, 11, { el: hm, kol: 1, seed: 8 });
  adn_insan(732, 780, 10.5, { el: hm, kol: -1, sac: true, seed: 9 });
  const cb = adn_cali({ x0: 100, x1: 1100, y: 794, amp: 14, wl: 60, seed: 84, yb: 840, L, cuts: .3, tooth: 5, endW: 150, endD: 50 });
  adn_cicek(cb.top.filter(p => p[0] > 160 && p[0] < 1040), { seed: 85, d: .06, r: 7, depth: 18 });
  // ön plan sağ: dal ve kuş; "nefret"te başını çevirir
  adn_tac({ x: 1990, y: 300, r: 300, seed: 86, L, n: 7 });
  { const P = new Path2D(); spline(P, [[2000, 860], [1650, 880], [1380, 920], [1320, 940], [1400, 940], [1660, 905], [2000, 900]], true, .4); adn_doldur(P, .02); }
  adn_cali({ x0: -300, x1: W + 300, y: 1050, amp: 26, wl: 110, seed: 87, yb: 1300, L, cuts: .5, tooth: 7, ends: false });
  adn_kus(1560, 900, 360, { f: -1, kanat: 0, L, t, goz: 1, bas: .12, don: E.io2(adn_u(t, tN - .1, tN + .9)) });
}
plan('P090', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540 }, { cx: 1010, cy: 540 }, st.p, E.sine), () => adn_h08(st.t), [.8, 0, 1]),
  { tr: ADN_FADE, over: (ctx, st) => adn_alintiA(ctx, '“Bense… bir cehenneme itildim.”', 820, 165, st.t - Wd('H08', 'bense') + .3, { px: 70 }) });

// ═════════ gece: çardak (H09, H10) ═════════
// Çardak: iki ağaç tacının kavuştuğu koyu kemer; içi zifiri. Ay ışığı ince huzmelerle uyuyan figürün örtüsüne düşer (temiz kâğıt kütle).
const ADN_AY = { x: 1520, y: 190, r: 52 };
function adn_cardak(t, o = {}) {
  const M = ADN_AY, L = M, HZ = 700;
  adn_gece(M, { R: 900, rays: 7 });
  adn_tac({ x: 1820, y: 640, r: 160, seed: 91, L, n: 6, rim: 4, cuts: .5, lobes: .6 });
  adn_geceZemin(HZ, { v0: .16 });
  adn_leke(1350, 860, 240, 30, 92); adn_leke(1700, 960, 200, 34, 93); adn_leke(1180, 1010, 140, 22, 94);
  // çardak: iki taç + gövdeler
  adn_govde(240, 900, 300, 50, 26, { L, rw: 4, dallar: [[.9, .6, 160, 16]] });
  adn_govde(1150, 900, 330, 46, 24, { L, rw: 4, dallar: [[.88, -.7, 170, 16]] });
  adn_tac({ x: 420, y: 260, r: 360, seed: 95, L, n: 8, wx: 1.3, sq: .6, rim: 5, cuts: .8, lobes: .8 });
  adn_tac({ x: 1010, y: 250, r: 330, seed: 96, L, n: 8, wx: 1.3, sq: .6, rim: 5, cuts: .8, lobes: .8 });
  // ay huzmeleri: çardağın aralığından örtüye
  for (let i = 0; i < 3; i++) adn_cizgi([[1250 - i * 30, 330 + i * 10], [lerp(1250 - i * 30, 760 + i * 40, .5), lerp(330, 740, .5)], [760 + i * 40, 740]], 7 - i, .96, .5);
  // uyuyan figür: örtü altında uzun alçak kütle (yüz yok); başı solda
  const P = new Path2D(); spline(P, [[560, 812], [566, 770], [600, 752], [640, 760], [700, 752], [800, 760], [890, 772], [930, 800], [920, 814]], true, .5);
  adn_doldur(P, .975, PI / 2, 10);
  GR.tx.save(); GR.tx.clip(P);
  adn_cizgi([[650, 812], [680, 780], [720, 770]], 4, .03, .5); adn_cizgi([[780, 812], [820, 786], [870, 780]], 4, .03, .5); adn_cizgi([[600, 812], [612, 785]], 3.5, .03, .5);
  GR.tx.restore();
  // ön plan: koyu ot bandı
  adn_cali({ x0: -300, x1: W + 300, y: 1050, amp: 30, wl: 110, seed: 97, yb: 1300, L, cuts: .4, tooth: 7, ends: false, rim: 3 });
  return { M };
}
// rüya dumanı: kurbağanın ağzından başa doğru kıvrılan ince kâğıt çizgiler
function adn_ruya(x, y, t, a = 1) {
  if (a <= 0) return;
  for (let k = 0; k < 3; k++) {
    const pts = [], ph = t * .5 + k * 2.1, len = (120 + k * 30) * a;
    for (let i = 0; i <= 16; i++) { const u = i / 16, s = u * len, curl = u > .6 ? (u - .6) * 2.5 : 0;
      pts.push([x - s * .65 + Math.sin(ph + u * 4) * 8 + Math.cos(ph * .7 + k + curl * 5) * 26 * curl, y - s * .55 - k * 8 + Math.sin(ph * .7 + k + curl * 5) * 26 * curl]); }
    adn_cizgi(pts, 5 - k, .96, .5);
  }
}
// ═════════ P091 (H09): gece; çardakta uyuyan uzak figür; kulağının yakınında küçük kurbağa; rüya dumanı ═════════
plan('P091', (ctx, st) => {
  const t = st.t, tK = Wd('H09', 'kurbağa'), tR = Wd('H09', 'rüyalar');
  levha(ctx, camLerp({ cx: 1000, cy: 540 }, { cx: 940, cy: 540 }, st.p, E.sine), () => {
    adn_cardak(t);
    adn_kurbaga(640, 760, 50, { f: -1, L: ADN_AY, nefes: Math.sin(t * 1.4) });
    adn_ruya(612, 744, t, E.io2(adn_u(t, tR - 1.2, tR + .8)));
  }, [.04, 0, 1]);
}, { tr: ADN_FADE });

// ═════════ P092 (H10): mızrak ucu dokunur; kurbağa patlayıp gerçek biçimine döner (IV.810–819) ═════════
function adn_patlama(x, y, R, seed) {
  if (R < 2) return;
  const q = rng(seed), pts = [], n = 22;
  for (let i = 0; i < n * 2; i++) { const a = i / (n * 2) * TAU + q() * .05, r = R * (i % 2 ? .45 + q() * .15 : .8 + q() * .4); pts.push([x + Math.cos(a) * r, y + Math.sin(a) * r * .8]); }
  const P = new Path2D(); poly(P, pts, true); GR.tx.fillStyle = GR.tone(.99); GR.tx.fill(P);
}
plan('P092', (ctx, st) => {
  const t = st.t, tM = Wd('H10', 'mızrağının'), tD = Wd('H10', 'dokunur'), tB = Wd('H10', 'biçimine');
  levha(ctx, { cx: 900, cy: 540, z: 1 }, () => {
    adn_cardak(t);
    const tip = [lerp(-260, 618, E.out3(adn_u(t, tM - .6, tD))) - 40 * E.io2(adn_u(t, tD + .6, tD + 2)), lerp(640, 748, E.out3(adn_u(t, tM - .6, tD)))];
    const ex = adn_u(t, tD, tD + .22), R = ex < 1 ? 520 * E.out3(ex) : lerp(520, 210, E.io2(adn_u(t, tD + .22, tB + .8)));
    const born = E.out3(adn_u(t, tD + .08, tB + .2)), h = lerp(8, 62, born);
    if (t > tD) {
      adn_patlama(660, 690, R, 3 + Math.floor((t - tD) * 6) % 3);
      if (t > tD + .22) PR.cloud({ x: 660, y: 620, w: 420 * clamp(R / 300), h: 260 * clamp(R / 300), seed: 7, lit: [.5, -.8], base: .9, hi: .99, core: .62, n: 3, drift: (t - tD) * 14, back: false });
      kiy_seytan(t, { x: 690, gy: 800, h, lum: .12, facing: -1, lit: [.6, -.8], lean: -.02, head: .25 * born, open: .25 + .5 * born, lift: .3 * born, armN: [.1, .2], armF: [-.25, .3] });
    } else adn_kurbaga(640, 760, 50, { f: -1, L: ADN_AY, nefes: Math.sin(t * 1.4) });
    // mızrak: soldan; kâğıt beyazı, mürekkep konturlu (koyu çardağın önünde)
    const a = Math.atan2(tip[0] + 260, -(tip[1] - 590)) * 0 + PI / 2 + Math.atan2(tip[1] - 590, tip[0] + 260);
    cen_mizrak(tip[0] - Math.cos(a - PI / 2) * 600, tip[1] - Math.sin(a - PI / 2) * 600, a, 1100, .52, 4.5, 60, 1);
  }, [.04, 0, 1]);
}, { tr: { type: 'cut' } });

// ═════════ gece bahçesi (H11, H12): solda koyu ağaç kütlesinin önünde beyaz bekçi melekler; sağda aya karşı koyu Şeytan ═════════
function adn_gece2(t, M, o = {}) {
  const L = M, HZ = o.hz ?? 780;
  adn_gece(M, { R: o.R ?? 900, rays: 8 });
  adn_tepe(HZ + 2, 22, 7, { v: .12 });
  adn_geceZemin(HZ, { v0: .14 });
  for (const [x, y, rx, ry, s] of (o.leke || [])) adn_leke(x, y, rx, ry, s);
}
function adn_bekci(t, list, L) {
  for (const p of list) cen_basmelek(Object.assign({ facing: 1, L, t, head: .12, twist: .3, armN: [-.05, .25], armF: [.3, .9], lift: .4, open: .55, wingS: 4.2 }, p));
}
function adn_h11(t) {
  const M = { x: 1330, y: 250, r: 58 }, tB = Wd('H11', 'beni'), tS = Wd('H11', 'şimdi');
  adn_gece2(t, M, { leke: [[1300, 900, 260, 36, 101], [880, 980, 180, 26, 102]] });
  adn_tac({ x: 280, y: 380, r: 360, seed: 103, L: M, n: 8, wx: 1.2, rim: 5, cuts: .8 });
  adn_tac({ x: -60, y: 640, r: 280, seed: 104, L: M, n: 6, rim: 5 });
  adn_cali({ x0: -300, x1: 760, y: 700, amp: 50, wl: 120, seed: 105, yb: 900, L: M, rim: 4, cuts: .6, endW: 160 });
  adn_bekci(t, [{ x: 180, y: 900 - 3.95 * 50, h: 50, seed: 3 }, { x: 360, y: 896 - 3.95 * 54, h: 54, seed: 4, armF: [.5, .6] }, { x: 540, y: 904 - 3.95 * 48, h: 48, seed: 5 }], M);
  // Şeytan: aya karşı; "beni" sorusunda başı kalkık, kolu açık; "şimdi"de başı iner
  const up = E.io2(adn_u(t, tB - .3, tB + .6)), dn = E.io2(adn_u(t, tS - .2, tS + 1.2));
  kiy_seytan(t, { x: 1300, gy: 920, h: 62, lum: .12, facing: -1, lit: [.15, -1], head: .2 * up - .35 * dn, lean: -.03 + .06 * dn, armN: [lerp(.15, -.5, up * (1 - dn)), .3], armF: [-.15, .2], open: .45 - .2 * dn, lift: .35 - .25 * dn });
  adn_cali({ x0: -300, x1: W + 300, y: 1060, amp: 24, wl: 100, seed: 106, yb: 1300, L: M, cuts: .4, tooth: 6, ends: false, rim: 3 });
}
plan('P093', (ctx, st) => levha(ctx, camLerp({ cx: 940, cy: 540 }, { cx: 990, cy: 540 }, st.p, E.sine), () => adn_h11(st.t), [.04, 0, 1]),
  { tr: { type: 'cut' }, over: (ctx, st) => quote(ctx, '“Şimdi günahına benziyorsun.”', 860, 130, st.t - Wd('H11', 'şimdi') + .3, { px: 68, panel: .55 }) });

// ═════════ P094 (H12): başı eğik; onların ışığı yanında kendi ışığının azlığı ═════════
function adn_h12(t) {
  const M = { x: 1380, y: 330, r: 64 }, tU = Wd('H12', 'utanç'), tS = Wd('H12', 'sönükleşen');
  adn_gece2(t, M, { hz: 800, leke: [[1500, 960, 280, 34, 111]] });
  adn_tac({ x: 160, y: 300, r: 380, seed: 112, L: M, n: 8, rim: 5, cuts: .8 });
  adn_cali({ x0: -300, x1: 760, y: 640, amp: 60, wl: 130, seed: 113, yb: 1000, L: M, rim: 4, cuts: .6, endW: 180 });
  adn_bekci(t, [{ x: 250, y: 1010 - 3.95 * 72, h: 72, seed: 6 }, { x: 520, y: 1020 - 3.95 * 66, h: 66, seed: 7, armF: [.45, .7] }], M);
  const bow = E.io2(adn_u(t, tU - .3, tU + 1.4)), dim = E.io2(adn_u(t, tS - .3, tS + 1.5));
  kiy_seytan(t, { x: 1340, gy: 1010, h: 100, lum: .1 * (1 - .8 * dim), facing: -1, lit: [.2, -1], head: .1 - .55 * bow, lean: .02 + .08 * bow, shTilt: -.04 + .05 * bow,
    armN: [.12, .15], armF: [-.08, .12], open: .35 - .22 * bow, lift: .3 - .25 * bow });
  adn_cali({ x0: -300, x1: W + 300, y: 1066, amp: 20, wl: 100, seed: 114, yb: 1300, L: M, cuts: .3, tooth: 6, ends: false, rim: 3 });
}
plan('P094', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540 }, { cx: 1000, cy: 540 }, st.p, E.sine), () => adn_h12(st.t), [.04, 0, 1]), { tr: ADN_FADE });

// ═════════ P095 (I01): bölüm kartı "YILANIN İÇİNDE" ═════════
function adn_i01(t) {
  const M = { x: 960, y: 150, r: 44 };
  adn_gece2(t, M, { hz: 820, R: 760, leke: [[960, 930, 300, 32, 121]] });
  adn_tac({ x: 120, y: 520, r: 320, seed: 122, L: M, n: 7, rim: 5 });
  adn_tac({ x: 1820, y: 540, r: 320, seed: 123, L: M, n: 7, rim: 5 });
  adn_cali({ x0: -300, x1: W + 300, y: 1040, amp: 34, wl: 110, seed: 124, yb: 1300, L: M, cuts: .4, tooth: 8, ends: false, rim: 3 });
}
plan('P095', (ctx, st) => levha(ctx, null, () => adn_i01(st.t), [.04, 0, 1]),
  { tr: { type: 'black', dur: 1.4, end: true }, over: (ctx, st) => chapterCard(ctx, 'YILANIN İÇİNDE', 'İntikam, tatlı mıdır?', st.lt, st.d) });

// ═════════ gece açıklığı (I04, I05): ay ışıklı otlar arasında uyuyan kıvrık yılan ═════════
const ADN_I4M = { x: 1290, y: 210, r: 56 };
function adn_i04Set(t) {
  const M = ADN_I4M;
  adn_gece2(t, M, { hz: 760, R: 950 });
  adn_tac({ x: 120, y: 420, r: 340, seed: 131, L: M, n: 8, rim: 5 });
  adn_tac({ x: 1900, y: 560, r: 240, seed: 132, L: M, n: 6, rim: 5 });
  adn_leke(1080, 920, 330, 62, 133, .95);
  adn_cali({ x0: 500, x1: 820, y: 900, amp: 36, wl: 40, seed: 134, yb: 1000, L: M, rim: 3, cuts: 0, tooth: 10, endW: 120, endD: 60 });
}
// uyuyan sarmal: baş en üstte, sola dönük
function adn_uyuyan(cx, cy, k) {
  const sp = adn_sarmal(cx, cy, 150 * k, 46 * k, 2.15, .36, .2, 130), e = sp[sp.length - 1];
  const hd = adn_spl([e, [e[0] - 30 * k, e[1] - 20 * k], [e[0] - 90 * k, e[1] - 26 * k], [e[0] - 140 * k, e[1] - 14 * k]], 30);
  return sp.concat(hd.slice(1));
}
const adn_uyW = k => u => k * lerp(6, 36, smooth(clamp(u / .45))) * (u > .9 ? lerp(1, .8, (u - .9) / .1) : 1);
function adn_uyuyanCiz(t, o = {}) {
  const C = adn_uyuyan(1080, 920, 1), br = Math.sin(t * .8) * 1.5;
  C.forEach(p => { p[1] += br * (p[0] - 900) / 600; });
  adn_yilan(C, adn_uyW(1), { L: ADN_I4M, t, seg: adn_sarmalSira(C, 130, [[130 / (C.length - 1), 1]]), goz: o.goz ?? 0, kesik: .6, rim: 4, basK: 1.35 });
  return C;
}
// ═════════ P097 (I04): otların arasında uyuyan kıvrık yılan; üstünde duraksayan koyu siluet; “Ne iğrenç bir alçalış!” ═════════
plan('P097', (ctx, st) => {
  const t = st.t, tI = Wd('I04', 'iğrenir');
  levha(ctx, camLerp({ cx: 990, cy: 540 }, { cx: 1030, cy: 540 }, st.p, E.sine), () => {
    adn_i04Set(t);
    adn_uyuyanCiz(t);
    const bob = Math.sin(t * .9) * 8, bow = E.io2(adn_u(t, tI - .4, tI + 1.2));
    kiy_seytan(t, { x: 1270, gy: 640 + bob, h: 52, lum: .1, facing: -1, lit: [0, -1], legs: true, head: -.1 - .4 * bow, lean: .15 + .1 * bow, open: .7 - .25 * bow, lift: .55 - .2 * bow,
      legN: [.25, -.6], legF: [.05, -.4], armN: [.3, .5], armF: [-.1, .4] });
    adn_cali({ x0: -300, x1: W + 300, y: 1050, amp: 34, wl: 60, seed: 135, yb: 1300, L: ADN_I4M, cuts: .3, tooth: 11, ends: false, rim: 3 });
  }, [.04, 0, 1]);
}, { tr: ADN_FADE, over: (ctx, st) => quote(ctx, '“Ne iğrenç bir alçalış!”', 560, 230, st.t - Wd('I04', 'iğrenç') + .3, { px: 70, panel: .55 }) });

// ═════════ P098 (I05): siluet duman olup yılanın ağzından içeri akar; “yükseldiği kadar alçalmak zorundadır” ═════════
function adn_dumanAkis(path, a, t, M) {
  if (a <= .01) return;
  const N = 16;
  for (let i = 0; i < N; i++) {
    const s = ((i / N) + t * .45) % 1, p = adn_yolNokta(path, s), r = lerp(30, 4, Math.pow(s, .8)) * a * (.8 + .3 * Math.sin(i * 1.9 + t));
    if (r < 1.5) continue;
    const P = new Path2D(), q = rng(i + 3), pts = []; for (let k = 0; k < 18; k++) { const an = k / 18 * TAU; pts.push([p[0] + Math.cos(an) * r * (1 + .15 * Math.sin(an * 3 + i)), p[1] + Math.sin(an) * r * (1 + .15 * Math.cos(an * 2 + i))]); }
    spline(P, pts, true, .6); adn_doldur(P, .02);
    if (r > 8) adn_kenar(P, M, p[0], p[1], Math.max(2.5, r * .16), 2);
  }
}
function adn_yolNokta(K, s) { const n = K.length - 1, u = s * n, i = Math.min(n - 1, Math.floor(u)), f = u - i; return [lerp(K[i][0], K[i + 1][0], f), lerp(K[i][1], K[i + 1][1], f)]; }
plan('P098', (ctx, st) => {
  const t = st.t, t0 = Wd('I05', 'sonra'), t1 = Wd('I05', 'girer') + .4, d = E.io2(adn_u(t, t0, t1)), a = clamp((t - t0) / .4) * (1 - E.io2(adn_u(t, t1 - .3, t1 + .8)));
  levha(ctx, { cx: 1030, cy: 540, z: 1 }, () => {
    const M = ADN_I4M;
    adn_i04Set(t);
    const C = adn_uyuyanCiz(t, { goz: E.io2(adn_u(t, t1, t1 + .8)) }), m = C[C.length - 1];
    const bob = Math.sin(t * .9) * 8, gy = 640 + bob, h = 52, top = gy - 8.6 * h, bot = gy + 30, yc = lerp(top - 140, bot, d);
    if (d < 1) {
      GR.save(); const Cl = new Path2D(); Cl.rect(-500, yc, W + 1000, 2000); GR.tx.clip(Cl); GR.px.clip(Cl);
      kiy_seytan(t, { x: 1270, gy, h, lum: .08, facing: -1, lit: [0, -1], head: -.5, lean: .25, open: .45 - .3 * d, lift: .35, legN: [.25, -.6], legF: [.05, -.4], armN: [.3, .5], armF: [-.1, .4] });
      GR.restore();
    }
    const path = adn_spl([[1270, Math.max(yc, top) + 30], [1210, lerp(yc, 760, .5)], [m[0] + 30, m[1] - 120], [m[0] - 30, m[1] - 50], [m[0] - 40, m[1]]], 40);
    adn_dumanAkis(path, a, t, M);
    adn_cali({ x0: -300, x1: W + 300, y: 1050, amp: 34, wl: 60, seed: 135, yb: 1300, L: M, cuts: .3, tooth: 11, ends: false, rim: 3 });
  }, [.04, 0, 1]);
}, { tr: { type: 'cut' }, over: (ctx, st) => {
  const t0 = Wd('I05', 'yükseldiği') - .5, e = Wd('I05', 'sonra');
  ctx.save(); ctx.globalAlpha *= clamp((e - st.t) / .6); quote(ctx, '“yükseldiği kadar alçalmak zorundadır”', 620, 220, st.t - t0, { px: 66, panel: .55, maxW: 900 }); ctx.restore();
} });

// ═════════ P100 (I07): alev geri gelir ═════════
function adn_i07(t, o) {
  const L = { x: 700, y: 280 }, HZ = 760;
  adn_gunduz(L, HZ, { r0: 380, tepeA: 22 });
  adn_tac({ x: 60, y: 470, r: 280, seed: 141, L, n: 7 });
  adn_cali({ x0: -300, x1: 760, y: 740, amp: 40, wl: 110, seed: 142, yb: 860, L, cuts: .6, endW: 140 });
  const C = adn_i06Ylan(1230, 1060, 1.5, o.yum), n = C.length - 1, ur = ADN_I06_N1 / n;
  adn_yilan(C, adn_ylnW(1.5), { L, t, seg: [[0, ur], [ur, 1]], basK: 1.45, alev: { k: o.alev, u: ur + .14, seed: 13 }, goz: 1, kesik: .7 });
  adn_cali({ x0: -300, x1: W + 300, y: 1060, amp: 24, wl: 110, seed: 143, yb: 1300, L, cuts: .5, tooth: 7, ends: false });
}
plan('P100', (ctx, st) => {
  const t = st.t, tY = Wd('I07', 'yanan'), tC = Wd('I07', 'cehennem'), tB = Wd('I07', 'bitirir');
  const k = kf(t, [[S('I07'), 0], [tY - .3, 0], [tY + .2, .25, E.out2], [tC + .6, 1.25, E.io2], [tB, 1.15], [tB + 1.5, 1.3]]) * (1 + .05 * Math.sin(t * 2.3));
  const yum = 1 - E.io2(adn_u(t, tC, tB + .4));
  levha(ctx, camLerp({ cx: 1000, cy: 540 }, { cx: 960, cy: 540 }, st.p, E.sine), () => adn_i07(t, { alev: k, yum }), [.8, 0, 1]);
}, { tr: { type: 'cut' } });

// ═════════ P101 (I08): dala uzanan el ve meyve; meyve kopar; sonra ikinci el ═════════
// El: yalnız yen (geniş kol ağzı) ve el silueti; yüz ve beden yok. Meyve yuvarlak (ayrıntısız).
function adn_el(x, y, s, ang, o = {}) {
  const c = Math.cos(ang), sn = Math.sin(ang), T = ([a, b]) => [x + (a * c - b * sn) * s, y + (a * sn + b * c) * s], k = clamp(o.kavra || 0), fl = o.flip ? -1 : 1;
  const F = (a, b) => T([a, b * fl]);
  const yen = new Path2D(); spline(yen, [[-.08, -.4], [-.6, -.5], [-3.2, -.7], [-3.2, .75], [-.6, .55], [-.08, .42]].map(([a, b]) => F(a, b)), true, .4);
  const tip = [[1.22, -.2], [1.28, -.06], [1.2, .06]].map(([a, b], i) => [lerp(a, .92 - i * .06, k), lerp(b, .12 + i * .1, k)]);
  const el = new Path2D(); spline(el, [[0, -.3], [.55, -.33], [lerp(1.05, .82, k), lerp(-.3, -.22, k)], ...tip, [lerp(.85, .7, k), lerp(.14, .28, k)], [.62, .2], [.78, .44 - .1 * k], [.86, .52 - .12 * k], [.76, .58 - .1 * k], [.42, .42], [0, .3]].map(([a, b]) => F(a, b)), true, .4);
  adn_doldur(el, .02); adn_doldur(yen, .02);
  const tx = GR.tx; tx.save(); tx.clip(yen); adn_cizgi([F(-.2, -.36), F(-.16, 0), F(-.2, .4)], Math.max(4, s * .06), .95, .4); adn_sivri([F(-.9, -.55), F(-2.2, -.45)], Math.max(4, s * .07), .95); tx.restore();
  tx.save(); tx.clip(el); adn_sivri([F(.15, -.27), F(.9, -.24)], Math.max(3, s * .05), .95); tx.restore();
  return T;
}
function adn_meyve(x, y, r, L) {
  const P = new Path2D(); P.arc(x, y, r, 0, TAU); adn_doldur(P, .02);
  const [lx, ly] = adn_nrm(L.x - x, L.y - y), tx = GR.tx;
  tx.save(); tx.clip(P); tx.fillStyle = GR.tone(.97); tx.beginPath(); tx.arc(x, y, r - 4, 0, TAU); tx.fill(); tx.fillStyle = GR.tone(.02); tx.beginPath(); tx.arc(x - lx * r * .3, y - ly * r * .3, r * 1.02, 0, TAU); tx.fill(); tx.restore();
}
function adn_i08(t) {
  const L = { x: 1300, y: 230 }, t0 = S('I08'), tH = Wd('I08', 'havvayı'), tK = Wd('I08', 'koparır'), tA = Wd('I08', 'adem');
  cen_gok(L, { r0: 420, r1: 1600, v: .72, n: 100 });
  // dal: sağ üstten; yaprak öbekleri; meyve koptuğunda dal yaylanır
  const sp = t > tK ? Math.sin((t - tK) * 9) * Math.exp(-(t - tK) * 2.5) * .06 : 0;
  GR.frame(1960, 120, sp, 1, 1);
  { const P = new Path2D(); spline(P, [[60, -40], [-300, 90], [-700, 250], [-880, 330], [-700, 270], [-300, 125], [60, 0]], true, .4); adn_doldur(P, .02); }
  adn_tac({ x: -180, y: 60, r: 170, seed: 151, L: { x: L.x - 1960, y: L.y - 120 }, n: 6 });
  adn_tac({ x: -640, y: 220, r: 120, seed: 152, L: { x: L.x - 1960, y: L.y - 120 }, n: 5 });
  adn_sivri([[-860, 322], [-890, 360]], 7);
  GR.unframe();
  // yılan dalın üstünde: başı meyvenin yanında, aşağıya (Havva'ya) dönük
  const yl = adn_spl([[1600, 210], [1450, 250], [1300, 320], [1200, 360], [1150, 400], [1120, 450]], 80);
  yl.forEach(p => { p[1] += Math.sin(t * 1.2 + p[0] * .01) * 2 * (1 - (p[0] - 1120) / 480); });
  adn_yilan(yl, u => lerp(4, 17, smooth(clamp(u / .4))) * (u > .9 ? .85 : 1), { L, t, goz: 1, kesik: .5, basK: 1.4 });
  // meyve: dalın ucunda; koparılınca elle birlikte iner
  const reach = E.io3(adn_u(t, tH - .6, tK)), pull = E.io2(adn_u(t, tK, tK + 1.1));
  const hx = lerp(240, 1040, reach) - 300 * pull, hy = lerp(1180, 548, reach) + 260 * pull, mx = 1080, my = 505;
  const T = adn_el(hx, hy, 92, -.95 + .35 * pull, { kavra: E.io2(adn_u(t, tK - .25, tK + .1)) });
  const fx = t < tK ? mx + Math.sin(t * .9) * 3 : lerp(mx, T([.8, .05])[0], 1), fy = t < tK ? my : T([.8, .05])[1] - 34 * (1 - E.out2(adn_u(t, tK, tK + .3))) * 0;
  if (t < tK) adn_sivri([[mx + 4, my - 40], [mx + 2, my - 30], [mx, my - 26]], 5);
  adn_meyve(t < tK ? mx + Math.sin(t * .9) * 3 : fx, t < tK ? my : fy, 36, L);
  if (t > tK) adn_el(hx, hy, 92, -.95 + .35 * pull, { kavra: 1 });   // parmaklar meyvenin önünde
  // ikinci el: sağ alttan, meyveye uzanır
  const r2 = E.io3(adn_u(t, tA - 1, tA + .6));
  if (r2 > 0) adn_el(lerp(1950, 1090, r2), lerp(1200, 860, r2), 96, PI + .55, { kavra: 0, flip: true });
}
plan('P101', (ctx, st) => levha(ctx, null, () => adn_i08(st.t), [.8, 0, 1]), { tr: ADN_FADE });

// ═════════ P102 (I09): gök kararır, yapraklar dökülür; yılan çalılığa süzülür ═════════
function adn_i09(t) {
  const { tx, px, tone } = GR, tD = Wd('I09', 'dünya'), tV = Wd('I09', 'verir'), tS = Wd('I09', 'suçlu'), tZ = Wd('I09', 'süzülür');
  const dk = E.io2(adn_u(t, tD - .3, tV + .5)), HZ = 760, L = { x: 1000, y: 330 };
  // gök: açıktan koyuya (yatay tarama; ışınsal tarama koyu tonda kâğıt gibi kalırdı)
  const g = tx.createRadialGradient(L.x, L.y, 60, L.x, L.y, 1400);
  g.addColorStop(0, tone(lerp(1, .5, dk))); g.addColorStop(.25, tone(lerp(.93, .3, dk))); g.addColorStop(.6, tone(lerp(.85, .12, dk))); g.addColorStop(1, tone(lerp(.78, .05, dk)));
  tx.fillStyle = g; tx.fillRect(-1600, -1600, W + 3200, HZ + 1600); px.fillStyle = GR.hatch({ th: 0, id: 1 }); px.fillRect(-1600, -1600, W + 3200, HZ + 1600);
  // kararan bulut kütleleri üstten iner
  PR.cloud({ x: 500, y: lerp(-260, 120, dk), w: 1100, h: 260, seed: 12, lit: [.6, .8], base: .03, hi: .7, core: .02, n: 4, drift: t * 6 });
  PR.cloud({ x: 1550, y: lerp(-300, 90, dk), w: 1000, h: 240, seed: 19, lit: [-.6, .8], base: .03, hi: .7, core: .02, n: 4, drift: -t * 5 });
  adn_tepe(HZ + 2, 22, 7, { v: lerp(.62, .14, dk) });
  { const P = new Path2D(); P.rect(-1600, HZ, W + 3200, 900); const gg = tx.createLinearGradient(0, HZ, 0, H); gg.addColorStop(0, tone(lerp(.88, .2, dk))); gg.addColorStop(1, tone(lerp(.97, .1, dk))); GR.fill(P, gg, { th: 0, id: 1 }); }
  // sol: ağaç (yaprak döker)
  adn_govde(300, 820, 420, 40, 20, { dallar: [[.8, .7, 120, 14], [.85, -.6, 110, 12]] });
  adn_tac({ x: 290, y: 330, r: 260, seed: 161, L, n: 7, cuts: 1 - dk, lobes: 1 - dk });
  // yılan: S dalgasıyla sağdaki çalılığa süzülür
  const m = E.io2(adn_u(t, tS - .4, tZ + 1.2)), C = [];
  for (let i = 0; i <= 90; i++) { const u = i / 90, x = lerp(560, 1060, u) + m * 760, y = 905 + Math.sin(u * 9 - t * 2.4) * 24 * (.4 + .6 * u) * (1 - u * .3); C.push([x, y]); }
  adn_yilan(C, u => lerp(5, 24, smooth(clamp(u / .4))) * (u > .92 ? .85 : 1), { L, t, goz: 1, kesik: .6, basK: 1.4 });
  adn_cali({ x0: 1500, x1: 2300, y: 820, amp: 70, wl: 90, seed: 162, yb: 1100, L, cuts: .5 * (1 - dk), tooth: 10, endW: 200 });
  // düşen yapraklar: tepeden doğar (kadraj dışı), sallanarak iner
  const q = rng(163);
  for (let i = 0; i < 26; i++) {
    const ts = tD - 1 + q() * 7, x0 = 100 + q() * 1500, sp = 70 + q() * 60, life = t - ts; if (life < 0) { q(); continue; }
    const x = x0 + Math.sin(life * 1.6 + i) * 30 + life * 20, y = 140 + life * sp, a = Math.sin(life * 2 + i) * 1.2, sz = 9 + q() * 6;
    if (y > 1100) continue;
    const P = new Path2D(); P.ellipse(x, y, sz, sz * .38, a, 0, TAU); adn_doldur(P, .02);
  }
  adn_cali({ x0: -300, x1: W + 300, y: 1050, amp: 26, wl: 110, seed: 164, yb: 1300, L, cuts: .3, tooth: 7, ends: false });
}
plan('P102', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540 }, { cx: 1020, cy: 540 }, st.p, E.sine), () => adn_i09(st.t), [.8, 0, 1]), { tr: { type: 'cut' } });

// ═════════ P103 (I10): siyah; yalnız yılanın gözü; "Kazanmıştır." ═════════
plan('P103', (ctx, st) => {
  ctx.save(); baseT(ctx); ctx.fillStyle = INK_CSS; ctx.fillRect(0, 0, W, H);
  const a = E.out3(clamp(st.lt / .8)) * (1 - .85 * Math.sin(PI * clamp((st.t - Wd('I10', 'kazanmıştır') - .9) / .35)));
  if (a > .02) { ctx.fillStyle = PAPER_CSS; ctx.beginPath(); ctx.ellipse(960, 450, 74, 10 * a, -.05, 0, TAU); ctx.fill(); }
  ctx.restore();
}, { tr: { type: 'fade', dur: .6 }, over: (ctx, st) => txt(ctx, 'Kazanmıştır.', 960, 640, { font: FONT.alinti(84), a: E.sine(clamp((st.t - Wd('I10', 'kazanmıştır') + .1) / .6)) }) });

// ═════════ P116 (K02): önceki an: iki figür diz çökmüş, başları eğik (uzak, arkadan); köşede dik duran koyu Şeytan ═════════
function adn_k02(t) {
  const L = { x: 720, y: 330 }, HZ = 700;
  adn_gunduz(L, HZ, { r0: 360, tepeA: 26 });
  adn_govde(760, 760, 470, 36, 20, { dallar: [[.85, .7, 110, 12]] });
  adn_tac({ x: 760, y: 450, r: 210, seed: 171, L, n: 7 });
  adn_tac({ x: 470, y: 560, r: 150, seed: 172, L, n: 6 });
  adn_cali({ x0: 300, x1: 1100, y: 690, amp: 44, wl: 100, seed: 173, yb: 820, L, cuts: .6, endW: 150 });
  const br = Math.sin(t * .6) * .03;
  adn_insan(712, 806, 12, { diz: 1, egik: .85 + br, seed: 11 });
  adn_insan(778, 806, 11.4, { diz: 1, egik: .9 + br, sac: true, seed: 12 });
  adn_cali({ x0: 200, x1: 1200, y: 812, amp: 12, wl: 60, seed: 174, yb: 860, L, cuts: .2, tooth: 5, endW: 160, endD: 40 });
  // sağ köşe: yükselti üstünde dik duran koyu Şeytan (açık göğe karşı)
  adn_cali({ x0: 1380, x1: 2300, y: 930, amp: 40, wl: 150, seed: 175, yb: 1300, L, cuts: .5, tooth: 7, endW: 260, endD: 200 });
  kiy_seytan(t, { x: 1690, gy: 930, h: 66, lum: 0, facing: -1, lit: [-.9, -.4], head: .05, lean: -.02, open: .3, lift: .35, armN: [.1, .15], armF: [-.1, .1] });
  adn_cali({ x0: -300, x1: 1500, y: 1060, amp: 22, wl: 100, seed: 176, yb: 1300, L, cuts: .4, tooth: 6, endW: 200, endD: 80 });
}
plan('P116', (ctx, st) => levha(ctx, camLerp({ cx: 980, cy: 540 }, { cx: 950, cy: 540 }, st.p, E.sine), () => adn_k02(st.t), [.8, 0, 1]), { tr: ADN_FADE });
