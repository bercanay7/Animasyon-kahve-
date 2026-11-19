// Çevre: gökyüzü, tepeler, deniz, bulut, tapınak, yıldız, parçacık, zincir, gemi, inek, kartal
'use strict';
function vgrad(ctx, stops, y0 = 0, y1 = H, x0 = -W, x1 = 2 * W) {
  const g = ctx.createLinearGradient(0, y0, 0, y1);
  stops.forEach(([o, c]) => g.addColorStop(o, c));
  ctx.fillStyle = g; ctx.fillRect(x0, y0 - 2000, x1 - x0, y1 - y0 + 4000);
}
// aynı rengin saydam hali (degrade siyaha doğru kararmasın: açık hâleler leke gibi görünmesin)
function clearOf(col) {
  if (col.startsWith('#')) { const n = parseInt(col.slice(1, 7), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},0)`; }
  const m = col.match(/rgba?\(([^,]+),([^,]+),([^,)]+)/); return m ? `rgba(${m[1]},${m[2]},${m[3]},0)` : 'rgba(0,0,0,0)';
}
function glow(ctx, x, y, r, col, a = 1) {
  const g = ctx.createRadialGradient(x, y, 0, x, y, r);
  g.addColorStop(0, col); g.addColorStop(.45, col.startsWith('rgba') ? col.replace(/,([\d.]+)\)$/, (m, v) => `,${(+v * .45).toFixed(3)})`) : col + '73'); g.addColorStop(1, clearOf(col));
  ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2); ctx.restore();
}
function disk(ctx, x, y, r, col, halo = null) {
  if (halo) glow(ctx, x, y, r * 2.6, halo);
  ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
}
// Yıldızlar (sabit tohum), t ile parıltı
function stars(ctx, t, n = 220, seed = 3, col = '#F3E6C8', area = [0, 0, W, H * .7], rotA = 0, rc = [W / 2, H * 1.2]) {
  const r = rng(seed);
  ctx.save(); ctx.fillStyle = col;
  for (let i = 0; i < n; i++) {
    let x = area[0] + r() * area[2], y = area[1] + r() * area[3]; const s = r() * 1.8 + .4, ph = r() * TAU;
    if (rotA) { const q = add(rot(sub([x, y], rc), rotA), rc); x = q[0]; y = q[1]; }
    ctx.globalAlpha = .35 + .65 * (0.5 + .5 * Math.sin(t * (1 + r() * 2) + ph));
    ctx.beginPath(); ctx.arc(x, y, s, 0, TAU); ctx.fill();
  }
  ctx.restore();
}
// Uçuşan kıvılcım/toz
function motes(ctx, t, n, seed, col, area = [0, 0, W, H], sp = 20, sz = 2.2, a = .7) {
  const r = rng(seed);
  ctx.save(); ctx.fillStyle = col;
  for (let i = 0; i < n; i++) {
    const x0 = r() * area[2], y0 = r() * area[3], vy = -(r() * .7 + .3) * sp, vx = (r() - .5) * sp * .6, ph = r() * 100;
    const x = area[0] + ((x0 + vx * t + Math.sin(t * .7 + ph) * 18) % area[2] + area[2]) % area[2];
    const y = area[1] + ((y0 + vy * t) % area[3] + area[3]) % area[3];
    ctx.globalAlpha = a * (.4 + .6 * Math.sin(t * 1.3 + ph) ** 2) * Math.sin(PI * clamp((y - area[1]) / area[3]));
    ctx.beginPath(); ctx.arc(x, y, sz * (.5 + r()), 0, TAU); ctx.fill();
  }
  ctx.restore();
}
// Toz patlaması: t0 anında x,y'den
function dustBurst(ctx, t, t0, x, y, n = 30, col = 'rgba(120,70,40,.5)', spread = 160, seed = 9) {
  const u = t - t0; if (u < 0 || u > 2.5) return;
  const r = rng(seed);
  ctx.save(); ctx.fillStyle = col;
  for (let i = 0; i < n; i++) {
    const a = PI + r() * PI, v = (r() * .8 + .2) * spread;
    const px = x + Math.cos(a) * v * E.out3(clamp(u / 1.4)) * 1.4, py = y + Math.sin(a) * v * .45 * E.out3(clamp(u / 1.4)) - u * 14;
    const s = (2.5 + r() * 8) * (.6 + u * .7);
    ctx.globalAlpha = clamp(1 - u / 2.4) * .5;
    ctx.beginPath(); ctx.arc(px, py, s, 0, TAU); ctx.fill();
  }
  ctx.restore();
}
// Dalga (Vitruvius sarmalı) motifi: deniz
function waveBand(ctx, x0, x1, y, h, ph, col) {
  const w = h * 1.6;
  ctx.save(); ctx.fillStyle = col;
  const off = ((ph * w) % w + w) % w;
  ctx.beginPath(); ctx.moveTo(x0 - w, y + h);
  for (let x = x0 - w * 2 + off; x < x1 + w; x += w) {
    ctx.lineTo(x, y + h);
    ctx.bezierCurveTo(x + w * .15, y + h * .2, x + w * .62, y - h * .05, x + w * .62, y + h * .42);
    ctx.bezierCurveTo(x + w * .62, y + h * .72, x + w * .38, y + h * .72, x + w * .4, y + h * .5);
    ctx.bezierCurveTo(x + w * .45, y + h * .62, x + w * .55, y + h * .6, x + w * .52, y + h * .45);
    ctx.bezierCurveTo(x + w * .5, y + h * .1, x + w * .22, y + h * .2, x + w * .3, y + h * .62);
    ctx.bezierCurveTo(x + w * .38, y + h, x + w * .8, y + h, x + w, y + h);
  }
  ctx.lineTo(x1 + w, y + h); ctx.lineTo(x1 + w, y + 2000); ctx.lineTo(x0 - w, y + 2000); ctx.closePath(); ctx.fill();
  ctx.restore();
}
function sea(ctx, x0, x1, y, rows, h, t, col, col2) {
  for (let i = 0; i < rows; i++) {
    waveBand(ctx, x0, x1, y + i * h * .85, h * (1 + i * .12), t * (i % 2 ? .25 : -.2) + i * .37, i % 2 ? col : (col2 || col));
  }
}
// Üslup bulut: yuvarlak öbek + kazınmış sarmal
function cloud(ctx, x, y, s, col, inc = null, seed = 1) {
  const r = rng(seed);
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = col; ctx.beginPath();
  const bumps = [[-80, 8, 34], [-40, -12, 44], [8, -24, 52], [58, -8, 42], [96, 10, 30], [20, 14, 40], [-30, 16, 34]];
  for (const [bx, by, br] of bumps) { ctx.moveTo(bx + br, by); ctx.arc(bx, by, br, 0, TAU); }
  ctx.moveTo(117, 22); ctx.ellipse(4, 22, 113, 19, 0, 0, TAU); // yuvarlak taban: düz kesik kenar yok
  ctx.fill('nonzero');
  // tek bulut dili: her zaman sarmal kazıma (açık bulutta koyu, koyu bulutta açık)
  if (!inc) inc = 'rgba(150,78,46,.42)';
  if (inc) {
    ctx.strokeStyle = inc; ctx.lineWidth = 2.6; ctx.lineCap = 'round';
    for (const [bx, by, br] of bumps.slice(0, 5)) {
      ctx.beginPath();
      for (let a = 0; a < TAU * 1.4; a += .2) { const rr = br * .55 * (1 - a / (TAU * 1.6)); const px = bx + Math.cos(a + PI) * rr, py = by + Math.sin(a + PI) * rr * .8; a ? ctx.lineTo(px, py) : ctx.moveTo(px, py); }
      ctx.stroke();
    }
  }
  ctx.restore();
}
// Dor tapınağı (cephe) — x merkez, y taban, s ölçek, n sütun
function temple(ctx, x, y, s, n = 6, col = C.ink, inc = C.clay) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const w = n * 30 + 10, hw = w / 2;
  ctx.fillStyle = col;
  ctx.fillRect(-hw - 16, -8, w + 32, 8); ctx.fillRect(-hw - 10, -16, w + 20, 8); ctx.fillRect(-hw - 4, -24, w + 8, 8);
  for (let i = 0; i < n; i++) {
    const cx = -hw + 20 + i * 30;
    ctx.beginPath(); ctx.moveTo(cx - 9, -24); ctx.lineTo(cx - 7.5, -112); ctx.lineTo(cx + 7.5, -112); ctx.lineTo(cx + 9, -24); ctx.fill();
    ctx.fillRect(cx - 11, -118, 22, 6);
    ctx.strokeStyle = inc; ctx.lineWidth = 1.2;
    for (const fx of [-3.5, 0, 3.5]) { ctx.beginPath(); ctx.moveTo(cx + fx, -28); ctx.lineTo(cx + fx * .85, -108); ctx.stroke(); }
  }
  ctx.fillRect(-hw - 4, -136, w + 8, 18);
  ctx.fillRect(-hw - 6, -152, w + 12, 16);
  ctx.strokeStyle = inc; ctx.lineWidth = 1.4;
  for (let gx = -hw + 4; gx < hw; gx += 15) { ctx.beginPath(); ctx.moveTo(gx, -150); ctx.lineTo(gx, -138); ctx.moveTo(gx + 3, -150); ctx.lineTo(gx + 3, -138); ctx.stroke(); }
  ctx.beginPath(); ctx.moveTo(-hw - 10, -152); ctx.lineTo(0, -196); ctx.lineTo(hw + 10, -152); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(-hw + 12, -156); ctx.lineTo(0, -188); ctx.lineTo(hw - 12, -156); ctx.closePath(); ctx.stroke();
  ctx.restore();
}
// Sütun (iç mekân)
function column(ctx, x, y0, y1, w, col = C.ink, inc = C.clay) {
  ctx.fillStyle = col;
  ctx.beginPath(); ctx.moveTo(x - w * .5, y1); ctx.lineTo(x - w * .42, y0 + w * .35); ctx.lineTo(x + w * .42, y0 + w * .35); ctx.lineTo(x + w * .5, y1); ctx.fill();
  ctx.fillRect(x - w * .7, y0, w * 1.4, w * .22);
  ctx.beginPath(); ctx.ellipse(x, y0 + w * .3, w * .58, w * .14, 0, 0, TAU); ctx.fill();
  ctx.fillRect(x - w * .62, y1 - w * .12, w * 1.24, w * .12);
  ctx.strokeStyle = inc; ctx.lineWidth = Math.max(1, w * .03);
  for (let k = -2; k <= 2; k++) { ctx.beginPath(); ctx.moveTo(x + k * w * .16, y1 - w * .16); ctx.lineTo(x + k * w * .135, y0 + w * .45); ctx.stroke(); }
}
// Zincir: noktalar boyunca halkalar
function chain(ctx, pts, L = 22, col = C.ink, inc = null, wid = 6, sag = 0, pitch = 0) {
  // toplam yol boyunca eşit aralıkla; pitch verilirse ilk noktadan sabit adımla (boy değişince halkalar yerinde kalır, fazlası kazık halkasına girer)
  const seg = []; let tot = 0;
  for (let i = 1; i < pts.length; i++) { const l = len(sub(pts[i], pts[i - 1])); seg.push(l); tot += l; }
  const sp = pitch || tot / Math.max(1, Math.floor(tot / (L * .78))), n = Math.max(1, Math.ceil(tot / sp - .5));
  const at = d => { let k = 0; while (k < seg.length - 1 && d > seg[k]) { d -= seg[k]; k++; } const u = clamp(d / seg[k]); return [lerp(pts[k][0], pts[k + 1][0], u), lerp(pts[k][1], pts[k + 1][1], u), Math.atan2(pts[k + 1][1] - pts[k][1], pts[k + 1][0] - pts[k][0])]; };
  ctx.save(); ctx.lineWidth = wid; ctx.strokeStyle = col; ctx.fillStyle = col;
  for (let i = 0; i < n; i++) {
    const [x, y, a] = at(Math.min(tot, (i + .5) * sp));
    ctx.save(); ctx.translate(x, y); ctx.rotate(a);
    if (pitch && i === n - 1) ctx.globalAlpha *= clamp((tot - (n - .5) * sp) / sp * 2);
    if (i % 2 === 0) { ctx.beginPath(); ctx.ellipse(0, 0, L * .5, L * .3, 0, 0, TAU); ctx.stroke(); }
    else { ctx.fillRect(-L * .5, -wid * .6, L, wid * 1.2); }
    if (inc && i % 2 === 0) { ctx.strokeStyle = inc; ctx.lineWidth = wid * .25; ctx.beginPath(); ctx.ellipse(0, -wid * .1, L * .5, L * .3, 0, PI * 1.1, PI * 1.6); ctx.stroke(); ctx.strokeStyle = col; ctx.lineWidth = wid; }
    ctx.restore();
  }
  ctx.restore();
}
// Kelepçe
function shackle(ctx, x, y, r, a, col = C.ink, open = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a);
  ctx.strokeStyle = col; ctx.lineWidth = r * .45;
  ctx.beginPath(); ctx.arc(0, 0, r, -PI / 2 + open * 1.4, PI * 1.5); ctx.stroke();
  ctx.fillStyle = col; ctx.fillRect(-r * .3, -r * 1.5, r * .6, r * .6);
  ctx.restore();
}
// Yıldırım (keraunos)
function bolt(ctx, x, y, s, a, col = C.gold, glowCol = 'rgba(255,220,140,.55)') {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s);
  glow(ctx, 0, 0, 120, glowCol);
  ctx.fillStyle = col; ctx.strokeStyle = C.ink; ctx.lineWidth = 2.4; ctx.lineJoin = 'round';
  ctx.beginPath();
  ctx.moveTo(0, -78); ctx.lineTo(9, -40); ctx.lineTo(3, -38); ctx.lineTo(13, -10); ctx.lineTo(5, -8); ctx.lineTo(8, 0);
  ctx.lineTo(5, 8); ctx.lineTo(13, 10); ctx.lineTo(3, 38); ctx.lineTo(9, 40); ctx.lineTo(0, 78);
  ctx.lineTo(-9, 40); ctx.lineTo(-3, 38); ctx.lineTo(-13, 10); ctx.lineTo(-5, 8); ctx.lineTo(-8, 0);
  ctx.lineTo(-5, -8); ctx.lineTo(-13, -10); ctx.lineTo(-3, -38); ctx.lineTo(-9, -40); ctx.closePath();
  ctx.fill(); ctx.stroke();
  ctx.fillStyle = C.ink; ctx.fillRect(-9, -4, 18, 8);
  ctx.restore();
}
// Yıldırım çakması (dallanan çizgi)
function lightning(ctx, x0, y0, x1, y1, seed, w = 6, col = '#FFF4D6') {
  const r = rng(seed);
  const pts = [[x0, y0]]; const n = 9;
  for (let i = 1; i < n; i++) { const u = i / n; pts.push([lerp(x0, x1, u) + (r() - .5) * 90, lerp(y0, y1, u) + (r() - .5) * 20]); }
  pts.push([x1, y1]);
  ctx.save(); ctx.strokeStyle = col; ctx.lineJoin = 'miter'; ctx.shadowColor = '#FFE6A0'; ctx.shadowBlur = 30;
  ctx.lineWidth = w; ctx.beginPath(); poly(ctx, pts, false); ctx.stroke();
  ctx.lineWidth = w * .4; for (let k = 2; k < n; k += 3) { ctx.beginPath(); ctx.moveTo(...pts[k]); ctx.lineTo(pts[k][0] + (r() - .5) * 160, pts[k][1] + 80 + r() * 80); ctx.stroke(); }
  ctx.restore();
}
// Ticaret gemisi (siyah figür)
function ship(ctx, x, y, s, t, col = C.ink, inc = C.clay, sail = '#E9DCC0') {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const bob = Math.sin(t * 1.6) * 2.5, rl = Math.sin(t * 1.3) * .02;
  ctx.translate(0, bob); ctx.rotate(rl);
  ctx.fillStyle = col;
  // gövde
  ctx.beginPath(); ctx.moveTo(-120, -20); ctx.quadraticCurveTo(-130, -46, -112, -58); ctx.lineTo(-104, -50);
  ctx.quadraticCurveTo(-104, -30, -90, -24); ctx.lineTo(96, -24); ctx.quadraticCurveTo(116, -26, 128, -46);
  ctx.lineTo(136, -44); ctx.quadraticCurveTo(130, -10, 108, 4); ctx.lineTo(-100, 4); ctx.quadraticCurveTo(-116, -2, -120, -20); ctx.fill();
  // göz (apotropaik)
  ctx.fillStyle = sail; ctx.beginPath(); ctx.ellipse(106, -14, 7, 4, 0, 0, TAU); ctx.fill();
  ctx.fillStyle = col; ctx.beginPath(); ctx.arc(107, -14, 2.4, 0, TAU); ctx.fill();
  ctx.strokeStyle = inc; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(-96, -12); ctx.lineTo(92, -12); ctx.stroke();
  // kürekler
  ctx.strokeStyle = col; ctx.lineWidth = 2.4;
  for (let i = 0; i < 9; i++) { const ox = -78 + i * 19, a = Math.sin(t * 3 + i * .1) * .25; ctx.beginPath(); ctx.moveTo(ox, -8); ctx.lineTo(ox - 14 + Math.sin(a) * 20, 26); ctx.stroke(); }
  // direk ve yelken
  ctx.fillStyle = col; ctx.fillRect(-3, -150, 6, 128);
  ctx.fillRect(-70, -150, 140, 5);
  const bl = Math.sin(t * 1.1) * 4;
  ctx.fillStyle = sail; ctx.beginPath(); ctx.moveTo(-66, -145); ctx.lineTo(66, -145); ctx.quadraticCurveTo(72 + bl, -100, 60, -62); ctx.lineTo(-60, -62); ctx.quadraticCurveTo(-72 + bl, -100, -66, -145); ctx.fill();
  ctx.strokeStyle = col; ctx.lineWidth = 2; ctx.stroke();
  ctx.lineWidth = 1.2; for (let k = -2; k <= 2; k++) { ctx.beginPath(); ctx.moveTo(k * 24, -145); ctx.lineTo(k * 22 + bl * .3, -62); ctx.stroke(); }
  ctx.beginPath(); ctx.moveTo(-60, -62); ctx.lineTo(-110, -40); ctx.moveTo(60, -62); ctx.lineTo(110, -40); ctx.stroke();
  ctx.restore();
}
// Amfora
function amphora(ctx, x, y, s, col = C.ink, band = C.red) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = col; ctx.beginPath();
  ctx.moveTo(-7, -60); ctx.lineTo(7, -60); ctx.lineTo(6, -52); ctx.quadraticCurveTo(26, -44, 24, -20);
  ctx.quadraticCurveTo(20, 0, 6, 10); ctx.lineTo(4, 16); ctx.lineTo(-4, 16); ctx.lineTo(-6, 10); ctx.quadraticCurveTo(-20, 0, -24, -20);
  ctx.quadraticCurveTo(-26, -44, -6, -52); ctx.closePath(); ctx.fill();
  ctx.lineWidth = 3; ctx.strokeStyle = col;
  ctx.beginPath(); ctx.moveTo(-6, -54); ctx.quadraticCurveTo(-20, -56, -18, -42); ctx.moveTo(6, -54); ctx.quadraticCurveTo(20, -56, 18, -42); ctx.stroke();
  ctx.fillStyle = band; ctx.fillRect(-22, -30, 44, 3);
  ctx.restore();
}
// Taht (klismos): x arka ayak hizası, y zemin, s ölçek, dir yön
// karanlıkta boş taht: koyu sır gövde, sol üstten soğuk beyaz kenar ışığı (Zeus'un rengi); zeminden ayrılır
function throneRim(ctx, x, y, s, dir = 1, o = {}) {
  ctx.save(); glow(ctx, x - 20 * s * dir, y - 40 * s, 46 * s, 'rgba(170,186,235,.25)');
  throne(ctx, x - 5, y - 5, s, dir, 'rgba(230,236,255,.85)', 'rgba(230,236,255,.85)', o);
  throne(ctx, x, y, s, dir, '#2C1D16', 'rgba(190,200,235,.42)', o); ctx.restore();
}
function throne(ctx, x, y, s, dir = 1, col = C.ink, inc = C.clay, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
  ctx.fillStyle = col; ctx.strokeStyle = col; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const sh = o.seat ?? 25;
  // arka ayak (kavisli) ve arkalık
  ctx.lineWidth = 3.2; ctx.beginPath(); ctx.moveTo(-10, 0); ctx.quadraticCurveTo(-6, -sh * .5, -8, -sh); ctx.quadraticCurveTo(-12, -sh - 18, -16, -sh - 30); ctx.stroke();
  ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(18, 0); ctx.quadraticCurveTo(14, -sh * .5, 16, -sh); ctx.stroke();
  ctx.fillRect(-12, -sh - 3, 32, 4.5);
  ctx.beginPath(); ctx.moveTo(-18, -sh - 32); ctx.quadraticCurveTo(-9, -sh - 34, -10, -sh - 24); ctx.lineTo(-14, -sh - 25); ctx.closePath(); ctx.fill();
  if (o.high) { ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-14, -sh - 28); ctx.lineTo(-14, -sh - 58); ctx.stroke(); ctx.beginPath(); ctx.arc(-14, -sh - 60, 3.4, 0, TAU); ctx.fill(); }
  ctx.strokeStyle = inc; ctx.lineWidth = .8; ctx.beginPath(); ctx.moveTo(-11, -sh - 1); ctx.lineTo(19, -sh - 1); ctx.stroke();
  // ayak taburesi
  if (o.stool !== false) { ctx.fillStyle = col; ctx.fillRect(22, -5, 20, 5); ctx.fillRect(24, -1, 3, 1); }
  ctx.restore();
}
// Gündüz göğü (açık kil) ve gece göğü
function daySky(ctx, warm = 0) { clayBG(ctx, mixCol('#E09A68', '#EAB27A', warm), mixCol('#B85C33', '#C8703E', warm)); }
function nightSky(ctx) { clayBG(ctx, '#4A2117', '#24100B'); }
// Şehir: surlar, evler, kapı
function city(ctx, x, y, s, col = C.ink, inc = C.clay, seed = 2) {
  const r = rng(seed);
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col;
  // evler (arkada)
  for (let i = 0; i < 9; i++) {
    const hx = -220 + i * 52 + r() * 10, hw = 40 + r() * 20, hh = 40 + r() * 46;
    ctx.fillRect(hx, -hh - 60, hw, hh + 60);
    ctx.beginPath(); ctx.moveTo(hx - 4, -hh - 60); ctx.lineTo(hx + hw / 2, -hh - 80); ctx.lineTo(hx + hw + 4, -hh - 60); ctx.fill();
    ctx.fillStyle = inc; ctx.fillRect(hx + hw * .35, -hh - 40, hw * .18, 12); ctx.fillStyle = col;
  }
  // surlar
  ctx.fillRect(-260, -70, 520, 70);
  for (let k = -260; k < 260; k += 26) ctx.fillRect(k, -84, 14, 16);
  ctx.fillRect(-300, -120, 50, 120); ctx.fillRect(250, -120, 50, 120);
  for (const tx of [-300, 250]) for (let k = 0; k < 3; k++) ctx.fillRect(tx + k * 18, -134, 12, 16);
  ctx.fillStyle = inc; ctx.beginPath(); ctx.moveTo(-26, 0); ctx.lineTo(-26, -40); ctx.quadraticCurveTo(0, -62, 26, -40); ctx.lineTo(26, 0); ctx.fill();
  ctx.strokeStyle = inc; ctx.lineWidth = 2; for (let k = -250; k < 250; k += 40) { ctx.beginPath(); ctx.moveTo(k, -50); ctx.lineTo(k + 30, -50); ctx.stroke(); }
  ctx.restore();
}
// Ahır
function barn(ctx, x, y, s, col = C.ink, inc = C.clay, open = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col;
  ctx.fillRect(-120, -150, 240, 150);
  ctx.beginPath(); ctx.moveTo(-140, -150); ctx.lineTo(0, -230); ctx.lineTo(140, -150); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = inc; ctx.lineWidth = 2.4;
  for (let k = -110; k < 120; k += 22) { ctx.beginPath(); ctx.moveTo(k, -146); ctx.lineTo(k, -4); ctx.stroke(); }
  // kapı
  ctx.fillStyle = '#2A1810'; ctx.fillRect(-50, -120, 100, 120);
  ctx.save(); ctx.translate(-50, 0); ctx.scale(1 - open * .9, 1);
  ctx.fillStyle = col; ctx.fillRect(0, -120, 50, 120); ctx.strokeStyle = inc; ctx.beginPath(); ctx.moveTo(2, -118); ctx.lineTo(48, -2); ctx.stroke(); ctx.restore();
  ctx.save(); ctx.translate(50, 0); ctx.scale(1 - open * .9, 1);
  ctx.fillStyle = col; ctx.fillRect(-50, -120, 50, 120); ctx.strokeStyle = inc; ctx.beginPath(); ctx.moveTo(-2, -118); ctx.lineTo(-48, -2); ctx.stroke(); ctx.restore();
  ctx.restore();
}
// Toynak izi (U biçimi) ve harf damgası
function hoofPrint(ctx, x, y, s, col = 'rgba(40,20,10,.75)') {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s * .45); ctx.fillStyle = col;
  ctx.beginPath(); ctx.ellipse(-4, 0, 3.4, 6, -.15, 0, TAU); ctx.ellipse(4, 0, 3.4, 6, .15, 0, TAU); ctx.fill(); ctx.restore();
}
// Pınar: t0 anında x,y'den fışkıran su (beyaz yaylar + damlalar)
function spring(ctx, x, y, t, t0, col = '#F4EEDD', power = 1) {
  const u = t - t0; if (u < 0) return;
  const grow = E.out3(clamp(u / .6)) * power;
  ctx.save(); ctx.strokeStyle = col; ctx.lineCap = 'round';
  for (let i = 0; i < 9; i++) {
    const a = -PI / 2 + (i - 4) * .16, v = (520 + hash(i) * 140) * grow, g = 900;
    ctx.lineWidth = 7 - Math.abs(i - 4) * .8; ctx.globalAlpha = .85;
    ctx.beginPath();
    for (let k = 0; k <= 40; k++) {
      const tt = k / 40 * 1.9 * grow + Math.sin(t * 12 + i) * .004;
      const px = x + Math.cos(a) * v * tt, py = y + Math.sin(a) * v * tt + .5 * g * tt * tt;
      if (py > y + 150) { ctx.lineTo(px, y + 150); break; }
      k ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
    }
    ctx.stroke();
  }
  ctx.fillStyle = col;
  for (let i = 0; i < 60; i++) {
    const ph = (t * (1.1 + hash(i) * .6) + hash(i * 7)) % 1;
    const a = -PI / 2 + (hash(i * 3) - .5) * 1.4, v = (380 + hash(i * 5) * 260) * grow, g = 900, tt = ph * 1.2;
    const px = x + Math.cos(a) * v * tt, py = y + Math.sin(a) * v * tt + .5 * g * tt * tt;
    if (py > y + 30) continue;
    ctx.globalAlpha = .8 * (1 - ph * .6);
    ctx.beginPath(); ctx.arc(px, py, 3 + hash(i) * 3, 0, TAU); ctx.fill();
  }
  ctx.restore();
}
// Çeşme evi (Peirene): sütunlu yapı, aslan ağızlı oluk
function fountainHouse(ctx, x, y, s, t, col = C.ink, inc = C.clay) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = col;
  ctx.fillRect(-260, -300, 520, 30);
  ctx.beginPath(); ctx.moveTo(-280, -300); ctx.lineTo(0, -380); ctx.lineTo(280, -300); ctx.fill();
  for (const cx of [-240, 240]) column(ctx, cx, -270, 0, 36, col, inc);
  ctx.fillRect(-200, -186, 400, 12); // raf aslan başlarının arkasında (su önünden düşer)
  // aslan başları
  for (const lx of [-90, 90]) {
    ctx.beginPath(); ctx.arc(lx, -170, 18, 0, TAU); ctx.fill();
    ctx.beginPath(); ctx.moveTo(lx + 10, -168); ctx.lineTo(lx + 26, -160); ctx.lineTo(lx + 10, -156); ctx.fill();
    // su akışı
    ctx.save(); ctx.strokeStyle = '#F4EEDD'; ctx.lineWidth = 6; ctx.globalAlpha = .9;
    ctx.beginPath(); ctx.moveTo(lx + 24, -160); ctx.quadraticCurveTo(lx + 40, -150, lx + 42 + Math.sin(t * 20 + lx) * 1.5, -40); ctx.stroke(); // havuza kadar
    ctx.restore();
  }
  ctx.fillRect(-220, -40, 440, 40);
  ctx.strokeStyle = inc; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(-210, -30); ctx.lineTo(210, -30); ctx.stroke();
  ctx.restore();
}
// Saray içi: zemin, sütun dizisi, isteğe bağlı kapı (open 0..1), ışık
function palace(ctx, t, o = {}) {
  const dark = o.dark ?? 0, gy = o.gy ?? 880;
  clayBG(ctx, mixCol('#C9733F', '#3A1A12', dark), mixCol('#8E4022', '#160A07', dark));
  ctx.fillStyle = mixCol(C.ink, '#0A0504', dark); ctx.fillRect(0, gy, W, H - gy);
  ctx.strokeStyle = mixCol(C.clayD, '#3A1A10', dark); ctx.lineWidth = 2;
  for (let k = 0; k < 6; k++) { ctx.beginPath(); ctx.moveTo(0, gy + 8 + k * 32); ctx.lineTo(W, gy + 8 + k * 32); ctx.stroke(); }
  if (o.door !== undefined) {
    const dx = o.doorX ?? W / 2, dw = 300, dh = 560, op = o.door;
    ctx.fillStyle = mixCol('#2A140C', '#050202', dark); ctx.fillRect(dx - dw / 2 - 30, gy - dh - 40, dw + 60, dh + 40);
    // dışarıdan ışık
    if (op > 0) { ctx.save(); ctx.globalAlpha = op; ctx.fillStyle = '#F2D6A4'; ctx.fillRect(dx - dw / 2, gy - dh, dw, dh); glow(ctx, dx, gy - dh / 2, 600, 'rgba(255,214,150,.35)'); ctx.restore();
      ctx.save(); ctx.globalAlpha = op * .35; ctx.fillStyle = '#F2D6A4'; ctx.beginPath(); ctx.moveTo(dx - dw / 2, gy); ctx.lineTo(dx + dw / 2, gy); ctx.lineTo(dx + dw * 1.6, H); ctx.lineTo(dx - dw * 1.6, H); ctx.fill(); ctx.restore(); }
    // kanatlar
    for (const sgn of [-1, 1]) {
      ctx.save(); ctx.translate(dx + sgn * dw / 2, 0); ctx.scale(1 - op * .85, 1);
      ctx.fillStyle = mixCol(C.ink, '#0A0504', dark); ctx.fillRect(sgn > 0 ? -dw / 2 : 0, gy - dh, dw / 2, dh);
      ctx.strokeStyle = mixCol(C.clayD, '#3A1A10', dark); ctx.lineWidth = 3;
      for (let k = 1; k < 4; k++) { ctx.beginPath(); ctx.moveTo(sgn > 0 ? -dw / 2 : 0, gy - dh + k * dh / 4); ctx.lineTo(sgn > 0 ? 0 : dw / 2, gy - dh + k * dh / 4); ctx.stroke(); }
      ctx.restore();
    }
  }
  for (const cx of (o.cols || [140, 520, 1400, 1780])) column(ctx, cx, 120, gy, 70, mixCol(C.ink, '#0A0504', dark), mixCol(C.clay, '#4A2414', dark));
  ctx.fillStyle = mixCol(C.ink, '#0A0504', dark); ctx.fillRect(0, 70, W, 50);
  meander(ctx, 0, W, 72, 40, mixCol(C.clayD, '#3A1A10', dark));
}
// Sunak
function altar(ctx, x, y, s, col = C.ink, inc = C.clay, fire = 0, t = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col;
  ctx.fillRect(-40, -60, 80, 60); ctx.fillRect(-48, -70, 96, 12); ctx.fillRect(-48, -6, 96, 6);
  ctx.strokeStyle = inc; ctx.lineWidth = 1.5; ctx.strokeRect(-32, -50, 64, 38);
  // sunak ateşi (renk kuralı: altın alev, sivri dil biçimi, açık çekirdek, sır kontur; filmin öbür ateşleriyle aynı dil)
  if (fire > 0) {
    ctx.globalAlpha = fire; ctx.lineJoin = 'round';
    for (let i = 0; i < 4; i++) {
      const fx = -22 + i * 15, fh = 30 + Math.sin(t * 9 + i * 2) * 8 + (i === 1 || i === 2 ? 10 : 0), lean = Math.sin(t * 5 + i) * 3;
      const tongue = (w, h) => { ctx.beginPath(); ctx.moveTo(fx - w, -70); ctx.bezierCurveTo(fx - w * 1.1, -70 - h * .45, fx + lean - w * .3, -70 - h * .7, fx + lean, -70 - h); ctx.bezierCurveTo(fx + lean + w * .4, -70 - h * .65, fx + w * 1.1, -70 - h * .4, fx + w, -70); ctx.closePath(); };
      tongue(8, fh); ctx.fillStyle = C.gold; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.6; ctx.stroke();
      tongue(3.5, fh * .5); ctx.fillStyle = '#FFF6D6'; ctx.fill();
    }
  }
  ctx.restore();
}
// Kline (sedir)
function kline(ctx, x, y, s, col = C.ink, inc = C.clay) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col;
  ctx.fillRect(-60, -30, 130, 7); ctx.fillRect(-56, -23, 6, 23); ctx.fillRect(58, -23, 6, 23);
  ctx.beginPath(); ctx.moveTo(-64, -30); ctx.quadraticCurveTo(-66, -48, -56, -52); ctx.lineTo(-52, -30); ctx.fill();
  ctx.fillStyle = C.red; ctx.beginPath(); ctx.ellipse(-48, -36, 10, 6, -.3, 0, TAU); ctx.fill();
  ctx.strokeStyle = inc; ctx.lineWidth = .8; ctx.beginPath(); ctx.moveTo(-58, -26); ctx.lineTo(68, -26); ctx.stroke();
  ctx.restore();
}
// Kandil
function oilLamp(ctx, x, y, s, t) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  glow(ctx, 0, -14, 260, 'rgba(255,190,110,.35)');
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.ellipse(0, 0, 18, 6, 0, 0, TAU); ctx.fill(); ctx.fillRect(14, -3, 10, 4);
  const fh = 12 + Math.sin(t * 13) * 2 + Math.sin(t * 7.3) * 1.5;
  ctx.fillStyle = '#FFD488'; ctx.beginPath(); ctx.moveTo(19, -3); ctx.quadraticCurveTo(24, -3 - fh * .6, 21, -3 - fh); ctx.quadraticCurveTo(17, -3 - fh * .5, 19, -3); ctx.fill();
  ctx.restore();
}
// Yeraltı (kırmızı figür zemin): kara zemin, sönük meşaleler, asfodel
function underworld(ctx, t, o = {}) {
  ctx.fillStyle = '#0B0605'; ctx.fillRect(0, 0, W, H);
  glow(ctx, W / 2, 420, 900, 'rgba(120,50,25,.28)');
  const gy = o.gy ?? 880;
  // zemin, meşaleler ve asfodeller dünya koordinatında (kamera ile ölçeklenir); friz çerçevesi ekranda, en üstte
  ctx.save(); if (o.c) cam(ctx, o.c, 1);
  ctx.fillStyle = '#1A0D09'; ctx.fillRect(-W, gy, 3 * W, 2 * H);
  ctx.fillStyle = '#C7683C'; ctx.fillRect(-W, gy, 3 * W, 3);
  for (const x of (o.torches || [180, 1740])) { ctx.fillStyle = '#C7683C'; ctx.fillRect(x - 5, 330, 10, 120); ctx.save(); ctx.translate(x, 330); ctx.fillStyle = C.gold; const fh = 30 + Math.sin(t * 11 + x) * 6; ctx.beginPath(); ctx.moveTo(-12, 0); ctx.quadraticCurveTo(0, -fh * 1.4, 12, 0); ctx.fill(); glow(ctx, 0, -14, 160, 'rgba(255,180,90,.3)'); ctx.restore(); }
  ctx.strokeStyle = '#C7683C'; ctx.lineWidth = 2;
  for (let i = 0; i < 14; i++) { const x = 60 + i * 140 + hash(i) * 40; ctx.beginPath(); ctx.moveTo(x, gy); ctx.quadraticCurveTo(x + 6, gy - 40, x + Math.sin(t + i) * 4, gy - 70); ctx.stroke(); ctx.fillStyle = '#C7683C'; ctx.beginPath(); ctx.arc(x + Math.sin(t + i) * 4, gy - 74, 5, 0, TAU); ctx.fill(); }
  ctx.restore();
  if (!o.noFrame) underworldFrame(ctx);
}
function underworldFrame(ctx) {
  ctx.fillStyle = '#0B0605'; ctx.fillRect(0, 0, W, 104);
  meander(ctx, 0, W, 60, 40, '#C7683C');
  ctx.fillStyle = '#1A0D09'; ctx.fillRect(0, H - 56, W, 56);
  tongues(ctx, 0, W, H - 50, 46, '#C7683C');
}
// Modern şehir silueti (beyaz zemin üslubu)
function skyline(ctx, x0, x1, y, col, seed = 3, hmax = 260, win = null) {
  // 1940'lar şehir silueti: çatılar, kubbe, baca, pencereler
  const r = rng(seed); ctx.fillStyle = col;
  for (let x = x0; x < x1;) {
    const w = 60 + r() * 120, h = 80 + r() * hmax, kind = r();
    ctx.fillStyle = col; ctx.fillRect(x, y - h, w, h);
    if (kind < .25) { ctx.beginPath(); ctx.moveTo(x - 4, y - h); ctx.lineTo(x + w / 2, y - h - w * .35); ctx.lineTo(x + w + 4, y - h); ctx.fill(); }
    else if (kind < .35) { ctx.beginPath(); ctx.arc(x + w / 2, y - h, w * .36, PI, TAU); ctx.fill(); ctx.fillRect(x + w / 2 - 3, y - h - w * .36 - 26, 6, 26); }
    else if (kind < .6) { ctx.fillRect(x + w * .2, y - h - 34, 12, 34); ctx.fillRect(x + w * .6, y - h - 22, 10, 22); }
    if (win) { ctx.fillStyle = win; for (let wy = y - h + 18; wy < y - 24; wy += 30) for (let wx = x + 10; wx < x + w - 14; wx += 22) if (r() < .55) ctx.fillRect(wx, wy, 9, 13); }
    x += w + 4 + r() * 10;
  }
}
function plane(ctx, x, y, s, col) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col;
  // 1940'lar pervaneli bombardıman uçağı (yandan)
  ctx.beginPath(); ctx.ellipse(0, 0, 52, 7.5, 0, 0, TAU); ctx.fill();
  ctx.beginPath(); ctx.moveTo(-40, -2); ctx.lineTo(-54, -22); ctx.lineTo(-46, -22); ctx.lineTo(-30, -4); ctx.closePath(); ctx.fill();
  ctx.fillRect(-56, -2, 22, 3);
  ctx.fillRect(-14, 1, 34, 4);
  for (const ex of [6, 20]) { ctx.beginPath(); ctx.ellipse(ex, 5, 7, 4, 0, 0, TAU); ctx.fill(); ctx.fillRect(ex + 7, -3, 2, 16); }
  ctx.beginPath(); ctx.ellipse(46, -3, 8, 4, 0, 0, TAU); ctx.fill();
  ctx.restore();
}
function clock(ctx, x, y, r, t, col = C.inkSoft, face = '#FFF9EC', ring = 0) {
  ctx.save(); ctx.translate(x + Math.sin(t * 60) * ring * 3, y);
  ctx.fillStyle = col; ctx.beginPath(); ctx.arc(-r * .6, -r * .9, r * .35, 0, TAU); ctx.arc(r * .6, -r * .9, r * .35, 0, TAU); ctx.fill();
  ctx.beginPath(); ctx.arc(0, 0, r, 0, TAU); ctx.fill(); ctx.fillStyle = face; ctx.beginPath(); ctx.arc(0, 0, r * .8, 0, TAU); ctx.fill();
  ctx.strokeStyle = col; ctx.lineWidth = r * .1; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -r * .6); ctx.moveTo(0, 0); ctx.lineTo(r * .4, r * .1); ctx.stroke();
  ctx.fillRect(-r * .7, r * .7, r * .2, r * .4); ctx.fillRect(r * .5, r * .7, r * .2, r * .4);
  if (ring) { ctx.lineWidth = r * .06; for (const sgn of [-1, 1]) { ctx.beginPath(); ctx.arc(sgn * r * 1.5, -r * .4, r * .4, -.6, .6); ctx.stroke(); } }
  ctx.restore();
}
function desk(ctx, x, y, s, col) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.fillStyle = col;
  ctx.fillRect(-60, -48, 120, 6); ctx.fillRect(-56, -42, 5, 42); ctx.fillRect(51, -42, 5, 42);
  // daktilo
  ctx.fillRect(-18, -60, 36, 12); ctx.fillRect(-14, -66, 28, 6); ctx.fillStyle = '#FFF9EC'; ctx.fillRect(-10, -80, 20, 16);
  ctx.restore();
}
