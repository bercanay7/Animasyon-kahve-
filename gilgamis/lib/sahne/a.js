// A: kanca (A01–A05) ve bölüm kartları. Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at;   // çapanın çekim içi zamanı
  // gölet suyu (y0'dan aşağı); figürün önüne yeniden çizilebilir (suya giren beden)
  window.GOLET_SU = (R, y0, x0 = -900, x1 = 2900) => {
    R.b.fillStyle = gv(.14); R.b.fillRect(x0, y0, x1 - x0, 1600 - y0); R.m.fillStyle = '#41639E'; R.m.fillRect(x0, y0, x1 - x0, 1600 - y0);
    R.d.fillStyle = 'rgb(128,128,128)'; R.d.fillRect(x0, y0, x1 - x0, 1600 - y0);
    for (let i = 0; i < 9; i++) { const y = y0 + 50 + i * 48, fz = (FIG_T || 0) * .6 + i; R.d.strokeStyle = dv(.4); R.d.lineWidth = 3; R.d.beginPath(); for (let x = x0; x < x1; x += 20) { const yy = y + Math.sin(x / 90 + fz) * 6; x === x0 ? R.d.moveTo(x, yy) : R.d.lineTo(x, yy); } R.d.stroke(); }
    FIG.cizgi(R, [[x0, y0], [x1, y0]], 4, -.7);
  };
  // ortak: gölet başı (A01 ve G06–G07 aynı set)
  window.SAHNE_GOLET = (R, st, o) => {
    SET.zemin(R);
    DK.tugla(R, -900, -300, 2900, 330, { z: .28, bw: 110, bh: 40, lw: 2 });
    SET.yer(R, -900, 2900, 330, { z: .3, cimen: true, kal: 30 });
    DK.hurma(R, 150, 360, 340, { z: .46 }); DK.hurma(R, 1720, 360, 300, { z: .46, egri: 30 });
    // su (lacivert), kıyı
    GOLET_SU(R, 640);
    R.b.fillStyle = gv(.4); R.b.beginPath(); R.b.moveTo(-900, 640); for (let x = -900; x < 2900; x += 60) R.b.lineTo(x, 610 + Math.sin(x / 210) * 14); R.b.lineTo(2900, 650); R.b.lineTo(-900, 650); R.b.fill();
    cizgi2(R, -900, 2900, 640);
  };
  const cizgi2 = (R, x0, x1, y) => FIG.cizgi(R, [[x0, y], [x1, y]], 4, -.7);

  // A01: bitki elde (kapak A'nın vaadi); "yılana"da yılan sudan yükselir, "kaptırdı"da kapar ve kaçar
  sahne('A01a', 'A01', 'golet', 'yakin', (R, st) => {
    const tY = rel(st, 'A01@yılana'), tK = rel(st, 'A01@kaptırdı');
    R.cam(960 + st.lt * 6, 540, 1);
    SET.zemin(R);
    DK.tugla(R, -400, -400, 2400, 560, { z: .26, bw: 200, bh: 80, lw: 4 });
    // su (lacivert) önde
    R.b.fillStyle = gv(.14); R.b.fillRect(-400, 760, 2800, 600); R.m.fillStyle = '#41639E'; R.m.fillRect(-400, 760, 2800, 600);
    for (let i = 0; i < 6; i++) { const y = 800 + i * 50, fz = st.lt * .7 + i; R.d.strokeStyle = dv(.4); R.d.lineWidth = 5; R.d.beginPath(); for (let x = -400; x < 2400; x += 24) { const yy = y + Math.sin(x / 120 + fz) * 8; x === -400 ? R.d.moveTo(x, yy) : R.d.lineTo(x, yy); } R.d.stroke(); }
    const kp = clamp((st.lt - tK) / .5);
    const g = FIG.fig(R, 1380, 1760, 1500, { tip: 'gilgamis', f: -1, giysi: 'pecek', kol: [[1.3, .45], [.4, .4]], bas: .1, el: { yakin: (R, e, S) => { if (kp < .5) DK.bitki(R, e[0] - S * .01, e[1] - S * .01, S * .26, { z: .95 }); } } });
    // yılan: sudan yükselir (sol alt), başı ele uzanır, kapar ve sola kaçar
    const yg = E.out3(clamp((st.lt - tY + .4) / 1.1)), yc = E.io3(clamp((st.lt - tK - .15) / 1.3));
    const hedef = [760, 380];
    const bas = [lerp(500, hedef[0], yg) - yc * 900, lerp(1100, hedef[1], yg) + yc * 520];
    if (yg > 0) { const pts = []; for (let i = 0; i < 22; i++) { const u = i / 21; pts.push([bas[0] - u * 260 + Math.sin(u * 6 - st.lt * 5) * 40 * u, bas[1] + u * 720]); } DK.yilan(R, pts, 78, { z: .9 }); }
    if (kp >= .5) DK.bitki(R, bas[0] + 40, bas[1] + 20, 300, { z: .96 });
    for (let k = 0; k < 3; k++) { const ph = (((st.lt * .6 + k / 3) % 1) + 1) % 1, rr = 30 + ph * 160; if (yg < .2) { R.d.strokeStyle = dv(.55 * (1 - ph)); R.d.lineWidth = 4; R.d.beginPath(); R.d.ellipse(520, 900, rr, rr * .25, 0, 0, TAU); R.d.stroke(); } }
    R.L.dir = [-.5, -.65, .55]; R.L.col = [1.05, .95, .85];
    R.L.pts.push({ x: hedef[0], y: hedef[1] - 120, z: 260, r: 520, i: .35 * (1 - yc), col: [.55, .75, 1.1] });
  }, { tr: { type: 'cut' } });

  // A02: ölü dost, başında oturan adam; "altı gün yedi gece"de duvara çentikler
  window.SAHNE_YATAK = (R, st, o = {}) => {
    SET.zemin(R); SET.oda(R, { kapiX: o.kapiX ?? 1700 });
    DK.yatak(R, 260, 1180, 640, {});
    FIG.yatan(R, 300, 640, 900, { tip: 'enkidu', ortu: o.ortu || 0, kapali: o.kapali !== false });
    if (o.gilgamis !== false) FIG.sekil(R, [[(o.gx ?? 1360) - 40, 860], [(o.gx ?? 1360) - 40, 712], [(o.gx ?? 1360) + 130, 712], [(o.gx ?? 1360) + 130, 860]], .48, .5, null, 0);
    if (o.gilgamis !== false) FIG.fig(R, o.gx ?? 1360, 860, 600, { tip: 'gilgamis', f: -1, otur: 1, egilme: o.eg ?? .35, bas: o.bas ?? .35, kol: o.kol || [[1.25, .9], [1.0, .9]] });
    if (o.centik) for (let i = 0; i < 7; i++) { const p = clamp(o.centik * 7 - i); if (p <= 0) continue; FIG.cizgi(R, [[1330 + i * 34, 210], [1330 + i * 34, 210 + 110 * p]], 9, -.95); }
    SET.mesale(R, 1560, 300, { son: o.son ?? 1 });
    R.L.int = .32; R.L.amb = .16; R.L.col = [.62, .58, .66]; R.L.dir = [-.4, -.6, .7];
  };
  sahne('A02a', 'A02', 'yatak', 'orta', (R, st) => {
    const t6 = rel(st, 'A02@altı');
    K(R, st, [760, 520, 1.0], [820, 540, 1.12]);
    SAHNE_YATAK(R, st, { ortu: 1, centik: clamp((st.lt - t6) / 2.2) });
  }, { tr: { type: 'fade', dur: .6 } });

  // A03: dönüş ve surlar: iki küçük figür surlara yürür; "Çık"ta sur üstü
  sahne('A03a', 'A03', 'uruk', 'genis', (R, st) => {
    K(R, st, [900, 520, .78], [1040, 520, .82]);
    SET.zemin(R);
    DK.sur(R, -600, 2600, 820, 380, { z: .45 });
    SET.yer(R, -900, 2900, 820, { z: .36 });
    for (let i = 0; i < 7; i++) DK.hurma(R, -500 + i * 470, 880, 260 + (i % 3) * 40, { z: .52 });
    const w = st.lt * 45;
    FIG.fig(R, 620 + w, 1000, 300, { tip: 'gilgamis', f: 1, giysi: 'post', bacak: [[Math.sin(st.lt * 4) * .3, -.1], [-Math.sin(st.lt * 4) * .3, .05]], kol: [[Math.sin(st.lt * 4 + 1) * .3, .3], [-.2, .2]] });
    FIG.fig(R, 470 + w, 1000, 290, { tip: 'ursa', f: 1, bacak: [[-Math.sin(st.lt * 4) * .3, -.1], [Math.sin(st.lt * 4) * .3, .05]], kol: [[2.7, .2], [.2, .2]], el: { yakin: (R, e, S) => FIG.uzuv(R, [e[0] - S * .1, e[1] + S * .5], [e[0] + S * .05, e[1] - S * .45], S * .025, S * .02, .86) } });
    R.L.dir = [-.75, -.35, .45]; R.L.col = [1.05, .9, .76];
  });
  sahne('A03b', 'A03@çık', 'surustu', 'orta', (R, st) => {
    K(R, st, [920, 470, 1.25], [1040, 520, 1.35]);
    SET.zemin(R);
    DK.tugla(R, -800, 560, 2800, 1400, { z: .5, bw: 120, bh: 46, renk: '#A9653F', tohum: 4 });
    FIG.fig(R, 1180, 580, 430, { tip: 'gilgamis', f: -1, kol: [[1.2, .45], [.2, .2]], giysi: 'cubbe' });
    FIG.fig(R, 760, 580, 410, { tip: 'ursa', f: 1, kol: [[.3, .5], [.1, .2]], bas: .25 });
    R.L.dir = [-.8, -.3, .5]; R.L.col = [1.1, .88, .7];
  });
  // A04: yakın yüz, akşam
  sahne('A04a', 'A04', 'surustu', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'gilgamis', f: -1, arka: 'tugla', tuglaRenk: '#A9653F', kay: 30, hy: 430, fig: { bas: -.04, giysi: 'cubbe' } });
    R.L.dir = [-.85, -.2, .4]; R.L.col = [1.12, .8, .6]; R.L.int = .9; R.L.amb = .28;
  });
  // A05: kile bastırılmış parmak izi ("sen"), sonra dünyanın ucuna yürüyen küçük figür
  sahne('A05a', 'A05', 'iz', 'ayrinti', (R, st) => {
    K(R, st, [960, 540, 1.0], [960, 540, 1.12]);
    SET.zemin(R); DK.civi(R, 200, 120, 1720, 960, { sh: 70, sz: 22, tohum: 11 });
    YAR.parmakIzi(R, 980, 560, 380, E.out3(clamp(st.lt / 1.2)));
    R.L.dir = [-.6, -.5, .6];
  });
  sahne('A05b', 'A05@gılgamış', 'ucu', 'orta', (R, st) => {
    K(R, st, [560, 640, 1.35], [900, 620, 1.3]);
    SET.zemin(R); DK.friz(R, -800, 2800, 150, 930);
    SET.tepeler(R, -800, 2800, 820, { h: 200, z: .28 });
    SET.yer(R, -800, 2800, 820, { z: .34 });
    SET.masu(R, 1900, 820, {});
    FIG.fig(R, 300 + st.lt * 60, 830, 230, { tip: 'gilgamis', giysi: 'post', f: 1, bacak: [[Math.sin(st.lt * 4) * .35, -.1], [-Math.sin(st.lt * 4) * .35, .05]], kol: [[Math.sin(st.lt * 4 + 1) * .3, .3], [-.2, .2]] });
    DK.gunes(R, 1900, 380, 70, { z: .5 });
    R.L.dir = [.8, -.3, .4]; R.L.col = [1.1, .82, .62]; R.L.int = .85;
  });

  // ---- bölüm kartları: başlık kile basılır (oyma) ----
  const KART = [['C01', 'II', 'ORMANIN BEKÇİSİ'], ['D01', 'III', 'YATAĞIN BAŞI'], ['E01', 'IV', 'DÜNYANIN UCU'], ['F01', 'V', 'TUFANDAN KURTULAN ADAM'], ['G01', 'VI', 'YILAN'], ['H01', 'VII', 'SURLAR']];
  for (const [id, no, ad] of KART) sahne('K_' + id, id + '-2.0', 'kart', 'kart', (R, st) => {
    K(R, st, [960, 540, 1.0], [960, 540, 1.06]);
    SET.zemin(R);
    DK.tablet(R, 960, 540, 1300, 620, { z: .45, yazi: false });
    DK.civi(R, 400, 260, 1520, 380, { sh: 40, sz: 14, tohum: no.length * 7 });
    DK.civi(R, 400, 700, 1520, 820, { sh: 40, sz: 14, tohum: no.length * 9 });
    const p = clamp(st.lt / .8);
    kilYazi(R, no, 960, 450, { px: 120, derin: .95 * p });
    kilYazi(R, ad, 960, 590, { px: ad.length > 18 ? 62 : ad.length > 14 ? 76 : 96, ls: 6, derin: .95 * p });
    R.L.dir = [-.5, -.6, .55];
  }, { tr: { type: 'muhur', dur: .8 } });
})();
