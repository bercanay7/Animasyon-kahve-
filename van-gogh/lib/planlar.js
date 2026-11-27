// Plan listesi (ölçek her plana yazılır; ardışık iki plan aynı ölçekte olmaz). Görsel ve figür yükleme, setlerin kurulumu.
import { W, H, A, S, Se, Wd, plan, sm, clamp, lerp, io, hsh, ikiser, mRect, mDaire, mTam } from './film_t.js';
import { figurDarbe, blenderKaynak, blenderKareleri } from '../../araclar/tablo/figur.js';
import { nesneMaske, RENK } from './nesne.js';
import { masaKur, CEKMECE } from './set_masa.js';
import { odaKur, ODA, TK } from './set_oda.js';
import { salonKur, SALON } from './set_salon.js';
import { tarlaKur, trenKur } from './set_disari.js';
import { planlar2 } from './planlar2.js';
import { tabloSahnesi, tabloCiz } from './film_t.js';
import { BRUSH, DAB, KNIFE } from '../../araclar/tablo/impasto.js';

// ---------- görseller (CC0 / kamu malı; araclar/ASSETS.md) ----------
const AD = 'gorsel/aday/';
const GORSEL = {
  oda_otoportre: 'gorsel/otoportre_hasir_sapka_1887_met436532.jpg',
  selvili_tarla: 'gorsel/selvili_bugday_tarlasi_1889_met436535.jpg',
  aycicek: AD + 'aycicekleri_1887_met436524.jpg', oda_aycicek: AD + 'aycicekleri_1887_met436524.jpg',
  selviler: AD + 'selviler_1889_met437980.jpg', irisler: AD + 'irisler_1889_getty90PA20.jpg',
  yatak: AD + 'yatak_odasi_1888_vgm_s0047V1962.jpg', oda_yatak: AD + 'yatak_odasi_1888_vgm_s0047V1962.jpg',   // ilk sürüm (Ekim 1888); AIC 1889 kopyası yedek
  auvers1: AD + 'yesil_bugday_tarlalari_1890_auvers_nga163323.jpg', auvers2: AD + 'beyazli_kiz_1890_auvers_nga46505.jpg', auvers3: AD + 'adeline_ravoux_1890_auvers_cma1958.31.jpg',
  remy1: AD + 'zeytin_agaclari_1889_saintremy_met437998.jpg', remy2: AD + 'zeytinlik_1889_saintremy_nga46627.jpg', remy3: AD + 'cinarlar_yol_iscileri_1889_saintremy_cma1947.209.jpg',
  sari_ev: AD + 'sari_ev_1888_vgm_f464_gap.jpg',
  badem: AD + 'badem_cicegi_1890_vgm_s0176V1962.jpg',
  sairin_bahcesi: AD + 'sairin_bahcesi_1888_arles_aic14586.jpg',
  remy4: AD + 'alpiller_iki_kavak_1889_saintremy_cma1958.32.jpg', remy5: AD + 'vazoda_irisler_1890_saintremy_met436528.jpg', remy6: AD + 'guller_1890_saintremy_met436534.jpg',
};
export async function gorselYukle() {
  const o = {};
  for (const [k, f] of Object.entries(GORSEL)) { const r = await fetch(f); if (!r.ok) { console.log('görsel yok: ' + f); continue; } o[k] = await createImageBitmap(await r.blob()); }
  return o;
}
// ---------- figür klipleri (Blender, 15 kare/sn; blender/klip.js) ----------
const KLIP = { theo_oda: ['blender/kare_oda', 121] };
for (const k of ['theo_dur', 'jo_dur', 'vincent_dur', 'theo_dis_dur', 'theo_oku', 'theo_yuru', 'jo_yuru', 'gauguin_yuru', 'vincent_yuru', 'theo_louvre', 'vincent_louvre']) KLIP[k] = ['blender/klip_' + k + '/kare', 121];
export async function figurYukle() { const o = {}; for (const [k, [d, n]] of Object.entries(KLIP)) o[k] = await blenderKareleri(d, n); return o; }
// döngülü kare (duruş klipleri 8 sn'de döner); yürüyüş klipleri son karede durur
const kareD = (BK, t, dongu = true) => { const n = BK.length, i = Math.round(ikiser(Math.max(0, t)) * 15); return BK[dongu ? i % (n - 1) : Math.min(n - 1, i)]; };
// figür yerleştirme: klibin ilk karesindeki boy ölçü; ayak ekranda [x, y], boy piksel
function figurBas(S, BK, t, ayak, boy, o = {}) {
  const k = kareD(BK, t + (o.kay || 0), o.dongu !== false); if (!k) return; const r = BK.find(Boolean); if (!r) return;
  const h0 = r.h, sc = boy / (h0 * 2), xc = r.x0 + r.w / 2, yb = r.y0 + r.h;
  figurDarbe(S, blenderKaynak(k), { W, konum: [ayak[0] - xc * 2 * sc, ayak[1] - yb * 2 * sc, sc], gunes: o.gunes || [ayak[0] - 400, ayak[1] - 900], hava: o.hava || [.1, .09, .085], havaK: o.havaK ?? .25, cz: Math.floor(t * 15),
    altin: o.altin || [1, .9, .74], kenarKirik: .45, kenarAlfa: o.kenarAlfa ?? .7, adim: o.adim || (boy > 500 ? 2 : 1) });
}
// ekran yazısı (alt banda inmez: y < 880): soluk krem, ince gölge; a saydamlık
function yazi(ctx, s, x, y, px, a = 1, hiz = 'center') {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha = clamp(a); ctx.font = `italic 600 ${px}px 'Cormorant Garamond', serif`; ctx.textAlign = hiz; ctx.textBaseline = 'alphabetic';
  ctx.shadowColor = 'rgba(0,0,0,.55)'; ctx.shadowBlur = px * .12; ctx.fillStyle = '#efe6d2'; ctx.fillText(s, x, Math.min(y, 860)); ctx.restore();
}
const kare = (BK, t) => BK[Math.max(0, Math.min(BK.length - 1, Math.round(ikiser(t) * 15)))];

export function setleriKur(M, IMG, FIG) { masaKur(M); odaKur(M, IMG); salonKur(M, IMG); tarlaKur(M); trenKur(M);
  // tablo sahneleri (gri dünya; renk örtüyle). Görsel gelmediyse yer tutucu: Selvili Buğday Tarlası
  // E03 "yüz elli resim": duvar boyu yan yana Saint-Rémy tabloları (her biri kendi oranında, araları koyu)
  const MZ = ['remy1', 'selviler', 'remy2', 'irisler', 'remy3', 'selvili_tarla', 'remy4', 'remy5', 'remy6'].filter(k => IMG[k]);
  M.tanimla('tb_mozaik', { zemin: [.07, .06, .05], kamera: () => ({ x: W / 2, y: H / 2, z: 1 }),
    katmanlar: MZ.map((k, i) => { const cx = 330 + (i % 3) * 630, cy = 200 + Math.floor(i / 3) * 340, im = IMG[k], ar = im.width / im.height, h = 300, w = Math.min(560, h * ar), hh = w / ar;
      return { ad: k, d: .72, ciz: tabloCiz(im, cx - w / 2, cy - hh / 2, w, hh, { maxR: 5 }), R: [10, 5, 2.6, 1.5], T: 8, olcek: .75 }; }),
    bitir: () => ({ light: [-.5, -.6, .7], norm: 2, expo: 1.04, contrast: 1.05, vig: .3, spec: .12, shin: 26, weave: .05 }) });
  // Commons (VGM) gelmezse CC0 yedek: Sarı Ev → Şairin Bahçesi (AIC; Arles 1888, sarı evin karşısındaki park); Fırtınalı gök → Yeşil Buğday Tarlaları, Auvers (NGA)
  const YEDEK = { sari_ev: 'sairin_bahcesi', firtina: 'auvers1' };
  for (const k of ['sari_ev', 'yatak', 'selviler', 'selvili_tarla', 'yildizli', 'badem', 'irisler', 'firtina']) tabloSahnesi(M, 'tb_' + k, IMG[k] || IMG[YEDEK[k]] || IMG.selvili_tarla, { dunya: true });
}

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
function bademDali(S, x0, y0, aci, u, sd = 3, olc = 1, iz = null) {   // iz: [x, y, r] dizisi (renk örtüsü dalın kendisine sınırlanır)
  // ana dal + iki yan sürgün; uç incelir; çiçekler beş taç yapraklı, beyazdan pembeye, ortası koyu (tablodaki gibi), tomurcuklar
  if (u <= 0) return;
  const dal = (x, y, a, n, k0, w0, sdd) => { const uc = []; for (let i = 0; i < n * clamp(u * 1.15 - k0); i++) { const L = (40 - i * 1.6) * olc; a += (hsh(sdd, i) - .5) * .32;
      const nx = x + Math.cos(a) * L, ny = y + Math.sin(a) * L, w = Math.max(2.5, (w0 - i * w0 / (n + 2)) * olc);
      if (iz) iz.push([(x + nx) / 2, (y + ny) / 2, L * .7]);
      S.push({ x: (x + nx) / 2, y: (y + ny) / 2, ang: a, len: L * 1.15, wid: w, c: [.2, .14, .11], c2: [.3, .22, .16], seed: sdd * 10 + i, type: BRUSH, alpha: 1, hgt: .7, taper: .15 });
      if (i % 2 === 1) uc.push([nx + Math.cos(a + (i % 4 ? 1.3 : -1.3)) * 16 * olc, ny + Math.sin(a + (i % 4 ? 1.3 : -1.3)) * 16 * olc, sdd * 50 + i, i / n]); x = nx; y = ny; }
    uc.push([x, y, sdd * 50 + 99, 1]); return { x, y, a, uc }; };
  const ana = dal(x0, y0, aci, 12, 0, 16, sd), c1 = [];
  const y1 = dal(x0 + Math.cos(aci) * 150 * olc, y0 + Math.sin(aci) * 150 * olc, aci + .7, 6, .3, 8, sd + 1), y2 = dal(x0 + Math.cos(aci) * 260 * olc, y0 + Math.sin(aci) * 260 * olc, aci - .8, 5, .45, 6, sd + 2);
  for (const [cx, cy, k, p] of [...ana.uc, ...y1.uc, ...y2.uc]) {
    const ac = clamp((u - .35 - p * .3) / .35); if (ac <= 0) continue; const r = (hsh(k, 1) < .3 ? 9 : 17) * olc * ac, tom = r < 10 * olc; if (iz) iz.push([cx, cy, r * 1.4]);
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

  // ================= B: Louvre'daki pusula =================
  const SE = SALON.ekr;
  // B01 · orta · SALON (Goupil şubesi): Theo sırttan, duvardaki çerçevelere bakar; kamera yanından kayar
  plan({ id: 'B01', at: 'B01', sahne: 'salon', olcek: 'orta', not: 'Goupil: Theo sırttan, çerçeveler',
    kamera: kamYol([1180, 560, 1.5], [1120, 560, 1.58], u => u),
    durum: st => ({ duvar: 'dolu', figur: (t, S) => figurBas(S, FIG.theo_dur, t, SE(1.4, 0, -5.2), 600, { gunes: [960, -300] }) }) });
  // B01b · ayrinti · MASA (çekmecesiz): katlı pusula açılır; ağabeyinin el yazısı (okunmaz)
  plan({ id: 'B01b', at: 'B01@pusula', sahne: 'masa', olcek: 'ayrinti', not: 'Pusula açılır',
    kamera: kamYol([960, 330, 1.45], [960, 340, 1.55], u => u),
    durum: st => ({ cekmece: false, nesneler: t => { const u = io(clamp(t / 1.3)); return [{ tur: 'kagit', x: 960, y: 330, w: 300 + 300 * u, h: 400, rot: -.06, tohum: 7, satir: 11, yazi: clamp(.15 + u), olc: 1.1, golge: true }]; } }) });
  // B02 · genis · SALON (Louvre, duvarlar dolu): Theo salonun derinliğine yürür; uzakta Vincent bir tabloya bakar, sonra döner
  plan({ id: 'B02', at: 'B02', sahne: 'salon', olcek: 'genis', not: 'Louvre: Theo yürür, uzakta Vincent',
    kamera: kamYol([960, 540, 1.0], [960, 545, 1.1], u => u),
    durum: st => ({ duvar: 'dolu', figur: (t, S) => { for (const k of ['vincent_louvre', 'theo_louvre']) { const B = FIG[k][Math.min(120, Math.round(ikiser(t + .6) * 15))]; if (B) figurDarbe(S, blenderKaynak(B), { W, gunes: [960, -400], hava: [.42, .4, .37], havaK: k === 'vincent_louvre' ? .35 : .15, cz: Math.floor(t * 15), altin: [1, .95, .85], kenarKirik: .5, kenarAlfa: .5 }); } } }) });
  // B03 · yakin · SALON (Goupil): bir çerçevenin önü; "satmak"ta köşesine satış etiketi asılır; Theo omzu kadrajın sağında
  plan({ id: 'B03', at: 'B03', sahne: 'salon', olcek: 'yakin', not: 'Başkalarının tabloları; satış etiketi',
    kamera: kamYol([380, 460, 2.3], [420, 470, 2.45], u => u),
    durum: st => { const te = A('B03@satmak') - st.at; return { duvar: 'dolu',
      nesneler: t => (t < te ? [] : [{ tur: 'bilet', x: 470, y: 560 + 30 * (1 - io(clamp((t - te) / .5))), w: 46, h: 28, rot: .25 + .1 * Math.sin((t - te) * 3) * Math.exp(-(t - te)), tohum: 3, golge: true }]),
      figur: (t, S) => figurBas(S, FIG.theo_dur, t, [760, 1300], 980, { gunes: [300, -200], adim: 2 }) }; } });
  // B04 · ayrinti · MASA: banknotlar zarfa girer, zarf kapanır; aynı hareket üç kez, üç mevsim ışığı (ritim)
  const B04 = [0, 1, 2];
  plan({ id: 'B04', at: 'B04', sahne: 'masa', olcek: 'ayrinti', not: 'Her ay bir zarf: üç tekrar, üç ışık',
    kamera: kamYol([960, 400, 1.3], [960, 400, 1.36], u => u),
    durum: st => { const T3 = st.d / 3, k = Math.min(2, Math.floor(st.lt / T3)), lt = st.lt - k * T3; return { cekmece: false, expo: [1.08, .92, 1.15][k],
      nesneler: () => { const u = io(clamp((lt - .3) / 1.2)), kap = io(clamp((lt - 1.7) / .6));
        return [{ tur: 'zarf', renk: 'gri', yuz: 'arka', x: 980, y: 420, w: 360, h: 220, rot: -.04 + k * .03, tohum: 40 + k, golge: true },
          ...[0, 1, 2].map(i => ({ tur: 'banknot', x: lerp(620 - i * 30, 980, u), y: lerp(330 + i * 18, 420, u), w: 300 * (1 - .3 * u), h: 150 * (1 - .3 * u), rot: -.3 + .26 * u + i * .05, tohum: 60 + i + k * 3, a: 1 - sm(.85, 1, u), kalk: .3 * (1 - u) })),
          ...(kap > 0 ? [{ tur: 'zarf', renk: 'gri', yuz: 'on', x: 980, y: 420, w: 360, h: 220, rot: -.04 + k * .03, tohum: 90 + k, a: kap }] : [])]; } }; },
    bitir: st => { const k = Math.min(2, Math.floor(st.lt / (st.d / 3))); return { light: [[-.45, -.7, .65], [.6, -.5, .6], [-.2, -.9, .5]][k], lightCol: [[1, .92, .8], [.85, .9, 1], [1, .97, .9]][k] }; } });
  // B05 · yakin · MASA: iki banknot destesi yan yana büyür: ince (işçinin aylığı) ve kalın (Theo'nun zarfı); üstte rakamlar (≤ 4 sn)
  plan({ id: 'B05', at: 'B05', sahne: 'masa', olcek: 'yakin', not: '32 gulden ve 50–75 gulden',
    kamera: kamYol([960, 420, 1.15], [960, 430, 1.22], u => u),
    durum: st => { const t1 = A('B05@otuz') - st.at, t2 = A('B05@bu') - st.at; return { cekmece: false,
      nesneler: t => { const L = []; const n1 = Math.round(4 * clamp((t - t1) / 1.2)), n2 = Math.round(9 * clamp((t - t2) / 2));
        // yelpaze: her banknot bir öncekinin üstüne kayık açılır (kalınlık tepeden görünmez; sayı yelpazenin genişliğiyle okunur)
        for (let i = 0; i < n1; i++) L.push({ tur: 'banknot', x: 520 + i * 34, y: 470 - i * 6, w: 280, h: 140, rot: -.25 + i * .09, tohum: 200 + i, golge: true });
        for (let i = 0; i < n2; i++) L.push({ tur: 'banknot', x: 1060 + i * 34, y: 470 - i * 6, w: 280, h: 140, rot: -.36 + i * .09, tohum: 300 + i, golge: true });
        return L; } }; },
    ust: (ctx, st) => { const t1 = A('B05@otuz') - st.at, t2 = A('B05@bu') - st.at;
      yazi(ctx, 'işçi: 32 gulden', 600, 250, 64, sm(t1, t1 + .4, st.lt) * (1 - sm(t1 + 3.6, t1 + 4, st.lt)));
      yazi(ctx, 'zarf: 50–75 gulden', 1260, 250, 64, sm(t2, t2 + .4, st.lt) * (1 - sm(t2 + 3.6, t2 + 4, st.lt))); } });
  // B06 · orta · ODA (rue Lepic, aynı daire: atölye): Vincent şövalenin başında, sırttan; "atölye"de şövaledeki tablo renge döner
  plan({ id: 'B06', at: 'B06', sahne: 'oda', olcek: 'orta', not: 'Odalardan biri atölye: şövalede renkli tablo',
    kamera: kamYol([900, 520, 1.45], [940, 500, 1.55], u => u),
    durum: st => ({ isik: 'ogle', tablo: 'oda_otoportre', figur: (t, S) => figurBas(S, FIG.vincent_dur, t, [520, 1020], 560, { gunes: [200, 200] }) }),
    maske: (st, kam) => { const ta = A('B06@atölye') - st.at; tabloMaske(kam, sm(ta, ta + .8, st.lt)); } });

  // B07 · orta · TARLA (akşam, park yolu): Theo ile Jo aralarında bir adım; "hayır"da Jo döner ve uzaklaşır
  plan({ id: 'B07', at: 'B07', sahne: 'tarla', olcek: 'orta', not: 'Evlenme teklifi; Jo hayır der, uzaklaşır',
    kamera: kamYol([1000, 640, 1.25], [980, 660, 1.32], u => u),
    durum: st => { const th = A('B07@hayır') - st.at; return { agac: true, expo: t => 1.0 - .06 * sm(th, th + 2, t),
      figur: (t, S) => { figurBas(S, FIG.theo_dis_dur, t, [860, 1010], 420, { gunes: [1500, 500], hava: [.3, .28, .3], havaK: .2 });
        if (t < th) figurBas(S, FIG.jo_dur, t, [1100, 1010], 390, { gunes: [1500, 500], hava: [.3, .28, .3], havaK: .2 });
        else figurBas(S, FIG.jo_yuru, t - th, [1100 + 160 * clamp((t - th) / 3), 1010 - 120 * clamp((t - th) / 3)], 390 * (1 - .3 * clamp((t - th) / 3)), { dongu: false, gunes: [1500, 500], hava: [.3, .28, .3], havaK: .2 + .2 * clamp((t - th) / 3) }); } }; } });
  // B08 · genis · TREN: gece treni güneye; "Ertesi"de gök ve ova öğleden sonra ışığına döner, tren yine geçer
  plan({ id: 'B08', at: 'B08', sahne: 'tren', olcek: 'genis', not: 'Gece treni; ertesi gün öğleden sonra',
    kamera: kamYol([960, 560, 1.04], [960, 560, 1.1], u => u),
    durum: st => { const te = A('B08@ertesi') - st.at; return { gun: t => sm(te, te + 1.2, t),
      tren: t => [[-200 + 520 * t, 1]] }; } });
  planlar2(M, IMG, FIG, { kamYol, yigin, duser, bademDali, figurBas, yazi, tabloMaske, kareD });
}
// kapak.html için: aynı setler ve yardımcılar
export function kapakYardim(M, IMG, FIG) {
  const tabloMaske = (kam, a = 1) => { const c = M.camK(kam, .3); mRect(c, TK[0] - 4, TK[1] - 4, TK[2] + 8, TK[3] + 8, a, 2); };
  const Y = yigin(40, { renk: 'gri', tohum: 70 }), IZ = [];
  return { tabloMaske,
    theo: (t, S) => figurBas(S, FIG.theo_dur, t, [1640, 1240], 900, { gunes: ODA.LAMBA, adim: 2, hava: [.05, .05, .05], havaK: .3 }),
    cekmeceDurum: () => ({ nesneler: () => Y, ust: (t, S) => { IZ.length = 0; bademDali(S, 700, 1040, -1.0, 1, 3, 1.7, IZ); } }),
    cekmeceMaske: (kam, m) => { const c = M.camK(kam, 0); for (const [x, y, r] of IZ) mDaire(c, x, y, r, 1, 2); } };
}
