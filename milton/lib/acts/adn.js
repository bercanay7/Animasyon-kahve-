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
  const { tx } = GR, d = clamp(o.diz || 0), eg = clamp(o.egik || 0), st = o.adim ?? 0, bob = -.07 * Math.abs(Math.sin(st)), dy = 2.7 * d - bob;
  const W2 = (lx, ly) => [x + lx * h, y + ly * h];
  const sw = .1 * Math.sin(st);
  // gövde ve örtü (sağ yarı → sol yarı)
  const R = [[.2, -6.42], [.78, -6.12 + .16 * eg], [.95, -5.5], [.98, -4.4], [.92, -3.5], [1.08 + .2 * d, -2.0], [1.22 + sw + .35 * d, -.35], [1.2 + sw + .4 * d, 0]];
  const Lf = [[-1.2 + sw - .4 * d, 0], [-1.22 + sw - .35 * d, -.35], [-1.08 - .2 * d, -2.0], [-.92, -3.5], [-.98, -4.4], [-.95, -5.5], [-.78, -6.12 + .16 * eg], [-.2, -6.42]];
  const sk = (p, i, arr) => { const top = p[1] < -2.4; return [p[0], top ? p[1] + dy : p[1] * (1 - .6 * d) + (p[1] < -1 ? dy * .2 : 0)]; };
  const body = [...R.map(sk), [0, .04], ...Lf.map(sk)].map(([a, b]) => W2(a, b));
  const P = new Path2D(); spline(P, body, true, .5);
  // baş: eğikken omuz çizgisinin arkasına iner
  const hc = W2(0, -6.95 + dy + .62 * eg), Hd = new Path2D(); Hd.ellipse(hc[0], hc[1], .43 * h, (.5 - .08 * eg) * h, 0, 0, TAU); P.addPath(Hd);
  if (o.sac) { const S = new Path2D(); spline(S, [[-.42, -7.1], [.42, -7.1], [.6, -6.3], [.66, -4.9], [.4, -4.5], [-.4, -4.5], [-.66, -4.9], [-.6, -6.3]].map(([a, b]) => W2(a, b + dy + .5 * eg * (b < -6 ? 1 : .3))), true, .6); P.addPath(S); }
  // tutulan el: omuzdan ele uzanan geniş yenli kol
  if (o.el) {
    const sd = o.kol || 1, sh = W2(.78 * sd, -5.95 + dy), e = o.el, mx = (sh[0] + e[0]) / 2 + sd * .25 * h, my = (sh[1] + e[1]) / 2 + .2 * h;
    const pts = [sh, [mx, my], e], A = [], Bq = [];
    for (let i = 0; i < 3; i++) { const p0 = pts[Math.max(0, i - 1)], p1 = pts[Math.min(2, i + 1)], [nx, ny] = adn_nrm(p1[1] - p0[1], -(p1[0] - p0[0])), w = [.36, .3, .17][i] * h; A.push([pts[i][0] + nx * w, pts[i][1] + ny * w]); Bq.push([pts[i][0] - nx * w, pts[i][1] - ny * w]); }
    const K = new Path2D(); spline(K, [...A, ...Bq.reverse()], true, .5); P.addPath(K);
    const Hn = new Path2D(); Hn.ellipse(e[0], e[1], .2 * h, .17 * h, 0, 0, TAU); P.addPath(Hn);
  }
  const v = o.v ?? .985;
  adn_doldur(P, v, PI / 2, 10);
  // açık figürde birkaç kıvrım (alttan giren sivri mürekkep vuruşu); koyu figürde yok
  if (v > .5 && h >= 9) {
    const q = rng(o.seed || 4); tx.save(); tx.clip(P);
    for (let i = 0; i < (o.kat ?? 2); i++) { const fx = (i ? .45 : -.3) + (q() - .5) * .2, L0 = (1.6 + q() * 1.4) * h * (1 - .5 * d), p0 = W2(fx + sw * .6, .1), pts = [];
      for (let m = 0; m <= 6; m++) pts.push([p0[0] + (q() - .5) * 1.2, p0[1] - L0 * m / 6]);
      adn_sivri(pts, Math.max(3, h * .12), .03); }
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
    PR.flameBank(bx[0] - s * .1, bx[0] + s * .1, bx[1] + s * .1, s * .52 * k, t, o.alev.seed || 7, { band: false, n: 3, wr: .42, curl: .4, speed: .5, solidBelow: 1e5, frags: false, smoke: false, strip: .12, env: f2 => .55 + .45 * Math.sin(f2 * PI) });
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
  // iç alev: daraltılmış gövde penceresinde (siyah iç), alttan yukarı küçük kâğıt beyazı diller
  if (o.alev && o.alev.k > .02) {
    const A = o.alev, win = adn_ylnTup(C, w, A.u0, A.u1, A.dar ?? .6), i0 = Math.round(A.u0 * n), i1 = Math.round(A.u1 * n);
    let yb = -1e9, xb = 0, yt = 1e9; for (let i = i0; i <= i1; i++) { if (C[i][1] > yb) { yb = C[i][1]; xb = C[i][0]; } yt = Math.min(yt, C[i][1]); }
    const ww = w((A.u0 + A.u1) / 2) * (A.dar ?? .6), hg = (yb - yt + ww * 1.4) * A.k;
    GR.save(); tx.clip(win); px.clip(win);
    adn_alevler(xb, yb + ww * .5, ww * 1.7, hg, o.t || 0, A.seed || 11, A.n ?? 3);
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
    adn_dil(x + (f - .5) * w * .62, y, h * big, w / n * 1.5, (f - .5) * .3, t, seed * 7 + i); }
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
    adn_sivri([T([w * .05, h * .02]), T([sw * h * .1, -h * .25]), T([sw * h * .3 - w * .05, -h * .5])].reverse(), Math.max(3, w * .14), .03);
    if (h > 60) adn_sivri([T([-w * .3, h * .02]), T([-w * .34 + sw * h * .05, -h * .22])].reverse(), Math.max(3, w * .1), .03);
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
  adn_zemin(hz, o.zemin || {});
}

// ═════════ P099 (I06): sabah; uzakta Havva (arkadan), önde dik duran yılan; içindeki alev bir an söner ═════════
// Yılanın merkez çizgisi: yerde 1,4 turluk sarmal, ortasından yükselen gövde, Havva'ya dönük baş. yum: 0 dik … 1 yumuşamış (baş iner, boyun gevşer)
function adn_i06Ylan(cx, cy, k, yum) {
  const sp = adn_sarmal(cx, cy, 170 * k, 78 * k, 1.42, .3, .25, 110), e = sp[sp.length - 1], hy = 44 * yum * k, hx = -26 * yum * k;
  const rise = adn_spl([e, [e[0] + 18 * k, e[1] - 70 * k], [e[0] + 42 * k, e[1] - 175 * k], [e[0] + 44 * k, e[1] - 280 * k], [e[0] + 14 * k + hx * .3, e[1] - 375 * k + hy * .4], [e[0] - 38 * k + hx * .7, e[1] - 440 * k + hy * .8], [e[0] - 100 * k + hx, e[1] - 470 * k + hy], [e[0] - 140 * k + hx, e[1] - 468 * k + hy * 1.1 + 10 * k * yum]], 90);
  return sp.concat(rise.slice(1));
}
const adn_ylnW = (k) => u => k * (lerp(5, 44, smooth(clamp(u / .32))) * (u > .86 ? lerp(1, .74, (u - .86) / .14) : 1) + 7 * Math.exp(-Math.pow((u - .7) / .07, 2)));
function adn_i06(t, o = {}) {
  const L = { x: 1190, y: 250 }, HZ = 700;
  adn_gunduz(L, HZ, { r0: 400, tepeA: 26 });
  // sol: Havva'nın arkasındaki koyu ağaç ve çit kütlesi
  adn_govde(260, 700, 420, 46, 22, { dallar: [[.7, -.7, 120, 16], [.85, .6, 110, 12]] });
  adn_tac({ x: 250, y: 330, r: 250, seed: 4, L, n: 8, wx: 1.25, sq: .7 });
  adn_tac({ x: -120, y: 470, r: 230, seed: 6, L, n: 6 });
  adn_cali({ x0: -100, x1: 900, y: 640, amp: 46, wl: 150, seed: 2, yb: 820, L, cuts: .8, tooth: 9 });
  // uzak sağ: ufukta küçük ağaç öbeği (sağ kenarın çapası)
  adn_tac({ x: 1880, y: 560, r: 150, seed: 9, L, n: 5, cuts: .6 });
  adn_cali({ x0: 1600, x1: 2100, y: 690, amp: 24, wl: 90, seed: 8, yb: 760, L, cuts: .5, tooth: 6 });
  // Havva: uzak, örtülü, arkadan; koyu çitin önünde
  adn_insan(470, 772, 13, { sac: true, seed: 5, kat: 2 });
  // çiçekli ön bant (eteğini örter)
  const cb = adn_cali({ x0: -100, x1: 980, y: 792, amp: 18, wl: 70, seed: 12, yb: 900, L, cuts: .4, tooth: 6 });
  adn_cicek(cb.top, { seed: 21, d: .06, r: 8, depth: 26 });
  // yılan
  const C = adn_i06Ylan(1390, 930, 1, o.yum || 0);
  adn_yilan(C, adn_ylnW(1), { L, t, seg: [[0, .3], [.3, .55], [.55, 1]], alev: { k: o.alev ?? 1, u0: .6, u1: .84, dar: .52, seed: 13 }, goz: o.goz ?? 1, kesik: .8 });
  // ön plan: alçak koyu ot bandı (karenin alt çapası)
  adn_cali({ x0: -100, x1: 2100, y: 1050, amp: 26, wl: 120, seed: 14, yb: 1300, L, cuts: .5, tooth: 7 });
}
function adn_i06Alev(t) {
  const k = kf(t, [[S('I06'), 1], [Wd('I06', 'nefreti'), 1], [Wd('I06', 'hilesi'), .8], [Wd('I06', 'kıskançlığı'), .64], [Wd('I06', 'intikamı'), .48], [Wd('I06', 'düşer'), .3],
    [Wd('I06', 'sersem'), .22], [Wd('I06', 'iyilik'), 0, E.io2]]);
  return k * (1 + .05 * Math.sin(t * 2.1));
}
plan('P099', (ctx, st) => {
  const t = st.t, yum = E.io2(adn_u(t, Wd('I06', 'kopup'), Wd('I06', 'durur') + .8)) * .7 + .3 * E.io2(adn_u(t, Wd('I06', 'sersem'), Wd('I06', 'donakalır')));
  const cam = camLerp({ cx: 900, cy: 540, z: 1 }, { cx: 1010, cy: 540, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => adn_i06(t, { alev: adn_i06Alev(t), yum, goz: 1 - .45 * yum }), [.8, 0, 1]);
}, { tr: ADN_FADE, over: (ctx, st) => {
  const t0 = Wd('I06', 'iyilik') - .25;
  adn_alintiA(ctx, 'sersem bir iyilik', 600, 250, st.t - t0, { px: 78 });
} });

// ═════════ P115 (K01): Aden'den çıkış: kapı ve dönen alev; önde geniş ova, gün doğumu; el ele yürüyen iki küçük figür (arkadan) ═════════
// Filmin en ferah karesi: gök ve ova temiz kâğıda yakın; koyu kütle yalnız sol üstte kapı (çerçeve) ve altta ince zemin bandı.
function adn_alevCark(cx, cy, rx, ry, t, o = {}) {
  // kapının üstünde dönen alev şeridi (figürsüz): elips boyunca dışa dönük diller; diller elips üzerinde yavaşça akar
  const n = o.n ?? 16, sp = o.sp ?? .05;
  for (let i = 0; i < n; i++) {
    const a = (i / n + t * sp) * TAU, x = cx + Math.cos(a) * rx, y = cy + Math.sin(a) * ry, back = Math.sin(a) < 0;
    const [nx, ny] = adn_nrm(Math.cos(a) / rx, Math.sin(a) / ry), ang = Math.atan2(ny, nx) + PI / 2;
    const hh = (o.h ?? 70) * (back ? .7 : 1) * (.8 + .3 * Math.sin(i * 2.3 + t * .7));
    GR.frame(x, y, ang * .55, 1, 1);
    PR.flame(0, 0, hh, hh * .42, t + i * 1.7, 300 + i, { speed: .55, curl: .35, solidBelow: 1e5 });
    GR.unframe();
  }
}
function adn_k01(t, o = {}) {
  const { tx, tone } = GR, L = { x: 1260, y: 655 }, HZ = 662;
  cen_gok(L, { r0: 560, r1: 1750, v: .74, n: 104 });
  // güneş: ufukta yarısı batık büyük temiz kâğıt disk (gökle birleşir; çevresi zaten temiz)
  // ufuk: ince koyu tepe şeridi; güneşin altını keser
  { const q = rng(31), P = new Path2D(); P.moveTo(-1600, HZ + 30); for (let x = -1600; x <= W + 1600; x += 12) P.lineTo(x, HZ - 6 - 10 * Math.abs(Math.sin(x / 260 + 1.3)) - 6 * Math.abs(Math.sin(x / 97)) - 22 * Math.exp(-Math.pow((x - 600) / 160, 2)) - 14 * Math.exp(-Math.pow((x - 1700) / 120, 2)));
    P.lineTo(W + 1600, HZ + 30); P.closePath(); adn_doldur(P, .03); }
  // ova: ufuktan öne açılan çayır, perspektif tarama; güneşin yansıdığı uzun açık yol
  adn_zemin(HZ + 8, { v0: .78, v1: .9, v2: .96 });
  { const P = new Path2D(); P.moveTo(L.x - 20, HZ + 10); P.lineTo(L.x + 20, HZ + 10); P.quadraticCurveTo(1150, 900, 980, H + 40); P.lineTo(620, H + 40); P.quadraticCurveTo(1000, 860, L.x - 20, HZ + 10); P.closePath();
    tx.save(); tx.globalCompositeOperation = 'lighten'; tx.fillStyle = tone(.985); tx.fill(P); tx.restore(); }
  // uzakta seyrek ağaçlar (ufukta küçük koyu taçlar)
  for (const [x, r, s] of [[420, 34, 51], [470, 22, 52], [1660, 30, 53], [1790, 44, 54]]) { adn_govde(x, HZ + 2, HZ - r * .8, 6, 4); adn_tac({ x, y: HZ - r * 1.3, r, seed: s, L, n: 4, tooth: 4, cuts: 0, lobes: 0 }); }
  // figürler: el ele, arkadan, ışığa doğru yürür; uzun gölgeleri öne düşer
  const w = o.yur ?? 0, ph = o.adim ?? 0, x1 = lerp(985, 1040, w), y1 = lerp(892, 846, w), h1 = lerp(12.5, 10.8, w), gap = 2.5 * h1;
  const xa = x1 - gap / 2, xb = x1 + gap / 2;
  for (const [x, hh] of [[xa, h1], [xb - .3 * h1, h1 * .95]]) {
    const P = new Path2D(), dx = (x - L.x), dy = (y1 - L.y), l = Math.hypot(dx, dy), ux = dx / l, uy = dy / l * .55, len = 26 * hh;
    poly(P, [[x - hh * .9, y1], [x + hh * .9, y1], [x + ux * len + hh * 1.4, y1 + uy * len * 1.6], [x + ux * len - hh * 1.2, y1 + uy * len * 1.6]], true);
    adn_doldur(P, .03);
  }
  const hm = [x1 - .1 * h1, y1 - 3.7 * h1];
  adn_insan(xa, y1, h1, { v: .02, el: hm, kol: 1, adim: ph, egik: o.egik || 0 });
  adn_insan(xb - .3 * h1, y1, h1 * .95, { v: .02, el: hm, kol: -1, adim: ph + PI, sac: true, egik: (o.egik || 0) * 1.1 });
  // sol üst: kapının kemeri ve sövesi (koyu çerçeve); kemerin önünde dönen alev şeridi
  const G = new Path2D(); G.moveTo(-200, -200); G.lineTo(1020, -200);
  { const pts = []; for (let i = 0; i <= 30; i++) { const u = i / 30, a = -PI / 2 + u * PI / 2; pts.push([300 + Math.cos(a + PI) * -1 * 0 + 300 + Math.cos(a) * 420 * -1 + 420 * 0, 0]); } }
  G.lineTo(1020, -60); G.bezierCurveTo(760, 20, 470, 120, 330, 330); G.lineTo(300, 420); G.lineTo(300, H + 200); G.lineTo(-200, H + 200); G.closePath();
  adn_doldur(G, .02);
  { // taş blok derzleri: sövede ve kemerde ışığa bakan kenardan içe seyrek beyaz vuruşlar; kemer alnında ince kenar ışığı
    tx.save(); tx.clip(G);
    adn_cizgi([[1010, -52], [760, 28], [520, 150], [338, 336], [306, 430], [306, 1080]], 7, .95, .25);
    const q = rng(77); for (let y = 470 + q() * 40; y < 1060; y += 90 + q() * 70) adn_sivri([[300, y], [270 - q() * 60, y + 3]], 6, .96);
    for (let i = 0; i < 6; i++) { const u = .12 + i * .15 + q() * .05, x = lerp(1010, 338, u), y = lerp(-52, 336, u * u * .9 + u * .1); adn_sivri([[x - 6, y - 4], [x - 30 - q() * 40, y - 40 - q() * 40]], 6, .96); }
    tx.restore();
  }
  adn_alevCark(470, 150, 300, 58, t, { n: 18, h: 62, sp: .035 });
  // ön zemin: sol altta sövenin dibinden uzanan alçak koyu ot bandı; sağ altta ince bant
  adn_cali({ x0: -200, x1: 760, y: 1040, amp: 34, wl: 110, seed: 61, yb: 1300, L, cuts: .5, tooth: 7 });
  adn_cali({ x0: 1500, x1: 2200, y: 1066, amp: 22, wl: 90, seed: 62, yb: 1300, L, cuts: .4, tooth: 6 });
}
plan('P115', (ctx, st) => {
  const t = st.t, t0 = S('K01'), tg = Wd('K01', 'gözyaşı'), ts = Wd('K01', 'sildiler');
  // yürüyüş: sürekli, gözyaşında yavaşlar (adım evresi hız integrali), başlar eğilir, "sildiler"de kalkar
  const slow = u => 1 - .75 * E.sine(adn_u(u, tg - 1.2, tg - .2)) * (1 - E.sine(adn_u(u, ts, ts + 1)));
  let ph = 0; for (let u = t0 - 1.4; u < t; u += .1) ph += .1 * 2.6 * slow(u);
  const eg = .55 * E.io2(adn_u(t, tg - 1, tg + .2)) * (1 - E.io2(adn_u(t, ts - .2, ts + .8)));
  const cam = camLerp({ cx: 930, cy: 540, z: 1 }, { cx: 1000, cy: 540, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => adn_k01(t, { yur: adn_u(t, t0 - 1.4, st.end), adim: ph, egik: eg }), [.8, 0, 1]);
}, { tr: { type: 'black', dur: 1.4, end: true }, over: (ctx, st) => {
  adn_alintiA(ctx, '“Bütün dünya önlerindeydi.”', 1290, 330, st.t - Wd('K01', 'bütün') + .15, { px: 72 });
} });
