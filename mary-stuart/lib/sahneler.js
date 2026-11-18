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
KART('C02k', AT('C02@gökyüzü') - .2, [Lq('“Gökyüzü bile, bu ülkeye', 'C02@gökyüzü', { size: 62 }), Lq('ne getirildiğini söylüyordu:', 'C02@ne', { size: 62 }), Lq('keder, acı ve karanlık.”', 'C02@keder', { size: 72 }), { text: '', size: 22 }, Ls('John Knox · Reformasyon Tarihi', AT('C02@gökyüzü') + 1, { size: 26 })]);
// C03: sisin içinde atlılar
P('C03', 'C03', (G, st) => {
  const g = G.g; G.kamera(720, 560, 1); G.zemin(.82);
  for (let i = 0; i < 5; i++) { const x = 300 + i * 230 + st.lt * 30, y = 820 + (i % 2) * 20; at(G, { x, y, s: 300 - i * 10, f: 1, ph: st.t * 1.2 + i * .23, dur: true, v: lerp(.25, .6, i / 5), binici: { kind: i === 2 ? 'mary' : 'erkek', veil: .9, v: lerp(.25, .6, i / 5) } }); }
  sis(G, st, 500, 1000, .75, { n: 14, v: .84 }); sis(G, st, 200, 700, .5, { n: 8, v: .86, seed: 9 });
  return { look: { sepia: .1, strength: .32 } };
}, 'G');
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
P('C05', 'C05', fotoP('mary_reg_scotorum_17yy', [.5, .45, .9], [.5, .38, .62], { kunye: 'Maria Reg. Scotorum · 17. yy gravürü · The Met (CC0)' }), 'Y');
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
P('D07', 'D07', fotoP('elizabeth_huys', [.53, .32, .7], [.53, .28, .48], { kunye: 'I. Elizabeth · Frans Huys · The Met (CC0)' }), 'Y');
P('D08', 'D08', (G, st) => { galeri(G, st, { cam: [800, 600, 1.35] });
  G.figur({ kind: 'eliz', x: 1010, y: 900, s: 520, f: -1, kol: 'onde', t: st.t, v: .1 });
  G.figur({ kind: 'erkek', x: 640, y: 910, s: 560, f: 1, kol: ac(st, 'D08@uzun') > 0 ? 'kaldir' : 'tut', t: st.t, sakal: true, v: .08 });
  return { look: { sepia: .3, strength: .28 } }; }, 'O');
KART('D09', 'D09', [Lq('“O hâlde fazla uzun.', 'D09@halde', { size: 78 }), Lq('Çünkü ben ne fazla uzunum,', 'D09@çünkü'), Lq('ne fazla kısa.”', AT('D09@kısa') - .5), { text: '', size: 22 }, Ls('Elizabeth · Melville\'in anılarından, 1564', S('D09') + 1, { size: 26 })], { level: 2 });
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
P('D15', 'D15', fotoP('mary_darnley_dunkarton', [.47, .5, .9], [.47, .42, .7], { kunye: 'Mary ve Darnley · R. Dunkarton, 1816 · The Met (CC0)' }), 'O');
P('D16', 'D16', (G, st) => {
  const g = G.g; kilise(G, st, { cam: [720, 560, lerp(1, 1.05, st.p)] });
  g.fillStyle = G.gri(.7); g.fillRect(560, 620, 320, 26); for (const x of [600, 840]) G.mum(x, 620, 140, st.t + x, { r: 380 });
  G.figur({ kind: 'mary', x: 680, y: 900, s: 300, f: 1, kol: 'onde', t: st.t, veil: .9, v: .12 }); G.figur({ kind: 'erkek', x: 760, y: 905, s: 330, f: -1, kol: 'onde', t: st.t, v: .1 });
  return { look: { sepia: .3, strength: .28 }, ust: etiket([{ text: 'Holyrood · 29 Temmuz 1565', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) };
}, 'G');

// ════════ E · HOLYROOD'DAKİ GECE ════════
bolumKarti('E');
P('E01', ILK('E'), fotoP('mary_darnley_dunkarton', [.32, .34, .5], [.32, .3, .36], { kunye: 'Lord Darnley · R. Dunkarton, 1816 · The Met (CC0)' }), 'Y');
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
P('E08', 'E08', (G, st) => { besikOda(G, st, { cam: [720, 700, lerp(1.4, 1.5, st.p)], bebek: true, salla: .03 }); return { look: { sepia: .3, strength: .28 }, ust: etiket([{ text: 'Edinburgh · 19 Haziran 1566', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'Y');
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
P('E12', 'E12', fotoP('elizabeth_huys', [.52, .4, .95], [.52, .36, .8], { kunye: 'I. Elizabeth · Frans Huys · The Met (CC0)',
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
  const g = G.g, ufuk = 640; G.kamera(lerp(760, 680, eio(st.p)), 600, 1.1); G.gok(ufuk, { ust: .62, alt: .86 }); G.bulutlar(120, 520, { seed: 25, drift: st.t * 3 });
  kale(G, 900, ufuk, 500, [{ t: 'sur', x: .5, w: 1.4, h: .16 }], { v: .3 }); g.fillStyle = G.gri(.55); g.fillRect(-300, ufuk, 2100, 600);
  g.strokeStyle = G.gri(.14); g.lineCap = 'round'; const dal = (x, y, a, L, w, d) => { if (d > 6) return; const x2 = x + Math.sin(a) * L, y2 = y - Math.cos(a) * L; g.lineWidth = w; g.beginPath(); g.moveTo(x, y); g.lineTo(x2, y2); g.stroke(); dal(x2, y2, a - .45, L * .72, w * .66, d + 1); dal(x2, y2, a + .35, L * .7, w * .66, d + 1); };
  dal(380, 900, .05, 220, 30, 0);
  g.fillStyle = G.gri(.18); g.save(); g.translate(820, 880); g.rotate(.4); g.fillRect(-60, -10, 120, 16); g.fillRect(-60, -110, 14, 120); g.fillRect(46, -10, 12, 70); g.fillRect(-56, -10, 12, 70); g.restore();     // devrik sandalye
  g.fillStyle = G.gri(.3); g.fill(G.pathOf([[560, 930], [700, 900], [780, 930], [720, 960], [600, 965]], true, .6));    // pelerin
  sis(G, st, 600, 950, .35, { n: 6, v: .8 });
  return { look: { sepia: .14, strength: .36 }, ust: etiket([{ text: 'Kirk o\'Field · 10 Şubat 1567', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) };
}, 'G');
// F04: parmaklar tek adamı gösterir (duvarda gölgeler); ortada Bothwell
P('F04', 'F04', (G, st) => {
  const g = G.g; G.kamera(720, 600, lerp(1, 1.1, eio(st.p))); G.gok(720, { ust: .55, alt: .85 }); kale(G, -100, 720, 1700, [{ t: 'ev', x: .2, w: .3, h: .3, cati: 'beşik', pen: 4 }, { t: 'ev', x: .55, w: .3, h: .36, cati: 'beşik', pen: 5 }, { t: 'ev', x: .85, w: .2, h: .28, cati: 'beşik', pen: 3 }], { v: .45 });
  g.fillStyle = G.gri(.5); g.fillRect(-300, 720, 2100, 500);
  const k = acS(st, 'F04@gösterdi', 1.2), b = acS(st, 'F04@botvel', 1.2);
  G.figur({ kind: 'erkek', x: 760, y: 860, s: 380, f: 1, kol: 'yan', t: st.t, v: lerp(.42, .06, b), sakal: true, pelerin: true });
  for (const [x, y, sc, f] of [[160, 1040, 1, 1], [380, 1080, 1.1, 1], [1180, 1050, 1, -1], [1380, 1090, 1.15, -1], [560, 1120, 1.2, 1], [980, 1120, 1.2, -1]]) G.figur({ kind: f > 0 && x < 300 ? 'kadin' : 'erkek', x, y, s: 520 * sc, f, kol: k > 0 ? 'isaret' : 'yan', t: st.t, v: .05 });
  return { look: { sepia: .16, strength: .38 }, ust: etiket([{ text: 'Edinburgh · Şubat 1567', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) };
}, 'Y');
P('F05', 'F05', (G, st) => { yazMasa(G, st, { cam: [720, 600, 1.05], prog: st.p * 1.2, yazi: ['Madame, mes oreilles ont été si', 'étourdies et mon cœur si effrayé…'], manset: 'dantel' }); return { look: { sepia: .3, strength: .28 } }; }, 'A');
KART('F06', 'F06', [Lq('“Duyduklarım kulaklarımı öyle sersemletti,', 'F06', { size: 56 }), Lq('yüreğimi öyle korkuttu ki,', 'F06@yüreğimi', { size: 56 }), Lq('yazacak gücüm zor yetiyor.', 'F06@yazacak', { size: 56 }), { text: '', size: 22 }, Ls('Elizabeth\'ten Mary\'ye · 24 Şubat 1567', S('F06') + 1, { size: 26 })], { level: 2 });
KART('F06b', AT('F06@sizin') - .2, [Lq('“Sizin için,', 'F06@sizin', { size: 80 }), Lq('ondan daha çok üzülüyorum.”', 'F06@ondan', { size: 72 })], { level: 2 });
P('F07', 'F07', fotoP('elizabeth_huys', [.53, .3, .4], [.53, .28, .3], { kunye: 'I. Elizabeth · Frans Huys · The Met (CC0)' }), 'Y');
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
  const g = G.g; g.globalAlpha = 1 - kay * .92; G.mektup(560, 560, 640, 760, -.08, { px: 34, lh: 50, yazi: ['Mon cœur, hélas, faut-il que la folie', 'd\'une femme, dont vous connaissez assez', 'l\'ingratitude vers moi…'], prog: 1 }); g.globalAlpha = 1;
  if (kop > 0) G.mektup(lerp(1300, 900, kop), 600, 600, 720, .05, { px: 30, lh: 46, yazi: ['Copie', 'My heart, alas, must the folly of a', 'woman whose unkindness to me…'], prog: 1, v: .86 });
  return { look: { sepia: .3, strength: .28 } }; }, 'Y');
P('F17', 'F17', (G, st) => { G.kamera(720, 560, 1.05); G.zemin(.18); isikHalka(G, 720, 380, 800, .5); terazi(G, 720, 940, 700, Math.sin(st.t * 1.3) * .08 * (1 - st.p * .7), 'Zweig: tutku', 'Melville: zor');
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
P('G05b', 'G05@yaşındaki', (G, st) => { besikOda(G, st, { cam: [720, 760, 1.6] }); const k = acS(st, 'G05@kral', 1.4); tac(G, 720, lerp(380, 770, k), 150, { v: .3 }); return { look: { sepia: .26, strength: .3 }, ust: etiket([{ text: 'Stirling · 29 Temmuz 1567', size: 34, font: 'Cormorant Garamond', italic: true, at: st.at + .3 }], { y: 110 }) }; }, 'A');
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
P('H08', 'H08', (G, st) => { G.kamera(720, 560, lerp(1, 1.15, eio(st.p))); G.zemin(.16); isikHalka(G, 600, 380, 900, .5); G.mektup(720, 540, 760, 600, -.04, { px: 36, lh: 52, yazi: ['Madame ma bonne sœur…'], prog: 1 });
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
P('H13b', 'H13@ertesi', (G, st) => { yazMasa(G, st, { cam: [720, 620, 1.1], prog: st.p * 1.1, yazi: ['Madame ma bonne sœur, je vous supplie', 'm\'envoyer quérir le plus tôt que vous pourrez…'], manset: 'kirmizi' }); return { look: { sepia: .3, strength: .28 } }; }, 'A');
KART('H14', 'H14', [Lq('“Size yalvarırım,', 'H14', { size: 72 }), Lq('beni bir an önce yanınıza çağırın.', 'H14@beni', { size: 60 }), { text: '', size: 22 }, Ls('Mary\'den Elizabeth\'e · Workington, 17 Mayıs 1568', S('H14') + 1, { size: 26 })], { level: 2 });
P('H14b', 'H14@acınacak', fotoP('mary_dul_moncornet', [.5, .42, .62], [.5, .4, .46], { kunye: 'Mary Stuart · B. Moncornet, 17. yy · The Met (CC0)', look: { sepia: .24 } }), 'Y');
P('H15', 'H15', (G, st) => { const g = G.g; G.kamera(lerp(620, 760, eio(st.p)), lerp(600, 680, eio(st.p)), 1.35); G.zemin(.14); isikHalka(G, 700, 500, 800, .5);
  G.mektup(720, 600, 1000, 640, -.03, { px: 44, lh: 66, yazi: ['vostre tres fidelle et affectionnee bonne', 'soeur et cousine et eschapee prisonniere,', 'Marie R'], prog: clamp((st.t - AT('H15@sadık')) / (AT('H15@meri') + .6 - AT('H15@sadık'))) });
  const m = acS(st, 'H15@meri', 1); if (m > 0) G.muhur(1000, 820, 64, { acil: m });
  return { look: { sepia: .3, strength: .28 } }; }, 'A');
KART('H16', 'H16', [{ text: 'KAÇMIŞ TUTSAK', size: 104, font: 'Cinzel', weight: 700, spacing: 10, at: S('H16') }, { text: '', size: 26 }, Lq('Bu imza, ömrünün geri kalanının başlığı olacaktı.', 'H16@bu', { size: 46, weight: 500 })], { level: 0 });
P('H17', 'H17', fotoP('mary_clouet_beyazyas_resim', [.53, .32, .52], [.53, .3, .42], { kunye: 'Mary Stuart (Clouet\'den sonra) · kamu malı', iris: st => 1 - .5 * acS(st, 'H17@bitmişti', 2.5) }), 'Y');
