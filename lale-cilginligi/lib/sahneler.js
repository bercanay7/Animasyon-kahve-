// Planlar (Lale Çılgınlığı). Her plan bir gravür levhası + el boyaması lale + baskı yazısı. Klasik betik.
// Kurallar: renk yalnız lalede ve renk değerdir (çöküşte ve 1730'da söner, sonda kitap sayfalarında geri gelir);
// ardışık iki plan aynı ölçekte değil (tools/plan_denet.js); her plan ilk saniyeden hareketli (kamera ya da sözcüğe bağlı eylem);
// şiddet gösterilmez; cami/minare/haç yok; Osmanlı belgeleri Latin harfli aktarım.
'use strict';
const PLANS = []; window.PLAN = {};
window.GORSELLER = { mwLaleler: 'gorsel/mallewagen1637_laleler.jpg', mwMeyhane: 'gorsel/mallewagen1637_harlem_meyhane.jpg', semper: 'gorsel/semper_augustus_anonim_1640oncesi.jpg' };
const CAM = (cx, cy, z = 1) => ({ cx, cy, z });
const p01 = (st, a, b) => clamp((st.lt - a) / (b - a));
const io = t => E.io2(clamp(t));
// plan bildirimi: id, çapa ('B01', 'B01@kelime', '+0.3'), set (geçiş politikası için), ölçek, çizim işlevi (st → {cam, ciz, renk, sonra, bg}), o: {tr, over}
function PL(id, at, set, olcek, f, o = {}) { PLANS.push({ id, at, set, olcek, f, o }); }
function sahne(ctx, st, p) {
  const r = p.f(st), cam = r.cam || CAM(960, 540, 1);
  LALE.sifirla(); YAZI.sifirla();
  levha(ctx, cam, () => { if (r.ciz) r.ciz(); }, r.bg || [.05, 0, 0]);
  YAZI.bas(ctx, cam);
  LALE.boya(ctx, cam, r.renk ?? 1);
  if (r.sonra) r.sonra(ctx, cam, st);
}
// çapa zamanı (çekim içinde sözcüğe bağlı eylem için): lt cinsinden
const W_ = (st, id, w, n = 0) => Wd(id, w, n) - st.at;
const S_ = (st, id) => S(id) - st.at;
// bölüm kartları (YouTube bölümleriyle aynı)
const KART = {
  B01: ['I · YOLCULUK', 'Lale Avrupa\'ya nasıl gitti?'], C01: ['II · ALEV', 'En pahalı lale neden alevliydi?'],
  D01: ['III · RÜZGÂR TİCARETİ', 'Toprağın altındaki çiçek nasıl satılır?'], E01: ['IV · ÇÖKÜŞ', 'O para ödendi mi?'],
  F01: ['V · EFSANE', 'Hollanda gerçekten battı mı?'], G01: ['VI · İSTANBUL', 'Lale eve dönünce ne oldu?'],
  H01: ['VII · 1730', 'Bahçelerin sonunu ne getirdi?'], I02: ['VIII · AD', 'Bu döneme neden Lale Devri deriz?'],
};
const kartOver = (k) => (ctx, st) => chapterCard(ctx, KART[k][0], KART[k][1], st.lt, Math.min(3.6, st.d), { y: 400 });
const etk = (s, o = {}) => (ctx, st) => etiket(ctx, s, o.x ?? 150, o.y ?? 120, st.lt - (o.t0 || 0), Math.min(st.d - (o.t0 || 0), o.d ?? 5), { align: o.align || 'left', px: o.px || 44 });
const alnt = (s, kaynak, o = {}) => (ctx, st) => quote(ctx, s, o.x ?? W / 2, o.y ?? 190, st.lt, { px: o.px || 62, t0: o.t0 ?? .4, maxW: o.maxW || 1300, kaynak });
const both = (...fs) => (ctx, st) => fs.forEach(f => f && f(ctx, st));
const buyukYazi = (s, o = {}) => (ctx, st) => { const a = clamp((st.lt - (o.t0 || 0)) / .5); if (a <= 0) return; txt(ctx, s, o.x ?? W / 2, o.y ?? 160, { px: o.px || 96, ls: 6, a: E.sine(a), panel: .75, col: o.col }); };

// ═════════ 0. KANCA ═════════
// terazi: a eğim (+ sağ kefe aşağı: ev ağır); soğan kefesi sol
function terazi(st, a, o = {}) {
  const [L, R] = SET.terazi(960, 1000, a);
  LALE.sogan(L[0], L[1] - 38, 1.2); LALE.ciz(L[0], L[1] - 118, 1.0, { sap: 40, cesit: 'semper', ac: .3, renk: o.renk ?? 1 });
  SET.ev(R[0] - 110, R[1], 220, 170, { ton: .45, basamak: 3 });
}
PL('P001', 'A01', 'TER', 'orta', st => ({ cam: camLerp(CAM(960, 560, 1), CAM(960, 600, 1.08), st.p), bg: [.7, 0, 10],
  ciz: () => { GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.82), { th: 0, id: 10 }); terazi(st, lerp(.0, -.05, io(st.lt / 2))); } }));
PL('P002', 'A02', 'TER', 'yakin', st => ({ cam: camLerp(CAM(450, 640, 1.9), CAM(450, 660, 2.1), st.p), bg: [.7, 0, 10],
  ciz: () => { GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.82), { th: 0, id: 10 }); terazi(st, lerp(-.05, -.13, io(st.lt / 1.6))); } }));
// mezat salonu (kapı sahnesi): mezatçı, kâtip, alıcılar
function mezatSalonu(st, o = {}) {
  const t = st.t;
  SET.meyhane({ isik: .8 }); SET.masa(760, 640, 420); SET.saksi(970, 640, 1.0);
  LALE.ciz(970, 515, 1.15, { sap: 62, cesit: o.cesit || 'amiral', ac: .2, renk: o.lr ?? 1 });
  SET.isik({ x: 970, y: 520, r1: 520, a: .85 });
  INSAN.adam({ x: 1200, y: 900, h: 560, yon: -1, sapka: 'genis', yaka: 'duz', kenar: .55, kenarYan: -1, kolOn: { a: (o.mezatKol ?? 1.5) + .25 * Math.sin(t * 1.4), b: .9 }, biyik: true, sakal: true });
  INSAN.adam({ x: 720, y: 880, h: 480, yon: 1, sapka: 'genis', yaka: 'duz', kenar: .45, kolOn: { a: .9, b: .9 } });
  const A = [[200, 1150, 700, 1], [520, 1200, 760, -1], [1440, 1190, 740, 1], [1760, 1150, 700, -1]];
  A.forEach(([x, y, h, yon], i) => { const up = (o.el ?? true) && Math.sin(t * 1.8 + i * 1.7) > .2;
    INSAN.adam({ x, y, h, yon, arka: true, sapka: 'genis', yaka: 'duz', kenar: .4, kenarYan: yon, giysi: 'pelerin', kolOn: up ? { a: 2.1, b: 1.0 } : { a: .25, b: .3 } }); });
}
PL('P003', 'A03', 'MEZ', 'genis', st => ({ cam: camLerp(CAM(960, 540, 1), CAM(980, 560, 1.12), st.p), bg: [.1, 0, 0], ciz: () => mezatSalonu(st) }),
  { over: etk('ALKMAAR · ŞUBAT 1637') });
// yedi yetim: pencere önünde yedi küçük siluet (sırtı dönük), dışarıda bahçede laleler
PL('P004', 'A04', 'YET', 'orta', st => ({ cam: camLerp(CAM(960, 560, 1.05), CAM(960, 520, 1.12), st.p), bg: [.06, 0, 0], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.07), { th: 0, id: 0 });
  GR.fill(SET.R(360, 160, 1200, 560), GR.tone(.9), { th: -.03, id: 10 });
  SET.kasaba(520, .7); for (let k = 0; k < 9; k++) LALE.ciz(420 + k * 135, 680, .55, { sap: 70, cesit: ['semper', 'viceroy', 'switsers', 'amiral'][k % 4] });
  for (const x of [360, 760, 1160, 1560]) GR.fill(SET.R(x - 14, 160, 28, 560), GR.tone(.08), { th: HV_, id: 9 });
  GR.fill(SET.R(340, 700, 1240, 40), GR.tone(.2), { th: 0, id: 9 });
  for (let i = 0; i < 7; i++) { const h = 300 + ((i * 37) % 5) * 40; INSAN.adam({ x: 470 + i * 165, y: 1080, h, yon: i % 2 ? 1 : -1, arka: true, kenar: .35, palto: .5, kolOn: { a: .1, b: .1 } }); }
} }), { over: etk('WOUTER WINKEL\'İN YEDİ ÇOCUĞU', { y: 120 }) });
const HV_ = Math.PI / 2;
// 5.200 gulden ve beş küçük ev
PL('P005', 'A05', 'EVL', 'yakin', st => ({ cam: camLerp(CAM(960, 560, 1.15), CAM(960, 560, 1.0), io(st.lt / 3)), bg: [.75, 0, 10], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.85), { th: 0, id: 10 });
  GR.fill(SET.R(-200, 760, 2400, 600), GR.tone(.4), { th: 0, id: 8 });
  LALE.sogan(520, 700, 2.0); LALE.ciz(520, 560, 1.6, { sap: 40, cesit: 'amiral', ac: .25 });
  const k0 = W_(st, 'A05', 'beş', 1);
  for (let i = 0; i < 5; i++) { const a = clamp((st.lt - k0 - i * .22) / .3); if (a <= 0) continue; const x = 900 + i * 190, y = 760 + (1 - E.out3(a)) * 60; SET.ev(x, y, 150, 140 * E.out3(a) + 1, { ton: .3, basamak: 2, kat: 1 }); }
} }), { over: buyukYazi('5.200 GULDEN', { y: 170, px: 110 }) });
// İstanbul gecesi: köşk, lale tarhı, İbrahim Paşa
PL('P006', 'A06', 'IST', 'genis', st => ({ cam: camLerp(CAM(960, 560, 1), CAM(1000, 600, 1.1), st.p), bg: [.08, 0, 1], ciz: () => {
  SET2.bogaz(st.t, { gece: true, kx: 560, kw: 800 });
  for (let r = 0; r < 2; r++) for (let x = 120; x < 1850; x += 120) LALE.ciz(x + r * 50, 940 + r * 70, .7 + r * .2, { sap: 70 + r * 20, tip: 'ist', cesit: r ? 'istSari' : 'ist', ac: .1 });
  for (let x = 160; x < 1850; x += 300) { SET.kandil(x, 900, st.t + x, 1.2); SET.isik({ x, y: 900, r1: 200, a: .6 }); }
  SET2.osmanli({ x: 1400, y: 1000, h: 520, yon: -1, sarikTon: .55, kenar: .5, kenarYan: -1, kolOn: { a: .4, b: .6 }, sakal: true });
} }), { over: etk('NEVŞEHİRLİ DAMAT İBRAHİM PAŞA', { x: 1770, y: 120, align: 'right' }) });
PL('P007', 'A06@patrona', 'ISY', 'orta', st => ({ cam: camLerp(CAM(960, 620, 1.2), CAM(960, 640, 1.05), st.p), bg: [.05, 0, 1], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.05), { th: -.05, id: 1 });
  SET.kosk(560, 760, 800, 260, { gece: true });
  const r = 1 - io((st.lt - 2.2) / 2.5);
  for (let x = 100; x < 1850; x += 140) LALE.ciz(x, 860, .6, { sap: 60, tip: 'ist', cesit: 'ist', renk: r });
  SET2.kalabalik(st.t, { n: 10, mesale: 3 });
} }), { over: etk('PATRONA HALİL\'İN İSYANI · 1730') });
// Lale Devri adı: okul kitabı / gazete (Ahmed Refik'in tefrikasının ekimi)
PL('P008', 'A07', 'GAZ', 'ayrinti', st => ({ cam: camLerp(CAM(960, 540, 1.25), CAM(960, 500, 1.4), st.p), bg: [.2, 0, 0], ciz: () => {
  SET2.masaUst(-300, { ton: .2 });
  SET2.gazete(560, 140, 800, 860);
  YAZI.ekle('LÂLE DEVRİ', 960, 300, { font: 'baslik', px: 86, align: 'center', ls: 8 });
  YAZI.ekle('1130 – 1143', 960, 350, { font: 'serif', px: 34, align: 'center' });
  LALE.ciz(960, 520, 1.2, { sap: 60, tip: 'ist', cesit: 'ist', yaprakYok: true });
} }));

// ═════════ 1. YOL ═════════
PL('P010', 'B01', 'YOL', 'genis', st => ({ cam: camLerp(CAM(900, 560, 1), CAM(1060, 620, 1.12), st.p), bg: [.9, 0, 10], ciz: () => SET2.kisYolu({ t: st.t }) }),
  { over: both(kartOver('B01'), etk('1554 · EDİRNE–İSTANBUL YOLU', { t0: 3.4 })) });
PL('P011', 'B01@demet', 'YOL', 'yakin', st => ({ cam: camLerp(CAM(960, 560, 1.15), CAM(960, 520, 1.25), st.p), bg: [.85, 0, 10], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.88), { th: -.03, id: 10 });
  SET2.osmanli({ x: 520, y: 1220, h: 900, yon: 1, sapka: 'sarik', kenar: .4, kolOn: { a: 1.3, b: .5 } });
  INSAN.adam({ x: 1420, y: 1240, h: 920, yon: -1, sapka: 'genis', yaka: 'duz', giysi: 'pelerin', kenar: .4, kenarYan: -1, kolOn: { a: 1.2, b: .6 } });
  SET2.buket(960 + Math.sin(st.t) * 4, 760, 1.0, st.t);
} }), { over: etk('OGIER GHISELIN DE BUSBECQ, HABSBURG ELÇİSİ', { x: 1770, align: 'right', px: 40 }) });
PL('P012', 'B02', 'YOL', 'ayrinti', st => ({ cam: camLerp(CAM(960, 420, 1.7), CAM(960, 380, 1.9), st.p), bg: [.85, 0, 10], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.9), { th: -.03, id: 10 }); SET2.buket(960, 760, 1.0, st.t); } }),
  { over: alnt('“… eorum quos Turcae Tulipan vocant”', 'BUSBECQ, 1581', { y: 800, px: 58 }) });
PL('P013', 'B03', 'SAR', 'orta', st => ({ cam: camLerp(CAM(960, 520, 1.05), CAM(1080, 400, 1.35), st.p), bg: [.6, 0, 0], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.55), { th: .3, id: 0 }); SET.isik({ x: 1100, y: 300, r1: 800, a: .6 }); SET2.sarik(960, 640, 1.3); } }),
  { over: (ctx, st) => { const k = W_(st, 'B03', 'tülbendin'); etiket(ctx, 'TÜLBENT → TULIPAN → TULIP', 150, 120, st.lt - k, st.d - k, { align: 'left', px: 44 }); } });
PL('P014', 'B04', 'MEK', 'yakin', st => { const k = clamp(st.lt / Math.max(1, st.d)); return { cam: camLerp(CAM(1020, 640, 1.3), CAM(1000, 660, 1.45), st.p), bg: [.06, 0, 0], ciz: () => {
  SET2.mektupMasasi(st.t, { yaz: k });
  YAZI.ekle('Turcae flores valde excolunt …', 800, 640, { font: 'el', px: 30, kadar: k * 1.4 });
  YAZI.ekle('… Tulipan …', 820, 690, { font: 'el', px: 30, kadar: (k - .3) * 2 });
} }; });
PL('P015', 'B05', 'LEI', 'genis', st => ({ cam: camLerp(CAM(960, 560, 1), CAM(860, 600, 1.1), st.p), bg: [.9, 0, 10], ciz: () => SET2.leiden(st.t) }),
  { over: etk('LEIDEN · 1593 · CAROLUS CLUSIUS') });
PL('P016', 'B06', 'HIR', 'orta', st => ({ cam: camLerp(CAM(1000, 700, 1.25), CAM(1040, 760, 1.4), st.p), bg: [.05, 0, 1], ciz: () => SET2.hirsiz(st.t) }));

// ═════════ 2. ALEV ═════════
PL('P020', 'C01', 'ALE', 'yakin', st => ({ cam: camLerp(CAM(960, 560, 1.05), CAM(960, 520, 1.18), st.p), bg: [.85, 0, 10], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.9), { th: 0, id: 10 });
  [['semper', 560], ['viceroy', 960], ['switsers', 1360]].forEach(([c, x], i) => { const a = clamp((st.lt - .3 - i * .5) / .5); LALE.ciz(x, 620, 2.1, { sap: 300, cesit: c, ac: .3, renk: a, egim: Math.sin(st.t * .8 + i) * .02 }); });
} }), { over: kartOver('C01') });
// kırılma: düz kırmızı lale sözcükte alevli laleye döner
PL('P021', 'C02', 'TAR', 'orta', st => { const k = W_(st, 'C02', 'kırılacağını'); return { cam: camLerp(CAM(960, 600, 1), CAM(960, 640, 1.15), st.p), bg: [.9, 0, 10], ciz: () => {
  SET.gok({ gun: 1, ufuk: 520 }); SET.kasaba(520, .7);
  GR.fill(SET.R(-600, 520, 3100, 900), GR.tone(.25), { type: 'persp', y0: 520, D: 240, p0: 6, p1: 14, id: 8 });
  for (let k2 = 0; k2 < 7; k2++) { const x = 300 + k2 * 220, kir = k2 === 3 ? clamp((st.lt - k) / .8) : 0;
    LALE.ciz(x, 800, .95, { sap: 130, cesit: kir > .5 ? 'semper' : 'duz', ac: .2 }); }
} }; });
PL('P022', 'C03', 'ALE', 'ayrinti', st => ({ cam: camLerp(CAM(960, 440, 2.6), CAM(960, 400, 3.0), st.p), bg: [.88, 0, 10], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.92), { th: 0, id: 10 });
  LALE.ciz(960, 600, 2.4, { sap: 200, cesit: 'semper', ac: .2 });
  for (let k = 0; k < 4; k++) { const x = 880 + k * 50 + Math.sin(st.t * 2 + k) * 6, y = 520 - k * 30; GR.fill(SET.E2(x, y, 6, 4), GR.tone(.1), { th: 0, id: 9 }); }   // yaprak bitleri
} }), { over: (ctx, st) => { const k = W_(st, 'C03', 'virüsün'); etiket(ctx, 'LALE KIRILMA VİRÜSÜ', 150, 120, st.lt - k, st.d - k, { align: 'left' }); } });
PL('P023', 'C04', 'ALE', 'yakin', st => ({ cam: camLerp(CAM(960, 600, 1.2), CAM(960, 620, 1.3), st.p), bg: [.15, 0, 4], ciz: () => {
  SET2.kesit(st.t); for (let k = 0; k < 3; k++) { const a = 1 - clamp((st.lt - 1 - k * .6) / 1.2); if (a > 0) LALE.sogan(1160 + k * 70, 900 + k * 10, .4 * a + .05, { ton: .6 }); }
} }));
// C05 başı: gerçek görsel. Anonim, Semper Augustus suluboyası (1640 öncesi; Norton Simon Müzesi; Commons, kamu malı). Renk lalede: kural bozulmaz
PL('P024a', 'C05', 'SEM', 'ayrinti', st => ({ cam: camLerp(CAM(960, 470, 1.0), CAM(960, 420, 1.12), st.p), bg: [.88, 0, 10], ciz: () => { GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.9), { th: 0, id: 10 }); },
  sonra: (ctx, cam) => { SET2.gorsel(ctx, cam, 'semper', 700, 40, 520, { golge: true }); } }),
  { over: etk('SEMPER AUGUSTUS · ANONİM SULUBOYA, 1640 ÖNCESİ (NORTON SIMON MÜZESİ)', { px: 32 }) });
PL('P024', 'C05@bin', 'AYN', 'orta', st => ({ cam: camLerp(CAM(960, 520, 1), CAM(960, 520, 1.12), st.p), bg: [.2, 0, 0], ciz: () => SET2.aynaKabine(st.t) }),
  { over: (ctx, st) => { const k = W_(st, 'C05', 'bin', 1); buyukYazi('1.200 GULDEN', { y: 800, px: 84, t0: k })(ctx, st); } });
PL('P025', 'C06', 'KES', 'yakin', st => { const g = io((st.lt - 1.6) / .8); return { cam: camLerp(CAM(960, 620, 1.3), CAM(960, 620, 1.4), st.p), bg: [.15, 0, 0], ciz: () => {
  SET2.masaUst(500, { ton: .2 }); SET2.kese(860 + g * 160, 760, 1.6); SET2.para(1200, 760, 6, 1.2);
  INSAN.adam({ x: 1500, y: 1500, h: 1300, yon: -1, sapka: 'genis', yaka: 'duz', kenar: .4, kolOn: { a: 1.4 - g * .3, b: .3 } });
} }; }, { over: buyukYazi('3.000 GULDEN', { y: 160, px: 96 }) });

// ═════════ 3. RÜZGÂR TİCARETİ ═════════
PL('P030', 'D01', 'EKI', 'genis', st => ({ cam: camLerp(CAM(960, 560, 1), CAM(1000, 600, 1.1), st.p), bg: [.9, 0, 10], ciz: () => SET2.ekim(st.t) }),
  { over: both(kartOver('D01'), etk('1636 SONBAHARI', { t0: 3.4 })) });
PL('P031', 'D02', 'SOZ', 'ayrinti', st => { const k = clamp(st.lt / 6); return { cam: camLerp(CAM(960, 520, 1.1), CAM(960, 560, 1.2), st.p), bg: [.86, 0, 10], ciz: () => {
  SET2.kesit(st.t); SET2.sayfa(620, 120, 680, 380, { ton: .96, cerceve: true });
  YAZI.ekle('Semper Augustus — 200 aes', 680, 220, { font: 'el', px: 38, kadar: k * 2 });
  YAZI.ekle('te leveren in Junij · te betalen in Junij', 680, 290, { font: 'el', px: 32, kadar: (k - .3) * 2 });
  YAZI.ekle('Haarlem, 1636', 680, 360, { font: 'el', px: 30, kadar: (k - .55) * 3 });
  SET2.kalem(1000 + k * 200, 400, -.8, .9);
} }; }, { over: (ctx, st) => { const k = W_(st, 'D02', 'haziranda'); etiket(ctx, 'HAZİRANDA TESLİM · HAZİRANDA ÖDEME', W / 2, 820, st.lt - k, st.d - k, { align: 'center', px: 42 }); } });
// kâğıt elden ele: masada uzanan eller, kâğıt sırayla geçer
PL('P032', 'D03', 'ODA', 'orta', st => ({ cam: camLerp(CAM(960, 620, 1.1), CAM(960, 600, 1.2), st.p), bg: [.08, 0, 0], ciz: () => {
  SET2.arkaOda(st.t);
  const pos = [[560, 760], [960, 720], [1360, 760]], k = (st.lt * .8) % 3, i = Math.floor(k), u = E.io2(k - i), a = pos[i], b = pos[(i + 1) % 3];
  SET2.sayfa(lerp(a[0], b[0], u) - 70, lerp(a[1], b[1], u) - 120 - Math.sin(u * PI) * 60, 140, 100, { ton: .95 });
  INSAN.adam({ x: 380, y: 1200, h: 800, yon: 1, arka: true, sapka: 'genis', yaka: 'duz', kenar: .35, kolOn: { a: .9, b: 1.0 } });
  SET2.usta({ x: 1560, y: 1200, h: 800, yon: -1, kenar: .4, kenarYan: -1, kolOn: { a: .9, b: 1.0 } });
} }));
PL('P033', 'D04', 'RUZ', 'genis', st => ({ cam: camLerp(CAM(960, 520, 1), CAM(1100, 500, 1.08), st.p), bg: [.9, 0, 10], ciz: () => {
  SET.gok({ gun: 1, ufuk: 640 }); SET.kasaba(640, .8); SET.degirmen(1500, 640, .8, st.t * 1.2);
  GR.fill(SET.R(-600, 640, 3100, 900), GR.tone(.3), { type: 'persp', y0: 640, D: 240, p0: 6, p1: 14, id: 8 });
  for (let k = 0; k < 14; k++) { const ph = (st.t * .12 + k * .071) % 1, x = -200 + ph * 2400, y = 300 + Math.sin(k * 2.1 + st.t * 1.3) * 120 + k * 22, r = st.t * 2 + k;
    GR.save(); GR.frame(x, y, Math.sin(r) * .8, 1, 1); SET2.sayfa(-50, -36, 100, 72, { ton: .95 }); GR.restore(); }
} }), { over: etk('WINDHANDEL · RÜZGÂR TİCARETİ') });
// D05: gerçek görsel. Crispijn van de Passe II, Floraes Mallewagen (1637), köşe resmi: Haarlem'de çiçekçilerin meyhane toplantısı (Rijksmuseum, CC0)
PL('P034', 'D05', 'ODA', 'yakin', st => ({ cam: camLerp(CAM(960, 540, 1.0), CAM(1060, 520, 1.12), st.p), bg: [.15, 0, 0], ciz: () => { SET2.masaUst(-300, { ton: .14 }); },
  sonra: (ctx, cam) => { SET2.gorsel(ctx, cam, 'mwMeyhane', 160, 60, 1600, { kirp: [0, 0, 1, .86] }); } }),
  { over: etk('“COMPARITY DER BLOEMISTEN TOT HARLEM” · 1637 GRAVÜRÜ (RIJKSMUSEUM)', { y: 120, px: 34 }) });
// Switsers: fiyat çizgisi gibi yükselen sap; renk koyulaşır
PL('P035', 'D06', 'SWI', 'ayrinti', st => { const u = io((st.lt - .5) / Math.max(1, st.d - 1)); return { cam: camLerp(CAM(960, 560, 1), CAM(960, 520, 1.05), st.p), bg: [.88, 0, 10], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.93), { th: 0, id: 10 });
  for (let k = 0; k < 6; k++) GR.fill(SET.R(260, 900 - k * 140, 1400, 2), GR.tone(.5), { th: 0, id: 9 });
  const x = 1500, y = 900 - u * 700;
  const p = new Path2D(); p.moveTo(300, 880); p.bezierCurveTo(800, 870, 1200, 800 - u * 300, x, y + 40); p.lineTo(x + 6, y + 44); p.bezierCurveTo(1200, 806 - u * 300, 800, 876, 300, 886); p.closePath();
  GR.fill(p, GR.tone(.15), { th: 0, id: 9 });
  LALE.ciz(x, y, 1.2 + u * .6, { sap: 0, cesit: 'switsers', ac: .2 + u * .2, renk: .4 + u * .6 });
  YAZI.ekle('31 ARALIK 1636 · 125', 300, 960, { font: 'baslik', px: 30 }); YAZI.ekle('1 ŞUBAT 1637 · ' + Math.round(125 + u * 1375), 1240, 960, { font: 'baslik', px: 30 });
} }; }, { over: etk('SWITSERS · GULDEN / POUND') });
PL('P036', 'D07', 'MEZ', 'orta', st => ({ cam: camLerp(CAM(1040, 560, 1.3), CAM(1060, 540, 1.4), st.p), bg: [.1, 0, 0], ciz: () => mezatSalonu(st, { mezatKol: 2.1 }) }));
PL('P037', 'D08', 'LIS', 'ayrinti', st => { const k = W_(st, 'D08', 'kâğıt'); return { cam: camLerp(CAM(960, 520, 1.1), CAM(960, 540, 1.0), st.p), bg: [.2, 0, 0], ciz: () => {
  SET2.masaUst(-300, { ton: .2 }); SET2.sayfa(560, 80, 800, 720, { ton: .95, cerceve: true });
  YAZI.ekle('Lijste van eenighe Tulpaen', 960, 170, { font: 'baslik', px: 40, align: 'center' });
  YAZI.ekle('verkocht aen de meest-biedende, op den 5. Februarij 1637', 960, 215, { font: 'italik', px: 28, align: 'center' });
  const L = [['Admirael van Enkhuysen', '5200'], ['Viceroy', '4203'], ['Brabanson', '1600'], ['Bruyn Purper', '2025'], ['Paragon van Delft', '605']];
  L.forEach(([a, b], i) => { YAZI.ekle(a, 640, 290 + i * 52, { font: 'serif', px: 32 }); YAZI.ekle(b + ' gl.', 1280, 290 + i * 52, { font: 'serif', px: 32, align: 'right' }); });
  YAZI.ekle('90.000', 960, 620, { font: 'baslik', px: 64, align: 'center', a: clamp(st.lt / .8) });
  for (let i = 0; i < 7; i++) { const a = clamp((st.lt - k - i * .12) / .4); if (a > 0) SET2.para(640 + i * 105, 760, 3 + Math.round(a * 3), .8); }
} }; });
PL('P038', 'D09', 'KES', 'yakin', st => ({ cam: camLerp(CAM(960, 560, 1.1), CAM(960, 700, 1.3), io(st.lt / Math.max(2, st.d))), bg: [.86, 0, 10], ciz: () => {
  SET2.kesit(st.t); SET2.sayfa(700, 180, 520, 280, { ton: .96 }); YAZI.ekle('Junij', 960, 340, { font: 'el', px: 64, align: 'center' });
} }), { over: buyukYazi('KÂĞIT ÜZERİNDE', { y: 150, px: 88 }) });

// ═════════ 4. ÇÖKÜŞ ═════════
PL('P040', 'E01', 'MEZ', 'genis', st => { const r = 1 - io((st.lt - 3.6) / 2.5); return { cam: camLerp(CAM(960, 540, 1.0), CAM(970, 520, 1.15), st.p), bg: [.1, 0, 0], ciz: () => mezatSalonu(st, { el: false, mezatKol: 2.1, cesit: 'switsers', lr: r }), renk: 1 }; },
  { over: both(kartOver('E01'), etk('HAARLEM · ŞUBAT 1637', { t0: 3.4 })) });
PL('P041', 'E02', 'BOS', 'orta', st => ({ cam: camLerp(CAM(960, 600, 1.05), CAM(900, 620, 1.15), st.p), bg: [.08, 0, 0], renk: 1 - io(st.lt / 3), ciz: () => {
  SET.meyhane({ isik: .5 });
  for (let k = 0; k < 5; k++) { const x = 300 + k * 330; GR.fill(SET.R(x, 840, 120, 14), GR.tone(.2), { th: 0, id: 9 }); GR.fill(SET.R(x + 8, 850, 12, 130), GR.tone(.1), { th: HV_, id: 9 }); GR.fill(SET.R(x + 100, 850, 12, 130), GR.tone(.1), { th: HV_, id: 9 }); GR.fill(SET.R(x + 100, 680, 14, 170), GR.tone(.1), { th: HV_, id: 9 }); }
  for (let k = 0; k < 9; k++) { const x = 200 + k * 190, y = 1010 + (k % 3) * 20; GR.save(); GR.frame(x, y, (k - 4) * .2, 1, 1); SET2.sayfa(-60, -30, 120, 60, { ton: .94 }); GR.restore(); }
  SET.saksi(1500, 830, .8); LALE.ciz(1500, 770, .8, { sap: 50, cesit: 'semper' });
} }));
// E02 ikinci yarı: gerçek görsel. Aynı 1637 hiciv gravüründe yere düşmüş, adları yazılı laleler (Viceroy, Admirael Catelyn, Gouda…)
PL('P041b', 'E02@dünün', 'MWL', 'ayrinti', st => ({ cam: camLerp(CAM(700, 540, 1.25), CAM(1220, 540, 1.25), io(st.lt / Math.max(2, st.d))), bg: [.15, 0, 0], renk: 0, ciz: () => { SET2.masaUst(-300, { ton: .12 }); },
  sonra: (ctx, cam) => { SET2.gorsel(ctx, cam, 'mwLaleler', -60, 300, 2040, { kirp: [.035, 0, .965, 1] }); } }),
  { over: etk('ÇİĞNENMİŞ LALELER · FLORAES MALLEWAGEN, 1637 (RIJKSMUSEUM)', { y: 120, px: 34 }) });
PL('P042', 'E03', 'AMS', 'yakin', st => ({ cam: camLerp(CAM(960, 620, 1.2), CAM(960, 600, 1.3), st.p), bg: [.08, 0, 0], renk: 0, ciz: () => {
  SET2.arkaOda(st.t);
  for (let i = 0; i < 4; i++) { const x = 560 + i * 280, yon = i < 2 ? 1 : -1; INSAN.adam({ x, y: 1030, h: 600, yon, sapka: 'genis', yaka: 'duz', kenar: .45, kenarYan: yon, kolOn: { a: .5 + Math.sin(st.t * 3 + i) * .3, b: 1.0 }, biyik: i % 2 === 0 }); }
} }), { over: etk('AMSTERDAM · 23–24 ŞUBAT 1637') });
PL('P043', 'E04', 'HAZ', 'orta', st => ({ cam: camLerp(CAM(960, 560, 1.05), CAM(1060, 580, 1.15), st.p), bg: [.9, 0, 10], renk: 0, ciz: () => {
  SET.gok({ gun: 1, ufuk: 640 });
  GR.fill(SET.R(-600, 640, 3100, 900), GR.tone(.3), { type: 'persp', y0: 640, D: 240, p0: 6, p1: 14, id: 8 });
  SET.ev(1100, 900, 420, 360, { ton: .2, basamak: 4, kat: 2 });
  for (let k = 0; k < 6; k++) LALE.sogan(300 + k * 110, 980, .5, { ton: .5 });
  INSAN.adam({ x: 1060, y: 960, h: 520, yon: 1, sapka: 'genis', yaka: 'duz', kenar: .5, kolOn: { a: 1.6 + Math.max(0, Math.sin(st.t * 6)) * .3, b: .9 } });
  SET2.kese(860, 960, .8);
} }), { over: etk('HAZİRAN 1637') });
PL('P044', 'E05', 'MAH', 'genis', st => ({ cam: camLerp(CAM(960, 520, 1), CAM(960, 500, 1.08), st.p), bg: [.85, 0, 10], renk: 0, ciz: () => {
  SET.gok({ gun: 1, ufuk: 900 });
  GR.fill(SET.R(360, 260, 1200, 640), GR.tone(.3), { th: 0, id: 4 });
  GR.fill(INSAN.F([[300, 270], [1620, 270], [960, 90]]), GR.tone(.15), { th: 0, id: 9 });
  for (let k = 0; k < 6; k++) GR.fill(SET.R(420 + k * 210, 330, 60, 570), GR.tone(.7), { th: HV_, id: 9 });
  GR.fill(SET.R(860, 640, 200, 260), GR.tone(.03), { th: HV_, id: 9 });
  GR.fill(SET.R(-600, 900, 3100, 600), GR.tone(.5), { type: 'persp', y0: 900, D: 200, p0: 8, p1: 15, id: 8 });
} }), { over: etk('HOF VAN HOLLAND · DEN HAAG') });
PL('P045', 'E06', 'KAR', 'ayrinti', st => ({ cam: camLerp(CAM(960, 520, 1.2), CAM(960, 520, 1.3), st.p), bg: [.2, 0, 0], renk: 0, ciz: () => {
  SET2.masaUst(-300, { ton: .2 }); SET2.sayfa(620, 140, 680, 760, { ton: .95, cerceve: true });
  YAZI.ekle('Haerlem, 1638', 960, 250, { font: 'baslik', px: 36, align: 'center' }); SET2.satirlar(680, 320, 560, 7, 34);
  const a = clamp((st.lt - W_(st, 'E06', 'yüzde')) / .3); YAZI.ekle('3½ %', 960, 760, { font: 'baslik', px: 120, align: 'center', a, renk: [120, 20, 20] });
} }));
PL('P046', 'E07', 'LIS', 'yakin', st => ({ cam: camLerp(CAM(960, 460, 1.4), CAM(960, 420, 1.6), st.p), bg: [.2, 0, 0], renk: 0, ciz: () => {
  SET2.masaUst(-300, { ton: .14 }); SET2.sayfa(560, 80, 800, 720, { ton: .9, cerceve: true });
  YAZI.ekle('Lijste van eenighe Tulpaen', 960, 170, { font: 'baslik', px: 40, align: 'center', a: .6 }); YAZI.ekle('90.000', 960, 460, { font: 'baslik', px: 96, align: 'center' }); YAZI.ekle('?', 1200, 470, { font: 'baslik', px: 120, align: 'center', a: clamp((st.lt - 1.2) / .5) });
} }));

// ═════════ 5. EFSANE ═════════
PL('P050', 'F01', 'MAT', 'genis', st => ({ cam: camLerp(CAM(960, 540, 1), CAM(1000, 520, 1.1), st.p), bg: [.1, 0, 0], renk: 0, ciz: () => SET2.matbaa(st.t) }),
  { over: both(kartOver('F01'), etk('HAARLEM · 1637', { t0: 3.4 })) });
PL('P051', 'F02', 'BRO', 'ayrinti', st => ({ cam: camLerp(CAM(960, 520, 1.15), CAM(960, 500, 1.25), st.p), bg: [.2, 0, 0], renk: 0, ciz: () => {
  SET2.masaUst(-300, { ton: .2 }); SET2.sayfa(600, 60, 720, 900, { ton: .93, cerceve: true });
  YAZI.ekle('SAMEN-SPRAECK', 960, 180, { font: 'baslik', px: 48, align: 'center' }); YAZI.ekle('tusschen', 960, 225, { font: 'italik', px: 30, align: 'center' });
  YAZI.ekle('WAERMONDT ende GAERGOEDT', 960, 275, { font: 'baslik', px: 36, align: 'center' }); YAZI.ekle('nopende de opkomste ende ondergangh van Flora', 960, 320, { font: 'italik', px: 26, align: 'center' });
  INSAN.adam({ x: 820, y: 820, h: 420, yon: 1, sapka: 'genis', yaka: 'duz', kenar: .5, kolOn: { a: 1.0 + Math.sin(st.t * 2) * .2, b: .8 } });
  SET2.usta({ x: 1100, y: 820, h: 420, yon: -1, kenar: .5, kenarYan: -1, kolOn: { a: 1.2 + Math.sin(st.t * 2 + 1) * .2, b: .9 } });
  YAZI.ekle('HAERLEM · ADRIAEN ROMAN · 1637', 960, 900, { font: 'baslik', px: 24, align: 'center' });
} }), { over: (ctx, st) => { const k = W_(st, 'F02', 'doğrucu'); etiket(ctx, 'WAERMONDT = DOĞRUCU · GAERGOEDT = AÇGÖZLÜ', W / 2, 830, st.lt - k, st.d - k, { align: 'center', px: 40 }); } });
PL('P052', 'F03', 'DOK', 'orta', st => { const k = W_(st, 'F03', 'tezgâhını'); const g = io((st.lt - k) / 1.6); return { cam: camLerp(CAM(960, 560, 1.05), CAM(960, 580, 1.12), st.p), bg: [.1, 0, 0], renk: 0, ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.12), { th: 0, id: 0 }); GR.fill(SET.R(-600, 900, 3100, 600), GR.tone(.25), { type: 'persp', y0: 900, D: 200, p0: 8, p1: 15, id: 8 });
  SET.isik({ x: 600, y: 300, r1: 900, a: .6 });
  SET2.tezgah(1200 + g * 700, 900, 1, g * .1);
  SET2.usta({ x: 560, y: 980, h: 640, yon: 1, kenar: .5, kolOn: { a: .2, b: .1 }, bas: .25 });
} }; }, { over: (ctx, st) => { const k = W_(st, 'F03', 'çılgınlıktı'); quote(ctx, '“Bir çılgınlıktı.”', W / 2, 190, st.lt - k + .4, { px: 70, kaynak: 'SAMEN-SPRAECK, 1637' }); } });
PL('P053', 'F04', 'MAC', 'genis', st => ({ cam: camLerp(CAM(960, 560, 1), CAM(1000, 600, 1.12), st.p), bg: [.08, 0, 0], renk: 0, ciz: () => {
  SET2.mackayOda(st.t); INSAN.adam({ x: 760, y: 1060, h: 620, yon: 1, arka: true, kenar: .45, kolOn: { a: .8, b: 1.0 } });
} }), { over: etk('CHARLES MACKAY · LONDRA, 1841') });
// denizci: rıhtımda oturur, soğanı ringa balığıyla yer
PL('P054', 'F05', 'RIH', 'orta', st => { const k = W_(st, 'F05', 'yiyor'); const isir = clamp((st.lt - k) / .4); return { cam: camLerp(CAM(1000, 640, 1.15), CAM(1040, 660, 1.3), st.p), bg: [.9, 0, 10], ciz: () => {
  SET2.rihtim(st.t);
  INSAN.adam({ x: 1000, y: 900, h: 460, yon: 1, egim: -.05, sapka: true, kenar: .45, kolOn: { a: 1.9 + Math.sin(st.t * 3) * .1 * isir, b: 1.1 }, kolArka: { a: .9, b: .4 } });
  LALE.sogan(1150, 560 + isir * 10, .45 * (1 - isir * .4), { ton: .5 });
  GR.fill(SET.E2(1040, 820, 60, 14, .2), GR.tone(.6), { th: 0, id: 9 });   // ringa
} }; }, { over: (ctx, st) => { const k = W_(st, 'F05', 'semper'); etiket(ctx, 'SEMPER AUGUSTUS', 1770, 120, st.lt - k, st.d - k, { align: 'right' }); } });
PL('P055', 'F06', 'BAC', 'yakin', st => ({ cam: camLerp(CAM(1000, 560, 1.15), CAM(1040, 500, 1.25), st.p), bg: [.88, 0, 10], ciz: () => {
  SET.gok({ gun: 1, ufuk: 1000 }); SET.ev(-100, 1100, 1300, 700, { ton: .25, basamak: 4, kat: 3 }); SET2.bacaci(900, 1040, st.t);
} }), { over: (ctx, st) => quote(ctx, '“… even chimney-sweeps …”', W / 2 + 300, 780, st.lt, { px: 52, kaynak: 'MACKAY, 1841', maxW: 900 }) });
PL('P056', 'F07', 'KIT', 'genis', st => ({ cam: camLerp(CAM(960, 560, 1), CAM(960, 400, 1.15), st.p), bg: [.15, 0, 0], renk: 0, ciz: () => {
  SET2.masaUst(820, { ton: .2 }); GR.fill(SET.R(-600, -500, 3100, 1320), GR.tone(.1), { th: 0, id: 0 });
  const n = Math.min(9, 2 + Math.floor(st.lt * 1.4)); for (let i = 0; i < n; i++) SET2.kitap(700 - (i % 2) * 20, 760 - i * 66, 520, 60, { ton: .1 + (i % 3) * .2 });
} }), { over: etk('1841 → 1900 → 1950 → 2000') });
PL('P057', 'F08', 'ARS', 'orta', st => ({ cam: camLerp(CAM(960, 560, 1.02), CAM(1040, 660, 1.2), st.p), bg: [.07, 0, 0], renk: 0, ciz: () => {
  SET2.arsiv(st.t); INSAN.adam({ x: 620, y: 1100, h: 640, yon: 1, arka: true, palto: .4, kenar: .45, kolOn: { a: 1.4, b: .5 } });
} }), { over: etk('ANNE GOLDGAR · TULIPMANIA, 2007') });
PL('P058', 'F09', 'ARS', 'ayrinti', st => ({ cam: camLerp(CAM(960, 520, 1.15), CAM(960, 520, 1.25), st.p), bg: [.2, 0, 0], renk: 0, ciz: () => {
  SET2.masaUst(-300, { ton: .16 }); SET2.defter(360, 160, 1200, 760, { cizgi: 14 });
  YAZI.ekle('faillissementen · 1637–1638', 400, 220, { font: 'el', px: 34 });
  for (let i = 0; i < 10; i++) YAZI.ekle('—', 520, 300 + i * 44, { font: 'serif', px: 32, a: clamp((st.lt - i * .25) / .3) });
  YAZI.ekle('0', 1340, 560, { font: 'baslik', px: 140, align: 'center', a: clamp((st.lt - 2.6) / .4), renk: [120, 20, 20] });
} }));
PL('P059', 'F10', 'ISI', 'genis', st => ({ cam: camLerp(CAM(960, 540, 1), CAM(960, 540, 1.08), st.p), bg: [.9, 0, 10], renk: 0, ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.92), { th: 0, id: 10 });
  for (let i = 0; i < 70; i++) { const x = 200 + (i % 14) * 110, y = 260 + Math.floor(i / 14) * 130, a = clamp((st.lt - i * .03) / .3); if (a > 0) INSAN.adam({ x, y: y + 110, h: 110 * a, yon: i % 2 ? 1 : -1, arka: i % 3 === 0, sapka: 'genis', yaka: 'duz', kenar: .5 }); }
} }), { over: etk('AŞAĞI YUKARI 350 AD') });
PL('P05A', 'F11', 'SOZ', 'yakin', st => { const k = W_(st, 'F11', 'tutulmayan'); const y = io((st.lt - k) / 1.0); return { cam: camLerp(CAM(960, 560, 1.15), CAM(960, 560, 1.25), st.p), bg: [.2, 0, 0], renk: 0, ciz: () => {
  SET2.masaUst(-300, { ton: .2 });
  SET2.sayfa(620 - y * 80, 300, 340, 440, { ton: .95 }); SET2.sayfa(960 + y * 80, 300, 340, 440, { ton: .95 });
  YAZI.ekle('te betalen in Junij', 650 - y * 80, 400, { font: 'el', px: 34 }); SET2.satirlar(650 - y * 80, 460, 280, 6, 34); SET2.satirlar(990 + y * 80, 460, 280, 6, 34);
} }; });

// ═════════ 6. İSTANBUL ═════════
PL('P060', 'G01', 'IST', 'orta', st => ({ cam: camLerp(CAM(960, 560, 1), CAM(1000, 560, 1.1), st.p), bg: [.9, 0, 10], ciz: () => {
  SET2.bogaz(st.t, { kx: 1000, kw: 700 });
  SET2.osmanli({ x: 520, y: 1040, h: 560, yon: 1, kenar: .5, sakal: true, kolOn: { a: .3, b: .5 } });
  SET2.osmanli({ x: 720, y: 1040, h: 520, yon: 1, kenar: .5, sakal: true, kolOn: { a: .8, b: .7 } });
  for (let x = 1100; x < 1900; x += 110) LALE.ciz(x, 1000, .8, { sap: 80, tip: 'ist', cesit: x % 220 ? 'ist' : 'istSari' });
} }), { over: both(kartOver('G01'), etk('III. AHMED · NEVŞEHİRLİ DAMAT İBRAHİM PAŞA · 1718', { t0: 3.4, px: 38 })) });
PL('P061', 'G02', 'SAA', 'genis', st => { const u = io(st.lt / Math.max(2, st.d - .5)); return { cam: camLerp(CAM(960, 600, 1.1), CAM(960, 580, 1.2), st.p), bg: [.9, 0, 10], ciz: () => {
  SET.gok({ gun: 1, ufuk: 700 });
  GR.fill(SET.R(-600, 700, 3100, 140), GR.tone(.72), { th: .01, id: 8 });
  SET.kosk(560, 700, 800, 300 * (.3 + u * .7), {});
  for (const [x, h] of [[250, 460], [1700, 520]]) SET.servi(x, 760, h);
  GR.fill(SET.R(-600, 840, 3100, 600), GR.tone(.35), { type: 'persp', y0: 840, D: 200, p0: 7, p1: 14, id: 8 });
} }; }, { over: etk('SAADABAD · KÂĞITHANE') });
PL('P062', 'G03', 'GEC', 'orta', st => ({ cam: camLerp(CAM(960, 620, 1.05), CAM(900, 640, 1.18), st.p), bg: [.08, 0, 1], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.08), { th: -.05, id: 1 });
  SET.kosk(560, 640, 800, 300, { gece: true });
  for (const [x, h] of [[300, 520], [1500, 600], [1700, 480]]) SET.servi(x, 700, h);
  GR.fill(SET.R(-200, 700, 2400, 500), GR.tone(.12), { type: 'persp', y0: 700, D: 200, p0: 7, p1: 14, id: 8 });
  for (let r = 0; r < 3; r++) for (let x = 120; x < 1850; x += 110) LALE.ciz(x + r * 40, 800 + r * 90, .6 + r * .2, { tip: 'ist', sap: 60 + r * 20, cesit: r === 1 ? 'istSari' : 'ist', ac: .1 });
  for (let x = 160; x < 1850; x += 220) { SET.kandil(x, 760, st.t + x, 1.2); SET.isik({ x, y: 760, r1: 170, a: .6 }); }
  const kx = 300 + st.lt * 60; SET.kaplumbaga(kx, 1010, 1.2, st.t); SET.isik({ x: kx, y: 900, r1: 220, a: .7 });
} }), { over: etk('ÇIRAĞAN · ANLATILANLARA GÖRE') });
PL('P063', 'G04', 'NIZ', 'yakin', st => ({ cam: camLerp(CAM(960, 520, 1.1), CAM(960, 480, 1.2), st.p), bg: [.88, 0, 10], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.9), { th: 0, id: 10 }); SET.isik({ x: 960, y: 400, r1: 800, a: .5 });
  LALE.ciz(960, 520, 2.6, { sap: 420, tip: 'ist', cesit: 'ist', ac: .05, egim: Math.sin(st.t * .7) * .02 });
} }), { over: (ctx, st) => { const k = W_(st, 'G04', 'nizeyi'); etiket(ctx, 'NÎZE-İ RUMMÂNÎ · NAR RENKLİ MIZRAK', 150, 120, st.lt - k, st.d - k, { align: 'left' }); } });
PL('P064', 'G05', 'CAR', 'genis', st => ({ cam: camLerp(CAM(960, 540, 1), CAM(1000, 560, 1.1), st.p), bg: [.3, 0, 0], ciz: () => {
  SET2.carsi(st.t);
  SET2.osmanli({ x: 700, y: 1060, h: 560, yon: 1, sapka: 'sarik', kenar: .45, kolOn: { a: 1.4, b: .6 } }); SET2.osmanli({ x: 1100, y: 1060, h: 540, yon: -1, sapka: 'sarik', kenar: .45, kenarYan: -1, kolOn: { a: 1.4, b: .6 } });
  SET2.para(900, 760, 3 + Math.floor(st.lt * 2) % 4, .8);
} }));
// kadı defteri: Latin harfli aktarım (Aktepe'nin yayımladığı listeden)
function narhDefteri(st, o = {}) {
  SET2.masaUst(-300, { ton: .2 }); SET2.defter(260, 120, 1400, 820, { cizgi: 15 });
  YAZI.ekle(o.baslik || 'Lâle-i rûmî ecnâsının fiat defteri · 27 Şevval 1138', 300, 175, { font: 'el', px: 30 });
  const L = o.liste || [['Nîze-i rummânî', '50 kuruş'], ['…', ''], ['…', ''], ['Bıyıklı', '1 akçe'], ['Şirin', '1 akçe']];
  L.forEach(([a, b], i) => { const al = clamp((st.lt - .3 - i * .25) / .4); YAZI.ekle(a, 320, 260 + i * 46, { font: 'serif', px: 34, a: al }); YAZI.ekle(b, 940, 260 + i * 46, { font: 'serif', px: 34, align: 'right', a: al }); });
  LALE.ciz(1250, 520, 1.6, { sap: 150, tip: 'ist', cesit: 'ist', ac: .05 });
}
PL('P065', 'G06', 'NAR', 'ayrinti', st => ({ cam: camLerp(CAM(960, 520, 1.05), CAM(900, 480, 1.15), st.p), bg: [.2, 0, 0], ciz: () => narhDefteri(st) }),
  { over: both(etk('İSTANBUL KADILIĞI DEFTERİ · 28 HAZİRAN 1726', { px: 38 }), (ctx, st) => etiket(ctx, 'Latin harfli aktarım: M. Münir Aktepe, 1953', W / 2, 830, st.lt - 1, st.d - 1, { align: 'center', px: 30 })) });
PL('P066', 'G07', 'SUR', 'orta', st => ({ cam: camLerp(CAM(960, 600, 1.05), CAM(1060, 620, 1.15), st.p), bg: [.85, 0, 10], ciz: () => {
  SET2.bogaz(st.t, { kosk: false, servi: [[200, 420]] }); SET2.gemi(1400, 700, 1, st.t);
  SET2.osmanli({ x: 700, y: 1040, h: 560, yon: -1, sapka: 'kavuk', kenar: .45, kenarYan: -1, kolOn: { a: 1.2, b: .6 } });
  SET.saksi(590, 880, .7); LALE.ciz(590, 830, .6, { sap: 40, tip: 'ist', cesit: 'ist' });
  SET2.osmanli({ x: 1080 + st.lt * 20, y: 1040, h: 520, yon: 1, arka: true, sapka: 'sarik', kenar: .4, adim: st.t * .8 });
} }), { over: etk('NARHIN ÜSTÜNDE SATANA: MÜSADERE VE SÜRGÜN') });
PL('P067', 'G08', 'NAR', 'yakin', st => ({ cam: camLerp(CAM(620, 380, 1.6), CAM(700, 460, 1.4), st.p), bg: [.2, 0, 0], ciz: () => narhDefteri(st) }),
  { over: (ctx, st) => { const k = W_(st, 'G08', 'üç'); buyukYazi('≈ 300 YEVMİYE', { y: 800, px: 84, t0: k })(ctx, st); } });
PL('P068', 'G09', 'NAR', 'ayrinti', st => { const k = W_(st, 'G09', 'dört'); return { cam: camLerp(CAM(700, 420, 1.5), CAM(700, 420, 1.6), st.p), bg: [.2, 0, 0], ciz: () => {
  narhDefteri(st, { baslik: 'Narh fermanı sureti · Muharrem 1140 (Ağustos 1727)', liste: [['Nîze-i rummânî', ''], ['Sâhib-kırân', '150 kuruş'], ['Gül-rîz', '100 kuruş']] });
  YAZI.ekle('50', 860, 306, { font: 'serif', px: 34, align: 'right', a: 1 - clamp((st.lt - k) / .3) });
  if (st.lt > k) { GR.fill(SET.R(800, 292, 70, 3), GR.tone(.1), { th: 0, id: 9 }); YAZI.ekle('200 kuruş', 940, 306, { font: 'serif', px: 38, align: 'right', renk: [130, 20, 20], a: clamp((st.lt - k) / .4) }); }
} }; }, { over: etk('BİR YIL SONRA · 1727') });

// ═════════ 7. 1730 ═════════
PL('P070', 'H01', 'CAD', 'genis', st => ({ cam: camLerp(CAM(960, 540, 1), CAM(1040, 540, 1.1), st.p), bg: [.8, 0, 10], ciz: () => SET2.cadirlar(st.t) }),
  { over: both(kartOver('H01'), etk('ÜSKÜDAR · EYLÜL 1730', { t0: 3.4 })) });
PL('P071', 'H02', 'BEY', 'orta', st => ({ cam: camLerp(CAM(960, 620, 1.1), CAM(960, 640, 1.0), st.p), bg: [.3, 0, 0], ciz: () => {
  SET2.carsi(st.t); SET2.kalabalik(st.t, { n: 4 + Math.floor(clamp(st.lt / st.d) * 12), mesale: 0 });
} }), { over: etk('BEYAZIT · 28 EYLÜL 1730') });
PL('P072', 'H03', 'SAR', 'genis', st => { const k = W_(st, 'H03', 'ekimin'); return { cam: camLerp(CAM(960, 560, 1), CAM(960, 520, 1.12), st.p), bg: [.05, 0, 1], ciz: () => SET2.sarayKapi(st.t, { kandil: 1 - clamp((st.lt - k - 1.2) / 1.4) }) }; },
  { over: (ctx, st) => { const k = W_(st, 'H03', 'ekimin'); etiket(ctx, '1 EKİM 1730', 150, 120, st.lt - k, st.d - k); } });
PL('P073', 'H04', 'SED', 'orta', st => ({ cam: camLerp(CAM(960, 600, 1.1), CAM(960, 620, 1.18), st.p), bg: [.12, 0, 0], ciz: () => {
  SET2.sedir(st.t); SET2.osmanli({ x: 1300 + st.lt * 60, y: 1040, h: 600, yon: 1, arka: true, kenar: .5, adim: st.t * .6 });
} }), { over: etk('2 EKİM 1730 · TAHT I. MAHMUD\'A') });
PL('P074', 'H05', 'KAG', 'genis', st => ({ cam: camLerp(CAM(960, 600, 1), CAM(960, 620, 1.08), st.p), bg: [.08, 0, 1], renk: 1 - io(st.lt / Math.max(1.5, st.d - .5)), ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.07), { th: -.05, id: 1 });
  SET.kosk(560, 700, 800, 300 * (1 - .35 * io(st.lt / st.d)), { gece: true });
  GR.fill(SET.R(-200, 760, 2400, 500), GR.tone(.12), { type: 'persp', y0: 760, D: 200, p0: 7, p1: 14, id: 8 });
  for (let r = 0; r < 3; r++) for (let x = 120; x < 1850; x += 120) LALE.ciz(x + r * 40, 860 + r * 80, .6 + r * .2, { tip: 'ist', sap: 60 + r * 20, cesit: 'ist', egim: .4 * io(st.lt / st.d) * ((x / 120) % 2 ? 1 : -1) });
} }), { over: etk('KÂĞITHANE · EKİM 1730') });
PL('P075', 'H06', 'PAT', 'yakin', st => { const u = io(st.lt / st.d); return { cam: camLerp(CAM(960, 560, 1.15), CAM(960, 560, 1.25), st.p), bg: [.05, 0, 1], renk: 0, ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.05), { th: 0, id: 1 });
  GR.fill(SET.R(700, 160, 520, 720), GR.tone(.88 - .55 * u), { th: HV_, id: 10 }); GR.fill(SET.R(956, 160, 8, 720), GR.tone(.1), { th: HV_, id: 9 });
  SET2.osmanli({ x: 980, y: 1160, h: 900, yon: 1, arka: true, sapka: 'sarik', sarikTon: .3, kenar: null, kolOn: { a: .15, b: .15 } });
} }; }, { over: etk('25 KASIM 1730') });

// ═════════ 8. AD ═════════
PL('P080', 'I02', 'KRO', 'ayrinti', st => ({ cam: camLerp(CAM(960, 540, 1.05), CAM(960, 540, 1.15), st.p), bg: [.1, 0, 0], renk: 0, ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.08), { th: 0, id: 0 });
  for (let i = 0; i < 9; i++) SET2.kitap(300 + i * 150, 300, 120, 560, { ton: .12 + (i % 3) * .12 });
  SET.isik({ x: 960, y: 400, r1: 900, a: .5 });
} }), { over: both(kartOver('I02'), etk('ON SEKİZİNCİ YÜZYIL VAKAYİNAMELERİ', { t0: 3.4, px: 38 })) });
PL('P081', 'I03', 'IKD', 'orta', st => ({ cam: camLerp(CAM(960, 540, 1), CAM(960, 500, 1.12), st.p), bg: [.15, 0, 0], ciz: () => {
  SET2.masaUst(-300, { ton: .18 }); SET2.gazete(420, 100, 760, 880);
  YAZI.ekle('İKDAM', 800, 200, { font: 'baslik', px: 80, align: 'center', ls: 10 }); YAZI.ekle('1913', 800, 245, { font: 'serif', px: 30, align: 'center' });
  YAZI.ekle('Lâle Devri', 800, 320, { font: 'baslik', px: 46, align: 'center', a: clamp((st.lt - W_(st, 'I03', 'ahmed')) / .5) });
  LALE.ciz(800, 560, .9, { sap: 40, tip: 'ist', cesit: 'ist', yaprakYok: true, renk: clamp((st.lt - W_(st, 'I03', 'ahmed')) / 1.2) });
  INSAN.adam({ x: 1500, y: 1060, h: 700, yon: -1, kenar: .45, kenarYan: -1, kolOn: { a: 1.0, b: .6 }, biyik: true, sapka: 'fes' });
} }), { over: (ctx, st) => { etiket(ctx, 'ŞAİR YAHYA KEMAL', 150, 120, st.lt, W_(st, 'I03', 'ahmed')); const k = W_(st, 'I03', 'ahmed'); etiket(ctx, 'TARİHÇİ AHMED REFİK', 1770, 120, st.lt - k, st.d - k, { align: 'right' }); } });
PL('P082', 'I04', 'KIT', 'yakin', st => ({ cam: camLerp(CAM(960, 560, 1.15), CAM(960, 520, 1.25), st.p), bg: [.15, 0, 0], ciz: () => {
  SET2.masaUst(-300, { ton: .16 }); SET2.kitap(360, 160, 1200, 760, { acik: true });
  YAZI.ekle('LÂLE DEVRİ', 660, 260, { font: 'baslik', px: 40, align: 'center' }); SET2.satirlar(420, 320, 480, 8, 34);
  YAZI.ekle('500 – 1000 altın', 1260, 280, { font: 'baslik', px: 44, align: 'center' });
  LALE.ciz(1260, 640, 1.3, { sap: 140, tip: 'ist', cesit: 'ist' });
  SET2.para(1160, 840, 3 + Math.floor(clamp(st.lt / 2) * 8), .9); SET2.para(1360, 840, 3 + Math.floor(clamp(st.lt / 2) * 6), .9);
} }), { over: etk('AHMED REFİK, LÂLE DEVRİ (1915)') });
PL('P083', 'I05', 'NAR', 'orta', st => { const g = io((st.lt - 2) / 1.5); return { cam: camLerp(CAM(960, 540, 1.0), CAM(960, 540, 1.08), st.p), bg: [.2, 0, 0], ciz: () => {
  narhDefteri(st);
  SET2.para(1500, 860, Math.max(1, Math.round(14 * (1 - g) + 1)), 1.0);
} }; }, { over: both(etk('M. MÜNİR AKTEPE · TARİH DERGİSİ, 1953'), (ctx, st) => quote(ctx, '“Bu rivayetin doğruluğunu isbat edecek bir vesika da ortada yoktur.”', W / 2, 790, st.lt - 2.5, { px: 46, maxW: 1500 })) });
PL('P084', 'I06', 'DER', 'yakin', st => ({ cam: camLerp(CAM(960, 560, 1.12), CAM(960, 540, 1.22), st.p), bg: [.15, 0, 0], ciz: () => {
  SET2.masaUst(-300, { ton: .2 }); SET2.kitap(360, 160, 1200, 760, { acik: true });
  YAZI.ekle('LÂLE DEVRİ (1718–1730)', 660, 250, { font: 'baslik', px: 32, align: 'center' }); SET2.satirlar(420, 300, 480, 9, 34);
  YAZI.ekle('zevk · sefahat · isyan', 1260, 250, { font: 'italik', px: 40, align: 'center' });
  SET.kosk(1000, 640, 520, 180, {}); for (let x = 1020; x < 1520; x += 70) LALE.ciz(x, 700, .4, { sap: 30, tip: 'ist', cesit: 'ist' });
} }), { over: etk('DERS KİTAPLARINDAKİ ANLATI') });
PL('P085', 'I07', 'KTP', 'ayrinti', st => ({ cam: camLerp(CAM(960, 520, 1.1), CAM(960, 520, 1.2), st.p), bg: [.15, 0, 0], ciz: () => {
  SET2.masaUst(-300, { ton: .2 }); SET2.kitap(700, 120, 520, 760, { ton: .85 });
  YAZI.ekle('LALE DEVRİ MI?', 960, 320, { font: 'baslik', px: 52, align: 'center' }); YAZI.ekle('2025', 960, 380, { font: 'serif', px: 32, align: 'center' });
  LALE.ciz(960, 640, 1.0, { sap: 60, tip: 'ist', cesit: 'ist', yaprakYok: true });
} }), { over: (ctx, st) => { const k = W_(st, 'I07', 'lale'); quote(ctx, '“Lale Devri hiç yaşanmamıştır.”', W / 2, 790, st.lt - k + .3, { px: 64, kaynak: 'SELİM KARAHASANOĞLU (ED.), 2025' }); } });
// etiket sökülür: bahçe gündüz, üstünde "SEFAHAT ÇAĞI" levhası düşer
PL('P086', 'I08', 'KAG', 'genis', st => { const k = W_(st, 'I08', 'sonradan'); const d = io((st.lt - k) / 1.2); return { cam: camLerp(CAM(960, 560, 1), CAM(960, 580, 1.08), st.p), bg: [.9, 0, 10], ciz: () => {
  SET2.bogaz(st.t, { kx: 560, kw: 800 });
  for (let x = 100; x < 1900; x += 110) LALE.ciz(x, 1000, .8, { sap: 80, tip: 'ist', cesit: (x / 110) % 2 ? 'ist' : 'istSari' });
  GR.save(); GR.frame(960, 180 + d * 900, d * .6, 1, 1); SET2.sayfa(-300, -60, 600, 120, { ton: .95 }); GR.restore();
  YAZI.ekle('SEFAHAT ÇAĞI', 960, 200 + d * 900, { font: 'baslik', px: 56, align: 'center', a: 1 - d });
} }; });

// ═════════ 9. SON ═════════
PL('P090', 'J02', 'KIT', 'orta', st => ({ cam: camLerp(CAM(960, 540, 1), CAM(960, 540, 1.1), st.p), bg: [.15, 0, 0], ciz: () => {
  SET2.masaUst(-300, { ton: .18 });
  SET2.kitap(160, 180, 760, 620, { acik: true }); SET2.kitap(1000, 180, 760, 620, { acik: true });
  YAZI.ekle('MACKAY · 1841', 540, 260, { font: 'baslik', px: 34, align: 'center' }); YAZI.ekle('AHMED REFİK · 1915', 1380, 260, { font: 'baslik', px: 34, align: 'center' });
  const r = io((st.lt - 1) / 2);
  LALE.ciz(540, 640, 1.3, { sap: 120, cesit: 'semper', renk: r }); LALE.ciz(1380, 640, 1.3, { sap: 120, tip: 'ist', cesit: 'ist', renk: r });
} }), { over: (ctx, st) => { etiket(ctx, 'İKİ ÇILGINLIK · İKİ KİTAP', W / 2, 860, st.lt - 1, st.d - 1, { align: 'center' }); } });
PL('P091', 'J03', 'ODA', 'yakin', st => ({ cam: camLerp(CAM(960, 660, 1.4), CAM(960, 640, 1.5), st.p), bg: [.08, 0, 0], ciz: () => {
  SET2.arkaOda(st.t);
  INSAN.adam({ x: 620, y: 1000, h: 640, yon: 1, sapka: 'genis', yaka: 'duz', kenar: .5, kolOn: { a: .6 + Math.sin(st.t * 2) * .2, b: 1.0 } });
  INSAN.adam({ x: 1330, y: 1000, h: 620, yon: -1, sapka: 'genis', yaka: 'duz', kenar: .5, kenarYan: -1, kolOn: { a: .5 + Math.sin(st.t * 2 + 1) * .2, b: 1.1 } });
} }));
PL('P092', 'J04', 'TER', 'orta', st => ({ cam: camLerp(CAM(960, 600, 1.08), CAM(960, 560, 1.0), st.p), bg: [.7, 0, 10],
  ciz: () => { GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.82), { th: 0, id: 10 }); terazi(st, Math.sin(st.t * 1.5) * .06); } }));
PL('P093', 'J05', 'SOZ', 'yakin', st => ({ cam: camLerp(CAM(960, 540, 1.0), CAM(960, 540, 1.5), io(st.lt / Math.max(2, st.d))), bg: [.2, 0, 0], ciz: () => {
  SET2.masaUst(-300, { ton: .14 }); SET2.sayfa(700, 280, 520, 520, { ton: .95 });
  YAZI.ekle('herkes alıyor', 960, 400, { font: 'el', px: 46, align: 'center' }); LALE.ciz(960, 660, 1.1, { sap: 60, cesit: 'semper' });
} }));
PL('P094', 'J06', 'SON', 'genis', st => ({ cam: camLerp(CAM(960, 560, 1.05), CAM(960, 600, 1.0), st.p), bg: [.9, 0, 10], ciz: () => {
  SET.gok({ gun: 1, ufuk: 566 }); SET.kasaba(566, 1); SET.degirmen(1560, 566, .7, st.t * .35); SET.tarla({ y0: 566, t: st.t, sira: 7 });
} }));
// bitiş ekranı: sol yarıda tarla ve başlık, sağ yarı boş (YouTube öğeleri)
PL('P095', 'J06@ekranda', 'SON', 'orta', st => ({ cam: CAM(960, 540, 1), bg: [.12, 0, 0], ciz: () => {
  GR.fill(SET.R(-200, -200, 2400, 1500), GR.tone(.1), { th: 0, id: 0 });
  GR.fill(SET.R(80, 140, 760, 800), GR.tone(.92), { th: -.02, id: 10 });
  for (let r = 0; r < 4; r++) for (let x = 140; x < 800; x += 110) LALE.ciz(x + (r % 2) * 50, 620 + r * 90, .55 + r * .15, { sap: 60, cesit: ['semper', 'viceroy', 'switsers', 'amiral'][(r + x / 110) % 4 | 0], egim: Math.sin(st.t + x) * .03 });
} }), { over: (ctx, st) => { txt(ctx, 'ZAMAN KURYESİ', 460, 230, { px: 54, ls: 8, col: `rgb(${GR.INK})` }); txt(ctx, 'Lale Çılgınlığı', 460, 300, { px: 40, font: FONT.alinti(44), col: `rgb(${GR.INK})` }); } });

function initScenes() {
  for (const p of PLANS) window.PLAN[p.id] = { at: p.at, set: p.set, olcek: p.olcek };
  for (const p of PLANS) plan(p.id, (ctx, st) => sahne(ctx, st, p), { tr: p.o.tr, over: p.o.over });
  window.DUR = window.DUR || (Object.values(window.CUES).reduce((m, c) => Math.max(m, c.e), 0) + 15);
}
