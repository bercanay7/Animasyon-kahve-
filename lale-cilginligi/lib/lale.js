// Lale (gravür + el boyaması). Klasik betik. Kural: filmde renk yalnız lalede; renk değerdir, çöküşte söner.
// İki geçiş:
//   1) LALE.ciz(x, y, s, o): gravür geçişinde (GR.begin/engrave arası) çiçeği çizgiyle çizer ve boyanacak yaprakları kuyruğa yazar;
//   2) LALE.boya(ctx, cam, renk): basmadan sonra kuyruktaki yaprakları suluboya gibi çarpma (multiply) karışımıyla boyar.
//      Siyah çizgi koyu kalır, kâğıt rengi alır: 17. yüzyılın elle renklendirilmiş botanik baskısı (Hortus Eystettensis, lale kitapları).
// Koordinat: dünya (1920×1080 sahne), (x, y) çanağın tabanı; s ölçek (1 = çanak boyu ~90 px). Sap aşağı doğru o.sap px.
// o.tip: 'hol' (Hollanda; yuvarlak çanak) | 'ist' (İstanbul; badem gövde, hançer uç). o.cesit: RENK anahtarı. o.ac: açıklık 0..1. o.egim: radyan.
'use strict';
const LALE = (() => {
  const PI = Math.PI, TAU = PI * 2, HV0 = PI / 2;
  // çeşitler: zemin, alev, kenar; alev = 'kırık' lalelerin virüs izi (yaprağın ortasından tepeye ince diller)
  const RENK = {
    semper:  { zem: [246, 240, 232], alev: [172, 18, 40], kenar: [120, 10, 28], ad: 'Semper Augustus' },   // beyaz + lal (Rozen)
    viceroy: { zem: [244, 240, 238], alev: [96, 40, 128], kenar: [60, 22, 90], ad: 'Viceroy' },               // beyaz + mor (Violetten)
    amiral:  { zem: [246, 242, 240], alev: [118, 46, 150], kenar: [70, 26, 98], ad: 'Admirael van Enkhuizen' },
    switsers:{ zem: [236, 196, 58], alev: [184, 52, 30], kenar: [140, 34, 20], ad: 'Switsers' },              // sarı + kırmızı (Bizarden)
    duz:     { zem: [196, 30, 44], alev: null, kenar: [120, 12, 26], ad: 'düz kırmızı' },                       // kırılmamış lale
    sari:    { zem: [234, 190, 40], alev: null, kenar: [160, 110, 14] },
    ist:     { zem: [182, 22, 40], alev: [120, 8, 24], kenar: [96, 6, 20], ad: 'İstanbul lalesi' },            // badem, hançer uçlu
    istSari: { zem: [232, 186, 44], alev: [190, 70, 20], kenar: [150, 90, 10] },
  };
  let Q = [];
  // örtü (22 Kasım, Fable son okuması): lale kuyruğa girdikten sonra gravürde üstüne çizilen her opak şekil (figür, el, yüz,
  // başka bir lale) boyayı orada siler; yoksa çarpma boyası önden geçen elin, yüzün, eteğin üstüne biner ("kanlı el" okuması).
  // n = şekil çizildiği anda kuyruktaki lale sayısı: şekil yalnız kendinden önce kuyruğa girmiş laleleri örter.
  // Yalnız düz opak ton ("rgb(…)") sayılır: yarı saydam ton, gradyan ve yalnız tarama örtmez (ışık, sis, gölge taraması).
  let OCC = [];
  const _fill = GR.fill;
  GR.fill = function (path, toneStyle, hs, rule = 'nonzero') {
    if (Q.length && typeof toneStyle === 'string' && toneStyle.startsWith('rgb(')) OCC.push({ p: path, m: GR.tx.getTransform(), n: Q.length, rule });
    return _fill(path, toneStyle, hs, rule);
  };
  const rnd = s => { const x = Math.sin(s * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  // yaprak yolu: taban (bx, by), genişlik w, boy h, uç kayması lean, uç kıvrımı tip (+ dışa), dönüş a (taban çevresinde)
  function yaprakPts(bx, by, w, h, lean, tip, a) {
    const ca = Math.cos(a), sa = Math.sin(a), R = (x, y) => [bx + x * ca - y * sa, by + x * sa + y * ca];
    return { R, k: [[-w * .3, 0], [-w * .62, -h * .38], [-w * .5 + lean * .5, -h * .86], [lean - tip, -h], [w * .5 + lean * .5, -h * .86], [w * .62, -h * .38], [w * .3, 0]] };
  }
  function yaprakYol(Y, ist) {
    const { R, k } = Y, p = new Path2D(), P = i => R(k[i][0], k[i][1]);
    const [a0, a1, a2, a3, a4, a5, a6] = [0, 1, 2, 3, 4, 5, 6].map(P);
    p.moveTo(...a0);
    if (ist) { p.bezierCurveTo(a1[0], a1[1], a2[0], a2[1], a3[0], a3[1]); p.bezierCurveTo(a4[0], a4[1], a5[0], a5[1], a6[0], a6[1]); }
    else { p.bezierCurveTo(a1[0], a1[1], a2[0], a2[1], a3[0], a3[1]); p.bezierCurveTo(a4[0], a4[1], a5[0], a5[1], a6[0], a6[1]); }
    const m = R(0, 9); p.quadraticCurveTo(m[0], m[1], a0[0], a0[1]); p.closePath(); return p;
  }
  // çiçek: gravür geçişi
  function ciz(x, y, s = 1, o = {}) {
    const ist = o.tip === 'ist', ac = o.ac ?? .25, eg = o.egim || 0, sap = o.sap ?? 160 * s, ton = o.ton ?? .9;
    const F = INSAN.F, Sm = INSAN.Sm, fill = INSAN.fill;
    // sap (hafif kavisli) ve yapraklar
    if (sap > 0) {
      const sx = x - Math.sin(eg) * sap, sy = y + Math.cos(eg) * sap, mx = (x + sx) / 2 + (o.kavis ?? 8) * s, my = (y + sy) / 2;
      const st = new Path2D(); st.moveTo(x - 3.2 * s, y + 2); st.quadraticCurveTo(mx - 3.5 * s, my, sx - 4 * s, sy); st.lineTo(sx + 4 * s, sy); st.quadraticCurveTo(mx + 3.5 * s, my, x + 3.2 * s, y + 2); st.closePath();
      fill(st, .18, { type: 'bend', ox: sx, oy: sy, a: -PI / 2 + eg, k: 0, id: 9 });
      if (o.yaprakYok !== true) for (const [d, L, yuk] of [[-1, .9, .78], [1, .72, .58]]) {
        const bx = lerp(x, sx, yuk), by = lerp(y, sy, yuk), Lp = sap * L, ux = d * .34, tx = bx + d * Lp * .42, ty = by - Lp * .85;
        const lw = Math.max(16 * s, Lp * .16), lf = new Path2D(); lf.moveTo(bx - d * 4 * s, by); lf.bezierCurveTo(bx + d * (lw * 1.6), by - Lp * .3, tx + d * lw * .2, ty + Lp * .25, tx, ty); lf.bezierCurveTo(tx - d * lw * .8, ty + Lp * .3, bx - d * lw * .3, by - Lp * .35, bx + d * 2, by - 6 * s); lf.closePath();
        GR.save(); GR.tx.lineWidth = 2.4 * Math.sqrt(s); GR.tx.strokeStyle = GR.tone(.05); GR.tx.stroke(lf); GR.px.lineWidth = 2.4 * Math.sqrt(s); GR.px.strokeStyle = GR.hatch({ th: 0, id: 9 }); GR.px.stroke(lf); GR.restore();
        fill(lf, .5, { type: 'bend', ox: bx, oy: by, a: Math.atan2(ty - by, tx - bx), k: d * .0015 / s, id: 9 });
      }
    }
    // çanak: arka iki yaprak (ön yaprağın arkasından yalnız kenarları görünür), ön yaprak. Hollanda: yumurta çanak, yuvarlak uç; İstanbul: badem, hançer uç
    const W0 = ist ? 30 * s : 52 * s, H0 = ist ? 120 * s : 92 * s, tip = ist ? 10 * s : 0;
    const Ys = [
      yaprakPts(x - (5 + ac * 16) * s, y + 1 * s, W0 * .96, H0 * .95, -4 * s - ac * 8 * s, -tip, eg - .13 - ac * .5),
      yaprakPts(x + (5 + ac * 16) * s, y + 1 * s, W0 * .96, H0 * .95, 4 * s + ac * 8 * s, tip, eg + .13 + ac * .5),
      yaprakPts(x, y + 3 * s, W0 * 1.2, H0, (o.lean || 0) * s, ist ? 3 * s : 0, eg),
    ];
    const kat = [];
    Ys.forEach((Y, i) => {
      const p = yaprakYol(Y, ist);
      // kontur: ince koyu çizgi; yaprak açık tonda, tarama yaprak ekseni boyunca (seyrek: renk kâğıda otursun)
      const lw = (ist ? 3.2 : 3.6) * Math.sqrt(s);
      GR.save(); GR.tx.lineWidth = lw; GR.px.lineWidth = lw; GR.tx.strokeStyle = GR.tone(.04); GR.tx.stroke(p); GR.px.strokeStyle = GR.hatch({ th: 0, id: 9 }); GR.px.stroke(p); GR.restore();
      const [ox, oy] = Y.R(0, 0), [tx, ty] = Y.R(0, -H0);
      fill(p, i < 2 ? ton - .1 : ton, { type: 'bend', ox, oy, a: Math.atan2(ty - oy, tx - ox), k: (i === 0 ? -1 : i === 1 ? 1 : 0) * .003 / s, id: 10 });
      // orta damar gölgesi (gravürde yaprağın kıvrımı): tabandan ortaya ince koyu şerit
      if (false) { const g = new Path2D(), [mx, my] = Y.R(0, -H0 * .55); g.moveTo(ox - 3 * s, oy - 4 * s); g.quadraticCurveTo(mx - 6 * s, my, mx, my - 6 * s); g.quadraticCurveTo(mx + 2 * s, my, ox + 3 * s, oy - 4 * s); fill(g, ton - .35, { th: HV0, id: 9 }); }
      kat.push({ p, Y, i });
    });
    Q.push({ kat, x, y, s, ist, H0, W0, cesit: o.cesit || (ist ? 'ist' : 'semper'), renk: o.renk ?? 1, tohum: o.tohum ?? (x * .13 + y * .07) });
  }
  // soğan (gravür): yuvarlak gövde, sivri uç, kuru kabuk çizgileri; o.renk > 0 ise kabuk sıcak kahverengi boyanır? Hayır: kural, renk yalnız çiçekte.
  // Ama soğanın değeri anlatılırken üstünde küçük bir alev (filizin ucu) boyanabilir: o.filiz
  function sogan(x, y, s = 1, o = {}) {
    const Sm = INSAN.Sm, fill = INSAN.fill;
    const g = Sm([[x, y - 70 * s], [x + 22 * s, y - 44 * s], [x + 46 * s, y - 14 * s], [x + 44 * s, y + 18 * s], [x + 20 * s, y + 34 * s], [x - 20 * s, y + 34 * s], [x - 44 * s, y + 18 * s], [x - 46 * s, y - 14 * s], [x - 22 * s, y - 44 * s]]);
    GR.save(); GR.tx.lineWidth = 4 * s; GR.px.lineWidth = 4 * s; GR.tx.strokeStyle = GR.tone(.05); GR.tx.stroke(g); GR.px.strokeStyle = GR.hatch({ th: 0, id: 9 }); GR.px.stroke(g); GR.restore();
    fill(g, o.ton ?? .5, { type: 'bend', ox: x, oy: y + 34 * s, a: -PI / 2, k: .0035 / s, id: 9 });   // boyuna kabuk çizgileri (halka tarama küçük boyda hedef tahtası okunuyordu)
    for (const d of [-1, 1]) { const k = new Path2D(); k.moveTo(x, y - 66 * s); k.quadraticCurveTo(x + d * 34 * s, y - 20 * s, x + d * 14 * s, y + 30 * s); k.lineTo(x + d * 10 * s, y + 30 * s); k.quadraticCurveTo(x + d * 28 * s, y - 20 * s, x, y - 60 * s); fill(k, .12, { th: PI / 2, id: 9 }); }
    // kökler
    for (let i = -3; i <= 3; i++) { const r = new Path2D(); r.moveTo(x + i * 8 * s, y + 32 * s); r.quadraticCurveTo(x + i * 12 * s, y + 46 * s, x + i * 15 * s + rnd(i) * 6, y + 58 * s); r.lineTo(x + i * 15 * s + 2, y + 58 * s); r.quadraticCurveTo(x + i * 12 * s + 2, y + 46 * s, x + i * 8 * s + 3, y + 32 * s); fill(r, .2, { th: PI / 2, id: 9 }); }
  }
  // uzak lale: gravürde minik koyu çanak, boyamada renk lekesi
  function nokta(x, y, r, cesit) {
    const p = new Path2D(); p.ellipse(x, y - r, r * .7, r, 0, 0, TAU);
    INSAN.fill(p, .35, { th: PI / 2, id: 9 });
    Q.push({ kat: [{ p, Y: { R: (a, b) => [x + a, y + b] }, i: 2 }], x, y, s: r / 40, ist: false, H0: r * 2, W0: r * 1.4, cesit, renk: 1, tohum: x, nokta: true });
  }
  // ── boyama geçişi ──
  const CV = makeCanvas(DW, DH), cx = CV.getContext('2d');
  // granül (suluboya pigment birikmesi): 256 karo alfa gürültüsü
  const GT = makeCanvas(256, 256); { const g = GT.getContext('2d'), im = g.createImageData(256, 256); for (let i = 0; i < 256 * 256; i++) { const x = i % 256, y = (i / 256) | 0; const v = .5 * noise2(x / 22, y / 22, 3) + .3 * noise2(x / 6, y / 6, 7) + .2 * rnd(i * .37); im.data[i * 4] = im.data[i * 4 + 1] = im.data[i * 4 + 2] = 255; im.data[i * 4 + 3] = Math.round(255 * (.72 + .28 * clamp(v))); } g.putImageData(im, 0, 0); }
  let GP = null;
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  // renk: genel çarpan (0 = renksiz gravür); o.kay: el boyamasının çizgiden kayması (px), o.pay: boyanan alan (0..1, boyama ilerlemesi)
  function boya(ctx, cam, renk = 1, o = {}) {
    if (!Q.length) return;
    const c = camOf(cam) || { x: 0, y: 0, s: 1 }, z = c.s * RS;
    cx.setTransform(1, 0, 0, 1, 0, 0); cx.globalCompositeOperation = 'source-over'; cx.clearRect(0, 0, DW, DH);
    const kay = o.kay ?? 2.2;
    let oi = 0;
    const ort = n => { // n'ye kadar (n dahil) kaydedilmiş örtüleri boya katmanından sil
      if (oi >= OCC.length || OCC[oi].n > n) return;
      cx.save(); cx.globalCompositeOperation = 'destination-out'; cx.fillStyle = '#000';
      for (; oi < OCC.length && OCC[oi].n <= n; oi++) { const O = OCC[oi]; cx.setTransform(O.m); cx.fill(O.p, O.rule); }
      cx.restore();
    };
    for (let qi = 0; qi < Q.length; qi++) {
      const L = Q[qi];
      ort(qi); // önceki lalelerin üstüne çizilenler (bu lalenin kendi çizgileri dahil değil: onlar n = qi ile kaydedildi ve önceki laleleri örter)
      const R = RENK[L.cesit] || RENK.semper, a = clamp(renk * L.renk); if (a <= .001) continue;
      cx.setTransform(z, 0, 0, z, (kay - c.x) * z, (kay * .6 - c.y) * z);
      for (const { p, Y, i } of L.kat) {
        const [ox, oy] = Y.R(0, 0), [tx, ty] = Y.R(0, -L.H0);
        cx.save(); cx.clip(p);
        // zemin: tabanda koyu, ortada açık (ışık), kenara doğru birikme
        const gz = cx.createLinearGradient(ox, oy, tx, ty);
        const zk = i < 2 ? .86 : 1;
        gz.addColorStop(0, rgba(R.zem.map(v => v * .78 * zk), a)); gz.addColorStop(.45, rgba(R.zem.map(v => Math.min(255, v * zk)), a * .92)); gz.addColorStop(1, rgba(R.zem.map(v => v * .92 * zk), a));
        cx.fillStyle = gz; cx.fill(p);
        // alevler: tabandan tepeye ince diller (kırık lale); tohumlu, kare kare sabit
        if (R.alev && !L.nokta) {
          const n = (L.ist ? 2 : 3) + (o.alevN || 0), ax = tx - ox, ay = ty - oy, Lh = Math.hypot(ax, ay), ux = ax / Lh, uy = ay / Lh, vx = -uy, vy = ux;
          cx.fillStyle = rgba(R.alev, a * .92);
          for (let k = 0; k < n; k++) {
            const off = (k - (n - 1) / 2) * L.W0 * .18 + (rnd(L.tohum + k + i * 7) - .5) * 6 * L.s, len = Lh * (.5 + .42 * rnd(L.tohum * 3 + k + i)), wd = L.W0 * (.035 + .045 * rnd(L.tohum + k * 5 + i)) * (o.alevK || 1);
            const b0x = ox + vx * off + ux * Lh * .1, b0y = oy + vy * off + uy * Lh * .1, ex = b0x + ux * len + vx * (rnd(k + i + L.tohum * 2) - .5) * 10 * L.s, ey = b0y + uy * len + vy * (rnd(k + i + L.tohum * 2) - .5) * 10 * L.s;
            cx.beginPath(); cx.moveTo(b0x - vx * wd, b0y - vy * wd);
            cx.bezierCurveTo(b0x - vx * wd * 1.4 + ux * len * .4, b0y - vy * wd * 1.4 + uy * len * .4, ex - vx * wd * .3 - ux * len * .2, ey - vy * wd * .3 - uy * len * .2, ex, ey);
            cx.bezierCurveTo(ex + vx * wd * .3 - ux * len * .2, ey + vy * wd * .3 - uy * len * .2, b0x + vx * wd * 1.4 + ux * len * .4, b0y + vy * wd * 1.4 + uy * len * .4, b0x + vx * wd, b0y + vy * wd);
            cx.closePath(); cx.fill();
          }
          // kenar alevi (yaprak kenarında ince şerit: "kenar tüyü")
          cx.strokeStyle = rgba(R.alev, a * .55); cx.lineWidth = 3.2 * L.s; cx.stroke(p);
        }
        // kenar birikmesi (suluboyanın kurumuş kenarı)
        cx.strokeStyle = rgba(R.kenar, a * .5); cx.lineWidth = 2.6 * L.s; cx.stroke(p);
        cx.restore();
      }
    }
    ort(Infinity);
    // granül: boyayı pigment gürültüsüyle seyrelt
    cx.setTransform(1, 0, 0, 1, 0, 0); if (!GP) GP = cx.createPattern(GT, 'repeat');
    cx.globalCompositeOperation = 'destination-in'; cx.fillStyle = GP; cx.fillRect(0, 0, DW, DH); cx.globalCompositeOperation = 'source-over';
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'multiply'; ctx.drawImage(CV, 0, 0); ctx.restore();
  }
  return { ciz, sogan, nokta, boya, RENK, sifirla: () => { Q = []; OCC = []; }, get kuyruk() { return Q; } };
})();
