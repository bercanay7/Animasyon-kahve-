// act4: IV · Ateşte dövülen kuşak (E01–E06), 1911–1918. Sahibi: IV. bölüm sahne yapımcısı.
// Palet: kâğıt, is, haki, okra (toprak). Çanakkale'de deniz turkuaz. Kırmızı yalnız cephe hattında ve sancakta.
// Bütün yerel yardımcılar a4_ önekiyle bu dosyadadır; ortak ilkeller (print/people/props/ui/film) değişmez.
'use strict';

// ———————————————————————————————— yardımcılar ————————————————————————————————
// figür zamanı: pozlar ikişer karede değişir (15 fps)
const a4_tf = t => Math.floor(t * 15) / 15;
// durağan katman (kenar payı m ile; kamera kayınca kenar görünmesin). Önbellek baskı geçişinin kayıklığını almaz.
function a4_L(key, draw, m = 0) {
  const b = REG.boost; REG.boost = 1;
  const c = layerCache('a4:' + key, g => { g.translate(m, m); draw(g); }, W + 2 * m, H + 2 * m);
  REG.boost = b;
  return { c, m };
}
// katmanı kamera + paralaks ile bas; baskı geçişinde katman bütünüyle yerine oturur
function a4_put(ctx, L, cm, k = 1, o = {}) {
  ctx.save(); if (cm) cam(ctx, cm, k);
  const b = REG.boost - 1; if (b > 0) ctx.translate(b * 1.4 * k, b * .7 * k);
  if (o.mode) ctx.globalCompositeOperation = o.mode;
  if (o.a != null) ctx.globalAlpha = o.a;
  ctx.drawImage(L.c, -L.m, -L.m, W + 2 * L.m, H + 2 * L.m);
  ctx.restore();
}
// kâğıt rengi tam kare
const a4_full = () => PL([[-200, -200], [W + 200, -200], [W + 200, H + 200], [-200, H + 200]]);
const a4_rect = (x0, y0, x1, y1) => PL([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]);
// gürültülü yatay çizgi (sırt, ufuk): x0..x1 arası n nokta
function a4_ridgePts(x0, x1, y, amp, seed, n = 14, f = 1) {
  const pts = [];
  for (let i = 0; i <= n; i++) { const u = i / n, x = lerp(x0, x1, u); pts.push([x, y + fbm1(u * 3.3 * f + seed * 1.7, seed) * amp]); }
  return pts;
}
// kapalı zemin yolu: sırt noktaları + alt kenar
function a4_groundPath(pts, yb = H + 200) { return SP([...pts, [pts[pts.length - 1][0] + 200, pts[pts.length - 1][1]], [pts[pts.length - 1][0] + 200, yb], [pts[0][0] - 200, yb], [pts[0][0] - 200, pts[0][1]]], true, .6); }
// sırt eğrisinin x'teki yüksekliği (doğrusal ara değer)
function a4_yAt(pts, x) {
  if (x <= pts[0][0]) return pts[0][1];
  for (let i = 1; i < pts.length; i++) if (x <= pts[i][0]) return lerp(pts[i - 1][1], pts[i][1], (x - pts[i - 1][0]) / (pts[i][0] - pts[i - 1][0]));
  return pts[pts.length - 1][1];
}
// kalıbı kaldırma: a = 1 → 0, kalkarken kâğıttan biraz kayar (ters baskı)
function a4_lift(lt, t0, d = .14) { const u = ramp(lt, t0, t0 + d, E.in2); return { a: 1 - u, dx: u * 9, dy: -u * 14 }; }
function a4_plateOff(ctx, name, p, lf, o = {}) { if (lf.a <= 0) return; ctx.save(); ctx.translate(lf.dx, lf.dy); plate(ctx, name, p, { ...o, a: (o.a ?? 1) * lf.a }); ctx.restore(); }

// —— patlama: düz is yıldızı (kâğıt çekirdekli) ——
function a4_starPts(x, y, R, seed, n = 13, inner = .46) {
  const r = rng(seed), pts = [];
  for (let i = 0; i < n * 2; i++) {
    const a = i / (n * 2) * TAU + (r() - .5) * .18, k = i % 2 ? inner * (.8 + r() * .35) : (.7 + r() * .45);
    pts.push([x + Math.cos(a) * R * k, y + Math.sin(a) * R * k * .86]);
  }
  return pts;
}
// k: 0..1 büyüme; çekirdek kâğıt (karenin en parlak yeri)
function a4_burst(ctx, x, y, R, seed, k = 1, o = {}) {
  if (k <= 0) return;
  const Rk = R * k;
  const outer = PL(a4_starPts(x, y, Rk, seed));
  knock(ctx, outer, P.ink); inkFill(ctx, outer);
  if (o.ring !== false) { const mid = PL(a4_starPts(x, y, Rk * .66, seed + 3, 11, .5)); knock(ctx, mid); plate(ctx, 'ochre', mid, { a: .55 }); }
  const core = PL(a4_starPts(x + Rk * .03, y - Rk * .02, Rk * .4, seed + 7, 9, .55));
  knock(ctx, core, '#F7F0DE');
  // kazıma ışın çizgileri (is kütlesinde)
  const r = rng(seed + 11);
  for (let i = 0; i < 9; i++) { const a = r() * TAU, r0 = Rk * .7, r1 = Rk * (.95 + r() * .2); cut(ctx, PL([[x + Math.cos(a) * r0, y + Math.sin(a) * r0 * .86], [x + Math.cos(a) * r1, y + Math.sin(a) * r1 * .86]], false), 2.4, { a: .7 }); }
}
// yarım ton duman bulutu (durağan katmana çizilir): üst üste daireler, içte yoğun
function a4_smokeCloud(g, x, y, R, seed, col = 'ink', dens = .5) {
  const r = rng(seed), blob = new Path2D();
  for (let i = 0; i < 9; i++) { const a = r() * TAU, d = R * .5 * r(); blob.moveTo(x + Math.cos(a) * d + R * .5, y + Math.sin(a) * d * .7); blob.ellipse(x + Math.cos(a) * d, y + Math.sin(a) * d * .7 - R * .2 * r(), R * (.35 + r() * .3), R * (.28 + r() * .22), 0, 0, TAU); }
  radialHT(g, col, x, y, R * .15, R * 1.05, dens, 0, { cell: 11, ang: 45, clip: blob, box: [x - R * 1.3, y - R * 1.1, x + R * 1.3, y + R * .9], sy: .8 });
}

// —— damga asker silueti (is): kabalak, kaput, sırtta çanta, omuzda süngülü tüfek; +x yönüne yürür. Birim: boy ≈ 96 ——
// u: yürüyüş evresi (döngü); o: {dir, lean, rifle:false, col, slung}
function a4_soldier(ctx, x, y, s, u, o = {}) {
  const dir = o.dir || 1, ph = TAU * u, bob = Math.abs(Math.sin(ph)) * 1.4;
  ctx.save(); ctx.translate(x, y + bob * s); ctx.scale(s * dir, s); ctx.rotate(o.lean || 0);
  const col = o.col || P.ink, st = (p, w, cap = 'round') => inkStroke(ctx, p, w, { col, cap });
  // bacaklar: kalça → diz → bilek, dolak kalın; postal
  for (const sg of [1, -1]) {
    const f = ph + (sg > 0 ? 0 : PI), th = .44 * Math.sin(f), kb = .12 + .55 * Math.max(0, Math.cos(f));
    const hp = [sg * 1.5, -38], kn = [hp[0] + Math.sin(th) * 20, hp[1] + Math.cos(th) * 20], an = [kn[0] + Math.sin(th - kb) * 19, kn[1] + Math.cos(th - kb) * 19];
    st(PL([hp, kn], false), 8.4); st(PL([kn, an], false), 7);
    const ba = th - kb + PI / 2, toe = [an[0] + Math.sin(ba) * 10, an[1] + Math.cos(ba) * 1.6 + .6];
    st(PL([[an[0] - 2.4, an[1] + .4], toe], false), 5.4, 'round');
  }
  // kaput: omuzdan etek ucuna, önü açık eteğe doğru
  const coat = SP([[-9, -76], [-4, -79], [5, -78.4], [9.6, -74], [10.6, -56], [13, -34], [6, -31], [-4, -30.6], [-13.6, -33], [-11.4, -56]], true, .6);
  inkFill(ctx, coat, { col });
  // sırt çantası + rulo battaniye
  const bp = SP([[-19.6, -73], [-10, -74], [-9.4, -51], [-19, -51.6]], true, .3); inkFill(ctx, bp, { col });
  const roll = new Path2D(); roll.ellipse(-12.6, -77.6, 9.4, 3.8, -.08, 0, TAU); inkFill(ctx, roll, { col });
  // boyun, baş (burun çıkıntısı +x), kabalak kubbesi
  const head = SP([[-3, -78], [-6, -83], [-5.4, -89], [1, -91.6], [7, -89.4], [8.4, -86], [10, -84.4], [8.4, -83], [8.6, -80.6], [6, -78.6], [2, -77]], true, .8);
  inkFill(ctx, head, { col });
  const kab = SP([[-8.4, -87], [-8, -93.6], [-2, -98.6], [5.6, -97.4], [10, -91.6], [9.4, -87.6], [1, -88.6]], true, .8);
  inkFill(ctx, kab, { col });
  // sallanan kol (uzak kol arkada kalır, yakın kol tüfekte)
  const ar = -.5 * Math.sin(ph), sh = [1, -72], el = [sh[0] + Math.sin(ar) * 15, sh[1] + Math.cos(ar) * 15], hd = [el[0] + Math.sin(ar + .35) * 14, el[1] + Math.cos(ar + .35) * 14];
  st(PL([sh, el, hd], false), 6.4);
  // tüfek: dipçik önde bel hizasında, namlu omuzdan geriye ve yukarı, süngü
  if (o.rifle !== false) {
    st(PL([[9.4, -50], [-9.6, -112]], false), 3.6, 'butt');
    st(PL([[-9.6, -112], [-13.4, -126]], false), 1.6);
    st(PL([[10.6, -52], [6.4, -42.4]], false), 5.6, 'butt');
  }
  // kazıma: kemer ve kaput önü (koyu kütle içinde beyaz çizgi)
  if (s > .9) { cut(ctx, PL([[-11.2, -55], [10.4, -55.6]], false), 1.6, { a: .5 }); cut(ctx, SP([[8.6, -70], [9.2, -56], [11.4, -36]], false), 1.4, { a: .45 }); }
  ctx.restore();
}

// —— hurma ağacı: eğik gövde (kazıma boğumlar), haki yapraklı taç; sw: salınım ——
function a4_palm(ctx, x, y, s, seed, sw = 0, o = {}) {
  const r = rng(seed), lean = (r() - .5) * .5 + (o.lean || 0), Hh = 230 * (.8 + r() * .35);
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const top = [Math.sin(lean) * Hh, -Hh];
  const mid = [top[0] * .4 + (r() - .5) * 30, -Hh * .55];
  // gövde
  const L = [[-8, 0], [mid[0] - 6, mid[1]], [top[0] - 4, top[1]]], R = [[top[0] + 4, top[1]], [mid[0] + 6, mid[1]], [8, 0]];
  const trunk = SP([...L, ...R], true, .7);
  knock(ctx, trunk); plate(ctx, 'ochre', trunk, { n: 2 }); plate(ctx, 'khaki', trunk, { a: .5 });
  inkStroke(ctx, trunk, 2.8 / s);
  for (let i = 1; i < 16; i++) { const u = i / 16, px = lerp(0, top[0], u) + Math.sin(u * PI) * mid[0] * .6, py = -Hh * u; inkStroke(ctx, PL([[px - 6, py + 2], [px + 6, py - 2]], false), 1.6 / s, { a: .7 }); }
  // taç: 9 yaprak, ince uzun kıvrık; kenarı taraklı
  ctx.translate(top[0], top[1]);
  const fronds = o.fronds || 9;
  for (let i = 0; i < fronds; i++) {
    const a = -PI / 2 + (i / (fronds - 1) - .5) * PI * 1.65 + (r() - .5) * .2 + sw * .06 * (i % 2 ? 1 : -1), Lf = 95 + r() * 45, droop = .55 + r() * .4;
    const tip = [Math.cos(a) * Lf, Math.sin(a) * Lf * .6 + Lf * droop * .65];
    const c1 = [Math.cos(a) * Lf * .5, Math.sin(a) * Lf * .55 - 12];
    const nx = -Math.sin(a), ny = Math.cos(a);
    const leaf = new Path2D(); leaf.moveTo(0, 0); leaf.quadraticCurveTo(c1[0] + nx * 14, c1[1] + ny * 14, tip[0], tip[1]); leaf.quadraticCurveTo(c1[0] - nx * 6, c1[1] - ny * 6, 0, 0);
    knock(ctx, leaf); plate(ctx, 'khaki', leaf, { n: i % 3 ? 1 : 2 }); inkStroke(ctx, leaf, 2.2 / s);
    // tarak: yaprakçıklar
    for (let k = 1; k < 9; k++) { const u = k / 9, px = lerp(lerp(0, c1[0], u), lerp(c1[0], tip[0], u), u), py = lerp(lerp(0, c1[1], u), lerp(c1[1], tip[1], u), u); inkStroke(ctx, PL([[px, py], [px + nx * 12 * (1 - u * .6) + Math.cos(a) * 6, py + ny * 12 * (1 - u * .6) + 7]], false), 1.4 / s, { a: .8 }); }
  }
  const nut = new Path2D(); nut.ellipse(0, 6, 14, 9, 0, 0, TAU); knock(ctx, nut); plate(ctx, 'ochre', nut, { n: 2 }); inkStroke(ctx, nut, 2 / s);
  ctx.restore();
}

// —— yerel gönüllü: açık yün cübbe (barakan, kâğıt + okra gölge, is kontur), sarık, tüfek. Birim: boy ≈ 100
//    k: 0 tüfek yanda, 1 omuzda, 2 fişeklik çapraz. Yüz özelliksiz (anonim, geniş plan)
function a4_local(ctx, x, y, s, k = 0, o = {}) {
  const dir = o.dir || 1, lw = px => px / s;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
  // tüfek (yanda ise gövdenin arkasında başlar)
  const rifle = () => {
    if (k === 1) { inkStroke(ctx, PL([[10, -48], [-10, -118]], false), 3.4, { cap: 'butt' }); inkStroke(ctx, PL([[10.6, -48], [7, -40]], false), 5, { cap: 'butt' }); }
    else { inkStroke(ctx, PL([[16, -2], [18, -112]], false), 3.2, { cap: 'butt' }); inkStroke(ctx, PL([[16.4, -2], [16, -18]], false), 5.4, { cap: 'butt' }); }
  };
  if (k !== 1) rifle();
  // ayaklar
  inkFill(ctx, PL([[-8, -4], [-2, -4], [-1, 0], [-11, 0]])); inkFill(ctx, PL([[4, -4], [10, -4], [13, 0], [4, 0]]));
  const robe = SP([[-9, -80], [-2, -83], [8, -80], [12, -60], [15, -30], [17, -4], [6, -2], [-6, -2], [-17, -4], [-15, -36], [-12, -62]], true, .7);
  knock(ctx, robe); plate(ctx, 'ochre', robe, { a: .28 });
  plate(ctx, 'khaki', SP([[-9, -80], [-12, -62], [-15, -36], [-17, -4], [-6, -2], [-4, -40], [-3, -78]], true, .7), { a: .55 }); // gölge yanı
  inkStroke(ctx, robe, lw(2.4));
  for (const q of [[[-2, -76], [-4, -44], [-6, -8]], [[6, -74], [9, -40], [10, -8]]]) inkStroke(ctx, SP(q, false), lw(1.3), { a: .55 });
  if (k === 2) { inkStroke(ctx, PL([[-8, -78], [10, -50]], false), lw(5)); for (let i = 0; i < 6; i++) cut(ctx, PL([[-6 + i * 3, -74 + i * 4.6], [-4 + i * 3, -76 + i * 4.6]], false), lw(1.2), { a: .8 }); }
  // yüz (özelliksiz, gölgede) + sarık + arkaya sarkan uç
  const face = SP([[-4, -84], [-5, -90], [1, -93], [6.4, -91], [8.2, -88.4], [9.8, -87], [8.4, -85.4], [7.6, -83.4], [2, -82]], true, .8);
  knock(ctx, face); plate(ctx, 'ochre', face, { n: 2 }); inkStroke(ctx, face, lw(1.8));
  const tail = SP([[-8, -92], [-13, -84], [-15, -70], [-11, -70], [-9, -84]], true, .8), tur = SP([[-8.6, -90], [-7, -98], [1, -101], [9, -97.6], [9.6, -92], [1, -93.6]], true, .8);
  for (const q of [tail, tur]) { knock(ctx, q); plate(ctx, 'ochre', q, { a: .14 }); inkStroke(ctx, q, lw(1.8)); }
  inkStroke(ctx, SP([[-7.6, -94.6], [1, -97.4], [9.2, -94.4]], false), lw(1.1), { a: .6 });
  if (k === 1) rifle();
  else inkFill(ctx, SP([[10, -62], [17.4, -61], [17.6, -56], [10.4, -56.6]], true)); // tüfeği tutan el (gölgede)
  ctx.restore();
}
// —— bohça: düğümlü bez çıkın (okra, haki çizgili, is kontur); x,y düğüm noktası ——
function a4_bundle(ctx, x, y, s, seed = 1, o = {}) {
  const lw = px => px / s;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(o.rot || 0);
  const b = SP([[-2, 1], [7, 2], [11, 9], [10, 18], [3, 21], [-6, 20], [-10, 13], [-8, 4]], true, .8);
  knock(ctx, b); plate(ctx, o.col || 'ochre', b, { a: .8 });
  ctx.save(); ctx.clip(b); plate(ctx, 'khaki', PL([[-14, 8], [14, 11], [14, 14], [-14, 11]]), { a: .7 }); plate(ctx, 'khaki', SP([[-10, 13], [-8, 4], [-2, 1], [0, 20], [-6, 20]], true, .8), { a: .55 }); ctx.restore();
  inkStroke(ctx, SP([[-1, 4], [2, 12], [1, 19]], false), lw(1.4), { a: .55 }); inkStroke(ctx, SP([[5, 4], [8, 10], [8, 17]], false), lw(1.2), { a: .45 });
  inkStroke(ctx, b, lw(2.4));
  const knot = SP([[-3, 2], [-4, -4], [0, -7], [4, -4], [3, 2]], true, .8); knock(ctx, knot); plate(ctx, o.col || 'ochre', knot, { n: 2 }); inkStroke(ctx, knot, lw(2));
  ctx.restore();
}
// —— çarşaflı kadın, arkadan ¾ (yüz görünmez): pelerin + etek, is kütle, kazınmış kıvrımlar; iki karede adım ——
// Birim: boy ≈ 100, +x'e yürür. o: {stoop, sep (8 px kâğıt ayırma), bundle: 'near'|'far', seed}
function a4_carsaf(ctx, x, y, s, ph, o = {}) {
  const lw = px => px / s, sw = ph ? 1 : -1;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(o.stoop || 0);
  if (o.bundle === 'far') a4_bundle(ctx, 18, -45, .85, (o.seed || 1) + 2, { rot: -.12 });
  for (const [fx, up] of [[sw * 5 + 4, 0], [-sw * 5 - 1, 1.2]]) inkFill(ctx, SP([[fx - 4.4, -2 - up], [fx + 4.6, -2.6 - up], [fx + 6.4, 0 - up], [fx - 4.6, .3 - up]], true, .6));
  const hm = sw * 1.4;
  const pts = [[-1, -100], [4.6, -99], [7.4, -95.4], [8.4, -90], [7.6, -85.6], [6.2, -83.4], [10.6, -80.6], [14.4, -70], [17.2, -57], [18.4, -49.6], [13.8, -47.4], [14.6, -30], [16.4 + hm, -12], [17.6 + hm, -3.4], [9, -2.4], [0, -3], [-9, -2.2], [-17.6 - hm * .6, -3.4], [-16 - hm * .4, -14], [-14, -32], [-13.6, -47.2], [-18.6, -49.8], [-17.6, -60], [-15, -72], [-11.6, -80], [-9.4, -86], [-8.6, -93], [-6, -98.4]];
  const body = SP(rough(pts, .2, o.seed || 3), true, .7);
  if (o.sep) inkStroke(ctx, body, lw(16), { col: P.paper });
  inkFill(ctx, body);
  // kazıma: başörtüsü kenarı, pelerin eteği, kıvrımlar
  const c = (q, w = 2.2, a = .6) => cut(ctx, SP(q, false), lw(w), { a });
  c([[5.6, -98], [3.4, -90], [5.6, -83]], 2, .5);
  c([[-17.4, -50.4], [-4, -47.4], [8, -47.8], [17.6, -50]], 2.4, .7);
  c([[-8, -80], [-11, -66], [-12.6, -52]], 2.2, .5); c([[2, -80], [2.4, -66], [3.4, -50]], 2, .45); c([[10.6, -76], [13.4, -64], [15.6, -52]], 2, .45);
  c([[-9, -44], [-10.4, -24], [-12.4, -6]], 2.2, .5); c([[1, -44], [0, -24], [1, -5]], 2, .45); c([[9.6, -44], [11.4, -24], [13, -6]], 2, .45);
  if (o.bundle === 'near') a4_bundle(ctx, -18, -46, .92, (o.seed || 1) + 5, { rot: .1 });
  ctx.restore();
}
// —— muhacir damgaları (is): bohçalı kadın, sırtında çuval taşıyan adam, çocuk; ph adım evresi ——
function a4_migrant(ctx, x, y, s, kind, ph, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const p = new Path2D(), sw = ph ? 1 : -1;
  if (kind === 0) { // başörtülü kadın, başında bohça
    spl(p, [[0, -46], [6, -45], [7.6, -39], [8.6, -30], [11, -16], [12 + sw, 0], [-9, 0], [-9, -14], [-8, -30], [-7, -40], [-5, -45]], true, .7);
    spl(p, [[-6, -46], [-4, -54], [6, -55], [9, -48], [2, -45]], true, .7);
  } else if (kind === 1) { // adam, sırtında çuval, elinde değnek
    spl(p, [[2, -48], [7, -47], [8, -42], [6, -38], [9, -24], [8, -14], [10 + sw * 3, 0], [6 + sw * 3, 0], [3, -14], [-1, -14], [-3 - sw * 3, 0], [-7 - sw * 3, 0], [-5, -16], [-6, -30], [-4, -40], [-2, -46]], true, .6);
    spl(p, [[-5, -42], [-14, -46], [-19, -36], [-16, -24], [-6, -24]], true, .7);
    p.moveTo(9, -30); p.lineTo(17, 0); p.lineTo(18.6, 0); p.lineTo(10.6, -30); p.closePath();
  } else { // çocuk
    spl(p, [[0, -30], [4, -29], [5, -24], [7, -12], [8 + sw * 2, 0], [-6 - sw * 2, 0], [-5, -12], [-4, -24], [-3, -29]], true, .7);
  }
  inkFill(ctx, p, { col: o.col });
  ctx.restore();
}
// uzak İstanbul silueti: kubbeler ve minareler (tek kalıp)
function a4_skyline(g, x0, y0, s, seed) {
  const r = rng(seed), p = new Path2D();
  let x = x0;
  p.moveTo(x0, y0);
  for (let i = 0; i < 7; i++) {
    const w = (70 + r() * 70) * s, dh = (20 + r() * 26) * s, big = i === 2 || i === 5;
    p.lineTo(x, y0 - 18 * s); p.lineTo(x + w * .15, y0 - 18 * s);
    const R = (big ? 46 : 22 + r() * 12) * s; p.lineTo(x + w * .5 - R, y0 - 18 * s - dh * .3); p.arc(x + w * .5, y0 - 18 * s - dh * .3, R, PI, TAU); p.lineTo(x + w * .85, y0 - 18 * s);
    if (big) for (const mx of [x + w * .5 - R - 26 * s, x + w * .5 + R + 26 * s]) { p.moveTo(mx - 3.4 * s, y0); p.lineTo(mx - 3.4 * s, y0 - 120 * s); p.lineTo(mx, y0 - 142 * s); p.lineTo(mx + 3.4 * s, y0 - 120 * s); p.lineTo(mx + 3.4 * s, y0); }
    p.moveTo(x + w, y0 - 18 * s); x += w;
  }
  p.lineTo(x, y0); p.lineTo(x0, y0); p.closePath();
  knock(g, p); plate(g, 'khaki', p, { a: .55 }); inkStroke(g, p, 1.6, { a: .8 });
}
// deve silueti (is): yük semerli; ph yürüyüş evresi
function a4_camel(ctx, x, y, s, ph = 0, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.dir || 1), s);
  const p = new Path2D();
  spl(p, [[-46, -66], [-30, -86], [-12, -92], [6, -84], [22, -74], [34, -70], [44, -78], [50, -96], [58, -104], [70, -104], [74, -98], [64, -96], [58, -86], [54, -66], [40, -50], [20, -46], [-20, -46], [-40, -52]], true, .7);
  for (const [lx, sw] of [[-34, 1], [-24, -1], [24, 1], [34, -1]]) { const a = (ph ? sw : -sw) * .14; p.moveTo(lx - 3, -50); p.lineTo(lx - 3 + Math.sin(a) * 26, -24); p.lineTo(lx - 2 + Math.sin(a) * 50, 0); p.lineTo(lx + 5 + Math.sin(a) * 50, 0); p.lineTo(lx + 3 + Math.sin(a) * 26, -24); p.lineTo(lx + 4, -50); p.closePath(); }
  inkFill(ctx, p, { col: o.col });
  // semer ve yük
  const load = SP([[-30, -88], [-20, -104], [2, -106], [12, -90], [-8, -86]], true, .6); knock(ctx, load); plate(ctx, 'ochre', load, { n: 2 }); inkStroke(ctx, load, 2.4 / s);
  inkStroke(ctx, SP([[-46, -66], [-56, -50], [-52, -40]], false), 2.4 / s, { col: o.col });
  ctx.restore();
}
// çan çadır: okra bez, haki gölge yüzü, açık kapı (is), ip ve kazıklar; üstünde küçük sancak (kırmızı, küçük alan)
function a4_tent(ctx, x, y, s, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const lit = PL([[-120, 0], [0, -150], [30, 0]]), shade = PL([[0, -150], [118, -2], [30, 0]]);
  for (const q of [lit, shade]) knock(ctx, q);
  plate(ctx, 'ochre', lit, { a: .45 }); plate(ctx, 'khaki', shade); plate(ctx, 'ochre', shade, { a: .4 });
  const door = PL([[-26, 0], [-4, -96], [12, 0]]); inkFill(ctx, door);
  for (const q of [lit, shade]) inkStroke(ctx, q, 3 / s);
  for (const u of [.25, .5, .75]) { inkStroke(ctx, PL([[lerp(0, -120, u), lerp(-150, 0, u)], [lerp(0, -120, u) - 40, 6]], false), 1.4 / s, { a: .7 }); inkStroke(ctx, PL([[lerp(0, 118, u), lerp(-150, -2, u)], [lerp(0, 118, u) + 40, 6]], false), 1.4 / s, { a: .7 }); }
  inkStroke(ctx, PL([[0, -150], [0, -214]], false), 3 / s);
  if (o.flag !== false && (o.raise ?? 1) > .02) {
    ctx.save(); ctx.translate(0, (1 - (o.raise ?? 1)) * 52);
    const wv = o.wave || 0, fl = SP([[0, -212], [24, -214 + wv], [50, -210 - wv], [50, -180 - wv * .5], [24, -184 + wv], [0, -182]], true, .5);
    knock(ctx, fl); plate(ctx, 'red', fl); inkStroke(ctx, fl, 2 / s);
    const cr = new Path2D(); cr.arc(20, -197, 7.4, 0, TAU); cr.arc(22.8, -197, 6, 0, TAU, true);
    ctx.save(); ctx.fillStyle = P.paper; ctx.fill(cr, 'evenodd');
    const stp = []; for (let i = 0; i < 10; i++) { const a = -PI / 2 + i * PI / 5, rr = i % 2 ? 1.7 : 4; stp.push([31 + Math.cos(a) * rr, -197 + Math.sin(a) * rr]); }
    ctx.fill(PL(stp)); ctx.restore();
    ctx.restore();
  }
  ctx.restore();
}
// düz damlı ak evler, kubbe, minare (uzak kasaba)
function a4_town(g, x0, y0, s, seed) {
  const r = rng(seed);
  let x = x0;
  for (let i = 0; i < 11; i++) {
    const w = (40 + r() * 50) * s, h = (26 + r() * 40) * s, yy = y0 - r() * 10 * s;
    const box = a4_rect(x, yy - h, x + w, yy);
    knock(g, box); plate(g, 'ochre', a4_rect(x + w * .66, yy - h, x + w, yy), { a: .45 }); inkStroke(g, box, 2);
    for (let k = 0; k < 2; k++) if (r() < .7) inkFill(g, a4_rect(x + w * (.2 + k * .3), yy - h * .6, x + w * (.2 + k * .3) + 5 * s, yy - h * .6 + 8 * s));
    if (i === 4) { const d = new Path2D(); d.arc(x + w / 2, yy - h, w * .34, PI, TAU); knock(g, d); plate(g, 'ochre', d, { a: .3 }); inkStroke(g, d, 2); }
    if (i === 6) { const mx = x + w * .3, mw = 9 * s, mh = 120 * s; const m = PL([[mx - mw, yy - h], [mx - mw, yy - mh], [mx, yy - mh - 26 * s], [mx + mw, yy - mh], [mx + mw, yy - h]]); knock(g, m); plate(g, 'ochre', PL([[mx, yy - h], [mx, yy - mh - 26 * s], [mx + mw, yy - mh], [mx + mw, yy - h]]), { a: .45 }); inkStroke(g, m, 2); inkStroke(g, PL([[mx - mw - 5, yy - mh * .78], [mx + mw + 5, yy - mh * .78]], false), 3); }
    x += w * (.8 + r() * .3);
  }
}

// —— cephe donanımı ——
// kum torbası sırası: knock + okra + haki gölge + is kontur; rows sıra, şaşırtmalı
function a4_sandbags(g, x0, x1, yTop, rows, seed, o = {}) {
  const r = rng(seed), bw = o.bw || 74, bh = o.bh || 30;
  for (let row = rows - 1; row >= 0; row--) {
    const y = yTop + row * (bh - 6);
    for (let x = x0 - (row % 2) * bw * .5; x < x1; x += bw - 4) {
      const w = bw * (.9 + r() * .2), j = (r() - .5) * 5;
      const b = SP(rough([[x, y + bh * .5 + j], [x + w * .1, y + j], [x + w * .5, y - 3 + j], [x + w * .9, y + j], [x + w, y + bh * .5 + j], [x + w * .9, y + bh + j], [x + w * .5, y + bh + 3 + j], [x + w * .1, y + bh + j]], 1, r() * 999 | 0), true, .7);
      knock(g, b); plate(g, 'ochre', b, { a: o.a ?? .55 }); plate(g, 'khaki', SP([[x, y + bh * .55 + j], [x + w, y + bh * .55 + j], [x + w * .9, y + bh + j], [x + w * .1, y + bh + j]], true, .7), { a: .55 });
      inkStroke(g, b, 2.2); inkStroke(g, PL([[x + w * .78, y + 4 + j], [x + w * .84, y + bh * .5 + j]], false), 1.4, { a: .55 });
    }
  }
}
// dikenli tel: çapraz kazık + bobin + dikenler
function a4_wire(g, x0, x1, y, seed, o = {}) {
  const r = rng(seed), h = o.h || 46, step = o.step || 150;
  for (let x = x0; x < x1; x += step * (.8 + r() * .4)) { inkStroke(g, PL([[x - 14, y], [x + 10, y - h - 8]], false), 3.2); inkStroke(g, PL([[x + 14, y], [x - 8, y - h - 6]], false), 3.2); }
  const coil = new Path2D(); for (let x = x0; x < x1; x += 15) { const k = r(); coil.moveTo(x + 22, y - h * .45); coil.ellipse(x, y - h * .45, 22, h * .45 + k * 4, .25, 0, TAU); }
  inkStroke(g, coil, 1.4, { a: .75 });
  for (const yy of [y - h * .2, y - h * .85]) { inkStroke(g, PL([[x0, yy], [x1, yy + (r() - .5) * 6]], false), 1.5); for (let x = x0 + 8; x < x1; x += 22) inkStroke(g, PL([[x - 4, yy - 4], [x + 4, yy + 4]], false), 1.4); }
}
// siper sırası: kabalak + süngü ucu (is), siperin üstünden görünür; birim boy ≈ 60
function a4_bayonetHead(ctx, x, y, s, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const p = new Path2D();
  spl(p, [[-12, 0], [-11, -14], [-8, -20], [-9, -27], [-6, -34], [2, -36], [8, -32], [10, -27], [9, -22], [12, -14], [13, 0]], true, .7);
  inkFill(ctx, p, { col: o.col });
  inkStroke(ctx, PL([[6, -6], [18, -56]], false), 3, { cap: 'butt', col: o.col }); inkStroke(ctx, PL([[18, -56], [20.6, -70]], false), 1.4, { col: o.col });
  ctx.restore();
}
// zırhlı gemi silueti (is): alçak gövde, iki baca, direkler, taret; dumanı düz
function a4_ship(ctx, x, y, s, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * (o.dir || 1), s);
  const p = new Path2D();
  p.moveTo(-100, -6); p.lineTo(-94, 4); p.lineTo(92, 4); p.lineTo(104, -12); p.lineTo(70, -10); p.lineTo(70, -18); p.lineTo(40, -18); p.lineTo(36, -28); p.lineTo(-10, -28); p.lineTo(-14, -18); p.lineTo(-60, -18); p.lineTo(-62, -10); p.closePath();
  for (const fx of [-2, 22]) { p.rect(fx, -46, 10, 20); }
  p.rect(-74, -24, 22, 8); p.rect(54, -24, 22, 8);
  inkFill(ctx, p, { col: o.col });
  inkStroke(ctx, PL([[-30, -28], [-30, -70]], false), 2.2, { col: o.col }); inkStroke(ctx, PL([[46, -18], [46, -60]], false), 2, { col: o.col });
  inkStroke(ctx, PL([[-74, -20], [-96, -24]], false), 3, { col: o.col }); inkStroke(ctx, PL([[76, -20], [98, -24]], false), 3, { col: o.col });
  ctx.restore();
}
// buharlı tren silueti (is): lokomotif + kömürlük + 3 vagon; +x'e gider; duman düz yuvarlaklar
function a4_train(ctx, x, y, s, t) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const p = new Path2D();
  p.rect(150, -46, 70, 34); p.rect(206, -64, 34, 52); p.moveTo(150, -46); p.lineTo(150, -50); p.lineTo(160, -50); p.lineTo(160, -46);
  p.rect(170, -70, 14, 26); p.moveTo(166, -70); p.lineTo(188, -70); p.lineTo(186, -76); p.lineTo(168, -76); p.closePath();
  p.moveTo(220, -14); p.lineTo(236, -2); p.lineTo(150, -2); p.lineTo(150, -14); p.closePath();
  p.rect(108, -40, 40, 30);
  for (const cx of [0, -96, -192]) { p.rect(cx - 2, -50, 92, 40); p.moveTo(cx - 6, -50); p.lineTo(cx + 94, -50); p.lineTo(cx + 88, -56); p.lineTo(cx, -56); p.closePath(); }
  inkFill(ctx, p);
  for (const cx of [-180, -120, -84, -24, 12, 72, 118, 140, 170, 196, 222]) { const w = new Path2D(); w.arc(cx, -6, cx > 160 ? 11 : 9, 0, TAU); knock(ctx, w, P.ink); cut(ctx, (() => { const q = new Path2D(); q.arc(cx, -6, cx > 160 ? 6 : 5, 0, TAU); return q; })(), 1.4, { a: .6 }); }
  for (const cx of [0, -96, -192]) for (let k = 0; k < 3; k++) cut(ctx, a4_rect(cx + 10 + k * 26, -42, cx + 26 + k * 26, -30), 1.6, { a: .55 });
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = rgba(P.khaki, .55);
  for (let j = 0; j < 6; j++) { ctx.beginPath(); ctx.ellipse(170 - j * 34 - (t * 30 % 34), -86 - j * 10, 16 + j * 5, 10 + j * 3, 0, 0, TAU); ctx.fill(); }
  ctx.restore();
  ctx.restore();
}
// cep saati: pirinç (okra) kasa, kâğıt kadran, akrep/yelkovan; saniye ibresi saniyede bir atar
function a4_watch(ctx, x, y, r, t, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.rot || 0);
  const crown = a4_rect(-r * .14, -r * 1.26, r * .14, -r * .96); knock(ctx, crown); plate(ctx, 'ochre', crown, { n: 2 }); inkStroke(ctx, crown, 2);
  const ring = new Path2D(); ring.arc(0, -r * 1.36, r * .2, 0, TAU); inkStroke(ctx, ring, 2.4);
  const cs = new Path2D(); cs.arc(0, 0, r, 0, TAU); knock(ctx, cs); plate(ctx, 'ochre', cs, { n: 2 }); inkStroke(ctx, cs, 2.8);
  const face = new Path2D(); face.arc(0, 0, r * .8, 0, TAU); knock(ctx, face, '#F7F0DE'); inkStroke(ctx, face, 1.6);
  for (let k = 0; k < 12; k++) { const a = k / 12 * TAU; inkStroke(ctx, PL([[Math.cos(a) * r * .66, Math.sin(a) * r * .66], [Math.cos(a) * r * .76, Math.sin(a) * r * .76]], false), k % 3 ? 1.2 : 2.4); }
  const sec = Math.floor(t) % 60, ah = -PI / 2 + (4 + 50 / 60) / 12 * TAU, am = -PI / 2 + 50 / 60 * TAU + sec / 3600 * TAU, as = -PI / 2 + sec / 60 * TAU;
  inkStroke(ctx, PL([[0, 0], [Math.cos(ah) * r * .4, Math.sin(ah) * r * .4]], false), 2.8); inkStroke(ctx, PL([[0, 0], [Math.cos(am) * r * .62, Math.sin(am) * r * .62]], false), 2);
  inkStroke(ctx, PL([[0, 0], [Math.cos(as) * r * .7, Math.sin(as) * r * .7]], false), 1);
  const hub = new Path2D(); hub.arc(0, 0, 2.6, 0, TAU); inkFill(ctx, hub);
  ctx.restore();
}
// baskıyla gelme (figür): üstten aşağı silme + kalıp kayıklığı yerine oturur. u: 0..1
function a4_pressIn(ctx, u, y0, y1, draw) {
  if (u <= 0) return;
  const b = REG.boost; REG.boost = 1 + 5 * (1 - E.out3(clamp(u)));
  ctx.save(); ctx.beginPath(); ctx.rect(-500, y0 - 400, W + 1000, (y1 - y0 + 400) * E.out2(clamp(u * 1.6)) + 400); ctx.clip();
  draw(); ctx.restore(); REG.boost = b;
}

// —— toz: rüzgârla sürüklenen benekler (hareketli, düz) ——
function a4_dust(ctx, t, o) {
  const r = rng(o.seed || 5), n = o.n || 60, [x0, y0, x1, y1] = o.box, wx = o.wind ?? 60, wy = o.rise ?? -6;
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = P[o.col || 'ochre'];
  for (let i = 0; i < n; i++) {
    const bx = r(), by = r(), sp = .6 + r() * .8, sz = (o.size || 3) * (.5 + r());
    const x = x0 + (((bx * (x1 - x0) + t * wx * sp) % (x1 - x0)) + (x1 - x0)) % (x1 - x0);
    const y = y0 + (((by * (y1 - y0) + t * wy * sp + Math.sin(t * 1.3 + i) * 6) % (y1 - y0)) + (y1 - y0)) % (y1 - y0);
    ctx.globalAlpha = (o.a ?? .55) * (.5 + .5 * r());
    ctx.beginPath(); ctx.ellipse(x, y, sz * 1.6, sz * .8, (r() - .5) * .6, 0, TAU); ctx.fill();
  }
  ctx.restore();
}

// —— küçük kişi levhası: nameTag ile aynı görünüm; genişlik harf aralığını (ls 1) da ölçer, uzun adlar kenara taşmaz ——
function a4_plaque(ctx, x, y, name, sub, lt, d, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .2, d - .4, d); if (a <= 0) return;
  const fs = o.size || 28, ss = o.sub || 19;
  ctx.save(); ctx.font = FONT.title(fs); ctx.letterSpacing = '1px'; const w1 = ctx.measureText(name).width; ctx.font = FONT.mono(ss); ctx.letterSpacing = '0px'; const w2 = ctx.measureText(sub || '').width; ctx.restore();
  const w = Math.max(w1, w2) + 48, h = fs + ss + 38, sl = (1 - E.out3(ramp(lt, 0, .3))) * 14;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, sl);
  plate(ctx, 'ink', a4_rect(x + 7, y + 9, x + w + 7, y + h + 9), { a: .35 });
  const box = PL(rough([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], .8, name.length + 3));
  knock(ctx, box, o.bg || P.paperD); inkStroke(ctx, box, 3);
  plate(ctx, 'red', a4_rect(x, y + h - 6, x + w, y + h));
  txt(ctx, name, x + 24, y + 14 + fs * .8, FONT.title(fs), { ls: 1 });
  if (sub) txt(ctx, sub, x + 24, y + 22 + fs + ss * .72, FONT.mono(ss));
  ctx.restore();
}
// —— izleyici katmanı harita etiketi (Courier, paperD kutu, çizgi) ——
function a4_tag(ctx, s, x, y, ax, ay, a = 1, o = {}) {
  if (NOTEXT || a <= 0) return;
  const fs = o.size || 26;
  ctx.save(); ctx.font = FONT.mono(fs); ctx.letterSpacing = '3px'; const w = ctx.measureText(s).width; ctx.restore();
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, (1 - a) * 8);
  if (ax != null) { const inX = ax >= x && ax <= x + w + 28, ex = inX ? clamp(ax, x + 12, x + w + 16) : (ax < x ? x : x + w + 28), ey = inX ? (ay < y ? y - fs - 2 : y + 12) : y - fs * .3; inkStroke(ctx, PL([[ax, ay], [ex, ey]], false), 1.8); }
  const b = PL(rough([[x, y - fs - 2], [x + w + 28, y - fs - 2], [x + w + 28, y + 12], [x, y + 12]], .7, s.length));
  plate(ctx, 'ink', PL([[x + 5, y - fs + 4], [x + w + 33, y - fs + 4], [x + w + 33, y + 17], [x + 5, y + 17]]), { a: .3 });
  knock(ctx, b, o.bg || P.paperD); inkStroke(ctx, b, 2);
  txt(ctx, s, x + 14, y + 2, FONT.mono(fs), { ls: 3 });
  ctx.restore();
}
// lastik damga şehir noktası: is halka + dolu kare; on: 0..1 (söner)
function a4_city(ctx, x, y, on = 1, o = {}) {
  const r = o.r || 11;
  const ring = new Path2D(); ring.arc(x, y, r, 0, TAU);
  knock(ctx, ring, P.paperD); inkStroke(ctx, ring, 2.6);
  if (on > 0) { const sq = a4_rect(x - r * .55, y - r * .55, x + r * .55, y + r * .55); inkFill(ctx, sq, { a: on }); }
}

// —— rota: kesik çizgi, kelimeye bağlı ilerler; lineDashOffset ile yürür ——
function a4_sample(pts, closed = false, per = 10) {
  // Catmull-Rom'u noktalara aç
  const out = [], n = pts.length, Pn = i => pts[clamp(i, 0, n - 1)];
  for (let i = 0; i < n - 1; i++) {
    const p0 = Pn(i - 1), p1 = Pn(i), p2 = Pn(i + 1), p3 = Pn(i + 2);
    const L = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]), m = Math.max(2, Math.ceil(L / per));
    for (let k = 0; k < m; k++) {
      const u = k / m, u2 = u * u, u3 = u2 * u;
      out.push([0, 1].map(j => .5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3)));
    }
  }
  out.push(pts[n - 1]);
  return out;
}
function a4_cumLen(s) { const c = [0]; for (let i = 1; i < s.length; i++) c.push(c[i - 1] + Math.hypot(s[i][0] - s[i - 1][0], s[i][1] - s[i - 1][1])); return c; }
// s: örneklenmiş noktalar, len: a4_cumLen; d: çizilecek uzunluk (px). Ucu döndürür.
function a4_partial(s, cl, d) {
  const out = [s[0]];
  for (let i = 1; i < s.length; i++) {
    if (cl[i] <= d) { out.push(s[i]); continue; }
    const f = (d - cl[i - 1]) / (cl[i] - cl[i - 1]); out.push([lerp(s[i - 1][0], s[i][0], f), lerp(s[i - 1][1], s[i][1], f)]); break;
  }
  return out;
}
function a4_route(ctx, s, cl, p, t, o = {}) {
  if (p <= 0) return null;
  const d = cl[cl.length - 1] * clamp(p), q = a4_partial(s, cl, d);
  if (q.length < 2) return null;
  const path = PL(q, false);
  ctx.save();
  inkStroke(ctx, path, (o.w || 5) + 6, { col: o.halo || P.paperD });
  ctx.setLineDash(o.dash || [18, 11]); ctx.lineDashOffset = -t * (o.speed ?? 26);
  inkStroke(ctx, path, o.w || 5, { cap: 'butt', col: o.col });
  ctx.restore();
  const e = q[q.length - 1], e0 = q[Math.max(0, q.length - 3)];
  return { x: e[0], y: e[1], ang: Math.atan2(e[1] - e0[1], e[0] - e0[0]) };
}
// karşı taraf oku: is gövde, 45° kazıma, uçta üçgen; p: 0..1 çizilme
function a4_arrow(ctx, pts, p, o = {}) {
  if (p <= 0) return;
  const s = a4_sample(pts, false, 8), cl = a4_cumLen(s), tot = cl[cl.length - 1], d = tot * clamp(p), q = a4_partial(s, cl, d);
  if (q.length < 2) return;
  const w = o.w || 16, col = o.col || 'ink';
  const path = PL(q, false);
  ctx.save();
  if (col === 'ink') inkStroke(ctx, path, w, { cap: 'butt' }); else { const [dx, dy] = regOf(col); ctx.translate(dx, dy); inkStroke(ctx, path, w, { col: P[col], cap: 'butt', mode: 'multiply' }); }
  ctx.restore();
  for (let k = 14; k < d - 10; k += 15) {
    const qq = a4_partial(s, cl, k), a = qq[qq.length - 1], b = qq[Math.max(0, qq.length - 2)], an = Math.atan2(a[1] - b[1], a[0] - b[0]) + PI / 4;
    cut(ctx, PL([[a[0] - Math.cos(an) * w * .45, a[1] - Math.sin(an) * w * .45], [a[0] + Math.cos(an) * w * .45, a[1] + Math.sin(an) * w * .45]], false), 1.6, { a: .75 });
  }
  const e = q[q.length - 1], e0 = q[Math.max(0, q.length - 3)], an = Math.atan2(e[1] - e0[1], e[0] - e0[0]), hs = w * 1.9;
  const head = PL([[e[0] + Math.cos(an) * hs * 1.1, e[1] + Math.sin(an) * hs * 1.1], [e[0] + Math.cos(an + 2.3) * hs, e[1] + Math.sin(an + 2.3) * hs], [e[0] + Math.cos(an - 2.3) * hs, e[1] + Math.sin(an - 2.3) * hs]]);
  col === 'ink' ? inkFill(ctx, head) : plate(ctx, col, head, { flat: true });
}
// cephe hattı (tarak dişli): Türk tarafı kırmızı; p: çizilme oranı
function a4_front(ctx, pts, p, o = {}) {
  if (p <= 0) return;
  const s = a4_sample(pts, false, 6), cl = a4_cumLen(s), tot = cl[cl.length - 1], d = tot * clamp(p), q = a4_partial(s, cl, d);
  if (q.length < 2) return;
  const col = o.col || 'red', w = o.w || 7, side = o.side || 1;
  ctx.save(); const [dx, dy] = regOf(col); ctx.translate(dx, dy);
  inkStroke(ctx, PL(q, false), w, { col: P[col], cap: 'butt', mode: 'multiply' }); ctx.restore();
  for (let k = 8; k < d; k += o.step || 18) {
    const qq = a4_partial(s, cl, k), a = qq[qq.length - 1], b = qq[Math.max(0, qq.length - 2)], an = Math.atan2(a[1] - b[1], a[0] - b[0]);
    const nx = Math.cos(an + side * PI / 2), ny = Math.sin(an + side * PI / 2), tx = Math.cos(an), ty = Math.sin(an), th = o.tooth || 12;
    plate(ctx, col, PL([[a[0] - tx * 5, a[1] - ty * 5], [a[0] + nx * th, a[1] + ny * th], [a[0] + tx * 5, a[1] + ty * 5]]), { flat: true });
  }
}
// harita kıyısı: kaba (gürültülü) kapalı yol
function a4_coast(pts, seed, amp = 2.2) { return SP(rough(pts, amp, seed), true, .5); }
// deniz eş-derinlik çizgileri: kıyı çevresinde 3 halka (kara dolgusu sonra örter)
function a4_ripples(g, lands, sc = 1, o = {}) {
  for (const [w, a] of [[30, .28], [15, .5]]) for (const L of lands) { inkStroke(g, L, (w + 1.6) * sc, { a: a * (o.a ?? 1) }); inkStroke(g, L, w * sc, { col: o.sea || P.paperD }); }
}
// gravür deniz: yatay ince tarama (kâğıt sınırı içinde, karalar sonra örter)
function a4_seaHatch(g, x0, y0, x1, y1, o = {}) {
  plate(g, 'khaki', a4_rect(x0, y0, x1, y1), { a: o.a ?? .2 });
  const p = new Path2D(); for (let y = y0; y < y1; y += o.step || 9) { p.moveTo(x0, y); p.lineTo(x1, y); }
  inkStroke(g, p, o.w || 1.1, { a: o.la ?? .22, cap: 'butt' });
}
// kurmay haritası kâğıdı: paperD, çift çerçeve, kenar ölçek dişleri, köşe raptiyeleri (raptiye is)
function a4_sheet(g, x, y, w, h, seed) {
  plate(g, 'ink', a4_rect(x + 14, y + 18, x + w + 14, y + h + 18), { a: .3 });
  const sh = PL(rough([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], 2.4, seed));
  knock(g, sh, P.paperD); plate(g, 'ochre', sh, { a: .12 });
  return sh;
}
function a4_sheetFrame(g, x, y, w, h, sh) {
  inkStroke(g, a4_rect(x + 22, y + 22, x + w - 22, y + h - 22), 2.6);
  inkStroke(g, a4_rect(x + 32, y + 32, x + w - 32, y + h - 32), 1.2, { a: .8 });
  for (let xx = x + 32; xx < x + w - 52; xx += 40) inkFill(g, a4_rect(xx, y + 22, xx + 20, y + 32)), inkFill(g, a4_rect(xx, y + h - 32, xx + 20, y + h - 22));
  for (const [px, py] of [[x + 40, y + 40], [x + w - 40, y + 40], [x + 40, y + h - 40], [x + w - 40, y + h - 40]]) { const p = new Path2D(); p.arc(px, py, 8, 0, TAU); knock(g, p); plate(g, 'khaki', p, { n: 2 }); inkStroke(g, p, 2.2); }
  inkStroke(g, sh, 3);
}
// kartuş: Osmanlıca soyut başlık izi
function a4_cartouche(g, x, y, w, h, seed) {
  const c = a4_rect(x, y, x + w, y + h); knock(g, c, P.paper); inkStroke(g, c, 2.2); inkStroke(g, a4_rect(x + 6, y + 6, x + w - 6, y + h - 6), 1);
  scriptLine(g, x + w - 16, y + h * .45, w * .82, 12, seed); scriptLine(g, x + w - 30, y + h * .78, w * .55, 9, seed + 1, { w: 1.6 });
}

// —— kişiler ——
// subay büstü: setre (haki) + kabalak; sep: önündeki figürü ayıran kâğıt kontur
function a4_officer(ctx, o) {
  const b = { x: o.x, y: o.y, s: o.s, dir: o.dir || -1 };
  bust(ctx, { ...b, coat: o.coat || 'setre', col: o.col || 'khaki', w: o.w || .98, seed: o.seed || 3, len: o.len || 300, tilt: o.btilt || 0, turn: o.turn ?? .2, sep: o.sep, back: o.back, arms: o.arms });
  head3q(ctx, { ...b, who: o.who, gear: o.gear === undefined ? 'kabalak' : o.gear, gearCol: 'ink', light: o.light || 'front', lookAt: o.lookAt, look: o.look, age: o.age, tilt: o.tilt || 0 });
}

// ———————————————————————————————— çekimler ————————————————————————————————

// E01 · Renk çöker: 1908 kartpostalının son kalıpları (altın şafak bandı "kuşağın"da, turkuaz tepeler "asıl"da) kalkar;
// geriye haki, okra ve is kalır. Güneş yarım ton dumanın ardında okra bir disktir (ışın yok, kırmızı yok).
// "savaş": tepelerde is patlama yıldızı + yarım ton duman, büyük SAVAŞ damgası; ufukta ince kırmızı cephe hattı çizilir.
// (Kelime anları mutlak zamanla: cutRules çekim başını kaydırabilir.)
{
  const T0 = S('E01'), tSav = Wd('E01', 'savaş'), tKus = Wd('E01', 'kuşağın'), tAsil = Wd('E01', 'asıl'), tOkul = Wd('E01', 'okulu');
  const SUN = [1290, 600], HOR = 668, BOOM = [820, 640];
  const hills = a4_ridgePts(-160, W + 160, 632, 24, 3, 16, 1.4);
  const ridge = a4_ridgePts(-200, W + 200, 826, 14, 8, 18, .9);
  const front = a4_ridgePts(-200, W + 200, 1004, 14, 41, 12);
  const frontLine = hills.map(([x, y]) => [x, y - 4]);
  const skyClip = a4_rect(-200, -200, W + 200, HOR + 4);
  shot(T0, (ctx, st) => {
    setReg(401);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt), t0 = t - lt;
    const sk = shake(t, tSav, 9, 5);
    const cm = { x: lerp(960, 1012, E.sine(st.p)), y: lerp(540, 566, E.sine(st.p)), z: lerp(1, 1.05, E.sine(st.p)), sx: sk[0], sy: sk[1] };
    // —— gök (durağan): kâğıt, ufka doğru okra bantlar, tepede is yarım ton
    const sky = a4_L('E01-sky2', g => {
      paperBG(g);
      g.save(); g.clip(skyClip);
      plate(g, 'ochre', a4_rect(-200, 352, W + 200, HOR + 4), { a: .16 });
      plate(g, 'ochre', a4_rect(-200, 512, W + 200, HOR + 4), { a: .22 });
      radialHT(g, 'ink', SUN[0], 1500, 1200, 1640, 0, .13, { cell: 12, ang: 45, box: [-160, -140, W + 160, 280] });
      g.restore();
    }, 90);
    a4_put(ctx, sky, cm, .25);
    ctx.save(); cam(ctx, cm, .25);
    // kartpostal kalıbı: altın şafak bandı "kuşağın"da kalkar
    ctx.save(); ctx.clip(skyClip); a4_plateOff(ctx, 'gold', a4_rect(-200, 440, W + 200, HOR + 4), a4_lift(t, tKus), { a: .55 }); ctx.restore();
    // güneş: okra disk (ufkun ardında)
    const sun = new Path2D(); sun.arc(SUN[0], SUN[1], 92, 0, TAU);
    ctx.save(); ctx.clip(skyClip); knock(ctx, sun, '#EADCBC'); plate(ctx, 'ochre', sun, { a: .95 }); inkStroke(ctx, sun, 2.6, { a: .8 }); ctx.restore();
    ctx.restore();
    // güneşin önünden sürüklenen yarım ton duman (durağan katman, yalnız kayar)
    const smk0 = a4_L('E01-smk0', g => { a4_smokeCloud(g, SUN[0] - 40, SUN[1] - 30, 200, 3, 'ink', .42); a4_smokeCloud(g, SUN[0] + 220, SUN[1] - 120, 150, 5, 'ink', .34); a4_smokeCloud(g, SUN[0] - 300, SUN[1] - 150, 120, 6, 'ink', .3); }, 120);
    ctx.save(); cam(ctx, cm, .3); ctx.translate(lt * 16 - 30, -lt * 4); a4_put(ctx, smk0, null, 1, { mode: 'multiply' }); ctx.restore();
    // —— "savaş": tepelerde patlama (is yıldızı + yarım ton duman)
    if (t >= tSav) {
      const u = t - tSav, smk = a4_L('E01-smoke2', g => { a4_smokeCloud(g, BOOM[0], BOOM[1] - 170, 240, 7, 'ink', .55); a4_smokeCloud(g, BOOM[0] - 330, BOOM[1] - 70, 130, 9, 'ink', .42); }, 60);
      ctx.save(); cam(ctx, cm, .3); const k = .7 + .3 * E.out3(clamp(u / 1.2));
      ctx.translate(BOOM[0], BOOM[1]); ctx.scale(k, k); ctx.translate(-BOOM[0], -BOOM[1] - u * 14);
      ctx.globalAlpha = clamp(u / .25); a4_put(ctx, smk, null, 1, { mode: 'multiply' }); ctx.restore();
      ctx.save(); cam(ctx, cm, .3);
      a4_burst(ctx, BOOM[0], BOOM[1] - 30, 200, 31, E.outBack(clamp(a4_tf(u) / .2)));
      if (u > .3) a4_burst(ctx, BOOM[0] - 470, BOOM[1] + 4, 84, 37, E.outBack(clamp((a4_tf(u) - .3) / .16)), { ring: false });
      ctx.restore();
    }
    // —— uzak tepeler: haki taban; turkuaz kartpostal kalıbı "asıl"da kalkar
    const far = a4_L('E01-far', g => {
      const p = a4_groundPath(hills, HOR + 60);
      knock(g, p); plate(g, 'khaki', p, { a: .42 }); inkStroke(g, SP(hills, false, .6), 2.4);
      for (let i = 0; i < 26; i++) { const x = -100 + i * 80, y = a4_yAt(hills, x); inkStroke(g, PL([[x, y + 10], [x + 26, y + 6]], false), 1.4, { a: .35 }); }
    }, 90);
    a4_put(ctx, far, cm, .45);
    ctx.save(); cam(ctx, cm, .45);
    a4_plateOff(ctx, 'teal', a4_groundPath(hills, HOR + 60), a4_lift(t, tAsil), { a: .75 });
    // ince kırmızı cephe hattı: "okulu"ndan "savaş"a soldan sağa çizilir (tek kırmızı)
    a4_front(ctx, frontLine, ramp(t, tOkul, tSav + .3, E.io2), { w: 3.2, tooth: 7, step: 14, side: -1 });
    ctx.restore();
    // —— açık ova (ufuktan sırta)
    const plain = a4_L('E01-plain', g => {
      const pp = a4_groundPath(a4_ridgePts(-200, W + 200, HOR + 2, 4, 21, 10), H + 100);
      knock(g, pp); plate(g, 'ochre', pp, { a: .42 });
      for (let i = 0; i < 8; i++) { const y = HOR + 14 + i * i * 2.6; inkStroke(g, SP(a4_ridgePts(-200, W + 200, y, 2.5, 30 + i, 8), false), 1.2, { a: .2 + i * .03 }); }
    }, 90);
    a4_put(ctx, plain, cm, .6);
    // —— yürüyüş sırtı: koyu haki toprak, ufka yakınsayan tarla izleri (kâğıt kazıma)
    const mid = a4_L('E01-mid2', g => {
      const rp = a4_groundPath(ridge, H + 100);
      knock(g, rp); plate(g, 'khaki', rp); plate(g, 'ochre', rp, { a: .3 });
      g.save(); g.clip(rp);
      for (let i = -14; i <= 14; i++) { const xb = 960 + i * 150, q = PL([[960 + i * 9, 826], [xb, 1180]], false); cut(g, q, 2.2, { a: .22 + .12 * (i % 2 === 0) }); }
      g.restore();
      inkStroke(g, SP(ridge, false, .6), 3.6);
    }, 90);
    a4_put(ctx, mid, cm, .8);
    // yürüyen kol (sağa); tozu ayaklarında; pozlar ikişer karede
    ctx.save(); cam(ctx, cm, .8);
    a4_dust(ctx, lt, { box: [-60, 790, W + 60, 836], n: 70, seed: 4, wind: 38, rise: -3, col: 'ochre', a: .6, size: 3.4 });
    for (let i = 0; i < 14; i++) {
      const x = -260 + i * 150 + tf * 30 + (i % 3) * 11;
      if (x < -100 || x > W + 100) continue;
      a4_soldier(ctx, x, a4_yAt(ridge, x) + 4, 1.48, tf * 1.5 + i * .37);
    }
    ctx.restore();
    // —— ön toprak şeridi (en yakın katman)
    const fg = a4_L('E01-fg', g => {
      const fp = a4_groundPath(front, H + 100);
      knock(g, fp); plate(g, 'khaki', fp, { n: 2 }); plate(g, 'ink', fp, { a: .25 }); inkStroke(g, SP(front, false), 3.6);
      const r = rng(44); for (let i = 0; i < 40; i++) { const x = r() * W, y = 1022 + r() * 60; cut(g, PL([[x, y], [x + 20 + r() * 30, y - 2 - r() * 4]], false), 2, { a: .3 }); }
      for (let i = 0; i < 16; i++) { const x = 40 + i * 124 + r() * 60, y = a4_yAt(front, x) + 4; for (let k = 0; k < 6; k++) inkStroke(g, PL([[x + k * 4, y + 2], [x + k * 5 - 9 + r() * 18, y - 18 - r() * 16]], false), 2); }
    }, 90);
    a4_put(ctx, fg, cm, 1);
    // —— izleyici katmanı: uzun başlıklı künye sol üstte (sağ alttaki kuşak şeridiyle çakışmasın); SAVAŞ künye kalkınca basılır
    chapterCard(ctx, 'IV', 'ATEŞTE DÖVÜLEN KUŞAK', '1911 · CUMHURİYET’E 12 YIL', lt - .15, tSav - t0 - .35, { y: 64 });
    bigStamp(ctx, 'SAVAŞ', 600, 250, t - tSav - .06, st.end - tSav + .6, { size: 240, rot: -.035, ls: 10 });
  }, { tr: { type: 'press', dur: .8 }, post: { stone: .28, vig: 1 } });
}

// E02a · Kurmay haritası 1911: İtalya'nın çıkarması (is oklar), gönüllülerin rotası İstanbul → Mısır → Derne (kelimeye bağlı).
{
  const T0 = S('E02'), T1 = Wd('E02', 'sahte');
  // izdüşüm: boylam 9.5–37, enlem 28.6–42.4 → kâğıt üstünde
  const X0 = 120, X1 = 1800, Y0 = 92, Y1 = 1000;
  const gx = lon => X0 + (lon - 9.5) / 27.5 * (X1 - X0), gy = lat => Y0 + (42.4 - lat) / 13.8 * (Y1 - Y0), G = ([lo, la]) => [gx(lo), gy(la)];
  const africa = [[8, 37.3], [10.2, 37.2], [11.1, 37.05], [10.5, 36.4], [10.7, 35.7], [11.1, 35.2], [10.8, 34.7], [10.1, 33.9], [10.9, 33.6], [11.5, 33.1], [12.5, 32.8], [13.2, 32.9], [14.3, 32.6], [15.1, 32.35], [15.4, 31.9], [16.6, 31.2], [17.6, 30.9], [18.5, 30.4], [19.6, 30.3], [20.1, 31.1], [20.0, 32.1], [20.6, 32.55], [21.6, 32.9], [22.6, 32.78], [23.3, 32.5], [24.0, 32.05], [25.1, 31.7], [25.2, 31.5], [26.5, 31.4], [27.2, 31.35], [28.6, 30.95], [29.9, 31.2], [30.4, 31.48], [31.0, 31.58], [31.8, 31.52], [32.3, 31.26], [33.2, 31.1], [33.8, 31.13], [34.45, 31.5], [34.75, 32.05], [35.0, 32.8], [35.3, 33.3], [35.5, 33.9], [35.8, 34.45], [35.85, 35.4], [36.0, 35.9], [36.15, 36.55], [35.6, 36.6], [34.9, 36.75], [34.6, 36.8], [34.0, 36.3], [33.4, 36.1], [32.8, 36.05], [32.2, 36.5], [31.5, 36.7], [30.7, 36.88], [30.5, 36.5], [30.1, 36.25], [29.6, 36.2], [29.1, 36.6], [28.3, 36.8], [27.6, 36.75], [27.4, 37.05], [27.2, 37.5], [27.25, 37.9], [26.9, 38.3], [26.3, 38.3], [26.6, 38.6], [26.8, 39.0], [26.7, 39.4], [26.1, 39.5], [26.2, 40.0], [26.45, 40.2], [26.7, 40.4], [27.3, 40.4], [28.0, 40.4], [29.0, 40.4], [29.9, 40.75], [29.3, 40.85], [29.05, 41.05], [29.15, 41.25], [30.0, 41.15], [31.4, 41.3], [32.4, 41.8], [33.5, 42.0], [35.0, 42.1], [36.2, 41.7], [38.5, 41.4], [38.5, 27], [8, 27]];
  const balkan = [[18.2, 43.5], [19.3, 42.4], [19.4, 42.1], [19.5, 41.6], [19.45, 41.0], [19.4, 40.6], [19.3, 40.4], [19.6, 40.2], [20.0, 39.7], [20.2, 39.4], [20.7, 39.05], [21.1, 38.6], [21.3, 38.35], [21.6, 38.3], [21.1, 37.9], [21.6, 37.3], [21.7, 36.8], [22.4, 36.5], [22.8, 36.8], [23.2, 36.45], [23.1, 37.3], [22.8, 37.6], [23.4, 37.9], [23.7, 37.95], [24.0, 37.7], [24.05, 38.2], [23.6, 38.5], [23.0, 38.9], [22.8, 39.3], [23.3, 39.15], [22.9, 39.6], [22.6, 40.0], [22.65, 40.5], [22.95, 40.63], [23.4, 40.3], [23.7, 39.95], [23.9, 40.2], [24.3, 40.15], [23.9, 40.6], [24.4, 40.85], [25.2, 40.95], [25.9, 40.85], [26.05, 40.75], [26.3, 40.6], [26.2, 40.05], [26.6, 40.35], [26.9, 40.6], [27.5, 40.98], [28.0, 41.0], [28.6, 41.03], [29.0, 41.08], [29.1, 41.25], [28.6, 41.5], [28.0, 41.7], [27.9, 42.0], [27.9, 43.5]];
  const italy = [[11.0, 43.5], [12.0, 42.6], [12.6, 41.6], [13.3, 41.25], [13.9, 41.2], [14.3, 40.8], [14.9, 40.5], [15.2, 40.2], [15.6, 40.0], [15.8, 39.4], [16.1, 38.9], [15.65, 38.25], [15.85, 37.95], [16.1, 38.0], [16.55, 38.4], [16.6, 38.85], [17.15, 39.05], [17.1, 39.4], [16.5, 39.7], [16.9, 40.4], [17.5, 40.35], [18.1, 40.1], [18.5, 40.15], [18.0, 40.65], [17.2, 40.9], [16.3, 41.35], [15.9, 41.6], [16.1, 41.9], [15.4, 42.2], [14.6, 42.6], [14.0, 43.5]];
  const sicily = [[12.4, 38.0], [13.3, 38.2], [14.5, 38.05], [15.6, 38.25], [15.2, 37.5], [15.1, 36.9], [14.3, 36.8], [13.3, 37.2], [12.5, 37.65]];
  const crete = [[23.5, 35.6], [24.2, 35.55], [25.0, 35.4], [26.3, 35.3], [26.1, 35.0], [24.7, 35.05], [23.5, 35.25]];
  const cyprus = [[32.3, 35.05], [33.0, 35.35], [34.6, 35.65], [34.0, 35.0], [33.0, 34.6], [32.4, 34.75]];
  const L = (pts, sd) => a4_coast(pts.map(G), sd, 2.4);
  const lands = [L(africa, 1), L(balkan, 2), L(italy, 3), L(sicily, 4), L(crete, 5), L(cyprus, 6)];
  const IST = G([29.0, 41.04]), ALX = G([29.9, 31.2]), DER = G([22.62, 32.74]), TRA = G([13.2, 32.88]), BIN = G([20.07, 32.1]), TOB = G([23.96, 32.06]);
  const routeS = a4_sample([IST, G([28.3, 40.72]), G([26.6, 40.22]), G([25.9, 39.5]), G([25.7, 38.4]), G([26.2, 37.0]), G([27.3, 35.6]), G([28.7, 33.6]), G([29.6, 32.1]), ALX, G([28.9, 30.75]), G([27.2, 31.05]), G([25.5, 31.25]), G([24.3, 31.75]), G([23.4, 32.35]), DER], false, 6);
  const routeL = a4_cumLen(routeS);
  const fAlx = (() => { let best = 0, bd = 1e9; routeS.forEach((q, i) => { const d = Math.hypot(q[0] - ALX[0], q[1] - ALX[1]); if (d < bd) { bd = d; best = i; } }); return routeL[best] / routeL[routeL.length - 1]; })();
  const ROT = -.012, CX = 960, CY = 545;
  const base = () => a4_L('E02-map', g => {
    // masa (haki keçe) — sayfa dışı koyu
    paperBG(g); plate(g, 'khaki', a4_full(), { n: 2 }); plate(g, 'ink', a4_full(), { a: .22 });
    radialHT(g, 'ink', CX, CY, 700, 1300, 0, .3, { cell: 12, ang: 45, box: [-150, -150, W + 150, H + 150] });
    g.translate(CX, CY); g.rotate(ROT); g.translate(-CX, -CY);
    const sx = 64, sy = 40, sw = W - 128, sh_ = H - 80;
    const sh = a4_sheet(g, sx, sy, sw, sh_, 61);
    g.save(); g.clip(sh);
    // deniz: gravür tarama + kıyı çevresinde eş-derinlik halkaları; sonra kara
    a4_seaHatch(g, sx, sy, sx + sw, sy + sh_, { a: .16 });
    a4_ripples(g, lands, 1, { sea: '#D3C6A8' });
    for (const [i, Lp] of lands.entries()) { knock(g, Lp, P.paper); plate(g, 'ochre', Lp, { a: i === 2 || i === 3 ? .2 : .34 }); }
    // Trablusgarp vilayeti: haki ikinci baskı (Tunus sınırı → Mısır sınırı)
    g.save(); g.clip(lands[0]); plate(g, 'khaki', a4_rect(gx(11.55), gy(34), gx(25.05), gy(28.4)), { a: .32 }); g.restore();
    for (const Lp of lands) inkStroke(g, Lp, 2.6);
    // sınırlar: kesik is çizgisi
    g.save(); g.setLineDash([14, 8]);
    inkStroke(g, PL([G([11.55, 33.15]), G([11.4, 31.5]), G([10.2, 30.2]), G([9.6, 28.4])], false), 2, { a: .8 });
    inkStroke(g, PL([G([25.15, 31.6]), G([24.9, 30.4]), G([25.0, 28.4])], false), 2, { a: .8 });
    g.restore();
    // Nil ve demiryolları
    inkStroke(g, SP([G([30.6, 31.45]), G([31.0, 30.6]), G([31.25, 29.9]), G([31.2, 28.4])], false), 3.4);
    inkStroke(g, SP([G([31.6, 31.5]), G([31.1, 30.7])], false), 2.2);
    const rail = SP([G([29.9, 40.75]), G([30.5, 39.8]), G([31.2, 39.0]), G([32.5, 37.9]), G([34.2, 37.4]), G([35.3, 37.0])], false);
    inkStroke(g, rail, 6); inkStroke(g, rail, 3, { col: P.paper }); g.save(); g.setLineDash([12, 12]); inkStroke(g, rail, 3); g.restore();
    const railE = SP([ALX, G([30.6, 30.6]), G([31.25, 30.05])], false);
    inkStroke(g, railE, 6); inkStroke(g, railE, 3, { col: P.paper }); g.save(); g.setLineDash([12, 12]); inkStroke(g, railE, 3); g.restore();
    // dağ taraması (tırtıl)
    const lwf = px => px;
    [[[G([30.6, 37.25]), G([31.8, 37.35]), G([33.2, 37.2]), G([34.6, 37.45])], 20], [[G([20.8, 32.42]), G([21.6, 32.55]), G([22.3, 32.5])], 14], [[G([11.6, 32.0]), G([12.6, 31.95]), G([13.6, 32.05])], 14], [[G([23.9, 41.55]), G([24.9, 41.45]), G([25.9, 41.4])], 16], [[G([21.4, 39.8]), G([21.6, 39.2]), G([21.9, 38.7])], 14], [[G([15.9, 40.4]), G([16.2, 39.6]), G([16.3, 38.9])], 12]].forEach(([sp, Lm], i) => ridge(g, sp, Lm, lwf, 70 + i));
    // Osmanlıca soyut deniz ve bölge izleri
    for (const [lo, la, len_, h, sd] of [[22.0, 35.3, 210, 12, 1], [33.4, 41.75, 150, 10, 2], [31.5, 39.0, 140, 10, 3], [33.0, 30.0, 120, 9, 4], [17.4, 30.0, 150, 10, 5], [12.7, 39.6, 120, 9, 6], [21.6, 41.6, 120, 9, 7]]) scriptLine(g, gx(lo), gy(la), len_, h, 300 + sd, { a: .75 });
    // şehirler (lastik damga)
    for (const c of [IST, ALX, TRA, BIN, DER, TOB, G([31.25, 30.05]), G([27.15, 38.42]), G([35.5, 33.9])]) a4_city(g, c[0], c[1], 1, { r: 9 });
    // kartuş ve ölçek
    a4_cartouche(g, gx(32.6), gy(30.2) - 40, 250, 86, 91);
    for (let i = 0; i < 6; i++) { const q = a4_rect(gx(12) + i * 36, gy(29.3), gx(12) + i * 36 + 36, gy(29.3) + 12); i % 2 ? inkStroke(g, q, 1.6) : inkFill(g, q); }
    // odak: Trablusgarp–Mısır kıyısı dışında hafif haki örtü (en açık yer kıyı şeridi)
    for (const k of [1, 1.3, 1.65]) { const out = new Path2D(); out.rect(sx - 10, sy - 10, sw + 20, sh_ + 20); out.ellipse(gx(23.2), gy(32.4), 560 * k, 260 * k, -.04, 0, TAU);
      g.save(); g.clip(out, 'evenodd'); plate(g, 'khaki', a4_rect(sx - 10, sy - 10, sx + sw + 10, sy + sh_ + 10), { a: .075, flat: true }); g.restore(); }
    g.restore();
    a4_sheetFrame(g, sx, sy, sw, sh_, sh);
  }, 60);
  shot(T0, (ctx, st) => {
    setReg(402);
    paperBG(ctx);
    const lt = st.lt, t = st.t;
    const cm = { x: lerp(940, 1010, E.sine(st.p)), y: lerp(560, 600, E.sine(st.p)), z: lerp(1.0, 1.065, E.sine(st.p)) };
    a4_put(ctx, base(), cm, 1);
    ctx.save(); cam(ctx, cm, 1); ctx.translate(CX, CY); ctx.rotate(ROT); ctx.translate(-CX, -CY);
    const tI = Wd('E02', 'italya'), tC = Wd('E02', 'çıktı'), tG = Wd('E02', 'genç'), tGo = Wd('E02', 'gönüllü'), tK = Wd('E02', 'kimi');
    // İtalyan çıkarması: is oklar
    a4_arrow(ctx, [G([13.9, 37.0]), G([14.4, 35.6]), G([13.8, 34.3]), G([13.3, 33.25])], ramp(t, tI, tI + .9, E.io2), { w: 15 });
    a4_arrow(ctx, [G([17.6, 39.7]), G([18.6, 37.4]), G([19.5, 34.7]), G([20.0, 32.5])], ramp(t, tI + .25, tI + 1.15, E.io2), { w: 15 });
    a4_arrow(ctx, [G([18.9, 38.3]), G([20.8, 36.0]), G([22.2, 34.0]), G([22.6, 33.08])], ramp(t, tI + .5, tC, E.io2), { w: 13 });
    // köprübaşları (karşı taraf, is tarak) ve direniş hattı (kırmızı, Derne'nin gerisinde)
    const bh = ramp(t, tC, tC + .5, E.out2);
    for (const c of [TRA, BIN, DER]) a4_front(ctx, [[c[0] - 34, c[1] + 6], [c[0], c[1] + 20], [c[0] + 34, c[1] + 6]], bh, { col: 'ink', w: 5, tooth: 9, step: 13, side: 1 });
    // gönüllülerin rotası
    const rp = kf(t, [[tG, 0], [tGo + .3, fAlx, E.io2], [tK, 1, E.io2]]);
    const head = a4_route(ctx, routeS, routeL, rp, lt, { w: 6, dash: [20, 12] });
    a4_front(ctx, [[DER[0] - 70, DER[1] + 18], [DER[0] - 40, DER[1] + 58], [DER[0] + 10, DER[1] + 72], [DER[0] + 58, DER[1] + 50], [DER[0] + 82, DER[1] + 14]], ramp(t, tK - .35, tK + .45), { w: 7, tooth: 11, step: 16, side: -1 });
    if (head && rp < 1) { const ring = new Path2D(); ring.arc(head.x, head.y, 13, 0, TAU); knock(ctx, ring, '#F7F0DE'); inkStroke(ctx, ring, 3); const dot = new Path2D(); dot.arc(head.x, head.y, 5, 0, TAU); inkFill(ctx, dot); }
    // etiketler: kelimeyle
    const la = (t0) => E.out2(ramp(t, t0, t0 + .3));
    a4_tag(ctx, 'İTALYA', gx(15.9), gy(41.3), gx(15.6), gy(40.6), la(tI));
    a4_tag(ctx, 'TRABLUSGARP', gx(13.0) - 40, gy(31.2), TRA[0], TRA[1] + 10, la(Wd('E02', 'trablusgarpa')));
    a4_tag(ctx, 'İSTANBUL', IST[0] + 30, IST[1] - 34, IST[0] + 10, IST[1] - 8, la(tG));
    a4_tag(ctx, 'MISIR', ALX[0] + 40, ALX[1] + 74, ALX[0] + 6, ALX[1] + 12, la(tGo + .2));
    a4_tag(ctx, 'DERNE', DER[0] - 190, DER[1] - 60, DER[0] - 10, DER[1] - 8, la(tK - .2));
    ctx.restore();
    stamp(ctx, 'TRABLUSGARP · 1911', 132, 1000, lt - .2, st.d, { size: 34 });
  }, { tr: { type: 'press', dur: .5 }, post: { stone: .24 } });
}

// E02b · Derne, 1911: çöl dioraması. Kefiyeli genç kolağası Mustafa Kemal (30), arkada yerel gönüllüler, çadır, hurmalar, ak kasaba.
{
  const T0 = Wd('E02', 'sahte'), tCo = Wd('E02', 'çöle'), tHa = Wd('E02', 'halkla'), tDi = Wd('E02', 'direniş'), tOr = Wd('E02', 'örgütledi');
  const HOR = 640, dune1 = a4_ridgePts(-200, W + 200, 700, 22, 15, 14, 1.2), dune2 = a4_ridgePts(-200, W + 200, 846, 26, 19, 12, .9);
  const MK = { x: 1236, y: 420, s: 1.36 };
  shot(T0, (ctx, st) => {
    setReg(403);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt);
    const cm = { x: lerp(990, 950, E.sine(st.p)), y: 540, z: lerp(1.0, 1.04, E.sine(st.p)) };
    // gök + uzak tepe + kasaba (durağan)
    const sky = a4_L('E02b-sky', g => {
      paperBG(g);
      plate(g, 'ochre', a4_rect(-200, -200, W + 200, HOR + 10), { a: .3 });
      plate(g, 'ochre', a4_rect(-200, 300, W + 200, HOR + 10), { a: .18 });
      plate(g, 'ochre', a4_rect(-200, 470, W + 200, HOR + 10), { a: .14 });
      // gökte sepya yarım ton yalnız solda ve tepede (başın çevresi temiz)
      const clip = new Path2D(); clip.rect(-200, -200, W + 400, 520); clip.ellipse(MK.x, MK.y - 40, 330, 330, 0, 0, TAU);
      g.save(); g.clip(clip, 'evenodd'); radialHT(g, 'sepia', 200, -420, 380, 980, .17, 0, { cell: 12, box: [-160, -160, W + 160, 300] }); g.restore();
      const hills = a4_ridgePts(-200, W + 200, 610, 34, 11, 10, 1.1), hp = a4_groundPath(hills, HOR + 40);
      knock(g, hp); plate(g, 'khaki', hp, { a: .45 }); inkStroke(g, SP(hills, false, .6), 2.2);
      ridge(g, [[150, 600], [260, 584], [380, 592]], 14, px => px, 81); ridge(g, [[1500, 610], [1640, 596], [1760, 604]], 12, px => px, 82);
      a4_town(g, 80, 652, 1.0, 7);
      const flat = a4_groundPath(a4_ridgePts(-200, W + 200, HOR + 4, 3, 13, 8), H + 100); knock(g, flat); plate(g, 'ochre', flat, { a: .4 });
    }, 90);
    a4_put(ctx, sky, cm, .3);
    // uzak hurmalık
    const palmsFar = a4_L('E02b-palms', g => { for (const [x, sd, sc] of [[620, 1, .62], [700, 2, .7], [770, 3, .58], [1510, 4, .6], [1590, 5, .66]]) a4_palm(g, x, 668, sc, sd); }, 90);
    a4_put(ctx, palmsFar, cm, .45);
    // kumullar ve çadır
    const dunes = a4_L('E02b-dunes', g => {
      const d1 = a4_groundPath(dune1, H + 100); knock(g, d1); plate(g, 'ochre', d1, { a: .62 }); inkStroke(g, SP(dune1, false, .6), 3);
      g.save(); g.clip(d1); for (let i = 0; i < 26; i++) { const x = -100 + i * 84, y = a4_yAt(dune1, x); inkStroke(g, SP([[x, y + 14], [x + 40, y + 24], [x + 90, y + 20]], false), 1.4, { a: .4 }); } g.restore();
    }, 90);
    a4_put(ctx, dunes, cm, .6);
    ctx.save(); cam(ctx, cm, .6);
    // "direniş": sancak direğe çekilir
    a4_tent(ctx, 905, a4_yAt(dune1, 905) + 6, .92, { wave: Math.sin(tf * 7) * 3, raise: E.out3(ramp(t, tDi, tDi + .5)) });
    ctx.restore();
    // gönüllüler: kum üstünde; pozlar ikişer karede (deve adımlar, biri yürür)
    ctx.save(); cam(ctx, cm, .72);
    const yd = x => a4_yAt(dune1, x) + 34;
    a4_camel(ctx, 170, yd(170) - 4, 1.32, Math.floor(tf * 4) % 2);
    // "halkla": yerel gönüllüler birer birer basılır; "örgütledi": tüfekler omza (poz değişimi)
    const shoul = t > tOr + .1;
    [[318, 1, 1.62, 1, 1], [420, 0, 1.72, 2, 1], [520, 2, 1.66, 3, 1], [640, 0, 1.76, 4, -1], [1010, 1, 1.6, 5, -1]].forEach(([x, k, sc, sd, dr], i) =>
      a4_pressIn(ctx, ramp(t, tHa + i * .12, tHa + i * .12 + .35, E.lin), yd(x) - 190, yd(x) + 10, () => a4_local(ctx, x, yd(x), sc, shoul && k !== 2 ? 1 : k, { seed: sd, dir: dr })));
    // "çöle geçip": subay çöle girer (soldan)
    const wx = lerp(-80, 760, E.out2(ramp(t, tCo - .6, tHa + .8))) + tf * 8; a4_soldier(ctx, wx, yd(wx), 1.62, tf * 1.4, { rifle: true });
    ctx.restore();
    const fg = a4_L('E02b-fg', g => { const d2 = a4_groundPath(dune2, H + 100); knock(g, d2); plate(g, 'ochre', d2, { a: .9 }); plate(g, 'khaki', d2, { a: .18 }); inkStroke(g, SP(dune2, false, .6), 3.4); const r = rng(9); for (let i = 0; i < 50; i++) { const x = r() * W, y = 870 + r() * 200; inkStroke(g, PL([[x, y], [x + 16 + r() * 26, y - 3]], false), 1.6, { a: .35 }); } }, 90);
    a4_put(ctx, fg, cm, .9);
    a4_dust(ctx, lt, { box: [-60, 560, W + 60, 980], n: 90, seed: 8, wind: 120 + 160 * ramp(t, tCo - .2, tCo + .3) * (1 - ramp(t, tCo + .8, tCo + 1.6)), rise: -4, col: 'ochre', a: .5, size: 2.6 });
    // Mustafa Kemal: kefiye, haki setre; gönüllülere dönük (sola); göz kırpar
    ctx.save(); cam(ctx, cm, 1);
    const io = idleOffsets(tf, 3, .8), bl = blinkAt(t, 3);
    const o = { x: MK.x, y: MK.y + io.breath, s: MK.s, dir: -1 };
    bust(ctx, { ...o, coat: 'setre', col: 'khaki', w: 1.06, seed: 3, len: (H + 40 - MK.y) / MK.s, turn: .35 });
    head3q(ctx, { ...o, who: 'mk', gear: 'kefiye', light: 'front', lookAt: [470, 600], age: 30, tilt: io.head * .6, eyeOpen: .72 * (1 - bl) });
    ctx.restore();
    // en ön kum sırtı: büstü bel hizasında keser (Alagöz'deki masa gibi)
    const crest = a4_L('E02b-crest', g => {
      const pts = [[-200, 960], [300, 944], [760, 920], [1010, 872], [1180, 836], [1420, 826], [1700, 842], [2100, 866]];
      const cp = SP([...pts, [2100, H + 120], [-200, H + 120]], true, .7);
      knock(g, cp); plate(g, 'ochre', cp, { n: 2 }); plate(g, 'khaki', cp, { a: .25 }); inkStroke(g, SP(pts, false, .7), 4);
      g.save(); g.clip(cp); for (let i = 0; i < 9; i++) { const y = 860 + i * 26; inkStroke(g, SP([[-200, y + 70], [700, y + 40], [1300, y - 6], [2100, y + 10]], false), 1.6, { a: .3 }); }
      const r = rng(17); for (let i = 0; i < 70; i++) { const x = r() * W, y = 880 + r() * 200; cut(g, PL([[x, y], [x + 14 + r() * 20, y - 2]], false), 1.8, { a: .35 }); } g.restore();
    }, 90);
    a4_put(ctx, crest, cm, 1.08);
    stamp(ctx, 'DERNE · 1911', 120, 120, lt - .2, st.d, { size: 34 });
    nameTag(ctx, 1860, 860, 'MUSTAFA KEMAL', '30 yaşında', lt - .45, st.d - .2, { align: 'right', size: 56, sub: 38, bg: P.paperD });
  }, { tr: { type: 'cut', dur: 0 }, post: { stone: .26 } });
}

// E03b · Muhacir kafilesi: kağnılar ve kadınlar yolda; önde arkadan Zübeyde Hanım ve Makbule (çarşaflı, bohçalı); ufukta İstanbul.
{
  const T0 = Wd('E03', 'mustafa'), tAn = Wd('E03', 'annesi'), tIs = Wd('E03', 'istanbula'), tMu = Wd('E03', 'muhacir');
  const HOR = 612, road = a4_ridgePts(-200, W + 200, 742, 10, 51, 12, .8);
  shot(T0, (ctx, st) => {
    setReg(405);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt);
    const cm = { x: lerp(930, 1050, E.sine(st.p)), y: lerp(540, 600, ramp(t, tMu, tMu + 1.2)), z: lerp(1.0, 1.02, E.sine(st.p)) + .035 * ramp(t, tMu, tMu + 1.2) };
    // gök: tepede haki + is yarım ton (aşağı doğru söner), ufka doğru açılan okra bantlar; sağ ufuk en açık (İstanbul)
    const sky = a4_L('E03b-sky', g => {
      paperBG(g);
      for (const [y0, a] of [[-200, .2], [-200, .16], [180, .1], [330, .08]]) plate(g, 'ochre', a4_rect(-300, y0, W + 300, HOR + 6), { a });
      plate(g, 'khaki', a4_rect(-300, -200, W + 300, 180), { a: .3 });
      radialHT(g, 'ink', 960, -1300, 1300, 1560, .22, 0, { cell: 12, ang: 45, box: [-200, -200, W + 200, 300] });
      // ufuk ışığı: İstanbul üstünde kademeli açılan kâğıt (düz kademeler, yarım ton yok)
      // ufuk ışığı: İstanbul'un ardında alçak, düz, kademeli kâğıt bantları (kubbe değil)
      for (const [x0, h_, c] of [[1120, 64, '#E6DBC0'], [1280, 40, '#ECE2CB'], [1420, 20, '#F2EAD7']]) { const bd = PL(rough([[x0, HOR - h_], [W + 300, HOR - h_ - 4], [W + 300, HOR + 2], [x0 - 60, HOR + 2]], 2, x0)); g.save(); g.fillStyle = c; g.globalAlpha = .8; g.fill(bd); g.restore(); }
      for (const [x0, y0, w_, sd] of [[-120, 300, 980, 1], [560, 236, 760, 2], [1180, 382, 900, 3]]) { const cl = SP(rough([[x0, y0], [x0 + w_ * .3, y0 - 16], [x0 + w_ * .7, y0 - 12], [x0 + w_, y0 + 2], [x0 + w_ * .6, y0 + 12], [x0 + w_ * .2, y0 + 10]], 3, sd), true, .8); knock(g, cl, '#E8DDC4'); inkStroke(g, SP([[x0 + w_ * .08, y0 + 10], [x0 + w_ * .6, y0 + 13], [x0 + w_ * .95, y0 + 4]], false), 1.6, { a: .45 }); }
      a4_skyline(g, 1380, HOR + 4, .82, 6);
      const hills = a4_ridgePts(-200, 1360, 590, 18, 23, 9, 1), hp = SP([...hills, [1360, HOR + 4], [-200, HOR + 4]], true, .6);
      knock(g, hp); plate(g, 'khaki', hp, { a: .42 }); inkStroke(g, SP(hills, false), 2);
      const fl = a4_groundPath(a4_ridgePts(-200, W + 200, HOR + 2, 2, 52, 8), H + 100); knock(g, fl); plate(g, 'ochre', fl, { a: .42 });
      for (let i = 0; i < 6; i++) inkStroke(g, SP(a4_ridgePts(-200, W + 200, HOR + 16 + i * i * 4, 2, 60 + i, 8), false), 1.2, { a: .22 + i * .03 });
    }, 140);
    a4_put(ctx, sky, cm, .3);
    ctx.save(); cam(ctx, cm, .3); a4_tag(ctx, 'İSTANBUL', 1500, 520, 1600, 590, E.out2(ramp(t, tIs, tIs + .3)) * (1 - ramp(t, tMu + 1.3, tMu + 1.6)), { size: 24 }); ctx.restore();
    // yol (kağnı izleri) ve kafile
    const rd = a4_L('E03b-road', g => {
      const top = road.map(([x, y]) => [x, y - 20]), bot = road.map(([x, y]) => [x, y + 24]), rp = SP([...top, ...bot.slice().reverse()], true, .6);
      knock(g, rp); plate(g, 'ochre', rp, { a: .6 }); plate(g, 'khaki', rp, { a: .22 }); inkStroke(g, SP(top, false), 1.8, { a: .6 }); inkStroke(g, SP(bot, false), 1.8, { a: .7 });
      for (const dy of [-6, 10]) { g.save(); g.setLineDash([30, 14]); inkStroke(g, SP(road.map(([x, y]) => [x, y + dy]), false), 1.6, { a: .5 }); g.restore(); }
    }, 140);
    a4_put(ctx, rd, cm, .55);
    ctx.save(); cam(ctx, cm, .55);
    const ph = Math.floor(lt * 6) % 2;
    const troupe = [[0, 0], [1, 34], [2, 64], [-1, 0], [0, 40], [1, 70], [-1, 0], [2, 26], [0, 50]];
    for (let i = 0; i < troupe.length; i++) {
      const x = -260 + i * 236 + tf * 20, yy = a4_yAt(road, x) + 8;
      if (x < -260 || x > W + 300) continue;
      const [k, dx] = troupe[i];
      if (k < 0) { stampOxcart(ctx, x, yy, 1.5, ph); a4_dust(ctx, lt + i, { box: [x - 170, yy - 34, x + 20, yy + 4], n: 8, seed: 30 + i, wind: -30, rise: -6, col: 'ochre', a: .55, size: 4 }); }
      else { a4_migrant(ctx, x, yy, 2.1, k, (ph + i) % 2); a4_migrant(ctx, x + dx + 30, yy + 1, 2.0, (k + 1) % 3, (ph + i + 1) % 2); }
    }
    ctx.restore();
    // ön toprak
    const fg = a4_L('E03b-fg', g => {
      const ln = a4_ridgePts(-200, W + 200, 800, 8, 61, 10), gp = a4_groundPath(ln, H + 100); knock(g, gp); plate(g, 'ochre', gp, { a: .62 }); plate(g, 'khaki', gp, { a: .42 });
      inkStroke(g, SP(ln, false), 3);
      const r = rng(13); for (let i = 0; i < 80; i++) { const x = r() * (W + 200) - 100, y = 820 + r() * 260; inkStroke(g, PL([[x, y], [x + 14 + r() * 30, y - 2]], false), 1.6, { a: .35 }); }
      for (let i = 0; i < 16; i++) { const x = r() * (W + 200) - 100, y = 850 + r() * 220, q = SP(rough([[x - 8, y], [x - 2, y - 6], [x + 8, y - 4], [x + 9, y + 3], [x - 5, y + 4]], 1.4, i), true, .7); knock(g, q); plate(g, 'ochre', q, { a: .5 }); inkStroke(g, q, 2); }
    }, 140);
    a4_put(ctx, fg, cm, .9);
    // Zübeyde Hanım (önde, hafif eğik, ötede bohça) ve Makbule (arkasında, beride bohça); ikisi omuz omuza
    ctx.save(); cam(ctx, cm, 1);
    const wx = tf * 22, ph2 = Math.floor(lt * 5) % 2;
    for (const [x, y, w_] of [[986 + wx, 968, 220], [800 + wx, 992, 240]]) plate(ctx, 'khaki', SP([[x - 60, y + 2], [x + 64, y], [x - w_, y + 34], [x - w_ - 90, y + 30]], true, .6), { n: 2, a: .8 });
    a4_carsaf(ctx, 986 + wx, 968, 4.0, ph2, { stoop: .06, bundle: 'far', seed: 5 });
    a4_carsaf(ctx, 800 + wx, 992, 4.3, 1 - ph2, { bundle: 'near', seed: 8 });
    a4_dust(ctx, lt, { box: [600 + wx, 950, 1140 + wx, 1004], n: 22, seed: 71, wind: -40, rise: -8, col: 'ochre', a: .5, size: 3.4 });
    ctx.restore();
    stamp(ctx, 'SELANİK → İSTANBUL · 1912', 110, 116, lt - .15, st.d, { size: 32 });
    nameTag(ctx, 1860, 884, 'ZÜBEYDE HANIM VE MAKBULE', 'annesi ve kız kardeşi', t - tAn, st.end - tAn, { align: 'right', size: 48, sub: 32, bg: P.paperD });
  }, { tr: { type: 'cut', dur: 0 }, post: { stone: .26 } });
}

// —— Balkan kurmay haritası (E03a ve E04 ortak): boylam 17.8–31.1, enlem 38.9–44.5 ——
const a4_BK = (() => {
  const X0 = 110, X1 = 1810, Y0 = 70, Y1 = 1010;
  const gx = lon => X0 + (lon - 17.8) / 13.3 * (X1 - X0), gy = lat => Y0 + (44.5 - lat) / 5.6 * (Y1 - Y0), G = ([lo, la]) => [gx(lo), gy(la)];
  const main = [[16.5, 46], [17.4, 43.4], [18.1, 42.65], [18.55, 42.4], [19.0, 42.1], [19.35, 41.88], [19.45, 41.6], [19.45, 41.0], [19.4, 40.6], [19.3, 40.4], [19.6, 40.2], [20.0, 39.7], [20.2, 39.4], [20.7, 39.05], [21.0, 38.3], [21.2, 37.6], [23.2, 37.6], [23.2, 38.4], [22.95, 39.35], [23.3, 39.15], [22.9, 39.6], [22.6, 40.0], [22.65, 40.5], [22.95, 40.63], [23.2, 40.35], [23.0, 40.0], [23.35, 39.95], [23.6, 40.2], [23.75, 39.95], [23.95, 40.15], [24.4, 40.15], [24.0, 40.45], [23.9, 40.7], [24.4, 40.9], [25.2, 40.95], [25.9, 40.85], [26.05, 40.75], [26.3, 40.6], [26.2, 40.05], [26.6, 40.35], [26.9, 40.6], [27.5, 40.98], [28.0, 41.0], [28.6, 41.03], [29.0, 41.08], [29.1, 41.25], [28.6, 41.5], [28.0, 41.75], [27.9, 42.1], [27.6, 42.5], [27.9, 42.9], [27.7, 43.2], [28.6, 43.4], [28.6, 44.0], [28.8, 44.5], [29.6, 45.2], [30.2, 46]];
  const asia = [[25.6, 37.6], [26.3, 38.3], [26.6, 38.6], [26.8, 39.0], [26.7, 39.4], [26.1, 39.5], [26.2, 40.0], [26.45, 40.2], [26.7, 40.4], [27.3, 40.4], [28.0, 40.4], [29.0, 40.4], [29.9, 40.75], [29.3, 40.85], [29.05, 41.05], [29.15, 41.25], [30.0, 41.15], [31.4, 41.3], [32, 41.4], [32, 37.6]];
  const isl = [[[25.05, 39.96], [25.2, 40.02], [25.32, 39.98], [25.44, 39.92], [25.36, 39.86], [25.4, 39.79], [25.24, 39.8], [25.18, 39.86], [25.1, 39.84]], [[24.56, 40.78], [24.7, 40.8], [24.8, 40.7], [24.76, 40.6], [24.62, 40.56], [24.52, 40.66]], [[25.68, 40.2], [25.8, 40.24], [25.98, 40.21], [25.94, 40.13], [25.8, 40.1], [25.7, 40.13]], [[23.0, 39.02], [23.3, 38.9], [23.6, 38.76], [23.5, 38.66], [23.2, 38.78]]];
  const rum = [[19.35, 41.88], [19.45, 41.6], [19.45, 41.0], [19.4, 40.6], [19.3, 40.4], [19.6, 40.2], [20.0, 39.7], [20.2, 39.4], [20.7, 39.1], [21.2, 39.15], [21.7, 39.35], [22.1, 39.65], [22.6, 39.95], [22.65, 40.5], [22.95, 40.63], [23.2, 40.35], [23.0, 40.0], [23.35, 39.95], [23.6, 40.2], [23.75, 39.95], [23.95, 40.15], [24.4, 40.15], [24.0, 40.45], [23.9, 40.7], [24.4, 40.9], [25.2, 40.95], [25.9, 40.85], [26.05, 40.75], [26.3, 40.6], [26.2, 40.05], [26.6, 40.35], [26.9, 40.6], [27.5, 40.98], [28.0, 41.0], [28.6, 41.03], [29.0, 41.08], [29.1, 41.25], [28.6, 41.5], [28.0, 41.75], [27.95, 41.98], [27.4, 42.05], [26.8, 42.0], [26.3, 41.8], [25.6, 41.62], [24.6, 41.55], [23.9, 41.6], [23.3, 41.85], [22.9, 42.15], [22.4, 42.35], [21.9, 42.4], [21.5, 42.65], [21.2, 43.0], [20.8, 43.25], [20.35, 43.2], [20.0, 42.85], [19.75, 42.6], [19.6, 42.35]];
  const em = [[26.08, 40.74], [26.4, 41.0], [26.9, 41.22], [27.4, 41.4], [27.8, 41.55], [28.12, 41.62]].map(G);
  const lands = [a4_coast(main.map(G), 21, 2.2), a4_coast(asia.map(G), 22, 2.2), ...isl.map((q, i) => a4_coast(q.map(G), 23 + i, 1.4))];
  const rumP = SP(rough(rum.map(G), 1.6, 31), true, .4);
  const city = { SEL: G([22.95, 40.64]), IST: G([29.0, 41.03]), EDI: G([26.55, 41.67]), USK: G([21.43, 42.0]), MAN: G([21.33, 41.03]), ISK: G([19.5, 42.07]), YAN: G([20.85, 39.67]), SOF: G([23.32, 42.7]) };
  return { X0, X1, Y0, Y1, gx, gy, G, lands, rumP, em, city };
})();
// harita zemini (durağan): masa, kâğıt, deniz taraması, karalar (açık), dağlar, demiryolu, sınırlar, şehirler, kartuş
function a4_balkanBase(g) {
  const { G, lands, city } = a4_BK, CX = 960, CY = 540;
  paperBG(g); plate(g, 'khaki', a4_full(), { n: 2 }); plate(g, 'ink', a4_full(), { a: .22 });
  radialHT(g, 'ink', CX, CY, 720, 1300, 0, .3, { cell: 12, ang: 45, box: [-150, -150, W + 150, H + 150] });
  g.translate(CX, CY); g.rotate(.01); g.translate(-CX, -CY);
  const sx = 56, sy = 34, sw = W - 112, sh_ = H - 68, sh = a4_sheet(g, sx, sy, sw, sh_, 62);
  g.save(); g.clip(sh);
  a4_seaHatch(g, sx, sy, sx + sw, sy + sh_, { a: .16 });
  a4_ripples(g, lands, 1, { sea: '#D3C6A8' });
  for (const Lp of lands) { knock(g, Lp, P.paper); plate(g, 'ochre', Lp, { a: .2 }); }
  // Anadolu: Osmanlı toprağı (haki + okra, Rumeli'yle aynı baskı)
  plate(g, 'khaki', lands[1], { a: .5 }); plate(g, 'ochre', lands[1], { a: .25 });
  // dağ taraması
  [[[G([19.9, 42.4]), G([20.4, 41.9]), G([20.6, 41.3])], 16], [[G([21.6, 41.6]), G([22.2, 41.4]), G([22.6, 41.1])], 14], [[G([23.9, 41.75]), G([24.8, 41.62]), G([25.7, 41.66])], 18], [[G([22.6, 42.9]), G([23.6, 42.6]), G([24.6, 42.65]), G([25.6, 42.75])], 18], [[G([21.3, 39.9]), G([21.6, 39.5]), G([21.9, 39.2])], 14], [[G([27.2, 42.0]), G([27.8, 41.9])], 12], [[G([29.6, 40.2]), G([30.6, 40.1])], 12]].forEach(([sp, L], i) => ridge(g, sp, L, px => px, 90 + i));
  // nehirler: Vardar, Meriç, Tuna
  inkStroke(g, SP([G([21.4, 42.2]), G([21.8, 41.7]), G([22.3, 41.3]), G([22.6, 40.8]), G([22.75, 40.6])], false), 3);
  inkStroke(g, SP([G([24.8, 42.15]), G([25.6, 42.05]), G([26.4, 41.75]), G([26.6, 41.3]), G([26.1, 40.75])], false), 3);
  inkStroke(g, SP([G([17.8, 44.6]), G([20.5, 44.6]), G([22.6, 44.1]), G([24.5, 43.7]), G([26.0, 43.9]), G([27.6, 44.1]), G([28.2, 44.6])], false), 4);
  // demiryolu: Selanik–Üsküp, Selanik–Dedeağaç–İstanbul (Şark Demiryolu)
  for (const pts of [[city.SEL, G([22.3, 41.3]), G([21.8, 41.7]), city.USK], [city.SEL, G([23.6, 41.1]), G([24.5, 41.15]), G([25.6, 40.9]), G([26.2, 41.2]), G([26.55, 41.6]), G([27.2, 41.4]), G([28.0, 41.15]), city.IST]]) {
    const rl = SP(pts, false); inkStroke(g, rl, 6); inkStroke(g, rl, 3, { col: P.paper }); g.save(); g.setLineDash([12, 12]); inkStroke(g, rl, 3); g.restore();
  }
  for (const Lp of lands) inkStroke(g, Lp, 2.6);
  // komşu devlet sınırları (kesik) ve Osmanlıca adları
  g.save(); g.setLineDash([14, 9]);
  inkStroke(g, SP([G([22.6, 39.95]), G([22.1, 39.65]), G([21.2, 39.15]), G([20.7, 39.1])], false), 2.2, { a: .8 });
  inkStroke(g, SP([G([27.95, 41.98]), G([26.8, 42.0]), G([25.6, 41.62]), G([23.9, 41.6]), G([22.9, 42.15]), G([21.9, 42.4]), G([21.2, 43.0]), G([20.35, 43.2]), G([19.75, 42.6]), G([19.35, 41.88])], false), 2.2, { a: .8 });
  inkStroke(g, SP([G([22.5, 44.3]), G([22.6, 43.4]), G([22.4, 42.35])], false), 2, { a: .6 });
  g.restore();
  for (const [lo, la, len_, sd] of [[25.6, 43.0, 160, 1], [21.9, 43.5, 140, 2], [19.7, 43.0, 90, 3], [22.4, 39.25, 120, 4], [25.2, 39.5, 150, 5], [29.6, 42.6, 170, 6], [30.4, 39.4, 130, 7]]) scriptLine(g, a4_BK.gx(lo), a4_BK.gy(la), len_, 10, 400 + sd, { a: .75 });
  for (const k of ['IST', 'EDI', 'USK', 'MAN', 'ISK', 'YAN', 'SOF']) a4_city(g, city[k][0], city[k][1], 1, { r: 9 });
  a4_cartouche(g, a4_BK.gx(29.2), a4_BK.gy(39.65) - 30, 240, 82, 93);
  for (let i = 0; i < 6; i++) { const q = a4_rect(a4_BK.gx(27.8) + i * 36, a4_BK.gy(39.05), a4_BK.gx(27.8) + i * 36 + 36, a4_BK.gy(39.05) + 12); i % 2 ? inkStroke(g, q, 1.6) : inkFill(g, q); }
  g.restore();
  a4_sheetFrame(g, sx, sy, sw, sh_, sh);
}
// Rumeli dolgusu (canlı): front = süpürme cephesinin ekran x'i (−∞: dolu, +∞: yalnız Enez–Midye doğusu kalır)
function a4_rumeliFill(ctx, front, seed = 5) {
  const { rumP, em, gx, gy } = a4_BK;
  const keep = new Path2D();
  if (front < W + 400) {
    // süpürme: cephenin doğusu (saat yönünde), kenarı silgi gibi kırık
    const r = rng(seed), pts = [];
    for (let y = -100; y <= H + 100; y += 40) pts.push([front + (r() - .5) * 26 + Math.sin(y * .011) * 30, y]);
    keep.moveTo(pts[0][0], pts[0][1]); keep.lineTo(W + 600, -100); keep.lineTo(W + 600, H + 100);
    for (let i = pts.length - 1; i >= 0; i--) keep.lineTo(pts[i][0], pts[i][1]);
    keep.closePath();
  }
  // Enez–Midye doğusu (saat yönünde)
  keep.moveTo(em[0][0], em[0][1]); for (const q of em) keep.lineTo(q[0], q[1]);
  keep.lineTo(em[em.length - 1][0], -400); keep.lineTo(W + 600, -400); keep.lineTo(W + 600, H + 400); keep.lineTo(em[0][0], H + 400); keep.closePath();
  ctx.save(); ctx.clip(keep);
  plate(ctx, 'khaki', rumP, { a: .5 }); plate(ctx, 'ochre', rumP, { a: .25 });
  ctx.save(); ctx.clip(rumP); txt(ctx, 'RUMELİ', gx(22.9), gy(41.35), FONT.mono(50), { ls: 22, align: 'center', col: P.ink, a: .8 }); ctx.restore();
  ctx.restore();
  // eski sınır: kesik is (silinince hayalet olarak kalır)
  ctx.save(); ctx.setLineDash([10, 8]); inkStroke(ctx, rumP, 2.2, { a: .55 }); ctx.restore();
}

// E03a · Balkan Savaşı 1912: dört ok (Karadağ, Sırbistan, Bulgaristan, Yunanistan); Rumeli dolgusu batıdan doğuya silinir;
// Selanik "teslim edildi"de söner; sonunda Enez–Midye hattı (kırmızı tarak).
{
  const T0 = S('E03');
  const { G, city, em } = a4_BK;
  shot(T0, (ctx, st) => {
    setReg(404);
    paperBG(ctx);
    const lt = st.lt, t = st.t;
    const cm = { x: kf(t, [[T0, 930], [Wd('E03', 'selanik'), 900], [Wd('E03', 'teslim'), 960], [T0 + st.d, 1010]]), y: lerp(560, 600, E.sine(st.p)), z: lerp(1.0, 1.07, E.sine(st.p)) };
    a4_put(ctx, a4_L('BK-base', a4_balkanBase, 60), cm, 1);
    ctx.save(); cam(ctx, cm, 1); ctx.translate(960, 540); ctx.rotate(.01); ctx.translate(-960, -540);
    const tB = Wd('E03', 'balkan'), tS = Wd('E03', 'selanik'), tT = Wd('E03', 'teslim'), tE = Wd('E03', 'edildi');
    // süpürme cephesi: Selanik'e "teslim"de varır, sonra Enez'i geçer
    const fx = kf(t, [[tS - .2, -200], [tT, city.SEL[0] + 40, E.io2], [T0 + st.d - .2, W + 500, E.in2]]);
    a4_rumeliFill(ctx, fx);
    // oklar (is): Karadağ, Sırbistan, Bulgaristan (iki kol), Yunanistan
    a4_arrow(ctx, [G([19.25, 42.85]), G([19.45, 42.45]), G([19.5, 42.18])], ramp(t, tB, tB + .7, E.io2), { w: 13 });
    a4_arrow(ctx, [G([21.7, 43.55]), G([21.6, 42.9]), G([21.45, 42.15])], ramp(t, tB + .15, tB + .85, E.io2), { w: 15 });
    a4_arrow(ctx, [G([26.0, 42.85]), G([26.4, 42.3]), G([26.55, 41.82])], ramp(t, tB + .3, tB + 1.0, E.io2), { w: 15 });
    a4_arrow(ctx, [G([27.0, 42.85]), G([27.6, 42.2]), G([27.9, 41.5]), G([28.3, 41.2])], ramp(t, tB + .45, tB + 1.2, E.io2), { w: 13 });
    a4_arrow(ctx, [G([22.1, 39.2]), G([22.45, 39.85]), G([22.8, 40.45])], ramp(t, tB + .3, tB + 1.1, E.io2), { w: 15 });
    // Selanik: vurgulanır, "teslim edildi"de söner
    const on = 1 - ramp(t, tT, tE + .2, E.in2), pulse = ramp(t, tS, tS + .5, E.out3) * (1 - ramp(t, tT, tE, E.io2));
    if (pulse > 0) { const rg = new Path2D(); rg.arc(city.SEL[0], city.SEL[1], 16 + 30 * pulse, 0, TAU); inkStroke(ctx, rg, 3, { a: (1 - pulse * .6) }); }
    a4_city(ctx, city.SEL[0], city.SEL[1], on, { r: 13 });
    // Enez–Midye hattı (kırmızı tarak, Türk tarafı doğu)
    a4_front(ctx, em, ramp(t, T0 + st.d - 1.0, T0 + st.d - .15, E.io2), { w: 7, tooth: 12, step: 17, side: -1 });
    // etiketler
    a4_tag(ctx, 'İSTANBUL', city.IST[0] - 70, city.IST[1] + 70, city.IST[0], city.IST[1] + 10, E.out2(ramp(lt, .3, .6)));
    a4_tag(ctx, 'SELANİK', city.SEL[0] - 250, city.SEL[1] + 86, city.SEL[0] - 8, city.SEL[1] + 12, E.out2(ramp(t, tS, tS + .3)));
    // "şehirde çarpışma olmadan": Selanik'in çevresinde kırık savunma halkası (silah sesi yok); "teslim": tarih etiketi
    const tCa = Wd('E03', 'çarpışma');
    if (t > tCa) { ctx.save(); ctx.setLineDash([6, 9]); const rg = new Path2D(); rg.arc(city.SEL[0], city.SEL[1], 46, 0, TAU * E.out2(ramp(t, tCa, tCa + .5))); inkStroke(ctx, rg, 2.6, { a: on }); ctx.restore(); }
    a4_tag(ctx, '8 KASIM 1912 · TESLİM', city.SEL[0] + 40, city.SEL[1] - 70, city.SEL[0] + 10, city.SEL[1] - 14, E.out2(ramp(t, tT, tT + .3)), { size: 22 });
    ctx.restore();
    stamp(ctx, 'BALKAN SAVAŞI · 1912', 120, 1004, lt - .2, st.d, { size: 34 });
  }, { tr: { type: 'press', dur: .6 }, post: { stone: .24 } });
}

// —— duvardaki Balkan haritası (E04): Rumeli silinmiş, eski sınır hayalet, Enez–Midye kırmızı. sc: ölçek, (cx,cy): kâğıt merkezi
function a4_wallMap(ctx, sc, cx, cy, o = {}) {
  ctx.save(); ctx.translate(cx, cy); ctx.scale(sc, sc); ctx.translate(-960, -540);
  ctx.save(); ctx.translate(960, 540); ctx.rotate(.01); ctx.translate(-960, -540);
  const sheet = a4_rect(46, 26, W - 46, H - 26);
  // kâğıdın duvara gölgesi
  plate(ctx, 'ink', a4_rect(46 + 18, 26 + 22, W - 46 + 18, H - 26 + 22), { a: .35 });
  ctx.save(); ctx.clip(sheet); ctx.restore();
  ctx.restore();
  ctx.save(); ctx.translate(960, 540); ctx.rotate(.01); ctx.translate(-960, -540); ctx.clip(a4_rect(50, 30, W - 50, H - 30)); ctx.translate(960, 540); ctx.rotate(-.01); ctx.translate(-960, -540);
  a4_put(ctx, a4_L('BK-base', a4_balkanBase, 60), null, 1);
  ctx.translate(960, 540); ctx.rotate(.01); ctx.translate(-960, -540);
  a4_rumeliFill(ctx, W + 1000);
  a4_front(ctx, a4_BK.em, 1, { w: 7, tooth: 12, step: 17, side: -1 });
  if (o.after) o.after(ctx);
  ctx.restore();
  ctx.restore();
}
// kâğıt yırtığı: üst kenardan aşağı ilerleyen kırık yarık (içi is, kenarı kâğıt lifli); p: 0..1
function a4_tear(ctx, pts, p, seed, wMax = 22) {
  if (p <= 0) return;
  const smp = a4_sample(pts, false, 14), cl = a4_cumLen(smp), q = a4_partial(smp, cl, cl[cl.length - 1] * clamp(p)), r = rng(seed);
  if (q.length < 2) return;
  const L = [], R = [], n = q.length;
  for (let i = 0; i < n; i++) {
    const a = q[Math.min(n - 1, i + 1)], b = q[Math.max(0, i - 1)], an = Math.atan2(a[1] - b[1], a[0] - b[0]) + PI / 2;
    const u = i / Math.max(1, n - 1), w = (wMax * (1 - u * .85) + 2) * (.7 + r() * .6), j = (r() - .5) * 7;
    L.push([q[i][0] + Math.cos(an) * (w / 2 + j), q[i][1] + Math.sin(an) * (w / 2 + j)]);
    R.push([q[i][0] - Math.cos(an) * (w / 2 - j * .5), q[i][1] - Math.sin(an) * (w / 2 - j * .5)]);
  }
  const gap = PL([...L, ...R.reverse()]);
  // lifli kâğıt kenarı (yırtılan kâğıdın beyaz iç yüzü)
  inkStroke(ctx, gap, 9, { col: '#F4EDDC' });
  plate(ctx, 'khaki', gap, { n: 2 }); inkFill(ctx, gap, { a: .78 });
  inkStroke(ctx, PL(L, false), 1.6, { a: .8 }); inkStroke(ctx, PL(R.slice().reverse(), false), 1.6, { a: .8 });
}
const a4_KUSAK = {
  // ¾ büst sırası; yaşlar yıla göre (doğum: MK 1881, Karabekir 1882, İsmet 1884, Fevzi 1876, Ali Fuat 1882)
  born: { mk: 1881, karabekir: 1882, ismet: 1884, fevzi: 1876, alifuat: 1882 },
  seed: { mk: 3, karabekir: 11, ismet: 5, fevzi: 7, alifuat: 13 },
  short: { mk: 'MUSTAFA KEMAL', karabekir: 'KARABEKİR', ismet: 'İSMET', fevzi: 'FEVZİ', alifuat: 'ALİ FUAT' },
};

// E04a · (yorum) Kuşak şeridi, kaybolan Rumeli haritasının önünde. "yara": harita Rumeli'den yırtılır.
{
  const T0 = S('E04'), tY = Wd('E04', 'yara'), tO = Wd('E04', 'ortak');
  const order = ['alifuat', 'karabekir', 'mk', 'ismet', 'fevzi'], Y = 1912;
  shot(T0, (ctx, st) => {
    setReg(406);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt);
    const cm = { x: lerp(960, 930, E.sine(st.p)), y: lerp(540, 520, E.sine(st.p)), z: lerp(1.0, 1.05, E.sine(st.p)) };
    const wall = a4_L('E04-wall', g => { paperBG(g); plate(g, 'khaki', a4_full(), { n: 2 }); plate(g, 'ochre', a4_full(), { a: .3 }); plate(g, 'ink', a4_full(), { a: .18 }); radialHT(g, 'ink', 900, 380, 640, 1300, 0, .3, { cell: 12, ang: 45, box: [-150, -150, W + 150, H + 150] }); }, 90);
    a4_put(ctx, wall, cm, .5);
    // yırtık: üst kenardan Selanik'e, oradan Ege'ye
    const { G } = a4_BK, tearPts = [G([21.9, 44.6]), G([22.2, 43.6]), G([21.8, 42.8]), G([22.4, 41.9]), G([22.7, 41.2]), G([22.95, 40.64]), G([23.3, 40.0]), G([23.6, 39.3])];
    const tp = ramp(t, tO, tY + .5, E.io2);
    ctx.save(); cam(ctx, cm, .75);
    a4_wallMap(ctx, .66, 960, 360, { after: c => a4_tear(c, tearPts, tp, 77, 34) });
    ctx.restore();
    // kuşak şeridi: beş büst, aynı ölçek, Rumeli'ye bakar; "bu kuşağı"nda soldan sağa basılarak gelir
    ctx.save(); cam(ctx, cm, 1);
    const look = [700, 300], tBu = Wd('E04', 'kuşağı') - .5;
    order.forEach((who, i) => {
      const x = 330 + i * 318, y = 690 + (i % 2) * 6, io = idleOffsets(tf, i * 3 + 1, .6);
      a4_pressIn(ctx, ramp(t, tBu + i * .22, tBu + i * .22 + .45, E.lin), y - 130, H, () =>
        a4_officer(ctx, { x, y: y + io.breath, s: 1.02, dir: -1, who, age: Y - a4_KUSAK.born[who], seed: a4_KUSAK.seed[who], len: (H + 40 - y) / 1.02, lookAt: look, tilt: io.head * .5, turn: .25, w: 1.02 }));
    });
    ctx.restore();
    order.forEach((who, i) => a4_tag(ctx, a4_KUSAK.short[who] + ' · ' + (Y - a4_KUSAK.born[who]), 330 + i * 318 - 112, 1040, null, null, E.out2(ramp(t, tBu + .5 + i * .22, tBu + .8 + i * .22)) * (1 - ramp(t, tO + .6, tO + 1)), { size: 22 }));
  }, { tr: { type: 'clay', dur: .8 }, post: { stone: .26 } });
}

// E04b · "Rumeli'yi kaybeden bu insanlar, bir gün yeni bir memleket kuracaktı": üç büst doğuya döner;
// "yeni bir memleket"te Anadolu dolgusu baskı merdanesiyle yeniden basılır.
{
  const T0 = Wd('E04', 'rumeliyi'), tY = Wd('E04', 'yeni'), tK = Wd('E04', 'kuracaktı');
  const order = [['karabekir', 250], ['mk', 590], ['ismet', 930]], Y = 1912;
  shot(T0, (ctx, st) => {
    setReg(407);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt);
    const cm = { x: lerp(960, 1000, E.sine(st.p)), y: 540, z: lerp(1.02, 1.07, E.sine(st.p)) };
    const wall = a4_L('E04-wall', g => { paperBG(g); plate(g, 'khaki', a4_full(), { n: 2 }); plate(g, 'ochre', a4_full(), { a: .3 }); plate(g, 'ink', a4_full(), { a: .18 }); radialHT(g, 'ink', 900, 380, 640, 1300, 0, .3, { cell: 12, ang: 45, box: [-150, -150, W + 150, H + 150] }); }, 90);
    a4_put(ctx, wall, cm, .5);
    const { lands, gx } = a4_BK;
    // Anadolu yeniden basılır: merdane soldan sağa
    const rx = kf(t, [[tY, gx(25.6)], [tK + .2, gx(32), E.io2]]);
    ctx.save(); cam(ctx, cm, .75);
    a4_wallMap(ctx, 1.3, 640, 250, { after: c => {
      if (t < tY) return;
      c.save(); c.clip(lands[1]); c.save(); c.clip(a4_rect(-500, -500, rx, H + 500));
      const [dx, dy] = [(1 - ramp(t, tY, tK + .4)) * 10, 0];
      c.translate(dx, dy); plate(c, 'khaki', lands[1], { a: .32 }); plate(c, 'ochre', lands[1], { a: .3 }); c.restore();
      inkStroke(c, PL([[rx, -200], [rx, H + 200]], false), 3.6, { a: .7 * (1 - ramp(t, tK, tK + .3)) });
      c.restore();
      inkStroke(c, lands[1], 2.6);
      a4_tag(c, 'ANADOLU', gx(26.9), a4_BK.gy(39.55), null, null, E.out2(ramp(t, Wd('E04', 'memleket'), Wd('E04', 'memleket') + .3)), { size: 30, bg: P.paper });
    } });
    ctx.restore();
    ctx.save(); cam(ctx, cm, 1);
    order.forEach(([who, x], i) => {
      const y = 720 + (i % 2) * 8, io = idleOffsets(tf, i * 5 + 2, .6), s = 1.2;
      a4_officer(ctx, { x, y: y + io.breath, s, dir: 1, who, age: Y - a4_KUSAK.born[who], seed: a4_KUSAK.seed[who], len: (H + 40 - y) / s, lookAt: [1500, 380], tilt: io.head * .5, turn: .25, w: 1.02 });
    });
    ctx.restore();
  }, { tr: { type: 'cut', dur: 0 }, post: { stone: .26 } });
}

// E05a · Çanakkale 1915: turkuaz deniz, zırhlılar, Arıburnu sırtları ve siperler; kelimeyle patlamalar ve etiketler;
// siperdeki süngü sırası birer birer boşalır (kayıp, kansız).
{
  const T0 = S('E05'), tA = Wd('E05', 'arıburnunda'), tN = Wd('E05', 'anafartalarda');
  const HOR = 560, crest = [[640, 760], [760, 640], [880, 560], [1000, 470], [1120, 420], [1260, 392], [1400, 410], [1520, 460], [1640, 500], [1800, 520], [2100, 540]];
  const trench = crest.map(([x, y]) => [x, y + 24]);
  shot(T0, (ctx, st) => {
    setReg(408);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt);
    const sk = shake(t, tA, 7, 6), sk2 = shake(t, tN, 6, 6);
    const cm = { x: lerp(940, 1000, E.sine(st.p)), y: 540, z: lerp(1.0, 1.045, E.sine(st.p)), sx: sk[0] + sk2[0], sy: sk[1] + sk2[1] };
    const bg = a4_L('E05a-bg', g => {
      paperBG(g);
      for (const [y0, a] of [[-200, .22], [220, .14], [380, .12]]) plate(g, 'ochre', a4_rect(-300, y0, W + 300, HOR + 4), { a });
      radialHT(g, 'ink', 300, -1100, 1100, 1420, .22, 0, { cell: 12, ang: 45, box: [-200, -200, 1100, 300] });
      // deniz: turkuaz, ufukta koyu bant, statik yarım ton
      const sea = a4_rect(-300, HOR, W + 300, H + 300);
      knock(g, sea); plate(g, 'teal', sea, { a: .78 }); plate(g, 'teal', a4_rect(-300, HOR, W + 300, HOR + 26), { a: .6 });
      radialHT(g, 'teal', 400, 1300, 400, 900, .5, 0, { cell: 12, box: [-200, HOR + 30, 1000, H + 100] });
      // karşı kıyı (uzak, haki)
      const far = SP([[1160, HOR + 2], [1300, 520], [1500, 500], [1700, 516], [2100, 506], [2100, HOR + 6]], true, .6); knock(g, far); plate(g, 'khaki', far, { a: .4 }); inkStroke(g, far, 1.8, { a: .7 });
      // sırtlar: uzaktan yakına üç katman
      const r2 = [[560, H + 100], [700, 700], [820, 600], [940, 520], [1060, 450], [1180, 410], [1300, 384], [1420, 404], [1540, 450], [1660, 490], [1800, 512], [2100, 530], [2100, H + 100]];
      const rp = SP(crest.concat([[2100, H + 100], [560, H + 100]]), true, .6);
      knock(g, rp); plate(g, 'khaki', rp); plate(g, 'ochre', rp, { a: .35 });
      g.save(); g.clip(rp);
      for (let i = 0; i < 70; i++) { const x = 620 + i * 22, y = a4_yAt(crest, x); inkStroke(g, PL([[x, y + 30], [x - 18, y + 120 + (i % 5) * 30]], false), 1.4, { a: .45 }); }
      // eş yükselti çizgileri ve çalılar
      for (let k = 1; k < 6; k++) inkStroke(g, SP(crest.map(([x, y]) => [x + k * 14, y + k * 70]), false, .6), 1.5, { a: .35 });
      const rr = rng(77); for (let i = 0; i < 46; i++) { const x = 700 + rr() * 1300, y = a4_yAt(crest, x) + 60 + rr() * 380; const b = SP(rough([[x - 14, y], [x - 8, y - 12], [x + 4, y - 15], [x + 14, y - 6], [x + 12, y + 2]], 2, i), true, .8); knock(g, b); plate(g, 'khaki', b, { n: 2 }); inkStroke(g, b, 1.8); }
      g.restore();
      inkStroke(g, SP(crest, false, .6), 3.2);
      // siper: kırık hendek + kum torbası üstü
      inkStroke(g, SP(trench, false, .6), 10); inkStroke(g, SP(trench.map(([x, y]) => [x, y - 7]), false, .6), 2.4, { col: P.paperD });
      // tel örgü (sırtın önünde)
      g.save(); g.translate(0, 0); a4_wire(g, 900, 1500, 560, 5, { h: 26, step: 90 }); g.restore();
      // sahil: kum şeridi
      const beach = SP([[-300, 900], [300, 884], [600, 868], [760, 900], [760, H + 300], [-300, H + 300]], true, .6);
      knock(g, beach); plate(g, 'ochre', beach, { a: .55 }); inkStroke(g, SP([[-300, 900], [300, 884], [600, 868], [760, 900]], false), 2.6);
    }, 90);
    a4_put(ctx, bg, cm, .8);
    ctx.save(); cam(ctx, cm, .8);
    // dalga çizgileri (kazıma, kayar)
    for (let i = 0; i < 9; i++) { const y = HOR + 40 + i * 26 + i * i * 2, off = ((lt * 18 + i * 37) % 120); const p = new Path2D(); for (let x = -200 - off; x < 760; x += 120) { p.moveTo(x, y); p.quadraticCurveTo(x + 30, y - 5, x + 60, y); } cut(ctx, p, 2, { a: .55 }); }
    // zırhlılar ve namlu ateşi
    for (const [x, y, s, k] of [[140, HOR + 2, .9, 0], [430, HOR + 4, 1.1, 1], [700, HOR + 1, .75, 2]]) {
      a4_ship(ctx, x + Math.sin(lt * .6 + k) * 3, y, s, { dir: 1 });
      const fl = (lt * 1.3 + k * .37) % 1.6; if (fl < .12) a4_burst(ctx, x + 100 * s, y - 20 * s, 26, 50 + k, 1, { ring: false });
      ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = rgba(P.khaki, .5); for (let j = 0; j < 5; j++) { ctx.beginPath(); ctx.ellipse(x - 20 * s - j * 28 - (lt * 12 % 28), y - 50 * s - j * 6, 14 + j * 4, 8 + j * 2, 0, 0, TAU); ctx.fill(); } ctx.restore();
    }
    // süngü sırası: sırtın siperinde; birer birer boşalır
    const gone = [[1180, tN + .4], [1340, tN + .9], [1060, tN + 1.4]];
    for (let x = 960; x < 1600; x += 62) {
      const g_ = gone.find(q => q[0] === x || Math.abs(q[0] - x) < 31); if (g_ && t > g_[1]) continue;
      a4_bayonetHead(ctx, x, a4_yAt(trench, x) - 4, .95);
    }
    // sancak (küçük, kırmızı)
    { const fx = 1270, fy = a4_yAt(crest, fx) - 6, wv = Math.sin(tf * 6) * 3; inkStroke(ctx, PL([[fx, fy], [fx, fy - 96]], false), 3);
      const fl = SP([[fx, fy - 94], [fx + 26, fy - 96 + wv], [fx + 54, fy - 92 - wv], [fx + 54, fy - 62 - wv], [fx + 26, fy - 66 + wv], [fx, fy - 62]], true, .5); knock(ctx, fl); plate(ctx, 'red', fl); inkStroke(ctx, fl, 2);
      const cr = new Path2D(); cr.arc(fx + 21, fy - 78, 7.4, 0, TAU); cr.arc(fx + 23.8, fy - 78, 6, 0, TAU, true); ctx.save(); ctx.fillStyle = P.paper; ctx.fill(cr, 'evenodd'); ctx.restore(); }
    // patlamalar: Arıburnu (yamaç) ve Anafartalar (sağ)
    for (const [x, y, t0, R, sd] of [[860, 620, tA, 120, 61], [1700, 470, tN, 110, 62]]) {
      if (t < t0) continue; const u = t - t0;
      const sm = a4_L('E05a-sm' + sd, g2 => a4_smokeCloud(g2, x, y - 110, 170, sd, 'ink', .5), 40);
      ctx.save(); ctx.translate(x, y); const k = .75 + .3 * E.out3(clamp(u / 1.4)); ctx.scale(k, k); ctx.translate(-x, -y - u * 10); a4_put(ctx, sm, null, 1, { mode: 'multiply', a: clamp(u / .25) }); ctx.restore();
      a4_burst(ctx, x, y - 30, R, sd, E.outBack(clamp(a4_tf(u) / .18)) * (1 - ramp(u, .9, 1.3)));
    }
    a4_tag(ctx, 'ARIBURNU', 430, 1000, 760, 860, E.out2(ramp(t, tA, tA + .3)));
    a4_tag(ctx, 'ANAFARTALAR', 1500, 330, 1700, 430, E.out2(ramp(t, tN, tN + .3)));
    ctx.restore();
    // yakın siper (en önde): kum torbası ve süngü sırası; "yarbay"a doğru iki asker eksilir (kayıp, kansız)
    ctx.save(); cam(ctx, cm, 1.06);
    const vac = [[2, tN + .7], [4, tN + 1.3]];
    for (let i = 0; i < 7; i++) { const v = vac.find(q => q[0] === i); if (v && t > v[1]) continue; a4_bayonetHead(ctx, 1010 + i * 128, 1000 + (i % 2) * 6, 2.05); }
    ctx.restore();
    a4_put(ctx, a4_L('E05a-fg', g => a4_sandbags(g, 880, W + 80, 992, 3, 41, { bw: 110, bh: 42 }), 90), cm, 1.06);
    stamp(ctx, 'ÇANAKKALE · 1915', 110, 116, lt - .1, st.d, { size: 34 });
  }, { tr: { type: 'press', dur: .6 }, post: { stone: .26 } });
}

// E05b · Sırtta yarbay Mustafa Kemal (34): kabalak, haki setre, elinde cep saati (saniye ibresi atar); aşağıda turkuaz deniz.
{
  const T0 = Wd('E05', 'bilinmeyen'), tYb = Wd('E05', 'yarbay'), tKo = Wd('E05', 'komutana');
  const MK = { x: 1200, y: 400, s: 1.34 };
  shot(T0, (ctx, st) => {
    setReg(409);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt);
    const cm = { x: lerp(980, 1000, E.sine(st.p)), y: lerp(540, 520, E.sine(st.p)), z: lerp(1.0, 1.05, E.sine(st.p)) };
    const bg = a4_L('E05b-bg', g => {
      paperBG(g);
      for (const [y0, a] of [[-200, .26], [260, .14], [420, .12]]) plate(g, 'ochre', a4_rect(-300, y0, W + 300, 640), { a });
      const clip = new Path2D(); clip.rect(-300, -300, W + 600, 900); clip.ellipse(MK.x - 20, MK.y - 30, 340, 340, 0, 0, TAU);
      g.save(); g.clip(clip, 'evenodd'); radialHT(g, 'ink', 200, -900, 900, 1300, .22, 0, { cell: 12, ang: 45, box: [-200, -200, W + 200, 300] }); g.restore();
      const sea = a4_rect(-300, 600, W + 300, H + 300); knock(g, sea); plate(g, 'teal', sea, { a: .78 }); plate(g, 'teal', a4_rect(-300, 600, W + 300, 622), { a: .6 });
      g.save(); g.clip(a4_rect(-300, 630, 760, H + 300)); radialHT(g, 'teal', 100, 1200, 300, 700, .5, 0, { cell: 12, box: [-200, 630, 800, H + 100] }); g.restore();
      for (const [x, s] of [[180, .55], [420, .7], [640, .5]]) a4_ship(g, x, 604, s, { dir: 1 });
      // karşı sırtlar (uzak)
      const far = SP([[-300, 640], [-100, 560], [200, 520], [520, 560], [760, 620], [900, 700], [900, H + 300], [-300, H + 300]], true, .6);
      knock(g, far); plate(g, 'ochre', far, { a: .5 }); plate(g, 'khaki', far, { a: .35 }); inkStroke(g, far, 2);
      for (let i = 0; i < 30; i++) { const x = -100 + i * 32, y = 560 + Math.abs(x - 300) * .12; inkStroke(g, PL([[x, y + 20], [x - 10, y + 80]], false), 1.2, { a: .4 }); }
      // bulunduğu sırt (yakın, MK'nin ayağı altında)
      const near = SP([[700, H + 300], [820, 800], [1000, 740], [1300, 720], [1600, 740], [2100, 780], [2100, H + 300]], true, .6);
      knock(g, near); plate(g, 'khaki', near); plate(g, 'ochre', near, { a: .3 }); inkStroke(g, SP([[820, 800], [1000, 740], [1300, 720], [1600, 740], [2100, 780]], false, .6), 3);
    }, 90);
    a4_put(ctx, bg, cm, .6);
    ctx.save(); cam(ctx, cm, .6);
    // sırtlardan yükselen düz duman (rüzgârla sağa sürüklenir)
    ctx.save(); ctx.globalCompositeOperation = 'multiply';
    for (const [x0, y0, k0] of [[260, 560, 0], [640, 610, 1]]) for (let j = 0; j < 9; j++) { const u = ((lt * .22 + j / 9 + k0 * .37) % 1), r = 18 + u * 70; ctx.globalAlpha = .5 * (1 - u); ctx.fillStyle = P.khaki; ctx.beginPath(); ctx.ellipse(x0 + u * 180 + Math.sin(j * 2.1) * 14, y0 - u * 330, r, r * .7, 0, 0, TAU); ctx.fill(); }
    ctx.restore();
    // uzak patlama ("komutana")
    if (t > tKo) { const u = t - tKo; a4_burst(ctx, 330, 560, 60, 81, E.outBack(clamp(a4_tf(u) / .16)) * (1 - ramp(u, .8, 1.1)), { ring: false }); }
    ctx.restore();
    a4_dust(ctx, lt, { box: [-60, 200, W + 60, 800], n: 50, seed: 19, wind: 70, rise: -10, col: 'khaki', a: .45, size: 3 });
    // Mustafa Kemal: denize (sola) bakar; sağ eli göğüs hizasında cep saati
    ctx.save(); cam(ctx, cm, 1);
    const io = idleOffsets(tf, 4, .7), bl = blinkAt(t, 4), o = { x: MK.x, y: MK.y + io.breath, s: MK.s, dir: -1 };
    bust(ctx, { ...o, coat: 'setre', col: 'khaki', w: 1.04, seed: 3, len: (H + 40 - MK.y) / MK.s, turn: .3 });
    head3q(ctx, { ...o, who: 'mk', gear: 'kabalak', light: 'front', lookAt: [300, 520], age: 33, tilt: io.head * .6, eyeOpen: .72 * (1 - bl) });
    const sh = [MK.x - 36, MK.y + 190], hand = [MK.x - 150, MK.y + 318 + io.breath];
    const A = arm(ctx, sh, hand, { upper: 96, fore: 90, w: 52, col: 'khaki', bend: 1 });
    handDraw(ctx, A.wr[0], A.wr[1], A.ang, A.w2 / 20, 'hold', { side: -1 });
    const wx_ = A.wr[0] + Math.cos(A.ang) * 22, wy_ = A.wr[1] + Math.sin(A.ang) * 22 - 18;
    // köstek: saatten setre düğmesine
    inkStroke(ctx, SP([[wx_ + 8, wy_ + 20], [wx_ + 40, wy_ + 70], [MK.x - 8, MK.y + 250]], false), 2.2, { a: .9 });
    a4_watch(ctx, wx_, wy_, 28, t, { rot: -.15 });
    ctx.restore();
    // ön siper: kum torbaları (büstü keser)
    const fg = a4_L('E05b-fg', g => { a4_sandbags(g, -40, W + 60, 880, 3, 14, { bw: 96, bh: 40 }); }, 90);
    a4_put(ctx, fg, cm, 1.08);
    // "adı pek bilinmeyen bir yarbay": 25 Nisan 1915 Arıburnu (yarbay rütbesi Haziran'a kadar) → 33 yaşında
    stamp(ctx, 'ARIBURNU · 25 NİSAN 1915', 110, 116, lt - .1, st.d, { size: 32 });
    nameTag(ctx, 1860, 868, 'MUSTAFA KEMAL', 'yarbay · 33 yaşında', t - tYb, st.end - tYb, { align: 'right', size: 56, sub: 38, bg: P.paperD });
  }, { tr: { type: 'cut', dur: 0 }, post: { stone: .26 } });
}

// E06a · Üç pano: Kafkasya (kar), Irak (nehir), Filistin (çöl); her pano kendi kelimesinde basılır, adı bilinen kişileri
// küçük levhalarıyla gelir (tarih danışmanı onaylı metinler, A4_E06_KISI). "birbirini": figürler panoların arasından birbirine döner
// (Kafkasya'da MK ile Fevzi yüz yüze; Karabekir önce Kafkasya'ya, "tanıdı"da Filistin'e). "yenildiğinde": panolar kararır.
// Kişi eşleşmesi tek dizidedir; değişiklik gelirse yalnız burası düzenlenir.
const A4_E06_KISI = [
  { panel: 0, who: 'mk', age: 35, x: 150, name: 'Mirliva Mustafa Kemal', sub: 'XVI. Kolordu · Muş–Bitlis 1916', dirs: [-1, 1] },
  { panel: 0, who: 'fevzi', age: 40, x: 404, name: 'Fevzi Paşa', sub: 'II. Kafkas Kolordusu · 1916', dirs: [1, -1] },
  { panel: 1, who: 'karabekir', age: 34, x: 290, name: 'Miralay Kâzım (Karabekir)', sub: 'XVIII. Kolordu · Kut 1916', dirs: [1, -1, 1] },
  { panel: 2, who: 'alifuat', age: 35, x: 150, name: 'Ali Fuat', sub: 'XX. Kolordu · Kudüs 1917', dirs: [1, -1] },
  { panel: 2, who: 'ismet', age: 34, x: 404, name: 'Miralay İsmet', sub: 'III. Kolordu · 1918', dirs: [1, -1], dy: 14 },
];
{
  const T0 = S('E06'), tK = Wd('E06', 'kafkasyada'), tI = Wd('E06', 'irakta'), tF = Wd('E06', 'filistinde'), tB = Wd('E06', 'birbirini'), tT = Wd('E06', 'tanıdı'), tY = Wd('E06', 'yenildiğinde');
  const PW = 560, PH = 700, PY = 250, PX = [80, 680, 1280];
  const SNOW = [[PX[0] - 20, PY + 610], [PX[0] + 180, PY + 584], [PX[0] + 380, PY + 546], [PX[0] + PW + 20, PY + 508]];
  const HEADY = PY + 520, FS = .74, words = ['kafkasyada', 'irakta', 'filistinde'];
  const panel = (i, g) => {
    const x0 = PX[i], y0 = PY, x1 = x0 + PW, y1 = y0 + PH, R = a4_rect(x0, y0, x1, y1);
    g.save(); g.clip(R); paperBG(g);
    if (i === 0) { // Kafkasya: koyu gök, karlı dağlar
      plate(g, 'khaki', R, { a: .6 }); plate(g, 'ink', a4_rect(x0, y0, x1, y0 + 360), { a: .35 });
      radialHT(g, 'ink', x0 + 280, y0 - 500, 500, 860, .4, 0, { cell: 11, ang: 45, box: [x0, y0, x1, y0 + 300] });
      for (const [px, py, w, sd] of [[x0 + 60, y0 + 520, 300, 1], [x0 + 300, y0 + 500, 340, 2], [x0 + 140, y0 + 600, 420, 3]]) { const m = PL([[px - w / 2, y1], [px - w * .1, py - w * .7], [px, py - w * .78], [px + w * .14, py - w * .64], [px + w / 2, y1]]); knock(g, m); inkStroke(g, m, 2.6); g.save(); g.clip(m); for (let k = 0; k < 14; k++) inkStroke(g, PL([[px + k * 12, py - w * .7 + k * 22], [px + k * 12 + 60, y1]], false), 1.6, { a: .5 }); plate(g, 'khaki', PL([[px, py - w * .78], [px + w * .14, py - w * .64], [px + w / 2, y1], [px + 20, y1]]), { a: .35 }); g.restore(); }
      const sn = SP([...SNOW, [x1 + 20, y1 + 20], [x0 - 20, y1 + 20]], true, .6); knock(g, sn); inkStroke(g, SP(SNOW, false, .6), 2.4);
      for (let k = 0; k < 6; k++) inkStroke(g, SP(SNOW.map(([x, y]) => [x, y + 24 + k * 18]), false, .6), 1.2, { a: .3 });
    } else if (i === 1) { // Irak: okra ova, kıvrılan nehir, hurmalar
      plate(g, 'ochre', R, { a: .35 }); plate(g, 'ochre', a4_rect(x0, y0 + 300, x1, y1), { a: .35 });
      radialHT(g, 'sepia', x0 + 280, y0 - 400, 400, 760, .3, 0, { cell: 11, box: [x0, y0, x1, y0 + 260] });
      const rv = SP([[x0 - 20, y0 + 330], [x0 + 200, y0 + 350], [x0 + 330, y0 + 400], [x0 + 200, y0 + 480], [x0 + 60, y0 + 560], [x0 + 260, y0 + 650], [x1 + 20, y1 + 10], [x1 + 20, y1 + 60], [x0 + 200, y0 + 700], [x0 - 10, y0 + 580], [x0 + 150, y0 + 470], [x0 + 230, y0 + 410], [x0 + 120, y0 + 380], [x0 - 20, y0 + 370]], true, .7);
      knock(g, rv); plate(g, 'khaki', rv, { a: .75 }); inkStroke(g, rv, 2.4);
      g.save(); g.clip(rv); for (let k = 0; k < 20; k++) cut(g, PL([[x0 + (k * 53) % PW, y0 + 340 + k * 18], [x0 + (k * 53) % PW + 30, y0 + 340 + k * 18]], false), 2, { a: .6 }); g.restore();
      for (const [px, sd, sc] of [[x0 + 420, 1, .9], [x0 + 500, 2, .75], [x0 + 70, 3, .8]]) a4_palm(g, px, y0 + 330, sc, sd + 20);
    } else { // Filistin: kumullar, demiryolu
      plate(g, 'ochre', R, { a: .28 });
      radialHT(g, 'sepia', x0 + 280, y0 - 400, 400, 760, .3, 0, { cell: 11, box: [x0, y0, x1, y0 + 260] });
      for (const [yy, a, sd] of [[y0 + 330, .4, 1], [y0 + 450, .6, 2], [y0 + 580, .85, 3]]) { const d = a4_groundPath(a4_ridgePts(x0 - 20, x1 + 20, yy, 30, sd + 40, 6), y1 + 20); knock(g, d); plate(g, 'ochre', d, { a }); inkStroke(g, SP(a4_ridgePts(x0 - 20, x1 + 20, yy, 30, sd + 40, 6), false), 2.2); }
      const rl = PL([[x0 - 20, y0 + 420], [x1 + 20, y0 + 400]], false); inkStroke(g, rl, 6); inkStroke(g, rl, 3, { col: P.paper }); g.save(); g.setLineDash([12, 12]); inkStroke(g, rl, 3); g.restore();
    }
    g.restore();
    inkStroke(g, R, 4); inkStroke(g, a4_rect(x0 + 10, y0 + 10, x1 - 10, y1 - 10), 1.2, { a: .7 });
  };
  shot(T0, (ctx, st) => {
    setReg(410);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt);
    const cm = { x: 960, y: lerp(560, 540, E.sine(st.p)), z: lerp(1.0, 1.04, E.sine(st.p)) };
    const wall = a4_L('E06a-wall', g => { paperBG(g); plate(g, 'khaki', a4_full(), { n: 2 }); plate(g, 'ink', a4_full(), { a: .3 }); radialHT(g, 'ink', 960, 560, 700, 1300, 0, .3, { cell: 12, ang: 45, box: [-150, -150, W + 150, H + 150] }); }, 90);
    a4_put(ctx, wall, cm, .5);
    const labs = ['KAFKASYA', 'IRAK', 'FİLİSTİN'], t0s = [tK, tI, tF];
    ctx.save(); cam(ctx, cm, 1);
    for (let i = 0; i < 3; i++) {
      const u = ramp(t, t0s[i] - .1, t0s[i] + .25, E.out3); if (u <= 0) continue;
      const L = a4_L('E06a-p' + i, g => panel(i, g), 0), x0 = PX[i];
      ctx.save(); ctx.translate(0, (1 - u) * -40);
      plate(ctx, 'ink', a4_rect(x0 + 14, PY + 18, x0 + PW + 14, PY + PH + 18), { a: .4 * u });
      ctx.save(); ctx.beginPath(); ctx.rect(x0, PY, PW * clamp(u * 1.3), PH); ctx.clip(); a4_put(ctx, L, null, 1); 
      // canlı öğeler
      ctx.beginPath(); ctx.rect(x0, PY, PW, PH); ctx.clip();
      if (i === 0) { for (let k = 0; k < 6; k++) { const x = x0 + 30 + ((tf * 22 + k * 86) % (PW - 30)), y = a4_yAt(SNOW, x) + 4; a4_soldier(ctx, x, y, .85, tf * 1.1 + k * .4, { lean: .12 }); }
        ctx.save(); ctx.fillStyle = '#F4EDDC'; const r = rng(4); for (let k = 0; k < 70; k++) { const sx = x0 + ((r() * PW + lt * 30 * (.5 + r())) % PW), sy = PY + ((r() * PH + lt * 90 * (.6 + r())) % PH); ctx.beginPath(); ctx.arc(sx, sy, 1.6 + r() * 2.2, 0, TAU); ctx.fill(); } ctx.restore(); }
      if (i === 1) { const bx = PX[1] + 150 + tf * 12; a4_ship(ctx, bx, PY + 452, .55, { dir: 1 }); }
      if (i === 2) { const tx = PX[2] - 330 + ((tf * 70) % (PW + 700)); a4_train(ctx, tx, PY + 412, .62, lt);
        for (let k = 0; k < 3; k++) { const x = PX[2] + 200 + k * 120 + tf * 10, y = PY + 488 + k * 8; a4_camel(ctx, x, y, .4, Math.floor(tf * 4 + k) % 2); } }
      // adı bilinen kişiler (panonun önünde, göz hizasında); "birbirini"de birbirine dönerler
      const ppl = A4_E06_KISI.filter(q => q.panel === i);
      ppl.forEach((q, k) => {
        const tw = Wd('E06', words[i]), ui = ramp(t, tw + .15 + k * .2, tw + .55 + k * .2, E.lin); if (ui <= 0) return;
        const turn = ramp(t, tB + .08 * A4_E06_KISI.indexOf(q), tB + .08 * A4_E06_KISI.indexOf(q) + .01), turn2 = q.dirs.length > 2 ? ramp(t, tT, tT + .01) : 0;
        const dir = turn2 > 0 ? q.dirs[2] : turn > 0 ? q.dirs[1] : q.dirs[0];
        const x = x0 + q.x, y = HEADY + (q.dy || 0), io = idleOffsets(tf, 11 + A4_E06_KISI.indexOf(q) * 3, .5);
        const others = A4_E06_KISI.filter(o => o !== q).map(o => [PX[o.panel] + o.x, HEADY + (o.dy || 0)]);
        const tgt = others.filter(([ox]) => (ox - x) * dir > 0).sort((m, n) => Math.abs(m[0] - x) - Math.abs(n[0] - x))[0];
        a4_pressIn(ctx, ui, y - 110, PY + PH, () => a4_officer(ctx, { x, y: y + io.breath, s: FS, dir, who: q.who, age: q.age, seed: a4_KUSAK.seed[q.who] || 3, len: (PY + PH + 20 - y) / FS, lookAt: turn > 0 && tgt ? tgt : null, look: [1, .25], tilt: io.head * .5, turn: .3, w: 1.04, sep: k > 0 }));
      });
      ctx.restore();
      // kararma ("yenildiğinde")
      const dk = ramp(t, tY + i * .12, tY + .5 + i * .12, E.io2); if (dk > 0) { plate(ctx, 'ink', a4_rect(x0, PY, x0 + PW, PY + PH), { a: .62 * dk }); }
      inkStroke(ctx, a4_rect(x0, PY, x0 + PW, PY + PH), 4);
      ctx.restore();
      a4_tag(ctx, labs[i], x0 + 24, PY - 34, null, null, u * (1 - .5 * ramp(t, tY, tY + .5)), { size: 30 });
    }
    // küçük levhalar (isim büyük, alt satır Courier); kişi kendi kelimesinde, "imparatorluk"ta kalkar
    for (let i = 0; i < 3; i++) A4_E06_KISI.filter(q => q.panel === i).forEach((q, k) => {
      const tw = Wd('E06', words[i]) + .35 + k * .2, tOut = Wd('E06', 'imparatorluk') + .2;
      a4_plaque(ctx, PX[i] + 16, PY + 16 + k * 96, q.name, q.sub, t - tw, tOut - tw, { size: 28, sub: 19 });
    });
    ctx.restore();
    stamp(ctx, '1914–1918', 80, 140, lt - .1, st.d, { size: 34 });
  }, { tr: { type: 'cut', dur: 0 }, post: { stone: .26 } });
}

// E06b · Siper, akşam: "tecrübe" (parapetteki harita, pusula, dürbün ışığa çıkar), "ve birbirleri": kuşak şeridi
// omuz omuza siperde basılarak belirir (soldan sağa merdane). İsim + yaş (1918).
{
  const T0 = Wd('E06', 'ellerinde'), tTc = Wd('E06', 'tecrübe'), tBr = Wd('E06', 've');
  const order = ['alifuat', 'karabekir', 'mk', 'ismet', 'fevzi'], Y = 1918, XS = [470, 715, 960, 1205, 1450];
  shot(T0, (ctx, st) => {
    setReg(411);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt);
    const cm = { x: 960, y: lerp(560, 540, E.sine(st.p)), z: lerp(1.0, 1.045, E.sine(st.p)) };
    const bg = a4_L('E06b-bg', g => {
      paperBG(g);
      plate(g, 'khaki', a4_rect(-300, -300, W + 300, 700), { a: .55 }); plate(g, 'ochre', a4_rect(-300, 330, W + 300, 700), { a: .3 });
      radialHT(g, 'ink', 960, -1100, 1100, 1330, .3, 0, { cell: 12, ang: 45, box: [-200, -200, W + 200, 230] });
      a4_smokeCloud(g, 120, 420, 160, 31, 'ink', .4); a4_smokeCloud(g, 1830, 400, 150, 32, 'ink', .4);
      a4_wire(g, -60, W + 60, 600, 9, { h: 40, step: 170 });
      a4_sandbags(g, -60, W + 60, 590, 5, 21, { bw: 92, bh: 38, a: .5 });
      // siper iç duvarı (koyu) ve basamak
      const wl = a4_rect(-300, 760, W + 300, H + 300); plate(g, 'khaki', wl, { n: 2 }); plate(g, 'ink', wl, { a: .35 });
      for (let x = -40; x < W + 60; x += 110) inkStroke(g, PL([[x, 760], [x, H + 100]], false), 3, { a: .6 });
    }, 90);
    a4_put(ctx, bg, cm, .7);
    // gökte sağa sürüklenen yarım ton duman: durağan katman yalnız kayar; başların 1,5 baş çevresinin dışında (y < 260)
    const drift = a4_L('E06b-drift', g => { a4_smokeCloud(g, 420, 150, 170, 41, 'ink', .36); a4_smokeCloud(g, 1180, 120, 200, 42, 'ink', .32); a4_smokeCloud(g, 1760, 170, 150, 43, 'ink', .3); }, 200);
    ctx.save(); cam(ctx, cm, .7); ctx.beginPath(); ctx.rect(-200, -200, W + 400, 470); ctx.clip(); ctx.translate(-120 + lt * 22, 0); a4_put(ctx, drift, null, 1, { mode: 'multiply' }); ctx.restore();
    // kuşak şeridi: "ve birbirleri"de soldan sağa merdane ile basılır; sağdan sola çizilir (soldaki önde)
    const rx = kf(t, [[tBr - .1, 200], [tBr + 1.1, 1800, E.io2]]);
    ctx.save(); cam(ctx, cm, 1);
    if (t > tBr - .1) {
      const b = REG.boost; REG.boost = 1 + 4 * (1 - ramp(t, tBr, tBr + 1.4, E.out3));
      ctx.save(); ctx.beginPath(); ctx.rect(-200, -200, rx, H + 400); ctx.clip();
      for (let i = order.length - 1; i >= 0; i--) {
        const who = order[i], x = XS[i], y = 470 + (i % 2) * 8, io = idleOffsets(tf, i * 4 + 3, .5);
        a4_officer(ctx, { x, y: y + io.breath, s: 1.1, dir: -1, who, age: Y - a4_KUSAK.born[who], seed: a4_KUSAK.seed[who], len: (H + 40 - y) / 1.1, lookAt: [100, 360], tilt: io.head * .5, turn: .3, w: 1.04, sep: true });
      }
      ctx.restore(); REG.boost = b;
      if (rx < 1800) inkStroke(ctx, PL([[rx, -100], [rx, H + 100]], false), 3, { a: .6 });
    }
    ctx.restore();
    // ön basamak ve "tecrübe": harita, pusula, dürbün
    const ledge = a4_L('E06b-ledge', g => {
      const top = PL([[-60, 900], [W + 60, 892], [W + 60, H + 100], [-60, H + 100]]); knock(g, top); plate(g, 'ochre', top); plate(g, 'khaki', top, { a: .45 }); inkStroke(g, PL([[-60, 900], [W + 60, 892]], false), 4);
      for (let i = 0; i < 7; i++) inkStroke(g, SP([[-60, 916 + i * 24], [700, 918 + i * 24 + (i % 2) * 4], [W + 60, 912 + i * 24]], false), 1.4, { a: .4 });
      paperSheet(g, 760, 965, 230, 120, -.05, 31, { rows: 4 }); compass(g, 1000, 975, 44); binoculars(g, 1250, 960, 1.05, .06);
      // basamakta düşmüş bir kabalak (kayıp; kansız)
      plate(g, 'ink', SP([[440, 1000], [590, 992], [600, 1010], [450, 1018]], true, .7), { a: .35 });
      headgear(g, { x: 500, y: 1058, s: .95, dir: 1, gear: 'kabalak', tilt: .22, sd: 5, WD: 1, HY: 1 });
    }, 90);
    a4_put(ctx, ledge, cm, 1.06);
    // karanlık: başta siper koyu; "tecrübe"de basamak, "birbirleri"nde siper aydınlanır
    const d1 = .5 * (1 - ramp(t, tTc - .1, tTc + .5)) + .2 * ramp(t, tBr + .8, tBr + 1.6), d2 = .5 * (1 - ramp(t, tBr, tBr + 1.2));
    if (d2 > 0) plate(ctx, 'ink', a4_rect(-50, -50, W + 50, 890), { a: d2 });
    if (d1 > 0) plate(ctx, 'ink', a4_rect(-50, 890, W + 50, H + 50), { a: d1 });
    // isim + yaş (1918)
    order.forEach((who, i) => { const lb = (who === 'mk' ? 'M. KEMAL' : a4_KUSAK.short[who]) + ' · ' + (Y - a4_KUSAK.born[who]); a4_tag(ctx, lb, XS[i] - (lb.length * 15.4 + 28) / 2, 862 + (i % 2) * 34, null, null, E.out2(ramp(t, tBr + .9 + i * .12, tBr + 1.2 + i * .12)), { size: 22 }); });
  }, { tr: { type: 'cut', dur: 0 }, post: { stone: .26 } });
}
