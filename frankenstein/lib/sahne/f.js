// F: V. Ben de yaratabilirim (F01–F11). Şiddet gösterilmez: an fener kapanarak geçilir; yerde parlayan madalyon kalır. Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  const KARE = { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 };
  sahne('F00k', 'F01-1.4', 'kart', 'kart', (R, st) => { R.cam(960, 540, 1); SET.kart(R, st, 'V', 'BEN DE YARATABİLİRİM', 'Terk edilen ne yapar?'); },
    { fener: { isik: { x: 960, y: 480, r: 900 }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1500, h: 860, yum: 30 } }, tr: { type: 'iris', dur: 1.2 } });
  window.CAYIR = (R, st, o = {}) => {
    R.gok(-600, -400, 2600, 760, [[0, '#6C5A7E'], [.6, '#C68A6A'], [1, '#E9B98A']], { firca: 1.2 });
    DK.daglar(R, -600, 2600, 700, [[-200, 560], [400, 500], [1000, 540], [1600, 480], [2200, 530]], '#5A4A68', {});
    R.yika(g => g.rect(-600, 700, 3200, 800), '#6E7A4A', { firca: 1 });
    R.kara(g => { g.moveTo(-600, 920); for (let x = -600; x <= 2600; x += 60) g.lineTo(x, 910 + Math.sin(x * .02) * 8 - (x % 120 === 0 ? 14 : 0)); g.lineTo(2600, 1500); g.lineTo(-600, 1500); g.closePath(); });
  };
  // F01: alacakaranlık çayır; çocuk koşar, yaratık ağacın ardından bakar
  sahne('F01a', 'F01+2.2', 'cayir', 'genis', (R, st) => {
    R.cam(960 + st.lt * 10, 560, 1.0);
    CAYIR(R, st);
    DK.kayin(R, 470, 920, 640, { sal: Math.sin(st.t * .5) });
    const g = HAREKET.yuruyus({ tip: 'kos', tur: .5 });
    const y = HAREKET.yuruyusYolu(g, { t0: 0, t1: 9, x0: 1700, yon: -1, olcek: 2.4, go: t => 1 - HAREKET.rampa(t, 4, 4.6) })(st.lt);
    FIG.kisi(R, y.x, 920, 360, { tip: 'cocuk', f: -1, bacak: y.poz, govde: .15 * y.go, kolO: [Math.sin(TAU * y.faz) * .7 * y.go, .9], kolA: [-Math.sin(TAU * y.faz) * .7 * y.go, .9] });
    FIG.kisi(R, 300, 930, 460, { tip: 'yaratik', f: 1, govde: .1, bas: .1, goz: 1 });
  }, { fener: { isik: { x: 900, y: 540, r: 820, sic: [1, .92, .8] }, kadraj: KARE } });
  // F02: çocuk gözlerini kapatır, çığlık; "Frankenstein" adı slayta düşer (yakın)
  sahne('F02a', 'F02', 'cayir', 'yakin', (R, st) => {
    R.cam(900, 680, 1.35);
    CAYIR(R, st);
    FIG.kisi(R, 1080, 930, 520, { tip: 'cocuk', f: -1, govde: -.08, bas: -.1, kolO: [2.6, 1.6], kolA: [2.5, 1.7] });
    FIG.kisi(R, 520, 930, 520, { tip: 'yaratik', f: 1, govde: .05, goz: 1 });
    SET.camYazi(R, 'FRANKENSTEIN', 960, 170, { px: 110, ls: 14, p: clamp((st.lt - rel(st, 'F02@frankenştayn')) / .7), renk: '#F2B89A' });
  }, { fener: { isik: { x: 1000, y: 520, r: 520, sic: [1, .9, .78] }, kadraj: { tip: 'oval', x: 980, y: 500, w: 1400, h: 900, yum: 40 } } });
  // F03: düşmanın adı; yaratığın gölgesi çocuğun üstüne düşer; fener kapanır (şiddet gösterilmez); açılınca çayırda yalnız madalyon
  sahne('F03a', 'F03', 'cayir', 'orta', (R, st) => {
    R.cam(960, 600, 1.3);
    CAYIR(R, st);
    const k = E.io3(clamp(st.lt / 3));
    R.yika(g => { g.moveTo(640, 935); g.lineTo(640 + 560 * k, 930); g.lineTo(640 + 560 * k, 950); g.lineTo(640, 955); g.closePath(); }, 'rgba(20,14,12,.7)', { kay: 0, firca: 0 });   // uzayan gölge
    FIG.kisi(R, 1180, 930, 360, { tip: 'cocuk', f: -1, govde: -.15 });
    FIG.kisi(R, 600, 940, 600, { tip: 'yaratik', f: 1, govde: .08, bas: .1, goz: 1 });
  }, { fener: st => { const tS = A('F03@susturmak') - st.at; const k = clamp((st.lt - tS) / 1.2); return { isik: { x: 1000, y: 540, r: 600, sic: [1, .86, .7] }, kadraj: { tip: 'daire', x: 1000, y: 560, r: 470 * (1 - E.io3(k)), yum: 40 }, parlak: 1 - k * .5 }; } });
  sahne('F03b', 'F03@bir+.4', 'cayir', 'ayrinti', (R, st) => {
    R.cam(960, 820, 2.2 + st.lt * .02);
    CAYIR(R, st);
    const p = .5 + .5 * Math.sin(st.lt * 3);
    R.isikli(g => g.ellipse(960, 880, 22, 28, 0, 0, TAU), '#F6D27A');
    R.g.save(); R.g.globalCompositeOperation = 'source-over'; R.g.strokeStyle = '#3A2A10'; R.g.lineWidth = 3; R.g.beginPath(); R.g.moveTo(960, 852); R.g.quadraticCurveTo(1000, 760, 1080, 790); R.g.stroke(); R.g.restore();
    R.sonra(ctx => { const [x, y] = R.ekr(960, 880); const gr = ctx.createRadialGradient(x, y, 0, x, y, 120); gr.addColorStop(0, `rgba(255,230,150,${.35 * p})`); gr.addColorStop(1, 'rgba(255,230,150,0)'); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = gr; ctx.fillRect(x - 130, y - 130, 260, 260); });
  }, { fener: st => ({ isik: { x: 960, y: 560, r: 520, sic: [1, .86, .7] }, kadraj: { tip: 'daire', x: 960, y: 560, r: 440 * E.io3(clamp(st.lt / 1)), yum: 40 }, parlak: .7 }) });
  // F04: el çırpma; gök kızarır, yaratık dimdik (orta)
  sahne('F04a', 'F04', 'cayir', 'genis', (R, st) => {
    R.cam(960, 560, 1.0);
    R.gok(-600, -400, 2600, 900, [[0, '#2A2238'], [1, '#6A4A5A']], { firca: 1.3 });
    R.kara(g => g.rect(-600, 900, 3200, 600));
    const c = Math.abs(Math.sin(st.lt * 7)) * clamp(1 - st.lt / 1.4);
    FIG.kisi(R, 960, 910, 640, { tip: 'yaratik', f: 1, govde: -.1, bas: -.2, kolO: [1.5, .4 + c * .5], kolA: [1.5, .5 + c * .5], pel: 1, sac: 1, goz: 1 });
  }, { fener: { isik: { x: 960, y: 520, r: 760, sic: [1, .82, .7] }, kadraj: KARE } });
  // F05: madalyondaki kadın (renkli minyatür); yaratığın eli tutar
  sahne('F05a', 'F05', 'madalyon', 'ayrinti', (R, st) => {
    const tO = rel(st, 'F05@sonra');
    R.cam(960, 540, 1.0 + st.lt * .02);
    R.gok(-600, -400, 2600, 1500, [[0, '#3A2E3E'], [1, '#2A2230']], { firca: 1.3 });
    // el
    R.g.save(); R.g.translate(1000, 720); R.g.scale(30, 30); R.g.fillStyle = R.KARA; FIG.uzuv(R.g, [12, 9], [1, 1], 5, 4); R.g.beginPath(); R.g.ellipse(0, 0, 3.6, 2.6, .3, 0, TAU); R.g.fill(); R.g.restore();
    R.yika(g => g.ellipse(940, 500, 150, 190, 0, 0, TAU), '#B48A3A', { kay: 0, firca: .5 });
    R.yika(g => g.ellipse(940, 500, 138, 178, 0, 0, TAU), '#C9D6E4', { kay: 0 });
    R.g.save(); R.g.beginPath(); R.g.ellipse(940, 500, 136, 176, 0, 0, TAU); R.g.clip();
    R.yika(g => { g.moveTo(800, 690); g.quadraticCurveTo(940, 540, 1080, 690); g.closePath(); }, '#7A3A4A', { kay: 0 });   // elbise
    R.yika(g => g.rect(920, 520, 40, 60), '#EAC8A8', { kay: 0, firca: .3 });                                            // boyun
    R.yika(g => g.ellipse(945, 470, 44, 56, 0, 0, TAU), '#F0D2B4', { kay: 0, firca: .3 });                               // yüz (sağa dönük)
    R.yika(g => { g.moveTo(900, 470); g.quadraticCurveTo(900, 400, 950, 404); g.quadraticCurveTo(995, 410, 990, 440); g.quadraticCurveTo(960, 430, 930, 450); g.quadraticCurveTo(915, 480, 912, 500); g.closePath(); g.ellipse(902, 430, 24, 22, 0, 0, TAU); }, '#3A2418', { kay: 0, firca: .3 });   // toplu saç
    R.nokta(965, 466, 4, '#2A1A10'); R.cizgi([[958, 500], [972, 500]], 3, { renk: '#9A4A4A' });                                    // göz, dudak
    R.g.restore();
    const kar = E.io3(clamp((st.lt - tO) / 1.5));
    if (kar > 0) R.yika(g => g.ellipse(940, 500, 150, 190, 0, 0, TAU), `rgba(40,20,20,${kar * .6})`, { kay: 0, firca: 0 });
  }, { fener: st => ({ isik: { x: 940, y: 500, r: 460, sic: [1, .9, .76] }, kadraj: { tip: 'daire', x: 960, y: 520, r: 430, yum: 40 }, parlak: 1 - .35 * E.io3(clamp((st.lt - (A('F05@sonra') - st.at)) / 1.5)) }) });
  // F06: (üçüncü tekil) buzulda kulübe: Victor anlar (yakın, ışık Victor'a döner)
  sahne('F06a', 'F06', 'kulube', 'yakin', (R, st) => {
    R.cam(640, 700, 1.6);
    R.gok(-600, -400, 2600, 1500, [[0, '#7A5A40'], [1, '#54402E']], { firca: 1.3 });
    DK.ates(R, 960, 880, 200, { t: st.t });
    FIG.kisi(R, 560, 990, 450, { tip: 'victor', f: 1, bacak: 'otur', govde: .3 + E.io3(clamp(st.lt / 2)) * .2, bas: .4, kolO: [1.6, 1.6], kenar: 'rgba(255,200,130,.9)' });
  }, { fener: { isik: { x: 900, y: 520, r: 460, sic: [1, .86, .6] }, kadraj: { tip: 'daire', x: 900, y: 520, r: 430, yum: 40 } } });
  // F07: "bana bir eş yap": yaratık yanındaki boşluğu gösterir (orta)
  sahne('F07a', 'F07', 'buzul', 'orta', (R, st) => {
    R.cam(1000, 600, 1.3);
    BUZUL(R, st);
    FIG.kisi(R, 640, 1000, 520, { tip: 'victor', f: 1, kolO: [.2, .5] });
    const k = E.io3(clamp((st.lt - rel(st, 'F07@eş')) / 1));
    FIG.kisi(R, 1160, 1000, 600, { tip: 'yaratik', f: -1, kolA: [lerp(.1, .9, k), lerp(.3, .6, k)], kolO: [.6, 1.3], goz: 1 });
    if (k > 0) R.yika(g => g.ellipse(1400, 760, 90 * k, 230 * k, 0, 0, TAU), `rgba(255,250,240,${.5 * k})`, { kay: 0, firca: 0 });
  }, { fener: { isik: { x: 1100, y: 520, r: 640, sic: [.96, .96, 1] }, kadraj: KARE } });
  // F08–F09: Orkney: ıssız kulübe, lamba; masada örtülü yarım beden; pencerede yüz; Victor örtüyü yere atar
  window.ADA_IC = (R, st) => {
    R.gok(-600, -400, 2600, 1500, [[0, '#7E7266'], [1, '#5A5048']], { firca: 1.3 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#3E3630', { firca: 1 });
    DK.pencere(R, 1500, 360, 300, 400, { gece: '#5A6E96' });
    R.kara(g => { g.rect(420, 700, 820, 28); g.rect(450, 720, 24, 260); g.rect(1190, 720, 24, 260); });
  };
  sahne('F08a', 'F08', 'ada', 'genis', (R, st) => {
    R.cam(1100 - st.lt * 20, 560, 1.0);
    R.gok(-600, -400, 2600, 700, [[0, '#4A5878'], [1, '#8A96AE']], { firca: 1.2 });
    DK.gol(R, -600, 2600, 700, 1400, '#4A5E7E', '#26344E', { t: st.t, n: 20, yx: 400 });
    R.kara(g => { g.moveTo(700, 1400); g.lineTo(800, 740); g.quadraticCurveTo(1100, 640, 1500, 700); g.lineTo(1700, 1400); g.closePath(); });
    R.kara(g => { g.rect(1080, 560, 240, 150); g.moveTo(1060, 560); g.lineTo(1200, 470); g.lineTo(1340, 560); g.closePath(); });
    R.isikli(g => g.rect(1180, 610, 40, 50), '#F2C27A');
  }, { fener: { isik: { x: 1000, y: 520, r: 760, sic: [.96, .96, 1] }, kadraj: KARE },
    over: (ctx, st) => { etiket(ctx, 'ORKNEY ADALARI', 960, 160, st.lt - .4, st.d - .3); } });
  sahne('F09a', 'F09', 'ada', 'orta', (R, st) => {
    const tY = rel(st, 'F09@yüzü'), tP = rel(st, 'F09@parçaladı');
    R.cam(1000, 560, 1.05);
    ADA_IC(R, st);
    const at = E.io3(clamp((st.lt - tP) / .8));
    R.yika(g => { g.moveTo(450 + at * 300, 700 + at * 220); g.quadraticCurveTo(700, 660 + at * 200, 900 + at * 100, 676 + at * 200); g.lineTo(1000 + at * 100, 704 + at * 200); g.lineTo(450 + at * 300, 704 + at * 220); g.closePath(); }, '#CFC6B0', { firca: .8 });
    FIG.kisi(R, 880, 990, 480, { tip: 'victor', f: 1, govde: lerp(.35, -.05, at), kolO: [lerp(1.4, 2.2, at), lerp(.6, .3, at)], kolA: [lerp(1.2, .4, at), .6] });
    const yz = E.io3(clamp((st.lt - tY + .4) / .6));
    if (yz > 0) { R.g.save(); R.g.beginPath(); R.g.rect(1350, 160, 300, 400); R.g.clip(); FIG.kisi(R, 1470, 900 - yz * 30, 560, { tip: 'yaratik', f: -1, goz: 1 }); R.g.restore(); }
    DK.mum(R, 1100, 700, 120, { t: st.t });
  }, { fener: { isik: { x: 1000, y: 480, r: 640, sic: [1, .88, .66] }, kadraj: KARE } });
  // F10: pencerede tehdit (yakın): "düğün gecende"
  sahne('F10a', 'F10', 'ada', 'yakin', (R, st) => {
    R.cam(1500, 380, 2.0);
    ADA_IC(R, st);
    R.g.save(); R.g.beginPath(); R.g.rect(1350, 160, 300, 400); R.g.clip(); FIG.kisi(R, 1470, 870, 560, { tip: 'yaratik', f: -1, goz: 1, bas: -.05, kenar: 'rgba(220,230,255,.8)' }); R.g.restore();
  }, { fener: { isik: { x: 960, y: 480, r: 440, sic: [.92, .94, 1] }, kadraj: { tip: 'daire', x: 960, y: 520, r: 430, yum: 40 }, parlak: .9 } });
  // F11: sözünü tuttu: üç mum birer birer söner (ölümler gösterilmez)
  sahne('F11a', 'F11', 'mumlar', 'ayrinti', (R, st) => {
    const t0 = rel(st, 'F11@sevdiklerini');
    R.cam(960, 600, 1.0);
    R.gok(-600, -400, 2600, 1500, [[0, '#3A2E2A'], [1, '#2A2220']], { firca: 1.3 });
    R.kara(g => g.rect(300, 760, 1320, 30));
    for (let i = 0; i < 3; i++) { const yan = 1 - clamp((st.lt - t0 - i * .9) / .25); DK.mum(R, 640 + i * 320, 760, 220, { t: st.t + i, yan }); }
  }, { fener: st => ({ isik: { x: 960, y: 560, r: 640, sic: [1, .86, .62] }, kadraj: { tip: 'oval', x: 960, y: 560, w: 1400, h: 860, yum: 40 }, parlak: 1 - .55 * clamp((st.lt - (A('F11@sevdiklerini') - st.at)) / 2.6) }) });
})();
