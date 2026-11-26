// Viktorya figürleri (gravür dili, milton KILAVUZ): düz siyah siluet + ışık yanında ince kenar ışığı + gövdeye giren birkaç beyaz kıvrım vuruşu.
// Kural: Dorian'ın yüzü dünyada görünmez (arka/¾ arka ya da gölgede). Basil ve Henry profil siluet olabilir; yüz ayrıntısı yok, kontur okunur.
// Koordinat: ayak tabanı orta (x, y); h = boy (px). yon = +1 sağa bakar, −1 sola. GR.frame ile yerel çerçeve (760 birim boy).
'use strict';
const INSAN = (() => {
  const PI = Math.PI;
  const F = pts => { const p = new Path2D(); p.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) p.lineTo(pts[i][0], pts[i][1]); p.closePath(); return p; };
  const Sm = pts => { const p = new Path2D(), n = pts.length; p.moveTo(pts[0][0], pts[0][1]);
    for (let i = 0; i < n; i++) { const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      p.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]); }
    p.closePath(); return p; };
  const fill = (p, ton, h) => GR.fill(p, GR.tone(ton), h || { th: PI / 2, id: 9 });
  const SIL = .03;   // siluet tonu (düz siyah)
  // kenar şeridi: bir eğrinin (pts) içine doğru kalınlık w kadar şerit (ışık yanı)
  function serit(pts, w, ton, nx) { const ins = pts.slice().reverse().map(([x, y]) => [x - nx * w, y]); fill(Sm([...pts, ...ins]), ton, { th: PI / 2, id: 9 }); }
  // beyaz kıvrım vuruşu: sivrilen ince çizgi (milton cehennem tarifi)
  function vurus(x0, y0, x1, y1, w = 5, ton = .9) { const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1, nx = -dy / L * w * .5, ny = dx / L * w * .5;
    fill(F([[x0 + nx, y0 + ny], [x1, y1], [x0 - nx, y0 - ny]]), ton, { th: 0, id: 9 }); }
  // kol: omuz (0,0); a üst kol açısı (0 = aşağı, + = ileri), b dirsek bükümü; uzunluk 300; el: 'yumruk' | 'acik'
  function kol(a, b, o = {}) {
    const L1 = 150, L2 = 140, w1 = o.w || 46, ton = o.ton ?? SIL;
    const ux = Math.sin(a), uy = Math.cos(a), ex = ux * L1, ey = uy * L1, a2 = a + b, vx = Math.sin(a2), vy = Math.cos(a2), wx = ex + vx * L2, wy = ey + vy * L2;
    const n = (x, y, s) => [-y * s, x * s];
    const [a1x, a1y] = n(ux, uy, w1 * .5), [e1x, e1y] = n(ux, uy, w1 * .4), [e2x, e2y] = n(vx, vy, w1 * .38), [w2x, w2y] = n(vx, vy, w1 * .26);
    fill(Sm([[a1x, a1y - 6], [ex + e1x, ey + e1y], [ex + e2x, ey + e2y], [wx + w2x, wy + w2y], [wx - w2x, wy - w2y], [ex - e2x, ey - e2y], [ex - e1x, ey - e1y], [-a1x, -a1y - 6]]), ton);
    // manşet (beyaz) ve el
    fill(F([[wx + w2x, wy + w2y], [wx + w2x + vx * 10, wy + w2y + vy * 10], [wx - w2x + vx * 10, wy - w2y + vy * 10], [wx - w2x, wy - w2y]]), .88, { th: 0, id: 5 });
    const hx = wx + vx * 12, hy = wy + vy * 12, hp = new Path2D(); hp.ellipse(hx + vx * 22, hy + vy * 22, 15, 26, -a2, 0, 2 * PI); fill(hp, o.elTon ?? .42, { th: .6, id: 5 });
    if (o.kenar != null) serit([[ex + e1x * (o.kYan || 1), ey + e1y * (o.kYan || 1)], [wx + w2x * (o.kYan || 1), wy + w2y * (o.kYan || 1)]].map(p => p), 5, o.kenar, o.kYan || 1);
    return [hx + vx * 40, hy + vy * 40];
  }
  // ADAM: o = { x, y, h, yon, arka, sapka, palto (0..1 etek boyu), kolOn/kolArka {a, b}, bas (baş eğimi rad), adim (yürüyüş fazı; null = duruş),
  //   egim (gövde eğimi), ton, kenar (kenar ışığı tonu, null = yok), kenarYan (+1 ön/ışık yanı ile aynı yön, −1 sırt), biyik, sakal, sigara, yuzTon }
  function adam(o) {
    const h = o.h || 600, k = h / 760, yon = o.yon || 1, ton = o.ton ?? SIL, kn = o.kenar, ks = (o.kenarYan ?? 1);
    const eg = o.egim || 0, ce = Math.cos(eg), se = Math.sin(eg);
    const W = (lx, ly) => [o.x + (lx * ce - ly * se) * yon * k, o.y + (lx * se + ly * ce) * k];   // yerel → dünya (yön aynalı)
    const ad = o.adim, sw = ad == null ? 0 : Math.sin(ad * 2 * PI) * .26;
    // arka kol (gövdenin arkasında)
    const ka = o.kolArka || { a: -.06, b: .08 };
    { const [sx, sy] = W(-44, -628); GR.save(); GR.frame(sx, sy, eg * yon, yon, k); kol(ka.a - sw * .8, ka.b, { ton: Math.max(0, ton - .01), w: 42 }); GR.restore(); }
    GR.save(); GR.frame(o.x, o.y, eg * yon, yon, k);
    // bacaklar (pantolon, ayakkabı)
    for (const [s, dx] of [[1, 20], [-1, -22]]) { const a = sw * s, top = -300, fx = dx + Math.sin(a) * 300, fy = top + Math.cos(a) * 300 - 8;
      fill(Sm([[dx - 30, top], [dx + 28, top], [(dx + fx) / 2 + 22, (top + fy) / 2], [fx + 18, fy - 4], [fx - 18, fy - 4], [(dx + fx) / 2 - 24, (top + fy) / 2]]), ton);
      fill(Sm([[fx - 22, fy - 10], [fx + 20, fy - 12], [fx + 46, fy + 2], [fx + 40, fy + 8], [fx - 22, fy + 8]]), .02, { th: 0, id: 9 });
      if (kn != null) vurus(dx + 20 * ks, top + 20, fx + 14 * ks, fy - 30, 4, kn); }
    // redingot: eğimli omuz, içeri bel, dizde etek
    const et = -300 + (1 - (o.palto ?? 1)) * 140;
    const govde = [[-64, -642], [-30, -662], [34, -662], [70, -642], [84, -604], [80, -540], [64, -470], [70, -420], [92, et], [-86, et], [-66, -420], [-58, -470], [-70, -540], [-78, -604]];
    fill(Sm(govde), ton);
    if (kn != null) { const yanX = ks > 0 ? [[70, -642], [84, -604], [80, -540], [64, -470], [70, -420], [92, et]] : [[-64, -642], [-78, -604], [-70, -540], [-58, -470], [-66, -420], [-86, et]]; serit(yanX, 7, kn, ks); }
    // kıvrımlar (beyaz vuruşlar) ve önden yaka açıklığı / arkadan yırtmaç
    if (o.arka) { vurus(4, -430, 6, et + 10, 4, .5); if (kn != null) { vurus(40 * ks, -560, 28 * ks, -470, 4, kn * .9); vurus(30 * ks, -440, 50 * ks, et + 40, 3, kn * .8); } }
    else { fill(F([[0, -654], [16, -654], [30, -480], [8, -440], [-14, -480]]), .16, { th: PI / 2, id: 9 }); vurus(10, -460, 34, et + 20, 3, .7); if (kn != null) vurus(46 * ks, -600, 40 * ks, -500, 4, kn); }
    // yaka (beyaz) ve boyun
    fill(F([[-22, -684], [28, -684], [34, -656], [-26, -656]]), o.yaka ?? (o.arka ? .8 : .9), { th: 0, id: 5 });   // o.yaka: kapakta griye çekilir (beyaz dikdörtgen = papaz yakası okuması, 27 Kasım)
    fill(F([[-14, -712], [24, -712], [26, -682], [-16, -682]]), o.arka ? .03 : (o.yuzTon ?? .04), { th: PI / 2, id: 5 });
    GR.restore();
    // baş
    { const [bx, by] = W(6, -702); GR.save(); GR.frame(bx, by, (eg + (o.bas || 0)) * yon, yon, k);
      if (o.arka) {
        fill(Sm([[-30, -6], [-38, -48], [-30, -92], [0, -116], [36, -112], [58, -84], [62, -44], [52, -12], [22, -2]]), .02, { th: .9, id: 6 });
        if (kn != null) { fill(Sm([[52, -50], [62, -44], [60, -22], [50, -12], [46, -34]]), Math.max(kn, .55), { th: PI / 2, id: 5 }); vurus(10, -110, 50, -86, 4, kn * .9); vurus(-8, -104, 30, -96, 3, kn * .7); }
      } else {
        // profil: alın, burun, dudak, çene konturu (düz siyah), saç kütlesi; kenar ışığı profil çizgisinde
        const prof = [[-34, -10], [-40, -58], [-26, -100], [8, -116], [38, -104], [50, -82], [54, -64], [66, -46], [56, -40], [58, -30], [54, -24], [56, -14], [44, -4], [22, 4], [-6, 0]];
        fill(Sm(prof), o.yuzTon ?? .03, { th: .9, id: 5 });
        fill(Sm([[-38, -26], [-46, -70], [-28, -112], [10, -124], [44, -110], [48, -92], [18, -100], [-10, -88], [-22, -50]]), .02, { th: .9, id: 6 });
        if (kn != null) serit([[50, -82], [54, -64], [66, -46], [56, -40], [58, -30], [54, -24], [56, -14], [44, -4]], 4, kn, 1);
        if (o.biyik) fill(F([[42, -30], [60, -34], [58, -26], [40, -24]]), .02, { th: 0, id: 6 });
        if (o.sakal) fill(Sm([[-6, -14], [52, -20], [56, 6], [30, 22], [0, 14]]), .02, { th: .9, id: 6 });
        if (o.sigara) fill(F([[58, -26], [92, -32], [93, -27], [59, -21]]), .92, { th: 0, id: 5 });
      }
      if (o.sapka) { fill(F([[-46, -98], [70, -98], [66, -108], [56, -110], [52, -198], [-24, -198], [-28, -110], [-42, -108]]), .02, { th: PI / 2, id: 9 }); if (kn != null) vurus(50 * ks, -190, 46 * ks, -112, 4, kn); }
      GR.restore(); }
    // ön kol
    const kno = o.kolOn || { a: .05, b: .08 };
    let uc; { const [sx, sy] = W(56, -630); GR.save(); GR.frame(sx, sy, eg * yon, yon, k); uc = kol(kno.a + sw * .8, kno.b, { ton, kenar: kn, kYan: ks, elTon: o.elTon }); GR.restore();
      uc = [sx + yon * k * (uc[0] * ce - uc[1] * se), sy + k * (uc[0] * se + uc[1] * ce)]; }
    return { el: uc, bas: W(10, -770) };
  }
  // KADIN (Sibyl, Juliet kılığı): dar korse, bel, kıvrımlı uzun etek; açık elbise koyu zeminin önünde (çizgili), koyu saç topuz
  function kadin(o) {
    const h = o.h || 560, k = h / 700, yon = o.yon || 1, el = o.elbise ?? .82;
    GR.save(); GR.frame(o.x, o.y, o.egim || 0, yon, k);
    const et = o.etek ?? 0;
    // etek: bel (−420) dar, yere doğru açılır; kıvrımlar bend taramayla
    fill(Sm([[-34, -424], [36, -424], [58, -330], [96 + et, -150], [130 + et, 0], [-124 - et, 0], [-90 - et, -150], [-54, -330]]), el, { type: 'bend', ox: 0, oy: -420, a: PI / 2, k: .0008, id: 9 });
    for (const [x0, x1] of [[-10, -40], [14, 40], [-30, -90], [30, 96]]) vurus(x0, -400, x1 + et * Math.sign(x1), -10, 6, .25);
    // korse ve göğüs, omuzlar, kısa kollu üst
    fill(Sm([[-34, -424], [36, -424], [40, -470], [46, -520], [30, -548], [-28, -548], [-44, -520], [-40, -470]]), el - .08, { th: 0, id: 9 });
    fill(F([[-36, -432], [38, -432], [38, -420], [-36, -420]]), .3, { th: 0, id: 9 });   // kemer
    // kol (yakın)
    const ka = o.kol || { a: .25, b: .6 };
    GR.save(); GR.frame(o.x + yon * k * 30, o.y - k * 540, o.egim || 0, yon, k); kol(ka.a, ka.b, { ton: el - .1, w: 30, elTon: .75 }); GR.restore();
    // boyun ve baş: profil, açık ten (ışıkta), koyu saç topuz
    fill(F([[-8, -582], [14, -582], [16, -544], [-10, -544]]), .62, { th: PI / 2, id: 5 });
    GR.save(); GR.frame(o.x + yon * k * 4, o.y - k * 580, (o.egim || 0) + (o.bas || 0) * yon, yon, k);
    fill(Sm([[-24, -6], [-30, -46], [-18, -82], [8, -94], [32, -84], [40, -64], [46, -48], [40, -42], [42, -32], [36, -24], [34, -8], [14, 2], [-6, 0]]), o.yuzTon ?? .66, { th: .9, id: 5 });
    fill(Sm([[-36, 0], [-40, -50], [-28, -90], [6, -104], [36, -92], [30, -76], [6, -82], [-14, -70], [-20, -30], [-18, 6]]), .03, { th: .9, id: 6 });
    fill(Sm([[-56, -76], [-40, -96], [-22, -84], [-30, -62], [-50, -58]]), .03, { th: .9, id: 6 });   // topuz
    GR.restore();
    GR.restore();
  }
  return { adam, kadin, F, Sm, fill, vurus };
})();
