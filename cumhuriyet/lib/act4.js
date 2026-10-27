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
  if (o.flag !== false) {
    const wv = o.wave || 0, fl = SP([[0, -212], [24, -214 + wv], [50, -210 - wv], [50, -180 - wv * .5], [24, -184 + wv], [0, -182]], true, .5);
    knock(ctx, fl); plate(ctx, 'red', fl); inkStroke(ctx, fl, 2 / s);
    const cr = new Path2D(); cr.arc(20, -197, 7.4, 0, TAU); cr.arc(22.8, -197, 6, 0, TAU, true);
    ctx.save(); ctx.fillStyle = P.paper; ctx.fill(cr, 'evenodd');
    const stp = []; for (let i = 0; i < 10; i++) { const a = -PI / 2 + i * PI / 5, rr = i % 2 ? 1.7 : 4; stp.push([31 + Math.cos(a) * rr, -197 + Math.sin(a) * rr]); }
    ctx.fill(PL(stp)); ctx.restore();
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

// E01 · Renk çöker: 1908'in kartpostal kalıpları (kırmızı güneş, turkuaz tepeler, altın ışınlar) birer birer kalkar;
// geriye haki, okra ve is kalır. "savaş": güneşin yerinde is patlama yıldızı + yarım ton duman, büyük SAVAŞ damgası.
{
  const T0 = S('E01'), tSav = Wd('E01', 'savaş'), tKus = Wd('E01', 'kuşağın'), tAsil = Wd('E01', 'asıl'), tOkul = Wd('E01', 'okulu');
  const SUN = [1250, 650], HOR = 668;
  const hills = a4_ridgePts(-160, W + 160, 632, 24, 3, 16, 1.4);
  const ridge = a4_ridgePts(-200, W + 200, 826, 14, 8, 18, .9);
  const front = a4_ridgePts(-200, W + 200, 1004, 14, 41, 12);
  const rays = (() => { const out = []; const n = 30; for (let i = 0; i < n; i += 2) { const a0 = PI + i / n * PI - .02, a1 = PI + (i + 1) / n * PI + .02, R = 2400; out.push(PL([SUN, [SUN[0] + Math.cos(a0) * R, SUN[1] + Math.sin(a0) * R], [SUN[0] + Math.cos(a1) * R, SUN[1] + Math.sin(a1) * R]])); } return out; })();
  const raysP = new Path2D(); rays.forEach(r => raysP.addPath(r));
  const skyClip = a4_rect(-200, -200, W + 200, HOR + 4);
  shot(T0, (ctx, st) => {
    setReg(401);
    paperBG(ctx);
    const lt = st.lt, t = st.t, tf = a4_tf(lt), ls = tSav - T0;
    const sk = shake(t, tSav, 9, 5);
    const cm = { x: lerp(960, 1012, E.sine(st.p)), y: lerp(540, 566, E.sine(st.p)), z: lerp(1, 1.05, E.sine(st.p)), sx: sk[0], sy: sk[1] };
    // —— gök (durağan): kâğıt, ufka doğru okra bantlar, tepede is yarım ton; ışınların sönük izi
    const sky = a4_L('E01-sky', g => {
      paperBG(g);
      g.save(); g.clip(skyClip);
      plate(g, 'ochre', a4_rect(-200, 352, W + 200, HOR + 4), { a: .16 });
      plate(g, 'ochre', a4_rect(-200, 512, W + 200, HOR + 4), { a: .22 });
      plate(g, 'ochre', raysP, { a: .1 });
      for (const r of rays) inkStroke(g, r, 1, { a: .16 });
      radialHT(g, 'ink', SUN[0], 1500, 1200, 1640, 0, .13, { cell: 12, ang: 45, box: [-160, -140, W + 160, 280] });
      g.restore();
    }, 90);
    a4_put(ctx, sky, cm, .25);
    // kartpostal kalıpları (canlı çizilir ki kalkabilsin)
    const lfR = a4_lift(lt, tKus - T0), lfT = a4_lift(lt, tAsil - T0), lfG = a4_lift(lt, tOkul - T0);
    ctx.save(); cam(ctx, cm, .25); ctx.save(); ctx.clip(skyClip);
    a4_plateOff(ctx, 'gold', raysP, lfG, { a: .62 });
    a4_plateOff(ctx, 'gold', a4_rect(-200, 440, W + 200, HOR + 4), lfG, { a: .5 });
    ctx.restore();
    // güneş: kırmızı kalıp kalkınca kâğıt disk kalır (odak); "savaş"ta yerini patlama alır
    if (lt < ls + .05) {
      const sun = new Path2D(); sun.arc(SUN[0], SUN[1], 80, PI, TAU); sun.closePath();
      knock(ctx, sun, '#F7F0DE'); a4_plateOff(ctx, 'red', sun, lfR); inkStroke(ctx, sun, 3.2);
    }
    ctx.restore();
    // —— patlama (güneşin yerinde, ufkun ardında): is yıldızı + durağan yarım ton duman
    if (lt >= ls) {
      const u = lt - ls, smk = a4_L('E01-smoke', g => { a4_smokeCloud(g, SUN[0], SUN[1] - 170, 240, 7, 'ink', .55); a4_smokeCloud(g, SUN[0] - 360, SUN[1] - 70, 130, 9, 'ink', .42); a4_smokeCloud(g, SUN[0] + 270, SUN[1] - 100, 160, 12, 'ink', .42); }, 60);
      ctx.save(); cam(ctx, cm, .3); const k = .7 + .3 * E.out3(clamp(u / 1.2));
      ctx.translate(SUN[0], SUN[1]); ctx.scale(k, k); ctx.translate(-SUN[0], -SUN[1] - u * 14);
      ctx.globalAlpha = clamp(u / .25); a4_put(ctx, smk, null, 1, { mode: 'multiply' }); ctx.restore();
      ctx.save(); cam(ctx, cm, .3);
      a4_burst(ctx, SUN[0], SUN[1] - 34, 220, 31, E.outBack(clamp(a4_tf(u) / .2)));
      if (u > .3) a4_burst(ctx, SUN[0] - 560, SUN[1] - 6, 84, 37, E.outBack(clamp((a4_tf(u) - .3) / .16)), { ring: false });
      ctx.restore();
    }
    // —— uzak tepeler: haki taban; turkuaz kartpostal kalıbı kalkar
    const far = a4_L('E01-far', g => {
      const p = a4_groundPath(hills, HOR + 60);
      knock(g, p); plate(g, 'khaki', p, { a: .42 }); inkStroke(g, SP(hills, false, .6), 2.4);
      for (let i = 0; i < 26; i++) { const x = -100 + i * 80, y = a4_yAt(hills, x); inkStroke(g, PL([[x, y + 10], [x + 26, y + 6]], false), 1.4, { a: .35 }); }
    }, 90);
    a4_put(ctx, far, cm, .45);
    ctx.save(); cam(ctx, cm, .45); a4_plateOff(ctx, 'teal', a4_groundPath(hills, HOR + 60), lfT, { a: .75 }); ctx.restore();
    // —— açık ova (ufuktan sırta)
    const plain = a4_L('E01-plain', g => {
      const pp = a4_groundPath(a4_ridgePts(-200, W + 200, HOR + 2, 4, 21, 10), H + 100);
      knock(g, pp); plate(g, 'ochre', pp, { a: .42 });
      for (let i = 0; i < 8; i++) { const y = HOR + 14 + i * i * 2.6; inkStroke(g, SP(a4_ridgePts(-200, W + 200, y, 2.5, 30 + i, 8), false), 1.2, { a: .2 + i * .03 }); }
    }, 90);
    a4_put(ctx, plain, cm, .6);
    // —— yürüyüş sırtı: koyu haki toprak, güneşe yakınsayan tarla izleri (kâğıt kazıma)
    const mid = a4_L('E01-mid', g => {
      const rp = a4_groundPath(ridge, H + 100);
      knock(g, rp); plate(g, 'khaki', rp); plate(g, 'ochre', rp, { a: .3 });
      g.save(); g.clip(rp);
      for (let i = -14; i <= 14; i++) { const xb = SUN[0] + i * 150, q = PL([[SUN[0] + i * 9, 826], [xb, 1180]], false); cut(g, q, 2.2, { a: .22 + .12 * (i % 2 === 0) }); }
      g.restore();
      inkStroke(g, SP(ridge, false, .6), 3.6);
    }, 90);
    a4_put(ctx, mid, cm, .8);
    // yürüyen kol (sağa, güneşe doğru); tozu ayaklarında; pozlar ikişer karede
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
    // —— izleyici katmanı
    chapterCard(ctx, 'IV', 'ATEŞTE DÖVÜLEN KUŞAK', '1911–1918', lt - .15, ls - .2);
    bigStamp(ctx, 'SAVAŞ', 600, 318, lt - ls - .06, st.d - ls + .6, { size: 240, rot: -.035, ls: 10 });
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

// —— geçici yer tutucular (çekimler yazıldıkça kalkar) ——
// E02b · Derne, 1911: çöl dioraması. Kefiyeli genç kolağası Mustafa Kemal (30), arkada yerel gönüllüler, çadır, hurmalar, ak kasaba.
{
  const T0 = Wd('E02', 'sahte');
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
      // gökte okra yarım ton yalnız solda ve tepede (başın çevresi temiz)
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
    a4_tent(ctx, 905, a4_yAt(dune1, 905) + 6, .92, { wave: Math.sin(tf * 7) * 3 });
    ctx.restore();
    // gönüllüler: kum üstünde, haki gölgeli; pozlar ikişer karede (tüfek sallanır, biri yürür)
    ctx.save(); cam(ctx, cm, .72);
    const yd = x => a4_yAt(dune1, x) + 34;
    a4_camel(ctx, 170, yd(170) - 4, 1.32, Math.floor(tf * 4) % 2);
    for (const [x, k, sc, sd, dr] of [[318, 1, 1.62, 1, 1], [420, 0, 1.72, 2, 1], [520, 2, 1.66, 3, 1], [640, 0, 1.76, 4, -1], [1010, 1, 1.6, 5, -1]]) a4_local(ctx, x, yd(x), sc, k, { seed: sd, dir: dr });
    // yürüyen gönüllü (soldan çadıra)
    const wx = 720 + tf * 26; a4_soldier(ctx, wx, yd(wx), 1.62, tf * 1.4, { rifle: true });
    ctx.restore();
    // ön kum: kaba sırt, koyu okra
    const fg = a4_L('E02b-fg', g => { const d2 = a4_groundPath(dune2, H + 100); knock(g, d2); plate(g, 'ochre', d2, { a: .9 }); plate(g, 'khaki', d2, { a: .18 }); inkStroke(g, SP(dune2, false, .6), 3.4); const r = rng(9); for (let i = 0; i < 50; i++) { const x = r() * W, y = 870 + r() * 200; inkStroke(g, PL([[x, y], [x + 16 + r() * 26, y - 3]], false), 1.6, { a: .35 }); } }, 90);
    a4_put(ctx, fg, cm, .9);
    a4_dust(ctx, lt, { box: [-60, 560, W + 60, 980], n: 90, seed: 8, wind: 120, rise: -4, col: 'ochre', a: .5, size: 2.6 });
    // Mustafa Kemal: kefiye, haki setre; gönüllülere dönük (sola); göz kırpar
    ctx.save(); cam(ctx, cm, 1);
    const io = idleOffsets(tf, 3, .8), bl = blinkAt(t, 3);
    const o = { x: MK.x, y: MK.y + io.breath, s: MK.s, dir: -1 };
    bust(ctx, { ...o, coat: 'setre', col: 'khaki', w: .98, seed: 3, len: (H + 40 - MK.y) / MK.s, turn: .25 });
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
for (const [id, w] of [['E03', null], ['E04', null], ['E05', null], ['E06', null]]) {
  shot(S(id), (ctx, st) => { setReg(9); paperBG(ctx); txt(ctx, id, W / 2, H / 2, FONT.title(120), { align: 'center' }); }, { tr: { type: 'cut', dur: 0 } });
}
