// act1: I · Sultanın okulları (B01–B06). Yardımcılar a1_ önekli (act3.js de kullanır).
'use strict';
if (typeof document !== 'undefined' && document.fonts) document.fonts.load('400 40px "GFS Didot"', 'ΚΑΦΕΝΕΙΟΝ');

// ——— genel yardımcılar ———
// kelime zamanı; bulunamazsa konsola yazar (cümle başına düşer)
function a1_W(id, w, n = 0, end = false) {
  const v = Wd(id, w, n, end);
  if (v === S(id) && !(window.WORDS || []).some(x => x.id === id && x.s === v)) console.log('[a1] kelime yok:', id, w);
  return v;
}
// durağan katman önbelleği: baskı geçişinin kayıklık büyütmesi (REG.boost) önbelleğe girmez
function a1_cache(key, draw, w, h) {
  if (LCACHE[key]) return LCACHE[key];
  const b = REG.boost; REG.boost = 1;
  const c = layerCache(key, draw, w, h);
  REG.boost = b; return c;
}
const a1_img = (ctx, c) => ctx.drawImage(c, 0, 0, W, H);
// kenar paylı önbellek (paralaks katmanı kare dışına taşar): dünya −m..W+m
const A1_LCM = {};
function a1_cacheM(key, draw, m = 220) {
  if (A1_LCM[key]) return A1_LCM[key];
  const b = REG.boost; REG.boost = 1;
  const c = makeCanvas(Math.ceil((W + 2 * m) * RS), Math.ceil((H + 2 * m) * RS)), g = c.getContext('2d');
  g.setTransform(RS, 0, 0, RS, m * RS, m * RS); draw(g);
  REG.boost = b; return (A1_LCM[key] = { c, m });
}
const a1_imgM = (ctx, o) => ctx.drawImage(o.c, -o.m, -o.m, W + 2 * o.m, H + 2 * o.m);
const a1_rect = (x0, y0, x1, y1) => PL([[x0, y0], [x1, y0], [x1, y1], [x0, y1]]);
// halka (dış saat yönü, iç ters): nonzero ile çerçeve bandı
function a1_ring(x0, y0, x1, y1, m) {
  const p = new Path2D();
  p.moveTo(x0, y0); p.lineTo(x1, y0); p.lineTo(x1, y1); p.lineTo(x0, y1); p.closePath();
  p.moveTo(x0 + m, y0 + m); p.lineTo(x0 + m, y1 - m); p.lineTo(x1 - m, y1 - m); p.lineTo(x1 - m, y0 + m); p.closePath();
  return p;
}
const a1_ell = (x, y, rx, ry, r = 0) => { const p = new Path2D(); p.ellipse(x, y, rx, ry, r, 0, TAU); return p; };
// basılma darbesi: 0 → 1, kısa büyümeyle (lastik damga)
const a1_pop = (t, t0, d = .16) => t < t0 ? 0 : 1 + (1 - E.out3(clamp((t - t0) / d))) * .35;

// toz: ışıkta yavaş süzülen zerreler (durağan belge/harita çekimlerinde sürekli, sakin hareket)
function a1_dust(ctx, t, seed = 1, n = 34, o = {}) {
  const r = rng(seed), col = o.col || P.sepia;
  ctx.save();
  for (let i = 0; i < n; i++) {
    const x0 = r() * W, y0 = r() * H, vx = 6 + r() * 14, vy = -4 - r() * 9, sz = 1.1 + r() * 1.8, a = (.25 + r() * .3) * (o.a ?? 1), ph = r() * 50;
    const x = ((x0 + vx * t + noise1(t * .3 + ph, i) * 24) % (W + 40) + W + 40) % (W + 40) - 20;
    const y = ((y0 + vy * t + noise1(t * .25 + ph, i + 9) * 18) % (H + 40) + H + 40) % (H + 40) - 20;
    ctx.globalAlpha = a * (.6 + .4 * Math.sin(t * 1.3 + ph)); ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, sz, 0, TAU); ctx.fill();
  }
  ctx.restore();
}
// Figür: bust + head3q. Boşta salınım, nefes, göz kırpma; pozlar ikişer karede (15 fps)
function a1_fig(ctx, t, o) {
  const tf = Math.floor(t * 15) / 15, sd = o.seed || 1;
  const io = idleOffsets(tf, sd, o.idle ?? 1), bl = o.blink === false || (window.noBlink && window.noBlink(t)) ? 0 : blinkAt(tf, sd);
  const pp = { ...PEOPLE.anon, ...(PEOPLE[o.who] || {}), ...(o.id || {}) };
  const eo = (o.eyeOpen ?? pp.eyeOpen ?? .8) * (1 - .9 * bl);
  const by = o.y + io.breath * .6 * (o.s / 1.2);
  const bs = o.bs ?? o.s;
  if (o.body !== false) bust(ctx, { x: o.x + (o.bdx || 0), y: by + (o.bdy || 0), s: bs, dir: o.dir, coat: o.coat || 'setre', col: o.col || 'ink', w: o.w || 1, len: o.len, seed: sd, tilt: (o.btilt || 0) + io.torso, turn: o.turn, sep: o.sep, back: o.back, arms: o.arms, collarCol: o.collarCol, skin: o.skin });
  if (o.under) o.under(by, io);
  const ht = (o.tilt || 0) + io.head + io.neck * .5, hd = o.hdir ?? o.dir;
  head3q(ctx, { x: o.x, y: by, s: o.s, dir: hd, who: o.who || 'anon', id: o.id, gear: o.gear, gearCol: o.gearCol, light: o.light || 'front', lookAt: o.lookAt, look: o.look, age: o.age, tilt: ht, eyeOpen: eo, skin: o.skin, wide: o.wide });
  if (o.over) o.over({ x: o.x, y: by, s: o.s, dir: hd, tilt: ht, WD: o.wide ?? pp.WD ?? 1.08, HY: pp.HY ?? 1 });
  return by;
}
// Çocuk: baş büyük, gövde dar ve kısa omuzlu
function a1_kid(ctx, t, o) {
  return a1_fig(ctx, t, { age: 12, gear: 'fes', coat: 'setre', col: 'navy', bs: o.s * .8, bdy: o.s * 12, w: .86, ...o });
}

// ——— şematik imparatorluk haritası (lon/lat → ekran) ———
// İçerik alanı 110..1810 × 90..990; boylam 5–57, enlem 46,4–23
const A1M = { x0: 110, y0: 90, kx: 32.7, ky: 38.5, lon0: 5, lat0: 46.4, cx0: 110, cy0: 90, cx1: 1810, cy1: 990, sx0: 70, sy0: 50, sx1: 1850, sy1: 1030 };
const a1_p = (lon, lat) => [A1M.x0 + (lon - A1M.lon0) * A1M.kx, A1M.y0 + (A1M.lat0 - lat) * A1M.ky];
const a1_pts = f => { const o = []; for (let i = 0; i < f.length; i += 2) o.push(a1_p(f[i], f[i + 1])); return o; };
// kaba kıyılar (denizler; adalar evenodd ile delinir)
const A1_SEAS = {
  med: [4, 43.4, 5.4, 43.25, 6, 43.1, 7.3, 43.7, 8.9, 44.4, 9.8, 44.1, 10.3, 43.5, 10.5, 42.95, 11.2, 42.4, 11.8, 42.1, 12.25, 41.75, 13.2, 41.3, 14.25, 40.85, 14.75, 40.65, 15.6, 40.05, 15.9, 39.5, 16.05, 38.9, 15.65, 38.3, 15.7, 37.95, 16.1, 38.0, 16.55, 38.75, 17.15, 39.1, 16.6, 39.75, 17.2, 40.45, 18.0, 40.05, 18.35, 39.8, 18.5, 40.15, 17.95, 40.65, 16.85, 41.13, 16.0, 41.45, 16.2, 41.9, 15.2, 41.95, 14.2, 42.47, 13.65, 43.05, 13.5, 43.6, 12.55, 44.1, 12.5, 44.95, 12.3, 45.45, 13.75, 45.65, 13.6, 45.1, 13.9, 44.8, 14.45, 45.3, 14.9, 44.9, 15.2, 44.1, 15.9, 43.7, 16.45, 43.5, 17.4, 43.0, 18.1, 42.65, 18.7, 42.4, 19.1, 42.1, 19.45, 41.85, 19.45, 41.3, 19.4, 40.9, 19.45, 40.45, 19.8, 40.05, 20.0, 39.85, 20.7, 38.95, 21.4, 38.35, 21.7, 38.25, 21.15, 37.9, 21.6, 37.2, 21.85, 36.8, 22.5, 36.4, 22.6, 36.75, 23.2, 36.45, 23.05, 36.7, 22.75, 37.55, 23.15, 37.35, 23.6, 37.95, 24.0, 37.65, 23.95, 38.2, 23.4, 38.45, 22.95, 38.85, 22.95, 39.35, 23.3, 39.15, 22.6, 40.0, 22.55, 40.5, 22.95, 40.63, 23.3, 40.25, 23.7, 39.95, 23.75, 40.2, 24.35, 40.15, 23.9, 40.35, 24.0, 40.75, 24.4, 40.93, 25.0, 40.95, 25.9, 40.85, 26.05, 40.75, 26.6, 40.6, 26.25, 40.3, 26.2, 40.0, 26.15, 39.5, 27.0, 39.55, 26.7, 39.3, 26.9, 38.95, 26.95, 38.65, 27.1, 38.45, 26.75, 38.35, 26.3, 38.32, 26.7, 38.2, 27.2, 37.9, 27.25, 37.35, 27.4, 37.03, 28.2, 37.03, 28.3, 36.8, 28.6, 36.75, 29.1, 36.65, 29.6, 36.2, 30.15, 36.3, 30.45, 36.45, 30.7, 36.88, 31.4, 36.75, 32.0, 36.55, 32.5, 36.1, 32.85, 36.02, 33.4, 36.15, 33.95, 36.3, 34.6, 36.78, 35.3, 36.6, 35.8, 36.75, 36.15, 36.6, 35.95, 36.25, 35.9, 36.05, 35.75, 35.5, 35.85, 34.9, 35.8, 34.45, 35.5, 33.9, 35.2, 33.25, 34.95, 32.8, 34.75, 32.05, 34.45, 31.5, 33.8, 31.13, 32.6, 31.05, 32.3, 31.27, 31.8, 31.52, 31.0, 31.6, 30.4, 31.47, 29.9, 31.2, 28.95, 30.85, 27.25, 31.35, 25.15, 31.57, 23.95, 32.08, 23.1, 32.6, 22.65, 32.77, 21.7, 32.9, 20.15, 32.3, 19.95, 31.3, 19.6, 30.6, 19.0, 30.3, 18.2, 30.7, 16.6, 31.2, 15.5, 31.8, 15.1, 32.35, 14.25, 32.65, 13.2, 32.9, 12.1, 32.93, 11.4, 33.2, 10.9, 33.75, 10.1, 33.9, 10.75, 34.75, 11.05, 35.5, 10.8, 35.8, 10.6, 36.4, 11.05, 37.05, 10.3, 36.85, 9.85, 37.3, 9.2, 37.2, 8.75, 36.95, 7.75, 36.9, 6.9, 36.9, 5.75, 36.8, 5.1, 36.75, 4, 36.9],
  black: [29.1, 41.22, 28.6, 41.35, 27.98, 41.88, 27.45, 42.5, 27.9, 42.85, 27.95, 43.2, 28.45, 43.36, 28.6, 43.75, 28.65, 44.17, 28.85, 44.6, 29.65, 45.2, 29.75, 45.6, 30.2, 45.85, 30.75, 46.45, 31.5, 46.65, 31.9, 46.55, 32.6, 46.05, 32.5, 45.35, 33.35, 45.2, 33.5, 44.6, 34.15, 44.5, 34.95, 44.85, 35.4, 45.0, 36.0, 45.0, 36.5, 45.2, 36.7, 45.15, 37.3, 44.9, 37.8, 44.7, 39.1, 44.1, 39.7, 43.6, 40.25, 43.3, 41.0, 43.0, 41.6, 42.6, 41.65, 42.15, 41.62, 41.62, 41.4, 41.4, 40.5, 41.03, 39.73, 41.0, 38.4, 40.92, 37.88, 40.98, 37.3, 41.13, 36.33, 41.29, 35.9, 41.72, 35.15, 42.03, 33.75, 41.98, 32.4, 41.75, 31.8, 41.45, 31.4, 41.28, 30.6, 41.15, 29.6, 41.18],
  azov: [34.85, 46.17, 35.5, 46.5, 36.8, 46.75, 37.55, 47.1, 38.9, 47.25, 39.3, 47.1, 38.25, 46.7, 37.95, 46.05, 37.6, 45.65, 37.3, 45.35, 36.6, 45.4, 35.4, 45.35, 35.05, 45.6],
  marmara: [26.67, 40.41, 27.5, 40.97, 28.0, 41.0, 28.65, 40.97, 28.98, 41.0, 29.3, 40.82, 29.92, 40.76, 29.4, 40.7, 29.1, 40.42, 28.88, 40.37, 28.2, 40.4, 27.97, 40.35, 27.8, 40.4, 27.3, 40.4, 26.68, 40.35],
  red: [32.55, 29.95, 32.7, 29.3, 33.55, 27.6, 33.95, 26.75, 34.3, 26.1, 34.9, 25.07, 35.5, 23.9, 35.7, 23.0, 36.6, 22.0, 37.1, 21.0, 39.4, 21.0, 39.1, 21.5, 39.0, 22.8, 38.05, 24.1, 37.25, 25.05, 36.45, 26.2, 35.7, 27.35, 34.85, 28.05, 34.95, 29.4, 35.0, 29.53, 34.9, 29.5, 34.65, 29.05, 34.5, 28.5, 34.25, 27.73, 33.6, 28.25, 32.9, 29.4],
  gulf: [48.0, 30.05, 48.9, 30.4, 50.1, 30.1, 50.8, 28.95, 51.4, 27.9, 52.5, 27.4, 53.7, 26.7, 54.8, 26.5, 55.6, 26.8, 56.3, 27.2, 57.0, 27.0, 57.8, 25.6, 59, 25.5, 59, 23.5, 58.0, 23.65, 56.75, 24.35, 56.35, 25.1, 56.35, 26.35, 56.0, 26.0, 55.3, 25.25, 54.4, 24.45, 53.0, 24.15, 51.6, 24.6, 51.6, 25.3, 51.2, 26.15, 50.8, 25.5, 50.8, 24.75, 50.2, 25.6, 50.1, 26.45, 49.6, 26.95, 48.8, 27.7, 48.45, 28.4, 47.95, 29.35],
  caspian: [47.9, 46.5, 47.4, 45.6, 47.6, 44.6, 47.5, 42.98, 48.3, 42.05, 48.9, 41.5, 49.9, 40.4, 49.45, 40.15, 49.0, 39.4, 48.85, 38.45, 49.1, 37.6, 49.45, 37.47, 50.3, 37.15, 51.5, 36.8, 53.0, 36.85, 54.0, 37.3, 53.9, 38.9, 53.2, 39.3, 53.0, 40.0, 52.75, 40.9, 52.4, 41.75, 52.6, 42.6, 51.3, 43.2, 51.2, 43.65, 50.3, 44.6, 51.3, 45.3, 53.0, 45.3, 53.2, 46.6, 52.0, 46.9, 49.5, 46.6],
};
const A1_ISLES = {
  sicily: [12.5, 37.95, 12.6, 38.1, 13.35, 38.18, 14.0, 38.03, 15.05, 38.12, 15.55, 38.22, 15.1, 37.5, 15.2, 37.05, 15.05, 36.72, 14.35, 36.82, 13.6, 37.15, 12.65, 37.6],
  sardinia: [8.4, 41.15, 9.2, 41.2, 9.65, 40.9, 9.6, 40.0, 9.55, 39.2, 9.1, 39.2, 8.6, 38.95, 8.42, 39.2, 8.42, 40.0, 8.2, 40.6, 8.22, 40.95],
  corsica: [9.4, 42.95, 9.52, 42.6, 9.47, 42.1, 9.2, 41.45, 8.82, 41.62, 8.65, 42.2, 8.68, 42.6, 9.0, 42.78],
  crete: [23.55, 35.6, 24.3, 35.52, 25.1, 35.33, 25.75, 35.25, 26.3, 35.28, 26.15, 35.02, 25.5, 34.97, 24.7, 34.97, 24.1, 35.18, 23.55, 35.3],
  cyprus: [32.3, 35.05, 32.95, 35.38, 33.7, 35.35, 34.55, 35.65, 34.0, 35.13, 33.9, 34.95, 33.0, 34.62, 32.42, 34.75],
  euboea: [23.15, 38.98, 23.6, 38.85, 24.25, 38.55, 24.6, 38.02, 24.4, 37.98, 23.82, 38.33, 23.3, 38.72],
};
const A1_DOTS_ISLE = [[28.0, 36.2, .32, .3], [26.25, 39.15, .4, .22], [26.0, 38.37, .16, .25], [26.75, 37.72, .25, .1], [25.25, 39.9, .2, .12], [19.85, 39.6, .1, .3], [14.4, 35.9, .1, .07], [25.45, 37.05, .14, .12], [25.15, 37.07, .1, .1], [24.85, 37.85, .1, .15], [25.15, 37.6, .1, .06], [25.43, 36.4, .07, .1], [24.42, 36.7, .12, .07], [22.98, 36.25, .07, .09], [27.15, 35.6, .07, .18], [27.15, 36.85, .2, .06]];
const A1_LAKES = [[42.3, 38.5, 42.9, 38.95, 43.6, 38.7, 43.2, 38.35, 42.5, 38.3], [45.3, 38.2, 45.9, 37.9, 45.7, 37.3, 45.2, 37.5], [33.3, 38.95, 33.6, 38.85, 33.45, 38.6, 33.25, 38.7]];
const A1_RIVERS = [
  [18.9, 46.6, 19.0, 45.6, 19.4, 45.2, 20.3, 44.85, 21.5, 44.75, 22.5, 44.6, 22.9, 44.0, 24.0, 43.7, 25.5, 43.65, 27.0, 44.05, 27.95, 44.4, 28.05, 45.0, 28.1, 45.4, 29.0, 45.35, 29.65, 45.2],
  [31.0, 30.1, 31.25, 29.0, 30.8, 27.6, 31.2, 27.2, 32.7, 26.15, 32.65, 25.7, 32.9, 24.1, 32.6, 22.9, 31.6, 21.5],
  [31.0, 30.1, 30.4, 31.45], [31.0, 30.1, 31.8, 31.5],
  [39.0, 39.6, 38.6, 38.5, 38.2, 37.2, 38.0, 36.4, 39.0, 35.95, 40.15, 35.3, 41.0, 34.45, 42.0, 34.1, 43.3, 33.4, 44.3, 32.5, 45.3, 31.6, 46.3, 31.0, 47.4, 30.95, 48.0, 30.4],
  [40.2, 38.1, 41.5, 37.4, 42.2, 37.3, 43.1, 36.35, 43.4, 35.4, 43.9, 34.5, 44.4, 33.35, 45.8, 32.5, 46.5, 31.7, 47.4, 30.95],
  [38.5, 39.6, 37.0, 39.7, 35.0, 39.0, 34.0, 39.6, 34.5, 40.8, 35.9, 41.7],
  [21.43, 42.0, 22.0, 41.4, 22.6, 40.6], [23.5, 42.3, 24.75, 42.15, 26.0, 41.9, 26.56, 41.68, 26.3, 41.2, 26.05, 40.75],
];
const A1_RIDGES = [
  [[6.5, 45.0, 8.0, 46.1, 10.0, 46.3, 12.5, 46.5], 10], [[8.5, 44.4, 10.5, 44.1, 12.5, 43.2, 14.0, 42.0, 15.5, 40.6, 16.2, 39.2], 9],
  [[14.8, 45.3, 16.5, 44.0, 18.0, 43.2, 19.5, 42.5], 10], [[22.5, 43.5, 24.0, 42.95, 25.5, 42.8, 27.0, 42.7], 9], [[23.5, 41.75, 24.5, 41.65, 25.5, 41.55], 7],
  [[20.8, 40.5, 21.3, 39.8, 21.8, 39.0], 8], [[31.5, 41.0, 34.0, 41.2, 37.0, 40.6, 40.0, 40.5, 42.0, 41.0], 9],
  [[29.5, 37.2, 31.5, 37.3, 33.5, 37.0, 35.5, 37.6, 38.0, 38.0, 41.0, 38.45, 43.5, 38.0], 11], [[45.0, 36.5, 46.5, 35.0, 48.0, 33.5, 50.0, 31.5, 52.0, 29.8, 54.5, 28.5], 11],
  [[38.5, 44.0, 41.0, 43.3, 43.5, 42.8, 46.0, 42.0, 48.5, 41.3], 11], [[35.9, 34.6, 36.3, 33.6], 7], [[5.5, 36.0, 7.5, 35.8, 9.0, 35.2], 8],
  [[35.5, 28.0, 37.0, 26.0, 38.5, 24.0, 39.6, 22.8], 9], [[49.0, 36.75, 51.0, 36.1, 53.5, 36.45], 8],
];
// İmparatorluk 1876 (Rumeli + Anadolu + Arap vilayetleri; Trablusgarp ayrı; Mısır ve Tunus imtiyazlı)
const A1_CORE = [15.75, 45.2, 17.0, 45.15, 19.0, 44.9, 20.45, 44.8, 22.6, 44.6, 22.9, 44.0, 24.0, 43.7, 25.5, 43.65, 27.25, 44.1, 27.95, 44.7, 28.1, 45.35, 29.0, 45.35, 29.7, 45.2, 30.6, 44.0, 35.0, 42.6, 39.0, 41.8, 41.4, 41.95, 42.5, 41.45, 43.4, 41.15, 43.7, 40.6, 44.3, 39.65, 44.45, 38.9, 44.25, 38.05, 44.8, 37.15, 45.45, 36.3, 45.9, 35.7, 45.6, 34.6, 46.2, 33.2, 47.4, 32.4, 47.7, 31.4, 48.55, 29.95, 49.4, 28.6, 50.4, 26.8, 51.7, 26.1, 51.7, 24.6, 50.6, 24.3, 49.2, 24.9, 48.0, 26.6, 46.8, 28.6, 46.0, 29.2, 44.0, 29.6, 42.0, 31.0, 39.3, 30.2, 38.2, 28.6, 39.2, 26.0, 40.2, 24.0, 40.8, 22.0, 38.6, 22.0, 36.8, 24.9, 35.2, 27.4, 34.7, 28.4, 34.95, 29.5, 34.25, 31.3, 33.9, 32.0, 33.6, 34.2, 32.0, 34.4, 32.0, 35.8, 29.5, 35.8, 27.6, 35.6, 26.6, 34.75, 23.3, 34.75, 23.3, 35.8, 24.5, 35.75, 26.4, 36.6, 26.0, 38.0, 25.2, 39.2, 24.9, 39.9, 23.8, 39.2, 22.6, 38.88, 22.0, 39.0, 21.4, 39.05, 21.0, 39.05, 20.4, 38.95, 20.1, 39.45, 19.3, 40.4, 19.1, 41.5, 19.2, 41.93, 19.1, 42.1, 18.45, 42.55, 18.35, 42.7, 17.6, 43.05, 17.0, 43.55, 16.4, 44.1, 15.9, 44.7];
const A1_LIBYA = [11.55, 33.15, 10.2, 30.5, 9.6, 26.5, 10.0, 22.0, 25.0, 22.0, 25.15, 31.6, 25.0, 33.0, 11.6, 34.0];
const A1_EGYPT = [25.15, 31.6, 25.0, 22.0, 38.6, 22.0, 36.8, 24.9, 35.2, 27.4, 34.7, 28.4, 34.95, 29.5, 34.25, 31.3, 33.9, 32.0, 25.0, 32.5];
const A1_TUNIS = [8.6, 37.6, 8.6, 36.95, 8.3, 35.0, 7.8, 33.5, 9.5, 30.3, 10.2, 30.5, 11.55, 33.15, 12.0, 34.0, 11.5, 37.6];
// 1878–1882 kayıpları
const A1_LOST = {
  L1: [14.5, 46.8, 31.2, 46.8, 31.2, 42.0, 28.05, 41.98, 27.3, 41.92, 26.6, 41.95, 26.1, 41.75, 25.4, 41.55, 24.6, 41.45, 24.0, 41.55, 23.2, 41.8, 22.7, 42.28, 22.35, 42.35, 21.9, 42.6, 21.5, 42.85, 20.8, 43.1, 20.4, 43.3, 19.6, 43.3, 19.75, 42.55, 19.4, 42.15, 19.2, 41.85, 18.5, 41.8, 14.5, 41.8],
  L2: [20.6, 38.8, 23.6, 38.8, 23.6, 39.95, 22.6, 40.0, 22.0, 39.85, 21.5, 39.4, 21.0, 39.15],
  L3: [41.2, 42.3, 44.0, 41.4, 43.9, 40.3, 43.1, 40.25, 42.5, 40.45, 41.9, 40.75, 41.5, 41.25, 41.3, 41.5],
};
// silme yönleri (ekran): başlangıç noktası (lon, lat), yön, uzunluk (px)
const A1_SWEEP = {
  L1: { o: [14.5, 46.6], d: [1, .42], len: 760 }, L2: { o: [20.4, 40.2], d: [1, .25], len: 120 }, L3: { o: [44.2, 42.2], d: [-1, .5], len: 150 },
  L4: { o: [31.3, 35.2], d: [1, 0], len: 130 }, tunis: { o: [7.5, 37.6], d: [.3, 1], len: 300 }, egypt: { o: [24.5, 32.6], d: [.75, 1], len: 520 },
};
let A1_GEO = null;
function a1_geo() {
  if (A1_GEO) return A1_GEO;
  const G = {};
  const sp = f => SP(a1_pts(f), true, .75);
  G.sea = new Path2D(); G.seaList = [];
  for (const k in A1_SEAS) { const p = sp(A1_SEAS[k]); G.sea.addPath(p); G.seaList.push(p); }
  G.isles = [];
  for (const k in A1_ISLES) { const p = sp(A1_ISLES[k]); G.sea.addPath(p); G.isles.push(p); }
  for (const [lo, la, rx, ry] of A1_DOTS_ISLE) { const [x, y] = a1_p(lo, la), p = a1_ell(x, y, rx * A1M.kx, ry * A1M.ky); G.sea.addPath(p); G.isles.push(p); }
  G.lakes = A1_LAKES.map(sp); for (const p of G.lakes) G.sea.addPath(p);
  G.core = PL(a1_pts(A1_CORE)); G.libya = PL(a1_pts(A1_LIBYA)); G.egypt = PL(a1_pts(A1_EGYPT)); G.tunis = PL(a1_pts(A1_TUNIS));
  for (const k in A1_LOST) G[k] = PL(a1_pts(A1_LOST[k]));
  { const [x, y] = a1_p(33.3, 35.1); G.L4 = a1_ell(x, y, 1.7 * A1M.kx, .95 * A1M.ky); }
  G.content = a1_rect(A1M.cx0, A1M.cy0, A1M.cx1, A1M.cy1);
  // 1900 sınırı içinde mi (okul noktaları için)
  const tc = makeCanvas(4, 4).getContext('2d');
  G.inEmpire1900 = (x, y) => (tc.isPointInPath(G.core, x, y) || tc.isPointInPath(G.libya, x, y)) && !['L1', 'L2', 'L3', 'L4'].some(k => tc.isPointInPath(G[k], x, y)) && !tc.isPointInPath(G.sea, x, y, 'evenodd');
  A1_GEO = G; return G;
}
// alt katman: kâğıt + kara toprağı yarım tonu (durağan)
function a1_mapUnder(key = 'a1-map-under') {
  return a1_cache(key, g => {
    paperBG(g);
    const G = a1_geo();
    halftone(g, 'sepia', G.content, .1, { cell: 10, ang: 15 });
  });
}
// üst katman: denizler (kâğıt + kıyıya koşut dalga çizgileri), kıyı, ırmaklar, dağ taraması, çerçeve, kartuş
function a1_mapTop(key = 'a1-map-top', o = {}) {
  return a1_cache(key, g => {
    const G = a1_geo();
    g.save(); g.clip(G.content);
    g.fillStyle = P.paper; g.fill(G.sea, 'evenodd');
    g.save(); g.clip(G.sea, 'evenodd');
    for (let k = 3; k >= 1; k--) {
      for (const p of [...G.seaList, ...G.isles.slice(0, 6)]) inkStroke(g, p, 2 * k * 10 + 1.3, { a: .34 - k * .06 });
      for (const p of [...G.seaList, ...G.isles.slice(0, 6)]) inkStroke(g, p, 2 * k * 10 - 1.3, { col: P.paper });
    }
    if (o.sea) plate(g, o.sea, G.content, { a: o.seaA ?? .32 });
    g.restore();
    // ırmaklar
    for (const r of A1_RIVERS) inkStroke(g, SP(a1_pts(r), false, .8), 1.7, { a: .85 });
    // dağlar
    for (const [f, L] of A1_RIDGES) ridge(g, a1_pts(f), L, px => px * .75, f.length);
    // kıyı ve adalar
    for (const p of G.seaList) inkStroke(g, p, 2.6);
    for (const p of G.isles) inkStroke(g, p, 2.2);
    for (const p of G.lakes) inkStroke(g, p, 1.8);
    // şehirler: is kare; İstanbul çift kare
    for (const [lo, la, big] of [[28.97, 41.01, 1], [22.94, 40.64], [26.56, 41.68], [27.14, 38.42], [36.3, 33.51], [37.16, 36.2], [44.4, 33.33], [13.19, 32.89], [31.24, 30.04], [39.6, 24.47], [41.27, 39.9], [21.33, 41.03], [35.22, 31.78], [32.86, 39.93]]) {
      const [x, y] = a1_p(lo, la), r = big ? 7 : 4.2;
      knock(g, a1_rect(x - r - 2, y - r - 2, x + r + 2, y + r + 2)); inkFill(g, a1_rect(x - r, y - r, x + r, y + r));
      if (big) { knock(g, a1_rect(x - 3, y - 3, x + 3, y + 3)); }
      scriptLine(g, x - 8, y - 9, 30 + (lo * 7) % 18, 5, Math.round(lo * 10), { w: 1.3, a: .8 });
    }
    // bölge adları: soyut Osmanlıca iz (seyrek, açık)
    for (const [lo, la, L, h, sd] of [[36.5, 39.2, 150, 12, 601], [42.5, 27.6, 130, 11, 602], [24.6, 42.9, 110, 10, 603], [18.5, 28.5, 120, 10, 604], [41.5, 34.8, 90, 9, 605], [30, 24.5, 100, 9, 606]]) {
      const [x, y] = a1_p(lo, la); scriptLine(g, x + L / 2, y, L, h, sd, { w: 2, a: .55 });
    }
    // deniz adları
    for (const [lo, la, L, sd] of [[18.5, 34.3, 120, 611], [34.0, 43.3, 100, 612], [36.0, 33.0, 0, 0], [50.5, 42.3, 60, 613]]) { if (!L) continue; const [x, y] = a1_p(lo, la); scriptLine(g, x + L / 2, y, L, 8, sd, { w: 1.4, a: .45 }); }
    // pusula gülü (sol üst)
    { const [cx, cy] = [210, 205]; for (let k = 0; k < 8; k++) { const a = k * PI / 4 - PI / 2, L = k % 2 ? 22 : 42; const p = PL([[cx, cy], [cx + Math.cos(a - .18) * L * .35, cy + Math.sin(a - .18) * L * .35], [cx + Math.cos(a) * L, cy + Math.sin(a) * L], [cx + Math.cos(a + .18) * L * .35, cy + Math.sin(a + .18) * L * .35]]); knock(g, p); if (k % 2 === 0) plate(g, 'sepia', p, { a: .8 }); inkStroke(g, p, 1.6); }
      inkStroke(g, a1_ell(cx, cy, 30, 30), 1.4); }
    // kartuş (sağ üst)
    { const x0 = 1480, y0 = 112, x1 = 1782, y1 = 232; plate(g, 'ink', a1_rect(x0 + 7, y0 + 8, x1 + 7, y1 + 8), { a: .3 }); knock(g, a1_rect(x0, y0, x1, y1));
      plate(g, 'sepia', a1_ring(x0, y0, x1, y1, 10), { a: .55 }); inkStroke(g, a1_rect(x0, y0, x1, y1), 2.4); inkStroke(g, a1_rect(x0 + 10, y0 + 10, x1 - 10, y1 - 10), 1.2);
      scriptLine(g, x1 - 30, y0 + 58, 240, 16, 621, { w: 2.6 }); scriptLine(g, x1 - 60, y0 + 92, 180, 9, 622, { w: 1.6 }); }
    g.restore();
    // pafta çerçevesi
    const sheet = a1_rect(A1M.sx0, A1M.sy0, A1M.sx1, A1M.sy1);
    const band = new Path2D(); band.addPath(sheet); band.addPath(G.content);
    g.save(); g.fillStyle = P.paperD; g.fill(band, 'evenodd'); g.restore();
    plate(g, 'sepia', band, { a: .12 });
    inkStroke(g, G.content, 2.6); inkStroke(g, a1_rect(A1M.cx0 - 10, A1M.cy0 - 10, A1M.cx1 + 10, A1M.cy1 + 10), 1.2);
    for (let x = A1M.cx0 - 10; x < A1M.cx1 + 10; x += 40) { inkFill(g, a1_rect(x, A1M.cy0 - 10, Math.min(x + 20, A1M.cx1 + 10), A1M.cy0)); inkFill(g, a1_rect(x + 20, A1M.cy1, Math.min(x + 40, A1M.cx1 + 10), A1M.cy1 + 10)); }
    for (let y = A1M.cy0; y < A1M.cy1; y += 40) { inkFill(g, a1_rect(A1M.cx0 - 10, y + 20, A1M.cx0, Math.min(y + 40, A1M.cy1))); inkFill(g, a1_rect(A1M.cx1, y, A1M.cx1 + 10, Math.min(y + 20, A1M.cy1))); }
    // pafta dışı: koyu masa
    const out = new Path2D(); out.addPath(a1_rect(-40, -40, W + 40, H + 40)); out.addPath(sheet);
    g.save(); g.fillStyle = P.paper; g.fill(out, 'evenodd'); g.restore();
    g.save(); g.clip(out, 'evenodd'); plate(g, 'sepia', a1_rect(-40, -40, W + 40, H + 40), { n: 2 }); plate(g, 'ink', a1_rect(-40, -40, W + 40, H + 40), { a: .35 });
    plate(g, 'ink', a1_rect(A1M.sx0 + 10, A1M.sy0 + 12, A1M.sx1 + 12, A1M.sy1 + 14), { a: .45 }); g.restore();
    inkStroke(g, PL(rough([[A1M.sx0, A1M.sy0], [A1M.sx1, A1M.sy0], [A1M.sx1, A1M.sy1], [A1M.sx0, A1M.sy1]], 1.5, 4)), 3);
    for (const [x, y] of [[A1M.sx0 + 18, A1M.sy0 + 18], [A1M.sx1 - 18, A1M.sy0 + 18], [A1M.sx0 + 18, A1M.sy1 - 18], [A1M.sx1 - 18, A1M.sy1 - 18]]) { const p = a1_ell(x, y, 8, 8); knock(g, p); plate(g, 'red', p); inkStroke(g, p, 2.2); }
  });
}
// imparatorluk dolgusu (her karede; kayıplar süpürülerek silinir). st: {L1..L4, egypt, tunis: 0..1 silinme}
let A1_FC = null;
function a1_sweepPoly(k, dist) {
  const s = A1_SWEEP[k], [ox, oy] = a1_p(s.o[0], s.o[1]), n0 = Math.hypot(s.d[0], s.d[1]), dx = s.d[0] / n0, dy = s.d[1] / n0, nx = -dy, ny = dx;
  const r = rng(k.length * 31 + 7), pts = [];
  for (let u = -1400; u <= 1400; u += 34) { const j = (r() - .5) * 14; pts.push([ox + dx * (dist + j) + nx * u, oy + dy * (dist + j) + ny * u]); }
  pts.push([ox + dx * (dist - 3000) + nx * 1400, oy + dy * (dist - 3000) + ny * 1400], [ox + dx * (dist - 3000) - nx * 1400, oy + dy * (dist - 3000) - ny * 1400]);
  return PL(pts);
}
function a1_empireDraw(g, st) {
  const G = a1_geo();
  plate(g, 'sepia', G.core, { a: .62 }); plate(g, 'sepia', G.libya, { a: .62 });
  for (const k of ['egypt', 'tunis']) {
    if ((st[k] ?? 0) >= 1) continue;
    plate(g, 'sepia', G[k], { a: .26 });
    g.save(); g.clip(G[k]); const hp = new Path2D(); for (let x = -1200; x < 2400; x += 13) { hp.moveTo(x, 0); hp.lineTo(x + 1100, 1100); } inkStroke(g, hp, 1.2, { a: .35 }); g.restore();
  }
  for (const k of ['L1', 'L2', 'L3', 'L4', 'egypt', 'tunis']) {
    const p = st[k] ?? 0; if (p <= 0) continue;
    g.save(); g.clip(G[k]); g.globalCompositeOperation = 'destination-out'; g.fillStyle = '#000';
    g.fill(a1_sweepPoly(k, p * A1_SWEEP[k].len)); g.restore();
  }
}
function a1_empire(ctx, st) {
  if (!A1_FC) A1_FC = makeCanvas(DW, DH);
  const g = A1_FC.getContext('2d');
  g.setTransform(RS, 0, 0, RS, 0, 0); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; g.clearRect(-10, -10, W + 20, H + 20);
  a1_empireDraw(g, st);
  if (st.reveal != null && st.reveal < 1) { const [ix, iy] = a1_p(28.97, 41.01), r = E.out2(st.reveal) * 1500; g.save(); g.globalCompositeOperation = 'destination-in'; g.beginPath(); for (let k = 0; k <= 48; k++) { const a = k / 48 * TAU, rr = r * (1 + .05 * noise1(k * .7, 3)); k ? g.lineTo(ix + Math.cos(a) * rr, iy + Math.sin(a) * rr) : g.moveTo(ix + rr, iy); } g.closePath(); g.fill(); g.restore(); }
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; a1_img(ctx, A1_FC); ctx.restore();
}
// 1900 dolgusu + yeni sınır çizgisi (durağan)
function a1_empire1900(key = 'a1-fill-1900') {
  return a1_cache(key, g => {
    const G = a1_geo();
    a1_empireDraw(g, { L1: 1, L2: 1, L3: 1, L4: 1, egypt: 1, tunis: 1 });
    // sınır: çekirdeğin kayıplar dışında kalan kenarı + kayıpların çekirdek içindeki kenarı
    g.save(); const outL = new Path2D(); outL.addPath(a1_rect(-50, -50, W + 50, H + 50)); for (const k of ['L1', 'L2', 'L3', 'L4']) outL.addPath(G[k]);
    g.clip(outL, 'evenodd'); inkStroke(g, G.core, 2, { a: .75 }); g.restore();
    g.save(); g.clip(G.core); for (const k of ['L1', 'L2', 'L3']) inkStroke(g, G[k], 2, { a: .75 }); g.restore();
    inkStroke(g, G.libya, 2, { a: .75 });
  });
}
function a1_drawMap1900(ctx, o = {}) {
  a1_img(ctx, a1_mapUnder());
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; a1_img(ctx, a1_empire1900()); ctx.restore();
  if (o.mid) o.mid(ctx);
  a1_img(ctx, a1_mapTop(o.topKey || 'a1-map-top', o.top || {}));
}

// Borç senedi (tahvil): süslü çift çerçeve, madalyon, kupon şeridi; sp: kırmızı damga (0..)
function a1_bond(ctx, x, y, w, h, rot, seed, sp = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  const x0 = -w / 2, y0 = -h / 2, x1 = w / 2, y1 = h / 2;
  plate(ctx, 'ink', a1_rect(x0 + 7, y0 + 9, x1 + 7, y1 + 9), { a: .32 });
  const r = PL(rough([[x0, y0], [x1, y0], [x1, y1], [x0, y1]], 1.1, seed));
  knock(ctx, r); plate(ctx, 'sepia', r, { a: .1 });
  plate(ctx, 'sepia', a1_ring(x0 + 9, y0 + 9, x1 - 9, y1 - 9, 11), { a: .55 });
  inkStroke(ctx, a1_rect(x0 + 9, y0 + 9, x1 - 9, y1 - 9), 1.6); inkStroke(ctx, a1_rect(x0 + 20, y0 + 20, x1 - 20, y1 - 20), 1.1);
  for (const [cx, cy] of [[x0 + 14.5, y0 + 14.5], [x1 - 14.5, y0 + 14.5], [x0 + 14.5, y1 - 14.5], [x1 - 14.5, y1 - 14.5]]) { const c = a1_ell(cx, cy, 7, 7); knock(ctx, c); inkStroke(ctx, c, 1.4); }
  scriptLine(ctx, x1 - 34, y0 + 50, w - 68, 10, seed * 3, { w: 2.2 });
  const my = y0 + h * .42, mr = w * .17;
  const med = a1_ell(0, my, mr, mr * .86); plate(ctx, 'sepia', med, { a: .5 }); inkStroke(ctx, med, 1.6);
  for (let k = 0; k < 16; k++) { const a = k / 16 * TAU; inkStroke(ctx, PL([[Math.cos(a) * mr * .35, my + Math.sin(a) * mr * .3], [Math.cos(a) * mr * .8, my + Math.sin(a) * mr * .7]], false), 1.1, { a: .7 }); }
  knock(ctx, a1_ell(0, my, mr * .3, mr * .26)); inkStroke(ctx, a1_ell(0, my, mr * .3, mr * .26), 1.2);
  for (let i = 0; i < 3; i++) scriptLine(ctx, x1 - 36, my + mr + 26 + i * 16, (w - 72) * (i === 2 ? .55 : .9), 6, seed * 7 + i, { w: 1.3, a: .85 });
  const cy = y1 - 56; ctx.save(); ctx.setLineDash([4, 4]); inkStroke(ctx, PL([[x0 + 22, cy - 8], [x1 - 22, cy - 8]], false), 1.1); ctx.restore();
  for (let i = 0; i < 4; i++) { const cw = (w - 44) / 4, cx0 = x0 + 22 + i * cw; inkStroke(ctx, a1_rect(cx0 + 3, cy, cx0 + cw - 3, y1 - 26), 1.1); scriptLine(ctx, cx0 + cw - 9, cy + 16, cw - 18, 4, seed + i, { w: 1, a: .7 }); }
  if (sp > 0) {
    ctx.save(); ctx.translate(w * .06, h * .1); ctx.rotate(-.32); ctx.scale(sp, sp);
    const sw = w * .74, sh = h * .2, b = PL(rough([[-sw / 2, -sh / 2], [sw / 2, -sh / 2], [sw / 2, sh / 2], [-sw / 2, sh / 2]], 1.4, seed + 9));
    inkStroke(ctx, b, 4.2, { col: P.red, mode: 'multiply', a: .92 }); inkStroke(ctx, a1_rect(-sw / 2 + 7, -sh / 2 + 7, sw / 2 - 7, sh / 2 - 7), 1.6, { col: P.red, mode: 'multiply', a: .85 });
    ctx.save(); ctx.globalCompositeOperation = 'multiply'; scriptLine(ctx, sw / 2 - 18, 6, sw - 36, sh * .3, seed + 13, { w: 3.4, col: P.red }); ctx.restore();
    ctx.restore();
  }
  inkStroke(ctx, r, 2.2);
  ctx.restore();
}

// ═══════════ B01a · İmparatorluk haritası, 1876: borç ve toprak kaybı ═══════════
shot(S('B01'), (ctx, st) => {
  setReg(101);
  paperBG(ctx);
  const t = st.t, lt = st.lt;
  const Tb = a1_W('B01', 'borç'), Tt = a1_W('B01', 'toprak'), Td = a1_W('B01', 'devraldı');
  const c = { x: kf(t, [[Tt - .5, 960], [Td + 1, 912]]), y: kf(t, [[Tt - .5, 540], [Td + 1, 508]]), z: kf(t, [[st.t - st.lt, 1], [Tt - .5, 1.025, E.out2], [Td + 1, 1.07]]) };
  ctx.save(); cam(ctx, c, 1);
  a1_img(ctx, a1_mapUnder());
  const w = (a, b) => E.io2(clamp((t - a) / (b - a)));
  a1_empire(ctx, { reveal: clamp((t - S('B01') + .3) / (Tb - S('B01') + .1)), L1: w(Tt, Tt + 1.35), L3: w(Tt + .7, Tt + 1.1), L4: w(Tt + .9, Tt + 1.25), L2: w(Tt + 1.35, Tt + 1.7), tunis: w(Tt + 1.6, Tt + 2.0), egypt: w(Tt + 1.8, Tt + 2.4) });
  // 1876 sınırı: silinen toprağın üstünde kesik çizgi olarak kalır
  { const G = a1_geo(); ctx.save(); ctx.setLineDash([7, 6]); for (const p of [G.core, G.libya, G.egypt, G.tunis]) inkStroke(ctx, p, 1.6, { a: .6 }); ctx.restore(); }
  a1_img(ctx, a1_mapTop());
  // kayıp yılları (izleyici katmanı, harita üstünde küçük damga)
  for (const [s, lo, la, tt] of [['1878', 24.3, 43.6, Tt + 1.0], ['1881', 6.9, 34.3, Tt + 1.9], ['1882', 28.6, 26.8, Tt + 2.3]]) { const [x, y] = a1_p(lo, la); stamp(ctx, s, x, y, t - tt, 9, { size: 40, typing: .3, bg: P.paperD }); }
  // borç senetleri: üç tahvil düşer, kırmızı damga yer
  for (let i = 0; i < 3; i++) {
    const t0 = Tb + i * .3, u = clamp((t - t0) / .22); if (u <= 0) continue;
    const e = E.out3(u), dy = (1 - e) * -70 + settle(t, t0 + .22, 6, 3, 9);
    ctx.save(); ctx.globalAlpha = clamp(u * 3);
    a1_bond(ctx, 1500 + i * 95, 720 + i * 52 + dy, 250, 330, -.16 + i * .13, 31 + i * 5, a1_pop(t, t0 + .3));
    ctx.restore();
  }
  ctx.restore();
  chapterCard(ctx, 'I', 'SULTANIN OKULLARI', '1876 · CUMHURİYET\u2019E 47 YIL', lt - .25, 4.6);
}, { tr: { type: 'press', dur: .8 } });

// ═══════════ B01b · Meclis kapısı mühürlenir; gece Yıldız, tek pencere ═══════════
// Yıldız silueti (gece): tepe, köşkler, saat kulesi, servi; win: yanan pencere (0..1)
function a1_yildiz(ctx, o = {}) {
  const hill = SP([[880, 640], [1000, 590], [1180, 548], [1380, 500], [1560, 470], [1760, 488], [1960, 530], [2140, 560], [2140, 700], [880, 700]], true, .8);
  knock(ctx, hill);
  if (o.night) { plate(ctx, 'navy', hill, { a: .85, flat: true }); plate(ctx, 'ink', hill, { a: .5, flat: true }); } else { plate(ctx, 'sepia', hill, { n: 2 }); plate(ctx, 'ink', hill, { a: .62 }); }
  const blk = new Path2D();
  for (const [x, y, w, h, rf] of [[1400, 470, 210, 58, 16], [1615, 462, 120, 52, 14], [1290, 494, 96, 40, 12], [1745, 476, 150, 46, 12], [1180, 520, 80, 30, 10]]) {
    blk.moveTo(x, y); blk.lineTo(x + w, y); blk.lineTo(x + w, y - h); blk.lineTo(x + w - 8, y - h - rf); blk.lineTo(x + 8, y - h - rf); blk.lineTo(x, y - h); blk.closePath();
  }
  // saat kulesi ve kubbe
  blk.moveTo(1572, 470); blk.lineTo(1572, 352); blk.lineTo(1584, 330); blk.lineTo(1596, 352); blk.lineTo(1596, 470); blk.closePath();
  blk.moveTo(1500, 412); blk.quadraticCurveTo(1530, 372, 1560, 412); blk.closePath();
  inkFill(ctx, blk);
  // pencere sıraları (sönük, kazıma)
  for (const [x, y, n, gap] of [[1414, 440, 9, 22], [1628, 434, 5, 21], [1756, 452, 6, 22], [1300, 474, 4, 20]]) for (let i = 0; i < n; i++) cut(ctx, PL([[x + i * gap, y], [x + i * gap, y + 9]], false), 2.2, { a: .22 });
  // saat kadranı
  cut(ctx, a1_ell(1584, 372, 6, 6), 1.6, { a: .45 });
  // serviler
  const cy = new Path2D(); for (const [x, y, h] of [[1360, 500, 70], [1380, 498, 58], [1880, 488, 76], [1905, 492, 60], [1120, 548, 54], [1700, 470, 44]]) { cy.moveTo(x, y); cy.quadraticCurveTo(x - 9, y - h * .5, x, y - h); cy.quadraticCurveTo(x + 9, y - h * .5, x, y); }
  inkFill(ctx, cy);
}
// nöbetçi: damga siluet (is), kırmızı fes, süngülü tüfek; ph: nefes evresi
function a1_guard(ctx, x, y, s, ph = 0, walk = false) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const st = walk ? (ph ? 4 : -4) : 0, by = walk ? -Math.abs(st) * .25 : -ph * .3;
  const b = new Path2D();
  b.moveTo(-4.5, -84 + by); b.quadraticCurveTo(-11, -83 + by, -12.5, -76 + by); b.lineTo(-14, -44 + by); b.lineTo(-15.5, -26 + by); b.lineTo(-8, -24 + by);
  b.lineTo(-7.5 - st, 0); b.lineTo(-1.5 - st, 0); b.lineTo(-.5, -24 + by); b.lineTo(1.5, -24 + by); b.lineTo(3 + st, 0); b.lineTo(9 + st, 0); b.lineTo(8, -24 + by);
  b.lineTo(14.5, -27 + by); b.lineTo(13, -46 + by); b.lineTo(12, -76 + by); b.quadraticCurveTo(10.5, -83 + by, 4.5, -84 + by); b.closePath();
  b.ellipse(0, -91 + by, 5.6, 6.8, 0, 0, TAU);
  inkFill(ctx, b);
  const fes = PL([[-5, -95.5 + by], [5.2, -95.5 + by], [4.2, -104.5 + by], [-4, -104.5 + by]]); knock(ctx, fes); plate(ctx, 'red', fes); inkStroke(ctx, fes, .7);
  inkStroke(ctx, PL([[15, -24 + by], [17.5, -96 + by]], false), 2.6); inkStroke(ctx, PL([[17.5, -96 + by], [18.2, -118 + by]], false), .9);
  cut(ctx, PL([[-11, -70 + by], [-12, -46 + by]], false), .6, { a: .4 }); cut(ctx, PL([[-2, -80 + by], [-2, -30 + by]], false), .5, { a: .35 });
  ctx.restore();
}
function a1_door(ctx, o = {}) {
  // taş cephe: ay ışığının aydınlattığı kâğıt bölgesi (açık değer); kapı kanatları düz lacivert + is
  const nv = (p, a) => plate(ctx, 'navy', p, { a, flat: true });
  const fac = PL([[-120, -20], [900, -20], [900, 1100], [-120, 1100]]);
  knock(ctx, fac); nv(fac, .14);
  nv(PL([[846, -20], [900, -20], [900, 1100], [846, 1100]]), .5);
  const r = rng(77);
  for (let y = 40; y < 1000; y += 56) { inkStroke(ctx, PL([[-120, y], [900, y]], false), 1.3, { a: .45 }); for (let x = -120 + ((y / 56) % 2) * 60; x < 900; x += 120) inkStroke(ctx, PL([[x + r() * 6, y], [x + r() * 6, y + 56]], false), 1.2, { a: .35 }); }
  for (const x of [70, 790]) { const col = a1_rect(x - 46, 120, x + 46, 1000); knock(ctx, col); nv(col, .08); nv(a1_rect(x + 10, 120, x + 46, 1000), .3); inkStroke(ctx, col, 3); for (const yy of [140, 980]) { const cap = a1_rect(x - 60, yy - 18, x + 60, yy + 18); knock(ctx, cap); nv(cap, .2); inkStroke(ctx, cap, 2.6); } }
  const archO = new Path2D(); archO.moveTo(140, 1000); archO.lineTo(140, 470); archO.arc(430, 470, 290, PI, 0); archO.lineTo(720, 1000); archO.closePath();
  knock(ctx, archO); nv(archO, .3); inkStroke(ctx, archO, 3.4);
  for (let k = 0; k < 13; k++) { const a = PI + k / 12 * PI; inkStroke(ctx, PL([[430 + Math.cos(a) * 254, 470 + Math.sin(a) * 254], [430 + Math.cos(a) * 290, 470 + Math.sin(a) * 290]], false), 2, { a: .7 }); }
  const kit = a1_rect(250, 92, 610, 160); knock(ctx, kit); inkStroke(ctx, kit, 2.4); inkStroke(ctx, a1_rect(258, 100, 602, 152), 1); scriptLine(ctx, 590, 136, 320, 15, 88, { w: 2.6 });
  const leaf = new Path2D(); leaf.moveTo(176, 1000); leaf.lineTo(176, 470); leaf.arc(430, 470, 254, PI, 0); leaf.lineTo(684, 1000); leaf.closePath();
  knock(ctx, leaf); nv(leaf, .85); plate(ctx, 'ink', leaf, { a: .3, flat: true });
  ctx.save(); ctx.clip(leaf);
  for (const [x0, x1] of [[200, 410], [450, 660]]) for (const [y0, y1] of [[330, 600], [640, 960]]) { const pnl = a1_rect(x0, y0, x1, y1); cut(ctx, pnl, 2.2, { a: .38 }); inkStroke(ctx, a1_rect(x0 + 8, y0 + 8, x1 - 8, y1 - 8), 2, { a: .8 }); }
  for (let y = 250; y < 1000; y += 46) for (const x of [196, 404, 456, 664]) { inkFill(ctx, a1_ell(x, y, 4.5, 4.5)); cut(ctx, a1_ell(x - 1.2, y - 1.4, 1.6, 1.6), 1.2, { a: .5 }); }
  ctx.restore();
  inkStroke(ctx, leaf, 3); inkStroke(ctx, PL([[430, 216], [430, 1000]], false), 3.4);
  for (const x of [400, 460]) { inkStroke(ctx, a1_ell(x, 650, 16, 18), 5); cut(ctx, a1_ell(x, 650, 16, 18), 1.4, { a: .45 }); inkFill(ctx, a1_ell(x, 628, 7, 7)); }
  for (let i = 0; i < 3; i++) { const st = a1_rect(-120 - i * 10, 1000 + i * 26, 900 + i * 10, 1026 + i * 26); knock(ctx, st); nv(st, .14 + i * .1); inkStroke(ctx, PL([[-130, 1000 + i * 26], [910, 1000 + i * 26]], false), 2.6); }
}
// zincir + asma kilit (pc: 0..1 iniş; sw: kilit salınımı)
function a1_chainLock(ctx, pc, sw) {
  if (pc <= 0) return;
  const dy = (1 - E.out3(pc)) * -160;
  ctx.save(); ctx.translate(0, dy);
  // zincir halkaları: iki halkadan sarkan katener
  const pts = []; for (let i = 0; i <= 18; i++) { const u = i / 18, x = lerp(400, 460, u), y = 666 + Math.sin(u * PI) * 46; pts.push([x - 34 * Math.sin(u * PI) * (u < .5 ? 1 : -1) * 0, y]); }
  const lx = 430, ly = 712;
  for (let i = 0; i < 9; i++) {
    for (const side of [-1, 1]) { const u = i / 9, x = lx + side * (1 - u) * 30, y = ly - (1 - u) * 44 * (1 - u * .3) - 6 * Math.sin(u * PI); const lk = a1_ell(x, y, 7, 4.5, side * .9 + (i % 2) * 1.2); inkStroke(ctx, lk, 3.4); cut(ctx, lk, 1, { a: .5 }); }
  }
  // kilit
  ctx.save(); ctx.translate(lx, ly); ctx.rotate(sw);
  const shk = new Path2D(); shk.moveTo(-14, 26); shk.lineTo(-14, 10); shk.arc(0, 10, 14, PI, 0); shk.lineTo(14, 26);
  inkStroke(ctx, shk, 6); cut(ctx, shk, 1.4, { a: .5 });
  const body = PL(rough([[-26, 24], [26, 24], [28, 78], [-28, 78]], .8, 5)); knock(ctx, body); inkFill(ctx, body);
  cut(ctx, PL([[-20, 34], [-20, 70]], false), 2, { a: .55 }); inkStroke(ctx, a1_ell(0, 50, 4, 4), 2, { col: P.paper, a: .7 }); cut(ctx, PL([[0, 52], [0, 62]], false), 2.2, { a: .7 });
  ctx.restore(); ctx.restore();
}
// kâğıt şerit + kırmızı mühür (sp: basılma ölçeği)
function a1_seal(ctx, x, y, sp) {
  if (sp <= 0) return;
  ctx.save(); ctx.translate(x, y);
  const strip = PL(rough([[-150, -30], [150, 10], [146, 46], [-154, 6]], 1.2, 12));
  plate(ctx, 'ink', PL([[-144, -22], [156, 18], [152, 54], [-148, 14]]), { a: .35 });
  knock(ctx, strip); scriptLine(ctx, 130, 22, 90, 7, 41, { w: 1.4 }); scriptLine(ctx, -50, 8, 90, 7, 42, { w: 1.4 }); inkStroke(ctx, strip, 2.2);
  ctx.scale(sp, sp);
  const wax = SP(rough([[-44, -6], [-30, -38], [4, -46], [36, -30], [46, 4], [32, 38], [-2, 46], [-36, 32]], 3, 7), true, .9);
  knock(ctx, wax); plate(ctx, 'red', wax); plate(ctx, 'red', a1_ell(8, 8, 30, 30), { a: .5 });
  inkStroke(ctx, a1_ell(4, 2, 28, 28), 2.2, { a: .8 }); inkStroke(ctx, a1_ell(4, 2, 21, 21), 1.2, { a: .7 });
  scriptLine(ctx, 20, 6, 32, 7, 43, { w: 2 });
  cut(ctx, SP([[-30, -20], [-14, -32], [6, -36]], false), 2.4, { a: .55 });
  inkStroke(ctx, wax, 2.4);
  ctx.restore();
}
shot(a1_W('B01', 'meclisi') - .45, (ctx, st) => {
  setReg(102);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const Tm = a1_W('B01', 'meclisi'), Tta = a1_W('B01', 'tatil'), Tet = a1_W('B01', 'etti'), Tu = a1_W('B01', 'ülkeyi'), Ty = a1_W('B01', 'yıldızdan'), Tk = a1_W('B01', 'tek');
  const pan = E.io2(clamp((t - Tu + .3) / 1.5));
  const [sx, sy] = shake(t, Tet, 7, 9);
  // kaydırma bitince kamera çekim sonuna dek yavaşça itmeye devam eder (çekimin son saniyeleri durmaz)
  const tail = clamp((t - (Tu + 1.2)) / Math.max(.5, st.end - (Tu + 1.2)));
  const c = { x: lerp(905, 1045, pan) + 30 * tail, y: 540, z: lerp(1.0 + .03 * ramp(t, Tm - .4, Tet, E.io2), 1.0, pan) + .03 * tail, sx, sy };
  // gök (durağan): koyu sepya + is, yarım ton, yıldızlar, hilal
  const sky = a1_cacheM('a1-b01b-sky', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220);
    knock(g, R); plate(g, 'navy', R, { a: .85, flat: true });
    const r = rng(9); for (let i = 0; i < 70; i++) { const x = -200 + r() * (W + 400), y = -100 + r() * 520, rr = .9 + r() * 1.8; knock(g, a1_ell(x, y, rr, rr), '#E9DEC4'); }
    const bite = new Path2D(); bite.rect(-300, -300, W + 600, H + 600); bite.arc(1497, 141, 33, 0, TAU);
    g.save(); g.clip(bite, 'evenodd'); knock(g, a1_ell(1480, 150, 38, 38), '#EDE3CB'); g.restore();
  });
  ctx.save(); cam(ctx, c, .3); a1_imgM(ctx, sky); ctx.restore();
  // uzak tepe: Yıldız ve kent ışıkları
  ctx.save(); cam(ctx, c, .65);
  a1_imgM(ctx, a1_cacheM('a1-b01b-hill', g => { g.translate(1500, 640); g.scale(1.18, 1.18); g.translate(-1500, -640); a1_yildiz(g, { night: true }); }));
  const hp = (x, y) => [1500 + (x - 1500) * 1.18, 640 + (y - 640) * 1.18];
  // kent pencereleri: "tek başına" sözünde birer birer söner
  const lights = [[1010, 600], [1072, 588], [1140, 574], [1215, 562], [1262, 548], [1688, 456], [1830, 470], [1938, 520]].map(([x, y]) => hp(x, y));
  lights.forEach(([x, y], i) => { const off = t > Tk + i * .09; if (!off) knock(ctx, a1_rect(x - 3, y - 4, x + 3, y + 4), '#E6D9BC'); });
  // Yıldız'da tek pencere: "Yıldız'dan" sözünde yanar
  const wl = ramp(t, Ty, Ty + .25, E.out2), [wx, wy] = hp(1510, 444);
  if (wl > 0) {
    const fl = .9 + .2 * hash(Math.floor(t * 15) * 3.7);  // lamba titrer (15 fps ızgarası)
    for (const [rx, a] of [[58, .08], [36, .14], [20, .24]]) { ctx.save(); ctx.globalAlpha = wl * a * fl; knock(ctx, a1_ell(wx, wy, rx * fl, rx * .8 * fl), P.paper); ctx.restore(); }
    ctx.save(); ctx.globalAlpha = wl; knock(ctx, a1_rect(wx - 8, wy - 10, wx + 8, wy + 10), '#FFF6E2'); plate(ctx, 'sepia', a1_rect(wx - 8, wy + 2, wx + 8, wy + 10), { a: .22 }); ctx.restore();
  }
  // Boğaz: koyu su, dalga kazımaları, pencere yansıması
  const sea = a1_rect(-240, 630, W + 260, 960);
  knock(ctx, sea); plate(ctx, 'navy', sea, { a: .85, flat: true }); plate(ctx, 'ink', sea, { a: .2, flat: true });
  const rr = rng(21); for (let i = 0; i < 90; i++) { const y = 640 + Math.pow(rr(), 1.4) * 300, x = ((-200 + rr() * (W + 420) + t * (12 + (y - 630) * .05)) % (W + 420) + W + 420) % (W + 420) - 200, L = 10 + (y - 630) * .18 + rr() * 30; cut(ctx, PL([[x, y], [x + L, y]], false), 1.2 + (y - 630) * .006, { a: .14 + (y - 630) * .0006 }); }
  inkStroke(ctx, PL([[-240, 630], [W + 260, 630]], false), 2, { a: .6 });
  if (wl > 0) for (let i = 0; i < 12; i++) { const y = 642 + i * 22, w = 14 + i * 2.2 + Math.sin(tf * 4 + i * 1.7) * 4; cut(ctx, PL([[wx - w + Math.sin(i * 2.3) * 6, y], [wx + w + Math.sin(i * 2.3) * 6, y]], false), 2.4, { a: wl * (.7 - i * .045) }); }
  ctx.restore();
  // ön plan: rıhtım, nöbetçi ve Meclis kapısı
  ctx.save(); cam(ctx, c, 1);
  const quay = a1_rect(700, 930, W + 300, H + 80); knock(ctx, quay); plate(ctx, 'navy', quay, { a: .85, flat: true }); plate(ctx, 'ink', quay, { a: .5, flat: true });
  inkStroke(ctx, PL([[700, 930], [W + 300, 930]], false), 3); cut(ctx, PL([[700, 938], [W + 300, 938]], false), 1.4, { a: .3 });
  for (let i = 0; i < 16; i++) cut(ctx, PL([[860 + i * 82, 944], [856 + i * 82, 1090]], false), 1.4, { a: .16 });
  // "Yıldız'dan" sözünden sonra nöbetçi rıhtım boyunca yürür (6 fps adım)
  const gw = Math.max(0, t - Ty - .2);
  a1_guard(ctx, 1030 + gw * 120, 1004, 3.1, Math.floor(t * 6) % 2, gw > 0);
  a1_imgM(ctx, a1_cacheM('a1-b01b-door', g => a1_door(g)));
  const pc = clamp((t - Tta + .18) / .3), sw = settle(t, Tta + .12, .22, 1.6, 3.2);
  a1_chainLock(ctx, pc, sw);
  a1_seal(ctx, 430, 520, a1_pop(t, Tet, .14));
  ctx.restore();
}, { tr: { type: 'cut' }, post: { vig: 1.1, stone: .10 } });

// ═══════════ B02 · Abdülhamid masada: okul planı ve jurnaller ═══════════
// okul planı (düz): cephe görünüşü + kat planı; p: çizim ilerlemesi 0..1
function a1_planDraw(g, p, o = {}) {
  const w = 600, h = 420;
  knock(g, PL(rough([[0, 0], [w, 0], [w, h], [0, h]], 1, 3)));
  inkStroke(g, a1_rect(10, 10, w - 10, h - 10), 1.4, { a: .8 });
  const seg = (a, b) => clamp((p - a) / (b - a));
  // cephe: zemin çizgisi, gövde, orta çıkıntı + alınlık, pencereler
  const draw = (path, len, a, b, wd = 2) => { const q = seg(a, b); if (q <= 0) return; g.save(); g.setLineDash([len * q, 1e5]); inkStroke(g, path, wd); g.restore(); };
  draw(PL([[40, 236], [560, 236]], false), 520, 0, .12, 2.4);
  draw(a1_rect(70, 110, 530, 236), 1180, .08, .3, 2.2);
  draw(PL([[240, 236], [240, 92], [300, 58], [360, 92], [360, 236]], false), 420, .2, .38, 2.2);
  draw(PL([[60, 110], [540, 110]], false), 480, .28, .36, 1.6);
  for (let f = 0; f < 2; f++) for (let i = 0; i < 9; i++) {
    const x = 92 + i * 50 + (i >= 3 ? 8 : 0) + (i >= 6 ? 8 : 0); if (i === 4) continue;
    const y = 132 + f * 54, wp = new Path2D(); wp.moveTo(x, y + 36); wp.lineTo(x, y + 10); wp.arc(x + 11, y + 10, 11, PI, 0); wp.lineTo(x + 22, y + 36); wp.closePath();
    const a = .34 + (f * 9 + i) / 18 * .3; draw(wp, 110, a, a + .05, 1.5);
  }
  { const dp = new Path2D(); dp.moveTo(282, 236); dp.lineTo(282, 186); dp.arc(300, 186, 18, PI, 0); dp.lineTo(318, 236); draw(dp, 160, .62, .68, 1.8); }
  // kat planı
  draw(a1_rect(70, 268, 530, 390), 1160, .66, .8, 2);
  for (const x of [130, 190, 240, 360, 410, 470]) draw(PL([[x, 268], [x, 390]], false), 122, .78, .86, 1.3);
  draw(PL([[240, 330], [360, 330]], false), 120, .84, .9, 1.3);
  // ölçü çizgileri ve Osmanlıca not
  if (p > .88) { g.save(); g.globalAlpha = seg(.88, .96); g.setLineDash([3, 4]); inkStroke(g, PL([[70, 252], [530, 252]], false), 1); g.restore(); scriptLine(g, 520, 412, 180, 6, 61, { w: 1.2, a: seg(.9, 1) }); scriptLine(g, 300, 36, 150, 8, 62, { w: 1.6, a: seg(.0, .1) }); }
  // memur ve subay damgaları
  for (const [cx, k, ic] of [[120, 'm', o.m || 0], [480, 's', o.s || 0]]) {
    if (ic <= 0) continue;
    g.save(); g.translate(cx, 330); g.scale(ic, ic); g.globalAlpha = .92;
    const ring = a1_ell(0, 0, 34, 34); knock(g, ring); inkStroke(g, ring, 3, { col: P.red, mode: 'multiply' }); inkStroke(g, a1_ell(0, 0, 27, 27), 1.3, { col: P.red, mode: 'multiply' });
    if (k === 'm') { inkStroke(g, PL([[-12, 14], [14, -16]], false), 3, { col: P.red, mode: 'multiply' }); inkFill(g, PL([[-14, 16], [-10, 10], [-8, 14]]), { col: P.red }); g.globalCompositeOperation = 'multiply'; plate(g, 'red', a1_rect(-16, 8, -2, 18), { flat: true }); }
    else { for (const sgn of [-1, 1]) inkStroke(g, PL([[-16 * sgn, 16], [16 * sgn, -16]], false), 3, { col: P.red, mode: 'multiply' }); inkStroke(g, PL([[-8, 4], [-2, 10]], false), 2, { col: P.red, mode: 'multiply' }); inkStroke(g, PL([[8, 4], [2, 10]], false), 2, { col: P.red, mode: 'multiply' }); }
    g.restore();
  }
}
let A1_PLAN = null;
function a1_planOn(ctx, x, y, sc, skew, p, o) {
  if (!A1_PLAN) A1_PLAN = makeCanvas(Math.ceil(620 * RS), Math.ceil(440 * RS));
  const g = A1_PLAN.getContext('2d'); g.setTransform(1, 0, 0, 1, 0, 0); g.clearRect(0, 0, A1_PLAN.width, A1_PLAN.height);
  g.setTransform(RS, 0, 0, RS, 10 * RS, 10 * RS); g.globalCompositeOperation = 'source-over';
  a1_planDraw(g, p, o);
  ctx.save(); ctx.translate(x, y); ctx.transform(sc, 0, skew, sc * .46, 0, 0);
  plate(ctx, 'ink', a1_rect(6, 14, 616, 446), { a: .32 });
  ctx.drawImage(A1_PLAN, -10, -10, 620, 440);
  ctx.restore();
}
// jurnal yığını: üst üste kâğıtlar, ip, gölgede; extra: yığına düşen yeni kâğıt (0..1)
function a1_jurnals(ctx, x, y, n, sc, extra = 0, seed = 5) {
  const r = rng(seed);
  ctx.save(); ctx.translate(x, y); ctx.scale(sc, sc);
  plate(ctx, 'ink', SP([[-200, 30], [200, 26], [220, 60], [-190, 64]], true), { a: .35 });
  for (let i = 0; i < n; i++) {
    const yy = -i * 7, dx = (r() - .5) * 26, rt = (r() - .5) * .05;
    const pg = PL(rough([[-180 + dx, yy - 40], [180 + dx, yy - 44], [190 + dx, yy + 26], [-186 + dx, yy + 30]].map(([a, b]) => [a * Math.cos(rt) - b * Math.sin(rt), a * Math.sin(rt) + b * Math.cos(rt)]), 1.4, seed + i));
    knock(ctx, pg); plate(ctx, 'sepia', pg, { a: .18 + (i % 3) * .06 }); inkStroke(ctx, pg, 2);
    inkStroke(ctx, PL([[-186 + dx, yy + 24], [190 + dx, yy + 20]], false), 1.2, { a: .5 });
  }
  const top = -(n - 1) * 7;
  for (let k = 0; k < 4; k++) scriptLine(ctx, 150, top - 24 + k * 12, 290 * (k === 3 ? .5 : .95), 4.5, seed * 9 + k, { w: 1.4, a: .85 });
  // ip
  inkStroke(ctx, PL([[-30, top - 46], [-24, 30]], false), 3); inkStroke(ctx, PL([[-196, top - 6], [196, top - 12]], false), 3);
  inkStroke(ctx, SP([[-26, top - 10], [-46, top - 26], [-60, top - 12]], false), 2.4); inkStroke(ctx, SP([[-26, top - 10], [-4, top - 30], [10, top - 16]], false), 2.4);
  if (extra > 0) {
    const e = E.out3(extra), yy = top - 10 - (1 - e) * 90, xx = 40 + (1 - e) * 160, rt = -.08 + (1 - e) * .3;
    ctx.save(); ctx.translate(xx, yy); ctx.rotate(rt); ctx.globalAlpha = clamp(extra * 4);
    const pg = PL(rough([[-170, -40], [170, -44], [176, 24], [-172, 28]], 1.4, 99)); plate(ctx, 'ink', PL([[-164, -32], [178, -36], [184, 34], [-166, 38]]), { a: .25 }); knock(ctx, pg); plate(ctx, 'sepia', pg, { a: .12 }); inkStroke(ctx, pg, 2);
    for (let k = 0; k < 4; k++) scriptLine(ctx, 150, -24 + k * 12, 290 * (k === 3 ? .5 : .95), 4.5, 700 + k, { w: 1.4 });
    ctx.restore();
  }
  ctx.restore();
}
// masa (sepya): üst yüzey + oymalı ön yüz
function a1_desk(g, y0, y1) {
  const top = PL([[-40, y0], [W + 40, y0], [W + 40, y1], [-40, y1]]);
  knock(g, top); plate(g, 'sepia', top, { a: .62 });
  const r = rng(17); for (let i = 0; i < 14; i++) { const yy = y0 + 8 + i * (y1 - y0 - 10) / 14 + r() * 2, p = new Path2D(); let x = -40; p.moveTo(x, yy); while (x < W + 40) { const nx = x + 90 + r() * 160; p.quadraticCurveTo((x + nx) / 2, yy + (r() - .5) * 5, nx, yy + (r() - .5) * 2); x = nx; } inkStroke(g, p, 1.4, { a: .35 + r() * .25 }); }
  const front = a1_rect(-40, y1, W + 40, H + 40); knock(g, front); plate(g, 'sepia', front, { n: 2 }); plate(g, 'ink', front, { a: .35 });
  inkStroke(g, PL([[-40, y0], [W + 40, y0]], false), 3.6); inkStroke(g, PL([[-40, y1], [W + 40, y1]], false), 4);
  cut(g, PL([[-40, y1 + 6], [W + 40, y1 + 6]], false), 1.6, { a: .45 });
  for (let i = 0; i < 4; i++) { const x0 = 40 + i * 480; inkStroke(g, a1_rect(x0, y1 + 36, x0 + 400, H + 60), 2.4, { a: .8 }); cut(g, a1_rect(x0 + 10, y1 + 46, x0 + 390, H + 60), 1.4, { a: .35 }); }
}
shot(S('B02'), (ctx, st) => {
  setReg(103);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const To = a1_W('B02', 'okuldu'), Ts = a1_W('B02', 'sadık'), Tme = a1_W('B02', 'memurlar'), Tsu = a1_W('B02', 'subaylar');
  const c = { x: kf(t, [[S('B02'), 960], [Se('B02') + .8, 920]]), y: kf(t, [[S('B02'), 540], [Se('B02') + .8, 560]]), z: kf(t, [[S('B02'), 1.0], [Se('B02') + .8, 1.06]]) };
  const HX = 935, HY = 292, HS = 1.95;
  // oda (durağan): düz duvar + ince duvar kâğıdı çizgisi (başın arkasında yarım ton yok), pencere, dolap
  const room = a1_cacheM('a1-b02-room', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R);
    plate(g, 'sepia', R, { a: .44 });
    for (let x = -200; x < W + 220; x += 46) { inkStroke(g, PL([[x, -220], [x, 600]], false), 1.1, { a: .16 }); for (let y = -200; y < 600; y += 92) inkFill(g, a1_ell(x + 23, y + ((x / 46) % 2) * 46, 3, 4.5), { a: .18 }); }
    inkStroke(g, PL([[-220, 600], [W + 220, 600]], false), 3); for (let i = 0; i < 11; i++) { const x0 = -200 + i * 230; inkStroke(g, a1_rect(x0, 626, x0 + 196, 800), 1.8, { a: .7 }); cut(g, a1_rect(x0 + 8, 634, x0 + 188, 792), 1.2, { a: .3 }); }
    plate(g, 'sepia', a1_rect(-220, 600, W + 220, H + 220), { a: .35 });
    // pencere (solda; nötr gün ışığı)
    const wx0 = 40, wx1 = 330, wy0 = 40, wy1 = 560, win = a1_rect(wx0, wy0, wx1, wy1);
    knock(g, win); plate(g, 'sepia', win, { a: .3 }); plate(g, 'sepia', a1_rect(wx0, 400, wx1, wy1), { a: .2 });
    const cyp = new Path2D(); for (const [x, h] of [[90, 170], [122, 120], [282, 190]]) { cyp.moveTo(x, 480); cyp.quadraticCurveTo(x - 16, 480 - h * .5, x, 480 - h); cyp.quadraticCurveTo(x + 16, 480 - h * .5, x, 480); }
    plate(g, 'sepia', cyp, { a: .5 }); plate(g, 'sepia', a1_rect(wx0, 476, wx1, wy1), { a: .38 });
    const fr = new Path2D(); fr.rect(wx0 - 16, wy0 - 16, wx1 - wx0 + 32, 16); fr.rect(wx0 - 16, wy1, wx1 - wx0 + 32, 20); fr.rect(wx0 - 16, wy0, 16, wy1 - wy0); fr.rect(wx1, wy0, 16, wy1 - wy0); fr.rect((wx0 + wx1) / 2 - 6, wy0, 12, wy1 - wy0); fr.rect(wx0, 290, wx1 - wx0, 10);
    knock(g, fr); plate(g, 'sepia', fr, { n: 2 }); inkStroke(g, fr, 2.4);
    for (const [x0, x1, sg] of [[-30, 80, 1], [290, 400, -1]]) { const cur = SP([[x0, 10], [x1, 10], [x1 - sg * 10, 300], [x1 + sg * 6, 620], [x0 - sg * 4, 630], [x0 + sg * 8, 300]], true, .7); knock(g, cur); plate(g, 'sepia', cur, { a: .75 }); inkStroke(g, cur, 2.6); for (let k = 1; k < 4; k++) { const xx = lerp(x0, x1, k / 4); inkStroke(g, SP([[xx, 20], [xx + sg * 6, 300], [xx - sg * 4, 620]], false), 1.6, { a: .6 }); } }
    inkStroke(g, PL([[-60, 6], [440, 6]], false), 5);
    // dolap ve kitaplar (sağ)
    const cab = a1_rect(1540, 40, 2000, 800); knock(g, cab); plate(g, 'sepia', cab, { n: 2 }); plate(g, 'ink', cab, { a: .25 }); inkStroke(g, cab, 3);
    const rr = rng(4);
    for (let sh = 0; sh < 5; sh++) { const y1 = 190 + sh * 150; cut(g, PL([[1552, y1], [1990, y1]], false), 2, { a: .4 }); let x = 1560; while (x < 1980) { const bw = 16 + rr() * 22, bh = 90 + rr() * 40, bk = a1_rect(x, y1 - bh, x + bw, y1 - 2); knock(g, bk); plate(g, 'sepia', bk, { a: .5 + rr() * .5 }); inkStroke(g, bk, 1.6); cut(g, PL([[x + 4, y1 - bh + 14], [x + bw - 4, y1 - bh + 14]], false), 1.2, { a: .5 }); x += bw + 2; } }
  });
  ctx.save(); cam(ctx, c, .55); a1_imgM(ctx, room); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  // Abdülhamid (oturuyor): planına dönük; ışık nötr
  a1_fig(ctx, t, { x: HX, y: HY, s: HS, dir: -1, who: 'abdulhamid', gear: 'fes', coat: 'setre', col: 'ink', age: 48, lookAt: [600, 820], len: 330, w: .9, turn: .4, seed: 21, tilt: .1, idle: .7 });
  a1_imgM(ctx, a1_cacheM('a1-b02-desk', g => a1_desk(g, 770, 905)));
  // jurnaller: sağda, gölgede; "sadık" sözünde yığına bir kâğıt daha
  a1_jurnals(ctx, 1400, 846, 12, .82, clamp((t - Ts) / .35));
  // plan çizilir; memur ve subay damgaları
  a1_planOn(ctx, 150, 762, 1.06, -.36, ramp(t, To, To + 2.4, E.io2), { m: a1_pop(t, Tme, .14), s: a1_pop(t, Tsu, .14) });
  // ön kol masada, el planın üstünde
  const sh = [HX - 58 * HS, HY + 116 * HS], hand = [610 + noise1(tf * .4, 3) * 3, 812];
  const A = arm(ctx, sh, hand, { upper: 190, fore: 176, w: 74, col: 'ink', bend: 1, lw: 4.4 });
  handDraw(ctx, A.wr[0], A.wr[1], A.ang, A.w2 / 20, 'rest', { side: 1 });
  ctx.restore();
  stamp(ctx, 'YILDIZ SARAYI · 1890', 114, 112, st.lt - .7, 4.4, { size: 48 });
}, { tr: { type: 'press', dur: .6 } });

// memur (kalem) / subay (çapraz kılıç) lastik damgası
function a1_roleStamp(g, kind, cx, cy, k) {
  if (k <= 0) return;
  g.save(); g.translate(cx, cy); g.scale(k, k); g.globalAlpha = .92;
  const ring = a1_ell(0, 0, 34, 34); knock(g, ring); inkStroke(g, ring, 3, { col: P.red, mode: 'multiply' }); inkStroke(g, a1_ell(0, 0, 27, 27), 1.3, { col: P.red, mode: 'multiply' });
  if (kind === 'm') { inkStroke(g, PL([[-12, 14], [14, -16]], false), 3, { col: P.red, mode: 'multiply' }); inkFill(g, PL([[-14, 16], [-10, 10], [-8, 14]]), { col: P.red }); }
  else { for (const sgn of [-1, 1]) inkStroke(g, PL([[-16 * sgn, 16], [16 * sgn, -16]], false), 3, { col: P.red, mode: 'multiply' }); inkStroke(g, PL([[-8, 4], [-2, 10]], false), 2, { col: P.red, mode: 'multiply' }); inkStroke(g, PL([[8, 4], [2, 10]], false), 2, { col: P.red, mode: 'multiply' }); }
  g.restore();
}
// ═══════════ B02b · Planın yakın planı: rüşdiye kareleri çizilerek çoğalır; memur ve subay damgaları ═══════════
let A1_MINI = null;
function a1_minis() {
  if (A1_MINI) return A1_MINI;
  const r = rng(52), out = [];
  let k = 0; while (out.length < 46 && k++ < 5000) {
    const x = 140 + r() * 1620, y = 110 + r() * 860;
    if (x < 860 && y < 640) continue; if (x < 820 && y > 760) continue;
    if (out.some(q => Math.abs(q[0] - x) < 104 && Math.abs(q[1] - y) < 86)) continue;
    out.push([x, y, Math.hypot(x - 500, y - 380) + r() * 120]);
  }
  return (A1_MINI = out.sort((a, b) => a[2] - b[2]));
}
shot(a1_W('B02', 'memurlar'), (ctx, st) => {
  setReg(110);
  paperBG(ctx);
  const t = st.t, t0 = st.t - st.lt, Tme = a1_W('B02', 'memurlar'), Tsu = a1_W('B02', 'subaylar'), T1 = st.t - st.lt + st.d;
  const c = { x: kf(t, [[t0, 960], [T1, 990, E.lin]]), y: kf(t, [[t0, 540], [T1, 520, E.lin]]), z: kf(t, [[t0, 1.0], [T1, 1.06, E.lin]]) };
  ctx.save(); cam(ctx, c, 1);
  a1_imgM(ctx, a1_cacheM('a1-b02b-sheet', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R); plate(g, 'sepia', R, { a: .72 });
    plate(g, 'ink', a1_rect(112, 84, 1856, 1046), { a: .35 });
    const sh = PL(rough([[92, 58], [1832, 50], [1842, 1024], [100, 1032]], 1.5, 5)); knock(g, sh);
    g.save(); g.clip(sh); for (let x = 100; x < 1850; x += 40) inkStroke(g, PL([[x, 40], [x, 1040]], false), 1, { a: .1 }); for (let y = 60; y < 1040; y += 40) inkStroke(g, PL([[80, y], [1850, y]], false), 1, { a: .1 }); g.restore();
    inkStroke(g, sh, 2.6); inkStroke(g, a1_rect(118, 80, 1816, 1006), 1.2, { a: .8 });
    g.save(); g.translate(150, 112); g.rotate(-.015); g.scale(1.12, 1.12); a1_planDraw(g, 1, {}); g.restore();
    scriptLine(g, 1790, 1050 - 70, 300, 12, 211, { w: 2.2 });
  }));
  // rüşdiye kareleri: birer birer çizilir (kelime anından bölümün sonuna)
  const M = a1_minis(), span = T1 - Tme + .05;
  M.forEach(([x, y], i) => {
    const ti = Tme - .05 + span * Math.pow(i / M.length, .8), q = clamp((t - ti) / .2); if (q <= 0) return;
    const R = a1_rect(x - 34, y - 24, x + 34, y + 24);
    ctx.save(); ctx.setLineDash([232 * q, 1e4]); inkStroke(ctx, R, 2.2); ctx.restore();
    if (q >= 1) { inkStroke(ctx, PL([[x - 34, y + 2], [x - 6, y + 2], [x - 6, y - 24]], false), 1.4); inkStroke(ctx, PL([[x + 10, y + 24], [x + 10, y + 14], [x + 22, y + 14], [x + 22, y + 24]], false), 1.4); scriptLine(ctx, x + 30, y + 40, 48, 5, 400 + i, { w: 1.2, a: .8 }); }
  });
  a1_roleStamp(ctx, 'm', 330, 850, a1_pop(t, Tme, .16) * 2.4);
  a1_roleStamp(ctx, 's', 620, 880, a1_pop(t, Tsu, .16) * 2.4);
  ctx.restore();

}, { tr: { type: 'cut' } });

// ═══════════ B03 · Okullar çoğalır: rüşdiye noktaları (600+), idadi kareleri (100+) ═══════════
let A1_SCH = null;
// bölge: Rumeli/Anadolu/Suriye yoğun; Irak orta; Hicaz kıyısı 6; Trablusgarp kıyısı 4; Necd, Ahsa ve Girit (1898 sonrası özerk) yok
function a1_region(lon, lat) {
  if (lon > 23.3 && lon < 26.5 && lat > 34.7 && lat < 35.8) return null;           // Girit
  if (lon < 25.2) return lat > 31.9 ? 'libya' : (lat > 38 ? 'core' : null);           // Trablusgarp yalnız kıyı
  if (lat < 30.2) return (lon > 35.6 && lon < 40.3 && lat < 29.5 && lat > 21) ? 'hicaz' : null;
  if (lon > 40 && lat < 37.2) return 'irak';
  return 'core';
}
function a1_schools() {
  if (A1_SCH) return A1_SCH;
  const G = a1_geo(), r = rng(1900), ist = a1_p(28.97, 41.01);
  const mk = (N, minD, quota, W) => {
    const out = [], cnt = {}; let k = 0;
    while (out.length < N && k++ < 60000) {
      const lon = 12 + r() * 37, lat = 21 + r() * 24, rg = a1_region(lon, lat); if (!rg) continue;
      if ((cnt[rg] || 0) >= (quota[rg] ?? 1e9) || r() > W[rg]) continue;
      const [x, y] = a1_p(lon, lat); if (!G.inEmpire1900(x, y)) continue;
      if (out.some(q => Math.hypot(q[0] - x, q[1] - y) < minD)) continue;
      cnt[rg] = (cnt[rg] || 0) + 1; out.push([x, y, Math.hypot(x - ist[0], y - ist[1]) + r() * 220]);
    }
    return out.sort((a, b) => a[2] - b[2]);
  };
  const rus = mk(300, 12.5, { libya: 4, hicaz: 6, irak: 26 }, { core: 1, irak: .5, hicaz: 1, libya: 1 });
  const ida = mk(78, 30, { libya: 1, hicaz: 1, irak: 6 }, { core: 1, irak: .5, hicaz: 1, libya: 1 });
  return (A1_SCH = { rus, ida });
}
function a1_schoolMarks(ctx, t, T0, T1, U0, U1, o = {}) {
  const { rus, ida } = a1_schools();
  const nR = Math.floor(rus.length * E.in2(clamp((t - T0) / (T1 - T0)))), nI = Math.floor(ida.length * E.io2(clamp((t - U0) / (U1 - U0))));
  const dur = (T1 - T0) / rus.length * 2.2;
  const settled = new Path2D(), halo = new Path2D();
  for (let i = 0; i < nR; i++) {
    const [x, y] = rus[i], ti = T0 + (T1 - T0) * Math.sqrt(i / rus.length), k = a1_pop(t, ti, .14);
    const r = 4.2 * (k || 1);
    halo.moveTo(x + r + 2, y); halo.arc(x, y, r + 2, 0, TAU); settled.moveTo(x + r, y); settled.arc(x, y, r, 0, TAU);
  }
  knock(ctx, halo); inkFill(ctx, settled, { col: o.dot || P.ink });
  for (let i = 0; i < nI; i++) {
    const [x, y] = ida[i], ti = U0 + (U1 - U0) * (i / ida.length), k = a1_pop(t, ti, .14) || 1, r = 7 * k;
    const sq = a1_rect(x - r, y - r, x + r, y + r);
    knock(ctx, a1_rect(x - r - 2.5, y - r - 2.5, x + r + 2.5, y + r + 2.5)); plate(ctx, 'red', sq, { flat: true }); inkStroke(ctx, sq, 2);
  }
}
shot(S('B03'), (ctx, st) => {
  setReg(104);
  paperBG(ctx);
  const t = st.t;
  const T0 = a1_W('B03', 'saltanatının'), T6 = a1_W('B03', 'altı'), Tr = a1_W('B03', 'rüşdiye'), Ty = a1_W('B03', 'yüzü', 1), Ti = a1_W('B03', 'idadi');
  const c = { x: kf(t, [[st.t - st.lt, 960], [Ti + 1, 984, E.lin]]), y: kf(t, [[st.t - st.lt, 540], [Ti + 1, 526, E.lin]]), z: kf(t, [[st.t - st.lt, 1.0], [Ti + 1, 1.055, E.lin]]) };
  ctx.save(); cam(ctx, c, 1);
  a1_drawMap1900(ctx);
  a1_schoolMarks(ctx, t, st.t - st.lt, Tr + .5, Ty - .05, st.t - st.lt + st.d - .1);
  ctx.restore();
  // izleyici katmanı: sayılar ve küçük etiketler (İran üstündeki boş kâğıtta)
  bigStamp(ctx, '600+', 1625, 390, t - T6, 9, { size: 150, knock: true });
  if (t > T6 + .15) stamp(ctx, '● RÜŞDİYE', 1520, 490, t - T6 - .15, 9, { size: 30, typing: .4, bg: P.paperD });
  bigStamp(ctx, '100+', 1625, 640, t - Ty, 9, { size: 150, plate: 'sepia', knock: true }); bigStamp(ctx, '100+', 1625, 640, t - Ty, 9, { size: 150, plate: 'sepia' });
  if (t > Ty + .15) stamp(ctx, '■ İDADİ', 1540, 740, t - Ty - .15, 9, { size: 30, typing: .4, bg: P.paperD });
}, { tr: { type: 'press', dur: .6 } });

// ═══════════ B04 · Askerî idadi yatakhanesi: sıra sıra demir karyola, fesli çocuklar ═══════════
// bir noktalı perspektif: göz 1,35 m, kaçış noktası (960, 430)
const A1_V = { x: 960, y: 430, f: 720, h: 1.35 };
const a1_v = (X, Y, Z) => [A1_V.x + X * A1_V.f / Z, A1_V.y + (A1_V.h - Y) * A1_V.f / Z];
const a1_vq = pts => PL(pts.map(p => a1_v(...p)));
function a1_bed(g, side, Z, seed) {
  const xw = side * 4.1, xa = side * 2.15, z0 = Z, z1 = Z + .92, top = .56, r = rng(seed);
  // bacaklar
  for (const [x, z] of [[xa, z0], [xa, z1]]) inkStroke(g, PL([a1_v(x, 0, z), a1_v(x, top, z)], false), Math.max(1.6, 26 / z));
  // şilte + battaniye
  const mt = a1_vq([[xw, top, z0], [xa, top, z0], [xa, top, z1], [xw, top, z1]]), mf = a1_vq([[xa, top, z0], [xa, top, z1], [xa, top - .2, z1], [xa, top - .2, z0]]);
  const side0 = a1_vq([[xw, top, z0], [xa, top, z0], [xa, top - .2, z0], [xw, top - .2, z0]]);
  for (const q of [mt, mf, side0]) knock(g, q);
  plate(g, 'sepia', side0, { a: .5 }); plate(g, 'sepia', mf, { a: .28 });
  const bl = a1_vq([[xw * .72 + xa * .28, top + .02, z0 - .02], [xa, top + .02, z0 - .02], [xa, top + .02, z1 + .02], [xw * .72 + xa * .28, top + .02, z1 + .02]]);
  plate(g, 'sepia', bl, { a: .42 });
  for (const u of [.35, .45]) { const x = lerp(xw * .72 + xa * .28, xa, u); inkStroke(g, PL([a1_v(x, top + .02, z0), a1_v(x, top + .02, z1)], false), Math.max(1, 14 / Z), { a: .55 }); }
  // yastık
  const pw = a1_vq([[xw * .98, top + .1, z0 + .12], [xw * .82 + xa * .18, top + .1, z0 + .12], [xw * .82 + xa * .18, top + .02, z1 - .1], [xw * .98, top + .02, z1 - .1]]); knock(g, pw); inkStroke(g, pw, Math.max(1.2, 20 / Z));
  for (const q of [mt, mf, side0]) inkStroke(g, q, Math.max(1.3, 22 / Z));
  // demir başlık ve ayak çubukları
  const lw = Math.max(1.6, 30 / Z);
  for (const [x, hh] of [[xw * .99, 1.15], [xa, .86]]) {
    inkStroke(g, PL([a1_v(x, 0, z0), a1_v(x, hh, z0), a1_v(x, hh, z1), a1_v(x, 0, z1)], false), lw);
    for (let k = 1; k < 4; k++) { const z = lerp(z0, z1, k / 4); inkStroke(g, PL([a1_v(x, top, z), a1_v(x, hh, z)], false), lw * .55); }
  }
}
// uzak çocuk: damga siluet (is) + kırmızı fes; oturur
function a1_stampKid(g, x, y, s, ph = 0) {
  const m = (px, py) => [x + px * s, y + py * s];
  const b = new Path2D(); b.ellipse(x, y + (-30 - ph * .4) * s, 5.2 * s, 6 * s, 0, 0, TAU);
  b.moveTo(...m(-9, -22)); b.quadraticCurveTo(...m(0, -25), ...m(9, -22)); b.lineTo(...m(11, 0)); b.lineTo(...m(-11, 0)); b.closePath();
  inkFill(g, b); const f = PL([m(-4.6, -34.5 - ph * .4), m(4.6, -34.5 - ph * .4), m(3.8, -42 - ph * .4), m(-3.8, -42 - ph * .4)]); knock(g, f); plate(g, 'red', f); inkStroke(g, f, Math.max(.8, .8 * s * .4));
}
// simge madalyonu: ekmek / setre / kitap
function a1_icon(ctx, kind, x, y, r, k) {
  if (k <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.scale(k, k);
  plate(ctx, 'ink', a1_ell(6, 8, r, r), { a: .35 });
  const c = a1_ell(0, 0, r, r); knock(ctx, c); plate(ctx, 'sepia', a1_ring(-r, -r, r, r, 0), { a: 0 });
  const ring = new Path2D(); ring.arc(0, 0, r, 0, TAU); ring.arc(0, 0, r - 12, 0, TAU, true); plate(ctx, 'sepia', ring, { a: .6 });
  inkStroke(ctx, c, 3); inkStroke(ctx, a1_ell(0, 0, r - 12, r - 12), 1.6);
  const u = r / 70;
  ctx.scale(u, u);
  if (kind === 'ekmek') {
    const loaf = SP([[-40, 14], [-38, -6], [-20, -22], [0, -26], [20, -22], [38, -6], [40, 14], [0, 20]], true, .8);
    knock(ctx, loaf); plate(ctx, 'sepia', loaf, { a: .7 }); plate(ctx, 'sepia', SP([[-40, 14], [40, 14], [36, 4], [-36, 4]], true), { a: .5 }); inkStroke(ctx, loaf, 3);
    for (const dx of [-18, 0, 18]) cut(ctx, SP([[dx - 6, -2], [dx + 2, -12], [dx + 8, -18]], false), 3.4, { a: .9 });
  } else if (kind === 'setre') {
    // uzun setre: dik yaka, tek sıra düğme, yanlara inen kollar, diz boyu etek
    const co = PL([[-12, -50], [12, -50], [22, -44], [30, -38], [34, 8], [36, 50], [-36, 50], [-34, 8], [-30, -38], [-22, -44]]);
    knock(ctx, co); plate(ctx, 'navy', co); inkStroke(ctx, co, 3);
    for (const sd of [-1, 1]) { const sl = PL([[sd * 26, -40], [sd * 40, -30], [sd * 44, 20], [sd * 34, 22], [sd * 30, -20]]); knock(ctx, sl); plate(ctx, 'navy', sl); plate(ctx, 'navy', sl, { a: .5 }); inkStroke(ctx, sl, 2.6); const cf = PL([[sd * 34, 14], [sd * 44, 12], [sd * 45, 22], [sd * 34, 24]]); knock(ctx, cf); plate(ctx, 'red', cf); inkStroke(ctx, cf, 1.6); }
    inkStroke(ctx, PL([[0, -44], [0, 50]], false), 2); for (let i = 0; i < 6; i++) { const b = a1_ell(-4, -36 + i * 13, 2.6, 2.6); knock(ctx, b); plate(ctx, 'sepia', b, { n: 2 }); inkStroke(ctx, b, .8); }
    const col = PL([[-12, -50], [12, -50], [12, -40], [-12, -40]]); knock(ctx, col); plate(ctx, 'red', col); inkStroke(ctx, col, 2);
  } else {
    // burs: büzgülü para kesesi ve önünde mecidiye
    const bag = SP([[-12, -30], [12, -30], [8, -20], [30, -4], [36, 22], [20, 40], [-20, 40], [-36, 22], [-30, -4], [-8, -20]], true, .8);
    knock(ctx, bag); plate(ctx, 'sepia', bag, { a: .8 }); plate(ctx, 'sepia', SP([[-36, 22], [-20, 40], [0, 40], [-10, 10], [-30, -4]], true), { a: .5 }); inkStroke(ctx, bag, 3);
    inkStroke(ctx, SP([[-14, -22], [0, -18], [14, -22]], false), 2.6); inkStroke(ctx, SP([[0, -19], [-14, -40], [-24, -30]], false), 2); inkStroke(ctx, SP([[0, -19], [10, -40], [22, -34]], false), 2);
    for (const [x, y] of [[-14, -8], [8, 6], [-4, 24]]) inkStroke(ctx, SP([[x, y], [x + 6, y + 4]], false), 1.6, { a: .6 });
    const coin = a1_ell(22, 26, 22, 22); knock(ctx, coin); plate(ctx, 'sepia', a1_ell(22, 26, 22, 22), { a: .18 }); inkStroke(ctx, coin, 2.6); inkStroke(ctx, a1_ell(22, 26, 16, 16), 1.2);
    for (let k = 0; k < 24; k++) { const a = k / 24 * TAU; inkStroke(ctx, PL([[22 + Math.cos(a) * 19, 26 + Math.sin(a) * 19], [22 + Math.cos(a) * 21.5, 26 + Math.sin(a) * 21.5]], false), 1, { a: .7 }); }
    scriptLine(ctx, 32, 28, 20, 4, 77, { w: 1.4 });
  }
  ctx.restore();
}
shot(S('B04'), (ctx, st) => {
  setReg(105);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const c = { x: 960, y: kf(t, [[st.t - st.lt, 540], [st.t - st.lt + st.d, 528, E.lin]]), z: kf(t, [[st.t - st.lt, 1.0], [st.t - st.lt + st.d, 1.06, E.lin]]) };
  const room = a1_cacheM('a1-b04-room', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R);
    const zB = 14, wl = 4.2, ht = 4.3;
    // tavan, duvarlar, zemin
    const ceil = a1_vq([[-wl, ht, 1], [wl, ht, 1], [wl, ht, zB], [-wl, ht, zB]]), floor = a1_vq([[-wl, 0, 1], [wl, 0, 1], [wl, 0, zB], [-wl, 0, zB]]);
    const lw_ = a1_vq([[-wl, 0, 1], [-wl, ht, 1], [-wl, ht, zB], [-wl, 0, zB]]), rw = a1_vq([[wl, 0, 1], [wl, ht, 1], [wl, ht, zB], [wl, 0, zB]]), back = a1_vq([[-wl, 0, zB], [wl, 0, zB], [wl, ht, zB], [-wl, ht, zB]]);
    plate(g, 'sepia', ceil, { a: .35 }); plate(g, 'sepia', lw_, { a: .2 }); plate(g, 'sepia', rw, { a: .3 }); plate(g, 'sepia', back, { a: .18 }); plate(g, 'sepia', floor, { a: .3 });
    // tavan kirişleri
    for (let z = 1.5; z < zB; z += 1.6) { const bm = a1_vq([[-wl, ht, z], [wl, ht, z], [wl, ht - .18, z + .01], [-wl, ht - .18, z + .01]]); plate(g, 'sepia', bm, { n: 2 }); inkStroke(g, PL([a1_v(-wl, ht - .18, z), a1_v(wl, ht - .18, z)], false), Math.max(1.4, 24 / z)); }
    // zemin tahtaları
    for (let x = -wl; x <= wl; x += .42) inkStroke(g, PL([a1_v(x, 0, 1), a1_v(x, 0, zB)], false), 1.2, { a: .35 });
    // sol duvar pencereleri (kemerli): kâğıt ışık + zemine düşen ışık
    for (let z = 2.2; z < zB - .5; z += 2.4) {
      const z0 = z, z1 = z + .9, y0 = 1.25, y1 = 3.2;
      const wp = new Path2D(); const P0 = a1_v(-wl, y0, z0), P1 = a1_v(-wl, y1, z0), P2 = a1_v(-wl, y1 + .35, (z0 + z1) / 2), P3 = a1_v(-wl, y1, z1), P4 = a1_v(-wl, y0, z1);
      wp.moveTo(...P0); wp.lineTo(...P1); wp.quadraticCurveTo(P1[0] + (P3[0] - P1[0]) * .5, P2[1] - (P1[1] - P2[1]) * .4, ...P3); wp.lineTo(...P4); wp.closePath();
      knock(g, wp); plate(g, 'sepia', wp, { a: .2 }); inkStroke(g, wp, Math.max(1.6, 40 / z)); inkStroke(g, PL([a1_v(-wl, (y0 + y1) / 2, z0), a1_v(-wl, (y0 + y1) / 2, z1)], false), Math.max(1, 20 / z));
      const shaft = a1_vq([[-wl, 0, z0 + .2], [-wl, 0, z1 + .2], [-wl + 2.6, 0, z1 + 1.1], [-wl + 2.6, 0, z0 + 1.1]]); g.save(); g.globalAlpha = .38; knock(g, shaft); g.restore();
    }
    // arka duvar: kapı ve saat
    const dr = a1_vq([[-.6, 0, zB], [.6, 0, zB], [.6, 2.3, zB], [-.6, 2.3, zB]]); knock(g, dr); plate(g, 'sepia', dr, { n: 2 }); inkStroke(g, dr, 2);
    const [ckx, cky] = a1_v(0, 3.2, zB); knock(g, a1_ell(ckx, cky, 12, 12)); inkStroke(g, a1_ell(ckx, cky, 12, 12), 2); inkStroke(g, PL([[ckx, cky], [ckx, cky - 8], [ckx, cky], [ckx + 6, cky]], false), 1.6);
    for (const q of [ceil, floor, lw_, rw, back]) inkStroke(g, q, 2.4);
    // karyolalar: arkadan öne
    for (let i = 5; i >= 0; i--) { const Z = 2.6 + i * 1.85; a1_bed(g, -1, Z, 10 + i); a1_bed(g, 1, Z, 20 + i); }
  });
  ctx.save(); cam(ctx, c, .85); a1_imgM(ctx, room);
  // yatakhane lambaları: "yatılıydı" sözünde yanar
  const Ty2 = a1_W('B04', 'yatılıydı');
  for (const [Z, k] of [[3.4, 0], [7.2, 1], [11, 2]]) {
    const on = ramp(t, Ty2 + k * .12, Ty2 + k * .12 + .15, E.out2), [lx, ly] = a1_v(0, 3.25, Z), sc = A1_V.f / Z / 120, [cx, cy] = a1_v(0, 4.3, Z);
    inkStroke(ctx, PL([[cx, cy], [lx, ly - 24 * sc]], false), Math.max(1.2, 3 * sc));
    if (on > 0) for (const [r, a] of [[150, .1], [95, .16], [55, .26]]) { ctx.save(); ctx.globalAlpha = on * a; knock(ctx, a1_ell(lx, ly + 14 * sc, r * sc, r * sc * .75)); ctx.restore(); }
    const gl = SP([[lx - 10 * sc, ly], [lx - 14 * sc, ly + 22 * sc], [lx, ly + 30 * sc], [lx + 14 * sc, ly + 22 * sc], [lx + 10 * sc, ly]], true, .8);
    knock(ctx, gl, on > .5 ? '#FFF7E4' : P.paper); if (on < .5) plate(ctx, 'sepia', gl, { a: .55 }); inkStroke(ctx, gl, Math.max(1.2, 2.6 * sc));
    const sh = PL([[lx - 40 * sc, ly + 2 * sc], [lx - 14 * sc, ly - 22 * sc], [lx + 14 * sc, ly - 22 * sc], [lx + 40 * sc, ly + 2 * sc]]); knock(ctx, sh); plate(ctx, 'sepia', sh, { n: 2 }); inkStroke(ctx, sh, Math.max(1.2, 2.8 * sc));
  }
  // uzaktaki çocuklar (damga siluet): karyola kenarında
  const ph = Math.floor(t * 6) % 2;
  const q15 = Math.floor(t * 15);
  [[-2.0, 11.9, 0], [2.0, 10.05, 1], [-2.0, 8.2, 1], [2.0, 6.35, 0], [-2.05, 4.5, 0], [2.05, 4.5, 1], [-2.0, 6.35, 1]].forEach(([X, Z, k], n) => { const [x, y] = a1_v(X + Math.sin(t * 1.3 + n * 2) * .03, .56, Z + .45); a1_stampKid(ctx, x, y, 1.15 * A1_V.f / Z / 52, Math.floor((q15 + n * 3) / (3 + n % 3)) % 2); });
  ctx.restore();
  // ön plan çocuklar (yüzleri seçilir; yarım ton yok)
  ctx.save(); cam(ctx, c, 1);
  const Ty = a1_W('B04', 'yediriyor'), Tg = a1_W('B04', 'giydiriyor'), Tb = a1_W('B04', 'burs');
  // "taşradan": iki çocuk başını çevirir (ara poz iki kare)
  const Tt = a1_W('B04', 'taşradan'), tq = Math.floor(t * 15) / 15, ph1 = tq < Tt ? 0 : tq < Tt + 2 / 15 ? 1 : 2;
  a1_kid(ctx, t, { x: 500, y: 520, s: 1.5, dir: 1, hdir: ph1 ? 1 : -1, wide: ph1 === 1 ? .78 : undefined, seed: 31, idle: 1.6, id: { mus: null, jaw: 1.0, hair: 'ink' }, age: 13, lookAt: t > Ty - .05 && t < Tg + .2 ? [260, 820] : ph1 ? [1300, 470] : [80, 380], look: ph1 === 1 ? [0, .2] : undefined, len: 520, tilt: ph1 ? -.03 : .04 });
  a1_kid(ctx, t, { x: 1430, y: 505, s: 1.6, dir: -1, hdir: ph1 ? -1 : 1, wide: ph1 === 1 ? .78 : undefined, seed: 32, idle: 1.6, id: { mus: null, jaw: .96, brow: .2, hair: 'sepia' }, age: 14, lookAt: t > Tg ? [1700, 600] : ph1 ? [600, 470] : [1900, 400], look: ph1 === 1 ? [0, .2] : undefined, len: 520 });
  // "giydiriyor": sağdaki yatağa katlanmış setre konur; "burs": üstüne bir mecidiye düşer
  const gk = clamp((t - Tg) / .3), [bx, by] = a1_v(2.75, .6, 2.75);
  if (gk > 0) {
    const dy = (1 - E.out3(gk)) * -220 + settle(t, Tg + .3, 7, 3, 8);
    ctx.save(); ctx.translate(bx + 30, by + dy - 26); ctx.rotate(-.05); ctx.scale(1.45, 1.45);
    plate(ctx, 'ink', a1_rect(-86, 16, 96, 34), { a: .3 });
    for (let k = 0; k < 3; k++) { const f = PL([[-88, 8 - k * 12], [88, 8 - k * 12], [92, 22 - k * 12], [-84, 22 - k * 12]]); knock(ctx, f); plate(ctx, 'navy', f); inkStroke(ctx, f, 2); }
    const cl = PL([[-30, -18], [30, -18], [26, -8], [-26, -8]]); knock(ctx, cl); plate(ctx, 'red', cl); inkStroke(ctx, cl, 1.8);
    for (let k = 0; k < 4; k++) { const b = a1_ell(-48 + k * 32, 2, 3, 3); knock(ctx, b); plate(ctx, 'sepia', b, { n: 2 }); }
    ctx.restore();
  }
  const bk = clamp((t - Tb) / .45);
  if (bk > 0) {
    const q = Math.floor(t * 15), land = bk >= 1;
    const x = lerp(1120, bx + 50, E.out2(bk)), y = lerp(260, by - 80, E.in2(bk)) + (land ? settle(t, Tb + .45, 6, 3, 9) : 0), sx = land ? 1 : Math.abs(Math.cos(q * .9)) * .85 + .15;
    const coin = a1_ell(x, y, 34 * sx, land ? 13 : 34); plate(ctx, 'ink', a1_ell(x + 6, y + 8, 34 * sx, land ? 12 : 30), { a: .25 }); knock(ctx, coin); plate(ctx, 'sepia', coin, { a: .22 }); inkStroke(ctx, coin, 3); inkStroke(ctx, a1_ell(x, y, 24 * sx, land ? 9 : 24), 1.4);
    if (!land && sx > .5) scriptLine(ctx, x + 12 * sx, y + 4, 22 * sx, 5, 77, { w: 1.6 });
  }
  ctx.restore();
  // "yediriyor": soldan ekmek uzatan el (aşçının kolu); ekmek elin önünde
  const ek = E.out3(clamp((t - Ty + .05) / .35));
  if (ek > 0) {
    ctx.save(); cam(ctx, c, 1);
    const hx = lerp(-120, 330, ek), hy = lerp(1000, 800, ek) + Math.sin(t * 2.2) * 3;
    const A = arm(ctx, [-260, 1180], [hx, hy], { upper: 300, fore: 280, w: 96, col: 'sepia', bend: 1, lw: 4.4 });
    handDraw(ctx, A.wr[0], A.wr[1], A.ang, A.w2 / 20 * .9, 'hold', { side: 1 });
    const loaf = SP([[-70, 16], [-64, -18], [-28, -44], [18, -46], [62, -26], [72, 12], [16, 28]], true, .8);
    ctx.save(); ctx.translate(A.wr[0] + 70, A.wr[1] - 30); ctx.rotate(-.18); plate(ctx, 'ink', SP([[-64, 30], [66, 26], [60, 40], [-60, 42]], true), { a: .3 });
    knock(ctx, loaf); plate(ctx, 'sepia', loaf, { a: .75 }); plate(ctx, 'sepia', SP([[-70, 16], [72, 12], [60, 2], [-62, 4]], true), { a: .5 }); inkStroke(ctx, loaf, 3.4);
    for (const dx of [-28, 2, 32]) cut(ctx, SP([[dx - 9, 0], [dx + 3, -18], [dx + 12, -27]], false), 4, { a: .9 });
    ctx.restore();
    ctx.restore();
  }
  // devletin verdikleri: ekmek, setre, kitap
  a1_icon(ctx, 'ekmek', 640, 170, 82, a1_pop(t, Ty, .18));
  a1_icon(ctx, 'setre', 960, 170, 82, a1_pop(t, Tg, .18));
  a1_icon(ctx, 'kese', 1280, 170, 82, a1_pop(t, Tb, .18));
}, { tr: { type: 'cut' } });

// ═══════════ B05a · Okul kapısı açılır; taşralı baba ve oğul (yorum cümlesi, 7,7 sn) ═══════════
// damga yaya: 'fes' | 'sapka' | 'carsaf'; ph: adım evresi
function a1_walker(g, x, y, s, kind, ph = 0) {
  g.save(); g.translate(x, y); g.scale(s, s);
  const b = new Path2D(), st = ph ? 3 : -3;
  b.ellipse(0, -90, 5.6, 6.6, 0, 0, TAU);
  if (kind === 'carsaf') { b.moveTo(-7, -96); b.quadraticCurveTo(0, -104, 7, -96); b.lineTo(12, -60); b.lineTo(15, -4); b.lineTo(-15, -4); b.lineTo(-11, -60); b.closePath(); }
  else { b.moveTo(-10, -82); b.lineTo(10, -82); b.lineTo(12, -40); b.lineTo(9, -38); b.lineTo(5 + st, 0); b.lineTo(0, 0); b.lineTo(1, -36); b.lineTo(-1, -36); b.lineTo(-4 - st, 0); b.lineTo(-9 - st, 0); b.lineTo(-9, -38); b.lineTo(-12, -40); b.closePath(); }
  inkFill(g, b);
  if (kind === 'fes') { const f = PL([[-5, -95], [5, -95], [4.2, -104], [-4.2, -104]]); knock(g, f); plate(g, 'red', f); inkStroke(g, f, .7); }
  else if (kind === 'sapka') { inkFill(g, PL([[-9, -95], [9, -95], [9, -97], [5, -97], [5, -106], [-5, -106], [-5, -97], [-9, -97]])); }
  g.restore();
}
// cepken: açık önlü kısa ceket; kaytan işlemeli kenarlar, arada gömlek ve kuşak (bust koordinatı)
function a1_cepken(ctx, x, y, s, dir, W_) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
  const shirt = PL([[-18, 82], [12, 84], [18, 330], [-26, 330]]); knock(ctx, shirt); plate(ctx, 'sepia', shirt, { a: .12 });
  for (let i = 0; i < 6; i++) inkStroke(ctx, PL([[-14 + i * .5, 110 + i * 34], [10 + i * .5, 110 + i * 34]], false), 1.2, { a: .35 });
  const sash = PL([[-100 * W_, 250], [74 * W_, 250], [74 * W_, 300], [-100 * W_, 300]]); knock(ctx, sash); plate(ctx, 'sepia', sash, { n: 2 }); plate(ctx, 'red', sash, { a: .45 }); for (let k = 0; k < 4; k++) inkStroke(ctx, PL([[-100 * W_, 258 + k * 12], [74 * W_, 258 + k * 12]], false), 1.4, { a: .55 }); inkStroke(ctx, sash, 2.2);
  for (const [a, b] of [[[-22, 80], [-34, 250]], [[14, 82], [24, 250]]]) {
    const e = SP([a, [lerp(a[0], b[0], .5) + (a[0] < 0 ? -6 : 6), lerp(a[1], b[1], .5)], b], false); inkStroke(ctx, e, 6); cut(ctx, e, 1.6, { a: .6 });
    for (let k = 0; k < 9; k++) { const u = k / 8, px = lerp(a[0], b[0], u) + (a[0] < 0 ? -9 : 9), py = lerp(a[1], b[1], u); inkStroke(ctx, a1_ell(px, py, 3.2, 2.4), 1.3, { a: .8 }); }
  }
  ctx.restore();
}
// yemeni: fesin dibine sarılı çizgili bez (taşra)
function a1_yemeni(ctx, hp) {
  ctx.save(); ctx.translate(hp.x, hp.y); ctx.rotate(hp.tilt || 0); ctx.scale(hp.s * hp.dir * hp.WD, hp.s * hp.HY);
  const band = SP([[-54, -14], [-30, -22], [4, -30], [30, -30], [36, -30], [35, -48], [6, -50], [-28, -42], [-52, -34]], true, .7);
  knock(ctx, band); plate(ctx, 'sepia', band, { a: .35 });
  ctx.save(); ctx.clip(band); for (let k = -6; k < 10; k++) inkStroke(ctx, PL([[-60 + k * 10, -10], [-46 + k * 10, -52]], false), 2, { a: .55 }); ctx.restore();
  inkStroke(ctx, band, 2.6 / hp.s * 1.2);
  const knot = SP([[-50, -30], [-64, -20], [-60, 0], [-52, -12]], true); knock(ctx, knot); plate(ctx, 'sepia', knot, { a: .5 }); inkStroke(ctx, knot, 2);
  ctx.restore();
}
// dalgalanan Osmanlı bayrağı (direğe bağlı); dalga 15 fps ızgarasında
function a1_flagWave(ctx, x, y, w, h, t) {
  const q = Math.floor(t * 15) / 15, wv = u => Math.sin(q * 5 - u * 5) * 7 * u;
  const top = [], bot = []; for (let k = 0; k <= 6; k++) { const u = k / 6; top.push([x + u * w, y + wv(u) + u * 4]); bot.push([x + u * w, y + h + wv(u) + u * 2]); }
  const fl = SP([...top, ...bot.reverse()], true, .5); knock(ctx, fl); plate(ctx, 'red', fl); inkStroke(ctx, fl, 2);
  const cx = x + w * .44, cy = y + h * .5 + wv(.44), cr = new Path2D(); cr.arc(cx, cy, h * .25, 0, TAU); cr.arc(cx + h * .07, cy - h * .03, h * .21, 0, TAU, true);
  ctx.save(); ctx.fillStyle = P.paper; ctx.fill(cr, 'evenodd'); ctx.restore(); knock(ctx, a0_starPath(new Path2D(), cx + h * .32, cy - h * .03, h * .12, PI)); // 1844 sonrası: beş köşeli yıldız, bir ucu aya
}
function a1_gateScene(g) {
  const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R);
  // gök: kâğıt, üstte seyrek sepya yarım ton (durağan)
  radialHT(g, 'sepia', 960, -1000, 1000, 1160, .3, 0, { cell: 12, ang: 15, box: [-220, -220, W + 220, 200] });
  // avlu (kapının ardı): aydınlık kâğıt, uzak bina
  const fac = a1_rect(900, 380, 1460, 700); plate(g, 'sepia', fac, { a: .22 });
  for (let i = 0; i < 6; i++) { const x = 940 + i * 86; for (const y of [430, 540]) { const w = a1_rect(x, y, x + 34, y + 62); plate(g, 'sepia', w, { a: .5 }); inkStroke(g, w, 1.4, { a: .7 }); } }
  inkStroke(g, PL([[900, 410], [1460, 410]], false), 2, { a: .7 }); plate(g, 'sepia', a1_rect(860, 700, 1500, 830), { a: .15 });
  // duvar ve kapı kemeri
  const wall = new Path2D(); wall.rect(-220, 250, W + 440, 580); wall.moveTo(1000, 830); wall.lineTo(1000, 560); wall.arc(1180, 560, 180, PI, 0); wall.lineTo(1360, 830); wall.closePath();
  g.save(); g.fillStyle = P.paper; g.fill(wall, 'evenodd'); g.restore();
  g.save(); g.clip(wall, 'evenodd');
  plate(g, 'sepia', a1_rect(-220, 250, W + 220, 830), { a: .42 });
  const r = rng(5); for (let y = 280; y < 830; y += 46) { inkStroke(g, PL([[-220, y], [W + 220, y]], false), 1.2, { a: .4 }); for (let x = -220 + ((y / 46) % 2) * 50; x < W + 220; x += 100) inkStroke(g, PL([[x + r() * 5, y], [x + r() * 5, y + 46]], false), 1.1, { a: .3 }); }
  g.restore();
  inkStroke(g, PL([[-220, 250], [W + 220, 250]], false), 3); plate(g, 'sepia', a1_rect(-220, 236, W + 220, 252), { n: 2 });
  for (const x of [960, 1400]) { const p = a1_rect(x - 44, 300, x + 44, 830); knock(g, p); plate(g, 'sepia', p, { a: .3 }); plate(g, 'sepia', a1_rect(x + 12, 300, x + 44, 830), { a: .45 }); inkStroke(g, p, 3); const cap = a1_rect(x - 58, 284, x + 58, 312); knock(g, cap); plate(g, 'sepia', cap, { a: .5 }); inkStroke(g, cap, 2.4); }
  const arch = new Path2D(); arch.moveTo(1000, 830); arch.lineTo(1000, 560); arch.arc(1180, 560, 180, PI, 0); arch.lineTo(1360, 830); inkStroke(g, arch, 3.4);
  const kit = a1_rect(1040, 300, 1320, 360); knock(g, kit); plate(g, 'sepia', kit, { a: .2 }); inkStroke(g, kit, 2.4); scriptLine(g, 1300, 340, 240, 14, 501, { w: 2.4 });
  // bayrak direği ve küçük bayrak (kırmızı vurgu)
  inkStroke(g, PL([[1180, 284], [1180, 120]], false), 4);
  // sokak
  const st = a1_rect(-220, 830, W + 220, H + 220); knock(g, st); plate(g, 'sepia', st, { a: .5 });
  inkStroke(g, PL([[-220, 830], [W + 220, 830]], false), 3);
  const rr = rng(8); for (let y = 850; y < H + 40; y += 26 + (y - 830) * .08) for (let x = -200 + rr() * 30; x < W + 200; x += 40 + (y - 830) * .12) inkStroke(g, SP([[x, y], [x + 14 + (y - 830) * .05, y - 6], [x + 28 + (y - 830) * .1, y]], false), 1.3, { a: .45 });
}
function a1_gateLeaf(g, hx, dir, ang) {
  // menteşe hx; kanat genişliği 180, açıldıkça daralır (cos) ve üst kenar perspektifle iner
  const w = 180 * Math.cos(ang), k = Math.sin(ang) * 26, x1 = hx + dir * w;
  const leaf = new Path2D(); leaf.moveTo(hx, 830); leaf.lineTo(hx, 560);
  const n = 12; for (let i = 0; i <= n; i++) { const u = i / n, a = PI + (dir > 0 ? u : 1 - u) * PI / 2 * (dir > 0 ? 1 : 1); }
  leaf.quadraticCurveTo(hx + dir * w * .1, 380 + k * .3, hx + dir * w, 380 + k);
  leaf.lineTo(x1, 830 - k * .4); leaf.closePath();
  knock(g, leaf); plate(g, 'sepia', leaf, { n: 2 }); plate(g, 'ink', leaf, { a: .2 + ang * .15 });
  g.save(); g.clip(leaf); for (let y = 600; y < 830; y += 60) inkStroke(g, PL([[hx, y], [x1, y - k * .2]], false), 2, { a: .6 }); for (let i = 1; i < 4; i++) { const x = hx + dir * w * i / 4; cut(g, PL([[x, 400], [x, 840]], false), 1.4, { a: .25 }); } g.restore();
  inkStroke(g, leaf, 3);
  if (ang < 1.2) { const kx = hx + dir * w * .82; inkStroke(g, a1_ell(kx, 690, 9 * Math.cos(ang) + 2, 11), 3.4); }
}
shot(S('B05'), (ctx, st) => {
  setReg(106);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const Tk = a1_W('B05', 'kapı'), Tta = a1_W('B05', 'taşralı'), Tes = a1_W('B05', 'esnafın'), Tc = a1_W('B05', 'çocuğu');
  const c = { x: kf(t, [[st.t - st.lt, 1010], [Tk + .6, 1050, E.out2], [Tta + 1.4, 960]]), y: kf(t, [[st.t - st.lt, 560], [Tk + .6, 556, E.out2], [Tta + 1.4, 540]]), z: kf(t, [[st.t - st.lt, 1.06], [Tk + .6, 1.08, E.out2], [Tta + 1.4, 1.0], [S('B05') + 7.7, 1.03]]) };
  ctx.save(); cam(ctx, c, .9);
  a1_imgM(ctx, a1_cacheM('a1-b05-gate', g => a1_gateScene(g)));
  // avluda öğrenciler (kapı açılınca görünür)
  const op = anticip(t, Tk - .05, Tk + .75, .06), ang = clamp(op) * 1.38;
  a1_flagWave(ctx, 1182, 124, 118, 52, t);
  ctx.save(); const ap = new Path2D(); ap.moveTo(1000, 830); ap.lineTo(1000, 560); ap.arc(1180, 560, 180, PI, 0); ap.lineTo(1360, 830); ctx.clip(ap);
  const ph = Math.floor(t * 6) % 2;
  for (const [x0, v, k] of [[1020, 38, 0], [1300, -30, 1], [1150, 22, 1]]) { const x = x0 + v * (t - Tk); a1_walker(ctx, x, 770, .9, 'fes', (ph + k) % 2); }
  a1_gateLeaf(ctx, 1000, 1, ang); a1_gateLeaf(ctx, 1360, -1, ang);
  ctx.restore();
  // açılan kapıdan sokağa düşen ışık
  if (op > 0) { ctx.save(); ctx.globalAlpha = clamp(op) * .5; knock(ctx, PL([[1010, 830], [1350, 830], [1600, H + 40], [760, H + 40]])); ctx.restore(); }
  ctx.restore();
  // baba ve oğul: "taşralı" sözünde soldan girer, kapıya bakar; baba elini oğlunun omzuna koyar
  ctx.save(); cam(ctx, c, 1);
  const wi = clamp((t - Tta + .25) / 1.25), ex = (1 - E.out2(wi)) * -620, bob = wi < 1 ? Math.abs(Math.sin(tf * 9)) * -10 : 0;
  const step = wi >= 1 ? ramp(t, Tc - .2, Tc + .6, E.io2) * 40 : 0;
  const fx = 560 + ex + step, sx = 820 + ex + step;
  const look = [1180, 600];
  if (wi > 0) {
    a1_fig(ctx, t, { x: fx, y: 330 + bob, s: 1.72, dir: 1, who: 'anon', id: { beard: 'short', musCol: 'ink', mus: 'pala', hair: 'ink', jaw: 1.12, WD: 1.14, brow: -.08, browW: 1.3 }, gear: 'fes', coat: 'setre', col: 'sepia', age: 44, lookAt: look, len: 520, seed: 41, w: 1.06,
      under: (by) => a1_cepken(ctx, fx, by, 1.72, 1, 1.06), over: hp => a1_yemeni(ctx, hp) });
    a1_kid(ctx, t + .3, { x: sx, y: 560 + bob * .7, s: 1.38, dir: 1, seed: 42, id: { mus: null, jaw: 1.0, hair: 'ink' }, age: 11, col: 'sepia', lookAt: look, len: 520, tilt: -.06 });
    const A = arm(ctx, [fx + 64 * 1.72, 330 + bob + 118 * 1.72], [sx - 62, 560 + bob * .7 + 120], { upper: 108, fore: 100, w: 54, col: 'sepia', bend: -1 });
    handDraw(ctx, A.wr[0], A.wr[1], A.ang, A.w2 / 20, 'rest', { side: 1 });
  }
  ctx.restore();
}, { tr: { type: 'press', dur: .6 } });

// ═══════════ B05b · Tavsiye mektubu çekilir, karne gelir (yakın plan) ═══════════
// lastik damga (izleyici katmanı): kırmızı çerçeveli slab yazı, basılma darbesiyle
function a1_rubber(ctx, s, x, y, lt, rot = 0, size = 90, o = {}) {
  if (NOTEXT || lt < 0) return;
  const k = 1 + (1 - E.out3(clamp(lt / .18))) * .3, a = clamp(lt / .06);
  ctx.save(); ctx.font = FONT.title(size); ctx.letterSpacing = '6px'; const w = ctx.measureText(s).width; ctx.restore();
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.rotate(rot); ctx.scale(k, k);
  const pl = o.plate || 'red', col = P[pl];
  const b = PL(rough([[-w / 2 - 34, -size * .72], [w / 2 + 34, -size * .72], [w / 2 + 34, size * .5], [-w / 2 - 34, size * .5]], 2, s.length));
  if (o.bg) { const pb = a1_rect(-w / 2 - 50, -size * .88, w / 2 + 50, size * .66); plate(ctx, 'ink', a1_rect(-w / 2 - 42, -size * .78, w / 2 + 58, size * .76), { a: .3 }); knock(ctx, pb); }
  inkStroke(ctx, b, 7, { col, mode: 'multiply', a: .92 }); inkStroke(ctx, a1_rect(-w / 2 - 22, -size * .6, w / 2 + 22, size * .38), 2.2, { col, mode: 'multiply', a: .85 });
  txt(ctx, s, 0, size * .26, FONT.title(size), { align: 'center', plate: pl, ls: 6 });
  ctx.restore();
}
function a1_letter(ctx, x, y, rot) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  plate(ctx, 'ink', a1_rect(-262, -172, 290, 200), { a: .32 });
  const p = PL(rough([[-280, -190], [280, -190], [280, 190], [-280, 190]], 1.4, 71)); knock(ctx, p); plate(ctx, 'sepia', p, { a: .1 });
  inkStroke(ctx, PL([[-280, -40], [280, -40]], false), 1.2, { a: .45 });
  for (let i = 0; i < 7; i++) scriptLine(ctx, 240, -140 + i * 34, i === 6 ? 220 : 470, 10, 300 + i, { w: 2 });
  scriptLine(ctx, -60, 160, 160, 12, 311, { w: 2.4 });
  const wax = SP(rough([[-40, -4], [-28, -34], [4, -42], [32, -28], [42, 4], [30, 34], [-2, 42], [-32, 30]], 3, 7), true, .9);
  ctx.save(); ctx.translate(170, 120); knock(ctx, wax); plate(ctx, 'red', wax); inkStroke(ctx, a1_ell(2, 0, 25, 25), 2, { a: .8 }); scriptLine(ctx, 18, 4, 32, 7, 44, { w: 2 }); inkStroke(ctx, wax, 2.4); ctx.restore();
  inkStroke(ctx, p, 2.6);
  ctx.restore();
}
function a1_karne(ctx, x, y, rot) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  plate(ctx, 'ink', a1_rect(-330, -226, 362, 262), { a: .32 });
  const p = PL(rough([[-350, -245], [350, -245], [350, 245], [-350, 245]], 1.2, 81)); knock(ctx, p);
  plate(ctx, 'sepia', a1_ring(-338, -233, 338, 233, 12), { a: .5 }); inkStroke(ctx, a1_rect(-338, -233, 338, 233), 1.8); inkStroke(ctx, a1_rect(-326, -221, 326, 221), 1.1);
  scriptLine(ctx, 150, -170, 300, 16, 801, { w: 2.8 }); scriptLine(ctx, 90, -128, 180, 9, 802, { w: 1.6 });
  // not çizelgesi
  const x0 = -290, x1 = 290, y0 = -100, rh = 46;
  inkStroke(ctx, a1_rect(x0, y0, x1, y0 + rh * 6), 1.8);
  for (let i = 1; i < 6; i++) inkStroke(ctx, PL([[x0, y0 + rh * i], [x1, y0 + rh * i]], false), 1.1, { a: .7 });
  for (const xx of [70, 180]) inkStroke(ctx, PL([[xx, y0], [xx, y0 + rh * 6]], false), 1.1, { a: .7 });
  plate(ctx, 'sepia', a1_rect(x0, y0, x1, y0 + rh), { a: .25 });
  for (let i = 0; i < 6; i++) { scriptLine(ctx, x1 - 18, y0 + rh * i + 30, 100, 7, 820 + i, { w: 1.6 }); scriptLine(ctx, 160, y0 + rh * i + 30, 70, 7, 830 + i, { w: 1.6 }); if (i) scriptLine(ctx, 50, y0 + rh * i + 30, 260 - (i * 37) % 90, 7, 840 + i, { w: 1.6 }); }
  // mühür ve imza
  inkStroke(ctx, a1_ell(-230, 200, 30, 30), 2.4, { a: .85 }); inkStroke(ctx, a1_ell(-230, 200, 22, 22), 1.2, { a: .75 }); scriptLine(ctx, -214, 204, 34, 6, 851, { w: 1.6 });
  inkStroke(ctx, SP([[60, 205], [90, 190], [120, 208], [150, 186], [190, 200], [230, 194]], false), 2.2);
  inkStroke(ctx, p, 2.6);
  ctx.restore();
}
shot(a1_W('B05', 'kimin'), (ctx, st) => {
  setReg(107);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  // çapalar: mektup "değil"de çekilir, karne girer; Osmanlıca mühür ve ses efekti Wd('B05','karnesiyle') anında vurur
  const Td = a1_W('B05', 'değil'), Tk = a1_W('B05', 'karnesiyle');
  const c = { x: kf(t, [[st.t - st.lt, 950], [st.t - st.lt + st.d, 975, E.lin]]), y: 540, z: kf(t, [[st.t - st.lt, 1.0], [Tk + 1.6, 1.06, E.out2]]) };
  ctx.save(); cam(ctx, c, 1);
  a1_imgM(ctx, a1_cacheM('a1-b05b-table', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R); plate(g, 'sepia', R, { a: .25 }); // sanat 3. tur: masa L ≥170
    const r = rng(23); for (let i = 0; i < 40; i++) { const y = -200 + i * 36 + r() * 8, p = new Path2D(); let x = -220; p.moveTo(x, y); while (x < W + 220) { const nx = x + 120 + r() * 200; p.quadraticCurveTo((x + nx) / 2, y + (r() - .5) * 10, nx, y + (r() - .5) * 4); x = nx; } inkStroke(g, p, 1.5, { a: .3 + r() * .3 }); }
    for (const y of [180, 620]) { inkStroke(g, PL([[-220, y], [W + 220, y]], false), 2.4, { a: .6 }); cut(g, PL([[-220, y + 4], [W + 220, y + 4]], false), 1.2, { a: .25 }); }
    for (const [rx, a] of [[760, .1], [560, .12], [400, .14]]) { g.save(); g.globalAlpha = a; knock(g, a1_ell(980, 540, rx, rx * .62)); g.restore(); }
  }));
  // "kimin adamı": mühürlü tavsiye mektubu; "değil" sözünde kenara itilir
  const lo = E.in3(clamp((t - Td) / .4));
  if (lo < 1) a1_letter(ctx, 900 - lo * 1300 + Math.sin(t * 1.2) * 6, 520 - lo * 120 + Math.cos(t * .9) * 4, -.06 - lo * .5 + Math.sin(t * .8) * .01);
  // karne iki elde aşağıdan gelir (mektup çekilirken); damga "karnesiyle"de vurur
  const ki = E.out3(clamp((t - Td - .05) / .45)), sway = noise1(tf * .6, 5) * 4 + Math.sin(t * 1.3) * 2;
  if (ki > 0) {
    const kx = 980 + sway, ky = 520 + (1 - ki) * 720 + Math.sin(t * 1.1) * 3, kr = .03 + (1 - ki) * .1 + Math.sin(t * .9) * .004;
    a1_karne(ctx, kx, ky, kr);
    for (const sd of [-1, 1]) {
      const hx = kx + sd * 316, hy = ky + 150 + sd * 10;
      const A = arm(ctx, [kx + sd * 520, ky + 600], [hx, hy + 52], { upper: 280, fore: 260, w: 80, col: 'navy', bend: -sd, lw: 4 });
      // gömlek manşeti: bilekte kâğıt bant
      const ca = A.ang, nx = -Math.sin(ca), ny = Math.cos(ca), cw = A.w2 * .62, bx = A.wr[0] - Math.cos(ca) * 4, by = A.wr[1] - Math.sin(ca) * 4;
      const cf = PL([[bx + nx * cw, by + ny * cw], [bx + nx * cw + Math.cos(ca) * 12, by + ny * cw + Math.sin(ca) * 12], [bx - nx * cw + Math.cos(ca) * 12, by - ny * cw + Math.sin(ca) * 12], [bx - nx * cw, by - ny * cw]]);
      knock(ctx, cf); inkStroke(ctx, cf, 2.2);
      handDraw(ctx, A.wr[0] + Math.cos(ca) * 10, A.wr[1] + Math.sin(ca) * 10, A.ang, A.w2 / 20 * .85, 'rest', { side: -sd, skin: true });
    }
  }
  ctx.restore();
  // sahne içi: karnedeki not sütununa Osmanlıca "âlâ" mührü (kırmızı, Amiri)
  const Tst = Tk; // damga "karnesiyle" sözünde vurur
  const sk = t >= Tst ? 1 + (1 - E.out3(clamp((t - Tst) / .18))) * .3 : 0;
  if (sk > 0) {
    ctx.save(); cam(ctx, c, 1); ctx.translate(1180 + sway, 470); ctx.rotate(-.12); ctx.scale(sk, sk);
    const rr = PL(rough([[-96, -62], [96, -62], [96, 52], [-96, 52]], 1.6, 31));
    inkStroke(ctx, rr, 6, { col: P.red, mode: 'multiply', a: .9 }); inkStroke(ctx, a1_rect(-84, -50, 84, 40), 1.8, { col: P.red, mode: 'multiply', a: .85 });
    ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.font = '700 84px Amiri'; ctx.textAlign = 'center'; ctx.direction = 'rtl'; ctx.fillStyle = P.red; ctx.fillText('اعلا', 0, 22); ctx.restore();
    ctx.restore();
    // izleyici katmanı: Türkçe karşılığı belgenin dışında
    if (!NOTEXT && t > Tst + .3) {
      const a = clamp((t - Tst - .3) / .2); ctx.save(); ctx.globalAlpha = a;
      inkStroke(ctx, PL([[1420, 330], [1330, 400]], false), 2); 
      ctx.restore();
      stamp(ctx, 'ÂLÂ · PEK İYİ', 1430, 318, t - Tst - .3, 9, { size: 34, typing: .01 });
    }
  }
}, { tr: { type: 'cut' } });

// ═══════════ B06a · Selanik sokağı: küçük Mustafa askerî rüşdiyeye gider ═══════════
function a1_selanik(g) {
  const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R);
  radialHT(g, 'sepia', 960, -1050, 1000, 1180, .28, 0, { cell: 12, ang: 15, box: [-220, -220, W + 220, 140] });
  // uzak siluetler: minare, kilise kubbesi, servi, kale tepesi
  const far = new Path2D();
  far.moveTo(-220, 470); far.quadraticCurveTo(300, 360, 700, 420); far.quadraticCurveTo(1100, 470, 1500, 400); far.quadraticCurveTo(1800, 360, 2140, 430); far.lineTo(2140, 520); far.lineTo(-220, 520); far.closePath();
  far.rect(352, 150, 22, 300); far.moveTo(348, 150); far.lineTo(363, 92); far.lineTo(378, 150); far.closePath(); far.rect(344, 240, 38, 10);
  far.moveTo(1040, 400); far.arc(1100, 400, 60, PI, 0); far.closePath(); far.rect(1096, 300, 8, 44); far.rect(1086, 312, 28, 6);
  far.rect(1000, 400, 200, 90);
  for (const [x, h] of [[560, 150], [590, 120], [1660, 170], [1690, 130]]) { far.moveTo(x, 450); far.quadraticCurveTo(x - 15, 450 - h * .5, x, 450 - h); far.quadraticCurveTo(x + 15, 450 - h * .5, x, 450); }
  plate(g, 'sepia', far, { a: .38 });
  // cephe dizisi: cumbalı evler, dükkân tabelaları (Fransızca, Rumca serbest)
  const houses = [[-220, 330, 'PHARMACIE'], [210, 300, 'ΚΑΦΕΝΕΙΟΝ'], [620, 320, 'LIBRAIRIE'], [1020, 340, null]];
  for (const [x0, w, sign] of houses) {
    const top = 300 + (x0 % 3) * 14, fac = a1_rect(x0, top, x0 + w + 80, 840);
    knock(g, fac); plate(g, 'sepia', fac, { a: .25 + (x0 % 2 ? .08 : 0) }); inkStroke(g, fac, 2.6);
    const roof = PL([[x0 - 20, top], [x0 + w + 100, top], [x0 + w + 70, top - 46], [x0 + 10, top - 46]]); knock(g, roof); plate(g, 'sepia', roof, { n: 2 }); inkStroke(g, roof, 2.4);
    for (let k = 0; k < 9; k++) inkStroke(g, PL([[x0 + k * (w + 80) / 9, top - 44], [x0 + k * (w + 80) / 9 - 6, top]], false), 1.2, { a: .5 });
    // cumba
    const cb = a1_rect(x0 + 40, top + 40, x0 + w + 40, top + 220); knock(g, cb); plate(g, 'sepia', cb, { a: .35 }); inkStroke(g, cb, 2.6);
    for (let k = 0; k < 4; k++) { const wx = x0 + 60 + k * (w - 40) / 4, wi = a1_rect(wx, top + 70, wx + (w - 40) / 4 - 22, top + 180); knock(g, wi); plate(g, 'sepia', wi, { a: .5 }); inkStroke(g, wi, 1.8); inkStroke(g, PL([[wx, top + 120], [wx + (w - 40) / 4 - 22, top + 120]], false), 1.2); }
    for (const bx of [x0 + 60, x0 + w + 20]) inkStroke(g, PL([[bx, top + 220], [bx - 30, top + 270]], false), 3);
    // dükkân
    const sh = a1_rect(x0 + 30, 620, x0 + w + 50, 840); knock(g, sh); plate(g, 'sepia', sh, { n: 2 }); plate(g, 'ink', sh, { a: .25 }); inkStroke(g, sh, 2.4);
    if (sign) { const sb = a1_rect(x0 + 40, 560, x0 + w + 40, 606); knock(g, sb); inkStroke(g, sb, 2.2); inkStroke(g, a1_rect(x0 + 46, 566, x0 + w + 34, 600), 1); txt(g, sign, x0 + w / 2 + 40, 596, /[Α-Ω]/.test(sign) ? '400 34px "GFS Didot"' : FONT.slab(28), { align: 'center', ls: 3 }); }
    const aw = PL([[x0 + 20, 612], [x0 + w + 60, 612], [x0 + w + 80, 650], [x0, 650]]); knock(g, aw); plate(g, 'sepia', aw, { a: .4 }); for (let k = 0; k < 12; k++) inkStroke(g, PL([[x0 + 20 + k * (w + 40) / 12, 612], [x0 + k * (w + 80) / 12, 650]], false), 1.2, { a: .6 }); inkStroke(g, aw, 2);
  }
  // askerî rüşdiye (sağ): iki katlı resmî cephe, kemerli kapı, kitabe, bayrak
  const sx0 = 1400, sch = a1_rect(sx0, 250, 2140, 840); knock(g, sch); plate(g, 'sepia', sch, { a: .3 }); inkStroke(g, sch, 3);
  plate(g, 'sepia', a1_rect(sx0, 236, 2140, 256), { n: 2 }); inkStroke(g, PL([[sx0, 470], [2140, 470]], false), 2);
  for (let i = 0; i < 8; i++) for (const y of [300, 520]) { const x = sx0 + 40 + i * 92; if (y === 520 && (i === 3 || i === 4)) continue; const wp = new Path2D(); wp.moveTo(x, y + 120); wp.lineTo(x, y + 20); wp.arc(x + 20, y + 20, 20, PI, 0); wp.lineTo(x + 40, y + 120); wp.closePath(); knock(g, wp); plate(g, 'sepia', wp, { a: .55 }); inkStroke(g, wp, 1.8); }
  const gate = new Path2D(); gate.moveTo(sx0 + 300, 840); gate.lineTo(sx0 + 300, 640); gate.arc(sx0 + 370, 640, 70, PI, 0); gate.lineTo(sx0 + 440, 840); gate.closePath(); knock(g, gate); plate(g, 'sepia', gate, { n: 2 }); plate(g, 'ink', gate, { a: .3 }); inkStroke(g, gate, 3);
  const kit = a1_rect(sx0 + 270, 486, sx0 + 470, 530); knock(g, kit); inkStroke(g, kit, 2); scriptLine(g, sx0 + 456, 516, 170, 11, 905, { w: 2.2 });
  inkStroke(g, PL([[sx0 + 370, 236], [sx0 + 370, 90]], false), 4); const fl = SP([[sx0 + 372, 94], [sx0 + 430, 102], [sx0 + 470, 96], [sx0 + 466, 140], [sx0 + 426, 146], [sx0 + 372, 138]], true, .6); knock(g, fl); plate(g, 'red', fl); inkStroke(g, fl, 2);
  { const cr = new Path2D(); cr.arc(sx0 + 412, 120, 11, 0, TAU); cr.arc(sx0 + 416, 118, 9.5, 0, TAU, true); g.save(); g.fillStyle = P.paper; g.fill(cr, 'evenodd'); g.restore(); knock(g, a0_starPath(new Path2D(), sx0 + 427, 119, 5.5, PI)); }
  // kaldırım ve kaldırım taşı
  const st = a1_rect(-220, 840, W + 220, H + 220); knock(g, st); plate(g, 'sepia', st, { a: .48 }); inkStroke(g, PL([[-220, 840], [W + 220, 840]], false), 3);
  const rr = rng(12); for (let y = 860; y < H + 40; y += 24 + (y - 840) * .1) for (let x = -200 + rr() * 30; x < W + 200; x += 38 + (y - 840) * .14) inkStroke(g, SP([[x, y], [x + 13 + (y - 840) * .05, y - 6], [x + 26 + (y - 840) * .1, y]], false), 1.3, { a: .45 });
}
shot(S('B06'), (ctx, st) => {
  setReg(108);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const Ta = a1_W('B06', 'askeri'), Tm = a1_W('B06', 'mustafa');
  const c = { x: kf(t, [[S('B06'), 900], [Tm + .8, 1040]]), y: 540, z: kf(t, [[S('B06'), 1.04], [Tm + .8, 1.07]]) };
  ctx.save(); cam(ctx, c, .85);
  const fOK = !document.fonts || document.fonts.check('400 34px "GFS Didot"', 'Κ');
  a1_imgM(ctx, a1_cacheM('a1-b06-street' + (fOK ? '' : '-yedek'), g => a1_selanik(g)));
  // yayalar: fesli, şapkalı, çarşaflı (kozmopolit Selanik)
  const ph = Math.floor(t * 6) % 2, dt = t - S('B06');
  for (const [x0, v, kind, k] of [[1260, -34, 'carsaf', 0], [300, 26, 'sapka', 1], [880, -22, 'fes', 0], [1700, -18, 'fes', 1], [-60, 30, 'fes', 1]]) a1_walker(ctx, x0 + v * dt, 846, 2.15, kind, (ph + k) % 2);
  ctx.restore();
  // küçük Mustafa: okula doğru yürür (gövde kadraj altında kesilir)
  ctx.save(); cam(ctx, c, 1);
  const wx = 640 + E.io2(clamp((t - S('B06')) / 5.4)) * 230, bob = Math.abs(Math.sin(tf * 7.5)) * -9;
  a1_kid(ctx, t, { x: wx, y: 520 + bob, s: 1.62, dir: 1, who: 'mk', id: { mus: null }, age: 12, gear: 'fes', col: 'navy', lookAt: [1800, 620], len: 520, seed: 3, tilt: -.02 });
  ctx.restore();
  nameTag(ctx, 90, 880, 'MUSTAFA', '12 yaşında · 1893', t - Tm, 9);
}, { tr: { type: 'press', dur: .6 } });

// apoletler (bust koordinatı): omuz başlarında sırma uçlu kalıp
function a1_epaulets(ctx, x, y, s, dir, W_, turn = 0, tilt = 0) {
  const FS = 1 - .15 * turn;
  ctx.save(); ctx.translate(x, y); ctx.rotate(tilt); ctx.scale(s * dir, s);
  for (const [x0, x1, y0] of [[-98 * W_, -64 * W_, 100], [44 * W_ * FS, 68 * W_ * FS, 94]]) {
    const ap = PL([[x0, y0 + 2], [x1, y0 - 5], [x1 + 2, y0 + 6], [x0, y0 + 12]]); knock(ctx, ap); plate(ctx, 'ochre', ap, { n: 2 }); inkStroke(ctx, ap, 1.8);
    for (let k = 0; k < 5; k++) { const u = k / 4, px = lerp(x0, x1, .82) + (u - .5) * 10; inkStroke(ctx, PL([[px, y0 + 6], [px, y0 + 16]], false), 1.2, { a: .8 }); }
  }
  ctx.restore();
}
// ═══════════ B06b · Sınıf: kara tahtada geometri; öğretmen ona ikinci adı verir ═══════════
// isim levhası dönüşümü: "MUSTAFA" → "MUSTAFA KEMAL" (Ts anında)
function a1_tagMorph(ctx, x, y, a, b, sub, lt, ts) {
  if (NOTEXT) return;
  const al = env(lt, 0, .2); if (al <= 0) return;
  const fs = 64, ss = 40;
  ctx.save(); ctx.font = FONT.title(fs); ctx.letterSpacing = '1px'; const wa = ctx.measureText(a).width, wb = ctx.measureText(b).width, wsp = ctx.measureText(a + ' ').width; ctx.letterSpacing = '0px'; ctx.font = FONT.mono(ss); const w2 = ctx.measureText(sub).width; ctx.restore();
  const q = E.out3(clamp((lt - ts) / .3)), w = lerp(Math.max(wa, w2), Math.max(wb, w2), q) + 48, h = fs + ss + 38, x0 = x - w;
  ctx.save(); ctx.globalAlpha = al;
  plate(ctx, 'ink', a1_rect(x0 + 7, y + 9, x0 + w + 7, y + h + 9), { a: .35 });
  const box = PL(rough([[x0, y], [x0 + w, y], [x0 + w, y + h], [x0, y + h]], .8, 10)); knock(ctx, box); inkStroke(ctx, box, 3.2);
  plate(ctx, 'red', a1_rect(x0, y + h - 7, x0 + w, y + h));
  txt(ctx, a, x0 + 24, y + 14 + fs * .8, FONT.title(fs), { ls: 1 });
  if (lt >= ts) {
    ctx.save(); ctx.beginPath(); ctx.rect(x0, y, w, h); ctx.clip();
    const k = 1 + (1 - E.out3(clamp((lt - ts) / .2))) * .4, ex = x0 + 24 + wsp, ey = y + 14 + fs * .8;
    ctx.translate(ex, ey); ctx.scale(k, k);
    txt(ctx, b.slice(a.length).trim(), 0, 0, FONT.title(fs), { ls: 1, plate: lt - ts < .5 ? 'red' : undefined });
    ctx.restore();
  }
  txt(ctx, sub, x0 + 24, y + 22 + fs + ss * .72, FONT.mono(ss));
  ctx.restore();
}
shot(a1_W('B06', 'kendi') - .1, (ctx, st) => {
  setReg(109);
  paperBG(ctx);
  const t = st.t, tf = Math.floor(t * 15) / 15;
  const Tma = a1_W('B06', 'matematik'), To = a1_W('B06', 'ona'), Tk = a1_W('B06', 'kemal');
  const c = { x: kf(t, [[st.t - st.lt, 960], [Tk + .6, 1010, E.out2], [st.t - st.lt + st.d, 1020]]), y: kf(t, [[st.t - st.lt, 540], [Tk + .6, 556, E.out2], [st.t - st.lt + st.d, 560]]), z: kf(t, [[st.t - st.lt, 1.0], [Tk + .6, 1.07, E.out2], [st.t - st.lt + st.d, 1.08, E.lin]]) };
  ctx.save(); cam(ctx, c, .8);
  a1_imgM(ctx, a1_cacheM('a1-b06b-room', g => {
    const R = a1_rect(-220, -220, W + 220, H + 220); knock(g, R); plate(g, 'sepia', R, { a: .2 });
    for (let x = -200; x < W + 220; x += 120) inkStroke(g, PL([[x, -220], [x, 700]], false), 1, { a: .14 });
    inkStroke(g, PL([[-220, 700], [W + 220, 700]], false), 3); plate(g, 'sepia', a1_rect(-220, 700, W + 220, H + 220), { a: .2 }); // sanat 3. tur: lambri L ≥175
    // kara tahta: ahşap çerçeve, is yüzey
    const fr = a1_rect(500, 90, 1460, 600); knock(g, fr); plate(g, 'sepia', fr, { n: 2 }); inkStroke(g, fr, 3);
    const bd = a1_rect(522, 112, 1438, 578); inkFill(g, bd); plate(g, 'sepia', bd, { a: .25 });
    const r = rng(3); for (let i = 0; i < 18; i++) { const x = 540 + r() * 860, y = 130 + r() * 420; cut(g, PL([[x, y], [x + 30 + r() * 80, y + (r() - .5) * 10]], false), 6 + r() * 8, { a: .05 }); }
    const ledge = a1_rect(490, 600, 1470, 618); knock(g, ledge); plate(g, 'sepia', ledge, { n: 2 }); inkStroke(g, ledge, 2);
    cut(g, a1_rect(600, 604, 640, 612), 2, { a: .8 });
  }));
  // tebeşir geometri: üçgen, çevrel çember, pergel yayları, açı işaretleri (kelimeye bağlı çizilir)
  const p = clamp((t - Tma + .2) / 2.2), seg = (a, b) => clamp((p - a) / (b - a));
  const A = [760, 470], B = [1180, 470], C = [880, 210], O = [970, 380], Rr = Math.hypot(A[0] - O[0], A[1] - O[1]);
  const chalk = (path, len, a, b, w = 4) => { const q = seg(a, b); if (q <= 0) return; ctx.save(); ctx.setLineDash([len * q, 1e5]); cut(ctx, path, w, { a: .9 }); ctx.restore(); };
  ctx.save(); cam(ctx, c, .8);
  chalk(PL([A, B], false), 420, 0, .15); chalk(PL([B, C], false), 410, .12, .27); chalk(PL([C, A], false), 290, .24, .36);
  const circ = new Path2D(); circ.arc(O[0], O[1], Rr, -PI / 2, PI * 1.5); chalk(circ, TAU * Rr, .38, .7, 3);
  for (const [cx, cy, a0] of [[A[0], A[1], -1.4], [B[0], B[1], -1.9]]) { const ar = new Path2D(); ar.arc(cx, cy, 260, a0 - .25, a0 + .25); chalk(ar, 130, .66, .76, 2.4); }
  chalk(PL([[970, 200], [970, 540]], false), 340, .72, .84, 2);
  for (const [v, a0, a1] of [[A, -.55, 0], [B, PI, PI + .55]]) { const ar = new Path2D(); ar.arc(v[0], v[1], 46, a0, a1); chalk(ar, 40, .84, .9, 2.4); }
  if (p > .88) { const q = seg(.88, 1); ctx.save(); ctx.globalAlpha = q; for (const [x, y, sd] of [[A[0] - 20, A[1] + 34, 1], [B[0] + 30, B[1] + 34, 2], [C[0] + 8, C[1] - 18, 3]]) scriptLine(ctx, x + 12, y, 22, 8, 950 + sd, { w: 2.6, col: P.paper }); ctx.restore(); }
  ctx.restore();
  // öğretmen (solda, tahtayı gösterir; "ona" sözünde Mustafa'ya döner) ve Mustafa (ön planda sırada)
  ctx.save(); cam(ctx, c, 1);
  const turned = t > To, lookT = turned ? [1500, 560] : [900, 300];
  a1_fig(ctx, t, { x: 290, y: 300, s: 1.6, dir: 1, who: 'anon', id: { mus: 'pala', beard: null, hair: 'ink', jaw: 1.02, brow: .1, browW: 1.15 }, gear: 'fes', coat: 'setre', col: 'navy', collarCol: 'red', age: 36, lookAt: lookT, len: 520, seed: 51, w: .88, turn: .4, idle: 1.4, tilt: t > Tk ? Math.sin((t - Tk) * 3.2) * .035 : 0,
    under: (by, io) => a1_epaulets(ctx, 290, by, 1.6, 1, .88, .4, io.torso) });
  { // kol: omuz açısı ve dirsek açısı ayrı ayrı canlanır; dirsek hep aynı yana bükülür
    const SH = [290 + 62 * 1.6, 300 + 112 * 1.6], U = 190, F = 176;
    const ik = tg => { const dx = tg[0] - SH[0], dy = tg[1] - SH[1], d = Math.min(Math.hypot(dx, dy), (U + F) * .98), ph = Math.atan2(dy, dx), al = Math.acos(clamp((U * U + d * d - F * F) / (2 * U * d), -1, 1)), ua = ph + al, el = [SH[0] + Math.cos(ua) * U, SH[1] + Math.sin(ua) * U], fa = Math.atan2(SH[1] + Math.sin(ph) * d - el[1], SH[0] + Math.cos(ph) * d - el[0]); return [ua, fa - ua]; };
    const tq = Math.floor(t * 15) / 15, [uA, rA] = ik([760 + Math.sin(tq * 5) * 5, 330 + Math.sin(tq * 7) * 6]), [uB, rB] = ik([640, 640 + Math.sin(tq * 3) * 5]);
    const f = Math.floor((t - To) * 15), D6 = 6 * PI / 180;
    let ua = uA, rel = rA, hk = 'point', ov = 0;
    if (f >= 0 && f < 2) ua = uA - D6 * (f + 1) / 2;
    else if (f >= 2) { const e = E.out2(clamp((f - 1) / 7)); ua = lerp(uA - D6, uB, e); rel = lerp(rA, rB, e); hk = f >= 5 ? 'rest' : 'point'; ov = f === 9 ? .16 : f === 10 ? .07 : 0; }
    const el = [SH[0] + Math.cos(ua) * U, SH[1] + Math.sin(ua) * U], wr = [el[0] + Math.cos(ua + rel) * F, el[1] + Math.sin(ua + rel) * F];
    const Ar = arm(ctx, SH, wr, { upper: U, fore: F, w: 62, col: 'navy', bend: -1 });
    handDraw(ctx, Ar.wr[0], Ar.wr[1], Ar.ang + ov, Ar.w2 / 20, hk, { side: 1 });
  }
  // küçük Mustafa: sıranın arkasında, tahtaya/öğretmene bakar; "Kemal" sözünde başını hafifçe kaldırır
  const kL = ramp(t, Tk, Tk + .35, E.out2);
  a1_kid(ctx, t, { x: 1540, y: 520, s: 1.5, dir: -1, who: 'mk', id: { mus: null }, age: 12, gear: 'fes', col: 'navy', collarCol: 'red', lookAt: turned ? [420, 380] : [900, 340], len: 420, seed: 3, tilt: -.05 * kL });
  // ön sırada iki öğrenci (sırtları, damga siluet)
  const ph2 = Math.floor(t * 6) % 2;
  a1_stampKid(ctx, 560, 1110, 9.5, ph2); a1_stampKid(ctx, 880, 1130, 8.8, 1 - ph2);
  // sıra
  const desk = PL([[1060, 900], [2000, 890], [2000, 1000], [1040, 1010]]); knock(ctx, desk); plate(ctx, 'sepia', desk, { n: 2 }); inkStroke(ctx, desk, 3);
  const top = PL([[1080, 860], [1990, 852], [2000, 892], [1060, 902]]); knock(ctx, top); plate(ctx, 'sepia', top, { a: .7 }); inkStroke(ctx, top, 3);
  const slate = PL([[1250, 872], [1420, 868], [1424, 892], [1246, 896]]); inkFill(ctx, slate); cut(ctx, PL([[1270, 882], [1400, 880]], false), 1.6, { a: .6 });
  ctx.restore();
  // levha ekrana sabit, çocuk Mustafa'nın başının üstünde (sağ kenar 1824)
  const tm = () => a1_tagMorph(ctx, 1824, 190, 'MUSTAFA', 'MUSTAFA KEMAL', '12 yaşında', st.lt - .5, Tk - (st.t - st.lt) - .5);
  if (typeof onScreen === 'function') onScreen(ctx, tm); else tm();
}, { tr: { type: 'cut' } });
