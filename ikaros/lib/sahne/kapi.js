// Üslup kapısı sahneleri (CLAUDE.md: manzara + orta plan figür + yakın plan + 15 sn hareket). ?scene=manzara|orta|yakin|ucus&t=…
'use strict';
const SCENES = {};
// ışıklı yüz: önce ışık mürekkebi, sonra koyu mürekkep ışığın tersine kaydırılmış ve şeklin içine kırpılmış → ışık yanında hilal
function litInk(pr, path, litRole, darkRole, lx, ly, d) {
  pr.ink(path, litRole, { sheen: .2 });
  const p2 = new Path2D(); p2.addPath(path, new DOMMatrix().translate(-lx * d, -ly * d));
  pr.ink(p2, darkRole, { clip: path, sheen: .25, trap: .4 });
}
function kSt(t, seed = 1) { return { t, lt: t, at: 0, d: 15, p: t / 15, seed }; }
// kanatlı figür: w = {ang, bend, span, chord, side, ruin}; kanat kola bağlı, yakın kol kanadın ön kenarında kalır
function kanatliFigur(pr, J, o) {
  const w = o.w, L = o.light, dl = o.litD ?? J.h * .09;
  if (w) {
    const wf = FG.wing({ root: [J.Sh[0] + (o.farOff || [0, 0])[0], J.Sh[1] + (o.farOff || [0, 0])[1]], ang: w.ang + (w.farDa ?? -.1), bend: w.bend, span: w.span * .93, chord: w.chord, f: w.side, seed: (w.seed || 1) + 1, ruin: w.ruin });
    pr.ink(wf.all, o.farWing || 'mid');
  }
  const fig = FG.figure(J, { ...(o.look || {}), noArmN: !!w && o.armInWing !== false, noArmF: !!w && o.armInWing !== false });
  pr.ink(fig.far, o.farLimb || 'mid');
  litInk(pr, fig.body, 'lit', o.body || 'near', L[0], L[1], dl);
  if (w) {
    const wn = FG.wing({ root: J.Sh, ang: w.ang, bend: w.bend, span: w.span, chord: w.chord, f: w.side, seed: w.seed || 1, ruin: w.ruin });
    litInk(pr, wn.all, 'lit', o.wing || 'near', L[0], L[1], dl * .8);
    pr.ink(wn.cov, o.cov || 'mid', { sheen: .1 });
  }
  return fig;
}
function gunes(pr, x, y, r, n = 3) { const s = FG.sunRings(x, y, r, n); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'acc'); }

// 1. MANZARA: şafakta Girit; yalıyarın üstünde labirent, denizin ortasında güneş doğuyor; kıyının ucunda baba ve oğul.
SCENES.manzara = (ctx, t) => baski(ctx, kSt(t, 2), null, pr => {
  pr.sky('sky2', 'sky1', 150, 420, 5);
  gunes(pr, 1360, 640, 118, 3);
  pr.ink(FG.ridge(980, 1920, 700, 600, 70, 11), 'far');
  const sea = new Path2D(); sea.rect(-50, 660, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 });
  pr.bands('near', 860, 1080, 4, 0, { trap: .2 });
  pr.ink(FG.glints(1220, 1500, 680, 860, 18, 5, t, 50), 'acc', { sheen: 0, reg: 0 });
  pr.ink(FG.glints(500, 1900, 720, 980, 16, 6, t, 40), 'sky1', { sheen: 0, reg: 0 });
  pr.ink(FG.cliff(-60, 860, 520, 1100, 1, 4), 'near');
  for (const [x, hh, beard] of [[738, 14, true], [790, 12, false]]) {
    const J = FG.rig({ x, y: 520 - hh * 3.75, h: hh, f: 1, armN: [.15, -.1], armF: [-.1, -.1] });
    kanatliFigur(pr, J, { w: { ang: 1.75, bend: .25, span: hh * 4.4, chord: hh * 1.7, side: 1, seed: x }, light: [1, -.2], farOff: [-2, -1], look: { beard, curls: !beard } });
  }
  [[1100, 300, 16, 1], [1180, 260, 11, 2.2], [1240, 330, 9, 4]].forEach(([x, y, s, ph]) => pr.ink(FG.gull(x, y + Math.sin(t * 1.3 + ph) * 4, s, t * 5 + ph), 'mid', { sheen: 0 }));
});

// 2. ORTA PLAN: kıyıdaki atölye. İkaros kanatları ilk kez açıyor; Daidalos (uzun tunik, sakal) arkasında kayışı tutuyor.
SCENES.orta = (ctx, t) => baski(ctx, kSt(t, 3), null, pr => {
  pr.sky('sky2', 'sky1', 120, 380, 5);
  gunes(pr, 1620, 300, 70, 2);
  const sea = new Path2D(); sea.rect(-50, 640, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 });
  pr.ink(FG.ridge(1250, 1960, 680, 580, 60, 21), 'far');
  pr.ink(FG.glints(200, 1900, 660, 780, 22, 8, t, 50), 'sky1', { sheen: 0, reg: 0 });
  pr.ink(FG.ridge(-40, 1960, 1100, 850, 40, 22, 5), 'near');
  const r = rng(9), tu = new Path2D(); for (let i = 0; i < 12; i++) { const x = 200 + r() * 1500, y = 900 + r() * 120, a = r() * 6.28, l = 26 + r() * 30; FG.ellipseInto(tu, x, y, l, 7, a, 14); } pr.ink(tu, 'lit', { sheen: 0 });
  const nf = Math.sin(t * 1.3), op = E.io2(clamp((t - 1) / 3));
  const Jd = FG.rig({ x: 700, y: 600, h: 56, f: 1, lean: .2, head: .2, armN: [1.35 + Math.sin(t * 2.4) * .05, -.7], armF: [1.1, -.9], legN: [.12, -.05], legF: [-.12, 0] });
  kanatliFigur(pr, Jd, { light: [1, -.35], look: { beard: true, long: true } });
  const Ji = FG.rig({ x: 1060, y: 610, h: 52, f: 1, lean: .08, head: -.35 - op * .15, armN: [.2, 0], armF: [.2, 0], legN: [.1, -.05], legF: [-.12, 0] });
  kanatliFigur(pr, Ji, { w: { ang: lerp(1.9, -2.35, op) + nf * .04 * op, bend: lerp(.2, -.35, op), span: 300, chord: 120, side: op > .5 ? -1 : 1, seed: 7 }, light: [1, -.35], farOff: [-16, -6], look: { curls: true } });
});

// 3. YAKIN PLAN: İkaros'un başı ve kanadı; güneşe bakıyor (güneş başın arkasında değil: hale okunmasın)
SCENES.yakin = (ctx, t) => baski(ctx, kSt(t, 4), null, pr => {
  pr.sky('sky2', 'sky1', 200, 560, 6);
  gunes(pr, 1540, 250, 95, 3);
  pr.ink(FG.cloud(1250, 520, 560, 110, 3), 'paper', { sheen: 0 });
  const J = FG.rig({ x: 860, y: 1180, h: 210, f: 1, lean: .05, head: -.62 + Math.sin(t * .8) * .04, armN: [.1, 0], armF: [.1, 0] });
  kanatliFigur(pr, J, { w: { ang: -2.55 + Math.sin(t * .8) * .03, bend: -.3, span: 980, chord: 360, side: -1, seed: 12 }, light: [1, -.7], litD: 14, farOff: [-50, 10], look: { curls: true, chest: true } });
});

// 4. HAREKETLİ (15 sn): baba ve oğul denizin üstünde; aşağıda bir balıkçı başını kaldırır; 8. sn'de gün ilerler (şafak → öğle, çapraz rakle)
PALT.push({ at: -1e9, pal: 'SAFAK' });
if (new URLSearchParams(location.search).get('scene') === 'ucus') PALT.push({ at: 8, pal: 'OGLE', dur: .7 });
SCENES.ucus = (ctx, t) => {
  const cam = { cx: 960 + t * 38, cy: 540 };
  baski(ctx, kSt(t, 5), cam, pr => {
    const x0 = cam.cx - 1100;
    pr.sky('sky2', 'sky1', 100, 420, 5);
    gunes(pr, cam.cx + 520 - t * 6, 230, 80, 3);
    pr.ink(FG.cloud(900 + t * 10, 330, 600, 110, 5), 'paper', { sheen: 0 });
    pr.ink(FG.cloud(2050, 280, 420, 80, 6), 'paper', { sheen: 0 });
    pr.ink(FG.ridge(1200, 2900, 780, 700, 60, 31), 'far');
    const sea = new Path2D(); sea.rect(x0 - 100, 760, 4000, 500); pr.ink(sea, 'mid', { sheen: 0 });
    pr.bands('near', 920, 1100, 4, 0, { trap: .2 });
    pr.ink(FG.glints(x0, x0 + 2600, 780, 1000, 34, 9, t, 50), 'sky1', { sheen: 0, reg: 0 });
    const rock = FG.ridge(1700, 2060, 1100, 900, 60, 41, 5); pr.ink(rock, 'near');
    const lookUp = E.io2(clamp((t - 4.5) / 1.5));
    const Jb = FG.rig({ x: 1860, y: 860, h: 16, f: -1, lean: .35 - lookUp * .4, head: .35 - lookUp * 1.25, armN: [1.25, -.6], armF: [1.05, -.4], legN: [1.45, -1.7], legF: [1.3, -1.5] });
    const fb = FG.figure(Jb, {}); pr.ink(fb.far, 'mid'); pr.ink(fb.body, 'near');
    const rod = new Path2D(); FG.capsule(rod, Jb.armN[2], [Jb.armN[2][0] - 130, Jb.armN[2][1] - 80 + Math.sin(t * 2) * 3], 2.4, 1.5); pr.ink(rod, 'near', { sheen: 0 });
    for (const [dx, dy, hh, beard, ph] of [[220, 520, 38, true, 0], [-120, 400, 34, false, 1.3]]) {
      const fl = Math.sin(t * 3.0 + ph), x = cam.cx + dx + Math.sin(t * .7 + ph) * 20, y = dy + Math.sin(t * 1.4 + ph) * 14 + fl * 6;
      const J = FG.rig({ x, y, h: hh, f: 1, lean: 1.3, head: -1.05, legN: [-.05, .12], legF: [-.18, .2] });
      kanatliFigur(pr, J, { w: { ang: -1.65 - fl * .55, bend: -.25 - fl * .1, span: hh * 6.4, chord: hh * 2.3, side: -1, seed: ph * 10 + 3, farDa: .25 }, light: [.8, -.6], farOff: [hh * .3, -hh * .2], look: { beard, curls: !beard } });
    }
    [[700, 620, 14, 0], [760, 580, 10, 1.4], [2400, 540, 12, 2]].forEach(([x, y, s, ph]) => pr.ink(FG.gull(x + t * 20, y + Math.sin(t * 1.3 + ph) * 5, s, t * 6 + ph), 'near', { sheen: 0 }));
  });
};
