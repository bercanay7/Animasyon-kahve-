// Siluet figürler (Çernobil'in çayı; frankenstein/lib/figur.js'ten 1986 Karadeniz'ine uyarlandı). ORTAK DOSYA: yalnız başkan değiştirir.
// Figürler çizgi plakasına (BASKI.l) düz mürekkeple basılır (kanal kuralı: ana figür koyu siluet). Uzak figür ton plakasına (o.renk gri) basılabilir.
// Yerel uzay: ayaklar y = 0, baş tepesi y = -100 (boy birimi), figür +x'e bakar. FIG.kisi(g, x, zeminY, boy, o) — g: 2B bağlam (BASKI.l ya da BASKI.k)
//   o.tip: 'toplayici' (yemenili, etekli çay toplayan kadın) | 'kadin' | 'takim' (takım elbiseli) | 'gazeteci' | 'isci' (kasketli) | 'koylu' | 'laborant' (önlüklü) | 'cocuk'
//   o.f: 1 sağa, -1 sola · o.govde: öne eğilme (radyan, + öne) · o.bas: baş eğimi (+ öne/aşağı)
//   o.kolO / o.kolA: [omuz açısı, dirsek bükümü] (0 = aşağı sarkık, + = öne kalkar; dirsek + öne bükülür)
//   o.bacak: 'dur' | 'otur' | 'diz' | 'cok' | HAREKET poz nesnesi · o.el: {on: fn(g, el), arka: fn} (el: {d, e, a} yerel)
// Hassasiyet (CLAUDE.md): düz kalkık kol yok (dirsek hep bükük), göğüste/yakada beyaz dikdörtgen yok (kravat ve gömlek yakası çizilmez),
//   simetrik açık kol yok, başın yanında açık leke yok; yemenili kadın baştan ayağa koyu değil: yemeni ve etek ton plakasında desenli (FIG.desen).
'use strict';
const FIG = (() => {
  const K = () => '#000';
  const P = (g, pts, k = 1) => { g.beginPath(); spline(g, pts, true, k); };
  // üstü eğri, altı düz kenarlı biçim (etek ve palto ucu taşmasın): ust eğri noktaları, alt düz noktalar
  const P2 = (g, ust, alt) => { g.beginPath(); spline(g, ust, false, .9); for (const q of alt) g.lineTo(q[0], q[1]); g.closePath(); };
  // sivrilen uzuv: p0→p1, kalınlık w0→w1, uçlar yuvarlak
  function uzuv(g, p0, p1, w0, w1) {
    const dx = p1[0] - p0[0], dy = p1[1] - p0[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    g.beginPath(); g.moveTo(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2); g.lineTo(p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2);
    g.lineTo(p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2); g.lineTo(p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2); g.closePath(); g.fill();
    g.beginPath(); g.arc(p0[0], p0[1], w0 / 2, 0, TAU); g.arc(p1[0], p1[1], w1 / 2, 0, TAU); g.fill();
  }
  const kol = (o, a1, a2, l1, l2) => { const d = [o[0] + Math.sin(a1) * l1, o[1] + Math.cos(a1) * l1]; const b = a1 + a2; return [d, [d[0] + Math.sin(b) * l2, d[1] + Math.cos(b) * l2]]; };
  const TIP = {
    takim: { olc: 1, giysi: 'ceket', sac: 'kisa', ince: 1.05 },
    gazeteci: { olc: .98, giysi: 'ceket', sac: 'kisa3', ince: 1 },
    isci: { olc: 1, giysi: 'yelek', sac: 'kasket', ince: 1.08 },
    koylu: { olc: .97, giysi: 'yelek', sac: 'kasket', ince: 1.12 },
    laborant: { olc: 1, giysi: 'palto', sac: 'kisa', ince: 1 },
    toplayici: { olc: .92, giysi: 'etek', sac: 'yemeni', ince: .98, kadin: 1 },
    kadin: { olc: .93, giysi: 'etek', sac: 'kisa2', ince: .92, kadin: 1 },
    cocuk: { olc: .58, giysi: 'yelek', sac: 'kisa', ince: 1.05, cocuk: 1 },
  };
  // baş (yerel; merkez 0,0, yaklaşık yarıçap 6,4; +x yüz). yr: yaratık (uzun çene, çökük yanak)
  function bas(g, tp, o, yr) {
    const prof = yr ? [[-6.2, -1.5], [-5, -6.8], [-1, -8.6], [3.2, -7.6], [5.6, -4.6], [5.9, -2.4], [7.2, .4], [6, 1.2], [6.1, 2.3], [5.4, 2.8], [5.5, 4], [4.6, 5.4], [2.2, 6.4], [-.8, 6], [-3.8, 4.4], [-5.8, 2]]
      : tp.cocuk ? [[-6.4, -.8], [-5.4, -6.6], [-1, -8.4], [3.4, -7], [5.6, -3.8], [5.8, -1.6], [6.8, .8], [5.6, 1.6], [5.8, 2.6], [5, 3.4], [5, 4.6], [2.6, 6.2], [-1.6, 6], [-5, 3]]
      : [[-6, -1.4], [-4.8, -6.6], [-.8, -8.2], [3.2, -7.2], [5.3, -4.4], [5.6, -2], [7, .6], [5.7, 1.4], [5.9, 2.6], [5.2, 3.2], [5.3, 4.6], [4.4, 6], [2, 7.2], [-1.4, 6.6], [-4.6, 3.8]];
    P(g, prof, .95); g.fill();
    const sw = o.sac || 0;
    if (tp.sac === 'uzun') { P(g, [[-6.4, -2.6], [-4.6, -8.2], [.6, -9.8], [4.4, -8.2], [5.6, -6.2], [2.6, -6.6], [-.8, -5.6], [-2.6, -1], [-3.2, 5], [-4.4 - sw * 2, 10.5], [-6.6 - sw * 3, 13], [-8.6 - sw * 4, 10], [-8.8 - sw * 2, 4], [-8, 0]], .85); g.fill(); }
    else if (tp.sac === 'uzun2') { P(g, [[-6.4, -2.4], [-4.8, -7.8], [.4, -9], [3.6, -7.6], [1.4, -6.6], [-1.6, -5], [-3, 1], [-4.6, 8], [-7.8, 9], [-8.4, 3]], .85); g.fill(); }
    else if (tp.sac === 'kisa') { P(g, [[-6.4, -1.4], [-5.2, -7.6], [.6, -9.4], [4.6, -7.6], [5.2, -5.6], [2.4, -6.4], [.4, -5], [-2.4, -4.4], [-4.6, .8]], .85); g.fill(); }
    else if (tp.sac === 'daginik') { P(g, [[-6.8, -.6], [-6.8, -6.4], [-3.4, -10], [1, -10.6], [4.6, -9.2], [6.4, -6.6], [3.6, -6.2], [.4, -5.2], [-2.8, -3.4], [-4.6, 2.6]], .8); g.fill(); }
    else if (tp.sac === 'kivir') { for (const [a, b, r] of [[-4.6, -6.6, 2.7], [-1.4, -8.6, 2.7], [2, -8.6, 2.5], [4.6, -6.6, 2], [-6.4, -3, 2.4], [-6, .8, 2.1], [-4.2, 3.4, 1.6]]) { g.beginPath(); g.arc(a, b, r, 0, TAU); g.fill(); } }
    else if (tp.sac === 'topuz') { P(g, [[-6.2, -1], [-5, -7.4], [.8, -9.2], [4.4, -7.6], [5.2, -5.6], [2.6, -6], [-.4, -4.6], [-3, -.6], [-4, 3]], .85); g.fill();
      g.beginPath(); g.ellipse(-6.6, -6.4, 3.4, 3.1, .3, 0, TAU); g.fill();
      for (let i = 0; i < 3; i++) { g.beginPath(); g.ellipse(4.6 - i * .5, -4.8 + i * 2.2, 1.2, 1.5, 0, 0, TAU); g.fill(); } }
    else if (tp.sac === 'topuz2') { P(g, [[-6.2, -1], [-5, -7.4], [.8, -9.2], [4.4, -7.6], [5.2, -5.6], [2.6, -6], [-.4, -4.6], [-3, -.6], [-4, 2]], .85); g.fill(); g.beginPath(); g.ellipse(-6.8, -3.6, 3, 2.8, .3, 0, TAU); g.fill(); }
    else if (tp.sac === 'ortu') { P(g, [[-6.8, -.4], [-5.4, -8.4], [1, -10], [4.8, -8.2], [5.8, -5.6], [3.6, -5.6], [-1.6, -4.2], [-3.4, 3], [-5.6, 8], [-8.4, 6]], .85); g.fill(); }
    else if (tp.sac === 'kisa2') { P(g, [[-7, 1], [-7.2, -6], [-2.6, -10], [2.6, -10], [5.8, -7.6], [6, -5], [3, -6], [.2, -4.6], [-2.6, -3], [-4.4, 2.6], [-5.4, 4.6]], .85); g.fill(); }
    else if (tp.sac === 'kisa3') { P(g, [[-6.4, -.6], [-5.6, -7.8], [.6, -9.8], [4.8, -8.4], [5.8, -6], [2.8, -6.6], [.4, -5.6], [-2.4, -4.6], [-4.6, 1.6]], .85); g.fill(); }
    else if (tp.sac === 'kasket') { P(g, [[-6.6, -2.4], [-6.4, -7.6], [-1, -10.2], [4.2, -9.6], [7.2, -8], [10, -6.6], [9.6, -5.6], [5.4, -5.8], [-1, -5.2], [-5.4, -1]], .8); g.fill(); }
    else if (tp.sac === 'yemeni') { // başı saran yemeni: alında saç çizgisinin üstünden, ensede düğüm ve iki uç
      P(g, [[-6.8, 1.6], [-6.4, -6.6], [-1.6, -10], [3.4, -9.4], [5.8, -6.8], [5.4, -5.2], [2, -6], [-.6, -4.8], [-2.4, -2.2], [-3.4, 2.4], [-5, 4.6]], .85); g.fill();
      g.beginPath(); g.ellipse(-7.4, .8, 2.2, 1.8, .4, 0, TAU); g.fill();
      P(g, [[-7.6, 1.6], [-10.6, 6.6], [-9.4, 7.4], [-7, 3]], .8); g.fill(); P(g, [[-8, 1.2], [-12, 3.8], [-11.4, 5], [-7.4, 2.6]], .8); g.fill(); }
    else if (tp.sac === 'sapka') { P(g, [[-9, -6], [8.4, -6.4], [8.4, -5.2], [4.6, -5.2], [4.4, -10.4], [-4.6, -10.6], [-5, -5.2], [-9, -5]], .7); g.fill(); }
    if (tp.sakal) { P(g, [[5.2, 3.4], [6, 6.6], [4.6, 11.4], [1.6, 13.4], [-1.2, 10.4], [-2.4, 6.6], [1, 7.4]], .85); g.fill(); }
    if (yr && (o.goz ?? 1) > 0) { g.fillStyle = o.gozRenk || '#C98A2E'; g.beginPath(); g.ellipse(3.3, -1.6, .85, .5 * (o.goz ?? 1), -.1, 0, TAU); g.fill(); g.fillStyle = o.renk || K(); }
    if (o.kenar) { g.save(); g.strokeStyle = o.kenar; g.lineWidth = .5; g.lineCap = 'round'; g.beginPath(); spline(g, prof.slice(4, 10), false); g.stroke(); g.restore(); }   // yalnız yüz (alından çeneye): başın tepesinde ışık yayı hale okunur
  }
  // el: avuç + başparmak (+ yaratıkta uzun ince parmaklar); a: kolun yönü
  function el(g, p, a, s, uzun) {
    g.save(); g.translate(p[0], p[1]); g.rotate(-a);
    g.beginPath(); g.ellipse(0, 2 * s, 1.5 * s, 2.5 * s, 0, 0, TAU); g.fill();
    g.beginPath(); g.ellipse(1.4 * s, 1 * s, .65 * s, 1.6 * s, -.6, 0, TAU); g.fill();
    if (uzun) for (let i = -1; i <= 1; i++) uzuv(g, [i * .55 * s, 3.4 * s], [i * .9 * s, 7 * s], .75 * s, .45 * s);
    g.restore();
  }
  function kisi(g, x, y, boy, o = {}) {
    const tp = TIP[o.tip || 'takim'], R = g, f = o.f || 1, s = boy * tp.olc / 100, renk = o.renk || K();
    const yr = false, ince = tp.ince, govde = (o.govde || 0) + (tp.kambur || 0);
    g.save(); g.translate(x, y); g.scale(f * s, s); g.fillStyle = renk;
    // ---- bacak eklemleri ----
    let kalca = [0, -50], ayak = [[3, -3], [-2.5, -3]], diz = [[2.2, -26.5], [-1.6, -26.5]];
    const b = o.bacak || 'dur';
    if (typeof b === 'object') { const m = p => [(p[0] - 40) * 1.05, (p[1] - 120) * 1.05]; kalca = m(b.kalca); ayak = [m(b.ayaklar[b.on].bilek), m(b.ayaklar[1 - b.on].bilek)]; diz = [m(b.ayaklar[b.on].diz), m(b.ayaklar[1 - b.on].diz)]; }
    else if (b === 'otur') { kalca = [-2, -26]; diz = [[20, -27.5], [18, -26.5]]; ayak = [[21, -3], [16.5, -3]]; }
    else if (b === 'diz') { kalca = [-1, -25]; diz = [[16, -22], [-6, -1.5]]; ayak = [[18, -3], [-23, -2]]; }
    else if (b === 'cok') { kalca = [-6, -19]; diz = [[12, -30], [9, -27]]; ayak = [[10, -3], [4, -3]]; }
    const omuzY = kalca[1] - 32, gx = kalca[0];
    const rot = p => { const dx = p[0] - kalca[0], dy = p[1] - kalca[1], c = Math.cos(govde), sn = Math.sin(govde); return [kalca[0] + dx * c - dy * sn, kalca[1] + dx * sn + dy * c]; };   // + govde: öne eğilir (25 Kasım düzeltmesi: işaret tersti)
    const omuz = rot([gx, omuzY + 1.5]);
    const basM = rot([gx + 2.6, omuzY - 10.6]);
    const kA = o.kolA || [-.12, .28], kO = o.kolO || [.1, .32], L1 = 16, L2 = 14.5, elS = tp.el || 1;
    const kolCiz = (kk, arka) => {
      if (kk[0] < .32 && !o.serbest) kk = [Math.min(kk[0], -.04), Math.min(kk[1], .12)];
      const sp = [omuz[0] + (arka ? -1 : 1), omuz[1] + 1.5];
      const [d, e] = kol(sp, kk[0] + govde, kk[1], L1, L2);
      const w = (yr ? 3.4 : tp.kadin ? 3.2 : 4.2) * ince;
      uzuv(g, sp, d, w * 1.05, w * .82); uzuv(g, d, e, w * .82, w * .58);
      if (tp.kadin && tp.giysi === 'elbise') { g.beginPath(); g.ellipse(sp[0] + Math.sin(kk[0] + govde) * 3, sp[1] + Math.cos(kk[0] + govde) * 3, 3.4, 3.8, -(kk[0] + govde), 0, TAU); g.fill(); }   // kabarık kısa kol
      const a = kk[0] + kk[1] + govde; el(g, e, a, elS * (tp.cocuk ? .9 : 1), yr);
      return { d, e, a };
    };
    // ---- arka kol ----
    const arkaKol = kolCiz(kA, true);
    if (o.el && o.el.arka) { g.save(); o.el.arka(g, arkaKol); g.restore(); }
    // ---- bacaklar (etekli değilse) ----
    const ayakkabi = (a, uz = 1) => { g.beginPath(); g.moveTo(a[0] - 2.6, a[1] - 1.4); g.quadraticCurveTo(a[0] + 2, a[1] - 2.2, a[0] + 6.6 * uz, a[1] + 1.6); g.lineTo(a[0] + 6.6 * uz, a[1] + 2.8); g.lineTo(a[0] - 2.4, a[1] + 2.8); g.closePath(); g.fill(); };
    const bacak = (k, d, a, w) => { uzuv(g, k, d, w * 1.25, w * .9); uzuv(g, d, a, w * .9, w * .55); ayakkabi(a, yr ? 1.15 : 1); };
    if (b === 'otur' && o.sandalye !== false) { g.save(); g.fillStyle = o.sandalyeRenk || renk;
      g.fillRect(kalca[0] - 9, kalca[1] + 2, 20, 2.6); g.fillRect(kalca[0] - 8.6, kalca[1] + 4, 2, -kalca[1] - 4); g.fillRect(kalca[0] + 8.4, kalca[1] + 4, 2, -kalca[1] - 4);
      g.fillRect(kalca[0] - 10.6, kalca[1] - 26, 2.2, 30); g.restore(); }
    const etekli = tp.kadin || tp.giysi === 'cubbe';
    if (!etekli) { const w = (yr ? 4.2 : 5) * ince; bacak([kalca[0] - .5, kalca[1]], diz[1], ayak[1], w); bacak([kalca[0] + .5, kalca[1]], diz[0], ayak[0], w); }
    // ---- gövde ----
    const T = (x_, y_) => rot([gx + x_, omuzY + y_]);
    if (tp.kadin) {
      // 1980'ler: belde etek, baldır ortasına; etek altında bacaklar (yürüyüşte açılır)
      const ac = typeof b === 'object' ? (ayak[0][0] - ayak[1][0]) * .3 : 0;
      P(g, [T(-5, -1.5), T(1.2, -3), T(5.4 * ince, 2.5), T(5.8 * ince, 9), T(4.4 * ince, 17), T(4.6 * ince, 23), T(-4.8 * ince, 23), T(-5 * ince, 12), T(-6, 4)], .9); g.fill();
      if (b === 'otur') P(g, [T(-5.6, 21), T(5, 21), [diz[0][0] + 3, diz[0][1] - 2], [diz[0][0] + 4, diz[0][1] + 4], [diz[0][0] - 6, diz[0][1] + 6], [kalca[0] - 8, kalca[1] + 4]], .85);
      else P2(g, [[gx - 8.6 + ac * .2, -15], T(-5.6, 21), T(5, 21), [gx + 8.6 + ac, -15]], [[gx + 9.4 + ac, -14.4], [gx - 9.4, -14.4]]);
      g.fill();
      const w = 4 * ince;
      const alt = (d, a) => { uzuv(g, d, a, w * .85, w * .55); ayakkabi(a, .9); };
      if (b === 'otur') { alt(diz[1], ayak[1]); alt(diz[0], ayak[0]); }
      else { const dz = k => [lerp(kalca[0], ayak[k][0], .62), lerp(kalca[1], ayak[k][1], .62)]; alt(typeof b === 'object' ? diz[1] : dz(1), ayak[1]); alt(typeof b === 'object' ? diz[0] : dz(0), ayak[0]); }
      if (o.desen !== false) R._desen = { etek: [[gx - 8.6, -15], T(-5.6, 21), T(5, 21), [gx + 8.6, -15]], f, s, x, y };
    } else if (tp.giysi === 'cubbe') {
      if (b === 'otur') P(g, [T(-6, -1), T(2, -3), T(6.4, 3), T(6.6, 14), T(5.4, 26), [diz[0][0] + 3, diz[0][1] - 2], [ayak[0][0] + 3, -2], [ayak[0][0] - 6, -1], [diz[0][0] - 6, diz[0][1] + 7], [kalca[0] - 9, kalca[1] + 3], T(-7, 20), T(-7.4, 6)], .85);
      else P2(g, [[gx - 9.6, -14], T(-7.4, 8), T(-6, -1), T(2, -3), T(6.4, 3), T(6.6, 14), [gx + 9.4, -14]], [[gx + 10.4, -1], [gx - 10.4, -1]]);
      g.fill();
      for (const a of ayak) ayakkabi(a);
    } else {
      // göğüs, bel, kalça
      P(g, [T(-5.2, -1.5), T(1.4, -3), T(5.8 * ince, 2.5), T(6.2 * ince, 9), T(4.6 * ince, 17), T(4.2 * ince, 24), T(5.6, 31), T(-5.4, 31.5), T(-4.6 * ince, 22), T(-5.2 * ince, 12), T(-6.4, 4)], .9); g.fill();
      if (tp.giysi === 'ceket') P(g, [T(-6, 24), T(6, 24), T(6.6, 36), T(-6.4, 36.5)], .8), g.fill();          // ceket eteği (kalça altına)
      if (tp.giysi === 'palto') P2(g, [[gx - 9, kalca[1] + 22], T(-5.6, 18), T(5.6, 18), [gx + 8.6, kalca[1] + 22]], []), g.fill();
      if (tp.yaka) P(g, [T(.6, -3), T(5.6, -7.2), T(5.8, -2), T(3.8, .6)], .85), g.fill();                           // açık yaka (şair)
      if (yr) { // yırtık pelerin: omuzlardan sırta, dize kadar; saçaklı kenar; salınım
        const sw = (o.pel || 0) * 4, alt = []; for (let i = 0; i <= 9; i++) { const u = i / 9; alt.push([lerp(gx + 6, gx - 11, u) + sw * u, kalca[1] + 12 + (i % 2 ? -4 : 1.5) + Math.sin(i * 2.3) * 1.4]); }
        P(g, [T(-6.4, 0), T(-1.6, -1.6), T(1.6, 1.4), T(2.6, 12), [gx + 5, kalca[1] + 4], ...alt, T(-9, 22), T(-8.4, 8)], .7); g.fill();   // pelerin sırtta; göğüs ve bel önden görünür
      }
    }
    // ---- boyun ve baş ----
    g.save(); g.translate(basM[0], basM[1]); g.rotate(govde * .55 + (o.bas || 0));   // + bas: baş öne/aşağı
    uzuv(g, [-.6, 4.6], [-1.4, 10.2], 4.8, 5.4);
    if (tp.cocuk) g.scale(1.22, 1.22);
    bas(g, tp, { ...o, renk }, yr);
    g.restore();
    // ---- ön kol ----
    const onKol = kolCiz(kO, false);
    if (o.el && o.el.on) { g.save(); o.el.on(g, onKol); g.restore(); }
    g.restore();
    const W2 = p => [x + p[0] * s * f, y + p[1] * s];
    return { elO: W2(onKol.e), elA: W2(arkaKol.e), dirsekO: W2(onKol.d), bas: W2(basM), omuz: W2(omuz), kalca: W2(kalca), s, f };
  }
  // yatan beden: yatay siluet (sırtüstü; baş solda f=1); o.nefes göğsün kalkması, o.goz yaratık
  function yatan(g, x, y, boy, o = {}) {
    const s = boy / 100, f = o.f || 1; g.save(); g.translate(x, y); g.scale(f * s, s); g.fillStyle = o.renk || K();
    const nf = o.nefes || 0;
    P(g, [[-44, -3], [-40, -10], [-28, -12 - nf], [-14, -11.5 - nf * 1.2], [-2, -8], [10, -8.5], [24, -7], [40, -5.6], [48, -9], [52, -8], [52, 0], [-44, 0]], .8); g.fill();
    g.beginPath(); g.ellipse(-51, -6.4, 7, 6, 0, 0, TAU); g.fill();
    if (o.profil !== false) { P(g, [[-55, -10], [-52, -12.2], [-49, -12.4], [-47.8, -13.6], [-46.2, -11.6], [-45.2, -9], [-45.6, -5]], .9); g.fill(); }   // yukarı bakan profil (alın, burun, çene)
    if (o.kadin) { P(g, [[-57, -9], [-62, -12], [-68, -8], [-70, -1], [-62, 2], [-55, -1]], .8); g.fill(); }
    if (o.sac) { P(g, [[-58, -8], [-53, -13], [-46, -11], [-47, -2], [-56, 1.5], [-64, 0], [-62, -5]], .8); g.fill(); }
    if (o.goz) { g.fillStyle = '#C98A2E'; g.beginPath(); g.ellipse(-49, -11.6, .9, .5 * o.goz, 0, 0, TAU); g.fill(); }
    g.restore();
  }
  // yakın plan el (ön kol + avuç + parmaklar): f yön, uzun: yaratığın ince uzun parmakları, kap: parmakların kapanması 0..1
  function elYakin(g, x, y, sc, f = 1, uzun = false, kap = 0) {
    g.save(); g.translate(x, y); g.scale(f * sc, sc); g.fillStyle = '#000';
    uzuv(g, [-26, 3], [-4, 0], 6.4, 5.2); g.beginPath(); g.ellipse(0, 0, 4.2, 2.6, 0, 0, TAU); g.fill();
    for (let i = 0; i < 4; i++) uzuv(g, [2.6, -1.4 + i * 1.1], [uzun ? 9.5 : 6.6, -2.4 + i * 1.6 + kap * (2 + i * .5)], 1.1, .8);
    uzuv(g, [0, -2], [2.6, -4.6], 1.3, 1); g.restore();
  }
  // küfe: sırtta taşınan, ağzı geniş çay sepeti (dünya koordinatı; omuz noktasına göre). B: BASKI. Örgü ton plakasında, kenar çizgi plakasında.
  function kufe(B, om, s, f = 1, dolu = 0) {
    const k = B.k, l = B.l, w0 = 15 * s, w1 = 9 * s, h = 26 * s, x = om[0] - f * 9 * s, y = om[1] - 4 * s;
    const yol = g => { g.moveTo(x - w0 / 2, y - h * .25); g.lineTo(x + w0 / 2, y - h * .25); g.lineTo(x + w1 / 2, y + h * .75); g.lineTo(x - w1 / 2, y + h * .75); g.closePath(); };
    k.save(); k.beginPath(); yol(k); k.fillStyle = B.ton(.55); k.fill(); k.clip(); k.strokeStyle = B.ton(.95); k.lineWidth = Math.max(1, s * .9);
    for (let i = -6; i <= 6; i++) { k.beginPath(); k.moveTo(x + i * s * 2.2, y - h * .3); k.lineTo(x + i * s * 1.4, y + h * .8); k.stroke(); }
    for (let j = 0; j < 7; j++) { k.beginPath(); k.moveTo(x - w0, y - h * .25 + j * h / 6.5); k.lineTo(x + w0, y - h * .25 + j * h / 6.5); k.stroke(); }
    k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = Math.max(1.5, s * 1.3); l.beginPath(); yol(l); l.stroke();
    l.beginPath(); l.moveTo(x - w0 / 2, y - h * .25); l.quadraticCurveTo(om[0] + f * 3 * s, om[1] - 2 * s, om[0] + f * 4 * s, om[1] + 8 * s); l.stroke(); l.restore();   // askı
    if (dolu > 0) B.cayBoya(g => { g.ellipse(x, y - h * .25, w0 * .5, h * .12 * dolu, 0, PI, TAU); }, 1, 0);   // ağızdan taşan yeşil yaprak
  }
  // desen: yemenili kadının eteğini ve başını ton plakasında açığa çeker (baştan ayağa koyu örtü okunmasın): son kisi() çağrısının etek yolu
  function desen(B, o = {}) {
    const d = B.l._desen; if (!d) return; B.l._desen = null;
    const k = B.k, l = B.l, tr = p => [d.x + p[0] * d.s * d.f, d.y + p[1] * d.s];
    const pts = d.etek.map(tr);
    l.save(); l.fillStyle = '#fff'; l.beginPath(); poly(l, pts, true); l.fill(); l.restore();   // eteği çizgi plakasından çıkar (beyaz = mürekkepsiz; saydam piksel siyah basılır)
    k.save(); k.beginPath(); poly(k, pts, true); k.fillStyle = B.ton(o.zemin ?? .62); k.fill(); k.clip();
    k.fillStyle = B.ton(.95); const r = rng(o.tohum || 7), sx = d.s * 3.4;
    for (let yy = -40; yy < 40; yy += sx) for (let xx = -40; xx < 40; xx += sx) { k.beginPath(); k.arc(d.x + xx * d.s + (r() - .5) * d.s, d.y - 15 * d.s + yy * d.s, d.s * .9, 0, TAU); k.fill(); }
    k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = Math.max(1.2, d.s * .9); l.beginPath(); poly(l, pts, true); l.stroke(); l.restore();
  }
  return { kisi, yatan, uzuv, elYakin, kufe, desen };
})();
