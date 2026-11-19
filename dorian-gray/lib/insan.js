// Viktorya figürleri (gravür dili): koyu siluet + kenar ışığı. Klasik betik; GR (milton/lib/gravur.js) üstüne.
// Kural: Dorian'ın yüzü dünyada görünmez (arka/¾ arka ya da gölge). Basil ve Henry profil ya da ¾ olabilir ama yüz ayrıntısı yok.
// Koordinat: ayak tabanı orta (x, y); h = boy (baş tepesinden ayağa, px). yon = +1 sağa bakar, −1 sola.
'use strict';
const INSAN = (() => {
  const PI = Math.PI;
  const F = (pts) => { const p = new Path2D(); p.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) p.lineTo(pts[i][0], pts[i][1]); p.closePath(); return p; };
  const Sm = (pts) => { const p = new Path2D(), n = pts.length; p.moveTo(pts[0][0], pts[0][1]);
    for (let i = 0; i < n; i++) { const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      p.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]); }
    p.closePath(); return p; };
  const fill = (p, ton, h) => GR.fill(p, GR.tone(ton), h || { th: PI / 2, id: 9 });
  // kol: omuzdan (0,0), açı a (0 = aşağı, + = ileri/yüzün yönü), dirsek bükümü b; boy L; kalınlık w
  function kol(L, w, a, b, ton, el = .55, elTon = null) {
    const ux = Math.sin(a), uy = Math.cos(a), ex = ux * L * .52, ey = uy * L * .52;
    const a2 = a + b, vx = Math.sin(a2), vy = Math.cos(a2), hx = ex + vx * L * .48, hy = ey + vy * L * .48;
    const n = (x, y) => [-y, x];
    const [n1x, n1y] = n(ux, uy), [n2x, n2y] = n(vx, vy);
    const p = Sm([[n1x * w * .5, n1y * w * .5], [ex + n1x * w * .45, ey + n1y * w * .45], [hx + n2x * w * .38, hy + n2y * w * .38], [hx - n2x * w * .38, hy - n2y * w * .38], [ex - n1x * w * .45, ey - n1y * w * .45], [-n1x * w * .5, -n1y * w * .5]]);
    fill(p, ton);
    if (elTon != null) { const e = new Path2D(); e.ellipse(hx + vx * w * .35, hy + vy * w * .35, w * .36, w * .5, -a2, 0, PI * 2); fill(e, elTon, { th: 0, id: 5 }); }
    return [hx + vx * w * .5, hy + vy * w * .5];   // el ucu (yerel)
  }
  // ADAM: o = { x, y, h, yon, arka (sırtı dönük), sapka, palto (0..1 boy), kolOn/kolArka {a, b}, bas (baş eğimi), adim (yürüyüş fazı 0..1, null = duruş),
  //   ton (siluet), kenar (kenar ışığı tonu, null = yok), kenarYan (+1 sağ / −1 sol), biyik, sigara, sakal, yaka (beyaz yaka görünür), saç (dağınık) }
  function adam(o) {
    const h = o.h || 600, k = h / 760, yon = o.yon || 1, ton = o.ton ?? .06;
    GR.save(); GR.frame(o.x, o.y, o.egim || 0, yon, k);
    // bacaklar (yürüyüşte salınım)
    const ad = o.adim, sw = ad == null ? 0 : Math.sin(ad * 2 * PI) * .22;
    for (const [s, dx] of [[1, 18], [-1, -22]]) {
      const a = sw * s, lx = dx, top = -330;
      const fx = lx + Math.sin(a) * 330, fy = top + Math.cos(a) * 330;
      fill(F([[lx - 26, top], [lx + 26, top], [fx + 20, fy - 8], [fx - 18, fy - 8]]), ton - .01);
      fill(Sm([[fx - 22, fy - 14], [fx + 26, fy - 14], [fx + 44, fy + 2], [fx - 22, fy + 3]]), .02, { th: 0, id: 9 });
    }
    // redingot: omuz, bel, dize kadar etek; palto uzunluğu
    const et = -282 + (1 - (o.palto ?? 1)) * 150;
    fill(Sm([[-70, -628], [-28, -656], [36, -656], [80, -628], [90, -560], [82, -470], [86, -380], [94, et], [-84, et], [-76, -380], [-72, -470], [-80, -560]]), ton);
    if (!o.arka) fill(F([[-6, -650], [10, -650], [26, -470], [2, -420], [-20, -470]]), ton + .06);   // yaka açıklığı (önden)
    // kenar ışığı (lamba/pencere yönü)
    if (o.kenar != null) { const s = o.kenarYan ?? 1; const xs = s > 0 ? [78, 90, 82, 86, 94] : [-70, -80, -72, -76, -84];
      const ys = [-626, -560, -470, -380, et];
      const pts = xs.map((x, i) => [x, ys[i]]), ins = pts.slice().reverse().map(([x, y]) => [x - s * 10, y]);
      fill(F([...pts, ...ins]), o.kenar); }
    // arka kol (uzak)
    const ka = o.kolArka || { a: -.08, b: .1 };
    GR.save(); GR.frame(o.x + yon * k * (-52), o.y - k * 600, (o.egim || 0), yon, k); kol(300, 52, ka.a, ka.b, ton - .02, .55, o.elTon ?? null); GR.restore();
    // yaka (beyaz) ve ense / boyun
    if (o.yaka !== false) fill(F([[-24, -676], [30, -676], [36, -650], [-28, -650]]), o.arka ? .86 : .9, { th: 0, id: 5 });
    fill(F([[-16, -704], [26, -704], [28, -674], [-18, -674]]), o.arka ? .28 : .5, { th: PI / 2, id: 5 });
    // baş
    GR.save(); GR.frame(o.x + yon * k * 6, o.y - k * 690, (o.bas || 0) * yon, yon, k);
    if (o.arka) {
      fill(Sm([[-30, -14], [-38, -54], [-30, -96], [2, -118], [38, -114], [60, -86], [62, -48], [52, -18], [24, -8]]), .1, { th: .9, id: 6 });
      if (o.kenar != null) fill(Sm([[54, -58], [64, -50], [62, -26], [52, -16], [48, -38]]), Math.max(o.kenar, .5), { th: PI / 2, id: 5 });
    } else {
      // profil (yüz ayrıntısı yok: koyu siluet, yalnız kenar çizgisi)
      fill(Sm([[-34, -14], [-42, -60], [-30, -100], [6, -118], [40, -104], [56, -76], [64, -54], [58, -44], [62, -34], [54, -24], [52, -8], [30, 6], [-8, 0]]), o.yuzTon ?? .12, { th: .9, id: 5 });
      fill(Sm([[-36, -30], [-44, -72], [-28, -108], [8, -122], [44, -108], [50, -88], [20, -94], [-10, -84], [-24, -50]]), .05, { th: .9, id: 6 });   // saç
      if (o.biyik) fill(F([[46, -20], [62, -26], [60, -18], [44, -14]]), .04, { th: 0, id: 6 });
      if (o.sakal) fill(Sm([[0, -10], [52, -16], [56, 8], [30, 22], [4, 14]]), .06, { th: .9, id: 6 });
      if (o.sigara) { fill(F([[62, -18], [96, -24], [97, -19], [63, -13]]), .9, { th: 0, id: 5 }); }
    }
    if (o.sapka) { fill(F([[-46, -96], [70, -96], [66, -108], [56, -110], [52, -196], [-24, -196], [-28, -110], [-42, -108]]), .03, { th: PI / 2, id: 9 }); }
    GR.restore();
    // ön kol (yakın)
    const kn = o.kolOn || { a: .06, b: .1 };
    GR.save(); GR.frame(o.x + yon * k * 62, o.y - k * 606, (o.egim || 0), yon, k);
    const uc = kol(310, 56, kn.a, kn.b, ton + .01, .55, o.elTon ?? null);
    GR.restore();
    GR.restore();
    // ön elin dünya konumu (sigara dumanı, nesne tutma için)
    const c = Math.cos(o.egim || 0), s = Math.sin(o.egim || 0), lx = (62 + uc[0]) * yon * k, ly = (-606 + uc[1]) * k;
    return { el: [o.x + lx * c - ly * s, o.y + lx * s + ly * c], bas: [o.x + yon * k * 10, o.y - k * 760] };
  }
  // KADIN (Sibyl, Juliet kılığı): açık elbise koyu zeminin önünde, çizgili; saç koyu; o.kol {a,b}, o.el (göğüste)
  function kadin(o) {
    const h = o.h || 560, k = h / 700, yon = o.yon || 1;
    GR.save(); GR.frame(o.x, o.y, o.egim || 0, yon, k);
    const et = o.etek ?? 0;
    fill(Sm([[-30, -540], [30, -540], [44, -470], [36, -400], [70 + et, -200], [118 + et, 0], [-112 - et, 0], [-66 - et, -200], [-34, -400], [-42, -470]]), o.elbise ?? .78, { th: PI / 2 - .05, id: 9 });
    fill(Sm([[-30, -540], [30, -540], [42, -480], [-40, -480]]), (o.elbise ?? .78) - .12, { th: 0, id: 9 });
    // kollar
    const ka = o.kol || { a: .3, b: .9 };
    GR.save(); GR.frame(o.x + yon * k * 26, o.y - k * 520, 0, yon, k); kol(250, 34, ka.a, ka.b, (o.elbise ?? .78) - .05, .55, .7); GR.restore();
    // boyun ve baş (profil, koyu saç, ışık yüzün kenarında)
    fill(F([[-10, -580], [14, -580], [16, -536], [-12, -536]]), .55, { th: PI / 2, id: 5 });
    GR.save(); GR.frame(o.x + yon * k * 4, o.y - k * 578, (o.bas || 0) * yon, yon, k);
    fill(Sm([[-26, -8], [-32, -48], [-20, -84], [8, -96], [34, -84], [44, -60], [48, -44], [42, -36], [46, -26], [38, -18], [36, -6], [14, 4], [-8, 2]]), o.yuzTon ?? .6, { th: .9, id: 5 });
    fill(Sm([[-40, 20], [-46, -40], [-30, -92], [8, -106], [38, -92], [34, -70], [8, -78], [-14, -66], [-20, -20], [-26, 30]]), .06, { th: .9, id: 6 });   // uzun koyu saç
    GR.restore();
    GR.restore();
  }
  return { adam, kadin, F, Sm, fill };
})();
