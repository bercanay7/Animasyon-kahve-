// Perde 5 (P37–P48): O değil, bu. Perde 6 (P49–P56): Görünmeyen böcek.
'use strict';
// üç pencereli baskı: bankada baba, lamba altında dikiş diken anne, tezgâhta Grete
plan('P37', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .03 * st.p }, k => {
  const g = k.m, lt = k.lt, pane = [[110, 560], [690, 560], [1270, 560]];
  pane.forEach(([x0], i) => {
    const r = KS.rect(x0, 110, 540, 700); g.strokeStyle = '#fff'; g.lineWidth = 8; g.strokeRect(x0, 110, 540, 700);
    g.save(); g.clip(r);
    if (i === 0) { KS.tara(g, 'p37:banka', [[[x0, 110], [x0 + 540, 110], [x0 + 540, 810], [x0, 810]]], { aci: Math.PI / 2, sp: 30, wmax: 10, seg: [400, 900], gap: [10, 30], seed: 321, ton: () => .35 }); O.fig(k, { x: x0 + 270, y: 800, h: 560, f: 1, tip: 'baba', kep: true, bas: Math.sin(lt * .8) * .03 }, { isik: [1, -.4] }); }
    if (i === 1) { O.lamba(k, 'p37:lamba', x0 + 270, 220, { n: 20, r1: [200, 380], w: 7 }); O.fig(k, { x: x0 + 210, y: 800, h: 480, f: 1, tip: 'anne', otur: true, egil: .4, bas: .4, kolN: [1.2 + Math.sin(lt * 6) * .15, -.8], kolF: [1.0, -.6] }, { isik: [.6, -1] }); }
    if (i === 2) { KS.ak(g, KS.rect(x0, 560, 540, 30)); KS.tara(g, 'p37:raf', [[[x0, 140], [x0 + 540, 140], [x0 + 540, 540], [x0, 540]]], { aci: 0, sp: 34, wmax: 8, seg: [80, 220], gap: [10, 40], seed: 325, ton: () => .5 }); O.fig(k, { x: x0 + 300, y: 820, h: 520, f: -1, tip: 'grete', bas: .1, kolN: [1.2, -.3], kolF: [1.0, -.2] }, { isik: [-.6, -1] }); }
    g.restore();
  });
}));
// eşikte ayak tabağı içeri iter; duvarda kir izleri
plan('P38', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.02 + .03 * st.p }, k => {
  const g = k.m, lt = k.lt;
  KS.tara(g, 'p38:duvar', [[[58, 40], [1862, 40], [1862, 620], [58, 620]]], { aci: Math.PI / 2, sp: 22, wmax: 4, seg: [40, 160], gap: [10, 30], seed: 331, ton: () => .35 });
  for (let i = 0; i < 6; i++) KS.kenar(g, 'p38:kir' + i, [[300 + i * 230, 120 + (i % 3) * 40], [290 + i * 232 + 30, 600]], { w: 14, kind: 'u', seg: [60, 180], gap: [10, 40], seed: 340 + i, renk: '#000' });
  KS.ak(g, KS.poly([[58, 620], [1862, 620], [1862, 900], [58, 900]]));
  KS.tara(g, 'p38:zemin', [[[58, 620], [1862, 620], [1862, 900], [58, 900]]], { aci: .02, sp: 14, wmax: 7, seg: [100, 400], gap: [4, 14], seed: 333, renk: '#000', ton: () => .45 });
  KS.benek(g, 'p38:toz', Array.from({ length: 40 }, (_, i) => [100 + hash(i * 2.7) * 1700, 640 + hash(i * 4.1) * 240, 3 + hash(i) * 3]), { renk: '#000' });
  const u = E.out3(clamp(lt / 1.3)), tx = lerp(1500, 1050, u);
  const tb = new Path2D(); tb.ellipse(tx, 760, 160, 36, 0, 0, TAU); KS.siluet(g, tb, { hale: 7, rim: 6, isik: [0, -1] });
  const ay = new Path2D(); FG.capsule(ay, [2000, 520], [tx + 260, 740], 60, 44); FG.ellipseInto(ay, tx + 200, 760, 110, 40, -.1); KS.siluet(g, ay, { hale: 9, rim: 8, isik: [-.4, -1] });
  bolum(k, 'O DEĞİL, BU', { pw: 620 });
}));
// salon: üç sakallı kiracı masada; Grete keman çalıyor
function a5_salon(k, o = {}) {
  const g = k.m, lt = k.lt;
  O.lamba(k, 'salon', 860, 230);
  O.masa(k, 'salon', 820, 600, 900, { boy: 300 });
  const don = o.don ?? 0;
  [[480, 1], [820, 1], [1140, -1]].forEach(([x, f], i) => O.fig(k, { x, y: 900, h: 500, f: don > .5 ? 1 : f, tip: 'kiraci', otur: don < .6, bas: -.1 * don, kolN: [1.1, -.3], kolF: [.9, -.2] }, { isik: [0, -1] }));
  if (o.grete !== false) { const sw = Math.sin(lt * 3) * .12; const F = O.fig(k, { x: 1560, y: 880, h: 540, f: -1, tip: 'grete', bas: .25, kolN: [2.2 + sw, -1.6], kolF: [2.0, -2.2] }, { isik: [-.4, -1] }); const kem = new Path2D(); FG.ellipseInto(kem, F.bas[0] - 34, F.bas[1] + 50, 46, 26, -.5); KS.siluet(g, kem, { hale: 5, rim: 4 }); }
}
plan('P39', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => a5_salon(k)));
plan('P40', (ctx, st) => kes(ctx, st, { cx: 760, cy: 520, z: 1.25 }, k => a5_salon(k, { don: E.io2(clamp(k.lt / 1.6)), grete: false })));
// Grete masaya vurur; baba ve anne oturuyor
function a5_karar(k, o = {}) {
  const g = k.m, lt = k.lt;
  O.lamba(k, 'karar', 960, 230);
  O.masa(k, 'karar', 960, 620, 1000, { boy: 280 });
  O.fig(k, { x: 600, y: 900, h: 500, f: 1, tip: 'baba', otur: true, egil: o.egil ?? .1, bas: o.babaBas ?? .2, kolN: o.babaKol || [1.1, -.4], kolF: o.babaKol || [.9, -.3] }, { isik: [.5, -1] });
  O.fig(k, { x: 860, y: 900, h: 460, f: 1, tip: 'anne', otur: true, bas: .3, kolN: [1.0, -.2], kolF: [.9, -.1] }, { isik: [.5, -1] });
  const vur = o.vur ? Math.max(0, 1 - Math.abs(lt - 1.0) * 4) : 0;
  O.fig(k, { x: 1320, y: 900, h: 600, f: -1, tip: 'grete', egil: .15 + vur * .2, bas: .1, kolN: [1.5 - vur * .4, -.2], kolF: [.2, -.1] }, { isik: [-.5, -1] });
  if (vur > 0) KS.isin(g, 'karar:vur', 1150, 610, { n: 14, r0: 30, r1: [80, 150], w: 6, a0: Math.PI, a1: TAU, seed: 351 });
}
plan('P41', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => { a5_karar(k, { vur: true }); alinti(k, '“Kardeşimin adını ağzıma almayacağım.”', { y: 110, pw: 1240, t0: 1.6 }); }));
plan('P42', (ctx, st) => kes(ctx, st, { cx: 760, cy: 560, z: 1.3 + .04 * st.p }, k => a5_karar(k, { egil: .55, babaBas: .5, babaKol: [2.4, -1.9] })));
plan('P43', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .05 * st.p }, k => a3_kase(k, { bos: true })));
// gece oda: kapının altından ince ışık
plan('P44', (ctx, st) => kes(ctx, st, { cx: 1100, cy: 470, z: 1.04 + .04 * st.p }, k => {
  const g = k.m;
  KS.kenar(g, 'p44:kasa', [[1040, ZY], [1040, 70], [1470, 70], [1470, ZY]], { w: 3.5, seed: 361 });
  const alt = KS.rect(1046, ZY - 8, 418, 8); KS.ak(g, alt);
  KS.tara(g, 'p44:sizi', [[[1040, ZY], [1470, ZY], [1700, 900], [810, 900]]], { dir: (x, y) => Math.atan2(y - ZY + 40, x - 1255), sp: 18, wmax: 4, seg: [30, 120], gap: [10, 30], seed: 363, ton: (x, y) => clamp(1 - (y - ZY) / 300) * .5 });
  O.pencere(k, 'p44', 230, 120, 330, 400, { gece: true });
}));
// pencere: kilise kulesi, gök aydınlanır (ışık oyulur)
plan('P45', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .05 * st.p }, k => {
  const g = k.m, lt = k.lt, u = clamp(lt / Math.max(4, st.d - .5));
  const cam = KS.rect(560, 90, 800, 700);
  KS.isin(g, 'p45:safak', 960, 900, { n: 40, r0: 220, r1: [500, 900], w: 18, a0: Math.PI * 1.08, a1: Math.PI * 1.92, seed: 371, reveal: { t0: 0, t1: 1, jit: .5 } }, u);
  const kule = new Path2D(); kule.rect(1100, 420, 90, 380); kule.moveTo(1080, 420); kule.lineTo(1145, 280); kule.lineTo(1210, 420); kule.closePath(); g.fillStyle = '#000'; g.fill(kule); KS.kenar(g, 'p45:kuleK', [[1106, 800], [1106, 424], [1145, 290]], { w: 3, seed: 373 });
  const ct = new Path2D(); ct.rect(560, 700, 800, 100); g.fill(ct);
  g.fillStyle = '#000'; g.fillRect(950, 90, 20, 700); g.fillRect(560, 380, 800, 20);
  KS.kenar(g, 'p45:kasa', [[540, 810], [540, 70], [1380, 70], [1380, 810], [540, 810]], { w: 4, seed: 375 });
  KS.ak(g, KS.rect(500, 820, 920, 10));
}));
// tramvay: güneşli kır yolu
function a5_tramvay(k, o = {}) {
  const g = k.m, lt = k.lt;
  KS.isin(g, 'tram:gunes', 1500, 200, { n: 44, r0: 90, r1: [400, 1300], w: 16, seed: 381 });
  const gn = new Path2D(); gn.arc(1500, 200, 80, 0, TAU); KS.ak(g, gn);
  KS.tara(g, 'tram:tarla', [[[58, 600], [1862, 560], [1862, 900], [58, 900]]], { aci: -.04, sp: 16, wmax: 7, seg: [80, 300], gap: [4, 16], seed: 383, ton: (x, y) => .55 });
  for (let i = 0; i < 12; i++) KS.kenar(g, 'tram:direk' + i, [[100 + i * 170 - (lt * 120 % 170), 360], [100 + i * 170 - (lt * 120 % 170), 600]], { w: 4, seed: 390 + i });
  KS.ak(g, KS.rect(58, 340, 1804, 5));
  const tx = 560 + Math.sin(lt * .3) * 6;
  const tr = new Path2D(); tr.rect(tx, 440, 760, 200); tr.rect(tx + 330, 380, 100, 60); KS.siluet(g, tr, { hale: 7, rim: 7, isik: [1, -1] });
  for (let i = 0; i < 6; i++) KS.ak(g, KS.rect(tx + 40 + i * 120, 470, 80, 80));
  [[tx + 220, 'baba'], [tx + 340, 'anne'], [tx + 520, 'grete']].forEach(([x, tp]) => { const F = IN.insan({ x, y: 560, h: 150, f: 1, tip: tp, otur: true }); g.fillStyle = '#000'; g.save(); g.clip(KS.rect(tx, 470, 760, 80)); g.fill(F.p); g.restore(); });
  g.strokeStyle = '#fff'; g.lineWidth = 3; g.beginPath(); g.moveTo(tx + 380, 380); g.lineTo(tx + 300, 330); g.stroke();
  for (const wx of [tx + 120, tx + 640]) { const w = new Path2D(); w.arc(wx, 650, 34, 0, TAU); g.fillStyle = '#000'; g.fill(w); g.strokeStyle = '#fff'; g.lineWidth = 4; g.stroke(w); }
}
plan('P46', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .03 * st.p }, k => a5_tramvay(k)));
// tramvayın içi: anne ve baba Grete'ye bakıyor
function a5_tramIc(k, o = {}) {
  const g = k.m, lt = k.lt;
  O.pencere(k, 'tramIc', 200, 120, 1500, 380, { gok: (k2, x, y, w, h) => { const gg = k2.m; KS.isin(gg, 'tramIc:g', 1400, 160, { n: 30, r0: 60, r1: [300, 900], w: 12, renk: '#000', seed: 401 }); KS.tara(gg, 'tramIc:t', [[[x, y + h * .65], [x + w, y + h * .6], [x + w, y + h], [x, y + h]]], { aci: -.04, sp: 14, wmax: 7, seg: [40, 160], gap: [6, 20], seed: 403, renk: '#000', ton: () => .5 }); } });
  const kalk = o.kalk ? E.io2(clamp((lt - 1.2) / 1.8)) : 0;
  O.fig(k, { x: 520, y: 900, h: 600, f: 1, tip: 'baba', otur: true, bas: -.1, kolN: [.9, -.4], kolF: [.8, -.3] }, { isik: [.3, -1] });
  O.fig(k, { x: 800, y: 900, h: 540, f: 1, tip: 'anne', otur: true, bas: -.05, kolN: [.9, -.3], kolF: [.8, -.3] }, { isik: [.3, -1] });
  O.fig(k, { x: 1300, y: 900 - kalk * 0, h: 560 + kalk * 120, f: -1, tip: 'grete', otur: kalk < .4, bas: -.2 * kalk, kolN: [.9 + kalk * 1.0, -.3 + kalk * 1.3], kolF: [.8 + kalk * 1.1, -.3 + kalk * 1.4] }, { isik: [.2, -1], rim: 9 });
}
plan('P47', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => a5_tramIc(k)));
plan('P48', (ctx, st) => kes(ctx, st, { cx: 1180, cy: 440, z: 1.15 - .08 * E.io2(st.p) }, k => a5_tramIc(k, { kalk: true })));

// ── GÖRÜNMEYEN BÖCEK ──
// 1915 ilk baskı (kendi çizimimiz): kapakta yalnız aralık kapı
plan('P49', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .05 * st.p }, k => {
  const g = k.m;
  KS.tara(g, 'p49:masa', [[[58, 40], [1862, 40], [1862, 900], [58, 900]]], { aci: .1, sp: 14, wmax: 5, seg: [200, 600], gap: [6, 20], seed: 411, ton: () => .3 });
  const kit = KS.poly([[640, 90], [1280, 110], [1260, 870], [620, 850]]); KS.ak(g, kit); g.strokeStyle = '#000'; g.lineWidth = 12; g.stroke(kit);
  g.save(); g.clip(kit); g.fillStyle = '#000'; g.fillRect(820, 380, 280, 400); g.fillStyle = '#fff'; g.fillRect(960, 386, 26, 394); g.restore();
  oyYazi({ ...k, m: g }, 'DIE VERWANDLUNG', 950, 230, { font: YF.serif(48, 600), ls: 4, renk: '#000', t0: 0, dur: .01 });
  oyYazi({ ...k, m: g }, 'FRANZ KAFKA · 1915', 950, 300, { font: YF.serif(34, 600), ls: 6, renk: '#000', t0: 0, dur: .01 });
}));
// masada mektup; alıntı
plan('P50', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.02 + .04 * st.p }, k => {
  const g = k.m, lt = k.lt;
  const mk = KS.poly([[420, 90], [1500, 120], [1470, 640], [400, 610]]); KS.ak(g, mk);
  g.save(); g.clip(mk); g.strokeStyle = '#000'; g.lineCap = 'round';
  const R = rng(21), sat = Math.floor(clamp(lt / 3) * 16) + 4;
  for (let i = 0; i < sat; i++) { let x = 480, y = 160 + i * 28 + i * 1.2; g.lineWidth = 3; g.beginPath(); g.moveTo(x, y); while (x < 1400 - (i % 4) * 60) { x += 8; g.lineTo(x, y + Math.sin(x * .3 + i) * 5 * R()); } g.stroke(); }
  g.restore();
  const kal = new Path2D(); FG.capsule(kal, [1300, 700], [1650, 450], 12, 8); KS.siluet(g, kal, { hale: 5, rim: 4 });
  alinti(k, '“Böceğin kendisi çizilemez.”', { y: 770, pw: 1060, t0: 1.0 });
  oyYazi(k, 'KAFKA → KURT WOLFF YAYINEVİ · 25 EKİM 1915', 960, 862, { font: YF.kunye(30), ls: 4, t0: 1.6, dur: .5 });
}));
plan('P51', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470 - 24 * E.io2(st.p), z: 1.0 + .05 * st.p }, k => a1_aileKapida(k, { bas: .4 })));
// gece: masa başında yazan adam silueti (dönem silueti), lamba; zarf; alıntı
plan('P52', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => {
  const g = k.m, lt = k.lt;
  KS.isin(g, 'p52:lamba', 1240, 300, { n: 34, r0: 50, r1: [300, 700], w: 11, seed: 421 });
  const ab = KS.poly([[1180, 300], [1300, 300], [1260, 240], [1220, 240]]); KS.ak(g, ab);
  O.masa(k, 'p52', 1080, 560, 900, { boy: 340 });
  O.fig(k, { x: 800, y: 900, h: 560, f: 1, tip: 'kafka', melon: false, otur: true, egil: .4, bas: .3, kolN: [1.5 + Math.sin(lt * 7) * .05, -.9], kolF: [1.3, -.7] }, { isik: [1, -.6] });
  const zarf = KS.poly([[1180, 520], [1400, 520], [1400, 556], [1180, 556]]); KS.ak(g, zarf);
  KS.kenar(g, 'p52:aski', [[300, 140], [300, 560]], { w: 6, seed: 423 }); const mel = new Path2D(); FG.ellipseInto(mel, 300, 150, 46, 34); mel.rect(250, 172, 100, 10); KS.siluet(g, mel, { hale: 5, rim: 4 });
  alinti(k, '“Yazdıklarım hep senin hakkındaydı.”', { y: 110, pw: 1180, t0: 1.2 });
  oyYazi(k, 'BABAYA MEKTUP · KASIM 1919', 960, 862, { font: YF.kunye(30), ls: 4, t0: 1.8, dur: .5 });
}));
// bugün: gece apartman koridoru, kapalı kapılar; birinin altından ışık
plan('P53', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .06 * st.p }, k => {
  const g = k.m;
  const v = [960, 380];
  for (let i = 0; i < 5; i++) { const d = 1 - i * .17, xl = lerp(v[0], 150, d), xr = lerp(v[0], 1770, d), yt = lerp(v[1], 90, d), yb = lerp(v[1], 860, d), w = 180 * d;
    for (const [x, s] of [[xl, -1], [xr, 1]]) { const kp = KS.poly([[x, yt + 40 * d], [x - s * w * .5, yt + 70 * d], [x - s * w * .5, yb - 20 * d], [x, yb]]); g.strokeStyle = '#fff'; g.lineWidth = 4 * d + 1; g.stroke(kp); if (i === 1 && s === 1) { KS.ak(g, KS.poly([[x, yb - 2], [x - s * w * .5, yb - 22 * d], [x - s * w * .5 - 30, yb + 30], [x + 30, yb + 50]])); } } }
  for (let i = 0; i < 9; i++) { const d = i / 9; KS.ak(g, KS.rect(lerp(150, 940, d), lerp(860, 400, d), lerp(1620, 40, d), 3)); }
  const lmb = new Path2D(); lmb.rect(930, 100, 60, 14); KS.ak(g, lmb);
}));
// kapının arkasında yatağın kenarında oturan bugünün insanı (kapüşonlu)
plan('P54', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => {
  const g = k.m;
  const kp = KS.rect(1360, 120, 360, 640); g.strokeStyle = '#fff'; g.lineWidth = 5; g.stroke(kp); KS.ak(g, KS.rect(1366, 752, 348, 8));
  KS.tara(g, 'p54:isik', [[[1366, 760], [1714, 760], [1862, 900], [1180, 900]]], { aci: 0, sp: 10, wmax: 5, seg: [40, 140], gap: [6, 16], seed: 431, ton: () => .6 });
  const yt = KS.rect(300, 640, 760, 60); KS.ak(g, yt); g.fillStyle = '#000'; g.fillRect(300, 700, 760, 200);
  const tel = new Path2D(); tel.rect(860, 600, 50, 90); KS.ak(g, tel);
  KS.isin(g, 'p54:tel', 885, 600, { n: 16, r0: 30, r1: [80, 160], w: 4, a0: Math.PI * 1.1, a1: Math.PI * 1.9, seed: 433 });
  O.fig(k, { x: 720, y: 900, h: 600, f: 1, tip: 'bugun', otur: true, egil: .35 + Math.sin(k.lt * .7) * .03, bas: .45, kolN: [1.3, -1.2], kolF: [1.1, -1.0] }, { isik: [1, -.3] });
}));
// açılış karesi geri döner; soru oyulur
plan('P55', (ctx, st) => kes(ctx, st, { cx: 1100, cy: 470, z: 1.04 + .04 * st.p }, k => { a1_kapiKaresi(k, { ac: 56 }); oyYazi(k, 'Seni mi seviyorlardı,\nişe yarayan hâlini mi?', 560, 330, { font: YF.italik(66, 600), t0: .6, dur: 1.2 }); }));
// son: tepede kaya ve küçük figür (Sisifos'a köprü); kanal adı; bitiş ekranı alanı (sağ yarı boş)
plan('P56', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .02 * st.p }, k => {
  const g = k.m, lt = k.lt;
  KS.isin(g, 'p56:gok', 520, 760, { n: 36, r0: 380, r1: [700, 1100], w: 14, a0: Math.PI * 1.05, a1: Math.PI * 1.95, seed: 441 });
  const tepe = KS.poly([[58, 900], [58, 760], [420, 470], [520, 450], [980, 900]]); g.fillStyle = '#000'; g.fill(tepe); KS.kenar(g, 'p56:tepeK', [[70, 760], [420, 474], [520, 454], [960, 890]], { w: 5, seed: 443 });
  const kay = new Path2D(); kay.arc(480, 380, 70, 0, TAU); KS.siluet(g, kay, { hale: 7, rim: 8, isik: [1, -1] });
  O.fig(k, { x: 380, y: 520, h: 170, f: 1, tip: 'gregor', egil: .7, kolN: [2.0, -.4], kolF: [1.8, -.3], adim: .5 }, { isik: [1, -1] });
  oyYazi(k, 'ZAMAN KURYESİ', 520, 120, { font: YF.serif(76, 600), ls: 12, t0: .5, dur: 1.0, panel: [140, 50, 760, 140] });
}));
