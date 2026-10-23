'use strict';
const SCENES = {};
SCENES.sheet = (ctx, t) => {
  clayBG(ctx);
  applyTexture(ctx, .9);
  const y0 = 900;
  ctx.fillStyle = C.ink; ctx.fillRect(0, y0, W, 6);
  // 1: duran Sisifos (kral)
  figure(ctx, { x: 220, y: y0 - 48 * 6.2, s: 6.2, lk: { beard: 'pointed', hair: 'long', headgear: 'diadem', garment: 'robe', himation: true, robeDots: true },
    p: { shN: .25, elN: .6, shF: -.15, elF: .2, hipN: .05, hipF: -.04, knN: .02, knF: 0, smile: .3 } });
  // 2: yürüyen
  const ph = t * 1.2;
  figure(ctx, { x: 560, y: y0 - 46 * 6.2, s: 6.2, lk: { beard: 'pointed', hair: 'long', garment: 'short' },
    p: { torso: .08, shN: Math.sin(ph * TAU) * .5, elN: .4, shF: -Math.sin(ph * TAU) * .5, elF: .4,
      hipN: Math.sin(ph * TAU) * .45, knN: .2 + Math.max(0, Math.cos(ph * TAU)) * .7, hipF: -Math.sin(ph * TAU) * .45, knF: .2 + Math.max(0, -Math.cos(ph * TAU)) * .7, ankN: 0, ankF: 0 } });
  // 3: kaya iten (IK)
  const rx = 1180, R = 150;
  boulder(ctx, rx, y0 - R, R, -t * .2);
  figure(ctx, { x: 905, y: y0 - 40 * 6.2, s: 6.2, lk: { beard: 'pointed', hair: 'long', garment: 'short', torn: true },
    p: { torso: .95, neck: -.35, head: -.35, handN: 'flat', handF: 'flat', brow: -1 },
    ik: { hN: [rx - R * .98, y0 - R * 1.25], hF: [rx - R * .95, y0 - R * .95], fN: [890, y0 - 3 * 6.2, 0], fF: [760, y0 - 3 * 6.2 - 10, .5] } });
  // 4: kadın (beyaz ten)
  figure(ctx, { x: 1500, y: y0 - 48 * 6.2, s: 6.2, lk: { fem: true, garment: 'robe', robeDots: true, earring: true },
    p: { shN: .5, elN: 1.2, shF: -.1, elF: .3, hipN: .04, hipF: -.03 } });
  // 5: Ares
  figure(ctx, { x: 1760, y: y0 - 47 * 6.2, s: 6.2, dir: -1, lk: { beard: 'pointed', headgear: 'helmet', garment: 'short', greaves: true },
    p: { shN: .9, elN: .9, shF: .3, elF: 1.4, hipN: .2, hipF: -.15, knF: .1 } });
  friezeFrame(ctx, { h: 50 });
  applyVignette(ctx, .8);
  applyGrain(ctx, t, .06);
};
SCENES.props = (ctx, t) => {
  clayBG(ctx);
  cloud(ctx, 300, 160, 1, C.clayD, C.clay, 1);
  temple(ctx, 1500, 360, 1.2);
  ship(ctx, 900, 330, 1.1, t);
  cow(ctx, 260, 700, 2.4, 1, t * .6, {});
  cow(ctx, 640, 700, 2.4, 1, t * .6 + .3, { col: C.white, inc: C.ink, farCol: '#CDBFA4' });
  eagle(ctx, 1150, 650, 1.6, 1, t * .8, {});
  ram(ctx, 1600, 760, 2.2, -1, {});
  bolt(ctx, 1780, 300, 1, .3);
  chain(ctx, [[100, 950], [500, 900], [900, 980]], 26, C.ink, C.clay, 6);
  amphora(ctx, 1300, 980, 1.4);
  sea(ctx, 1000, 1920, 900, 3, 40, t, C.ink, '#2a1b14');
  applyTexture(ctx, .85);
};
SCENES.tart = (ctx, t) => {
  const xr = 300 + t * 60;
  const c = { x: xr - 60, y: hillY(xr) - 180, z: 1.0 };
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: .5 });
  pushScene(ctx, c, xr, 150, 4.0, t, {});
};
SCENES.tartWide = (ctx, t) => {
  const xr = 900 + t * 30;
  const c = { x: 700, y: 420, z: .55 };
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: .5 });
  pushScene(ctx, c, xr, 150, 4.0, t, {});
};
SCENES.tartGrid = (ctx, t) => {
  const vars = [{}, { stride: 52, footBack: 12 }, { stride: 38, footBack: 6 }, { T: 1.45, reach: 12 }];
  vars.forEach((v, i) => {
    ctx.save(); ctx.translate((i % 2) * W / 2, Math.floor(i / 2) * H / 2); ctx.scale(.5, .5);
    ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.clip();
    const xr = 300 + t * 60; const c = { x: xr - 60, y: hillY(xr) - 180, z: 1 };
    tartarosBG(ctx, t, c, {}); tartarosHill(ctx, c, {});
    pushScene(ctx, c, xr, 150, 4.0, t, v);
    txt(ctx, JSON.stringify(v), 200, 60, { font: '40px monospace', col: '#fff' });
    ctx.restore();
  });
};
SCENES.flatGrid = (ctx, t) => {
  const vars = [{ R: 130, T: 1.1, hA: .85, hB: .85 }, { R: 120, T: 1.0, hA: 1.0, hB: .9, reach: 15 }, { R: 130, T: 1.2, hA: .8, hB: .8, footBack: 16 }, { R: 140, T: 1.1, hA: .7, hB: .7 }];
  clayBG(ctx);
  vars.forEach((v, i) => {
    const gx = (i % 2) * W / 2, gy = Math.floor(i / 2) * H / 2 + 480;
    ctx.fillStyle = C.ink; ctx.fillRect(gx, gy, W / 2, 4);
    pushScene(ctx, null, gx + 560, v.R, 3.6, t, { noCam: true, ground: groundOf(() => gy), dist: 560, ...v });
    txt(ctx, JSON.stringify(v), gx + 300, gy - 420, { font: '28px monospace', col: '#000' });
  });
};
