// Üslup karesi: yanan göl (A02). Dünya koordinatı 1920×1080.
'use strict';
function sahneGol(t, o = {}) {
  const { tx, px, tone, pat, fill } = GR;
  GR.begin(.1, 0, 1);
  // ── değer planı: zifiri tonoz; ufukta figürün arkasında büyük ateş parıltısı; sağ üstte yitik cennetin yarığı ──
  const FX = 800; // figür ekseni
  let g = tx.createLinearGradient(0, 0, 0, 600);
  g.addColorStop(0, tone(.04)); g.addColorStop(.45, tone(.1)); g.addColorStop(.8, tone(.3)); g.addColorStop(1, tone(.55));
  tx.fillStyle = g; tx.fillRect(0, 0, W, 600);
  PR.glow(FX + 60, 590, 20, 620, 1, .85);            // ufuk parıltısı (figürün arkası)
  PR.glow(1600, -20, 4, 330, 1, .9);                 // yarık
  PR.rays(1600, -30, PI * .56, PI * .93, 9, 1150, { str: .3, seed: 4, t, blur: 16 });
  // duman tonozu: üstte koyu kütleler, ufka yakın alttan aydınlanan karınlar
  PR.cloud({ x: 300, y: 150, w: 1100, h: 250, seed: 3, lit: [.2, .9], base: .04, hi: .26, drift: Math.sin(t * .1) * 10 });
  PR.cloud({ x: 1150, y: 210, w: 800, h: 210, seed: 8, lit: [.5, -.6], base: .05, hi: .5, drift: Math.sin(t * .08 + 1) * 12 });
  PR.cloud({ x: 250, y: 420, w: 900, h: 170, seed: 12, lit: [.6, .7], base: .12, hi: .6, soft: 8 });
  PR.cloud({ x: 1560, y: 440, w: 900, h: 170, seed: 17, lit: [-.6, .7], base: .14, hi: .66, soft: 8 });
  // göl
  g = tx.createLinearGradient(0, 590, 0, H);
  g.addColorStop(0, tone(.8)); g.addColorStop(.1, tone(.34)); g.addColorStop(.45, tone(.13)); g.addColorStop(1, tone(.05));
  tx.fillStyle = g; tx.fillRect(0, 590, W, H - 590);
  PR.lake(590, H, t, { bands: 16 });
  { // figürün arkasındaki parıltının göldeki yansıması
    tx.save(); tx.globalCompositeOperation = 'lighter';
    const rg = tx.createRadialGradient(FX + 60, 600, 2, FX + 60, 600, 520); rg.addColorStop(0, 'rgba(255,255,255,.55)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
    tx.translate(FX + 60, 600); tx.scale(1, .42); tx.translate(-FX - 60, -600); tx.fillStyle = rg; tx.fillRect(FX - 500, 600, 1100, 540); tx.restore(); }
  PR.flameBank(-60, W + 60, 602, 80, t, 1, { base: .75, wr: .5 });
  PR.flameBank(480, 1180, 640, 150, t, 5, { env: f => .35 + .65 * Math.sin(f * PI), base: .8 });
  PR.flameBank(1250, W + 80, 760, 200, t, 3, { env: f => .45 + .55 * f });
  // ── Şeytan: gölden doğrulmuş, yüzü yarığa dönük; arkadan aydınlanan koyu kütle, kenar ışığı ──
  const br = Math.sin(t * .6) * 2.5, h = 74;
  const J = {
    hd: [FX + 16, 462 + br * .4], nk: [FX + 6, 512 + br * .6], shR: [FX - 68, 560 + br], shL: [FX + 56, 552 + br],
    elR: [FX - 122, 668], wrR: [FX - 104, 770], elL: [FX + 118, 652], wrL: [FX + 132, 752],
    hpR: [FX - 50, 790], hpL: [FX + 48, 790], knR: [FX - 52, 930], knL: [FX + 50, 930], anR: [FX - 52, 1080], anL: [FX + 50, 1080],
  };
  for (const side of [-1, 1]) { // kanatlar: figürün arkasında, yanık, yarı açık
    const root = [FX - 8 + side * 34, 570 + br];
    GR.frame(root[0], root[1], side < 0 ? -.05 : .22, side, 1);
    KN.feathered({ span: side < 0 ? 600 : 520, open: side < 0 ? .92 : .8, lift: side < 0 ? .5 : .78, t, seed: side < 0 ? 31 : 32, dark: .9, rim: .55 });
    GR.unframe();
  }
  // beden: önden; ateş alttan aydınlatır, ufuk parıltısı kenarlarda ışık bırakır
  FG.sbody(J, { h, near: 'L', noHead: true, legs: true,
    sh: { lit: [.75, -.55], lz: .2, lo: .03, hi: .8, amb: .04, rim: 1.0, rimAll: .18, rimDir: [.75, -.6], axis: .2, wrap: 2.4, depth: 30, bump: .3, edge: .5 } });
  // baş: önden, yüz gölgede; saç koyu kıvırcık kütle; karanlığın içinde açılan iki göz
  const hh = 86, HX = J.hd[0] - 6, HY = J.hd[1] + 4, open = o.eyes ?? 1;
  FG.sculpt([HX - 70, HY - 80, HX + 70, HY + 80], c => { c.beginPath(); c.ellipse(HX, HY, hh * .36, hh * .5, .04, 0, TAU); c.fill(); },
    c => { c.fillStyle = 'rgba(255,255,255,.8)'; c.beginPath(); c.ellipse(HX, HY + hh * .1, hh * .07, hh * .16, 0, 0, TAU); c.fill();   // burun
      for (const sd of [-1, 1]) { c.beginPath(); c.ellipse(HX + sd * hh * .19, HY + hh * .14, hh * .12, hh * .09, 0, 0, TAU); c.fill(); } },   // elmacıklar
    { lit: [.8, -.5], lz: .12, lo: .015, hi: .3, amb: .02, rim: .9, rimDir: [.8, -.5], infl: 8, bump: .4, depth: 34, id: 5, axis: .15, wrap: 1.6, edge: .4 });
  FG.sculpt([HX - 80, HY - 100, HX + 80, HY + 40], c => {
    const r = rng(5), cy = HY - hh * .2;
    c.beginPath(); c.ellipse(HX, cy - hh * .08, hh * .4, hh * .3, 0, 0, TAU); c.fill();
    for (let i = 0; i < 17; i++) { const a = PI * .12 - i / 16 * PI * 1.24, rr = hh * (.4 + r() * .06); c.beginPath(); c.arc(HX + Math.cos(a) * rr, cy + Math.sin(a) * rr * .9, hh * (.1 + r() * .06), 0, TAU); c.fill(); }
  }, c => { const r = rng(6); c.fillStyle = 'rgba(255,255,255,.9)'; for (let i = 0; i < 26; i++) { c.beginPath(); c.arc(HX - hh * .5 + r() * hh, HY - hh * .75 + r() * hh * .6, 4 + r() * 4, 0, TAU); c.fill(); } },
  { lit: [.6, -.7], lz: .25, lo: .01, hi: .36, amb: .03, rim: .8, rimDir: [.7, -.7], infl: 3, bump: 1.3, id: 4, axis: .6, wrap: 1 });
  if (open > 0) for (const sd of [-1, 1]) { // gözler: karanlık yüzde iki ince ışık
    const ex = HX + sd * hh * .145, ey = HY - hh * .03;
    tx.fillStyle = tone(1); tx.beginPath(); tx.ellipse(ex, ey, hh * .06, hh * .024 * open, sd * .14, 0, TAU); tx.fill();
    PR.glow(ex, ey, 1, hh * .11, 1, .35 * open);
  }
  // zincirler: bileklerden göle
  PR.chain(J.wrR[0], J.wrR[1] + 8, FX - 230, 840, 22, { v: .8 });
  PR.chain(J.wrL[0], J.wrL[1] + 8, FX + 270, 838, 22, { v: .85 });
  // göl yüzeyi figürün önünde (belden aşağısını örter), bel hizasında alevler
  { const P = new Path2D(); P.rect(0, 806, W, H); const g2 = tx.createLinearGradient(0, 806, 0, H); g2.addColorStop(0, tone(.3)); g2.addColorStop(.2, tone(.14)); g2.addColorStop(1, tone(.05)); fill(P, g2, { th: 0, ph: .3, id: 8 });
    PR.glow(FX, 815, 5, 260, 1, .35);
    PR.flameBank(FX - 260, FX + 300, 836, 110, t, 7, { env: f => .35 + .65 * Math.abs(f - .5) * 2, wr: .55 });
    PR.flameBank(-80, 420, 900, 170, t, 2, { env: f => .5 + .5 * Math.sin(f * PI) }); }
  // sağ ön: dev alev dilleri (çerçeve)
  PR.flameBank(1500, W + 120, H + 30, 400, t, 4, { env: f => .5 + .5 * f, wr: .5 });
  // sol ön: kaya kıyısı
  const RK = [[-20, 520], [60, 548], [118, 600], [196, 628], [232, 700], [300, 742], [322, 836], [392, 900], [410, H + 20], [-20, H + 20]];
  PR.rock(RK, { lit: [.85, -.45], hi: .78, mid: .24, lo: .02, seed: 2, th: -.9, cracks: 60 });
  { tx.save(); tx.filter = 'blur(2px)'; tx.strokeStyle = tone(.92, .75); tx.lineWidth = 5; tx.lineJoin = 'round'; tx.beginPath(); poly(tx, RK.slice(1, 9), false); tx.stroke(); tx.restore(); }
  GR.engrave(o.out || ctx, o.cam);
  applyPaper(o.out || ctx, .8);
  applyVignette(o.out || ctx, .65);
}
