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
function warpRings(cv, rings, t, T, box, calm) {
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
  // tur 3: sakin bölge (calm {x, y, r}, mantıksal): yansıyan gözün çevresinde kaydırma yumuşakça sıfıra iner (ince göz çizgisi piksel piksel kırılıp 'kırık iz' bırakmasın)
  const cc = calm ? [calm.x * S + T.e - x0, calm.y * S + T.f - y0, calm.r * S] : null;
  for (let y = 0; y < bh; y++) for (let x = 0; x < bw; x++) {
    let dx = 0, dy = 0;
    for (const q of P) {
      const ex = x - q.cx, ey = (y - q.cy) / q.R.sq, r = Math.hypot(ex, ey);
      if (r < 1) continue;
      const env = ringEnv(q.R, r / S, q.age); if (env === 0) continue;
      const d = env * S * Math.cos(q.om * q.age - q.kap * r);
      dx += d * ex / r; dy += d * ey / r * q.R.sq * 2.2;
    }
    if (cc) { const q = clamp((Math.hypot(x - cc[0], y - cc[1]) / cc[2] - 1) / 1.2); const w = q * q * (3 - 2 * q); dx *= w; dy *= w; }
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
    const age = t - R.t0; if (R.noLines || age <= 0 || age > (R.life || 4)) continue;
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
  if (o.rings) warpRings(LY.warp, o.rings, t, T, o.warpBox, o.calmAt);
  ctx.save(); ctx.beginPath(); clipFn(ctx); ctx.clip();
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = o.a ?? .5;
  ctx.drawImage(LY.warp, 0, 0);
  ctx.setTransform(T); ctx.globalAlpha = 1;
  if (o.rings) {
    const mk = o.rings.filter(R => R.mask), free = o.rings.filter(R => !R.mask);
    if (free.length) ringLines(ctx, free, t, o.ringStyle);
    if (mk.length) { // tur 3: maskeli halka çizgileri yansıyan figürün çevresindeki şeritte (R.mask px) çizilmez: baş çevresinde yay ('hale') kalmaz; çizgiler açık suda eşmerkezli görünür
      const rl = layer('rl'); rl.setTransform(T); ringLines(rl, mk, t, o.ringStyle);
      rl.setTransform(1, 0, 0, 1, 0, 0); rl.globalCompositeOperation = 'destination-out'; rl.drawImage(reflMask(Math.max(...mk.map(R => R.mask)) * S), 0, 0, CW, CH); rl.globalCompositeOperation = 'source-over';
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(LY.rl, 0, 0); ctx.setTransform(T);
    }
  }
  ctx.restore();
}
// yansıyan figürün (LY.refl, dalgasız) yumuşak kenarlı, d piksel genişletilmiş silueti (çeyrek çözünürlükte; belirlenimci)
const MQ = 4;
function reflMask(d) {
  if (!LY.mq) { LY.mq = makeCanvas(Math.ceil(CW / MQ), Math.ceil(CH / MQ)); LY.mq2 = makeCanvas(LY.mq.width, LY.mq.height); }
  const w = LY.mq.width, h = LY.mq.height, a = LY.mq.getContext('2d'), b = LY.mq2.getContext('2d');
  a.setTransform(1, 0, 0, 1, 0, 0); a.globalCompositeOperation = 'source-over'; a.filter = 'none'; a.clearRect(0, 0, w, h);
  const r = d / MQ;
  for (const k of [.35, .7, 1]) for (let i = 0; i < 16; i++) { const an = i / 16 * TAU; a.drawImage(LY.refl, Math.cos(an) * r * k, Math.sin(an) * r * k, w, h); }
  b.setTransform(1, 0, 0, 1, 0, 0); b.clearRect(0, 0, w, h); b.filter = `blur(${Math.max(1, r * .25)}px)`; b.drawImage(LY.mq, 0, 0); b.filter = 'none';
  return LY.mq2;
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
const LK_MOD = { jaw: true, modern: true, rf: true, hairPts: HAIR_MOD, garment: 'coat', coatCol: '#6E331B', sleeveCol: '#6E331B', earHidden: false, headS: 1.45, eyeS: 1.12 }; // tur 1: daha genç (büyük baş, iri göz)
// tur 1: efeb başı (kısa bukleli saç, kulak açık, köşeli çene) ve görünür khiton (seyreltik sır, koyu sır yaka/etek/kol kenarı; nokta deseni ve kemer yok)
const KHITON = { col: '#93492A', edge: 1.3, sleeve: false };
const LK_NK = { hair: 'short', rf: true, garment: 'short', noCurls: true, efeb: true, hairPts: HAIR_EF, jaw: true, khiton: KHITON, noBelt: true };
function phoneScene(ctx, t, o) {
  const m = o.m; // 0 telefon camı, 1 havuz
  baseView(ctx);
  glaze(ctx, 1100, 820, 1100, `rgba(${lerp(80, 120, m) | 0},${lerp(42, 48, m) | 0},${lerp(28, 22, m) | 0},.45)`);
  const p = { torso: .3, neck: o.neckA ?? .42, head: (o.headA ?? .55) + (o.headNod || 0), shN: .38, elN: .5, shF: .32, elF: .55, handN: 'fist', handF: 'fist', smile: 0, brow: .15, mouthOpen: 0, blink: o.blink,
    mouthFlat: !!o.neutral, eyeWide: o.neutral ? .3 : 0 }; // tur 3: nötr ağız, açık göz
  let f = { x: 0, y: 0, s: 20.5, dir: 1, sty: STY.red, lk: LK_MOD, seed: 31, idle: .6, p, faceW: 1.35, stripe: .35 };
  f = placeNeck(ctx, f, o.neck || [640, 370]);
  const { J: J0, M: M0 } = joints(ctx, f), e = headPt(ctx, J0, M0, [3.7, -6.75]);
  // küçük telefon camı (yüzün iki katı kadar), eğik tutulduğu için yansıma camın ortasına kayar (dxR)
  // tur 3: yansıma gerçek başın tam altında (dx = 0), cam yüzden uzak (wy), cam başın altında; iki yüz çapraz 'öpüşme' çizgisi kurmasın
  const wy = o.wy ?? 600, pcx = e[0] + (o.phDx ?? 330), pw = o.pw ?? 270;
  const dxR = o.refDx != null ? o.refDx : o.dxFixed ? pcx - e[0] - 20 : lerp(pcx - e[0] - 20, 0, m);
  const hy = o.handY ?? 340;
  if (o.armToPhone) { f.ik = { hN: [pcx - pw - 70, wy + hy + 120 + 420 * m] }; f.noFarArm = true; } // tur 3: yakın kol telefonu tutan ele uzanır (kamera geniş; sarkan yumruk görünmesin)
  if (o.auto) o.cam = [pcx - 120, wy + 40, o.cam[2]];
  camAt(ctx, ...o.cam);
  const phone = roundRectPts(pcx - pw, wy, pcx + pw, wy + 900, 56, 56);
  const pool = ellipsePts(pcx - 100, wy + 360, 1300, 360);
  const shape = morphPts(phone, pool, m);
  const clip = c => poly(c, shape);

  // figür: omuz başı solda kadraj kenarında, başı ekrana eğik; ekran ışığı alttan

  waterBody(ctx, clip, wy, t, { a: .2 * m, seed: 6, span: [300, 2100], n: 40 });
  if (o.feedA > .005) phoneFeed(ctx, clip, pcx, pw, wy, o.feed || 0, o.feedA * (1 - m));
  // eğik cam: yansıma camın ortasına kayar (dx)
  const rings = typeof o.rings === 'function' ? o.rings(pcx, wy, e) : o.rings;
  mirror(ctx, c => figure(c, f), wy, clip, t, { a: o.refA ?? .42, rings, calm: lerp(.15, 1.2, m), dx: dxR, calmAt: o.eyeCalm ? { x: e[0] + dxR, y: 2 * wy - e[1], r: o.eyeCalm } : null });
  const ph = 1 - m;
  if (o.glare && ph > .01) glassGlare(ctx, clip, pcx, wy, pw, ph * o.glare, t);
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
  if (ph > .02) phoneHand(ctx, pcx - pw, wy, t, ph, o.thumb || 0, o.light, hy);
  return f;
}
const SCENES_N = {};
// tur 3 (A/E): yansıma gerçek başın birebir aynası ve tam altında (dx 0); cam yüzden uzak (wy 630: burun-burun ~300 px), baş daha az eğik (iki yüz çapraz 'öpüşme' çizgisi kurmaz),
// yansıma soluk (refA .3) ve üstünden çapraz cam parlaması geçer; gerçek yüzde nötr ağız, açık göz; yakın kol telefonu tutan ele uzanır; el camın sol alt köşesinde (başparmak yansıyan yüzden uzak)
const PH3 = { refDx: 0, phDx: 140, pw: 230, wy: 630, armToPhone: true, headA: .3, neckA: .3, neutral: true, glare: 1, handY: 480, eyeCalm: 55 };
SCENES_N.A = (ctx, t) => {
  const tc = Wd('S1', 'camın').t0;
  const m = ramp(t, Wd('S1', 'içinden').t0 - .05, 3.45, E.io2);
  // tur 2: kadraj telefona yakın (gövde kadrajın sol kenarında küçük kalır), yüz büyük
  const z = kf(t, [[0, .82], [2.8, .86, E.io2], [3.5, 1.3, E.in2]]);
  const fx = lerp(720, 1000, ramp(t, 2.8, 3.5, E.in2)), fy = lerp(650, 760, ramp(t, 2.8, 3.5, E.in2));
  // başparmak üç kez yukarı kaydırır; ekran içeriği her kaydırmada yukarı kayar, ekran ışığı kısa bir an değişir (yeni içerik)
  const flicks = [.3, 1.0, 1.7];
  const th = flicks.reduce((v, f0) => Math.max(v, ramp(t, f0, f0 + .24, E.io2) * (1 - ramp(t, f0 + .3, f0 + .58, E.io2))), 0);
  const feed = flicks.reduce((v, f0) => v + 330 * E.out3(ramp(t, f0 + .1, f0 + .5, E.lin)), 0);
  const fl = flicks.reduce((v, f0, i) => v + (t > f0 + .2 ? [.12, -.1, .08][i] : 0), 0) * (1 - ramp(t, 2.4, 2.9, E.io2));
  phoneScene(ctx, t, {
    m, thumb: th, cam: [fx, fy, z], ...PH3, light: lerp(.75 + fl, .35, m), refA: lerp(.2, .42, m), feed, feedA: 1 - ramp(t, 2.0, 2.6, E.io2),
    headNod: .04 * Math.sin(t * 1.1) - .05 * ramp(t, Wd('S1', 'kendine').t0, Wd('S1', 'bakıyorsun').t1, E.io2) + .06 * ramp(t, tc - .2, tc + .3, E.io2),
    rings: (cx, wy) => [{ x: cx + 20, y: wy + 190, t0: tc, A: 9, sq: .32, v: 330, lam: 44, k: .9, reach: 1200, life: 4 }],
  });
};
SCENES_N.E = (ctx, t) => {
  const t0 = 16.0;
  const m = 1 - ramp(t, Wd('S5', 'bakmayı').t0, Wd('S5', 'yine').t1, E.io2);
  // tur 3: A'nın geometrisi (PH3); kamera havuz yakınından (A'nın sonu gibi) telefon kadrajına açılır, sonra çok yavaş yaklaşır
  const u = ramp(t, Wd('S5', 'bakmayı').t0, Wd('S5', 'yine').t1, E.io2);
  const z = lerp(1.22, .83, u) + .04 * ramp(t, Wd('S5', 'yine').t1, 19.5, E.lin);
  const fx = lerp(990, 720, u), fy = lerp(740, 655, u);
  phoneScene(ctx, t, {
    m, ...PH3, cam: [fx, fy, z], light: lerp(.25, 1, ramp(t, Wd('S5', 'yine').t0, Wd('S5', 'bırakamadı').t0, E.io2)), refA: lerp(.42, .2, 1 - m),
    headNod: .03 * Math.sin(t * .9),
    rings: (cx, wy) => [{ x: cx - 10, y: wy + 170, t0: S('S5').t0 - .1, A: 7, sq: .32, v: 220, lam: 40, k: .7, reach: 1000, life: 4.5 },
      { x: cx + 40, y: wy + 200, t0: Wd('S5', 'bırakamadı').t0, A: 6, sq: .32, v: 220, lam: 40, k: .8, reach: 900, life: 3 }],
  });
};

// tur 3: çapraz cam parlaması: yansımanın üstünden geçen iki paralel, yumuşak kenarlı şerit (sağ üstten sol alta); 'cam' okunsun, yansıma camın içinde kalsın
function glassGlare(ctx, clip, pcx, wy, pw, a, t) {
  ctx.save(); ctx.beginPath(); clip(ctx); ctx.clip();
  const ang = -.62, ca = Math.cos(ang), sa = Math.sin(ang), drift = 6 * Math.sin(t * .5);
  for (const [off, w, k] of [[-40, 110, 1], [120, 38, .7]]) {
    const cx = pcx + off + drift, cy = wy + 330;
    // şeridin ekseni yönü (ca, sa); dik yönde (−sa, ca) yumuşak profil
    const nx = -sa, ny = ca;
    const g = ctx.createLinearGradient(cx - nx * w, cy - ny * w, cx + nx * w, cy + ny * w);
    g.addColorStop(0, 'rgba(255,236,210,0)'); g.addColorStop(.35, `rgba(255,236,210,${.13 * k * a})`); g.addColorStop(.5, `rgba(255,240,220,${.17 * k * a})`); g.addColorStop(.65, `rgba(255,236,210,${.13 * k * a})`); g.addColorStop(1, 'rgba(255,236,210,0)');
    ctx.fillStyle = g; ctx.beginPath();
    const L = 1400;
    ctx.moveTo(cx - ca * L - nx * w, cy - sa * L - ny * w); ctx.lineTo(cx + ca * L - nx * w, cy + sa * L - ny * w); ctx.lineTo(cx + ca * L + nx * w, cy + sa * L + ny * w); ctx.lineTo(cx - ca * L + nx * w, cy - sa * L + ny * w); ctx.closePath(); ctx.fill();
  }
  ctx.restore();
}
// ekran içeriği (akış): camın arkasında soluk kartlar; her kaydırmada yukarı kayar (tur 2: kaydırma görünür olsun)
function phoneFeed(ctx, clip, pcx, pw, wy, off, a) {
  ctx.save(); ctx.beginPath(); clip(ctx); ctx.clip();
  const x0 = pcx - pw + 46, w = 2 * pw - 92, H = 330;
  for (let k = -1; k < 6; k++) {
    const y = wy + 80 + k * H - off; if (y > wy + 1000 || y + H < wy) continue;
    ctx.globalAlpha = a;
    ctx.fillStyle = 'rgba(255,226,186,.09)'; ctx.beginPath(); ctx.roundRect(x0, y, w, 210, 18); ctx.fill();
    ctx.fillStyle = 'rgba(255,226,186,.1)';
    ctx.beginPath(); ctx.arc(x0 + 26, y + 238, 18, 0, TAU); ctx.fill();
    ctx.beginPath(); ctx.roundRect(x0 + 56, y + 228, w * (.45 + .2 * ((k * 7 + 3) % 3) / 2), 12, 6); ctx.fill();
    ctx.beginPath(); ctx.roundRect(x0 + 56, y + 252, w * .3, 10, 5); ctx.fill();
  }
  ctx.restore();
}
// telefonu tutan el (tur 2): avuç camın sol kenarının arkasında, alt köşede; başparmak kısa (iki boğum + tırnak), camın sol alt kenarında
// th 0..1: kaydırma (başparmak yukarı süpürür, uç ~60 birim yol alır); yüzün yansımasına (ağız, çene) hiç yaklaşmaz
function phoneHand(ctx0, X0, wy, t, a, th, light, hy = 340) {
  const T = ctx0.getTransform(), ctx = layer('hand'); ctx.setTransform(T);
  ctx.save(); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  const Y = wy + hy, ink = C.ink, skin = '#C9703F';
  // kol (ceket kolu) alttan sola
  ctx.beginPath(); ctx.moveTo(X0 - 300, Y + 420); ctx.quadraticCurveTo(X0 - 210, Y + 190, X0 - 110, Y + 105); ctx.lineTo(X0 - 30, Y + 175); ctx.quadraticCurveTo(X0 - 110, Y + 260, X0 - 140, Y + 440); ctx.closePath();
  ctx.fillStyle = '#6E331B'; ctx.fill(); ctx.strokeStyle = ink; ctx.lineWidth = 4; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(X0 - 118, Y + 116); ctx.lineTo(X0 - 40, Y + 186); ctx.lineWidth = 2.4; ctx.stroke(); // kol ağzı
  // başparmak: kök avuçta (X0-26, Y+40); iki boğum; kaydırırken yukarı döner ve düzleşir
  const B = [X0 - 26, Y + 40], aP = lerp(.1, -1.1, th), bend = lerp(.45, .1, th), L1 = 40, L2 = 32, W1 = 13, W2 = 11.5;
  const K = [B[0] + Math.cos(aP) * L1, B[1] + Math.sin(aP) * L1], aD = aP - bend, P = [K[0] + Math.cos(aD) * L2, K[1] + Math.sin(aD) * L2];
  const nrm = a0 => [-Math.sin(a0), Math.cos(a0)], n1 = nrm(aP), n2 = nrm(aD), nk = nrm((aP + aD) / 2);
  ctx.beginPath();
  ctx.moveTo(B[0] - n1[0] * W1, B[1] - n1[1] * W1);
  ctx.lineTo(K[0] - nk[0] * W1 * .95, K[1] - nk[1] * W1 * .95);
  ctx.lineTo(P[0] - n2[0] * W2, P[1] - n2[1] * W2);
  ctx.arc(P[0], P[1], W2, aD - PI / 2, aD + PI / 2);
  ctx.lineTo(K[0] + nk[0] * W1 * 1.05, K[1] + nk[1] * W1 * 1.05);
  ctx.lineTo(B[0] + n1[0] * W1 * 1.15, B[1] + n1[1] * W1 * 1.15);
  ctx.closePath(); ctx.fillStyle = skin; ctx.fill(); ctx.lineWidth = 3.6; ctx.strokeStyle = ink; ctx.stroke();
  // boğum çizgisi ve tırnak (üst yüzde, uca yakın)
  ctx.beginPath(); ctx.moveTo(K[0] - nk[0] * W1 * .7, K[1] - nk[1] * W1 * .7); ctx.lineTo(K[0] - nk[0] * W1 * .05, K[1] - nk[1] * W1 * .05); ctx.lineWidth = 2.2; ctx.stroke();
  const dn = [Math.cos(aD), Math.sin(aD)], nc = [P[0] - dn[0] * 9 - n2[0] * 4.5, P[1] - dn[1] * 9 - n2[1] * 4.5];
  ctx.save(); ctx.translate(...nc); ctx.rotate(aD); ctx.beginPath(); ctx.roundRect(-8, -5.5, 17, 11, [3, 5.5, 5.5, 3]); ctx.fillStyle = '#DE9564'; ctx.fill(); ctx.lineWidth = 2; ctx.stroke(); ctx.restore();
  // avuç: camın sol kenarını arkadan kavrar; iki parmak ucu camın kenarında
  ctx.beginPath(); ctx.moveTo(X0 - 112, Y + 108); ctx.quadraticCurveTo(X0 - 92, Y + 30, X0 - 30, Y + 4); ctx.lineTo(X0 + 6, Y + 14); ctx.lineTo(X0 + 8, Y + 150); ctx.quadraticCurveTo(X0 - 20, Y + 186, X0 - 36, Y + 180); ctx.closePath();
  ctx.fillStyle = skin; ctx.fill(); ctx.lineWidth = 4; ctx.stroke();
  for (const yy of [92, 130]) { ctx.beginPath(); ctx.moveTo(X0 - 8, Y + yy); ctx.quadraticCurveTo(X0 + 14, Y + yy - 2, X0 + 16, Y + yy + 14); ctx.quadraticCurveTo(X0 + 8, Y + yy + 26, X0 - 6, Y + yy + 24); ctx.fillStyle = skin; ctx.fill(); ctx.lineWidth = 3; ctx.stroke(); }
  // ekran ışığı elin üstünde
  ctx.globalCompositeOperation = 'source-atop';
  const g = ctx.createRadialGradient(X0 + 80, Y - 80, 0, X0 + 80, Y - 80, 340); g.addColorStop(0, `rgba(255,226,186,${.3 * light})`); g.addColorStop(1, 'rgba(255,226,186,0)');
  ctx.fillStyle = g; ctx.fillRect(X0 - 600, Y - 400, 1200, 1200);
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
    ik: { fN: o.flatFeet ? [px - 47 * s, gy - 1.7 * s, o.flatFeet] : [px - 41 * s, gy - 2.5 * s, PI / 2 - .25], fF: o.flatFeet ? [px - 47.6 * s, gy - 2.0 * s, o.flatFeet] : [px - 43 * s, gy - 4.5 * s, PI / 2 - .35],
      hF: o.hF || [px + 31 * s, gy - 1.5 * s], hN: o.hN || [px + 33 * s, gy - 1.2 * s] } };
}
function pPose(o = {}) {
  return { torso: 1.33, neck: -.5 + (o.neck || 0), head: .38 + (o.head || 0), handN: o.handN || 'flat', handF: 'flat', wrN: o.wrN || 0, wrF: 0,
    smile: o.smile || 0, brow: o.brow ?? .2, mouthOpen: o.mouthOpen || 0, browUp: o.browUp || 0, eyeWide: o.eyeWide || 0, blink: o.blink };
}
// kaya kenarı (dirseklerin dayandığı çıkıntı) suyun içine iner
function ledge(ctx, xe, gy, wy) {
  crag(ctx, [[-2600, gy + 4], [xe - 260, gy - 6], [xe - 40, gy - 2], [xe + 4, gy + 14], [xe - 6, wy + 30], [xe - 40, wy + 700], [-2600, wy + 700]], { fill: '#5A2C16', seed: 9, flat: [0, 5, 6], wob: 4, strata: 4, lobes: 3 });
}
let C_HEM = .62, C_FOOT = -2.9;
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
  // tur 3: bacaklar düz, yerde (diz kırılıp ayak kalkmaz: 'ayak sallama' okunmasın); khiton uyluk ortasına iner, etek ucu uyluğa dik
  let f = proneFig(px, gy, s, { ...pPose({ head: .08 * look, neck: .04 * look, handN: reach > .3 ? 'open' : 'flat', smile: .25 * reach }), hemPerp: true, hemT: C_HEM }, { hN, hF: [grip[0] - 9, grip[1]], flatFeet: C_FOOT });
  const { J } = joints(ctx, f);
  f.p = { ...f.p, wrN: aN - J.AN.foA, wrF: .12 - J.AF.foA };
  const water = c => c.rect(xe - 10, wy, 4000, 2000);
  waterBody(ctx, water, wy, t, { a: .2, seed: 5, span: [xe, 2300], n: 28, depth: 380 });
  const bank = c => { for (const [x, sd, h] of [[1290, 5, 60], [1318, 8, 48], [1350, 2, 56]]) narcissus(c, x, wy - 14, .62, t, sd, { dir: -1, h }); };
  mirror(ctx, bank, wy, c => c.rect(1150, wy, 4000, 2000), t, { a: .45, calm: 1.1 });
  mirror(ctx, c => figure(c, f), wy, water, t, { a: .42, calm: 1.1 });
  farBank(ctx, 1180, 2600, wy, t, 17, { h: 22, grass: 7, fill: '#3A1B0D' }); bank(ctx);
  ledge(ctx, xe, gy, wy);
  for (let i = 0; i < 5; i++) { const gx = 120 + i * 160; if (gx > px - 50 * s && gx < xe) continue; grass(ctx, gx, gy + 2, 1.6, t, i + 11); } // tur 3: figürün altında kalan ot tutamı yok (dibi bacağın altından nokta sırası gibi taşıyordu)
  // tur 2: ayak arkasındaki ince mızrak çubuğu silindi (mızrak okunmuyordu; kayanın kenarıyla karışıyordu)
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
  // tur 2: kalkış yavaş ve alçak (dirsek kayada kalır; hareket bulanıklığında şekilsiz kol lekesi olmasın)
  const son = Wd('S4', 'sonra').t0, ben = Wd('S4', 'benim').t0, tTouch = ben - .3, tBack = ben + .45;
  const rest = D_REST, mid = { w: [455, 545], a: 1.05, hand: 'point' }, touch = { w: [600, 520], a: 1.068, hand: 'point' };
  const t0 = son - .25, tm = t0 + .5;
  const mix = (A, B, u) => ({ w: lerp2(A.w, B.w, u), a: lerp(A.a, B.a, u), hand: u < .35 ? A.hand : B.hand });
  if (t < t0) return { ...rest, k: 0 };
  if (t < tm) return { ...mix(rest, mid, E.in2(clamp((t - t0) / (tm - t0)))), k: 1 };
  if (t < tTouch) return { ...mix(mid, touch, E.out2(clamp((t - tm) / (tTouch - tm)))), k: 2 };
  if (t < tBack) return { ...touch, k: 3 };
  if (t < tBack + .5) return { ...mix(touch, mid, E.io2(clamp((t - tBack) / .5))), k: 4 };
  return { ...mix(mid, rest, E.io2(clamp((t - tBack - .5) / .5))), k: 5 };
}
function dPoseO(t) {
  const tear = Wd('S4', 'düştü').t0, son = Wd('S4', 'sonra').t0, ben = Wd('S4', 'benim').t0;
  const lean0 = ramp(t, 10.5, 11.3, E.io2) * .04;
  const flinch = settle(t, tear + .05, .05, 1.2, 2.2);
  const leanIn = ramp(t, son, ben - .05, E.io2) * .05 * (1 - ramp(t, ben, ben + .35, E.out3));
  const recoil = ramp(t, ben - .02, ben + .22, E.out3) * .34 * (1 - .45 * ramp(t, ben + .5, 16, E.io2));   // irkilme (tur 2): baş belirgin geri çekilir
  const sad = ramp(t, ben + .6, 16, E.io2);
  return { neck: lean0 + leanIn * .5 - recoil * .6, head: lean0 + flinch + leanIn - recoil * .5,
    smile: -.2 - .3 * sad, brow: .3 + 1.1 * ramp(t, ben - .02, ben + .15, E.out3) - .45 * sad, mouthOpen: 2.1 * ramp(t, ben - .02, ben + .18, E.out3) * (1 - .6 * sad), browUp: .5 * ramp(t, ben - .02, ben + .15, E.out3) * (1 - .7 * sad), eyeWide: .55 * ramp(t, ben - .02, ben + .12, E.out3) * (1 - .8 * sad), blink: t > ben - .02 && t < ben + .12 ? 0 : undefined };
}
const D_S = 26, D_XE = 640;
let D_RV = 1000, D_RL = 115;
function dFig(ctx, t, NT, s = D_S, o = {}) { // NT: [kaya kenarı x, su çizgisi y]
  const gy = NT[1] - D_GAP + .2 * s, px = NT[0] - 30 * s;
  const q = dPoseO(t), pp = pPose(q);
  pp.neck = 1.0 + q.neck; pp.head = -.9 + q.head; // boyun kenardan aşağı sarkar, yüz suya bakar (öpüşme ekseni)
  const R = o.handOff ? { w: [140, 600], a: 1.62, hand: 'flat' } : o.rest ? D_REST : dReach(t); // handOff: el kadraj dışında (kapak)
  pp.handN = R.hand; pp.handF = 'flat';
  const hN = [R.w[0] + (NT[0] - D_XE), R.w[1] + (NT[1] - D_WY)];
  const f = proneFig(px, gy, s, pp, { idle: .3, faceW: 1.5, stripe: .3, hN, hF: o.handOff ? [px + 12 * s, gy - .2 * s] : [px + 17 * s, gy - .4 * s] });
  f.noFarArm = true; // tur 2: uzak kol gövdenin arkasında (kayanın üstünde kütük okunmasın)
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
  // tur 3: gözyaşı halkası ikiye ayrıldı: yüzü dağıtan kaydırma (çizgisiz) + görünen çizgiler (hızlı, sık, eşmerkezli; yansıyan figürün 60 px çevresinde çizilmez: hale okunmasın)
  const rings = o.rings || [{ x: tx, y: wy + 4, t0: tHit, A: 80, sq: .62, v: 820, lam: 150, k: 1.4, reach: 1800, life: 4.5, shear: 3.2, noLines: true },
    { x: tx, y: wy + 4, t0: tHit, A: 1, sq: .62, v: D_RV, lam: D_RL, k: .8, reach: 2600, life: 4.5, mask: 80 },
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
