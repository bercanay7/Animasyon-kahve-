// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir). Kapak sistemi (kanal/KAPAK_SISTEMI.md, 27 Kasım): yazı solda ve üstte, figür sağda.
// A "ELİNİ UZATTI": filmin ilk karesiyle aynı figür, bu kez sağda ve sola, perdenin aralığındaki ışığa uzanır; el ışığın içinde (tek odak), sarı göz = tek vurgu rengi.
//   Figür belden yukarı (büyük ölçek): tam boyda pelerin ucu küçük resimde etek gibi okunuyordu.
//   Yazı soldaki koyu perdenin üstünde; ışık şeridi yazının sağında başlar (yazıya ışık binmez).
// B "18 YAŞINDA YAZDI": mum ışığında yazan genç kadın sağda, sola bakar; mum solda (alev = vurgu rengi); kâğıtta mürekkep satırları, elinde tüy kalem.
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
    const s0 = o.serit || [770, 1110], fx = o.fx ?? 1580;          // ışık şeridi (perde aralığı) ve yaratığın ayak x'i
    // Fable bulgusu (27 Kasım): tam boy yaratık küçük resimde "yere kadar siyah giysili, uzun saçlı kadın" okunuyordu.
    // Figür büyütülür ve belden aşağısı kadraj dışında kalır (etek gibi okunan pelerin ucu görünmez); omuz, kol, yüz ve göz büyür.
    const R = FENER; R.begin({ isik: { x: o.lx ?? 1000, y: o.ly ?? 450, r: o.lr ?? 600, sic: [1, .9, .72] }, kadraj: { tip: 'kare', x: 960, y: 540, w: 1960, h: 1120, r: 0, yum: 2 }, toz: .5, parlak: o.parlak ?? 1.1 });
    R.cam(960, 540, 1);
    R.gok(-400, -300, 2400, 1400, [[0, '#30406A'], [.6, '#4A5C8A'], [1, '#2C3450']], { firca: 1 });
    R.isikli(g => { g.moveTo(s0[0], 0); g.lineTo(s0[1], 0); g.lineTo(s0[1], 1080); g.lineTo(s0[0], 1080); g.closePath(); }, '#F3D9A0');   // aralanan perdenin ardındaki ışık
    R.yika(g => { g.moveTo(-100, 0); g.lineTo(s0[0], 0); g.lineTo(s0[0], 1080); g.lineTo(-100, 1080); g.closePath(); }, '#8A2E28', { firca: 1, fa: PI / 2 });
    for (let i = 1; i < 8; i++) R.cizgi([[s0[0] - i * 100, 0], [s0[0] - i * 100 - 10, 1080]], 4, { a: .5 });
    const k = FIG.kisi(R, fx, o.fy ?? 1860, o.boy ?? 1500, { tip: 'yaratik', f: -1, govde: o.govde ?? .08, bas: .05, kolO: o.kolO || [1.25, .45], kolA: o.kolA || [-.25, .3], goz: 1, sac: o.sac ?? .3, kenar: 'rgba(255,220,160,.9)', gozRenk: SARI });
    window.EL = k.elO;
    R.compose(ctx, 0);
    if (o.yazi !== false) yazi(ctx, o.satir || ['ELİNİ', 'UZATTI'], o.tx ?? 70, o.ty ?? 330, o.px ?? 300, { renkler: [FILDISI, SARI] });
    return cv;
  },
  B(o) {
    // Fable bulguları (27 Kasım): "YAZDI" görüntüde okunmuyordu (kalem yok, kâğıt 10 px'lik çizgi) ve penceredeki yansıma telefonda
    // ölü bir koyu kutuydu (turuncu göz tek piksel). Pencere çıkarıldı; odak tek küme: alev + yazılı kâğıt + tüy kalem + el.
    const wx = o.wx ?? 1300;
    const R = FENER; R.begin({ isik: { x: o.lx ?? 1000, y: o.ly ?? 620, r: o.lr ?? 640, sic: [1, .86, .6] }, kadraj: { tip: 'kare', x: 960, y: 540, w: 1960, h: 1120, r: 0, yum: 2 }, toz: .5, parlak: o.parlak ?? 1 });
    R.cam(o.cx ?? 1000, o.cy ?? 600, o.z ?? 1.12);
    R.gok(-400, -300, 2400, 1400, [[0, '#4A3424'], [1, '#33241A']], { firca: 1.2 });
    const ty = o.masaY ?? 760, [k0, k1] = o.kagit || [800, 1120];
    // masa: üstten hafif görülen tabla + ön kenar
    R.kara(g => { g.moveTo(560, ty - 46); g.lineTo(1420, ty - 46); g.lineTo(1440, ty); g.lineTo(520, ty); g.closePath(); }, { renk: '#1C120C' });
    R.kara(g => g.rect(520, ty, 920, 30));
    // kâğıt: tablanın üstünde, yüzeyi görünür (eğik dörtgen), üstünde mürekkep satırları
    const kp = [[k0 + 30, ty - 40], [k1 + 10, ty - 42], [k1 + 30, ty - 4], [k0, ty - 2]];
    R.isikli(g => { g.moveTo(...kp[0]); for (const q of kp.slice(1)) g.lineTo(...q); g.closePath(); }, '#F1E4C2');
    const sat = 4, r = rng(5);
    for (let i = 0; i < sat; i++) { const u = (i + .7) / (sat + .4), y0 = lerp(ty - 36, ty - 7, u), xa = lerp(k0 + 28, k0 + 4, u) + 14, xb = lerp(k1 + 8, k1 + 28, u) - 20 - (i === sat - 1 ? (k1 - k0) * .45 : 0);
      const pts = []; for (let x = xa; x <= xb; x += 14) pts.push([x, y0 + Math.sin(x * .37 + i) * 1.6 + (r() - .5) * 1.4]);
      R.cizgi(pts, 2.6, { a: .8, renk: '#2A1A10' }); }
    window.ALEV = DK.mum(R, o.mumx ?? 720, ty - 20, 270, { t: .4 });
    // yazan genç kadın: sağda, sola bakar; ön el kâğıdın üstünde (kalemi tutar), arka el kâğıdın kenarında
    const k = FIG.kisi(R, wx, 1130, 1050, { tip: 'mary', f: -1, bacak: 'otur', govde: o.govde ?? .3, bas: o.bas ?? .42, kolO: o.kolO || [.45, .95], kolA: o.kolA || [.6, .85], kenar: 'rgba(255,210,140,.95)' });
    window.EL = k.elO;
    // tüy kalem: uç kâğıtta, gövde elin içinden yukarı ve geriye (yazanın omzuna doğru); açık krem tüy, ince koyu sap
    const [nx, ny] = o.uc || [k.elO[0] - 26, ty - 22], ka = o.ka ?? -1.4, L = o.kl ?? 270;
    const ux = Math.cos(ka), uy = Math.sin(ka), px = -uy, py = ux, at = (t, w) => [nx + ux * L * t + px * w, ny + uy * L * t + py * w];
    R.cizgi([[nx, ny], at(.42, 0)], 4, { renk: '#1A100A' });
    R.isikli(g => { g.moveTo(...at(.18, 0)); g.bezierCurveTo(...at(.4, 20), ...at(.8, 26), ...at(1, 4)); g.bezierCurveTo(...at(.86, -10), ...at(.5, -14), ...at(.18, 0)); g.closePath(); }, o.tuy || '#E4D6B2');
    R.cizgi([at(.18, 0), at(1, 3)], 2, { renk: 'rgba(60,40,24,.7)' });
    for (let i = 0; i < 5; i++) { const t = .32 + i * .12; R.cizgi([at(t, 1), at(t - .05, 16 - i * 1.5)], 1.4, { renk: 'rgba(60,40,24,.45)' }); }
    R.compose(ctx, .4);
    if (o.yazi !== false) yazi(ctx, o.satir || ['18 YAŞINDA', 'YAZDI'], o.tx ?? 60, o.ty ?? 300, o.px ?? 290, { renkler: [FILDISI, SARI], ls: o.ls ?? -1, ara: o.ara ?? .93 });
    return cv;
  },
};
window.kapak = (v, o = {}) => KAPAK[v](o);
window.READY = false;
(async () => { for (const f of ['400 80px "Bebas Neue"', '700 40px Cinzel']) await document.fonts.load(f, 'AaİıŞşĞğ18'); FENER.init(); window.READY = true; })();
