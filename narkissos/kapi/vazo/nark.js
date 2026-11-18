// Narkissos üslup kapısı: VAZO adayı (kırmızı figür, prometheus/lib motoru).
// Beş plan, ortak sahte anlatıma (../ortak/zaman.json) S()/Wd() ile bağlı. Belirlenimci: rastgelelik yalnız rng(tohum).
'use strict';
const Qs = new URLSearchParams(location.search);
const DIKEY = Qs.get('dikey') === '1';
const CW = DIKEY ? 1080 * RS : DW, CH = DIKEY ? 1920 * RS : DH; // çıktı tuvali (cihaz pikseli)
function jointPt(ctx, M, q) { const sp = M.transformPoint(new DOMPoint(q[0], q[1])); const r = ctx.getTransform().inverse().transformPoint(sp); return [r.x, r.y]; }

// ---- görünüm: yatayda 1920×1080 mantıksal, dikeyde aynı sahne D'nin baş+yansıma eksenine ortalanır ----
let DV = [850, 545, 1.32]; // dikey: [sahne x, sahne y, ölçek] → 1080×1920 merkezine
function baseView(ctx) {
  if (!DIKEY) { ctx.setTransform(RS, 0, 0, RS, 0, 0); return; }
  const [fx, fy, k] = DV;
  ctx.setTransform(RS * k, 0, 0, RS * k, RS * (540 - fx * k), RS * (960 - fy * k));
}
// sahne kamerası: (fx,fy) noktası ekranda (sx,sy)'ye, z yakınlaşmayla
function camAt(ctx, fx, fy, z, sx = W / 2, sy = H / 2) { ctx.translate(sx, sy); ctx.scale(z, z); ctx.translate(-fx, -fy); }

// ---- ara katmanlar (çıktı tuvali boyunda) ----
const LY = {};
function layer(n) {
  if (!LY[n]) LY[n] = makeCanvas(CW, CH);
  const x = LY[n].getContext('2d');
  x.setTransform(1, 0, 0, 1, 0, 0); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; x.filter = 'none';
  x.clearRect(0, 0, CW, CH);
  return x;
}

// ---- zemin: siyah sır + alttan (sudan) gelen sıcak ışık; başın arkasında ışık yok (hale okunmasın) ----
function glaze(ctx, gx, gy, gr, warm = 'rgba(120,48,22,.5)') {
  ctx.fillStyle = PC.glaze; ctx.fillRect(-3000, -3000, 9000, 9000);
  const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, gr);
  g.addColorStop(0, warm); g.addColorStop(.55, 'rgba(60,24,12,.22)'); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g; ctx.fillRect(-3000, -3000, 9000, 9000);
}

// ---- analitik halka: h(r,t) = A·e^(−k·yaş)·sin(ω·yaş − κ·r), cephe v·yaş'ta yumuşakça biter ----
// halka {x, y (su yüzeyi, mantıksal), t0, A, sq (perspektif basıklığı), v, lam, k}
function ringEnv(R, r, age) {
  const front = R.v * age;
  if (r > front + R.lam) return 0;
  const taper = clamp((front + R.lam - r) / (R.lam * 1.6));
  return R.A * Math.exp(-R.k * age) * taper * Math.exp(-r / (R.reach || 900));
}
function ringOm(R) { return 2 * PI / R.lam * R.v * .8; }
// yansımayı halkalarla piksel piksel kaydırır (yalnız halkanın etkin sınır kutusunda)
function warpRings(cv, rings, t, T, box) {
  const S = T.a; // mantıksal → cihaz ölçeği
  const act = rings.filter(R => t - R.t0 > 0 && t - R.t0 < (R.life || 4) && R.A * Math.exp(-R.k * (t - R.t0)) * T.a > 2.5); // sönmüş halka piksel kaydırmaz (süre)
  if (!act.length) return;
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const R of act) {
    const rr = (R.v * (t - R.t0) + R.lam) * S, cx = R.x * S + T.e, cy = R.y * S + T.f;
    x0 = Math.min(x0, cx - rr); x1 = Math.max(x1, cx + rr); y0 = Math.min(y0, cy - rr * R.sq); y1 = Math.max(y1, cy + rr * R.sq);
  }
  if (box) { x0 = Math.max(x0, box[0] * S + T.e); y0 = Math.max(y0, box[1] * S + T.f); x1 = Math.min(x1, box[2] * S + T.e); y1 = Math.min(y1, box[3] * S + T.f); } // yalnız yansımanın bulunduğu bölge (boş suyu kaydırmak boşa)
  x0 = Math.max(0, Math.floor(x0)); y0 = Math.max(0, Math.floor(y0)); x1 = Math.min(cv.width, Math.ceil(x1)); y1 = Math.min(cv.height, Math.ceil(y1));
  const bw = x1 - x0, bh = y1 - y0; if (bw <= 2 || bh <= 2) return;
  const cx2 = cv.getContext('2d');
  const src = cx2.getImageData(x0, y0, bw, bh), out = cx2.createImageData(bw, bh), sd = src.data, od = out.data;
  const P = act.map(R => ({ R, cx: R.x * S + T.e - x0, cy: R.y * S + T.f - y0, age: t - R.t0, kap: 2 * PI / (R.lam * S), om: ringOm(R) }));
  for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) {
    let dx = 0, dy = 0;
    for (const q of P) {
      const ex = x - q.cx, ey = (y - q.cy) / q.R.sq, r = Math.hypot(ex, ey);
      if (r < 1) continue;
      const env = ringEnv(q.R, r / S, q.age); if (env === 0) continue;
      const d = env * S * Math.cos(q.om * q.age - q.kap * r);
      dx += d * ex / r; dy += d * ey / r * q.R.sq * 2.2;
    }
    const sx = clamp(Math.round(x + dx), 0, bw - 1), sy = clamp(Math.round(y + dy), 0, bh - 1);
    const i = (y * bw + x) * 4, j = (sy * bw + sx) * 4;
    od[i] = sd[j]; od[i + 1] = sd[j + 1]; od[i + 2] = sd[j + 2]; od[i + 3] = sd[j + 3];
  }
  cx2.putImageData(out, x0, y0);
}
// halkanın görünen tepeleri: vazo dilinde ince kil çizgiler (ayrılmış çizgi)
function ringLines(ctx, rings, t, o = {}) {
  ctx.save(); ctx.lineCap = 'round';
  for (const R of rings) {
    const age = t - R.t0; if (age <= 0 || age > (R.life || 4)) continue;
    const kap = 2 * PI / R.lam, om = ringOm(R);
    for (let n = 0; n < 12; n++) {
      const r = (om * age - PI / 2 - 2 * PI * n) / kap; if (r <= 2) break;
      const e = ringEnv(R, r, age) / R.A * clamp((r - R.lam * .5) / (R.lam * 1.5)); if (e < .03) continue; // merkezdeki küçük elips söner (hale okunmasın)
      ctx.strokeStyle = o.col || `rgba(226,150,96,${clamp(.95 * e * (o.a ?? 1))})`;
      ctx.lineWidth = (o.w || 3.2) * (.5 + .5 * e);
      ctx.beginPath(); ctx.ellipse(R.x, R.y, r, r * R.sq, 0, .12, PI - .12); ctx.stroke(); // ön yarı (izleyiciye yakın)
      ctx.globalAlpha = .55; ctx.beginPath(); ctx.ellipse(R.x, R.y, r, r * R.sq, 0, PI + .12, TAU - .12); ctx.stroke(); ctx.globalAlpha = 1;
    }
  }
  ctx.restore();
}
// yansıma: sahneyi wy çizgisine göre aynalar, sakin su şerit kaydırması + halkalar, kırpma yolu içinde seyreltik sırla basar
function mirror(ctx, drawFn, wy, clipFn, t, o = {}) {
  const T = ctx.getTransform();
  const rx = layer('refl');
  rx.setTransform(T); rx.translate(o.dx || 0, 2 * wy); rx.scale(1, -1); drawFn(rx);
  const wx = layer('warp');
  const S = T.a, wyD = Math.floor(wy * S + T.f), step = 2, calm = (o.calm ?? 1.2) * S;
  if (wyD > 0) wx.drawImage(LY.refl, 0, 0, CW, wyD, 0, 0, CW, wyD);
  for (let y = Math.max(0, wyD); y < CH; y += step) {
    const d = (y - wyD) / S;
    let dx = calm * (Math.sin(d * .19 + t * 1.25) * .7 + Math.sin(d * .053 - t * .8) * .5) * clamp(d / 30);
    // kırılma (R.shear): halka geçerken yansıma yatay şeritlere bölünüp kayar; yüz 120 px'te de görünen kırık bir lekeye dağılır
    if (o.rings) for (const R of o.rings) if (R.shear) {
      const age = t - R.t0; if (age <= 0 || age > (R.life || 4)) continue;
      const yl = (y - T.f) / S, dr = Math.abs(yl - R.y) / R.sq, env = ringEnv(R, dr, age) / R.A;
      if (env > .01) { const band = Math.floor(dr / 17); dx += S * R.A * R.shear * env * Math.exp(-1.6 * age) * Math.sin(band * 2.17 + age * 7.5) * (.6 + .4 * Math.sin(band * 1.31)); }
    }
    wx.drawImage(LY.refl, 0, y, CW, step, dx, y, CW, step);
  }
  if (o.rings) warpRings(LY.warp, o.rings, t, T, o.warpBox);
  ctx.save(); ctx.beginPath(); clipFn(ctx); ctx.clip();
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = o.a ?? .5;
  ctx.drawImage(LY.warp, 0, 0);
  ctx.setTransform(T); ctx.globalAlpha = 1;
  if (o.rings) ringLines(ctx, o.rings, t, o.ringStyle);
  ctx.restore();
}
// su gövdesi: koyu sır + yatay ayrılmış kısa çizgiler (vazo ressamının suyu)
function waterBody(ctx, clipFn, wy, t, o = {}) {
  ctx.save(); ctx.beginPath(); clipFn(ctx); ctx.clip();
  ctx.fillStyle = o.fill || '#050302'; ctx.fillRect(-3000, wy, 9000, 4000);
  const r = rng(o.seed || 4), a = o.a ?? .2;
  ctx.strokeStyle = `rgba(201,112,63,${a})`; ctx.lineCap = 'round';
  const [x0, x1] = o.span || [-200, 2200], n = o.n || 34;
  for (let i = 0; i < n; i++) {
    const y = wy + 14 + Math.pow(r(), 1.5) * (o.depth || 420), x = x0 + r() * (x1 - x0), L = 40 + r() * 170, dr = Math.sin(t * .6 + i) * 6;
    ctx.lineWidth = 1.6 + r() * 1.4; ctx.beginPath(); ctx.moveTo(x + dr, y); ctx.lineTo(x + L + dr, y); ctx.stroke();
  }
  ctx.restore();
}
// figürü ayrı katmanda çizip alttan ışıkla boyar (kaynak: su ya da ekran); ışık yalnız figürün üstünde
function litFigure(ctx, f, light) {
  const T = ctx.getTransform(), lx = layer('fig');
  lx.setTransform(T); const J = figure(lx, f);
  if (light && light.a > 0) {
    lx.globalCompositeOperation = 'source-atop';
    const g = lx.createRadialGradient(light.x, light.y, 0, light.x, light.y, light.r);
    g.addColorStop(0, light.c.replace('A', light.a.toFixed(3))); g.addColorStop(1, light.c.replace('A', '0'));
    lx.fillStyle = g; lx.fillRect(-3000, -3000, 9000, 9000);
    if (light.dark) { // üst kısım gölgede (ışık yukarıdan değil)
      const g2 = lx.createLinearGradient(0, light.y - light.r, 0, light.y);
      g2.addColorStop(0, `rgba(20,8,4,${light.dark})`); g2.addColorStop(1, 'rgba(20,8,4,0)');
      lx.fillStyle = g2; lx.fillRect(-3000, -3000, 9000, 9000);
    }
    lx.globalCompositeOperation = 'source-over';
  }
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(LY.fig, 0, 0); ctx.restore();
  return J;
}
// figür eklemleri (çizmeden)
function joints(ctx, f) { let J = null, M = null; figure(ctx, { ...f, alpha: 0, jointsOnly: true, onJoints: (j, m) => { J = j; M = m; } }); return { J, M }; }
function headPt(ctx, J, M, q) { return jointPt(ctx, M, add(J.neckT, rot(q, J.headA))); }
function placeNeck(ctx, f, target) {
  const { J, M } = joints(ctx, f); const q = jointPt(ctx, M, J.neckT), dx = target[0] - q[0], dy = target[1] - q[1];
  const ik = f.ik ? Object.fromEntries(Object.entries(f.ik).map(([k, v]) => [k, [v[0] + dx, v[1] + dy, ...v.slice(2)]])) : f.ik;
  return { ...f, x: f.x + dx, y: f.y + dy, ik };
}

// ---- biçim dönüşümü: telefonun yuvarlak köşeli camı ↔ havuz elipsi (aynı başlangıç noktası ve yön, eşit yay aralığı) ----
function resample(pts, n) {
  const L = [0]; for (let i = 1; i <= pts.length; i++) L.push(L[i - 1] + len(sub(pts[i % pts.length], pts[i - 1])));
  const tot = L[pts.length], out = []; let j = 0;
  for (let k = 0; k < n; k++) { const s = tot * k / n; while (L[j + 1] < s) j++; const u = (s - L[j]) / (L[j + 1] - L[j] || 1); out.push(lerp2(pts[j], pts[(j + 1) % pts.length], u)); }
  return out;
}
function roundRectPts(x0, y0, x1, y1, rTop, rBot, bulge = 0) { // üst kenarın ortasından saat yönünde
  const P = [], arc = (cx, cy, r, a0, a1) => { for (let i = 0; i <= 10; i++) { const a = lerp(a0, a1, i / 10); P.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } };
  P.push([(x0 + x1) / 2, y0]);
  arc(x1 - rTop, y0 + rTop, rTop, -PI / 2, 0);
  arc(x1 - rBot + bulge, y1 - rBot, rBot, 0, PI / 2);
  arc(x0 + rBot - bulge, y1 - rBot, rBot, PI / 2, PI);
  arc(x0 + rTop, y0 + rTop, rTop, PI, PI * 1.5);
  return P;
}
function ellipsePts(cx, cy, rx, ry) { const P = []; for (let i = 0; i < 64; i++) { const a = -PI / 2 + i / 64 * TAU; P.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]); } return P; }
function morphPts(A, B, m) { const n = 120, a = resample(A, n), b = resample(B, n); return a.map((p, i) => lerp2(p, b[i], m)); }

// ================= PLAN A ve E: bugünün genci, siyah telefon camı ↔ havuz =================
const LK_MOD = { modern: true, rf: true, hairPts: HAIR_MOD, garment: 'coat', coatCol: '#6E331B', sleeveCol: '#6E331B', earHidden: false, headS: 1.24, eyeS: 1.12 }; // tur 1: daha genç (büyük baş, iri göz)
// tur 1: efeb başı (kısa bukleli saç, kulak açık, köşeli çene) ve görünür khiton (seyreltik sır, koyu sır yaka/etek/kol kenarı; nokta deseni ve kemer yok)
const KHITON = { col: '#93492A', edge: 1.3, sleeve: false };
const LK_NK = { hair: 'short', rf: true, garment: 'short', noCurls: true, efeb: true, hairPts: HAIR_EF, jaw: true, khiton: KHITON, noBelt: true };
function phoneScene(ctx, t, o) {
  const m = o.m; // 0 telefon camı, 1 havuz
  baseView(ctx);
  glaze(ctx, 1100, 820, 1100, `rgba(${lerp(80, 120, m) | 0},${lerp(42, 48, m) | 0},${lerp(28, 22, m) | 0},.45)`);
  const p = { torso: .3, neck: .42, head: .55 + (o.headNod || 0), shN: .38, elN: .5, shF: .32, elF: .55, handN: 'fist', handF: 'fist', smile: 0, brow: .15, mouthOpen: 0, blink: o.blink };
  let f = { x: 0, y: 0, s: 24, dir: 1, sty: STY.red, lk: LK_MOD, seed: 31, idle: .6, p, faceW: 1.35, stripe: .35 };
  f = placeNeck(ctx, f, o.neck || [640, 370]);
  const { J: J0, M: M0 } = joints(ctx, f), e = headPt(ctx, J0, M0, [3.7, -6.75]);
  // küçük telefon camı (yüzün iki katı kadar), eğik tutulduğu için yansıma camın ortasına kayar (dxR)
  const wy = 600, pcx = e[0] + 330, pw = 270;
  const dxR = o.dxFixed ? pcx - e[0] - 20 : lerp(pcx - e[0] - 20, 0, m);
  if (o.auto) o.cam = [pcx - 120, wy + 40, o.cam[2]];
  camAt(ctx, ...o.cam);
  const phone = roundRectPts(pcx - pw, wy, pcx + pw, wy + 900, 56, 56);
  const pool = ellipsePts(pcx - 100, wy + 360, 1300, 360);
  const shape = morphPts(phone, pool, m);
  const clip = c => poly(c, shape);

  // figür: omuz başı solda kadraj kenarında, başı ekrana eğik; ekran ışığı alttan

  waterBody(ctx, clip, wy, t, { a: .2 * m, seed: 6, span: [300, 2100], n: 40 });
  // eğik cam: yansıma camın ortasına kayar (dx)
  const rings = typeof o.rings === 'function' ? o.rings(pcx, wy, e) : o.rings;
  mirror(ctx, c => figure(c, f), wy, clip, t, { a: o.refA ?? .42, rings, calm: lerp(.15, 1.2, m), dx: dxR });
  const ph = 1 - m;
  if (ph > .01) { // cam parıltısı ve telefon ayrıntıları: havuza dönerken söner
    ctx.save(); ctx.beginPath(); clip(ctx); ctx.clip();
    const g = ctx.createLinearGradient(pcx - 200, wy, pcx + 250, wy + 600); g.addColorStop(0, 'rgba(255,240,215,0)'); g.addColorStop(.45, `rgba(255,240,215,${.07 * ph})`); g.addColorStop(.55, `rgba(255,240,215,${.07 * ph})`); g.addColorStop(1, 'rgba(255,240,215,0)');
    ctx.fillStyle = g; ctx.fillRect(600, wy, 1100, 900);
    ctx.restore();
    ctx.save(); ctx.globalAlpha = ph; ctx.fillStyle = '#21160f';
    ctx.beginPath(); ctx.roundRect(pcx - 50, wy + 20, 100, 13, 6.5); ctx.fill();
    ctx.beginPath(); ctx.arc(pcx + 78, wy + 26, 7, 0, TAU); ctx.fill();
    ctx.restore();
  }
  ctx.save(); ctx.beginPath(); poly(ctx, shape); ctx.lineWidth = lerp(4.5, 6, m); ctx.strokeStyle = mixCol('#B9653A', '#C9703F', m); ctx.lineJoin = 'round'; ctx.stroke(); ctx.restore();
  if (o.light > 0) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, pcx - 120, wy, 420, `rgba(255,220,170,${.14 * o.light})`); ctx.restore(); }
  litFigure(ctx, f, { x: e[0] + 120, y: wy + 20, r: 430, c: 'rgba(255,226,186,A)', a: .34 * o.light, dark: .25 + .25 * o.light });
  if (ph > .02) phoneHand(ctx, pcx - pw, wy, t, ph, o.thumb || 0, o.light);
  return f;
}
const SCENES_N = {};
SCENES_N.A = (ctx, t) => {
  const tc = Wd('S1', 'camın').t0;
  const m = ramp(t, Wd('S1', 'içinden').t0 - .05, 3.45, E.io2);
  const z = kf(t, [[0, 1.0], [2.8, 1.07, E.io2], [3.5, 1.24, E.in2]]);
  const fy = lerp(540, 700, ramp(t, 2.8, 3.5, E.in2));
  // başparmak üç kez kaydırır; her kaydırmada ekran ışığı kısa bir an değişir (yeni içerik)
  const flicks = [.35, 1.05, 1.75], th = flicks.reduce((v, f0) => Math.max(v, ramp(t, f0, f0 + .18, E.out2) * (1 - ramp(t, f0 + .22, f0 + .5, E.io2))), 0);
  const fl = flicks.reduce((v, f0, i) => v + (t > f0 + .15 ? [.12, -.1, .08][i] : 0), 0) * (1 - ramp(t, 2.4, 2.9, E.io2));
  phoneScene(ctx, t, {
    m, thumb: th, cam: [960, fy, z], light: lerp(.75 + fl, .35, m), refA: .42,
    headNod: .04 * Math.sin(t * 1.1) - .05 * ramp(t, Wd('S1', 'kendine').t0, Wd('S1', 'bakıyorsun').t1, E.io2) + .06 * ramp(t, tc - .2, tc + .3, E.io2),
    rings: (cx, wy) => [{ x: cx + 20, y: wy + 190, t0: tc, A: 9, sq: .32, v: 330, lam: 44, k: .9, reach: 1200, life: 4 }],
  });
};
SCENES_N.E = (ctx, t) => {
  const t0 = 16.0;
  const m = 1 - ramp(t, Wd('S5', 'bakmayı').t0, Wd('S5', 'yine').t1, E.io2);
  const z = kf(t, [[t0, 1.34], [19.5, 1.46, E.lin]]);
  phoneScene(ctx, t, {
    m, dxFixed: true, auto: true, cam: [0, 0, z], light: lerp(.25, 1, ramp(t, Wd('S5', 'yine').t0, Wd('S5', 'bırakamadı').t0, E.io2)), refA: lerp(.5, .4, 1 - m),
    headNod: .03 * Math.sin(t * .9),
    rings: (cx, wy) => [{ x: cx - 10, y: wy + 170, t0: S('S5').t0 - .1, A: 7, sq: .32, v: 220, lam: 40, k: .7, reach: 1000, life: 4.5 },
      { x: cx + 40, y: wy + 200, t0: Wd('S5', 'bırakamadı').t0, A: 6, sq: .32, v: 220, lam: 40, k: .8, reach: 900, life: 3 }],
  });
};

// telefonu tutan el: avuç camın sol kenarının arkasında, başparmak camın önünde (kaydırır); kol yeni giysinin seyreltik sırrı
function phoneHand(ctx0, X0, wy, t, a, th, light) {
  const T = ctx0.getTransform(), ctx = layer('hand'); ctx.setTransform(T);
  ctx.save(); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  const y0 = wy + 190;
  // kol (ceket kolu) alttan sola
  ctx.beginPath(); ctx.moveTo(X0 - 330, y0 + 520); ctx.quadraticCurveTo(X0 - 230, y0 + 230, X0 - 105, y0 + 140); ctx.lineTo(X0 - 10, y0 + 230); ctx.quadraticCurveTo(X0 - 110, y0 + 330, X0 - 150, y0 + 560); ctx.closePath();
  ctx.fillStyle = '#6E331B'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke();
  // avuç ve parmaklar camın kenarını sarar
  ctx.beginPath(); ctx.moveTo(X0 - 112, y0 + 150); ctx.quadraticCurveTo(X0 - 60, y0 + 40, X0 + 4, y0 + 10); ctx.lineTo(X0 + 20, y0 + 60); ctx.lineTo(X0 + 22, y0 + 120); ctx.lineTo(X0 + 18, y0 + 180); ctx.quadraticCurveTo(X0 - 20, y0 + 230, X0 - 12, y0 + 232); ctx.closePath();
  ctx.fillStyle = '#C9703F'; ctx.fill(); ctx.stroke();
  for (const yy of [70, 125, 178]) { ctx.beginPath(); ctx.moveTo(X0 - 6, y0 + yy); ctx.lineTo(X0 + 20, y0 + yy - 4); ctx.lineWidth = 2.6; ctx.stroke(); }
  // başparmak: camın önünde, ucu kaydırma hareketiyle oynar (th: 0..1)
  const tip = [X0 + 118 + 10 * th, y0 - 20 - 46 * th];
  ctx.beginPath(); ctx.moveTo(X0 - 70, y0 + 60); ctx.quadraticCurveTo(X0 + 10, y0 + 4 - 20 * th, tip[0] - 18, tip[1] - 4); ctx.quadraticCurveTo(tip[0] + 14, tip[1] + 6, tip[0] - 4, tip[1] + 30); ctx.quadraticCurveTo(X0 + 30, y0 + 70 - 10 * th, X0 - 50, y0 + 120); ctx.closePath();
  ctx.fillStyle = '#C9703F'; ctx.fill(); ctx.lineWidth = 4; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(tip[0] - 26, tip[1] + 2); ctx.quadraticCurveTo(tip[0] - 14, tip[1] + 14, tip[0] - 12, tip[1] + 24); ctx.lineWidth = 2.2; ctx.stroke(); // tırnak
  // ekran ışığı elin üstünde
  ctx.globalCompositeOperation = 'source-atop';
  const g = ctx.createRadialGradient(X0 + 120, y0 - 60, 0, X0 + 120, y0 - 60, 360); g.addColorStop(0, `rgba(255,226,186,${.3 * light})`); g.addColorStop(1, 'rgba(255,226,186,0)');
  ctx.fillStyle = g; ctx.fillRect(X0 - 600, y0 - 400, 1200, 1200);
  ctx.restore();
  ctx0.save(); ctx0.setTransform(1, 0, 0, 1, 0, 0); ctx0.globalAlpha = a; ctx0.drawImage(LY.hand, 0, 0); ctx0.restore();
}
// ================= PLAN B: orman kenarında pınar (geniş) =================
// vazo ağacı: ince gövde, kıvrık dallar, dal boyunca çift sıra zeytin yaprağı (kil dolgu, siyah kontur)
function vaseTree(ctx, x, y, s, seed, t, o = {}) {
  const r = rng(seed), sway = Math.sin(t * .7 + seed) * .012;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(sway);
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const trunk = [[0, 0], [-4, -60], [6, -130], [-2, -200], [4, -260]];
  ctx.beginPath(); spline(ctx, trunk, false); ctx.strokeStyle = C.ink; ctx.lineWidth = 15; ctx.stroke();
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = 9; ctx.stroke();
  const leaf = (px, py, a, L) => { ctx.save(); ctx.translate(px, py); ctx.rotate(a); ctx.beginPath(); ctx.ellipse(L / 2, 0, L / 2, L * .17, 0, 0, TAU); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.lineWidth = 1.8; ctx.strokeStyle = C.ink; ctx.stroke(); ctx.beginPath(); ctx.moveTo(L * .1, 0); ctx.lineTo(L * .85, 0); ctx.lineWidth = 1.2; ctx.stroke(); ctx.restore(); };
  const nb = o.branches || 6;
  for (let b = 0; b < nb; b++) {
    const u = .25 + .75 * (b / (nb - 1)), side = b % 2 ? 1 : -1, by = -260 * u, bx = Math.sin(u * 5) * 4;
    const L = (o.reach || 90) * (1.15 - u * .5) * (.8 + r() * .4), ph = Math.sin(t * 1.1 + b + seed) * 2.5;
    const P = [[bx, by], [bx + side * L * .5, by - 22 - r() * 14], [bx + side * L, by - 30 - r() * 30 + ph]];
    ctx.beginPath(); spline(ctx, P, false); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.stroke(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 3; ctx.stroke();
    for (let k = 1; k <= 7; k++) {
      const v = k / 7.5, q = lerp2(lerp2(P[0], P[1], v), lerp2(P[1], P[2], v), v), da = Math.atan2(P[2][1] - P[0][1], P[2][0] - P[0][0]);
      leaf(q[0], q[1], da - side * (.9 - v * .4) - (side < 0 ? PI : 0) * 0, 26 - v * 6);
      leaf(q[0], q[1], da + side * (.9 - v * .4) + (side < 0 ? 0 : 0), 24 - v * 6);
    }
  }
  ctx.restore();
}
function groundBand(ctx, y, x0 = -400, x1 = 2400) {
  ctx.save(); ctx.fillStyle = PC.clayR; ctx.fillRect(x0, y, x1 - x0, 7);
  ctx.fillStyle = '#5A2C16'; ctx.fillRect(x0, y + 7, x1 - x0, 300);
  ctx.restore();
}
function grass(ctx, x, y, s, t, seed) {
  ctx.save(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 2.6; ctx.lineCap = 'round';
  const r = rng(seed);
  for (let i = 0; i < 5; i++) { const a = -PI / 2 + (i - 2) * .28 + Math.sin(t * 1.3 + i + seed) * .04, L = s * (14 + r() * 10); ctx.beginPath(); ctx.moveTo(x + (i - 2) * 3, y); ctx.quadraticCurveTo(x + (i - 2) * 3 + Math.cos(a) * L * .4, y + Math.sin(a) * L * .6, x + (i - 2) * 6 + Math.cos(a) * L, y + Math.sin(a) * L); ctx.stroke(); }
  ctx.restore();
}
function spear(ctx, a, ang, L, s) {
  const b = add(a, [Math.cos(ang) * L, Math.sin(ang) * L]), c0 = add(a, [-Math.cos(ang) * L * .45, -Math.sin(ang) * L * .45]);
  ctx.save(); ctx.lineCap = 'round';
  ctx.strokeStyle = C.ink; ctx.lineWidth = 1.9 * s; ctx.beginPath(); ctx.moveTo(...c0); ctx.lineTo(...b); ctx.stroke();
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = .8 * s; ctx.stroke();
  ctx.translate(...b); ctx.rotate(ang); ctx.beginPath(); ctx.moveTo(0, -1.6 * s); ctx.lineTo(7 * s, 0); ctx.lineTo(0, 1.6 * s); ctx.closePath(); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.lineWidth = .5 * s; ctx.strokeStyle = C.ink; ctx.stroke();
  ctx.restore();
}
SCENES_N.B = (ctx, t) => {
  baseView(ctx);
  glaze(ctx, 1250, 900, 1200, 'rgba(120,48,22,.42)');
  const z = kf(t, [[3.5, 1.2], [4.7, 1.03, E.out3], [7.0, 1.0, E.lin]]);
  camAt(ctx, lerp(1180, 980, ramp(t, 3.5, 4.7, E.out3)), lerp(700, 560, ramp(t, 3.5, 4.7, E.out3)), z);
  const gy = 760, pc = [1290, 812], prx = 380, pry = 58;
  const trees = c => {
    vaseTree(c, 150, gy, 1.75, 3, t, { branches: 7, reach: 110 });
    vaseTree(c, 1720, gy, 1.9, 8, t, { branches: 7, reach: 120 });
    vaseTree(c, 1900, gy, 1.45, 5, t, { branches: 6 });
    vaseTree(c, 1010, gy, 1.05, 11, t, { branches: 5, reach: 70 });
  };
  // yürüyen genç (avcı): S2 'genç' sözcüğünde kadraja yerleşmiş, 'pınara'da yavaşlar, 'eğildi'de durup başını eğer
  const tA = 3.5, tStop = Wd('S2', 'pınara').t1, stand = ramp(t, tStop - .3, tStop + .25, E.io2);
  const s = 4.4, xw = lerp(260, 850, E.out2(clamp((t - tA) / (tStop - tA)))) + 0 * stand;
  const lean = ramp(t, Wd('S2', 'eğildi').t0, Wd('S2', 'eğildi').t1 + .3, E.io2);
  const ground = groundOf(() => gy);
  let J = null, M = null;
  const walker = (c, al = 1) => walkScene(c, null, xw, s, t, 1, { ground, noCam: true, sty: STY.red, lk: LK_NK, dist: (xw - 260) * 1.0, stand, stripe: .5, lean: .06 + lean * .12, neck: lean * .25, head: lean * .35, alpha: al, onJoints: (j, m) => { J = j; M = m; }, p: { shF: -.55 + .15 * stand, elF: -.2 } });
  // pınar (havuz): yansıma kıyı çizgisine göre
  const pool = c => c.ellipse(pc[0], pc[1], prx, pry, 0, 0, TAU);
  groundBand(ctx, gy);
  for (let i = 0; i < 9; i++) grass(ctx, 80 + i * 230 + (i % 2) * 70, gy + 2, 1.5, t, i + 3);
  ctx.save(); ctx.beginPath(); pool(ctx); ctx.fillStyle = '#050302'; ctx.fill(); ctx.restore();
  waterBody(ctx, pool, pc[1] - pry, t, { a: .22, seed: 9, span: [pc[0] - prx, pc[0] + prx - 120], n: 12, depth: pry * 1.6 });
  const nerg = c => { for (const [x, sd, h] of [[1560, 5, 58], [1610, 8, 46], [1655, 2, 54], [975, 11, 50]]) narcissus(c, x, gy, 1.35, t, sd, { dir: x > 1300 ? -1 : 1, h }); }; // pınar kıyısında nergisler
  mirror(ctx, c => { trees(c); nerg(c); walker(c); }, gy, pool, t, { a: .4, calm: .8 });
  ctx.save(); ctx.beginPath(); pool(ctx); ctx.lineWidth = 4; ctx.strokeStyle = PC.clayR; ctx.stroke(); ctx.restore();
  // kıyı kayası (C'deki oturma yeri)
  crag(ctx, [[pc[0] - prx - 70, gy + 4], [pc[0] - prx + 10, gy - 34], [pc[0] - prx + 80, gy - 30], [pc[0] - prx + 120, gy + 8]], { fill: '#5A2C16', seed: 4, wob: 4, strata: 2, lobes: 1 });
  trees(ctx);
  nerg(ctx);
  walker(ctx);
  spear(ctx, jointPt(ctx, M, J.AF.wr), -1.2, 62 * s, s * .9);
  ctx.save(); baseView(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze); ctx.restore();
};

// ================= PLAN C ve D: kıyıda uzanmış genç (dirsekleri kayada), başı suyun üstünde =================
// Uzanma: gövde yatay (göğüs aşağı), bacaklar geriye uzanır, dirsekler kaya kenarında; diz çökme ve alın yere değme yok.
// pose(t, k): k = ek baş eğimi; ön kol 'âşık'ta suya uzanır (C)
function proneFig(px, gy, s, p, o = {}) {
  return { x: px, y: gy - 6.5 * s, s, dir: 1, sty: STY.red, lk: LK_NK, seed: 23, idle: o.idle ?? .4, p, stripe: o.stripe ?? .5, faceW: o.faceW || 1.2,
    ik: { fN: [px - 41 * s, gy - 2.5 * s, PI / 2 - .25], fF: [px - 43 * s, gy - 4.5 * s, PI / 2 - .35],
      hF: o.hF || [px + 31 * s, gy - 1.5 * s], hN: o.hN || [px + 33 * s, gy - 1.2 * s] } };
}
function pPose(o = {}) {
  return { torso: 1.33, neck: -.5 + (o.neck || 0), head: .38 + (o.head || 0), handN: o.handN || 'flat', handF: 'flat', wrN: o.wrN || 0, wrF: 0,
    smile: o.smile || 0, brow: o.brow ?? .2, mouthOpen: o.mouthOpen || 0, blink: o.blink };
}
// kaya kenarı (dirseklerin dayandığı çıkıntı) suyun içine iner
function ledge(ctx, xe, gy, wy) {
  crag(ctx, [[-2600, gy + 4], [xe - 260, gy - 6], [xe - 40, gy - 2], [xe + 4, gy + 14], [xe - 6, wy + 30], [xe - 40, wy + 700], [-2600, wy + 700]], { fill: '#5A2C16', seed: 9, flat: [0, 5, 6], wob: 4, strata: 4, lobes: 3 });
}
SCENES_N.C = (ctx, t) => {
  baseView(ctx);
  glaze(ctx, 1150, 900, 1150, 'rgba(130,52,24,.5)');
  const z = kf(t, [[7.0, 1.5], [10.5, 1.64, E.lin]]);
  camAt(ctx, lerp(860, 920, ramp(t, 7, 10.5, E.lin)), 610, z);
  const wy = 640, gy = 618, xe = 980, s = 6.0, px = xe - 30 * s;
  const ly = Wd('S3', 'yüze'), la = Wd('S3', 'âşık');
  const look = ramp(t, ly.t0 - .2, ly.t1 + .3, E.io2), reach = ramp(t, la.t0 - .1, Wd('S3', 'oldu').t1, E.io2);
  // tur 1: eller kıyıyı kavrar (parmaklar kenardan aşağı), 'âşık'ta yalnız yakın el suya uzanır (avuç yukarı, yakarış okuması yok)
  const grip = [xe - 12, gy - .6];
  const hN = [lerp(grip[0] + 4, xe + 40, reach), lerp(grip[1], wy - 34, reach)], aN = lerp(.12, .42, reach);
  let f = proneFig(px, gy, s, pPose({ head: .08 * look, neck: .04 * look, handN: reach > .3 ? 'open' : 'flat', smile: .25 * reach }), { hN, hF: [grip[0] - 9, grip[1]] });
  const { J } = joints(ctx, f);
  f.p = { ...f.p, wrN: aN - J.AN.foA, wrF: .12 - J.AF.foA };
  const water = c => c.rect(xe - 10, wy, 4000, 2000);
  waterBody(ctx, water, wy, t, { a: .2, seed: 5, span: [xe, 2300], n: 28, depth: 380 });
  const spr = c => spear(c, [px - 150, gy - 40], -.18, 330, 4.4);
  const bank = c => { for (const [x, sd, h] of [[1290, 5, 60], [1318, 8, 48], [1350, 2, 56]]) narcissus(c, x, wy - 14, .62, t, sd, { dir: -1, h }); };
  mirror(ctx, bank, wy, c => c.rect(1150, wy, 4000, 2000), t, { a: .45, calm: 1.1 });
  mirror(ctx, c => figure(c, f), wy, water, t, { a: .42, calm: 1.1 });
  farBank(ctx, 1180, 2600, wy, t, 17, { h: 22, grass: 7, fill: '#3A1B0D' }); bank(ctx);
  ledge(ctx, xe, gy, wy);
  for (let i = 0; i < 5; i++) grass(ctx, 120 + i * 160, gy + 2, 1.6, t, i + 11);
  spr(ctx);
  litFigure(ctx, f, { x: xe + 80, y: wy + 40, r: 520, c: 'rgba(255,205,150,A)', a: .3 });
  shoreLine(ctx, xe - 10, wy, { w: 2.6 });
  ctx.save(); baseView(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze); ctx.restore();
};

const D_WY = 630, D_GAP = 40; // su çizgisi kaya üstünden 40 birim aşağıda: el kıyıdan suya iner, buluşma noktası açık suda
// ---- nergis (Narcissus poeticus): beyaz, düzensiz oval taç yapraklar (yandan, basık: altı köşeli yıldız okunmasın), safran göbek, kırmızı kenarlı kadeh ----
// (x, y): sapın dibi; s ölçek; yön suya doğru eğik (nod); belirlenimci (seed)
function narcissus(ctx, x, y, s, t, seed, o = {}) {
  const r = rng(seed), dir = o.dir ?? 1, H = (o.h || 70) * (.85 + r() * .3), sway = Math.sin(t * .9 + seed * 1.7) * .035;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s); ctx.rotate(sway);
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  // iki şerit yaprak
  for (const [a, L] of [[-.32, H * .62], [.22, H * .5]]) {
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(Math.sin(a) * L * .5 - 2, -L * .6, Math.sin(a) * L * 1.1, -L);
    ctx.strokeStyle = C.ink; ctx.lineWidth = 4.2; ctx.stroke(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 2.2; ctx.stroke();
  }
  // sap: yukarı çıkar, tepede suya doğru eğilir
  const top = [7, -H], head = [16, -H + 8];
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(-2, -H * .6, top[0], top[1]); ctx.quadraticCurveTo(13, -H - 2, head[0], head[1]);
  ctx.strokeStyle = C.ink; ctx.lineWidth = 3.4; ctx.stroke(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 1.5; ctx.stroke();
  // çiçek başı: yüzü suya dönük (yandan basık)
  ctx.translate(head[0] + 3, head[1] + 2); ctx.rotate(.55 + (o.tilt || 0));
  ctx.scale(.52, 1);
  const n = 6, a0 = r() * TAU;
  for (let i = 0; i < n; i++) {
    const a = a0 + i * TAU / n + (r() - .5) * .45, L = 11 * (.8 + r() * .35), w = L * (.42 + r() * .12);
    ctx.save(); ctx.rotate(a); ctx.beginPath(); ctx.ellipse(0, -L * .55, w * .5, L * .55, (r() - .5) * .3, 0, TAU);
    ctx.fillStyle = C.white; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.6; ctx.stroke(); ctx.restore();
  }
  ctx.beginPath(); ctx.ellipse(0, 0, 4.2, 4.2, 0, 0, TAU); ctx.fillStyle = '#E2A33A'; ctx.fill(); ctx.strokeStyle = '#8E2F1F'; ctx.lineWidth = 1.6; ctx.stroke();
  ctx.beginPath(); ctx.arc(0, 0, 1.6, 0, TAU); ctx.fillStyle = '#6E4A12'; ctx.fill();
  ctx.restore();
}
// karşı kıyı: suyun ufkunda alçak, seyreltik sır şerit + ot; ufuk çizgisi belirgin (yan görünüşte suyu okutur)
function farBank(ctx, x0, x1, wy, t, seed, o = {}) {
  const r = rng(seed), h = o.h || 46;
  ctx.save();
  ctx.beginPath(); ctx.moveTo(x0, wy);
  for (let x = x0; x <= x1 + 40; x += 40) ctx.lineTo(x, wy - h * (.55 + .45 * noise1(x * .004, seed)));
  ctx.lineTo(x1 + 40, wy); ctx.closePath(); ctx.fillStyle = o.fill || '#2A130A'; ctx.fill();
  ctx.strokeStyle = 'rgba(201,112,63,.35)'; ctx.lineWidth = 2; ctx.stroke();
  for (let i = 0; i < (o.grass ?? 10); i++) grass(ctx, x0 + 30 + r() * (x1 - x0 - 60), wy - h * .55 + 4, 1.2, t, seed + i);
  ctx.restore();
}
// kıyı ve ufuk çizgisi: suyun yüzeyi açık kil, kalın (yan görünüşte suyu okutan çizgi)
function shoreLine(ctx, x0, wy, o = {}) {
  ctx.save(); ctx.strokeStyle = o.col || 'rgba(232,160,104,.92)'; ctx.lineWidth = o.w || 3.6; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x0, wy); ctx.lineTo(o.x1 || 6000, wy); ctx.stroke(); ctx.restore();
}
// ---- tanıma hamlesi: el suya uzanır, yansımanın eli 0,3 sn geç gelir; 'benim'de aynı karede buluşur ----
// el bileği yolu (sahne koordinatı) ve elin yönü (ileri-açı: dirF(a) = [sin a, cos a]); 'open' el, parmak ucu bilekten ~7 birim
const D_TOUCH = { tip: [800, 630] };
const D_REST = { w: [300, 590], a: 1.62, hand: 'flat' };
function dReach(t) {
  const son = Wd('S4', 'sonra').t0, ben = Wd('S4', 'benim').t0, tTouch = ben - .3, tBack = ben + .45;
  const rest = D_REST, lift = { w: [470, 455], a: .55, hand: 'point' }, touch = { w: [600, 520], a: 1.068, hand: 'point' };
  const mix = (A, B, u) => ({ w: lerp2(A.w, B.w, u), a: lerp(A.a, B.a, u), hand: u < .5 ? A.hand : B.hand });
  if (t < son) return { ...rest, k: 0 };
  if (t < son + .46) return { ...mix(rest, lift, anticip(t, son, son + .46, .12)), k: 1 };
  if (t < tTouch) return { ...mix(lift, touch, E.io2(clamp((t - son - .46) / (tTouch - son - .46)))), k: 2 };
  if (t < tBack) return { ...touch, k: 3 };
  if (t < tBack + .35) return { ...mix(touch, lift, E.out3(clamp((t - tBack) / .35))), k: 4 };
  return { ...mix(lift, rest, E.io2(clamp((t - tBack - .35) / .9))), k: 5 };
}
function dPoseO(t) {
  const tear = Wd('S4', 'düştü').t0, son = Wd('S4', 'sonra').t0, ben = Wd('S4', 'benim').t0;
  const lean0 = ramp(t, 10.5, 11.3, E.io2) * .04;
  const flinch = settle(t, tear + .05, .05, 1.2, 2.2);
  const leanIn = ramp(t, son, ben - .05, E.io2) * .05 * (1 - ramp(t, ben, ben + .35, E.out3));
  const recoil = ramp(t, ben, ben + .3, E.out3) * .13;   // irkilme: baş geri çekilir
  const sad = ramp(t, ben + .6, 16, E.io2);
  return { neck: lean0 + leanIn * .5 - recoil * .6, head: lean0 + flinch + leanIn - recoil * .5,
    smile: -.2 - .3 * sad, brow: .3 + .8 * ramp(t, ben, ben + .2, E.out3) - .35 * sad, mouthOpen: .55 * ramp(t, ben, ben + .25, E.out3) * (1 - .6 * sad), blink: t > ben - .02 && t < ben + .12 ? 0 : undefined };
}
const D_S = 26, D_XE = 640;
function dFig(ctx, t, NT, s = D_S, o = {}) { // NT: [kaya kenarı x, su çizgisi y]
  const gy = NT[1] - D_GAP + .2 * s, px = NT[0] - 30 * s;
  const q = dPoseO(t), pp = pPose(q);
  pp.neck = 1.0 + q.neck; pp.head = -.9 + q.head; // boyun kenardan aşağı sarkar, yüz suya bakar (öpüşme ekseni)
  const R = o.handOff ? { w: [140, 600], a: 1.62, hand: 'flat' } : o.rest ? D_REST : dReach(t); // handOff: el kadraj dışında (kapak)
  pp.handN = R.hand; pp.handF = 'flat';
  const hN = [R.w[0] + (NT[0] - D_XE), R.w[1] + (NT[1] - D_WY)];
  const f = proneFig(px, gy, s, pp, { idle: .3, faceW: 1.5, stripe: .3, hN, hF: o.handOff ? [px + 12 * s, gy - .2 * s] : [px + 17 * s, gy - .4 * s] });
  const { J } = joints(ctx, f);
  f.p = { ...f.p, wrN: R.a - J.AN.foA, wrF: 1.62 - J.AF.foA }; // el yönü (bileği kır): dinlenirken avuç kayada, uzanırken parmaklar suya
  return f;
}
function dScene(ctx, t, o = {}) {
  const wy0 = o.wy || D_WY, NT = [o.xe ?? D_XE, wy0];
  const tTear = Wd('S4', 'gözyaşı').t0, tHit = Wd('S4', 'düştü').t0, ben = Wd('S4', 'benim').t0;
  const wy = o.wy || D_WY;
  const f = dFig(ctx, t, NT, D_S, o);
  const { J, M } = joints(ctx, f);
  const eye = headPt(ctx, J, M, [3.7, -6.75]);
  // 'benim'e kadar yansıma kendi zamanında 0,3 sn geride (başka biri gibi geç cevap verir) ve seyreltik sırla soluk;
  // el suya 0,3 sn önce değer, yansımanın eli tam 'benim'de gelir; gecikme sıfırlanır (birebir kilit), yansıma bedenin kiline yaklaşır
  const lag = o.lag ?? (.3 * (1 - ramp(t, ben - .02, ben + .1, E.io2)));
  const fR = lag ? dFig(ctx, t - lag, NT, D_S, o) : f;
  const lock = ramp(t, ben, ben + .45, E.out3);
  const brk = ramp(t, tHit, tHit + .15, E.out2) * (1 - ramp(t, tHit + .7, tHit + 1.6, E.io2));
  const refA = o.refA ?? (lerp(.44, .84, lock) + .26 * brk);
  const tx = eye[0] + 4;
  if (o.rings && o.ringFix) for (const R of o.rings) { R.x = tx; R.y = wy + 4; }
  const rings = o.rings || [{ x: tx, y: wy + 4, t0: tHit, A: 80, sq: .62, v: 820, lam: 150, k: 1.4, reach: 1800, life: 4.5, shear: 3.2 },
    { x: D_TOUCH.tip[0] + (NT[0] - D_XE), y: wy + 3, t0: ben - .3, A: 5, sq: .62, v: 260, lam: 34, k: 1.6, reach: 500, life: 2.2 }];
  const water = c => c.rect(NT[0] - 10, wy, 9000, 3000);
  waterBody(ctx, water, wy, t, { a: .16, seed: 3, n: 30, depth: 420 });
  const bank = c => { if (!o.noBank) { for (const [x, sd, h] of [[1290, 5, 64], [1350, 8, 52], [1420, 2, 60]]) narcissus(c, x, wy - 44, 2.3, t, sd, { dir: -1, h }); } };
  if (!o.noBank) { ctx.save(); ctx.beginPath(); ctx.rect(1100, wy, 9000, 3000); ctx.clip(); ctx.globalAlpha = .45; ctx.translate(0, 2 * wy); ctx.scale(1, -1); bank(ctx); ctx.restore(); } // karşı kıyının yansıması (ucuz: dalgasız, halkanın kırılmasından ayrı)
  mirror(ctx, c => figure(c, fR), wy, water, t, { a: refA, rings, calm: 1.0, ringStyle: o.ringStyle, warpBox: [NT[0] - 10, wy, 1180 + (NT[0] - D_XE), wy + 720] });
  if (!o.noBank) { farBank(ctx, 1120, 2600, wy, t, 12, { h: 74, grass: 9, fill: '#3A1B0D' }); bank(ctx); }
  ledge(ctx, NT[0], wy - D_GAP + .2 * D_S, wy);
  litFigure(ctx, f, { x: eye[0] + 30, y: wy + 30, r: 440, c: 'rgba(255,214,160,A)', a: .32, dark: .3 });
  shoreLine(ctx, NT[0], wy);
  // gözyaşı: 'gözyaşı'nda göz pınarında belirir, 'düştü'de suya değer
  if (!o.noTear && t > tTear && t < tHit) {
    const form = ramp(t, tTear, tTear + .2, E.out2), fall = clamp((t - (tTear + .14)) / (tHit - tTear - .14));
    const y = lerp(eye[1] + 16, wy - 6, fall * fall), r = 6.5 * form;
    ctx.save(); ctx.fillStyle = '#F2E6CE'; ctx.strokeStyle = C.ink; ctx.lineWidth = 1.8;
    ctx.beginPath(); ctx.moveTo(tx, y - r * 2.2); ctx.quadraticCurveTo(tx + r * 1.1, y - r * .2, tx, y + r); ctx.quadraticCurveTo(tx - r * 1.1, y - r * .2, tx, y - r * 2.2); ctx.fill(); ctx.stroke(); ctx.restore();
  }
  return { f, eye, reye: [eye[0], 2 * wy - eye[1]], J, M };
}
SCENES_N.D = (ctx, t) => {
  baseView(ctx);
  glaze(ctx, 900, 800, 1100, 'rgba(140,56,26,.55)');
  const z = kf(t, [[10.5, .92], [16, 1.0, E.lin]]);
  camAt(ctx, D_XE + 330, D_WY - 22, z);
  dScene(ctx, t);
};

// ================= çerçeveleme =================
const PLANS = () => ZAMAN.veri.planlar;
function planAt(t) { return ZAMAN.plan(t); }
function drawScene(ctx, t) {
  const p = DIKEY ? { id: 'D' } : planAt(t);
  ctx.save(); SCENES_N[p.id](ctx, t); ctx.restore();
}
function post(ctx, fi) {
  // kil dokusu (çarpma) + vinyet + gren (tohum floor(f/2): iki karede bir değişir)
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = .55; ctx.drawImage(TEX.clay, 0, 0, CW, CH);
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = .9; ctx.drawImage(TEX.vig, 0, 0, CW, CH);
  const g = Math.floor(fi / 2), r = rng(g + 1), L = TEX.grain.length;
  ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = .06;
  const ox = -r() * 512, oy = -r() * 512, tile = TEX.grain[g % L];
  for (let y = oy; y < CH; y += 512) for (let x = ox; x < CW; x += 512) ctx.drawImage(tile, x, y);
  ctx.restore();
}
