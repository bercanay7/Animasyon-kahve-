// act2: II · Selanik ve yasak kitaplar (C01–C06). Sahibi: II. bölüm sahne yapımcısı.
// Kalıplar: kâğıt + is + turkuaz (deniz) + lacivert (gece) + sepya/okra; kırmızı yalnız fes vurgusu.
// Yerel yardımcılar a2_ önekiyle; ortak ilkellere dokunulmaz.
'use strict';

// ——————————————————————————————————————————— genel ———
const a2_q = t => Math.floor(t * 15) / 15;                       // figür poz zamanı (ikişer kare)
const a2_R = (x0, y0, x1, y1) => PL([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]);
// kenar paylı durağan katman (kamera kayması için); kayık baskı çekimin setReg'ine sabitlenir, baskı geçişinin artışı karışmaz
function a2_cache(key, m, draw) {
  const c = layerCache('a2-' + key, g => { const b = REG.boost; REG.boost = 1; g.translate(m, m); draw(g); REG.boost = b; }, W + 2 * m, H + 2 * m);
  return { c, m };
}
function a2_blit(ctx, L, cm, k = 1) {
  ctx.save(); if (cm) cam(ctx, cm, k); ctx.drawImage(L.c, -L.m, -L.m, W + 2 * L.m, H + 2 * L.m); ctx.restore();
}
const a2_camAt = (lt, d, a, b, e = E.sine) => mix(a, b, e(clamp(lt / d)));
function a2_ell(cx, cy, rx, ry, rot = 0) { const p = new Path2D(); p.ellipse(cx, cy, rx, ry, rot, 0, TAU); return p; }
// çekim: açık bitişle (süre komşu bölümün yazılıp yazılmadığına bağlı kalmasın; kamera ve zarflar bu süreye göre)
function a2_shot(at, end, draw, o) { shot(at, (ctx, st) => draw(ctx, { ...st, d: end - at, p: clamp((st.t - at) / (end - at)) }), o); }
// kelimeye bağlı belirme: [a, a+dur] arasında 0→1
const a2_in = (t, at, dur = .35) => E.out3(clamp((t - at) / dur));

// ——— yazı izleri (sahne içi) ———
// İbrani harfli Ladino gazetesi/tabelası için soyut kare harf izi (okunur değildir; sağdan sola)
function a2_squareTrace(ctx, x1, y, len, h, seed, o = {}) {
  const r = rng(seed), p = new Path2D(); let x = x1;
  while (x > x1 - len) {
    const w = h * (.55 + r() * .35), k = Math.floor(r() * 6);
    if (k === 0) { p.moveTo(x - w, y - h); p.lineTo(x, y - h); p.lineTo(x, y); }                       // ד
    else if (k === 1) { p.moveTo(x - w, y - h); p.lineTo(x, y - h); p.lineTo(x, y); p.lineTo(x - w, y); } // ב
    else if (k === 2) { p.moveTo(x - w, y - h); p.lineTo(x, y - h); p.lineTo(x, y); p.moveTo(x - w, y - h * .45); p.lineTo(x - w, y); } // ה
    else if (k === 3) { p.moveTo(x - w * .2, y - h * 1.35); p.lineTo(x - w * .2, y - h); p.lineTo(x, y - h * .6); p.lineTo(x - w, y); } // ל
    else if (k === 4) { p.moveTo(x - w * .5, y - h); p.lineTo(x - w * .5, y); }                       // ו
    else { p.moveTo(x - w, y - h); p.lineTo(x - w, y); p.lineTo(x, y); p.moveTo(x - w * .4, y - h); p.lineTo(x, y - h * .7); } // מ benzeri
    x -= w + h * (r() < .22 ? .75 : .28);
  }
  inkStroke(ctx, p, o.w || Math.max(1.6, h * .2), { col: o.col, a: o.a, cap: 'square' });
}
// tabela: zemin + çerçeve + yazı (Fransızca/Rumca gerçek harf; Türkçe ve Ladino soyut iz)
function a2_sign(g, x, y, w, h, o = {}) {
  const box = PL(rough([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], .8, (o.seed || 1) + 300));
  knock(g, box, o.bg || P.paper);
  if (o.plate) plate(g, o.plate, box, { a: o.pa ?? 1, n: o.pn || 1 });
  if (o.dark) inkFill(g, box);
  inkStroke(g, box, o.lw || 3);
  inkStroke(g, a2_R(x + 6, y + 6, x + w - 6, y + h - 6), 1.2, { a: o.dark ? 0 : .7 });
  const col = o.dark ? P.paper : P.ink;
  if (o.text) txt(g, o.text, x + w / 2, y + h / 2 + 2, o.font || FONT.title(Math.round(h * .55)), { align: 'center', base: 'middle', ls: o.ls ?? 2, col });
  else if (o.trace === 'osm') scriptLine(g, x + w - 14, y + h * .62, w - 28, h * .32, o.seed || 9, { col, w: Math.max(2, h * .07) });
  else if (o.trace === 'heb') a2_squareTrace(g, x + w - 14, y + h * .7, w - 28, h * .38, o.seed || 9, { col, w: Math.max(2, h * .07) });
}
const a2_GREEK = s => `700 ${s}px "Liberation Serif", "FreeSerif", serif`;

// ——————————————————————————————————————— deniz ———
// durağan deniz zemini: turkuaz kalıp, ufukta ve önde ikinci baskı, uzakta durağan yarım ton
function a2_seaBase(g, y0, y1, o = {}) {
  const x0 = o.x0 ?? -160, x1 = o.x1 ?? W + 160, sea = a2_R(x0, y0, x1, y1);
  knock(g, sea); plate(g, 'teal', sea, { a: o.a ?? .78 });
  plate(g, 'teal', a2_R(x0, y0, x1, y0 + (y1 - y0) * .1), { a: .5 });
  plate(g, 'teal', a2_R(x0, y1 - (y1 - y0) * .32, x1, y1), { a: .4 });
  if (o.ht !== false) halftone(g, 'teal', a2_R(x0, y0 + (y1 - y0) * .1, x1, y0 + (y1 - y0) * .45), .2, { cell: 11, ang: 15 });
  inkStroke(g, PL([[x0, y0], [x1, y0]], false), 2.6);
}
// hareketli dalga: yavaş kayan düz şeritler (açık: kâğıt, koyu: turkuazın ikinci baskısı). Yarım ton değil.
function a2_waves(ctx, y0, y1, t, o = {}) {
  const r = rng(o.seed || 7), n = o.rows || 15, x0 = (o.x0 ?? -200), x1 = (o.x1 ?? W + 200), sp = o.speed ?? 1;
  const light = new Path2D(), dark = new Path2D();
  for (let i = 0; i < n; i++) {
    const u = (i + .5) / n, d = Math.pow(u, 1.6), y = lerp(y0 + 6, y1 - 8, d);
    const L = lerp(46, 300, d) * (o.len || 1), th = lerp(1.8, 8, d) * (o.th || 1), per = L * (2.2 + r() * 1.4);
    const v = (5 + 20 * d) * sp * (i % 2 ? 1 : -.6), ph = r() * per, bob = Math.sin(t * (.9 + r() * .5) + i) * lerp(.5, 3, d);
    for (let x = x0 - per + ((ph + v * t) % per + per) % per; x < x1; x += per) {
      const isL = (Math.floor((x - ph) / per) + i) % 3 !== 0, P_ = isL ? light : dark, k = isL ? 1 : 1.4, yy = y + bob + (isL ? 0 : th * 1.6);
      const th2 = th * (.75 + .25 * Math.sin(t * 1.3 + x * .01 + i));
      P_.moveTo(x, yy); P_.quadraticCurveTo(x + L * k / 2, yy - th2, x + L * k, yy); P_.quadraticCurveTo(x + L * k / 2, yy + th2 * .35, x, yy);
    }
  }
  plate(ctx, 'teal', dark, { a: .75, flat: true });
  knock(ctx, light, o.lightCol || P.paper);
}
// yansıma: su üstünde kırık yatay şeritler (dalgaya bağlı yatay oynama)
function a2_reflect(ctx, x, y0, w, h, t, col, o = {}) {
  const p = new Path2D(), n = Math.floor(h / 9);
  for (let i = 0; i < n; i++) {
    const y = y0 + i * 9 + 3, k = 1 - i / n, ww = w * k * (.7 + .3 * Math.sin(i * 2.1)), dx = Math.sin(t * 1.7 + i * 1.3) * 5 * (1 + i * .12);
    p.rect(x - ww / 2 + dx, y, ww, 3.2 + k * 1.5);
  }
  if (col === 'paper') knock(ctx, p); else if (col === 'ink') inkFill(ctx, p, { a: o.a ?? .7 }); else plate(ctx, col, p, { a: o.a ?? .8, flat: true });
}

// ——————————————————————————————————————— gemiler, martılar ———
// buharlı vapur (yandan): x gövde ortası, yw su hattı, s ölçek (boy ≈ 430·s), dir +1 pruva sağda
function a2_steamer(ctx, x, yw, s, dir, t, o = {}) {
  const tq = a2_q(t), pitch = Math.sin(tq * .9 + (o.seed || 0)) * .006, bob = Math.sin(tq * 1.1 + (o.seed || 0)) * 1.6 * s;
  ctx.save(); ctx.translate(x, yw + bob); ctx.rotate(pitch * dir); ctx.scale(s * dir, s);
  const lw = px => px / s;
  // üst yapı (kâğıt), bacalar (okra), direkler
  const funnels = o.funnels || 1, fx = funnels === 2 ? [-46, 22] : [-12];
  for (const mx of [-150, 148]) inkStroke(ctx, PL([[mx, -40], [mx - 12, -196]], false), lw(3.2));
  inkStroke(ctx, PL([[-162, -196], [-214, -36]], false), lw(1.1), { a: .8 }); inkStroke(ctx, PL([[136, -196], [222, -46]], false), lw(1.1), { a: .8 });
  inkStroke(ctx, PL([[-162, -194], [136, -194]], false), lw(1.1), { a: .8 });
  for (const f of fx) {
    const fun = PL([[f, -76], [f + 30, -76], [f + 20, -158], [f - 10, -158]]);
    knock(ctx, fun); plate(ctx, 'ochre', fun); plate(ctx, 'ochre', PL([[f + 18, -76], [f + 30, -76], [f + 20, -158], [f + 8, -158]]), { a: .7 });
    inkFill(ctx, PL([[f - 8, -146], [f + 21, -146], [f + 20, -158], [f - 10, -158]]));
    inkStroke(ctx, fun, lw(2.6));
  }
  const dh1 = PL([[-118, -30], [126, -30], [126, -58], [-118, -58]]), dh2 = PL([[-70, -58], [74, -58], [74, -76], [-70, -76]]), br = PL([[78, -58], [118, -58], [118, -86], [78, -86]]);
  for (const q of [dh1, dh2, br]) { knock(ctx, q); plate(ctx, 'ochre', q, { a: .18 }); }
  plate(ctx, 'sepia', PL([[-118, -30], [126, -30], [126, -36], [-118, -36]]), { a: .4 });
  const win = new Path2D(); for (let wx = -108; wx < 118; wx += 14) win.rect(wx, -50, 7, 9); for (let wx = -62; wx < 66; wx += 14) win.rect(wx, -71, 7, 8); win.rect(86, -80, 24, 8);
  inkFill(ctx, win);
  for (const q of [dh1, dh2, br]) inkStroke(ctx, q, lw(2.2));
  inkStroke(ctx, PL([[-118, -60], [126, -60]], false), lw(1.2)); // küpeşte
  // gövde (is) + kâğıt sırt şeridi + lumbozlar
  const hull = SP([[-214, -36], [-196, -30], [0, -28], [180, -32], [222, -44], [214, -20], [206, 2], [-188, 2], [-204, -10]], true, .4);
  knock(ctx, hull); inkFill(ctx, hull);
  cut(ctx, SP([[-200, -24], [0, -21], [190, -25], [214, -33]], false, .6), lw(2.2), { a: .9 });
  const pw = new Path2D(); for (let px = -170; px < 190; px += 22) { pw.moveTo(px + 3, -12); pw.arc(px, -12, 3, 0, TAU); } knock(ctx, pw);
  ctx.restore();
  // duman: yarım ton küre dizisi (dünya koordinatında; hücre ölçekten bağımsız ≥10 px), rüzgâr kıça doğru
  const wind = o.wind ?? -dir;
  for (const f of fx) {
    const tx = x + (f + 5) * s * dir, ty = yw + bob - 160 * s, n = 7;
    for (let i = n - 1; i >= 0; i--) {
      const a = ((t * .22 + i / n) % 1), rr = lerp(10, 58, a) * s * 1.6;
      const px = tx + wind * a * 330 * s + Math.sin(t * .8 + i) * 6 * s, py = ty - a * 120 * s - Math.sin(a * 3) * 10 * s;
      const pp = a2_ell(px, py, rr * 1.25, rr * .8);
      halftone(ctx, o.smoke || 'sepia', pp, lerp(.5, .1, a), { cell: 10, ang: 45 });
    }
  }
}
// martı: iki kanat yayı; ph kanat evresi
function a2_gull(ctx, x, y, s, ph) {
  const p = new Path2D(), k = ph ? -1 : .4;
  p.moveTo(x - 18 * s, y - 6 * s * k); p.quadraticCurveTo(x - 9 * s, y - 10 * s * k - 3 * s, x, y); p.quadraticCurveTo(x + 9 * s, y - 10 * s * k - 3 * s, x + 18 * s, y - 6 * s * k);
  inkStroke(ctx, p, Math.max(2, 2.6 * s));
}
// küçük yelkenli (kayık, Latin yelken)
function a2_sailboat(ctx, x, yw, s, t) {
  const tq = a2_q(t), rk = Math.sin(tq * 1.4) * .03;
  ctx.save(); ctx.translate(x, yw + Math.sin(tq * 1.2) * 2); ctx.rotate(rk); ctx.scale(s, s);
  const sail = SP([[-4, -8], [2, -120], [70, -22]], true, .3);
  knock(ctx, sail); plate(ctx, 'ochre', sail, { a: .35 }); plate(ctx, 'ochre', SP([[-4, -8], [2, -120], [14, -30]], true, .3), { a: .4 }); inkStroke(ctx, sail, 2.2 / s);
  inkStroke(ctx, PL([[0, 0], [0, -126]], false), 3 / s); inkStroke(ctx, PL([[-30, -96], [74, -18]], false), 2.4 / s);
  const hull = SP([[-60, -10], [64, -12], [52, 6], [-46, 6]], true, .5); knock(ctx, hull); inkFill(ctx, hull); cut(ctx, PL([[-56, -6], [60, -8]], false), 1.6 / s, { a: .7 });
  ctx.restore();
}

// ——————————————————————————————————————— Selanik siluetleri ———
// Beyaz Kule: x orta, yb taban, s ölçek (s=1 → ~430 px). Işık soldan; gölge yanı sepya ikinci baskı, sarmal mazgallar
function a2_whiteTower(g, x, yb, s) {
  g.save(); g.translate(x, yb); g.scale(s, s);
  const lw = px => px / s, R = 104, H1 = 300, r2 = 52, H2 = 74;
  // dış sur (sekizgen alçak duvar)
  const wall = PL(rough([[-170, 0], [-170, -46], [170, -46], [170, 0]], .6, 81)); knock(g, wall); plate(g, 'ochre', wall, { a: .32 });
  plate(g, 'sepia', PL([[90, -46], [170, -46], [170, 0], [90, 0]]), { a: .35 });
  for (let i = -170; i < 170; i += 22) { const m = a2_R(i, -56, i + 12, -46); knock(g, m); plate(g, 'ochre', m, { a: .32 }); inkStroke(g, m, lw(1.6)); }
  inkStroke(g, wall, lw(2.6));
  for (const gx of [-160, 146]) { const gate = SP([[gx, 0], [gx, -18], [gx + 7, -25], [gx + 14, -18], [gx + 14, 0]], true, .5); inkFill(g, gate); }
  // gövde silindir
  const body = new Path2D(); body.moveTo(-R, -40); body.lineTo(-R, -H1); body.ellipse(0, -H1, R, 12, 0, PI, 0, false); body.lineTo(R, -40); body.ellipse(0, -40, R, 14, 0, 0, PI, false); body.closePath();
  knock(g, body);
  g.save(); g.clip(body);
  plate(g, 'sepia', a2_R(R * .38, -H1 - 20, R + 2, -30), { a: .42 });
  plate(g, 'sepia', a2_R(R * .74, -H1 - 20, R + 2, -30), { a: .45 });
  for (let i = 0; i < 9; i++) { const xx = R * (.42 + i * .065); inkStroke(g, PL([[xx, -H1 + 20], [xx, -42]], false), lw(1.1), { a: .35 }); }
  // taş sıraları (çok ince)
  for (let yy = -H1 + 36; yy < -44; yy += 26) { const q = new Path2D(); q.ellipse(0, yy, R, 12, 0, .15, PI - .15); inkStroke(g, q, lw(.9), { a: .22 }); }
  // sarmal mazgal pencereleri
  for (let i = 0; i < 11; i++) { const a = -1.15 + i * .55, yy = -60 - i * 21; const xx = Math.sin(a) * R * .9; if (Math.cos(a) < .15) continue; const ww = 6 * Math.cos(a) + 2; inkFill(g, a2_R(xx - ww / 2, yy - 13, xx + ww / 2, yy)); }
  g.restore();
  inkStroke(g, body, lw(3.4));
  // kornişli mazgal dişleri
  const cor = new Path2D(); for (let i = -6; i <= 6; i++) { const xx = Math.sin(i / 6 * 1.45) * R; cor.moveTo(xx - 5, -H1 + 6); cor.quadraticCurveTo(xx, -H1 + 16, xx + 5, -H1 + 6); }
  inkStroke(g, cor, lw(1.4), { a: .7 });
  const par = new Path2D(); par.rect(-R - 6, -H1 - 14, 2 * R + 12, 16); knock(g, par); plate(g, 'sepia', a2_R(R * .4, -H1 - 14, R + 6, -H1 + 2), { a: .4 }); inkStroke(g, par, lw(2.2));
  for (let i = -5; i <= 5; i++) { const xx = Math.sin(i / 5 * 1.4) * (R + 6), ww = 14 * Math.cos(i / 5 * 1.4) + 3; const m = a2_R(xx - ww / 2, -H1 - 34, xx + ww / 2, -H1 - 14); knock(g, m); if (xx > R * .3) plate(g, 'sepia', m, { a: .45 }); inkStroke(g, m, lw(1.8)); }
  // üst kule
  const top = new Path2D(); top.moveTo(-r2, -H1 - 14); top.lineTo(-r2, -H1 - 14 - H2); top.lineTo(r2, -H1 - 14 - H2); top.lineTo(r2, -H1 - 14); top.closePath();
  knock(g, top); plate(g, 'sepia', a2_R(r2 * .35, -H1 - 14 - H2, r2, -H1 - 14), { a: .45 }); inkStroke(g, top, lw(2.8));
  for (let i = -3; i <= 3; i++) { const xx = Math.sin(i / 3 * 1.3) * (r2 + 4), ww = 11 * Math.cos(i / 3 * 1.3) + 3; const m = a2_R(xx - ww / 2, -H1 - 14 - H2 - 18, xx + ww / 2, -H1 - 14 - H2); knock(g, m); if (xx > r2 * .3) plate(g, 'sepia', m, { a: .45 }); inkStroke(g, m, lw(1.6)); }
  inkFill(g, a2_R(-30, -H1 - 58, -24, -H1 - 40));
  g.restore();
}
// ev: duvar + kiremit çatı + pencereler (yukarı şehir ve rıhtım cepheleri)
function a2_house(g, x, yb, w, h, o = {}) {
  const r = rng(o.seed || 1), lwv = o.lw || 1.6;
  const wall = a2_R(x, yb - h, x + w, yb); knock(g, wall); plate(g, 'ochre', wall, { a: o.wa ?? .22 });
  if (o.shade) plate(g, 'sepia', a2_R(x + w * .72, yb - h, x + w, yb), { a: .3 });
  const rh = h * (o.roof ?? .32), roof = PL([[x - w * .06, yb - h], [x + w * .2, yb - h - rh], [x + w * .8, yb - h - rh], [x + w * 1.06, yb - h]]);
  knock(g, roof); plate(g, 'ochre', roof, { n: 2, a: .8 }); plate(g, 'sepia', roof, { a: .35 }); inkStroke(g, roof, lwv);
  const cols = Math.max(1, Math.round(w / (o.wsp || 26))), rows = o.rows || Math.max(1, Math.round(h / (o.hsp || 30))), ww = w / cols * .34, wh = h / rows * .42;
  const win = new Path2D();
  for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) { if (r() < .12) continue; const cx = x + (i + .5) * w / cols, cy = yb - h + (j + .55) * h / rows; win.rect(cx - ww / 2, cy - wh / 2, ww, wh); }
  inkFill(g, win, { a: o.wina ?? .9 });
  inkStroke(g, wall, lwv);
}
function a2_minaret(g, x, yb, h, s = 1) {
  const w = 12 * s, sh = a2_R(x - w / 2, yb - h, x + w / 2, yb); knock(g, sh); plate(g, 'sepia', a2_R(x + w * .1, yb - h, x + w / 2, yb), { a: .35 }); inkStroke(g, sh, 1.6);
  const bal = a2_R(x - w * .9, yb - h * .78, x + w * .9, yb - h * .74); knock(g, bal); inkStroke(g, bal, 1.4);
  const cap = PL([[x - w * .62, yb - h], [x, yb - h - 30 * s], [x + w * .62, yb - h]]); inkFill(g, cap);
}
function a2_dome(g, x, yb, r) {
  const drum = a2_R(x - r * .8, yb - r * .5, x + r * .8, yb); knock(g, drum); inkStroke(g, drum, 1.4);
  const d = new Path2D(); d.moveTo(x - r, yb - r * .5); d.arc(x, yb - r * .5, r, PI, 0); d.closePath(); knock(g, d); plate(g, 'sepia', d, { a: .55 }); inkStroke(g, d, 1.8);
}
function a2_cypress(g, x, yb, h, w) {
  const c = SP([[x, yb - h], [x + w * .5, yb - h * .55], [x + w * .45, yb - h * .1], [x, yb], [x - w * .45, yb - h * .1], [x - w * .5, yb - h * .55]], true, .8);
  knock(g, c); plate(g, 'teal', c, { n: 2 }); plate(g, 'ink', c, { a: .3 }); inkStroke(g, c, 1.6);
}

// ——————————————————————————————————————— damga kalabalık ———
// tam boy damga figür (birim: boy 100, ayak y=0, yüz +x). kind: 'fes'|'hat'|'boater'|'scarf'|'child'|'porter'; ph adım evresi; dir yürüyüş yönü
// pl: 'ink' (orta sıra) ya da 'tint' (arka sıra: tek açık sepya kalıbı — arka sıralarda kalıp azalır); red: fes kırmızısı
function a2_figure(ctx, x, yf, h, kind, ph, dir = 1, o = {}) {
  const s = h / 100, sc = kind === 'child' ? .64 : 1;
  ctx.save(); ctx.translate(x, yf); ctx.scale(s * sc * dir, s * sc);
  const p = new Path2D(), st = ph ? 6.5 : 2.2, sw = ph ? 4 : -2;
  if (kind === 'scarf') { // başörtü + uzun ferace
    spl(p, [[1, -104], [6.5, -101], [8, -93], [7.5, -86], [11, -82], [13, -62], [15 + (ph ? 2 : 0), -30], [17 + (ph ? 3 : 0), -1], [-13 + (ph ? -2 : 0), -1], [-12, -30], [-12, -64], [-10, -82], [-6.5, -88], [-6, -99]], true, .8);
    p.ellipse(8 + (ph ? 3 : 0), -1.5, 4.5, 2, 0, 0, TAU);
  } else {
    const bd = kind === 'porter' ? 9 : 0;                    // hamal öne eğik
    p.ellipse(2 + bd, -92 + bd * .3, 5.4, 6.6, 0, 0, TAU);   // baş
    spl(p, [[-2 + bd * .8, -85 + bd * .3], [6 + bd * .8, -84 + bd * .3], [9 + bd * .6, -78], [10, -60], [11.5, -36], [-11, -36], [-10, -60], [-9 + bd * .3, -79]], true, .7); // gövde (İstanbulin / ceket)
    // kollar: öndeki ileri, arkadaki geri salınır
    spl(p, [[6 + bd * .6, -80], [9 + bd * .5, -78], [12 + sw, -56], [12 + sw * 1.4, -48], [9 + sw * 1.4, -47], [7 + sw, -58]], true, .8);
    spl(p, [[-8 + bd * .3, -80], [-5, -78], [-9 - sw, -56], [-10 - sw * 1.4, -48], [-13 - sw * 1.4, -49], [-12 - sw, -60]], true, .8);
    // bacaklar (konik pantolon) ve kunduralar
    spl(p, [[-1, -38], [6, -38], [3 + st, -3], [-1 + st, -3]], true, .4);
    spl(p, [[-6, -38], [1, -38], [-2 - st, -3], [-6 - st, -3]], true, .4);
    p.ellipse(3 + st, -1.8, 5, 2, 0, 0, TAU); p.ellipse(-2 - st, -1.8, 5, 2, 0, 0, TAU);
    if (kind === 'porter') spl(p, [[-16, -88], [2, -100], [10, -96], [8, -70], [-14, -54], [-20, -66]], true, .8); // sırtta yük
  }
  const tint = o.pl === 'tint';
  if (tint) { knock(ctx, p); plate(ctx, 'sepia', p, { a: o.a ?? .5, flat: true }); } else inkFill(ctx, p);
  const solid = q => tint ? plate(ctx, 'sepia', q, { a: (o.a ?? .5) + .2, flat: true }) : inkFill(ctx, q);
  // başlık
  if (kind === 'fes' || kind === 'child' || kind === 'porter') {
    const bx = kind === 'porter' ? 9 : 0, by = kind === 'porter' ? 2.7 : 0;
    const f = PL([[-3.8 + bx, -96.5 + by], [5.2 + bx, -96.5 + by], [4.2 + bx, -105.5 + by], [-2.6 + bx, -105.5 + by]]);
    if (o.red !== false && !tint) { knock(ctx, f); plate(ctx, 'red', f, { flat: true }); inkStroke(ctx, f, 1 / s / sc); } else solid(f);
  } else if (kind === 'hat') {
    const hp = new Path2D(); hp.ellipse(1.5, -97, 9, 1.8, 0, 0, TAU); hp.moveTo(-4.5, -97); hp.quadraticCurveTo(-4.5, -106.5, 1.5, -106.5); hp.quadraticCurveTo(7.5, -106.5, 7.5, -97); hp.closePath();
    solid(hp);
  } else if (kind === 'boater') {
    const hp = new Path2D(); hp.ellipse(1.5, -98, 9.5, 1.8, 0, 0, TAU); hp.rect(-4, -104, 11, 6);
    knock(ctx, hp); if (tint) plate(ctx, 'sepia', hp, { a: .25, flat: true }); inkStroke(ctx, hp, 1 / s / sc, { a: tint ? .5 : 1 }); solid(a2_R(-4, -100.5, 7, -98.5));
  }
  ctx.restore();
}

// Ön sıra yüzü seçilen figür: büst + ¾ baş; kind: 'fes'|'hat'|'scarf'|'boy'
function a2_frontFig(ctx, o) {
  const { x, y, s, dir } = o;
  if (o.kind === 'scarf') {
    a2_cloak(ctx, x, y, s, dir, o.col || 'teal', o.seed || 1, o.len || 340);
    head3q(ctx, { x, y, s, dir, who: 'anon', id: { mus: null, fem: 1, jaw: .9, brow: .12, browW: .7, eyeOpen: .82, seed: o.seed || 31 }, gear: 'basortu', light: 'front', look: o.look || [1, .2], age: o.age || 30, tilt: o.tilt || 0 });
    return;
  }
  bust(ctx, { x, y, s, dir, coat: o.coat || 'setre', col: o.col || 'ink', w: o.w || .92, seed: o.seed || 1, len: o.len || 330, turn: .3, sep: o.sep });
  const boy = o.kind === 'boy';
  head3q(ctx, { x, y, s, dir, who: 'anon', id: { mus: boy ? null : (o.mus ?? 'mk'), seed: o.seed || 9, ...(o.id || {}) }, gear: o.kind === 'hat' ? null : 'fes', light: 'front', look: o.look || [1, .25], age: o.age || (boy ? 14 : 34), tilt: o.tilt || 0 });
  if (o.kind === 'hat') a2_bowler(ctx, x, y, s, dir);
}
// melon şapka (baş koordinatında; head3q'den sonra)
function a2_bowler(ctx, x, y, s, dir) {
  const lw = px => Math.max(1.7 / s, px * Math.pow(s / 1.3, .75) / s);
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir * 1.08, s);
  const crown = SP([[-50, -30], [-48, -62], [-34, -84], [-8, -92], [18, -86], [32, -66], [36, -30]], true, .8);
  const brim = SP([[-70, -26], [-56, -38], [0, -42], [44, -36], [54, -26], [38, -20], [0, -24], [-48, -18]], true, .8);
  for (const q of [crown, brim]) { knock(ctx, q); inkFill(ctx, q); }
  cut(ctx, SP([[-42, -40], [-38, -66], [-20, -82]], false), lw(2), { a: .55 });
  cut(ctx, SP([[-58, -30], [0, -34], [44, -30]], false), lw(1.4), { a: .45 });
  ctx.restore();
}
// başörtülü kadının feracesi (büst boyu): yuvarlak omuzlu pelerin
function a2_cloak(ctx, x, y, s, dir, col, seed, len = 340) {
  const lw = px => Math.max(1.7 / s, px * Math.pow(s / 1.3, .75) / s), L = len;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
  const c = SP(rough([[-40, 70], [-84, 96], [-104, 160], [-112, L], [80, L], [74, 170], [58, 104], [24, 78]], .7, seed + 50), true, .8);
  knock(ctx, c); plate(ctx, col, c); plate(ctx, col, SP([[-40, 70], [-84, 96], [-104, 160], [-112, L], [-60, L], [-58, 150]], true), { a: .55 });
  for (const q of [[[-70, 130], [-80, L - 10]], [[-20, 120], [-12, L - 10]], [[40, 140], [46, L - 10]]]) inkStroke(ctx, SP(q, false), lw(1.6), { a: .5 });
  inkStroke(ctx, c, lw(3.4));
  ctx.restore();
}

// ——————————————————————————————————————— C01 · Selanik rıhtımı ———
// C01a: panorama — turkuaz deniz, Beyaz Kule (odak), vapurlar, yukarı şehir; bölüm kartı
function a2_C01_sky(g) {
  paperBG(g); g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  const x0 = -140, x1 = W + 140;
  plate(g, 'ochre', a2_R(x0, -140, x1, 520), { a: .2 });
  plate(g, 'ochre', a2_R(x0, -140, x1, 250), { a: .18 });
  halftone(g, 'sepia', a2_R(x0, -140, x1, 170), .11, { cell: 12, ang: 15 });
  // düz bulut bantları
  for (const [cx, cy, w, h, sd] of [[420, 150, 520, 34, 1], [1500, 110, 640, 40, 2], [980, 230, 380, 22, 3]]) {
    const c = SP(rough([[cx - w / 2, cy + h / 2], [cx - w * .3, cy - h * .2], [cx - w * .1, cy - h / 2], [cx + w * .15, cy - h * .4], [cx + w * .35, cy - h * .1], [cx + w / 2, cy + h / 2]], 2, sd + 60), true, .8);
    knock(g, c); plate(g, 'sepia', a2_R(cx - w / 2, cy + h * .15, cx + w / 2, cy + h / 2 + 2), { a: .25 }); inkStroke(g, c, 1.6, { a: .7 });
  }
}
function a2_C01_hills(g) {
  // Hortiaç dağı (uzak, sepya)
  const far = SP(rough([[-160, 470], [-160, 360], [120, 318], [420, 290], [700, 300], [980, 262], [1260, 286], [1540, 250], [1800, 290], [2080, 320], [2080, 470]], 3, 71), true, .7);
  knock(g, far); plate(g, 'sepia', far, { a: .3 }); halftone(g, 'sepia', far, .18, { cell: 11, ang: 15 }); inkStroke(g, far, 2);
  // yukarı şehir tepesi
  const hill = SP(rough([[-160, 600], [-160, 470], [200, 420], [520, 380], [820, 360], [1100, 372], [1400, 404], [1700, 440], [2080, 470], [2080, 600]], 2, 72), true, .8);
  knock(g, hill); plate(g, 'ochre', hill, { a: .28 }); plate(g, 'sepia', hill, { a: .16 }); inkStroke(g, hill, 2);
  // Yedikule surları tepede
  const wl = new Path2D(); const crest = [[360, 396], [520, 380], [700, 366], [860, 360]];
  for (let i = 0; i < crest.length - 1; i++) { const [ax, ay] = crest[i], [bx, by] = crest[i + 1]; for (let k = 0; k < 8; k++) { const u = k / 8, xx = lerp(ax, bx, u), yy = lerp(ay, by, u); wl.rect(xx, yy - 12, 12, 12); wl.rect(xx, yy - 16, 6, 4); } }
  knock(g, wl); plate(g, 'sepia', wl, { a: .4 }); inkStroke(g, wl, 1.2);
  for (const [tx, ty] of [[360, 396], [610, 373], [860, 360]]) { const tw = a2_R(tx - 12, ty - 40, tx + 12, ty); knock(g, tw); plate(g, 'sepia', tw, { a: .45 }); inkStroke(g, tw, 1.5); }
  // ev sıraları (yamaçta, küçükten büyüğe)
  const r = rng(73);
  for (let row = 0; row < 4; row++) {
    const yb = 430 + row * 42, sc = .55 + row * .2;
    for (let x = -140 + r() * 40; x < W + 140; x += (40 + r() * 34) * sc) {
      const hillY = 380 + Math.abs(x - 820) * .07; if (yb - 22 * sc < hillY) continue;
      a2_house(g, x, yb + r() * 8, (30 + r() * 26) * sc, (18 + r() * 16) * sc, { seed: row * 100 + Math.floor(x), lw: 1.2, wsp: 14, hsp: 14, wa: .18 + r() * .1, shade: r() < .5 });
      if (r() < .08) a2_minaret(g, x + 10, yb, 70 * sc, sc);
      if (r() < .06) a2_cypress(g, x - 6, yb + 4, 54 * sc, 14 * sc);
    }
  }
  a2_dome(g, 1010, 486, 30); a2_minaret(g, 1060, 492, 120, 1.1); a2_minaret(g, 520, 470, 104); a2_dome(g, 300, 500, 24);
}
function a2_C01_quay(g) {
  // rıhtım cepheleri (3–4 kat), Beyaz Kule sağda; rıhtım taşı
  const r = rng(91);
  let x = -150;
  while (x < W + 150) {
    const w = 120 + r() * 90, h = 90 + r() * 70;
    if (x > 1120 && x < 1560) { x += 40; continue; }               // kulenin çevresi açık (rıhtım meydanı)
    a2_house(g, x, 652, w, h, { seed: Math.floor(x), lw: 1.8, wsp: 24, hsp: 26, wa: .2 + r() * .14, shade: r() < .6, roof: .18 });
    x += w + 6 + r() * 14;
  }
  for (const cx of [140, 980, 1700]) a2_cypress(g, cx, 600, 120, 30);
  const quay = a2_R(-160, 640, W + 160, 700); knock(g, quay); plate(g, 'ochre', quay, { a: .45 }); plate(g, 'sepia', a2_R(-160, 652, W + 160, 700), { a: .4 });
  for (let i = -160; i < W + 160; i += 46) inkStroke(g, PL([[i, 652], [i, 700]], false), 1.2, { a: .45 });
  inkStroke(g, PL([[-160, 640], [W + 160, 640]], false), 2.4); inkStroke(g, PL([[-160, 652], [W + 160, 652]], false), 1.6);
  a2_whiteTower(g, 1340, 648, 1.0);
}
a2_shot(S('C01'), Wd('C01', 'rıhtımda'), (ctx, st) => {
  setReg(201);
  paperBG(ctx);
  const { t, lt, d } = st;
  const cm = a2_camAt(lt, d + 1, { x: W / 2 - 30, y: H / 2, z: 1.0 }, { x: W / 2 + 26, y: H / 2 - 6, z: 1.055 });
  a2_blit(ctx, a2_cache('c01-sky', 140, a2_C01_sky), cm, .15);
  a2_blit(ctx, a2_cache('c01-hills', 140, a2_C01_hills), cm, .45);
  // rıhtımdaki küçük kalabalık (kule dibinde, uzak)
  a2_blit(ctx, a2_cache('c01-quay', 140, a2_C01_quay), cm, .7);
  ctx.save(); cam(ctx, cm, .7);
  const tq = a2_q(lt), ph = Math.floor(t * 6) % 2;
  const kinds = ['fes', 'hat', 'scarf', 'fes', 'porter', 'fes', 'boater', 'scarf', 'fes', 'child', 'hat', 'fes'];
  kinds.forEach((k, i) => { const v = (i % 2 ? 9 : -7), x0 = 60 + i * 168 + (i * 37 % 50); a2_figure(ctx, x0 + v * tq, 640, 40, k, (ph + i) % 2, v > 0 ? 1 : -1, { red: true }); });
  ctx.restore();
  // deniz (ön katman)
  ctx.save(); cam(ctx, cm, 1);
  ctx.drawImage(a2_cache('c01-sea', 140, g => a2_seaBase(g, 652, H + 140)).c, -140, -140, W + 280, H + 280);
  a2_reflect(ctx, 1340, 664, 200, 120, t, 'paper');
  a2_waves(ctx, 652, H + 60, t, { seed: 11, rows: 16 });
  a2_steamer(ctx, 1760 - lt * 6, 712, .42, -1, t, { seed: 2 });
  a2_sailboat(ctx, 1090 + lt * 4, 790, .62, t);
  a2_steamer(ctx, 470 + lt * 11, 840, 1.0, 1, t, { funnels: 2, seed: 1 });
  a2_reflect(ctx, 470 + lt * 11, 846, 420, 90, t, 'ink', { a: .45 });
  ctx.restore();
  // martılar
  ctx.save(); cam(ctx, cm, .9);
  for (let i = 0; i < 5; i++) { const gx = 420 + i * 120 + lt * (24 + i * 5) + Math.sin(t * .7 + i) * 20, gy = 260 + Math.sin(i * 2.3) * 60 + Math.sin(t * 1.1 + i) * 8; a2_gull(ctx, gx, gy, .9 + (i % 3) * .2, Math.floor(t * 5 + i) % 2); }
  ctx.restore();
  chapterCard(ctx, 'II', 'SELANİK', 'YASAK KİTAPLAR · 1889–1906', lt, d, { size: 92 }); // alt satır başlıktan uzun: kutu başlığa göre ölçüldüğünden başlık büyütüldü
}, { tr: { type: 'press', dur: .8 } });

// C01b: rıhtım caddesi — Fransızca/Rumca tabelalar, Ladino ve Osmanlıca soyut iz; üç derinlikte damga kalabalık; ön sırada yüzü seçilen dört kişi
// cephe: zemin katta dükkân (tente + tabela), üst katlarda turkuaz kepenkli pencereler ve balkon
function a2_facade(g, x, w, o = {}) {
  const r = rng(o.seed || 1), yb = 706, top = -160;
  const wall = a2_R(x, top, x + w, yb); knock(g, wall); plate(g, 'ochre', wall, { a: o.wa ?? .3 });
  if (o.shade) plate(g, 'sepia', a2_R(x + w - 46, top, x + w, yb), { a: .32 });
  // kat silmeleri
  for (const yy of [118, 300, 470]) { const c = a2_R(x - 8, yy, x + w + 8, yy + 14); knock(g, c); plate(g, 'ochre', c, { a: .45 }); inkStroke(g, c, 2); }
  // üst kat pencereleri: turkuaz kepenkler
  const n = o.n || Math.max(2, Math.round(w / 150));
  for (let fl = 0; fl < 2; fl++) {
    const wy0 = fl ? 340 : 160, wh = fl ? 106 : 118;
    for (let i = 0; i < n; i++) {
      const cx = x + (i + .5) * w / n, ww = 52;
      const win = o.arch ? SP([[cx - ww / 2, wy0 + wh], [cx - ww / 2, wy0 + 22], [cx - ww * .36, wy0 + 6], [cx, wy0], [cx + ww * .36, wy0 + 6], [cx + ww / 2, wy0 + 22], [cx + ww / 2, wy0 + wh]], true, .5) : a2_R(cx - ww / 2, wy0, cx + ww / 2, wy0 + wh);
      knock(g, win); plate(g, 'sepia', win, { n: 2 }); inkFill(g, win, { a: .38 });
      cut(g, PL([[cx, wy0 + 4], [cx, wy0 + wh - 4]], false), 2, { a: .5 }); cut(g, PL([[cx - ww / 2 + 4, wy0 + wh * .4], [cx + ww / 2 - 4, wy0 + wh * .4]], false), 2, { a: .5 });
      for (const sd of [-1, 1]) {
        const sx0 = cx + sd * ww / 2, sx1 = cx + sd * (ww / 2 + 26), sh = a2_R(Math.min(sx0, sx1), wy0, Math.max(sx0, sx1), wy0 + wh);
        knock(g, sh); plate(g, 'teal', sh); for (let k = 1; k < 8; k++) inkStroke(g, PL([[sx0, wy0 + k * wh / 8], [sx1, wy0 + k * wh / 8]], false), 1.2, { a: .55 }); inkStroke(g, sh, 2);
      }
      const lin = a2_R(cx - ww / 2 - 30, wy0 - 14, cx + ww / 2 + 30, wy0 - 4); knock(g, lin); inkStroke(g, lin, 1.6);
      inkStroke(g, win, 2.4);
      if (fl === 1 && (i + (o.seed || 0)) % 2 === 0) { // balkon
        const bx0 = cx - 62, bx1 = cx + 62, by = wy0 + wh + 2;
        const sl = a2_R(bx0 - 6, by, bx1 + 6, by + 10); knock(g, sl); inkStroke(g, sl, 2);
        const rail = new Path2D(); rail.moveTo(bx0, by - 46); rail.lineTo(bx1, by - 46); for (let bx = bx0; bx <= bx1; bx += 10) { rail.moveTo(bx, by - 46); rail.lineTo(bx, by); }
        inkStroke(g, rail, 1.8);
      }
    }
  }
  // zemin kat: koyu dükkân açıklıkları
  const sx = x + 24, sw = w - 48;
  for (let i = 0; i < 3; i++) {
    const ox = sx + i * sw / 3 + 12, ow = sw / 3 - 24;
    const op = SP([[ox, yb], [ox, 584], [ox + ow / 2, 566], [ox + ow, 584], [ox + ow, yb]], true, .3);
    knock(g, op); plate(g, 'sepia', op, { n: 2 }); inkFill(g, op, { a: .55 });
    if (i === 1) { for (let k = 0; k < 3; k++) cut(g, PL([[ox + 10, 610 + k * 30], [ox + ow - 10, 610 + k * 30]], false), 1.6, { a: .35 }); }
    else { const shelf = new Path2D(); for (let k = 0; k < 4; k++) { const yy = 612 + k * 22; for (let j = 0; j < 6; j++) shelf.rect(ox + 10 + j * (ow - 20) / 6, yy - 12 - (j % 2) * 4, (ow - 20) / 6 - 4, 12 + (j % 2) * 4); } knock(g, shelf, P.paperD); plate(g, 'ochre', shelf, { a: .4 }); }
  }
  // tente: turkuaz-kâğıt çizgili, saçaklı
  const ay0 = 520, ay1 = 562, aw = new Path2D(), stripes = Math.round(sw / 34);
  for (let i = 0; i < stripes; i++) if (i % 2 === 0) { const a0 = sx + i * sw / stripes, a1 = sx + (i + 1) * sw / stripes; aw.moveTo(a0, ay0); aw.lineTo(a1, ay0); aw.lineTo(a1 + (a1 - x - w / 2) * .06, ay1); aw.lineTo(a0 + (a0 - x - w / 2) * .06, ay1); aw.closePath(); }
  const awAll = PL([[sx, ay0], [sx + sw, ay0], [sx + sw + sw * .03, ay1], [sx - sw * .03, ay1]]);
  knock(g, awAll); plate(g, o.awn || 'teal', aw); plate(g, 'sepia', a2_R(sx - 20, ay1 - 10, sx + sw + 20, ay1), { a: .25 });
  const sc = new Path2D(); for (let i = 0; i < stripes; i++) { const a0 = sx - sw * .03 + i * sw * 1.06 / stripes; sc.moveTo(a0, ay1); sc.quadraticCurveTo(a0 + sw * 1.06 / stripes / 2, ay1 + 16, a0 + sw * 1.06 / stripes, ay1); }
  inkStroke(g, sc, 2); inkStroke(g, awAll, 2.4);
  inkStroke(g, PL([[x, top], [x, yb]], false), 2.6); inkStroke(g, PL([[x + w, top], [x + w, yb]], false), 2.6);
  if (o.sign) a2_sign(g, x + (w - o.sign.w) / 2, 486 - 6, o.sign.w, 32 + 4, { seed: o.seed, ...o.sign });
  if (o.topSign) a2_sign(g, x + (w - o.topSign.w) / 2, 34, o.topSign.w, 60, { seed: o.seed + 5, ...o.topSign });
}
function a2_C01b_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-160, -160, W + 320, H + 320);
  a2_facade(g, -170, 470, { seed: 1, wa: .34, sign: { w: 380, text: "HÔTEL D'ANGLETERRE", font: FONT.title(24), dark: true } });
  a2_facade(g, 300, 440, { seed: 2, wa: .2, shade: true, arch: true, sign: { w: 330, text: 'ΚΑΦΕΝΕΙΟΝ', font: a2_GREEK(30), ls: 4, plate: 'ochre', pa: .35 } });
  a2_facade(g, 740, 460, { seed: 3, wa: .42, n: 2, sign: { w: 300, trace: 'heb', plate: 'ochre', pa: .25 } });
  a2_facade(g, 1200, 470, { seed: 4, wa: .24, shade: true, arch: true, sign: { w: 330, trace: 'osm', dark: true } });
  a2_facade(g, 1670, 460, { seed: 5, wa: .36, sign: { w: 380, text: 'BANQUE DE SALONIQUE', font: FONT.title(24), dark: true }, awn: 'teal' });
  // kenarlarda gölge (düz iki basamak): ışık sokağın ortasında
  for (const [x0, x1] of [[-160, 330], [1590, W + 160]]) plate(g, 'sepia', a2_R(x0, -160, x1, 706), { a: .16 });
  for (const [x0, x1] of [[-160, 120], [1800, W + 160]]) plate(g, 'sepia', a2_R(x0, -160, x1, 706), { a: .14 });
  // kaldırım: ufuk göz hizasında (y≈560), taş derzleri
  const pave = a2_R(-160, 706, W + 160, H + 160); knock(g, pave); plate(g, 'ochre', pave, { a: .2 });
  plate(g, 'sepia', a2_R(-160, 706, W + 160, 724), { a: .35 }); inkStroke(g, PL([[-160, 706], [W + 160, 706]], false), 2.6);
  for (let k = 0; k < 8; k++) { const yy = 724 + Math.pow(k / 7, 1.6) * 360; inkStroke(g, PL([[-160, yy], [W + 160, yy]], false), 1.1, { a: .3 }); }
  for (let i = -12; i <= 12; i++) { const xb = 960 + i * 150; inkStroke(g, PL([[960 + (xb - 960) * .18, 724], [960 + (xb - 960) * 2.4, H + 160]], false), 1.1, { a: .25 }); }
  // sokak lambası direkleri
  for (const lx of [250, 1450]) {
    const post = SP([[lx - 7, 720], [lx - 4, 420], [lx + 4, 420], [lx + 7, 720]], true, .4); knock(g, post); inkFill(g, post);
    const lan = PL([[lx - 20, 380], [lx + 20, 380], [lx + 14, 420], [lx - 14, 420]]); knock(g, lan); plate(g, 'ochre', lan, { a: .5 }); inkStroke(g, lan, 2.4);
    inkFill(g, PL([[lx - 24, 380], [lx, 360], [lx + 24, 380]]));
  }
}
// kelimeye bağlı dil damgası (izleyici katmanı): basılma darbesiyle gelir
function a2_wordStamp(ctx, s, x, y, lt, o = {}) {
  if (NOTEXT || lt < 0) return;
  const fs = o.size || 66, k = 1 + (1 - E.out3(clamp(lt / .18))) * .22, a = clamp(lt / .06) * (o.a ?? 1);
  ctx.save(); ctx.font = FONT.title(fs); ctx.letterSpacing = '2px'; const w = ctx.measureText(s).width; ctx.restore();
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(k, k); ctx.rotate(o.rot || 0);
  const bw = w + 44, bh = fs * 1.02, box = PL(rough([[-bw / 2, -bh / 2], [bw / 2, -bh / 2], [bw / 2, bh / 2], [-bw / 2, bh / 2]], .9, s.length + 11));
  plate(ctx, 'ink', PL([[-bw / 2 + 7, -bh / 2 + 8], [bw / 2 + 7, -bh / 2 + 8], [bw / 2 + 7, bh / 2 + 8], [-bw / 2 + 7, bh / 2 + 8]]), { a: .35 });
  knock(ctx, box, o.bg || P.paper); inkStroke(ctx, box, 3);
  txt(ctx, s, 0, fs * .02, FONT.title(fs), { align: 'center', base: 'middle', ls: 2 });
  ctx.restore();
}
a2_shot(Wd('C01', 'rıhtımda'), S('C02'), (ctx, st) => {
  setReg(202);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(lt), ph = Math.floor(t * 6) % 2;
  const cm = a2_camAt(lt, d, { x: W / 2 - 40, y: H / 2, z: 1.03 }, { x: W / 2 + 60, y: H / 2 - 4, z: 1.06 });
  a2_blit(ctx, a2_cache('c01b-bg', 160, a2_C01b_bg), cm, .55);
  // arka sıra: yalnız sepya kalıbı
  ctx.save(); cam(ctx, cm, .65);
  const back = ['hat', 'fes', 'scarf', 'fes', 'boater', 'porter', 'fes', 'scarf', 'hat', 'fes', 'child', 'fes', 'scarf', 'hat'];
  back.forEach((k, i) => { const v = i % 3 === 0 ? 22 : -16, x0 = -120 + i * 160 + (i * 53 % 70); a2_figure(ctx, x0 + v * tq, 742, 168, k, (ph + i) % 2, v > 0 ? 1 : -1, { pl: 'tint', a: .5, red: false }); });
  ctx.restore();
  // orta sıra: is + fes kırmızısı
  ctx.save(); cam(ctx, cm, .82);
  const mid = [['fes', 34], ['scarf', -26], ['hat', -30], ['porter', 24], ['boater', -24], ['fes', -28], ['child', 30], ['fes', 26]];
  mid.forEach(([k, v], i) => { const x0 = [-40, 200, 760, 1290, 1420, 1900, 2050, 2200][i]; a2_figure(ctx, x0 + v * tq, 880, 300, k, (ph + i + 1) % 2, v > 0 ? 1 : -1, {}); });
  ctx.restore();
  // ön sıra: yüzü seçilen dört kişi (büst), yavaşça sola yürür; adım evresinde hafif iniş-kalkış
  ctx.save(); cam(ctx, cm, 1);
  const bob = i => (Math.floor(t * 6 + i) % 2) * 5;
  const F = [
    { kind: 'hat', x: 1660 - 30 * tq, y: 640, s: .96, dir: -1, coat: 'civil', col: 'sepia', seed: 61, age: 40, look: [1, .2] },
    { kind: 'scarf', x: 1170 - 34 * tq, y: 652, s: .94, dir: -1, col: 'teal', seed: 33, age: 32, look: [1, .25] },
    { kind: 'boy', x: 1000 - 34 * tq, y: 756, s: .72, dir: -1, coat: 'setre', col: 'navy', seed: 41, age: 12, look: [1, -.2] },
    { kind: 'fes', x: 560 - 28 * tq, y: 646, s: .98, dir: -1, coat: 'setre', col: 'ink', seed: 51, age: 46, mus: 'pala', id: { hair: 'grey', musCol: 'grey' }, look: [1, .25] },
  ];
  F.forEach((f, i) => a2_frontFig(ctx, { ...f, y: f.y + bob(i), len: (H + 40 - f.y) / f.s, sep: true }));
  ctx.restore();
  // dil damgaları: kelimesi duyulduğu an basılır
  const words = [['LADINO', 'ladino'], ['RUMCA', 'rumca'], ['BULGARCA', 'bulgarca'], ['TÜRKÇE', 'türkçe']];
  words.forEach(([s, w], i) => a2_wordStamp(ctx, s, 300 + i * 440, 112, t - Wd('C01', w), { rot: [-.03, .02, -.015, .025][i], size: 70 }));
}, { tr: { type: 'cut' } });

// ——————————————————————————————————————— C02 · Rıhtımda çocuk (yorum) ———
// gün batımı körfez: gök okra bantları, Olimpos silueti, güneş (kâğıt), turkuaz deniz; hy: ufuk (göz hizası)
function a2_gulfBG(g, hy, o = {}) {
  g.fillStyle = P.paper; g.fillRect(-160, -160, W + 320, H + 320);
  const x0 = -160, x1 = W + 160, sx = o.sunX ?? 1180, sy = hy - (o.sunH ?? 90);
  plate(g, 'ochre', a2_R(x0, -160, x1, hy), { a: .3 });
  plate(g, 'ochre', a2_R(x0, -160, x1, hy - 260), { a: .22 });
  plate(g, 'sepia', a2_R(x0, -160, x1, hy - 420), { a: .14 });
  halftone(g, 'sepia', a2_R(x0, -160, x1, hy - 420), .12, { cell: 12, ang: 15 });
  // güneş: kâğıt disk + düz okra halkalar (ışık kaynağının kendi çevresi)
  for (const [r, a] of [[150, .1], [100, .12]]) { const hp = a2_ell(sx, sy, r * 1.3, r); knock(g, hp, '#E9DCBF'); plate(g, 'ochre', hp, { a }); }
  const sun = a2_ell(sx, sy, 52, 52); knock(g, sun, '#F6EFDD'); inkStroke(g, sun, 2.2);
  // bulut şeritleri güneşin önünden geçer
  for (const [cx, cy, w, h, sd] of [[sx - 120, sy + 22, 420, 14, 1], [sx + 260, sy - 70, 520, 18, 2], [380, hy - 330, 600, 26, 3]]) {
    const c = SP(rough([[cx - w / 2, cy + h / 2], [cx - w * .25, cy - h / 2], [cx + w * .2, cy - h * .4], [cx + w / 2, cy + h / 2]], 1.5, sd + 90), true, .8);
    knock(g, c, P.paperD); plate(g, 'sepia', c, { a: .35 }); inkStroke(g, c, 1.6, { a: .8 });
  }
  // Olimpos: körfezin karşısında, karlı tepe
  const ol = SP(rough([[-160, hy], [-160, hy - 60], [-20, hy - 96], [110, hy - 150], [200, hy - 172], [260, hy - 196], [330, hy - 206], [390, hy - 192], [450, hy - 210], [520, hy - 198], [600, hy - 160], [700, hy - 140], [800, hy - 100], [930, hy - 66], [1060, hy - 30], [1140, hy]], 2, 95), true, .7);
  knock(g, ol); plate(g, 'sepia', ol, { a: .3 }); plate(g, 'teal', ol, { a: .18 });
  const snow = SP(rough([[210, hy - 168], [260, hy - 194], [330, hy - 204], [390, hy - 190], [450, hy - 208], [520, hy - 196], [566, hy - 172], [510, hy - 180], [450, hy - 186], [390, hy - 174], [330, hy - 188], [270, hy - 172]], 1, 96), true, .7);
  knock(g, snow); inkStroke(g, ol, 1.8);
  a2_seaBase(g, hy, H + 160, { a: .74 });
  // rıhtım taşı (ön), y: o.qy
  if (o.qy) {
    const qy = o.qy, top = a2_R(-160, qy, W + 160, qy + 40), face = a2_R(-160, qy + 40, W + 160, H + 160);
    knock(g, top); knock(g, face); plate(g, 'ochre', top, { a: .5 }); plate(g, 'sepia', face, { a: .8 }); plate(g, 'ochre', face, { a: .35 });
    for (let i = -160; i < W + 160; i += 170) { inkStroke(g, PL([[i, qy], [i - 10, qy + 40]], false), 1.6); inkStroke(g, PL([[i + 60, qy + 40], [i + 60, H + 160]], false), 1.4, { a: .6 }); }
    for (let yy = qy + 110; yy < H + 160; yy += 70) cut(g, PL([[-160, yy], [W + 160, yy]], false), 1.6, { a: .3 });
    inkStroke(g, PL([[-160, qy], [W + 160, qy]], false), 3); inkStroke(g, PL([[-160, qy + 40], [W + 160, qy + 40]], false), 2.6);
  }
}
// güneş yolu: güneşin altındaki kırık kâğıt şeritler (dalgayla oynar)
function a2_sunPath(ctx, sx, hy, y1, t) {
  const p = new Path2D(), r = rng(5);
  for (let y = hy + 6, i = 0; y < y1; i++) {
    const d = (y - hy) / (y1 - hy), w = lerp(40, 380, d) * (.5 + r() * .6), dx = Math.sin(t * 1.4 + i * 1.7) * lerp(3, 26, d) + (r() - .5) * lerp(20, 140, d), th = lerp(2, 9, d);
    p.moveTo(sx + dx - w / 2, y); p.quadraticCurveTo(sx + dx, y - th, sx + dx + w / 2, y); p.quadraticCurveTo(sx + dx, y + th * .4, sx + dx - w / 2, y);
    y += lerp(5, 26, d);
  }
  knock(ctx, p, '#F6EFDD');
}
// çocuk, arkadan (oturmuş): baş merkezi (x,y), s ölçek (s=1 → baş ≈ 110 px); turn: başın sağa dönüşü (-1..1), ph: püskül evresi
function a2_childBack(ctx, x, y, s, o = {}) {
  const lw = px => Math.max(1.6 / s, px / s), turn = o.turn || 0, up = o.up || 0;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  // gövde: lacivert mektep setresi (arkadan); kollar yanlarda, eller taşa dayalı
  const body = SP(rough([[-22, 46], [-60, 60], [-78, 100], [-84, 245], [84, 245], [78, 100], [60, 60], [22, 46]], .5, 501), true, .8);
  const armL = SP([[-66, 70], [-86, 100], [-100, 190], [-104, 236], [-84, 240], [-80, 180], [-72, 120]], true, .8), armR = SP([[66, 70], [86, 100], [100, 190], [104, 236], [84, 240], [80, 180], [72, 120]], true, .8);
  for (const q of [armL, armR, body]) { knock(ctx, q); plate(ctx, 'navy', q); }
  plate(ctx, 'navy', SP([[30, 50], [60, 60], [78, 100], [84, 245], [50, 245], [44, 120]], true, .8), { a: .5 });  // gölge yanı (ikinci baskı)
  plate(ctx, 'navy', armR, { a: .5 });
  for (const q of [armL, armR]) inkStroke(ctx, q, lw(3.4));
  inkStroke(ctx, body, lw(3.6));
  inkStroke(ctx, SP([[0, 58], [2, 150], [0, 245]], false), lw(1.8), { a: .55 });       // sırt dikişi
  for (const q of [[[-50, 90], [-44, 160]], [[48, 94], [42, 170]], [[-64, 190], [-44, 240]]]) cut(ctx, SP(q, false), lw(1.6), { a: .35 });
  // eller (taşa dayalı)
  for (const sd of [-1, 1]) { const hd = SP([[sd * 84, 232], [sd * 106, 230], [sd * 114, 246], [sd * 82, 247]], true, .8); knock(ctx, hd); plate(ctx, 'ochre', hd, { a: .35 }); inkStroke(ctx, hd, lw(2.4)); }
  // dik yaka
  const col = SP([[-30, 34], [30, 34], [34, 56], [-34, 56]], true, .6); knock(ctx, col); plate(ctx, 'navy', col, { n: 2 }); inkStroke(ctx, col, lw(2.6));
  // boyun (kâğıt) + ense gölgesi
  const neck = SP([[-22, 16], [22, 16], [24, 38], [-24, 38]], true, .6); knock(ctx, neck); plate(ctx, 'ochre', a2_R(-24, 16, 24, 26), { a: .4 }); inkStroke(ctx, neck, lw(2.4));
  ctx.save(); ctx.translate(0, -up * 6); ctx.rotate(turn * .08 - up * .04);
  // kulaklar (dönüşe göre)
  for (const sd of [-1, 1]) {
    const ex = sd * (44 - sd * turn * 6), ear = SP([[ex, -8], [ex + sd * 10, -12], [ex + sd * 13, 4], [ex + sd * 8, 20], [ex, 18]], true, .8);
    knock(ctx, ear); plate(ctx, 'ochre', ear, { a: .3 }); inkStroke(ctx, ear, lw(2.2)); inkStroke(ctx, SP([[ex + sd * 4, -4], [ex + sd * 8, 6], [ex + sd * 4, 14]], false), lw(1.2));
  }
  // yanak (sağa dönünce sağda belirir)
  if (turn > .1) { const ch = SP([[30, 0], [48 + turn * 6, 6], [46 + turn * 6, 30], [30, 34]], true, .8); knock(ctx, ch); plate(ctx, 'ochre', ch, { a: .25 }); inkStroke(ctx, SP([[46 + turn * 6, 4], [48 + turn * 6, 18], [42, 32]], false), lw(2.2)); }
  // kısa kesilmiş saç (ense)
  const skull = SP([[-44, -30], [-46, 0], [-36, 22], [-20, 30], [0, 32], [20, 30], [36, 22], [46, 0], [44, -30]], true, .8);
  knock(ctx, skull); plate(ctx, 'ochre', skull, { a: .3 }); inkStroke(ctx, skull, lw(2.6));
  const hair = SP(rough([[-44, -30], [-45, -4], [-36, 6], [-18, 11], [0, 14], [18, 11], [36, 6], [45, -4], [44, -30]], .4, 502), true, .8);
  knock(ctx, hair); inkFill(ctx, hair);
  for (let i = 0; i < 9; i++) cut(ctx, SP([[-34 + i * 8.5, -22], [-36 + i * 8.6, -8], [-33 + i * 8.2, 4]], false), lw(1.1), { a: .3 });
  // fes (arkadan): kırmızı vurgu, koyu yanı ikinci baskı; püskül arkaya sarkar
  const fes = SP(rough([[-45, -24], [-40, -56], [-33, -84], [33, -84], [40, -56], [45, -24], [0, -18]], .4, 503), true, .5);
  knock(ctx, fes); plate(ctx, 'red', fes); plate(ctx, 'red', SP([[16, -84], [33, -84], [40, -56], [45, -24], [22, -20]], true, .5), { a: .5 }); inkStroke(ctx, fes, lw(3.2));
  const topE = new Path2D(); topE.ellipse(0, -84, 33, 5, 0, PI, TAU); inkStroke(ctx, topE, lw(2));
  const sw = (o.ph ? 1 : -1) * 4;
  inkFill(ctx, SP([[-2, -86], [6, -84], [8 + sw, -46], [4 + sw, -34], [-6 + sw, -36], [-4 + sw, -48]], true, .8));
  ctx.restore();
  ctx.restore();
}
// gazete destesi (iple bağlı) — C02a'da çocuğun yanında
function a2_bundle(ctx, x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  for (let i = 0; i < 4; i++) { const sh = PL(rough([[-90, -i * 9 - 9], [90, -i * 9 - 11], [92, -i * 9], [-88, -i * 9 + 2]], .8, 510 + i)); knock(ctx, sh); plate(ctx, 'ochre', sh, { a: .12 + i * .04 }); inkStroke(ctx, sh, 2 / s); }
  const top = PL(rough([[-86, -48], [84, -50], [92, -38], [-90, -36]], .6, 520)); knock(ctx, top); inkStroke(ctx, top, 2.2 / s);
  inkStroke(ctx, PL([[-20, -48], [-26, 2]], false), 3 / s); inkStroke(ctx, PL([[30, -50], [24, 0]], false), 3 / s);
  ctx.restore();
}
a2_shot(S('C02'), Wd('C02', 'burada'), (ctx, st) => {
  setReg(203);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t), hy = 560;
  const cm = a2_camAt(lt, d, { x: W / 2, y: H / 2, z: 1.0 }, { x: W / 2 + 20, y: H / 2 - 8, z: 1.05 });
  ctx.save(); cam(ctx, cm, .5); ctx.drawImage(a2_cache('c02a-bg', 160, g => a2_gulfBG(g, hy, { qy: 905, sunX: 1060 })).c, -160, -160, W + 320, H + 320);
  a2_sunPath(ctx, 1060, hy, 900, t);
  a2_waves(ctx, hy, 905, t, { seed: 21, rows: 14, speed: .7 });
  a2_steamer(ctx, 1640 - lt * 7, hy + 6, .3, -1, t, { seed: 5 });
  a2_sailboat(ctx, 420 + lt * 5, hy + 70, .5, t);
  for (let i = 0; i < 3; i++) a2_gull(ctx, 900 + i * 140 + lt * (18 + i * 6), 300 + i * 40 + Math.sin(t + i) * 10, 1.1, Math.floor(t * 5 + i) % 2);
  ctx.restore();
  // ön plan: rıhtım taşı üstünde çocuk ve gazete destesi; baba direği (bollard)
  ctx.save(); cam(ctx, cm, 1);
  a2_bundle(ctx, 470, 902, 1.1);
  const bol = SP([[1438, 906], [1446, 860], [1440, 842], [1420, 834], [1424, 818], [1470, 812], [1516, 818], [1520, 834], [1500, 842], [1494, 860], [1502, 906]], true, .5); knock(ctx, bol); inkFill(ctx, bol); cut(ctx, SP([[1428, 824], [1470, 820], [1512, 824]], false), 2, { a: .6 }); cut(ctx, PL([[1452, 856], [1450, 900]], false), 2, { a: .4 });
  const rope = new Path2D(); for (let k = 0; k < 4; k++) rope.ellipse(1600, 896 - k * 10, 90 - k * 8, 16, 0, 0, TAU); knock(ctx, a2_ell(1600, 880, 92, 34)); inkStroke(ctx, rope, 3); plate(ctx, 'ochre', a2_ell(1600, 880, 92, 34), { a: .35 });
  const turn = kf(tq - S('C02'), [[0, -.2], [1.6, .5], [3.4, .5], [4.6, .1]]);
  a2_childBack(ctx, 800, hy + 4 + Math.sin(tq * 1.5) * 1.5, 1.39, { turn, ph: Math.floor(t * 4) % 2 });
  ctx.restore();
}, { tr: { type: 'press', dur: .6 } });

// C02b: "dünyanın tek kalıba sığmadığını": dört alfabede gazete rüzgârda uçuşur; her biri başka kalıpla basılmış (is, turkuaz, lacivert, sepya)
// kind: 'fr' (Journal de Salonique), 'gr' (Φάρος), 'lad' (Ladino, İbrani harfli soyut iz), 'osm' (Osmanlıca soyut iz); flap: kanat evresi -1..1
function a2_newspaper(ctx, x, y, w, h, rot, kind, flap, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  const sx = .42 + .58 * Math.abs(Math.cos(flap * 1.1)), sk = Math.sin(flap * 1.7) * .2;
  ctx.transform(sx, sk * .3, sk, 1, 0, 0);
  const bend = flap * h * .07, hw = w / 2, hh = h / 2;
  const sheet = new Path2D(); sheet.moveTo(-hw, -hh); sheet.quadraticCurveTo(0, -hh - bend, hw, -hh + bend * .6); sheet.lineTo(hw + bend * .3, hh + bend * .6); sheet.quadraticCurveTo(0, hh - bend, -hw, hh); sheet.closePath();
  knock(ctx, sheet, o.bg || '#F3EBD8'); if (o.age) plate(ctx, 'ochre', sheet, { a: o.age });
  ctx.save(); ctx.clip(sheet);
  const pl = { fr: 'ink', gr: 'teal', lad: 'navy', osm: 'sepia' }[kind], col = P[pl], my = -hh + h * .13;
  if (kind === 'fr') txt(ctx, 'JOURNAL DE SALONIQUE', 0, my, FONT.title(Math.round(w * .072)), { align: 'center', base: 'middle', col });
  else if (kind === 'gr') txt(ctx, 'ΦΑΡΟΣ ΤΗΣ ΜΑΚΕΔΟΝΙΑΣ', 0, my, a2_GREEK(Math.round(w * .062)), { align: 'center', base: 'middle', plate: 'teal' });
  else if (kind === 'lad') a2_squareTrace(ctx, hw * .7, my + h * .035, w * .7, h * .07, 611, { col, w: Math.max(3, w * .014) });
  else scriptLine(ctx, hw * .74, my + h * .02, w * .74, h * .06, 621, { col, w: Math.max(3, w * .013) });
  // başlık altı çift çizgi (kendi kalıbında)
  for (const dy of [h * .085, h * .1]) plate(ctx, pl, a2_R(-hw + 14, my + dy, hw - 14, my + dy + (dy > h * .09 ? 2 : 4)), { flat: true });
  // sütunlar
  const cols = 3, cw = (w - 40) / cols, y0 = my + h * .15, rows = Math.floor((hh - 20 - y0) / (h * .036));
  for (let c = 0; c < cols; c++) {
    const cx0 = -hw + 20 + c * cw;
    if (c) inkStroke(ctx, PL([[cx0 - 2, y0 - 4], [cx0 - 2, hh - 14]], false), 1.2, { a: .5 });
    for (let r = 0; r < rows; r++) {
      const yy = y0 + r * h * .036, L = (cw - 16) * (r % 7 === 6 ? .55 : 1);
      if (c === 1 && r < 5) continue;                                   // gravür kutusu
      if (kind === 'fr' || kind === 'gr') inkStroke(ctx, PL([[cx0 + 6, yy], [cx0 + 6 + L, yy]], false), Math.max(1.5, h * .006), { a: .55, cap: 'butt' });
      else if (kind === 'lad') a2_squareTrace(ctx, cx0 + cw - 10, yy + 3, L, h * .014, 640 + c * 40 + r, { w: 1.4, a: .7 });
      else scriptLine(ctx, cx0 + cw - 10, yy + 2, L, h * .014, 660 + c * 40 + r, { w: 1.4, a: .75 });
    }
  }
  // gravür kutusu: kendi kalıbıyla taranmış küçük resim (vapur silueti)
  const bx0 = -hw + 20 + cw + 4, by0 = y0 - 2, bx1 = bx0 + cw - 12, by1 = y0 + 5 * h * .036 - 6, box = a2_R(bx0, by0, bx1, by1);
  plate(ctx, pl, box, { a: .22, flat: true }); for (let k = 0; k < 9; k++) inkStroke(ctx, PL([[bx0, by0 + k * (by1 - by0) / 9], [bx1, by0 + k * (by1 - by0) / 9]], false), 1, { a: .3 });
  { const bw = bx1 - bx0, bh = by1 - by0, hz = by0 + bh * .66, u = bw / 100;
    inkStroke(ctx, PL([[bx0, hz], [bx1, hz]], false), 1.2, { a: .7 });
    inkFill(ctx, PL([[bx0 + 14 * u, hz - 8 * u], [bx0 + 88 * u, hz - 9 * u], [bx0 + 82 * u, hz + 2 * u], [bx0 + 20 * u, hz + 2 * u]]));
    knock(ctx, a2_R(bx0 + 32 * u, hz - 14 * u, bx0 + 70 * u, hz - 8 * u)); inkStroke(ctx, a2_R(bx0 + 32 * u, hz - 14 * u, bx0 + 70 * u, hz - 8 * u), 1);
    inkFill(ctx, PL([[bx0 + 46 * u, hz - 14 * u], [bx0 + 54 * u, hz - 14 * u], [bx0 + 52 * u, hz - 30 * u], [bx0 + 44 * u, hz - 30 * u]]));
    for (const mx of [24, 80]) inkStroke(ctx, PL([[bx0 + mx * u, hz - 8 * u], [bx0 + (mx - 2) * u, hz - 38 * u]], false), 1.2);
    for (let k = 0; k < 4; k++) { const q = a2_ell(bx0 + (40 - k * 9) * u, hz - (34 + k * 4) * u, (3 + k) * u, (2 + k * .6) * u); inkFill(ctx, q, { a: .55 - k * .1 }); } }
  inkStroke(ctx, box, 1.6);
  ctx.restore();
  // kıvrım gölgesi ve dış hat
  if (Math.abs(flap) > .25) plate(ctx, 'sepia', PL([[0, -hh - bend * .5], [hw, -hh + bend * .6], [hw + bend * .3, hh + bend * .6], [0, hh - bend * .5]]), { a: .18 * Math.abs(flap) });
  inkStroke(ctx, sheet, 2.6);
  ctx.restore();
}
a2_shot(Wd('C02', 'burada'), S('C03'), (ctx, st) => {
  setReg(204);
  paperBG(ctx);
  const { t, lt, d } = st, lq = a2_q(lt), hy = 690;
  const cm = a2_camAt(lt, d, { x: W / 2 + 10, y: H / 2, z: 1.02 }, { x: W / 2 - 24, y: H / 2 - 10, z: 1.06 });
  ctx.save(); cam(ctx, cm, .4); ctx.drawImage(a2_cache('c02b-bg', 160, g => a2_gulfBG(g, hy, { qy: 916, sunX: 1540, sunH: 130 })).c, -160, -160, W + 320, H + 320);
  a2_sunPath(ctx, 1540, hy, 912, t);
  a2_waves(ctx, hy, 916, t, { seed: 23, rows: 10, speed: .7 });
  ctx.restore();
  // gazeteler: rüzgâr sağdan sola; uzaktakiler küçük ve yaşlı kâğıt, öndeki (Fransızca) en parlak
  ctx.save(); cam(ctx, cm, .85);
  const P_ = [
    { k: 'gr', x0: 1960, y0: 250, v: 120, w: 280, h: 370, r0: .32, f: .9, ph: 1.1, age: .16 },
    { k: 'osm', x0: 760, y0: 300, v: 95, w: 300, h: 400, r0: -.28, f: .8, ph: 2.3, age: .14 },
    { k: 'lad', x0: 1720, y0: 640, v: 80, w: 250, h: 330, r0: .14, f: 1.1, ph: .4, age: .18 },
  ];
  for (const p of P_) a2_newspaper(ctx, p.x0 - p.v * lq, p.y0 + Math.sin(lq * p.f + p.ph) * 40, p.w, p.h, p.r0 + Math.sin(lq * 1.3 + p.ph) * .18, p.k, Math.sin(lq * 2.2 * PI * .5 + p.ph), { age: p.age });
  ctx.restore();
  ctx.save(); cam(ctx, cm, 1);
  a2_newspaper(ctx, 1260 - 92 * lq, 420 + Math.sin(lq * .9) * 34, 420, 540, -.12 + Math.sin(lq * 1.1) * .14, 'fr', Math.sin(lq * 2.6 + .6) * .9, { bg: '#F7F1E2' });
  a2_childBack(ctx, 300, hy + 4, .92, { turn: .8, up: 1, ph: Math.floor(t * 4) % 2 });
  ctx.restore();
}, { tr: { type: 'cut' } });

// ——————————————————————————————————————— C03 · Sorgulama ve yasak kitaplar ———
// C03a: masada geometri defteri; pirinç pergel yay çizer, "sorgulamayı"da yay soru işaretine tamamlanır
// pergel (üstten, hafif eğik): N iğne ucu, T kalem ucu; menteşe ikisinin ortasından yukarıda
function a2_dividers(ctx, N, T, lift = 0) {
  const mx = (N[0] + T[0]) / 2, my = (N[1] + T[1]) / 2, Hh = [mx + lift * 30, my - 250 - lift * 40];
  const leg = (A, B, w0, w1) => { const an = Math.atan2(B[1] - A[1], B[0] - A[0]), nx = -Math.sin(an), ny = Math.cos(an); return PL([[A[0] + nx * w0, A[1] + ny * w0], [B[0] + nx * w1, B[1] + ny * w1], [B[0] - nx * w1, B[1] - ny * w1], [A[0] - nx * w0, A[1] - ny * w0]]); };
  // gölge (masada, sağ alta)
  if (lift < .9) { const sh = new Path2D(); for (const B of [N, T]) sh.addPath(leg([Hh[0] + 16 + lift * 60, Hh[1] + 24 + lift * 80], [B[0] + 3, B[1] + 4], 8, 2)); plate(ctx, 'sepia', sh, { a: .22 * (1 - lift) }); }
  for (const [B, pen] of [[N, 0], [T, 1]]) {
    const L = leg(Hh, B, 10, 3); knock(ctx, L); plate(ctx, 'ochre', L, { n: 2 }); inkStroke(ctx, L, 2.4);
    const an = Math.atan2(B[1] - Hh[1], B[0] - Hh[0]);
    cut(ctx, PL([[Hh[0] + Math.cos(an) * 30 - 3, Hh[1] + Math.sin(an) * 30], [B[0] - Math.cos(an) * 40 - 2, B[1] - Math.sin(an) * 40]], false), 2, { a: .7 });
    const tip = [B[0] - Math.cos(an) * 26, B[1] - Math.sin(an) * 26];
    if (pen) { const pc = leg(tip, B, 5, 1.5); knock(ctx, pc); inkFill(ctx, pc); } else inkStroke(ctx, PL([tip, B], false), 2.2);
  }
  const knob = SP([[Hh[0] - 14, Hh[1]], [Hh[0] - 10, Hh[1] - 40], [Hh[0] + 10, Hh[1] - 40], [Hh[0] + 14, Hh[1]]], true, .5);
  knock(ctx, knob); plate(ctx, 'ochre', knob, { n: 2 }); inkStroke(ctx, knob, 2.4); for (let k = 0; k < 5; k++) inkStroke(ctx, PL([[Hh[0] - 11, Hh[1] - 8 - k * 7], [Hh[0] + 11, Hh[1] - 8 - k * 7]], false), 1.4, { a: .7 });
  const hinge = a2_ell(Hh[0], Hh[1] + 4, 18, 14); knock(ctx, hinge); plate(ctx, 'ochre', hinge, { n: 2 }); inkStroke(ctx, hinge, 2.6); inkFill(ctx, a2_ell(Hh[0], Hh[1] + 4, 4, 4));
}
function a2_C03a_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  // masa: sepya ahşap, damarlar
  const desk = a2_R(-140, -140, W + 140, H + 140); plate(g, 'sepia', desk, { a: .62 }); plate(g, 'ochre', desk, { a: .35 });
  const r = rng(301);
  for (let i = 0; i < 30; i++) { const yy = -120 + i * 46 + r() * 12, p = new Path2D(); let x = -140; p.moveTo(x, yy); while (x < W + 140) { const nx = x + 120 + r() * 200; p.quadraticCurveTo((x + nx) / 2, yy + (r() - .5) * 12, nx, yy + (r() - .5) * 5); x = nx; } inkStroke(g, p, 1.5, { a: .3 + r() * .2 }); }
  // lamba ışığı masada (düz halkalar, sol üstte lamba kaynağı)
  for (const [rx, ry, a] of [[900, 640, .0], [700, 500, .0]]) { }
  // defter sayfası (çift sayfa), odağın zemini
  g.save(); g.translate(1010, 560); g.rotate(-.035);
  plate(g, 'ink', a2_R(-650, -400 + 18, 650 + 22, 420 + 18), { a: .35 });
  const pg = PL(rough([[-650, -400], [650, -400], [650, 420], [-650, 420]], 1.4, 302)); knock(g, pg, '#F4ECDA');
  plate(g, 'ochre', a2_R(-650, -400, -40, 420), { a: .07 });
  inkStroke(g, PL([[0, -400], [0, 420]], false), 2); plate(g, 'sepia', a2_R(-14, -400, 0, 420), { a: .25 });
  // sol sayfa: Osmanlıca soyut satırlar ve basılı bir üçgen çizimi
  for (let i = 0; i < 4; i++) scriptLine(g, -60, -330 + i * 34, i === 0 ? 300 : 520, 11, 330 + i, { w: 2, a: .85 });
  const A = [-500, 250], B = [-180, 250], Cc = [-390, 10];
  inkStroke(g, PL([A, B, Cc]), 2, { a: .7 }); inkStroke(g, PL([Cc, [-390, 250]], false), 1.2, { a: .45 }); inkStroke(g, PL([[-402, 250], [-402, 238], [-390, 238]], false), 1.1, { a: .6 });
  const cc = new Path2D(); cc.arc(-382, 168, 82, 0, TAU); inkStroke(g, cc, 1.2, { a: .35 });
  for (const P0 of [A, B, Cc]) inkFill(g, a2_ell(P0[0], P0[1], 5, 5));
  for (let i = 0; i < 3; i++) scriptLine(g, -60, 330 + i * 30 - 30, 440, 9, 340 + i, { w: 1.7, a: .75 });
  // sağ sayfa: kurşun kalemle yardımcı çizgiler (pergelin çalışma alanı)
  for (let i = 0; i < 16; i++) inkStroke(g, PL([[30, -360 + i * 48], [620, -360 + i * 48]], false), 1, { a: .12 });
  scriptLine(g, 600, -330, 260, 10, 350, { w: 1.8, a: .8 });
  g.restore();
  // cetvel, hokka, kitap
  g.save(); g.translate(250, 930); g.rotate(.09);
  const rul = a2_R(-260, -26, 420, 26); knock(g, rul); plate(g, 'ochre', rul, { a: .7 }); inkStroke(g, rul, 2.6);
  for (let i = 0; i < 68; i++) inkStroke(g, PL([[-250 + i * 10, -26], [-250 + i * 10, -26 + (i % 5 ? 10 : 18)]], false), 1.4);
  g.restore();
  const ink0 = SP([[1700, 260], [1640, 250], [1630, 180], [1660, 150], [1740, 150], [1770, 180], [1760, 250]], true, .7); plate(g, 'ink', a2_ell(1712, 268, 80, 20), { a: .35 }); knock(g, ink0); inkFill(g, ink0); cut(g, SP([[1652, 190], [1656, 236]], false), 3, { a: .5 });
  const neck = a2_ell(1700, 150, 30, 9); knock(g, neck); plate(g, 'ochre', neck, { n: 2 }); inkStroke(g, neck, 2);
  g.save(); g.translate(1760, 820); g.rotate(-.2);
  const bk = a2_R(-170, -120, 170, 120); plate(g, 'ink', a2_R(-160, -106, 186, 136), { a: .35 }); knock(g, bk); plate(g, 'navy', bk); plate(g, 'navy', a2_R(-170, -120, -130, 120), { a: .6 }); inkStroke(g, bk, 3);
  inkStroke(g, a2_R(-110, -70, 130, 70), 1.6, { a: .7, col: P.paper });
  g.restore();
}
a2_shot(S('C03'), Wd('C03', 'manastırda'), (ctx, st) => {
  setReg(301);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t);
  const tS = Wd('C03', 'sorgulamayı'), C = [1360, 520], R = 130;
  const cm = a2_camAt(lt, d, { x: W / 2 + 20, y: H / 2, z: 1.0 }, { x: C[0] - 330, y: C[1] + 40, z: 1.07 }, E.io2);
  ctx.save(); cam(ctx, cm, 1);
  ctx.drawImage(a2_cache('c03a-bg', 140, a2_C03a_bg).c, -140, -140, W + 280, H + 280);
  // lamba ışığı (düz okra halkaları, sol üstte kaynak)
  // yay: soldan başlar, tepeden saat yönünde döner (soru işaretinin başı); gövde teğetle devam eder
  const a0 = PI * .98, a1 = PI * 2.22;
  const pd = clamp((tq - S('C03') - .4) / (tS - S('C03') - .5));
  const aNow = lerp(a0, a1, E.io2(pd));
  const arcP = new Path2D(); arcP.arc(C[0], C[1], R, a0, aNow); inkStroke(ctx, arcP, 8);
  const ps = clamp((tq - tS) / .45), E0 = [C[0] + Math.cos(a1) * R, C[1] + Math.sin(a1) * R], tg = [-Math.sin(a1), Math.cos(a1)];
  if (ps > 0) {
    const sp = new Path2D(); sp.moveTo(E0[0], E0[1]); sp.bezierCurveTo(E0[0] + tg[0] * R * .5, E0[1] + tg[1] * R * .5, C[0], C[1] + R * .78, C[0], C[1] + R * 1.12); sp.lineTo(C[0], C[1] + R * 1.42);
    ctx.save(); ctx.setLineDash([320 * E.out2(ps), 9999]); inkStroke(ctx, sp, 8, { cap: 'round' }); ctx.restore();
  }
  const pdot = clamp((tq - tS - .55) / .12);
  if (pdot > 0) { const k = 1 + (1 - pdot) * .6; inkFill(ctx, a2_ell(C[0], C[1] + R * 1.8, 14 * k, 14 * k)); }
  // pergel: çizerken iğne merkezde, kalem yayın ucunda; "sorgulamayı"da kalkar ve noktayı vurup çekilir
  const lift = clamp((tq - tS + .1) / .5);
  if (tq < tS + 1.2) {
    let Nn = C, Tt = [C[0] + Math.cos(aNow) * R, C[1] + Math.sin(aNow) * R];
    if (lift > 0) { const dotP = [C[0], C[1] + R * 1.8], k = E.io2(lift), up = Math.sin(clamp((tq - tS - .3) / .9) * PI) ; Nn = [lerp(C[0], dotP[0], k), lerp(C[1], dotP[1], k) - up * 30]; Tt = [Nn[0] + 120 + k * 60, Nn[1] - 40 - k * 40]; const away = clamp((tq - tS - .75) / .45); Nn = [Nn[0] + away * 900, Nn[1] - away * 500]; Tt = [Tt[0] + away * 900, Tt[1] - away * 500]; }
    a2_dividers(ctx, Nn, Tt, lift);
  }
  ctx.restore();
}, { tr: { type: 'press', dur: .6 } });
