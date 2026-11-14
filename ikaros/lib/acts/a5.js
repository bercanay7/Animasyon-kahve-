// Perde 5 (P33–P42): Kekliğin sevinci. Kırmızı çizgi: itiş gösterilmez; Athena yalnız ışık ve baykuş; kenarda aşağı bakan figür yok.
'use strict';
function a5_hendek(pr, t) { pr.sky('sky2', 'sky1', 60, 360, 5); pr.ink(FG.ridge(-40, 1960, 1100, 640, 40, 91, 5), 'far'); const m = new Path2D(); m.moveTo(-50, 780); for (let x = -50; x <= 1970; x += 20) m.lineTo(x, 780 + Math.sin(x / 160) * 20); m.lineTo(1970, 1200); m.lineTo(-50, 1200); m.closePath(); pr.ink(m, 'near', { sheen: .1 }); const sz = new Path2D(); for (let i = 0; i < 26; i++) { const x = 40 + i * 74 + Math.sin(i * 3.1) * 20, h = 90 + (i * 37 % 70); FG.capsule(sz, [x, 800], [x + Math.sin(t * .8 + i) * 8, 800 - h], 5, 2); } pr.ink(sz, 'near', { sheen: 0 }); }
function a5_baykus(x, y, s) { const p = new Path2D(); FG.ellipseInto(p, x, y, s * .42, s * .55, 0, 22); FG.polyInto(p, [[x - s * .38, y - s * .42], [x - s * .3, y - s * .75], [x - s * .12, y - s * .5]]); FG.polyInto(p, [[x + s * .38, y - s * .42], [x + s * .3, y - s * .75], [x + s * .12, y - s * .5]]); return p; }
function a5_akropolis(pr) { pr.ink(FG.ridge(300, 1600, 1100, 520, 140, 101, 6), 'near'); const sur = new Path2D(); for (let i = 0; i < 10; i++) sur.rect(560 + i * 64, 480 - (i % 2) * 14, 52, 70 + (i % 2) * 14); sur.rect(560, 520, 640, 40); pr.ink(sur, 'near', { sheen: .2 }); }

// P33 — F01: kıyıda Daidalos sırtı dönük, bir kayada oturuyor (uzak)
plan('P33', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 120, 460, 5); const sea = new Path2D(); sea.rect(-50, 620, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 });
  pr.ink(FG.glints(200, 1800, 630, 760, 16, 4, st.lt, 40), 'sky1', { sheen: 0, reg: 0 });
  pr.ink(FG.ridge(-40, 1960, 1100, 780, 30, 92, 5), 'near'); { const rk = new Path2D(); FG.ellipseInto(rk, 960, 790, 120, 60, 0, 24); rk.rect(840, 790, 240, 60); pr.ink(rk, 'far', { sheen: .1 }); }
  const J = FG.rig({ x: 950, y: 732, h: 40, f: -1, lean: .22, head: .75 + Math.sin(st.lt * .5) * .03, armN: [1.2, -1.0], armF: [1.1, -1.0], legN: [1.55, -1.45], legF: [1.45, -1.5] });
  kanatliFigur(pr, J, { light: [1, -.3], litD: 3, look: { beard: true, long: true } });
}));

// P34 — F02: çamurlu hendekte keklik kanat çırpıyor, ötüyor
plan('P34', (ctx, st) => baski(ctx, st, null, pr => {
  a5_hendek(pr, st.lt);
  const fl = Math.max(0, Math.sin(st.lt * 5)) * (st.t > Wd('F02', 'kanatlarını') ? 1 : 0);
  litInk(pr, keklikPath(1000, 700, 300, -1, fl, .4 + .3 * Math.sin(st.lt * 3)), 'lit', 'near', -1, -.4, 6);
}));

// P35 — F03: kekliğin silueti yeniden basılır: aynı yerde bir çocuk silueti; Ovidius'un sözü
plan('P35', (ctx, st) => baski(ctx, st, null, pr => {
  a5_hendek(pr, st.lt);
  const tC = Wd('F03', 'çocuktu'), k = clamp((st.t - tC) / .45);
  if (k < 1) pr.ink(keklikPath(1000, 700, 300, -1, 0, .3), 'near', { clip: (() => { const c = SK.wipeRegion([0, 0, W, H], 'right', k, 7, 40, 6), inv = new Path2D(); inv.rect(-1e4, -1e4, 2e4, 2e4); inv.addPath(c); return inv; })(), rule: 'nonzero' });
  if (k > 0) { const J = FG.rig({ x: 1000, y: 800 - 46 * 3.75, h: 46, f: -1, head: -.1, armN: [.2, -.2], armF: [-.1, -.1] }); const fg = FG.figure(J, { curls: true }); pr.ink(fg.far, 'near', { clip: SK.wipeRegion([0, 0, W, H], 'right', k, 7, 40, 6) }); pr.ink(fg.body, 'near', { clip: SK.wipeRegion([0, 0, W, H], 'right', k, 7, 40, 6) }); if (fg.belt) pr.ink(fg.belt, 'lit', { sheen: 0, clip: SK.wipeRegion([0, 0, W, H], 'right', k, 7, 40, 6) }); }
}), { over: (ctx, st, pal) => {
  basYazi(ctx, '“SENİN BİTMEYECEK SUÇUN, DAİDALOS.”', W / 2, 200, st.t - Wd('F03', 'ovidius'), { px: 92, ls: 4, col: pal.near, dur: .6 });
  basYazi(ctx, 'OVİDİUS · DÖNÜŞÜMLER · VIII.240', W / 2, 300, st.t - Wd('F03', 'ovidius') - .5, { font: FONT.metin(40, 600), ls: 6, col: pal.near, dur: .5 });
} });

// P36 — F04: atölye: çırak testereyle çalışıyor; arkada büyük Daidalos bakıyor (sabah)
plan('P36', (ctx, st) => baski(ctx, st, null, pr => {
  a2_atolye(pr, st.lt);
  const tz = new Path2D(); tz.rect(980, 760, 520, 40); FG.capsule(tz, [1010, 800], [1010, 950], 14, 12); FG.capsule(tz, [1470, 800], [1470, 950], 14, 12); pr.ink(tz, 'far');
  const saw = Math.sin(st.lt * 6) * 30;
  const Jc = FG.rig({ x: 1250, y: 760 - 30 * 1.0, h: 34, f: -1, lean: .35, head: .3, armN: [1.3 + saw / 200, -.6], armF: [1.1, -.8], legN: [.1, -.05], legF: [-.1, 0] });
  kanatliFigur(pr, Jc, { light: [1, -.4], litD: 3, look: { curls: true } });
  const sb = new Path2D(); sb.rect(1080 + saw, 744, 150, 12); for (let i = 0; i < 8; i++) FG.polyInto(sb, [[1080 + saw + i * 19, 756], [1090 + saw + i * 19, 768], [1099 + saw + i * 19, 756]]); pr.ink(sb, 'lit', { sheen: 0 });
  const Jd = FG.rig({ x: 560, y: 600, h: 70, f: 1, lean: .04, head: .15, armN: [.3, -1.6], armF: [.2, -1.4] });
  kanatliFigur(pr, Jd, { light: [1, -.4], litD: 4, faceFill: false, look: { beard: true, long: true, face: true } });
}));

// P37 — F04@testereyi: icat afişi: balık kılçığı → testere; iki kollu pergel
plan('P37', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('paper'); bant(pr, 0, 90, 'sky2'); bant(pr, 990, 1080, 'sky2');
  const k = E.io2(clamp((st.lt - .4) / 1.2));
  const sp = new Path2D(); sp.rect(220, 520, 700, 16); for (let i = 0; i < 16; i++) { const x = 250 + i * 42; FG.polyInto(sp, [[x, 536], [x + lerp(-20, 18, k), lerp(640, 580, k)], [x + 18, 536]]); if (k < .98) FG.polyInto(sp, [[x, 520], [x - 20, lerp(410, 520, k)], [x + 18, 520]]); }
  const sap = new Path2D(); FG.capsule(sap, [110, 528], [215, 528], 34, 30); pr.ink(sp, 'near', { sheen: .2 }); pr.ink(sap, 'far', { sheen: .2 });
  const ang = .32 + Math.sin(st.lt * .9) * .08, pg = new Path2D(), top = [1430, 300];
  FG.capsule(pg, top, [top[0] - Math.sin(ang) * 520, top[1] + Math.cos(ang) * 520], 18, 8); FG.capsule(pg, top, [top[0] + Math.sin(ang) * 520, top[1] + Math.cos(ang) * 520], 18, 8); FG.ellipseInto(pg, top[0], top[1], 34, 34, 0, 18);
  litInk(pr, pg, 'lit', 'near', 1, -.5, 4);
  const yay = new Path2D(); const r0 = 520 * Math.sin(ang) * .98; for (let i = 0; i <= 30; i++) { const a = Math.PI / 2 - .5 + i / 30; } yay.addPath(SK.ringPath(top[0], top[1] + 520 * Math.cos(ang), r0, r0 + 5)); pr.ink(yay, 'mid', { sheen: 0, clip: (() => { const c = new Path2D(); c.rect(900, top[1] + 520 * Math.cos(ang) - 40, 1100, 140); return c; })() });
}));

// P38 — F05: Akropolis kayası alacakaranlıkta; tepede iki küçük figür; itiş gösterilmez
plan('P38', (ctx, st) => baski(ctx, st, { cx: lerp(960, 1180, E.io2(st.p)), cy: lerp(540, 470, E.io2(st.p)), z: lerp(1, 1.3, E.io2(st.p)) }, pr => {
  pr.sky('sky2', 'sky1', 120, 520, 6);
  a5_akropolis(pr);
  for (const [x, hh, beard] of [[1230, 22, true], [1290, 15, false]]) { const J = FG.rig({ x, y: 545 - hh * 3.75, h: hh, f: -1, armN: [.2, -.1], armF: [-.1, -.1] }); const fg = FG.figure(J, { beard, long: beard, curls: !beard }); pr.ink(fg.far, 'near'); pr.ink(fg.body, 'near'); }
}));

// P39 — F05@yalan: Daidalos'un profili; arkada boş kale kenarı
plan('P39', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 80, 380, 5);
  pr.ink(FG.ridge(1100, 1960, 1100, 640, 80, 102, 5), 'far');
  const yl = E.io2(clamp((st.t - Wd('F05', 'yalan')) / 1.2)); const J = FG.rig({ x: 760, y: 1250, h: 220, f: 1, lean: .02 + yl * .06, head: .12 + yl * .42, armN: [.05, 0], armF: [.05, 0] });
  kanatliFigur(pr, J, { light: [-1, -.4], litD: 4, faceFill: false, look: { beard: true, long: true, chest: true, face: true } });
}));

// P40 — F06: ışık huzmesi; düşen küçük siluet tüy patlamasıyla kekliğe döner; surda baykuş
plan('P40', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 100, 420, 5);
  const hz = new Path2D(); FG.polyInto(hz, [[200, -40], [520, -40], [1180, 1100], [760, 1100]]); pr.ink(hz, 'acc', { sheen: 0 });
  a5_akropolis(pr);
  pr.ink(a5_baykus(640, 432, 56), 'near', { sheen: .1 });
  const tY = Wd('F06', 'kuşa'), k = clamp((st.t - tY) / .5), y = lerp(560, 760, clamp(st.lt / 1.4));
  if (k < 1) { const J = FG.rig({ x: 960, y, h: 16, f: -1, lean: .5, head: .2, armN: [.8, -.6], armF: [.6, -.7], legN: [.8, -1.2], legF: [.6, -1.0] }); const fg = FG.figure(J, { curls: true }); pr.ink(fg.body, 'paper'); }
  if (k > 0) { const p = new Path2D(), r = rng(4); for (let i = 0; i < 12; i++) { const a = r() * 6.28, d = 30 + k * 120 * r(); a2_tuy(p, 960 + Math.cos(a) * d, y + Math.sin(a) * d, 26, a, .18); } pr.ink(p, 'paper', { sheen: 0 }); pr.ink(keklikPath(960 - k * 260, y - k * 40, 90, -1, Math.max(0, Math.sin(st.lt * 8)), .4), 'paper'); }
}));

// P41 — F07: keklik çitlerin üstünden alçaktan uçar; çit dibinde yuva
plan('P41', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 80, 420, 5); pr.ink(FG.ridge(-40, 1960, 1100, 700, 50, 111, 5), 'far');
  const cit = new Path2D(); for (let i = 0; i < 9; i++) FG.ellipseInto(cit, 100 + i * 230, 840, 160, 110, 0, 20); cit.rect(-50, 840, 2020, 300); pr.ink(cit, 'near', { sheen: .1 });
  const yuva = new Path2D(); FG.ellipseInto(yuva, 1520, 900, 70, 22, 0, 16); pr.ink(yuva, 'lit', { sheen: 0 }); const yum = new Path2D(); for (let i = 0; i < 3; i++) FG.ellipseInto(yum, 1495 + i * 24, 886, 12, 15, 0, 12); pr.ink(yum, 'paper', { sheen: 0, reg: 0 });
  const x = lerp(-100, 2000, clamp(st.lt / Math.max(4, st.d))), fl = Math.sin(st.lt * 9);
  pr.ink(keklikPath(x, 690 + Math.sin(st.lt * 2) * 10, 90, 1, .5 + .5 * fl, .1), 'near');
}));

// P42 — F08: uyarı afişi yeniden; üstüne Daidalos'un profili kayık baskıyla düşer
plan('P42', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('paper'); bant(pr, 0, 330, 'sky2'); bant(pr, 750, 1080, 'mid'); bant(pr, 330, 344, 'near'); bant(pr, 736, 750, 'near');
  const s = FG.sunRings(1500, 165, 70, 2); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'acc');
  const k = E.out3(clamp((st.t - Wd('F08', 'atmıştı')) / .6));
  const J = FG.rig({ x: 820, y: 1300, h: 230, f: 1, lean: .02, head: .1, armN: [.05, 0], armF: [.05, 0] });
  const fg = FG.figure(J, { beard: true, long: true, chest: true });
  pr.ink(fg.body, 'near', { reg: [lerp(60, 3, k), lerp(-40, 2, k)] });
}), { over: (ctx, st, pal) => basYazi(ctx, 'ORTADAN UÇ', 1440, 560, 99, { px: 150, ls: 10, col: pal.near, dur: .5 }) });
