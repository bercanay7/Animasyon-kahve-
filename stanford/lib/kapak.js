// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir), filmin motoruyla (lib/ekran.js).
// A "RASTGELE SEÇİLDİ": monitör görüntüsünde ¾ duran gardiyan (filmin ilk karesindeki figür), aynalı gözlükte koridorun ışığı. Tek odak: camdaki parıltı. Yüz çizilmez.
// B "BANTTA NE İSTENDİ?": karanlık odada ışık konisinin altında makaralı teyp; tek renk kırmızı kayıt lambası (karenin en parlak noktası).
// Kurallar: tek odak; Bebas ≥ 290 px; figürle yazı arası ≥ 30 px; sağ alt süre rozeti bölgesi (x 1440–1874, y 829–1034) boş; kapak yazısı başlığın sözcüklerini tekrar etmez.
// Hassasiyet: gardiyan Türk polisi/askeri okunmasın (şapka, rütbe, arma yok; haki gömlek yakası yok); iki cam "bembeyaz göz" okunmasın (cam gri, parıltı küçük ve camın içinde).
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
function yazi(c, satirlar, x, y, px, o = {}) {
  c.save(); c.font = `400 ${px}px "Bebas Neue"`; c.textAlign = o.align || 'left'; c.textBaseline = 'alphabetic'; c.letterSpacing = (o.ls ?? 4) + 'px';
  satirlar.forEach((s, i) => { const yy = y + i * px * .9;
    c.fillStyle = o.golge || 'rgba(10,12,13,.85)'; for (const [dx, dy] of [[0, 8], [6, 6], [-4, 6]]) c.fillText(s, x + dx, yy + dy);
    c.fillStyle = (o.renkler && o.renkler[i]) || '#E6DCC4'; c.fillText(s, x, yy); });
  c.restore();
}
// ¾ baş: koyu kütle, kulak, ense, omuz; aynalı gözlük (iki cam, uzak cam dar), camlarda koridor lambalarının yansıması
function ucCeyrek(B, cx, cy, s) {
  const l = B.l; l.save(); l.fillStyle = '#000';
  l.beginPath(); l.moveTo(cx - 560 * s, 1200); l.quadraticCurveTo(cx - 500 * s, cy + 430 * s, cx - 120 * s, cy + 400 * s); l.lineTo(cx + 150 * s, cy + 400 * s); l.quadraticCurveTo(cx + 560 * s, cy + 440 * s, cx + 640 * s, 1200); l.closePath(); l.fill();   // omuzlar
  l.fillRect(cx - 130 * s, cy + 200 * s, 260 * s, 260 * s);   // boyun
  l.beginPath(); l.ellipse(cx, cy, 270 * s, 340 * s, .06, 0, TAU); l.fill();   // baş
  l.beginPath(); l.ellipse(cx + 40 * s, cy + 250 * s, 210 * s, 120 * s, .1, 0, TAU); l.fill();   // çene
  l.beginPath(); l.ellipse(cx - 262 * s, cy + 20 * s, 46 * s, 82 * s, .15, 0, TAU); l.fill(); l.beginPath(); l.ellipse(cx + 262 * s, cy + 30 * s, 34 * s, 74 * s, -.1, 0, TAU); l.fill();   // kulaklar
  // gömlek yakası (koyu gri, açık değil: papaz yakası/beyaz dikdörtgen okunmasın)
  l.fillStyle = '#2E3436'; l.beginPath(); l.moveTo(cx - 140 * s, cy + 390 * s); l.lineTo(cx, cy + 520 * s); l.lineTo(cx - 40 * s, cy + 600 * s); l.lineTo(cx - 230 * s, cy + 430 * s); l.closePath(); l.fill();
  l.beginPath(); l.moveTo(cx + 150 * s, cy + 390 * s); l.lineTo(cx + 10 * s, cy + 520 * s); l.lineTo(cx + 50 * s, cy + 600 * s); l.lineTo(cx + 250 * s, cy + 430 * s); l.closePath(); l.fill(); l.fillStyle = '#000';
  l.beginPath(); l.moveTo(cx - 280 * s, cy - 120 * s); l.quadraticCurveTo(cx - 200 * s, cy - 380 * s, cx + 60 * s, cy - 360 * s); l.quadraticCurveTo(cx + 280 * s, cy - 330 * s, cx + 270 * s, cy - 150 * s); l.lineTo(cx + 200 * s, cy - 200 * s); l.quadraticCurveTo(cx - 40 * s, cy - 260 * s, cx - 230 * s, cy - 60 * s); l.closePath(); l.fill();   // saç
  // gözlük: köprü ve iki cam (yakın cam geniş, uzak cam dar)
  // pilot gözlüğü: iki damla biçimli cam; camda koridor lambalarının parlak yansıması (tek odak)
  const cam = (x, y, w, h, sg) => { const p = new Path2D(); p.moveTo(x - w, y - h * .55); p.quadraticCurveTo(x, y - h * .8, x + w, y - h * .55); p.quadraticCurveTo(x + w * 1.05, y + h * .5, x + sg * w * .2, y + h); p.quadraticCurveTo(x - w * 1.0, y + h * .9, x - w, y - h * .55); p.closePath(); return p; };
  const C = [cam(cx + 115 * s, cy - 30 * s, 118 * s, 84 * s, 1), cam(cx - 118 * s, cy - 34 * s, 92 * s, 80 * s, -1)];
  l.lineWidth = 14 * s; l.strokeStyle = '#000'; l.beginPath(); l.moveTo(cx - 30 * s, cy - 70 * s); l.quadraticCurveTo(cx, cy - 84 * s, cx + 30 * s, cy - 70 * s); l.stroke();
  C.forEach((p, i) => {
    l.fillStyle = '#8C9598'; l.fill(p);
    l.save(); l.clip(p);
    const x0 = i ? cx - 118 * s : cx + 115 * s, y0 = cy - 30 * s;
    l.fillStyle = '#E8EDEE'; for (let j = 0; j < 3; j++) l.fillRect(x0 - 100 * s + j * 70 * s, y0 - 64 * s + j * 10 * s, 52 * s, 18 * s);   // lamba yansımaları
    l.fillStyle = '#FFFFFF'; l.beginPath(); l.ellipse(x0 - 20 * s, y0 - 10 * s, 70 * s, 30 * s, -.4, 0, TAU); l.fill();   // parıltı
    l.restore(); l.lineWidth = 10 * s; l.strokeStyle = '#000'; l.stroke(p);
  });
  l.restore();
}
const KAPAK = {
  A(o) {
    const B = BASKI; B.begin({ mod: 'video', parlak: 1.2 }); B.cam(960, 540, 1);
    D.koridor(B, 0, { vp: [1350, 470], gen: 900, levha: false, isik: 1 });
    ucCeyrek(B, 640, 520, 1.0);
    B.compose(ctx);
    if (o.yazi !== false) yazi(ctx, o.satir || ['RASTGELE', 'SEÇİLDİ'], 1840, 360, 300, { align: 'right', renkler: ['#B3AB96', '#B3AB96'] });
    return cv;
  },
  B(o) {
    const B = BASKI; B.begin({ mod: 'kagit', kuru: .6 }); B.cam(960, 540, 1);
    SET.karanlik(B, .9); SET.koni(B, 640, -200, 160, 1100, 1000, { a: .5, tohum: 3 });
    SET.koni(B, 640, -200, 160, 1100, 1000, { a: 0, tohum: 3 });
    SET.teyp(B, 640, 330, 1.4, 0, { ang: .6, kayit: 1, vu: .55, vuIsik: .35 });
    const lx = 640 + 150 * 1.4, ly = 330 + 305 * 1.4;   // kayıt lambası: büyüt, ışıt (tek odak)
    { const g = B.c, gr = g.createRadialGradient(lx, ly, 0, lx, ly, 110); gr.addColorStop(0, 'rgba(255,255,0,1)'); gr.addColorStop(.3, 'rgba(255,255,0,1)'); gr.addColorStop(1, 'rgba(255,255,0,0)');
      g.save(); g.fillStyle = gr; g.beginPath(); g.arc(lx, ly, 110, 0, TAU); g.fill(); g.restore(); }   // yumuşak ışıma (eş merkezli halka yok: hedef okunmasın)
    B.compose(ctx);
    if (o.yazi !== false) yazi(ctx, o.satir || ['BANTTA NE', 'İSTENDİ?'], 1860, 360, 300, { align: 'right', renkler: ['#CFC6AE', '#CFC6AE'] });
    return cv;
  },
};
window.kapak = (v, o = {}) => KAPAK[v](o);
window.READY = false;
(async () => { for (const f of ['400 40px "Bebas Neue"', '400 40px Anton', '700 40px "Courier Prime"']) await document.fonts.load(f, 'ÇĞİÖŞÜçğıöşü'); BASKI.init(); window.READY = true; })();
