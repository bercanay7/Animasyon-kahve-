// C: II. Kasım gecesi (C01–C09): romanda Victor; yaratık ışığın kenarında; sonunda ışık yaratığa geçer. Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  const KARE = { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 };
  sahne('C00k', 'C01-1.4', 'kart', 'kart', (R, st) => { R.cam(960, 540, 1); SET.kart(R, st, 'II', 'KASIM GECESİ', 'Kaçan adam ne gördü?'); },
    { fener: { isik: { x: 960, y: 480, r: 900 }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1500, h: 860, yum: 30 } }, tr: { type: 'iris', dur: 1.2 } });
  // çatı katı laboratuvarı: masa, örtülü beden, kavanozlar, mum, yağmurlu pencere
  window.LAB = (R, st, o = {}) => {
    R.gok(-600, -400, 2600, 1500, [[0, '#6E6A60'], [1, '#4E4A44']], { firca: 1.3 });
    R.kara(g => { g.moveTo(-600, 200); g.lineTo(700, -300); g.lineTo(760, -300); g.lineTo(-600, 260); g.closePath(); });     // çatı kirişi
    DK.pencere(R, 1560, 300, 260, 360, { gece: '#56688E' });
    R.yika(g => g.rect(-600, 900, 3200, 600), '#4A3C30', { firca: 1 });
    R.kara(g => { g.rect(500, 700, 900, 28); g.rect(530, 720, 24, 260); g.rect(1350, 720, 24, 260); });
    if (o.ortu !== false) R.yika(g => { g.moveTo(520, 700); g.quadraticCurveTo(700, 640, 900, 660); g.quadraticCurveTo(1100, 645, 1390, 672); g.lineTo(1400, 704); g.lineTo(510, 704); g.closePath(); }, '#CFC6B0', { firca: .8 });
    // raf ve kavanozlar (yuvarlak değil: uzun dar şişeler)
    R.kara(g => g.rect(80, 380, 360, 14));
    for (let i = 0; i < 5; i++) { const x = 110 + i * 66, h = 70 + (i % 3) * 24; R.kara(g => { g.rect(x, 380 - h, 34, h); g.rect(x + 10, 380 - h - 16, 14, 18); }); R.yika(g => g.rect(x + 6, 380 - h + 10, 22, h - 14), ['#7FA08A', '#B9A26A', '#8E8AB0'][i % 3], { kay: 0, firca: 0 }); }
    DK.yagmur(R, st.t, { a: .07, n: 30 });
  };
  sahne('C01a', 'C01+2.2', 'lab', 'orta', (R, st) => {
    R.cam(900 + st.lt * 10, 560, 1.0);
    LAB(R, st);
    FIG.kisi(R, 420, 980, 480, { tip: 'victor', f: 1, govde: .32, bas: .25, kolO: [1.3 + Math.sin(st.lt * 4) * .05, .7], kolA: [1.0, .9] });
    DK.mum(R, 1240, 700, 140, { t: st.t });
  }, { fener: { isik: { x: 760, y: 520, r: 600, sic: [1, .86, .64] }, kadraj: KARE },
    over: (ctx, st) => { etiket(ctx, 'VICTOR FRANKENSTEIN', 560, 200, st.lt - .2, st.d - .3); } });
  // C02: yüz seçimi: masada çizilmiş profiller, biri öne çekilir (ayrıntı)
  sahne('C02a', 'C02', 'lab', 'ayrinti', (R, st) => {
    R.cam(960, 560, 1.0 + st.lt * .03);
    R.gok(-600, -400, 2600, 1500, [[0, '#6A5E50'], [1, '#4E4438']], { firca: 1.3 });
    const sec = E.io3(clamp((st.lt - .5) / 1.2));
    for (let i = 0; i < 3; i++) { const x = 560 + i * 400, y = 560 - (i === 1 ? sec * 60 : 0), sc = i === 1 ? 1 + sec * .12 : 1;
      R.isikli(g => g.rect(x - 160 * sc, y - 210 * sc, 320 * sc, 420 * sc), '#EDE2C4');
      // kalemle çizilmiş profil (ince çizgi)
      R.g.save(); R.g.translate(x, y + 20); R.g.scale(sc * 14, sc * 14); R.g.strokeStyle = '#3A2A1C'; R.g.lineWidth = .16; R.g.beginPath();
      spline(R.g, [[-4.6, 4], [-5.8, -2], [-4.4, -7], [0, -8.6], [3.6, -7], [5.2, -3.6], [5.4, -1.6], [6.8, .8], [5.4, 1.4], [5.6, 2.8], [5, 3.4], [5, 5], [3, 6.4], [0, 7]], false); R.g.stroke(); R.g.restore(); }
    DK.mum(R, 1500, 860, 140, { t: st.t });
  }, { fener: { isik: { x: 960, y: 520, r: 620, sic: [1, .86, .64] }, kadraj: { tip: 'oval', x: 960, y: 540, w: 1600, h: 920, yum: 40 } } });
  // C03a: göz açılır (yatan yaratık, yakın)
  sahne('C03a', 'C03', 'lab', 'yakin', (R, st) => {
    R.cam(820, 640, 2.4 + st.lt * .03);
    LAB(R, st, { ortu: false });
    FIG.yatan(R, 960, 700, 760, { f: 1, sac: 1, goz: clamp((st.lt - .3) / .5), nefes: st.lt > .8 ? Math.sin(st.lt * 3) * 2 : 0 });
    R.yika(g => { g.moveTo(700, 690); g.quadraticCurveTo(900, 650, 1300, 672); g.lineTo(1400, 704); g.lineTo(700, 704); g.closePath(); }, '#CFC6B0', { firca: .8 });
    DK.mum(R, 560, 700, 110, { t: st.t, yan: .6 });
  }, { fener: { isik: { x: 760, y: 520, r: 420, sic: [1, .84, .6] }, kadraj: { tip: 'daire', x: 900, y: 520, r: 430, yum: 40 }, parlak: .85 } });
  // C03b: yaratık doğrulur: tarif sözcükleriyle (yakın, kenar ışığı)
  sahne('C03b', 'C03@sarı', 'lab', 'orta', (R, st) => {
    const k = E.io3(clamp(st.lt / 2.4));
    R.cam(980, 520, 1.3 + st.lt * .015);
    LAB(R, st, { ortu: false });
    FIG.kisi(R, 900, 1000, 760, { tip: 'yaratik', f: 1, bacak: 'otur', govde: lerp(.6, .1, k), bas: lerp(.4, .05, k), kolO: [.5, .6], kolA: [.2, .4], goz: 1, kenar: 'rgba(250,215,150,.8)', sac: .1 });
    R.yika(g => { g.moveTo(1000, 690); g.quadraticCurveTo(1200, 660, 1390, 680); g.lineTo(1400, 704); g.lineTo(1000, 704); g.closePath(); }, '#CFC6B0', { firca: .8 });
  }, { fener: { isik: { x: 860, y: 440, r: 520, sic: [1, .84, .6] }, kadraj: { tip: 'oval', x: 960, y: 500, w: 1300, h: 920, yum: 40 } } });
  // C04: Victor kaçar (kapı), yaratık masada kalır; ışık onu bırakır
  sahne('C04a', 'C04', 'lab', 'genis', (R, st) => {
    R.cam(900, 540, .92);
    LAB(R, st, { ortu: false });
    R.kara(g => { g.rect(-120, 220, 20, 690); g.rect(150, 220, 20, 690); g.rect(-120, 200, 290, 24); });
    const g = HAREKET.yuruyus({ tip: 'kos', uyluk: 23, baldir: 23, tur: .6 });
    const y = HAREKET.yuruyusYolu(g, { t0: 0, t1: 6, x0: 520, yon: -1, olcek: 4.3, go: t => HAREKET.rampa(t, 0, .3) })(st.lt);
    if (y.x > -60) FIG.kisi(R, y.x, 980, 430, { tip: 'victor', f: -1, bacak: y.poz, govde: .25, kolO: [.8 + Math.sin(TAU * y.faz) * .6, .9], kolA: [-.6 - Math.sin(TAU * y.faz) * .6, .9] });
    FIG.kisi(R, 1000, 1000, 640, { tip: 'yaratik', f: -1, bacak: 'otur', govde: .15, kolO: [lerp(.4, 1.0, clamp(st.lt / 1.5)), .5], goz: 1 });
  }, { fener: st => { const k = E.io3(clamp((st.lt - (A('C04@ne') - st.at)) / 1.8)); return { isik: { x: lerp(700, 300, k), y: 520, r: 600 }, kadraj: { ...KARE }, parlak: 1 - k * .3 }; } });
  // C05: sıfatlar camın üstüne kazınır, yaratığın çevresine
  sahne('C05a', 'C05', 'karanlik', 'orta', (R, st) => {
    R.cam(960, 540, 1.0 + st.lt * .01);
    R.gok(-600, -400, 2600, 1500, [[0, '#3E3C52'], [1, '#2A2838']], { firca: 1.4 });
    FIG.kisi(R, 960, 1010, 720, { tip: 'yaratik', f: 1, govde: .12, bas: .2, kolO: [.1, .4], goz: 1 });
    const w = [['SEFİL', 'sefil', 500, 300], ['ALÇAK', 'alçak', 1420, 380], ['CANAVAR', 'canavar', 1360, 760]];
    for (const [s, k, x, y] of w) SET.camYazi(R, s, x, y, { px: 84, ls: 8, p: clamp((st.lt - rel(st, 'C05@' + k)) / .5), renk: '#E9C79A' });
  }, { fener: { isik: { x: 960, y: 500, r: 760, sic: [.95, .9, .86] }, kadraj: KARE, parlak: .95 } });
  // C06: buzul (Mer de Glace): Victor küçük; yaratık buzun üstünde hızla gelir
  window.BUZUL = (R, st, o = {}) => {
    R.gok(-800, -600, 3600, 700, [[0, '#8FA2C2'], [1, '#D6DCE4']], { firca: 1.2 });
    DK.daglar(R, -800, 3600, 520, [[-500, 200], [0, 120], [520, -40], [900, 180], [1400, 60], [2000, 160], [2600, 90]], '#56688E', { kar: '#F4F6FA' });
    R.yika(g => { g.moveTo(-800, 600); g.lineTo(3600, 560); g.lineTo(3600, 1500); g.lineTo(-800, 1500); g.closePath(); }, '#C9D6E6', { firca: 1 });
    for (let i = 0; i < 14; i++) { const y = 620 + i * 40, r = rng(i + 3); R.cizgi([[-800 + r() * 400, y], [600 + r() * 600, y + 14], [1800 + r() * 600, y - 10], [3600, y + 6]], 3 + i * .3, { egri: true, renk: '#6C7E9C', a: .8 }); }
  };
  sahne('C06a', 'C06', 'buzul', 'genis', (R, st) => {
    R.cam(1000 + st.lt * 14, 560, 1.0);
    BUZUL(R, st);
    FIG.kisi(R, 760, 900, 220, { tip: 'victor', f: 1, bas: -.1 });
    const g = HAREKET.yuruyus({ tip: 'kos', uyluk: 23, baldir: 23, tur: .7 });
    const y = HAREKET.yuruyusYolu(g, { t0: 0, t1: 8, x0: 1900, yon: -1, olcek: 2.6, go: t => 1 - HAREKET.rampa(t, 3.4, 4.2) })(st.lt);
    FIG.kisi(R, y.x, 940, 300, { tip: 'yaratik', f: -1, bacak: y.poz, govde: .15 * y.go, pel: Math.sin(st.lt * 4), kolO: [.4 + Math.sin(TAU * y.faz) * .5 * y.go, .5], kolA: [-.4 - Math.sin(TAU * y.faz) * .5 * y.go, .5] });
  }, { fener: { isik: { x: 1000, y: 460, r: 900, sic: [.96, .96, 1] }, kadraj: KARE },
    over: (ctx, st) => { etiket(ctx, 'MER DE GLACE · MONT BLANC', 960, 150, st.lt - .3, st.d - .3); } });
  // C07: yaratık konuşur (yakın): iddiası
  sahne('C07a', 'C07', 'buzul', 'yakin', (R, st) => {
    R.cam(1100, 560, 1.55 + st.lt * .02);
    BUZUL(R, st);
    FIG.kisi(R, 1080, 1000, 760, { tip: 'yaratik', f: -1, govde: .05, bas: .05, kolO: [.9 + Math.sin(st.lt * 1.5) * .1, 1.3], goz: 1, kenar: 'rgba(255,240,220,.8)', sac: Math.sin(st.lt) * .4 });
  }, { fener: { isik: { x: 980, y: 420, r: 520, sic: [.96, .96, 1] }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1300, h: 900, yum: 40 } } });
  // C08: "beni dinle": iki figür; yaratık kulübeyi gösterir (orta)
  sahne('C08a', 'C08', 'buzul', 'orta', (R, st) => {
    R.cam(1000, 600, 1.35);
    BUZUL(R, st);
    R.kara(g => { g.moveTo(1500, 900); g.lineTo(1500, 760); g.lineTo(1620, 680); g.lineTo(1740, 760); g.lineTo(1740, 900); g.closePath(); });
    R.isikli(g => g.rect(1580, 800, 60, 80), '#F2C27A');
    FIG.kisi(R, 760, 1000, 430, { tip: 'victor', f: 1, bas: -.1, kolO: [.2, .4] });
    const k = E.io3(clamp((st.lt - 1) / 1));
    FIG.kisi(R, 1180, 1000, 600, { tip: 'yaratik', f: -1, govde: .06, kolO: [lerp(.3, -.0, k), .4], kolA: [lerp(.1, 1.1, k), lerp(.4, .2, k)], goz: 1 });
  }, { fener: { isik: { x: 1000, y: 520, r: 700, sic: [.96, .96, 1] }, kadraj: KARE } });
  // C09: kulübede ateş; ışık dairesi Victor'dan yaratığa kayar ("bundan sonrası onun kendi ağzından")
  sahne('C09a', 'C09', 'kulube', 'orta', (R, st) => {
    R.cam(960, 560, 1.05);
    R.gok(-600, -400, 2600, 1500, [[0, '#7A5A40'], [1, '#54402E']], { firca: 1.3 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#3E2E22', { firca: 1 });
    DK.ates(R, 960, 880, 200, { t: st.t });
    FIG.kisi(R, 560, 990, 450, { tip: 'victor', f: 1, bacak: 'otur', govde: .1, kolO: [.9, 1.2] });
    FIG.kisi(R, 1360, 990, 620, { tip: 'yaratik', f: -1, bacak: 'otur', govde: .12, kolO: [.9, 1.0], goz: 1 });
  }, { fener: st => { const k = E.io3(clamp((st.lt - (A('C09@bundan') - st.at)) / 2)); return { isik: { x: lerp(620, 1340, k), y: 560, r: 520 }, kadraj: { tip: 'daire', x: lerp(640, 1300, k), y: 560, r: 470, yum: 40 } }; } });
})();
