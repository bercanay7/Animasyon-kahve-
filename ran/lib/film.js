// film.js (Ran): Zaman Kuryesi çekim sistemi (S, Wd, A, plan) + LemoLab ink-wash birleştiricisi.
// Her plan: fn(L, st) → birleştirici seçenekleri {bleed, vig, warm, paperCol, fade, flash}. L = layerSet (wet, dry, col); kamera L.xf ile.
'use strict';
const S = id => (window.CUES && CUES[id] ? CUES[id].s : 0);
const Se = id => (window.CUES && CUES[id] ? CUES[id].e : 0);
function Wd(id, w, n = 0, end = false) {
  const nw = w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  let k = 0;
  for (const x of (window.WORDS || [])) if (x.id === id && x.w.startsWith(nw)) { if (k++ === n) return end ? x.e : x.s; }
  console.log('kelime yok: ' + id + '@' + w); return S(id);
}
function AT(at) {
  if (typeof at === 'number') return at;
  const m = at.match(/^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$/);
  if (!m) return 0;
  return (m[2] ? Wd(m[1], m[2], +(m[3] || 0)) : S(m[1])) + (m[4] ? +m[4] : 0);
}
const SHOTS = []; let SORTED = false;
function plan(id, at, fn, o = {}) { SHOTS.push({ id, at: AT(at), fn, ...o }); SORTED = false; }
function shotAt(t) { if (!SORTED) { SHOTS.sort((a, b) => a.at - b.at); SORTED = true; } let i = 0; for (let k = 0; k < SHOTS.length; k++) if (SHOTS[k].at <= t) i = k; return i; }
function shotState(i, t) { const sh = SHOTS[i], end = SHOTS[i + 1] ? SHOTS[i + 1].at : window.DUR; return { id: sh.id, t, at: sh.at, lt: t - sh.at, d: end - sh.at, p: LIB.clamp((t - sh.at) / (end - sh.at)), end }; }
// kamera: dünya noktası (cx, cy) ekranın ortasında, z yakınlık
function cam(L, cx = 960, cy = 540, z = 1) { L.xf(z, 960 - cx * z, 540 - cy * z); }
const IMG = {};
function loadImg(k, src) { return new Promise(r => { const im = new Image(); im.onload = () => { IMG[k] = im; r(); }; im.onerror = () => { console.log('görsel yok ' + src); r(); }; im.src = src; }); }
