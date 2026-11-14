// Üslup kapısı sahneleri (CLAUDE.md: manzara + orta plan figür + yakın plan + 15 sn hareket). ?scene=manzara|orta|yakin|ucus&t=…
'use strict';
const SCENES = {};
// 1. MANZARA: şafakta Girit; yalıyarın üstünde labirent, denizin ortasında güneş doğuyor; kıyının ucunda baba ve oğul.
SCENES.manzara = (ctx, t, st) => baski(ctx, st || kSt(t, 2), null, pr => {
  pr.sky('sky2', 'sky1', 150, 420, 5);
  gunes(pr, 1360, 640, 118, 3);
  pr.ink(FG.ridge(980, 1920, 700, 600, 70, 11), 'far');
  const sea = new Path2D(); sea.rect(-50, 660, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 });
  pr.bands('near', 860, 1080, 4, 0, { trap: .2 });
  pr.ink(FG.glints(1220, 1500, 680, 860, 18, 5, t, 50), 'acc', { sheen: 0, reg: 0 });
  pr.ink(FG.glints(500, 1900, 720, 980, 16, 6, t, 40), 'sky1', { sheen: 0, reg: 0 });
  litInk(pr, FG.cliff(-60, 860, 520, 1100, 1, 4), 'lit', 'near', 1, -.15, 16);
  for (const [x, hh, beard] of [[600, 14, true], [652, 12, false]]) {
    const J = FG.rig({ x, y: 520 - hh * 3.75, h: hh, f: 1, armN: [.15, -.1], armF: [-.1, -.1] });
    kanatliFigur(pr, J, { w: { ang: 1.75, bend: .25, span: hh * 4.4, chord: hh * 1.7, side: 1, seed: x }, light: [1, -.2], farOff: [-2, -1], look: { beard, curls: !beard } });
  }
  [[1100, 300, 16, 1], [1180, 260, 11, 2.2], [1240, 330, 9, 4]].forEach(([x, y, s, ph]) => pr.ink(FG.gull(x, y + Math.sin(t * 1.3 + ph) * 4, s, t * 5 + ph), 'mid', { sheen: 0 }));
});

// 2. ORTA PLAN: kıyıdaki atölye. İkaros kanatları ilk kez açıyor; Daidalos (uzun tunik, sakal) arkasında kayışı tutuyor.
SCENES.orta = (ctx, t, st) => baski(ctx, st || kSt(t, 3), null, pr => {
  pr.sky('sky2', 'sky1', 120, 380, 5);
  gunes(pr, 1620, 300, 70, 2);
  const sea = new Path2D(); sea.rect(-50, 640, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 });
  pr.ink(FG.ridge(1250, 1960, 680, 580, 60, 21), 'far');
  pr.ink(FG.glints(200, 1900, 660, 780, 22, 8, t, 50), 'sky1', { sheen: 0, reg: 0 });
  pr.ink(FG.ridge(-40, 1960, 1100, 850, 40, 22, 5), 'near');
  const r = rng(9), tu = new Path2D(); for (let i = 0; i < 5; i++) { const x = 300 + r() * 1300, y = 930 + r() * 90, a = -.3 + r() * .6, l = 46 + r() * 20; FG.ellipseInto(tu, x, y, l, 7, a, 14); } pr.ink(tu, 'lit', { sheen: 0 });
  const nf = Math.sin(t * 1.3), op = E.io2(clamp((t - 1) / 3));
  // İkaros kayalığın ucunda kanatlarını ilk kez açıyor; Daidalos geride (daha küçük), bir eli kalkık, izliyor
  const Ji = FG.rig({ x: 1150, y: 640, h: 58, f: 1, lean: .1, head: -.35 - op * .2, armN: [.2, 0], armF: [.2, 0], legN: [.12, -.05], legF: [-.16, 0] });
  const Jd = FG.rig({ x: 470, y: 600, h: 72, f: 1, lean: .04, head: -.12, armN: [1.0 + Math.sin(t * 1.2) * .05, -.5], armF: [.15, -.3], legN: [.08, -.03], legF: [-.1, 0] });
  kanatliFigur(pr, Jd, { light: [1, -.35], litD: 4, look: { beard: true, long: true, face: true } });
  kanatliFigur(pr, Ji, { w: { ang: -2.15 + nf * .04 * op - (1 - op) * .45, bend: -.35, span: lerp(150, 330, op), chord: lerp(80, 130, op), side: -1, seed: 7 }, rootBack: .55, light: [1, -.35], litD: 5, farOff: [-22, -10], look: { curls: true, face: true } });
});

// 3. YAKIN PLAN: İkaros'un başı ve kanadı; güneşe bakıyor (güneş başın arkasında değil: hale okunmasın)
SCENES.yakin = (ctx, t, st) => baski(ctx, st || kSt(t, 4), null, pr => {
  pr.sky('sky2', 'sky1', 90, 330, 5);
  gunes(pr, 1540, 250, 95, 3);
  const J = FG.rig({ x: 860, y: 1180, h: 210, f: 1, lean: .05, head: -.62 + Math.sin(t * .8) * .04, armN: [.1, 0], armF: [.1, 0] });
  kanatliFigur(pr, J, { w: { ang: -2.55 + Math.sin(t * .8) * .03, bend: -.3, span: 980, chord: 360, side: -1, seed: 12 }, armInWing: false, kosum: true, light: [1, -.7], litD: 4, farOff: [-50, 10], faceFill: false, look: { curls: true, chest: true, face: true } });
});

// 4. HAREKETLİ (15 sn): baba ve oğul denizin üstünde; aşağıda bir balıkçı başını kaldırır; 8. sn'de gün ilerler (şafak → öğle, çapraz rakle)
if (new URLSearchParams(location.search).get('scene')) { PALT.length = 0; PALT.push({ at: -1e9, pal: 'SAFAK' }); if (new URLSearchParams(location.search).get('scene') === 'ucus') PALT.push({ at: 8, pal: 'OGLE', dur: .7 }); }
SCENES.ucus = (ctx, t, st) => {
  const cam = { cx: 960 + t * 38, cy: 540 }, dx = cam.cx - 960, par = k => dx * (1 - k);   // par: düzlemin kamerayla birlikte kayan payı (k = derinlik katsayısı)
  baski(ctx, st || kSt(t, 5), cam, pr => {
    pr.sky('sky2', 'sky1', 100, 420, 5);
    gunes(pr, 1660 + par(.04), 170, 70, 2);
    pr.ink(FG.cloud(900 + par(.35), 330, 600, 110, 5), 'paper', { sheen: 0 });
    pr.ink(FG.cloud(2050 + par(.35), 280, 420, 80, 6), 'paper', { sheen: 0 });
    pr.ink(FG.ridge(1200 + par(.15), 2900 + par(.15), 780, 700, 60, 31), 'far');
    const sea = new Path2D(); sea.rect(cam.cx - 1200, 760, 4000, 500); pr.ink(sea, 'mid', { sheen: 0 });
    pr.bands('near', 980, 1100, 3, 0, { trap: .2 });
    pr.ink(FG.glints(-200, 3200, 780, 1000, 60, 9, t, 50), 'sky1', { sheen: 0, reg: 0 });
    const rock = FG.ridge(1700, 2060, 1100, 900, 60, 41, 5); pr.ink(rock, 'near');
    const lookUp = E.io2(clamp((t - 4.5) / 1.5));
    const Jb = FG.rig({ x: 1850, y: 830, h: 26, f: -1, lean: .35 - lookUp * .5, head: .45 - lookUp * 1.5, armN: [1.25, -.6], armF: [1.05, -.4], legN: [1.45, -1.7], legF: [1.3, -1.5] });
    const fb = FG.figure(Jb, {}); pr.ink(fb.far, 'near'); litInk(pr, fb.body, 'lit', 'near', -1, -.4, 2);
    const rod = new Path2D(); FG.capsule(rod, Jb.armN[2], [Jb.armN[2][0] - 170, Jb.armN[2][1] - 100 + Math.sin(t * 2) * 3], 3, 2); pr.ink(rod, 'near', { sheen: 0 });
    for (const [ox, oy, hh, beard, ph] of [[150, 560, 50, true, 0], [-230, 450, 42, false, 1.3]]) {
      // çırpma: aşağı vuruş döngünün %40'ı (kanat tam açık), yukarı vuruşta toplanır
      const cyc = ((t * .55 + ph * .2) % 1 + 1) % 1, down = cyc < .4, u = down ? cyc / .4 : (cyc - .4) / .6;
      const angW = down ? lerp(-1.6, -2.95, E.io2(u)) : lerp(-2.95, -1.6, E.io2(u)), open = down ? 1 : .72 + .28 * Math.abs(u - .5) * 2;
      const x = cam.cx + ox + Math.sin(t * .7 + ph) * 20, y = oy + Math.sin(t * 1.4 + ph) * 14 + (down ? -6 : 6) * Math.sin(u * Math.PI);
      const J = FG.rig({ x, y, h: hh, f: 1, lean: 1.12, head: -.85, legN: [-.12, .35], legF: [-.38, .55] });
      kanatliFigur(pr, J, { w: { ang: angW, bend: -.25, span: hh * 6.4 * open, chord: hh * 2.3 * (.8 + .2 * open), side: -1, seed: ph * 10 + 3, farDa: .6 }, light: [.8, -.6], litD: 3, farOff: [hh * .3, -hh * .2], look: { beard, curls: !beard, long: false } });
    }
    [[700, 620, 14, 0], [760, 580, 10, 1.4], [2400, 540, 12, 2]].forEach(([x, y, s, ph]) => pr.ink(FG.gull(x + t * 20, y + Math.sin(t * 1.3 + ph) * 5, s, t * 6 + ph), 'near', { sheen: 0 }));
  });
};
