// Perde 6 (P43–P53): Üç uçuş · Bruegel · son soru · bitiş. Kırmızı çizgi: üç panel Golgota gibi dizilmez (ortası en alçak); Bruegel'de bacaklar küçük.
'use strict';
function a6_panel(pr, x, y, w, h, fn, k) {
  if (k <= 0) return;
  const clip = new Path2D(); clip.rect(x, y, w, h);
  const fr = new Path2D(); fr.rect(x - 14, y - 14, w + 28, h + 28); fr.rect(x, y, w, h); pr.ink(fr, 'paper', { rule: 'evenodd', sheen: 0, clip: SK.wipeRegion([x - 20, y - 20, w + 40, h + 40], 'down', k, 3, 30, 6) });
  const c2 = new Path2D(); c2.addPath(clip); const ctx = pr.ctx; ctx.save(); ctx.clip(SK.wipeRegion([x, y, w, h], 'down', k, 5, 30, 6)); ctx.clip(c2); fn(); ctx.restore();
}
function a6_kursu(pr, x, y, h) { const p = new Path2D(); p.rect(x - h * .9, y, h * 1.8, h * 3); p.rect(x - h * 1.1, y - h * .18, h * 2.2, h * .22); pr.ink(p, 'far', { sheen: .2 }); }

// P43 — G01: üç panelli afiş: güneşe giden çocuk (yüksek) / keklik (alçak) / usta (orta)
plan('P43', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('near');
  const k = s => E.out3(clamp((st.t - s) / .5)), t1 = Wd('G01', 'güneşe'), t2 = Wd('G01', 'keklik'), t3 = Wd('G01', 'usta');
  a6_panel(pr, 120, 90, 520, 720, () => { bant(pr, 90, 810, 'sky2'); gunes(pr, 470, 220, 60, 2); a3_ucan(pr, st.lt, 300, 320, 26, 1.3, false, { rise: .4 }); }, k(t1));
  a6_panel(pr, 700, 330, 520, 720, () => { bant(pr, 330, 1050, 'sky1'); const c = new Path2D(); for (let i = 0; i < 4; i++) FG.ellipseInto(c, 760 + i * 150, 940, 110, 80, 0, 18); c.rect(690, 940, 540, 120); pr.ink(c, 'mid'); pr.ink(keklikPath(960, 875, 80, 1, .4 + .4 * Math.sin(st.lt * 7), .1), 'near'); }, k(t2));
  a6_panel(pr, 1280, 210, 520, 720, () => { bant(pr, 210, 930, 'sky2'); bant(pr, 540, 610, 'lit'); a3_ucan(pr, st.lt, 1540, 570, 30, 0, true); }, k(t3));
}));

// P44 — G02: usta "ortada" değildi: kürsünün tepesinde, orta bandın üstünde
plan('P44', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 80, 360, 5);
  bant(pr, 560, 650, 'lit');
  const k = E.out3(clamp(st.lt / 1.2)), ky = lerp(980, 640, k); a6_kursu(pr, 960, ky, 70);
  const J = FG.rig({ x: 960, y: ky - 50 * 3.75 + 8, h: 50, f: 1, lean: -.04, head: -.18, armN: [.2, -.1], armF: [-.1, -.1] });
  kanatliFigur(pr, J, { light: [1, -.4], litD: 4, faceFill: false, look: { beard: true, long: true, face: true } });
  pr.ink(FG.ridge(-40, 1960, 1100, 980, 20, 121, 4), 'near');
}));

// P45 — G03: yazı afişi
plan('P45', (ctx, st) => baski(ctx, st, null, pr => { pr.fillAll('near'); bant(pr, 520, 534, 'lit'); }),
  { over: (ctx, st, pal) => { basYazi(ctx, 'YA EN İYİSİ', W / 2, 400, st.t - Wd('G03', 'en'), { px: 190, ls: 12, col: pal.paper, dur: .45 }); basYazi(ctx, 'YA HİÇ', W / 2, 680, st.t - Wd('G03', 'hiç'), { px: 190, ls: 12, col: pal.acc, dur: .45 }); } });

// P46 — G04: bölünmüş kare: solda kürsüdeki usta (EN İYİSİ), sağda alçakta keklik (HİÇ)
plan('P46', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('sky1'); const sag = new Path2D(); sag.rect(960, -50, 1100, 1200); pr.ink(sag, 'sky2', { sheen: 0 }); bant(pr, 0, 0, 'near');
  const ay = new Path2D(); ay.rect(952, -50, 16, 1200); pr.ink(ay, 'near', { sheen: 0 });
  a6_kursu(pr, 480, 660, 64); const J = FG.rig({ x: 480, y: 660 - 48 * 3.75 + 8, h: 48, f: 1, head: -.15, armN: [.2, -.1], armF: [-.1, -.1] }); kanatliFigur(pr, J, { light: [1, -.4], litD: 4, look: { beard: true, long: true } });
  const c = new Path2D(); for (let i = 0; i < 5; i++) FG.ellipseInto(c, 1040 + i * 200, 960, 140, 100, 0, 18); c.rect(960, 960, 1000, 200); pr.ink(c, 'mid');
  pr.ink(keklikPath(1440, 890, 110, -1, 0, .2), 'near');
  pr.ink(FG.ridge(-40, 960, 1100, 1000, 10, 122, 3), 'near');
}), { over: (ctx, st, pal) => { basYazi(ctx, 'EN İYİSİ', 480, 150, st.t - Wd('G04', 'daidalos'), { px: 110, ls: 8, col: pal.near, dur: .4 }); basYazi(ctx, 'HİÇ', 1440, 150, st.t - Wd('G04', 'keklik'), { px: 110, ls: 8, col: pal.paper, dur: .4 }); } });

// P47 — G05: ıslanan tüyler sessizce, yavaşça batar (su altı kesiti)
plan('P47', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('sky2'); bant(pr, 0, 140, 'sky1');
  const yW = 150, sea = new Path2D(); sea.moveTo(-50, yW); for (let x = -50; x <= 1970; x += 16) sea.lineTo(x, yW + Math.sin(x / 130 + st.lt) * 10); sea.lineTo(1970, 1200); sea.lineTo(-50, 1200); sea.closePath(); pr.ink(sea, 'mid', { sheen: 0 });
  bant(pr, 520, 1100, 'far'); bant(pr, 820, 1100, 'near');
  const p = new Path2D(), r = rng(31); for (let i = 0; i < 7; i++) { const x = 260 + i * 230 + Math.sin(st.lt * .4 + i) * 40, y = 160 + ((st.lt * 34 + r() * 700) % 900), a = Math.PI / 2 + Math.sin(st.lt * .6 + i) * .5; a2_tuy(p, x, y, 130, a, .14); }
  pr.ink(p, 'lit', { sheen: .1 });
}));

// P48 — G06: İkaros'un uçuşu, sevinç (yakın; sabah paleti geri döner)
plan('P48', (ctx, st) => baski(ctx, st, { cx: 960 + st.lt * 20, cy: 540 }, pr => {
  pr.sky('sky2', 'sky1', 60, 340, 5); gunes(pr, 1720 + st.lt * 19, 200, 70, 3);
  pr.ink(FG.cloud(500 + st.lt * 14, 900, 900, 160, 21), 'paper', { sheen: 0 });
  a3_ucan(pr, st.lt, 980 + st.lt * 20, 560, 120, .7, false, { rise: .25 });
}));

// P49 — G07 (ters açı): bulutların üstünde İkaros en tepede; babası aşağıda, bulutların altında küçük
plan('P49', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 120, 520, 6); gunes(pr, 1500, 170, 80, 3);
  a3_ucan(pr, st.lt, 1100, 300, 34, 1.3, false, { rise: .3 });
  const cl = new Path2D(); for (let i = 0; i < 9; i++) FG.ellipseInto(cl, 80 + i * 240, 760 + Math.sin(i * 2.1) * 30, 200, 90, 0, 22); cl.rect(-50, 760, 2020, 400); pr.ink(cl, 'paper', { sheen: 0 });
  a3_ucan(pr, st.lt, 420, 690, 12, 0, true);
}));

// P50 — G08: Bruegel'e saygı (kopya değil): önde saban süren çiftçi, göğe bakan çoban, gemi; köşede denizde iki küçük bacak
plan('P50', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 60, 320, 4);
  const sun = FG.sunRings(1500, 470, 60, 2); sun.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(sun.disk, 'acc');
  const sea = new Path2D(); sea.rect(-50, 480, 2020, 700); pr.ink(sea, 'far', { sheen: 0 });
  pr.ink(FG.glints(900, 1900, 500, 900, 30, 4, st.lt, 50), 'sky1', { sheen: 0, reg: 0 });
  const gm = new Path2D(); FG.polyInto(gm, [[1140, 700], [1400, 700], [1360, 750], [1170, 750]]); FG.polyInto(gm, [[1260, 470], [1262, 700], [1150, 690]]); FG.polyInto(gm, [[1270, 500], [1272, 700], [1360, 690]]); gm.rect(1262, 450, 8, 250); pr.ink(gm, 'near', { sheen: .1 });
  const tepe = new Path2D(); tepe.moveTo(-50, 640); tepe.bezierCurveTo(400, 600, 900, 700, 1100, 1100); tepe.lineTo(-50, 1100); tepe.closePath(); pr.ink(tepe, 'mid', { sheen: .1 });
  const sv = new Path2D(); for (let i = 0; i < 8; i++) sv.rect(-50, 760 + i * 46, 900 - i * 60, 12); pr.ink(sv, 'near', { sheen: 0, clip: tepe });
  a3_tanik(pr, 430, 900, 52, 'ciftci', 0, st.lt);
  a3_tanik(pr, 820, 690, 26, 'coban', 1, st.lt);
  const koyun = new Path2D(); for (let i = 0; i < 5; i++) FG.ellipseInto(koyun, 700 + i * 40, 690 - (i % 2) * 8, 18, 12, 0, 12); pr.ink(koyun, 'paper', { sheen: 0 });
  const bc = new Path2D(), sp = Math.sin(st.lt * 5) * 6; FG.capsule(bc, [1620, 900], [1612, 862 + sp], 6, 5); FG.capsule(bc, [1636, 900], [1650, 866 - sp], 6, 5); pr.ink(bc, 'lit', { sheen: 0 });
  const sc = new Path2D(); FG.ellipseInto(sc, 1630, 904, 40, 8, 0, 16); pr.ink(sc, 'paper', { sheen: 0, reg: 0 });
}));

// P51 — G08@bacak: denizde iki bacak ve tüyler; dalda bir keklik
plan('P51', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('sky1'); const sea = new Path2D(); sea.rect(-50, 560, 2020, 600); pr.ink(sea, 'far', { sheen: 0 });
  const bc = new Path2D(), sp = Math.sin(st.lt * 4) * 14; FG.capsule(bc, [900, 600], [870, 330 + sp], 30, 24); FG.capsule(bc, [960, 600], [1010, 350 - sp], 30, 24); pr.ink(bc, 'lit', { sheen: .2 });
  const sc = new Path2D(); for (let i = 0; i < 7; i++) { const a = -Math.PI + i * .5; FG.ellipseInto(sc, 930 + Math.cos(a) * 150, 590 + Math.sin(a) * 40, 30, 12, a, 12); } pr.ink(sc, 'paper', { sheen: 0 });
  const p = new Path2D(); for (let i = 0; i < 6; i++) a2_tuy(p, 500 + i * 180, 640 + (i % 2) * 60 + Math.sin(st.lt + i) * 8, 110, i * 1.1, .14); pr.ink(p, 'near', { sheen: .1 });
  const dal = new Path2D(); FG.capsule(dal, [-50, 160], [520, 220], 16, 8); pr.ink(dal, 'near', { sheen: 0 }); pr.ink(keklikPath(330, 150, 110, 1, 0, .5), 'near');
}));

// P52 — G09: boş gök, güneş; tek tüy yükselir; soru basılır
plan('P52', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 80, 380, 5); gunes(pr, 1500, 260, 80, 3);
  const p = new Path2D(); a2_tuy(p, 700 + Math.sin(st.lt * .9) * 40, lerp(1000, 520, clamp(st.lt / Math.max(4, st.d))), 180, -1.3 + Math.sin(st.lt * 1.2) * .3, .16); litInk(pr, p, 'lit', 'near', 1, -.5, 4);
}), { over: (ctx, st, pal) => basYazi(ctx, 'HANGİ YÜKSEKLİKTE UÇARDIN?', W / 2, 760, st.t - Wd('G09', 'hangi'), { px: 120, ls: 8, col: pal.near, dur: .6 }) });

// P53 — H01: bitiş ekranı: solda başlık ve küçük kanatlı; sağ yarı YouTube öğelerine boş (video: x 1000–1840, y 160–640; abone: x 1300–1520, y 720–940)
plan('P53', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('near'); bant(pr, 1040, 1080, 'mid');
  const fr = new Path2D(); fr.rect(980, 140, 880, 520); pr.ink(fr, 'mid', { sheen: 0 });
  a3_ucan(pr, st.lt, 470, 640, 40, 1.3, false, { rise: .2, light: [1, -.6] });
  gunes(pr, 720, 320, 44, 2);
}), { over: (ctx, st, pal) => { basYazi(ctx, 'ZAMAN KURYESİ', 480, 860, st.lt - .3, { px: 120, ls: 10, col: pal.paper, dur: .5 }); basYazi(ctx, 'GEÇMİŞTEN BUGÜNE BİR SORU', 480, 950, st.lt - .8, { font: FONT.metin(36, 600), ls: 6, col: pal.lit, dur: .5 }); } });
