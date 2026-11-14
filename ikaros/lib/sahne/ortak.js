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
  pr.ink(fig.far, o.farLimb || 'mid');
  litInk(pr, fig.body, 'lit', o.body || 'near', L[0], L[1], dl);
  if (fig.face) { pr.ink(fig.face, 'lit', { sheen: .2 }); pr.ink(fig.eye, o.body || 'near', { sheen: 0 }); }
  if (w) {
    const wn = FG.wing({ root: R0, ang: w.ang, bend: w.bend, span: w.span, chord: w.chord, f: w.side, seed: w.seed || 1, ruin: w.ruin });
    litInk(pr, wn.all, 'lit', o.wing || 'near', L[0], L[1], dl * .8);
    pr.ink(wn.cov, o.cov || 'mid', { sheen: .1 });
  }
  return fig;
}
function gunes(pr, x, y, r, n = 3) { const s = FG.sunRings(x, y, r, n); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'acc'); }

