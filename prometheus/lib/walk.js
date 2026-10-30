// Yardımcılar: renk karışımı, zemin nesnesi, yürüyüş adımı ve yürüyen figür (Sisifos motorundan, tepeye bağımlılığı kaldırıldı)
'use strict';
function mixCol(a, b, p) {
  if (p <= 0) return a; if (p >= 1) return b;
  const pa = parseCol(a), pb = parseCol(b);
  const m = pa.map((v, i) => lerp(v, pb[i], p));
  return `rgba(${m[0] | 0},${m[1] | 0},${m[2] | 0},${m[3].toFixed(3)})`;
}
const _colCache = {};
function parseCol(c) {
  if (_colCache[c]) return _colCache[c];
  let r;
  if (c[0] === '#') { const n = parseInt(c.slice(1), 16); r = [n >> 16 & 255, n >> 8 & 255, n & 255, 1]; }
  else { const m = c.match(/[\d.]+/g).map(Number); r = [m[0], m[1], m[2], m[3] ?? 1]; }
  return (_colCache[c] = r);
}
function gait(d, S2, h, o) {
  const c = d / S2 + o, k = Math.floor(c), u = c - k;
  let x = (k - o) * S2 + .3 * S2, lift = 0, heel = 0;
  if (u >= .6) { const v = (u - .6) / .4; x += S2 * E.sine(v); lift = Math.sin(v * PI) * h; heel = -.25 * Math.sin(v * PI); }
  else if (u > .42) heel = .55 * (u - .42) / .18;
  return { x, lift, heel, u };
}
function groundOf(f) { // y(x) fonksiyonundan zemin nesnesi
  return { y: f, a: x => Math.atan2(f(x + 2) - f(x - 2), 4), n: x => { const dy = f(x + 2) - f(x - 2), l = Math.hypot(4, dy); return [dy / l, -4 / l]; } };
}
// Zemin boyunca yürüyen figür: x konumu, yön dir, o.ground zemin nesnesi (groundOf)
function walkScene(ctx, c, x, s, t, dir, o = {}) {
  const gr = o.ground, hillY = gr.y, hillAng = gr.a;
  const S2 = (o.stride || 34) * s;
  const d = o.dist ?? x * dir;
  const fN = gait(d, S2, 6 * s, 0), fF = gait(d, S2, 6 * s, .5);
  const footPos = f => { const fx = x + (f.x - d) * dir; return [fx, hillY(fx) - 3 * s - f.lift - Math.max(0, Math.sin(f.heel)) * 9 * s, -(hillAng(fx) * dir + f.heel)]; };
  // kalça yüksekliği: duruş bacağı neredeyse düz kalacak kadar yüksek (çömelmiş yürüyüşü önler)
  let PF = [footPos(fN), footPos(fF)];
  // durma: ayaklar yan yana yere basar, bacaklar düzleşir (adım ortasında donmaz)
  const sd = o.stand || 0;
  if (sd > 0) { const fs = [x + 6 * s * dir, x - 5 * s * dir]; PF = PF.map((q, i) => [lerp(q[0], fs[i], sd), lerp(q[1], hillY(fs[i]) - 3 * s, sd), lerp(q[2], -hillAng(fs[i]) * dir, sd)]); }
  const L = (o.legL || 43.4) * s * lerp(.968, .99, sd); // hafif dizle: ne çömelme ne parmak ucu
  let py = -1e9;
  for (const [fx, fy] of PF) { const dx = Math.min(Math.abs(fx - x), L * .97); py = Math.max(py, fy - Math.sqrt(L * L - dx * dx)); }
  ctx.save(); if (!o.noCam) cam(ctx, c, 1);
  const J = figure(ctx, {
    x, y: py, s, dir, sty: o.sty || STY.black, cutCol: o.cutCol, alpha: o.alpha, onJoints: o.onJoints, hold: o.hold, extra: o.extra, margin: o.margin, stripe: o.stripe,
    lk: o.lk || { beard: 'pointed', hair: 'long', garment: 'short', torn: true },
    p: {
      // ikincil hareket: kollar bacaklardan biraz geç sallanır (gecikme), dirsek ileri salınımda bükülür,
      // baş adımla ters yönde hafif dengelenir, gövde her basışta hafifçe çöker
      torso: (o.lean ?? .08) + (dir > 0 ? hillAng(x) * .3 : -hillAng(x) * .25) + Math.sin((d / S2) * TAU * 2 - .6) * .02,
      neck: (o.neck || 0) - Math.sin((d / S2) * TAU * 2 - .9) * .035, head: o.head || 0,
      shN: Math.sin((d / S2) * TAU - .35) * .36, elN: .3 + Math.max(0, Math.sin((d / S2) * TAU - .6)) * .3,
      shF: -Math.sin((d / S2) * TAU - .35) * .36, elF: .3 + Math.max(0, -Math.sin((d / S2) * TAU - .6)) * .3,
      handN: 'open', handF: 'open', smile: o.smile || 0, brow: o.brow || 0, breath: Math.sin(t * 2) * .6, blink: o.blink,
      ...(o.p || {}),
    },
    ik: { fN: PF[0], fF: PF[1], ...(o.ik || {}) },
  });
  ctx.restore();
  return J;
}
