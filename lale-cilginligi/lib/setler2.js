// İkinci set kitabı: belgeler, iç mekânlar, nesneler, İstanbul. Klasik betik; GR.begin/engrave arasında dünya koordinatında çizer.
// Kurallar: renk yalnız lalede (LALE.ciz); belge yazıları YAZI.ekle ile (basıldıktan sonra okunur kalır).
// Hassasiyet: cami, minare, haç, kilise kulesi, Arap harfi taklidi yok; Osmanlı belgeleri Latin harfli "bizim aktarımımız" olarak gösterilir.
'use strict';
const SET2 = (() => {
  const PI = Math.PI, { F, Sm, fill } = INSAN, R = SET.R, E2 = SET.E2, rnd = SET.rnd, H0 = 0, HV = PI / 2;
  const IMG = {};
  function yukle(ad, url) { return new Promise((res, rej) => { const im = new Image(); im.onload = () => { IMG[ad] = im; res(im); }; im.onerror = () => rej(new Error('görsel yok: ' + url)); im.src = url; }); }
  // gerçek görsel: basmadan SONRA ctx'e kamera dönüşümüyle çizilir (dünya kutusu x, y, w); o.gri: siyah-beyaz (renk kuralı), o.kirp [sx, sy, sw, sh] (oran 0..1)
  function gorsel(ctx, cam, ad, x, y, w, o = {}) {
    const im = IMG[ad]; if (!im) return;
    const c = camOf(cam) || { x: 0, y: 0, s: 1 }, z = c.s * RS;
    const k = o.kirp || [0, 0, 1, 1], sw = im.width * k[2], sh = im.height * k[3], h = w * sh / sw;
    ctx.save(); ctx.setTransform(z, 0, 0, z, -c.x * z, -c.y * z);
    if (o.golge !== false) { ctx.fillStyle = 'rgba(0,0,0,.45)'; ctx.fillRect(x + 10, y + 12, w, h); }
    ctx.globalAlpha = o.a ?? 1; if (o.gri) ctx.filter = 'grayscale(1) contrast(1.08)';
    ctx.drawImage(im, im.width * k[0], im.height * k[1], sw, sh, x, y, w, h);
    ctx.restore(); return h;
  }
  // ── kâğıt sayfa (gravürde açık dikdörtgen + kenar gölgesi); yazılar ayrıca YAZI ile
  function sayfa(x, y, w, h, o = {}) {
    fill(R(x + 8, y + 10, w, h), .06, { th: H0, id: 9 });
    fill(R(x, y, w, h), o.ton ?? .95, { th: o.th ?? .02, id: 10 });
    if (o.cerceve) { fill(R(x + 24, y + 24, w - 48, 3), .2, { th: H0, id: 9 }); fill(R(x + 24, y + h - 27, w - 48, 3), .2, { th: H0, id: 9 }); }
  }
  // satır satır sahte metin çizgisi (okunmayan gövde metni)
  function satirlar(x, y, w, n, ara = 26, o = {}) { for (let i = 0; i < n; i++) { const L = w * (i === n - 1 ? .55 : .82 + rnd(i + x) * .18); fill(R(x, y + i * ara, L, o.kalin ?? 3), .25, { th: H0, id: 9 }); } }
  // masa yüzeyi (ahşap)
  function masaUst(y, o = {}) { fill(R(-600, y, 3100, 900), o.ton ?? .22, { th: .03, id: 9 }); for (let k = 0; k < 9; k++) fill(R(-600, y + 40 + k * 70 + rnd(k) * 20, 3100, 3), .08, { th: .03, id: 9 }); }
  // tüy kalem ve hokka
  function kalem(x, y, a = -.6, s = 1) { const c = Math.cos(a), sn = Math.sin(a); fill(F([[x, y], [x + c * 260 * s - sn * 10, y + sn * 260 * s + c * 10], [x + c * 260 * s + sn * 18, y + sn * 260 * s - c * 18]]), .85, { th: a, id: 6 }); fill(F([[x - 4, y - 2], [x + c * 30, y + sn * 30], [x + 4, y + 2]]), .05, { th: a, id: 9 }); }
  function hokka(x, y, s = 1) { fill(Sm([[x - 40 * s, y], [x + 40 * s, y], [x + 34 * s, y - 50 * s], [x + 14 * s, y - 62 * s], [x - 14 * s, y - 62 * s], [x - 34 * s, y - 50 * s]]), .08, { th: HV, id: 9 }); }
  function mumluk(x, y, t, s = 1) { fill(Sm([[x - 40 * s, y], [x + 40 * s, y], [x + 20 * s, y - 14 * s], [x - 20 * s, y - 14 * s]]), .3, { th: H0, id: 9 }); SET.mum(x, y - 54 * s, t, s); }
  // para: gulden yığını (n sikke)
  function para(x, y, n, s = 1) { for (let i = 0; i < n; i++) { const cx = x + (rnd(i * 3) - .5) * 30 * s, cy = y - i * 7 * s; fill(E2(cx, cy, 26 * s, 9 * s), .7 + (i % 2) * .1, { th: 0, id: 9 }); fill(E2(cx, cy, 26 * s, 9 * s), .3, { th: H0, id: 9 }); fill(E2(cx, cy - 2 * s, 22 * s, 7 * s), .82, { type: 'rad', cx, cy, id: 9 }); } }
  // kese
  function kese(x, y, s = 1) { fill(Sm([[x - 50 * s, y], [x + 50 * s, y], [x + 60 * s, y - 50 * s], [x + 20 * s, y - 90 * s], [x - 20 * s, y - 90 * s], [x - 60 * s, y - 50 * s]]), .3, { th: Math.PI / 2 + .25, id: 9 }); for (const d of [-26, 0, 26]) fill(R(x + d * s - 2, y - 84 * s, 4, 70 * s), .12, { th: H0, id: 9 }); /* kese: büzgüden inen kıvrımlar */ fill(R(x - 22 * s, y - 100 * s, 44 * s, 12 * s), .1, { th: H0, id: 9 }); }
  // ── KIŞ YOLU: karlı tepeler, yol, araba (kupa), atlı silueti; o.t
  function kisYolu(o = {}) {
    const t = o.t || 0;
    fill(R(-600, -500, 3100, 1300), .9, { th: -.03, id: 10 });
    for (let k = 0; k < 3; k++) { const y0 = 520 + k * 90; fill(Sm([[-600, y0 + 60], [-200, y0 - 20 + k * 10], [300, y0 + 30], [800, y0 - 40], [1300, y0 + 10], [1900, y0 - 30], [2500, y0 + 40], [2500, 1500], [-600, 1500]]), .93 - k * .12, { th: -.04 - k * .02, id: k ? 9 : 10 }); }
    // yol
    fill(F([[860, 640], [1000, 640], [1500, 1100], [300, 1100]]), .7, { type: 'persp', y0: 640, D: 200, p0: 9, p1: 16, id: 8 });
    // çıplak ağaçlar
    for (let i = 0; i < 7; i++) { const x = 100 + i * 290 + rnd(i) * 80, y = 700 + rnd(i + 4) * 80, h = 160 + rnd(i * 3) * 120; fill(F([[x - 4, y], [x + 4, y], [x + 2, y - h], [x - 2, y - h]]), .06, { th: HV, id: 9 }); for (let b = 0; b < 5; b++) { const by = y - h * (.4 + b * .12), d = b % 2 ? 1 : -1; fill(F([[x, by], [x + d * 60, by - 50], [x + d * 62, by - 46], [x + 2, by + 4]]), .06, { th: d * .8, id: 9 }); } }
    // araba (kupa): kutu + iki tekerlek + çeken at silueti
    const ax = 1060 + Math.sin(t * .6) * 4, ay = 860;
    fill(R(ax - 120, ay - 170, 240, 130), .08, { th: HV, id: 9 }); fill(R(ax - 90, ay - 150, 70, 60), .7, { th: HV, id: 10 });
    fill(F([[ax - 140, ay - 180], [ax + 140, ay - 180], [ax + 120, ay - 196], [ax - 120, ay - 196]]), .04, { th: H0, id: 9 });
    for (const dx of [-90, 90]) { fill(E2(ax + dx, ay - 30, 46, 46), .06, { type: 'rad', cx: ax + dx, cy: ay - 30, id: 9 }); fill(E2(ax + dx, ay - 30, 30, 30), .6, { type: 'rad', cx: ax + dx, cy: ay - 30, id: 9 }); }
    at(ax + 260, ay, 1, 1, t);
  }
  // at silueti (yandan): gövde, boyun, baş, dört bacak; t ile hafif adım
  function at(x, y, s = 1, yon = 1, t = 0) {
    GR.save(); GR.frame(x, y, 0, yon, s);
    const b = Math.sin(t * 4) * 6;
    fill(Sm([[-120, -150], [-60, -175], [60, -172], [120, -160], [150, -210], [178, -262], [210, -250], [196, -220], [176, -170], [150, -120], [120, -100], [-110, -100], [-140, -120]]), .05, { th: .3, id: 9 });
    for (const [lx, ph] of [[-100, 0], [-70, PI], [90, PI], [120, 0]]) { const a = Math.sin(t * 4 + ph) * .25; fill(F([[lx - 9, -110], [lx + 9, -110], [lx + 9 + Math.sin(a) * 100, -2], [lx - 5 + Math.sin(a) * 100, -2]]), .05, { th: HV, id: 9 }); }
    fill(Sm([[-140, -150], [-170, -110 + b], [-160, -100 + b], [-130, -130]]), .05, { th: .2, id: 9 });   // kuyruk
    GR.restore();
  }
  // buket: nergis (beyaz, renksiz), sümbül (gravür), laleler (renkli); x, y sapların bağlandığı yer; s ölçek
  function buket(x, y, s = 1, t = 0, o = {}) {
    for (let i = 0; i < 9; i++) { const a = -PI / 2 + (i - 4) * .13, L = 260 * s + rnd(i) * 60 * s, ex = x + Math.cos(a) * L, ey = y + Math.sin(a) * L; fill(F([[x - 2, y], [x + 2, y], [ex + 2, ey], [ex - 2, ey]]), .2, { th: a, id: 9 }); }
    // nergisler: altı yapraklı beyaz yıldız + göbek
    for (const [dx, dy] of [[-120, -240], [110, -250], [-40, -300]]) { const cx = x + dx * s, cy = y + dy * s;
      for (let k = 0; k < 6; k++) { const a = k * PI / 3 + .2; fill(Sm([[cx, cy], [cx + Math.cos(a - .25) * 34 * s, cy + Math.sin(a - .25) * 34 * s], [cx + Math.cos(a) * 46 * s, cy + Math.sin(a) * 46 * s], [cx + Math.cos(a + .25) * 34 * s, cy + Math.sin(a + .25) * 34 * s]]), .93, { type: 'rad', cx, cy, id: 10 }); }
      fill(E2(cx, cy, 13 * s, 13 * s), .55, { type: 'rad', cx, cy, id: 9 }); }
    // sümbül: küçük çan dizisi
    { const cx = x + 40 * s, cy = y - 330 * s; for (let k = 0; k < 9; k++) fill(E2(cx + (k % 2 ? 12 : -12) * s, cy + k * 16 * s, 11 * s, 9 * s), .6, { type: 'rad', cx, cy, id: 9 }); }
    // laleler (renkli)
    LALE.ciz(x - 60 * s, y - 330 * s, .75 * s, { sap: 0, tip: 'ist', cesit: 'ist', egim: -.15 + Math.sin(t) * .02 });
    LALE.ciz(x + 150 * s, y - 320 * s, .7 * s, { sap: 0, tip: 'ist', cesit: 'istSari', egim: .2 });
    LALE.ciz(x + 10 * s, y - 380 * s, .8 * s, { sap: 0, tip: 'ist', cesit: 'ist', egim: .02 });
    // bağ
    fill(R(x - 26 * s, y - 20 * s, 52 * s, 24 * s), .85, { th: H0, id: 9 });
  }
  // sarık (yan profil, büyük): kat kat dolanmış tülbent, kıvrımına takılı lale
  function sarik(x, y, s = 1, o = {}) {
    // baş/omuz silueti (yüz yok: arkadan ¾)
    fill(Sm([[x - 260 * s, y + 420 * s], [x - 200 * s, y + 200 * s], [x - 110 * s, y + 120 * s], [x + 130 * s, y + 120 * s], [x + 220 * s, y + 200 * s], [x + 280 * s, y + 420 * s]]), .05, { th: HV, id: 9 });
    fill(Sm([[x - 110 * s, y + 140 * s], [x - 130 * s, y + 20 * s], [x - 90 * s, y - 40 * s], [x + 90 * s, y - 40 * s], [x + 130 * s, y + 20 * s], [x + 110 * s, y + 140 * s]]), .05, { th: .9, id: 6 });
    // tülbent: yuvarlak kütle, sargı bantları
    fill(Sm([[x - 200 * s, y - 20 * s], [x - 210 * s, y - 120 * s], [x - 140 * s, y - 220 * s], [x, y - 250 * s], [x + 150 * s, y - 220 * s], [x + 215 * s, y - 120 * s], [x + 200 * s, y - 20 * s], [x, y + 10 * s]]), .9, { th: -.15, id: 9 });   // sargı yönünde tarama (halka tarama hedef tahtası okunuyordu)
    for (let k = 0; k < 6; k++) { const yy = y - 30 * s - k * 36 * s, ww = 200 * s * (1 - k * .1); fill(Sm([[x - ww, yy], [x - ww * .3, yy - 20 * s], [x + ww * .6, yy - 34 * s], [x + ww, yy - 26 * s], [x + ww * .6, yy - 22 * s], [x - ww * .3, yy - 8 * s]]), .62, { th: -.15, id: 9 }); }
    LALE.ciz(x + 150 * s, y - 150 * s, 1.1 * s, { sap: 40 * s, tip: 'ist', cesit: 'ist', egim: .55, yaprakYok: true });
  }
  // mektup masası: masa, mum, kâğıt, kalem; elçinin sırtı (Avrupalı kıyafet) solda
  function mektupMasasi(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .06, { th: H0, id: 0 });
    masaUst(700);
    sayfa(760, 560, 520, 300, { ton: .95, th: .02 });
    mumluk(1420, 690, t, 1.2); SET.isik({ x: 1420, y: 600, r1: 700, a: .9 });
    hokka(1320, 700, 1); kalem(1000 + (o.yaz || 0) * 120, 700, -.9, 1);
  }
  // ── LEIDEN BAHÇESİ: dikdörtgen tarhlar, çit, alçak bina; botanikçi ve sandık
  function leiden(t, o = {}) {
    SET.gok({ gun: 1, ufuk: 560 });
    SET.kasaba(560, .8);
    fill(R(-600, 560, 3100, 900), .3, { type: 'persp', y0: 560, D: 240, p0: 6, p1: 14, id: 8 });
    // tarhlar (perspektifte), içinde laleler
    for (let r = 0; r < 4; r++) { const yy = 640 + r * r * 34 + r * 70, sc = .3 + r * .22;
      for (let c = -3; c <= 3; c++) { const cx = 960 + c * 380 * (.5 + r * .3); fill(R(cx - 140 * (.5 + r * .3), yy, 280 * (.5 + r * .3), 30 * (.5 + r * .4)), .12, { th: H0, id: 9 });
        for (let k = 0; k < 4; k++) LALE.ciz(cx - 90 * (.5 + r * .3) + k * 60 * (.5 + r * .3), yy + 8, sc * .7, { sap: 50 * sc, cesit: ['semper', 'duz', 'sari', 'viceroy'][(k + c + r + 9) % 4], yaprakYok: sc < .4, tohum: cx + k }); } }
    if (o.botanikci !== false) { INSAN.adam({ x: 520, y: 1040, h: 560, yon: 1, sapka: 'genis', yaka: 'duz', kenar: .5, giysi: 'pelerin', kolOn: { a: .7, b: .8 } }); fill(R(640, 900, 160, 90), .25, { th: H0, id: 9 }); }
  }
  // gece bahçesi + hırsız (soğanları sökerken), ay
  function hirsiz(t) {
    fill(R(-600, -500, 3100, 1600), .05, { th: -.05, id: 1 });
    fill(E2(1500, 220, 70, 70), .97, { type: 'rad', cx: 1500, cy: 220, id: 10 }); SET.isik({ x: 1500, y: 220, r1: 500, a: .45 });
    fill(R(-600, 700, 3100, 900), .1, { type: 'persp', y0: 700, D: 220, p0: 7, p1: 14, id: 8 });
    fill(R(-600, 520, 3100, 180), .03, { th: HV, id: 9 });   // çit
    for (let x = -560; x < 2500; x += 60) fill(R(x, 480, 14, 220), .12, { th: HV, id: 9 });
    for (let k = 0; k < 6; k++) LALE.ciz(300 + k * 200, 820, .55, { sap: 60, cesit: k % 2 ? 'semper' : 'viceroy', renk: .7 });
    const dig = Math.sin(t * 3) * .3;
    INSAN.adam({ x: 1100, y: 960, h: 520, yon: -1, egim: .55, arka: false, sapka: 'genis', kenar: .35, kenarYan: 1, kolOn: { a: 1.4 + dig, b: .9 }, kolArka: { a: 1.2, b: .6 } });
    LALE.sogan(960, 930, .7); LALE.sogan(1010, 950, .55);
    kese(1240, 980, .9);
  }
  // aynalı kabine (Pauw'un bahçesi, Wassenaer 1623): ortada saksıda tek lale, iki yanda aynalarda yansımaları
  function aynaKabine(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .2, { th: H0, id: 0 });
    fill(R(-600, 820, 3100, 700), .35, { type: 'persp', y0: 820, D: 200, p0: 8, p1: 15, id: 8 });
    for (const [x, w] of [[260, 380], [1280, 380]]) { fill(R(x - 20, 180, w + 40, 640), .08, { th: HV, id: 9 }); fill(R(x, 200, w, 600), .75, { th: x < 900 ? .5 : -.5, id: 10 }); }
    SET.saksi(960, 800, 1.3); LALE.ciz(960, 640, 1.6, { sap: 100, cesit: 'semper', ac: .25, egim: Math.sin(t * .7) * .02 });
    // aynalardaki yansımalar (daha küçük, aynanın içinde)
    LALE.ciz(450, 620, .9, { sap: 70, cesit: 'semper', ac: .25, renk: .8 }); LALE.ciz(1470, 620, .9, { sap: 70, cesit: 'semper', ac: .25, renk: .8 });
    LALE.ciz(330, 600, .55, { sap: 50, cesit: 'semper', renk: .6 }); LALE.ciz(1590, 600, .55, { sap: 50, cesit: 'semper', renk: .6 });
    SET.isik({ x: 960, y: 560, r1: 600, a: .8 });
  }
  // ekim: tarlada eğilmiş bahçıvanlar soğan gömer; o.p (0..1) ilerleme
  function ekim(t, o = {}) {
    SET.gok({ gun: 1, ufuk: 520 }); SET.kasaba(520, .7); SET.degirmen(300, 520, .6, t * .3);
    fill(R(-600, 520, 3100, 900), .28, { type: 'persp', y0: 520, D: 240, p0: 6, p1: 14, id: 8 });
    for (let r = 0; r < 6; r++) fill(R(-600, 600 + r * r * 22 + r * 40, 3100, 10 + r * 4), .1, { th: H0, id: 9 });
    for (let i = 0; i < 3; i++) { const x = 600 + i * 420, ph = t * 2 + i; INSAN.adam({ x, y: 1060 + i * 20, h: 400, yon: i % 2 ? -1 : 1, egim: .32 + Math.sin(ph) * .04, sapka: 'genis', palto: .4, kenar: .4, kolOn: { a: .5 + Math.sin(ph) * .2, b: .5 }, kolArka: { a: .35, b: .4 } }); }
    for (let k = 0; k < 8; k++) LALE.sogan(400 + k * 160, 1010 + (k % 2) * 10, .45, { ton: .45 });
  }
  // toprak kesiti: yukarıda zemin çizgisi ve bir kâğıt (sözleşme) masa üstünde, aşağıda toprakta soğan
  function kesit(t, o = {}) {
    fill(R(-600, -500, 3100, 1100), .86, { th: -.02, id: 10 });
    fill(R(-600, 560, 3100, 1000), .14, { th: .2, id: 4 });
    for (let k = 0; k < 40; k++) fill(E2(rnd(k) * 2000 - 40, 620 + rnd(k + 9) * 440, 6 + rnd(k * 3) * 10, 4 + rnd(k * 7) * 6), .4, { th: 0, id: 9 });
    LALE.sogan(960, 820, 1.4, { ton: .55 });
    for (let k = 0; k < 7; k++) fill(R(820 + k * 40, 560, 3, 180 + rnd(k) * 60), .5, { th: HV, id: 9 });   // filiz yok: kış
  }
  // meyhane arka oda: yuvarlak masa, maşrapalar, kâğıtlar, tebeşir tahtası
  function arkaOda(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .08, { th: H0, id: 0 });
    fill(R(-600, 900, 3100, 600), .22, { type: 'persp', y0: 900, D: 200, p0: 8, p1: 15, id: 8 });
    fill(R(1260, 220, 420, 300), .05, { th: HV, id: 9 }); fill(R(1280, 240, 380, 260), .18, { th: .3, id: 4 });   // tebeşir tahtası
    fill(E2(960, 760, 520, 90), .3, { th: H0, id: 9 }); fill(R(940, 760, 40, 260), .08, { th: HV, id: 9 });
    for (const [x, y] of [[760, 730], [1160, 740], [980, 700]]) { fill(R(x - 22, y - 70, 44, 70), .35, { th: HV, id: 9 }); fill(R(x + 22, y - 56, 16, 36), .2, { th: HV, id: 9 }); }
    for (let k = 0; k < 4; k++) fill(F([[820 + k * 90, 770], [900 + k * 90, 762], [906 + k * 90, 790], [826 + k * 90, 798]]), .92, { th: .1, id: 5 });
    SET.mum(1060, 690, t, 1); SET.isik({ x: 1060, y: 640, r1: 640, a: .85 });
  }
  // usta önlüğü olan figür (dokumacı/fırıncı): adam + açık renk önlük
  function usta(o) { const r = INSAN.adam({ ...o, sapka: o.sapka ?? 'genis' }); if (!o.arka) { const k = (o.h || 600) / 760; fill(F([[o.x - 50 * k, o.y - 520 * k], [o.x + 50 * k, o.y - 520 * k], [o.x + 64 * k, o.y - 250 * k], [o.x - 64 * k, o.y - 250 * k]]), .82, { th: HV, id: 9 }); } return r; }
  // defter/hesap sayfası (çift sayfa), satırlar YAZI ile; o.satir: [[sol, sağ], …]
  function defter(x, y, w, h, o = {}) {
    fill(R(x - 14, y - 10, w + 28, h + 24), .08, { th: H0, id: 9 });
    sayfa(x, y, w / 2 - 4, h, { ton: .95 }); sayfa(x + w / 2 + 4, y, w / 2 - 4, h, { ton: .95 });
    fill(R(x + w / 2 - 4, y, 8, h), .3, { th: HV, id: 9 });
    for (let i = 0; i < (o.cizgi ?? 14); i++) { fill(R(x + 30, y + 80 + i * 44, w / 2 - 60, 1.6), .55, { th: H0, id: 9 }); fill(R(x + w / 2 + 30, y + 80 + i * 44, w / 2 - 60, 1.6), .55, { th: H0, id: 9 }); }
  }
  // matbaa presi: ahşap çerçeve, vida, kâğıt yığını; basılan sayfalar
  function matbaa(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .1, { th: H0, id: 0 });
    fill(R(-600, 900, 3100, 600), .26, { type: 'persp', y0: 900, D: 200, p0: 8, p1: 15, id: 8 });
    fill(R(760, 160, 60, 760), .06, { th: HV, id: 9 }); fill(R(1100, 160, 60, 760), .06, { th: HV, id: 9 });
    fill(R(740, 140, 440, 60), .06, { th: H0, id: 9 }); fill(R(780, 520, 360, 40), .1, { th: H0, id: 9 });
    const v = Math.sin(t * 2) * 30; fill(R(945, 200, 30, 280 + v), .4, { th: HV, id: 9 }); fill(R(820, 470 + v, 280, 30), .2, { th: H0, id: 9 });
    fill(F([[1180, 380], [1420, 300], [1430, 316], [1192, 398]]), .2, { th: -.32, id: 9 });   // kol
    for (let k = 0; k < 6; k++) sayfa(1300 + k * 8, 640 - k * 10, 300, 200, { ton: .93 });
    SET.isik({ x: 1000, y: 300, r1: 800, a: .7 });
  }
  // dokuma tezgâhı (taşınırken): ahşap çerçeve, çözgü ipleri
  function tezgah(x, y, s = 1, a = 0) {
    GR.save(); GR.frame(x, y, a, 1, s);
    for (const dx of [-200, 200]) fill(R(dx - 12, -400, 24, 400), .1, { th: HV, id: 9 });
    fill(R(-220, -410, 440, 24), .1, { th: H0, id: 9 }); fill(R(-220, -180, 440, 24), .1, { th: H0, id: 9 });
    for (let k = -180; k <= 180; k += 14) fill(R(k, -390, 2, 210), .5, { th: HV, id: 9 });
    GR.restore();
  }
  // 1841 Londra çalışma odası: kitap yığınları, gaz lambası, pencere (sis)
  function mackayOda(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .08, { th: H0, id: 0 });
    fill(R(1300, 160, 420, 520), .65, { th: HV, id: 1 }); for (const x of [1300, 1510, 1720]) fill(R(x - 5, 160, 10, 520), .1, { th: HV, id: 9 });
    masaUst(700, { ton: .18 });
    for (let k = 0; k < 4; k++) { const x = 380 + k * 150; for (let j = 0; j < 3 + k % 2; j++) fill(R(x, 690 - j * 46, 130, 40), .15 + (j % 3) * .2, { th: H0, id: 9 }); }
    sayfa(900, 600, 420, 220, { ton: .95 }); hokka(1380, 700); kalem(1160, 720, -1.0, .8);
    SET.lamba ? 0 : 0; mumluk(1520, 690, t, 1.1); SET.isik({ x: 1520, y: 620, r1: 620, a: .8 });
  }
  // rıhtım: kazıklar, gemi pruvası, halat yığını; denizci oturur (o.t)
  function rihtim(t, o = {}) {
    SET.gok({ gun: 1, ufuk: 560 });
    fill(R(-600, 560, 3100, 300), .55, { th: .02, id: 8 });
    fill(Sm([[-300, 560], [500, 560], [700, 300], [640, 290], [520, 470], [-300, 470]]), .08, { th: .2, id: 9 });   // gemi pruvası
    fill(R(560, 40, 12, 460), .06, { th: HV, id: 9 });
    fill(R(-600, 840, 3100, 700), .32, { type: 'persp', y0: 840, D: 220, p0: 7, p1: 14, id: 8 });
    for (let x = -300; x < 2400; x += 260) fill(R(x, 760, 26, 120), .08, { th: HV, id: 9 });
    for (let k = 0; k < 4; k++) fill(E2(1200 + (k % 2) * 8, 905 - k * 14, 120 - k * 14, 16), .4 + (k % 2) * .12, { th: .35, id: 9 });   // halat yığını: üst üste kangallar (halka tarama hedef okunuyordu)
  }
  // bacacı: merdiven, uzun fırça; elinde boyalı lale (Mackay'in iddiası)
  function bacaci(x, y, t) {
    fill(F([[x + 60, y], [x + 80, y], [x + 300, y - 700], [x + 280, y - 700]]), .1, { th: 1.25, id: 9 });
    for (let k = 1; k < 10; k++) { const p = k / 10; fill(F([[x + 60 + p * 220, y - p * 700], [x + 80 + p * 220 + 40, y - p * 700 - 6], [x + 84 + p * 220 + 40, y - p * 700], [x + 64 + p * 220, y - p * 700 + 6]]), .1, { th: 0, id: 9 }); }
    INSAN.adam({ x, y, h: 600, yon: 1, sapka: true, kenar: .45, kolOn: { a: 2.0, b: .9 }, kolArka: { a: .2, b: .2 } });
    LALE.ciz(x + 130, y - 690, .9, { sap: 90, cesit: 'semper', egim: .2 });
  }
  // kitap: kapalı (sırt) ya da açık; o.acik
  function kitap(x, y, w, h, o = {}) {
    if (o.acik) { fill(Sm([[x, y], [x + w / 2, y + 16], [x + w, y], [x + w, y + h], [x + w / 2, y + h + 16], [x, y + h]]), .12, { th: H0, id: 9 }); sayfa(x + 10, y + 6, w / 2 - 14, h - 14, { ton: .95 }); sayfa(x + w / 2 + 4, y + 6, w / 2 - 14, h - 14, { ton: .95 }); }
    else { fill(R(x, y, w, h), o.ton ?? .12, { th: HV, id: 9 }); fill(R(x + 6, y + 6, w - 12, h - 12), (o.ton ?? .12) + .08, { th: .4, id: 9 }); }
  }
  // arşiv: raflarda defterler, masa lambası, araştırmacı sırtı
  function arsiv(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .07, { th: H0, id: 0 });
    for (let r = 0; r < 5; r++) { const y = 120 + r * 150; fill(R(-200, y + 120, 2400, 12), .2, { th: H0, id: 9 }); for (let x = -180; x < 2200; x += 30 + (x % 7)) fill(R(x, y + 20 + rnd(x + r) * 20, 24 + rnd(x * 3) * 8, 100 - rnd(x + r) * 20), .1 + rnd(x * r) * .2, { th: HV, id: 9 }); }
    masaUst(800, { ton: .16 });
    defter(760, 640, 560, 180, { cizgi: 3 });
    SET.isik({ x: 1040, y: 640, r1: 520, a: .9 });
  }
  // ── İSTANBUL ──
  // Boğaz/Kâğıthane manzarası: su, karşı kıyı tepeleri, kayıklar, köşkler (cami/minare yok)
  function bogaz(t, o = {}) {
    const g = o.gece ? .06 : .94;
    fill(R(-600, -500, 3100, 1100), g, { th: -.03, id: o.gece ? 1 : 10 });
    fill(Sm([[-600, 470], [-200, 420], [300, 450], [700, 400], [1200, 440], [1700, 410], [2500, 450], [2500, 560], [-600, 560]]), o.gece ? .03 : .45, { th: -.05, id: 9 });
    for (let k = 0; k < 14; k++) { const x = -300 + k * 190, y = 480 + rnd(k) * 30; fill(R(x, y - 20, 60, 30), o.gece ? .5 : .2, { th: H0, id: 9 }); }
    fill(R(-600, 560, 3100, 400), o.gece ? .12 : .7, { th: .01, id: 8 });
    // kayık bir servinin önünden ya da arkasından geçmez: dikey servi + yatay kayık haç silueti verir (Fable son okuması, 22 Kasım)
    const servis = o.servi || [[300, 480], [520, 420], [1950, 500]];
    for (let k = 0; k < 3; k++) { const x = 300 + k * 600 + Math.sin(t * .5 + k) * 20; if (servis.some(([sx]) => Math.abs(sx - x) < 190)) continue; fill(Sm([[x - 90, 640 + k * 30], [x + 90, 640 + k * 30], [x + 60, 660 + k * 30], [x - 60, 660 + k * 30]]), .08, { th: H0, id: 9 }); }
    if (o.kosk !== false) SET.kosk(o.kx ?? 1100, 900, o.kw ?? 700, 260, { gece: o.gece });
    for (const [x, h] of servis) SET.servi(x, 960, h);
    fill(R(-600, 900, 3100, 600), o.gece ? .1 : .35, { type: 'persp', y0: 900, D: 200, p0: 7, p1: 14, id: 8 });
  }
  // Osmanlı figürü: kaftan + kavuk/sarık; o.sultan için daha geniş kaftan ve yüksek kavuk
  function osmanli(o) { return INSAN.adam({ giysi: 'kaftan', sapka: o.sapka || 'kavuk', ...o }); }
  // çarşı: kemerli dükkânlar (sivil), tezgâhlarda saksılar
  function carsi(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .3, { th: H0, id: 0 });
    for (let k = 0; k < 6; k++) { const x = -100 + k * 360; fill(R(x, 220, 320, 520), .08, { th: HV, id: 9 }); fill(Sm([[x + 30, 740], [x + 30, 380], [x + 160, 300], [x + 290, 380], [x + 290, 740]]), .2, { th: HV, id: 9 }); fill(R(x + 30, 640, 260, 100), .4, { th: H0, id: 9 }); }
    fill(R(-600, 740, 3100, 800), .4, { type: 'persp', y0: 740, D: 200, p0: 7, p1: 14, id: 8 });
    if (o.lale !== false) for (let k = 0; k < 6; k++) { const x = 60 + k * 360; SET.saksi(x + 100, 640, .6); for (const [dx, dy, e] of [[-20, 6, -.25], [0, -10, 0], [20, 6, .25]]) LALE.ciz(x + 100 + dx, 590 + dy, .45, { sap: 34, tip: 'ist', cesit: (k + dx) % 2 ? 'ist' : 'istSari', egim: e }); }
  }
  // gemi (sürgün): tek direkli kadırga silueti, iskele
  function gemi(x, y, s = 1, t = 0) { fill(Sm([[x - 300 * s, y], [x + 320 * s, y], [x + 260 * s, y + 70 * s], [x - 240 * s, y + 70 * s]]), .06, { th: H0, id: 9 }); fill(R(x - 6 * s, y - 380 * s, 12 * s, 380 * s), .06, { th: HV, id: 9 }); fill(Sm([[x, y - 360 * s], [x + 200 * s, y - 120 * s + Math.sin(t) * 6], [x, y - 80 * s]]), .85, { th: .3, id: 10 }); }
  // ordu çadırları (Üsküdar): ufukta sıra çadırlar
  function cadirlar(t) {
    fill(R(-600, -500, 3100, 1100), .82, { th: -.03, id: 10 });
    fill(R(-600, 560, 3100, 900), .4, { type: 'persp', y0: 560, D: 220, p0: 7, p1: 14, id: 8 });
    for (let r = 0; r < 3; r++) for (let k = 0; k < 9; k++) { const x = -100 + k * 260 + r * 90, y = 640 + r * 90, s = .6 + r * .25; fill(F([[x - 90 * s, y], [x, y - 110 * s], [x + 90 * s, y]]), .2 + r * .05, { th: .9, id: 9 }); fill(F([[x - 6 * s, y], [x, y - 60 * s], [x + 6 * s, y]]), .05, { th: HV, id: 9 }); }
  }
  // kalabalık: sırtı dönük siluetler, meşale ışıkları (şiddet yok); o.n kişi, o.t
  function kalabalik(t, o = {}) {
    const n = o.n ?? 14;
    for (let i = 0; i < n; i++) { const r = i % 3, x = 100 + (i * 137) % 1800, y = 980 + r * 60; INSAN.adam({ x, y, h: 420 + r * 70, yon: i % 2 ? 1 : -1, arka: o.karisik ? i % 3 !== 1 : true, giysi: 'kaftan', sapka: i % 3 === 0 ? 'kavuk' : 'sarik', sarikTon: .45, kenar: .35, kolOn: { a: .3 + Math.sin(t * 2 + i) * .1, b: .4 } }); }
    for (let k = 0; k < (o.mesale ?? 3); k++) { const x = 400 + k * 520, y = 520 + Math.sin(t + k) * 6; fill(R(x - 4, y, 8, 140), .1, { th: HV, id: 9 }); SET.alev(x, y, t + k, 1.4); SET.isik({ x, y: y - 20, r1: 340, a: .7 }); }
  }
  // saray kapısı (gece): iki kule arasında kemerli kapı; kandil
  function sarayKapi(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .05, { th: -.05, id: 1 });
    fill(R(460, 200, 1000, 760), o.duvar ?? .14, { th: H0, id: 4 });
    for (const x of [380, 1460]) fill(R(x, 140, 160, 820), (o.duvar ?? .14) - .04, { th: HV, id: 4 });
    fill(R(760, 520, 400, 440), .03, { th: HV, id: 9 }); fill(R(956, 520, 8, 440), .25, { th: HV, id: 9 });   // düz, kapalı çift kanat ahşap kapı
    for (let k = 0; k < 4; k++) fill(R(760, 560 + k * 110, 400, 6), .2, { th: H0, id: 9 });
    fill(R(-600, 960, 3100, 600), .12, { type: 'persp', y0: 960, D: 200, p0: 7, p1: 14, id: 8 });
    const a = o.kandil ?? 1; fill(R(1250, 560, 10, 140), .2, { th: HV, id: 9 });
    if (a > .05) { SET.kandil(1255, 540, t, o.kandilS ?? 1.4); SET.isik({ x: 1255, y: 540, r1: (o.kandilR ?? 420) * a, a: .8 * a }); }
  }
  // sedir (boş taht yerine sivil oturma): uzun minder, yastıklar, pencere ışığı
  function sedir(t, o = {}) {
    fill(R(-600, -500, 3100, 1600), .12, { th: H0, id: 0 });
    for (let k = 0; k < 3; k++) { const x = 560 + k * 300; fill(R(x, 220, 240, 340), .8, { th: HV, id: 10 }); fill(R(x + 116, 220, 8, 340), .2, { th: HV, id: 9 }); }
    SET.huzme([[560, 560], [1400, 560], [1700, 1080], [300, 1080]], .25);
    fill(R(400, 640, 1120, 140), .3, { th: H0, id: 9 }); fill(R(400, 780, 1120, 60), .1, { th: H0, id: 9 });
    for (let k = 0; k < 4; k++) { fill(Sm([[480 + k * 260, 640], [480 + k * 260, 520], [640 + k * 260, 520], [640 + k * 260, 640]]), .55, { th: .35, id: 9 }); fill(R(556 + k * 260, 536, 8, 96), .3, { th: HV, id: 9 }); }   // yastık: çapraz tarama + dikiş (halka tarama hedef tahtası gibi okunuyordu)
    fill(R(-600, 840, 3100, 700), .28, { type: 'persp', y0: 840, D: 200, p0: 8, p1: 15, id: 8 });
  }
  // gazete sayfası (1913): başlık alanı, sütunlar; yazılar YAZI ile
  function gazete(x, y, w, h) { sayfa(x, y, w, h, { ton: .92 }); fill(R(x + 30, y + 130, w - 60, 4), .2, { th: H0, id: 9 }); for (let c = 0; c < 4; c++) satirlar(x + 40 + c * (w - 80) / 4, y + 200, (w - 80) / 4 - 30, Math.floor((h - 240) / 22), 22, { kalin: 2.5 }); }
  return { IMG, yukle, gorsel, sayfa, satirlar, masaUst, kalem, hokka, mumluk, para, kese, kisYolu, at, buket, sarik, mektupMasasi, leiden, hirsiz, aynaKabine, ekim, kesit, arkaOda, usta, defter, matbaa, tezgah, mackayOda, rihtim, bacaci, kitap, arsiv, bogaz, osmanli, carsi, gemi, cadirlar, kalabalik, sarayKapi, sedir, gazete };
})();
