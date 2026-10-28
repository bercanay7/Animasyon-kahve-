// act6: VI · KAPANIŞ (G01–G06). TBMM 29 Ekim akşamı "Yaşasın Cumhuriyet!" (ilk tam kırmızı bayrak) → üç büst ve
// Erkân-ı Harbiye diplomaları → 1924'te çatlayan kuşak şeridi → okul sırası / siper → bugünün sınıfı → soru kartı
// → son afiş → bitiş ekranı (sağ yarı boş). act0'ın a0_ yardımcılarını kullanır; kendi yardımcıları a6_ önekli.
'use strict';

// ——— bayrak ———
// düz bayrak (Türk Bayrağı Kanunu oranları: G yükseklik, L = 1,5G; ay dış çemberi G/2 çap, iç çember 2/5G, aralık G/16;
// yıldız çemberi G/4 çap, iç çemberden G/3 uzakta; bir ucu aya bakar)
function a6_flagImg(G) {
  const L = G * 1.5;
  return a0_cache('a6-flag-' + G, g => {
    const M = G / 30, field = PL([[0, 0], [L, 0], [L, G], [0, G]]);
    knock(g, field); plate(g, 'red', field); plate(g, 'red', PL([[0, 0], [M * 1.4, 0], [M * 1.4, G], [0, G]]), { a: .4 });
    const cx = M + G / 2, cy = G / 2, r1 = G / 4, cx2 = cx + G / 16, r2 = G / 5;
    const outer = new Path2D(); outer.arc(cx, cy, r1, 0, TAU);
    const inner = new Path2D(); inner.arc(cx2, cy, r2, 0, TAU);
    const notInner = new Path2D(); notInner.rect(-10, -10, L + 20, G + 20); notInner.arc(cx2, cy, r2, 0, TAU, true);
    g.save(); g.clip(outer); g.clip(notInner, 'evenodd'); g.fillStyle = '#F4EEDF'; g.fillRect(-10, -10, L + 20, G + 20); g.restore();
    const sx = cx2 + r2 + G / 3 + G / 8, star = a0_starPath(new Path2D(), sx, cy, G / 8, PI, .382);
    knock(g, star, '#F4EEDF');
    // ince is kontur (taş baskı): ay ve yıldız
    const cres = new Path2D(); cres.arc(cx, cy, r1, 0, TAU); inkStroke(g, cres, 1.4, { a: .45 });
    g.save(); g.clip(outer); inkStroke(g, inner, 1.4, { a: .45 }); g.restore();
    inkStroke(g, star, 1.3, { a: .45 });
  }, G * 1.5 + 2, G + 2);
}
// dalgalanan bayrak: x,y gönder ucundaki üst köşe; unfurl 0..1 (açılma), amp dalga genliği; poz 15 fps
function a6_flag(ctx, x, y, G, t, o = {}) {
  const img = a6_flagImg(G), L = G * 1.5, n = 54, sw = L / n, tf = Math.floor(t * 15) / 15;
  const vis = L * clamp(o.unfurl ?? 1), amp = o.amp ?? G * .09, sp = o.speed ?? 3.2;
  if (vis < 2) return;
  const dyAt = u => amp * Math.pow(u, .9) * Math.sin(u * TAU * 1.25 - tf * sp) + (o.droop ?? 0) * u * u * G;
  const top = [], bot = [], shade = new Path2D(), shade2 = new Path2D();
  for (let i = 0; i < n; i++) {
    const x0 = i * sw; if (x0 >= vis) break;
    const w = Math.min(sw, vis - x0), u = (x0 + w / 2) / L, dy = dyAt(u);
    ctx.drawImage(img, x0 * RS, 0, Math.max(1, (w + .8) * RS), G * RS, x + x0, y + dy, w + .8, G);
    const sl = (dyAt(u + .01) - dyAt(u - .01)) / (.02 * L);
    if (sl > .05) shade.rect(x + x0, y + dy, w + .8, G);
    if (sl > .12) shade2.rect(x + x0, y + dy, w + .8, G);
    top.push([x + x0, y + dy]); bot.push([x + x0, y + dy + G]);
    if (x0 + sw >= vis) { const de = dyAt(vis / L); top.push([x + vis, y + de]); bot.push([x + vis, y + de + G]); }
  }
  // kıvrım gölgesi: aynı kalıbın ikinci baskısı (gradyan yok)
  plate(ctx, 'red', shade, { a: .35 }); plate(ctx, 'ink', shade2, { a: .14 });
  const out = PL([...top, ...bot.slice().reverse()]);
  inkStroke(ctx, out, o.lw ?? 3.2);
}
// gönder: is çizgi + altın alem topu
function a6_pole(ctx, x, y0, y1, o = {}) {
  inkStroke(ctx, PL([[x, y0], [x, y1]], false), o.w || 9, { cap: 'butt' });
  cut(ctx, PL([[x - 2, y0 + 10], [x - 2, y1]], false), 1.6, { a: .3 });
  const b = new Path2D(); b.arc(x, y0 - 10, o.r || 13, 0, TAU); knock(ctx, b); plate(ctx, 'gold', b, { a: .9 }); plate(ctx, 'ochre', b, { a: .4 }); inkStroke(ctx, b, 2.6);
}

// ——— G01 · TBMM, 29 Ekim 1923 akşamı ———
// ayakta mebus silueti (profil, sağa dönük): baş + gövde + isteğe bağlı kalkık kol
function a6_deputy(ctx, x, y, s, kind, o = {}) {
  ctx.save();
  if (o.col) { // arka sıralar: tek kalıp (lacivert), is yok
    ctx.translate(x, y); ctx.rotate(o.tilt || 0); ctx.scale(s, s);
    const p = a0_profPath({ seed: o.seed, bot: 420 });
    plate(ctx, o.col, p, { a: o.a ?? .8, flat: true });
    if (kind === 'kalpak') plate(ctx, o.col, SP(A0_KALPAK, true, .25), { a: o.a ?? .8, flat: true });
    if (kind === 'fes') plate(ctx, o.col, SP(A0_FES, true, .2), { a: o.a ?? .8, flat: true });
    if (kind === 'sarik') plate(ctx, o.col, SP([[26, -40], [32, -62], [16, -86], [-14, -96], [-44, -88], [-62, -62], [-60, -30], [-20, -40]], true, .8), { a: o.a ?? .8, flat: true });
    if (o.arm) plate(ctx, o.col, a6_armPath(o.arm), { a: o.a ?? .8, flat: true });
    ctx.restore(); return;
  }
  ctx.restore();
  a0_prof(ctx, x, y, s, 1, kind, { ...o, bot: 420 });
  if (o.arm) { ctx.save(); ctx.translate(x, y); ctx.rotate(o.tilt || 0); ctx.scale(s, s); const ap = a6_armPath(o.arm); inkFill(ctx, ap); cut(ctx, SP([[30, 96], [44, 40], [40, -40]], false), 1.6 / s, { a: .3 }); ctx.restore(); }
}
// kalkık kol (yumruk / açık el): u 0..1 kalkış
function a6_armPath(u) {
  const ex = lerp(60, 48, u), ey = lerp(200, 30, u), hx = lerp(70, 54, u), hy = lerp(300, -90, u);
  const p = new Path2D();
  spl(p, [[20, 100], [ex + 14, ey], [hx + 13, hy + 6], [hx + 10, hy - 20], [hx - 12, hy - 22], [hx - 12, hy + 6], [ex - 14, ey], [-10, 110]], true, .6);
  return p;
}
function a6_shotTBMM() {
  const FL = { x: 1250, y: 210, G: 300 }; // gönder ucu ve bayrak yüksekliği
  shot(S('G01') - 1.0, (ctx, st) => {
    setReg(601);
    paperBG(ctx);
    const tY = a0_W('G01', 'yaşasın') - (st.t - st.lt); // yerel
    const p = ramp(st.lt, 0, st.d + .4, E.io2), c = { x: 960 + 50 * p, y: 540 - 20 * p, z: 1 + .06 * p };
    const [sx, sy] = shake(st.lt, tY, 5, 5, 18); c.sx = sx; c.sy = sy;
    const bg = a0_cache('a6-tbmm-bg', g => {
      paperBG(g);
      plate(g, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .3 });
      // tavan kirişi ve yüksek pencereler (gece)
      const beam = PL([[-20, -20], [W + 20, -20], [W + 20, 40], [-20, 44]]); plate(g, 'ochre', beam, { n: 2 }); plate(g, 'sepia', beam, { a: .4 }); inkStroke(g, PL([[-20, 44], [W + 20, 40]], false), 3.4);
      for (let i = 0; i < 6; i++) { const x0 = 70 + i * 196, win = PL([[x0, 70], [x0 + 110, 70], [x0 + 110, 150], [x0, 150]]); knock(g, win); plate(g, 'navy', win, { a: .85 }); halftone(g, 'navy', win, .3, { cell: 10 }); inkStroke(g, win, 3); inkStroke(g, PL([[x0 + 55, 70], [x0 + 55, 150]], false), 2.4); }
      // lambalar (yalnız lamba çevresi altın)
      for (const lx of [330, 900]) { for (const [rr, a] of [[120, .16], [74, .3]]) { const q = new Path2D(); q.ellipse(lx, 196, rr * 1.2, rr * .8, 0, 0, TAU); plate(g, 'gold', q, { a }); } }
      for (const lx of [330, 900]) gasLamp(g, lx, 186, .8, 0);
      // ahşap lambri
      const pan = PL([[-20, 610], [W + 20, 610], [W + 20, H + 20], [-20, H + 20]]); plate(g, 'ochre', pan, { n: 2 }); plate(g, 'sepia', pan, { a: .35 });
      inkStroke(g, PL([[-20, 610], [W + 20, 610]], false), 3.4);
      for (let x = 40; x < W; x += 150) inkStroke(g, PL([[x, 620], [x, H]], false), 1.6, { a: .45 });
      // kürsü arkasında "Hâkimiyet Milletindir" levhası (Osmanlıca soyut iz) ve başkanlık kürsüsü
      const lv = PL([[1430, 150], [1850, 150], [1850, 250], [1430, 250]]); plate(g, 'ink', PL([[1440, 160], [1860, 160], [1860, 260], [1440, 260]]), { a: .3 });
      knock(g, lv, P.paperD); inkStroke(g, lv, 3.6); inkStroke(g, PL([[1440, 160], [1840, 160], [1840, 240], [1440, 240]]), 1.2);
      scriptLine(g, 1820, 212, 360, 26, 611, { w: 3.6 });
      const k1 = PL(rough([[1400, 620], [1860, 620], [1880, 660], [1380, 660]], 1, 3)); knock(g, k1); plate(g, 'ochre', k1, { n: 2 }); inkStroke(g, k1, 3.2);
      const k2 = PL([[1400, 660], [1860, 660], [1860, H + 20], [1400, H + 20]]); knock(g, k2); plate(g, 'ochre', k2, { n: 2 }); plate(g, 'sepia', k2, { a: .5 }); inkStroke(g, k2, 3.2);
      for (const x of [1490, 1630, 1770]) inkStroke(g, PL([[x, 680], [x, H]], false), 2, { a: .5 });
      const kx = PL([[1520, 520], [1740, 520], [1760, 620], [1500, 620]]); knock(g, kx); plate(g, 'ochre', kx, { n: 2 }); plate(g, 'ink', kx, { a: .2 }); inkStroke(g, kx, 3);
    });
    a0_layer(ctx, bg, c, .75);
    ctx.save(); cam(ctx, c, .9);
    // bayrak: "Yaşasın"da gönderde açılır (ilk tam kırmızı); öncesinde gönder boş
    const un = ramp(st.lt, tY - .1, tY + .7, E.out3);
    a6_pole(ctx, FL.x, FL.y - 30, 980);
    a6_flag(ctx, FL.x + 5, FL.y, FL.G, st.t, { unfurl: un, amp: FL.G * lerp(.18, .09, un), droop: (1 - un) * .3 });
    ctx.restore();
    // kalabalık: üç derinlik; arka sıralarda tek kalıp, önde yüzü seçilen dört mebus
    const tf = Math.floor(st.t * 15) / 15, cheer = u0 => ramp(st.lt, tY + u0, tY + u0 + .25, E.out3);
    ctx.save(); cam(ctx, c, .95);
    const kinds = ['kalpak', 'fes', 'sarik', 'kalpak', 'bare', 'kalpak', 'fes', 'kalpak', 'bald', 'kalpak', 'fes', 'kalpak', 'sarik', 'kalpak'];
    for (let i = 0; i < 14; i++) { const x = 40 + i * 92, io = idleOffsets(tf, 700 + i, 1.5); a6_deputy(ctx, x, 470 + (i % 3) * 6, .62, kinds[i], { col: 'navy', a: .55, seed: 700 + i, tilt: io.head, arm: i % 3 === 1 ? cheer(.05 * i) : 0 }); }
    ctx.restore();
    ctx.save(); cam(ctx, c, 1);
    for (let i = 0; i < 10; i++) { const x = 10 + i * 128, io = idleOffsets(tf, 720 + i, 1.4); a6_deputy(ctx, x, 506 + (i % 2) * 10, .86, kinds[(i + 5) % 14], { col: 'navy', a: .9, seed: 720 + i, tilt: io.head * .7, arm: i % 2 === 0 ? cheer(.08 + .04 * i) : 0 }); }
    ctx.restore();
    ctx.save(); cam(ctx, c, 1.08);
    const front = [
      { x: 190, who: 'anon', id: { mus: 'gur', jaw: 1.08, seed: 81 }, gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 44, seed: 81 },
      { x: 500, who: 'anon', id: { mus: 'mk', hair: 'grey', WD: 1.1, seed: 82 }, gear: 'fes', coat: 'civil', col: 'navy', age: 50, seed: 82 },
      { x: 810, who: 'anon', id: { mus: 'pala', musCol: 'grey', hair: 'grey', seed: 83 }, gear: 'kalpak', gearCol: 'grey', coat: 'civil', col: 'ink', age: 52, seed: 83 },
      { x: 1110, who: 'anon', id: { mus: 'thin', WD: 1.04, seed: 84 }, gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 38, seed: 84 },
    ];
    front.forEach((f, i) => {
      const up = cheer(.12 + i * .07);
      a0_fig(ctx, { ...f, y: 560, s: 1.28, dir: 1, w: .98, len: 420, lookAt: [FL.x + 260, lerp(500, 300, up)], tilt: -.05 * up, sep: true, turn: .2 }, st.t);
    });
    ctx.restore();
    chapterCard(ctx, 'VI', 'CUMHURİYET', 'TBMM · 29 EKİM 1923 · 20.30', st.lt - .5, 5.2);
    bigStamp(ctx, 'YAŞASIN CUMHURİYET!', 640, 300, st.lt - tY, st.d - tY + 1, { size: 100 });
  }, { tr: { type: 'press', dur: .7 }, post: { vig: .95 } });
}

// ——— G02 · Üç büst, aynı kurmay okulu ———
function a6_diploma(ctx, x, y, rot, sd, lt, lab) {
  const h = a0_hit(lt, 0, .16); if (h.a <= 0) return;
  ctx.save(); ctx.globalAlpha = h.a; ctx.translate(x, y); ctx.scale(h.k, h.k); ctx.translate(-x, -y);
  paperSheet(ctx, x, y, 230, 150, rot, sd, { header: true, rows: 4 });
  // mühür: kırmızı lastik damga, içinde soyut yazı
  const sx = x + 66, sy = y + 34, ring = new Path2D(); ring.arc(sx, sy, 34, 0, TAU);
  const rb = REG.boost; REG.boost = rb * (1 + 4 * (1 - E.out3(clamp(lt / .3))));
  plate(ctx, 'red', ring, { a: .78 }); REG.boost = rb;
  const inner = new Path2D(); inner.arc(sx, sy, 26, 0, TAU); cut(ctx, inner, 2.2, { a: .8 }); cut(ctx, ring, 1.6, { a: .5 });
  scriptLine(ctx, sx + 16, sy + 4, 32, 7, sd + 9, { col: P.paper, w: 1.8 });
  ctx.restore();
  if (lab && !NOTEXT) { ctx.save(); ctx.globalAlpha = h.a; txt(ctx, lab, x, y + 128, FONT.mono(30), { align: 'center', ls: 3 }); ctx.restore(); }
}
function a6_shotUcBust() {
  const B0 = 130, B1 = 760, XS = [420, 960, 1500];
  shot(S('G02') - .35, (ctx, st) => {
    setReg(613);
    paperBG(ctx);
    const T0 = st.t - st.lt, p = ramp(st.lt, 0, st.d + .4, E.io2), c = { x: 960, y: 540 - 14 * p, z: 1.02 + .04 * p };
    const bg = a0_cache('a6-uc-bg', g => { paperBG(g); a0_band(g, B0, B1, 'ochre', .5); });
    a0_layer(ctx, bg, c, .85);
    const tM = a0_W('G02', 'cumhurbaşkanı') - T0, tI = a0_W('G02', 'ismet') - T0, tF = a0_W('G02', 'fevzi') - T0;
    const L = [
      { x: XS[1], app: tM - .25, who: 'mk', gear: null, coat: 'civil', col: 'ink', age: 42, seed: 3, name: 'MUSTAFA KEMAL', sub: 'Cumhurbaşkanı · 42', tn: tM, dip: 'ERKÂN-I HARBİYE · 1905' },
      { x: XS[0], app: tI - .15, who: 'ismet', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 39, seed: 5, name: 'İSMET', sub: 'Başvekil · 39', tn: tI, dip: 'ERKÂN-I HARBİYE · 1906' },
      { x: XS[2], app: tF - .15, who: 'fevzi', gear: 'kalpak', gearCol: 'grey', coat: 'kaput', col: 'khaki', age: 47, seed: 7, name: 'FEVZİ', sub: 'Erkân-ı Harbiye Reisi · 47', tn: tF, dip: 'ERKÂN-I HARBİYE · 1898' },
    ];
    ctx.save(); cam(ctx, c, 1);
    ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
    for (const f of L) {
      const h = a0_hit(st.lt, f.app, .14); if (h.a <= 0) continue;
      ctx.save(); ctx.globalAlpha = h.a; ctx.translate(f.x, B1); ctx.scale(h.k, h.k); ctx.translate(-f.x, -B1);
      const rb = REG.boost; REG.boost = rb * (1 + 5 * (1 - E.out3(clamp((st.lt - f.app) / .35))));
      a0_fig(ctx, { ...f, y: 438, s: 2.12, dir: -1, w: .98, len: (B1 - 438) / 2.12 + 10, look: [.3, .25], sep: true, idle: .8 }, st.t);
      REG.boost = rb; ctx.restore();
    }
    ctx.restore();
    ctx.restore();
    for (const f of L) nameTag(ctx, f.x, 640, f.name, f.sub, st.lt - f.tn, 3.4, { align: 'center', size: 44, sub: 28 });
    // "Üçü de aynı kurmay okulunun mezunuydu": diplomalar sırayla damgalanır
    const tD = a0_W('G02', 'üçü') - T0;
    [1, 0, 2].forEach((k, j) => a6_diploma(ctx, L[k].x, 852, [-.03, .02, -.015][k], 640 + k, st.lt - tD - j * .28, L[k].dip));
  }, { tr: { type: 'press', dur: .5 }, post: { vig: .9 } });
}

// ——— G03 · 1924: şerit çatlar; ama hepsi aynı yerden: okul sırası ve siper ———
const A6_SIX = [
  { who: 'karabekir', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 42, seed: 11, lab: 'KARABEKİR', w: 'karabekir' },
  { who: 'alifuat', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 42, seed: 13, lab: 'ALİ FUAT', w: 'ali' },
  { who: 'rauf', gear: null, coat: 'civil', col: 'navy', age: 43, seed: 15, lab: 'RAUF', w: 'rauf' },
  { who: 'mk', gear: null, coat: 'civil', col: 'ink', age: 43, seed: 3 },
  { who: 'ismet', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 40, seed: 5 },
  { who: 'fevzi', gear: 'kalpak', gearCol: 'grey', coat: 'kaput', col: 'khaki', age: 48, seed: 7 },
];
const A6_X6 = [236, 500, 764, 1156, 1420, 1684];
// yırtık kenar: üstten alta kırık çizgi
function a6_tearPts(x, y0, y1, sd) { const r = rng(sd), pts = []; for (let y = y0; y <= y1; y += 26) pts.push([x + (r() - .5) * 34, y]); pts[pts.length - 1][1] = y1; return pts; }
function a6_shotCatlak() {
  const B0 = 150, B1 = 720, TX = 960;
  shot(S('G03') - .2, (ctx, st) => {
    setReg(617);
    paperBG(ctx, P.paperD);
    const T0 = st.t - st.lt, p = ramp(st.lt, 0, st.d + .3, E.io2), c = { x: 960, y: 540, z: 1.0 + .03 * p };
    const tC = a0_W('G03', 'dörtte') - T0, tM = a0_W('G03', 'muhalefete') - T0, tA = a0_W('G03', 'ama') - T0;
    const crack = ramp(st.lt, tC - .1, tC + .35, E.out2);              // çatlak yukarıdan aşağı ilerler
    const sep = ramp(st.lt, tM - .2, tM + .7, E.io3) * (1 - ramp(st.lt, tA, tA + .9, E.io3)); // ayrılır, sonra yine yan yana
    const tear = a6_tearPts(TX, -40, H + 40, 77);
    const yC = lerp(-40, H + 40, crack);
    const halves = [
      { clip: PL([[-60, -60], ...tear.map(([x, y]) => [y <= yC ? x : W + 60, y]), [-60, H + 60]]), dx: -46 * sep, rot: -.012 * sep, idx: [0, 1, 2] },
      { clip: PL([[W + 60, -60], ...tear.map(([x, y]) => [y <= yC ? x : W + 60, y]), [W + 60, H + 60]]), dx: 0, rot: 0, idx: [3, 4, 5] },
    ];
    ctx.save(); cam(ctx, c, 1);
    halves.forEach((hv, k) => {
      ctx.save(); ctx.translate(hv.dx, 0); ctx.translate(TX, (B0 + B1) / 2); ctx.rotate(hv.rot); ctx.translate(-TX, -(B0 + B1) / 2);
      ctx.save(); if (crack > 0) ctx.clip(hv.clip); else if (k === 1) { ctx.restore(); ctx.restore(); return; }
      if (crack <= 0) { ctx.beginPath(); ctx.rect(-60, -60, W + 120, H + 120); ctx.clip(); }
      paperBG(ctx); a0_band(ctx, B0, B1, 'ochre', .5);
      ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
      for (const i of (crack > 0 ? hv.idx : [0, 1, 2, 3, 4, 5])) a0_fig(ctx, { ...A6_SIX[i], x: A6_X6[i], y: 412, s: 1.26, dir: -1, w: .96, len: (B1 - 412) / 1.26 + 10, look: [.3, .25], sep: true }, st.t);
      ctx.restore();
      // adlar: ayrılan üçü, söylendikleri anda
      for (const i of (crack > 0 ? hv.idx : [0, 1, 2])) if (A6_SIX[i].lab) { const tl = a0_W('G03', A6_SIX[i].w) - T0; label(ctx, A6_SIX[i].lab, A6_X6[i], 812, FONT.mono(34), { align: 'center', ls: 4, a: ramp(st.lt, tl, tl + .3) }); }
      ctx.restore();
      if (crack > 0) inkStroke(ctx, PL(tear.filter(([, y]) => y <= yC + 26).map(([x, y]) => [x, Math.min(y, yC)]), false), 3.4);
      ctx.restore();
    });
    ctx.restore();
    stamp(ctx, 'TERAKKİPERVER FIRKA · 1924', 70, 930, st.lt - tM - .2, tA - tM + .7, { size: 32 });
    // 1924 damgası (çatlakla birlikte)
    label(ctx, '1924', W / 2, 108, FONT.title(78), { align: 'center', ls: 4, a: ramp(st.lt, tC - .3, tC) });
    if (!NOTEXT) { const ty = ramp(st.lt, tA + .4, tA + .9); label(ctx, 'AYNI YERDEN', W / 2, 960, FONT.title(64), { align: 'center', ls: 4, a: ty }); }
  }, { tr: { type: 'cut' }, post: { vig: .9 } });
  // "bir okul sırasından…": 1893 mektep sırası (A04 ile aynı kare; geri dönüş)
  shot(a0_W('G03', 'okul') - .15, (ctx, st) => {
    setReg(137);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d, E.io2), c = { x: 960 + 26 * p, y: 540, z: 1.04 + .03 * p };
    const bg = a0_cache('a0-k93-bg', g => a0_classBG(g, 150, 740));
    a0_layer(ctx, bg, c, .8);
    ctx.save(); cam(ctx, c, 1); a0_classKids(ctx, st.t, 150, 740); ctx.restore();
    A0_ORD.forEach((i, k) => a0_age(ctx, A0_XS[i], 862, A0_AGE93[i], 'yaşında', st.lt + .3 - k * .06));
    label(ctx, '1893', W / 2, 108, FONT.title(78), { align: 'center', ls: 4 });
  }, { tr: { type: 'cut' }, post: { vig: .9 } });
  // "…ve bir siperden": aynı sıra, kabalaklı, siperde omuz omuza (1915)
  shot(a0_W('G03', 'siperden') - .2, (ctx, st) => {
    setReg(621);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d, E.io2), c = { x: 960 - 24 * p, y: 540, z: 1.04 + .03 * p };
    const bg = a0_cache('a6-siper-bg', g => {
      paperBG(g);
      const band = PL([[-20, 150], [W + 20, 150], [W + 20, 740], [-20, 740]]);
      plate(g, 'khaki', band, { a: .3 });
      // gök: duman (raster) — başların uzağında, üst şeritte
      g.save(); g.beginPath(); g.rect(-20, 150, W + 40, 120); g.clip();
      const rs = rng(9);
      for (const [x, y, r] of [[300, 196, 70], [1100, 186, 90], [1700, 204, 60]]) { const q = new Path2D(); for (let k = 0; k < 7; k++) { const a = k / 7 * PI, rr = r * (.55 + rs() * .5); q.moveTo(x + Math.cos(a) * r * 1.4 + rr, y - Math.sin(a) * r * .4); q.arc(x + Math.cos(a) * r * 1.4, y - Math.sin(a) * r * .4, rr, 0, TAU); } halftone(g, 'ink', q, .12, { cell: 12 }); }
      g.restore();
      // arka siper duvarı + tel örgü kazıkları
      const back = SP([[-20, 330], [300, 318], [700, 334], [1100, 320], [1500, 336], [W + 20, 324], [W + 20, 740], [-20, 740]], true, .5);
      plate(g, 'khaki', back, { n: 2 }); plate(g, 'ochre', back, { a: .3 }); inkStroke(g, SP([[-20, 330], [300, 318], [700, 334], [1100, 320], [1500, 336], [W + 20, 324]], false, .5), 3);
      for (let x = 60; x < W; x += 210) { inkStroke(g, PL([[x, 330], [x + 6, 250]], false), 4); }
      for (let x = 60; x < W - 210; x += 210) for (const yy of [262, 290]) inkStroke(g, SP([[x + 6, yy], [x + 60, yy + 10], [x + 110, yy - 6], [x + 214, yy]], false), 1.6, { a: .7 });
      inkStroke(g, PL([[-20, 150], [W + 20, 150]], false), 4); inkStroke(g, PL([[-20, 740], [W + 20, 740]], false), 4);
    });
    a0_layer(ctx, bg, c, .8);
    ctx.save(); cam(ctx, c, 1);
    ctx.save(); ctx.beginPath(); ctx.rect(-40, 152, W + 80, 586); ctx.clip();
    const kab = [{ who: 'anon', id: { mus: 'mk', seed: 31 } }, { who: 'ismet' }, { who: 'mk' }, { who: 'karabekir' }, { who: 'alifuat' }];
    // süngü uçları (başların arkasında)
    for (let i = 0; i < 5; i++) { const x = A0_XS[i] + 90; inkStroke(ctx, PL([[x, 640], [x + 30, 240]], false), 6); inkFill(ctx, PL([[x + 27, 250], [x + 33, 250], [x + 34, 190]])); }
    kab.forEach((f, i) => a0_fig(ctx, { ...f, x: A0_XS[i], y: 430, s: 1.26, dir: -1, w: .96, len: 260, age: 34, gear: 'kabalak', coat: 'setre', col: 'khaki', look: [.3, .25], sep: true, seed: 90 + i }, st.t));
    // ön siper: kum torbaları
    const r = rng(5);
    for (let row = 0; row < 3; row++) for (let i = -1; i < 14; i++) {
      const x = i * 150 + (row % 2) * 75, y = 590 + row * 52, sb = SP(rough([[x, y], [x + 150, y + 2], [x + 152, y + 52], [x - 2, y + 54]], 4, row * 31 + i), true, .9);
      knock(ctx, sb); plate(ctx, 'khaki', sb, { a: .7 + r() * .2 }); plate(ctx, 'ochre', sb, { a: .3 }); inkStroke(ctx, sb, 2.6);
      inkStroke(ctx, SP([[x + 20, y + 14], [x + 70, y + 10], [x + 130, y + 16]], false), 1.2, { a: .4 });
    }
    ctx.restore();
    ctx.restore();
    [31, 31, 34, 33, 33].forEach((a, i) => a0_age(ctx, A0_XS[i], 862, a, 'yaşında', st.lt + .3 - Math.abs(i - 2) * .06));
    label(ctx, '1915', W / 2, 108, FONT.title(78), { align: 'center', ls: 4 });
  }, { tr: { type: 'cut' }, post: { vig: .9 } });
}

// ——— G04 · Bugünün sınıfı (Latin harf serbest) ———
// uzun saç (başın arkası; baş koordinatı): 'bob' | 'pony'
function a6_hair(ctx, x, y, s, dir, tilt, f) {
  const pp = { ...PEOPLE.anon, ...(f.id || {}) }, WD = pp.WD ?? 1.08, HY = pp.HY ?? 1;
  ctx.save(); ctx.translate(x, y); ctx.rotate(tilt || 0); ctx.scale(s * dir * WD, s * HY);
  let p;
  if (f.style === 'pony') p = SP([[-48, -40], [-62, -36], [-70, -14], [-74, 20], [-70, 52], [-62, 58], [-60, 26], [-56, -4], [-46, -24]], true, .8);
  else p = SP([[-4, -68], [-34, -66], [-58, -50], [-66, -20], [-66, 14], [-60, 34], [-46, 38], [-34, 32], [-28, 12], [-26, -8]], true, .8);
  knock(ctx, p);
  if (pp.hair === 'ink') { inkFill(ctx, p); cut(ctx, SP([[-40, -50], [-60, -10], [-62, 40]], false), 1.8 / s, { a: .35 }); }
  else { plate(ctx, pp.hair, p, { a: .6 }); plate(ctx, 'gold', p, { a: .3 }); inkStroke(ctx, p, 2.4 / s); inkStroke(ctx, SP([[-40, -50], [-60, -10], [-62, 30]], false), 1.4 / s, { a: .5 }); }
  if (f.style === 'pony') { const tie = PL([[-50, -42], [-62, -40], [-60, -30], [-48, -32]]); knock(ctx, tie); plate(ctx, 'red', tie, { a: .9 }); inkStroke(ctx, tie, 1.6 / s); }
  ctx.restore();
}
// beyaz gömlek yakası (büst koordinatı)
function a6_collar(ctx, x, y, s, dir, tilt) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(tilt || 0); ctx.scale(s * dir, s);
  for (const w of [[[-27, 72], [-6, 100], [-33, 96]], [[16, 74], [2, 100], [27, 92]]]) { const q = PL(w); knock(ctx, q); inkStroke(ctx, q, 2.2 / s); }
  ctx.restore();
}
const A6_KIDS = [
  { id: { mus: null, hair: 'ink', WD: 1.06, jaw: .96, browW: .75, seed: 51 }, style: 'pony', col: 'teal' },
  { id: { mus: null, hair: 'sepia', WD: 1.1, jaw: 1.02, seed: 52 }, col: 'navy' },
  { id: { mus: null, hair: 'sepia', WD: 1.04, jaw: .94, browW: .7, seed: 53 }, style: 'bob', col: 'ochre' },
  { id: { mus: null, hair: 'ink', WD: 1.12, jaw: 1.04, seed: 54 }, col: 'khaki' },
  { id: { mus: null, hair: 'ink', WD: 1.04, jaw: .95, browW: .72, seed: 55 }, style: 'bob', col: 'navy' },
];
function a6_shotBugun() {
  const B0 = 150, B1 = 740;
  shot(S('G04') - .3, (ctx, st) => {
    setReg(631);
    paperBG(ctx);
    const T0 = st.t - st.lt, p = ramp(st.lt, 0, st.d + .3, E.io2), c = { x: 944 + 36 * p, y: 540 - 10 * p, z: 1.02 + .04 * p };
    const bg = a0_cache('a6-bugun-bg', g => {
      paperBG(g);
      a0_band(g, B0, B1, 'ochre', .25);
      g.save(); g.beginPath(); g.rect(-20, B0 + 2, W + 40, B1 - B0 - 4); g.clip();
      a0_board(g, 120, 196, 1800, 560, 41, { green: true });
      // tahtanın sağ üstünde tarih (öğretmen yazısı)
      txt(g, '29 Ekim 2026', 1770, 250, FONT.quote(44), { align: 'right', col: '#EDE6D2' });
      a0_chalkGeo(g, [['tri', 250, 300, .55]], .7);
      g.restore();
      inkStroke(g, PL([[-20, B0], [W + 20, B0]], false), 4); inkStroke(g, PL([[-20, B1], [W + 20, B1]], false), 4);
    });
    a0_layer(ctx, bg, c, .8);
    ctx.save(); cam(ctx, c, 1);
    // tebeşir: "yazılır"da yazı harf harf belirir
    const tw = a0_W('G04', 'bugünkü') - T0, s1 = 'Cumhuriyet 103 yaşında';
    const n = Math.floor(clamp((st.lt - tw) / 1.5) * s1.length);
    if (n > 0) txt(ctx, s1.slice(0, n), 960, 312, FONT.quote(76), { align: 'center', col: '#EDE6D2' });
    ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
    A6_KIDS.forEach((f, i) => a0_fig(ctx, { who: 'anon', id: f.id, x: A0_XS[i], y: 452, s: 1.2, dir: -1, w: .84, len: (B1 - 452) / 1.2 + 10, age: 12, gear: null, coat: 'plain', col: f.col, look: [.2, .25], sep: true, seed: 60 + i,
      under: (cx, x, y, s, dir, tl) => { a6_collar(cx, x, y, s, dir, tl); if (f.style) a6_hair(cx, x, y, s, dir, tl, f); } }, st.t));
    a0_desk(ctx, -30, W + 30, 660, B1, 79, { pl: 'ochre', books: [[380, 90, 10, 'teal'], [1090, 80, 12, 'ochre'], [1460, 86, 10, 'navy']] });
    ctx.restore();
    ctx.restore();
    const tO = a0_W('G04', 'otuz') - T0, now = [12, 11, 12, 13, 12];
    A0_ORD.forEach((i, k) => {
      const tk = tO + k * .12, out = 1 - ramp(st.lt, tk - .12, tk);
      if (out > 0) a0_age(ctx, A0_XS[i], 862, now[i], 'yaşında', st.lt - .2 - k * .1, { a: out });
      if (st.lt >= tk) a0_age(ctx, A0_XS[i], 862, now[i] + 30, '2056’da', st.lt - tk);
    });
    label(ctx, '2026', W / 2, 108, FONT.title(78), { align: 'center', ls: 4 });
  }, { tr: { type: 'press', dur: .6 }, post: { vig: .9 } });
}

// ——— G05 · Soru kartı + öğretmen silueti ———
// ayakta öğretmen (profil, sağa dönük; 1920'ler kadın öğretmen: kısa saç, ceket, etek), kitap ve tebeşir
function a6_teacher(ctx, x, y, s, t) {
  const tf = Math.floor(t * 15) / 15, io = idleOffsets(tf, 91, 1.4);
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(io.torso * .5);
  const lw = px => px / s;
  // gövde profili (sağa dönük): küt saç, ceket, diz altı etek
  const body = SP([[-6, -306], [18, -298], [24, -282], [23, -273], [31, -262], [25, -257], [27, -251], [23, -247], [25, -239], [12, -233], [10, -222], [16, -210], [36, -200], [46, -172], [46, -148], [36, -92], [44, -40], [58, 40], [-56, 40], [-40, -40], [-30, -92], [-38, -160], [-36, -196], [-14, -222], [-24, -232], [-36, -250], [-38, -276], [-28, -296]], true, .55);
  inkFill(ctx, body);
  for (const [x0, x1] of [[12, 28], [-20, -5]]) { const leg = PL([[x0, 38], [x1, 38], [x1 - 1, 214], [x0 + 1, 214]]); inkFill(ctx, leg); }
  inkFill(ctx, SP([[12, 212], [30, 212], [44, 222], [42, 229], [10, 229]], true, .5)); inkFill(ctx, SP([[-20, 212], [-4, 212], [8, 222], [6, 229], [-22, 229]], true, .5));
  // kazımalar: saç çizgisi, yaka, kemer, etek kıvrımı, ışık kenarı
  cut(ctx, SP([[18, -298], [2, -290], [-14, -276], [-24, -250]], false), lw(2), { a: .4 });
  cut(ctx, SP([[12, -216], [24, -196], [14, -172]], false), lw(2), { a: .45 });
  cut(ctx, PL([[-34, -92], [38, -92]], false), lw(2), { a: .35 });
  cut(ctx, SP([[4, -40], [8, 0], [6, 36]], false), lw(1.6), { a: .3 });
  cut(ctx, SP([[18, -298], [24, -282], [23, -273], [31, -262]], false, .5), lw(2.2), { a: .55 });
  // önde sarkan kolun tuttuğu kitap
  const bk = PL([[24, -130], [64, -126], [60, -62], [20, -66]]); inkFill(ctx, bk); cut(ctx, PL([[60, -124], [57, -64]], false), lw(3), { a: .7 });
  // tebeşir tutan kol: tahtaya doğru (geriye) kalkar, dirsek bükük; poz 15 fps
  const u = .5 + .5 * Math.sin(tf * 1.3), sh = [-22, -194], el = [-66, -156 + 4 * u], hd = [-104 - 6 * u, -206 + 6 * u];
  const arm = new Path2D(); arm.moveTo(sh[0], sh[1]); arm.lineTo(el[0], el[1]); arm.lineTo(hd[0], hd[1]);
  inkStroke(ctx, arm, 22, { cap: "round" });
  const hand = new Path2D(); hand.ellipse(hd[0] - 4, hd[1] - 6, 9, 11, -.6, 0, TAU); inkFill(ctx, hand);
  const ch = PL([[hd[0] - 10, hd[1] - 16], [hd[0] - 22, hd[1] - 24], [hd[0] - 19, hd[1] - 29], [hd[0] - 7, hd[1] - 21]]); knock(ctx, ch);
  ctx.restore();
}
function a6_shotSoru() {
  shot(S('G05') - .3, (ctx, st) => {
    setReg(641);
    paperBG(ctx);
    const T0 = st.t - st.lt, p = ramp(st.lt, 0, st.d + .3, E.io2), c = { x: 960 - 30 * p, y: 540, z: 1 + .04 * p };
    const bg = a0_cache('a6-soru-bg', g => {
      paperBG(g);
      plate(g, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .28 });
      a0_board(g, 70, 190, 760, 700, 43);
      a0_chalkGeo(g, [['tri', 260, 330, .9], ['circ', 560, 330, .8], ['ang', 200, 560, .9], ['arc', 560, 520, .8]]);
      const fl = PL([[-20, 900], [W + 20, 900], [W + 20, H + 20], [-20, H + 20]]); plate(g, 'ochre', fl, { n: 2 }); plate(g, 'sepia', fl, { a: .4 }); inkStroke(g, PL([[-20, 900], [W + 20, 900]], false), 3);
    });
    a0_layer(ctx, bg, c, .7);
    ctx.save(); cam(ctx, c, 1); a6_teacher(ctx, 900, 672, 1.0, st.t); ctx.restore();
    // soru kartı
    const tc = a0_W('G05', 'sizin') - T0, h = a0_hit(st.lt, tc - .1, .2);
    if (h.a > 0 && !NOTEXT) {
      const x0 = 1080, y0 = 220, w = 760, hh = 560;
      ctx.save(); ctx.globalAlpha = h.a; ctx.translate(x0 + w / 2, y0 + hh / 2); ctx.scale(h.k, h.k); ctx.translate(-(x0 + w / 2), -(y0 + hh / 2));
      plate(ctx, 'ink', PL([[x0 + 14, y0 + 16], [x0 + w + 14, y0 + 16], [x0 + w + 14, y0 + hh + 16], [x0 + 14, y0 + hh + 16]]), { a: .4 });
      const card = PL(rough([[x0, y0], [x0 + w, y0], [x0 + w, y0 + hh], [x0, y0 + hh]], 1, 9));
      knock(ctx, card); inkStroke(ctx, card, 4); inkStroke(ctx, PL([[x0 + 16, y0 + 16], [x0 + w - 16, y0 + 16], [x0 + w - 16, y0 + hh - 16], [x0 + 16, y0 + hh - 16]]), 1.6);
      const cx = x0 + w / 2;
      txt(ctx, 'SİZİN HAYATINIZDA', cx, y0 + 130, FONT.title(66), { align: 'center', ls: 2 });
      txt(ctx, 'İZ BIRAKAN', cx, y0 + 250, FONT.title(96), { align: 'center', ls: 2 });
      txt(ctx, 'ÖĞRETMEN', cx - 34, y0 + 384, FONT.title(108), { align: 'center', ls: 2 });
      ctx.save(); ctx.font = FONT.title(108); ctx.letterSpacing = '2px'; const qw = ctx.measureText('ÖĞRETMEN').width; ctx.restore();
      txt(ctx, '?', cx - 34 + qw / 2 + 10, y0 + 384, FONT.title(108), { plate: 'red' });
      plate(ctx, 'red', PL([[x0 + 90, y0 + 420], [x0 + w - 90, y0 + 420], [x0 + w - 90, y0 + 428], [x0 + 90, y0 + 428]]));
      ctx.restore();
      const ty = a0_W('G05', 'yorumlara') - T0;
      label(ctx, 'Yorumlara yazın.', x0 + w / 2, y0 + 500, FONT.quote(52), { align: 'center', a: h.a * ramp(st.lt, ty - .1, ty + .3) });
    }
  }, { tr: { type: 'press', dur: .5 }, post: { vig: .9 } });
}

// ——— G06 · Son afiş ———
function a6_shotAfis() {
  const B0 = 330, B1 = 760;
  shot(S('G06') - .3, (ctx, st) => {
    setReg(651);
    paperBG(ctx);
    const T0 = st.t - st.lt, p = ramp(st.lt, 0, st.d + .3, E.io2), c = { x: 960, y: 540 + 10 * p, z: 1.05 - .05 * p };
    const bg = a0_cache('a6-afis-bg', g => { paperBG(g); a0_band(g, B0, B1, 'ochre', .5); });
    a0_layer(ctx, bg, c, .85);
    ctx.save(); cam(ctx, c, .9);
    a6_pole(ctx, 700, 70, 330, { w: 7, r: 10 });
    a6_flag(ctx, 704, 82, 220, st.t, { amp: 18, speed: 2.6 });
    ctx.restore();
    ctx.save(); cam(ctx, c, 1);
    ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
    a0_seven(ctx, st.t, st.lt, [-9, -9, -9, -9, -9, -9, -9], { y: 524, s: 1.0, yb: B1, xs: [240, 480, 720, 960, 1200, 1440, 1680] });
    ctx.restore();
    ctx.restore();
    if (!NOTEXT) {
      const t1 = a0_W('G06', 'cumhuriyetimizin') - T0, t2 = a0_W('G06', 'kutlu') - T0;
      const h1 = a0_hit(st.lt, t1, .2), h2 = a0_hit(st.lt, t2, .2);
      if (h1.a > 0) { ctx.save(); ctx.globalAlpha = h1.a; ctx.translate(960, 876); ctx.scale(h1.k, h1.k); txt(ctx, 'CUMHURİYETİMİZİN 103. YILI', 0, 0, FONT.title(88), { align: 'center', ls: 2 }); ctx.restore(); }
      if (h2.a > 0) {
        ctx.save(); ctx.globalAlpha = h2.a; ctx.translate(960, 990); ctx.scale(h2.k, h2.k); txt(ctx, 'KUTLU OLSUN', 0, 0, FONT.title(88), { align: 'center', ls: 6, plate: 'red' }); ctx.restore();
      }
      const ta = a0_W('G06', 'atatürkü') - T0;
      label(ctx, '29 EKİM 1923 — 29 EKİM 2026', 1220, 210, FONT.mono(34), { align: 'left', ls: 4, a: ramp(st.lt, ta, ta + .5) });
    }
  }, { tr: { type: 'press', dur: .6 }, post: { vig: .9 } });
}

// ——— Bitiş ekranı (~13 sn): solda sakin afiş, sağ yarı boş (YouTube abone ve video öğeleri) ———
function a6_shotBitis() {
  shot(Se('G06') + .5, (ctx, st) => {
    setReg(661);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d, E.sine), c = { x: 960, y: 540 - 8 * p, z: 1.0 + .015 * p };
    const X0 = 70, Y0 = 70, X1 = 890, Y1 = 1010;
    const bg = a0_cache('a6-bitis-bg', g => {
      paperBG(g);
      const sh = PL([[X0 + 14, Y0 + 16], [X1 + 14, Y0 + 16], [X1 + 14, Y1 + 16], [X0 + 14, Y1 + 16]]); plate(g, 'ink', sh, { a: .3 });
      const pan = PL(rough([[X0, Y0], [X1, Y0], [X1, Y1], [X0, Y1]], 1, 3)); knock(g, pan); plate(g, 'ochre', pan, { a: .3 });
      inkStroke(g, pan, 4); inkStroke(g, PL([[X0 + 16, Y0 + 16], [X1 - 16, Y0 + 16], [X1 - 16, Y1 - 16], [X0 + 16, Y1 - 16]]), 1.6);
      const st_ = PL([[X0 + 16, 812], [X1 - 16, 812], [X1 - 16, 994], [X0 + 16, 994]]); plate(g, 'ochre', st_, { a: .45 }); inkStroke(g, PL([[X0 + 16, 812], [X1 - 16, 812]], false), 3);
    });
    a0_layer(ctx, bg, c, 1);
    ctx.save(); cam(ctx, c, 1);
    a6_pole(ctx, 300, 120, 400, { w: 6, r: 9 });
    a6_flag(ctx, 303, 132, 200, st.t, { amp: 14, speed: 2.2 });
    // alt şerit: yedi baş küçük ölçekte
    ctx.save(); ctx.beginPath(); ctx.rect(X0 + 18, 814, X1 - X0 - 36, 178); ctx.clip();
    a0_seven(ctx, st.t, 9, [-9, -9, -9, -9, -9, -9, -9], { y: 900, s: .66, yb: 994, xs: [160, 266, 372, 480, 588, 694, 800], look: [.3, .25] });
    ctx.restore();
    ctx.restore();
    label(ctx, '29 EKİM 1923', 480, 470, FONT.mono(36), { align: 'center', ls: 6, force: true });
    label(ctx, '103. YIL', 480, 640, FONT.title(150), { align: 'center', ls: 4, force: true });
    label(ctx, 'KUTLU OLSUN', 480, 740, FONT.title(64), { align: 'center', ls: 6, force: true, plate: 'red' });
  }, { tr: { type: 'press', dur: .8 }, post: { vig: .7 } });
}

a6_shotTBMM();
a6_shotUcBust();
a6_shotCatlak();
a6_shotBugun();
a6_shotSoru();
a6_shotAfis();
a6_shotBitis();
