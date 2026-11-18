// Sahneler (Mary Stuart): plan listesi. Her plan bir cümleye ya da sözcüğe bağlı (S, Wd, AT); ölçek o.olcek (G geniş, O orta, Y yakın, A ayrıntı, K kart).
// Kurallar: ardışık iki plan aynı ölçekte olmaz; kart ≤ 8 sn; durağan plan yok (her planda kamera ya da sözcüğe bağlı eylem); kırmızı yalnız Mary.
'use strict';
window.GORSEL = {};
for (const k of ['mary_siyah_hacli_tamboy', 'mary_dul_18yy', 'mary_clouet_beyazyas_resim', 'mary_peceli_profil', 'elizabeth_madalya_16yy', 'elizabeth_depasse_1592', 'elizabeth_huys',
  'darnley_17yy', 'mary_darnley_dunkarton', 'evlilik_madalyasi', 'james_dejode_1603', 'james_unite_sikke_1613', 'mary_tamboy_18yy', 'mary_dul_moncornet', 'fotheringhay_sabah_dawe',
  'idam_iln_1861', 'lochleven_feragat', 'lochleven_kacis_rogers', 'lochleven_kacis_sharp', 'lochleven_icinde', 'westminster_mezar_heykeli', 'holyrood_kucuk_oda', 'holyrood_giyinme_odasi',
  'rizzio_cinayeti_taylor', 'rizzio_cinayeti_dickinson', 'bothwell_tutuklama', 'hayali_bulusma_currier', 'mary_reg_scotorum_17yy', 'mary_peceli_18yy']) GORSEL[k] = 'kaynak/gorsel/' + k + '.jpg';
const P = (id, at, fn, olcek, o = {}) => plan(id, at, fn, { olcek, ...o });
const KART = (id, at, lines, o = {}) => P(id, at, kartFn(lines, o), 'K');
const Lq = (text, at, o = {}) => ({ text, at: at == null ? null : AT(at), size: 66, font: 'Cormorant Garamond', italic: true, weight: 600, ...o });
const Ls = (text, at, o = {}) => ({ text, at: at == null ? null : AT(at), size: 30, font: 'Cinzel', spacing: 4, ...o });
// bölüm kartı: önceki cümlenin sonundan başlar; ilk içerik planı S(ilk) + 1,2'de
const BOLUM = { B: ['I', 'Altı Günlük Kraliçe'], C: ['II', 'Siste Dönüş'], D: ['III', 'Görmediği Kuzen'], E: ['IV', 'Holyrood\'daki Gece'], F: ['V', 'Bothwell'], G: ['VI', 'Gölün Ortasındaki Ada'],
  H: ['VII', 'Solway'], I: ['VIII', 'On Dokuz Yıl'], J: ['IX', 'Bira Fıçısındaki Mektuplar'], K: ['X', 'Elizabeth, Elizabeth\'e Karşı'], L: ['XI', 'Kırmızı'], M: ['XII', 'Sonumda Başlangıcım'] };
const SORU = { B: 'Bir arma, iki kuzeni nasıl düşman yaptı?', C: 'Ona inanmayan bir ülkede kraliçe olmak nasıl bir şeydi?', D: 'Hiç karşılaşmadan birbirlerini nasıl tanıdılar?', E: 'Kalbiyle seçtiği adam ona ne yaptı?',
  F: 'Bothwell\'le neden evlendi?', G: 'Bir kraliçe tahtını nasıl kaybeder?', H: 'Neden rakibine sığındı?', I: 'Elizabeth onu neden ne bıraktı ne öldürdü?', J: 'Mektuplarını kim okuyordu?', K: 'O imzayı kim attı?', L: 'Neden kırmızı giydi?', M: 'Peki kim kazandı?' };
function bolumKarti(h) {
  const ids = Object.keys(CUES), i = ids.indexOf(h + '01'), t0 = Math.max(CUES[ids[i - 1]].e + .15, S(h + '01') - 1.7);
  KART('K' + h, t0, [Ls(BOLUM[h][0], null, { size: 34, spacing: 10 }), { text: BOLUM[h][1].toLocaleUpperCase('tr'), size: Math.min(78, Math.round(78 * 17 / BOLUM[h][1].length)), font: 'Cinzel', weight: 700, spacing: 6 }, { text: '', size: 30 }, Lq(SORU[h], t0 + .7, { size: 50, weight: 500 })], { level: 2 });
}
const ILK = h => S(h + '01') + 1.5;    // bölümün ilk içerik planı

// ── ortak çizimler ──
// karanlık oda: arka duvar, zemin, pencere ışığı (o.pencere: [x, y, w, h], dis: pencere dışı fonksiyonu)
function oda(G, st, o = {}) {
  const g = G.g; G.zemin(o.duvar ?? .2);
  const fl = g.createLinearGradient(0, o.zeminY ?? 820, 0, 1080); fl.addColorStop(0, G.gri(o.zeminV ?? .26)); fl.addColorStop(1, G.gri(.1)); g.fillStyle = fl; g.fillRect(-500, o.zeminY ?? 820, 2500, 800);
  // taş derzleri (yumuşak)
  const q = G.rng(o.seed || 21); g.fillStyle = G.gri((o.duvar ?? .2) - .05, .6); for (let i = 0; i < 26; i++) { const y = q() * (o.zeminY ?? 820), x = q() * 1440; g.fillRect(x, y, 80 + q() * 140, 3); }
  if (o.pencere) { const [x, y, w, h] = o.pencere; G.pencere({ x, y, w, h, d: o.derin ?? 70, duvar: o.duvar ?? .2, dis: o.dis || (() => { G.gok(y + h, { ust: .8, alt: .95 }); }) }); }
}
// mum ışığı halkası (yalnız ışık, mum çizilmez)
function isikHalka(G, x, y, r, v = .5) { const g = G.g, lg = g.createRadialGradient(x, y, 0, x, y, r); lg.addColorStop(0, G.gri(1, v)); lg.addColorStop(1, G.gri(1, 0)); g.fillStyle = lg; g.fillRect(x - r, y - r, r * 2, r * 2); }
// kar (pencere dışı)
function kar(G, st, x0, y0, w, h, n = 60) { const g = G.g, q = G.rng(77); g.fillStyle = G.gri(1, .9); for (let i = 0; i < n; i++) { const sp = 20 + q() * 30, x = x0 + ((q() * w + Math.sin(st.t * .7 + i) * 12) % w), y = y0 + ((q() * h + st.t * sp) % h); g.beginPath(); g.arc(x, y, 2 + q() * 3, 0, TAU); g.fill(); } }
// martılar
function martilar(G, st, x0, y0, n, o = {}) { const g = G.g, q = G.rng(o.seed || 4); g.strokeStyle = G.gri(o.v ?? .2); g.lineWidth = o.w ?? 3; g.lineCap = 'round';
  for (let i = 0; i < n; i++) { const x = x0 + q() * 300 + st.lt * (o.hiz ?? 60) * (.8 + q() * .4), y = y0 + q() * 120 + Math.sin(st.t * 1.5 + i) * 6, s = (o.s ?? 14) * (.7 + q() * .6), fl = Math.sin(st.t * 7 + i * 2) * .35;
    g.beginPath(); g.moveTo(x - s, y - s * (.3 + fl)); g.quadraticCurveTo(x - s * .4, y - s * .45, x, y); g.quadraticCurveTo(x + s * .4, y - s * .45, x + s, y - s * (.3 + fl)); g.stroke(); } }

// ════════ A · KIRMIZI VE DENİZ (kanca) ════════
// A01: siyah elbiseli Mary (Finden, 19. yy); kamera yakadan eteğe iner, kırmızı alttan yükselir
// Finden gravürünün sol altındaki ek resim idam anını (balta, kütük) gösterir: hiçbir planda görünmez
const ORT_IDAM = [[.226, .528, .372, .672]];
const SIYAH_ETEK = [[.405, .51], [.45, .525], [.5, .545], [.55, .525], [.585, .51], [.574, .57], [.565, .63], [.63, .642], [.655, .69], [.672, .758], [.5, .762], [.36, .758], [.372, .69], [.385, .62], [.395, .56]];
const SIYAH_CIKAR = [[[.519, .6105], [.556, .5765], [.59, .581], [.652, .572], [.652, .63], [.59, .629], [.5645, .638], [.551, .638], [.519, .6165]]];   // kitap ve parmaklar sıkı sınırla (dikdörtgen kesik gri kutu gibi okunuyordu)   // kitap ve el: kırmızı değmez (kan gibi okunur)
P('A01', 0, fotoP('mary_siyah_hacli_tamboy', [.545, .41, .36], [.535, .6, .4], {
  klip: [.232, .242, .765, .762], ort: ORT_IDAM, kontrast: 1.45, parlak: .93, renkTon: 'brightness(2.6) contrast(.95)', u: st => ss((st.t - 1.3) / 4.2),
  kirmizi: { poly: SIYAH_ETEK, cikar: SIYAH_CIKAR, yum: 12, sil: st => ss((st.t - AT('A01@altından')) / 1.8) }, karart: st => 1 - clamp(st.t / .9),
  kunye: 'E. F. Finden, 19. yy gravürü · The Met (CC0)', look: { sepia: .16, strength: .34 } }), 'O');
P('A02', 'A02', fotoP('mary_dul_18yy', [.5, .4, .72], [.5, .34, .46], {
  etiket: [{ text: 'MARY STUART', size: 70, weight: 700, spacing: 8, at: S('A02') + .2 }, { text: 'İskoçya Kraliçesi  ·  8 Şubat 1587', size: 40, font: 'Cormorant Garamond', italic: true, weight: 600, at: AT('A02@şubat') - .3 }],
  kunye: '18. yy (?) gravürü · The Met (CC0)' }), 'Y');
// A03: Solway, şafak; küçük balıkçı teknesi İngiltere kıyısına geçer
function solway(G, st, o = {}) {
  const g = G.g, ufuk = o.ufuk ?? 560, cam = o.cam || [720, 540, 1]; G.kamera(...cam);
  G.gok(ufuk, { ust: o.gokUst ?? .5, alt: .93, isik: o.isik || [1050, ufuk - 40, 480, 1] });
  G.bulutlar(150, ufuk - 70, { seed: o.seed || 3, drift: st.t * 6, govde: .5, n: 5 });
  const sis = o.sis ?? 0;
  G.kiyi(700, 2200, ufuk + 2, 95, { seed: 7, v: lerp(.52, .78, sis), d0: .05, d1: .8, k: 3 });       // İngiltere (uzak)
  G.kiyi(-700, 520, ufuk + 6, 150, { seed: 2, v: .22, d0: .2, d1: 1.1, k: 5 });                     // İskoçya (yakın, koyu)
  G.deniz(ufuk, 1080, { t: st.t, ufuk: .82, on: .34, yansima: [o.isik ? o.isik[0] : 1050, 220, .97], n: 110 });
}
P('A03', 'A03', (G, st) => {
  const sis = 1 - acS(st, 'A03@ülkesine', 2.2), bx = 470 + st.lt * 48;
  solway(G, st, { cam: [lerp(620, 860, eio(st.p)), 560, 1.0], sis, ufuk: 500, isik: [1180, 470, 520, 1] });
  G.tekne({ x: bx, y: 760, s: 520, f: 1, t: st.t, oar: st.t * .9, sail: 0, kisi: [
    { kind: 'erkek', x: .3, h: .3, poz: 'otur', kol: 'kurek', f: -1 }, { kind: 'erkek', x: .1, h: .3, poz: 'otur', kol: 'kurek', f: -1 },
    { kind: 'mary', x: -.2, h: .4, poz: 'otur', kol: 'onde', f: 1, kirmizi: 'etek', veil: .8, veilA: .6 }, { kind: 'erkek', x: -.4, h: .42, kol: 'yan', f: 1, sakal: true }] });
  dalgaOn(G, st, 900, 1080);
  martilar(G, st, 280, 200, 4, { hiz: 70, v: .25 });
  return { look: { sepia: .12, strength: .36 } };
}, 'G');
// ön plan dalgaları (koyu sırtlar)
function dalgaOn(G, st, y0, y1) { const g = G.g, q = G.rng(31); for (let i = 0; i < 14; i++) { const u = q(), y = lerp(y0, y1, u), x = ((q() * 2200 + st.t * (20 + u * 30)) % 2200) - 300, w = lerp(160, 420, u);
  g.fillStyle = G.gri(.2 + q() * .1, .8); g.beginPath(); g.moveTo(x - w, y); g.quadraticCurveTo(x - w * .3, y - 18 - u * 22, x, y - 6); g.quadraticCurveTo(x + w * .4, y - 14, x + w, y + 4); g.lineTo(x - w, y + 8); g.closePath(); g.fill(); } }
// A04: harita: "Fransa'ya git" (soluk, kesik) ve Solway'den İngiltere'ye kırmızı yol
const FRANSA_YOLU = [[-3.95, 54.76], [-4.7, 54.3], [-5.25, 53.2], [-5.55, 52.0], [-5.9, 50.6], [-5.1, 49.7], [-3.4, 49.25], [-2.1, 48.95]];
const SOLWAY_YOLU = [[-3.95, 54.79], [-3.78, 54.72], [-3.57, 54.65]];
P('A04', 'A04', (G, st) => { harita(G, st, { k0: [-4.2, 53.2, 1.0], k1: [-3.9, 54.4, 1.9], u: eio(st.p),
  yollar: [{ pts: FRANSA_YOLU, p: acS(st, 'A04@fransaya', 2.2), kesik: true, v: .35, alfa: lerp(.9, .45, acS(st, 'A04@rakibine', .6)) }, { pts: SOLWAY_YOLU, p: acS(st, 'A04@rakibine', 1.2), kirmizi: true, w: 10 }],
  yazilar: [['İSKOÇYA', -4.3, 56.6, 34], ['İNGİLTERE', -1.6, 52.6, 34], ['FRANSA', 0.2, 48.3, 34], ['SOLWAY', -4.4, 54.45, 24, acS(st, 'A04@rakibine', 1)]], isaretler: [{ yer: 'dundrennan', kirmizi: true }] });
  return { look: { sepia: .3, strength: .26 } }; }, 'A');
// A05: iki yüz, iki kesme: Mary sağa, Elizabeth sola bakar; aynı karede hiç değil
P('A05', 'A05', fotoP('mary_peceli_profil', [.5, .4, .62], [.54, .36, .52], { kunye: 'Mary Stuart · 18. yy gravürü · The Met (CC0)' }), 'Y');
P('A05b', AT('A05@kez') - .1, fotoP('elizabeth_madalya_16yy', [.5, .42, .58], [.46, .44, .5], { kunye: 'I. Elizabeth · 16. yy madalyası · The Met (CC0)', parlak: 1.1 }), 'Y');
KART('A06', 'A06', [Ls('Stefan Zweig\'ın anlattığı hikâye · Maria Stuart (1935)', S('A06'), { size: 28 }), { text: '', size: 24 }, Lq('Biri kalbiyle yaşar,', 'A06@kalbiyle', { size: 76 }), Lq('öteki aklıyla.', 'A06@aklıyla', { size: 76 }), { text: '', size: 24 }, { text: 'SEN HANGİSİSİN?', size: 46, font: 'Cinzel', weight: 700, spacing: 6, at: AT('A06@sen') }]);
// A07 + B01 + B03: beşik (Linlithgow, Aralık 1542); kış penceresi, mum
function besikOda(G, st, o = {}) {
  const cam = o.cam || [720, 560, 1]; G.kamera(...cam);
  oda(G, st, { duvar: .17, zeminY: 800, pencere: [1060, 170, 300, 470], derin: 90, dis: () => { G.gok(640, { ust: .62, alt: .86 }); G.kiyi(900, 1500, 640, 120, { v: .78, seed: 5 }); if (o.kar !== false) kar(G, st, 900, 160, 320, 500, 50); } });
  isikHalka(G, 440, 520, 520, .38);
  G.mum(300, 820, 150, st.t, { r: 600 });
  G.dik(220, 820, 160, 24, .12);
  besik(G, { x: 720, y: 890, s: 560, t: st.t, salla: o.salla ?? .02, bebek: o.bebek });
}
P('A07', 'A07', (G, st) => { besikOda(G, st, { cam: [720, 600, lerp(1, 1.06, st.p)] }); return { iris: ss(st.lt / 1.4), irisX: 720, irisY: 650, look: { sepia: .28, strength: .3 } }; }, 'O');

// ════════ B · ALTI GÜNLÜK KRALİÇE ════════
bolumKarti('B');
P('B01', ILK('B'), (G, st) => { besikOda(G, st, { cam: [700, 700, lerp(1.45, 1.55, st.p)] }); return { look: { sepia: .28, strength: .3 } }; }, 'Y');
// B02: Solway Moss, kış: kırık mızraklar, yırtık sancak, kuzgunlar
function bataklik(G, st, o = {}) {
  const g = G.g; G.kamera(...(o.cam || [720, 540, 1]));
  G.gok(600, { ust: .48, alt: .8 }); G.bulutlar(120, 520, { seed: 9, drift: st.t * 4, govde: .45, ufukV: .7 });
  G.kiyi(-400, 1900, 602, 40, { v: .55, seed: 3, k: 6 });
  const gr = g.createLinearGradient(0, 600, 0, 1080); gr.addColorStop(0, G.gri(.7)); gr.addColorStop(1, G.gri(.35)); g.fillStyle = gr; g.fillRect(-500, 600, 2500, 600);
  const q = G.rng(14);
  for (let i = 0; i < 40; i++) { const x = q() * 1600 - 80, y = 620 + Math.pow(q(), 1.5) * 460, w = 60 + q() * 200; g.fillStyle = G.gri(q() < .5 ? .88 : .3, .7); g.beginPath(); g.ellipse(x, y, w, w * .06 + 2, 0, 0, TAU); g.fill(); }   // su birikintileri ve otlar
  g.strokeStyle = G.gri(.12); g.lineCap = 'round';
  for (const [x, y, a, L] of [[300, 900, -.5, 420], [420, 930, -.2, 380], [980, 880, .6, 300], [1150, 950, -.9, 260], [760, 990, .3, 340]]) { g.lineWidth = 7; g.beginPath(); g.moveTo(x, y); g.lineTo(x + Math.sin(a) * L, y - Math.cos(a) * L); g.stroke(); }
  // yırtık sancak (rüzgârda)
  const bx = 300 + Math.sin(-.2) * 380, by = 930 - Math.cos(-.2) * 380, wv = k => Math.sin(st.t * 2.2 + k * 2) * 18 * k;
  g.lineWidth = 6; g.beginPath(); g.moveTo(bx - 10, by + 4); g.lineTo(bx + 150, by + 40); g.stroke();    // çapraz çubuk
  g.fillStyle = G.gri(.3); g.fill(G.pathOf([[bx - 6, by + 6], [bx + 146, by + 40], [bx + 150 + wv(.4), by + 150], [bx + 120 + wv(.7), by + 230], [bx + 95 + wv(.8), by + 190], [bx + 70 + wv(1), by + 260], [bx + 40 + wv(.8), by + 200], [bx + 10 + wv(.6), by + 240], [bx - 4 + wv(.3), by + 140]], true, .4));
  // kuzgunlar
  martilar(G, st, 200, 260, 3, { hiz: 35, v: .1, w: 5, s: 22, seed: 8 });
}
P('B02', 'B02', (G, st) => { bataklik(G, st, { cam: [lerp(760, 680, eio(st.p)), 560, 1.05] }); return { look: { sepia: .1, strength: .45 }, ust: etiket([{ text: 'Solway Moss savaşı · 24 Kasım 1542', size: 34, font: 'Cormorant Garamond', italic: true, at: AT('B02@savaşı') - .2 }], { y: 120 }) }; }, 'G');
// B02b: kralın yatağı (Falkland); B03'te mum söner
P('B02b', 'B02@kral', (G, st) => {
  // kralın tacı yastıkta, yanında mum; "ölür"de mum söner, duman yükselir
  const g = G.g; G.kamera(720, 600, lerp(1, 1.1, st.p)); G.zemin(.07);
  const son = acS(st, 'B03@ölür', 1.0), x = 1000, y = 860;
  isikHalka(G, x, y - 260, lerp(1000, 260, son), .6);
  g.fillStyle = G.gri(.16); g.fillRect(-200, 860, 1900, 400);
  const yg = g.createLinearGradient(380, 0, 900, 0); yg.addColorStop(0, G.gri(.18)); yg.addColorStop(1, G.gri(lerp(.55, .25, son))); g.fillStyle = yg;
  g.fill(G.pathOf([[360, 860], [400, 790], [520, 770], [700, 772], [840, 790], [880, 860], [800, 880], [440, 880]], true, .6));      // yastık
  tac(G, 620, 790, 300, { v: lerp(.42, .22, son) });
  if (son < 1) G.mum(x, y, 240, st.t, { r: 10 }); else G.dik(x - 20, y - 240, 40, 240, .6);
  if (son > 0) { const k = st.t - AT('B03@ölür'); for (let i = 0; i < 3; i++) { g.fillStyle = G.gri(.75, .45 * (1 - clamp((k - i * .3) / 2.4))); g.beginPath(); g.ellipse(x + Math.sin(st.t * 2 + i) * 14, y - 320 - k * 50 - i * 40, 16 + i * 6, 46, Math.sin(st.t + i) * .3, 0, TAU); g.fill(); } }
  return { look: { sepia: .2, strength: .38 } };
}, 'A');
P('B03b', 'B03@meri', (G, st) => { besikOda(G, st, { cam: [720, 760, 1.6] }); const k = acS(st, 'B03@kraliçe', 1.4); tac(G, 720, lerp(380, 770, k), 150, { v: .3, rot: (1 - k) * .2 }); return { look: { sepia: .26, strength: .3 } }; }, 'Y');
// B04: harita: Dumbarton'dan Roscoff'a (1548); sonra Fransız sarayı, dans
const ROSCOFF_YOLU = [[-4.6, 55.9], [-5.0, 55.4], [-5.3, 54.6], [-5.4, 53.3], [-5.7, 52.0], [-6.0, 50.6], [-5.2, 49.7], [-3.98, 48.9]];
P('B04', 'B04', (G, st) => { harita(G, st, { k0: [-4.3, 54.5, 1.15], k1: [-3.3, 51.0, 1.15], yollar: [{ pts: ROSCOFF_YOLU, p: acS(st, 'B04@yaşında', 2.6) }],
  yazilar: [['İSKOÇYA', -4.3, 56.6, 34], ['FRANSA', 0.2, 48.3, 34], ['1548', -6.7, 51.3, 30, acS(st, 'B04@fransaya', 1)]] }); return { look: { sepia: .3, strength: .26 } }; }, 'A');
function salon(G, st, o = {}) {
  const g = G.g; G.kamera(...(o.cam || [720, 540, 1])); G.zemin(o.duvar ?? .3);
  const y0 = o.zeminY ?? 760, n = o.pencere ?? 4;
  for (let i = 0; i < n; i++) { const x = 180 + i * (1080 / Math.max(1, n - 1)); g.fillStyle = G.gri(o.pencereV ?? .88); g.beginPath(); g.moveTo(x - 60, y0 - 120); g.lineTo(x - 60, 220); g.arc(x, 220, 60, Math.PI, 0); g.lineTo(x + 60, y0 - 120); g.closePath(); g.fill();
    g.strokeStyle = G.gri(.4); g.lineWidth = 4; g.beginPath(); g.moveTo(x, 160); g.lineTo(x, y0 - 120); g.moveTo(x - 60, 420); g.lineTo(x + 60, 420); g.stroke();
    if (o.huzme !== false) { g.save(); g.globalAlpha = .18; g.fillStyle = G.gri(1); g.beginPath(); g.moveTo(x - 60, 300); g.lineTo(x + 60, 260); g.lineTo(x + 260, 1080); g.lineTo(x + 20, 1080); g.closePath(); g.fill(); g.restore(); } }
  const fl = g.createLinearGradient(0, y0, 0, 1080); fl.addColorStop(0, G.gri(o.zeminV ?? .5)); fl.addColorStop(1, G.gri(.22)); g.fillStyle = fl; g.fillRect(-600, y0, 2700, 600);
  g.strokeStyle = G.gri(.35, .6); g.lineWidth = 2; for (let i = -12; i <= 12; i++) { g.beginPath(); g.moveTo(720 + i * 60, y0); g.lineTo(720 + i * 220, 1080); g.stroke(); }
  g.fillStyle = G.gri(.15); g.fillRect(-600, 60, 2700, 30); for (let i = 0; i < 9; i++) g.fillRect(i * 180 - 20, 60, 22, 90);   // tavan kirişi
}
P('B04b', 'B04@şiir', (G, st) => {
  salon(G, st, { cam: [lerp(640, 800, eio(st.p)), 560, 1.05], duvar: .36, zeminV: .55 });
  const ph = st.t * .4;
  for (const [cx0, y, sc, k] of [[980, 790, .62, 3], [420, 800, .66, 2], [700, 860, .82, 1], [260, 930, 1, 0], [1130, 935, 1, 4]]) {
    const a = ph * TAU * .25 + k, cx = cx0 + Math.sin(a) * 24 * sc, d = 64 * sc * Math.cos(a * .7);
    G.figur({ kind: 'kadin', x: cx - 70 * sc, y, s: 330 * sc, f: 1, poz: 'yuru', walk: ph + k * .3, kol: 'uzat', t: st.t, v: .12 + (1 - sc) * .2 });
    G.figur({ kind: 'erkek', x: cx + 70 * sc, y: y + 4, s: 350 * sc, f: -1, poz: 'yuru', walk: ph + k * .3 + .5, kol: 'uzat', t: st.t, v: .1 + (1 - sc) * .2 }); }
  return { look: { sepia: .34, strength: .26 }, exposure: 1.05 };
}, 'G');
// B05: evlilik madalyası (1558) masada; büyüteç François ve Mary'nin çift portresine
P('B05', 'B05', masaP('evlilik_madalyasi', { boy: 980, k0: [720, 520, 1.05], k1: [640, 420, 1.35], lens: { at: 'B05@veliahtla', u: [.355, .23], z: 2.4, r: 200 }, kunye: 'Evlilik madalyası (1558), J. West\'in 1849 baskısı · The Met (CC0)' }), 'A');
// B06–B08: arma; İngiltere'nin arması eklenir (kırmızı: Mary'nin iddiası)
P('B06', 'B06', (G, st) => {
  const g = G.g; G.kamera(720, 540, lerp(1, 1.08, st.p)); G.zemin(.22); isikHalka(G, 720, 420, 700, .35);
  arma(G, 720, 580, 520, 640, { ing: acS(st, 'B06@kraliyet', 1.6), ingKirmizi: acS(st, 'B06@anlamı', 1.4), tac: acS(st, 'B06@gerçek', 1.2) });
  return { look: { sepia: .24, strength: .3 } };
}, 'Y');
P('B07', 'B07', masaP('elizabeth_depasse_1592', { boy: 1000, rot: .02, k0: [720, 560, .95], k1: [720, 380, 1.5], kunye: 'I. Elizabeth · Crispijn de Passe, 1592 · The Met (CC0)' }), 'O');
// B08: imzasız antlaşma (Edinburgh, 1560); tüy kalem iner, imzalamadan kalkar; kırmızı damla
function belge(G, st, o = {}) {
  const g = G.g; G.zemin(.2); isikHalka(G, 620, 360, 800, .4);
  g.save(); g.translate(720, 560); g.rotate(o.rot ?? -.03);
  BOYA.golge(g, -420, -480, 860, 1000, .6);
  g.fillStyle = G.gri(.94); g.fillRect(-440, -500, 860, 1000);
  g.fillStyle = G.gri(.2); g.font = '600 46px "Cinzel"'; g.textAlign = 'center'; g.fillText(o.baslik || 'TRACTATUS', 0, -400);
  g.font = 'italic 500 32px "Cormorant Garamond"'; g.textAlign = 'left'; const q = G.rng(o.seed || 3);
  for (let i = 0; i < (o.satir ?? 11); i++) { let x = -360; while (x < 330) { const w = 30 + q() * 90; g.fillStyle = G.gri(.32, .85); g.fillRect(x, -330 + i * 46, w, 5); x += w + 14; } }
  g.strokeStyle = G.gri(.25); g.lineWidth = 3; g.beginPath(); g.moveTo(-60, 330); g.lineTo(340, 330); g.stroke();
  if (o.imza) { g.fillStyle = G.gri(.12); g.font = 'italic 600 58px "Cormorant Garamond"'; g.save(); g.beginPath(); g.rect(-60, 240, 420 * clamp(o.imza), 120); g.clip(); g.fillText(o.imzaYazi || 'Elizabeth R', -40, 320); g.restore(); }
  g.restore();
}
function kalem(G, x, y, a = -.6, s = 1) { const g = G.g; g.save(); g.translate(x, y); g.rotate(a); g.scale(s, s); g.fillStyle = G.gri(.82); g.fill(G.pathOf([[0, 0], [8, -60], [26, -220], [40, -420], [18, -470], [-6, -400], [-14, -220], [-8, -60]], true, .6)); g.strokeStyle = G.gri(.3); g.lineWidth = 3; g.beginPath(); g.moveTo(0, 0); g.lineTo(16, -440); g.stroke(); g.fillStyle = G.gri(.1); g.fill(G.pathOf([[0, 0], [4, -24], [-4, -24]], true, .2)); g.restore(); }
P('B08', 'B08', (G, st) => {
  G.kamera(720, lerp(560, 640, eio(st.p)), lerp(1, 1.25, eio(st.p)));
  belge(G, st, { baslik: 'EDINBURGH · 1560' });
  const in1 = acS(st, 'B08@imzalasın', 1.2), up = acS(st, 'B08@hiç', 1.0); kalem(G, 820 + up * 140, lerp(230, 860, in1) - up * 420, -.5);
  const d = acS(st, 'B08@bedelini', 1.6);
  if (d > 0) { const y = lerp(300, 840, Math.min(1, d * 1.4)); G.kirmiziCiz(r => { r.beginPath(); if (d < .7) r.ellipse(900, y, 9, 14, 0, 0, TAU); else r.ellipse(900, 850, lerp(10, 40, (d - .7) / .3), lerp(10, 28, (d - .7) / .3), 0, 0, TAU); r.fill(); }); G.g.fillStyle = G.gri(.4); G.g.beginPath(); G.g.ellipse(900, d < .7 ? y : 850, d < .7 ? 9 : lerp(10, 40, (d - .7) / .3), d < .7 ? 14 : lerp(10, 28, (d - .7) / .3), 0, 0, TAU); G.g.fill(); }
  return { look: { sepia: .3, strength: .28 } };
}, 'A');
// B09: beyaz yas (Clouet'den sonra, 1560)
P('B09', 'B09', fotoP('mary_clouet_beyazyas_resim', [.5, .42, .95], [.53, .33, .6], { kunye: 'Beyaz yas içinde Mary · Clouet\'nin 1561 portresinden kopya · NGS (kamu malı)', kontrast: 1.05 }), 'Y');
// B10: Calais, Ağustos 1561: kadırga açılır; uzakta bir gemi batar
P('B10', 'B10', (G, st) => {
  const g = G.g, ufuk = 600; G.kamera(lerp(820, 640, eio(st.p)), 540, 1.02);
  G.gok(ufuk, { ust: .58, alt: .92, isik: [400, 520, 380, 1] }); G.bulutlar(160, 520, { seed: 6, drift: st.t * 5 });
  G.deniz(ufuk, 1080, { t: st.t, ufuk: .8, on: .4, n: 100, yansima: [400, 160, .95] });
  // Calais iskelesi ve kale (sağda)
  kale(G, 1080, ufuk + 4, 520, [{ t: 'sur', x: .6, w: 1.2, h: .14 }, { x: .08, w: .12, h: .3, cati: 'konik' }, { x: .38, w: .1, h: .26, cati: 'konik' }, { x: .62, w: .16, h: .5, cati: 'mazgal' }, { x: .55, w: .05, h: .62, cati: 'sivri', ch: .25 },
    { x: .9, w: .12, h: .34, cati: 'konik' }, { t: 'ev', x: .26, w: .14, h: .2, cati: 'beşik' }, { t: 'ev', x: .78, w: .12, h: .18, cati: 'beşik' }, { x: 1.06, w: .08, h: .7, cati: 'sivri', ch: .35 }], { v: .3, isik: .55 });
  g.fillStyle = G.gri(.18); g.fillRect(960, ufuk + 40, 700, 26); for (let i = 0; i < 9; i++) g.fillRect(980 + i * 80, ufuk + 60, 12, 120);
  const b = acS(st, 'B10@battığını', 3.5); karaka(G, { x: 360, y: ufuk + 6, s: 110, b, v: .45 });
  kadirga(G, { x: 900 - st.lt * 26, y: 780, s: 760, f: -1, t: st.t, yelken: .5, kisi: [{ kind: 'mary', x: -.43, h: .17, kol: 'yan', veil: .9, f: -1 }, { kind: 'kadin', x: -.38, h: .15, f: -1 }] });
  return { look: { sepia: .18, strength: .32 }, ust: etiket([{ text: 'Calais · Ağustos 1561', size: 34, font: 'Cormorant Garamond', italic: true, at: S('B10') + .4 }], { y: 120 }) };
}, 'G');
P('B10b', 'B10@brantom', (G, st) => { const g = G.g, ufuk = 600; G.kamera(360, 560, 2.4); G.gok(ufuk, { ust: .58, alt: .92, isik: [400, 520, 380, 1] }); G.bulutlar(160, 520, { seed: 6, drift: st.t * 5 });
  G.deniz(ufuk, 1080, { t: st.t, ufuk: .8, on: .4, n: 100, yansima: [400, 160, .95] }); karaka(G, { x: 360, y: ufuk + 6, s: 110, b: acS(st, 'B10@battığını', 3.5), v: .4 });
  return { look: { sepia: .18, strength: .34 } }; }, 'A');
// B11: kıçta Mary, uzaklaşan Fransa kıyısı; sonra "Elveda Fransa"
P('B11', 'B11', (G, st) => {
  const g = G.g, ufuk = 520; G.kamera(720, 560, lerp(1, 1.1, st.p));
  G.gok(ufuk, { ust: .55, alt: .9, isik: [1100, 480, 420, .98] }); G.bulutlar(140, 460, { seed: 12, drift: st.t * 3 });
  G.kiyi(700, 1700, ufuk + 2, lerp(60, 30, st.p), { v: lerp(.5, .7, st.p), seed: 9, k: 4 });
  G.deniz(ufuk, 1080, { t: st.t, ufuk: .82, on: .36, n: 90, yansima: [1100, 160, .95] });
  g.fillStyle = G.gri(.14); g.fill(G.pathOf([[-100, 820], [500, 800], [760, 760], [900, 700], [940, 720], [820, 830], [600, 900], [-100, 1100]], true, .5));   // kıç küpeştesi
  g.fillStyle = G.gri(.5); g.fill(G.pathOf([[-100, 560], [200, 520], [520, 540], [560, 600], [-100, 640]], true, .5));   // tente
  g.strokeStyle = G.gri(.12); g.lineWidth = 10; g.beginPath(); g.moveTo(540, 560); g.lineTo(560, 820); g.stroke();
  G.figur({ kind: 'mary', x: 640, y: 830, s: 480, f: 1, kol: 'pencere', t: st.t, veil: .95, wind: .8, v: .1, lean: .08 });
  return { look: { sepia: .2, strength: .32 } };
}, 'O');
KART('B11k', AT('B11@elveda') - .25, [Lq('“Elveda Fransa.', 'B11@elveda', { size: 84 }), Lq('Seni bir daha göremeyeceğim.”', AT('B11@seni') - .1, { size: 72 }), { text: '', size: 24 }, Ls('Brantôme\'un anlattığı · 1561', AT('B11@elveda') + 1.2, { size: 26 })], { level: 2 });
P('B12', 'B12', (G, st) => {
  const g = G.g, ufuk = 560; G.kamera(720, 540, lerp(1.05, 1, st.p));
  G.gok(ufuk, { ust: .62, alt: .88 }); G.bulutlar(160, 500, { seed: 13, drift: st.t * 3, ufukV: .86 });
  const k = acS(st, 'B12', 2.2); G.kiyi(500, 1100, ufuk + 2, 26, { v: lerp(.62, .86, k), seed: 9, k: 4 });
  G.deniz(ufuk, 1080, { t: st.t, ufuk: .84, on: .45, n: 80 });
  const sis = g.createLinearGradient(0, ufuk - 200, 0, ufuk + 200); sis.addColorStop(0, G.gri(.88, 0)); sis.addColorStop(.5, G.gri(.9, .4 + .5 * k)); sis.addColorStop(1, G.gri(.88, 0)); g.fillStyle = sis; g.fillRect(-500, ufuk - 200, 2500, 400);
  return { look: { sepia: .16, strength: .3 }, karart: clamp((st.t - (S('C01') - .9)) / .8) };
}, 'G');

// ════════ C · SİSTE DÖNÜŞ ════════
bolumKarti('C');
// C01: Leith, sis; gemi rıhtıma yanaşır, kıyıda birkaç kişi
P('C01', ILK('C'), (G, st) => {
  const g = G.g, ufuk = 560; G.kamera(lerp(760, 660, eio(st.p)), 560, 1.04);
  G.gok(ufuk, { ust: .7, alt: .86 }); G.deniz(ufuk, 1080, { t: st.t, ufuk: .82, on: .55, n: 60 });
  kale(G, 900, ufuk + 6, 600, [{ t: 'sur', x: .5, w: 1.3, h: .1 }, { t: 'ev', x: .2, w: .18, h: .2, cati: 'beşik' }, { t: 'ev', x: .45, w: .15, h: .24, cati: 'beşik' }, { x: .7, w: .1, h: .4, cati: 'mazgal' }, { t: 'ev', x: 1, w: .2, h: .18, cati: 'beşik' }], { v: .5, isik: .62 });
  g.fillStyle = G.gri(.35); g.fillRect(700, ufuk + 60, 1200, 40); for (let i = 0; i < 10; i++) g.fillRect(720 + i * 110, ufuk + 90, 14, 160);
  ordu(G, st, { x0: 900, x1: 1300, y: ufuk + 62, s: 70, n: 9, v: .4, mizrak: 0 });
  karaka(G, { x: 500 + st.lt * 10, y: 780, s: 420, v: .3 });
  sis(G, st, 380, 900, .55 + .2 * (1 - st.p), { n: 10 });
  return { look: { sepia: .12, strength: .36 }, ust: etiket([{ text: 'Leith · 19 Ağustos 1561', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) };
}, 'G');
// C02: Knox kürsüde (siluet), sonra sözleri
function kilise(G, st, o = {}) {
  const g = G.g; G.kamera(...(o.cam || [720, 540, 1])); G.zemin(.24);
  for (let i = 0; i < 4; i++) { const x = 150 + i * 380; g.fillStyle = G.gri(.14); g.fillRect(x - 40, 120, 80, 900); g.fillStyle = G.gri(.34); g.fillRect(x - 40, 120, 22, 900);
    g.strokeStyle = G.gri(.14); g.lineWidth = 34; g.beginPath(); g.arc(x + 190, 330, 190, Math.PI, 0); g.stroke(); }
  const w = g.createRadialGradient(720, 200, 20, 720, 200, 700); w.addColorStop(0, G.gri(.95, .55)); w.addColorStop(1, G.gri(.9, 0)); g.fillStyle = w; g.fillRect(0, 0, 1440, 1080);
}
P('C02', 'C02', (G, st) => {
  const g = G.g; kilise(G, st, { cam: [760, 520, lerp(1, 1.1, st.p)] });
  g.fillStyle = G.gri(.12); g.fill(G.polyP([[880, 640], [1120, 640], [1090, 880], [910, 880]])); g.fillRect(860, 620, 280, 30); g.fillRect(975, 880, 50, 200);   // kürsü
  G.figur({ kind: 'erkek', x: 1000, y: 760, s: 420, f: -1, kol: ac(st, 'C02@yazacaktı') > 0 ? 'kaldir' : 'uzat', t: st.t, sakal: true, sapka: false, pelerin: true, v: .08 });
  for (let i = 0; i < 9; i++) { const x = 120 + i * 150, y = 1000 + (i % 2) * 30; g.fillStyle = G.gri(.06); g.beginPath(); g.arc(x, y - 70, 42, 0, TAU); g.fill(); g.fillRect(x - 70, y - 40, 140, 200); }   // cemaat (arkadan)
  return { look: { sepia: .14, strength: .4 } };
}, 'O');
KART('C02k', AT('C02@gökyüzü') + .2, [Lq('“Gökyüzü bile, bu ülkeye', 'C02@gökyüzü', { size: 62 }), Lq('ne getirildiğini söylüyordu:', 'C02@ne', { size: 62 }), Lq('keder, acı, karanlık…”', 'C02@keder', { size: 72 }), { text: '', size: 22 }, Ls('John Knox · Reformasyon Tarihi', AT('C02@gökyüzü') + 1, { size: 26 })]);
// C03: sisin içinde atlılar
P('C03', 'C03', (G, st) => {
  const g = G.g; G.kamera(720, 560, 1); G.zemin(.82);
  G.kamera(720, 700, 1.3); for (let i = 0; i < 5; i++) { const x = 300 + i * 230 + st.lt * 30, y = 820 + (i % 2) * 20; at(G, { x, y, s: 300 - i * 10, f: 1, ph: st.t * 1.2 + i * .23, dur: true, v: lerp(.25, .6, i / 5), binici: { kind: i === 2 ? 'mary' : 'erkek', veil: .9, v: lerp(.25, .6, i / 5) } }); }
  sis(G, st, 500, 1000, .75, { n: 14, v: .84 }); sis(G, st, 200, 700, .5, { n: 8, v: .86, seed: 9 });
  return { look: { sepia: .1, strength: .32 } };
}, 'O');
// C04: Edinburgh: kale kayası ve şehir
P('C04', 'C04', (G, st) => {
  const g = G.g, ufuk = 640; G.kamera(lerp(640, 800, eio(st.p)), 540, 1.02);
  G.gok(ufuk, { ust: .5, alt: .82 }); G.bulutlar(140, 520, { seed: 17, drift: st.t * 5 });
  g.fillStyle = G.gri(.3); g.fill(G.pathOf([[100, ufuk], [180, 420], [300, 360], [480, 350], [560, 400], [600, ufuk]], true, .5));    // kale kayası
  kale(G, 200, 380, 400, [{ x: .35, w: .5, h: .18 }, { x: .25, w: .12, h: .32, cati: 'mazgal' }, { x: .6, w: .1, h: .26 }], { v: .22 });
  kale(G, 560, ufuk, 700, [{ t: 'ev', x: .1, w: .14, h: .25, cati: 'beşik', pen: 3 }, { t: 'ev', x: .28, w: .16, h: .3, cati: 'beşik', pen: 3 }, { x: .5, w: .1, h: .55, cati: 'sivri', ch: .3 }, { t: 'ev', x: .7, w: .2, h: .26, cati: 'beşik', pen: 4 }, { t: 'ev', x: .95, w: .2, h: .22, cati: 'beşik', pen: 3 }, { x: 1.2, w: .12, h: .3, cati: 'konik' }], { v: .26 });
  g.fillStyle = G.gri(.42); g.fillRect(-200, ufuk, 1900, 500);
  return { look: { sepia: .16, strength: .34 } };
}, 'G');
P('C05', 'C05', fotoP('mary_reg_scotorum_17yy', [.5, .45, .9], [.5, .38, .62], { kunye: 'Maria Reg: Scotorum · 17. yy (?) gravürü · The Met (CC0)' }), 'Y');
P('C05b', 'C05@kendi', (G, st) => {
  const g = G.g; G.kamera(720, 600, lerp(1, 1.08, st.p)); oda(G, st, { duvar: .13, zeminY: 860 });
  g.fillStyle = G.gri(.32); g.fillRect(420, 600, 600, 260); g.fillStyle = G.gri(.75); g.fillRect(400, 580, 640, 30);   // sunak, örtü
  for (const x of [520, 920]) G.mum(x, 580, 180, st.t + x, { r: 420 });
  g.fillStyle = G.gri(.55); g.beginPath(); g.moveTo(560, 200); g.lineTo(560, 480); g.lineTo(880, 480); g.lineTo(880, 200); g.arc(720, 200, 160, 0, Math.PI, true); g.fill();     // küçük pencere ışığı
  G.figur({ kind: 'mary', x: 600, y: 1000, s: 480, f: 1, poz: 'diz', kol: 'dua', t: st.t, veil: .95, v: .1 });
  return { look: { sepia: .3, strength: .3 } };
}, 'O');
// C06: pencerede Mary, güneye bakar
P('C06', 'C06', (G, st) => {
  const g = G.g; G.kamera(760, 520, lerp(1.25, 1.35, st.p));
  G.pencere({ x: 980, y: 140, w: 420, h: 640, d: 120, duvar: .14, dis: () => { G.gok(560, { ust: .72, alt: .95, isik: [1100, 520, 300, 1] }); G.kiyi(700, 1400, 560, 70, { v: .6, seed: 3 }); g.fillStyle = G.gri(.7); g.fillRect(700, 560, 800, 300);
    g.strokeStyle = G.gri(.45); g.lineWidth = 6; g.beginPath(); g.moveTo(980, 900); g.quadraticCurveTo(1010, 680, 1080, 565); g.stroke(); } });
  G.figur({ kind: 'mary', x: 800, y: 1080, s: 900, f: 1, kol: 'pencere', t: st.t, veil: .9, v: .1, head: -.05 });
  return { look: { sepia: .24, strength: .3 } };
}, 'Y');

// ════════ D · GÖRMEDİĞİ KUZEN ════════
bolumKarti('D');
P('D01', ILK('D'), (G, st) => { const g = G.g; G.kamera(720, 560, lerp(1, 1.15, eio(st.p))); G.zemin(.12); isikHalka(G, 620, 360, 900, .5); yuzuk(G, 720, 520, 330, { t: st.t, parilti: .5 + .5 * Math.sin(st.t * 1.7) });
  return { look: { sepia: .3, strength: .26 }, ust: etiket([{ text: 'Haziran 1562', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'A');
KART('D02', 'D02@iyi', [Lq('“İyi niyetimi bundan daha iyi', 'D02@iyi'), Lq('anlatan bir şey bilmiyorum.”', 'D02@anlatan'), { text: '', size: 22 }, Ls('Mary, İngiliz elçisi Randolph\'a · 1562', AT('D02@iyi') + 1, { size: 26 })], { level: 2 });
// D03: haberci güneye; sonra harita: Edinburgh ve Londra Nottingham'a yönelir, D04'te geri çekilir
P('D03', 'D03', (G, st) => {
  const g = G.g, ufuk = 600; G.kamera(720, 560, 1);
  G.gok(ufuk, { ust: .55, alt: .9, isik: [300, 560, 400, 1] }); G.bulutlar(150, 520, { seed: 21, drift: st.t * 8 });
  G.kiyi(-300, 900, ufuk + 4, 120, { v: .5, seed: 5 }); G.kiyi(600, 1900, ufuk + 6, 80, { v: .58, seed: 6 });
  const gr = g.createLinearGradient(0, ufuk, 0, 1080); gr.addColorStop(0, G.gri(.62)); gr.addColorStop(1, G.gri(.3)); g.fillStyle = gr; g.fillRect(-300, ufuk, 2100, 500);
  at(G, { x: 200 + st.lt * 260, y: 900, s: 380, f: 1, ph: st.t * 1.6, binici: { kind: 'erkek', pelerin: true } });
  return { look: { sepia: .2, strength: .32 } };
}, 'G');
P('D03b', 'D03@yaz', (G, st) => {
  const ileri = acS(st, 'D03@görüşmeyi', 2), geri = acS(st, 'D04@ertelendi', 1.6), p = ileri * (1 - geri * .8);
  const E = [-3.19, 55.95], L = [-0.12, 51.5], N = [-1.15, 52.95], ara = (a, b, k) => [lerp(a[0], b[0], k), lerp(a[1], b[1], k)];
  harita(G, st, { k0: [-2, 53.6, 1.6], k1: [-1.6, 53.4, 1.75], yollar: [{ pts: [E, ara(E, N, .92)], p, kesik: true, v: .3 }, { pts: [L, ara(L, N, .92)], p, kesik: true, v: .3 }],
    isaretler: [{ yer: 'edinburgh', kirmizi: true }, { yer: 'londra' }, { yer: 'nottingham', a: ileri * (1 - geri) }], yazilar: [['EDINBURGH', -3.2, 56.3, 26], ['LONDRA', -0.1, 51.2, 26], ['NOTTINGHAM?', -1.1, 53.25, 22, ileri * (1 - geri)]] });
  return { look: { sepia: .3, strength: .26 } };
}, 'A');
// D05–D08: Whitehall galerisi; elçi Melville uzaktaki Elizabeth'e yaklaşır
function galeri(G, st, o = {}) { salon(G, st, { cam: o.cam, duvar: .32, zeminV: .58, pencere: 5, huzme: true }); }
P('D05', 'D05', (G, st) => { galeri(G, st, { cam: [720, 560, 1.15] }); G.figur({ kind: 'erkek', x: 380 + st.lt * 40, y: 1000, s: 620, f: 1, poz: 'yuru', walk: st.t * .7, kol: 'tut', t: st.t, sakal: true, v: .08 });
  return { look: { sepia: .3, strength: .28 } }; }, 'O');
P('D06', 'D06', (G, st) => { galeri(G, st, { cam: [lerp(700, 760, st.p), 540, 1] });
  G.figur({ kind: 'eliz', x: 1080, y: 800, s: 260, f: -1, kol: 'onde', t: st.t, v: .12 });
  G.figur({ kind: 'erkek', x: 380 + eio(st.p) * 220, y: 960, s: 360, f: 1, poz: st.p < .8 ? 'yuru' : 'ayakta', walk: st.t * .7, kol: 'tut', t: st.t, sakal: true, v: .08 });
  return { look: { sepia: .3, strength: .28 }, ust: etiket([{ text: 'Londra · 1564', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('D07', 'D07', fotoP('elizabeth_huys', [.53, .32, .7], [.53, .28, .48], { kunye: 'I. Elizabeth · Frans Huys\'a atfedilir · The Met (CC0)' }), 'Y');
P('D08', 'D08', (G, st) => { galeri(G, st, { cam: [800, 600, 1.35] });
  G.figur({ kind: 'eliz', x: 1010, y: 900, s: 520, f: -1, kol: 'onde', t: st.t, v: .1 });
  G.figur({ kind: 'erkek', x: 640, y: 910, s: 560, f: 1, kol: ac(st, 'D08@uzun') > 0 ? 'kaldir' : 'tut', t: st.t, sakal: true, v: .08 });
  return { look: { sepia: .3, strength: .28 } }; }, 'O');
KART('D09', 'D09', [Lq('“O hâlde fazla uzun.', 'D09@halde', { size: 78 }), Lq('Çünkü ben ne fazla uzunum,', 'D09@çünkü'), Lq('ne fazla kısa.”', AT('D09@kısa') - .5), { text: '', size: 22 }, Ls('Elizabeth · Melville\'in aktarımıyla, 1564', S('D09') + 1, { size: 26 })], { level: 2 });
// D10: el aynası; aynada öteki kraliçe (Mary'nin profili)
P('D10', 'D10', (G, st) => {
  const g = G.g; G.kamera(720, 540, lerp(1, 1.12, eio(st.p))); G.zemin(.14); isikHalka(G, 600, 380, 900, .5);
  const cx = 760, cy = 470, rx = 250, ry = 320;
  g.fillStyle = G.gri(.3); g.fillRect(cx - 40, cy + ry, 80, 360); g.fillStyle = G.gri(.5); g.fillRect(cx - 40, cy + ry, 22, 360);   // sap
  g.fillStyle = G.gri(.32); g.beginPath(); g.ellipse(cx, cy, rx + 40, ry + 40, 0, 0, TAU); g.fill(); g.fillStyle = G.gri(.58); g.beginPath(); g.ellipse(cx - 6, cy - 6, rx + 26, ry + 26, 0, Math.PI * .9, Math.PI * 1.6); g.fill();
  const im = IMG.mary_peceli_profil; g.save(); g.beginPath(); g.ellipse(cx, cy, rx, ry, 0, 0, TAU); g.clip(); g.fillStyle = G.gri(.4); g.fillRect(cx - rx, cy - ry, rx * 2, ry * 2);
  if (im) { const W = im.naturalWidth, H = im.naturalHeight, k = 1.9 * rx / (W * .45); g.globalAlpha = lerp(.0, .95, acS(st, 'D10@kendini', 1.6)); g.drawImage(BOYA.griOn(im, 1.1, 1.05), cx - .5 * W * k, cy - .34 * H * k, W * k, H * k); g.globalAlpha = 1; }
  const pr = g.createLinearGradient(cx - rx, cy - ry, cx + rx, cy + ry); pr.addColorStop(0, G.gri(1, .3)); pr.addColorStop(.5, G.gri(1, 0)); g.fillStyle = pr; g.fillRect(cx - rx, cy - ry, rx * 2, ry * 2); g.restore();
  el(G, cx + 30, cy + ry + 200, 300, { kalem: false, a: -1.5, manset: 'dantel', f: 1 });
  return { look: { sepia: .26, strength: .28 } };
}, 'Y');
// D11–D14: satranç: beyaz vezir (Elizabeth), kırmızı vezir (Mary); damat adayları taş olarak
const TAHTA0 = () => [{ tip: 'vezir', renk: 'beyaz', u: 1, v: 1 }, { tip: 'sah', renk: 'siyah', u: 0, v: 0, h: 130 }, { tip: 'piyon', renk: 'beyaz', u: 2, v: 2 }, { tip: 'piyon', renk: 'siyah', u: 5, v: 2 }, { tip: 'fil', renk: 'siyah', u: 3, v: 4 }];
P('D11', 'D11', (G, st) => {
  const k = acS(st, 'D11@kiminle', 1.6), sah = acS(st, 'D12@kocası', 1.6);
  satranc(G, st, { cam: [lerp(560, 860, eio(st.p)), lerp(640, 560, eio(st.p)), 1.15], taslar: [...TAHTA0(), { tip: 'vezir', renk: 'kirmizi', u: 5, v: 5 }, { tip: 'sah', renk: 'siyah', u: lerp(7, 5, sah), v: lerp(7, 6, sah), h: 160 * (k > 0 ? 1 : 0) + .01 }] });
  return { look: { sepia: .24, strength: .3 } };
}, 'A');
P('D13', 'D13', (G, st) => {
  const k = acS(st, 'D13@gözdesi', 1.8);
  satranc(G, st, { cam: [700, 640, 1.45], taslar: [...TAHTA0(), { tip: 'vezir', renk: 'kirmizi', u: 5, v: 5 }, { tip: 'at', renk: 'beyaz', u: lerp(2, 4, k), v: lerp(3, 5, k), f: 1 }] });
  el(G, lerp(560, 900, k), lerp(600, 520, k), 330, { kalem: false, a: -.2, manset: 'dantel' });
  return { look: { sepia: .24, strength: .3 } };
}, 'O');
P('D14', 'D14', (G, st) => {
  const dus = acS(st, 'D14@kalbini', 1.2), yeni = acS(st, 'D14@başka', 1.2);
  satranc(G, st, { cam: [880, 560, 1.7], taslar: [{ tip: 'vezir', renk: 'kirmizi', u: 5, v: 5 }, { tip: 'at', renk: 'beyaz', u: 4, v: 5, f: 1, dus }, { tip: 'sah', renk: 'siyah', u: 6, v: 5, h: 190 * yeni + .01 }] });
  return { look: { sepia: .24, strength: .3 } };
}, 'A');
P('D14b', 'D14@uzun', fotoP('darnley_17yy', [.5, .58, .62], [.5, .52, .42], { kunye: 'Lord Darnley · 17. yy gravürü · The Met (CC0)' }), 'Y');
P('D15', 'D15', fotoP('mary_darnley_dunkarton', [.47, .5, .9], [.47, .42, .7], { kunye: 'Mary ve Darnley · R. Dunkarton, y. 1816 · The Met (CC0)' }), 'O');
P('D16', 'D16', (G, st) => {
  const g = G.g; kilise(G, st, { cam: [720, 560, lerp(1, 1.05, st.p)] });
  g.fillStyle = G.gri(.7); g.fillRect(560, 620, 320, 26); for (const x of [600, 840]) G.mum(x, 620, 140, st.t + x, { r: 380 });
  G.figur({ kind: 'mary', x: 680, y: 900, s: 300, f: 1, kol: 'onde', t: st.t, veil: .9, v: .12 }); G.figur({ kind: 'erkek', x: 760, y: 905, s: 330, f: -1, kol: 'onde', t: st.t, v: .1 });
  return { look: { sepia: .3, strength: .28 }, ust: etiket([{ text: 'Holyrood · 29 Temmuz 1565', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) };
}, 'G');

// ════════ E · HOLYROOD'DAKİ GECE ════════
bolumKarti('E');
P('E01', ILK('E'), fotoP('mary_darnley_dunkarton', [.32, .34, .5], [.32, .3, .36], { kunye: 'Lord Darnley · R. Dunkarton, y. 1816 · The Met (CC0)' }), 'Y');
// E02: taç yastıkta; asa (yetki) çekilir
P('E02', 'E02', (G, st) => {
  const g = G.g; G.kamera(720, 600, lerp(1, 1.1, st.p)); G.zemin(.13); isikHalka(G, 640, 400, 900, .45);
  const yg = g.createLinearGradient(380, 0, 1060, 0); yg.addColorStop(0, G.gri(.5)); yg.addColorStop(1, G.gri(.22)); g.fillStyle = yg;
  g.fill(G.pathOf([[340, 860], [400, 760], [560, 735], [880, 735], [1040, 760], [1100, 860], [1000, 900], [440, 900]], true, .6));
  tac(G, 620, 760, 260, { v: .3 });
  const c = acS(st, 'E02@vermedi', 1.2); g.save(); g.translate(880 + c * 700, 820); g.rotate(-.35); g.fillStyle = G.gri(.55); g.fillRect(-8, -420, 16, 420); g.fillStyle = G.gri(.75); g.beginPath(); g.arc(0, -440, 32, 0, TAU); g.fill(); g.fillRect(-4, -500, 8, 40); g.fillRect(-18, -488, 36, 8); g.restore();
  return { look: { sepia: .26, strength: .3 } };
}, 'A');
// E03: Rizzio lavtasıyla; kapıda uzun bir gölge (Darnley)
P('E03', 'E03', (G, st) => {
  const g = G.g; G.kamera(720, 580, lerp(1, 1.06, st.p)); oda(G, st, { duvar: .3, zeminY: 840 }); isikHalka(G, 500, 600, 700, .4);
  g.fillStyle = G.gri(.06); g.fillRect(1040, 220, 260, 640); const k = acS(st, 'E03@kıskançlığı', 1.5);
  G.figur({ kind: 'erkek', x: 1170, y: 860, s: 600, f: -1, kol: 'yan', t: st.t, v: lerp(.06, .2, k), pelerin: true });
  G.figur({ kind: 'erkek', x: 470, y: 880, s: 440, f: 1, poz: 'otur', kol: 'tut', t: st.t, v: .1, sapka: false });
  g.fillStyle = G.gri(.45); g.save(); g.translate(560, 640); g.rotate(-.5); g.beginPath(); g.ellipse(0, 0, 60, 44, 0, 0, TAU); g.fill(); g.fillStyle = G.gri(.2); g.fillRect(40, -6, 160, 12); g.restore();   // lavta
  return { look: { sepia: .24, strength: .32 } };
}, 'O');
P('E04', 'E04', fotoP('holyrood_kucuk_oda', [.5, .5, .85], [.47, .46, .62], { kunye: 'Holyrood\'daki küçük oda · S. D. Swarbreck, 1837 · The Met (CC0)', etiket: [{ text: '9 Mart 1566', size: 40, font: 'Cormorant Garamond', italic: true, at: S('E04') + .4 }] }), 'G');
// E05: gölge oyunu: duvarda silahlı adamların gölgeleri; masa, mum devrilir
P('E05', 'E05', (G, st) => {
  const g = G.g; G.kamera(720, 560, 1); const gir = acS(st, 'E05@girdi', 1.8), sur = acS(st, 'E05@sürükleyip', 2.2), son = acS(st, 'E05@öldürdü', 1.2);
  G.zemin(.62); isikHalka(G, 720, 900, 900, .55);
  G.yumusak(4, Y => {
    Y.figur({ kind: 'mary', x: 560, y: 1000, s: 700, f: 1, kol: 'uzat', t: st.t, veil: 0, v: .22 });
    for (let i = 0; i < 4; i++) { const x = lerp(1600, 980 + i * 120, gir) - sur * 300; Y.figur({ kind: 'erkek', x, y: 1020, s: 760, f: -1, poz: 'yuru', walk: st.t * .6 + i * .3, kol: i % 2 ? 'kaldir' : 'uzat', t: st.t, v: .14 }); }
    Y.figur({ kind: 'erkek', x: lerp(660, 300, sur), y: 1030, s: 600, f: 1, poz: 'diz', kol: 'uzat', t: st.t, v: .18, sapka: false }); }, .85);
  g.fillStyle = G.gri(.1); g.fillRect(380, 900, 680, 200); const dev = son; G.mum(720 + dev * 80, 900, 150, st.t, { r: lerp(500, 50, dev) });
  return { look: { sepia: .14, strength: .45 }, exposure: lerp(1, .6, son) };
}, 'O');
KART('E06', 'E06@hizmetkarımı', [Lq('“Hizmetkârımı gözümün önünde,', 'E06@hizmetkarımı'), Lq('ben hamileyken öldürdüler.”', 'E06@ben'), { text: '', size: 22 }, Ls('Mary · Workington, 17 Mayıs 1568', AT('E06@hizmetkarımı') + 1, { size: 26 })]);
P('E06a', 'E06', (G, st) => { const g = G.g; G.kamera(720, 560, 1.05); G.zemin(.1); isikHalka(G, 720, 640, 520, .4); g.fillStyle = G.gri(.25); g.fillRect(300, 800, 840, 300); G.dik(700, 650, 40, 150, .7); return { look: { sepia: .2, strength: .4 } }; }, 'A');
// E07: gece kaçışı: iki atlı, ay, saray silueti
function gece(G, st, o = {}) { const g = G.g, ufuk = o.ufuk ?? 700; G.zemin(.12); const gr = g.createLinearGradient(0, 0, 0, ufuk); gr.addColorStop(0, G.gri(.08)); gr.addColorStop(1, G.gri(.3)); g.fillStyle = gr; g.fillRect(-500, -500, 2500, ufuk + 500);
  const m = o.ay || [1100, 200]; isikHalka(G, m[0], m[1], 300, .5); g.fillStyle = G.gri(.95); g.beginPath(); g.arc(m[0], m[1], 46, 0, TAU); g.fill();
  const q = G.rng(3); g.fillStyle = G.gri(.9); for (let i = 0; i < 60; i++) { const x = q() * 1600 - 80, y = q() * ufuk * .8; g.fillRect(x, y, 2 + q() * 2, 2 + q() * 2); }
  g.fillStyle = G.gri(.1); g.fillRect(-500, ufuk, 2500, 600); }
P('E07', 'E07', (G, st) => {
  G.kamera(lerp(620, 820, eio(st.p)), 540, 1); gece(G, st);
  kale(G, 100, 702, 600, [{ x: .2, w: .3, h: .45, cati: 'konik', pen: 4 }, { x: .5, w: .4, h: .3, cati: 'mazgal', pen: 5 }, { x: .8, w: .14, h: .55, cati: 'konik', pen: 3 }], { v: .14, isik: .22, gece: true });
  const k = acS(st, 'E07@kaçtılar', 1.5);
  for (const [i, kind] of [[0, 'mary'], [1, 'erkek']]) at(G, { x: lerp(500, 1200, k) + i * 220 + st.lt * 30, y: 840 + i * 30, s: 300, f: 1, ph: st.t * 1.7 + i * .4, v: .05, binici: { kind, veil: .9, v: .05 } });
  return { look: { sepia: .06, strength: .45 }, exposure: .9 };
}, 'G');
P('E08', 'E08', (G, st) => { besikOda(G, st, { cam: [720, 700, lerp(1.4, 1.5, st.p)], bebek: true, salla: .03, kar: false }); return { look: { sepia: .3, strength: .28 }, ust: etiket([{ text: 'Edinburgh · 19 Haziran 1566', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'Y');
// E09–E10: Greenwich; Elizabeth dans eder; sonra oturur, eli yanağında
function greenwich(G, st, o = {}) { salon(G, st, { cam: o.cam, duvar: .38, zeminV: .6, pencere: 4 }); isikHalka(G, 720, 600, 700, .35); }
P('E09', 'E09', (G, st) => { greenwich(G, st, { cam: [lerp(650, 780, eio(st.p)), 560, 1.05] });
  const ph = st.t * .4; for (const [cx, y, sc, k] of [[360, 820, .65, 1], [1080, 820, .65, 2], [250, 930, 1, 3], [1180, 935, 1, 4]]) { G.figur({ kind: 'kadin', x: cx - 70 * sc, y, s: 330 * sc, poz: 'yuru', walk: ph + k * .3, kol: 'uzat', t: st.t, v: .2 }); G.figur({ kind: 'erkek', x: cx + 70 * sc, y, s: 350 * sc, f: -1, poz: 'yuru', walk: ph + k * .3 + .5, kol: 'uzat', t: st.t, v: .18 }); }
  G.figur({ kind: 'eliz', x: 700 + Math.sin(st.t * .9) * 30, y: 880, s: 430, f: 1, poz: 'yuru', walk: ph, kol: 'uzat', t: st.t, v: .08 }); G.figur({ kind: 'erkek', x: 840 - Math.sin(st.t * .9) * 30, y: 885, s: 450, f: -1, poz: 'yuru', walk: ph + .5, kol: 'uzat', t: st.t, v: .1 });
  return { look: { sepia: .34, strength: .26 }, exposure: 1.05, ust: etiket([{ text: 'Greenwich · Haziran 1566', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('E10', 'E10', (G, st) => { greenwich(G, st, { cam: [720, 640, 1.4] }); const otur = ac(st, 'E10@oturdu') > 0;
  G.figur({ kind: 'eliz', x: 720, y: 930, s: 560, f: 1, poz: otur ? 'otur' : 'ayakta', kol: otur ? 'yanak' : 'onde', t: st.t, v: .08 });
  return { look: { sepia: .3, strength: .3 }, exposure: lerp(1.05, .9, acS(st, 'E10@oturdu', 2)) }; }, 'O');
KART('E10k', AT('E10@iskoçya') - .2, [Lq('“İskoçya kraliçesi güzel bir oğlan doğurdu,', 'E10@iskoçya', { size: 58 }), Lq('bense kısır bir kütüğüm.”', 'E10@bense', { size: 72 }), { text: '', size: 22 }, Ls('Elizabeth · Melville\'in anılarından, 1566', AT('E10@iskoçya') + 1, { size: 26 })], { level: 2 });
P('E11', 'E11', fotoP('elizabeth_depasse_1592', [.5, .32, .5], [.5, .29, .36], { parlak: 1.08, kunye: 'I. Elizabeth · Crispijn de Passe, 1592 · The Met (CC0)', look: { sepia: .3 } }), 'Y');
P('E12', 'E12', fotoP('elizabeth_huys', [.52, .4, .95], [.52, .36, .8], { kunye: 'I. Elizabeth · Frans Huys\'a atfedilir · The Met (CC0)',
  ciz: (G, st, W, H) => { const k = acS(st, 'E12@içi', 2.2); if (k <= 0) return; const g = G.g, gr = g.createLinearGradient(W * .3, 0, W * .62, 0); gr.addColorStop(0, G.gri(0, 0)); gr.addColorStop(1, G.gri(0, .6 * k)); g.fillStyle = gr; g.fillRect(W * .3, 0, W * .7, H); } }), 'O');

// ════════ F · BOTHWELL ════════
bolumKarti('F');
P('F01', ILK('F'), (G, st) => { const g = G.g; galeri(G, st, { cam: [720, 560, 1.05] }); g.fillStyle = G.gri(0, .25); g.fillRect(-300, -300, 2100, 1700);
  G.figur({ kind: 'mary', x: 330, y: 960, s: 420, f: -1, kol: 'yan', t: st.t, veil: .9, v: .08 }); G.figur({ kind: 'erkek', x: 1150, y: 965, s: 450, f: 1, kol: 'yan', t: st.t, v: .08 });
  return { look: { sepia: .2, strength: .34 } }; }, 'O');
// F02: Kirk o'Field, gece; ev havaya uçar
P('F02', 'F02', (G, st) => {
  const g = G.g, pat = st.t - AT('F02@havaya'), k = clamp(pat / .4); G.kamera(720 + (pat > 0 && pat < 1.2 ? Math.sin(pat * 60) * 12 * (1 - pat / 1.2) : 0), 560, 1.05); gece(G, st, { ay: [300, 180] });
  if (pat < .25) kale(G, 560, 702, 520, [{ t: 'ev', x: .3, w: .5, h: .34, cati: 'beşik', pen: 4 }, { t: 'ev', x: .72, w: .3, h: .28, cati: 'beşik', pen: 2 }], { v: .16, isik: .24, gece: true });
  else { kale(G, 560, 702, 520, [{ t: 'ev', x: .18, w: .2, h: .12 }, { t: 'ev', x: .58, w: .14, h: .06 }], { v: .12 }); }
  if (pat > 0) { isikHalka(G, 720, 600, lerp(200, 1200, k), lerp(1, .2, clamp(pat / 2.5))); const q = G.rng(9); for (let i = 0; i < 40; i++) { const a = q() * Math.PI - Math.PI, sp = 200 + q() * 500, tt = Math.min(pat, 3); g.fillStyle = G.gri(.1); g.fillRect(720 + Math.cos(a) * sp * tt, 640 + Math.sin(a) * sp * tt + 160 * tt * tt, 8 + q() * 14, 6 + q() * 10); }
    sis(G, st, 400, 720, clamp(pat / 1.5) * .6, { v: .5, n: 6 }); }
  return { look: { sepia: .08, strength: .5 }, exposure: pat > 0 && pat < .5 ? 1.8 - pat * 1.4 : .95 };
}, 'G');
// F03: bahçe, şafak: armut ağacı, sandalye, pelerin (beden gösterilmez)
P('F03', 'F03', (G, st) => {
  const g = G.g, ufuk = 640; G.kamera(lerp(740, 700, eio(st.p)), 820, 1.5); G.gok(ufuk, { ust: .62, alt: .86 }); G.bulutlar(120, 520, { seed: 25, drift: st.t * 3 });
  kale(G, 900, ufuk, 500, [{ t: 'sur', x: .5, w: 1.4, h: .16 }], { v: .3 }); g.fillStyle = G.gri(.55); g.fillRect(-300, ufuk, 2100, 600);
  g.strokeStyle = G.gri(.14); g.lineCap = 'round'; const dal = (x, y, a, L, w, d) => { if (d > 6) return; const x2 = x + Math.sin(a) * L, y2 = y - Math.cos(a) * L; g.lineWidth = w; g.beginPath(); g.moveTo(x, y); g.lineTo(x2, y2); g.stroke(); dal(x2, y2, a - .45, L * .72, w * .66, d + 1); dal(x2, y2, a + .35, L * .7, w * .66, d + 1); };
  dal(380, 900, .05, 220, 30, 0);
  g.fillStyle = G.gri(.18); g.save(); g.translate(820, 880); g.rotate(.4); g.fillRect(-60, -10, 120, 16); g.fillRect(-60, -110, 14, 120); g.fillRect(46, -10, 12, 70); g.fillRect(-56, -10, 12, 70); g.restore();     // devrik sandalye
  g.fillStyle = G.gri(.3); g.fill(G.pathOf([[560, 930], [700, 900], [780, 930], [720, 960], [600, 965]], true, .6));    // pelerin
  sis(G, st, 600, 950, .35, { n: 6, v: .8 });
  return { look: { sepia: .14, strength: .36 }, ust: etiket([{ text: 'Kirk o\'Field · 10 Şubat 1567', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) };
}, 'O');
// F04: parmaklar tek adamı gösterir (duvarda gölgeler); ortada Bothwell
P('F04', 'F04', (G, st) => {
  const g = G.g; G.kamera(720, 600, lerp(1, 1.1, eio(st.p))); G.gok(720, { ust: .55, alt: .85 }); kale(G, -100, 720, 1700, [{ t: 'ev', x: .2, w: .3, h: .3, cati: 'beşik', pen: 4 }, { t: 'ev', x: .55, w: .3, h: .36, cati: 'beşik', pen: 5 }, { t: 'ev', x: .85, w: .2, h: .28, cati: 'beşik', pen: 3 }], { v: .45 });
  g.fillStyle = G.gri(.5); g.fillRect(-300, 720, 2100, 500);
  const k = acS(st, 'F04@gösterdi', 1.2), b = acS(st, 'F04@botvel', 1.2);
  G.figur({ kind: 'erkek', x: 760, y: 860, s: 380, f: 1, kol: 'yan', t: st.t, v: lerp(.42, .06, b), sakal: true, pelerin: true });
  for (const [x, y, sc, f] of [[160, 1040, 1, 1], [380, 1080, 1.1, 1], [1180, 1050, 1, -1], [1380, 1090, 1.15, -1], [560, 1120, 1.2, 1], [980, 1120, 1.2, -1]]) G.figur({ kind: f > 0 && x < 300 ? 'kadin' : 'erkek', x, y, s: 520 * sc, f, kol: k > 0 ? 'isaret' : 'yan', t: st.t, v: .05 });
  return { look: { sepia: .16, strength: .38 }, ust: etiket([{ text: 'Edinburgh · Şubat 1567', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) };
}, 'Y');
P('F05', 'F05', (G, st) => { yazMasa(G, st, { cam: [720, 600, 1.05], prog: st.p * 1.2, karalama: 3, manset: 'dantel' }); return { look: { sepia: .3, strength: .28 } }; }, 'A');
KART('F06', 'F06', [Lq('“Duyduklarım kulaklarımı öyle sersemletti,', 'F06', { size: 56 }), Lq('yüreğimi öyle korkuttu ki,', 'F06@yüreğimi', { size: 56 }), Lq('yazacak gücüm zor yetiyor.', 'F06@yazacak', { size: 56 }), { text: '', size: 22 }, Ls('Elizabeth\'ten Mary\'ye · 24 Şubat 1567 (İngilizce özetinden)', S('F06') + 1, { size: 26 })], { level: 2 });
KART('F06b', AT('F06@sizin') - .2, [Lq('“Sizin için,', 'F06@sizin', { size: 80 }), Lq('ondan daha çok üzülüyorum.”', 'F06@ondan', { size: 72 })], { level: 2 });
P('F07', 'F07', fotoP('elizabeth_huys', [.53, .3, .4], [.53, .28, .3], { kunye: 'I. Elizabeth · Frans Huys\'a atfedilir · The Met (CC0)' }), 'Y');
// F08: Bothwell mahkemeden çıkar; mızraklı adamlar arasında
P('F08', 'F08', (G, st) => {
  const g = G.g; G.kamera(720, 560, 1.05); G.gok(700, { ust: .55, alt: .8 }); kale(G, 200, 720, 1000, [{ t: 'ev', x: .5, w: .9, h: .5, cati: 'beşik', pen: 6 }], { v: .3 });
  g.fillStyle = G.gri(.06); g.fillRect(600, 420, 240, 300); g.fillStyle = G.gri(.5); g.fillRect(-200, 700, 1900, 500);
  const k = acS(st, 'F08@aklandı', 2); ordu(G, st, { x0: 60, x1: 560, y: 900, s: 300, n: 7, v: .14 }); ordu(G, st, { x0: 900, x1: 1400, y: 905, s: 300, n: 7, v: .14, seed: 7 });
  G.figur({ kind: 'erkek', x: 720, y: lerp(720, 960, k), s: lerp(300, 460, k), f: 1, poz: k > 0 && k < 1 ? 'yuru' : 'ayakta', walk: st.t * .8, kol: 'yan', t: st.t, v: .06, pelerin: true, sakal: true });
  return { look: { sepia: .2, strength: .34 } };
}, 'O');
P('F09', 'F09', fotoP('bothwell_tutuklama', [.5, .45, .52], [.5, .46, .36], { kunye: 'Bothwell Mary\'nin yolunu keser · J. Walker, 1792 · The Met (CC0)', etiket: [{ text: '24 Nisan 1567', size: 40, font: 'Cormorant Garamond', italic: true, at: S('F09') + .4 }] }), 'G');
P('F10', 'F10', (G, st) => { const g = G.g; G.kamera(720, 600, lerp(1, 1.12, st.p)); G.zemin(.16); isikHalka(G, 620, 400, 900, .5); kitap(G, 720, 860, 900, { baslik: 'MEMOIRS · MELVILLE' });
  const k = acS(st, 'F10@iki', .8); g.fillStyle = G.gri(.1); g.font = '700 70px "Cinzel"'; g.textAlign = 'center'; g.globalAlpha = k; g.fillText('I', 450, 520); g.globalAlpha = acS(st, 'F10@yazar', .8); g.fillText('II', 990, 520); g.globalAlpha = 1;
  return { look: { sepia: .32, strength: .26 } }; }, 'A');
// F11: Dunbar kalesi, deniz kayalıkları; atlılar kapıdan girer
P('F11', 'F11', (G, st) => {
  const g = G.g, ufuk = 560; G.kamera(lerp(700, 780, eio(st.p)), 540, 1); G.gok(ufuk, { ust: .4, alt: .78 }); G.bulutlar(130, 480, { seed: 27, drift: st.t * 6, govde: .42 });
  G.deniz(ufuk, 1080, { t: st.t, ufuk: .72, on: .3, n: 80 });
  g.fillStyle = G.gri(.2); g.fill(G.pathOf([[500, 1100], [560, 760], [640, 640], [900, 600], [1200, 620], [1500, 700], [1700, 1100]], true, .5));
  kale(G, 640, 640, 700, [{ t: 'sur', x: .4, w: .7, h: .15 }, { x: .12, w: .14, h: .4 }, { x: .5, w: .2, h: .3, pen: 2 }, { x: .78, w: .12, h: .45, cati: 'konik' }], { v: .16 });
  for (let i = 0; i < 3; i++) at(G, { x: 1500 - st.lt * 60 - i * 120, y: 700, s: 110, f: -1, ph: st.t + i * .3, v: .1, binici: { kind: i === 1 ? 'mary' : 'erkek', veil: .8, v: .1 } });
  return { look: { sepia: .14, strength: .4 }, ust: etiket([{ text: 'Dunbar', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) };
}, 'G');
P('F12', 'F12', (G, st) => { const g = G.g, k = acS(st, 'F12@zorla', 1.6); G.kamera(720, 560, lerp(1, 1.15, st.p)); oda(G, st, { duvar: .22, zeminY: 900 });
  g.fillStyle = G.gri(.04); g.fillRect(420, 140, 600, 760); g.save(); g.translate(420, 140); g.scale(lerp(.15, 1, k), 1); g.fillStyle = G.gri(.32); g.fillRect(0, 0, 600, 760); for (let i = 0; i < 5; i++) { g.fillStyle = G.gri(.24); g.fillRect(i * 120 + 10, 0, 6, 760); } g.fillStyle = G.gri(.12); g.fillRect(0, 160, 600, 30); g.fillRect(0, 560, 600, 30); g.restore();
  return { look: { sepia: .14, strength: .42 }, exposure: lerp(1, .75, k) }; }, 'Y');
P('F13', 'F13', (G, st) => { const g = G.g; salon(G, st, { cam: [720, 560, lerp(1, 1.04, st.p)], duvar: .18, zeminV: .32, pencere: 3, pencereV: .35, huzme: false }); for (const x of [560, 880]) G.mum(x, 640, 120, st.t + x, { r: 300 });
  G.figur({ kind: 'mary', x: 680, y: 860, s: 260, kol: 'onde', t: st.t, veil: .9, v: .12 }); G.figur({ kind: 'erkek', x: 760, y: 862, s: 280, f: -1, kol: 'onde', t: st.t, v: .1, sakal: true });
  return { look: { sepia: .1, strength: .4 }, ust: etiket([{ text: 'Holyrood · 15 Mayıs 1567, sabah dört', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('F14', 'F14', (G, st) => { G.kamera(720, 600, lerp(1.05, 1.2, st.p)); G.zemin(.16); isikHalka(G, 620, 400, 900, .5); kitap(G, 720, 860, 900, { baslik: 'MARIA STUART · ZWEIG', cevir: (st.lt * .7) % 1 }); return { look: { sepia: .32, strength: .26 } }; }, 'A');
P('F15', 'F15', (G, st) => { const g = G.g; G.kamera(720, 600, lerp(1, 1.1, st.p)); G.zemin(.14); isikHalka(G, 720, 420, 800, .5); g.fillStyle = G.gri(.26); g.fillRect(-200, 760, 1900, 400);
  sandik(G, 720, 790, 560, acS(st, 'F15@mektuplar', 1.6), { mektup: true }); return { look: { sepia: .28, strength: .3 } }; }, 'O');
P('F16', 'F16', (G, st) => { G.kamera(720, 560, 1.05); G.zemin(.2); isikHalka(G, 600, 380, 900, .5); const kay = acS(st, 'F16@kayıp', 1.6), kop = acS(st, 'F16@kopyalar', 1.4);
  const g = G.g; g.globalAlpha = 1 - kay * .92; G.mektup(560, 560, 640, 760, -.08, { lh: 50, karalama: 9, seed: 3, prog: 1 }); g.globalAlpha = 1;
  if (kop > 0) G.mektup(lerp(1300, 900, kop), 600, 600, 720, .05, { lh: 46, karalama: 10, seed: 8, prog: 1, v: .86 });
  return { look: { sepia: .3, strength: .28 }, ust: kunye('Casket mektupları: asılları kayıp, yalnız kopyaları kaldı · canlandırma') }; }, 'Y');
P('F17', 'F17', (G, st) => { G.kamera(720, 560, 1.05); G.zemin(.18); isikHalka(G, 720, 380, 800, .5); terazi(G, 720, 940, 700, Math.sin(st.t * 1.3) * .08 * (1 - st.p * .7), 'Zweig: tutku', 'Melville: zorla');
  return { look: { sepia: .28, strength: .28 } }; }, 'O');

// ════════ G · GÖLÜN ORTASINDAKİ ADA ════════
bolumKarti('G');
function tepeler(G, st, ufuk, o = {}) { const g = G.g; G.gok(ufuk, { ust: o.ust ?? .5, alt: .85 }); G.bulutlar(130, ufuk - 80, { seed: o.seed || 31, drift: st.t * 4 });
  G.kiyi(-400, 900, ufuk + 4, 160, { v: .4, seed: 11 }); G.kiyi(500, 1900, ufuk + 6, 140, { v: .45, seed: 12 }); const gr = g.createLinearGradient(0, ufuk, 0, 1080); gr.addColorStop(0, G.gri(.5)); gr.addColorStop(1, G.gri(.25)); g.fillStyle = gr; g.fillRect(-400, ufuk, 2300, 600); }
P('G01', ILK('G'), (G, st) => { G.kamera(lerp(680, 760, st.p), 560, 1); tepeler(G, st, 560);
  ordu(G, st, { x0: 40, x1: 560, y: 640, s: 90, n: 26, v: .16, sancak: [{ x: 200 }, { x: 420 }] }); ordu(G, st, { x0: 880, x1: 1420, y: 630, s: 90, n: 26, v: .16, seed: 9, sancak: [{ x: 1000 }, { x: 1300, v: .5 }] });
  return { look: { sepia: .18, strength: .34 }, ust: etiket([{ text: 'Carberry · 15 Haziran 1567', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('G02', 'G02', (G, st) => { G.kamera(720, 600, 1.2); tepeler(G, st, 620, { seed: 33 }); const k = acS(st, 'G02@kaçtı', 3);
  at(G, { x: lerp(900, 1500, k), y: lerp(720, 660, k), s: lerp(200, 80, k), f: 1, ph: st.t * 1.8, v: .12, binici: { kind: 'erkek', v: .12 } });
  G.figur({ kind: 'mary', x: 520, y: 1000, s: 560, f: 1, kol: 'yan', t: st.t, veil: .9, v: .08 });
  return { look: { sepia: .18, strength: .34 } }; }, 'O');
function lochleven(G, st, o = {}) { const g = G.g, ufuk = o.ufuk ?? 560; G.kamera(...(o.cam || [720, 560, 1])); G.gok(ufuk, { ust: o.ust ?? .55, alt: .88 }); G.bulutlar(140, ufuk - 80, { seed: 35, drift: st.t * 3 });
  G.kiyi(-400, 1900, ufuk + 4, 90, { v: .55, seed: 13, k: 5 }); G.deniz(ufuk, 1080, { t: st.t * .5, ufuk: .84, on: .55, n: 60 });
  g.fillStyle = G.gri(.32); g.fill(G.pathOf([[460, ufuk + 70], [600, ufuk + 40], [900, ufuk + 36], [1060, ufuk + 60], [960, ufuk + 90], [560, ufuk + 92]], true, .6));
  kale(G, 580, ufuk + 62, 520, [{ t: 'sur', x: .5, w: .8, h: .12 }, { x: .28, w: .2, h: .5, cati: 'mazgal', pen: 3 }, { x: .7, w: .1, h: .22 }], { v: .18 });
  sis(G, st, ufuk - 40, ufuk + 160, o.sis ?? .3, { n: 6, v: .88 }); }
P('G03', 'G03', (G, st) => { lochleven(G, st, { cam: [lerp(640, 760, eio(st.p)), 560, lerp(1, 1.08, st.p)] }); return { look: { sepia: .14, strength: .34 }, ust: etiket([{ text: 'Loch Leven · Haziran 1567', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('G04', 'G04', (G, st) => { const g = G.g, k = acS(st, 'G04@düşürdü', 1.2); G.kamera(720, 600, 1.25); G.zemin(.08); G.pencere({ x: 720, y: 200, w: 300, h: 420, d: 90, duvar: .12, dis: () => { G.gok(620, { ust: .3, alt: .5 }); } });
  if (k < 1) G.mum(720, 800, 160, st.t, { r: lerp(500, 60, k) }); else G.dik(706, 640, 28, 160, .5);
  return { look: { sepia: .12, strength: .42 }, exposure: lerp(1, .7, k) }; }, 'A');
P('G05', 'G05', fotoP('lochleven_feragat', [.5, .38, .5], [.5, .4, .36], { kunye: 'Feragat · P.-L. Dandeleux, 1835 · The Met (CC0)', etiket: [{ text: '24 Temmuz 1567', size: 40, font: 'Cormorant Garamond', italic: true, at: S('G05') + .4 }] }), 'O');
P('G05b', 'G05@yaşındaki', (G, st) => { besikOda(G, st, { cam: [720, 760, 1.6], kar: false }); const k = acS(st, 'G05@kral', 1.4); tac(G, 720, lerp(380, 770, k), 150, { v: .3 }); return { look: { sepia: .26, strength: .3 }, ust: etiket([{ text: 'Stirling · 29 Temmuz 1567', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'A');
P('G06', 'G06', fotoP('mary_peceli_18yy', [.5, .4, .7], [.5, .36, .5], { kunye: 'Mary Stuart · 18. yy gravürü · The Met (CC0)' }), 'Y');
P('G07', 'G07', (G, st) => { const g = G.g; G.kamera(760, 520, lerp(1.1, 1.18, st.p));
  G.pencere({ x: 900, y: 140, w: 420, h: 620, d: 110, duvar: .15, dis: () => { lochleven(G, st, { ufuk: 520, sis: .2 }); G.kamera(760, 520, lerp(1.1, 1.18, st.p)); kar(G, st, 680, 140, 440, 620, 70); } });
  G.figur({ kind: 'mary', x: 560, y: 1050, s: 820, f: 1, kol: 'pencere', t: st.t, veil: .9, v: .1 });
  return { look: { sepia: .12, strength: .36 } }; }, 'O');
P('G08', 'G08', fotoP('lochleven_kacis_rogers', [.5, .5, .72], [.48, .55, .5], { kunye: 'Lochleven\'den kaçış · J. Rogers, 19. yy · The Met (CC0)', etiket: [{ text: '2 Mayıs 1568, gece', size: 40, font: 'Cormorant Garamond', italic: true, at: S('G08') + .4 }] }), 'G');
P('G08b', AT('G08@kilitledi') - .3, (G, st) => { G.kamera(720, 560, 1.1); G.zemin(.2); isikHalka(G, 700, 400, 700, .35); kilit(G, 720, 600, 420, acS(st, 'G08@kilitledi', .8)); return { look: { sepia: .16, strength: .4 } }; }, 'A');
P('G09', 'G09', (G, st) => { G.kamera(720, 560, 1); tepeler(G, st, 560, { seed: 37 }); const k = acS(st, 'G09@ordu', 2.5);
  ordu(G, st, { x0: 100, x1: lerp(500, 1340, k), y: 700, s: 110, n: Math.round(lerp(8, 34, k)), v: .14, sancak: [{ x: 300, up: k }, { x: 700, up: k * .9 }, { x: 1100, up: k * .8 }] });
  return { look: { sepia: .18, strength: .34 } }; }, 'G');
P('G10', 'G10', (G, st) => { const g = G.g; G.kamera(720, 600, 1.2); tepeler(G, st, 600, { seed: 39, ust: .4 }); const k = acS(st, 'G10@dağıldı', 2);
  ordu(G, st, { x0: 100, x1: 1300, y: 780, s: 150, n: Math.round(lerp(20, 4, k)), v: .14, sancak: [{ x: 400, dus: k }, { x: 900, dus: k * .8 }] }); sis(G, st, 500, 900, .4 * k + .1, { v: .6, n: 8 });
  return { look: { sepia: .14, strength: .4 }, ust: etiket([{ text: 'Langside · 13 Mayıs 1568 · 45 dakika', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'O');

// ════════ H · SOLWAY (karar) ════════
bolumKarti('H');
function bozkir(G, st, ufuk, o = {}) { const g = G.g; G.gok(ufuk, { ust: o.ust ?? .45, alt: .82, isik: o.isik }); G.bulutlar(130, ufuk - 80, { seed: o.seed || 41, drift: st.t * 6, govde: .45 });
  G.kiyi(-400, 1900, ufuk + 4, 70, { v: .42, seed: 15, k: 6 }); const gr = g.createLinearGradient(0, ufuk, 0, 1080); gr.addColorStop(0, G.gri(.45)); gr.addColorStop(1, G.gri(.18)); g.fillStyle = gr; g.fillRect(-400, ufuk, 2300, 600); }
P('H01', ILK('H'), (G, st) => { G.kamera(lerp(600, 840, eio(st.p)), 560, 1); bozkir(G, st, 600, { isik: [1200, 560, 400, .9] });
  for (let i = 0; i < 4; i++) at(G, { x: 300 + st.lt * 140 + i * 210, y: 860 + (i % 2) * 40, s: 300, f: 1, ph: st.t * 1.6 + i * .27, v: .08, binici: { kind: i === 1 ? 'mary' : 'erkek', veil: .9, v: .08, pelerin: true } });
  return { look: { sepia: .14, strength: .38 } }; }, 'G');
KART('H03', 'H03', [Lq('“Doksan iki mil,', 'H03', { size: 78 }), Lq('durmadan, attan inmeden.', 'H03@durmadan', { size: 66 }), { text: '', size: 22 }, Ls('Mary, Carlisle\'dan · 21 Haziran 1568', S('H03') + 1, { size: 26 })], { level: 1 });
P('H03b', 'H03@sonra', (G, st) => { const g = G.g; G.kamera(720, 600, lerp(1, 1.08, st.p)); gece(G, st, { ufuk: 720, ay: [1150, 160] });
  g.strokeStyle = G.gri(.06); g.lineWidth = 18; g.beginPath(); g.moveTo(1240, 720); g.lineTo(1200, 300); g.lineTo(1000, 260); g.stroke(); g.fillStyle = G.gri(.06); g.fill(G.pathOf([[1060, 262], [1080, 220], [1100, 262], [1110, 300], [1050, 300]], true, .7)); g.beginPath(); g.arc(1080, 222, 24, 0, TAU); g.fill();   // dal ve baykuş
  isikHalka(G, 560, 860, 300, .35); g.fillStyle = G.gri(.5); for (let i = 0; i < 5; i++) { g.beginPath(); g.ellipse(540 + i * 12, 880 - Math.abs(Math.sin(st.t * 3 + i)) * 8, 10, 6, 0, 0, TAU); g.fill(); }   // köz
  G.figur({ kind: 'mary', x: 760, y: 900, s: 360, f: -1, poz: 'diz', kol: 'egik', t: st.t, veil: .4, v: .06, lean: 1.2 });
  return { look: { sepia: .08, strength: .44 }, exposure: .9 }; }, 'O');
KART('H03c', 'H03@üç', [Lq('“Üç gece,', 'H03@üç', { size: 84 }), Lq('baykuşlar gibi.”', 'H03@baykuşlar', { size: 84 })], { level: 1 });
P('H04', 'H04', (G, st) => { const g = G.g, ufuk = 640; G.kamera(720, 560, lerp(1.05, 1, st.p)); G.gok(ufuk, { ust: .5, alt: .88, isik: [720, 600, 500, .95] });
  for (let i = 0; i < 3; i++) { const x = 300 + i * 420; g.fillStyle = G.gri(.2); g.fillRect(x - 60, 160, 120, 760); g.fillStyle = G.gri(.4); g.fillRect(x - 60, 160, 30, 760); }
  g.strokeStyle = G.gri(.2); g.lineWidth = 70; for (let i = 0; i < 2; i++) { const x = 510 + i * 420; g.beginPath(); g.moveTo(x - 210, 330); g.quadraticCurveTo(x, 40, x + 210, 330); g.stroke(); }
  g.fillStyle = G.gri(.38); g.fillRect(-200, 920, 1900, 300);
  G.figur({ kind: 'mary', x: lerp(520, 700, st.p), y: 940, s: 360, f: 1, poz: 'yuru', walk: st.t * .5, kol: 'yan', t: st.t, veil: .9, v: .08 });
  return { look: { sepia: .14, strength: .36 }, ust: etiket([{ text: 'Dundrennan Manastırı · 15 Mayıs 1568', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'O');
P('H05', 'H05', (G, st) => { solway(G, st, { cam: [lerp(700, 860, eio(st.p)), 540, 1], ufuk: 520, sis: 1 - acS(st, 'H05@ingiltere', 2), isik: [1180, 480, 480, 1] });
  G.figur({ kind: 'mary', x: 420, y: 1070, s: 560, f: 1, kol: 'yan', t: st.t, veil: .95, v: .08, wind: .8 });
  return { look: { sepia: .12, strength: .34 } }; }, 'G');
P('H06', 'H06', (G, st) => { bataklik(G, st, { cam: [720, 600, 1.25] }); return { iris: lerp(.75, .62, st.p), look: { sepia: .5, strength: .48 }, ust: etiket([{ text: 'Solway Moss · 1542', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .2 }], { y: 160 }) }; }, 'A');
P('H07', 'H07', (G, st) => { solway(G, st, { cam: [720, 600, 1.25], ufuk: 560, sis: .6 });
  G.figur({ kind: 'mary', x: 760, y: 1050, s: 520, f: 1, kol: 'yan', t: st.t, veil: .95, v: .08 });
  G.figur({ kind: 'erkek', x: 480, y: 1060, s: 500, f: 1, kol: 'uzat', t: st.t, v: .1, sakal: true }); G.figur({ kind: 'erkek', x: 1080, y: 1060, s: 300, f: -1, poz: 'diz', kol: 'uzat', t: st.t, v: .1 }); G.figur({ kind: 'erkek', x: 300, y: 1070, s: 480, f: 1, kol: 'isaret', t: st.t, v: .12 });
  return { look: { sepia: .14, strength: .34 } }; }, 'O');
P('H08', 'H08', (G, st) => { G.kamera(720, 560, lerp(1, 1.15, eio(st.p))); G.zemin(.16); isikHalka(G, 600, 380, 900, .5); G.mektup(720, 540, 760, 600, -.04, { lh: 52, karalama: 6, prog: 1 });
  G.muhur(820, 720, 70, { acil: acS(st, 'H08@haberci', 1) }); return { look: { sepia: .3, strength: .26 } }; }, 'A');
P('H09', 'H09', (G, st) => { G.kamera(720, 560, lerp(1.1, 1.3, eio(st.p))); G.zemin(.12); isikHalka(G, 620, 360, 900, .5); yuzuk(G, 720, 520, 330, { t: st.t, parilti: .5 + .5 * Math.sin(st.t * 1.7) }); return { look: { sepia: .3, strength: .26 } }; }, 'Y');
P('H10', 'H10', (G, st) => { G.kamera(720, 560, 1.05); G.zemin(.16); isikHalka(G, 600, 380, 900, .45); G.g.fillStyle = G.gri(.3); G.g.fillRect(-200, 820, 1900, 400);
  kumSaati(G, 720, 600, 420, clamp(.05 + st.lt * .03), acS(st, 'H10@beklemedi', .9)); return { look: { sepia: .26, strength: .3 } }; }, 'A');
P('H11', 'H11', fotoP('mary_tamboy_18yy', [.47, .22, .5], [.47, .19, .34], { kunye: 'Mary Stuart · 18. yy gravürü · The Met (CC0)' }), 'Y');
P('H12', 'H12', (G, st) => { const bx = 400 + st.lt * 46;
  solway(G, st, { cam: [lerp(560, 900, eio(st.p)), 560, 1.0], sis: .2, ufuk: 480, isik: [1250, 450, 560, 1], gokUst: .45 });
  G.tekne({ x: bx, y: 780, s: 600, f: 1, t: st.t, oar: st.t * .9, sail: .9, yelken: .7, kisi: [
    { kind: 'erkek', x: .3, h: .3, poz: 'otur', kol: 'kurek', f: -1 }, { kind: 'erkek', x: .12, h: .3, poz: 'otur', kol: 'kurek', f: -1 },
    { kind: 'mary', x: -.2, h: .4, poz: 'otur', kol: 'onde', f: 1, kirmizi: 'etek', veil: .9, veilA: .6 }, { kind: 'erkek', x: -.4, h: .42, kol: 'yan', f: 1, sakal: true }] });
  dalgaOn(G, st, 920, 1080);
  return { look: { sepia: .12, strength: .34 }, ust: etiket([{ text: '16 Mayıs 1568', size: 40, font: 'Cormorant Garamond', italic: true, at: st.at + .4 }], { y: 110 }) }; }, 'G');
P('H13', 'H13', (G, st) => { const g = G.g, ufuk = 520; G.kamera(720, 560, lerp(1, 1.06, st.p)); G.gok(ufuk, { ust: .35, alt: .75, isik: [300, 500, 400, .9] }); G.deniz(ufuk, 820, { t: st.t, ufuk: .7, on: .5, n: 60 });
  const kum = g.createLinearGradient(0, 760, 0, 1080); kum.addColorStop(0, G.gri(.55)); kum.addColorStop(1, G.gri(.3)); g.fillStyle = kum; g.fill(G.pathOf([[-200, 820], [400, 780], [1000, 760], [1700, 790], [1700, 1200], [-200, 1200]], true, .5));
  G.tekne({ x: 520, y: 800, s: 520, f: -1, t: 0, sail: 0, kisi: [] });
  G.figur({ kind: 'mary', x: lerp(700, 860, eio(st.p)), y: 900, s: 400, f: 1, poz: 'yuru', walk: st.t * .5, kol: 'yan', t: st.t, veil: .9, v: .08 }); G.figur({ kind: 'erkek', x: lerp(560, 720, eio(st.p)), y: 900, s: 420, f: 1, poz: 'yuru', walk: st.t * .5 + .5, kol: 'yan', t: st.t, v: .1 });
  return { look: { sepia: .1, strength: .36 }, ust: etiket([{ text: 'Workington · akşam', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'O');
P('H13b', 'H13@ertesi', (G, st) => { yazMasa(G, st, { cam: [720, 620, 1.1], prog: st.p * 1.1, yazi: ['Je vous suplie le plus tost que pourrés', 'm\'envoyer quérir, car je suis en piteux estat…'], manset: 'kirmizi' }); return { look: { sepia: .3, strength: .28 } }; }, 'A');
KART('H14', 'H14', [Lq('“Size yalvarırım,', 'H14', { size: 72 }), Lq('beni bir an önce yanınıza çağırın.', 'H14@beni', { size: 60 }), { text: '', size: 22 }, Ls('Mary\'den Elizabeth\'e · Workington, 17 Mayıs 1568', S('H14') + 1, { size: 26 })], { level: 2 });
P('H14b', 'H14@acınacak', fotoP('mary_dul_moncornet', [.5, .42, .62], [.5, .4, .46], { kunye: 'Mary Stuart · B. Moncornet, 17. yy · The Met (CC0)', look: { sepia: .24 } }), 'Y');
P('H15', 'H15', (G, st) => { const g = G.g; G.kamera(lerp(620, 760, eio(st.p)), lerp(600, 680, eio(st.p)), 1.35); G.zemin(.14); isikHalka(G, 700, 500, 800, .5);
  G.mektup(720, 600, 1000, 640, -.03, { px: 44, lh: 66, yazi: ['Votre très fidelle et affectionnée bonne', 'sœur et cousine et eschappée prisonière,', 'Marie R.'], prog: clamp((st.t - AT('H15@sadık')) / (AT('H15@meri') + .6 - AT('H15@sadık'))) });
  const m = acS(st, 'H15@meri', 1); if (m > 0) G.muhur(1000, 820, 64, { acil: m });
  return { look: { sepia: .3, strength: .28 } }; }, 'A');
KART('H16', 'H16', [{ text: 'KAÇMIŞ TUTSAK', size: 104, font: 'Cinzel', weight: 700, spacing: 10, at: S('H16') }, { text: '', size: 26 }, Lq('Bu imza, ömrünün geri kalanının başlığı olacaktı.', 'H16@bu', { size: 46, weight: 500 })], { level: 0 });
P('H17', 'H17', fotoP('mary_clouet_beyazyas_resim', [.53, .32, .52], [.53, .3, .42], { kunye: 'Mary Stuart · Clouet\'nin 1561 portresinden kopya · NGS (kamu malı)', iris: st => 1 - .5 * acS(st, 'H17@bitmişti', 2.5) }), 'Y');

// ════════ I · ON DOKUZ YIL ════════
bolumKarti('I');
// I01–I05: Elizabeth üç kapalı kapının önünde (arkadan); her kapı sözcükte aralanır, ötesi görünür
function kapilar(G, st, o = {}) {
  const g = G.g; G.kamera(...(o.cam || [720, 560, 1])); G.zemin(.3); isikHalka(G, 720, 460, 900, .3);
  g.fillStyle = G.gri(.45); g.fillRect(-300, 820, 2100, 400);
  [[300, o.a1 || 0, o.d1], [720, o.a2 || 0, o.d2], [1140, o.a3 || 0, o.d3]].forEach(([x, a, dis], i) => {
    const w = 240, h = 520, y = 820 - h; g.fillStyle = G.gri(.12); g.fillRect(x - w / 2 - 26, y - 26, w + 52, h + 26); g.beginPath(); g.arc(x, y, w / 2 + 26, Math.PI, 0); g.fill();
    g.save(); g.beginPath(); g.rect(x - w / 2, y - w / 2, w, h + w / 2); g.clip(); g.fillStyle = G.gri(.9); g.fillRect(x - w / 2, y - w / 2, w, h + w / 2); if (dis && a > 0) dis(x, y + h, w, h); g.restore();
    const kw = w * (1 - a * .85); g.fillStyle = G.gri(.22); g.fillRect(x - w / 2, y, kw, h); g.beginPath(); g.moveTo(x - w / 2, y); g.arc(x, y, w / 2, Math.PI, 0); g.lineTo(x - w / 2 + kw, y); g.fill();
    g.fillStyle = G.gri(.36); for (let j = 0; j < 4; j++) g.fillRect(x - w / 2 + 8, y + 20 + j * 120, kw - 16, 10); g.fillStyle = G.gri(.6); g.beginPath(); g.arc(x - w / 2 + kw - 30, y + h * .55, 10, 0, TAU); g.fill();
  });
  if (o.eliz !== false) G.figur({ kind: 'eliz', x: o.ex ?? 720, y: 1060, s: 520, f: o.ef ?? 1, kol: 'onde', t: st.t, v: .06 });
}
P('I01', ILK('I'), (G, st) => { kapilar(G, st, { cam: [720, 560, lerp(1, 1.05, st.p)] }); return { look: { sepia: .22, strength: .32 } }; }, 'G');
P('I02', 'I02', (G, st) => { kapilar(G, st, { cam: [400, 560, 1.5], ex: 470, ef: -1, a1: acS(st, 'I02@serbest', 1.2), d1: (x, y, w, h) => ordu(G, st, { x0: x - w / 2, x1: x + w / 2, y: y - h * .2, s: 120, n: 6, v: .3, sancak: [{ x }] }) }); return { look: { sepia: .22, strength: .32 } }; }, 'O');
P('I03', 'I03', (G, st) => { kapilar(G, st, { cam: [720, 500, 1.9], eliz: false, a2: acS(st, 'I03@fransaya', 1.2), d2: (x, y, w, h) => { G.deniz(y - h * .5, y, { t: st.t, ufuk: .8, on: .5, n: 20 }); karaka(G, { x, y: y - h * .48, s: 90, v: .3 }); } }); return { look: { sepia: .22, strength: .32 } }; }, 'Y');
P('I04', 'I04', (G, st) => { kapilar(G, st, { cam: [1040, 560, 1.5], ex: 960, a3: acS(st, 'I04@öldürürse', 1.2), d3: (x, y, w, h) => { const k = acS(st, 'I04@tacını', 1.6); tac(G, x, lerp(y - h * .65, y - 40, k), 120, { v: .25, rot: k * 1.2 }); } }); return { look: { sepia: .22, strength: .34 } }; }, 'O');
P('I05', 'I05', (G, st) => { G.kamera(720, 560, 1.05); G.zemin(.16); isikHalka(G, 600, 380, 900, .45); G.g.fillStyle = G.gri(.3); G.g.fillRect(-200, 820, 1900, 400); kumSaati(G, 720, 600, 440, clamp(.1 + st.lt * .08)); return { look: { sepia: .26, strength: .3 } }; }, 'A');
P('I06', 'I06', (G, st) => { const g = G.g, ufuk = 620; G.kamera(lerp(680, 760, st.p), 560, 1); G.gok(ufuk, { ust: .45, alt: .8 }); G.bulutlar(140, 520, { seed: 43, drift: st.t * 4 });
  kale(G, 360, ufuk + 4, 700, [{ t: 'sur', x: .5, w: 1.1, h: .2 }, { x: .25, w: .3, h: .55, pen: 3 }, { x: .05, w: .1, h: .32 }, { x: .95, w: .12, h: .35 }, { x: .7, w: .14, h: .28 }], { v: .2 }); g.fillStyle = G.gri(.4); g.fillRect(-300, ufuk, 2100, 500);
  return { look: { sepia: .16, strength: .36 }, ust: etiket([{ text: 'Carlisle Kalesi · 1568', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
KART('I06k', AT('I06@bir#3') - .2, [Lq('“Bir tutsaktan', AT('I06@bir#3'), { size: 84 }), Lq('pek farkım yok.”', AT('I06@pek'), { size: 84 }), { text: '', size: 22 }, Ls('Mary, Carlisle\'dan · 21 Haziran 1568', AT('I06@bir#3') + 1, { size: 26 })]);
P('I07', 'I07', masaP('hayali_bulusma_currier', { boy: 900, k0: [720, 520, 1.05], k1: [720, 470, 1.2], kunye: '"Rakip Kraliçeler" · Currier & Ives, 1868–70 · The Met (CC0)',
  ust: etiket([{ text: 'Hayal (1868–70). Böyle bir buluşma hiç olmadı.', size: 38, font: 'Cormorant Garamond', italic: true, weight: 600, at: S('I07') + .6 }], { y: 800 }),
  nesne: (G, st) => { const k = acS(st, 'I07@reddetti', 1.4); if (k <= 0) return; const g = G.g, w = 160 * k, L = [], R = [];
    for (let i = 0; i <= 14; i++) { const y = -100 + i * 90, j = (i % 2 ? 1 : -1) * 22; L.push([720 + j - w / 2, y]); R.push([720 + j + w / 2, y]); }
    g.fillStyle = G.gri(.2); g.fill(G.polyP([...L, ...R.reverse()])); g.strokeStyle = G.gri(.95); g.lineWidth = 5; g.beginPath(); L.forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.stroke(); g.beginPath(); R.reverse().forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.stroke(); } }), 'O');
P('I08', 'I08', (G, st) => { const g = G.g; salon(G, st, { cam: [720, 600, lerp(1, 1.06, st.p)], duvar: .26, zeminV: .42, pencere: 3 }); g.fillStyle = G.gri(.18); g.fillRect(260, 760, 920, 60); g.fillStyle = G.gri(.8); g.fillRect(250, 740, 940, 24);
  for (let i = 0; i < 6; i++) G.figur({ kind: 'erkek', x: 320 + i * 160, y: 760, s: 300, f: i < 3 ? 1 : -1, poz: 'otur', kol: 'onde', t: st.t, v: .1, sakal: i % 2 === 0 });
  const k = acS(st, 'I08@mektuplar', 1.2); sandik(G, 720, lerp(500, 742, k), 180, 0, {});
  return { look: { sepia: .22, strength: .32 }, ust: etiket([{ text: 'York ve Westminster · 1568–69', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('I09', 'I09', (G, st) => { harita(G, st, { k0: [-2.0, 53.6, 1.7], k1: [-1.4, 53.1, 1.9], isaretler: [{ yer: 'carlisle', tur: 'kale' }, { yer: 'tutbury', tur: 'kale', a: acS(st, 'I09@tatberi', .6) }, { yer: 'sheffield', tur: 'kale', a: acS(st, 'I09@şefild', .6) }, { yer: 'chartley', a: acS(st, 'I09@çartli', .6) }, { ll: [-1.96, 54.32], tur: 'kale' }],
  yollar: [{ pts: [[-2.94, 54.9], [-1.96, 54.32], [-1.69, 52.86], [-1.47, 53.38], [-1.98, 52.85]], p: acS(st, 'I09@tatberi', 3.4), kesik: true, kirmizi: true, w: 6 }], yazilar: [['BOLTON', -1.5, 54.45, 24], ['TUTBURY', -1.3, 52.7, 24, acS(st, 'I09@tatberi', .6)], ['SHEFFIELD', -1.1, 53.5, 24, acS(st, 'I09@şefild', .6)], ['CHARTLEY', -2.5, 52.75, 24, acS(st, 'I09@çartli', .6)]] }); return { look: { sepia: .3, strength: .26 } }; }, 'A');
// I10: iğne ve iplik (işleme kasnağı)
function isleme(G, st, o = {}) { const g = G.g; G.kamera(...(o.cam || [720, 560, 1])); G.zemin(.16); isikHalka(G, 600, 400, 900, .5);
  g.fillStyle = G.gri(.82); g.fillRect(260, 160, 920, 760); g.strokeStyle = G.gri(.3); g.lineWidth = 26; g.strokeRect(250, 150, 940, 780);
  g.save(); g.beginPath(); g.rect(260, 160, 920, 760); g.clip(); g.globalAlpha = .12; g.fillStyle = G.gri(.2); for (let y = 160; y < 920; y += 8) g.fillRect(260, y, 920, 2); for (let x = 260; x < 1180; x += 8) g.fillRect(x, 160, 2, 760); g.restore();
  if (o.anka != null) anka(G, 720, 600, 300, o.anka, st.t);
  if (o.yazi) { g.fillStyle = G.gri(.18); g.font = 'italic 600 54px "Cormorant Garamond"'; g.textAlign = 'center'; g.save(); g.beginPath(); g.rect(260, 800, 920 * clamp(o.yaziP ?? 1), 100); g.clip(); g.fillText(o.yazi, 720, 860); g.restore(); } }
function anka(G, x, y, s, k, t) { const g = G.g;   // alevlerden yükselen anka (yandan): kıvrık kanatlar, tepelik, uzun kuyruk tüyleri; k: işlenme ilerlemesi
  g.save(); g.beginPath(); g.rect(x - s * 2, y + s * .9 - s * 2.4 * k, s * 4, s * 3); g.clip();
  for (let i = -4; i <= 4; i++) { const h = s * (.45 + .3 * Math.cos(i * .7)) * (1 + .05 * Math.sin(t * 3 + i)); g.fillStyle = G.gri(i % 2 ? .4 : .58); g.fill(G.pathOf([[x + i * s * .15 - s * .1, y + s * .9], [x + i * s * .15 + s * .05 * Math.sin(t * 2 + i), y + s * .9 - h], [x + i * s * .15 + s * .1, y + s * .9]], true, .9)); }
  g.fillStyle = G.gri(.2);
  g.fill(G.pathOf([[x - s * .05, y + s * .35], [x - s * .2, y + s * .05], [x - s * .12, y - s * .25], [x + s * .02, y - s * .4], [x + s * .1, y - s * .55], [x + s * .2, y - s * .58], [x + s * .3, y - s * .52], [x + s * .22, y - s * .48], [x + s * .14, y - s * .4], [x + s * .12, y - s * .2], [x + s * .1, y + s * .1], [x + s * .05, y + s * .35]], true, .7));   // gövde, boyun, baş
  g.fill(G.pathOf([[x + s * .12, y - s * .58], [x + s * .06, y - s * .72], [x + s * .14, y - s * .64], [x + s * .16, y - s * .78], [x + s * .2, y - s * .62]], true, .6));   // tepelik
  for (const [d, sc] of [[-1, 1], [1, .8]]) { const pts = [[x, y - s * .2]]; for (let j = 0; j <= 6; j++) { const a = -1.9 + j * .28, r = s * (.7 + .25 * Math.sin(j * 1.3)) * sc; pts.push([x + d * Math.cos(a + (d < 0 ? 0 : .15)) * r * 1.1, y - s * .2 + Math.sin(a) * r * .9]); pts.push([x + d * Math.cos(a + .12) * r * .78, y - s * .2 + Math.sin(a + .12) * r * .68]); } pts.push([x + d * s * .1, y]); g.fill(G.pathOf(pts, true, .5)); }   // kanatlar (tüy uçlu)
  for (let j = 0; j < 4; j++) { g.strokeStyle = G.gri(.22); g.lineWidth = s * .03; g.beginPath(); g.moveTo(x, y + s * .3); g.quadraticCurveTo(x - s * (.3 + j * .12), y + s * .55, x - s * (.2 + j * .2), y + s * (.75 - j * .05)); g.stroke(); }   // kuyruk
  g.restore(); }
P('I10', 'I10', (G, st) => { isleme(G, st, { cam: [760, 640, 2.2], anka: .3 + st.p * .2 }); const g = G.g, k = (st.lt * .8) % 1, x = 800 + k * 40, y = 700 - Math.sin(k * Math.PI) * 160;
  g.strokeStyle = G.gri(.3); g.lineWidth = 2; g.beginPath(); g.moveTo(760, 720); g.quadraticCurveTo(780, 600, x, y); g.stroke(); g.fillStyle = G.gri(.85); g.save(); g.translate(x, y); g.rotate(-.6); g.fillRect(-3, -60, 6, 70); g.restore();
  return { look: { sepia: .32, strength: .26 } }; }, 'Y');
// I11: tahtın sayvanı, işlenmiş söz; ziyaretçi bakar
P('I11', 'I11', (G, st) => { const g = G.g; G.kamera(720, 540, lerp(1, 1.08, st.p)); oda(G, st, { duvar: .24, zeminY: 880 });
  g.fillStyle = G.gri(.18); g.fillRect(470, 100, 500, 600); g.fillStyle = G.gri(.6); g.fillRect(500, 150, 440, 520); g.fillStyle = G.gri(.14); g.fill(G.pathOf([[440, 90], [1000, 90], [990, 170], [930, 150], [870, 175], [810, 150], [750, 175], [690, 150], [630, 175], [570, 150], [510, 175], [450, 160]], true, .4));
  g.fillStyle = G.gri(.2); g.font = 'italic 600 34px "Cormorant Garamond"'; g.textAlign = 'center'; g.fillText('En ma fin est mon commencement', 720, 560);
  g.fillStyle = G.gri(.16); g.fillRect(600, 640, 240, 260); g.fillRect(580, 620, 280, 40);
  G.figur({ kind: 'erkek', x: 260, y: 960, s: 560, f: 1, kol: 'yan', t: st.t, v: .08, sakal: true, head: -.15 });
  return { look: { sepia: .26, strength: .3 }, ust: etiket([{ text: 'Tutbury · 1569', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'O');
KART('I12', 'I12', [Lq('En ma fin est mon commencement.', 'I12', { size: 70 }), { text: '', size: 18 }, { text: 'SONUMDA BAŞLANGICIM', size: 52, font: 'Cinzel', weight: 700, spacing: 6, at: AT('I12@sonumda') }], { level: 2 });
P('I13', 'I13', (G, st) => { isleme(G, st, { cam: [720, 560, lerp(1.25, 1.35, st.p)], anka: acS(st, 'I13@ateşin', 2.4), yazi: 'En ma fin git mon commencement', yaziP: acS(st, 'I13@yazılıydı', 1.5) }); return { look: { sepia: .32, strength: .26 } }; }, 'Y');
// I14: satranç: kırmızı vezir ortada, planlar (taşlar) çevresinde düşer; zincir
P('I14', 'I14', (G, st) => { const k1 = acS(st, 'I14@kuzeyin', 1.5), k2 = acS(st, 'I14@italyan', 1.5), z = acS(st, 'I14@zincir', 2);
  satranc(G, st, { cam: [720, lerp(640, 600, st.p), lerp(1.1, 1.5, eio(st.p))], taslar: [{ tip: 'vezir', renk: 'kirmizi', u: 3.5, v: 3.5 }, { tip: 'at', renk: 'siyah', u: 2, v: 5, f: 1, dus: k1 }, { tip: 'at', renk: 'siyah', u: 5, v: 5, f: -1, dus: k1 }, { tip: 'fil', renk: 'siyah', u: 5, v: 2, dus: k2 }, { tip: 'vezir', renk: 'beyaz', u: 0, v: 7 }] });
  if (z > 0) { const g = G.g, [x, y, k] = tahtaNokta(4, 4); g.strokeStyle = G.gri(.2); g.lineWidth = 10 * k; for (let i = 0; i < 8 * z; i++) { const yy = y - 20 * k - i * 18 * k; g.beginPath(); g.ellipse(x + (i % 2 ? 6 : -6) * k, yy, 38 * k, 12 * k, 0, 0, TAU); g.stroke(); } }
  return { look: { sepia: .24, strength: .32 } }; }, 'A');
P('I14b', 'I14@kuzeyin', (G, st) => { G.kamera(720, 560, 1); tepeler(G, st, 580, { seed: 45, ust: .38 }); ordu(G, st, { x0: 100, x1: 1340, y: 760, s: 140, n: 22, v: .12, sancak: [{ x: 360 }, { x: 760 }, { x: 1120 }] });
  return { look: { sepia: .16, strength: .38 }, ust: etiket([{ text: 'Kuzeyin ayaklanması · 1569', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('I14c', AT('I14@italyan') - .4, (G, st) => { G.kamera(720, 560, lerp(1.05, 1.15, st.p)); G.zemin(.16); isikHalka(G, 600, 380, 900, .5); G.mektup(720, 560, 820, 720, .04, { px: 34, lh: 50, yazi: ['Ridolfi · 1571', '…', '…'], prog: 1 }); return { look: { sepia: .3, strength: .28 } }; }, 'Y');
P('I14d', AT('I14@her') - .2, (G, st) => { const z = acS(st, 'I14@zincir', 2); satranc(G, st, { cam: [720, 560, 1.9], taslar: [{ tip: 'vezir', renk: 'kirmizi', u: 3.5, v: 3.5 }] });
  const g = G.g, [x, y, k] = tahtaNokta(4, 4); g.strokeStyle = G.gri(.18); g.lineWidth = 12 * k; for (let i = 0; i < Math.round(9 * z); i++) { const yy = y - 18 * k - i * 17 * k; g.beginPath(); g.ellipse(x + (i % 2 ? 7 : -7) * k, yy, 40 * k, 12 * k, 0, 0, TAU); g.stroke(); }
  return { look: { sepia: .22, strength: .34 } }; }, 'A');
P('I15', 'I15', fotoP('james_dejode_1603', [.5, .5, .8], [.5, .42, .55], { kunye: 'VI. James · Pieter de Jode, 1603 · The Met (CC0)' }), 'Y');
P('I15b', 'I15@yıllık', (G, st) => { const g = G.g; G.kamera(720, 600, lerp(1.1, 1.25, st.p)); G.zemin(.16); isikHalka(G, 640, 420, 800, .5); g.fillStyle = G.gri(.28); g.fillRect(-200, 700, 1900, 500);
  const q = G.rng(8); for (let i = 0; i < 14 * clamp(st.lt / 1.5); i++) { const x = 600 + q() * 260, y = 760 - i * 10; g.fillStyle = G.gri(.7); g.beginPath(); g.ellipse(x, y, 54, 16, 0, 0, TAU); g.fill(); g.fillStyle = G.gri(.4); g.fillRect(x - 54, y, 108, 8); }
  return { look: { sepia: .32, strength: .28 } }; }, 'A');
P('I16', 'I16', (G, st) => { galeri(G, st, { cam: [720, 600, 1.15] }); G.g.fillStyle = G.gri(0, .3); G.g.fillRect(-300, -300, 2100, 1700);
  G.figur({ kind: 'mary', x: 380 + st.lt * 28, y: 1000, s: 560, f: 1, poz: 'yuru', walk: st.t * .3, kol: 'tut', t: st.t, veil: .9, v: .08, lean: .1 });
  return { look: { sepia: .2, strength: .32 } }; }, 'O');
// I17: Walsingham (siluet, arkadan): mumlu masa, mektup yığınları; adında başını çevirir
P('I17', 'I17', (G, st) => { const g = G.g; G.kamera(800, 640, lerp(1.4, 1.5, st.p)); G.zemin(.08); isikHalka(G, 900, 600, 700, .5);
  g.fillStyle = G.gri(.3); g.fillRect(420, 720, 900, 30); g.fillStyle = G.gri(.18); g.fillRect(440, 750, 860, 400); for (let i = 0; i < 6; i++) G.mektup(980 + i * 30, 700 - i * 8, 260, 40, .02 * i, { yazi: [], v: .85 - i * .03 });
  G.mum(1180, 720, 160, st.t, { r: 10 }); const k = acS(st, 'I17@volsingım', 1.2);
  G.figur({ kind: 'erkek', x: 700, y: 1000, s: 620, f: 1, poz: 'otur', kol: 'yaz', t: st.t, v: .04, sapka: false, sakal: true, head: lerp(0, -.25, k) });
  return { look: { sepia: .12, strength: .4 }, ust: etiket([{ text: 'Francis Walsingham', size: 46, weight: 700, spacing: 6, at: AT('I17@frensis') }], { y: 780 }) }; }, 'Y');

// ════════ J · BİRA FIÇISINDAKİ MEKTUPLAR ════════
bolumKarti('J');
P('J01', ILK('J'), (G, st) => { const g = G.g, ufuk = 600; G.kamera(lerp(700, 760, st.p), 560, 1); G.gok(ufuk, { ust: .45, alt: .82 }); G.bulutlar(140, 520, { seed: 47, drift: st.t * 4 });
  kale(G, 380, ufuk + 4, 680, [{ t: 'ev', x: .3, w: .5, h: .3, cati: 'beşik', pen: 5 }, { x: .05, w: .1, h: .4, cati: 'konik' }, { t: 'ev', x: .8, w: .4, h: .26, cati: 'beşik', pen: 4 }], { v: .22 });
  G.deniz(ufuk + 4, ufuk + 60, { t: st.t, ufuk: .6, on: .5, n: 10 }); g.fillStyle = G.gri(.4); g.fillRect(-300, ufuk + 60, 2100, 500);
  ordu(G, st, { x0: 300, x1: 900, y: 820, s: 160, n: 4, v: .1 });
  return { look: { sepia: .16, strength: .36 }, ust: etiket([{ text: 'Chartley · 1586', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
function fici(G, x, y, s, o = {}) { const g = G.g, gr = g.createLinearGradient(x - s * .4, 0, x + s * .4, 0); gr.addColorStop(0, G.gri(.25)); gr.addColorStop(.35, G.gri(.55)); gr.addColorStop(1, G.gri(.18)); g.fillStyle = gr;
  g.fill(G.pathOf([[x - s * .32, y - s * .5], [x + s * .32, y - s * .5], [x + s * .4, y], [x + s * .32, y + s * .5], [x - s * .32, y + s * .5], [x - s * .4, y]], true, .6));
  g.fillStyle = G.gri(.12); for (const k of [-.36, -.14, .14, .36]) g.fillRect(x - s * .4, y + k * s - s * .02, s * .8, s * .04);
  if (o.tapa != null) { g.fillStyle = G.gri(.08); g.beginPath(); g.arc(x, y, s * .05, 0, TAU); g.fill(); g.fillStyle = G.gri(.45); g.beginPath(); g.arc(x - o.tapa * s * .3, y - o.tapa * s * .2, s * .05, 0, TAU); g.fill(); } }
P('J02', 'J02', (G, st) => { const g = G.g; G.kamera(720, 540, lerp(1.1, 1.3, st.p)); G.zemin(.12); isikHalka(G, 600, 400, 800, .5); fici(G, 720, 600, 760, { tapa: acS(st, 'J02@açıldı', 1) });
  const k = acS(st, 'J02@açıldı', 1.6); if (k > 0) { g.fillStyle = G.gri(.75); g.save(); g.translate(720, 600 - k * 120); g.rotate(-.2); g.fillRect(-50, -30, 100, 60); g.fillStyle = G.gri(.5); g.fillRect(-50, -4, 100, 8); g.restore(); }
  return { look: { sepia: .26, strength: .32 } }; }, 'A');
P('J03', 'J03', (G, st) => { const g = G.g, ufuk = 600; G.kamera(720, 560, 1); G.gok(ufuk, { ust: .5, alt: .85 }); g.fillStyle = G.gri(.42); g.fillRect(-300, ufuk, 2100, 500);
  kale(G, 900, ufuk + 4, 600, [{ t: 'ev', x: .4, w: .6, h: .32, cati: 'beşik', pen: 5 }], { v: .24 }); const x = lerp(100, 900, st.p);
  for (let i = 0; i < 3; i++) fici(G, x - 120 + i * 120, 760, 130, {}); g.fillStyle = G.gri(.14); g.fillRect(x - 220, 820, 360, 20); for (const dx of [-160, 80]) { g.beginPath(); g.arc(x + dx, 860, 50, 0, TAU); g.fill(); }
  at(G, { x: x + 260, y: 880, s: 260, f: 1, ph: st.t * .7, dur: false, v: .1 }); G.figur({ kind: 'erkek', x: x + 420, y: 885, s: 340, f: 1, poz: 'yuru', walk: st.t * .7, kol: 'tut', t: st.t, v: .1 });
  return { look: { sepia: .22, strength: .32 }, ust: etiket([{ text: 'Burton\'lu biracı', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('J04', 'J04', (G, st) => { yazMasa(G, st, { cam: [720, 620, 1.12], prog: st.p * 1.1, yazi: ['ƆϽ Ꝋ ʘ ϟ ꝏ ∆ ⊕ ∞', '⊗ ϟ ∆ ꝏ ʘ Ɔ ϡ ⊕'], manset: 'kirmizi' }); return { look: { sepia: .3, strength: .28 } }; }, 'Y');
// J05: Walsingham'ın masası: mühür kaldırılır, şifre, kopya, yeniden mühür
P('J05', 'J05', (G, st) => { const g = G.g; G.kamera(lerp(680, 780, eio(st.p)), 560, 1.0); G.zemin(.12); isikHalka(G, 1000, 380, 900, .5);
  const m = acS(st, 'J05@masasına', 1), s2 = acS(st, 'J05@şifresi', .8), k = acS(st, 'J05@kopyalanıyor', 1.2), y = acS(st, 'J05@yoluna', 1);
  G.mektup(lerp(-300, 520, m), 520, 560, 660, -.05, { px: 32, lh: 48, yazi: s2 > 0 ? ['ƆϽ Ꝋ ʘ ϟ ꝏ ∆ ⊕ ∞ ϡ', '⊗ ϟ ∆ ꝏ ʘ Ɔ ϡ ⊕ ∞', 'Ꝋ ϟ ʘ ∆ ⊕ ꝏ Ɔ ϡ'] : [], prog: s2 });
  if (k > 0) G.mektup(lerp(1700, 1060, k), 560, 520, 640, .06, { lh: 46, karalama: 8, seed: 5, prog: k, v: .88 });
  G.muhur(lerp(-300, 680, m), 780, 50, { acil: y > 0 ? y : 1 - s2 });
  return { look: { sepia: .26, strength: .3 } }; }, 'A');
P('J06', 'J06', (G, st) => { const g = G.g; G.kamera(720, 600, lerp(1, 1.06, st.p)); G.zemin(.1); isikHalka(G, 720, 650, 640, .55); g.fillStyle = G.gri(.26); g.fillRect(380, 720, 680, 30); G.mum(720, 720, 140, st.t, { r: 10 });
  for (const [x, f] of [[420, 1], [560, 1], [880, -1], [1020, -1]]) G.figur({ kind: 'erkek', x, y: 960, s: 520, f, poz: 'otur', kol: 'onde', t: st.t, v: .06, sakal: x % 3 === 0 });
  G.figur({ kind: 'erkek', x: 720, y: 980, s: 600, f: 1, kol: 'yaz', t: st.t, v: .04, sapka: false });
  return { look: { sepia: .14, strength: .4 }, ust: etiket([{ text: 'Anthony Babington · Temmuz 1586', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .4 }], { y: 110 }) }; }, 'O');
P('J07', 'J07', (G, st) => { G.kamera(720, 560, lerp(1.15, 1.3, st.p)); G.zemin(.16); isikHalka(G, 600, 380, 900, .5); G.mektup(720, 560, 760, 600, -.04, { px: 34, lh: 50, yazi: ['ƆϽ Ꝋ ʘ ϟ ꝏ ∆ ⊕ ∞', '⊗ ϟ ∆ ꝏ ʘ Ɔ ϡ ⊕'], prog: 1 }); G.muhur(860, 740, 64, { acil: acS(st, 'J07@cevap', .7) }); return { look: { sepia: .3, strength: .26 } }; }, 'Y');
P('J06b', 'J06@plan', (G, st) => { G.kamera(720, 560, lerp(1.1, 1.25, st.p)); G.zemin(.14); isikHalka(G, 640, 380, 900, .5); G.mektup(720, 560, 820, 700, -.03, { px: 34, lh: 52, yazi: ['ƆϽ Ꝋ ʘ ϟ ꝏ ∆ ⊕ ∞ ϡ ⊗', 'ϟ ∆ ꝏ ʘ Ɔ ϡ ⊕ ∞ Ꝋ', 'ʘ ∆ ⊕ ꝏ Ɔ ϡ ϟ ∆', '⊗ ∞ Ꝋ ʘ ϟ'], prog: clamp(st.lt / 5) }); return { look: { sepia: .3, strength: .28 }, ust: kunye('Babington\'ın şifreli mektubu · Temmuz 1586 · canlandırma') }; }, 'A');
KART('J08', 'J08@o', [Lq('“O zaman altı beyefendiyi', 'J08@o', { size: 70 }), Lq('işe koşmanın vakti gelecek.”', 'J08@işe', { size: 70 }), { text: '', size: 22 }, Ls('Mary\'nin 17 Temmuz 1586 mektubu · çözülmüş kopya', AT('J08@o') + 1, { size: 26 })]);
P('J08a', 'J08', (G, st) => { G.kamera(720, 560, 1.2); G.zemin(.16); isikHalka(G, 600, 380, 900, .5); G.mektup(720, 560, 760, 700, .03, { lh: 50, karalama: 10, seed: 5, prog: 1, v: .88 }); return { look: { sepia: .3, strength: .28 }, ust: kunye('Çözülmüş kopya · Temmuz 1586 · canlandırma') }; }, 'A');
P('J09', 'J09', (G, st) => { const g = G.g; G.kamera(720, 600, 1.05); G.zemin(.2); isikHalka(G, 720, 500, 800, .4); g.fillStyle = G.gri(.3); g.fillRect(-200, 900, 1900, 300);
  for (let i = 0; i < 6; i++) { const a = acS(st, AT('J09') + i * .35, .5); if (a <= 0) continue; G.figur({ kind: 'erkek', x: 220 + i * 200, y: 960, s: 560, f: i < 3 ? 1 : -1, kol: 'yan', t: st.t, v: lerp(.6, .06, a), pelerin: true }); }
  return { look: { sepia: .16, strength: .38 } }; }, 'O');
P('J10', 'J10', (G, st) => { const g = G.g; G.kamera(720, 520, lerp(1.2, 1.35, st.p)); G.zemin(.16); isikHalka(G, 600, 380, 900, .5); G.mektup(720, 600, 820, 760, .03, { lh: 50, karalama: 11, seed: 5, prog: 1, v: .9 });
  const k = clamp((st.t - AT('J10@darağacı') + .3) / 1.6); g.strokeStyle = G.gri(.08); g.lineWidth = 7; g.lineCap = 'round'; const seg = [[[620, 470], [620, 300]], [[620, 300], [720, 300]], [[720, 300], [720, 340]], [[580, 470], [660, 470]]];
  seg.forEach(([a, b], i) => { const f = clamp(k * 4 - i); if (f <= 0) return; g.beginPath(); g.moveTo(...a); g.lineTo(lerp(a[0], b[0], f), lerp(a[1], b[1], f)); g.stroke(); });
  return { look: { sepia: .3, strength: .28 }, ust: kunye('Phelippes\'in kopyaya çizdiği darağacı (1586) · canlandırma') }; }, 'A');
function fotheringhay(G, st, o = {}) { const g = G.g, ufuk = 620; G.gok(ufuk, { ust: o.ust ?? .42, alt: .78 }); G.bulutlar(140, 520, { seed: 49, drift: st.t * 4, govde: .4 });
  g.fillStyle = G.gri(.32); g.fill(G.pathOf([[200, ufuk + 6], [420, ufuk - 80], [700, ufuk - 96], [960, ufuk - 70], [1200, ufuk + 6]], true, .5));
  kale(G, 360, ufuk - 80, 800, [{ t: 'sur', x: .5, w: .9, h: .14 }, { x: .5, w: .26, h: .36, cati: 'mazgal', pen: 3 }, { x: .12, w: .1, h: .24 }, { x: .88, w: .1, h: .24 }], { v: .16, isik: .3, gece: o.gece });
  G.deniz(ufuk + 6, 760, { t: st.t, ufuk: .6, on: .5, n: 20 }); g.fillStyle = G.gri(.3); g.fillRect(-300, 760, 2100, 500); }
P('J11', 'J11', (G, st) => { G.kamera(lerp(680, 760, st.p), 560, 1); fotheringhay(G, st); at(G, { x: lerp(100, 600, st.p), y: 900, s: 200, f: 1, ph: st.t, v: .1, binici: { kind: 'erkek', v: .1 } });
  return { look: { sepia: .14, strength: .38 }, ust: etiket([{ text: 'Fotheringhay · Eylül 1586', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
function dava(G, st, o = {}) { const g = G.g; salon(G, st, { cam: o.cam, duvar: .24, zeminV: .4, pencere: 3, pencereV: .7 });
  for (let r = 0; r < 2; r++) for (let i = 0; i < 6; i++) G.figur({ kind: 'erkek', x: 820 + i * 100 + r * 50, y: 760 + r * 70, s: 260 + r * 30, f: -1, poz: 'otur', kol: 'onde', t: st.t, v: .08, sakal: (i + r) % 2 === 0 });
  g.fillStyle = G.gri(.14); g.fillRect(260, 760, 120, 140); G.figur({ kind: 'mary', x: 330, y: 900, s: 330, f: 1, poz: 'otur', kol: o.kol || 'onde', t: st.t, veil: .9, v: .06 }); }
P('J12', 'J12', (G, st) => { dava(G, st, { cam: [560, 680, lerp(1.35, 1.42, st.p)] }); return { look: { sepia: .18, strength: .34 } }; }, 'O');
KART('J12k', AT('J12@vicdanınıza') + .1, [Lq('“Vicdanınıza bakın ve unutmayın:', 'J12@vicdanınıza', { size: 60 }), Lq('bütün dünya sahnesi', 'J12@bütün', { size: 70 }), Lq('İngiltere krallığından daha geniştir.”', 'J12@ingiltere', { size: 60 }), { text: '', size: 22 }, Ls('Mary, Fotheringhay\'deki yargıçlarına · Ekim 1586 · Camden\'ın aktarımı', AT('J12@vicdanınıza') + 1, { size: 26 })], { level: 1 });
P('J13', 'J13', (G, st) => { dava(G, st, { cam: [720, 600, lerp(1, .96, st.p)], kol: 'yan' }); return { look: { sepia: .14, strength: .38 }, exposure: lerp(1, .85, st.p) }; }, 'G');
P('J13b', 'J13@geriye', (G, st) => { G.kamera(720, lerp(600, 760, eio(st.p)), lerp(1, 1.3, eio(st.p))); belge(G, st, { baslik: 'FERMAN · 1587', satir: 10, seed: 9 }); return { look: { sepia: .3, strength: .28 } }; }, 'A');

// ════════ K · ELIZABETH, ELIZABETH'E KARŞI ════════
bolumKarti('K');
P('K01', ILK('K'), fotoP('elizabeth_depasse_1592', [.5, .31, .44], [.5, .3, .32], { kunye: 'I. Elizabeth · Crispijn de Passe, 1592 · The Met (CC0)' }), 'Y');
// K02: aynı gravür ve aynadaki eşi: Elizabeth, Elizabeth'e karşı
P('K02', 'K02', (G, st) => { const g = G.g, im = IMG.elizabeth_depasse_1592; G.zemin(.08); if (!im) return {}; const W = im.naturalWidth, H = im.naturalHeight, c = BOYA.griOn(im, 1.12, 1.03), ay = acS(st, 'K02@kendi', 2);
  const sw = W * .42, sh = sw * 1080 / 700, sx = W * .29, sy = H * .12, k = lerp(1, 1.05, st.p);
  g.save(); g.translate(720, 540); g.scale(k, k); g.translate(-720, -540);
  g.drawImage(c, sx, sy, sw, sh, 0, 0, 700, 1080);
  g.save(); g.translate(1440, 0); g.scale(-1, 1); g.globalAlpha = lerp(.35, 1, ay); g.drawImage(c, sx, sy, sw, sh, 0, 0, 700, 1080); g.restore();
  g.fillStyle = G.gri(.05); g.fillRect(700, 0, 40, 1080); g.restore();
  return { look: { sepia: .22, strength: .34 }, ust: kunye('Aynı gravür ve ayna görüntüsü (de Passe, 1592)') }; }, 'O');
P('K03', 'K03', (G, st) => { const g = G.g; salon(G, st, { cam: [720, 600, lerp(1, 1.05, st.p)], duvar: .28, zeminV: .45, pencere: 3 });
  for (let r = 0; r < 3; r++) for (let i = 0; i < 9; i++) G.figur({ kind: 'erkek', x: 120 + i * 150 + r * 40, y: 800 + r * 90, s: 240 + r * 50, f: 1, poz: 'otur', kol: r === 2 && i === 4 && ac(st, 'K03@idam') > 0 ? 'kaldir' : 'onde', t: st.t, v: .07 + r * .02, sakal: (i + r) % 3 === 0 });
  return { look: { sepia: .2, strength: .32 }, ust: etiket([{ text: 'Parlamento · Kasım 1586', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
KART('K04', 'K04', [Lq('“Dileğinizi kabul etmeyeceğim desem,', 'K04', { size: 58 }), Lq('belki düşündüğümden fazlasını söylemiş olurum.', 'K04@belki', { size: 50 }), { text: '', size: 22 }, Ls('Elizabeth, Parlamento\'ya · 24 Kasım 1586', S('K04') + 1, { size: 26 })], { level: 1 });
P('K04b', AT('K04@kabul#1') - .2, fotoP('elizabeth_huys', [.53, .27, .32], [.53, .27, .24], { kunye: 'I. Elizabeth · Frans Huys\'a atfedilir · The Met (CC0)' }), 'Y');
KART('K04c', AT('K04@size') - .2, [Lq('“Size', 'K04@size', { size: 70 }), { text: 'CEVAPSIZ BİR CEVAP', size: 82, font: 'Cinzel', weight: 700, spacing: 6, at: AT('K04@cevapsız') }, Lq('vermek zorundayım.”', 'K04@vermek', { size: 70 })], { level: 1 });
P('K05', 'K05', (G, st) => { G.kamera(720, lerp(640, 760, eio(st.p)), lerp(1.05, 1.3, eio(st.p))); belge(G, st, { baslik: 'FERMAN · 1587', satir: 10, seed: 9, imza: acS(st, 'K05@imzaladı', 1.6) }); const k = acS(st, 'K05@imzaladı', 1.6);
  if (k < 1) el(G, lerp(700, 1080, k), 840, 340, { manset: 'dantel' }); return { look: { sepia: .3, strength: .28 }, ust: etiket([{ text: '1 Şubat 1587', size: 40, font: 'Cormorant Garamond', italic: true, at: AT('K05@bir') }], { y: 110 }) }; }, 'A');
P('K06', 'K06', (G, st) => { const g = G.g; G.kamera(720, 600, 1.05); G.zemin(.1); isikHalka(G, 720, 600, 640, .5); g.fillStyle = G.gri(.26); g.fillRect(360, 740, 720, 30); G.mum(720, 740, 140, st.t, { r: 10 });
  G.figur({ kind: 'erkek', x: 520, y: 980, s: 560, f: 1, poz: 'otur', kol: 'yaz', t: st.t, v: .05, sakal: true }); G.figur({ kind: 'erkek', x: 920, y: 980, s: 560, f: -1, poz: 'otur', kol: 'yaz', t: st.t, v: .05 });
  return { look: { sepia: .14, strength: .4 }, ust: etiket([{ text: 'Walsingham ve Davison\'dan Paulet\'e', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'O');
P('K07', 'K07', (G, st) => { const g = G.g; G.kamera(lerp(700, 760, st.p), 560, 1.3); G.zemin(.16); isikHalka(G, 600, 380, 900, .5);
  G.mektup(720, 560, 1060, 720, -.02, { px: 36, lh: 54, yazi: ['…you have not in all this time of yourselves', '(without other provocation) found out some', 'way to shorten the life of that Queen…'], prog: 1 });
  const k = acS(st, 'K07@o', 1.6); if (k > 0) { g.save(); g.translate(720, 560); g.rotate(-.02); g.strokeStyle = G.gri(.1); g.lineWidth = 5; g.beginPath(); g.moveTo(-60, -186); g.lineTo(-60 + 300 * Math.min(1, k * 2), -186); g.moveTo(-460, -132); g.lineTo(-460 + 560 * Math.max(0, k * 2 - 1), -132); g.stroke(); g.restore(); }
  return { look: { sepia: .3, strength: .28 }, ust: kunye('Walsingham ve Davison\'dan Paulet\'e · 1 Şubat 1587') }; }, 'A');
P('K08', 'K08', (G, st) => { const g = G.g; G.kamera(720, 560, lerp(1, 1.06, st.p)); G.zemin(.08); const k = acS(st, 'K08@sessizce', 1.5);
  g.fillStyle = G.gri(.18); g.fill(G.polyP([[0, 0], [520, 260], [520, 820], [0, 1080]])); g.fill(G.polyP([[1440, 0], [920, 260], [920, 820], [1440, 1080]])); g.fillStyle = G.gri(.12); g.fillRect(520, 260, 400, 560);
  isikHalka(G, 720, 600, lerp(420, 40, k), .6); g.fillStyle = G.gri(.5); g.fillRect(700, 560, 40, 60);
  return { look: { sepia: .1, strength: .44 }, exposure: lerp(1, .7, k) }; }, 'G');
P('K09', 'K09', (G, st) => { const g = G.g; G.kamera(720, 600, 1.15); G.zemin(.1); isikHalka(G, 900, 600, 600, .5); g.fillStyle = G.gri(.26); g.fillRect(500, 740, 700, 30); G.mum(1000, 740, 140, st.t, { r: 10 });
  G.figur({ kind: 'erkek', x: 720, y: 990, s: 600, f: 1, poz: 'otur', kol: 'yaz', t: st.t, v: .05, sakal: true, sapka: false });
  return { look: { sepia: .14, strength: .4 }, ust: etiket([{ text: 'Amias Paulet · 2 Şubat 1587', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'O');
KART('K09k', AT('K09@tanrı') - .2, [Lq('“Tanrı korusun;', 'K09@tanrı', { size: 66 }), Lq('vicdanımı böyle kirletemem,', 'K09@vicdanımı', { size: 60 }), Lq('torunlarıma böyle bir leke bırakamam.', 'K09@torunlarıma', { size: 56 })], { level: 1 });
KART('K09c', AT('K09@kanun') - .2, [Lq('“Kanun ve ferman olmadan', 'K09@kanun', { size: 74 }), Lq('kan dökmem.”', 'K09@kan#1', { size: 84 }), { text: '', size: 22 }, Ls('Amias Paulet · 2 Şubat 1587', AT('K09@kanun') + 1, { size: 26 })], { level: 0 });
P('K10', 'K10', (G, st) => { G.kamera(lerp(640, 820, eio(st.p)), 560, 1); fotheringhay(G, st, { ust: .2, gece: true }); G.g.fillStyle = G.gri(0, .35); G.g.fillRect(-300, -300, 2100, 1700);
  at(G, { x: lerp(1500, 600, st.p), y: 900, s: 260, f: -1, ph: st.t * 1.7, v: .05, binici: { kind: 'erkek', v: .05, pelerin: true } });
  return { look: { sepia: .06, strength: .44 }, exposure: .9 }; }, 'G');
P('K10b', 'K10@elizabethin', fotoP('elizabeth_madalya_16yy', [.48, .44, .5], [.46, .45, .42], { kunye: 'I. Elizabeth · 16. yy madalyası · The Met (CC0)', parlak: 1.05 }), 'Y');
P('K11', 'K11', (G, st) => { const g = G.g; G.kamera(720, 600, lerp(1, 1.06, st.p)); oda(G, st, { duvar: .16, zeminY: 860 }); isikHalka(G, 560, 640, 560, .5); g.fillStyle = G.gri(.24); g.fillRect(360, 720, 420, 26); G.mum(460, 720, 120, st.t, { r: 10 });
  G.figur({ kind: 'mary', x: 620, y: 930, s: 420, f: 1, poz: 'otur', kol: 'onde', t: st.t, veil: .9, v: .06 });
  g.fillStyle = G.gri(.5); g.fillRect(1060, 260, 240, 600); const k = acS(st, 'K11@öğrendi', 1.5);
  G.figur({ kind: 'erkek', x: 1130, y: 880, s: 520, f: -1, kol: 'tut', t: st.t, v: .05, sakal: true }); G.figur({ kind: 'erkek', x: 1260, y: 885, s: 520, f: -1, kol: 'yan', t: st.t, v: .05 });
  return { look: { sepia: .16, strength: .38 }, exposure: lerp(1, .85, k), ust: etiket([{ text: 'Fotheringhay · 7 Şubat 1587, akşam', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'O');

// ════════ L · KIRMIZI ════════
bolumKarti('L');
P('L01', ILK('L'), fotoP('fotheringhay_sabah_dawe', [.5, .45, .9], [.45, .38, .6], { kunye: 'Fotheringhay\'de son sabah · G. Dawe, 1796 · The Met (CC0)' }), 'O');
P('L02', 'L02', (G, st) => { yazMasa(G, st, { cam: [720, 620, 1.15], prog: st.p, karalama: 3, manset: 'kirmizi' }); return { look: { sepia: .3, strength: .3 } }; }, 'A');
const SON_MEKTUP = ['Monsieur mon beau-frère, estant, par la permission', 'de Dieu, pour mes péchez, comme je croy, venue', 'me jetter entre les bras de ceste Royne ma cousine,', 'où j\'ay eu beaucoup d\'ennuis et passé près de vingt', 'ans, je suis enfin par elle et ses Estats condamnée', 'à la mort…'];   // Labanoff 1844, VI, harfiyen
P('L03', 'L03', (G, st) => { const g = G.g, k = acS(st, 'L04', 2); G.kamera(lerp(720, 600, k), lerp(560, 420, k), lerp(1, 1.5, k)); G.zemin(.12); G.mum(1220, 980, 330, st.t, { r: 900 });
  G.mektup(620, 520, 860, 1000, -.04, { px: 40, lh: 56, yazi: SON_MEKTUP, prog: clamp(st.lt / 6.5) });
  return { look: { sepia: .26, strength: .3 }, ust: etiket([{ text: '8 Şubat 1587, gece saat 2', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'Y');
KART('L05', 'L05', [Lq('“Tanrı\'nın izniyle, sanırım günahlarım yüzünden,', 'L05', { size: 52 }), Lq('bu kraliçenin, kuzenimin', 'L05@bu', { size: 64 }), Lq('kollarına atıldım.', 'L05@kollarına', { size: 64 }), { text: '', size: 22 }, Ls('Mary\'den III. Henri\'ye · 8 Şubat 1587', S('L05') + 1, { size: 26 })], { level: 2 });
KART('L05b', AT('L05@orada') - .2, [Lq('“Orada çok sıkıntı çektim', 'L05@orada', { size: 70 }), Lq('ve yirmi yıla yakın zaman geçirdim.”', 'L05@ve', { size: 62 })], { level: 2 });
P('L06', 'L06', (G, st) => { solway(G, st, { cam: [lerp(640, 760, st.p), 560, 1], sis: .4, ufuk: 500, isik: [1180, 470, 520, 1] });
  G.tekne({ x: 560 + st.lt * 30, y: 760, s: 420, f: 1, t: st.t, oar: st.t * .9, sail: 0, kisi: [{ kind: 'erkek', x: .3, h: .3, poz: 'otur', kol: 'kurek', f: -1 }, { kind: 'mary', x: -.2, h: .4, poz: 'otur', kol: 'onde', f: 1, kirmizi: 'etek', veil: .8 }] });
  return { iris: lerp(.62, .7, st.p), look: { sepia: .5, strength: .42 }, ust: etiket([{ text: 'Solway · 1568', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 160 }) }; }, 'G');
P('L07', 'L07', fotoP('idam_iln_1861', [.3, .48, .42], [.31, .49, .36], { kunye: 'Fotheringhay\'in büyük salonu · ILN, 1861 (J. Gilbert) · The Met (CC0)', etiket: [{ text: '8 Şubat 1587, sabah', size: 40, font: 'Cormorant Garamond', italic: true, at: S('L07') + .4 }] }), 'O');
P('L07b', 'L07@elinde', fotoP('mary_siyah_hacli_tamboy', [.45, .48, .42], [.52, .6, .34], {
  klip: [.232, .242, .765, .762], ort: ORT_IDAM, kontrast: 1.45, parlak: .93, renkTon: 'brightness(2.6) contrast(.95)', u: st => ss((st.t - AT('L08') + 1) / 4),
  kirmizi: { poly: SIYAH_ETEK, cikar: SIYAH_CIKAR, yum: 12, sil: st => ss((st.t - AT('L08@kızıl')) / 2.2) }, kunye: 'E. F. Finden, 19. yy gravürü · The Met (CC0)', look: { sepia: .14, strength: .36 } }), 'Y');
// idam salonu (çizim): siyah örtülü kürsü, parmaklık, seyirciler, şömine; balta ve kütük gösterilmez
function idamSalonu(G, st, o = {}) { const g = G.g; G.kamera(...(o.cam || [720, 560, 1])); G.zemin(.26);
  g.fillStyle = G.gri(.7); g.beginPath(); g.moveTo(1080, 120); g.lineTo(1260, 120); g.lineTo(1260, 520); g.lineTo(1080, 520); g.fill(); g.save(); g.globalAlpha = .2; g.fillStyle = G.gri(1); g.beginPath(); g.moveTo(1080, 200); g.lineTo(1260, 160); g.lineTo(900, 900); g.lineTo(560, 900); g.closePath(); g.fill(); g.restore();
  g.fillStyle = G.gri(.15); g.fillRect(120, 380, 260, 380); g.fillStyle = G.gri(.06); g.fillRect(160, 470, 180, 290); for (let i = 0; i < 6; i++) { g.fillStyle = G.gri(.4 + .1 * Math.sin(st.t * 8 + i)); g.beginPath(); g.ellipse(200 + i * 22, 740 - Math.abs(Math.sin(st.t * 5 + i)) * 30, 12, 34, 0, 0, TAU); g.fill(); }   // şömine
  g.fillStyle = G.gri(.4); g.fillRect(-300, 820, 2100, 400);
  g.fillStyle = G.gri(.08); g.fill(G.polyP([[440, 820], [1000, 820], [1060, 740], [380, 740]])); g.fillRect(380, 700, 680, 50);   // siyah örtülü kürsü
  g.fillStyle = G.gri(.12); for (let i = 0; i < 12; i++) g.fillRect(360 + i * 64, 640, 10, 70); g.fillRect(350, 636, 730, 12);   // parmaklık
  ordu(G, st, { x0: -100, x1: 330, y: 960, s: 300, n: 6, v: .1, mizrak: .5, seed: 3 }); ordu(G, st, { x0: 1110, x1: 1540, y: 960, s: 300, n: 6, v: .1, mizrak: .5, seed: 4 }); }
P('L09', 'L09', (G, st) => { idamSalonu(G, st, { cam: [720, 600, lerp(1, 1.05, st.p)] });
  G.figur({ kind: 'mary', x: 720, y: 720, s: 280, f: 1, kol: 'onde', t: st.t, veil: .9, v: .1, kirmizi: 'etek' });
  G.figur({ kind: 'kadin', x: 560, y: 724, s: 160, f: 1, poz: 'diz', kol: 'egik', t: st.t, v: .14 }); G.figur({ kind: 'kadin', x: 880, y: 724, s: 160, f: -1, poz: 'diz', kol: 'egik', t: st.t, v: .14 });
  return { look: { sepia: .12, strength: .4 } }; }, 'G');
KART('L09k', AT('L09@ağlamayın') - .2, [Lq('“Ağlamayın,', 'L09@ağlamayın', { size: 84 }), Lq('sizin için dua ettim.”', 'L09@sizin', { size: 74 })], { level: 2 });
P('L10', 'L10', (G, st) => { const g = G.g; G.kamera(720, 600, lerp(1.6, 1.7, st.p)); idamSalonu(G, st, { cam: [720, 620, lerp(1.6, 1.7, st.p)] });
  G.figur({ kind: 'mary', x: 680, y: 742, s: 300, f: 1, poz: 'diz', kol: 'dua', t: st.t, veil: .9, v: .1, kirmizi: 'etek' });
  return { look: { sepia: .12, strength: .4 } }; }, 'O');
KART('L10k', AT('L10@son') - .2, [Lq('In manus tuas, Domine,', 'L10@son', { size: 66 }), Lq('commendo spiritum meum.', 'L10@son', { size: 66 }), { text: '', size: 22 }, { text: 'Rabbim, ruhumu senin ellerine bırakıyorum.', size: 46, font: 'Cormorant Garamond', italic: true, weight: 500, at: AT('L10@ruhumu') }], { level: 2 });
P('L11', 'L11', (G, st) => { idamSalonu(G, st, { cam: [720, 560, lerp(1.1, 1, eio(st.p))] }); return { look: { sepia: .1, strength: .42 }, karart: clamp((st.t - S('L11') - .6) / 2.4) }; }, 'G');
// L12: kızıl kadife (kıvrımlar)
function kadife(G, st, o = {}) { const g = G.g; G.kamera(...(o.cam || [720, 540, 1])); G.zemin(.2); const n = 9;
  for (let i = 0; i < n; i++) { const x0 = -100 + i * 190 + Math.sin(st.t * .4 + i) * 10, gr = g.createLinearGradient(x0, 0, x0 + 190, 0); gr.addColorStop(0, G.gri(.18)); gr.addColorStop(.45, G.gri(.62)); gr.addColorStop(1, G.gri(.16)); g.fillStyle = gr;
    const P0 = G.pathOf([[x0, -100], [x0 + 190, -100], [x0 + 200 + Math.sin(i) * 20, 600], [x0 + 190, 1200], [x0, 1200], [x0 + 10 + Math.cos(i) * 20, 600]], true, .5); g.fill(P0); }
  G.kirmiziCiz(r => { r.globalAlpha = o.a ?? 1; r.fillRect(-500, -500, 2500, 2100); }); }
P('L12', 'L12', (G, st) => { kadife(G, st, { cam: [720, 540, lerp(1, 1.1, st.p)], a: acS(st, 'L12', 1.2) }); return { look: { sepia: .14, strength: .3 }, renkTon: 'contrast(.6) brightness(1.5)' }; }, 'A');
P('L13', 'L13', fotoP('mary_siyah_hacli_tamboy', [.52, .58, .34], [.52, .6, .3], { klip: [.232, .242, .765, .762], ort: ORT_IDAM, kontrast: 1.45, parlak: .93, renkTon: 'brightness(2.6) contrast(.95)', kirmizi: { poly: SIYAH_ETEK, cikar: SIYAH_CIKAR, yum: 12 }, kunye: 'E. F. Finden, 19. yy gravürü · The Met (CC0)', look: { sepia: .14 } }), 'Y');
P('L14', 'L14', (G, st) => { const g = G.g; G.kamera(lerp(700, 760, st.p), 560, 1.35); G.zemin(.14); isikHalka(G, 600, 380, 900, .5);
  G.mektup(720, 560, 1060, 640, -.02, { px: 38, lh: 56, yazi: ['…La religion catholique et le maintien', 'du droit que Dieu m\'a donné à ceste couronne', 'sont les deux points de ma condemnation…'], prog: 1 });
  const k = acS(st, 'L14@inancı', 2); if (k > 0) { g.save(); g.translate(720, 560); g.rotate(-.02); g.strokeStyle = G.gri(.1); g.lineWidth = 5; g.beginPath(); g.moveTo(-460, -200); g.lineTo(-460 + 620 * Math.min(1, k * 2), -200); g.moveTo(-460, -144); g.lineTo(-460 + 760 * Math.max(0, k * 2 - 1), -144); g.stroke(); g.restore(); }
  return { look: { sepia: .3, strength: .28 }, ust: kunye('Mary\'den III. Henri\'ye · 8 Şubat 1587') }; }, 'A');
P('L15', 'L15', (G, st) => { idamSalonu(G, st, { cam: [700, 600, lerp(2, 2.15, st.p)] }); G.figur({ kind: 'mary', x: 680, y: 742, s: 300, f: 1, poz: 'diz', kol: 'dua', t: st.t, veil: .9, v: .1, kirmizi: 'etek' });
  return { look: { sepia: .12, strength: .38 }, exposure: 1.08 }; }, 'O');
// L16: tül süzülerek düşer
P('L16', 'L16', (G, st) => { const g = G.g; G.kamera(720, 560, 1); G.zemin(.16); isikHalka(G, 720, 300, 900, .5); g.fillStyle = G.gri(.36); g.fillRect(-300, 900, 2100, 400);
  const k = clamp(st.lt / 6), y = lerp(-200, 860, k), sw = Math.sin(st.lt * 1.6) * 120 * (1 - k);
  g.fillStyle = G.gri(.92, .7); g.fill(G.pathOf([[620 + sw, y - 90], [820 + sw, y - 70 + Math.sin(st.t * 3) * 20], [900 + sw, y + 30 * (1 - k)], [780 + sw, y + 60], [600 + sw, y + 40 * (1 - k)], [560 + sw, y - 20]], true, .7));
  return { look: { sepia: .14, strength: .36 } }; }, 'A');
P('L16b', 'L16@kırk', fotoP('mary_dul_18yy', [.5, .34, .5], [.5, .33, .4], { kunye: '18. yy (?) gravürü · The Met (CC0)' }), 'Y');
KART('L17', 'L17', [Lq('“Kraliçe\'nin bütün düşmanları', AT('L17@kraliçenin'), { size: 70 }), Lq('böyle yok olsun.”', AT('L17@böyle'), { size: 78 }), { text: '', size: 22 }, Ls('Peterborough Dekanı · 8 Şubat 1587', S('L17') + .6, { size: 26 })], { level: 0 });
// L18: köpek kızıl kumaşın altından çıkar, yanında oturur
function kopek(G, x, y, s, f = 1) { const g = G.g; g.save(); g.translate(x, y); g.scale(s * f, s); g.fillStyle = G.gri(.12);
  g.fill(G.pathOf([[-.5, -.05], [-.45, -.4], [-.2, -.48], [.2, -.46], [.38, -.6], [.5, -.78], [.6, -.8], [.72, -.72], [.78, -.62], [.7, -.55], [.55, -.5], [.48, -.3], [.42, 0], [.32, 0], [.3, -.2], [-.2, -.2], [-.25, 0], [-.35, 0], [-.4, -.2], [-.55, -.3], [-.7, -.42], [-.62, -.3]], true, .5));
  g.fill(G.pathOf([[.5, -.78], [.46, -.95], [.56, -.82]], true, .3)); g.fill(G.pathOf([[.62, -.8], [.64, -.97], [.7, -.8]], true, .3)); g.restore(); }
P('L18', 'L18', (G, st) => { kadife(G, st, { cam: [720, 640, 1.1], a: 1 }); const g = G.g; g.fillStyle = G.gri(.4); g.fillRect(-300, 880, 2100, 400); const k = acS(st, 'L18@çıktı', 1.5);
  kopek(G, lerp(560, 860, k), 900, 260, 1); return { look: { sepia: .14, strength: .32 }, renkTon: 'contrast(.6) brightness(1.5)' }; }, 'A');
P('L19', 'L19', fotoP('elizabeth_depasse_1592', [.5, .3, .4], [.5, .3, .34], { kunye: 'I. Elizabeth · Crispijn de Passe, 1592 · The Met (CC0)',
  ciz: (G, st, W, H) => { const k = acS(st, 'L19@değişti', 2.4); if (k <= 0) return; G.g.fillStyle = G.gri(0, .45 * k); G.g.fillRect(0, 0, W, H); } }), 'Y');
P('L19b', 'L19@yas', (G, st) => { galeri(G, st, { cam: [720, 600, 1.1] }); G.g.fillStyle = G.gri(0, .35); G.g.fillRect(-300, -300, 2100, 1700);
  G.figur({ kind: 'eliz', x: 520, y: 960, s: 520, f: 1, kol: ac(st, 'L19@meclisini') > 0 ? 'isaret' : 'yanak', t: st.t, v: .04 });
  for (let i = 0; i < 4; i++) G.figur({ kind: 'erkek', x: 860 + i * 140, y: 960, s: 460, f: -1, kol: 'egik', t: st.t, v: .06, lean: .25, sakal: i % 2 === 0 });
  return { look: { sepia: .12, strength: .4 } }; }, 'O');
P('L20', 'L20', (G, st) => { const g = G.g, ufuk = 620; G.kamera(720, 560, lerp(1, 1.05, st.p)); G.gok(ufuk, { ust: .42, alt: .78 }); G.bulutlar(140, 520, { seed: 53, drift: st.t * 4 });
  kale(G, 300, ufuk + 4, 820, [{ t: 'sur', x: .5, w: 1.1, h: .16 }, { x: .5, w: .34, h: .44, cati: 'mazgal', pen: 3 }, { x: .33, w: .06, h: .56, cati: 'konik', ch: .08 }, { x: .67, w: .06, h: .56, cati: 'konik', ch: .08 }, { x: .05, w: .1, h: .26 }, { x: .95, w: .1, h: .26 }], { v: .18 });
  G.deniz(ufuk + 4, 1080, { t: st.t, ufuk: .7, on: .4, n: 50 });
  return { look: { sepia: .16, strength: .36 }, ust: etiket([{ text: 'Londra Kulesi · Davison', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('L20b', 'L20@merinin', (G, st) => { const g = G.g; G.kamera(lerp(700, 760, st.p), 560, 1.3); G.zemin(.14); isikHalka(G, 600, 380, 900, .5);
  G.mektup(720, 560, 1060, 640, .02, { px: 36, lh: 54, yazi: ['…for that miserable accident, which,', 'far contrary to my meaning,', 'hath befallen.'], prog: 1 });
  const k = acS(st, 'L20@niyetimin', 1.4); if (k > 0) { g.save(); g.translate(720, 560); g.rotate(.02); g.strokeStyle = G.gri(.1); g.lineWidth = 5; g.beginPath(); g.moveTo(-460, -146); g.lineTo(-460 + 470 * k, -146); g.stroke(); g.restore(); }
  return { look: { sepia: .3, strength: .28 }, ust: kunye('Elizabeth\'ten VI. James\'e · 14 Şubat 1587') }; }, 'A');
KART('L21', 'L21', [Lq('Niyetimin', 'L21', { size: 96 }), Lq('tam tersine.', 'L21@tam', { size: 96 })], { level: 0 });

// ════════ M · SONUMDA BAŞLANGICIM ════════
bolumKarti('M');
P('M01', ILK('M'), (G, st) => { const g = G.g; salon(G, st, { cam: [720, 600, lerp(1.1, 1, eio(st.p))], duvar: .3, zeminV: .5, pencere: 4 });
  g.fillStyle = G.gri(.14); g.fillRect(560, 700, 320, 80); g.fillRect(600, 400, 240, 300); g.fillStyle = G.gri(.2); g.fill(G.pathOf([[580, 400], [860, 400], [840, 330], [720, 290], [600, 330]], true, .5));
  G.figur({ kind: 'eliz', x: 720, y: 780, s: 380, f: 1, poz: 'otur', kol: 'onde', t: st.t, v: .06 });
  return { look: { sepia: .26, strength: .3 } }; }, 'G');
P('M02', 'M02', fotoP('elizabeth_depasse_1592', [.5, .34, .5], [.5, .48, .92], { kunye: 'I. Elizabeth · Crispijn de Passe, 1592 · The Met (CC0)' }), 'O');
P('M03', 'M03', (G, st) => { const g = G.g, im = IMG.elizabeth_madalya_16yy, k = acS(st, 'M03@öldü', 1.2); G.kamera(720, 560, 1.05); G.zemin(.1); isikHalka(G, 900, 500, lerp(800, 200, k), .55);
  if (im) { const c = BOYA.griOn(im, 1.1, 1.05); g.drawImage(c, 300, 140, 560, 560 * im.naturalHeight / im.naturalWidth); }
  if (k < 1) G.mum(1080, 900, 240, st.t, { r: 10 }); else G.dik(1062, 660, 36, 240, .6);
  return { look: { sepia: .2, strength: .34 }, exposure: lerp(1, .8, k), ust: ust2(kunye('I. Elizabeth · 16. yy madalyası · The Met (CC0)'), etiket([{ text: '24 Mart 1603', size: 40, font: 'Cormorant Garamond', italic: true, at: st.at + .2 }], { y: 110 })) }; }, 'A');
P('M04', 'M04', fotoP('james_dejode_1603', [.5, .45, .55], [.5, .42, .4], { kunye: 'VI. James, 1603\'te I. James · P. de Jode · The Met (CC0)' }), 'Y');
P('M05', 'M05', (G, st) => { G.kamera(720, 540, lerp(1.1, 1, st.p)); G.zemin(.2); isikHalka(G, 720, 420, 700, .35); arma(G, 720, 580, 520, 640, { ing: 1, ingKirmizi: 1, tac: 1 }); return { look: { sepia: .24, strength: .3 } }; }, 'O');
P('M05b', 'M05@ama', fotoP('james_unite_sikke_1613', [.5, .5, .62], [.5, .5, .5], { kunye: '"Unite" sikkesi, I. James, 1613 · The Met (CC0)', parlak: .95, zemin: .15 }), 'Y');
// M06: soy çizgisi: Tudor dalı Elizabeth'te biter; Stuart dalı bugüne iner (çizgi adların arasında kesilir, adların üstünden geçmez)
P('M06', 'M06', (G, st) => { const g = G.g; G.kamera(720, lerp(500, 640, eio(st.p)), 1); G.zemin(.88); const k = acS(st, 'M06@bugün', 4), t2 = acS(st, 'M06@tudor', 1.5);
  g.fillStyle = G.gri(.2); g.textAlign = 'center'; g.font = '600 38px "Cinzel"';
  g.fillText('TUDOR', 400, 170); g.fillText('MARY\'NİN SOYU', 1040, 170);
  g.strokeStyle = G.gri(.2); g.lineWidth = 6; g.beginPath(); g.moveTo(400, 200); g.lineTo(400, 520); g.stroke(); g.font = 'italic 600 40px "Cormorant Garamond"'; g.fillText('I. Elizabeth', 400, 570);
  if (t2 > 0) { g.lineWidth = 8; g.beginPath(); g.moveTo(340, 620); g.lineTo(460, 620); g.stroke(); g.fillText('1603', 400, 670); }
  const son = 200 + 900 * k; g.lineWidth = 6; g.beginPath(); for (const [a, b] of [[270, 382], [442, 612], [656, 1022]]) if (son > a) { g.moveTo(1040, a); g.lineTo(1040, Math.min(b, son)); } g.stroke(); g.fillText('Mary Stuart', 1040, 250); if (k > .25) g.fillText('VI. ve I. James', 1040, 420); if (k > .55) g.fillText('…', 1040, 640); if (k > .85) g.fillText('bugünkü kraliyet ailesi', 1040, 1060);
  G.kirmiziCiz(r => { r.beginPath(); r.arc(1040, 200, 14, 0, TAU); r.fill(); });
  return { look: { sepia: .3, strength: .26 } }; }, 'A');
P('M07', 'M07', (G, st) => { isleme(G, st, { cam: [720, 760, lerp(1.6, 1.45, st.p)], yazi: 'En ma fin est mon commencement', yaziP: 1 }); return { look: { sepia: .32, strength: .26 } }; }, 'Y');
P('M08', 'M08', fotoP('westminster_mezar_heykeli', [.55, .45, .7], [.55, .4, .5], { kunye: 'Mary\'nin mezar heykeli, Westminster · T. W. Knight, 1859 · The Met (CC0)' }), 'O');
// M09–M10: VII. Henry Şapeli: iki yan nef, iki mezar, arada koridor
function sapel(G, st, o = {}) { const g = G.g; G.kamera(...(o.cam || [720, 560, 1])); G.zemin(.3);
  for (let i = 0; i < 7; i++) { const x = 100 + i * 210; g.fillStyle = G.gri(.18); g.fillRect(x - 18, 80, 36, 800); g.strokeStyle = G.gri(.2); g.lineWidth = 14; g.beginPath(); g.moveTo(x, 300); g.quadraticCurveTo(x + 105, 120, x + 210, 300); g.stroke(); }
  const fl = g.createLinearGradient(0, 760, 0, 1080); fl.addColorStop(0, G.gri(.55)); fl.addColorStop(1, G.gri(.3)); g.fillStyle = fl; g.fillRect(-400, 760, 2300, 500);
  g.fillStyle = G.gri(.7, .5); g.fill(G.polyP([[640, 760], [800, 760], [1000, 1080], [440, 1080]]));    // koridor
  for (const [x, ad] of [[300, o.sol || 'I. ELİZABETH'], [1140, o.sag || 'MARY STUART']]) { g.fillStyle = G.gri(.22); g.fillRect(x - 170, 560, 340, 200); g.fillStyle = G.gri(.82); g.fillRect(x - 150, 520, 300, 50);
    for (const dx of [-160, 160]) { g.fillStyle = G.gri(.16); g.fillRect(x + dx - 12, 260, 24, 300); } g.fillStyle = G.gri(.2); g.fill(G.pathOf([[x - 190, 260], [x + 190, 260], [x + 150, 200], [x, 160], [x - 150, 200]], true, .4));
    g.fillStyle = G.gri(.15); g.font = '600 26px "Cinzel"'; g.textAlign = 'center'; g.fillText(ad, x, 820); } }
P('M09', 'M09', (G, st) => { sapel(G, st, { cam: [lerp(400, 1040, eio(st.p)), 560, 1.2] }); return { look: { sepia: .28, strength: .3 }, ust: etiket([{ text: 'Westminster Abbey · VII. Henry Şapeli', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'G');
P('M09b', 'M09@hayattayken', (G, st) => { sapel(G, st, { cam: [720, 760, lerp(1.5, 1.4, st.p)] }); return { look: { sepia: .28, strength: .3 } }; }, 'O');
P('M10', 'M10', (G, st) => { const k = acS(st, 'M10@romantik', 1.6); sapel(G, st, { cam: [lerp(400, 1040, k), 560, 1.15] });
  return { look: { sepia: .28, strength: .3 }, ust: etiket([{ text: 'Gerçekçi Elizabeth tarihte kazanır;', size: 44, font: 'Cormorant Garamond', italic: true, weight: 600, at: AT('M10@gerçekçi') }, { text: 'romantik Mary ise şiirde ve efsanede.', size: 44, font: 'Cormorant Garamond', italic: true, weight: 600, at: AT('M10@romantik') }, { text: 'Stefan Zweig', size: 26, at: AT('M10@gerçekçi') + 1 }], { y: 700 }) }; }, 'G');
KART('M11', 'M11', [Lq('Şimdi soru senin:', 'M11', { size: 56 }), { text: 'KALBİNLE Mİ, AKLINLA MI?', size: 76, font: 'Cinzel', weight: 700, spacing: 4, at: AT('M11@kalbinle') }, { text: '', size: 18 }, Lq('Sence hangisi kazandı?', 'M11@sence', { size: 56 }), Ls('Cevabını yorumlara yaz.', 'M11@cevabını', { size: 30 })], { level: 2 });
P('M12', 'M12', (G, st) => { solway(G, st, { cam: [720, 560, 1], sis: .3, ufuk: 520, isik: [720, 500, 620, 1], gokUst: .4 });
  G.tekne({ x: 300 + st.lt * 30, y: 680, s: 220, f: 1, t: st.t, sail: .8, kisi: [{ kind: 'mary', x: -.2, h: .45, poz: 'otur', kirmizi: 'etek', veil: .8 }] });
  return { look: { sepia: .3, strength: .32 }, ust: etiket([{ text: 'ZAMAN KURYESİ', size: 56, weight: 700, spacing: 10, at: S('M12') + .3 }], { y: 160 }), iris: lerp(1, .8, st.p) }; }, 'G');
// M13 + bitiş ekranı (son 20 sn): sakin kart; ortası YouTube bitiş ögelerine boş
P('M13', 'M13', () => ({ kart: { level: 2, lines: [{ text: 'ZAMAN KURYESİ', size: 40, font: 'Cinzel', weight: 700, spacing: 10 }, { text: '', size: 380 }, Lq('Aynı yüzyılda tahtını bırakan bir imparator…', AT('M13@aynı') + .5, { size: 40, weight: 500 })] }, look: { sepia: .2, strength: .26 } }), 'K');
