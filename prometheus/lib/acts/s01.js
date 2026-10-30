// I. ERHAT'IN SORUSU (B01–B07): tiyatro, tek kalan oyun, Erhat'ın okuması (tek sürekli sayfa), büyük soru, taht kavgasına dönüş
'use strict';

// --- Atina'da Dionysos tiyatrosu (kırmızı figür): oturma basamakları, orkestra, skene ve tanrı maskeleri ---
function tragicMask(ctx, x, y, s, o = {}) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = o.col || PC.clayR; ctx.strokeStyle = C.ink; ctx.lineWidth = 3 / s;
  ctx.beginPath(); ctx.ellipse(0, 0, 40, 52, 0, 0, TAU); ctx.fill(); ctx.stroke();
  // saç ve sakal (siyah sır), göz delikleri, açık ağız
  ctx.fillStyle = C.ink;
  ctx.beginPath(); ctx.ellipse(0, -40, 44, 20, 0, PI, TAU); ctx.fill();
  if (o.beard) { ctx.beginPath(); ctx.moveTo(-30, 22); ctx.quadraticCurveTo(0, 80, 30, 22); ctx.quadraticCurveTo(0, 40, -30, 22); ctx.fill(); }
  for (const sx of [-15, 15]) { ctx.beginPath(); ctx.ellipse(sx, -8, 8, 5, sx > 0 ? .25 : -.25, 0, TAU); ctx.fill(); }
  ctx.beginPath(); ctx.ellipse(0, 22, 11, 8, 0, 0, TAU); ctx.fill();
  ctx.strokeStyle = C.ink; ctx.lineWidth = 2.4 / s; ctx.beginPath(); ctx.moveTo(-26, -22); ctx.quadraticCurveTo(-14, -28, -4, -20); ctx.moveTo(26, -22); ctx.quadraticCurveTo(14, -28, 4, -20); ctx.stroke();
  ctx.restore();
}
function theatre(ctx, t, c, o = {}) {
  const day = o.day || 0;
  glazeBG(ctx, t, { gx: 960, gy: 520, gr: 1200, stars: false, warm: day ? 'rgba(170,80,36,.6)' : 'rgba(130,52,24,.55)' });
  ctx.save(); cam(ctx, c, .1); vaseStars(ctx, t, day ? 0 : 40, 19, [0, 40, W, 300], [], .35); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  const ox = 960, oy = 800;
  // oturma basamakları: orkestranın çevresinde yarım elipsler, sıra sıra seyirci başları
  for (let k = 9; k >= 0; k--) {
    const rx = 330 + k * 70, ry = 92 + k * 22;
    ctx.fillStyle = k % 2 ? '#2A170F' : '#341C12'; ctx.beginPath(); ctx.ellipse(ox, oy, rx, ry, 0, PI, TAU); ctx.lineTo(ox + rx, oy + 40); ctx.lineTo(ox - rx, oy + 40); ctx.fill();
    ctx.strokeStyle = 'rgba(201,112,63,.45)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(ox, oy, rx, ry, 0, PI, TAU); ctx.stroke();
    if (o.crowd !== false) {
      const n = 22 + k * 5, r = rng(k + 3);
      for (let i = 0; i < n; i++) {
        const a = PI + (i + .5) / n * PI, x = ox + Math.cos(a) * (rx - 30), y = oy + Math.sin(a) * (ry - 8) - 4 + Math.sin(t * 2 + i + k) * .8;
        if (Math.abs(x - ox) < 300 && y > oy - 140) continue;
        ctx.fillStyle = r() < .5 ? PC.clayR : '#B86438'; ctx.beginPath(); ctx.arc(x, y, 6 + k * .4, 0, TAU); ctx.fill();
      }
    }
  }
  // skene: sahne binası, kapılar, üstünde tanrı maskeleri
  ctx.fillStyle = '#1C100B'; ctx.fillRect(640, 560, 640, 150); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 3; ctx.strokeRect(640, 560, 640, 150);
  for (const dx of [700, 900, 1100]) { ctx.strokeRect(dx + 20, 600, 80, 110); }
  meanderSaltire(ctx, 640, 1280, 540, 22, mixCol(PC.clayR, PC.glaze, .2), '#1C100B');
  (o.masks || [[740, 470, 1, true], [960, 455, 1.1, true], [1180, 470, 1, false]]).forEach(([x, y, s, b], i) => tragicMask(ctx, x, y + Math.sin(t * .8 + i) * 2, s, { beard: b }));
  // orkestra ve sunak (thymele)
  ctx.fillStyle = '#5A311D'; ctx.beginPath(); ctx.ellipse(ox, oy, 280, 70, 0, 0, TAU); ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3.5; ctx.stroke();
  altar(ctx, ox, oy + 6, 1.2, C.ink, PC.clayR, 1, t);
  // meşaleler
  for (const [x, y] of [[560, 690], [1360, 690]]) { ctx.fillStyle = C.ink; ctx.fillRect(x - 5, y, 10, 90); flame(ctx, x, y, .7, t + x, { haloR: 120 }); }
  ctx.restore();
}
shot(PA('P016'), (ctx, st) => {
  const u = E.io2(clamp(st.lt / (st.d + .5)));
  theatre(ctx, st.t, { x: 960, y: lerp(380, 600, u), z: lerp(.82, 1.45, u) });
  // eşleşen kesme: P015'in yükselen kıvılcımı akşam yıldızı olur (gökte kalır, kamera inerken yavaşça yukarı kayar)
  { const sy = 140 - 200 * u, a = 1 - ramp(st.lt, 4, 6); if (a > 0) { glow(ctx, 1350, sy, 46, `rgba(255,214,150,${.5 * a})`); sparkle(ctx, 1350, sy, 22, a, '#FFE9C4'); } }
  kayaFrame(ctx, st.t);
  chapterCard(ctx, 'BÖLÜM I', "ERHAT'IN SORUSU", st.lt - .3, 3.4, { y: 170 });
}, { tr: { type: 'clay', dur: .8 }, post: { tex: .55, vig: 1, grain: .06 } });

// --- B02: Aiskhylos (stilize kırmızı figür) papirüsünü açar; üç oyundan ikisi toza döner, biri kalır ---
const AISKH = { beard: 'full', hair: 'nape', rf: true, earHidden: true, sevEye: true, garment: 'robe', himation: true, old: false };
shot(A('B02'), (ctx, st) => {
  const t = st.t, lt = st.lt, tT = A('B02@tek');
  const c = { x: 960 + lt * 5, y: 560, z: 1.05 };
  glazeBG(ctx, t, { gx: 760, gy: 700, gr: 900, stars: false, warm: 'rgba(140,58,26,.55)' });
  ctx.save(); cam(ctx, c, 1);
  const open = ramp(lt, .3, 1.8);
  let J = null, M = null;
  figure(ctx, { x: 700, y: 900 - 44.5 * 6, s: 6, dir: 1, sty: STY.red, lk: AISKH, stripe: .55, seed: 31,
    p: { torso: .04, neck: .12, head: .12, shN: 1.0, elN: .9 - .2 * open, shF: .9, elF: 1.2 - .3 * open, handN: 'fist', handF: 'fist' },
    onJoints: (j, m) => { J = j; M = m; } });
  const wN = jointPt(ctx, M, J.AN.wr), wF = jointPt(ctx, M, J.AF.wr);
  // papirüs: iki rulonun arasında açılan krem şerit, üstünde satır izleri
  const a = [Math.min(wN[0], wF[0]), (wN[1] + wF[1]) / 2], b = [a[0] + 80 + 260 * open, a[1] - 10];
  ctx.fillStyle = '#E9DCBE'; ctx.strokeStyle = C.ink; ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.moveTo(a[0], a[1] - 48); ctx.lineTo(b[0], b[1] - 48); ctx.lineTo(b[0], b[1] + 48); ctx.lineTo(a[0], a[1] + 48); ctx.closePath(); ctx.fill(); ctx.stroke();
  for (let i = 0; i < 6; i++) scribble(ctx, a[0] + 14, a[1] - 34 + i * 14, Math.max(0, b[0] - a[0] - 28), 1, 70 + i, { col: 'rgba(40,25,15,.5)', w: 1.4 });
  for (const q of [a, b]) { ctx.fillStyle = PC.clayRL; ctx.beginPath(); ctx.ellipse(q[0], q[1], 14, 56, 0, 0, TAU); ctx.fill(); ctx.stroke(); }
  dipinto(ctx, 'ΑΙΣΧΥΛΟΣ', 700, 300, 30, { col: '#9C3A24', w: .1 });
  // üç papirüs: ikisi toza döner
  const shelf = [1300, 760];
  ctx.fillStyle = '#2A170F'; ctx.fillRect(1180, shelf[1] + 40, 520, 24); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 2; ctx.strokeRect(1180, shelf[1] + 40, 520, 24);
  [[1270, 0], [1440, 1], [1610, 2]].forEach(([x, i]) => {
    const dz = i === 1 ? 0 : ramp(t, tT + .1 + i * .25, tT + 1.2 + i * .25);
    if (dz < 1) { ctx.save(); ctx.globalAlpha = 1 - dz; ctx.fillStyle = '#E2D3B5'; ctx.strokeStyle = C.ink; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.ellipse(x, shelf[1], 26, 38, 0, 0, TAU); ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.ellipse(x, shelf[1], 9, 14, 0, 0, TAU); ctx.stroke(); ctx.restore(); }
    if (dz > 0 && dz < 1) dustBurst(ctx, t, tT + .1 + i * .25, x, shelf[1], 26, 'rgba(226,211,181,.55)', 90, 11 + i);
  });
  const kl = ramp(t, tT + 1.4, tT + 2.0);
  if (kl > 0) txt(ctx, 'Zincire Vurulmuş Prometheus', 1440, 650, { font: 'italic 600 40px "Cormorant Garamond"', col: '#F1E4C8', a: kl });
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- B04–B06: Erhat'ın okuması tek sürekli sayfada; kamera duraklar arasında kayar ---
const B_ST = () => [
  // maske insan yüzüne döner: "oynanan dram, insanlığın dramıdır"
  { at: A('B04') - .1, x: 960, draw: (ctx, lt, t) => {
    const m = ramp(lt, 1.2, 2.6);
    ctx.save(); ctx.globalAlpha = 1 - m; tragicMask(ctx, 960, 420, 3.2, { col: PW.paperL, beard: true }); ctx.restore();
    ctx.save(); ctx.globalAlpha = m;
    figure(ctx, { x: 980, y: 760 - 44.5 * 7.5 + 120, s: 7.5, dir: 1, sty: STY.lek, lk: { hair: 'nape', beard: 'short' }, p: { torso: 0, head: .05 }, margin: 60 });
    ctx.restore();
    penLine(ctx, 'insanlığın dramı', 960, 830, ramp(lt, 2.4, 3.6), { font: 'italic 600 54px "Cormorant Garamond"', col: PW.ink });
  } },
  // "insan dostu, tanrı düşmanı": figür insanla tanrı arasında, insana döner
  { at: A('B05'), x: 2900, draw: (ctx, lt, t) => {
    quoteCard(ctx, 'İnsan dostu, tanrı düşmanı', 'A. ERHAT · ÖNSÖZ · S. V', 2900, 230, 1300, lt - .2);
    const y1 = 780, turn = ramp(lt, 2.0, 2.8);
    marginBand(ctx, 2200, 3600, 360, y1, ramp(lt, 0, 1.2));
    figure(ctx, { x: 2500, y: y1 - 14 - 44.5 * 3.4, s: 3.4, dir: 1, sty: STY.lek, lk: { hair: 'nape' }, p: { torso: .05 } });
    figure(ctx, { x: 2900, y: y1 - 14 - 44.5 * 4, s: 4, dir: turn > .5 ? -1 : 1, sty: STY.lek, lk: LK.promFree, p: { torso: -.05, shN: -.3 - turn * .4, elN: .6 } });
    figure(ctx, { x: 3300, y: y1 - 14 - 44.5 * 4.2, s: 4.2, dir: -1, sty: STY.lek, lk: LK.zeus, p: { torso: .05 } });
  } },
  // XX. yüzyıl: meander zaman şeridi boyunca yürüyen figür
  { at: A('B05@yirminci'), x: 4800, draw: (ctx, lt, t) => {
    const y = 640; meander(ctx, 3900, 5700, y, 46, PW.line, null);
    const k = ramp(lt, 0, 3.2, E.lin), fx = lerp(4100, 5450, k);
    walkScene(ctx, null, fx, 3.2, t, 1, { noCam: true, ground: FLAT(y - 2), sty: STY.lek, lk: { hair: 'nape', beard: 'short' } });
    txt(ctx, 'MÖ V. yy', 4100, 740, { font: '600 40px Cinzel', col: PW.line, ls: 4 });
    txt(ctx, 'XX. yy', 5450, 740, { font: '600 40px Cinzel', col: PW.red, ls: 4, a: ramp(lt, 1.6, 2.4) });
  } },
  // büyük soru: solda kırmızı figür levha (Aiskhylos yazar), sağda beyaz zeminde ayağa kalkan figür; çizgi yüzyılları aşar
  { at: A('B06'), x: 6700, draw: (ctx, lt, t) => {
    ctx.save(); ctx.translate(6080, 470);
    ctx.fillStyle = PC.glaze; ctx.fillRect(-300, -260, 600, 520); ctx.strokeStyle = PW.line; ctx.lineWidth = 6; ctx.strokeRect(-300, -260, 600, 520);
    ctx.save(); ctx.beginPath(); ctx.rect(-300, -260, 600, 520); ctx.clip();
    figure(ctx, { x: -60, y: 240 - 44.5 * 5, s: 5, dir: 1, sty: STY.red, lk: AISKH, p: { torso: .3, neck: .25, head: .2, shN: 1.2, elN: 1.1, handN: 'fist' }, stripe: .5 });
    flame(ctx, 200, 120, .6, t, { haloR: 90 });
    ctx.restore(); ctx.restore();
    const k = ramp(lt, 1.2, 4.0, E.lin);
    inkPoly(ctx, sampleF(u => [lerp(6400, 7100, u), 470 + Math.sin(u * PI * 3) * 40], 60), k, { col: PW.red, w: 4 });
    const up = ramp(lt, 3.6, 5.0);
    figure(ctx, { x: 7350, y: 760 - 44.5 * 5 * lerp(.82, 1, up), s: 5, dir: -1, sty: STY.lek, lk: { hair: 'nape', beard: 'short' },
      p: { torso: lerp(.5, 0, up), neck: lerp(.4, -.05, up), head: lerp(.3, -.1, up) }, ik: { fN: [7330, 757, 0], fF: [7400, 757, 0] } });
    txt(ctx, 'MÖ V. yy', 6080, 790, { font: '600 36px Cinzel', col: PW.line, ls: 4 });
    txt(ctx, 'XX. yy', 7350, 820, { font: '600 36px Cinzel', col: PW.red, ls: 4 });
  } },
  { at: A('B06@yaratabildi') + .2, x: 8600, draw: (ctx, lt, t) => {
    const k = ramp(lt, 0, .8);
    txt(ctx, 'NASIL?', 8600, 470, { font: '900 220px Cinzel', col: mixCol(PW.paperD, PW.red, k), ls: 10, a: k, force: true });
    circleMark(ctx, 8600, 470, 480, 170, ramp(lt, .6, 1.6));
  } },
];
let B_STATIONS = null;
shot(A('B04') - .1, (ctx, st) => {
  if (!B_STATIONS) B_STATIONS = B_ST();
  pageJourney(ctx, st.t, B_STATIONS, { num: 'v' });
}, { tr: { type: 'ink', dur: .8 }, post: { tex: .35, vig: .55, grain: .045 } });

// --- B07: önce çok daha geriye: sayfalar geri çevrilir, kil levhada üç taht (siyah figür) belirir ---
shot(A('B07@taht') - .6, (ctx, st) => {
  const t = st.t, lt = st.lt;
  clayBG(ctx, C.clayL, C.clayD);
  const z = lerp(1.15, 1, E.io2(clamp(lt / 1.6)));
  ctx.save(); ctx.translate(960, 600); ctx.scale(z, z); ctx.translate(-960, -600);
  ctx.fillStyle = C.ink; ctx.fillRect(0, 760, W, 8);
  [[560, 0], [960, 1], [1360, 2]].forEach(([x, i]) => { const k = ramp(lt, .2 + i * .35, .8 + i * .35); ctx.save(); ctx.globalAlpha = k; throne(ctx, x, 760, 6.2, 1, C.ink, C.clay, { high: true }); ctx.restore(); });
  ['ΟΥΡΑΝΟΣ', 'ΚΡΟΝΟΣ', 'ΖΕΥΣ'].forEach((n, i) => dipinto(ctx, n, [560, 960, 1360][i] + 20, 830, 30, { col: C.ink, a: ramp(lt, .6 + i * .35, 1.2 + i * .35) }));
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'clay', dur: 1.0 }, post: { tex: .85, vig: .85, grain: .055 } });
