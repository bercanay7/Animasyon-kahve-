const add2c = (a, b, k) => [a[0] + b[0] * k, a[1] + b[1] * k];
// Ortak sahne yardımcıları (İkaros): ışıklı mürekkep, kanatlı figür, güneş. Bütün setler kullanır; yalnız başkan değiştirir.
'use strict';
// ışıklı yüz: önce ışık mürekkebi, sonra koyu mürekkep ışığın tersine kaydırılmış ve şeklin içine kırpılmış → ışık yanında hilal
function litInk(pr, path, litRole, darkRole, lx, ly, d) {
  pr.ink(path, litRole, { sheen: .2 });
  const p2 = new Path2D(); p2.addPath(path, new DOMMatrix().translate(-lx * d, -ly * d));
  pr.ink(p2, darkRole, { clip: path, sheen: .25, trap: .4 });
}
function kSt(t, seed = 1) { return { t, lt: t, at: 0, d: 15, p: t / 15, seed }; }
// kanatlı figür: w = {ang, bend, span, chord, side, ruin}; kanat kola bağlı, yakın kol kanadın ön kenarında kalır
function kanatliFigur(pr, J, o) {
  const w = o.w, L = o.light, dl = o.litD ?? J.h * .09, rb = (o.rootBack ?? .45) * J.h, R0 = [J.Sh[0] - J.upv[0] * rb, J.Sh[1] - J.upv[1] * rb];
  if (w) {
    const wf = FG.wing({ root: [R0[0] + (o.farOff || [0, 0])[0], R0[1] + (o.farOff || [0, 0])[1]], ang: w.ang + (w.farDa ?? -.1), bend: w.bend, span: w.span * .93, chord: w.chord, f: w.side, seed: (w.seed || 1) + 1, ruin: w.ruin });
    pr.ink(wf.all, o.farWing || 'mid');
  }
  const fig = FG.figure(J, { ...(o.look || {}), noArmN: !!w && o.armInWing !== false, noArmF: !!w && o.armInWing !== false });
  pr.ink(fig.far, o.farLimb || 'near');
  litInk(pr, fig.body, 'lit', o.body || 'near', L[0], L[1], dl);
  if (fig.belt) pr.ink(fig.belt, o.beltRole || 'lit', { sheen: 0 });
  if (o.kosum) { const k = new Path2D(), fw = [Math.cos(J.lean) * J.f, Math.sin(J.lean)]; FG.capsule(k, add2c(add2c(J.Sh, fw, -.35 * J.h), J.upv, .05 * J.h), add2c(add2c(J.H, fw, .45 * J.h), J.upv, 1.5 * J.h), J.h * .07, J.h * .07); pr.ink(k, 'lit', { sheen: 0 }); }
  if (fig.face) { if (o.faceFill !== false) { pr.ink(fig.face, 'lit', { sheen: .2 }); pr.ink(fig.eye, o.body || 'near', { sheen: 0 }); } else pr.ink(fig.eye, 'paper', { sheen: 0, reg: 0 }); }
  if (w) {
    const wn = FG.wing({ root: R0, ang: w.ang, bend: w.bend, span: w.span, chord: w.chord, f: w.side, seed: w.seed || 1, ruin: w.ruin });
    litInk(pr, wn.all, 'lit', o.wing || 'near', L[0], L[1], dl * .8);
    pr.ink(wn.cov, o.cov || 'mid', { sheen: .1 });
    // kol kanadın ön kenarında: omuzdan bileğe ten rengi kol + iki kayış (melek değil, kola bağlı yapma kanat)
    if (o.armInWing !== false) { const arm = new Path2D(); FG.capsule(arm, J.Sh, wn.wrist, J.h * .2, J.h * .14); pr.ink(arm, o.armRole || 'lit', { sheen: .2 });
      const kay = new Path2D(); for (const u of [.35, .78]) { const q = [lerp(J.Sh[0], wn.wrist[0], u), lerp(J.Sh[1], wn.wrist[1], u)], a = Math.atan2(wn.wrist[1] - J.Sh[1], wn.wrist[0] - J.Sh[0]), n = [-Math.sin(a), Math.cos(a)]; FG.capsule(kay, add2c(q, n, -J.h * .24), add2c(q, n, J.h * .24), J.h * .055, J.h * .055); }
      pr.ink(kay, o.body || 'near', { sheen: 0 }); }
  }
  return fig;
}
function gunes(pr, x, y, r, n = 3) { const s = FG.sunRings(x, y, r, n); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'acc'); }

// keklik: tombul gövde, küçük baş, kısa kuyruk; f yön, s ölçek (gövde boyu), kanat (0 kapalı .. 1 açık çırpma), bas (0..1 baş kalkık)
function keklikPath(x, y, s, f = 1, kanat = 0, bas = 0) {
  const p = new Path2D(), T = (a, b) => [x + a * s * f, y + b * s];
  FG.ellipseInto(p, ...T(0, 0), s * .55, s * .38, -.12 * f, 24);
  FG.ellipseInto(p, ...T(.5, -.36 - bas * .12), s * .19, s * .17, 0, 16);
  FG.polyInto(p, [T(.66, -.38 - bas * .12), T(.8, -.33 - bas * .12), T(.66, -.29 - bas * .12)]);
  FG.polyInto(p, [T(-.5, -.1), T(-.8, -.22), T(-.78, -.05), T(-.5, .1)]);
  FG.capsule(p, T(.08, .3), T(.1, .56), s * .035, s * .03); FG.capsule(p, T(-.1, .3), T(-.12, .56), s * .035, s * .03);
  if (kanat > 0) FG.polyInto(p, [T(-.1, -.2), T(-.3 - kanat * .3, -.55 - kanat * .55), T(.15, -.7 - kanat * .4), T(.25, -.2)]);
  return p;
}
// yalnız düz mürekkep yazı afişi için: kare boyu bir bant
function bant(pr, y0, y1, role, o = {}) { const p = new Path2D(); p.rect(pr.cam.x - 200, y0, W / pr.cam.s + 400, y1 - y0); pr.ink(p, role, { sheen: 0, trap: .3, ...o }); }
