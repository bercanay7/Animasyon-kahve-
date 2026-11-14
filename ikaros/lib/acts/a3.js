// Perde 3 (P20–P26): Tanrılar gibi. Plan listesi: animatik/planlar.json
'use strict';
// uçan figür (tek çağrı): x, y, h, faz, sakal; o.rise: gövde eğimi (+ yukarı tırmanış)
function a3_ucan(pr, t, x, y, hh, ph, beard, o = {}) {
  const cyc = ((t * .55 + ph * .2) % 1 + 1) % 1, down = cyc < .4, u = down ? cyc / .4 : (cyc - .4) / .6;
  const angW = down ? lerp(-1.6, -2.95, E.io2(u)) : lerp(-2.95, -1.6, E.io2(u)), open = down ? 1 : .72 + .28 * Math.abs(u - .5) * 2;
  const J = FG.rig({ x, y: y + (down ? -6 : 6) * Math.sin(u * Math.PI) * hh / 40, h: hh, f: o.f || 1, lean: 1.12 - (o.rise || 0), head: -.85 + (o.rise || 0) * .3, legN: [-.12, .35], legF: [-.38, .55] });
  kanatliFigur(pr, J, { w: { ang: (o.f || 1) > 0 ? angW - (o.rise || 0) * .5 : Math.PI - angW, bend: -.25, span: hh * 6.4 * open, chord: hh * 2.3 * (.8 + .2 * open), side: -(o.f || 1), seed: ph * 10 + 3, farDa: .6 }, light: o.light || [.8, -.6], litD: Math.max(2, hh * .06), farOff: [hh * .3, -hh * .2], faceFill: false, look: { beard, curls: !beard, face: hh > 60 } });
  return J;
}
function a3_tanik(pr, x, yBase, hh, tur, bak, t) {
  // tur: 'balikci' oturur, olta; 'coban' değnek; 'ciftci' saban kolu. bak: 0..1 baş kalkar
  if (tur === 'balikci') { const J = FG.rig({ x, y: yBase - hh * 1.6, h: hh, f: 1, lean: .3 - bak * .45, head: .3 - bak * 1.4, armN: [1.25, -.6], armF: [1.05, -.4], legN: [1.45, -1.7], legF: [1.3, -1.5] }); const fb = FG.figure(J, {}); pr.ink(fb.far, 'near'); litInk(pr, fb.body, 'lit', 'near', 1, -.4, 2); const rod = new Path2D(); FG.capsule(rod, J.armN[2], [J.armN[2][0] + hh * 6, J.armN[2][1] - hh * 3 + Math.sin(t * 2) * 3], hh * .1, hh * .07); pr.ink(rod, 'near', { sheen: 0 }); return; }
  const J = FG.rig({ x, y: yBase - hh * 3.75, h: hh, f: tur === 'coban' ? -1 : 1, lean: tur === 'ciftci' ? .3 - bak * .2 : .05, head: .1 - bak * 1.25, armN: tur === 'coban' ? [.6, -.4] : [1.0, -.3], armF: [.8, -.5], legN: [.12, -.05], legF: [-.14, 0] });
  const fb = FG.figure(J, { beard: tur === 'ciftci' }); pr.ink(fb.far, 'near'); litInk(pr, fb.body, 'lit', 'near', 1, -.4, 2); if (fb.belt) pr.ink(fb.belt, 'lit', { sheen: 0 });
  const tool = new Path2D();
  if (tur === 'coban') FG.capsule(tool, [J.armN[2][0], yBase], [J.armN[2][0] - hh * .3, J.armN[2][1] - hh * 1.4], hh * .08, hh * .07);
  else { FG.capsule(tool, J.armN[2], [J.armN[2][0] + hh * 2.2, yBase - hh * .2], hh * .09, hh * .08); FG.polyInto(tool, [[J.armN[2][0] + hh * 2.1, yBase - hh * .5], [J.armN[2][0] + hh * 3.2, yBase], [J.armN[2][0] + hh * 1.9, yBase]]); }
  pr.ink(tool, 'near', { sheen: 0 });
}

// P20 — D01: kalkış ve uçuş (üslup kapısı uçuş sahnesi)
plan('P20', (ctx, st) => SCENES.ucus(ctx, st.lt, st));

// P21 — D01@kuş: daha yakın; Daidalos önde, oğluna dönüp dönüp bakar (baş geriye kalkar)
plan('P21', (ctx, st) => baski(ctx, st, { cx: 960 + st.lt * 30, cy: 540 }, pr => {
  const dx = st.lt * 30;
  pr.sky('sky2', 'sky1', 60, 300, 4); gunes(pr, 1700 + dx * .96, 160, 52, 2);
  pr.ink(FG.cloud(700 + dx * .65, 820, 700, 130, 8), 'paper', { sheen: 0 }); pr.ink(FG.cloud(1500 + dx * .65, 900, 520, 100, 9), 'paper', { sheen: 0 });
  const bak = Math.max(0, Math.sin(st.lt * 1.3));
  a3_ucan(pr, st.lt, 960 + dx + 420, 430, 80, 0, true, { rise: -bak * .25 });
  a3_ucan(pr, st.lt, 960 + dx - 470, 690, 62, 1.3, false);
}));

// P22 — D02 (ters açı): yerden bakış; balıkçı, çoban, çiftçi başlarını kaldırır; gökte iki küçük kanatlı
plan('P22', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 80, 380, 5); gunes(pr, 1560, 220, 60, 2);
  for (const [x, y, ph] of [[860, 300, 0], [760, 360, 1.3]]) a3_ucan(pr, st.lt, x + st.lt * 18, y, 14, ph, ph === 0);
  pr.ink(FG.ridge(-40, 760, 1100, 820, 40, 71, 5), 'far'); const sea = new Path2D(); sea.rect(700, 860, 1300, 300); pr.ink(sea, 'mid', { sheen: 0 });
  pr.ink(FG.ridge(-40, 1960, 1100, 930, 26, 72, 4), 'near');
  const bak = t0 => E.io2(clamp((st.t - t0) / .8));
  a3_tanik(pr, 1400, 940, 34, 'balikci', bak(Wd('D02', 'balıkçı')), st.lt);
  a3_tanik(pr, 900, 950, 40, 'coban', bak(Wd('D02', 'çoban')), st.lt);
  a3_tanik(pr, 330, 955, 44, 'ciftci', bak(Wd('D02', 'çiftçi')), st.lt);
}));

// P23 — D03: çiftçinin başı profilden, göğe bakıyor
plan('P23', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 60, 300, 4);
  for (const [x, y, ph] of [[1450, 230, 0], [1360, 270, 1.3]]) a3_ucan(pr, st.lt, x + st.lt * 10, y, 12, ph, ph === 0);
  pr.ink(FG.ridge(-40, 1960, 1100, 900, 30, 73, 4), 'far');
  const J = FG.rig({ x: 700, y: 1240, h: 210, f: 1, lean: .02, head: -.75 + Math.sin(st.lt * .7) * .03, armN: [.05, 0], armF: [.05, 0] });
  kanatliFigur(pr, J, { light: [1, -.6], litD: 4, faceFill: false, look: { beard: true, chest: true, face: true } });
}));

// P24 — D04: İkaros babasını aşağıda bırakıp güneşe tırmanır (öğle)
plan('P24', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 200, 600, 6);
  gunes(pr, 1320, 210, 120, 3);
  pr.ink(FG.cloud(600, 900, 900, 140, 12), 'paper', { sheen: 0 }); pr.ink(FG.cloud(1500, 980, 700, 110, 13), 'paper', { sheen: 0 });
  const u = E.io2(clamp((st.t - Wd('D04', 'bıraktı')) / 4));
  a3_ucan(pr, st.lt, 380, 830, 24, 0, true);
  a3_ucan(pr, st.lt, lerp(760, 1020, u), lerp(660, 450, u), 34, 1.3, false, { rise: .35 * u });
}));

// P25 — D04@yükseğe: İkaros'un yüzü güneşte (açılış karesinin aynası, öğle paletiyle)
plan('P25', (ctx, st) => SCENES.yakin(ctx, st.lt + 5, st));

// P26 — D05: göğe basılan kelimeler
plan('P26', (ctx, st) => baski(ctx, st, null, pr => {
  pr.sky('sky2', 'sky1', 120, 420, 5); gunes(pr, 1600, 200, 60, 2);
  a3_ucan(pr, st.lt, 1500 + st.lt * 8, 760, 18, 1.3, false, { rise: .3 });
}), { over: (ctx, st, pal) => {
  basYazi(ctx, 'KİBİR DEĞİL', W / 2, 420, st.t - Wd('D05', 'kibir'), { px: 130, ls: 10, col: pal.near, dur: .45 });
  const w = ['CÜRET', 'SEVİNÇ', 'ARZU'], k = ['cüretten', 'sevinçten', 'arzudan'];
  w.forEach((s, i) => basYazi(ctx, s, W / 2 + (i - 1) * 420, 620, st.t - Wd('D05', k[i]), { px: 110, ls: 8, col: pal.near, dur: .4 }));
} });
