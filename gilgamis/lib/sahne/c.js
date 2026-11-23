// C: Ormanın bekçisi (C01–C11). Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at, yur = (t, k = 4) => ({ bacak: [[Math.sin(t * k) * .32, -.1], [-Math.sin(t * k) * .32, .05]] });
  // C01: Gılgamış uzaktaki ormanı gösterir
  sahne('C01a', 'C01', 'uruk', 'genis', (R, st) => {
    K(R, st, [800, 540, .9], [1000, 540, .92]);
    SET.zemin(R); DK.friz(R, -600, 2600, 130, 950);
    SET.tepeler(R, 900, 2600, 760, { h: 260, z: .27 });
    SET.orman(R, 1300, 2500, 760, { h: 340, ara: 170, z: .34 });
    SET.yer(R, -900, 2900, 860, { z: .34 });
    FIG.fig(R, 520, 870, 420, { tip: 'gilgamis', f: 1, kol: [[1.55, .05], [.1, .2]] });
    FIG.fig(R, 300, 870, 420, { tip: 'enkidu', f: 1, kol: [[.2, .3], [0, .2]], tohum: 4 });
    R.L.dir = [-.55, -.55, .6];
  }, { over: (c, st) => etiket(c, 'SEDİR ORMANI', 1450, 210, st.lt - 1.5, 4) });
  // C02: Humbaba'nın yüzü (Enkidu'nun anlattığı); kükreme, ateş, ölüm
  sahne('C02a', 'C02@kükremesi', 'humbaba', 'yakin', (R, st) => {
    const tA = rel(st, 'C02@ağzı');
    K(R, st, [960, 520, 1.0], [960, 520, 1.12]);
    SET.zemin(R); SET.orman(R, -200, 2200, 1000, { h: 900, ara: 300, z: .3 });
    YAR.humbaba(R, 960, 520, 760, { agiz: .5 + .5 * Math.sin(st.lt * 5) });
    R.L.int = .55; R.L.amb = .18; R.L.dir = [.0, -.3, .8];
    if (st.lt > tA) R.L.pts.push({ x: 960, y: 650, z: 120, r: 900, i: 1.4 * clamp((st.lt - tA) / .5), col: [1.2, .55, .2] });
    if (st.lt > tA) R.after(c => { c.globalCompositeOperation = 'screen'; const g = c.createRadialGradient(960, 640, 10, 960, 640, 260); g.addColorStop(0, 'rgba(255,170,70,.75)'); g.addColorStop(1, 'rgba(255,80,0,0)'); c.fillStyle = g; c.fillRect(600, 380, 720, 520); });
  }, { tr: { type: 'fade', dur: .5 } });
  // C03: Gılgamış önden yürür
  sahne('C03a', 'C03', 'yol', 'orta', (R, st) => {
    K(R, st, [700, 520, 1.1], [1100, 520, 1.1]);
    SET.zemin(R); SET.tepeler(R, -600, 2800, 700, { h: 220, z: .27 }); SET.yer(R, -900, 2900, 880, { z: .34 });
    const w = st.lt * 75;
    FIG.fig(R, 700 + w, 885, 480, { tip: 'gilgamis', f: 1, ...yur(st.lt), kol: [[Math.sin(st.lt * 4 + 1) * .35, .4], [2.4, .2]], el: { uzak: (R, e, S) => { FIG.uzuv(R, [e[0], e[1]], [e[0] + S * .12, e[1] - S * .25], S * .03, S * .025, .68); FIG.sekil(R, [[e[0] + S * .1, e[1] - S * .3], [e[0] + S * .22, e[1] - S * .27], [e[0] + S * .15, e[1] - S * .18]], .7, .5); } } });
    FIG.fig(R, 380 + w, 885, 470, { tip: 'enkidu', f: 1, ...yur(st.lt + 1), kol: [[.3, .5], [-.2, .2]], tohum: 4 });
    R.L.dir = [-.6, -.5, .6];
  }, { over: (c, st) => quote(c, '“Düşersem adımı bırakırım.”', 960, 190, st.lt, { t0: rel(st, 'C03@düşersem'), px: 66, kaynak: 'Eski Babil, Yale tableti' }) });
  // C04: kile basılan ad (kamış kalem çivi işaretleri basar)
  sahne('C04a', 'C04', 'ad', 'ayrinti', (R, st) => {
    K(R, st, [960, 540, 1.3], [1060, 540, 1.4]);
    SET.zemin(R); DK.tablet(R, 960, 540, 1500, 700, { z: .45, yazi: false });
    const p = clamp(st.lt / 3.2);
    R.b.save(); R.b.beginPath(); R.b.rect(0, 0, 360 + p * 1200, 2000); R.b.clip();
    R.d.save(); R.d.beginPath(); R.d.rect(0, 0, 360 + p * 1200, 2000); R.d.clip();
    DK.civi(R, 330, 420, 1590, 680, { sh: 120, sz: 46, tohum: 21 });
    R.b.restore(); R.d.restore();
    const x = 360 + p * 1200; FIG.uzuv(R, [x + 40, 300], [x + 520, -200], 34, 30, .9);
    R.L.dir = [-.7, -.4, .5];
  });
  // C05: orman, iki küçük figür girer
  sahne('C05a', 'C05', 'orman', 'genis', (R, st) => {
    K(R, st, [900, 520, .8], [1050, 520, .84]);
    SET.zemin(R); SET.orman(R, -500, 2600, 880, { h: 760, ara: 230 });
    SET.yer(R, -900, 2900, 880, { z: .36 });
    const w = st.lt * 50;
    FIG.fig(R, 250 + w, 890, 260, { tip: 'gilgamis', f: 1, ...yur(st.lt) });
    FIG.fig(R, 140 + w, 890, 255, { tip: 'enkidu', f: 1, ...yur(st.lt + 1), tohum: 4 });
    R.L.dir = [-.4, -.7, .55]; R.L.int = .85;
  });
  // C06 başı: kaçakçıdan alınan kırık tablet
  sahne('C06t', 'C06', 'tablet', 'ayrinti', (R, st) => {
    K(R, st, [960, 540, 1.0], [960, 540, 1.1]);
    SET.zemin(R);
    DK.tablet(R, 960, 540, 760, 900, { z: .5, sh: 56, sz: 19, tohum: 33, kirik: [[1340, 0], [1340, 1100], [1180, 1100], [1250, 760], [1150, 520], [1260, 300], [1170, 0]] });
    R.L.dir = [-.7, -.45, .5];
  }, { over: (c, st) => kunye(c, 'Süleymaniye Müzesi · 2011', st.lt, 99) });
  // C06: ormanın sesi: maymunlar, kuşlar, ağustosböcekleri (2011 tableti)
  sahne('C06a', 'C06@tablet#1', 'orman', 'orta', (R, st) => {
    K(R, st, [900, 500, 1.1], [1060, 500, 1.15]);
    SET.zemin(R); SET.orman(R, -200, 2400, 980, { h: 980, ara: 360, z: .42 });
    const t = st.lt;
    YAR.maymun(R, 560, 470 + Math.abs(Math.sin(t * 3)) * -30, 150, { kol: Math.abs(Math.sin(t * 3)), z: .78 });
    YAR.maymun(R, 1250, 380 + Math.abs(Math.sin(t * 2.5 + 1)) * -26, 130, { f: -1, kol: .5 + .5 * Math.sin(t * 4), z: .78 });
    YAR.maymun(R, 1700, 560, 120, { kol: .3, z: .76 });
    for (let i = 0; i < 6; i++) YAR.kus(R, 300 + i * 260 + Math.sin(t + i) * 40, 200 + (i % 3) * 90 + Math.sin(t * 2 + i) * 20, 70, { kanat: t * 12 + i, z: .8 });
    for (let i = 0; i < 5; i++) YAR.agustos(R, 420 + i * 330, 760 + (i % 2) * 60, 46);
    R.L.dir = [-.45, -.65, .6];
  }, { over: (c, st) => kunye(c, 'V. tablet, Süleymaniye Müzesi tableti (2011)', st.lt, 6) });
  // C07: Humbaba diz çöker, aman diler; Enkidu "Dinleme onu"
  sahne('C07a', 'C07', 'humbaba', 'genis', (R, st) => {
    const to = rel(st, 'C07@öldürdüler');
    K(R, st, [960, 540, .86], [960, 530, .9]);
    SET.zemin(R); SET.orman(R, -200, 2400, 960, { h: 900, ara: 330, z: .3 }); SET.yer(R, -900, 2900, 880, { z: .34 });
    YAR.humbaba(R, 1350, 560, 420, { agiz: .3 });
    FIG.uzuv(R, [1350, 760], [1350, 880], 180, 220, .74);
    FIG.fig(R, 720, 885, 520, { tip: 'gilgamis', f: 1, kol: [[st.lt > to - .6 ? 3.0 : 1.0, .3], [.3, .2]] });
    FIG.fig(R, 420, 885, 510, { tip: 'enkidu', f: 1, kol: [[1.3, .2], [.1, .2]], tohum: 4 });
    if (st.lt > to) { R.L.int *= clamp(1 - (st.lt - to) / .5, .15, 1); R.L.amb *= .6; }
    R.L.dir = [-.5, -.6, .6];
  });
  // C08: en yüksek sedir devrilir; Enkidu kapı yapar
  sahne('C08a', 'C08', 'orman', 'genis', (R, st) => {
    K(R, st, [960, 520, .85], [960, 520, .9]);
    SET.zemin(R); SET.orman(R, -500, 2600, 900, { h: 600, ara: 300, z: .34 }); SET.yer(R, -900, 2900, 900, { z: .36 });
    const p = E.in2(clamp((st.lt - .5) / 1.6));
    R.b.save(); R.d.save(); R.m.save(); for (const c of [R.b, R.d, R.m]) { c.translate(980, 900); c.rotate(p * 1.45); c.translate(-980, -900); }
    DK.sedir(R, 980, 900, 900, { z: .7, kat: 9 });
    R.b.restore(); R.d.restore(); R.m.restore();
    FIG.fig(R, 700, 905, 300, { tip: 'gilgamis', f: 1, kol: [[2.6 - p * 1.6, .3], [.2, .2]] });
    R.L.dir = [-.5, -.6, .6];
  }, { mb: 3 });
  sahne('C08b', 'C08@enkidu', 'kapi_yap', 'orta', (R, st) => {
    K(R, st, [960, 520, 1.1], [980, 520, 1.15]);
    SET.zemin(R); SET.yer(R, -900, 2900, 890, { z: .34 });
    const p = clamp(st.lt / 3);
    FIG.sekil(R, [[1050, 120], [1500, 120], [1500, 880], [1050, 880]], .62, .6, null, 0);
    for (let k = 0; k < 4; k++) FIG.cizgi(R, [[1070, 300 + k * 160], [1480, 300 + k * 160]], 6, -.6);
    for (let k = 0; k < Math.floor(p * 8); k++) FIG.sekil(R, [[1110 + (k % 2) * 200, 160 + Math.floor(k / 2) * 160], [1250 + (k % 2) * 200, 160 + Math.floor(k / 2) * 160], [1180 + (k % 2) * 200, 280 + Math.floor(k / 2) * 160]], .68, .5);
    FIG.fig(R, 760, 895, 500, { tip: 'enkidu', f: 1, kol: [[1.8 + Math.sin(st.lt * 5) * .5, .3], [.5, .4]], tohum: 4, el: { yakin: (R, e, S) => { FIG.uzuv(R, e, [e[0] + S * .02, e[1] - S * .2], S * .025, S * .02, .9); FIG.sekil(R, [[e[0] - S * .04, e[1] - S * .22], [e[0] + S * .1, e[1] - S * .24], [e[0] + S * .08, e[1] - S * .14]], .9, .5); } } });
    R.L.dir = [-.55, -.55, .6];
  });
  // C09: Gök Boğası
  sahne('C09a', 'C09', 'boga', 'orta', (R, st) => {
    const to = rel(st, 'C09@öldürdüler'), p = clamp((st.lt - to) / .8);
    K(R, st, [900, 560, 1.15], [920, 560, 1.2]);
    SET.zemin(R); DK.friz(R, -600, 2600, 120, 960);
    SET.yer(R, -900, 2900, 860, { z: .36 });
    DK.gunes(R, 300, 300, 60, { z: .48 });
    YAR.boga(R, 1260 - (1 - p) * clamp(st.lt / 2) * 300, 860, 520, { f: -1, kos: p < .1 ? st.lt * 8 : 0, don: -p * .25 });
    FIG.fig(R, 620, 870, 420, { tip: 'gilgamis', f: 1, kol: [[1.6, .1], [.6, .3]], bacak: [[.45, -.2], [-.3, .1]] });
    FIG.fig(R, 400, 870, 415, { tip: 'enkidu', f: 1, kol: [[1.3, .2], [.4, .3]], tohum: 4 });
    R.L.dir = [-.55, -.55, .6];
  }, { tr: { type: 'muhur', dur: .8 } });
  // C10: tanrılar toplanır: üstte işaretler (taçlar, güneş), altta iki küçük dost
  sahne('C10a', 'C10', 'tanrilar', 'genis', (R, st) => {
    K(R, st, [960, 520, .92], [960, 560, 1.0]);
    SET.zemin(R); DK.friz(R, -600, 2600, 90, 980);
    FIG.cizgi(R, [[-600, 520], [2600, 520]], 8, .6);
    const n = 5, p = clamp(st.lt / 2.5);
    for (let i = 0; i < n; i++) { const pp = clamp(p * n - i); if (pp > 0) SET.tac(R, 360 + i * 300, 500, 240 * (.7 + .3 * pp)); }
    DK.gunes(R, 1560, 330, 110, { z: .55 });
    SET.yer(R, -900, 2900, 900, { z: .34 });
    FIG.fig(R, 850, 905, 300, { tip: 'gilgamis', f: 1, kol: [[.2, .2], [0, .2]] });
    FIG.fig(R, 1080, 905, 300, { tip: 'enkidu', f: -1, kol: [[.2, .2], [0, .2]], tohum: 4 });
    R.L.dir = [0, -.8, .6];
  });
  // C11: Enkidu'nun yüzü; ışık söner
  sahne('C11a', 'C11', 'tanrilar', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'enkidu', f: -1, arka: 'tepe', kay: -30, fig: { tohum: 4, bas: .12 } });
    R.L.dir = [0, -.8, .6]; R.L.int = lerp(1, .35, clamp(st.lt / 2.5)); R.L.amb = lerp(.34, .2, clamp(st.lt / 2.5));
  });
})();
