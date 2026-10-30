// IV. MEKONE'DEKİ HİLE (E01–E16b): kurbanın kökeni, iki pay, bile bile aldanan Zeus, ateşin esirgenmesi ve çalınışı,
// Pandora ve küp; Erhat'ın okuması: yeni bir devrimin hazırlayıcısı, akıl gücü insanlara geçmiştir, üçüncü ve son devrim
'use strict';

// --- METOP frizi: tek uzun siyah figür friz, kamera pano pano kayar (E_ öneki) ---
const E_PW = 1500, E_GY = 820;
// pano çerçevesi: i. pano [i*E_PW, (i+1)*E_PW]; triglif bantları ve üst-alt kornişler
function E_frieze(ctx, i0, i1) {
  D_metope(ctx, i0 * E_PW, (i1 + 1) * E_PW, 120, 900, i1 - i0 + 1);
  ctx.fillStyle = C.ink; ctx.fillRect(i0 * E_PW, E_GY, (i1 - i0 + 1) * E_PW, 6);
}
// kamera: durak durak (her durak bir pano merkezi), durağa varınca hafif kayma
function E_cam(t, st, z = 1.2, lead = .8) {
  let i = 0; for (let k = 0; k < st.length; k++) if (t >= st[k][0] - lead) i = k;
  const a = st[Math.max(0, i - 1)], b = st[i], u = i === 0 ? 1 : E.io3(ramp(t, b[0] - lead, b[0], E.lin));
  const px = c => (c + .5) * E_PW;
  return { x: lerp(px(a[1]), px(b[1]), u) + (t - b[0]) * 10, y: 500, z: (b[2] ?? z) * (1 + .006 * Math.sin(t * .7)) };
}
const E_fig = (c, x, s, dir, lk, p = {}, o = {}) => bf(c, x, E_GY, s, dir, lk, { breath: Math.sin((window.FIG_T || 0) * 1.5 + x * .01) * .5, ...p }, o);
// uyluk kemiği: düz sap, iki ucunda çift topuz (eklenmiş beyaz, siyah kontur)
function E_bone(c, x, y, len, rot, col = C.bone) {
  c.save(); c.translate(x, y); c.rotate(rot); c.fillStyle = col; c.strokeStyle = C.ink; c.lineWidth = 2.4;
  c.beginPath(); c.rect(-len / 2, -7, len, 14); for (const e of [-1, 1]) { c.moveTo(e * len / 2 + 14, -9); c.arc(e * len / 2, -9, 14, 0, TAU); c.moveTo(e * len / 2 + 14, 9); c.arc(e * len / 2, 9, 14, 0, TAU); }
  c.fill(); c.stroke(); c.fillRect(-len / 2 + 2, -6, len - 4, 12); c.restore();
}
// iki pay bir sofranın (trapeza) üstünde: solda ağzı bağlı siyah işkembe torbası (iki eklenmiş kırmızı şerit),
// sağda topaklı yağ kütlesi (mat eklenmiş beyaz, dalgalı yağ kıvrımları); iki ucundan uyluk kemiği topuzları çıkar
function E_portions(c, x, y, o = {}) {
  const T = y - 120, ft = window.FIG_T || 0;
  // sofra: kalın tabla, iki kıvrık bacak
  c.fillStyle = C.ink; c.fillRect(x - 450, T, 900, 18);
  c.strokeStyle = C.clay; c.lineWidth = 2; c.beginPath(); c.moveTo(x - 440, T + 9); c.lineTo(x + 440, T + 9); c.stroke();
  for (const e of [-1, 1]) { c.fillStyle = C.ink; c.beginPath(); c.moveTo(x + e * 400, T + 16); c.quadraticCurveTo(x + e * 370, T + 70, x + e * 395, y - 8); c.lineTo(x + e * 420, y); c.lineTo(x + e * 380, y); c.quadraticCurveTo(x + e * 350, T + 70, x + e * 375, T + 16); c.closePath(); c.fill(); }
  // işkembe torbası: sofraya çökmüş, yamuk bir çuval; ağzı sağa yatık, iple bağlı, ip uçları sarkar
  const bx = x - 230;
  c.fillStyle = C.ink; c.beginPath(); c.moveTo(bx - 165, T);
  c.bezierCurveTo(bx - 190, T - 70, bx - 150, T - 120, bx - 80, T - 118);
  c.bezierCurveTo(bx - 30, T - 116, bx + 10, T - 150, bx + 52, T - 168);
  c.lineTo(bx + 78, T - 150);
  c.bezierCurveTo(bx + 80, T - 120, bx + 150, T - 95, bx + 160, T - 50);
  c.quadraticCurveTo(bx + 168, T - 12, bx + 150, T); c.closePath(); c.fill();
  // bağ: yatık boğumun üstünde düğüm ve iki sarkan ip ucu
  c.save(); c.translate(bx + 66, T - 166); c.rotate(.6);
  c.beginPath(); c.ellipse(-12, -10, 16, 10, -.4, 0, TAU); c.ellipse(12, -10, 16, 10, .4, 0, TAU); c.fill(); c.restore();
  c.strokeStyle = C.ink; c.lineWidth = 4; c.beginPath(); c.moveTo(bx + 70, T - 168); c.quadraticCurveTo(bx + 104, T - 160, bx + 112, T - 128); c.moveTo(bx + 72, T - 164); c.quadraticCurveTo(bx + 96, T - 140, bx + 92, T - 116); c.stroke();
  c.strokeStyle = C.red; c.lineWidth = 8;
  for (const [x0, y0, x1, y1, cy] of [[-150, -42, 150, -36, -66], [-120, -88, 110, -82, -112]]) { c.beginPath(); c.moveTo(bx + x0, T + y0); c.quadraticCurveTo(bx + (x0 + x1) / 2, T + cy, bx + x1, T + y1); c.stroke(); }
  c.strokeStyle = C.clay; c.lineWidth = 2;
  for (const [x0, y0, x1, y1] of [[-110, -16, -76, -24], [60, -18, 100, -26], [-40, -128, -4, -140], [30, -110, 60, -128], [-150, -70, -130, -96]]) { c.beginPath(); c.moveTo(bx + x0, T + y0); c.quadraticCurveTo(bx + (x0 + x1) / 2, T + y0 - 10, bx + x1, T + y1); c.stroke(); }
  c.beginPath(); c.moveTo(bx + 50, T - 162); c.lineTo(bx + 76, T - 146); c.stroke();
  // yağ payı: önce altındaki kemikler, sonra yağ (kazıma ve kaldırma yağı inceltir)
  const fx = x + 200, fat = o.fat ?? 1, sc = o.scratch || 0;
  E_bone(c, fx - 58, T - 23, 220, 0); E_bone(c, fx + 58, T - 23, 220, 0); E_bone(c, fx, T - 69, 300, 0); E_bone(c, fx + 4, T - 112, 280, .03);
  const fa = fat * (1 - .5 * sc);
  if (fa > 0) {
    c.save(); c.globalAlpha *= fa; c.translate(0, -110 * (1 - fat));
    c.fillStyle = '#E8DCC0'; c.strokeStyle = C.ink; c.lineWidth = 3;
    c.beginPath();
    for (let k = 0; k <= 40; k++) { const a = PI + k / 40 * PI, r = 1 + .08 * Math.sin(a * 5 + 1) + .05 * Math.sin(a * 9); c.lineTo(fx + Math.cos(a) * 172 * r, T - 6 + Math.sin(a) * 168 * r); }
    c.closePath(); c.fill(); c.stroke();
    c.lineWidth = 2.6;
    for (let k = 0; k < 3; k++) { const yy = T - 40 - k * 40, hw = 140 - k * 30; c.beginPath(); for (let q = 0; q <= 20; q++) { const xx = fx - hw + q / 20 * 2 * hw; c.lineTo(xx, yy + Math.sin(q * 1.3 + k) * 6); } c.stroke(); }
    c.restore();
  }
  // kazıma: yağın üstünde ince tarama çizgileri, altındaki kemik seçilir
  if (sc > 0) { c.save(); c.strokeStyle = C.ink; c.lineWidth = 1.6; c.globalAlpha = .7 * fat; const n = Math.floor(12 * sc); for (let k = 0; k < n; k++) { c.beginPath(); c.moveTo(fx - 120 + k * 20, T - 20); c.lineTo(fx - 90 + k * 20, T - 140); c.stroke(); } c.restore(); }
}

// --- P075–P082: sunak, Hesiodos, Mekone, öküz, iki pay, seçim, kemikler, yüzyıllar ---
shot(PA('P075'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const ST = [[PA('P075'), 0, 1.0], [A('E01@neden'), 0, 1.25], [A('E03'), 1], [A('E03@mekone'), 2], [A('E03@prometeus'), 3], [A('E04'), 4], [A('E05'), 5], [A('E05@altından'), 5, 1.45], [A('E05@o'), 6, .95]];
  const c = E_cam(t, ST);
  clayBG(ctx, C.clayL, C.clayD);
  ctx.save(); cam(ctx, c, 1);
  E_frieze(ctx, 0, 6);
  // 0: sunak ve ziyafet: insanlar et yer, kemik dumanı tanrılara yükselir (E01@kemikleri)
  { const x = .5 * E_PW, k = ramp(t, A('E01@kemikleri') - .3, A('E01@kemikleri') + 1.2);
    altar(ctx, x, E_GY, 3.2, C.ink, C.clay, 1, t);
    for (const [dx, dir] of [[-460, 1], [-300, 1], [320, -1], [480, -1]]) E_fig(ctx, x + dx, 3.6, dir, LK.human, { torso: .25, shN: 1.6 + .2 * Math.sin(t * 3 + dx), elN: 1.4, handN: 'fist' });
    smokeWisps(ctx, x, E_GY - 150, 260 + 220 * k, t, { a: .6 + .3 * k, w: 4, spread: 24, sway: 26 });
    if (k > 0) for (let i = 0; i < 3; i++) { ctx.save(); ctx.globalAlpha = k; E_fig(ctx, x - 160 + i * 160, 1.6, i < 1 ? 1 : -1, { beard: 'full', hair: 'long', garment: 'robe' }, { torso: -.05, head: -.25 }, { }); ctx.restore(); }
  }
  // 1: Hesiodos (rapsod, asa): ad etiketi üst katmanda
  { const x = 1.5 * E_PW; E_fig(ctx, x, 5.2, 1, LK.hesiodos, { torso: .02, head: .05, shN: .5 + .15 * Math.sin(t * 2.4), elN: .9, handN: 'open' }, { hold: { F: HOLD.spear(96) } }); dipinto(ctx, 'ΗΣΙΟΔΟΣ', x - 260, 420, 54, { col: C.ink, vertical: true }); }
  // 2: Mekone: solda oturan tanrılar, sağda ayakta insanlar
  { const x = 2.5 * E_PW;
    for (let i = 0; i < 3; i++) { throne(ctx, x - 560 + i * 170, E_GY, 3.2, 1, C.ink, C.clay, { high: i === 1 }); bf(ctx, x - 545 + i * 170, E_GY - 18, 3.3, 1, i === 1 ? LK.zeus : { beard: 'full', hair: 'long', garment: 'robe' }, { torso: -.05, shN: .3, elN: .9 }, { ik: { fN: [x - 545 + i * 170 + 92, E_GY - 10, 0], fF: [x - 545 + i * 170 + 70, E_GY - 10, 0] } }); }
    for (let i = 0; i < 4; i++) E_fig(ctx, x + 200 + i * 130, 3.4, -1, i % 2 ? LK.humanF : LK.human, { head: .05 });
    dipinto(ctx, 'ΜΗΚΟΝΗ', x, 200, 60, { col: C.ink, a: ramp(t, A('E03@mekonede'), A('E03@mekonede') + .6) }); }
  // 3: Prometheus koca bir öküzü keser; E03@ikiye'de öküz silueti ikiye ayrılır
  { const x = 3.5 * E_PW, sp = E.io2(ramp(t, A('E03@ikiye') - .1, A('E03@ayırır') + .4));
    for (const [sg, side] of [[-1, 0], [1, 1]]) { ctx.save(); ctx.beginPath(); side ? ctx.rect(x + 40, 0, 2000, 2000) : ctx.rect(x - 2000, 0, 2040, 2000); ctx.clip(); ctx.translate(sg * 70 * sp, 0); cow(ctx, x + 40, E_GY, 3.4, -1, 0, { col: C.ink, inc: C.clay }); ctx.restore(); }
    E_fig(ctx, x - 420, 4.6, 1, LK.promFree, { torso: .25, shN: lerp(2.6, .6, ramp(t, A('E03@keser') - .2, A('E03@keser') + .3)), elN: .2, handN: 'fist' }, { hold: { N: HOLD.chisel() } });
    if (sp > 0 && sp < 1) smokeWisps(ctx, x + 40, E_GY - 200, 180, t, { n: 2, a: .5 * Math.sin(PI * sp), w: 3, spread: 18, sway: 16, seed: 2 }); }
  // 4: iki pay yan yana; kazıma yağın altındaki kemiği ele verir (E04@çıplak)
  { const x = 4.5 * E_PW; E_portions(ctx, x, E_GY, { scratch: ramp(t, A('E04@çıplak') - .2, A('E04@kemikler') + .6) }); }
  // 5: Prometheus sunar ("Hangisini istersen seç"); Zeus parlak paya uzanır; E05@altından'da yağ kalkar, beyaz kemikler; Zeus'un profili donar
  { const x = 5.5 * E_PW, rch = ramp(t, A('E05@zeus#1') - .2, A('E05@alır') + .2), lift = ramp(t, A('E05@altından'), A('E05@altından') + .5);
    E_portions(ctx, x, E_GY, { fat: 1 - lift });
    E_fig(ctx, x - 560, 4.4, 1, LK.promFree, { torso: .05, shN: 1.4, elN: .2, handN: 'open' });
    let J = null, M = null;
    E_fig(ctx, x + 620, 5.0, -1, LK.zeus, { torso: .1 * rch, shN: lerp(.2, 1.35, rch), elN: lerp(.4, .1, rch), handN: 'open', head: lift > .5 ? .02 : 0 }, { hold: { F: HOLD.scepter(80) }, still: lift > .5 }); }
  // 6: zaman atlaması: yüzyıllar boyunca sunaklar; kemik dumanı tanrılara, et insanlara (friz akar)
  { const x = 6.5 * E_PW;
    for (let i = 0; i < 4; i++) { const ax = x - 540 + i * 360 + ((t * 40) % 360); altar(ctx, ax, E_GY, 2.0, C.ink, C.clay, 1, t + i); smokeWisps(ctx, ax, E_GY - 100, 300, t, { a: .7, w: 3, spread: 16, sway: 20, seed: i }); E_fig(ctx, ax + 110, 2.6, -1, LK.human, { torso: .3, shN: 1.5, elN: 1.4 }); } }
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => {
    chapterCard(ctx, 'BÖLÜM IV', "MEKONE'DEKİ HİLE", st.lt - .15, 3.2, { y: 170 });
    if (st.t > A('E03@hesiodosta') - .2 && st.t < A('E03@mekone')) nameTag(ctx, 'HESİODOS', 'Theogonia · İşler ve Günler', 110, 700, st.t - A('E03@hesiodosta'), 3.2, { col: C.ink, line: C.red });
    const tH = A('E05');
    if (st.t > tH && st.t < A('E05@zeus#1') + .6) { const p = ramp(st.t, tH, tH + 1.2, E.lin); ctx.save(); ctx.globalAlpha = 1 - ramp(st.t, A('E05@zeus#1'), A('E05@zeus#1') + .6); speechFlow(ctx, 'Hangisini istersen seç.', u => [lerp(560, 1360, u), 300 - Math.sin(u * PI) * 60], p, { font: '600 56px Cinzel', col: C.ink, glow: 'rgba(242,214,170,.9)' }); ctx.restore(); }
  } });

// --- P083–P084: beyaz zemin: sayfada bir çizgi tanrıları insanlardan ayırır; Prometheus çizgiyi aşar; tanrılar silinir, tepeye insanlar çıkar ---
shot(PA('P083'), (ctx, st) => {
  const t = st.t, lt = st.lt, tP = A('E07@prometeus'), tE = A('E08@olimpos'), tY = A('E08@yeni');
  const c = { x: 960 + lt * 4, y: 540, z: 1.02 + lt * .003 };
  ctx.save(); cam(ctx, c, 1);
  paperBG(ctx, t, { seed: 71 });
  const gy = 820;
  inkPoly(ctx, [[240, gy], [1680, gy]], ramp(lt, 0, .6), { col: PW.line, w: 3 });
  // ayırma çizgisi (dikey) ve titremesi
  const shake = Math.exp(-Math.max(0, t - tP - 1.2) * 3) * (t > tP + 1.2 ? 1 : 0);
  inkPoly(ctx, [[960 + Math.sin(t * 30) * 3 * shake, 330], [960, gy]], ramp(lt, .3, 1.0), { col: PW.red, w: 4 });
  // solda tanrılar (Olympos tepesi), sağda insanlar
  const er = ramp(t, tE, tE + 2.0);
  inkPoly(ctx, sampleF(u => [lerp(280, 900, u), gy - 260 * Math.sin(u * PI) ** 1.4], 40), 1, { col: PW.line, w: 3 });
  ctx.save(); ctx.globalAlpha = 1 - er;
  for (let i = 0; i < 3; i++) figure(ctx, { x: 470 + i * 140, y: gy - 230 - 44.5 * 2.2, s: 2.2, dir: 1, sty: STY.lek, lk: i === 1 ? LK.zeus : { beard: 'full', hair: 'long', garment: 'robe' }, seed: 40 + i, p: { torso: 0 } });
  ctx.restore();
  for (let i = 0; i < 4; i++) { const up = ramp(t, tE + .6 + i * .3, tE + 1.6 + i * .3); figure(ctx, { x: lerp(1160 + i * 120, 470 + i * 130 - 60, up), y: gy - 44.5 * 2.4 - 260 * Math.sin(clamp((lerp(1160 + i * 120, 470 + i * 130 - 60, up) - 280) / 620) * PI) ** 1.4 * (up > .01 ? 1 : 0), s: 2.4, dir: up > 0 ? -1 : -1, sty: STY.lek, lk: i % 2 ? LK.humanF : LK.human, seed: 50 + i, p: { breath: Math.sin(t * 2 + i) * .5 } }); }
  // küçük Prometheus çizgiyi aşar
  const step = E.io2(ramp(t, tP + .4, tP + 2.0));
  walkScene(ctx, null, lerp(820, 1080, step), 2.8, t, 1, { noCam: true, ground: FLAT(gy), stride: 34, dist: lerp(820, 1080, step), stand: 1 - Math.sin(PI * step), sty: STY.lek, lk: LK.promFree });
  ctx.restore();
}, { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => { const q = A('E08@yeni'); if (st.t > q - .2) quoteCard(ctx, 'Yeni bir devrimin hazırlayıcısıdır.', 'A. ERHAT · ÖNSÖZ · S. X', 960, 200, 1500, st.t - q, { font: 'italic 500 76px "Cormorant Garamond"', lh: 86 }); } });

// --- P085: METOP: Zeus'un gözü kısılır: hileyi görür ve yine de parlak payı alır (bile bile aldanır) ---
shot(PA('P085'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('E09@bile'), sq = ramp(t, A('E09@görür') - .2, A('E09@görür') + .4);
  clayBG(ctx, C.clayL, C.clayD);
  const c = { x: 5.5 * E_PW + 300, y: lerp(580, 560, sq), z: lerp(1.45, 1.7, E.io2(clamp(lt / st.d))) };
  ctx.save(); cam(ctx, c, 1);
  E_frieze(ctx, 5, 5);
  const x = 5.5 * E_PW, take = ramp(t, tB, tB + 1.0);
  E_portions(ctx, x, E_GY, { fat: 1 });
  let J = null, M = null;
  E_fig(ctx, x + 620, 5.0, -1, LK.zeus, { torso: .12 * take, shN: lerp(.6, 1.35, take), elN: lerp(.4, .1, take), handN: take > .8 ? 'fist' : 'open', blink: .35 + .5 * sq, brow: -.6 - .6 * sq }, { hold: { F: HOLD.scepter(80) } });
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'clay', dur: .5, end: true }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P086: ova (siyah figür): Zeus'un pelerininin gölgesi köyün üstünden geçer; ocaklar gölgenin kenarı değdikçe söner, sonuncusu E09@ateşi'de ---
shot(PA('P086'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('E09@ateşi'), t0 = PA('P086');
  clayBG(ctx, C.clayL, C.clayD);
  const c = { x: 960 + lt * 6, y: 540, z: 1.05 };
  ctx.save(); cam(ctx, c, 1);
  const gy = 780; ctx.fillStyle = C.ink; ctx.fillRect(-200, gy, 2400, 8);
  const edge = lerp(-400, 1700, ramp(t, t0, tA + .1, E.lin));
  const HX = [180, 420, 660, 900, 1140, 1380, 1600];
  HX.forEach((x, i) => {
    E_fig(ctx, x - 60, 2.4, 1, i % 2 ? LK.humanF : LK.human, { torso: .3, shN: 1.4, elN: 1.2, handN: 'open' });
    const lit = x > edge;
    if (lit) { glow(ctx, x, gy - 20, 70, 'rgba(255,190,90,.45)'); flame(ctx, x, gy - 4, .7, t + i, { haloR: 50 }); }
    else if (edge - x < 220) for (let k = 0; k < 3; k++) { const ph = (t * .8 + k / 3) % 1; ctx.fillStyle = `rgba(23,16,12,${.3 * Math.sin(PI * ph) * (1 - (edge - x) / 220)})`; ctx.beginPath(); ctx.arc(x + Math.sin(k + t) * 8, gy - 30 - ph * 120, 10 + ph * 16, 0, TAU); ctx.fill(); }
    ctx.fillStyle = C.ink; ctx.fillRect(x - 24, gy - 8, 48, 8);
  });
  // gölge: koyu bulut (pelerin), kenarı ilerler
  ctx.fillStyle = 'rgba(23,16,12,.55)'; ctx.beginPath(); ctx.moveTo(-600, 0); ctx.lineTo(edge, 0); for (let y = 0; y <= 900; y += 30) ctx.lineTo(edge + Math.sin(y * .012 + t) * 40, y); ctx.lineTo(-600, 900); ctx.closePath(); ctx.fill();
  for (let i = 0; i < 4; i++) cloud(ctx, edge - 300 - i * 380, 220 + (i % 2) * 70, 1.6, C.ink, C.clay, i + 81);
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P087–P088: gece, tanrıların ocağı: Prometheus rezene sapını közün üstüne indirir; sap tutuşur; sert kesme: dağdan aşağı koşu (kapak karesinin siyah figür eşi) ---
shot(PA('P087'), (ctx, st) => {
  const t = st.t, lt = st.lt, tR = A('E10@rezene'), tI = A('E10@insanlara');
  clayBG(ctx, '#7A3E22', '#3E1E10');
  if (t < tI) {
    const c = { x: 960 + lt * 5, y: 520, z: 1.25 };
    ctx.save(); cam(ctx, c, 1);
    D_metope(ctx, 200, 1720, 120, 900, 1);
    ctx.fillStyle = C.ink; ctx.fillRect(220, E_GY, 1480, 6);
    altar(ctx, 1150, E_GY, 3.6, C.ink, C.clay, 1, t);
    const low = E.io2(ramp(t, tR - .8, tR + .2)), lit = ramp(t, tR + .1, tR + .6);
    let J = null, M = null;
    E_fig(ctx, 760, 5.0, 1, LK.promFree, { torso: .35 * low, neck: .2 * low, head: .15 * low, shN: lerp(.6, 1.0, low), elN: .3, handN: 'fist' }, { onJoints: (j, m) => { J = j; M = m; } });
    const wr = jointPt(ctx, M, J.AN.wr), tip = [lerp(wr[0] + 120, 1110, low), lerp(wr[1] - 60, E_GY - 110, low)];
    fennel(ctx, wr[0], wr[1], tip[0], tip[1], t, { col: C.ink, inc: C.clay, w: 9, fire: lit > 0, k: lit, fs: .9 });
    glow(ctx, 1150, E_GY - 80, 160, `rgba(255,170,80,${.3 + .2 * Math.sin(t * 6)})`);
    ctx.restore();
  } else {
    // dağdan aşağı koşu: siyah figür, rezenenin ucunda alev; kapak karesinin eşi (sert kesme)
    const c = { x: 600 + (t - tI) * 300, y: 520, z: 1.0 };
    ctx.save(); cam(ctx, c, 1);
    const g = x => 520 + x * .22;
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-400, g(-400)); ctx.lineTo(3000, g(3000)); ctx.lineTo(3000, 1400); ctx.lineTo(-400, 1400); ctx.fill();
    const x = 600 + (t - tI) * 300;
    let J = null, M = null;
    walkScene(ctx, null, x, 5.2, t, 1, { noCam: true, ground: groundOf(g), stride: 52, lean: .26, sty: STY.black, lk: LK.promFree, p: { shN: 2.2, elN: .2, handN: 'fist' }, onJoints: (j, m) => { J = j; M = m; } });
    const wr = jointPt(ctx, M, J.AN.wr);
    fennel(ctx, wr[0], wr[1], wr[0] + Math.cos(-.72) * 150, wr[1] + Math.sin(-.72) * 150, t, { col: C.ink, inc: C.clay, w: 9, fs: 1.1 });
    ctx.restore();
  }
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P089: Olympos'ta sırtı dönük Zeus; aşağıdaki karanlık dünyada tek parlak nokta yanıp söner; yumruk sıkılır ---
shot(PA('P089'), (ctx, st) => {
  const t = st.t, lt = st.lt, tI = A('E10@ısırır');
  clayBG(ctx, '#6E381E', '#2E160B');
  const c = { x: 960, y: lerp(500, 540, E.io2(clamp(lt / st.d))), z: lerp(1.0, 1.12, E.io2(clamp(lt / st.d))) };
  ctx.save(); cam(ctx, c, 1);
  // Olympos tepesi (önde), aşağıda karanlık dünya ve tek ışık
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-200, 1200); ctx.lineTo(-200, 760); ctx.quadraticCurveTo(300, 600, 760, 640); ctx.lineTo(760, 1200); ctx.fill();
  const fl = .5 + .5 * Math.sin(t * 5) * Math.sin(t * 1.7);
  glow(ctx, 1380, 800, 80, `rgba(255,200,110,${.35 + .35 * fl})`); ctx.fillStyle = C.white; ctx.beginPath(); ctx.arc(1380, 800, 5 + 2 * fl, 0, TAU); ctx.fill();
  // sırtı dönük Zeus (izleyiciye arkası, ışığa bakar): profil sağa, pelerin dalgası
  const fist = ramp(t, tI - .4, tI + .3);
  bf(ctx, 520, 650, 6.0, 1, { ...LK.zeus, cape: true }, { torso: .06, neck: .12, head: .2, shN: .1, elN: lerp(.3, 1.3, fist), handN: fist > .5 ? 'fist' : 'open', breath: Math.sin(t * 1.3) * .5 });
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'clay', dur: .5, end: true }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P090–P098: METOP: Hephaistos kilden kız yoğurur; tanrılar süsler; ΠΑΝΔΩΡΑ; uyarı; Epimetheus kucak açar; küp; keresler; ELPİS; iki kez aldatılan Zeus ---
shot(PA('P090'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const ST = [[PA('P090'), 7], [A('E12@tanrılar'), 7, 1.35], [A('E12@adı'), 7, 1.5], [A('E12@prometeus'), 8], [A('E12@ama'), 9], [A('E14'), 10], [A('E14@hastalıklar'), 10, .9], [A('E14@içeride'), 10, 1.5], [A('E11'), 11]];
  const c = E_cam(t, ST);
  clayBG(ctx, C.clayL, C.clayD);
  ctx.save(); cam(ctx, c, 1);
  E_frieze(ctx, 7, 11);
  // 7: Hephaistos kızı yoğurur (kil vazonun kendi rengi), tanrılar süsler, ad yazılır
  { const x = 7.5 * E_PW, kn = ramp(t, A('E12@hefaistos'), A('E12@yoğurur') + .6), dec = ramp(t, A('E12@tanrılar'), A('E12@süsler') + .4);
    E_fig(ctx, x - 300, 4.6, 1, LK.hephaistos, { torso: .4 + .05 * Math.sin(t * 4), shN: 1.1 + .1 * Math.sin(t * 4), elN: .6, handN: 'open' });
    // kil kız: önce topak, sonra ayakta duran figür (kil rengi: siyah figür değil, zeminin kendisi; kontur siyah)
    const g = clamp(kn * 1.3);
    if (g < 1) { ctx.fillStyle = C.clayD; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(x + 40, E_GY - 60, 70 * (1 - g * .5), 60 + 120 * g, 0, 0, TAU); ctx.fill(); ctx.stroke(); }
    if (g > .4) { ctx.save(); ctx.globalAlpha = ramp(g, .4, 1); E_fig(ctx, x + 40, 4.6, -1, { ...LK.pandora, robe: true }, { head: .05 }, { sty: { ...STY.black, fill: C.clayD, cut: C.ink, line: C.ink } }); ctx.restore(); }
    // armağanlar: stephane (yedi dik yapraklı taç, siyah figür + eklenmiş kırmızı) dikey iner, saç bandına oturur;
    // gerdanlık sağdan boyun hizasında gelir (eklenmiş beyaz boncuklar, siyah kontur), yüzü hiç kesmez
    if (dec > 0) { const hx = x + 40 + 2, hy = E_GY - 4.6 * 92.5, ty = lerp(140, hy, E.out3(clamp(dec * 1.25)));
      ctx.save(); ctx.translate(hx, ty);
      // hilal stephane: ortada yüksek, yanlara incelen siyah bant; üst kenarda yedi küçük diş, içinde kazıma ve kırmızı noktalar
      ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-38, 12); ctx.quadraticCurveTo(0, -26, 38, 12); ctx.quadraticCurveTo(0, 0, -38, 12); ctx.closePath(); ctx.fill();
      for (let k = 0; k < 7; k++) { const u = k / 6, bx = lerp(-30, 30, u), by = 12 - 19 * Math.sin(u * PI) - 2; ctx.beginPath(); ctx.moveTo(bx - 4, by + 2); ctx.lineTo(bx, by - 6 - 3 * Math.sin(u * PI)); ctx.lineTo(bx + 4, by + 2); ctx.closePath(); ctx.fill(); }
      ctx.strokeStyle = C.clay; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(-30, 9); ctx.quadraticCurveTo(0, -14, 30, 9); ctx.stroke();
      ctx.fillStyle = C.red; for (const dx of [-16, 0, 16]) { ctx.beginPath(); ctx.arc(dx, 4 - (dx ? 4 : 8), 3, 0, TAU); ctx.fill(); }
      ctx.restore();
      const nk = E.io2(ramp(dec, .35, 1)), ny = E_GY - 4.6 * 74.5, nx = lerp(x + 360, x + 40, nk);
      if (nk > 0) for (let k = 0; k < 7; k++) { const u = k / 6 - .5, px = nx + u * 36 * lerp(1.8, 1, nk), py = ny + (1 - 4 * u * u) * 8 * nk; ctx.fillStyle = C.white; ctx.strokeStyle = C.ink; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.arc(px, py, 4.2, 0, TAU); ctx.fill(); ctx.stroke(); } }
    const na = ramp(t, A('E12@adı'), A('E12@pandoradır') + .5); if (na > 0) dipinto(ctx, 'ΠΑΝΔΩΡΑ', x + 300, 440, 64, { col: C.ink, vertical: true, p: na }); }
  // 8: geri dönüş: Prometheus kardeşini uyarır
  { const x = 8.5 * E_PW; E_fig(ctx, x - 200, 4.6, 1, LK.promFree, { torso: .05, shN: 1.5, elN: .3 + .3 * Math.sin(t * 6), handN: 'open' }); E_fig(ctx, x + 200, 4.6, -1, LK.epimetheus, { torso: -.05, head: .1 }); }
  // 9: Epimetheus kollarını açar (temas yok); iş işten geçince başı geriye döner
  { const x = 9.5 * E_PW, op = ramp(t, A('E12@ama') + .4, A('E12@epimeteus') + .6), back = ramp(t, A('E12@geçince') - .2, A('E12@geçince') + .4);
    E_fig(ctx, x + 260, 4.6, -1, LK.pandora, { torso: -.05 });
    E_fig(ctx, x - 160, 4.6, 1, LK.epimetheus, { torso: .05, shN: lerp(.2, 1.7, op), elN: lerp(.3, .2, op), shF: lerp(-.1, 1.5, op), elF: .2, handN: 'open', handF: 'open', headBack: back > .5 }); }
  // 10: büyük küp; Pandora kapağı kaldırır; keresler fırlar; kapak kapanır, dipte ELPİS'in soluk ışığı
  { const x = 10.5 * E_PW, lid = ramp(t, A('E14@kapağını'), A('E14@kaldırır') + .3) * (1 - ramp(t, A('E14@içeride'), A('E14@içeride') + .4)), sw = ramp(t, A('E14@hastalıklar') - .2, A('E14@yayılır') + 1.0, E.lin);
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(x - 90, E_GY - 420); ctx.quadraticCurveTo(x - 260, E_GY - 300, x - 180, E_GY - 60); ctx.quadraticCurveTo(x - 120, E_GY, x, E_GY); ctx.quadraticCurveTo(x + 120, E_GY, x + 180, E_GY - 60); ctx.quadraticCurveTo(x + 260, E_GY - 300, x + 90, E_GY - 420); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = C.clay; ctx.lineWidth = 3; for (const yy of [E_GY - 330, E_GY - 160]) { ctx.beginPath(); ctx.moveTo(x - 200, yy); ctx.quadraticCurveTo(x, yy + 20, x + 200, yy); ctx.stroke(); }
    ctx.save(); ctx.translate(x - 110, E_GY - 430); ctx.rotate(-lid * .9); ctx.fillStyle = C.ink; ctx.fillRect(0, -16, 220, 20); ctx.restore();
    E_fig(ctx, x - 400, 4.4, 1, LK.pandora, { torso: .1, shN: lerp(1.0, 2.2, lid), elN: .4, handN: 'open' });
    if (sw > 0 && sw < 1) for (let k = 0; k < 40; k++) { const r = rng(k + 3), d = clamp(sw * 1.3 - r() * .3), a = r() * TAU, bx = x + Math.cos(a) * 900 * d + Math.sin(t * 4 + k) * 20, by = E_GY - 440 - Math.abs(Math.sin(a)) * 380 * d + Math.cos(t * 5 + k) * 14;
      ctx.fillStyle = C.ink; ctx.beginPath(); ctx.ellipse(bx, by, 10, 6, 0, 0, TAU); ctx.fill(); const f = Math.sin(t * 22 + k); ctx.beginPath(); ctx.moveTo(bx - 4, by); ctx.lineTo(bx - 14, by - 12 * f); ctx.lineTo(bx + 2, by - 2); ctx.moveTo(bx + 4, by); ctx.lineTo(bx + 14, by - 12 * f); ctx.lineTo(bx - 2, by - 2); ctx.fill(); }
    const el = ramp(t, A('E14@içeride') + .3, A('E14@umut'));
    if (el > 0) { glow(ctx, x, E_GY - 70, 60, `rgba(205,218,235,${(.3 + .1 * Math.sin(t * 2)) * el})`); ctx.fillStyle = `rgba(220,230,240,${.8 * el})`; ctx.beginPath(); ctx.arc(x, E_GY - 70, 7, 0, TAU); ctx.fill(); } }
  // 11: iki kez aldatılmış Zeus (çentikler: iki kazıma çizgisi tahtın kolunda)
  { const x = 11.5 * E_PW; throne(ctx, x + 80, E_GY, 5.0, 1, C.ink, C.clay, { high: true }); bfSeat(ctx, x + 80, E_GY, 5.0, 5.0, 1, LK.zeus, { torso: .06, head: .15, shN: .3, elN: 1.2, handN: 'fist' });
    const nk = ramp(t, A('E11@iki'), A('E11@kez') + .3); ctx.strokeStyle = C.clay; ctx.lineWidth = 5; for (let k = 0; k < 2; k++) if (nk > k * .5) { ctx.beginPath(); ctx.moveTo(x - 250 + k * 40, 360); ctx.lineTo(x - 230 + k * 40, 470); ctx.stroke(); } }
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => {
    const t = st.t, tP = A('E12@prometeus');
    if (t > tP && t < A('E12@ama') + .3) { const p = ramp(t, A('E12@zeustan'), A('E12@alma') + .4, E.lin); ctx.save(); ctx.globalAlpha = 1 - ramp(t, A('E12@ama'), A('E12@ama') + .3); speechFlow(ctx, 'Zeus’tan armağan alma!', u => [lerp(560, 1360, u), 290 - Math.sin(u * PI) * 50], p, { font: '600 56px Cinzel', col: C.ink, glow: 'rgba(242,214,170,.9)' }); ctx.restore(); }
    const tU = A('E14@umut'); if (t > tU - .1 && t < A('E11')) { const a = ramp(t, tU - .1, tU + .5); txt(ctx, 'ΕΛΠΙΣ · umut', 960, 300, { font: '700 64px Cinzel', col: C.ink, ls: 6, a, shadow: 'rgba(242,214,170,.9)', blur: 14 }); }
    erhatStrip(ctx, t - A('E11@kaba') + .4, 3.0, 'kaba kuvvet', 'x', { icon: (c, p) => { c.save(); c.globalAlpha = p; c.fillStyle = PW.line; c.beginPath(); c.ellipse(0, 0, 46 * p, 36 * p, 0, 0, TAU); c.fill(); c.restore(); } });
  } });

// --- P099–P104: beyaz zemin öbeği (E15–E16): rapsod Hesiodos (iç kare), satır aralarındaki gülme, ayakları silinen taht, insanlara geçen kıvılcım, üçüncü ve son devrim ---
shot(PA('P099'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('E15@ama'), tT = A('E15@tahtının'), tC = A('E15@çünkü'), tU = A('E16@üçüncü'), tI = A('E16@insan');
  const pan = E.io2(ramp(t, tT - .6, tT + .6)), cl = E.io2(ramp(t, tI + .3, tI + 1.6));
  const c = { x: 960 + lt * 3, y: 540, z: lerp(1, 1.08, pan) * lerp(1, 1.5, cl) };
  ctx.save(); cam(ctx, c, 1);
  paperBG(ctx, t, { seed: 72 });
  // iç kare: siyah figür rapsod Hesiodos Zeus'u över (asa vuruşu)
  const ia = 1 - ramp(t, tT - .4, tT + .2);
  if (ia > 0) { ctx.save(); ctx.globalAlpha = ia; ctx.fillStyle = C.clay; ctx.fillRect(560, 160, 800, 420); ctx.strokeStyle = PW.line; ctx.lineWidth = 5; ctx.strokeRect(560, 160, 800, 420);
    ctx.save(); ctx.beginPath(); ctx.rect(560, 160, 800, 420); ctx.clip();
    bf(ctx, 760, 560, 3.6, 1, LK.hesiodos, { shN: .4 + .2 * Math.max(0, Math.sin(t * 3)), elN: .9 }, { hold: { F: HOLD.spear(90) } });
    throne(ctx, 1160, 560, 3.6, -1, C.ink, C.clay, { high: true }); bfSeat(ctx, 1160, 560, 3.6, 3.6, -1, LK.zeus, { torso: -.05 });
    ctx.restore(); ctx.restore(); }
  // satırlar aralanır: aralarında gizli görüntü: insanlar küçük bir Zeus'a güler
  const op = ramp(t, tA, tA + 1.0) * (1 - ramp(t, tT - .3, tT + .3));
  for (let i = 0; i < 6; i++) { const y = 640 + i * 34 + (i > 2 ? 60 : 0) * op; scribble(ctx, 520, y, 880, 1, 140 + i, { col: `rgba(74,52,35,${.55 * ia})` }); }
  if (op > 0) { ctx.save(); ctx.globalAlpha = op; for (let i = 0; i < 4; i++) figure(ctx, { x: 620 + i * 110, y: 742 - 44.5 * 1.3, s: 1.3, dir: 1, sty: STY.lek, lk: i % 2 ? LK.humanF : LK.human, seed: 60 + i, p: { torso: .05 * Math.sin(t * 16 + i), head: -.1 } }); figure(ctx, { x: 1180, y: 742 - 44.5 * .8, s: .8, dir: -1, sty: STY.lek, lk: LK.zeus, seed: 66, p: {} }); ctx.restore(); }
  // TAHT (beyaz zemin): ayakları silinir, boşlukta asılı kalır; önünde insan doğrulur, gölgesi tahtı örter
  const th = ramp(t, tT - .2, tT + .5);
  if (th > 0) { ctx.save(); ctx.globalAlpha = th;
    const legs = 1 - ramp(t, tT + .3, tT + 1.6), sway = Math.sin(t * 1.3) * 6 * (1 - legs);
    // taht künyenin altında kalır (tepesi y≈300); silinen bacaklar %25 soluk iz olarak kalır (taht "L" gibi okunmaz)
    ctx.save(); ctx.translate(sway, 0); ctx.save(); ctx.globalAlpha *= .25 * (1 - legs * 0); ctx.beginPath(); ctx.rect(0, 860 - 160 * (1 - legs), W, 400); ctx.clip(); throne(ctx, 1000, 860, 6.2, 1, PW.line, PW.paperL, { high: true }); ctx.restore();
    ctx.beginPath(); ctx.rect(0, 0, W, 860 - 160 * (1 - legs)); ctx.clip(); throne(ctx, 1000, 860, 6.2, 1, PW.line, PW.paperL, { high: true }); ctx.restore();
    // kıvılcım tanrıların katından insanların başlarına iner
    const sp = ramp(t, tC, tC + 1.6);
    if (sp > 0 && sp < 1) { const x = lerp(1000, 640, sp), y = lerp(200, 640, sp); glow(ctx, x, y, 40, 'rgba(255,190,90,.7)'); ctx.fillStyle = PC.fireCore; ctx.beginPath(); ctx.arc(x, y, 6, 0, TAU); ctx.fill(); }
    const up = ramp(t, tU - .2, tU + 1.2), sh = ramp(t, tI - .2, tI + 1.2);
    // doğrulan insanın gölgesi tahta düşer ve onu örter (insan biçimli gölge, kaba elips değil)
    if (up > 0) { if (sh > 0) { const sc2 = 'rgba(74,52,35,.3)'; figure(ctx, { x: lerp(700, 980, sh), y: 860 - 44.5 * lerp(4.4, 8.6, sh), s: lerp(4.4, 8.6, sh), dir: 1, still: true, alpha: sh, sty: { fill: sc2, cut: 'rgba(0,0,0,0)', red: sc2, white: sc2, line: 'rgba(0,0,0,0)' }, lk: LK.human, seed: 61, p: { torso: -.05, head: -.1 } }); }
      figure(ctx, { x: 640, y: 760 - 44.5 * 4.4 * lerp(.7, 1, up), s: 4.4, dir: 1, sty: STY.lek, lk: LK.human, seed: 61, p: { torso: lerp(.6, 0, up), neck: lerp(.4, -.1, up), head: lerp(.3, -.1, up), shN: lerp(.8, .4, cl), elN: lerp(.4, 1.6, cl), shF: lerp(.8, .5, cl), elF: lerp(.4, 1.5, cl), handN: 'open', handF: 'open' }, ik: { fN: [660, 757, 0], fF: [610, 757, 0] } });
      if (cl > 0) { glow(ctx, 760, 520, 120 * cl, `rgba(255,190,90,${.45 * cl})`); flame(ctx, 760, 560, .8 * cl, t, { haloR: 60 }); } }
    ctx.restore(); }
  ctx.restore();
}, { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => {
    const t = st.t, q1 = A('E15@akıl'), q2 = A('E16@üçüncü');
    if (t > q1 - .2 && t < q2) { ctx.save(); ctx.globalAlpha = 1 - ramp(t, q2 - .5, q2); quoteCard(ctx, 'akıl gücü tanrılardan insanlara geçmiştir', 'A. ERHAT · ÖNSÖZ · S. XI', 960, 120, 1600, t - q1, { font: 'italic 500 76px "Cormorant Garamond"', lh: 84 }); ctx.restore(); }
    if (t > q2 - .1) { ctx.save(); ctx.globalAlpha = 1 - ramp(t, A('E16@insan') + 1.2, A('E16@insan') + 1.8); quoteCard(ctx, 'üçüncü ve son devrim', 'A. ERHAT · ÖNSÖZ · S. XI', 960, 120, 1500, t - q2, { font: 'italic 500 80px "Cormorant Garamond"', lh: 90 }); ctx.restore(); }
  } });

// --- P105–P106: P015'in alevi aynı kadrajda büyür; boş taht geride kararır; alevde uygarlık frizinin önizlemesi; sert kesme: zincirin ilk halkası, tragedya maskesi ---
shot(PA('P105'), (ctx, st) => {
  const t = st.t, lt = st.lt, tZ = A('E16b@zincirin');
  if (t < tZ) {
    glazeBG(ctx, t, { gx: 960, gy: 900, gr: 600, stars: false, warm: 'rgba(150,62,28,.45)' });
    const u = E.io2(clamp(lt / (tZ - st.at)));
    const c = { x: 960, y: lerp(470, 560, u), z: lerp(1.0, 1.25, u) };
    ctx.save(); cam(ctx, c, 1);
    ctx.save(); ctx.globalAlpha = .9 - .4 * u; throneRim(ctx, 960 - 60, 820, 14, 1, { high: true, stool: false }); ctx.restore();
    const fs = lerp(1.15, 3.4, u);
    humanFires(ctx, t, [[960, 900, fs]], 1);
    // alevin içinde uygarlık frizinin önizlemesi (maskeli, döner)
    ctx.save(); ctx.beginPath(); ctx.ellipse(960, 900 - 70 * fs, 34 * fs, 56 * fs, 0, 0, TAU); ctx.clip(); ctx.globalAlpha = .5 * u;
    const ox = (t * 60) % 300;
    for (let k = -2; k < 6; k++) { const x = 840 + k * 100 - ox; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.strokeRect(x, 760, 90, 90); figure(ctx, { x: x + 45, y: 845 - 44.5 * .8, s: .8, dir: 1, sty: STY.red, lk: LK.human, seed: k + 90, still: true, p: {} }); }
    ctx.restore();
    ctx.restore();
    kayaFrame(ctx, t);
  } else {
    // zincirin ilk halkasının parıltısı; zincir yukarı, kadraj dışına; bir tragedya maskesi belirir
    const lz = t - tZ, c = { x: 1400, y: lerp(620, 420, E.io2(clamp(lz / 3.5))), z: 3.0 };
    const { wind } = kayaWorld(ctx, t, c, { sky: 'gece' });
    ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind }); ctx.restore();
    const g = Math.exp(-lz * 2.5); if (g > .02) { ctx.save(); cam(ctx, c, 1); sparkle(ctx, PROM_KAYA.sN[0] - 40, PROM_KAYA.sN[1] - 20, 40 * g, g, '#FFE2A8'); ctx.restore(); }
    const m = ramp(t, A('E16b@şair') - .4, A('E16b@şair') + .6);
    if (m > 0) { ctx.save(); ctx.globalAlpha = m; tragicMask(ctx, 520, 360, 2.6, { beard: true }); ctx.restore(); }
    kayaFrame(ctx, t);
  }
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });
