// Tartaros dünyası: dik tepe, kaya, iten/yürüyen Sisifos. Dünya koordinatları (piksel, kamera ile çerçevelenir).
'use strict';
const HILL = { x0: -900, y0: 1060, sx: 1560, sy: 120 };
function hillY(x) {
  const { x0, y0, sx, sy } = HILL;
  if (x <= x0) return y0;
  if (x <= sx) { const u = (x - x0) / (sx - x0); const f = u * u * (3 - 2 * u); return lerp(y0, sy, Math.pow(f, .92)); }
  const v = (x - sx) / 520; return Math.min(y0, sy + v * v * 260);
}
function hillN(x) { // yüzey normali (yukarı/sol)
  const dx = 2, dy = hillY(x + dx) - hillY(x - dx);
  const l = Math.hypot(2 * dx, dy); return [dy / l, -2 * dx / l];
}
function hillAng(x) { const dy = hillY(x + 2) - hillY(x - 2); return Math.atan2(dy, 4); }
// Arka plan: gök (karanlık), ışık diski, uzak katmanlar
function tartarosBG(ctx, t, c, o = {}) {
  const warm = o.warm || 0; // 0 soğuk, 1 altın (Camus bölümü)
  // gök: tepede koyu, ufukta kor rengi (siluetler okunsun)
  ctx.save(); cam(ctx, c, .1);
  const g = ctx.createLinearGradient(0, -900, 0, 1100);
  g.addColorStop(0, mixCol('#120A09', '#2E1A10', warm)); g.addColorStop(.45, mixCol('#3B1A12', '#7A4118', warm));
  g.addColorStop(.75, mixCol('#8A3A1F', '#D08A3A', warm)); g.addColorStop(1, mixCol('#B4552C', '#EDB25A', warm));
  ctx.fillStyle = g; ctx.fillRect(-3000, -2000, 8000, 5000);
  ctx.restore();
  // ışık diski (üst dünyanın ışığı)
  ctx.save(); cam(ctx, c, .15);
  const dc = mixCol('#E9D9B4', '#FFD98A', warm);
  disk(ctx, o.diskX ?? 1520, o.diskY ?? 60, o.diskR ?? 300, dc, mixCol('rgba(233,217,180,.22)', 'rgba(255,200,110,.45)', warm));
  ctx.restore();
  stars(ctx, t * .2, 120, 5, 'rgba(240,220,190,.6)', [0, 0, W, H * .45]);
  // uzak sıradağlar
  ctx.save(); cam(ctx, c, .3);
  ctx.fillStyle = mixCol('#5A2617', '#9A5A26', warm);
  ctx.beginPath(); ctx.moveTo(-1500, 1300);
  for (let x = -1500; x <= 3400; x += 40) ctx.lineTo(x, 700 + fbm1(x * .0016, 2) * 160 - Math.sin(x * .0012) * 60);
  ctx.lineTo(3400, 1300); ctx.fill();
  ctx.restore();
  ctx.save(); cam(ctx, c, .55);
  ctx.fillStyle = mixCol('#33160E', '#6A3D17', warm);
  ctx.beginPath(); ctx.moveTo(-1500, 1400);
  for (let x = -1500; x <= 3600; x += 30) ctx.lineTo(x, 860 + fbm1(x * .0024, 7) * 140);
  ctx.lineTo(3600, 1400); ctx.fill();
  ctx.restore();
}
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
// Tepe (ön plan, kamera derinliği 1)
function tartarosHill(ctx, c, o = {}) {
  const warm = o.warm || 0;
  ctx.save(); cam(ctx, c, 1);
  ctx.fillStyle = mixCol('#0E0907', '#1C110A', warm);
  const X0 = o.wide ? -12000 : -2500, X1 = o.wide ? 12000 : 3500, stp = o.wide ? 40 : 12;
  ctx.beginPath(); ctx.moveTo(X0, 9000); ctx.lineTo(X0, hillY(X0));
  for (let x = X0; x <= X1; x += stp) ctx.lineTo(x, Math.min(hillY(x), 1060) + fbm1(x * .02, 4) * 3);
  ctx.lineTo(X1, 9000); ctx.closePath(); ctx.fill();
  // kenar ışığı
  ctx.strokeStyle = mixCol('rgba(214,130,80,.55)', 'rgba(255,190,100,.85)', warm); ctx.lineWidth = 3 / Math.max(.15, c.z ?? 1);
  ctx.beginPath(); for (let x = X0; x <= X1; x += stp) { const y = Math.min(hillY(x), 1060) + fbm1(x * .02, 4) * 3; x === X0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); } ctx.stroke();
  // kazınmış katmanlar (tabakalar) ve aşınmış yol
  ctx.strokeStyle = mixCol('rgba(160,80,45,.35)', 'rgba(200,130,60,.45)', warm); ctx.lineWidth = 2;
  for (let k = 1; k < 9; k++) {
    ctx.beginPath();
    for (let x = -2400; x <= 3400; x += 24) { const y = hillY(x) + k * 46 + fbm1(x * .006, k) * 18; x === -2400 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); }
    ctx.stroke();
  }
  if (o.groove) { // zamanla derinleşen yol izi
    ctx.strokeStyle = `rgba(0,0,0,${.5 * o.groove})`; ctx.lineWidth = 10 * o.groove;
    ctx.beginPath(); for (let x = -700; x <= HILL.sx; x += 16) { const y = hillY(x) + 6; x === -700 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); } ctx.stroke();
  }
  ctx.restore();
}
// Yürüyüş adım üreteci: d mesafe, S2 adım uzunluğu (aynı ayak), h kaldırma
function gait(d, S2, h, o) {
  const c = d / S2 + o, k = Math.floor(c), u = c - k;
  let x = (k - o) * S2 + .3 * S2, lift = 0, heel = 0;
  if (u >= .6) { const v = (u - .6) / .4; x += S2 * E.sine(v); lift = Math.sin(v * PI) * h; heel = -.25 * Math.sin(v * PI); }
  else if (u > .42) heel = .55 * (u - .42) / .18;
  return { x, lift, heel, u };
}
// Kaya iten Sisifos: xr kaya merkez x (tepe üstünde), R kaya yarıçapı, s figür ölçeği
// o: {strain, slip(0..1 ayak kayması), look, smile, lk, sty, handsOff(0..1 kayadan ayrılma)}
const HILLG = { y: hillY, n: hillN, a: hillAng };
function groundOf(f) { // y(x) fonksiyonundan zemin nesnesi
  return { y: f, a: x => Math.atan2(f(x + 2) - f(x - 2), 4), n: x => { const dy = f(x + 2) - f(x - 2), l = Math.hypot(4, dy); return [dy / l, -4 / l]; } };
}
function pushScene(ctx, c, xr, R, s, t, o = {}) {
  const gr = o.ground || HILLG, hillY = gr.y, hillN = gr.n, hillAng = gr.a;
  const n = hillN(xr), a = hillAng(xr);
  const cx = xr + n[0] * R, cy = hillY(xr) + n[1] * R;
  const rockAng = (o.rockAng ?? xr / R);
  // eller kaya yüzeyinde; omuz, ellerden kol boyu kadar geride; leğen omuzdan hesaplanır
  const strain = o.strain ?? 1;
  const off = o.handsOff || 0;
  const T = (o.T ?? 1.3) + a * .3 + Math.sin(t * 7) * .01 * strain - off * .5;
  const hA = PI - .62 + a * .35 + (o.hA || 0), hB = PI - .22 + a * .35 + (o.hB || 0);
  const onR = (th, k = 0) => [cx + Math.cos(th) * (R + 1.5 * s + k), cy + Math.sin(th) * (R + 1.5 * s + k)];
  const hm = onR((hA + hB) / 2);
  const reach = (o.reach ?? 14) * s + off * 26 * s;
  const sh = [hm[0] - Math.cos(a) * reach, hm[1] - Math.sin(a) * reach];
  const so = rot([.6, -26.6], T);
  const px = sh[0] - so[0] * s, py0 = sh[1] - so[1] * s;
  const d = o.dist ?? xr;
  const S2 = (o.stride ?? 50) * s;
  const fN = gait(d, S2, 7 * s, 0), fF = gait(d, S2, 7 * s, .5);
  const slip = o.slip || 0;
  const footPos = (f) => { const fx = px + (f.x - d) - (o.footBack ?? 11) * s - slip * 20 * s; return [fx, hillY(fx) - 3 * s - f.lift, -(hillAng(fx) + f.heel)]; };
  const bob = Math.sin((d / S2) * TAU * 2) * 1.0 * s;
  const jit = (o.jitter || 0) * s; // kas titremesi
  const pel = [px + noise1(t * 38, 7) * jit, py0 + bob + noise1(t * 38, 8) * jit];
  const hN = add(onR(hA), [-off * 30 * s, 0]), hF = add(onR(hB), [-off * 30 * s, 0]);
  const head = add(pel, scl(rot([.4, -36], T), s));
  if (o.dry) return { cx, cy, pel, head };
  ctx.save(); if (!o.noCam) cam(ctx, c, 1);
  const shadeRock = () => boulder(ctx, cx, cy, R, rockAng, { shadow: false, light: o.light ?? -1.2 });
  if (!o.rockFront) shadeRock();
  const dv = o.dive || 0;
  if (dv > 0) { ctx.save(); ctx.translate(pel[0], pel[1]); ctx.rotate(-dv * .7); ctx.scale(1 + dv * .1, 1 + dv * .1); ctx.translate(-pel[0] - dv * 34 * s, -pel[1] + dv * 52 * s); }
  figure(ctx, {
    x: pel[0], y: pel[1], s, sty: o.sty || STY.black, cutCol: o.cutCol,
    lk: o.lk || { beard: 'pointed', hair: 'long', garment: 'short', torn: true }, alpha: o.alpha,
    p: { torso: T, neck: -.25, head: -.55 + (o.look || 0), handN: 'flat', handF: 'flat',
      brow: -strain, smile: o.smile || 0, breath: Math.sin(t * 2.4) * .5, blink: o.blink || 0, mouthOpen: o.mouthOpen || 0 },
    ik: { hN, hF, fN: footPos(fN), fF: footPos(fF) },
  });
  if (dv > 0) ctx.restore();
  if (o.rockFront) shadeRock();
  ctx.restore();
  return { cx, cy, pel, head };
}
// Tepe boyunca yürüyen Sisifos (aşağı ya da yukarı), x konumu, yön dir
function walkScene(ctx, c, x, s, t, dir, o = {}) {
  const gr = o.ground || HILLG, hillY = gr.y, hillAng = gr.a;
  const S2 = (o.stride || 34) * s;
  const d = o.dist ?? x * dir;
  const fN = gait(d, S2, 6 * s, 0), fF = gait(d, S2, 6 * s, .5);
  const footPos = f => { const fx = x + (f.x - d) * dir; return [fx, hillY(fx) - 3 * s - f.lift, -(hillAng(fx) * dir + f.heel)]; };
  // kalça yüksekliği: duruş bacağı neredeyse düz kalacak kadar yüksek (çömelmiş yürüyüşü önler)
  const L = (o.legL || 43.4) * s, PF = [footPos(fN), footPos(fF)];
  let py = -1e9;
  for (const [fx, fy] of PF) { const dx = Math.min(Math.abs(fx - x), L * .97); py = Math.max(py, fy - Math.sqrt(L * L - dx * dx)); }
  ctx.save(); if (!o.noCam) cam(ctx, c, 1);
  const J = figure(ctx, {
    x, y: py, s, dir, sty: o.sty || STY.black, cutCol: o.cutCol, alpha: o.alpha, onJoints: o.onJoints, hold: o.hold, extra: o.extra, margin: o.margin,
    lk: o.lk || { beard: 'pointed', hair: 'long', garment: 'short', torn: true },
    p: {
      torso: (o.lean ?? .08) + (dir > 0 ? hillAng(x) * .3 : -hillAng(x) * .25), neck: o.neck || 0, head: o.head || 0,
      shN: Math.sin((d / S2) * TAU) * .35, elN: .35, shF: -Math.sin((d / S2) * TAU) * .35, elF: .35,
      handN: 'open', handF: 'open', smile: o.smile || 0, brow: o.brow || 0, breath: Math.sin(t * 2) * .6, blink: o.blink || 0,
      ...(o.p || {}),
    },
    ik: { fN: PF[0], fF: PF[1], ...(o.ik || {}) },
  });
  ctx.restore();
  return J;
}
