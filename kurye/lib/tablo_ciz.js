// "Mektuplar" v2: durağan resmin katmanları (değer planlı düz resim; impasto motoru bunu fırça darbelerine çevirir).
// Klasik betik; window.TABLO verir. Her katman ayrı tuval (derinlik kayması için): gok, daglar, tarla, agac, on.
// Birim: 1920×1080 kare pikseli. Ufuk y = 700 (3B kamera bununla eşleşir: tablo.html KAMERA).
// v2 (bağımsız eleştiriden):
//   - fırça biçimi izler, uzaklıkla küçülür: gökte yatay sürütme, tarlada yakında dik kırık darbe, ufka doğru küçük yatay;
//   - güneş gövdeden ayrı (solda, alçak); disk canlı katmanda (batar); disk halka darbeyle çizilmez (hedef tahtası okunur);
//   - tacın ışığı kül pembesi ve mor gök boşlukları (turuncu lekeler köz okunuyordu);
//   - ufuk cetvel çizgisi değil: uzak çit ve ağaç öbekleri, pus;
//   - ağacın gölgesi yumuşak, taç biçimli bir göl; patika iki tekerlek izi.
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
  // tohumlu 1B gürültü (değer gürültüsü)
  const gur = (x, s = 0) => { const h = n => { const v = Math.sin(n * 127.1 + s * 311.7) * 43758.5453; return v - Math.floor(v); }; const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return h(i) + (h(i + 1) - h(i)) * u; };
  const fbm = (x, s = 0) => gur(x, s) * .55 + gur(x * 2.1, s + 3) * .3 + gur(x * 4.7, s + 7) * .15;

  const GUNES = [1010, 628];
  const UFUK = 700;

  // ---------------- gök ----------------
  function gok(R) {
    // gök: yatay sürütülmüş fırça (uzun, ince, alçak kabartma); renk tepede gece moru, ufukta altın
    R.fill(P([[-120, -120], [2040, -120], [2040, 780], [-120, 780]]), lin([[0, '#1c1a3a'], [.24, '#35294f'], [.46, '#6e3f63'], [.62, '#b46068'], [.76, '#e08c62'], [.88, '#f6b874'], [1, '#ffd89c']], 0, -120, 0, 780),
      { dir: 0, maxR: 30, type: 1, len: 2.4, wid: .6, hgt: .35, group: 'gok', jit: .05, aj: .16 });
    // güneşin çevresinde ışıma: ışıktan dışa doğru yayılan darbeler (disk ayrı, canlı katmanda)
    R.fill(Ell(GUNES[0], GUNES[1] + 20, 620, 330), rad([[0, 'rgba(255,238,196,1)'], [.14, 'rgba(255,220,150,.9)'], [.42, 'rgba(250,178,104,.42)'], [1, 'rgba(240,150,96,0)']], GUNES[0], GUNES[1] + 20, 620),
      { dir: { radial: GUNES }, maxR: 18, type: 1, len: 2, wid: .6, hgt: .3, group: 'gok', jit: .04 });
    const r = rng(17);
    // tepe bulutları: yumuşak kütleler, alt kenarları gülden ışık alır; yatay sürütme
    const kume = (cx, cy, w, h, n, ust, orta, alt, grup) => {
      for (let i = 0; i < n; i++) {
        const lx = cx + (r() - .5) * w * 1.7, ly = cy + (r() - .5) * h * .6, rx = w * (.24 + r() * .3), ry = h * (.45 + r() * .5), pts = [];
        for (let k = 0; k < 20; k++) { const a = k / 20 * PI * 2, kk = .8 + .35 * fbm(k * .9 + i * 7, cx) ; pts.push([lx + Math.cos(a) * rx * kk, ly + Math.sin(a) * ry * kk * (Math.sin(a) > 0 ? .4 : 1)]); }
        R.fill(S(pts), lin([[0, ust], [.55, orta], [.88, alt], [1, alt]], 0, ly - ry, 0, ly + ry * .4), { dir: { fn: (x, y) => .06 * Math.sin(x * .013 + y * .02) }, maxR: 14, type: 1, len: 2.6, wid: .55, hgt: .4, group: grup, jit: .07, aj: .22 });
      }
    };
    kume(330, 140, 300, 66, 7, '#28233f', '#44305a', '#8a4e6a', 'b1');
    kume(1050, 86, 400, 56, 9, '#24203d', '#3c2d55', '#744866', 'b2');
    kume(1720, 190, 280, 76, 7, '#30264a', '#563a62', '#b06468', 'b3');
    // ince bulut tabakaları: düzensiz kalınlık, yırtık uçlar, alt kenar ışıkta (mercek biçimi değil)
    const tabaka = (x0, x1, y, th, s, ust, alt, grup) => {
      const ustK = [], altK = [], n = 48;
      for (let i = 0; i <= n; i++) {
        const u = i / n, x = x0 + (x1 - x0) * u;
        const zarf = Math.pow(Math.sin(PI * u), .5) * (.45 + .9 * fbm(u * 6, s)) * (fbm(u * 17, s + 5) > .28 ? 1 : .15);
        ustK.push([x, y - th * zarf * (.7 + .5 * fbm(u * 9, s + 2)) + 6 * Math.sin(u * 7 + s)]);
        altK.push([x, y + th * .45 * zarf * (.6 + .6 * fbm(u * 11, s + 9)) + 6 * Math.sin(u * 7 + s)]);
      }
      R.fill(P([...ustK, ...altK.reverse()]), lin([[0, ust], [.62, ust], [1, alt]], 0, y - th, 0, y + th * .45), { dir: { fn: (x, y2) => -.03 + .05 * Math.sin(x * .004 + s) }, maxR: 6, type: 1, len: 3, wid: .5, hgt: .35, group: grup, jit: .06, aj: .1 });
    };
    tabaka(-80, 1100, 352, 34, 1, '#6a3c5e', '#e68a66', 't1');
    tabaka(1180, 2000, 410, 26, 2, '#8a4a62', '#f4a06a', 't2');
    tabaka(120, 860, 470, 18, 3, '#9a5464', '#ffb878', 't3');
    tabaka(560, 1500, 545, 9, 4, '#c87a6c', '#ffd496', 't4');
    tabaka(1380, 2020, 585, 8, 5, '#c07068', '#ffc886', 't5');
  }
  // ---------------- uzak tepeler: pusun içinde, güneşin altında alçalır ----------------
  function daglar(R) {
    const sirt = (y0, A, f, ph, gk) => { const pts = [[-120, UFUK + 40]]; for (let x = -120; x <= 2040; x += 24) {
      const dus = 1 - .75 * Math.exp(-Math.pow((x - GUNES[0]) / 360, 2));    // güneşin altında tepe alçalır (disk tepeye batar)
      pts.push([x, y0 - A * dus * (fbm(x * f, ph) * 1.2 - .1)]); } pts.push([2040, UFUK + 40]); return P(pts); };
    R.fill(sirt(UFUK - 12, 70, .0022, 1.2), lin([[0, '#b07a88'], [1, '#d89a88']], 0, UFUK - 80, 0, UFUK + 20), { dir: 0, maxR: 10, type: 1, len: 2.4, wid: .6, hgt: .3, group: 'd1', jit: .04 });
    R.fill(sirt(UFUK - 2, 44, .0034, 4.1), lin([[0, '#8a6684'], [1, '#b08088']], 0, UFUK - 50, 0, UFUK + 30), { dir: 0, maxR: 8, type: 1, len: 2.4, wid: .6, hgt: .3, group: 'd2', jit: .05 });
  }
  // ---------------- tarla ----------------
  function tarlaGolge(R) {
  // ağacın gölgesi: gövde gölgesi incecik başlar, taç gölgesi önde yumuşak, loblu bir göl olur (güneşten uzağa: sağa ve bize)
  { const gk = [], n = 40, A = [1318, 748], B = [1780, 1230];
    for (let i = 0; i <= n; i++) { const u = i / n, x = A[0] + (B[0] - A[0]) * u, y = A[1] + (B[1] - A[1]) * Math.pow(u, 1.15);
      const gen = (u < .12 ? 6 + 40 * u : 11 + 330 * Math.pow((u - .12) / .88, .9)), lob = .55 + .9 * fbm(u * 6, 3), lob2 = .55 + .9 * fbm(u * 6, 11);
      gk.push([x - gen * lob + 14 * Math.sin(u * 41), y, x + gen * 1.1 * lob2 + 14 * Math.sin(u * 37 + 1), y]); }
    R.fill(S([...gk.map(p => [p[0], p[1]]), ...gk.reverse().map(p => [p[2], p[3]])]), 'rgba(52,30,52,.62)',
      { dir: { fn: () => Math.atan2(482, 462) }, maxR: 9, type: 1, len: 2, wid: .6, hgt: .2, group: 'tgolge', jit: .08, alpha: .8 }); }
  }
  function tarla(R, patika, o = {}) {
    const r = rng(5);
    // uzak çit ve ağaç öbekleri: ufku kırar (cetvel çizgisi yok); pusun içinde gül-mor
    const cit = [[-120, UFUK + 30]];
    for (let x = -120; x <= 2040; x += 6) { const ag = Math.max(0, fbm(x * .011, 21) - .52) * 60 + Math.max(0, fbm(x * .05, 4) - .6) * 18; cit.push([x, UFUK - 1 - ag - 2.5 * fbm(x * .2, 9)]); }
    cit.push([2040, UFUK + 30]);
    R.fill(P(cit), c => { const gr = c.createLinearGradient(0, 0, 1920, 0); gr.addColorStop(0, '#5e4060'); gr.addColorStop(.4, '#8a5866'); gr.addColorStop(.53, '#c8826e'); gr.addColorStop(.66, '#8a5866'); gr.addColorStop(1, '#5a3e5e'); return gr; },
      { dir: 0, maxR: 3, type: 1, len: 2, wid: .7, hgt: .3, group: 'cit', jit: .05 });
    // tarla düzlüğü: ufukta ışıkla yanan altın, öne doğru koyulaşan toprak; darbe boyu uzaklıkla büyür, yakında dikleşir
    const tarlaRenk = lin([[0, '#ffcf88'], [.06, '#eaa65e'], [.22, '#bc7a42'], [.5, '#7c4c32'], [1, '#2e1e22']], 0, UFUK + 4, 0, 1080);
    R.fill(P([[-120, UFUK + 4], [2040, UFUK + 4], [2040, 740], [-120, 740]]), tarlaRenk, { dir: 0, maxR: 3.5, type: 1, len: 3, wid: .45, hgt: .3, group: 'tarla', jit: .08, aj: .08 });
    R.fill(P([[-120, 740], [2040, 740], [2040, 830], [-120, 830]]), tarlaRenk, { dir: { fn: (x, y) => -.15 - (y - 740) / 90 * .55 }, maxR: 8, type: 1, len: 2.2, wid: .55, hgt: .45, group: 'tarla', jit: .1, aj: .3 });
    R.fill(P([[-120, 830], [2040, 830], [2040, 1220], [-120, 1220]]), tarlaRenk, { dir: { fn: (x, y) => -PI / 2 + .25 * Math.sin(x * .02) }, maxR: 16, type: 1, len: 2.4, wid: .42, hgt: .7, group: 'tarla', jit: .12, aj: .35 });
    // pus: ufkun üstünde güneşin altında yanan ışık (tepelerle tarlayı birbirine eritir)
    R.fill(Ell(GUNES[0], UFUK + 6, 760, 26), rad([[0, 'rgba(255,226,160,.95)'], [.5, 'rgba(250,196,124,.55)'], [1, 'rgba(240,170,110,0)']], GUNES[0], UFUK + 6, 760),
      { dir: 0, maxR: 4, type: 1, len: 3, wid: .45, hgt: .25, group: 'tarla', jit: .05, alpha: .85 });
    // güneşin sıyırdığı ışık şeritleri: düzensiz, kırık
    for (let i = 0; i < 10; i++) { const y = UFUK + 8 + i * i * 3.2, x = 140 + r() * 1600, w = 160 + r() * 420, pts = [];
      for (let k = 0; k <= 16; k++) { const u = k / 16; pts.push([x - w + 2 * w * u, y - (1.5 + i * .9) * Math.sin(PI * u) * (.5 + fbm(u * 5, i))]); }
      for (let k = 16; k >= 0; k--) { const u = k / 16; pts.push([x - w + 2 * w * u, y + (1.5 + i * .9) * Math.sin(PI * u) * (.5 + fbm(u * 5, i + 20))]); }
      R.fill(P(pts), `rgba(255,${214 - i * 8},${146 - i * 8},${.75 - i * .05})`, { dir: 0, maxR: 4, type: 1, len: 3, wid: .5, hgt: .3, group: 'tarla', jit: .06 }); }
    if (o.golge !== false) tarlaGolge(R);   // Van Gogh: ağaçsız planlarda gölge ayrı katman (tek koyu tümsek taze mezar okunuyordu)
    // patika: iki tekerlek izi ve arada otlu sırt; kenarlar düzensiz
    if (patika && patika.length) {
      const yol = (k0, k1, renk, grup, pr) => { const sol = [], sag = [];
        patika.forEach((p, i) => { const n1 = 1 + .38 * (fbm(i * .45, k0 * 10 + 3) - .5); sol.push([p[0] + p[2] * k0 * n1, p[1]]); sag.push([p[0] + p[2] * k1 * n1, p[1]]); });
        R.fill(P([...sol, ...sag.reverse()]), renk, { dir: { fn: (x, y) => -.35 }, maxR: 7, type: 1, len: 2, wid: .6, hgt: .5, group: grup, jit: .08, follow: 4, ...pr }); };
      yol(-1, 1, lin([[0, '#f2c486'], [.45, '#c08a56'], [1, '#6a4632']], 0, UFUK + 20, 0, 1080), 'patika');
      // ortadaki otlu sırt: kesik kesik ve genişliği değişen yamalar (cetvelle çizilmiş iki paralel iz okunuyordu)
      for (let k = 0; k < patika.length - 2; k += 2) { const p0 = patika[k], p1 = patika[Math.min(patika.length - 1, k + 2)];
        if (fbm(k * .37, 8) < .35) continue; const w0 = .12 + .3 * fbm(k * .5, 5), w1 = .12 + .3 * fbm(k * .5 + .5, 5), o0 = (fbm(k * .3, 6) - .5) * .4;
        R.fill(P([[p0[0] + p0[2] * (o0 - w0), p0[1]], [p1[0] + p1[2] * (o0 - w1), p1[1]], [p1[0] + p1[2] * (o0 + w1), p1[1]], [p0[0] + p0[2] * (o0 + w0), p0[1]]]),
          lin([[0, '#c8935a'], [.45, '#8a5a3a'], [1, '#3e2a26']], 0, UFUK + 20, 0, 1080), { dir: { fn: () => -.35 }, maxR: 6, type: 1, len: 2, wid: .6, hgt: .5, group: 'patika', jit: .1 }); }
    }
  }
  // ---------------- yalnız meşe: geniş kollu; taç yaprak kümelerinden; ışık kenarları kül pembesi ----------------
  const AGAC = { x: 1312, y: 744 }, KUM = [];
  function agac(R) {
    const r = rng(23), tx = AGAC.x, ty = AGAC.y;
    const dal = (pts, w0, w1) => { for (let i = 0; i < pts.length - 1; i++) { const w = w0 + (w1 - w0) * i / (pts.length - 1);
      R.line(c => { c.moveTo(pts[i][0], pts[i][1]); c.lineTo(pts[i + 1][0], pts[i + 1][1]); }, '#22161f', w, { dir: 'edge', maxR: 6, type: 1, group: 'govde', jit: .06 }); } };
    const kollar = [
      [[tx, ty - 150], [tx - 60, ty - 250], [tx - 190, ty - 330], [tx - 330, ty - 370]],
      [[tx, ty - 170], [tx + 70, ty - 270], [tx + 210, ty - 340], [tx + 360, ty - 360]],
      [[tx - 4, ty - 200], [tx - 20, ty - 330], [tx - 70, ty - 450]],
      [[tx + 6, ty - 210], [tx + 40, ty - 360], [tx + 110, ty - 470]],
      [[tx - 60, ty - 250], [tx - 120, ty - 410], [tx - 220, ty - 470]],
    ];
    for (const k of kollar) dal(k, 30, 9);
    // gövde: güneşe bakan sol kenarda ince sıcak kenar ışığı
    R.fill(S([[tx - 62, ty + 8], [tx - 30, ty - 20], [tx - 26, ty - 150], [tx - 10, ty - 210], [tx + 14, ty - 214], [tx + 30, ty - 150], [tx + 30, ty - 24], [tx + 70, ty + 8], [tx, ty + 14]]),
      lin([[0, '#c27a4e'], [.1, '#6a3e30'], [.26, '#2c1c22'], [.6, '#1e1520'], [1, '#18111b']], tx - 34, 0, tx + 40, 0), { dir: 90, maxR: 6, type: 1, group: 'govde', jit: .06, follow: 3, len: 2.2, wid: .5 });
    // taç: kollar boyunca yaprak kümeleri
    const kum = KUM; kum.length = 0;
    for (const k of kollar) for (let i = 1; i < k.length; i++) for (let j = 0; j < 3; j++) { const u = r(); kum.push([k[i - 1][0] + (k[i][0] - k[i - 1][0]) * u + (r() - .5) * 80, k[i - 1][1] + (k[i][1] - k[i - 1][1]) * u - 30 - r() * 60, 60 + r() * 70, 34 + r() * 34]); }
    for (let i = 0; i < 8; i++) kum.push([tx + (r() - .5) * 520, ty - 430 - r() * 120, 70 + r() * 60, 40 + r() * 30]);
    kum.sort((a, b) => a[1] - b[1]);
    for (const [cx, cy, rx, ry] of kum) {
      const pts = []; const n = 22;
      for (let i = 0; i < n; i++) { const a = i / n * PI * 2, k = .78 + r() * .34 + .08 * Math.sin(a * 5 + cx); pts.push([cx + Math.cos(a) * rx * k, cy + Math.sin(a) * ry * k]); }
      // güneş solda ve aşağıda: alt-sol kenar kül pembesi yanar (doygun turuncu değil); üst kenar gökten soğuk mor ışık
      const sx = Math.sign(GUNES[0] - cx) || -1;
      R.fill(S(pts), c => { const gr = c.createLinearGradient(cx + sx * rx, cy + ry, cx - sx * rx * .6, cy - ry); gr.addColorStop(0, '#8e5a66'); gr.addColorStop(.12, '#4e3040'); gr.addColorStop(.36, '#24182a'); gr.addColorStop(.8, '#20182a'); gr.addColorStop(1, '#40344e'); return gr; },
        { dir: 'edge', fallback: -25, maxR: 8, group: 'tac', type: 1, len: 1.5, wid: .7, jit: .14, hgt: .55, aj: .9, follow: 3 });
    }
    // yaprak kenarı: kümelerin dış çevresine küçük lekeler (pürüzlü, yapraklı siluet)
    for (const [cx, cy, rx, ry] of kum) for (let i = 0; i < 14; i++) { const a = r() * PI * 2, x = cx + Math.cos(a) * rx * (1 + r() * .12), y = cy + Math.sin(a) * ry * (1 + r() * .14);
      R.fill(Ell(x, y, 5 + r() * 7, 3 + r() * 5, r() * PI), Math.cos(a) * Math.sign(GUNES[0] - cx) > .4 && Math.sin(a) > -.2 ? '#5a3848' : '#20172a', { maxR: 3, group: 'tac', type: 1, len: 1.4, wid: .7, jit: .08, hgt: .5, dir: 'edge' }); }
    // gök boşlukları: tacın içinden görünen gök (arkadaki gökün rengi: gül-mor; köz gibi turuncu değil)
    for (let i = 0; i < 14; i++) { const k = kum[(r() * kum.length) | 0];
      const x = k[0] + (r() - .5) * k[2] * .8, y = k[1] + (r() - .5) * k[3] * .6, gy = Math.max(0, Math.min(1, (y + 120) / 900));
      const renk = gy < .5 ? '#5a3e66' : gy < .62 ? '#8e5470' : '#c27a74';
      R.fill(Ell(x, y, 3 + r() * 5, 2 + r() * 4, r() * PI), renk, { maxR: 3, group: 'tac', type: 1, len: 1.3, wid: .8, jit: .05, hgt: .3 }); }
  }
  // ---------------- ön plan: koyu toprak tümsekleri; karşı ışıkta ucu yanan ot öbekleri ----------------
  function on(R) {
    const r = rng(31);
    R.fill(S([[-80, 1200], [-80, 950], [140, 972], [300, 1012], [480, 1046], [640, 1072], [760, 1200]]), '#160f18', { dir: 80, maxR: 8, type: 1, group: 'onsol', jit: .08, follow: 2 });
    R.fill(S([[1260, 1200], [1480, 1060], [1680, 1004], [1860, 968], [2000, 952], [2000, 1200]]), '#140d17', { dir: 100, maxR: 8, type: 1, group: 'onsag', jit: .08 });
    const yaprak = (x0, y0, h, eg, gen, grup) => {
      const x1 = x0 + Math.sin(eg) * h, y1 = y0 - Math.cos(eg) * h, bx = x0 + Math.sin(eg * .5) * h * .5 + 6 * Math.sign(eg || 1), by = y0 - h * .55;
      R.fill(c => { c.moveTo(x0 - gen, y0); c.quadraticCurveTo(bx - gen * .5, by, x1, y1); c.quadraticCurveTo(bx + gen * .5, by, x0 + gen, y0); c.closePath(); },
        lin([[0, '#140d16'], [.65, '#2a1a22'], [.9, '#7a4434'], [1, '#e8a466']], 0, y0, 0, y1), { dir: 'edge', maxR: 3, type: 1, group: grup, jit: .06, follow: 1 });
    };
    const basak = (x, y, eg, grup) => { for (let k = 0; k < 6; k++) R.fill(Ell(x + Math.sin(eg) * k * 6, y - Math.cos(eg) * k * 6, 2, 4, eg), k < 1 ? '#d89058' : '#6a3e2c', { maxR: 2, group: grup, type: 2, jit: .05, hgt: 1.1 }); };
    for (let i = 0; i < 150; i++) { const sol = i < 85, x0 = sol ? r() * 720 : 1320 + r() * 620, y0 = sol ? 1084 - r() * 50 + Math.max(0, 380 - x0) * .25 : 1084 - r() * 60, h = 50 + r() * 200, eg = (r() - .5) * .7 + (sol ? .12 : -.08);
      yaprak(x0, y0, h, eg, 2 + r() * 3.5, sol ? 'onsol' : 'onsag');
      if (r() < .12) basak(x0 + Math.sin(eg) * h, y0 - Math.cos(eg) * h, eg, sol ? 'onsol' : 'onsag'); }
  }
  g.TABLO = { gok, daglar, tarla, tarlaGolge, agac, on, GUNES, UFUK, AGAC, KUM, fbm };
})(window);
