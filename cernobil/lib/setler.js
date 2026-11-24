// Setler ve sahne nesneleri (Çernobil'in çayı). ORTAK DOSYA: yalnız başkan değiştirir.
// D (dekor.js) ve FIG (figur.js) üstüne kurulur. Hepsi BASKI plakalarına çizer.
'use strict';
const SET = (() => {
  const T = (B, d) => B.ton(d);
  const ink = (g, w = 2) => { g.strokeStyle = '#000'; g.fillStyle = '#000'; g.lineWidth = w; g.lineCap = 'round'; g.lineJoin = 'round'; };
  // düz zemin (ton) + alt yüzey (masa ya da döşeme)
  function zemin(B, d = .12, ufuk = 700, d2 = .3) { const k = B.k; k.save(); k.fillStyle = T(B, d); k.fillRect(-600, -600, W + 1200, ufuk + 600); k.fillStyle = T(B, d2); k.fillRect(-600, ufuk, W + 1200, H + 600); k.restore(); }
  // masa örtüsü / masa yüzü: kenar çizgisi + hafif ton
  function masa(B, y, d = .22, x0 = -300, x1 = W + 300) { const k = B.k, l = B.l; k.save(); k.fillStyle = T(B, d); k.fillRect(x0, y, x1 - x0, H + 400); k.restore(); l.save(); ink(l, 3); l.beginPath(); l.moveTo(x0, y); l.lineTo(x1, y); l.stroke(); l.restore(); }
  // el ve önkol (yakın plan): bardağı tutar ya da boştur. (x,y) bilek, a önkol açısı (0 = sağdan gelir), s ölçek, kav: parmakların kapanması 0..1
  // Kanal kuralı: havaya kalkmış düz kol yok — önkol hep çapraz ya da yatay; el bardak yüksekliğinde.
  function el(B, x, y, s, a = 0, o = {}) {
    const g = o.ton ? B.k : B.l; g.save(); g.translate(x, y); g.rotate(a); g.scale(o.f || 1, 1); g.fillStyle = o.ton ? T(B, o.ton) : '#000';
    // önkol (kol yeni, ceket kolu: manşet yok — beyaz dikdörtgen kuralı)
    g.beginPath(); g.moveTo(0, -26 * s); g.lineTo(420 * s, -40 * s); g.lineTo(420 * s, 46 * s); g.lineTo(0, 24 * s); g.closePath(); g.fill();
    // avuç ve parmaklar (sola bakan)
    g.beginPath(); g.ellipse(-26 * s, 0, 34 * s, 26 * s, 0, 0, TAU); g.fill();
    const kav = o.kav ?? .8;
    for (let i = 0; i < 4; i++) { const yy = -20 * s + i * 13 * s; g.beginPath(); g.ellipse(-58 * s + kav * 10 * s, yy, 18 * s, 6.5 * s, kav * .5, 0, TAU); g.fill(); }
    g.beginPath(); g.ellipse(-40 * s, -26 * s, 16 * s, 7 * s, -.6, 0, TAU); g.fill();   // başparmak
    g.restore();
  }
  // basın masası (1986): uzun masa, örtü, önde mikrofon demeti, masanın arkasında oturan figür (sırttan değil, mikrofonların arkasında gövde; yüz gölgede)
  function basinMasasi(B, t, o = {}) {
    zemin(B, o.duvar ?? .2, 640, .35);
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .3); for (let i = 0; i < 5; i++) k.fillRect(180 + i * 360, 120, 8, 520); k.restore();   // duvar panoları
    if (o.pencere) { k.save(); k.fillStyle = T(B, .05); k.fillRect(1420, 150, 360, 300); k.restore(); l.save(); ink(l, 6); l.strokeRect(1420, 150, 360, 300); l.beginPath(); l.moveTo(1600, 150); l.lineTo(1600, 450); l.moveTo(1420, 300); l.lineTo(1780, 300); l.stroke(); l.restore(); }
    // oturan konuşmacı: gövde ve baş siluet, yüz yok (baş öne eğik, ışık arkadan)
    if (o.konusmaci !== false) bust(B, o.kx ?? 960, 610, o.ks ?? 1.6, o.bas ?? 0);
    // masa
    k.save(); k.fillStyle = T(B, .55); k.fillRect(200, 600, 1520, 40); k.fillStyle = T(B, .4); k.fillRect(220, 640, 1480, 300); k.restore();
    l.save(); ink(l, 3); l.strokeRect(200, 600, 1520, 40); l.restore();
    D.mikrofonlar(B, o.mx ?? 960, 600, 1.1, o.mn ?? 7, 6);
  }
  // büst: masanın arkasında oturan biri (omuz, boyun, baş; yüz yok, ışık arkadan). bas: başın eğimi
  function bust(B, x, y, s, bas = 0) {
    const l = B.l; l.save(); l.fillStyle = '#000';
    l.beginPath(); l.moveTo(x - 150 * s, y); l.quadraticCurveTo(x - 150 * s, y - 120 * s, x - 60 * s, y - 135 * s); l.lineTo(x + 60 * s, y - 135 * s); l.quadraticCurveTo(x + 150 * s, y - 120 * s, x + 150 * s, y); l.closePath(); l.fill();
    l.fillRect(x - 22 * s, y - 170 * s, 44 * s, 45 * s);
    l.translate(x, y - 205 * s); l.rotate(bas); l.beginPath(); l.ellipse(0, 0, 44 * s, 54 * s, 0, 0, TAU); l.fill(); l.beginPath(); l.ellipse(-4 * s, -30 * s, 46 * s, 30 * s, 0, PI, TAU); l.fill(); l.restore();
  }
  // gazeteci sırtları (önde, kadrajın altında): kasket/saç, omuz, kalkık fotoğraf makineleri (dirsek bükük)
  function gazeteciler(B, t, o = {}) {
    const r = rng(o.tohum || 8), n = o.n || 6, y = o.y ?? 1180, l = B.l;
    for (let i = 0; i < n; i++) {
      const x = 120 + i * (W - 240) / (n - 1) + (r() - .5) * 60, s = (o.s || 1) * (.9 + r() * .25);
      l.save(); l.fillStyle = '#000';
      l.beginPath(); l.ellipse(x, y - 360 * s, 60 * s, 70 * s, 0, 0, TAU); l.fill();           // baş (arkadan)
      l.beginPath(); l.moveTo(x - 170 * s, y); l.quadraticCurveTo(x - 160 * s, y - 280 * s, x, y - 290 * s); l.quadraticCurveTo(x + 160 * s, y - 280 * s, x + 170 * s, y); l.closePath(); l.fill();   // omuzlar
      if (o.makine && r() < .6) { const sg = r() < .5 ? -1 : 1, cx = x + sg * 105 * s, cy = y - 380 * s - Math.sin(t * 2 + i) * 5; D.kamera(l, cx, cy, 2.4 * s);   // makine başın yanında, göz hizasında
        l.lineWidth = 36 * s; l.lineCap = 'round'; l.strokeStyle = '#000'; l.beginPath(); l.moveTo(x + sg * 130 * s, y - 230 * s); l.quadraticCurveTo(x + sg * 175 * s, y - 300 * s, cx + sg * 30 * s, cy + 20 * s); l.stroke(); }
      l.restore();
    }
  }
  // fotoğrafçı (profil, ayakta): makine yüzün önünde, iki dirsek bükük
  function fotografci(B, x, y, boy, f = 1) {
    const kk = FIG.kisi(B.l, x, y, boy, { tip: 'gazeteci', f, govde: .08, bas: -.02, kolO: [1.9, 1.45], kolA: [1.7, 1.5] });
    D.kamera(B.l, kk.bas[0] + f * kk.s * 9, kk.bas[1] - kk.s * 1, kk.s * .55); return kk;
  }
  // flaş zamanları: seçilmiş anlarda kısa patlama (t film zamanı)
  function flaslar(B, t, zamanlar) { let a = 0; for (const z of zamanlar) { const d = t - z; if (d >= 0 && d < .25) a = Math.max(a, 1 - d / .25); } D.flas(B, a); }
  // bakkal rafı: üç raf, paketler (genel "ÇAY" etiketi, marka yok), tarih damgası
  function bakkal(B, t, o = {}) {
    zemin(B, .25, 2000);
    const k = B.k, l = B.l, r = rng(o.tohum || 12);
    for (let j = 0; j < 3; j++) { const y = 300 + j * 250;
      k.save(); k.fillStyle = T(B, .55); k.fillRect(-100, y + 6, W + 200, 24); k.restore(); l.save(); ink(l, 3); l.beginPath(); l.moveTo(-100, y + 6); l.lineTo(W + 100, y + 6); l.stroke(); l.restore();
      for (let i = 0; i < 13; i++) { const x = 40 + i * 150 + (r() - .5) * 8; paket(B, x, y, 1, { yil: o.yil || '1986', d: .2 + r() * .15 }); } }
  }
  function paket(B, x, y, s, o = {}) {
    const k = B.k, l = B.l, w = 96 * s, h = 190 * s;
    k.save(); k.fillStyle = T(B, o.d ?? .2); k.fillRect(x - w / 2, y - h, w, h); k.fillStyle = T(B, .7); k.fillRect(x - w / 2, y - h * .62, w, h * .2); k.restore();
    l.save(); ink(l, 2 * s); l.strokeRect(x - w / 2, y - h, w, h); l.fillStyle = '#fff'; l.font = FONT.manset(Math.round(34 * s)); l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText('ÇAY', x, y - h * .52);
    if (o.yil) { l.fillStyle = '#000'; l.font = FONT.daktilo(Math.round(16 * s), 700); l.fillText(o.yil, x, y - h * .15); }
    if (o.sayi) { l.fillStyle = '#000'; l.font = FONT.daktilo(Math.round(14 * s), 700); l.fillText(o.sayi, x, y - h * .82); }
    l.restore();
  }
  // damga: kauçuk mühür (çift çerçeve, kalın yazı, hafif eğik); p: basılma (0 → 1 arası düşer)
  function damga(B, s, x, y, o = {}) {
    const p = clamp(o.p ?? 1); if (p <= 0) return; const l = B.l, sc = 1 + (1 - E.out3(p)) * 1.6;
    l.save(); l.translate(x, y); l.rotate(o.a ?? -.08); l.scale(sc, sc); l.globalAlpha = Math.min(1, p * 3) * .92; ink(l, 6);
    l.font = FONT.manset(o.px || 64); const w = l.measureText(s).width + 50, h = (o.px || 64) * 1.35;
    l.strokeRect(-w / 2, -h / 2, w, h); l.lineWidth = 2.5; l.strokeRect(-w / 2 + 9, -h / 2 + 9, w - 18, h - 18);
    l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText(s, 0, 3); l.restore();
  }
  // daktilo kâğıdı: beyaz sayfa, satırlar harf harf yazılır (p: 0..1 toplam), başlık satırları
  function daktilo(B, x, y, w, h, satirlar, p = 1, o = {}) {
    const k = B.k, l = B.l;
    k.save(); k.translate(10, 14); k.fillStyle = T(B, .3); k.fillRect(x, y, w, h); k.restore();
    k.save(); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
    l.save(); l.strokeStyle = T(B, .5); l.lineWidth = 1; l.strokeRect(x, y, w, h);
    const px = o.px || 30, top = satirlar.join('\n').length; let n = Math.floor(top * clamp(p)), yy = y + 60;
    l.fillStyle = '#000'; l.textBaseline = 'alphabetic'; l.textAlign = 'left';
    for (const s of satirlar) { const kalin = s.startsWith('!'); const tx = kalin ? s.slice(1) : s; l.font = FONT.daktilo(kalin ? px * 1.05 : px, kalin ? 700 : 400);
      const lines = wrapLines(l, tx, w - 100); for (const ln of lines) { if (n <= 0) break; l.fillText([...ln].slice(0, n).join(''), x + 50, yy); n -= [...ln].length + 1; yy += px * 1.45; } yy += px * .35; if (n <= 0) break; }
    l.restore();
  }
  // pano: mantar pano dokusu (ton), iğneler (siyah), kupürleri iğneler
  function pano(B, o = {}) { const k = B.k, r = rng(o.tohum || 40); k.save(); k.fillStyle = T(B, .42); k.fillRect(-300, -300, W + 600, H + 600); k.fillStyle = T(B, .55); for (let i = 0; i < 900; i++) { k.beginPath(); k.arc(r() * W, r() * H, 1 + r() * 2.4, 0, TAU); k.fill(); } k.restore(); }
  function igne(B, x, y, s = 1) { const l = B.l; l.save(); l.fillStyle = '#000'; l.beginPath(); l.arc(x, y, 12 * s, 0, TAU); l.fill(); l.fillStyle = '#fff'; l.beginPath(); l.arc(x - 4 * s, y - 4 * s, 3 * s, 0, TAU); l.fill(); l.restore(); }
  // demlik ve ocak: üst demlik, alt çaydanlık, buhar
  function demlik(B, x, y, s, t, o = {}) {
    // Türk çaydanlığı: altta geniş su çaydanlığı (yassı, yanda emzik), üstünde küçük demlik (emzik, kapak topuzu), sapları
    const k = B.k, l = B.l;
    const alt = g => { g.moveTo(x - 150 * s, y); g.lineTo(x - 130 * s, y - 130 * s); g.quadraticCurveTo(x, y - 175 * s, x + 130 * s, y - 130 * s); g.lineTo(x + 150 * s, y); g.closePath(); };
    const ust = g => { g.moveTo(x - 85 * s, y - 150 * s); g.quadraticCurveTo(x - 100 * s, y - 230 * s, x - 40 * s, y - 255 * s); g.lineTo(x + 40 * s, y - 255 * s); g.quadraticCurveTo(x + 100 * s, y - 230 * s, x + 85 * s, y - 150 * s); g.closePath(); };
    k.save(); k.beginPath(); alt(k); k.fillStyle = T(B, .55); k.fill(); k.beginPath(); ust(k); k.fillStyle = T(B, .4); k.fill(); k.restore();
    l.save(); ink(l, 3 * s); l.beginPath(); alt(l); l.stroke(); l.beginPath(); ust(l); l.stroke();
    l.lineWidth = 12 * s; l.beginPath(); l.moveTo(x + 135 * s, y - 70 * s); l.quadraticCurveTo(x + 200 * s, y - 90 * s, x + 225 * s, y - 150 * s); l.stroke();   // alt emzik
    l.lineWidth = 8 * s; l.beginPath(); l.moveTo(x + 85 * s, y - 190 * s); l.quadraticCurveTo(x + 130 * s, y - 200 * s, x + 145 * s, y - 240 * s); l.stroke();   // demlik emziği
    l.beginPath(); l.arc(x, y - 268 * s, 12 * s, 0, TAU); l.fill();
    l.lineWidth = 7 * s; l.beginPath(); l.arc(x - 115 * s, y - 95 * s, 40 * s, PI * .6, PI * 1.45); l.stroke(); l.restore();   // sap
    if (o.ocak) { l.save(); ink(l, 4 * s); l.strokeRect(x - 190 * s, y, 380 * s, 30 * s); l.restore(); }
    k.save(); k.strokeStyle = T(B, .25); k.lineWidth = 8 * s; k.lineCap = 'round'; for (let j = 0; j < 3; j++) { k.beginPath(); for (let u = 0; u <= 1; u += .05) { const yy = y - 160 * s - u * 260 * s, xx = x + 228 * s + Math.sin(u * 6 + t * 2 + j) * 20 * s * u + j * 10 * s; u ? k.lineTo(xx, yy) : k.moveTo(xx, yy); } k.stroke(); } k.restore();
  }
  // terazi: kefeli eski bakkal terazisi; sol/sağ kefe yükü fonksiyonla
  function terazi(B, x, y, s, a, solYuk, sagYuk) {
    const l = B.l, k = B.k; l.save(); ink(l, 5 * s);
    l.beginPath(); l.moveTo(x, y); l.lineTo(x, y - 300 * s); l.stroke(); l.fillRect(x - 90 * s, y - 10 * s, 180 * s, 20 * s);
    const c = Math.cos(a), sn = Math.sin(a), L = 300 * s, p1 = [x - L * c, y - 300 * s - L * sn], p2 = [x + L * c, y - 300 * s + L * sn];
    l.beginPath(); l.moveTo(p1[0], p1[1]); l.lineTo(p2[0], p2[1]); l.stroke();
    for (const [p, f] of [[p1, solYuk], [p2, sagYuk]]) { l.lineWidth = 2 * s; l.beginPath(); l.moveTo(p[0], p[1]); l.lineTo(p[0] - 90 * s, p[1] + 160 * s); l.moveTo(p[0], p[1]); l.lineTo(p[0] + 90 * s, p[1] + 160 * s); l.stroke();
      k.save(); k.fillStyle = T(B, .5); k.beginPath(); k.ellipse(p[0], p[1] + 165 * s, 110 * s, 22 * s, 0, 0, PI); k.fill(); k.restore(); l.lineWidth = 3 * s; l.beginPath(); l.ellipse(p[0], p[1] + 165 * s, 110 * s, 22 * s, 0, 0, PI); l.stroke();
      if (f) f(p[0], p[1] + 160 * s); }
    l.restore();
  }
  // yığın çay (kefe üstünde ya da yerde): kubbe biçimli, renk çay plakasında (ton: 0 yaş yaprak, .9 kuru siyah çay)
  function cayYigini(B, x, y, rx, ry, ton, sd = 3) {
    const r = rng(sd), yol = g => { g.ellipse(x, y, rx, ry, 0, PI, TAU); };
    B.cayBoya(yol, 1, ton);
    const k = B.k; k.save(); k.beginPath(); yol(k); k.clip(); k.fillStyle = T(B, ton > .7 ? .55 : .2); for (let i = 0; i < 160; i++) { const a = PI + r() * PI, rr = Math.sqrt(r()); k.beginPath(); k.ellipse(x + Math.cos(a) * rx * rr, y + Math.sin(a) * ry * rr, 6, 3, r() * PI, 0, TAU); k.fill(); } k.restore();
    const l = B.l; l.save(); ink(l, 2); l.beginPath(); yol(l); l.stroke(); l.restore();
  }
  // televizyon (1986): ahşap kasa, bombeli ekran; ekranın içinde fn ile çizim (ton plakasına, ekrana kırpılmış)
  function tv(B, x, y, s, ekran) {
    const k = B.k, l = B.l, w = 420 * s, h = 320 * s;
    k.save(); k.fillStyle = T(B, .6); k.fillRect(x - w / 2, y - h / 2, w, h); k.restore();
    const ex = x - w / 2 + 30 * s, ey = y - h / 2 + 30 * s, ew = w * .72, eh = h - 60 * s;
    k.save(); k.beginPath(); k.roundRect(ex, ey, ew, eh, 30 * s); k.fillStyle = T(B, .3); k.fill(); k.clip(); if (ekran) ekran(ex, ey, ew, eh); k.restore();
    l.save(); ink(l, 3 * s); l.strokeRect(x - w / 2, y - h / 2, w, h); l.beginPath(); l.roundRect(ex, ey, ew, eh, 30 * s); l.stroke();
    for (let i = 0; i < 3; i++) { l.beginPath(); l.arc(x + w / 2 - 50 * s, y - h / 2 + 70 * s + i * 70 * s, 16 * s, 0, TAU); l.fill(); } l.restore();
    l.save(); ink(l, 5 * s); l.beginPath(); l.moveTo(x - w / 2 + 40 * s, y + h / 2); l.lineTo(x - w / 2 + 20 * s, y + h / 2 + 70 * s); l.moveTo(x + w / 2 - 40 * s, y + h / 2); l.lineTo(x + w / 2 - 20 * s, y + h / 2 + 70 * s); l.stroke(); l.restore();
  }
  // saat (duvar saati): akrep ve yelkovan; saat: ondalık saat (ör. 13.5)
  function saat(B, x, y, r, sa) { const l = B.l, k = B.k; k.save(); k.fillStyle = '#fff'; k.beginPath(); k.arc(x, y, r, 0, TAU); k.fill(); k.restore(); l.save(); ink(l, r * .06); l.beginPath(); l.arc(x, y, r, 0, TAU); l.stroke();
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; l.beginPath(); l.moveTo(x + Math.sin(a) * r * .82, y - Math.cos(a) * r * .82); l.lineTo(x + Math.sin(a) * r * .94, y - Math.cos(a) * r * .94); l.stroke(); }
    const ak = (sa % 12) / 12 * TAU, yk = (sa % 1) * TAU; l.lineWidth = r * .08; l.beginPath(); l.moveTo(x, y); l.lineTo(x + Math.sin(ak) * r * .5, y - Math.cos(ak) * r * .5); l.stroke(); l.lineWidth = r * .05; l.beginPath(); l.moveTo(x, y); l.lineTo(x + Math.sin(yk) * r * .78, y - Math.cos(yk) * r * .78); l.stroke(); l.restore(); }
  // kesit: toprak katmanı ve içinde çuvallar (gömü); renk çuvalların ağzında söner (sön: 0 renkli → 1 sönük)
  function gomu(B, x, y, w, h, son, o = {}) {
    const k = B.k, r = rng(o.tohum || 55);
    k.save(); k.fillStyle = T(B, .62); k.fillRect(x - w / 2, y, w, h); k.fillStyle = T(B, .78); for (let i = 0; i < 400; i++) { k.beginPath(); k.arc(x - w / 2 + r() * w, y + r() * h, 1 + r() * 3, 0, TAU); k.fill(); } k.restore();
    for (let i = 0; i < (o.n || 7); i++) D.cuval(B, x - w * .35 + i * w * .7 / Math.max(1, (o.n || 7) - 1), y + h * .75 + (i % 2) * 20, 1.6, { d: .7, cay: 1 - son, ton: .7 });
    const l = B.l; l.save(); ink(l, 3); l.beginPath(); l.moveTo(x - w / 2, y); l.lineTo(x + w / 2, y); l.stroke(); l.restore();
  }
  // çubuk grafik (gazete grafiği): değerler [etiket, oran 0..1], p büyüme
  function cubuklar(B, x, y, w, h, veri, p = 1) { const k = B.k, l = B.l, n = veri.length, bw = w / n * .6;
    veri.forEach(([et, v, d], i) => { const bx = x + i * w / n + (w / n - bw) / 2, bh = h * v * E.out3(clamp(p * 1.4 - i * .2)); k.save(); k.fillStyle = T(B, d ?? .7); k.fillRect(bx, y - bh, bw, bh); k.restore();
      l.save(); ink(l, 2); l.strokeRect(bx, y - bh, bw, bh); l.font = FONT.daktilo(40, 700); l.textAlign = 'center'; l.textBaseline = 'top'; l.fillText(et, bx + bw / 2, y + 16); l.textBaseline = 'bottom'; if (bh > 2) l.fillText('%' + Math.round(v * 100), bx + bw / 2, y - bh - 10); l.restore(); });
    l.save(); ink(l, 3); l.beginPath(); l.moveTo(x - 20, y); l.lineTo(x + w + 20, y); l.stroke(); l.restore(); }
  return { zemin, masa, el, bust, fotografci, basinMasasi, gazeteciler, flaslar, bakkal, paket, damga, daktilo, pano, igne, demlik, terazi, cayYigini, tv, saat, gomu, cubuklar };
})();
