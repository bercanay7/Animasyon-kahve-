// IV. Ölçülmeyen (F01-F07) ve V. Depo (E01-E16).
'use strict';
const KU3 = (s, o = {}) => (ctx, st) => kunye(ctx, s, st.lt, st.d, o);

// ── IV. ÖLÇÜLMEYEN ──
// P52 vücut sayacı: kurşun kabinde sandalye, oturan siluet; Ocak 1988
sahne('P52', 'F01', 'sayim', 'genis', (B, st) => {
  B.cam(960, 560, 1.02 + st.lt * .012);
  D.lab(B);
  const l = B.l, k = B.k; k.save(); k.fillStyle = B.ton(.78); k.fillRect(560, 260, 520, 640); k.fillStyle = B.ton(.25); k.fillRect(620, 320, 400, 580); k.restore();
  FIG.kisi(B.l, 760, 900, 400, { tip: 'koylu', f: 1, bacak: 'otur', bas: .05, kolO: [.9, .9], kolA: [.8, 1] });
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(560, 260, 520, 640); l.restore();
  D.tarihBandi(B, 'OCAK 1988 · ANKARA', 110, clamp(st.lt / .5));
  D.sayi(B, String(Math.floor(st.lt * 937) % 10000).padStart(4, '0'), 1660, 560, { px: 90 });
}, { tr: { type: 'merdane', dur: .9 } });
// P53 iki sayı (kart): Artvin ↔ Ankara
sahne('P53', 'F02', 'iki_sayi2', 'kart', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .006);
  SET.zemin(B, .05, 2000);
  const l = B.l; l.save(); l.fillStyle = '#000'; l.fillRect(958, 220, 4, 600); l.restore();
  D.sayi(B, 'ARTVİN', 520, 320, { px: 56 }); D.sayi(B, 'ANKARA', 1400, 320, { px: 56 });
  D.sayi(B, '4.693', 520, 580, { px: 190, birim: 'Bq', p: ramp(st.t, A('F02@dört') - .2, A('F02@dört') + 1) });
  D.sayi(B, '687', 1400, 580, { px: 190, birim: 'Bq', p: ramp(st.t, A('F02@ankaradaki') - .2, A('F02@ankaradaki') + .8) });
}, { over: KU3('Milliyet, 27 Ocak 1988, s. 9 (vücut sayımı, Atom Enerjisi Kurumu)') });
// P54 Kurum'un açıklaması: çay bardağı ve "çok çay içmesine"
sahne('P54', 'F03', 'sayim', 'yakin', (B, st) => {
  B.cam(960, 540, 1.04 + st.lt * .014);
  SET.zemin(B, .3, 2000);
  D.bardak(B, 600, 860, 2.6, { buhar: st.t });
  D.kupur(B, 1260, 440, { w: 760, h: 380, a: .02, ust: 'MİLLİYET · 27 OCAK 1988', alinti: 'Kurum yetkilileri fazlalığı "çok çay içmesine" bağladı.', px: 42, ah: 260, sutun: 2, p: ramp(st.t, st.at + .3, Se('F03')) });
});
// P55 harita: Doğu Karadeniz, boş tablo (tarama yok); 1992
sahne('P55', 'F04', 'harita', 'genis', (B, st) => {
  B.cam(1290 + st.lt * 6, 820, 1.7);
  D.harita(B, { kara: .3 });
  const r = rng(6), l = B.l; for (let i = 0; i < 26; i++) { const lon = 36.5 + r() * 5, lat = 40.2 + r() * .7, q = D.hp([lon, lat]); l.save(); l.strokeStyle = '#000'; l.lineWidth = 2; l.beginPath(); l.arc(q[0], q[1], 5, 0, TAU); l.stroke(); l.restore(); }   // köyler: içi boş halka (ölçüm yok)
  B.cam(); SET.daktilo(B, 1200, 200, 560, 280, ['!TARAMA', 'Kişi: ......', 'Doz:  ......'], 1, { px: 34 });
  D.sayi(B, '1992: kanser kaydı başlıyor', 1480, 560, { px: 34, p: ramp(st.t, A('F04@türkiyenin') - .2, A('F04@türkiyenin') + 1.2) });
});
// P56 araştırmalar: dosya yığını, iki rapor kapağı
sahne('P56', 'F05', 'arsiv', 'orta', (B, st) => {
  B.cam(960, 560, 1.02 + st.lt * .01);
  SET.zemin(B, .35, 760, .5);
  SET.daktilo(B, 300, 200, 560, 620, ['!SAĞLIK BAKANLIĞI', '2006', 'Karadeniz Bölgesi', 'kanser araştırması', '', 'Artış yok.'], ramp(st.t, A('F05@sağlık') - .2, A('F05@sağlık') + 2), { px: 32 });
  SET.daktilo(B, 1020, 260, 560, 620, ['!RİZE, 2008', '~100.000 kişi tarandı', 'tiroit kanseri', '', 'Ülke ortalamasından', 'yüksek değil.'], ramp(st.t, A('F05@rizede') - .2, A('F05@rizede') + 2), { px: 32 });
}, { over: KU3('Sağlık Bakanlığı 2006 (CORDIS 2006) · Acar ve ark., ISRN Surgery 2011') });
// P57 çelişen sonuçlar: damgalar
sahne('P57', 'F06', 'arsiv', 'yakin', (B, st) => {
  B.cam(960, 540, 1.1 + st.lt * .01);
  SET.zemin(B, .4, 2000);
  for (let i = 0; i < 3; i++) SET.daktilo(B, 220 + i * 520, 200 + i * 40, 480, 560, ['!ARAŞTIRMA ' + (i + 1), '.......', '.......'], 1, { px: 30 });
  SET.damga(B, 'ARTIŞ VAR', 470, 560, { px: 48, a: -.1, p: ramp(st.t, st.at + .3, st.at + .55, E.lin) });
  SET.damga(B, 'KARAR VERİLEMEZ', 1000, 620, { px: 44, a: .06, p: ramp(st.t, A('F06@karar') - .1, A('F06@karar') + .15, E.lin) });
  D.sayi(B, '?', 960, 200, { px: 150, p: ramp(st.t, A('F06@kesin') - .1, A('F06@kesin') + .5) });
}, { over: KU3('Kocakuşak 2016 · Şahin 2013 · Emral 2003') });
// P58 akşam Karadeniz köyü, yağmur; ışıklı pencereler; insan yüzü yok
sahne('P58', 'F07', 'koy', 'orta', (B, st) => {
  B.cam(960 + st.lt * 6, 540, 1.02);
  SET.zemin(B, .45, 2000);
  D.bulutlar(B, st.t, { y: 200, d: .6, hiz: 20 });
  D.daglar(B, { y: 420, kat: [[.55, 0], [.68, 170]] });
  for (const [x, y, s] of [[420, 860, 3.2], [1000, 780, 2.4], [1500, 880, 3.4]]) { D.ev(B, x, y, s, { d: .85 }); const k = B.k; k.save(); k.fillStyle = '#fff'; k.fillRect(x - 32 * s, y - 52 * s, 14 * s, 18 * s); k.restore(); }
  D.yagmur(B, st.t, { d: .8, n: 300 });
}, { tr: { type: 'fade', dur: .7 } });

// ── V. DEPO ──
// P59 vadi (1988): boş bir dere yatağı, sis
sahne('P59', 'E01', 'vadi', 'genis', (B, st) => {
  B.cam(960 - st.lt * 10, 540, 1.04);
  D.daglar(B, { y: 300, kat: [[.25, 0], [.4, 160], [.55, 330]] });
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); for (let y = 1100; y > 600; y -= 20) l.lineTo(960 + Math.sin(y / 70) * 60 * (y - 500) / 600, y); l.stroke(); l.restore();
  D.tarihBandi(B, '1988', 110, clamp(st.lt / .5));
  D.yigin(B, 960, 980, .6, { kat: 3, gen: 5 });
}, { tr: { type: 'merdane', dur: .9 } });
// P60 başlık: valilerin çay savaşı
sahne('P60', 'E02', 'kupur', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.08 + st.lt * .012);
  SET.pano(B, { tohum: 17 });
  D.kupur(B, 960, 500, { w: 1100, h: 600, a: -.015, ust: 'MİLLİYET · 3 ŞUBAT 1988 · SAYFA 3', manset: '"Benim ilim radyasyonlu çaya mezar olamaz"', mpx: 86, sutun: 4 });
});
// P61 fırın, gece: çuvallar ağızdan atılır; saat 04.00
sahne('P61', 'E03', 'firin', 'orta', (B, st) => {
  B.cam(960, 560, 1.02 + st.lt * .01);
  SET.zemin(B, .6, 2000);
  const k = B.k, l = B.l, fl = .5 + .5 * Math.sin(st.t * 9) * Math.sin(st.t * 5.3);
  k.save(); k.fillStyle = '#fff'; k.beginPath(); k.roundRect(760, 520, 420, 260, 30); k.fill(); k.fillStyle = B.ton(.2 + fl * .15); k.beginPath(); k.roundRect(790, 560, 360, 200, 20); k.fill(); k.restore();   // fırın ağzı: ışık kâğıt beyazı
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 8; l.beginPath(); l.roundRect(760, 520, 420, 260, 30); l.stroke(); l.restore();
  const at = ramp(st.t, st.at + .6, st.at + 2.2);
  const kk = FIG.kisi(B.l, 520 + at * 120, 1000, 460, { tip: 'isci', f: 1, govde: .35 + at * .2, bas: .2, kolO: [1.3 - at * .3, .6], kolA: [1.1, .7] });
  D.cuval(B, kk.elO[0] + 40, kk.elO[1] + 30, 1.1, { d: .6 });
  SET.saat(B, 1550, 300, 90, 4.0);
  D.tarihBandi(B, 'AĞUSTOS 1988 · RİZE, TRABZON', 110, clamp(st.lt / .5));
}, { over: KU3('Milliyet, 18 Ağustos 1988, s. 14') });
// P62 valinin sözü
sahne('P62', 'E03@valisi', 'kupur', 'yakin', (B, st) => {
  B.cam(960, 520, 1.04 + st.lt * .01);
  SET.zemin(B, .75, 2000);
  D.kupur(B, 960, 480, { w: 1060, h: 520, a: .02, ust: 'MİLLİYET · 18 AĞUSTOS 1988 · SAYFA 14', alinti: '"Bu durum kamuoyundan gizlenmemeliydi. Gizlilik endişe verir."', px: 52, ah: 240, sutun: 3, p: ramp(st.t, A('E03@bu'), Se('E03')) });
});
// P63 çit: iki kişi bozuk yerden girer (Ekim 1988, Ankara yakınları)
sahne('P63', 'E04', 'cit', 'genis', (B, st) => {
  B.cam(960 + st.lt * 8, 540, 1.0);
  SET.zemin(B, .1, 760, .35);
  D.sera(B, 500, 760, .9, st.t, { tohum: 2 }); D.sera(B, 1500, 760, .9, st.t + 1, { tohum: 5 });
  D.cit(B, -200, W + 200, 900, 1.2, { bozuk: 1000 });
  const yuru = clamp(st.lt / 5), g = HAREKET.yuruyus({ tip: 'yuru' });
  for (let i = 0; i < 2; i++) { const x = 820 + yuru * 360 - i * 140; const ph = HAREKET.poz ? null : null;
    const kk = FIG.kisi(B.l, x, 1020 - yuru * 60, 330, { tip: i ? 'gazeteci' : 'kadin', f: 1, govde: .12, bas: .08, kolO: [.5 + Math.sin(st.t * 4 + i) * .2, .5], kolA: [-.2, .3] });
    if (i) D.kamera(B.l, kk.elO[0], kk.elO[1], kk.s * .5); }
  D.tarihBandi(B, 'EKİM 1988 · ANKARA YAKINLARI', 110, clamp(st.lt / .5));
}, { over: KU3('Milliyet, 17 Ekim 1988, s. 12') });
// P64 seranın içi: kırık camlar, branda dalgalanır, koli açılır: bakır renkli çay
sahne('P64', 'E05', 'sera', 'orta', (B, st) => {
  B.cam(960, 600, 1.2 + st.lt * .01);
  SET.zemin(B, .12, 760, .3);
  D.sera(B, 960, 900, 2.0, st.t, { tohum: 2 });
  const ac = ramp(st.t, A('E05@kolileri'), A('E05@kolileri') + 1);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.45); k.fillRect(820, 760, 280, 160); k.restore(); l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(820, 760, 280, 160); l.beginPath(); l.moveTo(820, 760); l.lineTo(820 - ac * 80, 700); l.moveTo(1100, 760); l.lineTo(1100 + ac * 80, 700); l.stroke(); l.restore();
  if (ac > .3) { SET.paket(B, 910, 770, .8, { yil: '1986' }); SET.paket(B, 1010, 770, .8, { yil: '1986' }); }
  const r = rng(9); l.save(); l.strokeStyle = '#000'; l.lineWidth = 2; for (let i = 0; i < 14; i++) { const x = 300 + r() * 1300, y = 940 + r() * 80; l.beginPath(); l.moveTo(x, y); l.lineTo(x + 20 + r() * 30, y - 6 - r() * 10); l.lineTo(x + 40, y + 4); l.stroke(); } l.restore();   // yerde kırık cam
});
// P65 Rize'de depolar: duvarlardan sızan koyu sıvı (Nisan 1989)
sahne('P65', 'E06', 'depo2', 'genis', (B, st) => {
  B.cam(960 + st.lt * 8, 560, 1.0);
  SET.zemin(B, .15, 720, .4);
  const k = B.k, l = B.l;
  for (let i = 0; i < 3; i++) { const x = 220 + i * 560; k.save(); k.fillStyle = B.ton(.45); k.fillRect(x, 420, 480, 320); k.fillStyle = B.ton(.7); k.beginPath(); k.moveTo(x - 20, 420); k.lineTo(x + 240, 330); k.lineTo(x + 500, 420); k.closePath(); k.fill(); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.strokeRect(x, 420, 480, 320); l.fillStyle = '#000'; l.fillRect(x + 190, 560, 100, 180); l.restore();
    for (let j = 0; j < 3; j++) { const sx = x + 50 + j * (j === 1 ? 300 : 120), L = 50 + ((st.lt * 10 + j * 30 + i * 20) % 90); k.save(); k.fillStyle = B.ton(.9); k.beginPath(); k.moveTo(sx - 14, 650); k.quadraticCurveTo(sx - 6, 650 + L * .5, sx - 10, 650 + L); k.quadraticCurveTo(sx, 660 + L, sx + 12, 650 + L); k.quadraticCurveTo(sx + 6, 650 + L * .5, sx + 14, 650); k.closePath(); k.fill(); k.beginPath(); k.ellipse(sx, 744, 40 + L * .3, 9, 0, 0, TAU); k.fill(); k.restore(); } }   // duvardan sızan koyu leke ve dipte birikinti
  D.tarihBandi(B, 'NİSAN 1989 · RİZE', 110, clamp(st.lt / .5));
}, { over: KU3('Milliyet, 22 Nisan 1989, s. 3') });
// P66 açıkta istif: tahtalar, naylon rüzgârda
sahne('P66', 'E07', 'acik', 'orta', (B, st) => {
  B.cam(960, 600, 1.06 + st.lt * .008);
  D.bulutlar(B, st.t, { y: 160, d: .35 });
  D.daglar(B, { y: 380, kat: [[.25, 0], [.38, 150]] });
  const k = B.k; k.save(); k.fillStyle = B.ton(.55); k.fillRect(200, 930, 1520, 26); k.restore();
  D.yigin(B, 960, 930, 1.15, { kat: 6, gen: 12, naylon: true, t: st.t });
  D.fabrika(B, 1650, 760, .5, { d: .4 });
}, { over: KU3('Milliyet, 25 Haziran 1989, s. 10') });
// P67 fabrika bahçesi, alacakaranlık: çukur, çuvallar indirilir (Aralık 1989)
sahne('P67', 'E08', 'bahce', 'genis', (B, st) => {
  B.cam(960 - st.lt * 6, 540, 1.0);
  SET.zemin(B, .45, 640, .55);
  D.fabrika(B, 1300, 640, .9, { d: .7 });
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.9); k.beginPath(); k.ellipse(760, 880, 420, 90, 0, 0, TAU); k.fill(); k.restore();
  const in_ = ramp(st.t, st.at + .5, st.at + 4);
  for (let i = 0; i < 4; i++) D.cuval(B, 560 + i * 130, 860 + in_ * 40 * (i % 2 ? 1 : .6), 1.1, { d: .55 });
  FIG.kisi(B.l, 1180, 1000, 420, { tip: 'isci', f: -1, govde: .4, bas: .3, kolO: [1.2, .5], kolA: [1, .6] });
  D.tarihBandi(B, 'ARALIK 1989', 110, clamp(st.lt / .5));
  D.sayi(B, '25.000 TON', 600, 330, { px: 100, p: ramp(st.t, A('E08@yirmi') - .2, A('E08@yirmi') + 1) });
}, { over: KU3('Milliyet, 25 Aralık 1989, s. 3 ve 12 (ANKA)'), tr: { type: 'merdane', dur: .9 } });
// P68 kürekle toprak; çuvalın ağzındaki çay rengi söner
sahne('P68', 'E09', 'bahce', 'yakin', (B, st) => {
  B.cam(960, 600, 1.08 + st.lt * .01);
  SET.zemin(B, .5, 2000);
  const son = ramp(st.t, st.at + 1, Se('E09'));
  SET.gomu(B, 960, 620, 1600, 600, son, { n: 6 });
  const kx = 1300 + Math.sin(st.t * 2.4) * 60, l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 14; l.beginPath(); l.moveTo(kx + 160, 120); l.lineTo(kx, 560); l.stroke(); l.beginPath(); l.ellipse(kx - 10, 590, 70, 40, -.4, 0, TAU); l.fill(); l.restore();
  D.kupur(B, 560, 300, { w: 760, h: 300, a: -.02, alinti: '"Killi toprağa gömülen çaylar çevreye zarar vermez."', px: 40, ah: 200, sutun: 0, ust: 'MİLLİYET · 25 ARALIK 1989', p: ramp(st.t, A('E09@killi'), Se('E09')) });
});
// P69 pano: iğnelenmiş kupür ile çukurun fotoğrafı yan yana (hüküm izleyicide)
sahne('P69', 'E10', 'pano', 'orta', (B, st) => {
  B.cam(960 - st.lt * 10, 540, 1.0 + st.lt * .01);
  SET.pano(B, { tohum: 9 });
  D.kupur(B, 620, 480, { w: 820, h: 420, a: -.04, alinti: '"...tüm çayı imha eder..."', px: 56, ah: 200, sutun: 2, ust: 'MİLLİYET · 9 ARALIK 1986 · SAYFA 7' });
  SET.igne(B, 300, 300, 1.3);
  // fotoğraf: çukur ve çuvallar (tram ton), beyaz kenarlı
  const k = B.k; k.save(); k.translate(1360, 520); k.rotate(.05); k.fillStyle = '#fff'; k.fillRect(-330, -250, 660, 500); k.fillStyle = B.ton(.5); k.fillRect(-300, -220, 600, 420); k.fillStyle = B.ton(.85); k.beginPath(); k.ellipse(0, 60, 220, 60, 0, 0, TAU); k.fill(); k.restore();
  SET.igne(B, 1360, 300, 1.3);
  D.sayi(B, 'ARALIK 1989', 1360, 830, { px: 40 });
});
// P70 Of, Mart 1990: karın erimesi, toprakta koyu leke; köylüler bakar
sahne('P70', 'E11', 'of', 'genis', (B, st) => {
  B.cam(960 + st.lt * 6, 540, 1.0);
  D.daglar(B, { y: 320, kat: [[.15, 0], [.3, 140]] });
  const k = B.k; k.save(); k.fillStyle = B.ton(.25); k.fillRect(-300, 640, W + 600, 600); k.restore();
  D.fabrika(B, 1450, 640, .7, { d: .5 });
  const yay = ramp(st.t, A('E11@sızıntı') - 1, A('E11@sızıntı') + 1);
  k.save(); k.fillStyle = B.ton(.85); k.beginPath(); for (let a = 0; a <= TAU + .01; a += .2) { const rr = (160 + 70 * noise1(a * 3, 4)) * (.4 + yay * .6); k.lineTo(820 + Math.cos(a) * rr * 1.8, 860 + Math.sin(a) * rr * .45); } k.closePath(); k.fill(); k.restore();
  const r = rng(3); k.save(); k.fillStyle = '#fff'; for (let i = 0; i < 40; i++) { k.beginPath(); k.ellipse(r() * W, 680 + r() * 360, 30 + r() * 60, 8 + r() * 10, 0, 0, TAU); k.fill(); } k.restore();   // kar lekeleri
  for (let i = 0; i < 3; i++) FIG.kisi(B.l, 260 + i * 120, 1040 - i * 20, 330 - i * 20, { tip: i === 1 ? 'kadin' : 'koylu', f: 1, govde: .1, bas: .3, kolO: [.15, .3], kolA: [.1, .3] });
  D.tarihBandi(B, 'MART 1990 · TRABZON', 110, clamp(st.lt / .5));
}, { over: KU3('Milliyet, 31 Mart 1990, s. 12') });
// P71 Kurum raporu: "sızıntıya rastlanmamıştır"
sahne('P71', 'E12', 'rapor2', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.06 + st.lt * .012);
  SET.zemin(B, .3, 2000);
  SET.daktilo(B, 440, 140, 1040, 760, ['!ATOM ENERJİSİ KURUMU', 'Toprak ve su örnekleri', '', 'Sonuç: herhangi bir sızıntıya rastlanmamıştır.'], ramp(st.t, st.at, Se('E12')));
});
// P72 iki köylü yan yana: biri raporu tutar, öbürü lekeye bakar; sözleri kupürde
sahne('P72', 'E13', 'of', 'orta', (B, st) => {
  B.cam(960, 600, 1.15 + st.lt * .01);
  SET.zemin(B, .2, 700, .3);
  const k = B.k; k.save(); k.fillStyle = B.ton(.85); k.beginPath(); k.ellipse(1300, 930, 420, 70, 0, 0, TAU); k.fill(); k.restore();
  const a = FIG.kisi(B.l, 640, 1020, 520, { tip: 'koylu', f: 1, govde: .05, bas: .25, kolO: [1.05, .9], kolA: [.2, .3] });
  const l = B.l; l.save(); l.fillStyle = '#fff'; l.translate(a.elO[0] + 20, a.elO[1] - 30); l.rotate(-.2); l.fillRect(-10, -50, 90, 110); l.restore(); l.save(); l.strokeStyle = '#000'; l.lineWidth = 2; l.translate(a.elO[0] + 20, a.elO[1] - 30); l.rotate(-.2); l.strokeRect(-10, -50, 90, 110); l.restore();
  FIG.kisi(B.l, 900, 1030, 500, { tip: 'koylu', f: 1, govde: .2, bas: .45 + Math.sin(st.t) * .03, kolO: [.15, .3], kolA: [.2, .4] });
  D.kupur(B, 1320, 360, { w: 820, h: 400, a: .02, alinti: '"TAEK\'in raporuna mı, yoksa kendi gözlerimize mi inanalım?"', px: 50, ah: 280, sutun: 2, ust: 'MİLLİYET · 31 MART 1990', p: ramp(st.t, st.at + .5, Se('E13')) });
});
// P73 hesap defteri (kart): 58.070 = 35.456 + 22.614
sahne('P73', 'E14', 'hesap', 'kart', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .006);
  SET.zemin(B, .05, 2000);
  D.sayi(B, '58.070 TON', 960, 330, { px: 120, p: ramp(st.t, A('E14@elli') - .2, A('E14@elli') + .8) });
  SET.cubuklar(B, 560, 820, 800, 300, [['İMHA', .61, .7], ['DEPODA', .39, .4]], ramp(st.t, A('E14@otuz') - .3, A('E14@yirmi') + .6));
  D.tarihBandi(B, 'HAZİRAN 1990', 110, clamp(st.lt / .5));
}, { over: KU3('Milliyet, 11 Haziran 1990, s. 15 (35.456 + 22.614)') });
// P74 İç Anadolu'da satın alınmış arazi: kazık ve şerit, "izin yok"
sahne('P74', 'E15', 'arazi', 'genis', (B, st) => {
  B.cam(960 - st.lt * 8, 560, 1.0);
  SET.zemin(B, .06, 600, .2);
  const k = B.k; k.save(); k.fillStyle = B.ton(.3); k.beginPath(); k.moveTo(-200, 620); for (let x = -200; x < W + 200; x += 40) k.lineTo(x, 600 - 40 * fbm1(x / 400, 2, 3)); k.lineTo(W + 200, 640); k.closePath(); k.fill(); k.restore();
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 6; for (let i = 0; i < 4; i++) { const x = 600 + i * 240; l.beginPath(); l.moveTo(x, 900); l.lineTo(x, 760); l.stroke(); } l.lineWidth = 2; l.setLineDash([14, 10]); l.beginPath(); l.moveTo(600, 790); l.lineTo(1320, 790); l.stroke(); l.restore();
  SET.damga(B, 'İZİN YOK', 960, 520, { px: 70, p: ramp(st.t, A('E15@valisi') - .1, A('E15@valisi') + .15, E.lin) });
  D.kupur(B, 1440, 300, { w: 700, h: 260, a: -.02, alinti: '"Bu çayları yurt dışına gömecek halimiz yok ya."', px: 40, ah: 180, sutun: 0, ust: 'MİLLİYET · 9 OCAK 1993', p: ramp(st.t, A('E15@bu'), Se('E15')) });
  D.tarihBandi(B, 'OCAK 1993', 110, clamp(st.lt / .5));
});
// P75 arşiv çekmecesi: 1993'ten sonra boş dosya; gölgede tek çuval
sahne('P75', 'E16', 'arsiv2', 'yakin', (B, st) => {
  B.cam(960, 560, 1.04 + st.lt * .02);
  SET.zemin(B, .55, 2000);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.35); k.fillRect(360, 360, 1200, 560); k.fillStyle = '#fff'; for (let i = 0; i < 8; i++) k.fillRect(400 + i * 140, 300 - (i === 7 ? 0 : 20), 120, 200); k.restore();
  l.save(); l.fillStyle = '#000'; l.font = FONT.daktilo(28, 700); l.textAlign = 'center'; ['1986', '1987', '1988', '1989', '1990', '1991', '1992', '1993 →'].forEach((s, i) => l.fillText(s, 460 + i * 140, 340)); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(360, 360, 1200, 560); l.restore();
  const p = ramp(st.t, st.at + 1, st.at + 3); k.save(); k.fillStyle = '#fff'; k.fillRect(1380, 300 - p * 120, 120, 200); k.restore(); l.save(); l.strokeStyle = '#000'; l.lineWidth = 2; l.strokeRect(1380, 300 - p * 120, 120, 200); l.restore();   // son dosya çekilir: içi boş
});
