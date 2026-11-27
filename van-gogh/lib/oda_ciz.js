// Van Gogh: Theo'nun Paris odası (gece, lamba). Değer planlı düz resim; tablo motoru darbelere çevirir, grisaille basılır.
// Kamera: göz hizası 1.5 m, düz bakış (ufuk y = 540), dikey görüş 40° (ODAK 1483). Arka duvar z = -4.2.
// Renk yok: yalnız Vincent'in tablosu renklidir (oda.html'de gerçek tablo fotoğrafı olarak basılır).
// Hassasiyet: pencere kayıtları yalnız dikey (haç); kemer, kandil, haç biçimli nesne yok; ay küçük ve halkasız.
'use strict';
(function (g) {
  const PI = Math.PI;
  const rng = s => () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
  const P = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
  const Ell = (x, y, rx, ry, r = 0) => c => { c.moveTo(x + rx * Math.cos(r), y + rx * Math.sin(r)); c.ellipse(x, y, rx, ry, r, 0, PI * 2); };
  const lin = (st, x0, y0, x1, y1) => c => { const gr = c.createLinearGradient(x0, y0, x1, y1); for (const [k, col] of st) gr.addColorStop(k, col); return gr; };
  const rad = (st, x, y, r) => c => { const gr = c.createRadialGradient(x, y, 0, x, y, r); for (const [k, col] of st) gr.addColorStop(k, col); return gr; };
  const ODAK = 540 / Math.tan(20 * PI / 180);
  const ekr = (x, y, z) => [960 + x / -z * ODAK, 540 + (1.5 - y) / -z * ODAK];
  const LAMBA = ekr(.62, 1.12, -3.0);           // lamba camı (ışık kaynağı)
  const SOVALE = { x: .32, y: 1.3, z: -3.45, gen: .34, yuk: .43 };   // tablo (Hasır Şapkalı Otoportre, 41×32 cm, çerçeveyle büyütüldü)
  const tabloKose = () => { const a = ekr(SOVALE.x - SOVALE.gen / 2, SOVALE.y + SOVALE.yuk / 2, SOVALE.z), b = ekr(SOVALE.x + SOVALE.gen / 2, SOVALE.y - SOVALE.yuk / 2, SOVALE.z); return [a[0], a[1], b[0] - a[0], b[1] - a[1]]; };

  // arka duvar: lambanın ışığı duvarda yuvarlak bir sıcaklık (grisaille'de açık gri); köşeler karanlık; dik fırça
  function duvar(R) {
    const [lx, ly] = LAMBA;
    R.fill(P([[-40, -40], [1960, -40], [1960, 1120], [-40, 1120]]), rad([[0, '#d8c8b0'], [.25, '#a89478'], [.6, '#5a4c40'], [1, '#221c1c']], lx, ly - 40, 1250),
      { dir: 90, maxR: 26, type: 1, len: 2.2, wid: .6, hgt: .35, group: 'duvar', jit: .06, aj: .18 });
    // duvar kâğıdı şeridi yok: düzenli dik şerit parmaklık (hapishane) okunuyordu; duvar yalnız sıva fırçası
    // süpürgelik ve döşeme
    const tY = ekr(0, 0, -4.2)[1];
    R.fill(P([[-40, tY - 40], [1960, tY - 40], [1960, tY], [-40, tY]]), '#2c2420', { dir: 0, maxR: 6, type: 1, len: 3, wid: .5, hgt: .4, group: 'supurge', jit: .05 });
    R.fill(P([[-40, tY], [1960, tY], [1960, 1120], [-40, 1120]]), lin([[0, '#3a3028'], [1, '#14100e']], 0, tY, 0, 1100), { dir: 0, maxR: 10, type: 1, len: 3, wid: .5, hgt: .4, group: 'zemin', jit: .08 });
  }
  // pencere: gece; Montmartre çatıları ve bacalar; kayıtlar yalnız dikey; perdeler
  function pencere(R) {
    const x0 = 150, x1 = 560, y0 = 120, y1 = 780, r = rng(9);
    R.fill(P([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]), lin([[0, '#262a36'], [.6, '#3a3e4a'], [1, '#4a4a50']], 0, y0, 0, y1), { dir: 0, maxR: 14, type: 1, len: 2.4, wid: .6, hgt: .3, group: 'gece', jit: .05 });
    // ay: küçük, yumuşak, halkasız (yatay sürütme)
    R.fill(Ell(470, 230, 16, 16), '#d8d6cc', { dir: 0, maxR: 4, type: 1, len: 2.4, wid: .6, hgt: .2, group: 'ay', jit: .03 });
    // çatılar ve bacalar (dik dikdörtgen bacalar; sivri kule, kubbe, haç yok)
    const cat = [[x0, y1]]; let x = x0;
    while (x < x1) { const w = 40 + r() * 70, h = 520 + r() * 120; cat.push([x, h]); if (r() < .5) { const bx = x + w * .3; cat.push([bx, h], [bx, h - 30 - r() * 20], [bx + 12, h - 30 - r() * 20], [bx + 12, h]); } x += w; cat.push([Math.min(x, x1), h]); }
    cat.push([x1, y1]);
    R.fill(P(cat), '#15161c', { dir: 0, maxR: 6, type: 1, len: 2, wid: .6, hgt: .3, group: 'catilar', jit: .05 });
    // birkaç sıcak pencere ışığı uzakta (küçük dikdörtgen)
    for (let i = 0; i < 3; i++) { const wx = x0 + 60 + r() * (x1 - x0 - 120), wy = 700 + r() * 50; R.fill(P([[wx, wy], [wx + 7, wy], [wx + 7, wy + 9], [wx, wy + 9]]), '#6e6656', { maxR: 2, type: 1, dir: 0, len: 1, wid: 1, group: 'pencereisigi' + i, jit: .02, hgt: .1 }); }
    // çerçeve ve iki dik kayıt
    for (const [a, b] of [[x0 - 18, x0], [x1, x1 + 18], [x0 + (x1 - x0) / 3 - 5, x0 + (x1 - x0) / 3 + 5], [x0 + 2 * (x1 - x0) / 3 - 5, x0 + 2 * (x1 - x0) / 3 + 5]])
      R.fill(P([[a, y0 - 18], [b, y0 - 18], [b, y1 + 18], [a, y1 + 18]]), '#2a2420', { dir: 90, maxR: 4, type: 1, len: 2.4, wid: .5, hgt: .5, group: 'kasa', jit: .05 });
    R.fill(P([[x0 - 30, y0 - 30], [x1 + 30, y0 - 30], [x1 + 30, y0 - 10], [x0 - 30, y0 - 10]]), '#2a2420', { dir: 0, maxR: 4, type: 1, group: 'kasa', jit: .05 });
    R.fill(P([[x0 - 30, y1 + 10], [x1 + 30, y1 + 10], [x1 + 40, y1 + 34], [x0 - 40, y1 + 34]]), '#3a322a', { dir: 0, maxR: 4, type: 1, group: 'kasa', jit: .05 });
    // perdeler: ağır, dik kıvrımlar
    for (const [a, b] of [[x0 - 90, x0 + 20], [x1 - 20, x1 + 90]]) {
      const pts = [[a, y0 - 60]]; for (let yy = y0 - 60; yy <= 1000; yy += 40) pts.push([a + 8 * Math.sin(yy * .03), yy]); pts.push([b, 1000]);
      for (let yy = 1000; yy >= y0 - 60; yy -= 40) pts.push([b + 6 * Math.sin(yy * .025 + 1), yy]);
      R.fill(P(pts), lin([[0, '#1c1614'], [.5, '#3c302a'], [1, '#1a1412']], a, 0, b, 0), { dir: 90, maxR: 8, type: 1, len: 2.6, wid: .5, hgt: .5, group: 'perde', jit: .06 }); }
  }
  // gündüz penceresi (sabah ve kış planları): soluk gök, açık gri çatılar; aynı kasa
  function pencereGun(R) {
    const x0 = 150, x1 = 560, y0 = 120, y1 = 780, r = rng(9);
    R.fill(P([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]), lin([[0, '#d8d4c8'], [.7, '#b8b2a4'], [1, '#a29a8a']], 0, y0, 0, y1), { dir: 0, maxR: 14, type: 1, len: 2.4, wid: .6, hgt: .3, group: 'gun', jit: .05 });
    const cat = [[x0, y1]]; let x = x0;
    while (x < x1) { const w = 40 + r() * 70, h = 520 + r() * 120; cat.push([x, h]); if (r() < .5) { const bx = x + w * .3; cat.push([bx, h], [bx, h - 30 - r() * 20], [bx + 12, h - 30 - r() * 20], [bx + 12, h]); } x += w; cat.push([Math.min(x, x1), h]); }
    cat.push([x1, y1]);
    R.fill(P(cat), '#6a645c', { dir: 0, maxR: 6, type: 1, len: 2, wid: .6, hgt: .3, group: 'catilar', jit: .05 });
  }
  // masa, lamba gövdesi, mektup yığını, şövale ve tablonun çerçevesi (tablonun kendisi renkli fotoğraf olarak üstüne basılır)
  function esya(R) {
    const r = rng(21), [lx, ly] = LAMBA;
    // masa: üst yüzey ve ön kenar (z -3.0…-3.7, x .2…1.6)
    const a = ekr(.18, .76, -3.0), b = ekr(1.7, .76, -3.0), c = ekr(1.7, .76, -3.75), d = ekr(.18, .76, -3.75), e = ekr(.18, .7, -3.0), f = ekr(1.7, .7, -3.0);
    R.fill(P([a, b, c, d]), lin([[0, '#8a7458'], [.5, '#5a4836'], [1, '#2a2018']], lx, a[1], 1900, c[1]), { dir: 0, maxR: 8, type: 1, len: 2.6, wid: .5, hgt: .5, group: 'masa', jit: .06 });
    R.fill(P([a, b, f, e]), '#1e1812', { dir: 0, maxR: 5, type: 1, len: 3, wid: .5, hgt: .4, group: 'masaon', jit: .05 });
    R.fill(P([e, f, [f[0], 1120], [e[0], 1120]]), '#120e0c', { dir: 90, maxR: 10, type: 1, group: 'masaalt', jit: .05 });
    // mektup yığını: üst üste zarflar (açık, kâğıt; ışıkta)
    for (let i = 0; i < 9; i++) { const zx = .95 + (r() - .5) * .18, zz = -3.25 - r() * .2, h = .76 + i * .012, w = .22, dd = .12, rot = (r() - .5) * .3;
      const k = [[-w / 2, -dd / 2], [w / 2, -dd / 2], [w / 2, dd / 2], [-w / 2, dd / 2]].map(([u, v]) => ekr(zx + u * Math.cos(rot) - v * Math.sin(rot), h, zz + u * Math.sin(rot) + v * Math.cos(rot)));
      R.fill(P(k), i % 3 ? '#d4c8b0' : '#c2b49a', { dir: 0, maxR: 4, type: 1, len: 2, wid: .6, hgt: .5, group: 'mektup' + i, jit: .04 }); }
    // açık mektup (masada, lambaya yakın), üzerinde çizgiler yazı değil: ince yatay darbe
    const m = [[.55, -3.15], [.85, -3.1], [.82, -3.4], [.5, -3.42]].map(([x, z]) => ekr(x, .765, z));
    R.fill(P(m), '#e4dac4', { dir: 0, maxR: 4, type: 1, len: 2.4, wid: .5, hgt: .3, group: 'acikmektup', jit: .03 });
    // gaz lambası: geniş taban, ince gövde, cam hazne, ince baca (ayaklı kâse biçimi urn okunuyordu)
    const tb = ekr(.62, .77, -3.0), gv = ekr(.62, .92, -3.0), hz = ekr(.62, .99, -3.0), bc = ekr(.62, 1.2, -3.0);
    R.fill(Ell(tb[0], tb[1] - 5, 38, 9), '#2e241c', { dir: 0, maxR: 4, type: 1, group: 'lamba', jit: .04 });
    R.fill(P([[tb[0] - 6, tb[1] - 8], [tb[0] + 6, tb[1] - 8], [gv[0] + 5, gv[1]], [gv[0] - 5, gv[1]]]), '#3a2e24', { dir: 90, maxR: 3, type: 1, group: 'lamba', jit: .04 });
    R.fill(Ell(hz[0], hz[1], 26, 18), '#4e4032', { dir: 0, maxR: 4, type: 1, group: 'lamba', jit: .04 });
    R.fill(P([[bc[0] - 9, hz[1] - 14], [bc[0] + 9, hz[1] - 14], [bc[0] + 7, bc[1]], [bc[0] - 7, bc[1]]]), '#9a8e78', { dir: 90, maxR: 3, type: 1, hgt: .3, group: 'baca', jit: .03 });
    // şövale: üç ince ayak (dik ve hafif eğik; kesişme haç okunmasın diye üst birleşim tek noktada değil)
    const [tx, ty, tw, th] = tabloKose();
    const ayak = (x0, y0, x1, y1, w) => R.fill(P([[x0 - w, y0], [x0 + w, y0], [x1 + w, y1], [x1 - w, y1]]), '#3a2c20', { dir: 'edge', maxR: 3, type: 1, group: 'sovale', jit: .05 });
    ayak(tx + tw * .2, ty - 30, tx + tw * .05, 1120, 5); ayak(tx + tw * .8, ty - 30, tx + tw * .95, 1120, 5);
    R.fill(P([[tx - 14, ty + th + 4], [tx + tw + 14, ty + th + 4], [tx + tw + 14, ty + th + 16], [tx - 14, ty + th + 16]]), '#3a2c20', { dir: 0, maxR: 3, type: 1, group: 'sovale', jit: .05 });
    // çerçeve (tablo fotoğrafı içine basılır)
    R.fill(P([[tx - 12, ty - 12], [tx + tw + 12, ty - 12], [tx + tw + 12, ty + th + 12], [tx - 12, ty + th + 12]]), '#4a3a28', { dir: 'edge', maxR: 3, type: 1, hgt: .8, group: 'cerceve', jit: .05 });
  }
  g.ODA = { duvar, pencere, pencereGun, esya, LAMBA, SOVALE, tabloKose, ekr, ODAK };
})(window);
