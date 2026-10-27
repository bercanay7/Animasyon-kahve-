// Nesneler ve ortam: kurmay haritası, gaz lambası, duvar, pencere manzarası, masa, dürbün, pusula, telgrafname, damga siluetler
'use strict';

// Kurmay haritası (yerel 1000×650 birim) — Sakarya meydan muharebesi bölgesi, şematik
// o: {x,y,w,rot, front: 0..1 (cephe hattının çizilme oranı), arrows: 0..1, focus:[u,v] (açık havuz merkezi)}
// Sırt tarama (tırtıl): omurga boyunca normal yönünde çizgiler; boy L = Lmax·sin(πu); güneydoğu yüz kalın
function ridge(ctx, spine, Lmax, lwf, seed) {
  const r = rng(seed), n = spine.length;
  let tot = 0; const seg = []; for (let i = 0; i < n - 1; i++) { const l = Math.hypot(spine[i + 1][0] - spine[i][0], spine[i + 1][1] - spine[i][1]); seg.push(l); tot += l; }
  plate(ctx, 'khaki', (() => { const p = new Path2D(); for (let side of [1, -1]) { } spl(p, spine.map(([x, y]) => [x, y]), false); return p; })(), { a: 0 });
  for (let d = 0; d <= tot; d += 6) {
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
  for (const [rx, ry, c] of [[260, 215, '#E3D8BC'], [190, 160, '#E9DFC6']]) { const pool = new Path2D(); pool.ellipse(F[0], F[1], rx, ry, 0, 0, TAU); knock(ctx, pool, c); }
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
  const R = [[[[560, 352], [610, 334], [660, 318], [720, 296]], 30], [[[700, 480], [760, 462], [830, 470], [890, 456]], 22], [[[650, 160], [700, 146], [760, 152], [820, 140]], 20], [[[120, 470], [190, 456], [260, 468], [320, 458]], 20], [[[90, 190], [150, 178], [220, 188]], 16]];
  R.forEach(([sp, L], i) => ridge(ctx, sp, L, lw, 30 + i));
  // demiryolu: kesik çift çizgi
  const rail = SP([[980, 90], [860, 120], [740, 100], [600, 70], [420, 60], [200, 90], [30, 110]], false);
  inkStroke(ctx, rail, lw(6)); inkStroke(ctx, rail, lw(3), { col: P.paperD });
  ctx.save(); ctx.setLineDash([lw(14), lw(14)]); inkStroke(ctx, rail, lw(3)); ctx.restore();
  for (const [x, y] of [[860, 120], [600, 70], [420, 60], [240, 560]]) inkFill(ctx, PL([[x - 9, y - 9], [x + 9, y - 9], [x + 9, y + 9], [x - 9, y + 9]]));
  // açıklayıcı Latin etiketler (izleyici katmanı) + altında küçük Osmanlıca iz
  const tag = (s, x, y, ax, ay) => {
    ctx.save(); ctx.font = FONT.mono(24); ctx.letterSpacing = '3px'; const w = ctx.measureText(s).width; ctx.restore();
    inkStroke(ctx, PL([[ax, ay], [x + w / 2 + 14, y + 6]], false), lw(1.4));
    const b = PL([[x, y - 22], [x + w + 28, y - 22], [x + w + 28, y + 12], [x, y + 12]]); knock(ctx, b, P.paperD); inkStroke(ctx, b, lw(1.8));
    txt(ctx, s, x + 14, y + 4, FONT.mono(24), { ls: 3 });
  };
  tag('SAKARYA', 90, 420, 300, 372); tag('DUATEPE', 720, 228, 660, 316); tag('POLATLI', 790, 74, 860, 116);
  for (const [x, y, L, sd] of [[920, 196, 70, 1], [760, 430, 70, 2], [270, 300, 80, 3], [860, 520, 100, 5], [330, 560, 110, 6]]) scriptLine(ctx, x, y, L, 10, sd + 50, { w: lw(1.8), a: .8 });
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
  // karşı taraf taarruz okları: lacivert dolu gövde, 45° kazıma
  const ar = clamp(o.arrows ?? 1);
  for (const pts of [[[150, 300], [300, 280], [450, 330], [560, 330]], [[210, 520], [380, 470], [520, 450], [610, 440]]]) {
    if (ar <= 0) break;
    const p = new Path2D(); spl(p, pts, false);
    ctx.save(); ctx.setLineDash([480 * ar, 9999]);
    const [dx, dy] = regOf('navy'); ctx.translate(dx, dy);
    inkStroke(ctx, p, lw(13), { col: P.navy, cap: 'butt', mode: 'multiply' });
    ctx.restore();
    // kazıma: ok boyunca 14 px aralıklı 45° çizgiler
    let acc = 0; for (let i = 0; i < pts.length - 1; i++) { const A = pts[i], B = pts[i + 1], L = Math.hypot(B[0] - A[0], B[1] - A[1]), an = Math.atan2(B[1] - A[1], B[0] - A[0]);
      for (let d = (14 - acc % 14) % 14; d < L; d += 14) { if (acc + d > 480 * ar) break; const x = A[0] + Math.cos(an) * d, y = A[1] + Math.sin(an) * d, k = an + PI / 4;
        cut(ctx, PL([[x - Math.cos(k) * 7, y - Math.sin(k) * 7], [x + Math.cos(k) * 7, y + Math.sin(k) * 7]], false), lw(1.4), { a: .7 }); } acc += L; }
    if (ar > .96) { const a = pts[pts.length - 2], b = pts[pts.length - 1], an = Math.atan2(b[1] - a[1], b[0] - a[0]);
      plate(ctx, 'navy', PL([[b[0] + Math.cos(an) * 26, b[1] + Math.sin(an) * 26], [b[0] + Math.cos(an + 2.4) * 22, b[1] + Math.sin(an + 2.4) * 22], [b[0] + Math.cos(an - 2.4) * 22, b[1] + Math.sin(an - 2.4) * 22]]), { flat: true }); }
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
  // öküz: uzun gövde (boy ≈ 2,2 × yükseklik), omuz hörgücü, eğik baş, lir boynuz, püsküllü kuyruk
  p.moveTo(-82, -24); p.quadraticCurveTo(-76, -36, -64, -36); p.quadraticCurveTo(-58, -42, -52, -37); p.lineTo(-40, -35); p.quadraticCurveTo(-36, -24, -40, -16); p.lineTo(-80, -15); p.closePath();
  p.moveTo(-82, -30); p.quadraticCurveTo(-92, -30, -96, -22); p.lineTo(-92, -18); p.quadraticCurveTo(-88, -24, -82, -22); p.closePath(); // baş, öne eğik
  for (const lx of [-78, -72, -48, -42]) p.rect(lx + (ph && (lx === -72 || lx === -42) ? 2 : 0), -16, 3, 16);
  inkFill(ctx, p);
  inkStroke(ctx, SP([[-90, -27], [-94, -36], [-88, -40]], false), 2.2 / s); inkStroke(ctx, SP([[-87, -28], [-86, -38], [-80, -40]], false), 2.2 / s); // lir boynuz
  inkStroke(ctx, SP([[-38, -32], [-33, -24], [-34, -14]], false), 1.6 / s); inkFill(ctx, (() => { const q = new Path2D(); q.ellipse(-34, -12, 2.2, 3.4, 0, 0, TAU); return q; })()); // kuyruk
  inkStroke(ctx, PL([[-86, -38], [-74, -40]], false), 3 / s); // boyunduruk
  inkStroke(ctx, PL([[-74, -38], [-20, -28]], false), 2.4 / s);  // ok (oklava)
  // kağnı: V yan çıtalar, cephane sandığı, iki dolu tahta teker
  const c = new Path2D(); c.moveTo(-26, -30); c.lineTo(30, -30); c.lineTo(22, -18); c.lineTo(-18, -18); c.closePath(); c.rect(-12, -44, 34, 13); inkFill(ctx, c);
  for (const [wx, wr] of [[-8, 13], [18, 13]]) { const w = new Path2D(); w.arc(wx, -13, wr, 0, TAU); knock(ctx, w, P.ink); cut(ctx, PL([[wx - wr + 3, -13], [wx + wr - 3, -13]], false), 1.6 / s, { a: .7 }); cut(ctx, (() => { const q = new Path2D(); q.arc(wx, -13, wr - 3.5, 0, TAU); return q; })(), 1.2 / s, { a: .5 }); }
  ctx.restore();
}
function stampWoman(ctx, x, y, s, ph = 0) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const p = new Path2D();
  p.moveTo(0, -46); p.quadraticCurveTo(8, -46, 8, -38); p.quadraticCurveTo(11, -30, 9, -22); p.lineTo(12 + (ph ? 1 : 0), 0); p.lineTo(-9, 0); p.lineTo(-6, -24); p.quadraticCurveTo(-9, -34, -6, -40); p.quadraticCurveTo(-4, -46, 0, -46);
  inkFill(ctx, p);
  // sırtında eğik mermi
  ctx.save(); ctx.translate(-9, -30); ctx.rotate(-1.35); const m = new Path2D(); m.rect(-2.4, -8, 4.8, 15); m.moveTo(-2.4, -8); m.quadraticCurveTo(0, -12.5, 2.4, -8); inkFill(ctx, m); ctx.restore();
  inkStroke(ctx, PL([[-6, -38], [-12, -22]], false), 1.2 / s); // bez askı
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
