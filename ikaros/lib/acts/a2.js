// Perde 2 (P09–P19): Mum ve tüy. Plan listesi: animatik/planlar.json
'use strict';
const A2_MUM = 'lit';
function a2_tuy(p, x, y, l, a, w = .16) { const n = [Math.cos(a + Math.PI / 2), Math.sin(a + Math.PI / 2)], u = [Math.cos(a), Math.sin(a)], pts = [];
  for (let i = 0; i <= 12; i++) { const k = i / 12, ww = Math.sin(Math.PI * Math.pow(k, .8)) * l * w; pts.push([x + u[0] * l * k + n[0] * ww, y + u[1] * l * k + n[1] * ww]); }
  for (let i = 12; i >= 0; i--) { const k = i / 12, ww = Math.sin(Math.PI * Math.pow(k, .8)) * l * w * .55; pts.push([x + u[0] * l * k - n[0] * ww, y + u[1] * l * k - n[1] * ww]); }
  FG.polyInto(p, pts); FG.capsule(p, [x - u[0] * l * .12, y - u[1] * l * .12], [x + u[0] * l * .9, y + u[1] * l * .9], l * .012, l * .006); }
function a2_atolye(pr, t) { pr.sky('sky2', 'sky1', 100, 380, 5); gunes(pr, 1640, 260, 60, 2); const sea = new Path2D(); sea.rect(-50, 640, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 }); pr.ink(FG.glints(100, 1900, 650, 760, 18, 6, t, 40), 'sky1', { sheen: 0, reg: 0 }); pr.ink(FG.ridge(-40, 1960, 1100, 860, 30, 52, 5), 'near'); }

// P09 — C01: tüyler küçükten büyüğe dizilir; ip; mum damlaları
plan('P09', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('sky1'); bant(pr, 760, 1100, 'far'); bant(pr, 760, 790, 'mid');
  const N = 11, tD = Wd('C01', 'dizdi', 0, true), tI = Wd('C01', 'iple'), tM = Wd('C01', 'mumla');
  const tu = new Path2D(); let n = 0;
  for (let i = 0; i < N; i++) { if (st.t < st.at + .25 + i * Math.max(.12, (tD - st.at) / N)) continue; n++; const x = 300 + i * 120, l = 220 + i * 46; a2_tuy(tu, x, 760, l, -Math.PI / 2 - .05 + i * .01, .2); }
  if (n) litInk(pr, tu, 'lit', 'near', 1, -.5, 4);
  if (st.t > tI) { const u = clamp((st.t - tI) / .8), ip = new Path2D(); ip.rect(280, 600, 1300 * u, 7); pr.ink(ip, 'mid', { sheen: 0 }); }
  if (st.t > tM) { const dr = new Path2D(); for (let i = 0; i < N; i++) { const k = clamp((st.t - tM - i * .12) / .4); if (k <= 0) continue; FG.ellipseInto(dr, 300 + i * 120, 752, 26 * k, 18 * k, 0, 16); } pr.ink(dr, A2_MUM, { sheen: .5 }); }
}));

// P10 — C02: İkaros uçuşan tüyleri yakalıyor; Daidalos oturmuş çalışıyor
plan('P10', (ctx, st) => baski(ctx, st, null, pr => {
  a2_atolye(pr, st.lt);
  const Jd = FG.rig({ x: 520, y: 760, h: 48, f: 1, lean: .45, head: .45, armN: [1.2 + Math.sin(st.lt * 3) * .1, -1.1], armF: [1.0, -1.2], legN: [1.55, -1.6], legF: [1.4, -1.5] });
  kanatliFigur(pr, Jd, { light: [1, -.4], litD: 4, look: { beard: true, face: true } });
  const jump = Math.max(0, Math.sin(st.lt * 2.2)) * 26, reach = .5 + .5 * Math.sin(st.lt * 2.2);
  const Ji = FG.rig({ x: 1150, y: 680 - jump, h: 48, f: -1, lean: -.08, head: -.5 - reach * .2, armN: [2.6 + reach * .3, .2], armF: [2.2, .3], legN: [.25 * reach, -.3 * reach], legF: [-.15, -.2] });
  kanatliFigur(pr, Ji, { light: [-1, -.4], litD: 4, look: { curls: true, face: true } });
  const tu = new Path2D(); for (let i = 0; i < 7; i++) { const ph = st.lt * .7 + i * 1.3, x = 1000 + Math.sin(ph) * 260 + i * 30, y = 260 + ((st.lt * 40 + i * 90) % 420); a2_tuy(tu, x, y, 70, ph * 1.4, .22); } pr.ink(tu, 'paper', { sheen: .2 });
}));

// P11 — C02@başparmağıyla: sarı mum diski, başparmak bastırır, iz kalır
plan('P11', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('far'); bant(pr, 0, 280, 'mid');
  const k = E.io2(clamp((st.lt - .3) / 1.0)), sq = 1 - .06 * k;
  const wax = new Path2D(); FG.ellipseInto(wax, 900, 600, 330 / sq, 230 * sq, 0, 48); pr.ink(wax, A2_MUM, { sheen: .6 });
  const iz = new Path2D(); for (let i = 0; i < 5; i++) { const r0 = 30 + i * 22; iz.addPath(SK.ringPath(0, 0, r0, r0 + 7), new DOMMatrix().translate(930, 560).scale(1.25, .8)); } pr.ink(iz, 'sky2', { sheen: 0, alpha: k });
  const tu = new Path2D(); for (let i = 0; i < 4; i++) a2_tuy(tu, 520 + i * 60, 820, 380, -2.3 + i * .12, .2); litInk(pr, tu, 'lit', 'near', 1, -.5, 4);
  const th = new Path2D(); const y = lerp(170, 455, k); FG.capsule(th, [1500, y - 260], [1040, y], 120, 92); FG.capsule(th, [1700, y - 360], [1500, y - 260], 150, 125); litInk(pr, th, 'lit', 'near', 1, -.7, 10);
}));

// P12 — C03: İkaros bir tüyü güneşe doğru tutuyor; güneş arkada büyük
plan('P12', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 480, 820, 5);
  const s = FG.sunRings(1320, 330, 150, 3); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'acc');
  const J = FG.rig({ x: 760, y: 1250, h: 200, f: 1, lean: .08, head: -.55, armN: [2.35 + Math.sin(st.lt) * .03, .35], armF: [.1, 0] });
  kanatliFigur(pr, J, { light: [1, -.6], litD: 12, look: { curls: true, chest: true, face: true } });
  const tu = new Path2D(); const hd = J.armN[2]; a2_tuy(tu, hd[0], hd[1], 300, -1.05 + Math.sin(st.lt * .9) * .04, .2); litInk(pr, tu, 'lit', 'near', 1, -.6, 5);
}));

// P13 — C04: Daidalos kanatlarla havada asılı; aşağıda İkaros bakıyor
plan('P13', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 80, 360, 5); gunes(pr, 1560, 240, 54, 2);
  const sea = new Path2D(); sea.rect(-50, 700, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 });
  pr.ink(FG.cliff(-60, 1250, 760, 1300, 1, 12), 'near');
  const fl = Math.sin(st.lt * 2.6), hov = Math.sin(st.lt * 1.3) * 10;
  const Jd = FG.rig({ x: 760, y: 360 + hov, h: 42, f: 1, lean: .25, head: -.2, legN: [.1, .1], legF: [-.15, .2] });
  kanatliFigur(pr, Jd, { w: { ang: -1.75 - fl * .5, bend: -.3, span: 42 * 6.4, chord: 42 * 2.3, side: -1, seed: 31 }, rootBack: .45, light: [1, -.4], litD: 4, farOff: [12, -8], look: { beard: true, long: true, face: true } });
  const Ji = FG.rig({ x: 1080, y: 760 - 22 * 3.75, h: 22, f: -1, head: -.6, armN: [.4, -.2], armF: [.1, -.1] });
  kanatliFigur(pr, Ji, { light: [-1, -.4], litD: 2, look: { curls: true } });
}));

// P14 — C04@omuzlarına: kanatlar oğlunun omuzlarında (üslup kapısı orta planı)
plan('P14', (ctx, st) => SCENES.orta(ctx, st.lt + .6, st));

// P15 — C05: uyarı afişi: deniz, güneş, orta; ortada küçük figür
plan('P15', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('paper');
  const tD = Wd('C05', 'alçalırsan'), tG = Wd('C05', 'yükselirsen'), tO = Wd('C05', 'arasından');
  const pull = (t0, box) => SK.wipeRegion(box, 'right', clamp((st.t - t0) / .5), 3, 40, 6);
  if (st.t > tG) { bant(pr, 0, 330, 'sky2', { clip: pull(tG, [0, 0, W, 330]) }); const s = FG.sunRings(1500, 165, 70, 2); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0, clip: pull(tG + .2, [0, 0, W, 330]) })); pr.ink(s.disk, 'acc', { clip: pull(tG + .2, [0, 0, W, 330]) }); }
  if (st.t > tD) { bant(pr, 750, 1080, 'mid', { clip: pull(tD, [0, 750, W, 330]) }); const wv = new Path2D(); for (let i = 0; i < 9; i++) { const x = 120 + i * 210; for (let k = 0; k < 3; k++) FG.ellipseInto(wv, x + k * 34, 800 + Math.sin(st.lt * 1.5 + i) * 6, 36, 13, 0, 16); } pr.ink(wv, 'sky1', { sheen: 0, clip: pull(tD + .2, [0, 750, W, 330]) }); }
  bant(pr, 330, 344, 'near'); bant(pr, 736, 750, 'near');
  if (st.t > tO) { const u = E.out3(clamp((st.t - tO) / .6)), fl = Math.sin(st.lt * 3.2); const J = FG.rig({ x: lerp(-120, 640, u), y: 560, h: 30, f: 1, lean: 1.15, head: -.8, legN: [-.12, .35], legF: [-.38, .55] });
    kanatliFigur(pr, J, { w: { ang: -1.65 - fl * .5, bend: -.25, span: 30 * 6.4, chord: 30 * 2.3, side: -1, seed: 5 }, light: [1, -.4], litD: 3, farOff: [6, -4], look: { curls: true } }); }
}), { over: (ctx, st, pal) => basYazi(ctx, 'ORTADAN UÇ', 1300, 560, st.t - Wd('C05', 'arasından'), { px: 150, ls: 10, col: pal.near, dur: .5 }) });

// P16 — C06: deniz bölgesi öne çıkar: dalga tüyü ağırlaştırır
plan('P16', (ctx, st) => baski(ctx, st, null, pr => {
  pr.fillAll('paper'); bant(pr, 0, 70, 'sky2'); bant(pr, 70, 84, 'near');
  const yW = 600, sea = new Path2D(); sea.moveTo(-50, yW); for (let x = -50; x <= 1970; x += 16) sea.lineTo(x, yW + Math.sin(x / 120 + st.lt * 1.4) * 22 + Math.sin(x / 47 + st.lt * 2.1) * 6); sea.lineTo(1970, 1200); sea.lineTo(-50, 1200); sea.closePath();
  const sink = E.io2(clamp(st.lt / Math.max(2, st.d))), tu = new Path2D(); a2_tuy(tu, 1240, 520 + sink * 130, 420, Math.PI * .92, .2);
  litInk(pr, tu, 'lit', 'near', 1, -.5, 5);
  pr.ink(sea, 'mid', { sheen: .2 }); pr.bands('near', 820, 1080, 4, 0, { trap: .2 });
}), { over: (ctx, st, pal) => basYazi(ctx, 'ÇOK ALÇAKTAN DA UÇMA', W / 2, 300, st.t - Wd('C06', 'çok'), { px: 140, ls: 6, col: pal.near, dur: .6 }) });

// P17 — C06@sırrı: Daidalos'un gölgesi uzar; çalılıkta bir keklik (ön işaret)
plan('P17', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 200, 520, 5);
  pr.ink(FG.ridge(-40, 1960, 1100, 760, 30, 61, 5), 'near');
  const gl = E.io2(clamp(st.lt / 2)), gp = new Path2D(); FG.polyInto(gp, [[640, 770], [700, 770], [700 + 900 * gl, 820 + 40 * gl], [640 + 860 * gl, 840 + 40 * gl]]); pr.ink(gp, 'mid', { sheen: 0 });
  const J = FG.rig({ x: 660, y: 770 - 64 * 3.75, h: 64, f: 1, lean: .06, head: .1, armN: [.15, -.1], armF: [-.1, -.1] });
  kanatliFigur(pr, J, { light: [-1, -.4], litD: 5, look: { beard: true, long: true, face: true } });
  const cal = new Path2D(); for (let i = 0; i < 9; i++) FG.ellipseInto(cal, 1340 + i * 34, 770 - Math.sin(i / 8 * Math.PI) * 50, 44, 34, 0, 14); pr.ink(cal, 'far');
  pr.ink(keklikPath(1440, 742, 54, -1, 0, Math.max(0, Math.sin(st.lt * 1.4))), 'near', { sheen: .2 });
}));

// P18 — C07: Daidalos ufku gösterir; İkaros arkasında
plan('P18', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 100, 400, 5); gunes(pr, 1500, 420, 70, 3);
  const sea = new Path2D(); sea.rect(-50, 640, 2020, 500); pr.ink(sea, 'mid', { sheen: 0 }); pr.ink(FG.glints(900, 1900, 650, 900, 22, 8, st.lt, 50), 'sky1', { sheen: 0, reg: 0 });
  pr.ink(FG.cliff(-60, 1000, 700, 1300, 1, 14), 'near');
  const pt = E.out3(clamp((st.t - Wd('C07', 'izle')) / .6));
  const Jd = FG.rig({ x: 820, y: 700 - 40 * 3.75, h: 40, f: 1, lean: .05, head: -.05, armN: [lerp(.4, 1.6, pt), -.05], armF: [-.1, -.2] });
  kanatliFigur(pr, Jd, { w: { ang: 1.85, bend: .25, span: 40 * 4.4, chord: 40 * 1.7, side: 1, seed: 8 }, armInWing: false, light: [1, -.3], litD: 3, farOff: [-3, -1], look: { beard: true, long: true } });
  const Ji = FG.rig({ x: 640, y: 700 - 34 * 3.75, h: 34, f: 1, head: -.05, armN: [.15, -.1], armF: [-.1, -.1] });
  kanatliFigur(pr, Ji, { w: { ang: 1.85, bend: .25, span: 34 * 4.4, chord: 34 * 1.7, side: 1, seed: 9 }, light: [1, -.3], litD: 3, farOff: [-3, -1], look: { curls: true } });
}));

// P19 — C08: iki baş profilden; baba oğlunun alnını öper; tek damla gözyaşı
plan('P19', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 380, 760, 5);
  const k = E.io2(clamp((st.t - Wd('C08', 'öptü')) / 1.0));
  const Ji = FG.rig({ x: 1120, y: 1250, h: 170, f: -1, lean: -.02, head: -.12, armN: [.05, 0], armF: [.05, 0] });
  kanatliFigur(pr, Ji, { light: [-1, -.5], litD: 8, look: { curls: true, chest: true, face: true } });
  const Jd = FG.rig({ x: 690 + k * 36, y: 1160, h: 185, f: 1, lean: .1 + k * .12, head: .3 + k * .15, armN: [.05, 0], armF: [.05, 0] });
  kanatliFigur(pr, Jd, { light: [1, -.5], litD: 8, look: { beard: true, long: true, chest: true, face: true } });
  const dt = clamp((st.t - Wd('C08', 'ıslandı')) / 2.5); if (dt > 0) { const yy = Jd.Hd[1] + 30 + dt * 120, d = new Path2D(); FG.ellipseInto(d, Jd.Hd[0] + 50, yy, 9, 14, 0, 14); pr.ink(d, 'acc', { sheen: .5, reg: 0 }); }
}));
