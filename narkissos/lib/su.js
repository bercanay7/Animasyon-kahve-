// Su: yansıma (mirror), analitik halka (warpRings, ringLines), yansıma maskesi ve yansıma gecikmesi kuralı. ORTAK DOSYA: yalnız başkan değiştirir.
// Kapı kodundan (kapi/vazo/nark.js) ayrıldı; davranış aynı. Belirlenimci.
'use strict';

// ---- analitik halka: h(r,t) = A·e^(−k·yaş)·sin(ω·yaş − κ·r), cephe v·yaş'ta yumuşakça biter ----
// halka R = {x, y (su yüzeyi, mantıksal), t0 (doğuş; Wd() zamanı), A (genlik), sq (perspektif basıklığı .3–.65), v (hız), lam (dalga boyu), k (sönüm),
//            reach, life (sn), shear (yansımayı yatay şeritlere bölen kırılma), noLines (yalnız kaydırma), mask (çizgiler yansıyan figürün bu kadar px çevresinde çizilmez)}
function ringEnv(R, r, age) {
  const front = R.v * age;
  if (r > front + R.lam) return 0;
  const taper = clamp((front + R.lam - r) / (R.lam * 1.6));
  return R.A * Math.exp(-R.k * age) * taper * Math.exp(-r / (R.reach || 900));
}
function ringOm(R) { return 2 * PI / R.lam * R.v * .8; }
// yansımayı halkalarla piksel piksel kaydırır (yalnız halkanın etkin sınır kutusunda; box: mantıksal [x0,y0,x1,y1] ile kısılır)
// calm {x, y, r} (mantıksal): bu çevrede kaydırma yumuşakça sıfıra iner (yansıyan gözde kırık iz kalmasın)
function warpRings(cv, rings, t, T, box, calm) {
  const S = T.a;
  const act = rings.filter(R => t - R.t0 > 0 && t - R.t0 < (R.life || 4) && R.A * Math.exp(-R.k * (t - R.t0)) * T.a > 2.5);
  if (!act.length) return;
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const R of act) {
    const rr = (R.v * (t - R.t0) + R.lam) * S, cx = R.x * S + T.e, cy = R.y * S + T.f;
    x0 = Math.min(x0, cx - rr); x1 = Math.max(x1, cx + rr); y0 = Math.min(y0, cy - rr * R.sq); y1 = Math.max(y1, cy + rr * R.sq);
  }
  if (box) { x0 = Math.max(x0, box[0] * S + T.e); y0 = Math.max(y0, box[1] * S + T.f); x1 = Math.min(x1, box[2] * S + T.e); y1 = Math.min(y1, box[3] * S + T.f); }
  x0 = Math.max(0, Math.floor(x0)); y0 = Math.max(0, Math.floor(y0)); x1 = Math.min(cv.width, Math.ceil(x1)); y1 = Math.min(cv.height, Math.ceil(y1));
  const bw = x1 - x0, bh = y1 - y0; if (bw <= 2 || bh <= 2) return;
  const cx2 = cv.getContext('2d');
  const src = cx2.getImageData(x0, y0, bw, bh), out = cx2.createImageData(bw, bh), sd = src.data, od = out.data;
  const P = act.map(R => ({ R, cx: R.x * S + T.e - x0, cy: R.y * S + T.f - y0, age: t - R.t0, kap: 2 * PI / (R.lam * S), om: ringOm(R) }));
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
// halkanın görünen tepeleri: vazo dilinde ince kil çizgiler. Merkezdeki küçük elips söner (hale okunmasın)
// o: {col, a, w}
function ringLines(ctx, rings, t, o = {}) {
  ctx.save(); ctx.lineCap = 'round';
  for (const R of rings) {
    const age = t - R.t0; if (R.noLines || age <= 0 || age > (R.life || 4)) continue;
    const kap = 2 * PI / R.lam, om = ringOm(R);
    for (let n = 0; n < 12; n++) {
      const r = (om * age - PI / 2 - 2 * PI * n) / kap; if (r <= 2) break;
      const e = ringEnv(R, r, age) / R.A * clamp((r - R.lam * .5) / (R.lam * 1.5)); if (e < .03) continue;
      ctx.strokeStyle = o.col || `rgba(226,150,96,${clamp(.95 * e * (o.a ?? 1))})`;
      ctx.lineWidth = (o.w || 3.2) * (.5 + .5 * e);
      ctx.beginPath(); ctx.ellipse(R.x, R.y, r, r * R.sq, 0, .12, PI - .12); ctx.stroke();
      ctx.globalAlpha = .55; ctx.beginPath(); ctx.ellipse(R.x, R.y, r, r * R.sq, 0, PI + .12, TAU - .12); ctx.stroke(); ctx.globalAlpha = 1;
    }
  }
  ctx.restore();
}
// ---- yansıma: drawFn'in çizdiğini wy çizgisine göre aynalar; sakin su şerit kaydırması + halkalar; clipFn içinde seyreltik sırla basar ----
// o: {a (saydamlık .2–.85), dx (yatay kayma), calm (sakin dalga genliği), rings, warpBox, calmAt, ringStyle}
function mirror(ctx, drawFn, wy, clipFn, t, o = {}) {
  const T = ctx.getTransform();
  const rx = layer('refl');
  rx.setTransform(T); rx.translate(o.dx || 0, 2 * wy); rx.scale(1, -1); drawFn(rx);
  const wx = layer('warp');
  const S = T.a, wyD = Math.floor(wy * S + T.f), step = Math.max(1, Math.round(2 * S)), calm = (o.calm ?? 1.2) * S;
  if (wyD > 0) wx.drawImage(LY.refl, 0, 0, CW, wyD, 0, 0, CW, wyD);
  for (let y = Math.max(0, wyD); y < CH; y += step) {
    const d = (y - wyD) / S;
    let dx = calm * (Math.sin(d * .19 + t * 1.25) * .7 + Math.sin(d * .053 - t * .8) * .5) * clamp(d / 30);
    if (o.rings) for (const R of o.rings) if (R.shear) {
      const age = t - R.t0; if (age <= 0 || age > (R.life || 4)) continue;
      const yl = (y - T.f) / S, dr = Math.abs(yl - R.y) / R.sq, env = ringEnv(R, dr, age) / R.A;
      if (env > .01) { const band = Math.floor(dr / 17); dx += S * R.A * R.shear * env * Math.exp(-1.6 * age) * Math.sin(band * 2.17 + age * 7.5) * (.6 + .4 * Math.sin(band * 1.31)); }
    }
    wx.drawImage(LY.refl, 0, y, CW, step, dx, y, CW, step);
  }
  if (o.rings) warpRings(LY.warp, o.rings, t, T, o.warpBox, o.calmAt);
  ctx.save(); ctx.beginPath(); clipFn(ctx); ctx.clip();
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha *= o.a ?? .5;
  ctx.drawImage(LY.warp, 0, 0);
  ctx.setTransform(T); ctx.globalAlpha = 1;
  if (o.rings) {
    const mk = o.rings.filter(R => R.mask), free = o.rings.filter(R => !R.mask);
    if (free.length) ringLines(ctx, free, t, o.ringStyle);
    if (mk.length) {
      const rl = layer('rl'); rl.setTransform(T); ringLines(rl, mk, t, o.ringStyle);
      rl.setTransform(1, 0, 0, 1, 0, 0); rl.globalCompositeOperation = 'destination-out'; rl.drawImage(reflMask(Math.max(...mk.map(R => R.mask)) * S), 0, 0, CW, CH); rl.globalCompositeOperation = 'source-over';
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(LY.rl, 0, 0); ctx.setTransform(T);
    }
  }
  ctx.restore();
}
// yansıyan figürün (LY.refl, dalgasız) yumuşak kenarlı, d piksel genişletilmiş silueti (çeyrek çözünürlükte)
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

// ---- yansıma gecikmesi (planlar.md genel kuralı; tek kural) ----
// D03'ten (P038) E04 'benim'e (P053) kadar yansıma gerçeği 9 kare (0,3 sn) geç izler; A bölümündeki havuz planları da (tanınmadan önce) aynı kurala uyar.
// 'benim'de gecikme 0,1 sn içinde sıfırlanır (kilit); sonrası birebir. Kullanım: figürü refLag(t) kadar önceki zamanla çizip yansıtın:
//   const lag = refLag(t); const fR = lag ? poz(t - lag) : poz(t); mirror(ctx, c => figure(c, fR), …)
// FIG_T de (göz kırpma, boşta salınım) aynı gecikmeyle çizilmeli: withFigT(t - lag, () => figure(c, fR)).
const REF_LAG = 9 / 30;
function refLag(t) {
  const ben = A('E04@benim');
  if (t >= ben + .1) return 0;
  return REF_LAG * (1 - ramp(t, ben - .02, ben + .1, E.io2));
}
// yansıma ne kadar kilitli (0: soluk/gecikmeli, 1: 'benim'den sonra bedenin kili): mirror a değeri için
function refLock(t) { return ramp(t, A('E04@benim'), A('E04@benim') + .45, E.out3); }
// figürün zaman bağımlı ayrıntılarını (göz kırpma, nefes) başka bir zamanda çizmek için
function withFigT(tt, fn) { const k = window.FIG_T; window.FIG_T = tt; try { return fn(); } finally { window.FIG_T = k; } }
