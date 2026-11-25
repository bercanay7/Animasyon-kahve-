// Kanca + I. Yazı tura (A01–B10). Bodrum yalnız monitörde (mod video); belgeler kâğıtta. Gözlemciler III. bölüme kadar görünmez (yalnız el, ses, levha).
'use strict';
const VID = { baski: { mod: 'video' } }, KAG = { baski: { mod: 'kagit' } };
const NUM = ['2093', '5704', '1037', '7258', '3401', '5486', '819', '4325', '8612'];
// bodrum koridoru + kişiler (kanal dersleri §3: sıra düzensiz; boy, aralık, poz farklı; gardiyan sıranın karşısında dikilmez, sayım tahtasıyla yürür)
// o.sayim: soldaki duvarda mahkûm sayısı · o.sayan: {z, x0, v} yürüyerek sayan gardiyan (yanal) · o.gardiyanlar: [{z,u,f,kol}] · o.kose: dışarıda oturan gardiyan (kahraman) {z,u}
const BODRUM_GAIT = HAREKET.yuruyus({ tip: 'yuru' });
function bodrum(B, st, o = {}) {
  const t = st.t;
  const K = D.koridor(B, t, { vp: o.vp, gen: o.gen, isik: o.isik ?? (1 - .05 * (Math.sin(t * 37) > .97 ? 1 : 0)), no: (y, i) => null, kapiYok: o.kapiYok, acik: o.acik, levha: o.levha });
  const kisi = (z, u, tip, oo = {}) => { const p = K.yer(z, u), s = K.olc(z); return FIG.kisi(B.l, p[0], p[1], 700 * s * (oo.boyK || 1), { tip, ...oo }); };
  if (o.sayim) { const r = rng(17); for (let i = 0; i < o.sayim; i++) { const z = .18 + i * .088 + (r() - .5) * .05, u = -.74 + (r() - .5) * .12, poz = r();
    kisi(z, u, 'mahkum', { f: 1, boyK: .9 + r() * .18, numara: NUM[i % NUM.length], kolO: poz < .4 ? [-.05, .1] : poz < .7 ? [.25, .9] : [-.2, .35], kolA: [-.08 + r() * .2, .1 + r() * .4], bas: (r() - .5) * .14 + Math.sin(t * .7 + i) * .03 + (o.basEgik || 0), govde: (r() - .5) * .08 }); } }
  if (o.sayan) { const g = o.sayan, z = g.z ?? .32, s = K.olc(z), p0 = K.yer(z, 0), x = (g.x0 ?? 620) + (g.v ?? 40) * st.lt, fz = BODRUM_GAIT.poz(st.lt * (g.v ?? 40) / (BODRUM_GAIT.hiz * 7.35 * s) / BODRUM_GAIT.tur, 1);
    FIG.kisi(B.l, x, p0[1], 700 * s, { tip: 'gardiyan', f: (g.v ?? 40) >= 0 ? 1 : -1, bacak: fz, cop: false, kolO: [.95, 1.05], kolA: [-.1, .3], bas: .12,
      el: { on: (gg, e) => { gg.save(); gg.translate(e.e[0], e.e[1]); gg.rotate(-.3); gg.fillRect(-2, -9, 11, 14); gg.restore(); } } }); }   // sayım tahtası (çizgi plakasında koyu)
  for (const g of (o.gardiyanlar || [])) kisi(g.z, g.u, 'gardiyan', { f: g.f ?? -1, kolO: g.kol || [.15 + Math.sin(t * 1.3 + g.z * 9) * .08, .5], kolA: [-.1, .3], bas: g.bas || 0, govde: g.govde || 0 });
  if (o.kose) { const z = o.kose.z ?? .5, u = o.kose.u ?? .86, p = K.yer(z, u), s = K.olc(z);
    FIG.kisi(B.l, p[0], p[1], 700 * s, { tip: 'gardiyan', f: -1, bacak: 'otur', sandalye: true, kolO: [.55, .9], kolA: [.4, .9], bas: .1 + Math.sin(t * .5) * .02 }); }
  return K;
}
// büyük baş-omuz (yakın plan): profil figür, baş kadraj içinde. tip, f, x, y (baş merkezi), s (boy px)
function yakinFig(B, tip, x, y, boy, o = {}) { return FIG.kisi(B.l, x, y + boy * .96, boy, { tip, f: o.f ?? 1, kolO: o.kolO || [.1, .3], kolA: o.kolA || [-.1, .2], bas: o.bas || 0, ...o }); }

// P01 sayım: mahkûmlar solda düzensiz dizili, bir gardiyan sayım tahtasıyla yürüyerek sayıyor; kahraman koridorun ucunda kapının dışında oturuyor; yaklaşma ona
sahne('P01', 'A01', 'koridor', 'genis', (B, st) => {
  const p = E.io2(clamp(st.lt / 7));
  B.cam(lerp(960, 1200, p), lerp(560, 560, p), 1 + .3 * p);
  bodrum(B, st, { sayim: 6, sayan: { z: .3, x0: 560, v: 34 }, kose: { z: .5, u: .86 } });
}, VID);
// P01T ayrıntı (≈3 sn, ilk 5 sn'de kapak B'nin nesnesi): karanlıkta teyp, makara döner, kırmızı lamba yanar; insan, yazı, bant içeriği yok
sahne('P01T', 'A01@dizilmiş', 'teyp', 'ayrinti', (B, st) => {
  B.cam(870, 430, 2.1 + st.lt * .05);
  SET.karanlik(B, .86); SET.koni(B, 960, -100, 140, 900, 700, { a: .6, tohum: 2 });
  SET.teyp(B, 960, 300, 1.25, st.t, { hz: .5, kayit: clamp(st.lt / .3) });
}, { baski: { mod: 'kagit', kuru: .5 } });
// P02 yakın: aynı oturan gardiyan, arkada kapı kenarı ve koridor ışığı; aynalı gözlükte ışık
sahne('P02', 'A01@gardiyanlardan', 'kose', 'yakin', (B, st) => {
  B.cam(960, 540, 1.02 + st.lt * .015);
  const k = B.k; k.save(); k.fillStyle = B.ton(.45); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.08); k.fillRect(1380, -300, 900, 1700); k.fillStyle = B.ton(.82); k.fillRect(1330, -300, 60, 1700); k.restore();   // sağda açık kapı aralığı ve koridor ışığı
  FIG.kisi(B.l, 860, 1460, 1500, { tip: 'gardiyan', f: 1, bacak: 'otur', sandalye: true, kolO: [.55, .9], kolA: [.4, .9], bas: .12 + Math.sin(st.t * .8) * .02, parilti: '#FFFFFF' });
}, VID);
// P03 ayrıntı: "rastgele": askıda bir gardiyan gömleği ve bir mahkûm önlüğü yan yana; el gömleği alır (yöntem iddiası yok)
sahne('P03', 'A01@rastgele', 'askı', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.04 + st.lt * .03);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.3); k.fillRect(-300, -300, 2600, 1700); k.restore();
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 8; l.beginPath(); l.moveTo(200, 230); l.lineTo(1720, 230); l.stroke(); l.restore();
  const al = ramp(st.lt, .6, 1.6);
  const giysi = (x, y, ton, gomlek) => { k.save(); k.fillStyle = B.ton(ton); k.beginPath(); k.moveTo(x - 60, y); k.quadraticCurveTo(x, y - 30, x + 60, y); k.lineTo(x + 210, y + 80); k.lineTo(x + 170, y + 170); k.lineTo(x + 130, y + 130); k.lineTo(x + 140, y + (gomlek ? 420 : 560)); k.lineTo(x - 140, y + (gomlek ? 420 : 560)); k.lineTo(x - 130, y + 130); k.lineTo(x - 170, y + 170); k.lineTo(x - 210, y + 80); k.closePath(); k.fill(); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 5; l.beginPath(); l.moveTo(x, y - 50); l.lineTo(x, y - 10); l.arc(x, y - 66, 16, PI * .5, PI * 2.2); l.stroke(); l.restore(); };
  giysi(700, 300 - al * 120, .7, true); giysi(1220, 300, .25, false);
  l.save(); l.font = '700 90px "Courier Prime"'; l.textAlign = 'center'; l.fillStyle = '#000'; l.fillText('2093', 1220, 560); l.restore();
  FIG.elYakin(B.l, 700, 250 - al * 120, 12, 1, false, .8);
}, VID);
// P04 gözlükteki yansıma: aynalı camda koridorun ışığı ve bulanık, üst üste binen kalabalık lekesi (eşit aralıklı dizi yok)
sahne('P04', 'A01@sen', 'gozluk', 'orta', (B, st) => {
  B.cam(960, 540, 1.1 + st.lt * .03);
  const k = B.k, l = B.l;
  k.save(); k.fillStyle = B.ton(.85); k.fillRect(-300, -300, 2600, 1700); k.restore();
  for (const [cx, sg] of [[640, -1], [1280, 1]]) {
    const yol = g => { g.beginPath(); g.ellipse(cx, 520, 300, 220, sg * .05, 0, TAU); };
    k.save(); yol(k); k.fillStyle = B.ton(.55); k.fill(); k.clip();
    k.fillStyle = B.ton(.05); for (let i = 0; i < 4; i++) k.fillRect(cx - 260 + i * 140, 330 - i * 6, 70, 22);   // tavan lambaları (yansıma)
    const r = rng(cx); k.fillStyle = B.ton(.25); k.beginPath(); for (let i = 0; i < 9; i++) { const x = cx - 230 + r() * 460 + Math.sin(st.t * .6 + i) * 8, y = 520 + r() * 80; k.ellipse(x, y, 30 + r() * 40, 70 + r() * 50, 0, 0, TAU); } k.fill();   // bulanık kalabalık
    k.restore();
    l.save(); l.lineWidth = 26; yol(l); l.strokeStyle = '#000'; l.stroke(); l.restore();
    k.save(); yol(k); k.clip(); k.fillStyle = B.ton(.0); k.globalAlpha = .7; k.beginPath(); k.ellipse(cx - 90, 420 + Math.sin(st.t) * 8, 90, 26, -.4, 0, TAU); k.fill(); k.restore();   // parıltı
  }
  l.save(); l.fillStyle = '#000'; l.fillRect(930, 470, 60, 26); l.fillRect(-100, 480, 440, 22); l.fillRect(1580, 480, 440, 22); l.restore();
}, VID);
// P05 kapak B: karanlıkta makaralı teyp (ışık konisi); "bandı"nda VU ibresi oynar (gözlemci yok)
sahne('P05', 'A02', 'teyp', 'genis', (B, st) => {
  B.cam(960, 520, 1 + st.lt * .02);
  SET.karanlik(B, .84); SET.koni(B, 960, -120, 160, 1000, 900, { a: .8, tohum: 4 });
  const on = clamp((st.lt - .3) / 1), vb = ramp(st.t, A('A02@bandı'), A('A02@bandı') + .4);
  SET.teyp(B, 960, 330, 1.15, st.lt, { hz: .45 * on, kayit: on, vuIsik: .3 + .55 * on, vu: .3 + .5 * vb * Math.abs(Math.sin(st.t * 6)) });
}, { baski: { mod: 'kagit', kuru: .5 }, over: ETK('AĞUSTOS 1971 · STANFORD ÜNİVERSİTESİ', 960, 150, { d: 4.5 }) });
// P05S orta: "sayım sırasında dışarıda oturan": kahraman kapının dışında, içeride sayım (kapı aralığından)
sahne('P05S', 'A02@sayım', 'kose', 'orta', (B, st) => {
  B.cam(960, 560, 1.05 + st.lt * .02);
  const k = B.k; k.save(); k.fillStyle = B.ton(.5); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.12); k.fillRect(980, 140, 620, 760); k.fillStyle = B.ton(.62); k.fillRect(-300, 900, 2600, 600); k.restore();   // açık kapı (içerisi aydınlık)
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 14; l.strokeRect(980, 140, 620, 760); l.restore();
  for (let i = 0; i < 4; i++) FIG.kisi(B.k, 1060 + i * 150 + (i % 2) * 20, 880 - (i % 2) * 8, 330 + (i * 13 % 30), { tip: 'mahkum', f: 1, renk: B.ton(.55), onlukRenk: B.ton(.35), numara: '', zincir: false, kolO: [.1 + i * .1, .4], kolA: [-.1, .3] });   // içeride, uzakta, soluk
  FIG.kisi(B.l, 600, 960, 720, { tip: 'gardiyan', f: 1, bacak: 'otur', sandalye: true, kolO: [.55, .9], kolA: [.4, .9], bas: .15 + Math.sin(st.t * .6) * .02 });
}, VID);
// P06 ayrıntı: dökümün ilk satırı; konuşanlar yalnız "SORU" ve "ERKEK SES", sözler kapalı
sahne('P06', 'A02@karşısına', 'dokum', 'kart', (B, st) => {
  B.cam(960, 520, 1.04 + st.lt * .02);
  SET.belge(B, 'STANFORD ARŞİVİ · SC0750 · BANT A', ['SORU: ████████ ██ ████ ██████ ███', '      ██████ ███ ████████ ███?', '', 'ERKEK SES: ███ ███████ ███', '', 'SORU: ████ ███████ ██ ██ ████ ████'], .3 + st.lt / 6, { px: 40 });
}, KAG);
// P07 koridor, boş; ışık titrer: "kendiliğinden mi sertleşti?"
sahne('P07', 'A03', 'koridor', 'genis', (B, st) => {
  B.cam(960, 520, 1.05 + st.lt * .02);
  bodrum(B, st, { gardiyanlar: [{ z: .35, u: -.2, f: 1, kol: [.1, .4] }], isik: 1 - .35 * (Math.sin(st.t * 23) > .9 ? 1 : 0) });
}, VID);
// P08 ayrıntı: makara yakın; "son kelimesini"nde makara yavaşlar ve durur (sona saklanan)
sahne('P08', 'A03@bandın', 'teyp', 'ayrinti', (B, st) => {
  B.cam(820, 420, 2.2 + st.lt * .04);
  SET.karanlik(B, .84); SET.koni(B, 960, -120, 160, 1000, 900, { a: .8, tohum: 4 });
  const dur = A('A03@son'), w = st.t < dur ? 1 : Math.max(0, 1 - (st.t - dur) / 1.2);
  const ang = (Math.min(st.t, dur) + (st.t > dur ? (1.2 - Math.pow(Math.max(0, 1.2 - (st.t - dur)), 2) / 1.2) * .5 : 0)) * .45 * TAU;
  SET.teyp(B, 960, 300, 1.25, st.t, { ang, kayit: 1, vu: .3 * w + .05 });
}, { baski: { mod: 'kagit', kuru: .5 } });

// ── I. Yazı tura ──
// P09 ilan (kâğıt): gazete ilanı daktiloyla
sahne('P09', 'B01', 'ilan', 'kart', (B, st) => {
  B.cam(960, 470, 1 + st.lt * .015);
  SET.belge(B, 'İLAN · 1971 YAZI', ['Erkek üniversite öğrencileri aranıyor:', 'hapishane hayatı üzerine', 'psikoloji araştırması.', '', 'Günde 15 dolar · 1-2 hafta'], st.lt / 3.5, { px: 46, vurgu: [4], vurguA: ramp(st.t, A('B01@günde'), A('B01@günde') + .6, E.lin) });
}, { ...KAG, over: KU('İlan metni: Stanford Magazine, 2011 (çevirisi bizim)') });
// P10 yirmi dört öğrenci (düzensiz kalabalık; farklı boy, aralık, duruş); "yazı tura"da ikiye ayrılırlar: solda gardiyan (gözlüklü), sağda mahkûm
sahne('P10', 'B02', 'secim', 'genis', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .012);
  const k = B.k; k.save(); k.fillStyle = B.ton(.2); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.4); k.fillRect(-300, 820, 2600, 600); k.restore();
  const ay = ramp(st.t, A('B02@yazı'), A('B02@yazı') + 2.2), r = rng(24);
  const L = []; for (let i = 0; i < 24; i++) L.push({ i, gard: (i * 7 + 3) % 2 === 0, x0: 200 + r() * 1520, dy: r() * 150, boy: 280 + r() * 90, kol: r(), f: r() < .5 ? 1 : -1 });
  L.sort((a, b) => a.dy - b.dy);
  for (const o of L) {
    const sira = L.filter(q => q.gard === o.gard && q.x0 < o.x0).length;
    const x1 = o.gard ? 160 + sira * 62 + (o.i % 3) * 14 : 1060 + sira * 62 + (o.i % 3) * 14;
    const x = lerp(o.x0, x1, ay), y = 760 + o.dy * .6, uzak = o.dy < 60;
    FIG.kisi(uzak ? B.k : B.l, x, y, o.boy * (uzak ? .85 : 1), { tip: ay > .5 ? (o.gard ? 'gardiyan' : 'mahkum') : 'takim', f: ay > .5 ? (o.gard ? 1 : -1) : o.f, gozluk: ay > .5, renk: uzak ? B.ton(.6) : '#000', kolO: o.kol < .5 ? [-.05, .12] : [.3, .8], kolA: [-.08, .1 + o.kol * .3], bas: (o.kol - .5) * .12, onlukRenk: '#9a9a94', zincir: false, cop: false });
  }
}, { ...VID, over: OV(ETK('GARDİYAN', 520, 240, { video: 1, t0: 3, d: 6 }), ETK('MAHKÛM', 1450, 240, { video: 1, t0: 3, d: 6 })) });
// P11 yönlendirme: gardiyan adayları arkadan, düzensiz oturuyor; karşılarında yalnız eli görünen Zimbardo (yüz yok); el "can sıkıntısı"nda saati, "korku"da kapıyı gösterir, "güç"te kendine döner
sahne('P11', 'B03', 'sinif', 'orta', (B, st) => {
  B.cam(960, 520, 1.02 + st.lt * .012);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.35); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.82); k.fillRect(1180, 120, 520, 330); k.fillStyle = B.ton(.55); k.fillRect(-300, 760, 2600, 600); k.restore();
  SET.saat(B, 360, 220, 70, 2, 30 + st.lt * 4);
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 10; l.strokeRect(1180, 120, 520, 330); l.strokeRect(560, 180, 170, 560); l.restore();
  const r = rng(9); for (let i = 0; i < 6; i++) { const x = 220 + i * 260 + (r() - .5) * 60, y = 1080 + (i % 2) * 30;
    FIG.kisi(B.l, x, y, 640 + r() * 60, { tip: 'takim', f: 1, bacak: 'otur', sandalye: false, kolO: [.5, .9], kolA: [.4, 1], bas: .05 + (r() - .5) * .1 + Math.sin(st.t * .7 + i) * .02 }); }
  const g1 = ramp(st.t, A('B04@can') - .3, A('B04@can') + .5), g2 = ramp(st.t, A('B04@korku') - .3, A('B04@korku') + .5), g3 = ramp(st.t, A('B04@güç#1') - .3, A('B04@güç#1') + .5);
  const hx = lerp(lerp(lerp(1560, 1250, g1), 1350, g2), 1700, g3), hy = lerp(lerp(lerp(520, 300, g1), 380, g2), 540, g3);   // el tahtanın önünde kalır: saati ve kapıyı oradan gösterir (başların üstünden uzanmaz)
  FIG.elYakin(B.l, hx, hy, 9, hx < 1500 ? -1 : 1, false, .3);
}, { baski: { mod: 'kagit' }, over: KU('Zimbardo, gardiyan yönlendirmesi, 14 Ağustos 1971 (Stanford arşivi, "Tape 2"; çevirisi bizim)', { x: 1800, align: 'right', y: 90 }) });
// P12 tahta (≤ 8 sn): sözcükler sesle birlikte yazılır
sahne('P12', 'B04@bütün', 'tahta', 'yakin', (B, st) => {
  B.cam(960, 470, 1.08 + st.lt * .01);
  const sat = ['CAN SIKINTISI', 'BUNALMA', 'KORKU', 'GÜÇ: BİZDE. ONLARDA YOK.'];
  SET.tahta(B, sat, clamp(.62 + (st.t - A('B04@güç#1') + .4) / 2.2 * .38), { px: 74, lh: 130, y: 110 });
}, KAG);
// P13 ayrıntı: masaya bırakılan cop (Zimbardo'nun sonradan yazdığı yasak: vurmak yok; levha yok)
sahne('P13', 'B05', 'cop', 'ayrinti', (B, st) => {
  B.cam(960, 560, 1.1 + st.lt * .03);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.4); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.6); k.fillRect(-300, 640, 2600, 900); k.restore();
  const p = ramp(st.lt, .2, 1.1, E.out3);
  l.save(); l.translate(960, lerp(420, 650, p)); l.rotate(lerp(-.5, -.04, p)); l.fillStyle = '#000'; l.beginPath(); l.roundRect(-420, -26, 840, 52, 26); l.fill(); l.fillRect(-460, -38, 60, 76); l.restore();
  FIG.elYakin(B.l, lerp(1240, 1300, p), lerp(410, 600, p) - p * 40, 14, -1, false, 1 - p);
}, VID);
// P14 Pazar sabahı: polis arabası, ev, öğrenci arabaya yaslanır (KRON televizyon görüntüsü gibi: video)
sahne('P14', 'B06', 'sokak', 'genis', (B, st) => {
  B.cam(960 + st.lt * 10, 560, 1 + st.lt * .01);
  const k = B.k; k.save(); k.fillStyle = B.ton(.08); k.fillRect(-300, -300, 2600, 1000); k.fillStyle = B.ton(.45); k.fillRect(-300, 820, 2600, 600); k.restore();
  SET.ev(B, 120, 820, 1.2);
  SET.polisArabasi(B, 1300, 900, 1.2, { lamba: .5 + .5 * Math.sin(st.t * 8) });
  // öğrenci eller arabanın tavanında; polis arkasında
  FIG.kisi(B.l, 1040, 900, 400, { tip: 'takim', f: 1, govde: .3, kolO: [1.4, .5], kolA: [1.3, .6], bas: .1, serbest: 1 });   // eller arabanın tavanında, dirsek bükük
  FIG.kisi(B.l, 860 + Math.sin(st.t * .8) * 6, 905, 420, { tip: 'takim', f: 1, kolO: [1.1, .8], kolA: [.6, .9], sac: 'kasket' });
}, { ...VID, over: KU('Palo Alto, Pazar 15 Ağustos 1971 sabahı', { video: 1, x: 1800, align: 'right', y: 90 }) });
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
  yakinFig(B, 'gardiyan', 900, 330, 2300, { f: 1, gozluk: p > .6, bas: -.02, kolO: [lerp(.2, 1.25, Math.sin(p * PI)), lerp(.3, 1.9, Math.sin(p * PI))], serbest: 1, parilti: st.t > A('B08@filminden') && st.t < A('B08@filminden') + .5 ? '#FFFFFF' : '#C9D0D2' });   // el göğüs hizasından şakağa; omuz ≤ 1,3 rad
}, VID);
// P19 koridorun ucu: iki kapı, "SUPERINTENDENT" ve "WARDEN" levhaları
sahne('P19', 'B09', 'koridor', 'genis', (B, st) => {
  B.cam(960, 470, 1 + st.lt * .02);
  bodrum(B, st, { levha: false, sonD: .7 });
  const l = B.l, k = B.k;
  const isikW = ramp(st.t, A('B09@lisans') - .2, A('B09@lisans') + .5);
  for (const [x, ad] of [[820, 'SUPERINTENDENT'], [1100, 'WARDEN']]) {
    k.save(); k.fillStyle = B.ton(ad === 'WARDEN' ? lerp(.75, .1, isikW) : .75); k.fillRect(x - 70, 350, 140, 240); k.fillStyle = B.ton(.02); k.fillRect(x - 64, 330, 128, 22); k.restore();
    l.save(); l.lineWidth = 3; l.strokeStyle = '#000'; l.strokeRect(x - 70, 350, 140, 240); l.strokeRect(x - 64, 330, 128, 22); l.font = '700 14px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillStyle = '#000'; l.fillText(ad, x, 341); l.restore();
  }
}, { ...VID, over: (ctx, st) => { etiket(ctx, 'AMİR', 820, 270, st.t - A('B09@amir'), 6, { col: '#E9EEF0', panelRGB: KOYU }); etiket(ctx, 'MÜDÜR · DAVID JAFFE', 1180, 640, st.t - A('B09@müdür'), 6, { col: '#E9EEF0', panelRGB: KOYU }); } });
// P20 ayrıntı: koridorun ucunda, bölmenin arkasında kamera (karanlık, insan yok); merceğe yaklaşma; gözlem masası III. bölüme kadar görünmez (Kural 2)
sahne('P20', 'B10', 'kamera', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.05 + Math.min(st.lt, 12) * .03);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.82); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.55); k.fillRect(640, 260, 640, 520); k.restore();
  l.save(); l.fillStyle = '#000'; l.beginPath(); l.roundRect(760, 380, 380, 220, 30); l.fill(); l.beginPath(); l.arc(1170, 490, 95, 0, TAU); l.fill(); l.fillRect(900, 600, 30, 340); l.fillRect(820, 920, 190, 26); l.restore();
  k.save(); k.fillStyle = B.ton(.15 + .08 * Math.sin(st.t * 2)); k.beginPath(); k.ellipse(1190, 470, 30, 22, -.3, 0, TAU); k.fill(); k.restore();
}, VID);
