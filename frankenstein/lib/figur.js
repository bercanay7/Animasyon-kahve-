// Siluet figürler (Frankenstein). ORTAK DOSYA: yalnız başkan değiştirir.
// Boyalı cam slaytta figürler örtücü koyu boyadır (kanal kuralı: ana figür koyu siluet). Kollar ayrı yolla, gövde kutu değil.
// Yerel uzay: ayaklar y = 0, baş tepesi y ≈ -100 (boy birimi), figür +x'e bakar. FIG.kisi(R, x, zeminY, boy, o)
//   o.tip: 'yaratik' | 'victor' | 'mary' | 'byron' | 'percy' | 'ihtiyar' | 'kiz' | 'genc' | 'cocuk' | 'kaptan' | 'koylu'
//   o.f: 1 sağa, -1 sola · o.govde: öne eğilme (radyan) · o.bas: baş eğimi · o.kolO / o.kolA: [omuz açısı, dirsek bükümü] (öndeki / arkadaki kol;
//        açı 0 = aşağı sarkık, + = öne kalkar) · o.bacak: 'dur' | 'otur' | 'diz' | 'cok' (çömelik) | HAREKET poz nesnesi
//   o.sac: rüzgârda saç savrulması (-1..1) · o.pel: pelerin salınımı · o.goz: yaratığın gözü (0 kapalı … 1 açık) · o.el: {on: fn(R, p, s), arka: fn}
// Hassasiyet (CLAUDE.md): düz kalkık kol yok (dirsek hep bükük), göğüste beyaz dikdörtgen yok, simetrik açık kol yok, başın yanında açık leke yok.
'use strict';
const FIG = (() => {
  const K = () => FENER.KARA;
  // iki kemik: omuz noktası, açılar → dirsek ve el (yerel, +x ön)
  const kol = (o, a1, a2, l1, l2) => { const d = [o[0] + Math.sin(a1) * l1, o[1] + Math.cos(a1) * l1]; const b = a1 + a2; return [d, [d[0] + Math.sin(b) * l2, d[1] + Math.cos(b) * l2]]; };
  const P = (g, pts, k = 1) => { g.beginPath(); spline(g, pts, true, k); };
  // tipler: boy oranı, giysi, saç
  const TIP = {
    yaratik: { olc: 1.16, giysi: 'pelerin', sac: 'uzun', ince: .82, omuz: 1.12 },
    victor: { olc: 1, giysi: 'ceket', sac: 'kisa', ince: 1 },
    byron: { olc: .98, giysi: 'ceket', sac: 'kivir', ince: 1.05, yaka: 1 },
    percy: { olc: 1.03, giysi: 'ceket', sac: 'daginik', ince: .92, yaka: 1 },
    kaptan: { olc: 1, giysi: 'palto', sac: 'kisa', ince: 1.05 },
    genc: { olc: 1, giysi: 'ceket', sac: 'kisa', ince: 1 },
    koylu: { olc: 1, giysi: 'yelek', sac: 'kisa', ince: 1.08 },
    ihtiyar: { olc: .95, giysi: 'cubbe', sac: 'ak', ince: 1, sakal: 1 },
    mary: { olc: .93, giysi: 'elbise', sac: 'topuz', ince: .9, kadin: 1 },
    kiz: { olc: .9, giysi: 'elbise', sac: 'ortu', ince: .9, kadin: 1 },
    cocuk: { olc: .6, giysi: 'ceket', sac: 'kisa', ince: 1.1, cocuk: 1 },
  };
  function kisi(R, x, y, boy, o = {}) {
    const tp = TIP[o.tip || 'victor'], g = R.g, f = o.f || 1, s = boy * tp.olc / 100, renk = o.renk || K();
    const govde = o.govde || 0, ince = tp.ince;
    g.save(); g.translate(x, y); g.scale(f * s, s);
    // ---- bacaklar / kalça ----
    let kalca = [0, -50], ayak = [[3, 0], [-3, 0]], diz = [[3, -25], [-2, -25]];
    const b = o.bacak || 'dur';
    if (typeof b === 'object') {   // HAREKET pozu (yerel 95 birimlik uzay → 100)
      const m = p => [(p[0] - 40) * 1.05, (p[1] - 120) * 1.05];
      kalca = m(b.kalca); ayak = [m(b.ayaklar[b.on].bilek), m(b.ayaklar[1 - b.on].bilek)]; diz = [m(b.ayaklar[b.on].diz), m(b.ayaklar[1 - b.on].diz)];
    } else if (b === 'otur') { kalca = [-2, -27]; diz = [[20, -29], [18, -28]]; ayak = [[22, 0], [17, 0]]; }
    else if (b === 'diz') { kalca = [-2, -26]; diz = [[16, -22], [-6, -1]]; ayak = [[18, 0], [-22, -1]]; }
    else if (b === 'cok') { kalca = [-6, -20]; diz = [[12, -30], [10, -26]]; ayak = [[10, 0], [4, 0]]; }
    else if (b === 'yat') { /* yatan: çağıran döndürür */ }
    const omuzY = kalca[1] - 30, gx = kalca[0];
    // gövde dönüşümü: kalça çevresinde eğilme
    const rot = (p) => { const dx = p[0] - kalca[0], dy = p[1] - kalca[1], c = Math.cos(govde), sn = Math.sin(govde); return [kalca[0] + dx * c + dy * sn, kalca[1] - dx * sn + dy * c]; };
    const omuz = rot([gx + 1, omuzY]), boyun = rot([gx + 2.5, omuzY - 4]);
    const basM = rot([gx + 3.5, omuzY - 11]);
    // ---- arka kol (önce) ----
    const kA = o.kolA || [-.15, .25], kO = o.kolO || [.12, .3];
    const L1 = 16.5, L2 = 15.5;
    const ciz = (pts, lw) => { g.save(); g.strokeStyle = renk; g.lineCap = 'round'; g.lineJoin = 'round'; g.lineWidth = lw; g.beginPath(); poly(g, pts, false); g.stroke(); g.restore(); };
    const el = (p, a, buyuk = 1) => { g.save(); g.translate(p[0], p[1]); g.rotate(-a); g.fillStyle = renk; g.beginPath(); g.ellipse(0, 2.2 * buyuk, 1.9 * buyuk, 3 * buyuk, 0, 0, TAU); g.fill(); g.beginPath(); g.ellipse(1.6 * buyuk, 1.1 * buyuk, .8 * buyuk, 1.8 * buyuk, -.5, 0, TAU); g.fill(); g.restore(); };
    const kolCiz = (kk, arka) => {
      const sp = [omuz[0] + (arka ? -1.2 : 1.2), omuz[1] + 2.5];
      const [d, e] = kol(sp, kk[0] - govde, kk[1], L1, L2);
      const kal = tp.giysi === 'pelerin' ? 3.6 : 4.6;
      ciz([sp, d], kal * 1.15 * ince); ciz([d, e], kal * .95 * ince); el(e, kk[0] + kk[1] - govde, tp.giysi === 'pelerin' ? 1.25 : 1);
      // yaratık: kemikli el bileği (elinden ince parmaklar)
      if (tp.giysi === 'pelerin') { const a = kk[0] + kk[1] - govde; for (let i = -1; i <= 1; i++) ciz([[e[0] + Math.sin(a) * 2, e[1] + Math.cos(a) * 2], [e[0] + Math.sin(a + i * .18) * 6.2, e[1] + Math.cos(a + i * .18) * 6.2]], 1.1); }
      return { d, e, a: kk[0] + kk[1] - govde };
    };
    const arkaKol = kolCiz(kA, true);
    if (o.el && o.el.arka) { g.save(); o.el.arka(R, arkaKol); g.restore(); }
    // ---- bacaklar ----
    const bacak = (k, h, a, lw) => { ciz([k, h, a], lw); g.save(); g.fillStyle = renk; g.beginPath(); g.ellipse(a[0] + 3, a[1] - 1.2, 4.4, 1.8, 0, 0, TAU); g.fill(); g.restore(); };
    const etekli = tp.kadin || tp.giysi === 'cubbe';
    if (!etekli) { bacak([kalca[0] - 1, kalca[1]], diz[1], ayak[1], 6.2 * ince); bacak([kalca[0] + 1, kalca[1]], diz[0], ayak[0], 6.6 * ince); }
    // ---- gövde ----
    g.fillStyle = renk;
    if (tp.kadin) {
      // yüksek belli elbise: göğüs altından yere dökülen etek; adımla açılır
      const ac = typeof b === 'object' ? (ayak[0][0] - ayak[1][0]) * .5 : (b === 'otur' ? 0 : 0);
      if (b === 'otur') P(g, [rot([gx - 7, omuzY + 1]), rot([gx + 6, omuzY + 2]), rot([gx + 7, omuzY + 9]), [diz[0][0] + 3, diz[0][1] - 2], [ayak[0][0] + 4, -1], [ayak[0][0] - 6, 0], [diz[0][0] - 6, diz[0][1] + 7], [kalca[0] - 9, kalca[1] + 4], rot([gx - 8, omuzY + 18])], .9);
      else P(g, [rot([gx - 6, omuzY]), rot([gx + 5.5, omuzY + 1.5]), rot([gx + 7, omuzY + 9]), rot([gx + 6.5, omuzY + 12]), [gx + 13 + ac, -1], [gx + 2, 0.5], [gx - 13 + ac * .4, -1], rot([gx - 7, omuzY + 14])], .85);
      g.fill();
      if (b !== 'otur') for (const a of ayak) { g.beginPath(); g.ellipse(a[0] + 3, a[1] - .8, 3.6, 1.4, 0, 0, TAU); g.fill(); }
    } else if (tp.giysi === 'cubbe') {
      const oturur = b === 'otur';
      if (oturur) P(g, [rot([gx - 7, omuzY]), rot([gx + 6, omuzY + 1]), rot([gx + 7, omuzY + 12]), [diz[0][0] + 3, diz[0][1] - 1], [ayak[0][0] + 3, -1], [ayak[0][0] - 7, 0], [diz[0][0] - 5, diz[0][1] + 8], [kalca[0] - 9, kalca[1] + 3]], .9);
      else P(g, [rot([gx - 7, omuzY]), rot([gx + 6, omuzY + 1]), rot([gx + 7.5, omuzY + 14]), [gx + 11, -1], [gx - 11, -1], rot([gx - 8, omuzY + 16])], .9);
      g.fill();
    } else {
      const om = tp.omuz || 1;
      P(g, [rot([gx - 6.5 * om, omuzY - 1]), rot([gx + 2, omuzY - 3]), rot([gx + 6.5 * ince, omuzY + 3]), rot([gx + 6 * ince, omuzY + 12]), rot([gx + 4.6 * ince, omuzY + 22]), rot([gx + 6, kalca[1] + 1]), rot([gx - 6, kalca[1] + 1]), rot([gx - 5.5, omuzY + 16]), rot([gx - 7 * om, omuzY + 6])], .9);
      g.fill();
      if (tp.giysi === 'ceket' && !tp.cocuk) { // frak kuyruğu
        P(g, [rot([gx - 5.5, kalca[1] - 3]), rot([gx - 1, kalca[1]]), rot([gx - 3, kalca[1] + 22]), rot([gx - 8.5, kalca[1] + 21])], .8); g.fill(); }
      if (tp.giysi === 'palto') { P(g, [rot([gx - 7, kalca[1] - 5]), rot([gx + 7, kalca[1] - 4]), [gx + 9, kalca[1] + 28], [gx - 10, kalca[1] + 29]], .9); g.fill(); }
      if (tp.yaka) { P(g, [rot([gx + 1, omuzY - 3]), rot([gx + 6.5, omuzY - 7]), rot([gx + 6, omuzY - 1]), rot([gx + 4, omuzY + 1])], .9); g.fill(); }
      if (tp.giysi === 'pelerin') { // yırtık pelerin: omuzdan dize, saçaklı etek; salınımlı
        const sw = (o.pel || 0) * 4, pts = [rot([gx - 7.5, omuzY - 2]), rot([gx + 4, omuzY - 3]), rot([gx + 7.5, omuzY + 6])];
        const alt = []; for (let i = 0; i <= 8; i++) { const u = i / 8, xx = lerp(gx + 9, gx - 13, u) + sw * u, yy = -20 + (i % 2 ? -4 : 2) + Math.sin(i * 2.3) * 2; alt.push([xx, yy]); }
        P(g, [...pts, rot([gx + 7, omuzY + 18]), ...alt, rot([gx - 10, omuzY + 18]), rot([gx - 9, omuzY + 4])], .7); g.fill();
      }
    }
    // ---- boyun ve baş ----
    g.save(); g.translate(basM[0], basM[1]); g.rotate(-(govde * .6 + (o.bas || 0)));
    g.fillStyle = renk;
    g.beginPath(); g.moveTo(-3.2, 5); g.lineTo(-2.4, 9 + 1); g.lineTo(3.2, 9.5); g.lineTo(3.2, 4.5); g.closePath(); g.fill();   // boyun
    const bs = tp.cocuk ? 1.22 : 1;
    g.scale(bs, bs);
    // kafa: profil (alın, burun, dudak, çene) — yaratıkta çene uzun, elmacık çökük
    const yr = tp.giysi === 'pelerin';
    P(g, yr ? [[-6, -2], [-4.5, -7.6], [1, -8.6], [5, -6], [6, -2.6], [7.4, .6], [6.1, 1.4], [6.3, 3], [5.6, 3.6], [5.6, 5.4], [3.2, 7.6], [-1.6, 7], [-5.4, 3.4]]
      : [[-5.8, -2], [-4.2, -7], [1, -8], [4.8, -5.6], [5.6, -2.2], [7.2, .7], [5.8, 1.4], [6, 2.8], [5.4, 3.4], [5.2, 4.8], [2.6, 6.6], [-1.4, 6.2], [-5.2, 3]], .95);
    g.fill();
    // saç
    const sw = (o.sac || 0);
    if (tp.sac === 'uzun') { P(g, [[-6.2, -3], [-3.6, -8.8], [2.4, -9.6], [5.2, -6.8], [3, -6.4], [-1, -5], [-3, 0], [-4, 6], [-6 - sw * 3, 13], [-9 - sw * 5, 17], [-10.5 - sw * 6, 12], [-8.6, 5]], .9); g.fill(); }
    else if (tp.sac === 'kisa') { P(g, [[-6.2, -1.8], [-4.8, -7.8], [1.4, -9.2], [5.2, -6.6], [3.2, -6.6], [1.4, -5.2], [-2.4, -4], [-4.4, 1.6]], .9); g.fill(); }
    else if (tp.sac === 'daginik') { P(g, [[-6.6, -1.2], [-6, -7.6], [-1.6, -10.4], [3.2, -9.6], [6, -7.2], [3.6, -6.4], [0, -5.4], [-3.2, -2.6], [-5, 2.6]], .8); g.fill(); }
    else if (tp.sac === 'kivir') { for (const [a, b2, r] of [[-5, -6, 2.6], [-1.8, -8.4, 2.6], [1.8, -8.4, 2.4], [4.4, -6.6, 2], [-6.2, -2.4, 2.4], [-5.4, 1.4, 2]]) { g.beginPath(); g.arc(a, b2, r, 0, TAU); g.fill(); } }
    else if (tp.sac === 'topuz') { P(g, [[-6, -1.2], [-4.6, -7.6], [1.6, -9], [5, -6.4], [2.8, -6.2], [-1, -4.6], [-3.6, -1], [-4.6, 3]], .9); g.fill(); g.beginPath(); g.ellipse(-6.4, -5.6, 3.3, 3, .3, 0, TAU); g.fill(); // topuz
      for (let i = 0; i < 3; i++) { g.beginPath(); g.ellipse(4.2 - i * .3, -4.2 + i * 2.4, 1.1, 1.4, 0, 0, TAU); g.fill(); } }   // şakak bukleleri
    else if (tp.sac === 'ortu') { P(g, [[-6.4, -1], [-4.8, -8.2], [1.8, -9.4], [5.4, -6.6], [3.6, -5.8], [-2, -4.4], [-4, 4], [-6.6, 7]], .9); g.fill(); }
    // ihtiyar: ak saç ve sakal (açık boya: geçen ışık)
    if (tp.sac === 'ak') {
      const ak = o.akRenk || '#C9C2B4';
      g.fillStyle = ak; P(g, [[-6.4, -1.4], [-4.6, -7.4], [1, -8.2], [3.6, -6.8], [-1.6, -5.8], [-3.6, -1], [-4, 5], [-7.6, 8], [-8.4, 3]], .9); g.fill();
      P(g, [[3.6, 3.6], [6, 4.4], [5.4, 8.4], [2.4, 12.6], [-.6, 10], [-1.8, 5.4]], .9); g.fill(); g.fillStyle = renk;
    }
    // yaratığın gözü: küçük, sıcak (kanal kuralı: bembeyaz göz yok)
    if (yr && (o.goz ?? 1) > 0) { g.fillStyle = o.gozRenk || '#D9A441'; g.beginPath(); g.ellipse(3.6, -1.4, 1.05, .62 * (o.goz ?? 1), 0, 0, TAU); g.fill(); }
    if (o.kenar) { // yakın planda kenar ışığı: profilin önüne ince sıcak çizgi
      g.strokeStyle = o.kenar; g.lineWidth = .55; g.beginPath(); spline(g, yr ? [[1, -8.6], [5, -6], [6, -2.6], [7.4, .6]] : [[1, -8], [4.8, -5.6], [5.6, -2.2], [7.2, .7]], false); g.stroke(); }
    g.restore();
    // ---- ön kol (en son) ----
    const onKol = kolCiz(kO, false);
    if (o.el && o.el.on) { g.save(); o.el.on(R, onKol); g.restore(); }
    g.restore();
    // eklem noktaları (dünya koordinatı): el uçları
    const W2 = p => [x + p[0] * s * f, y + p[1] * s];
    return { elO: W2(onKol.e), elA: W2(arkaKol.e), bas: W2(basM), omuz: W2(omuz), kalca: W2(kalca), s, f };
  }
  // yatan beden (masadaki yaratık, tabuttaki ölü): yatay siluet; o.kalk 0..1 göğsün kalkması
  function yatan(R, x, y, boy, o = {}) {
    const g = R.g, s = boy / 100, f = o.f || 1; g.save(); g.translate(x, y); g.scale(f * s, s); g.fillStyle = o.renk || K();
    const nf = o.nefes || 0;
    P(g, [[-50, -4], [-46, -10], [-30, -11 - nf], [-14, -12 - nf * 1.4], [0, -10], [14, -8], [30, -7], [44, -6], [50, -3], [50, 0], [-50, 0]], .8); g.fill();
    g.beginPath(); g.ellipse(-58, -7, 7.6, 6.2, 0, 0, TAU); g.fill();       // baş (sola)
    if (o.sac) { P(g, [[-64, -10], [-58, -14], [-51, -11], [-54, -2], [-62, 2], [-70, 1], [-67, -6]], .8); g.fill(); }
    if (o.goz) { g.fillStyle = '#D9A441'; g.beginPath(); g.ellipse(-56, -12, 1.2, .7 * o.goz, 0, 0, TAU); g.fill(); }
    g.restore();
  }
  return { kisi, yatan, kol };
})();
