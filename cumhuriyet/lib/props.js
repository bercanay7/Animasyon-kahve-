// Nesneler ve ortam: kurmay haritası, gaz lambası, duvar, pencere manzarası, masa, dürbün, pusula, telgrafname, damga siluetler
'use strict';

// Kurmay haritası (yerel 1000×650 birim) — Sakarya meydan muharebesi bölgesi, şematik
// o: {x,y,w,rot, front: 0..1 (cephe hattının çizilme oranı), arrows: 0..1, focus:[u,v] (açık havuz merkezi)}
// Sırt tarama (tırtıl): omurga boyunca normal yönünde çizgiler; boy L = Lmax·sin(πu); güneydoğu yüz kalın
function ridge(ctx, spine, Lmax, lwf, seed) {
  const r = rng(seed), n = spine.length;
  let tot = 0; const seg = []; for (let i = 0; i < n - 1; i++) { const l = Math.hypot(spine[i + 1][0] - spine[i][0], spine[i + 1][1] - spine[i][1]); seg.push(l); tot += l; }
  plate(ctx, 'khaki', (() => { const p = new Path2D(); for (let side of [1, -1]) { } spl(p, spine.map(([x, y]) => [x, y]), false); return p; })(), { a: 0 });
  for (let d = 0; d <= tot; d += 7) {
    let k = 0, acc = 0; while (k < seg.length - 1 && acc + seg[k] < d) { acc += seg[k]; k++; }
    const f = (d - acc) / seg[k], p0 = spine[k], p1 = spine[k + 1];
    const x = lerp(p0[0], p1[0], f), y = lerp(p0[1], p1[1], f), an = Math.atan2(p1[1] - p0[1], p1[0] - p0[0]);
    const u = d / tot, L = Lmax * Math.sin(PI * u) * (.85 + r() * .3);
    for (const sd of [1, -1]) {
      const na = an + sd * PI / 2, nx = Math.cos(na), ny = Math.sin(na);
      const se = .5 + .5 * Math.cos(na - PI / 4); // güneydoğu yüz
      inkStroke(ctx, PL([[x + nx * 3, y + ny * 3], [x + nx * (3 + L), y + ny * (3 + L)]], false), lwf(1.0 + 1.2 * se), { cap: 'butt', a: .55 + .4 * se });
    }
  }
  const top = spine[Math.floor(n / 2)];
  inkFill(ctx, PL([[top[0], top[1] - 9], [top[0] + 8, top[1] + 5], [top[0] - 8, top[1] + 5]]));
}
function staffMap(ctx, o) {
  const sc = o.w / 1000, hh = 650;
  ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(o.rot || 0); ctx.scale(sc, sc);
  const lw = px => px / sc;
  const sheet = PL(rough([[0, 0], [1000, 0], [1000, hh], [0, hh]], 2.5, 41));
  plate(ctx, 'ink', PL([[14, 16], [1016, 16], [1016, hh + 16], [14, hh + 16]]), { a: .25 });
  knock(ctx, sheet, P.paperD); plate(ctx, 'ochre', sheet, { a: .15 });
  // odak çevresinde açık havuz
  const F = o.focus || [640, 330];
  ctx.save(); ctx.clip(sheet);
  const pool = new Path2D(); pool.ellipse(F[0], F[1], 250, 210, 0, 0, TAU); knock(ctx, pool, P.paper);
  radialHT(ctx, 'sepia', F[0], F[1], 170, 330, 0, .2, { cell: 10, box: [F[0] - 340, F[1] - 300, F[0] + 340, F[1] + 300], sy: .85 });
  ctx.restore();
  inkStroke(ctx, PL([[24, 24], [976, 24], [976, hh - 24], [24, hh - 24]]), lw(2.6));
  inkStroke(ctx, PL([[34, 34], [966, 34], [966, hh - 34], [34, hh - 34]]), lw(1.2), { a: .8 });
  for (let x = 34; x < 966; x += 40) inkFill(ctx, PL([[x, 24], [x + 20, 24], [x + 20, 34], [x, 34]]));
  // nehir: Sakarya, kuzeyde ince, güneye doğru kalınlaşan tek çizgi; içinde su çizgileri
  const river = [[560, 34], [540, 110], [470, 170], [380, 190], [300, 250], [290, 330], [350, 400], [460, 430], [520, 500], [500, 580], [470, 616]];
  const rp = new Path2D(); spl(rp, river, false, 1);
  for (let i = 0; i < river.length - 1; i++) { const q = new Path2D(); spl(q, river.slice(Math.max(0, i - 1), i + 3), false); }
  ctx.save(); ctx.lineCap = 'round';
  for (let i = 0; i < 10; i++) { const p = new Path2D(); spl(p, river.slice(i, i + 2 <= river.length ? i + 2 : river.length), false); inkStroke(ctx, p, lw(3 + i * .55)); }
  ctx.restore();
  inkStroke(ctx, rp, lw(1.2), { col: P.paper, a: .9 });
  const trib = SP([[290, 330], [210, 360], [130, 350], [60, 380]], false); inkStroke(ctx, trib, lw(2.6));
  // sırtlar (Duatepe, Çal, Mangal, Karadağ …): uzun, gürültülü omurgalar
  const R = [[[640, 300], [690, 288], [740, 300]], [[720, 470], [780, 455], [840, 470], [880, 462]], [[600, 150], [650, 140], [700, 152]], [[790, 210], [840, 200], [880, 214]], [[140, 470], [200, 458], [260, 472], [300, 466]], [[110, 190], [160, 180], [210, 192]]];
  R.forEach((sp, i) => ridge(ctx, sp, 26, lw, 30 + i));
  // demiryolu: kesik çift çizgi
  const rail = SP([[980, 90], [860, 120], [740, 100], [600, 70], [420, 60], [200, 90], [30, 110]], false);
  inkStroke(ctx, rail, lw(6)); inkStroke(ctx, rail, lw(3), { col: P.paperD });
  ctx.save(); ctx.setLineDash([lw(14), lw(14)]); inkStroke(ctx, rail, lw(3)); ctx.restore();
  for (const [x, y] of [[860, 120], [600, 70], [420, 60], [240, 560]]) inkFill(ctx, PL([[x - 9, y - 9], [x + 9, y - 9], [x + 9, y + 9], [x - 9, y + 9]]));
  // açıklayıcı Latin etiketler (izleyici katmanı) + altında küçük Osmanlıca iz
  txt(ctx, 'Sakarya', 228, 262, `italic 600 ${34}px "Cormorant Garamond"`, { col: P.ink });
  txt(ctx, 'DUATEPE', 640, 340, FONT.mono(22), { col: P.ink, ls: 3 });
  txt(ctx, 'POLATLI', 812, 160, FONT.mono(22), { col: P.ink, ls: 3 });
  for (const [x, y, L, sd] of [[880, 186, 70, 1], [700, 366, 70, 2], [330, 296, 80, 3], [860, 520, 100, 5], [330, 560, 110, 6]]) scriptLine(ctx, x, y, L, 10, sd + 50, { w: lw(1.8), a: .8 });
  // başlık kartuşu
  const cart = PL([[52, hh - 130], [300, hh - 130], [300, hh - 52], [52, hh - 52]]); knock(ctx, cart, P.paper); inkStroke(ctx, cart, lw(2.2)); inkStroke(ctx, PL([[58, hh - 124], [294, hh - 124], [294, hh - 58], [58, hh - 58]]), lw(1));
  scriptLine(ctx, 284, hh - 98, 210, 12, 77, { w: lw(2) }); scriptLine(ctx, 250, hh - 70, 150, 9, 78, { w: lw(1.6) });
  // ölçek çubuğu
  for (let i = 0; i < 6; i++) { const q = PL([[700 + i * 40, hh - 70], [740 + i * 40, hh - 70], [740 + i * 40, hh - 58], [700 + i * 40, hh - 58]]); i % 2 ? inkStroke(ctx, q, lw(1.4)) : inkFill(ctx, q); }
  // cephe hattı: Türk mevzileri (kırmızı tarak)
  const front = [[640, 60], [610, 140], [600, 230], [630, 320], [680, 390], [700, 470], [680, 560], [650, 610]];
  const fr = clamp(o.front ?? 1);
  if (fr > 0) {
    const fp = new Path2D(); spl(fp, front, false);
    ctx.save(); ctx.setLineDash([620 * fr, 9999]); inkStroke(ctx, fp, lw(9), { col: P.red, cap: 'butt', mode: 'multiply' }); ctx.restore();
    for (let i = 0; i < 30; i++) {
      const u = i / 30; if (u > fr) break;
      const sg = Math.min(front.length - 2, Math.floor(u * (front.length - 1))), f = u * (front.length - 1) - sg;
      const a = front[sg], b = front[sg + 1], x = lerp(a[0], b[0], f), y = lerp(a[1], b[1], f), an = Math.atan2(b[1] - a[1], b[0] - a[0]);
      const nx = Math.cos(an + PI / 2), ny = Math.sin(an + PI / 2), tx = Math.cos(an), ty = Math.sin(an);
      plate(ctx, 'red', PL([[x - tx * 6, y - ty * 6], [x + nx * 16, y + ny * 16], [x + tx * 6, y + ty * 6]]), { flat: true });
    }
  }
  // karşı taraf taarruz okları: dolu is gövde, içinde çapraz kazıma
  const ar = clamp(o.arrows ?? 1);
  for (const pts of [[[150, 300], [300, 280], [450, 330], [560, 330]], [[210, 520], [380, 470], [520, 450], [610, 440]]]) {
    if (ar <= 0) break;
    const p = new Path2D(); spl(p, pts, false);
    ctx.save(); ctx.setLineDash([480 * ar, 9999]); inkStroke(ctx, p, lw(20), { cap: 'butt' });
    ctx.setLineDash([lw(3), lw(9)]); inkStroke(ctx, p, lw(14), { col: P.paperD, cap: 'butt', a: .5 }); ctx.restore();
    if (ar > .96) { const a = pts[pts.length - 2], b = pts[pts.length - 1], an = Math.atan2(b[1] - a[1], b[0] - a[0]);
      inkFill(ctx, PL([[b[0] + Math.cos(an) * 30, b[1] + Math.sin(an) * 30], [b[0] + Math.cos(an + 2.4) * 28, b[1] + Math.sin(an + 2.4) * 28], [b[0] + Math.cos(an - 2.4) * 28, b[1] + Math.sin(an - 2.4) * 28]])); }
  }
  for (const [x, y] of [[40, 40], [960, 40], [40, hh - 40], [960, hh - 40]]) { const p = new Path2D(); p.arc(x, y, 9, 0, TAU); knock(ctx, p); plate(ctx, 'red', p); inkStroke(ctx, p, lw(2.4)); }
  inkStroke(ctx, sheet, lw(3));
  ctx.restore();
  return { toWorld: (u, v) => { const c = Math.cos(o.rot || 0), s = Math.sin(o.rot || 0); return [o.x + (u * c - v * s) * sc, o.y + (u * s + v * c) * sc]; } };
}

// Asma gaz lambası: zincir, abajur, şişe, hazne; lambanın kendisi
function gasLamp(ctx, x, y, s, t = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const lw = px => px / s;
  for (let i = 0; i < 8; i++) { const p = new Path2D(); p.ellipse(0, -y / s + 10 + i * ((y / s - 70) / 8), 5, 9, i % 2 ? 0 : PI / 2, 0, TAU); inkStroke(ctx, p, lw(2.6)); }
  // abajur (geniş, düz)
  const shade = SP([[-70, -26], [-24, -52], [24, -52], [70, -26], [62, -20], [-62, -20]], true, .6);
  knock(ctx, shade); plate(ctx, 'khaki', shade); inkStroke(ctx, shade, lw(3.4));
  inkStroke(ctx, SP([[-62, -20], [62, -20]], false), lw(2));
  // şişe (altın ışık: kâğıt + altın)
  const glass = SP([[-12, -20], [-16, -4], [-22, 14], [-14, 30], [14, 30], [22, 14], [16, -4], [12, -20]], true, .8);
  knock(ctx, glass); plate(ctx, 'gold', glass, { a: .55 }); inkStroke(ctx, glass, lw(2.6));
  const flame = SP([[0, 0], [5, 10], [0, 22], [-5, 10]], true); knock(ctx, flame, '#FFF8E6');
  // hazne
  const font = SP([[-24, 30], [24, 30], [30, 44], [18, 58], [-18, 58], [-30, 44]], true, .8);
  knock(ctx, font); plate(ctx, 'ochre', font, { n: 2 }); inkStroke(ctx, font, lw(3));
  cut(ctx, SP([[-20, 40], [-8, 36]], false), lw(2), { a: .8 });
  ctx.restore();
}

// Damga siluetler (kağnı, yazmalı kadın): mürekkep tek kalıp; ph: poz evresi (0/1)
function stampOxcart(ctx, x, y, s, ph = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const p = new Path2D();
  p.ellipse(-36, -20, 17, 9, 0, 0, TAU); p.ellipse(-55, -24, 6.5, 4.5, -.35, 0, TAU);
  for (const lx of [-46, -40, -30, -24]) p.rect(lx + (ph ? 1.2 : 0), -13, 2.6, 13);
  p.moveTo(-58, -28); p.quadraticCurveTo(-62, -36, -56, -38); p.lineTo(-55, -35); p.quadraticCurveTo(-58, -33, -55, -28); // boynuz
  p.rect(-4, -30, 46, 12); p.rect(2, -42, 32, 12); // kasa ve yük (cephane sandığı)
  inkFill(ctx, p);
  inkStroke(ctx, PL([[-4, -22], [-44, -24]], false), 2.6 / s);
  const wh = new Path2D(); wh.arc(24, -10, 12, 0, TAU); inkFill(ctx, wh); // dolu tahta teker
  cut(ctx, PL([[16, -10], [32, -10]], false), 1.6 / s, { a: .8 }); cut(ctx, PL([[24, -18], [24, -2]], false), 1.6 / s, { a: .8 });
  ctx.restore();
}
function stampWoman(ctx, x, y, s, ph = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const p = new Path2D();
  p.moveTo(0, -46); p.quadraticCurveTo(8, -46, 8, -38); p.quadraticCurveTo(11, -30, 9, -22); p.lineTo(12 + (ph ? 1 : 0), 0); p.lineTo(-9, 0); p.lineTo(-6, -24); p.quadraticCurveTo(-9, -34, -6, -40); p.quadraticCurveTo(-4, -46, 0, -46);
  inkFill(ctx, p);
  // sırtında eğik mermi
  ctx.save(); ctx.translate(-8, -30); ctx.rotate(-.5); const m = new Path2D(); m.rect(-3.5, -16, 7, 26); m.moveTo(-3.5, -16); m.quadraticCurveTo(0, -24, 3.5, -16); inkFill(ctx, m); ctx.restore();
  ctx.restore();
}

// Ahşap masa (önde): üst yüzey + ön kenar; y0 üst kenar
function woodTable(ctx, y0, o = {}) {
  const top = PL([[-20, y0], [W + 20, y0 - 6], [W + 20, H + 20], [-20, H + 20]]);
  knock(ctx, top); plate(ctx, 'ochre', top); plate(ctx, 'ochre', top, { a: .5 });
  // ön kenar (koyu)
  const edge = PL([[-20, y0 + 150], [W + 20, y0 + 146], [W + 20, H + 20], [-20, H + 20]]);
  plate(ctx, 'ochre', edge); plate(ctx, 'ink', edge, { a: .55 });
  inkStroke(ctx, PL([[-20, y0], [W + 20, y0 - 6]], false), 4.4); inkStroke(ctx, PL([[-20, y0 + 150], [W + 20, y0 + 146]], false), 3.6);
  // damar çizgileri
  const r = rng(o.seed || 71);
  for (let i = 0; i < 16; i++) {
    const yy = y0 + 12 + i * 8.6 + r() * 3, p = new Path2D(); let x = -20; p.moveTo(x, yy);
    while (x < W + 20) { const nx = x + 80 + r() * 140; p.quadraticCurveTo((x + nx) / 2, yy + (r() - .5) * 7, nx, yy + (r() - .5) * 3); x = nx; }
    inkStroke(ctx, p, 1.6, { a: .45 + r() * .3 });
  }
  for (let i = 0; i < 5; i++) { const yy = y0 + 166 + i * 14, p = new Path2D(); p.moveTo(-20, yy); p.bezierCurveTo(500, yy + 6, 1300, yy - 6, W + 20, yy + 2); cut(ctx, p, 1.6, { a: .25 }); }
}

// Dürbün (çift tüp), yatık
function binoculars(ctx, x, y, s, rot = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s);
  const lw = px => px / s;
  plate(ctx, 'ink', SP([[-70, 34], [80, 34], [70, 44], [-60, 44]], true), { a: .35 });
  for (const oy of [-14, 16]) {
    const tube = SP([[-66, oy - 13], [-20, oy - 11], [26, oy - 15], [66, oy - 17], [70, oy], [66, oy + 17], [26, oy + 15], [-20, oy + 11], [-66, oy + 13], [-70, oy]], true, .6);
    knock(ctx, tube); inkFill(ctx, tube);
    cut(ctx, SP([[-58, oy - 8], [-20, oy - 6], [22, oy - 9], [58, oy - 11]], false), lw(2.2), { a: .8 });
    const lens = new Path2D(); lens.ellipse(68, oy, 4, 15, 0, 0, TAU); knock(ctx, lens); plate(ctx, 'khaki', lens); inkStroke(ctx, lens, lw(2));
    for (let k = 0; k < 4; k++) cut(ctx, PL([[-46 + k * 7, oy - 11], [-46 + k * 7, oy + 11]], false), lw(1.4), { a: .5 });
  }
  const bridge = PL([[-6, -6], [10, -6], [10, 6], [-6, 6]]); knock(ctx, bridge); plate(ctx, 'ochre', bridge, { n: 2 }); inkStroke(ctx, bridge, lw(2));
  ctx.restore();
}
// Pusula (pirinç kutu)
function compass(ctx, x, y, r) {
  const rim = new Path2D(); rim.ellipse(x, y, r, r * .62, 0, 0, TAU);
  plate(ctx, 'ink', (() => { const p = new Path2D(); p.ellipse(x + 8, y + 10, r, r * .6, 0, 0, TAU); return p; })(), { a: .35 });
  knock(ctx, rim); plate(ctx, 'ochre', rim, { n: 2 }); inkStroke(ctx, rim, 3.4);
  const face = new Path2D(); face.ellipse(x, y - 3, r * .8, r * .48, 0, 0, TAU); knock(ctx, face); inkStroke(ctx, face, 2);
  for (let k = 0; k < 16; k++) { const a = k / 16 * TAU, x0 = x + Math.cos(a) * r * .68, y0 = y - 3 + Math.sin(a) * r * .4, x1 = x + Math.cos(a) * r * .78, y1 = y - 3 + Math.sin(a) * r * .47; inkStroke(ctx, PL([[x0, y0], [x1, y1]], false), k % 4 ? 1.2 : 2.4); }
  plate(ctx, 'red', PL([[x - r * .55, y - 3 + r * .1], [x + 2, y - 3 - 4], [x + 2, y - 3 + 4]]));
  inkFill(ctx, PL([[x + r * .55, y - 3 - r * .1], [x - 2, y - 3 - 4], [x - 2, y - 3 + 4]]));
}
// Telgrafname / evrak: Osmanlıca soyut satırlar
function paperSheet(ctx, x, y, w, h, rot, seed, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  const p = PL(rough([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]], 1.2, seed));
  if (o.shadow !== false) plate(ctx, 'ink', PL([[-w / 2 + 6, -h / 2 + 8], [w / 2 + 6, -h / 2 + 8], [w / 2 + 6, h / 2 + 8], [-w / 2 + 6, h / 2 + 8]]), { a: .3 });
  knock(ctx, p);
  if (o.header) { inkStroke(ctx, PL([[-w / 2 + 12, -h / 2 + 22], [w / 2 - 12, -h / 2 + 22]], false), 1.6); }
  const rows = o.rows || Math.floor((h - 40) / 18);
  for (let i = 0; i < rows; i++) scriptLine(ctx, w / 2 - 14, -h / 2 + 40 + i * 18, (w - 28) * (i === rows - 1 ? .5 : .92), 7, seed * 10 + i, { w: 1.6, a: .9 });
  inkStroke(ctx, p, 2.6);
  ctx.restore();
}
