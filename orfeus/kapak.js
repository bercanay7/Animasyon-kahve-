// Orfeus ve Evridiki — YouTube kapağı (1920×1080 çizilir, 1280×720 dışa aktarılır)
// Üslup videoyla aynı: katmanlı kâğıt kesme / düz vektör, dalgalı ve kenarı açık çizgili bulutlar, köşeli (low-poly) kayalar, ateş böceği kıvılcımları, dokulu yüzey.
// Kanca: yeryüzüne çıkışın eşiğinde Orfeus geri döner; Evridiki parmak uçları değmeden ışık zerrelerine dönüşür.
// Kullanım: kapak.html?v=a|b  (a: ARKANA BAKMA!, b: NEDEN BAKTI?)  &notext=1
'use strict';
const W = 1920, H = 1080, TAU = Math.PI * 2, PI = Math.PI;
const Q = new URLSearchParams(location.search);
const cv = document.getElementById('c'); cv.width = W; cv.height = H;
const ctx = cv.getContext('2d');
const lerp = (a, b, t) => a + (b - a) * t;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
function rng(seed) { let s = (seed * 2654435761) >>> 0 || 1; return () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; }; }
function hex(c) { if (Array.isArray(c)) return c; if (c[0] !== '#') return c.match(/[\d.]+/g).slice(0, 3).map(Number); const n = parseInt(c.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function mix(a, b, t) { const A = hex(a), B = hex(b); t = clamp(t); return `rgb(${A.map((v, i) => Math.round(lerp(v, B[i], t))).join(',')})`; }
function rgba(c, a) { const A = hex(c); return `rgba(${A[0]},${A[1]},${A[2]},${a})`; }
function glow(g, x, y, r, c, a) { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, rgba(c, a)); gr.addColorStop(.4, rgba(c, a * .45)); gr.addColorStop(1, rgba(c, 0)); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
function layer() { const c = document.createElement('canvas'); c.width = W; c.height = H; return [c, c.getContext('2d')]; }
// Catmull-Rom → bezier düzgün eğri
function sp(p, pts, closed = true, k = 1) {
  const n = pts.length; p.moveTo(pts[0][0], pts[0][1]);
  for (let i = 0; i < (closed ? n : n - 1); i++) {
    const p1 = pts[i], p2 = pts[(i + 1) % n];
    const p0 = !closed && i === 0 ? p1 : pts[(i - 1 + n) % n], p3 = !closed && i + 2 >= n ? p2 : pts[(i + 2) % n];
    p.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k, p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k, p2[0], p2[1]);
  }
  if (closed) p.closePath();
}
const path = (pts, closed = true, k = 1) => { const p = new Path2D(); sp(p, pts, closed, k); return p; };
const poly = pts => { const p = new Path2D(); pts.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); p.closePath(); return p; };

// ——— üslup öğeleri ———
// dalgalı bulut şeridi: kâğıt katmanı, altında gölge, üst kıvrımlarda açık kenar çizgisi
function cloudBank(g, x0, x1, y, rmin, rmax, fill, rim, seed, o = {}) {
  const r = rng(seed), pts = []; let x = x0 - rmax;
  while (x < x1 + rmax) { const rr = lerp(rmin, rmax, r()); pts.push([x, y - rr * (.3 + r() * .35), rr]); x += rr * (.95 + r() * .4); }
  const p = new Path2D(); for (const [cx, cy, rr] of pts) { p.moveTo(cx + rr, cy); p.arc(cx, cy, rr, 0, TAU); }
  p.rect(x0 - rmax, y - 2, x1 - x0 + 2 * rmax, o.depth ?? 360);
  if (o.shadow) { g.save(); g.translate(0, o.sh ?? 10); g.fillStyle = o.shadow; g.fill(p); g.restore(); }
  g.fillStyle = fill; g.fill(p);
  if (rim) { g.save(); g.clip(p); g.strokeStyle = rim; g.lineWidth = o.rw ?? 4; g.lineCap = 'round';
    for (const [cx, cy, rr] of pts) { g.beginPath(); g.arc(cx, cy, rr - (o.rin ?? 8), PI * 1.15, PI * 1.85); g.stroke(); } g.restore(); }
}
// videodaki çok tonlu bulut: alttan üste açılan kâğıt katmanları, her katın altı bir alttakini şerit gibi gösterir
function puffs(g, x0, x1, y, r0, r1, tones, rim, seed, o = {}) {
  const n = tones.length, step = o.step ?? 16, inset = o.inset ?? 26;
  for (let k = 0; k < n; k++) {
    const sc = 1 - k * .1;
    cloudBank(g, x0 + k * inset, x1 - k * inset, y - k * step, r0 * sc, r1 * sc, tones[k], k === n - 1 ? rim : null, seed + k * 7,
      { depth: o.depth ?? 34, shadow: k === 0 ? o.shadow : null, sh: o.sh ?? 12, rw: o.rw ?? 5, rin: o.rin ?? 7 });
  }
}
// köşeli kaya yüzeyi: titrek ızgaradan üçgenler, her yüzün tonu ayrı
function lowPoly(g, clip, bx0, by0, bx1, by1, cell, seed, shade) {
  const r = rng(seed), nx = Math.ceil((bx1 - bx0) / cell), ny = Math.ceil((by1 - by0) / cell), P = [];
  for (let j = 0; j <= ny; j++) for (let i = 0; i <= nx; i++) P.push([bx0 + i * cell + (r() - .5) * cell * .8, by0 + j * cell + (r() - .5) * cell * .8]);
  const id = (i, j) => P[j * (nx + 1) + i];
  g.save(); if (clip) g.clip(clip, 'evenodd');
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const a = id(i, j), b = id(i + 1, j), c = id(i + 1, j + 1), d = id(i, j + 1);
    for (const t of (r() < .5 ? [[a, b, c], [a, c, d]] : [[a, b, d], [b, c, d]])) {
      const cx = (t[0][0] + t[1][0] + t[2][0]) / 3, cy = (t[0][1] + t[1][1] + t[2][1]) / 3, col = shade(cx, cy, r());
      const pp = poly(t); g.fillStyle = col; g.strokeStyle = col; g.lineWidth = 1.5; g.fill(pp); g.stroke(pp);
    }
  }
  g.restore();
}
function sparkle(g, x, y, s, col, a = 1) {
  g.save(); g.globalAlpha = a; glow(g, x, y, s * 4, col, .55);
  g.fillStyle = '#fffbe8'; g.beginPath();
  for (let i = 0; i < 8; i++) { const ang = i / 8 * TAU - PI / 2, rr = i % 2 ? s * .28 : s; g.lineTo(x + Math.cos(ang) * rr, y + Math.sin(ang) * rr); }
  g.closePath(); g.fill(); g.restore();
}
// altın lir (kaplumbağa kabuğu gövde, iki kıvrık kol, boyunduruk, teller)
function lyre(g, x, y, s, a) {
  g.save(); g.translate(x, y); g.rotate(a); g.scale(s, s); g.lineJoin = g.lineCap = 'round';
  const arms = () => { g.beginPath(); g.moveTo(-16, 8); g.bezierCurveTo(-36, -12, -32, -46, -18, -60); g.moveTo(16, 8); g.bezierCurveTo(36, -12, 32, -46, 18, -60); g.moveTo(-26, -52); g.lineTo(26, -52); };
  g.strokeStyle = '#7a4a12'; g.lineWidth = 11; arms(); g.stroke(); g.strokeStyle = '#f2c14e'; g.lineWidth = 6.5; arms(); g.stroke();
  g.strokeStyle = '#fff1bf'; g.lineWidth = 1.6; arms(); g.stroke();
  g.fillStyle = '#e9b23e'; g.strokeStyle = '#7a4a12'; g.lineWidth = 3.5; g.beginPath(); g.ellipse(0, 12, 23, 15, 0, 0, TAU); g.fill(); g.stroke();
  g.fillStyle = '#f7d77a'; g.beginPath(); g.ellipse(-4, 8, 12, 6, -.2, 0, TAU); g.fill();
  g.strokeStyle = '#fff5d6'; g.lineWidth = 1.4; for (let k = -2; k <= 2; k++) { g.beginPath(); g.moveTo(k * 4.6, -52); g.lineTo(k * 3.4, 8); g.stroke(); }
  g.restore();
}
// el: avuç + dört parmak + başparmak; ang yönüne uzanır
function hand(g, x, y, ang, s, skin, dark, o = {}) {
  g.save(); g.translate(x, y); g.rotate(ang); g.scale(s, s * (o.flip ? -1 : 1));
  g.lineCap = 'round'; g.fillStyle = skin; g.strokeStyle = skin;
  g.beginPath(); g.ellipse(20, 0, 24, 21, 0, 0, TAU); g.fill();
  const sp_ = o.spread ?? .12;
  [[-14, 36, -1.5], [-5, 41, -.5], [5, 40, .5], [14, 34, 1.5]].forEach(([oy, L, k]) => {
    g.lineWidth = 12.5; g.beginPath(); g.moveTo(34, oy * .8); g.lineTo(34 + Math.cos(k * sp_) * L, oy * .8 + Math.sin(k * sp_) * L); g.stroke();
  });
  g.lineWidth = 13; g.beginPath(); g.moveTo(16, -16); g.quadraticCurveTo(30, -34, 46, -36); g.stroke(); // başparmak
  g.strokeStyle = dark; g.lineWidth = 2.2; g.globalAlpha = .55;
  for (const oy of [-9.5, .2, 9.6]) { g.beginPath(); g.moveTo(44, oy * .8); g.lineTo(62, oy * .8 + oy * sp_ * .9); g.stroke(); }
  g.restore();
}
// kavrayan el: yerel y ekseni boyunca uzanan çubuğu sarar; bilek -x tarafında
function grip(g, x, y, ang, s, skin, dark) {
  g.save(); g.translate(x, y); g.rotate(ang); g.scale(s, s); g.lineCap = 'round';
  g.fillStyle = skin; g.beginPath(); g.ellipse(-12, 0, 19, 20, 0, 0, TAU); g.fill();
  for (let i = 0; i < 4; i++) { g.beginPath(); g.ellipse(7, -15 + i * 10, 12, 5.6, 0, 0, TAU); g.fill(); }
  g.strokeStyle = dark; g.lineWidth = 1.8; g.globalAlpha = .55;
  for (let i = 0; i < 3; i++) { g.beginPath(); g.moveTo(0, -10 + i * 10); g.lineTo(17, -10 + i * 10); g.stroke(); }
  g.globalAlpha = 1; g.strokeStyle = skin; g.lineWidth = 10; g.beginPath(); g.moveTo(-16, -14); g.quadraticCurveTo(-4, -26, 9, -25); g.stroke();
  g.restore();
}
// ¾ açılı baş: yüz +x yönüne dönük (dir -1 ile aynalanır), iki göz görünür. Birimler: saç tepesi -140, çene +108.
function head3q(g, cx, cy, s, dir, o) {
  g.save(); g.translate(cx, cy); g.rotate(o.tilt ?? 0); g.scale(s * dir * (o.narrow ?? 1), s); g.lineJoin = g.lineCap = 'round';
  const fem = !!o.fem;
  // arka saç kütlesi (yüzün arkasında)
  g.fillStyle = o.hair;
  if (fem) { g.beginPath(); g.arc(-92, -64, 46, 0, TAU); g.fill(); g.fill(path([[-100, 10], [-108, -50], [-80, -112], [-20, -138], [44, -130], [84, -96], [60, -70], [0, -84], [-60, -60], [-86, -10]])); }
  else {
    g.fill(path([[-104, 30], [-112, -40], [-92, -104], [-40, -140], [24, -142], [74, -116], [98, -76], [70, -64], [10, -76], [-56, -60], [-86, -10]]));
    for (const [x, y, rr] of [[-104, 18, 22], [-112, -20, 24], [-108, -60, 24], [-88, -100, 24], [-52, -128, 24], [-10, -140, 23], [32, -136, 22], [68, -114, 20], [92, -84, 18]]) { g.beginPath(); g.arc(x, y, rr, 0, TAU); g.fill(); }
  }
  // ten: yüz ovali (çene sağda, ¾ açı)
  const face = path(fem
    ? [[-80, -36], [-66, -84], [-18, -106], [34, -100], [68, -72], [82, -30], [84, 8], [78, 42], [62, 72], [36, 94], [8, 100], [-22, 92], [-50, 72], [-70, 40], [-82, 2]]
    : [[-82, -40], [-68, -88], [-20, -110], [36, -104], [72, -76], [88, -32], [92, 6], [88, 44], [74, 76], [48, 100], [16, 110], [-16, 102], [-46, 80], [-68, 46], [-82, 4]]);
  g.fillStyle = o.skin; g.fill(face);
  g.save(); g.clip(face);
  const sh = g.createLinearGradient(-90, 0, 40, 0); sh.addColorStop(0, rgba(o.skinDark, .75)); sh.addColorStop(1, rgba(o.skinDark, 0)); g.fillStyle = sh; g.fillRect(-120, -140, 240, 280); // uzak yanak gölgesi
  g.fillStyle = rgba(o.skinDark, .22); g.beginPath(); g.ellipse(-20, 104, 90, 20, 0, 0, TAU); g.fill();                      // çene altı (hafif)
  if (o.cool) { const cg = g.createLinearGradient(100, 0, 20, 0); cg.addColorStop(0, rgba(o.cool, .5)); cg.addColorStop(1, rgba(o.cool, 0)); g.fillStyle = cg; g.fillRect(-120, -140, 240, 280); }
  g.restore();
  // kulak (görünen yan)
  g.fillStyle = o.skin; g.beginPath(); g.ellipse(-82, 6, 14, 24, .1, 0, TAU); g.fill();
  g.strokeStyle = o.skinDark; g.lineWidth = 3; g.beginPath(); g.arc(-80, 6, 9, -1.4, 1.4); g.stroke();
  if (fem) { g.fillStyle = o.accent; g.beginPath(); g.arc(-80, 36, 7, 0, TAU); g.fill(); }
  // gözler: yakın (büyük) ve uzak (kısalmış); dehşette üst kapak yüksek, irisin üstünde beyaz görünür; bakış +x yönüne
  const eyes = [[-12, -16, 26, 18], [54, -16, 19, 15]];
  for (const [ex, ey, rx, ry] of eyes) {
    const open = o.eyeOpen ?? 1;
    // göz akı: kavisli üst kapak (ortası yüksek), yuvarlak alt kapak
    const eye = new Path2D(); eye.moveTo(ex - rx, ey + 3); eye.bezierCurveTo(ex - rx * .55, ey - ry * 1.25 * open, ex + rx * .55, ey - ry * 1.3 * open, ex + rx, ey - 1);
    eye.bezierCurveTo(ex + rx * .6, ey + ry * .95, ex - rx * .6, ey + ry * .95, ex - rx, ey + 3);
    g.fillStyle = '#ffffff'; g.fill(eye);
    const ix = ex + rx * .16 + (o.lookX ?? 0), iy = ey + 2 + (o.lookY ?? 2);
    g.save(); g.clip(eye); g.fillStyle = o.iris; g.beginPath(); g.arc(ix, iy, ry * .82, 0, TAU); g.fill();
    g.fillStyle = '#0b0705'; g.beginPath(); g.arc(ix, iy, ry * .4, 0, TAU); g.fill(); g.restore();
    g.fillStyle = '#ffffff'; g.beginPath(); g.arc(ix + ry * .28, iy - ry * .3, ry * .24, 0, TAU); g.fill(); g.beginPath(); g.arc(ix - ry * .3, iy + ry * .3, ry * .1, 0, TAU); g.fill();
    g.strokeStyle = o.line; g.lineWidth = fem ? 5 : 5.5; g.beginPath(); g.moveTo(ex - rx - 3, ey + 4); g.bezierCurveTo(ex - rx * .55, ey - ry * 1.3 * open, ex + rx * .55, ey - ry * 1.35 * open, ex + rx + 3, ey - 1); g.stroke();
    g.lineWidth = 2; g.globalAlpha = .5; g.beginPath(); g.moveTo(ex - rx * .6, ey + ry * .85); g.quadraticCurveTo(ex, ey + ry * 1.05, ex + rx * .6, ey + ry * .7); g.stroke(); g.globalAlpha = 1;
    if (fem) { g.lineWidth = 3; for (const k of [.2, .55, .85]) { const x = lerp(ex - rx, ex + rx, k), y = ey - ry * 1.4 * Math.sin(k * PI) * open + 2; g.beginPath(); g.moveTo(x, y); g.lineTo(x - 4, y - 7); g.stroke(); } }
  }
  // kaşlar: iç uçlar (burun köküne yakın) yüksek — keder / dehşet
  g.strokeStyle = o.brow; g.lineWidth = fem ? 6 : 9;
  const bi = o.browIn ?? 1;
  g.beginPath(); g.moveTo(-42, -36); g.quadraticCurveTo(-18, -44 - 6 * bi, 10, -48 - 12 * bi); g.stroke();
  g.beginPath(); g.moveTo(36, -50 - 10 * bi); g.quadraticCurveTo(56, -46 - 4 * bi, 74, -36); g.stroke();
  if (!fem) { g.strokeStyle = rgba(o.skinDark, .7); g.lineWidth = 3; g.beginPath(); g.moveTo(20, -58); g.lineTo(18, -46); g.moveTo(28, -58); g.lineTo(28, -48); g.stroke(); }
  // burun: köprü gölgesi, uç ve kanat
  // burun: kısa kama gölgesi + burun deliği (uzun çizgi yara gibi okunuyordu)
  { const k = fem ? .8 : 1; g.fillStyle = rgba(o.skinDark, .75); g.beginPath(); g.moveTo(30 * k, 2); g.quadraticCurveTo(44 * k, 18 * k, 50 * k, 30 * k); g.quadraticCurveTo(40 * k, 34 * k, 30 * k, 31 * k); g.quadraticCurveTo(34 * k, 18 * k, 30 * k, 2); g.fill();
    g.fillStyle = rgba(o.skinDark, 1); g.beginPath(); g.ellipse(40 * k, 32 * k, 5 * k, 3.2 * k, .3, 0, TAU); g.fill(); }
  // ağız: dehşette açık (nefesi kesilmiş), Evridiki'de adını söyler gibi aralık
  const mo = o.mouthOpen ?? .5, mx = fem ? 26 : 28, my = fem ? 62 : 68;
  const mw = fem ? 13 : 22, mh = (fem ? 6 : 6) + mo * (fem ? 8 : 11);
  g.fillStyle = o.mouthDark; g.beginPath(); g.moveTo(mx - mw, my - 2); g.quadraticCurveTo(mx, my - mh * 1.1, mx + mw, my - 4); g.quadraticCurveTo(mx + 2, my + mh * 1.3, mx - mw, my - 2); g.fill();
  if (!fem && mo > .4) { g.fillStyle = '#efe6d6'; g.beginPath(); g.moveTo(mx - mw * .7, my - mh * .55); g.quadraticCurveTo(mx, my - mh * .95, mx + mw * .7, my - mh * .6); g.lineTo(mx + mw * .6, my - mh * .35); g.quadraticCurveTo(mx, my - mh * .6, mx - mw * .6, my - mh * .3); g.fill(); }
  g.strokeStyle = o.lip; g.lineWidth = fem ? 6 : 6; g.beginPath(); g.moveTo(mx - mw * .8, my + mh * .5); g.quadraticCurveTo(mx, my + mh * 1.5, mx + mw * .8, my + mh * .4); g.stroke();
  // gözyaşları: iri, parlak
  if (o.tear) for (const [tx, ty, tl] of [[-2, 2, 44], [62, 2, 30]]) {
    g.strokeStyle = 'rgba(200,238,255,.9)'; g.lineWidth = 5; g.beginPath(); g.moveTo(tx, ty); g.quadraticCurveTo(tx + 4, ty + tl * .5, tx + 2, ty + tl); g.stroke();
    g.fillStyle = '#d9f4ff'; g.beginPath(); g.moveTo(tx + 2, ty + tl - 6); g.quadraticCurveTo(tx + 12, ty + tl + 10, tx + 2, ty + tl + 14); g.quadraticCurveTo(tx - 8, ty + tl + 10, tx + 2, ty + tl - 6); g.fill();
    g.fillStyle = '#ffffff'; g.beginPath(); g.arc(tx, ty + tl + 6, 2.6, 0, TAU); g.fill();
  }
  // ön saç ve taç
  g.fillStyle = o.hair;
  if (fem) {
    g.fill(path([[84, -72], [56, -92], [10, -96], [-40, -86], [-74, -60], [-86, -24], [-70, -40], [-30, -70], [20, -80], [62, -70]]));
    g.strokeStyle = o.accent; g.lineWidth = 8; g.beginPath(); g.moveTo(80, -84); g.quadraticCurveTo(0, -122, -88, -64); g.stroke();
    g.strokeStyle = o.hairLight; g.lineWidth = 3; for (const k of [0, 1, 2]) { g.beginPath(); g.moveTo(60 - k * 34, -92 + k * 4); g.quadraticCurveTo(30 - k * 34, -104, -10 - k * 30, -96 + k * 8); g.stroke(); }
  } else {
    for (const [x, y, rr] of [[-70, -64, 18], [-44, -76, 18], [-16, -82, 17], [14, -84, 17], [42, -80, 16], [66, -72, 15], [86, -60, 13], [-84, -36, 15]]) { g.beginPath(); g.arc(x, y, rr, 0, TAU); g.fill(); }
    g.strokeStyle = o.hairLight; g.lineWidth = 3.4; const r2 = rng(19);
    for (const [x, y, rr] of [[-100, -20, 12], [-96, -60, 13], [-76, -98, 13], [-40, -122, 12], [0, -130, 12], [40, -122, 11], [74, -100, 10], [-60, -70, 10], [-20, -86, 10], [20, -88, 10], [56, -80, 9]]) { g.beginPath(); g.arc(x, y, rr, PI * (1.05 + r2() * .3), PI * (1.7 + r2() * .3)); g.stroke(); }
    // altın defne tacı: alnın üstünden şakaklara
    const band = [[96, -64], [64, -92], [20, -108], [-24, -106], [-66, -90], [-98, -58]];
    g.strokeStyle = '#a8761c'; g.lineWidth = 6; g.beginPath(); sp(g, band, false); g.stroke();
    for (let i = 0; i < band.length - 1; i++) for (let k = 0; k < 3; k++) {
      const u = k / 3, x = lerp(band[i][0], band[i + 1][0], u), y = lerp(band[i][1], band[i + 1][1], u), a = Math.atan2(band[i + 1][1] - band[i][1], band[i + 1][0] - band[i][0]);
      for (const sd of [-1, 1]) { g.save(); g.translate(x, y); g.rotate(a + sd * .75 + PI); g.fillStyle = sd > 0 ? '#f6cf5a' : '#d9a12c'; g.beginPath(); g.ellipse(11, 0, 13, 5.4, 0, 0, TAU); g.fill(); g.restore(); }
    }
  }
  g.restore();
}
// uzuv: iki eklemli kalın kol (yuvarlak uçlu), sırayla daralır
function limb(g, pts, widths, col) { g.save(); g.lineCap = g.lineJoin = 'round'; g.strokeStyle = col;
  for (let i = 0; i < pts.length - 1; i++) { g.lineWidth = widths[i]; g.beginPath(); g.moveTo(...pts[i]); g.lineTo(...pts[i + 1]); g.stroke(); } g.restore(); }
// bir katmana kenar ışığı: şeklin kaydırılmış kopyası çıkarılınca kalan ince şerit renklenir
function rim(dst, src, dx, dy, col, a, blur = 3) {
  const [c, g] = layer(); g.drawImage(src, 0, 0); g.globalCompositeOperation = 'destination-out'; g.drawImage(src, dx, dy);
  g.globalCompositeOperation = 'source-in'; g.fillStyle = col; g.fillRect(0, 0, W, H);
  dst.save(); dst.globalCompositeOperation = 'lighter'; dst.globalAlpha = a; dst.filter = `blur(${blur}px)`; dst.drawImage(c, 0, 0); dst.filter = 'none'; dst.globalAlpha = a * .8; dst.drawImage(c, 0, 0); dst.restore();
}

// ——— sahne ———
// mağara ağzı: Orfeus'un sırtının hemen arkasında biter; uzanan kolu ışıktan karanlığa geçer
const OPEN = [[-80, -80], [600, -80], [800, 40], [890, 260], [920, 520], [900, 800], [840, 1160], [-80, 1160]];
const OPEN_P = path(OPEN);
function edgeX(y) { for (let i = 1; i < OPEN.length - 2; i++) { const a = OPEN[i], b = OPEN[i + 1]; if (y >= a[1] && y <= b[1]) return lerp(a[0], b[0], (y - a[1]) / (b[1] - a[1])); } return y < 0 ? 600 : 840; }
const GAP = [1150, 676];   // parmak uçları arasındaki boşluk: karenin odağı

function underworld(g) {
  const bg = g.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#161d48'); bg.addColorStop(.55, '#0f1435'); bg.addColorStop(1, '#080b20');
  g.fillStyle = bg; g.fillRect(0, 0, W, H);
  glow(g, 1720, 140, 640, '#4a2f86', .45);
  // videodaki gece bulutları: üst üste kâğıt katmanları; her alt kat bir öncekini örter (arada çıplak gök kalmaz), öne geldikçe koyulaşır
  puffs(g, 1000, 2000, 500, 44, 82, ['#1a2254', '#26306c', '#34428a'], '#8fa3ea', 3, { shadow: '#10153a', depth: 700, step: 18 });
  puffs(g, 1120, 2000, 650, 40, 74, ['#141a44', '#1d2659', '#283573'], '#6f86d6', 4, { shadow: '#0c1030', depth: 700, step: 16 });
  puffs(g, 1240, 2000, 800, 36, 66, ['#0f1436', '#161d48', '#1f2960'], '#5a6fc0', 5, { shadow: '#090c26', depth: 700, step: 14 });
  lowPoly(g, poly([[880, 960], [1200, 920], [1560, 950], [2000, 920], [2000, 1100], [880, 1100]]), 840, 880, 2000, 1100, 96, 21,
    (x, y, r) => mix('#0e1334', '#1f2860', r * .8 + (y < 970 ? .2 : 0)));
}
function dawnWorld(g) {
  g.save(); g.clip(OPEN_P);
  const sky = g.createLinearGradient(0, 0, 0, 900); sky.addColorStop(0, '#c4673f'); sky.addColorStop(.4, '#dc8450'); sky.addColorStop(.8, '#eea468'); sky.addColorStop(1, '#e48f55');
  g.fillStyle = sky; g.fillRect(-80, -80, 1100, 1300);
  // şafak güneşi solda, ufka yakın (hale değil); ışınlar oradan yayılır
  const sx = 250, sy = 400;
  glow(g, sx, sy, 400, '#ffd98a', .5);
  g.save(); g.globalAlpha = .1; g.fillStyle = '#fff4d0';
  for (let i = 0; i < 18; i++) { const a = i / 18 * TAU + .1, w = .07; g.beginPath(); g.moveTo(sx, sy); g.lineTo(sx + Math.cos(a - w) * 1400, sy + Math.sin(a - w) * 1400); g.lineTo(sx + Math.cos(a + w) * 1400, sy + Math.sin(a + w) * 1400); g.fill(); }
  g.restore();
  g.fillStyle = '#ffe9a6'; g.beginPath(); g.arc(sx, sy, 92, 0, TAU); g.fill(); g.strokeStyle = '#fff8e0'; g.lineWidth = 6; g.beginPath(); g.arc(sx, sy, 84, PI * 1.05, PI * 1.6); g.stroke();
  // videodaki gibi çok tonlu bulutlar: mavi-gri gölge, şeftali, açık şeftali, krem üst, beyaz kenar
  const T = ['#a88a9c', '#e3a079', '#f6cfa2', '#fff0d8'];
  puffs(g, -80, 330, 150, 36, 62, T, '#ffffff', 7, { depth: 30, step: 14 });
  puffs(g, 460, 900, 104, 40, 70, T, '#ffffff', 9, { depth: 30, step: 15 });
  puffs(g, -80, 170, 318, 30, 50, T, '#ffffff', 11, { depth: 26, step: 12, inset: 18 });
  { const tg = g.createLinearGradient(0, 0, 0, 260); tg.addColorStop(0, 'rgba(120,40,40,.2)'); tg.addColorStop(1, 'rgba(120,40,40,0)'); g.fillStyle = tg; g.fillRect(-80, -80, 1100, 340); }
  glow(g, 690, 430, 330, '#ffdca0', .3);   // başın arkasında yumuşak ışık (disk değil)
  // tepe ve kasaba (videodaki yeryüzü), yanında çamlar
  g.fillStyle = '#5f9a8c'; g.fill(path([[-80, 760], [120, 700], [360, 740], [640, 700], [900, 760], [900, 1200], [-80, 1200]]));
  const hill = path([[-80, 560], [40, 470], [150, 440], [270, 470], [350, 560], [420, 700], [-80, 760]]);
  g.fillStyle = '#7fae69'; g.fill(hill);
  g.save(); g.clip(hill); g.fillStyle = '#93bd74'; g.fill(path([[-80, 540], [40, 470], [150, 440], [120, 520], [40, 600], [-80, 640]])); g.restore();
  { const r = rng(5), hs = [];
    // evler yamaca dağınık: boşluklu, farklı boyda; tepede tapınak
    for (let y = 488; y <= 700; y += 27) for (let x = -50; x <= 380; x += 42) {
      const hx = x + (r() - .5) * 22, hy = y + (r() - .5) * 8, w = 30 + r() * 16, h = 22 + r() * 12;
      if (hx > 70 && hx < 210 && hy < 500) continue;
      if (g.isPointInPath(hill, hx, hy - 10) && g.isPointInPath(hill, hx + w, hy - 10) && g.isPointInPath(hill, hx + w / 2, hy + h + 6) && r() < .62) hs.push([hx, hy, w, h]);
    }
    for (const [x, y, w, h] of hs) {
      g.fillStyle = 'rgba(60,70,60,.25)'; g.fillRect(x + 4, y + 4, w, h);
      g.fillStyle = '#f3ead8'; g.fillRect(x, y, w, h); g.fillStyle = '#dccdb1'; g.fillRect(x + w * .62, y, w * .38, h);
      g.fillStyle = '#bf5236'; g.beginPath(); g.moveTo(x - 4, y + 1); g.lineTo(x + w * .5, y - h * .5); g.lineTo(x + w + 4, y + 1); g.fill();
      g.fillStyle = '#6f7d86'; g.fillRect(x + w * .25, y + h * .4, 7, 9); }
    g.fillStyle = '#f3ead8'; g.fillRect(96, 444, 90, 34); for (let k = 0; k < 6; k++) { g.fillStyle = '#dfd3bb'; g.fillRect(100 + k * 15, 452, 7, 26); } g.fillStyle = '#f3ead8'; g.beginPath(); g.moveTo(88, 446); g.lineTo(141, 420); g.lineTo(194, 446); g.fill(); }
  const pine = (x, y, h) => { for (let k = 0; k < 4; k++) { const w = h * (.34 - k * .06), yy = y - k * h * .22; g.fillStyle = k % 2 ? '#2f7f78' : '#3a8f86'; g.beginPath(); g.moveTo(x - w, yy); g.lineTo(x, yy - h * .42); g.lineTo(x + w, yy); g.fill(); } g.fillStyle = '#5b3a2a'; g.fillRect(x - 5, y, 10, h * .12); };
  pine(-10, 800, 220); pine(88, 830, 170);
  g.restore();
}
function caveRock(g) {
  // iri köşeli kaya yüzleri: ağız kenarında sıcak ışık, içeri doğru soğuk ve koyu; sağa doğru arka plana karışır
  const [rc, rg] = layer();
  const clip = new Path2D(); clip.rect(-100, -100, W + 200, H + 200); clip.addPath(OPEN_P);
  lowPoly(rg, clip, 520, -140, 1700, 1220, 112, 13, (x, y, r) => {
    const d = (x - edgeX(y)) / 460, warm = clamp(1 - d * 2.2);
    const base = mix(mix('#3d4588', '#20275d', r), '#121845', clamp(d * .8)), lit = mix('#e0915c', '#8f505c', r);
    return mix(base, lit, warm * (.45 + r * .55));
  });
  rg.globalCompositeOperation = 'destination-in'; const fade = rg.createLinearGradient(1250, 0, 1650, 0); fade.addColorStop(0, 'rgba(0,0,0,1)'); fade.addColorStop(1, 'rgba(0,0,0,0)');
  rg.fillStyle = fade; rg.fillRect(-100, -100, W + 200, H + 200);
  g.drawImage(rc, 0, 0);
  g.save(); g.globalCompositeOperation = 'lighter'; for (let y = 0; y < H; y += 60) glow(g, edgeX(y) + 30, y, 150, '#ff9a55', .1); g.restore();
}
// kâğıt katman gölgesi: figür bir kat yukarıda duruyormuş gibi alta yumuşak koyu gölge
function paperShadow(dst, src, dx, dy, a) { dst.save(); dst.filter = `blur(10px) brightness(0)`; dst.globalAlpha = a; dst.drawImage(src, dx, dy); dst.restore(); }
function orpheus() {
  const [c, g] = layer();
  const SK = '#a8653f', SKD = '#6e3923', CH = '#e3d3b4', CA = '#5e1c22', CA2 = '#7c2a2d';
  // gövde çıkışa (sola) dönük, sırtı bize yarım dönük; baş omzunun üstünden geriye, Evridiki'ye bakar
  // uzak kol: öne (sola) uzanır, lir elinde — gövdenin arkasında kalır
  limb(g, [[480, 800], [392, 846], [306, 852]], [58, 48], SK);
  lyre(g, 236, 868, 2.6, -.5);
  grip(g, 280, 846, PI + .1, 1.5, SK, SKD);
  // kiton: yalnız göğüs önü (ışık tarafı) görünür; gövde çıkışa doğru eğik
  const torso = path([[436, 776], [520, 738], [650, 714], [790, 716], [850, 760], [872, 860], [862, 980], [880, 1100], [418, 1100], [398, 980], [406, 860]]);
  g.fillStyle = CH; g.fill(torso);
  g.save(); g.clip(torso); g.strokeStyle = '#c9b48e'; g.lineWidth = 7; g.lineCap = 'round';
  for (const x0 of [414, 442]) { g.beginPath(); g.moveTo(x0, 800); g.quadraticCurveTo(x0 - 18, 950, x0 - 6, 1100); g.stroke(); }
  g.restore();
  // pelerin: sırtı örter; yürüyüşün gerisinde sağa savrulur, ucunda açık astar görünür
  const cape = path([[466, 766], [560, 730], [668, 714], [790, 716], [846, 750], [882, 830], [904, 920], [960, 994], [1056, 1052], [1120, 1100], [478, 1100], [466, 1000], [476, 880]]);
  g.fillStyle = CA; g.fill(cape);
  g.save(); g.clip(cape);
  const cl = g.createLinearGradient(466, 0, 740, 0); cl.addColorStop(0, rgba(CA2, 1)); cl.addColorStop(1, rgba(CA2, 0)); g.fillStyle = cl; g.fillRect(0, 0, W, H);
  g.fillStyle = '#b4584a'; g.fill(path([[900, 960], [962, 1010], [1056, 1056], [1120, 1100], [1010, 1100], [944, 1046], [906, 994]]));   // savrulan ucun astarı
  g.lineCap = 'round';
  g.strokeStyle = '#3a0f14'; g.lineWidth = 10; g.beginPath(); g.moveTo(700, 730); g.bezierCurveTo(740, 820, 736, 960, 716, 1100); g.stroke();   // sırt çizgisi
  for (const [x0, x1, c_] of [[560, 520, '#3f1116'], [620, 610, '#8d3434'], [790, 880, '#8d3434'], [826, 990, '#3f1116']]) {
    g.strokeStyle = c_; g.lineWidth = 8; g.beginPath(); g.moveTo(x0, 770); g.quadraticCurveTo((x0 + x1) / 2 + 24, 930, x1, 1100); g.stroke(); }
  g.strokeStyle = '#a24a3e'; g.lineWidth = 6; g.beginPath(); g.moveTo(472, 774); g.quadraticCurveTo(620, 724, 790, 720); g.stroke();   // omuz kıvrımında ışık
  g.strokeStyle = 'rgba(255,190,150,.35)'; g.lineWidth = 14; g.beginPath(); g.moveTo(770, 760); g.quadraticCurveTo(840, 790, 860, 880); g.stroke();   // kürek kemiği çıkıntısı
  g.restore();
  // omuz tokası
  g.fillStyle = '#d9a43a'; g.beginPath(); g.arc(782, 726, 17, 0, TAU); g.fill(); g.fillStyle = '#f6d77a'; g.beginPath(); g.arc(777, 721, 7, 0, TAU); g.fill();
  // geriye, ona uzanan kol: pelerinin altından çıkar; açık avuç, yayılmış parmaklar
  g.fillStyle = CH; g.beginPath(); g.ellipse(822, 732, 46, 38, .2, 0, TAU); g.fill();
  limb(g, [[818, 734], [910, 716], [1004, 690]], [66, 56], SK);
  g.fillStyle = CH; g.beginPath(); g.ellipse(818, 730, 44, 36, .2, -.9, 2.2); g.fill();
  g.strokeStyle = '#d9a43a'; g.lineWidth = 6; g.beginPath(); g.ellipse(818, 730, 44, 36, .2, -.6, 1.4); g.stroke();
  hand(g, 1000, 690, -.08, 1.42, SK, SKD, { spread: .36 });
  // boyun: ince, dönmüş (göğüs-kulak kası çizgisi); çenenin gölgesi boyna düşer
  const neck = path([[640, 596], [732, 594], [746, 650], [758, 714], [630, 720], [634, 660]]);
  g.fillStyle = SK; g.fill(neck);
  g.save(); g.clip(neck); const ns = g.createLinearGradient(0, 596, 0, 668); ns.addColorStop(0, rgba(SKD, .85)); ns.addColorStop(1, rgba(SKD, 0)); g.fillStyle = ns; g.fillRect(0, 0, W, H);
  g.strokeStyle = rgba(SKD, .7); g.lineWidth = 4; g.beginPath(); g.moveTo(660, 620); g.quadraticCurveTo(694, 670, 734, 712); g.stroke(); g.restore();
  g.fillStyle = CA; g.fill(path([[596, 730], [612, 676], [646, 650], [672, 676], [690, 724]]));
  g.strokeStyle = '#a24a3e'; g.lineWidth = 5; g.beginPath(); g.moveTo(604, 704); g.quadraticCurveTo(618, 668, 648, 654); g.stroke();
  head3q(g, 684, 440, 1.78, 1, { narrow: .91, skin: SK, skinDark: SKD, cool: '#7fd0ff', hair: '#1e130d', hairLight: '#6b4532', iris: '#3a2416', line: '#1a0f09', brow: '#150c07', lip: '#6e2a1f', mouthDark: '#2a0d08', tear: true, mouthOpen: .8, browIn: 1.25, lookX: 6, lookY: 1, tilt: .07 });
  // ışık: soldan şafak (sıcak kenar), sağdan hayaletin soğuk mavisi; alt kısım koyulaşır (odak yüz ve eller)
  const [o, og] = layer(); paperShadow(og, c, 14, 18, .45); og.drawImage(c, 0, 0);
  og.globalCompositeOperation = 'source-atop';
  const cool = og.createLinearGradient(1160, 0, 780, 0); cool.addColorStop(0, 'rgba(120,200,255,.38)'); cool.addColorStop(1, 'rgba(120,200,255,0)'); og.fillStyle = cool; og.fillRect(0, 0, W, H);
  const shade = og.createLinearGradient(0, 740, 0, 1080); shade.addColorStop(0, 'rgba(20,16,50,0)'); shade.addColorStop(1, 'rgba(20,16,50,.6)'); og.fillStyle = shade; og.fillRect(0, 0, W, H);
  og.globalCompositeOperation = 'source-over';
  rim(og, c, 10, 0, '#ffd28a', .7, 2.5);
  rim(og, c, -7, 2, '#8fe3ff', .55, 3);
  return o;
}
const EV = { dy: 40, flakes: [] };
function eurydice() {
  const [c, g] = layer();
  const SK = '#dff4ff', SKD = '#7fb0d8', DR = '#bfe6fb', dy = EV.dy;
  g.save(); g.translate(0, dy);
  g.fillStyle = SK; g.fill(path([[1410, 740], [1500, 744], [1516, 830], [1400, 834]])); // boyun
  const body = path([[1360, 830], [1460, 812], [1560, 830], [1620, 920], [1650, 1040], [1670, 1140], [1330, 1140], [1340, 1010], [1338, 900]]);
  g.fillStyle = DR; g.fill(body);
  g.save(); g.clip(body); g.strokeStyle = '#8fc6ea'; g.lineWidth = 7; g.lineCap = 'round';
  for (const x of [1390, 1450, 1510, 1570]) { g.beginPath(); g.moveTo(x, 850); g.quadraticCurveTo(x + 14, 990, x + 26, 1140); g.stroke(); }
  g.restore();
  g.restore();
  // ona uzanan kol: omuz aşağıda, el yerinde (parmak uçları arası boşluk sabit)
  limb(g, [[1400, 900], [1326, 826], [1284, 716]], [54, 44], SK);
  g.fillStyle = DR; g.fill(path([[1430, 870], [1380, 860], [1326, 826], [1308, 866], [1360, 916], [1420, 934]]));
  hand(g, 1286, 712, PI + .45, 1.3, SK, SKD, { spread: .3, flip: true });
  head3q(g, 1470, 618 + dy, 1.32, -1, { fem: true, skin: SK, skinDark: SKD, hair: '#4f7fb8', hairLight: '#bfe0ff', iris: '#163f74', line: '#0f2a5a', brow: '#102c5e', lip: '#2c5594', mouthDark: '#14336a', accent: '#ffd36a', mouthOpen: .55, browIn: 1.1, lookX: 0, lookY: 1 });
  // dağılma: etek ve sağ kenar keskin kenarlı kâğıt pullarına ayrılır (sağa-yukarı, karanlığa doğru savrulur)
  g.globalCompositeOperation = 'destination-in';
  const m = g.createLinearGradient(0, 900, 0, 1100); m.addColorStop(0, 'rgba(0,0,0,1)'); m.addColorStop(1, 'rgba(0,0,0,.08)'); g.fillStyle = m; g.fillRect(0, 0, W, H);
  g.globalCompositeOperation = 'destination-out';
  const r = rng(44), flake = (x, y, s_, a) => { const p = []; for (let k = 0; k < 4; k++) { const t = a + k * TAU / 4 + (r() - .5) * .9, rr = s_ * (.6 + r() * .6); p.push([x + Math.cos(t) * rr, y + Math.sin(t) * rr]); } return poly(p); };
  for (let i = 0; i < 260; i++) {
    const x = 1520 + r() * 190, y = 780 + r() * 360, k = clamp((x - 1545) / 130) * clamp((y - 800) / 240 + .4);
    if (r() < k) { const s_ = 10 + r() * 16, a = r() * TAU; g.fill(flake(x, y, s_, a)); if (r() < .7) EV.flakes.push([x, y, s_, a]); }
  }
  g.globalCompositeOperation = 'source-over';
  return c;
}

function draw(v) {
  underworld(ctx); dawnWorld(ctx); caveRock(ctx);
  // Evridiki: hayalet ışıması, zerre akışı (sağa ve geriye, karanlığa doğru uzayan çizgiler)
  glow(ctx, 1470, 760, 540, '#62c8ff', .3);
  const ev = eurydice();
  paperShadow(ctx, ev, 12, 16, .35);
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.filter = 'blur(20px)'; ctx.globalAlpha = .45; ctx.drawImage(ev, 0, 0); ctx.restore();
  ctx.drawImage(ev, 0, 0);
  { const r = rng(71), pal = ['#ffffff', '#e2f6ff', '#bde6ff'];
    // kopan pullar: kesildikleri yerden sağa-yukarı savrulur, uzaklaştıkça küçülür ve seyrelir
    const [fc, fg] = layer();
    for (const [x0, y0, s0, a0] of EV.flakes) {
      const t = Math.pow(r(), .8), dx = 60 + t * 330, x = x0 + dx, y = y0 - dx * (.42 + r() * .3) + (r() - .5) * 40, s_ = s0 * (1 - t * .7);
      if (x > 1900 || r() < t * .55) continue;
      const p = []; for (let k = 0; k < 4; k++) { const ang = a0 + t * 3 + k * TAU / 4 + (r() - .5) * .9, rr = s_ * (.6 + r() * .6); p.push([x + Math.cos(ang) * rr, y + Math.sin(ang) * rr]); }
      fg.globalAlpha = 1 - t * .5; fg.fillStyle = pal[(r() * 3) | 0]; fg.fill(poly(p)); fg.globalAlpha = .6 - t * .3; fg.strokeStyle = '#ffffff'; fg.lineWidth = 2; fg.stroke(poly(p));
    }
    ctx.save(); ctx.filter = 'blur(12px)'; ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = .8; ctx.drawImage(fc, 0, 0); ctx.restore();
    ctx.drawImage(fc, 0, 0);
    // yuvarlak yumuşak zerreler ve videodaki altın ateş böcekleri
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 46; i++) { const t = r(), x = 1580 + t * 300 + (r() - .5) * 80, y = 880 + r() * 200 - t * 300, rr = 2 + (1 - t) * 4;
      glow(ctx, x, y, rr * 4, '#c8f0ff', .35 * (1 - t * .6)); ctx.fillStyle = `rgba(225,248,255,${.8 - t * .5})`; ctx.beginPath(); ctx.arc(x, y, rr, 0, TAU); ctx.fill(); }
    for (let i = 0; i < 26; i++) { const x = 1240 + r() * 660, y = 480 + r() * 560; if (x > 1330 && x < 1560 && y < 760) continue; const rr = 2.5 + r() * 3;
      glow(ctx, x, y, rr * 6, '#ffcf6a', .45); ctx.fillStyle = '#fff1bf'; ctx.beginPath(); ctx.arc(x, y, rr, 0, TAU); ctx.fill(); }
    ctx.restore(); }
  { const r = rng(12); for (let i = 0; i < 8; i++) sparkle(ctx, 960 + r() * 260, 520 + r() * 420, 4 + r() * 5, '#ffd36a', .45 + r() * .4); }
  const orf = orpheus(); ctx.drawImage(orf, 0, 0);
  // parmak uçları arasındaki kıvılcım: karedeki en parlak nokta
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, GAP[0], GAP[1], 280, '#ffe2a0', .45); glow(ctx, GAP[0], GAP[1], 150, '#fff0c8', .3); ctx.restore();
  sparkle(ctx, GAP[0], GAP[1], 42, '#fff0c4', 1);
  // kâğıt dokusu (videodaki gibi belirgin) + odağa (yüz ve eller) merkezli kenar kararması
  const [n, ng] = layer(); const id = ng.createImageData(W, H), d = id.data, r = rng(3);
  for (let i = 0; i < d.length; i += 4) { const v_ = 128 + (r() - .5) * 80; d[i] = d[i + 1] = d[i + 2] = v_; d[i + 3] = 255; }
  ng.putImageData(id, 0, 0);
  ctx.save(); ctx.globalCompositeOperation = 'soft-light'; ctx.globalAlpha = .45; ctx.drawImage(n, 0, 0); ctx.restore();
  const vg = ctx.createRadialGradient(980, 580, H * .45, 980, 580, H * 1.2); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,12,.55)');
  ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  // yazı (dokunun üstünde, keskin)
  if (!Q.has('notext')) {
    const T = { a: ['ARKANA', 'BAKMA!'], b: ['NEDEN', 'BAKTI?'] }[v] || ['ARKANA', 'BAKMA!'];
    const font = Q.get('font') || 'Anton';
    const f1 = +(Q.get('f1') || 168), f2 = +(Q.get('f2') || 246), x = 1872, y1 = 26 + f1 * .86, y2 = y1 + 16 + f2 * .86;
    ctx.save(); ctx.textBaseline = 'alphabetic'; ctx.lineJoin = 'round';
    const fnt = f => `${font === 'Anton' ? '' : '900 '}${f}px ${font}`, wd = (s, f) => { ctx.font = fnt(f); return ctx.measureText(s).width; };
    const left = false, lx = x - Math.max(wd(T[0], f1), wd(T[1], f2));
    ctx.textAlign = left ? 'left' : 'right';
    for (const [s, y, f, fill] of [[T[0], y1, f1, '#ffffff'], [T[1], y2, f2, '#ffcf3a']]) {
      ctx.font = fnt(f); const xx = left ? lx : x;
      ctx.shadowColor = 'rgba(5,6,25,.9)'; ctx.shadowBlur = 28; ctx.shadowOffsetY = 8;
      ctx.lineWidth = f * .14; ctx.strokeStyle = '#0a0d28'; ctx.strokeText(s, xx, y);
      ctx.shadowColor = 'transparent'; ctx.fillStyle = fill; ctx.fillText(s, xx, y);
    }
    ctx.restore();
  }
}
window.ready = (async () => {
  for (const f of ['150px Anton', '900 150px Cinzel']) await document.fonts.load(f, 'ARKANABAKMAĞİŞÖÜÇ!?');
  draw(Q.get('v') || 'a');
  return true;
})();
