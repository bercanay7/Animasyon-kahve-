// Ortak dekor ilkelleri (ağaç baskı). Hepsi dünya koordinatında k.m (maske) ve k.c (kırmızı levha) üstüne çizer.
// Işık oyulur: ak = bıçağın oyduğu yer. Koyu kütleler oyulmamış blok. Tek renk yalnız elmada.
'use strict';
const O = {
  // yerden bakışla oda duvarı + zemin. o: {zemY (zemin çizgisi), isik:[x,y] (ışık kaynağı, ör. kapı aralığı), key}
  duvar(k, key, o = {}) {
    const zy = o.zemY ?? 700, [lx, ly] = o.isik || [1260, 420];
    // duvar kâğıdı: dikey ince kesikler, ışığa yakın genişler (ışık oyulur), uzakta biter
    KS.tara(k.m, key + ':duvar', [[[58, 40], [1862, 40], [1862, zy], [58, zy]]], { aci: Math.PI / 2, sp: 15, wmax: 5.5, seg: [40, 160], gap: [6, 22], seed: 21,
      ton: (x, y) => clamp(1.15 - Math.hypot((x - lx) * .8, (y - ly) * 1.3) / (o.yar ?? 620)) * .85 });
    // süpürgelik: ince ak kesik çizgi
    KS.kenar(k.m, key + ':supurge', [[58, zy - 34], [1862, zy - 34]], { w: 2.4, seg: [80, 260], gap: [4, 14], seed: 23 });
  },
  // zemin tahtaları: kaçış noktasına koşan derzler; yalnız ışıkta görünür (karanlıkta blok)
  zemin(k, key, o = {}) {
    const zy = o.zemY ?? 700, vx = o.vx ?? 960, [lx, ly] = o.isik || [1260, 760];
    KS.tara(k.m, key + ':zemin', [[[58, zy], [1862, zy], [1862, 900], [58, 900]]], {
      dir: (x, y) => Math.atan2(y - (zy - 260), x - vx), sp: 13, wmax: 6, seg: [50, 200], gap: [4, 16], seed: 27,
      ton: (x, y) => clamp(1.05 - Math.hypot((x - lx) * .7, (y - ly) * 1.6) / (o.yar ?? 520)) * .8 });
  },
  // aralık kapı (yerden): kasa, kanat, aralık; aralıktan zemine ışık şeridi. ac: aralık genişliği (px)
  kapi(k, key, o = {}) {
    const x0 = o.x0 ?? 1060, x1 = o.x1 ?? 1460, y0 = o.y0 ?? 110, zy = o.zemY ?? 700, ac = o.ac ?? 46, gx = o.gx ?? 1250;
    const g = k.m;
    // kasa: ince ak bıçak çerçevesi
    KS.kenar(g, key + ':kasa', [[x0, zy], [x0, y0], [x1, y0], [x1, zy]], { w: 4.5, seg: [90, 300], gap: [3, 9], seed: 31 });
    KS.kenar(g, key + ':kasa2', [[x0 - 22, zy], [x0 - 22, y0 - 22], [x1 + 22, y0 - 22], [x1 + 22, zy]], { w: 2.2, seg: [60, 220], gap: [4, 14], seed: 33 });
    // aralık: ak dikey yarık, içinde ışığın hareleri (yan odadaki lamba)
    const ar = KS.rect(gx, y0 + 6, ac, zy - y0 - 6); KS.ak(g, ar);
    if (o.icerde) o.icerde(k, gx, y0, ac, zy);
    // kanat kenarı: aralığın solunda kalın kara kenar + tek ak çizgi (kapı kalınlığı)
    g.fillStyle = '#000'; g.fillRect(gx - 14, y0 + 6, 14, zy - y0 - 6);
    KS.kenar(g, key + ':kanat', [[gx - 20, y0 + 10], [gx - 20, zy - 4]], { w: 2, seg: [120, 320], gap: [3, 8], seed: 35 });
    // kapı kolu: küçük ak oval
    const kol = new Path2D(); kol.ellipse(gx - 48, (y0 + zy) / 2 + 40, 9, 6, 0, 0, TAU); KS.ak(g, kol);
    // zemine düşen ışık şeridi: aralıktan bize doğru açılan yamuk; içinde tahta derzleri kara kalır
    if (o.serit !== false) O.serit(k, key, gx, ac, zy, o);
  },
  serit(k, key, gx, ac, zy, o = {}) {
    const g = k.m, aci = o.serAci ?? 1, xb = o.serX ?? (gx + ac / 2 - 70), wb = (o.serW ?? 380) * (ac / 46) ** .7;
    const pts = [[gx, zy], [gx + ac, zy], [xb + wb / 2 + 40, 905], [xb - wb / 2, 905]];
    const pa = KS.poly(pts); KS.ak(g, pa);
    g.save(); g.clip(pa); g.strokeStyle = '#000';
    // derzler: kaçış noktasından
    const vx = o.vx ?? 960;
    for (let i = -10; i <= 10; i++) { const xb2 = gx + ac / 2 + i * 95; g.lineWidth = 3.2; g.beginPath(); g.moveTo(vx + (xb2 - vx) * .0 + (xb2 - vx) * .25, zy - 260 + 260 * .25 * 0); g.lineTo(xb2 + (xb2 - (gx + ac / 2)) * 2.4, 905 + 300); g.stroke(); }
    // ışığın sönüşü: kesik kesik kara çizgiler uca doğru sıklaşır (blok rengi geri gelir)
    KS.tara(g, key + ':seritTon', [pts], { aci: 0, sp: 9, wmax: 6, seg: [30, 140], gap: [6, 18], seed: 41, renk: '#000', ton: (x, y) => clamp((y - zy) / 240) * .5 * clamp(Math.abs(x - (gx + ac / 2)) / 260 + .3) });
    g.restore();
  },
  // elma: oyulmuş ak disk (biçimi saran yay kesikleri kara kalır) + kırmızı levha; gölgesi kara
  elma(k, x, y, r, o = {}) {
    const g = k.m, c = k.c, rot = o.rot || 0;
    const body = new Path2D(); body.moveTo(x, y - r * .78);
    body.bezierCurveTo(x + r * .55, y - r * 1.12, x + r * 1.1, y - r * .6, x + r * 1.0, y + r * .05);
    body.bezierCurveTo(x + r * .95, y + r * .7, x + r * .45, y + r * 1.0, x, y + r * .88);
    body.bezierCurveTo(x - r * .45, y + r * 1.0, x - r * .95, y + r * .7, x - r * 1.0, y + r * .05);
    body.bezierCurveTo(x - r * 1.1, y - r * .6, x - r * .55, y - r * 1.12, x, y - r * .78); body.closePath();
    g.save(); g.translate(x, y); g.rotate(rot); g.translate(-x, -y);
    if (o.hale !== false) { g.strokeStyle = '#fff'; g.lineWidth = r * .16; g.stroke(body); }
    KS.ak(g, body);
    // biçimi saran kara yaylar (gölge tarafında sık)
    g.save(); g.clip(body); g.strokeStyle = '#000';
    for (let i = 0; i < 9; i++) { const a = .5 + i * .16; g.lineWidth = r * (.035 + .05 * (i / 8)); g.beginPath(); g.ellipse(x + r * .55, y + r * .3, r * (1.55 - i * .1), r * (1.45 - i * .1), 0, Math.PI * .65, Math.PI * 1.25); g.stroke(); }
    g.lineWidth = r * .07; g.beginPath(); g.ellipse(x - r * .25, y - r * .25, r * .22, r * .3, -.6, 0, TAU); g.stroke();
    g.restore();
    // sap
    g.strokeStyle = '#fff'; g.lineWidth = r * .09; g.lineCap = 'round'; g.beginPath(); g.moveTo(x, y - r * .7); g.quadraticCurveTo(x + r * .08, y - r * 1.05, x + r * .25, y - r * 1.25); g.stroke();
    g.restore();
    // kırmızı levha (oyulmuş akta görünür)
    c.save(); c.translate(x, y); c.rotate(rot); c.translate(-x, -y); c.fillStyle = `rgba(0,0,0,${o.kirmizi ?? 1})`; c.fill(body); c.restore();
  },
  // tavandan sarkan lamba + oyulmuş ışınlar
  lamba(k, key, x, y, o = {}) {
    const g = k.m; g.strokeStyle = '#fff'; g.lineWidth = 2.5; g.beginPath(); g.moveTo(x, 40); g.lineTo(x, y - 40); g.stroke();
    const sh = KS.poly([[x - 70, y], [x + 70, y], [x + 30, y - 46], [x - 30, y - 46]]); KS.ak(g, sh);
    g.save(); g.clip(sh); g.strokeStyle = '#000'; g.lineWidth = 3; for (let i = -6; i <= 6; i++) { g.beginPath(); g.moveTo(x + i * 12, y - 46); g.lineTo(x + i * 20, y); g.stroke(); } g.restore();
    KS.isin(g, key + ':lamba', x, y + 6, { n: o.n ?? 30, r0: 40, r1: o.r1 || [260, 520], w: o.w ?? 9, a0: .15, a1: Math.PI - .15, jit: .7, seed: 8 });
  },
  // pencere: kasa + camlar; dışarısı ak gök (yağmur kesikleri kara) ya da gece (blok, yıldız benekleri)
  pencere(k, key, x, y, w, h, o = {}) {
    const g = k.m, cam = KS.rect(x, y, w, h);
    if (o.gece) { KS.benek(g, key + ':yildiz', Array.from({ length: 14 }, (_, i) => [x + 20 + hash(i * 3.1) * (w - 40), y + 20 + hash(i * 7.7) * (h * .5), 2.5 + hash(i) * 2])); }
    else {
      KS.ak(g, cam);
      if (o.gok) o.gok(k, x, y, w, h);
      if (o.yagmur) { g.save(); g.clip(cam); g.strokeStyle = '#000'; const r = rng(5); for (let i = 0; i < 70; i++) { const px = x + r() * w, py = y + ((r() * h + k.lt * 260 * (.8 + r() * .4)) % h), L = 20 + r() * 30; g.lineWidth = 2 + r() * 1.5; g.beginPath(); g.moveTo(px, py); g.lineTo(px - L * .25, py + L); g.stroke(); } g.restore(); }
    }
    // kasa ve kayıtlar
    g.fillStyle = '#000'; g.fillRect(x + w / 2 - 7, y, 14, h); g.fillRect(x, y + h * .42 - 7, w, 14);
    KS.kenar(g, key + ':kasa', [[x - 14, y + h + 14], [x - 14, y - 14], [x + w + 14, y - 14], [x + w + 14, y + h + 14], [x - 14, y + h + 14]], { w: 3, seg: [80, 260], gap: [3, 9], seed: 51 });
    // pervaz: ak çizgi
    g.fillStyle = '#fff'; g.fillRect(x - 30, y + h + 16, w + 60, 6);
  },
  // masa (önden): tabla + iki bacak; üstüne ışık
  masa(k, key, x, y, w, o = {}) {
    const g = k.m, th = 18;
    const tab = KS.rect(x - w / 2, y, w, th); KS.ak(g, tab);
    g.save(); g.clip(tab); g.strokeStyle = '#000'; g.lineWidth = 2.4; for (let i = 0; i < w; i += 14) { g.beginPath(); g.moveTo(x - w / 2 + i, y + 4); g.lineTo(x - w / 2 + i + 50, y + th); g.stroke(); } g.restore();
    g.fillStyle = '#000'; g.fillRect(x - w / 2 + 30, y + th, 22, o.boy ?? 240); g.fillRect(x + w / 2 - 52, y + th, 22, o.boy ?? 240);
    KS.kenar(g, key + ':masaB1', [[x - w / 2 + 30, y + th + 4], [x - w / 2 + 30, y + th + (o.boy ?? 240)]], { w: 2, seed: 61 });
    KS.kenar(g, key + ':masaB2', [[x + w / 2 - 30, y + th + 4], [x + w / 2 - 30, y + th + (o.boy ?? 240)]], { w: 2, seed: 62 });
  },
  // sikke: oyulmuş ak disk, ortası ince kara halka
  sikke(g, x, y, r, sq = .35) { const p = new Path2D(); p.ellipse(x, y, r, r * sq, 0, 0, TAU); KS.ak(g, p); g.strokeStyle = '#000'; g.lineWidth = Math.max(1.5, r * .1); g.beginPath(); g.ellipse(x, y, r * .7, r * .7 * sq, 0, 0, TAU); g.stroke(); g.fillStyle = '#000'; g.fillRect(x - r, y + r * sq * .2, r * 2, Math.max(2, r * .12)); },
  // figür basımı (hale + ışıklı kenar)
  fig(k, o, s = {}) { const F = IN.insan(o), all = new Path2D(F.p); all.addPath(F.kp);
    const so = { hale: s.hale ?? Math.max(4, o.h * .011), isik: s.isik || [-1, -.4], rim: s.rim ?? Math.max(3, o.h * .009), kesSp: s.kesSp ?? Math.max(10, o.h * .024), kesW: s.kesW ?? Math.max(2, o.h * .004), kes: s.kes };
    KS.siluet(k.m, all, so);
    // kol konturu: gövdeden ince bir bıçak çizgisiyle ayrılır (kara kütle içinde okunur)
    k.m.save(); k.m.strokeStyle = '#fff'; k.m.lineWidth = Math.max(1.6, o.h * .0035); k.m.stroke(F.kp); k.m.fillStyle = '#000'; k.m.fill(F.kp); k.m.restore(); if (F.dug.length) for (const d of F.dug) { const p = new Path2D(); p.arc(d[0], d[1], F.u * .1, 0, TAU); KS.ak(k.m, p); } return F; },
};
