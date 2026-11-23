// H: VII. Çirkin evladım (H01–H11): 1831 önsözü ve 1815 günlüğü yan yana (nedensellik kurulmaz); bitiş ekranı. Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  const KARE = { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 };
  sahne('H00k', 'H01-1.2', 'kart', 'kart', (R, st) => { R.cam(960, 540, 1); SET.kart(R, st, 'VII', 'ÇİRKİN EVLADIM', 'On sekiz yaşında bir kız bunu neden yazdı?'); },
    { fener: { isik: { x: 960, y: 480, r: 900 }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1500, h: 860, yum: 30 } }, tr: { type: 'iris', dur: 1.6 } });
  // kâğıt slaytı: krem sayfa, mürekkep harfler (ekran koordinatı)
  const sayfa = (R, w = 980, h = 860) => { R.gok(-600, -400, 2600, 1500, [[0, '#6A5038'], [1, '#4A3626']], { firca: 1.3 }); R.ekran(g => { g.fillStyle = '#EFE4C6'; g.fillRect(960 - w / 2, 520 - h / 2, w, h); }); };
  const satir = (R, s, y, px, o = {}) => SET.camYazi(R, s, o.x ?? 960, y, { px, font: o.font || FONT.metin(px, 600), renk: o.renk || '#2A1A10', ls: o.ls ?? 2, force: true, p: o.p ?? 1, align: o.align });
  // H02a: 1818 başlık sayfası: yazar adının olacağı yer boş
  sahne('H02a', 'H02', 'kitap', 'ayrinti', (R, st) => {
    R.cam(960, 540, 1.0 + st.lt * .01);
    sayfa(R);
    satir(R, 'FRANKENSTEIN;', 230, 72, { ls: 6 }); satir(R, 'OR,', 300, 40); satir(R, 'THE MODERN PROMETHEUS.', 360, 52, { ls: 4 });
    satir(R, 'IN THREE VOLUMES.', 470, 36); satir(R, 'VOL. I.', 520, 36);
    satir(R, 'London:', 760, 40, { font: FONT.alinti(40) }); satir(R, '1818.', 830, 40);
    const k = clamp((st.lt - rel(st, 'H02@kapağında')) / .6);
    if (k > 0) R.ekran(g => { g.save(); g.setLineDash([14, 12]); g.strokeStyle = `rgba(160,60,40,${k})`; g.lineWidth = 4; g.strokeRect(700, 590, 520, 90); g.restore(); });
  }, { fener: { isik: { x: 960, y: 520, r: 620, sic: [1, .92, .78] }, kadraj: { tip: 'kare', x: 960, y: 520, w: 1100, h: 940, r: 40, yum: 30 } },
    over: (ctx, st) => { kunye(ctx, 'Frankenstein, ilk baskı, 1818', st.lt - .5, st.d); } });
  // H02b: 1823 afişi: yaratığın adının yerinde çizgi
  sahne('H02b', 'H02@yıllar', 'afis', 'ayrinti', (R, st) => {
    R.cam(960, 540, 1.0 + st.lt * .015);
    sayfa(R, 860, 900);
    satir(R, 'ENGLISH OPERA HOUSE', 150, 44, { ls: 4 }); satir(R, '1823', 205, 38);
    satir(R, 'PRESUMPTION;', 300, 64, { ls: 4 }); satir(R, 'or, the Fate of Frankenstein', 370, 46, { font: FONT.alinti(46) });
    satir(R, 'Frankenstein  . . . . . .  Mr. WALLACK', 520, 38, { ls: 1 });
    const k = clamp((st.lt - rel(st, 'H02@çizgi') + .2) / .5);
    satir(R, '— — —  . . . . . .  Mr. T. P. COOKE', 600, 38, { ls: 1, renk: k > 0 ? `rgb(${lerp(42, 170, k)},${lerp(26, 50, k)},${lerp(16, 30, k)})` : '#2A1A10' });
  }, { fener: { isik: { x: 960, y: 520, r: 620, sic: [1, .92, .78] }, kadraj: { tip: 'kare', x: 960, y: 520, w: 960, h: 980, r: 40, yum: 30 } },
    over: (ctx, st) => { kunye(ctx, 'Oyun afişi, Mary Shelley’nin mektubundan, 1823', st.lt - .5, st.d); } });
  // H03: 1831: Mary (yas siyahı) masada yazar
  sahne('H03a', 'H03', 'masa', 'orta', (R, st) => {
    R.cam(900, 560, 1.0 + st.lt * .01);
    SET.masa(R, st, { gece: '#B8C0CC' });
    FIG.kisi(R, 560, 960, 500, { tip: 'mary', f: 1, bacak: 'otur', govde: .25, bas: .3, kolO: [1.3 + Math.sin(st.lt * 6) * .04, 1.0], kolA: [1.0, 1.2] });
    DK.sandalye(R, 470, 700, .9);
    R.isikli(g => g.rect(720, 626, 170, 12), '#F1E6C9');
    DK.mum(R, 1080, 640, 150, { t: st.t });
  }, { fener: { isik: { x: 820, y: 560, r: 640, sic: [1, .92, .8] }, kadraj: { tip: 'oval', x: 900, y: 540, w: 1500, h: 960, yum: 40 } },
    over: (ctx, st) => { etiket(ctx, '1831 · ÖNSÖZ', 600, 170, st.lt - .2, st.d - .3); } });
  // H04: önsözdeki cümle
  sahne('H04a', 'H04', 'kitap', 'yakin', (R, st) => {
    R.cam(960, 540, 1.0);
    sayfa(R, 1300, 700);
    SET.elYazisi(R, '…the offspring of happy days, when death and grief were but words, which found no true echo in my heart.', 420, 420, 50, 1, { maxW: 1100 });
  }, { fener: { isik: { x: 960, y: 520, r: 700, sic: [1, .94, .84] }, kadraj: { tip: 'oval', x: 960, y: 520, w: 1500, h: 860, yum: 40 } },
    over: (ctx, st) => { quote(ctx, 'Ölüm ve keder, o zaman benim için yalnızca sözcüklerdi.', 960, 760, st.lt - .3, { px: 64, maxW: 1400, kaynak: 'Mary Shelley, 1831 önsözü' }); } });
  // H05: 1815 günlüğü (13 Mart)
  sahne('H05a', 'H05', 'gunluk', 'ayrinti', (R, st) => {
    R.cam(960, 540, 1.0 + st.lt * .012);
    sayfa(R, 1200, 760);
    satir(R, 'Monday, March 13.', 300, 46, { font: FONT.alinti(46), x: 420, align: 'left' });
    SET.elYazisi(R, '…whenever I am left alone to my own thoughts… they always come back to the same point — that I was a mother, and am so no longer.', 420, 400, 44, clamp((st.lt - 1) / 4), { maxW: 1080 });
  }, { fener: { isik: { x: 960, y: 520, r: 700, sic: [1, .92, .78] }, kadraj: { tip: 'oval', x: 960, y: 520, w: 1500, h: 900, yum: 40 } },
    over: (ctx, st) => { etiket(ctx, 'MARY’NİN GÜNLÜĞÜ · 13 MART 1815', 960, 150, st.lt - .3, st.d - .3, { px: 42 });
      quote(ctx, 'Bir anneydim, artık değilim.', 960, 790, st.lt - rel(st, 'H05@bir'), { px: 68, panel: .7 }); } });
  // H06: düş: ocak ateşi, küçük örtülü bohça ve dört el; "uyandım"da ateş söner, beşik boş
  sahne('H06a', 'H06', 'dus', 'ayrinti', (R, st) => {
    R.cam(960, 600, 1.1 + st.lt * .015);
    R.gok(-600, -400, 2600, 1500, [[0, '#8E5A36'], [1, '#5C3A24']], { firca: 1.3 });
    DK.ates(R, 1380, 900, 260, { t: st.t });
    R.yika(g => g.ellipse(900, 720, 120, 70, 0, 0, TAU), '#E6D8BA', { kay: 0 });
    const ov = Math.sin(st.lt * 4) * 8;
    FIG.elYakin(R, 760 + ov, 700, 15, 1, false, .3); FIG.elYakin(R, 1050 - ov, 710, 15, -1, false, .3);
  }, { fener: { isik: { x: 1000, y: 640, r: 560, sic: [1, .84, .6] }, kadraj: { tip: 'daire', x: 980, y: 600, r: 450, yum: 60 } },
    over: (ctx, st) => { kunye(ctx, 'Günlük, 19 Mart 1815', st.lt - .5, st.d); } });
  sahne('H06b', 'H06@uyandım', 'besik', 'orta', (R, st) => {
    R.cam(960, 560, 1.05 + st.lt * .01);
    R.gok(-400, -300, 2400, 1400, [[0, '#56607E'], [1, '#3C4258']], { firca: 1.2 });
    R.yika(g => g.rect(-400, 820, 2800, 600), '#4A3E3A', { firca: 1 });
    DK.besik(R, 960, 820, 2.2, { a: 0 });
  }, { fener: { isik: { x: 960, y: 560, r: 480, sic: [.9, .92, 1] }, kadraj: { tip: 'daire', x: 960, y: 560, r: 440, yum: 40 }, parlak: .75 } });
  // H07: iki kayıt, iki ayrı fener dairesi yan yana (birleşmezler)
  sahne('H07a', 'H07', 'iki', 'genis', (R, st) => {
    R.cam(960, 540, 1.0);
    R.kara(g => g.rect(-2000, -2000, 6000, 6000), { renk: '#140C07' });
    for (const [x, ust, alt] of [[560, '1831', 'ÖNSÖZ'], [1360, '1815', 'GÜNLÜK']]) {
      R.ekran(g => { const gr = g.createRadialGradient(x, 500, 0, x, 500, 330); gr.addColorStop(0, '#EFE2C2'); gr.addColorStop(.8, '#D8C49C'); gr.addColorStop(1, 'rgba(20,12,7,1)'); g.fillStyle = gr; g.beginPath(); g.arc(x, 500, 330, 0, TAU); g.fill(); });
      satir(R, ust, x === 560 ? 460 : 460, 80, { x, ls: 6 }); satir(R, alt, 560, 46, { x, ls: 8 });
    }
  }, { fener: { isik: { x: 960, y: 500, r: 900 }, kadraj: KARE } });
  // H08: Mary kitabı göğsünden ışığa uzatır: "git ve yolun açık olsun"
  sahne('H08a', 'H08', 'salon', 'orta', (R, st) => {
    const k = E.io3(clamp((st.lt - rel(st, 'H08@git') + .2) / 1.6));
    R.cam(1000, 560, 1.15);
    R.gok(-600, -400, 2600, 1500, [[0, '#A88A66'], [1, '#7A6046']], { firca: 1.2 });
    DK.pencere(R, 1480, 380, 360, 520, { gece: '#D8E2EA' });
    R.yika(g => g.rect(-600, 900, 3200, 700), '#5A4030', { firca: 1 });
    FIG.kisi(R, 1060, 960, 500, { tip: 'mary', f: 1, bas: lerp(.25, -.05, k), kolO: [lerp(1.2, 1.3, k), lerp(1.4, .5, k)], kolA: [lerp(1.0, 1.25, k), lerp(1.5, .6, k)],
      el: { on: (R2, e) => { const g = R2.g; g.save(); g.translate(e.e[0], e.e[1]); g.rotate(-e.a + PI / 2); g.fillStyle = '#5A2A1C'; g.fillRect(-1, -6, 9, 12); g.fillStyle = '#E8DCC0'; g.fillRect(7.6, -5.4, 1.2, 10.8); g.restore(); } } });
  }, { fener: st => ({ isik: { x: lerp(1060, 1300, E.io3(clamp((st.lt - (A('H08@git') - st.at)) / 2))), y: 480, r: lerp(480, 760, E.io3(clamp((st.lt - (A('H08@git') - st.at)) / 2))), sic: [1, .95, .86] }, kadraj: KARE }),
    over: (ctx, st) => { quote(ctx, 'Çirkin evladıma bir kez daha, git ve yolun açık olsun, diyorum.', 860, 170, st.lt - rel(st, 'H08@çirkin'), { px: 58, maxW: 1300, kaynak: 'Mary Shelley, 1831', panel: .6 }); } });
  // H09: Victor yarattığından kaçar (karanlığa); Mary kitabı ışıkta tutar
  sahne('H09a', 'H09', 'iki', 'genis', (R, st) => {
    R.cam(960, 560, 1.0);
    R.gok(-600, -400, 2600, 1500, [[0, '#6E6A70'], [1, '#4A4650']], { firca: 1.3 });
    R.yika(g => g.rect(-600, 900, 3200, 700), '#3A3030', { firca: 1 });
    const g = HAREKET.yuruyus({ tip: 'kos', uyluk: 23, baldir: 23, tur: .6 });
    const y = HAREKET.yuruyusYolu(g, { t0: 0, t1: 8, x0: 640, yon: -1, olcek: 3.4, go: () => 1 })(st.lt);
    FIG.kisi(R, y.x, 960, 360, { tip: 'victor', f: -1, bacak: y.poz, govde: .25, kolO: [.8 + Math.sin(TAU * y.faz) * .6, .9], kolA: [-.6 - Math.sin(TAU * y.faz) * .6, .9] });
    const k = E.io3(clamp((st.lt - rel(st, 'H09@meri')) / 1));
    FIG.kisi(R, 1340, 960, 460, { tip: 'mary', f: -1, kolO: [1.25, .5], kolA: [1.2, .6],
      el: { on: (R2, e) => { const gg = R2.g; gg.save(); gg.translate(e.e[0], e.e[1]); gg.fillStyle = '#5A2A1C'; gg.fillRect(-2, -10, 10, 13); gg.restore(); } } });
  }, { fener: st => { const k = E.io3(clamp((st.lt - (A('H09@meri') - st.at)) / 1.4)); return { isik: { x: lerp(500, 1320, k), y: 560, r: 560 }, kadraj: KARE }; } });
  // H10: yarım kalan: boş masa, yarım yazılmış sayfa, bırakılmış kalem; ışık yavaşça açılır
  sahne('H10a', 'H10', 'masa', 'yakin', (R, st) => {
    R.cam(960, 600, 1.5 - st.lt * .02);
    R.gok(-600, -400, 2600, 1500, [[0, '#6A5038'], [1, '#4A3626']], { firca: 1.3 });
    DK.masa(R, 960, 700, 1000, { h: 300 });
    R.isikli(g => { g.moveTo(700, 690); g.lineTo(1140, 676); g.lineTo(1170, 700); g.lineTo(720, 712); g.closePath(); }, '#EFE4C6');
    R.cizgi([[1180, 694], [1330, 640]], 4);
    R.kara(g => { g.moveTo(1250, 668); g.bezierCurveTo(1300, 620, 1360, 600, 1420, 560); g.bezierCurveTo(1380, 610, 1330, 650, 1270, 678); g.closePath(); });
    DK.sandalye(R, 560, 720, .9);
  }, { fener: st => ({ isik: { x: 960, y: 620, r: lerp(300, 620, E.io3(clamp(st.lt / 5))), sic: [1, .9, .74] }, kadraj: { tip: 'daire', x: 960, y: 600, r: lerp(260, 520, E.io3(clamp(st.lt / 5))), yum: 50 } }) });
  // H11: bitiş: sol üçte birde Prometheus'un ateşi (küçük alev), sağ taraf bitiş ekranı öğelerine boş
  sahne('H11a', 'H11', 'son', 'orta', (R, st) => {
    R.cam(960, 560, 1.0);
    R.kara(g => g.rect(-2000, -2000, 6000, 6000), { renk: '#140C07' });
    R.gok(80, 160, 760, 900, [[0, '#4A3A50'], [1, '#2A2030']], { firca: 1.2 });
    DK.ates(R, 420, 760, 220, { t: st.t });
    FIG.kisi(R, 300, 820, 420, { tip: 'yaratik', f: 1, bacak: 'cok', govde: .2, kolO: [1.2, .6], goz: 1 });
    SET.camYazi(R, 'MODERN PROMETHEUS', 420, 300, { px: 56, ls: 6, p: clamp((st.lt - .4) / 1) });
  }, { fener: { isik: { x: 420, y: 520, r: 520, sic: [1, .86, .62] }, kadraj: { tip: 'oval', x: 420, y: 520, w: 700, h: 820, yum: 40 } } });
})();
