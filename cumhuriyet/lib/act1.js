// act1: I · Sultanın okulları (B01–B06). Yardımcılar a1_ önekli (act3.js de kullanır).
'use strict';

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

// Figür: bust + head3q. Boşta salınım, nefes, göz kırpma; pozlar ikişer karede (15 fps)
function a1_fig(ctx, t, o) {
  const tf = Math.floor(t * 15) / 15, sd = o.seed || 1;
  const io = idleOffsets(tf, sd, o.idle ?? 1), bl = o.blink === false ? 0 : blinkAt(tf, sd);
  const pp = { ...PEOPLE.anon, ...(PEOPLE[o.who] || {}), ...(o.id || {}) };
  const eo = (o.eyeOpen ?? pp.eyeOpen ?? .8) * (1 - .9 * bl);
  const by = o.y + io.breath * .6 * (o.s / 1.2);
  const bs = o.bs ?? o.s;
  if (o.body !== false) bust(ctx, { x: o.x + (o.bdx || 0), y: by + (o.bdy || 0), s: bs, dir: o.dir, coat: o.coat || 'setre', col: o.col || 'ink', w: o.w || 1, len: o.len, seed: sd, tilt: (o.btilt || 0) + io.torso, turn: o.turn, sep: o.sep, back: o.back, arms: o.arms, collarCol: o.collarCol, skin: o.skin });
  if (o.under) o.under(by);
  head3q(ctx, { x: o.x, y: by, s: o.s, dir: o.dir, who: o.who || 'anon', id: o.id, gear: o.gear, gearCol: o.gearCol, light: o.light || 'front', lookAt: o.lookAt, look: o.look, age: o.age, tilt: (o.tilt || 0) + io.head + io.neck * .5, eyeOpen: eo, skin: o.skin, wide: o.wide });
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
  const c = { x: kf(t, [[Tt - .5, 960], [Td + 1, 912]]), y: kf(t, [[Tt - .5, 540], [Td + 1, 508]]), z: kf(t, [[S('B01'), 1], [Tt - .5, 1.025], [Td + 1, 1.07]]) };
  ctx.save(); cam(ctx, c, 1);
  a1_img(ctx, a1_mapUnder());
  const w = (a, b) => E.io2(clamp((t - a) / (b - a)));
  a1_empire(ctx, { L1: w(Tt, Tt + 1.35), L3: w(Tt + .7, Tt + 1.1), L4: w(Tt + .9, Tt + 1.25), L2: w(Tt + 1.35, Tt + 1.7), tunis: w(Tt + 1.6, Tt + 2.0), egypt: w(Tt + 1.8, Tt + 2.4) });
  // 1876 sınırı: silinen toprağın üstünde kesik çizgi olarak kalır
  { const G = a1_geo(); ctx.save(); ctx.setLineDash([7, 6]); for (const p of [G.core, G.libya, G.egypt, G.tunis]) inkStroke(ctx, p, 1.6, { a: .6 }); ctx.restore(); }
  a1_img(ctx, a1_mapTop());
  // kayıp yılları (izleyici katmanı, harita üstünde küçük damga)
  for (const [s, lo, la, tt] of [['1878', 24.3, 43.6, Tt + 1.0], ['1881', 6.9, 34.3, Tt + 1.9], ['1882', 28.6, 26.8, Tt + 2.3]]) { const [x, y] = a1_p(lo, la); stamp(ctx, s, x, y, t - tt, 9, { size: 28, typing: .3, bg: P.paperD }); }
  // borç senetleri: üç tahvil düşer, kırmızı damga yer
  for (let i = 0; i < 3; i++) {
    const t0 = Tb + i * .3, u = clamp((t - t0) / .22); if (u <= 0) continue;
    const e = E.out3(u), dy = (1 - e) * -70 + settle(t, t0 + .22, 6, 3, 9);
    ctx.save(); ctx.globalAlpha = clamp(u * 3);
    a1_bond(ctx, 1500 + i * 95, 720 + i * 52 + dy, 250, 330, -.16 + i * .13, 31 + i * 5, a1_pop(t, t0 + .3));
    ctx.restore();
  }
  ctx.restore();
  chapterCard(ctx, 'I', 'SULTANIN OKULLARI', '1876–1900', lt - .25, 4.6);
}, { tr: { type: 'press', dur: .8 } });
