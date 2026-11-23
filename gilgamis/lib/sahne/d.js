// D: Yatağın başı (D01–D15). Filmin gücü burada: ışık meşale, hareket az, sessizlik uzun. Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at, yur = (t, k = 4) => ({ bacak: [[Math.sin(t * k) * .32, -.1], [-Math.sin(t * k) * .32, .05]] });
  // D01: Enkidu rüyada kararı duyar, yatağa düşer
  sahne('D01a', 'D01', 'yatak', 'genis', (R, st) => {
    K(R, st, [800, 520, .9], [820, 540, .98]);
    SAHNE_YATAK(R, st, { gilgamis: false, kapali: true });
    const p = clamp(st.lt / 2); SET.gece(R, .4 + .3 * p);
  }, { tr: { type: 'muhur', dur: .8 } });
  // D02: sedir kapıya öfke
  sahne('D02a', 'D02', 'kapi_oda', 'orta', (R, st) => {
    const tb = rel(st, 'D02@paramparça');
    K(R, st, [1000, 520, 1.05], [1050, 520, 1.12]);
    SET.zemin(R); SET.oda(R, { kapi: false });
    // kapı (C08'deki kapı)
    FIG.sekil(R, [[1150, 200], [1560, 200], [1560, 860], [1150, 860]], .6, .6, null, 0);
    for (let k = 0; k < 4; k++) FIG.cizgi(R, [[1170, 360 + k * 140], [1540, 360 + k * 140]], 6, -.6);
    for (let k = 0; k < 8; k++) FIG.sekil(R, [[1200 + (k % 2) * 180, 230 + Math.floor(k / 2) * 150], [1330 + (k % 2) * 180, 230 + Math.floor(k / 2) * 150], [1265 + (k % 2) * 180, 340 + Math.floor(k / 2) * 150]], .66, .5);
    if (st.lt > tb) for (let k = 0; k < 5; k++) FIG.cizgi(R, [[1200 + k * 80, 220], [1240 + k * 70, 500], [1190 + k * 85, 840]], 6, -.95 * clamp((st.lt - tb) / .4));
    FIG.fig(R, 720, 870, 520, { tip: 'enkidu', f: 1, egilme: .15, kol: [[2.2 + Math.sin(st.lt * 3) * .2, .6], [.3, .3]], tohum: 4 });
    SET.mesale(R, 400, 300, {});
    R.L.int = .35; R.L.amb = .18; R.L.col = [.62, .58, .66];
  });
  // D03: Şamhat'ı lanetler: duvarda soluk Şamhat (hatıra, alçak kabartma)
  sahne('D03a', 'D03', 'yatak', 'yakin', (R, st) => {
    K(R, st, [700, 440, 1.6], [690, 440, 1.68]);
    SET.zemin(R); SET.oda(R, { kapi: false });
    FIG.fig(R, 1250, 700, 420, { tip: 'samhat', f: -1, z: .42, kol: [[.4, .5], [.1, .2]] });
    DK.yatak(R, 260, 1000, 640, {});
    FIG.fig(R, 520, 640, 520, { tip: 'enkidu', f: 1, otur: 1, egilme: .1, kol: [[1.9, .2], [.3, .3]], tohum: 4 });
    SET.mesale(R, 1600, 300, {});
    R.L.int = .35; R.L.amb = .18; R.L.col = [.62, .58, .66];
  });
  // D04: Şamaş gökten konuşur: odaya güneş ışığı düşer; sayılan nesneler duvarda belirir
  sahne('D04a', 'D04', 'samas', 'genis', (R, st) => {
    K(R, st, [960, 520, .92], [960, 540, .98]);
    SET.zemin(R); SET.oda(R, { kapi: false });
    DK.gunes(R, 960, 150, 90, { z: .6, faz: st.lt * .1 });
    DK.yatak(R, 260, 1000, 700, {});
    FIG.yatan(R, 300, 700, 700, { tip: 'enkidu', kapali: false });
    const ws = ['D04@ekmek', 'D04@içki', 'D04@giysi', 'D04@dost'].map(a => rel(st, a));
    const xs = [1200, 1420, 1640];
    if (st.lt > ws[0]) YAR.ekmek(R, xs[0], 560, 80, 0);
    if (st.lt > ws[1]) YAR.testi(R, xs[1], 620, 190);
    if (st.lt > ws[2]) { const x = xs[2]; FIG.sekil(R, [[x - 70, 430], [x + 70, 430], [x + 90, 620], [x - 90, 620]], .66, .5); }
    if (st.lt > ws[3]) FIG.fig(R, 1420, 870, 220, { tip: 'gilgamis', f: -1, z: .62 });
    R.L.dir = [0, -.9, .45]; R.L.int = 1.05; R.L.amb = .26; R.L.col = [1.1, 1.0, .85];
    R.after(c => { c.globalCompositeOperation = 'screen'; const g = c.createLinearGradient(960, 150, 960, 900); g.addColorStop(0, 'rgba(255,230,170,.35)'); g.addColorStop(1, 'rgba(255,230,170,0)'); c.fillStyle = g; c.beginPath(); c.moveTo(860, 150); c.lineTo(1060, 150); c.lineTo(1500, 900); c.lineTo(300, 900); c.fill(); });
  }, { over: (c, st) => kunye(c, 'VII. tablet', st.lt, 6) });
  // D05: öfke diner; duvardaki Şamhat aydınlanır (kutsama)
  sahne('D05a', 'D05', 'yatak', 'yakin', (R, st) => {
    K(R, st, [700, 470, 1.6], [720, 480, 1.7]);
    SET.zemin(R); SET.oda(R, { kapi: false });
    const p = clamp((st.lt - rel(st, 'D05@kutsadı')) / 1.5);
    FIG.fig(R, 1050, 700, 420, { tip: 'samhat', f: -1, z: .42 + p * .25, kol: [[.4, .5], [.1, .2]] });
    DK.yatak(R, 260, 1000, 640, {});
    FIG.fig(R, 520, 640, 520, { tip: 'enkidu', f: 1, otur: 1, egilme: .1 - p * .1, kol: [[.6, .4], [.3, .3]], bas: -.05, tohum: 4 });
    SET.mesale(R, 1500, 300, {});
    R.L.int = .35 + p * .25; R.L.amb = .18; R.L.col = [.7, .62, .66];
  });
  // D06: ekmek, bira, giysi, dost (ayrıntı; B09'un yankısı) + birleşen iki el
  sahne('D06a', 'D06', 'nesne', 'ayrinti', (R, st) => {
    K(R, st, [960, 560, 1.05], [960, 560, 1.15]);
    SET.zemin(R); DK.tablet(R, 960, 590, 1700, 560, { z: .4, yazi: false });
    UC_NESNE(R, 3, 360);
    FIG.fig(R, 1500, 790, 330, { tip: 'gilgamis', f: 1, z: .74, kol: [[.5, .3], [.1, .2]] }); FIG.fig(R, 1660, 790, 330, { tip: 'enkidu', f: -1, z: .74, kol: [[.5, .3], [.1, .2]], tohum: 4 });
    const k = clamp((st.lt - rel(st, 'D06@ölmek')) / 1.5);
    R.L.dir = [-.7, -.4, .5]; R.L.int = lerp(1, .7, k); R.L.col = [1, lerp(.97, .85, k), lerp(.9, .72, k)];
  });
  // D07: on iki gün: başında oturan Gılgamış, gün ışığı döner
  sahne('D07a', 'D07', 'yatak', 'genis', (R, st) => {
    K(R, st, [800, 520, .88], [820, 540, .92]);
    SAHNE_YATAK(R, st, { kapali: true, gx: 1420, eg: .15, bas: .45, kol: [[.9, .9], [.7, .9]] });
  }, { tr: { type: 'fade', dur: .6 } });
  // D08: el göğüste; kalp atmıyor
  sahne('D08a', 'D08', 'yatak', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'gilgamis', f: -1, arka: 'oda', kay: 15, hx: 1000, fig: { bas: .5, kol: [[.7, .7], [.4, .4]] } });
    const ta = rel(st, 'D08@atmıyordu'), k = clamp((st.lt - ta) / 1.2);
    R.L.int = .15; R.L.amb = .08; R.L.col = [.55, .52, .6];
    R.L.pts.push({ x: 1650, y: 200, z: 300, r: 1800, i: lerp(1.5, .9, k) * (.92 + .08 * noise1(st.t * 6, 2)), col: [1.15, .72, .42] });
  });
  // D09: yüzü gelin gibi örttü (örtü baştan göğse iner)
  sahne('D09a', 'D09', 'yatak', 'orta', (R, st) => {
    K(R, st, [800, 520, 1.25], [780, 520, 1.3]);
    SAHNE_YATAK(R, st, { ortu: E.io3(clamp((st.lt - .3) / 2.0)), gx: 1300, eg: .45, kol: [[1.6, .5], [1.3, .6]] });
  });
  // D10: dişi aslan gibi bir ileri bir geri; saçını yolar, süslerini atar
  sahne('D10a', 'D10', 'yatak', 'genis', (R, st) => {
    K(R, st, [900, 520, .95], [940, 520, 1.0]);
    SAHNE_YATAK(R, st, { ortu: 1, gilgamis: false });
    const ph = st.lt * .45, x = 1000 + Math.sin(ph * PI) * 380, f = Math.cos(ph * PI) > 0 ? 1 : -1;
    const ts = rel(st, 'D10@saçlarını');
    FIG.fig(R, x, 870, 560, { tip: 'gilgamis', f, ...yur(st.lt, 3.3), kol: st.lt > ts ? [[3.0, .9], [2.9, .8]] : [[.3, .4], [-.2, .3]], bas: .2 });
    if (st.lt > rel(st, 'D10@süsleri')) for (let k = 0; k < 5; k++) { const u = clamp((st.lt - rel(st, 'D10@süsleri') - k * .15) / .8); R.b.fillStyle = gv(.8); R.b.beginPath(); R.b.arc(x + (k - 2) * 30, lerp(500, 860, u * u), 12, 0, TAU); R.b.fill(); }
  }, { mb: 2 });
  // D11: gömdürmedi: kapalı kapı, oturan adam (geniş, durgun)
  sahne('D11a', 'D11', 'kapi_oda', 'ayrinti', (R, st) => {
    K(R, st, [1810, 600, 1.9], [1810, 610, 2.0]);
    SAHNE_YATAK(R, st, { ortu: 1, kapiX: 1700, gx: 1330 });
    // kapalı kapı: opak tahta kanat, iki sürgü (biri yukarıda, biri aşağıda; haç biçimi olmasın)
    R.b.fillStyle = gv(.52); R.b.fillRect(1700, 360, 220, 500); R.d.fillStyle = R.T.kilPd; R.d.fillRect(1700, 360, 220, 500); R.m.fillStyle = '#9C6E48'; R.m.fillRect(1700, 360, 220, 500);
    for (let k = 1; k < 5; k++) FIG.cizgi(R, [[1700 + k * 44, 370], [1700 + k * 44, 850]], 4, -.5);
    FIG.uzuv(R, [1680, 470], [1950, 470], 30, 30, .72); FIG.uzuv(R, [1680, 760], [1950, 760], 30, 30, .72);
  });
  // D12: altı gün yedi gece: duvara çentikler, meşale kısalır
  sahne('D12a', 'D12@altı', 'yatak', 'orta', (R, st) => {
    K(R, st, [1100, 420, 1.2], [1150, 440, 1.25]);
    SAHNE_YATAK(R, st, { ortu: 1, centik: clamp(st.lt / Math.max(2, st.d * .6)), gx: 1330, son: lerp(1, .6, clamp(st.lt / st.d)) });
  }, { over: (c, st) => kunye(c, 'Eski Babil Sippar tableti; Standart sürüm, X. tablet', st.lt, 99) });
  // D13: "Ta ki burnundan bir kurt düşene kadar." Karanlık; yalnız yüz; meşale söner. (Kurt gösterilmez.)
  sahne('D13a', 'D13', 'yatak', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'gilgamis', f: -1, arka: 'oda', kay: 12, hx: 900, fig: { bas: .45 } });
    const son = clamp(1 - (st.lt - 1.6) / 2.2);
    R.L.int = .12; R.L.amb = .06; R.L.col = [.5, .5, .6];
    R.L.pts.push({ x: 1600, y: 200, z: 300, r: 1800, i: 1.5 * son * (.9 + .1 * noise1(st.t * 6, 2)), col: [1.15, .7, .4] });
  }, { tr: { type: 'fade', dur: .6 } });
  // D14: bozkırda yalnız: "Ben de ölmeyecek miyim?"
  sahne('D14a', 'D14', 'bozkir', 'genis', (R, st) => {
    K(R, st, [960, 560, .9], [1000, 560, .95]);
    SET.zemin(R); SET.tepeler(R, -600, 2700, 760, { h: 220, z: .26 }); SET.yer(R, -900, 2900, 860, { z: .33 });
    FIG.fig(R, 960, 865, 360, { tip: 'gilgamis', f: 1, kol: [[.2, .4], [.1, .3]], bas: .15, ...yur(st.lt * .4, 3) });
    YAR.aslan(R, 1600, 860, 260, { f: -1, z: .58 });
    R.L.dir = [.8, -.3, .4]; R.L.col = [1.1, .78, .6]; R.L.int = .8; R.L.amb = .26;
  }, { tr: { type: 'black', dur: 1.0 }, over: (c, st) => kunye(c, 'IX. tablet', st.lt, 5) });
  // D15: aslan postuna bürünür, yola çıkar
  sahne('D15a', 'D15', 'bozkir', 'orta', (R, st) => {
    K(R, st, [800, 520, 1.15], [1100, 520, 1.15]);
    SET.zemin(R); SET.tepeler(R, -600, 2700, 760, { h: 220, z: .26 }); SET.yer(R, -900, 2900, 880, { z: .33 });
    FIG.fig(R, 760 + st.lt * 90, 885, 480, { tip: 'gilgamis', f: 1, giysi: 'post', ...yur(st.lt, 4) });
    R.L.dir = [.8, -.3, .4]; R.L.col = [1.1, .78, .6]; R.L.int = .8;
  });
})();
