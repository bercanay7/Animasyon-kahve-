// B: I. Yazsız yıl (B01–B16): 1816 çerçevesi, kahramanı Mary. Renk: gece mavisi ve mum sarısı. Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  const KARE = { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 };
  // Cenevre Gölü, 1816 Haziran gecesi
  window.GOL_GECE = (R, st, o = {}) => {
    const fl = o.simsek || 0;
    R.gok(-600, -400, 2600, 640, [[0, '#3C4C78'], [.55, '#6A7FAE'], [1, '#9AA6C4']], { firca: 1.2 });
    if (fl > 0) R.gok(-600, -400, 2600, 640, [[0, `rgba(255,255,255,${fl})`], [1, `rgba(255,255,255,${fl * .6})`]], { firca: 0, kay: 0 });
    for (let i = 0; i < 6; i++) { const cx = -300 + i * 480 + Math.sin(st.t * .05 + i) * 40, cy = 60 + (i % 2) * 70;
      R.yika(g => { g.ellipse(cx, cy, 380, 90, 0, 0, TAU); g.ellipse(cx + 200, cy + 40, 300, 80, 0, 0, TAU); }, 'rgba(70,78,110,.75)', { kay: 0 }); }
    DK.daglar(R, -600, 2600, 560, [[-300, 420], [200, 360], [700, 400], [1200, 330], [1700, 390], [2200, 350]], '#2E3654', {});
    DK.gol(R, -600, 2600, 560, 1300, '#5D6F9E', '#2E3A5E', { t: st.t, yx: 1180, yw: 500, n: 30, yansima: 'rgba(255,226,160,.6)' });
    R.kara(g => { g.moveTo(700, 900); g.quadraticCurveTo(1100, 760, 1500, 740); g.lineTo(2600, 720); g.lineTo(2600, 1400); g.lineTo(700, 1400); g.closePath(); });
    DK.villa(R, 1560, 760, 520, {});
    for (const [x, h] of [[1180, 260], [1960, 320], [2100, 280]]) DK.cam(R, x, 770, h, { sal: Math.sin(st.t * .7) });
  };
  sahne('B01a', 'B01', 'gol', 'genis', (R, st) => {
    R.cam(980 + st.lt * 9, 540, 1);
    GOL_GECE(R, st, {});
    DK.yagmur(R, st.t, { a: .28 });
  }, { fener: { isik: { x: 960, y: 480, r: 900, sic: [1, .93, .8] }, kadraj: KARE },
    over: (ctx, st) => { etiket(ctx, 'CENEVRE GÖLÜ · HAZİRAN 1816', 960, 150, st.lt - .3, st.d - .2); } });
  // B02: Mary'nin mektubu: yazılan satırlar; "şimşek"te pencere ağarır, "zifiri karanlık"ta ışık söner
  sahne('B02a', 'B02', 'mektup', 'ayrinti', (R, st) => {
    const tS = rel(st, 'B02@şimşek'), tZ = rel(st, 'B02@zifiri');
    R.cam(960 - st.lt * 8, 540, 1.1);
    R.gok(-400, -300, 2400, 1400, [[0, '#7A5638'], [1, '#5A3E2A']], { firca: 1.2 });
    DK.pencere(R, 1500, 300, 420, 560, { gece: '#5A6E9C' });
    const fl = DK.simsek(R, 1500, 60, 520, (st.lt - tS) / 1.6, {});
    if (fl > 0) R.yika(g => g.rect(1290, 20, 420, 560), `rgba(255,255,255,${fl * .9})`, { kay: 0, firca: 0 });
    R.isikli(g => { g.moveTo(260, 520); g.lineTo(1080, 470); g.lineTo(1140, 860); g.lineTo(300, 900); g.closePath(); }, '#EFE3C4');
    SET.elYazisi(R, 'An almost perpetual rain confines us principally to the house…', 380, 600, 46, clamp(st.lt / 5), { maxW: 700 });
  }, { fener: st => { const tZ = A('B02@zifiri') - st.at, k = clamp((st.lt - tZ) / .5); return { isik: { x: 800, y: 560, r: 640, sic: [1, .88, .66] }, kadraj: { tip: 'oval', x: 900, y: 540, w: 1600, h: 980, yum: 40 }, parlak: 1 - k * .82 }; },
    over: (ctx, st) => { kunye(ctx, 'Mary Shelley, mektup, 1 Haziran 1816', st.lt - 1, st.d - .3); } });
  // B03: Mary pencerede (18), arkasında Percy; ışık Mary'de
  sahne('B03a', 'B03', 'salon', 'orta', (R, st) => {
    R.cam(1150, 560, 1.0 + st.lt * .012);
    SET.salon(R, st);
    DK.yagmur(R, st.t, { a: .14, n: 40, kutu: [1315, 125, 330, 470] });
    FIG.kisi(R, 1320, 960, 470, { tip: 'mary', f: 1, bas: -.08, kolO: [.9, 1.0], kolA: [0, 0] });
    FIG.kisi(R, 1060, 960, 500, { tip: 'percy', f: 1, govde: .04, kolO: [.2, .4], kolA: [-.1, .3] });
  }, { fener: { isik: { x: 1220, y: 500, r: 560, sic: [1, .9, .72] }, kadraj: { tip: 'oval', x: 1080, y: 520, w: 1500, h: 960, yum: 40 } },
    over: (ctx, st) => { etiket(ctx, 'MARY · 18', 1420, 230, st.lt - .3, st.d - .3); etiket(ctx, 'PERCY SHELLEY', 820, 300, rel(st, 'B03@pörsi'), st.d - .3); } });
  // B04: annesinin siluet portresi (oval); ayrıntı
  sahne('B04a', 'B04', 'portre', 'ayrinti', (R, st) => {
    R.cam(960, 500 - st.lt * 6, 1.0 + st.lt * .02);
    R.gok(-400, -300, 2400, 1400, [[0, '#8E6C4C'], [1, '#6C4C34']], { firca: 1.2 });
    DK.portre(R, 960, 470, 2.4, { tip: 'mary', f: 1 });
  }, { fener: { isik: { x: 960, y: 470, r: 520, sic: [1, .9, .74] }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1000, h: 920, yum: 40 } },
    over: (ctx, st) => { etiket(ctx, 'MARY WOLLSTONECRAFT · 1759–1797', 960, 870 - 40, st.lt - .4, st.d - .3, { px: 42 }); } });
  // B05: boş beşik (kız), sonra kucakta beş aylık oğul
  sahne('B05a', 'B05', 'besik', 'orta', (R, st) => {
    R.cam(960, 560, 1.05 + st.lt * .015);
    R.gok(-400, -300, 2400, 1400, [[0, '#56607E'], [1, '#3C4258']], { firca: 1.2 });
    R.yika(g => g.rect(-400, 820, 2800, 600), '#4A3E3A', { firca: 1 });
    DK.besik(R, 960, 820, 2.2, { a: Math.sin(st.lt * 1.2) * .02, ortu: '#D8CDB6' });
  }, { fener: { isik: { x: 960, y: 560, r: 480, sic: [.92, .92, 1] }, kadraj: { tip: 'daire', x: 960, y: 560, r: 470, yum: 30 }, parlak: .85 } });
  sahne('B05b', 'B05@şimdi', 'salon', 'yakin', (R, st) => {
    R.cam(1250, 520, 1.5 + st.lt * .02);
    SET.salon(R, st);
    FIG.kisi(R, 1200, 960, 480, { tip: 'mary', f: 1, bas: .35, govde: .05, kolO: [1.0, 1.5], kolA: [.8, 1.6],
      el: { on: (R2, e) => { const g = R2.g; g.fillStyle = '#E4D6BA'; g.beginPath(); g.ellipse(e.e[0] - 2, e.e[1] - 3, 7, 4.4, -.3, 0, TAU); g.fill(); g.fillStyle = R2.KARA; g.beginPath(); g.arc(e.e[0] + 3.2, e.e[1] - 5.4, 2.4, 0, TAU); g.fill(); } } });
  }, { fener: { isik: { x: 1100, y: 440, r: 520, sic: [1, .9, .72] }, kadraj: { tip: 'oval', x: 1000, y: 500, w: 1300, h: 900, yum: 40 } } });
  // B06: villa (Byron), sonra Byron'ın dizesi: güneş söner
  sahne('B06a', 'B06', 'gol', 'genis', (R, st) => {
    R.cam(1400 + st.lt * 12, 620, 1.25);
    GOL_GECE(R, st, {});
    DK.yagmur(R, st.t, { a: .2 });
  }, { fener: { isik: { x: 1000, y: 500, r: 760 }, kadraj: KARE },
    over: (ctx, st) => { etiket(ctx, 'VİLLA DİODATİ · LORD BYRON', 960, 160, st.lt - .3, rel(st, 'B06@bir') - .2); } });
  sahne('B06b', 'B06@bir', 'gunes', 'ayrinti', (R, st) => {
    const k = E.io3(clamp((st.lt - rel(st, 'B06@sönmüştü') + .2) / 1.6));
    R.cam(960, 520, 1.0 + st.lt * .01);
    R.gok(-400, -300, 2400, 1400, [[0, '#C29A5C'], [1, '#7C5A3C']], { firca: 1.4 });
    R.isikli(g => g.arc(960, 470, 230, 0, TAU), '#FFF1C8');
    R.yika(g => g.arc(960, 470, 232, 0, TAU), `rgba(30,22,18,${k * .95})`, { kay: 0, firca: .5 });
    R.yika(g => g.rect(-400, 760, 2800, 600), '#3A3040', { firca: 1 });
  }, { fener: st => ({ isik: { x: 960, y: 480, r: 700 }, kadraj: { tip: 'daire', x: 960, y: 480, r: 480, yum: 30 }, parlak: 1 - .55 * E.io3(clamp((st.lt - (A('B06@sönmüştü') - st.at)) / 1.6)) }),
    over: (ctx, st) => { quote(ctx, 'Bir düş gördüm, hepsi düş değildi. Parlak güneş sönmüştü.', 960, 780, st.lt, { px: 66, maxW: 1300, kaynak: 'Byron, “Karanlık”, 1816' }); } });
  // B07: Tambora: denizin ufkunda patlayan dağ; kül bulutu güneşi örter; sonra Cenevre'de yağan yağmur
  sahne('B07a', 'B07', 'tambora', 'genis', (R, st) => {
    const tP = rel(st, 'B07@patladı');
    const p = E.out3(clamp((st.lt - tP + .3) / 3.5));
    R.cam(960 + st.lt * 8, 540 - p * 40, 1.0 - p * .08);
    R.gok(-600, -600, 2600, 700, [[0, '#7E8EA8'], [1, '#D7B98C']], { firca: 1.2 });
    DK.gol(R, -600, 2600, 700, 1400, '#5E7C96', '#2C4258', { t: st.t, yx: 900, yw: 300, n: 18, yansima: 'rgba(255,200,130,.5)' });
    DK.yanardag(R, 820, 720, .8, p, st.lt);
  }, { fener: { isik: { x: 900, y: 460, r: 820, sic: [1, .9, .76] }, kadraj: KARE },
    over: (ctx, st) => { etiket(ctx, 'TAMBORA · ENDONEZYA · NİSAN 1815', 960, 150, rel(st, 'B07@tambora') - .2, st.d - .3); } });
  sahne('B07b', 'B07@bunu', 'mektup', 'yakin', (R, st) => {
    R.cam(1500, 360, 1.45 + st.lt * .02);
    R.gok(-400, -300, 2400, 1400, [[0, '#7A5638'], [1, '#5A3E2A']], { firca: 1.2 });
    DK.pencere(R, 1500, 300, 420, 560, { gece: '#647698' });
    DK.yagmur(R, st.t, { a: .35, n: 120, kutu: [1290, 20, 420, 560] });
    FIG.kisi(R, 1240, 1000, 560, { tip: 'mary', f: 1, bas: -.12, kolO: [.4, 1.4], kolA: [.2, 1.3] });
  }, { fener: { isik: { x: 1100, y: 420, r: 520, sic: [.95, .9, .8] }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1300, h: 900, yum: 40 } } });
  // B08: hayalet hikâyeleri kitabı (ayrıntı): Fantasmagoriana
  sahne('B08a', 'B08', 'salon', 'ayrinti', (R, st) => {
    R.cam(960, 560, 1.0 + st.lt * .02);
    R.gok(-400, -300, 2400, 1400, [[0, '#8E5A36'], [1, '#5C3A24']], { firca: 1.2 });
    const ac = E.io3(clamp((st.lt - .6) / 1.4));
    R.kara(g => { g.moveTo(560, 760); g.lineTo(1360, 760); g.lineTo(1340, 800); g.lineTo(580, 800); g.closePath(); });
    R.isikli(g => { g.moveTo(600, 760); g.quadraticCurveTo(780, 700 - ac * 20, 960, 752); g.quadraticCurveTo(1140, 700 - ac * 20, 1320, 760); g.lineTo(1320, 772); g.lineTo(600, 772); g.closePath(); }, '#EDE0C0');
    R.isikli(g => g.rect(640, 430, 640, 300), '#E6D6B0');
    SET.camYazi(R, 'FANTASMAGORIANA', 960, 520, { px: 64, ls: 6, renk: '#2A1A10', force: true });
    SET.camYazi(R, 'ou Recueil d’Histoires d’Apparitions', 960, 600, { font: FONT.alinti(40), renk: '#3A2418', force: true });
    DK.ates(R, 1650, 960, 260, { t: st.t });
  }, { fener: { isik: { x: 960, y: 560, r: 640, sic: [1, .86, .62] }, kadraj: { tip: 'oval', x: 960, y: 540, w: 1500, h: 920, yum: 40 } } });
  // B09: Byron ayağa kalkar, öneri (orta); ışık onda
  sahne('B09a', 'B09', 'salon', 'orta', (R, st) => {
    const k = E.out3(clamp((st.lt - .3) / 1.2));
    R.cam(760, 560, 1.0);
    SET.salon(R, st);
    FIG.kisi(R, 700, 960, 480, { tip: 'byron', f: 1, kolO: [lerp(.2, 1.2, k), lerp(.4, 1.0, k)], kolA: [-.1, .4], bas: -.05 });
    FIG.kisi(R, 1080, 960, 470, { tip: 'percy', f: -1, bacak: 'otur' });
    FIG.kisi(R, 1340, 960, 440, { tip: 'mary', f: -1, bacak: 'otur' });
  }, { fener: { isik: { x: 760, y: 470, r: 600, sic: [1, .86, .62] }, kadraj: KARE } });
  // B10: sabahlar: ötekiler yazar, Mary'nin kâğıdı boş; "her sabah"ta başını sallar (yakın)
  sahne('B10a', 'B10', 'masa', 'genis', (R, st) => {
    R.cam(960 + st.lt * 10, 560, .95);
    R.gok(-600, -400, 2600, 1500, [[0, '#A9A49A'], [1, '#7E766A']], { firca: 1.2 });
    DK.pencere(R, 1600, 340, 360, 480, { gece: '#B7C2CF' });
    DK.yagmur(R, st.t, { a: .14, n: 40, kutu: [1420, 100, 360, 480] });
    DK.masa(R, 960, 760, 1300, { h: 220 });
    const yaz = Math.sin(st.lt * 7);
    FIG.kisi(R, 420, 980, 460, { tip: 'byron', f: 1, bacak: 'otur', govde: .3, bas: .3, kolO: [1.4 + yaz * .04, 1.0] });
    FIG.kisi(R, 1500, 980, 470, { tip: 'percy', f: -1, bacak: 'otur', govde: .3, bas: .3, kolO: [1.4 - yaz * .04, 1.0] });
    FIG.kisi(R, 960, 980, 430, { tip: 'mary', f: 1, bacak: 'otur', govde: .05, bas: .2, kolO: [1.2, 1.3], kolA: [1.1, 1.4] });
    R.isikli(g => { g.rect(560, 744, 140, 10); g.rect(1220, 744, 140, 10); g.rect(1040, 744, 150, 10); }, '#EFE6CC');
  }, { fener: { isik: { x: 960, y: 520, r: 760, sic: [.98, .95, .88] }, kadraj: KARE } });
  sahne('B10b', 'B10@ve', 'masa', 'yakin', (R, st) => {
    R.cam(1000, 560, 1.7);
    R.gok(-600, -400, 2600, 1500, [[0, '#A9A49A'], [1, '#7E766A']], { firca: 1.2 });
    const s = Math.sin(st.lt * 5) * clamp(1 - st.lt / 2.5) * .18;
    FIG.kisi(R, 960, 980, 430, { tip: 'mary', f: 1, bacak: 'otur', govde: .05, bas: .2 + s, kolO: [1.2, 1.3], kolA: [1.1, 1.4] });
    DK.masa(R, 960, 760, 1300, { h: 220 }); R.isikli(g => g.rect(1040, 744, 150, 10), '#EFE6CC');
  }, { fener: { isik: { x: 1000, y: 470, r: 440 }, kadraj: { tip: 'daire', x: 960, y: 500, r: 440, yum: 30 } } });
  // B11: gece konuşması: Byron ve Percy ateşin önünde (ışık onlarda), Mary kenarda, karanlıkta dinler
  sahne('B11a', 'B11', 'salon', 'orta', (R, st) => {
    R.cam(820 - st.lt * 8, 580, 1.05);
    SET.salon(R, st);
    const j = Math.sin(st.lt * 2.2);
    FIG.kisi(R, 720, 960, 470, { tip: 'byron', f: 1, bacak: 'otur', govde: .1, kolO: [.9 + j * .2, 1.1] }); DK.sandalye(R, 650, 700, .8);
    FIG.kisi(R, 1080, 960, 480, { tip: 'percy', f: -1, bacak: 'otur', govde: .15, kolO: [.9 - j * .2, 1.0] });
    FIG.kisi(R, 1420, 960, 440, { tip: 'mary', f: -1, bacak: 'otur', bas: .1, kolO: [.6, 1.6], kolA: [.5, 1.6] });
    if (st.lt > rel(st, 'B11@ölü')) { const k = clamp((st.lt - rel(st, 'B11@ölü')) / .6); DK.ates(R, 360, 870, 200 + 120 * Math.sin(k * PI), { t: st.t }); }
  }, { fener: { isik: { x: 880, y: 520, r: 520, sic: [1, .84, .6] }, kadraj: KARE } });
  // B12: yatakta, uykusuz; kepenk aralığından ay
  sahne('B12a', 'B12', 'yatak', 'yakin', (R, st) => {
    R.cam(980, 600, 1.4 + st.lt * .01);
    R.gok(-400, -300, 2400, 1400, [[0, '#7182AE'], [1, '#56628A']], { firca: 1.2 });
    R.yika(g => { g.moveTo(1500, 0); g.lineTo(1560, 0); g.lineTo(1100, 1100); g.lineTo(980, 1100); g.closePath(); }, 'rgba(230,236,250,.7)', { kay: 0, firca: 0 });
    R.yika(g => g.rect(500, 660, 1000, 300), '#C9C0B0', { firca: .7 });
    R.yika(g => g.ellipse(700, 640, 150, 46, 0, 0, TAU), '#E8E2D4', { kay: 0 });   // yastık
    R.g.save(); R.g.translate(1300, 640); R.g.rotate(-PI / 2); FIG.kisi(R, 0, 0, 640, { tip: 'mary', f: -1, bas: -.1 }); R.g.restore();   // sırtüstü, yüz yukarı
    R.yika(g => { g.moveTo(860, 610); g.quadraticCurveTo(1150, 570, 1500, 620); g.lineTo(1500, 760); g.lineTo(860, 760); g.closePath(); }, '#D9D0BE', { firca: .8 });   // yorgan
  }, { fener: { isik: { x: 760, y: 600, r: 460, sic: [.9, .92, 1] }, kadraj: { tip: 'daire', x: 820, y: 600, r: 440, yum: 30 } } });
  // B13: uyanık düş: Mary'nin üstünde ikinci, küçük bir fener dairesi açılır: öğrenci, örtülü beden kıpırdar, öğrenci kaçar
  sahne('B13a', 'B13', 'dus', 'orta', (R, st) => {
    const tK = rel(st, 'B13@kıpırdıyor'), tKc = rel(st, 'B13@kaçıyor');
    R.cam(960, 540, 1.0 + st.lt * .01);
    R.gok(-400, -300, 2400, 1400, [[0, '#7A7290'], [1, '#5A546E']], { firca: 1.4 });
    // masa ve örtülü beden
    R.kara(g => { g.rect(620, 700, 760, 30); g.rect(650, 720, 24, 260); g.rect(1330, 720, 24, 260); });
    const kp = st.lt > tK ? Math.sin((st.lt - tK) * 9) * clamp(1 - (st.lt - tK) / 2.5) * 6 : 0;
    R.yika(g => { g.moveTo(640, 700); g.quadraticCurveTo(760, 640 + kp, 900, 662); g.quadraticCurveTo(1100, 650 - kp, 1360, 676); g.lineTo(1370, 704); g.lineTo(630, 704); g.closePath(); }, '#D4CCB8', { firca: .8 });
    // öğrenci: önce diz çökmüş, sonra kaçar
    const ka = st.lt > tKc ? E.in3(clamp((st.lt - tKc) / 1.4)) : 0;
    if (ka < 1) FIG.kisi(R, 560 - ka * 700, 980, 440, { tip: 'victor', f: ka > 0 ? -1 : 1, bacak: ka > 0 ? 'dur' : 'diz', govde: ka > 0 ? .2 : .25, kolO: [ka > 0 ? .8 : 1.2, .8] });
  }, { fener: { isik: { x: 960, y: 520, r: 520, sic: [.95, .92, .86] }, kadraj: { tip: 'daire', x: 960, y: 560, r: 470, yum: 50 }, parlak: 1.05 } });
  // B14: yatağın başı, düşte: sarı, ıslak, düşünen gözler (A01'in yankısı; yaratığın yüzü yakın, gözler öne)
  sahne('B14a', 'B14', 'dus', 'yakin', (R, st) => {
    R.cam(1100, 380, 2.2 + st.lt * .03);
    ODA_GECE(R, st, { ay: false });
    DK.perde(R, 1290, 1520, 60, 700, '#B0433A', { t: st.lt * .3, kivrim: 6 });
    FIG.kisi(R, 1060, 1000, 700, { tip: 'yaratik', f: 1, govde: .2, bas: .25, kolA: [1.55, .1], kolO: [.9, .6], goz: clamp((st.lt - .4) / .5), kenar: 'rgba(240,210,160,.7)' });
  }, { fener: { isik: { x: 1000, y: 420, r: 420, sic: [.95, .92, .86] }, kadraj: { tip: 'daire', x: 960, y: 500, r: 430, yum: 50 }, parlak: .9 } });
  // B15: Mary korkuyla gözlerini açar ve doğrulur
  sahne('B15a', 'B15', 'yatak', 'orta', (R, st) => {
    const k = E.outBack(clamp(st.lt / .7));
    R.cam(980, 600, 1.15);
    R.gok(-400, -300, 2400, 1400, [[0, '#7182AE'], [1, '#56628A']], { firca: 1.2 });
    R.yika(g => { g.moveTo(1500, 0); g.lineTo(1560, 0); g.lineTo(1100, 1100); g.lineTo(980, 1100); g.closePath(); }, 'rgba(230,236,250,.7)', { kay: 0, firca: 0 });
    R.kara(g => { g.rect(480, 560, 30, 440); g.rect(480, 960, 1060, 40); g.rect(1510, 760, 30, 240); });   // karyola
    R.yika(g => g.ellipse(640, 740, 120, 40, 0, 0, TAU), '#E8E2D4', { kay: 0 });   // yastık
    FIG.kisi(R, 860, 990, 470, { tip: 'mary', f: 1, bacak: 'otur', sandalye: false, govde: lerp(-.9, .05, k), bas: lerp(-.4, .1, k), kolO: [lerp(.2, .9, k), .8] });
    R.yika(g => { g.moveTo(780, 800); g.quadraticCurveTo(1100, 760, 1510, 800); g.lineTo(1510, 960); g.lineTo(780, 960); g.closePath(); }, '#D9D0BE', { firca: .8 });
  }, { fener: { isik: { x: 900, y: 560, r: 500, sic: [.9, .92, 1] }, kadraj: KARE } });
  // B16: ertesi sabah: Mary yazar; kâğıtta ilk cümle
  sahne('B16a', 'B16', 'masa', 'genis', (R, st) => {
    R.cam(900, 560, 1.0 + st.lt * .015);
    SET.masa(R, st, { gece: '#C4CCD6' });
    FIG.kisi(R, 560, 960, 500, { tip: 'mary', f: 1, bacak: 'otur', govde: .25, bas: .3, kolO: [1.3 + Math.sin(st.lt * 6) * .04, 1.0], kolA: [1.0, 1.2] });
    R.isikli(g => g.rect(720, 626, 170, 12), '#F1E6C9');
  }, { fener: { isik: { x: 900, y: 520, r: 760, sic: [1, .97, .9] }, kadraj: KARE } });
  sahne('B16b', 'B16@yazdığı', 'mektup', 'ayrinti', (R, st) => {
    R.cam(980 + st.lt * 10, 560, 1.4);
    R.gok(-400, -300, 2400, 1400, [[0, '#9A7A58'], [1, '#7A5E44']], { firca: 1.2 });
    R.isikli(g => { g.moveTo(460, 520); g.lineTo(1460, 480); g.lineTo(1520, 800); g.lineTo(520, 840); g.closePath(); }, '#F2E7CB');
    SET.elYazisi(R, 'It was on a dreary night of November', 600, 660, 62, clamp((st.lt - .6) / 2.8), { maxW: 1000 });
  }, { fener: { isik: { x: 960, y: 560, r: 640, sic: [1, .96, .88] }, kadraj: { tip: 'oval', x: 960, y: 560, w: 1500, h: 900, yum: 40 } },
    over: (ctx, st) => { kunye(ctx, 'Frankenstein, 1818, IV. bölümün ilk cümlesi', st.lt - 1.2, st.d); } });
})();
