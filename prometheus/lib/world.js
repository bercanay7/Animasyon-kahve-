// Prometheus dünyası: kırmızı figür gece zemini, dünyanın ucundaki kayalık, ateş/rezene sapı, zincir kazıkları, uzaktaki insan ateşleri.
// Üslup mantığı: Hesiodos ve tanrıların soyu siyah figür (arkaik), Aiskhylos kırmızı figür (V. yüzyıl Atina), Erhat beyaz zemin (modern okuma).
'use strict';
const PC = {
  glaze: '#0E0907', glazeL: '#1C120D', clayR: '#C9703F', clayRL: '#E08A52', rock: '#B9653A', rockD: '#8E4826',
  fire: '#FFD27A', fireCore: '#FFF6D6', fireDeep: '#E8762B', ember: 'rgba(255,170,80,.55)',
};
// Siyah sır zemin: hafif sıcak dalgalanma + seyrek yıldızlar
function glazeBG(ctx, t, o = {}) {
  ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
  const g = ctx.createRadialGradient(o.gx ?? W * .55, o.gy ?? H * .9, 0, o.gx ?? W * .55, o.gy ?? H * .9, o.gr ?? 1300);
  g.addColorStop(0, o.warm || 'rgba(120,48,22,.55)'); g.addColorStop(.5, 'rgba(60,24,12,.25)'); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (o.stars !== false) stars(ctx, t, o.nStars ?? 120, o.seed ?? 11, 'rgba(240,215,170,.8)', [0, 0, W, H * .62]);
}
// Kırmızı figür kayalık: ayrılmış kil rengi kütle, siyah kontur, katman çizgileri ve kenar taraması.
// pts: dış hat (dünya koordinatı), o: {fill, line, seed, strata}
function crag(ctx, pts, o = {}) {
  const fill = o.fill || PC.rock, line = o.line || C.ink, r = rng(o.seed || 5);
  ctx.save();
  ctx.beginPath(); poly(ctx, pts, true); ctx.fillStyle = fill; ctx.fill();
  ctx.clip();
  // gölge yüzü: ışık sol üstten (ateş/ufuk), sağ yüzler koyu
  const sh = ctx.createLinearGradient(o.lx0 ?? 900, 0, o.lx1 ?? 1920, 0);
  sh.addColorStop(0, 'rgba(255,220,170,.10)'); sh.addColorStop(.6, 'rgba(60,20,8,.0)'); sh.addColorStop(1, 'rgba(40,12,4,.45)');
  ctx.fillStyle = sh; ctx.fillRect(-4000, -4000, 9000, 9000);
  // katman (strata) çizgileri: el çizimi, kesik kesik
  ctx.strokeStyle = o.strataCol || line; ctx.lineCap = 'round';
  const [bx0, by0, bx1, by1] = bbox(pts);
  for (let k = 0; k < (o.strata ?? 14); k++) {
    const y = lerp(by0 + 40, by1, (k + r() * .5) / (o.strata ?? 14)), a = (r() - .5) * .25;
    ctx.lineWidth = 2 + r() * 2.2;
    let x = bx0 - 50;
    while (x < bx1 + 50) {
      const L = 60 + r() * 180, gap = 20 + r() * 70;
      ctx.beginPath(); ctx.moveTo(x, y + x * a * .2 + fbm1(x * .01, k) * 10);
      for (let xx = x; xx <= x + L; xx += 20) ctx.lineTo(xx, y + xx * a * .2 + fbm1(xx * .01, k) * 10);
      ctx.stroke(); x += L + gap;
    }
  }
  // kenar boyunca iç tarama (siluete hacim)
  ctx.lineWidth = 2.2; ctx.strokeStyle = o.strataCol || line;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i], p1 = pts[i + 1], d = sub(p1, p0), L = len(d); if (L < 40) continue;
    const n = scl([-d[1], d[0]], 1 / L), m = Math.floor(L / 26);
    for (let j = 1; j < m; j++) { if (r() < .45) continue; const q = add(p0, scl(d, j / m)); const l2 = 10 + r() * 22; ctx.beginPath(); ctx.moveTo(q[0] - n[0] * 4, q[1] - n[1] * 4); ctx.lineTo(q[0] - n[0] * (4 + l2), q[1] - n[1] * (4 + l2)); ctx.stroke(); }
  }
  ctx.restore();
  ctx.beginPath(); poly(ctx, pts, true); ctx.lineWidth = o.lw || 6; ctx.strokeStyle = line; ctx.lineJoin = 'round'; ctx.stroke();
}
function bbox(pts) { let a = 1e9, b = 1e9, c = -1e9, d = -1e9; for (const [x, y] of pts) { a = Math.min(a, x); b = Math.min(b, y); c = Math.max(c, x); d = Math.max(d, y); } return [a, b, c, d]; }
// Vazo alevi: üç dilli stilize alev (altın), iç çekirdek açık, hâle. t: titreme, k: büyüklük 0..1
function flame(ctx, x, y, s, t, o = {}) {
  const k = o.k ?? 1; if (k <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * k, s * k);
  if (o.halo !== false) { glow(ctx, 0, -18, o.haloR || 120, o.haloCol || 'rgba(255,190,90,.55)'); glow(ctx, 0, -14, 34, 'rgba(255,240,200,.65)'); }
  const tongue = (dx, h, w, ph, col) => {
    const sw = Math.sin(t * 7.3 + ph) * 3 + Math.sin(t * 13.1 + ph * 2) * 1.6;
    ctx.fillStyle = col; ctx.beginPath();
    ctx.moveTo(dx - w, 0);
    ctx.bezierCurveTo(dx - w * 1.1, -h * .45, dx - w * .2 + sw * .4, -h * .62, dx + sw, -h);
    ctx.bezierCurveTo(dx + w * .5 + sw * .3, -h * .6, dx + w * 1.15, -h * .4, dx + w, 0);
    ctx.quadraticCurveTo(dx, w * .5, dx - w, 0); ctx.fill();
  };
  tongue(-6, 34, 7, 1.3, PC.fireDeep); tongue(7, 30, 7, 2.1, PC.fireDeep); tongue(0, 50, 11, 0, PC.fire);
  tongue(0, 30, 6, .6, PC.fireCore);
  ctx.restore();
}
// Rezene sapı (narthex): içi boş sap, boğumlar; ucunda için için yanan ateş
function fennel(ctx, x0, y0, x1, y1, t, o = {}) {
  const a = Math.atan2(y1 - y0, x1 - x0), L = Math.hypot(x1 - x0, y1 - y0), w = o.w || 9;
  ctx.save(); ctx.translate(x0, y0); ctx.rotate(a);
  ctx.fillStyle = o.col || C.ink; ctx.strokeStyle = o.inc || PC.clayR;
  ctx.beginPath(); ctx.moveTo(0, -w * .45); ctx.lineTo(L, -w * .55); ctx.lineTo(L, w * .55); ctx.lineTo(0, w * .45); ctx.closePath(); ctx.fill();
  ctx.lineWidth = 2; for (let u = .18; u < 1; u += .21) { ctx.beginPath(); ctx.moveTo(L * u, -w * .5); ctx.lineTo(L * u, w * .5); ctx.stroke(); }
  ctx.restore();
  if (o.fire !== false) {
    const ex = x1 + Math.cos(a) * 4, ey = y1 + Math.sin(a) * 4;
    glow(ctx, ex, ey, 26, 'rgba(255,200,110,.9)');
    flame(ctx, ex, ey + 4, o.fs || 1, t, { k: o.k ?? 1, haloR: o.haloR || 140 });
  }
}
// Zincir kazığı: kayaya çakılmış kama + kelepçe halkası
function stake(ctx, x, y, s, a = 0, col = C.ink, line = null) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s);
  ctx.fillStyle = col; ctx.strokeStyle = line || C.ink; ctx.lineWidth = 1.2;
  // kayaya gömülü çivi başı (dörtgen) ve halka
  ctx.beginPath(); ctx.rect(-4.5, -4.5, 9, 9); ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.arc(-6, 0, 5, 0, TAU); ctx.lineWidth = 2.4; ctx.strokeStyle = col; ctx.stroke();
  ctx.restore();
}
// Uzakta, karanlık ovada insanların ateşleri (Prometheus'un armağanı)
function humanFires(ctx, t, pts, a = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  pts.forEach(([x, y, s], i) => {
    const fl = .85 + .15 * Math.sin(t * (5 + i) + i * 2.3);
    glow(ctx, x, y - 6 * s, 60 * s * fl, 'rgba(255,170,80,.45)');
    flame(ctx, x, y, .32 * s, t + i * .7, { halo: false });
  });
  ctx.restore();
}
// Kartal (Zeus'un kartalı): parametrik kanatlar. Yerel birim: gövde ~110 birim, +x baş yönü, y aşağı.
// o: {flap 0..1 kanat fazı (ya da ang ile sabit), spread 0..1, talon 0 kapalı..1 öne uzanmış açık pençe, beak 0..1, col, line, far}
function eagle2(ctx, x, y, s, dir, o = {}) {
  const col = o.col || PC.clayR, line = o.line || C.ink, farCol = o.farCol || mixCol(col, '#000000', .35);
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s); ctx.rotate(o.tilt || 0);
  ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  const ph = (o.flap ?? 0) * TAU, up = o.ang ?? (Math.cos(ph) * .5 + .5); // 1 yukarıda, 0 aşağıda
  const LW = 1.6;
  // kanat: iki rijit parça (kol + el); kök etrafında a1, bilekte a2 bükülür. Kanat çerçevesi: +x kökten uca, -y ön kenar
  const wing = (root, far) => {
    // profilde çırpma: kanat dikey düzlemde iner-kalkar; izdüşümde yönü neredeyse sabit, boyu |cos| kadar kısalır
    const hi = up >= .5, q = Math.abs(up * 2 - 1);
    const a1 = (hi ? lerp(-1.25, -1.95, q) : lerp(-.2, 1.05, q)) + (far ? -.16 : 0) + (o.wingA || 0);
    const fs = lerp(.34, 1, q ** .8);
    const a2 = (hi ? lerp(.1, -.3, q) : lerp(.1, .5, q)) * (o.fold ?? 1);
    const fc = far ? farCol : col, ln = far ? mixCol(line, col, .25) : line;
    ctx.save(); ctx.translate(root[0], root[1]); ctx.rotate(a1);
    ctx.scale(fs, far ? .82 : 1);
    ctx.fillStyle = fc; ctx.strokeStyle = ln;
    // kol: ön kenar hafif dışbükey, arka kenarda ikincil tüy uçları
    const inner = c => { c.moveTo(-4, -7); c.bezierCurveTo(14, -13, 36, -14, 52, -10); c.lineTo(54, 28);
      for (let k = 0; k < 5; k++) { const x0 = 54 - k * 11.5, x1 = x0 - 11.5; c.quadraticCurveTo((x0 + x1) / 2 + 1, 37 - k * .8, x1, 27 - k * .6); }
      c.quadraticCurveTo(-8, 16, -4, -7); c.closePath(); };
    ctx.beginPath(); inner(ctx); ctx.fill(); ctx.lineWidth = LW * 1.2; ctx.stroke();
    if (!far) {
      ctx.lineWidth = 1.2;
      for (let r = 0; r < 2; r++) for (let k = 0; k < 6; k++) { const qx = 6 + k * 8 + r * 4, qy = -4 + r * 7; ctx.beginPath(); ctx.arc(qx, qy, 3.6, .15, PI - .15); ctx.stroke(); }
      ctx.beginPath(); ctx.moveTo(-2, 10); ctx.quadraticCurveTo(26, 6, 53, 10); ctx.stroke();
      for (let k = 0; k < 5; k++) { const x0 = 49 - k * 11.5; ctx.beginPath(); ctx.moveTo(x0, 12); ctx.lineTo(x0 - 3, 30 - k * .7); ctx.stroke(); }
    }
    // el: bilekte bükülür, birincil tüyler parmak gibi ayrık
    ctx.translate(52, 0); ctx.rotate(a2);
    const outer = c => { c.moveTo(-2, -10); c.bezierCurveTo(16, -12, 40, -9, 60, -3);
      const tips = [[66, 1], [62, 11], [55, 19], [46, 25], [35, 29], [22, 31]];
      let prev = [60, -3];
      for (const [tx, ty] of tips) { c.quadraticCurveTo(prev[0] + 4, (prev[1] + ty) / 2, tx, ty); c.lineTo(tx - 7, ty - 4); prev = [tx - 7, ty - 4]; }
      c.lineTo(2, 28); c.closePath(); };
    ctx.beginPath(); outer(ctx); ctx.fill(); ctx.lineWidth = LW * 1.2; ctx.stroke();
    if (!far) {
      ctx.lineWidth = 1.2;
      for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.arc(6 + k * 8, -4, 3.4, .15, PI - .15); ctx.stroke(); }
      ctx.beginPath(); ctx.moveTo(0, 6); ctx.quadraticCurveTo(22, 2, 44, -2); ctx.stroke();
      for (const [tx, ty] of [[60, 0], [56, 9], [49, 17], [40, 23], [29, 27]]) { ctx.beginPath(); ctx.moveTo(lerp(6, tx, .25), lerp(8, ty, .25) - 2); ctx.lineTo(tx - 6, ty - 2); ctx.stroke(); }
    }
    ctx.restore();
  };
  wing([2, -12], true);
  // kuyruk yelpazesi
  ctx.fillStyle = col; ctx.strokeStyle = line;
  for (let i = 0; i < 5; i++) { const a = PI + lerp(-.32, .28, i / 4) + (o.tailA || 0); const tip = add([-40, 2], rot([40, 0], a)); const nrm = rot([0, 5], a);
    ctx.beginPath(); ctx.moveTo(-38 - nrm[0], 2 - nrm[1]); ctx.lineTo(tip[0] - nrm[0], tip[1] - nrm[1]); ctx.quadraticCurveTo(tip[0] + rot([5, 0], a)[0], tip[1] + rot([5, 0], a)[1], tip[0] + nrm[0], tip[1] + nrm[1]); ctx.lineTo(-38 + nrm[0], 2 + nrm[1]); ctx.closePath(); ctx.fill(); ctx.lineWidth = LW; ctx.stroke(); }
  // bacaklar ve pençeler (talon: 0 gövde altında kapalı, 1 öne uzanmış açık)
  const tk = o.talon ?? 0;
  const leg = (hip, far) => {
    const kneeA = lerp(1.9, .55, tk) + (far ? .16 : 0), knee = add(hip, rot([16, 0], kneeA));
    const ankA = lerp(1.2, .25, tk) + (far ? .2 : 0), ank = add(knee, rot([18, 0], ankA));
    ctx.fillStyle = far ? farCol : col; ctx.strokeStyle = line;
    // tüylü "pantolon"
    ctx.beginPath(); ctx.ellipse(lerp(hip[0], knee[0], .5), lerp(hip[1], knee[1], .5), 11, 7, kneeA, 0, TAU); ctx.fill(); ctx.lineWidth = LW; ctx.stroke();
    ctx.lineWidth = 5.2; ctx.beginPath(); ctx.moveTo(...knee); ctx.lineTo(...ank); ctx.stroke(); ctx.lineWidth = 3; ctx.strokeStyle = far ? farCol : col; ctx.beginPath(); ctx.moveTo(...knee); ctx.lineTo(...ank); ctx.stroke();
    // dört pençe: üçü öne, biri geriye; açıklık tk ile
    const spreadT = lerp(.25, 1, tk);
    for (const [ta, tl] of [[ankA - .9 * spreadT, 11], [ankA - .2 * spreadT, 13], [ankA + .55 * spreadT, 11], [ankA + PI - .5 * spreadT, 9]]) {
      const m = add(ank, rot([tl * .7, 0], ta)), tip = add(m, rot([tl * .45, 0], ta + 1.1));
      for (const [w, c] of [[4.2, line], [2.2, far ? farCol : col]]) { ctx.strokeStyle = c; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(...ank); ctx.quadraticCurveTo(m[0], m[1], tip[0], tip[1]); ctx.stroke(); }
    }
  };
  leg([-4, 6], true);
  // gövde
  ctx.fillStyle = col; ctx.strokeStyle = line;
  ctx.beginPath(); spline(ctx, [[-42, 0], [-26, -14], [2, -20], [24, -18], [36, -12], [40, -2], [30, 10], [6, 16], [-22, 12]]); ctx.fill(); ctx.lineWidth = LW * 1.3; ctx.stroke();
  // göğüs tüyü kavisleri
  for (let r = 0; r < 3; r++) for (let i = 0; i < 4; i++) { const qx = 26 - i * 10 - r * 4, qy = -6 + r * 6; ctx.beginPath(); ctx.arc(qx, qy, 3.4, .3, PI - .3); ctx.lineWidth = 1.1; ctx.stroke(); }
  // baş ve gaga
  const bk = o.beak ?? 0;
  ctx.save(); ctx.translate(36, -14); ctx.rotate(o.headA || 0); ctx.scale(1.22, 1.22);
  ctx.beginPath(); spline(ctx, [[-6, 6], [-2, -6], [8, -11], [17, -9], [21, -3], [18, 4], [8, 8]]); ctx.fill(); ctx.lineWidth = LW * 1.2; ctx.stroke();
  // üst gaga (çengel) ve alt gaga (açılır)
  ctx.beginPath(); ctx.moveTo(18, -7); ctx.quadraticCurveTo(30, -8, 31, 2); ctx.quadraticCurveTo(27, -2, 20, -.5); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.save(); ctx.translate(19, 0); ctx.rotate(bk * .45); ctx.beginPath(); ctx.moveTo(0, -.5); ctx.quadraticCurveTo(7, 0, 9, 2.4); ctx.quadraticCurveTo(4, 3, 0, 2.4); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
  // göz (beyaz ayrılmış halka + siyah bebek), kaş çıkıntısı
  ctx.fillStyle = o.eye || '#F3E3C0'; ctx.beginPath(); ctx.ellipse(12.4, -4.2, 2.3, 1.7, -.15, 0, TAU); ctx.fill(); ctx.lineWidth = 1; ctx.stroke();
  ctx.fillStyle = line; ctx.beginPath(); ctx.arc(13.1, -4.1, 1.15, 0, TAU); ctx.fill();
  // sert kaş çıkıntısı: gözün üstüne inen kalın çizgi (öfkeli bakış)
  ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(8.2, -7.4); ctx.quadraticCurveTo(12.6, -7.8, 17.2, -5.2); ctx.stroke();
  // ense tüyleri: başın arkasında kısa pul kavisleri (solungaç gibi okunan düz çizgiler yerine)
  ctx.lineWidth = 1.1; for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(-1 + i * 3.2, 3.5 - i * .6, 2.4, -.2, PI - .6); ctx.stroke(); }
  ctx.restore();
  leg([2, 8], false);
  wing([6, -14], false);
  ctx.restore();
}
// Devrilen taht: arka ayağın ucu çevresinde arkaya devrilir, arkalığı yere vurunca seker (devrik taht arkalığının üstünde yatar).
// p: 0 dik → 1 yerde. Üç taht motifi (Uranos, Kronos, Zeus).
function throneTip(ctx, x, y, s, p, o = {}) {
  const dir = o.dir || 1, q = E.in2(clamp(p)), bounce = p > 1 ? Math.exp(-(p - 1) * 9) * Math.sin((p - 1) * 30) * .05 : 0;
  const ang = (q * 1.43 - bounce) * dir;
  ctx.save(); ctx.translate(x - 10 * s * dir, y); ctx.rotate(-ang); ctx.translate(10 * s * dir, 0);
  if (o.shake) ctx.translate(Math.sin((window.FIG_T || 0) * 41) * o.shake, 0);
  throne(ctx, 0, 0, s, dir, o.col || C.ink, o.inc || C.clay, { high: true, stool: false });
  ctx.restore();
}
// Ayaktaki çatlak: taht ayağında yukarı doğru ilerleyen zikzak (p: 0..1)
function crackLine(ctx, x, y, h, p, o = {}) {
  const pts = sampleF(u => [x + (Math.floor(u * 7) % 2 ? 5 : -5) * (o.s || 1), y - u * h], 14);
  inkPoly(ctx, pts, p, { col: o.col || PW.red, w: o.w || 3, jit: .4 });
}
