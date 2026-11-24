// D: III. Duvardaki yarık (D01–D13): yaratık kendi ağzından; ışığın merkezi onda. Aile yalnız duvardaki yarıktan görülür (dar dikey kadraj).
// Renk mevsimle gelir: kış mavi-gri → ilkbahar yeşili (D08–D10) → yansımada soğur. Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  const KARE = { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 };
  const YARIK = { tip: 'kare', x: 960, y: 500, w: 420, h: 900, r: 160, yum: 50 };
  sahne('D00k', 'D01-1.4', 'kart', 'kart', (R, st) => { R.cam(960, 540, 1); SET.kart(R, st, 'III', 'DUVARDAKİ YARIK', 'Kimse sana bakmazsa ne öğrenirsin?'); },
    { fener: { isik: { x: 960, y: 480, r: 900 }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1500, h: 860, yum: 30 } }, tr: { type: 'iris', dur: 1.2 } });
  window.ORMAN_GECE = (R, st, o = {}) => {
    R.gok(-800, -400, 3600, 1000, [[0, o.gok1 || '#2C3A66'], [.7, o.gok2 || '#4C5E8E'], [1, '#6E7B9E']], { firca: 1.1 });
    if (o.ay) DK.ay(R, o.ay[0], o.ay[1], o.ay[2] || 60);
    for (let i = 0; i < 9; i++) DK.cam(R, -600 + i * 430 + (i % 3) * 60, 900, 520 + (i % 4) * 90, { tohum: 30 + i, sal: Math.sin(st.t * .6 + i) * .5 });
    R.yika(g => g.rect(-800, 880, 4400, 600), o.yer || '#3A4A3A', { firca: 1 });
    R.kara(g => { g.moveTo(-800, 900); for (let x = -800; x <= 3600; x += 80) g.lineTo(x, 890 + Math.sin(x * .013) * 10); g.lineTo(3600, 1400); g.lineTo(-800, 1400); g.closePath(); });
  };
  // D01: duyuların karışıklığı: "ışık"ta parlar, "karanlık"ta söner, "açlık"ta kıvrılır, "soğuk"ta pelerine sarılır
  sahne('D01a', 'D01+2.2', 'orman', 'orta', (R, st) => {
    R.cam(960, 600, 1.15);
    ORMAN_GECE(R, st, { gok1: '#3A4A70' });
    const so = E.io3(clamp((st.lt - rel(st, 'D01@soğuk')) / .8)), ac = E.io3(clamp((st.lt - rel(st, 'D01@açlık')) / .8));
    FIG.kisi(R, 960, 900, 560, { tip: 'yaratik', f: 1, bacak: 'cok', govde: .3 + ac * .2, bas: .3, kolO: [lerp(.5, .7, so), lerp(.6, 2.2, so)], kolA: [lerp(.3, .5, so), lerp(.5, 2.3, so)], goz: 1 });
  }, { fener: st => { const tI = A('D01@işık') - st.at, tK = A('D01@karanlık') - st.at; const p = st.lt < tK ? 1 + .4 * Math.max(0, 1 - Math.abs(st.lt - tI) / .6) : .35 + .65 * clamp((st.lt - tK - 1.2) / 1.5);
    return { isik: { x: 960, y: 520, r: 560 }, kadraj: { tip: 'daire', x: 960, y: 540, r: 470, yum: 50 }, parlak: p }; } });
  // D02: ay yükselir (üslup kapısının yürüyüş planı)
  sahne('D02a', 'D02', 'orman', 'genis', (R, st) => {
    const tY = rel(st, 'D02@yükseldi');
    const go = t => HAREKET.rampa(t, 0, .4) * (1 - HAREKET.rampa(t, tY + .2, tY + .9));
    const g = HAREKET.yuruyus({ tip: 'yuru', tur: 1.25 });
    const y = HAREKET.yuruyusYolu(g, { t0: 0, t1: 30, x0: 420, olcek: 7.4, go })(st.lt);
    const ayY = lerp(780, 300, E.out3(clamp((st.lt - tY) / 2.6)));
    R.cam(900 + y.x * .3, 540, 1);
    ORMAN_GECE(R, st, { ay: [1560, ayY, 70] });
    const bak = E.io3(clamp((st.lt - tY - .4) / 1.2));
    FIG.kisi(R, y.x, 900, 640, { tip: 'yaratik', f: 1, bacak: y.poz, bas: -bak * .35, govde: .08 - bak * .06, kolO: [.15 + Math.sin(TAU * y.faz) * .3 * y.go + bak * .25, .35], kolA: [-.1 - Math.sin(TAU * y.faz) * .3 * y.go, .3], pel: Math.sin(st.lt * 2) * .5 });
  }, { fener: { isik: { x: 960, y: 520, r: 760, sic: [.95, .95, 1] }, kadraj: KARE } });
  // D03: kuşlar dalda; ağzını açar, kuşlar kaçar (yakın)
  sahne('D03a', 'D03', 'orman', 'yakin', (R, st) => {
    const tK = rel(st, 'D03@korkuttu');
    R.cam(1100, 420, 1.8);
    ORMAN_GECE(R, st, { gok1: '#5A6E96', gok2: '#8A9CB8' });
    R.cizgi([[1060, 290], [1500, 270], [1900, 310]], 10, { egri: true }); for (const x of [1200, 1420, 1650]) R.cizgi([[x, 280], [x + 50, 230], [x + 90, 220]], 5, { egri: true });
    for (let i = 0; i < 4; i++) { const u = clamp((st.lt - tK + .6 - i * .1) / 1.5), x = 1300 + i * 90 + u * 600 * (i % 2 ? 1 : .7), y = 270 - 14 - u * 300 + Math.sin(u * 20 + i) * 10;
      R.kara(g => { g.ellipse(x, y, 16, 11, 0, 0, TAU); g.ellipse(x + 13, y - 8, 7, 7, 0, 0, TAU); g.moveTo(x - 14, y); g.lineTo(x - 30, y + 4); g.lineTo(x - 14, y + 6); if (u > 0) { const k = Math.sin(st.lt * 30 + i) * 12; g.moveTo(x, y - 4); g.lineTo(x - 14, y - 26 - k); g.lineTo(x + 6, y - 6); } }); }
    FIG.kisi(R, 800, 1180, 720, { tip: 'yaratik', f: 1, bas: -.35, govde: -.04, kolO: [.3, .4], goz: 1, kenar: 'rgba(230,230,250,.7)' });
  }, { fener: { isik: { x: 1000, y: 420, r: 560, sic: [.95, .95, 1] }, kadraj: { tip: 'oval', x: 980, y: 480, w: 1400, h: 900, yum: 40 } } });
  // D04: gezginlerin ateşi; el közlere uzanır, geri çekilir (el zinciri)
  sahne('D04a', 'D04', 'orman', 'orta', (R, st) => {
    const tS = rel(st, 'D04@soktum'), tC = rel(st, 'D04@çektim');
    R.cam(1060, 620, 1.25);
    R.gok(-800, -400, 3600, 1000, [[0, '#3A4A70'], [1, '#6E7B9E']], { firca: 1.1 }); R.kara(g => g.rect(-800, 890, 4400, 600));
    DK.ates(R, 1260, 880, 230, { t: st.t });
    const u = st.lt < tS ? E.io3(clamp((st.lt - tS + 1.2) / 1.2)) : st.lt < tC ? 1 : 1 - E.outBack(clamp((st.lt - tC) / .4));
    FIG.kisi(R, 880, 900, 560, { tip: 'yaratik', f: 1, bacak: 'cok', govde: .3 + u * .15, bas: .2, kolO: [lerp(.7, 1.6, u), lerp(.6, .15, u)], kolA: [.4, .5], goz: 1 });
  }, { fener: { isik: { x: 1000, y: 620, r: 560, sic: [1, .85, .62] }, kadraj: { tip: 'oval', x: 960, y: 560, w: 1500, h: 900, yum: 40 } } });
  // D05: köy: kapıdan çocuklar kaçar, taşlar uçar
  sahne('D05a', 'D05', 'koy', 'genis', (R, st) => {
    R.cam(980 + st.lt * 16, 560, 1.0);
    R.gok(-800, -400, 3600, 900, [[0, '#B48E6A'], [1, '#E4C29A']], { firca: 1.2 });
    for (let i = 0; i < 3; i++) { const x = 300 + i * 420, h = 260 + (i % 2) * 60; R.kara(g => { g.rect(x, 880 - h, 300, h); g.moveTo(x - 30, 880 - h); g.lineTo(x + 150, 880 - h - 140); g.lineTo(x + 330, 880 - h); g.closePath(); }); R.isikli(g => g.rect(x + 120, 880 - h + 70, 50, 70), '#F2C27A'); }
    R.yika(g => g.rect(-800, 880, 3600, 600), '#6A5A48', { firca: 1 });
    const g = HAREKET.yuruyus({ tip: 'kos', uyluk: 23, baldir: 23, tur: .55 });
    const y = HAREKET.yuruyusYolu(g, { t0: 0, t1: 8, x0: 1500, yon: -1, olcek: 4.6, go: t => HAREKET.rampa(t, .2, .6) })(st.lt);
    FIG.kisi(R, y.x, 980, 600, { tip: 'yaratik', f: -1, bacak: y.poz, govde: .2, kolO: [1.4, 1.3], kolA: [1.2, 1.4], pel: Math.sin(st.lt * 5) });
    for (let i = 0; i < 3; i++) FIG.kisi(R, 1620 + i * 130, 980, 300 + i * 30, { tip: i === 1 ? 'kiz' : 'koylu', f: -1, kolO: [i === 1 ? .6 : 1.0, .9], govde: .05 });
    const tT = rel(st, 'D05@taşlarla');
    for (let i = 0; i < 6; i++) { const u = (st.lt - tT - i * .25); if (u < 0 || u > 1.2) continue; const x = lerp(1700, y.x + 60, u / 1.2), yy = 700 - Math.sin(u / 1.2 * PI) * 200 + i * 10; R.kara(g => g.ellipse(x, yy, 10, 8, u * 3, 0, TAU)); }
  }, { fener: { isik: { x: 960, y: 520, r: 820, sic: [1, .9, .76] }, kadraj: KARE } });
  // odunluk ve yarık: dışarıdan kulübe duvarı (genis), içeriden yarıktan aile (dar dikey kadraj)
  window.KULUBE_IC = (R, st, o = {}) => {
    R.gok(-600, -400, 2600, 1500, [[0, o.duvar1 || '#E6B878'], [1, o.duvar2 || '#C49058']], { firca: 1.3 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#5A4232', { firca: 1 });
    DK.ates(R, 1260, 870, 170, { t: st.t });
    R.kara(g => { g.rect(1120, 560, 280, 30); g.rect(1130, 590, 40, 290); g.rect(1350, 590, 40, 290); });   // ocak
    DK.masa(R, 760, 770, 260, { h: 110 });
  };
  sahne('D06a', 'D06', 'odunluk', 'orta', (R, st) => {
    R.cam(900 + st.lt * 10, 560, 1.0);
    R.gok(-600, -400, 2600, 900, [[0, '#7A8CA8'], [1, '#B9C2CE']], { firca: 1.2 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#E2E6EC', { firca: .8 });   // kar
    // kulübe (sağ) + bitişik alçak odunluk (sol)
    R.kara(g => { g.rect(980, 460, 700, 430); g.moveTo(940, 460); g.lineTo(1330, 230); g.lineTo(1720, 460); g.closePath(); g.rect(560, 640, 420, 250); g.moveTo(540, 640); g.lineTo(980, 560); g.lineTo(980, 640); g.closePath(); });
    R.isikli(g => { g.rect(1180, 560, 90, 110); g.rect(1440, 560, 90, 110); }, '#F2C27A');
    const k = E.io3(clamp((st.lt - rel(st, 'D06@yarık')) / 1));
    R.isikli(g => g.rect(972, 700, 16, 120), `rgba(250,200,120,${k})`);   // yarıktan sızan ışık
    const g = HAREKET.yuruyus({ tip: 'yuru', tur: 1.2 });
    const y = HAREKET.yuruyusYolu(g, { t0: 0, t1: 9, x0: 0, olcek: 4.2, go: t => 1 - HAREKET.rampa(t, 2.4, 3.2) })(st.lt);
    const ic = clamp((st.lt - 3.2) / 1);
    if (ic < 1) FIG.kisi(R, y.x + 200, 890, 360, { tip: 'yaratik', f: 1, bacak: y.poz, govde: .1, pel: .3, kolO: [.2 + Math.sin(TAU * y.faz) * .3 * y.go, .4] });
  }, { fener: { isik: { x: 960, y: 520, r: 820, sic: [.96, .96, 1] }, kadraj: KARE } });
  sahne('D06b', 'D06@oradan', 'yarik', 'yakin', (R, st) => {
    R.cam(890, 760, 1.55);
    KULUBE_IC(R, st);
    const g = n => E.out3(clamp((st.lt - rel(st, n) + .3) / .8));
    FIG.kisi(R, 800, 980, 420, { tip: 'ihtiyar', f: 1, bacak: 'otur', kolO: [.8, 1.0] });
    FIG.kisi(R, lerp(1300, 930, g('D06@kızı')), 980, 400, { tip: 'kiz', f: -1 });
    FIG.kisi(R, lerp(1400, 1020, g('D06@oğlu')), 980, 440, { tip: 'genc', f: -1 });
  }, { fener: { isik: { x: 900, y: 520, r: 520, sic: [1, .88, .66] }, kadraj: YARIK } });
  // D07: yoksul sofra; yaratık yiyecekten el çeker (yarıktan; sonra odunlukta kökler)
  sahne('D07a', 'D07', 'yarik', 'ayrinti', (R, st) => {
    R.cam(830 + st.lt * 8, 760, 2.0 + st.lt * .03);
    KULUBE_IC(R, st);
    FIG.kisi(R, 700, 980, 420, { tip: 'ihtiyar', f: 1, bacak: 'otur', kolO: [1.3, .8] });
    FIG.kisi(R, 960, 980, 400, { tip: 'kiz', f: -1, bacak: 'otur', kolO: [1.2, .9] });
    const al = E.io3(clamp((st.lt - rel(st, 'D07@çalıyordum') + .4) / .9)) * (1 - E.io3(clamp((st.lt - rel(st, 'D07@bıraktım') + .2) / .9)));
    R.isikli(g => g.ellipse(830 + al * 260, 762 - al * 30, 30, 8, 0, 0, TAU), '#E8D6A8');   // tek parça ekmek
    if (al > .01) FIG.elYakin(R, 1240 - (1 - al) * 300 + al * 40, 752 - al * 30, 4.2, -1, true, al);
  }, { fener: { isik: { x: 860, y: 520, r: 460, sic: [1, .88, .66] }, kadraj: YARIK } });
  // D08: gece odun keser, kapıya yığar (ay)
  sahne('D08a', 'D08', 'odunluk', 'orta', (R, st) => {
    R.cam(1000, 600, 1.2);
    ORMAN_GECE(R, st, { ay: [1500, 260, 60], yer: '#4A5A4A' });
    R.kara(g => { g.rect(1100, 560, 700, 360); g.moveTo(1070, 560); g.lineTo(1450, 380); g.lineTo(1830, 560); g.closePath(); }); R.isikli(g => g.rect(1500, 640, 70, 80), '#F2C27A');
    const n = Math.min(6, Math.floor(st.lt * 2.2));
    for (let i = 0; i < n; i++) R.kara(g => g.ellipse(1180 - (i % 3) * 34, 900 - Math.floor(i / 3) * 26, 60, 13, 0, 0, TAU));
    const k = Math.sin(st.lt * 6);
    FIG.kisi(R, 860, 920, 560, { tip: 'yaratik', f: 1, govde: .3 + k * .1, kolO: [1.6 - k * .6, .4], kolA: [1.4 - k * .6, .5], goz: 1, pel: k * .4,
      el: { on: (R2, e) => { const g = R2.g, ux = Math.sin(e.a), uy = Math.cos(e.a), q = [e.e[0] + ux * 16, e.e[1] + uy * 16]; FIG.uzuv(g, e.e, q, 1.6, 1.6); g.save(); g.translate(q[0], q[1]); g.rotate(-e.a); g.beginPath(); g.moveTo(-1, -1); g.lineTo(5, -2); g.quadraticCurveTo(7, 1, 5, 4); g.lineTo(-1, 2); g.closePath(); g.fill(); g.restore(); } } });
  }, { fener: { isik: { x: 1000, y: 560, r: 620, sic: [.95, .95, 1] }, kadraj: KARE } });
  // D09: sabah kız kapıyı açar, odun yığını; "görünmeyen bir el": yarıkta yaratığın gözü
  sahne('D09a', 'D09', 'kapi', 'genis', (R, st) => {
    R.cam(960 + st.lt * 10, 560, 1.0 + st.lt * .02);
    R.gok(-600, -400, 2600, 900, [[0, '#A9C2A0'], [1, '#DCE6C6']], { firca: 1.2 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#7E9A6A', { firca: 1 });
    R.kara(g => { g.rect(700, 440, 900, 460); g.moveTo(660, 440); g.lineTo(1150, 200); g.lineTo(1640, 440); g.closePath(); g.rect(340, 640, 360, 260); g.moveTo(320, 640); g.lineTo(700, 560); g.lineTo(700, 640); g.closePath(); });
    const ac = E.io3(clamp(st.lt / .8));
    R.isikli(g => g.rect(1000, 520, 150 * ac, 380), '#F0D8A0');
    for (let i = 0; i < 6; i++) R.kara(g => g.ellipse(860 - (i % 3) * 40, 890 - Math.floor(i / 3) * 26, 64, 14, 0, 0, TAU));
    const bak = Math.sin(clamp((st.lt - 2.5) / 3) * PI * 2);
    FIG.kisi(R, 1070, 900, 330, { tip: 'kiz', f: bak > .3 ? 1 : -1, kolO: [lerp(.2, 1.6, clamp((st.lt - .6) / .5)), 1.2], kolA: [.3, 1.4] });
    if (st.lt > rel(st, 'D09@kendi') - .5) FIG.kisi(R, lerp(1110, 1260, E.io3(clamp((st.lt - rel(st, 'D09@kendi') + .5) / 1))), 900, 360, { tip: 'genc', f: -1, kolO: [1.3, .9] });
    R.yika(g => g.rect(688, 700, 10, 90), 'rgba(40,30,20,1)', { kay: 0 }); R.nokta(693, 742, 4, '#C98A2E');   // odunluk duvarındaki yarıkta göz
  }, { fener: { isik: { x: 960, y: 560, r: 820, sic: [1, .97, .9] }, kadraj: KARE },
    over: (ctx, st) => { etiket(ctx, '“İYİ RUH”', 960, 170, st.lt - rel(st, 'D09@iyi'), st.d - rel(st, 'D09@iyi'), { px: 56 }); } });
  // D10: aile sözcükleri (yarıktan, ilkbahar); sonra odunlukta yalnız yaratık
  sahne('D10a', 'D10', 'yarik', 'orta', (R, st) => {
    R.cam(880 + st.lt * 6, 740, 1.45 + st.lt * .03);
    KULUBE_IC(R, st, { duvar1: '#E6C890', duvar2: '#C4A468' });
    FIG.kisi(R, 680, 980, 420, { tip: 'ihtiyar', f: 1, bacak: 'otur', kolO: [1.0, 1.0] });
    FIG.kisi(R, lerp(980, 820, E.io3(clamp((st.lt - rel(st, 'D10@anne')) / 1.2))), 980, 400, { tip: 'kiz', f: -1, kolO: [lerp(0, 1.0, E.io3(clamp((st.lt - rel(st, 'D10@anne')) / 1.2))), .8] });
    FIG.kisi(R, 1060, 980, 440, { tip: 'genc', f: -1, bacak: st.lt > rel(st, 'D10@kardeş') ? 'otur' : 'dur' });
    for (const [s, k, y] of [['BABA', 'baba', 160], ['ANNE', 'anne', 250], ['KARDEŞ', 'kardeş', 340]]) SET.camYazi(R, s, 960, y, { px: 64, ls: 10, p: clamp((st.lt - rel(st, 'D10@' + k)) / .4) });
  }, { fener: { isik: { x: 880, y: 520, r: 520, sic: [1, .9, .7] }, kadraj: YARIK } });
  sahne('D10b', 'D10@benim', 'odunluk', 'yakin', (R, st) => {
    R.cam(980 - st.lt * 8, 560, 1.4 + st.lt * .035);
    R.gok(-600, -400, 2600, 1500, [[0, '#4A4A58'], [1, '#34343E']], { firca: 1.4 });
    R.isikli(g => g.rect(1240, 300, 14, 600), 'rgba(250,200,120,.8)');
    const kb = E.io3(clamp((st.lt - rel(st, 'D10@neredeydi')) / .8)) * (1 - E.io3(clamp((st.lt - rel(st, 'D10@olmadı')) / 1.4)));
    FIG.kisi(R, 900, 1000, 640, { tip: 'yaratik', f: 1, bacak: 'cok', govde: .55 - kb * .35, bas: .6 - kb * .8, kolO: [.7, 1.1], kolA: [.6, 1.2], goz: 1 });
  }, { fener: { isik: { x: 960, y: 560, r: 440 }, kadraj: { tip: 'daire', x: 960, y: 560, r: 420, yum: 40 }, parlak: .85 } });
  // D11: su yansıması; geri sıçrar (yakın)
  sahne('D11a', 'D11', 'su', 'orta', (R, st) => {
    const tS = rel(st, 'D11@sıçradım');
    R.cam(960, 470, 1.0);
    R.gok(-600, -400, 2600, 700, [[0, '#8FA88A'], [1, '#B9C8A6']], { firca: 1.2 });
    R.yika(g => g.rect(-600, 620, 3200, 900), '#6E8A8E', { firca: 1 });
    const u = st.lt < tS ? 0 : E.outBack(clamp((st.lt - tS) / .5));
    const egil = lerp(.9, .2, u);
    // yansıma (su yüzeyinde ters, dalgalı)
    R.g.save(); R.g.beginPath(); R.g.rect(-600, 626, 3200, 900); R.g.clip(); R.g.translate(0, 620 * 2); R.g.scale(1, -1); R.g.globalAlpha = .55;
    FIG.kisi(R, 1000 - u * 140, 900, 560, { tip: 'yaratik', f: -1, bacak: 'cok', govde: egil, bas: .3, goz: 1, renk: '#1E2A2E' });
    R.g.restore();
    for (let i = 0; i < 8; i++) R.kazi([[600 + i * 90, 660 + i * 30], [700 + i * 90 + Math.sin(st.lt * 2 + i) * 10, 660 + i * 30]], 3, 'rgba(230,240,240,.4)');
    R.kara(g => g.rect(-600, 600, 3200, 26));
    FIG.kisi(R, 1000 - u * 140, 610, 560, { tip: 'yaratik', f: -1, bacak: 'cok', govde: egil, bas: .3, goz: 1, kolO: [lerp(.9, 1.8, u), .6] });
  }, { fener: { isik: { x: 960, y: 560, r: 600, sic: [.95, .97, .95] }, kadraj: { tip: 'oval', x: 960, y: 560, w: 1400, h: 920, yum: 40 } } });
  // D12: odunlukta mum ışığında Victor'un günlüğü (ayrıntı)
  sahne('D12a', 'D12', 'odunluk', 'ayrinti', (R, st) => {
    R.cam(960, 640, 1.15 + st.lt * .03);
    R.gok(-600, -400, 2600, 1500, [[0, '#5A4636'], [1, '#3E3026']], { firca: 1.4 });
    const dus = E.in3(clamp((st.lt - rel(st, 'D12@tiksinip')) / 1.2)); R.g.save(); R.g.translate(960, 710); R.g.rotate(dus * .5); R.g.translate(-960, -710 + dus * 520);
    R.isikli(g => { g.moveTo(560, 600); g.lineTo(1300, 560); g.lineTo(1360, 820); g.lineTo(600, 860); g.closePath(); }, '#E8DCBC');
    SET.elYazisi(R, '…the lifeless thing that lay at my feet. Its yellow eye…', 640, 660, 40, 1, { maxW: 620, renk: '#3A2A1C' });
    FIG.elYakin(R, 1330, 760, 9, -1, true, .4); R.g.restore();
    DK.mum(R, 420, 860, 160, { t: st.t });
  }, { fener: { isik: { x: 900, y: 640, r: 560, sic: [1, .86, .62] }, kadraj: { tip: 'oval', x: 960, y: 600, w: 1400, h: 860, yum: 40 }, parlak: .95 } });
  // D13: umut: yarıktan yalnız ihtiyar, ışık onda
  sahne('D13a', 'D13', 'yarik', 'orta', (R, st) => {
    R.cam(680 + st.lt * 6, 780, 1.75 + st.lt * .04);
    KULUBE_IC(R, st, { duvar1: '#E6C890', duvar2: '#C4A468' });
    FIG.kisi(R, 700, 980, 440, { tip: 'ihtiyar', f: 1, bacak: 'otur', bas: -.1 + Math.sin(st.lt * 1.2) * .06, kolO: [.9 + Math.sin(st.lt * 5) * .08, 1.0], kolA: [.7, 1.2] });
  }, { fener: { isik: { x: 760, y: 520, r: 460, sic: [1, .9, .7] }, kadraj: YARIK } });
})();
