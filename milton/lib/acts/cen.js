// cen grubu (CEN: cennet): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Açık anahtar: kâğıt beyazı kütleler, ışık merkezine göre eş merkezli tarama, %15–25 koyu çapa.
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const cen_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));

// ═════════ P019 (C02): melek safları arasında başmelek (açık tariflerin üslup karesi) ═════════
function cen_c02(t, o = {}) {
  const L = { x: 1520, y: 110 };
  cen_gok(L, { r0: 130, v: .62, mid: .86, kama: [{ a: PI * .8, w: .045, len: 1500 }, { a: PI * .6, w: .03, len: 900 }] });
  // ordunun arkasındaki bulut duvarı: üstü ışıklı yumrular, gövdesi aşağı doğru koyulaşır (safların zemini ve karenin koyu çapası)
  cen_bulut({ x: 1470, y: 440, w: 1300, h: 130, seed: 31, L, sh: 1, n: 10, len: 3.4, cuts: .7, base: false });
  // saflar: uzak mızrak ormanı + üç üst üste binen sıra (ışığa doğru küçülür)
  cen_saflar([{ mass: true, y: 590, h: 8, x0: 930, x1: 1990, v: .93, seed: 4, spearAng: () => .02 }], { t, L });
  cen_saflar([{ y: 640, h: 10, x0: 900, x1: 1990, n: 30, facing: -1, seed: 6, sh: .14, dy: .5 }], { t, L });
  cen_saflar([{ y: 730, h: 15, x0: 880, x1: 1980, n: 19, facing: -1, seed: 7, dy: .5 }], { t, L });
  cen_saflar([{ y: 860, h: 23, x0: 930, x1: 1960, n: 11, facing: -1, seed: 8, dy: .4 }], { t, L });
  // önde ışıklı bulut sırtı: ön sıranın ayaklarını örter; altı koyu
  cen_bulut({ x: 1450, y: 870, w: 1300, h: 80, seed: 34, L, sh: .9, n: 12, len: 2.5, by: .2 });
  // başmeleğin terası (sol) ve kendisi: sol yarının taralı göğü önünde
  cen_bulut({ x: 450, y: 920, w: 1200, h: 150, seed: 24, L, sh: .9, n: 8, len: 1.6, by: .1 });
  cen_basmelek({ x: 640, y: 560, h: 78, facing: -1, L, t, lum: 1, head: .2, twist: .32, armN: [-.08, .3], armF: [.2, 1.3], wingRot: -.05 });
  // ön plan: koyu bulut kenarı (çapa)
  cen_bulut({ x: 700, y: 1110, w: 2400, h: 120, seed: 25, L, sh: 1, n: 12, len: 2, by: -.2 });
}
plan('P019', (ctx, st) => {
  const cam = camLerp({ cx: 1010, cy: 540, z: 1.06 }, { cx: 910, cy: 540, z: 1.06 }, st.p, E.io2);
  levha(ctx, cam, () => cen_c02(st.t), [.8, 0, 1]);
}, { tr: { type: 'fade', dur: .8 } });
