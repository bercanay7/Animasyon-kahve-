// act0: 0 · AÇILIŞ (A01–A05). Çankaya gecesi → sofra → "Yarın Cumhuriyet…" → kuşak şeridi 1923 ↔ 1893 mektep sırası
// → II. Abdülhamid portresi → başlık kartı "BİR KUŞAĞIN HİKÂYESİ". Yardımcılar a0_ önekli; act6 de bunları kullanır.
'use strict';

// ——— yardımcılar ———
// kelime zamanı; bulunamazsa konsola yazar (Wd sessizce cümle başına döner)
const A0_MISS = new Set();
function a0_W(id, w, n = 0, end = false) {
  const nw = w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  const hit = (window.WORDS || []).filter(x => x.id === id && x.w.startsWith(nw)).length > n;
  if (!hit && !A0_MISS.has(id + w)) { A0_MISS.add(id + w); console.log('[a0] kelime bulunamadı:', id, w); }
  return Wd(id, w, n, end);
}
// Önbellek: geçiş sırasında (REG.boost > 1) kurulursa kayıklık zemine kalıcı işlenmesin diye boost=1 ile kurulur
function a0_cache(key, draw, w, h) {
  if (LCACHE[key]) return LCACHE[key];
  const b = REG.boost; REG.boost = 1;
  try { return layerCache(key, draw, w, h); } finally { REG.boost = b; }
}
// önbellekli katmanı kamera + paralaks ile çiz
function a0_layer(ctx, img, c, k) { ctx.save(); cam(ctx, c, k); ctx.drawImage(img, 0, 0, W, H); ctx.restore(); }
// figür: büst + ¾ baş; boşta salınım ve göz kırpma 15 fps pozla (ikişer kare)
function a0_fig(ctx, f, t) {
  const tf = Math.floor(t * 15) / 15, sd = f.seed ?? 1;
  const io = idleOffsets(tf, sd, f.idle ?? 1), bl = f.blink === false ? 0 : blinkAt(tf + sd * .37, sd);
  const pp = { ...PEOPLE.anon, ...(PEOPLE[f.who] || {}), ...(f.id || {}) };
  const s = f.s, dir = f.dir || -1, x = f.x, y = f.y + io.breath * s * .45;
  bust(ctx, { x, y, s, dir, coat: f.coat, col: f.col, w: f.w ?? .96, seed: sd, len: f.len, tilt: (f.btilt || 0) + io.torso * .5, turn: f.turn, sep: f.sep, back: f.back, arms: f.arms, skin: f.skin, collarCol: f.collarCol });
  if (f.under) f.under(ctx);
  head3q(ctx, { x: x + io.neck * s * 5 * dir, y, s, dir, who: f.who, id: f.id, gear: f.gear, gearCol: f.gearCol || 'ink', light: f.light || 'front', lookAt: f.lookAt, look: f.look, age: f.age, tilt: (f.tilt || 0) + io.head, skin: f.skin, eyeOpen: (f.eyeOpen ?? pp.eyeOpen ?? .8) * (1 - .9 * bl) });
}
// damga gibi beliren öğe: darbe ölçeği + saydamlık (kalıcı)
function a0_hit(lt, a = 0, dur = .16) { const u = clamp((lt - a) / dur); return { a: u > 0 ? Math.min(1, u * 3) : 0, k: 1 + (1 - E.out3(u)) * .22 }; }
// yaş levhası: büyük Abril sayı + Courier alt satır, basılma darbesiyle
function a0_age(ctx, x, y, num, sub, lt, o = {}) {
  if (NOTEXT) return;
  const h = a0_hit(lt, 0, .15); if (h.a <= 0) return;
  ctx.save(); ctx.globalAlpha = h.a * (o.a ?? 1); ctx.translate(x, y); ctx.scale(h.k, h.k);
  txt(ctx, String(num), 0, 0, FONT.title(o.size || 96), { align: 'center', ls: 1 });
  if (sub) txt(ctx, sub, 0, 54, FONT.mono(30), { align: 'center', ls: 3 });
  ctx.restore();
}
// kuşak şeridi bandı: düz kalıp + üst/alt is çizgisi
function a0_band(ctx, y0, y1, pl = 'ochre', a = .55) {
  plate(ctx, pl, PL([[-20, y0], [W + 20, y0], [W + 20, y1], [-20, y1]]), { a });
  inkStroke(ctx, PL([[-20, y0], [W + 20, y0]], false), 4); inkStroke(ctx, PL([[-20, y1], [W + 20, y1]], false), 4);
}
// çay bardağı (ince belli) tabağıyla; x,y tabağın merkezi
function a0_tea(ctx, x, y, s, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const lw = px => px / s;
  const sau = new Path2D(); sau.ellipse(0, 0, 17, 4.2, 0, 0, TAU);
  knock(ctx, sau); plate(ctx, 'ochre', sau, { a: .25 }); inkStroke(ctx, sau, lw(1.6));
  const gl = SP([[-8, -1], [-6.4, -5], [-4.6, -12], [-7.4, -22], [-9, -31], [9, -31], [7.4, -22], [4.6, -12], [6.4, -5], [8, -1]], true, .7);
  knock(ctx, gl);
  const tea = SP([[-6.6, -2], [-5.4, -5.4], [-4.2, -12], [-6.8, -21], [-8.2, -27], [8.2, -27], [6.8, -21], [4.2, -12], [5.4, -5.4], [6.6, -2]], true, .7);
  if (o.empty !== true) { plate(ctx, 'ochre', tea, { n: 2 }); plate(ctx, 'sepia', tea, { a: .35 }); plate(ctx, 'gold', PL([[-4, -25], [-2, -25], [-1.6, -8], [-3, -8]]), { a: .8 }); }
  inkStroke(ctx, gl, lw(1.5)); inkStroke(ctx, PL([[-9, -31], [9, -31]], false), lw(1.2));
  ctx.restore();
}
// profil siluet (damga): baş + boyun + omuz; yüz +x yönünde, x,y göz hizası. kind: 'kalpak' | 'fes' | 'bare' | 'bald'
function a0_profPath(o = {}) {
  const m = o.mus;
  const pts = [[22, -54], [30, -36], [34, -16], [31, -8], [37, 2], [44, 14], [41, 19], [34, 22], m ? [41, 25] : [36, 28], m ? [37, 30] : [33, 32], [35, 36], [31, 41], [34, 50], [28, 57], [12, 60], [9, 70], [12, 80],
    [30, 88], [58, 104], [70, 140], [72, o.bot || 172], [-98, o.bot || 172], [-96, 160], [-86, 116], [-62, 92], [-34, 80], [-32, 62], [-38, 40], [-48, 22], [-58, -4], [-56, -30], [-38, -60], [-8, -69]];
  return SP(rough(pts, .35, o.seed || 1), true, .5);
}
const A0_KALPAK = [[26, -46], [30, -88], [-10, -91], [-50, -87], [-55, -36], [-14, -43]];
const A0_FES = [[24, -46], [15, -100], [-34, -99], [-50, -36], [-14, -42]];
function a0_prof(ctx, x, y, s, dir, kind, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.tilt || 0); ctx.scale(s * dir, s);
  const lw = px => px / s, sd = o.seed || 1;
  // parçalar ayrı ayrı doldurulur (üst üste binen alt yollar nonzero kuralında delik açmasın)
  const p = a0_profPath(o), parts = [p];
  if (kind === 'kalpak') parts.push(SP(rough(A0_KALPAK, .8, sd + 1), true, .25));
  if (kind === 'fes') parts.push(SP(rough(A0_FES, .6, sd + 2), true, .2));
  if (kind === 'bare') parts.push(SP([[22, -54], [10, -66], [-20, -72], [-50, -56], [-60, -20], [-50, -10], [-30, -40], [0, -56]], true, .7));
  for (const q of parts) { inkFill(ctx, q); if (o.col) plate(ctx, o.col, q, { a: o.colA ?? .5 }); }
  // ışık tarafında kontur üzerinde kâğıt çizgi (ışık kenarı), kulak, beyaz yaka, yaka kıvrımı
  cut(ctx, SP([[22, -54], [30, -36], [34, -16], [31, -8], [37, 2], [44, 14]], false, .5), lw(2.4), { a: o.rim ?? .6 });
  cut(ctx, SP([[-12, -8], [-19, -4], [-19, 8], [-12, 14]], false), lw(1.8), { a: .45 });
  const coll = PL([[9, 70], [20, 82], [16, 94], [3, 86], [5, 74]]); knock(ctx, coll); inkStroke(ctx, coll, lw(1.4));
  cut(ctx, SP([[16, 94], [34, 130], [46, 170]], false), lw(1.8), { a: .35 });
  if (o.glasses) { const g = new Path2D(); g.ellipse(27, -5, 6.5, 5, 0, 0, TAU); cut(ctx, g, lw(1.6), { a: .7 }); cut(ctx, PL([[21, -5], [-8, -7]], false), lw(1.3), { a: .6 }); }
  if (kind === 'kalpak') {
    cut(ctx, SP([[26, -44], [-14, -42], [-55, -34]], false, .6), lw(2), { a: .55 });
    const r = rng(sd * 7);
    for (let i = 0; i < 16; i++) { const q = new Path2D(), xx = lerp(-48, 24, r()), yy = lerp(-84, -50, r()), a0 = r() * TAU; q.arc(xx, yy, 2.2, a0, a0 + 2.4); cut(ctx, q, lw(1.3), { a: .3 }); }
  }
  if (kind === 'fes') { cut(ctx, SP([[24, -46], [-14, -42], [-50, -36]], false, .6), lw(2), { a: .5 }); plate(ctx, 'red', SP(A0_FES, true, .2), { a: .5 }); inkStroke(ctx, SP([[-8, -99], [-30, -86], [-44, -60]], false), lw(5)); }
  ctx.restore();
}
// beş köşeli yıldız yolu (bayrak ve gece gökü)
function a0_starPath(p, cx, cy, R, rot = -PI / 2, k = .382) {
  for (let i = 0; i < 10; i++) { const a = rot + i * PI / 5, r = i % 2 ? R * k : R; const x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r; i ? p.lineTo(x, y) : p.moveTo(x, y); }
  p.closePath(); return p;
}
// kara tahta (çerçeve + soluk silinmiş izler; yazı yok). x0,y0,x1,y1 tahta alanı
function a0_board(ctx, x0, y0, x1, y1, seed, o = {}) {
  const fr = PL(rough([[x0 - 22, y0 - 22], [x1 + 22, y0 - 22], [x1 + 22, y1 + 22], [x0 - 22, y1 + 22]], 1, seed));
  knock(ctx, fr); plate(ctx, 'ochre', fr, { n: 2 }); inkStroke(ctx, fr, 3.4);
  const bd = PL([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]);
  if (o.green) { knock(ctx, bd); plate(ctx, 'teal', bd, { n: 2 }); plate(ctx, 'ink', bd, { a: .55 }); }
  else plate(ctx, 'ink', bd, { a: .86 });
  inkStroke(ctx, bd, 2.4);
  const r = rng(seed + 3);
  for (let i = 0; i < 9; i++) { const xx = lerp(x0 + 40, x1 - 200, r()), yy = lerp(y0 + 30, y1 - 30, r()), L = 120 + r() * 220; cut(ctx, SP([[xx, yy], [xx + L * .5, yy + (r() - .5) * 14], [xx + L, yy + (r() - .5) * 10]], false), 14, { a: .05 }); }
  const ledge = PL([[x0 - 26, y1 + 22], [x1 + 26, y1 + 22], [x1 + 30, y1 + 36], [x0 - 30, y1 + 36]]);
  knock(ctx, ledge); plate(ctx, 'ochre', ledge, { n: 2 }); plate(ctx, 'ink', ledge, { a: .3 }); inkStroke(ctx, ledge, 2.4);
}
// tebeşir geometri: üçgen + yükseklik, çember + kiriş, açı yayı, pergel yayı (yazı değil)
function a0_chalkGeo(ctx, list, a = .85) {
  for (const g of list) {
    const [kind, x, y, s] = g;
    if (kind === 'tri') {
      const A = [x - 70 * s, y + 50 * s], B = [x + 80 * s, y + 50 * s], C = [x + 10 * s, y - 60 * s];
      cut(ctx, PL(rough([A, B, C], 1.2, x)), 3, { a }); cut(ctx, PL([C, [C[0], A[1]]], false), 2, { a: a * .7 });
      cut(ctx, PL([[C[0], A[1] - 12 * s], [C[0] + 12 * s, A[1] - 12 * s], [C[0] + 12 * s, A[1]]], false), 1.6, { a: a * .7 });
    } else if (kind === 'circ') {
      const c = new Path2D(); c.ellipse(x, y, 60 * s, 58 * s, .1, 0, TAU); cut(ctx, c, 3, { a });
      cut(ctx, PL([[x - 52 * s, y - 28 * s], [x + 46 * s, y + 36 * s]], false), 2, { a: a * .8 });
      const d = new Path2D(); d.arc(x, y, 3 * s, 0, TAU); cut(ctx, d, 2.4, { a });
      cut(ctx, PL([[x, y], [x + 60 * s, y - 6 * s]], false), 1.8, { a: a * .7 });
    } else if (kind === 'ang') {
      cut(ctx, PL([[x + 90 * s, y], [x, y], [x + 70 * s, y - 60 * s]], false), 3, { a });
      const q = new Path2D(); q.arc(x, y, 34 * s, -0.71, 0); cut(ctx, q, 2, { a: a * .8 });
    } else if (kind === 'arc') {
      const q = new Path2D(); q.arc(x, y + 60 * s, 90 * s, -2.3, -.8); cut(ctx, q, 2, { a: a * .6 });
      cut(ctx, PL([[x - 60 * s, y + 52 * s], [x + 62 * s, y + 52 * s]], false), 2.6, { a });
    }
  }
}
// okul sırası (ön tahta + üst kapak; mürekkep hokkası, kitap). y0 üst kenar
function a0_desk(ctx, x0, x1, y0, y1, sd, o = {}) {
  const top = PL(rough([[x0, y0], [x1, y0 - 2], [x1 + 10, y0 + 18], [x0 - 10, y0 + 20]], .8, sd));
  knock(ctx, top); plate(ctx, 'ochre', top, { n: 2 }); inkStroke(ctx, top, 3);
  const fr = PL([[x0 - 10, y0 + 20], [x1 + 10, y0 + 18], [x1 + 10, y1], [x0 - 10, y1]]);
  knock(ctx, fr); plate(ctx, 'ochre', fr, { n: 2 }); plate(ctx, o.pl || 'sepia', fr, { a: .45 }); inkStroke(ctx, fr, 3);
  for (let x = x0 + 160; x < x1; x += 350) inkStroke(ctx, PL([[x, y0 + 22], [x, y1]], false), 2.2, { a: .7 });
  const r = rng(sd + 1);
  for (let i = 0; i < 5; i++) { const yy = y0 + 34 + i * 12; inkStroke(ctx, SP([[x0, yy], [lerp(x0, x1, .4), yy + (r() - .5) * 4], [x1, yy + (r() - .5) * 3]], false), 1.2, { a: .35 }); }
  for (const [bx, w, h, pl] of (o.books || [])) { const b = PL([[bx - w / 2, y0 + 4], [bx + w / 2, y0 + 4], [bx + w / 2 - 4, y0 - h], [bx - w / 2 - 2, y0 - h]]); knock(ctx, b); plate(ctx, pl, b, { a: .8 }); inkStroke(ctx, b, 2.2); inkStroke(ctx, PL([[bx - w / 2 + 6, y0 - h + 5], [bx + w / 2 - 8, y0 - h + 5]], false), 1.2, { a: .6 }); }
  for (const ix of (o.ink || [])) { const w_ = new Path2D(); w_.ellipse(ix, y0 + 8, 10, 3.4, 0, 0, TAU); inkFill(ctx, w_); }
}

// ——— A01 · Çankaya, gece, dış ———
// köşk: yerel koordinat, köken cephe tabanının ortası; y yukarı negatif
function a0_kosk(g, hx, hy, hs) {
  g.save(); g.translate(hx, hy); g.scale(hs, hs);
  const wall = PL([[-300, 0], [300, 0], [300, -280], [-300, -280]]);
  const tower = PL([[-110, -300], [110, -300], [110, -440], [-110, -440]]);
  const roof = PL(rough([[-336, -276], [336, -276], [214, -352], [-214, -352]], 1.2, 61));
  const troof = PL(rough([[-134, -436], [134, -436], [0, -500]], 1, 62));
  knock(g, tower); plate(g, 'red', tower, { a: .2 }); plate(g, 'navy', tower, { a: .45 }); inkStroke(g, tower, 3.2);
  knock(g, troof); plate(g, 'navy', troof, { n: 2 }); plate(g, 'ink', troof, { a: .35 }); inkStroke(g, troof, 3.2);
  for (let i = 1; i < 6; i++) inkStroke(g, PL([[-134 + i * 22, -436], [i * 2, -500 + i * 2]], false), 1.2, { a: .35 });
  for (const [cx, top] of [[-180, -400], [200, -404]]) { const ch = PL([[cx - 16, -330], [cx + 16, -330], [cx + 16, top], [cx - 16, top]]); knock(g, ch); plate(g, 'red', ch, { a: .2 }); plate(g, 'navy', ch, { a: .6 }); inkStroke(g, ch, 2.6); inkFill(g, PL([[cx - 22, top], [cx + 22, top], [cx + 22, top - 10], [cx - 22, top - 10]])); }
  knock(g, roof); plate(g, 'navy', roof, { n: 2 }); plate(g, 'ink', roof, { a: .3 }); inkStroke(g, roof, 3.6);
  for (let i = 0; i < 4; i++) { const yy = -290 - i * 16, k = (yy + 276) / -76; inkStroke(g, PL([[-336 + 122 * k, yy], [336 - 122 * k, yy]], false), 1.3, { a: .4 }); }
  // cephe: gece pembesi (kırmızı .2 + lacivert)
  knock(g, wall); plate(g, 'red', wall, { a: .2 }); plate(g, 'navy', wall, { a: .42 });
  plate(g, 'navy', PL([[-300, -280], [300, -280], [300, -258], [-300, -258]]), { a: .7 });
  for (let i = 1; i < 14; i++) inkStroke(g, PL([[-300, -i * 20], [300, -i * 20]], false), 1, { a: .12 });
  for (const sx of [-1, 1]) plate(g, 'navy', PL([[sx * 300, 0], [sx * 268, 0], [sx * 268, -280], [sx * 300, -280]]), { a: .35 }); // köşe taşları
  inkStroke(g, PL([[-306, -140], [306, -140]], false), 5);
  inkStroke(g, wall, 3.6);
  // pencereler: [x, yAlt, w, h, ışık 0 karanlık / 1 loş / 2 odak]
  const wins = [[-230, -20, 56, 92, 0], [-130, -20, 56, 92, 1], [130, -20, 56, 92, 2], [230, -20, 56, 92, 2],
    [-230, -164, 52, 86, 0], [-130, -164, 52, 86, 1], [0, -164, 52, 86, 0], [130, -164, 52, 86, 0], [230, -164, 52, 86, 1],
    [-60, -364, 34, 54, 0], [0, -364, 34, 54, 1], [60, -364, 34, 54, 0]];
  for (const [x, yb, w, h, L] of wins) {
    const pane = PL([[x - w / 2, yb], [x + w / 2, yb], [x + w / 2, yb - h], [x - w / 2, yb - h]]);
    knock(g, pane);
    if (L === 2) plate(g, 'gold', pane, { a: .3 });
    else if (L === 1) { plate(g, 'gold', pane, { a: .75 }); plate(g, 'ochre', pane, { a: .55 }); }
    else { plate(g, 'navy', pane, { n: 2 }); plate(g, 'ink', pane, { a: .25 }); }
    if (L === 2) plate(g, 'ochre', PL([[x - w / 2, yb - h], [x + w / 2, yb - h], [x + w / 2, yb - h + 14], [x - w / 2, yb - h + 14]]), { a: .5 }); // perde saçağı
    inkStroke(g, pane, 3); inkStroke(g, PL([[x, yb], [x, yb - h]], false), 2.4); inkStroke(g, PL([[x - w / 2, yb - h * .62], [x + w / 2, yb - h * .62]], false), 2.4);
    if (L === 0) for (const sx of [-1, 1]) { const sh = PL([[x + sx * w / 2, yb], [x + sx * (w / 2 + 16), yb], [x + sx * (w / 2 + 16), yb - h], [x + sx * w / 2, yb - h]]); plate(g, 'navy', sh, { n: 2 }); inkStroke(g, sh, 2); }
    inkFill(g, PL([[x - w / 2 - 8, yb], [x + w / 2 + 8, yb], [x + w / 2 + 8, yb + 6], [x - w / 2 - 8, yb + 6]]));
  }
  const door = PL([[-36, 0], [36, 0], [36, -108], [0, -124], [-36, -108]]);
  knock(g, door); plate(g, 'navy', door, { n: 2 }); plate(g, 'ochre', door, { a: .3 }); inkStroke(g, door, 3); inkStroke(g, PL([[0, 0], [0, -118]], false), 2);
  for (const cx of [-70, 70]) { const col = PL([[cx - 9, 0], [cx + 9, 0], [cx + 9, -132], [cx - 9, -132]]); knock(g, col); plate(g, 'navy', col, { a: .3 }); inkStroke(g, col, 2.6); }
  const bal = PL([[-96, -132], [96, -132], [96, -144], [-96, -144]]); knock(g, bal); plate(g, 'navy', bal, { a: .6 }); inkStroke(g, bal, 2.6);
  for (let i = 0; i <= 12; i++) inkStroke(g, PL([[-90 + i * 15, -144], [-90 + i * 15, -170]], false), 2);
  inkStroke(g, PL([[-96, -172], [96, -172]], false), 3.4);
  for (let i = 0; i < 3; i++) { const st = PL([[-60 - i * 10, i * 9], [60 + i * 10, i * 9], [60 + i * 10, i * 9 + 9], [-60 - i * 10, i * 9 + 9]]); knock(g, st); plate(g, 'navy', st, { a: .35 + i * .1 }); inkStroke(g, st, 2); }
  g.restore();
}
// kavak: ince alev biçimli is siluet + kazıma
function a0_poplar(g, x, yb, h, w, sd) {
  const r = rng(sd), L = [], R = [];
  for (let i = 0; i <= 10; i++) { const u = i / 10, yy = yb - h * u, ww = w * Math.sin(PI * Math.pow(1 - u, .8)) * (.85 + r() * .3) * (u < .08 ? .3 : 1); L.push([x - ww * .5, yy]); R.push([x + ww * .5, yy]); }
  const p = SP([...R, ...L.reverse()], true, .7); inkFill(g, p);
  for (let i = 0; i < 6; i++) { const yy = yb - h * (.2 + i * .12); cut(g, SP([[x - w * .18, yy], [x + w * .05, yy - 22], [x + w * .2, yy - 50]], false), 1.6, { a: .3 }); }
  inkStroke(g, PL([[x, yb + 4], [x, yb - h * .1]], false), 5);
}
function a0_shotKoskDis() {
  const t0 = 0; // film başı: A01 burada açılır
  const HX = 820, HY = 770, HS = 1.12, FOC = [HX + 180 * HS, HY - 66 * HS];
  shot(t0, (ctx, st) => {
    setReg(101);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d + .6, E.io2), z = 1 + .07 * p;
    const c = { x: 960 + 54 * p, y: 540 + 30 * p, z };
    // gök (paralaks .35): lacivert raster yukarıda yoğun, ufka doğru seyrek; uzak tepeler, Ankara kalesi ve şehir ışıkları
    const sky = a0_cache('a0-kosk-sky', g => {
      paperBG(g);
      plate(g, 'navy', PL([[-20, -20], [W + 20, -20], [W + 20, 820], [-20, 820]]), { a: .22 });
      radialHT(g, 'navy', 960, 820, 240, 900, .04, .52, { cell: 11, ang: 15, box: [-20, -20, W + 20, 820], sx: 2.2 });
      const hills = SP([[-40, 820], [-40, 690], [260, 664], [520, 686], [760, 654], [1080, 680], [1380, 650], [1640, 672], [1960, 654], [1960, 820]], true, .6);
      plate(g, 'navy', hills, { a: .6 }); inkStroke(g, SP([[-40, 690], [260, 664], [520, 686], [760, 654], [1080, 680], [1380, 650], [1640, 672], [1960, 654]], false, .6), 2.4, { a: .7 });
      const kale = PL([[1520, 658], [1520, 628], [1534, 628], [1534, 618], [1548, 618], [1548, 628], [1586, 628], [1586, 614], [1602, 614], [1602, 628], [1630, 628], [1630, 658]]);
      plate(g, 'navy', kale, { n: 2 }); inkStroke(g, kale, 1.6, { a: .6 });
      const r = rng(7);
      for (let i = 0; i < 30; i++) { const x = 1400 + r() * 400, y = 656 + r() * 30, d = new Path2D(); d.arc(x, y, 1.6 + r() * 1.4, 0, TAU); knock(g, d, '#F2D9A0'); plate(g, 'gold', d, { a: .6 }); }
    });
    a0_layer(ctx, sky, c, .35);
    // yıldızlar (kâğıt): küçükler sabit, büyükler 15 fps'te ışıldar
    ctx.save(); cam(ctx, c, .35);
    const tf = Math.floor(st.t * 15) / 15, r = rng(19);
    for (let i = 0; i < 80; i++) {
      const x = r() * W, y = r() * 560, big = i < 8, sz = big ? 7 + r() * 5 : 1.4 + r() * 2.2, ph = r() * TAU;
      if (x > 400 && x < 1260 && y > 170) continue; // köşkün arkası boş
      const k = big ? 1 + .32 * Math.sin(tf * 2.6 + ph) : 1, q = new Path2D();
      if (big) { const R = sz * k; q.moveTo(x, y - R); q.quadraticCurveTo(x, y, x + R * .9, y); q.quadraticCurveTo(x, y, x, y + R); q.quadraticCurveTo(x, y, x - R * .9, y); q.quadraticCurveTo(x, y, x, y - R); }
      else q.arc(x, y, sz, 0, TAU);
      knock(ctx, q, '#F3EBD8');
    }
    ctx.restore();
    // köşk + kavaklar + tepe (paralaks 1)
    const house = a0_cache('a0-kosk-house', g => {
      const ground = SP([[-40, 1120], [-40, 800], [300, 780], [600, 772], [1200, 772], [1500, 784], [1960, 800], [1960, 1120]], true, .5);
      plate(g, 'navy', ground, { a: .7 }); plate(g, 'ink', ground, { a: .2 });
      inkStroke(g, SP([[-40, 800], [300, 780], [600, 772], [1200, 772], [1500, 784], [1960, 800]], false, .5), 3);
      for (const [x, h, w, sd] of [[372, 470, 78, 3], [456, 390, 62, 4], [1280, 500, 84, 5], [1376, 420, 68, 6], [1466, 350, 58, 7], [1800, 300, 54, 8]]) a0_poplar(g, x, 782, h, w, sd);
      a0_kosk(g, HX, HY, HS);
      // cephe dibinde çalılar (is siluet) ve çimende kısa kazımalar
      const rb = rng(23);
      for (const [x0, x1] of [[HX - 330 * HS, HX - 90 * HS], [HX + 90 * HS, HX + 330 * HS]]) {
        const pts = [[x0, HY + 14]];
        for (let x = x0; x <= x1; x += 26) pts.push([x, HY - 18 - rb() * 26]);
        pts.push([x1, HY + 14]);
        const bush = SP(pts, true, .9); inkFill(g, bush); plate(g, 'navy', bush, { a: .4 });
        for (let x = x0 + 14; x < x1; x += 30) { const q = new Path2D(); q.arc(x, HY - 6 - rb() * 10, 6, PI * 1.1, PI * 1.9); cut(g, q, 1.6, { a: .3 }); }
      }
      for (let i = 0; i < 60; i++) { const x = rb() * W, y = 800 + rb() * 180; if (Math.abs(x - HX) < 140) continue; inkStroke(g, PL([[x, y], [x + 3, y - 9]], false), 1.4, { a: .3 }); }
      // yol: kapıdan aşağı, loş
      const path = SP([[HX - 34, HY + 34], [HX + 34, HY + 34], [HX + 110, H + 30], [HX - 110, H + 30]], true, .4);
      knock(g, path, P.paperD); plate(g, 'navy', path, { a: .5 });
      inkStroke(g, SP([[HX - 34, HY + 34], [HX - 110, H + 30]], false), 2.4); inkStroke(g, SP([[HX + 34, HY + 34], [HX + 110, H + 30]], false), 2.4);
    });
    a0_layer(ctx, house, c, 1);
    // ön plan: alçak bahçe duvarı (paralaks 1.15)
    const fg = a0_cache('a0-kosk-fg', g => {
      const wl = PL(rough([[-40, 1000], [HX - 130, 990], [HX - 130, 1120], [-40, 1120]], 1.5, 9));
      const wr = PL(rough([[HX + 130, 990], [1960, 1000], [1960, 1120], [HX + 130, 1120]], 1.5, 10));
      for (const w_ of [wl, wr]) { knock(g, w_, P.paperD); plate(g, 'navy', w_, { n: 2 }); plate(g, 'ink', w_, { a: .3 }); inkStroke(g, w_, 3.2); }
      for (let x = -20; x < W; x += 70) if (Math.abs(x - HX) > 150) inkStroke(g, PL([[x, 1004], [x + 6, 1090]], false), 1.6, { a: .45 });
      for (const px of [HX - 146, HX + 130]) { const pl = PL([[px, 960], [px + 16, 960], [px + 16, 1120], [px, 1120]]); knock(g, pl); plate(g, 'navy', pl, { n: 2 }); inkStroke(g, pl, 2.8); inkFill(g, PL([[px - 6, 950], [px + 22, 950], [px + 22, 962], [px - 6, 962]])); }
    });
    a0_layer(ctx, fg, c, 1.15);
    stamp(ctx, 'ANKARA · 28 EKİM 1923 · GECE', 86, 118, st.t - a0_W('A01', 'ankara'), 4.6);
  }, { post: { vig: 1 } });
}

// ——— A01 sonu / A02 · Sofra (geniş) ———
// konuklar: [x, göz y, ölçek, başlık, tohum, eğim, {mus, glasses}]
const A0_GUESTS = [[206, 606, 1.24, 'kalpak', 41, .03, { mus: 1 }], [462, 616, 1.18, 'bare', 42, -.04, { glasses: 1 }], [722, 602, 1.26, 'kalpak', 43, .0, { mus: 1 }], [978, 614, 1.2, 'bald', 44, -.03, { mus: 1 }], [1230, 606, 1.22, 'fes', 45, .04, {}]];
function a0_cloth(ctx, x0, x1, yt, yf, yh, sd) {
  const top = PL([[x0 + 16, yt], [x1 - 16, yt], [x1, yf], [x0, yf]]);
  knock(ctx, top); inkStroke(ctx, top, 3);
  const hem = [[x0, yf]]; const r = rng(sd);
  for (let x = x0; x <= x1; x += 46) hem.push([x, yh + (r() - .5) * 6 + ((x / 46) % 2 ? 7 : 0)]);
  hem.push([x1, yh]); hem.push([x1, yf]);
  const front = SP(hem, true, .4);
  knock(ctx, front); plate(ctx, 'ochre', front, { a: .22 });
  for (let x = x0 + 40; x < x1; x += 92) plate(ctx, 'ochre', PL([[x, yf + 4], [x + 18, yf + 4], [x + 26, yh], [x + 2, yh]]), { a: .22 });
  inkStroke(ctx, front, 3);
  inkStroke(ctx, PL([[x0 + 6, yf + 10], [x1 - 6, yf + 10]], false), 1.3, { a: .35 });
}
function a0_shotSofra() {
  const MK = { x: 1580, y: 452, s: 1.32 }, TY = 776;
  shot(a0_W('A01', 'küçük') - .3, (ctx, st) => {
    setReg(113);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d + .4, E.io2), c = { x: 960 + 34 * p, y: 540 - 16 * p, z: 1 + .045 * p };
    const L0 = [1330, 170];
    const bg = a0_cache('a0-sofra-bg', g => {
      paperBG(g);
      plate(g, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .38 });
      // tavan köşeleri lambadan uzakta koyulaşır (düz ikinci baskı, başlardan uzak)
      plate(g, 'ochre', PL([[-20, -20], [760, -20], [520, 150], [-20, 300]]), { a: .3 });
      plate(g, 'sepia', PL([[-20, -20], [380, -20], [-20, 170]]), { a: .25 });
      plate(g, 'ochre', PL([[W + 20, -20], [1760, -20], [W + 20, 170]]), { a: .3 });
      // tavan silmesi
      const cor = PL([[-20, -20], [W + 20, -20], [W + 20, 40], [-20, 44]]); plate(g, 'ochre', cor, { n: 2 }); plate(g, 'sepia', cor, { a: .4 }); inkStroke(g, PL([[-20, 44], [W + 20, 40]], false), 3.4);
      for (const [rr, a] of [[180, .16], [110, .3]]) { const q = new Path2D(); q.ellipse(L0[0], L0[1] + 10, rr * 1.2, rr * .8, 0, 0, TAU); plate(g, 'gold', q, { a }); }
      // pencere (gece) solda, düz perdeler
      const wx0 = 110, wx1 = 300, wy0 = 214, wy1 = 560, win = PL([[wx0, wy0], [wx1, wy0], [wx1, wy1], [wx0, wy1]]);
      knock(g, win); plate(g, 'navy', win, { a: .8 }); halftone(g, 'navy', win, .3, { cell: 10 });
      for (const [sx, sy] of [[160, 260], [262, 300], [200, 380], [280, 460]]) { const q = new Path2D(); q.arc(sx, sy, 2.4, 0, TAU); knock(g, q, '#F3EBD8'); }
      const fr = new Path2D(); fr.rect(wx0 - 16, wy0 - 16, wx1 - wx0 + 32, 16); fr.rect(wx0 - 16, wy1, wx1 - wx0 + 32, 20); fr.rect(wx0 - 16, wy0, 16, wy1 - wy0); fr.rect(wx1, wy0, 16, wy1 - wy0); fr.rect((wx0 + wx1) / 2 - 6, wy0, 12, wy1 - wy0); fr.rect(wx0, 370, wx1 - wx0, 10);
      knock(g, fr); plate(g, 'ochre', fr, { n: 2 }); inkStroke(g, fr, 2.6);
      inkStroke(g, PL([[40, 172], [380, 172]], false), 6);
      for (const [cx0, cx1] of [[46, 126], [284, 364]]) { const cur = PL(rough([[cx0, 174], [cx1, 174], [cx1 + 6, 660], [cx0 - 4, 660]], 1, cx0)); knock(g, cur); plate(g, 'ochre', cur, { n: 2 }); plate(g, 'sepia', cur, { a: .35 }); inkStroke(g, cur, 2.6); for (let k = 1; k < 4; k++) inkStroke(g, PL([[cx0 + k * (cx1 - cx0) / 4, 180], [cx0 + k * (cx1 - cx0) / 4 + 2, 656]], false), 1.4, { a: .5 }); }
      // duvarda Osmanlıca levha (soyut yazı izi)
      const lv = PL([[560, 270], [860, 270], [860, 386], [560, 386]]); plate(g, 'ink', PL([[568, 280], [868, 280], [868, 396], [568, 396]]), { a: .3 });
      knock(g, lv, P.paperD); plate(g, 'ochre', lv, { a: .2 }); inkStroke(g, lv, 3.6); inkStroke(g, PL([[574, 284], [846, 284], [846, 372], [574, 372]]), 1.2);
      scriptLine(g, 830, 340, 240, 22, 501, { w: 3.2 }); scriptLine(g, 780, 362, 140, 8, 502, { w: 1.4, a: .7 });
      // lambri ve zemin
      plate(g, 'ochre', PL([[-20, 690], [W + 20, 690], [W + 20, TY + 20], [-20, TY + 20]]), { a: .45 });
      inkStroke(g, PL([[-20, 690], [W + 20, 690]], false), 2.6);
      const fl = PL([[-20, 914], [W + 20, 914], [W + 20, H + 20], [-20, H + 20]]); plate(g, 'ochre', fl, { n: 2 }); plate(g, 'ink', fl, { a: .35 });
      for (let i = 0; i < 6; i++) inkStroke(g, PL([[-20, 940 + i * 28], [W + 20, 936 + i * 28]], false), 1.4, { a: .4 });
      gasLamp(g, L0[0], L0[1], 1.05, 0);
    });
    a0_layer(ctx, bg, c, .7);
    ctx.save(); cam(ctx, c, 1);
    const tf = Math.floor(st.t * 15) / 15;
    // konuklar: anonim profil siluetler, sofranın başına (sağa) dönük
    A0_GUESTS.forEach(([x, y, s, kind, sd, tl, o]) => {
      const io = idleOffsets(tf, sd, 1.4);
      a0_prof(ctx, x, y + io.breath * .8, s, 1, kind, { ...o, tilt: tl + io.head * .6, seed: sd });
    });
    // Mustafa Kemal: masanın başında ayakta, sivil koyu ceket, başı açık
    a0_fig(ctx, { ...MK, dir: -1, who: 'mk', age: 42, gear: null, coat: 'civil', col: 'ink', w: .96, len: (TY + 30 - MK.y) / MK.s, lookAt: [820, 640], tilt: .02, seed: 3, arms: 'back', turn: .3 }, st.t);
    // sofra: beyaz örtü (kâğıt), çay bardakları, demlik, şekerlik; kadeh yok
    a0_cloth(ctx, 30, 1890, TY - 6, TY + 22, 914, 5);
    A0_GUESTS.forEach(([x], i) => a0_tea(ctx, x + 84 + (i % 2) * 14, TY + 10, 1.45));
    a0_tea(ctx, MK.x - 170, TY + 10, 1.45, { empty: true });
    const tp = SP([[598, TY + 10], [582, TY - 14], [586, TY - 40], [606, TY - 52], [648, TY - 52], [668, TY - 40], [672, TY - 14], [656, TY + 10]], true, .7);
    knock(ctx, tp); plate(ctx, 'ochre', tp, { a: .6 }); plate(ctx, 'gold', tp, { a: .4 }); inkStroke(ctx, tp, 2.6);
    inkStroke(ctx, SP([[672, TY - 24], [702, TY - 42], [710, TY - 58]], false), 4); inkStroke(ctx, SP([[586, TY - 34], [568, TY - 22], [584, TY - 2]], false), 3);
    inkFill(ctx, PL([[616, TY - 52], [638, TY - 52], [634, TY - 64], [620, TY - 64]]));
    const sb = SP([[856, TY + 10], [850, TY - 14], [892, TY - 14], [886, TY + 10]], true, .6); knock(ctx, sb); plate(ctx, 'ochre', sb, { a: .3 }); inkStroke(ctx, sb, 2.2);
    ctx.restore();
  }, { tr: { type: 'press', dur: .7 }, post: { vig: 1 } });
}

// ——— A02 · Mustafa Kemal ¾ yakın + söz ———
function a0_shotMK() {
  const MK = { x: 1330, y: 470, s: 2.5 };
  shot(S('A02') - .14, (ctx, st) => {
    setReg(127);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d + .5, E.io2), c = { x: 960 + 40 * p, y: 540 - 20 * p, z: 1 + .06 * p };
    const L0 = [430, 96];
    const bg = a0_cache('a0-mk-bg', g => {
      paperBG(g);
      plate(g, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .42 });
      for (const [rr, a] of [[180, .15], [112, .3]]) { const q = new Path2D(); q.ellipse(L0[0], L0[1] + 10, rr * 1.2, rr * .8, 0, 0, TAU); plate(g, 'gold', q, { a }); }
      // perdenin duvara düşen gölgesi (düz ikinci baskı) ve sol alt köşe gölgesi
      plate(g, 'ochre', PL([[1640, -20], [W + 20, -20], [W + 20, H + 20], [1700, H + 20]]), { a: .4 });
      // duvarda resim çerçevesinin kenarı (solda üstte)
      const pf = PL([[700, 120], [1010, 120], [1010, 330], [700, 330]]); plate(g, 'ink', PL([[710, 132], [1020, 132], [1020, 342], [710, 342]]), { a: .3 });
      knock(g, pf, P.paperD); plate(g, 'ochre', pf, { a: .25 }); inkStroke(g, pf, 4); inkStroke(g, PL([[716, 136], [994, 136], [994, 314], [716, 314]]), 1.4);
      scriptLine(g, 960, 226, 200, 26, 511, { w: 3.6 }); scriptLine(g, 900, 262, 100, 9, 512, { w: 1.6, a: .7 });
      const cur = SP([[1790, -20], [1960, -20], [1960, H + 20], [1810, H + 20], [1780, 600]], true, .5);
      knock(g, cur); plate(g, 'ochre', cur, { n: 2 }); plate(g, 'sepia', cur, { a: .4 }); inkStroke(g, cur, 3);
      for (let k = 0; k < 4; k++) inkStroke(g, SP([[1820 + k * 34, -20], [1810 + k * 36, 600], [1830 + k * 34, H + 20]], false), 1.6, { a: .5 });
      gasLamp(g, L0[0], L0[1], 1.15, 0);
    });
    a0_layer(ctx, bg, c, .6);
    ctx.save(); cam(ctx, c, 1);
    // "yarın" kelimesinde baş hafifçe kalkar, bakış masadan ileriye döner
    const tq = a0_W('A02', 'yarın') - (st.t - st.lt), u = ramp(st.lt, tq - .25, tq + .45, E.out3);
    const tilt = lerp(.04, -.005, u) + settle(st.lt, tq + .45, .008, 2, 4);
    const look = [lerp(260, 80, u), lerp(660, 470, u)];
    a0_fig(ctx, { ...MK, dir: -1, who: 'mk', age: 42, gear: null, coat: 'civil', col: 'ink', w: .98, len: (1100 - MK.y) / MK.s, lookAt: look, tilt, seed: 3, turn: .25, idle: .8 }, st.t);
    ctx.restore();
    // ön plan: konuk silueti, masa köşesi, çay bardakları (paralaks 1.2)
    ctx.save(); cam(ctx, c, 1.2);
    const tf = Math.floor(st.t * 15) / 15, io = idleOffsets(tf, 41, 1.2);
    a0_prof(ctx, 140, 650 + io.breath, 2.0, 1, 'kalpak', { tilt: -.03 + io.head * .5, seed: 41, mus: 1 });
    a0_cloth(ctx, -40, 1060, 934, 968, 1180, 7);
    a0_tea(ctx, 520, 962, 2.6); a0_tea(ctx, 840, 960, 2.6, { empty: true });
    ctx.restore();
    nameTag(ctx, 1860, 850, 'MUSTAFA KEMAL', '42 yaşında', st.t - a0_W('A02', 'mustafa'), 3.4, { align: 'right', size: 56, sub: 36 });
    quote(ctx, 'Yarın Cumhuriyet ilan edeceğiz!', 680, 480, st.t - a0_W('A02', 'yarın') + .1, 3.6, { cite: '— Nutuk, 1927', maxW: 760, size: 70 });
  }, { tr: { type: 'cut' }, post: { vig: 1 } });
}

// ——— A04 · Kuşak şeridi: 1923 kadrosu → 1893 mektep sırası → II. Abdülhamid ———
const A0_XS = [260, 610, 960, 1310, 1660];
// sofradakiler (1923): ortada Mustafa Kemal; yaşlar 42, 39, 39, 43, 40 (basılma sırası: orta, sol, sol, sağ, sağ)
const A0_K23 = [
  { who: 'anon', id: { mus: 'mk', jaw: 1.06, WD: 1.1, seed: 31 }, gear: 'kalpak', gearCol: 'grey', coat: 'kaput', col: 'khaki', age: 39, seed: 31 },
  { who: 'ismet', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 39, seed: 5 },
  { who: 'mk', gear: null, coat: 'civil', col: 'ink', age: 42, seed: 3 },
  { who: 'anon', id: { mus: 'thin', hair: 'ink', jaw: 1.0, WD: 1.04, brow: .1, seed: 33 }, gear: null, coat: 'civil', col: 'navy', age: 43, seed: 33 },
  { who: 'anon', id: { mus: 'gur', jaw: 1.1, WD: 1.12, brow: -.06, seed: 35 }, gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 40, seed: 35 },
];
const A0_AGE23 = [39, 39, 42, 43, 40], A0_ORD = [2, 1, 0, 3, 4];
// otuz yıl önce: aynı sıra, fesli çocuklar (setre, lacivert)
const A0_K93 = [
  { who: 'anon', id: { mus: null, jaw: 1.0, WD: 1.08, seed: 31 } },
  { who: 'ismet', id: { mus: null } },
  { who: 'mk', id: { mus: null } },
  { who: 'anon', id: { mus: null, hair: 'sepia', jaw: 1.02, WD: 1.04, brow: .1, seed: 33 } },
  { who: 'anon', id: { mus: null, jaw: 1.04, WD: 1.12, seed: 35 } },
];
const A0_AGE93 = [9, 9, 12, 13, 10];
// mektep sırası şeridi (act6 G03 de kullanır): tahta + çocuklar + sıra
function a0_classBG(g, B0, B1) {
  paperBG(g);
  a0_band(g, B0, B1, 'ochre', .35);
  g.save(); g.beginPath(); g.rect(-20, B0 + 2, W + 40, B1 - B0 - 4); g.clip();
  a0_board(g, 120, 196, 1800, 560, 21);
  a0_chalkGeo(g, [['tri', 440, 262, .72], ['circ', 790, 256, .62], ['ang', 1100, 300, .75], ['arc', 1470, 222, .7], ['circ', 230, 262, .55], ['tri', 1690, 262, .6]]);
  g.restore();
  inkStroke(g, PL([[-20, B0], [W + 20, B0]], false), 4); inkStroke(g, PL([[-20, B1], [W + 20, B1]], false), 4);
}
function a0_classKids(ctx, t, B0, B1, o = {}) {
  ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
  A0_K93.forEach((f, i) => a0_fig(ctx, { ...f, x: A0_XS[i], y: o.y ?? 446, s: 1.2, dir: -1, w: .86, len: (B1 - 446) / 1.2 + 10, age: 12, gear: 'fes', coat: 'setre', col: 'navy', look: [.2, .25], sep: true, seed: (A0_K23[i].seed || 1) + 50 }, t));
  a0_desk(ctx, -30, W + 30, 652, B1, 77, { books: [[372, 70, 14, 'sepia'], [1102, 60, 12, 'navy'], [1452, 76, 16, 'khaki']], ink: [470, 820, 1170, 1520] });
  ctx.restore();
}
function a0_shotStrips() {
  const B0 = 150, B1 = 740;
  // 1923 şeridi
  shot(S('A04') - .4, (ctx, st) => {
    setReg(131);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d + .3, E.io2), c = { x: 944 + 32 * p, y: 540, z: 1.02 + .02 * p };
    const bg = a0_cache('a0-k23-bg', g => { paperBG(g); a0_band(g, B0, B1, 'ochre', .55); });
    a0_layer(ctx, bg, c, .8);
    ctx.save(); cam(ctx, c, 1);
    ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
    A0_K23.forEach((f, i) => a0_fig(ctx, { ...f, x: A0_XS[i], y: 412, s: 1.32, dir: -1, w: .98, len: (B1 - 412) / 1.32 + 10, look: [.2, .25], sep: true }, st.t));
    ctx.restore();
    ctx.restore();
    const tk = a0_W('A04', 'kırk');
    A0_ORD.forEach((i, k) => a0_age(ctx, A0_XS[i], 862, A0_AGE23[i], 'yaşında', st.t - tk - k * .17));
    label(ctx, '1923', W / 2, 108, FONT.title(78), { align: 'center', ls: 4 });
  }, { tr: { type: 'press', dur: .6 }, post: { vig: .9 } });
  // 1893 mektep sırası (sınıf fotoğrafı eşleşmesi: aynı sıra, aynı konumlar)
  shot(a0_W('A04', 'otuz') - .35, (ctx, st) => {
    setReg(137);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d + .3, E.io2), c = { x: 976 - 30 * p, y: 540 - 8 * p, z: 1.02 + .03 * p };
    const bg = a0_cache('a0-k93-bg', g => a0_classBG(g, B0, B1));
    a0_layer(ctx, bg, c, .8);
    ctx.save(); cam(ctx, c, 1); a0_classKids(ctx, st.t, B0, B1); ctx.restore();
    const tk = a0_W('A04', 'önce') + .05;
    A0_ORD.forEach((i, k) => a0_age(ctx, A0_XS[i], 862, A0_AGE93[i], 'yaşında', st.t - tk - k * .15));
    label(ctx, '1893', W / 2, 108, FONT.title(78), { align: 'center', ls: 4 });
  }, { tr: { type: 'press', dur: .8 }, post: { vig: .9 } });
}
// sınıf duvarında II. Abdülhamid portresi; ışık nötr
function a0_shotPortrait() {
  const FX = 960, FY = 452;
  shot(a0_W('A04', 'ikinci') - .12, (ctx, st) => {
    setReg(139);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d + .4, E.io2), c = { x: 960, y: 540 - 22 * p, z: 1 + .05 * p };
    const bg = a0_cache('a0-portre-bg', g => {
      paperBG(g);
      plate(g, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .32 });
      // duvar: durağan zemin rasteri (portre başının 1,5 yarıçapı çerçevenin içinde kalır; orada raster yok)
      halftone(g, 'sepia', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), .1, { cell: 12, ang: 45 });
      a0_board(g, -60, 940, W + 60, 1200, 23);
      inkStroke(g, PL([[FX - 200, FY - 300], [FX, FY - 400], [FX + 200, FY - 300]], false), 2.4);
      const nail = new Path2D(); nail.arc(FX, FY - 402, 6, 0, TAU); inkFill(g, nail);
      // çerçeve: sade ahşap + ince yaldız; süs yok
      const o = [FX - 290, FY - 340, FX + 290, FY + 350], i_ = [FX - 236, FY - 286, FX + 236, FY + 296];
      plate(g, 'ink', PL([[o[0] + 14, o[1] + 16], [o[2] + 14, o[1] + 16], [o[2] + 14, o[3] + 16], [o[0] + 14, o[3] + 16]]), { a: .35 });
      const fr = PL([[o[0], o[1]], [o[2], o[1]], [o[2], o[3]], [o[0], o[3]]]);
      knock(g, fr); plate(g, 'ochre', fr, { n: 2 }); plate(g, 'sepia', fr, { a: .45 }); inkStroke(g, fr, 4);
      const gl = PL([[i_[0] - 12, i_[1] - 12], [i_[2] + 12, i_[1] - 12], [i_[2] + 12, i_[3] + 12], [i_[0] - 12, i_[3] + 12]]);
      inkStroke(g, gl, 6, { col: P.gold, mode: 'multiply' }); inkStroke(g, gl, 1.4);
      for (const [a, b] of [[[o[0], o[1]], [i_[0] - 12, i_[1] - 12]], [[o[2], o[1]], [i_[2] + 12, i_[1] - 12]], [[o[0], o[3]], [i_[0] - 12, i_[3] + 12]], [[o[2], o[3]], [i_[2] + 12, i_[3] + 12]]]) inkStroke(g, PL([a, b], false), 2);
      const cv = PL([[i_[0], i_[1]], [i_[2], i_[1]], [i_[2], i_[3]], [i_[0], i_[3]]]);
      knock(g, cv, P.paperD); plate(g, 'sepia', cv, { a: .18 }); inkStroke(g, cv, 2.4);
      g.save(); g.clip(cv);
      bust(g, { x: FX + 10, y: FY - 30, s: 2.05, dir: -1, coat: 'setre', col: 'ink', w: .98, seed: 21, len: 230 });
      head3q(g, { x: FX + 10, y: FY - 30, s: 2.05, dir: -1, who: 'abdulhamid', gear: 'fes', gearCol: 'ink', light: 'front', look: [-.2, .2], age: 51 });
      g.restore();
    });
    a0_layer(ctx, bg, c, 1);
    nameTag(ctx, FX + 330, FY + 120, 'II. ABDÜLHAMİD', '1876–1909', st.t - a0_W('A04', 'ikinci') - .25, 9, { size: 54, sub: 34 });
  }, { tr: { type: 'cut' }, post: { vig: .9 } });
}

// ——— A05 · Başlık kartı: "BİR KUŞAĞIN HİKÂYESİ" ———
// yedi büst (1923): Halide Edib, Karabekir, Ali Fuat, Mustafa Kemal, İsmet, Fevzi, Rauf
const A0_SEVEN = [
  { who: 'halide', gear: 'carsaf', coat: 'plain', col: 'ink', age: 39, seed: 19 },
  { who: 'karabekir', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 41, seed: 11 },
  { who: 'alifuat', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 41, seed: 13 },
  { who: 'mk', gear: null, coat: 'civil', col: 'ink', age: 42, seed: 3 },
  { who: 'ismet', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 39, seed: 5 },
  { who: 'fevzi', gear: 'kalpak', gearCol: 'grey', coat: 'kaput', col: 'khaki', age: 47, seed: 7 },
  { who: 'rauf', gear: null, coat: 'civil', col: 'navy', age: 42, seed: 15 },
];
const A0_X7 = [216, 464, 712, 960, 1208, 1456, 1704];
// yedi büstlük kuşak şeridi; app[i] = belirme zamanı (yerel)
function a0_seven(ctx, t, lt, app, o = {}) {
  const y = o.y ?? 400, s = o.s ?? 1.12, yb = o.yb ?? 700;
  A0_SEVEN.forEach((f, i) => {
    const h = a0_hit(lt, app[i], .14); if (h.a <= 0) return;
    const x = (o.xs || A0_X7)[i];
    ctx.save(); ctx.globalAlpha = h.a; ctx.translate(x, yb); ctx.scale(h.k, h.k); ctx.translate(-x, -yb);
    const rb = REG.boost; REG.boost = rb * (1 + 5 * (1 - E.out3(clamp((lt - app[i]) / .35))));
    a0_fig(ctx, { ...f, x, y, s, dir: o.dir || -1, w: .96, len: (yb - y) / s + 10, look: o.look || [.3, .25], sep: true, idle: .8, ...(o.over ? o.over(i) : {}) }, t);
    REG.boost = rb;
    ctx.restore();
  });
}
function a0_shotTitle() {
  const B0 = 196, B1 = 696;
  shot(S('A05') - .45, (ctx, st) => {
    setReg(149);
    paperBG(ctx);
    const tb = a0_W('A05', 'bir', 1) - (st.t - st.lt); // "bir kuşağın" (yerel)
    const p = ramp(st.lt, tb - .3, tb + 1.6, E.io2), c = { x: 960, y: 520 + 20 * p, z: 1.06 - .06 * p };
    const bg = a0_cache('a0-title-bg', g => { paperBG(g); a0_band(g, B0, B1, 'ochre', .5); });
    a0_layer(ctx, bg, c, .85);
    ctx.save(); cam(ctx, c, 1);
    ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
    const app = [tb + .34, tb + .17, tb, -9, tb, tb + .17, tb + .34];
    a0_seven(ctx, st.t, st.lt, app, { y: 412, s: 1.14, yb: B1 });
    ctx.restore();
    ctx.restore();
    if (!NOTEXT) {
      const tk = a0_W('A05', 'kuşağın') - (st.t - st.lt), h = a0_hit(st.lt, tk, .2);
      if (h.a > 0) {
        ctx.save(); ctx.globalAlpha = h.a; ctx.translate(960, 850); ctx.scale(h.k, h.k);
        txt(ctx, 'BİR KUŞAĞIN HİKÂYESİ', 0, 0, FONT.title(118), { align: 'center', ls: 3 });
        ctx.restore();
        const rl = 640 * E.out3(ramp(st.lt, tk + .15, tk + .7));
        plate(ctx, 'red', PL([[960 - rl, 882], [960 + rl, 882], [960 + rl, 891], [960 - rl, 891]]));
      }
      const ts = a0_W('A05', 'hikayesi', 0, true) - (st.t - st.lt) + .1;
      label(ctx, 'Cumhuriyet’i kuranlar nasıl yetişti?', 960, 966, FONT.quote(50), { align: 'center', a: ramp(st.lt, ts, ts + .5) });
    }
  }, { tr: { type: 'press', dur: .7 }, post: { vig: .9 } });
}

a0_shotKoskDis();
a0_shotSofra();
a0_shotMK();
a0_shotStrips();
a0_shotPortrait();
a0_shotTitle();
