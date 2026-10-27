// Kişiler: ¾ büst (bust3q), başlıklar (kalpak, fes, kabalak), giysiler (kaput, setre, sivil ceket), kollar ve eller.
// Baş birimleri: yüz +x yönüne dönük, köken göz hizasında; tepe ≈ -66, çene ≈ +52 (baş boyu ≈ 118 birim).
'use strict';
// Kişi kimlikleri (USLUP.md): yüz biçimi, kaş, bıyık, göz rengi
const PEOPLE = {
  mk: { name: 'MUSTAFA KEMAL', born: 1881, jaw: .97, cheek: 1.06, brow: .30, browW: 1.15, mus: 'mk', iris: P.eye, hair: 'sepia', lean: 1, nose: 1.04, ear: 1, seed: 3 },
  ismet: { name: 'İSMET', born: 1884, jaw: 1.04, cheek: 1.0, brow: .06, browW: .95, mus: 'thin', iris: P.sepia, hair: 'ink', nose: .96, ear: 1.08, seed: 5, short: true },
  fevzi: { name: 'FEVZİ', born: 1876, jaw: 1.1, cheek: 1.02, brow: -.08, browW: 1.1, mus: 'thick', musCol: 'grey', iris: P.sepia, hair: 'grey', nose: 1.02, ear: 1.02, seed: 7, lines: 1 },
  anon: { jaw: 1.02, cheek: 1, brow: .05, browW: 1, mus: 'mk', iris: P.sepia, hair: 'ink', nose: 1, ear: 1, seed: 9 },
};

// Baş çizimi. o: {x,y,s (px/birim), dir (+1 sağa bakar), who, gear:'kalpak'|'fes'|'kabalak'|null, gearCol,
//   light:'front'|'back'|'top', look:[dx,dy] (iris kayması), skin: true (yakın plan ten kalıbı), tilt, age}
// Oranlar: tepe -64, kaş -12, göz 0, burun altı +22, ağız +33, çene +56; yakın kulak x≈-28, uzak kontur x≈+34.
function head3q(ctx, o) {
  const pp = { ...PEOPLE.anon, ...(PEOPLE[o.who] || {}), ...(o.id || {}) };
  const s = o.s, dir = o.dir || 1, lw = px => px * Math.pow(s / 1.3, .75) / s;
  const jw = pp.jaw, ck = pp.cheek, sd = pp.seed, age = o.age ?? 38;
  const yg = clamp(inv(30, 18, age)); // gençlik: yanak dolgun, çene yumuşak
  const WD = o.wide ?? 1.16;
  ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(o.tilt || 0); ctx.scale(s * dir * WD, s);
  const face = [[28, -42], [31, -26], [33.5, -12], [33, -3], [35.5 * ck, 6], [33.5 * ck, 16], [31 * jw, 28], [28 * jw, 40], [24 * jw, 50], [14, 56 + yg], [0, 55.5], [-12 * jw, 50], [-21 * jw, 40], [-25, 28], [-40, 22], [-54, 2], [-58, -24], [-50, -48], [-30, -62], [-4, -66], [16, -60]];
  const faceP = SP(rough(face, .3, sd), true, .9);
  const nose = rough([[30, -6], [32.5, 2], [36 * pp.nose, 9], [39.5 * pp.nose, 14], [41 * pp.nose, 17.5], [39.5, 20.6], [35.5, 21.8], [31.5, 21]], .15, sd + 1);
  const noseP = SP(nose, true, .85);
  knock(ctx, faceP);
  if (o.skin) plate(ctx, 'skin', faceP);
  const light = o.light || 'front';
  const shPl = o.skin ? 'skin' : 'ochre', shA = o.skin ? .8 : .36;
  const shadows = [];
  if (light === 'front') {
    shadows.push([[-8, -46], [-12, -26], [-10, -8], [-4, 4], [6, 14], [8, 24], [2, 36], [4, 48], [10, 57], [-14, 58], [-26, 34], [-60, 20], [-60, -50]]); // yakın yan düzlem: şakak, elmacık altı, çene yanı
    shadows.push([[-4, -8], [14, -10.5], [24, -9], [17, -4.6], [4, -4.2]]); // göz çukuru
    shadows.push([[14, 49], [27, 44], [22, 54], [12, 57]]);            // çene altı
    shadows.push([[30, 22.5], [41, 22], [37, 26.5], [31, 26]]);        // burun gölgesi
  } else if (light === 'back') {
    shadows.push([[28, -42], [31, -26], [34, -12], [31.5, -3], [36, 7], [34, 22], [31, 34], [24, 49], [13, 57], [12, 40], [18, 22], [16, 4], [14, -16], [16, -36]]);
  } else {
    shadows.push([[-4, -9], [30, -10], [33, -3], [-4, -3]]);
    shadows.push([[-12, 44], [22, 48], [16, 58], [-6, 56]]);
  }
  if (pp.lean && light === 'front') shadows.push([[10, 12], [24, 14], [30, 22], [22, 26], [12, 22]]);
  ctx.save(); ctx.clip(faceP); for (const q of shadows) plate(ctx, shPl, SP(q, true, .8), { a: shA }); ctx.restore();
  // saç: başlık varsa yalnız şakak ve ense; yoksa geriye taranmış tepe
  const hairPl = pp.hair;
  const hairSide = SP(rough([[-14, -36], [-30, -32], [-40, -18], [-44, 2], [-38, 14], [-30, 4], [-26, -12], [-20, -24]], .35, sd + 2), true, .9);
  const hairTop = SP(rough([[30, -36], [22, -54], [0, -67], [-30, -63], [-52, -46], [-59, -20], [-54, 4], [-42, 18], [-32, 8], [-28, -10], [-14, -30], [10, -40]], .4, sd + 3), true, .9);
  const hp = o.gear ? hairSide : hairTop;
  if (hairPl === 'ink') inkFill(ctx, hp);
  else { plate(ctx, hairPl, hp, { a: hairPl === 'sepia' ? .7 : 1 }); if (hairPl !== 'sepia') plate(ctx, hairPl, hp, { a: .55 }); inkStroke(ctx, hp, lw(1.8)); }
  if (!o.gear) for (let i = 0; i < 6; i++) { const y0 = -58 + i * 7, q = new Path2D(); q.moveTo(24 - i * 5, y0 + 10); q.quadraticCurveTo(-12 - i * 3, y0 - 3, -46 - i, y0 + 12 + i * 3); hairPl === 'ink' ? cut(ctx, q, lw(1.3), { a: .55 }) : inkStroke(ctx, q, lw(1.4), { a: .7 }); }
  // kulak
  const E_ = pp.ear, ear = SP(rough([[-24, -6], [-30, -9], [-35, -4], [-36, 6], [-33, 16], [-27, 21], [-23, 16], [-23, 4]].map(([x, y]) => [-24 + (x + 24) * E_, y]), .25, sd + 4), true, .9);
  knock(ctx, ear); if (o.skin) plate(ctx, 'skin', ear);
  plate(ctx, shPl, ear, { a: shA * .9 });
  inkStroke(ctx, ear, lw(2.4)); inkStroke(ctx, SP([[-27, -3], [-31, 2], [-31, 10], [-28, 14]], false), lw(1.6));
  inkStroke(ctx, faceP, lw(3.6));
  // burun (yanağın önünde)
  knock(ctx, noseP); if (o.skin) plate(ctx, 'skin', noseP);
  if (light === 'front') plate(ctx, shPl, SP([[29.5, -6], [31.5, 6], [34, 16], [32, 21], [29.5, 12]], true), { a: shA * .8 });
  inkStroke(ctx, SP(nose.slice(0, 7), false, .85), lw(3));
  inkStroke(ctx, SP([[33.5, 20.5], [31, 17.5], [33.5, 15]], false), lw(2));
  // gözler: badem, küçük iris; bakış +x
  const look = o.look || [1.6, .4];
  for (const [k, e] of [[0, { c: [6, -1], w: 9, h: 4.2 }], [1, { c: [25.5, -1.2], w: 5, h: 3.7 }]]) {
    const [ex, ey] = e.c, w = e.w, h = e.h * (o.eyeOpen ?? .86);
    const eyeP = new Path2D(); eyeP.moveTo(ex - w, ey + .8); eyeP.bezierCurveTo(ex - w * .5, ey - h * 1.2, ex + w * .4, ey - h * 1.3, ex + w, ey - .2);
    eyeP.bezierCurveTo(ex + w * .45, ey + h * .9, ex - w * .55, ey + h * .85, ex - w, ey + .8);
    knock(ctx, eyeP, '#F7F1E4');
    ctx.save(); ctx.clip(eyeP);
    const ix = ex + look[0] * (k ? .7 : 1) + (k ? .6 : 0), iy = ey + look[1] + .6, ir = k ? 3.0 : 3.7;
    ctx.fillStyle = pp.iris; ctx.beginPath(); ctx.arc(ix, iy, ir, 0, TAU); ctx.fill();
    ctx.fillStyle = P.ink; ctx.beginPath(); ctx.arc(ix, iy, ir * .45, 0, TAU); ctx.fill();
    ctx.fillStyle = '#FCF9F1'; ctx.beginPath(); ctx.arc(ix + ir * .32, iy - ir * .4, ir * .25, 0, TAU); ctx.fill();
    plate(ctx, 'ochre', PL([[ex - w, ey - h * 1.4], [ex + w, ey - h * 1.4], [ex + w, ey - h * .3], [ex - w, ey - h * .4]]), { a: .3 });
    ctx.restore();
    const lid = new Path2D(); lid.moveTo(ex - w - .6, ey + 1); lid.bezierCurveTo(ex - w * .5, ey - h * 1.25, ex + w * .4, ey - h * 1.35, ex + w + .5, ey - .2);
    inkStroke(ctx, lid, lw(k ? 2.4 : 3));
    const fold = new Path2D(); fold.moveTo(ex - w * .6, ey - h * 1.6); fold.quadraticCurveTo(ex + w * .1, ey - h * 2.1, ex + w * .85, ey - h * 1.45);
    inkStroke(ctx, fold, lw(1.3), { a: .6 });
    const low = new Path2D(); low.moveTo(ex - w * .5, ey + h * .8); low.quadraticCurveTo(ex, ey + h * 1.05, ex + w * .7, ey + h * .55);
    inkStroke(ctx, low, lw(1.2), { a: .5 });
  }
  // kaşlar: pp.brow > 0 dış uç yukarı (keskin)
  const bA = pp.brow, bW = pp.browW;
  const nbP = SP([[18, -10.5], [10, -12.6 - bA * 3], [0, -13.4 - bA * 6], [-5, -12.8 - bA * 8], [-4, -15.6 - bA * 8], [2, -16.6 - bA * 6], [11, -15.4 - bA * 3], [18.5, -12.6]], true, .8);
  inkFill(ctx, SP(rough([[18, -10.5], [10, -12.4 - bA * 3], [0, -13.2 - bA * 6], [-5, -12.6 - bA * 8], [-4.5, -12.6 - bA * 8 - 2.6 * bW], [2, -13.2 - bA * 6 - 3.2 * bW], [11, -12.4 - bA * 3 - 3 * bW], [18.5, -10.5 - 2.2 * bW]], .15, sd + 8), true, .8));
  inkFill(ctx, SP([[23.5, -11], [29, -12.4 - bA * 2.5], [33.5, -11.8 - bA * 3.5], [33.5, -11.8 - bA * 3.5 - 2.2 * bW], [29, -12.4 - bA * 2.5 - 2.6 * bW], [23.5, -11 - 1.8 * bW]], true, .8));
  // yüz çizgileri
  if (pp.lines) {
    inkStroke(ctx, SP([[29, 25], [26, 31], [25.5, 37]], false), lw(1.3), { a: .55 });
    inkStroke(ctx, SP([[-2, -28], [10, -30], [22, -28]], false), lw(1.1), { a: .3 });
    inkStroke(ctx, SP([[-6, 4], [0, 8], [8, 9]], false), lw(1.1), { a: .4 });
  }
  // ağız ve çene
  const mouth = new Path2D(); mouth.moveTo(17, 33.5); mouth.quadraticCurveTo(25, 34.6, 33, 32.6); inkStroke(ctx, mouth, lw(2.4));
  inkStroke(ctx, SP([[21, 38.8], [26, 39.6], [30, 38.6]], false), lw(1.4), { a: .45 });
  inkStroke(ctx, SP([[11, 50.5], [17, 51.5]], false), lw(1.3), { a: .4 });
  // bıyık
  if (pp.mus && !(age < 20 && pp.mus !== 'mk')) {
    let m;
    if (pp.mus === 'thick') m = [[15, 25], [23, 23.4], [31, 23.2], [38, 24.2], [42, 28.4], [40, 31.6], [34, 29.8], [26, 30.4], [19, 31.4], [13, 30]];
    else if (pp.mus === 'thin') m = [[19, 26.4], [26, 25.2], [33, 25.3], [38.5, 27], [35.5, 28.6], [28, 28], [21, 28.8]];
    else m = [[16, 26.4], [22.5, 24.6], [30, 24.4], [37, 25.4], [40.5, 28.6], [35.5, 29.4], [28.5, 28.8], [21, 29.8], [15, 29.2]];
    const th = age < 22 ? .55 : 1;
    if (th < 1) m = m.map(([x, y]) => [x, 26.5 + (y - 26.5) * th]);
    const mP = SP(rough(m, .15, sd + 6), true, .9);
    knock(ctx, mP);
    if (pp.musCol === 'grey') { plate(ctx, 'grey', mP, { a: .6 }); inkStroke(ctx, mP, lw(1.8)); for (let i = 0; i < 6; i++) { const x = 18 + i * 4; inkStroke(ctx, SP([[x, 24.5], [x + 1.4, 30]], false), lw(1), { a: .65 }); } }
    else if (pp.hair !== 'ink') { plate(ctx, 'sepia', mP, { a: .95 }); plate(ctx, 'ochre', mP, { a: .4 }); inkStroke(ctx, mP, lw(1.8)); for (let i = 0; i < 5; i++) { const x = 19 + i * 4.2; inkStroke(ctx, SP([[x, 25], [x + 1.2, 28.6]], false), lw(1), { a: .6 }); } if (th < 1) ctx.globalAlpha = 1; }
    else { inkFill(ctx, mP, { a: th < 1 ? .6 : 1 }); for (let i = 0; i < 4; i++) { const x = 21 + i * 4.4; cut(ctx, SP([[x, 25.4], [x + 1.2, 28.4]], false), lw(.9), { a: .35 }); } }
  }
  ctx.restore();
  if (o.gear) headgear(ctx, { ...o, sd, WD });
}

// Başlıklar (baş koordinatında)
function headgear(ctx, o) {
  const s = o.s, dir = o.dir || 1, lw = px => px * Math.pow(s / 1.3, .75) / s, sd = o.sd || 1;
  ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(o.tilt || 0); ctx.scale(s * dir * (o.WD || 1), s);
  if (o.gear === 'kalpak') {
    // ¾ silindir; hafifçe daralan; tepe kenarı içe dönük
    const body = SP(rough([[-60, -14], [-60, -42], [-57, -70], [-44, -82], [-14, -88], [16, -87], [33, -80], [36, -56], [37, -28], [24, -33], [2, -34], [-26, -26], [-48, -18]], .5, sd + 10), true, .7);
    knock(ctx, body);
    const col = o.gearCol || 'ink';
    if (col === 'ink') inkFill(ctx, body); else { plate(ctx, col, body); inkStroke(ctx, body, lw(3.6)); }
    // kıvırcık kuzu yünü: kazıma ilmikler (ink) ya da is ilmikler (gri)
    const r = rng(sd + 11);
    ctx.save(); ctx.clip(body);
    for (let i = 0; i < 150; i++) {
      const u = r(), v = r();
      const x = lerp(-58, 35, u), ytop = lerp(-80, -86, u) + 3, ybot = lerp(-16, -32, u);
      const y = lerp(ytop, ybot, v), rr = 1.4 + r() * 1.6, a0 = r() * TAU;
      const q = new Path2D(); q.arc(x, y, rr, a0, a0 + PI * (.9 + r() * .7));
      col === 'ink' ? cut(ctx, q, lw(1.25), { a: .22 + (1 - v) * .35 * (u > .55 ? 1.2 : .7) }) : inkStroke(ctx, q, lw(1.3), { a: .45 });
    }
    ctx.restore();
    // tepe: açık oval kenar (ışık üstten)
    const top = new Path2D(); top.ellipse(-12, -83, 44, 6, -.05, PI * 1.02, PI * 1.98);
    col === 'ink' ? cut(ctx, top, lw(2.2), { a: .8 }) : inkStroke(ctx, top, lw(2.2));
    // alt kenar gölgesi alında
    inkStroke(ctx, SP([[-48, -18], [-26, -26], [2, -34], [24, -33], [37, -28]], false), lw(3.2));
  } else if (o.gear === 'fes') {
    const body = SP(rough([[-52, -16], [-46, -50], [-40, -80], [-10, -86], [16, -84], [26, -56], [34, -28], [10, -32], [-22, -24]], .4, sd + 12), true, .6);
    knock(ctx, body); plate(ctx, 'red', body); plate(ctx, 'red', SP([[-46, -22], [-40, -56], [-34, -84], [-20, -88], [-24, -50], [-28, -26]], true), { a: .6 });
    inkStroke(ctx, body, lw(3.6));
    const top = new Path2D(); top.ellipse(-12, -84, 27, 4, -.06, PI, TAU); inkStroke(ctx, top, lw(2));
    // püskül
    inkFill(ctx, SP([[-12, -86], [-34, -78], [-48, -56], [-52, -36], [-46, -38], [-40, -58], [-26, -76], [-10, -82]], true));
  } else if (o.gear === 'kabalak') {
    const body = SP(rough([[-62, -10], [-64, -44], [-50, -74], [-16, -88], [18, -84], [38, -58], [40, -24], [22, -28], [-6, -26], [-36, -16]], .6, sd + 13), true, .8);
    knock(ctx, body); plate(ctx, 'khaki', body);
    plate(ctx, 'khaki', SP([[-62, -10], [-64, -44], [-50, -74], [-32, -82], [-38, -46], [-40, -16]], true));
    inkStroke(ctx, body, lw(3.8));
    for (let i = 0; i < 5; i++) { const q = new Path2D(); const y = -30 - i * 11; q.moveTo(-60 + i * 2, y + 14); q.bezierCurveTo(-34, y - 2, 6, y - 10 + i, 38 - i * 3, y - 2 - i * 2); inkStroke(ctx, q, lw(2), { a: .75 }); }
  }
  ctx.restore();
}

// Gövde (büst): omuzlar, yaka, kaput/setre/ceket. Baş koordinatında çizilir: boyun tabanı ≈ (−6, 78)
// o: {x,y,s,dir, coat:'kaput'|'setre'|'civil', col:'khaki'|'ink'|'navy'|..., w (omuz genişliği çarpanı), len (alt sınır, birim)}
function bust(ctx, o) {
  const s = o.s, dir = o.dir || 1, lw = px => px * Math.pow(s / 1.3, .75) / s, sd = (o.seed || 1) + 40, W_ = o.w || 1, len = o.len || 330;
  ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(o.tilt || 0); ctx.scale(s * dir, s);
  const col = o.col || 'khaki', dark = col === 'ink';
  const fillC = (p, n = 1, a = 1) => dark ? inkFill(ctx, p) : plate(ctx, col, p, { n, a });
  // boyun (kalın, eril)
  const neck = SP([[-26, 30], [-28, 76], [16, 80], [14, 48]], true, .6);
  knock(ctx, neck); if (o.skin) plate(ctx, 'skin', neck);
  plate(ctx, o.skin ? 'skin' : 'ochre', SP([[-26, 30], [-28, 80], [4, 82], [6, 56]], true), { a: o.skin ? .8 : .36 });
  inkStroke(ctx, SP([[-26, 34], [-28, 72]], false), lw(2.8)); inkStroke(ctx, SP([[14, 52], [15, 68]], false), lw(2.6));
  // gövde: omuzlar boyundan eğimle iner
  const body = SP(rough([[-24, 74], [-64 * W_, 88], [-92 * W_, 112], [-100 * W_, 170], [-102 * W_, len], [74 * W_, len], [72 * W_, 168], [66 * W_, 110], [46 * W_, 86], [14, 78]], .7, sd), true, .75);
  knock(ctx, body); fillC(body);
  const shade = SP([[-24, 74], [-64 * W_, 88], [-92 * W_, 112], [-100 * W_, 170], [-102 * W_, len], [-58, len], [-60, 170], [-52, 110]], true, .8);
  if (!dark) plate(ctx, col, shade, { a: .7 });
  inkStroke(ctx, body, lw(3.8));
  if (o.coat === 'kaput') {
    // dik iç yaka (setre) + geniş yatık kaput yakası: iki sivri kanat, aralarında V
    const band = SP([[-30, 54], [-32, 78], [16, 82], [18, 58]], true, .6);
    knock(ctx, band); fillC(band, 2); inkStroke(ctx, band, lw(2.6));
    const lapN = PL(rough([[-30, 74], [-74 * W_, 92], [-62 * W_, 112], [-34, 156], [-8, 186], [-10, 110]], .6, sd + 1));
    const lapF = PL(rough([[16, 78], [50 * W_, 94], [42 * W_, 112], [26, 154], [4, 188], [4, 112]], .6, sd + 2));
    for (const l of [lapN, lapF]) { knock(ctx, l); fillC(l, 1); if (!dark) plate(ctx, col, l, { a: .45 }); inkStroke(ctx, l, lw(2.8)); }
    const v = PL([[-10, 110], [4, 112], [4, 188], [-2, 196], [-8, 186]]);
    knock(ctx, v); fillC(v, 2); inkStroke(ctx, v, lw(1.8));
    for (const [bx, by] of [[-24, 230], [24, 230], [-25, 290], [26, 290]]) { const b = new Path2D(); b.arc(bx, by, 4.2, 0, TAU); knock(ctx, b); plate(ctx, 'ochre', b, { n: 2 }); inkStroke(ctx, b, lw(1.6)); }
    inkStroke(ctx, SP([[-2, 196], [0, len]], false), lw(2.6));
    if (dark) { cut(ctx, SP([[-62, 112], [-8, 186]], false), lw(1.8), { a: .6 }); cut(ctx, SP([[42, 112], [4, 188]], false), lw(1.8), { a: .6 }); }
  } else if (o.coat === 'setre') {
    const coll = SP([[-30, 54], [-32, 82], [16, 86], [18, 58]], true, .6);
    knock(ctx, coll); plate(ctx, o.collarCol || col, coll, { n: 2 }); if (o.collarCol === 'red') plate(ctx, 'red', coll); inkStroke(ctx, coll, lw(2.6));
    for (let i = 0; i < 5; i++) { const b = new Path2D(); b.arc(-6, 116 + i * 38, 3.8, 0, TAU); knock(ctx, b); plate(ctx, 'ochre', b, { n: 2 }); inkStroke(ctx, b, lw(1.5)); }
    inkStroke(ctx, SP([[-4, 94], [-2, len]], false), lw(2.4));
  } else if (o.coat === 'civil') {
    const shirt = SP([[-20, 76], [14, 80], [4, 160], [-8, 160]], true); knock(ctx, shirt); inkStroke(ctx, shirt, lw(2));
    const coll = SP([[-22, 66], [-24, 84], [-6, 96], [12, 86], [14, 70]], true, .6); knock(ctx, coll); inkStroke(ctx, coll, lw(2));
    const tie = SP([[-8, 90], [2, 90], [5, 150], [-2, 162], [-9, 150]], true); knock(ctx, tie); inkFill(ctx, tie); cut(ctx, SP([[-4, 100], [0, 146]], false), lw(1.2), { a: .4 });
    const lapN = SP([[-24, 74], [-58 * W_, 90], [-40, 150], [-6, 214], [-12, 130]], true, .7), lapF = SP([[14, 78], [44 * W_, 94], [36, 150], [4, 216], [8, 132]], true, .7);
    for (const l of [lapN, lapF]) { knock(ctx, l); fillC(l, 2); inkStroke(ctx, l, lw(2.6)); }
    if (dark) { cut(ctx, SP([[-40, 150], [-6, 214]], false), lw(1.8), { a: .55 }); cut(ctx, SP([[36, 150], [4, 216]], false), lw(1.8), { a: .55 }); }
  }
  if (o.boards) for (const [x0, x1, y0] of [[-86 * W_, -50, 98], [40, 64 * W_, 92]]) {
    const b = SP([[x0, y0 + 4], [x1, y0 - 4], [x1, y0 + 6], [x0, y0 + 14]], true); knock(ctx, b); plate(ctx, 'gold', b); inkStroke(ctx, b, lw(2));
  }
  // kumaş kırışıkları
  const folds = [[[-82, 190], [-70, 250], [-74, 320]], [[58, 200], [52, 280]], [[-88, 132], [-70, 150]]];
  for (const q of folds) dark ? cut(ctx, SP(q, false), lw(1.8), { a: .4 }) : inkStroke(ctx, SP(q, false), lw(1.8), { a: .55 });
  ctx.restore();
}

// Kol: omuzdan (dünya koordinatı) ele iki kemikli ters kinematik; kol kalınlığı px
function arm(ctx, sh, hand, o) {
  const a = o.upper, b = o.fore, bend = o.bend ?? 1;
  const dx = hand[0] - sh[0], dy = hand[1] - sh[1], d = clamp(Math.hypot(dx, dy), Math.abs(a - b) + 1, (a + b) * .999);
  const phi = Math.atan2(dy, dx), al = Math.acos(clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1));
  const ua = phi - bend * al, el = [sh[0] + Math.cos(ua) * a, sh[1] + Math.sin(ua) * a];
  const wr = [sh[0] + Math.cos(phi) * d, sh[1] + Math.sin(phi) * d];
  const w0 = o.w || 40, w1 = w0 * .86, w2 = w0 * .66;
  // kılıf çokgeni
  const seg = (p, q, wa, wb) => { const ang = Math.atan2(q[1] - p[1], q[0] - p[0]) + PI / 2, c = Math.cos(ang), s_ = Math.sin(ang);
    return [[p[0] + c * wa / 2, p[1] + s_ * wa / 2], [q[0] + c * wb / 2, q[1] + s_ * wb / 2], [q[0] - c * wb / 2, q[1] - s_ * wb / 2], [p[0] - c * wa / 2, p[1] - s_ * wa / 2]]; };
  const up = seg(sh, el, w0, w1), fo = seg(el, wr, w1, w2);
  const sleeve = new Path2D(); spl(sleeve, up, true, .4); const p2 = new Path2D(); spl(p2, fo, true, .4);
  const elbow = new Path2D(); elbow.arc(el[0], el[1], w1 / 2, 0, TAU);
  for (const q of [sleeve, elbow, p2]) knock(ctx, q);
  const col = o.col || 'khaki';
  for (const q of [sleeve, elbow, p2]) col === 'ink' ? inkFill(ctx, q) : plate(ctx, col, q);
  if (col !== 'ink') plate(ctx, col, p2, { a: .5 });
  // kontur: dış hatlar
  inkStroke(ctx, PL([up[0], up[1]], false), o.lw || 4.4); inkStroke(ctx, PL([up[3], up[2]], false), o.lw || 4.4);
  inkStroke(ctx, PL([fo[0], fo[1]], false), o.lw || 4.4); inkStroke(ctx, PL([fo[3], fo[2]], false), o.lw || 4.4);
  const cuffA = Math.atan2(wr[1] - el[1], wr[0] - el[0]);
  // kol ağzı
  const cuff = PL(seg([wr[0] - Math.cos(cuffA) * 12, wr[1] - Math.sin(cuffA) * 12], wr, w2 * 1.04, w2 * 1.04));
  knock(ctx, cuff); col === 'ink' ? inkFill(ctx, cuff) : plate(ctx, col, cuff, { n: 2 }); inkStroke(ctx, cuff, 3);
  if (col === 'ink') cut(ctx, PL([up[1], [el[0], el[1]]], false), 2, { a: .4 });
  else inkStroke(ctx, SP([[el[0] - 6, el[1] - 10], [el[0] + 4, el[1] + 2], [el[0] - 2, el[1] + 14]], false), 2, { a: .6 });
  return { el, wr, ang: cuffA };
}

// El: bilekten ang yönüne; kind: 'point' | 'rest' | 'hold'; s: px/birim (el boyu ≈ 40 birim); side: +1 başparmak üstte
function handDraw(ctx, x, y, ang, s, kind = 'rest', o = {}) {
  const side = o.side || 1, lw = px => px / s;
  ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s * side);
  const parts = [];
  const palm = SP([[0, -9], [14, -11], [24, -8], [26, 6], [16, 10], [2, 9]], true, .8);
  parts.push(palm);
  if (kind === 'point') {
    parts.push(SP([[22, -9], [44, -8.5], [47, -6], [44, -3.5], [22, -3]], true, .8)); // işaret parmağı
    for (const [yy, L] of [[-1.5, 30], [3.5, 29], [8, 26]]) parts.push(SP([[20, yy - 2.6], [L, yy - 2.8], [L + 3, yy], [L, yy + 2.8], [20, yy + 2.6]], true, .9)); // bükük parmaklar
    parts.push(SP([[8, -10], [20, -16], [27, -15], [24, -11], [14, -7]], true, .8)); // başparmak
  } else if (kind === 'hold') {
    for (const [yy, L] of [[-7, 34], [-2, 36], [3, 34], [8, 30]]) parts.push(SP([[22, yy - 2.6], [L, yy - 2.6], [L + 2.6, yy], [L, yy + 2.6], [22, yy + 2.6]], true, .9));
    parts.push(SP([[10, -10], [22, -18], [30, -19], [28, -14], [16, -6]], true, .8));
  } else {
    for (const [yy, L, a] of [[-7, 40, -.06], [-2, 43, -.01], [3, 41, .04], [8, 36, .1]]) parts.push(SP([[22, yy - 2.7], [L, yy - 2.6 + a * 20], [L + 2.7, yy + a * 20], [L, yy + 2.6 + a * 20], [22, yy + 2.7]], true, .9));
    parts.push(SP([[8, -10], [20, -17], [32, -19], [30, -14], [16, -6]], true, .8));
  }
  for (const q of parts) knock(ctx, q);
  if (o.skin) for (const q of parts) plate(ctx, 'skin', q);
  plate(ctx, o.skin ? 'skin' : 'ochre', SP([[0, 3], [16, 4], [26, 6], [16, 10], [2, 9]], true), { a: o.skin ? .8 : .4 });
  for (const q of parts) inkStroke(ctx, q, lw(2.6));
  ctx.restore();
}
