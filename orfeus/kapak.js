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
// yan profil baş (+x yönüne bakar; dir -1 ile aynalanır). Birimler: baş ~230 birim yüksekliğinde.
function head(g, cx, cy, s, dir, o) {
  g.save(); g.translate(cx, cy); g.scale(s * dir, s); g.lineJoin = g.lineCap = 'round';
  const fem = !!o.fem;
  // saç: arka kütle
  if (fem) {
    g.fillStyle = o.hair; g.beginPath(); g.arc(-88, -62, 44, 0, TAU); g.fill(); // topuz
    g.fill(path([[-96, -40], [-90, -92], [-48, -126], [12, -132], [58, -110], [74, -84], [46, -92], [6, -96], [-18, -80], [-22, -46], [-34, -8], [-62, 22], [-92, 6]]));
  } else {
    const hp = path([[-96, -28], [-100, -76], [-72, -118], [-18, -138], [38, -128], [74, -102], [80, -80], [52, -88], [22, -94], [0, -82], [-12, -58], [-10, -30], [-28, -8], [-46, 34], [-68, 58], [-96, 34]]);
    g.fillStyle = o.hair; g.fill(hp);
    // bukleler: kenar boyunca küçük daireler
    const r = rng(9);
    for (const [x, y, rr] of [[-92, 28, 20], [-100, -2, 22], [-104, -36, 22], [-98, -72, 22], [-80, -104, 22], [-50, -126, 22], [-14, -136, 22], [22, -132, 21], [54, -116, 20], [74, -96, 17], [-72, 52, 18], [-52, 40, 16]]) {
      g.beginPath(); g.arc(x, y, rr, 0, TAU); g.fill();
    }
    g.strokeStyle = o.hairLight; g.lineWidth = 3.2;
    for (const [x, y, rr] of [[-92, 26, 12], [-98, -6, 13], [-100, -40, 13], [-92, -76, 13], [-74, -104, 13], [-44, -122, 12], [-10, -128, 12], [22, -122, 11], [50, -106, 10], [-70, 46, 10], [-40, -60, 12], [-54, -20, 12], [-20, -96, 12]]) {
      g.beginPath(); g.arc(x, y, rr, PI * (1.05 + r() * .3), PI * (1.7 + r() * .3)); g.stroke();
    }
  }
  // ten: kafatası + yüz profili (saç başlığı ve kulak tenden sonra çizilir)
  const sk = new Path2D();
  if (fem) {
    sk.moveTo(-60, -84); sk.bezierCurveTo(-36, -118, 30, -124, 60, -92); sk.bezierCurveTo(74, -76, 78, -58, 80, -44);
    sk.quadraticCurveTo(84, -38, 82, -32); sk.bezierCurveTo(88, -20, 98, -6, 101, 2); sk.quadraticCurveTo(99, 8, 90, 9);
    sk.quadraticCurveTo(88, 13, 91, 18); sk.quadraticCurveTo(94, 22, 91, 26); sk.lineTo(85, 30); sk.lineTo(90, 34); sk.quadraticCurveTo(92, 40, 87, 45);
    sk.bezierCurveTo(85, 52, 88, 58, 82, 66); sk.bezierCurveTo(74, 80, 56, 84, 38, 80); sk.bezierCurveTo(18, 76, -2, 64, -16, 48);
  } else {
    sk.moveTo(-60, -84); sk.bezierCurveTo(-40, -120, 30, -128, 62, -94); sk.bezierCurveTo(76, -78, 80, -60, 82, -46);
    sk.quadraticCurveTo(89, -40, 85, -33); sk.bezierCurveTo(93, -20, 105, -6, 111, 2); sk.quadraticCurveTo(110, 10, 97, 11);
    sk.quadraticCurveTo(92, 15, 95, 20); sk.quadraticCurveTo(99, 23, 96, 27); sk.lineTo(85, 32); sk.lineTo(94, 42);
    sk.quadraticCurveTo(97, 48, 92, 54); sk.bezierCurveTo(90, 60, 95, 66, 90, 76); sk.bezierCurveTo(84, 92, 62, 96, 40, 92); sk.bezierCurveTo(20, 88, 0, 76, -14, 60);
  }
  sk.bezierCurveTo(-40, 40, -78, 4, -60, -84); sk.closePath();
  g.fillStyle = o.mouthDark; g.beginPath(); g.ellipse(fem ? 88 : 92, fem ? 31 : 34, 7, fem ? 6 : 10, 0, 0, TAU); g.fill(); // ağız içi (açık)
  g.fillStyle = o.skin; g.fill(sk);
  // yanak ve çene gölgesi
  g.save(); g.clip(sk); const sg = g.createLinearGradient(0, 20, 0, 100); sg.addColorStop(0, rgba(o.skinDark, 0)); sg.addColorStop(1, rgba(o.skinDark, .7)); g.fillStyle = sg; g.fillRect(-120, 0, 260, 120);
  g.fillStyle = rgba(o.skinDark, .35); g.beginPath(); g.ellipse(-20, -10, 40, 70, 0, 0, TAU); g.fill(); g.restore();
  // saç başlığı: alından enseye kafatasını örter
  g.fillStyle = o.hair;
  if (fem) g.fill(path([[66, -92], [48, -84], [24, -76], [6, -60], [-6, -36], [-22, -14], [-36, 14], [-60, 30], [-96, 10], [-100, -50], [-70, -112], [-10, -132], [44, -118]]));
  else {
    g.fill(path([[76, -94], [60, -84], [38, -78], [20, -66], [8, -48], [2, -28], [-14, -14], [-24, 12], [-40, 40], [-64, 60], [-98, 40], [-106, -30], [-82, -112], [-20, -142], [42, -132]]));
    for (const [x, y, rr] of [[8, -50, 13], [-2, -26, 12], [-18, 0, 12], [-30, 26, 12], [20, -66, 12]]) { g.beginPath(); g.arc(x, y, rr, 0, TAU); g.fill(); }
    g.strokeStyle = o.hairLight; g.lineWidth = 3.2; const r2 = rng(19);
    for (const [x, y, rr] of [[-60, -80, 13], [-30, -110, 12], [-70, -40, 13], [-50, 10, 12], [-80, 10, 12], [0, -100, 11], [30, -104, 10], [-30, -60, 12]]) { g.beginPath(); g.arc(x, y, rr, PI * (1.05 + r2() * .3), PI * (1.7 + r2() * .3)); g.stroke(); }
  }
  // kulak
  g.fillStyle = o.skin; g.beginPath(); g.ellipse(-8, -8, 13, 19, .15, 0, TAU); g.fill();
  g.strokeStyle = o.skinDark; g.lineWidth = 3; g.beginPath(); g.arc(-6, -8, 9, -1.2, 1.6); g.stroke();
  if (fem) { g.fillStyle = o.accent; g.beginPath(); g.arc(-6, 20, 6, 0, TAU); g.fill(); } // küpe
  // göz: iri, açık (dehşet / özlem), irise ışık
  const ex = 64, ey = -27;
  g.fillStyle = '#ffffff'; g.beginPath(); g.moveTo(ex - 18, ey); g.quadraticCurveTo(ex - 2, ey - 14, ex + 16, ey - 1); g.quadraticCurveTo(ex, ey + 9, ex - 18, ey); g.fill();
  g.fillStyle = o.iris; g.beginPath(); g.arc(ex + 5, ey - 2, 7.5, 0, TAU); g.fill();
  g.fillStyle = '#ffffff'; g.beginPath(); g.arc(ex + 7.5, ey - 4.5, 2.4, 0, TAU); g.fill();
  g.strokeStyle = o.line; g.lineWidth = 4; g.beginPath(); g.moveTo(ex - 20, ey + 1); g.quadraticCurveTo(ex - 2, ey - 16, ex + 18, ey - 1); g.stroke();
  // kaş: iç ucu (öne doğru) kalkık — keder/korku
  g.strokeStyle = o.brow; g.lineWidth = fem ? 5 : 7; g.beginPath(); g.moveTo(ex - 20, ey - 15); g.quadraticCurveTo(ex - 2, ey - 19, ex + 16, ey - 31); g.stroke();
  if (!fem) { g.strokeStyle = rgba(o.skinDark, .8); g.lineWidth = 2.5; g.beginPath(); g.moveTo(ex - 6, ey - 42); g.quadraticCurveTo(ex + 6, ey - 46, ex + 14, ey - 44); g.moveTo(ex - 2, ey - 52); g.quadraticCurveTo(ex + 8, ey - 55, ex + 13, ey - 53); g.stroke(); }
  // burun deliği, dudak çizgisi
  g.strokeStyle = o.skinDark; g.lineWidth = 2.5; g.beginPath(); g.arc(fem ? 90 : 99, fem ? 5 : 6, 4, PI * .2, PI * 1.1); g.stroke();
  g.fillStyle = o.lip; g.beginPath(); g.ellipse(fem ? 87 : 93, fem ? 40 : 46, 6, 3.5, .3, 0, TAU); g.fill();
  // gözyaşı
  if (o.tear) { g.fillStyle = '#c9eeff'; g.beginPath(); g.moveTo(ex - 2, ey + 14); g.quadraticCurveTo(ex + 6, ey + 28, ex - 1, ey + 32); g.quadraticCurveTo(ex - 8, ey + 28, ex - 2, ey + 14); g.fill(); g.fillStyle = '#ffffff'; g.beginPath(); g.arc(ex - 3, ey + 26, 2, 0, TAU); g.fill(); }
  // ön saç / defne tacı
  if (fem) {
    g.fillStyle = o.hair; g.fill(path([[60, -96], [30, -114], [-20, -118], [-60, -100], [-40, -92], [0, -98], [40, -92]]));
    g.strokeStyle = o.accent; g.lineWidth = 7; g.beginPath(); g.moveTo(62, -92); g.quadraticCurveTo(0, -122, -70, -84); g.stroke();
  } else {
    g.fillStyle = o.hair; for (const [x, y, rr] of [[66, -96, 16], [50, -108, 16], [72, -82, 11]]) { g.beginPath(); g.arc(x, y, rr, 0, TAU); g.fill(); }
    // altın defne tacı
    const band = [[70, -92], [40, -110], [0, -116], [-40, -108], [-74, -88], [-92, -60]];
    g.strokeStyle = '#a8761c'; g.lineWidth = 5; g.beginPath(); sp(g, band, false); g.stroke();
    for (let i = 0; i < band.length - 1; i++) for (let k = 0; k < 3; k++) {
      const u = k / 3, x = lerp(band[i][0], band[i + 1][0], u), y = lerp(band[i][1], band[i + 1][1], u), a = Math.atan2(band[i + 1][1] - band[i][1], band[i + 1][0] - band[i][0]);
      for (const sd of [-1, 1]) { g.save(); g.translate(x, y); g.rotate(a + sd * .7 + PI); g.fillStyle = sd > 0 ? '#f6cf5a' : '#e0a92e'; g.beginPath(); g.ellipse(9, 0, 11, 4.6, 0, 0, TAU); g.fill(); g.restore(); }
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
const OPEN = [[-80, -80], [540, -80], [740, 30], [910, 220], [1000, 470], [1010, 760], [950, 1160], [-80, 1160]];
const OPEN_P = path(OPEN);
function edgeX(y) { for (let i = 1; i < OPEN.length - 2; i++) { const a = OPEN[i], b = OPEN[i + 1]; if (y >= a[1] && y <= b[1]) return lerp(a[0], b[0], (y - a[1]) / (b[1] - a[1])); } return y < 0 ? 540 : 950; }

function underworld(g) {
  const bg = g.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#202a63'); bg.addColorStop(.55, '#151b45'); bg.addColorStop(1, '#0b0f2a');
  g.fillStyle = bg; g.fillRect(0, 0, W, H);
  glow(g, 1700, 120, 700, '#5b3a9a', .55); glow(g, 1300, 900, 600, '#1f6f86', .25);
  cloudBank(g, 980, 2000, 250, 50, 95, '#26306b', '#6f86d4', 3, { shadow: '#18204f', depth: 60, rw: 3.5 });
  cloudBank(g, 1100, 2000, 330, 40, 80, '#1e275c', '#5268b8', 4, { shadow: '#141a44', depth: 40, rw: 3 });
  // zemin: köşeli koyu kayalar
  lowPoly(g, poly([[700, 940], [1100, 900], [1500, 930], [2000, 900], [2000, 1100], [700, 1100]]), 650, 860, 2000, 1100, 70, 21,
    (x, y, r) => mix('#1b2350', '#2e3a74', r * .7 + (y < 950 ? .3 : 0)));
}
function dawnWorld(g) {
  g.save(); g.clip(OPEN_P);
  const sky = g.createLinearGradient(0, 0, 0, 900); sky.addColorStop(0, '#fff2cc'); sky.addColorStop(.45, '#fcd38c'); sky.addColorStop(.8, '#f7a35d'); sky.addColorStop(1, '#ef8a4c');
  g.fillStyle = sky; g.fillRect(-80, -80, 1200, 1300);
  // güneş ve ışınlar
  const sx = 330, sy = 640;
  g.save(); g.globalAlpha = .16; g.fillStyle = '#fffbe8';
  for (let i = 0; i < 18; i++) { const a = i / 18 * TAU + .1, w = .07; g.beginPath(); g.moveTo(sx, sy); g.lineTo(sx + Math.cos(a - w) * 1500, sy + Math.sin(a - w) * 1500); g.lineTo(sx + Math.cos(a + w) * 1500, sy + Math.sin(a + w) * 1500); g.fill(); }
  g.restore();
  glow(g, sx, sy, 520, '#fff1c4', .9); g.fillStyle = '#fff8e2'; g.beginPath(); g.arc(sx, sy, 78, 0, TAU); g.fill();
  cloudBank(g, -80, 760, 210, 46, 86, '#fff6df', '#efa35b', 7, { shadow: '#f4c58c', depth: 70 });
  cloudBank(g, 120, 820, 360, 30, 58, '#ffe8bd', '#ec9a52', 8, { shadow: '#f0b77a', depth: 40, rw: 3.5 });
  // tepeler ve tepedeki şehir (videodaki yeryüzü)
  g.fillStyle = '#6fa597'; g.fill(path([[-80, 720], [180, 640], [420, 690], [700, 650], [1000, 700], [1000, 1200], [-80, 1200]]));
  g.fillStyle = '#86b36c'; g.fill(path([[-80, 600], [60, 540], [170, 520], [300, 560], [380, 640], [520, 760], [-80, 820]]));
  { const r = rng(5); for (let row = 0; row < 5; row++) for (let i = 0; i < 6 - row; i++) {
      const x = 30 + row * 24 + i * 44 + r() * 8, y = 600 - row * 26 - Math.max(0, 2 - Math.abs(i - 2.5)) * 6;
      g.fillStyle = '#f6eedd'; g.fillRect(x, y, 34, 26); g.fillStyle = '#c4553a'; g.beginPath(); g.moveTo(x - 4, y); g.lineTo(x + 17, y - 14); g.lineTo(x + 38, y); g.fill();
      g.fillStyle = '#7c8a8f'; g.fillRect(x + 12, y + 10, 7, 9); } // ev, kiremit çatı, pencere
    g.fillStyle = '#f6eedd'; g.fillRect(132, 448, 70, 30); for (let k = 0; k < 5; k++) { g.fillStyle = '#e6dcc6'; g.fillRect(136 + k * 14, 456, 6, 22); } g.fillStyle = '#f6eedd'; g.beginPath(); g.moveTo(126, 450); g.lineTo(167, 428); g.lineTo(208, 450); g.fill(); }
  // yol: mağaradan güneşe
  g.fillStyle = '#e8b072'; g.fill(path([[318, 716], [342, 716], [380, 780], [330, 860], [420, 960], [600, 1160], [80, 1160], [200, 960], [250, 860], [300, 780]]));
  g.strokeStyle = '#f6d39a'; g.lineWidth = 5; g.beginPath(); sp(g, [[330, 724], [336, 790], [300, 870], [330, 970], [360, 1160]], false); g.stroke();
  glow(g, sx, sy, 900, '#ffd89a', .35);
  g.restore();
}
function caveRock(g) { // eslint-disable-line no-param-reassign
  // ağız çevresi: dışarıdaki ışıkla yanan sıcak yüzler, içeri doğru soğuk ve koyu
  // kaya ayrı katmanda çizilir, sağa doğru saydamlaşarak yeraltının arka planına karışır (dikiş çizgisi olmaz)
  const dst = g; const [rc, rg] = layer(); g = rg;
  const clip = new Path2D(); clip.rect(-100, -100, W + 200, H + 200); clip.addPath(OPEN_P);
  lowPoly(g, clip, 380, -120, 1520, 1200, 84, 13, (x, y, r) => {
    const d = (x - edgeX(y)) / 420; // ağız kenarından uzaklık
    const warm = clamp(1 - d * 1.8), base = mix(mix('#4a5291', '#2b3270', r), '#1d2457', clamp(d * .9)), lit = mix('#e39a64', '#9c5a63', r);
    return mix(base, lit, warm * (.5 + r * .5));
  });
  g.globalCompositeOperation = 'destination-in'; const fade = g.createLinearGradient(1050, 0, 1460, 0); fade.addColorStop(0, 'rgba(0,0,0,1)'); fade.addColorStop(1, 'rgba(0,0,0,0)');
  g.fillStyle = fade; g.fillRect(-100, -100, W + 200, H + 200); g.globalCompositeOperation = 'source-over';
  dst.drawImage(rc, 0, 0); g = dst;
  // ağız kenarında ışık sızması
  g.save(); g.globalCompositeOperation = 'lighter'; for (let y = 0; y < H; y += 60) glow(g, edgeX(y) + 30, y, 160, '#ff9a55', .12); g.restore();
}
function orpheus() {
  const [c, g] = layer();
  const SK = '#b26b45', SKD = '#7b3f27';
  lyre(g, 596, 620, 2.6, -.42);                                   // sırtında lir: gökyüzüne karşı siluet
  g.fillStyle = SK; g.fill(path([[740, 520], [820, 530], [828, 590], [846, 636], [704, 636], [722, 590]]));  // boyun
  // kiton
  const body = path([[640, 612], [700, 594], [790, 590], [884, 608], [934, 656], [958, 770], [978, 910], [992, 1120], [540, 1120], [556, 910], [580, 770], [604, 666]]);
  g.fillStyle = '#e6d6b8'; g.fill(body);
  g.save(); g.clip(body); g.strokeStyle = '#d6c4a2'; g.lineWidth = 7; g.lineCap = 'round';
  for (const [x0, x1] of [[650, 600], [700, 660], [760, 740], [830, 850], [900, 940]]) { g.beginPath(); g.moveTo(x0, 640); g.quadraticCurveTo((x0 + x1) / 2 - 12, 860, x1, 1100); g.stroke(); }
  g.fillStyle = '#b8372a'; g.fill(poly([[620, 640], [700, 610], [1000, 1010], [1000, 1120], [930, 1120]])); // kırmızı şal
  g.fillStyle = '#8e2a20'; g.fill(poly([[700, 610], [722, 616], [1000, 990], [1000, 1010]]));
  g.strokeStyle = '#f2c14e'; g.lineWidth = 9; g.beginPath(); g.moveTo(700, 604); g.quadraticCurveTo(780, 628, 872, 612); g.stroke(); // altın yaka
  g.restore();
  // geriye uzanan kol ve el (Evridiki'ye)
  limb(g, [[884, 650], [1000, 694], [1086, 676]], [66, 54], SK);
  g.fillStyle = '#efe4cd'; g.beginPath(); g.ellipse(902, 652, 46, 38, .4, 0, TAU); g.fill(); // kol ağzı
  g.strokeStyle = '#f2c14e'; g.lineWidth = 6; g.beginPath(); g.ellipse(902, 652, 46, 38, .4, -.2, 1.6); g.stroke();
  hand(g, 1082, 676, -.12, 1.05, SK, SKD, { spread: .16 });
  head(g, 778, 440, 1.34, 1, { skin: SK, skinDark: SKD, hair: '#22150f', hairLight: '#6b4532', iris: '#1d120c', line: '#24140c', brow: '#1d110b', lip: '#8a3a2a', mouthDark: '#3d140e', tear: true });
  // ışık: arkadan sıcak güneş (sol kenar), önden Evridiki'nin soğuk mavisi (sağ kenar)
  const [o, og] = layer(); og.drawImage(c, 0, 0);
  og.globalCompositeOperation = 'source-atop';
  const cool = og.createLinearGradient(1180, 0, 760, 0); cool.addColorStop(0, 'rgba(120,200,255,.42)'); cool.addColorStop(1, 'rgba(120,200,255,0)'); og.fillStyle = cool; og.fillRect(0, 0, W, H);
  const shade = og.createLinearGradient(0, 700, 0, 1080); shade.addColorStop(0, 'rgba(20,20,60,0)'); shade.addColorStop(1, 'rgba(20,20,60,.6)'); og.fillStyle = shade; og.fillRect(0, 0, W, H);
  rim(og, c, 9, 0, '#ffd28a', .95, 2.5);    // sol kenar: güneş
  rim(og, c, -6, 2, '#8fe3ff', .8, 3);      // sağ kenar: hayalet ışığı
  return o;
}
function eurydice() {
  const [c, g] = layer();
  const SK = '#e3f6ff', SKD = '#8fc0e2', DR = '#c4e9fd';
  g.fillStyle = SK; g.fill(path([[1440, 606], [1494, 610], [1508, 684], [1430, 686]]));
  const body = path([[1396, 690], [1468, 676], [1546, 690], [1588, 768], [1606, 890], [1632, 1010], [1656, 1120], [1376, 1120], [1386, 990], [1384, 850], [1382, 748]]);
  g.fillStyle = DR; g.fill(body);
  g.save(); g.clip(body); g.strokeStyle = '#9fd0ee'; g.lineWidth = 6; g.lineCap = 'round';
  for (const x of [1424, 1476, 1528, 1576]) { g.beginPath(); g.moveTo(x, 724); g.quadraticCurveTo(x + 14, 880, x + 30, 1100); g.stroke(); }
  g.strokeStyle = '#7fb9e6'; g.lineWidth = 8; g.beginPath(); g.moveTo(1404, 704); g.quadraticCurveTo(1468, 734, 1540, 704); g.stroke();
  g.restore();
  limb(g, [[1424, 720], [1352, 742], [1300, 700]], [54, 44], SK);
  g.fillStyle = DR; g.beginPath(); g.ellipse(1416, 718, 38, 32, -.4, 0, TAU); g.fill();
  hand(g, 1304, 698, PI + .3, .9, SK, SKD, { spread: .2, flip: true });
  head(g, 1484, 556, .98, -1, { fem: true, skin: SK, skinDark: SKD, hair: '#8fc2e6', hairLight: '#d9f2ff', iris: '#1f4f86', line: '#24508a', brow: '#2f5f99', lip: '#6f9fd6', mouthDark: '#3d6aa3', accent: '#ffd36a' });
  // dağılma: alt ve arka kısım zerrelere dönüşür
  g.globalCompositeOperation = 'destination-in';
  const m = g.createLinearGradient(0, 700, 0, 1060); m.addColorStop(0, 'rgba(0,0,0,1)'); m.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = m; g.fillRect(0, 0, W, H);
  g.globalCompositeOperation = 'destination-out';
  { const r = rng(44); for (let i = 0; i < 420; i++) { const x = 1490 + r() * 200, y = 640 + r() * 460, k = clamp((x - 1510) / 160) * clamp((y - 680) / 300 + .3); if (r() < k) { g.beginPath(); g.arc(x, y, 3 + r() * 10, 0, TAU); g.fill(); } } }
  g.globalCompositeOperation = 'source-over';
  return c;
}

function draw(v) {
  underworld(ctx); dawnWorld(ctx); caveRock(ctx);
  // Evridiki: hayalet ışıması + zerreler
  glow(ctx, 1470, 700, 520, '#6fd3ff', .34);
  const ev = eurydice();
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.filter = 'blur(22px)'; ctx.globalAlpha = .75; ctx.drawImage(ev, 0, 0); ctx.restore();
  ctx.drawImage(ev, 0, 0);
  { const r = rng(71); ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (let i = 0; i < 160; i++) { const t = r(), x = 1500 + t * 420 + (r() - .5) * 80, y = 640 + r() * 420 - t * 260, s = (1 - t) * 7 + 1.5;
      ctx.fillStyle = r() < .2 ? `rgba(255,214,110,${.5 + r() * .5})` : `rgba(200,240,255,${.35 + r() * .55})`; ctx.beginPath(); ctx.arc(x, y, s, 0, TAU); ctx.fill(); }
    ctx.restore(); }
  // ateş böcekleri (videodaki altın kıvılcımlar)
  { const r = rng(12); for (let i = 0; i < 26; i++) sparkle(ctx, 1000 + r() * 900, 380 + r() * 560, 5 + r() * 7, '#ffd36a', .5 + r() * .5); }
  // Orfeus
  const orf = orpheus(); ctx.drawImage(orf, 0, 0);
  // parmak uçları arasında kıvılcım: odak noktası
  sparkle(ctx, 1194, 676, 26, '#ffe7a6', 1); glow(ctx, 1194, 676, 120, '#ffe7a6', .35);
  // kâğıt dokusu + kenar kararması
  const [n, ng] = layer(); const id = ng.createImageData(W, H), d = id.data, r = rng(3);
  for (let i = 0; i < d.length; i += 4) { const v_ = 128 + (r() - .5) * 70; d[i] = d[i + 1] = d[i + 2] = v_; d[i + 3] = 255; }
  ng.putImageData(id, 0, 0);
  ctx.save(); ctx.globalCompositeOperation = 'soft-light'; ctx.globalAlpha = .32; ctx.drawImage(n, 0, 0); ctx.restore();
  const vg = ctx.createRadialGradient(W / 2, H / 2, H * .45, W / 2, H / 2, H * 1.05); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,10,.45)');
  ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
  // yazı
  if (!Q.has('notext')) {
    const T = { a: ['ARKANA', 'BAKMA!'], b: ['TEK BİR', 'BAKIŞ'], c: ['SAKIN', 'DÖNME!'] }[v] || ['ARKANA', 'BAKMA!'];
    const font = Q.get('font') || 'Anton';
    const f1 = +(Q.get('f1') || 132), f2 = +(Q.get('f2') || 226), x = 1868;
    ctx.save(); ctx.textAlign = 'right'; ctx.textBaseline = 'alphabetic'; ctx.lineJoin = 'round';
    for (const [s, y, f, fill] of [[T[0], 60 + f1 * .9, f1, '#ffffff'], [T[1], 60 + f1 * .9 + 18 + f2 * .9, f2, '#ffcf3a']]) {
      ctx.font = `${font === 'Anton' ? '' : '900 '}${f}px ${font}`;
      ctx.shadowColor = 'rgba(5,6,25,.85)'; ctx.shadowBlur = 26; ctx.shadowOffsetY = 8;
      ctx.lineWidth = f * .13; ctx.strokeStyle = '#0b0f2e'; ctx.strokeText(s, x, y);
      ctx.shadowColor = 'transparent'; ctx.fillStyle = fill; ctx.fillText(s, x, y);
    }
    ctx.restore();
  }
}
window.ready = (async () => {
  for (const f of ['150px Anton', '150px "Alfa Slab One"', '150px "Lilita One"', '150px "Bebas Neue"', '900 150px Cinzel']) await document.fonts.load(f, 'ARKANABAKMAĞİŞÖÜÇ!?');
  draw(Q.get('v') || 'a');
  return true;
})();
