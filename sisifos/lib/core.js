// Temel yardımcılar: zaman, yumuşatma, rastgelelik, gürültü, şekil çizimi
'use strict';
const W = 1920, H = 1080;
const PI = Math.PI, TAU = Math.PI * 2;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, t) => a + (b - a) * t;
const inv = (a, b, x) => clamp((x - a) / (b - a));
const smooth = t => t * t * (3 - 2 * t);
const E = {
  lin: t => t,
  in2: t => t * t,
  out2: t => 1 - (1 - t) * (1 - t),
  in3: t => t * t * t,
  out3: t => 1 - Math.pow(1 - t, 3),
  io2: t => t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2,
  io3: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
  io5: t => t < .5 ? 16 * Math.pow(t, 5) : 1 - Math.pow(-2 * t + 2, 5) / 2,
  sine: t => -(Math.cos(PI * t) - 1) / 2,
  outBack: t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); },
  outExpo: t => t >= 1 ? 1 : 1 - Math.pow(2, -10 * t),
  inExpo: t => t <= 0 ? 0 : Math.pow(2, 10 * t - 10),
};
// a..b aralığında yumuşatılmış ilerleme
const ramp = (t, a, b, e = E.io3) => e(inv(a, b, t));

// Anahtar kareler: [[zaman, değer, (gelen eğri)], ...]; değerler sayı ya da sayı nesnesi
function kf(t, keys) {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const [t1, v1, e] = keys[i];
    if (t <= t1) {
      const [t0, v0] = keys[i - 1];
      const p = (e || E.io3)(inv(t0, t1, t));
      return mix(v0, v1, p);
    }
  }
  return keys[keys.length - 1][1];
}
function mix(a, b, p) {
  if (typeof a === 'number') return a + (b - a) * p;
  if (Array.isArray(a)) return a.map((x, i) => mix(x, b[i], p));
  if (a && typeof a === 'object') {
    const o = {};
    for (const k in a) o[k] = (k in b) ? mix(a[k], b[k], p) : a[k];
    for (const k in b) if (!(k in a)) o[k] = b[k];
    return o;
  }
  return p < .5 ? a : b;
}

function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}
function hash(n) { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }
function noise1(x, seed = 0) {
  const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f);
  return lerp(hash(i + seed * 57.3), hash(i + 1 + seed * 57.3), u) * 2 - 1;
}
function fbm1(x, seed = 0, oct = 3) {
  let v = 0, a = .5, f = 1;
  for (let i = 0; i < oct; i++) { v += a * noise1(x * f, seed + i * 13); a *= .5; f *= 2; }
  return v;
}
function hash2(x, y, s) { const v = Math.sin(x * 127.1 + y * 311.7 + s * 74.7) * 43758.5453; return v - Math.floor(v); }
function noise2(x, y, s = 0) {
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi;
  const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const a = hash2(xi, yi, s), b = hash2(xi + 1, yi, s), c = hash2(xi, yi + 1, s), d = hash2(xi + 1, yi + 1, s);
  return lerp(lerp(a, b, u), lerp(c, d, u), v);
}

// Catmull-Rom üzerinden pürüzsüz yol (kapalı ya da açık)
function spline(ctx, pts, closed = true, k = 1) {
  const n = pts.length;
  if (n < 2) return;
  const P = i => closed ? pts[(i + n) % n] : pts[clamp(i, 0, n - 1)];
  ctx.moveTo(pts[0][0], pts[0][1]);
  const last = closed ? n : n - 1;
  for (let i = 0; i < last; i++) {
    const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
    ctx.bezierCurveTo(
      p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k,
      p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k,
      p2[0], p2[1]);
  }
  if (closed) ctx.closePath();
}
function poly(ctx, pts, closed = true) {
  ctx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length; i++) ctx.lineTo(pts[i][0], pts[i][1]);
  if (closed) ctx.closePath();
}
function rot(p, a) { const c = Math.cos(a), s = Math.sin(a); return [p[0] * c - p[1] * s, p[0] * s + p[1] * c]; }
function add(a, b) { return [a[0] + b[0], a[1] + b[1]]; }
function sub(a, b) { return [a[0] - b[0], a[1] - b[1]]; }
function scl(a, k) { return [a[0] * k, a[1] * k]; }
function len(a) { return Math.hypot(a[0], a[1]); }
