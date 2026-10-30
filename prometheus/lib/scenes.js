// Deneme sahneleri (?scene=...): üslup karesi ve çizim ilkelleri
'use strict';
const SCENES = {};
// Üslup karesi: dünyanın ucunda zincirli Prometheus, inen kartal, aşağıda insanların ateşleri
SCENES.style = (ctx, t) => {
  glazeBG(ctx, t, { gx: 480, gy: 1020, gr: 1000 });
  // uzak ova ve ufuk
  ctx.fillStyle = '#140B07'; ctx.beginPath(); ctx.moveTo(0, 905); for (let x = 0; x <= 1100; x += 20) ctx.lineTo(x, 890 + fbm1(x * .004, 3) * 26); ctx.lineTo(1100, 1080); ctx.lineTo(0, 1080); ctx.fill();
  ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 2; ctx.beginPath(); for (let x = 0; x <= 1100; x += 20) { const y = 890 + fbm1(x * .004, 3) * 26; x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
  humanFires(ctx, t, [[150, 935, 1.1], [270, 952, .8], [395, 928, 1], [530, 962, 1.2], [660, 941, .8], [790, 966, 1]], 1);
  // kayalık: koyu kütle, ayrılmış (kil) kontur
  const R = [[880, 1080], [930, 940], [1010, 860], [1060, 720], [1030, 590], [1100, 470], [1170, 330], [1260, 230], [1380, 170], [1520, 150], [1720, 175], [1920, 120], [1920, 1080]];
  crag(ctx, R, { seed: 7, fill: '#2A170F', line: PC.clayR, strataCol: 'rgba(201,112,63,.42)' });
  const gy = 868;
  crag(ctx, [[1010, 1080], [1030, 880], [1140, gy], [1330, gy + 6], [1440, 910], [1470, 1080]], { seed: 9, fill: '#3A2116', line: PC.clayR, strataCol: 'rgba(201,112,63,.38)', strata: 5 });
  // zincir kazıkları (kayada, başın arkasında yukarıda)
  const sN = [1470, 600], sF = [1450, 230];
  const s = 6.3, px = 1255;
  let J = null, M = null;
  figure(ctx, {
    x: px, y: gy - 44.5 * s, s, dir: -1, sty: STY.red, lk: LK.prom,
    p: { torso: -.1, neck: -.3, head: -.38, handN: 'fist', handF: 'fist', brow: -1.2, mouthOpen: .7 },
    ik: { hN: [px + 120, gy - 300], hF: [px + 110, gy - 575], fN: [px - 40, gy - 3 * s, 0], fF: [px + 70, gy - 3 * s, .1] },
    onJoints: (j, m) => { J = j; M = m; },
  });
  const wN = jointPt(ctx, M, J.AN.wr), wF = jointPt(ctx, M, J.AF.wr);
  chain(ctx, [wF, sF], 20, PC.clayR, null, 4.5);
  chain(ctx, [wN, sN], 20, PC.clayR, null, 4.5);
  stake(ctx, sN[0], sN[1], 2.4, 0, PC.clayR); stake(ctx, sF[0], sF[1], 2.4, 0, PC.clayR);
  // kartal
  const fl = (t * .55) % 1, glide = .5 + .5 * Math.cos(fl * TAU);
  // süzülüp dalış: kanat yukarıda uzun süre kalır, kısa bir vuruşla iner (yavaş, tehditkâr ritim)
  eagle2(ctx, 700 + Math.sin(t * .7) * 14, 420 + Math.sin(t * 1.1) * 10, 3.1, 1, { ang: lerp(.35, 1, Math.pow(glide, .5)), talon: .95, beak: .5 + .3 * Math.sin(t * 2.3), tilt: .3 + Math.sin(t * .7) * .03 });
  friezeFrame(ctx, { col: PC.clayR, h: 46 });
};
// Poz ızgarası: zincirli Prometheus duruş denemeleri
SCENES.poses = (ctx, t) => {
  ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
  const V = [
    { T: -.22, nk: -.25, hd: -.35, hN: [60, -330], hF: [110, -300], fN: [40, 0], fF: [-150, 0], y: -40 },
    { T: -.12, nk: -.3, hd: -.4, hN: [90, -360], hF: [140, -330], fN: [70, 0], fF: [-80, 0], y: -44 },
    { T: -.3, nk: -.1, hd: -.2, hN: [150, -250], hF: [190, -200], fN: [120, 0], fF: [-110, 0], y: -26 },
    { T: .1, nk: -.3, hd: -.5, hN: [110, -150], hF: [140, -120], fN: [90, 0], fF: [-140, 0], y: -26 },
  ];
  V.forEach((v, i) => {
    ctx.save(); ctx.translate((i % 2) * W / 2, Math.floor(i / 2) * H / 2); ctx.scale(.5, .5);
    const gx = 900, gy = 980, s = 6.4;
    ctx.fillStyle = '#2a1a12'; ctx.fillRect(gx + 120, 0, 700, H * 2);
    figure(ctx, { x: gx, y: gy + v.y * s, s, dir: -1, sty: STY.red, lk: LK.prom,
      p: { torso: v.T, neck: v.nk, head: v.hd, handN: 'fist', handF: 'fist', brow: -.8 },
      ik: { hN: [gx + v.hN[0], gy + v.hN[1] + v.y * s], hF: [gx + v.hF[0], gy + v.hF[1] + v.y * s], fN: [gx + v.fN[0], gy - 3 * s, 0], fF: [gx + v.fF[0], gy - 3 * s, 0] } });
    ctx.fillStyle = PC.clayR; ctx.fillRect(0, gy, W, 6);
    ctx.restore();
  });
};
SCENES.eagles = (ctx, t) => {
  ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
  [0, .25, .5, .75].forEach((f, i) => eagle2(ctx, 260 + i * 460, 380, 2.0, 1, { flap: f, talon: i / 3, beak: i % 2 }));
  [0, .5].forEach((f, i) => eagle2(ctx, 500 + i * 900, 860, 2.4, 1, { ang: f, talon: 1, beak: .7, tilt: .3, col: C.ink, line: PC.clayR }));
};
// Beyaz zemin denemesi: yaşayan sayfa (alıntı kartı, kenar şeridinde figürler, daire, üstü çizme, mühür)
SCENES.sayfa = (ctx, t) => {
  const c = { x: W / 2 + t * 6, y: H / 2, z: 1.02 + t * .004 };
  ctx.save(); cam(ctx, c, 1);
  paperBG(ctx, t, { book: true, num: 'v' });
  quoteCard(ctx, 'İnsan dostu, tanrı düşmanı', 'A. ERHAT · ÖNSÖZ · S. V', W / 2, 250, 1300, t - .3);
  // kenar şeridi: solda insan, ortada Prometheus, sağda tanrı
  const y0 = 470, y1 = 760;
  marginBand(ctx, 260, 1660, y0, y1, ramp(t, .2, 1.6));
  const a = ramp(t, 1.0, 1.8);
  ctx.save(); ctx.globalAlpha = a;
  const turn = ramp(t, 3.2, 4.0);
  figure(ctx, { x: 560, y: y1 - 14 - 44.5 * 3.4, s: 3.4, dir: 1, sty: STY.lek, lk: {}, p: { torso: .05, neck: .1, head: .1 } });
  figure(ctx, { x: 960, y: y1 - 14 - 44.5 * 4, s: 4, dir: turn > .5 ? -1 : 1, sty: STY.lek, lk: LK.prom, p: { torso: -.05, shN: -.4 - turn * .3, elN: .6 } });
  figure(ctx, { x: 1380, y: y1 - 14 - 44.5 * 4.2, s: 4.2, dir: -1, sty: STY.lek, lk: LK.zeus, p: { torso: .05 } });
  ctx.restore();
  circleMark(ctx, 960, y1 - 100 - 40, 110, 140, ramp(t, 4.2, 5.0));
  penLine(ctx, 'insan', 560, 820, ramp(t, 1.8, 2.3), { font: 'italic 600 40px "Cormorant Garamond"', col: PW.line });
  penLine(ctx, 'tanrı', 1380, 820, ramp(t, 2.0, 2.5), { font: 'italic 600 40px "Cormorant Garamond"', col: PW.line });
  strike(ctx, 1320, 822, 1440, 816, ramp(t, 5.0, 5.4));
  stamp(ctx, 'POLİS', 1600, 300, t - 5.6);
  ctx.restore();
};
// Siyah figür denemesi: dönen amfora frizi (Gaia, Uranos, Kronos ve tırpan)
SCENES.amfora = (ctx, t) => {
  const rot = 400 + t * 120;
  amphoraFrieze(ctx, t, rot, (c, x0, x1, t) => {
    const by = 600;  // bant içi zemin çizgisi
    c.fillStyle = C.ink; c.fillRect(x0, by, x1 - x0, 6);
    // Gaia (yatan), Uranos (kemer), Kronos (tırpanla)
    figure(c, { x: 300, y: by - 44.5 * 5, s: 5, dir: 1, sty: STY.black, lk: { fem: true, hair: 'long', robe: true }, p: { torso: .1 } });
    figure(c, { x: 900, y: by - 44.5 * 5.4, s: 5.4, dir: -1, sty: STY.black, lk: LK.zeus, p: { shN: -1.2, elN: .4 } });
    figure(c, { x: 1500, y: by - 44.5 * 4.6, s: 4.6, dir: 1, sty: STY.black, lk: { beard: 'short' }, p: { shN: -2.2, elN: .5, torso: .15 } });
    c.font = '600 34px Cinzel'; c.fillStyle = C.ink; c.textAlign = 'center';
    c.fillText('ΓΑΙΑ', 300, 120); c.fillText('ΟΥΡΑΝΟΣ', 900, 90); c.fillText('ΚΡΟΝΟΣ', 1500, 130);
  });
};
// Üç taht ve kylix denemesi
SCENES.taht = (ctx, t) => {
  paperBG(ctx, t, {});
  // her taht sola devrilir (ön ayak sağda, dir -1): komşusunun üstüne düşmez
  const X = [520, 960, 1400], s = 6;
  X.forEach((x, i) => throneTip(ctx, x, 640, s, i === 0 ? ramp(t, .5, 1.3) * 1.15 : i === 1 ? ramp(t, 1.5, 2.3) * 1.15 : 0, { dir: 1, col: PW.line, inc: PW.paperL, shake: i === 2 ? 2 * ramp(t, 2.6, 3) : 0 }));
  crackLine(ctx, 1400 + 18 * s + 2, 640, 140, ramp(t, 3, 4));
  ['ΟΥΡΑΝΟΣ', 'ΚΡΟΝΟΣ', 'ΖΕΥΣ'].forEach((n, i) => txt(ctx, n, X[i], 720, { font: '600 34px Cinzel', col: PW.line, ls: 4 }));
};
SCENES.kylix = (ctx, t) => {
  ctx.fillStyle = '#120B08'; ctx.fillRect(0, 0, W, H);
  kylix(ctx, t, W / 2, H / 2 + 20, 400, t * .12, (c, t, r) => {
    c.fillStyle = C.ink; c.fillRect(-r, r * .55, 2 * r, 8);
    figure(c, { x: -170, y: r * .55 - 44.5 * 3.6, s: 3.6, dir: 1, sty: STY.black, lk: { beard: 'short', hair: 'long' }, p: { shN: -2.6, shF: -2.5, elN: -.5, elF: -.6, torso: .1 } });
    figure(c, { x: 170, y: r * .55 - 44.5 * 3.6, s: 3.6, dir: -1, sty: STY.black, lk: LK.prom, p: { torso: -.1 } });
    eagle2(c, 120, -150, 1.6, 1, { flap: (t * .6) % 1, col: C.ink, line: C.clay });
  }, { tilt: .96 });
};
SCENES.style2 = (ctx, t) => {
  const u = E.io2(clamp(t / 6));
  const c = { x: lerp(1000, 1060, u), y: lerp(540, 520, u), z: lerp(1.0, 1.06, u), sx: noise1(t * .3, 1) * 3, sy: noise1(t * .3, 2) * 2 };
  // kartal: sol üst köşeden göğse doğru köşegen dalış (Zeus'un soğuk çakmasının içinden çıkar)
  const k = E.io2(clamp(t / 5.5));
  const ex = lerp(-160, 720, k), ey = lerp(300, 425, k), es = lerp(2.2, 2.9, k);
  const { wind } = kayaWorld(ctx, t, c, { eagleX: ex, eagleY: ey });
  ctx.save(); cam(ctx, c, 1);
  if (t < .6) { const fa = Math.sin(clamp(t / .6) * PI); glow(ctx, 160, 120, 380, `rgba(225,232,255,${.35 * fa})`); ctx.save(); ctx.globalAlpha = .75 * fa; bolt(ctx, 170, 140, 1.3, .55, '#DDE3F2', 'rgba(210,220,255,.25)'); ctx.restore(); }
  // dipinto ad yazısı (eklenmiş kırmızı), figür boyunca dikey
  dipinto(ctx, 'ΠΡΟΜΗΘΕΥΣ', 985, 62, 28, { col: '#9C3A24', vertical: true, align: 'left', w: .1 });
  // çığlıkta tepki: irkilmez; çenesini kaldırır, gözünü kısar, gövdesi tek bir kez gerilir
  const br3 = Math.exp(-Math.pow((t - 3.45) / .45, 2)), lid = .28 + .12 * E.io2(clamp((t - 3.3) / .5));
  promChained(ctx, t, { look: lerp(-.12, -.04, k) - .07 * br3, wind, pull: .25 + .15 * br3, dust: br3, p: { blink: lid, scowl: .6 + .25 * br3 } });
  const fl = (t * .55) % 1, glide = .5 + .5 * Math.cos(fl * TAU);
  const cry = Math.exp(-Math.pow((t - 3.2) / .25, 2));
  eagle2(ctx, ex + Math.sin(t * .7) * 8, ey + Math.sin(t * 1.1) * 6 - 4 * es * Math.sin(TAU * (fl - .08)) * .4, es, 1, {
    ang: lerp(.62, lerp(.74, .97, k), Math.pow(glide, .5)), angFar: .2, farOff: -.5, fsMin: .62,
    talon: lerp(.4, 1, k), beak: .08 + .8 * cry, tilt: lerp(.32, .46, k) + Math.sin(t * .7) * .02, headA: -Math.sin(t * .7) * .03 - .06,
    col: '#A85A32', wingCol: mixCol(PC.clayR, PC.glaze, .22), farCol: mixCol(PC.clayR, PC.glaze, .5), eye: '#E39A4E', headS: 1.4,
  });
  ctx.restore();
  kayaFrame(ctx, t);
};
SCENES.style2.post = { tex: .55, vig: 1, grain: .06 };
// Kartal çırpma döngüsü denemesi: 16 faz
SCENES.flap = (ctx, t) => {
  ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
  for (let i = 0; i < 16; i++) eagle2(ctx, 160 + (i % 8) * 230, 260 + Math.floor(i / 8) * 480, 1.25, 1, { ang: .5 + .5 * Math.cos(i / 16 * TAU), angFar: .5 + .5 * Math.cos(i / 16 * TAU + .3), farOff: -.3, fsMin: .5, col: '#A85A32', wingCol: mixCol(PC.clayR, PC.glaze, .22), farCol: mixCol(PC.clayR, PC.glaze, .5), eye: '#E39A4E' });
};
