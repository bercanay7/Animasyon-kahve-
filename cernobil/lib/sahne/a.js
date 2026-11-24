// Kanca (A01-A03) ve I. Yaprak (B01-B12). Planlar cümleye/sözcüğe bağlı; ölçek: genis | orta | yakin | ayrinti | kart.
'use strict';
const KU = (s, o = {}) => (ctx, st) => kunye(ctx, s, st.lt, st.d, o);   // künye üst katmanı
const KAGIT = { kagit: 1 };

// ── KANCA ──
// P01 Rize, Ağustos 1986: gazetecilerin sırtı, flaşlar, masada mikrofonlar ve bardak. Yüz yok.
sahne('P01', 'A01-0.4', 'rize86', 'genis', (B, st) => {
  B.cam(960 + st.lt * 4, 520, 1.0 + st.lt * .006);
  SET.basinMasasi(B, st.t, { pencere: true });
  D.bardak(B, 760, 600, 1.3, { buhar: st.t, tabak: true });
  SET.gazeteciler(B, st.t, { n: 5, s: .85, y: 1200 });
  D.tarihBandi(B, 'AĞUSTOS 1986 · RİZE', 110, clamp(st.lt / .6));
  SET.flaslar(B, st.t, [S('A01') + 1.2, S('A01') + 2.3, A('A01@bardak') + .2]);
});
// P02 bardak yakın: el bardağı kaldırır (kapak A kompozisyonu), mikrofonlar arkada, flaş
sahne('P02', 'A01@bardak', 'rize86', 'yakin', (B, st) => {
  B.cam(980, 560, 1.06 + st.lt * .01);
  SET.zemin(B, .3, 2000);
  SET.bust(B, 1420, 1100, 2.4, .1);
  D.mikrofonlar(B, 1250, 1060, 1.7, 5, 9);
  const kalk = E.io3(clamp(st.lt / 2.2)), y = 900 - kalk * 110;
  D.bardak(B, 880, y, 3.2, { buhar: st.t, tabak: false });
  SET.el(B, 940, y - 140, 1.25, .5, { kav: .9 });
  SET.flaslar(B, st.t, [st.at + .5, st.at + 2.6]);
});
// P03 Ocak 1987: depo, çuval yığını, ışık şeridi; sayı yazılır
sahne('P03', 'A02', 'depo', 'genis', (B, st) => {
  B.cam(960 - st.lt * 6, 540, 1.02 + st.lt * .005);
  D.depoIc(B, { d: .45 });
  D.yigin(B, 700, 980, 1.1, { kat: 6, gen: 11 }); D.yigin(B, 1500, 1000, 1.25, { kat: 5, gen: 8 });
  D.tarihBandi(B, 'OCAK 1987', 110, clamp(st.lt / .6));
  D.sayi(B, '56.000', 1240, 330, { px: 150, birim: 'TON', p: ramp(st.t, A('A02@elli'), A('A02@elli') + 1.2) });
}, { over: KU('Çaykur açıklaması, Milliyet, 6 Ocak 1987, s. 11', { y: 640 }) });
// P04 kupür: 6 Ocak 1987 başlığı
sahne('P04', 'A02@insan', 'depo', 'ayrinti', (B, st) => {
  B.cam(960, 540 - st.lt * 5, 1.12 + st.lt * .01);
  SET.pano(B, { tohum: 4 });
  D.kupur(B, 960, 520, { w: 980, h: 640, a: -.02, ust: 'MİLLİYET · 6 OCAK 1987 · SAYFA 11', manset: 'Piyasaya sürülmedi, depolarda bekletiliyor: 56 bin ton çay radyasyonlu', mpx: 70, alinti: '...insan sağlığına tehlikeli olduğu için piyasaya sürülmedi.', px: 44, ah: 150, p: ramp(st.t, st.at + .3, Se('A02')) });
});
// P05 soru: tek bir bardak, beyaz örtü; buhar; kamera deme iner
sahne('P05', 'A03', 'bardak', 'orta', (B, st) => {
  B.cam(960, 560 - st.lt * 8, 1 + st.lt * .03);
  SET.zemin(B, .08, 640, .16);
  D.bardak(B, 960, 760, 3, { buhar: st.t, kasik: true });
  // "göremediğin, koklayamadığın, tadını": üç küçük boşluk vuruşu — bardağın etrafında hiçbir şey belirmez; yalnız buhar kesilir
}, { baski: st => ({ kagit: 1 }) });
sahne('P06', 'A03@neye', 'bardak', 'ayrinti', (B, st) => {
  // demin yüzeyi yakından: pencere yansıması (kâğıt beyazı şerit) yavaşça kayar; halka çizgisi yok (hedef tahtası okunmasın)
  B.cam(960, 540, 1 + st.lt * .03);
  SET.zemin(B, .2, 2000);
  D.bardak(B, 960, 1500, 11, { tabak: false });
  const k = B.k, x = 700 + st.lt * 30; k.save(); k.fillStyle = '#fff'; k.globalAlpha = .8; k.beginPath(); k.moveTo(x, 300); k.lineTo(x + 60, 300); k.lineTo(x + 20, 700); k.lineTo(x - 40, 700); k.closePath(); k.fill(); k.restore();
  B.c.save(); B.c.fillStyle = '#000'; B.c.beginPath(); B.c.moveTo(x, 300); B.c.lineTo(x + 60, 300); B.c.lineTo(x + 20, 700); B.c.lineTo(x - 40, 700); B.c.closePath(); B.c.fill(); B.c.restore();
});

// ── I. YAPRAK ──
// P07 Mayıs 1986, Rize yamaçları
sahne('P07', 'B01', 'yamac', 'genis', (B, st) => {
  B.cam(960 + st.lt * 10, 520, 1.02);
  D.bulutlar(B, st.t, { y: 90, d: .2, hiz: 30 });
  D.daglar(B, { y: 360, kat: [[.22, 0], [.34, 110], [.46, 220]] });
  D.bahce(B, { y0: 560, sira: 10, surgun: .9 });
  for (const [x, y, s] of [[300, 520, .8], [1500, 470, .6], [1720, 540, .9]]) D.ev(B, x, y, s);
  D.tarihBandi(B, 'MAYIS 1986 · RİZE', 110, clamp(st.lt / .6) * clamp((st.d - st.lt) / .4));
}, { tr: { type: 'merdane', dur: .9 } });
// P08 kahraman yaprak: sürgün ucunda iki yaprak bir tomurcuk; esinti
sahne('P08', 'B02', 'yaprak', 'ayrinti', (B, st) => {
  B.cam(960, 540, 1.0 + st.lt * .015);
  SET.zemin(B, .1, 2000);
  D.bahce(B, { y0: 820, y1: 1300, sira: 4, tohum: 5 });
  const sw = Math.sin(st.t * 1.3) * .05;
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 10; l.beginPath(); l.moveTo(940, 1120); l.quadraticCurveTo(950, 800, 960 + sw * 200, 460); l.stroke(); l.restore();
  D.yaprak(B, 860 + sw * 150, 640, 9, -.7 + sw, { renk: 0 });
  D.yaprak(B, 1080 + sw * 180, 560, 7.5, .6 + sw, { renk: 0 });
  D.yaprak(B, 965 + sw * 210, 400, 4.2, .08 + sw, { renk: 0, sap: false });   // tomurcuk
});
// P09 harita: Çernobil ve Rize; mesafe çizgisi
sahne('P09', 'B03', 'harita', 'genis', (B, st) => {
  B.cam(1000 + st.lt * 5, 520, .92 + st.lt * .005);
  D.harita(B, { kara: .3 });
  const c = D.sehir(B, 'Cernobil', 'ÇERNOBİL', { px: 40 }), r = D.sehir(B, 'Rize', 'RİZE', { px: 40, dy: -40, dx: -10 });
  const p = ramp(st.t, A('B03@kilometre') - .6, A('B03@kilometre') + .6), l = B.l;
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.setLineDash([16, 12]); l.beginPath(); l.moveTo(c[0], c[1]); l.lineTo(lerp(c[0], r[0], p), lerp(c[1], r[1], p)); l.stroke(); l.restore();
  D.sayi(B, '1.400 km', (c[0] + r[0]) / 2 + 160, (c[1] + r[1]) / 2, { px: 64, p });
  D.tarihBandi(B, '26 NİSAN 1986', 110, clamp(st.lt / .5));
});
// P10 bulut Avrupa'yı dolaşıp Trakya'ya
sahne('P10', 'B04', 'harita', 'orta', (B, st) => {
  B.cam(700 - st.lt * 6, 560, 1.15);
  D.harita(B, { kara: .3 });
  const e = D.sehir(B, 'Edirne', 'EDİRNE', { px: 40, dy: -36, dx: -30 });
  const u = ramp(st.t, st.at, A('B04@trakya') + .4, E.io2);
  D.bulutGolge(B, lerp(700, e[0] + 40, u), lerp(80, e[1] - 30, u), 300, 190, .62);
  D.tarihBandi(B, '29 NİSAN', 110, ramp(st.t, A('B04@trakya') - .3, A('B04@trakya') + .3));
});
// P11 Edirne köyü: süt güğümü devrilir, süt toprağa (kâğıt beyazı)
sahne('P11', 'B04@edirnenin', 'edirne', 'yakin', (B, st) => {
  B.cam(960, 600, 1.05 + st.lt * .01);
  SET.zemin(B, .25, 760, .5);
  const k = B.k, l = B.l, a = -ramp(st.t, A('B04@sütler') - .3, A('B04@sütler') + .5) * .9;
  // dökülen süt: kâğıt beyazı akıntı (ton ve çizgiden silinir)
  const akis = ramp(st.t, A('B04@sütler'), A('B04@sütler') + 1.6);
  FIG.kisi(l, 1180, 980, 420, { tip: 'koylu', f: -1, govde: .35, bas: .2, kolO: [.9, .8], kolA: [.7, .9] });
  // süt güğümü: yuvarlak omuz, dar boyun, kulp, kapak; yana yatar
  l.save(); l.translate(930, 870); l.rotate(a); l.fillStyle = '#000';
  l.beginPath(); l.moveTo(-70, 0); l.lineTo(-70, -120); l.quadraticCurveTo(-70, -170, -34, -180); l.lineTo(-30, -215); l.lineTo(30, -215); l.lineTo(34, -180); l.quadraticCurveTo(70, -170, 70, -120); l.lineTo(70, 0); l.closePath(); l.fill();
  l.fillRect(-40, -228, 80, 14); l.strokeStyle = '#000'; l.lineWidth = 9; l.beginPath(); l.arc(0, -150, 95, PI * 1.15, PI * 1.85); l.stroke();
  l.fillStyle = '#fff'; l.fillRect(-70, -60, 140, 8); l.restore();
  // ağızdan akan süt (kâğıt beyazı)
  if (a < -.3) { const k2 = B.k; k2.save(); k2.strokeStyle = '#fff'; k2.lineWidth = 22; k2.lineCap = 'round'; const m = rot([0, -215], a); k2.beginPath(); k2.moveTo(930 + m[0], 870 + m[1]); k2.quadraticCurveTo(820, 760, 790, 890); k2.stroke(); k2.restore(); }
  if (akis > 0) { k.save(); k.fillStyle = '#fff'; k.beginPath(); k.ellipse(760, 900, 260 * akis, 40 * akis, 0, 0, TAU); k.fill(); k.restore(); l.save(); l.strokeStyle = '#000'; l.lineWidth = 2; l.beginPath(); l.ellipse(760, 900, 260 * akis, 40 * akis, 0, 0, TAU); l.stroke(); l.restore(); }
});
// P12 harita: 7 Mayıs, bulutlar Doğu Karadeniz'e
sahne('P12', 'B05', 'harita', 'genis', (B, st) => {
  B.cam(1180 + st.lt * 10, 640, 1.1);
  D.harita(B, { kara: .3 });
  D.sehir(B, 'Rize', 'RİZE', { px: 40, dy: 34, dx: -10 });
  const u = ramp(st.t, st.at, st.at + 3, E.io2);
  D.bulutGolge(B, lerp(900, 1520, u), lerp(420, 780, u), 330, 150, .62);
  D.tarihBandi(B, '7 MAYIS', 110, clamp(st.lt / .5));
});
// P13 yağmur yamaçta
sahne('P13', 'B05@yağmur', 'yamac', 'orta', (B, st) => {
  B.cam(900 - st.lt * 8, 560, 1.12);
  D.bulutlar(B, st.t, { y: 230, d: .6, hiz: 40 });
  D.daglar(B, { y: 420, kat: [[.32, 0], [.48, 120]] });
  D.bahce(B, { y0: 640, sira: 7, surgun: .9, tohum: 21 });
  D.yagmur(B, st.t, { d: .55, n: 420 });
});
// P14 yaprakta damlalar: rengi yok, kokusu yok, tadı yok (görüntüde hiçbir şey belirmez); damlalar kâğıt beyazı
sahne('P14', 'B06', 'yaprak', 'ayrinti', (B, st) => {
  B.cam(960, 540, 1.15 + st.lt * .012);
  SET.zemin(B, .18, 2000);
  D.yagmur(B, st.t, { d: .35, n: 140, boy: 110, w: 2.4 });
  const sw = Math.sin(st.t * 2.1) * .03 - ramp(st.t, A('B06@yaprak'), A('B06@yaprak') + .4) * .03;
  D.yaprak(B, 960, 560, 16, -.35 + sw, { renk: 0 });
  const r = rng(77), l = B.l, k = B.k;
  for (let i = 0; i < 9; i++) { const dx = (r() - .5) * 170, dy = (r() - .5) * 420, rr = 8 + r() * 10, ak = ((st.t * .2 + r()) % 1) * 60;
    const p = rot([dx, dy + ak], -.35 + sw); const x = 960 + p[0], y = 560 + p[1];
    k.save(); k.fillStyle = '#fff'; k.beginPath(); k.ellipse(x, y, rr, rr * 1.2, 0, 0, TAU); k.fill(); k.restore();
    B.c.save(); B.c.fillStyle = '#000'; B.c.beginPath(); B.c.ellipse(x, y, rr * .7, rr * .8, 0, 0, TAU); B.c.fill(); B.c.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 2.2; l.beginPath(); l.ellipse(x, y, rr, rr * 1.2, 0, 0, TAU); l.stroke(); l.restore(); }
});
// P15 TAEK ekibi sahil yolunda ölçüyor: elde ölçüm aleti; sayı
sahne('P15', 'B07', 'sahil', 'orta', (B, st) => {
  B.cam(960 + st.lt * 12, 560, 1.0);
  SET.zemin(B, .12, 640, .3);
  const k = B.k; k.save(); k.fillStyle = B.ton(.05); k.fillRect(-600, 520, W + 1200, 130); k.restore();      // deniz
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); for (let x = -400; x < W + 400; x += 30) l.lineTo(x, 650 + Math.sin(x / 60 + st.t * 2) * 4); l.stroke(); l.restore();
  // araç (minibüs siluet)
  l.save(); l.fillStyle = '#000'; l.beginPath(); l.roundRect(260, 640, 420, 190, 26); l.fill(); l.fillStyle = '#fff'; for (let i = 0; i < 3; i++) l.fillRect(300 + i * 120, 670, 90, 60); l.fillStyle = '#000'; l.beginPath(); l.arc(350, 840, 40, 0, TAU); l.arc(600, 840, 40, 0, TAU); l.fill(); l.restore();
  const walk = HAREKET.yuruyus({ tip: 'yuru' });
  const kk = FIG.kisi(l, 980 + st.lt * 18, 900, 360, { tip: 'laborant', f: 1, govde: .12, bas: .3, kolO: [1.05, .9], kolA: [.2, .3] });
  // ölçüm aleti elinde
  l.save(); l.fillStyle = '#000'; l.fillRect(kk.elO[0] - 4, kk.elO[1] - 38, 70, 46); l.restore();
  D.tarihBandi(B, '11 MAYIS 1986 · SİNOP', 110, clamp(st.lt / .5));
  D.sayi(B, '30-40 µR/sa', 1440, 380, { px: 70, p: ramp(st.t, A('B07@buldukları'), A('B07@buldukları') + 1) });
  D.sayi(B, 'TRAKYA 20-30', 1440, 470, { px: 44, p: ramp(st.t, A('B07@trakya') - .3, A('B07@trakya') + .6) });
}, { over: KU('Milliyet, 19 Şubat 1988, s. 9 (o günlerin belgeleri)', { y: 200 }) });
// P16 harita: Edirne damgalı, Rize boş
sahne('P16', 'B08', 'harita', 'genis', (B, st) => {
  B.cam(960, 640, 1.0 + st.lt * .01);
  D.harita(B, { kara: .3 });
  const e = D.sehir(B, 'Edirne', 'EDİRNE', { px: 36, dy: -36, dx: -30 }), r = D.sehir(B, 'Rize', 'RİZE', { px: 36, dy: 34, dx: -10 });
  SET.damga(B, 'ÖNLEM', e[0] + 120, e[1] + 110, { px: 54, p: ramp(st.t, st.at + .3, st.at + .6, E.lin) });
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.setLineDash([8, 10]); l.strokeRect(r[0] - 130, r[1] + 60, 260, 90); l.restore();   // Rize: boş çerçeve (önlem yok)
});
// P17 1986 oturma odası: televizyonda konuşan siluet (Kurum başkanı; yüz yok), önde oturanların sırtı
sahne('P17', 'B08@kurumun', 'tv', 'orta', (B, st) => {
  B.cam(960, 560, 1.04 + st.lt * .012);
  SET.zemin(B, .45, 760, .62);
  SET.tv(B, 960, 460, 1.4, (x, y, w, h) => { const k = B.k; k.fillStyle = B.ton(.15); k.fillRect(x, y, w, h); FIG.kisi(k, x + w * .5, y + h + 60, h * .95, { tip: 'takim', f: 1, renk: B.ton(.75), bas: .05 + Math.sin(st.t * 3) * .03, kolO: [.75 + Math.sin(st.t * 2) * .12, 1.2], kolA: [-.05, .15] }); });
  SET.bust(B, 560, 1160, 1.5, .05); SET.bust(B, 1360, 1180, 1.35, -.05);
  D.bardak(B, 1500, 980, 1.6, { buhar: st.t, renk: 1 });
}, { over: KU('"Korkulacak bir durum olmadığını…" — Milliyet, 19 Şubat 1988, s. 9', { y: 96 }) });
// P18 toplayıcılar yamaçta, sırtlarında küfe; yürüyüş
sahne('P18', 'B09', 'yamac', 'genis', (B, st) => {
  B.cam(960, 560, 1.06);
  D.daglar(B, { y: 300, kat: [[.2, 0], [.32, 120]] });
  D.bahce(B, { y0: 500, sira: 10, surgun: .8, tohum: 33 });
  const g = HAREKET.yuruyus({ tip: 'surun' });
  for (let i = 0; i < 3; i++) {
    const x = 420 + i * 420 + st.lt * 26, y = 800 + i * 50;
    const kk = FIG.kisi(B.l, x, y, 250 + i * 30, { tip: 'toplayici', f: 1, govde: .3 + Math.sin(st.t * 2 + i) * .04, bas: .25, kolO: [.9 + Math.sin(st.t * 3 + i) * .2, .6], kolA: [.5, .5] });
    FIG.desen(B, { tohum: i + 3 }); FIG.kufe(B, kk.omuz, kk.s, 1, .8);
  }
});
// P19 el yaprağı koparır, sepete
sahne('P19', 'B09@yapraklar', 'yaprak', 'ayrinti', (B, st) => {
  B.cam(960, 540, 1.05);
  SET.zemin(B, .14, 2000);
  D.bahce(B, { y0: 760, y1: 1300, sira: 4, tohum: 5, surgun: .9 });
  const kop = ramp(st.t, st.at + .5, st.at + 1.3), git = ramp(st.t, st.at + 1.6, st.at + 3.0);
  const lx = lerp(980, 1500, git), ly = lerp(520, 300, git) + kop * -40;
  D.yaprak(B, lx, ly, 9, -.5 + git * 1.2, { renk: 0 });
  SET.el(B, lx + 70, ly + 20, 1.2, .5 - git * .3, { kav: .3 + kop * .6, f: 1 });
});
// P20 sepetler patikadan fabrikaya
sahne('P20', 'B09@fabrikaya', 'yol', 'orta', (B, st) => {
  B.cam(960 - st.lt * 14, 520, 1.0);
  D.daglar(B, { y: 300, kat: [[.25, 0], [.4, 160]] });
  D.fabrika(B, 1500, 640, .8, { duman: st.t, d: .45 });
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.beginPath(); l.moveTo(-200, 1000); l.quadraticCurveTo(700, 780, 1300, 660); l.stroke(); l.restore();
  for (let i = 0; i < 4; i++) { const u = (i * .22 + st.lt * .03) % 1, x = lerp(-100, 1250, u), y = lerp(1000, 670, Math.pow(u, .8)), s = lerp(300, 120, u);
    const kk = FIG.kisi(B.l, x, y, s, { tip: i % 2 ? 'koylu' : 'toplayici', f: 1, govde: .2, bas: .1, kolO: [.3, .4], kolA: [.2, .4] }); if (i % 2 === 0) FIG.desen(B, { tohum: 9 + i }); FIG.kufe(B, kk.omuz, kk.s, 1, 1); }
});
// P21 fabrika içi: soldurma tekneleri, kıvırma; "bakır"da renk döner (sözcüğe bağlı palet)
sahne('P21', 'B10', 'fabrika', 'genis', (B, st) => {
  B.cam(960 + st.lt * 8, 540, 1.02);
  D.depoIc(B, { d: .55 });
  const ton = ramp(st.t, A('B10@bakır') - .5, A('B10@bakır') + .7);
  const k = B.k, l = B.l;
  for (let j = 0; j < 3; j++) { const y = 620 + j * 140; k.save(); k.fillStyle = B.ton(.65); k.fillRect(120, y, 1680, 26); k.restore(); l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.strokeRect(120, y, 1680, 26); l.restore();
    const r = rng(j + 7); for (let i = 0; i < 60; i++) { const x = 140 + i * 28 + ((st.lt * 30 * (j % 2 ? -1 : 1)) % 28), yy = y - 12 - r() * 16; const a = r() * PI; B.cayBoya(g => g.ellipse(x, yy, 18, 8, a, 0, TAU), 1, ton); B.k.save(); B.k.strokeStyle = B.ton(.8); B.k.lineWidth = 1.5; B.k.beginPath(); B.k.ellipse(x, yy, 18, 8, a, 0, TAU); B.k.stroke(); B.k.restore(); } }
  FIG.kisi(B.l, 1560, 1080, 380, { tip: 'isci', f: -1, govde: .3, bas: .2, kolO: [.9, .5], kolA: [.6, .6] });
});
// P22 kurutma: kahraman yaprak koyulaşıyor (ton .5 → .9) ve küçülüyor
sahne('P22', 'B10@kurutulur', 'fabrika', 'ayrinti', (B, st) => {
  B.cam(960, 540, 1.1);
  SET.zemin(B, .55, 2000);
  const p = ramp(st.t, st.at, st.at + 2.6);
  D.yaprak(B, 960, 540, lerp(13, 8, p), .3 + p * 1.8, { renk: lerp(.55, .92, p), gol: lerp(.12, .55, p) });
  const k = B.k; k.save(); k.strokeStyle = B.ton(.85); k.lineWidth = 3; for (let i = 0; i < 12; i++) { k.beginPath(); k.moveTo(-100, 200 + i * 70 + (st.lt * 40) % 70); k.lineTo(W + 100, 200 + i * 70 + (st.lt * 40) % 70); k.stroke(); } k.restore();
});
// P23 terazi: beş kilo yaş yaprak ↔ bir kilo kuru çay
sahne('P23', 'B11', 'terazi', 'orta', (B, st) => {
  B.cam(960, 540, 1.0 + st.lt * .008);
  SET.zemin(B, .1, 820, .3);
  SET.cayYigini(B, 560, 820, 280, 200, 0, 3);
  const p = ramp(st.t, A('B11@bir') - .6, A('B11@bir') + .4), l = B.l;
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 8; l.beginPath(); l.moveTo(900, 700); l.lineTo(900 + 260 * p, 700); l.stroke(); if (p > .9) { l.beginPath(); l.moveTo(1130, 670); l.lineTo(1165, 700); l.lineTo(1130, 730); l.stroke(); } l.restore();
  if (p > .5) SET.cayYigini(B, 1400, 820, 120, 70, .92, 4);
  D.sayi(B, '5 kg', 560, 420, { px: 90, p: ramp(st.t, A('B11@beş') - .2, A('B11@beş') + .5) });
  D.sayi(B, '1 kg', 1400, 420, { px: 90, p: ramp(st.t, A('B11@bir') - .2, A('B11@bir') + .5) });
});
// P24 bakkal rafı 1986; el bir paket alır
sahne('P24', 'B12', 'bakkal', 'genis', (B, st) => {
  B.cam(960 + st.lt * 14, 540, 1.0);
  SET.bakkal(B, st.t, { yil: '1986' });
  const al = ramp(st.t, st.at + .6, st.at + 2);
  SET.el(B, 1180 + al * 80, 520 - al * 40, 1, .3, { kav: .8, f: 1 });
});
