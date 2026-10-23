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
  // yüzeyde çakıllar (dünya koordinatında): yürüyüşte ve kamerayla kayar, ayaklar zemine basıyor okunur
  ctx.fillStyle = mixCol('#2A1710', '#3A2414', warm);
  for (let x = Math.ceil(X0 / 29) * 29; x <= X1; x += 29) {
    const h = hash(x * .137); if (h < .45) continue;
    const xx = x + (hash(x * .71) - .5) * 20, r = 2 + hash(x * .29) * 5;
    ctx.beginPath(); ctx.ellipse(xx, Math.min(hillY(xx), 1060) - r * .45, r * 1.4, r * .7, hillAng(xx), 0, TAU); ctx.fill();
  }
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
  // itiş ritmi: titreşime ek olarak yavaş bir yüklenme-bırakma döngüsü (her itişte gövde öne yüklenir)
  const T = (o.T ?? 1.3) + a * .3 + Math.sin(t * 7) * .01 * strain + Math.max(0, Math.sin(t * 1.9)) * .03 * Math.min(1, strain) - off * .5;
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
  let hN = add(onR(hA), [-off * 30 * s, 0]), hF = add(onR(hB), [-off * 30 * s, 0]);
  let head = add(pel, scl(rot([.4, -36], T), s));
  if (o.dry) return { cx, cy, pel, head };
  // yere kapanma (prone) ve dört ayak üstünde doğrulma (rise): itme pozundan yamaç üstündeki pozlara karışım
  let P = pel, TT = T, nk = -.25, hd = -.55 + (o.look || 0), fNp = footPos(fN), fFp = footPos(fF);
  const pr = o.prone || 0;
  if (pr > 0) {
    const X = o.proneX ?? pel[0] - 8 * s, a2 = hillAng(X), n2 = hillN(X), ca = Math.cos(a2), r = o.rise || 0;
    const gp = (x, h) => { const nn = hillN(x); return [x + nn[0] * h, hillY(x) + nn[1] * h]; };
    const pelP = add([X, hillY(X)], scl(n2, 7.5 * s)), TP = PI / 2 + a2 - .05;
    const kx = X + ca * 5 * s, pelK = add([kx, hillY(kx)], scl(hillN(kx), 22 * s)), TK = 1.12 + a2 * .5;
    const pP = lerp2(pelP, pelK, r), Tq = lerp(TP, TK, r);
    const shq = add(pP, scl(rot([.6, -26.6], Tq), s));
    const hx = shq[0] + ca * lerp(5, 1, r) * s;
    const hNq = gp(hx + 2 * s, 1.2 * s), hFq = gp(hx - 2 * s, 1.2 * s);
    const fxP = X - ca * 40 * s, fxK = kx - ca * 20 * s, fx = lerp(fxP, fxK, r);
    const toe = -lerp(1.35, .95, r) - a2;
    const fNq = [...gp(fx + 2 * s, 2 * s), toe], fFq = [...gp(fx - 3 * s, 2 * s), toe];
    const e = pr;
    P = lerp2(pel, pP, e); TT = lerp(T, Tq, e);
    hN = lerp2(hN, hNq, e); hF = lerp2(hF, hFq, e);
    fNp = [...lerp2(fNp, fNq, e), lerp(fNp[2], fNq[2], e)]; fFp = [...lerp2(fFp, fFq, e), lerp(fFp[2], fFq[2], e)];
    // baş: yere kapanınca içe çekili, doğrulurken aşağı (kayanın gittiği yöne değil, yorgun) bakar
    nk = lerp(nk, lerp(.15, .25, r), e); hd = lerp(hd, lerp(.9 - TP - .15, .55 - TK - .25, r) + (o.look || 0), e);
    head = add(P, scl(rot([.4, -36], TT), s));
    // kaya üstünden geçerken kollarıyla başını korur; yere çarpınca gövde hafifçe seker (sönümlü)
    const cv = o.cover || 0;
    if (cv > 0) { hN = lerp2(hN, add(head, scl(rot([2, -4], TT), s)), cv); hF = lerp2(hF, add(head, scl(rot([-3, -6], TT), s)), cv); }
    if (o.bounce) P = add(P, scl(n2, o.bounce * 4 * s));
  }
  ctx.save(); if (!o.noCam) cam(ctx, c, 1);
  const rk = o.rock;
  const shadeRock = () => { if (o.noRock) return; if (rk) boulder(ctx, rk[0], rk[1], R, rk[2], { shadow: false, light: o.light ?? -1.2 }); else boulder(ctx, cx, cy, R, rockAng, { shadow: false, light: o.light ?? -1.2 }); };
  if (!o.rockFront) shadeRock();
  figure(ctx, {
    x: P[0], y: P[1], s, sty: o.sty || STY.black, cutCol: o.cutCol,
    lk: o.lk || { beard: 'pointed', hair: 'long', garment: 'short', torn: true }, alpha: o.alpha,
    p: { torso: TT, neck: nk, head: hd, handN: 'flat', handF: 'flat',
      brow: -strain, smile: o.smile || 0, breath: o.breath ?? Math.sin(t * 2.4) * (.5 + .4 * strain), blink: o.blink, mouthOpen: o.mouthOpen || 0 },
    ik: { hN, hF, fN: fNp, fF: fFp },
  });
  if (o.rockFront) shadeRock();
  ctx.restore();
  return { cx, cy, pel: P, head };
}
// Kaya elden kaçar: Sisifos yamaca yüzüstü kapanır, kaya sırtının üstünden sekerek aşar ve aşağı yuvarlanmayı sürdürür.
// xr0 = bırakma anındaki temas noktası, tg = kayanın geri kaçmaya başladığı an. Dönen nesne zamanla kaya/poz değerlerini verir.
function rockOver(xr0, R, s, tg, o = {}) {
  const st = pushScene(null, null, xr0, R, s, tg, { dist: o.dist ?? xr0, dry: true, T: o.T });
  const X = st.pel[0] - 8 * s, ca = Math.cos(hillAng(X));
  const headX = X + ca * 36 * s, feetX = X - ca * 44 * s;
  const xl = headX + R * .72, xd = feetX - R * .55;          // sıçrama ve iniş temas noktaları
  const tl = tg + (o.pre ?? .35), td = tl + (o.fly ?? .42);  // sıçrama ve iniş anları
  const Hm = o.hop ?? 85;
  const v1 = (xl - xd) / (td - tl), acc = o.acc ?? 900;
  // inişten sonra: küçülen sekmeler
  const B = []; { let tb = td, h = 26; for (let k = 0; k < (o.nb ?? 4); k++) { const gap = .34 - k * .04; B.push({ a: tb, b: tb + gap, h }); tb += gap; h *= .62; } }
  const xAt = t => {
    if (t < tg) return xr0;
    if (t < tl) { const q = (t - tg) / (tl - tg); return xr0 - (xr0 - xl) * q * q; }
    if (t < td) return xl - (t - tl) * v1;
    const u = t - td; return xd - v1 * u - .5 * acc * u * u;
  };
  const hopAt = t => {
    if (t >= tl && t < td) { const v = (t - tl) / (td - tl); return 4 * Hm * v * (1 - v); }
    for (const b of B) if (t >= b.a && t < b.b) { const v = (t - b.a) / (b.b - b.a); return 4 * b.h * v * (1 - v); }
    return 0;
  };
  const rockAt = t => { const x = xAt(t), n = hillN(x); return [x + n[0] * R, hillY(x) + n[1] * R - hopAt(t), x / R]; };
  const prone = t => ramp(t, tg - .3, tg + .08, E.in2);
  const rise = t => { const t0 = td + (o.riseAt ?? .35), d = o.riseDur ?? .7; return Math.max(0, anticip(t, t0, t0 + d, .12)); }; // önce bastırır, sonra kalkar
  const cover = t => ramp(t, tl - .2, tl + .05, E.out3) * (1 - ramp(t, td + .15, td + .5, E.io2));
  const bounce = t => settle(t, tg + .08, 1, 3.2, 7) + settle(t, td, .6, 4, 8);
  return { cover, bounce, X, headX, feetX, xl, xd, tg, tl, td, B, xAt, hopAt, rockAt, prone, rise, bounces: [td, ...B.slice(1).map(b => b.a)] };
}
// Tepe boyunca yürüyen Sisifos (aşağı ya da yukarı), x konumu, yön dir
function walkScene(ctx, c, x, s, t, dir, o = {}) {
  const gr = o.ground || HILLG, hillY = gr.y, hillAng = gr.a;
  const S2 = (o.stride || 34) * s;
  const d = o.dist ?? x * dir;
  const fN = gait(d, S2, 6 * s, 0), fF = gait(d, S2, 6 * s, .5);
  const footPos = f => { const fx = x + (f.x - d) * dir; return [fx, hillY(fx) - 3 * s - f.lift, -(hillAng(fx) * dir + f.heel)]; };
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
    x, y: py, s, dir, sty: o.sty || STY.black, cutCol: o.cutCol, alpha: o.alpha, onJoints: o.onJoints, hold: o.hold, extra: o.extra, margin: o.margin,
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
