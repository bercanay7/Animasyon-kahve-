// Perde 2 (P10–P17): Hayvan sesi · Perde 3 (P18–P26): Süt ve elma
'use strict';
// bölüm başlığı: üstte kara panelde oyulmuş başlık (blok içinde; alt banda inmez)
function bolum(k, s, o = {}) { oyYazi(k, s, 960, o.y ?? 130, { font: YF.serif(o.px ?? 92, 600), ls: 14, t0: o.t0 ?? .2, dur: .9, panel: o.panel === false ? null : [960 - (o.pw ?? 760) / 2, (o.y ?? 130) - 75, o.pw ?? 760, 150] }); }
// alıntı: kara panelde oyulmuş italik
function alinti(k, s, o = {}) { oyYazi(k, s, 960, o.y ?? 790, { font: YF.italik(o.px ?? 64, 600), ls: 2, t0: o.t0 ?? .4, dur: 1.1, panel: [960 - (o.pw ?? 1320) / 2, (o.y ?? 790) - (o.ph ?? 120) / 2, o.pw ?? 1320, o.ph ?? 120] }); }

// yağmurda yürüyen satıcı (insan Gregor; geri dönüş). dx: yürüyüş ilerlemesi
function a2_yol(k, o = {}) {
  const g = k.m, lt = k.lt;
  // ıslak kaldırım: yansıyan sokak lambaları (dikey kesikler)
  KS.tara(g, 'yol:gok', [[[58, 40], [1862, 40], [1862, 560], [58, 560]]], { aci: 1.25, sp: 20, wmax: 3, seg: [30, 90], gap: [20, 60], seed: 141, ton: () => .45 });
  for (let i = 0; i < 5; i++) { const x = 200 + i * 380; g.fillStyle = '#fff'; g.fillRect(x, 160, 8, 420); const l = new Path2D(); l.arc(x + 4, 150, 26, 0, TAU); KS.ak(g, l); KS.isin(g, 'yol:lamba' + i, x + 4, 150, { n: 18, r0: 34, r1: [90, 160], w: 5, seed: 150 + i }); KS.kenar(g, 'yol:yans' + i, [[x + 4, 620], [x + 4, 880]], { w: 6, seg: [14, 40], gap: [8, 20], seed: 160 + i }); }
  KS.ak(g, KS.rect(58, 580, 1804, 14));
  const x = 520 + lt * 70, ph = lt * 4.2, adim = Math.sin(ph) * .5;
  const F = O.fig(k, { x, y: 820, h: 360, f: 1, tip: 'gregor', melon: true, egil: .12, adim: .3 + adim * .3, kolN: [.1 + adim * .3, -.1], kolF: [-.15 - adim * .3, -.1] }, { isik: [-1, -.5] });
  // çanta (kumaş örnekleri)
  const c = KS.rect(F.elN[0] - 30, F.elN[1], 90, 62); KS.siluet(g, c, { hale: 4, rim: 3 });
  // yağmur: çapraz kesikler
  g.strokeStyle = '#fff'; const r = rng(3); for (let i = 0; i < 110; i++) { const px = 58 + r() * 1804, py = 40 + ((r() * 860 + lt * 420) % 860), L = 18 + r() * 22; g.lineWidth = 1.6 + r(); g.beginPath(); g.moveTo(px, py); g.lineTo(px - L * .3, py + L); g.stroke(); }
}
plan('P10', (ctx, st) => kes(ctx, st, { cx: 900 + st.lt * 30, cy: 470, z: 1.02 }, k => { a2_yol(k); bolum(k, 'HAYVAN SESİ'); }));

// borç: masada senetler ve sikkeler; bir el sikkeleri iter
function a2_borc(k) {
  const g = k.m, lt = k.lt;
  KS.ak(g, KS.poly([[58, 380], [1862, 330], [1862, 900], [58, 900]]));
  KS.tara(g, 'borc:masa', [[[58, 380], [1862, 330], [1862, 900], [58, 900]]], { aci: -.03, sp: 12, wmax: 7, seg: [120, 400], gap: [4, 14], seed: 171, renk: '#000', ton: (x, y) => .35 + (y - 400) / 1400 });
  // senetler: yamuk kâğıtlar, üstünde kara yazı satırları
  [[300, 440, -.12], [520, 520, .08], [380, 650, -.04]].forEach(([x, y, a], i) => { g.save(); g.translate(x, y); g.rotate(a); const p = KS.rect(-150, -100, 300, 200); KS.ak(g, p); g.strokeStyle = '#000'; g.lineWidth = 6; g.strokeRect(-150, -100, 300, 200); g.lineWidth = 3; for (let j = 0; j < 7; j++) { g.beginPath(); g.moveTo(-120, -70 + j * 24); g.lineTo(-120 + 200 + (j * 37 % 60), -70 + j * 24); g.stroke(); } g.restore(); });
  // sikke yığınları
  for (let s = 0; s < 4; s++) for (let j = 0; j < 6 + s * 2; j++) O.sikke(g, 1000 + s * 170, 700 - j * 14, 58);
  // el: ekrandan girer, öne iter (siluet kol + parmaklar)
  const ex = lerp(1950, 1640, E.out3(clamp(lt / 1.4))) - Math.max(0, lt - 2) * 25;
  const el = new Path2D(); FG.capsule(el, [2100, 520], [ex + 120, 600], 70, 58); FG.ellipseInto(el, ex + 60, 610, 90, 58, -.2);
  for (let i = 0; i < 4; i++) FG.capsule(el, [ex + 20, 580 + i * 26], [ex - 70, 570 + i * 30], 16, 13);
  KS.siluet(g, el, { hale: 8, isik: [-.3, -1], rim: 9 });
}
plan('P11', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.03 + .03 * st.p }, k => a2_borc(k)));

// koridor: kapalı kapı (Gregor'un kapısı) önünde müdür yardımcısı; arkada anne ve baba
function a2_koridor(k, o = {}) {
  const g = k.m;
  KS.tara(g, 'kor:duvar', [[[58, 40], [1862, 40], [1862, 760], [58, 760]]], { aci: Math.PI / 2, sp: 18, wmax: 6, seg: [60, 260], gap: [6, 22], seed: 181, ton: (x, y) => clamp(1 - Math.abs(x - 600) / 1100) * .75 });
  // Gregor'un kapısı (sağda, kapalı): kara kanat, ak pervaz, kilitte anahtar deliği
  const kp = KS.rect(1360, 150, 360, 610); g.fillStyle = '#000'; g.fill(kp); KS.kenar(g, 'kor:kasa', [[1340, 760], [1340, 130], [1740, 130], [1740, 760]], { w: 5, seed: 183 });
  KS.kenar(g, 'kor:pano1', [[1400, 200], [1680, 200], [1680, 420], [1400, 420], [1400, 200]], { w: 2.6, seed: 184 }); KS.kenar(g, 'kor:pano2', [[1400, 480], [1680, 480], [1680, 720], [1400, 720], [1400, 480]], { w: 2.6, seed: 185 });
  const kl = new Path2D(); kl.ellipse(1400, 450, 12, 8, 0, 0, TAU); KS.ak(g, kl);
  KS.ak(g, KS.rect(58, 760, 1804, 10));
  O.fig(k, { x: 690, y: 780, h: 600, f: 1, tip: 'anne', bas: .1, kolN: [.9, 1.3], kolF: [.7, 1.4] }, { isik: [1, -.5] });
  O.fig(k, { x: 880, y: 790, h: 640, f: 1, tip: 'baba', bas: .05, kolN: [.1, -.1], kolF: [-.1, -.1] }, { isik: [1, -.5] });
  O.fig(k, { x: 1220, y: 800, h: 640, f: 1, tip: 'mudur', egil: .18 + Math.sin(k.lt * 1.5) * .03, bas: .15, kolN: [.9, -.6], kolF: [.1, -.1] }, { isik: [-1, -.5] });
}
plan('P12', (ctx, st) => kes(ctx, st, { cx: 960 + 40 * st.p, cy: 470, z: 1.02 }, k => a2_koridor(k)));
// müdür yardımcısının baş profili (yakın), kapıya eğilmiş; alıntı
plan('P13', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => {
  const g = k.m;
  const kp = KS.rect(1320, 40, 600, 860); g.fillStyle = '#000'; g.fill(kp); KS.kenar(g, 'p13:kasa', [[1300, 40], [1300, 900]], { w: 7, seed: 191 });
  KS.tara(g, 'p13:fon', [[[58, 40], [1290, 40], [1290, 900], [58, 900]]], { dir: WC.dirRadial(300, 200), sp: 15, wmax: 8, seg: [60, 260], gap: [6, 20], seed: 193, ton: (x, y) => clamp(1 - Math.hypot(x - 300, y - 200) / 1100) * .9 });
  O.fig(k, { x: 880, y: 1620, h: 1300, f: 1, tip: 'mudur', egil: .3, bas: .28, kolN: [.1, 0], kolF: [0, 0] }, { isik: [-1, -.4], rim: 12, kesSp: 22 });
  alinti(k, '“Bu bir hayvan sesiydi.”', { y: 790, t0: .8, pw: 1100 });
}));
// kilitte dönen anahtar
plan('P14', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .05 * st.p }, k => {
  const g = k.m;
  KS.tara(g, 'p14:kapi', [[[58, 40], [1862, 40], [1862, 900], [58, 900]]], { aci: Math.PI / 2, sp: 14, wmax: 5, seg: [200, 600], gap: [6, 20], seed: 201, ton: () => .35 });
  const pl = KS.poly([[820, 200], [1100, 200], [1100, 760], [820, 760]]); KS.ak(g, pl); g.strokeStyle = '#000'; g.lineWidth = 10; g.stroke(pl);
  const del = new Path2D(); del.arc(960, 430, 34, 0, TAU); del.moveTo(940, 430); del.lineTo(980, 430); del.lineTo(990, 560); del.lineTo(930, 560); del.closePath(); g.fillStyle = '#000'; g.fill(del);
  const a = -E.io2(clamp((k.lt - .6) / 2.4)) * Math.PI / 2;
  g.save(); g.translate(960, 470); g.rotate(a);
  const an = new Path2D(); an.rect(-14, -10, 28, 160); an.arc(0, 200, 56, 0, TAU); an.rect(-14, -60, 60, 26);
  g.strokeStyle = '#000'; g.lineWidth = 12; g.stroke(an); KS.ak(g, an); const del2 = new Path2D(); del2.arc(0, 200, 26, 0, TAU); g.fillStyle = '#000'; g.fill(del2);
  g.restore();
}));
// merdiven boşluğu: müdür yardımcısı kaçar
plan('P15', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470 + 40 * st.p, z: 1.02 }, k => {
  const g = k.m, lt = k.lt;
  for (let i = 0; i < 14; i++) { const y = 120 + i * 58, x = 300 + i * 70; const b = KS.poly([[x, y], [x + 900, y], [x + 900, y + 14], [x, y + 14]]); KS.ak(g, b); }
  KS.kenar(g, 'p15:korkuluk', [[260, 80], [1300, 900]], { w: 9, seg: [200, 500], gap: [4, 10], seed: 211 });
  for (let i = 0; i < 12; i++) KS.kenar(g, 'p15:dik' + i, [[300 + i * 86, 112 + i * 67], [300 + i * 86, 230 + i * 67]], { w: 4, seed: 212 + i });
  const u = clamp(lt / 3), x = lerp(700, 1300, u), y = lerp(430, 900, u), ph = lt * 9;
  O.fig(k, { x, y, h: 380, f: 1, tip: 'mudur', egil: .3, adim: .5 + Math.sin(ph) * .4, kolN: [-.9 + Math.sin(ph) * .4, .3], kolF: [1.4, -.4] }, { isik: [-1, -.6] });
}));
// aşağıdan baba: baston kalkık, gazete elinde, üstümüze yürür
function a2_babaUstte(k, o = {}) {
  const g = k.m, lt = k.lt;
  const bos = KS.rect(420, 40, 1080, 860); KS.ak(g, bos);
  g.save(); g.clip(bos); KS.isin(g, 'baba:arka', 960, 160, { n: 50, r0: 200, r1: [800, 1100], w: 13, renk: '#000', seed: 222 }); g.restore();
  const sw = Math.sin(lt * 5) * .25;
  const F = O.fig(k, { x: 960, y: 1080 + lt * 20, h: 1150 + lt * 40, f: -1, tip: 'baba', kep: !!o.kep, bas: .35, kolN: o.baston === false ? [.1, -.05] : [2.6 + sw, -.2], kolF: o.baston === false ? [-.08, -.05] : [.9, .9] }, { isik: [0, -1] });
  if (o.baston !== false) { g.save(); g.lineCap = 'round'; g.strokeStyle = '#fff'; g.lineWidth = 34; const a = -1.0 + sw; g.beginPath(); g.moveTo(F.elN[0], F.elN[1]); g.lineTo(F.elN[0] + Math.cos(a) * 520, F.elN[1] + Math.sin(a) * 520); g.stroke(); g.strokeStyle = '#000'; g.lineWidth = 20; g.stroke(); g.restore();
    const gz = KS.poly([[F.elF[0] - 90, F.elF[1] - 60], [F.elF[0] + 70, F.elF[1] - 90], [F.elF[0] + 100, F.elF[1] + 60], [F.elF[0] - 60, F.elF[1] + 80]]); KS.ak(g, gz); g.save(); g.clip(gz); g.strokeStyle = '#000'; g.lineWidth = 4; for (let i = 0; i < 12; i++) { g.beginPath(); g.moveTo(F.elF[0] - 120, F.elF[1] - 70 + i * 14); g.lineTo(F.elF[0] + 120, F.elF[1] - 90 + i * 14); g.stroke(); } g.restore(); }
}
plan('P16', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .06 * E.in2(st.p) }, k => a2_babaUstte(k)));
// kapı kapanır: ışık şeridi daralıp kaybolur
plan('P17', (ctx, st) => kes(ctx, st, { cx: 1100, cy: 470, z: 1.08 }, k => {
  const ac = 46 * (1 - E.in3(clamp((k.lt - 1.5) / 1.6)));
  if (ac > 1) a1_kapiKaresi(k, { ac, elma: false, key: 'p17' });
  else { KS.kenar(k.m, 'p17:kasa', [[1040, ZY], [1040, 70], [1470, 70], [1470, ZY]], { w: 4.5, seed: 31 }); }
}));

// ── SÜT VE ELMA ──
// Grete eşikte diz çöker, kâse bırakır (yerden bakış; kapı açık, arkası ışık)
function a3_greteEsik(k, o = {}) {
  const g = k.m, lt = k.lt;
  const bos = KS.rect(560, 40, 820, 700); KS.ak(g, bos);
  g.save(); g.clip(bos); KS.tara(g, 'grete:arka', [[[560, 40], [1380, 40], [1380, 740], [560, 740]]], { aci: Math.PI / 2, sp: 22, wmax: 10, seg: [100, 400], gap: [8, 30], seed: 231, renk: '#000', ton: (x, y) => .25 }); g.restore();
  KS.ak(g, KS.poly([[560, 740], [1380, 740], [1640, 900], [300, 900]]));
  KS.tara(g, 'grete:zemin', [[[560, 740], [1380, 740], [1640, 900], [300, 900]]], { dir: (x, y) => Math.atan2(y - 300, x - 970), sp: 26, wmax: 5, seg: [40, 160], gap: [10, 30], seed: 233, renk: '#000', ton: () => .4 });
  const d = E.io2(clamp(lt / 2.2));
  O.fig(k, { x: 960, y: 880, h: 640, f: -1, tip: 'grete', egil: .5 * d, bas: .3 * d, otur: d > .5, kolN: [.8 + d * .5, -.4], kolF: [.6 + d * .4, -.3] }, { isik: [0, -1] });
  const kx = 860, ky = 860; const kas = new Path2D(); kas.ellipse(kx, ky - 20, 90, 28, 0, 0, TAU); kas.moveTo(kx - 90, ky - 20); kas.quadraticCurveTo(kx, ky + 50, kx + 90, ky - 20); KS.siluet(g, kas, { hale: 6, rim: 5, isik: [0, -1] });
}
plan('P18', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => { a3_greteEsik(k); bolum(k, 'SÜT VE ELMA', { y: 120, pw: 720 }); }));
// süt kâsesi, ekmek parçaları; süt halkalanır
function a3_kase(k, o = {}) {
  const g = k.m, lt = k.lt, bos = !!o.bos;
  KS.tara(g, 'kase:zemin' + (bos ? 'b' : ''), [[[58, 40], [1862, 40], [1862, 900], [58, 900]]], { aci: .05, sp: 26, wmax: 5, seg: [120, 400], gap: [10, 30], seed: 241, ton: (x, y) => clamp(1 - Math.hypot(x - 960, (y - 470) * 1.6) / 1100) * (bos ? .3 : .6) });
  const cx = 960, cy = 470;
  const dis = new Path2D(); dis.ellipse(cx, cy, 520, 230, 0, 0, TAU); g.strokeStyle = '#fff'; g.lineWidth = 14; g.stroke(dis); g.fillStyle = '#000'; g.fill(dis);
  const ic = new Path2D(); ic.ellipse(cx, cy + 10, 440, 180, 0, 0, TAU);
  if (!bos) {
    KS.ak(g, ic);
    g.save(); g.clip(ic); g.strokeStyle = '#000';
    for (let i = 0; i < 6; i++) { const r = ((lt * 50 + i * 70) % 420); g.lineWidth = 3; g.beginPath(); g.ellipse(cx - 120, cy, r, r * .4, 0, 0, TAU); g.stroke(); }
    const R = rng(9); for (let i = 0; i < 6; i++) { const bx = cx - 300 + R() * 560 + Math.sin(lt * .5 + i) * 10, by = cy - 80 + R() * 170; const b = KS.poly([[bx, by], [bx + 70, by - 10], [bx + 80, by + 40], [bx + 5, by + 46]]); g.fillStyle = '#000'; g.fill(b); g.strokeStyle = '#fff'; g.lineWidth = 3; g.stroke(b); }
    g.restore();
  } else {
    g.fillStyle = '#000'; g.fill(ic);
    KS.benek(g, 'kase:toz', Array.from({ length: 50 }, (_, i) => [cx - 400 + hash(i * 3.3) * 800, cy - 150 + hash(i * 5.1) * 300, 2 + hash(i) * 2.5]));
    g.strokeStyle = '#fff'; g.lineWidth = 3; g.beginPath(); g.ellipse(cx, cy + 10, 440, 180, 0, Math.PI * 1.1, Math.PI * 1.6); g.stroke();
  }
}
plan('P19', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .05 * st.p }, k => a3_kase(k)));
// gazete üstünde yemek artıkları
plan('P20', (ctx, st) => kes(ctx, st, { cx: 900 + 80 * st.p, cy: 470, z: 1.04 }, k => {
  const g = k.m;
  const gz = KS.poly([[200, 260], [1700, 200], [1760, 820], [160, 860]]); KS.ak(g, gz);
  g.save(); g.clip(gz); g.strokeStyle = '#000'; g.lineWidth = 3;
  for (let c = 0; c < 6; c++) for (let i = 0; i < 26; i++) { const x0 = 230 + c * 250, y = 280 + i * 21 - c * 8; g.beginPath(); g.moveTo(x0, y); g.lineTo(x0 + 200 - (i * 31 % 70), y - 3); g.stroke(); }
  g.lineWidth = 8; g.beginPath(); g.moveTo(230, 250); g.lineTo(1700, 196); g.stroke();
  g.restore();
  // sebzeler (yarı çürük): kara biçimler, ak kesikli; peynir: üçgen, delikli; kemikler: ak
  const sb = (x, y, r, s) => { const p = new Path2D(); p.ellipse(x, y, r, r * .62, s, 0, TAU); KS.siluet(g, p, { hale: 7, rim: 6, isik: [-1, -1] }); };
  sb(520, 520, 120, .3); sb(700, 600, 90, -.4); sb(420, 650, 80, 1.2);
  const pe = KS.poly([[980, 440], [1260, 520], [1000, 640]]); KS.siluet(g, pe, { hale: 7, rim: 8 }); for (let i = 0; i < 4; i++) { const d = new Path2D(); d.arc(1040 + i * 40, 520 + (i % 2) * 40, 12, 0, TAU); KS.ak(g, d); }
  for (let i = 0; i < 3; i++) { const b = new Path2D(); FG.capsule(b, [1250 + i * 60, 640 + i * 30], [1450 + i * 40, 590 + i * 50], 14, 14); FG.ellipseInto(b, 1250 + i * 60, 640 + i * 30, 26, 20); FG.ellipseInto(b, 1450 + i * 40, 590 + i * 50, 26, 20); g.strokeStyle = '#000'; g.lineWidth = 10; g.stroke(b); KS.ak(g, b); }
}));
// Grete'nin profili (yakın), aşağı bakıyor; kandil ışığı
plan('P21', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => {
  const g = k.m;
  KS.tara(g, 'p21:fon', [[[58, 40], [1862, 40], [1862, 900], [58, 900]]], { dir: WC.dirRadial(1500, 300), sp: 15, wmax: 8, seg: [60, 260], gap: [6, 20], seed: 251, ton: (x, y) => clamp(1 - Math.hypot(x - 1500, y - 300) / 1000) * .95 });
  O.fig(k, { x: 820, y: 1560, h: 1250, f: 1, tip: 'grete', egil: .08, bas: .42 + Math.sin(k.lt * .7) * .02, kolN: [.12, .15], kolF: [-.05, .1] }, { isik: [1, -.4], rim: 12, kesSp: 22 });
}));
// aşağıdan üniformalı baba, kep, ak düğmeler
plan('P22', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .05 * st.p }, k => a2_babaUstte(k, { kep: true, baston: false })));
// büfede meyve tabağı; babanın eli elmaları alır
plan('P23', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.02 + .04 * st.p }, k => {
  const g = k.m, lt = k.lt;
  KS.ak(g, KS.rect(58, 640, 1804, 260)); KS.tara(g, 'p23:bufe', [[[58, 640], [1862, 640], [1862, 900], [58, 900]]], { aci: 0, sp: 12, wmax: 7, seg: [200, 600], gap: [4, 10], seed: 261, renk: '#000', ton: () => .5 });
  const tb = new Path2D(); tb.ellipse(960, 620, 380, 70, 0, 0, TAU); KS.siluet(g, tb, { hale: 8, rim: 8, isik: [0, -1] });
  const al = clamp((lt - 1.2) / 2.5);
  [[800, 560], [900, 540], [1010, 548], [1110, 565], [860, 500], [980, 492], [1060, 505]].forEach(([x, y], i) => { if (i >= 7 - Math.floor(al * 4)) return; O.elma(k, x, y, 50, { rot: (i % 3 - 1) * .3 }); });
  const ex = lerp(1950, 1150, E.out3(clamp((lt - .3) / 1.0)));
  const el = new Path2D(); FG.capsule(el, [2100, 300], [ex + 90, 470], 74, 56); FG.ellipseInto(el, ex + 30, 485, 84, 56, .3); for (let i = 0; i < 4; i++) FG.capsule(el, [ex, 470 + i * 22], [ex - 80, 500 + i * 26], 15, 12);
  KS.siluet(g, el, { hale: 9, rim: 8, isik: [-.5, -1] });
}));
// yerde yuvarlanan elmalar ("elektrikli gibi")
function a3_elmalarYerde(k, o = {}) {
  const g = k.m, lt = k.lt;
  KS.tara(g, 'yer:zemin', [[[58, 300], [1862, 300], [1862, 900], [58, 900]]], { dir: (x, y) => Math.atan2(y + 400, x - 960), sp: 15, wmax: 6, seg: [60, 260], gap: [6, 20], seed: 271, ton: (x, y) => .2 + (y - 300) / 1400 });
  KS.tara(g, 'yer:duvar', [[[58, 40], [1862, 40], [1862, 290], [58, 290]]], { aci: Math.PI / 2, sp: 18, wmax: 3, seg: [40, 140], gap: [10, 30], seed: 272, ton: () => .25 });
  KS.ak(g, KS.rect(58, 290, 1804, 8));
  const R = rng(13);
  for (let i = 0; i < 7; i++) {
    const x0 = 200 + R() * 400, y0 = 420 + R() * 380, vx = 160 + R() * 260, vy = (R() - .5) * 80, dmp = Math.exp(-lt * .5);
    const x = x0 + vx * (1 - Math.exp(-lt * .6)) / .6 + Math.sin(lt * 8 + i) * 8 * dmp, y = y0 + vy * (1 - Math.exp(-lt * .6)) / .6;
    O.elma(k, x, y, 44, { rot: lt * vx / 44 * .6 + i });
  }
}
plan('P24', (ctx, st) => kes(ctx, st, { cx: 960 + 120 * E.io2(st.p), cy: 470, z: 1.02 }, k => a3_elmalarYerde(k)));
// bir elma karanlığa uçar, kırmızı leke olarak kalır (kanepe altı karanlığı; içinde ne olduğu görünmez)
function a3_karanlikElma(k, o = {}) {
  const g = k.m, lt = k.lt;
  // kanepe: üst tarafta ak oyulmuş kıvrımlar, altı mutlak karanlık
  const kan = KS.poly([[300, 200], [1620, 200], [1700, 470], [220, 470]]); KS.ak(g, kan);
  g.save(); g.clip(kan); g.strokeStyle = '#000'; for (let i = 0; i < 18; i++) { g.lineWidth = 6; g.beginPath(); g.moveTo(300 + i * 80, 200); g.quadraticCurveTo(320 + i * 80, 340, 280 + i * 82, 470); g.stroke(); } g.restore();
  for (const x of [330, 1590]) { const ay = KS.rect(x - 20, 470, 40, 90); KS.ak(g, ay); }
  KS.ak(g, KS.rect(58, 560, 1804, 10));
  const hedef = [960, 420], u = clamp((lt - .2) / .55);
  if (o.sabit) { O.elma(k, hedef[0], hedef[1], 46 * (o.sabit), { kirmizi: o.koyu ?? 1, hale: false }); return; }
  if (u < 1) { const x = lerp(-80, hedef[0], u), y = lerp(80, hedef[1], u) - Math.sin(u * Math.PI) * 120; O.elma(k, x, y, 60 - 14 * u, { rot: u * 6 }); }
  else { const s = 1 + .25 * Math.exp(-(lt - .75) * 8) * Math.sin((lt - .75) * 40); O.elma(k, hedef[0], hedef[1], 46 * s, { hale: false }); }
}
plan('P25', (ctx, st) => kes(ctx, st, { cx: 960, cy: 400, z: 1.06 + .04 * st.p }, k => a3_karanlikElma(k)));
plan('P26', (ctx, st) => kes(ctx, st, { cx: 960, cy: 420, z: 1.3 + .1 * st.p }, k => a3_karanlikElma(k, { sabit: 1 - .25 * st.p, koyu: 1 - .65 * E.io2(st.p) })));
