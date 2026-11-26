// Figür → fırça darbeleri (tablo motoru). Kaynak: saydam zeminli bir figür görüntüsü (Blender karesi ya da manken çizimi).
// İç: dik, iri darbeler (seyrek ızgara + titreşim). Kenar: biçimi saran kısa spatula darbeleri (iç darbelerden sonra basılır).
// Karşı ışık: yalnız güneşe bakan kenar, kırık altın darbe (her yanı saran parlak kenar "çıkartma" okunur).
// Belirlenimci: titreşim tohumu piksel konumundan ve çizim sırasından (cz).
import { KNIFE, BRUSH } from './impasto.js';
const PI = Math.PI;
const hsh = (a, b = 0, c = 0) => { const x = Math.sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453; return x - Math.floor(x); };

// Blender karelerini yükle: klasör/k_0000.png …; saydam olmayan bölge kırpılıp saklanır (bellek). Döner: dizi[kare] = {x0, y0, w, h, d} | null
export async function blenderKareleri(klasor, n, { W = 960, H = 540 } = {}) {
  const c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d', { willReadFrequently: true }); const out = [];
  for (let k = 0; k < n; k++) {
    const r = await fetch(`${klasor}/k_${String(k).padStart(4, '0')}.png`); if (!r.ok) { out.push(null); continue; }
    const im = await createImageBitmap(await r.blob()); x.clearRect(0, 0, W, H); x.drawImage(im, 0, 0);
    const d = x.getImageData(0, 0, W, H).data; let x0 = W, y0 = H, x1 = -1, y1 = -1;
    for (let y = 0; y < H; y++) for (let xx = 0; xx < W; xx++) if (d[(y * W + xx) * 4 + 3] > 20) { if (xx < x0) x0 = xx; if (xx > x1) x1 = xx; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    out.push(x1 < 0 ? null : { x0, y0, w: x1 - x0 + 1, h: y1 - y0 + 1, d: x.getImageData(x0, y0, x1 - x0 + 1, y1 - y0 + 1).data, W, H });
  }
  return out;
}
// kaynak arayüzü: {w, h, fig(x, y), renk(x, y), kutu: [x0, y0, x1, y1]}
export function blenderKaynak(BK) {
  return { w: BK.W, h: BK.H, kutu: [BK.x0 + 1, BK.y0 + 1, BK.x0 + BK.w - 2, BK.y0 + BK.h - 2],
    fig: (x, y) => x >= BK.x0 && y >= BK.y0 && x < BK.x0 + BK.w && y < BK.y0 + BK.h && BK.d[((y - BK.y0) * BK.w + x - BK.x0) * 4 + 3] > 140,
    renk: (x, y) => { const j = ((y - BK.y0) * BK.w + x - BK.x0) * 4; return [BK.d[j] / 255, BK.d[j + 1] / 255, BK.d[j + 2] / 255]; } };
}
// S: Strokes; o: {W (çıktı genişliği), gunes: [x, y] (ekran), hava: [r,g,b] (uzaklık rengi), havaK (0..1), cz (çizim sırası), kutu (kaynak pikseli; yoksa kaynağınki),
//   olcek (darbe boyu çarpanı), altin (kenar ışığı rengi), kenarEsik}
export function figurDarbe(S, src, o = {}) {
  const W = o.W || 1920, w = src.w, h = src.h, sc = W / w, cz = o.cz || 0, k = o.olcek || 1;
  const [gx, gy] = o.gunes || [W / 2, -1e4], hava = o.hava || [.36, .24, .3], hk = o.havaK ?? .14, altin = o.altin || [1, .72, .42];
  const [x0, y0, x1, y1] = o.kutu || src.kutu || [1, 1, w - 2, h - 2];
  const fig = src.fig, KEN = [], KIS = [];
  for (let y = Math.max(1, y0); y <= Math.min(h - 2, y1); y++) for (let x = Math.max(1, x0); x <= Math.min(w - 2, x1); x++) {
    if (!fig(x, y)) continue;
    const kenar = !(fig(x - 1, y) && fig(x + 1, y) && fig(x, y - 1) && fig(x, y + 1));
    let c = src.renk(x, y).map((v, i) => v + (hava[i] - v) * hk);
    const X = (x + .5 + (hsh(x, y, cz + 1) - .5) * .5) * sc, Y = (y + .5 + (hsh(x, y, cz + 2) - .5) * .5) * sc;
    if (!kenar) {
      if ((x + 2 * y + cz) % 3) continue;
      S.push({ x: X, y: Y, ang: PI / 2 + (hsh(x, y, cz) - .5) * .5, len: 4.6 * sc * k, wid: 2.4 * sc * k, c, c2: c.map(v => v * .9), seed: hsh(x, y, cz) * 999, type: BRUSH, hgt: .25 });
      continue;
    }
    let nx = (fig(x - 1, y) ? 1 : 0) - (fig(x + 1, y) ? 1 : 0), ny = (fig(x, y - 1) ? 1 : 0) - (fig(x, y + 1) ? 1 : 0);
    nx += ((fig(x - 1, y - 1) ? 1 : 0) + (fig(x - 1, y + 1) ? 1 : 0) - (fig(x + 1, y - 1) ? 1 : 0) - (fig(x + 1, y + 1) ? 1 : 0)) * .5;
    ny += ((fig(x - 1, y - 1) ? 1 : 0) + (fig(x + 1, y - 1) ? 1 : 0) - (fig(x - 1, y + 1) ? 1 : 0) - (fig(x + 1, y + 1) ? 1 : 0)) * .5;
    const nl = Math.hypot(nx, ny) || 1; nx /= nl; ny /= nl;
    const sx = gx - X, sy = gy - Y, sl = Math.hypot(sx, sy) || 1;
    const kenarIsik = Math.max(0, (nx * sx / sl + ny * sy / sl) - .35) / .65 * (hsh(x >> 1, y >> 1, 77) < .7 ? 1 : .25);
    const ta = Math.atan2(ny, nx) + PI / 2;
    KEN.push({ x: X - nx * .6 * sc, y: Y - ny * .6 * sc, ang: ta, len: 2.1 * sc * k, wid: 1.4 * sc * k, c: c.map((v, i) => v + (hava[i] * .6 - v) * .2), c2: c, seed: hsh(x, y, cz) * 999, type: KNIFE, hgt: .2 });
    if (kenarIsik > (o.kenarEsik ?? .12)) KIS.push({ x: X + nx * .15 * sc, y: Y + ny * .15 * sc, ang: ta, len: 4.4 * sc * k, wid: .8 * sc * k, c: altin, c2: altin.map(v => v * .85), seed: hsh(x, y, cz + 9) * 999, type: KNIFE, hgt: .15, alpha: Math.min(1, kenarIsik * 1.4) });
  }
  for (const q of KEN) S.push(q); for (const q of KIS) S.push(q);
}
