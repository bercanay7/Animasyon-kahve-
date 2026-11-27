// MASA seti: Theo'nun yazı masası tepeden (ayrıntı planları). Üst yarı masa yüzü, alt yarı açık alt çekmece.
// Işık sol üstten (lamba kadraj dışında; tepeden bakışta lamba tabanı halka okunur: hedef tahtası). Nesneler canlı katmanda (lib/nesne.js).
import { nesne } from './nesne.js';
import { W, H, hsh } from './film_t.js';
const P = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
const rad = (st, x, y, r) => c => { const g = c.createRadialGradient(x, y, 0, x, y, r); for (const [k, col] of st) g.addColorStop(k, col); return g; };
const lin = (st, x0, y0, x1, y1) => c => { const g = c.createLinearGradient(x0, y0, x1, y1); for (const [k, col] of st) g.addColorStop(k, col); return g; };
export const CEKMECE = { x0: 330, x1: 1590, y0: 640, y1: 1160 };   // çekmecenin iç tabanı (dünya)
export const ISIK = [520, 120];
function yuzey(R) {
  const [lx, ly] = ISIK;
  R.fill(P([[-80, -80], [W + 80, -80], [W + 80, 600], [-80, 600]]), rad([[0, '#9a8064'], [.35, '#6e5640'], [.75, '#3a2c22'], [1, '#1e1612']], lx, ly, 1500),
    { dir: 0, maxR: 16, type: 1, len: 3.2, wid: .45, hgt: .45, group: 'masa', jit: .07, aj: .06 });
  // ahşap damarı: seyrek, düzensiz, kesik; yer yer budak çizgisi (düzenli şerit oluklu sac okunuyordu)
  for (let i = 0; i < 14; i++) { const y = -30 + i * 46 + 30 * hsh(i), a = 6 + 10 * hsh(i, 2), x0 = -80 + 900 * hsh(i, 5), x1 = x0 + 500 + 1200 * hsh(i, 6);
    R.line(c => { c.moveTo(x0, y); for (let x = x0; x <= x1; x += 40) c.lineTo(x, y + a * Math.sin(x * .003 + i * 1.7) + 4 * Math.sin(x * .011 + i)); }, `rgba(24,16,11,${.12 + .14 * hsh(i, 3)})`, 1.5 + 3 * hsh(i, 4), { dir: 0, maxR: 3, type: 1, len: 3, wid: .5, group: 'damar' + (i % 4), jit: .06 }); }
  // masa kenarı (ön kayış) ve çekmecenin ön tahtası
  R.fill(P([[-80, 590], [W + 80, 590], [W + 80, 625], [-80, 625]]), '#24190f', { dir: 0, maxR: 4, type: 1, len: 3, wid: .5, hgt: .7, group: 'kenar', jit: .05 });
  R.fill(P([[-80, 625], [W + 80, 625], [W + 80, H + 80], [-80, H + 80]]), '#120d0a', { dir: 90, maxR: 8, type: 1, group: 'karanlik', jit: .05 });
}
// çekmecesiz planlar: masa yüzü bütün kareyi kaplar
function yuzeyTam(R) {
  const [lx, ly] = ISIK;
  R.fill(P([[-80, -80], [W + 80, -80], [W + 80, H + 80], [-80, H + 80]]), rad([[0, '#9a8064'], [.35, '#6e5640'], [.75, '#3a2c22'], [1, '#1e1612']], lx, ly + 200, 1600),
    { dir: 0, maxR: 16, type: 1, len: 3.2, wid: .45, hgt: .45, group: 'masa', jit: .07, aj: .06 });
  for (let i = 0; i < 24; i++) { const y = -30 + i * 48 + 30 * hsh(i, 9), a = 6 + 10 * hsh(i, 2), x0 = -80 + 900 * hsh(i, 5), x1 = x0 + 500 + 1200 * hsh(i, 6);
    R.line(c => { c.moveTo(x0, y); for (let x = x0; x <= x1; x += 40) c.lineTo(x, y + a * Math.sin(x * .003 + i * 1.7) + 4 * Math.sin(x * .011 + i)); }, `rgba(24,16,11,${.12 + .14 * hsh(i, 3)})`, 1.5 + 3 * hsh(i, 4), { dir: 0, maxR: 3, type: 1, len: 3, wid: .5, group: 'damar' + (i % 4), jit: .06 }); }
}
function cekmece(R) {
  const { x0, x1, y0, y1 } = CEKMECE, [lx] = ISIK;
  // yan duvarlar ve arka duvar (içe doğru koyulaşan)
  R.fill(P([[x0 - 40, 612], [x1 + 40, 612], [x1 + 40, H + 80], [x0 - 40, H + 80]]), '#3a2a1e', { dir: 90, maxR: 5, type: 1, len: 2.5, wid: .5, hgt: .6, group: 'cekyan', jit: .05 });
  R.fill(P([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]), lin([[0, '#5c4632'], [.5, '#4a3726'], [1, '#2e2219']], lx, y0, x1, y1), { dir: 0, maxR: 10, type: 1, len: 3, wid: .45, hgt: .4, group: 'cektaban', jit: .06, aj: .06 });
  R.fill(P([[x0, y0], [x1, y0], [x1 - 10, y0 + 26], [x0 + 10, y0 + 26]]), '#1c130d', { dir: 0, maxR: 4, type: 1, group: 'cekarka', jit: .05 });
  // çekmecenin ön tahtası (kadrajın altında kalın koyu kenar: çekmece olduğu okunur)
  R.fill(P([[x0 - 60, 1040], [x1 + 60, 1040], [x1 + 60, H + 80], [x0 - 60, H + 80]]), lin([[0, '#4a3524'], [1, '#22170f']], 0, 1040, 0, 1100), { dir: 0, maxR: 5, type: 1, len: 3, wid: .5, hgt: .8, group: 'cekon', jit: .05 });
  // tutamak (çekmecenin ön yüzü kadrajın altında; tutamak yok: yuvarlak tokmak tepeden halka okunur)
}
// MASA sahnesi: durum.nesneler(lt) → nesne listesi (çizim sırasıyla); durum.ust(lt, S): ek darbeler (toz, ışık)
export function masaKur(M) {
  M.tanimla('masa', {
    zemin: [.06, .05, .04],
    kamera: () => ({ x: W / 2, y: H / 2, z: 1 }),
    katmanlar: [
      { ad: 'yuzey', d: 0, ciz: yuzey, R: [26, 13, 6.5, 3.2, 1.7], T: 10, alfa: (t, du) => (du && du.cekmece === false ? 0 : 1) },
      { ad: 'yuzeyTam', d: 0, ciz: yuzeyTam, R: [26, 13, 6.5, 3.2, 1.7], T: 10, alfa: (t, du) => (du && du.cekmece === false ? 1 : 0) },
      { ad: 'cekmece', d: 0, ciz: cekmece, R: [20, 10, 5, 2.6, 1.5], T: 10, alfa: (t, du) => (du && du.cekmece === false ? 0 : 1) },
      { ad: 'nesne', d: 0, canli: (t, S, cam, c, du) => { if (du && du.nesneler) for (const it of du.nesneler(t)) nesne(S, it); if (du && du.ust) du.ust(t, S); }, kap: 6000, wet: .15, run: 0 },
    ],
    bitir: (t, du) => ({ light: [-.45, -.7, .65], norm: 1.8, ground: [.06, .05, .04], expo: (du && du.expo) || 1.05, contrast: 1.08, vig: .4, spec: .14, shin: 26, weave: .05, lightCol: [1, .92, .8],
      mono: 1, monoK: [.045, .04, .04], monoA: [.97, .94, .88] }),
  });
}
