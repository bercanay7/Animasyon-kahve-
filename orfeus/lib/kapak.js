// Orfeus ve Evridiki — kapak sistemine uyan kapak (27 Kasım 2026; kanal/KAPAK_SISTEMI.md)
// Üslup filmle aynı: katmanlı kâğıt kesme, köşeli (low-poly) mağara kayası, kâğıt pulu olup dağılan Evridiki, dokulu yüzey.
// Sistem: yazı sol üstte (Bebas, fildişi), Orfeus sağda koyu siluet (¾ yüz, defne tacı), zemin bastırılmış lacivert.
// Tek renkli nesne Evridiki'nin solgun ışığıdır; vurgu kelimesi de o renktedir. Karenin (yazı hariç) en parlak yeri iki elin arasıdır.
// Sağ alt süre rozeti (x 1440–1874, y 829–1034) yalnız koyu pelerin; önemli içerik yok.
// Kullanım: kapak_sistem.html → window.kapak({ yazisiz, satir:[[metin,vurgu?],…], px, tx, ty })
'use strict';
const W = 1920, H = 1080, TAU = Math.PI * 2, PI = Math.PI;
const ACC = '#9ED8F2', FIL = '#F3EAD7';           // vurgu (Evridiki'nin ışığı), fildişi
const SIL = '#0a0e1b', SIL2 = '#131a2c';          // siluet, siluetin kâğıt katı
const lerp = (a, b, t) => a + (b - a) * t, clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
function rng(seed) { let s = (seed * 2654435761) >>> 0 || 1; return () => { s ^= s << 13; s >>>= 0; s ^= s >>> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; }; }
function hex(c) { const n = parseInt(c.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function mix(a, b, t) { const A = hex(a), B = hex(b); t = clamp(t); return '#' + A.map((v, i) => Math.round(lerp(v, B[i], t)).toString(16).padStart(2, '0')).join(''); }
function rgba(c, a) { const A = hex(c); return `rgba(${A[0]},${A[1]},${A[2]},${a})`; }
function glow(g, x, y, r, c, a) { const gr = g.createRadialGradient(x, y, 0, x, y, r); gr.addColorStop(0, rgba(c, a)); gr.addColorStop(.4, rgba(c, a * .45)); gr.addColorStop(1, rgba(c, 0)); g.fillStyle = gr; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
function layer() { const c = document.createElement('canvas'); c.width = W; c.height = H; return [c, c.getContext('2d')]; }
function sp(p, pts, closed = true) {
  const n = pts.length; p.moveTo(pts[0][0], pts[0][1]);
  for (let i = 0; i < (closed ? n : n - 1); i++) {
    const p1 = pts[i], p2 = pts[(i + 1) % n], p0 = !closed && i === 0 ? p1 : pts[(i - 1 + n) % n], p3 = !closed && i + 2 >= n ? p2 : pts[(i + 2) % n];
    p.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]);
  }
  if (closed) p.closePath();
}
const path = (pts, closed = true) => { const p = new Path2D(); sp(p, pts, closed); return p; };
const poly = pts => { const p = new Path2D(); pts.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); p.closePath(); return p; };
const tr = (pts, ox, oy, s) => pts.map(([x, y]) => [ox + x * s, oy + y * s]);
// köşeli kaya: titrek ızgaradan üçgenler, her yüzün tonu ayrı (filmdeki mağara)
function lowPoly(g, bx0, by0, bx1, by1, cell, seed, shade) {
  const r = rng(seed), nx = Math.ceil((bx1 - bx0) / cell), ny = Math.ceil((by1 - by0) / cell), P = [];
  for (let j = 0; j <= ny; j++) for (let i = 0; i <= nx; i++) P.push([bx0 + i * cell + (r() - .5) * cell * .8, by0 + j * cell + (r() - .5) * cell * .8]);
  const id = (i, j) => P[j * (nx + 1) + i];
  for (let j = 0; j < ny; j++) for (let i = 0; i < nx; i++) {
    const a = id(i, j), b = id(i + 1, j), c = id(i + 1, j + 1), d = id(i, j + 1);
    for (const t of (r() < .5 ? [[a, b, c], [a, c, d]] : [[a, b, d], [b, c, d]])) {
      const cx = (t[0][0] + t[1][0] + t[2][0]) / 3, cy = (t[0][1] + t[1][1] + t[2][1]) / 3, col = shade(cx, cy, r()), pp = poly(t);
      g.fillStyle = col; g.strokeStyle = col; g.lineWidth = 1.5; g.fill(pp); g.stroke(pp);
    }
  }
}
// kenar ışığı: şeklin kaydırılmış kopyası çıkarılınca kalan şerit renklenir (ışık kaydırmanın tersinden gelir)
function rim(dst, src, dx, dy, col, a, blur = 3) {
  const [c, g] = layer(); g.drawImage(src, 0, 0); g.globalCompositeOperation = 'destination-out'; g.drawImage(src, dx, dy);
  g.globalCompositeOperation = 'source-in'; g.fillStyle = col; g.fillRect(0, 0, W, H);
  dst.save(); dst.globalCompositeOperation = 'lighter'; dst.globalAlpha = a; dst.filter = `blur(${blur}px)`; dst.drawImage(c, 0, 0); dst.filter = 'none'; dst.globalAlpha = a * .8; dst.drawImage(c, 0, 0); dst.restore();
}
function paperShadow(dst, src, dx, dy, a) { dst.save(); dst.filter = 'blur(10px) brightness(0)'; dst.globalAlpha = a; dst.drawImage(src, dx, dy); dst.restore(); }
function limb(g, pts, widths, col) { g.save(); g.lineCap = g.lineJoin = 'round'; g.strokeStyle = col;
  for (let i = 0; i < pts.length - 1; i++) { g.lineWidth = widths[i]; g.beginPath(); g.moveTo(...pts[i]); g.lineTo(...pts[i + 1]); g.stroke(); } g.restore(); }
// uzanan el: avuç + dört parmak + başparmak; ang yönüne uzanır
function hand(g, x, y, ang, s, col, spread = .25) {
  g.save(); g.translate(x, y); g.rotate(ang); g.scale(s, s); g.lineCap = 'round'; g.fillStyle = g.strokeStyle = col;
  g.beginPath(); g.ellipse(14, 0, 20, 17, 0, 0, TAU); g.fill();
  [[-11, 30, -1.5], [-4, 35, -.5], [4, 34, .5], [11, 28, 1.5]].forEach(([oy, L, k]) => { g.lineWidth = 9.5; g.beginPath(); g.moveTo(26, oy); g.lineTo(26 + Math.cos(k * spread) * L, oy + Math.sin(k * spread) * L); g.stroke(); });
  g.lineWidth = 10; g.beginPath(); g.moveTo(12, -12); g.quadraticCurveTo(22, -26, 36, -28); g.stroke();
  g.restore();
}

// ——— sahne ———
const GAP = [1092, 640];   // iki parmak ucu arasındaki boşluk: karenin odağı
function cave(g) {
  const bg = g.createLinearGradient(0, 0, 0, H); bg.addColorStop(0, '#111830'); bg.addColorStop(1, '#070a16'); g.fillStyle = bg; g.fillRect(0, 0, W, H);
  // kaya yüzleri: lacivert-gri, Evridiki'nin ışığına yakın yüzler hafifçe aydınlanır; sol üst (yazının altı) en sakin
  lowPoly(g, -120, -120, W + 120, H + 120, 150, 13, (x, y, r) => {
    const d = Math.hypot(x - GAP[0], y - GAP[1]) / 700, lit = clamp(1 - d) ** 2;
    const base = mix(mix('#1a2238', '#111729', r), '#0b0f1e', clamp((x < 1000 && y < 620 ? .55 : 0) + y / H * .5));
    return mix(base, mix('#2c4058', '#3a5670', r), lit * .75);
  });
  // tünelin ağzı: sağ üstte bastırılmış, renksiz soluk açıklık (yukarı dünya); odaktan sönük kalır
  g.save(); g.globalCompositeOperation = 'lighter'; glow(g, 1830, 40, 420, '#8b8f96', .16); g.restore();
  // filmdeki kâğıt katları: önde iki koyu kaya kenarı (sol alt ve üst)
  g.save(); g.fillStyle = 'rgba(0,0,0,.35)'; g.translate(8, 12);
  const rocks = [poly([[-40, 1100], [-40, 820], [120, 860], [260, 930], [430, 990], [620, 1100]]), poly([[-40, -40], [700, -40], [560, 30], [300, 60], [80, 50], [-40, 90]])];
  for (const p of rocks) g.fill(p); g.restore();
  g.fillStyle = '#0c1122'; for (const p of rocks) g.fill(p);
  g.strokeStyle = 'rgba(158,216,242,.10)'; g.lineWidth = 3; g.stroke(rocks[0]);
}
// Evridiki: uzakta, aşağıda; solgun ışıktan bir siluet, eteği ve sol yanı kâğıt pullarına ayrılıp karanlığa savrulur
const FLAKES = [];
function eurydice() {
  const [c, g] = layer();
  const SK = '#cce9f5', DR = '#b7e2f5', HR = '#6c9fc2';
  // gövde ve etek
  const body = path([[880, 800], [930, 786], [985, 794], [1012, 860], [1030, 960], [1050, 1100], [830, 1100], [846, 960], [858, 860]]);
  g.fillStyle = DR; g.fill(body);
  g.save(); g.clip(body); g.strokeStyle = '#8cc4e0'; g.lineWidth = 5; g.lineCap = 'round';
  for (const x of [880, 925, 970]) { g.beginPath(); g.moveTo(x, 820); g.quadraticCurveTo(x + 10, 950, x + 18, 1100); g.stroke(); }
  g.restore();
  // boyun ve baş (¾, ona, yukarı bakar); saç topuz, yüz çizgisiz (küçük boyda göz çizilmez: beyaz göz okuması olmasın)
  g.fillStyle = SK; g.fill(poly([[910, 760], [944, 758], [948, 800], [906, 802]]));
  g.fillStyle = HR; g.beginPath(); g.ellipse(904, 712, 40, 44, -.3, 0, TAU); g.fill(); g.beginPath(); g.arc(874, 696, 22, 0, TAU); g.fill();
  g.fillStyle = SK; g.fill(path([[906, 690], [936, 680], [962, 696], [970, 724], [962, 752], [940, 768], [916, 764], [902, 740]]));
  g.fillStyle = HR; g.fill(path([[900, 688], [930, 672], [962, 684], [944, 694], [916, 704]]));
  // ona uzanan kol: omuz → dirsek → bilek, parmaklar sağa-yukarı
  limb(g, [[976, 812], [1034, 768], [1050, 694]], [30, 24], SK);
  hand(g, 1050, 694, -.8, .95, SK, .3);
  // dağılma: alt kısım saydamlaşır; sol ve alt kenardan pullar kopar
  g.globalCompositeOperation = 'destination-in';
  const m = g.createLinearGradient(0, 900, 0, 1080); m.addColorStop(0, 'rgba(0,0,0,1)'); m.addColorStop(1, 'rgba(0,0,0,.05)'); g.fillStyle = m; g.fillRect(0, 0, W, H);
  g.globalCompositeOperation = 'destination-out';
  const r = rng(44), flake = (x, y, s_, a) => { const p = []; for (let k = 0; k < 4; k++) { const t = a + k * TAU / 4 + (r() - .5) * .9, rr = s_ * (.6 + r() * .6); p.push([x + Math.cos(t) * rr, y + Math.sin(t) * rr]); } return poly(p); };
  for (let i = 0; i < 220; i++) {
    const x = 820 + r() * 160, y = 820 + r() * 260, k = clamp((900 - x) / 70 + .2) * clamp((y - 840) / 160 + .3);
    if (r() < k) { const s_ = 7 + r() * 11, a = r() * TAU; g.fill(flake(x, y, s_, a)); if (r() < .75) FLAKES.push([x, y, s_, a]); }
  }
  g.globalCompositeOperation = 'source-over';
  return c;
}
// Orfeus: koyu siluet; gövde çıkışa (sağa-yukarı) dönük, baş omzunun üstünden geriye, ona bakar (¾ yüz, sola-aşağı)
function orpheus() {
  const [c, g] = layer();
  const HX = 1440, HY = 322, S = 1.3, RT = -.3;           // baş merkezi, ölçeği, eğimi (aşağı, ona doğru)
  const P = pts => pts.map(([x, y]) => [HX + (x * Math.cos(RT) - y * Math.sin(RT)) * S, HY + (x * Math.sin(RT) + y * Math.cos(RT)) * S]);
  // pelerin (sırt): omuz eğimli, sırt çıkışa doğru kambur; kâğıt katları
  const cape = path([[1236, 600], [1300, 548], [1390, 520], [1480, 500], [1560, 506], [1640, 548], [1700, 620], [1742, 716], [1772, 840], [1790, 1100], [1110, 1100], [1150, 900], [1186, 744]]);
  g.fillStyle = SIL; g.fill(cape);
  g.save(); g.clip(cape);
  g.fillStyle = SIL2; g.fill(path([[1560, 512], [1650, 560], [1716, 650], [1756, 790], [1780, 960], [1790, 1100], [1660, 1100], [1672, 930], [1640, 770], [1590, 630]]));
  g.strokeStyle = '#04060d'; g.lineWidth = 9; g.lineCap = 'round';
  for (const [x0, y0, x1] of [[1330, 570, 1262], [1440, 540, 1420], [1570, 560, 1590]]) { g.beginPath(); g.moveTo(x0, y0); g.quadraticCurveTo((x0 + x1) / 2 + 30, 820, x1, 1100); g.stroke(); }
  g.restore();
  // ona uzanan kol: omuzdan aşağı-sola, dirsek bükük; parmaklar onun eline
  limb(g, [[1300, 590], [1214, 628], [1146, 636]], [62, 48], SIL);
  g.fillStyle = SIL; g.fill(path([[1236, 576], [1316, 540], [1360, 588], [1300, 646], [1226, 656], [1196, 620]]));   // omzu örten pelerin
  hand(g, 1146, 636, PI + .22, 1.05, SIL, .28);
  // boyun: dönmüş, çenenin altına
  g.fillStyle = SIL; g.fill(poly(P([[-36, 80], [52, 40], [80, 170], [-30, 176]])));
  // arka saç kütlesi: dalgalı, tutam uçlu kenar (yuvarlak top değil), ense uzun
  const hair = path(P([[-60, -90], [-44, -118], [-24, -126], [-8, -140], [14, -134], [34, -146], [52, -130], [72, -128], [86, -106], [104, -98], [106, -70], [120, -52], [112, -26], [122, 0], [108, 22], [112, 48], [92, 62], [84, 84], [60, 76], [40, 40], [20, -30], [-30, -60]]));
  g.fillStyle = SIL; g.fill(hair);
  // yüz: ¾ (uzak yanak çizgisi solda, burun yalnız ucu taşar), sola-aşağı bakar
  const face = path(P([[-58, -88], [-68, -62], [-70, -40], [-64, -26], [-70, -8], [-80, 8], [-72, 16], [-66, 24], [-70, 36], [-64, 44], [-66, 54], [-58, 66], [-58, 82], [-46, 96], [-18, 104], [16, 94], [38, 60], [42, 18], [22, -40], [-10, -82]]));
  g.fillStyle = SIL; g.fill(face);
  g.save(); g.clip(face);
  // ışık düzlemi: Evridiki'nin ışığı yüzün ona dönük yarısını soluk aydınlatır; sağ yarı (kulağa doğru) gölgede
  const [a0, a1] = P([[-80, 0], [20, 0]]);
  const lg = g.createLinearGradient(a0[0], a0[1], a1[0], a1[1]); lg.addColorStop(0, '#3d5d76'); lg.addColorStop(.5, '#22354b'); lg.addColorStop(1, rgba(SIL, 0));
  g.fillStyle = lg; g.fillRect(HX - 200, HY - 200, 400, 400);
  g.fillStyle = 'rgba(8,12,24,.85)';
  g.fill(path(P([[-66, -40], [-46, -44], [-30, -40], [-6, -36], [0, -22], [-22, -14], [-40, -20], [-60, -22]])));   // kaş çıkıntısının gölgesi, iki göz çukuru
  g.fill(path(P([[-44, -14], [-34, 4], [-38, 18], [-50, 22], [-46, 4]])));                                          // burnun gölge yanı
  g.fill(path(P([[-70, 18], [-56, 16], [-48, 22], [-62, 26]])));                                                   // burun altı
  g.fill(path(P([[-66, 44], [-46, 40], [-30, 46], [-48, 50], [-64, 48]])));                                        // dudak arası
  g.fill(path(P([[-50, 72], [-20, 80], [10, 90], [-10, 104], [-46, 96]])));                                        // çene altı
  g.fillStyle = 'rgba(8,12,24,.75)'; g.fill(path(P([[-22, -60], [16, -40], [34, 20], [22, 70], [-8, 62], [-14, 0], [-28, -36]])));   // yanağın gölge yanı
  g.restore();
  // gözler: küçük, sıcak tonlu parıltı (beyaz göz yok); yakın gözden soluk gözyaşı izi
  for (const [gx, gy, k] of [[-18, -24, 1], [-56, -26, .75]]) {
    const [ex, ey] = P([[gx, gy]])[0]; g.fillStyle = '#05070e'; g.beginPath(); g.ellipse(ex, ey, 11 * S * k, 5 * S * k, RT - .1, 0, TAU); g.fill();
    g.fillStyle = '#c0915f'; g.beginPath(); g.arc(ex - 4 * S * k, ey + 1.5 * S, 2.4 * S * k, 0, TAU); g.fill();
  }
  { const [t0, t1, t2] = P([[-24, -16], [-30, 10], [-26, 36]]); g.strokeStyle = rgba(ACC, .4); g.lineWidth = 3; g.lineCap = 'round'; g.beginPath(); g.moveTo(...t0); g.quadraticCurveTo(...t1, ...t2); g.stroke(); }
  { const [kx, ky] = P([[30, 4]])[0]; g.fillStyle = SIL2; g.beginPath(); g.ellipse(kx, ky, 10 * S, 17 * S, RT + .15, 0, TAU); g.fill(); }   // kulak
  // defne tacı: alından enseye; yapraklar geriye yatık, siluetin dışına taşar (kenar ışığı yaprakları seçer)
  const band = P([[-64, -76], [-40, -104], [-4, -118], [36, -114], [74, -94], [104, -60]]);
  g.strokeStyle = SIL2; g.lineWidth = 6; g.beginPath(); sp(g, band, false); g.stroke();
  for (let i = 0; i < band.length - 1; i++) for (let k = 0; k < 3; k++) {
    const u = k / 3, x = lerp(band[i][0], band[i + 1][0], u), y = lerp(band[i][1], band[i + 1][1], u), a = Math.atan2(band[i + 1][1] - band[i][1], band[i + 1][0] - band[i][0]);
    for (const sd of [-1, 1]) { g.save(); g.translate(x, y); g.rotate(a + PI + sd * .65); g.fillStyle = sd > 0 ? SIL : '#1b2437'; g.beginPath(); g.ellipse(17 * S * .8, 0, 18 * S * .8, 6.4 * S * .8, 0, 0, TAU); g.fill(); g.restore(); }
  }
  // lir (ayrı katta, uzak yanda olduğu için kenar ışığı zayıf): uzak elinde, sırtın sağından taşar (karanlık zeminde siluet olarak okunur); rozetin üstünde kalır
  const [lc, l] = layer(); { const g = l;
  g.save(); g.translate(1778, 668); g.rotate(.22); g.lineCap = g.lineJoin = 'round'; g.strokeStyle = SIL; g.lineWidth = 17;
  g.beginPath(); g.moveTo(-26, 26); g.bezierCurveTo(-64, -12, -58, -74, -34, -106); g.moveTo(26, 26); g.bezierCurveTo(64, -12, 58, -74, 34, -106); g.moveTo(-50, -90); g.lineTo(50, -90); g.stroke();
  g.fillStyle = SIL; g.beginPath(); g.ellipse(0, 32, 42, 27, 0, 0, TAU); g.fill();
  g.strokeStyle = '#33405e'; g.lineWidth = 2.4; for (let k = -2; k <= 2; k++) { g.beginPath(); g.moveTo(k * 8, -90); g.lineTo(k * 6, 22); g.stroke(); }
  g.restore();
  limb(g, [[1690, 610], [1736, 680], [1772, 700]], [46, 38], SIL); }   // lir tutan kol
  // kâğıt gölgesi + Evridiki tarafından (sol-aşağı) soğuk kenar ışığı + üstten çok hafif ikinci kenar
  const [o, og] = layer(); paperShadow(og, c, 14, 18, .55); og.drawImage(c, 0, 0);
  rim(og, c, 8, -5, ACC, .75, 2.5);
  rim(og, c, -2, 6, '#7e8ea8', .2, 3);
  paperShadow(og, lc, 14, 18, .5); og.drawImage(lc, 0, 0); rim(og, lc, 6, -4, ACC, .28, 2.5);
  // alt kısım kararır (odak yüz ve el; pelerinin alt kenar ışığı söner)
  og.save(); og.globalCompositeOperation = 'source-atop'; const lo = og.createLinearGradient(0, 660, 0, 960); lo.addColorStop(0, 'rgba(3,4,10,0)'); lo.addColorStop(1, 'rgba(3,4,10,.85)'); og.fillStyle = lo; og.fillRect(0, 0, W, H); og.restore();
  return o;
}
function yazi(g, satir, x, top, px) {
  g.save(); g.font = `400 ${px}px "Bebas Neue"`; g.textBaseline = 'alphabetic'; g.letterSpacing = '4px';
  const cap = px * .7, gap = px * .25; const kutu = [];
  satir.forEach(([s, vurgu], i) => {
    const y = top + cap + i * (cap + gap);
    g.shadowColor = 'rgba(2,4,12,.9)'; g.shadowBlur = px * .08; g.shadowOffsetY = 6; g.fillStyle = vurgu ? ACC : FIL; g.fillText(s, x, y);
    kutu.push([x, y - cap, g.measureText(s).width, cap]);
  });
  g.restore(); return kutu;
}
window.kapak = (o = {}) => {
  FLAKES.length = 0;
  const cv = document.getElementById('c'), g = cv.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, W, H);
  cave(g);
  // Evridiki'nin ışığı: el ile el arası en parlak; geniş ve sönük hale değil, ele merkezli
  g.save(); g.globalCompositeOperation = 'lighter'; glow(g, 990, 820, 380, ACC, .16); g.restore();
  const ev = eurydice(); paperShadow(g, ev, 10, 14, .4);
  g.save(); g.globalCompositeOperation = 'lighter'; g.filter = 'blur(20px)'; g.globalAlpha = .45; g.drawImage(ev, 0, 0); g.restore();
  g.drawImage(ev, 0, 0);
  // kopan pullar: sola-aşağı, karanlığa doğru savrulur; uzaklaştıkça küçülür ve söner
  { const r = rng(71);
    for (const [x0, y0, s0, a0] of FLAKES) {
      const t = Math.pow(r(), .8), dx = 30 + t * 300, x = x0 - dx, y = y0 + 20 + dx * (.25 + r() * .3) - 40 * r(), s_ = s0 * (1 - t * .6);
      if (r() < .3 || y > 1070) continue;
      const p = []; for (let k = 0; k < 4; k++) { const ang = a0 + t * 3 + k * TAU / 4 + (r() - .5) * .9, rr = s_ * (.6 + r() * .6); p.push([x + Math.cos(ang) * rr, y + Math.sin(ang) * rr]); }
      g.globalAlpha = (1 - t) * .8; g.fillStyle = r() < .5 ? '#cfeefb' : ACC; g.fill(poly(p));
    }
    g.globalAlpha = 1; }
  const orf = orpheus(); g.drawImage(orf, 0, 0);
  // parmak uçları arası: karenin en parlak noktası (yıldız ya da haç biçimi yok; yalnız yumuşak ışık)
  g.save(); g.globalCompositeOperation = 'lighter'; glow(g, GAP[0], GAP[1], 210, ACC, .42); glow(g, GAP[0], GAP[1], 80, '#eef9ff', .75); g.restore();
  // kâğıt dokusu + odağa merkezli kenar kararması
  const [n, ng] = layer(); const id = ng.createImageData(W, H), d = id.data, r = rng(3);
  for (let i = 0; i < d.length; i += 4) { const v_ = 128 + (r() - .5) * 70; d[i] = d[i + 1] = d[i + 2] = v_; d[i + 3] = 255; }
  ng.putImageData(id, 0, 0); g.save(); g.globalCompositeOperation = 'soft-light'; g.globalAlpha = .4; g.drawImage(n, 0, 0); g.restore();
  const vg = g.createRadialGradient(1150, 600, H * .35, 1150, 600, H * 1.15); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,10,.55)'); g.fillStyle = vg; g.fillRect(0, 0, W, H);
  // yazı: sol üst, iki satır, tek vurgu kelimesi Evridiki'nin renginde; kapak yazısı başlığın sözcüklerini tekrar etmez
  if (!o.yazisiz) window.KUTU = yazi(g, o.satir || [['ÇIKIŞTA'], ['KAYBETTİ', 1]], o.tx ?? 92, o.ty ?? 66, o.px ?? 300);
  return cv;
};
(async () => { await document.fonts.load('400 200px "Bebas Neue"', 'ÇIKIŞTA KAYBETTİ ĞÜŞÖ'); window.READY = true; })();
