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
    if (kind === 'sarik') { const tp = SP([[26, -40], [32, -62], [16, -86], [-14, -96], [-44, -88], [-62, -62], [-60, -30], [-20, -40]], true, .8); knock(ctx, tp, P.paperD); plate(ctx, o.col, tp, { a: (o.a ?? .8) * .25, flat: true }); inkStroke(ctx, tp, 1.6 / s, { a: .7 }); }
    if (o.arm) plate(ctx, o.col, a6_armPath(o.arm), { a: o.a ?? .8, flat: true });
    ctx.restore(); return;
  }
  ctx.restore();
  a0_prof(ctx, x, y, s, 1, kind, { ...o, bot: 420 });
  if (o.arm) { ctx.save(); ctx.translate(x, y); ctx.rotate(o.tilt || 0); ctx.scale(s, s); const ap = a6_armPath(o.arm); inkFill(ctx, ap); cut(ctx, SP([[30, 96], [44, 40], [40, -40]], false), 1.6 / s, { a: .3 }); ctx.restore(); }
}
// bir derinlik sırasını tek kalıpta bas: siluetlerin birleşimi bir kez (çakışmalar koyulaşmaz); beyaz sarıklar üstte
const A6_TMP = {};
const A6_SARIK = [[26, -40], [32, -62], [16, -86], [-14, -96], [-44, -88], [-62, -62], [-60, -30], [-20, -40]];
function a6_rowPrint(ctx, items, col, a, o = {}) {
  if (!A6_TMP.c) { A6_TMP.c = makeCanvas(DW, DH); A6_TMP.g = A6_TMP.c.getContext('2d'); }
  const g = A6_TMP.g, m = ctx.getTransform(), [dx, dy] = regOf(col);
  g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, DW, DH);
  g.setTransform(m); g.translate(dx, dy); g.fillStyle = P[col];
  for (const it of items) {
    g.save(); g.translate(it.x, it.y); g.rotate(it.tilt || 0); g.scale(it.s, it.s);
    g.fill(a0_profPath({ seed: it.seed, bot: 420 }));
    // başlık: it.hat (0..1) kadar kalkık elde, havada
    const hat = it.kind === 'kalpak' ? SP(A0_KALPAK, true, .25) : it.kind === 'fes' ? SP(A0_FES, true, .2) : it.kind === 'sarik' ? SP(A6_SARIK, true, .8) : null;
    if (hat) { g.save(); if (it.hat) g.translate(34 * it.hat, -120 * it.hat); g.fill(hat); g.restore(); }
    if (it.arm) g.fill(a6_armPath(it.arm));
    g.restore();
  }
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (o.knock !== false) { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-in'; g.fillStyle = P.paper; g.fillRect(0, 0, DW, DH); g.restore(); ctx.drawImage(A6_TMP.c, 0, 0);
    g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalCompositeOperation = 'source-in'; g.fillStyle = P[col]; g.fillRect(0, 0, DW, DH); g.restore(); }
  ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = a; ctx.drawImage(A6_TMP.c, 0, 0); ctx.restore();
  for (const it of items) if (it.kind === 'sarik') {
    ctx.save(); ctx.translate(it.x, it.y); ctx.rotate(it.tilt || 0); ctx.scale(it.s, it.s); if (it.hat) ctx.translate(34 * it.hat, -120 * it.hat);
    const tp = SP(A6_SARIK, true, .8); knock(ctx, tp, P.paperD); plate(ctx, col, tp, { a: a * .2, flat: true });
    for (let k = 0; k < 3; k++) inkStroke(ctx, SP([[28 - k * 3, -48 - k * 12], [-10, -54 - k * 12], [-56, -42 - k * 12]], false), 1.4 / it.s, { a: .5 });
    inkStroke(ctx, tp, 1.8 / it.s, { a: .8 }); ctx.restore();
  }
}
// kalkık kol (yumruk / açık el): u 0..1 kalkış
function a6_armPath(u) {
  const ex = lerp(60, 48, u), ey = lerp(200, 30, u), hx = lerp(70, 54, u), hy = lerp(300, -90, u);
  const p = new Path2D();
  spl(p, [[20, 100], [ex + 14, ey], [hx + 13, hy + 6], [hx + 10, hy - 20], [hx - 12, hy - 22], [hx - 12, hy + 6], [ex - 14, ey], [-10, 110]], true, .6);
  return p;
}
// Birinci Meclis salonu: arka duvar, yüksek pencereler, ahşap dinleyici locası, levha, kürsü (önbellek)
function a6_tbmmBG(g) {
  paperBG(g);
  plate(g, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .3 });
  const beam = PL([[-20, -20], [W + 20, -20], [W + 20, 40], [-20, 44]]); plate(g, 'ochre', beam, { n: 2 }); plate(g, 'sepia', beam, { a: .4 }); inkStroke(g, PL([[-20, 44], [W + 20, 40]], false), 3.4);
  for (let i = 0; i < 6; i++) { const x0 = 70 + i * 196, win = PL([[x0, 60], [x0 + 110, 60], [x0 + 110, 128], [x0, 128]]); knock(g, win); plate(g, 'navy', win, { a: .85 }); halftone(g, 'navy', win, .3, { cell: 10 }); inkStroke(g, win, 3); inkStroke(g, PL([[x0 + 55, 60], [x0 + 55, 128]], false), 2.4); }
  for (const lx of [330, 900]) { for (const [rr, a] of [[110, .15], [68, .28]]) { const q = new Path2D(); q.ellipse(lx, 146, rr * 1.2, rr * .8, 0, 0, TAU); plate(g, 'gold', q, { a }); } }
  for (const lx of [330, 900]) gasLamp(g, lx, 136, .72, 0);
  // ahşap lambri
  const pan = PL([[-20, 610], [W + 20, 610], [W + 20, H + 20], [-20, H + 20]]); plate(g, 'ochre', pan, { a: .6 }); plate(g, 'sepia', pan, { a: .2 });
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
}
// dinleyici locasının korkuluğu (saydam katman: arkasındaki dinleyiciler canlı çizilir)
function a6_tbmmRail(g) {
  const rail = PL([[-20, 330], [1250, 330], [1250, 340], [-20, 340]]); knock(g, rail); plate(g, 'ochre', rail, { n: 2 }); inkStroke(g, rail, 2.4);
  const fas = PL([[-20, 392], [1250, 392], [1250, 424], [-20, 424]]); knock(g, fas); plate(g, 'ochre', fas, { n: 2 }); plate(g, 'sepia', fas, { a: .4 }); inkStroke(g, fas, 2.8);
  for (let x = 6; x < 1250; x += 22) { const bl = PL([[x, 340], [x + 8, 340], [x + 8, 392], [x, 392]]); knock(g, bl); plate(g, 'ochre', bl, { n: 2 }); inkStroke(g, bl, 1.4); }
  for (const x of [-4, 620, 1244]) { const post = PL([[x - 9, 330], [x + 9, 330], [x + 9, 430], [x - 9, 430]]); knock(g, post); plate(g, 'ochre', post, { n: 2 }); plate(g, 'ink', post, { a: .25 }); inkStroke(g, post, 2.2); }
}
// salon çizimi; zamanlar mutlak (iki salon çekimi saat ara çekimiyle bölünür, kamera kesintisiz sürer)
function a6_tbmm(ctx, t) {
  const FL = { x: 1250, y: 210, G: 300 }, T0 = S('G01') - 1.0, lt = t - T0, tf = Math.floor(t * 15) / 15;
  const tY = a0_W('G01', 'yaşasın') - T0, tS = a0_W('G01', 'sesler') - T0;
  // doruk: "yaşasın"dan 3,6 sn boyunca kesintisiz 1,00 → 1,05 ek yaklaşma (yalnız sahne katmanı)
  const p = ramp(lt, 0, 10.4, E.lin), pk = ramp(lt, tY - .03, tY + 3.6, E.lin), c = { x: 960 + 50 * p, y: 540 - 20 * p - 18 * pk, z: (1 + .07 * p) * (1 + .05 * pk) };
  const [sx, sy] = shake(lt, tY, 5, 5, 18); c.sx = sx; c.sy = sy;
  a0_layer(ctx, a0_cache('a6-tbmm-bg', a6_tbmmBG), c, .75);
  // dinleyici locası: "yaşasın"da kalpaklar ve eller kalkar (2 pozlu, 15 fps, kişi başına 0–0,15 sn gecikme)
  { const r = rng(13), wv = Math.floor(tf * 4) % 2;
    ctx.save(); cam(ctx, c, .75);
    a6_rowPrint(ctx, Array.from({ length: 17 }, (_, i) => { const x = 30 + i * 72 + r() * 20, dl = r() * .15, k = ['kalpak', 'fes', 'bare', 'kalpak', 'sarik'][i % 5], up = lt >= tY + dl ? 1 : 0, pose = (wv + i) % 2;
      return { x, y: 324 - up * 6 * pose, s: .36, kind: k, seed: 760 + i, tilt: idleOffsets(tf, 760 + i, 1.5).head, hat: up && (k === 'kalpak' || k === 'fes') ? (pose ? 1 : .8) : 0, arm: up ? (pose ? 1 : .85) : 0 }; }), 'navy', .5);
    ctx.drawImage(a0_cache('a6-tbmm-rail', a6_tbmmRail), 0, 0, W, H);
    ctx.restore(); }
  ctx.save(); cam(ctx, c, .9);
  const un = ramp(lt, tY - .1, tY + .7, E.out3), mP = ctx.getTransform(), poleScr = (mP.a * FL.x + mP.c * 260 + mP.e) / RS;
  a6_pole(ctx, FL.x, FL.y - 30, 980);
  a6_flag(ctx, FL.x + 5, FL.y, FL.G, t, { unfurl: un, amp: FL.G * lerp(.18, .09, un), droop: (1 - un) * .3 });
  ctx.restore();
  // kalabalık: "sesler"de arka sıralar ayağa kalkar (oturuştan kademeli); "yaşasın"da kollar kalkar
  const cheer = u0 => ramp(lt, tY + u0, tY + u0 + .25, E.out3);
  const rise = i => { const tl = Math.floor(lt * 15) / 15; return ramp(tl, tS + i * .03, tS + i * .03 + .4, E.outBack); };
  const kinds = ['kalpak', 'fes', 'sarik', 'kalpak', 'bare', 'kalpak', 'fes', 'kalpak', 'bald', 'kalpak', 'fes', 'kalpak', 'sarik', 'kalpak'];
  ctx.save(); cam(ctx, c, .95);
  a6_rowPrint(ctx, kinds.map((k, i) => ({ x: 40 + i * 92, y: 470 + (i % 3) * 6 + 64 * (1 - rise(i)), s: .62, kind: k, seed: 700 + i, tilt: idleOffsets(tf, 700 + i, 1.5).head, arm: i % 3 === 1 ? cheer(.05 * i) : 0 })), 'navy', .55);
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  const mid = ['kalpak', 'sarik', 'fes', 'kalpak', 'sarik', 'bare', 'kalpak', 'fes', 'kalpak', 'sarik'];
  // orta sıra: tek baskı; beyaz sarıklı mebuslar sarığıyla seçilir
  a6_rowPrint(ctx, mid.map((k, i) => ({ x: 10 + i * 128, y: 506 + (i % 2) * 10 + 84 * (1 - rise(i + 3)), s: .86, kind: k, seed: 720 + i, tilt: idleOffsets(tf, 720 + i, 1.4).head * .7, arm: i % 2 === 0 ? cheer(.08 + .04 * i) : 0 })), 'navy', .9);
  ctx.restore();
  ctx.save(); cam(ctx, c, 1.08);
  // ön sıra: dört anonim mebus (o akşam Meclis'te olduğu kesin olmayan kimse tanınır çizilmez); "yaşasın"da başlar bayrağa döner
  const front = [
    { x: 190, who: 'anon', id: { mus: 'mk', jaw: 1.0, WD: 1.12, brow: -.05, seed: 81 }, gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 44, seed: 81 },
    { x: 500, who: 'anon', id: { mus: 'mk', hair: 'grey', WD: 1.1, seed: 82 }, gear: 'fes', coat: 'civil', col: 'navy', age: 50, seed: 82 },
    { x: 810, who: 'anon', id: { mus: 'thin', hair: 'grey', jaw: 1.06, WD: 1.06, seed: 83 }, gear: 'kalpak', coat: 'civil', col: 'ink', age: 52, seed: 83 },
    { x: 1110, who: 'anon', id: { mus: 'mk', beard: 'short', hair: 'ink', WD: 1.1, jaw: 1.08, seed: 84 }, gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 48, seed: 84 },
  ];
  front.forEach((f, i) => {
    const up = cheer(.12 + i * .07), tq = ramp(Math.floor(lt * 15) / 15, tY + .05 + i * .06, tY + .45 + i * .06, E.out2);
    a0_fig(ctx, { ...f, y: 560, s: 1.28, dir: 1, w: .98, len: 420, lookAt: [lerp(FL.x - 60, FL.x + 220, tq), lerp(520, 250, tq)], tilt: -.08 * tq, hx: 7 * tq, sep: true, turn: lerp(.2, .45, tq) }, t);
  });
  ctx.restore();
  chapterCard(ctx, 'VI', 'CUMHURİYET', 'TBMM · 29 EKİM 1923 · 20.30', lt - .5, 2.75);
  // bayrağın solunda ve üstünde: bayrak açıkta kalır (ölçek çapası metnin ortası; sol ≥96, gönderle arası ≥30)
  if (!NOTEXT && lt >= tY) {
    // ekran koordinatında (genel kayma geri alınır): gönderin ekrandaki yeri ölçülür; sol ≥96, gönderle arası ≥30
    const xr = Math.min(1190, poleScr - 30), xl = 96;
    const u = clamp((lt - tY) / .18), k = 1 + (1 - E.out3(u)) * .08;
    ctx.save(); ctx.font = FONT.title(90); ctx.letterSpacing = '2px'; const tw = ctx.measureText('YAŞASIN CUMHURİYET!').width; ctx.restore();
    const cx0 = Math.min(620, (xl + xr) / 2), half = Math.min(cx0 - xl, xr - cx0) - 2, fs = Math.min(90, 90 * 2 * half / tw), kk = Math.min(k, 2 * half / (tw * fs / 90));
    ctx.save(); if (window.DRIFT && typeof undrift === 'function') undrift(ctx); ctx.globalAlpha = Math.min(1, u * 3); ctx.translate(cx0, 242); ctx.scale(kk, kk);
    txt(ctx, 'YAŞASIN CUMHURİYET!', 0, 0, FONT.title(fs), { align: 'center', base: 'middle', ls: 2 });
    ctx.restore();
  }
}
// duvar saati (sakaklı, rakamsız kadran): "saat sekiz buçukta" — yelkovan "buçukta" 29'dan 30'a atlar
function a6_saatBG(g) {
  paperBG(g);
  plate(g, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .3 });
  const pan = PL([[-20, 900], [W + 20, 900], [W + 20, H + 20], [-20, H + 20]]); plate(g, 'ochre', pan, { n: 2 }); plate(g, 'sepia', pan, { a: .35 }); inkStroke(g, PL([[-20, 900], [W + 20, 900]], false), 3.4);
  // kasa
  plate(g, 'ink', PL([[716, 136], [1236, 136], [1236, 1010], [716, 1010]]), { a: .3 });
  const cs = SP([[700, 190], [760, 140], [960, 108], [1160, 140], [1220, 190], [1220, 996], [700, 996]], true, .3); knock(g, cs); plate(g, 'ochre', cs, { n: 2 }); plate(g, 'sepia', cs, { a: .45 }); inkStroke(g, cs, 4);
  const door = PL([[820, 660], [1100, 660], [1100, 960], [820, 960]]); knock(g, door, P.paperD); plate(g, 'ochre', door, { a: .25 }); inkStroke(g, door, 3); inkStroke(g, PL([[834, 674], [1086, 674], [1086, 946], [834, 946]]), 1.4);
  const bez = new Path2D(); bez.arc(960, 420, 214, 0, TAU); knock(g, bez); plate(g, 'gold', bez, { a: .75 }); plate(g, 'ochre', bez, { a: .35 }); inkStroke(g, bez, 3.4);
  const face = new Path2D(); face.arc(960, 420, 196, 0, TAU); knock(g, face, '#F4EEDF'); inkStroke(g, face, 2.4);
  const inner = new Path2D(); inner.arc(960, 420, 150, 0, TAU); inkStroke(g, inner, 1.2, { a: .6 });
  for (let k = 0; k < 60; k++) { const a = k / 60 * TAU, big = k % 5 === 0, r0 = big ? 158 : 172, r1 = 186; inkStroke(g, PL([[960 + Math.cos(a) * r0, 420 + Math.sin(a) * r0], [960 + Math.cos(a) * r1, 420 + Math.sin(a) * r1]], false), big ? (k % 15 === 0 ? 7 : 5) : 1.4, { cap: 'butt' }); }
}
function a6_hand(ctx, cx, cy, ang, L, w) { const c = Math.cos(ang), s_ = Math.sin(ang), n = [-s_, c]; inkFill(ctx, PL([[cx - c * L * .16 + n[0] * w * .5, cy - s_ * L * .16 + n[1] * w * .5], [cx + c * L, cy + s_ * L], [cx - c * L * .16 - n[0] * w * .5, cy - s_ * L * .16 - n[1] * w * .5]])); }
function a6_shotTBMM() {
  shot(S('G01') - 1.0, (ctx, st) => { setReg(601); paperBG(ctx); a6_tbmm(ctx, st.t); }, { tr: { type: 'press', dur: .7 }, post: { vig: .95 } });
  // ara çekim: saat 20.30
  shot(a0_W('G01', 'saat') - .1, (ctx, st) => {
    setReg(603); paperBG(ctx);
    const T0 = st.t - st.lt, p = ramp(st.lt, 0, st.d + .3, E.io2), c = { x: 960 + 20 * p, y: 540 - 26 * p, z: 1 + .05 * p };
    a0_layer(ctx, a0_cache('a6-saat-bg', a6_saatBG), c, 1);
    ctx.save(); cam(ctx, c, 1);
    const tq = Math.floor(st.t * 15) / 15;
    // sarkaç (cam kapak ardında)
    const sw = Math.sin(tq * PI * 1.2) * .2, px = 960 + Math.sin(sw) * 230, py = 650 + Math.cos(sw) * 230;
    ctx.save(); ctx.beginPath(); ctx.rect(834, 674, 252, 272); ctx.clip();
    inkStroke(ctx, PL([[960, 650], [px, py]], false), 5); const bob = new Path2D(); bob.arc(px, py, 34, 0, TAU); knock(ctx, bob); plate(ctx, 'gold', bob, { a: .85 }); plate(ctx, 'ochre', bob, { a: .4 }); inkStroke(ctx, bob, 2.6);
    ctx.restore();
    const tB = a0_W('G01', 'buçuk') - T0, m = st.lt < tB ? 29 : 30 + settle(st.lt, tB, .25, 3, 7), h = 8 + m / 60;
    a6_hand(ctx, 960, 420, h / 12 * TAU - PI / 2, 108, 18);
    a6_hand(ctx, 960, 420, m / 60 * TAU - PI / 2, 166, 12);
    const cap = new Path2D(); cap.arc(960, 420, 12, 0, TAU); knock(ctx, cap); plate(ctx, 'gold', cap); inkStroke(ctx, cap, 2);
    ctx.restore();
    stamp(ctx, 'SAAT 20.30', 1330, 320, st.lt + .3, st.d - .2, { size: 44 });
  }, { tr: { type: 'cut' }, post: { vig: .95 } });
  shot(a0_W('G01', 'meclis') - .1, (ctx, st) => { setReg(601); paperBG(ctx); a6_tbmm(ctx, st.t); }, { tr: { type: 'cut' }, post: { vig: .95 } });
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
      { x: XS[1], app: tM - .25, who: 'mk', gear: null, coat: 'civil', col: 'ink', age: 42, seed: 3, name: 'MUSTAFA KEMAL', sub: '42 yaşında · Cumhurbaşkanı', tn: tM, dip: 'ERKÂN-I HARBİYE · 1905' },
      { x: XS[0], app: tI - .15, who: 'ismet', gear: 'kalpak', coat: 'kaput', col: 'khaki', age: 39, seed: 5, name: 'İSMET', sub: '39 yaşında · Başvekil', tn: tI, dip: 'ERKÂN-I HARBİYE · 1906' },
      { x: XS[2], app: tF - .15, who: 'fevzi', gear: 'kalpak', gearCol: 'grey', coat: 'kaput', col: 'khaki', age: 47, seed: 7, name: 'FEVZİ', sub: '47 yaşında · Erkân-ı Harbiye Reisi', tn: tF, dip: 'ERKÂN-I HARBİYE · 1898' },
    ];
    ctx.save(); cam(ctx, c, 1);
    ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
    for (const f of L) {
      const h = a0_hit(st.lt, f.app, .14); if (h.a <= 0) continue;
      ctx.save(); ctx.globalAlpha = h.a; ctx.translate(f.x, B1); ctx.scale(h.k, h.k); ctx.translate(-f.x, -B1);
      const rb = REG.boost; REG.boost = rb * (1 + 5 * (1 - E.out3(clamp((st.lt - f.app) / .35))));
      a0_fig(ctx, { ...f, y: 438, s: 2.12, dir: -1, w: .98, len: (B1 - 438) / 2.12 + 10, look: [.3, .25], idle: .8 }, st.t);
      REG.boost = rb; ctx.restore();
    }
    ctx.restore();
    ctx.restore();
        const tEnd = [tI - .1, tF - .1, st.d];
    L.forEach((f, k) => nameTag(ctx, k === 2 ? 1824 : f.x, 96, f.name, f.sub, st.lt - f.tn, tEnd[k] - f.tn, { align: k === 2 ? 'right' : 'center', size: 64, sub: 40 }));
    stamp(ctx, '30 EKİM 1923', 100, 92, st.lt - (a0_W('G02', 'ertesi') - T0), tI - (a0_W('G02', 'ertesi') - T0) - .05, { size: 48 });
    // "aynı": üç diplomayı bağlayan kırmızı çizgi (aynı okul)
    { const ta = a0_W('G02', 'aynı') - T0, u = E.out3(ramp(st.lt, ta, ta + .6));
      if (u > 0) { const x0 = XS[0] - 230, x1 = lerp(x0, XS[2] + 230, u); plate(ctx, 'red', PL([[x0, 1022], [x1, 1022], [x1, 1030], [x0, 1030]]));
        for (const x of XS) if (x1 >= x) { const d = new Path2D(); d.arc(x, 1026, 9, 0, TAU); knock(ctx, d); plate(ctx, 'red', d); inkStroke(ctx, d, 2); } } }
    // "Üçü de aynı kurmay okulunun mezunuydu": diplomalar sırayla damgalanır
    const tD = a0_W('G02', 'üçü') - T0;
    [1, 0, 2].forEach((k, j) => a6_diploma(ctx, L[k].x, 852, [-.03, .02, -.015][k], 640 + k, st.lt - tD - j * .28, L[k].dip));
  }, { tr: { type: 'press', dur: .5 }, post: { vig: .9 } });
}

// ——— G03 · 1924: şerit çatlar; ama hepsi aynı yerden: okul sırası ve siper ———
const A6_SIX = [
  { who: 'karabekir', gear: 'kalpak', coat: 'civil', col: 'ink', age: 42, seed: 11, lab: 'KARABEKİR', w: 'karabekir' },
  { who: 'alifuat', gear: 'kalpak', coat: 'civil', col: 'sepia', age: 42, seed: 13, lab: 'ALİ FUAT', w: 'ali' },
  { who: 'rauf', gear: 'fes', coat: 'civil', col: 'navy', age: 43, seed: 15, lab: 'RAUF', w: 'rauf' },
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
      for (const i of [0, 1, 2, 3, 4, 5]) a0_fig(ctx, { ...A6_SIX[i], x: A6_X6[i], y: 412, s: 1.26, dir: -1, w: .96, len: (B1 - 412) / 1.26 + 10, look: [.3, .25] }, st.t);
      ctx.restore();
      // adlar: ayrılan üçü, söylendikleri anda
      for (const i of (crack > 0 ? hv.idx : [0, 1, 2])) if (A6_SIX[i].lab) { const tl = a0_W('G03', A6_SIX[i].w) - T0; label(ctx, A6_SIX[i].lab, A6_X6[i], 812, FONT.mono(34), { align: 'center', ls: 4, a: ramp(st.lt, tl, tl + .3) }); }
      ctx.restore();
      if (crack > 0) inkStroke(ctx, PL(tear.filter(([, y]) => y <= yC + 26).map(([x, y]) => [x, Math.min(y, yC)]), false), 3.4);
      ctx.restore();
    });
    ctx.restore();
    { ctx.save(); ctx.font = FONT.mono(48); ctx.letterSpacing = '4px'; const sw = ctx.measureText('TERAKKİPERVER CUMHURİYET FIRKASI · 1924').width; ctx.restore();
      stamp(ctx, 'TERAKKİPERVER CUMHURİYET FIRKASI · 1924', 960 - sw / 2, 1000, st.lt - tM - .2, tA - tM + .3, { size: 48 }); }
    // yazılar çatlağın üstünde, kâğıt bant üzerinde
    const band = (x0, y0, x1, y1, a, sd) => { if (a <= 0) return; ctx.save(); ctx.globalAlpha = a; const b = PL(rough([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], 1.2, sd)); knock(ctx, b); inkStroke(ctx, b, 2.4); ctx.restore(); };
    if (!NOTEXT) { const a1 = ramp(st.lt, tC - .3, tC); band(810, 36, 1110, 128, a1, 5); label(ctx, '1924', W / 2, 108, FONT.title(78), { align: 'center', ls: 4, a: a1 });
      const ty = ramp(st.lt, tA + .4, tA + .9); band(700, 868, 1220, 958, ty, 6); label(ctx, 'AYNI YERDEN', W / 2, 936, FONT.title(64), { align: 'center', ls: 4, a: ty }); }
  }, { tr: { type: 'cut' }, post: { vig: .9 } });
  // "bir okul sırasından…": A04'teki 1893 karesinin aynısı (aynı kadraj, aynı yaş satırı)
  shot(a0_W('G03', 'okul') - .15, (ctx, st) => {
    setReg(137);
    paperBG(ctx);
    const p0 = ramp(a0_W('A04', 'otuz'), A0_CAM0, A0_CAM1, E.lin);
    a0_class93(ctx, st.t, p0 + .18 * ramp(st.lt, 0, st.d, E.lin));
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
    // Arıburnu, 25 Nisan 1915: Fevzi 39, İsmet 30, Mustafa Kemal 33, Karabekir 33, Ali Fuat 32
    const kab = [{ who: 'fevzi', age: 39 }, { who: 'ismet', age: 30 }, { who: 'mk', age: 33 }, { who: 'karabekir', age: 33 }, { who: 'alifuat', age: 32 }];
    // süngü uçları (başların arkasında)
    for (let i = 0; i < 5; i++) { const x = A0_XS[i] + 90; inkStroke(ctx, PL([[x, 640], [x + 30, 240]], false), 6); inkFill(ctx, PL([[x + 27, 250], [x + 33, 250], [x + 34, 190]])); }
    kab.forEach((f, i) => a0_fig(ctx, { x: A0_XS[i], y: 430, s: 1.26, dir: -1, w: .96, len: 260, ...f, gear: 'kabalak', coat: 'setre', col: 'khaki', look: [.3, .25], seed: 90 + i }, st.t));
    // ön siper: kum torbaları
    const r = rng(5);
    for (let row = 0; row < 3; row++) for (let i = -1; i < 14; i++) {
      const x = i * 150 + (row % 2) * 75, y = 590 + row * 52, sb = SP(rough([[x, y], [x + 150, y + 2], [x + 152, y + 52], [x - 2, y + 54]], 4, row * 31 + i), true, .9);
      knock(ctx, sb); plate(ctx, 'khaki', sb, { a: .7 + r() * .2 }); plate(ctx, 'ochre', sb, { a: .3 }); inkStroke(ctx, sb, 2.6);
      inkStroke(ctx, SP([[x + 20, y + 14], [x + 70, y + 10], [x + 130, y + 16]], false), 1.2, { a: .4 });
    }
    ctx.restore();
    ctx.restore();
    [39, 30, 33, 33, 32].forEach((a, i) => a0_age(ctx, A0_XS[i], 862, a, 'yaşında', st.lt + .3 - Math.abs(i - 2) * .06));
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
    // tebeşir: "ders"te dersin cümlesi harf harf yazılır; "yazılır"da altı çizilir
    const tw = a0_W('G04', 'ders') - T0, s1 = 'Cumhuriyet 103 yaşında';
    const n = Math.floor(clamp((st.lt - tw) / 1.2) * s1.length);
    if (n > 0) txt(ctx, s1.slice(0, n), 960, 312, FONT.quote(76), { align: 'center', col: '#EDE6D2' });
    const tz = a0_W('G04', 'yazılır') - T0, uz = E.out2(ramp(st.lt, tz, tz + .45));
    if (uz > 0) cut(ctx, SP([[660, 336], [lerp(660, 1262, uz * .5), 340], [lerp(660, 1262, uz), 334]], false), 4.5, { col: '#EDE6D2', a: .9 });
    ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
    A6_KIDS.forEach((f, i) => a0_fig(ctx, { who: 'anon', id: f.id, x: A0_XS[i], y: 452, s: 1.2, dir: -1, w: .84, len: (B1 - 452) / 1.2 + 10, age: 12, gear: null, coat: 'plain', col: f.col, look: [.2, .25], seed: 60 + i,
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
    ctx.save(); cam(ctx, c, 1); a6_teacher(ctx, 900, 672, 1.0, st.t);
    // öğretmen kürsüsü (bacakları örter)
    const kt = PL(rough([[748, 712], [1132, 712], [1124, 736], [756, 736]], .8, 3)); knock(ctx, kt); plate(ctx, 'ochre', kt, { n: 2 }); inkStroke(ctx, kt, 3);
    const kf = PL([[760, 736], [1120, 736], [1120, 1100], [760, 1100]]); knock(ctx, kf); plate(ctx, 'ochre', kf, { n: 2 }); plate(ctx, 'sepia', kf, { a: .45 }); inkStroke(ctx, kf, 3);
    inkStroke(ctx, PL([[790, 770], [1090, 770], [1090, 1060], [790, 1060]]), 1.8, { a: .6 });
    paperSheet(ctx, 1050, 694, 96, 44, -.04, 33, { rows: 0, shadow: false }); const iw = new Path2D(); iw.ellipse(800, 706, 14, 6, 0, 0, TAU); inkFill(ctx, iw);
    ctx.restore();
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
      ctx.save(); ctx.font = FONT.title(108); ctx.letterSpacing = '2px'; const mw = ctx.measureText('ÖĞRETMEN'); ctx.letterSpacing = '0px'; const mq = ctx.measureText('?'); ctx.restore();
      const inkR = mw.actualBoundingBoxRight, qL = mq.actualBoundingBoxLeft, qW = mq.actualBoundingBoxLeft + mq.actualBoundingBoxRight, tot = inkR + 4 + qW, gx = cx - tot / 2;
      txt(ctx, 'ÖĞRETMEN', gx, y0 + 384, FONT.title(108), { ls: 2 });
      txt(ctx, '?', gx + inkR + 4 + qL, y0 + 384, FONT.title(108), { plate: 'red' });
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
    const tSg = a0_W('G06', 'saygıyla') - T0, hoist = ramp(st.lt, tSg - .4, tSg + 1.6, E.io2);
    a6_pole(ctx, 700, 40, 330, { w: 7, r: 10 });
    // ip ve makara izi gönder boyunca
    inkStroke(ctx, PL([[708, 44], [708, 330]], false), 1.4, { a: .55 });
    ctx.save(); ctx.beginPath(); ctx.rect(600, -100, 900, B0 + 100); ctx.clip();
    a6_flag(ctx, 704, lerp(B0 + 6, 56, hoist), 220, st.t, { amp: lerp(10, 18, hoist), speed: 2.6 });
    ctx.restore();
    ctx.restore();
    ctx.save(); cam(ctx, c, 1);
    ctx.save(); ctx.beginPath(); ctx.rect(-40, B0 + 2, W + 80, B1 - B0 - 4); ctx.clip();
    const tAt = a0_W('G06', 'atatürkü') - T0, tKu = a0_W('G06', 'kuşağını') - T0;
    a0_seven(ctx, st.t, st.lt, [tKu + .3, tKu + .15, tKu, tAt, tKu, tKu + .15, tKu + .3], { y: 524, s: 1.0, yb: B1, xs: [240, 480, 720, 960, 1200, 1440, 1680] });
    ctx.restore();
    ctx.restore();
    if (!NOTEXT) {
      const t1 = a0_W('G06', 'cumhuriyetimizin') - T0, t2 = a0_W('G06', 'kutlu') - T0;
      const h1 = a0_hit(st.lt, t1, .2), h2 = a0_hit(st.lt, t2, .2);
      if (h1.a > 0) { ctx.save(); ctx.globalAlpha = h1.a; ctx.translate(960, 876); ctx.scale(h1.k, h1.k); txt(ctx, 'CUMHURİYETİMİZİN 103. YILI', 0, 0, FONT.title(88), { align: 'center', ls: 2 }); ctx.restore(); }
      if (h2.a > 0) {
        ctx.save(); ctx.globalAlpha = h2.a; ctx.translate(960, 990); ctx.scale(h2.k, h2.k); txt(ctx, 'KUTLU OLSUN', 0, 0, FONT.title(88), { align: 'center', ls: 6, plate: 'red' }); ctx.restore();
      }
      const ta = a0_W('G06', 'anıyoruz') - T0;
      label(ctx, '29 EKİM 1923 — 29 EKİM 2026', 1220, 210, FONT.mono(34), { align: 'left', ls: 4, a: ramp(st.lt, ta, ta + .5) });
    }
  }, { tr: { type: 'press', dur: .6 }, post: { vig: .9 } });
}

// ——— Bitiş ekranı (~13 sn): solda sakin afiş, sağ yarı boş (YouTube abone ve video öğeleri) ———
function a6_shotBitis() {
  shot(Se('G06') + .5, (ctx, st) => {
    setReg(661);
    paperBG(ctx);
    const p = ramp(st.lt, 0, st.d, E.sine), c = { x: 960, y: 540 - 12 * p, z: 1.0 + .025 * p }; // afiş yavaşça yaklaşır; sağ yarı (YouTube öğeleri) yazıları sabit
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
    a6_flag(ctx, 303, 132, 200, st.t, { amp: 18, speed: 3.14 }); // ~0,5 Hz sürekli dalga
    // alt şerit: yedi baş küçük ölçekte
    ctx.save(); ctx.beginPath(); ctx.rect(X0 + 18, 814, X1 - X0 - 36, 178); ctx.clip();
    a0_seven(ctx, st.t, st.lt, [4.4, 4.2, 4.0, 3.8, 4.0, 4.2, 4.4].map(x => x + .9), { y: 900, s: .66, yb: 994, xs: [160, 266, 372, 480, 588, 694, 800], look: [.3, .25] });
    ctx.restore();
    a0_dust(ctx, st.t, [X0 + 24, Y0 + 24, X1 - 24, 800], 24, 661); // afişin önünde süzülen toz: bitiş ekranı da hiç durmaz
    ctx.restore();
    const L = st.lt, f = (t0) => ramp(L, t0, t0 + .35);
    ctx.save(); cam(ctx, c, 1); // afiş yazıları afişle birlikte
    label(ctx, '29 EKİM 1923', 480, 470, FONT.mono(36), { align: 'center', ls: 6, force: true, a: f(.6) });
    { const h = a0_hit(L, 1.2, .16); if (h.a > 0) { ctx.save(); ctx.globalAlpha = h.a; ctx.translate(480, 590); ctx.scale(h.k, h.k); txt(ctx, '103. YIL', 0, 50, FONT.title(150), { align: 'center', ls: 4 }); ctx.restore(); } }
    label(ctx, 'KUTLU OLSUN', 480, 740, FONT.title(64), { align: 'center', ls: 6, force: true, plate: 'red', a: f(2.0) });
    ctx.restore();
    // sağ yarı: yalnız yönlendirme yazıları; video öğesi (y ≈ 260–) ve abone öğesi (≈ 1420, 870) için alan boş
    // YouTube öğeleri 6:05'te açılır: yönlendirme yazıları hemen (365,3'te tam) görünür
    label(ctx, 'SIRADAKİ HİKÂYE', 1420, 175 + 20, FONT.title(56), { align: 'center', ls: 3, a: ramp(L, 0, .2) });
    { const u = E.out2(ramp(L, .05, .35)); if (u > 0) { const y1 = lerp(215, 275, u);
      if (window.DRIFT && typeof undrift === 'function') { ctx.save(); undrift(ctx); }
      inkStroke(ctx, SP([[1420, 215], [1423, (215 + y1) / 2], [1420, y1]], false), 4);
      if (u > .95) inkStroke(ctx, PL([[1404, 256], [1420, 277], [1437, 255]], false), 4);
      if (window.DRIFT && typeof undrift === 'function') ctx.restore(); } }
    label(ctx, 'ZAMAN KURYESİ’NE ABONE OL', 1420, 1010 + 11, FONT.mono(32), { align: 'center', ls: 3, a: ramp(L, 0, .2) });
  }, { tr: { type: 'press', dur: .8 }, post: { vig: .7 } });
}

a6_shotTBMM();
a6_shotUcBust();
a6_shotCatlak();
a6_shotBugun();
a6_shotSoru();
a6_shotAfis();
a6_shotBitis();
