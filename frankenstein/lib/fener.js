// Sihirli fener motoru (Frankenstein). ORTAK DOSYA: yalnız başkan değiştirir.
// Fikir: 1816'da hayaletler fenerle duvara düşürülürdü (fantazmagorya); Diodati'deki yarışı başlatan kitabın adı da Fantasmagoriana.
// Her plan bir boyalı cam slayttır; karanlık bir perdeye fener ışığıyla düşer.
//   R.g    slayt tuvali (dünya koordinatı, kamera dönüşümüyle). Beyaz = saydam cam, renk = boya (geçen ışığı süzer), siyah = örtücü boya.
//          Boya katmanları çarpılarak birleşir (R.yika); örtücü boya düz basılır (R.kara). Kazıma (R.kazi): siyahın içinden ışık geçiren çizgi.
//   R.isik {x, y, r, sic}  fener ışığı (ekran koordinatı): sıcak lekenin merkezi ve yarıçapı; sic = ışık rengi [r,g,b] (0..1.2)
//   R.kadraj {tip: 'daire'|'oval'|'kare', x, y, w, h, r, yum}  slaytın maskesi (ekran koordinatı): dışı karanlık perde
//   R.parlak  0..1.5 genel ışık şiddeti (bakış kuralı: ışık kimdeyse onu taşır)
//   R.cam(cx, cy, z)  kamerayı (slaytı) kaydırır: ekran merkezine gelen dünya noktası ve yakınlık
//   R.sonra(fn)  ışıklandırılmış karenin üstüne (ekran koordinatı) çizer: ateş parıltısı, mum alevi ışığı
// Işık kuralı (uretim_plani.md §4): fener ışığı bakıştır. Yaratık başkalarının sahnesinde ışığın kenarında kalır;
// kendi hikâyesini anlattığı bölümde (D–F) ışığın merkezi ondadır. Son sahnede ışık kapanır.
'use strict';
const makeCanvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const FENER = (() => {
  const w = DW, h = DH;
  const cG = makeCanvas(w, h), xG = cG.getContext('2d');          // slayt
  const cO = makeCanvas(w, h), xO = cO.getContext('2d');          // ışıklı slayt
  const cM = makeCanvas(w, h), xM = cM.getContext('2d');          // kadraj maskesi
  const bw = Math.round(w / 8), bh = Math.round(h / 8);
  const cB = makeCanvas(bw, bh), xB = cB.getContext('2d');        // parıltı
  const cB2 = makeCanvas(Math.round(bw / 2), Math.round(bh / 2)), xB2 = cB2.getContext('2d');
  const T = {};
  // ---- dokular ----
  function dokuYap() {
    // fırça izi: boya yıkamasının içindeki ince yatay-çapraz izler (döşenebilir, açık gri: çarpılınca boyayı hafif bozar)
    const S = 512;
    const mkT = (fn, seed) => { const c = makeCanvas(S, S), x = c.getContext('2d'), id = x.createImageData(S, S), d = id.data, r = rng(seed);
      for (let y = 0; y < S; y++) for (let X = 0; X < S; X++) { const k = (y * S + X) * 4, v = fn(X, y, r); d[k] = v[0]; d[k + 1] = v[1]; d[k + 2] = v[2]; d[k + 3] = v[3] ?? 255; }
      x.putImageData(id, 0, 0); return c; };
    const tn = (u, v, p, s) => { // döşenebilir değer gürültüsü
      const xi = Math.floor(u), yi = Math.floor(v), xf = u - xi, yf = v - yi, a = (i, j) => hash2(((i % p) + p) % p, ((j % p) + p) % p, s);
      const uu = xf * xf * (3 - 2 * xf), vv = yf * yf * (3 - 2 * yf);
      return lerp(lerp(a(xi, yi), a(xi + 1, yi), uu), lerp(a(xi, yi + 1), a(xi + 1, yi + 1), uu), vv); };
    T.firca = mkT((X, y) => { const u = X / S, v = y / S;
      const izler = tn(u * 6, v * 70, 6, 3) * .55 + tn(u * 3 + v * 2, v * 22, 3, 5) * .45;   // fırça çekişi: yatay uzun izler
      const leke = tn(u * 4, v * 4, 4, 9);
      const k = 255 - (izler * 34 + leke * 22); return [k, k, k]; }, 1);
    // cam tozu ve kıl: koyu noktalar ve ince eğri çizgiler (saydam zemin)
    const ct = makeCanvas(S * 2, S * 2), cx = ct.getContext('2d'), r = rng(77);
    for (let i = 0; i < 260; i++) { const x = r() * S * 2, y = r() * S * 2, rr = .6 + r() * r() * 2.6; cx.fillStyle = `rgba(20,12,6,${.25 + r() * .5})`; cx.beginPath(); cx.arc(x, y, rr, 0, TAU); cx.fill(); }
    for (let i = 0; i < 7; i++) { let x = r() * S * 2, y = r() * S * 2, a = r() * TAU; cx.strokeStyle = `rgba(20,12,6,${.18 + r() * .25})`; cx.lineWidth = .7 + r() * .6; cx.beginPath(); cx.moveTo(x, y);
      for (let k = 0; k < 14; k++) { a += (r() - .5) * .9; x += Math.cos(a) * 9; y += Math.sin(a) * 9; cx.lineTo(x, y); } cx.stroke(); }
    // ince çizikler (açık): camın üstündeki eski çizikler
    for (let i = 0; i < 18; i++) { const x = r() * S * 2, y = r() * S * 2, a = r() * PI, l = 30 + r() * 160; cx.strokeStyle = `rgba(255,245,225,${.05 + r() * .08})`; cx.lineWidth = .8; cx.beginPath(); cx.moveTo(x, y); cx.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); cx.stroke(); }
    T.toz = ct;
    // perde dokusu (ekrana sabit): ince bez örgüsü + geniş lekeler
    T.perde = mkT((X, y) => { const u = X / S, v = y / S, orgu = .5 + .25 * Math.sin(X * 1.9) * Math.sin(y * 1.9), leke = tn(u * 3, v * 3, 3, 21);
      const k = 255 - (orgu * 10 + leke * 26); return [k, k * .99, k * .97]; }, 2);
  }
  let pFirca, pToz, pPerde;
  // ---- durum ----
  const R = { g: xG, T, isik: null, kadraj: null, parlak: 1, _cam: { x: 0, y: 0, s: 1 }, _sonra: [], iris: 1, titreme: 1 };
  R.begin = (o = {}) => {
    xG.setTransform(1, 0, 0, 1, 0, 0); xG.globalAlpha = 1; xG.globalCompositeOperation = 'source-over'; xG.filter = 'none';
    xG.fillStyle = o.cam || '#F3EEE2'; xG.fillRect(0, 0, w, h);                  // saydam cam (hafif sarımsı)
    R.isik = { x: W / 2, y: H * .47, r: 760, sic: [1.0, .9, .72], ...(o.isik || {}) };
    R.kadraj = { tip: 'kare', x: W / 2, y: H / 2, w: 1800, h: 1010, r: 90, yum: 26, ...(o.kadraj || {}) };
    R.parlak = o.parlak ?? 1; R._sonra = []; R.toz = o.toz ?? 1; R.perdeA = o.perde ?? 1; R.iris = 1;
    R.cam(W / 2, H / 2, 1);
  };
  R.cam = (cx, cy, z = 1) => { R._cam = { x: cx - W / 2 / z, y: cy - H / 2 / z, s: z }; R.T_ = [RS * z, 0, 0, RS * z, -R._cam.x * RS * z, -R._cam.y * RS * z]; xG.setTransform(...R.T_); };
  R.reset = () => xG.setTransform(...R.T_);
  R.ekran = fn => { xG.save(); xG.setTransform(RS, 0, 0, RS, 0, 0); fn(xG); xG.restore(); };   // slayta ekran koordinatıyla çiz
  R.sonra = fn => R._sonra.push(fn);
  // ---- boya yardımcıları ----
  // yika(yol, renk, o): saydam boya (çarpma). o.firca: fırça izi gücü; o.kay: boyanın çizgiden kayması (elde boyamanın kusuru)
  R.yika = (yol, renk, o = {}) => {
    const g = xG; g.save(); const k = o.kay ?? 3;
    if (k) g.translate(k * .8, -k * .5);
    g.globalCompositeOperation = 'multiply'; g.globalAlpha = o.a ?? 1;
    g.beginPath(); yol(g); g.fillStyle = renk; g.fill(o.kural || 'nonzero');
    if ((o.firca ?? 1) > 0) { g.clip(o.kural || 'nonzero'); g.globalAlpha = (o.a ?? 1) * (o.firca ?? 1); g.fillStyle = pFirca; g.save(); g.rotate(o.fa || 0); g.fillRect(-6000, -6000, 12000, 12000); g.restore(); }
    g.restore();
  };
  // gok(y0, y1, renkler): dikey boya geçişi (gökyüzü, deniz); renkler [[0,'#..'],[1,'#..']]
  R.gok = (x0, y0, x1, y1, renkler, o = {}) => { const gr = xG.createLinearGradient(0, y0, 0, y1); for (const [p, c] of renkler) gr.addColorStop(p, c); R.yika(g => g.rect(x0, y0, x1 - x0, y1 - y0), gr, { kay: 0, ...o }); };
  R.halka = (x, y, r0, r1, renkler, o = {}) => { const gr = xG.createRadialGradient(x, y, r0, x, y, r1); for (const [p, c] of renkler) gr.addColorStop(p, c); R.yika(g => g.rect(x - r1, y - r1, r1 * 2, r1 * 2), gr, { kay: 0, firca: 0, ...o }); };
  // kara(yol, o): örtücü siyah boya (siluet). o.renk: koyu boya rengi (çok koyu kahve), o.a
  R.KARA = '#0E0906';
  R.kara = (yol, o = {}) => { const g = xG; g.save(); g.globalCompositeOperation = 'source-over'; g.globalAlpha = o.a ?? 1; g.beginPath(); yol(g); g.fillStyle = o.renk || R.KARA; g.fill(o.kural || 'nonzero'); g.restore(); };
  // cizgi(noktalar, kalınlık, o): siyah fırça çizgisi (uçları yuvarlak; o.kapali)
  R.cizgi = (pts, lw, o = {}) => { const g = xG; g.save(); g.globalCompositeOperation = o.mod || 'source-over'; g.globalAlpha = o.a ?? 1; g.strokeStyle = o.renk || R.KARA; g.lineWidth = lw; g.lineCap = 'round'; g.lineJoin = 'round';
    g.beginPath(); if (o.egri) spline(g, pts, !!o.kapali); else poly(g, pts, !!o.kapali); g.stroke(); g.restore(); };
  // kazi(yol çizgisi, kalınlık, renk): siyahın içinden kazınmış ışık çizgisi (göz, kenar ışığı); renk açık boya
  R.kazi = (pts, lw, renk = '#F2D58A', o = {}) => R.cizgi(pts, lw, { ...o, renk, mod: 'source-over' });
  R.nokta = (x, y, r, renk) => { const g = xG; g.save(); g.globalCompositeOperation = 'source-over'; g.fillStyle = renk; g.beginPath(); g.arc(x, y, r, 0, TAU); g.fill(); g.restore(); };
  R.isikli = (yol, renk = '#FFF6DC') => { const g = xG; g.save(); g.globalCompositeOperation = 'source-over'; g.beginPath(); yol(g); g.fillStyle = renk; g.fill(); g.restore(); };   // saydam cama dönen alan (ay, alev)
  // ---- birleştirme ----
  R.init = () => { dokuYap(); pFirca = xG.createPattern(T.firca, 'repeat'); pToz = xO.createPattern(T.toz, 'repeat'); pPerde = xO.createPattern(T.perde, 'repeat'); };
  function maske() {
    const k = R.kadraj, iris = R.iris; xM.setTransform(1, 0, 0, 1, 0, 0); xM.clearRect(0, 0, w, h);
    xM.setTransform(RS, 0, 0, RS, 0, 0); xM.fillStyle = '#fff';
    xM.filter = `blur(${(k.yum || 20) * RS * .6}px)`;
    xM.beginPath();
    if (k.tip === 'daire') xM.arc(k.x, k.y, Math.max(0, k.r * iris), 0, TAU);
    else if (k.tip === 'oval') xM.ellipse(k.x, k.y, Math.max(0, k.w / 2 * iris), Math.max(0, k.h / 2 * iris), 0, 0, TAU);
    else { const ww = k.w * (iris < 1 ? lerp(.0, 1, iris) : 1), hh = k.h * (iris < 1 ? lerp(.0, 1, iris) : 1), rr = Math.min(k.r, ww / 2, hh / 2); if (ww > 1 && hh > 1) xM.roundRect(k.x - ww / 2, k.y - hh / 2, ww, hh, rr); }
    xM.fill(); xM.filter = 'none';
  }
  R.compose = (ctx, t = 0) => {
    // tozun ve çiziklerin slayta yapışık katmanı (kamera ile kayar)
    if (R.toz > 0) { xG.save(); xG.setTransform(...R.T_); xG.globalAlpha = R.toz; xG.globalCompositeOperation = 'source-over'; const pz = xG.createPattern(T.toz, 'repeat'); xG.fillStyle = pz; xG.fillRect(R._cam.x - 50, R._cam.y - 50, W / R._cam.s + 100, H / R._cam.s + 100); xG.restore(); }
    // ışık: sıcak leke + geniş taban; titreme (iki ölçekte gürültü) iki karede bir değişir
    const L = R.isik, fi = Math.floor(t * 15), tit = 1 + (.022 * (hash(fi * 1.7) - .5) + .02 * noise1(t * 1.3, 4)) * R.titreme;
    const P = R.parlak * tit, [sr, sg, sb] = L.sic;
    xO.setTransform(1, 0, 0, 1, 0, 0); xO.globalAlpha = 1; xO.globalCompositeOperation = 'source-over';
    const gr = xO.createRadialGradient(L.x * RS, L.y * RS, 0, L.x * RS, L.y * RS, L.r * RS * 1.55);
    const c = (k) => `rgb(${Math.min(255, sr * k * 255) | 0},${Math.min(255, sg * k * 255) | 0},${Math.min(255, sb * k * 255) | 0})`;
    gr.addColorStop(0, c(1.15 * P)); gr.addColorStop(.4, c(1.05 * P)); gr.addColorStop(.75, c(.85 * P)); gr.addColorStop(1, c(.55 * P));
    xO.fillStyle = gr; xO.fillRect(0, 0, w, h);
    // perde dokusu (ekrana sabit)
    if (R.perdeA > 0) { xO.globalCompositeOperation = 'multiply'; xO.globalAlpha = R.perdeA; xO.fillStyle = pPerde; xO.fillRect(0, 0, w, h); xO.globalAlpha = 1; }
    // slayt × ışık
    xO.globalCompositeOperation = 'multiply'; xO.drawImage(cG, 0, 0);
    // kadraj maskesi
    maske(); xO.globalCompositeOperation = 'destination-in'; xO.drawImage(cM, 0, 0); xO.globalCompositeOperation = 'source-over';
    // perde: karanlık + kadrajın çevresine taşan hafif ışık
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    ctx.fillStyle = '#080503'; ctx.fillRect(0, 0, w, h);
    const sp = ctx.createRadialGradient(L.x * RS, L.y * RS, 0, L.x * RS, L.y * RS, 1300 * RS);
    sp.addColorStop(0, `rgba(70,46,24,${.55 * Math.min(1, P) * R.iris})`); sp.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = sp; ctx.fillRect(0, 0, w, h);
    ctx.drawImage(cO, 0, 0);
    // parıltı: parlak yerlerin çevresi (ay, alev, mum) — küçük tuvalde bulanık, ekranla
    xB.setTransform(1, 0, 0, 1, 0, 0); xB.globalCompositeOperation = 'source-over'; xB.clearRect(0, 0, bw, bh); xB.filter = 'brightness(0.9) contrast(2.2)'; xB.drawImage(cO, 0, 0, bw, bh); xB.filter = 'none';
    xB2.clearRect(0, 0, cB2.width, cB2.height); xB2.drawImage(cB, 0, 0, cB2.width, cB2.height);
    ctx.globalCompositeOperation = 'screen'; ctx.globalAlpha = .22; ctx.imageSmoothingQuality = 'high'; ctx.drawImage(cB2, 0, 0, w, h); ctx.globalAlpha = .16; ctx.drawImage(cB, 0, 0, w, h);
    ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
    ctx.restore();
    // sonra katmanı (ekran koordinatı)
    for (const fn of R._sonra) { ctx.save(); baseT(ctx); fn(ctx); ctx.restore(); }
  };
  // dünya → ekran
  R.ekr = (x, y) => [(x - R._cam.x) * R._cam.s, (y - R._cam.y) * R._cam.s];
  return R;
})();
