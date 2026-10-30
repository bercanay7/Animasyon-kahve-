// KAYA seti (kırmızı figür, Aiskhylos): filmin yaklaşık %38'i bu sette geçer. İskit uçurumu, zincirli Prometheus,
// ova ve insanların ateşleri, gök durumları (gece / şafak / fırtına), rüzgâr, akan dalga kuşağı.
// Bütün hareket t'nin kapalı fonksiyonudur (4 işçili render kareleri sırasız çizer; kareden kareye durum biriktirilmez).
'use strict';
const PROM_KAYA = { px: 1225, gy: 868, s: 6.3, sF: [1480, 215], sN: [1495, 600], sL: [1272, 876] };
// kamera ön ayarları: eşleşen planlar (ör. açılış ve I08c) aynı ayarı kullanır
const CAMS = {
  genis: { x: 1000, y: 540, z: 1 },
  orta: { x: 1250, y: 560, z: 1.75 },
  yakin: { x: 1290, y: 330, z: 3.4 },
  alt: { x: 1240, y: 640, z: 1.35, r: -.04 },
  gok: { x: 1000, y: 300, z: 1.1 },
};
const camMix = (a, b, p) => mix(a, b, p);
// rüzgâr: plan boyunca hafifçe değişir; saç, sakal, zincir ve gökteki çizgiler aynı değeri kullanır
const windAt = (t, base = .5) => base + .3 * noise1(t * .8, 4);

// Vitruvius sarmalı (akan dalga) kuşağı: phase px kaydırır; deniz kuşağı da olur
function runningWave(ctx, x0, x1, y, h, col, phase = 0, bg = null) {
  if (bg) { ctx.fillStyle = bg; ctx.fillRect(x0, y, x1 - x0, h); }
  const w = h * 1.6;
  ctx.save(); ctx.beginPath(); ctx.rect(x0, y, x1 - x0, h); ctx.clip();
  ctx.fillStyle = col; ctx.fillRect(x0, y + h - h * .12, x1 - x0, h * .12);
  const st = Math.floor((x0 - phase) / w) * w + phase;
  ctx.beginPath();
  for (let x = st; x < x1 + w; x += w) {
    const b = y + h * .88, top = y + h * .12;
    ctx.moveTo(x, b);
    ctx.bezierCurveTo(x + w * .35, b, x + w * .55, top, x + w * .78, top + h * .05);
    ctx.bezierCurveTo(x + w * 1.0, top + h * .1, x + w * .98, y + h * .55, x + w * .78, y + h * .58);
    ctx.bezierCurveTo(x + w * .62, y + h * .6, x + w * .6, y + h * .4, x + w * .72, y + h * .38);
    ctx.bezierCurveTo(x + w * .66, y + h * .5, x + w * .8, y + h * .5, x + w * .82, y + h * .44);
    ctx.bezierCurveTo(x + w * .85, y + h * .3, x + w * .7, y + h * .26, x + w * .62, y + h * .34);
    ctx.bezierCurveTo(x + w * .52, y + h * .5, x + w * .7, b, x + w, b);
  }
  ctx.lineTo(x1 + w, y + h); ctx.lineTo(st, y + h); ctx.closePath(); ctx.fill();
  ctx.restore();
}
// gökte vazo üslubu rüzgâr çizgileri (kil, sönük), sola akar
function windLines(ctx, t, wind, area = [0, 120, W, 560], n = 9, seed = 31) {
  const r = rng(seed);
  ctx.save(); ctx.strokeStyle = 'rgba(201,112,63,1)'; ctx.lineCap = 'round'; ctx.lineWidth = 2;
  for (let i = 0; i < n; i++) {
    const L = 60 + r() * 80, y = area[1] + r() * area[3], sp = (100 + r() * 80) * (.4 + wind), x = area[0] + ((r() * area[2] - t * sp) % (area[2] + 300) + area[2] + 300) % (area[2] + 300) - 150;
    ctx.globalAlpha = .16 * (.6 + wind * .6);
    ctx.beginPath(); ctx.moveTo(x, y); ctx.bezierCurveTo(x + L * .3, y - 6, x + L * .6, y + 6, x + L, y - 2); ctx.stroke();
    if (r() < .4) { ctx.beginPath(); ctx.arc(x + L + 6, y - 6, 5, PI * .5, PI * 2.1); ctx.stroke(); }
  }
  ctx.restore();
}
// şafak/güneş diski: kil tonunda (ateşin çekirdeğinden sönük), kenarı siyah konturlu
function sunDisk(ctx, x, y, r, a = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  glow(ctx, x, y, r * 2.2, 'rgba(200,110,55,.22)');
  const g = ctx.createRadialGradient(x - r * .2, y - r * .2, r * .1, x, y, r);
  g.addColorStop(0, '#D9A066'); g.addColorStop(1, '#B9653A');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
  ctx.strokeStyle = C.ink; ctx.lineWidth = 5; ctx.stroke();
  ctx.restore();
}
// Zincirli Prometheus. o: {look (baş), p (poz ekleri), wind, pullK}
function promChained(ctx, t, o = {}) {
  const { px, gy, s, sF, sN, sL } = PROM_KAYA;
  // ~4,2 sn'lik gerilme döngüsü: gövde öne asılır, zincir gerilir; geri gelince sarkar
  const ph = (t % 4.2) / 4.2, pull = (ph < .35 ? E.io2(ph / .35) : 1 - E.io2((ph - .35) / .65)) * (o.pullK ?? 1);
  let J = null, M = null;
  figure(ctx, {
    x: px, y: gy - 42.5 * s, s, dir: -1, sty: STY.red, lk: LK.prom, seed: 17, stripe: .55,
    p: { torso: .1 + .07 * pull, neck: -.04, head: -.1 + (o.look || 0), handN: 'fist', handF: 'fist', mouthOpen: 0, smile: -1, breath: 1.3 * Math.sin(t * 1.65), wind: o.wind ?? 0, ...(o.p || {}) },
    ik: { hF: [px + 200, gy - 625], hN: [px + 185, gy - 300], fN: [px - 70, gy - 3 * s, 0], fF: [px + 90, gy - 3 * s, .25] },
    hold: { N: CUFF, F: CUFF },
    onJoints: (j, m) => { J = j; M = m; },
  });
  const wN = jointPt(ctx, M, J.AN.wr), wF = jointPt(ctx, M, J.AF.wr), aN = jointPt(ctx, M, J.LN.ank), aF = jointPt(ctx, M, J.LF.ank);
  const slack = 1.03 - .03 * pull, sw = (o.wind ?? 0) * 6 * Math.sin(t * 1.3);
  ironChain(ctx, [wF[0] + 6, wF[1] - 4], [sF[0] - 18, sF[1]], { L0: len(sub(sF, wF)) * slack, sag: sw * .3 });
  ironChain(ctx, [wN[0] + 6, wN[1] - 4], [sN[0] - 18, sN[1]], { L0: len(sub(sN, wN)) * slack, sag: sw * .5 });
  ironChain(ctx, [aN[0], aN[1] - 12], sL, { L0: len(sub(sL, aN)) * 1.15, w: 5, link: 20 });
  ironChain(ctx, [aF[0], aF[1] - 12], sL, { L0: len(sub(sL, aF)) * 1.15, w: 5, link: 20 });
  stake(ctx, sF[0], sF[1], 3.6, Math.atan2(wF[1] - sF[1], wF[0] - sF[0]) + PI);
  stake(ctx, sN[0], sN[1], 3.6, Math.atan2(wN[1] - sN[1], wN[0] - sN[0]) + PI);
  stake(ctx, sL[0], sL[1] + 4, 2.4, -PI / 2);
  // gerilme anında kazıklardan toz dökülür
  if (ph > .3 && ph < .5) for (const q of [sF, sN]) motes(ctx, t, 6, 5 + q[1], 'rgba(201,112,63,.8)', [q[0] - 20, q[1], 40, 70], 30, 1.6, .6 * Math.sin((ph - .3) / .2 * PI));
  return { J, M, pull, wN, wF };
}
// Kartal gölgesi: kayanın ve bedenin üstünden geçen bulanık siluet (kaya poligonuna kırpılır)
function eagleShadow(ctx, x, y, s, o = {}) {
  ctx.save(); ctx.filter = 'blur(8px)'; ctx.globalAlpha *= o.a ?? .5;
  eagle2(ctx, x, y, s, 1, { ang: o.ang ?? .9, angFar: .2, farOff: -.55, col: '#050201', wingCol: '#050201', farCol: '#050201', line: 'rgba(0,0,0,0)', eye: '#050201' });
  ctx.restore();
}
// Dünya: gök, ova ve ateşler, kaya, zemin çizgisi, hâle. c: kamera. o: {sky, eagleX, eagleY, wind, fires}
function kayaWorld(ctx, t, c, o = {}) {
  const fl = .9 + .1 * noise1(t * 5, 7) + .05 * noise1(t * 15, 9), sky = o.sky || 'gece', wind = o.wind ?? windAt(t);
  glazeBG(ctx, t, { gx: 760, gy: 860, gr: 900, stars: false, warm: sky === 'safak' ? 'rgba(150,62,28,.6)' : undefined });
  glow(ctx, 300, 140, 900, 'rgba(36,48,70,.10)');
  ctx.save(); cam(ctx, c, .1);
  vaseStars(ctx, t, sky === 'gece' ? 60 : 22, 11, [0, 60, 1900, 620], [[o.eagleX ?? 700, o.eagleY ?? 320, 300], [1270, 330, 260]], sky === 'gece' ? .45 : .22);
  if (sky === 'safak') sunDisk(ctx, o.sunX ?? 560, o.sunY ?? 330, o.sunR ?? 230, o.sunA ?? 1);
  ctx.restore();
  ctx.save(); cam(ctx, c, .4); windLines(ctx, t, wind); ctx.restore();
  // ova: yüksekte ufuk (uçurumun yüksekliği), üç dalgalı ayrılmış zemin çizgisi, derinlikli ateşler
  ctx.save(); cam(ctx, c, .35);
  const hz = x => 760 + fbm1(x * .004, 3) * 18;
  ctx.fillStyle = '#140B07'; ctx.beginPath(); ctx.moveTo(-600, hz(-600)); for (let x = -600; x <= 1300; x += 20) ctx.lineTo(x, hz(x)); ctx.lineTo(1300, 1500); ctx.lineTo(-600, 1500); ctx.fill();
  ctx.strokeStyle = 'rgba(201,112,63,.55)'; ctx.lineWidth = 2.4;
  for (const [y0, a] of [[0, 1], [52, .8], [118, .6]]) { ctx.globalAlpha = a; ctx.beginPath(); for (let x = -600; x <= 1300; x += 20) { const y = hz(x) + y0 + fbm1(x * .006, 9 + y0) * 8; x > -600 ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); }
  ctx.globalAlpha = 1;
  glow(ctx, 640, 820, 600, `rgba(255,140,60,${.14 * fl})`);
  if (o.fires !== false) humanFires(ctx, t, [[120, 790, .45], [300, 802, .55], [480, 818, .7], [860, 846, 1.6]], o.fireA ?? 1, { people: [[810, 846, 1.25, 1], [912, 846, 1.25, -1]] });
  motes(ctx, t, 14, 21, 'rgba(255,190,110,.85)', [760, 640, 200, 200], 22, 1.3, .55 * (o.fireA ?? 1));
  ctx.restore();
  // kaya: kadrajın dışına (yukarı ve sağa) uzanır, yukarı çevrinme ve kaydırmalarda kenarı görünmez
  ctx.save(); cam(ctx, c, 1);
  const lw = 3.5 / Math.max(1, (c.z || 1) * .8);
  const R = [[1000, 1500], [1020, 900], [1040, 700], [1080, 560], [1130, 430], [1200, 300], [1290, 190], [1350, 120], [1420, 150], [1500, 95], [1580, 175], [1720, 240], [1990, 290], [2600, 230], [2600, 1500]];
  crag(ctx, R, { seed: 7, grad: [1050, '#5A311D', 1900, '#341C12'], line: C.ink, lw, hole: [1265, 560, 250, 390], strata: 7, lobes: 8, flat: [13, 14], bounce: [960, 860, 460, `rgba(255,150,70,${.22 * fl * (o.fireA ?? 1)})`] });
  // zemin çizgisi (vazo uylaşımı): figür kayanın üstündeki dalgalı bir çizgiye basar; altı hafif gölgeli
  const gl = x => 870 + fbm1(x * .02, 4) * 6 + Math.max(0, (x - 1400) * .12);
  ctx.beginPath(); ctx.moveTo(1035, gl(1035)); for (let x = 1035; x <= 2600; x += 12) ctx.lineTo(x, gl(x)); ctx.lineTo(2600, 1500); ctx.lineTo(1015, 1500); ctx.closePath();
  const sg = ctx.createLinearGradient(0, 870, 0, 1080); sg.addColorStop(0, 'rgba(14,9,7,.38)'); sg.addColorStop(1, 'rgba(14,9,7,.12)');
  ctx.fillStyle = sg; ctx.fill();
  ctx.strokeStyle = C.ink; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.beginPath(); for (let x = 1035; x <= 2600; x += 12) x > 1035 ? ctx.lineTo(x, gl(x)) : ctx.moveTo(x, gl(x)); ctx.stroke();
  // figürün arkasında sıcak hâle (ateşle titrer)
  glow(ctx, 1270, 540, 560, `rgba(150,60,25,${.38 * fl})`);
  // zincirin öbür ucu: üst kazığın halkasından göğe, bulutların içine (A02, J04)
  if (o.skyChain) {
    const sF = PROM_KAYA.sF, top = [sF[0] + 70, -1150], tug = o.chainTug || 0;
    ironChain(ctx, [sF[0] - 30, sF[1] - 4], top, { L0: len(sub(top, sF)) * (1.01 - .01 * Math.abs(tug)), sag: -tug * 12, w: 6, link: 24 });
    for (let i = 0; i < 6; i++) cloud(ctx, sF[0] - 260 + i * 120 + Math.sin(t * .2 + i) * 20, -560 + (i % 2) * 70, 1.5, '#1A100B', 'rgba(201,112,63,.4)', i + 3);
    if (o.glint) sparkle(ctx, top[0] - 30, -470, 30 * o.glint, o.glint, '#E6ECFF'); // Zeus'un rengi soğuk beyaz (altın ateşe ayrılmıştır)
  }
  ctx.restore();
  return { wind, fl };
}
// KAYA çerçevesi: üstte kesik meander (kırmızı figür), altta akan dalga kuşağı (ekranda sabit; dalga akar)
function kayaFrame(ctx, t, o = {}) {
  ctx.save(); baseT(ctx);
  const col = mixCol(PC.clayR, PC.glaze, .3), th = 38;
  meanderSaltire(ctx, -th * 2, W + th * 2, 0, th, col, PC.glaze);
  runningWave(ctx, -10, W + 10, H - th * 1.05, th * 1.05, col, t * 18 + (o.off || 0), PC.glaze);
  ctx.restore();
}
