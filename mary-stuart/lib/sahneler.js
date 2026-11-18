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
  KART('K' + h, t0, [Ls(BOLUM[h][0], null, { size: 34, spacing: 10 }), { text: BOLUM[h][1].toLocaleUpperCase('tr'), size: 78, font: 'Cinzel', weight: 700, spacing: 6 }, { text: '', size: 30 }, Lq(SORU[h], t0 + .7, { size: 50, weight: 500 })], { level: 2 });
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
const SIYAH_ETEK = [[.42, .515], [.5, .545], [.575, .515], [.565, .57], [.56, .635], [.625, .645], [.645, .69], [.66, .755], [.5, .762], [.37, .755], [.385, .69], [.395, .62], [.405, .56]];
P('A01', 0, fotoP('mary_siyah_hacli_tamboy', [.545, .41, .36], [.535, .6, .4], {
  klip: [.232, .242, .765, .762], kontrast: 1.2, renkTon: 'contrast(.42) brightness(2)', u: st => ss((st.t - 1.3) / 4.2),
  kirmizi: { poly: SIYAH_ETEK, sil: st => ss((st.t - AT('A01@altından')) / 1.8) }, karart: st => 1 - clamp(st.t / .9),
  kunye: 'E. F. Finden, 19. yy gravürü · The Met (CC0)', look: { sepia: .16, strength: .34 } }), 'O');
P('A02', 'A02', fotoP('mary_dul_18yy', [.5, .4, .72], [.5, .34, .46], {
  etiket: [{ text: 'MARY STUART', size: 70, weight: 700, spacing: 8, at: S('A02') + .2 }, { text: 'İskoçya Kraliçesi  ·  8 Şubat 1587', size: 40, font: 'Cormorant Garamond', italic: true, weight: 600, at: AT('A02@şubat') - .3 }],
  kunye: '18. yy gravürü · The Met (CC0)' }), 'Y');
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
KART('A06', 'A06', [Ls('Stefan Zweig · Maria Stuart (1935)', S('A06'), { size: 28 }), { text: '', size: 24 }, Lq('Biri kalbiyle yaşar,', 'A06@kalbiyle', { size: 76 }), Lq('öteki aklıyla.', 'A06@aklıyla', { size: 76 }), { text: '', size: 24 }, { text: 'SEN HANGİSİSİN?', size: 46, font: 'Cinzel', weight: 700, spacing: 6, at: AT('A06@sen') }]);
// A07 + B01 + B03: beşik (Linlithgow, Aralık 1542); kış penceresi, mum
function besikOda(G, st, o = {}) {
  const cam = o.cam || [720, 560, 1]; G.kamera(...cam);
  oda(G, st, { duvar: .17, zeminY: 800, pencere: [1060, 170, 300, 470], derin: 90, dis: () => { G.gok(640, { ust: .62, alt: .86 }); G.kiyi(900, 1500, 640, 120, { v: .78, seed: 5 }); kar(G, st, 900, 160, 320, 500, 50); } });
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
P('B02', 'B02', (G, st) => { bataklik(G, st, { cam: [lerp(760, 680, eio(st.p)), 560, 1.05] }); return { look: { sepia: .1, strength: .45 }, ust: etiket([{ text: 'Solway Moss · Kasım 1542', size: 34, font: 'Cormorant Garamond', italic: true, at: S('B02') + .4 }], { y: 120 }) }; }, 'G');
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
  yazilar: [['İSKOÇYA', -4.3, 56.6, 34], ['FRANSA', 0.2, 48.3, 34], ['1548', -6.9, 52.2, 30, acS(st, 'B04@fransaya', 1)]] }); return { look: { sepia: .3, strength: .26 } }; }, 'A');
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
P('B09', 'B09', fotoP('mary_clouet_beyazyas_resim', [.5, .42, .95], [.53, .33, .6], { kunye: 'Beyaz yas içinde Mary, 1560 (Clouet\'den sonra) · kamu malı', kontrast: 1.05 }), 'Y');
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
