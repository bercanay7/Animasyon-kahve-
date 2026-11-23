// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir). A "ELİNİ UZATTI": filmin ilk karesiyle aynı figür, uzanan el (tek odak), sarı göz (tek vurgu).
// B "18 YAŞINDA YAZDI": mum ışığında yazan genç kadın; karanlık camda uzun bir siluetin yansıması. Kapak yazısı başlığın sözcüklerini tekrar etmez.
// Kurallar: tek odak (en parlak yer), Bebas ≥ 290 px, figürle yazı arası ≥ 30 px, sağ alt süre rozeti bölgesi (x 1440–1874, y 829–1034) boş.
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
function yazi(c, satirlar, x, y, px, o = {}) {
  c.save(); c.font = `400 ${px}px "Bebas Neue"`; c.textAlign = o.align || 'left'; c.textBaseline = 'alphabetic'; c.letterSpacing = (o.ls ?? 4) + 'px';
  satirlar.forEach((s, i) => { const yy = y + i * px * .88;
    c.fillStyle = 'rgba(10,4,2,.9)'; for (const [dx, dy] of [[0, 10], [7, 8], [-5, 8]]) c.fillText(s, x + dx, yy + dy);
    c.fillStyle = (o.renkler && o.renkler[i]) || o.col || '#F6EAD2'; c.fillText(s, x, yy); });
  c.restore();
}
const KAPAK = {
  A(o) {
    const R = FENER; R.begin({ isik: { x: 1180, y: 640, r: 620, sic: [1, .9, .72] }, kadraj: { tip: 'kare', x: 960, y: 540, w: 1960, h: 1120, r: 0, yum: 2 }, toz: .5, parlak: 1.1 });
    R.cam(960, 540, 1);
    R.gok(-400, -300, 2400, 1400, [[0, '#30406A'], [.6, '#4A5C8A'], [1, '#2C3450']], { firca: 1 });
    R.isikli(g => { g.moveTo(1000, 0); g.lineTo(1400, 0); g.lineTo(1400, 1080); g.lineTo(1000, 1080); g.closePath(); }, '#F3D9A0');   // aralanan perdenin ardındaki ışık
    R.yika(g => { g.moveTo(1400, 0); g.lineTo(2000, 0); g.lineTo(2000, 1080); g.lineTo(1400, 1080); g.closePath(); }, '#8A2E28', { firca: 1, fa: PI / 2 });
    for (let i = 1; i < 6; i++) R.cizgi([[1400 + i * 100, 0], [1400 + i * 100 + 10, 1080]], 4, { a: .5 });
    FIG.kisi(R, 560, 1430, 1100, { tip: 'yaratik', f: 1, govde: .08, bas: .05, kolO: [1.25, .45], kolA: [-.25, .3], goz: 1, sac: .3, kenar: 'rgba(255,220,160,.9)', gozRenk: '#F2B53A' });
    R.compose(ctx, 0);
    if (o.yazi !== false) yazi(ctx, o.satir || ['ELİNİ', 'UZATTI'], 1880, 330, 300, { align: 'right', renkler: ['#F6EAD2', '#F2B53A'] });
    return cv;
  },
  B(o) {
    const R = FENER; R.begin({ isik: { x: 1000, y: 560, r: 700, sic: [1, .86, .6] }, kadraj: { tip: 'kare', x: 960, y: 540, w: 1960, h: 1120, r: 0, yum: 2 }, toz: .5 });
    R.cam(960, 540, 1);
    R.gok(-400, -300, 2400, 1400, [[0, '#5A3E2A'], [1, '#3A281C']], { firca: 1.2 });
    // karanlık pencere: camda uzun bir siluetin yansıması (soluk)
    R.yika(g => g.rect(60, 80, 520, 760), '#6F82AE', { firca: 1 });
    R.g.save(); R.g.beginPath(); R.g.rect(60, 80, 520, 760); R.g.clip(); FIG.kisi(R, 300, 1060, 900, { tip: 'yaratik', f: 1, goz: 1, renk: 'rgba(14,9,6,.6)' }); R.g.restore();
    R.kara(g => { g.rect(40, 60, 560, 20); g.rect(40, 840, 560, 24); g.rect(40, 60, 20, 800); g.rect(580, 60, 20, 800); g.rect(312, 60, 14, 800); });
    R.kara(g => g.rect(600, 760, 900, 30));
    R.isikli(g => { g.moveTo(860, 758); g.lineTo(1160, 752); g.lineTo(1180, 762); g.lineTo(870, 766); g.closePath(); }, '#F4EAD0');
    FIG.kisi(R, 720, 1130, 1050, { tip: 'mary', f: 1, bacak: 'otur', govde: .25, bas: .32, kolO: [1.3, 1.0], kolA: [1.0, 1.2], kenar: 'rgba(255,210,140,.95)' });
    DK.mum(R, 1330, 760, 260, { t: .4 });
    R.compose(ctx, .4);
    if (o.yazi !== false) yazi(ctx, o.satir || ['18 YAŞINDA', 'YAZDI'], 1880, 300, 300, { align: 'right', renkler: ['#F6EAD2', '#F2B53A'] });
    return cv;
  },
};
window.kapak = (v, o = {}) => KAPAK[v](o);
window.READY = false;
(async () => { for (const f of ['400 80px "Bebas Neue"', '700 40px Cinzel']) await document.fonts.load(f, 'AaİıŞşĞğ18'); FENER.init(); window.READY = true; })();
