// A: kanca (A01–A05). Sahibi: başkan.
// Kapak A (uzanan el) ve kapak B (18 yaşında yazan kız) ilk 5 sn'de. Işık kuralı: yaratık Victor'un sahnesinde ışığın kenarında.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  // Victor'un yatak odası, gece: kepenk aralığından ay ışığı, perdeli yatak (sağda), kapı (solda)
  window.ODA_GECE = (R, st, o = {}) => {
    R.gok(-400, -300, 2400, 1400, [[0, '#4F6699'], [.6, '#6378A6'], [1, '#4A5272']], { firca: 1 });
    R.yika(g => g.rect(-400, 900, 2800, 600), '#7A5E48', { firca: .8 });
    DK.pencere(R, 560, 300, 260, 360, { gece: '#9DB2DA', kepenk: .55, ay: o.ay ?? true });
    R.yika(g => { g.moveTo(530, 480); g.lineTo(590, 480); g.lineTo(820, 1100); g.lineTo(560, 1100); g.closePath(); }, 'rgba(225,232,250,.65)', { kay: 0, firca: 0 });
    // kapı (en solda)
    R.kara(g => { g.rect(40, 200, 22, 700); g.rect(300, 200, 22, 700); g.rect(40, 180, 282, 24); });
    if (o.kapiAcik != null) R.yika(g => g.rect(62, 204, 238 * o.kapiAcik, 696), '#2A2230', { kay: 0 });
    // yatak (sağ): karyola direkleri, çarşaf
    R.kara(g => { g.rect(1260, 40, 26, 980); g.rect(1880, 40, 26, 980); g.rect(1240, 20, 700, 40); });
    R.kara(g => { g.rect(1270, 700, 640, 140); g.rect(1270, 830, 30, 190); g.rect(1880, 830, 30, 190); });
    R.yika(g => g.rect(1290, 640, 600, 70), '#B9B2A6', { firca: .6 });
  };
  // A01p: ilk saniye: mum ışığında yazan el, kâğıtta İngilizce ilk cümle (kapak B'nin vaadi)
  sahne('A01p', 'A01', 'masa', 'ayrinti', (R, st) => {
    R.cam(980 + st.lt * 10, 560, 1.5 + st.lt * .03);
    R.gok(-400, -300, 2400, 1400, [[0, '#7A5638'], [1, '#5A3E2A']], { firca: 1.2 });
    R.isikli(g => { g.moveTo(560, 560); g.lineTo(1420, 520); g.lineTo(1500, 760); g.lineTo(620, 820); g.closePath(); }, '#EFE3C4');
    SET.elYazisi(R, 'It was on a dreary night of November', 700, 640, 58, clamp(st.lt / 2.6), { maxW: 900 });
    // yalnız tüy kalem (el çizilmez: el + kalem siluet uzaktan tabanca gibi okunuyordu)
    const k = Math.min(2.6, st.lt), hx = 700 + 560 * clamp(k / 2.6) + Math.sin(st.lt * 18) * 5, hy = 642 + Math.sin(st.lt * 11) * 4;
    R.cizgi([[hx, hy], [hx + 110, hy - 260]], 4);
    R.kara(g => { g.moveTo(hx + 60, hy - 140); g.bezierCurveTo(hx + 30, hy - 260, hx + 120, hy - 380, hx + 190, hy - 430); g.bezierCurveTo(hx + 170, hy - 330, hx + 150, hy - 220, hx + 84, hy - 136); g.closePath(); });
    for (let i = 0; i < 9; i++) { const u = i / 9; R.cizgi([[hx + 70 + u * 100, hy - 160 - u * 250], [hx + 30 + u * 110, hy - 190 - u * 250]], 2.2); }
    DK.mum(R, 1380, 470, 170, { t: st.t });
  }, { fener: { isik: { x: 900, y: 520, r: 620, sic: [1, .86, .62] }, kadraj: { tip: 'oval', x: 960, y: 520, w: 1400, h: 900, yum: 40 } } });
  // A01a: yatağın başı; perde aralanır, el uzanır (kapak A)
  sahne('A01a', 'A01@yaratık', 'oda', 'yakin', (R, st) => {
    const tU = rel(st, 'A01@uzatıyor'), tP = rel(st, 'A01@perdeyi');
    R.cam(1200, 520, 1.02 + st.lt * .01);
    ODA_GECE(R, st);
    FIG.yatan(R, 1600, 662, 560, { f: 1, nefes: Math.sin(st.lt * 1.6) * 1.2 });
    const pa = E.io3(clamp((st.lt - tP + .3) / 1.2));
    DK.perde(R, 1286 + pa * 230, 1520, 60, 700, '#B0433A', { t: st.lt * .3, kivrim: 6 });
    const ue = E.io3(clamp((st.lt - tU + .2) / 1.4));
    FIG.kisi(R, 1060, 1000, 700, { tip: 'yaratik', f: 1, govde: .1, bas: .08,
      kolA: [lerp(.9, 1.55, pa), lerp(.5, .1, pa)], kolO: [lerp(.2, 1.15, ue), lerp(.25, .55, ue)], sac: .2, goz: 1 });
  }, { fener: { isik: { x: 1100, y: 420, r: 560, sic: [1, .92, .78] }, kadraj: { tip: 'daire', x: 1010, y: 520, r: 520, yum: 30 } } });
  // A02: Victor yataktan fırlar, kapıya koşar; yaratık ışığın kenarında kalır
  sahne('A02a', 'A02', 'oda', 'genis', (R, st) => {
    R.cam(900 - st.lt * 20, 540, .9);
    ODA_GECE(R, st, { kapiAcik: clamp(st.lt / .6) });
    const g = HAREKET.yuruyus({ tip: 'kos', uyluk: 23, baldir: 23, tur: .6 });
    const yol = HAREKET.yuruyusYolu(g, { t0: 0, t1: 8, x0: 1300, yon: -1, olcek: 4.4, go: t => HAREKET.rampa(t, .15, .5) });
    const y = yol(st.lt);
    FIG.kisi(R, 1880, 1000, 700, { tip: 'yaratik', f: -1, govde: .06, kolO: [1.0, .5], goz: 1 });
    if (y.x > 150) FIG.kisi(R, y.x, 1000, 430, { tip: 'victor', f: -1, bacak: y.poz, govde: .25, kolO: [.8 + Math.sin(TAU * y.faz) * .6, .9], kolA: [-.6 - Math.sin(TAU * y.faz) * .6, .9] });
  }, { fener: { isik: { x: 760, y: 520, r: 700 }, kadraj: { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 } } });
  // A03: adsız: yaratık yalnız, yatağın yanında; "Frankenstein"de ad slayta büyük harfle yazılır, ama ona değil: boş kapıya
  sahne('A03a', 'A03', 'oda', 'orta', (R, st) => {
    const tF = rel(st, 'A03@frankenştayn'), tK = rel(st, 'A03@kaçan');
    R.cam(980 - st.lt * 6, 540, 1.0 + st.lt * .006);
    ODA_GECE(R, st, { kapiAcik: 1 });
    const don = E.io3(clamp((st.lt - tK) / 1.2));
    FIG.kisi(R, 1150, 1000, 700, { tip: 'yaratik', f: lerp(1, -1, don) > 0 ? 1 : -1, govde: .08, bas: .1, kolO: [.15, .3], goz: 1 });
    SET.camYazi(R, 'FRANKENSTEIN', 900, 150, { px: 120, ls: 14, p: clamp((st.lt - tF) / .9) });
  }, { fener: st => ({ isik: { x: 820, y: 460, r: 620 }, kadraj: { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 } }),
    over: (ctx, st) => { etiket(ctx, 'YARATIĞIN ADI YOK', 1420, 180, st.lt - .6, rel(st, 'A03@iki') - .2); } });
  // A04: Mary Shelley (on sekiz yaşında), mum ışığında; soru
  sahne('A04a', 'A04', 'masa', 'genis', (R, st) => {
    R.cam(900, 560, 1.0 + st.lt * .01);
    SET.masa(R, st, {});
    DK.yagmur(R, st.t, { a: .1, n: 40 });
    const yaz = Math.sin(st.lt * 6) * .04;
    FIG.kisi(R, 560, 960, 500, { tip: 'mary', f: 1, bacak: 'otur', govde: .25, bas: .3, kolO: [1.3 + yaz, 1.0], kolA: [1.0, 1.2] });
    DK.sandalye(R, 470, 700, .9);
    R.isikli(g => g.rect(720, 626, 170, 12), '#F1E6C9');
    DK.mum(R, 1080, 640, 150, { t: st.t });
  }, { fener: { isik: { x: 820, y: 560, r: 620, sic: [1, .88, .66] }, kadraj: { tip: 'oval', x: 900, y: 540, w: 1500, h: 960, yum: 40 } },
    over: (ctx, st) => { etiket(ctx, 'MARY SHELLEY', 600, 170, st.lt - .3, st.d - .3); } });
  // A05: yaratık konuşacak: ışık kenardan merkezine kayar; "terk edilince"de geri çekilir
  sahne('A05a', 'A05', 'karanlik', 'yakin', (R, st) => {
    const tC = rel(st, 'A05@canavar'), tT = rel(st, 'A05@terk');
    R.cam(960, 520, 1.25 + st.lt * .01);
    R.gok(-400, -300, 2400, 1400, [[0, '#3A4466'], [1, '#2A2E44']], { firca: 1.4 });
    FIG.kisi(R, 900, 1100, 780, { tip: 'yaratik', f: 1, govde: .12, bas: .18, kolO: [.3, .9], goz: 1, kenar: 'rgba(240,200,140,.8)' });
  }, { fener: st => { const tC = A('A05@canavar') - st.at, tT = A('A05@terk') - st.at;
    const m = E.io3(clamp(st.lt / 2.5)) * (1 - E.io3(clamp((st.lt - tT) / 1.4)) * .7);
    return { isik: { x: lerp(1500, 980, m), y: 470, r: 520 }, kadraj: { tip: 'daire', x: lerp(1450, 1000, m), y: 500, r: lerp(380, 470, m), yum: 30 }, parlak: .9 }; },
    over: (ctx, st) => { const tC = rel(st, 'A05@canavar'); if (st.lt > tC - .2) txt(ctx, 'CANAVAR DOĞULUR MU, OLUNUR MU?', 960, 140, { font: FONT.buyuk(96), px: 96, ls: 3, a: E.out3(clamp((st.lt - tC + .2) / .4)), panel: .6 }); } });
})();
