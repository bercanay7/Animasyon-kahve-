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
