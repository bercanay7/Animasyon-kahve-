// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir), filmin motoruyla (lib/ekran.js).
// Kapak sistemi (kanal/KAPAK_SISTEMI.md, 27 Kasım): yazı solda ve üstte, figür sağda; Bebas fildişi #F3EAD7, tek vurgu kelimesi; zemin bastırılmış; rozet/çerçeve yok.
// A "RASTGELE SEÇİLDİ": monitör görüntüsünde ¾ duran gardiyan (filmin ilk planlarındaki aynalı gözlüklü figür) sağda; sahne eski kapağın aynası (koridor solda).
//   Koridor gölgede (fildişi yazı okunsun); tavan lambaları kısık. Tek odak: camdaki çapraz parıltı (karenin en parlak noktası). Renkli nesne yok: vurgu altın #E2B04F.
// B "BANTTA NE İSTENDİ?": karanlık odada makaralı teyp sağda, ışık teybin yüzüne düşer (koninin tepesi kadraj dışında); tek renk kırmızı kayıt lambası → vurgu kelimesi o kırmızı.
// Kurallar: tek odak; Bebas ≥ 290 px; figürle yazı arası ≥ 30 px; sağ alt süre rozeti bölgesi (x 1440–1874, y 829–1034) boş; kapak yazısı başlığın sözcüklerini tekrar etmez.
// Hassasiyet: gardiyan Türk polisi/askeri okunmasın (şapka, rütbe, arma yok; haki gömlek yakası yok); iki cam "bembeyaz göz" okunmasın (cam gri, parıltı oval değil
//   çapraz şerit: CLAUDE.md Stanford listesi); kayıt lambasının ışıması küçük ve lambanın üstünde (kan lekesi okunmasın).
const FILDISI = '#F3EAD7', ALTIN = '#E2B04F', KIRMIZI = '#B92D22';
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
function yazi(c, satirlar, x, y, px, o = {}) {
  c.save(); c.font = `400 ${px}px "Bebas Neue"`; c.textAlign = o.align || 'left'; c.textBaseline = 'alphabetic'; c.letterSpacing = (o.ls ?? 4) + 'px';
  satirlar.forEach((s, i) => { const yy = y + i * px * (o.lh ?? .9);
    c.fillStyle = o.golge || 'rgba(10,12,13,.85)'; for (const [dx, dy] of [[0, 8], [6, 6], [-4, 6]]) c.fillText(s, x + dx, yy + dy);
    c.fillStyle = (o.renkler && o.renkler[i]) || FILDISI; c.fillText(s, x, yy); });
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
    l.fillStyle = '#B4BCBE'; for (let j = 0; j < 3; j++) l.fillRect(x0 - 100 * s + j * 70 * s, y0 - 64 * s + j * 10 * s, 52 * s, 18 * s);   // lamba yansımaları (sönük)
    l.restore(); l.lineWidth = 10 * s; l.strokeStyle = '#000'; l.stroke(p);
    // camın arkasında ton plakası: cam orta gri (zemin ne olursa olsun), parıltı şeridinin altı beyaz (tek odak)
    const k = B.k; k.save(); k.fillStyle = B.ton(.42); k.fill(p); k.clip(p);
    const serit = (g, w) => { g.beginPath(); g.moveTo(x0 - 10 * s, y0 - 90 * s); g.lineTo(x0 + (w - 10) * s, y0 - 90 * s); g.lineTo(x0 + (w - 95) * s, y0 + 95 * s); g.lineTo(x0 - 95 * s, y0 + 95 * s); g.closePath(); };
    const sw = i ? 26 : 38;   // uzak cam dar şerit
    k.fillStyle = '#fff'; serit(k, sw); k.fill(); k.restore();
    l.save(); l.clip(p); l.fillStyle = '#fff'; serit(l, sw); l.fill(); l.restore();   // parıltı: çapraz şerit (oval beyaz göz okunmasın)
  });
  l.restore();
}
const KAPAK = {
  A(o) {
    const B = BASKI; B.begin({ mod: 'video', parlak: 1.2 }); B.cam(960, 540, 1);
    B.each(g => { g.translate(W, 0); g.scale(-1, 1); });   // eski kapağın aynası: gardiyan sağa, koridor sola (sahnede yazı, rakam, yönlü nesne yok; levha kapalı)
    D.koridor(B, 0, { vp: [1350, 470], gen: 900, levha: false, isik: o.isik ?? .55 });
    { const k = B.k, g = k.createLinearGradient(1920, 0, 700, 0); g.addColorStop(0, `rgba(0,0,0,${o.golge ?? .64})`); g.addColorStop(.55, `rgba(0,0,0,${(o.golge ?? .64) * .8})`); g.addColorStop(1, `rgba(0,0,0,${o.golgeSag ?? .58})`);
      k.save(); k.fillStyle = g; k.fillRect(-100, -100, 2200, 1300); k.restore(); }   // koridor gölgede: yazının arkası koyu, odak camda kalsın
    ucCeyrek(B, o.gx ?? 500, o.gy ?? 500, 1.0);
    B.compose(ctx);
    if (o.yazi !== false) yazi(ctx, o.satir || ['RASTGELE', 'SEÇİLDİ'], o.tx ?? 70, o.ty ?? 290, 300, { ls: 2, lh: o.lh ?? 1.0, renkler: [ALTIN, FILDISI] });
    return cv;
  },
  B(o) {
    const B = BASKI; B.begin({ mod: 'kagit', kuru: .6 }); B.cam(960, 540, 1);
    const tx = o.bx ?? 1490, ty = o.by ?? 350, ts = o.bs ?? 1.3, tw = 520 * ts, th = 360 * ts;
    SET.karanlik(B, .9);
    SET.koni(B, tx, -900, 60, ty + th + 260, tw * 1.35, { a: o.koniA ?? .22, taban: 1, tohum: 3 });   // koninin tepesi kadraj dışında: üstte parlak kaynak yok
    { const k = B.k, cx = tx, cy = ty + th * .8, gr = k.createRadialGradient(cx, cy, 0, cx, cy, tw * .85); gr.addColorStop(0, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
      k.save(); k.fillStyle = gr; k.fillRect(cx - tw, cy - tw, tw * 2, tw * 2); k.restore(); }   // masada ışık havuzu teybin çevresinde
    SET.teyp(B, tx, ty, ts, 0, { ang: .6, kayit: 1, vu: .55, vuIsik: .35 });
    { const k = B.k, cx = tx + tw * .12, cy = ty + th * .55, gr = k.createRadialGradient(cx, cy, 0, cx, cy, tw * .62); gr.addColorStop(0, `rgba(255,255,255,${o.yuz ?? .8})`); gr.addColorStop(.6, `rgba(255,255,255,${(o.yuz ?? .8) * .45})`); gr.addColorStop(1, 'rgba(255,255,255,0)');
      k.save(); k.globalCompositeOperation = 'screen'; k.fillStyle = gr; k.fillRect(tx - tw / 2, ty, tw, th); k.restore(); }   // ışık teybin yüzüne düşer: karenin en parlak bölgesi teyp
    const lx = tx + 150 * ts, ly = ty + 305 * ts, lr = 55;   // kayıt lambası: küçük yumuşak ışıma (eş merkezli halka yok: hedef okunmasın)
    { const g = B.c, gr = g.createRadialGradient(lx, ly, 0, lx, ly, lr); gr.addColorStop(0, 'rgba(255,255,0,1)'); gr.addColorStop(.35, 'rgba(255,255,0,1)'); gr.addColorStop(1, 'rgba(255,255,0,0)');
      g.save(); g.fillStyle = gr; g.beginPath(); g.arc(lx, ly, lr, 0, TAU); g.fill(); g.restore();
      const k = B.k; k.save(); k.fillStyle = '#fff'; k.beginPath(); k.arc(lx, ly, 15 * ts, 0, TAU); k.fill(); k.restore(); }   // yanan lamba: altı açık, kırmızı kendi rengiyle görünür (vurgu rengi bu)
    B.compose(ctx);
    { const a = o.solKoyu ?? .62, e = o.solBit ?? 1100, g = ctx.createLinearGradient(0, 0, e, 0); g.addColorStop(0, `rgba(8,8,8,${a})`); g.addColorStop(.65, `rgba(8,8,8,${a * .85})`); g.addColorStop(1, 'rgba(8,8,8,0)');
      ctx.save(); ctx.fillStyle = g; ctx.fillRect(0, 0, e, 1080); ctx.restore(); }   // yazının arkası koyu (Fable, 27 Kasım): kırmızı vurgu satırı gri değerde de zeminden ayrılsın; koni (x > 1100) ve teyp etkilenmez
    if (o.yazi !== false) yazi(ctx, o.satir || ['BANTTA NE', 'İSTENDİ?'], o.tx ?? 70, o.ty ?? 290, 300, { ls: 2, lh: o.lh ?? 1.0, renkler: [FILDISI, o.vurgu || KIRMIZI] });
    return cv;
  },
};
window.kapak = (v, o = {}) => KAPAK[v](o);
window.READY = false;
(async () => { for (const f of ['400 40px "Bebas Neue"', '400 40px Anton', '700 40px "Courier Prime"']) await document.fonts.load(f, 'ÇĞİÖŞÜçğıöşü'); BASKI.init(); window.READY = true; })();
