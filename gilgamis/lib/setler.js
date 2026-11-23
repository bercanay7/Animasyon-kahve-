// Sahne setleri ve yaratıklar (Gılgamış). ORTAK DOSYA: başkan.
// Kural: her plan ilk saniyeden hareketli (kamera kayar ya da bir şey kımıldar); yükseklikler: zemin .18, uzak .3–.45, figür .7–.85.
'use strict';
const SET = {}, YAR = {};
(() => {
  const { sekil, cizgi, uzuv } = FIG;
  // kamera: süre boyunca a → b ([cx, cy, z]); e: yumuşatma
  SET.kam = (R, st, a, b, e = E.sine) => { const p = e(clamp(st.lt / Math.max(1, st.d))); R.cam(lerp(a[0], b[0], p), lerp(a[1], b[1], p), lerp(a[2], b[2], p)); };
  SET.zemin = (R, o = {}) => R.kilZemin(-3000, -2000, 6000, 3000, o);
  // yer çizgisi (kabartma bandı) ve çimen öbekleri
  SET.yer = (R, x0, x1, y, o = {}) => {
    R.b.fillStyle = gv(o.z ?? .32); R.b.fillRect(x0, y, x1 - x0, o.kal || 60);
    cizgi(R, [[x0, y], [x1, y]], 3, -.6);
    if (o.cimen !== false) for (let x = x0 + 30; x < x1; x += 90 + hash(x) * 80) { for (let k = -2; k <= 2; k++) cizgi(R, [[x + k * 6, y], [x + k * 11, y - 22 - hash(x + k) * 18]], 3, .6); }
  };
  // uzak tepeler (alçak kabartma)
  SET.tepeler = (R, x0, x1, y, o = {}) => {
    const pts = [[x0, y]]; for (let x = x0; x <= x1; x += 40) pts.push([x, y - (o.h || 120) * (.5 + .5 * Math.sin(x / (o.p || 380) + (o.faz || 0))) * (.6 + .4 * noise1(x / 300, 7))]);
    pts.push([x1, y]);
    R.b.fillStyle = gv(o.z ?? .27); R.b.beginPath(); poly(R.b, pts); R.b.fill();
    R.d.strokeStyle = dv(-.4); R.d.lineWidth = 2.5; R.d.beginPath(); for (let i = 1; i < pts.length - 1; i++) i === 1 ? R.d.moveTo(...pts[i]) : R.d.lineTo(...pts[i]); R.d.stroke();
    // pul pul dağ deseni (Mezopotamya dağ işareti)
    for (let x = x0 + 30; x < x1; x += 70) for (let yy = y - 20; yy > y - (o.h || 120) * .5; yy -= 34) { R.d.strokeStyle = dv(-.35); R.d.lineWidth = 2; R.d.beginPath(); R.d.arc(x + (yy % 68 ? 35 : 0), yy, 16, PI, TAU); R.d.stroke(); }
  };
  // su (lacivert taş): dalgalı yüzey + renk
  SET.su = (R, x0, x1, y, o = {}) => DK.dalga(R, x0, x1, y, { renk: o.renk || '#3E5F96', faz: o.faz || 0, z: o.z ?? .3, a: o.a || 14, p: o.p || 140, alt: o.alt });
  // gölet (yukarıdan bakılmış oval, lacivert)
  SET.golet = (R, x, y, rx, ry, o = {}) => {
    R.b.fillStyle = gv(o.z ?? .12); R.b.beginPath(); R.b.ellipse(x, y, rx, ry, 0, 0, TAU); R.b.fill();
    R.m.fillStyle = o.renk || '#4A6CA6'; R.m.beginPath(); R.m.ellipse(x, y, rx, ry, 0, 0, TAU); R.m.fill();
    R.d.strokeStyle = dv(-.6); R.d.lineWidth = 4; R.d.beginPath(); R.d.ellipse(x, y, rx, ry, 0, 0, TAU); R.d.stroke();
    for (let i = 1; i < 5; i++) { R.d.strokeStyle = dv(.35); R.d.lineWidth = 2.5; R.d.beginPath(); R.d.ellipse(x + Math.sin((o.faz || 0) + i) * 10, y, rx * (1 - i * .18), ry * (1 - i * .18), 0, .2 + i, 2.2 + i); R.d.stroke(); }
  };
  // ev (düz damlı kerpiç), kapılı
  SET.ev = (R, x, y, w, h, o = {}) => {
    const z = o.z ?? .45;
    R.b.fillStyle = gv(z); R.b.fillRect(x, y - h, w, h);
    cizgi(R, [[x, y - h], [x + w, y - h]], 4, .6); cizgi(R, [[x, y - h], [x, y]], 3, -.6); cizgi(R, [[x + w, y - h], [x + w, y]], 3, -.6);
    R.b.fillStyle = gv(z - .2); const dx = x + w * (o.kapi ?? .35), dw = Math.min(70, w * .25); R.b.fillRect(dx, y - h * .55, dw, h * .55);
    for (let k = 0; k < (o.kiris ?? 5); k++) { R.b.fillStyle = gv(z + .06); R.b.beginPath(); R.b.arc(x + 20 + k * (w - 40) / 4, y - h + 14, 7, 0, TAU); R.b.fill(); } // dam kirişleri
  };
  // tandır fırını (kubbe) ve duman
  SET.firin = (R, x, y, r, o = {}) => {
    R.b.fillStyle = gv(o.z ?? .55); R.b.beginPath(); R.b.arc(x, y, r, PI, TAU); R.b.fill();
    R.b.fillStyle = gv(.25); R.b.beginPath(); R.b.arc(x, y - r * .25, r * .28, PI, TAU); R.b.fill();
    cizgi(R, [[x - r, y], [x + r, y]], 3, -.6);
    R.after(c => { const t = FIG_T || 0; c.globalCompositeOperation = 'screen'; for (let i = 0; i < 4; i++) { const u = ((t * .3 + i * .25) % 1); c.fillStyle = `rgba(230,200,170,${.18 * (1 - u)})`; c.beginPath(); c.arc(x + Math.sin(t + i) * 12 * u, y - r - u * 160, 16 + u * 40, 0, TAU); c.fill(); } c.fillStyle = 'rgba(255,140,60,.35)'; c.beginPath(); c.arc(x, y - r * .25, r * .2, 0, TAU); c.fill(); });
  };
  // yuvarlak ekmek (durum: 0 taze, ... bkz. YAR.ekmek)
  // meşale (duvar demiri + alev parıltısı); ışık noktasını R.L.pts'e ekler
  SET.mesale = (R, x, y, o = {}) => {
    uzuv(R, [x, y + 60], [x, y - 10], 18, 26, .62, .6);
    sekil(R, [[x - 24, y - 10], [x + 24, y - 10], [x + 18, y + 6], [x - 18, y + 6]], .66, .5);
    const t = FIG_T || 0, fl = .85 + .15 * noise1(t * 6, 3) + (o.titre ?? 0) * .1 * Math.sin(t * 23);
    const [sx, sy] = R.scr(x, y - 40);
    R.L.pts.push({ x: sx, y: sy, z: 220 * R.z, r: (o.r || 1500) * Math.max(.7, R.z), i: (o.i ?? 1.6) * fl * (o.son ?? 1), col: [1.15, .72, .4] });
    if ((o.son ?? 1) > .05) R.after(c => { c.globalCompositeOperation = 'screen'; const g = c.createRadialGradient(x, y - 40, 2, x, y - 40, 120 * fl); g.addColorStop(0, `rgba(255,220,150,${.9 * (o.son ?? 1)})`); g.addColorStop(.3, `rgba(255,140,50,${.45 * (o.son ?? 1)})`); g.addColorStop(1, 'rgba(255,90,20,0)'); c.fillStyle = g; c.beginPath(); c.arc(x, y - 40, 120 * fl, 0, TAU); c.fill();
      c.fillStyle = `rgba(255,200,120,${.8 * (o.son ?? 1)})`; c.beginPath(); c.moveTo(x - 16, y - 12); c.quadraticCurveTo(x - 10 + Math.sin(t * 9) * 6, y - 60, x + Math.sin(t * 7) * 8, y - 90 * fl); c.quadraticCurveTo(x + 12, y - 50, x + 16, y - 12); c.fill(); });
  };
  // ışığı gece yap
  SET.gece = (R, k = 1) => { R.L.int *= lerp(1, .22, k); R.L.amb *= lerp(1, .45, k); R.L.col = [lerp(1, .55, k), lerp(.97, .62, k), lerp(.9, .85, k)]; };
  // oda: tuğla duvar + zemin + kapı
  SET.oda = (R, o = {}) => {
    DK.tugla(R, -800, -400, 2800, 860, { z: .3, bw: 90, bh: 36, lw: 2.5 });
    R.b.fillStyle = gv(.38); R.b.fillRect(-800, 860, 3600, 400); cizgi(R, [[-800, 860], [2800, 860]], 4, -.7);
    if (o.kapi !== false) { const kx = o.kapiX ?? 1650; R.b.fillStyle = gv(.16); R.b.fillRect(kx, 360, 220, 500); cizgi(R, [[kx, 860], [kx, 360], [kx + 220, 360], [kx + 220, 860]], 6, .7); }
  };
  // orman: sedirler sırası
  SET.orman = (R, x0, x1, y, o = {}) => { for (let x = x0, i = 0; x < x1; x += o.ara || 260, i++) DK.sedir(R, x + hash(i * 7.3) * 60, y, (o.h || 640) * (.8 + hash(i * 3.1) * .35), { z: (o.z ?? .5) + (i % 2) * .05, kat: 4 + (i % 2) }); };
  // dağ (Maşu): çift tepe, ortada kapı
  SET.masu = (R, x, y, o = {}) => {
    const tepe = (cx, h) => { const pts = [[cx - 380, y], [cx - 200, y - h * .6], [cx - 60, y - h], [cx + 60, y - h * .95], [cx + 220, y - h * .5], [cx + 380, y]]; sekil(R, pts, .42, .5, null, .7); for (let yy = y - 40; yy > y - h * .85; yy -= 44) for (let xx = cx - 300; xx < cx + 300; xx += 60) if (Math.abs(xx - cx) < (y - yy) * .55) { R.d.strokeStyle = dv(-.4); R.d.lineWidth = 2.5; R.d.beginPath(); R.d.arc(xx + ((yy / 44) % 2) * 30, yy, 20, PI, TAU); R.d.stroke(); } };
    tepe(x - 330, 560); tepe(x + 330, 600);
    R.b.fillStyle = gv(.08); R.b.beginPath(); R.b.moveTo(x - 90, y); R.b.lineTo(x - 90, y - 230); R.b.arc(x, y - 230, 90, PI, TAU); R.b.lineTo(x + 90, y); R.b.fill();
    cizgi(R, [[x - 90, y], [x - 90, y - 230]], 6, .7); cizgi(R, [[x + 90, y], [x + 90, y - 230]], 6, .7);
  };
  // mücevher ağacı: dallarda lacivert ve akik meyveler (renk malzeme tuvalinde)
  SET.mucevherAgaci = (R, x, y, h, o = {}) => {
    uzuv(R, [x, y], [x, y - h * .6], 26, 16, .55, .6);
    for (let i = 0; i < 5; i++) { const a = -PI / 2 + (i - 2) * .45, e = [x + Math.cos(a) * h * .4, y - h * .55 + Math.sin(a) * h * .4]; uzuv(R, [x, y - h * .5], e, 12, 6, .57, .5);
      for (let k = 0; k < 4; k++) { const p = [lerp(x, e[0], .55 + k * .15) + (k % 2 ? 14 : -14), lerp(y - h * .5, e[1], .55 + k * .15)], r = 16 + (k % 2) * 4, col = (i + k) % 3 === 0 ? '#2A4590' : (i + k) % 3 === 1 ? '#3E63B0' : '#6A8CCB';
        R.b.fillStyle = gv(.8); R.b.beginPath(); R.b.arc(p[0], p[1], r, 0, TAU); R.b.fill(); R.m.fillStyle = col; R.m.beginPath(); R.m.arc(p[0], p[1], r, 0, TAU); R.m.fill(); R.d.fillStyle = dv(.5); R.d.beginPath(); R.d.arc(p[0] - r * .3, p[1] - r * .3, r * .25, 0, TAU); R.d.fill(); } }
  };
  // tanrı işaretleri: boynuzlu taç kaideler (Mezopotamya sınır taşlarındaki gibi); insan biçimi yok
  SET.tac = (R, x, y, s, o = {}) => {
    sekil(R, [[x - s * .35, y], [x + s * .35, y], [x + s * .3, y - s * .3], [x - s * .3, y - s * .3]], .55, .5);
    for (let k = 0; k < 3; k++) { const yy = y - s * .32 - k * s * .17; sekil(R, [[x - s * .28, yy], [x - s * .36, yy - s * .14], [x - s * .2, yy - s * .1], [x + s * .2, yy - s * .1], [x + s * .36, yy - s * .14], [x + s * .28, yy]], .62, .5); }
    R.b.fillStyle = gv(.66); R.b.beginPath(); R.b.arc(x, y - s * .9, s * .1, 0, TAU); R.b.fill();
  };


  // yakın yüz: figürü büyük çizer (kamera z≈1; ayrıntı keskin kalır). baş ekranda (hx, hy). o: {tip, f, arka: 'tugla'|'tepe'|'oda'|'su'|'karanlik', fig: ek figür seçenekleri, renk}
  SET.yakin = (R, st, o = {}) => {
    const S = o.S || 1500, f = o.f ?? 1, hx = o.hx ?? 960, hy = o.hy ?? 470;
    const kx = o.kay ? o.kay * clamp(st.lt / Math.max(1, st.d)) : 0;
    R.cam(960 + kx, 540, 1);
    SET.zemin(R);
    if (o.arka === 'tugla' || o.arka === 'oda') DK.tugla(R, -400, -400, 2400, 1500, { z: .28, bw: 260, bh: 100, lw: 5, renk: o.tuglaRenk });
    if (o.arka === 'tepe') { SET.tepeler(R, -400, 2400, 1200, { h: 500, p: 700, z: .26 }); }
    if (o.arka === 'su') { DK.dalga(R, -400, 2400, 760, { renk: '#41639E', faz: st.lt * .6, z: .2, a: 30, p: 300, lw: 7 }); }
    FIG.fig(R, hx - f * S * .015, hy + S * .9, S, { tip: o.tip || 'gilgamis', f, kol: o.kol || [[.15, .3], [.05, .2]], ...(o.fig || {}) });
  };

  // ---- yaratıklar ----
  YAR.aslan = (R, x, y, s, o = {}) => {
    const f = o.f ?? 1, z = o.z ?? .7, k = s; for (const c of [R.b, R.d, R.m]) { c.save(); c.translate(x, y); c.scale(f, 1); }
    const a = o.kos ? Math.sin(o.kos) * .4 : 0;
    const ayak = (hx, an, zz) => { const d = [hx + Math.sin(an) * k * .12, -k * .18]; uzuv(R, [hx, -k * .38], d, k * .1, k * .07, zz); uzuv(R, d, [d[0] + Math.sin(an) * k * .05, 0], k * .07, k * .06, zz); };
    ayak(-k * .35, -a, z - .1); ayak(k * .3, a, z - .1);
    sekil(R, [[-k * .5, -k * .35], [-k * .45, -k * .55], [k * .1, -k * .58], [k * .3, -k * .62], [k * .38, -k * .45], [k * .2, -k * .32], [-k * .3, -k * .3]], z, .5);
    sekil(R, [[k * .22, -k * .72], [k * .48, -k * .7], [k * .56, -k * .55], [k * .45, -k * .4], [k * .25, -k * .38], [k * .15, -k * .55]], z + .05, .55); // yele ve baş
    for (let q = 0; q < 14; q++) { const u = q / 14; cizgi(R, [[k * (.2 + u * .1), -k * (.4 + u * .3)], [k * (.15 + u * .1), -k * (.45 + u * .3)]], Math.max(1.5, k * .012), -.6); }
    R.d.fillStyle = dv(-.9); R.d.beginPath(); R.d.arc(k * .46, -k * .58, k * .015, 0, TAU); R.d.fill();
    uzuv(R, [-k * .5, -k * .45], [-k * .72, -k * .62 + Math.sin((FIG_T || 0) * 2) * k * .04], k * .03, k * .02, z - .05);
    ayak(-k * .28, a * .7, z + .03); ayak(k * .36, -a * .7, z + .03);
    for (const c of [R.b, R.d, R.m]) c.restore();
  };
  YAR.boga = (R, x, y, s, o = {}) => {
    const f = o.f ?? 1, z = o.z ?? .7, k = s; for (const c of [R.b, R.d, R.m]) { c.save(); c.translate(x, y); c.scale(f, 1); if (o.don) c.rotate(o.don); }
    const a = o.kos ? Math.sin(o.kos) * .5 : 0;
    const ayak = (hx, an, zz) => { const d = [hx + Math.sin(an) * k * .1, -k * .2]; uzuv(R, [hx, -k * .45], d, k * .11, k * .07, zz); uzuv(R, d, [d[0], 0], k * .07, k * .06, zz); };
    ayak(-k * .4, -a, z - .1); ayak(k * .32, a, z - .1);
    sekil(R, [[-k * .55, -k * .42], [-k * .5, -k * .72], [k * .1, -k * .78], [k * .38, -k * .8], [k * .42, -k * .55], [k * .3, -k * .4], [-k * .35, -k * .36]], z, .5);
    sekil(R, [[k * .36, -k * .82], [k * .62, -k * .72], [k * .66, -k * .58], [k * .5, -k * .52], [k * .36, -k * .55]], z + .05, .55);
    cizgi(R, [[k * .42, -k * .8], [k * .38, -k * 1.0], [k * .5, -k * 1.08]], Math.max(3, k * .04), .8); // boynuz
    R.d.fillStyle = dv(-.9); R.d.beginPath(); R.d.arc(k * .52, -k * .7, k * .018, 0, TAU); R.d.fill();
    for (let q = 0; q < 10; q++) cizgi(R, [[k * (.25 + q * .012), -k * .78], [k * (.2 + q * .012), -k * .6]], Math.max(1.5, k * .01), -.5);
    ayak(-k * .32, a * .7, z + .03); ayak(k * .38, -a * .7, z + .03);
    uzuv(R, [-k * .55, -k * .65], [-k * .62, -k * .3], k * .03, k * .02, z);
    for (const c of [R.b, R.d, R.m]) c.restore();
  };
  // Humbaba: geleneksel bağırsak kıvrımlı yüz maskesi (önden)
  YAR.humbaba = (R, x, y, s, o = {}) => {
    const z = o.z ?? .8;
    sekil(R, [[x - s * .42, y - s * .3], [x - s * .3, y - s * .55], [x, y - s * .62], [x + s * .3, y - s * .55], [x + s * .42, y - s * .3], [x + s * .38, y + s * .1], [x + s * .2, y + s * .38], [x, y + s * .45], [x - s * .2, y + s * .38], [x - s * .38, y + s * .1]], z, .6);
    // bağırsak kıvrımları: iç içe yollar
    for (let i = 0; i < 9; i++) { R.d.strokeStyle = dv(-.6); R.d.lineWidth = Math.max(2, s * .012); R.d.beginPath(); const rr = s * (.08 + i * .035); R.d.arc(x + Math.sin(i * 1.7) * s * .06, y - s * .05, rr, i * .9, i * .9 + PI * 1.4); R.d.stroke(); }
    for (const sx of [-1, 1]) { R.b.fillStyle = gv(z + .08); R.b.beginPath(); R.b.ellipse(x + sx * s * .15, y - s * .2, s * .08, s * .05, 0, 0, TAU); R.b.fill(); R.d.fillStyle = dv(-.95); R.d.beginPath(); R.d.arc(x + sx * s * .15, y - s * .2, s * .025, 0, TAU); R.d.fill(); }
    R.b.fillStyle = gv(z - .2); R.b.beginPath(); R.b.ellipse(x, y + s * .2, s * .17, s * (.06 + (o.agiz || 0) * .08), 0, 0, TAU); R.b.fill();
    for (let q = -3; q <= 3; q++) cizgi(R, [[x + q * s * .045, y + s * .15], [x + q * s * .045, y + s * .2]], Math.max(2, s * .015), .7);
  };
  YAR.maymun = (R, x, y, s, o = {}) => { // dala oturmuş maymun, profil; (x, y) dalın üstü
    const z = o.z ?? .7, f = o.f ?? 1; for (const c of [R.b, R.d, R.m]) { c.save(); c.translate(x, y); c.scale(f, 1); }
    const t = FIG_T || 0;
    // kuyruk: daldan aşağı sarkan S eğrisi
    const kp = []; for (let i = 0; i <= 10; i++) { const u = i / 10; kp.push([-s * .25 - Math.sin(u * 3 + t) * s * .08, s * (.05 + u * .7)]); }
    for (let i = 0; i < 10; i++) uzuv(R, kp[i], kp[i + 1], s * .045, s * .04, z - .05, 0);
    sekil(R, [[-s * .3, 0], [-s * .32, -s * .3], [-s * .12, -s * .48], [s * .12, -s * .42], [s * .2, -s * .15], [s * .15, 0]], z, .5, null, .7); // gövde (çömelmiş)
    sekil(R, [[s * .05, -s * .45], [s * .1, -s * .65], [s * .25, -s * .7], [s * .42, -s * .6], [s * .45, -s * .5], [s * .3, -s * .42]], z + .04, .55, null, .8); // baş ve burun
    R.d.fillStyle = dv(-.9); R.d.beginPath(); R.d.arc(s * .3, -s * .6, s * .025, 0, TAU); R.d.fill();
    cizgi(R, [[s * .38, -s * .5], [s * .44, -s * .5 + (o.kol || 0) * s * .05]], Math.max(1.5, s * .02), -.8); // açık ağız
    R.d.strokeStyle = dv(-.5); R.d.lineWidth = Math.max(1.5, s * .012); R.d.beginPath(); R.d.arc(s * .12, -s * .62, s * .05, 0, TAU); R.d.stroke(); // kulak
    uzuv(R, [s * .1, -s * .35], [s * .32, -s * (.38 + (o.kol || 0) * .3)], s * .07, s * .05, z + .03, .5, true); // kol
    uzuv(R, [s * .05, -s * .05], [s * .22, 0], s * .09, s * .06, z + .03, .5, true); // bacak
    for (const c of [R.b, R.d, R.m]) c.restore();
  };
  YAR.kus = (R, x, y, s, o = {}) => { const z = o.z ?? .7, k = Math.sin(o.kanat || 0); sekil(R, [[x - s * .4, y], [x, y - s * .12], [x + s * .45, y - s * .05], [x + s * .5, y + s * .03], [x, y + s * .1]], z, .5); sekil(R, [[x - s * .1, y - s * .05], [x + s * .1, y - s * .05], [x - s * .05, y - s * (.2 + k * .35)]], z + .04, .5); };
  YAR.agustos = (R, x, y, s) => { sekil(R, [[x - s * .5, y], [x - s * .2, y - s * .2], [x + s * .5, y - s * .1], [x + s * .3, y + s * .1]], .72, .5); cizgi(R, [[x - s * .3, y - s * .1], [x + s * .4, y - s * .05]], 2, -.6); };
  // akrep insan: insan gövdesi, akrep kuyruğu ve kuş ayakları (Mezopotamya mühürlerindeki gibi)
  YAR.akrep = (R, x, y, s, o = {}) => {
    const f = o.f ?? 1; const r = FIG.fig(R, x, y, s, { tip: 'adam', f, z: .74, kol: o.kol || [[1.2, 1.0], [.3, .3]], bacak: [[.1, 0], [-.1, 0]], giysi: 'etek' });
    for (const c of [R.b, R.d, R.m]) { c.save(); c.translate(x, y); c.scale(f, 1); }
    // kuyruk: kalçadan çıkıp sırtın üstünde öne kıvrılan, kalınlığı azalan, boğumlu akrep kuyruğu ve kanca iğne
    const pts = []; for (let i = 0; i <= 24; i++) { const u = i / 24, a = PI * .78 + u * PI * .95, rr = s * (.32 - u * .06); pts.push([-s * .06 + Math.cos(a) * rr, -s * .78 + Math.sin(a) * rr * 1.1]); }
    for (let i = 0; i < 24; i++) uzuv(R, pts[i], pts[i + 1], s * (.085 - i * .0022), s * (.083 - i * .0022), .7, 0);
    for (let i = 3; i < 24; i += 3) { const p = pts[i], q = pts[i + 1], an = Math.atan2(q[1] - p[1], q[0] - p[0]) + PI / 2, ww = s * (.085 - i * .0022) * .5; cizgi(R, [[p[0] + Math.cos(an) * ww, p[1] + Math.sin(an) * ww], [p[0] - Math.cos(an) * ww, p[1] - Math.sin(an) * ww]], Math.max(1.5, s * .006), -.6); }
    const e = pts[24], e2 = pts[22];
    sekil(R, [e, [e[0] + s * .09, e[1] + s * .02], [e[0] + s * .13, e[1] + s * .1], [e[0] + s * .05, e[1] + s * .06]], .76, .6);
    for (const c of [R.b, R.d, R.m]) c.restore();
    return r;
  };

  // ekmek: durum 0 taze, 1 kuru (çatlak), 2 bozuk, 3 yumuşak (çökmüş), 4 beyaz, 5 küflü, 6 korda (parlıyor)
  YAR.ekmek = (R, x, y, r, d = 0) => {
    const z = .7 - (d === 3 ? .15 : 0), ry = r * (d === 3 ? .45 : .7);
    R.b.fillStyle = gv(z); R.b.beginPath(); R.b.ellipse(x, y, r, ry, 0, PI, TAU); R.b.lineTo(x - r, y); R.b.fill();
    R.d.fillStyle = R.T.kilPd; R.d.beginPath(); R.d.ellipse(x, y, r, ry, 0, PI, TAU); R.d.fill();
    cizgi(R, [[x - r, y], [x + r, y]], 3, -.6);
    if (d === 1) for (let i = 0; i < 6; i++) cizgi(R, [[x - r * .6 + i * r * .25, y - ry * .7], [x - r * .5 + i * r * .22, y - ry * .3], [x - r * .55 + i * r * .25, y - ry * .05]], 3, -.85);
    if (d === 2) for (let i = 0; i < 9; i++) { R.d.fillStyle = dv(-.6); R.d.beginPath(); R.d.arc(x + (hash(i) - .5) * r * 1.4, y - ry * hash(i + 4) * .8, r * .07, 0, TAU); R.d.fill(); }
    const renk = { 2: 'rgba(110,90,60,.45)', 4: 'rgba(240,235,220,.75)', 5: 'rgba(120,140,110,.6)' }[d];
    if (renk) { R.m.fillStyle = renk; R.m.beginPath(); R.m.ellipse(x, y, r, ry, 0, PI, TAU); R.m.fill(); }
    if (d === 5) for (let i = 0; i < 14; i++) { R.d.fillStyle = dv(.5); R.d.beginPath(); R.d.arc(x + (hash(i * 2) - .5) * r * 1.5, y - ry * hash(i * 3) * .85, r * .05, 0, TAU); R.d.fill(); }
    if (d === 0 || d === 6) cizgi(R, [[x - r * .4, y - ry * .55], [x + r * .4, y - ry * .55]], 3, -.4);
    if (d === 6) { R.b.fillStyle = gv(.45); R.b.fillRect(x - r * 1.2, y, r * 2.4, 22); const [sx, sy] = R.scr(x, y + 10); R.L.pts.push({ x: sx, y: sy, z: 60 * R.z, r: 260 * R.z, i: 1.2, col: [1.2, .55, .2] }); R.after(c => { c.globalCompositeOperation = 'screen'; c.fillStyle = 'rgba(255,120,40,.4)'; c.fillRect(x - r * 1.15, y + 4, r * 2.3, 14); }); }
  };
  // testi
  YAR.testi = (R, x, y, h) => { sekil(R, [[x - h * .12, y - h], [x + h * .12, y - h], [x + h * .1, y - h * .85], [x + h * .3, y - h * .5], [x + h * .2, y], [x - h * .2, y], [x - h * .3, y - h * .5], [x - h * .1, y - h * .85]], .72, .55); cizgi(R, [[x - h * .25, y - h * .55], [x + h * .25, y - h * .55]], 2.5, -.5); };
  // parmak izi (izleyicinin izi): kile bastırılmış iç içe kıvrımlar
  YAR.parmakIzi = (R, x, y, s, p = 1) => {
    R.b.fillStyle = gv(.1); R.b.globalAlpha = p; R.b.beginPath(); R.b.ellipse(x, y, s * .38, s * .5, 0, 0, TAU); R.b.fill(); R.b.globalAlpha = 1;
    R.d.strokeStyle = dv(.55 * p); R.d.lineWidth = Math.max(2, s * .012);
    for (let i = 1; i < 16; i++) { const rr = i / 16; R.d.beginPath(); R.d.ellipse(x + Math.sin(i * .9) * s * .01, y + s * .06 * rr, s * .36 * rr, s * .46 * rr, 0, PI * (1.05 - rr * .1), PI * (1.95 + rr * .1)); R.d.stroke(); }
  };
})();
