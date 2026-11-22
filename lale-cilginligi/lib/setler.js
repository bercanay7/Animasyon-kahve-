// Mekânlar (gravür dili; milton/lib/gravur.js). Klasik betik. Hepsi dünya koordinatında (1920×1080 sahne), GR.begin/engrave arasında çağrılır.
// Değer kuralı (milton KILAVUZ): üç değer; koyu kütleler düz siyah, ışık yalnız kaynağın çevresinde. Renk yalnız lalede (LALE.boya).
'use strict';
const SET = (() => {
  const PI = Math.PI, { F, Sm, fill } = INSAN;
  const H0 = 0, HV = PI / 2;
  const R = (x, y, w, h) => F([[x, y], [x + w, y], [x + w, y + h], [x, y + h]]);
  const E2 = (x, y, rx, ry, r = 0) => { const p = new Path2D(); p.ellipse(x, y, rx, ry, r, 0, PI * 2); return p; };
  const rnd = s => { const x = Math.sin(s * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  function isik(L) {
    const tx = GR.tx; tx.save(); tx.globalCompositeOperation = 'screen';
    const g = tx.createRadialGradient(L.x, L.y, L.r0 || 10, L.x, L.y, L.r1);
    const a = L.a ?? 1; g.addColorStop(0, `rgba(255,255,255,${.85 * a})`); g.addColorStop(.25, `rgba(255,255,255,${.42 * a})`); g.addColorStop(.6, `rgba(255,255,255,${.12 * a})`); g.addColorStop(1, 'rgba(255,255,255,0)');
    tx.fillStyle = g; tx.fillRect(L.x - L.r1, L.y - L.r1, L.r1 * 2, L.r1 * 2); tx.restore();
  }
  function huzme(pts, a = .5) { const tx = GR.tx; tx.save(); tx.globalCompositeOperation = 'screen'; tx.fillStyle = `rgba(255,255,255,${a})`; tx.fill(F(pts)); tx.restore(); }
  function alev(x, y, t, s = 1) {
    const f = 1 + .12 * Math.sin(t * 9.1) + .07 * Math.sin(t * 15.7 + 1.3), ln = .08 * Math.sin(t * 3.7), p = new Path2D();
    p.moveTo(x - 9 * s, y + 8); p.bezierCurveTo(x - 12 * s, y - 10 * s * f, x + ln * 60, y - 30 * s * f, x + ln * 80, y - 46 * s * f);
    p.bezierCurveTo(x + 12 * s, y - 24 * s * f, x + 11 * s, y - 6 * s, x + 9 * s, y + 8); p.closePath();
    GR.fill(p, GR.tone(1), { th: HV, id: 3 });
  }
  function mum(x, y, t, s = 1) { fill(R(x - 6 * s, y, 12 * s, 40 * s), .85, { th: HV, id: 9 }); alev(x, y, t, s * .7); }
  // ── HOLLANDA ──
  // basamaklı alınlıklı kanal evi (trapgevel); x sol, y taban, w genişlik, h gövde boyu; o.ton cephe, o.pen pencere ışığı
  function ev(x, y, w, h, o = {}) {
    const st = o.basamak ?? 4, gh = h * .55, ton = o.ton ?? .55;
    const pts = [[x, y], [x, y - h]]; const sw = w / (st * 2 + 1);
    for (let i = 0; i < st; i++) { const yy = y - h - gh * (i / st), yy2 = y - h - gh * ((i + 1) / st); pts.push([x + sw * i, yy2], [x + sw * (i + 1), yy2]); }
    pts.push([x + w - sw * st, y - h - gh]);
    for (let i = st - 1; i >= 0; i--) { const yy2 = y - h - gh * ((i + 1) / st), yy = y - h - gh * (i / st); pts.push([x + w - sw * (i + 1), yy2], [x + w - sw * i, yy2], [x + w - sw * i, yy]); }
    pts.push([x + w, y - h], [x + w, y]);
    fill(F(pts), ton, { th: HV, id: 9 });
    // tuğla sıraları (ince koyu çizgiler)
    for (let yy = y - 18; yy > y - h; yy -= 22) fill(R(x + 2, yy, w - 4, 2.5), ton - .22, { th: H0, id: 9 });
    // pencereler: kurşunlu camlar
    const nc = Math.max(2, Math.round(w / 70)), cw = w / nc;
    for (let r = 0; r < Math.floor(h / 120); r++) for (let c = 0; c < nc; c++) {
      const px = x + c * cw + cw * .2, py = y - h + 40 + r * 120, pw = cw * .6, ph = 80;
      const lit = o.pen && rnd(x + r * 7 + c) < o.pen;
      fill(R(px, py, pw, ph), lit ? .92 : .08, { th: HV, id: lit ? 10 : 9 });
      fill(R(px + pw / 2 - 2, py, 4, ph), .35, { th: HV, id: 9 }); fill(R(px, py + ph / 2 - 2, pw, 4), .35, { th: H0, id: 9 });
    }
    // çatı penceresi / vinç kancası
    fill(R(x + w / 2 - 14, y - h - gh * .72, 28, 40), .05, { th: HV, id: 9 });
    fill(R(x + w / 2 - 3, y - h - gh * .92, 6, 22), .1, { th: HV, id: 9 });
    // kapı
    if (o.kapi !== false) fill(Sm([[x + w * .4, y], [x + w * .4, y - 90], [x + w * .5, y - 104], [x + w * .6, y - 90], [x + w * .6, y]]), .05, { th: HV, id: 9 });
  }
  // gökyüzü + uzak ufuk; o.gun (1 gündüz .. 0 gece)
  function gok(o = {}) {
    const g = o.gun ?? 1;
    fill(R(-600, -500, 3100, 1300), .86 * g + .04, { th: -.05, id: 10 });
    if (g > .5) for (let i = 0; i < 5; i++) { const cx = 200 + i * 420 + rnd(i) * 140, cy = 140 + rnd(i + 3) * 120; fill(Sm([[cx - 160, cy + 30], [cx - 120, cy - 20], [cx - 40, cy - 46], [cx + 60, cy - 40], [cx + 150, cy - 6], [cx + 170, cy + 30]]), .72, { type: 'rad', cx, cy: cy + 60, id: 2 }); }
  }
  // yel değirmeni (uzak): x, y taban, s ölçek, a kanat açısı
  function degirmen(x, y, s, a) {
    fill(F([[x - 30 * s, y], [x - 18 * s, y - 150 * s], [x + 18 * s, y - 150 * s], [x + 30 * s, y]]), .12, { th: HV, id: 9 });
    fill(F([[x - 24 * s, y - 150 * s], [x, y - 180 * s], [x + 24 * s, y - 150 * s]]), .08, { th: H0, id: 9 });
    for (let k = 0; k < 4; k++) { const b = a + k * PI / 2, c = Math.cos(b), d = Math.sin(b), hx = x, hy = y - 160 * s, L = 150 * s;
      fill(F([[hx + c * 8 * s - d * 2, hy + d * 8 * s + c * 2], [hx + c * L - d * 2, hy + d * L + c * 2], [hx + c * L - d * 22 * s, hy + d * L + c * 22 * s], [hx + c * 30 * s - d * 22 * s, hy + d * 30 * s + c * 22 * s]]), .45, { th: b, id: 9 }); }
  }
  // lale tarlası: yatay şeritler perspektifte; satır satır laleler (renkli); o.y0 ufuk, o.t salınım zamanı, o.cesitler sıra sıra
  function tarla(o = {}) {
    const y0 = o.y0 ?? 640, t = o.t || 0;
    fill(R(-600, y0, 3100, 900), .4, { type: 'persp', y0, D: 240, p0: 6, p1: 16, id: 8 });
    const ces = o.cesitler || ['switsers', 'duz', 'semper', 'sari', 'viceroy', 'duz', 'switsers'];
    const rows = o.sira ?? 9;
    for (let r = rows - 1; r >= 0; r--) {
      const u = (r + 1) / rows, yy = y0 + 18 + Math.pow(u, 1.8) * 520, sc = .16 + Math.pow(u, 1.6) * .8, step = 120 * sc + 22;
      fill(R(-600, yy + 6 * sc, 3100, 20 * sc), .22, { th: H0, id: 9 });   // toprak sırtı
      for (let x = -560 + (r % 2) * step * .5; x < 2500; x += step) {
        const sw = Math.sin(t * 1.3 + x * .004 + r) * .06;
        LALE.ciz(x + rnd(x * .01 + r) * step * .3, yy, sc, { sap: 70 * sc, egim: sw, cesit: ces[r % ces.length], yaprakYok: sc < .3, tohum: x * .01 + r * 3.1 });
      }
    }
  }
  // meyhane salonu (Schutters-Doelen): ahşap kirişli tavan, büyük pencere solda, şömine sağda; o.isik
  function meyhane(o = {}) {
    fill(R(-600, -400, 3100, 1900), .1, { th: H0, id: 0 });
    // kirişler
    for (let x = -300; x < 2400; x += 260) fill(F([[x, -60], [x + 70, -60], [x + 50, 150], [x + 20, 150]]), .04, { th: HV, id: 9 });
    fill(R(-600, 140, 3100, 26), .2, { th: H0, id: 9 });
    // ahşap lambri
    fill(R(-600, 640, 3100, 300), .14, { th: HV, id: 9 });
    for (let x = -560; x < 2500; x += 120) fill(R(x, 660, 6, 260), .05, { th: HV, id: 9 });
    // pencere (sol), kurşunlu cam, ışık huzmesi
    fill(R(120, 200, 360, 400), .9, { th: HV, id: 10 });
    for (let x = 120; x <= 480; x += 60) fill(R(x - 3, 200, 6, 400), .2, { th: HV, id: 9 });
    for (let y = 200; y <= 600; y += 50) fill(R(120, y - 3, 360, 6), .2, { th: H0, id: 9 });
    huzme([[120, 200], [480, 200], [1300, 1080], [500, 1080]], .22 * (o.isik ?? 1));
    // duvarda asılı bir resim ve bir nişan tahtası (schutterij: atıcılar loncası)
    fill(R(1500, 260, 300, 220), .05, { th: HV, id: 9 }); fill(R(1516, 276, 268, 188), .32, { th: .4, id: 0 });
    // zemin karoları
    fill(F([[-600, 930], [2500, 930], [2500, 1500], [-600, 1500]]), .3, { type: 'persp', y0: 930, D: 200, p0: 8, p1: 15, id: 8 });
  }
  // mezat masası: uzun masa, üstünde örtü, saksı, kâğıtlar
  function masa(x, y, w, o = {}) {
    fill(F([[x, y], [x + w, y], [x + w + 30, y + 26], [x - 30, y + 26]]), .3, { th: H0, id: 9 });
    fill(F([[x - 30, y + 26], [x + w + 30, y + 26], [x + w + 24, y + 140], [x - 24, y + 140]]), .08, { th: HV, id: 9 });
    for (let i = 0; i < 3; i++) fill(F([[x + 60 + i * 120, y - 4], [x + 150 + i * 120, y - 10], [x + 158 + i * 120, y + 6], [x + 66 + i * 120, y + 10]]), .9, { th: .2, id: 5 });
  }
  function saksi(x, y, s = 1) { fill(F([[x - 40 * s, y - 70 * s], [x + 40 * s, y - 70 * s], [x + 30 * s, y], [x - 30 * s, y]]), .28, { th: HV, id: 9 }); fill(R(x - 46 * s, y - 80 * s, 92 * s, 14 * s), .2, { th: H0, id: 9 }); }
  // terazi: dayanak (x, y taban), eğim a (+ sağ kefe aşağı), kefe ipleri; döner: [solKefe, sağKefe] merkezleri
  function terazi(x, y, a, o = {}) {
    const L = o.L ?? 520, top = y - (o.boy ?? 560);
    fill(F([[x - 130, y], [x + 130, y], [x + 90, y - 30], [x - 90, y - 30]]), .1, { th: H0, id: 9 });
    fill(F([[x - 14, y - 30], [x + 14, y - 30], [x + 9, top], [x - 9, top]]), .12, { th: HV, id: 9 });
    fill(E2(x, top, 20, 20), .2, { type: 'rad', cx: x, cy: top, id: 9 });
    const c = Math.cos(a), s = Math.sin(a), lx = x - c * L, ly = top - s * L, rx = x + c * L, ry = top + s * L;
    fill(F([[lx - s * 8, ly + c * 8], [rx - s * 8, ry + c * 8], [rx + s * 8, ry - c * 8], [lx + s * 8, ly - c * 8]]), .1, { th: a, id: 9 });
    const ip = 300, kef = [];
    for (const [ex, ey] of [[lx, ly], [rx, ry]]) {
      const kx = ex, ky = ey + ip;
      for (const d of [-1, 1]) fill(F([[ex - 1.5, ey], [ex + 1.5, ey], [kx + d * 120 + 1.5, ky], [kx + d * 120 - 1.5, ky]]), .1, { th: HV, id: 9 });
      fill(Sm([[kx - 140, ky], [kx + 140, ky], [kx + 110, ky + 34], [kx - 110, ky + 34]]), .22, { th: H0, id: 9 });
      kef.push([kx, ky]);
    }
    return kef;
  }
  // ── İSTANBUL ──
  function servi(x, y, h, o = {}) { fill(Sm([[x, y - h], [x + h * .09, y - h * .6], [x + h * .1, y - h * .2], [x + h * .06, y], [x - h * .06, y], [x - h * .1, y - h * .2], [x - h * .09, y - h * .6]]), o.ton ?? .04, { type: 'bend', ox: x, oy: y, a: -PI / 2, k: 0, id: 6 }); }
  function kaplumbaga(x, y, s, t, o = {}) {
    fill(Sm([[x - 60 * s, y], [x - 50 * s, y - 30 * s], [x - 10 * s, y - 46 * s], [x + 36 * s, y - 38 * s], [x + 60 * s, y - 6 * s], [x + 56 * s, y + 4 * s]]), .25, { type: 'rad', cx: x, cy: y, id: 4 });
    for (const d of [-1, 1]) fill(E2(x + d * 36 * s, y + 6 * s, 12 * s, 7 * s), .2, { th: 0, id: 9 });
    fill(E2(x + 72 * s, y - 6 * s + Math.sin(t * 2) * 2, 14 * s, 9 * s), .2, { th: 0, id: 9 });
    if (o.mum !== false) mum(x - 4 * s, y - 86 * s, t, s);
  }
  function kandil(x, y, t, s = 1) { fill(E2(x, y, 12 * s, 8 * s), .7, { type: 'rad', cx: x, cy: y, id: 9 }); alev(x, y - 6 * s, t, s * .5); }
  // köşk (Sadabad tipi): ince sütunlu ön cephe, geniş saçak, kubbe değil (sivil yapı)
  function kosk(x, y, w, h, o = {}) {
    fill(R(x, y - h, w, h), .2, { th: HV, id: 9 });
    fill(F([[x - 60, y - h], [x + w + 60, y - h], [x + w + 20, y - h - 50], [x - 20, y - h - 50]]), .06, { th: H0, id: 9 });
    const n = Math.round(w / 90);
    for (let i = 0; i <= n; i++) fill(R(x + i * w / n - 6, y - h, 12, h), .55, { th: HV, id: 9 });
    for (let i = 0; i < n; i++) fill(Sm([[x + i * w / n + 10, y - h * .25], [x + i * w / n + 10, y - h * .8], [x + (i + .5) * w / n, y - h * .92], [x + (i + 1) * w / n - 10, y - h * .8], [x + (i + 1) * w / n - 10, y - h * .25]]), o.gece ? .06 : .7, { th: HV, id: o.gece ? 9 : 10 });
    fill(R(x - 40, y, w + 80, 24), .3, { th: H0, id: 9 });
  }
  return { isik, huzme, alev, mum, ev, gok, degirmen, tarla, meyhane, masa, saksi, terazi, servi, kaplumbaga, kandil, kosk, E2, R, rnd };
})();
