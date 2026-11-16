// ran_cizim.js: Zaman Kuryesi / Ran için çizim ilkelleri. LemoLab ink-wash motorunun (lib/ink.bundle.js) fırça ilkellerini kullanır.
// Japon suiboku: kale (1870'ler fotoğraflarındaki genel tenshu biçimi; filmin kalesi değil), xieyi figür (yüz yok, makyaj yok), ateş (tek kırmızı).
// Koordinatlar dünya pikseli (1920×1080). L = layerSet() (wet, dry, col).
'use strict';
const RC = (() => {
  const { mk, draw, mass, blot, qpts, TONE } = INK;
  const { clamp, lerp, vnoise } = LIB;
  const VERM = [176, 46, 34], FIRE = [196, 62, 30];
  const S = (L, pts, o) => draw(L.ink || L, mk(pts, o), o.p ?? 1, o.am ?? 1);

  // ---------- Kale (tenshu) ----------
  // x: orta, y: taş temelin altı, s: ölçek (1 → temel genişliği ~460 px). Japon kalesi: alçak, dik içbükey taş temel; ak sıva duvar; koyu, kalkık saçaklı çatılar.
  function castle(L, X) {
    const x = X.x, y = X.y, s = X.s ?? 1, am = X.am ?? 1, sd = X.seed ?? 11;
    const bw = 460 * s, bh = 105 * s, top = 380 * s;
    const base = [];
    for (let i = 0; i <= 10; i++) { const u = i / 10; base.push([x - bw / 2 + (bw - top) / 2 * Math.pow(u, .55), y - bh * u]); }
    for (let i = 10; i >= 0; i--) { const u = i / 10; base.push([x + bw / 2 - (bw - top) / 2 * Math.pow(u, .55), y - bh * u]); }
    mass(L.cw, base, .48 * am, 2 * s, sd);
    for (let k = 0; k < 5; k++) {   // taş dokusu: kırık kuru fırça
      const u = (k + .5) / 5, yy = y - bh * u, hw = bw / 2 - (bw - top) / 2 * Math.pow(u, .55);
      for (let m = 0; m < 4; m++) { const x0 = x - hw + (m + vnoise(k + m * 3) * .4) * hw / 2; S(L, [[x0, yy], [x0 + hw * .35, yy + 1.5]], { w: 3 * s, tone: .55, dry: .85, seed: sd * 50 + k * 7 + m, prof: 'even', am }); }
    }
    S(L, base.slice(0, 11), { w: 10 * s, tone: TONE.nong, dry: .35, seed: sd * 9 + 1, prof: 'robe', am });
    S(L, base.slice(11), { w: 10 * s, tone: TONE.nong, dry: .35, seed: sd * 9 + 2, prof: 'robe', am });
    const tiers = [[top * .86, 96 * s], [top * .64, 84 * s], [top * .44, 76 * s]];
    let yb = y - bh; const win = [];
    tiers.forEach(([w, h], i) => {
      const wh = h * .58;
      // ak sıva duvar: kâğıt kalır; yalnız alt kenar ve köşe direkleri
      mass(L.cw, [[x - w / 2, yb], [x + w / 2, yb], [x + w / 2, yb - wh], [x - w / 2, yb - wh]], .07 * am, 1 * s, sd + i);
      S(L, [[x - w / 2, yb], [x - w / 2, yb - wh]], { w: 4 * s, tone: .6, dry: .5, seed: sd * 60 + i, prof: 'even', am });
      S(L, [[x + w / 2, yb], [x + w / 2, yb - wh]], { w: 4 * s, tone: .6, dry: .5, seed: sd * 61 + i, prof: 'even', am });
      const nw = 4 - i;
      for (let k = 0; k < nw; k++) { const wx = x - w * .34 + k * w * .68 / Math.max(1, nw - 1); win.push([wx, yb - wh * .5]); mass(L.cw, [[wx - 9 * s, yb - wh * .3], [wx + 9 * s, yb - wh * .3], [wx + 9 * s, yb - wh * .7], [wx - 9 * s, yb - wh * .7]], .78 * am, 1 * s, sd + k + i * 7); }
      // çatı: geniş saçak, uçları kalkık; üst yüzey koyu kütle
      const ew = w * .5 + 46 * s, ey = yb - wh, ry = ey - h * .42;
      const roof = [[x - ew - 14 * s, ey - 16 * s], ...qpts(x - ew - 14 * s, ey - 16 * s, x - ew * .6, ey + 4 * s, x, ey + 6 * s, 6).slice(1), ...qpts(x, ey + 6 * s, x + ew * .6, ey + 4 * s, x + ew + 14 * s, ey - 16 * s, 6).slice(1), [x + w * .28, ry], [x - w * .28, ry]];
      mass(L.cw, roof, .74 * am, 2 * s, sd + 30 + i);
      S(L, [[x - ew - 14 * s, ey - 16 * s], [x - ew * .6, ey + 4 * s], [x, ey + 6 * s], [x + ew * .6, ey + 4 * s], [x + ew + 14 * s, ey - 16 * s]], { w: 9 * s, tone: TONE.jiao, dry: .3, seed: sd * 70 + i, prof: 'tip', darkDir: [0, 1], am });
      if (i < 2) { const gx = x + (i ? -1 : 1) * w * .16; mass(L.cw, [[gx - 30 * s, ey - 6 * s], [gx, ey - 34 * s], [gx + 30 * s, ey - 6 * s]], .8 * am, 1, sd + 90 + i); }
      yb = ry;
    });
    S(L, [[x - top * .14, yb + 2], [x + top * .14, yb + 2]], { w: 8 * s, tone: TONE.jiao, dry: .2, seed: sd * 99, prof: 'even', am });
    return { top: yb, base: y - bh, bw, x, win };
  }

  // ---------- Ateş: col katmanında tek kırmızı ----------
  // pts: [[x, y, r]] alev kaynakları; k: şiddet; t: zaman (alev 12 fps adım). Alev dilleri sivri, birbirine karışan, yukarı yalayan.
  function fire(L, pts, k, t) {
    const c = L.cc, tq = Math.floor(t * 12) / 12;
    c.save(); c.globalCompositeOperation = 'source-over';
    for (const [x, y, r] of pts) {
      const g = c.createRadialGradient(x, y - r, 0, x, y - r, r * 4.5);
      g.addColorStop(0, `rgba(${FIRE},${.36 * k})`); g.addColorStop(1, `rgba(${FIRE},0)`);
      c.fillStyle = g; c.fillRect(x - r * 4.5, y - r * 5.5, r * 9, r * 9);
      const N = 9;
      for (let j = 0; j < N; j++) {
        const u = j / (N - 1) - .5, ph = vnoise(x * .013 + j * 2.7 + tq * 1.9);
        const hgt = r * (2.2 + 3.2 * ph) * k * (1 - Math.abs(u) * .9), bx = x + u * r * 2.2, bw = r * (.45 + .3 * (1 - Math.abs(u)));
        const sway = (vnoise(j * 5.7 + tq * 2.6) - .5) * r * 1.1, lean = sway + u * r * .5;
        c.beginPath(); c.moveTo(bx - bw, y);
        c.bezierCurveTo(bx - bw * 1.1, y - hgt * .35, bx + lean * .4 - bw * .4, y - hgt * .7, bx + lean, y - hgt);
        c.bezierCurveTo(bx + lean * .4 + bw * .3, y - hgt * .7, bx + bw * 1.1, y - hgt * .35, bx + bw, y);
        c.closePath(); c.fillStyle = `rgba(${FIRE},${(.42 + .4 * ph) * k})`; c.fill();
      }
      for (let e = 0; e < 5; e++) {   // kıvılcım
        const v = (vnoise(e * 9.1 + x) + tq * .4) % 1, ex = x + (vnoise(e * 3.3 + x * .1) - .5) * r * 3, ey = y - r * 3 - v * r * 6;
        c.fillStyle = `rgba(${FIRE},${(1 - v) * .8 * k})`; c.fillRect(ex, ey, 3, 3);
      }
    }
    c.restore();
  }
  // duman: ıslak katmanda yükselen kütleler (bleed ile yayılır)
  function smoke(L, x, y, w, h, t, am = 1, sd = 3) {
    for (let j = 0; j < 9; j++) {
      const u = ((j / 9) + t * .035) % 1, yy = y - u * h, xx = x + (vnoise(j * 2.3 + sd) - .5) * w + u * w * .5;
      blot(L.cw, xx, yy, (40 + 90 * u) * (w / 300), .22 * am * Math.sin(Math.PI * u), vnoise(j) * 3, .55, sd + j);
    }
  }

  // ---------- Xieyi figür ----------
  // X: {x, y (ayak), s (1 → boy ~110 px), dir (1 sağa), pose: 'walk'|'stand'|'sit'|'kneel', t, am, seed, hair: 'old'|'young'|'none', bowed: 0..1}
  function figure(L, X) {
    const x = X.x, y = X.y, s = X.s ?? 1, d = X.dir ?? 1, am = X.am ?? 1, sd = X.seed ?? 5, t = X.t ?? 0, bow = X.bowed ?? 0;
    const tq = Math.floor(t * 12) / 12, H = 110 * s;
    const P = ([px, py]) => [x + px * s * d, y + py * s];
    const pose = X.pose || 'stand';
    let hipY = -52, shX = 4 + bow * 10, shY = -86 + bow * 10, hem = -6;
    if (pose === 'sit') { hipY = -18; shY = -58 + bow * 8; hem = -2; }
    if (pose === 'kneel') { hipY = -26; shY = -66 + bow * 8; hem = -2; }
    const sw = pose === 'walk' ? Math.sin(tq * Math.PI * 1.6) : 0;
    // cüppe kütlesi (soluk) — hakama'nın geniş eteği
    const robe = pose === 'sit' || pose === 'kneel'
      ? [[shX - 8, shY], [shX + 10, shY + 2], [22, hipY + 4], [34, hem], [-24, hem], [-14, hipY]]
      : [[shX - 9, shY], [shX + 9, shY + 2], [12, hipY], [20 + sw * 4, hem], [-22 + sw * 3, hem], [-10, hipY]];
    mass(L.cw, robe.map(P), .3 * am, 1.6 * s, sd);
    // iki yüklü kontur: sırt ve ön
    S(L, [[shX - 9, shY], [-12, (shY + hipY) / 2], robe[5].slice(0, 2), robe[4].slice(0, 2)].map(P), { w: 9 * s, tone: TONE.nong, dry: .3, seed: sd * 31 + 1, prof: 'robe', darkDir: [-d, 0], am });
    S(L, [[shX + 9, shY + 2], robe[2].slice(0, 2), robe[3].slice(0, 2)].map(P), { w: 6 * s, tone: TONE.zhong, dry: .4, seed: sd * 31 + 2, prof: 'brush', am });
    // kol / yen: tek darbe
    const arm = pose === 'sit' ? [[shX + 6, shY + 4], [20, shY + 26], [26, hipY - 2]] : [[shX + 6, shY + 4], [12 + sw * 3, shY + 30], [14 + sw * 4, hipY + 6]];
    S(L, arm.map(P), { w: 10 * s, tone: TONE.zhong, dry: .45, seed: sd * 31 + 3, prof: 'lens', am });
    // bacaklar (yalnız yürürken etek altında iki kısa darbe)
    if (pose === 'walk') {
      S(L, [[-2, hem - 6], [6 + sw * 9, -1]].map(P), { w: 4 * s, tone: TONE.nong, dry: .3, seed: sd * 31 + 4, prof: 'nail', am });
      S(L, [[-6, hem - 6], [-8 - sw * 9, -1]].map(P), { w: 4 * s, tone: TONE.nong, dry: .3, seed: sd * 31 + 5, prof: 'nail', am });
    }
    // baş: soluk leke + saç (yaşlı: kuru açık gri tepe topuzu; genç: koyu topuz). Yüz çizilmez.
    const hx = shX + 3 + bow * 6, hy = shY - 12 + bow * 4;
    blot(L.cw, ...P([hx, hy]), 8.5 * s, (X.headTone ?? .2) * am, 0, 1.15, sd);
    if (X.hair !== 'none') {
      const old = X.hair === 'old';
      S(L, [[hx - 7, hy - 3], [hx - 2, hy - 10], [hx + 5, hy - 7]].map(P), { w: 5 * s, tone: old ? .3 : TONE.nong, dry: old ? .85 : .3, seed: sd * 31 + 6, prof: 'lens', am });
      S(L, [[hx - 3, hy - 10], [hx - 1, hy - 15]].map(P), { w: 4 * s, tone: old ? .32 : TONE.jiao, dry: old ? .8 : .2, seed: sd * 31 + 7, prof: 'dot', am });
    }
    return { head: P([hx, hy]), hand: P(arm[arm.length - 1]), H };
  }

  // ---------- Yan flüt (yokobue) ve eller: yakın plan ----------
  // Eller xieyi: avuç = soluk kütle + koyu yüklü kenar; parmaklar flütün üstünden kıvrılan darbeler. Kollar alttan giren koyu yen kütleleri.
  function fluteClose(L, X) {
    const x = X.x, y = X.y, s = X.s ?? 1, am = X.am ?? 1, t = X.t ?? 0, sd = X.seed ?? 21;
    const a = -.16, len = 1300 * s, ca = Math.cos(a), sa = Math.sin(a);
    const Q = u => [x + ca * len * u, y + sa * len * u];
    const N = [-sa, ca];   // flütün altına bakan normal
    // yenler (kollar): alttan giren iki büyük koyu kütle
    for (const [u, k] of [[.3, 0], [.62, 1]]) {
      const [px, py] = Q(u);
      mass(L.cw, [[px - 230 * s, 1180], [px - 120 * s, py + 150 * s], [px + 40 * s, py + 120 * s], [px + 150 * s, 1180]], .55 * am, 6 * s, sd + 60 + k, [0, py + 100 * s, 0, 1100, .75, 1]);
      S(L, [[px - 210 * s, 1150], [px - 120 * s, py + 160 * s], [px - 20 * s, py + 130 * s]], { w: 26 * s, tone: TONE.nong, dry: .45, seed: sd + 70 + k, prof: 'robe', am });
    }
    // gövde: bambu
    S(L, [Q(-.02), Q(.5), Q(1.02)], { w: 34 * s, tone: TONE.zhong, dry: .25, seed: sd, prof: 'even', darkDir: N, am });
    S(L, [Q(0), Q(1)].map(([px, py]) => [px - N[0] * 13 * s, py - N[1] * 13 * s]), { w: 5 * s, tone: TONE.nong, dry: .55, seed: sd + 1, prof: 'even', am });
    for (const u of [.12, .5, .9]) { const [px, py] = Q(u); S(L, [[px + N[0] * -20 * s, py - 20 * s * N[1]], [px + N[0] * 20 * s, py + 20 * s * N[1]]], { w: 7 * s, tone: TONE.jiao, dry: .2, seed: sd + 10 + u * 9, prof: 'dot', am }); }
    for (let k = 0; k < 7; k++) { const [px, py] = Q(.22 + k * .065); blot(L.cw, px - N[0] * 4 * s, py - N[1] * 4 * s, 6 * s, .92 * am, a, .6, sd + k); }
    // eller
    for (const [u, k] of [[.3, 0], [.62, 1]]) {
      const [px, py] = Q(u);
      const palm = [[px - 120 * s, py + 150 * s], [px - 70 * s, py + 30 * s], [px + 70 * s, py + 22 * s], [px + 60 * s, py + 110 * s], [px + 20 * s, py + 140 * s]];
      mass(L.cw, palm, .2 * am, 4 * s, sd + 40 + k);
      S(L, [palm[0], palm[1], [px - 20 * s, py + 22 * s]], { w: 14 * s, tone: TONE.zhong, dry: .4, seed: sd + 44 + k, prof: 'brush', darkDir: [-1, 0], am });
      for (let f = 0; f < 4; f++) {   // parmaklar: flütün üstünden kıvrılır; ortadaki ikisi ezgiyle kalkar
        const fx = px - 50 * s + f * 36 * s, play = X.play && (f === 1 || f === 2) ? Math.max(0, Math.sin(Math.floor(t * 6) * 1.9 + f + k * 2)) : 0, lift = play * 16 * s;
        S(L, [[fx, py + 40 * s], [fx + 4 * s, py - 6 * s - lift], [fx + 22 * s, py - 24 * s - lift], [fx + 34 * s, py - 10 * s - lift * .6]], { w: 15 * s, tone: TONE.zhong, dry: .35, seed: sd + 50 + f + k * 10, prof: 'press', darkDir: [0, -1], am });
      }
      // başparmak: alttan
      S(L, [[px - 70 * s, py + 80 * s], [px - 30 * s, py + 34 * s], [px + 6 * s, py + 26 * s]], { w: 14 * s, tone: TONE.zhong, dry: .35, seed: sd + 58 + k, prof: 'nail', am });
    }
  }

  // ---------- Arazi yardımcıları ----------
  function ground(L, y0, x0, x1, am = 1, sd = 7) {
    S(L, [[x0, y0], [lerp(x0, x1, .35), y0 - 6], [lerp(x0, x1, .7), y0 + 4], [x1, y0 - 2]], { w: 7, tone: TONE.zhong, dry: .7, seed: sd, prof: 'even', am });
    for (let k = 0; k < 12; k++) { const gx = lerp(x0, x1, (k + .5) / 12) + (vnoise(k * 3 + sd) - .5) * 60; S(L, [[gx, y0 + 8 + k % 3 * 6], [gx + 40 + vnoise(k) * 50, y0 + 10 + k % 3 * 6]], { w: 3, tone: .3, dry: .85, seed: sd * 10 + k, prof: 'tip', am }); }
  }
  return { castle, fire, smoke, figure, fluteClose, ground, VERM, FIRE, S };
})();
window.RC = RC;
