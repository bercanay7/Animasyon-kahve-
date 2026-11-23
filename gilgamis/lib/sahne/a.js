// A: kanca (A01–A05) ve bölüm kartları. Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at;   // çapanın çekim içi zamanı
  // ortak: gölet başı (A01 ve G06–G07 aynı set)
  window.SAHNE_GOLET = (R, st, o) => {
    SET.zemin(R);
    DK.tugla(R, -900, -300, 2900, 330, { z: .28, bw: 110, bh: 40, lw: 2 });
    SET.yer(R, -900, 2900, 330, { z: .3, cimen: true, kal: 30 });
    DK.hurma(R, 150, 360, 340, { z: .46 }); DK.hurma(R, 1720, 360, 300, { z: .46, egri: 30 });
    // su (lacivert), kıyı
    R.b.fillStyle = gv(.14); R.b.fillRect(-900, 640, 3800, 900); R.m.fillStyle = '#41639E'; R.m.fillRect(-900, 640, 3800, 900);
    for (let i = 0; i < 9; i++) { const y = 690 + i * 48, fz = (FIG_T || 0) * .6 + i; R.d.strokeStyle = dv(.4); R.d.lineWidth = 3; R.d.beginPath(); for (let x = -900; x < 2900; x += 20) { const yy = y + Math.sin(x / 90 + fz) * 6; x === -900 ? R.d.moveTo(x, yy) : R.d.lineTo(x, yy); } R.d.stroke(); }
    R.b.fillStyle = gv(.4); R.b.beginPath(); R.b.moveTo(-900, 640); for (let x = -900; x < 2900; x += 60) R.b.lineTo(x, 610 + Math.sin(x / 210) * 14); R.b.lineTo(2900, 650); R.b.lineTo(-900, 650); R.b.fill();
    cizgi2(R, -900, 2900, 640);
  };
  const cizgi2 = (R, x0, x1, y) => FIG.cizgi(R, [[x0, y], [x1, y]], 4, -.7);

  // A01: el bitkiyi tutar; "kaptırdı"da yılan alır
  sahne('A01a', 'A01', 'golet', 'yakin', (R, st) => {
    const tY = rel(st, 'A01@yılana'), tK = rel(st, 'A01@kaptırdı');
    K(R, st, [980, 470, 1.55], [1000, 480, 1.75]);
    SAHNE_GOLET(R, st);
    // el ve kol (sağdan uzanan) — kabartma: kol + yumruk + bitki
    const kp = clamp((st.lt - tK) / .9), bx = 980 - kp * 0, by = 520;
    FIG.uzuv(R, [1500, 640], [1150, 540], 120, 95, .78); FIG.uzuv(R, [1150, 540], [1010, 520], 95, 80, .8);
    FIG.cizgi(R, [[1060, 490], [1060, 555]], 7, .6); // bilezik
    if (kp < .6) DK.bitki(R, 940, 520, 300 * (1 - kp * .3), { z: .86 });
    R.b.fillStyle = gv(.84); R.b.beginPath(); R.b.ellipse(980, 520, 62, 50, 0, 0, TAU); R.b.fill();
    for (let k = 0; k < 3; k++) FIG.cizgi(R, [[945 + k * 22, 488], [955 + k * 22, 545]], 4, -.6);
    // yılan: soldan gelir, bitkiyi kapar, geri çekilir
    const yg = clamp((st.lt - tY + .6) / 1.0), yc = clamp((st.lt - tK - .2) / 1.4);
    const bas = [lerp(220, 930, E.out3(yg)) - E.io3(yc) * 820, lerp(640, 470, E.out3(yg)) + E.io3(yc) * 140];
    const pts = []; for (let i = 0; i < 20; i++) pts.push([bas[0] - i * 38, bas[1] + 40 + Math.sin(i * .7 - st.lt * 4) * 26 + i * 4]);
    DK.yilan(R, pts, 62, { z: .9 });
    if (kp >= .6) DK.bitki(R, bas[0] + 30, bas[1] + 10, 210, { z: .93 });
    R.L.dir = [-.5, -.7, .55];
  }, { tr: { type: 'cut' } });

  // A02: ölü dost, başında oturan adam; "altı gün yedi gece"de duvara çentikler
  window.SAHNE_YATAK = (R, st, o = {}) => {
    SET.zemin(R); SET.oda(R, { kapiX: o.kapiX ?? 1700 });
    DK.yatak(R, 260, 1180, 640, {});
    if (o.ortu) { // gelin gibi örtülü beden
      const p = o.ortu; FIG.sekil(R, [[300, 640], [320, 560], [700, 548], [1060, 520], [1130, 560], [1150, 640]], .7, .5, null, .8);
      for (let k = 0; k < 9; k++) FIG.cizgi(R, [[360 + k * 85, 556 - k * 3], [380 + k * 85, 636]], 3, -.45);
      if (p < 1) { /* örtü iniyor: yüz görünüyor */ }
    } else FIG.fig(R, 300, 630, 860, { tip: 'enkidu', don: PI / 2, f: -1, z: .72, kol: [[.05, 0], [0, .1]], bacak: [[0, 0], [0, 0]], basO: { kapali: o.kapali !== false }, tohum: 2 });
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
    FIG.fig(R, 1180, 580, 430, { tip: 'gilgamis', f: -1, kol: [[1.55, .05], [.2, .2]], giysi: 'etek' });
    FIG.fig(R, 760, 580, 410, { tip: 'ursa', f: 1, kol: [[.3, .5], [.1, .2]], bas: .25 });
    R.L.dir = [-.8, -.3, .5]; R.L.col = [1.1, .88, .7];
  });
  // A04: yakın yüz, akşam
  sahne('A04a', 'A04', 'surustu', 'yakin', (R, st) => {
    K(R, st, [1180, 300, 2.3], [1160, 300, 2.45]);
    SET.zemin(R);
    DK.tugla(R, -800, 560, 2800, 1400, { z: .5, bw: 120, bh: 46, renk: '#A9653F', tohum: 4 });
    FIG.fig(R, 1180, 580, 430, { tip: 'gilgamis', f: -1, kol: [[.2, .2], [.1, .2]], bas: -.05 });
    R.L.dir = [-.85, -.2, .4]; R.L.col = [1.12, .8, .6]; R.L.int = .9; R.L.amb = .28;
  });
  // A05: kile bastırılmış parmak izi ("sen"), sonra dünyanın ucuna yürüyen küçük figür
  sahne('A05a', 'A05', 'iz', 'ayrinti', (R, st) => {
    K(R, st, [960, 540, 1.0], [960, 540, 1.12]);
    SET.zemin(R); DK.civi(R, 200, 120, 1720, 960, { sh: 70, sz: 22, tohum: 11 });
    YAR.parmakIzi(R, 980, 560, 380, E.out3(clamp(st.lt / 1.2)));
    R.L.dir = [-.6, -.5, .6];
  });
  sahne('A05b', 'A05@gılgamış', 'ucu', 'genis', (R, st) => {
    K(R, st, [700, 560, .9], [1100, 560, .95]);
    SET.zemin(R); DK.friz(R, -800, 2800, 150, 930);
    SET.tepeler(R, -800, 2800, 820, { h: 200, z: .28 });
    SET.yer(R, -800, 2800, 820, { z: .34 });
    SET.masu(R, 1900, 820, {});
    FIG.fig(R, 300 + st.lt * 60, 830, 230, { tip: 'gilgamis', giysi: 'post', f: 1, bacak: [[Math.sin(st.lt * 4) * .35, -.1], [-Math.sin(st.lt * 4) * .35, .05]], kol: [[Math.sin(st.lt * 4 + 1) * .3, .3], [-.2, .2]] });
    DK.gunes(R, 1900, 380, 70, { z: .5 });
    R.L.dir = [.8, -.3, .4]; R.L.col = [1.1, .82, .62]; R.L.int = .85;
  });

  // ---- bölüm kartları: başlık kile basılır (oyma) ----
  const KART = [['B01', 'I', 'YABANİ ADAM'], ['C01', 'II', 'ORMANIN BEKÇİSİ'], ['D01', 'III', 'YATAĞIN BAŞI'], ['E01', 'IV', 'DÜNYANIN UCU'], ['F01', 'V', 'TUFANDAN KURTULAN ADAM'], ['G01', 'VI', 'YILAN'], ['H01', 'VII', 'SURLAR']];
  for (const [id, no, ad] of KART) sahne('K_' + id, id + '-2.0', 'kart', 'kart', (R, st) => {
    K(R, st, [960, 540, 1.0], [960, 540, 1.06]);
    SET.zemin(R);
    DK.tablet(R, 960, 540, 1300, 620, { z: .45, yazi: false });
    DK.civi(R, 400, 260, 1520, 380, { sh: 40, sz: 14, tohum: no.length * 7 });
    DK.civi(R, 400, 700, 1520, 820, { sh: 40, sz: 14, tohum: no.length * 9 });
    const p = clamp(st.lt / .8);
    kilYazi(R, no, 960, 450, { px: 120, derin: .95 * p });
    kilYazi(R, ad, 960, 590, { px: ad.length > 14 ? 76 : 96, ls: 6, derin: .95 * p });
    R.L.dir = [-.5, -.6, .55];
  }, { tr: { type: 'muhur', dur: .8 } });
})();
