// KAYA seti (kırmızı figür, Aiskhylos): filmin yaklaşık %38'i bu sette geçer. İskit uçurumu, zincirli Prometheus,
// ova ve insanların ateşleri, gök durumları (gece / şafak / fırtına), rüzgâr, akan dalga kuşağı.
// Bütün hareket t'nin kapalı fonksiyonudur (4 işçili render kareleri sırasız çizer; kareden kareye durum biriktirilmez).
'use strict';
const PROM_KAYA = { px: 1225, gy: 868, s: 6.3, sF: [1435, 165], sN: [1450, 690], sL: [1272, 876] };
// kamera ön ayarları: eşleşen planlar (ör. açılış ve I08c) aynı ayarı kullanır
const CAMS = {
  genis: { x: 900, y: 540, z: 1 },
  orta: { x: 1260, y: 585, z: 1.55 }, // boy plan: saç tepesi ≈85, ayaklar ≈975; sol 0–600 konuk için boş
  yakin: { x: 1290, y: 395, z: 3.4 }, // göz ≈330, sakal ucu ≈640: ağız altyazı bandının üstünde; plan içi yaklaşmada yalnız z değişir
  alt: { x: 1100, y: 560, z: 1.45, r: -.05, low: 1 }, // alttan kahraman karesi: ova aşağı iner, ışık kadrajın altından
  zincir: { x: 1400, y: 610, z: 2.8 }, // alt bilek kelepçesi ve kazığa giden zincir; baş kadraj dışında
  ust: p => ({ x: 1225, y: 500, z: lerp(.55, 1.3, p), r: lerp(.9, 0, p) }), // gökten figüre sarmal iniş (kartal bakışı)
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
// gökte vazo üslubu rüzgâr çizgileri (kil, sönük), sağa akar: rüzgâr soldan, açık denizden eser (saç, dalga kuşağı ve alevle aynı yön)
function windLines(ctx, t, wind, area = [0, 120, W, 560], n = 9, seed = 31) {
  const r = rng(seed);
  ctx.save(); ctx.strokeStyle = 'rgba(201,112,63,1)'; ctx.lineCap = 'round'; ctx.lineWidth = 2;
  for (let i = 0; i < n; i++) {
    const L = 60 + r() * 80, y = area[1] + r() * area[3], sp = (100 + r() * 80) * (.4 + wind), x = area[0] + ((r() * area[2] + t * sp) % (area[2] + 300) + area[2] + 300) % (area[2] + 300) - 150;
    ctx.globalAlpha = .16 * (.6 + wind * .6);
    ctx.beginPath(); ctx.moveTo(x, y); ctx.bezierCurveTo(x + L * .3, y - 6, x + L * .6, y + 6, x + L, y - 2); ctx.stroke();
    r(); // (eski uç kıvrımı kalktı: çizgi film dili; rastgele sıra korunur)
  }
  ctx.restore();
}
// şafak/güneş diski: kil tonunda (ateşin çekirdeğinden sönük), kenarı siyah konturlu
function sunDisk(ctx, x, y, r, a = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  // değer sırası: ateş > Prometheus > gök; disk figürden koyu kalır (başın arkasında ayla etkisi yapmaz)
  glow(ctx, x, y, r * 2.2, 'rgba(200,110,55,.10)');
  const g = ctx.createRadialGradient(x - r * .2, y - r * .2, r * .1, x, y, r);
  g.addColorStop(0, '#8E4826'); g.addColorStop(1, '#6A3420');
  ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
  ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke();
  ctx.restore();
}
// Prometheus'un KAYA pozları (geçişler plan kodunda mix ile 0,6–0,9 sn)
const PROM_POSE = {
  direnis: { torso: .2, neck: -.1, head: -.12 },
  gok: { torso: -.1, neck: -.3, head: -.38 },
  sessiz: { torso: .05, neck: .35, head: .25 },
  alay: { torso: .1, neck: -.1, head: -.15, mouthOpen: .5 },
};
// Zincirli Prometheus. o: {look, p (poz ekleri), expr (EXPR adı), pose (PROM_POSE adı), wind, pull (0..1 gerilme; verilmezse çok hafif nefes), dust}
function promChained(ctx, t, o = {}) {
  const { px, gy, s, sF, sN, sL } = PROM_KAYA;
  // taban gerilme: düzensiz, ağır bir ağırlık değişimi (metronom değil; çırpınma okunmasın diye genliği düşük), üstüne plan vuruşları (o.pullAdd)
  const tw = t + 1.2 * noise1(t * .12, 8), ph = (tw % 5.6) / 5.6;
  const cyc = (ph < .35 ? E.io2(ph / .35) : 1 - E.io2((ph - .35) / .65)) + settle(ph * 5.6, 1.96, .06, 1.7, 4);
  const pull = (o.pull ?? cyc * (o.pullK ?? .45)) + (o.pullAdd || 0);
  const base = { ...(PROM_POSE[o.pose || 'direnis']), ...(EXPR[o.expr || 'direnc']) };
  let J = null, M = null;
  const ik = { hF: [px + 200, gy - 625], hN: [px + 185, gy - 300], fN: [px - 95, gy - 3 * s, .05], fF: [px + 124, gy - 3 * s - 20, -.5] };
  // ayak zincirleri figürün arkasında (kalkık topuğun parmaklarını örtmesin): eklemleri önce görünmez bir çizimle al
  figure(ctx, { x: px, y: gy - 42.5 * s, s, dir: -1, sty: STY.red, lk: LK.prom, seed: 17, alpha: 0, ik, p: { ...base, torso: base.torso + .06 * pull }, onJoints: (j, m) => { J = j; M = m; } });
  const aN = jointPt(ctx, M, J.LN.ank), aF = jointPt(ctx, M, J.LF.ank);
  ironChain(ctx, [aN[0], aN[1] - 12], sL, { L0: len(sub(sL, aN)) * (1.15 - .05 * pull), w: 5, link: 20 });
  ironChain(ctx, [aF[0], aF[1] - 12], sL, { L0: len(sub(sL, aF)) * (1.15 - .05 * pull), w: 5, link: 20 });
  stake(ctx, sL[0], sL[1] + 4, 2.4, -PI / 2);
  figure(ctx, {
    x: px, y: gy - 42.5 * s, s, dir: -1, sty: STY.red, lk: LK.prom, seed: 17, stripe: .55,
    p: { handN: 'fist', handF: 'fist', breath: 1.3 * Math.sin(t * 1.65), wind: o.wind ?? 0, ...base, torso: base.torso + .06 * pull, head: (base.head || 0) + (o.look || 0), ...(o.p || {}) },
    ik, hold: { N: o.cuffText ? CUFF_TXT(o.cuffText) : CUFF, F: CUFF },
    onJoints: (j, m) => { J = j; M = m; },
  });
  const wN = jointPt(ctx, M, J.AN.wr), wF = jointPt(ctx, M, J.AF.wr);
  const slack = 1.03 - .03 * pull, sw = (o.wind ?? 0) * 6 * Math.sin(t * 1.3);
  // o.freeF: uzak bileğin zinciri henüz kayaya çakılmadı (V: zincirin ucu Kratos'un elinde, çekiç inince kazık belirir)
  if (!o.freeF) ironChain(ctx, [wF[0] + 6, wF[1] - 4], [sF[0] - 18, sF[1]], { L0: len(sub(sF, wF)) * slack, sag: sw * .3 });
  ironChain(ctx, [wN[0] + 6, wN[1] - 4], [sN[0] - 18, sN[1]], { L0: len(sub(sN, wN)) * slack, sag: sw * .5 });
  if (!o.freeF) stake(ctx, sF[0], sF[1], 2.3, Math.atan2(wF[1] - sF[1], wF[0] - sF[0]) + PI);
  stake(ctx, sN[0], sN[1], 2.3, Math.atan2(wN[1] - sN[1], wN[0] - sN[0]) + PI);
  // kazık tozu yalnız vuruşta (o.dust)
  if ((o.dust || 0) > .1) for (const q of (o.freeF ? [sN] : [sF, sN])) motes(ctx, t, 6, 5 + q[1], 'rgba(201,112,63,.8)', [q[0] - 20, q[1], 40, 70], 30, 1.6, .6 * o.dust);
  return { J, M, pull, wN, wF, neck: jointPt(ctx, M, J.neckT) };
}
// Kartal gölgesi: kayanın ve bedenin üstünden geçen bulanık siluet (kaya poligonuna kırpılır)
// Kartal gölgesi: tek parça, kanatları açık kartal silueti (kylix kartalının biçimi; baş öne, parmaklı birincil tüyler, yelpaze kuyruk).
// s: ölçek (s 1 ≈ 150 px kanat açıklığı); o.rot: dönüş; o.flap: kanat çırpışı; kenar bulanıklığı ≤ 4 px
function eagleShadow(ctx, x, y, s, o = {}) {
  const span = 150 * s / 2, fl = o.flap ?? Math.sin((window.FIG_T || 0) * 3) * .06;
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.rot ?? -.18); ctx.scale(span, span);
  ctx.filter = `blur(${Math.min(4, o.blur ?? 3)}px)`; ctx.globalAlpha *= o.a ?? .6; ctx.fillStyle = '#050201';
  ctx.beginPath();
  for (const e of [1, -1]) {
    const F = (px, py) => [e * px, py - fl * px * px];
    const P = [[.08, -.08], [.3, -.2], [.58, -.24], [.86, -.2], [1.0, -.12], [.93, -.07], [1.02, -.02], [.9, .01], [.97, .07], [.83, .07], [.88, .14], [.72, .13], [.62, .2], [.4, .2], [.16, .16]];
    const Q = P.map(([a, b]) => F(a, b));
    ctx.moveTo(...Q[0]); for (let k = 1; k < Q.length; k++) ctx.lineTo(...Q[k]); ctx.lineTo(0, .12); ctx.closePath();
  }
  // gövde, baş ve gaga (öne), yelpaze kuyruk (geriye)
  ctx.moveTo(.11, 0); ctx.ellipse(0, 0, .11, .3, 0, 0, TAU);
  ctx.moveTo(.08, -.34); ctx.arc(0, -.34, .08, 0, TAU);
  ctx.moveTo(-.03, -.42); ctx.quadraticCurveTo(.06, -.5, .02, -.55); ctx.lineTo(.05, -.42); ctx.closePath();
  ctx.moveTo(-.08, .22); ctx.lineTo(-.2, .52); ctx.lineTo(-.07, .48); ctx.lineTo(0, .55); ctx.lineTo(.07, .48); ctx.lineTo(.2, .52); ctx.lineTo(.08, .22); ctx.closePath();
  ctx.fill('nonzero');
  ctx.restore();
}
// Dünya: gök, ova ve ateşler, kaya, zemin çizgisi, hâle. c: kamera. o: {sky, eagleX, eagleY, wind, fires}
function kayaWorld(ctx, t, c, o = {}) {
  const sky = o.sky || 'gece', storm = sky === 'firtina', fl = .82 + .2 * noise1(t * 6, 7) + .1 * noise1(t * 13, 9), wind = o.wind ?? windAt(t, storm ? .9 : .5);
  // bölüm saati (güneşin yolu): sabah (V), ikindi (VII), gün batımı (VIII), gece, şafak, fırtına (X). Zemin hep siyah sır; saat güneş diski ve ufuk ışığıyla okunur
  const SUN = { safak: [560, 330, 230, 'rgba(150,62,28,.6)'], sabah: [300, 330, 110, 'rgba(150,66,30,.45)'], ikindi: [760, 160, 100, 'rgba(160,82,38,.4)'], gunbatimi: [330, 610, 170, 'rgba(176,60,24,.7)'] }[sky];
  glazeBG(ctx, t, { gx: 760, gy: 860, gr: 900, stars: false, warm: SUN ? SUN[3] : undefined });
  glow(ctx, 300, 140, 900, 'rgba(36,48,70,.10)');
  ctx.save(); cam(ctx, c, .1);
  if (sky === 'gece' || sky === 'safak' || storm) vaseStars(ctx, t, sky === 'gece' ? 60 : 22, 11, [0, 60, 1900, 620], [[o.eagleX ?? 700, o.eagleY ?? 320, 300], [1270, 330, 260]], storm ? .05 : sky === 'gece' ? .45 : .22, o.starRot || 0);
  if (SUN) sunDisk(ctx, o.sunX ?? SUN[0], o.sunY ?? SUN[1], o.sunR ?? SUN[2], o.sunA ?? 1);
  ctx.restore();
  // gece bulutları (o.clouds) ve fırtına: vazo bulutları rüzgârla sağa kayar; fırtınada düzensiz, kısa soğuk şimşek (saniyede ≤ 3 flaş)
  if (o.clouds || storm) { ctx.save(); cam(ctx, c, .2); const nC = storm ? 6 : (o.clouds === true ? 4 : o.clouds);
    for (let i = 0; i < nC; i++) { const x0 = (i * 523) % 2400, y = storm ? 40 + (i * 37) % 220 : 140 + (i * 53) % 180;
      cloud(ctx, ((x0 + t * (storm ? 40 : 8) * (.5 + wind)) % 2400) - 300, y, storm ? 1.9 : 1.4, '#1C120D', 'rgba(201,112,63,.35)', i + 21); }
    ctx.restore(); }
  if (storm && noise1(t * .7, 13) > .55 && (t * 30 | 0) % 12 < 4) { ctx.save(); cam(ctx, c, .2); bolt(ctx, 400 + 900 * (.5 + .5 * noise1(t * .2, 14)), 120, 1.6, .7, '#DDE3F2', 'rgba(210,220,255,.3)'); ctx.restore(); }
  ctx.save(); cam(ctx, c, .4); windLines(ctx, t, wind, undefined, storm ? 18 : 9); ctx.restore();
  // ova: yüksekte ufuk (uçurumun yüksekliği), üç dalgalı ayrılmış zemin çizgisi, derinlikli ateşler
  ctx.save(); cam(ctx, c, .35); ctx.translate(0, 300 * (c.low || 0));
  // telefon kuralı: ateş, yüz ve yazı y ≤ 700 (altyazı ve oynatıcı kontrolleri alt bandı kapatır)
  const hz = x => 610 + fbm1(x * .004, 3) * 16;
  ctx.fillStyle = '#140B07'; ctx.beginPath(); ctx.moveTo(-600, hz(-600)); for (let x = -600; x <= 1300; x += 20) ctx.lineTo(x, hz(x)); ctx.lineTo(1300, 1500); ctx.lineTo(-600, 1500); ctx.fill();
  ctx.strokeStyle = 'rgba(201,112,63,.55)'; ctx.lineWidth = 2.4;
  // büyük ateş grubunun çevresi temiz kalır (çizgiler başlardan ve ellerden geçmesin); grup kendi kısa zemin çizgisine basar
  const FX = 860, FY = 690;
  ctx.save(); ctx.beginPath(); ctx.rect(-4000, -4000, 9000, 9000); ctx.ellipse(FX, FY - 46, 150, 66, 0, 0, TAU); ctx.clip('evenodd');
  for (const [y0, a] of [[0, 1], [48, .8], [175, .6]]) { ctx.globalAlpha = a; ctx.beginPath(); for (let x = -600; x <= 1300; x += 20) { const y = hz(x) + y0 + fbm1(x * .006, 9 + y0) * 8; x > -600 ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); }
  ctx.restore();
  ctx.globalAlpha = .8; ctx.beginPath(); ctx.moveTo(FX - 125, FY + 5); ctx.bezierCurveTo(FX - 60, FY + 1, FX + 60, FY + 7, FX + 125, FY + 3); ctx.stroke();
  ctx.globalAlpha = 1;
  glow(ctx, 660, 680, 600, `rgba(255,140,60,${.14 * fl})`);
  if (o.fires !== false && !c.low) humanFires(ctx, t, [[95, 630, .38], [215, 644, .46], [505, 666, .62], [860, 690, 1.6]], o.fireA ?? 1, { wind, people: [[798, 690, 1.25, 1], [924, 690, 1.25, -1]] });
  if (c.low) glow(ctx, 1150, 820, 700, `rgba(255,140,60,${.22 * fl})`); // ALT: ateş kadraj dışında, ışık aşağıdan
  motes(ctx, t, 14, 21, 'rgba(255,190,110,.85)', [760, 480, 200, 200], 22, 1.3, .55 * (o.fireA ?? 1));
  ctx.restore();
  // kaya: kadrajın dışına (yukarı ve sağa) uzanır, yukarı çevrinme ve kaydırmalarda kenarı görünmez
  ctx.save(); cam(ctx, c, 1);
  const lw = 3.5 / Math.max(1, (c.z || 1) * .8);
  const R = [[1000, 1500], [1020, 900], [1040, 700], [1080, 560], [1130, 430], [1200, 300], [1290, 190], [1350, 120], [1420, 150], [1500, 95], [1580, 175], [1720, 240], [1990, 290], [2600, 230], [2600, 1500]];
  crag(ctx, R, { seed: 7, grad: [1050, '#5A311D', 1900, '#341C12'], line: C.ink, lw, hole: [1265, 560, 250, 390], strata: 7, lobes: 8, flat: [13, 14], avoid: [[PROM_KAYA.sF[0], PROM_KAYA.sF[1], 150], [PROM_KAYA.sN[0], PROM_KAYA.sN[1], 150]], bounce: [935, 740, 300, `rgba(255,150,70,${.36 * fl * (o.fireA ?? 1)})`], shade: [1290, 540, 430, 'rgba(14,9,7,.55)'] });
  // zemin çizgisi (vazo uylaşımı): figür kayanın üstündeki dalgalı bir çizgiye basar; altı hafif gölgeli
  const gl = x => 870 + fbm1(x * .02, 4) * 6 + Math.max(0, (x - 1400) * .12);
  ctx.beginPath(); ctx.moveTo(1035, gl(1035)); for (let x = 1035; x <= 2600; x += 12) ctx.lineTo(x, gl(x)); ctx.lineTo(2600, 1500); ctx.lineTo(1015, 1500); ctx.closePath();
  const sg = ctx.createLinearGradient(0, 870, 0, 1080); sg.addColorStop(0, 'rgba(14,9,7,.38)'); sg.addColorStop(1, 'rgba(14,9,7,.12)');
  ctx.fillStyle = sg; ctx.fill();
  ctx.strokeStyle = C.ink; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.beginPath(); for (let x = 1035; x <= 2600; x += 12) x > 1035 ? ctx.lineTo(x, gl(x)) : ctx.moveTo(x, gl(x)); ctx.stroke();
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
// ön katman (k 1,5): ateşten yükselip kameranın önünden geçen iri, sönük közler; figürden sonra, çerçeveden önce çizilir
function kayaFront(ctx, t, c, wind = .5, a = 1) {
  ctx.save(); cam(ctx, c, 1.5); motes(ctx, t, 16, 41, 'rgba(255,180,110,.28)', [-300, 80, 2600, 900], -18, 2.4, (.5 + .4 * wind) * a); ctx.restore();
}
// KAYA çerçevesi: üstte kesik meander (kırmızı figür), altta akan dalga kuşağı (ekranda sabit; dalga akar)
function kayaFrame(ctx, t, o = {}) {
  ctx.save(); baseT(ctx);
  const col = mixCol(PC.clayR, PC.glaze, .3), th = 38;
  meanderSaltire(ctx, -th * 2, W + th * 2, 0, th, col, PC.glaze);
  runningWave(ctx, -10, W + 10, H - th * 1.05, th * 1.05, col, t * 18 + (o.off || 0), PC.glaze);
  ctx.restore();
}
