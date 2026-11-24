// G: VI. Buzların arasında (G01–G05): kapak A'nın halkası (uzanan el); son sahnede fener kapanır. Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  const KARE = { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 };
  sahne('G00k', 'G01-1.4', 'kart', 'kart', (R, st) => { R.cam(960, 540, 1); SET.kart(R, st, 'VI', 'BUZLARIN ARASINDA', 'Son kez uzanan el'); },
    { fener: { isik: { x: 960, y: 480, r: 900 }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1500, h: 860, yum: 30 } }, tr: { type: 'iris', dur: 1.2 } });
  window.BUZ_DENIZ = (R, st) => {
    R.gok(-800, -400, 3600, 640, [[0, '#2C3A5E'], [1, '#7C8EB0']], { firca: 1.2 });
    R.yika(g => g.rect(-800, 620, 4400, 900), '#3C5274', { firca: 1 });
    for (let i = 0; i < 7; i++) { const x = -600 + i * 520, w = 260 + (i % 3) * 120, y = 640 + (i % 2) * 120;
      R.isikli(g => { g.moveTo(x, y); g.lineTo(x + w * .3, y - 50); g.lineTo(x + w * .7, y - 36); g.lineTo(x + w, y); g.lineTo(x + w * .9, y + 30); g.lineTo(x + w * .1, y + 30); g.closePath(); }, '#D8E2F0'); }
  };
  // G01: buz denizinde sıkışmış gemi; uzakta kızak ve kovalayan
  sahne('G01a', 'G01+2.2', 'buz', 'genis', (R, st) => {
    R.cam(900 + st.lt * 12, 640, 1.6);
    BUZ_DENIZ(R, st);
    R.kara(g => { g.moveTo(1100, 720); g.lineTo(1700, 720); g.lineTo(1640, 800); g.lineTo(1160, 800); g.closePath(); g.rect(1380, 340, 14, 380); g.rect(1240, 420, 10, 300); });
    R.yika(g => { g.moveTo(1394, 360); g.lineTo(1560, 420); g.lineTo(1394, 560); g.closePath(); }, '#C8C4B4', {});
    const x = 500 + st.lt * 50;
    R.kara(g => { g.rect(x, 700, 110, 12); g.rect(x + 100, 680, 10, 30); });
    FIG.kisi(R, x - 40, 712, 150, { tip: 'victor', f: 1, govde: .3, kolO: [1.2, .3] });
  }, { fener: { isik: { x: 960, y: 520, r: 820, sic: [.95, .96, 1] }, kadraj: KARE } });
  // G02: kamara: tabut, üstüne eğilmiş karaltı, uzun dağınık saç; "bir eli uzanmıştı" (kapak A'nın halkası)
  window.KAMARA = (R, st) => {
    R.gok(-600, -400, 2600, 1500, [[0, '#5A5A6E'], [1, '#3E3E50']], { firca: 1.3 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#3A3030', { firca: 1 });
    R.isikli(g => g.ellipse(1480, 330, 80, 80, 0, 0, TAU), '#C8D4EA');   // lomboz (ay ışığı; başın yanında değil: hale okunmasın)
    R.kara(g => { g.rect(500, 680, 900, 140); g.rect(520, 820, 30, 80); g.rect(1350, 820, 30, 80); });   // tabut (düz kapak, haç yok)
    FIG.yatan(R, 960, 680, 760, { f: 1, profil: false });
    R.yika(g => { g.moveTo(640, 676); g.quadraticCurveTo(900, 610, 1380, 650); g.lineTo(1390, 690); g.lineTo(630, 690); g.closePath(); }, '#D0CEDA', { firca: .8 });   // örtü (boyna kadar)
  };
  sahne('G02a', 'G02', 'kamara', 'orta', (R, st) => {
    const tE = rel(st, 'G02@uzanmıştı');
    R.cam(820, 560, 1.0 + st.lt * .012);
    KAMARA(R, st);
    const u = E.io3(clamp((st.lt - tE + .4) / 1.4));
    FIG.kisi(R, 380, 1000, 700, { tip: 'yaratik', f: 1, bacak: 'diz', govde: .4, bas: .5, kolO: [lerp(.4, 1.2, u), lerp(.3, .35, u)], goz: 0, sac: -.4 });
    R.isikli(g => g.rect(1760, 200, 120, 700), 'rgba(240,210,150,.9)');   // kapıdan giren kaptanın feneri
  }, { fener: { isik: { x: 860, y: 540, r: 640, sic: [.95, .94, .96] }, kadraj: KARE } });
  // G03: halka: ilk gece (A01) ↔ şimdi; aynı el, aynı yön
  sahne('G03a', 'G03', 'oda', 'yakin', (R, st) => {
    R.cam(1200, 520, 1.02);
    ODA_GECE(R, st);
    FIG.yatan(R, 1600, 662, 560, { f: 1 });
    FIG.kisi(R, 1060, 1000, 700, { tip: 'yaratik', f: 1, govde: .1, bas: .08, kolO: [1.15, .55], goz: 1 });
  }, { fener: { isik: { x: 1100, y: 420, r: 560, sic: [1, .92, .78] }, kadraj: { tip: 'daire', x: 1010, y: 520, r: 520, yum: 30 }, parlak: .8 } });
  sahne('G03b', 'G03@şimdi', 'kamara', 'orta', (R, st) => {
    R.cam(620, 640, 1.35);
    KAMARA(R, st);
    FIG.kisi(R, 380, 1000, 700, { tip: 'yaratik', f: 1, bacak: 'diz', govde: .15, bas: .45, kolO: [.95, .4], goz: 0, sac: .3 });
  }, { fener: { isik: { x: 900, y: 560, r: 480, sic: [.95, .94, .96] }, kadraj: { tip: 'daire', x: 960, y: 520, r: 460, yum: 40 }, parlak: 1.2 } });
  // G04: yaratığın yüzü saçların ardında (yakın); "soğumuş"
  sahne('G04a', 'G04', 'kamara', 'yakin', (R, st) => {
    R.cam(520 + st.lt * 10, 560, 1.55 + st.lt * .04);
    KAMARA(R, st);
    FIG.kisi(R, 300, 1000, 700, { tip: 'yaratik', f: 1, bacak: 'diz', govde: .05 + .1 * E.io3(clamp((st.lt - rel(st, 'G04@soğumuş')) / 1.2)), bas: .35 + .3 * E.io3(clamp((st.lt - rel(st, 'G04@soğumuş')) / 1.2)), kolO: [lerp(1.3, .5, E.io3(clamp((st.lt - rel(st, 'G04@soğumuş')) / 1.2))), 1.0], goz: 1, sac: .5, kenar: 'rgba(220,228,250,.7)' });
  }, { fener: { isik: { x: 1100, y: 480, r: 520, sic: [.95, .94, .96] }, kadraj: { tip: 'oval', x: 1000, y: 500, w: 1300, h: 900, yum: 40 } } });
  // G05: buz salı karanlıkta uzaklaşır; fener iris gibi kapanır
  sahne('G05a', 'G05', 'buz', 'genis', (R, st) => {
    const tD = rel(st, 'G05@dalgalar');
    R.cam(960, 560, 1.0);
    BUZ_DENIZ(R, st);
    const u = E.io2(clamp((st.lt - tD) / 6));
    const x = lerp(820, 1500, u), y = lerp(780, 650, u), s = lerp(1, .25, u);
    R.isikli(g => { g.moveTo(x - 160 * s, y); g.lineTo(x + 170 * s, y - 8 * s); g.lineTo(x + 150 * s, y + 20 * s); g.lineTo(x - 140 * s, y + 22 * s); g.closePath(); }, '#D8E2F0');
    FIG.kisi(R, x, y, 420 * s, { tip: 'yaratik', f: 1, govde: .05, pel: Math.sin(st.lt) * .5, sac: .6 });
    R.kara(g => { g.moveTo(-600, 1000); g.lineTo(700, 980); g.lineTo(700, 1500); g.lineTo(-600, 1500); g.closePath(); g.rect(380, 520, 14, 480); });   // geminin kıçı (önde)
  }, { fener: st => { const tD = A('G05@dalgalar') - st.at, k = E.io3(clamp((st.lt - tD - 1.5) / 4.5));
    return { isik: { x: lerp(960, 1450, k), y: lerp(520, 640, k), r: lerp(820, 200, k), sic: [.95, .96, 1] }, kadraj: { tip: 'daire', x: lerp(960, 1460, k), y: lerp(540, 650, k), r: lerp(900, 0, k), yum: 40 } }; } });
})();
