// ink.bundle.js: LemoLab ink-wash motoru (MIT, commit d33bdea) tek klasik betik. Kaynak modüller lib/vendor/ altında, değiştirilmedi.
// Üretici: ran/tools/bundle_ink.py.
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
__M.ink = (() => {
// 水墨笔触引擎（Canvas2D）
// 一笔 = 中心线 + 压力轮廓 + 若干"笔毫"。湿笔的墨体画进 wet 画布（合成器里会晕开、积边），
// 干笔的笔毫画进 dry 画布（按墨量断开 → 飞白）。所有坐标是世界单位，由调用者 setTransform。
const { clamp, lerp, mulberry, hash, vnoise } = __M.lib;

const TONE = { jiao: .96, nong: .82, zhong: .6, dan: .34, qing: .16 }; // 焦浓重淡清

// Catmull-Rom 加密 → 等弧长重采样
function densify(P, per = 8) {
  if (P.length < 3) {
    const out = []; const [a, b] = [P[0], P[P.length - 1]];
    for (let i = 0; i <= per; i++) { const t = i / per; out.push([lerp(a[0], b[0], t), lerp(a[1], b[1], t), lerp(a[2] ?? 1, b[2] ?? 1, t)]); }
    return out;
  }
  const out = [];
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[Math.max(0, i - 1)], p1 = P[i], p2 = P[i + 1], p3 = P[Math.min(P.length - 1, i + 2)];
    for (let k = 0; k < per; k++) {
      const t = k / per, t2 = t * t, t3 = t2 * t;
      const f = (a, b, c, d) => .5 * (2 * b + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t2 + (-a + 3 * b - 3 * c + d) * t3);
      out.push([f(p0[0], p1[0], p2[0], p3[0]), f(p0[1], p1[1], p2[1], p3[1]), lerp(p1[2] ?? 1, p2[2] ?? 1, t)]);
    }
  }
  const l = P[P.length - 1]; out.push([l[0], l[1], l[2] ?? 1]);
  return out;
}
function resample(D, ds) {
  const acc = [0];
  for (let i = 1; i < D.length; i++) acc.push(acc[i - 1] + Math.hypot(D[i][0] - D[i - 1][0], D[i][1] - D[i - 1][1]));
  const L = acc[acc.length - 1] || 1e-6, n = Math.max(2, Math.min(600, Math.ceil(L / ds) + 1)), out = [];
  let j = 0;
  for (let i = 0; i < n; i++) {
    const s = L * i / (n - 1);
    while (j < D.length - 2 && acc[j + 1] < s) j++;
    const u = clamp((s - acc[j]) / ((acc[j + 1] - acc[j]) || 1e-6));
    out.push([lerp(D[j][0], D[j + 1][0], u), lerp(D[j][1], D[j + 1][1], u), lerp(D[j][2], D[j + 1][2], u)]);
  }
  return { pts: out, len: L };
}

// 压力轮廓
const PROF = {
  brush: s => Math.min(1, .45 + s / .1 * .55) * Math.pow(1 - s * .9, .45),          // 顿笔起、渐收
  even: s => Math.min(1, .55 + s / .05 * .45) * Math.min(1, .5 + (1 - s) / .06 * .5),
  tip: s => Math.pow(Math.sin(Math.PI * clamp(s * .96 + .02)), .6),                  // 两头尖
  lens: s => Math.pow(Math.sin(Math.PI * clamp(s)), .75),
  nail: s => Math.pow(1 - s, .7) * Math.min(1, .7 + s * 6),                          // 起笔重、出锋
  na: s => (.25 + .75 * Math.pow(clamp(s / .82), 1.4)) * (s > .82 ? Math.pow(1 - (s - .82) / .18, .6) : 1), // 捺：由轻到重、平出
  press: s => Math.min(1, .3 + s / .15 * .7) * Math.min(1, (1 - s) / .12 * .8 + .2),
  fan: s => (.4 + .6 * Math.pow(s, .8)) * Math.min(1, (1 - s) / .06 * .6 + .4) * Math.min(1, s / .05 * .5 + .5),
  robe: s => (.75 + .25 * s) * Math.min(1, s / .05 * .5 + .5) * Math.min(1, (1 - s) / .08 * .7 + .3),
  rise: s => Math.min(1, .12 + s / .14 * .88) * Math.min(1, (1 - s) / .08 * .7 + .3),
  cone: s => Math.pow(1 - s, .55) * Math.min(1, s / .04 * .6 + .4),
  dot: s => Math.pow(Math.sin(Math.PI * clamp(s * .9 + .05)), .45),
};

let SEED = 1;
function reseed(s) { SEED = s | 0; }

// 建一笔
// pts: [[x,y,(p)]]，o: {w, tone, dry, wet, prof, rough, nb, seed, ds, fade}
function mk(pts, o = {}) {
  const w = o.w ?? 4, seed = o.seed ?? (SEED = (SEED * 16807) % 2147483647);
  const ds = o.ds ?? Math.max(.25, w * .18);
  const { pts: P, len } = resample(densify(pts, o.per ?? 10), ds);
  const n = P.length, prof = typeof o.prof === 'function' ? o.prof : PROF[o.prof || 'brush'];
  const rough = o.rough ?? .12, ws = [], nx = [], ny = [];
  for (let i = 0; i < n; i++) {
    const s = i / (n - 1);
    ws.push(Math.max(w * .04, w * prof(s) * P[i][2] * (1 + rough * (vnoise(seed * .013 + (o.boil || 0) * .35 + s * (o.gapLen ?? len) / (w * 1.3 + 1)) * 2 - 1))));
    const a = P[Math.max(0, i - 1)], b = P[Math.min(n - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
    nx.push(-dy / L); ny.push(dx / L);
  }
  const dry = o.dry ?? .25;
  let side = o.side || 0;
  if (o.darkDir) {  // 自动决定浓的一侧：笔的平均法线朝向 darkDir 的那一边
    let ax = 0, ay = 0; for (let i = 0; i < n; i++) { ax += nx[i]; ay += ny[i]; }
    side = (Math.abs(o.side || 1)) * Math.sign(ax * o.darkDir[0] + ay * o.darkDir[1] || 1);
  }
  const nb = o.nb ?? Math.round(clamp(w * 1.1, 4, 56));
  const R = mulberry(seed);
  const br = [];
  for (let j = 0; j < nb; j++) {
    const off = (j + .5) / nb - .5 + (R() - .5) * .6 / nb;
    const edge = Math.abs(off) * 2;                          // 0 中心 → 1 边
    br.push({
      off, bw: w / nb * (1.0 + R() * 1.1), a: .55 + R() * .45, ph: R() * 1000,
      load: 1 - dry * (.15 + .85 * edge) * (.5 + R() * .7),  // 边缘笔毫墨少
      gs: .5 + R() * 1.6,                                    // 断墨的尺度
      end: 1 - R() * dry * .35,
    });
  }
  return { P, n, len, ws, nx, ny, w, tone: o.tone ?? TONE.nong, dry, wet: o.wet ?? 0, br, seed, fade: o.fade ?? dry * .55, bodyK: o.body ?? 1, brK: o.bristle ?? 1, color: o.color || null, side, brWet: !!o.brWet, solid: !!o.solid, gapLen: o.gapLen ?? null };
}

// 画一笔。L = {wet, dry} 两个 2D 上下文；p = 画到哪（0..1）；am = 整体透明度
function draw(L, s, p = 1, am = 1) {
  if (p <= 0 || am <= 0) return;
  p = clamp(p);
  const { P, n, ws, nx, ny } = s, m = (n - 1) * p, k = Math.floor(m), f = m - k;
  const cnt = f > .001 && k < n - 1 ? k + 2 : k + 1;
  const X = i => i <= k ? P[i][0] : lerp(P[k][0], P[k + 1][0], f), Y = i => i <= k ? P[i][1] : lerp(P[k][1], P[k + 1][1], f);
  const CC = s.color ? s.color.join(',') : '0,0,0';
  const WW = i => ws[Math.min(i, n - 1)] * (p < 1 && i >= cnt - 2 ? .75 : 1);
  // 墨体
  const bodyA = s.tone * Math.pow(1 - s.dry, 1.6) * s.bodyK * am;
  if (bodyA > .004) {
    const path = new Path2D();
    for (let i = 0; i < cnt; i++) { const j = Math.min(i, n - 1), hw = WW(i) / 2; const x = X(i) + nx[j] * hw, y = Y(i) + ny[j] * hw; i ? path.lineTo(x, y) : path.moveTo(x, y); }
    for (let i = cnt - 1; i >= 0; i--) { const j = Math.min(i, n - 1), hw = WW(i) / 2; path.lineTo(X(i) - nx[j] * hw, Y(i) - ny[j] * hw); }
    path.closePath();
    // 沿笔方向墨量递减（干笔更明显）
    const g = (c, a) => {
      if (a <= .003) return;
      const gr = c.createLinearGradient(P[0][0], P[0][1], P[n - 1][0], P[n - 1][1]);
      gr.addColorStop(0, `rgba(${CC},${clamp(a)})`); gr.addColorStop(1, `rgba(${CC},${clamp(a * (1 - s.fade))})`);
      c.fillStyle = gr; c.fill(path);
    };
    if (s.color) { if (L.col) g(L.col, bodyA); }
    else {
      if (s.solid) { if (L.dry) g(L.dry, bodyA * .92); if (L.wet && s.wet > 0) g(L.wet, bodyA * s.wet); }
      else {
        if (s.wet > 0 && L.wet) g(L.wet, bodyA * s.wet);
        if (s.wet < 1 && L.dry) g(L.dry, bodyA * (1 - s.wet) * .8);
      }
    }
  }
  // 笔毫（飞白）
  const c = s.color ? L.col : (s.brWet ? L.wet : L.dry); if (!c || s.brK <= 0) return;
  const brA = s.tone * am * s.brK * (s.brWet ? 1 : (s.wet > .6 ? .12 : 1));
  c.lineCap = 'round'; c.lineJoin = 'round'; c.strokeStyle = `rgb(${CC})`;
  const dsl = (s.gapLen ?? s.len) / (n - 1);
  for (const b of s.br) {
    const e = Math.min(m, (n - 1) * b.end), kk = Math.floor(e); if (kk < 1) continue;
    const lat = s.side ? lerp(1 - Math.abs(s.side), 1, clamp(b.off * Math.sign(s.side) * 1.6 + .5)) : 1;
    c.globalAlpha = clamp(brA * b.a * lat);
    c.lineWidth = b.bw;
    c.beginPath(); let on = false;
    const gsc = Math.max(6, s.w * 1.4) * b.gs;
    for (let i = 0; i <= kk; i++) {
      const u = i / (n - 1), sl = i * dsl;
      // 墨量：随笔程下降，干笔下降更快；噪声决定断在哪
      const ink = b.load - s.dry * (.08 + 1.15 * Math.pow(u, 1.25));
      const v = ink + (vnoise(b.ph + sl / gsc) - .5) * .9 * s.dry + (vnoise(b.ph * 1.7 + sl / (gsc * .18)) - .5) * .25 * s.dry;
      if (v > .42 * s.dry + .02) {
        const hw = ws[i] * (b.off + (vnoise(b.ph * 3 + sl / (gsc * 2)) - .5) * .07), x = P[i][0] + nx[i] * hw, y = P[i][1] + ny[i] * hw;
        on ? c.lineTo(x, y) : c.moveTo(x, y); on = true;
      } else on = false;
    }
    c.stroke();
  }
  c.globalAlpha = 1;
}

// 按顺序画一组笔（书写顺序），p ∈ [0,1]
function drawSeq(L, S, p = 1, am = 1, overlap = .15) {
  const N = S.length; if (!N) return;
  if (p >= 1) { for (const s of S) draw(L, s, 1, am); return; }
  // 按长度分配时间
  const tot = S.reduce((a, s) => a + s.len + 20, 0); let acc = 0;
  for (const s of S) {
    const t0 = acc / tot, t1 = (acc + s.len + 20) / tot; acc += s.len + 20;
    draw(L, s, (p - t0) / ((t1 - t0) * (1 + overlap)), am);
  }
}

// 墨点（点苔、溅墨）：一个小的压扁椭圆团
function blot(c, x, y, r, a, rot = 0, sq = 1, seed = 0) {
  if (a <= .003 || r <= .05) return;
  c.save(); c.translate(x, y); c.rotate(rot); c.scale(1, sq);
  c.globalAlpha = clamp(a); c.fillStyle = '#000';
  c.beginPath();
  const N = 18, ph = seed * 7.13 + x * .01;
  for (let i = 0; i <= N; i++) {
    const t = i / N * Math.PI * 2, rr = r * (.78 + .44 * vnoise(ph + i * .9) + .12 * Math.sin(t * 3 + ph));
    i ? c.lineTo(Math.cos(t) * rr, Math.sin(t) * rr) : c.moveTo(Math.cos(t) * rr, Math.sin(t) * rr);
  }
  c.fill();
  c.restore(); c.globalAlpha = 1;
}

// 墨块：多边形湿墨（斗笠、远山、袍的底色）。边缘细分 + 噪声抖动，可带线性渐变 g = [x0,y0,x1,y1,a0,a1]
function mass(c, poly, a, jit = 0, seed = 0, g = null) {
  if (a <= .003) return;
  const pts = [];
  const N = poly.length;
  for (let i = 0; i < N; i++) {
    const p = poly[i], q = poly[(i + 1) % N], L = Math.hypot(q[0] - p[0], q[1] - p[1]);
    const k = jit ? Math.max(1, Math.min(24, Math.round(L / Math.max(2, jit * 2.5)))) : 1;
    const nx = -(q[1] - p[1]) / (L || 1), ny = (q[0] - p[0]) / (L || 1);
    for (let j = 0; j < k; j++) {
      const u = j / k, d = jit ? (vnoise(seed * 3.1 + i * 5.3 + u * k * .8) - .5) * jit * 2 : 0;
      pts.push([lerp(p[0], q[0], u) + nx * d, lerp(p[1], q[1], u) + ny * d]);
    }
  }
  c.globalAlpha = 1;
  if (g) { const gr = c.createLinearGradient(g[0], g[1], g[2], g[3]); gr.addColorStop(0, `rgba(0,0,0,${clamp(a * g[4])})`); gr.addColorStop(1, `rgba(0,0,0,${clamp(a * g[5])})`); c.fillStyle = gr; }
  else { c.fillStyle = `rgba(0,0,0,${clamp(a)})`; }
  c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(p[0], p[1]) : c.moveTo(p[0], p[1])); c.closePath(); c.fill();
}

// 实用：二次贝塞尔点列
function qpts(x0, y0, cx, cy, x1, y1, n = 8, p0 = 1, p1 = 1) {
  const out = [];
  for (let i = 0; i <= n; i++) { const t = i / n, u = 1 - t; out.push([u * u * x0 + 2 * u * t * cx + t * t * x1, u * u * y0 + 2 * u * t * cy + t * t * y1, lerp(p0, p1, t)]); }
  return out;
}


const __e = {};
if (typeof hash !== 'undefined') __e.hash = hash;
if (typeof vnoise !== 'undefined') __e.vnoise = vnoise;
if (typeof TONE !== 'undefined') __e.TONE = TONE;
if (typeof reseed !== 'undefined') __e.reseed = reseed;
if (typeof mk !== 'undefined') __e.mk = mk;
if (typeof draw !== 'undefined') __e.draw = draw;
if (typeof drawSeq !== 'undefined') __e.drawSeq = drawSeq;
if (typeof blot !== 'undefined') __e.blot = blot;
if (typeof mass !== 'undefined') __e.mass = mass;
if (typeof qpts !== 'undefined') __e.qpts = qpts;
return __e;
})();
__M.comp = (() => {
// comp_hizli.js (Ran): LemoLab ink-wash birleştiricisinin (lib/vendor/ink-wash/comp.js, MIT) hızlı sürümü.
// Fark yalnız hesaplama sırası: kâğıt rengi ve bütün durağan gürültü alanları (fbm/vn) yalnız konuma bağlı olduğundan
// bir kez ön geçişte dokulara yazılır; her karede yalnız okunur. Görünüm aynı (gürültü 8 bit nicemlenir).
// Kullanılmayan özellikler (A/B mürekkep geçişi, "rev" açılışı) çıkarıldı. Yazılımsal WebGL'de (SwiftShader) kare süresi ~10 kat kısalır.
const VS = `#version 300 es
in vec2 p; void main(){ gl_Position = vec4(p,0,1); }`;
const NOISE = `
float h21(vec2 p){ p = fract(p*vec2(123.34, 456.21)); p += dot(p, p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.-2.*f);
  return mix(mix(h21(i), h21(i+vec2(1,0)), f.x), mix(h21(i+vec2(0,1)), h21(i+vec2(1,1)), f.x), f.y); }
float fbm(vec2 p){ float a = 0., w = .5; for(int i=0;i<5;i++){ a += w*vn(p); p = p*2.03 + 17.1; w *= .5; } return a; }
float fiber(vec2 p, float ang){ float c = cos(ang), s = sin(ang); vec2 q = vec2(c*p.x + s*p.y, -s*p.x + c*p.y);
  float n = vn(vec2(q.x*.018, q.y*.9)); return smoothstep(.78, .95, n); }`;
// ön geçiş: mode 0 kâğıt rengi, 1 disp/feather, 2 g1/g2/j, 3 tooth/sp
const PRE = `#version 300 es
precision highp float; out vec4 o;
uniform vec2 res; uniform int mode; uniform vec3 paperCol; uniform vec3 X;
${NOISE}
void main(){
  vec2 fc = gl_FragCoord.xy; fc.y = res.y - fc.y;
  vec2 p = (fc + X.xy) / X.z;
  if (mode == 0) {
    float fine = clamp(X.z*1.2, 0., 1.);
    float cloud = fbm(p*.0028) - .5, cloud2 = fbm(p*.011 + 3.) - .5;
    float fb = fiber(p, .35) + fiber(p + 91., 2.1) * .8 + fiber(p*1.7 + 13., 1.2) * .6;
    float grain = vn(p*.9) - .5;
    vec3 c = paperCol * (1. + cloud*.07 + cloud2*.03*fine + grain*.035*fine);
    c += vec3(.018,.016,.012) * fb * fine;
    c -= vec3(.012,.014,.018) * smoothstep(.65,.9, vn(p*.05 + 7.)) * fine;
    o = vec4(c, 1.);
  } else if (mode == 1) {
    o = vec4(fbm(p*.012), fbm(p*.012 + 31.), vn(p*.21), vn(p*.21 + 7.));
  } else if (mode == 2) {
    o = vec4(vn(p*.35), fbm(p*.06), vn(p*.7), vn(p*.7 + 5.));
  } else {
    float tooth = smoothstep(.62, .9, vn(p*.55 + 3.));
    float sp = smoothstep(.2, .45, vn(p*.8 + 11.));
    o = vec4(tooth, sp, 0., 1.);
  }
}`;
const FS = `#version 300 es
precision highp float; out vec4 o;
uniform sampler2D wA, dA, cA, NP, N1, N2, N3;
uniform vec2 res; uniform vec2 shake; uniform float flash, fade, vig, warm, bleed, rimK; uniform vec3 paperCol;
const vec2 PD[12] = vec2[](vec2(-.326,-.406), vec2(-.840,-.074), vec2(-.696,.457), vec2(-.203,.621), vec2(.962,-.195), vec2(.473,-.480),
  vec2(.519,.767), vec2(.185,-.893), vec2(.507,.064), vec2(.896,.412), vec2(-.322,-.933), vec2(-.792,-.598));
void main(){
  vec2 fc = gl_FragCoord.xy; fc.y = res.y - fc.y; fc += shake;
  vec2 uvn = clamp(fc, vec2(0.), res - 1.) / res;
  vec3 pc = texture(NP, uvn).rgb;
  vec4 n1 = texture(N1, uvn), n2 = texture(N2, uvn), n3 = texture(N3, uvn);
  float R = bleed;
  vec2 disp = n1.xy - .5, feather = n1.zw - .5;
  vec2 q = fc + disp * R * 1.1 + feather * R * .35;
  float a = 0., b = 0.;
  for (int i = 0; i < 12; i++) { a += texture(wA, (q + PD[i] * R * .5) / res).a; b += texture(wA, (q + PD[i] * R * 1.35) / res).a; }
  a /= 12.; b /= 12.;
  float s0 = texture(wA, q / res).a;
  float edge = max(0., a - b);
  float wet = mix(s0, a, .72) * (.86 + .22*n2.y) + edge * rimK * (.8 + .5*n2.x) + b * .10;
  vec2 j = n2.zw - .5;
  float dry = texture(dA, (fc + j * 1.6) / res).a;
  float tooth = n3.x * .45;
  dry *= 1. - tooth * (1. - dry*.5);
  float D = clamp(1. - (1. - clamp(wet,0.,1.)) * (1. - clamp(dry,0.,1.)), 0., 1.);
  vec3 inkc = mix(vec3(.52,.55,.58), vec3(.075,.068,.062), smoothstep(.0, .85, D));
  vec3 c = pc * mix(vec3(1.), inkc, clamp(D*1.05, 0., 1.));
  vec4 col = texture(cA, fc / res);
  float sp = n3.y * .25 + .75;
  c = mix(c, col.rgb * (pc / paperCol), col.a * sp);
  vec2 uv = gl_FragCoord.xy / res - .5;
  c *= 1. - vig * dot(uv*vec2(1.,.9), uv*vec2(1.,.9)) * 1.2;
  c = mix(c, c * vec3(1.02, .99, .94), warm);
  c = mix(c, paperCol, flash);
  c = mix(c, vec3(0.), fade);
  o = vec4(clamp(c, 0., 1.), 1.);
}`;

function makeComp(canvas) {
  const gl = canvas.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false });
  if (!gl) throw new Error('no webgl2');
  const W = canvas.width, H = canvas.height;
  const sh = (t, s) => { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(x)); return x; };
  const prog = fs => { const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr); if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr)); return pr; };
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const bindAttr = pr => { const loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0); };
  const mkTex = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); return t; };
  // ön geçiş: dört durağan doku
  const pre = prog(PRE); gl.useProgram(pre); bindAttr(pre);
  const PU = n => gl.getUniformLocation(pre, n);
  gl.uniform2f(PU('res'), W, H); gl.uniform3f(PU('paperCol'), .95, .925, .87); gl.uniform3f(PU('X'), 0, 0, 1);
  const fb = gl.createFramebuffer(), noise = [];
  for (let m = 0; m < 4; m++) {
    const t = mkTex(); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, W, H, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, fb); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
    gl.viewport(0, 0, W, H); gl.uniform1i(PU('mode'), m); gl.drawArrays(gl.TRIANGLES, 0, 3); noise.push(t);
  }
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  // ana geçiş
  const pr = prog(FS); gl.useProgram(pr); bindAttr(pr);
  const U = n => gl.getUniformLocation(pr, n);
  const tex = ['wA', 'dA', 'cA'].map((n, i) => { gl.activeTexture(gl.TEXTURE0 + i); const t = mkTex(); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4)); gl.uniform1i(U(n), i); return t; });
  ['NP', 'N1', 'N2', 'N3'].forEach((n, k) => { gl.activeTexture(gl.TEXTURE3 + k); gl.bindTexture(gl.TEXTURE_2D, noise[k]); gl.uniform1i(U(n), 3 + k); });
  const up = (i, cv) => { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, tex[i]); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cv); };
  return function composite(A, B, o = {}) {
    gl.useProgram(pr); gl.viewport(0, 0, W, H);
    up(0, A.wet); up(1, A.dry); up(2, A.col);
    gl.uniform2f(U('res'), W, H);
    gl.uniform1f(U('bleed'), o.bleed ?? 6); gl.uniform1f(U('rimK'), o.rim ?? .8);
    const sk = o.shake || [0, 0]; gl.uniform2f(U('shake'), sk[0], sk[1]);
    gl.uniform1f(U('flash'), o.flash ?? 0); gl.uniform1f(U('fade'), o.fade ?? 0);
    gl.uniform1f(U('vig'), o.vig ?? .22); gl.uniform1f(U('warm'), o.warm ?? .5);
    gl.uniform3f(U('paperCol'), .95, .925, .87);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
}

function layerSet(W = 1920, H = 1080) {
  const mk = () => { const c = document.createElement('canvas'); c.width = W; c.height = H; return c; };
  const wet = mk(), dry = mk(), col = mk();
  const L = { wet, dry, col, W, H, cw: wet.getContext('2d'), cd: dry.getContext('2d'), cc: col.getContext('2d') };
  L.ink = { wet: L.cw, dry: L.cd, col: L.cc };
  L.clear = () => { for (const c of [L.cw, L.cd, L.cc]) { c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.clearRect(0, 0, W, H); } };
  L.xf = (s, tx, ty) => { for (const c of [L.cw, L.cd, L.cc]) c.setTransform(s, 0, 0, s, tx, ty); };
  return L;
}

const __e = {};
if (typeof makeComp !== 'undefined') __e.makeComp = makeComp;
if (typeof layerSet !== 'undefined') __e.layerSet = layerSet;
return __e;
})();
__M.land = (() => {
// 山水：远山（湿墨渐隐入雾）、中山（披麻皴 + 点苔）、崖石（斧劈）、松、芦苇、墨圈涟漪
const { mk, draw, mass, blot, TONE } = __M.ink;
const { mulberry, lerp, clamp, vnoise } = __M.lib;

const fbm = x => vnoise(x) * .55 + vnoise(x * 2.1 + 17) * .28 + vnoise(x * 4.7 + 41) * .17;

// 2D 值噪声
const h2 = (x, y) => { const n = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return n - Math.floor(n); };
function vn2(x, y) {
  const i = Math.floor(x), j = Math.floor(y), f = x - i, g = y - j, u = f * f * (3 - 2 * f), v = g * g * (3 - 2 * g);
  return lerp(lerp(h2(i, j), h2(i + 1, j), u), lerp(h2(i, j + 1), h2(i + 1, j + 1), u), v);
}
const fbm2 = (x, y) => vn2(x, y) * .5 + vn2(x * 2.07 + 5.1, y * 2.07 + 1.3) * .3 + vn2(x * 4.3 + 9, y * 4.3 + 3) * .2;

// 山脊：尖峰（指数衰减，p 越小越尖）+ 分形起伏。peaks: [[x, h, w]]
function ridgeFn(peaks, base, seed = 1, rough = 18) {
  return x => {
    let y = 0;
    for (const [px, h, w] of peaks) { const d = Math.abs(x - px) / w; y = Math.max(y, h * Math.exp(-Math.pow(d, 1.7)) * (1 - .12 * Math.exp(-d * d * 30))); }
    const n = (fbm(x * .004 + seed) - .5) * rough + (vnoise(x * .018 + seed * 3) - .5) * rough * .45 + (vnoise(x * .07 + seed * 5) - .5) * rough * .12;
    return base - y * (1 + (vnoise(x * .01 + seed) - .5) * .25) - n;
  };
}

// 山体（逐像素）：山脊下一道浓边往下渐淡，山脚被横向的雾带切断；返回缓存画布
// o: {W, H, ridge, depth, tone, rim(山脊浓边), rimW, mist(雾量), seed}
function mountainLayer(o) {
  const W = o.W, H = o.H, cv = document.createElement('canvas'); cv.width = W; cv.height = H;
  const c = cv.getContext('2d'), img = c.createImageData(W, H), D = img.data;
  const sd = o.seed || 1, depth = o.depth, rimW = o.rimW || 16;
  for (let x = 0; x < W; x++) {
    const r = o.ridge(x + (o.x0 || 0)), y0 = Math.max(0, Math.floor(r));
    const colK = .8 + .4 * vn2(x * .012 + sd, 3.3);                     // 竖向的浓淡变化（像笔意）
    const xm = o.xmask ? o.xmask(x + (o.x0 || 0)) : 1; if (xm <= 0) continue;
    for (let y = y0; y < Math.min(H, r + depth); y++) {
      const d = y - r; if (d < -1) continue;
      const cover = d < 0 ? 1 + d : 1;
      const f = Math.pow(1 - d / depth, 1.6);
      const tex = .7 + .6 * fbm2((x + (o.x0 || 0)) * .018 + sd, y * .03);
      const mist = o.mist ? clamp(1 - o.mist * Math.max(0, fbm2((x + (o.x0 || 0)) * .0025 + sd * 2, y * .012) - .38) * 3.2) : 1;
      const a = o.tone * (f * .6 * tex + Math.exp(-d / rimW) * (o.rim ?? .7) * colK) * mist * cover * xm;
      D[(y * W + x) * 4 + 3] = Math.min(255, a * 255);
    }
  }
  c.putImageData(img, 0, 0);
  return cv;
}

// 皴 + 苔点（画在山体之上）
function cun(L, o) {
  const R = mulberry(o.seed || 1);
  const nC = Math.round((o.x1 - o.x0) / 100 * (o.cun ?? 1.2));
  for (let i = 0; i < nC; i++) {
    const x = lerp(o.x0 + 20, o.x1 - 20, R()), y = o.ridge(x) + 4 + R() * 30 * (o.cunDepth || 1);
    const sl = (o.ridge(x + 8) - o.ridge(x - 8)) / 16;
    const len = (25 + R() * 60) * (o.cunLen || 1), dx = clamp(sl * len * .8, -len * .7, len * .7);
    const pts = [[x, y], [x + dx * .45 + (R() - .5) * 6, y + len * .5], [x + dx * .8, y + len]];
    draw(L, mk(pts, { w: (7 + R() * 9) * (o.cunW || 1), tone: o.tone * (1.3 + R() * .8), darkDir: [-1, 0], side: .7, brWet: true, body: .25, dry: .6 + R() * .2, wet: .8, prof: 'tip', seed: (o.seed || 1) * 1000 + i }), 1, .75);
  }
  const nM = Math.round((o.x1 - o.x0) / 100 * (o.moss ?? 1.5));
  for (let i = 0; i < nM; i++) {
    const x = lerp(o.x0 + 10, o.x1 - 10, R()), y = o.ridge(x) + R() * 8;
    for (let k = 0; k < 3; k++) blot(L.wet, x + (R() - .5) * 14, y + R() * 5, (1.2 + R() * 2.2) * (o.mossR || 1), clamp(o.tone * 3), R() * 3, .6 + R() * .3, (o.seed || 1) + i * 3 + k);
  }
}

// 崖石：勾（断续的焦墨轮廓）+ 皴（沿结构线的短斧劈）+ 染（阴面淡墨，往下消失在雾里）+ 点（苔）。flip=-1 时崖面朝左
function cliff(L, x, y, s, seed = 3, flip = 1) {
  const R = mulberry(seed);
  const T = p => [x + p[0] * s * flip, y + p[1] * s];
  const top = [[-40, 3], [0, -1], [45, 1], [90, -2], [128, 1], [152, 4]];
  const face = [[152, 4], [172, 22], [167, 62], [188, 98], [183, 142], [204, 192], [214, 262]];
  const facets = [[[112, 4], [132, 42], [127, 92], [148, 150], [152, 240]], [[62, 3], [80, 52], [74, 120], [94, 210]], [[18, 2], [30, 60], [26, 150]]];
  // 染：整体淡墨 + 各阴面一笔含墨（往下变淡）
  mass(L.wet, [...top, ...face.slice(1), [70, 262], [10, 150], [-25, 40]].map(T), .2, 2 * s, seed, [0, y, 0, y + 250 * s, 1.2, .05]);
  const shade = [face, ...facets];
  shade.forEach((f, i) => draw(L, mk(f.map(p => [p[0] - 12, p[1] + 4]).map(T), { w: (i === 0 ? 34 : 22) * s, tone: i === 0 ? .55 : .35, darkDir: [flip, 0], side: .85, brWet: true, body: .3, dry: .55, wet: .9, prof: 'rise', seed: seed * 5 + i }), 1, .9));
  // 勾：崖顶与崖面，分段、提按
  const outline = (pts, w, sd) => { for (let i = 0; i < pts.length - 1; i += 2) draw(L, mk(pts.slice(i, i + 3).map((p, j) => [...T(p), j === 1 ? 1.2 : .7]), { w: w * s, tone: .92, dry: .5, wet: .25, prof: 'brush', seed: sd + i })); };
  outline(top, 4.2, seed * 13); outline(face, 4.6, seed * 17);
  facets.forEach((f, i) => draw(L, mk(f.slice(0, 3 + (i === 0 ? 1 : 0)).map(T), { w: (3 - i * .6) * s, tone: .85, dry: .6, wet: .2, prof: 'tip', seed: seed * 23 + i })));
  // 皴：沿结构线的短斧劈
  for (const f of [face, ...facets]) {
    for (let i = 0; i < 6; i++) {
      const u = R() * .75, k = Math.floor(u * (f.length - 1)), fr = u * (f.length - 1) - k;
      const px = lerp(f[k][0], f[k + 1][0], fr) - 4 - R() * 10, py = lerp(f[k][1], f[k + 1][1], fr) + 4;
      const len = 16 + R() * 22;
      draw(L, mk([[px, py], [px - len * .35, py + len * .5], [px - len * .5, py + len]].map(T), { w: (7 + R() * 7) * s, tone: .75, dry: .6, wet: .4, prof: 'nail', seed: seed * 50 + i + f.length * 7 }), 1, clamp(1.3 - py / 200));
    }
  }
  // 点：崖顶苔点（成簇）
  for (let c = 0; c < 5; c++) {
    const cx = R() * 150, cy = 0;
    for (let i = 0; i < 4; i++) { const p = T([cx + (R() - .5) * 16, cy - 1 + R() * 4]); blot(L.wet, p[0], p[1], (1.2 + R() * 2) * s, .85, R() * 3, .6, c * 10 + i + seed); }
  }
  for (let i = 0; i < 6; i++) { const px = 10 + R() * 140; const p0 = T([px, 0]); draw(L, mk([p0, [p0[0] + (R() - .5) * 10 * s, p0[1] - (8 + R() * 12) * s]], { w: 1.5 * s, tone: .8, dry: .5, prof: 'tip', seed: seed * 300 + i })); }
}

// 松：弯曲的老干 + 几簇扇形松针
function pine(L, x, y, s, seed = 5, t = 0, wind = 0, flip = 1) {
  const R = mulberry(seed);
  const trunk = [[0, 0], [-6, -40], [4, -90], [-10, -140], [10, -185], [40, -215], [80, -226]];
  const T = p => [x + p[0] * s * flip, y + p[1] * s];
  draw(L, mk(trunk.map(T), { w: 14 * s, tone: .75, darkDir: [flip, 0], side: .8, brWet: true, body: .3, dry: .6, wet: .8, prof: 'press', seed: seed * 11 }));
  // 树皮鳞纹
  for (let i = 0; i < 9; i++) { const u = .1 + R() * .8, k = Math.floor(u * (trunk.length - 1)), f = u * (trunk.length - 1) - k; const p = [lerp(trunk[k][0], trunk[k + 1][0], f), lerp(trunk[k][1], trunk[k + 1][1], f)]; draw(L, mk([T([p[0] - 5, p[1]]), T([p[0] + 3, p[1] + 3])], { w: 2.2 * s, tone: .85, dry: .5, prof: 'lens', seed: seed * 90 + i })); }
  // 枝
  const branches = [[[4, -90], [-40, -110], [-80, -112]], [[-10, -140], [-50, -160], [-70, -175]], [[10, -185], [50, -190], [90, -186]], [[40, -215], [70, -240], [110, -245]], [[80, -226], [120, -220], [150, -228]]];
  branches.forEach((b, i) => draw(L, mk(b.map(T), { w: 5 * s, tone: .8, dry: .55, wet: .3, prof: 'tip', seed: seed * 20 + i })));
  // 松针簇：每簇两层扇形短线，浓墨，略随风摆
  const clusters = [[-80, -114, 1], [-70, -178, .9], [-35, -165, .8], [90, -190, 1], [55, -196, .8], [110, -248, 1.1], [150, -232, .9], [75, -244, .8], [120, -222, .7], [-45, -112, .7]];
  clusters.forEach(([cx, cy, k], i) => {
    const sw = Math.sin(t * 1.3 + i) * wind * 2;
    for (let layer = 0; layer < 2; layer++) {
      const n = 11, spread = 1.35, rr = (layer ? 22 : 28) * k;
      for (let j = 0; j < n; j++) {
        const a = -Math.PI / 2 + (j / (n - 1) - .5) * spread * 2 + (layer ? .12 : 0);
        const c0 = T([cx + sw, cy + (layer ? 4 : 0)]);
        const c1 = [c0[0] + Math.cos(a) * rr * s, c0[1] + Math.sin(a) * rr * s * .55 + rr * s * .18];
        draw(L, mk([c0, c1], { w: 2.1 * s, tone: layer ? .9 : .7, dry: .35, wet: .35, prof: 'tip', seed: seed * 1000 + i * 40 + layer * 20 + j }));
      }
      // 簇底淡墨
      const c0 = T([cx + sw, cy + 6]);
      blot(L.wet, c0[0], c0[1], 16 * k * s, .18, 0, .35, i);
    }
  });
}

// 芦苇：细长弯茎 + 几片叶 + 穗
function reed(L, x, y, h, s, seed = 9, bend = 0, tone = .8) {
  const R = mulberry(seed);
  const top = [x + bend * h * .35, y - h];
  draw(L, mk([[x, y], [x + bend * h * .1, y - h * .5], top], { w: 2.4 * s, tone, dry: .35, wet: .3, prof: 'tip', seed: seed * 3 }));
  for (let i = 0; i < 3; i++) {
    const u = .25 + i * .2 + R() * .08, px = x + bend * h * .1 * u * 2, py = y - h * u;
    const dir = R() < .5 ? -1 : 1, L2 = h * (.3 + R() * .25);
    draw(L, mk([[px, py], [px + dir * L2 * .45, py - L2 * .35], [px + dir * L2 * .9 + bend * 10, py - L2 * .1]], { w: 5 * s, tone: tone * .9, dry: .4, wet: .4, prof: 'lens', seed: seed * 10 + i }));
  }
  // 穗
  draw(L, mk([top, [top[0] + bend * 14 * s + 6 * s, top[1] - 4 * s], [top[0] + bend * 26 * s + 14 * s, top[1] + 8 * s]], { w: 6 * s, tone: tone * .7, dry: .7, wet: .3, prof: 'lens', seed: seed * 17 }));
}

// 墨圈涟漪：一个透视椭圆，起笔重、收笔轻，缺一小口（像一笔画成）
function ripple(L, x, y, r, a, seed = 1, sq = .2, w = 3) {
  if (a <= .01 || r < 1) return;
  const n = 28, ph = (seed * 1.7) % 6.28, pts = [];
  for (let i = 0; i <= n; i++) { const t = ph + i / n * Math.PI * 1.86; pts.push([x + Math.cos(t) * r, y + Math.sin(t) * r * sq]); }
  draw(L, mk(pts, { w, tone: .75, dry: .55, wet: .45, prof: 'brush', seed: seed * 7 }), 1, a);
}

const __e = {};
if (typeof vn2 !== 'undefined') __e.vn2 = vn2;
if (typeof ridgeFn !== 'undefined') __e.ridgeFn = ridgeFn;
if (typeof mountainLayer !== 'undefined') __e.mountainLayer = mountainLayer;
if (typeof cun !== 'undefined') __e.cun = cun;
if (typeof cliff !== 'undefined') __e.cliff = cliff;
if (typeof pine !== 'undefined') __e.pine = pine;
if (typeof reed !== 'undefined') __e.reed = reed;
if (typeof ripple !== 'undefined') __e.ripple = ripple;
return __e;
})();
__M.hero = (() => {
// 无名侠客：写意造型，几笔成形。姿势 = 关节字典（局部坐标，身高 100，y 向下为正，脚底为原点，面朝右）。
// 每一帧按姿势重新生成笔触（种子固定 → 笔毫纹理稳定），面朝左时镜像。
const { mk, draw, mass, TONE } = __M.ink;
const { lerp, clamp, vnoise } = __M.lib;

const VERM = [176, 46, 34];

// ---------------- 姿势 ----------------
// 侧面（side）关节：H 胯 C 肩 Hd 头心 aF/aB 前后臂[肩,肘,手] lF/lB 前后腿[胯,膝,脚] hemF/hemB 前后摆 flare 摆尾飘出
// sword: {m:'sheath'|'hand', g 护手位置, a 鞘的方向} 或 {m:'hand', a 剑身方向}；rib 飘带方向与长度
const POSE = {
  stand: {
    v: 'side', H: [-.5, -46], C: [1.5, -75], Hd: [3.5, -83], tilt: .03,
    aF: [[2.5, -74], [7, -60], [11.5, -50]], aB: null,
    lF: [[1, -46], [3, -23], [4, 0]], lB: [[-1, -46], [-2, -23], [-4, 0]],
    hemF: [10, -6], hemB: [-14, -6.5], flare: .6,
    sheath: [9, -49, 2.5], sword: null, rib: [-1, .08, 22],
  },
  // 轻功腾空：前膝提起，后腿拖直，身体前倾，双袖向后，袍摆长长拖在后面
  leap: {
    v: 'side', H: [0, -52], C: [14, -70], Hd: [21, -76.5], tilt: -.28,
    aF: [[13, -69], [3, -64.5], [-8, -63]], aB: [[12, -69.5], [1, -71], [-11, -73.5]],
    lF: [[2, -52], [15, -47], [6, -38]], lB: [[-1, -52], [-11, -44], [-20, -38]],
    hemF: [11, -43], hemB: [-44, -58], flare: 1.5,
    sheath: [6, -56, 3.05], sword: null, rib: [-1, -.2, 46],
  },
  // 点水：单脚点水，另一腿收起
  touch: {
    v: 'side', H: [0, -46], C: [8, -72], Hd: [12.5, -80], tilt: -.14,
    aF: [[8, -71], [0, -64], [-9, -60]], aB: [[7, -71.5], [-2, -71], [-12, -72]],
    lF: [[1, -46], [5, -23], [3, 0]], lB: [[-1, -46], [11, -38], [4, -28]],
    hemF: [10, -9], hemB: [-32, -30], flare: 1.2,
    sheath: [3, -48, 2.7], sword: null, rib: [-1, -.05, 34],
  },
  // 滑停：重心后坐，前脚撑，袍摆向前甩
  skid: {
    v: 'side', H: [-3, -38], C: [-5, -65], Hd: [-3.5, -73.5], tilt: .08,
    aF: [[-4, -64], [5, -56], [13, -54]], aB: [[-6, -64], [-15, -58], [-23, -62]],
    lF: [[-2, -38], [10, -21], [20, 0]], lB: [[-4, -38], [-10, -18], [-14, 0]],
    hemF: [16, -6], hemB: [-12, -4], flare: -.4,
    sheath: [4, -41, 2.6], sword: null, rib: [1, .05, 18],
  },
  walk1: {
    v: 'side', H: [0, -46], C: [1.5, -75], Hd: [3.5, -83], tilt: 0,
    aF: [[2, -74], [7, -60], [11.5, -50]], aB: null,
    lF: [[1, -46], [5, -23], [8, 0]], lB: [[-1, -46], [-4, -23], [-8, 0]],
    hemF: [12, -6], hemB: [-13, -5.5], flare: .3,
    sheath: [9, -49, 2.5], sword: null, rib: [-1, .08, 22],
  },
  walk2: {
    v: 'side', H: [0, -47], C: [1.5, -76], Hd: [3.5, -84], tilt: 0,
    aF: [[2, -75], [7, -61], [11.5, -51]], aB: null,
    lF: [[1, -47], [1, -24], [0, -1]], lB: [[-1, -47], [-1, -24], [1, -2]],
    hemF: [10, -6], hemB: [-12, -5.5], flare: .3,
    sheath: [9, -50, 2.5], sword: null, rib: [-1, .08, 22],
  },
  // 拔剑（侧面），剑指前方
  draw: {
    v: 'side', H: [0, -46], C: [2, -75], Hd: [4, -83], tilt: -.04,
    aF: [[3, -74], [15, -72], [28, -74]], aB: [[0, -74], [-8, -66], [-15, -62]],
    lF: [[1, -46], [8, -23], [13, 0]], lB: [[-1, -46], [-7, -23], [-10, 0]],
    hemF: [14, -6], hemB: [-15, -5.5], flare: .5,
    sheath: [7, -49, 2.55], sword: { a: -.1 }, rib: [-1, .02, 28],
  },
  front: {
    v: 'front', H: [0, -46], C: [0, -75], Hd: [0, -83], tilt: 0,
    aL: [[-8.5, -74], [-11, -60], [-11.5, -48]], aR: [[8.5, -74], [11, -60], [11.5, -48]],
    lL: [[-3, -46], [-4, -23], [-4.5, 0]], lR: [[3, -46], [4, -23], [4.5, 0]],
    hemL: [-14, -5.5], hemR: [14, -5.5], sheath: [-8, -48, 2.2], rib: [0, 1, 0],
  },
  // 抱拳一礼：左掌包右拳，头微低
  bow: {
    v: 'front', H: [0, -46], C: [0, -74], Hd: [0, -81.5], tilt: 0,
    aL: [[-8.5, -73], [-13, -63], [-2, -65]], aR: [[8.5, -73], [13, -63], [2, -65]],
    lL: [[-3, -46], [-4, -23], [-4.5, 0]], lR: [[3, -46], [4, -23], [4.5, 0]],
    hemL: [-14, -5.5], hemR: [14, -5.5], sheath: [-8, -48, 2.2], fist: 1, rib: [0, 1, 0],
  },
  back: {
    v: 'back', H: [0, -46], C: [0, -75], Hd: [0, -83], tilt: 0,
    aL: [[-8.5, -74], [-11, -60], [-11.5, -48]], aR: [[8.5, -74], [11, -60], [11.5, -48]],
    lL: [[-3, -46], [-4, -23], [-4.5, 0]], lR: [[3, -46], [4, -23], [4.5, 0]],
    hemL: [-14, -5.5], hemR: [14, -5.5], sheath: [8, -48, .8], rib: [.3, 1, 14],
  },
  // 背面执剑写字：右臂高举，剑向右上
  backWrite: {
    v: 'back', H: [0, -46], C: [1, -75], Hd: [0, -83], tilt: -.04,
    aL: [[-8.5, -74], [-14, -63], [-16, -54]], aR: [[8.5, -74], [19, -81], [29, -90]],
    lL: [[-3, -46], [-8, -23], [-11, 0]], lR: [[3, -46], [7, -23], [10, 0]],
    hemL: [-16, -5.5], hemR: [16, -5.5], sheath: [-8, -48, 2.3], sword: { a: -.9 }, rib: [-1, .2, 22],
  },
};

// 递归插值两个姿势（数组/数字），非数值取 b
function mixPose(a, b, t) {
  if (typeof a === 'number' && typeof b === 'number') return lerp(a, b, t);
  if (Array.isArray(a) && Array.isArray(b)) return a.map((x, i) => mixPose(x, b[i], t));
  if (a && b && typeof a === 'object' && typeof b === 'object') { const o = {}; for (const k in b) o[k] = k in a ? mixPose(a[k], b[k], t) : b[k]; return o; }
  return t < .5 ? a : b;
}

// ---------------- 笔触生成 ----------------
const add2 = (a, b) => [a[0] + b[0], a[1] + b[1]], mid = (a, b, t = .5) => [lerp(a[0], b[0], t), lerp(a[1], b[1], t)];
const rot = (p, c, a) => { const s = Math.sin(a), co = Math.cos(a), x = p[0] - c[0], y = p[1] - c[1]; return [c[0] + x * co - y * s, c[1] + x * s + y * co]; };

// 从 knee→foot 找到摆下沿以下的部分
function legBelow(l, hemY) {
  const [hp, kn, ft] = l;
  if (kn[1] >= hemY) { const u = clamp((hemY - hp[1]) / ((kn[1] - hp[1]) || 1)); return [mid(hp, kn, u), kn, ft]; }
  const u = clamp((hemY - kn[1]) / ((ft[1] - kn[1]) || 1)); return [mid(kn, ft, u), ft];
}

function hatStrokes(S, Hd, tilt, half = 20, M, skew = 0) {
  const R = p => rot(p, Hd, tilt);
  const by = Hd[1] - 3, ap = [Hd[0] + skew, by - 11.5];
  const bl = [Hd[0] - half * .92, by + .4], br = [Hd[0] + half * 1.05, by + .8], bc = [Hd[0] + skew * .3, by + 1.6];
  // 斗笠：一块浓墨（湿）铺出锥面，两条干笔勾出笠坡，笠檐一线焦墨
  M([R(ap), R(add2(mid(ap, bl), [-.6, -.8])), R(bl), R(bc), R(br), R(add2(mid(ap, br), [.6, -.8]))], .5);
  S([R(add2(bl, [2, -1])), R(add2(bc, [0, -1.6])), R(add2(br, [-2, -1]))], LOAD(4, .55, [0, 1], { dry: .5, prof: 'lens' }));
  S([R(add2(ap, [-.3, .3])), R(add2(mid(ap, bl), [-.6, -.6])), R(bl)], { w: 2.4, tone: TONE.jiao, wet: .2, dry: .5, prof: 'nail' });
  S([R(add2(ap, [.3, .3])), R(add2(mid(ap, br), [.6, -.6])), R(br)], { w: 2.2, tone: TONE.jiao, wet: .2, dry: .55, prof: 'nail' });
  S([R(add2(ap, [.5, 2.5])), R(mid(bl, br, .62))], { w: 1, tone: TONE.nong, dry: .85, prof: 'tip' });   // 竹篾
  S([R([bl[0] - 1.2, bl[1] + .2]), R(bc), R([br[0] + 1.2, br[1] + .2])], { w: 1.9, tone: TONE.jiao, wet: .1, dry: .45, prof: 'tip' });
}

function swordStrokes(S, g, a, len, hilt = 7, inHand = false) {
  const d = [Math.cos(a), Math.sin(a)];
  const tip = [g[0] + d[0] * len, g[1] + d[1] * len], pom = [g[0] - d[0] * hilt, g[1] - d[1] * hilt];
  if (inHand) S([g, mid(g, tip, .5), tip], { w: 1.5, tone: TONE.jiao, dry: .15, wet: 0, prof: 'tip', rough: .05 });   // 剑身：一线焦墨
  else S([g, mid(g, tip, .5), tip], { w: 2.6, tone: TONE.zhong, dry: .3, wet: .2, prof: 'even', rough: .08 });        // 鞘
  S([g, pom], { w: 2.1, tone: TONE.jiao, dry: .25, prof: 'even' });
  const n = [-d[1], d[0]];
  S([[g[0] + n[0] * 2.8, g[1] + n[1] * 2.8], [g[0] - n[0] * 2.8, g[1] - n[1] * 2.8]], { w: 2, tone: TONE.jiao, dry: .2, prof: 'even' });
  return { tip, pom };
}

function tassel(S, pom, t, wind = [0, 0]) {
  const sw = Math.sin(t * 5.1) * .8, sw2 = Math.sin(t * 7.3 + 1) * 1;
  S([[pom[0], pom[1] + .3], [pom[0] + .6 + wind[0] * 1.5 + sw * .3, pom[1] + 3 + wind[1]], [pom[0] + wind[0] * 3.5 + sw, pom[1] + 6 + wind[1] * 2], [pom[0] + .8 + wind[0] * 6 + sw2, pom[1] + 8.5 + wind[1] * 3]],
    { w: 1.7, color: VERM, tone: .9, dry: .35, prof: 'brush', nb: 5 });
}

function ribbon(S, p0, rib, t, w = 1.5) {
  const [dx, dy, L] = rib; if (L <= 0) return;
  const pts = []; const n = 6;
  for (let i = 0; i <= n; i++) {
    const u = i / n, wav = Math.sin(t * 6.3 - u * 5.5) * 2.2 * u;
    pts.push([p0[0] + dx * L * u - dy * wav, p0[1] + dy * L * u + dx * wav * .9 + u * u * 2]);
  }
  S(pts, { w, tone: TONE.zhong, dry: .45, wet: .1, prof: 'tip' });
}

const curve = (a, c, b, n) => { const o = []; for (let i = 0; i < n; i++) { const t = n === 1 ? .5 : i / (n - 1), u = 1 - t; o.push([u * u * a[0] + 2 * u * t * c[0] + t * t * b[0], u * u * a[1] + 2 * u * t * c[1] + t * t * b[1]]); } return o; };
// 含墨一笔（笔尖浓、笔根淡）：没骨法，浓的一侧就是轮廓
const LOAD = (w, tone, dark, o = {}) => ({ w, tone, darkDir: dark, side: o.side ?? .85, brWet: true, body: o.body ?? .18, dry: o.dry ?? .38, wet: .9, prof: o.prof || 'robe', nb: o.nb, rough: .12 });

function faceSide(S, Hd, tilt) {
  const R = p => rot(p, Hd, tilt);
  // 脸：一笔清墨（湿），笠下阴影一笔淡墨
  S([R([Hd[0] + .5, Hd[1] - 1.5]), R([Hd[0] + 2.2, Hd[1] + 2.2]), R([Hd[0] + 1.2, Hd[1] + 4.8])], { w: 5.5, tone: .1, wet: 1, dry: 0, prof: 'lens' });
  S([R([Hd[0] - 2.5, Hd[1] - 2]), R([Hd[0] + 3.5, Hd[1] - 2.2])], { w: 2.4, tone: .3, wet: 1, dry: .1, prof: 'lens' });
  S([R([Hd[0] + 3.4, Hd[1] - 1.8]), R([Hd[0] + 4.6, Hd[1] + .8]), R([Hd[0] + 3.6, Hd[1] + 2]), R([Hd[0] + 4, Hd[1] + 3.6]), R([Hd[0] + 2.4, Hd[1] + 5.2])], { w: 1.2, tone: TONE.nong, dry: .35, prof: 'tip' });   // 侧脸一线
  S([R([Hd[0] + 3.2, Hd[1] + 4.3]), R([Hd[0] + 2.4, Hd[1] + 8.2])], { w: 1.1, tone: TONE.nong, dry: .55, prof: 'tip' });   // 须
  S([R([Hd[0] - 2.6, Hd[1] - 1.5]), R([Hd[0] - 3.2, Hd[1] + 2.5])], { w: 2.2, tone: TONE.nong, wet: .3, dry: .4, prof: 'tip' });   // 鬓
}

function sideStrokes(P, S, M, t) {
  const [hx, hy] = P.H, [cx, cy] = P.C, Hd = P.Hd;
  const nape = [Hd[0] - 3.5, Hd[1] + 5], bw = [hx - 7, hy - 1], fw = [hx + 7, hy - 2], chestF = [cx + 5, cy + 1.5];
  const tail = [P.hemB[0] - 6 * P.flare, P.hemB[1] - 3 * Math.abs(P.flare)];
  const hemC = [lerp(P.hemB[0], P.hemF[0], .5), Math.max(P.hemB[1], P.hemF[1]) + 1];
  const hem = curve(tail, hemC, P.hemF, 4);
  // 后臂（身后，最淡）
  if (P.aB) {
    const [s, e, h] = P.aB;
    S([s, e, h], LOAD(7.5, .4, [0, 1], { dry: .5 }));
  }
  // 腿（摆下，先画，被袍压住）
  const hemAt = x => {  // 下摆曲线在 x 处的高度
    let best = hem[0][1], bd = 1e9;
    for (let i = 0; i < 40; i++) { const u = i / 39, q = curve(tail, hemC, P.hemF, 40)[i]; const d = Math.abs(q[0] - x); if (d < bd) { bd = d; best = q[1]; } }
    return best;
  };
  for (const l of [P.lB, P.lF]) {
    const kx = lerp(l[1][0], l[2][0], .3);
    const seg = legBelow(l, hemAt(kx) + 1.5);
    S(seg, { w: 2, tone: TONE.nong, dry: .4, wet: .1, prof: 'even' });
    const ft = l[2];
    S([[ft[0] - 1, ft[1] - .3], [ft[0] + 4, ft[1] + .3]], { w: 2.8, tone: TONE.jiao, dry: .2, wet: .2, prof: 'nail' });
  }
  // 袍：一块清墨打底 + 背一笔含墨（浓边在背）+ 前一笔含墨（浓边在前）
  M([nape, chestF, add2(fw, [1, 0]), P.hemF, ...hem.slice(1, -1).reverse(), tail, add2(bw, [-1, 0])], .19 + .05 * clamp(P.flare - .8));
  S([[nape[0] + .5, nape[1] - 1], add2(mid(nape, bw), [-1.6, 0]), [bw[0] - .8, bw[1]], add2(mid(bw, tail, .55), [-1.4, 0]), tail], LOAD(10, .78, [-1, 0], { dry: .42 }));
  S([[chestF[0] - 1, chestF[1] - 1.5], add2(mid(chestF, fw), [1, 0]), fw, add2(mid(fw, P.hemF), [.6, 0]), P.hemF], LOAD(7, .55, [1, 0], { dry: .5 }));
  // 衣褶（干、细）
  S([add2(mid(nape, chestF, .5), [0, 7]), add2(mid(bw, fw, .45), [0, 2]), hem[1]], { w: 1.2, tone: TONE.zhong, dry: .75, prof: 'tip' });
  // 交领
  S([[Hd[0] - 1.5, Hd[1] + 6], [cx + 3.5, cy + 3.5], [fw[0] - 1, fw[1] - 6]], { w: 2.1, tone: TONE.nong, dry: .45, prof: 'tip' });
  // 下摆一线
  S(hem.map((p, i) => [p[0], p[1] + (i === 0 || i === hem.length - 1 ? 0 : .8)]), { w: 1.6, tone: TONE.zhong, dry: .7, prof: 'tip' });
  // 腰带：一笔焦墨 + 垂下的带尾
  S([[bw[0] - 1, bw[1] - 1.5], [hx, hy - 2.5], [fw[0] + 1.2, fw[1] - 2]], { w: 3.4, tone: TONE.jiao, dry: .3, wet: .2, prof: 'nail' });
  S([[bw[0] + 1, bw[1] - 1], [bw[0] - 2 + P.rib[0] * 3, bw[1] + 6], [bw[0] - 1 + P.rib[0] * 6, bw[1] + 12]], { w: 1.7, tone: TONE.nong, dry: .45, prof: 'tip' });
  // 鞘（腰间）
  let pom = null;
  if (P.sheath) {
    const [gx, gy, a] = P.sheath;
    if (P.sword) { const d = [Math.cos(a), Math.sin(a)]; S([[gx, gy], [gx + d[0] * 36, gy + d[1] * 36]], { w: 2.4, tone: TONE.zhong, dry: .35, wet: .2, prof: 'even' }); }
    else pom = swordStrokes(S, [gx, gy], a, 36).pom;
  }
  // 前臂：宽袖 = 一块清墨 + 一笔含墨（浓边在袖底）+ 袖口焦墨
  {
    const [sh, e, h] = P.aF, droop = add2(mid(e, h, .6), [-.5, 7.5]);
    M([add2(sh, [-2, -1]), add2(e, [0, -2]), add2(h, [0, -2.2]), add2(h, [.5, 4]), droop, add2(e, [-1, 3])], .12);
    S([[sh[0] - 1, sh[1] - .5], add2(e, [0, 1]), add2(h, [0, .5])], LOAD(7, .5, [0, 1], { dry: .45 }));
    S([add2(e, [-.5, 3]), droop, add2(h, [.4, 4.2])], LOAD(3.5, .7, [0, 1], { dry: .5, prof: 'tip' }));
    S([add2(h, [-.4, -1.5]), add2(h, [.3, 3.2])], { w: 1.8, tone: TONE.nong, dry: .45, prof: 'tip' });
  }
  // 剑在手
  if (P.sword) { const h = P.aF[2]; pom = swordStrokes(S, add2(h, [1.5, 0]), P.sword.a, 42, 6, true).pom; }
  // 脸、斗笠、飘带
  faceSide(S, Hd, P.tilt);
  hatStrokes(S, Hd, P.tilt, 20, M, -1);
  const R = p => rot(p, Hd, P.tilt);
  ribbon(S, R([Hd[0] - 4, Hd[1] - 1]), P.rib, t);
  if (pom) tassel(S, pom, t, [P.rib[0] * .5, 0]);
}

function frontStrokes(P, S, M, t, back = false) {
  const [hx, hy] = P.H, [cx, cy] = P.C, Hd = P.Hd;
  const sL = [cx - 8.5, cy + 1.5], sR = [cx + 8.5, cy + 1.5];
  const nL = [Hd[0] - 4.5, Hd[1] + 6], nR = [Hd[0] + 4.5, Hd[1] + 6];
  const wL = [hx - 7.5, hy - 1], wR = [hx + 7.5, hy - 1];
  const hemC = [hx, Math.max(P.hemL[1], P.hemR[1]) + 1.2];
  const hem = curve(P.hemL, hemC, P.hemR, 5);
  const sleeve = (a, side) => {
    const [sh, e, h] = a, droop = add2(mid(e, h, .55), [side * 2.5, 8]);
    M([add2(sh, [-side * 2, -1]), add2(e, [side * 1.5, -1]), add2(h, [0, -1.5]), add2(h, [0, 4]), droop, add2(e, [-side * 1, 3])], .12);
    S([sh, add2(e, [side * 1, 1]), h], LOAD(7, .5, [side, .3], { dry: .45 }));
    S([add2(e, [side * 1.5, 3]), droop, add2(h, [0, 4.2])], LOAD(3.5, .66, [side, 1], { dry: .5, prof: 'tip' }));
  };
  // 腿
  for (const l of [P.lL, P.lR]) {
    const seg = legBelow(l, hemC[1] - 3);
    S(seg, { w: 2.2, tone: TONE.nong, dry: .35, wet: .1, prof: 'even' });
    const ft = l[2]; S([[ft[0] - 1.8, ft[1]], [ft[0] + 1.8, ft[1] + .3]], { w: 3, tone: TONE.jiao, dry: .2, wet: .2, prof: 'even' });
  }
  // 袍：一块清墨 + 左右两笔含墨（浓边在外）
  M([nL, sL, add2(wL, [-1, 0]), ...hem, add2(wR, [1, 0]), sR, nR], .19);
  S([add2(nL, [-.5, -1]), add2(mid(sL, wL), [-1.2, 0]), add2(wL, [-.8, 0]), add2(mid(wL, P.hemL), [-.8, 0]), P.hemL], LOAD(8.5, back ? .72 : .66, [-1, 0], { dry: .42 }));
  S([add2(nR, [.5, -1]), add2(mid(sR, wR), [1.2, 0]), add2(wR, [.8, 0]), add2(mid(wR, P.hemR), [.8, 0]), P.hemR], LOAD(8, back ? .68 : .6, [1, 0], { dry: .46 }));
  S(hem, { w: 1.5, tone: TONE.zhong, dry: .7, prof: 'tip' });
  if (!back) {
    S([[Hd[0] - 4, Hd[1] + 5.5], [Hd[0] + 1, cy + 4], [hx + 4.5, hy - 4]], { w: 2.2, tone: TONE.nong, dry: .45, prof: 'tip' });   // 交领（右衽）
    S([[Hd[0] + 4, Hd[1] + 5.5], [Hd[0] + 1.5, cy + 2]], { w: 2, tone: TONE.nong, dry: .45, prof: 'tip' });
    S([add2(wL, [3, 3]), add2(hem[1], [.8, -1])], { w: 1.1, tone: TONE.zhong, dry: .75, prof: 'tip' });
    S([add2(wR, [-2.5, 3]), add2(hem[3], [-.8, -1])], { w: 1.1, tone: TONE.zhong, dry: .75, prof: 'tip' });
  } else {
    S([[Hd[0], Hd[1] + 7], [cx + .3, cy + 12], [hx, hy - 3], [hx - .5, hy + 20]], { w: 1.3, tone: TONE.zhong, dry: .7, prof: 'tip' });   // 背缝
  }
  S([[wL[0] - 1, wL[1] - 2.5], [hx, hy - 3.2], [wR[0] + 1, wR[1] - 2.5]], { w: 3.4, tone: TONE.jiao, dry: .3, wet: .2, prof: 'nail' });
  let pom = null;
  if (P.sheath) {
    const [gx, gy, a] = P.sheath;
    if (P.sword) { const d = [Math.cos(a), Math.sin(a)]; S([[gx, gy], [gx + d[0] * 30, gy + d[1] * 30]], { w: 2.4, tone: TONE.zhong, dry: .35, wet: .2, prof: 'even' }); }
    else pom = swordStrokes(S, [gx, gy], a, back ? 32 : 28, 6).pom;
  }
  sleeve(P.aL, -1); sleeve(P.aR, 1);
  if (P.fist) {
    const h = mid(P.aL[2], P.aR[2]);
    S([add2(h, [-2.4, -1.2]), add2(h, [2.4, -1])], { w: 4.4, tone: .2, wet: .8, dry: .1, prof: 'dot' });
    S([add2(h, [-2.8, -2.8]), add2(h, [-3.3, .8]), add2(h, [2.2, 1.4])], { w: 1.2, tone: TONE.nong, dry: .4, prof: 'tip' });
  } else if (!P.sword) {
    for (const a of [P.aL, P.aR]) { const h = a[2]; S([add2(h, [0, 3.8]), add2(h, [0, 6.2])], { w: 2.6, tone: .2, wet: .7, dry: .1, prof: 'dot' }); }
  }
  if (P.sword) { const h = P.aR[2]; pom = swordStrokes(S, h, P.sword.a, 42, 6, true).pom; }
  const R = p => rot(p, Hd, P.tilt);
  if (!back) {
    S([R([Hd[0], Hd[1] - 1.5]), R([Hd[0], Hd[1] + 3])], { w: 7, tone: .1, wet: 1, dry: 0, prof: 'lens' });            // 脸
    S([R([Hd[0] - 4, Hd[1] - 2.2]), R([Hd[0] + 4, Hd[1] - 2.2])], { w: 2.4, tone: .3, wet: 1, dry: .1, prof: 'lens' }); // 笠影
    S([R([Hd[0] - 3.4, Hd[1] + .5]), R([Hd[0] - 2.2, Hd[1] + 3.6]), R([Hd[0], Hd[1] + 4.6]), R([Hd[0] + 2.2, Hd[1] + 3.6]), R([Hd[0] + 3.4, Hd[1] + .5])], { w: 1.1, tone: TONE.nong, dry: .45, prof: 'tip' });
    S([R([Hd[0], Hd[1] + 3.8]), R([Hd[0] + .3, Hd[1] + 7.5])], { w: 1.2, tone: TONE.nong, dry: .55, prof: 'tip' });
    S([R([Hd[0] - 2.2, Hd[1] + 1.4]), R([Hd[0], Hd[1] + 1]), R([Hd[0] + 2.2, Hd[1] + 1.4])], { w: 1, tone: TONE.nong, dry: .5, prof: 'tip' });
    S([R([Hd[0] - 3.8, Hd[1] - 1.5]), R([Hd[0] - 4.2, Hd[1] + 2])], { w: 1.8, tone: TONE.nong, wet: .3, dry: .4, prof: 'tip' });
    if (P.eyes) {   // 抱拳时的笑眼：两弯
      S([R([Hd[0] - 3.2, Hd[1] - .2]), R([Hd[0] - 1.9, Hd[1] - .9]), R([Hd[0] - .8, Hd[1] - .2])], { w: .9, tone: TONE.jiao, dry: .3, prof: 'tip' });
      S([R([Hd[0] + .8, Hd[1] - .2]), R([Hd[0] + 1.9, Hd[1] - .9]), R([Hd[0] + 3.2, Hd[1] - .2])], { w: .9, tone: TONE.jiao, dry: .3, prof: 'tip' });
    }
    S([R([Hd[0] + 3.8, Hd[1] - 1.5]), R([Hd[0] + 4.2, Hd[1] + 2])], { w: 1.8, tone: TONE.nong, wet: .3, dry: .4, prof: 'tip' });
  } else {
    S([R([Hd[0], Hd[1] - 1]), R([Hd[0], Hd[1] + 4])], { w: 7.5, tone: .34, wet: .9, dry: .2, prof: 'lens' });          // 后脑发
    ribbon(S, R([Hd[0] - 1, Hd[1] + 2]), [P.rib[0] - .15, P.rib[1], P.rib[2]], t, 1.2);
    ribbon(S, R([Hd[0] + 1, Hd[1] + 2]), [P.rib[0] + .15, P.rib[1], P.rib[2] * .85], t + .7, 1.2);
  }
  hatStrokes(S, Hd, P.tilt, 20, M);
  if (pom) tassel(S, pom, t);
}

// 画侠客。X: {x, y, s, dir, seed, t, am, p(被画出来的进度 0..1), boil}
function hero(L, pose, X = {}) {
  const x0 = X.x ?? 0, y0 = X.y ?? 0, sc = X.s ?? 1, dir = X.dir ?? 1, t = X.t ?? 0, am = X.am ?? 1;
  const list = [];
  let idx = 0;
  const T = p => [x0 + p[0] * sc * dir, y0 + p[1] * sc, p[2] ?? 1];
  const S = (pts, o) => {
    const oo = { ...o, w: o.w * sc, seed: (X.seed ?? 7) * 1000 + (idx++) * 97, gapLen: 45 * sc, boil: X.boil ? (Math.floor(X.boil) % 5) : 0 };
    if (o.darkDir) oo.darkDir = [o.darkDir[0] * dir, o.darkDir[1]];
    list.push({ s: mk(pts.map(T), oo) });
  };
  const M = (poly, a) => { list.push({ m: poly.map(T), a, seed: idx++ }); };
  if (pose.v === 'side') sideStrokes(pose, S, M, t);
  else frontStrokes(pose, S, M, t, pose.v === 'back');
  const p = X.p ?? 1, N = list.length;
  for (let i = 0; i < N; i++) {
    const it = list[i];
    const pi = p >= 1 ? 1 : (p - i / N * .8) / .25;
    if (pi <= 0) continue;
    if (it.s) draw(L, it.s, pi, am);
    else mass(L.wet, it.m, it.a * am * clamp(pi), .6 * sc, it.seed);
  }
  return list;
}

const __e = {};
if (typeof VERM !== 'undefined') __e.VERM = VERM;
if (typeof POSE !== 'undefined') __e.POSE = POSE;
if (typeof mixPose !== 'undefined') __e.mixPose = mixPose;
if (typeof hero !== 'undefined') __e.hero = hero;
return __e;
})();
__M.face = (() => {
// 侠客面部特写（3/4 侧向右）：斗笠檐压在额上，线描为主、清墨托阴影。
// 局部坐标：脸心 (0,0)，额到下巴约 70 单位；expr: calm(闭目) / alert(睁眼) / resolve(决) / peace(笑)
const { mk, draw, mass, TONE } = __M.ink;
const { lerp, clamp } = __M.lib;

const EXPR = {
  //   brow: 内端/外端高度偏移（负=高），eye: 0 闭 1 睁，lid: 上眼睑压低，smile: 嘴角上扬，iris: 瞳孔
  calm: { bi: 0, bo: 0, eye: 0, lid: 0, smile: 0, mouth: 0 },
  alert: { bi: -2, bo: -1, eye: 1, lid: 0, smile: 0, mouth: 0 },
  resolve: { bi: 3, bo: -2.5, eye: 1, lid: .45, smile: -1.2, mouth: 1 },
  peace: { bi: -1, bo: .5, eye: .35, lid: .2, smile: 2.2, mouth: 0 },
};


function face(L, expr, X = {}) {
  const e = typeof expr === 'string' ? EXPR[expr] : expr;
  const x0 = X.x ?? 0, y0 = X.y ?? 0, sc = X.s ?? 1, am = X.am ?? 1;
  let idx = 0; const list = [];
  const T = p => [x0 + p[0] * sc, y0 + p[1] * sc, p[2] ?? 1];
  const S = (pts, o) => list.push({ s: mk(pts.map(T), { ...o, w: o.w * sc, seed: (X.seed ?? 11) * 1000 + (idx++) * 131 }) });
  const M = (poly, a) => list.push({ m: poly.map(T), a, seed: idx++ });
  const hatY = X.hatY ?? -30;          // 笠檐高度
  // 笠下阴影（淡墨，湿）
  S([[-40, hatY + 5], [0, hatY + 7], [38, hatY + 4]], { w: 14, tone: .34, darkDir: [0, -1], side: .9, brWet: true, body: .3, dry: .3, wet: 1, prof: 'lens', rough: .2 });
  // 脸的轮廓：远侧（右）一线浓淡，近侧（左）断续
  S([[23, hatY + 5, .6], [26.5, -9, 1.3], [24.5, 4, .8], [19, 17, 1.1], [8, 27.5, 1], [1, 29.5, .6]], { w: 2.4, tone: TONE.nong, dry: .45, prof: 'brush' });
  list.push({ m: [[26, hatY + 6], [14, hatY + 8], [12, -2], [20, 14], [24, 4]].map(T), a: .07, seed: 21 });   // 远侧脸颊清墨
  S([[-25, hatY + 8, .5], [-26.5, -8, 1.2], [-23.5, 8, 1], [-15, 21, .6]], { w: 2, tone: TONE.zhong, dry: .6, prof: 'tip' });
  // 耳
  S([[-24, -12], [-30, -9], [-30, -1], [-25, 2]], { w: 1.8, tone: TONE.zhong, dry: .5, prof: 'tip' });
  // 鬓发（干笔）
  S([[-21, hatY + 2], [-24, -18], [-26, -8]], { w: 3.6, tone: TONE.nong, dry: .7, wet: .2, prof: 'tip' });
  S([[-17, hatY + 3], [-19, -18]], { w: 2.4, tone: TONE.nong, dry: .75, prof: 'tip' });
  if (!X.hide) {
  // 剑眉：眉头重、眉尾上挑出锋
  const by = -16;
  S([[-3.5, by + e.bi], [-11, by - 2 + (e.bo + e.bi) / 2], [-20, by - 3.5 + e.bo]], { w: 3.6, tone: TONE.jiao, dry: .5, wet: .2, prof: 'nail' });
  S([[4, by + e.bi * .8], [11, by - 1.8 + (e.bo + e.bi) / 2 * .8], [18, by - 3 + e.bo * .8]], { w: 3.1, tone: TONE.jiao, dry: .55, wet: .2, prof: 'nail' });
  // 丹凤眼：上睑一笔由内眼角挑到外眼角，瞳孔被上睑压住一半
  const eye = (ci, co, far) => {    // ci 内眼角, co 外眼角
    const o = e.eye, lid = e.lid, mx = (ci[0] + co[0]) / 2, my = (ci[1] + co[1]) / 2;
    const sgn = Math.sign(co[0] - ci[0]);
    if (o < .2) {
      S([ci, [mx, my + 1.6], [co[0], co[1] - .2], [co[0] + sgn * 1.5, co[1] - 1]], { w: 1.9, tone: TONE.jiao, dry: .35, prof: 'tip' });
      return;
    }
    if (e.smile > 1) {
      S([[ci[0], ci[1] + .8], [mx, my - 1.6], [co[0], co[1] + .4]], { w: 2, tone: TONE.jiao, dry: .35, prof: 'tip' });
      S([[mx - sgn * 2, my + 2.2], [mx + sgn * 2, my + 2]], { w: .8, tone: TONE.dan, dry: .6, prof: 'tip' });
      return;
    }
    const up = lerp(-2.6, -1, lid);
    const ir = far ? 1.8 : 2.2;
    list.push({ dot: T([mx + sgn * (far ? -.3 : .4), my + .6 + lid * .5]), r: ir * sc, a: .9 });
    S([ci, [lerp(ci[0], co[0], .4), my + up], [co[0], co[1] + up * .2], [co[0] + sgn * 2, co[1] - 1.4]], { w: 2.4, tone: TONE.jiao, dry: .3, prof: 'nail' });
    S([[lerp(ci[0], co[0], .25), my + 2], [lerp(ci[0], co[0], .8), my + 1.6]], { w: .8, tone: TONE.zhong, dry: .6, prof: 'tip' });
  };
  eye([-4, -7.5], [-17, -8.5], false); eye([5, -7.5], [16, -8.3], true);
  }
  // 鼻：一笔由眉间下到鼻翼
  S([[3, -12], [5, -2], [7.5, 5], [4, 8.5], [0, 8]], { w: 1.8, tone: TONE.zhong, dry: .4, prof: 'brush' });
  // 髭（两笔下垂）
  S([[-.5, 12], [-6, 14.5], [-11, 19]], { w: 1.6, tone: TONE.nong, dry: .65, prof: 'tip' });
  S([[3, 12], [8, 14], [12, 18]], { w: 1.4, tone: TONE.nong, dry: .65, prof: 'tip' });
  // 嘴
  const sm = e.smile;
  S([[-5, 17.5 - sm * .8], [1, 17.5 + sm * .2 + e.mouth * .3], [7, 17 - sm * .7]], { w: 1.7 + e.mouth * .4, tone: TONE.nong, dry: .35, prof: 'tip' });
  // 颏须
  S([[2, 24], [2.5, 32], [1, 40]], { w: 2, tone: TONE.nong, dry: .7, prof: 'tip' });
  S([[6, 23], [7.5, 31], [7, 37]], { w: 1.4, tone: TONE.zhong, dry: .75, prof: 'tip' });
  // 颈与交领
  S([[-14, 26], [-15, 40]], { w: 1.6, tone: TONE.dan * 1.4, dry: .6, prof: 'tip' });
  S([[16, 22], [17, 36]], { w: 1.6, tone: TONE.zhong, dry: .55, prof: 'tip' });
  list.push({ m: [[-60, 64], [-44, 44], [-24, 40], [-6, 46], [8, 60], [12, 47], [26, 38], [46, 42], [58, 64]].map(T), a: .15, seed: 9, g: [0, T([0, 40])[1], 0, T([0, 64])[1], 1, 0] });
  S([[-26, 40], [-6, 46], [8, 59]], { w: 3.6, tone: TONE.nong, dry: .45, wet: .2, prof: 'brush' });
  S([[28, 38], [12, 46], [4, 56]], { w: 3.2, tone: TONE.nong, dry: .5, wet: .2, prof: 'brush' });
  S([[-56, 62], [-44, 45], [-26, 40]], { w: 3, tone: TONE.zhong, dry: .6, prof: 'tip' });
  S([[54, 62], [44, 44], [28, 38]], { w: 2.6, tone: TONE.zhong, dry: .65, prof: 'tip' });
  // 斗笠：一块浓墨（上浅下深）+ 两笔含墨压出锥面明暗 + 几丝干笔竹篾 + 笠檐焦墨一线
  const ap = [2, hatY - 44];
  list.push({ m: [[-86, hatY], [ap[0] - 3, ap[1]], [ap[0] + 3, ap[1]], [90, hatY - 1], [40, hatY + 2.5], [-40, hatY + 3]].map(T), a: .66, seed: 5, g: [0, T([0, ap[1]])[1], 0, T([0, hatY])[1], .75, 1.1] });
  [-58, -22, 16, 50].forEach(bx => S([[ap[0], ap[1] + 4], [bx, hatY - 2]], { w: 1.6, tone: TONE.jiao, dry: .8, prof: 'tip' }));
  S([[-88, hatY + .5, .7], [-30, hatY + 3, 1], [30, hatY + 3, 1.1], [92, hatY - .5, .7]], { w: 3.6, tone: TONE.jiao, dry: .4, wet: .2, prof: 'brush' });
  // 画
  for (const it of list) {
    if (it.s) draw(L, it.s, 1, am);
    else if (it.m) mass(L.wet, it.m, it.a * am, .5 * sc, it.seed, it.g || null);
    else if (it.dot) { const c = L.dry; c.globalAlpha = clamp(it.a * am); c.fillStyle = '#000'; c.beginPath(); c.arc(it.dot[0], it.dot[1], it.r, 0, Math.PI * 2); c.fill(); c.globalAlpha = 1; }
  }
  // 笠檐的水珠
  if (X.drop != null && X.drop >= 0) {
    const d = X.drop, px = T([30 + d * 2, hatY + 3 + d * d * 60]);
    const c = L.wet; c.globalAlpha = clamp((1 - d * .6) * .55 * am); c.fillStyle = '#000';
    c.beginPath(); c.ellipse(px[0], px[1], 1.6 * sc, 2.4 * sc, 0, 0, Math.PI * 2); c.fill(); c.globalAlpha = 1;
  }
}

const __e = {};
if (typeof EXPR !== 'undefined') __e.EXPR = EXPR;
if (typeof face !== 'undefined') __e.face = face;
return __e;
})();
__M.seal = (() => {
// 朱红白文方印"水"：印文用代码画的篆意线条（中间一道 S 形长画，两侧各两段折水纹）
const { vnoise, clamp } = __M.lib;
const { VERM } = __M.hero;
function seal(c, x, y, size, am = 1, seed = 3) {
  if (am <= 0) return;
  c.save(); c.translate(x, y);
  const S = size, jit = S * .018;
  // 印面：略不规则的方形
  c.beginPath();
  const N = 28;
  for (let i = 0; i < N; i++) {
    const t = i / N * 4, side = Math.floor(t), u = t - side;
    let px, py; if (side === 0) { px = u * S; py = 0; } else if (side === 1) { px = S; py = u * S; } else if (side === 2) { px = S - u * S; py = S; } else { px = 0; py = S - u * S; }
    px += (vnoise(seed + i * 1.3) - .5) * jit * 2; py += (vnoise(seed + 40 + i * 1.3) - .5) * jit * 2;
    i ? c.lineTo(px, py) : c.moveTo(px, py);
  }
  c.closePath(); c.fillStyle = `rgba(${VERM.join(',')},${clamp(am)})`; c.fill();
  // 印文（挖白）
  c.globalCompositeOperation = 'destination-out';
  c.fillStyle = '#000'; c.strokeStyle = '#000'; c.lineCap = 'round'; c.lineJoin = 'round';
  c.lineWidth = S * .085;
  const P = pts => { c.beginPath(); pts.forEach(([a, b], i) => { const X = a * S + (vnoise(seed + i * 2.1 + a * 9) - .5) * jit, Y = b * S + (vnoise(seed + 7 + i * 2.1 + b * 9) - .5) * jit; i ? c.lineTo(X, Y) : c.moveTo(X, Y); }); c.stroke(); };
  P([[.5, .12], [.5, .3], [.42, .4], [.5, .5], [.58, .6], [.5, .7], [.5, .88]]);          // 中画
  P([[.3, .16], [.3, .3], [.2, .38], [.2, .46]]);                                          // 左上
  P([[.17, .58], [.28, .64], [.28, .8], [.34, .86]]);                                      // 左下
  P([[.7, .16], [.7, .3], [.8, .38], [.8, .46]]);                                          // 右上
  P([[.83, .58], [.72, .64], [.72, .8], [.66, .86]]);                                      // 右下
  // 印泥不匀：细小的白点
  for (let i = 0; i < 70; i++) { const a = vnoise(seed + i * 3.7) , b = vnoise(seed + 91 + i * 2.9); c.globalAlpha = .5 + .5 * vnoise(i * 1.1); c.beginPath(); c.arc(a * S, b * S, S * (.004 + .012 * vnoise(i * 5.3)), 0, 7); c.fill(); }
  c.restore();
}

const __e = {};
if (typeof seal !== 'undefined') __e.seal = seal;
return __e;
})();
__M.wave = (() => {
// 巨浪：泼墨浪身 + 顺势的水纹线（学宋人水图的线描）+ 含墨卷起的浪头（飞白即浪花）+ 墨点水沫
// 局部坐标：原点在浪脚水面，y 向上为负。o: {x, y, s, rise(0..1), curl(0..1), t, seed, am}
const { mk, draw, mass, blot, TONE } = __M.ink;
const { mulberry, lerp, clamp, vnoise } = __M.lib;

function cr(pts, n = 8) {   // Catmull-Rom 加密，给水纹线用
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[Math.max(0, i - 1)], p1 = pts[i], p2 = pts[i + 1], p3 = pts[Math.min(pts.length - 1, i + 2)];
    for (let k = 0; k < n; k++) { const t = k / n, t2 = t * t, t3 = t2 * t; const f = j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3); out.push([f(0), f(1)]); }
  }
  out.push(pts[pts.length - 1]); return out;
}

function waveShape(o) {
  const r = o.rise ?? 1, c = o.curl ?? 1, t = o.t ?? 0;
  const sway = Math.sin(t * 1.7) * 6;
  const face = [[-460, 0], [-310, -55 * r], [-165, -210 * r], [-70, -440 * r], [-10 + sway * .3, -610 * r]];
  const crest = [-10 + sway * .5, -650 * r];
  const lip = [[40, -600 * r], crest, [lerp(-10, -90, c), lerp(-690, -725, c) * r], [lerp(0, -200, c), lerp(-700, -728, c) * r], [lerp(10, -272, c), lerp(-680, -684, c) * r], [lerp(20, -290, c) + sway, lerp(-650, -618, c) * r]];
  const back = [crest, [130, -590 * r], [310, -420 * r], [540, -260 * r], [820, -150 * r], [1150, -70 * r], [1500, -20 * r]];
  return { face, crest, lip, back, r, c };
}

function wave(L, o) {
  const x0 = o.x ?? 0, y0 = o.y ?? 0, s = o.s ?? 1, am = o.am ?? 1, R = mulberry(o.seed ?? 21), t = o.t ?? 0;
  const W = waveShape(o);
  const T = p => [x0 + p[0] * s, y0 + p[1] * s];
  const r = W.r; if (r <= .02) return W;
  // 浪身：淡墨湿块（浪面上半最浓，往下被水雾吃掉）
  const body = [...W.face, W.crest, ...W.back.slice(1), [1500, 30], [-460, 30]].map(T);
  mass(L.wet, body, .32 * am, 8 * s, 3, [0, y0 - 650 * r * s, 0, y0 + 20 * s, 1, .15]);
  // 浪：几笔巨大的含墨笔，从浪脚顺势扫上去、在浪顶卷过来（笔势就是浪势）
  const guide = [...W.face, ...W.lip.slice(1)];
  const strokes = [
    { off: [0, 0], w: 130, tone: .85, dry: .42, k: 1 },
    { off: [90, 30], w: 110, tone: .7, dry: .5, k: .93 },
    { off: [190, 70], w: 95, tone: .55, dry: .55, k: .85 },
    { off: [300, 110], w: 80, tone: .45, dry: .6, k: .74 },
    { off: [-40, -10], w: 36, tone: .95, dry: .35, k: 1.03 },
  ];
  strokes.forEach((st, i) => {
    const pts = guide.map((p, j) => {
      const u = j / (guide.length - 1);
      return [p[0] * st.k + st.off[0] * (1 - u * .9), p[1] * st.k * (1 - (1 - st.k) * .2) + st.off[1] * (1 - u)];
    });
    draw(L, mk(cr(pts, 4).map(T), { w: st.w * s, tone: st.tone, darkDir: [-1, -1], side: .9, brWet: true, body: .32, dry: st.dry, wet: .85, prof: 'rise', rough: .2, nb: 56, seed: 300 + i }), 1, am);
  });
  // 背坡：两笔淡墨
  for (let k = 0; k < 2; k++) {
    const pts = W.back.map(p => [p[0] + 20 + k * 60, p[1] + 30 + k * 70 * r]);
    draw(L, mk(cr(pts, 3).map(T), { w: (70 - k * 20) * s, tone: .4 - k * .12, darkDir: [0, -1], side: .8, brWet: true, body: .3, dry: .55, wet: .9, prof: 'lens', seed: 350 + k }), 1, am);
  }
  // 几道水纹线（宋人水图的线描），顺浪势
  for (let k = 0; k < 6; k++) {
    const f = k / 5, off = 60 + f * 380;
    const g = [[-420 + off * .5, -6], [-280 + off * .8, -70 * r * (1 - f * .5)], [-140 + off, -230 * r * (1 - f * .45)], [-50 + off * .9, -440 * r * (1 - f * .4)], [off * .75, -580 * r * (1 - f * .35)]];
    draw(L, mk(cr(g, 3).map(T), { w: 2.6 * s, tone: .8, dry: .6, wet: .2, prof: 'tip', seed: 400 + k }), 1, am * .8);
  }
  // 水沫：浪头上方的墨点
  const n = Math.round(46 * W.c);
  for (let i = 0; i < n; i++) {
    const a = R() * Math.PI, d = 30 + R() * 160;
    const px = W.crest[0] - 120 + Math.cos(a) * d * 1.4 + Math.sin(t * 2 + i) * 6, py = W.crest[1] - Math.sin(a) * d * .8 - 20 + Math.cos(t * 1.7 + i) * 5;
    const p = T([px, py]); blot(L.wet, p[0], p[1], (2 + R() * 7) * s, .75 * am, R() * 3, .7 + R() * .3, i);
  }
  return W;
}

const __e = {};
if (typeof waveShape !== 'undefined') __e.waveShape = waveShape;
if (typeof wave !== 'undefined') __e.wave = wave;
return __e;
})();
window.LIB = __M.lib; window.INK = __M.ink; window.INKC = __M.comp; window.INKL = __M.land; window.INKH = __M.hero; window.INKF = __M.face; window.INKS = __M.seal; window.INKW = __M.wave;
