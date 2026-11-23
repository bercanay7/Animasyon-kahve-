// G: Yılan (G01–G10). Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at, yur = (t, k = 4) => ({ bacak: [[Math.sin(t * k) * .32, -.1], [-Math.sin(t * k) * .32, .05]] });
  // G01: yıkanma, temiz giysi
  sahne('G01a', 'G01', 'yikanma', 'orta', (R, st) => {
    K(R, st, [960, 520, 1.1], [960, 520, 1.15]);
    SET.zemin(R); SET.su(R, -900, 2900, 640, { faz: st.lt * .6, alt: 150 }); R.b.fillStyle = gv(.34); R.b.fillRect(-900, 780, 3800, 600); FIG.cizgi(R, [[-900, 780], [2900, 780]], 4, -.6); SET.yer(R, -900, 2900, 870, { z: .36 });
    const tg = rel(st, 'G01@temiz'), p = st.lt > tg ? 1 : 0;
    FIG.fig(R, 860, 880, 540, { tip: 'gilgamis', f: 1, giysi: p ? 'cubbe' : 'post', kol: [[p ? .2 : 2.6, .3], [p ? .1 : 2.4, .3]] });
    if (!p) for (let i = 0; i < 6; i++) { const u = (st.lt * 1.2 + i / 6) % 1; R.b.fillStyle = gv(.7); R.b.beginPath(); R.b.arc(830 + Math.sin(i * 2) * 50, 300 + u * 500, 9, 0, TAU); R.b.fill(); R.m.fillStyle = '#5A7FB8'; R.m.beginPath(); R.m.arc(830 + Math.sin(i * 2) * 50, 300 + u * 500, 9, 0, TAU); R.m.fill(); }
    FIG.fig(R, 1250, 880, 520, { tip: 'ursa', f: -1, kol: [[1.6, .4], [.1, .2]] });
    R.L.dir = [-.55, -.55, .6];
  }, { tr: { type: 'muhur', dur: .8 } });
  // G02: denizin dibinde dikenli bitki (kesit: yüzey üstte, bitki dipte)
  window.DENIZ_KESIT = (R, st) => {
    SET.zemin(R);
    R.b.fillStyle = gv(.16); R.b.fillRect(-900, 300, 3800, 1200); R.m.fillStyle = '#2E4C86'; R.m.fillRect(-900, 300, 3800, 1200);
    SET.su(R, -900, 2900, 290, { faz: st.lt * .7, renk: '#3E5F96' });
    R.b.fillStyle = gv(.36); R.b.beginPath(); R.b.moveTo(-900, 1100); for (let x = -900; x < 2900; x += 80) R.b.lineTo(x, 900 + Math.sin(x / 170) * 30); R.b.lineTo(2900, 1100); R.b.fill();
    R.m.fillStyle = '#5F6E7E'; R.m.beginPath(); R.m.moveTo(-900, 1100); for (let x = -900; x < 2900; x += 80) R.m.lineTo(x, 900 + Math.sin(x / 170) * 30); R.m.lineTo(2900, 1100); R.m.fill();
    for (let i = 0; i < 18; i++) { const u = ((st.lt * .15 + i / 18) % 1); R.d.strokeStyle = dv(.5); R.d.lineWidth = 3; R.d.beginPath(); R.d.arc(200 + i * 100 + Math.sin(i) * 40, 880 - u * 560, 6 + (i % 3) * 3, 0, TAU); R.d.stroke(); }
  };
  sahne('G02a', 'G02', 'deniz', 'genis', (R, st) => {
    K(R, st, [960, 560, .9], [960, 640, 1.0]);
    DENIZ_KESIT(R, st);
    DK.bitki(R, 1100, 905, 230, { z: .78 });
    DK.kayik(R, 700, 280, 460, {});
    FIG.fig(R, 700, 240, 250, { tip: 'utna', f: 1 });
    R.L.dir = [-.3, -.8, .5]; R.L.col = [.85, .92, 1.08]; R.L.int = .8;
    R.L.pts.push({ x: 1100, y: 800, z: 160, r: 380, i: .9, col: [.55, .8, 1.1] });
  }, { over: (c, st) => kunye(c, 'XI. tablet', st.lt, 5) });
  // G03: ayaklarına taş bağlar, dalar, bitkiyi koparır, kıyıya çıkar
  sahne('G03a', 'G03', 'deniz', 'orta', (R, st) => {
    const tk = rel(st, 'G03@kopardı'), tt = rel(st, 'G03@kesti');
    K(R, st, [1000, 620, 1.1], [1000, 680, 1.15]);
    DENIZ_KESIT(R, st);
    DK.bitki(R, 1100, 905, 230, { z: .78 });
    const d = E.io2(clamp(st.lt / Math.max(.5, tk))), u = E.in2(clamp((st.lt - tt) / 1.4));
    const y = lerp(360, 900, d) - u * 700, x = 980;
    FIG.fig(R, x, y, 430, { tip: 'gilgamis', f: 1, giysi: 'pecek', egilme: .2, kol: [[st.lt > tk ? 1.6 : 2.4, .3], [2.2, .3]], bacak: [[.1, 0], [-.05, 0]] });
    if (st.lt < tt) for (const dx of [-20, 40]) { R.b.fillStyle = gv(.82); R.b.beginPath(); R.b.ellipse(x + dx, y + 24, 38, 26, 0, 0, TAU); R.b.fill(); FIG.cizgi(R, [[x + dx, y - 20], [x + dx, y + 10]], 4, .5); }
    R.L.dir = [-.3, -.8, .5]; R.L.col = [.85, .92, 1.08]; R.L.int = .8;
  }, { mb: 2 });
  // G04: bitki elde, adı (ayrıntı)
  sahne('G04a', 'G04', 'bitki', 'ayrinti', (R, st) => {
    K(R, st, [960, 520, 1.5], [960, 500, 1.6]);
    SET.zemin(R); SET.su(R, -900, 2900, 860, { faz: st.lt * .6 });
    FIG.uzuv(R, [1700, 1000], [1150, 680], 130, 100, .78, .5, true); FIG.cizgi(R, [[1200, 650], [1235, 740]], 9, .6);
    DK.bitki(R, 1010, 650, 380, { z: .88 });
    FIG.el(R, 1150, 680, 170, PI + .5, { kapali: true, z: .9 });
    for (let k = 0; k < 4; k++) FIG.cizgi(R, [[1060 + k * 18, 640], [1064 + k * 18, 660]], 4, -.95); // diken çizikleri
    R.L.dir = [-.55, -.55, .6];
  }, { over: (c, st) => buyukSoz(c, 'YAŞLI ADAM GENÇLEŞİR', st.t, A('G04@yaşlı'), { px: 110, y: 170 }) });
  // G05: Urşanabi'yle yürür, bitki elinde
  sahne('G05a', 'G05', 'yol', 'orta', (R, st) => {
    K(R, st, [800, 520, 1.1], [1100, 520, 1.1]);
    SET.zemin(R); SET.tepeler(R, -600, 2800, 720, { h: 200, z: .27 }); SET.yer(R, -900, 2900, 880, { z: .34 });
    const w = st.lt * 70;
    FIG.fig(R, 760 + w, 885, 470, { tip: 'gilgamis', f: 1, giysi: 'cubbe', kol: [[1.1, .5], [.1, .2]], el: { yakin: (R, e, S) => DK.bitki(R, e[0], e[1] + 10, S * .4, { z: .92 }) } });
    FIG.fig(R, 480 + w, 885, 450, { tip: 'ursa', f: 1, kol: [[.3, .3], [.1, .2]], bacak: [[Math.sin(st.lt * 4) * .3, -.1], [-Math.sin(st.lt * 4) * .3, .05]] });
    R.L.dir = [-.55, -.55, .6];
  });
  // G06: serin gölet; suya iner; bitki kıyıda
  sahne('G06a', 'G06', 'golet', 'genis', (R, st) => {
    K(R, st, [960, 470, 1.0], [980, 480, 1.06]);
    SAHNE_GOLET(R, st);
    const p = E.io2(clamp(st.lt / 2.2));
    DK.bitki(R, 640, 610, 170, { z: .8 });
    FIG.fig(R, lerp(820, 1150, p), lerp(610, 800, p), 360, { tip: 'gilgamis', f: 1, giysi: 'pecek', ...yur(st.lt * (1 - p)) }); if (p > .3) GOLET_SU(R, 660, 980, 1500);
    R.L.dir = [-.5, -.7, .55];
  });
  // G07: yılan gelir, bitkiyi alır, derisini bırakır (A01'in cevabı)
  sahne('G07a', 'G07', 'golet', 'yakin', (R, st) => {
    const tc = rel(st, 'G07@çıktı'), ta = rel(st, 'G07@aldı#1'), td = rel(st, 'G07@derisini');
    K(R, st, [760, 540, 1.45], [790, 545, 1.55]);
    SAHNE_GOLET(R, st);
    const g = E.out3(clamp((st.lt - tc + .3) / 1.4)), c = E.io3(clamp((st.lt - ta - .3) / 1.8));
    const bas = [lerp(150, 620, g) - c * 700, lerp(560, 560, g) + c * 30];
    if (st.lt < ta + .2) DK.bitki(R, 640, 610, 170, { z: .8 });
    // deri: geride kalan soluk kabuk (düşük kabartma)
    if (st.lt > td) { const pts = []; for (let i = 0; i < 14; i++) pts.push([560 - i * 26, 590 + Math.sin(i * .8) * 14]); DK.yilan(R, pts, 40, { z: .45 }); }
    const pts = []; for (let i = 0; i < 20; i++) pts.push([bas[0] - i * 34 * (1 - c * .3), bas[1] + 20 + Math.sin(i * .8 - st.lt * 5) * 18]);
    DK.yilan(R, pts, 52, { z: .88 });
    if (st.lt >= ta + .2) DK.bitki(R, bas[0] + 24, bas[1] + 6, 130, { z: .92 });
    FIG.fig(R, 1180, 880, 440, { tip: 'gilgamis', f: -1, giysi: 'pecek', z: .62, kol: [[.6, .4], [.3, .3]] }); GOLET_SU(R, 740, 980, 1500);
    R.L.dir = [-.5, -.7, .55];
  });
  // G08: oturur ve ağlar (deri yanında)
  sahne('G08a', 'G08', 'golet', 'orta', (R, st) => {
    K(R, st, [800, 480, 1.3], [800, 480, 1.36]);
    SAHNE_GOLET(R, st);
    const pts = []; for (let i = 0; i < 14; i++) pts.push([560 - i * 26, 590 + Math.sin(i * .8) * 14]); DK.yilan(R, pts, 40, { z: .45 });
    FIG.fig(R, 900, 640, 440, { tip: 'gilgamis', f: -1, giysi: 'pecek', otur: 1, egilme: .45, bas: .55, kol: [[2.2, 1.6], [2.0, 1.6]], basO: { gozyasi: (st.lt * .4) % 1 } });
    R.L.dir = [-.5, -.7, .55]; R.L.int = .8;
  });
  sahne('G09a', 'G09', 'golet', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'gilgamis', f: -1, arka: 'su', kay: 25, fig: { giysi: 'pecek', bas: .35, basO: { gozyasi: (st.lt * .35) % 1 } } });
    R.L.dir = [-.5, -.7, .55]; R.L.int = .75;
  }, { over: (c, st) => quote(c, '“Kimin için yoruldu bu kollar?”', 960, 170, st.lt, { t0: rel(st, 'G09@kimin'), px: 64 }) });
  // G10: eli boş dönüş: iki küçük figür uzun frizde
  sahne('G10a', 'G10', 'yol', 'genis', (R, st) => {
    K(R, st, [800, 560, .8], [1100, 560, .8]);
    SET.zemin(R); DK.friz(R, -800, 3000, 150, 930);
    SET.tepeler(R, -800, 3000, 820, { h: 150, z: .27 }); SET.yer(R, -800, 3000, 820, { z: .34 });
    FIG.fig(R, 700 + st.lt * 50, 830, 230, { tip: 'gilgamis', giysi: 'cubbe', f: 1, ...yur(st.lt, 3.4), kol: [[.1, .1], [0, .1]] });
    FIG.fig(R, 560 + st.lt * 50, 830, 220, { tip: 'ursa', f: 1, ...yur(st.lt + 1, 3.4) });
    R.L.dir = [.75, -.4, .5]; R.L.col = [1.1, .82, .62]; R.L.int = .85;
  });
})();
