// woodcut.bundle.js: LemoLab woodcut motoru (MIT, commit d33bdea) tek klasik betik. Kaynak modüller lib/vendor/ altında, değiştirilmedi.
// Üretici: kafka/tools/bundle_woodcut.py. Genel ad: WC (index API), WCL (core/lib), WCT (trans).
'use strict';
const __M = {};
__M.lib = (() => {
// 通用小工具：确定性随机、插值、缓动
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const ss = t => { t = clamp(t); return t * t * (3 - 2 * t); };
const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const eo = t => 1 - Math.pow(1 - clamp(t), 3);
const ei = t => Math.pow(clamp(t), 3);
const back = (t, s = 1.8) => { t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s); };
// 弹簧落定：0→1，带一两次回弹
const spring = (t, k = 7, z = .35) => { t = Math.max(0, t); return 1 - Math.exp(-z * k * t) * Math.cos(k * Math.sqrt(1 - z * z) * t * 1.6); };
function mulberry(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
const vnoise = x => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return lerp(hash(i), hash(i + 1), u); };
const TAU = Math.PI * 2;

// 单调三次插值（Fritsch–Carlson）
function monotone(keys) {
  const n = keys.length, xs = keys.map(k => k[0]), ys = keys.map(k => k[1]);
  if (n === 1) return () => ys[0];
  const d = [], m = new Array(n).fill(0);
  for (let i = 0; i < n - 1; i++) d.push((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]));
  m[0] = d[0]; m[n - 1] = d[n - 2];
  for (let i = 1; i < n - 1; i++) m[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
  for (let i = 0; i < n - 1; i++) {
    if (d[i] === 0) { m[i] = m[i + 1] = 0; continue; }
    const a = m[i] / d[i], b = m[i + 1] / d[i], s = a * a + b * b;
    if (s > 9) { const k = 3 / Math.sqrt(s); m[i] = k * a * d[i]; m[i + 1] = k * b * d[i]; }
  }
  return t => {
    if (t <= xs[0]) return ys[0]; if (t >= xs[n - 1]) return ys[n - 1];
    let i = 0; while (t > xs[i + 1]) i++;
    const h = xs[i + 1] - xs[i], u = (t - xs[i]) / h, u2 = u * u, u3 = u2 * u;
    return (2 * u3 - 3 * u2 + 1) * ys[i] + (u3 - 2 * u2 + u) * h * m[i] + (-2 * u3 + 3 * u2) * ys[i + 1] + (u3 - u2) * h * m[i + 1];
  };
}
// 多维关键帧：[[t,[a,b,c]],...] → t => [..]
function track(keys) {
  const dim = keys[0][1].length, fs = [];
  for (let j = 0; j < dim; j++) fs.push(monotone(keys.map(k => [k[0], k[1][j]])));
  return t => fs.map(f => f(t));
}
// 分段：在 [a,b] 间 0→1→0 的包络
const env = (t, a, b, fi = .3, fo = .3) => Math.min(seg(t, a, a + fi), 1 - seg(t, b - fo, b));

const __e = {};
if (typeof clamp !== 'undefined') __e.clamp = clamp;
if (typeof lerp !== 'undefined') __e.lerp = lerp;
if (typeof seg !== 'undefined') __e.seg = seg;
if (typeof ss !== 'undefined') __e.ss = ss;
if (typeof eio !== 'undefined') __e.eio = eio;
if (typeof eo !== 'undefined') __e.eo = eo;
if (typeof ei !== 'undefined') __e.ei = ei;
if (typeof back !== 'undefined') __e.back = back;
if (typeof spring !== 'undefined') __e.spring = spring;
if (typeof mulberry !== 'undefined') __e.mulberry = mulberry;
if (typeof hash !== 'undefined') __e.hash = hash;
if (typeof vnoise !== 'undefined') __e.vnoise = vnoise;
if (typeof TAU !== 'undefined') __e.TAU = TAU;
if (typeof monotone !== 'undefined') __e.monotone = monotone;
if (typeof track !== 'undefined') __e.track = track;
if (typeof env !== 'undefined') __e.env = env;
if (typeof a !== 'undefined') __e.a = a;
if (typeof b !== 'undefined') __e.b = b;
if (typeof s !== 'undefined') __e.s = s;
if (typeof k !== 'undefined') __e.k = k;
if (typeof z !== 'undefined') __e.z = z;
if (typeof f !== 'undefined') __e.f = f;
if (typeof u !== 'undefined') __e.u = u;
if (typeof fi !== 'undefined') __e.fi = fi;
if (typeof fo !== 'undefined') __e.fo = fo;
return __e;
})();
__M.knife = (() => {
// Woodcut engine · knife strokes
// A stroke is one cut of a carving tool: a centreline, a width per point, a tool profile, and (optionally)
// a reveal time so it can be carved "live" (the knife travels from the first point to the last).
//
//   stroke = { p: Float32Array [x0,y0,x1,y1,...], w: Float32Array [w0,w1,...] | number,
//              kind: 'v' | 'u' | 'k' | 'stab',   seed, t0, dur }
//
// Everything here draws onto a *mask* canvas: white = wood carved away (paper stays white in the print),
// black = wood left standing (takes ink). Use colour '#000' to "leave" wood (re-ink) on top of a cut area.
const { clamp, hash } = __M.lib;

// cheap 1-D value noise with seed
const vn = (x, s) => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); const a = hash(i * 1.37 + s * 17.1), b = hash((i + 1) * 1.37 + s * 17.1); return a + (b - a) * u; };

function mkStroke(pts, w, o = {}) {
  // pts: [[x,y],...] or flat array
  const p = pts.length && Array.isArray(pts[0]) ? Float32Array.from(pts.flat()) : Float32Array.from(pts);
  const n = p.length / 2;
  const ws = typeof w === 'number' ? new Float32Array(n).fill(w) : Float32Array.from(w);
  return { p, w: ws, kind: o.kind || 'v', seed: o.seed ?? (Math.abs(pts[0][0] * 12.9898 + pts[0][1] * 78.233) % 1000)  /* Zaman Kuryesi: Math.random yerine nokta özeti (işçiler arası belirlenimcilik) */, t0: o.t0 ?? -1e9, dur: o.dur ?? .2, chip: o.chip ?? .16 };
}

// resample a polyline [[x,y]...] so no segment is longer than `step`
function resample(pts, step = 3) {
  const out = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    const [ax, ay] = pts[i - 1], [bx, by] = pts[i], d = Math.hypot(bx - ax, by - ay), k = Math.max(1, Math.ceil(d / step));
    for (let j = 1; j <= k; j++) out.push([ax + (bx - ax) * j / k, ay + (by - ay) * j / k]);
  }
  return out;
}
// Catmull-Rom through control points → dense polyline
function spline(cp, step = 3, closed = false) {
  const P = closed ? [cp[cp.length - 1], ...cp, cp[0], cp[1]] : [cp[0], ...cp, cp[cp.length - 1]];
  const out = [];
  for (let i = 1; i < P.length - 2; i++) {
    const [p0, p1, p2, p3] = [P[i - 1], P[i], P[i + 1], P[i + 2]];
    const d = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]), k = Math.max(2, Math.ceil(d / step));
    for (let j = 0; j < k; j++) {
      const t = j / k, t2 = t * t, t3 = t2 * t;
      out.push([.5 * (2 * p1[0] + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
      .5 * (2 * p1[1] + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)]);
    }
  }
  out.push(closed ? P[P.length - 2] : cp[cp.length - 1]);
  return out;
}

// width multiplier of the tool along the cut. s = distance from start, L = total length, w = local width
function prof(kind, s, L, w) {
  if (kind === 'u') {
    const a = clamp(s / (.55 * w + .5)), b = clamp((L - s) / (.7 * w + .5));
    return Math.sqrt(1 - (1 - a) * (1 - a)) * Math.sqrt(1 - (1 - b) * (1 - b));
  }
  if (kind === 'k') return clamp(s / (1.5 * w + 1)) ** .5 * clamp((L - s) / (3 * w + 2)) ** .6;
  if (kind === 'stab') { const u = clamp(s / Math.max(L, .01)); return Math.sin(Math.PI * Math.min(1, u * 1.35)) ** .6 * (1 - .35 * u); }
  // 'v' gouge: fairly blunt entry, long pointed exit
  const a = clamp(s / (.9 * w + 1)), b = clamp((L - s) / (2.6 * w + 2));
  return (.35 + .65 * a * (2 - a)) * Math.pow(b, .75);
}

const _L = [], _R = [];
// append the outline of stroke `s` carved up to progress `pr` (0..1) to the current path of g
function strokePath(g, s, pr = 1) {
  const p = s.p, n = p.length / 2; if (n < 2 || pr <= 0) return 0;
  // cumulative length
  let L = 0; const cum = strokePath._c || (strokePath._c = new Float32Array(4096));
  const C = cum.length < n ? (strokePath._c = new Float32Array(n * 2)) : cum;
  C[0] = 0; for (let i = 1; i < n; i++) { L += Math.hypot(p[2 * i] - p[2 * i - 2], p[2 * i + 1] - p[2 * i - 1]); C[i] = L; }
  if (L < .5) return 0;
  const Lv = L * clamp(pr), live = pr < 1, tipL = 6;
  _L.length = 0; _R.length = 0;
  const ch = s.chip, sd = s.seed;
  for (let i = 0; i < n; i++) {
    let si = C[i], x = p[2 * i], y = p[2 * i + 1];
    if (si > Lv) {  // interpolate the live tip
      const f = (Lv - C[i - 1]) / Math.max(1e-6, si - C[i - 1]);
      x = p[2 * i - 2] + (x - p[2 * i - 2]) * f; y = p[2 * i - 1] + (y - p[2 * i - 1]) * f; si = Lv;
    }
    const i0 = Math.max(0, i - 1), i1 = Math.min(n - 1, i + 1);
    let tx = p[2 * i1] - p[2 * i0], ty = p[2 * i1 + 1] - p[2 * i0 + 1]; const tl = Math.hypot(tx, ty) || 1; tx /= tl; ty /= tl;
    const wi = s.w[i] ?? s.w[0];
    let hw = .5 * wi * prof(s.kind, si, live ? Math.max(Lv, Math.min(L, Lv + tipL)) : L, wi);
    if (live) hw *= Math.pow(clamp((Lv - si) / tipL + .15), .5);
    const el = 1 + ch * (vn(si * .21, sd) - .5) * 2 + ch * .8 * (vn(si * .9, sd + 3) - .5);
    const er = 1 + ch * (vn(si * .21, sd + 7) - .5) * 2 + ch * .8 * (vn(si * .9, sd + 11) - .5);
    _L.push(x - ty * hw * el, y + tx * hw * el); _R.push(x + ty * hw * er, y - tx * hw * er);
    if (si >= Lv) break;
  }
  const m = _L.length / 2; if (m < 2) return 0;
  g.moveTo(_L[0], _L[1]);
  for (let i = 1; i < m; i++) g.lineTo(_L[2 * i], _L[2 * i + 1]);
  for (let i = m - 1; i >= 0; i--) g.lineTo(_R[2 * i], _R[2 * i + 1]);
  g.closePath();
  return Lv;
}

// progress of a stroke at time t (knife moves with a slight ease-in)
const progOf = (s, t) => { const u = clamp((t - s.t0) / s.dur); return u < 1 ? u * (0.55 + 0.45 * u) : 1; };

// draw many strokes at time t in one fill. Returns list of live tips [{x,y,a,w}] (for chips / sound hooks)
function drawStrokes(g, list, { t = 1e9, color = '#fff', tips = null } = {}) {
  g.fillStyle = color; g.beginPath();
  for (const s of list) {
    const pr = progOf(s, t); if (pr <= 0) continue;
    const Lv = strokePath(g, s, pr);
    if (tips && pr < 1 && Lv > 0) tips.push(tipOf(s, Lv));
  }
  g.fill('nonzero');
}
function tipOf(s, Lv) {
  const p = s.p, n = p.length / 2; let L = 0;
  for (let i = 1; i < n; i++) {
    const d = Math.hypot(p[2 * i] - p[2 * i - 2], p[2 * i + 1] - p[2 * i - 1]);
    if (L + d >= Lv) { const f = (Lv - L) / (d || 1); return { x: p[2 * i - 2] + (p[2 * i] - p[2 * i - 2]) * f, y: p[2 * i - 1] + (p[2 * i + 1] - p[2 * i - 1]) * f, a: Math.atan2(p[2 * i + 1] - p[2 * i - 1], p[2 * i] - p[2 * i - 2]), w: s.w[i] ?? s.w[0], kind: s.kind }; }
    L += d;
  }
  return { x: p[2 * n - 2], y: p[2 * n - 1], a: 0, w: s.w[0], kind: s.kind };
}

// a curl of wood chip lifting at the knife tip (block world only)
function chip(g, tip, k = 1, col = '#fff') {
  const { x, y, a, w } = tip, r = Math.max(2.5, w * .9) * k;
  g.save(); g.translate(x, y); g.rotate(a);
  g.fillStyle = col; g.beginPath();
  g.moveTo(0, -r * .5); g.bezierCurveTo(r * 1.6, -r * 1.2, r * 2.2, r * .2, r * 1.2, r * .9);
  g.bezierCurveTo(r * 1.5, r * .1, r * 1.1, -r * .5, 0, r * .3); g.closePath(); g.fill();
  g.restore();
}

// bounding-box helpers
function strokeBounds(s) { let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; for (let i = 0; i < s.p.length; i += 2) { x0 = Math.min(x0, s.p[i]); x1 = Math.max(x1, s.p[i]); y0 = Math.min(y0, s.p[i + 1]); y1 = Math.max(y1, s.p[i + 1]); } return [x0, y0, x1, y1]; }
// transform a stroke list by a 2-D affine [a,b,c,d,e,f] (returns new strokes, widths scaled by sqrt|det|)
function xform(list, m) {
  const k = Math.sqrt(Math.abs(m[0] * m[3] - m[1] * m[2]));
  return list.map(s => { const p = new Float32Array(s.p.length); for (let i = 0; i < p.length; i += 2) { const x = s.p[i], y = s.p[i + 1]; p[i] = m[0] * x + m[2] * y + m[4]; p[i + 1] = m[1] * x + m[3] * y + m[5]; } return { ...s, p, w: s.w.map(v => v * k) }; });
}

const __e = {};
if (typeof mkStroke !== 'undefined') __e.mkStroke = mkStroke;
if (typeof resample !== 'undefined') __e.resample = resample;
if (typeof spline !== 'undefined') __e.spline = spline;
if (typeof strokePath !== 'undefined') __e.strokePath = strokePath;
if (typeof progOf !== 'undefined') __e.progOf = progOf;
if (typeof drawStrokes !== 'undefined') __e.drawStrokes = drawStrokes;
if (typeof chip !== 'undefined') __e.chip = chip;
if (typeof strokeBounds !== 'undefined') __e.strokeBounds = strokeBounds;
if (typeof xform !== 'undefined') __e.xform = xform;
return __e;
})();
__M.hatch = (() => {
// Woodcut engine · regions + flow-aligned hatching (white-line technique)
// A Region is a rasterised shape (mask + exact distance-to-edge field). From it we derive
//  - an "inflated" normal (the shape read as a soft relief) → tone from a light direction
//  - a contour direction (lines that wrap around the form, Doré-style)
// hatch() traces evenly spaced streamlines (Jobard–Lefer) along a direction field and turns them into
// knife strokes whose width follows the tone: bright = wide white cuts, dark = no cut (solid ink).
const { clamp, mulberry } = __M.lib;
const { mkStroke } = __M.knife;

// ---------- exact Euclidean distance transform (Felzenszwalb) ----------
function edt1(f, n, d, v, z) {
  let k = 0; v[0] = 0; z[0] = -1e20; z[1] = 1e20;
  for (let q = 1; q < n; q++) {
    let s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]);
    while (s <= z[k]) { k--; s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k]); }
    k++; v[k] = q; z[k] = s; z[k + 1] = 1e20;
  }
  k = 0; for (let q = 0; q < n; q++) { while (z[k + 1] < q) k++; d[q] = (q - v[k]) * (q - v[k]) + f[v[k]]; }
}
function edt(grid, W, H) {   // grid: 0 at sources, INF elsewhere → squared distances (in place)
  const n = Math.max(W, H), f = new Float64Array(n), d = new Float64Array(n), v = new Int32Array(n), z = new Float64Array(n + 1);
  for (let x = 0; x < W; x++) { for (let y = 0; y < H; y++) f[y] = grid[y * W + x]; edt1(f, H, d, v, z); for (let y = 0; y < H; y++) grid[y * W + x] = d[y]; }
  for (let y = 0; y < H; y++) { for (let x = 0; x < W; x++) f[x] = grid[y * W + x]; edt1(f, W, d, v, z); for (let x = 0; x < W; x++) grid[y * W + x] = d[x]; }
}

let _cv = null;
function scratch(w, h) { if (!_cv) _cv = document.createElement('canvas'); if (_cv.width < w || _cv.height < h) { _cv.width = Math.max(w, _cv.width); _cv.height = Math.max(h, _cv.height); } const q = _cv.getContext('2d', { willReadFrequently: true }); q.setTransform(1, 0, 0, 1, 0, 0); q.clearRect(0, 0, _cv.width, _cv.height); return q; }

// polys: array of polygons, each [[x,y],...] (even-odd fill → holes allowed), or a function(q) that fills a path on q
class Region {
  constructor(polys, { res = 2, pad = 6, bbox = null } = {}) {
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    if (bbox) [x0, y0, x1, y1] = bbox;
    else for (const P of polys) for (const [x, y] of P) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
    x0 -= pad * res; y0 -= pad * res; x1 += pad * res; y1 += pad * res;
    const W = Math.max(2, Math.ceil((x1 - x0) / res)), H = Math.max(2, Math.ceil((y1 - y0) / res));
    Object.assign(this, { x0, y0, res, W, H, bbox: [x0, y0, x1, y1] });
    const q = scratch(W, H);
    q.setTransform(1 / res, 0, 0, 1 / res, -x0 / res, -y0 / res);
    q.fillStyle = '#fff'; q.beginPath();
    if (typeof polys === 'function') polys(q); else for (const P of polys) { q.moveTo(P[0][0], P[0][1]); for (let i = 1; i < P.length; i++) q.lineTo(P[i][0], P[i][1]); q.closePath(); }
    q.fill('evenodd');
    const id = q.getImageData(0, 0, W, H).data, m = new Uint8Array(W * H);
    for (let i = 0; i < W * H; i++) m[i] = id[i * 4 + 3] > 127 ? 1 : 0;
    this.m = m;
    // inside distance to the edge (px)
    const g = new Float64Array(W * H); for (let i = 0; i < W * H; i++) g[i] = m[i] ? 1e20 : 0;
    edt(g, W, H); const D = new Float32Array(W * H); for (let i = 0; i < W * H; i++) D[i] = Math.sqrt(g[i]) * res;
    // smooth a little so the gradient is clean
    this.D = blur(D, W, H, 2);
  }
  _i(x, y) { return [(x - this.x0) / this.res, (y - this.y0) / this.res]; }
  inside(x, y) { const i = Math.floor((x - this.x0) / this.res), j = Math.floor((y - this.y0) / this.res); return i >= 0 && j >= 0 && i < this.W && j < this.H && this.m[j * this.W + i] === 1; }
  dist(x, y) {
    let [u, v] = this._i(x, y); u = clamp(u - .5, 0, this.W - 1.001); v = clamp(v - .5, 0, this.H - 1.001);
    const i = Math.floor(u), j = Math.floor(v), f = u - i, e = v - j, W = this.W, D = this.D;
    return (D[j * W + i] * (1 - f) + D[j * W + i + 1] * f) * (1 - e) + (D[(j + 1) * W + i] * (1 - f) + D[(j + 1) * W + i + 1] * f) * e;
  }
  grad(x, y) { const h = this.res * 1.5; const gx = this.dist(x + h, y) - this.dist(x - h, y), gy = this.dist(x, y + h) - this.dist(x, y - h); const l = Math.hypot(gx, gy); return l < 1e-5 ? [0, 0, 0] : [gx / l, gy / l, l / (2 * h)]; }
  // "inflated" relief normal: height h(d) = R·sqrt(1-(1-d/R)^2) → round edges, flat top
  normal(x, y, R = 60) {
    const d = this.dist(x, y), [gx, gy, gl] = this.grad(x, y);
    const u = clamp(d / R), s = Math.max(.08, Math.sqrt(1 - (1 - u) * (1 - u))), dh = clamp((1 - u) / s, 0, 6) * clamp(gl);
    const nx = -gx * dh, ny = -gy * dh, nz = 1, l = Math.hypot(nx, ny, nz);
    return [nx / l, ny / l, nz / l];
  }
}
function blur(A, W, H, r) {
  const B = new Float32Array(W * H), C = new Float32Array(W * H), k = 2 * r + 1;
  for (let y = 0; y < H; y++) { let s = 0; for (let x = -r; x <= r; x++) s += A[y * W + clamp(x, 0, W - 1)]; for (let x = 0; x < W; x++) { B[y * W + x] = s / k; s += A[y * W + Math.min(W - 1, x + r + 1)] - A[y * W + Math.max(0, x - r)]; } }
  for (let x = 0; x < W; x++) { let s = 0; for (let y = -r; y <= r; y++) s += B[clamp(y, 0, H - 1) * W + x]; for (let y = 0; y < H; y++) { C[y * W + x] = s / k; s += B[Math.min(H - 1, y + r + 1) * W + x] - B[Math.max(0, y - r) * W + x]; } }
  return C;
}

// ---------- tone helpers ----------
const light = (lx, ly, lz) => { const l = Math.hypot(lx, ly, lz); return [lx / l, ly / l, lz / l]; };
// lambert tone on the inflated relief of a region
function reliefTone(reg, L, { R = 60, amb = .1, k = 1, rim = 0 } = {}) {
  return (x, y) => { const n = reg.normal(x, y, R); const d = n[0] * L[0] + n[1] * L[1] + n[2] * L[2]; return clamp(amb + k * Math.max(0, d) + rim * (1 - n[2])); };
}

// ---------- direction fields ----------
const dirAngle = a => () => a;
const dirRadial = (cx, cy) => (x, y) => Math.atan2(y - cy, x - cx);
const dirRing = (cx, cy, sy = 1) => (x, y) => Math.atan2((y - cy) / sy, x - cx) + Math.PI / 2;
// lines parallel to the region outline; deep inside, blend towards `a0`
const dirContour = (reg, a0 = 0, depth = 40) => (x, y) => {
  const [gx, gy, gl] = reg.grad(x, y), w = clamp(1 - reg.dist(x, y) / depth) * clamp(gl * 3);
  const cx = -gy, cy = gx, ax = Math.cos(a0), ay = Math.sin(a0);
  const sgn = cx * ax + cy * ay < 0 ? -1 : 1;
  return Math.atan2(w * cy * sgn + (1 - w) * ay, w * cx * sgn + (1 - w) * ax);
};

// ---------- streamline hatching ----------
// o: { dir(x,y)→angle, tone(x,y)→0..1, sp, wmax, lo, hi, gamma, step, seg:[min,max], gap:[min,max], kind,
//      minLen, maxLen, dtest, seed, reveal:{t0,t1,key(x,y)→0..1,speed,jit} , wmin, jit }
function hatch(reg, o = {}) {
  const sp = o.sp ?? 9, h = o.step ?? Math.max(1.5, sp * .28), dtest = sp * (o.dtest ?? .6);
  const dir = o.dir || dirAngle(0), tone = o.tone || (() => .5);
  const wmax = o.wmax ?? sp * .95, lo = o.lo ?? .18, hi = o.hi ?? .95, gam = o.gamma ?? 1, wmin = o.wmin ?? Math.max(.8, sp * .08);
  const rnd = mulberry(o.seed ?? 7), minLen = o.minLen ?? sp * 1.2, maxLen = o.maxLen ?? 4000;
  const seg = o.seg || [sp * 4, sp * 16], gap = o.gap || [1.5, sp * .5];
  const [bx0, by0, bx1, by1] = reg.bbox, cs = dtest, GW = Math.ceil((bx1 - bx0) / cs) + 1, GH = Math.ceil((by1 - by0) / cs) + 1;
  const grid = new Array(GW * GH);
  const lines = [];
  const near = (x, y, dd, id) => {
    const gi = Math.floor((x - bx0) / cs), gj = Math.floor((y - by0) / cs), r = Math.ceil(dd / cs), d2 = dd * dd;
    for (let j = gj - r; j <= gj + r; j++) { if (j < 0 || j >= GH) continue; for (let i = gi - r; i <= gi + r; i++) { if (i < 0 || i >= GW) continue; const c = grid[j * GW + i]; if (!c) continue; for (let k = 0; k < c.length; k += 3) { if (c[k + 2] === id) continue; const dx = c[k] - x, dy = c[k + 1] - y; if (dx * dx + dy * dy < d2) return true; } } }
    return false;
  };
  const addPt = (x, y, id) => { const gi = Math.floor((x - bx0) / cs), gj = Math.floor((y - by0) / cs); if (gi < 0 || gj < 0 || gi >= GW || gj >= GH) return; const k = gj * GW + gi; (grid[k] || (grid[k] = [])).push(x, y, id); };
  const jit = o.jit ?? 0;
  const dirAt = (x, y) => dir(x, y) + (jit ? jit * (Math.sin(x * .031 + y * .017) + Math.sin(x * .013 - y * .027)) * .5 : 0);
  const trace = (sx, sy, id) => {
    const half = sgn => {
      const out = []; let x = sx, y = sy, a = dirAt(x, y), px = Math.cos(a) * sgn, py = Math.sin(a) * sgn, len = 0;
      for (let it = 0; it < 20000; it++) {
        let a1 = dirAt(x, y), vx = Math.cos(a1), vy = Math.sin(a1); if (vx * px + vy * py < 0) { vx = -vx; vy = -vy; }
        const mx = x + vx * h * .5, my = y + vy * h * .5; let a2 = dirAt(mx, my), wx = Math.cos(a2), wy = Math.sin(a2); if (wx * vx + wy * vy < 0) { wx = -wx; wy = -wy; }
        const nx = x + wx * h, ny = y + wy * h;
        if (!reg.inside(nx, ny) || near(nx, ny, dtest, id)) break;
        if (len > 30 && Math.hypot(nx - sx, ny - sy) < h * 1.5) break;   // closed loop
        x = nx; y = ny; px = wx; py = wy; len += h; out.push([x, y]); if (len > maxLen * .5) break;
      }
      return out;
    };
    const f = half(1), b = half(-1);
    return [...b.reverse(), [sx, sy], ...f];
  };
  const queue = [];
  const tryLine = (sx, sy) => {
    if (!reg.inside(sx, sy) || near(sx, sy, sp * .92, -1)) return;
    const id = lines.length, L = trace(sx, sy, id);
    if (L.length * h < minLen) return;
    lines.push(L); for (const [x, y] of L) addPt(x, y, id);
    for (let k = 0; k < L.length; k += 3) {
      const i0 = Math.max(0, k - 1), i1 = Math.min(L.length - 1, k + 1); let tx = L[i1][0] - L[i0][0], ty = L[i1][1] - L[i0][1]; const tl = Math.hypot(tx, ty) || 1; tx /= tl; ty /= tl;
      queue.push([L[k][0] - ty * sp, L[k][1] + tx * sp], [L[k][0] + ty * sp, L[k][1] - tx * sp]);
    }
  };
  // coarse seed grid (random order) + neighbour seeding
  const seeds = [];
  for (let y = by0 + sp * .5; y < by1; y += sp * 2.2) for (let x = bx0 + sp * .5; x < bx1; x += sp * 2.2) seeds.push([x + (rnd() - .5) * sp, y + (rnd() - .5) * sp]);
  for (let i = seeds.length - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [seeds[i], seeds[j]] = [seeds[j], seeds[i]]; }
  if (o.seedAt) seeds.unshift(...o.seedAt);
  for (const s of seeds) { tryLine(s[0], s[1]); while (queue.length) { const q = queue.shift(); tryLine(q[0], q[1]); } }

  if (o.debug) console.warn('hatch lines', lines.length, seeds.length, lines.reduce((a, l) => a + l.length, 0));
  // lines → knife strokes, width from tone, broken into cut lengths
  const out = [], rv = o.reveal, kind = o.kind || 'v';
  for (const L of lines) {
    let cur = [], cw = [], acc = 0, target = seg[0] + rnd() * (seg[1] - seg[0]), skip = 0;
    const flush = () => {
      if (cur.length >= 3) {
        const s = mkStroke(cur, cw, { kind, seed: rnd() * 1000, chip: o.chip ?? .16 });
        if (rv) {
          const a = cur[0], b = cur[cur.length - 1], ka = rv.key(a[0], a[1]), kb = rv.key(b[0], b[1]);
          if (kb < ka && !rv.keepDir) { s.p = Float32Array.from(cur.slice().reverse().flat()); s.w = Float32Array.from(cw.slice().reverse()); }
          const k0 = Math.min(ka, kb);
          s.t0 = rv.t0 + clamp(k0 + (rnd() - .5) * (rv.jit ?? .08)) * (rv.t1 - rv.t0);
          s.dur = Math.max(.04, acc / (rv.speed ?? 900));
        }
        out.push(s);
      }
      cur = []; cw = []; acc = 0; target = seg[0] + rnd() * (seg[1] - seg[0]);
    };
    for (let i = 0; i < L.length; i++) {
      const [x, y] = L[i];
      if (skip > 0) { skip -= h; continue; }
      const t = tone(x, y), u = clamp((t - lo) / (hi - lo)), w = wmax * Math.pow(u, gam);
      if (w < wmin) { flush(); continue; }
      cur.push([x, y]); cw.push(w); if (cur.length > 1) acc += h;
      if (acc > target) { flush(); skip = gap[0] + rnd() * (gap[1] - gap[0]); }
    }
    flush();
  }
  return out;
}

// straight parallel lines clipped to a region (fast path for skies / planks); widths from tone
function lines(reg, o = {}) { return hatch(reg, { ...o, dir: dirAngle(o.angle ?? 0) }); }

const __e = {};
if (typeof Region !== 'undefined') __e.Region = Region;
if (typeof light !== 'undefined') __e.light = light;
if (typeof reliefTone !== 'undefined') __e.reliefTone = reliefTone;
if (typeof dirAngle !== 'undefined') __e.dirAngle = dirAngle;
if (typeof dirRadial !== 'undefined') __e.dirRadial = dirRadial;
if (typeof dirRing !== 'undefined') __e.dirRing = dirRing;
if (typeof dirContour !== 'undefined') __e.dirContour = dirContour;
if (typeof hatch !== 'undefined') __e.hatch = hatch;
if (typeof lines !== 'undefined') __e.lines = lines;
if (typeof sy !== 'undefined') __e.sy = sy;
if (typeof a0 !== 'undefined') __e.a0 = a0;
if (typeof depth !== 'undefined') __e.depth = depth;
return __e;
})();
__M.print = (() => {
// Woodcut engine · printing compositor (WebGL2)
// Takes the carve MASK (white = cut away, black = wood left standing) and an optional COLOUR PLATE
// (alpha = plate density) and turns them into either
//   mode 'print': black ink pulled onto laid paper — ragged knife edges, uneven ink, wood-grain streaks,
//                 specks where the ink didn't take, the colour plate overprinted with its own mottle and
//                 a fixed misregistration;
//   mode 'block': the inked wood block itself — glossy black surface with grain sheen, pale wood in the
//                 cuts with groove shading.
const VS = `#version 300 es
in vec2 p; void main(){ gl_Position = vec4(p,0.,1.); }`;
const FS = `#version 300 es
precision highp float;
uniform sampler2D M, C; uniform vec2 R; uniform float mode, seed, inkSeed, edge, plateAmt, inkAmt, grainAng, sheen;
uniform vec2 reg; uniform float wetX; uniform vec3 paperC, inkC, plateC, woodC;
out vec4 o;
float h21(vec2 p){ p = fract(p*vec2(123.34, 456.21)); p += dot(p, p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h21(i),h21(i+vec2(1,0)),f.x), mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),f.x), f.y); }
float fbm(vec2 p){ float s=0., a=.5; for(int i=0;i<4;i++){ s+=a*vn(p); p=p*2.03+17.1; a*=.5; } return s; }
mat2 rot(float a){ float c=cos(a), s=sin(a); return mat2(c,-s,s,c); }
void main(){
  vec2 px = vec2(gl_FragCoord.x, R.y - gl_FragCoord.y);
  vec2 sp = px + seed*97.;             // paper-anchored noise
  vec2 ip = px + inkSeed*131.;         // per-impression noise (can step at 12 fps)
  // ragged knife edge: displace the lookup, then threshold with noise
  vec2 d = (vec2(vn(ip*.33), vn(ip*.33+19.7)) - .5) * 2.6 * edge + (vec2(vn(ip*1.3+5.), vn(ip*1.3+9.)) - .5) * 1.1 * edge;
  float m = texture(M, (px + d) / R).r;
  float th = .5 + (vn(ip*.7+3.) - .5) * .34 * edge;
  float cut = smoothstep(th - .1, th + .1, m);
  float ink = 1. - cut;
  vec3 col;
  if (mode < .5) {
    // ---- paper ----
    float cloud = fbm(sp*.0035) - .5, fib = vn(rot(.35)*sp*vec2(.9,.035)) + vn(rot(-.8)*sp*vec2(.7,.03)) - 1.;
    vec3 paper = paperC * (1. + .05*cloud + .022*fib + .018*(h21(sp)-.5));
    // colour plate (misregistered), mottled, overprints paper where the wood was cut
    float c = texture(C, (px - reg) / R).a;
    float cm = c * (.8 + .28*fbm(ip*.02+4.)) * plateAmt;
    cm *= 1. - .35*smoothstep(.6,.9, vn(ip*.25+2.)) ;
    vec3 base = mix(paper, paper * plateC / paperC, clamp(cm,0.,1.));
    // ---- ink ----
    vec2 gp = rot(grainAng) * ip;
    float dens = .965 + .035*(fbm(ip*.004)-.5)*2.;
    dens -= .045 * smoothstep(.62, .9, vn(gp*vec2(.0035, .7)));                   // wood grain streaks
    dens -= .55 * smoothstep(.84, .92, vn(ip*.5)) * smoothstep(.4, .8, fbm(ip*.007)); // specks that didn't take
    dens = clamp(dens * inkAmt, 0., 1.);
    vec3 inkT = inkC * mix(vec3(1.), plateC / paperC, .18 * clamp(cm, 0., 1.));    // black over the plate: warm black
    col = mix(base, inkT, ink * dens);
  } else {
    // ---- the inked block ----
    vec2 gp = rot(grainAng) * px;
    float grain = vn(gp*vec2(.003, .09)) * .6 + vn(gp*vec2(.01, .35)) * .4;
    vec3 wood = woodC * (.86 + .2*grain) * (1. + .04*(h21(px)-.5));
    float mb = textureLod(M, px / R, 2.2).r;                              // blurred mask → groove depth
    vec2 gm = vec2(textureLod(M, (px+vec2(3,0))/R, 2.).r - textureLod(M, (px-vec2(3,0))/R, 2.).r,
                   textureLod(M, (px+vec2(0,3))/R, 2.).r - textureLod(M, (px-vec2(0,3))/R, 2.).r);
    wood *= .62 + .38*smoothstep(.25, .95, mb);
    wood *= 1. + .5*clamp(dot(gm, vec2(-.7,-.7)), -.5, .5);               // lit / shaded groove walls
    float sh = pow(vn(gp*vec2(.0022, .3)), 3.) * sheen * .6 + .25*sheen*smoothstep(0., 1., 1. - length((px - vec2(.25,.2)*R)/R));
    float wet = smoothstep(wetX + 40., wetX - 60., px.x) * step(0., wetX);
    sh += wet * (.05 + .22 * pow(vn(gp*vec2(.004, .02) + 3.), 2.));
    vec3 surf = inkC * (1. + .18*grain) + vec3(sh);
    col = mix(wood, surf, ink);
  }
  o = vec4(col, 1.);
}`;
const hex = s => { const n = parseInt(s.slice(1), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255]; };

function makePrinter(W = 1920, H = 1080) {
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
  const gl = cv.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false, premultipliedAlpha: false });
  if (!gl) throw new Error('webgl2 unavailable');
  const sh = (t, s) => { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(x)); return x; };
  const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr));
  gl.useProgram(pr);
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const tex = u => { const t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + u); gl.bindTexture(gl.TEXTURE_2D, t); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); return t; };
  const tM = tex(0), tC = tex(1);
  const U = n => gl.getUniformLocation(pr, n);
  gl.uniform1i(U('M'), 0); gl.uniform1i(U('C'), 1); gl.uniform2f(U('R'), W, H);
  const blank = document.createElement('canvas'); blank.width = 4; blank.height = 4;
  function upload(u, t, c) { gl.activeTexture(gl.TEXTURE0 + u); gl.bindTexture(gl.TEXTURE_2D, t); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, c); gl.generateMipmap(gl.TEXTURE_2D); }
  return {
    canvas: cv,
    // mask: canvas (white = cut), color: canvas with alpha = plate density (or null)
    render(mask, color, o = {}) {
      gl.viewport(0, 0, W, H);
      upload(0, tM, mask); upload(1, tC, color || blank);
      gl.uniform1f(U('mode'), o.mode === 'block' ? 1 : 0);
      gl.uniform1f(U('seed'), o.seed ?? 1); gl.uniform1f(U('inkSeed'), o.inkSeed ?? o.seed ?? 1);
      gl.uniform1f(U('edge'), o.edge ?? 1); gl.uniform1f(U('plateAmt'), o.plateAmt ?? 1); gl.uniform1f(U('inkAmt'), o.inkAmt ?? 1);
      gl.uniform1f(U('grainAng'), o.grainAng ?? 0); gl.uniform1f(U('sheen'), o.sheen ?? .12);
      gl.uniform2f(U('reg'), ...(o.reg || [3, 2])); gl.uniform1f(U('wetX'), o.wetX ?? -1);
      gl.uniform3f(U('paperC'), ...hex(o.paper || '#EFE8D8')); gl.uniform3f(U('inkC'), ...hex(o.ink || '#111111'));
      gl.uniform3f(U('plateC'), ...hex(o.plate || '#C8502A')); gl.uniform3f(U('woodC'), ...hex(o.wood || '#D8C29C'));
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      return cv;
    }
  };
}

const __e = {};
if (typeof makePrinter !== 'undefined') __e.makePrinter = makePrinter;
return __e;
})();
__M.filter = (() => {
// Woodcut engine · image / video-frame → woodcut filter
// Luminance decides how wide each white cut is (bright = wide), the structure tensor of the image decides
// which way the cuts run (along the isophotes, i.e. around the forms, like an engraver follows a cheek).
// Returns knife strokes in target space, each with a reveal time, so the frame can be "carved" live.
//
//   const F = woodcutFilter(img, { rect:[x,y,w,h], sp: 6 });   // → { strokes, tone(x,y), dir(x,y) }
//   drawStrokes(maskCtx, F.strokes, { t })                      // mask pre-filled black
const { clamp } = __M.lib;
const { Region, hatch } = __M.hatch;

function boxBlur(A, W, H, r) {
  if (r < 1) return A;
  const B = new Float32Array(W * H), C = new Float32Array(W * H), k = 2 * r + 1;
  for (let y = 0; y < H; y++) { let s = 0; for (let x = -r; x <= r; x++) s += A[y * W + clamp(x, 0, W - 1)]; for (let x = 0; x < W; x++) { B[y * W + x] = s / k; s += A[y * W + Math.min(W - 1, x + r + 1)] - A[y * W + Math.max(0, x - r)]; } }
  for (let x = 0; x < W; x++) { let s = 0; for (let y = -r; y <= r; y++) s += B[clamp(y, 0, H - 1) * W + x]; for (let y = 0; y < H; y++) { C[y * W + x] = s / k; s += B[Math.min(H - 1, y + r + 1) * W + x] - B[Math.max(0, y - r) * W + x]; } }
  return C;
}
const blur = (A, W, H, r) => boxBlur(boxBlur(A, W, H, r), W, H, r);   // ≈ gaussian

// src: image / canvas / video frame. o: { rect:[x,y,w,h] target, res (px per analysis cell), sp, wmax, lo, hi, gamma,
//   black, white (levels), a0 (fallback angle), tensor (blur radius, cells), coh, seg, gap, kind, seed,
//   reveal: { t0, t1, mode:'light'|'radial'|'down'|fn, cx, cy, speed, jit } }
function woodcutFilter(src, o = {}) {
  const [rx, ry, rw, rh] = o.rect || [0, 0, 1920, 1080], res = o.res ?? 3;
  const W = Math.max(8, Math.round(rw / res)), H = Math.max(8, Math.round(rh / res));
  const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
  const q = cv.getContext('2d', { willReadFrequently: true });
  // cover-fit the source into the rect
  const sw = src.videoWidth || src.naturalWidth || src.width, sh = src.videoHeight || src.naturalHeight || src.height;
  const k = Math.max(W / sw, H / sh), dw = sw * k, dh = sh * k;
  q.drawImage(src, (W - dw) / 2 + (o.shift?.[0] ?? 0) / res, (H - dh) / 2 + (o.shift?.[1] ?? 0) / res, dw, dh);
  const id = q.getImageData(0, 0, W, H).data, Lr = new Float32Array(W * H);
  for (let i = 0; i < W * H; i++) Lr[i] = (.2126 * id[4 * i] + .7152 * id[4 * i + 1] + .0722 * id[4 * i + 2]) / 255;
  const L = blur(Lr, W, H, o.pre ?? 1);
  // levels
  const bk = o.black ?? .08, wt = o.white ?? .85, gm = o.gamma ?? 1;
  const T = new Float32Array(W * H); for (let i = 0; i < W * H; i++) T[i] = Math.pow(clamp((L[i] - bk) / (wt - bk)), gm);
  // structure tensor
  const Jxx = new Float32Array(W * H), Jxy = new Float32Array(W * H), Jyy = new Float32Array(W * H);
  for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
    const i = y * W + x, a = L[i - W - 1], b = L[i - W], c = L[i - W + 1], d = L[i - 1], f = L[i + 1], g = L[i + W - 1], h = L[i + W], j = L[i + W + 1];
    const gx = (c + 2 * f + j) - (a + 2 * d + g), gy = (g + 2 * h + j) - (a + 2 * b + c);
    Jxx[i] = gx * gx; Jxy[i] = gx * gy; Jyy[i] = gy * gy;
  }
  const tr = o.tensor ?? 4, bxx = blur(Jxx, W, H, tr), bxy = blur(Jxy, W, H, tr), byy = blur(Jyy, W, H, tr);
  // doubled-angle field (cos2θ, sin2θ) of the isophote direction, blended to a0 where incoherent
  const a0 = o.a0 ?? .45, C2 = new Float32Array(W * H), S2 = new Float32Array(W * H), cohK = o.coh ?? 1;
  let mx = 1e-9; for (let i = 0; i < W * H; i++) mx = Math.max(mx, bxx[i] + byy[i]);
  // (box blurs can leave tiny negative sums in flat areas → clamp before sqrt)
  for (let i = 0; i < W * H; i++) {
    const a = Math.max(0, bxx[i]), b = bxy[i], c = Math.max(0, byy[i]), tr2 = a + c, det = Math.sqrt((a - c) * (a - c) + 4 * b * b);
    const coh = tr2 > 1e-9 ? Math.min(1, det / tr2) : 0, str = clamp(Math.sqrt(tr2 / mx) * 6);
    const th = .5 * Math.atan2(2 * b, a - c) + Math.PI / 2;           // along the edge
    const w = clamp(coh * str * cohK);
    C2[i] = w * Math.cos(2 * th) + (1 - w) * Math.cos(2 * a0); S2[i] = w * Math.sin(2 * th) + (1 - w) * Math.sin(2 * a0);
  }
  const sm = o.smooth ?? 2, C2b = blur(C2, W, H, sm), S2b = blur(S2, W, H, sm);
  const samp = (A, x, y) => { let u = (x - rx) / res - .5, v = (y - ry) / res - .5; u = clamp(u, 0, W - 1.001); v = clamp(v, 0, H - 1.001); const i = Math.floor(u), j = Math.floor(v), fu = u - i, fv = v - j; return (A[j * W + i] * (1 - fu) + A[j * W + i + 1] * fu) * (1 - fv) + (A[(j + 1) * W + i] * (1 - fu) + A[(j + 1) * W + i + 1] * fu) * fv; };
  const tone = (x, y) => samp(T, x, y);
  const dir = (x, y) => .5 * Math.atan2(samp(S2b, x, y), samp(C2b, x, y));
  const reg = o.region || new Region([[[rx, ry], [rx + rw, ry], [rx + rw, ry + rh], [rx, ry + rh]]], { res: 4, pad: 1 });
  let reveal = null;
  if (o.reveal) {
    const r = o.reveal, mode = r.mode || 'light';
    const key = typeof mode === 'function' ? mode
      : mode === 'radial' ? (x, y) => clamp(Math.hypot(x - (r.cx ?? rx + rw / 2), y - (r.cy ?? ry + rh / 2)) / (Math.hypot(rw, rh) * .55))
        : mode === 'down' ? (x, y) => clamp((y - ry) / rh)
          : (x, y) => clamp(1 - tone(x, y)) * .85 + .15 * clamp((y - ry) / rh);   // lights first ("coarse to fine")
    reveal = { t0: r.t0 ?? 0, t1: r.t1 ?? 1, key, speed: r.speed ?? 1200, jit: r.jit ?? .06 };
  }
  const sp = o.sp ?? 6;
  const strokes = hatch(reg, { dir, tone, sp, wmax: o.wmax ?? sp * 1.02, lo: o.lo ?? .12, hi: o.hi ?? 1, gamma: o.lineGamma ?? .9, seg: o.seg || [sp * 5, sp * 22], gap: o.gap || [1, sp * .6], kind: o.kind || 'v', seed: o.seed ?? 3, reveal, step: o.step, dtest: o.dtest ?? .62, jit: o.jit ?? 0, debug: o.debug });
  return { strokes, tone, dir, W, H };
}

const __e = {};
if (typeof woodcutFilter !== 'undefined') __e.woodcutFilter = woodcutFilter;
return __e;
})();
__M.index = (() => {
// Woodcut engine · public API
// Draw anything as a relief print: shapes become black wood with white knife cuts that follow the form,
// light is literally carved (bright = wide cuts), and the result is printed by the WebGL compositor.
//
//   const P = WC.makePrinter();                 // once
//   const S = WC.shape([[..poly..]], { light: WC.light(.5,-.7,.6), sp: 8, halo: 6 });
//   mask: fill black (uncut block), S.draw(g, t) ... ; color plate: WC.plate(c, poly)
//   const out = P.render(maskCanvas, colorCanvas, { mode: 'print' });   // → canvas
const { clamp, mulberry } = __M.lib;
const { mkStroke, spline, resample, drawStrokes, strokePath, progOf, chip, xform } = __M.knife;
const { Region, hatch, lines, reliefTone, light, dirAngle, dirRadial, dirRing, dirContour } = __M.hatch;
const { makePrinter } = __M.print;
const { woodcutFilter } = __M.filter;


const INK = '#111111', PAPER = '#EFE8D8', COPPER = '#C8502A', WOOD = '#D8C29C';

function canvas(w = 1920, h = 1080) { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; }
function pathOf(g, P, close = true) { g.moveTo(P[0][0], P[0][1]); for (let i = 1; i < P.length; i++) g.lineTo(P[i][0], P[i][1]); if (close) g.closePath(); }
function fillPoly(g, polys, col = '#000', rule = 'evenodd') { g.fillStyle = col; g.beginPath(); for (const P of polys) pathOf(g, P); g.fill(rule); }

// offset a closed polygon along its vertex normals (d > 0 = outward for counter-clockwise… we auto-detect)
function offsetPoly(P, d) {
  let A = 0; for (let i = 0; i < P.length; i++) { const [x0, y0] = P[i], [x1, y1] = P[(i + 1) % P.length]; A += x0 * y1 - x1 * y0; }
  const sgn = A > 0 ? -1 : 1, n = P.length;
  return P.map((p, i) => { const a = P[(i - 1 + n) % n], b = P[(i + 1) % n]; let tx = b[0] - a[0], ty = b[1] - a[1]; const l = Math.hypot(tx, ty) || 1; tx /= l; ty /= l; return [p[0] + ty * d * sgn, p[1] - tx * d * sgn]; });
}

// break a (closed or open) path into hand-cut knife strokes. o: {w, kind, seg:[a,b], gap:[a,b], seed, jw, reveal:{t0,t1,speed}}
function cutAlong(P, o = {}) {
  const rnd = mulberry(o.seed ?? 3), pts = resample(o.closed ? [...P, P[0]] : P, o.step ?? 3);
  const seg = o.seg || [40, 140], gap = o.gap || [1, 5], w = o.w ?? 3, jw = o.jw ?? .25;
  const out = []; let cur = [], cw = [], acc = 0, target = seg[0] + rnd() * (seg[1] - seg[0]), skip = 0, total = 0, startLen = 0;
  const L = []; let s = 0; for (let i = 0; i < pts.length; i++) { if (i) s += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); L.push(s); }
  const TL = s || 1;
  const flush = () => {
    if (cur.length >= 2) {
      const st = mkStroke(cur, cw, { kind: o.kind || 'v', seed: rnd() * 1000, chip: o.chip ?? .14 });
      if (o.reveal) { const r = o.reveal; st.t0 = r.t0 + (startLen / TL) * (r.t1 - r.t0); st.dur = Math.max(.03, acc / (r.speed ?? 900)); }
      out.push(st);
    }
    cur = []; cw = []; acc = 0; target = seg[0] + rnd() * (seg[1] - seg[0]);
  };
  const wf = typeof w === 'function' ? w : () => w;
  const wv = 1 + (rnd() - .5) * jw * 2;
  for (let i = 0; i < pts.length; i++) {
    const step = i ? L[i] - L[i - 1] : 0;
    if (skip > 0) { skip -= step; continue; }
    if (!cur.length) startLen = L[i];
    cur.push(pts[i]); cw.push(wf(L[i] / TL, pts[i]) * wv); acc += step;
    if (acc > target) { flush(); skip = gap[0] + rnd() * (gap[1] - gap[0]); }
  }
  flush();
  return out;
}

// snow / stipple: short stab cuts. pts [[x,y,r?],...]
function flecks(pts, o = {}) {
  const rnd = mulberry(o.seed ?? 11), r0 = o.r ?? 3, ang = o.angle ?? 1.2;
  return pts.map(([x, y, r = r0]) => {
    const a = ang + (rnd() - .5) * .9, L = r * (1.4 + rnd() * .9);
    const s = mkStroke([[x - Math.cos(a) * L * .5, y - Math.sin(a) * L * .5], [x, y], [x + Math.cos(a) * L * .5, y + Math.sin(a) * L * .5]], r * 1.25, { kind: 'stab', seed: rnd() * 1000, chip: .2 });
    s.x = x; s.y = y; s.r = r; return s;
  });
}

// radial burst of carved rays (light made of cuts). o: {n, r0, r1:[a,b], w, jit, seed, a0, a1, kind, reveal:{t0,t1}}
function rays(cx, cy, o = {}) {
  const rnd = mulberry(o.seed ?? 5), n = o.n ?? 40, a0 = o.a0 ?? 0, a1 = o.a1 ?? Math.PI * 2, out = [];
  for (let i = 0; i < n; i++) {
    const a = a0 + (a1 - a0) * (i + .5 + (rnd() - .5) * (o.jit ?? .6)) / n;
    const r0 = (o.r0 ?? 40) * (.8 + rnd() * .5), r1 = (o.r1 ? o.r1[0] + rnd() * (o.r1[1] - o.r1[0]) : 600);
    const wv = (o.w ?? 14) * (.6 + rnd() * .8), bend = (rnd() - .5) * (o.bend ?? .05);
    const pts = []; const N = Math.max(4, Math.ceil((r1 - r0) / 8));
    for (let k = 0; k <= N; k++) { const u = k / N, r = r0 + (r1 - r0) * u, aa = a + bend * u * u; pts.push([cx + Math.cos(aa) * r, cy + Math.sin(aa) * r]); }
    const ws = pts.map((_, k) => wv * (1 - .75 * (k / N)));
    const s = mkStroke(pts, ws, { kind: o.kind || 'u', seed: rnd() * 1000, chip: .18 });
    if (o.reveal) { s.t0 = o.reveal.t0 + rnd() * (o.reveal.jit ?? .15) * (o.reveal.t1 - o.reveal.t0); s.dur = (o.reveal.t1 - o.reveal.t0) * (.55 + rnd() * .45); }
    out.push(s);
  }
  return out;
}

// A carved SHAPE: black silhouette + white halo around it + form-following hatching lit by `light`.
// polys: [[x,y],...][]   o: { light, R, amb, sp, wmax, lo, hi, dir:'contour'|angle|fn, a0, halo, haloW, inset,
//                              kind, seg, seed, tone(x,y)→ override, reveal:{t0,t1,key,speed}, res, fill }
function shape(polys, o = {}) {
  const reg = new Region(polys, { res: o.res ?? 2 });
  const L = o.light || light(.55, -.65, .55);
  const tone = o.tone ? o.tone(reg) : reliefTone(reg, L, { R: o.R ?? 50, amb: o.amb ?? .05, k: o.k ?? 1.05, rim: o.rim ?? 0 });
  let dir = o.dir;
  if (dir === undefined || dir === 'contour') dir = dirContour(reg, o.a0 ?? 0, o.depth ?? 36);
  else if (typeof dir === 'number') dir = dirAngle(dir);
  const ins = o.inset ?? 0;
  const regIn = ins ? { ...reg, bbox: reg.bbox, inside: (x, y) => reg.inside(x, y) && reg.dist(x, y) > ins } : reg;
  const white = !!o.white, htone = white ? (x, y) => 1 - tone(x, y) : tone;
  const strokes = hatch(regIn, { dir, tone: htone, sp: o.sp ?? 8, wmax: o.wmax, lo: o.lo ?? .3, hi: o.hi ?? .95, gamma: o.gamma ?? 1, kind: o.kind || 'v', seg: o.seg, gap: o.gap, seed: o.seed ?? 1, reveal: o.reveal, jit: o.jit ?? .12, chip: o.chip });
  const halo = o.halo ? polys.flatMap((P, i) => cutAlong(offsetPoly(P, o.halo * .5 + (o.haloOff ?? 0)), { closed: true, w: o.halo, kind: 'v', seg: o.haloSeg || [60, 200], gap: [0, 2], seed: (o.seed ?? 1) + i * 7, reveal: o.reveal ? { t0: o.reveal.t0, t1: o.reveal.t0 + (o.reveal.t1 - o.reveal.t0) * .5, speed: 1400 } : null })) : [];
  return {
    reg, strokes, halo, polys, tone,
    // draw on mask g at time t. fill: true = paint the silhouette black first (covers what is behind)
    draw(g, t = 1e9, opts = {}) {
      if (halo.length) drawStrokes(g, halo, { t, color: '#fff' });
      if (o.fill !== false && opts.fill !== false) fillPoly(g, polys, white ? '#fff' : '#000');
      drawStrokes(g, strokes, { t, color: white ? '#000' : '#fff', tips: opts.tips });
    }
  };
}

// colour plate: paint polygons (or any path fn) on the colour canvas with density a
function plate(c, polys, a = 1) { c.fillStyle = `rgba(0,0,0,${a})`; c.beginPath(); if (typeof polys === 'function') polys(c); else for (const P of polys) pathOf(c, P); c.fill('evenodd'); }

// ellipse / helper polygons
function ellipse(cx, cy, rx, ry, n = 64, a0 = 0) { const out = []; for (let i = 0; i < n; i++) { const a = a0 + i / n * Math.PI * 2; out.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]); } return out; }
function rect(x, y, w, h) { return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; }

const __e = {};
if (typeof mkStroke !== 'undefined') __e.mkStroke = mkStroke;
if (typeof spline !== 'undefined') __e.spline = spline;
if (typeof resample !== 'undefined') __e.resample = resample;
if (typeof drawStrokes !== 'undefined') __e.drawStrokes = drawStrokes;
if (typeof strokePath !== 'undefined') __e.strokePath = strokePath;
if (typeof progOf !== 'undefined') __e.progOf = progOf;
if (typeof chip !== 'undefined') __e.chip = chip;
if (typeof xform !== 'undefined') __e.xform = xform;
if (typeof Region !== 'undefined') __e.Region = Region;
if (typeof hatch !== 'undefined') __e.hatch = hatch;
if (typeof lines !== 'undefined') __e.lines = lines;
if (typeof reliefTone !== 'undefined') __e.reliefTone = reliefTone;
if (typeof light !== 'undefined') __e.light = light;
if (typeof dirAngle !== 'undefined') __e.dirAngle = dirAngle;
if (typeof dirRadial !== 'undefined') __e.dirRadial = dirRadial;
if (typeof dirRing !== 'undefined') __e.dirRing = dirRing;
if (typeof dirContour !== 'undefined') __e.dirContour = dirContour;
if (typeof makePrinter !== 'undefined') __e.makePrinter = makePrinter;
if (typeof woodcutFilter !== 'undefined') __e.woodcutFilter = woodcutFilter;
if (typeof INK !== 'undefined') __e.INK = INK;
if (typeof canvas !== 'undefined') __e.canvas = canvas;
if (typeof pathOf !== 'undefined') __e.pathOf = pathOf;
if (typeof fillPoly !== 'undefined') __e.fillPoly = fillPoly;
if (typeof offsetPoly !== 'undefined') __e.offsetPoly = offsetPoly;
if (typeof cutAlong !== 'undefined') __e.cutAlong = cutAlong;
if (typeof flecks !== 'undefined') __e.flecks = flecks;
if (typeof rays !== 'undefined') __e.rays = rays;
if (typeof shape !== 'undefined') __e.shape = shape;
if (typeof plate !== 'undefined') __e.plate = plate;
if (typeof ellipse !== 'undefined') __e.ellipse = ellipse;
if (typeof rect !== 'undefined') __e.rect = rect;
if (typeof PAPER !== 'undefined') __e.PAPER = PAPER;
if (typeof COPPER !== 'undefined') __e.COPPER = COPPER;
if (typeof WOOD !== 'undefined') __e.WOOD = WOOD;
return __e;
})();
__M.trans = (() => {
// The Bell Founder · paper transitions: a sheet with weight that curls off a surface (page curl on a cylinder)
const { clamp } = __M.lib;
const W = 1920, H = 1080, PI = Math.PI;

// Draw a sheet lying on the frame whose free (right) edge has been peeled back to the fold line xf, rolling
// over a cylinder of radius r and lying flipped (underside up) to the left of the fold.
//  up   : the face that is up while the sheet lies flat (canvas W×H)
//  down : the underside (canvas W×H, as it reads once turned over a vertical axis)
//  offX : horizontal camera offset (world→screen), F: perspective distance (px) — lifted paper grows toward camera
function curl(g, up, down, xf, r, { offX = 0, F = 2400, step = 3, shadow = .38 } = {}) {
  r = Math.max(.5, r);
  const cx = W / 2, cy = H / 2;
  const P = z => F / (F - z);
  const place = d => d < PI * r ? [xf + r * Math.sin(d / r), r * (1 - Math.cos(d / r))] : [xf - (d - PI * r), 2 * r];
  // flat part (still lying)
  const xa = clamp(xf, 0, W);
  if (xa > 0) g.drawImage(up, 0, 0, xa, H, offX, 0, xa, H);
  // cast shadow of the curl onto whatever is under it (to the right of the roll)
  const xr = xf + r + offX;
  if (xf < W) {
    const gr = g.createLinearGradient(xr, 0, xr + 70 + r * .8, 0);
    gr.addColorStop(0, `rgba(0,0,0,${shadow})`); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(Math.max(xa + offX, xr - 4), 0, 90 + r, H);
  }
  const rising = [], top = [], flipped = [];
  for (let x = Math.max(0, Math.floor(xf)); x < W; x += step) {
    const d0 = x - xf, d1 = d0 + step, dm = (d0 + d1) / 2;
    if (d1 <= 0) continue;
    const [X0, z0] = place(Math.max(0, d0)), [X1, z1] = place(d1);
    const s = { x, X0, X1, z: (z0 + z1) / 2, dm };
    if (dm < PI * r * .5) rising.push(s); else if (dm < PI * r) top.push(s); else flipped.push(s);
  }
  const drawStrip = (s, face) => {
    const k = P(s.z), a = Math.min(s.X0, s.X1) + offX, b = Math.max(s.X0, s.X1) + offX;
    const x0 = cx + (a - cx) * k, x1 = cx + (b - cx) * k + .8, y0 = cy - cy * k, h = H * k;
    const src = face === 'up' ? up : down, sx = face === 'up' ? s.x : W - s.x - step;
    if (x1 - x0 < .2) return;
    g.drawImage(src, Math.max(0, sx), 0, step, H, x0, y0, x1 - x0, h);
    const th = s.dm < PI * r ? s.dm / r : PI;                           // surface angle
    const lum = face === 'up' ? Math.cos(th) : -Math.cos(th);           // how much the face looks at the camera
    const dark = clamp(.75 * (1 - lum) ** 1.3 + (face === 'up' ? .08 : 0), 0, .8);
    if (dark > .01) { g.fillStyle = `rgba(20,14,8,${dark})`; g.fillRect(x0, y0, x1 - x0, h); }
  };
  for (const s of rising) drawStrip(s, 'up');
  // shadow of the flipped leaf onto the flat sheet, at its left edge
  if (flipped.length) {
    const l = flipped[flipped.length - 1], k = P(2 * r), xl = cx + (Math.min(l.X0, l.X1) + offX - cx) * k;
    const gr = g.createLinearGradient(xl, 0, xl - 50, 0); gr.addColorStop(0, 'rgba(0,0,0,.28)'); gr.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = gr; g.fillRect(xl - 50, 0, 50, H);
  }
  for (const s of flipped) drawStrip(s, 'down');
  for (const s of top) drawStrip(s, 'down');
  // bright rim where the roll turns over
  if (xf < W && r > 2) {
    const k = P(r), xe = cx + (xf + r + offX - cx) * k;
    g.fillStyle = 'rgba(255,250,235,.35)'; g.fillRect(xe - 2.5, cy - cy * k, 2.5, H * k);
  }
}

// a page with weight: slow unstick, a big soft roll in the middle, a flop at the end
function peelState(u, rmax = 150) {
  u = clamp(u);
  const e = u < .22 ? .12 * (u / .22) ** 2 : .12 + .88 * (1 - Math.pow(1 - (u - .22) / .78, 2.2));
  const xf = W * (1 - e) - (u > .9 ? (u - .9) / .1 * 12 : 0);
  const r = 4 + rmax * Math.pow(Math.sin(PI * Math.min(1, u * 1.05)), .7);
  return { xf, r };
}

const __e = {};
if (typeof curl !== 'undefined') __e.curl = curl;
if (typeof peelState !== 'undefined') __e.peelState = peelState;
return __e;
})();
window.WC = __M.index; window.WCL = __M.lib; window.WCT = __M.trans;
