// XII. BAŞKALDIRAN YARATIK (K08a–K06): NASIL? sorusunun cevabı (siyasi kişi, politik dram), akıl gücü ile kaba güç,
// sanık hâlâ insana benziyor; önsözün ilk sayfası: insan başkaldıran yaratıktır; tek uzun sayfa yolculuğu; başlığın halkası
'use strict';

// --- P275: bölüm kartı; önceki planlarda iğneli duran küçük NASIL? kartı iğnesinden kopar ve kadrajı doldurur ---
function K_nasil(ctx, x, y, s, rot, a = 1) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s); ctx.globalAlpha *= a;
  ctx.fillStyle = 'rgba(70,45,25,.22)'; ctx.fillRect(-150 + 6, -70 + 8, 300, 140);
  ctx.fillStyle = PW.paperL; ctx.fillRect(-150, -70, 300, 140); ctx.strokeStyle = PW.line; ctx.lineWidth = 2; ctx.strokeRect(-150, -70, 300, 140);
  txt(ctx, 'NASIL?', 0, 4, { font: '900 74px Cinzel', col: PW.red, ls: 4, force: true });
  ctx.restore();
}
shot(PA('P275'), (ctx, st) => {
  const t = st.t, lt = st.lt, tS = A('K08a@sorusu'), tN = A('K08a@nasıl');
  const c = { x: W / 2 + lt * 3, y: H / 2, z: 1 + lt * .006 };
  ctx.save(); cam(ctx, c, 1);
  paperBG(ctx, t, { seed: 52 });
  for (let i = 0; i < 6; i++) scribble(ctx, 360, 380 + i * 60, 1200, 1, 70 + i, { col: 'rgba(74,52,35,.28)' });
  ctx.restore();
  // kart: sağ üstte iğneli ve soluk; K08a@sorusu'da iğneden kopar, sallanarak büyür ve kadrajın ortasına gelir
  const k = E.io3(ramp(t, tS, tN - .05, E.lin)), sw = Math.exp(-Math.max(0, t - tS) * 3) * Math.sin((t - tS) * 10) * .12 * (t > tS ? 1 : 0);
  const x = lerp(1560, 960, k), y = lerp(210, 470, k), s = lerp(.55, 2.4, k);
  if (k < .05) { ctx.fillStyle = PW.red; ctx.beginPath(); ctx.arc(1560, 156, 7, 0, TAU); ctx.fill(); }
  K_nasil(ctx, x, y, s, lerp(-.06, 0, k) + sw, lerp(.7, 1, k));
}, { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => chapterCard(ctx, 'BÖLÜM XII', 'BAŞKALDIRAN YARATIK', st.lt - .15, 3.2, { y: 170 }) });

// --- P276: B06'nın bölünmüş karesi: solda Aiskhylos yazar (kırmızı figür levha), sağda XX. yüzyıl insanı ayakta; K08a@yaratabildi'de döner ---
shot(PA('P276'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('K08a@yaratabildi'), turn = ramp(t, tY - .2, tY + .5);
  const c = { x: 960 + lt * 4, y: 540, z: 1.02 + lt * .004 };
  ctx.save(); cam(ctx, c, 1);
  paperBG(ctx, t, { seed: 53 });
  // sol levha (kırmızı figür)
  ctx.save(); ctx.translate(520, 500);
  ctx.fillStyle = PC.glaze; ctx.fillRect(-330, -300, 660, 600); ctx.strokeStyle = PW.line; ctx.lineWidth = 6; ctx.strokeRect(-330, -300, 660, 600);
  ctx.save(); ctx.beginPath(); ctx.rect(-330, -300, 660, 600); ctx.clip();
  const wr = .1 * Math.sin(t * 3);
  figure(ctx, { x: -80, y: 270 - 44.5 * 5.4, s: 5.4, dir: 1, sty: STY.red, lk: AISKH, seed: 31, stripe: .5, p: { torso: .3, neck: .25, head: .2, shN: 1.2 + wr, elN: 1.1, handN: 'fist', breath: .5 * Math.sin(t * 1.5) } });
  flame(ctx, 210, 110, .6, t, { haloR: 90 });
  ctx.restore(); ctx.restore();
  txt(ctx, 'MÖ V. yy', 520, 860, { font: '600 40px Cinzel', col: PW.line, ls: 4 });
  // sağ: ayakta XX. yüzyıl insanı; döner ve Aiskhylos'a bakar
  figure(ctx, { x: 1480, y: 800 - 44.5 * 6.2 + 30, s: 6.2, dir: turn > .5 ? -1 : 1, sty: STY.lek, lk: { hair: 'nape', garment: 'coat', modern: true }, seed: 12,
    p: { torso: -.02, head: turn > .5 ? lerp(.2, -.05, (turn - .5) * 2) : lerp(0, .2, turn * 2), breath: .6 * Math.sin(t * 1.6) }, ik: { fN: [1500, 797, 0], fF: [1450, 797, 0] } });
  txt(ctx, 'XX. yy', 1480, 870, { font: '600 40px Cinzel', col: PW.red, ls: 4 });
  // çizgi bu kez sağdan sola akar: XX. yüzyıldan Aiskhylos'a
  inkPoly(ctx, sampleF(u => [lerp(1330, 880, u), 470 + Math.sin(u * PI * 3) * 36], 60), ramp(t, tY, tY + 2.2, E.lin), { col: PW.red, w: 4 });
  ctx.restore();
  // NASIL? P275'in kartından eşleşen kesmeyle gelir: üstte, yeniden yazılmaz
  K_nasil(ctx, 960, 150, 1.25 - ramp(lt, 0, 1.2) * .25, 0, 1);
}, { tr: { type: 'cut' }, post: { tex: .35, vig: .55, grain: .045 } });

// --- P277–P278: tek kesintisiz kırmızı figür tiyatro planı: skenede taht kavgası, ortada Prometheus (siyasi kişi); kamera Atinalı kalabalığa döner ---
shot(PA('P277'), (ctx, st) => {
  const t = st.t, lt = st.lt, tT = A('K08a@taht'), tS = A('K08a@siyasi'), tP = A('K08a@politik'), tA = A('K08a@ayshilostu');
  const pan = E.io3(ramp(t, tP - .2, tP + 2.2, E.lin));
  const c = { x: lerp(960, 960, pan), y: lerp(470, 640, pan), z: lerp(1.75, 1.1, pan) + lt * .004 };
  theatre(ctx, t, c, { crowd: true });
  ctx.save(); cam(ctx, c, 1);
  // skene frizi: iki küme taht kavgası (Titanlar, Olymposlular), ortada dimdik Prometheus
  const fy = 525, sc = 1.55;
  ctx.fillStyle = '#1C100B'; ctx.fillRect(640, fy - 70, 640, 70);
  const ph = ramp(t, tT - .3, tT + .6);
  for (const [x, dir, lk] of [[700, 1, { beard: 'short', hair: 'nape', garment: 'short' }], [760, 1, { beard: 'full', hair: 'long', garment: 'short' }], [1160, -1, LK.zeus], [1220, -1, { beard: 'short', hair: 'nape', headgear: 'helmet', garment: 'short' }]]) {
    figure(ctx, { x, y: fy - 44.5 * sc, s: sc, dir, sty: STY.red, lk: { ...lk, rf: true, earHidden: true }, seed: x | 0,
      p: { torso: .25 * ph, shN: lerp(.2, -1.6, ph) + .1 * Math.sin(t * 4 + x), elN: .4, handN: 'fist' }, hold: { N: HOLD.spear(60) } });
  }
  figure(ctx, { x: 960, y: fy - 44.5 * sc * 1.15, s: sc * 1.15, dir: -1, sty: STY.red, lk: { ...LK.promFree, legIrons: false }, seed: 17, stripe: .4, p: { torso: 0, head: -.05, breath: .5 * Math.sin(t * 1.4) } });
  ctx.restore();
  // Erhat'ın kalemi siyasi kişiyi daire içine alır (P048'in eşi): ekran katmanında, kameranın üstünde değil; kamera dönünce söner
  const cm = ramp(t, tS, tS + 1.0) * (1 - ramp(t, tP, tP + .8));
  if (cm > 0) { ctx.save(); cam(ctx, c, 1); circleMark(ctx, 960, fy - 50, 70, 92, cm * 1.05, { w: 3.4 }); ctx.restore(); }
  // kandil ışığında ΑΙΣΧΥΛΟΣ: kalabalığın önünde yanar
  const la = ramp(t, tA - .3, tA + .6);
  if (la > 0) { ctx.save(); cam(ctx, c, 1); oilLamp(ctx, 760, 905, 2.2, t); dipinto(ctx, 'ΑΙΣΧΥΛΟΣ', 1000, 880, 58, { col: mixCol('#5A311D', PC.fire, la), a: la, w: .1, glow: la }); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const t0 = A('K08a@politik#1'); erhatStrip(ctx, st.t - t0, 3.2, '“politik görüşü en köklü”', 'vi'); } });

// --- P279–P279b: terazide kaba güç ile akıl; düşünceye gem vurulamaz: gem kırılır, kanatlı düşünce sayfadan kaçar ---
shot(PA('P279'), (ctx, st) => {
  const t = st.t, lt = st.lt, tU = A('K08c@üstündür'), tD = A('K08c@düşünceye'), tG = A('K08c@gem'), tV = A('K08c@vurulamaz');
  const c = { x: 960 + lt * 3, y: 540, z: 1 + lt * .005 };
  ctx.save(); cam(ctx, c, 1);
  paperBG(ctx, t, { seed: 54 });
  // terazi: dikey direk, kiriş; akıl ağır basar (K08c@üstündür)
  const tilt = lerp(.12, -.2, E.outBack(ramp(t, tU - .2, tU + .9, E.lin))) + .01 * Math.sin(t * 2);
  const px = 960, py = 300;
  inkPoly(ctx, [[px, py], [px, 720]], ramp(lt, 0, .5), { col: PW.line, w: 6 });
  inkPoly(ctx, [[px - 120, 740], [px + 120, 740]], ramp(lt, .2, .6), { col: PW.line, w: 6 });
  const ends = [-1, 1].map(sg => [px + sg * 380 * Math.cos(tilt), py + sg * 380 * Math.sin(tilt)]);
  inkPoly(ctx, [ends[0], ends[1]], ramp(lt, .3, .9), { col: PW.line, w: 7 });
  ends.forEach(([ex, ey], i) => {
    inkPoly(ctx, [[ex, ey], [ex - 70, ey + 150]], ramp(lt, .6, 1.0), { col: PW.line, w: 2.2 });
    inkPoly(ctx, [[ex, ey], [ex + 70, ey + 150]], ramp(lt, .6, 1.0), { col: PW.line, w: 2.2 });
    inkPoly(ctx, sampleF(u => [ex - 90 + 180 * u, ey + 150 + Math.sin(u * PI) * 26], 20), ramp(lt, .8, 1.2), { col: PW.line, w: 4 });
    if (i === 0) { // kaba güç: ağır çomak
      ctx.save(); ctx.translate(ex, ey + 128); ctx.rotate(-.25); ctx.fillStyle = PW.ink; ctx.beginPath(); ctx.moveTo(-60, 6); ctx.lineTo(50, -6); ctx.quadraticCurveTo(76, -12, 74, 4); ctx.quadraticCurveTo(70, 18, 50, 10); ctx.lineTo(-60, 12); ctx.closePath(); ctx.globalAlpha = ramp(lt, 1.0, 1.4); ctx.fill(); ctx.restore();
    } else { // akıl: küçük, ağır bir kıvılcım
      const a = ramp(lt, 1.2, 1.6); if (a > 0) { glow(ctx, ex, ey + 118, 90, `rgba(255,180,90,${.5 * a})`); flame(ctx, ex, ey + 140, .8 * a, t, { haloR: 60 }); }
    }
  });
  // gem: K08c@düşünceye'de sağ üstte çizilir; K08c@gem'de kırılır; K08c@vurulamaz'da kanatlı düşünce sayfadan uçar
  const g0 = ramp(t, tD - .1, tD + .4), br = ramp(t, tG, tG + .35, E.out3);
  if (g0 > 0) {
    ctx.save(); ctx.translate(1500, 250); ctx.globalAlpha = g0 * (1 - ramp(t, tV + .6, tV + 1.4));
    for (const sg of [-1, 1]) { ctx.save(); ctx.translate(sg * (90 + br * 60), br * 40 * (sg > 0 ? 1 : -.3)); ctx.rotate(sg * br * .6); ctx.strokeStyle = PW.ink; ctx.lineWidth = 7; ctx.beginPath(); ctx.arc(sg * 40, 0, 34, 0, TAU); ctx.stroke(); ctx.beginPath(); ctx.moveTo(-sg * 50, 0); ctx.lineTo(sg * 6, 0); ctx.stroke(); ctx.restore(); }
    ctx.restore();
    if (br > 0 && t - tG < .6) dustBurst(ctx, t, tG, 1500, 250, 18, 'rgba(74,52,35,.6)', 90, 3);
  }
  const fly = ramp(t, tV - .1, tV + 1.6, E.in2);
  if (fly > 0) {
    const bx = lerp(1500, 2200, fly), by = lerp(250, -120, fly), fl = Math.sin(t * 18);
    ctx.save(); ctx.translate(bx, by); ctx.strokeStyle = PW.red; ctx.lineWidth = 5; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(-40, -10 * fl); ctx.quadraticCurveTo(-18, -26 * fl, 0, 0); ctx.quadraticCurveTo(18, -26 * fl, 40, -10 * fl); ctx.stroke(); ctx.restore();
  }
  ctx.restore();
}, { tr: { type: 'ink', dur: .5, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => {
    const a = ramp(st.lt, 1.0, 1.6);
    txt(ctx, 'KABA GÜÇ', 560, 760, { font: '700 46px Cinzel', col: PW.ink, ls: 4, a });
    txt(ctx, 'AKIL GÜCÜ', 1360, 760, { font: '700 46px Cinzel', col: PW.red, ls: 4, a });
  } });

// --- P280: KAYA ORTA: zincirli sanık; K08c@sanık'ta siluet bir an modern bir insan siluetine döner ve geri gelir ---
shot(PA('P280'), (ctx, st) => {
  const t = st.t, lt = st.lt, tS = A('K08c@sanık'), tB = A('K08c@benziyor');
  const c = { ...CAMS.orta, x: CAMS.orta.x - lt * 4, z: CAMS.orta.z + lt * .006 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'gunbatimi' });
  const m = ramp(t, tS - .1, tS + .5) * (1 - ramp(t, tB + .3, tB + 1.0));
  ctx.save(); cam(ctx, c, 1);
  ctx.save(); ctx.globalAlpha = 1 - m * .85; promChained(ctx, t, { wind }); ctx.restore();
  if (m > 0) {
    // aynı duruşta modern siluet: koyu kil, kontur ateş ışıklı (yüz yok)
    const { px, gy, s } = PROM_KAYA;
    ctx.save(); ctx.globalAlpha = m;
    figure(ctx, { x: px, y: gy - 42.5 * s, s, dir: -1, sty: { ...STY.red, fill: '#2A170F', cut: PC.clayR, line: PC.clayR }, lk: { hair: 'nape', garment: 'coat', modern: true }, seed: 17,
      ik: { hF: [px + 200, gy - 625], hN: [px + 185, gy - 300], fN: [px - 95, gy - 3 * s, .05], fF: [px + 124, gy - 3 * s - 20, -.5] }, p: { ...PROM_POSE.direnis, handN: 'fist', handF: 'fist' } });
    ctx.restore();
  }
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P281–P288a: önsözün ilk sayfası; tek uzun sayfa yolculuğu: aynı küçük figür bütün durakları geçer ---
const K_LK = { hair: 'nape', garment: 'short' };
const K_STY = { ...STY.lek };
function K_walker(ctx, x, gy, s, t, o = {}) {
  return walkScene(ctx, null, x, s, t, o.dir || 1, { noCam: true, ground: FLAT(gy), stride: 40, lean: .08, dist: o.dist ?? x, stand: o.stand || 0, sty: o.sty || K_STY, lk: o.lk || K_LK, hold: o.hold, p: o.p || {} });
}
// iç içe çerçeveler (P283): içte siyah figür (kil zemin, meander), ortada kırmızı figür (sır zemin), dışta sayfa; sayfanın dışı ateşin altın ışığı
const K_FR = [[-260, -190, 260, 190], [-470, -300, 470, 300], [-700, -400, 700, 400]];
function K_frames(ctx, cx, cy, t, figX, gy, s) {
  const rect = (r, o = 0) => ctx.rect(cx + r[0] - o, cy + r[1] - o, r[2] - r[0] + 2 * o, r[3] - r[1] + 2 * o);
  // dış ışık
  glow(ctx, cx + 900, cy + 120, 700, 'rgba(255,180,90,.5)');
  ctx.save(); ctx.beginPath(); rect(K_FR[2]); ctx.fillStyle = PW.paperL; ctx.fill(); ctx.restore();
  ctx.save(); ctx.beginPath(); rect(K_FR[1]); ctx.fillStyle = PC.glaze; ctx.fill(); ctx.restore();
  ctx.save(); ctx.beginPath(); rect(K_FR[0]); ctx.fillStyle = C.clay; ctx.fill(); ctx.restore();
  // figür her bölgede o bölgenin tekniğiyle (sınırı geçerken ikiye bölünmüş görünür)
  const zones = [
    { clip: c => { c.beginPath(); rect(K_FR[0]); }, sty: STY.black },
    { clip: c => { c.beginPath(); rect(K_FR[1]); rect(K_FR[0]); }, sty: STY.red, eo: true },
    { clip: c => { c.beginPath(); rect(K_FR[2]); rect(K_FR[1]); }, sty: K_STY, eo: true },
    { clip: c => { c.beginPath(); c.rect(-9e3, -9e3, 2e4, 2e4); rect(K_FR[2]); }, sty: { ...STY.red, fill: '#F2B25A', cut: PW.ink, line: PW.ink }, eo: true },
  ];
  for (const z of zones) { ctx.save(); z.clip(ctx); ctx.clip(z.eo ? 'evenodd' : 'nonzero'); K_walker(ctx, figX, gy, s, t, { sty: z.sty, lk: z.sty === STY.red ? { ...K_LK, rf: true, earHidden: true } : K_LK }); ctx.restore(); }
  meander(ctx, cx + K_FR[0][0], cx + K_FR[0][2], cy + K_FR[0][3] - 30, 30, C.ink);
  ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.beginPath(); rect(K_FR[0]); ctx.stroke();
  meanderSaltire(ctx, cx + K_FR[1][0], cx + K_FR[1][2], cy + K_FR[1][1], 30, PC.clayR, PC.glaze);
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = 5; ctx.beginPath(); rect(K_FR[1]); ctx.stroke();
  ctx.strokeStyle = PW.line; ctx.lineWidth = 3; ctx.beginPath(); rect(K_FR[2]); ctx.stroke();
}
// ELPİS küpü (P095–P097'nin levhası): kapalı siyah figür küp, dibinde soluk soğuk ışık
function K_pithos(ctx, x, y, s, t, a = 1) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.globalAlpha *= a;
  ctx.fillStyle = C.clay; ctx.fillRect(-120, -170, 240, 300); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.strokeRect(-120, -170, 240, 300);
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-40, -120); ctx.quadraticCurveTo(-90, -60, -70, 40); ctx.quadraticCurveTo(-50, 100, 0, 104); ctx.quadraticCurveTo(50, 100, 70, 40); ctx.quadraticCurveTo(90, -60, 40, -120); ctx.closePath(); ctx.fill();
  ctx.fillRect(-46, -136, 92, 18);
  ctx.strokeStyle = C.clay; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(-74, -10); ctx.lineTo(74, -10); ctx.stroke();
  glow(ctx, 0, 70, 40, `rgba(200,215,235,${.25 + .1 * Math.sin(t * 2)})`);
  dipinto(ctx, 'ΕΛΠΙΣ', 0, 150, 26, { col: C.ink, w: .1 });
  ctx.restore();
}
const K_ST = () => {
  const gy = 820;
  return [
    // önsözün ilk sayfası (v): K01@ilk'te sayfa çevrilir
    { at: PA('P281'), x: 960, draw: (ctx, lt, t) => {
      const tI = A('K01@ilk') - PA('P281'), turn = ramp(lt, tI, tI + .9);
      txt(ctx, 'ÖNSÖZ', 960, 200, { font: '600 64px Cinzel', col: PW.line, ls: 14, a: 1 - turn });
      for (let i = 0; i < 7; i++) scribble(ctx, 480, 300 + i * 58, 960, 1, 80 + i, { col: `rgba(74,52,35,${.6 * (1 - turn)})` });
      txt(ctx, '— v —', 960, 760, { font: 'italic 500 34px "Cormorant Garamond"', col: PW.lineL, a: 1 - turn });
      if (turn > 0 && turn < 1) { // çevrilen yaprak: sağ kenardan sola katlanır
        const w = 980 * Math.cos(turn * PI); ctx.fillStyle = 'rgba(70,45,25,.16)'; ctx.fillRect(470 + 980 - Math.abs(w), 140, Math.abs(w), 700);
        ctx.fillStyle = PW.paperL; ctx.fillRect(470 + (w > 0 ? 0 : 980 + w), 120, Math.abs(w), 700); ctx.strokeStyle = PW.lineL; ctx.lineWidth = 2; ctx.strokeRect(470 + (w > 0 ? 0 : 980 + w), 120, Math.abs(w), 700);
      }
    } },
    // "İnsan nedir?": dört ayak üstünde figür yukarı bakar
    { at: PA('P281b'), x: 2900, draw: (ctx, lt, t) => {
      const t0 = PA('P281b');
      txt(ctx, 'İnsan nedir?', 2900, 300, { font: 'italic 600 92px "Cormorant Garamond"', col: PW.ink, a: ramp(lt, 0, .25) });
      txt(ctx, 'Ne zaman insan olmaya başladı?', 2900, 410, { font: 'italic 500 70px "Cormorant Garamond"', col: PW.ink, a: ramp(t, A('K01@ne#1') - .05, A('K01@ne#1') + .3) });
      marginBand(ctx, 2300, 3500, 520, gy + 8, ramp(lt, 0, 1));
      const s = 4.4, x = 2880;
      figure(ctx, { x, y: gy - 30 * s, s, dir: 1, sty: K_STY, lk: K_LK, seed: 5, p: { torso: 1.25, neck: -.9, head: -.35 + .05 * Math.sin(t * 1.3), shN: 1.4, elN: .1, shF: 1.5, elF: .1, handN: 'open', handF: 'open', breath: .8 * Math.sin(t * 1.8) },
        ik: { hN: [x + 30 * s, gy - 2], hF: [x + 26 * s, gy - 2], fN: [x - 18 * s, gy - 3 * s, -1.2], fF: [x - 22 * s, gy - 3 * s, -1.2] } });
    } },
    // cevap: figür ayağa kalkar (K02); tam sayfa alıntı (üst katmanda)
    { at: PA('P282'), x: 4800, draw: (ctx, lt, t) => {
      const s = 4.4, x = 4780, up = E.io2(ramp(lt, 0, 1.6));
      marginBand(ctx, 4200, 5400, 520, gy + 8, 1);
      figure(ctx, { x, y: gy - 44.5 * s * lerp(.68, 1, up), s, dir: 1, sty: K_STY, lk: K_LK, seed: 5,
        p: { torso: lerp(1.25, -.02, up), neck: lerp(-.9, -.1, up), head: lerp(-.35, -.12, up), shN: lerp(1.4, .2, up), elN: .2, shF: lerp(1.5, -.1, up), elF: .3, breath: .8 * Math.sin(t * 1.8) },
        ik: { fN: [x + 8 * s, gy - 3 * s, 0], fF: [x - 8 * s, gy - 3 * s, 0] } });
    } },
    // iç içe çerçevelerden çıkış: siyah figür → kırmızı figür → sayfa → ateşin altın ışığı; kamera geri çekilir
    { at: PA('P283'), x: 6700, y: 540, z: .62, draw: (ctx, lt, t) => {
      const cx = 6700, cy = 560, tD = A('K02@doğaya'), tI = A('K02@insan#1'), tH = A('K02@her');
      const keys = [[PA('P283') - .3, cx - 120], [tD, cx + K_FR[0][2]], [tI, cx + K_FR[1][2]], [tH, cx + K_FR[2][2]], [tH + 3, cx + K_FR[2][2] + 260]];
      let fx = keys[0][1];
      for (let i = 1; i < keys.length; i++) if (t >= keys[i - 1][0]) fx = lerp(keys[i - 1][1], keys[i][1], clamp((t - keys[i - 1][0]) / (keys[i][0] - keys[i - 1][0])));
      // kamera iç içe çerçevelerden geri çekilir (durağın ölçeği .62; içerik 2,2 → 1)
      const k = lerp(2.2, 1, E.io2(ramp(t, PA('P283') - .3, tH + .8, E.lin)));
      // durak kendi alanında kalır (komşu duraklara taşmasın)
      ctx.save(); ctx.beginPath(); ctx.rect(5850, -2000, 1800, 5000); ctx.clip();
      ctx.translate(cx, cy); ctx.scale(k, k); ctx.translate(-cx, -cy);
      K_frames(ctx, cx, cy, t, fx, cy + 150, 3.4);
      ctx.restore();
    } },
    // gelenek süsleri: çelenk ve takı üstünden atılır, çizgi olarak düşer
    { at: PA('P285'), x: 8600, draw: (ctx, lt, t) => {
      const tA = A('K04@atar') - PA('P285'), x = 8600, s = 4.6, off = ramp(lt, tA - .4, tA + .2);
      marginBand(ctx, 8000, 9200, 400, gy + 8, 1);
      figure(ctx, { x, y: gy - 44.5 * s, s, dir: 1, sty: K_STY, lk: K_LK, seed: 5, p: { torso: -.05, head: -.08, shN: lerp(.2, -2.6, off) * (1 - ramp(lt, tA + .4, tA + 1.2)) + .2, elN: .3, shF: lerp(-.1, -2.4, off) * (1 - ramp(lt, tA + .4, tA + 1.2)), elF: .3, breath: .7 * Math.sin(t * 1.6) }, ik: { fN: [x + 8 * s, gy - 3 * s, 0], fF: [x - 8 * s, gy - 3 * s, 0] } });
      const fall = ramp(lt, tA, tA + 1.4, E.in2);
      // çelenk ve kolye: başın üstünden düşen çizgiler
      ctx.save(); ctx.strokeStyle = PW.red; ctx.lineWidth = 4; ctx.globalAlpha = 1 - ramp(lt, tA + 1.0, tA + 1.6);
      const hy = gy - 44.5 * s * 1.45;
      ctx.beginPath(); ctx.ellipse(x + 10 - fall * 120, hy + fall * 380, 34, 10, fall * 2, 0, TAU); ctx.stroke();
      for (let k = 0; k < 7; k++) { ctx.beginPath(); ctx.arc(x + 20 + fall * (80 + k * 12), hy + 110 + fall * (330 + k * 6), 5, 0, TAU); ctx.stroke(); }
      ctx.restore();
    } },
    // ELPİS küpü gelir; figür küpten döner, elinde ateşle güneşe yürür (umut soluk, ateş altın)
    { at: PA('P286'), x: 10500, draw: (ctx, lt, t) => {
      const tU = A('K04@umuda'), tB = A('K04@bugün'), x0 = 10450;
      const jar = ramp(t, tU - .4, tU + .4, E.out3);
      K_pithos(ctx, lerp(9700, 10050, jar), 560, 1.15, t, jar);
      sunDisk(ctx, 11300, 360, 120, ramp(t, tB - .3, tB + .6));
      const walk = ramp(t, tB, tB + 6, E.lin), fx = x0 + walk * 520;
      K_walker(ctx, fx, gy, 4.2, t, { dir: t > tB - .1 ? 1 : -1, dist: walk > 0 ? fx : x0, stand: walk > 0 ? 0 : 1, hold: { N: HOLD.torch() } });
      marginBand(ctx, 9500, 11600, 300, gy + 8, 1);
    } },
    // çaba ve cefa: taşıyan ve kuran figürlerden bir friz; küçük figür ateşi taşımayı sürdürür
    { at: PA('P287'), x: 12400, draw: (ctx, lt, t) => {
      marginBand(ctx, 11600, 13200, 360, gy + 8, 1);
      const sp = 60;
      // friz figürleri sonraki durağa (P288a) taşmasın: kapağa geçilirken söner
      const fo = 1 - ramp(t, PA('P288a') - .7, PA('P288a') + .2); ctx.save(); ctx.globalAlpha *= fo;
      if (fo > 0) { [[11800, HOLD.bag()], [12050, HOLD.hydria()], [12550, HOLD.bag()], [12800, HOLD.hammer()]].forEach(([x, h], i) => K_walker(ctx, x + lt * sp, gy, 3.6, t + i * .4, { hold: { N: h }, p: { torso: .18 } }));
        K_walker(ctx, 12300 + lt * sp, gy, 3.9, t, { hold: { N: HOLD.torch() } }); }
      ctx.restore();
      // kurulan duvar: taşlar sırayla yerine oturur
      for (let k = 0; k < 6; k++) { const a = ramp(lt, k * .6, k * .6 + .5); if (a > 0) { ctx.save(); ctx.globalAlpha = a; ctx.strokeStyle = PW.line; ctx.lineWidth = 3; ctx.strokeRect(13020 + (k % 3) * 60, gy - 50 - Math.floor(k / 3) * 46 - (1 - a) * 40, 58, 44); ctx.restore(); } }
    } },
    // kapanan kitabın kapağı: küçük figürün ateşi PROMETHEUS harflerini tutuşturur
    { at: PA('P288a'), x: 14300, draw: (ctx, lt, t) => {
      const tP = A('K06@prometeustur') - .9;
      ctx.fillStyle = 'rgba(40,25,15,.25)'; ctx.fillRect(13930, 220, 760, 560); ctx.fillStyle = '#B8693F'; ctx.fillRect(13920, 205, 760, 560); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.strokeRect(13920, 205, 760, 560);
      meanderSaltire(ctx, 13940, 14660, 225, 26, C.ink, '#B8693F');
      const ig = ramp(t, tP, tP + .8);
      txt(ctx, 'PROMETHEUS', 14300, 470, { font: '700 78px Cinzel', col: mixCol(C.ink, PC.fire, ig), ls: 6, shadow: ig > 0 ? 'rgba(255,170,80,.8)' : undefined, blur: 26 * ig, force: true });
      if (ig > 0) motes(ctx, t, 26, 61, 'rgba(255,200,120,.9)', [13980, 360, 640, 160], 40, 1.6, .7 * ig);
      const fx = lerp(13700, 13990, ramp(t, PA('P288a'), tP, E.io2));
      K_walker(ctx, fx, gy + 40, 3.6, t, { dist: fx, stand: ramp(t, tP - .4, tP), hold: { N: HOLD.torch() }, p: t > tP - .4 ? { shN: -1.3, elN: .2 } : {} });
    } },
  ];
};
let K_STATIONS = null;
shot(PA('P281'), (ctx, st) => {
  if (!K_STATIONS) K_STATIONS = K_ST();
  pageJourney(ctx, st.t, K_STATIONS, {});
}, { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => {
    const t = st.t;
    // tam sayfa alıntılar (üst katman, telefon kuralı: y ≤ 700)
    const q1 = A('K02@insan'), q1e = A('K02@doğaya') - .1;
    if (t > q1 - .2 && t < q1e + .6) { ctx.save(); ctx.globalAlpha = 1 - ramp(t, q1e, q1e + .6); quoteCard(ctx, 'İnsan başkaldıran yaratıktır.', 'A. ERHAT · ÖNSÖZ · S. V', 960, 220, 1500, t - q1, { font: 'italic 500 92px "Cormorant Garamond"', lh: 100 }); ctx.restore(); }
    const q2 = A('K04@umuda'), q2e = A('K06');
    if (t > q2 - .2 && t < q2e + .6) { ctx.save(); ctx.globalAlpha = 1 - ramp(t, q2e, q2e + .6); quoteCard(ctx, 'Umuda karşı da ayaklandık.', 'A. ERHAT · ÖNSÖZ · S. VI', 960, 200, 1500, t - q2, { font: 'italic 500 80px "Cormorant Garamond"', lh: 90 }); ctx.restore(); }
    const q3 = A('K06'), q3e = A('K06@ve');
    if (t > q3 && t < q3e + .6) { ctx.save(); ctx.globalAlpha = ramp(t, q3, q3 + .5) * (1 - ramp(t, q3e, q3e + .6)); txt(ctx, 'İNSAN OLMAK', 960, 200, { font: '700 76px Cinzel', col: PW.ink, ls: 10 }); txt(ctx, 'ERHAT · ÖNSÖZ · S. VI', 960, 268, { font: '600 40px Cinzel', col: PW.line, ls: 4 }); ctx.restore(); }
    const q4 = A('K06@bu#2');
    if (t > q4 - .2) quoteCard(ctx, 'Bu ülkünün ilk temsilcisi Prometheus’tur.', 'A. ERHAT · ÖNSÖZ · S. VI', 960, 140, 1600, t - q4, { font: 'italic 500 76px "Cormorant Garamond"', lh: 86 });
  } });

// --- P288b: eşleşen kesme: kapaktaki ateşli harfler açılış başlığının (P011) harflerine geçer; zincirli siluet; tek kıvılcım lambaya iner ---
shot(PA('P288b'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  glazeBG(ctx, t, { gx: 960, gy: 760, gr: 900, stars: false, warm: 'rgba(120,48,22,.4)' });
  vaseStars(ctx, t, 40, 13, [0, 60, W, 500], [], .35);
  const z = lerp(1.25, 1.0, E.io2(clamp(lt / 2.4)));
  ctx.save(); ctx.translate(960, 480); ctx.scale(z, z); ctx.translate(-960, -480);
  ctx.save(); ctx.globalAlpha = (.16 + .04 * Math.sin(t * 1.7)) * ramp(lt, .3, 1.4); ctx.translate(960, 560); ctx.scale(.62, .62); ctx.translate(-1225, -560);
  figure(ctx, { x: 1225, y: 868 - 42.5 * 6.3, s: 6.3, dir: -1, sty: { ...STY.red, fill: '#5A2C18', dilute: '#5A2C18' }, lk: LK.prom, still: true, p: { torso: .12, head: -.1 },
    ik: { hF: [1425, 243], hN: [1410, 568], fN: [1155, 849, 0], fF: [1315, 849, .25] } });
  ctx.restore();
  glow(ctx, 960, 470, 700, 'rgba(255,170,80,.22)');
  txt(ctx, 'PROMETHEUS', 960, 480, { font: '700 138px Cinzel', col: PC.fire, ls: 16, shadow: 'rgba(255,170,80,.8)', blur: 30, force: true });
  motes(ctx, t, 40, 17, 'rgba(255,200,120,.9)', [480, 360, 960, 160], 40, 1.6, .7);
  ctx.restore();
  // sessizlikte tek kıvılcım harflerden ayrılıp aşağı, P289'un lambasına iner
  const sp = ramp(lt, 1.9, st.d, E.io2);
  if (sp > 0) { const x = lerp(1120, 1180, sp), y = lerp(500, 1000, sp); glow(ctx, x, y, 30, 'rgba(255,210,140,.8)'); ctx.fillStyle = PC.fireCore; ctx.beginPath(); ctx.arc(x, y, 4, 0, TAU); ctx.fill(); }
  friezeFrame(ctx, { col: mixCol(PC.clayR, PC.glaze, .3), h: 38, saltire: true, bandBg: PC.glaze, alpha: .9 });
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const q4 = A('K06@bu#2'); ctx.save(); ctx.globalAlpha = 1 - ramp(st.t, Se('K06') + .4, Se('K06') + 1.0); quoteCard(ctx, 'Bu ülkünün ilk temsilcisi Prometheus’tur.', 'A. ERHAT · ÖNSÖZ · S. VI', 960, 140, 1600, st.t - q4, { font: 'italic 500 76px "Cormorant Garamond"', lh: 86 }); ctx.restore(); } });
