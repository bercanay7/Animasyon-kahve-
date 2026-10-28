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
// (main.js cutRules başlangıcı cümle başından öne alabilir; süre gerçek başlangıçtan hesaplanır)
function a2_shot(at, end, draw, o) { shot(at, (ctx, st) => { const d = end - (st.t - st.lt); draw(ctx, { ...st, d, p: clamp(st.lt / d) }); }, o); }
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
  if (o.text) {
    txt(g, o.text, x + w / 2, y + h / 2 + 2, o.font || FONT.title(Math.round(h * .55)), { align: 'center', base: 'middle', ls: o.ls ?? 2, col });
    if (o.stroke) { g.save(); g.font = o.font; g.textAlign = 'center'; g.textBaseline = 'middle'; g.letterSpacing = (o.ls ?? 2) + 'px'; g.lineWidth = o.stroke; g.strokeStyle = col; g.strokeText(o.text, x + w / 2, y + h / 2 + 2); g.restore(); }
  }
  else if (o.trace === 'osm') scriptLine(g, x + w - 14, y + h * .62, w - 28, h * .32, o.seed || 9, { col, w: Math.max(2, h * .07) });
  else if (o.trace === 'heb') a2_squareTrace(g, x + w - 14, y + h * .7, w - 28, h * .38, o.seed || 9, { col, w: Math.max(2, h * .07) });
}
const a2_HEB = s => `700 ${s}px "Liberation Serif", "FreeSerif", serif`;   // İbrani harfi (sistem fontu; Amiri basmıyor)
const a2_LADINO = 'לה איפוקה';   // La Epoka: Selanik'te çıkan Ladino gazetesi
const a2_GREEK = s => `400 ${s}px "GFS Didot", "Liberation Serif", "FreeSerif", serif`;
// GFS Didot erken yüklensin; yüklenmeden önce kurulmuş önbellek ayrı anahtarla tutulur (yüklenince yenisi kurulur)
try { document.fonts.load('400 40px "GFS Didot"', 'ΚΑΦΕΝΕΙΟΝ ΒΙΒΛΙΟΠΩΛΕΙΟΝ ΦΑΡΟΣ ΤΗΣ ΜΑΚΕΔΟΝΙΑΣ'); } catch (e) { }
const a2_grKey = () => { try { return document.fonts.check('400 40px "GFS Didot"', 'Κ') ? '' : '-fb'; } catch (e) { return ''; } };
// gece istisnası (sanat yönetmeni): lacivert tek baskı, düz (benek yok), a ≤ .85; koyu yüzeyde taş greni .10
const a2_NIGHT = { stone: .1 };
const a2_navy = (g, p, a = .85) => plate(g, 'navy', p, { a: Math.min(a, .85), flat: true });

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
  chapterCard(ctx, 'II', 'SELANİK', '1889 · CUMHURİYET’E 34 YIL', lt, d);
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
  if (o.sign) a2_sign(g, o.sign.x ?? x + (w - o.sign.w) / 2, 486 - 6, o.sign.w, 32 + 4, { seed: o.seed, ...o.sign });
  if (o.topSign) a2_sign(g, x + (w - o.topSign.w) / 2, 34, o.topSign.w, 60, { seed: o.seed + 5, ...o.topSign });
}
function a2_C01b_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-160, -160, W + 320, H + 320);
  // tabelalar kamera kaymasında bile kareden taşmayacak yerde (kenarda yarım kelime kalmaz): Rumca · Fransızca · Ladino · Fransızca · Osmanlıca iz
  a2_facade(g, -170, 470, { seed: 1, wa: .34, sign: { x: 96, w: 196, text: 'ΚΑΦΕΝΕΙΟΝ', font: a2_GREEK(28), ls: 3, stroke: .6, plate: 'ochre', pa: .35 } });
  a2_facade(g, 300, 440, { seed: 2, wa: .2, shade: true, arch: true, sign: { w: 360, text: 'HÔTEL D’ANGLETERRE', font: FONT.title(24), dark: true } });
  a2_facade(g, 740, 460, { seed: 3, wa: .42, n: 2, sign: { w: 300, text: a2_LADINO, font: a2_HEB(30), ls: 1, plate: 'ochre', pa: .25 } });
  a2_facade(g, 1200, 470, { seed: 4, wa: .24, shade: true, arch: true, sign: { w: 370, text: 'BANQUE DE SALONIQUE', font: FONT.title(24), dark: true } });
  a2_facade(g, 1670, 460, { seed: 5, wa: .36, sign: { x: 1690, w: 150, trace: 'osm', dark: true }, awn: 'teal' });
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
  a2_blit(ctx, a2_cache('c01b-bg' + a2_grKey(), 160, a2_C01b_bg), cm, .55);
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
  a2_seaBase(g, hy, H + 160, { a: .74, ht: false });   // C02: düz turkuaz deniz, yarım ton yok
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
  ctx.save(); ctx.translate(-Math.max(0, turn) * 5, -up * 6); ctx.rotate(turn * .08 - up * .04);
  // kulaklar (dönüşe göre)
  for (const sd of [-1, 1]) {
    const ex = sd * (44 - sd * turn * 6), ear = SP([[ex, -8], [ex + sd * 10, -12], [ex + sd * 13, 4], [ex + sd * 8, 20], [ex, 18]], true, .8);
    knock(ctx, ear); plate(ctx, 'ochre', ear, { a: .3 }); inkStroke(ctx, ear, lw(2.2)); inkStroke(ctx, SP([[ex + sd * 4, -4], [ex + sd * 8, 6], [ex + sd * 4, 14]], false), lw(1.2));
  }
  // yanak (sağa dönünce sağda belirir)
  if (turn > .1) {
    const ch = SP([[30, -6], [48 + turn * 10, 0], [50 + turn * 10, 14], [46 + turn * 10, 30], [30, 34]], true, .8); knock(ctx, ch); plate(ctx, 'ochre', ch, { a: .25 });
    if (turn > .6) { // kayıp profil: burun ucu yanak çizgisinin ötesine taşar, kirpik ve kaş ucu görünür
      const k = clamp((turn - .6) / .4), bx = 49 + turn * 10;
      const nose = SP([[bx - 2, 4], [bx + 9 * k, 12], [bx + 7 * k, 17], [bx - 2, 19]], true, .7); knock(ctx, nose); plate(ctx, 'ochre', nose, { a: .25 }); inkStroke(ctx, SP([[bx - 1, 4], [bx + 9 * k, 12], [bx + 7 * k, 17], [bx - 1, 19]], false, .7), lw(2.2));
      inkStroke(ctx, SP([[bx - 8, -4], [bx - 2 + 3 * k, -6], [bx + 1 + 4 * k, -3]], false), lw(2.2));          // kirpik
      inkFill(ctx, SP([[bx - 12, -16], [bx + 2 * k, -18], [bx + 2 * k, -15], [bx - 12, -13]], true), { a: k }); // kaş ucu
      inkStroke(ctx, SP([[bx - 2, 19], [bx - 4, 26], [bx - 6, 32]], false), lw(1.8));
    }
    inkStroke(ctx, SP([[30, -6], [48 + turn * 10, 0], [50 + turn * 10, 14]], false), lw(2.2)); inkStroke(ctx, SP([[46 + turn * 10, 22], [44 + turn * 10, 30], [36, 34]], false), lw(2.2));
  }
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
  a2_waves(ctx, hy, 905, t, { seed: 21, rows: 20, speed: .7 });
  a2_steamer(ctx, 1640 - lt * 7, hy + 6, .3, -1, t, { seed: 5 });
  a2_sailboat(ctx, 420 + lt * 5, hy + 70, .5, t);
  for (let i = 0; i < 3; i++) a2_gull(ctx, 900 + i * 140 + lt * (18 + i * 6), 300 + i * 40 + Math.sin(t + i) * 10, 1.1, Math.floor(t * 5 + i) % 2);
  ctx.restore();
  // ön plan: rıhtım taşı üstünde çocuk ve gazete destesi; baba direği (bollard)
  ctx.save(); cam(ctx, cm, 1);
  a2_bundle(ctx, 470, 902, 1.1);
  const bol = SP([[1438, 906], [1446, 860], [1440, 842], [1420, 834], [1424, 818], [1470, 812], [1516, 818], [1520, 834], [1500, 842], [1494, 860], [1502, 906]], true, .5); knock(ctx, bol); inkFill(ctx, bol); cut(ctx, SP([[1428, 824], [1470, 820], [1512, 824]], false), 2, { a: .6 }); cut(ctx, PL([[1452, 856], [1450, 900]], false), 2, { a: .4 });
  const rope = new Path2D(); for (let k = 0; k < 4; k++) rope.ellipse(1600, 896 - k * 10, 90 - k * 8, 16, 0, 0, TAU); knock(ctx, a2_ell(1600, 880, 92, 34)); inkStroke(ctx, rope, 3); plate(ctx, 'ochre', a2_ell(1600, 880, 92, 34), { a: .35 });
  // rüzgâr desteden bir gazeteyi kaldırır ("filizlendi"den sonra), sağ üste uçar — C02b'nin uçuşan gazetelerine bağlanır
  const tW = Wd('C02', 'filizlendi'), fw = clamp((tq - tW) / 1.4);
  if (fw > 0) { const fx = lerp(470, 1500, E.in2(fw)), fy = lerp(860, 180, E.out2(fw)) + Math.sin(fw * 9) * 30; a2_newspaper(ctx, fx, fy, 200, 260, -.2 + fw * 1.1, 'fr', Math.sin(tq * 7), { age: .1 }); }
  const turn = kf(tq - tW, [[-3.7, -.15], [-2.3, .45], [-.1, .45], [.35, .95], [.9, 1.0]]);
  a2_childBack(ctx, 800, hy + 4 + Math.sin(tq * 1.5) * 1.5, 1.39, { turn, up: kf(tq - tW, [[0, 0], [.6, .6]]), ph: Math.floor(t * 4) % 2 });
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
  else if (kind === 'lad') txt(ctx, a2_LADINO, 0, my, a2_HEB(Math.round(w * .1)), { align: 'center', base: 'middle', plate: 'navy' });
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
  a2_waves(ctx, hy, 916, t, { seed: 23, rows: 14, speed: .7 });
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
  const tO = Wd('C02', 'öğrenir'), tq2 = a2_q(t);
  const cTurn = kf(tq2 - tO, [[-3.4, .35], [-2.2, .55], [-1.2, .3], [-.25, .3], [.3, 1.0]]), cUp = kf(tq2 - tO, [[-3.4, .9], [-2.2, .6], [-1.2, 1], [-.25, 1], [.3, .25]]);
  a2_childBack(ctx, 300, hy + 4, .92, { turn: cTurn, up: cUp, ph: Math.floor(t * 4) % 2 });
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

// C03b: gece yatakhane (lacivert), tek nokta perspektif; yat borusunda lamba söner, "yasak kitaplar"da bir yorgan mumla ışır
const a2_VP = [960, 500], a2_F = 900;
const a2_pj = (X, Y, Z) => [a2_VP[0] + X / Z * a2_F, a2_VP[1] + Y / Z * a2_F];   // Y aşağı (+), göz yüksekliği 0, zemin Y=1.55
// a2_LIT: ışık havuzu sürümü (aynı çizim, lacivert ~%30, üstüne altın .25) — mumun aydınlattığı bölge bu sürümden kırpılır
let a2_LIT = 0;
const a2_nv = a => a2_LIT ? a * .45 : a;
function a2_bed(g, X0, X1, Z0, Z1, o = {}) {
  // X0: duvar tarafı (baş), X1: ayak ucu; Z0 yakın, Z1 uzak kenar. Demir: ay ışığını alan kazıma çizgi
  const yF = 1.55, yM = 1.0, P_ = (x, y, z) => a2_pj(x, y, z), lw = Math.max(1.3, 6 / Z0), ws = Math.sign(X0);
  const top = PL([P_(X0, yM, Z0), P_(X1, yM, Z0), P_(X1, yM, Z1), P_(X0, yM, Z1)]);
  const front = PL([P_(X0, yM, Z0), P_(X1, yM, Z0), P_(X1, yM + .28, Z0), P_(X0, yM + .28, Z0)]);
  const side = PL([P_(X1, yM, Z0), P_(X1, yM, Z1), P_(X1, yM + .28, Z1), P_(X1, yM + .28, Z0)]);
  for (const q of [side, front, top]) knock(g, q);
  a2_navy(g, side, a2_nv(.85)); plate(g, 'ink', side, { a: a2_nv(.25), flat: true }); a2_navy(g, front, a2_nv(.85)); plate(g, 'ink', front, { a: a2_nv(.4), flat: true }); a2_navy(g, top, a2_nv(.72));
  // yastık ve uyuyan
  const pil = PL([P_(X0 - ws * .06, yM - .03, Z0 + .1), P_(X0 - ws * .5, yM - .05, Z0 + .1), P_(X0 - ws * .5, yM - .05, Z1 - .1), P_(X0 - ws * .06, yM - .03, Z1 - .1)]);
  knock(g, pil); a2_navy(g, pil, a2_nv(.4)); cut(g, pil, lw * .6, { a: .5 });
  if (o.sleeper !== false) {
    const zc = (Z0 + Z1) / 2, hd = P_(X0 - ws * .3, yM - .1, zc), r = .12 / zc * a2_F;
    inkFill(g, a2_ell(hd[0], hd[1], r * 1.05, r * .8));
    const hump = SP([P_(X0 - ws * .5, yM, Z0 + .06), P_(X0 - ws * .7, yM - .2, zc), P_(X0 - ws * 1.3, yM - .15, zc), P_(X1 + ws * .02, yM - .05, zc), P_(X1 + ws * .02, yM, Z0 + .04)], true, .8);
    knock(g, hump); a2_navy(g, hump, a2_nv(.85)); plate(g, 'ink', hump, { a: a2_nv(.15), flat: true }); cut(g, hump, lw * .7, { a: .45 });
  }
  cut(g, PL([P_(X0, yM + .06, Z0), P_(X1, yM + .06, Z0)], false), lw * .6, { a: .35 });
  // demir başlık ve ayak demiri (kazıma)
  const hb = new Path2D();
  for (const z of [Z0, Z1]) { const a = P_(X0, yF, z), b = P_(X0, .3, z); hb.moveTo(a[0], a[1]); hb.lineTo(b[0], b[1]); }
  for (const y of [.3, .58]) { const a = P_(X0, y, Z0), b = P_(X0, y, Z1); hb.moveTo(a[0], a[1]); hb.lineTo(b[0], b[1]); }
  for (let k = 1; k < 5; k++) { const z = lerp(Z0, Z1, k / 5), a = P_(X0, .3, z), b = P_(X0, .58, z); hb.moveTo(a[0], a[1]); hb.lineTo(b[0], b[1]); }
  for (const z of [Z0, Z1]) { const a = P_(X1, yF, z), b = P_(X1, .74, z); hb.moveTo(a[0], a[1]); hb.lineTo(b[0], b[1]); }
  { const a = P_(X1, .74, Z0), b = P_(X1, .74, Z1); hb.moveTo(a[0], a[1]); hb.lineTo(b[0], b[1]); }
  inkStroke(g, hb, lw * 1.5); cut(g, hb, lw * .55, { a: .55 });
}
function a2_C03b_bg(g, lit = 0) {
  a2_LIT = lit;
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  const Zb = 17, wl = -4.2, wr = 4.2, yC = -2.7, yF = 1.55;
  const BW = PL([a2_pj(wl, yC, Zb), a2_pj(wr, yC, Zb), a2_pj(wr, yF, Zb), a2_pj(wl, yF, Zb)]);
  const LW = PL([[-140, -140 * 3], a2_pj(wl, yC, Zb), a2_pj(wl, yF, Zb), [-140, H + 140]]), RW = PL([[W + 140, -140 * 3], a2_pj(wr, yC, Zb), a2_pj(wr, yF, Zb), [W + 140, H + 140]]);
  const CE = PL([[-140, -140], [W + 140, -140], a2_pj(wr, yC, Zb), a2_pj(wl, yC, Zb)]), FL = PL([[-140, H + 140], [W + 140, H + 140], a2_pj(wr, yF, Zb), a2_pj(wl, yF, Zb)]);
  // lacivert tek baskı, düz; yüzeyler arası fark yalnız tonla
  a2_navy(g, LW, a2_nv(.85)); a2_navy(g, RW, a2_nv(.7)); a2_navy(g, CE, a2_nv(.85)); plate(g, 'ink', CE, { a: a2_nv(.3), flat: true }); a2_navy(g, BW, a2_nv(.62)); a2_navy(g, FL, a2_nv(.75)); plate(g, 'sepia', FL, { a: .2, flat: true });
  for (let z = 2.2; z < Zb; z += 1.6) { const a = a2_pj(wl, yC, z), b = a2_pj(wr, yC, z); cut(g, PL([a, b], false), Math.max(1.2, 6 / z), { a: .22 }); }
  for (let x = -4.2; x <= 4.21; x += .45) { const a = a2_pj(x, yF, 1.2), b = a2_pj(x, yF, Zb); inkStroke(g, PL([a, b], false), 1.4, { a: .4 }); }
  inkStroke(g, BW, 2.4);
  for (const [a, b] of [[a2_pj(wl, yC, Zb), a2_pj(wl, yC, .9)], [a2_pj(wr, yC, Zb), a2_pj(wr, yC, .9)], [a2_pj(wl, yF, Zb), a2_pj(wl, yF, 1.1)], [a2_pj(wr, yF, Zb), a2_pj(wr, yF, 1.1)]]) inkStroke(g, PL([a, b], false), 2.6);
  for (let z = 3.4; z < Zb - 1; z += 2.8) {
    const zz = [z, z + 1.1], top = -2.1, bot = -.3, zm = (zz[0] + zz[1]) / 2;
    // ay ışığı: pencereden koridora düşen kâğıt renginde şerit (altın .25)
    const strip = PL([a2_pj(-2.1, yF, zz[0] + .35), a2_pj(2.0, yF, zz[0] + 1.5), a2_pj(2.0, yF, zz[1] + 2.7), a2_pj(-2.1, yF, zz[1] + 1.45)]);
    knock(g, strip); plate(g, 'gold', strip, { a: .25, flat: true }); if (a2_LIT) plate(g, 'gold', strip, { a: .1, flat: true });
    // karşı duvara düşen pencere biçimli ay lekesi
    const zr = [zz[0] + 3.0, zz[1] + 3.9], rw = SP([a2_pj(wr, bot + .62, zr[0]), a2_pj(wr, top + .6, zr[0]), a2_pj(wr, top + .35, (zr[0] + zr[1]) / 2), a2_pj(wr, top + .6, zr[1]), a2_pj(wr, bot + .62, zr[1])], true, .5);
    knock(g, rw, '#ECE6D6'); plate(g, 'gold', rw, { a: .16, flat: true });
    const win = SP([a2_pj(wl, bot, zz[0]), a2_pj(wl, top + .35, zz[0]), a2_pj(wl, top, zm), a2_pj(wl, top + .35, zz[1]), a2_pj(wl, bot, zz[1])], true, .5);
    knock(g, win, '#E9E4D6'); a2_navy(g, win, .18);
    const bars = new Path2D(); for (const q of [[a2_pj(wl, top + .05, zm), a2_pj(wl, bot, zm)], [a2_pj(wl, -1.2, zz[0]), a2_pj(wl, -1.2, zz[1])]]) { bars.moveTo(q[0][0], q[0][1]); bars.lineTo(q[1][0], q[1][1]); }
    inkStroke(g, bars, Math.max(1.4, 9 / z)); inkStroke(g, win, Math.max(1.8, 12 / z));
    if (z < 4) { const m = a2_pj(wl, -1.75, zz[0] + .35); knock(g, a2_ell(m[0], m[1], 26, 26), '#F4F1E6'); inkStroke(g, a2_ell(m[0], m[1], 26, 26), 2); }
  }
  for (let i = 9; i >= 0; i--) {
    const z0 = 2.6 + i * 1.45;
    a2_bed(g, wl + .05, wl + 2.05, z0, z0 + .95, { sleeper: i !== 2 });
    a2_bed(g, wr - .05, wr - 2.05, z0, z0 + .95, { sleeper: true });
  }
  if (lit) plate(g, 'gold', a2_R(-140, -140, W + 140, H + 140), { a: .25, flat: true });
  a2_LIT = 0;
}
function a2_C03b_light(g, on, t) {
  // arka duvardaki asma lamba (yanarken düz okra halkalar, lambanın kendi çevresi)
  const L = a2_pj(0, -1.6, 15.6), T0 = a2_pj(0, -2.7, 15.6);
  inkStroke(g, PL([[L[0], T0[1]], L], false), 2); cut(g, PL([[L[0], T0[1]], L], false), .8, { a: .4 });
  if (on) for (const [r, col, sd] of [[120, '#C9B48B', 1], [76, '#DCCAA3', 2], [40, '#EFE3C4', 3]]) knock(g, a2_roughCircle(L[0], L[1] + 14, r, 860 + sd, .03, 28), col);
  const sh = PL([[L[0] - 24, L[1]], [L[0] + 24, L[1]], [L[0] + 12, L[1] - 16], [L[0] - 12, L[1] - 16]]); knock(g, sh); a2_navy(g, sh); cut(g, sh, 1.4, { a: .5 });
  const gl = a2_ell(L[0], L[1] + 12, 9, 12); knock(g, gl, on ? '#F6EFDD' : P.paperD); if (!on) a2_navy(g, gl); inkStroke(g, gl, 1.8);
}
// kırık kenarlı daire (ışık havuzu)
function a2_roughCircle(cx, cy, r, seed, amp = .035, n = 28) { const pts = []; for (let i = 0; i < n; i++) { const a = i / n * TAU; pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } return SP(rough(pts, r * amp, seed), true, .9); }
// yorgan çadırı: yatağın üstüne oturan kubbe; içten mumla ışır, ayak ucundaki aralıktan ışık sızar
function a2_quiltTent(ctx, X0, X1, z0, Z1, glow, fl) {
  const zc = (z0 + Z1) / 2, yM = 1.0, P_ = (x, y, z) => a2_pj(x, y, z);
  const tent = SP([P_(X0 + .02, yM + .04, z0 - .04), P_(X0 + .15, .52, z0 + .15), P_(X0 + .9, .34, zc), P_(X1 - .25, .5, z0 + .2), P_(X1 + .04, yM + .06, z0 - .04)], true, .75);
  knock(ctx, tent);
  if (glow > 0) { knock(ctx, tent, '#F1E6CA'); plate(ctx, 'gold', tent, { a: .3, flat: true }); if (glow < 1) a2_navy(ctx, tent, .85 * (1 - glow)); }
  else a2_navy(ctx, tent, .85);
  // kıvrımlar (ışıkta is, karanlıkta kazıma)
  const folds = [[P_(X0 + .9, .36, zc), P_(X0 + .5, .7, z0 + .05), P_(X0 + .3, yM, z0 - .03)], [P_(X0 + .95, .36, zc), P_(X0 + 1.2, .72, z0 + .05), P_(X0 + 1.35, yM, z0 - .03)], [P_(X0 + .7, .4, zc), P_(X0 + .2, .62, z0 + .1)]];
  for (const q of folds) glow > 0 ? inkStroke(ctx, SP(q, false), 2.2, { a: .5 }) : cut(ctx, SP(q, false), 1.8, { a: .4 });
  // yorgan dikişleri (kesik eğriler)
  ctx.save(); ctx.clip(tent); ctx.setLineDash([7, 6]);
  for (let k = 0; k < 6; k++) { const u = k / 5; const q = SP([P_(lerp(X0 + .1, X1 - .1, u), yM, z0 - .04), P_(lerp(X0 + .5, X1 - .6, u), .5, zc), P_(lerp(X0 + .4, X1 - .5, u), .3, Z1)], false); glow > 0 ? inkStroke(ctx, q, 1.6, { a: .45, cap: 'butt' }) : cut(ctx, q, 1.4, { a: .3, cap: 'butt' }); }
  ctx.restore();
  if (glow > 0) {
    // ayak ucundaki aralık: kâğıt ışık + mum alevi
    const gap = SP([P_(X1 - .3, yM + .02, z0 - .02), P_(X1 - .22, .7, z0 + .05), P_(X1 - .06, .74, z0 + .02), P_(X1 + .02, yM + .04, z0 - .03)], true, .7);
    knock(ctx, gap, '#F8F1DE'); const fc = P_(X1 - .16, .9, z0 + .02), fh = 20 * fl;
    const flame = SP([[fc[0], fc[1] - fh], [fc[0] + 5, fc[1] - fh * .35], [fc[0], fc[1]], [fc[0] - 5, fc[1] - fh * .35]], true, .9); plate(ctx, 'ochre', flame, { n: 2 }); inkStroke(ctx, flame, 1.4);
    inkStroke(ctx, gap, 2);
    // ışık yere ve koridora düşer (düz okra leke)
    const spill = PL([P_(X1 + .02, 1.55, z0 - .1), P_(X1 + 1.6 * fl, 1.55, z0 - .5), P_(X1 + 1.8 * fl, 1.55, Z1 + .3), P_(X1 + .02, 1.55, Z1)]);
    knock(ctx, spill, '#D6C49C'); plate(ctx, 'gold', spill, { a: .2 * glow, flat: true });
  }
  inkStroke(ctx, tent, 3.2);
}
a2_shot(Wd('C03', 'manastırda'), Wd('C03', 'elden'), (ctx, st) => {
  setReg(302);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t);
  const tOff = Wd('C03', 'yat'), tBook = Wd('C03', 'yasak');
  const cm = a2_camAt(lt, d, { x: W / 2, y: H / 2, z: 1.0 }, { x: W / 2 - 70, y: H / 2 + 30, z: 1.07 });
  ctx.save(); cam(ctx, cm, 1);
  ctx.drawImage(a2_cache('c03b-bg', 140, a2_C03b_bg).c, -140, -140, W + 280, H + 280);
  const on = t < tOff + .5;
  a2_C03b_light(ctx, on, t);
  // yorgan altında mum (2. sol yatak): "yasak kitaplar"da içten ışır; çevresine r 260 altın ışık havuzu (aynı sahnenin aydınlık sürümü kırpılır) — odak
  const z0 = 2.6 + 2 * 1.45, wl = -4.2;
  const glow = ramp(t, tBook - .1, tBook + .45), fl = .88 + .12 * Math.sin(tq * 23) * Math.sin(tq * 7);
  if (glow > 0) {
    const c = a2_pj(wl + 1.1, .55, z0 + .3);
    ctx.save(); ctx.clip(a2_roughCircle(c[0], c[1] + 20, 260 * (.55 + .45 * E.out2(glow)) * (.97 + .03 * fl), 311));
    ctx.drawImage(a2_cache('c03b-lit', 140, g => a2_C03b_bg(g, 1)).c, -140, -140, W + 280, H + 280);
    ctx.restore();
  }
  a2_quiltTent(ctx, wl + .05, wl + 2.05, z0, z0 + .95, glow, fl);
  ctx.restore();
  // yer damgaları (kelimeye bağlı)
  stamp(ctx, 'MANASTIR', 80, 128, t - Wd('C03', 'manastırda'), d, { size: 48 });
  stamp(ctx, 'HARBİYE', 430, 128, t - Wd('C03', 'harbiyede'), d, { size: 48 });
}, { tr: { type: 'press', dur: .5 }, post: a2_NIGHT });

// C03c: yorgan altında yakın plan — mum, iki öğrenci (anonim), elden ele geçen ve açılan yasak kitap; Namık Kemal… vatan… hürriyet…
function a2_C03c_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-120, -120, W + 240, H + 240);
  const cx = 960, cy = 640;
  // yorganın iç yüzü: lacivert tek baskı (düz); ışık yalnız mumun çevresinde: kırık kenarlı üç düz halka
  const all = a2_R(-120, -120, W + 120, H + 120);
  a2_navy(g, all, .85);
  for (const [r, col, sd] of [[300, '#BEA982', 1], [200, '#D8C59E', 2], [120, '#EFE3C4', 3]]) knock(g, a2_roughCircle(cx, cy, r, 330 + sd, .025, 36), col);
  // yorgan plileri ve dikişleri (kazıma: karanlık kütlede açık çizgi)
  const r = rng(331);
  for (let i = 0; i < 14; i++) { const x0 = -60 + i * 150 + r() * 40, q = SP([[x0, -120], [x0 + (r() - .5) * 80, 160], [x0 + (cx - x0) * .2 + (r() - .5) * 40, 440]], false); cut(g, q, 2, { a: .16 }); }
  g.save(); g.setLineDash([12, 10]);
  for (let k = 0; k < 4; k++) { const q = new Path2D(); q.ellipse(cx, -260, 700 + k * 300, 420 + k * 130, 0, .12, PI - .12); cut(g, q, 1.6, { a: .14, cap: 'butt' }); }
  g.restore();
}
// çarşaf (öndeki şilte yüzü): mumun önü açık, kenarlar lacivert
function a2_C03c_sheet(g) {
  const sheet = SP([[-120, 786], [500, 774], [1000, 780], [1500, 770], [W + 120, 784], [W + 120, H + 120], [-120, H + 120]], true, .6);
  knock(g, sheet); a2_navy(g, sheet, .85);
  g.save(); g.clip(sheet);
  for (const [rx, ry, col, a] of [[760, 330, '#9C8C70', 1], [560, 250, '#C9B48C', 1], [380, 180, '#E9DEC4', 1]]) knock(g, a2_ell(960, 800, rx, ry), col);
  plate(g, 'ochre', a2_ell(960, 800, 380, 180), { a: .14 });
  g.restore();
  inkStroke(g, SP([[-120, 786], [500, 774], [1000, 780], [1500, 770], [W + 120, 784]], false, .6), 3);
  for (const q of [[[260, 830], [480, 900], [640, 1080]], [[1360, 840], [1480, 930], [1580, 1080]]]) inkStroke(g, SP(q, false), 1.8, { a: .35 });
}
function a2_candle(ctx, x, y, tq) {
  // teneke şamdan + mum + alev (alev ikişer karede biçim değiştirir)
  const dish = a2_ell(x, y, 70, 16); plate(ctx, 'ink', a2_ell(x + 10, y + 8, 76, 16), { a: .3 }); knock(ctx, dish); plate(ctx, 'ochre', dish, { n: 2 }); inkStroke(ctx, dish, 2.6);
  const hd = SP([[x + 64, y - 2], [x + 98, y - 18], [x + 104, y - 6], [x + 70, y + 8]], true, .6); knock(ctx, hd); plate(ctx, 'ochre', hd, { n: 2 }); inkStroke(ctx, hd, 2.2);
  const stick = SP([[x - 18, y - 2], [x - 18, y - 120], [x - 10, y - 126], [x + 4, y - 122], [x + 18, y - 128], [x + 18, y - 2]], true, .4); knock(ctx, stick, '#F6EEDA'); plate(ctx, 'ochre', a2_R(x + 6, y - 130, x + 18, y), { a: .35 }); inkStroke(ctx, stick, 2.4);
  inkStroke(ctx, SP([[x - 4, y - 124], [x - 6, y - 104], [x - 2, y - 92]], false), 2.4); // eriyen mum damlası
  inkStroke(ctx, PL([[x, y - 124], [x + 1, y - 138]], false), 2.4);
  const k = Math.sin(tq * 31) * .5 + Math.sin(tq * 13) * .5, fh = 64 + k * 10, sway = Math.sin(tq * 17) * 5;
  const flame = SP([[x + sway * 1.4, y - 138 - fh], [x + 13, y - 138 - fh * .38], [x + 9, y - 132], [x, y - 128], [x - 9, y - 132], [x - 13, y - 138 - fh * .38]], true, .9);
  knock(ctx, flame, '#FBF6E8'); plate(ctx, 'ochre', SP([[x + 9, y - 134], [x, y - 128], [x - 9, y - 134], [x, y - 160]], true, .8), { n: 2, a: .8 }); inkStroke(ctx, flame, 2.2);
}
function a2_book(ctx, x, y, w, h, rot, open, seed) {
  // open 0: kapalı (lacivert kapak, soyut sırt yazısı); 1: açık (iki sayfa, Osmanlıca soyut satırlar)
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  if (open < .5) {
    plate(ctx, 'ink', a2_R(-w / 2 + 8, -h / 2 + 10, w / 2 + 8, h / 2 + 10), { a: .35 });
    const c = a2_R(-w / 2, -h / 2, w / 2, h / 2); knock(ctx, c); plate(ctx, 'sepia', c, { n: 2 }); inkStroke(ctx, c, 2.6);
    inkStroke(ctx, a2_R(-w / 2 + 10, -h / 2 + 10, w / 2 - 10, h / 2 - 10), 1.4, { col: P.ochre, a: .8 });
    scriptLine(ctx, w * .3, -h * .08, w * .6, h * .1, seed, { col: '#E8C98A', w: 2.2 });
  } else {
    const pw = w * .95, ph = h;
    plate(ctx, 'ink', PL([[-pw + 10, -ph / 2 + 14], [pw + 10, -ph / 2 + 14], [pw + 10, ph / 2 + 14], [-pw + 10, ph / 2 + 14]]), { a: .35 });
    const cov = PL([[-pw - 10, -ph / 2 - 8], [pw + 10, -ph / 2 - 8], [pw + 10, ph / 2 + 8], [-pw - 10, ph / 2 + 8]]); knock(ctx, cov); plate(ctx, 'sepia', cov, { n: 2 }); inkStroke(ctx, cov, 2.4);
    const L = SP([[-pw, -ph / 2], [-pw * .5, -ph / 2 - 10], [0, -ph / 2 + 4], [0, ph / 2], [-pw * .5, ph / 2 - 6], [-pw, ph / 2]], true, .4), R = SP([[pw, -ph / 2], [pw * .5, -ph / 2 - 10], [0, -ph / 2 + 4], [0, ph / 2], [pw * .5, ph / 2 - 6], [pw, ph / 2]], true, .4);
    for (const q of [L, R]) { knock(ctx, q, '#FBF5E6'); inkStroke(ctx, q, 2.2); }
    plate(ctx, 'ochre', a2_R(-24, -ph / 2, 0, ph / 2), { a: .3 });
    for (let i = 0; i < 9; i++) { const yy = -ph / 2 + 30 + i * (ph - 50) / 9; scriptLine(ctx, -16, yy, pw - 40, 9, seed + i, { w: 1.8 }); scriptLine(ctx, pw - 20, yy, pw - 40, 9, seed + 40 + i, { w: 1.8 }); }
  }
  ctx.restore();
}
a2_shot(Wd('C03', 'elden'), S('C04'), (ctx, st) => {
  setReg(303);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t), lq = a2_q(lt);
  const cm = a2_camAt(lt, d, { x: W / 2, y: H / 2 + 10, z: 1.0 }, { x: W / 2, y: H / 2 + 50, z: 1.06 });
  ctx.save(); cam(ctx, cm, .6); ctx.drawImage(a2_cache('c03c-bg', 120, a2_C03c_bg).c, -120, -120, W + 240, H + 240); ctx.restore();
  ctx.save(); cam(ctx, cm, 1);
  // kitap çarşafın üstünde soldakinden sağdakine kayar (elden ele), sonra mumun önünde açılır
  const pass = E.io2(clamp(lq / .95)), down = E.io2(clamp((lq - 1.1) / .45));
  const bx = lerp(lerp(770, 1130, pass), 960, down), by = lerp(868, 905, down), open = down > .5 ? 1 : 0;
  const look = [bx, by - 30];
  // öğrenciler yüzüstü, dirsekler şiltede: baş ve omuz; gövde şiltenin arkasında kalır
  const SL = { x: 556, y: 520, s: 1.5, dir: 1 }, SR = { x: 1372, y: 530, s: 1.5, dir: -1 };   // halka kenarı ile yüz arası ≥60 px
  const lHold = lq < .62, rHold = lq > .4 && down < .9;
  bust(ctx, { ...SL, coat: 'setre', col: 'paperD', w: .92, seed: 71, len: 190, turn: .55, tilt: .12 });
  head3q(ctx, { ...SL, who: 'anon', id: { mus: 'faint', seed: 71, jaw: .98, WD: 1.04, hair: 'ink' }, gear: null, light: 'front', lookAt: look, age: 18, tilt: .1 });
  bust(ctx, { ...SR, coat: 'setre', col: 'paperD', w: .92, seed: 73, len: 190, turn: .55, tilt: -.1 });
  head3q(ctx, { ...SR, who: 'anon', id: { mus: null, seed: 73, jaw: 1.06, WD: 1.12, brow: .14, hair: 'sepia' }, gear: null, light: 'front', lookAt: look, age: 17, tilt: -.08 });
  // yorganın iki yana inen kenarları: sırtlarını örter (yorganın altındalar)
  for (const sd of [-1, 1]) {
    const m = q => q.map(([x, y]) => [sd < 0 ? x : W - x, y]);
    const dr = SP(m([[-160, -160], [300, -160], [372, 180], [420, 440], [470, 690], [492, 800], [-160, 800]]), true, .8);
    knock(ctx, dr); a2_navy(ctx, dr, .85); plate(ctx, 'ink', dr, { a: .18, flat: true });
    for (const q of [[[180, 0], [260, 380], [330, 790]], [[60, 120], [110, 500], [160, 790]]]) cut(ctx, SP(m(q), false), 2, { a: .22 });
    inkStroke(ctx, SP(m([[300, -160], [372, 180], [420, 440], [470, 690], [492, 800]]), false, .8), 3);
  }
  ctx.drawImage(a2_cache('c03c-sheet', 120, a2_C03c_sheet).c, -120, -120, W + 240, H + 240);
  a2_candle(ctx, 960, 792, tq);
  // ön kollar şiltede: soldaki kitabı iter ve bırakır; sağdaki alır
  const lHand = lHold ? [bx - 96, by + 6] : [800, 930], rHand = rHold ? [bx + 96, by + 8] : [1124, 940];
  const aL = arm(ctx, [650, 770], lHand, { upper: 120, fore: 150, w: 54, col: 'paperD', bend: -1 });
  const aR = arm(ctx, [1276, 776], rHand, { upper: 120, fore: 150, w: 54, col: 'paperD', bend: 1 });
  a2_book(ctx, bx, by, open ? 150 : 132, 172, open ? 0 : -.1 + pass * .2, open, 341);
  handDraw(ctx, aL.wr[0], aL.wr[1], aL.ang, aL.w2 / 22, lHold ? 'hold' : 'rest', { side: -1 });
  handDraw(ctx, aR.wr[0], aR.wr[1], aR.ang, aR.w2 / 22, rHold ? 'hold' : 'rest', { side: 1 });
  ctx.restore();
  // fısıldanan sözler: kelimesi duyulduğu an, tek tek (izleyici katmanı, Cormorant italik)
  if (!NOTEXT) {
    const parts = [['Namık Kemal…', 'namık'], ['vatan…', 'vatan'], ['hürriyet…', 'hürriyet']], fs = 96, gap = 56;
    ctx.save(); ctx.font = FONT.quote(fs); const ws = parts.map(p => ctx.measureText(p[0]).width); ctx.restore();
    let x = W / 2 - (ws.reduce((a, b) => a + b, 0) + gap * 2) / 2;
    parts.forEach(([s, w], i) => { const k = a2_in(t, Wd('C03', w), .45); if (k > 0) label(ctx, s, x, 196 - (1 - k) * 14, FONT.quote(fs), { col: '#F3E6C6', a: k }); x += ws[i] + gap; });
  }
}, { tr: { type: 'cut' }, post: a2_NIGHT });

// ——————————————————————————————————————— profil siluet (C04, C05, C06) ———
// profil büst siluet (is): baş merkezi (x,y), s ölçek (baş ≈ 120·s), dir yüz yönü; fes kırmızı vurgu; ön yüzde kazıma ışık çizgisi
// o: {len (birim), fes, mus, rim, col ('ink'|'navy'), tilt, reach: [dünyaX, dünyaY] (uzanan kol), ear: kulak arkasına el (hafiye)}
function a2_profile(ctx, x, y, s, dir, o = {}) {
  const L = o.len || 330;
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.tilt || 0); ctx.scale(s * dir, s);
  const lw = px => px / s;
  const bw = o.bow || 0, cb = Math.cos(bw), sb = Math.sin(bw), B = q => q.map(([u, v]) => v > 66 ? [u, v] : [u * cb - (v - 72) * sb, 72 + u * sb + (v - 72) * cb]);
  const face = B([[-8, -62], [14, -60], [27, -48], [31, -32], [33, -17], [37, -8], [47, 7], [49, 13], [40, 17], [41, 23], [37, 27], [40, 33], [36, 39], [34, 49], [24, 57], [12, 61], [12, 76]]);
  const body = B([[30, 92], [58, 112], [66, 190], [64, L], [-104, L], [-106, 190], [-94, 118], [-62, 94], [-34, 80], [-30, 64], [-44, 40], [-54, 10], [-54, -24], [-42, -50], [-26, -60]]);
  const p = SP(rough([...face, ...body], .3, o.seed || 1), true, .55);
  const fill = q => o.col === 'navy' ? (a2_navy(ctx, q, .85), plate(ctx, 'ink', q, { a: .4, flat: true })) : inkFill(ctx, q);
  knock(ctx, p); fill(p);
  if (o.collar) { const c = SP([[-40, 70], [-56, 30], [-30, 40], [-6, 66], [20, 76], [26, 96], [-10, 104]], true, .7); knock(ctx, c); fill(c); cut(ctx, SP([[-50, 34], [-20, 66], [18, 86]], false), lw(2.4), { a: .45 }); }
  if (o.mus) inkFill(ctx, SP(B([[33, 20], [44, 22], [46, 27], [36, 26]]), true, .8));
  // ön yüzde ışık çizgisi (lamba önde)
  if (o.rim !== false) cut(ctx, SP(face.slice(1, 15), false, .55), lw(3), { a: .75 });
  if (o.rim !== false) cut(ctx, SP([[30, 94], [56, 114], [62, 170]], false), lw(2.4), { a: .45 });
  // fes
  if (o.fes !== false) {
    const f = SP(B([[-46, -34], [-40, -70], [-34, -98], [12, -103], [22, -76], [30, -44], [-6, -40]]), true, .5);
    knock(ctx, f);
    if (o.col === 'navy') { plate(ctx, 'red', f, { a: .6 }); a2_navy(ctx, f, .6); } else plate(ctx, 'red', f);
    plate(ctx, 'red', SP(B([[-46, -34], [-40, -70], [-34, -98], [-18, -100], [-22, -38]]), true, .5), { a: .5 });
    inkStroke(ctx, f, lw(3));
    inkFill(ctx, SP(B([[-24, -100], [-36, -94], [-50, -72], [-54, -50], [-48, -52], [-42, -74], [-30, -92]]), true, .8));
  }
  // kulağa götürülmüş el (hafiye dinler)
  if (o.ear) {
    const arm = SP([[-92, 120], [-130, 80], [-96, 30], [-40, 2], [-26, 12], [-30, 28], [-74, 52], [-96, 92], [-70, 130]], true, .7); knock(ctx, arm); fill(arm);
    cut(ctx, SP([[-118, 82], [-90, 40], [-46, 14]], false), lw(2.2), { a: .4 });
    const hd = SP([[-40, -6], [-20, -16], [-10, 0], [-14, 22], [-30, 26], [-42, 14]], true, .8); knock(ctx, hd); fill(hd); cut(ctx, SP([[-20, -14], [-10, 2], [-14, 20]], false), lw(2), { a: .6 });
  }
  ctx.restore();
  // uzanan kol (dünya koordinatında): omuzdan hedefe, dirsek aşağıda
  if (o.reach) {
    const sh = [x + 34 * s * dir, y + 120 * s], tg = o.reach, el = [lerp(sh[0], tg[0], .42), Math.max(sh[1], tg[1]) + 56 * s];
    const ap = new Path2D(); ap.moveTo(sh[0], sh[1]); ap.lineTo(el[0], el[1]); ap.lineTo(tg[0], tg[1]);
    ctx.save(); ctx.lineJoin = 'round'; inkStroke(ctx, ap, 34 * s, { cap: 'round', col: o.col === 'navy' ? '#232A3A' : P.ink }); ctx.restore();
    const hd = a2_ell(tg[0], tg[1], 24 * s, 15 * s, dir > 0 ? .1 : -.1); knock(ctx, hd); inkFill(ctx, hd, { col: o.col === 'navy' ? '#232A3A' : P.ink });
    const rp = new Path2D(); rp.moveTo(el[0], el[1] - 15 * s); rp.lineTo(tg[0] - dir * 8 * s, tg[1] - 13 * s); cut(ctx, rp, 2.4, { a: .55 });
  }
}

// ——————————————————————————————————————— C04 · Hafiye ve jurnaller ———
// sol: gece mektep duvarı, ışıklı pencere; önde pencereye kulak veren hafiye silueti. "jurnaller"de sağdan Yıldız paneli basılır: masaya yığılan jurnaller, karanlık
function a2_C04_left(g) {
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  const wall = a2_R(-140, -140, W + 140, 870); a2_navy(g, wall, .85);
  const r = rng(401);
  for (let row = 0; row < 14; row++) { const yy = -120 + row * 78; cut(g, PL([[-140, yy], [W + 140, yy]], false), 1.6, { a: .2 }); for (let x = -140 + (row % 2) * 70 + r() * 20; x < W + 140; x += 140 + r() * 30) cut(g, PL([[x, yy], [x, Math.min(900, yy + 78)]], false), 1.4, { a: .16 }); }
  // zemin (sokak taşı) ve pencerenin ona düşürdüğü ışık
  const gr = a2_R(-140, 870, W + 140, H + 140); knock(g, gr); plate(g, 'sepia', gr, { a: .8, flat: true }); a2_navy(g, gr, .5);
  inkStroke(g, PL([[-140, 870], [W + 140, 870]], false), 3);
  const wx0 = 530, wx1 = 1000, wy0 = 140, wy1 = 690;
  const spill = SP(rough([[wx0 - 60, 874], [wx1 + 60, 874], [wx1 + 420, H + 140], [wx0 - 300, H + 140]], 3, 402), true, .3);
  knock(g, spill, '#DCCBA2'); plate(g, 'ochre', spill, { a: .12, flat: true });
  for (let i = 0; i < 5; i++) { const yy = 914 + i * 44; inkStroke(g, PL([[-140, yy], [W + 140, yy]], false), 1.2, { a: .3 }); }
  // pencere: kemerli, demir parmaklık; içeride mum ışığı ve iki baş (sahnenin tek ışık kaynağı)
  const win = SP([[wx0, wy1], [wx0, wy0 + 130], [wx0 + 48, wy0 + 34], [(wx0 + wx1) / 2, wy0], [wx1 - 48, wy0 + 34], [wx1, wy0 + 130], [wx1, wy1]], true, .5);
  knock(g, win, '#EFDDAE'); plate(g, 'ochre', win, { a: .16, flat: true });
  g.save(); g.clip(win);
  knock(g, a2_ell(765, 520, 170, 120), '#F6ECD0');
  inkFill(g, a2_ell(680, 492, 40, 50)); inkFill(g, SP([[620, 700], [632, 548], [680, 524], [730, 548], [738, 700]], true, .6));
  inkFill(g, a2_ell(866, 498, 38, 48)); inkFill(g, SP([[808, 700], [818, 554], [866, 530], [914, 554], [924, 700]], true, .6));
  plate(g, 'ochre', a2_R(wx0, 610, wx1, wy1), { a: .3, flat: true });
  g.restore();
  const bars = new Path2D(); for (let x = wx0 + 52; x < wx1; x += 52) { bars.moveTo(x, wy0); bars.lineTo(x, wy1); } for (const yy of [340, 520]) { bars.moveTo(wx0, yy); bars.lineTo(wx1, yy); }
  inkStroke(g, bars, 6);
  const fr = SP([[wx0 - 22, wy1 + 30], [wx0 - 22, wy0 + 124], [wx0 + 30, wy0 + 14], [(wx0 + wx1) / 2, wy0 - 22], [wx1 - 30, wy0 + 14], [wx1 + 22, wy0 + 124], [wx1 + 22, wy1 + 30]], false, .5);
  inkStroke(g, fr, 8); cut(g, fr, 2, { a: .4 });
  const sill = a2_R(wx0 - 50, wy1, wx1 + 50, wy1 + 34); knock(g, sill); a2_navy(g, sill, .5); inkStroke(g, sill, 3);
}
function a2_C04_right(g) {
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  const room = a2_R(-140, -140, W + 140, H + 140); a2_navy(g, room, .85);
  // perde ve yüksek pencere (Yıldız): ay ışığında saray bahçesi silueti
  const wn = a2_R(1560, 150, 1800, 520); knock(g, wn); a2_navy(g, wn, .6); inkStroke(g, wn, 6);
  inkFill(g, SP([[1560, 520], [1560, 430], [1600, 400], [1640, 420], [1690, 380], [1740, 410], [1800, 390], [1800, 520]], true, .7));
  for (const cx of [1610, 1740]) { const c = SP([[cx, 330], [cx + 14, 400], [cx, 470], [cx - 14, 400]], true, .8); inkFill(g, c); }
  const mul = new Path2D(); mul.moveTo(1680, 150); mul.lineTo(1680, 520); mul.moveTo(1560, 300); mul.lineTo(1800, 300); inkStroke(g, mul, 5);
  // masa (sepya), yeşil çuha yerine koyu sepya
  const desk = PL([[1020, 730], [W + 140, 716], [W + 140, H + 140], [1020, H + 140]]); knock(g, desk); plate(g, 'sepia', desk, { a: .85, flat: true }); plate(g, 'ink', desk, { a: .2, flat: true });
  // lambanın masaya düşürdüğü ışık (düz)
  knock(g, a2_roughCircle(1420, 800, 230, 407, .03), '#B9A47A'); knock(g, a2_roughCircle(1420, 790, 150, 408, .03), '#D9C7A0');
  inkStroke(g, PL([[1020, 730], [W + 140, 716]], false), 4); cut(g, PL([[1020, 736], [W + 140, 722]], false), 1.6, { a: .4 });
  // hokka ve kalem
  const ink0 = SP([[1760, 760], [1740, 700], [1800, 690], [1820, 760]], true, .7); knock(g, ink0); inkFill(g, ink0); cut(g, SP([[1752, 712], [1756, 750]], false), 2.4, { a: .5 });
  inkStroke(g, PL([[1790, 696], [1850, 600]], false), 3);
}
// jurnal yaprağı (masada): Osmanlıca soyut satırlar + mühür
function a2_jurnal(ctx, x, y, rot, seed, w = 300, h = 210) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  const p = PL(rough([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]], 1.2, seed)); knock(ctx, p, '#EFE6D0'); plate(ctx, 'ochre', p, { a: .12 });
  for (let i = 0; i < 6; i++) scriptLine(ctx, w / 2 - 20, -h / 2 + 34 + i * 26, (w - 50) * (i === 5 ? .5 : .9), 8, seed * 7 + i, { w: 1.6, a: .85 });
  const seal = a2_ell(-w / 2 + 50, h / 2 - 40, 22, 22); plate(ctx, 'sepia', seal, { n: 2 }); inkStroke(ctx, seal, 1.6);
  inkStroke(ctx, p, 2.2);
  ctx.restore();
}
a2_shot(S('C04'), S('C05'), (ctx, st) => {
  setReg(401);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t), tJ = Wd('C04', 'jurnaller'), tEar = Wd('C04', 'kulakları'), tH = Wd('C04', 'hafiyeler');
  const cm = a2_camAt(lt, d, { x: W / 2 + 30, y: H / 2, z: 1.02 }, { x: W / 2 - 30, y: H / 2 + 10, z: 1.07 });
  ctx.save(); cam(ctx, cm, .6); ctx.drawImage(a2_cache('c04-left', 140, a2_C04_left).c, -140, -140, W + 280, H + 280); ctx.restore();
  // hafiye: "kulakları"nda pencereye eğilir, elini kulağına götürür
  ctx.save(); cam(ctx, cm, 1);
  const lean = E.io2(clamp((tq - tEar) / .5)) * .07 + Math.sin(tq * 1.3) * .006;
  ctx.save(); ctx.translate(330, 1180); ctx.rotate(lean); ctx.translate(-330, -1180);
  a2_profile(ctx, 340, 470, 1.75, 1, { len: 440, collar: true, mus: true, ear: tq > tEar + .15, rim: false, seed: 41 });
  // "hafiyeler dinler": kâğıda not (küçük beyaz defter, ikişer karede kalem oynar)
  if (tq > tH) { const nb = a2_R(470, 860, 560, 930); knock(ctx, nb, '#EFE6D0'); inkStroke(ctx, nb, 2); for (let i = 0; i < 3; i++) scriptLine(ctx, 550, 880 + i * 16, 70 * clamp((tq - tH) * 1.4 - i * .4), 5, 450 + i, { w: 1.2 }); inkStroke(ctx, PL([[540 - (Math.floor(tq * 15) % 3) * 8, 900], [600, 860]], false), 4); }
  ctx.restore();
  ctx.restore();
  // Yıldız paneli: "jurnaller"de sağdan basılır (merdane gibi), masaya jurnaller yığılır; sonunda lamba söner
  const rv = E.out3(clamp((t - tJ + .32) / .3));
  if (rv > 0) {
    const x0 = lerp(W + 30, 1010, rv);
    ctx.save(); ctx.beginPath(); ctx.rect(x0, -10, W - x0 + 20, H + 20); ctx.clip();
    ctx.drawImage(a2_cache('c04-right', 140, a2_C04_right).c, -140, -140, W + 280, H + 280);
    const dim = 1 - ramp(t, S('C05') - .65, S('C05') - .05);
    const L = [1330, 520];
    if (dim > 0) for (const [r, col] of [[150, '#A99572'], [92, '#DCCAA2']]) knock(ctx, a2_ell(L[0], L[1] + 40, r * 1.3 * (.5 + .5 * dim), r * (.5 + .5 * dim)), col);
    gasLamp(ctx, L[0], L[1], .8, t);
    const n = Math.min(11, Math.max(1, Math.floor((tq - tJ + .2) / .17) + 1)), r = rng(431);
    for (let i = 0; i < n; i++) { const fall = i === n - 1 ? 1 - E.out3(clamp(((tq - tJ + .2) - i * .17) / .12)) : 0; a2_jurnal(ctx, 1450 + (r() - .5) * 60, 760 - i * 9 - fall * 120, (r() - .5) * .3, 440 + i); }
    if (dim < 1) plate(ctx, 'ink', a2_R(x0, -10, W + 10, H + 10), { a: .55 * (1 - dim), flat: true });
    ctx.restore();
    // panel ayırıcı (kalın is + kâğıt kenar)
    knock(ctx, a2_R(x0 - 14, -10, x0, H + 10)); inkFill(ctx, a2_R(x0 - 8, -10, x0 + 4, H + 10));
    stamp(ctx, 'YILDIZ', x0 + 70, 128, t - tJ + .2, d, { size: 48 });
  }
}, { tr: { type: 'cut' }, post: a2_NIGHT });

// ——————————————————————————————————————— C05 · Askerî Tıbbiye, 1889 ———
// C05a: sabah, Askerî Tıbbiye cephesi güneşte (aydınlık çekim: üç koyu çekimden sonra soluk); dört öğrenci birlikte geçer (odak), kapıda nöbetçi
function a2_C05a_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  // gök: düz okra bantlar + üstte durağan sepya yarım ton
  plate(g, 'ochre', a2_R(-140, -140, W + 140, 420), { a: .2 }); plate(g, 'ochre', a2_R(-140, -140, W + 140, 200), { a: .14 });
  halftone(g, 'sepia', a2_R(-140, -140, W + 140, 120), .1, { cell: 12, ang: 15 });
  for (const [cx, cy, w, h, sd] of [[360, 150, 520, 26, 1], [1500, 110, 600, 30, 2]]) { const c = SP(rough([[cx - w / 2, cy + h / 2], [cx - w * .25, cy - h / 2], [cx + w * .2, cy - h * .4], [cx + w / 2, cy + h / 2]], 1.5, sd + 520), true, .8); knock(g, c); plate(g, 'sepia', a2_R(cx - w / 2, cy + h * .1, cx + w / 2, cy + h / 2 + 2), { a: .22 }); inkStroke(g, c, 1.6, { a: .7 }); }
  // cephe: kâğıt, sağ kanat ve saçak altları sepya gölge (güneş soldan)
  const yT = 360, yB = 860, fac = a2_R(-140, yT, W + 140, 905); knock(g, fac); plate(g, 'ochre', fac, { a: .14 });
  const ped = PL([[720, yT + 10], [960, 230], [1200, yT + 10]]), cen = a2_R(740, yT, 1180, yB); knock(g, ped); knock(g, cen); plate(g, 'ochre', cen, { a: .08 });
  plate(g, 'sepia', PL([[960, 230], [1200, yT + 10], [960, yT + 10]]), { a: .3 }); plate(g, 'sepia', a2_R(1180, yT, W + 140, 905), { a: .22 });
  inkStroke(g, ped, 3); inkStroke(g, cen, 3);
  for (const yy of [yT, 600]) { plate(g, 'sepia', a2_R(-140, yy + 8, W + 140, yy + 30), { a: .35 }); const c = a2_R(-140, yy, W + 140, yy + 10); knock(g, c); inkStroke(g, c, 2); }
  inkStroke(g, PL([[-140, yT], [720, yT]], false), 3); inkStroke(g, PL([[1200, yT], [W + 140, yT]], false), 3);
  const win = (q) => { knock(g, q); plate(g, 'sepia', q, { a: .85 }); plate(g, 'ink', q, { a: .3 }); inkStroke(g, q, 2.2); };
  for (let x = -100; x < W + 140; x += 120) { if (x > 700 && x < 1200) continue; for (const [y0, y1] of [[420, 570], [650, 820]]) { const w = SP([[x, y1], [x, y0 + 20], [x + 30, y0], [x + 60, y0 + 20], [x + 60, y1]], true, .4); win(w); cut(g, PL([[x + 30, y0 + 6], [x + 30, y1]], false), 1.6, { a: .35 }); } }
  for (const x of [790, 1080]) win(a2_R(x, 420, x + 50, 570));
  const door = SP([[900, yB], [900, 690], [960, 650], [1020, 690], [1020, yB]], true, .5); knock(g, door); inkFill(g, door); cut(g, PL([[960, 660], [960, yB]], false), 2, { a: .4 });
  for (const x of [760, 860, 1060, 1160]) { const col = a2_R(x - 12, 620, x + 12, yB); knock(g, col); plate(g, 'sepia', a2_R(x + 2, 620, x + 12, yB), { a: .35 }); inkStroke(g, col, 2); }
  scriptLine(g, 1050, 330, 180, 12, 551, { w: 2.4 });
  // sokak (güneşli) ve uzun sabah gölgeleri (sağa düşer)
  const st = a2_R(-140, 905, W + 140, H + 140); knock(g, st); plate(g, 'ochre', st, { a: .3 }); plate(g, 'sepia', st, { a: .1 });
  inkStroke(g, PL([[-140, 905], [W + 140, 905]], false), 3);
  const fence = new Path2D(); for (let x = -130; x < W + 140; x += 26) { fence.moveTo(x, 905); fence.lineTo(x, 790); fence.moveTo(x - 5, 798); fence.lineTo(x, 782); fence.lineTo(x + 5, 798); } fence.moveTo(-140, 812); fence.lineTo(W + 140, 812); fence.moveTo(-140, 884); fence.lineTo(W + 140, 884);
  inkStroke(g, fence, 3.4);
  plate(g, 'sepia', PL([[-140, 905], [W + 140, 905], [W + 140, 960], [-140, 950]]), { a: .3 }); // parmaklığın gölgesi
  for (const [cx, h] of [[140, 560], [330, 420], [1640, 520], [1830, 600]]) {
    plate(g, 'sepia', PL([[cx - 30, 905], [cx + 40, 905], [cx + 340, 1000], [cx + 250, 1010]]), { a: .3 });
    const c = SP([[cx, 900 - h], [cx + 48, 900 - h * .55], [cx + 40, 900 - h * .1], [cx, 900], [cx - 40, 900 - h * .1], [cx - 48, 900 - h * .55]], true, .8);
    knock(g, c); plate(g, 'teal', c, { n: 2 }); plate(g, 'ink', c, { a: .3 }); cut(g, SP([[cx - 14, 900 - h * .8], [cx - 26, 900 - h * .4], [cx - 18, 880]], false), 2, { a: .35 }); inkStroke(g, c, 2);
  }
}
a2_shot(S('C05'), Wd('C05', 'dört'), (ctx, st) => {
  setReg(501);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t), lq = a2_q(lt);
  const cm = a2_camAt(lt, d, { x: W / 2 - 40, y: H / 2, z: 1.0 }, { x: W / 2 + 60, y: H / 2 + 20, z: 1.07 });
  ctx.save(); cam(ctx, cm, .85); ctx.drawImage(a2_cache('c05a-day', 140, a2_C05a_bg).c, -140, -140, W + 280, H + 280);
  // bacadan duman (yarım ton, durağan olmayan duman serbest) ve geçen güvercinler
  for (let i = 5; i >= 0; i--) { const a = ((lt * .2 + i / 6) % 1), rr = lerp(12, 46, a); halftone(ctx, 'sepia', a2_ell(1400 + a * 160, 220 - a * 120, rr * 1.3, rr * .8), lerp(.4, .08, a), { cell: 10, ang: 45 }); }
  const chim = a2_R(1384, 222, 1416, 300); knock(ctx, chim); plate(ctx, 'sepia', chim, { a: .5 }); inkStroke(ctx, chim, 2.2);
  for (let i = 0; i < 4; i++) a2_gull(ctx, 300 + i * 90 + lt * (60 + i * 8), 200 + i * 26 + Math.sin(t * 1.4 + i) * 8, .8, Math.floor(t * 6 + i) % 2);
  // nöbetçi: kapı önünde (parmaklığın ardında)
  const sx = 960 + Math.sin(lq * .7) * 110, dirS = Math.cos(lq * .7) >= 0 ? 1 : -1;
  a2_figure(ctx, sx, 880, 220, 'fes', Math.floor(t * 5) % 2, dirS, { red: true });
  inkStroke(ctx, PL([[sx - 9 * dirS, 690], [sx - 4 * dirS, 830]], false), 4);
  ctx.restore();
  // dört öğrenci birlikte, sokakta soldan sağa (ikişer karede adım); uzun gölgeleri sağa düşer
  ctx.save(); cam(ctx, cm, 1);
  for (let i = 0; i < 4; i++) {
    const x = 240 + i * 120 + lq * 64 + (i % 2) * 14, yf = 1018 + (i % 2) * 14, h = 300 - (i % 2) * 10;
    plate(ctx, 'sepia', PL([[x - 14, yf], [x + 14, yf], [x + 220, yf + 40], [x + 190, yf + 48]]), { a: .35 });
    a2_figure(ctx, x, yf, h, i === 2 ? 'fes' : 'fes', (Math.floor(t * 6) + i) % 2, 1, { red: true });
    // kitap/çanta (biri koltuğunda kitap)
    if (i === 1) { const b = a2_R(x + 6 * h / 100, yf - 62 * h / 100, x + 13 * h / 100, yf - 50 * h / 100); knock(ctx, b, '#EFE6D0'); inkStroke(ctx, b, 2); }
  }
  ctx.restore();
  const yr = 1899 - Math.min(10, Math.floor(clamp((lt - .25) / 1.1) * 11));
  stamp(ctx, 'İSTANBUL · ' + yr, 80, 128, lt + .06, d + .06, { size: 48, typing: .001 });
  stamp(ctx, 'ASKERÎ TIBBİYE', 80, 214, t - Wd('C05', 'askeri'), d, { size: 48 });
}, { tr: { type: 'press', dur: .6 } });

// C05b: loş oda, dört öğrenci silueti; "cemiyet"te eller masadaki yemin kitabının üstüne konur, başlar öne eğilir; "ittihat"ta damga
function a2_C05b_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  const wall = a2_R(-140, -140, W + 140, 760); a2_navy(g, wall, .85);
  const dado = a2_R(-140, 640, W + 140, 800); knock(g, dado); plate(g, 'sepia', dado, { a: .85, flat: true }); a2_navy(g, dado, .35);
  for (let x = -100; x < W + 140; x += 180) inkStroke(g, a2_R(x, 664, x + 150, 780), 2, { a: .5 });
  inkStroke(g, PL([[-140, 640], [W + 140, 640]], false), 3);
  const fl = a2_R(-140, 800, W + 140, H + 140); knock(g, fl); plate(g, 'sepia', fl, { a: .85, flat: true }); plate(g, 'ink', fl, { a: .15, flat: true });
  // tek ışık kaynağı: asma lamba; duvarda kırık kenarlı düz halkalar (yalnız lambanın çevresi; başlara ≥40 px)
  // lambri lamba altında aydınlanır
  knock(g, a2_roughCircle(960, 720, 360, 519, .03, 32), '#CDB990'); g.save(); g.clip(a2_R(-140, 640, W + 140, 800)); for (let x = -100; x < W + 140; x += 180) inkStroke(g, a2_R(x, 664, x + 150, 780), 2, { a: .5 }); g.restore(); inkStroke(g, PL([[-140, 640], [W + 140, 640]], false), 3);
  for (const [r, col, sd] of [[232, '#C9B48B', 1], [155, '#DCCAA3', 2], [90, '#EFE3C4', 3]]) knock(g, a2_roughCircle(960, 430, r, 520 + sd, .03, 32), col);
  // lambanın yere düşürdüğü ışık havuzu (masanın çevresi)
  knock(g, a2_ell(960, 950, 620, 130), '#C8B48A'); knock(g, a2_ell(960, 945, 460, 95), '#E0CFA8');
  // kitap rafı (sağda, karanlıkta)
  const sh = a2_R(1560, 160, 1900, 640); knock(g, sh); plate(g, 'sepia', sh, { a: .85, flat: true }); plate(g, 'ink', sh, { a: .35, flat: true }); inkStroke(g, sh, 3);
  const r = rng(521); for (let row = 0; row < 4; row++) { const y1 = 260 + row * 110; inkStroke(g, PL([[1560, y1], [1900, y1]], false), 3); for (let x = 1574; x < 1886; x += 14 + r() * 10) { const bk = a2_R(x, y1 - 70 - r() * 20, x + 10 + r() * 6, y1); a2_navy(g, bk, .5 + r() * .35); cut(g, bk, 1, { a: .25 }); } }
  // masa (yuvarlak, örtülü): lamba altında aydınlık
  const top = a2_ell(960, 780, 300, 44); plate(g, 'ink', a2_ell(970, 800, 310, 50), { a: .35 });
  const cloth = SP([[660, 780], [700, 900], [960, 930], [1220, 900], [1260, 780]], true, .6); knock(g, cloth, '#CBB68C'); plate(g, 'ochre', cloth, { a: .2 }); plate(g, 'sepia', PL([[1060, 780], [1260, 780], [1220, 900], [1080, 922]]), { a: .35 }); inkStroke(g, cloth, 2.6);
  knock(g, top, '#E6D6B2'); inkStroke(g, top, 2.6);
  for (const x of [740, 860, 1060, 1180]) inkStroke(g, SP([[x, 800], [x + (x - 960) * .05, 900]], false), 1.6, { a: .45 });
}
a2_shot(Wd('C05', 'dört'), S('C06'), (ctx, st) => {
  setReg(502);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t);
  const tG = Wd('C05', 'gizli'), tC = Wd('C05', 'cemiyet'), tI = Wd('C05', 'ittihat');
  const cm = a2_camAt(lt, d, { x: W / 2, y: H / 2, z: 1.0 }, { x: W / 2, y: H / 2 - 30, z: 1.07 });
  ctx.save(); cam(ctx, cm, .6); ctx.drawImage(a2_cache('c05b-bg', 140, a2_C05b_bg).c, -140, -140, W + 280, H + 280); ctx.restore();
  ctx.save(); cam(ctx, cm, 1);
  gasLamp(ctx, 960, 400, .8, t);
  // dört öğrenci: arkadakiler lacivert ikinci baskı, öndekiler is; "gizli"de öne eğilirler; "cemiyet"te eller birleşir
  const lean = E.io2(clamp((tq - tG) / .6)) * .06, join = E.io2(clamp((tq - tC + .3) / .6));
  const C = [960, 762];   // yemin kitabının üstü
  const F4 = [
    { x: 520, y: 520, s: .88, dir: 1, col: 'navy', seed: 61, mus: true, tgt: [C[0] - 54, C[1] - 6] },
    { x: 1400, y: 516, s: .88, dir: -1, col: 'navy', seed: 63, mus: false, tgt: [C[0] + 44, C[1] - 10] },
    { x: 690, y: 580, s: 1.0, dir: 1, col: 'ink', seed: 65, mus: false, tgt: [C[0] - 22, C[1] + 2] },
    { x: 1232, y: 586, s: 1.0, dir: -1, col: 'ink', seed: 67, mus: true, tgt: [C[0] + 18, C[1] - 2] },
  ];
  // yemin kitabı: masanın ortasında yatık, kapalı (sepya cilt, kâğıt sayfa kenarı)
  { const bx = 960, by = 768, top = PL([[bx - 118, by - 10], [bx + 92, by - 18], [bx + 128, by + 4], [bx - 84, by + 14]]), side = PL([[bx - 84, by + 14], [bx + 128, by + 4], [bx + 128, by + 20], [bx - 84, by + 30]]);
    plate(ctx, 'ink', PL([[bx - 80, by + 30], [bx + 136, by + 20], [bx + 150, by + 30], [bx - 70, by + 40]]), { a: .3, flat: true });
    knock(ctx, side, '#F3EBD6'); for (let k = 1; k < 4; k++) inkStroke(ctx, PL([[bx - 84, by + 14 + k * 4], [bx + 128, by + 4 + k * 4]], false), 1, { a: .5 }); inkStroke(ctx, side, 2.2);
    knock(ctx, top); plate(ctx, 'sepia', top, { a: .9, flat: true }); inkStroke(ctx, top, 2.6); inkStroke(ctx, PL([[bx - 96, by - 4], [bx + 84, by - 11], [bx + 104, by + 2], [bx - 72, by + 9]]), 1.4, { col: P.ochre, a: .9 }); }
  const bowK = E.io2(clamp((tq - tC + .1) / .5));
  for (const f of F4) {
    const rest = [f.x + f.dir * 130 * f.s, 790 + (f.col === 'navy' ? -40 : 0)], tg = [lerp(rest[0], f.tgt[0], join), lerp(rest[1], f.tgt[1], join)];
    ctx.save(); ctx.translate(f.x, f.y + 300); ctx.rotate(lean * f.dir); ctx.translate(-f.x, -(f.y + 300));
    a2_profile(ctx, f.x, f.y, f.s, f.dir, { len: (H + 60 - f.y) / f.s, col: f.col, mus: f.mus, seed: f.seed, reach: tg, bow: (.06 + .2 * bowK) });
    ctx.restore();
  }
  ctx.restore();
  // damga: İTTİHAT VE TERAKKİ'NİN ÇEKİRDEĞİ (iki satır)
  if (!NOTEXT && t >= tI) {
    const k = 1 + (1 - E.out3(clamp((t - tI) / .18))) * .22, a = clamp((t - tI) / .06);
    ctx.save(); ctx.globalAlpha = a; ctx.translate(W / 2, 150); ctx.scale(k, k); ctx.rotate(-.025);
    const bw = 1180, bh = 210, box = PL(rough([[-bw / 2, -bh / 2], [bw / 2, -bh / 2], [bw / 2, bh / 2], [-bw / 2, bh / 2]], 1.2, 77));
    plate(ctx, 'ink', PL([[-bw / 2 + 10, -bh / 2 + 12], [bw / 2 + 10, -bh / 2 + 12], [bw / 2 + 10, bh / 2 + 12], [-bw / 2 + 10, bh / 2 + 12]]), { a: .4 });
    knock(ctx, box); inkStroke(ctx, box, 4); inkStroke(ctx, a2_R(-bw / 2 + 12, -bh / 2 + 12, bw / 2 - 12, bh / 2 - 12), 1.6);
    txt(ctx, 'İTTİHAT VE TERAKKİ’NİN', 0, -22, FONT.title(78), { align: 'center', base: 'middle', ls: 2 });
    txt(ctx, 'ÇEKİRDEĞİ', 0, 62, FONT.mono(50), { align: 'center', base: 'middle', ls: 14 });
    ctx.restore();
  }
}, { tr: { type: 'cut' }, post: a2_NIGHT });

// ——————————————————————————————————————— C06 · Kurmay yüzbaşılar, ihbar, Şam ———
// C06a: Erkân-ı Harbiye dershanesi; duvarda Rumeli haritası; Ali Fuat (22) arkada, Mustafa Kemal (23) önde (Ocak 1905); lacivert setre, fes.
// "ihbarla": sağdan iki subayın üstüne bir insan gölgesi düşer (is .35), oda kararır, ikisi de dönüp bakar.
// insan gölgesi: profil siluetin yolu (fesli), tek düz is kalıbı
function a2_shadowFig(ctx, x, y, s, dir, a) {
  const face = [[-8, -62], [14, -60], [27, -48], [31, -32], [33, -17], [37, -8], [47, 7], [49, 13], [40, 17], [41, 23], [37, 27], [40, 33], [36, 39], [34, 49], [24, 57], [12, 61], [12, 76]];
  const body = [[30, 92], [64, 114], [80, 200], [84, 520], [-150, 520], [-140, 200], [-110, 116], [-62, 94], [-34, 80], [-30, 64], [-44, 40], [-54, 10], [-54, -24], [-42, -50], [-26, -60]];
  const fes = [[-46, -34], [-40, -70], [-34, -98], [12, -103], [22, -76], [30, -44]];
  const T = q => q.map(([u, v]) => [x + u * s * dir, y + v * s]);
  const p = SP(T([...face, ...body]), true, .55); p.addPath(SP(T(fes), true, .5));
  plate(ctx, 'ink', p, { a, flat: true });
}
function a2_C06a_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  const wall = a2_R(-140, -140, W + 140, H + 140); plate(g, 'ochre', wall, { a: .36 });
  // başların çevresi hariç durağan sepya yarım ton (duvar)
  const htClip = new Path2D(); htClip.rect(-140, 60, W + 280, 820); htClip.ellipse(830, 330, 230, 230, 0, 0, TAU); htClip.ellipse(1220, 340, 250, 250, 0, 0, TAU);
  g.save(); g.clip(htClip, 'evenodd'); radialHT(g, 'sepia', 1300, 120, 200, 1300, 0, .17, { cell: 11, box: [-140, 60, W + 140, 880], sx: 1.3 }); g.restore();
  const beam = PL(rough([[-140, 0], [W + 140, 0], [W + 140, 56], [-140, 62]], 1.5, 3)); plate(g, 'sepia', beam, { a: .8 }); plate(g, 'ink', beam, { a: .3 }); inkStroke(g, PL([[-140, 62], [W + 140, 56]], false), 4);
  // Rumeli haritası (soyut kıyılar, sepya kara, turkuaz deniz), Osmanlıca kartuş
  g.save(); g.translate(70, 150); g.rotate(-.018);
  plate(g, 'ink', a2_R(14, 16, 600, 490), { a: .3 });
  const sh = a2_R(0, 0, 586, 474); knock(g, sh, P.paperD); inkStroke(g, sh, 3); inkStroke(g, a2_R(12, 12, 574, 462), 1.2);
  const sea = a2_R(12, 12, 574, 462); plate(g, 'teal', sea, { a: .45 });
  g.save(); g.clip(sea);
  const land = SP(rough([[-40, -40], [640, -40], [640, 130], [560, 150], [500, 200], [470, 240], [430, 250], [400, 300], [340, 290], [300, 330], [270, 370], [220, 380], [180, 430], [150, 520], [-40, 520]], 1.5, 601), true, .9);
  knock(g, land, '#E3D6B8'); plate(g, 'ochre', land, { a: .3 }); inkStroke(g, land, 2.2);
  g.restore();
  ridge(g, [[60, 140], [130, 120], [210, 140], [270, 120]], 16, px => px, 611); ridge(g, [[90, 300], [150, 290], [200, 310]], 12, px => px, 612);
  for (const [x, y] of [[370, 230], [160, 250], [470, 90]]) { inkFill(g, a2_ell(x, y, 7, 7)); }
  const cart = a2_R(380, 380, 556, 444); knock(g, cart); inkStroke(g, cart, 1.8); scriptLine(g, 544, 410, 150, 10, 621, { w: 1.8 }); scriptLine(g, 520, 432, 100, 7, 622, { w: 1.4 });
  for (const [x, y] of [[20, 20], [566, 20], [20, 454], [566, 454]]) { const p = a2_ell(x, y, 6, 6); knock(g, p); plate(g, 'sepia', p, { n: 2 }); inkStroke(g, p, 1.6); }
  g.restore();
  // kara tahta köşesi (sağda): geometri çizimi
  const bb = a2_R(1560, 150, W + 140, 640); knock(g, bb); inkFill(g, bb); plate(g, 'navy', bb, { a: .5 });
  const ci = new Path2D(); ci.arc(1760, 380, 110, 0, TAU); cut(g, ci, 2.2, { a: .6 }); cut(g, PL([[1650, 470], [1880, 290], [1700, 290]]), 2, { a: .5 });
  inkStroke(g, bb, 6, { col: P.sepia });
}
function a2_C06a_table(g) {
  const tb = PL([[-140, 836], [W + 140, 830], [W + 140, H + 140], [-140, H + 140]]); knock(g, tb); plate(g, 'sepia', tb, { n: 2 }); plate(g, 'ochre', tb, { a: .3 });
  inkStroke(g, PL([[-140, 836], [W + 140, 830]], false), 4.4);
  const r = rng(605); for (let i = 0; i < 12; i++) { const yy = 850 + i * 18 + r() * 4, q = new Path2D(); let x = -140; q.moveTo(x, yy); while (x < W + 140) { const nx = x + 100 + r() * 160; q.quadraticCurveTo((x + nx) / 2, yy + (r() - .5) * 6, nx, yy + (r() - .5) * 3); x = nx; } inkStroke(g, q, 1.5, { a: .35 }); }
  paperSheet(g, 1500, 900, 230, 120, .05, 607, { header: true }); paperSheet(g, 420, 920, 200, 110, -.07, 608, { rows: 4 });
}
a2_shot(S('C06'), Wd('C06', 'tutuklanıp'), (ctx, st) => {
  setReg(601);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t);
  const tA = Wd('C06', 'ihbarla'), tM = Wd('C06', 'mustafa'), tF = Wd('C06', 'ali');
  const cm = a2_camAt(lt, d, { x: W / 2 - 20, y: H / 2, z: 1.0 }, { x: W / 2 + 60, y: H / 2 - 10, z: 1.06 });
  ctx.save(); cam(ctx, cm, .55); ctx.drawImage(a2_cache('c06a-bg', 140, a2_C06a_bg).c, -140, -140, W + 280, H + 280); ctx.restore();
  ctx.save(); cam(ctx, cm, 1);
  // ihbar: dönüp bakış (haritadan sağa)
  const turn = E.io2(clamp((tq - tA - .15) / .35));
  const look = [lerp(330, 1900, turn), lerp(360, 420, turn)];
  const S_ = 1.32;
  const af = { x: 830, y: 350, s: S_, dir: -1 };
  bust(ctx, { ...af, coat: 'setre', col: 'navy', w: .96, seed: 13, len: (860 - af.y) / S_, tilt: .03, turn: .3, back: true });
  head3q(ctx, { ...af, who: 'alifuat', gear: 'fes', light: 'front', lookAt: look, age: 22, tilt: -.03 + turn * .04 });
  const mk = { x: 1220, y: 364, s: S_, dir: -1 };
  bust(ctx, { ...mk, coat: 'setre', col: 'navy', w: .98, seed: 3, len: (860 - mk.y) / S_, tilt: .05, turn: .3, sep: true, arms: 'back' });
  head3q(ctx, { ...mk, who: 'mk', gear: 'fes', light: 'front', lookAt: look, age: 23, tilt: -.04 + turn * .05 });
  // ihbar: sağdan gelen birinin gölgesi iki subayın üstüne düşer (kişi kareye girmez)
  const hk = E.out3(clamp((tq - tA + .5) / .5));
  if (hk > 0) a2_shadowFig(ctx, lerp(2350, 1120, hk), 300, 3.3, -1, .35);
  ctx.drawImage(a2_cache('c06a-table', 140, a2_C06a_table).c, -140, -140, W + 280, H + 280);
  // ortam kararır (lacivert basılır)
  const dk = ramp(t, tA, tA + .5);
  if (dk > 0) plate(ctx, 'navy', a2_R(-160, -160, W + 160, H + 160), { a: .16 * dk, flat: true });
  ctx.restore();
  stamp(ctx, 'ERKÂN-I HARBİYE · 1905', 80, 128, t - Wd('C06', 'beşte'), d, { size: 48 });
  // levhalar (64/40): MK sağ üstte (fesin üstünde ≥40 px), Ali Fuat sol altta; sağ alt kuşak şeridine ayrılı
  nameTag(ctx, 1860, 54, 'MUSTAFA KEMAL', '23 yaşında · kurmay yüzbaşı', t - tM, 99, { align: 'right', size: 64, sub: 40, bg: P.paperD });
  nameTag(ctx, 80, 896, 'ALİ FUAT', '22 yaşında · kurmay yüzbaşı', t - tF, 99, { align: 'left', size: 64, sub: 40, bg: P.paperD });
}, { tr: { type: 'press', dur: .6 } });

// C06b: harita — İstanbul'dan deniz yoluyla Beyrut'a, oradan Şam'a sürgün yolu (kelimeye bağlı çizilir)
function a2_C06b_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  const desk = a2_R(-140, -140, W + 140, H + 140); plate(g, 'sepia', desk, { a: .7 }); plate(g, 'ink', desk, { a: .2 });
  g.save(); g.translate(60, 40); g.rotate(-.012);
  const MW = 1800, MH = 1000;
  plate(g, 'ink', a2_R(16, 18, MW + 16, MH + 18), { a: .35 });
  const sheet = PL(rough([[0, 0], [MW, 0], [MW, MH], [0, MH]], 2, 631)); knock(g, sheet, P.paperD);
  g.save(); g.clip(sheet);
  plate(g, 'teal', a2_R(0, 0, MW, MH), { a: .5 }); halftone(g, 'teal', a2_R(0, 0, MW, MH), .14, { cell: 12, ang: 15 });
  // kara: Balkanlar, Anadolu, Levant, Kıbrıs, Ege adaları (şematik)
  const lands = [
    [[0, 0], [700, 0], [690, 120], [620, 170], [585, 210], [540, 240], [500, 300], [430, 320], [400, 380], [340, 420], [300, 520], [250, 560], [200, 640], [120, 660], [60, 760], [0, 780]],
    [[630, 230], [700, 190], [760, 160], [900, 150], [1100, 130], [1300, 120], [1500, 140], [1800, 120], [1800, 740], [1640, 700], [1460, 640], [1380, 600], [1300, 620], [1180, 640], [1040, 640], [920, 610], [820, 640], [740, 580], [700, 520], [640, 470], [660, 400], [620, 330], [600, 270]],
    [[1440, 640], [1640, 700], [1800, 740], [1800, 1000], [1560, 1000], [1530, 900], [1500, 820], [1470, 740]],
  ];
  for (const L of lands) { const p = SP(rough(L, 2.5, L.length * 7), true, .5); knock(g, p, '#E6D9BC'); plate(g, 'ochre', p, { a: .35 }); inkStroke(g, p, 2.6); }
  // Karadeniz (kuzeyde, kara içinde deniz)
  const bs = SP(rough([[760, 0], [1700, 0], [1700, 90], [1500, 110], [1200, 100], [960, 120], [800, 120], [740, 60]], 2, 641), true, .6); knock(g, bs); plate(g, 'teal', bs, { a: .5 }); inkStroke(g, bs, 2.4);
  const mar = a2_ell(700, 205, 50, 16); knock(g, mar); plate(g, 'teal', mar, { a: .5 }); inkStroke(g, mar, 2);
  const cy = SP(rough([[1150, 770], [1260, 740], [1330, 720], [1300, 760], [1220, 800], [1150, 800]], 1.5, 651), true, .6); knock(g, cy, '#E6D9BC'); plate(g, 'ochre', cy, { a: .35 }); inkStroke(g, cy, 2.2);
  for (const [x, y, r] of [[520, 420, 22], [560, 520, 16], [470, 560, 18], [600, 620, 26], [760, 700, 30], [430, 480, 12], [300, 760, 60]]) { const p = SP(rough([[x - r, y], [x, y - r * .6], [x + r, y], [x, y + r * .6]], r * .15, x), true, .8); knock(g, p, '#E6D9BC'); plate(g, 'ochre', p, { a: .35 }); inkStroke(g, p, 1.8); }
  // Toros sıradağları (taramalı), çöl kenarı
  ridge(g, [[900, 560], [1000, 520], [1120, 540], [1240, 510], [1360, 540]], 22, px => px, 661);
  ridge(g, [[1560, 760], [1600, 860], [1630, 960]], 16, px => px, 662);
  // Osmanlıca soyut yer adları ve kartuş
  for (const [x, y, L, sd] of [[1200, 300, 160, 1], [1660, 420, 120, 2], [380, 120, 140, 3], [1720, 880, 100, 4]]) scriptLine(g, x, y, L, 11, 670 + sd, { w: 2, a: .8 });
  const cart = a2_R(60, 860, 400, 960); knock(g, cart); inkStroke(g, cart, 2.2); inkStroke(g, a2_R(68, 868, 392, 952), 1); scriptLine(g, 380, 905, 290, 13, 681, { w: 2 }); scriptLine(g, 330, 935, 190, 9, 682, { w: 1.6 });
  // pusula gülü
  const rose = new Path2D(); for (let k = 0; k < 8; k++) { const a = k / 8 * TAU, r = k % 2 ? 26 : 60; rose.moveTo(1000, 860); rose.lineTo(1000 + Math.cos(a) * r, 860 + Math.sin(a) * r); } inkStroke(g, rose, 2); inkFill(g, PL([[1000, 800], [1008, 860], [992, 860]]));
  g.restore();
  inkStroke(g, sheet, 3); inkStroke(g, a2_R(14, 14, MW - 14, MH - 14), 1.2);
  g.restore();
}
a2_shot(Wd('C06', 'tutuklanıp'), Wd('C06', 'yeni'), (ctx, st) => {
  setReg(602);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t);
  const tR = Wd('C06', 'suriyeye'), tS = Wd('C06', 'şamda');
  const cm = a2_camAt(lt, d, { x: W / 2 - 60, y: H / 2 - 10, z: 1.0 }, { x: W / 2 + 90, y: H / 2 + 30, z: 1.07 }, E.io2);
  ctx.save(); cam(ctx, cm, 1);
  ctx.drawImage(a2_cache('c06b-bg', 140, a2_C06b_bg).c, -140, -140, W + 280, H + 280);
  // yol: İstanbul → Çanakkale → Ege → Rodos önü → Kıbrıs güneyi → Beyrut → (kara) Şam
  const o = [60, 40];
  const route = [[700, 210], [640, 290], [610, 380], [620, 520], [700, 660], [880, 720], [1100, 840], [1300, 850], [1470, 790]].map(([x, y]) => [x + o[0], y + o[1]]);
  const land = [[1470, 790], [1540, 800], [1610, 790]].map(([x, y], i) => i ? [x + o[0], y + o[1]] : [x + o[0], y + o[1]]);
  const pr = E.io2(clamp((tq - tR + .2) / 1.9)), pl = E.io2(clamp((tq - tS + .6) / .6));
  const rp = new Path2D(); spl(rp, route, false, 1);
  ctx.save(); ctx.setLineDash([22, 14]); ctx.lineDashOffset = 0;
  ctx.save(); ctx.beginPath(); const xr = lerp(route[0][0] - 60, route[route.length - 1][0] + 40, pr); ctx.rect(-200, -200, xr + 200, H + 400); ctx.clip(); inkStroke(ctx, rp, 7, { cap: 'butt' }); ctx.restore();
  if (pl > 0) { const lp = new Path2D(); lp.moveTo(land[0][0], land[0][1]); lp.lineTo(lerp(land[0][0], land[2][0], pl), lerp(land[0][1], land[2][1], pl)); inkStroke(ctx, lp, 7, { cap: 'butt' }); }
  ctx.restore();
  // vapur simgesi rotada ilerler
  if (pr > 0 && pr < 1) { let k = Math.min(route.length - 2, Math.floor(pr * (route.length - 1))), f = pr * (route.length - 1) - k; const x = lerp(route[k][0], route[k + 1][0], f), y = lerp(route[k][1], route[k + 1][1], f); a2_steamer(ctx, x, y + 6, .16, 1, t, { seed: 9 }); }
  // şehir damgaları (lastik damga: daire + nokta) ve Latin etiketler (izleyici katmanı)
  const city = (x, y, s, lab, at, big) => {
    const k = a2_in(t, at, .2); if (k <= 0) return;
    const r0 = (big ? 22 : 15) * (1 + (1 - k) * .6); const c = a2_ell(x, y, r0, r0); knock(ctx, c); inkStroke(ctx, c, 4); inkFill(ctx, a2_ell(x, y, r0 * .45, r0 * .45));
    if (!NOTEXT) { ctx.save(); ctx.globalAlpha = k; ctx.font = FONT.mono(big ? 48 : 40); ctx.letterSpacing = '4px'; const w = ctx.measureText(lab).width; ctx.restore();
      const left = s < 0, bh = big ? 66 : 58, bx = left ? x - 28 - w - 36 : x + (big ? 36 : 28), by = left ? y + 24 : y - (big ? 70 : 54); ctx.save(); ctx.globalAlpha = k; const b = a2_R(bx, by, bx + w + 36, by + bh); plate(ctx, 'ink', a2_R(bx + 6, by + 7, bx + w + 42, by + bh + 7), { a: .35 }); knock(ctx, b); inkStroke(ctx, b, 2.6); ctx.restore();
      label(ctx, lab, bx + 18, by + bh * .72, FONT.mono(big ? 48 : 40), { ls: 4, a: k }); }
  };
  city(700 + o[0], 210 + o[1], 1, 'İSTANBUL', S('C06') - 10, false);
  city(1470 + o[0], 790 + o[1], -1, 'BEYRUT', tR + 1.6, false);
  city(1610 + o[0], 790 + o[1], 1, 'ŞAM', tS, true);
  ctx.restore();
  stamp(ctx, 'ŞAM’A TAYİN · 1905', 80, 128, t - tR, d, { size: 48 });
}, { tr: { type: 'cut' } });

// C06c: Şam, gizli toplantı — çizgili (ablak) sivri kemerler, asma lamba, masa başında beş subay silueti; "VATAN VE HÜRRİYET" damgası
function a2_C06c_bg(g) {
  g.fillStyle = P.paper; g.fillRect(-140, -140, W + 280, H + 280);
  const wall = a2_R(-140, -140, W + 140, H + 140); a2_navy(g, wall, .7); plate(g, 'sepia', wall, { a: .3, flat: true });
  // kemerler: açık taş / sepya çizgili (Şam ablakı), içleri karanlık avlu
  for (const cx of [300, 960, 1620]) {
    const w = 440, y0 = 160, y1 = 760, arch = SP([[cx - w / 2, y1], [cx - w / 2, y0 + 200], [cx - w * .3, y0 + 40], [cx, y0 - 20], [cx + w * .3, y0 + 40], [cx + w / 2, y0 + 200], [cx + w / 2, y1]], true, .5);
    const outer = SP([[cx - w / 2 - 60, y1], [cx - w / 2 - 60, y0 + 190], [cx - w * .32 - 40, y0 - 10], [cx, y0 - 90], [cx + w * .32 + 40, y0 - 10], [cx + w / 2 + 60, y0 + 190], [cx + w / 2 + 60, y1]], true, .5);
    knock(g, outer, '#E6D8B6');
    g.save(); g.clip(outer); for (let k = 0; k < 12; k++) if (k % 2) plate(g, 'sepia', a2_R(cx - 400, y0 - 100 + k * 42, cx + 400, y0 - 70 + k * 42), { a: .6, flat: true }); g.restore();
    knock(g, arch); a2_navy(g, arch, cx === 960 ? .4 : .72);   // orta kemer: ay ışığındaki avlu (açık), yanlar karanlık
    inkStroke(g, arch, 3); inkStroke(g, outer, 2.4);
  }
  inkFill(g, PL([[950, 760], [956, 470], [966, 470], [972, 760]]));
  for (let k = 0; k < 7; k++) { const a = -PI / 2 + (k - 3) * .42, q = SP([[961, 470], [961 + Math.cos(a) * 60, 470 + Math.sin(a) * 40 - 10], [961 + Math.cos(a) * 120, 470 + Math.sin(a) * 80 + 30]], false); inkStroke(g, q, 7); }
  const fl = a2_R(-140, 760, W + 140, H + 140); knock(g, fl); plate(g, 'sepia', fl, { a: .85, flat: true }); plate(g, 'ink', fl, { a: .2, flat: true });
  for (let i = 0; i < 9; i++) cut(g, PL([[-140, 790 + i * 40], [W + 140, 790 + i * 40]], false), 1.4, { a: .15 });
  // tek ışık kaynağı: asma lamba — kırık kenarlı düz halkalar (başlara ≥60 px), yerde ışık havuzu
  for (const [r, col, sd] of [[140, '#C9B48B', 1], [100, '#DCCAA3', 2], [62, '#EFE3C4', 3]]) knock(g, a2_roughCircle(960, 318, r, 690 + sd, .03, 32), col);
  knock(g, a2_ell(960, 1000, 760, 140), '#CFBB92'); knock(g, a2_ell(960, 990, 560, 100), '#E3D3AE');
  // alçak masa (Şam işi sedef kakmalı), lamba altında açık
  const tb = SP([[640, 800], [1280, 800], [1240, 860], [680, 860]], true, .4); knock(g, tb, '#E3D3AE'); inkStroke(g, tb, 3);
  const fr = a2_R(690, 860, 1230, 1000); knock(g, fr); plate(g, 'sepia', fr, { a: .85, flat: true }); inkStroke(g, fr, 3); for (let x = 720; x < 1220; x += 50) cut(g, a2_ell(x, 930, 12, 12), 1.6, { a: .45 });
  paperSheet(g, 960, 828, 220, 52, .02, 691, { rows: 1, shadow: false });
}
a2_shot(Wd('C06', 'yeni'), S('D01'), (ctx, st) => {
  setReg(603);
  paperBG(ctx);
  const { t, lt, d } = st, tq = a2_q(t);
  const tV = Wd('C06', 'vatan');
  const cm = a2_camAt(lt, d, { x: W / 2, y: H / 2 + 10, z: 1.0 }, { x: W / 2, y: H / 2 - 20, z: 1.06 });
  ctx.save(); cam(ctx, cm, .6); ctx.drawImage(a2_cache('c06c-bg', 140, a2_C06c_bg).c, -140, -140, W + 280, H + 280); ctx.restore();
  ctx.save(); cam(ctx, cm, 1);
  gasLamp(ctx, 960, 300, .8, t);
  // beş subay (aynı ölçek; Mustafa Kemal kadronun içinde, ortada sağda): öne eğilip masadaki kâğıda bakarlar
  const lean = E.io2(clamp((tq - Wd('C06', 'cemiyet') + .2) / .6)) * .05;
  const G = [
    { x: 380, y: 470, s: .92, dir: 1, col: 'navy', mus: true, seed: 81 },
    { x: 1540, y: 474, s: .92, dir: -1, col: 'navy', mus: true, seed: 83 },
    { x: 560, y: 520, s: 1.02, dir: 1, col: 'ink', mus: true, seed: 85 },
    { x: 1370, y: 526, s: 1.02, dir: -1, col: 'ink', mus: true, seed: 3 },
    { x: 760, y: 560, s: 1.06, dir: 1, col: 'ink', mus: false, seed: 87 },
  ];
  for (const f of G) { ctx.save(); ctx.translate(f.x, f.y + 320); ctx.rotate(lean * f.dir); ctx.translate(-f.x, -(f.y + 320)); a2_profile(ctx, f.x, f.y, f.s, f.dir, { len: (H + 60 - f.y) / f.s, col: f.col, mus: f.mus, seed: f.seed, reach: f.col === 'ink' ? [f.x + f.dir * 150 * f.s, 812] : null }); ctx.restore(); }
  ctx.restore();
  stamp(ctx, 'ŞAM · 1905–06', 80, 128, lt, (tV - .1) - (t - lt), { size: 48 });   // VATAN VE HÜRRİYET gelmeden kalkar
  // VATAN VE HÜRRİYET damgası
  if (!NOTEXT && t >= tV) {
    const k = 1 + (1 - E.out3(clamp((t - tV) / .18))) * .22, a = clamp((t - tV) / .06);
    ctx.save(); ctx.globalAlpha = a; ctx.translate(W / 2, 176); ctx.scale(k, k); ctx.rotate(.02);
    const bw = 1080, bh = 150, box = PL(rough([[-bw / 2, -bh / 2], [bw / 2, -bh / 2], [bw / 2, bh / 2], [-bw / 2, bh / 2]], 1.2, 79));
    plate(ctx, 'ink', PL([[-bw / 2 + 10, -bh / 2 + 12], [bw / 2 + 10, -bh / 2 + 12], [bw / 2 + 10, bh / 2 + 12], [-bw / 2 + 10, bh / 2 + 12]]), { a: .4 });
    knock(ctx, box); inkStroke(ctx, box, 4); inkStroke(ctx, a2_R(-bw / 2 + 12, -bh / 2 + 12, bw / 2 - 12, bh / 2 - 12), 1.6);
    txt(ctx, 'VATAN VE HÜRRİYET', 0, 6, FONT.title(92), { align: 'center', base: 'middle', ls: 3 });
    ctx.restore();
  }
}, { tr: { type: 'cut' }, post: a2_NIGHT });
