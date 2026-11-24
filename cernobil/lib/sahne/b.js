// II. Bardak (C01-C11) ve III. Yirmi saat (D01-D13).
'use strict';
const KU2 = (s, o = {}) => (ctx, st) => kunye(ctx, s, st.lt, st.d, o);

// ── II. BARDAK ──
// P25 paket yakın: soru
sahne('P25', 'C01', 'bakkal', 'yakin', (B, st) => {
  B.cam(960, 540 - st.lt * 6, 1.0 + st.lt * .02);
  SET.zemin(B, .3, 2000);
  SET.paket(B, 960, 900, 3.4, { yil: '1986', d: .2 });
  const l = B.l; l.save(); l.font = FONT.manset(150); l.textAlign = 'center'; l.fillStyle = '#000'; l.globalAlpha = ramp(st.t, st.at + .3, st.at + .8); l.fillText('?', 1420, 420); l.restore();
});
// P26 Almanya'da laboratuvar: önlüklü siluet, sayaç ekranında rakamlar dönüyor
sahne('P26', 'C01@kasım', 'labDE', 'orta', (B, st) => {
  B.cam(960 + st.lt * 8, 540, 1.04);
  D.lab(B);
  FIG.kisi(B.l, 800, 960, 520, { tip: 'laborant', f: 1, govde: .18, bas: .35, kolO: [.6, 1.3], kolA: [.4, 1.3] });
  SET.paket(B, 1310, 375, 1, { yil: '1986', d: .25 });
  D.tarihBandi(B, 'KASIM 1986 · ALMANYA', 110, clamp(st.lt / .5));
  D.sayi(B, String(1000 + Math.floor(st.lt * 1234) % 9000).padStart(5, '0'), 1310, 640, { px: 64 });
});
// P27 bekerel: sayaç her saniye bir artar (kart)
sahne('P27', 'C02', 'sayac', 'kart', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .006);
  SET.zemin(B, .06, 2000);
  const n = Math.floor(Math.max(0, st.t - A('C02@saniyede')) + 1);
  D.sayi(B, 'BEKEREL', 960, 330, { px: 96 });
  D.sayi(B, String(st.t >= A('C02@saniyede') ? n : 0), 960, 640, { px: 260 });
  SET.saat(B, 1560, 600, 90, st.t / 60);
  D.sayi(B, '1 Bq = saniyede 1 bozunma', 960, 800, { px: 44, p: ramp(st.t, A('C02@saniyede') - .2, A('C02@saniyede') + .8) });
});
// P28 sınır: bir kilo, 600
sahne('P28', 'C03', 'terazi', 'orta', (B, st) => {
  B.cam(960, 540, 1.0 + st.lt * .01);
  SET.zemin(B, .12, 860, .3);
  SET.terazi(B, 760, 860, 1, Math.sin(st.t * 1.2) * .015, (x, y) => SET.cayYigini(B, x, y, 80, 60, .92, 6), (x, y) => { const l = B.l; l.fillRect(x - 40, y - 60, 80, 60); });
  D.sayi(B, '1 kg', 460, 380, { px: 70 });
  D.sayi(B, '600', 1460, 520, { px: 200, birim: 'Bq/kg', p: ramp(st.t, A('C03@altı') - .3, A('C03@altı') + .6) });
  SET.damga(B, 'SINIR', 1460, 700, { px: 60, p: ramp(st.t, A('C03@izin') - .1, A('C03@izin') + .25, E.lin) });
}, { over: KU2('Avrupa Topluluğu sınırı, 1986') });
// P29 gizli rapor: daktilo satırları, 15.000 büyür
sahne('P29', 'C04', 'rapor', 'yakin', (B, st) => {
  B.cam(960, 540, 1.04 + st.lt * .01);
  SET.zemin(B, .5, 2000);
  SET.daktilo(B, 300, 120, 820, 860, ['!RADYASYON ÖLÇÜM RAPORU', 'Birinci sürgün, kuru çay', 'Fabrika: GÜNEYSU', 'Sonuç (Bq/kg): ..........'], ramp(st.t, st.at, st.at + 2.4));
  SET.damga(B, 'GİZLİ', 900, 220, { px: 70, a: .12, p: ramp(st.t, st.at + .4, st.at + .65, E.lin) });
  D.sayi(B, '15.000', 1450, 560, { px: 170, p: ramp(st.t, A('C04@on'), A('C04@on') + 1) });
}, { over: KU2('Milliyet, 6 Ocak 1987, s. 11 (Çaykur\'un raporları)') });
// P30 Ankara, kış: basın toplantısı salonu, pencerede kar
sahne('P30', 'C05', 'ankara86', 'genis', (B, st) => {
  B.cam(960 - st.lt * 5, 520, 1.0 + st.lt * .004);
  SET.basinMasasi(B, st.t, { pencere: true, kx: 1000 });
  const k = B.k, r = rng(3); k.save(); k.fillStyle = '#fff'; for (let i = 0; i < 40; i++) { const x = 1430 + r() * 340, y = 160 + ((r() * 280 + st.t * 30) % 280); k.beginPath(); k.arc(x, y, 3, 0, TAU); k.fill(); } k.restore();
  D.bardak(B, 820, 600, 1.2, { buhar: st.t });
  SET.gazeteciler(B, st.t, { n: 5, s: .8, y: 1210, tohum: 3 });
  D.tarihBandi(B, 'ARALIK 1986 · ANKARA', 110, clamp(st.lt / .5));
  SET.flaslar(B, st.t, [A('C05@demli') + .1]);
}, { tr: { type: 'merdane', dur: .9 } });
// P31 gazeteciler soruyor: el kaldıran (dirsek bükük), not defterleri
sahne('P31', 'C06', 'ankara86', 'orta', (B, st) => {
  B.cam(960, 620, 1.18);
  SET.zemin(B, .2, 640, .35);
  for (let i = 0; i < 4; i++) { const x = 300 + i * 420, kk = FIG.kisi(B.l, x, 1120, 520, { tip: 'gazeteci', f: i < 2 ? 1 : -1, bacak: 'otur', govde: .15, bas: .2 + Math.sin(st.t * 2 + i) * .05, kolO: [.75, 1.25], kolA: [.55, 1.35] });
    const l = B.l; l.save(); l.fillStyle = '#fff'; l.fillRect(kk.elA[0] - 20, kk.elA[1] - 10, 40, 30); l.restore(); }
});
// P32 Milliyet kupürü: "radyasyona nispet yapar gibi"
sahne('P32', 'C06@ertesi', 'kupur', 'ayrinti', (B, st) => {
  B.cam(960, 520 - st.lt * 4, 1.06 + st.lt * .01);
  SET.pano(B, { tohum: 7 });
  D.kupur(B, 960, 500, { w: 1000, h: 700, a: .02, ust: 'MİLLİYET · 9 ARALIK 1986 · SAYFA 7', manset: 'Radyasyona inat, bardak bardak içti', mpx: 84, alinti: '"...radyasyona nispet yapar gibi, son derece koyu demli çay içti."', px: 44, ah: 170, p: ramp(st.t, st.at + .3, Se('C06')) });
});
// P33 bardak elde, buhar; söz kupürü yanda
sahne('P33', 'C07', 'ankara86', 'yakin', (B, st) => {
  B.cam(1000, 560, 1.05 + st.lt * .012);
  SET.zemin(B, .32, 2000);
  SET.bust(B, 1500, 1160, 2.2, .12);
  const y = 860 - Math.sin(clamp(st.lt / 3) * PI) * 60;
  D.bardak(B, 1080, y, 2.8, { buhar: st.t });
  SET.el(B, 1130, y - 120, 1.1, .5, { kav: .9 });
  D.kupur(B, 560, 400, { w: 760, h: 520, a: -.03, ust: 'MİLLİYET · 9 ARALIK 1986', alinti: '"Çayda da bir miktar radyasyon olduğu doğrudur. Ama bu, sağlık açısından son derece zararsızdır."', px: 44, ah: 330, sutun: 2, p: ramp(st.t, st.at + .2, Se('C07')) });
});
// P34 demlik kaynıyor: 300-350 ↔ 600
sahne('P34', 'C08', 'kaynama', 'orta', (B, st) => {
  B.cam(960, 560, 1.02 + st.lt * .01);
  SET.zemin(B, .1, 780, .3);
  SET.demlik(B, 620, 700, 1.3, st.t, { ocak: true });
  D.sayi(B, '300-350 Bq/kg', 1360, 420, { px: 96, p: ramp(st.t, A('C08@üç') - .2, A('C08@üç') + .9) });
  D.sayi(B, '< 600', 1380, 620, { px: 120, p: ramp(st.t, A('C08@altı') - .2, A('C08@altı') + .6) });
}, { over: KU2('Bakanın sözü, Milliyet, 9 Aralık 1986, s. 7') });
// P35 marul ve bardak (bakanın kendi benzetmesi), yan yana masada
sahne('P35', 'C09', 'marul', 'ayrinti', (B, st) => {
  B.cam(960, 560, 1.1 + st.lt * .012);
  SET.zemin(B, .08, 760, .22);
  D.bardak(B, 1320, 860, 2.6, { buhar: st.t, kasik: true });
  D.kupur(B, 680, 440, { w: 820, h: 360, a: .02, alinti: '"Yani, çay marul gibi yenmezse hiçbir tehlike söz konusu değildir."', px: 46, ah: 260, sutun: 0, ust: 'MİLLİYET · 9 ARALIK 1986 · SAYFA 7', p: ramp(st.t, st.at + .2, Se('C09')) });
});
// P36 basın masası: bakan cümleyi kuruyor; kupür satırı
sahne('P36', 'C10', 'ankara86', 'genis', (B, st) => {
  B.cam(960, 560, 1.0 + st.lt * .01);
  SET.basinMasasi(B, st.t, { pencere: true, kx: 1000, bas: Math.sin(st.t * 1.7) * .04 });
  D.bardak(B, 820, 600, 1.2);
  SET.gazeteciler(B, st.t, { n: 5, s: .8, y: 1210, tohum: 3 });
  D.kupur(B, 520, 300, { w: 780, h: 380, a: -.02, golge: true, alinti: '"Eğer biz on kişinin bile öleceğine inansaydık, tüm çayı imha eder, 150 milyarlık çay ithalatına giderdik."', px: 38, ah: 300, sutun: 0, p: ramp(st.t, A('C10@eğer'), Se('C10')) });
});
// P37 pano: kupür iğnelenir
sahne('P37', 'C11', 'pano', 'yakin', (B, st) => {
  B.cam(960, 540, 1.08 + st.lt * .02);
  SET.pano(B, { tohum: 9 });
  const dus = E.out3(clamp(st.lt / .5));
  D.kupur(B, 960, 500 - (1 - dus) * 60, { w: 980, h: 420, a: -.04, alinti: '"Eğer biz on kişinin bile öleceğine inansaydık, tüm çayı imha eder, 150 milyarlık çay ithalatına giderdik."', px: 48, ah: 330, sutun: 0, ust: 'MİLLİYET · 9 ARALIK 1986 · SAYFA 7' });
  SET.igne(B, 520, 320, 1.4); SET.igne(B, 1400, 300, 1.4);
});

// ── III. YİRMİ SAAT ──
// P38 daktilo yazı: 15 Aralık
sahne('P38', 'D01', 'yazi', 'ayrinti', (B, st) => {
  B.cam(960, 560 - st.lt * 10, 1.02 + st.lt * .01);
  SET.zemin(B, .45, 2000);
  SET.daktilo(B, 420, 120, 1080, 900, ['!T.C. SANAYİ VE TİCARET BAKANLIĞI', '15 Aralık 1986', 'ÇAY İŞLETMELERİ GENEL MÜDÜRLÜĞÜNE', '', 'Bundan sonra, Atom Enerjisi Kurumu uzmanları incelemeden hiçbir çay piyasaya sürülmeyecektir.'], ramp(st.t, st.at, Se('D01') - .5));
}, { over: KU2('Bakanlık yazısı, Milliyet, 27 Kasım 1987, s. 8') });
// P39 depo: Ocak 1987, 56.000 ton
sahne('P39', 'D02', 'depo', 'genis', (B, st) => {
  B.cam(960 + st.lt * 10, 560, 1.06);
  D.depoIc(B, { d: .45 });
  D.yigin(B, 520, 1000, 1.2, { kat: 7, gen: 10 }); D.yigin(B, 1420, 1000, 1.2, { kat: 7, gen: 10 });
  D.tarihBandi(B, 'OCAK 1987', 110, clamp(st.lt / .5));
  D.sayi(B, '56.000 TON', 960, 330, { px: 110, p: ramp(st.t, A('D02@elli'), A('D02@elli') + 1) });
}, { tr: { type: 'merdane', dur: .9 } });
// P40 genel müdürün masası: çay döker (eller), aile fotoğrafı çerçevesi (yüzsüz), söz kupürde
sahne('P40', 'D03', 'ofis', 'orta', (B, st) => {
  B.cam(960, 560, 1.04 + st.lt * .01);
  SET.zemin(B, .2, 700, .45);
  SET.bust(B, 760, 760, 1.6, .15);
  SET.masa(B, 700, .35);
  const p = clamp((st.lt - .5) / 2.5);
  D.bardak(B, 1000, 760, 1.6, { dolu: .2 + p * .65, buhar: st.t });
  D.kupur(B, 1460, 300, { w: 720, h: 400, a: .03, alinti: '"Ben göstermelik olsun diye çay içmiyorum. Hem ben hem de aile fertlerim rahatlıkla içiyoruz."', px: 38, ah: 300, sutun: 0, ust: 'MİLLİYET · 6 OCAK 1987', p: ramp(st.t, A('D03@ben'), Se('D03')) });
});
// P41 harman: iki yığın kürekle karıştırılır; ortalama 10.000
sahne('P41', 'D04', 'harman', 'yakin', (B, st) => {
  B.cam(960, 560, 1.06 + st.lt * .01);
  SET.zemin(B, .2, 760, .35);
  const m = ramp(st.t, st.at + .5, st.at + 4);
  SET.cayYigini(B, lerp(620, 860, m), 900, 260, 180, .92, 3); SET.cayYigini(B, lerp(1300, 1060, m), 900, 260, 160, .85, 8);
  const kx = 960 + Math.sin(st.t * 3) * 120; const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 16; l.beginPath(); l.moveTo(kx + 200, 300); l.lineTo(kx + 30, 700); l.stroke(); l.lineWidth = 6; l.beginPath(); l.moveTo(kx + 175, 290); l.lineTo(kx + 235, 300); l.stroke(); l.fillStyle = '#000'; l.beginPath(); l.moveTo(kx - 40, 700); l.lineTo(kx + 90, 700); l.lineTo(kx + 70, 800); l.lineTo(kx - 20, 800); l.closePath(); l.fill(); l.restore();   // kürek (sap, tutamak, düz ağız)
  D.sayi(B, 'ort. 10.000', 960, 300, { px: 90, birim: 'Bq/kg', p: ramp(st.t, A('D04@ortalama') - .2, A('D04@ortalama') + .8) });
}, { over: KU2('ODTÜ\'lü dört bilim insanının bildirisi, Milliyet, 4 Mart 1987, s. 9') });
// P42 mektup: zarf ve daktilo satırı
sahne('P42', 'D05', 'mektup', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.0 + st.lt * .014);
  SET.zemin(B, .4, 2000);
  SET.daktilo(B, 360, 140, 1200, 780, ['!TÜRKİYE ATOM ENERJİSİ KURUMU', '27 Ocak 1987', 'Başbakanlığa, Bakanlıklara, ODTÜ Rektörlüğüne', '', '...ilmi tutanağı olmayan koca bir yalandır.'], ramp(st.t, st.at, Se('D05') - .3));
}, { over: KU2('Mektubun tam metni, Milliyet, 25 Şubat 1987, s. 9') });
// P43 İstanbul, yirmi saatlik masa: iki taraf, bardaklar çoğalır, saat döner
sahne('P43', 'D06', 'masa', 'genis', (B, st) => {
  B.cam(960, 560, 1.0 + st.lt * .006);
  SET.zemin(B, .15, 600, .3);
  const k = B.k; k.save(); k.fillStyle = B.ton(.55); k.beginPath(); k.ellipse(960, 760, 760, 150, 0, 0, TAU); k.fill(); k.restore();
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.ellipse(960, 760, 760, 150, 0, 0, TAU); l.stroke(); l.restore();
  for (let i = 0; i < 5; i++) { FIG.kisi(B.l, 380 + i * 60, 1010 - i * 70, 380 - i * 30, { tip: i % 2 ? 'takim' : 'gazeteci', f: 1, bacak: 'otur', govde: .1, bas: .1, kolO: [1.3, 1.3], kolA: [1.1, 1.2] }); FIG.kisi(B.l, 1540 - i * 60, 1010 - i * 70, 380 - i * 30, { tip: i % 2 ? 'gazeteci' : 'takim', f: -1, bacak: 'otur', govde: .1, bas: .1, kolO: [1.3, 1.3], kolA: [1.1, 1.2] }); }
  const n = Math.floor(clamp(st.lt / 6) * 14) + 2, r = rng(4);
  for (let i = 0; i < n; i++) D.bardak(B, 560 + r() * 800, 720 + r() * 70, .7, { dolu: .3 + r() * .5, tabak: true });
  SET.saat(B, 960, 300, 110, 10 + st.lt * 2.4);
  D.tarihBandi(B, 'ŞUBAT 1987 · İSTANBUL', 110, clamp(st.lt / .5));
}, { over: KU2('Milliyet, 15 Şubat 1987, s. 1') });
// P44 masanın bir yanı boşalır (gergin bitti): sandalyeler boş
sahne('P44', 'D06@gergin', 'masa', 'orta', (B, st) => {
  B.cam(1200, 620, 1.3);
  SET.zemin(B, .15, 600, .3);
  const k = B.k; k.save(); k.fillStyle = B.ton(.55); k.beginPath(); k.ellipse(960, 760, 760, 150, 0, 0, TAU); k.fill(); k.restore();
  const git = ramp(st.t, st.at + .2, st.at + 1.8);
  for (let i = 0; i < 3; i++) { const kk = FIG.kisi(B.l, 1500 - i * 70 + git * 400, 1010 - i * 70, 380 - i * 30, { tip: 'takim', f: 1, govde: .05, bas: .05, kolO: [.15, .25], kolA: [-.35, .2] }); B.l.fillStyle = '#000'; B.l.fillRect(kk.elA[0] - 6 * kk.s, kk.elA[1], 12 * kk.s, 9 * kk.s); }   // çantalar
  const r = rng(4); for (let i = 0; i < 14; i++) D.bardak(B, 560 + r() * 800, 720 + r() * 70, .7, { dolu: r() * .3, tabak: true });
});
// P45 soru: kuru çay → dem; süzgeçte posa, bardakta dem
sahne('P45', 'D07', 'demlik', 'ayrinti', (B, st) => {
  B.cam(960, 560, 1.06 + st.lt * .015);
  SET.zemin(B, .08, 800, .2);
  SET.cayYigini(B, 520, 760, 170, 120, .92, 12);
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 6; l.beginPath(); l.moveTo(760, 640); l.lineTo(1080, 640); l.stroke(); l.beginPath(); l.moveTo(1060, 615); l.lineTo(1100, 640); l.lineTo(1060, 665); l.stroke(); l.restore();
  D.bardak(B, 1380, 860, 2.6, { dolu: ramp(st.t, st.at + .5, st.at + 2.5) * .85, buhar: st.t });
  D.sayi(B, '?', 920, 540, { px: 140 });
});
// P46 iki sayı (kart): Kurum %1,66 ↔ ODTÜ %65; ODTÜ'nün beyanı: "kabul edildi"
sahne('P46', 'D08', 'iki_sayi', 'kart', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .005);
  SET.zemin(B, .05, 2000);
  const l = B.l; l.save(); l.fillStyle = '#000'; l.fillRect(958, 200, 4, 620); l.restore();
  D.sayi(B, 'KURUM', 520, 300, { px: 56 }); D.sayi(B, 'ODTÜ', 1400, 300, { px: 56 });
  D.sayi(B, '%1,66', 520, 560, { px: 190, p: ramp(st.t, st.at + .2, st.at + 1.2) });
  D.sayi(B, '%65', 1400, 560, { px: 190, p: ramp(st.t, A('D08@odtünün'), A('D08@odtünün') + 1) });
  D.sayi(B, 'en çok %3', 520, 700, { px: 48, p: ramp(st.t, st.at + 1, st.at + 1.6) });
  D.sayi(B, "ODTÜ'ye göre Kurum da kabul etti", 1400, 720, { px: 36, p: ramp(st.t, A('D08@kabul') - .2, A('D08@kabul') + .8) });
}, { over: KU2('Kurum: Milliyet, 25 Şubat 1987 · ODTÜ: Milliyet, 4 Mart 1987') });
// P47 komite kitapçığı: %2
sahne('P47', 'D09', 'kitapcik', 'yakin', (B, st) => {
  B.cam(960, 540, 1.04 + st.lt * .014);
  SET.zemin(B, .35, 2000);
  const k = B.k; k.save(); k.translate(12, 14); k.fillStyle = B.ton(.4); k.fillRect(560, 120, 800, 840); k.restore(); k.save(); k.fillStyle = '#fff'; k.fillRect(560, 120, 800, 840); k.restore();
  const l = B.l; l.save(); l.fillStyle = '#000'; l.font = FONT.manset(70); l.textAlign = 'center'; l.fillText('RADYASYON HAKKINDA', 960, 280); l.fillText('ÖZET BİLGİLER', 960, 360); l.font = FONT.daktilo(36, 700); l.fillText('Türkiye Radyasyon Güvenliği Komitesi', 960, 450); l.restore();
  D.sayi(B, 'geçiş oranı: %2', 960, 680, { px: 64, p: ramp(st.t, st.at + .4, st.at + 1.4) });
  const p = ramp(st.t, A('D09@yüzde') - .2, A('D09@yüzde') + .7); if (p > 0) { l.save(); l.strokeStyle = '#000'; l.lineWidth = 6; l.beginPath(); l.ellipse(1130, 660, 120, 60, -.1, 0, TAU * p); l.stroke(); l.restore(); }
}, { over: KU2('ODTÜ\'lülerin bildirisi, Milliyet, 4 Mart 1987, s. 9') });
// P48 mutfak: kuru çay süzgeçte sıcak suyla çalkalanır (ODTÜ'nün önerisi)
sahne('P48', 'D10', 'mutfak', 'orta', (B, st) => {
  B.cam(960, 560, 1.06 + st.lt * .01);
  SET.zemin(B, .2, 720, .38);
  SET.demlik(B, 1450, 760, .9, st.t, { ocak: true });
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 8; l.beginPath(); l.arc(800, 640, 120, 0, PI); l.stroke(); l.beginPath(); l.moveTo(920, 640); l.lineTo(1180, 600); l.stroke(); l.restore();
  SET.cayYigini(B, 800, 700, 100, 40, .92, 2);
  B.cayBoya(g => { g.moveTo(780, 760); g.lineTo(820, 760); g.lineTo(830, 1000); g.lineTo(770, 1000); g.closePath(); }, .5, 1, .9 * clamp(Math.sin(st.t * 2) + .4));   // süzülen açık dem
  const k = B.k; k.save(); k.strokeStyle = B.ton(.35); k.lineWidth = 5; k.setLineDash([18, 12]); k.lineDashOffset = -st.t * 80; k.beginPath(); k.moveTo(640, 360); k.quadraticCurveTo(720, 440, 790, 560); k.stroke(); k.restore();   // dökülen sıcak su (kesik çizgi)
  B.save(); B.each(g => { g.translate(520, 300); g.rotate(.5); }); SET.demlik(B, 0, 0, .55, st.t); B.restore();
});
// P49 bildirinin başlığı (gazete sütunu)
sahne('P49', 'D11', 'gazete', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.1 + st.lt * .012);
  SET.pano(B, { tohum: 13 });
  D.kupur(B, 960, 520, { w: 1060, h: 600, a: .015, ust: 'MİLLİYET · 4 MART 1987 · SAYFA 9', manset: '"Radyasyonun dozu küçük gösterildi"', mpx: 80, alinti: 'Çayı demlemeden önce sıcak suyla çalkalayın; çocuklar ve hamile kadınlar çayı azaltsın.', px: 40, ah: 160 });
});
// P50 özel fabrikalar: kamyonlar, paketler; birinin paketinde sayı yazılı
sahne('P50', 'D12', 'ozel', 'genis', (B, st) => {
  B.cam(960 - st.lt * 12, 540, 1.0);
  D.daglar(B, { y: 360, kat: [[.25, 0], [.4, 140]] });
  D.fabrika(B, 520, 720, .7, { d: .5, duman: st.t }); D.fabrika(B, 1500, 760, .8, { d: .45, duman: st.t + 3 });
  for (let i = 0; i < 3; i++) { const x = 200 + ((st.lt * 70 + i * 600) % 2200) - 200; const l = B.l; l.save(); l.fillStyle = '#000'; l.fillRect(x, 860, 300, 120); l.fillRect(x + 300, 900, 90, 80); l.beginPath(); l.arc(x + 60, 990, 30, 0, TAU); l.arc(x + 330, 990, 30, 0, TAU); l.fill(); l.restore(); }
  D.tarihBandi(B, 'EYLÜL 1987', 110, clamp(st.lt / .5));
  D.sayi(B, '≈20.000 TON', 1500, 330, { px: 80, p: ramp(st.t, A('D12@yirmi') - .3, A('D12@yirmi') + .8) });
}, { over: KU2('Milliyet, 30 Eylül 1987, s. 10') });
// P51 bakkal, Aralık 1987: rafta 1986 paketleri; Kurum'un yeni başkanının sözü
sahne('P51', 'D13', 'bakkal', 'orta', (B, st) => {
  B.cam(820 + st.lt * 10, 560, 1.35);
  SET.bakkal(B, st.t, { yil: '1986', tohum: 4 });
  SET.damga(B, '1986', 760, 420, { px: 60, p: ramp(st.t, A('D13@bakkalda') - .1, A('D13@bakkalda') + .2, E.lin) });
  D.kupur(B, 1180, 660, { w: 720, h: 300, a: -.03, alinti: '"Bakkalda ben hâlâ 1986 yılında paketlenmiş çaylar görüyorum."', px: 40, ah: 220, sutun: 0, ust: 'MİLLİYET · 31 ARALIK 1987', p: ramp(st.t, A('D13@bakkalda'), Se('D13')) });
});
