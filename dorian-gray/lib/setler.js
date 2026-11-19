// Mekânlar (gravür dili; milton/lib/gravur.js). Klasik betik. Hepsi dünya koordinatında (1920×1080 sahne), GR.begin/engrave arasında çağrılır.
// Değer kuralı (milton KILAVUZ): üç değer; koyu kütleler düz siyah, ışık yalnız kaynağın çevresinde; ara tonlar geçişte.
'use strict';
const SET = (() => {
  const PI = Math.PI, { F, Sm, fill } = INSAN;
  const H0 = 0, HV = PI / 2;
  const R = (x, y, w, h) => F([[x, y], [x + w, y], [x + w, y + h], [x, y + h]]);
  const E2 = (x, y, rx, ry, r = 0) => { const p = new Path2D(); p.ellipse(x, y, rx, ry, r, 0, PI * 2); return p; };
  // ışık: ton katmanını açar (screen); L = {x, y, r0, r1, a}
  function isik(L) {
    const tx = GR.tx; tx.save(); tx.globalCompositeOperation = 'screen';
    const g = tx.createRadialGradient(L.x, L.y, L.r0 || 10, L.x, L.y, L.r1);
    const a = L.a ?? 1; g.addColorStop(0, `rgba(255,255,255,${.85 * a})`); g.addColorStop(.25, `rgba(255,255,255,${.42 * a})`); g.addColorStop(.6, `rgba(255,255,255,${.12 * a})`); g.addColorStop(1, 'rgba(255,255,255,0)');
    tx.fillStyle = g; tx.fillRect(L.x - L.r1, L.y - L.r1, L.r1 * 2, L.r1 * 2); tx.restore();
  }
  // pencere ışığı: dörtgen huzme (gün ışığı), ton katmanında
  function huzme(pts, a = .5) { const tx = GR.tx; tx.save(); tx.globalCompositeOperation = 'screen'; tx.fillStyle = `rgba(255,255,255,${a})`; tx.fill(F(pts)); tx.restore(); }
  function alev(x, y, t, s = 1) {
    const f = 1 + .12 * Math.sin(t * 9.1) + .07 * Math.sin(t * 15.7 + 1.3), ln = .08 * Math.sin(t * 3.7), p = new Path2D();
    p.moveTo(x - 9 * s, y + 8); p.bezierCurveTo(x - 12 * s, y - 10 * s * f, x + ln * 60, y - 30 * s * f, x + ln * 80, y - 46 * s * f);
    p.bezierCurveTo(x + 12 * s, y - 24 * s * f, x + 11 * s, y - 6 * s, x + 9 * s, y + 8); p.closePath();
    GR.fill(p, GR.tone(1), { th: HV, id: 3 });
  }
  // masa lambası (gövde + cam + alev); ışığı ayrıca isik() ile verilir
  function lamba(x, y, t, s = 1) {
    fill(Sm([[x - 37 * s, y + 85 * s], [x + 37 * s, y + 85 * s], [x + 31 * s, y + 62 * s], [x + 13 * s, y + 50 * s], [x + 17 * s, y + 26 * s], [x - 17 * s, y + 26 * s], [x - 13 * s, y + 50 * s], [x - 31 * s, y + 62 * s]]), .45, { type: 'rad', cx: x, cy: y + 62 * s, id: 9 });
    fill(Sm([[x - 21 * s, y + 26 * s], [x + 21 * s, y + 26 * s], [x + 29 * s, y], [x + 17 * s, y - 38 * s], [x - 17 * s, y - 38 * s], [x - 29 * s, y]]), .9, { th: HV, id: 7 });
    alev(x, y + 6 * s, t, s);
  }
  // yaldızlı çerçeve (gravür); portre yerel (0..500 × 0..720) → dünya: (x0, y0, s). Dönüş: ekran matrisi üreten işlev
  function cerceve(x0, y0, s, o = {}) {
    GR.save(); GR.frame(x0, y0, 0, 1, s);
    fill(R(0, 0, 500, 720), o.ton ?? .34, { th: HV, id: 9 });
    fill(R(14, 14, 472, 692), .1, { th: HV, id: 9 });
    const p = new Path2D(); p.rect(34, 34, 432, 652); for (const cx of [GR.tx, GR.px]) { cx.lineWidth = 7; }
    GR.tx.strokeStyle = GR.tone(.9); GR.tx.stroke(p); GR.px.strokeStyle = GR.hatch({ th: HV, id: 9 }); GR.px.stroke(p);
    if (!o.bos) fill(R(46, 46, 408, 628), .18, { th: .55, id: 0 });   // tuval (renk ayrıca bindirilir)
    else fill(R(46, 46, 408, 628), .1, { th: .55, id: 0 });
    GR.restore();
    return cam => { const c = camOf(cam) || { x: 0, y: 0, s: 1 }, z = c.s * RS; return [s * z, 0, 0, s * z, (x0 - c.x) * z, (y0 - c.y) * z]; };
  }
  // ── KİLİTLİ ODA (eski okul odası): gece. o = { lamba: {x,y} | null, t }
  function oda(o = {}) {
    fill(R(-400, -400, 2800, 1900), .05, { th: H0, id: 0 });
    fill(F([[-400, -400], [2400, -400], [2400, 60], [-400, 190]]), .02, { th: -.07, id: 0 });
    fill(F([[-400, 190], [2400, 60], [2400, 84], [-400, 222]]), .12, { th: -.07, id: 9 });
    fill(R(-400, 640, 2800, 265), .05, { th: H0, id: 0 });
    for (let x = -340; x < 2400; x += 230) fill(R(x, 668, 170, 210), .03, { th: H0, id: 0 });
    fill(R(-400, 632, 2800, 14), .18, { th: H0, id: 9 });
    fill(F([[-400, 905], [2400, 905], [2400, 1500], [-400, 1500]]), .03, { type: 'persp', y0: 905, D: 200, p0: 7, p1: 14, id: 8 });
    // kitaplık (okul kitapları)
    fill(R(40, 250, 330, 655), .02, { th: HV, id: 4 });
    for (let r = 0; r < 4; r++) { const y = 290 + r * 150; fill(R(62, y, 286, 118), .01, { th: H0, id: 4 });
      let x = 70; for (let k = 0; x < 330; k++) { const w = 14 + ((k * 37 + r * 11) % 17), hh = 78 + ((k * 23 + r * 7) % 34); if (x + w > 340) break; fill(R(x, y + 118 - hh, w - 3, hh), .07 + ((k + r) % 3) * .02, { th: HV, id: 9 }); x += w; } }
    // boyalı sandık (cassone) ve masa
    fill(Sm([[1640, 760], [1890, 760], [1900, 790], [1890, 905], [1640, 905], [1630, 790]]), .1, { th: H0, id: 9 });
    fill(R(1650, 800, 230, 6), .3, { th: H0, id: 9 });
    fill(F([[790, 735], [1030, 735], [1022, 752], [798, 752]]), .2, { th: H0, id: 9 });
    fill(R(808, 752, 14, 153), .08, { th: HV, id: 9 }); fill(R(998, 752, 14, 153), .08, { th: HV, id: 9 });
  }
  // ── STÜDYO: gün ışığı (büyük pencere sağda), şövale, divan, kürsü. o = { isik: 0..1 }
  function studyo(o = {}) {
    fill(R(-400, -400, 2800, 1900), .32, { th: H0, id: 0 });
    fill(R(-400, 870, 2800, 700), .2, { type: 'persp', y0: 870, D: 220, p0: 8, p1: 15, id: 8 });
    // büyük pencere (sağ), kayıt çıtaları
    fill(R(1380, 90, 520, 700), .96, { th: HV, id: 10 });
    for (const x of [1380, 1550, 1720, 1890]) fill(R(x - 6, 90, 12, 700), .1, { th: HV, id: 9 });
    for (const y of [90, 320, 550, 790]) fill(R(1374, y - 6, 532, 12), .1, { th: H0, id: 9 });
    fill(R(1340, 60, 30, 760), .08, { th: HV, id: 9 });   // perde kenarı
    huzme([[1380, 90], [1900, 90], [1500, 1080], [700, 1080]], .28 * (o.isik ?? 1));
    // divan (sol), arkasında İran heybesi desenli örtü
    fill(Sm([[60, 700], [560, 690], [600, 760], [590, 880], [70, 880], [40, 780]]), .14, { th: H0, id: 9 });
    fill(Sm([[70, 640], [540, 630], [560, 700], [60, 712]]), .22, { th: -.2, id: 9 });
    // kürsü (model platformu)
    fill(F([[1000, 860], [1360, 860], [1380, 900], [980, 900]]), .26, { th: H0, id: 9 });
  }
  // şövale (ahşap): tuval çerçevesiz, ön yüz; döner: portre ekran matrisi işlevi (cerceve yerine; çerçevesiz tuval)
  function sovale(x, y, s, o = {}) {
    fill(F([[x + 60 * s, y - 40 * s], [x + 80 * s, y - 40 * s], [x + 210 * s, y + 900 * s], [x + 190 * s, y + 900 * s]]), .1, { th: 1.2, id: 9 });
    fill(F([[x + 440 * s, y - 40 * s], [x + 420 * s, y - 40 * s], [x + 290 * s, y + 900 * s], [x + 310 * s, y + 900 * s]]), .1, { th: 1.9, id: 9 });
    fill(F([[x + 240 * s, y - 80 * s], [x + 260 * s, y - 80 * s], [x + 262 * s, y + 900 * s], [x + 242 * s, y + 900 * s]]), .08, { th: HV, id: 9 });
    fill(R(x + 10 * s, y + 690 * s, 480 * s, 22 * s), .14, { th: H0, id: 9 });   // tuval rafı
    // tuval: yerel 0..500 × 0..720'nin iç kısmı (46..454 × 46..674); çerçeve yok
    GR.save(); GR.frame(x, y, 0, 1, s); fill(R(40, 40, 420, 640), .9, { th: HV, id: 10 }); if (!o.bos) fill(R(46, 46, 408, 628), .2, { th: .55, id: 0 }); GR.restore();
    return cam => { const c = camOf(cam) || { x: 0, y: 0, s: 1 }, z = c.s * RS; return [s * z, 0, 0, s * z, (x - c.x) * z, (y - c.y) * z]; };
  }
  // ── BAHÇE (çizim): leylak çalıları, akşamüstü ışığı; o = { t }
  function bahce(o = {}) {
    fill(R(-400, -400, 2800, 1100), .9, { type: 'ray', cx: 1500, cy: 120, n: 90, id: 10, w: 3 });
    fill(R(-400, 820, 2800, 700), .3, { type: 'persp', y0: 820, D: 260, p0: 8, p1: 16, id: 8 });
    const t = o.t || 0;
    // leylak kümeleri (koyu kütle, salkımlar açık)
    for (const [cx, cy, rx, ry] of [[160, 420, 420, 420], [620, 360, 300, 330], [1820, 460, 380, 400]]) {
      fill(E2(cx, cy, rx, ry), .06, { type: 'rad', cx, cy, id: 2 });
      for (let k = 0; k < 9; k++) { const a = k * 2.39, r = rx * .62, x = cx + Math.cos(a) * r * .9, y = cy + Math.sin(a) * ry * .6 + Math.sin(t * 1.1 + k) * 3;
        fill(E2(x, y, 26, 58, .3 * Math.sin(k)), .68, { type: 'bend', ox: x, oy: y - 50, a: HV, k: .004, id: 6 }); }
    }
    fill(F([[860, 840], [1240, 840], [1250, 860], [850, 860]]), .15, { th: H0, id: 9 });   // bank
  }
  // ── TİYATRO: sahne ağzı, ayak ışıkları, balkon dekoru; loca (sol önde); o = { t, isik }
  function tiyatro(o = {}) {
    fill(R(-400, -400, 2800, 1900), .03, { th: H0, id: 0 });
    // sahne ağzı perdeleri
    fill(F([[300, 60], [460, 60], [430, 860], [300, 860]]), .08, { type: 'bend', ox: 380, oy: 60, a: HV, k: .0006, id: 9 });
    fill(F([[1620, 60], [1460, 60], [1490, 860], [1620, 860]]), .08, { type: 'bend', ox: 1540, oy: 60, a: HV, k: -.0006, id: 9 });
    fill(F([[300, 40], [1620, 40], [1620, 140], [960, 180], [300, 140]]), .07, { th: H0, id: 9 });
    // boyalı dekor: Capulet balkonu (açık ton, çizgili)
    fill(R(460, 140, 1000, 720), .16, { th: H0, id: 0 });
    fill(F([[1050, 380], [1360, 380], [1360, 420], [1050, 420]]), .7, { th: H0, id: 9 });
    for (let x = 1060; x < 1360; x += 28) fill(R(x, 420, 10, 70), .7, { th: HV, id: 9 });
    fill(F([[1080, 160], [1330, 160], [1330, 380], [1080, 380]]), .2, { th: HV, id: 9 });
    // sahne zemini ve ayak ışıkları
    fill(F([[300, 860], [1620, 860], [1700, 930], [220, 930]]), .35, { th: H0, id: 9 });
    isik({ x: 960, y: 960, r0: 60, r1: 900, a: .75 * (o.isik ?? 1) });
    for (let x = 340; x < 1600; x += 90) { fill(E2(x, 922, 14, 8), .97, { th: H0, id: 3 }); }
  }
  // loca (önde, sol): kadife korkuluk, oturan siluetler ayrı çizilir
  function loca() {
    fill(F([[-400, 760], [700, 760], [740, 820], [740, 1500], [-400, 1500]]), .04, { th: H0, id: 9 });
    fill(F([[-400, 740], [720, 740], [740, 780], [-400, 790]]), .25, { type: 'bend', ox: 0, oy: 760, a: 0, k: 0, id: 9 });
  }
  // ── EV: hol, duvar paneli, merdiven, pencere (panjur); o = { safak: 0..1 }
  function ev(o = {}) {
    fill(R(-400, -400, 2800, 1900), .1 + .12 * (o.safak || 0), { th: H0, id: 0 });
    for (let x = -300; x < 2400; x += 300) fill(R(x, 120, 260, 520), .07 + .1 * (o.safak || 0), { th: HV, id: 9 });
    fill(R(-400, 660, 2800, 18), .25, { th: H0, id: 9 });
    fill(R(-400, 900, 2800, 600), .08, { type: 'persp', y0: 900, D: 220, p0: 8, p1: 15, id: 8 });
    // pencere (sol), panjur payı o.panjur 0 kapalı .. 1 açık
    const pj = o.panjur ?? 0;
    fill(R(80, 160, 360, 560), .2 + .7 * pj, { th: HV, id: 10 });
    fill(R(80, 160, 360, 560 * (1 - pj)), .3, { th: H0, id: 9 });
    if (pj > 0) huzme([[80, 160 + 560 * (1 - pj)], [440, 160 + 560 * (1 - pj)], [1500, 1080], [600, 1080]], .25 * pj);
  }
  // ── SALON: şömine (ateş), piyano, divan, pencere perdesi; o = { t, ates }
  function salon(o = {}) {
    fill(R(-400, -400, 2800, 1900), .08, { th: H0, id: 0 });
    fill(R(-400, 880, 2800, 600), .05, { type: 'persp', y0: 880, D: 220, p0: 8, p1: 15, id: 8 });
    // şömine (sağ)
    fill(R(1420, 420, 420, 460), .22, { th: H0, id: 9 }); fill(R(1500, 560, 260, 320), .02, { th: H0, id: 0 });
    fill(R(1400, 400, 460, 30), .35, { th: H0, id: 9 });
    if (o.ates !== false) { const t = o.t || 0; for (let k = 0; k < 4; k++) { const x = 1560 + k * 50, f = 1 + .2 * Math.sin(t * 7 + k * 2); const p = new Path2D(); p.moveTo(x - 20, 870); p.quadraticCurveTo(x, 870 - 120 * f, x + 6, 870 - 150 * f); p.quadraticCurveTo(x + 18, 860 - 60 * f, x + 22, 870); p.closePath(); GR.fill(p, GR.tone(1), { th: HV, id: 3 }); }
      isik({ x: 1630, y: 800, r0: 40, r1: 820, a: .7 }); }
    // şamdan (piyanonun üstünde) ve ışığı
    { const t2 = o.t || 0; for (const dx of [-30, 0, 30]) alev(520 + dx, 560, t2 + dx, .6); isik({ x: 520, y: 560, r1: 700, a: .65 }); }
    // piyano (sol orta)
    fill(Sm([[260, 600], [760, 600], [780, 640], [780, 760], [240, 760], [240, 640]]), .03, { th: H0, id: 9 }); fill(R(280, 610, 460, 14), .5, { th: H0, id: 9 });
    fill(R(250, 740, 520, 26), .3, { th: H0, id: 9 });
    for (const x of [280, 740]) fill(R(x, 760, 22, 130), .02, { th: HV, id: 9 });
    // divan (orta sağ)
    fill(Sm([[900, 760], [1320, 760], [1340, 820], [1330, 890], [890, 890], [880, 820]]), .12, { th: H0, id: 9 });
  }
  // ── MAHKEME (1895): ahşap paneller, yargıç kürsüsü, sanık/tanık yeri, galeri; o = {}
  function mahkeme(o = {}) {
    fill(R(-400, -400, 2800, 1900), .14, { th: H0, id: 0 });
    for (let x = -300; x < 2400; x += 140) fill(R(x, 300, 120, 500), .1, { th: HV, id: 9 });
    fill(R(-400, 200, 2800, 40), .3, { th: H0, id: 9 });
    // yüksek pencere ışığı
    fill(R(820, 0, 280, 200), .9, { th: HV, id: 10 }); huzme([[820, 200], [1100, 200], [1400, 1080], [600, 1080]], .16);
    // yargıç kürsüsü (arka orta)
    fill(F([[600, 520], [1320, 520], [1320, 760], [600, 760]]), .06, { th: H0, id: 9 });
    fill(R(590, 500, 740, 26), .3, { th: H0, id: 9 });
    // galeri sırası (siluet başlar)
    for (let r = 0; r < 2; r++) for (let x = -200 + r * 40; x < 2200; x += 70) { const y = 900 + r * 80; fill(E2(x, y, 26, 30), .03, { th: .9, id: 6 }); fill(F([[x - 40, y + 20], [x + 40, y + 20], [x + 50, y + 200], [x - 50, y + 200]]), .03); }
  }
  // ── Gerçek görseller
  const IMG = {};
  function yukle(ad, url) { return new Promise((res, rej) => { const im = new Image(); im.onload = () => { IMG[ad] = im; res(im); }; im.onerror = () => rej(new Error('görsel yok: ' + url)); im.src = url; }); }
  // Doré levhası: doğrudan (zaten gravür), mürekkep ve kâğıt rengine eşlenir. cam {cx, cy, z} dünya: görüntü (0,0)'da, genişliği bw
  function dore(ctx, ad, cam, bw = 1920) {
    const im = IMG[ad], c = camOf(cam) || { x: 0, y: 0, s: 1 }, z = c.s * RS, bh = bw * im.height / im.width;
    ctx.save(); ctx.setTransform(z, 0, 0, z, -c.x * z, -c.y * z); ctx.imageSmoothingQuality = 'high'; ctx.fillStyle = '#000'; ctx.fillRect(-200, -200, bw + 400, bh + 400); ctx.drawImage(im, 0, 0, bw, bh); ctx.restore();
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = `rgb(${GR.PAPER})`; ctx.fillRect(0, 0, DW, DH);
    ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgb(${GR.INK})`; ctx.fillRect(0, 0, DW, DH); ctx.restore();
  }
  // Fotoğrafı gravüre çevir: ton katmanına gri (kontrastlı) çizer, yama katmanına tarama. (x, y, w) dünya
  function fotoGravur(ad, x, y, w, o = {}) {
    const im = IMG[ad], h = w * im.height / im.width, sx = o.kirp || [0, 0, im.width, im.height];
    const hh = w * sx[3] / sx[2];
    GR.tx.save(); GR.tx.filter = `grayscale(1) contrast(${o.kontrast ?? 1.5}) brightness(${o.parlak ?? 1.05})`; GR.tx.drawImage(im, sx[0], sx[1], sx[2], sx[3], x, y, w, hh); GR.tx.restore();
    GR.px.fillStyle = GR.hatch(o.tarama || { th: .55, id: 5 }); GR.px.fillRect(x, y, w, hh);
    return hh;
  }
  // Kâğıt belge (Lippincott sayfası): doğrudan, sıcak kâğıt tonu
  function belge(ctx, ad, cam, x, y, w, o = {}) {
    const im = IMG[ad], c = camOf(cam) || { x: 0, y: 0, s: 1 }, z = c.s * RS, sx = o.kirp || [0, 0, im.width, im.height], h = w * sx[3] / sx[2];
    ctx.save(); ctx.setTransform(z, 0, 0, z, -c.x * z, -c.y * z);
    ctx.fillStyle = `rgb(${GR.INK})`; ctx.fillRect(-400, -400, 2800, 1900);
    ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 30; ctx.fillStyle = `rgb(${GR.PAPER})`; ctx.fillRect(x, y, w, h); ctx.shadowBlur = 0;
    ctx.globalCompositeOperation = 'multiply'; ctx.filter = 'grayscale(1) contrast(1.15)'; ctx.drawImage(im, sx[0], sx[1], sx[2], sx[3], x, y, w, h); ctx.filter = 'none';
    ctx.restore();
    return h;
  }
  return { isik, huzme, alev, lamba, cerceve, sovale, oda, studyo, bahce, tiyatro, loca, ev, salon, mahkeme, yukle, IMG, dore, fotoGravur, belge, R, E2 };
})();
