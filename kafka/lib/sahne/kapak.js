// Kapaklar (1280×720'ye küçültülür). ?scene=kapakA|kapakB. Kurallar: tek odak (kırmızı elma), harf ≥ %18 (Bebas ≥ 290 px / 1080), sağ alt (rozet) boş.
// A ve B'nin vaadi filmin ilk saniyelerinde karşılanır: A = ilk kare (aralık kapı + elma), B = ikinci plan (kapıda aile, 4,5. sn).
'use strict';
var SCENES = window.SCENES || {}; window.SCENES = SCENES;
function kapakYazi(ctx, lines, x, y, px, col, align = 'left') { ctx.save(); baseT(ctx); ctx.font = `400 ${px}px "Bebas Neue"`; ctx.textAlign = align; ctx.textBaseline = 'alphabetic'; ctx.letterSpacing = '6px'; ctx.fillStyle = col; lines.forEach((l, i) => ctx.fillText(l, x, y + i * px * .92)); ctx.restore(); }
const kSt = (t, s) => ({ t, lt: t, p: 0, seed: s, d: 10 });
SCENES.kapakA = (ctx, t) => {
  kes(ctx, kSt(6, 3), { cx: 1010, cy: 560, z: 1.12 }, k => a1_kapiKaresi(k, { ac: 62, er: 70, ex: 1215, ey: 760 }), { tamKare: true });
  kapakYazi(ctx, ['ARTIK', 'O DEĞİL'], 70, 470, 300, KAGIT);
};
SCENES.kapakB = (ctx, t) => {
  kes(ctx, kSt(2, 5), { cx: 1430, cy: 470, z: 1.0 }, k => { a1_aileKapida(k, { bas: .4 }); O.elma(k, 815, 845, 52, { rot: -.3 }); }, { tamKare: true });
  kapakYazi(ctx, ['SEVGİ', 'KOŞULLU', 'MU?'], 1860, 250, 290, KAGIT, 'right');
};
