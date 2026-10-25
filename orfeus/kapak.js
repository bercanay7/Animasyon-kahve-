// Orfeus ve Evridiki — YouTube kapağı (1920×1080 çizilir, 1280×720 dışa aktarılır)
// Üslup videoyla aynı: katmanlı kâğıt kesme / düz vektör, dalgalı ve kenarı açık çizgili bulutlar, köşeli (low-poly) kayalar, ateş böceği kıvılcımları, dokulu yüzey.
// Kanca: yeryüzüne çıkışın eşiğinde Orfeus geri döner; Evridiki parmak uçları değmeden ışık zerrelerine dönüşür.
// Kullanım: kapak.html?v=a|b|c  (yazı seçenekleri)  &notext=1
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
// ¾ açılı baş: yüz +x yönüne dönük (dir -1 ile aynalanır), iki göz görünür. Birimler: saç tepesi -140, çene +108.
function head3q(g, cx, cy, s, dir, o) {
  g.save(); g.translate(cx, cy); g.scale(s * dir, s); g.lineJoin = g.lineCap = 'round';
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
  g.fillStyle = rgba(o.skinDark, .5); g.beginPath(); g.ellipse(-20, 96, 90, 26, 0, 0, TAU); g.fill();                      // çene altı
  if (o.cool) { const cg = g.createLinearGradient(100, 0, 20, 0); cg.addColorStop(0, rgba(o.cool, .5)); cg.addColorStop(1, rgba(o.cool, 0)); g.fillStyle = cg; g.fillRect(-120, -140, 240, 280); }
  g.restore();
  // kulak (görünen yan)
  g.fillStyle = o.skin; g.beginPath(); g.ellipse(-82, 6, 14, 24, .1, 0, TAU); g.fill();
  g.strokeStyle = o.skinDark; g.lineWidth = 3; g.beginPath(); g.arc(-80, 6, 9, -1.4, 1.4); g.stroke();
  if (fem) { g.fillStyle = o.accent; g.beginPath(); g.arc(-80, 36, 7, 0, TAU); g.fill(); }
  // gözler: yakın (büyük) ve uzak (kısalmış); dehşette üst kapak yüksek, irisin üstünde beyaz görünür; bakış +x yönüne
  const eyes = [[-12, -16, 25, 15], [54, -16, 18, 13]];
  for (const [ex, ey, rx, ry] of eyes) {
    const open = o.eyeOpen ?? 1;
    g.fillStyle = '#ffffff'; g.beginPath(); g.moveTo(ex - rx, ey + 2); g.quadraticCurveTo(ex - rx * .2, ey - ry * 1.5 * open, ex + rx, ey - 2); g.quadraticCurveTo(ex, ey + ry * 1.1, ex - rx, ey + 2); g.fill();
    g.save(); g.clip(); g.fillStyle = o.iris; g.beginPath(); g.arc(ex + rx * .38 + (o.lookX ?? 0), ey + (o.lookY ?? 3), ry * .72, 0, TAU); g.fill();
    g.fillStyle = '#0b0705'; g.beginPath(); g.arc(ex + rx * .38 + (o.lookX ?? 0), ey + (o.lookY ?? 3), ry * .34, 0, TAU); g.fill(); g.restore();
    g.fillStyle = '#ffffff'; g.beginPath(); g.arc(ex + rx * .5 + (o.lookX ?? 0), ey - 2 + (o.lookY ?? 3) - 1, ry * .2, 0, TAU); g.fill();
    g.strokeStyle = o.line; g.lineWidth = fem ? 4.5 : 5; g.beginPath(); g.moveTo(ex - rx - 2, ey + 3); g.quadraticCurveTo(ex - rx * .2, ey - ry * 1.55 * open, ex + rx + 2, ey - 2); g.stroke();
    if (fem) { g.lineWidth = 3; for (const k of [.2, .55, .85]) { const x = lerp(ex - rx, ex + rx, k), y = ey - ry * 1.4 * Math.sin(k * PI) * open + 2; g.beginPath(); g.moveTo(x, y); g.lineTo(x - 4, y - 7); g.stroke(); } }
  }
  // kaşlar: iç uçlar (burun köküne yakın) yüksek — keder / dehşet
  g.strokeStyle = o.brow; g.lineWidth = fem ? 6 : 9;
  const bi = o.browIn ?? 1;
  g.beginPath(); g.moveTo(-42, -36); g.quadraticCurveTo(-18, -44 - 6 * bi, 10, -48 - 12 * bi); g.stroke();
  g.beginPath(); g.moveTo(36, -50 - 10 * bi); g.quadraticCurveTo(56, -46 - 4 * bi, 74, -36); g.stroke();
  if (!fem) { g.strokeStyle = rgba(o.skinDark, .9); g.lineWidth = 3.5; g.beginPath(); g.moveTo(20, -58); g.lineTo(18, -44); g.moveTo(28, -58); g.lineTo(28, -46);
    g.moveTo(-10, -72); g.quadraticCurveTo(14, -78, 40, -72); g.moveTo(-4, -84); g.quadraticCurveTo(16, -88, 36, -84); g.stroke(); }
  // burun: köprü gölgesi, uç ve kanat
  g.strokeStyle = o.skinDark; g.lineWidth = fem ? 4 : 5; g.beginPath(); g.moveTo(22, -10); g.quadraticCurveTo(30, 18, fem ? 46 : 52, fem ? 26 : 30); g.stroke();
  g.fillStyle = rgba(o.skinDark, .9); g.beginPath(); g.ellipse(fem ? 40 : 44, fem ? 32 : 36, fem ? 5 : 7, fem ? 3.5 : 4.5, .3, 0, TAU); g.fill();
  // ağız: dehşette açık (nefesi kesilmiş), Evridiki'de adını söyler gibi aralık
  const mo = o.mouthOpen ?? .5, mx = fem ? 26 : 28, my = fem ? 62 : 68;
  const mw = fem ? 13 : 22, mh = (fem ? 6 : 6) + mo * (fem ? 8 : 11);
  g.fillStyle = o.mouthDark; g.beginPath(); g.moveTo(mx - mw, my - 2); g.quadraticCurveTo(mx, my - mh * 1.1, mx + mw, my - 4); g.quadraticCurveTo(mx + 2, my + mh * 1.3, mx - mw, my - 2); g.fill();
  if (!fem && mo > .4) { g.fillStyle = '#efe6d6'; g.beginPath(); g.moveTo(mx - mw * .7, my - mh * .55); g.quadraticCurveTo(mx, my - mh * .95, mx + mw * .7, my - mh * .6); g.lineTo(mx + mw * .6, my - mh * .35); g.quadraticCurveTo(mx, my - mh * .6, mx - mw * .6, my - mh * .3); g.fill(); }
  g.strokeStyle = o.lip; g.lineWidth = fem ? 6 : 6; g.beginPath(); g.moveTo(mx - mw * .8, my + mh * .5); g.quadraticCurveTo(mx, my + mh * 1.5, mx + mw * .8, my + mh * .4); g.stroke();
  if (!fem) { g.strokeStyle = rgba(o.skinDark, .8); g.lineWidth = 3; g.beginPath(); g.moveTo(mx - mw - 6, my - 14); g.quadraticCurveTo(mx - mw - 10, my + 2, mx - mw - 2, my + 12); g.stroke(); } // gülme çizgisi değil: gerilmiş yanak
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
  // videodaki gece bulutları: kalın kâğıt şeritler, mavi-gri gölge katmanı, açık kenar çizgisi
  cloudBank(g, 1000, 2000, 470, 46, 88, '#1f285e', '#5d73c4', 3, { shadow: '#121838', sh: 16, depth: 50, rw: 4 });
  cloudBank(g, 1180, 2000, 560, 38, 70, '#19214f', '#4a5fae', 4, { shadow: '#0f1430', sh: 14, depth: 40, rw: 3.5 });
  lowPoly(g, poly([[880, 960], [1200, 920], [1560, 950], [2000, 920], [2000, 1100], [880, 1100]]), 840, 880, 2000, 1100, 96, 21,
    (x, y, r) => mix('#151c44', '#2a3570', r * .8 + (y < 970 ? .2 : 0)));
}
function dawnWorld(g) {
  g.save(); g.clip(OPEN_P);
  const sky = g.createLinearGradient(0, 0, 0, 900); sky.addColorStop(0, '#cf7146'); sky.addColorStop(.4, '#e08a52'); sky.addColorStop(.8, '#eea468'); sky.addColorStop(1, '#e48f55');
  g.fillStyle = sky; g.fillRect(-80, -80, 1100, 1300);
  // güneş Orfeus'un başının arkasında: hale ve ışınlar
  const sx = 600, sy = 420;
  glow(g, sx, sy, 440, '#ffe2a8', .5);
  g.save(); g.globalAlpha = .12; g.fillStyle = '#fff4d0';
  for (let i = 0; i < 20; i++) { const a = i / 20 * TAU + .05, w = .06; g.beginPath(); g.moveTo(sx, sy); g.lineTo(sx + Math.cos(a - w) * 1400, sy + Math.sin(a - w) * 1400); g.lineTo(sx + Math.cos(a + w) * 1400, sy + Math.sin(a + w) * 1400); g.fill(); }
  g.restore();
  // videodaki gibi ayrı ayrı kalın kâğıt bulut şeritleri: açık krem dolgu, altında koyu kızıl gölge katmanı, üstte ışık kenarı
  for (const [x0, x1, y, r0, r1, sd] of [[-80, 250, 120, 40, 70, 7], [420, 900, 84, 44, 76, 9], [-80, 170, 300, 36, 60, 8], [230, 470, 236, 32, 54, 11]])
    cloudBank(g, x0, x1, y, r0, r1, '#ffe7c2', '#fff8ea', sd, { shadow: '#c87a5c', sh: 14, depth: 40, rw: 5, rin: 7 });
  g.fillStyle = '#fff1d2'; g.beginPath(); g.arc(sx, sy, 250, 0, TAU); g.fill();
  g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 6; g.beginPath(); g.arc(sx, sy, 236, PI * 1.05, PI * 1.6); g.stroke();
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
  pine(330, 720, 210); pine(392, 760, 170); pine(-20, 760, 190);
  glow(g, sx, sy, 900, '#ffd38f', .15);
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
  const SK = '#a8653f', SKD = '#6e3923';
  // pelerin: koyu bordo, yürüyüşün gerisinde (sağa) dalgalanır; kolun altında kalır
  g.fillStyle = '#5e1c20'; g.fill(path([[770, 690], [860, 700], [960, 780], [1050, 900], [1110, 1040], [1080, 1140], [880, 1140], [900, 980], [880, 840], [820, 760]]));
  g.fillStyle = '#7a2428'; g.fill(path([[790, 700], [860, 712], [930, 790], [990, 900], [1020, 1040], [960, 1140], [900, 1140], [910, 990], [880, 840]]));
  // gövde: sola (çıkışa) eğik, kiton; öne giden kol lir taşır
  const body = path([[420, 720], [520, 690], [650, 684], [800, 700], [870, 770], [910, 920], [940, 1140], [380, 1140], [370, 960], [380, 820]]);
  g.fillStyle = '#e3d3b4'; g.fill(body);
  g.save(); g.clip(body); g.strokeStyle = '#c9b48e'; g.lineWidth = 8; g.lineCap = 'round';
  for (const [x0, x1] of [[470, 400], [560, 500], [660, 620], [760, 740], [830, 840]]) { g.beginPath(); g.moveTo(x0, 730); g.quadraticCurveTo((x0 + x1) / 2 - 16, 920, x1, 1140); g.stroke(); }
  g.strokeStyle = '#d9a43a'; g.lineWidth = 10; g.beginPath(); g.moveTo(520, 700); g.quadraticCurveTo(640, 734, 780, 704); g.stroke(); // altın yaka
  g.strokeStyle = '#6b4226'; g.lineWidth = 9; g.beginPath(); g.moveTo(800, 704); g.lineTo(470, 960); g.stroke(); // lir kayışı
  g.restore();
  g.fillStyle = SK; g.fill(path([[540, 600], [680, 604], [700, 700], [520, 704]])); // boyun (baş üstüne gelir)
  // öne uzanan kol: lir elinde, güneşe karşı
  limb(g, [[460, 740], [400, 850], [430, 930]], [62, 52], SK);
  lyre(g, 400, 930, 3.0, -.25);
  g.fillStyle = SK; g.beginPath(); g.ellipse(430, 934, 30, 24, .3, 0, TAU); g.fill();
  // geriye, ona uzanan kol: açık avuç, yayılmış parmaklar
  limb(g, [[800, 730], [910, 716], [1004, 690]], [70, 58], SK);
  g.fillStyle = '#e3d3b4'; g.beginPath(); g.ellipse(806, 728, 52, 42, .2, 0, TAU); g.fill();
  g.strokeStyle = '#d9a43a'; g.lineWidth = 7; g.beginPath(); g.ellipse(806, 728, 52, 42, .2, -.3, 1.5); g.stroke();
  hand(g, 1000, 690, -.08, 1.42, SK, SKD, { spread: .36 });
  head3q(g, 610, 440, 1.78, 1, { skin: SK, skinDark: SKD, cool: '#7fd0ff', hair: '#1e130d', hairLight: '#6b4532', iris: '#3a2416', line: '#1a0f09', brow: '#150c07', lip: '#6e2a1f', mouthDark: '#2a0d08', tear: true, mouthOpen: .8, browIn: 1.25, lookX: 3 });
  // ışık: arkadan güneş (sol kenar ışığı), önden hayaletin soğuk mavisi; hafif mat (videodaki gibi parlak değil)
  const [o, og] = layer(); paperShadow(og, c, 14, 18, .45); og.drawImage(c, 0, 0);
  og.globalCompositeOperation = 'source-atop';
  const cool = og.createLinearGradient(1160, 0, 780, 0); cool.addColorStop(0, 'rgba(120,200,255,.38)'); cool.addColorStop(1, 'rgba(120,200,255,0)'); og.fillStyle = cool; og.fillRect(0, 0, W, H);
  const shade = og.createLinearGradient(0, 760, 0, 1080); shade.addColorStop(0, 'rgba(20,16,50,0)'); shade.addColorStop(1, 'rgba(20,16,50,.55)'); og.fillStyle = shade; og.fillRect(0, 0, W, H);
  og.globalCompositeOperation = 'source-over';
  rim(og, c, 10, 0, '#ffd28a', .7, 2.5);
  rim(og, c, -7, 2, '#8fe3ff', .55, 3);
  return o;
}
function eurydice() {
  const [c, g] = layer();
  const SK = '#dff4ff', SKD = '#86b8dc', DR = '#bfe6fb';
  g.fillStyle = SK; g.fill(path([[1410, 740], [1500, 744], [1516, 830], [1400, 834]])); // boyun
  const body = path([[1360, 830], [1460, 812], [1560, 830], [1620, 920], [1650, 1040], [1670, 1140], [1330, 1140], [1340, 1010], [1338, 900]]);
  g.fillStyle = DR; g.fill(body);
  g.save(); g.clip(body); g.strokeStyle = '#8fc6ea'; g.lineWidth = 7; g.lineCap = 'round';
  for (const x of [1390, 1450, 1510, 1570]) { g.beginPath(); g.moveTo(x, 850); g.quadraticCurveTo(x + 14, 990, x + 26, 1140); g.stroke(); }
  g.restore();
  // ona uzanan kol: dökümlü yen omuzdan dirseğe
  limb(g, [[1400, 860], [1330, 800], [1284, 716]], [54, 44], SK);
  g.fillStyle = DR; g.fill(path([[1430, 830], [1380, 820], [1330, 790], [1310, 830], [1360, 880], [1420, 896]]));
  hand(g, 1286, 712, PI + .45, 1.3, SK, SKD, { spread: .3, flip: true });
  head3q(g, 1470, 618, 1.32, -1, { fem: true, skin: SK, skinDark: SKD, hair: '#86b9e0', hairLight: '#d9f2ff', iris: '#1d4f86', line: '#1f4a80', brow: '#2a5a94', lip: '#5f8fca', mouthDark: '#2f5a92', accent: '#ffd36a', mouthOpen: .55, browIn: 1.1, lookX: 2, lookY: 2 });
  // dağılma: alt ve arka kısım ışık zerrelerine dönüşür (yeraltına doğru çekiliyor)
  g.globalCompositeOperation = 'destination-in';
  const m = g.createLinearGradient(0, 860, 0, 1100); m.addColorStop(0, 'rgba(0,0,0,1)'); m.addColorStop(1, 'rgba(0,0,0,.05)'); g.fillStyle = m; g.fillRect(0, 0, W, H);
  g.globalCompositeOperation = 'destination-out';
  g.filter = 'blur(5px)';
  { const r = rng(44); for (let i = 0; i < 300; i++) { const x = 1500 + r() * 220, y = 700 + r() * 440, k = clamp((x - 1530) / 150) * clamp((y - 760) / 260 + .35); if (r() < k) { g.beginPath(); g.arc(x, y, 6 + r() * 12, 0, TAU); g.fill(); } } }
  g.filter = 'none';
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
  { const r = rng(71); ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.lineCap = 'round';
    for (let i = 0; i < 110; i++) { const t = r(), x = 1540 + t * 360 + (r() - .5) * 70, y = 780 + r() * 360 - t * 240, s_ = (1 - t) * 6 + 1.5, gold = r() < .22;
      const col = gold ? '255,214,110' : '200,240,255', a = (gold ? .6 : .4) + r() * .4;
      const gr = ctx.createLinearGradient(x, y, x - 34, y + 12); gr.addColorStop(0, `rgba(${col},${a})`); gr.addColorStop(1, `rgba(${col},0)`);
      ctx.strokeStyle = gr; ctx.lineWidth = s_ * .8; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - 34, y + 12); ctx.stroke();  // geride kalan iz
      ctx.fillStyle = `rgba(${col},${a})`; ctx.beginPath(); ctx.arc(x, y, s_, 0, TAU); ctx.fill(); }
    ctx.restore(); }
  { const r = rng(12); for (let i = 0; i < 12; i++) sparkle(ctx, 1000 + r() * 880, 460 + r() * 520, 5 + r() * 6, '#ffd36a', .5 + r() * .4); }
  const orf = orpheus(); ctx.drawImage(orf, 0, 0);
  // parmak uçları arasındaki kıvılcım: karedeki en parlak nokta
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, GAP[0], GAP[1], 230, '#ffe2a0', .55); ctx.restore();
  sparkle(ctx, GAP[0], GAP[1], 42, '#fff0c4', 1);
  // kâğıt dokusu (videodaki gibi belirgin) + odağa (yüz ve eller) merkezli kenar kararması
  const [n, ng] = layer(); const id = ng.createImageData(W, H), d = id.data, r = rng(3);
  for (let i = 0; i < d.length; i += 4) { const v_ = 128 + (r() - .5) * 80; d[i] = d[i + 1] = d[i + 2] = v_; d[i + 3] = 255; }
  ng.putImageData(id, 0, 0);
  ctx.save(); ctx.globalCompositeOperation = 'soft-light'; ctx.globalAlpha = .45; ctx.drawImage(n, 0, 0); ctx.restore();
  const vg = ctx.createRadialGradient(900, 560, H * .4, 900, 560, H * 1.1); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,12,.55)');
  ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  // yazı (dokunun üstünde, keskin)
  if (!Q.has('notext')) {
    const T = { a: ['ARKANA', 'BAKMA!'], b: ['TEK BAKIŞ', 'YETTİ'] }[v] || ['ARKANA', 'BAKMA!'];
    const font = Q.get('font') || 'Anton';
    const f1 = +(Q.get('f1') || 168), f2 = +(Q.get('f2') || 246), x = 1872, y1 = 26 + f1 * .86, y2 = y1 + (v === 'b' ? 34 : 16) + f2 * .86;
    ctx.save(); ctx.textBaseline = 'alphabetic'; ctx.lineJoin = 'round';
    const fnt = f => `${font === 'Anton' ? '' : '900 '}${f}px ${font}`, wd = (s, f) => { ctx.font = fnt(f); return ctx.measureText(s).width; };
    // B'de Ş'nin çengeli alttaki İ'nin noktasına değmesin: blok sola hizalı, kısa satır sağda boşluk bırakır
    const left = v === 'b', lx = x - Math.max(wd(T[0], f1), wd(T[1], f2));
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
