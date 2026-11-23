// H: Surlar (H01–H11). Pişmiş tuğla rengi yalnız burada (bölümün kuralı: yaş kilden pişmiş tuğlaya). Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at, yur = (t, k = 4) => ({ bacak: [[Math.sin(t * k) * .32, -.1], [-Math.sin(t * k) * .32, .05]] });
  const TUGLA = '#A4603A';
  // H01: Uruk ufukta; yaklaşırlar
  sahne('H01a', 'H01', 'uruk', 'genis', (R, st) => {
    K(R, st, [960, 540, .75], [960, 540, .86]);
    SET.zemin(R); DK.sur(R, -600, 2600, 800, 420, { z: .45, renk: TUGLA });
    SET.yer(R, -900, 2900, 800, { z: .36 });
    for (let i = 0; i < 7; i++) DK.hurma(R, -500 + i * 470, 860, 260 + (i % 3) * 40, { z: .52, meyve: true });
    FIG.fig(R, 760 + st.lt * 30, 990, 300, { tip: 'gilgamis', giysi: 'cubbe', f: 1, ...yur(st.lt * .8) });
    FIG.fig(R, 600 + st.lt * 30, 990, 290, { tip: 'ursa', f: 1, ...yur(st.lt * .8 + 1) });
    R.L.dir = [-.75, -.35, .45]; R.L.col = [1.08, .9, .74];
  }, { tr: { type: 'muhur', dur: .8 } });
  // H02: sur üstü; tuğlaya bakın
  sahne('H02a', 'H02', 'surustu', 'orta', (R, st) => {
    K(R, st, [960, 470, 1.15], [1000, 480, 1.22]);
    SET.zemin(R); DK.tugla(R, -800, 560, 2800, 1400, { z: .5, bw: 120, bh: 46, renk: TUGLA, tohum: 4 });
    for (let b = -800; b < 2800; b += 120) { R.b.fillStyle = gv(.55); R.b.fillRect(b, 500, 70, 60); R.m.fillStyle = TUGLA; R.m.fillRect(b, 500, 70, 60); }
    FIG.fig(R, 1180, 500, 430, { tip: 'gilgamis', giysi: 'cubbe', f: -1, kol: [[1.4 + Math.sin(st.lt * .8) * .2, .1], [.2, .2]] });
    FIG.fig(R, 760, 500, 410, { tip: 'ursa', f: 1, kol: [[.3, .5], [.1, .2]], bas: .3 });
    R.L.dir = [-.8, -.3, .5]; R.L.col = [1.1, .9, .74];
  }, { over: (c, st) => kunye(c, 'XI. tablet, son satırlar', st.lt, 5) });
  sahne('H02b', 'H02@tuğlaları#1', 'tugla', 'ayrinti', (R, st) => {
    K(R, st, [960, 540, 1.8], [1060, 540, 1.85]);
    SET.zemin(R); DK.tugla(R, -800, -400, 2800, 1400, { z: .5, bw: 240, bh: 90, renk: TUGLA, tohum: 8, lw: 6 });
    for (let i = 0; i < 40; i++) { R.d.fillStyle = dv(-.5); R.d.beginPath(); R.d.arc(400 + hash(i) * 1200, 200 + hash(i + 9) * 700, 4 + hash(i + 3) * 5, 0, TAU); R.d.fill(); }
    R.L.dir = [-.85, -.25, .45]; R.L.col = [1.12, .86, .66];
  });
  // H03: şehir, hurma bahçesi, kil çukuru (kaydırma)
  window.SEHIR = (R, st, o = {}) => {
    SET.zemin(R);
    for (let i = 0; i < 10; i++) SET.ev(R, -400 + i * 230, 520 + (i % 2) * 40, 200, 160 + (i % 3) * 30, { z: .4 });
    for (let i = 0; i < 6; i++) DK.hurma(R, 1950 + i * 170, 600, 260, { z: .46, meyve: true });
    // kil çukuru: tuğla kalıpları kuruyor
    R.b.fillStyle = gv(.12); R.b.beginPath(); R.b.ellipse(3200, 560, 300, 80, 0, 0, TAU); R.b.fill();
    for (let i = 0; i < 10; i++) { R.b.fillStyle = gv(.5); R.b.fillRect(2950 + (i % 5) * 100, 640 + Math.floor(i / 5) * 50, 70, 30); }
    // ön: sur korkuluğu
    DK.tugla(R, -900, 780, 4200, 1300, { z: .58, bw: 120, bh: 46, renk: TUGLA, tohum: 4 });
  };
  sahne('H03a', 'H03', 'sehir', 'genis', (R, st) => {
    K(R, st, [600, 540, .9], [2900, 540, .9], E.io2);
    SEHIR(R, st);
    R.L.dir = [-.75, -.4, .5]; R.L.col = [1.08, .9, .74];
  });
  // H04: surun içi: fırınlar, bahçe, el ele insanlar, elini tutan çocuk
  sahne('H04a', 'H04', 'sehir_ici', 'orta', (R, st) => {
    K(R, st, [900, 520, 1.05], [1050, 520, 1.1]);
    SET.zemin(R); DK.tugla(R, -800, 80, 2800, 300, { z: .32, bw: 100, bh: 40 });
    SET.ev(R, -200, 760, 500, 380, {}); SET.ev(R, 1500, 760, 600, 420, { kapi: .6 });
    SET.yer(R, -900, 2900, 880, { z: .36, cimen: false });
    SET.firin(R, 380, 880, 110, {}); YAR.ekmek(R, 560, 880, 46, 0);
    FIG.fig(R, 260, 885, 380, { tip: 'kadin', f: 1, egilme: .3, kol: [[1.2, .5], [.8, .4]] });
    DK.hurma(R, 1400, 880, 420, { meyve: true });
    const w = st.lt * 40;
    FIG.fig(R, 800 + w, 885, 420, { tip: 'adam', f: 1, ...yur(st.lt, 3), kol: [[.2, .1], [.45, .1]] });
    FIG.fig(R, 960 + w, 885, 280, { tip: 'cocuk', f: 1, ...yur(st.lt + .5, 3.6), kol: [[.3, .2], [-.55, .1]], z: .76 });
    FIG.fig(R, 1180 + w, 885, 400, { tip: 'kadin', f: 1, ...yur(st.lt + 1, 3), kol: [[-.4, .1], [.2, .2]] });
    R.L.dir = [-.6, -.5, .6]; R.L.col = [1.07, .95, .82];
  });
  // H05–H07: destanın ilk tableti; sandık, kilit, lacivert tablet
  sahne('H05a', 'H05', 'tablet', 'orta', (R, st) => {
    K(R, st, [960, 540, 1.2], [960, 540, 1.0]);
    SET.zemin(R);
    DK.tablet(R, 960, 540, 820, 1000, { z: .5, sh: 52, sz: 18, tohum: 41 });
    kilYazi(R, 'I', 960, 90, { px: 60 });
    R.L.dir = [-.65, -.5, .55];
  }, { tr: { type: 'fade', dur: .6 }, over: (c, st) => kunye(c, 'I. tablet, ilk satırlar', st.lt, 99) });
  sahne('H06a', 'H06', 'tablet', 'yakin', (R, st) => {
    K(R, st, [960, 460, 1.6], [960, 480, 1.7]);
    SET.zemin(R);
    DK.tablet(R, 960, 540, 820, 1000, { z: .5, sh: 52, sz: 18, tohum: 41 });
    R.L.dir = [-.65, -.5, .55];
  }, { over: (c, st) => quote(c, '“Çık Uruk\'un surlarına, yürü.”', 960, 200, st.lt, { t0: rel(st, 'H06@çık'), px: 66 }) });
  sahne('H07a', 'H07', 'sandik', 'ayrinti', (R, st) => {
    const tk = rel(st, 'H07@kilidini'), tt = rel(st, 'H07@tableti');
    K(R, st, [960, 600, 1.05], [960, 560, 1.25]);
    SET.zemin(R); DK.tugla(R, -800, -400, 2800, 1400, { z: .45, bw: 150, bh: 56, renk: TUGLA, tohum: 12 });
    R.b.fillStyle = gv(.12); R.b.fillRect(520, 380, 880, 560);
    FIG.sekil(R, [[600, 520], [1320, 520], [1320, 900], [600, 900]], .55, .6, '#8C6644', 0);
    for (let k = 0; k < 6; k++) FIG.cizgi(R, [[620, 560 + k * 60], [1300, 560 + k * 60]], 3, -.45);
    const ac = E.io3(clamp((st.lt - tk) / 1.2));
    R.b.save(); R.d.save(); R.m.save(); for (const c of [R.b, R.d, R.m]) { c.translate(600, 520); c.rotate(-ac * 1.1); c.translate(-600, -520); }
    FIG.sekil(R, [[590, 460], [1330, 460], [1330, 525], [590, 525]], .66, .6, '#8C6644', 0);
    R.b.restore(); R.d.restore(); R.m.restore();
    FIG.sekil(R, [[930, 500], [990, 500], [990, 570], [930, 570]], .74, .6, ac > .1 ? '#7A5A30' : '#9A7A40', 0);
    const tp = E.out3(clamp((st.lt - tt) / 1.4));
    if (tp > 0) { DK.tablet(R, 960, lerp(720, 470, tp), 420, 300, { z: .82, renk: '#2F4E95', sh: 24, sz: 9, tohum: 50 }); R.L.pts.push({ x: 960, y: 470, z: 200, r: 600 * tp, i: .5 * tp, col: [.55, .7, 1.1] }); }
    R.L.dir = [-.6, -.5, .6];
  });
  // H08: harita kabartması: Uruk'tan Hattuşa'ya
  sahne('H08a', 'H08', 'harita', 'genis', (R, st) => {
    const th = rel(st, 'H08@hattuşa'), p = clamp((st.lt - .3) / Math.max(1, th - .3));
    K(R, st, [1050, 520, .95], [960, 480, 1.0]);
    SET.zemin(R);
    // kara (alçak kabartma), Fırat ve Dicle (lacivert oyuk), dağlar
    FIG.sekil(R, [[200, 100], [1700, 60], [1800, 500], [1500, 980], [300, 1000], [150, 600]], .3, .4, null, .6);
    const nehir = (pts) => { R.b.strokeStyle = gv(.18); R.b.lineWidth = 22; R.b.beginPath(); spline(R.b, pts, false); R.b.stroke(); R.m.strokeStyle = '#3B5C99'; R.m.lineWidth = 22; R.m.beginPath(); spline(R.m, pts, false); R.m.stroke(); };
    nehir([[700, 260], [820, 420], [980, 600], [1180, 790], [1330, 900]]); nehir([[980, 230], [1080, 380], [1180, 560], [1300, 760], [1380, 900]]);
    for (let i = 0; i < 9; i++) SET.tepeler(R, 400 + i * 80, 470 + i * 80, 330 - (i % 3) * 20, { h: 60, z: .38 });
    const U = [1300, 860], Hp = [560, 230];
    FIG.cizgi(R, [U, [lerp(U[0], Hp[0], p), lerp(U[1], Hp[1], p)]], 8, .8);
    for (const [q, r] of [[U, 26], [Hp, 26 * clamp(p * 3 - 2)]]) if (r > 0) { R.b.fillStyle = gv(.6); R.b.beginPath(); R.b.arc(q[0], q[1], r, 0, TAU); R.b.fill(); }
    R.L.dir = [-.6, -.5, .6];
  }, { tr: { type: 'muhur', dur: .8 }, over: (c, st) => { etiket(c, 'URUK', 1340, 930, st.lt, 99, { px: 40 }); etiket(c, 'HATTUŞA · Çorum', 560, 160, st.lt - rel(st, 'H08@hattuşa'), 99, { px: 44 }); } });
  // H09: sur üstünde yabancı; sonra yer boşalır ve kile bir parmak izi basılır ("o yabancı sensin")
  sahne('H09a', 'H09', 'surustu', 'orta', (R, st) => {
    const ts = rel(st, 'H09@sensin') - .4, p = clamp((st.lt - ts) / 1.2);
    K(R, st, [960, 520, 1.1], [960, 540, 1.16]);
    SET.zemin(R); DK.tugla(R, -800, 560, 2800, 1400, { z: .5, bw: 120, bh: 46, renk: TUGLA, tohum: 4 });
    FIG.fig(R, 1180, 560, 430, { tip: 'gilgamis', giysi: 'cubbe', f: -1, kol: [[1.4, .1], [.2, .2]] });
    if (p < 1) FIG.fig(R, 760, 560, 410, { tip: 'ursa', f: 1, z: lerp(.78, .18, E.in2(p)), kol: [[.3, .5], [.1, .2]] });
    if (p > .5) YAR.parmakIzi(R, 760, 360, 260, E.out3((p - .5) * 2));
    R.L.dir = [-.85, -.25, .45]; R.L.col = [1.12, .86, .66];
  });
  // H10: geniş, akşam; soru
  sahne('H10a', 'H10', 'uruk', 'genis', (R, st) => {
    K(R, st, [960, 540, .82], [960, 520, .76]);
    SET.zemin(R); DK.sur(R, -800, 2800, 820, 420, { z: .45, renk: TUGLA });
    SET.yer(R, -900, 2900, 820, { z: .36 });
    for (let i = 0; i < 8; i++) DK.hurma(R, -600 + i * 460, 880, 250 + (i % 3) * 40, { z: .52, meyve: true });
    FIG.fig(R, 1100, 330, 150, { tip: 'gilgamis', giysi: 'cubbe', f: -1, z: .62 });
    R.L.dir = [-.9, -.15, .4]; R.L.col = [1.15, .78, .55]; R.L.int = .95;
  }, { over: (c, st) => quote(c, 'Sen hangi suru göstereceksin?', 960, 180, st.lt, { t0: rel(st, 'H10@peki'), px: 70 }) });
  // H11: bitiş ekranı zemini (son ~20 sn): sol yarı boş (bitiş öğeleri), sağda sur ve küçük figür
  sahne('H11a', 'H11', 'son', 'genis', (R, st) => {
    K(R, st, [960, 540, .9], [960, 540, .92]);
    SET.zemin(R); DK.friz(R, -800, 2800, 120, 960);
    DK.sur(R, 1100, 2800, 860, 470, { z: .44, renk: TUGLA, kayma: 120, ara: 420 });
    SET.yer(R, -900, 2900, 860, { z: .34 });
    FIG.fig(R, 1500, 380, 120, { tip: 'gilgamis', giysi: 'cubbe', f: -1, z: .6 });
    R.L.dir = [-.85, -.25, .45]; R.L.col = [1.1, .82, .62]; R.L.int = .9;
  }, { tr: { type: 'fade', dur: .7 } });
})();
