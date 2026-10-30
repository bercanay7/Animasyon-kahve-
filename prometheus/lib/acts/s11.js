// XI. HERAKLES'TEN OPPENHEIMER'A (L01–L06): okçu gelir, kartal vurulur (Hesiodos), kayıp oyun, zincirdeki hâliyle hatırlanan Titan:
// çağlar galerisi, Goethe, Frankenstein, American Prometheus, meşale koşusu
'use strict';

// --- yardımcılar (L_ öneki: bütün perdeler aynı global kapsamı paylaşır) ---
// aslan postu: başın üstünde başlık gibi duran profil aslan başı, sırttan sarkan post (siyah sır, kil kazıma)
function L_lionHood(ctx, J, M, s, sty, t) {
  const h = jointPt(ctx, M, J.neckT), d = J.headA || 0;
  ctx.save(); ctx.translate(h[0], h[1]); ctx.scale(s, s);
  ctx.fillStyle = sty === STY.red ? C.ink : C.ink; ctx.strokeStyle = sty === STY.red ? PC.clayR : C.clay; ctx.lineWidth = .45;
  // başlık: alından enseye, üstte yele dişleri
  ctx.beginPath(); ctx.moveTo(4.6, -9.2); ctx.quadraticCurveTo(2.4, -14.8, -3.2, -14.2); ctx.quadraticCurveTo(-7.4, -12.6, -7.6, -7.4);
  ctx.quadraticCurveTo(-9.4, -2, -8.6, 4.5); ctx.lineTo(-6.2, 3.2); ctx.quadraticCurveTo(-5.4, -4.6, -2.4, -8.4); ctx.quadraticCurveTo(1.6, -10.4, 4.6, -9.2); ctx.fill();
  for (let i = 0; i < 6; i++) { const a = -2.8 + i * .32; ctx.beginPath(); ctx.moveTo(-3 + Math.cos(a) * 9, -6 + Math.sin(a) * 8); ctx.lineTo(-3 + Math.cos(a) * 11.4, -6 + Math.sin(a) * 10.2 + Math.sin(t * 2 + i) * .2); ctx.stroke(); }
  // aslanın gözü ve kulak
  ctx.beginPath(); ctx.arc(1.2, -11.2, .55, 0, TAU); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(-2.4, -14.1); ctx.lineTo(-1.2, -16.2); ctx.lineTo(.2, -13.9); ctx.fill();
  ctx.restore();
}
// okçu Herakles: yayı geren kırmızı figür (dir 1, sağa bakar); draw: 0..1 gerginlik, rel: bırakış (0..1 sonrası)
function L_archer(ctx, x, gy, s, t, draw, rel, o = {}) {
  const sty = o.sty || STY.red;
  let J = null, M = null;
  const pull = draw * (1 - E.out3(clamp(rel * 3)));
  figure(ctx, { x, y: gy - 44.5 * s, s, dir: 1, sty, lk: { ...LK.herakles, rf: sty === STY.red, earHidden: true, sevEye: true, cape: true }, seed: 41, stripe: sty === STY.red ? .55 : 0,
    p: { torso: .08, neck: -.02, head: -.04, handN: 'fist', handF: 'fist', breath: .6 * Math.sin(t * 1.6), scowl: .4 },
    ik: { hN: [x + 40 * s, gy - 70 * s], hF: [x + lerp(22, 4, pull) * s, gy - 69.4 * s], fN: [x + 14 * s, gy - 3 * s, 0], fF: [x - 12 * s, gy - 3 * s, .2] },
    onJoints: (j, m) => { J = j; M = m; } });
  const wN = jointPt(ctx, M, J.AN.wr), wF = jointPt(ctx, M, J.AF.wr);
  // yay: tutan elin önünde dik kavis; kiriş çeken ele gider; bırakınca kiriş titrer
  const bh = 24 * s, bow = [wN[0] + 2 * s, wN[1]], bend = lerp(5, 9, pull) * s;
  const top = [bow[0] - bend * .6, bow[1] - bh], bot = [bow[0] - bend * .6, bow[1] + bh];
  ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5 * s; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(top[0], top[1]); ctx.quadraticCurveTo(bow[0] + bend, bow[1], bot[0], bot[1]); ctx.stroke();
  if (sty === STY.red) { ctx.strokeStyle = PC.clayR; ctx.lineWidth = .4 * s; ctx.beginPath(); ctx.moveTo(top[0] - .6 * s, top[1]); ctx.quadraticCurveTo(bow[0] + bend - .9 * s, bow[1], bot[0] - .6 * s, bot[1]); ctx.stroke(); }
  const vib = rel > 0 ? Math.exp(-rel * 9) * Math.sin(rel * 90) * 2.5 * s : 0;
  const nock = pull > .02 ? [wF[0], wF[1]] : [top[0] + vib, (top[1] + bot[1]) / 2];
  ctx.strokeStyle = sty === STY.red ? PC.clayRL : C.clay; ctx.lineWidth = .45 * s;
  ctx.beginPath(); ctx.moveTo(top[0], top[1]); ctx.lineTo(nock[0], nock[1]); ctx.lineTo(bot[0], bot[1]); ctx.stroke();
  L_lionHood(ctx, J, M, s, sty, t);
  return { nock, bow, J, M, wN, wF };
}
function L_arrow(ctx, x, y, a, s, glint = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.strokeStyle = C.ink; ctx.fillStyle = C.ink; ctx.lineWidth = 1.1 * s;
  ctx.beginPath(); ctx.moveTo(-34 * s, 0); ctx.lineTo(0, 0); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(3.2 * s, 0); ctx.lineTo(-1.6 * s, -1.8 * s); ctx.lineTo(-1.6 * s, 1.8 * s); ctx.closePath(); ctx.fill();
  for (const sg of [-1, 1]) { ctx.beginPath(); ctx.moveTo(-34 * s, 0); ctx.lineTo(-29 * s, sg * 2.4 * s); ctx.lineTo(-26 * s, 0); ctx.fill(); }
  ctx.restore();
  if (glint > 0) sparkle(ctx, x + Math.cos(a) * 3 * s, y + Math.sin(a) * 3 * s, 22 * glint, glint, '#FFE2A8');
}

// --- P264: bölüm kartı; okçu oku bırakır ("gerçekten geldi mi?") ---
shot(PA('P264'), (ctx, st) => {
  const t = st.t, lt = st.lt, tR = A('L01@geldi'), rel = Math.max(0, t - tR);
  const c = { x: lerp(980, 1060, E.io2(clamp(lt / st.d))), y: 520, z: lerp(1.0, 1.08, E.io2(clamp(lt / st.d))), sx: noise1(t * .3, 3) * 2, sy: noise1(t * .3, 4) * 1.5 };
  glazeBG(ctx, t, { gx: 900, gy: 760, gr: 1000, stars: false, warm: 'rgba(150,62,28,.42)' });
  ctx.save(); cam(ctx, c, .1); vaseStars(ctx, t, 30, 51, [0, 60, W, 520], [], .35); ctx.restore();
  ctx.save(); cam(ctx, c, .4); windLines(ctx, t, .45); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  const gy = 870;
  // meander şeridi (P209–P210 ile aynı zemin): okçunun bastığı bordür
  meanderSaltire(ctx, -400, 2600, gy, 34, mixCol(PC.clayR, PC.glaze, .25), PC.glaze);
  const draw = ramp(lt, .2, Math.max(.6, tR - st.at - .2), E.io2);
  const A1 = L_archer(ctx, 560, gy, 7.2, t, draw, rel);
  // ok: bırakılınca sağa uçar; bırakılmadan ucunda parıltı (önceki kıvılcımla eşleşir)
  const a = -.02;
  if (rel <= 0) L_arrow(ctx, A1.bow[0] + 26, A1.nock[1] - 2, a, 7.2 * .9, Math.max(.35, 1 - ramp(lt, 0, .8)));
  else { const fx = A1.bow[0] + 26 + rel * 2300; L_arrow(ctx, fx, A1.nock[1] - 2 - rel * 40, a - .03, 7.2 * .9, .6); if (rel < .5) { ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(fx - 300, A1.nock[1] - rel * 30); ctx.lineTo(fx - 260, A1.nock[1] - 2 - rel * 40); ctx.stroke(); } }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { chapterCard(ctx, 'BÖLÜM XI', "HERAKLES'TEN OPPENHEIMER'A", st.lt - .15, 3.4, { y: 170 }); } });

// --- P265: açılıştaki Lakonya kylixi: aynı kupada Herakles kartalı vurur (siyah figür, Hesiodos) ---
shot(PA('P265'), (ctx, st) => {
  const t = st.t, lt = st.lt, tK = A('L02@öldürdü'), hit = clamp((t - tK) / .25);
  ctx.fillStyle = '#120B08'; ctx.fillRect(-50, -50, W + 100, H + 100);
  const R = 430, cx = W / 2, cy = H / 2 + 10, z = lerp(1.0, 1.08, E.io2(clamp(lt / st.d)));
  ctx.save(); ctx.translate(cx, cy); ctx.scale(z, z); ctx.translate(-cx, -cy);
  kylix(ctx, t, cx, cy, R, -.18 + lt * .03, (c, t, r) => {
    c.fillStyle = C.ink; c.fillRect(-r, r * .58, 2 * r, 7);
    column(c, 175, r * .58, -r * .52, 34, C.ink, C.clay);
    const s = 4.1, px = 110, gy = r * .58;
    figure(c, { x: px, y: gy - 44.2 * s, s, dir: -1, sty: STY.black, lk: LK.prom, seed: 23,
      p: { torso: -.05, neck: -.1, head: lerp(-.1, -.3, ramp(t, tK, tK + .8)), handN: 'fist', handF: 'fist' },
      ik: { hN: [px + 62, gy - 20 * s], hF: [px + 60, gy - 23 * s], fN: [px - 30, gy - 3 * s, 0], fF: [px + 28, gy - 3 * s, 0] } });
    c.strokeStyle = C.clay; c.lineWidth = 3; for (const yy of [gy - 21 * s, gy - 9 * s]) { c.beginPath(); c.ellipse(175, yy, 22, 6, 0, 0, TAU); c.stroke(); }
    // okçu solda: yayı gerer ve bırakır (bırakış ok saplanmadan önce)
    const rel = Math.max(0, t - (tK - .45));
    const A1 = L_archer(c, -300, gy, 3.6, t, ramp(lt, .3, Math.max(.8, tK - .45 - st.at)), rel, { sty: STY.black });
    // kartal (siyah figür): Prometheus'un göğsüne iner; vurulunca düşer
    const fall = ramp(t, tK, tK + 1.4, E.in2);
    const ex = lerp(-60, 40, ramp(lt, 0, 2)) + fall * 40, ey = lerp(-250, -120, ramp(lt, 0, 2)) + fall * 380;
    eagle2(c, ex, ey, 1.25, -1, { ang: hit > 0 ? lerp(.7, .1, fall) : .5 + .5 * Math.cos(t * 3.4), angFar: .2, col: C.ink, wingCol: C.ink, farCol: '#3A2116', line: C.clay, eye: C.clay, tilt: lerp(.1, 1.4, fall), beak: .1 + .5 * hit * (1 - fall) });
    // ok: yaydan kartala
    if (rel > 0 && hit <= 0) { const k = clamp(rel / .45), fx = lerp(A1.bow[0] + 10, ex - 20, k), fy = lerp(A1.nock[1], ey + 8, k); L_arrow(c, fx, fy, Math.atan2(ey + 8 - A1.nock[1], ex - 20 - A1.bow[0]), 3.4); }
    if (hit > 0) { L_arrow(c, ex - 8, ey + 8 + 0, 1.1 + fall, 3.4); if (t - tK < .6) dustBurst(c, t, tK, ex, ey, 18, 'rgba(201,112,63,.7)', 70, 5); }
  });
  ctx.restore();
}, { tr: { type: 'clay', dur: .6, end: true }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => { const a = ramp(st.lt, .4, 1.0) * (1 - ramp(st.lt, st.d - .6, st.d)); if (a > 0) dipinto(ctx, 'ΗΡΑΚΛΗΣ', 330, 160, 64, { col: C.clay, a, w: .1 }); } });

// --- P266: buluttan Zeus izin verir gibi başını sallar (siyah figür amfora, ikonografik Zeus) ---
shot(PA('P266'), (ctx, st) => {
  const t = st.t, lt = st.lt, n1 = A('L02@zeusun'), n2 = A('L02@oğlunun');
  amphoraFrieze(ctx, t, 700 + lt * 40, (c, x0, x1) => {
    // bulut kütlesi ve üstünde tahtında Zeus; altta küçük Herakles ünüyle (başında çelenk)
    for (let i = 0; i < 5; i++) cloud(c, 420 + i * 140, 700 + (i % 2) * 30, 1.6, C.ink, C.clay, i + 61);
    const nod = Math.exp(-Math.pow((t - n1 - .2) / .25, 2)) + Math.exp(-Math.pow((t - n2 - .2) / .25, 2));
    throne(c, 640, 690, 5.4, 1, C.ink, C.clay, { high: true });
    figure(c, { x: 660, y: 690 - 44.5 * 5.6 + 70, s: 5.6, dir: 1, sty: STY.black, lk: LK.zeus, seed: 5, hold: { N: HOLD.scepter(80), F: HOLD.bolt() },
      p: { torso: -.05, neck: .05 + .25 * nod, head: .05 + .2 * nod, shN: .5, elN: .9, shF: -.2, elF: .6, kneeN: 1.4, kneeF: 1.4, hipN: -1.4, hipF: -1.4 } });
    bf(c, 1080, 820, 3.4, -1, { ...LK.herakles, cape: true }, { torso: .05, head: -.15, shN: -2.4, elN: .3, handN: 'open' });
    const w = ramp(t, n2, n2 + .9);
    if (w > 0) { c.save(); c.globalAlpha = w; c.strokeStyle = C.clay; c.lineWidth = 4; c.beginPath(); c.ellipse(1062, 655, 30, 9, 0, 0, TAU); c.stroke(); c.restore(); }
  });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P267: B02'nin üç papirüsü: "Kurtulmuş Prometheus" toza döner (kırmızı figür, tiyatronun önünde) ---
shot(PA('P267'), (ctx, st) => {
  const t = st.t, lt = st.lt, tK = A('L02@kayıp');
  const c = { x: 960 + lt * 6, y: 520, z: 1.04 + lt * .006 };
  theatre(ctx, t, { x: 960, y: 520, z: .95 }, { crowd: false });
  ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(14,9,7,.55)'; ctx.fillRect(0, 0, W, H); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  const shelf = [960, 560];
  ctx.fillStyle = '#2A170F'; ctx.fillRect(560, shelf[1] + 52, 800, 26); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 2; ctx.strokeRect(560, shelf[1] + 52, 800, 26);
  // sol: B02'de kaybolan oyunların boş yeri (soluk iz); orta: Zincire Vurulmuş (kalır); sağ: Kurtulmuş (L02@kayıp'ta toza döner)
  const scroll = (x, a) => { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#E2D3B5'; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(x, shelf[1], 40, 58, 0, 0, TAU); ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.ellipse(x, shelf[1], 14, 21, 0, 0, TAU); ctx.stroke(); ctx.restore(); };
  ctx.save(); ctx.setLineDash([8, 10]); ctx.strokeStyle = 'rgba(226,211,181,.3)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(700, shelf[1], 40, 58, 0, 0, TAU); ctx.stroke(); ctx.restore();
  scroll(960, 1);
  const dz = ramp(t, tK + .1, tK + 1.5);
  if (dz < 1) scroll(1220, 1 - dz);
  if (t > tK) dustBurst(ctx, t, tK + .1, 1220, shelf[1], 40, 'rgba(226,211,181,.6)', 140, 23);
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tK = A('L02@kayıp');
    txt(ctx, 'Zincire Vurulmuş Prometheus', 960, 360, { font: 'italic 600 46px "Cormorant Garamond"', col: '#F1E4C8', a: ramp(st.lt, .2, .8) });
    txt(ctx, 'Kurtulmuş Prometheus', 1240, 450, { font: 'italic 600 42px "Cormorant Garamond"', col: '#F1E4C8', a: ramp(st.lt, .6, 1.2) * (1 - ramp(t, tK + .2, tK + 1.2)) });
  } });

// --- P268: aynı zincirli duruş çağ çağ (siyah figür, kırmızı figür, beyaz zemin, gravür, modern kontur); galeri kayması ---
const L_ERAS = [
  { ad: 'MÖ VI. yy', bg: C.clay, sty: STY.black, frame: C.ink },
  { ad: 'MÖ V. yy', bg: PC.glaze, sty: STY.red, frame: PC.clayR },
  { ad: 'MÖ V. yy · beyaz zemin', bg: PW.paperL, sty: STY.lek, frame: PW.line },
  { ad: 'XVII. yy · gravür', bg: '#E8DFC9', sty: STY.lek, frame: PW.ink, hatch: true },
  { ad: 'XX. yy', bg: PW.paper, sty: { ...STY.lek, fill: PW.paper, cut: PW.ink, line: PW.ink }, frame: PW.red, modern: true },
];
function L_boundPose(ctx, x, gy, s, sty, t, lk, o = {}) {
  // promChained ile aynı duruş (zincire karşı asılma), kaya olmadan; zincirler iki kazığa
  const ik = { hF: [x + 200 / 6.3 * s, gy - 625 / 6.3 * s], hN: [x + 185 / 6.3 * s, gy - 300 / 6.3 * s], fN: [x - 95 / 6.3 * s, gy - 3 * s, .05], fF: [x + 124 / 6.3 * s, gy - 3 * s - 20 / 6.3 * s, -.5] };
  let J = null, M = null;
  figure(ctx, { x, y: gy - 42.5 * s, s, dir: -1, sty, lk, seed: 17, stripe: o.stripe || 0, ik, hold: { N: CUFF, F: CUFF },
    p: { ...EXPR.direnc, ...PROM_POSE.direnis, handN: 'fist', handF: 'fist', breath: 1.3 * Math.sin(t * 1.65), torso: PROM_POSE.direnis.torso + .02 * Math.sin(t * .9) }, onJoints: (j, m) => { J = j; M = m; } });
  const wN = jointPt(ctx, M, J.AN.wr), wF = jointPt(ctx, M, J.AF.wr), sF = [x + 210 / 6.3 * s, gy - 700 / 6.3 * s], sN = [x + 225 / 6.3 * s, gy - 180 / 6.3 * s];
  chain(ctx, [wF, sF], 3.4 * s, o.chainCol || sty.line, null, .9 * s, 0, 2.6 * s);
  chain(ctx, [wN, sN], 3.4 * s, o.chainCol || sty.line, null, .9 * s, 0, 2.6 * s);
}
shot(PA('P268'), (ctx, st) => {
  const t = st.t, lt = st.lt, u = E.io2(clamp(lt / st.d));
  const c = { x: lerp(760, 3240, u), y: 540, z: 1 };
  paperBG(ctx, t, { seed: 33 });
  ctx.save(); cam(ctx, c, 1);
  L_ERAS.forEach((e, i) => {
    const x0 = 360 + i * 640, y0 = 210, w = 520, h = 620;
    ctx.fillStyle = 'rgba(70,45,25,.18)'; ctx.fillRect(x0 + 10, y0 + 12, w, h);
    ctx.fillStyle = e.bg; ctx.fillRect(x0, y0, w, h);
    ctx.save(); ctx.beginPath(); ctx.rect(x0, y0, w, h); ctx.clip();
    const s = 4.4, gy = y0 + h - 40;
    L_boundPose(ctx, x0 + 230, gy, s, e.sty, t + i * .7, e.modern ? { ...LK.prom, rf: false, anat: false, modern: true } : e.sty === STY.red ? LK.prom : { ...LK.prom, rf: false }, { stripe: e.sty === STY.red ? .5 : 0 });
    if (e.hatch) { ctx.strokeStyle = 'rgba(43,29,20,.35)'; ctx.lineWidth = 1.2; for (let k = -h; k < w; k += 9) { ctx.beginPath(); ctx.moveTo(x0 + k, y0 + h); ctx.lineTo(x0 + k + h * .55, y0); ctx.stroke(); } }
    ctx.restore();
    ctx.strokeStyle = e.frame; ctx.lineWidth = 6; ctx.strokeRect(x0, y0, w, h);
    txt(ctx, e.ad, x0 + w / 2, y0 - 46, { font: '600 40px Cinzel', col: PW.line, ls: 3 });
  });
  ctx.restore();
}, { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 } });

// --- P269–P271: Goethe'nin şiiri (tek sayfa; duraklar): dizeler el yazısıyla, Titan insan yoğurur, insan kendini biçimlendirir ---
// Goethe, "Prometheus" (1774), kamu malı: ilk ve son kıtadan iki dize
function L_clayMan(ctx, x, gy, s, k, t, o = {}) {
  // kilden insan: k 0 topak, 1 ayakta figür (beyaz zeminde tek kil renkli öğe)
  if (k <= 0) return;
  const lump = 1 - clamp(k * 1.6);
  if (lump > 0) { ctx.fillStyle = PC.clayR; ctx.strokeStyle = PW.line; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x, gy - 18 * s * (1 - lump * .4), 9 * s * (.6 + lump), 18 * s * (1 - lump * .55), 0, 0, TAU); ctx.fill(); ctx.stroke(); }
  if (k > .35) {
    const u = ramp(k, .35, 1);
    ctx.save(); ctx.globalAlpha *= u;
    figure(ctx, { x, y: gy - 44.5 * s * lerp(.7, 1, u), s, dir: o.dir || 1, sty: { ...STY.lek, fill: PC.clayR, cut: PW.ink, line: PW.ink }, lk: { hair: 'nape' }, seed: 9,
      p: { torso: lerp(.5, o.torso ?? 0, u), neck: lerp(.4, 0, u), head: o.head ?? 0, shN: o.shN ?? .2, elN: o.elN ?? .4, shF: -.1, elF: .3, breath: .6 * Math.sin(t * 2), handN: o.handN || 'open' },
      hold: o.hold, ik: { fN: [x + 4 * s, gy - 3 * s, 0], fF: [x - 4 * s, gy - 3 * s, 0] } });
    ctx.restore();
  }
}
const L_ST = () => [
  { at: PA('P269') + .3, x: 960, draw: (ctx, lt, t) => {
    penLine(ctx, 'Bedecke deinen Himmel, Zeus,', 960, 330, ramp(lt, .2, 1.6), { font: 'italic 500 66px "Cormorant Garamond"', col: PW.ink });
    penLine(ctx, 'mit Wolkendunst …', 960, 420, ramp(lt, 1.5, 2.4), { font: 'italic 500 66px "Cormorant Garamond"', col: PW.ink });
    // gökyüzü bulutu: kalemle çizilen bulut ve içinde kıvrılan şimşek (Zeus'a meydan okuma)
    inkPoly(ctx, sampleF(u => [lerp(700, 1220, u), 560 - Math.abs(Math.sin(u * PI * 4)) * 34], 60), ramp(lt, .8, 2.6), { col: PW.line, w: 3 });
    inkPoly(ctx, [[1010, 600], [985, 650], [1010, 650], [980, 720]], ramp(lt, 2.4, 3.0), { col: PW.red, w: 4 });
  } },
  { at: PA('P270'), x: 2900, draw: (ctx, lt, t) => {
    penLine(ctx, 'Hier sitz’ ich, forme Menschen', 2900, 250, ramp(lt, .2, 1.6), { font: 'italic 500 62px "Cormorant Garamond"', col: PW.ink });
    penLine(ctx, 'nach meinem Bilde …', 2900, 330, ramp(lt, 1.4, 2.2), { font: 'italic 500 62px "Cormorant Garamond"', col: PW.ink });
    const gy = 860, kn = ramp(lt, .6, 4.6, E.lin);
    marginBand(ctx, 2300, 3500, 420, gy + 8, ramp(lt, 0, 1));
    // Titan diz çökmüş, elleri kil topağın üstünde; yoğurma ritmi
    const kneel = 5.2, x = 2700;
    figure(ctx, { x, y: gy - 44.5 * kneel + 60, s: kneel, dir: 1, sty: STY.lek, lk: LK.promFree, seed: 19,
      p: { torso: .55 + .04 * Math.sin(t * 3), neck: .35, head: .25, shN: .9 + .08 * Math.sin(t * 3), elN: .7, shF: .8 + .08 * Math.sin(t * 3 + 1), elF: .9, handN: 'open', handF: 'open', breath: .8 * Math.sin(t * 1.6) },
      ik: { fN: [x + 22 * kneel, gy - 3 * kneel, -1.2], fF: [x - 18 * kneel, gy - 3 * kneel, -.4] } });
    L_clayMan(ctx, 3010, gy, 3.6, kn, t, { torso: .1, head: .05 });
  } },
  { at: PA('P271'), x: 4800, draw: (ctx, lt, t) => {
    const gy = 860, x = 4800;
    // insan aracı alır ve kendini biçimlendirir: kendi bedenini yontar gibi; Titan'ın silueti geride söner
    ctx.save(); ctx.globalAlpha = 1 - ramp(lt, .4, 2.0) * .8;
    figure(ctx, { x: 4380, y: gy - 44.5 * 5.2 + 60, s: 5.2, dir: 1, sty: STY.lek, lk: LK.promFree, seed: 19, p: { torso: .2, neck: .1, head: .1, shN: .3, elN: .4 }, ik: { fN: [4380 + 18 * 5.2, gy - 15.6, 0], fF: [4380 - 14 * 5.2, gy - 15.6, 0] } });
    ctx.restore();
    const sc = ramp(lt, .5, 3.5);
    L_clayMan(ctx, x + 120, gy, lerp(3.6, 5.6, E.io2(sc)), 1, t, { torso: .05 + .05 * Math.sin(t * 2.6), head: .2, shN: .9 + .25 * Math.sin(t * 2.6), elN: 1.2, handN: 'fist', hold: HOLD.chisel() });
    marginBand(ctx, 4200, 5400, 420, gy + 8, 1);
  } },
];
let L_STATIONS = null;
shot(PA('P269'), (ctx, st) => {
  if (!L_STATIONS) L_STATIONS = L_ST();
  pageJourney(ctx, st.t, L_STATIONS, { num: 'xi' });
}, { tr: { type: 'cut' }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => {
    const t = st.t;
    erhatTag(ctx, st.lt, 'GOETHE · PROMETHEUS (1774)', { d: A('L04@götenin') - st.at + .2 });
    const q0 = A('L04@erhata');
    if (t > q0 - .2) quoteCard(ctx, 'Asıl yaratıcı, insanın kendisidir.', 'A. ERHAT · ÖNSÖZ · S. XI', 960, 230, 1500, t - q0, { font: 'italic 500 76px "Cormorant Garamond"', lh: 88 });
  } });

// --- P272: Frankenstein'ın başlık sayfası (1818, kamu malı); üstünde şimşek, masadaki kil figürün eli kıpırdar ---
shot(PA('P272'), (ctx, st) => {
  const t = st.t, lt = st.lt, tM = A('L05@modern');
  ctx.save(); cam(ctx, { x: 960, y: lerp(560, 520, E.io2(clamp(lt / st.d))), z: lerp(1.0, 1.06, E.io2(clamp(lt / st.d))) }, 1);
  paperBG(ctx, t, { book: true, seed: 41 });
  const f = Math.exp(-Math.pow((lt - .5) / .06, 2)) + Math.exp(-Math.pow((t - tM) / .06, 2));
  inkPoly(ctx, [[960, 70], [930, 130], [968, 132], [920, 210]], ramp(lt, .3, .7), { col: PW.red, w: 5 });
  if (f > .02) glow(ctx, 950, 140, 160, `rgba(255,250,235,${.6 * f})`);
  txt(ctx, 'FRANKENSTEIN;', 960, 300, { font: '700 92px Cinzel', col: PW.ink, ls: 6, a: ramp(lt, .1, .6) });
  txt(ctx, 'OR,', 960, 380, { font: 'italic 500 48px "Cormorant Garamond"', col: PW.ink, a: ramp(lt, .4, .9) });
  txt(ctx, 'THE MODERN PROMETHEUS.', 960, 450, { font: '700 64px Cinzel', col: mixCol(PW.ink, PW.red, ramp(t, tM, tM + .5)), ls: 3, a: ramp(lt, .6, 1.1) });
  txt(ctx, '1818', 960, 560, { font: '600 46px Cinzel', col: PW.line, ls: 10, a: ramp(lt, .9, 1.4) });
  // masada yatan kil figür: el, şimşekle kıpırdar
  ctx.fillStyle = 'rgba(74,52,35,.25)'; ctx.fillRect(560, 790, 800, 14);
  const tw = Math.exp(-Math.pow((t - tM - .25) / .3, 2));
  figure(ctx, { x: 960, y: 760, s: 2.6, dir: 1, sty: { ...STY.lek, fill: PC.clayR, cut: PW.ink, line: PW.ink }, lk: { hair: 'nape' }, seed: 3, still: true,
    p: { torso: PI / 2 - .05, neck: 0, head: 0, shN: -.3 - .7 * tw, elN: .3 + .9 * tw, shF: .1, elF: .2, handN: 'open' },
    ik: { fN: [960 + 40 * 2.6, 784, PI / 2], fF: [960 + 42 * 2.6, 788, PI / 2] } });
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .35, vig: .55, grain: .045 } });

// --- P273: AMERICAN PROMETHEUS (kitap kapağı, kendi tasarımımız) → L05@nolanın'da meşale; L05@kitaba'da beyaz parlama ---
shot(PA('P273'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('L05@amerikan'), tN = A('L05@nolanın'), tK = A('L05@kitaba');
  if (t < tN) {
    ctx.save(); cam(ctx, { x: 960, y: 540, z: 1 + lt * .01 }, 1);
    paperBG(ctx, t, { seed: 44 });
    // kapak: koyu cilt, ortada küçük bir alev amblemi; yazar adları küçük
    const op = ramp(t, tA - .3, tA + .3);
    ctx.save(); ctx.globalAlpha = op;
    ctx.fillStyle = 'rgba(40,25,15,.3)'; ctx.fillRect(700, 130, 540, 760); ctx.fillStyle = '#2B1D14'; ctx.fillRect(690, 118, 540, 760);
    ctx.strokeStyle = '#B8693F'; ctx.lineWidth = 3; ctx.strokeRect(712, 140, 496, 716);
    txt(ctx, 'AMERICAN', 960, 270, { font: '700 70px Cinzel', col: '#EBDCC0', ls: 8 });
    txt(ctx, 'PROMETHEUS', 960, 350, { font: '700 70px Cinzel', col: '#EBDCC0', ls: 8 });
    flame(ctx, 960, 610, 1.6, t, { haloR: 120 });
    txt(ctx, 'KAI BIRD · MARTIN J. SHERWIN', 960, 790, { font: '600 26px Cinzel', col: '#CDB896', ls: 3 });
    ctx.restore();
    // önce: atom çağı gerçekçi bir patlama olmadan: kalemle çizilmiş çöl ufku, sırtı dönük küçük bir figür, ufukta büyüyen soluk bir ışık noktası
    const pre = 1 - op;
    if (pre > 0) { ctx.save(); ctx.globalAlpha = pre;
      inkPoly(ctx, [[300, 640], [1620, 640]], ramp(lt, 0, .8), { col: PW.line, w: 3 });
      const gl = ramp(t, A('L05@babası'), A('L05@babası') + 1.6);
      glow(ctx, 1240, 630, 60 + 140 * gl, `rgba(255,246,228,${.35 + .4 * gl})`);
      figure(ctx, { x: 820, y: 640 - 44.5 * 3.2 + 2, s: 3.2, dir: 1, sty: STY.lek, lk: { hair: 'nape', garment: 'coat', modern: true }, seed: 8, p: { torso: 0, head: .05 + .04 * gl, breath: .5 * Math.sin(t * 1.4) } });
      txt(ctx, '1945', 960, 760, { font: '600 52px Cinzel', col: PW.line, ls: 12, a: ramp(lt, .3, .9) });
      ctx.restore(); }
    ctx.restore();
  } else {
    // meşale (kırmızı figür şerit): beyaz parlama L05@kitaba'da alevin içinden yayılır ve söner
    const c = { x: 960, y: 540, z: 1.1 - (t - tN) * .01 };
    glazeBG(ctx, t, { gx: 960, gy: 540, gr: 900, stars: false, warm: 'rgba(150,62,28,.45)' });
    ctx.save(); cam(ctx, c, 1);
    meanderSaltire(ctx, -200, 2200, 860, 34, mixCol(PC.clayR, PC.glaze, .25), PC.glaze);
    ctx.fillStyle = C.ink; ctx.strokeStyle = PC.clayR; ctx.lineWidth = 3; ctx.fillRect(948, 470, 24, 380); ctx.strokeRect(948, 470, 24, 380);
    flame(ctx, 960, 470, 3.2, t, { haloR: 160 });
    motes(ctx, t, 30, 71, 'rgba(255,200,120,.9)', [820, 200, 280, 280], 50, 1.8, .7);
    ctx.restore();
    kayaFrame(ctx, t);
    const fl = Math.exp(-Math.max(0, t - tK) * 2.2) * ramp(t, tK - .12, tK);
    if (fl > 0) { ctx.save(); baseT(ctx); ctx.globalAlpha = .85 * fl; ctx.fillStyle = '#FFF8EC'; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  }
}, { tr: { type: 'cut' }, post: { tex: .4, vig: .7, grain: .05 },
  over: (ctx, st) => { const tN = A('L05@nolanın'); if (st.t > tN) erhatTag(ctx, st.t - tN, 'NOLAN · OPPENHEIMER (2023)', { bg: 'rgba(238,229,209,.9)' }); } });

// --- P274: bayrak koşusu: tek koşucu silueti hep aynı, zemin bordürü çağ çağ değişir; L06@el'de el alevin önünde durur ---
shot(PA('P274'), (ctx, st) => {
  const t = st.t, lt = st.lt, tE = A('L06@el'), stop = ramp(t, tE - .5, tE + .2);
  clayBG(ctx, C.clayL, C.clayD);
  const gy = 760, BORD = 6, seg = Math.min(BORD - 1, Math.floor(lt / (st.d / BORD)));
  // koşucu ekranda sabit, dünya akar; durunca dünya da yavaşlar
  const run = lt * 420 * (1 - stop * .85);
  const ground = FLAT(gy);
  ctx.save();
  // bordür: çağ çağ değişir (meander, dalga, yumurta-ok, zikzak, düz çizgi, modern şerit)
  const col = C.ink;
  ctx.save(); ctx.translate(-run % 400, 0);
  if (seg === 0) meander(ctx, -400, W + 800, gy + 8, 46, col);
  else if (seg === 1) runningWave(ctx, -400, W + 800, gy + 8, 46, col, 0, C.clay);
  else if (seg === 2) { for (let x = -400; x < W + 800; x += 46) { ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(x, gy + 31, 14, 18, 0, 0, TAU); ctx.fill(); ctx.fillRect(x + 21, gy + 14, 4, 34); } }
  else if (seg === 3) { ctx.strokeStyle = col; ctx.lineWidth = 6; ctx.beginPath(); for (let x = -400; x < W + 800; x += 40) { ctx.lineTo(x, gy + 14); ctx.lineTo(x + 20, gy + 48); } ctx.stroke(); }
  else { ctx.fillStyle = col; ctx.fillRect(-400, gy + 10, W + 1200, seg === 4 ? 10 : 4); }
  ctx.restore();
  ctx.fillStyle = col; ctx.fillRect(0, gy, W, 8);
  // alev hedefi: sağda, son bölümde yaklaşır
  const fx = lerp(2300, 1420, ramp(lt, st.d * .6, tE - st.at));
  ctx.fillStyle = C.ink; ctx.fillRect(fx - 10, gy - 260, 20, 260);
  flame(ctx, fx, gy - 260, 1.7, t, { haloR: 130 });
  const modern = seg >= 4;
  const J = walkScene(ctx, null, 820 + run * 0, 5.6, t, 1, { noCam: true, ground, stride: 56, lean: .22 * (1 - stop), dist: run, stand: stop, sty: modern ? STY.white : STY.black,
    lk: modern ? { hair: 'nape', garment: 'coat', modern: true } : { hair: 'nape', beard: 'short', garment: 'short' },
    hold: { N: HOLD.torch() }, p: stop > 0 ? { shN: lerp(0, -1.5, stop), elN: lerp(.3, .1, stop), handN: 'open' } : {} });
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'clay', dur: .6, end: true }, post: { tex: .85, vig: .85, grain: .055 } });
