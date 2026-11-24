// VI. Bugün (G01-G10) ve bitiş ekranı.
'use strict';
const KU4 = (s, o = {}) => (ctx, st) => kunye(ctx, s, st.lt, st.d, o);

// P76 1992: eski cumhurbaşkanının sözü (yalnız söz, başlık değil)
sahne('P76', 'G01', 'kupur', 'ayrinti', (B, st) => {
  B.cam(960, 520, 1.06 + st.lt * .012);
  SET.pano(B, { tohum: 21 });
  D.kupur(B, 960, 480, { w: 1100, h: 560, a: .015, ust: 'MİLLİYET · 24 ARALIK 1992 · SAYFA 12', alinti: '"Bilim adamları tehlike yok deyince biz de çay içmiştik."', px: 60, ah: 260, sutun: 4, p: ramp(st.t, A('G01@bilim'), Se('G01')) });
}, { tr: { type: 'merdane', dur: .9 } });
// P77 zincir: dört bardak sırayla (Kurum → bakan → cumhurbaşkanı → halk); sonuncusu bir ev masasında
sahne('P77', 'G02', 'zincir', 'orta', (B, st) => {
  B.cam(800 + st.lt * 60, 560, 1.0);
  SET.zemin(B, .1, 760, .25);
  const etik = ['ÖLÇÜM', 'BAKAN', 'CUMHURBAŞKANI', 'HALK'];
  for (let i = 0; i < 4; i++) { const x = 360 + i * 480, p = ramp(st.t, st.at + i * .9, st.at + i * .9 + .6);
    if (p <= 0) continue; D.bardak(B, x, 820, 1.8, { buhar: i === 3 ? st.t : null, dolu: .85 * p });
    D.sayi(B, etik[i], x, 420, { px: 40, p }); if (i < 3) { const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.globalAlpha = p; l.beginPath(); l.moveTo(x + 110, 700); l.lineTo(x + 370, 700); l.stroke(); l.beginPath(); l.moveTo(x + 350, 685); l.lineTo(x + 370, 700); l.lineTo(x + 350, 715); l.stroke(); l.restore(); } }
});
// P78 2007, Rize: kıyıda boş arsa, inşaat panosu ve vinç; kesitte toprağın altında çuvallar (renk sönük)
sahne('P78', 'G03', 'otel', 'genis', (B, st) => {
  B.cam(960 + st.lt * 6, 520, 1.0);
  const k = B.k; k.save(); k.fillStyle = B.ton(.06); k.fillRect(-300, -300, W + 600, 900); k.fillStyle = B.ton(.12); k.fillRect(-300, 380, W + 600, 140); k.restore();   // deniz
  SET.gomu(B, 960, 620, W + 400, 520, 1, { n: 9 });
  const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 8; l.beginPath(); l.moveTo(1500, 620); l.lineTo(1500, 120); l.lineTo(1100, 120); l.stroke(); l.lineWidth = 3; l.beginPath(); l.moveTo(1180, 120); l.lineTo(1180, 300 + Math.sin(st.t) * 10); l.stroke(); l.restore();   // vinç, boş kanca
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
  k.save(); k.fillStyle = '#fff'; k.fillRect(360, 420, 220, 280); k.restore(); B.cayBoya(g => g.rect(372, 480, 196, 214), 1, .9);
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
  const k = B.k, l = B.l; k.save(); k.fillStyle = '#fff'; k.fillRect(880, 470, 200, 230); k.restore(); B.cayBoya(g => g.rect(892, 520, 176, 174), 1, .9);
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(880, 470, 200, 230); l.font = FONT.daktilo(32, 700); l.textAlign = 'center'; l.fillStyle = '#000'; l.fillText('1986', 980, 450); l.restore();
});
// P83 bugün: masada bir bardak, sayı 39 ↔ 600
sahne('P83', 'G08', 'bugun', 'orta', (B, st) => {
  B.cam(960, 560, 1.0 + st.lt * .01);
  SET.zemin(B, .06, 740, .16);
  D.bardak(B, 760, 880, 2.6, { buhar: st.t, kasik: true });
  D.sayi(B, '39', 1360, 520, { px: 200, birim: 'Bq/kg', p: ramp(st.t, A('G08@otuz') - .2, A('G08@otuz') + .8) });
  D.sayi(B, 'sınır 600', 1360, 680, { px: 56, p: ramp(st.t, A('G08@altı') - .2, A('G08@altı') + .6) });
  D.tarihBandi(B, '2017', 110, clamp(st.lt / .5));
}, { over: KU4('Ağuş (TAEK), Karaelmas Fen ve Mühendislik Dergisi, 2017') });
// P84 kapak A'nın halkası: el bardağı kaldırır (açılıştaki kompozisyon), ama flaş yok, mikrofon yok
sahne('P84', 'G09', 'bugun', 'yakin', (B, st) => {
  B.cam(980, 560, 1.06 + st.lt * .008);
  SET.zemin(B, .2, 2000);
  const kalk = E.io3(clamp(st.lt / 3)), y = 900 - kalk * 90;
  D.bardak(B, 880, y, 3.2, { buhar: st.t });
  SET.el(B, 940, y - 140, 1.25, .5, { kav: .9 });
});
// P85 izleyicinin bardağı: dem yüzeyi yukarıdan; bitiş ekranı (son 20 sn)
sahne('P85', 'G10', 'bugun', 'ayrinti', (B, st) => {
  B.cam(960, 540, 1 + Math.min(st.lt, 8) * .01);
  SET.zemin(B, .1, 2000);
  B.cayBoya(g => g.arc(960, 470, 300, 0, TAU), 1, 1);
  const k = B.k, l = B.l; k.save(); k.fillStyle = B.ton(.25); k.beginPath(); k.arc(960, 470, 300, 0, TAU); k.fill(); k.restore();
  l.save(); l.strokeStyle = '#000'; l.lineWidth = 8; l.beginPath(); l.arc(960, 470, 300, 0, TAU); l.stroke(); l.lineWidth = 3; l.beginPath(); l.arc(960, 470, 380, 0, TAU); l.stroke();
  l.lineWidth = 2; for (let i = 1; i < 4; i++) { const r = ((st.lt * .2 + i / 4) % 1); l.globalAlpha = 1 - r; l.beginPath(); l.arc(960, 470, 290 * r, 0, TAU); l.stroke(); } l.restore();
  // bitiş ekranı: son anın içinde kanal adı
  const p = ramp(st.t, Se('G10') + .5, Se('G10') + 1.5); if (p > 0) { l.save(); l.globalAlpha = p; l.fillStyle = '#000'; l.font = FONT.manset(64); l.textAlign = 'center'; l.fillText('ZAMAN KURYESİ', 960, 790); l.restore(); }
});
