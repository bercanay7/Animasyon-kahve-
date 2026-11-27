// Masadaki nesneler fırça darbesi olarak (canlı katman): zarf, banknot, bilet, kâğıt, defter, dergi, telgraf, cilt, kalem.
// Nesne: {tur, x, y, w, h, rot (radyan), renk: 'sari' | 'gri' | [r,g,b], kalk (0..1: havada, gölge uzar), a (saydamlık), tohum, yazi (0..1: el yazısı payı), acik (zarf kapağı)}
// Hassasiyet: zarf kapağı yalnız V (çarpı yok); banknotta halka ya da madalyon yok (halka tarama = hedef); kâğıtta okunur yazı yok.
import { BRUSH, KNIFE, DAB } from '../../araclar/tablo/impasto.js';
import { hsh, clamp } from './film_t.js';
import { mx, ekrana, MW } from './film_t.js';
export const RENK = { sari: [.86, .66, .3], sari2: [.84, .6, .18], gri: [.74, .71, .64], kagit: [.9, .86, .76], murekkep: [.16, .13, .12], banknot: [.66, .62, .52], bilet: [.7, .66, .58], defter: [.28, .2, .15], dergi: [.8, .77, .7], cilt: [.32, .24, .18] };
const rot = (it, u, v) => { const c = Math.cos(it.rot || 0), s = Math.sin(it.rot || 0); return [it.x + u * c - v * s, it.y + u * s + v * c]; };
// dikdörtgen gövde: uzun eksene paralel üst üste binen darbeler
function govde(S, it, c, o = {}) {
  // üst üste binen, yönü ve tonu hafif oynayan darbeler; kenarda saydamlaşır (kesik bant değil, boyanmış kâğıt)
  const w = it.w, h = it.h, sd = it.tohum || 0, al = (it.a ?? 1) * (o.a ?? 1), wid = o.wid || Math.max(8, Math.min(26, h / 3.2));
  const ton = 1 + (hsh(sd, 91) - .5) * (o.tonOyna ?? .12), sic = (hsh(sd, 92) - .5) * .05;   // nesneye özgü ton ve sıcaklık
  { const [x, y] = rot(it, 0, 0); S.push({ x, y, ang: it.rot || 0, len: w * .985, wid: h * .985, c: c.map(q => q * ton * .97), c2: c.map(q => q * ton * .94), seed: sd * 17 + 3, type: KNIFE, alpha: al, hgt: (o.hgt ?? .3) * .6 }); }   // v3: alt kat (darbe aralığından gölge sızıp kenarı tırtıklı gösteriyordu)
  const sat = Math.max(2, Math.ceil(h / (wid * .62))), uz = Math.max(30, Math.min(140, w * .55)), n = Math.max(2, Math.ceil(w / (uz * .62)));
  for (let j = 0; j < sat; j++) for (let i = 0; i < n; i++) {
    // v3: satırlar kayık, boylar düzensiz (tuğla dizisi okunuyordu)
    const Ls = Math.min(w * .96, w / n * (1.15 + .5 * hsh(sd, i + 3, j))), u = clamp(-w / 2 + (i + .5 + (j % 2 ? .5 : 0) * (hsh(sd, j, 5) + .3)) * w / n + (hsh(sd, i, j) - .5) * w / n * .6, -w / 2 + Ls / 2, w / 2 - Ls / 2), v = clamp(-h / 2 + (j + .5) * h / sat + (hsh(sd, j, i + 9) - .5) * h / sat * .4, -h / 2 + wid * .45, h / 2 - wid * .45);
    const kenarda = Math.max(Math.abs(u) / (w / 2), Math.abs(v) / (h / 2));
    const [x, y] = rot(it, u, v), k = ton * (1 + (hsh(sd, i * 3, j) - .5) * .05), isik = o.isik ? o.isik(u / w, v / h) : 1;
    const cc = [c[0] * k * isik + sic, c[1] * k * isik, c[2] * k * isik - sic].map(q => clamp(q));
    S.push({ x, y, ang: (it.rot || 0) + (hsh(sd, i, j + 4) - .5) * .05, len: Ls, wid: wid * (.85 + .25 * hsh(sd, i, j + 7)), c: cc, c2: cc.map(q => clamp(q * (.9 + .08 * hsh(sd, j, i)))), seed: sd * 31 + i * 7 + j, type: o.tip ?? KNIFE, alpha: al * (kenarda > .85 ? .9 : 1), hgt: o.hgt ?? .3 });
  }
}
function kenar(S, it, c, k = .78) {
  const w = it.w, h = it.h, sd = it.tohum || 0, al = (it.a ?? 1) * .8;
  for (const [u0, v0, u1, v1] of [[-w / 2, -h / 2, w / 2, -h / 2], [w / 2, -h / 2, w / 2, h / 2], [w / 2, h / 2, -w / 2, h / 2], [-w / 2, h / 2, -w / 2, -h / 2]]) {
    const L = Math.hypot(u1 - u0, v1 - v0), n = Math.max(1, Math.round(L / 40));
    for (let i = 0; i < n; i++) { const a = (i + .5) / n, [x, y] = rot(it, u0 + (u1 - u0) * a, v0 + (v1 - v0) * a);   // v3: boşluksuz (kesik koyu kenar tırtıklı okunuyordu)
      S.push({ x, y, ang: (it.rot || 0) + Math.atan2(v1 - v0, u1 - u0), len: L / n * 1.08, wid: 1.5, c: c.map(q => q * k), c2: c.map(q => q * k * .9), seed: sd * 13 + i, type: KNIFE, alpha: al, hgt: .25 }); }
  }
}
function cizgi(S, it, u0, v0, u1, v1, c, w = 2, al = .8, sd = 0) {
  const [x0, y0] = rot(it, u0, v0), [x1, y1] = rot(it, u1, v1), L = Math.hypot(x1 - x0, y1 - y0);
  S.push({ x: (x0 + x1) / 2, y: (y0 + y1) / 2, ang: Math.atan2(y1 - y0, x1 - x0), len: L, wid: w, c, c2: c, seed: sd, type: KNIFE, alpha: al * (it.a ?? 1), hgt: .15, taper: .3 });
}
// el yazısı: dalgalı kısa mürekkep darbeleri, satır satır (okunmaz)
function yazi(S, it, satir, pay = 1, olc = 1, akis = null) {
  const w = it.w, h = it.h, sd = it.tohum || 0, c = RENK.murekkep;
  for (let j = 0; j < satir; j++) {
    const v = -h / 2 + h * (j + 1) / (satir + 1), uzun = (.55 + .4 * hsh(sd, j)) * w * .85; let u = -w * .42;
    const pj = akis == null ? pay : clamp(akis * satir - j); if (pj <= 0) break;   // v3: akış: satır satır dolar
    while (u < -w * .42 + uzun * pj) { const L = (10 + 18 * hsh(sd, j, u)) * olc; cizgi(S, it, u, v + (hsh(u, sd, j) - .5) * 2, u + L, v + (hsh(u + 1, sd, j) - .5) * 3, c, 1.6 * olc, .75, sd * 7 + j * 31 + u); u += L + 5 * olc; }
  }
}
function golge(S, it) {
  if (!it.kalk && !it.golge) return;
  const k = it.kalk || 0, [x, y] = [it.x + 8 + 30 * k, it.y + 10 + 40 * k], a0 = (.32 - .2 * k) * (it.a ?? 1);
  // v3: yuvarlak DAB kâğıdın arkasından yarım daire disk taşırıyordu; dikdörtgen, kenara doğru üç kat
  for (const [p, f] of [[0, .45], [10, .3], [22, .2]]) S.push({ x: x + p / 2, y: y + p / 2, ang: it.rot || 0, len: it.w * (1 + .1 * k) + p, wid: it.h * (1 + .1 * k) + p, c: [.05, .04, .035], c2: [.05, .04, .035], seed: (it.tohum || 0) + 77 + p, type: KNIFE, alpha: a0 * f, hgt: 0 });
}
export function nesne(S, it) {
  if ((it.a ?? 1) <= .01) return;
  golge(S, it);
  const t = it.tur;
  if (it.kalinlik !== false && (t === 'zarf' || t === 'defter' || t === 'cilt')) { const [x, y] = rot(it, 2, it.h / 2 + 3); S.push({ x, y, ang: it.rot || 0, len: it.w * .98, wid: 6, c: [.12, .09, .07], c2: [.1, .08, .06], seed: (it.tohum || 0) + 5, type: BRUSH, alpha: .7 * (it.a ?? 1), hgt: .3 }); }
  if (t === 'zarf') {
    const c = it.renk === 'sari' ? RENK.sari : it.renk === 'gri' ? RENK.gri : it.renk || RENK.gri;
    govde(S, it, c, { isik: (u, v) => 1 - .06 * v });
    kenar(S, it, c, .7);
    // kapak: V (ön yüzde adres; arka yüzde V kapak). it.yuz: 'on' | 'arka'
    if (it.yuz === 'arka') { const w = it.w, h = it.h, cc = c.map(q => q * .72); cizgi(S, it, -w / 2, -h / 2, 0, h * .08, cc, 2.4, .8, 1); cizgi(S, it, w / 2, -h / 2, 0, h * .08, cc, 2.4, .8, 2); }
    else { const w = it.w, h = it.h; const sub = { ...it, w: w * .5, h: h * .45, x: rot(it, w * .08, h * .08)[0], y: rot(it, w * .08, h * .08)[1] }; yazi(S, sub, 3, it.yazi ?? 1, .8);
      const [px, py] = rot(it, w * .36, -h * .3); S.push({ x: px, y: py, ang: it.rot || 0, len: w * .1, wid: h * .2, c: c.map(q => q * .8), c2: c.map(q => q * .74), seed: 5, type: KNIFE, alpha: .75 * (it.a ?? 1), hgt: .3 }); }   // pul (dikdörtgen, damgasız)
  } else if (t === 'banknot') {
    govde(S, it, RENK.banknot, { wid: 6 }); kenar(S, it, RENK.banknot, .72);
    const w = it.w, h = it.h, cc = RENK.banknot.map(q => q * .72);   // iç çerçeve (dikdörtgen), köşede yazı dokusu; madalyon yok
    for (const [a, b, c2, d] of [[-.42, -.36, .42, -.36], [.42, -.36, .42, .36], [.42, .36, -.42, .36], [-.42, .36, -.42, -.36]]) cizgi(S, it, w * a, h * b, w * c2, h * d, cc, 1.6, .6);
    yazi(S, { ...it, w: w * .5, h: h * .4 }, 2, .7, .7);
  } else if (t === 'bilet') {
    govde(S, it, RENK.bilet, { wid: 5 }); kenar(S, it, RENK.bilet, .7); yazi(S, { ...it, w: it.w * .7, h: it.h * .6 }, 2, .8, .6);
  } else if (t === 'kagit' || t === 'telgraf') {
    govde(S, it, t === 'telgraf' ? [.8, .76, .66] : RENK.kagit); kenar(S, it, RENK.kagit, .85);
    yazi(S, it, it.satir ?? Math.max(3, Math.round(it.h / 26)), it.yazi ?? 1, it.olc ?? 1, it.akis ?? null);
  } else if (t === 'defter' || t === 'cilt' || t === 'dergi') {
    const c = RENK[t]; govde(S, it, c, { wid: 10, hgt: .5 }); kenar(S, it, c, .65);
    if (t === 'dergi') { yazi(S, { ...it, h: it.h * .9 }, 7, 1, .7); cizgi(S, it, -it.w * .45, -it.h * .4, it.w * .45, -it.h * .4, RENK.murekkep, 4, .8); }
    if (t === 'cilt' && it.sirt) cizgi(S, it, -it.w * .3, 0, it.w * .3, 0, [.75, .66, .42], 2.2, .8);   // sırt yazısı yerine ince altın çizgi
  } else if (t === 'acikdefter') {
    const L = { ...it, w: it.w / 2, x: rot(it, -it.w / 4, 0)[0], y: rot(it, -it.w / 4, 0)[1] }, Rr = { ...it, w: it.w / 2, x: rot(it, it.w / 4, 0)[0], y: rot(it, it.w / 4, 0)[1] };
    govde(S, L, RENK.kagit); govde(S, Rr, RENK.kagit); kenar(S, it, RENK.kagit, .75);
    yazi(S, L, it.satirL ?? 10, 1, .8, it.akisL ?? null); if (it.satirR) yazi(S, Rr, it.satirR, it.yazi ?? 1, .8, it.akis ?? null);
    cizgi(S, it, 0, -it.h / 2, 0, it.h / 2, [.5, .45, .38], 2, .6);
  } else if (t === 'cerceve') {
    // v3: duvardaki çerçeveli tablo (gri, adlandırılmaz): koyu çerçeve + boyalı yüz (yatay ve dikey düzensiz darbeler; halka ya da çapraz yok)
    const c = it.ic || [.5, .48, .44]; govde(S, it, c, { wid: Math.max(6, it.h / 9), tonOyna: .3, hgt: .45 });
    for (let q = 0; q < 6; q++) { const [x, y] = rot(it, (hsh(it.tohum, q) - .5) * it.w * .7, (hsh(it.tohum, q, 2) - .5) * it.h * .6); S.push({ x, y, ang: (it.rot || 0) + (hsh(q, it.tohum) - .5) * .6, len: it.w * (.15 + .2 * hsh(q, 3)), wid: it.h * .08, c: c.map(v => v * (.7 + .5 * hsh(q, it.tohum, 4))), seed: it.tohum * 9 + q, type: BRUSH, alpha: .8 * (it.a ?? 1), hgt: .4 }); }
    const f = it.cer ?? Math.max(8, it.w * .06), cc = [.16, .12, .09], w = it.w, h = it.h;
    for (const [u0, v0, u1, v1] of [[-w / 2, -h / 2, w / 2, -h / 2], [w / 2, -h / 2, w / 2, h / 2], [w / 2, h / 2, -w / 2, h / 2], [-w / 2, h / 2, -w / 2, -h / 2]]) cizgi(S, it, u0, v0, u1, v1, cc, f, 1, it.tohum + u0);
  } else if (t === 'tuvalsirt') {
    // v3: tuvalin arkası: açık keten + yalnız çevre çıtası (ara çıta yok: çapraz çıta haç okunur)
    govde(S, it, [.72, .66, .55], { wid: Math.max(6, it.h / 8), tonOyna: .1 }); const f = Math.max(5, it.w * .07), cc = [.42, .33, .23], w = it.w, h = it.h;
    for (const [u0, v0, u1, v1] of [[-w / 2 + f / 2, -h / 2 + f / 2, w / 2 - f / 2, -h / 2 + f / 2], [w / 2 - f / 2, -h / 2 + f / 2, w / 2 - f / 2, h / 2 - f / 2], [w / 2 - f / 2, h / 2 - f / 2, -w / 2 + f / 2, h / 2 - f / 2], [-w / 2 + f / 2, h / 2 - f / 2, -w / 2 + f / 2, -h / 2 + f / 2]]) cizgi(S, it, u0, v0, u1, v1, cc, f, 1, it.tohum + v0);
  } else if (t === 'kitap') {
    // v3: tepeden kitap: sayfa bloğu (sağ ve alt kenarda krem şerit), cilt kapağı, solda koyu sırt ve iki altın bant (tek çizgili koyu levha kara tahta okunuyordu)
    const w = it.w, h = it.h, sb = { ...it, x: rot(it, 7, 7)[0], y: rot(it, 7, 7)[1] }; govde(S, sb, [.86, .82, .72], { wid: 8, tonOyna: .05 }); kenar(S, sb, [.86, .82, .72], .6);
    const c = it.renkK || [.42, .3, .22]; govde(S, it, c, { wid: Math.max(8, h / 6), hgt: .5 }); kenar(S, it, c, .6);
    const sw = w * .12, [sx, sy] = rot(it, -w / 2 + sw / 2, 0); S.push({ x: sx, y: sy, ang: (it.rot || 0) + Math.PI / 2, len: h * .98, wid: sw, c: c.map(v => v * .6), c2: c.map(v => v * .52), seed: (it.tohum || 0) + 3, type: KNIFE, alpha: it.a ?? 1, hgt: .55 });
    for (const v of [-.3, .3]) cizgi(S, it, -w / 2 + 2, h * v, -w / 2 + sw - 2, h * v, [.78, .64, .36], 4, .9, it.tohum + v * 9);
    if (it.serit) { const [bx, by] = rot(it, w * .2, h / 2 + 22); S.push({ x: bx, y: by, ang: (it.rot || 0) + Math.PI / 2, len: 54, wid: 22, c: RENK.kagit, c2: RENK.kagit.map(v => v * .9), seed: it.tohum + 8, type: KNIFE, alpha: it.serit, hgt: .3 }); }   // ayraç: çevrilen cilt
  } else if (t === 'kalem') {
    cizgi(S, it, -it.w / 2, 0, it.w / 2, 0, [.22, .17, .13], 6, 1); cizgi(S, it, it.w / 2, 0, it.w / 2 + 14, 0, [.1, .09, .08], 3, 1);
  }
}
// örtü: renkli nesnenin dönük dikdörtgeni (c: katman kamerası)
export function nesneMaske(c, it, a = 1) {
  if (a <= 0) return; const k = MW / 1920, pts = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([u, v]) => ekrana(c, ...rot(it, u * (it.w / 2 + 6), v * (it.h / 2 + 8))));
  mx.save(); mx.globalAlpha = clamp(a * (it.a ?? 1)); mx.filter = 'blur(2.5px)'; mx.fillStyle = '#fff'; mx.beginPath(); pts.forEach(([x, y], i) => (i ? mx.lineTo(x * k, y * k) : mx.moveTo(x * k, y * k))); mx.closePath(); mx.fill(); mx.restore();
}
