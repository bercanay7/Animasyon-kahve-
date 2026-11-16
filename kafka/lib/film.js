// Çekim sistemi (Kafka): Milton/İkaros çekim sistemi (S, Wd, A, PA, plan); baskı lib/kes.js'te (ağaç baskı).
// Her çekim bir baskıdır: draw(ctx, st) içinde baski(ctx, st, cam, fn) çağrılır; fn(pr) dünya koordinatında mürekkep basar.
// Üslup yasası (cinecode silkscreen-poster): opak düz mürekkep, gradyan yok (bantlar), çizgi yok, her katman 1–3 px kayık,
// kâğıt bir renktir, tek vurgu mürekkebi (güneş). Saydamlıkla geçiş yok: kesme, mürekkep çekişi (pull) ya da yeniden mürekkepleme.
'use strict';
const S = id => (window.CUES && CUES[id] ? CUES[id].s : 0);
const Se = id => (window.CUES && CUES[id] ? CUES[id].e : 0);
function Wd(id, w, n = 0, end = false) {
  const nw = w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  let k = 0;
  for (const x of (window.WORDS || [])) if (x.id === id && x.w.startsWith(nw)) { if (k++ === n) return end ? x.e : x.s; }
  return S(id);
}
function A(at) {
  if (typeof at === 'number') return at;
  const m = at.match(/^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$/);
  if (!m) return 0;
  return (m[2] ? Wd(m[1], m[2], +(m[3] || 0)) : S(m[1])) + (m[4] ? +m[4] : 0);
}
function PA(id, off = 0) { const p = (window.PLAN || {})[id]; if (!p) { console.log('plan yok: ' + id); return 0; } return A(p.at) + off; }

const SHOTS = [];
let SHOTS_SORTED = false;
// shot(başlangıç, çizim, {tr: {type: 'cut'|'pull', dur, dir}, over, mb, id, pal})
function shot(at, draw, o = {}) { SHOTS.push({ at, draw, ...o }); SHOTS_SORTED = false; }
function plan(id, draw, o = {}) { shot(PA(id, o.off || 0), draw, { id, ...o }); }
function shotAt(t) {
  if (!SHOTS_SORTED) { SHOTS.sort((a, b) => a.at - b.at); SHOTS_SORTED = true; }
  let i = 0;
  for (let k = 0; k < SHOTS.length; k++) if (SHOTS[k].at <= t) i = k;
  return i;
}
function shotState(i, t) {
  const sh = SHOTS[i], end = (SHOTS[i + 1] ? SHOTS[i + 1].at : (window.DUR || sh.at + 10));
  return { t, at: sh.at, lt: t - sh.at, d: end - sh.at, p: clamp((t - sh.at) / (end - sh.at)), end, seed: (i + 1) * 7.31 };
}
function camOf(c) { if (!c) return { x: 0, y: 0, s: 1 }; const z = c.z ?? 1, cx = c.cx ?? W / 2, cy = c.cy ?? H / 2; return { x: cx - W / 2 / z, y: cy - H / 2 / z, s: z }; }
function camLerp(a, b, p, ease = E.io2) { const u = ease(clamp(p)); return { cx: lerp(a.cx ?? W / 2, b.cx ?? W / 2, u), cy: lerp(a.cy ?? H / 2, b.cy ?? H / 2, u), z: lerp(a.z ?? 1, b.z ?? 1, u) }; }


function drawShot(ctx, i, t) { const sh = SHOTS[i]; if (!sh) return; ctx.save(); sh.draw(ctx, shotState(i, t)); ctx.restore(); }
function drawFilm(ctx, t) {
  const sc = new URLSearchParams(location.search).get('scene');
  if (sc && typeof SCENES !== 'undefined' && SCENES[sc]) { SCENES[sc](ctx, t); return; }
  if (!SHOTS.length) return;
  drawShot(ctx, shotAt(t), t);                     // geçiş: yalnız kesme (yeni baskı); saydamlık yok
}
function drawOver(ctx, t) {
  if (!SHOTS.length) return;
  const i = shotAt(t), sh = SHOTS[i]; if (!sh || !sh.over) return;
  const st = shotState(i, t); ctx.save(); baseT(ctx); sh.over(ctx, st); ctx.restore();
}
