// Dekor ve nesneler (Çernobil'in çayı). ORTAK DOSYA: yalnız başkan değiştirir.
// Hepsi BASKI plakalarına çizer: B.k ton (tram), B.l çizgi (düz mürekkep), B.c çay (renk). Dünya koordinatı; kamera B.cam ile.
// Kural: radyasyon çizilmez (parıltı, parçacık, yonca yok). Renk yalnız çayda (yaprak yeşil → bakır → kehribar dem).
'use strict';
const D = (() => {
  const T = (B, d) => B.ton(d);
  // ── Karadeniz yamacı: katmanlı dağlar (uzak açık ton, yakın koyu), sis bantları, çay sıraları ──
  function daglar(B, o = {}) {
    const k = B.k, y0 = o.y ?? 520, sd = o.tohum || 3;
    const kat = o.kat || [[.18, 0], [.3, 90], [.45, 190]];
    kat.forEach(([d, dy], i) => {
      k.save(); k.beginPath(); k.moveTo(-400, H + 400);
      for (let x = -400; x <= W + 400; x += 20) k.lineTo(x, y0 + dy - 120 * fbm1(x / (520 - i * 90), sd + i, 3) - 60 * Math.sin(x / 700 + i));
      k.lineTo(W + 400, H + 400); k.closePath(); k.fillStyle = T(B, d); k.fill(); k.restore();
      // sis bandı (katın eteğinde açık şerit)
      k.save(); const g = k.createLinearGradient(0, y0 + dy + 40, 0, y0 + dy - 60); g.addColorStop(0, 'rgba(255,255,255,.75)'); g.addColorStop(1, 'rgba(255,255,255,0)');
      k.fillStyle = g; k.fillRect(-400, y0 + dy - 60, W + 800, 100); k.restore();
    });
  }
  // çay sıraları: eğimli yamaçta kontur boyunca yuvarlak çalı sıraları (ton + çizgi), ön sırada sürgün uçları (çay plakası yeşil)
  function bahce(B, o = {}) {
    const k = B.k, l = B.l, x0 = o.x0 ?? -260, x1 = o.x1 ?? W + 260, y0 = o.y0 ?? 560, y1 = o.y1 ?? H + 80, n = o.sira || 9, sd = o.tohum || 11;
    const r = rng(sd);
    for (let i = 0; i < n; i++) {
      const u = i / Math.max(1, n - 1), y = lerp(y0, y1, Math.pow(u, 1.5)), s = lerp(.4, 1.7, Math.pow(u, 1.4)), egim = o.egim ?? -.06;
      const d = lerp(.5, .8, u);
      for (let x = x0 + (i % 2) * 30 * s; x < x1; x += (62 + r() * 16) * s) {
        const yy = y + (x - W / 2) * egim + Math.sin(x / 300 + i) * 12 * s, rr = (30 + r() * 10) * s;
        const yol = g => { g.moveTo(x - rr * 1.2, yy + rr * .25); for (let a = 0; a <= 1; a += .1) { const th = PI + a * PI; const bump = 1 + .12 * Math.sin(a * 23 + x); g.lineTo(x + Math.cos(th) * rr * 1.2 * bump, yy + Math.sin(th) * rr * .8 * bump); } g.lineTo(x + rr * 1.2, yy + rr * .25); g.closePath(); };
        k.save(); k.beginPath(); yol(k); k.fillStyle = T(B, d); k.fill(); k.clip();
        const g = k.createRadialGradient(x - rr * .3, yy - rr * .7, 0, x, yy - rr * .3, rr * 1.3); g.addColorStop(0, T(B, d * .45)); g.addColorStop(1, 'rgba(255,255,255,0)'); k.fillStyle = g; k.fillRect(x - rr * 1.4, yy - rr, rr * 2.8, rr * 1.4);
        k.restore();
        if (u > .45) { l.save(); l.strokeStyle = '#000'; l.lineWidth = 1.3 * s; l.beginPath(); yol(l); l.stroke(); for (let j = 0; j < 5; j++) { const a = PI + .3 + r() * (PI - .6), px = x + Math.cos(a) * rr * .8, py = yy + Math.sin(a) * rr * .5; l.beginPath(); l.moveTo(px, py); l.lineTo(px + 6 * s, py - 4 * s); l.stroke(); } l.restore(); }
        if (o.surgun && u > .35) { const m = Math.round(2 + r() * 3); for (let j = 0; j < m; j++) { const a = PI + .35 + r() * (PI - .7); const px = x + Math.cos(a) * rr * 1.15, py = yy + Math.sin(a) * rr * .78;
          B.cayBoya(gg => { gg.ellipse(px, py - 3 * s, 3.4 * s, 6.5 * s, a + PI / 2, 0, TAU); }, o.surgun, 0); } }
      }
    }
  }
  // yamaç evi (Karadeniz): dik çatılı, iki katlı küçük ev; ton + çizgi
  function ev(B, x, y, s, o = {}) {
    const k = B.k, l = B.l, w = 90 * s, h = 70 * s;
    k.save(); k.fillStyle = T(B, o.d ?? .3); k.fillRect(x - w / 2, y - h, w, h); k.fillStyle = T(B, .7); k.beginPath(); k.moveTo(x - w / 2 - 10 * s, y - h); k.lineTo(x, y - h - 40 * s); k.lineTo(x + w / 2 + 10 * s, y - h); k.closePath(); k.fill(); k.restore();
    l.save(); l.fillStyle = '#000'; for (let i = 0; i < 3; i++) l.fillRect(x - w / 2 + 12 * s + i * 26 * s, y - h + 16 * s, 12 * s, 16 * s); l.restore();
  }
  // tek çay yaprağı: tırtıklı kenar, orta damar; renk çay plakasında (ton: 0 yeşil, .5 bakır, 1 kehribar), kenar çizgi plakasında
  function yaprak(B, x, y, s, a = 0, o = {}) {
    const pts = []; const n = 28;
    for (let i = 0; i <= n; i++) { const u = i / n, th = u * TAU; const rx = 8 * s, ry = 20 * s; let px = Math.sin(th) * rx * (1 - .25 * Math.cos(th)), py = -Math.cos(th) * ry;
      const dis = (i % 2 ? .93 : 1); pts.push([px * dis, py]); }
    const yol = g => { g.save(); g.translate(x, y); g.rotate(a); g.moveTo(pts[0][0], pts[0][1]); for (const p of pts) g.lineTo(p[0], p[1]); g.closePath(); g.restore(); };
    if (o.ton !== false) B.cayBoya(yol, o.d ?? 1, o.renk ?? 0);
    const k = B.k; k.save(); k.translate(x, y); k.rotate(a); k.beginPath(); for (const p of pts) k.lineTo(p[0] * .96, p[1] * .96); k.closePath(); k.fillStyle = T(B, o.gol ?? .12); k.fill(); k.restore();
    const l = B.l; l.save(); l.translate(x, y); l.rotate(a); l.strokeStyle = '#000'; l.lineWidth = Math.max(1, s * .55); l.lineJoin = 'round';
    l.beginPath(); for (const p of pts) l.lineTo(p[0], p[1]); l.closePath(); l.stroke();
    l.lineWidth = Math.max(.8, s * .4); l.beginPath(); l.moveTo(0, 20 * s); l.lineTo(0, -18 * s); l.stroke();
    for (let j = -3; j <= 3; j++) { if (!j) continue; const yy = j * 4.6 * s; l.beginPath(); l.moveTo(0, yy); l.quadraticCurveTo(3 * s * Math.sign(j), yy - 3 * s, 6 * s, yy - 6 * s); l.stroke(); l.beginPath(); l.moveTo(0, yy); l.quadraticCurveTo(-3 * s, yy - 3 * s, -6 * s, yy - 6 * s); l.stroke(); }
    if (o.sap !== false) { l.lineWidth = Math.max(1.4, s * .9); l.beginPath(); l.moveTo(0, 20 * s); l.quadraticCurveTo(2 * s, 28 * s, 5 * s, 36 * s); l.stroke(); }
    l.restore();
  }
  // yağmur: ince eğik çizgiler (ton plakası; tramda kırık noktalı görünür), t ile akar
  function yagmur(B, t, o = {}) {
    const k = B.k, r = rng(o.tohum || 5), n = o.n || 260, ac = o.aci ?? .18, h = o.boy || 70, v = o.hiz || 1400;
    k.save(); k.strokeStyle = T(B, o.d ?? .5); k.lineWidth = o.w || 1.6; k.lineCap = 'round';
    for (let i = 0; i < n; i++) { const x0 = r() * (W + 400) - 200, ph = r(); const y = ((ph * (H + 300) + t * v * (.8 + r() * .4)) % (H + 300)) - 150; const x = x0 + y * ac;
      k.beginPath(); k.moveTo(x, y); k.lineTo(x - h * ac, y - h); k.stroke(); }
    k.restore();
  }
  // gökyüzü bulutları (yağmur bulutu): koyu ton, alt kenarı yırtık; t ile kayar. Radyasyon değil, bulut.
  function bulutlar(B, t, o = {}) {
    const k = B.k, y = o.y ?? 160, d = o.d ?? .55, sd = o.tohum || 9;
    k.save(); k.beginPath(); k.moveTo(-200, -200);
    for (let x = -200; x <= W + 200; x += 16) k.lineTo(x, y + 90 * fbm1((x + t * (o.hiz || 20)) / 300, sd, 4));
    k.lineTo(W + 200, -200); k.closePath(); const g = k.createLinearGradient(0, -100, 0, y + 100); g.addColorStop(0, T(B, d + .15)); g.addColorStop(1, T(B, d)); k.fillStyle = g; k.fill(); k.restore();
  }
  // ── gazete kupürü: kâğıt parçası (yırtık kenar, hafif gölge), manşet, sütunlar, vurgulu alıntı. Çizgi plakasında (notext'te de kalır: sahnenin parçası).
  // o: {w, h, manset, ust (gazete adı ve tarih satırı), alinti (okunacak söz), px (alıntı punto), sutun (sütun sayısı), a (dönme), p (0..1 yazılma; alıntı harf harf), golge}
  function kupur(B, x, y, o = {}) {
    const k = B.k, l = B.l, w = o.w || 760, h = o.h || 520, r = rng(o.tohum || 21);
    const kenar = []; const N = 60;
    for (let i = 0; i < N; i++) { const u = i / N; let px, py; if (u < .25) { px = -w / 2 + u * 4 * w; py = -h / 2; } else if (u < .5) { px = w / 2; py = -h / 2 + (u - .25) * 4 * h; } else if (u < .75) { px = w / 2 - (u - .5) * 4 * w; py = h / 2; } else { px = -w / 2; py = h / 2 - (u - .75) * 4 * h; }
      kenar.push([px + (r() - .5) * 7, py + (r() - .5) * 7]); }
    const yol = g => { g.moveTo(kenar[0][0], kenar[0][1]); for (const p of kenar) g.lineTo(p[0], p[1]); g.closePath(); };
    for (const g of [k, l]) { g.save(); g.translate(x, y); g.rotate(o.a || 0); }
    if (o.golge !== false) { k.save(); k.translate(10, 14); k.beginPath(); yol(k); k.fillStyle = T(B, .35); k.filter = 'blur(6px)'; k.fill(); k.restore(); }
    l.save(); l.beginPath(); yol(l); l.fillStyle = '#fff'; l.fill(); l.restore(); B.c.save(); B.c.translate(x, y); B.c.rotate(o.a || 0); B.c.beginPath(); yol(B.c); B.c.fillStyle = '#000'; B.c.fill(); B.c.restore();
    k.beginPath(); yol(k); k.fillStyle = '#fff'; k.fill();                        // kupür kâğıdı: tramsız (zemin kâğıdından ayrışsın diye çevresinde gölge)
    l.save(); l.beginPath(); yol(l); l.clip();
    l.fillStyle = '#000'; let yy = -h / 2 + 34;
    if (o.ust) { l.font = FONT.daktilo(20, 700); l.textAlign = 'left'; l.textBaseline = 'middle'; l.fillText(o.ust, -w / 2 + 26, yy); l.fillRect(-w / 2 + 26, yy + 16, w - 52, 2); yy += 40; }
    if (o.manset) { const mp = o.mpx || 66; l.font = FONT.manset(mp); l.textAlign = 'left'; l.textBaseline = 'top'; for (const ln of wrapLines(l, o.manset, w - 52)) { l.fillText(ln, -w / 2 + 26, yy); yy += mp * 1.08; } yy += 10; }
    // sütunlar: okunmayan dizgi dokusu (ince çizgiler)
    const sut = o.sutun ?? 3, sw = (w - 52 - (sut - 1) * 18) / sut, altY = o.alinti ? h / 2 - (o.ah || 190) : h / 2 - 20;
    for (let c = 0; c < sut; c++) { const cx = -w / 2 + 26 + c * (sw + 18); for (let ly = yy; ly < altY; ly += 13) { const L = sw * (ly > altY - 20 || r() < .08 ? .5 + r() * .4 : .96); l.fillRect(cx, ly, L, 5.2); } }
    if (o.alinti) {  // vurgulu alıntı: kutu içinde iri italik; p ile harf harf belirir
      const px = o.px || 46, ay = h / 2 - (o.ah || 190) + 14; l.fillRect(-w / 2 + 26, ay - 8, w - 52, 3);
      l.font = FONT.alinti(px, 600); l.textAlign = 'left'; l.textBaseline = 'top';
      const s = o.alinti, nn = Math.ceil([...s].length * clamp(o.p ?? 1)); const vis = [...s].slice(0, nn).join('');
      let yy2 = ay + 8; const lines = wrapLines(l, s, w - 70); let used = 0;
      for (const ln of lines) { const part = [...vis].slice(used, used + [...ln].length).join(''); l.fillText(part, -w / 2 + 34, yy2); used += [...ln].length + 1; yy2 += px * 1.14; }
    }
    l.restore();
    l.save(); l.strokeStyle = T(B, .6); l.lineWidth = 1; l.beginPath(); yol(l); l.stroke(); l.restore();
    for (const g of [k, l]) g.restore();
  }
  // sayı: radyasyonun görüntüdeki tek biçimi. Dizgi rakamları (Courier kalın), birimi küçük. p: belirme (rakamlar sayar gibi dönerek yerine oturur)
  function sayi(B, s, x, y, o = {}) {
    const l = B.l, px = o.px || 180; const p = clamp(o.p ?? 1); if (p <= 0) return;
    l.save(); l.translate(x, y); l.fillStyle = '#000'; l.textAlign = o.align || 'center'; l.textBaseline = 'alphabetic';
    l.font = FONT.daktilo(px, 700);
    // belirme: dizgi soldan sağa daktilo gibi basılır; ara karede hiçbir zaman yanlış rakam görünmez (Fable son okuması)
    const gs = s, wd = l.measureText(s).width, al = o.align || 'center', x0 = al === 'center' ? -wd / 2 : al === 'right' ? -wd : 0;
    const nGor = p < 1 ? Math.floor(p * s.length + .5) : s.length;
    if (nGor > 0) { l.textAlign = 'left'; l.fillText([...s].slice(0, nGor).join(''), x0, 0); l.textAlign = al; }
    if (o.birim && p >= 1) { l.font = FONT.daktilo(Math.round(px * .3), 700); l.textAlign = 'left'; const bx = (o.align || 'center') === 'center' ? wd / 2 + 16 : (o.align === 'left' ? wd + 16 : 16); l.fillText(o.birim, bx, 0); }
    l.restore();
  }
  // ince belli çay bardağı (yakın plan): cam kenarı çizgi, dem çay plakasında (kehribar), tabak ve kaşık; dolu: 0..1, buhar: t
  function bardak(B, x, y, s, o = {}) {
    const l = B.l, k = B.k, dolu = o.dolu ?? .85;
    const prof = u => { const a = 20, b = 13, c = 22; return u < .55 ? lerp(c, b, E.sine(u / .55)) : lerp(b, a, E.sine((u - .55) / .45)); };  // u 0 alt → 1 üst; yarıçap
    const yH = 92 * s, yol = (g, ust = 1) => { g.moveTo(x - prof(0) * s, y); for (let u = 0; u <= ust; u += .04) g.lineTo(x - prof(u) * s, y - u * yH); for (let u = ust; u >= 0; u -= .04) g.lineTo(x + prof(u) * s, y - u * yH); g.closePath(); };
    if (o.tabak !== false) { k.save(); k.beginPath(); k.ellipse(x, y + 4 * s, 46 * s, 9 * s, 0, 0, TAU); k.fillStyle = T(B, .45); k.fill(); k.restore(); l.save(); l.strokeStyle = '#000'; l.lineWidth = 2 * s; l.beginPath(); l.ellipse(x, y + 4 * s, 46 * s, 9 * s, 0, 0, TAU); l.stroke(); l.restore(); }
    if (dolu > 0) { B.cayBoya(g => yol(g, dolu), o.d ?? 1, o.renk ?? 1); k.save(); k.beginPath(); yol(k, dolu); k.fillStyle = T(B, .25); k.fill(); k.restore(); }
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 2.4 * s; l.beginPath(); yol(l, 1); l.stroke();
    l.lineWidth = 1.6 * s; l.beginPath(); l.ellipse(x, y - yH, prof(1) * s, 3.4 * s, 0, 0, TAU); l.stroke();
    if (dolu > 0) { l.lineWidth = 1.2 * s; l.beginPath(); l.ellipse(x, y - dolu * yH, prof(dolu) * s, 2.6 * s, 0, 0, TAU); l.stroke(); }
    // cam parıltısı: kâğıt açıklığı (çizgi ve tondan sil)
    for (const g of [k, l]) { g.save(); g.fillStyle = '#fff'; g.beginPath(); g.ellipse(x - prof(.75) * s * .55, y - yH * .72, 2.6 * s, 14 * s, -.05, 0, TAU); g.fill(); g.restore(); }
    B.c.save(); B.c.globalCompositeOperation = 'source-over'; B.c.fillStyle = '#000'; B.c.beginPath(); B.c.ellipse(x - prof(.75) * s * .55, y - yH * .72, 2.6 * s, 14 * s, -.05, 0, TAU); B.c.fill(); B.c.restore();
    l.restore();
    if (o.kasik) { l.save(); l.strokeStyle = '#000'; l.lineWidth = 3 * s; l.lineCap = 'round'; l.beginPath(); l.moveTo(x + 8 * s, y - yH * .9); l.lineTo(x + 26 * s, y - yH * 1.25); l.stroke(); l.restore(); }
    if (o.buhar != null) { k.save(); k.strokeStyle = T(B, .22); k.lineWidth = 5 * s; k.lineCap = 'round'; const t = o.buhar;
      for (let j = 0; j < 3; j++) { k.beginPath(); for (let u = 0; u <= 1; u += .05) { const yy = y - yH - 6 * s - u * 70 * s, xx = x + (j - 1) * 9 * s + Math.sin(u * 5 + t * 1.6 + j * 2) * 7 * s * u; u ? k.lineTo(xx, yy) : k.moveTo(xx, yy); } k.globalAlpha = .8; k.stroke(); } k.restore(); }
    return { ust: y - yH, alt: y, r: prof(1) * s };
  }
  // mikrofon demeti (basın masası): sapları ve başlıkları siluet; kurum yazısı yok
  function mikrofonlar(B, x, y, s, n = 5, sd = 4) {
    const l = B.l, r = rng(sd); l.save(); l.fillStyle = '#000'; l.strokeStyle = '#000';
    for (let i = 0; i < n; i++) { const a = (i - (n - 1) / 2) * .16 + (r() - .5) * .1, L = (110 + r() * 60) * s, bx = x + Math.sin(a) * L, by = y - Math.cos(a) * L;
      l.lineWidth = 6 * s; l.beginPath(); l.moveTo(x + (i - n / 2) * 12 * s, y); l.lineTo(bx, by); l.stroke(); l.fillRect(x + (i - n / 2) * 12 * s - 14 * s, y - 6 * s, 28 * s, 8 * s);
      l.beginPath(); l.ellipse(bx, by, 13 * s, 18 * s, a, 0, TAU); l.fill(); l.fillRect(bx - 11 * s, by + 12 * s, 22 * s, 10 * s); }
    l.restore();
  }
  // flaş: o karede bütün mürekkebi açar (fotoğraf patlaması). a 0..1. Sahnenin sonunda çağrılır.
  function flas(B, a) {
    if (a <= 0) return;
    for (const g of [B.k, B.l]) { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = clamp(a) * .85; g.fillStyle = '#fff'; g.fillRect(0, 0, DW, DH); g.restore(); }
  }
  // fotoğraf makinesi tutan eller ve gövde (gazeteci siluetinin önünde)
  function kamera(g, x, y, s) { g.save(); g.fillStyle = '#000'; g.fillRect(x - 22 * s, y - 14 * s, 44 * s, 28 * s); g.beginPath(); g.arc(x, y, 11 * s, 0, TAU); g.fill(); g.fillRect(x - 8 * s, y - 22 * s, 16 * s, 9 * s); g.restore(); }
  // çuval: YATIK jüt çuvalı (yastık biçimi, köşelerde kulak, ortada dikiş). Dik, yuvarlak tepeli çuval sıra hâlinde mezar taşı okunur: kullanılmaz.
  // (x, y) çuvalın alt orta noktası. o.cay: ağzından görünen çay (çay plakası)
  function cuval(B, x, y, s, o = {}) {
    const k = B.k, l = B.l, w = 34 * s, h = 15 * s, cy = y - h;
    const yol = g => { g.moveTo(x - w, cy - h * .7); g.quadraticCurveTo(x - w * .5, cy - h * 1.25, x, cy - h * 1.1); g.quadraticCurveTo(x + w * .5, cy - h * 1.25, x + w, cy - h * .7);
      g.quadraticCurveTo(x + w * 1.12, cy, x + w, cy + h * .75); g.quadraticCurveTo(x, cy + h * 1.1, x - w, cy + h * .75); g.quadraticCurveTo(x - w * 1.12, cy, x - w, cy - h * .7); g.closePath(); };
    const d = o.d ?? .55;
    k.save(); k.beginPath(); yol(k); k.fillStyle = T(B, d); k.fill(); k.clip(); k.strokeStyle = T(B, Math.min(1, d + .18)); k.lineWidth = 1.1;
    for (let i = -8; i <= 8; i++) { k.beginPath(); k.moveTo(x + i * 4.2 * s, cy - h * 1.3); k.lineTo(x + i * 4.2 * s + 3 * s, cy + h * 1.2); k.stroke(); }
    const g2 = k.createLinearGradient(0, cy - h, 0, cy + h); g2.addColorStop(0, 'rgba(255,255,255,.35)'); g2.addColorStop(1, 'rgba(255,255,255,0)'); k.fillStyle = g2; k.fillRect(x - w * 1.2, cy - h * 1.3, w * 2.4, h * 1.4); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 1.5 * s; l.beginPath(); yol(l); l.stroke();
    l.lineWidth = 1 * s; l.setLineDash([3 * s, 3 * s]); l.beginPath(); l.moveTo(x - w * .8, cy - h * .1); l.quadraticCurveTo(x, cy + h * .15, x + w * .8, cy - h * .1); l.stroke(); l.setLineDash([]);
    l.lineWidth = 2.4 * s; l.beginPath(); l.moveTo(x + w * .95, cy - h * .75); l.lineTo(x + w * 1.12, cy - h * 1.05); l.moveTo(x - w * .95, cy - h * .75); l.lineTo(x - w * 1.12, cy - h * 1.05); l.stroke(); l.restore();   // kulaklar
    if (o.cay) B.cayBoya(g => { g.ellipse(x + w * .95, cy, 4 * s, 7 * s, 0, 0, TAU); }, o.cay, o.ton ?? .55);
  }
  // çuval yığını: yatık çuvallar tuğla düzeninde (kat kat), naylon örtü isteğe bağlı (buruşuk, kubbe değil)
  function yigin(B, x, y, s, o = {}) {
    const kat = o.kat || 5, gen = o.gen || 9, r = rng(o.tohum || 3);
    for (let j = 0; j < kat; j++) { const n = gen - Math.floor(j / 2); for (let i = 0; i < n; i++) cuval(B, x + (i - (n - 1) / 2) * 66 * s + (j % 2) * 33 * s + (r() - .5) * 6 * s, y - j * 28 * s, s * (.95 + r() * .1), { d: .5 + r() * .25, cay: o.cay && j === kat - 1 && i === 1 ? o.cay : 0 }); }
    if (o.naylon) { const k = B.k, w = gen * 66 * s, h = kat * 28 * s + 20 * s, t = o.t || 0;
      k.save(); k.globalAlpha = .5; k.fillStyle = T(B, .18); k.beginPath(); k.moveTo(x - w / 2 - 20 * s, y - h * .25);
      for (let u = 0; u <= 1; u += .04) k.lineTo(x - w / 2 + u * w, y - h - 14 * s * Math.sin(u * 17 + t * 2) - 10 * s * Math.sin(u * 5));
      k.lineTo(x + w / 2 + 20 * s, y - h * .25); for (let u = 1; u >= 0; u -= .05) k.lineTo(x - w / 2 + u * w, y - h * .3 + 12 * s * Math.sin(u * 11 + t)); k.closePath(); k.fill(); k.restore(); }
  }
  // fabrika: çay fabrikası cephesi (uzun yapı, baca, pencere sıraları); ton + çizgi
  function fabrika(B, x, y, s, o = {}) {
    const k = B.k, l = B.l, w = 620 * s, h = 180 * s;
    k.save(); k.fillStyle = T(B, o.d ?? .4); k.fillRect(x - w / 2, y - h, w, h); k.fillStyle = T(B, (o.d ?? .4) + .25); k.beginPath(); k.moveTo(x - w / 2 - 14 * s, y - h); k.lineTo(x, y - h - 70 * s); k.lineTo(x + w / 2 + 14 * s, y - h); k.closePath(); k.fill();
    k.fillRect(x + w * .32, y - h - 210 * s, 34 * s, 210 * s); k.restore();
    l.save(); l.fillStyle = '#000'; for (let i = 0; i < 9; i++) for (let j = 0; j < 2; j++) l.fillRect(x - w / 2 + 30 * s + i * 66 * s, y - h + 30 * s + j * 70 * s, 34 * s, 42 * s);
    l.strokeStyle = '#000'; l.lineWidth = 2 * s; l.strokeRect(x - w / 2, y - h, w, h); l.restore();
    if (o.duman != null) { const t = o.duman; k.save(); k.fillStyle = T(B, .2); for (let i = 0; i < 9; i++) { const u = ((t * .08 + i / 9) % 1); k.globalAlpha = (1 - u) * .8; k.beginPath(); k.arc(x + w * .32 + 17 * s + u * 140 * s, y - h - 220 * s - u * 200 * s, (14 + u * 50) * s, 0, TAU); k.fill(); } k.restore(); }
  }
  // depo içi: uzun çatı makasları, kolonlar, loş ışık; ton
  function depoIc(B, o = {}) {
    const k = B.k, l = B.l;
    const dd = o.d ?? .5; k.save(); k.fillStyle = T(B, dd); k.fillRect(-200, -200, W + 400, H + 400);
    const g = k.createLinearGradient(0, 0, 0, H); g.addColorStop(0, T(B, dd + .2)); g.addColorStop(.6, T(B, dd - .15)); g.addColorStop(1, T(B, dd + .05)); k.fillStyle = g; k.fillRect(-200, 0, W + 400, H);
    for (let i = 0; i < 6; i++) { const x = 120 + i * 340; k.fillStyle = 'rgba(255,255,255,.35)'; k.beginPath(); k.moveTo(x, 80); k.lineTo(x + 60, 80); k.lineTo(x + 260, H); k.lineTo(x + 120, H); k.closePath(); k.fill(); }   // çatı aralığından düşen gün ışığı
    k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; for (let i = 0; i < 7; i++) { const x = i * 330 - 60; l.beginPath(); l.moveTo(x, 260); l.lineTo(x + 165, 60); l.lineTo(x + 330, 260); l.stroke(); l.beginPath(); l.moveTo(x, 260); l.lineTo(x, H); l.stroke(); }
    l.beginPath(); l.moveTo(-100, 260); l.lineTo(W + 100, 260); l.stroke(); l.restore();
  }
  // çit: beton direkler ve tel örgü (baklava ağ, açık ton). Dikenli tel çizilmez (kamp çağrışımı). o.bozuk: bir aralık açık
  function cit(B, x0, x1, y, s, o = {}) {
    const l = B.l, k = B.k, h = 130 * s, acik = x => o.bozuk && Math.abs(x - o.bozuk) < 70 * s;
    k.save(); k.strokeStyle = T(B, .45); k.lineWidth = 1.2 * s;
    for (let x = x0; x < x1; x += 18 * s) { if (acik(x)) continue; k.beginPath(); k.moveTo(x, y); k.lineTo(x + 18 * s, y - h); k.moveTo(x + 18 * s, y); k.lineTo(x, y - h); k.stroke(); }
    k.restore();
    l.save(); l.fillStyle = '#000'; l.strokeStyle = '#000'; l.lineWidth = 2 * s;
    for (let x = x0; x <= x1; x += 180 * s) { if (acik(x)) continue; l.fillRect(x - 5 * s, y - h - 10 * s, 10 * s, h + 10 * s); }
    l.beginPath(); for (let x = x0; x <= x1; x += 8 * s) { if (acik(x)) { l.stroke(); l.beginPath(); continue; } l.lineTo(x, y - h); } l.stroke();
    if (o.bozuk) { l.lineWidth = 1.4 * s; l.beginPath(); l.moveTo(o.bozuk - 70 * s, y - h); l.quadraticCurveTo(o.bozuk - 40 * s, y - h * .3, o.bozuk - 20 * s, y - 10 * s); l.stroke(); }   // kıvrılmış örgü
    l.restore();
  }
  // sera: ince çerçeve, kırık camlar (bazı bölmeler boş), naylon branda dalgalanır
  function sera(B, x, y, s, t = 0, o = {}) {
    const k = B.k, l = B.l, w = 520 * s, h = 230 * s, r = rng(o.tohum || 31);
    const yol = g => { g.moveTo(x - w / 2, y); g.lineTo(x - w / 2, y - h * .65); g.lineTo(x, y - h); g.lineTo(x + w / 2, y - h * .65); g.lineTo(x + w / 2, y); g.closePath(); };
    k.save(); k.beginPath(); yol(k); k.fillStyle = T(B, .08); k.fill(); k.clip(); k.fillStyle = T(B, .25); for (let i = 0; i < 9; i++) k.fillRect(x - w / 2 + i * w / 8 - 4 * s, y - h, 8 * s, h); k.restore();   // cam: neredeyse kâğıt, arkadaki saksı ve çay kolileri gölge
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 2 * s; l.beginPath(); yol(l); l.stroke(); l.lineWidth = 1.2 * s;
    for (let i = 1; i < 8; i++) { const xx = x - w / 2 + i * w / 8; l.beginPath(); l.moveTo(xx, y); l.lineTo(xx, y - h * (.65 + .35 * (1 - Math.abs(xx - x) / (w / 2)))); l.stroke(); }
    for (let i = 0; i < 8; i++) if (r() < .45) { const xx = x - w / 2 + i * w / 8 + 4 * s; l.beginPath(); l.moveTo(xx, y - h * .3); l.lineTo(xx + w / 16, y - h * .48); l.lineTo(xx + w / 10, y - h * .2); l.stroke(); }   // kırık cam çatlakları
    l.restore();
    k.save(); k.globalAlpha = .7; k.fillStyle = T(B, .12); k.beginPath(); k.moveTo(x - w / 2, y - h * .65); for (let u = 0; u <= 1; u += .05) k.lineTo(x - w / 2 - 30 * s * Math.sin(u * 6 + t * 3) * u, y - h * .65 + u * h * .65); k.lineTo(x - w / 2 + 50 * s, y); k.lineTo(x - w / 2 + 50 * s, y - h * .65); k.closePath(); k.fill(); k.restore();   // rüzgârda açılan branda
  }
  // laboratuvar: tezgâh, raf, kurşun zırhlı dedektör (silindir), Marinelli kabı; ton + çizgi
  function lab(B, o = {}) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .18); k.fillRect(-200, -200, W + 400, H + 400); k.fillStyle = T(B, .5); k.fillRect(-200, 700, W + 400, 30); k.fillStyle = T(B, .35); k.fillRect(-200, 730, W + 400, 500); k.restore();
    l.save(); l.fillStyle = '#000'; l.fillRect(1180, 380, 260, 320); l.fillStyle = '#fff'; l.fillRect(1196, 396, 228, 8); l.fillStyle = '#000'; l.font = FONT.daktilo(30, 700); l.textAlign = 'center'; l.fillText('DEDEKTÖR', 1310, 360); l.restore();   // kurşun zırh (dedektör kalkanı)
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; for (let i = 0; i < 3; i++) { l.beginPath(); l.moveTo(160, 260 + i * 130); l.lineTo(900, 260 + i * 130); l.stroke(); } l.restore();
  }
  // harita: Karadeniz çevresi (basit kıyı çizgisi, dünya koordinatında 1920×1080 çerçeve); kara ton, deniz kâğıt; şehir noktaları
  const KIYI = { // kıyılar (yaklaşık, boylam-enlem); izdüşüm hp: x = (boylam-22)*82, y = (53-enlem)*72 → Çernobil, Edirne ve Rize aynı karede
    karadeniz: [[29.05,41.22],[29.6,41.18],[30.7,41.1],[31.4,41.28],[31.8,41.45],[32.4,41.75],[33.0,41.9],[33.75,41.98],[34.6,42.0],[35.2,42.1],[35.2,41.8],[35.95,41.72],[36.33,41.29],[36.9,41.38],[37.28,41.13],[37.88,40.98],[38.39,40.92],[39.2,41.05],[39.72,41.0],[40.52,41.03],[41.43,41.39],[41.64,41.65],[41.67,42.15],[41.0,43.0],[39.73,43.58],[39.07,44.1],[37.77,44.72],[37.32,44.9],[36.6,45.3],[35.38,45.03],[34.97,44.85],[34.16,44.5],[33.52,44.6],[33.37,45.19],[32.5,45.35],[33.0,45.85],[32.0,46.2],[31.6,46.6],[30.74,46.48],[30.2,45.85],[29.7,45.2],[29.0,44.7],[28.65,44.17],[28.6,43.6],[27.92,43.2],[27.75,42.7],[27.47,42.5],[27.98,41.88],[28.1,41.63],[28.6,41.35]],
    azak: [[36.6,45.4],[35.5,45.3],[35.0,45.8],[35.3,46.4],[36.8,46.7],[38.2,47.1],[39.2,47.2],[38.3,46.6],[37.9,46.0],[37.4,45.4]],
    marmara: [[26.7,40.45],[27.5,40.95],[28.6,40.98],[29.05,41.05],[29.4,40.75],[29.0,40.38],[28.0,40.38],[27.2,40.35],[26.75,40.3]],
    ege: [[21,40.6],[22.9,40.6],[23.7,40.2],[24.4,40.9],[25.5,40.85],[26.0,40.7],[26.2,40.4],[26.4,40.0],[26.1,39.4],[26.6,39.0],[26.8,38.4],[27.2,37.9],[26.5,36.0],[21,36]],
  };
  const hp = ([lon, lat]) => [(lon - 22) * 82, (53 - lat) * 72];
  function harita(B, o = {}) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, o.kara ?? .28); k.fillRect(-400, -400, W + 800, H + 800);
    for (const nm of ['karadeniz', 'marmara', 'ege']) { k.beginPath(); KIYI[nm].forEach((p, i) => { const q = hp(p); i ? k.lineTo(q[0], q[1]) : k.moveTo(q[0], q[1]); }); k.closePath(); k.fillStyle = '#fff'; k.fill(); }
    k.restore();
    k.save(); k.beginPath(); KIYI.karadeniz.forEach((p, i) => { const q = hp(p); i ? k.lineTo(q[0], q[1]) : k.moveTo(q[0], q[1]); }); k.closePath(); k.clip(); k.strokeStyle = T(B, .3); k.lineWidth = 2;
    for (let yy = 260; yy < 900; yy += 34) for (let xx = 500; xx < 1700; xx += 70) { k.beginPath(); k.moveTo(xx, yy); k.quadraticCurveTo(xx + 12, yy - 8, xx + 24, yy); k.quadraticCurveTo(xx + 36, yy + 8, xx + 48, yy); k.stroke(); } k.restore();
    { const q = hp([34.2, 43.4]); l.save(); l.font = FONT.daktilo(30, 700); l.textAlign = 'center'; l.fillStyle = '#000'; l.letterSpacing = '10px'; l.fillText('KARADENİZ', q[0], q[1]); l.restore(); }
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 2.4; for (const nm of ['karadeniz', 'marmara', 'ege']) { l.beginPath(); KIYI[nm].forEach((p, i) => { const q = hp(p); i ? l.lineTo(q[0], q[1]) : l.moveTo(q[0], q[1]); }); l.closePath(); l.stroke(); }
    l.restore();
  }
  const SEHIR = { Cernobil: [30.1, 51.39], Rize: [40.52, 41.03], Edirne: [26.56, 41.68], Ankara: [32.86, 39.93], Sinop: [35.15, 42.03], Istanbul: [28.97, 41.01], Trabzon: [39.72, 41.0] };
  function sehir(B, ad, etiket, o = {}) { const q = hp(SEHIR[ad]); const l = B.l; l.save(); l.fillStyle = '#000'; l.beginPath(); l.arc(q[0], q[1], o.r || 9, 0, TAU); l.fill();
    if (etiket) { l.font = FONT.daktilo(o.px || 34, 700); l.textAlign = o.align || 'left'; l.textBaseline = 'middle'; l.fillText(etiket, q[0] + (o.dx ?? 18), q[1] + (o.dy ?? 0)); } l.restore(); return q; }
  // bulut gölgesi haritada: yumuşak ton lekesi (radyasyon değil hava kütlesi; parıltı yok)
  function bulutGolge(B, x, y, rx, ry, d = .35) { const k = B.k; k.save(); k.translate(x, y); k.scale(rx, ry); const g = k.createRadialGradient(0, 0, 0, 0, 0, 1); g.addColorStop(0, T(B, d)); g.addColorStop(.7, T(B, d * .7)); g.addColorStop(1, 'rgba(255,255,255,0)'); k.fillStyle = g; k.beginPath(); k.arc(0, 0, 1, 0, TAU); k.fill(); k.restore(); }
  // tarih bandı (gazete künyesi gibi): üstte ince çift çizgi arasında "7 AY ÖNCE · MAYIS 1986". Çizgi plakası, sahnenin parçası
  function tarihBandi(B, s, y = 120, p = 1) {
    if (p <= 0) return; const l = B.l; l.save(); baseT(l); l.globalAlpha = clamp(p);
    l.fillStyle = '#000'; l.fillRect(140, y - 30, W - 280, 3); l.fillRect(140, y + 30, W - 280, 3);
    l.font = FONT.daktilo(36, 700); l.textAlign = 'center'; l.textBaseline = 'middle'; l.letterSpacing = '6px';
    { const wd = l.measureText(s).width + 48; for (const g of [B.k, l]) { g.save(); baseT(g); g.globalAlpha = clamp(p); g.fillStyle = '#fff'; g.fillRect(W / 2 - wd / 2, y - 26, wd, 52); g.restore(); } B.c.save(); baseT(B.c); B.c.globalAlpha = clamp(p); B.c.fillStyle = '#000'; B.c.fillRect(W / 2 - wd / 2, y - 26, wd, 52); B.c.restore(); }   // yazının arkası kâğıt: arkadaki çizgiler okunurluğu bozmasın
    l.fillText(s, W / 2, y + 2); l.restore();
  }
  return { daglar, bahce, ev, yaprak, yagmur, bulutlar, kupur, sayi, bardak, mikrofonlar, flas, kamera, cuval, yigin, fabrika, depoIc, cit, sera, lab, harita, sehir, hp, bulutGolge, tarihBandi };
})();
