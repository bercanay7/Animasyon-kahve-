// B: Yabani adam (B01–B11). Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at, yur = (t, k = 4) => ({ bacak: [[Math.sin(t * k) * .32, -.1], [-Math.sin(t * k) * .32, .05]] });
  // Uruk'un önünde dev kral (üçte ikisi tanrı)
  sahne('B01a', 'B01', 'uruk', 'genis', (R, st) => {
    K(R, st, [960, 560, .82], [960, 520, .9]);
    SET.zemin(R); DK.friz(R, -600, 2600, 110, 960);
    DK.sur(R, -600, 2600, 860, 430, { z: .42 });
    SET.yer(R, -900, 2900, 860, { z: .36 });
    for (let i = 0; i < 9; i++) FIG.fig(R, 150 + i * 70 + (i > 4 ? 900 : 0), 940, 150, { tip: i % 3 === 2 ? 'kadin' : 'adam', f: i > 4 ? -1 : 1, z: .62, kol: [[.1, .3], [0, .2]] });
    FIG.fig(R, 960, 950, 640, { tip: 'gilgamis', f: 1, kol: [[.25, .5], [-.1, .2]], bas: -.05, el: { yakin: (R, e, S) => FIG.uzuv(R, [e[0], e[1] + S * .45], [e[0], e[1] - S * .3], S * .03, S * .025, .9) } });
    R.L.dir = [-.6, -.5, .6];
  }, { over: (c, st) => etiket(c, 'URUK · bugünkü Irak', 960, 160, st.lt - .4, 4.5) });
  // B02: gençler tuğla taşır; "babasına oğul"da ayrılan baba ve oğul
  sahne('B02a', 'B02', 'uruk', 'orta', (R, st) => {
    K(R, st, [900, 540, 1.0], [1100, 540, 1.05]);
    SET.zemin(R); DK.tugla(R, -800, 150, 2800, 760, { z: .3, bw: 100, bh: 40 });
    SET.yer(R, -900, 2900, 860, { z: .36, cimen: false });
    for (let i = 0; i < 5; i++) { const x = -100 + i * 260 + st.lt * 70; const f = FIG.fig(R, x, 880, 340, { tip: 'adam', f: 1, egilme: .3, ...yur(st.lt + i), kol: [[2.6, .4], [2.5, .3]] });
      DK.tugla(R, f.bas[0] - 60, f.bas[1] - 115, f.bas[0] + 60, f.bas[1] - 50, { z: .84, bw: 60, bh: 22 }); }
    const tb = rel(st, 'B02@babasına'), pp = clamp((st.lt - tb) / 2.5);
    FIG.fig(R, 1700, 880, 360, { tip: 'adam', f: -1, kol: [[1.4 - pp * .2, .1], [.2, .2]], sakal: true });
    FIG.fig(R, 1500 - pp * 200, 880, 260, { tip: 'cocuk', f: 1, kol: [[.2, .1], [-1.2 * (1 - pp), .2]], ...yur(pp * 4) });
    R.L.dir = [-.6, -.55, .6];
  });
  // B03: büyük el kili koparır; bozkırda Enkidu kilden yükselir
  sahne('B03a', 'B03', 'bozkir', 'yakin', (R, st) => {
    K(R, st, [960, 540, 1.0], [960, 560, 1.08]);
    SET.zemin(R);
    const tk = rel(st, 'B03@kopardı'), ta = rel(st, 'B03@attı'), tE = rel(st, 'B03@doğdu');
    // tanrıça figürle değil ışıkla: gökten inen ışık, kil yığınından bir parça koparır (CLAUDE.md: tanrı ışıkla gösterilir)
    const hp = clamp((st.lt - tk) / 1.2), yp = clamp((st.lt - ta) / 1.0);
    FIG.sekil(R, [[560, 885], [640, 760], [760, 730], [860, 770], [920, 885]], .5, .5, null, .8); // kil yığını
    if (hp > 0 && yp <= 0) { R.b.fillStyle = gv(.6 + .2 * hp); R.b.beginPath(); R.b.arc(760, 730 - hp * 80, 34, 0, TAU); R.b.fill(); }
    const [lx, ly] = R.scr(760, 300); R.L.pts.push({ x: lx, y: ly, z: 400 * R.z, r: 900 * R.z, i: .7 * clamp(st.lt / 1.0), col: [1.15, 1.0, .82] });
    R.after(c => { c.globalCompositeOperation = 'screen'; const g = c.createLinearGradient(760, 0, 760, 760); g.addColorStop(0, `rgba(255,235,190,${.45 * clamp(st.lt / 1.0)})`); g.addColorStop(1, 'rgba(255,235,190,0)'); c.fillStyle = g; c.beginPath(); c.moveTo(700, 0); c.lineTo(820, 0); c.lineTo(900, 760); c.lineTo(620, 760); c.fill(); });
    // atılan kil topağı yayla düşer
    if (yp > 0 && yp < 1) { const x = lerp(760, 1180, yp), y = lerp(650, 840, yp) - Math.sin(yp * PI) * 220; R.b.fillStyle = gv(.8); R.b.beginPath(); R.b.arc(x, y, 34, 0, TAU); R.b.fill(); }
    SET.tepeler(R, -600, 2600, 880, { h: 160, z: .26 }); SET.yer(R, -900, 2900, 880, { z: .3 });
    // Enkidu kilden yükselir: kabartma yüksekliği zeminden figüre
    const ez = clamp((st.lt - tE + .8) / 1.8);
    if (ez > 0) FIG.fig(R, 1180, 890, 470, { tip: 'enkidu', f: -1, z: lerp(.22, .8, E.out3(ez)), otur: 1 - ez, egilme: .4 * (1 - ez), kol: [[.2, .3], [-.1, .2]], tohum: 1 });
    R.L.dir = [-.5, -.6, .6];
  }, { tr: { type: 'muhur', dur: .8 } });
  // B04: bozkırda ceylanlarla otlar, sudan içer
  sahne('B04a', 'B04', 'bozkir', 'genis', (R, st) => {
    K(R, st, [800, 560, .9], [1100, 560, .95]);
    SET.zemin(R); SET.tepeler(R, -600, 2700, 700, { h: 180, z: .26 });
    SET.yer(R, -900, 2900, 830, { z: .33 });
    SET.golet(R, 1300, 900, 330, 50, { faz: st.lt });
    for (let i = 0; i < 5; i++) DK.ceylan(R, 500 + i * 200 + Math.sin(st.lt * .5 + i) * 10, 840, 200 + (i % 2) * 30, { f: i % 2 ? -1 : 1, z: .6 + (i % 2) * .06 });
    FIG.fig(R, 1180, 845, 380, { tip: 'enkidu', f: 1, egilme: .25 + Math.sin(st.lt) * .05, kol: [[.9, .4], [.6, .3]], tohum: 4 });
    R.L.dir = [-.6, -.5, .6];
  });
  // B05: Şamhat gelir
  sahne('B05a', 'B05', 'bozkir', 'orta', (R, st) => {
    K(R, st, [1000, 540, 1.15], [960, 540, 1.2]);
    SET.zemin(R); SET.tepeler(R, -600, 2700, 700, { h: 150, z: .26 }); SET.yer(R, -900, 2900, 880, { z: .33 });
    const w = Math.min(st.lt, 3) * 60;
    FIG.fig(R, 1500 - w, 885, 470, { tip: 'samhat', f: -1, kol: [[.5, .6], [.1, .2]], ...yur(Math.min(st.lt, 3), 3.5) });
    FIG.fig(R, 650, 885, 480, { tip: 'enkidu', f: 1, kol: [[.15, .2], [0, .2]], bas: -.08, tohum: 4 });
    DK.ceylan(R, 330, 880, 230, { f: 1, z: .6 });
    R.L.dir = [-.55, -.55, .6];
  }, { over: (c, st) => etiket(c, 'ŞAMHAT', 1320, 200, st.lt - 1.2, 3.5) });
  // B06: altı gün yedi gece (ışık yedi kez döner), sonra ceylanlar kaçar
  sahne('B06a', 'B06', 'bozkir', 'genis', (R, st) => {
    const tk = rel(st, 'B06@kaçtı') - .9;
    K(R, st, [960, 560, .95], [960, 560, 1.0]);
    SET.zemin(R); SET.tepeler(R, -600, 2700, 700, { h: 180, z: .26 }); SET.yer(R, -900, 2900, 860, { z: .33 });
    SET.golet(R, 480, 930, 260, 40, { faz: st.lt });
    const pk = clamp((st.lt - tk) / 2.5);
    FIG.fig(R, 900, 865, 420, { tip: 'samhat', f: 1, otur: 1, kol: [[.6, .5], [.2, .3]] });
    FIG.fig(R, 1140, 865, 430, { tip: 'enkidu', f: pk > .05 ? 1 : -1, otur: 1 - pk, kol: [[.4 + pk * 1.0, .4], [.1, .2]], tohum: 4 });
    for (let i = 0; i < 4; i++) DK.ceylan(R, 1350 + i * 170 + E.in2(pk) * (500 + i * 120), 860, 190, { f: 1, z: .6, kos: pk > 0 ? st.lt * 9 + i : 0 });
    // ışık: yedi gün dönüşü (yalnız "altı gün yedi gece" boyunca)
    const gd = clamp((st.lt - .2) / Math.max(1, tk - .2)), a = gd * 7 * TAU;
    if (gd < 1) { R.L.dir = [Math.cos(a) * .8, -.5 - Math.abs(Math.sin(a)) * .2, .55]; const gece = .5 + .5 * Math.cos(a + PI); R.L.int = lerp(1.0, .3, gece); R.L.col = [lerp(1, .6, gece), lerp(.96, .68, gece), lerp(.88, .9, gece)]; }
    else R.L.dir = [-.6, -.5, .6];
  });
  sahne('B07a', 'B07', 'bozkir', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'enkidu', f: 1, arka: 'tepe', kay: 40, fig: { tohum: 4, bas: .08 } });
    R.L.dir = [-.6, -.45, .6];
  });
  // B08: ekmek, yedi testi, giysi
  sahne('B08a', 'B08', 'ekmek', 'orta', (R, st) => {
    const te = rel(st, 'B08@ekmek'), tb = rel(st, 'B08@bira'), tg = rel(st, 'B08@giysisini');
    K(R, st, [960, 520, 1.15], [960, 540, 1.2]);
    SET.zemin(R); SET.yer(R, -900, 2900, 880, { z: .33 });
    const gp = clamp((st.lt - tg) / 2.0);
    FIG.fig(R, 1260, 885, 520, { tip: 'samhat', f: -1, kol: [[1.4, .3], [.2, .3]], el: { yakin: (R, e) => { if (st.lt > te && st.lt < tb + .3) YAR.ekmek(R, e[0] + 10, e[1] + 10, 46, 0); } } });
    FIG.fig(R, 720, 885, 520, { tip: 'enkidu', f: 1, kol: [[1.2, .4], [.3, .3]], giysi: gp > .5 ? 'etek' : 'pecek', tohum: 4 });
    const n = clamp(Math.floor((st.lt - tb) / .25), 0, 7);
    for (let i = 0; i < n; i++) YAR.testi(R, 860 + i * 58, 880, 90);
    if (gp > 0 && gp < .5) { const x = lerp(1180, 760, gp * 2); FIG.sekil(R, [[x - 70, 560], [x + 70, 560], [x + 90, 760], [x - 90, 760]], .86, .5); }
    R.L.dir = [-.55, -.55, .6];
  });
  // B09: üç nesne yan yana (ayrıntı)
  window.UC_NESNE = (R, k = 3, x0 = 560) => {
    if (k > 0) YAR.ekmek(R, x0, 640, 120, 0);
    if (k > 1) YAR.testi(R, x0 + 400, 700, 280);
    if (k > 2) { const x = x0 + 800; FIG.sekil(R, [[x - 60, 420], [x - 20, 440], [x + 20, 440], [x + 60, 420], [x + 190, 480], [x + 160, 540], [x + 90, 515], [x + 110, 720], [x - 110, 720], [x - 90, 515], [x - 160, 540], [x - 190, 480]], .7, .55, null, 0); for (let q = 0; q < 6; q++) FIG.cizgi(R, [[x - 80 + q * 32, 540], [x - 90 + q * 36, 710]], 3, -.45); for (let q = 0; q < 12; q++) FIG.cizgi(R, [[x - 110 + q * 20, 720], [x - 110 + q * 20, 748]], 3, .6); }
  };
  sahne('B09a', 'B09', 'nesne', 'ayrinti', (R, st) => {
    K(R, st, [960, 560, 1.0], [960, 560, 1.12]);
    SET.zemin(R); DK.tablet(R, 960, 590, 1500, 560, { z: .4, yazi: false });
    UC_NESNE(R, 1 + Math.floor(clamp(st.lt / .7) * 2.99));
    R.L.dir = [-.7, -.4, .5];
  });
  // B10: kapıda boğuşma; eşik yıkılır, duvar sarsılır
  sahne('B10a', 'B10', 'kapi', 'genis', (R, st) => {
    K(R, st, [960, 520, .9], [960, 520, .95]);
    SET.zemin(R); DK.sur(R, -600, 2600, 860, 380, { z: .4, kayma: 300, ara: 1100 });
    R.b.fillStyle = gv(.12); R.b.fillRect(820, 470, 300, 390); FIG.cizgi(R, [[820, 860], [820, 470], [1120, 470], [1120, 860]], 8, .7);
    SET.yer(R, -900, 2900, 860, { z: .36, cimen: false });
    const w = Math.min(st.lt, 2.2) * 120;
    FIG.fig(R, 1100, 870, 380, { tip: 'enkidu', f: -1, kol: [[.4, .4], [.1, .2]], bacak: [[.5, -.2], [-.1, .05]], tohum: 4 });
    FIG.fig(R, 300 + w, 870, 380, { tip: 'gilgamis', f: 1, ...yur(Math.min(st.lt, 2.2)), kol: [[.3, .4], [-.2, .2]] });
    R.L.dir = [-.6, -.5, .6];
  });
  sahne('B10b', 'B10@boğuştular', 'kapi', 'orta', (R, st) => {
    const ty = rel(st, 'B10@yıktılar'), ts = rel(st, 'B10@sarstılar'), sh = st.lt > ts ? Math.sin(st.lt * 40) * 6 * clamp(1 - (st.lt - ts)) : 0;
    K(R, st, [960 + sh, 520, 1.15], [960 + sh, 530, 1.2]);
    SET.zemin(R); DK.tugla(R, 300, 120, 1700, 860, { z: .3, bw: 100, bh: 40 });
    if (st.lt > ts) for (let k = 0; k < 3; k++) FIG.cizgi(R, [[700 + k * 300, 120], [740 + k * 300, 300], [690 + k * 300, 420]], 5, -.95);
    const yy = clamp((st.lt - ty) / .6); R.b.fillStyle = gv(.4 - yy * .2); R.b.fillRect(300, 860, 1400, 50);
    if (yy > 0) for (let k = 0; k < 6; k++) { R.b.fillStyle = gv(.6); R.b.fillRect(500 + k * 160, 860 + yy * 40, 70, 30); }
    const s = Math.sin(st.lt * 3) * .08;
    FIG.fig(R, 790, 900, 620, { tip: 'gilgamis', f: 1, egilme: .38 + s, kol: [[1.5, .2], [1.2, .6]], bacak: [[.4, -.2], [-.35, .1]] });
    FIG.fig(R, 1150, 900, 630, { tip: 'enkidu', f: -1, egilme: .38 - s, kol: [[1.4, .4], [1.0, .7]], bacak: [[.35, -.1], [-.4, .15]], tohum: 3 });
    R.L.dir = [-.6, -.5, .6];
  }, { mb: 3 });
  // B11: öfke diner, yan yana dost
  sahne('B11a', 'B11', 'kapi', 'yakin', (R, st) => {
    K(R, st, [960, 420, 1.65], [960, 410, 1.75]);
    SET.zemin(R); DK.tugla(R, 300, 120, 1700, 860, { z: .3, bw: 100, bh: 40 });
    SET.yer(R, 200, 1800, 860, { z: .36, cimen: false });
    const p = E.io3(clamp(st.lt / 2.5));
    FIG.fig(R, 830, 880, 600, { tip: 'gilgamis', f: 1, egilme: .3 * (1 - p), kol: [[lerp(1.5, .9, p), lerp(.2, .2, p)], [.1, .2]] });
    FIG.fig(R, 1110, 880, 610, { tip: 'enkidu', f: -1, egilme: .3 * (1 - p), kol: [[lerp(1.4, .95, p), .2], [.1, .2]], tohum: 3 });
    R.L.dir = [-.6, -.5, .6]; R.L.col = [1.05, .95, .85];
  });
})();
