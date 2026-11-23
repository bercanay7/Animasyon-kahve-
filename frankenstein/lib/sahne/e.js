// E: IV. Kör adam (E01–E10): görmeyen kabul eder, görenler kovar. Tek sıcak daireyi paylaşırlar; kapı açılınca ışık sertleşir. Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  const KARE = { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 };
  sahne('E00k', 'E01-1.4', 'kart', 'kart', (R, st) => { R.cam(960, 540, 1); SET.kart(R, st, 'IV', 'KÖR ADAM', 'Seni görmeyen biri seni sever mi?'); },
    { fener: { isik: { x: 960, y: 480, r: 900 }, kadraj: { tip: 'oval', x: 960, y: 480, w: 1500, h: 860, yum: 30 } }, tr: { type: 'iris', dur: 1.2 } });
  // E01: üçü yürüyüşe çıkar (sağa), ihtiyar kapıda; yaratık kapıya gelir
  sahne('E01a', 'E01+2.2', 'kapi', 'genis', (R, st) => {
    R.cam(960, 560, 1.0);
    R.gok(-600, -400, 2600, 900, [[0, '#9EBE92'], [1, '#D8E4BC']], { firca: 1.2 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#6E9A5A', { firca: 1 });
    R.kara(g => { g.rect(500, 440, 900, 460); g.moveTo(460, 440); g.lineTo(950, 200); g.lineTo(1440, 440); g.closePath(); });
    R.yika(g => g.rect(820, 640, 140, 260), '#6A4A30', { kay: 0 });
    const g = HAREKET.yuruyus({ tip: 'yuru', tur: 1.1 });
    const y = HAREKET.yuruyusYolu(g, { t0: 0, t1: 6, x0: 1200, olcek: 3.6, go: () => 1 })(st.lt);
    ['genc', 'kiz'].forEach((tp, i) => FIG.kisi(R, y.x + 400 + i * 120, 900, 300, { tip: tp, f: 1, bacak: y.poz, kolO: [Math.sin(TAU * y.faz) * .3, .3] }));
    const k = HAREKET.yuruyusYolu(g, { t0: 0, t1: 6, x0: -200, olcek: 4.6, go: t => HAREKET.rampa(t, .8, 1.2) * (1 - HAREKET.rampa(t, 2.6, 3)) })(st.lt);
    FIG.kisi(R, k.x, 910, 470, { tip: 'yaratik', f: 1, bacak: k.poz, govde: .1, pel: .3, kolO: [st.lt > rel(st, 'E01@kapıyı') ? 1.1 + Math.sin(st.lt * 14) * .08 : .2, st.lt > rel(st, 'E01@kapıyı') ? 1.6 : .2] });
  }, { fener: { isik: { x: 900, y: 560, r: 760, sic: [1, .97, .9] }, kadraj: KARE } });
  // E02–E03: ihtiyar ve yaratık ateşin iki yanında; tek sıcak daire (ışık ikisini kapsar)
  sahne('E02a', 'E02', 'kulube', 'orta', (R, st) => {
    R.cam(960, 600, 1.05 + st.lt * .01);
    R.gok(-600, -400, 2600, 1500, [[0, '#C0905A'], [1, '#8E6640']], { firca: 1.3 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#5A4232', { firca: 1 });
    DK.ates(R, 960, 880, 180, { t: st.t });
    FIG.kisi(R, 640, 990, 440, { tip: 'ihtiyar', f: 1, bacak: 'otur', bas: -.15, kolO: [.8 + Math.sin(st.lt * 1.3) * .1, 1.1] });
    FIG.kisi(R, 1300, 990, 600, { tip: 'yaratik', f: -1, bacak: 'otur', govde: .2, bas: .1, kolO: [.7, 1.4], kolA: [.6, 1.5], goz: 1 });
  }, { fener: { isik: { x: 960, y: 560, r: 640, sic: [1, .86, .6] }, kadraj: { tip: 'oval', x: 960, y: 560, w: 1500, h: 900, yum: 40 } },
    over: (ctx, st) => { quote(ctx, 'Ben körüm, yüzünü göremem; ama sözlerinde bir şey var.', 960, 170, st.lt - rel(st, 'E02@ben'), { px: 64, maxW: 1400, panel: .6 }); } });
  sahne('E03a', 'E03', 'kulube', 'yakin', (R, st) => {
    R.cam(1260, 520, 1.9 + st.lt * .02);
    R.gok(-600, -400, 2600, 1500, [[0, '#C0905A'], [1, '#8E6640']], { firca: 1.3 });
    DK.ates(R, 960, 880, 180, { t: st.t });
    FIG.kisi(R, 1300, 990, 600, { tip: 'yaratik', f: -1, bacak: 'otur', govde: .2, bas: .0, kolO: [.7, 1.4], kolA: [.6, 1.5], goz: 1, kenar: 'rgba(255,200,130,.9)' });
  }, { fener: { isik: { x: 1100, y: 520, r: 460, sic: [1, .86, .6] }, kadraj: { tip: 'daire', x: 1000, y: 520, r: 440, yum: 40 } } });
  // E04: eller: yaratık ihtiyarın elini tutar (ayrıntı)
  sahne('E04a', 'E04', 'kulube', 'ayrinti', (R, st) => {
    const k = E.io3(clamp((st.lt - rel(st, 'E04@elini') + .3) / .8));
    R.cam(960, 560, 1.0);
    R.gok(-600, -400, 2600, 1500, [[0, '#C0905A'], [1, '#8E6640']], { firca: 1.3 });
    // iki kol ve el, yakın: ihtiyarın kısa eli (soldan, avuç yukarı) ve yaratığın uzun parmaklı eli (sağdan) üstüne kapanır
    const el = (x, y, sc, f, uzun, kap) => { const g = R.g; g.save(); g.translate(x, y); g.scale(f * sc, sc); g.fillStyle = R.KARA;
      FIG.uzuv(g, [-26, 3], [-4, 0], 6.4, 5.2);                                         // ön kol (kol ağzıyla)
      g.beginPath(); g.ellipse(0, 0, 4.2, 2.6, 0, 0, TAU); g.fill();                    // avuç
      for (let i = 0; i < 4; i++) FIG.uzuv(g, [2.6, -1.4 + i * 1.1], [uzun ? 9.5 : 6.6, -2.4 + i * 1.6 + kap * (2 + i * .5)], 1.1, .8);
      FIG.uzuv(g, [0, -2], [2.6, -4.6], 1.3, 1);                                         // başparmak
      g.restore(); };
    el(820, 600, 16, 1, false, 0);
    el(lerp(1500, 1010, k), lerp(520, 578, k), 16, -1, true, k);
    DK.ates(R, 1500, 980, 160, { t: st.t });
  }, { fener: { isik: { x: 960, y: 560, r: 560, sic: [1, .86, .6] }, kadraj: { tip: 'oval', x: 960, y: 560, w: 1300, h: 820, yum: 40 } } });
  // E05: kapı açılır, ışık sertleşir; kız düşer, oğul sopa kaldırır (darbe gösterilmez)
  sahne('E05a', 'E05', 'kulube', 'genis', (R, st) => {
    const tK = rel(st, 'E05@bayıldı'), tO = rel(st, 'E05@kopardı'), tV = rel(st, 'E05@vurdu');
    R.cam(960, 560, .95);
    R.gok(-600, -400, 2600, 1500, [[0, '#D8C0A0'], [1, '#B09070']], { firca: 1.3 });
    R.isikli(g => g.rect(160, 260, 260, 640), '#FFF6E0');   // açılan kapı (gün ışığı)
    R.yika(g => g.rect(-600, 880, 3200, 600), '#6A5040', { firca: 1 });
    const d = E.io3(clamp((st.lt - tK) / .6));
    FIG.kisi(R, 320, 900, 380, { tip: 'kiz', f: 1, govde: -d * .6, bas: -d * .4, kolO: [d * .8, .4] });
    FIG.kisi(R, 780, 990, 420, { tip: 'ihtiyar', f: 1, bacak: 'otur', bas: -.2, kolO: [.9, .8] });
    const ko = E.io3(clamp((st.lt - tO) / .6));
    FIG.kisi(R, lerp(980, 1300, ko), 1000, 640, { tip: 'yaratik', f: -1, bacak: ko > .5 ? 'cok' : 'diz', govde: .3 + ko * .2, kolO: [1.4 - ko, .8], goz: 1 });
    const v = clamp((st.lt - tV + .6) / .6);
    FIG.kisi(R, lerp(520, 880, clamp((st.lt - tO + .5) / .8)), 900, 420, { tip: 'genc', f: 1, govde: .15, kolO: [lerp(.4, 2.4, v), lerp(.6, .9, v)], kolA: [.3, .5],
      el: { on: (R2, e) => FIG.uzuv(R2.g, e.e, [e.e[0] + Math.sin(e.a) * 26, e.e[1] + Math.cos(e.a) * 26], 2, 1.6) } });
  }, { fener: { isik: { x: 760, y: 520, r: 760, sic: [1, 1, .96] }, kadraj: KARE, parlak: 1.2 } });
  // E06: yerde, yumruk sıkılır ama kalkmaz (yakın)
  sahne('E06a', 'E06', 'kulube', 'yakin', (R, st) => {
    const tK = rel(st, 'E06@kaldırmadım');
    R.cam(1000, 700, 1.4);
    R.gok(-600, -400, 2600, 1500, [[0, '#B09070'], [1, '#8A6A50']], { firca: 1.3 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#5A4232', { firca: 1 });
    const kalk = st.lt < tK ? E.io3(clamp(st.lt / 1.4)) * .5 : .5 * (1 - E.io3(clamp((st.lt - tK) / .7)));
    FIG.kisi(R, 1000, 900, 560, { tip: 'yaratik', f: 1, bacak: 'diz', govde: .45, bas: .5, kolO: [lerp(.5, 2.1, kalk), lerp(.3, 1.3, kalk)], kolA: [.6, .3], goz: 1 });
  }, { fener: { isik: { x: 960, y: 700, r: 460, sic: [1, .95, .86] }, kadraj: { tip: 'daire', x: 960, y: 620, r: 440, yum: 40 }, parlak: .9 } });
  // E07: boş kulübe, kapı açık sallanır (sabah, soğuk)
  sahne('E07a', 'E07', 'kapi', 'genis', (R, st) => {
    R.cam(960, 560, 1.15 + st.lt * .02);
    R.gok(-600, -400, 2600, 900, [[0, '#9AA4AE'], [1, '#C6CCD0']], { firca: 1.2 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#7C8670', { firca: 1 });
    R.kara(g => { g.rect(500, 440, 900, 460); g.moveTo(460, 440); g.lineTo(950, 200); g.lineTo(1440, 440); g.closePath(); });
    const a = .5 + Math.sin(st.lt * 1.6) * .15;
    R.yika(g => g.rect(820, 640, 140, 260), '#2A2420', { kay: 0 });
    R.kara(g => { g.moveTo(960, 640); g.lineTo(960 + 140 * a, 660); g.lineTo(960 + 140 * a, 880); g.lineTo(960, 900); g.closePath(); });
  }, { fener: { isik: { x: 960, y: 560, r: 640, sic: [.95, .96, 1] }, kadraj: KARE, parlak: .9 } });
  // E08: gece: kulübe yanar; yaratık siluet olarak izler
  sahne('E08a', 'E08', 'kapi', 'orta', (R, st) => {
    R.cam(960, 560, 1.0);
    R.gok(-600, -400, 2600, 900, [[0, '#3A2A3A'], [1, '#8A4A30']], { firca: 1.2 });
    R.yika(g => g.rect(-600, 880, 3200, 600), '#2A2020', { firca: 1 });
    R.kara(g => { g.rect(500, 440, 900, 460); g.moveTo(460, 440); g.lineTo(950, 200); g.lineTo(1440, 440); g.closePath(); });
    for (let i = 0; i < 3; i++) R.yika(g => g.ellipse(700 + i * 300 + Math.sin(st.t * .4 + i) * 40, 200 - i * 40 - (st.t * 20 % 60), 260, 120, 0, 0, TAU), 'rgba(60,40,40,.7)', { kay: 0 });
    DK.ates(R, 760, 640, 460, { t: st.t }); DK.ates(R, 1180, 560, 360, { t: st.t + 2 });
    FIG.kisi(R, 1640, 960, 520, { tip: 'yaratik', f: -1, govde: .05, kolO: [.1, .3], pel: Math.sin(st.lt * 3) * .5 });
  }, { fener: { isik: { x: 900, y: 500, r: 760, sic: [1, .8, .56] }, kadraj: KARE, parlak: 1.05 } });
  // E09: nehir: kız düşer; yaratık atlar, kıyıya taşır, başında diz çöker
  sahne('E09a', 'E09', 'nehir', 'genis', (R, st) => {
    const tA = rel(st, 'E09@atladım'), tK = rel(st, 'E09@kıyıya'), tU = rel(st, 'E09@uğraştım');
    R.cam(960, 560, 1.0);
    R.gok(-600, -400, 2600, 700, [[0, '#9CB894'], [1, '#D2DEB4']], { firca: 1.2 });
    R.yika(g => { g.moveTo(-600, 640); g.lineTo(2600, 600); g.lineTo(2600, 1500); g.lineTo(-600, 1500); g.closePath(); }, '#5E8296', { firca: 1 });
    for (let i = 0; i < 10; i++) { const y = 660 + i * 40, x = ((st.lt * 120 + i * 230) % 2400) - 400; R.kazi([[x, y], [x + 120, y]], 3, 'rgba(235,245,250,.5)'); }
    R.yika(g => { g.moveTo(-600, 880); g.quadraticCurveTo(300, 840, 760, 880); g.lineTo(760, 1500); g.lineTo(-600, 1500); g.closePath(); }, '#8EA676', { firca: 1 });   // sol kıyı (açık: üstünde yatan kız görünür)
    for (const x of [-500, -260]) DK.kayin(R, x, 900, 520, { sal: Math.sin(st.t * .5) });
    if (st.lt < tA) { FIG.kisi(R, 900, 720, 320, { tip: 'kiz', f: 1, govde: -.9, kolO: [2.2, .6], kolA: [2.4, .5] }); }
    const k = E.io3(clamp((st.lt - tK) / 1.2));
    if (st.lt >= tA) {
      const x = lerp(1000, 420, k), y = lerp(760, 880, k);
      FIG.kisi(R, x, y, 560, { tip: 'yaratik', f: -1, bacak: st.lt > tU ? 'diz' : 'dur', govde: st.lt > tU ? .6 : .15, kolO: [1.2, 1.0], goz: 1 });
      if (st.lt > tU) FIG.yatan(R, x - 300, 880, 300, { f: 1, kadin: 1 });
    }
  }, { fener: { isik: { x: 760, y: 560, r: 760, sic: [1, .97, .9] }, kadraj: KARE } });
  // E10: adam tüfek kaldırır; namlu alevi; yaratık omzunu tutarak düşer; ışık kararır
  sahne('E10a', 'E10', 'nehir', 'orta', (R, st) => {
    const tA = rel(st, 'E10@ateş');
    R.cam(980, 600, 1.2);
    R.gok(-600, -400, 2600, 920, [[0, '#9CB894'], [1, '#D2DEB4']], { firca: 1.2 });
    R.yika(g => g.rect(-600, 900, 3200, 600), '#5A6E4A', { firca: 1 });
    const kalk = E.io3(clamp((st.lt - tA + 1.2) / .8));
    FIG.kisi(R, 1500, 900, 440, { tip: 'koylu', f: -1, govde: -.05, kolO: [lerp(.3, 1.45, kalk), lerp(.4, .25, kalk)], kolA: [lerp(.2, 1.3, kalk), lerp(.3, .7, kalk)],
      el: { on: (R2, e) => FIG.uzuv(R2.g, [e.e[0] - Math.sin(e.a) * 8, e.e[1] - Math.cos(e.a) * 8], [e.e[0] + Math.sin(e.a) * 30, e.e[1] + Math.cos(e.a) * 30], 2.2, 1.6) } });
    if (st.lt > tA && st.lt < tA + .12) R.isikli(g => g.arc(1320, 640, 40, 0, TAU), '#FFF4C0');
    const d = E.io3(clamp((st.lt - tA) / .9));
    FIG.kisi(R, 640, 900, 600, { tip: 'yaratik', f: 1, bacak: d > .5 ? 'diz' : 'dur', govde: d * .5, bas: d * .3, kolO: [lerp(.3, .9, d), lerp(.4, 2.0, d)], goz: 1 });
  }, { fener: st => ({ isik: { x: 960, y: 560, r: 700, sic: [1, .97, .9] }, kadraj: KARE, parlak: 1 - .6 * E.io3(clamp((st.lt - (A('E10@iyiliğimin') - st.at)) / 2.5)) }) });
})();
