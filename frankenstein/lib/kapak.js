// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir). Kapak sistemi (kanal/KAPAK_SISTEMI.md, 27 Kasım): yazı solda ve üstte, figür sağda.
// A "ELİNİ UZATTI": filmin ilk karesiyle aynı figür, bu kez sağda ve sola, perdenin aralığındaki ışığa uzanır; el ışığın içinde (tek odak), sarı göz = tek vurgu rengi.
//   Yazı soldaki koyu perdenin üstünde; ışık şeridi yazının sağında başlar (yazıya ışık binmez).
// B "18 YAŞINDA YAZDI": mum ışığında yazan genç kadın sağda, sola bakar; mum ortada (alev = vurgu rengi); arkasındaki karanlık camda uzun bir siluetin yansıması.
//   Pencere sağ üstte biter (y ≤ 780): sağ alt süre rozeti bölgesi boş kalır.
// Kurallar: tek odak (yazı hariç en parlak yer), Bebas ≥ 290 px fildişi #F3EAD7, tek vurgu kelimesi, figürle yazı arası ≥ 30 px,
// sağ alt süre rozeti bölgesi (x 1440–1874, y 829–1034) önemli içeriksiz. Kapak yazısı başlığın sözcüklerini tekrar etmez. Rozet, çerçeve, şerit yok.
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const FILDISI = '#F3EAD7', SARI = '#F2B53A';   // SARI: yaratığın gözü (A) ve mum alevi (B); kapakta başka renkli nesne yok
function yazi(c, satirlar, x, y, px, o = {}) {
  c.save(); c.font = `400 ${px}px "Bebas Neue"`; c.textAlign = o.align || 'left'; c.textBaseline = 'alphabetic'; c.letterSpacing = (o.ls ?? 4) + 'px';
  const ara = o.ara ?? .88, kutu = [];
  satirlar.forEach((s, i) => { const yy = y + i * px * ara;
    c.fillStyle = 'rgba(10,4,2,.9)'; for (const [dx, dy] of [[0, 10], [7, 8], [-5, 8]]) c.fillText(s, x + dx, yy + dy);
    c.fillStyle = (o.renkler && o.renkler[i]) || o.col || FILDISI; c.fillText(s, x, yy);
    const m = c.measureText(s); kutu.push([x - m.actualBoundingBoxLeft, yy - m.actualBoundingBoxAscent, x + m.actualBoundingBoxRight, yy + m.actualBoundingBoxDescent]); });
  c.restore(); window.YAZI_KUTU = kutu; return kutu;
}
const KAPAK = {
  A(o) {
    const s0 = o.serit || [770, 1110], fx = o.fx ?? 1500;          // ışık şeridi (perde aralığı) ve yaratığın ayak x'i
    const R = FENER; R.begin({ isik: { x: o.lx ?? 1000, y: o.ly ?? 450, r: o.lr ?? 600, sic: [1, .9, .72] }, kadraj: { tip: 'kare', x: 960, y: 540, w: 1960, h: 1120, r: 0, yum: 2 }, toz: .5, parlak: o.parlak ?? 1.1 });
    R.cam(960, 540, 1);
    R.gok(-400, -300, 2400, 1400, [[0, '#30406A'], [.6, '#4A5C8A'], [1, '#2C3450']], { firca: 1 });
    R.isikli(g => { g.moveTo(s0[0], 0); g.lineTo(s0[1], 0); g.lineTo(s0[1], 1080); g.lineTo(s0[0], 1080); g.closePath(); }, '#F3D9A0');   // aralanan perdenin ardındaki ışık
    R.yika(g => { g.moveTo(-100, 0); g.lineTo(s0[0], 0); g.lineTo(s0[0], 1080); g.lineTo(-100, 1080); g.closePath(); }, '#8A2E28', { firca: 1, fa: PI / 2 });
    for (let i = 1; i < 8; i++) R.cizgi([[s0[0] - i * 100, 0], [s0[0] - i * 100 - 10, 1080]], 4, { a: .5 });
    const k = FIG.kisi(R, fx, 1430, 1100, { tip: 'yaratik', f: -1, govde: .08, bas: .05, kolO: [1.25, .45], kolA: [-.25, .3], goz: 1, sac: .3, kenar: 'rgba(255,220,160,.9)', gozRenk: SARI });
    window.EL = k.elO;
    R.compose(ctx, 0);
    if (o.yazi !== false) yazi(ctx, o.satir || ['ELİNİ', 'UZATTI'], o.tx ?? 70, o.ty ?? 330, o.px ?? 300, { renkler: [FILDISI, SARI] });
    return cv;
  },
  B(o) {
    const wx = o.wx ?? 1300, Mx = x => wx - (x - 720);   // eski yerleşim (kadın 720'de, sağa bakar) kadının yeni yeri etrafında aynalanır
    const R = FENER; R.begin({ isik: { x: o.lx ?? 980, y: o.ly ?? 600, r: o.lr ?? 700, sic: [1, .86, .6] }, kadraj: { tip: 'kare', x: 960, y: 540, w: 1960, h: 1120, r: 0, yum: 2 }, toz: .5 });
    R.cam(960, 540, 1);
    R.gok(-400, -300, 2400, 1400, [[0, '#5A3E2A'], [1, '#3A281C']], { firca: 1.2 });
    // karanlık pencere (sağ üst, rozet bölgesinin üstünde biter): camda uzun bir siluetin yansıması (soluk), kadının sırtına bakar
    const [px, py, pw, ph] = o.pen || [1470, 70, 400, 700];
    R.yika(g => g.rect(px, py, pw, ph), '#6F82AE', { firca: 1 });
    R.g.save(); R.g.beginPath(); R.g.rect(px, py, pw, ph); R.g.clip(); FIG.kisi(R, px + pw * (o.yx ?? .75), py + ph + (o.yy ?? 400), 900, { tip: 'yaratik', f: -1, goz: 1, renk: 'rgba(14,9,6,.6)' }); R.g.restore();
    R.kara(g => { g.rect(px - 20, py - 20, pw + 40, 20); g.rect(px - 20, py + ph, pw + 40, 24); g.rect(px - 20, py - 20, 20, ph + 44); g.rect(px + pw, py - 20, 20, ph + 44); g.rect(px + pw / 2 - 7, py - 20, 14, ph + 20); });
    R.kara(g => g.rect(Mx(1500), 760, 900, 30));
    R.isikli(g => { g.moveTo(Mx(860), 758); g.lineTo(Mx(1160), 752); g.lineTo(Mx(1180), 762); g.lineTo(Mx(870), 766); g.closePath(); }, '#F4EAD0');
    FIG.kisi(R, wx, 1130, 1050, { tip: 'mary', f: -1, bacak: 'otur', govde: .25, bas: .32, kolO: [.7, .8], kolA: [.5, .9], kenar: 'rgba(255,210,140,.95)' });
    window.ALEV = DK.mum(R, Mx(o.mumx ?? 1330), 760, 260, { t: .4 });
    R.compose(ctx, .4);
    if (o.yazi !== false) yazi(ctx, o.satir || ['18 YAŞINDA', 'YAZDI'], o.tx ?? 60, o.ty ?? 300, o.px ?? 290, { renkler: [FILDISI, SARI], ls: o.ls ?? -1, ara: o.ara ?? .93 });
    return cv;
  },
};
window.kapak = (v, o = {}) => KAPAK[v](o);
window.READY = false;
(async () => { for (const f of ['400 80px "Bebas Neue"', '700 40px Cinzel']) await document.fonts.load(f, 'AaİıŞşĞğ18'); FENER.init(); window.READY = true; })();
