// cen grubu (CEN: cennet): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Açık anahtar: kâğıt beyazı kütleler, ışık merkezine göre eş merkezli tarama, %15–25 koyu çapa.
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const cen_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));

// ═════════ P019 (C02): melek safları arasında başmelek (açık tariflerin üslup karesi) ═════════
function cen_c02(t, o = {}) {
  const L = { x: 1520, y: 120 };
  cen_gok(L, { r0: 130, v: .62, mid: .86, kama: [{ a: PI * .8, w: .045, len: 1500 }, { a: PI * .6, w: .03, len: 900 }] });
  // ordunun arkasındaki bulut duvarı: üstü ışıklı yumrular, gövdesi aşağı doğru koyulaşır (safların zemini ve karenin koyu çapası)
  cen_bulut({ x: 1480, y: 470, w: 1300, h: 150, seed: 31, L, sh: .9, n: 9, by: .1, len: 1.6, cuts: .6 });
  // saflar: üç sıra + uzak mızrak ormanı; her sıra ince bir bulut sırtında
  cen_saflar([{ mass: true, y: 560, h: 7, x0: 960, x1: 1990, v: .9, seed: 4, spearAng: () => .02 }], { t, L });
  cen_saflar([{ y: 600, h: 9, x0: 930, x1: 1990, n: 32, facing: -1, seed: 6, sh: .12, dy: .5 }], { t, L });
  cen_bulut({ x: 1460, y: 618, w: 1180, h: 40, seed: 32, L, sh: .7, n: 12, cuts: 0, by: .3 });
  cen_saflar([{ y: 690, h: 14, x0: 900, x1: 1970, n: 20, facing: -1, seed: 7, dy: .5 }], { t, L });
  cen_bulut({ x: 1440, y: 712, w: 1250, h: 56, seed: 33, L, sh: .8, n: 11, cuts: .4, by: .3 });
  cen_saflar([{ y: 820, h: 22, x0: 960, x1: 1940, n: 11, facing: -1, seed: 8, dy: .4 }], { t, L });
  cen_bulut({ x: 1450, y: 848, w: 1350, h: 90, seed: 34, L, sh: .9, n: 9, by: .25 });
  // başmeleğin terası (sol) ve kendisi: sol yarının koyu göğü önünde
  cen_bulut({ x: 470, y: 930, w: 1250, h: 170, seed: 24, L, sh: .9, n: 7, by: .05 });
  cen_basmelek({ x: 640, y: 570, h: 78, facing: -1, L, t, lum: 1, head: .2, twist: .32, armN: [-.08, .3], armF: [.2, 1.3], wingRot: -.05 });
  // ön plan: koyu bulut kenarı (çapa) ve sağ altta kadrajı kesen yakın saf
  cen_saflar([{ y: 1150, h: 36, x0: 1380, x1: 1990, n: 4, facing: -1, seed: 9 }], { t, L });
  cen_bulut({ x: 900, y: 1140, w: 2700, h: 140, seed: 25, L, sh: 1, n: 10, by: -.25 });
}
plan('P019', (ctx, st) => {
  const cam = camLerp({ cx: 1010, cy: 540, z: 1.06 }, { cx: 910, cy: 540, z: 1.06 }, st.p, E.io2);
  levha(ctx, cam, () => cen_c02(st.t), [.8, 0, 1]);
}, { tr: { type: 'fade', dur: .8 } });
