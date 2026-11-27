// SALON seti: uzun bir galeri salonu, tek kaçış noktalı (Louvre, Goupil şubesi, Bağımsızlar, Brüksel, 1905 müzesi, bugünkü müze).
// Göz 1.6 m, ufuk y = 540, dikey görüş 40° (ODA ile aynı ekr). Tavanda ışıklık (gri gün ışığı). Duvarlarda çerçeveler (iki yoğunluk).
// Çerçevedeki resimler belirsiz gri lekeler: hangi tablonun asıldığı iddia edilmez. Çerçeve yuvarlak değil (halka); tuval sırtı gösterilmez (kasnak artısı = haç).
import { W, H, hsh } from './film_t.js';
import { nesne } from './nesne.js';
import { tabloCiz } from './film_t.js';
const PI = Math.PI, ODAK = 540 / Math.tan(20 * PI / 180);
export const ekr = (x, y, z) => [960 + x / -z * ODAK, 540 + (1.6 - y) / -z * ODAK];
const P = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
const lin = (st, x0, y0, x1, y1) => c => { const g = c.createLinearGradient(x0, y0, x1, y1); for (const [k, col] of st) g.addColorStop(k, col); return g; };
const GX = 4.5, GY = 7, Z0 = -1.2, Z1 = -46;
const VP = { radial: [960, 540] };
function mimari(R) {
  const q = (a, b, c, d) => P([a, b, c, d]);
  // tavan ve ışıklık
  R.fill(q(ekr(-GX, GY, Z0), ekr(GX, GY, Z0), ekr(GX, GY, Z1), ekr(-GX, GY, Z1)), lin([[0, '#5a544c'], [1, '#8a8478']], 0, 0, 0, 540), { dir: 0, maxR: 12, type: 1, len: 2.4, wid: .5, hgt: .4, group: 'tavan', jit: .05 });
  R.fill(q(ekr(-2.2, GY, Z0), ekr(2.2, GY, Z0), ekr(2.2, GY, Z1), ekr(-2.2, GY, Z1)), lin([[0, '#c8c4b8'], [1, '#e2ded2']], 0, 0, 0, 520), { dir: VP, maxR: 10, type: 1, len: 2.2, wid: .5, hgt: .25, group: 'isiklik', jit: .04 });
  for (let z = -2; z > Z1; z -= 3) R.line(c => { const a = ekr(-2.2, GY, z), b = ekr(2.2, GY, z); c.moveTo(...a); c.lineTo(...b); }, '#6a645a', Math.max(1.5, 14 / -z * 3), { dir: 0, maxR: 2, type: 1, group: 'kiris', jit: .03 });
  // yan duvarlar: ışıklığa yakın üst açık, alta doğru koyulaşır
  for (const s of [-1, 1]) R.fill(q(ekr(s * GX, GY, Z0), ekr(s * GX, GY, Z1), ekr(s * GX, 0, Z1), ekr(s * GX, 0, Z0)), lin([[0, '#9a9488'], [.6, '#6e685e'], [1, '#3e3a34']], 0, -200, 0, 1100), { dir: VP, maxR: 16, type: 1, len: 2.6, wid: .5, hgt: .35, group: 'duvar' + s, jit: .06 });
  // korniş ve süpürgelik çizgileri (kaçış noktasına)
  for (const s of [-1, 1]) for (const [y, w] of [[5.2, 10], [.25, 14]]) R.line(c => { c.moveTo(...ekr(s * GX, y, Z0)); c.lineTo(...ekr(s * GX, y, Z1)); }, '#2e2a26', w, { dir: VP, maxR: 3, type: 1, group: 'kornis', jit: .04 });
  // arka duvar ve kapı aralığı (aydınlık: salon sürüp gider)
  R.fill(q(ekr(-GX, GY, Z1), ekr(GX, GY, Z1), ekr(GX, 0, Z1), ekr(-GX, 0, Z1)), '#7a7468', { dir: 0, maxR: 4, type: 1, group: 'arka', jit: .05 });
  R.fill(q(ekr(-1.2, 4.2, Z1), ekr(1.2, 4.2, Z1), ekr(1.2, 0, Z1), ekr(-1.2, 0, Z1)), '#c4beb0', { dir: 90, maxR: 3, type: 1, group: 'kapi', jit: .04 });
  // döşeme: parke, kaçış noktasına uzanan tahta çizgileri; ışıklığın yansıması ortada
  R.fill(q(ekr(-GX, 0, Z0), ekr(GX, 0, Z0), ekr(GX, 0, Z1), ekr(-GX, 0, Z1)), lin([[0, '#3a332c'], [.5, '#5a5248'], [1, '#6e665a']], 0, 1080, 0, 560), { dir: VP, maxR: 14, type: 1, len: 3, wid: .45, hgt: .4, group: 'zemin', jit: .06 });
  for (let x = -GX; x <= GX; x += .45) R.line(c => { c.moveTo(...ekr(x, 0, Z0)); c.lineTo(...ekr(x, 0, Z1)); }, 'rgba(30,26,22,.35)', 2, { dir: VP, maxR: 2, type: 1, group: 'parke' + (Math.round(x / .45) % 3 + 3) % 3, jit: .04 });
  R.fill(q(ekr(-1.6, 0, -3), ekr(1.6, 0, -3), ekr(1.2, 0, Z1), ekr(-1.2, 0, Z1)), lin([[0, 'rgba(160,152,138,.0)'], [.5, 'rgba(170,162,148,.45)'], [1, 'rgba(180,172,158,.2)']], 0, 1000, 0, 560), { dir: VP, maxR: 8, type: 1, group: 'yansima', jit: .04, hgt: .2 });
}
// çerçeveler: (s yan, z merkez, y alt, gen, yuk); yoğunluk: dolu (Louvre: iki sıra, sık) | seyrek (sergi: tek sıra, aralıklı)
export function cerceveListesi(tur) {
  const L = [];
  if (tur === 'dolu') for (const s of [-1, 1]) for (let z = -3, i = 0; z > Z1 + 2; i++) { const gen = 1.6 + 1.6 * hsh(i, s, 1); L.push({ s, z: z - gen / 2, y: 1.1 + .3 * hsh(i, s, 2), gen, yuk: 1.2 + 1.2 * hsh(i, s, 3) });
      if (hsh(i, s, 4) < .7) L.push({ s, z: z - gen / 2 + (hsh(i, s, 5) - .5) * .4, y: 3.3 + .2 * hsh(i, s, 6), gen: gen * .8, yuk: .9 + .8 * hsh(i, s, 7) }); z -= gen + .5; }
  else for (const s of [-1, 1]) for (let z = -4, i = 0; z > Z1 + 2; i++) { const gen = 1.0 + .7 * hsh(i, s, 8); L.push({ s, z: z - gen / 2, y: 1.35, gen, yuk: .8 + .5 * hsh(i, s, 9) }); z -= gen + 2.6; }
  return L;
}
function cerceveCiz(L) {
  return R => L.forEach((f, i) => {
    const x = f.s * (GX - .03), a = ekr(x, f.y + f.yuk, f.z + f.gen / 2), b = ekr(x, f.y + f.yuk, f.z - f.gen / 2), c = ekr(x, f.y, f.z - f.gen / 2), d = ekr(x, f.y, f.z + f.gen / 2);
    R.fill(P([a, b, c, d]), '#2a2420', { dir: VP, maxR: 4, type: 1, hgt: .9, group: 'cer' + (i % 6), jit: .06 });
    const k = .08, ia = ekr(x, f.y + f.yuk - k, f.z + f.gen / 2 - k), ib = ekr(x, f.y + f.yuk - k, f.z - f.gen / 2 + k), ic = ekr(x, f.y + k, f.z - f.gen / 2 + k), id = ekr(x, f.y + k, f.z + f.gen / 2 - k);
    const t1 = 70 + 90 * hsh(i, 11), t2 = 50 + 80 * hsh(i, 12);   // belirsiz resim: iki tonlu gri leke
    R.fill(P([ia, ib, ic, id]), lin([[0, `rgb(${t1},${t1 - 4},${t1 - 10})`], [1, `rgb(${t2},${t2 - 3},${t2 - 8})`]], ia[0], ia[1], ic[0], ic[1]), { dir: 'edge', maxR: 5, type: 1, hgt: .6, group: 'res' + (i % 6), jit: .1, aj: .8 });
  });
}
// yan duvara perspektifle basılmış tablo (dikey şeritler): s yan (-1 sol), z0 > z1 derinlik, y0–y1 yükseklik; çerçeve koyu
export function tabloDuvar(img, s, z0, z1, y0, y1, o = {}) {
  return R => {
    const x = s * (GX - .04), N = 80, kc = .1, Q = (a, b, c, d) => q => { q.moveTo(...a); q.lineTo(...b); q.lineTo(...c); q.lineTo(...d); q.closePath(); };
    if (!o.cercevesiz) R.fill(Q(ekr(x, y1 + kc, z0 + kc), ekr(x, y1 + kc, z1 - kc), ekr(x, y0 - kc, z1 - kc), ekr(x, y0 - kc, z0 + kc)), '#2a2420', { dir: 'edge', maxR: 3, type: 1, hgt: .9, group: 'dcer', jit: .05 });
    R.fill(Q(ekr(x, y1, z0), ekr(x, y1, z1), ekr(x, y0, z1), ekr(x, y0, z0)), '#000', { maxR: o.maxR ?? 6, type: 1, len: 1.6, wid: .7, hgt: .55, group: 'dtablo' + (o.grup || ''), jit: .03, aj: .25, detail: .8 });
    const c = R.ref.ctx; c.save(); c.beginPath(); Q(ekr(x, y1, z0), ekr(x, y1, z1), ekr(x, y0, z1), ekr(x, y0, z0))(c); c.clip();
    for (let i = 0; i < N; i++) { const za = z0 + (z1 - z0) * i / N, zb = z0 + (z1 - z0) * (i + 1) / N, [xa, ya0] = ekr(x, y1, za), [, ya1] = ekr(x, y0, za), [xb] = ekr(x, y1, zb);
      const u = s < 0 ? i / N : 1 - (i + 1) / N; c.drawImage(img, u * img.width, 0, img.width / N + 1, img.height, Math.min(xa, xb), ya0, Math.abs(xb - xa) + 1, ya1 - ya0); }
    c.restore();
  };
}
export const SALON = { ekr, GX, GY, Z0, Z1 };
export function salonKur(M, IMG = {}) {
  const [ax, ay] = ekr(-1.6, 4.4, -45.8), [bx, by] = ekr(1.6, 1.4, -45.8);
  M.tanimla('salon', {
    zemin: [.08, .07, .06], kamera: () => ({ x: W / 2, y: H / 2, z: 1 }),
    katmanlar: [
      { ad: 'mimari', d: .72, ciz: mimari, R: [24, 12, 6, 3, 1.6], T: 10 },
      { ad: 'dolu', d: .72, ciz: cerceveCiz(cerceveListesi('dolu')), R: [12, 6, 3, 1.6], T: 9, alfa: (t, du) => (du && du.duvar === 'dolu' ? 1 : 0) },
      { ad: 'seyrek', d: .72, ciz: cerceveCiz(cerceveListesi('seyrek')), R: [12, 6, 3, 1.6], T: 9, alfa: (t, du) => (du && du.duvar === 'seyrek' ? 1 : 0) },
      ...(IMG.badem ? [{ ad: 'arkaTablo', d: .72, ciz: tabloCiz(IMG.badem, ax, ay, bx - ax, by - ay, { maxR: 2 }), R: [4, 2.4, 1.4], T: 8, olcek: 1, alfa: (t, du) => (du && du.arkaTablo ? 1 : 0) }] : []),
      ...(IMG.irisler ? [(() => { const [x0, y0] = ekr(-1.3, 2.7, -8), [x1, y1] = ekr(1.3, .7, -8), k = 16;   // E04: salonun ortasında bölme duvar, çerçeveli İrisler
        return { ad: 'iris', d: .72, ciz: R => { const P_ = (a, b, c, d) => q => { q.moveTo(a, b); q.lineTo(c, b); q.lineTo(c, d); q.lineTo(a, d); q.closePath(); };
          const [bx0, by0] = ekr(-1.9, 3.3, -8.05), [bx1, by1] = ekr(1.9, 0, -8.05);
          R.fill(P_(bx0, by0, bx1, by1), '#8a8478', { dir: 90, maxR: 8, type: 1, group: 'bolme', jit: .05 });
          R.fill(P_(x0 - k, y0 - k, x1 + k, y1 + k), '#2a2420', { dir: 'edge', maxR: 3, type: 1, hgt: .9, group: 'ircer', jit: .05 });
          tabloCiz(IMG.irisler, x0, y0, x1 - x0, y1 - y0, { maxR: 5, grup: 'iristablo' })(R); }, R: [10, 5, 2.6, 1.5], T: 8, olcek: .75, alfa: (t, du) => (du && du.iris ? 1 : 0) }; })()] : []),
      ...(IMG.badem ? [{ ad: 'bademDuvar', d: .72, ciz: tabloDuvar(IMG.badem, -1, -9.6, -14.2, 1.2, 4.8), R: [12, 6, 3, 1.6], T: 8, olcek: .75, alfa: (t, du) => (du && du.bademDuvar ? 1 : 0) }] : []),
      // H05 (1905 sergisi): yakın çerçevelerin yüzüne gerçek tablolar (Saint-Rémy, Auvers, Arles; adlandırılmaz, 1905 listesi iddia edilmez); renk örtüyle açılır
      ...(() => { const ks = ['selviler', 'remy1', 'auvers1', 'irisler', 'remy2', 'sari_ev', 'remy3', 'firtina', 'remy5', 'yildizli'].filter(k => IMG[k]); if (!ks.length) return [];
        const L = cerceveListesi('dolu').filter(f => f.z > -17).slice(0, 10);
        return [{ ad: 'g1905', d: .72, ciz: R => L.forEach((f, i) => { const kc = .08; tabloDuvar(IMG[ks[i % ks.length]], f.s, f.z + f.gen / 2 - kc, f.z - f.gen / 2 + kc, f.y + kc, f.y + f.yuk - kc, { maxR: 3, cercevesiz: true, grup: i })(R); }),
          R: [8, 4, 2, 1.3], T: 8, olcek: .75, alfa: (t, du) => (du && du.g1905 ? 1 : 0) }]; })(),
      { ad: 'nesne', d: .72, canli: (t, S, c, x, du) => { if (du && du.nesneler) for (const it of du.nesneler(t)) nesne(S, it); }, kap: 2000, wet: .15, run: 0 },
      { ad: 'figur', d: .72, canli: (t, S, c, x, du) => { if (du && du.figur) du.figur(t, S); }, kap: 16000, wet: .2, run: 0 },
      { ad: 'ust', d: .72, canli: (t, S, c, x, du) => { if (du && du.ust) du.ust(t, S); }, kap: 4000, wet: .2, run: 0 },
    ],
    bitir: (t, du) => ({ light: [0, -.8, .6], norm: 1.6, ground: [.08, .07, .06], expo: (du && du.expo) || 1.04, contrast: 1.06, vig: .38, spec: .1, shin: 24, weave: .06, lightCol: [.97, .97, 1],
      mono: 1, monoK: [.045, .04, .04], monoA: [.97, .94, .88] }),
  });
}
