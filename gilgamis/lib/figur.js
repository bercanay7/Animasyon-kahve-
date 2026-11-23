// Kabartma figürleri (Mezopotamya geleneği: profil gövde, omuzlar önden, önden göz). ORTAK DOSYA: başkan.
// fig(R, x, y, s, o): ayak tabanı (x, y), boy s (dünya px). o:
//   tip: 'gilgamis' | 'enkidu' | 'samhat' | 'siduri' | 'utna' | 'ursa' | 'adam' | 'kadin' | 'cocuk'
//   f: +1 sağa bakar, -1 sola     z: kabartma yüksekliği (0..1, varsayılan .72)
//   eğilme: gövde açısı (rad, + öne)      bas: baş açısı (+ öne eğik)
//   kol: [[omuz, dirsek], [omuz, dirsek]] yakın ve uzak kol (rad; 0 aşağı sarkık, + öne)
//   bacak: [[kalça, diz], [kalça, diz]] yakın ve uzak bacak (0 dik, + öne)
//   otur: 0..1 (oturma; kalça ve dizler bükülür)   yat: true → yatan figür (döndürülmüş)
//   giysi: 'etek' | 'cubbe' | 'pecek' | 'post' (aslan postu)   el: {yakin: fn(ctxlar, x, y), uzak: …} ele tutulan nesne çizimi
'use strict';
const FIG = {};
(() => {
  // yardımcı: üç tuvale aynı yolu farklı stillerle uygula
  const P = (R, f) => { for (const c of [R.b, R.d, R.m]) { c.save(); f(c); c.restore(); } };
  // uzuv: kalınlığı değişen kapsül (a → b, wa → wb), tabana yükseklik z, ayrıntıya kontur oyuğu
  function uzuv(R, a, b, wa, wb, z, kontur = .5, acik = false) {
    const dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
    const path = c => { c.beginPath(); c.moveTo(a[0] + nx * wa / 2, a[1] + ny * wa / 2); c.lineTo(b[0] + nx * wb / 2, b[1] + ny * wb / 2); c.arc(b[0], b[1], wb / 2, Math.atan2(ny, nx), Math.atan2(ny, nx) + PI); c.lineTo(a[0] - nx * wa / 2, a[1] - ny * wa / 2); c.arc(a[0], a[1], wa / 2, Math.atan2(-ny, -nx), Math.atan2(-ny, -nx) + PI); c.closePath(); };
    R.b.fillStyle = gv(z); path(R.b); R.b.fill();
    R.d.fillStyle = R.T.kilPd; path(R.d); R.d.fill();
    R.m.fillStyle = R.renk || R.T.kil; path(R.m); R.m.fill();
    if (kontur) { R.d.strokeStyle = dv(-kontur); R.d.lineWidth = Math.max(1.2, wa * .07);
      if (acik) { const c = R.d; c.beginPath(); c.moveTo(a[0] + nx * wa / 2, a[1] + ny * wa / 2); c.lineTo(b[0] + nx * wb / 2, b[1] + ny * wb / 2); c.arc(b[0], b[1], wb / 2, Math.atan2(ny, nx), Math.atan2(ny, nx) + PI); c.lineTo(a[0] - nx * wa / 2, a[1] - ny * wa / 2); c.stroke(); }
      else { path(R.d); R.d.stroke(); } }
  }
  function sekil(R, pts, z, kontur = .55, renk = null, smoothK = 1) {
    const path = c => { c.beginPath(); spline(c, pts, true, smoothK); };
    R.b.fillStyle = gv(z); path(R.b); R.b.fill();
    R.d.fillStyle = R.T.kilPd; path(R.d); R.d.fill();
    R.m.fillStyle = renk || R.renk || R.T.kil; path(R.m); R.m.fill();
    if (kontur) { R.d.strokeStyle = dv(-kontur); R.d.lineWidth = R._lw; path(R.d); R.d.stroke(); }
  }
  function cizgi(R, pts, w, v) { const c = R.d; c.strokeStyle = dv(v); c.lineWidth = w; c.beginPath(); c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.stroke(); }
  const pol = (o, ang, r) => [o[0] + Math.sin(ang) * r, o[1] + Math.cos(ang) * r];
  // el: (x, y) bilek; a: yön (rad, parmakların gösterdiği yön); s: el boyu; kapali: tutan el (parmaklar kıvrık)
  FIG.el = (R, x, y, s, a, o = {}) => {
    const z = o.z ?? .86, ca = Math.cos(a), sa = Math.sin(a), T = (u, v) => [x + u * ca - v * sa, y + u * sa + v * ca];
    sekil(R, [T(0, -s * .22), T(s * .45, -s * .26), T(s * .5, s * .2), T(0, s * .22)], z, .5, null, .7);
    for (let k = 0; k < 4; k++) { const v = -s * .2 + k * s * .13, L = (o.kapali ? .25 : .5) * (k === 0 || k === 3 ? .85 : 1); uzuv(R, T(s * .45, v), T(s * (.45 + L), v + (o.kapali ? s * .12 : 0)), s * .12, s * .1, z + .02, .45, true); }
    uzuv(R, T(s * .12, s * .2), T(s * .38, s * .42), s * .13, s * .1, z + .03, .45, true);
  };
  FIG.uzuv = uzuv; FIG.sekil = sekil; FIG.cizgi = cizgi; FIG.pol = pol;

  // Baş (profil, sağa bakar; birim: boy). c: merkez, s: ölçek, tip
  function bas(R, c, s, tip, z, a = 0, o = {}) {
    const k = s; const T = (x, y) => { const ca = Math.cos(a), sa = Math.sin(a); return [c[0] + (x * ca - y * sa) * k, c[1] + (x * sa + y * ca) * k]; };
    const kadin = tip === 'samhat' || tip === 'siduri' || tip === 'kadin', cocuk = tip === 'cocuk';
    // saç (başın arkası): kabartmada başın gerisinde
    if (tip === 'enkidu') sekil(R, [T(-.03, -.07), T(-.075, -.03), T(-.1, .06), T(-.11, .16), T(-.07, .2), T(-.035, .12), T(-.02, .03)], z - .03);
    else if (kadin) sekil(R, [T(-.02, -.07), T(-.07, -.03), T(-.085, .05), T(-.09, .15), T(-.06, .17), T(-.03, .08), T(-.01, .02)], z - .03);
    else if (!cocuk) sekil(R, [T(-.03, -.03), T(-.075, .0), T(-.08, .05), T(-.05, .07), T(-.02, .04)], z - .02); // topuz
    // yüz ve kafatası
    const yuz = [T(-.055, -.02), T(-.04, -.065), T(0, -.075), T(.04, -.06), T(.052, -.03), T(.07, .0), T(.05, .012), T(.054, .03), T(.044, .045), T(.04, .06), T(.0, .07), T(-.045, .045)];
    sekil(R, yuz, z, .55);
    // sakal
    const sakal = { gilgamis: [T(.035, .035), T(.04, .07), T(.03, .15), T(-.035, .15), T(-.04, .05), T(0, .055)],
      enkidu: [T(.035, .035), T(.045, .08), T(.02, .17), T(-.03, .16), T(-.04, .05)],
      utna: [T(.035, .035), T(.042, .09), T(.025, .25), T(-.02, .26), T(-.04, .06)],
      ursa: [T(.035, .035), T(.04, .07), T(.025, .12), T(-.03, .11), T(-.04, .05)], adam: [T(.035, .035), T(.04, .07), T(.03, .12), T(-.03, .11), T(-.04, .05)] }[tip];
    if (sakal && !o.sakalsiz) {
      sekil(R, sakal, z + .02, .5);
      // bukleler: sıra sıra küçük oyuk halkalar (Gılgamış), dalgalı çizgiler (Enkidu, Utnapiştim)
      const rows = tip === 'utna' ? 7 : tip === 'gilgamis' ? 4 : 5;
      for (let r = 0; r < rows; r++) for (let q = 0; q < 3; q++) {
        const p = T(-.025 + q * .025, .06 + r * (tip === 'utna' ? .028 : .022));
        if (tip === 'gilgamis') { const pq = T(-.03 + q * .024 + (r % 2) * .012, .055 + r * .023); R.d.strokeStyle = dv(-.7); R.d.lineWidth = Math.max(1, s * .004); R.d.beginPath(); R.d.arc(pq[0], pq[1], s * .007, a + .6, a + .6 + PI * 1.5); R.d.stroke(); }
        else cizgi(R, [p, T(-.02 + q * .025, .07 + r * .022), T(-.025 + q * .025, .08 + r * .022)], Math.max(1, s * .004), -.6);
      }
    }
    // saç çizgileri / alın bandı
    if (tip === 'gilgamis' || tip === 'ursa' || tip === 'adam') cizgi(R, [T(-.055, -.035), T(-.01, -.06), T(.03, -.055)], Math.max(1.5, s * .008), .7);
    if (tip === 'enkidu') for (let q = 0; q < 5; q++) cizgi(R, [T(-.04 - q * .012, -.05 + q * .02), T(-.07 - q * .008, .05 + q * .02), T(-.065 - q * .006, .14)], Math.max(1, s * .004), -.55);
    if (kadin) { cizgi(R, [T(-.05, -.04), T(-.01, -.064), T(.03, -.055)], Math.max(1.5, s * .007), .7); for (let q = 0; q < 4; q++) cizgi(R, [T(-.03 - q * .012, -.04), T(-.06 - q * .006, .06), T(-.06 - q * .004, .15)], Math.max(1, s * .004), -.5); }
    // önden göz: badem, büyük
    const g = T(.022, -.018);
    R.d.save(); R.d.translate(g[0], g[1]); R.d.rotate(a);
    R.d.strokeStyle = dv(-.85); R.d.lineWidth = Math.max(1.2, s * .005);
    R.d.beginPath(); R.d.ellipse(0, 0, s * .017, s * .008, 0, 0, TAU); R.d.stroke();
    R.d.fillStyle = dv(-.9); R.d.beginPath(); R.d.arc(s * .003, 0, s * .0045, 0, TAU); R.d.fill();
    if (o.kapali) { R.d.strokeStyle = dv(-.8); R.d.beginPath(); R.d.moveTo(-s * .017, 0); R.d.lineTo(s * .017, 0); R.d.stroke(); }
    // kaş
    R.d.strokeStyle = dv(.6); R.d.lineWidth = Math.max(1.5, s * .006); R.d.beginPath(); R.d.moveTo(-s * .02, -s * .016); R.d.quadraticCurveTo(s * .005, -s * .026, s * .03, -s * .014); R.d.stroke();
    R.d.restore();
    // kulak
    const ku = T(-.022, .0); R.d.strokeStyle = dv(-.5); R.d.lineWidth = Math.max(1, s * .004); R.d.beginPath(); R.d.ellipse(ku[0], ku[1], s * .008, s * .014, a, 0, TAU); R.d.stroke();
    if (o.gozyasi) { const p = T(.03, .01 + o.gozyasi * .05); R.b.fillStyle = gv(z + .06); R.b.beginPath(); R.b.arc(p[0], p[1], s * .005, 0, TAU); R.b.fill(); }
  }
  FIG.bas = bas;


  // Yatan figür (sırtüstü; baş sağda, yüz yukarı). (x, y): yatağın üstünde topukların yeri; L: boy. o: {tip, z, kapali, ortu (0..1 örtü yüzü kapatır)}
  FIG.yatan = function (R, x, y, L, o = {}) {
    const tip = o.tip || 'enkidu', z = o.z ?? .74; R._lw = Math.max(1.2, L * .0045);
    // bacaklar
    uzuv(R, [x + L * .04, y - L * .03], [x + L * .27, y - L * .045], L * .045, L * .06, z - .06);
    uzuv(R, [x + L * .27, y - L * .045], [x + L * .5, y - L * .05], L * .07, L * .08, z - .04);
    sekil(R, [[x, y - L * .02], [x + L * .03, y - L * .1], [x + L * .06, y - L * .06]], z - .04, .5); // ayak
    // etek/peçe
    const ek = [[x + L * .42, y - L * .01], [x + L * .43, y - L * .1], [x + L * .58, y - L * .11], [x + L * .6, y - L * .01]];
    R.b.fillStyle = gv(z + .02); R.b.beginPath(); poly(R.b, ek); R.b.fill(); R.m.fillStyle = R.T.kil; R.m.beginPath(); poly(R.m, ek); R.m.fill();
    R.d.fillStyle = R.T.kilPd; R.d.beginPath(); poly(R.d, ek); R.d.fill();
    for (let q = 1; q < 6; q++) cizgi(R, [[x + L * (.43 + q * .025), y - L * .1], [x + L * (.43 + q * .025), y - L * .01]], Math.max(1, L * .003), -.45);
    // gövde
    sekil(R, [[x + L * .56, y - L * .005], [x + L * .57, y - L * .1], [x + L * .7, y - L * .12], [x + L * .79, y - L * .13], [x + L * .8, y - L * .005]], z, .55, null, .8);
    if (tip === 'enkidu') for (let q = 0; q < 18; q++) { const u = hash(q * 9.1), v = hash(q * 3.3); const p = [x + L * (.6 + u * .18), y - L * (.02 + v * .09)]; cizgi(R, [p, [p[0] + L * .008, p[1] + L * .006]], Math.max(1, L * .003), -.55); }
    // kol (gövde boyunca)
    uzuv(R, [x + L * .77, y - L * .085], [x + L * .63, y - L * .075], L * .05, L * .045, z + .06);
    uzuv(R, [x + L * .63, y - L * .075], [x + L * .5, y - L * .07], L * .045, L * .035, z + .06);
    R.b.fillStyle = gv(z + .07); R.b.beginPath(); R.b.arc(x + L * .49, y - L * .07, L * .025, 0, TAU); R.b.fill();
    // yastık ve baş (yüz yukarı)
    sekil(R, [[x + L * .82, y], [x + L * .83, y - L * .08], [x + L * .98, y - L * .08], [x + L * .99, y]], z - .1, .5);
    if ((o.ortu ?? 0) < 1) FIG.bas(R, [x + L * .885, y - L * .115], L * 1.1, tip, z + .02, -1.25, { kapali: o.kapali !== false, sakalsiz: true });
    if (o.ortu) { // gelin gibi örtü: baştan göğse, yatağın kenarından sarkar, saçaklı
      const k = o.ortu, x0 = x + L * (1.0 - .26 * k), x1 = x + L * 1.0;
      const pts = [[x0, y + L * .045], [x0 + L * .01, y - L * .1], [x0 + L * .06, y - L * .14], [x1 - L * .05, y - L * .17], [x1, y - L * .12], [x1 + L * .01, y + L * .045]];
      R.b.fillStyle = gv(z + .1); R.b.beginPath(); poly(R.b, pts); R.b.fill(); R.m.fillStyle = R.T.kil; R.m.beginPath(); poly(R.m, pts); R.m.fill(); R.d.fillStyle = R.T.kilPd; R.d.beginPath(); poly(R.d, pts); R.d.fill();
      R.d.strokeStyle = dv(-.5); R.d.lineWidth = R._lw; R.d.beginPath(); poly(R.d, pts); R.d.stroke();
      for (let q = 1; q < 5; q++) cizgi(R, [[x0 + (x1 - x0) * q / 5, y - L * (.12 + .03 * Math.sin(q))], [x0 + (x1 - x0) * q / 5 + L * .01, y + L * .03]], Math.max(1.2, L * .0025), -.35);
      for (let q = 0; q <= 14; q++) { const xx = lerp(x0, x1 + L * .01, q / 14); cizgi(R, [[xx, y + L * .045], [xx, y + L * .065]], Math.max(1.2, L * .003), .5); }
    }
  };

  // Figür
  FIG.fig = function (R, x, y, s, o = {}) {
    const tip = o.tip || 'adam', f = o.f ?? 1, z0 = o.z ?? .78, S = s;
    R._lw = Math.max(1.2, s * .0045);
    const kadin = tip === 'samhat' || tip === 'siduri' || tip === 'kadin';
    for (const c of [R.b, R.d, R.m]) { c.save(); c.translate(x, y); if (o.don) c.rotate(o.don); c.scale(f, 1); }
    const eg = o.egilme || 0, ot = clamp(o.otur || 0);
    const UY = S * .24, AL = S * .23;           // uyluk, baldır
    const kalca = [ot * -S * .02, -S * (.48 - ot * .22)];
    // gövde çerçevesi: kalçada döner (x ileri, y yukarı; S birimi)
    const TF = (u, v) => [kalca[0] + (u * Math.cos(eg) + v * Math.sin(eg)) * S, kalca[1] + (u * Math.sin(eg) - v * Math.cos(eg)) * S];
    const kolC = (k, sh, L1 = .15, L2 = .14) => { const dir = pol(sh, k[0] + eg * .3, S * L1); const el = pol(dir, k[0] + k[1] + eg * .3, S * L2); return [dir, el]; };
    // bacak: [kalça açısı, diz açısı]; oturuşta uyluk öne yatay, baldır dik
    const bacak = o.bacak || [[.12, -.06], [-.1, .02]], kol = o.kol || [[.12, .35], [-.08, .2]];
    const ayak = (b, dx) => { const h0 = lerp(b[0], PI / 2 - .05, ot), d0 = lerp(b[1], -(PI / 2 - .05) + b[0] * .2, ot);
      const kc = [kalca[0] + dx, kalca[1]], diz = pol(kc, h0, UY), ay = pol(diz, h0 + d0, AL); return [kc, diz, ay]; };
    const zL = z0 - .14, zN = z0 + .05;
    const bacakCiz = (kc, diz, ay, z) => {
      uzuv(R, kc, diz, S * .1, S * .072, z, .5, true);
      // baldır kası (Asur kabartması gibi belirgin)
      const m = [lerp(diz[0], ay[0], .35), lerp(diz[1], ay[1], .35)];
      uzuv(R, diz, m, S * .072, S * .074, z, .5, true); uzuv(R, m, ay, S * .074, S * .045, z, 0);
      uzuv(R, [ay[0] - S * .01, ay[1] - S * .012], [ay[0] + S * .07, ay[1] + S * .004], S * .035, S * .024, z);
    };
    const giysi = o.giysi || (kadin || tip === 'utna' ? 'cubbe' : tip === 'enkidu' ? 'pecek' : 'etek');
    // --- uzak bacak ve kol
    const [kU, dU, aU] = ayak(bacak[1], -S * .02);
    if (giysi !== 'cubbe' || ot > .3) bacakCiz(kU, dU, aU, zL);
    const omU = TF(-.05, .29), [dkU, elU] = kolC(kol[1], omU);
    uzuv(R, omU, dkU, S * .07, S * .058, zL + .03, .5, true); uzuv(R, dkU, elU, S * .058, S * .045, zL + .03, .5, true);
    R.b.fillStyle = gv(zL + .04); R.b.beginPath(); R.b.arc(elU[0], elU[1], S * .03, 0, TAU); R.b.fill();
    if (o.el && o.el.uzak) o.el.uzak(R, elU, S);
    // --- gövde
    const gv0 = [TF(-.08, -.02), TF(-.065, .1), TF(-.085, .21), TF(-.115, .29), TF(-.075, .335), TF(-.025, .35), TF(.035, .35), TF(.085, .335), TF(.135, .29), TF(.11, .2), TF(.065, .1), TF(.085, -.02)];
    sekil(R, gv0, z0, .55, null, .8);
    if (tip === 'enkidu') for (let q = 0; q < 34; q++) { const u = -.06 + hash(q * 9.1 + 2) * .15, v = .02 + hash(q * 3.7 + (o.tohum || 0)) * .3; const p = TF(u, v); cizgi(R, [p, [p[0] + S * .01, p[1] + S * .014]], Math.max(1, S * .0035), -.6); }
    if (tip === 'gilgamis' || tip === 'ursa' || tip === 'adam') cizgi(R, [TF(-.07, .24), TF(.12, .26)], Math.max(1.2, S * .004), -.35); // göğüs çizgisi
    // --- giysi (dünya dikeyinde; kalçadan aşağı)
    const bel = TF(0, .07);
    if (giysi === 'cubbe' || giysi === 'etek' || giysi === 'pecek' || giysi === 'post') {
      const boy = giysi === 'cubbe' ? -bel[1] - S * .012 : giysi === 'pecek' ? S * .17 : S * .3;
      const w0 = S * .085, w1 = giysi === 'cubbe' ? S * .14 : giysi === 'pecek' ? S * .1 : S * .12;
      let pts;
      if (ot > .3 && giysi !== 'pecek') { // oturuşta etek uyluğun üstünden dizlere örter
        const [, dN0] = ayak(bacak[0], S * .02);
        pts = [[bel[0] - w0, bel[1]], [bel[0] + w0, bel[1]], [dN0[0] + S * .02, dN0[1] - S * .05], [dN0[0] + S * .03, dN0[1] + S * (giysi === 'cubbe' ? .2 : .08)], [kalca[0] - S * .1, kalca[1] + S * .06]];
      } else pts = [[bel[0] - w0, bel[1]], [bel[0] + w0, bel[1]], [bel[0] + w1 + S * .01, bel[1] + boy], [bel[0] - w1, bel[1] + boy]];
      R.b.fillStyle = gv(z0 + .02); R.b.beginPath(); poly(R.b, pts); R.b.fill();
      R.d.fillStyle = R.T.kilPd; R.d.beginPath(); poly(R.d, pts); R.d.fill();
      R.m.fillStyle = R.renk || R.T.kil; R.m.beginPath(); poly(R.m, pts); R.m.fill();
      R.d.strokeStyle = dv(-.55); R.d.lineWidth = R._lw; R.d.beginPath(); poly(R.d, pts); R.d.stroke();
      const n = giysi === 'cubbe' ? 10 : 7, bot = [pts[pts.length - 1], pts[pts.length - 2]];
      for (let q = 1; q < n; q++) { const u = q / n; cizgi(R, [[lerp(pts[0][0], pts[1][0], u), pts[0][1] + S * .03], [lerp(bot[0][0], bot[1][0], u), lerp(bot[0][1], bot[1][1], u) - S * .015]], Math.max(1, S * .0035), -.45); }
      for (let q = 0; q <= 16; q++) { const u = q / 16, p = [lerp(bot[0][0], bot[1][0], u), lerp(bot[0][1], bot[1][1], u)]; cizgi(R, [p, [p[0], p[1] + S * .025]], Math.max(1, S * .004), .6); }
      cizgi(R, [[pts[0][0], pts[0][1] + S * .014], [pts[1][0], pts[1][1] + S * .014]], Math.max(1.5, S * .009), .7);
    }
    if (giysi === 'post') { const pp = [TF(-.08, .33), TF(-.13, .25), TF(-.14, .05), TF(-.17, -.12), TF(-.12, -.06), TF(-.1, -.14), TF(-.07, -.02), TF(-.05, .2)]; sekil(R, pp, z0 + .04, .5, null, .6); for (let q = 0; q < 9; q++) { const p = TF(-.13 + hash(q * 3) * .05, .25 - q * .035); cizgi(R, [p, [p[0] - S * .012, p[1] + S * .01]], Math.max(1, S * .0035), -.5); } const pc = TF(-.14, -.13), pc2 = TF(-.1, -.15); for (const pw of [pc, pc2]) { R.b.fillStyle = gv(z0 + .05); R.b.beginPath(); R.b.arc(pw[0], pw[1], S * .018, 0, TAU); R.b.fill(); for (let k = -1; k <= 1; k++) cizgi(R, [[pw[0] + k * S * .009, pw[1] + S * .008], [pw[0] + k * S * .011, pw[1] + S * .02]], Math.max(1, S * .003), -.6); } }
    if (giysi === 'cubbe') cizgi(R, [TF(.11, .29), TF(-.06, .05)], Math.max(1.5, S * .007), .6);
    // --- baş
    bas(R, TF(.015, .43), S * 1.18, tip, z0 + .03, (o.bas || 0) + eg * .6, o.basO || {});
    // --- yakın bacak
    const [kN, dN, aN] = ayak(bacak[0], S * .02);
    if (giysi !== 'cubbe' || ot > .3) bacakCiz(kN, dN, aN, zN);
    else uzuv(R, [aN[0] + S * .01, aN[1] - S * .03], [aN[0] + S * .07, aN[1] + S * .004], S * .035, S * .024, zN);
    // --- yakın kol
    const omN = TF(.07, .29), [dkN, elN] = kolC(kol[0], omN);
    uzuv(R, omN, dkN, S * .078, S * .062, zN + .04, .5, true); uzuv(R, dkN, elN, S * .062, S * .048, zN + .04, .5, true);
    R.b.fillStyle = gv(zN + .05); R.b.beginPath(); R.b.arc(elN[0], elN[1], S * .032, 0, TAU); R.b.fill();
    const bl = [lerp(dkN[0], elN[0], .8), lerp(dkN[1], elN[1], .8)], ang = Math.atan2(elN[1] - dkN[1], elN[0] - dkN[0]) + PI / 2;
    cizgi(R, [[bl[0] - Math.cos(ang) * S * .028, bl[1] - Math.sin(ang) * S * .028], [bl[0] + Math.cos(ang) * S * .028, bl[1] + Math.sin(ang) * S * .028]], Math.max(1.5, S * .008), .6); // bilezik
    if (o.el && o.el.yakin) o.el.yakin(R, elN, S);
    for (const c of [R.b, R.d, R.m]) c.restore();
    const W2 = p => { const c = Math.cos(o.don || 0), sn = Math.sin(o.don || 0), px = p[0] * f; return [x + px * c - p[1] * sn, y + px * sn + p[1] * c]; };
    return { bas: W2(TF(.015, .43)), elN: W2(elN), elU: W2(elU), omuz: W2(TF(0, .3)), kalca: W2(kalca), S };
  };
})();
