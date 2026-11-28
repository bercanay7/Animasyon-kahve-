// Plan listesi (ölçek her plana yazılır; ardışık iki plan aynı ölçekte olmaz). Görsel ve figür yükleme, setlerin kurulumu.
import { W, H, A, S, Se, Wd, plan, planlar, sm, clamp, lerp, io, hsh, ikiser, mRect, mDaire, mTam, mSil, mx, MW, ekrana } from './film_t.js';
import { figurDarbe, blenderKaynak, blenderKareleri } from '../../araclar/tablo/figur.js';
import { nesneMaske, RENK } from './nesne.js';
import { masaKur, CEKMECE } from './set_masa.js';
import { odaKur, ODA, TK, TKf } from './set_oda.js';
import { salonKur, SALON } from './set_salon.js';
import { tarlaKur, trenKur } from './set_disari.js';
import { planlar2 } from './planlar2.js';
import { tabloSahnesi, tabloCiz } from './film_t.js';
import { BRUSH, DAB, KNIFE } from '../../araclar/tablo/impasto.js';

// ---------- görseller (CC0 / kamu malı; araclar/ASSETS.md) ----------
const AD = 'gorsel/aday/';
const GORSEL = {
  // v4: Theo'nun dairesinde belgelenen tablolar (DOGRULAMA §8). Met otoportresi 1887–88'de başkasına verilmişti; VGM'ninki Theo'da kaldı
  oda_otoportre: 'gorsel/aday_v3/vgm_otoportre_hasir_sapka_1887_s0164V1962.jpg', oda_manzara: 'gorsel/aday_v3/vgm_theo_dairesinden_gorunum_1887_s0057V1962.jpg', oda_hasat: 'gorsel/aday_v3/vgm_hasat_1888_s0030V1962.jpg',
  met_otoportre: 'gorsel/otoportre_hasir_sapka_1887_met436532.jpg',
  selvili_tarla: 'gorsel/selvili_bugday_tarlasi_1889_met436535.jpg',
  aycicek: AD + 'aycicekleri_1887_met436524.jpg', oda_aycicek: AD + 'aycicekleri_1887_met436524.jpg',
  selviler: AD + 'selviler_1889_met437980.jpg', irisler: AD + 'irisler_1889_getty90PA20.jpg',
  yatak: AD + 'yatak_odasi_1888_vgm_s0047V1962.jpg', oda_yatak: AD + 'yatak_odasi_1888_vgm_s0047V1962.jpg',   // ilk sürüm (Ekim 1888); AIC 1889 kopyası yedek
  auvers1: AD + 'yesil_bugday_tarlalari_1890_auvers_nga163323.jpg', auvers2: AD + 'beyazli_kiz_1890_auvers_nga46505.jpg', auvers3: AD + 'adeline_ravoux_1890_auvers_cma1958.31.jpg',
  remy1: AD + 'zeytin_agaclari_1889_saintremy_met437998.jpg', remy2: AD + 'zeytinlik_1889_saintremy_nga46627.jpg', remy3: AD + 'cinarlar_yol_iscileri_1889_saintremy_cma1947.209.jpg',
  yildizli: AD + 'yildizli_gece_1889_moma_gap.jpg',
  firtina: AD + 'firtinali_gok_bugday_1890_vgm_s0106V1962.jpg',
  sari_ev: AD + 'sari_ev_1888_vgm_f464_gap.jpg',
  badem: AD + 'badem_cicegi_1890_vgm_s0176V1962.jpg', oda_badem: AD + 'badem_cicegi_1890_vgm_s0176V1962.jpg',
  sairin_bahcesi: AD + 'sairin_bahcesi_1888_arles_aic14586.jpg',
  rhone: 'gorsel/aday_v3/rhone_yildizli_gece_1888_orsay.jpg',
  // v3: sergilenen eserler (C03 1888, F08 1890; vangoghletters 582 n. 9, 854 n. 7; künye ASSETS.md)
  sergi88_1: 'gorsel/aday_v3/sergi88_1_montmartre_moulin_f316.jpg', sergi88_2: 'gorsel/aday_v3/sergi88_2_montmartre_bostan_f350.jpg', sergi88_3: 'gorsel/aday_v3/sergi88_3_romans_parisiens_f359.jpg',
  sergi90_ravine: 'gorsel/aday_v3/sergi90_ravine_f662.jpg', sergi90_kestane: 'gorsel/aday_v3/sergi90_kestane_f517.jpg', sergi90_dut: 'gorsel/aday_v3/sergi90_dut_f637.jpg', sergi90_sarmasik: 'gorsel/aday_v3/sergi90_sarmasik_f609.jpg',
  sergi90_gundogumu: 'gorsel/aday_v3/sergi90_gundogumu_f737.jpg', sergi90_aycicek: 'gorsel/aday_v3/sergi90_aycicek_f454.jpg', sergi90_dagli: 'gorsel/aday_v3/sergi90_dagli_f611.jpg', sergi90_zeytin: 'gorsel/aday_v3/sergi90_zeytin_f586.jpg', kirmizi_bag: 'gorsel/aday_v3/kirmizi_bag_1888_pushkin.jpg',   // v3: Commons PD-Art (Google Art Project / Puşkin); ASSETS.md
  remy4: AD + 'alpiller_iki_kavak_1889_saintremy_cma1958.32.jpg', remy5: AD + 'vazoda_irisler_1890_saintremy_met436528.jpg', remy6: AD + 'guller_1890_saintremy_met436534.jpg', oda_guller: AD + 'guller_1890_saintremy_met436534.jpg',
};
export async function gorselYukle() {
  const o = {};
  for (const [k, f] of Object.entries(GORSEL)) { const r = await fetch(f); if (!r.ok) { console.log('görsel yok: ' + f); continue; } o[k] = await createImageBitmap(await r.blob()); }
  return o;
}
// ---------- figür klipleri (Blender, 15 kare/sn; blender/klip.js) ----------
const KLIP = { theo_oda: ['blender/kare_oda', 121] };
for (const k of ['theo_dur', 'jo_dur', 'vincent_dur', 'theo_dis_dur', 'theo_oku', 'theo_yuru', 'jo_yuru', 'gauguin_yuru', 'vincent_yuru', 'theo_louvre', 'vincent_louvre', 'vincent_oku', 'jo_bebek', 'jo_egil', 'theo_don', 'vincent_goster', 'theo_goster', 'jo_yan', 'theo_egil']) KLIP[k] = ['blender/klip_' + k + '/kare', 121];
// v4 (Y4): Blender'da modellenmiş figürler; ?fig=v4 ile denenir (kapı). Kırpılmış teslim tam kareye açılmış hâli.
const V4 = { theo_oda: 'blender/kare_oda_v4', theo_dur: 'blender/klip_theo_dur_v4/kare', vincent_goster: 'blender/klip_vincent_goster_v4/kare' };
export async function figurYukle() { const v4 = new URLSearchParams(location.search).get('fig') === 'v4', o = {};
  for (const [k, [d, n]] of Object.entries(KLIP)) o[k] = await blenderKareleri(v4 && V4[k] ? V4[k] : d, n); return o; }
// döngülü kare (duruş klipleri 8 sn'de döner); yürüyüş klipleri son karede durur
const kareD = (BK, t, dongu = true) => { const n = BK.length, i = Math.round(ikiser(Math.max(0, t)) * 15); return BK[dongu ? i % (n - 1) : Math.min(n - 1, i)]; };
// figür yerleştirme: klibin ilk karesindeki boy ölçü; ayak ekranda [x, y], boy piksel
function figurBas(S, BK, t, ayak, boy, o = {}) {
  const k = kareD(BK, t + (o.kay || 0), o.dongu !== false); if (!k) return; const r = BK.find(Boolean); if (!r) return;
  const h0 = r.h, sc = boy / (h0 * 2), xc = r.x0 + r.w / 2, yb = r.y0 + r.h;
  // zemine temas gölgesi (havada durma); v3: o karenin ayak noktasından (yürüyen figürde ilk karenin yerinde kalıyordu)
  if (!o.golge && o.temas !== false) { const fx = ayak[0] + ((k.x0 + k.w / 2) - xc) * 2 * sc, fy = ayak[1] + ((k.y0 + k.h) - yb) * 2 * sc, bk = boy * (k.h / h0);
    S.push({ x: fx, y: fy - bk * .004, ang: 0, len: bk * .34, wid: bk * .036, c: [.03, .025, .02], c2: [.03, .025, .02], seed: 7, type: DAB, alpha: .4, hgt: 0 }); }
  figurDarbe(S, blenderKaynak(k), { W, konum: [ayak[0] - xc * 2 * sc, ayak[1] - yb * 2 * sc, sc], gunes: o.gunes || [ayak[0] - 400, ayak[1] - 900], hava: o.hava || [.1, .09, .085], havaK: o.havaK ?? .25, cz: Math.floor(t * 15),
    altin: o.altin || [1, .9, .74], kenarKirik: .45, kenarAlfa: o.kenarAlfa ?? .7, adim: o.adim || (boy > 500 ? 2 : 1), golge: o.golge });
}
// ekran yazısı (alt banda inmez: y < 880): soluk krem, ince gölge; a saydamlık
function yazi(ctx, s, x, y, px, a = 1, hiz = 'center') {
  if (a <= 0) return; ctx.save(); ctx.globalAlpha = clamp(a); ctx.font = `italic 600 ${px}px 'Cormorant Garamond', serif`; ctx.textAlign = hiz; ctx.textBaseline = 'alphabetic';
  ctx.shadowColor = 'rgba(0,0,0,.55)'; ctx.shadowBlur = px * .12; ctx.fillStyle = '#efe6d2'; ctx.fillText(s, x, Math.min(y, 860)); ctx.restore();
}
const kare = (BK, t) => BK[Math.max(0, Math.min(BK.length - 1, Math.round(ikiser(t) * 15)))];

export function setleriKur(M, IMG, FIG) { masaKur(M, IMG); odaKur(M, IMG); salonKur(M, IMG); tarlaKur(M); trenKur(M);
  // tablo sahneleri (gri dünya; renk örtüyle). Görsel gelmediyse yer tutucu: Selvili Buğday Tarlası
  // E03 "yüz elli resim": duvar boyu yan yana Saint-Rémy tabloları (her biri kendi oranında, araları koyu)
  const MZ = ['remy1', 'selviler', 'remy2', 'irisler', 'remy3', 'selvili_tarla', 'remy4', 'remy5', 'remy6'].filter(k => IMG[k]);
  M.tanimla('tb_mozaik', { zemin: [.08, .08, .08],   // v3: nötr (kahverengi duvar renk kuralını bozuyordu)
    kamera: () => ({ x: W / 2, y: H / 2, z: 1 }),
    katmanlar: MZ.map((k, i) => { const cx = 330 + (i % 3) * 630, cy = 200 + Math.floor(i / 3) * 340, im = IMG[k], ar = im.width / im.height, h = 300, w = Math.min(560, h * ar), hh = w / ar;
      return { ad: k, d: .72, ciz: tabloCiz(im, cx - w / 2, cy - hh / 2, w, hh, { maxR: 5 }), R: [10, 5, 2.6, 1.5], T: 8, olcek: .75 }; }),
    bitir: () => ({ light: [-.5, -.6, .7], norm: 2, expo: 1.04, contrast: 1.05, vig: .3, spec: .12, shin: 26, weave: .05 }) });
  // Commons (VGM) gelmezse CC0 yedek: Sarı Ev → Şairin Bahçesi (AIC; Arles 1888, sarı evin karşısındaki park); Fırtınalı gök → Yeşil Buğday Tarlaları, Auvers (NGA)
  const YEDEK = { sari_ev: 'sairin_bahcesi', firtina: 'auvers1', rhone: 'yildizli' };
  // v3: Yatak Odası ince darbeyle (kırmızı yorgan büyük darbede dokusuz düz lekeye dönüyordu: kan okuması); Rhône karanlık çekim, ışık açılır
  const TS = { yatak: { maxR: 6, detail: 1, R: [11, 5.5, 2.8, 1.5] }, rhone: { maxR: 8 } };
  for (const k of ['sari_ev', 'yatak', 'selviler', 'selvili_tarla', 'yildizli', 'badem', 'irisler', 'firtina', 'rhone']) tabloSahnesi(M, 'tb_' + k, IMG[k] || IMG[YEDEK[k]] || IMG.selvili_tarla, { dunya: true, ...(TS[k] || {}) });
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

// v3: badem dalı Badem Çiçeği tablosunun kendisinden kesilir (turkuaz gök anahtarlanır); darbe noktaları bir kez örneklenir.
//   Çizilmiş dal (beyaz papatya + turuncu hale) çıkartma gibi okunuyordu; şimdi 0:10'daki dal 4:58'deki doruğun tohumu.
//   kesit: tablonun üst ortasındaki çiçekli sürgün; kök kesitin sağ kenarında (kx, ky)
const BKR = [.27, 0, .48, .4], BKOK = [.97, .47];
let BKS = null;
function bademKes(img, N = 240) {
  if (BKS || !img) return BKS; const sw = BKR[2] * img.width, sh = BKR[3] * img.height, Mh = Math.round(N * sh / sw);
  const cv = new OffscreenCanvas(N, Mh), cx = cv.getContext('2d'); cx.drawImage(img, BKR[0] * img.width, BKR[1] * img.height, sw, sh, 0, 0, N, Mh);
  const d = cx.getImageData(0, 0, N, Mh).data, P = [], sil = new OffscreenCanvas(N, Mh), sx = sil.getContext('2d'), sd = sx.createImageData(N, Mh);
  const gok = (x, y) => { if (x < 0 || y < 0 || x >= N || y >= Mh) return true; const i = (y * N + x) * 4; return d[i + 2] > d[i] + 14 && d[i + 1] > d[i] + 2; };
  for (let y = 0; y < Mh; y++) for (let x = 0; x < N; x++) { const i = (y * N + x) * 4, r = d[i], g = d[i + 1], b = d[i + 2]; if (gok(x, y)) continue;
    let k = 0; for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) if ((dx || dy) && !gok(x + dx, y + dy)) k++; if (k < 2) continue;   // v3: gök kenarındaki kırıntı (küf gibi benek) atılır
    P.push([x / N, y / Mh, r / 255, g / 255, b / 255, Math.hypot(x / N - BKOK[0], (y / Mh - BKOK[1]) * Mh / N)]); sd.data[i] = sd.data[i + 1] = sd.data[i + 2] = sd.data[i + 3] = 255; }
  sx.putImageData(sd, 0, 0); P.sort((a, b) => a[5] - b[5]); return (BKS = { P, sil, N, M: Mh, dmax: P.length ? P[P.length - 1][5] : 1 });
}
// dal: kök ekranda (x0, y0), uç yönü aci, genişlik gen piksel; u 0..1 büyüme (kökten uca)
function bademKesCiz(S, B, x0, y0, aci, u, gen = 560) {
  if (!B || u <= 0) return; const s = gen / B.N, a = aci - Math.PI, ca = Math.cos(a), sa = Math.sin(a), lim = u * B.dmax * 1.02;
  for (const [px, py, r, g, b, dd] of B.P) { if (dd > lim) break; const lx = (px - BKOK[0]) * gen, ly = (py - BKOK[1]) * gen * B.M / B.N;
    const X = x0 + lx * ca - ly * sa, Y = y0 + lx * sa + ly * ca, c = [r, g, b];
    S.push({ x: X, y: Y, ang: a + (px * 9 % 1) * .6, len: s * 2.1, wid: s * 1.7,   /* v3: komşu darbeler birleşir (dal nokta mozaiği gibi kopuktu) */ c, c2: c.map(v => v * .9), seed: px * 977 + py * 131, type: DAB, alpha: clamp((lim - dd) / (B.dmax * .05)), hgt: .5 }); }
}
function bademKesMaske(c, B, x0, y0, aci, u, gen = 560) {
  if (!B || u <= 0) return; const k = MW / 1920, [X, Y] = ekrana(c, x0, y0), sc = gen / B.N * c.zoom * k;
  mx.save(); mx.translate(X * k, Y * k); mx.rotate(aci - Math.PI); mx.scale(sc, sc); mx.beginPath(); mx.arc(0, 0, u * B.dmax * B.N * 1.02, 0, Math.PI * 2); mx.clip();
  mx.filter = 'blur(.6px)'; mx.drawImage(B.sil, -BKOK[0] * B.N, -BKOK[1] * B.M); mx.restore();
}

// ---------- planlar ----------
export function planlariKur(M, IMG, FIG) {
  const BK = bademKes(IMG.badem);
  const TM = [TK[0] + TK[2] / 2, TK[1] + TK[3] / 2];
  const tabloMaske = (kam, a = 1, k = 'oda_otoportre') => { const c = M.camK(kam, .3), R = TKf(IMG[k]); mRect(c, R[0] - 4, R[1] - 4, R[2] + 8, R[3] + 8, a, 2); };
  const theo = (t, S) => { const k = kare(FIG.theo_oda, t); if (k) figurDarbe(S, blenderKaynak(k), { W, gunes: ODA.LAMBA, hava: [.1, .09, .085], havaK: .25, cz: Math.floor(t * 15), altin: [1, .86, .62], kenarKirik: .45, kenarAlfa: .85 }); };
  // A01 · genis · ODA gece: kancanın odası (kapak A): lamba, sırtı dönük Theo, şövalede tek renkli tuval; yavaş yaklaşma
  plan({ id: 'A01', at: 'A01', sahne: 'oda', olcek: 'genis', not: 'Kapak A odası: Theo, lamba, renkli tuval',
    kamera: kamYol([960, 540, 1], [960 + (TM[0] - 960) * .45, 540 + (TM[1] - 540) * .45, 1.12], u => u),
    durum: st => ({ isik: 'gece', tablo: 'oda_otoportre', figur: theo }),
    maske: (st, kam) => tabloMaske(kam) });
  // A01b · yakin · MASA (v2): çekmecede gri bir zarf yığını; "sarı"da renk yığına yayılır; "dolu"da yığının arasından badem dalı uzanır (kapak B'nin vaadi,
  //   dal sahnenin sonuna kadar tam görünür); "her hafta bir zarf daha"da bir zarf düşer
  const Y1 = yigin(34, { tohum: 10 });
  plan({ id: 'A01b', at: 'A01@alt', sahne: 'masa', olcek: 'yakin', not: 'Çekmece: "sarı"da renk, "dolu"da badem dalı, bir zarf daha',
    kamera: kamYol([960, 820, 1.35], [960, 860, 1.48], u => u),
    durum: st => { const te = A('A01@bir#1') - st.at + .25, tb = A('A01@dolu') - st.at; return {
      nesneler: t => { const L = Y1.slice(); const z = duser({ tur: 'zarf', x: 1010, y: 800, w: 240, h: 146, rot: .12, renk: 'sari', yuz: 'on', tohum: 99 }, t, te - .2); if (z) L.push(z); return L; },
      ust: (t, S) => (BK ? bademKesCiz(S, BK, 1120, 770, -2.2, clamp((t - tb) / 1.4), 700) : bademDali(S, 700, 960, -.95, clamp((t - tb) / 1.2))) }; },
    maske: (st, kam) => { const c = M.camK(kam, 0), ts = A('A01@sarı') - st.at, te = A('A01@bir#1') - st.at + .25, tb = A('A01@dolu') - st.at;
      Y1.forEach((it, i) => nesneMaske(c, it, clamp((st.lt - ts - Math.hypot(it.x - 960, it.y - 860) / 900) / .35)));   // sarı yığına merkezden yayılır (masa gri kalır)
      const z = duser({ tur: 'zarf', x: 1010, y: 800, w: 240, h: 146, rot: .12 }, st.lt, te - .2); if (z) nesneMaske(c, z);
      if (BK) bademKesMaske(c, BK, 1120, 770, -2.2, clamp((st.lt - tb) / 1.4), 700); else mDaire(c, 860, 800, 260, clamp((st.lt - tb) / .6), 6); } });   // v3: örtü yalnız dalın kendisi (hale yok)
  // A02 · orta · MASA (v2): masanın tamamı; sarı yığın "mektup"a dek yükselir; sağda kalın gri blok (Theo'nun 39 mektubu); "altı yüz elli bir" ve "otuz dokuz" ekranda (≤ 4 sn);
  //   "attı ya yaktı"da gri bloktan yapraklar kalkar, kadrajdan uçar (ateş gösterilmez)
  const Y2 = yigin(40, { x: 700, y: 760, dx: 420, dy: 160, tohum: 50 }), G2 = yigin(39, { x: 1400, y: 780, dx: 20, dy: 12, renk: 'gri', w: 200, h: 120, rot: .12, tohum: 200, kat: 1.5 });
  plan({ id: 'A02', at: 'A02', sahne: 'masa', olcek: 'orta', not: '651 sarı zarf ve 39 gri; gri deste kalkar',
    kamera: kamYol([960, 600, 1.0], [950, 640, 1.05]),   // v3: kenarda siyah bant kalmasın
    durum: st => { const ty = A('A02@attı') - st.at, tm = A('A02@mektup') - st.at; return {
      nesneler: t => { const L = [];
        Y2.forEach((it, i) => { const z = duser(it, t, -1 + i * (tm + 1) / 40, .5); if (z) L.push(z); });
        G2.forEach((it, i) => { const u = clamp((t - ty - (i % 9) * .12 - Math.floor(i / 9) * .05) / 1.6); if (i < 6) L.push(it); else if (u < 1) L.push({ ...it, x: it.x + 700 * u * u, y: it.y - 500 * u * u - i * .6, rot: it.rot + 3 * u, kalk: u, a: 1 - u * .2 }); });
        return L; } }; },
    maske: (st, kam) => { const c = M.camK(kam, 0), tm = A('A02@mektup') - st.at; Y2.forEach((it, i) => { const z = duser(it, st.lt, -1 + i * (tm + 1) / 40, .5); if (z) nesneMaske(c, z); }); },
    ust: (ctx, st) => { const t1 = A('A02@altı') - st.at, t2 = A('A02@otuz') - st.at;
      yazi(ctx, '651', 700, 330, 150, sm(t1, t1 + .4, st.lt) * (1 - sm(t1 + 3.6, t1 + 4, st.lt)));
      yazi(ctx, '39', 1400, 330, 150, sm(t2, t2 + .4, st.lt) * (1 - sm(t2 + 3.6, t2 + 4, st.lt))); } });
  // A03 · ayrinti · MASA (v2): Jo ekilir: masaya düşen bir kadın gölgesi (toplu saç, omuz; yüz yok); "iki"de bir sarı zarf yukarı kalkıp kadrajdan çıkar;
  //   "ikincisi"nde çekmece kapanır, ince ışık yarığı kalır; ışık kararır
  plan({ id: 'A03', at: 'A03', sahne: 'masa', olcek: 'ayrinti', not: 'Jo ekilir: gölge, kalkan zarf, çekmece kapanır',
    kamera: kamYol([1000, 700, 1.55], [1000, 740, 1.65], u => u),
    durum: st => { const ti = A('A03@iki') - st.at, tk = A('A03@ikincisi') - st.at; return {
      expo: 1.05 - .7 * sm(st.d - 1.1, st.d - .1, st.lt), cekmeceAc: t => 1 - .93 * io(clamp((t - tk) / 1.0)),
      nesneler: t => { const L = Y1.slice(0, 20); const u = clamp((t - ti) / 1.2); if (u > 0) L.push({ tur: 'zarf', renk: 'sari', yuz: 'on', x: 1050 + 120 * u, y: 790 - 700 * io(u), w: 240, h: 146, rot: .1 + .4 * u, kalk: .6 * u, tohum: 98 }); return L; },
      golge: (t, S) => figurBas(S, FIG.jo_dur, t, [1640, 2900], 3000, { golge: (.38) * .55, adim: 2, temas: false }) }; },
    maske: (st, kam) => { const c = M.camK(kam, 0), ti = A('A03@iki') - st.at, tk = A('A03@ikincisi') - st.at, k = 1 - sm(st.d - 1.1, st.d - .1, st.lt);
      for (const it of Y1.slice(0, 20)) nesneMaske(c, it, k); const u = clamp((st.lt - ti) / 1.2); if (u > 0) nesneMaske(c, { x: 1050 + 120 * u, y: 790 - 700 * io(u), w: 240, h: 146, rot: .1 + .4 * u });
      const ac = 1 - .93 * io(clamp((st.lt - tk) / 1.0)); mSil(c, 0, 625, 1920, (1 - ac) * 575); } });

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
  // B03 · yakin · SALON (Goupil, v3): cepheden bir duvar, gri tablolar; "satmak"ta ortadaki çerçeveye "satıldı" kartı asılır, sonra tablo duvardan indirilip kadrajdan çıkar
  //   (duvarda açık bir iz kalır); Theo sağ önde sırttan. Plan notundaki etiket karede yoktu: somut olay.
  const B3 = [{ tur: 'cerceve', x: 650, y: 440, w: 170, h: 210, tohum: 33, ic: [.46, .44, .4] }, { tur: 'cerceve', x: 1190, y: 430, w: 200, h: 150, tohum: 35, ic: [.56, .53, .47] }];
  const B3k = kamYol([930, 500, 1.78], [950, 505, 1.86], u => u);
  plan({ id: 'B03', at: 'B03', sahne: 'salon', olcek: 'yakin', not: 'Başkalarının tabloları: biri satılır, duvardan iner', kamera: B3k,
    durum: st => { const te = A('B03@başkalarının') - st.at; return { duvar: 'seyrek', bolme: true,
      nesneler: t => { const k = io(clamp((t - te - 1.5) / 1.4)), dy = -700 * k, kart = io(clamp((t - te) / .5)), sal = .12 * Math.sin((t - te) * 4) * Math.exp(-1.5 * Math.max(0, t - te));
        return [...B3, ...(k > 0 ? [{ tur: 'kagit', x: 915, y: 460, w: 236, h: 176, satir: 0, a: .2 * k, tohum: 36 }] : []),
          { tur: 'cerceve', x: 915, y: 460 + dy, w: 240, h: 180, tohum: 34, ic: [.6, .56, .48] },
          ...(kart > 0 ? [{ tur: 'bilet', bos: true, x: 1000, y: 575 + dy - 26 * (1 - kart), w: 92, h: 46, rot: .08 + sal, tohum: 37, a: kart, golge: true }] : [])]; },
      figur: (t, S) => figurBas(S, FIG.theo_dur, t, [1330, 1180], 860, { gunes: [700, -200], adim: 2 }) }; },
    ust: (ctx, st) => { const te = A('B03@başkalarının') - st.at, kart = io(clamp((st.lt - te) / .5)); if (kart <= 0) return; const k = io(clamp((st.lt - te - 1.5) / 1.4)), dy = -700 * k, sal = .12 * Math.sin((st.lt - te) * 4) * Math.exp(-1.5 * Math.max(0, st.lt - te));
      const c = M.camK(B3k(st.u), .72), [x, y] = ekrana(c, 1000, 575 + dy - 26 * (1 - kart)); if (y < -50) return;
      ctx.save(); ctx.globalAlpha = kart; ctx.translate(x, Math.min(y, 860)); ctx.rotate(.08 + sal); ctx.font = `italic 700 ${Math.round(26 * c.zoom)}px 'Cormorant Garamond', serif`; ctx.fillStyle = '#2a1f18'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('satıldı', 0, 2); ctx.restore(); } });
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
  // B05 · yakin · MASA (v3): boş masa ≤ 1 sn: işçinin aylığı (4 banknotluk ince yelpaze) soldan kayarak "işçi"ye dek gelir; "zarflar"da sağdan gri bir zarf ve
  //   9 banknotluk geniş yelpaze. Rakamlar büyük, opak ve plan sonuna dek ekranda (telefonda okunmuyordu)
  plan({ id: 'B05', at: 'B05', sahne: 'masa', olcek: 'yakin', not: '32 gulden ve 50–75 gulden',
    kamera: kamYol([960, 440, 1.12], [960, 450, 1.18], u => u),
    durum: st => { const t1 = A('B05@işçi') - st.at, t2 = A('B05@zarflar') - st.at; return { cekmece: false,
      nesneler: t => { const L = [], gir = (a, b, i, n) => io(clamp((t - a - (b - a) * i / n) / .6));
        for (let i = 0; i < 4; i++) { const v = gir(.15, t1 - .4, i, 4); if (v > 0) L.push({ tur: 'banknot', x: 470 + i * 40 - 800 * (1 - v), y: 560 - i * 6, w: 280, h: 140, rot: -.25 + i * .09, tohum: 200 + i, golge: true, kalk: .3 * (1 - v) }); }
        const z = io(clamp((t - t2 + .3) / .6)); if (z > 0) L.push({ tur: 'zarf', renk: 'gri', yuz: 'arka', x: 1380 + 700 * (1 - z), y: 600, w: 380, h: 230, rot: -.05, tohum: 210, golge: true });
        for (let i = 0; i < 9; i++) { const v = gir(t2, t2 + 1.6, i, 9); if (v > 0) L.push({ tur: 'banknot', x: 1100 + i * 40 + 800 * (1 - v), y: 560 - i * 6, w: 280, h: 140, rot: -.36 + i * .09, tohum: 300 + i, golge: true, kalk: .3 * (1 - v) }); }
        return L; } }; },
    ust: (ctx, st) => { const t1 = A('B05@otuz') - st.at, t2 = A('B05@elli') - st.at, a1 = sm(t1 - .1, t1 + .3, st.lt), a2 = sm(t2 - .1, t2 + .3, st.lt);
      yazi(ctx, '32 gulden', 600, 250, 96, a1); yazi(ctx, 'bir işçinin aylığı', 600, 318, 50, a1);
      yazi(ctx, '50–75 gulden', 1330, 250, 96, a2); yazi(ctx, 'her ay bir zarf', 1330, 318, 50, a2); } });
  // B06 · orta · ODA (rue Lepic, aynı daire: atölye): Vincent şövalenin başında, sırttan; "atölye"de şövaledeki tablo renge döner
  plan({ id: 'B06', at: 'B06', sahne: 'oda', olcek: 'orta', not: 'Odalardan biri atölye: şövalede renkli tablo',
    kamera: kamYol([900, 520, 1.45], [940, 500, 1.55], u => u),
    durum: st => ({ isik: 'ogle', tablo: 'oda_manzara', figur: (t, S) => figurBas(S, FIG.vincent_dur, t, [520, 1020], 560, { gunes: [200, 200] }) }),
    maske: (st, kam) => { const ta = A('B06@odalardan') - st.at; tabloMaske(kam, sm(ta, ta + .8, st.lt), 'oda_manzara');   /* tarama: 'atölye'de açılınca tam renk 0,4 sn kalıyordu */ } });

  // B07 · orta · TARLA (akşam, park yolu): Theo ile Jo aralarında bir adım; "hayır"da Jo döner ve uzaklaşır
  plan({ id: 'B07', at: 'B07', sahne: 'tarla', olcek: 'genis', not: 'Evlenme teklifi; Jo hayır der, uzaklaşır',
    kamera: kamYol([960, 560, 1.0], [960, 570, 1.06], u => u),
    durum: st => { const th = A('B07@hayır') - st.at; return { agac: true, expo: t => 1.0 - .06 * sm(th, th + 2, t),
      figur: (t, S) => { figurBas(S, FIG.theo_dis_dur, t, [860, 1010], 420, { gunes: [1500, 500], hava: [.3, .28, .3], havaK: .2 });
        if (t < th) figurBas(S, FIG.jo_dur, t, [1100, 1010], 390, { gunes: [1500, 500], hava: [.3, .28, .3], havaK: .2 });
        else { const q = clamp((t - th) / 2); figurBas(S, FIG.jo_yuru, (t - th) * 1.6, [1100 + 260 * q, 1010 - 150 * q], 390 * (1 - .4 * q), { dongu: false, gunes: [1500, 500], hava: [.3, .28, .3], havaK: .2 + .25 * q }); } } }; } });   // v3: "hayır"da hızla uzaklaşır
  // B08 · genis · TREN: gece treni güneye; "Ertesi"de gök ve ova öğleden sonra ışığına döner, tren yine geçer
  plan({ id: 'B08', at: 'B08', sahne: 'tren', olcek: 'orta', not: 'Gece treni; ertesi gün öğleden sonra',
    kamera: kamYol([1000, 690, 1.5], [1060, 690, 1.58], u => u),
    durum: st => { const te = A('B08@ertesi') - st.at; return { gun: t => sm(te, te + 1.2, t),
      tren: t => [[300 + 260 * t, 1]] }; } });
  planlar2(M, IMG, FIG, { kamYol, yigin, duser, bademDali, figurBas, yazi, tabloMaske, kareD, mSil });
  // v2: masa planlarının ışığı mekâna ve zamana göre (planın kendi durumu belirtmediyse): gece lamba, gün pencere, bugün soğuk müze
  const MI = { A01b: 'gece', A02: 'gece', A03: 'gece', B01b: 'gun', B05: 'gun', C01: 'gun', C02: 'gun', C10: 'gece', D02: 'gece', D04: 'gece', D07: 'gun', D07b: 'gun', E02: 'gun', F02: 'gun', F03: 'gece', F07: 'gun', G07: 'gun', H03: 'gun', H04: 'gece', H06: 'gun', H09: 'gece', I03: 'bugun', I04: 'bugun' };
  Object.assign(MI, { C08: 'gece', F03b: 'gece', I01: 'gece' });
  for (const p of planlar()) if (MI[p.id]) p.isik = MI[p.id];
  // v3 renk kuralı: Vincent'in tablosu bir kez renklendiyse griye dönmez. Odadaki şövale tablosu (B06'daki ilk renklenmeden sonra) düşük doygunlukta renkli.
  //   Gri, çerçeveli portre siyah-beyaz anma fotoğrafı okunuyordu.
  for (const p of planlar()) if (p.sahne === 'oda' && !p.maske && p.id !== 'A01') p.maske = (st, kam) => tabloMaske(kam, .7, (p.durum && p.durum(st).tablo) || 'oda_otoportre');
}
// kapak.html için: aynı setler ve yardımcılar
export function kapakYardim(M, IMG, FIG) {
  const tabloMaske = (kam, a = 1, k = 'oda_otoportre') => { const c = M.camK(kam, .3), R = TKf(IMG[k]); mRect(c, R[0] - 4, R[1] - 4, R[2] + 8, R[3] + 8, a, 2); };
  const Y = yigin(40, { renk: 'gri', tohum: 70 }), IZ = [];
  return { tabloMaske,
    theo: (t, S) => figurBas(S, FIG.theo_dur, t, [1640, 1240], 900, { gunes: ODA.LAMBA, adim: 2, hava: [.05, .05, .05], havaK: .3 }),
    // v3: kapak B'nin dalı da filmdeki gibi tablodan kesilir
    // kapak boyunda tablodan kesilen dal benekli okunuyor: kapakta çizilmiş dal (v2'de onaylanan kapak)
    cekmeceDurum: () => ({ nesneler: () => Y, ust: (t, S) => { IZ.length = 0; bademDali(S, 700, 1040, -1.0, 1, 3, 1.7, IZ); } }),
    cekmeceMaske: (kam, m) => { const c = M.camK(kam, 0); for (const [x, y, r] of IZ) mDaire(c, x, y, r, 1, 2); } };
}
