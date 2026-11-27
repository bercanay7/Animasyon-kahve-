// ODA seti: Theo'nun Paris odası (lib/oda_ciz.js resmi; üslup kapısı oda.html'den). Işık: gece (lamba), sabah, kış.
// Şövalede Vincent'in tablosu darbe katmanı (renk örtüsüyle renkli). Theo ve öbür figürler Blender karelerinden (figurDarbe).
// durum: {isik: 'gece'|'sabah'|'kis'|'ogle', alev(t) 0..1, figur(t, S), nesneler(t), ust(t, S), tablo: 'ad' | null, tabloA(t)}
import { BRUSH, DAB } from '../../araclar/tablo/impasto.js';
import { nesne } from './nesne.js';
import { W, H, hsh, ikiser, tabloCiz } from './film_t.js';
const O = window.ODA;
export const TK = O.tabloKose();   // [x, y, w, h] şövaledeki tuval (ekran = dünya, d = .3 katmanı)
const PI2 = i => i * .7;
function alev(t, S, f0) {
  const [lx, ly] = O.LAMBA, f = (.85 + .15 * Math.sin(t * 9.1) * Math.sin(t * 3.7 + 1)) * f0; if (f0 <= .01) return;
  for (let i = 0; i < 4; i++) S.push({ x: lx, y: ly, ang: PI2(i), len: 120 + 90 * i, wid: 120 + 90 * i, c: [1, .9, .7], seed: i, type: DAB, alpha: .07 * f, hgt: 0 });
  S.push({ x: lx, y: ly + 4, ang: Math.PI / 2, len: 46 * (.4 + .6 * f0), wid: 26, c: [1, .97, .86], c2: [1, .86, .6], seed: 9, type: BRUSH, alpha: .95 * Math.min(1, f0 * 1.5), hgt: .05, taper: .5 });
  S.push({ x: lx, y: ly + 2, ang: Math.PI / 2 + .04 * Math.sin(t * 7), len: 14 * f0, wid: 7 * f, c: [1, 1, .95], seed: 11, type: BRUSH, alpha: f0, hgt: 0, taper: .8 });
}
function toz(t, S, k) { const [lx, ly] = O.LAMBA; if (k <= 0) return; for (let i = 0; i < 40; i++) { const a = hsh(i, 1) * 6.28, r = 40 + 300 * Math.sqrt(hsh(i, 2));
  const x = lx + Math.cos(a) * r + 20 * Math.sin(t * .3 + i), y = ly + Math.sin(a) * r * .8 - t * 6 + 12 * Math.sin(t * .5 + i * 2), yak = Math.max(0, 1 - Math.hypot(x - lx, y - ly) / 360);
  S.push({ x, y, ang: 0, len: 2.4, wid: 2, c: [1, .94, .8], seed: i, type: DAB, alpha: .5 * yak * k, hgt: 0 }); } }
const ISIK = {
  gece: { light: [.55, -.4, .7], expo: 1.02, lightCol: [1, .93, .82], vig: .42 },
  sabah: { light: [-.7, -.45, .6], expo: 1.12, lightCol: [.96, .97, 1], vig: .3 },
  ogle: { light: [-.5, -.7, .6], expo: 1.05, lightCol: [1, .98, .94], vig: .34 },
  kis: { light: [-.8, -.3, .55], expo: .98, lightCol: [.9, .94, 1], vig: .46 },
};
export function odaKur(M, IMG) {
  const tablolar = Object.keys(IMG).filter(k => k.startsWith('oda_'));
  M.tanimla('oda', {
    zemin: [.08, .07, .06],
    kamera: () => ({ x: W / 2, y: H / 2, z: 1 }),
    katmanlar: [
      { ad: 'duvar', d: 0, ciz: O.duvar, R: [30, 15, 7.5, 3.6, 1.8], T: 10 },
      { ad: 'pencere', d: .05, ciz: O.pencere, R: [20, 10, 5, 2.6, 1.5], T: 10, alfa: (t, du) => (du && du.isik && du.isik !== 'gece' ? 0 : 1) },
      { ad: 'pencereGun', d: .05, ciz: O.pencereGun, R: [20, 10, 5, 2.6, 1.5], T: 10, alfa: (t, du) => (du && du.isik && du.isik !== 'gece' ? 1 : 0) },
      { ad: 'esya', d: .3, ciz: O.esya, R: [20, 10, 5, 2.6, 1.5], T: 10 },
      ...tablolar.map(k => ({ ad: k, d: .3, ciz: tabloCiz(IMG[k], ...TK, { maxR: 6 }), R: [10, 5, 2.6, 1.5], T: 8, olcek: .75, alfa: (t, du) => (du && du.tablo === k ? (du.tabloA ? du.tabloA(t) : 1) : 0) })),
      { ad: 'alev', d: .3, canli: (t, S, c, x, du) => alev(ikiser(t), S, du && du.alev ? du.alev(t) : (du && du.isik && du.isik !== 'gece' ? .25 : 1)), kap: 16 },
      { ad: 'nesne', d: .3, canli: (t, S, c, x, du) => { if (du && du.nesneler) for (const it of du.nesneler(t)) nesne(S, it); }, kap: 4000, wet: .15, run: 0 },
      { ad: 'figur', d: .3, canli: (t, S, c, x, du) => { if (du && du.figur) du.figur(t, S); }, kap: 12000, wet: .2, run: 0 },
      { ad: 'toz', d: .3, canli: (t, S, c, x, du) => toz(ikiser(t), S, du && du.isik && du.isik !== 'gece' ? .4 : 1), kap: 64 },
      { ad: 'ust', d: .3, canli: (t, S, c, x, du) => { if (du && du.ust) du.ust(t, S); }, kap: 2000, wet: .15, run: 0 },
    ],
    bitir: (t, du) => ({ norm: 1.6, ground: [.08, .07, .06], sat: 1, contrast: 1.08, spec: .1, shin: 24, weave: .07, mono: 1, monoK: [.045, .04, .04], monoA: [.97, .94, .88],
      ...ISIK[(du && du.isik) || 'gece'] }),
  });
}
export { O as ODA };
