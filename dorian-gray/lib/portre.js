// Portre: impasto (Lemo-Opuscar, MIT; ../kapi/vendor) ile boyanan tek renkli istisna. ES modülü; window.PORTRE verir.
//   PORTRE.hazir: Promise
//   PORTRE.ciz(ctx, { M, durum, t, gecis: {dan, t0}, maske(mx), expo })
//     M: portre yerel (0..500 × 0..720) → ekran (1920×1080 cihaz pikseli) afin [a,b,c,d,e,f]
//     durum: 'G' | 'Z' | 'Y' | 'C' | 'I' (portre_ciz.js)
//     gecis: önceki durumdan yeniden boyama; t0 film zamanında başlar, darbeler değişen bölgeden dışa doğru belirir (süre durum başına sabit)
//     maske(mx): ekran koordinatında öndeki nesneleri tuvalden düşürür (mx.globalCompositeOperation zaten 'destination-out')
//     expo: pozlama (karanlık odada < 1)
import { Impasto, Strokes, hex } from '../kapi/vendor/impasto.js';
import { Ref, paintRef } from '../kapi/vendor/plate.js';

const PC = window.PORTRE_CIZ, W = 1920, H = 1080;
// yeniden boyama: merkez (yerel), yarıçap (bunun dışı hemen yerinde), süre (sn)
const BOYA = { G: { c: [258, 260], r: 1e9, sure: 2.6 }, Z: { c: [222, 330], r: 90, sure: 1.8 }, Y: { c: [250, 240], r: 230, sure: 3.0 }, C: { c: [250, 240], r: 260, sure: 3.0 }, I: { c: [258, 300], r: 110, sure: 2.0 } };
let E, gl, PL = {};
function levhaYap(durum) {
  const Rf = new Ref(PC.W, PC.H, 1.3);
  const R = { fill: (pf, c, p) => Rf.fill(pf, c, { seed: 1, ...p }), line: (pf, c, w, p) => Rf.line(pf, c, w, p || {}), text: (s, x, y, f, c, p) => Rf.text(s, x, y, f, c, p || {}) };
  PC.tuval(R, durum);
  const B = BOYA[durum];
  const app = (x, y, level) => { const d = Math.hypot(x - B.c[0], y - B.c[1]); if (d > B.r) return -100; return (d / Math.min(B.r, 330)) * B.sure * .8 + level * .06 + (((x * 13.1 + y * 7.7) % 1 + 1) % 1) * .12; };
  const st = paintRef(Rf, { R: [26, 13, 6.5, 3.2, 1.8], T: 10, seed: 11, app });
  return { b: E.batch(st.data()), tex: E.texture(Rf.ctx.canvas), n: st.n };
}
const mask = document.createElement('canvas'); mask.width = W; mask.height = H; const mx = mask.getContext('2d');
const POST = { expo: 1.04, sat: 1.02, contrast: 1.06, vig: 0, spec: .22, shin: 26, lightCol: [1, .95, .86], ground: [.16, .12, .09] };
function ciz(ctx, o) {
  const M = o.M, cam = { x: W / 2, y: H / 2, zoom: 1, rot: 0 }, t = o.t;
  E.begin(POST.ground);
  const hedef = PL[o.durum];
  if (o.gecis && o.gecis.dan && t < o.gecis.t0 + BOYA[o.durum].sure + .4) {
    const dan = PL[o.gecis.dan];
    E.under(dan.tex, PC.W, PC.H, { M, cam }); E.draw(dan.b, { M, cam, t: 10 });
    E.draw(hedef.b, { M, cam, t, appear: o.gecis.t0, appDur: .18 });
  } else { E.under(hedef.tex, PC.W, PC.H, { M, cam }); E.draw(hedef.b, { M, cam, t: 10 }); }
  E.finish({ ...POST, expo: (o.expo ?? 1) * POST.expo });
  // maske: tuval dörtgeni − öndeki nesneler
  mx.setTransform(1, 0, 0, 1, 0, 0); mx.globalCompositeOperation = 'source-over'; mx.clearRect(0, 0, W, H);
  mx.setTransform(M[0], M[1], M[2], M[3], M[4], M[5]); mx.fillStyle = '#fff'; mx.fillRect(PC.IN.x, PC.IN.y, PC.IN.w, PC.IN.h);
  mx.setTransform(1, 0, 0, 1, 0, 0);
  if (o.maske) { mx.save(); mx.globalCompositeOperation = 'destination-out'; mx.fillStyle = '#000'; o.maske(mx); mx.restore(); }
  mx.globalCompositeOperation = 'source-in'; mx.drawImage(gl, 0, 0); mx.globalCompositeOperation = 'source-over';
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(mask, 0, 0); ctx.restore();
}
window.PORTRE = {
  ciz, BOYA,
  hazir: (async () => {
    await document.fonts.load('italic 600 21px "Cormorant Garamond"', 'BASIL HALLWARD');
    gl = document.createElement('canvas'); E = new Impasto(gl, { W, H, ss: 2 });
    for (const d of Object.keys(PC.DUR)) PL[d] = levhaYap(d);
    window.PORTRE.darbe = Object.fromEntries(Object.entries(PL).map(([k, v]) => [k, v.n]));
    return true;
  })(),
};
