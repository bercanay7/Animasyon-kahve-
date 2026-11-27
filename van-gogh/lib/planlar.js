// Plan listesi (ölçek her plana yazılır; ardışık iki plan aynı ölçekte olmaz). Görsel ve figür yükleme, setlerin kurulumu.
import { W, H, A, S, Se, Wd, plan, sm, clamp, lerp, io, hsh, ikiser, mRect, mDaire, mTam } from './film_t.js';
import { figurDarbe, blenderKaynak, blenderKareleri } from '../../araclar/tablo/figur.js';
import { nesneMaske, RENK } from './nesne.js';
import { masaKur, CEKMECE } from './set_masa.js';
import { odaKur, ODA, TK } from './set_oda.js';
import { BRUSH, DAB, KNIFE } from '../../araclar/tablo/impasto.js';

// ---------- görseller (CC0 / kamu malı; araclar/ASSETS.md) ----------
const GORSEL = {
  oda_otoportre: 'gorsel/otoportre_hasir_sapka_1887_met436532.jpg',
  selvili_tarla: 'gorsel/selvili_bugday_tarlasi_1889_met436535.jpg',
};
export async function gorselYukle() {
  const o = {};
  for (const [k, f] of Object.entries(GORSEL)) { const r = await fetch(f); if (!r.ok) { console.log('görsel yok: ' + f); continue; } o[k] = await createImageBitmap(await r.blob()); }
  return o;
}
// ---------- figür klipleri (Blender, 15 kare/sn; blender/klip.js) ----------
const KLIP = { theo_oda: ['blender/kare_oda', 121] };
export async function figurYukle() { const o = {}; for (const [k, [d, n]] of Object.entries(KLIP)) o[k] = await blenderKareleri(d, n); return o; }
const kare = (BK, t) => BK[Math.max(0, Math.min(BK.length - 1, Math.round(ikiser(t) * 15)))];

export function setleriKur(M, IMG, FIG) { masaKur(M); odaKur(M, IMG); }

// ---------- yardımcılar ----------
const kamYol = (a, b, e = io) => u => { const k = e(clamp(u)); return { x: lerp(a[0], b[0], k), y: lerp(a[1], b[1], k), z: lerp(a[2], b[2], k) }; };
// tohumlu zarf yığını (çekmece): n zarf, üst üste, hafif dağınık; renk sarı (Vincent) ya da gri
function yigin(n, o = {}) {
  const L = [], cx = o.x ?? 960, cy = o.y ?? 860, dx = o.dx ?? 520, dy = o.dy ?? 200;
  for (let i = 0; i < n; i++) L.push({ tur: 'zarf', x: cx + (hsh(i, 1) - .5) * dx, y: cy + (hsh(i, 2) - .5) * dy - i * (o.kat ?? .25), w: o.w ?? 230, h: o.h ?? 140, rot: (hsh(i, 3) - .5) * (o.rot ?? .5), renk: o.renk || 'sari', yuz: hsh(i, 4) < .5 ? 'on' : 'arka', tohum: (o.tohum || 0) + i });
  return L;
}
// düşen zarf: t0'da yukarıdan iner, yığına oturur (gölge daralır)
function duser(it, t, t0, d = .6) { const u = clamp((t - t0) / d); if (u <= 0) return null; const k = 1 - io(u); return { ...it, y: it.y - 260 * k, rot: it.rot + .5 * k, kalk: k, w: it.w * (1 + .15 * k), h: it.h * (1 + .15 * k) }; }
// badem dalı (kapak B'nin vaadi): koyu dal darbeleri ve beş yapraklı beyaz çiçekler; büyüme u 0..1
function bademDali(S, x0, y0, aci, u, sd = 3, olc = 1) {
  // ana dal + iki yan sürgün; uç incelir; çiçekler beş taç yapraklı, beyazdan pembeye, ortası koyu (tablodaki gibi), tomurcuklar
  if (u <= 0) return;
  const dal = (x, y, a, n, k0, w0, sdd) => { const uc = []; for (let i = 0; i < n * clamp(u * 1.15 - k0); i++) { const L = (40 - i * 1.6) * olc; a += (hsh(sdd, i) - .5) * .32;
      const nx = x + Math.cos(a) * L, ny = y + Math.sin(a) * L, w = Math.max(2.5, (w0 - i * w0 / (n + 2)) * olc);
      S.push({ x: (x + nx) / 2, y: (y + ny) / 2, ang: a, len: L * 1.15, wid: w, c: [.2, .14, .11], c2: [.3, .22, .16], seed: sdd * 10 + i, type: BRUSH, alpha: 1, hgt: .7, taper: .15 });
      if (i % 2 === 1) uc.push([nx + Math.cos(a + (i % 4 ? 1.3 : -1.3)) * 16 * olc, ny + Math.sin(a + (i % 4 ? 1.3 : -1.3)) * 16 * olc, sdd * 50 + i, i / n]); x = nx; y = ny; }
    uc.push([x, y, sdd * 50 + 99, 1]); return { x, y, a, uc }; };
  const ana = dal(x0, y0, aci, 12, 0, 16, sd), c1 = [];
  const y1 = dal(x0 + Math.cos(aci) * 150 * olc, y0 + Math.sin(aci) * 150 * olc, aci + .7, 6, .3, 8, sd + 1), y2 = dal(x0 + Math.cos(aci) * 260 * olc, y0 + Math.sin(aci) * 260 * olc, aci - .8, 5, .45, 6, sd + 2);
  for (const [cx, cy, k, p] of [...ana.uc, ...y1.uc, ...y2.uc]) {
    const ac = clamp((u - .35 - p * .3) / .35); if (ac <= 0) continue; const r = (hsh(k, 1) < .3 ? 9 : 17) * olc * ac, tom = r < 10 * olc;
    if (tom) { S.push({ x: cx, y: cy, ang: hsh(k) * 6, len: r * 1.4, wid: r, c: [.93, .8, .78], c2: [.85, .62, .6], seed: k, type: DAB, alpha: 1, hgt: .5 }); continue; }
    for (let q = 0; q < 5; q++) { const t = q / 5 * Math.PI * 2 + hsh(k, 2) * 6; const pc = [.97, .95 - .04 * hsh(k, q), .92 - .06 * hsh(q, k)];
      S.push({ x: cx + Math.cos(t) * r * .62, y: cy + Math.sin(t) * r * .62, ang: t, len: r * 1.05, wid: r * .85, c: pc, c2: [.93, .86, .84], seed: k * 5 + q, type: BRUSH, alpha: 1, hgt: .55, taper: .4 }); }
    S.push({ x: cx, y: cy, ang: 0, len: r * .38, wid: r * .38, c: [.55, .3, .25], c2: [.4, .22, .18], seed: k + 3, type: DAB, alpha: .95, hgt: .35 }); }
}

// ---------- planlar ----------
export function planlariKur(M, IMG, FIG) {
  const TM = [TK[0] + TK[2] / 2, TK[1] + TK[3] / 2];
  const tabloMaske = (kam, a = 1) => { const c = M.camK(kam, .3); mRect(c, TK[0] - 4, TK[1] - 4, TK[2] + 8, TK[3] + 8, a, 2); };
  const theo = (t, S) => { const k = kare(FIG.theo_oda, t); if (k) figurDarbe(S, blenderKaynak(k), { W, gunes: ODA.LAMBA, hava: [.1, .09, .085], havaK: .25, cz: Math.floor(t * 15), altin: [1, .86, .62], kenarKirik: .45, kenarAlfa: .85 }); };
  // A01 · genis · ODA gece: kancanın odası (kapak A): lamba, sırtı dönük Theo, şövalede tek renkli tuval; yavaş yaklaşma
  plan({ id: 'A01', at: 'A01', sahne: 'oda', olcek: 'genis', not: 'Kapak A odası: Theo, lamba, renkli tuval',
    kamera: kamYol([960, 540, 1], [960 + (TM[0] - 960) * .45, 540 + (TM[1] - 540) * .45, 1.12], u => u),
    durum: st => ({ isik: 'gece', tablo: 'oda_otoportre', figur: theo }),
    maske: (st, kam) => tabloMaske(kam) });
  // A01b · yakin · MASA: alt çekmece sarı zarflarla dolu; "ekleniyor"da bir zarf daha düşer; yığının arasından badem dalı ucu (kapak B)
  const Y1 = yigin(34, { tohum: 10 });
  plan({ id: 'A01b', at: 'A01@alt', sahne: 'masa', olcek: 'yakin', not: 'Çekmece, sarı zarflar; bir zarf daha; badem dalı ucu',
    kamera: kamYol([960, 820, 1.35], [960, 860, 1.48], u => u),
    durum: st => { const te = A('A01@bir') - st.at, tb = A('A01@ekleniyor') - st.at; return {
      nesneler: t => { const L = Y1.slice(); const z = duser({ tur: 'zarf', x: 1010, y: 800, w: 240, h: 146, rot: .12, renk: 'sari', yuz: 'on', tohum: 99 }, t, te - .2); if (z) L.push(z); return L; },
      ust: (t, S) => bademDali(S, 700, 960, -.95, clamp((t - tb) / 1.7)) }; },
    maske: (st, kam) => { const c = M.camK(kam, 0); for (const it of Y1) nesneMaske(c, it); const te = A('A01@bir') - st.at, tb = A('A01@ekleniyor') - st.at; const z = duser({ tur: 'zarf', x: 1010, y: 800, w: 240, h: 146, rot: .12 }, st.lt, te - .2); if (z) nesneMaske(c, z); mDaire(c, 860, 800, 260, clamp((st.lt - tb) / .6), 6); } });
  // A02 · orta · MASA: masanın tamamı; solda sarı zarflar birer birer düşer (yığın yükselir), sağda ince gri deste (Theo'nun 39 mektubu);
  //   "attı ya yaktı": gri desteden birkaç yaprak kalkar, kadrajdan uçar (ateş gösterilmez)
  const Y2 = yigin(40, { x: 760, y: 820, dx: 420, dy: 160, tohum: 50 }), G2 = yigin(6, { x: 1430, y: 840, dx: 40, dy: 30, renk: 'gri', rot: .15, tohum: 200, kat: 1.2 });
  plan({ id: 'A02', at: 'A02', sahne: 'masa', olcek: 'orta', not: 'Sarı zarflar yağar; gri deste incelir',
    kamera: kamYol([960, 640, 1.02], [940, 700, 1.1]),
    durum: st => { const ty = A('A02@attı') - st.at; return {
      nesneler: t => { const L = [];
        Y2.forEach((it, i) => { const z = duser(it, t, i * .12 - 1.2, .5); if (z) L.push(z); });
        G2.forEach((it, i) => { const u = clamp((t - ty - i * .25) / 1.6); if (i < 3) L.push(it); else if (u < 1) L.push({ ...it, x: it.x + 700 * u * u, y: it.y - 500 * u * u, rot: it.rot + 3 * u, kalk: u, a: 1 - u * .2 }); });
        return L; } }; },
    maske: (st, kam) => { const c = M.camK(kam, 0); Y2.forEach((it, i) => { const z = duser(it, st.lt, i * .12 - 1.2, .5); if (z) nesneMaske(c, z); }); } });
  // A03 · ayrinti · MASA: masaya kapı aralığından bir kadın gölgesi düşer (yüz, el yok), çekmece karanlıkta kalır; ışık kapanır
  plan({ id: 'A03', at: 'A03', sahne: 'masa', olcek: 'ayrinti', not: 'Lamba kısılır, çekmece karanlıkta kalır (ikinci cevap sona saklanır)',
    kamera: kamYol([1000, 760, 1.6], [1000, 800, 1.7], u => u),
    durum: st => ({ expo: 1.05 - .75 * sm(st.d - 1.1, st.d - .1, st.lt), nesneler: () => Y1.slice(0, 20),
      }),
    maske: (st, kam) => { const c = M.camK(kam, 0); for (const it of Y1.slice(0, 20)) nesneMaske(c, it, 1 - sm(st.d - 1.1, st.d - .1, st.lt)); } });
}
