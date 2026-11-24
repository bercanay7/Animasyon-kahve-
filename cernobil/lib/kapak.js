// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir), filmin baskı motoruyla.
// A "BAKAN İÇTİ": basın masasında kaldırılan bardak (açılıştaki P02 kompozisyonu), mikrofonlar, flaş; yüz yok. Tek odak: kehribar dem.
// B "58 BİN TON NEREYE?": alacakaranlıkta naylonla örtülü çuval yığını; yırtık çuvaldan dökülen bakır renkli çay (tek renk).
// Kurallar: tek odak, Bebas ≥ 290 px, figürle yazı arası ≥ 30 px, sağ alt süre rozeti bölgesi (x 1440–1874, y 829–1034) boş. Kapak yazısı başlığın sözcüklerini tekrar etmez.
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
function yazi(c, satirlar, x, y, px, o = {}) {
  c.save(); c.font = `400 ${px}px "Bebas Neue"`; c.textAlign = o.align || 'left'; c.textBaseline = 'alphabetic'; c.letterSpacing = (o.ls ?? 4) + 'px';
  satirlar.forEach((s, i) => { const yy = y + i * px * .86;
    c.fillStyle = 'rgba(236,226,201,.95)'; for (const [dx, dy] of [[0, 9], [7, 7], [-5, 7]]) c.fillText(s, x + dx, yy + dy);
    c.fillStyle = (o.renkler && o.renkler[i]) || '#1E1915'; c.fillText(s, x, yy); });
  c.restore();
}
const KAPAK = {
  A(o) {
    const B = BASKI; B.begin({ per: 8 }); B.cam(960, 540, 1);
    SET.zemin(B, .32, 2000);
    const k = B.k; const g = k.createRadialGradient(700, 420, 0, 700, 420, 520); g.addColorStop(0, '#fff'); g.addColorStop(1, 'rgba(255,255,255,0)'); k.fillStyle = g; k.fillRect(0, 0, W, H);   // flaş arkada
    SET.bust(B, 1180, 1250, 2.6, .1);
    D.mikrofonlar(B, 1050, 1150, 2.0, 5, 9);
    D.bardak(B, 640, 900, 4.4, { buhar: 1.2 });
    SET.el(B, 715, 700, 1.7, .5, { kav: .9 });
    B.compose(ctx);
    if (o.yazi !== false) yazi(ctx, o.satir || ['BAKAN', 'İÇTİ'], 1880, 330, 300, { align: 'right', renkler: ['#1E1915', '#8E2A14'] });
    return cv;
  },
  B(o) {
    const B = BASKI; B.begin({ per: 8 }); B.cam(960, 540, 1);
    SET.zemin(B, .55, 2000);
    D.bulutlar(B, 0, { y: 260, d: .7 });
    D.daglar(B, { y: 420, kat: [[.6, 0], [.72, 150]] });
    const k = B.k; k.save(); k.fillStyle = B.ton(.6); k.fillRect(0, 900, W, 200); k.restore();
    D.yigin(B, 560, 990, 2.3, { kat: 7, gen: 7, naylon: true, t: .5, tohum: 9 });
    // yırtık çuvaldan dökülen çay: tek renk
    D.cuval(B, 1000, 1030, 2.6, { d: .55 });
    B.cayBoya(g => { g.moveTo(1010, 900); g.quadraticCurveTo(1100, 950, 1180, 1030); g.lineTo(940, 1060); g.closePath(); }, 1, .55);
    SET.cayYigini(B, 1060, 1040, 160, 60, .55, 5);
    B.compose(ctx);
    if (o.yazi !== false) yazi(ctx, o.satir || ['58 BİN TON', 'NEREYE?'], 1880, 330, 290, { align: 'right', renkler: ['#1E1915', '#1E1915'] });
    return cv;
  },
};
window.kapak = (v, o = {}) => KAPAK[v](o);
window.READY = false;
(async () => { for (const f of ['400 40px "Bebas Neue"', '400 40px Anton', '700 40px "Courier Prime"']) await document.fonts.load(f, 'ÇĞİÖŞÜçğıöşü'); BASKI.init(); window.READY = true; })();
