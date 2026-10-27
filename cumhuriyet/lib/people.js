// Kişiler: ¾ büst (bust3q), başlıklar (kalpak, fes, kabalak), giysiler (kaput, setre, sivil ceket), kollar ve eller.
// Baş birimleri: yüz +x yönüne dönük, köken göz hizasında; tepe ≈ -66, çene ≈ +52 (baş boyu ≈ 118 birim).
'use strict';
// Kişi kimlikleri (USLUP.md): yüz biçimi, kaş, bıyık, göz rengi. WD: ¾ yüz genişliği, HY: yüz boyu
const PEOPLE = {
  // Mustafa Kemal: uzun ince yüz, yüksek alın, ağır göz kapağı, keskin kaş; bıyık yaşa bağlı (1919 sonrası fotoğraflarda bıyıksız)
  mk: { name: 'MUSTAFA KEMAL', born: 1881, WD: 1.02, HY: 1.03, jaw: .98, cheek: 1.0, brow: .55, browW: 1.2, browY: 1.5, cheekWedge: 1, mus: a => a < 20 ? 'faint' : a < 38 ? 'mk' : null, iris: P.eye, hair: 'sepia', eyeOpen: .72, forehead: 3, seed: 3 },
  ismet: { name: 'İSMET', born: 1884, WD: 1.18, HY: .95, jaw: 1.04, cheek: 1.04, brow: .06, browW: .95, mus: 'thin', iris: P.sepia, hair: 'ink', ear: 1.15, eyeOpen: .8, seed: 5 },
  fevzi: { name: 'FEVZİ', born: 1876, WD: 1.08, HY: 1.0, jaw: 1.12, cheek: 1.02, brow: -.12, browW: 1.15, browY: -.6, mus: 'pala', musCol: 'grey', iris: P.sepia, hair: 'grey', eyeOpen: .76, bags: 1, seed: 7 },
  anon: { WD: 1.08, jaw: 1.02, cheek: 1, brow: .05, browW: 1, mus: 'mk', iris: P.sepia, hair: 'ink', seed: 9 },
};

// Baş çizimi. o: {x,y,s (px/birim), dir (+1 sağa bakar), who, gear:'kalpak'|'fes'|'kabalak'|'kefiye'|null, gearCol,
//   light:'front'|'back'|'top', lookAt:[x,y] (ekran) ya da look:[dx,dy], skin: true (yakın plan ten kalıbı), tilt, age}
// Birimler: göz hizası 0, tepe -64, çene ucu +57; yüz +x'e bakar. Burun kökü iki gözün arasında (19,-7); uzak göz burun sırtının ötesinde.
function head3q(ctx, o) {
  const pp = { ...PEOPLE.anon, ...(PEOPLE[o.who] || {}), ...(o.id || {}) };
  const s = o.s, dir = o.dir || 1, lw = px => Math.max(1.7 / s, px * Math.pow(s / 1.3, .75) / s);
  const age = o.age ?? 38, sd = pp.seed;
  const yg = clamp(inv(28, 18, age)), old = clamp(inv(36, 44, age));
  const jw = pp.jaw * (1 - yg * .03), ck = (pp.cheek || 1) + yg * .05;
  const WD = o.wide ?? pp.WD ?? 1.08, HY = pp.HY ?? 1;
  ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(o.tilt || 0); ctx.scale(s * dir * WD, s * HY);
  const face = [[26, -44], [30, -28], [32, -12], [33 * ck, 0], [34 * ck, 8], [32.5 * jw, 26], [29.5 * jw, 43], [22 * jw, 57 - yg * 1.5], [10, 58.5], [-14 * jw, 47], [-22 * jw, 36], [-25, 26], [-40, 22], [-54, 2], [-58, -24], [-50, -48], [-30, -62], [-4, -66], [16, -60]];
  const faceP = SP(rough(face, .25, sd), true, .9);
  knock(ctx, faceP);
  if (o.skin) plate(ctx, 'skin', faceP);
  const light = o.light || 'front', shPl = o.skin ? 'skin' : 'ochre', shA = o.skin ? .8 : .42;
  // tek terminatör düzlemi (kulak tarafı gölgede)
  let sh;
  if (light === 'front') sh = pp.cheekWedge && age >= 26
    ? [[-4, -50], [0, -28], [3, -10], [2, 2], [16, 13], [21, 22], [15, 29], [8, 40], [10, 52], [12, 62], [-30, 62], [-62, 20], [-62, -54]]
    : [[-4, -50], [0, -28], [3, -10], [10, 4], [14, 14], [12, 28], [7, 40], [10, 52], [12, 62], [-30, 62], [-62, 20], [-62, -54]];
  else if (light === 'back') sh = [[26, -44], [30, -28], [32, -12], [33, 0], [34, 8], [32.5, 26], [29.5, 43], [22, 57], [12, 60], [16, 34], [20, 10], [18, -20], [16, -44]];
  else sh = [[-60, 30], [36, 30], [36, 62], [-60, 62]];
  ctx.save(); ctx.clip(faceP); plate(ctx, shPl, SP(sh, true, .7), { a: shA });
  if (o.gear) plate(ctx, 'sepia', PL([[-60, -40 - (pp.forehead || 0)], [40, -40 - (pp.forehead || 0)], [40, -28 - (pp.forehead || 0)], [-60, -26 - (pp.forehead || 0)]]), { a: .4 }); // başlığın alna düşen gölgesi
  ctx.restore();
  // saç
  const hairPl = pp.hair;
  let hp;
  if (o.gear) hp = SP(rough([[-14, -36], [-30, -32], [-40, -18], [-44, 2], [-38, 14], [-30, 4], [-26, -12], [-20, -24]], .3, sd + 2), true, .9);
  else hp = SP(rough([[24, -44], [16, -52], [10, -60], [-6, -67], [-30, -66], [-52, -52], [-61, -26], [-56, 4], [-42, 18], [-32, 8], [-28, -10], [-18, -34], [-4, -47], [6, -53], [14, -48]], .35, sd + 3), true, .85);
  if (hairPl === 'ink') inkFill(ctx, hp);
  else { plate(ctx, hairPl, hp, { a: hairPl === 'sepia' ? .55 : 1 }); if (hairPl === 'sepia') plate(ctx, 'gold', hp, { a: .3 }); inkStroke(ctx, hp, lw(1.8)); }
  if (!o.gear) for (let i = 0; i < 7; i++) { const u = i / 6, q = new Path2D(); q.moveTo(lerp(16, -20, u), lerp(-50, -40, u)); q.quadraticCurveTo(lerp(-10, -36, u), lerp(-66, -54, u), lerp(-44, -56, u), lerp(-46, -14, u)); hairPl === 'ink' ? cut(ctx, q, lw(1.2), { a: .5 }) : inkStroke(ctx, q, lw(1.2), { a: .6 }); }
  // kulak
  const E_ = pp.ear || 1, ear = SP(rough([[-24, -6], [-30, -9], [-35, -4], [-36, 6], [-33, 16], [-27, 21], [-23, 16], [-23, 4]].map(([x, y]) => [-24 + (x + 24) * E_, y]), .2, sd + 4), true, .9);
  knock(ctx, ear); if (o.skin) plate(ctx, 'skin', ear);
  plate(ctx, shPl, ear, { a: shA });
  inkStroke(ctx, ear, lw(2.3)); inkStroke(ctx, SP([[-27, -3], [-31, 2], [-31, 10], [-28, 14]], false), lw(1.5));
  inkStroke(ctx, faceP, lw(3.4));
  // burun: sırt çizgisi yok; burun silueti uzak yanak konturunun önüne geçer (kontur burnun arkasında kalır)
  const noseSil = SP([[28.6, 1], [32.4, 7.6], [35.6, 15.4], [35.8, 19.2], [33.6, 21.4], [30.6, 21.6], [28.4, 18]], true, .8);
  knock(ctx, noseSil); if (o.skin) plate(ctx, 'skin', noseSil);
  plate(ctx, shPl, PL([[27, 6], [31, 8], [32, 18], [28, 20]]), { a: shA * 1.1 });               // yakın yandaki burun gölgesi (çizgisiz)
  plate(ctx, shPl, SP([[24, 20], [30, 21.6], [35, 20.6], [32, 24.5], [26, 24]], true), { a: shA }); // burun altı
  inkStroke(ctx, SP([[32.6, 7.8], [35.6, 15.4], [35.8, 19.2], [33.6, 21.4], [30.4, 21.7]], false, .8), lw(2.6)); // dış hat: sırtın ucu, uç, alt
  inkStroke(ctx, SP([[22, 17], [23.2, 20.4], [27, 21.6]], false), lw(2));                        // burun deliği kıvrımı
  // gözler: ağır üst kapak
  const target = o.lookAt ? (() => { const ex = o.x + 6 * s * dir * WD, ey = o.y; const dx = (o.lookAt[0] - ex) * dir, dy = o.lookAt[1] - ey, n = Math.hypot(dx, dy) || 1; return [dx / n * 1.5, dy / n * 1.1]; })() : (o.look || [1, .3]);
  const eo = o.eyeOpen ?? pp.eyeOpen ?? .8;
  for (const [k, e] of [[0, { c: [5.5, -1], w: 9 }], [1, { c: [27, -1], w: 3.8 }]]) {
    const [ex, ey] = e.c, w = e.w, h = (k ? 3.6 : 4.2) * eo * (1 + yg * .12);
    const eyeP = new Path2D(); eyeP.moveTo(ex - w, ey + .8); eyeP.bezierCurveTo(ex - w * .5, ey - h * 1.25, ex + w * .4, ey - h * 1.3, ex + w, ey - .1);
    eyeP.bezierCurveTo(ex + w * .45, ey + h * .85, ex - w * .55, ey + h * .85, ex - w, ey + .8);
    knock(ctx, eyeP, '#F6F0E2');
    ctx.save(); ctx.clip(eyeP);
    const ix = ex + target[0] * (k ? .55 : 1) + (k ? .4 : .3), iy = ey + target[1] + .9, ir = k ? 2.6 : 3.4;
    ctx.fillStyle = pp.iris; ctx.beginPath(); ctx.arc(ix, iy, ir, 0, TAU); ctx.fill();
    ctx.fillStyle = P.ink; ctx.beginPath(); ctx.arc(ix, iy, ir * .45, 0, TAU); ctx.fill();
    ctx.fillStyle = '#FCF9F1'; ctx.beginPath(); ctx.arc(ix + ir * .3, iy - ir * .4, ir * .24, 0, TAU); ctx.fill();
    plate(ctx, 'ochre', PL([[ex - w, ey - h * 1.5], [ex + w, ey - h * 1.5], [ex + w, ey - h * .2], [ex - w, ey - h * .3]]), { a: .32 });
    ctx.restore();
    const lid = new Path2D(); lid.moveTo(ex - w - (k ? .4 : 1.5), ey + 1.2); lid.bezierCurveTo(ex - w * .5, ey - h * 1.3, ex + w * .4, ey - h * 1.38, ex + w + .5, ey - .1);
    inkStroke(ctx, lid, lw(k ? 2.4 : 3.4));
    const fold = new Path2D(); fold.moveTo(ex - w * .7, ey - h * 1.75); fold.quadraticCurveTo(ex + w * .05, ey - h * 2.2, ex + w * .8, ey - h * 1.6);
    inkStroke(ctx, fold, lw(1.2), { a: .55 });
    if (!k) { const low = new Path2D(); low.moveTo(ex - w * .95, ey + h * .5); low.quadraticCurveTo(ex - w * .5, ey + h * .95, ex, ey + h * .9); inkStroke(ctx, low, lw(1.2), { a: .55 }); }
    if (pp.bags || old > 0) { const bg = new Path2D(); bg.moveTo(ex - w * .7, ey + h * 1.7); bg.quadraticCurveTo(ex - w * .1, ey + h * 2.3, ex + w * .5, ey + h * 1.7); inkStroke(ctx, bg, lw(1.1), { a: .35 + (pp.bags ? .15 : 0) }); }
  }
  // kaşlar: göze yakın; pp.brow > 0 dış uç yukarı kırılır
  const bA = pp.brow, bW = pp.browW, bY = pp.browY || 0;
  const nb = rough([[14.5, -9.6 + bY], [7, -11.6 + bY - bA * 1.5], [-2, -13.2 + bY - bA * 3], [-6, -12.2 + bY - bA * 4.6], [-6.5, -13.8 + bY - bA * 4.6 - 1.4 * bW], [-2, -15.6 + bY - bA * 3 - 1.6 * bW], [7, -14.6 + bY - bA * 1.5 - 2 * bW], [14.8, -12.2 + bY - 1.6 * bW]], .1, sd + 8);
  inkFill(ctx, SP(nb, true, .7));
  inkFill(ctx, SP([[23, -10 + bY], [28, -11.2 + bY - bA * 1.2], [31.6, -10.6 + bY - bA * 2], [31.6, -12.2 + bY - bA * 2 - 1.2 * bW], [28, -12.8 + bY - bA * 1.2 - 1.8 * bW], [23, -11.6 + bY - 1.4 * bW]], true, .7));
  if (o.who === 'mk') inkStroke(ctx, SP([[0, -9.5], [8, -8.6]], false), lw(1), { a: .4 }); // kaş kemiği altı
  // yaş çizgileri
  if (old > 0) {
    inkStroke(ctx, SP([[29, 22], [26, 29], [24, 36]], false), lw(1.2), { a: .45 * old });
    inkStroke(ctx, PL([[17.6, -15], [18, -10.4]], false), lw(1.1), { a: .4 * old });
  }
  if (pp.lines) inkStroke(ctx, SP([[-2, -28], [10, -30], [22, -28]], false), lw(1.1), { a: .3 });
  if (age >= 28 && age < 38 && o.who === 'mk') inkStroke(ctx, SP([[8, 12], [13, 18], [15, 24]], false), lw(1.1), { a: .35 }); // elmacık altı çukur
  // ağız ve çene
  const mus0 = typeof pp.mus === 'function' ? pp.mus(age) : pp.mus;
  if (mus0 !== 'pala') inkStroke(ctx, SP([[17, 33.6], [25, 33.4], [31, 33.9]], false), lw(2.3));
  plate(ctx, shPl, SP([[19.5, 37.2], [25, 38.6], [29.5, 37.4], [25, 40.2]], true), { a: shA * .8 });
  inkStroke(ctx, SP([[20.5, 39], [25, 39.8], [28.5, 38.8]], false), lw(1.2), { a: .4 });
  inkStroke(ctx, SP([[15, 51.5], [20, 52.5]], false), lw(1.2), { a: .4 });
  // bıyık
  const mus = typeof pp.mus === 'function' ? pp.mus(age) : pp.mus;
  if (mus) {
    let m;
    if (mus === 'pala') m = [[14, 28.6], [18, 25.6], [26, 24], [31, 25], [34, 28.4], [36, 33], [34.4, 33.2], [31, 30.4], [26, 30.8], [20, 30.8], [15.6, 33.4], [14, 34]];
    else if (mus === 'thin') m = [[17, 28.4], [24, 25.8], [31, 25.9], [34.5, 27.8], [31, 28.8], [24, 28], [18, 29.4]];
    else if (mus === 'faint') m = [[17, 28.6], [24, 26.6], [31, 26.6], [33.4, 28], [30, 28.4], [24, 27.8], [18, 29.2]];
    else m = [[14, 29], [18.5, 26.4], [26, 24.6], [31, 25.6], [33.5, 27.6], [30, 28.6], [26, 27.8], [20, 29.2], [15, 30.2]];
    const mP = SP(rough(m, .12, sd + 6), true, .9);
    knock(ctx, mP);
    if (pp.musCol === 'grey') {
      plate(ctx, 'grey', mP, { a: .7 }); inkStroke(ctx, mP, lw(1.6));
      for (const q of [[[17, 27], [22, 27.6], [25, 30]], [[23, 25.8], [28.5, 26.8], [32, 30.6]], [[27, 25.4], [31.6, 26.6], [34.2, 31.8]]]) inkStroke(ctx, SP(q, false), lw(1.1), { a: .55 });
    } else if (hairPl !== 'ink') { plate(ctx, 'sepia', mP, { a: mus === 'faint' ? .45 : .9 }); inkStroke(ctx, mP, lw(mus === 'faint' ? 1 : 1.6), { a: mus === 'faint' ? .5 : 1 }); }
    else { inkFill(ctx, mP); for (let i = 0; i < 3; i++) { const x = 20 + i * 4.5; cut(ctx, SP([[x, 26.4], [x + 1.4, 28.6]], false), lw(.9), { a: .35 }); } }
  }
  ctx.restore();
  if (o.gear) headgear(ctx, { ...o, sd, WD, HY, lift: pp.forehead || 0 });
}

// Başlıklar (baş koordinatında)
function headgear(ctx, o) {
  const s = o.s, dir = o.dir || 1, lw = px => Math.max(1.7 / s, px * Math.pow(s / 1.3, .75) / s), sd = o.sd || 1;
  ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(o.tilt || 0); ctx.scale(s * dir * (o.WD || 1), s * (o.HY || 1)); ctx.translate(0, -(o.lift || 0));
  if (o.gear === 'kalpak') {
    // ¾ silindir; hafifçe daralan; tepe kenarı içe dönük
    const body = SP(rough([[-60, -14], [-60, -42], [-57, -70], [-44, -82], [-14, -88], [16, -87], [33, -80], [36, -56], [37, -28], [24, -33], [2, -34], [-26, -26], [-48, -18]], .5, sd + 10), true, .7);
    knock(ctx, body);
    const col = o.gearCol || 'ink';
    if (col === 'ink') inkFill(ctx, body); else { plate(ctx, col, body); inkStroke(ctx, body, lw(3.6)); }
    // kıvırcık kuzu yünü: kazıma ilmikler (ink) ya da is ilmikler (gri)
    const r = rng(sd + 11);
    ctx.save(); ctx.clip(body);
    for (let row = 0; row < 7; row++) for (let i = 0; i < 26; i++) {
      const u = (i + (row % 2) * .5 + r() * .3) / 26, v = (row + .3 + r() * .4) / 7;
      const x = lerp(-58, 35, u) + (r() - .5) * 3, ytop = lerp(-82, -86, u) + 2, ybot = lerp(-17, -31, u);
      const y = lerp(ytop, ybot, v) + (r() - .5) * 3, rr = (1.1 + r() * .7) * (.7 + r() * .6), a0 = r() * TAU;
      const q = new Path2D(); q.arc(x, y, rr, a0, a0 + PI * (.8 + r() * .4));
      col === 'ink' ? cut(ctx, q, lw(1.15), { a: .28 + (1 - v) * .3 }) : inkStroke(ctx, q, lw(1.1), { a: .5 });
    }
    ctx.restore();
    // tepe: açık oval kenar (ışık üstten)
    const top = new Path2D(); top.ellipse(-12, -79, 42, 5.5, -.05, PI * 1.05, PI * 1.95);
    ctx.save(); ctx.clip(body); col === 'ink' ? cut(ctx, top, lw(2), { a: .7 }) : inkStroke(ctx, top, lw(2)); ctx.restore();
    // alt kenar gölgesi alında
    inkStroke(ctx, SP([[-48, -18], [-26, -26], [2, -34], [24, -33], [37, -28]], false), lw(3.2));
  } else if (o.gear === 'fes') {
    const body = SP(rough([[-50, -18], [-46, -52], [-42, -86], [-12, -90], [14, -88], [24, -58], [32, -28], [10, -32], [-22, -24]], .4, sd + 12), true, .5);
    knock(ctx, body); plate(ctx, 'red', body); plate(ctx, 'red', SP([[-46, -22], [-40, -56], [-34, -84], [-20, -88], [-24, -50], [-28, -26]], true), { a: .6 });
    inkStroke(ctx, body, lw(3.6));
    const top = new Path2D(); top.ellipse(-12, -84, 27, 4, -.06, PI, TAU); inkStroke(ctx, top, lw(2));
    // püskül
    inkFill(ctx, SP([[-12, -86], [-34, -78], [-48, -56], [-52, -36], [-46, -38], [-40, -58], [-26, -76], [-10, -82]], true));
  } else if (o.gear === 'kefiye') {
    const cloth = SP(rough([[-78, 120], [-80, 40], [-70, -10], [-62, -50], [-40, -78], [-6, -88], [22, -82], [38, -56], [40, -26], [30, -24], [24, -30], [-4, -34], [-28, -24], [-36, 10], [-34, 60], [-20, 112]], .7, sd + 14), true, .8);
    knock(ctx, cloth); plate(ctx, 'ochre', cloth, { a: .22 }); inkStroke(ctx, cloth, lw(3.2));
    plate(ctx, 'ochre', SP([[-78, 120], [-80, 40], [-70, -10], [-60, -40], [-54, 20], [-50, 116]], true), { a: .4 });
    for (const q of [[[-66, -30], [-70, 60], [-66, 116]], [[-52, -50], [-56, 30], [-50, 110]], [[-40, 0], [-42, 60], [-34, 108]]]) inkStroke(ctx, SP(q, false), lw(1.5), { a: .6 });
    for (const dy of [0, 7]) { const agal = SP([[-62, -44 + dy], [-30, -60 + dy], [8, -64 + dy], [37, -50 + dy]], false, .7); inkStroke(ctx, agal, lw(4.6)); cut(ctx, agal, lw(1), { a: .35 }); }
  } else if (o.gear === 'kabalak') {
    const body = SP(rough([[-62, -12], [-64, -40], [-50, -66], [-16, -78], [18, -74], [38, -52], [40, -24], [22, -28], [-6, -26], [-36, -16]], .6, sd + 13), true, .8);
    knock(ctx, body); plate(ctx, 'khaki', body);
    plate(ctx, 'khaki', SP([[-62, -12], [-64, -40], [-50, -66], [-32, -74], [-38, -42], [-40, -16]], true));
    inkStroke(ctx, body, lw(3.8));
    ctx.save(); ctx.clip(body); for (let i = -3; i < 6; i++) { const q = new Path2D(); q.moveTo(-70 + i * 16, -10); q.bezierCurveTo(-50 + i * 16, -40, -30 + i * 18, -70, -4 + i * 18, -96); inkStroke(ctx, q, lw(1.8), { a: .6 }); } ctx.restore();
  }
  ctx.restore();
}

// Gövde (büst): omuzlar, yaka, kaput/setre/ceket. Baş koordinatında çizilir: boyun tabanı ≈ (−6, 78)
// o: {x,y,s,dir, coat:'kaput'|'setre'|'civil', col:'khaki'|'ink'|'navy'|..., w (omuz genişliği çarpanı), len (alt sınır, birim), tilt}
function bust(ctx, o) {
  const s = o.s, dir = o.dir || 1, lw = px => Math.max(1.7 / s, px * Math.pow(s / 1.3, .75) / s), sd = (o.seed || 1) + 40, W_ = o.w || 1, len = o.len || 330;
  ctx.save(); ctx.translate(o.x, o.y); ctx.rotate(o.tilt || 0); ctx.scale(s * dir, s);
  const col = o.col || 'khaki', dark = col === 'ink', tu = o.turn || 0, TX = tu * 26, FS = 1 - .15 * tu;
  const fillC = (p, n = 1, a = 1) => dark ? inkFill(ctx, p) : plate(ctx, col, p, { n, a });
  // boyun: ön çizgi çene altından
  const neck = SP([[-28, 30], [-30, 78], [18, 82], [15, 50]], true, .6);
  knock(ctx, neck); if (o.skin) plate(ctx, 'skin', neck);
  plate(ctx, o.skin ? 'skin' : 'ochre', SP([[-28, 30], [-29.6, 66], [17, 66], [16, 60], [6, 56]], true), { a: o.skin ? .8 : .42 });
  inkStroke(ctx, SP([[-28, 34], [-29.6, 62]], false), lw(3.2)); inkStroke(ctx, SP([[15, 52], [16, 62]], false), lw(3));
  const body = SP(rough([[-26, 74], [-64 * W_, 88], [-92 * W_, 112], [-100 * W_, 170], [-102 * W_, len], [74 * W_ * FS, len], [72 * W_ * FS, 168], [66 * W_ * FS, 110], [46 * W_ * FS, 86], [16, 78]], .7, sd), true, .75);
  if (o.sep) inkStroke(ctx, body, 8 / s, { col: P.paper });
  knock(ctx, body); fillC(body);
  if (o.back) plate(ctx, col, body, { a: .35 });
  if (!dark) plate(ctx, col, SP([[-26, 74], [-64 * W_, 88], [-92 * W_, 112], [-100 * W_, 170], [-102 * W_, len], [-58, len], [-60, 170], [-52, 110]], true, .8), { a: .6 });
  ctx.save(); ctx.clip(body);
  if (o.coat === 'kaput') {
    // dik iç yaka (haki) + omuza uzanan geniş devrik kaput yakası; küçük apoletler
    const band = SP([[-30, 62], [-32, 78], [16, 82], [18, 66]], true, .6);
    knock(ctx, band); fillC(band); inkStroke(ctx, band, lw(2.2));
    const lapN = PL(rough([[-28, 76], [-88 * W_, 100], [-80 * W_, 124], [-36 + TX, 160], [-8 + TX, 190], [-10 + TX * .6, 112]], .5, sd + 1));
    const lapF = PL(rough([[16, 80], [64 * W_ * FS, 98], [58 * W_ * FS, 120], [26 + TX, 156], [4 + TX, 192], [4 + TX * .6, 114]], .5, sd + 2));
    for (const l of [lapN, lapF]) { knock(ctx, l); fillC(l); if (!dark) plate(ctx, col, l, { a: .3 }); inkStroke(ctx, l, lw(2.6)); }
    const v = PL([[-10 + TX * .6, 112], [4 + TX * .6, 114], [4 + TX, 192], [-2 + TX, 198], [-8 + TX, 190]]);
    knock(ctx, v); fillC(v, 1); if (!dark) plate(ctx, col, v, { a: .5 }); inkStroke(ctx, v, lw(1.6));
    for (const [bx, by] of [[-24 + TX, 232], [24 + TX, 232], [-25 + TX, 292], [26 + TX, 292]]) { const b = new Path2D(); b.arc(bx, by, 4.2, 0, TAU); knock(ctx, b); plate(ctx, 'ochre', b, { n: 2 }); inkStroke(ctx, b, lw(1.5)); }
    inkStroke(ctx, SP([[-2 + TX, 198], [TX, len]], false), lw(2.4));
    for (const [x0, x1, y0] of [[-96 * W_, -66 * W_, 100], [46 * W_ * FS, 66 * W_ * FS, 94]]) { const ap = PL([[x0, y0 + 2], [x1, y0 - 4], [x1, y0 + 4], [x0, y0 + 10]]); knock(ctx, ap); fillC(ap, 1); plate(ctx, 'gold', ap, { a: .6 }); inkStroke(ctx, ap, lw(1.6)); }
    if (dark) { cut(ctx, SP([[-80, 124], [-8, 190]], false), lw(1.8), { a: .6 }); cut(ctx, SP([[58, 120], [4, 192]], false), lw(1.8), { a: .6 }); }
  } else if (o.coat === 'setre') {
    const coll = SP([[-30, 64], [-32, 78], [-10, 82], [16, 80], [18, 66]], true, .6);
    knock(ctx, coll); plate(ctx, o.collarCol || col, coll, { n: o.collarCol ? 1 : 1 }); inkStroke(ctx, coll, lw(2.4));
    inkStroke(ctx, SP([[-12, 80], [-6, 86], [0, 80]], false), lw(1.6));
    for (let i = 0; i < 5; i++) { const b = new Path2D(); b.arc(-6, 112 + i * 38, 3.8, 0, TAU); knock(ctx, b); plate(ctx, 'ochre', b, { n: 2 }); inkStroke(ctx, b, lw(1.4)); }
    inkStroke(ctx, SP([[-4, 84], [-2, len]], false), lw(2.2));
    for (const q of [[[-60, 150], [-20, 154]], [[30, 150], [60, 146]]]) inkStroke(ctx, SP(q, false), lw(1.8), { a: .6 }); // cep kapakları
  } else if (o.coat === 'civil') {
    const shirt = SP([[-20, 76], [14, 80], [4, 160], [-8, 160]], true); knock(ctx, shirt); inkStroke(ctx, shirt, lw(1.8));
    const coll = SP([[-22, 66], [-24, 84], [-6, 96], [12, 86], [14, 70]], true, .6); knock(ctx, coll); inkStroke(ctx, coll, lw(1.8));
    const tie = SP([[-8, 90], [2, 90], [5, 150], [-2, 162], [-9, 150]], true); knock(ctx, tie); inkFill(ctx, tie); cut(ctx, SP([[-4, 100], [0, 146]], false), lw(1.1), { a: .4 });
    const lapN = SP([[-24, 74], [-62 * W_, 92], [-42, 150], [-6, 214], [-12, 130]], true, .7), lapF = SP([[14, 78], [48 * W_, 96], [36, 150], [4, 216], [8, 132]], true, .7);
    for (const l of [lapN, lapF]) { knock(ctx, l); fillC(l, 2); inkStroke(ctx, l, lw(2.4)); }
    if (dark) { cut(ctx, SP([[-42, 150], [-6, 214]], false), lw(1.7), { a: .55 }); cut(ctx, SP([[36, 150], [4, 216]], false), lw(1.7), { a: .55 }); }
  }
  if (o.arms === 'back') for (const [x0, x1, sg] of [[-86 * W_, -80 * W_, -1], [60 * W_ * FS, 56 * W_ * FS, 1]]) {
    inkStroke(ctx, SP([[x0, 118], [x0 + sg * 4, 200], [x1, 300]], false), lw(2.6));
    for (const yy of [212, 228]) inkStroke(ctx, SP([[x0 + sg * 2, yy], [x0 - sg * 10, yy + 6]], false), lw(1.8), { a: .6 });
  }
  const folds = [[[-82, 190], [-70, 250], [-74, 320]], [[58, 200], [52, 280]], [[-88, 132], [-70, 150]]];
  for (const q of folds) dark ? cut(ctx, SP(q, false), lw(1.7), { a: .4 }) : inkStroke(ctx, SP(q, false), lw(1.7), { a: .5 });
  ctx.restore();
  inkStroke(ctx, body, lw(3.6));
  ctx.restore();
}

// Kol: omuzdan (dünya koordinatı) ele iki kemikli ters kinematik; tek parça kol yolu (dirsekte açıortay)
function arm(ctx, sh, hand, o) {
  const a = o.upper, b = o.fore, bend = o.bend ?? 1;
  const dx = hand[0] - sh[0], dy = hand[1] - sh[1], d = clamp(Math.hypot(dx, dy), Math.abs(a - b) + 1, (a + b) * .999);
  const phi = Math.atan2(dy, dx), al = Math.acos(clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1));
  const ua = phi - bend * al, el = [sh[0] + Math.cos(ua) * a, sh[1] + Math.sin(ua) * a];
  const wr = [sh[0] + Math.cos(phi) * d, sh[1] + Math.sin(phi) * d];
  const w0 = o.w || 40, w1 = w0 * .9, w2 = w0 * .7;
  const a1 = Math.atan2(el[1] - sh[1], el[0] - sh[0]), a2 = Math.atan2(wr[1] - el[1], wr[0] - el[0]);
  const nrm = an => [Math.cos(an + PI / 2), Math.sin(an + PI / 2)];
  const n1 = nrm(a1), n2 = nrm(a2), nb = (() => { const x = n1[0] + n2[0], y = n1[1] + n2[1], l = Math.hypot(x, y) || 1; return [x / l, y / l]; })();
  const kb = 1 / Math.max(.45, (n1[0] * nb[0] + n1[1] * nb[1]));
  const L = [[sh[0] + n1[0] * w0 / 2, sh[1] + n1[1] * w0 / 2], [el[0] + nb[0] * w1 / 2 * kb, el[1] + nb[1] * w1 / 2 * kb], [wr[0] + n2[0] * w2 / 2, wr[1] + n2[1] * w2 / 2]];
  const R = [[wr[0] - n2[0] * w2 / 2, wr[1] - n2[1] * w2 / 2], [el[0] - nb[0] * w1 / 2 * kb, el[1] - nb[1] * w1 / 2 * kb], [sh[0] - n1[0] * w0 / 2, sh[1] - n1[1] * w0 / 2]];
  const sleeve = PL([...L, ...R]);
  knock(ctx, sleeve);
  const col = o.col || 'khaki';
  col === 'ink' ? inkFill(ctx, sleeve) : plate(ctx, col, sleeve);
  inkStroke(ctx, PL(L, false), o.lw || 4); inkStroke(ctx, PL(R, false), o.lw || 4);
  // kol ağzı
  const c0 = [wr[0] - Math.cos(a2) * 12, wr[1] - Math.sin(a2) * 12];
  const cuff = PL([[c0[0] + n2[0] * w2 * .54, c0[1] + n2[1] * w2 * .54], [wr[0] + n2[0] * w2 * .54, wr[1] + n2[1] * w2 * .54], [wr[0] - n2[0] * w2 * .54, wr[1] - n2[1] * w2 * .54], [c0[0] - n2[0] * w2 * .54, c0[1] - n2[1] * w2 * .54]]);
  knock(ctx, cuff); col === 'ink' ? inkFill(ctx, cuff) : plate(ctx, col, cuff, { n: 2 }); inkStroke(ctx, cuff, 2.6);
  // dirsek kıvrımları
  const fx = (k, l) => [el[0] + nb[0] * k + Math.cos(a2) * l, el[1] + nb[1] * k + Math.sin(a2) * l];
  for (const [k, l] of [[-w1 * .2, -8], [-w1 * .05, 6]]) { const q = SP([fx(k - 8, l), fx(k, l + 4), fx(k + 8, l)], false); col === 'ink' ? cut(ctx, q, 2, { a: .45 }) : inkStroke(ctx, q, 2, { a: .55 }); }
  return { el, wr, ang: a2, w2 };
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
  { const U = new Path2D(); for (const q of parts) U.addPath(q); ctx.save(); ctx.clip(U); plate(ctx, o.skin ? 'skin' : 'ochre', PL([[-10, 1.5], [60, 1.5], [60, 20], [-10, 20]]), { a: o.skin ? .8 : .38 }); ctx.restore(); }
  for (const q of parts) inkStroke(ctx, q, lw(2.6));
  ctx.restore();
}
