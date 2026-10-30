// V. DURUŞMA: KAFKA'NIN GÖZÜYLE (F01–F14): iki şair iki Prometheus, Erhat'ın ikinci sorusu, duruşma (sanık, suç, görünmeyen yargıç),
// İskit uçurumu, Güç ve Zor (polis), Hephaistos, "Zeus'tan başka hiç kimse özgür değildir", özgürlük ve kölelik, sessizlik,
// göğe sesleniş, iç ses (rüzgâr durur)
'use strict';

// --- yardımcılar (F_ öneki) ---
// kamera anahtar kareleri: keys [[t, {x,y,z,r?,low?}], ...]; her anahtara 'lead' sn önce yumuşakça geçer
function F_cam(t, keys, lead = .9, drift = 4) {
  let i = 0; for (let k = 0; k < keys.length; k++) if (t >= keys[k][0] - lead) i = k;
  const a = keys[Math.max(0, i - 1)][1], b = keys[i][1], u = i === 0 ? 1 : E.io3(ramp(t, keys[i][0] - lead, keys[i][0], E.lin));
  const m = (p, q, d = 0) => lerp(p ?? d, q ?? d, u);
  return { x: m(a.x, b.x) - (t - keys[i][0]) * drift, y: m(a.y, b.y), z: m(a.z, b.z, 1) * (1 + .003 * Math.sin(t * .6)), r: m(a.r, b.r), low: m(a.low, b.low), sx: noise1(t * .3, 1) * 2, sy: noise1(t * .3, 2) * 1.5 };
}
// kayadaki konuklar (Prometheus'un arkasında, sağdaki çıkıntıda): Hephaistos, Kratos, Bia
const F_GL = x => 870 + Math.max(0, (x - 1400) * .12);
// konuklar arası ≥ 30 px boşluk (kil figürler kil zeminde birbirine karışmasın)
const F_POS = { heph: 1500, kratos: 1710, bia: 1920 };
// ikincil kırmızı figürler Prometheus'tan bir ton koyu (değer sırası: Prometheus öne çıkar)
const F_STY2 = { ...STY.red, fill: '#B4643A', white: '#B4643A' };
// son çizilen başlar (etiketlerin yardımcı çizgileri için): { kratos: [M, q], bia: [M, q] }
let F_HEADS = {};
function F_guests(ctx, t, o = {}) {
  const a = o.a ?? 1; if (a <= 0) return {};
  const out = {};
  ctx.save(); ctx.globalAlpha *= a;
  const ex = o.exit || 0; // kadrajdan çıkış: sağa yürürler
  if (o.bia !== false) { const x = F_POS.bia + ex * 700; walkScene(ctx, null, x, 5.6, t, ex > 0 ? 1 : -1, { noCam: true, ground: groundOf(F_GL), stand: ex > 0 ? 0 : 1, dist: x, sty: F_STY2, lk: { ...LK.bia, rf: false }, hold: { N: HOLD.spear(90) }, p: { torso: .02, ...(o.biaP || {}) }, onJoints: (j, m) => { F_HEADS.bia = [m, j.neckT]; } }); }
  if (o.kratos !== false) { const x = F_POS.kratos + ex * 700; out.kratos = walkScene(ctx, null, x, 5.8, t, ex > 0 ? 1 : -1, { noCam: true, ground: groundOf(F_GL), stand: ex > 0 ? 0 : 1, dist: x, sty: F_STY2, lk: LK.kratos, hold: { F: HOLD.spear(96) }, p: { torso: -.03, ...(o.kratosP || {}) }, onJoints: (j, m) => { F_HEADS.kratos = [m, j.neckT]; F_HEADS.kratosHand = [m, j.AN.wr]; } }); }
  if (o.heph !== false) { const x = F_POS.heph + ex * 700; let J = null, M = null;
    walkScene(ctx, null, x, 5.6, t, ex > 0 ? 1 : -1, { noCam: true, ground: groundOf(F_GL), stand: ex > 0 ? 0 : 1, dist: x, sty: F_STY2, lk: LK.hephaistos, hold: { N: HOLD.hammer() }, p: { torso: .05, ...(o.hephP || {}) }, onJoints: (j, m) => { J = j; M = m; } });
    out.hephJ = J; out.hephM = M; }
  ctx.restore();
  return out;
}
// dikey eksende boş taht (KAYA/EKSEN): karanlıkta yüksek siluet; gözler kısılabilir (o.eyes)
function F_throne(ctx, x, y, s, a, t, o = {}) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  glow(ctx, x + 40, y - 120, 260, 'rgba(0,0,0,.55)');
  throne(ctx, x, y, s, -1, '#120A07', 'rgba(201,112,63,.5)', { high: true });
  if (o.bolt > .02) { ctx.save(); ctx.globalAlpha *= o.bolt; lightning(ctx, x + 140, y - 330, x + 70, y - 60, 31 + Math.floor(t * 8), 5, '#E6ECFF'); ctx.restore(); }
  ctx.restore();
}
// mahkeme şeridi (üst katman): SANIK, SUÇ, YARGIÇ satırları sırayla dolar
function F_court(ctx, t, rows, a = 1) {
  if (a <= 0) return;
  ctx.save(); baseT(ctx); ctx.globalAlpha = a;
  const y0 = 40, h = 150;
  ctx.fillStyle = 'rgba(14,9,7,.82)'; ctx.fillRect(0, y0, W, h);
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(0, y0 + h - 6); ctx.lineTo(W, y0 + h - 6); ctx.stroke();
  rows.forEach(([lab, val, t0], i) => {
    const k = ramp(t, t0, t0 + .5); if (k <= 0) return;
    const x = [110, 560, 1560][i] ?? 110 + i * 600;
    txt(ctx, lab, x, y0 + 52, { font: '700 40px Cinzel', col: PC.clayR, align: 'left', ls: 5, a: k });
    txt(ctx, val, x, y0 + 104, { font: `600 ${val.length > 20 ? 40 : 46}px Cinzel`, col: '#F1E4C8', align: 'left', ls: 1, a: ramp(t, t0 + .2, t0 + .8), maxW: i === 1 ? 960 : 520 });
  });
  ctx.restore();
}
const F_SKY = 'sabah';
// süs Yunan harf akışı (Türkçe söz yok): ağızdan akan kil harfler
function F_greek(ctx, s, x, y, p, a = 1, o = {}) { if (a <= 0) return; ctx.save(); ctx.globalAlpha *= a; speechFlow(ctx, s, u => [x + (o.dir || -1) * u * (o.len || 520), y - Math.sin(u * PI) * 40 + u * (o.dy || 0)], p, { font: '600 40px Cinzel', col: o.col || PC.clayRL }); ctx.restore(); }

// --- P107: P106'daki maskeden geri çekilerek gündüz Atina tiyatrosu açılır; bölüm levhası sessizlikte ---
shot(PA('P107'), (ctx, st) => {
  const t = st.t, lt = st.lt, u = E.io3(ramp(lt, 0, 3.6, E.lin));
  theatre(ctx, t, { x: 960, y: lerp(455, 560, u), z: lerp(3.4, .95, u) }, { day: 1 });
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => chapterCard(ctx, 'BÖLÜM V', "DURUŞMA: KAFKA'NIN GÖZÜYLE", st.lt - .15, 3.4, { y: 170 }) });

// --- P108: iki tabak: solda siyah figür (Hesiodos), sağda kırmızı figür (Aiskhylos); taht kavgası aynı; F02@büsbütün'de Prometheus figürleri değişir ---
shot(PA('P108'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('F02@büsbütün'), push = E.io2(ramp(t, tB - .6, tB + .6)), ch = ramp(t, tB + .1, tB + .7);
  ctx.fillStyle = '#120B08'; ctx.fillRect(0, 0, W, H);
  const z = lerp(1, 1.18, push);
  ctx.save(); ctx.translate(960, 560); ctx.scale(z, z); ctx.translate(-960, -560);
  [[520, STY.black, 0], [1400, STY.red, 1]].forEach(([x, sty, i]) => {
    kylix(ctx, t, x, 560, 300, (i ? .1 : -.1) + lt * .03 * (i ? -1 : 1), (c, t, r) => {
      if (sty === STY.red) { c.fillStyle = PC.glaze; c.beginPath(); c.arc(0, 0, r, 0, TAU); c.fill(); }
      const gy = r * .55, col = sty === STY.red ? PC.clayR : C.ink;
      c.fillStyle = col; c.fillRect(-r, gy, 2 * r, 5);
      // aynı taht kavgası: iki taht, biri devrik
      c.save(); c.globalAlpha = .9; throneTip(c, -150, gy, 2.6, 1.1, { col, inc: sty === STY.red ? C.ink : C.clay }); throne(c, 150, gy, 2.6, 1, col, sty === STY.red ? C.ink : C.clay, { high: true }); c.restore();
      // Prometheus: solda hilekâr (eti saklayan, sinsice eğik), sağda zincirli kahraman; F02@büsbütün'de belirginleşir
      const lk = sty === STY.red ? { ...LK.prom, rf: true } : LK.promFree;
      if (i === 0) figure(c, { x: 0, y: gy - 44.5 * 2.8, s: 2.8, dir: 1, sty, lk, seed: 3, p: { torso: lerp(.05, .35, ch), neck: .2 * ch, head: .25 * ch, shN: lerp(.2, 1.4, ch), elN: 1.2, handN: 'fist' } });
      else figure(c, { x: 0, y: gy - 42.5 * 2.8, s: 2.8, dir: -1, sty, lk, seed: 17, hold: { N: CUFF, F: CUFF }, p: { torso: .15, neck: -.1, head: -.12 - .1 * ch, shN: lerp(.4, 2.6, ch), elN: .2, shF: lerp(.3, 1.4, ch), elF: .2, handN: 'fist', handF: 'fist' } });
      if (i === 1 && ch > 0) { c.save(); c.globalAlpha = ch; chain(c, [[16, gy - 230], [130, gy - 300]], 9, PC.clayR, null, 2.4); chain(c, [[22, gy - 150], [140, gy - 120]], 9, PC.clayR, null, 2.4); c.restore(); }
    }, { glaze: sty === STY.red ? C.ink : undefined });
  });
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .7, vig: .9, grain: .055 },
  over: (ctx, st) => { const a = ramp(st.lt, .3, .9); txt(ctx, 'HESİODOS', 520, 960 - 60, { font: '700 40px Cinzel', col: '#E3B98C', ls: 6, a }); txt(ctx, 'AİSKHYLOS', 1400, 960 - 60, { font: '700 40px Cinzel', col: '#E3B98C', ls: 6, a }); } });

// --- P109–P111: sayfa: iğneli NASIL? kartı ve ikinci soru; kenar şeridinde mahkeme; Kafka: dev kapının önünde bekleyen minik figür ---
const F_ST = () => [
  { at: PA('P109'), x: 960, draw: (ctx, lt, t) => {
    const tO = A('F03@öbür') - PA('P109');
    K_nasil(ctx, 360, 230, .75, -.05, .55 + .45 * Math.exp(-Math.pow((lt - tO - .6) / .7, 2)));
    ctx.fillStyle = PW.red; ctx.beginPath(); ctx.arc(360, 186, 6, 0, TAU); ctx.fill();
    penLine(ctx, 'Prometheus ne bakımdan', 1080, 430, ramp(t, A('F03@prometeus') - .1, A('F03@bakımdan') + .2), { font: 'italic 600 78px "Cormorant Garamond"', col: PW.ink });
    penLine(ctx, 'insandır?', 1080, 530, ramp(t, A('F03@insandır') - .1, A('F03@insandır') + .5), { font: 'italic 600 78px "Cormorant Garamond"', col: PW.red });
    txt(ctx, 'ERHAT · ÖNSÖZ · S. XI', 1080, 620, { font: '600 40px Cinzel', col: PW.line, ls: 4, a: ramp(t, A('F03@insandır') + .3, A('F03@insandır') + .9) });
  } },
  { at: PA('P110'), x: 2900, draw: (ctx, lt, t) => {
    // mahkeme: uzun sıra ve yüksek, boş yargıç kürsüsü (kalem çizer)
    const k = ramp(lt, 0, 2.2, E.lin);
    inkPoly(ctx, [[2300, 800], [3500, 800]], k * 2, { col: PW.line, w: 4 });
    inkPoly(ctx, [[2380, 700], [3000, 700], [3000, 800]], k * 1.6 - .2, { col: PW.line, w: 3 });
    for (let i = 0; i < 5; i++) inkPoly(ctx, [[2420 + i * 120, 700], [2420 + i * 120, 800]], k * 1.6 - .3, { col: PW.lineL, w: 2 });
    inkPoly(ctx, [[3150, 800], [3150, 330], [3450, 330], [3450, 800]], k * 1.4 - .2, { col: PW.ink, w: 5 });
    inkPoly(ctx, [[3120, 330], [3480, 330]], k * 1.4 - .4, { col: PW.ink, w: 7 });
    ctx.save(); ctx.globalAlpha = ramp(lt, 1.2, 2.2); txt(ctx, '—', 3300, 260, { font: '700 72px Cinzel', col: PW.red }); ctx.restore();
  } },
  { at: PA('P111'), x: 4800, z: 1.05, draw: (ctx, lt, t) => {
    // Kafka: dev kapı, aralığından ışık, önünde minicik bekleyen figür
    const fl = .85 + .15 * Math.sin(t * 3);
    ctx.fillStyle = 'rgba(43,29,20,.86)'; ctx.fillRect(4560, 150, 480, 650);
    ctx.fillStyle = `rgba(255,236,190,${.85 * fl})`; ctx.fillRect(4796, 150, 10, 650);
    glow(ctx, 4801, 600, 220, `rgba(255,230,180,${.35 * fl})`);
    inkPoly(ctx, [[4300, 800], [5300, 800]], 1, { col: PW.line, w: 3 });
    figure(ctx, { x: 4700, y: 800 - 44.5 * 1.2, s: 1.2, dir: 1, sty: STY.lek, lk: { hair: 'nape', garment: 'coat', modern: true }, seed: 4, p: { head: -.15, breath: Math.sin(t * 1.5) * .4 } });
  } },
];
let F_STATIONS = null;
shot(PA('P109'), (ctx, st) => { if (!F_STATIONS) F_STATIONS = F_ST(); pageJourney(ctx, st.t, F_STATIONS, {}); },
  { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 },
    over: (ctx, st) => { const t0 = A('F03@oyunu'); if (st.t > t0) erhatTag(ctx, st.t - t0, 'KAFKA · DAVA (1925)'); } });

// --- P112–P115: duruşma KAYA'da: mahkeme şeridi iner (sanık, suç, görünmeyen yargıç); taş stelde suç; karanlıkta boş taht; İskit ---
shot(PA('P112'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('F05b'), tZ = A('F05b@zeus'), tI = A('F06');
  const c = F_cam(t, [[PA('P112'), { ...CAMS.genis }], [A('F05@suçu'), { x: 1180, y: 520, z: 1.25 }], [tY, { x: 1425, y: 540, z: 1.0 }], [tI, { x: 760, y: 560, z: .92 }]], 1.0);
  const { wind } = kayaWorld(ctx, t, c, { sky: F_SKY });
  ctx.save(); cam(ctx, c, 1);
  // taş yasa steli (suçun kazındığı yer): çıkıntının solunda
  const sa = ramp(t, A('F05@suçu') - .3, A('F05@suçu') + .4) * (1 - ramp(t, tI - .4, tI));
  if (sa > 0) { ctx.save(); ctx.globalAlpha = sa; ctx.fillStyle = '#4A2817'; ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(1450, 872); ctx.lineTo(1470, 560); ctx.quadraticCurveTo(1560, 520, 1650, 560); ctx.lineTo(1670, 890); ctx.closePath(); ctx.fill(); ctx.stroke(); for (let i = 0; i < 5; i++) { ctx.strokeStyle = PC.clayR; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(1490, 620 + i * 46); ctx.lineTo(1490 + 140 * ramp(t, A('F05@ateşi') + i * .35, A('F05@ateşi') + .4 + i * .35), 620 + i * 46); ctx.stroke(); } ctx.restore(); }
  promChained(ctx, t, { wind, look: lerp(-.1, -.3, ramp(t, tY, tY + .8)) });
  ctx.restore();
  // dikey eksende boş taht (sanığın üstünde, karanlıkta); "Zeus"ta arkasında şimşek titrer
  const ta = ramp(t, tY - .3, tY + .8) * (1 - ramp(t, tI - .3, tI + .3));
  // ekranda, mahkeme şeridinin altında (sanığın sağ üstünde); soğuk hâle Zeus'un rengi
  if (ta > 0) { ctx.save(); baseT(ctx); glow(ctx, 1330, 360, 230, `rgba(160,175,220,${.16 * ta})`); F_throne(ctx, 1300, 540, 3.6, ta, t, { bolt: Math.exp(-Math.pow((t - tZ) / .09, 2)) + .6 * Math.exp(-Math.pow((t - tZ - .35) / .07, 2)) }); ctx.restore(); }
  // İskit (F06): kuşlar ve uzak dalgalar; rüzgâr güçlenir
  const ia = ramp(t, tI - .2, tI + .6);
  if (ia > 0) { ctx.save(); cam(ctx, c, .5); ctx.strokeStyle = 'rgba(201,112,63,.7)'; ctx.lineWidth = 3; for (let i = 0; i < 6; i++) { const bx = 200 + i * 170 + (t * 40 + i * 70) % 400, by = 220 + Math.sin(t * 1.2 + i) * 30 + i * 18, f = Math.sin(t * 6 + i) * 8; ctx.globalAlpha = ia; ctx.beginPath(); ctx.moveTo(bx - 18, by - f); ctx.quadraticCurveTo(bx - 6, by - 10, bx, by); ctx.quadraticCurveTo(bx + 6, by - 10, bx + 18, by - f); ctx.stroke(); } ctx.restore(); }
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tI = A('F06');
    F_court(ctx, t, [['SANIK', 'PROMETHEUS', A('F05@sanık')], ['SUÇ', 'ateşi çalmak · düzene karşı gelmek', A('F05@suçu')], ['YARGIÇ', '—', A('F05b@yargıç')]], ramp(t, PA('P112'), PA('P112') + .4) * (1 - ramp(t, tI - .3, tI + .2)));
    if (t > tI) erhatTag(ctx, t - tI, 'İSKİT · DÜNYANIN UCU', { d: 3.4, bg: 'rgba(238,229,209,.9)' });
  } });

// --- P116: vazo alayı: üç figür soldan sağa profilden yürür; Prometheus ortada, zinciri iki uşağın elinden bileğine gergin ---
shot(PA('P116'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { x: 1200 + lt * 30, y: 560, z: 1.15 };
  const { wind } = kayaWorld(ctx, t, c, { sky: F_SKY });
  ctx.save(); cam(ctx, c, 1);
  const g = x => F_GL(x) - 2, x0 = 1180 + lt * 70;
  const K = walkScene(ctx, null, x0 + 420, 5.2, t, 1, { noCam: true, ground: groundOf(g), stride: 36, dist: x0 + 420, sty: F_STY2, lk: LK.kratos, hold: { F: HOLD.spear(96) }, p: { shN: -.9, elN: .4, handN: 'fist' } });
  let Jp = null, Mp = null;
  walkScene(ctx, null, x0 + 140, 5.6, t, 1, { noCam: true, ground: groundOf(g), stride: 30, dist: x0 + 140, sty: STY.red, lk: { ...LK.promFree, rf: true }, p: { shN: .9, elN: .9, shF: .9, elF: 1.0, handN: 'fist', handF: 'fist', head: -.05 }, onJoints: (j, m) => { Jp = j; Mp = m; } });
  walkScene(ctx, null, x0 - 140, 5.2, t, 1, { noCam: true, ground: groundOf(g), stride: 36, dist: x0 - 140, sty: F_STY2, lk: LK.bia, hold: { N: HOLD.spear(90) }, p: { shF: .9, elF: .4 } });
  const w = jointPt(ctx, Mp, Jp.AN.wr);
  ironChain(ctx, [w[0], w[1]], [x0 + 330, F_GL(x0 + 330) - 300], { L0: 240, w: 5, link: 20 });
  ironChain(ctx, [w[0] - 10, w[1] + 6], [x0 - 70, F_GL(x0 - 70) - 290], { L0: 240, w: 5, link: 20 });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P117–P125: Güç ve Zor (polis), Kratos'un buyruğu, kıpırtısız profil, Hephaistos'un isteksizliği, boş taht, çekiç ---
shot(PA('P117'), (ctx, st) => {
  const t = st.t, lt = st.lt, tP = A('F08'), tIn = A('F08@insanseverlikten'), tH = A('F07'), tIs = A('F07@istemeyerek'), tA = A('F07@ama'), tK = A('F07@kendi#1'), tF9 = A('F09');
  const hit = A('F07@kendi#1') + 1.1;
  // kadrajlar: P117–P118 geniş; P119 Kratos'un omzunun üstünden (Kratos sağda ön planda, Prometheus x≈600); P120 yakın; P121 Hephaistos orta plan;
  // P122 titreyen el; P123 boş taht; P124 zincir yakın; P125 Hephaistos'un eğik başı yakın
  const c = F_cam(t, [[PA('P117'), { x: 1640, y: 600, z: 1.5 }], [tP, { x: 1384, y: 520, z: 1.96 }], [tIn, { ...CAMS.yakin, x: 1290 }], [tH, { x: 1480, y: 560, z: 2.0 }], [tIs, { x: 1600, y: 560, z: 2.3 }],
    [tA, { x: 1420, y: 420, z: 1.3 }], [tK, { ...CAMS.zincir, x: 1430, y: 330, z: 2.4 }], [tF9, { x: 1470, y: 470, z: 3.0 }]], .8);
  const { wind } = kayaWorld(ctx, t, c, { sky: F_SKY });
  { const ta = ramp(t, tA - .2, tA + .5) * (1 - ramp(t, tK + .3, tK + .9)); if (ta > 0) { ctx.save(); baseT(ctx); glow(ctx, 1330, 300, 230, `rgba(160,175,220,${.16 * ta})`); F_throne(ctx, 1300, 480, 3.6, ta, t, { bolt: Math.exp(-Math.pow((t - tA - .5) / .08, 2)) }); ctx.restore(); } }
  ctx.save(); cam(ctx, c, 1);
  const raise = ramp(t, tA, tA + .7) * (1 - ramp(t, hit - .1, hit + .05)), tremble = ramp(t, tIs, tIs + .3) * (1 - ramp(t, tA, tA + .3));
  const G = F_guests(ctx, t, { kratosP: { shF: t > tP && t < tIn ? -1.5 : .1, elF: .1, handF: 'open' },
    hephP: { shN: lerp(.4, 2.9, raise) + .05 * Math.sin(t * 30) * tremble, elN: lerp(.6, .3, raise), head: t > tIs && t < tA ? -.35 : 0, neck: t > tF9 ? .35 : 0, torso: t > tF9 ? .3 : .05 } });
  const freeF = t < hit - .04;
  const R = promChained(ctx, t, { wind, look: -.05, freeF, pullAdd: Math.exp(-Math.pow((t - hit) / .2, 2)) * .3 });
  // çekiç inene kadar zincirin ucu Kratos'un elinde (alaydan süreklilik: henüz kayaya çakılmadı)
  if (freeF && R && F_HEADS.kratosHand) { const kh = jointPt(ctx, F_HEADS.kratosHand[0], F_HEADS.kratosHand[1]); ironChain(ctx, [R.wF[0] + 6, R.wF[1] - 4], kh, { L0: len(sub(kh, R.wF)) * 1.08, sag: 20 }); }
  if (t > hit - .2) { hammerHit(ctx, PROM_KAYA.sF[0] - 22, PROM_KAYA.sF[1], hit, t, 1.0); if (t > hit && t - hit < .5) { dustBurst(ctx, t, hit, PROM_KAYA.sF[0], PROM_KAYA.sF[1], 24, 'rgba(201,112,63,.6)', 110, 6); sparkle(ctx, PROM_KAYA.sF[0] - 6, PROM_KAYA.sF[1], 24 * (1 - (t - hit) / .5), 1); } }
  ctx.restore();
  if (t > hit && t < hit + .15) { ctx.save(); baseT(ctx); ctx.fillStyle = '#FFF4DE'; ctx.globalAlpha = .5 * (1 - (t - hit) / .15); ctx.fillRect(0, 0, W, H); ctx.restore(); }
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tE = A('F06@erhat'), tP = A('F06@polis'), tF8 = A('F08');
    const na = ramp(st.lt, .2, .7) * (1 - ramp(t, tF8 - .3, tF8 + .2));
    if (na > 0) { ctx.save(); ctx.globalAlpha = na;
      // etiketler sağdaki boş şeritte; her biri kendi başına ince kil çizgiyle bağlanır (yüzleri kesmez)
      for (const [k, s, y] of [['kratos', 'ΚΡΑΤΟΣ · Güç', 210], ['bia', 'ΒΙΑ · Zor', 300]]) {
        // sağa hizalı (sağ uç x 1820, güvenli alan); çizgi tepeliklerin üstünden geçip kendi başında biter
        ctx.save(); ctx.font = '700 54px Cinzel'; ctx.letterSpacing = '4px'; const tw = ctx.measureText(L(s)).width; ctx.restore();
        const h = F_HEADS[k]; if (h) { const [hx, hy] = jointPt(ctx, h[0], h[1]); ctx.strokeStyle = 'rgba(219,134,85,.85)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(1800 - tw, y - 8); ctx.quadraticCurveTo(hx + 80, Math.min(hy - 140, 160), hx + 20, hy - 86); ctx.stroke(); }
        txt(ctx, s, 1820 - tw, y, { font: '700 54px Cinzel', col: '#F1E4C8', ls: 4, align: 'left', shadow: 'rgba(0,0,0,.7)', blur: 12 }); }
      ctx.restore();
      if (t > tP - .3) stamp(ctx, 'POLİS', 1690, 500, t - tP, { col: '#E6ECFF', font: '700 92px Cinzel', h: 130, a: .9 * (1 - ramp(t, tF8 - .3, tF8 + .2)) }); }
    // Kratos'un buyruğu: süs Yunan harf akışı; Hephaistos'un sözü kil levhada belirip söner; inleyişi soluk harfler
    F_greek(ctx, 'ΤΗΝ ΔΙΟΣ ΤΥΡΑΝΝΙΔΑ ΣΤΕΡΓΕΙΝ', 1180, 300, ramp(t, tF8 + .2, A('F08@insanseverlikten')), 1 - ramp(t, A('F08@insanseverlikten'), A('F08@insanseverlikten') + .5));
    const kt = A('F07@kendi#1'); if (t > kt && t < kt + 2.6) { ctx.save(); ctx.globalAlpha = .55 * (1 - ramp(t, kt + 1.8, kt + 2.6)); carvedTablet(ctx, ['ΑΠΑΣ ΔΕ ΤΡΑΧΥΣ', 'ΟΣΤΙΣ ΑΝ ΝΕΟΝ ΚΡΑΤΗι'], 560, 330, 700, t - kt, { font: '700 46px Cinzel' }); ctx.restore(); }
    F_greek(ctx, 'Ω ΠΟΛΛΑ ΜΙΣΗΘΕΙΣΑ ΧΕΙΡΩΝΑΞΙΑ', 1100, 320, ramp(t, A('F09@ah'), A('F09@zanaatım') + .3), .7 * (1 - ramp(t, A('F09@güçün') - .2, A('F09@güçün') + .3)));
  } });

// --- P126–P128: Kratos'un soğuk profili alttan; sözü kil levhaya kazınır; levha kenara konur; kenar şeridi: özgürlük · kölelik ---
shot(PA('P126'), (ctx, st) => {
  const t = st.t, lt = st.lt, tE = A('F10@erhatın');
  // P126 alttan: Kratos'un soğuk profili sağda (baş y≈420), üstte taş levha; kamera hafif eğik
  const c = F_cam(t, [[PA('P126'), { x: 1460, y: 450, z: 1.8, r: -.05 }], [A('F10'), { x: 1500, y: 620, z: 1.4, r: -.03 }], [tE, { ...CAMS.genis, x: 1000 }]], .9);
  const { wind } = kayaWorld(ctx, t, c, { sky: F_SKY });
  ctx.save(); cam(ctx, c, 1);
  F_guests(ctx, t, { kratosP: { head: -.12, neck: -.05 } });
  promChained(ctx, t, { wind });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tZ = A('F09@zeustan'), tF10 = A('F10'), tE = A('F10@erhatın');
    // Güç'ün sözü taş: kil levhaya kazınır; F10'da donar ve kenara (sol üst köşeye) konur
    if (t > tZ - .2) { const off = E.io2(ramp(t, tF10 + .6, tE + .2)); ctx.save(); ctx.translate(lerp(-100, -330, off), lerp(-30, -60, off)); ctx.globalAlpha = 1 - ramp(t, tE + 1.4, tE + 2.0);
      const s = lerp(.7, .5, off); ctx.translate(960, 330); ctx.scale(s, s); ctx.translate(-960, -330);
      carvedTablet(ctx, ['ZEUS’TAN BAŞKA HİÇ KİMSE', 'ÖZGÜR DEĞİLDİR.'], 960, 330, 1240, t - tZ, { font: '700 62px Cinzel', lh: 78 }); ctx.restore(); }
    erhatStrip(ctx, t - tE + .2, Se('F10') - tE + .6, 'özgürlük · kölelik', 'xiii', { icon: (c, p, lt) => { const a = .25 * Math.sin(lt * 1.6); c.save(); c.globalAlpha = p; c.strokeStyle = PW.line; c.lineWidth = 3; c.beginPath(); c.moveTo(0, 50); c.lineTo(0, -40); c.moveTo(-60 * Math.cos(a), -40 - 60 * Math.sin(a)); c.lineTo(60 * Math.cos(a), -40 + 60 * Math.sin(a)); c.stroke(); for (const sg of [-1, 1]) { c.beginPath(); c.arc(sg * 60 * Math.cos(a), -40 + sg * 60 * Math.sin(a) + 20, 18, 0, PI); c.stroke(); } c.restore(); } });
  } });

// --- P129: beyaz zemin kenar şeridi: Atina'da bir çömlekçi atölyesinde çalışan köleler (çark döner); eşleşen kesme: pranga → kelepçe ---
shot(PA('P129'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  ctx.save(); cam(ctx, { x: 960 + lt * 5, y: 540, z: 1.04 }, 1);
  paperBG(ctx, t, { seed: 73 });
  const gy = 760;
  marginBand(ctx, 260, 1660, 330, gy + 10, ramp(lt, 0, 1));
  // çömlekçi çarkı: döner tabla ve üstünde kabaran vazo
  const wx = 960; ctx.strokeStyle = PW.line; ctx.lineWidth = 4; ctx.beginPath(); ctx.ellipse(wx, gy - 60, 120, 20, 0, 0, TAU); ctx.stroke();
  for (let k = 0; k < 6; k++) { const a = t * 3 + k * PI / 3; ctx.beginPath(); ctx.moveTo(wx + Math.cos(a) * 110, gy - 60 + Math.sin(a) * 18); ctx.lineTo(wx + Math.cos(a) * 60, gy - 60 + Math.sin(a) * 10); ctx.stroke(); }
  ctx.beginPath(); ctx.moveTo(wx, gy - 60); ctx.lineTo(wx, gy); ctx.stroke();
  ctx.fillStyle = 'rgba(201,112,63,.85)'; ctx.beginPath(); ctx.moveTo(wx - 40, gy - 80); ctx.quadraticCurveTo(wx - 70, gy - 160, wx - 26, gy - 210 - 10 * Math.sin(t)); ctx.lineTo(wx + 26, gy - 210 - 10 * Math.sin(t)); ctx.quadraticCurveTo(wx + 70, gy - 160, wx + 40, gy - 80); ctx.fill();
  // çömlekçiler: oturan biri vazoyu biçimlendirir, biri kil taşır, biri fırını besler; ayak bileğinde pranga (saygılı, sade)
  figure(ctx, { x: wx - 210, y: gy - 28 - 44.5 * 3.4, s: 3.4, dir: 1, sty: STY.lek, lk: LK.human, seed: 31, p: { torso: .35, shN: 1.3 + .08 * Math.sin(t * 3), elN: .6, shF: 1.2, elF: .7, handN: 'open' }, ik: { fN: [wx - 110, gy - 10, 0], fF: [wx - 140, gy - 10, 0] } });
  walkScene(ctx, null, 520 + ((lt * 40) % 120), 3.2, t, 1, { noCam: true, ground: FLAT(gy), stride: 30, sty: STY.lek, lk: LK.human, hold: { N: HOLD.bag() }, p: { torso: .2 } });
  figure(ctx, { x: 1420, y: gy - 44.5 * 3.2, s: 3.2, dir: -1, sty: STY.lek, lk: LK.human, seed: 33, p: { torso: .25, shN: 1.2 + .3 * Math.sin(t * 2), elN: .3 } });
  // pranga yakın planı (sağ altta, eşleşen kesmenin kaynağı)
  const fx = 1450, fy = gy - 10; ctx.strokeStyle = PW.ink; ctx.lineWidth = 5; ctx.beginPath(); ctx.ellipse(fx, fy, 22, 9, 0, 0, TAU); ctx.stroke(); chain(ctx, [[fx + 20, fy], [fx + 150, fy + 4]], 14, PW.ink, null, 3);
  ctx.restore();
}, { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => erhatTag(ctx, st.lt, 'ATİNA · MÖ V. YY', { d: st.d }) });

// --- P130–P131: eşleşen sert kesme: zincirli bilekler (halkada ΔΕΣΜΩΤΗΣ dokusu); tanrısal altın kenar ışığı söner ---
shot(PA('P130'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('F10a@ama'), tD = A('F10a@köle#1');
  const c = F_cam(t, [[PA('P130'), { x: 1360, y: 560, z: 2.8 }], [tA, { ...CAMS.orta }]], 1.0);
  const { wind } = kayaWorld(ctx, t, c, { sky: F_SKY });
  ctx.save(); cam(ctx, c, 1);
  // tanrısal kenar ışığı: figürün arkasında altın çizgi, F10a@köle#1'de söner
  const gl = 1 - ramp(t, tD - .3, tD + 1.0);
  if (gl > 0) { ctx.save(); ctx.globalAlpha = gl * .8; glow(ctx, 1240, 520, 420, 'rgba(255,200,110,.35)'); ctx.restore(); }
  // ΔΕΣΜΩΤΗΣ (tutsak) yakın bilekteki kelepçe bandına kazılı; yüzen yazı değil
  promChained(ctx, t, { wind, look: .05 * (1 - gl), cuffText: lt < 3 ? 'ΔΕΣΜΩΤΗΣ' : null });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P132: kenar şeridinde geri saran panolar: öbürlerinin ağzından söz akar, Prometheus'un söz bandı boş; F10b@tek'te boşluk daire içine alınır ---
shot(PA('P132'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { ...CAMS.genis, x: 900 + lt * 6, z: 1.02 };
  const { wind } = kayaWorld(ctx, t, c, { sky: F_SKY });
  ctx.save(); cam(ctx, c, 1); F_guests(ctx, t, { a: .5 }); promChained(ctx, t, { wind }); ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tD = A('F10b@dikkat'), tT = A('F10b@tek');
    erhatStrip(ctx, t - tD + .3, A('F10b@çekiç') - tD + .2, 'Dikkat ettin mi?', 'xi', { icon: (c, p, lt) => {
      // dört küçük pano: Kratos, Hephaistos, Kratos konuşur (akan çizgi), Prometheus'un bandı boş
      for (let i = 0; i < 4; i++) { const x = -330 + i * 110; c.save(); c.globalAlpha = p; c.strokeStyle = PW.line; c.lineWidth = 2; c.strokeRect(x - 48, -60, 96, 120);
        if (i < 3) { c.beginPath(); for (let k = 0; k < 4; k++) { c.moveTo(x - 30, -40 + k * 12); c.lineTo(x - 30 + 60 * ((lt * 2 + k * .3 + i) % 1), -40 + k * 12); } c.stroke(); }
        figure(c, { x, y: 50 - 44.5 * .6, s: .6, dir: i === 3 ? -1 : 1, sty: STY.lek, lk: i === 3 ? LK.prom : LK.kratos, seed: 70 + i, still: true, p: {} }); c.restore(); }
      if (st.t > tT) circleMark(c, -0, -34, 54, 30, ramp(st.t, tT, tT + .7), { w: 3.5 });
    } });
  } });

// --- P133: ZİNCİR: P004'ün birebir kompozisyonu; iki vuruş F10b@indi #0 ve #1'de; her vuruşta kamera bir kademe yaklaşır ---
shot(PA('P133'), (ctx, st) => {
  const t = st.t, lt = st.lt, h1 = A('F10b@indi'), h2 = A('F10b@indi#1');
  const k = (t > h1 ? 1 : 0) + (t > h2 ? 1 : 0), sk = shake(t, t > h2 ? h2 : h1, 14, 7);
  const c = { x: lerp(1430, 1330, k / 2), y: lerp(300, 380, k / 2), z: lerp(1.9, 2.5, k / 2) + lt * .01, sx: sk[0], sy: sk[1] };
  const { wind } = kayaWorld(ctx, t, c, { skyChain: true, sky: F_SKY });
  ctx.save(); cam(ctx, c, 1);
  promChained(ctx, t, { wind, look: -.05 });
  const sF = PROM_KAYA.sF;
  for (const hh of [h1, h2]) { if (t > hh - .5 && t < hh + .3) hammerHit(ctx, sF[0] - 22, sF[1], hh, t, 1.1); if (t > hh) { dustBurst(ctx, t, hh, sF[0], sF[1], hh === h2 ? 40 : 24, 'rgba(201,112,63,.6)', hh === h2 ? 170 : 110, hh === h2 ? 8 : 4); if (t - hh < .5) sparkle(ctx, sF[0] - 6, sF[1], (hh === h2 ? 34 : 24) * (1 - (t - hh) / .5), 1); } }
  ctx.restore();
  for (const hh of [h1, h2]) if (t > hh && t < hh + .15) { ctx.save(); baseT(ctx); ctx.fillStyle = '#FFF4DE'; ctx.globalAlpha = .55 * (1 - (t - hh) / .15); ctx.fillRect(0, 0, W, H); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P135–P137: kilitli çene, sessiz profil; konuklar çıkar, dev kayada yapayalnız minik figür; başını göğe kaldırır ---
shot(PA('P135'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('F13'), tI = A('F13@ilk');
  const c = F_cam(t, [[PA('P135'), { ...CAMS.yakin, z: 3.2 }], [tY + .2, { x: 1050, y: 420, z: .62 }], [tI + .3, { ...CAMS.orta, y: 560 }]], 1.1);
  const { wind } = kayaWorld(ctx, t, c, { sky: F_SKY });
  ctx.save(); cam(ctx, c, 1);
  F_guests(ctx, t, { exit: ramp(t, tY - .2, tY + 2.4, E.lin), a: 1 - ramp(t, tY + 1.6, tY + 2.4) });
  promChained(ctx, t, { wind, look: -.05 - .32 * ramp(t, tI - .2, tI + .6) });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P138–P143: tek sürekli panorama: göğe sesleniş (EY KUTSAL GÖK), rüzgârlar, ırmaklar, denizin gülüşü, toprak; "bakın bana": yüze hızlı yaklaşma ---
shot(PA('P138'), (ctx, st) => {
  const t = st.t, lt = st.lt, tH = A('F13@hızlı'), tR = A('F13@ırmakların'), tD = A('F13@deniz'), tS = A('F13@sen'), tB = A('F13@bakın');
  const c = F_cam(t, [[PA('P138'), { x: 1100, y: 160, z: 1.0 }], [tH, { x: 700, y: 260, z: .9 }], [tR, { x: 1400, y: 560, z: 1.0 }], [tD, { x: 900, y: 760, z: 1.0 }], [tS, { x: 1300, y: 860, z: 1.25 }], [tB + .3, { ...CAMS.yakin, x: 1170, z: 3.0 }]], .9, 0);
  const wind = .5 + .45 * ramp(t, tH, tH + .8) * (1 - ramp(t, tR, tR + 1));
  kayaWorld(ctx, t, c, { sky: F_SKY, wind, clouds: 5 });
  ctx.save(); cam(ctx, c, .4);
  // hızlı kanatlı rüzgârlar: rüzgâr çizgileri kanat biçimli yaylara dönüşür ve bulutları sürer
  const wg = ramp(t, tH, tH + .6) * (1 - ramp(t, tR + .5, tR + 1.2));
  if (wg > 0) { ctx.strokeStyle = `rgba(242,214,170,${.55 * wg})`; ctx.lineWidth = 4; ctx.lineCap = 'round'; for (let i = 0; i < 7; i++) { const x = -200 + ((t * 260 + i * 330) % 2200), y = 120 + i * 60, f = Math.sin(t * 5 + i) * 18; ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x + 60, y - 40 - f, x + 120, y); ctx.quadraticCurveTo(x + 180, y - 40 + f, x + 240, y); ctx.stroke(); } }
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  // ırmakların kaynakları: kayadan inen su çizgileri
  const rv = ramp(t, tR, tR + .8);
  if (rv > 0) { ctx.strokeStyle = `rgba(150,180,200,${.6 * rv})`; ctx.lineWidth = 4; for (let k = 0; k < 4; k++) { ctx.beginPath(); for (let y = 300; y < 1000; y += 20) { const x = 1700 + k * 60 + Math.sin(y * .02 + t * 4 + k) * 10; y === 300 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); } ctx.setLineDash([30, 24]); ctx.lineDashOffset = -t * 120; ctx.stroke(); ctx.setLineDash([]); } }
  promChained(ctx, t, { wind, look: lerp(-.42, -.05, ramp(t, tS, tB + .4)), expr: t < tB ? 'goge' : 'direnc', pose: t < tB ? 'gok' : 'direnis' });
  // ve sen, herkesin anası toprak: kayanın dibinde kil ışığı
  const ea = Math.exp(-Math.pow((t - tS - .8) / 1.0, 2)); if (ea > .02) glow(ctx, 1300, 1000, 500, `rgba(201,112,63,${.3 * ea})`);
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
  // denizin sayısız gülüşü: alttaki dalga kuşağı pırıl pırıl güler
  const sm = ramp(t, tD, tD + .6) * (1 - ramp(t, tS, tS + .8));
  if (sm > 0) { ctx.save(); baseT(ctx); for (let i = 0; i < 18; i++) { const x = (i * 113 + t * 40) % W, y = H - 26 + Math.sin(t * 3 + i) * 6, f = Math.max(0, Math.sin(t * 7 + i * 1.7)); if (f > .5) sparkle(ctx, x, y, 10 * f * sm, sm, '#FFE9C4'); } ctx.restore(); }
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tE = A('F13@ey'), tB = A('F13@bakın');
    // ağzından göğe kil renkli söz akar: EY KUTSAL GÖK (anahtar dize, Türkçe)
    const p = ramp(t, tE, A('F13@gök') + .4, E.lin), a = 1 - ramp(t, A('F13@hızlı') + .8, A('F13@hızlı') + 1.6);
    if (p > 0 && a > 0) { ctx.save(); ctx.globalAlpha = a; speechFlow(ctx, 'EY KUTSAL GÖK', u => [lerp(820, 1040, u), lerp(560, 150, u)], p, { font: '700 76px Cinzel', follow: .2 }); ctx.restore(); }
    const p2 = ramp(t, tB, A('F13@çekiyorum') + .3, E.lin);
    if (p2 > 0) speechFlow(ctx, 'BAKIN BANA', u => [lerp(800, 260, u), 380 - Math.sin(u * PI) * 40], p2, { font: '700 72px Cinzel' });
  } });

// --- P144–P147: iç ses: F14@ama'da rüzgâr durur, en yakın büst, arka plan koyulaşır; gökte üç soluk siluet; geri çekilme, baş eğilir; söz yarım kalır ve rüzgârsız havada asılı kalır ---
shot(PA('P144'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('F14@ama'), tB = A('F14@bana#1'), tZ = A('F14@zorunluluğun'), tY = A('F14@yine');
  const still = ramp(t, tA - .1, tA + .25);
  const c = F_cam(t, [[PA('P144'), { ...CAMS.yakin, z: 3.2 }], [tA, { ...CAMS.yakin, z: 3.6 }], [tB, { ...CAMS.orta }], [tY + .3, { ...CAMS.orta, z: 1.65 }]], 1.0, 2);
  const wind = lerp(.5, 0, still);
  kayaWorld(ctx, t, c, { sky: F_SKY, wind, fireA: lerp(1, .5, still) });
  // arka plan sır siyahına koyulaşır
  ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(14,9,7,${.55 * still})`; ctx.fillRect(0, 0, W, H); ctx.restore();
  // gökte, bakış çizgisi yönünde üç soluk kırmızı figür siluet: kartal, fırtına, okçu
  ctx.save(); cam(ctx, c, .25);
  const vis = (w, d = 2.4) => { const t0 = A(w); return ramp(t, t0 - .2, t0 + .5) * (1 - ramp(t, t0 + d, t0 + d + .8)); };
  const v1 = vis('F14@önceden'), v2 = vis('F14@apaçık'), v3 = vis('F14@habersiz');
  if (v1 > 0) { ctx.save(); ctx.globalAlpha = .38 * v1; eagle2(ctx, 520 + (t - A('F14@önceden')) * 40, 300, 2.0, 1, { ang: .5 + .5 * Math.cos(t * 2.5), angFar: .3, col: '#B86438', wingCol: '#9A4F2C', farCol: '#7A3E22', eye: '#B86438' }); ctx.restore(); }
  if (v2 > 0) { ctx.save(); ctx.globalAlpha = .4 * v2; for (let i = 0; i < 4; i++) cloud(ctx, 640 + i * 150 + (t - A('F14@apaçık')) * 30, 260 + (i % 2) * 40, 1.6, '#3A2116', 'rgba(201,112,63,.5)', i + 31); lightning(ctx, 820, 240, 780, 460, 41, 4, 'rgba(230,236,255,.6)'); ctx.restore(); }
  if (v3 > 0) { ctx.save(); ctx.globalAlpha = .38 * v3; L_archer(ctx, 600 + (t - A('F14@habersiz')) * 30, 560, 3.4, t, .9, 0, { sty: { ...STY.red, fill: '#9A4F2C' } }); ctx.restore(); }
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  // kenardan tek tük kil tozu kopar (iç ses tabanı)
  if (still > .5) motes(ctx, t, 6, 77, 'rgba(201,112,63,.6)', [1000, 300, 500, 600], 14, 1.4, .5 * still);
  promChained(ctx, t, { wind, look: lerp(-.05, .22, ramp(t, tB - .4, tB + 1.2)), pose: t > tB ? 'sessiz' : 'direnis', pullK: lerp(.45, .1, ramp(t, tZ, tZ + 1)), p: { blink: Math.max(.28, blinkAt(t, 17)) } });
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tS = A('F14@susabiliyorum'), tK = A('F14@konuşabiliyorum'), tE = Se('F14');
    // söz yarım kalır (susabiliyorum), rüzgârsız havada asılı kalır (konuşabiliyorum) ve uzayan sessizlikte dağılır
    const p = Math.min(ramp(t, tS - .1, tS + .6, E.lin) * .55, .55) + .1 * ramp(t, tK, tK + .5);
    const fade = ramp(t, tE + .9, tE + 2.0);
    // iki satır, ağızdan sola akar (soldan sağa okunur)
    if (p > 0) { speechFlow(ctx, 'NE SUSABİLİYORUM', u => [lerp(760, 140, u), 250 - Math.sin(u * PI) * 30], clamp(p / .55 * 1.0), { font: '600 50px Cinzel', fade });
      if (p > .3) speechFlow(ctx, 'NE DE KONUŞABİLİYORUM', u => [lerp(780, 60, u), 330 - Math.sin(u * PI) * 30], clamp((p - .3) / .35), { font: '600 50px Cinzel', fade }); }
  } });
