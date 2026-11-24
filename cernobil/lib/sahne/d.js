// VI. Bugün (G01-G10) ve bitiş ekranı.
'use strict';
const KU4 = (s, o = {}) => (ctx, st) => kunye(ctx, s, st.lt, st.d, o);

// P76 1992: eski cumhurbaşkanının sözü (yalnız söz, başlık değil)
sahne('P76', 'G01', 'kupur', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.06 + st.lt * .012);
  SET.pano(B, { tohum: 21 });
  D.kupur(B, 960, 480, { w: 1100, h: 560, a: .015, ust: 'MİLLİYET · 24 ARALIK 1992 · SAYFA 12', alinti: '"Bilim adamları tehlike yok deyince biz de çay içmiştik."', px: 60, ah: 260, sutun: 4, p: ramp(st.t, st.at + .5, Se('G01')) });
}, { tr: { type: 'merdane', dur: .9 } });
// P77 zincir: dört bardak sırayla (Kurum → bakan → cumhurbaşkanı → halk); sonuncusu bir ev masasında
sahne('P77', 'G02', 'zincir', 'orta', (B, st) => {
  B.cam(800 + st.lt * 60, 560, 1.0);
  SET.zemin(B, .1, 760, .25);
  const etik = ['ÖLÇÜM', 'HÜKÜMET', 'CUMHURBAŞKANI', 'HALK'];
  for (let i = 0; i < 4; i++) { const x = 360 + i * 480, p = ramp(st.t, st.at + i * .9, st.at + i * .9 + .6);
    if (p <= 0) continue; D.bardak(B, x, 820, 1.8, { buhar: i === 3 ? st.t : null, dolu: .85 * p });
    D.sayi(B, etik[i], x, 420, { px: 40, p }); if (i < 3) { const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.globalAlpha = p; l.beginPath(); l.moveTo(x + 110, 700); l.lineTo(x + 370, 700); l.stroke(); l.beginPath(); l.moveTo(x + 350, 685); l.lineTo(x + 370, 700); l.lineTo(x + 350, 715); l.stroke(); l.restore(); } }
});
// P78 2007, Rize: kıyıda boş arsa, inşaat panosu ve vinç; kesitte toprağın altında çuvallar (renk sönük)
sahne('P78', 'G03', 'otel', 'genis', (B, st) => {
  B.cam(960 + st.lt * 6, 520, 1.0);
  const k = B.k; k.save(); k.fillStyle = B.ton(.06); k.fillRect(-300, -300, W + 600, 900); k.fillStyle = B.ton(.12); k.fillRect(-300, 380, W + 600, 140); k.restore();   // deniz
  SET.gomu(B, 960, 620, W + 400, 520, 1, { n: 9 });
  D.ev(B, 1500, 600, 2.2, { d: .5 }); D.ev(B, 1720, 590, 1.6, { d: .55 });   // kıyıda binalar (vinç yok: darağacı okuması)
  SET.daktilo(B, 300, 300, 420, 240, ['!PROJE', '5 yıldızlı otel'], 1, { px: 30 });
  D.tarihBandi(B, '2007 · RİZE', 110, clamp(st.lt / .5));
}, { over: KU4('Milliyet, 11 Kasım 2007, s. 17') });
// P79 pano üstünde İPTAL damgası
sahne('P79', 'G04', 'otel', 'yakin', (B, st) => {
  B.cam(600, 520, 1.6 + st.lt * .01);
  SET.zemin(B, .12, 620, .4);
  SET.daktilo(B, 300, 300, 600, 340, ['!PROJE', '5 yıldızlı otel', 'Rize Serbest Bölge arazisi'], 1, { px: 30 });
  SET.damga(B, 'VAZGEÇİLDİ', 600, 520, { px: 60, p: ramp(st.t, A('G04@vazgeçiyorlar') - .1, A('G04@vazgeçiyorlar') + .15, E.lin) });
});
// P80 laboratuvar: "1986" etiketli kavanozda çay — renk geri gelir; karıştırılır, kaplara dağıtılır
sahne('P80', 'G05', 'lab', 'genis', (B, st) => {
  B.cam(960 + st.lt * 6, 540, 1.0);
  D.lab(B);
  const k = B.k, l = B.l, mix = ramp(st.t, A('G05@karıştırıp') - .2, A('G05@karıştırıp') + 1.5);
  // kavanoz
  k.save(); k.fillStyle = '#fff'; k.fillRect(360, 420, 220, 280); k.restore(); B.cayBoya(g => g.rect(372, 480, 196, 214), 1, .9); { const r = rng(5); k.save(); k.fillStyle = B.ton(.6); for (let i = 0; i < 120; i++) { k.beginPath(); k.ellipse(375 + r() * 190, 485 + r() * 205, 7, 3, r() * PI, 0, TAU); k.fill(); } k.restore(); B.l.fillStyle = '#000'; B.l.fillRect(352, 404, 236, 22); }   // kuru yaprak dokusu, kapak
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(360, 420, 220, 280); l.font = FONT.daktilo(36, 700); l.textAlign = 'center'; l.fillStyle = '#000'; l.fillText('1986', 470, 400); l.restore();
  // 20 küçük kap (laboratuvarlara giden)
  const n = Math.floor(ramp(st.t, A('G05@yirmi') - .5, A('G05@yirmi') + 1.5) * 20);
  for (let i = 0; i < n; i++) { const x = 720 + (i % 10) * 70, y = 620 + Math.floor(i / 10) * 90; k.save(); k.fillStyle = '#fff'; k.fillRect(x, y, 50, 64); k.restore(); B.cayBoya(g => g.rect(x + 4, y + 20, 42, 40), 1, .9 * mix + .3); l.save(); l.strokeStyle = '#000'; l.lineWidth = 2; l.strokeRect(x, y, 50, 64); l.restore(); }
  D.sayi(B, '8 kg', 470, 780, { px: 56, p: ramp(st.t, A('G05@sekiz') - .2, A('G05@sekiz') + .6) });
}, { over: KU4('Yeltepe ve ark. (TAEK), Applied Radiation and Isotopes, 2018') });
// P81 sonuç grafiği (kart)
sahne('P81', 'G06', 'lab', 'kart', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .006);
  SET.zemin(B, .05, 2000);
  D.sayi(B, '19 laboratuvar · 41 sonuç', 960, 250, { px: 56 });
  SET.cubuklar(B, 460, 820, 1000, 420, [['KABUL', .49, .5], ['UYARILI', .19, .7], ['KABUL EDİLMEZ', .32, .9]], ramp(st.t, st.at + .5, Se('G06')));
});
// P82 kavanoz dedektörün önünde: tek renkli nesne
sahne('P82', 'G07', 'lab', 'ayrinti', (B, st) => {
  B.cam(1000, 560, 1.4 + st.lt * .02);
  D.lab(B);
  const k = B.k, l = B.l; k.save(); k.fillStyle = '#fff'; k.fillRect(880, 470, 200, 230); k.restore(); B.cayBoya(g => g.rect(892, 520, 176, 174), 1, .9); { const r = rng(6); k.save(); k.fillStyle = B.ton(.6); for (let i = 0; i < 100; i++) { k.beginPath(); k.ellipse(895 + r() * 170, 525 + r() * 165, 7, 3, r() * PI, 0, TAU); k.fill(); } k.restore(); l.fillStyle = '#000'; l.fillRect(872, 455, 216, 20); }
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(880, 470, 200, 230); l.font = FONT.daktilo(32, 700); l.textAlign = 'center'; l.fillStyle = '#000'; l.fillText('1986', 980, 450); l.restore();
});
// P83 bugün: masada bir bardak, sayı 39 ↔ 600
sahne('P83', 'G08', 'bugun', 'orta', (B, st) => {
  { const z = E.io2(ramp(st.t, st.at + .2, st.end - .2)); B.cam(lerp(900, 1000, z), lerp(520, 620, z), lerp(.95, 1.35, z)); }   // bardağa ve sayıya yaklaşma (donma: 5,1 sn)
  SET.zemin(B, .06, 740, .16);
  D.bardak(B, 760, 880, 2.6, { buhar: st.t, kasik: true });
  D.sayi(B, '39', 1360, 520, { px: 200, birim: 'Bq/kg', p: ramp(st.t, A('G08@otuz') - .2, A('G08@otuz') + .8) });
  D.sayi(B, 'sınır 600', 1360, 680, { px: 56, p: ramp(st.t, A('G08@altı') - .2, A('G08@altı') + .6) });
  D.tarihBandi(B, '2017', 110, clamp(st.lt / .5));
}, { over: KU4('Ağuş (TAEK), Karaelmas Fen ve Mühendislik Dergisi, 2017', { y: 220 }) });
// P84 kapak A'nın halkası: el bardağı kaldırır (açılıştaki kompozisyon), ama flaş yok, mikrofon yok
sahne('P84', 'G09', 'bugun', 'yakin', (B, st) => {
  B.cam(980, 560, 1.06 + st.lt * .008);
  SET.zemin(B, .2, 2000);
  // bardak kalkar ("içebilir"), iner ("söylemez"); sonra üç soru sırayla dizgiyle basılır
  const kalk = ramp(st.t, st.at + .3, A('G09@içebilir'), E.io3) * (1 - ramp(st.t, A('G09@söylemez') - .3, A('G09@söylemez') + .6, E.io3)), y = 900 - kalk * 110;
  D.bardak(B, 700, y, 3.2, { buhar: st.t });
  SET.el(B, 760, y - 140, 1.25, .5, { kav: .9 });
  const S3 = [['Sayıyı kim ölçtü?', 'G09@sayıyı'], ['Sana söyledi mi?', 'G09@sana'], ['Geri kalan çaya ne yaptı?', 'G09@geri']];
  S3.forEach(([s, at], i) => D.sayi(B, s, 1120, 360 + i * 150, { px: 54, align: 'left', p: ramp(st.t, A(at) - .2, A(at) + .9) }));
});
// P85 izleyicinin bardağı: dem yüzeyi yukarıdan; bitiş ekranı (son 20 sn)
sahne('P85', 'G10', 'bugun', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1 + Math.min(st.lt, 10) * .008);
  SET.zemin(B, .1, 640, .22);
  D.bardak(B, 820, 760, 3.6, { buhar: st.t, kasik: false });
  // kaşık demde döner (sürekli küçük hareket)
  const a = st.t * 2.2, l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 9; l.lineCap = 'round'; l.beginPath(); l.moveTo(820 + Math.cos(a) * 30, 520); l.lineTo(820 + Math.cos(a) * 60, 360); l.stroke(); l.restore();
  D.sayi(B, '39 Bq/kg', 1380, 560, { px: 90, p: ramp(st.t, A('G10@sayıyı') - .2, A('G10@sayıyı') + .8) });
  D.sayi(B, 'kim ölçtü? · nerede yazıyor?', 1380, 660, { px: 34, p: ramp(st.t, A('G10@sor') - .2, A('G10@sor') + .9) });
  const p = ramp(st.t, Se('G10') + .5, Se('G10') + 1.5); if (p > 0) { l.save(); l.globalAlpha = p; l.fillStyle = '#000'; l.font = FONT.manset(60); l.textAlign = 'center'; l.fillText('ZAMAN KURYESİ', 960, 160); l.restore(); }
});
