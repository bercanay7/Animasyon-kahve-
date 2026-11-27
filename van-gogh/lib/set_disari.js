// Dış setler: TARLA (Auvers kırı, park yolu; kurye/lib/tablo_ciz.js resmi, grisaille) ve TREN (gece ovası, geçen tren).
// Hassasiyet: tarlada mezar, haç, kilise yok; alçak taş duvar düz ve sürekli (sıra hâlinde dik taş yok); telgraf direği yok (ters L + sarkan tel = darağacı).
import { BRUSH, DAB, KNIFE } from '../../araclar/tablo/impasto.js';
import { W, H, hsh, ikiser, clamp, sm } from './film_t.js';
const P = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
const lin = (st, x0, y0, x1, y1) => c => { const g = c.createLinearGradient(x0, y0, x1, y1); for (const [k, col] of st) g.addColorStop(k, col); return g; };
const T = () => window.TABLO;
// rüzgârda başaklar (ön plan): tohumlu öbek; dalga soldan sağa geçer
const BASAK = []; for (let i = 0; i < 900; i++) { const y = 760 + 320 * Math.pow(hsh(i, 2), .7), k = (y - 700) / 380; BASAK.push({ x: hsh(i, 1) * 2000 - 40, y, L: 14 + 70 * k, w: 2 + 4.5 * k, f: hsh(i, 3) * 6, c: [.62 + .2 * hsh(i, 4), .52 + .16 * hsh(i, 4), .3] }); }
BASAK.sort((a, b) => a.y - b.y);
function basaklar(t, S, guc = 1) {
  for (const b of BASAK) { const dl = .5 + .5 * Math.sin(b.x * .004 - t * 1.4), dal = guc * (.12 * Math.sin(b.x * .006 + b.y * .004 - t * 1.7) + .05 * Math.sin(b.x * .03 - t * 3 + b.f) + .22 * dl);
    const a = -Math.PI / 2 + dal; S.push({ x: b.x + Math.cos(a) * b.L / 2, y: b.y + Math.sin(a) * b.L / 2, ang: a, len: b.L, wid: b.w, c: b.c.map(v => v * .6), c2: b.c.map(v => Math.min(1, v * (1 + .3 * dl))), seed: b.f * 100, type: BRUSH, hgt: .5, bend: dal * .8, taper: .7 }); }
}
// alçak taş duvar (H07): sürekli, yatay; üstünde sarmaşık lekeleri
function duvar(R) {
  const y0 = 760, y1 = 830;
  R.fill(P([[-60, y0 + 12], [2000, y0 - 18], [2000, y1 - 10], [-60, y1 + 16]]), lin([[0, '#8a8274'], [1, '#4a443c']], 0, y0, 0, y1), { dir: 0, maxR: 6, type: 1, len: 1.6, wid: .8, hgt: .8, group: 'duvar', jit: .1 });
  // sarmaşık lekesi yok: sıra hâlinde yuvarlak koyu lekeler mezar taşı okunuyordu (H07); duvarın üst kenarı tek açık çizgi
  R.line(c => { c.moveTo(-60, y0 + 12); c.lineTo(2000, y0 - 18); }, '#a49c8c', 5, { dir: 0, maxR: 2, type: 1, group: 'duvarust', jit: .05 });
}
export function tarlaKur(M) {
  const TB = T();
  M.tanimla('tarla', {
    zemin: [.1, .09, .08], kamera: () => ({ x: W / 2, y: H / 2, z: 1 }),
    katmanlar: [
      { ad: 'gok', d: 0, ciz: TB.gok, R: [30, 15, 7.5, 3.6, 1.8], T: 10 },
      { ad: 'daglar', d: .2, ciz: TB.daglar },
      { ad: 'tarla', d: .45, ciz: R => TB.tarla(R, [], { golge: false }) },
      { ad: 'tgolge', d: .45, ciz: TB.tarlaGolge, alfa: (t, du) => (du && du.agac === false ? 0 : 1) },
      { ad: 'agac', d: .5, ciz: TB.agac, R: [20, 10, 5, 2.6, 1.5], T: 10, alfa: (t, du) => (du && du.agac === false ? 0 : 1) },
      { ad: 'duvar', d: .7, ciz: duvar, R: [12, 6, 3, 1.6], T: 9, alfa: (t, du) => (du && du.duvar ? 1 : 0) },
      { ad: 'figur', d: .6, canli: (t, S, c, x, du) => { if (du && du.figur) du.figur(t, S); }, kap: 16000, wet: .2, run: 0 },
      { ad: 'basak', d: .9, canli: (t, S, c, x, du) => basaklar(ikiser(t), S, du && du.ruzgar != null ? du.ruzgar : 1), kap: 1024 },
      { ad: 'on', d: 1, ciz: TB.on },
    ],
    bitir: (t, du) => ({ light: [-.5, -.55, .7], norm: 1.7, ground: [.1, .09, .08], expo: du && du.expo ? du.expo(t) : 1.02, contrast: 1.05, vig: .32, spec: .1, shin: 24, weave: .06, lightCol: [1, .95, .86],
      mono: 1, monoK: [.05, .045, .045], monoA: [.96, .94, .9] }),
  });
}
// ---------------- TREN ----------------
const UF = 640;
// bulut: alt kenarı düz, üstü kabarık öbekler (tek elips "uçan daire" okunuyordu); gölgeli alt, aydınlık tepe
function bulutlar(R, alt, ust, sd) {
  for (let i = 0; i < 6; i++) { const x0 = 120 + i * 330 + 90 * hsh(i, sd), y0 = 200 + 170 * hsh(i, sd + 1), gen = 260 + 160 * hsh(i, sd + 2), n = 6;
    R.fill(c => { c.moveTo(x0 - gen / 2, y0); for (let k = 0; k <= n; k++) { const x = x0 - gen / 2 + gen * k / n, r = 30 + 40 * hsh(i, k + sd) * Math.sin(Math.PI * k / n) + 10; c.arc(x, y0 - r * .3, r, Math.PI, 0); } c.lineTo(x0 + gen / 2, y0 + 8); c.lineTo(x0 - gen / 2, y0 + 8); c.closePath(); },
      lin([[0, ust], [1, alt]], 0, y0 - 90, 0, y0 + 8), { dir: 0, maxR: 8, type: 1, len: 2.6, wid: .55, group: 'bulut' + (i % 3), jit: .06, hgt: .35 }); }
}
function gece(R) {
  R.fill(P([[-60, -60], [1980, -60], [1980, UF + 20], [-60, UF + 20]]), lin([[0, '#141820'], [.7, '#2a2e38'], [1, '#4a4a4c']], 0, 0, 0, UF), { dir: 0, maxR: 26, type: 1, len: 3, wid: .5, hgt: .3, group: 'gok', jit: .05 });
  bulutlar(R, '#363840', '#4a4c54', 3);
  R.fill(c => c.ellipse(1500, 150, 14, 14, 0, 0, 7), '#d6d2c6', { dir: 0, maxR: 3, type: 1, len: 2.4, wid: .6, group: 'ay', jit: .03 });
}
function gunduz(R) {
  R.fill(P([[-60, -60], [1980, -60], [1980, UF + 20], [-60, UF + 20]]), lin([[0, '#8a9098'], [.7, '#c2c0b8'], [1, '#dcd6c6']], 0, 0, 0, UF), { dir: 0, maxR: 26, type: 1, len: 3, wid: .5, hgt: .3, group: 'gok', jit: .05 });
  bulutlar(R, '#9a9890', '#ece8de', 7);
}
function ova(R, gun) {
  const tep = [[-60, UF + 30]]; for (let x = -60; x <= 1980; x += 20) tep.push([x, UF - 30 * Math.max(0, Math.sin(x * .004 + 1)) - 12 * hsh(Math.floor(x / 20), 4)]); tep.push([1980, UF + 30]);
  R.fill(P(tep), gun ? '#8a8676' : '#1e2026', { dir: 0, maxR: 6, type: 1, len: 2, wid: .6, group: 'tepe', jit: .05 });
  R.fill(P([[-60, UF], [1980, UF], [1980, 1140], [-60, 1140]]), lin(gun ? [[0, '#a29c86'], [1, '#5a5444']] : [[0, '#24262a'], [1, '#0c0c0e']], 0, UF, 0, 1100), { dir: 0, maxR: 16, type: 1, len: 3, wid: .5, hgt: .4, group: 'ova', jit: .06 });
  // demiryolu seddi: alçak, yatay; raylar ince açık çizgi
  R.fill(P([[-60, 770], [1980, 770], [1980, 800], [-60, 800]]), gun ? '#6e6858' : '#16161a', { dir: 0, maxR: 4, type: 1, group: 'sed', jit: .04 });
  R.line(c => { c.moveTo(-60, 772); c.lineTo(1980, 772); }, gun ? '#c8c2b0' : '#5a5a5e', 2.5, { dir: 0, maxR: 2, type: 1, group: 'ray', jit: .03 });
}
// tren: lokomotif + 5 vagon siluet, aydınlık pencereler (sıcak), buhar; x: lokomotifin burnu; yon: +1 sağa
function tren(t, S, x0, yon, gun, k = 1.6) {
  const y = 772, kar = gun ? [.3, .28, .26] : [.05, .05, .06], pen = gun ? [.8, .78, .72] : [1, .86, .58];
  // v3: gündüz açık gövde, açık pencere, üç vagon, tekerlek, görünür duman (boş ovada kapkara uzun tren sürgün treni okunuyordu)
  const parca = [{ L: 150 * k, h: 70 * k, lok: true }, ...Array.from({ length: gun ? 3 : 5 }, () => ({ L: 200 * k, h: 78 * k }))];
  let x = x0;
  parca.forEach((p, i) => { const xm = x - yon * p.L / 2;
    S.push({ x: xm, y: y - p.h / 2 - 8, ang: 0, len: p.L - 10, wid: p.h, c: kar, c2: kar, seed: i, type: KNIFE, alpha: 1, hgt: .4 });
    for (const q of [-.3, .3]) S.push({ x: xm + q * p.L, y: y - 6, ang: 0, len: 20 * k, wid: 20 * k, c: [.08, .07, .07], seed: i * 3 + q, type: DAB, alpha: 1, hgt: .4 });   // tekerlek (düz disk, halka yok)
    if (p.lok) { S.push({ x: x - yon * 30 * k, y: y - p.h - 22 * k, ang: 0, len: 22 * k, wid: 34 * k, c: kar, seed: 50, type: KNIFE, alpha: 1, hgt: .4 });   // baca
      for (let q = 0; q < 8; q++) { const a = (t * .9 + q * .13) % 1; S.push({ x: x - yon * 30 * k - yon * a * 420, y: y - p.h - 60 * k - a * 110 + 10 * Math.sin(q + t), ang: 0, len: 60 + 180 * a, wid: 44 + 90 * a, c: gun ? [.62, .6, .58] : [.4, .4, .42], seed: 60 + q, type: DAB, alpha: (gun ? .7 : .5) * (1 - a), hgt: 0 }); } }
    else for (let q = 0; q < 4; q++) S.push({ x: xm + (q - 1.5) * 42 * k, y: y - p.h / 2 - 12 * k, ang: Math.PI / 2, len: 30 * k, wid: 22 * k, c: pen, c2: pen.map(v => v * .9), seed: i * 10 + q, type: KNIFE, alpha: gun ? .8 : 1, hgt: .2 });
    x -= yon * (p.L + 8 * k); });
  if (!gun) S.push({ x: x0 - yon * 600, y: y + 40, ang: 0, len: 1300, wid: 50, c: [1, .85, .55], seed: 99, type: DAB, alpha: .06, hgt: 0 });   // pencerelerin yere düşen ışığı
}
export function trenKur(M) {
  M.tanimla('tren', {
    zemin: [.06, .06, .07], kamera: () => ({ x: W / 2, y: H / 2, z: 1 }),
    katmanlar: [
      { ad: 'gece', d: 0, ciz: gece, R: [30, 15, 7.5, 3.6, 1.8], T: 10, alfa: (t, du) => 1 - (du && du.gun ? du.gun(t) : 0) },
      { ad: 'gunduz', d: 0, ciz: gunduz, R: [30, 15, 7.5, 3.6, 1.8], T: 10, alfa: (t, du) => (du && du.gun ? du.gun(t) : 0) },
      { ad: 'ovaG', d: .4, ciz: R => ova(R, false), R: [20, 10, 5, 2.6, 1.5], T: 10, alfa: (t, du) => 1 - (du && du.gun ? du.gun(t) : 0) },
      { ad: 'ovaD', d: .4, ciz: R => ova(R, true), R: [20, 10, 5, 2.6, 1.5], T: 10, alfa: (t, du) => (du && du.gun ? du.gun(t) : 0) },
      { ad: 'figur', d: .4, canli: (t, S, c, x, du) => { if (du && du.figur) du.figur(t, S); }, kap: 16000, wet: .2, run: 0 },
      { ad: 'tren', d: .4, canli: (t, S, c, x, du) => { if (du && du.tren) for (const [x0, yon] of du.tren(t)) tren(ikiser(t), S, x0, yon, du.gun ? du.gun(t) > .5 : false); }, kap: 400, wet: .1, run: 0 },
    ],
    bitir: (t, du) => { const g = du && du.gun ? du.gun(t) : 0; return { light: [-.4, -.6, .7], norm: 1.6, ground: [.06, .06, .07], expo: .98 + .1 * g, contrast: 1.08, vig: .4 - .1 * g, spec: .1, shin: 24, weave: .06, lightCol: [1, .95, .86],
      mono: 1, monoK: [.04, .04, .045], monoA: [.96, .94, .9] }; },
  });
}
