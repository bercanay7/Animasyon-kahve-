// Üslup kapısı: manzara + orta plan figür + yakın plan + 15 sn hareket (+ İstanbul gecesi). ?scene=ad&t=sn
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d'); cv.width = DW; cv.height = DH;
const Q = new URLSearchParams(location.search);
const CAMx = (cx, cy, z = 1) => ({ cx, cy, z });
function sahne(ctx, cam, fn, renk = 1, bg = [.05, 0, 0]) { LALE.sifirla(); levha(ctx, cam, fn, bg); LALE.boya(ctx, cam, renk); }
const SC = {
  // MANZARA: Haarlem dışı, lale tarlası, kanal evleri, değirmen; yavaş kayan kamera
  manzara(ctx, t) {
    const cam = CAMx(960 + t * 8, 540, 1.0);
    sahne(ctx, cam, () => {
      SET.gok({ gun: 1 });
      SET.degirmen(1560, 566, .7, t * .35);
      SET.kasaba(560, 1);
      SET.tarla({ y0: 566, t, sira: 7 });
    });
  },
  // ORTA PLAN: Alkmaar mezadı; mezatçı masada, saksıda tek renkli lale, kalabalık sırtı ve kalkan eller
  mezat(ctx, t) {
    const cam = CAMx(960, 560, 1.0);
    sahne(ctx, cam, () => {
      SET.meyhane({ isik: .8 });
      SET.masa(760, 640, 420);
      SET.saksi(970, 640, 1.0); LALE.ciz(970, 515, 1.15, { sap: 62, cesit: 'amiral', ac: .2 });
      SET.isik({ x: 970, y: 520, r1: 520, a: .85 });
      // mezatçı (masanın arkasında, ¾ profil, ışıkta) ve yanında kâtip
      INSAN.adam({ x: 1200, y: 900, h: 560, yon: -1, sapka: 'genis', yaka: 'duz', kenar: .55, kenarYan: -1, kolOn: { a: 1.5 + .25 * Math.sin(t * 1.4), b: .9 }, biyik: true, sakal: true });
      INSAN.adam({ x: 720, y: 880, h: 480, yon: 1, sapka: 'genis', yaka: 'duz', kenar: .45, kolOn: { a: .9, b: .9 } });
      // alıcılar: ön planda sırtı dönük, farklı derinlik ve boyda; kolları dirsekten kırık, avuç açık (selam okunmaz)
      const A = [[200, 1150, 700, 1], [520, 1200, 760, -1], [1440, 1190, 740, 1], [1760, 1150, 700, -1]];
      A.forEach(([x, y, h, yon], i) => { const up = Math.sin(t * 1.8 + i * 1.7) > .2;
        INSAN.adam({ x, y, h, yon, arka: true, sapka: 'genis', yaka: 'duz', kenar: .4, kenarYan: yon, giysi: 'pelerin', kolOn: up ? { a: 2.1, b: 1.0 } : { a: .25, b: .3 } }); });
    }, 1, [.1, 0, 0]);
  },
  // YAKIN: tek kırık lale (Semper Augustus); ışık
  yakin(ctx, t) {
    const cam = CAMx(960, 520, 1.0);
    sahne(ctx, cam, () => {
      GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.62), { th: .3, id: 0 });
      SET.isik({ x: 960, y: 430, r1: 900, a: .6 });
      LALE.ciz(960, 520, 3.6, { sap: 520, cesit: 'semper', ac: .32, egim: .03 * Math.sin(t * .8) });
    });
  },
  // 15 SN HAREKET: tarla gündüz → el boyaması iner (0–5 sn), değer artar (terazi), çöküş: renk söner (10–15 sn)
  hareket(ctx, t) {
    if (t < 7.5) {
      const cam = camLerp(CAMx(960, 520, 1), CAMx(1060, 700, 1.6), t / 7.5);
      const r = clamp(t / 2.5);
      sahne(ctx, cam, () => { SET.gok({ gun: 1 }); SET.kasaba(560, 1); SET.tarla({ y0: 566, t, sira: 7 }); }, r);
    } else {
      const u = t - 7.5, a = lerp(-.02, .16, E.io2(clamp(u / 3))), renk = 1 - E.io2(clamp((u - 4) / 3));
      sahne(ctx, CAMx(960, 560, 1), () => {
        GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.7), { th: 0, id: 10 });
        const [L, Rr] = SET.terazi(960, 1000, a);
        LALE.sogan(L[0], L[1] - 38, 1.2); LALE.ciz(L[0], L[1] - 120, 1, { sap: 40, cesit: 'semper', ac: .3 });
        SET.ev(Rr[0] - 110, Rr[1], 220, 170, { ton: .5, basamak: 3 });
      }, renk);
    }
  },
  // İSTANBUL GECESİ: Kâğıthane, köşk, servi, lale tarhı, kaplumbağa sırtında mum
  istanbul(ctx, t) {
    const cam = CAMx(960, 560, 1);
    sahne(ctx, cam, () => {
      GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.08), { th: -.05, id: 1 });
      SET.kosk(560, 640, 800, 300, { gece: true });
      for (const [x, h] of [[300, 520], [1500, 600], [1700, 480]]) SET.servi(x, 700, h);
      GR.fill(SET.R(-200, 700, 2400, 500), GR.tone(.12), { type: 'persp', y0: 700, D: 200, p0: 7, p1: 14, id: 8 });
      for (let r = 0; r < 3; r++) for (let x = 120; x < 1850; x += 110) LALE.ciz(x + r * 40, 800 + r * 90, .6 + r * .2, { tip: 'ist', sap: 60 + r * 20, cesit: r === 1 ? 'istSari' : 'ist', ac: .1 });
      for (let x = 160; x < 1850; x += 220) { SET.kandil(x, 760, t + x, 1.2); SET.isik({ x, y: 760, r1: 170, a: .6 }); }
      const kx = 400 + t * 40; SET.kaplumbaga(kx, 1010, 1.2, t); SET.isik({ x: kx, y: 900, r1: 220, a: .7 });
    }, 1, [.08, 0, 1]);
  },
};
window.renderFrame = t => { baseT(ctx); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H); SC[Q.get('scene') || 'manzara'](ctx, t); post(ctx, t); return cv; };
(async () => { try { await document.fonts.load('700 40px Cinzel'); buildTextures(); window.READY = true; if (Q.has('still')) renderFrame(+Q.get('t') || 0); } catch (e) { window.HATA = String(e.stack || e); } })();
