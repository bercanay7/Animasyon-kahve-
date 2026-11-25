// Kanca + I. Yazı tura (A01–B10). Bodrum yalnız monitörde (mod video); belgeler kâğıtta. Gözlemciler III. bölüme kadar görünmez (yalnız el, ses, levha).
'use strict';
const VID = { baski: { mod: 'video' } }, KAG = { baski: { mod: 'kagit' } };
const NUM = ['2093', '5704', '1037', '7258', '3401', '5486', '819', '4325', '8612'];
// bodrum koridoru + kişiler. o.sayim: soldaki duvarda dizilmiş mahkûmlar · o.gardiyanlar: [{z,u,f,kol}] · o.kose: kenarda duran gardiyan (kahraman)
function bodrum(B, st, o = {}) {
  const t = st.t;
  const K = D.koridor(B, t, { vp: o.vp, gen: o.gen, isik: o.isik ?? (1 - .05 * (Math.sin(t * 37) > .97 ? 1 : 0)), no: (y, i) => null, kapiYok: o.kapiYok, acik: o.acik, levha: o.levha });
  const kisi = (z, u, tip, oo = {}) => { const p = K.yer(z, u), s = K.olc(z); return FIG.kisi(B.l, p[0], p[1], 700 * s, { tip, ...oo }); };
  if (o.sayim) for (let i = 0; i < o.sayim; i++) { const z = .2 + i * .085; kisi(z, -.72, 'mahkum', { f: 1, numara: NUM[i % NUM.length], kolO: [-.05, .1], kolA: [-.08, .1], bas: Math.sin(t * .7 + i) * .03 + (o.basEgik || 0) }); }
  for (const g of (o.gardiyanlar || [])) kisi(g.z, g.u, 'gardiyan', { f: g.f ?? -1, kolO: g.kol || [.15 + Math.sin(t * 1.3 + g.z * 9) * .08, .5], kolA: [-.1, .3], bas: g.bas || 0, govde: g.govde || 0 });
  if (o.kose) kisi(o.kose.z ?? .62, o.kose.u ?? .78, 'gardiyan', { f: -1, kolO: [-.08, .1], kolA: [-.1, .12], bas: .12 + Math.sin(t * .5) * .02 });
  return K;
}
// büyük baş-omuz (yakın plan): profil figür, baş kadraj içinde. tip, f, x, y (baş merkezi), s (boy px)
function yakinFig(B, tip, x, y, boy, o = {}) { return FIG.kisi(B.l, x, y + boy * .96, boy, { tip, f: o.f ?? 1, kolO: o.kolO || [.1, .3], kolA: o.kolA || [-.1, .2], bas: o.bas || 0, ...o }); }

// P01 sayım: mahkûmlar solda dizili, iki gardiyan sayıyor, biri sağ köşede hiçbir şey yapmadan duruyor; yavaş yaklaşma köşeye
sahne('P01', 'A01', 'koridor', 'genis', (B, st) => {
  B.cam(lerp(960, 1180, E.io2(clamp(st.lt / 9))), lerp(560, 600, clamp(st.lt / 9)), 1 + .25 * E.io2(clamp(st.lt / 9)));
  bodrum(B, st, { sayim: 6, gardiyanlar: [{ z: .3, u: .1, kol: [.9 + Math.sin(st.t * 2) * .15, .9] }, { z: .45, u: .25 }], kose: { z: .55, u: .8 } });
}, VID);
// P02 yakın: köşedeki gardiyan, aynalı gözlükte koridorun ışığı; baş hafif öne
sahne('P02', 'A01@gardiyanlardan', 'kose', 'yakin', (B, st) => {
  B.cam(960, 540, 1.02 + st.lt * .015);
  const k = B.k; k.save(); k.fillStyle = B.ton(.45); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.82); k.fillRect(200, -300, 260, 1700); k.restore();   // arkada hücre kapısı
  yakinFig(B, 'gardiyan', 1060, 330, 2300, { f: -1, bas: .1 + Math.sin(st.t * .8) * .02, parilti: '#FFFFFF' });
}, VID);
// P03 ayrıntı: yazı tura (dönen para düşüyor, eli kapanır)
sahne('P03', 'A01@yazı', 'para', 'ayrinti', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .02);
  const k = B.k; k.save(); k.fillStyle = B.ton(.35); k.fillRect(-300, -300, 2600, 1700); k.restore();
  const u = clamp(st.lt / 2.2), y = 300 + 280 * (1 - Math.pow(2 * u - 1, 2)) * -1 + 500 * u;
  D.para(B, 960, Math.min(760, y + 120), 90, st.lt * 14);
  FIG.elYakin(B.l, 760, 900, 14, 1, false, clamp((st.lt - 2) / .4));
}, VID);
// P04 gözlükteki yansıma: gardiyanın aynalı camında sayım sırası (izleyici onun yerinde)
sahne('P04', 'A01@sen', 'gozluk', 'orta', (B, st) => {
  B.cam(960, 540, 1.1 + st.lt * .03);
  const k = B.k, l = B.l;
  k.save(); k.fillStyle = B.ton(.85); k.fillRect(-300, -300, 2600, 1700); k.restore();
  // iki cam (aynalı): içinde sıradaki mahkûmlar küçük, ters koridor
  for (const [cx, sg] of [[640, -1], [1280, 1]]) {
    const yol = g => { g.beginPath(); g.ellipse(cx, 520, 300, 220, sg * .05, 0, TAU); };
    k.save(); yol(k); k.fillStyle = B.ton(.55); k.fill(); k.clip();
    k.fillStyle = B.ton(.2); for (let i = 0; i < 5; i++) { const x = cx - 220 + i * 110 + Math.sin(st.t * .5) * 10; k.fillRect(x, 470, 34, 160); k.beginPath(); k.arc(x + 17, 450, 22, 0, TAU); k.fill(); }
    k.restore();
    l.save(); l.lineWidth = 26; yol(l); l.strokeStyle = '#000'; l.stroke(); l.restore();
    k.save(); yol(k); k.clip(); k.fillStyle = B.ton(.0); k.globalAlpha = .7; k.beginPath(); k.ellipse(cx - 90, 420 + Math.sin(st.t) * 8, 90, 26, -.4, 0, TAU); k.fill(); k.restore();   // parıltı
  }
  l.save(); l.fillStyle = '#000'; l.fillRect(930, 470, 60, 26); l.fillRect(-100, 480, 440, 22); l.fillRect(1580, 480, 440, 22); l.restore();
}, VID);
// P05 kapak B: karanlıkta makaralı teyp; makaralar dönmeye başlar, kırmızı kayıt lambası yanar (gözlemci yok)
sahne('P05', 'A02', 'teyp', 'genis', (B, st) => {
  B.cam(960, 520, 1 + st.lt * .02);
  const k = B.k; k.save(); k.fillStyle = B.ton(.88); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.7); k.fillRect(-300, 760, 2600, 900); k.restore();
  const on = clamp((st.lt - .4) / 1.2);
  SET.teyp(B, 960, 300, 1.25, st.lt, { hz: .45 * on, kayit: on, vuIsik: .3 + .55 * on });
}, { ...KAG, over: ETK('AĞUSTOS 1971 · STANFORD ÜNİVERSİTESİ', 960, 150, { d: 4.5 }) });
// P06 ayrıntı: dökümün ilk satırı; konuşanlar yalnız "SORU" ve "ERKEK SES", sözler kapalı
sahne('P06', 'A02@karşısına', 'dokum', 'kart', (B, st) => {
  B.cam(960, 520, 1.04 + st.lt * .02);
  SET.belge(B, 'STANFORD ARŞİVİ · SC0750 · BANT A', ['SORU: ████████ ██ ████ ██████ ███', '      ██████ ███ ████████ ███?', '', 'ERKEK SES: ███ ███████ ███', '', 'SORU: ████ ███████ ██ ██ ████ ████'], .3 + st.lt / 6, { px: 40 });
}, KAG);
// P07 koridor, boş; ışık titrer: "kendiliğinden mi, biri mi?"
sahne('P07', 'A03', 'koridor', 'genis', (B, st) => {
  B.cam(960, 520, 1.05 + st.lt * .02);
  bodrum(B, st, { gardiyanlar: [{ z: .35, u: -.2, f: 1, kol: [.1, .4] }], isik: 1 - .35 * (Math.sin(st.t * 23) > .9 ? 1 : 0) });
}, VID);
// P08 ayrıntı: makara (bant yaklaşır), ses göstergesi
sahne('P08', 'A03@iz', 'teyp', 'ayrinti', (B, st) => {
  B.cam(820, 420, 2.2 + st.lt * .04);
  const k = B.k; k.save(); k.fillStyle = B.ton(.88); k.fillRect(-300, -300, 2600, 1700); k.restore();
  SET.teyp(B, 960, 300, 1.25, st.t, { hz: .45 });
}, KAG);

// ── I. Yazı tura ──
// P09 ilan (kâğıt): gazete ilanı daktiloyla
sahne('P09', 'B01', 'ilan', 'kart', (B, st) => {
  B.cam(960, 470, 1 + st.lt * .015);
  SET.belge(B, 'İLAN · 1971 YAZI', ['Erkek üniversite öğrencileri aranıyor:', 'hapishane hayatı üzerine', 'psikoloji araştırması.', '', 'Günde 15 dolar · 1-2 hafta'], st.lt / 3.5, { px: 46, vurgu: [4], vurguA: ramp(st.t, A('B01@günde'), A('B01@günde') + .6, E.lin) });
}, { ...KAG, over: KU('İlan metni: Stanford Magazine, 2011 (çevirisi bizim)') });
// P10 yirmi dört siluet; yazı tura: yarısının gözünde gözlük parlıyor
sahne('P10', 'B02', 'secim', 'genis', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .012);
  const k = B.k; k.save(); k.fillStyle = B.ton(.2); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.4); k.fillRect(-300, 820, 2600, 600); k.restore();
  const ay = ramp(st.t, A('B02@yazı'), A('B02@yazı') + 2.2);
  for (let i = 0; i < 24; i++) {
    const sira = Math.floor(i / 12), j = i % 12, gard = (i * 7 + 3) % 2 === 0;
    const x0 = 180 + j * 140 + sira * 70, x1 = gard ? 120 + (j % 6) * 130 + sira * 60 : 1100 + (j % 6) * 130 + sira * 60;
    const x = lerp(x0, x1, ay), y = 820 - sira * 70 + (sira ? 0 : 0);
    FIG.kisi(B.l, x, y + (sira ? -10 : 40), sira ? 300 : 340, { tip: ay > .5 ? (gard ? 'gardiyan' : 'mahkum') : 'takim', f: gard ? 1 : -1, gozluk: ay > .5, renk: sira ? '#3a3a3a' : '#000', kolO: [-.05, .12], kolA: [-.08, .1], onlukRenk: '#9a9a94', zincir: false });
  }
}, { ...VID, over: OV(ETK('GARDİYAN', 520, 240, { video: 1, t0: 3, d: 6 }), ETK('MAHKÛM', 1450, 240, { video: 1, t0: 3, d: 6 })) });
// P11 yazı tahtası: Zimbardo'nun eli tebeşirle yazıyor (yüz yok)
sahne('P11', 'B03', 'tahta', 'orta', (B, st) => {
  B.cam(960, 470, 1 + st.lt * .012);
  const T0 = SET.tahta(B, ['GARDİYAN YÖNLENDİRMESİ', 'CUMARTESİ 14 AĞUSTOS 1971'], clamp(st.lt / 3), { px: 60 });
  const p = clamp(st.lt / 3), ex = 330 + 900 * p, ey = 230 + (p > .5 ? 110 : 0);
  FIG.elYakin(B.l, ex + 40, ey + 40, 10, -1, false, .6);
}, KAG);
// P12 yakın: tahtadaki sözcükler (B04 alıntısıyla)
sahne('P12', 'B04', 'tahta', 'yakin', (B, st) => {
  B.cam(960, 470, 1.08 + st.lt * .01);
  const sat = ['CAN SIKINTISI', 'BUNALMA', 'KORKU', 'GÜÇ: BİZDE. ONLARDA YOK.'];
  const p = [A('B04@can'), A('B04@bunalma'), A('B04@korku'), A('B04@güç')];
  const n = p.filter(x => st.t > x).length, son = p[Math.max(0, n - 1)];
  const ilerle = n ? (n - 1 + clamp((st.t - son) / 1.2)) / sat.length : 0;
  SET.tahta(B, sat, ilerle, { px: 74, lh: 130, y: 110 });
}, { ...KAG, over: OV(KU('Zimbardo, gardiyan yönlendirmesi, 14 Ağustos 1971 (Stanford Üniv. arşivi, "Tape 2")')) });
// P13 ayrıntı: cop masaya bırakılır, tebeşir "VURMAK YOK" altını çizer
sahne('P13', 'B05', 'tahta', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.15 + st.lt * .02);
  SET.tahta(B, ['VURMAK YOK'], clamp(st.lt / 1.2), { px: 120, y: 200, h: 420, lh: 140 });
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 10; l.beginPath(); l.moveTo(330, 470); l.lineTo(330 + 900 * clamp((st.lt - 1.2) / .8), 470); l.stroke(); l.restore();
}, KAG);
// P14 Pazar sabahı: polis arabası, ev, öğrenci arabaya yaslanır (KRON televizyon görüntüsü gibi: video)
sahne('P14', 'B06', 'sokak', 'genis', (B, st) => {
  B.cam(960 + st.lt * 10, 560, 1 + st.lt * .01);
  const k = B.k; k.save(); k.fillStyle = B.ton(.08); k.fillRect(-300, -300, 2600, 1000); k.fillStyle = B.ton(.45); k.fillRect(-300, 820, 2600, 600); k.restore();
  SET.ev(B, 120, 820, 1.2);
  SET.polisArabasi(B, 1300, 900, 1.2, { lamba: .5 + .5 * Math.sin(st.t * 8) });
  // öğrenci eller arabanın tavanında; polis arkasında
  FIG.kisi(B.l, 1040, 900, 400, { tip: 'takim', f: 1, govde: .35, kolO: [1.9, .1], kolA: [1.7, .2], bas: .1, serbest: 1 });
  FIG.kisi(B.l, 860 + Math.sin(st.t * .8) * 6, 905, 420, { tip: 'takim', f: 1, kolO: [1.1, .8], kolA: [.6, .9], sac: 'kasket' });
}, { ...VID, over: KU('Palo Alto, Pazar 15 Ağustos 1971 sabahı', { video: 1 }) });
// P15 ayrıntı: kelepçe kapanır (bileklerin yakın planı)
sahne('P15', 'B06@kelepçe', 'sokak', 'ayrinti', (B, st) => {
  B.cam(960, 540, 1.05 + st.lt * .03);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.3); k.fillRect(-300, -300, 2600, 1700); k.restore();
  const p = clamp(st.lt / .8);
  for (const [x, a] of [[760, .12], [1160, -.12]]) { l.save(); l.translate(x, 560); l.rotate(a); l.fillStyle = '#000'; l.fillRect(-420 * (x < 900 ? 1 : -1) - (x < 900 ? 0 : 0), -60, x < 900 ? 420 : -420, 120); l.restore(); }
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 16; for (const x of [800, 1120]) { l.beginPath(); l.arc(x, 560, 95, -PI * .5, -PI * .5 + TAU * (.55 + .45 * p)); l.stroke(); } l.lineWidth = 12; l.beginPath(); l.moveTo(895, 560); l.lineTo(1025, 560); l.stroke(); l.restore();
}, VID);
// P16 gözleri bağlı mahkûm koridorda götürülüyor (yürüyüş): gardiyan kolundan tutmuş
sahne('P16', 'B07', 'koridor', 'orta', (B, st) => {
  B.cam(960, 560, 1.1 + st.lt * .01);
  const K = bodrum(B, st, { levha: false });
  const t = st.lt, x0 = 380;
  const m = SET.yuru(B.l, x0, 1010, 620, t, { tip: 'mahkum', f: 1, numara: '', kolO: [.2, .2], kolA: [.1, .2], bas: .12 });
  const l = B.l; l.save(); l.fillStyle = '#5a5a5a'; l.fillRect(m.bas[0] - 30, m.bas[1] - 18, 64, 18); l.restore();   // göz bağı (açık ton şerit; başın yanında açık bohça değil, gözün üstünde)
  SET.yuru(B.l, x0 - 160, 1012, 660, t, { tip: 'gardiyan', f: 1, kolO: [1.2, .3], kolA: [.2, .3] });
}, { ...VID, mb: 4 });
// P17 ayrıntı: önlüğe numara basılır
sahne('P17', 'B07@bundan', 'numara', 'ayrinti', (B, st) => {
  B.cam(960, 540, 1.05 + st.lt * .02);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.25); k.fillRect(-300, -300, 2600, 1700); k.restore();
  l.save(); l.fillStyle = '#000'; l.fillRect(-300, -300, 2600, 1700); l.fillStyle = '#B8B8B2'; l.beginPath(); l.moveTo(560, -100); l.lineTo(1360, -100); l.lineTo(1460, 1200); l.lineTo(460, 1200); l.closePath(); l.fill();
  l.fillStyle = '#000'; l.font = '700 300px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; const s = '2093', n = Math.floor(clamp(st.lt / .7) * 4 + .001); l.fillText(s.slice(0, n), 960, 560); l.restore();
}, VID);
// P18 gardiyan gözlüğü takar: yakın, parıltı
sahne('P18', 'B08', 'kose', 'yakin', (B, st) => {
  B.cam(960, 540, 1.02 + st.lt * .015);
  const k = B.k; k.save(); k.fillStyle = B.ton(.5); k.fillRect(-300, -300, 2600, 1700); k.restore();
  const p = ramp(st.t, A('B08@aynalı') - .4, A('B08@aynalı') + .5);
  yakinFig(B, 'gardiyan', 900, 330, 2300, { f: 1, gozluk: p > .6, bas: -.02, kolO: [lerp(.2, 2.3, Math.sin(p * PI)), lerp(.3, 1.4, Math.sin(p * PI))], serbest: 1 });
}, VID);
// P19 koridorun ucu: iki kapı, "SUPERINTENDENT" ve "WARDEN" levhaları
sahne('P19', 'B09', 'koridor', 'genis', (B, st) => {
  B.cam(960, 470, 1 + st.lt * .02);
  bodrum(B, st, { levha: false, sonD: .7 });
  const l = B.l, k = B.k;
  for (const [x, ad] of [[820, 'SUPERINTENDENT'], [1100, 'WARDEN']]) {
    k.save(); k.fillStyle = B.ton(.75); k.fillRect(x - 70, 350, 140, 240); k.fillStyle = B.ton(.02); k.fillRect(x - 64, 330, 128, 22); k.restore();
    l.save(); l.lineWidth = 3; l.strokeStyle = '#000'; l.strokeRect(x - 70, 350, 140, 240); l.strokeRect(x - 64, 330, 128, 22); l.font = '700 14px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillStyle = '#000'; l.fillText(ad, x, 341); l.restore();
  }
}, { ...VID, over: OV(ETK('AMİR', 820, 270, { video: 1, t0: 1.2, d: 9 }), ETK('MÜDÜR · DAVID JAFFE', 1180, 640, { video: 1, t0: 4, d: 6 })) });
// P20 kayıt: kâğıt dünyada boş masa, monitörler ve teyp (kimse yok)
sahne('P20', 'B10', 'gozlem', 'orta', (B, st) => {
  B.cam(960, 520, 1.03 + st.lt * .012);
  SET.oda(B, { masa: 780 });
  SET.monitorIci(B, 160, 170, 620, 440, (B2) => bodrum(B2, st, { sayim: 4, gardiyanlar: [{ z: .35, u: .2 }] }));
  SET.monitorIci(B, 860, 230, 420, 300, (B2) => bodrum(B2, st, { vp: [700, 470], gardiyanlar: [{ z: .5, u: -.3, f: 1 }] }));
  SET.teyp(B, 1560, 420, .7, st.t);
}, { ...KAG, over: ETK('GÖZLEM MASASI', 960, 120, { t0: .5, d: 5 }) });
