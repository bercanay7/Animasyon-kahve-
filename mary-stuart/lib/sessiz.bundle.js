// sessiz.bundle.js: LemoLab silent-film motoru (MIT, commit 3a7132b) tek klasik betik. Kaynak modüller lib/vendor/ altında, değiştirilmedi.
// Üretici: mary-stuart/tools/bundle_sessiz.py.
'use strict';
const __M = {};
__M.ink = (() => {
// Silent-film "redrawn photoplay" drawing primitives (Canvas2D).
// Everything is drawn in grey values; film.js adds the silver tone, sepia, grain and damage.
// Look: warm-black ink contour (heavier on the side away from the light) + silver wash with a soft light gradient
//       + 45° hatching in the shadows + a faint wash mottle.
const INK = '#15120f';
const V = [0.10, 0.24, 0.43, 0.65, 0.90];            // the five wash values (dark → light)
const grey = (v, a = 1) => { const c = Math.round(Math.max(0, Math.min(1, v)) * 255); return a >= 1 ? `rgb(${c},${c},${c})` : `rgba(${c},${c},${c},${a})`; };

// global drawing state (per frame)
// mode 'tonal': draw values only (soft shading + thin separation lines); the Redraw pass (redraw.js) then inks,
//               hatches and posterises the whole frame — this is the house style.
// mode 'ink'  : draw finished ink + hatching directly (for use without the Redraw pass).
const S = { t: 0, boil: 1, light: [-0.62, -0.78], lineScale: 1, hatchScale: 1, seedBase: 0, mode: 'tonal', sepLine: .5 };
function setFrame(t, { boil = 1, light, lineScale = 1 } = {}) {
  S.t = t; S.boil = boil; S.lineScale = lineScale; if (light) S.light = light;
}
const hash = n => { n = Math.sin(n * 127.1 + 311.7) * 43758.5453; return n - Math.floor(n); };
const vn = x => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return hash(i) * (1 - u) + hash(i + 1) * u; };
const H = hash, VN = vn;
const boilKey = () => Math.floor(S.t * 12);                  // line boil on twos

// ---------- geometry helpers ----------
function catmull(pts, closed = true, n = 8) {          // Catmull-Rom through control points → dense polyline
  const out = [], L = pts.length, cnt = closed ? L : L - 1;
  for (let i = 0; i < cnt; i++) {
    const p0 = pts[closed ? (i - 1 + L) % L : Math.max(0, i - 1)], p1 = pts[i], p2 = pts[(i + 1) % L], p3 = pts[closed ? (i + 2) % L : Math.min(L - 1, i + 2)];
    for (let k = 0; k < n; k++) {
      const t = k / n, t2 = t * t, t3 = t2 * t;
      out.push([
        .5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3),
        .5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)]);
    }
  }
  if (!closed) out.push(pts[L - 1].slice());
  return out;
}
function bez(p0, p1, p2, p3, n = 12) { const o = []; for (let i = 0; i <= n; i++) { const t = i / n, u = 1 - t; o.push([u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0], u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1]]); } return o; }
function ellipsePts(cx, cy, rx, ry, rot = 0, n = 36) { const o = [], c = Math.cos(rot), s = Math.sin(rot); for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2, x = Math.cos(a) * rx, y = Math.sin(a) * ry; o.push([cx + x * c - y * s, cy + x * s + y * c]); } return o; }
function rectPts(x, y, w, h) { return [[x, y], [x + w, y], [x + w, y + h], [x, y + h]]; }
function xform(pts, m) { return pts.map(([x, y]) => [m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]]); }
function bbox(pts) { let a = 1e9, b = 1e9, c = -1e9, d = -1e9; for (const [x, y] of pts) { if (x < a) a = x; if (y < b) b = y; if (x > c) c = x; if (y > d) d = y; } return [a, b, c, d]; }
function pathOf(g, pts, closed = true) { g.beginPath(); g.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) g.lineTo(pts[i][0], pts[i][1]); if (closed) g.closePath(); }
function resample(pts, closed, step) {
  const P = closed ? pts.concat([pts[0]]) : pts, out = [];
  let acc = 0; out.push(P[0]);
  for (let i = 1; i < P.length; i++) {
    const [x0, y0] = P[i - 1], [x1, y1] = P[i], d = Math.hypot(x1 - x0, y1 - y0);
    let s = step - acc;
    while (s <= d) { const t = s / d; out.push([x0 + (x1 - x0) * t, y0 + (y1 - y0) * t]); s += step; }
    acc = d - (s - step);
  }
  if (!closed) { const l = P[P.length - 1]; const o = out[out.length - 1]; if (Math.hypot(l[0] - o[0], l[1] - o[1]) > step * .3) out.push(l); }
  else if (out.length > 2) { const o = out[out.length - 1]; if (Math.hypot(P[0][0] - o[0], P[0][1] - o[1]) < step * .3) out.pop(); }
  return out;
}

// ---------- ink line: variable width, tapered, heavier away from the light, boiling ----------
// opts: w (px), taper (0..1 of ends), closed, light (weight by normal·(-light)), seed, dry (0..1 breaks), boil (px)
function ink(g, pts, o = {}) {
  if (!pts || pts.length < 2) return;
  const closed = !!o.closed, w = (o.w ?? 2.5) * S.lineScale, seed = o.seed ?? 1;
  const step = Math.max(1.2, Math.min(6, w * 1.1));
  let P = resample(pts, closed, step);
  const n = P.length; if (n < 2) return;
  const bk = boilKey(), bamp = (o.boil ?? 0.6) * S.boil;
  // boil: low-frequency wobble along the line, re-rolled on twos
  if (bamp > 0) P = P.map((p, i) => { const u = i * step / 40; return [p[0] + (vn(u + seed * 7.1 + bk * 13.7) - .5) * 2 * bamp, p[1] + (vn(u + seed * 3.3 + bk * 9.1 + 50) - .5) * 2 * bamp]; });
  const [lx, ly] = S.light, L = [], R = [];
  const lightK = o.light ?? 0.55, taper = o.taper ?? (closed ? 0 : 0.18);
  for (let i = 0; i < n; i++) {
    const a = P[closed ? (i - 1 + n) % n : Math.max(0, i - 1)], b = P[closed ? (i + 1) % n : Math.min(n - 1, i + 1)];
    let tx = b[0] - a[0], ty = b[1] - a[1]; const tl = Math.hypot(tx, ty) || 1; tx /= tl; ty /= tl;
    const nx = ty, ny = -tx;                                   // outward normal for clockwise(screen) paths
    let wk = 1;
    if (lightK) { const d = -(nx * lx + ny * ly); wk *= 1 - lightK * .5 + lightK * Math.max(0, d); }   // heavier on the shadow side
    if (!closed && taper > 0) { const u = i / (n - 1), e = Math.min(u, 1 - u) / taper; wk *= Math.min(1, .25 + .75 * Math.sqrt(Math.min(1, e))); }
    wk *= .82 + .36 * vn(i * step / 55 + seed * 5.7);             // pressure
    if (o.dry) { const d = vn(i * step / 18 + seed * 11.3); if (d < o.dry * .55) wk *= Math.max(0, (d / (o.dry * .55)) * 1.4 - .4); }
    const hw = w * wk * .5, p = P[i];
    L.push([p[0] + nx * hw, p[1] + ny * hw]); R.push([p[0] - nx * hw, p[1] - ny * hw]);
  }
  g.save(); g.fillStyle = o.color || INK; if (o.alpha != null) g.globalAlpha *= o.alpha;
  g.beginPath();
  if (closed) {
    g.moveTo(L[0][0], L[0][1]); for (let i = 1; i < n; i++) g.lineTo(L[i][0], L[i][1]); g.closePath();
    g.moveTo(R[n - 1][0], R[n - 1][1]); for (let i = n - 2; i >= 0; i--) g.lineTo(R[i][0], R[i][1]); g.closePath();
    g.fill('evenodd');
  } else {
    g.moveTo(L[0][0], L[0][1]); for (let i = 1; i < n; i++) g.lineTo(L[i][0], L[i][1]);
    for (let i = n - 1; i >= 0; i--) g.lineTo(R[i][0], R[i][1]); g.closePath(); g.fill();
  }
  g.restore();
}

// ---------- silver wash: fill with a soft light gradient + mottle ----------
function wash(g, pts, v, o = {}) {
  const [x0, y0, x1, y1] = bbox(pts), cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, r = Math.max(x1 - x0, y1 - y0) * .5 + 1;
  const [lx, ly] = o.lightDir || S.light, k = o.grad ?? 0.16;
  pathOf(g, pts, true);
  if (k > 0) {
    const gr = g.createLinearGradient(cx + lx * r, cy + ly * r, cx - lx * r, cy - ly * r);
    gr.addColorStop(0, grey(v + k * .55)); gr.addColorStop(.55, grey(v)); gr.addColorStop(1, grey(v - k * .6));
    g.fillStyle = gr;
  } else g.fillStyle = grey(v);
  g.fill();
}

// ---------- hatching: 45° parallel lines, fading from the shadow side ----------
// o: angle (rad), gap (px), w, strength(0..1), cross(0..1), side (true = only on shadow side)
function hatch(g, pts, o = {}) {
  const strength = o.strength ?? 0.6; if (strength <= 0.02) return;
  const [x0, y0, x1, y1] = bbox(pts), cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, r = Math.hypot(x1 - x0, y1 - y0) * .5 + 2;
  const ang = o.angle ?? -Math.PI / 4, gap = (o.gap ?? 6) * S.lineScale, w = (o.w ?? 1.1) * S.lineScale, seed = o.seed ?? 3;
  g.save(); pathOf(g, pts, true); g.clip();
  const [lx, ly] = S.light;
  let style = INK;
  if (o.side !== false) {
    const gr = g.createLinearGradient(cx + lx * r, cy + ly * r, cx - lx * r, cy - ly * r);
    const s0 = o.sideStart ?? .35;
    gr.addColorStop(0, 'rgba(21,18,15,0)'); gr.addColorStop(s0, 'rgba(21,18,15,0)'); gr.addColorStop(1, `rgba(21,18,15,${Math.min(1, strength * 1.2)})`);
    style = gr;
  } else g.globalAlpha *= strength;
  g.strokeStyle = style; g.lineWidth = w; g.lineCap = 'round';
  const pass = (a, off) => {
    const c = Math.cos(a), s = Math.sin(a);
    g.beginPath();
    for (let d = -r; d <= r; d += gap) {
      const j = (H(d * .37 + seed + off) - .5) * gap * .35, jj = (H(d * .71 + seed * 2 + off) - .5) * .06;
      const px = cx - s * (d + j), py = cy + c * (d + j);
      g.moveTo(px - c * r, py - s * r - jj * r); g.lineTo(px + c * r, py + s * r + jj * r);
    }
    g.stroke();
  };
  pass(ang, 0);
  if ((o.cross ?? 0) > 0.02) { g.globalAlpha *= o.cross; pass(ang + Math.PI / 2.3, 9); }
  g.restore();
}

// ---------- form = wash + hatching + contour (the basic "drawn object") ----------
// style: { v, grad, line (px, 0 = none), hatch (auto from v if undefined), cross, lineLight, dry, seed, color }
function form(g, pts, st = {}) {
  const v = st.v ?? V[3];
  if (S.mode === 'tonal') {
    if (st.fill !== false) wash(g, pts, v, st);
    if (st.cyl != null) cylShade(g, pts, st.cyl, st.cylK ?? .13);
    if (st.texture) st.texture(g, pts);
    if (st.shade) shade(g, pts, typeof st.shade === 'number' ? { off: st.shade, hatch: 0, a: v > .7 ? .2 : .3, seed: st.seed, soft: st.shade * .25 } : { ...st.shade, hatch: 0 });
    if ((st.line ?? 2.6) > 0) {
      const o = { w: (st.line ?? 2.6) * S.sepLine, closed: !st.openEnd, taper: .04, light: .5, seed: st.seed ?? 1, color: st.lineColor || grey(Math.max(0, v - .45)), boil: st.boil };
      ink(g, pts, o);
    }
    return;
  }
  if (st.fill !== false) wash(g, pts, v, st);
  if (st.texture) st.texture(g, pts);
  if (st.shade) shade(g, pts, typeof st.shade === 'number' ? { off: st.shade, hatch: v < .5 ? .7 : .45, a: v > .7 ? .16 : .26, seed: st.seed } : st.shade);
  const hs = st.hatch ?? Math.max(0, Math.min(1, (0.62 - v) * 1.9));
  if (hs > 0.02) hatch(g, pts, { strength: hs, gap: st.gap ?? (v < .25 ? 4.5 : 6), cross: st.cross ?? (v < .2 ? .6 : 0), seed: st.seed, side: st.hatchSide ?? (v > .22), angle: st.hatchAngle, sideStart: st.sideStart });
  if ((st.line ?? 2.6) > 0) {
    if (st.openEnd) ink(g, pts, { w: st.line ?? 2.6, closed: false, taper: .04, light: st.lineLight ?? .6, seed: st.seed ?? 1, dry: st.dry, color: st.lineColor, boil: st.boil });
    else ink(g, pts, { w: st.line ?? 2.6, closed: true, light: st.lineLight ?? .6, seed: st.seed ?? 1, dry: st.dry, color: st.lineColor, boil: st.boil });
  }
}

// open strokes (folds, details)
function stroke(g, pts, w = 1.6, o = {}) { ink(g, pts, { w, closed: false, taper: o.taper ?? .3, light: o.light ?? 0, seed: o.seed ?? 5, dry: o.dry, alpha: o.alpha, boil: o.boil, color: o.color }); }

// ---------- drawShape: draw ANY path in this style ----------
// shape: array of points (closed) or {pts, closed}. style: form() style plus { color: '#D97757' } to keep a hue
// (a coloured shape is drawn in colour; film.js keeps its hue if it is also painted into the colour mask — see film.js).
function drawShape(g, shape, style = {}) {
  const pts = Array.isArray(shape) ? shape : shape.pts, closed = Array.isArray(shape) ? true : shape.closed !== false;
  if (!closed) { stroke(g, pts, style.line ?? 2.6, style); return; }
  if (style.color) {                                           // coloured element: hue fill, ink contour kept
    pathOf(g, pts); g.fillStyle = style.color; g.fill();
    if (style.hatch) hatch(g, pts, { strength: style.hatch, seed: style.seed });
    ink(g, pts, { w: style.line ?? 2.6, closed: true, light: .6, seed: style.seed ?? 1 });
    return;
  }
  form(g, pts, style);
}

// four-pointed star with a cursor tail (example shape for §10)
function sparkPts(cx, cy, r, tail = 0) {
  const pts = [];
  for (let i = 0; i < 8; i++) { const a = i / 8 * Math.PI * 2 - Math.PI / 2, rr = i % 2 ? r * .28 : r; pts.push([cx + Math.cos(a) * rr, cy + Math.sin(a) * rr]); }
  const star = catmull(pts, true, 4);
  return { star, tail: tail > 0 ? [[cx - r * .3, cy + r * .9], [cx - r * .3 - tail * .2, cy + r * .9 + tail]] : null };
}

// ---------- wash mottle (painted-sheet feel), cached noise tile ----------
let mottleTile = null;
function mottle(g, x, y, w, h, a = .08, seed = 0) {
  if (!mottleTile) {
    mottleTile = document.createElement('canvas'); mottleTile.width = mottleTile.height = 512;
    const c = mottleTile.getContext('2d'), im = c.createImageData(512, 512);
    for (let j = 0; j < 512; j++) for (let i = 0; i < 512; i++) {
      const n = .5 * vn2(i / 64, j / 64, 8) + .3 * vn2(i / 16, j / 16 + 3, 32) + .2 * vn2(i / 8, j / 8 + 5, 64);
      const k = (i + j * 512) * 4, c8 = Math.round(n * 255); im.data[k] = im.data[k + 1] = im.data[k + 2] = c8; im.data[k + 3] = 255;
    }
    c.putImageData(im, 0, 0);
  }
  g.save(); g.globalAlpha *= a; g.globalCompositeOperation = 'overlay';
  const p = g.createPattern(mottleTile, 'repeat'); p.setTransform(new DOMMatrix().translate(seed * 97 % 512, seed * 61 % 512));
  g.fillStyle = p; g.fillRect(x, y, w, h); g.restore();
}
function vn2(x, y, P) { // periodic value noise, period P lattice cells (tileable)
  const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
  const h = (a, b) => hash(((a % P) + P) % P * 57 + ((b % P) + P) % P * 131 + P);
  return (h(xi, yi) * (1 - u) + h(xi + 1, yi) * u) * (1 - v) + (h(xi, yi + 1) * (1 - u) + h(xi + 1, yi + 1) * u) * v;
}

// ---------- form shadow: the crescent on the side away from the light (outline minus itself shifted toward the light)
// o: off (px shift), v (shadow wash value), a (wash alpha), hatch (0..1), gap, soft (px blur of the terminator)
function shade(g, pts, o = {}) {
  const off = o.off ?? 8; if (off <= .3) return;
  const [lx, ly] = o.lightDir || S.light, dx = lx * off, dy = ly * off;
  const [x0, y0, x1, y1] = bbox(pts);
  g.save(); pathOf(g, pts, true); g.clip();
  const crescent = () => {
    g.beginPath(); g.rect(x0 - off * 3, y0 - off * 3, x1 - x0 + off * 6, y1 - y0 + off * 6);
    g.moveTo(pts[0][0] + dx, pts[0][1] + dy); for (let i = 1; i < pts.length; i++) g.lineTo(pts[i][0] + dx, pts[i][1] + dy); g.closePath();
  };
  if (o.soft) g.filter = `blur(${o.soft}px)`;
  crescent(); g.fillStyle = `rgba(22,18,14,${o.a ?? .22})`; g.fill('evenodd');
  g.filter = 'none';
  if ((o.hatch ?? .5) > .02) {
    crescent(); g.clip('evenodd');
    const gap = (o.gap ?? 5) * S.lineScale, ang = o.angle ?? -Math.PI / 4, c = Math.cos(ang), s = Math.sin(ang), r = Math.hypot(x1 - x0, y1 - y0) / 2 + off * 3, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    g.strokeStyle = `rgba(21,18,15,${Math.min(1, o.hatch ?? .5)})`; g.lineWidth = (o.hw ?? .9) * S.lineScale; g.beginPath();
    for (let d = -r; d <= r; d += gap) { const j = (H(d * .31 + (o.seed ?? 1)) - .5) * gap * .3, px = cx - s * (d + j), py = cy + c * (d + j); g.moveTo(px - c * r, py - s * r); g.lineTo(px + c * r, py + s * r); }
    g.stroke();
  }
  g.restore();
}

// cylindrical form shading: darker at both edges across the axis (angle, rad), lighter core shifted toward the light
function cylShade(g, pts, axis, k = .13) {
  const [x0, y0, x1, y1] = bbox(pts), cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  const nx = -Math.sin(axis), ny = Math.cos(axis);                 // across the form
  const ext = Math.abs(nx) * (x1 - x0) / 2 + Math.abs(ny) * (y1 - y0) / 2 + 1;
  const [lx, ly] = S.light, sh = (nx * lx + ny * ly) > 0 ? -1 : 1;  // which edge faces the light
  const gr = g.createLinearGradient(cx - nx * ext, cy - ny * ext, cx + nx * ext, cy + ny * ext);
  const a = `rgba(20,16,12,${k})`, a2 = `rgba(20,16,12,${k * 1.6})`, z = 'rgba(20,16,12,0)';
  if (sh > 0) { gr.addColorStop(0, a); gr.addColorStop(.3, z); gr.addColorStop(.62, z); gr.addColorStop(1, a2); }
  else { gr.addColorStop(0, a2); gr.addColorStop(.38, z); gr.addColorStop(.7, z); gr.addColorStop(1, a); }
  g.save(); pathOf(g, pts); g.clip(); g.fillStyle = gr; g.fillRect(x0 - 2, y0 - 2, x1 - x0 + 4, y1 - y0 + 4); g.restore();
}

const __e = {};
if (typeof INK !== 'undefined') __e.INK = INK;
if (typeof V !== 'undefined') __e.V = V;
if (typeof grey !== 'undefined') __e.grey = grey;
if (typeof S !== 'undefined') __e.S = S;
if (typeof setFrame !== 'undefined') __e.setFrame = setFrame;
if (typeof H !== 'undefined') __e.H = H;
if (typeof catmull !== 'undefined') __e.catmull = catmull;
if (typeof bez !== 'undefined') __e.bez = bez;
if (typeof ellipsePts !== 'undefined') __e.ellipsePts = ellipsePts;
if (typeof rectPts !== 'undefined') __e.rectPts = rectPts;
if (typeof xform !== 'undefined') __e.xform = xform;
if (typeof bbox !== 'undefined') __e.bbox = bbox;
if (typeof pathOf !== 'undefined') __e.pathOf = pathOf;
if (typeof ink !== 'undefined') __e.ink = ink;
if (typeof wash !== 'undefined') __e.wash = wash;
if (typeof hatch !== 'undefined') __e.hatch = hatch;
if (typeof form !== 'undefined') __e.form = form;
if (typeof stroke !== 'undefined') __e.stroke = stroke;
if (typeof drawShape !== 'undefined') __e.drawShape = drawShape;
if (typeof sparkPts !== 'undefined') __e.sparkPts = sparkPts;
if (typeof mottle !== 'undefined') __e.mottle = mottle;
if (typeof shade !== 'undefined') __e.shade = shade;
if (typeof cylShade !== 'undefined') __e.cylShade = cylShade;
if (typeof a !== 'undefined') __e.a = a;
if (typeof VN !== 'undefined') __e.VN = VN;
return __e;
})();
__M.redraw = (() => {
// "Video frame → silent-film drawing" (WebGL2). Also the house style: the film's own tonal paintings go through it too,
// so real footage and animation share one hand.
//   const rd = new Redraw(1440, 1080);
//   const out = rd.render(srcCanvasOrImage, { frame, lines: 1, tone: 1, hatch: 1, levels: 5 });   // → canvas (grey)
// Pipeline: luminance + gentle contrast → separable Gaussian blurs at σ and kσ → XDoG edges (soft tanh threshold) = ink lines
//           → luminance posterised into `levels` wash steps with soft transitions → hatching in the darks (45°, then crossed),
//           hatch pattern re-drawn ("boils") every 2 frames like hand-redrawn animation → paper white highlights.
// Params: sigma (px, 1.1), k (1.6), p (XDoG sharpen, 22), eps (.62), phi (edge softness, 26), lines/tone/hatch (mix 0..1),
//         levels (wash steps), gamma (tone curve), gap (hatch spacing px), lineDark (ink value), paper (white value),
//         src = { x, y, w, h } crop of the source in source pixels (fit to cover), flipX.
const VS = `#version 300 es
in vec2 p; out vec2 uv; void main(){ uv = p*.5+.5; gl_Position = vec4(p,0,1); }`;
const HEAD = `#version 300 es
precision highp float; in vec2 uv; out vec4 o; uniform vec2 R; uniform sampler2D T;`;
const FS_LUM = HEAD + `
uniform vec4 crop; uniform vec2 srcSize; uniform float gam, con;
void main(){
  vec2 px = vec2(uv.x, 1.-uv.y) * R;
  vec2 sp = crop.xy + px / R * crop.zw;             // source pixel
  vec3 c = texture(T, sp / srcSize).rgb;
  float L = dot(c, vec3(.30,.59,.11));
  L = pow(clamp(L,0.,1.), gam);
  L = clamp((L - .5) * con + .5, 0., 1.);
  o = vec4(vec3(L), 1.);
}`;
const FS_BLUR = HEAD + `
uniform vec2 dir; uniform float sig;
void main(){
  vec2 st = uv; float s = 0., w = 0.;
  int n = int(ceil(sig*3.));
  for (int i = -12; i <= 12; i++) { if (i < -n || i > n) continue; float x = float(i); float k = exp(-x*x/(2.*sig*sig)); s += texture(T, st + dir*x/R).r * k; w += k; }
  o = vec4(vec3(s/w), 1.);
}`;
const FS_BILAT = HEAD + `
uniform float rs, ss2;
void main(){
  float c = texture(T, uv).r, s = 0., w = 0.;
  for (int j = -3; j <= 3; j++) for (int i = -3; i <= 3; i++) {
    vec2 o2 = vec2(float(i), float(j)) * ss2;
    float v = texture(T, uv + o2 / R).r;
    float k = exp(-dot(o2,o2)/(2.*9.*ss2*ss2) - (v-c)*(v-c)/(2.*rs*rs));
    s += v*k; w += k;
  }
  o = vec4(vec3(s/w), 1.);
}`;
const FS_FINAL = HEAD + `
uniform sampler2D A, B, Lm; uniform float frame, p, eps, phi, uLines, uTone, uHatch, levels, gap, lineDark, paper, seed, washDark, washGam, h1, h2, h3;
float h21(vec2 q){ q = fract(q*vec2(123.34,456.21)); q += dot(q,q+45.32); return fract(q.x*q.y); }
float vn(vec2 q){ vec2 i=floor(q), f=fract(q); vec2 u=f*f*(3.-2.*f);
  return mix(mix(h21(i),h21(i+vec2(1,0)),u.x), mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),u.x), u.y); }
// one family of hatch lines: angle a, spacing g, darkness-driven width
float hatchLine(vec2 px, float a, float g, float w, float bk){
  vec2 d = vec2(cos(a), sin(a));
  float wob = (vn(px * .02 + bk * 3.7) - .5) * 2.2 + (vn(px*.11 + bk) - .5) * .7;   // hand wobble
  float t = dot(px, vec2(-d.y, d.x)) + wob + bk * 17.31;
  float f = abs(fract(t / g) - .5) * g;                                             // distance to nearest line (px)
  float brk = smoothstep(.18, .3, vn(vec2(dot(px, d) * .035, floor(t / g) * 1.7 + bk)));   // broken strokes
  return (1. - smoothstep(w * .5, w * .5 + .9, f)) * brk;
}
void main(){
  vec2 px = vec2(uv.x, 1.-uv.y) * R;
  float g1 = texture(A, uv).r, g2 = texture(B, uv).r, L = texture(Lm, uv).r;
  // XDoG
  // DoG band-pass: ink on the dark side of every edge (tone-independent, so dark areas are not flooded)
  float Dg = g1 - g2;
  float ink = smoothstep(eps, eps + 1. / phi, -Dg * p);
  float edge = 1. - ink;
  // wash: soft posterisation of the smoothed luminance
  float Ls = mix(L, g1, .6);
  float q = Ls * (levels - 1.);
  float fq = floor(q), fr = q - fq;
  float st = (fq + smoothstep(.3, .7, fr)) / (levels - 1.);
  float wash = mix(Ls, st, uTone);
  wash = mix(washDark, paper, pow(wash, washGam));
  // hatching in the darks, boiling every 2 frames (each frame is "redrawn")
  float bk = floor(frame / 2.);
  float dk = 1. - Ls;
  float h = 0.;
  h = max(h, hatchLine(px, .785, gap, .75 + dk * 1.1, bk) * smoothstep(h1, h1 + .08, dk));
  h = max(h, hatchLine(px, -.785, gap * 1.1, .7 + dk * 1.0, bk + 5.) * smoothstep(h2, h2 + .08, dk));
  h = max(h, hatchLine(px, .12, gap * .85, .7 + dk * .9, bk + 9.) * smoothstep(h3, h3 + .06, dk));
  float c = mix(wash, lineDark, h * uHatch * .88);
  c = mix(c, lineDark, (1. - edge) * uLines);
  o = vec4(vec3(c), 1.);
}`;

class Redraw {
  constructor(w = 1440, h = 1080) {
    this.w = w; this.h = h;
    this.canvas = document.createElement('canvas'); this.canvas.width = w; this.canvas.height = h;
    const gl = this.gl = this.canvas.getContext('webgl2', { preserveDrawingBuffer: true });
    if (!gl) throw new Error('webgl2 unavailable');
    const sh = (t, src) => { const s = gl.createShader(t); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; };
    const prog = fs => { const p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p)); return p; };
    this.pLum = prog(FS_LUM); this.pBlur = prog(FS_BLUR); this.pFin = prog(FS_FINAL); this.pBil = prog(FS_BILAT);
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    for (const p of [this.pLum, this.pBlur, this.pFin, this.pBil]) { const l = gl.getAttribLocation(p, 'p'); gl.enableVertexAttribArray(l); gl.vertexAttribPointer(l, 2, gl.FLOAT, false, 0, 0); }
    const mkTex = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); return t; };
    this.src = mkTex();
    this.rt = [0, 1, 2, 3, 4, 5].map(() => { const t = mkTex(); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null); const fb = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, fb); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0); return { t, fb }; });
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }
  _pass(prog, target, texs, uni) {
    const gl = this.gl; gl.useProgram(prog);
    gl.bindFramebuffer(gl.FRAMEBUFFER, target ? target.fb : null); gl.viewport(0, 0, this.w, this.h);
    let i = 0; for (const [name, tex] of texs) { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, tex); gl.uniform1i(gl.getUniformLocation(prog, name), i); i++; }
    gl.uniform2f(gl.getUniformLocation(prog, 'R'), this.w, this.h);
    for (const k in uni) { const v = uni[k], l = gl.getUniformLocation(prog, k); if (l == null) continue; if (Array.isArray(v)) (v.length === 2 ? gl.uniform2f(l, ...v) : gl.uniform4f(l, ...v)); else gl.uniform1f(l, v); }
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  render(img, o = {}) {
    const gl = this.gl;
    const sw = img.videoWidth || img.naturalWidth || img.width, shh = img.videoHeight || img.naturalHeight || img.height;
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, this.src);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
    // crop: cover-fit by default
    let cr = o.src; if (!cr) { const a = this.w / this.h, b = sw / shh; cr = b > a ? { x: (sw - shh * a) / 2, y: 0, w: shh * a, h: shh } : { x: 0, y: (shh - sw / a) / 2, w: sw, h: sw / a }; }
    let [L, A1, A2, B1, B2, L2] = this.rt;
    // texture v=0 is the top row (no flip), so sampling with top-left pixel coords is direct; render targets are bottom-up, handled by uv
    this._pass(this.pLum, L, [['T', this.src]], { crop: [cr.x, cr.y, cr.w, cr.h], srcSize: [sw, shh], gam: o.gamma ?? 1, con: o.contrast ?? 1.08 });
    for (let i = 0; i < (o.bilateral ?? 0); i++) { this._pass(this.pBil, L2, [['T', L.t]], { rs: o.bilRange ?? .09, ss2: o.bilStep ?? 1.3 }); [L, L2] = [L2, L]; }
    const sig = o.sigma ?? 1.1, k = o.k ?? 1.6;
    this._pass(this.pBlur, A1, [['T', L.t]], { dir: [1, 0], sig });
    this._pass(this.pBlur, A2, [['T', A1.t]], { dir: [0, 1], sig });
    this._pass(this.pBlur, B1, [['T', L.t]], { dir: [1, 0], sig: sig * k });
    this._pass(this.pBlur, B2, [['T', B1.t]], { dir: [0, 1], sig: sig * k });
    this._pass(this.pFin, null, [['A', A2.t], ['B', B2.t], ['Lm', L.t]], {
      frame: o.frame ?? 0, p: o.p ?? 14, eps: o.eps ?? .35, phi: o.phi ?? 4, uLines: o.lines ?? 1, uTone: o.tone ?? 1, uHatch: o.hatch ?? 1,
      levels: o.levels ?? 5, gap: o.gap ?? 5.5, lineDark: o.lineDark ?? .07, paper: o.paper ?? .95, seed: o.seed ?? 1,
      washDark: o.washDark ?? .34, washGam: o.washGam ?? .85, h1: o.h1 ?? .42, h2: o.h2 ?? .6, h3: o.h3 ?? .8 });
    return this.canvas;
  }
}

const __e = {};
if (typeof Redraw !== 'undefined') __e.Redraw = Redraw;
return __e;
})();
__M.film = (() => {
// Film-aging post module (WebGL2). Stack it on ANY 2D canvas:
//   const film = new FilmPost(1440, 1080);
//   const out = film.render(srcCanvas, { frame, strength: .6, sepia: .15 }, colorMaskCanvas?);   // → canvas
//   damage(g2d, x, y, w, h, frame, strength)   // dust, hairs and splice marks drawn on top (2D)
// Params (all optional, 0..1 unless noted):
//   strength  master amount of damage (scales flicker, weave, scratches, dust, burn, grain)
//   grain, flicker, weave, scratches, burn, vignette, halation   individual multipliers (default 1)
//   sepia     0 = neutral silver, 1 = full brown-toned print
//   black, white  print density endpoints (default .055 / .93); contrast (S-curve, default 1)
//   jump      px vertical frame jump (splice), exposure (multiplier, default 1)
//   crank     projector speed (1 = normal; >1 makes the flicker faster/stronger — hand-cranked)
// colorMask: optional canvas whose alpha marks pixels that keep their own colour ("the one colour").
const VS = `#version 300 es
in vec2 p; out vec2 uv; void main(){ uv = p*.5+.5; gl_Position = vec4(p,0,1); }`;
const FS = `#version 300 es
precision highp float; in vec2 uv; out vec4 o;
uniform sampler2D T, B, C; uniform vec2 R; uniform float frame, seed;
uniform float uStr, uGrain, uFlick, uScr, uBurn, uVig, uHal, uSepia, uBlack, uWhite, uCon, uExpo, uHasC;
uniform vec2 uWeave;
float h21(vec2 p){ p = fract(p*vec2(123.34,456.21)); p += dot(p,p+45.32); return fract(p.x*p.y); }
float h11(float x){ return fract(sin(x*127.1+311.7)*43758.5453); }
float vn(vec2 p){ vec2 i=floor(p), f=fract(p); vec2 u=f*f*(3.-2.*f);
  return mix(mix(h21(i),h21(i+vec2(1,0)),u.x), mix(h21(i+vec2(0,1)),h21(i+vec2(1,1)),u.x), u.y); }
float fbm(vec2 p){ float a=.5, s=0.; for(int i=0;i<4;i++){ s+=a*vn(p); p*=2.07; a*=.5; } return s; }
float lum(vec3 c){ return dot(c, vec3(.299,.587,.114)); }
void main(){
  vec2 px = vec2(uv.x, 1.-uv.y)*R;                       // pixel coords, top-left origin
  vec2 q = px - uWeave;                                   // gate weave: image moves under the fixed aperture
  vec2 st = q / R;
  // slight optical softness (print of a print)
  vec3 c0 = texture(T, st).rgb;
  vec3 c1 = (texture(T, st+vec2(.7,0)/R).rgb + texture(T, st-vec2(.7,0)/R).rgb + texture(T, st+vec2(0,.7)/R).rgb + texture(T, st-vec2(0,.7)/R).rgb)*.25;
  vec3 col = mix(c0, c1, .45);
  float L = lum(col);
  // halation: highlights bleed
  vec3 bl = texture(B, st).rgb; float Lb = lum(bl);
  L += uHal * .22 * max(0., Lb - .55) * 1.8;
  // exposure + flicker (uExpo already contains per-frame flicker) + uneven density across the frame
  float dens = (fbm(vec2(st.x*1.3, st.y*1.1) + vec2(frame*.021, seed)) - .5) * .09 * uFlick * uStr;
  L = L * uExpo + dens;
  // S-curve contrast
  L = clamp(L, 0., 1.2);
  float s = L*L*(3.-2.*L); L = mix(L, s, clamp(uCon-1., -1., 1.) + .35);
  // print density endpoints
  L = mix(uBlack, uWhite, clamp(L, 0., 1.));
  // vertical scratches (white = emulsion scraped off the print, dark = dirt on the negative)
  float scr = 0.;
  for (int i = 0; i < 4; i++) {
    float fi = float(i);
    float life = floor((frame + fi*17.) / (5. + fi*3.));               // each scratch lives a few frames
    float on = step(1. - uScr*uStr*(.55 - fi*.1), h11(life*3.1 + fi*7.7));
    float x = h11(life*1.7 + fi) * R.x + sin(frame*.37 + fi)*3.;
    float w = .6 + h11(life + fi*2.) * 1.4;
    float d = abs(px.x - x);
    float seg = step(.25, vn(vec2(px.y*.008 + fi*9., life)));           // broken along its length
    float dark = step(.62, h11(life*9.1 + fi));
    scr += on * seg * smoothstep(w, 0., d) * (dark > .5 ? -.55 : .7);
  }
  L += scr;
  // burn / edge fog: uneven brown darkening creeping in from the frame edges
  vec2 e = min(st, 1. - st); float ed = min(e.x*R.x/R.y, e.y);
  float burnN = fbm(st*vec2(3.,2.4) + vec2(seed*.3, frame*.004));
  float burn = smoothstep(.12 + burnN*.1, 0., ed) * uBurn * uStr;
  L *= 1. - burn*.55;
  // vignette
  vec2 cv = st - .5; float vig = dot(cv*vec2(1.,1.15), cv*vec2(1.,1.15));
  L *= 1. - uVig * smoothstep(.10, .62, vig) * .62;
  // silver grain: 2 octaves, coarser in the mids
  float g1 = h21(floor(px/1.25) + vec2(frame*13.1, frame*7.7)) - .5;
  float g2 = vn(px/2.6 + vec2(frame*31.7, frame*11.3)) - .5;
  float gmid = 1. - abs(L - .5)*1.3;
  L += (g1*.08 + g2*.07) * uGrain * (.45 + uStr*.55) * gmid;
  L = clamp(L, 0., 1.);
  // tone: neutral silver → sepia print
  vec3 silver = vec3(L) * vec3(.985, .99, 1.0);
  vec3 sep = mix(vec3(.105,.07,.045), vec3(.62,.50,.37), smoothstep(0., .6, L));
  sep = mix(sep, vec3(.97,.92,.82), smoothstep(.5, 1., L));
  vec3 outc = mix(silver, sep, uSepia);
  outc += vec3(.035,.012,-.01) * burn;                     // burned edges go brown
  // the one colour: keep hue where the mask says so (same grain + exposure)
  if (uHasC > .5) {
    vec4 cm = texture(C, st);
    if (cm.a > .003) {
      vec3 cc = cm.rgb * uExpo;
      cc += (g1*.06 + g2*.05) * uGrain;
      cc *= 1. - uVig * smoothstep(.10, .62, vig) * .62;
      outc = mix(outc, clamp(cc, 0., 1.), cm.a);
    }
  }
  // outside the image (weave exposes the frame line) → black
  float inside = step(0., st.x) * step(st.x, 1.) * step(0., st.y) * step(st.y, 1.);
  o = vec4(outc * inside, 1.);
}`;

class FilmPost {
  constructor(w = 1440, h = 1080) {
    this.w = w; this.h = h;
    this.canvas = document.createElement('canvas'); this.canvas.width = w; this.canvas.height = h;
    const gl = this.gl = this.canvas.getContext('webgl2', { preserveDrawingBuffer: true, premultipliedAlpha: false });
    if (!gl) throw new Error('webgl2 unavailable');
    const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; };
    const pr = this.pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr));
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    this.tex = [0, 1, 2].map(() => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); return t; });
    this.U = {}; for (const n of ['T', 'B', 'C', 'R', 'frame', 'seed', 'uStr', 'uGrain', 'uFlick', 'uScr', 'uBurn', 'uVig', 'uHal', 'uSepia', 'uBlack', 'uWhite', 'uCon', 'uExpo', 'uHasC', 'uWeave']) this.U[n] = gl.getUniformLocation(pr, n);
    this.small = document.createElement('canvas'); this.small.width = Math.round(w / 8); this.small.height = Math.round(h / 8);
    this.sg = this.small.getContext('2d', { willReadFrequently: true });
    this.mean = .5;
  }
  // per-frame random helpers (deterministic)
  static rnd(n) { n = Math.sin(n * 91.3458 + 17.123) * 47453.5453; return n - Math.floor(n); }
  weaveAt(frame, p = {}) {
    const k = (p.strength ?? .6) * (p.weave ?? 1), cr = p.crank ?? 1, r = FilmPost.rnd;
    const f = frame * cr;
    let x = (Math.sin(f * .31) * .6 + Math.sin(f * .113 + 1.3) * .8 + (r(frame) - .5) * .5) * 1.4 * k;
    let y = (Math.sin(f * .23 + .7) * .7 + Math.sin(f * .071 + 2.1) * .9 + (r(frame + 99) - .5) * .6) * 1.6 * k;
    if (r(Math.floor(frame / 2) * 3.7) < .025 * k) y += 4 * k;                       // occasional perforation jump
    return [x, y + (p.jump || 0)];
  }
  flickerAt(frame, p = {}) {
    const k = (p.strength ?? .6) * (p.flicker ?? 1), cr = p.crank ?? 1, r = FilmPost.rnd;
    const f = frame * cr;
    return 1 + ((r(frame) - .5) * .09 + Math.sin(f * 1.9) * .025 * cr + Math.sin(f * .37) * .02) * k;
  }
  render(src, p = {}, colorMask = null) {
    const gl = this.gl, U = this.U, frame = p.frame ?? 0;
    gl.viewport(0, 0, this.w, this.h); gl.useProgram(this.pr);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
    this.sg.drawImage(src, 0, 0, this.small.width, this.small.height);
    // mean brightness (for theatre spill light)
    const d = this.sg.getImageData(0, 0, this.small.width, this.small.height).data; let s = 0; for (let i = 0; i < d.length; i += 16) s += d[i]; this.mean = s / (d.length / 16) / 255;
    this.sg.filter = 'blur(2px)'; this.sg.drawImage(this.small, 0, 0); this.sg.filter = 'none';
    const up = (i, img) => { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, this.tex[i]); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img); };
    up(0, src); up(1, this.small); if (colorMask) up(2, colorMask); else { gl.activeTexture(gl.TEXTURE2); gl.bindTexture(gl.TEXTURE_2D, this.tex[2]); }
    gl.uniform1i(U.T, 0); gl.uniform1i(U.B, 1); gl.uniform1i(U.C, 2);
    gl.uniform2f(U.R, this.w, this.h); gl.uniform1f(U.frame, frame); gl.uniform1f(U.seed, p.seed ?? 3.1);
    const str = p.strength ?? .6;
    gl.uniform1f(U.uStr, str); gl.uniform1f(U.uGrain, p.grain ?? 1); gl.uniform1f(U.uFlick, p.flicker ?? 1);
    gl.uniform1f(U.uScr, p.scratches ?? 1); gl.uniform1f(U.uBurn, p.burn ?? 1); gl.uniform1f(U.uVig, p.vignette ?? 1);
    gl.uniform1f(U.uHal, p.halation ?? 1); gl.uniform1f(U.uSepia, p.sepia ?? .12);
    gl.uniform1f(U.uBlack, p.black ?? .055); gl.uniform1f(U.uWhite, p.white ?? .93); gl.uniform1f(U.uCon, p.contrast ?? 1);
    gl.uniform1f(U.uExpo, (p.exposure ?? 1) * this.flickerAt(frame, p)); gl.uniform1f(U.uHasC, colorMask ? 1 : 0);
    const [wx, wy] = this.weaveAt(frame, p); gl.uniform2f(U.uWeave, wx, wy);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    return this.canvas;
  }
}

// dust specks, hairs and the odd blotch, drawn over the processed frame (2D). Deterministic per frame.
function damage(g, x, y, w, h, frame, strength = .6, o = {}) {
  const r = FilmPost.rnd, k = strength;
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
  const nDust = Math.floor((2 + r(frame * 1.3) * 7) * k * (o.dust ?? 1));
  for (let i = 0; i < nDust; i++) {
    const a = r(frame * 7.1 + i * 3.3), b = r(frame * 3.7 + i * 5.9), c = r(frame * 1.9 + i * 8.1);
    const px = x + a * w, py = y + b * h, rad = .8 + c * c * 3.2;
    const white = r(frame + i * 11.7) < .35;
    g.fillStyle = white ? `rgba(240,232,215,${.55 + c * .4})` : `rgba(12,10,8,${.6 + c * .35})`;
    g.beginPath();
    const m = 5 + Math.floor(c * 4);
    for (let j = 0; j < m; j++) { const an = j / m * Math.PI * 2, rr = rad * (.6 + r(i * 13 + j + frame) * .7); j ? g.lineTo(px + Math.cos(an) * rr, py + Math.sin(an) * rr) : g.moveTo(px + Math.cos(an) * rr, py + Math.sin(an) * rr); }
    g.fill();
  }
  // a hair caught in the gate: stays for ~10 frames, wiggles
  const hairLife = Math.floor(frame / 11);
  if (r(hairLife * 5.3) < .22 * k * (o.hair ?? 1)) {
    const hx = x + r(hairLife * 2.1) * w, hy = y + r(hairLife * 4.7) * h, len = 40 + r(hairLife) * 90;
    g.strokeStyle = 'rgba(10,8,6,.75)'; g.lineWidth = 1.2; g.beginPath();
    for (let j = 0; j <= 20; j++) { const u = j / 20, px = hx + Math.sin(u * 5 + hairLife) * 14 * u + u * len * .6, py = hy + u * len + Math.sin(u * 9 + frame * .3) * 3; j ? g.lineTo(px, py) : g.moveTo(px, py); }
    g.stroke();
  }
  // rare big blotch (cue-mark-like) for a single frame
  if (r(frame * 2.9) < .012 * k * (o.blotch ?? 1)) {
    const bx = x + (.2 + r(frame) * .6) * w, by = y + (.15 + r(frame * 3) * .3) * h;
    g.fillStyle = 'rgba(245,238,222,.5)'; g.beginPath(); g.arc(bx, by, 10 + r(frame * 5) * 18, 0, 7); g.fill();
  }
  g.restore();
}

const __e = {};
if (typeof FilmPost !== 'undefined') __e.FilmPost = FilmPost;
if (typeof damage !== 'undefined') __e.damage = damage;
return __e;
})();
__M.cards = (() => {
// Intertitle cards (art-deco border + serif), iris, and the theatre around the 4:3 gate.
const { grey } = __M.ink;
const CARD_BG = '#0e0d0b', CARD_FG = '#ece5d5';
const FONT_BODY = 'Old Standard TT', FONT_TITLE = 'Playfair Display SC';

// ---- art-deco border ----
// level 0 = one heavy rule (a shout), 1 = double rule + stepped corners + fans, 2 = + vines and flowers (tender)
function decoBorder(g, x, y, w, h, level = 1, col = CARD_FG, seed = 1) {
  g.save(); g.strokeStyle = col; g.fillStyle = col; g.lineCap = 'square';
  const wob = (v, i) => v + Math.sin(i * 12.9898 + seed * 78.233) * .5;   // hand-lettered card: tiny wobble
  if (level === 0) { g.lineWidth = 9; g.strokeRect(x + 30, y + 30, w - 60, h - 60); g.restore(); return; }
  const m1 = 34, m2 = 52, st = 34;
  g.lineWidth = 2.2; g.strokeRect(wob(x + m1, 1), wob(y + m1, 2), w - 2 * m1, h - 2 * m1);
  // inner heavy rule with stepped (notched) corners
  g.lineWidth = 5.5;
  const X0 = x + m2, Y0 = y + m2, X1 = x + w - m2, Y1 = y + h - m2, s = st;
  g.beginPath();
  g.moveTo(X0 + s, Y0); g.lineTo(X1 - s, Y0); g.lineTo(X1 - s, Y0 + s * .5); g.lineTo(X1 - s * .5, Y0 + s * .5); g.lineTo(X1 - s * .5, Y0 + s); g.lineTo(X1, Y0 + s);
  g.lineTo(X1, Y1 - s); g.lineTo(X1 - s * .5, Y1 - s); g.lineTo(X1 - s * .5, Y1 - s * .5); g.lineTo(X1 - s, Y1 - s * .5); g.lineTo(X1 - s, Y1);
  g.lineTo(X0 + s, Y1); g.lineTo(X0 + s, Y1 - s * .5); g.lineTo(X0 + s * .5, Y1 - s * .5); g.lineTo(X0 + s * .5, Y1 - s); g.lineTo(X0, Y1 - s);
  g.lineTo(X0, Y0 + s); g.lineTo(X0 + s * .5, Y0 + s); g.lineTo(X0 + s * .5, Y0 + s * .5); g.lineTo(X0 + s, Y0 + s * .5); g.closePath();
  g.stroke();
  // corner fans (sunburst) in the notches
  const fan = (cx, cy, a0) => { g.lineWidth = 1.6; for (let i = 0; i <= 6; i++) { const a = a0 + i / 6 * Math.PI / 2; g.beginPath(); g.moveTo(cx + Math.cos(a) * 6, cy + Math.sin(a) * 6); g.lineTo(cx + Math.cos(a) * 26, cy + Math.sin(a) * 26); g.stroke(); } g.beginPath(); g.arc(cx, cy, 4, 0, 7); g.fill(); };
  fan(x + m1, y + m1, 0); fan(x + w - m1, y + m1, Math.PI / 2); fan(x + w - m1, y + h - m1, Math.PI); fan(x + m1, y + h - m1, Math.PI * 1.5);
  // top/bottom centre diamonds with rules
  const dia = (cx, cy) => { g.beginPath(); g.moveTo(cx, cy - 11); g.lineTo(cx + 16, cy); g.lineTo(cx, cy + 11); g.lineTo(cx - 16, cy); g.closePath(); g.fill(); g.lineWidth = 2; g.beginPath(); g.moveTo(cx - 120, cy); g.lineTo(cx - 26, cy); g.moveTo(cx + 26, cy); g.lineTo(cx + 120, cy); g.stroke(); g.beginPath(); g.arc(cx - 132, cy, 3, 0, 7); g.arc(cx + 132, cy, 3, 0, 7); g.fill(); };
  dia(x + w / 2, y + m2 + 30); dia(x + w / 2, y + h - m2 - 30);
  if (level >= 2) {        // vines + small flowers along the sides
    g.lineWidth = 1.5;
    for (const side of [0, 1]) {
      const sx = side ? x + w - m2 - 26 : x + m2 + 26;
      g.beginPath();
      for (let i = 0; i <= 60; i++) { const u = i / 60, yy = y + m2 + 70 + u * (h - 2 * m2 - 140), xx = sx + Math.sin(u * Math.PI * 5) * 9 * (side ? -1 : 1); i ? g.lineTo(xx, yy) : g.moveTo(xx, yy); }
      g.stroke();
      for (let k = 0; k < 5; k++) {
        const u = (k + .5) / 5, yy = y + m2 + 70 + u * (h - 2 * m2 - 140), xx = sx + Math.sin(u * Math.PI * 5) * 9 * (side ? -1 : 1);
        for (let p = 0; p < 5; p++) { const a = p / 5 * Math.PI * 2; g.beginPath(); g.ellipse(xx + Math.cos(a) * 5, yy + Math.sin(a) * 5, 4.2, 2.4, a, 0, 7); g.fill(); }
        g.fillStyle = CARD_BG; g.beginPath(); g.arc(xx, yy, 2, 0, 7); g.fill(); g.fillStyle = col;
      }
    }
  }
  g.restore();
}

// ---- intertitle: spec = { lines:[{text, font, size, italic, caps, spacing}], level, seed, shake }
function intertitle(g, W, H, spec, t = 0) {
  g.save();
  g.fillStyle = CARD_BG; g.fillRect(0, 0, W, H);
  // faint fibre in the black card (it was a painted card photographed)
  g.globalAlpha = .06; for (let i = 0; i < 90; i++) { const a = Math.sin(i * 91.7) * 43758.5, b = a - Math.floor(a); const c = Math.sin(i * 17.3) * 9631.1, d = c - Math.floor(c); g.fillStyle = grey(.5 + d * .3); g.fillRect(b * W, d * H, 1 + d * 2, 1); }
  g.globalAlpha = 1;
  decoBorder(g, 0, 0, W, H, spec.level ?? 1, CARD_FG, spec.seed ?? 1);
  const lines = spec.lines, gap = spec.gap ?? 1.28;
  const total = lines.reduce((s, l) => s + l.size * gap, 0);
  let yy = H / 2 - total / 2 + (spec.dy ?? 0);
  for (const l of lines) {
    const f = `${l.italic ? 'italic ' : ''}${l.weight ?? 400} ${l.size}px "${l.font ?? FONT_BODY}"`;
    g.font = f; g.fillStyle = l.color ?? CARD_FG; g.textAlign = 'center'; g.textBaseline = 'middle';
    let sx = 0, sy = 0;
    if (spec.shake) { const k = Math.max(0, 1 - t / spec.shake) ; sx = Math.sin(t * 90) * 5 * k; sy = Math.cos(t * 77) * 4 * k; }
    const txt = l.caps ? l.text.toUpperCase() : l.text;
    if (l.spacing) { g.letterSpacing = l.spacing + 'px'; }
    g.fillText(txt, W / 2 + sx, yy + l.size * gap / 2 + sy);
    g.letterSpacing = '0px';
    if (l.rule) { const tw = g.measureText(txt).width; g.fillRect(W / 2 - tw * .35, yy + l.size * gap - 4, tw * .7, 2); }
    yy += l.size * gap;
  }
  g.restore();
}

// ---- iris: black outside a circle (soft optical edge). r in px; r >= diag means fully open.
function iris(g, W, H, cx, cy, r, feather = 3) {
  if (r > Math.hypot(W, H)) return;
  const rr = Math.max(0.01, r);
  const gr = g.createRadialGradient(cx, cy, Math.max(0, rr - feather), cx, cy, rr + feather);
  gr.addColorStop(0, 'rgba(8,7,6,0)'); gr.addColorStop(1, 'rgba(8,7,6,1)');     // beyond the last stop the gradient stays opaque
  g.save(); g.fillStyle = gr; g.fillRect(0, 0, W, H); g.restore();
}

// ---- theatre around the gate: black house, velvet curtains lit by the screen's spill ----
function theatre(g, W, H, gate, spill = .3, curtainOpen = 1) {
  // gate = {x, y, w, h}
  g.save();
  g.fillStyle = '#050404'; g.fillRect(0, 0, W, H);
  const drawCurtain = (x0, x1, side) => {
    const n = 7, cw = (x1 - x0) / n;
    for (let i = 0; i < n; i++) {
      const xa = x0 + i * cw, gr = g.createLinearGradient(xa, 0, xa + cw, 0);
      const near = side < 0 ? (i + 1) / n : 1 - i / n;           // folds nearer the screen catch more light
      const L = (.035 + spill * .16 * Math.pow(near, 1.6));
      gr.addColorStop(0, `rgb(${L * 255 * 1.25 | 0},${L * 255 * .62 | 0},${L * 255 * .55 | 0})`);
      gr.addColorStop(.5, `rgb(${L * 255 * .5 | 0},${L * 255 * .25 | 0},${L * 255 * .22 | 0})`);
      gr.addColorStop(1, `rgb(${L * 255 * 1.1 | 0},${L * 255 * .55 | 0},${L * 255 * .5 | 0})`);
      g.fillStyle = gr; g.fillRect(xa, 0, cw + 1, H);
    }
    // top shadow
    const tg = g.createLinearGradient(0, 0, 0, H); tg.addColorStop(0, 'rgba(0,0,0,.75)'); tg.addColorStop(.25, 'rgba(0,0,0,.2)'); tg.addColorStop(.8, 'rgba(0,0,0,.15)'); tg.addColorStop(1, 'rgba(0,0,0,.7)');
    g.fillStyle = tg; g.fillRect(x0, 0, x1 - x0, H);
  };
  const cwid = gate.x;
  const off = (1 - curtainOpen) * (W / 2);        // curtains close toward the centre
  drawCurtain(0 - 0 + off - (1 - curtainOpen) * 0, cwid + off, -1);
  drawCurtain(W - cwid - off, W - off, 1);
  g.restore();
}

const __e = {};
if (typeof CARD_BG !== 'undefined') __e.CARD_BG = CARD_BG;
if (typeof FONT_BODY !== 'undefined') __e.FONT_BODY = FONT_BODY;
if (typeof decoBorder !== 'undefined') __e.decoBorder = decoBorder;
if (typeof intertitle !== 'undefined') __e.intertitle = intertitle;
if (typeof iris !== 'undefined') __e.iris = iris;
if (typeof theatre !== 'undefined') __e.theatre = theatre;
if (typeof CARD_FG !== 'undefined') __e.CARD_FG = CARD_FG;
if (typeof FONT_TITLE !== 'undefined') __e.FONT_TITLE = FONT_TITLE;
return __e;
})();
window.SFI = __M.ink; window.SFR = __M.redraw; window.SFP = __M.film; window.SFC = __M.cards;
