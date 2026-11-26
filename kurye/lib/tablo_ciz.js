// "Mektuplar": durağan resmin katmanları (değer planlı düz resim; impasto motoru bunu spatula ve fırça darbelerine çevirir).
// Klasik betik; window.TABLO verir. Her katman ayrı tuval (derinlik kayması için): gok, daglar, tarla, agac, on.
// Birim: 1920×1080 kare pikseli. Ufuk y = 700 (3B kamera bununla eşleşir: tablo.html KAMERA).
// Kompozisyon: altın oranda sağda yalnız meşe; güneş tacın sol alt kenarının ardında (ışık yapraklardan sızar);
// sol alttan ağaca kıvrılan patika; ön planda koyu ot siluetleri çerçeveler.
'use strict';
(function (g) {
  const PI = Math.PI;
  const rng = s => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const P = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
  const Ell = (x, y, rx, ry, r = 0) => c => { c.moveTo(x + rx * Math.cos(r), y + rx * Math.sin(r)); c.ellipse(x, y, rx, ry, r, 0, PI * 2); };
  // yumuşak kapalı eğri (Catmull-Rom → Bezier)
  const S = pts => c => { const n = pts.length; c.moveTo(pts[0][0], pts[0][1]);
    for (let i = 0; i < n; i++) { const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      c.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]); }
    c.closePath(); };
  const lin = (stops, x0, y0, x1, y1) => c => { const gr = c.createLinearGradient(x0, y0, x1, y1); for (const [k, col] of stops) gr.addColorStop(k, col); return gr; };
  const rad = (stops, x, y, r) => c => { const gr = c.createRadialGradient(x, y, 0, x, y, r); for (const [k, col] of stops) gr.addColorStop(k, col); return gr; };
  // tepe silueti: sinüs katmanlarıyla tohumlu
  const sirt = (y0, A, f, ph, x0 = -60, x1 = 1980, alt = 1140) => { const pts = [[x0, alt]]; for (let x = x0; x <= x1; x += 40) pts.push([x, y0 - A * (Math.sin(x * f + ph) * .6 + Math.sin(x * f * 2.3 + ph * 1.7) * .3 + Math.sin(x * f * 5.1 + ph * .3) * .1)]); pts.push([x1, alt]); return P(pts); };

  const GUNES = [1188, 622];
  const UFUK = 700;

  // ---------------- gök ----------------
  function gok(R) {
    R.fill(P([[-80, -80], [2000, -80], [2000, 760], [-80, 760]]), lin([[0, '#1a1838'], [.28, '#3a2b58'], [.5, '#8a4d6c'], [.68, '#d87a62'], [.82, '#f2a65c'], [.93, '#ffd08a'], [1, '#ffe2a8']], 0, -80, 0, 760), { dir: 0, maxR: 30, group: 'gok', jit: .05, aj: .25 });
    // güneşin çevresinde ışıma
    R.fill(Ell(GUNES[0], GUNES[1], 520, 300), rad([[0, 'rgba(255,240,196,1)'], [.18, 'rgba(255,214,140,.85)'], [.5, 'rgba(250,170,96,.35)'], [1, 'rgba(240,150,90,0)']], GUNES[0], GUNES[1], 520), { dir: { radial: GUNES }, maxR: 16, group: 'gok', jit: .04 });
    R.fill(Ell(GUNES[0], GUNES[1], 38, 38), '#fff6dc', { dir: { radial: GUNES, off: 90 }, maxR: 6, group: 'gunes', jit: .02, hgt: 1.4 });
    // bulut kümeleri: her küme üst üste binen loblar; üstleri mor gölgede, altları güneşe göre gül → altın yanar
    const r = rng(17);
    const kume = (cx, cy, w, h, n, ust, orta, alt, grup) => {
      for (let i = 0; i < n; i++) {
        const lx = cx + (r() - .5) * w * 1.6, ly = cy + (r() - .5) * h * .5, rx = w * (.28 + r() * .32), ry = h * (.5 + r() * .5), pts = [];
        for (let k = 0; k < 16; k++) { const a = k / 16 * PI * 2, kk = .85 + r() * .25; pts.push([lx + Math.cos(a) * rx * kk, ly + Math.sin(a) * ry * kk * (Math.sin(a) > 0 ? .45 : 1)]); }
        R.fill(S(pts), lin([[0, ust], [.55, orta], [.86, alt], [1, alt]], 0, ly - ry, 0, ly + ry * .45), { dir: { fn: (x, y) => .08 * Math.sin(x * .01) }, maxR: 13, group: grup, jit: .08, aj: .4, len: 1.5, wid: .85, follow: 8 });
      }
    };
    kume(360, 150, 300, 70, 7, '#2a2448', '#4c3462', '#9a5470', 'b1');
    kume(1020, 90, 380, 60, 8, '#262243', '#41305c', '#7e4a6c', 'b2');
    kume(1700, 200, 280, 80, 7, '#34284f', '#5e3c66', '#c06a68', 'b3');
    kume(620, 365, 420, 46, 9, '#4e3462', '#9a5068', '#f09064', 'b4');
    kume(1560, 420, 300, 44, 7, '#6a4066', '#c6686a', '#ffb070', 'b5');
    kume(220, 470, 260, 30, 5, '#7a4868', '#de8068', '#ffc480', 'b6');
    // ufka yakın ince ışıklı şeritler
    for (const [x, y, w] of [[860, 540, 380], [1480, 560, 300], [420, 585, 340]]) R.fill(Ell(x, y, w, 7), '#ffd696', { dir: 0, maxR: 5, group: 'serit', jit: .04, len: 2.2, wid: .6 });
  }
  // ---------------- uzak tepeler (üç kat, hava perspektifi) ----------------
  function daglar(R) {
    R.fill(sirt(UFUK - 46, 36, .0023, 1.2), lin([[0, '#9b7896'], [1, '#c08a86']], 0, UFUK - 100, 0, UFUK), { dir: 0, maxR: 14, group: 'd1', jit: .04 });
    R.fill(sirt(UFUK - 22, 30, .0031, 4.1), lin([[0, '#6f5682'], [1, '#8f6a80']], 0, UFUK - 60, 0, UFUK + 10), { dir: 0, maxR: 12, group: 'd2', jit: .05 });
    R.fill(sirt(UFUK - 4, 16, .0042, 2.2), lin([[0, '#4c3d62'], [1, '#5e4867']], 0, UFUK - 30, 0, UFUK + 20), { dir: 0, maxR: 10, group: 'd3', jit: .05 });
  }
  // ---------------- tarla: uzakta yatay altın, yakında koyu toprak; ağacın tepesi; patika ----------------
  function tarla(R, patika) {
    const r = rng(5);
    // tarla düzlüğü: ufukta ışıkla yanan altın, öne doğru koyulaşan toprak
    R.fill(P([[-80, UFUK - 2], [2000, UFUK - 2], [2000, 1200], [-80, 1200]]), lin([[0, '#ffc77a'], [.05, '#e2a058'], [.22, '#b0703c'], [.55, '#6e4430'], [1, '#2a1c20']], 0, UFUK, 0, 1080), { dir: 0, maxR: 18, group: 'tarla', jit: .1, len: 1.8, wid: .7 });
    // uzakta ışık şeritleri (güneş tarlayı sıyırır)
    for (let i = 0; i < 9; i++) { const y = UFUK + 6 + i * i * 3.6, x = 80 + r() * 1500, w = 200 + r() * 460;
      R.fill(Ell(x, y, w, 2.5 + i * 1.4), `rgba(255,${215 - i * 9},${140 - i * 8},${.8 - i * .06})`, { dir: 0, maxR: 5, group: 'tarla', jit: .06, len: 2.4, wid: .6 }); }
    // ağacın dibinde hafif sıcak kabarma (çizgi bırakmadan)
    R.fill(Ell(1312, 748, 260, 14), '#d8955a', { dir: 0, maxR: 6, group: 'tarla', jit: .06, len: 2, wid: .6 });
    // ağacın uzun gölgesi: gövdeden bize doğru açılan koyu kama
    R.fill(P([[1290, 744], [1336, 744], [1520, 1200], [1080, 1200]]), 'rgba(40,24,40,.72)', { dir: { fn: () => Math.atan2(456, 70) }, maxR: 10, group: 'tepe', jit: .07 });
    // patika (3B yürüyüş yolunun izdüşümü): açık, sıcak; uzağa doğru incelir
    if (patika && patika.length) {
      const sol = [], sag = [];
      for (const p of patika) { sol.push([p[0] - p[2], p[1]]); sag.push([p[0] + p[2], p[1]]); }
      R.fill(P([...sol, ...sag.reverse()]), lin([[0, '#f6c886'], [.45, '#c98e56'], [1, '#6a4632']], 0, UFUK + 20, 0, 1080), { dir: { fn: (x, y) => -.35 }, maxR: 7, group: 'patika', jit: .07, follow: 4 });
    }
  }
  // ---------------- yalnız meşe: geniş kollu; taç yaprak kümelerinden; güneşe bakan kenarlar yanar, üstler gökten soğuk ışık alır ----------------
  const AGAC = { x: 1312, y: 744 };
  function agac(R) {
    const r = rng(23), tx = AGAC.x, ty = AGAC.y;
    // dallar: gövdeden kollara (çizgi darbeleri), kalınlık uca doğru azalır
    const dal = (pts, w0, w1) => { for (let i = 0; i < pts.length - 1; i++) { const w = w0 + (w1 - w0) * i / (pts.length - 1);
      R.line(c => { c.moveTo(pts[i][0], pts[i][1]); c.lineTo(pts[i + 1][0], pts[i + 1][1]); }, '#1e1520', w, { dir: 'edge', maxR: 6, group: 'govde', jit: .06 }); } };
    const kollar = [
      [[tx, ty - 150], [tx - 60, ty - 250], [tx - 190, ty - 330], [tx - 330, ty - 370]],
      [[tx, ty - 170], [tx + 70, ty - 270], [tx + 210, ty - 340], [tx + 360, ty - 360]],
      [[tx - 4, ty - 200], [tx - 20, ty - 330], [tx - 70, ty - 450]],
      [[tx + 6, ty - 210], [tx + 40, ty - 360], [tx + 110, ty - 470]],
      [[tx - 60, ty - 250], [tx - 120, ty - 410], [tx - 220, ty - 470]],
    ];
    for (const k of kollar) dal(k, 30, 9);
    // gövde: kökler tepeye yayılır
    R.fill(S([[tx - 62, ty + 8], [tx - 30, ty - 20], [tx - 26, ty - 150], [tx - 10, ty - 210], [tx + 14, ty - 214], [tx + 30, ty - 150], [tx + 30, ty - 24], [tx + 70, ty + 8], [tx, ty + 14]]),
      lin([[0, '#6a4232'], [.2, '#3a2626'], [.5, '#1e1520'], [1, '#150f18']], tx - 50, 0, tx + 40, 0), { dir: 90, maxR: 7, group: 'govde', jit: .06, follow: 3 });
    // taç: kollar boyunca yaprak kümeleri
    const kum = [];
    for (const k of kollar) for (let i = 1; i < k.length; i++) for (let j = 0; j < 3; j++) { const u = r(); kum.push([k[i - 1][0] + (k[i][0] - k[i - 1][0]) * u + (r() - .5) * 80, k[i - 1][1] + (k[i][1] - k[i - 1][1]) * u - 30 - r() * 60, 60 + r() * 70, 34 + r() * 34]); }
    for (let i = 0; i < 8; i++) kum.push([tx + (r() - .5) * 520, ty - 430 - r() * 120, 70 + r() * 60, 40 + r() * 30]);
    kum.sort((a, b) => a[1] - b[1]);
    for (const [cx, cy, rx, ry] of kum) {
      const pts = []; const n = 22;
      for (let i = 0; i < n; i++) { const a = i / n * PI * 2, k = .78 + r() * .34 + .08 * Math.sin(a * 5 + cx); pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]); }
      // güneş solda ve aşağıda: alt-sol kenar sıcak yanar; üst kenar gökten soğuk mor ışık
      const sx = Math.sign(GUNES[0] - cx) || -1;
      R.fill(S(pts), c => { const gr = c.createLinearGradient(cx + sx * rx, cy + ry, cx - sx * rx * .6, cy - ry); gr.addColorStop(0, '#e07a3c'); gr.addColorStop(.12, '#7a3a2c'); gr.addColorStop(.36, '#22161e'); gr.addColorStop(.82, '#1d1622'); gr.addColorStop(1, '#3e3250'); return gr; },
        { dir: 'edge', fallback: 20, maxR: 9, group: 'tac', type: 2, jit: .12, hgt: 1.35, aj: .8 });
    }
    // yaprak kenarı: kümelerin dış çevresine küçük lekeler (pürüzlü, yapraklı siluet)
    for (const [cx, cy, rx, ry] of kum) for (let i = 0; i < 14; i++) { const a = r() * PI * 2, x = cx + Math.cos(a) * rx * (1 + r() * .12), y = cy + Math.sin(a) * ry * (1 + r() * .14);
      R.fill(Ell(x, y, 5 + r() * 7, 3 + r() * 5, r() * PI), Math.cos(a) * Math.sign(GUNES[0] - cx) > .4 && Math.sin(a) > -.2 ? '#7a3c2c' : '#1e1620', { maxR: 3, group: 'tac', type: 2, jit: .08, hgt: 1.3 }); }
    // tacın içinde, güneşe bakan kümelerde sızan ışık: küçük sıcak lekeler (kümelerin içinde)
    for (let i = 0; i < 40; i++) { const k = kum[(r() * kum.length) | 0]; if (k[0] > GUNES[0] + 160) continue;
      R.fill(Ell(k[0] - k[2] * (.2 + r() * .5), k[1] + k[3] * (.1 + r() * .5), 4 + r() * 7, 3 + r() * 4, r() * PI), ['#ffcf7a', '#f6a85e', '#ffe6aa'][i % 3], { maxR: 3, group: 'tac', type: 2, jit: .05, hgt: 1.6 }); }
  }
  // ---------------- ön plan: koyu toprak tümsekleri; karşı ışıkta ucu yanan ot ve başak öbekleri ----------------
  function on(R) {
    const r = rng(31);
    R.fill(S([[-80, 1200], [-80, 950], [140, 972], [300, 1012], [480, 1046], [640, 1072], [760, 1200]]), '#140f17', { dir: 80, maxR: 8, group: 'onsol', jit: .08, follow: 2 });
    R.fill(S([[1260, 1200], [1480, 1060], [1680, 1004], [1860, 968], [2000, 952], [2000, 1200]]), '#120d16', { dir: 100, maxR: 8, group: 'onsag', jit: .08 });
    // ot yaprağı: sivrilen eğri şerit; dipte koyu, uçta (karşı ışık) sıcak
    const yaprak = (x0, y0, h, eg, gen, grup) => {
      const x1 = x0 + Math.sin(eg) * h, y1 = y0 - Math.cos(eg) * h, bx = x0 + Math.sin(eg * .5) * h * .5 + 6 * Math.sign(eg || 1), by = y0 - h * .55;
      R.fill(c => { c.moveTo(x0 - gen, y0); c.quadraticCurveTo(bx - gen * .5, by, x1, y1); c.quadraticCurveTo(bx + gen * .5, by, x0 + gen, y0); c.closePath(); },
        lin([[0, '#120d16'], [.65, '#2a1a22'], [.9, '#8a4a34'], [1, '#ffb466']], 0, y0, 0, y1), { dir: 'edge', maxR: 3, group: grup, jit: .06, follow: 1 });
    };
    const basak = (x, y, eg, grup) => { for (let k = 0; k < 6; k++) R.fill(Ell(x + Math.sin(eg) * k * 6, y - Math.cos(eg) * k * 6, 2, 4, eg), k < 1 ? '#e8a060' : '#7a4630', { maxR: 2, group: grup, type: 2, jit: .05, hgt: 1.4 }); };
    for (let i = 0; i < 150; i++) { const sol = i < 85, x0 = sol ? r() * 720 : 1320 + r() * 620, y0 = sol ? 1084 - r() * 50 + Math.max(0, 380 - x0) * .25 : 1084 - r() * 60, h = 50 + r() * 200, eg = (r() - .5) * .7 + (sol ? .12 : -.08);
      yaprak(x0, y0, h, eg, 2 + r() * 3.5, sol ? 'onsol' : 'onsag');
      if (r() < .12) basak(x0 + Math.sin(eg) * h, y0 - Math.cos(eg) * h, eg, sol ? 'onsol' : 'onsag'); }
  }
  g.TABLO = { gok, daglar, tarla, agac, on, GUNES, UFUK, AGAC };
})(window);
