// Perde 4 (P27–P36): Kapının arkasındaki hesap. Geri dönüşte Gregor insandır (yalnız silueti).
'use strict';
// sofra: lamba altında masa, aile oturuyor; Gregor (insan) parayı koyar
function a4_sofra(k, o = {}) {
  const g = k.m, lt = k.lt;
  O.lamba(k, 'sofra', 960, 250, { r1: [300, 560] });
  O.masa(k, 'sofra', 960, 600, 1100, { boy: 300 });
  // masa örtüsü kenarı (ak dişli)
  if (o.gregor !== false) { const u = E.io2(clamp(lt / 2)); O.fig(k, { x: 1560, y: 900, h: 560, f: -1, tip: 'gregor', egil: .35 * u, bas: .2, kolN: [1.2 * u + .1, -.3 * u], kolF: [.1, -.1] }, { isik: [-1, -.6] }); }
  O.fig(k, { x: 560, y: 900, h: 520, f: 1, tip: 'baba', otur: true, bas: .1, kolN: [1.1, -.4], kolF: [.9, -.3] }, { isik: [1, -.8] });
  O.fig(k, { x: 820, y: 900, h: 470, f: 1, tip: 'anne', otur: true, bas: .25, kolN: [1.1, -.2], kolF: [.9, -.1] }, { isik: [.5, -1] });
  O.fig(k, { x: 1120, y: 900, h: 440, f: -1, tip: 'grete', otur: true, bas: .2, kolN: [1.0, -.2], kolF: [.9, -.1] }, { isik: [-.5, -1] });
  // masadaki para
  const n = o.sikke ?? 6; for (let i = 0; i < n; i++) O.sikke(g, 900 + (i % 3) * 70 + (o.sx || 0), 590 - Math.floor(i / 3) * 12, 30);
}
plan('P27', (ctx, st) => kes(ctx, st, { cx: 960 - 60 * st.p, cy: 470, z: 1.02 }, k => {
  const g = k.m, lt = k.lt;
  // geri dönüş: kapı açılır, Gregor (insan) girer, şapkasını asar
  const kap = KS.rect(1180, 120, 380, 640); KS.ak(g, kap); g.save(); g.clip(kap); KS.isin(g, 'p27:dis', 1370, 300, { n: 30, r0: 60, r1: [500, 700], w: 10, renk: '#000', seed: 281 }); g.restore();
  KS.tara(g, 'p27:duvar', [[[58, 40], [1170, 40], [1170, 760], [58, 760]]], { aci: Math.PI / 2, sp: 18, wmax: 5, seg: [60, 260], gap: [6, 22], seed: 283, ton: (x, y) => clamp(1 - Math.abs(x - 1170) / 900) * .7 });
  // askılık
  KS.kenar(g, 'p27:aski', [[700, 200], [700, 760]], { w: 8, seed: 285 }); KS.kenar(g, 'p27:aski2', [[640, 230], [760, 230]], { w: 6, seed: 286 });
  const u = clamp(lt / 2.6);
  O.fig(k, { x: lerp(1380, 900, E.io2(u)), y: 800, h: 560, f: -1, tip: 'gregor', melon: u < .8, adim: .2 + Math.sin(lt * 4) * .2 * (1 - u), kolN: [u > .7 ? 2.4 : .1, -.2], kolF: [-.1, -.1] }, { isik: [-1, -.5] });
  if (u >= .8) { const sp = new Path2D(); FG.ellipseInto(sp, 700, 262, 50, 30); sp.rect(650, 268, 100, 12); KS.siluet(g, sp, { hale: 5, rim: 4 }); }
  KS.ak(g, KS.rect(58, 800, 1804, 10));
  bolum(k, 'KAPININ ARKASINDAKİ HESAP', { px: 70, pw: 1060, y: 110 });
}));
plan('P28', (ctx, st) => kes(ctx, st, { cx: 960, cy: 480, z: 1.0 + .04 * st.p }, k => a4_sofra(k, { sikke: Math.min(6, Math.floor(clamp((k.lt - 1.6) / 2) * 7)) })));
// masada para; eller alır, kimse başını kaldırmaz; Kafka'nın cümlesi
plan('P29', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.02 + .03 * st.p }, k => {
  const g = k.m, lt = k.lt;
  KS.ak(g, KS.rect(58, 300, 1804, 600));
  KS.tara(g, 'p29:masa', [[[58, 300], [1862, 300], [1862, 900], [58, 900]]], { aci: .02, sp: 12, wmax: 7, seg: [200, 600], gap: [4, 12], seed: 291, renk: '#000', ton: (x, y) => .45 + (y - 300) / 1600 });
  const R = rng(17); const al = clamp((lt - .5) / 4);
  for (let i = 0; i < 18; i++) { const x = 500 + R() * 900, y = 380 + R() * 280; if (R() < al) continue; O.sikke(g, x, y, 40); }
  // eller: üç yönden (anne, baba, Grete), ekranda yalnız kollar
  [[[-100, 200], [700, 420]], [[2020, 250], [1250, 430]], [[960, -100], [980, 360]]].forEach(([a, b], i) => { const w = Math.sin(lt * 1.3 + i) * 20; const el = new Path2D(); FG.capsule(el, a, [b[0] + w, b[1]], 60, 46); FG.ellipseInto(el, b[0] + w, b[1] + 20, 66, 44, Math.atan2(b[1] - a[1], b[0] - a[0])); KS.siluet(g, el, { hale: 8, rim: 7, isik: [0, -1] }); });
  alinti(k, '“Parayı minnetle alıyorlardı… ama aralarında\nartık özel bir sıcaklık kalmamıştı.”', { y: 760, px: 54, ph: 170, pw: 1420, t0: 1.2 });
}));
// kapı aralığından içerisi: lamba altında baba küçük bir kasa açıyor (Gregor'un bakışı: karanlık taraf)
function a4_aralik(k, o = {}) {
  const g = k.m, gx = 830, ac = o.ac ?? 260;
  const ar = KS.rect(gx, 40, ac, 860); KS.ak(g, ar);
  g.save(); g.clip(ar);
  KS.tara(g, 'aralik:ic', [[[gx, 40], [gx + ac, 40], [gx + ac, 900], [gx, 900]]], { aci: Math.PI / 2, sp: 20, wmax: 9, seg: [80, 300], gap: [6, 24], seed: 301, renk: '#000', ton: () => .22 });
  if (o.ic) o.ic(k, gx, ac); g.restore();
  g.fillStyle = '#000'; g.fillRect(gx - 26, 40, 26, 860); KS.kenar(g, 'aralik:kenar', [[gx - 30, 40], [gx - 30, 900]], { w: 3, seed: 303 });
}
plan('P30', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.04 + .05 * st.p }, k => a4_aralik(k, { ic: (k2, gx, ac) => {
  O.fig(k2, { x: gx + ac * .55, y: 960, h: 760, f: -1, tip: 'baba', otur: true, egil: .35, bas: .3, kolN: [1.3, -.6], kolF: [1.1, -.4] }, { isik: [0, -1] });
  const ks = KS.rect(gx + 20, 640, 150, 100); KS.siluet(k2.m, ks, { hale: 6, rim: 6, isik: [0, -1] });
} })));
// kasanın içi: sikke yığınları büyür
plan('P31', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .06 * st.p }, k => {
  const g = k.m, lt = k.lt;
  const kut = KS.poly([[360, 300], [1560, 300], [1660, 860], [260, 860]]); g.strokeStyle = '#fff'; g.lineWidth = 16; g.stroke(kut);
  const kap = KS.poly([[360, 300], [1560, 300], [1500, 90], [420, 90]]); KS.ak(g, kap); g.save(); g.clip(kap); g.strokeStyle = '#000'; g.lineWidth = 5; for (let i = 0; i < 20; i++) { g.beginPath(); g.moveTo(420 + i * 60, 90); g.lineTo(380 + i * 62, 300); g.stroke(); } g.restore();
  const n = Math.floor(clamp(lt / 6) * 14) + 4;
  for (let s = 0; s < 6; s++) { const h = Math.min(n, 4 + s * 2 + Math.floor(n / 2)); for (let j = 0; j < h; j++) O.sikke(g, 520 + s * 180, 800 - j * 22, 72); }
}));
plan('P32', (ctx, st) => kes(ctx, st, { cx: 900 + st.lt * 30, cy: 470, z: 1.04 }, k => a2_yol(k)));
plan('P33', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.1 }, k => a4_aralik(k, { ac: 70 })));
// "başını salladı": kamera aralığa yakın, yavaşça iner kalkar (iki kez)
plan('P34', (ctx, st) => kes(ctx, st, { cx: 900, cy: 470 + Math.sin(clamp(st.lt / 2.4) * Math.PI * 4) * 18 * (1 - clamp(st.lt / 3)), z: 1.35 }, k => a4_aralik(k, { ac: 70 })));
// terazi: bir kefede Gregor'un fotoğrafı, ötekinde sikkeler; sikkeler ağır basar
plan('P35', (ctx, st) => kes(ctx, st, { cx: 960, cy: 480, z: 1.0 + .04 * st.p }, k => {
  const g = k.m, lt = k.lt;
  KS.tara(g, 'p35:fon', [[[58, 40], [1862, 40], [1862, 900], [58, 900]]], { dir: WC.dirRadial(960, 200), sp: 18, wmax: 6, seg: [60, 260], gap: [8, 26], seed: 311, ton: (x, y) => clamp(1 - Math.hypot(x - 960, y - 200) / 900) * .8 });
  const a = -.22 * E.outBack(clamp((lt - .8) / 1.6)) + Math.sin(lt * 2) * .01;
  KS.ak(g, KS.rect(945, 220, 30, 600)); KS.ak(g, KS.poly([[860, 860], [1060, 860], [1000, 810], [920, 810]]));
  g.save(); g.translate(960, 230); g.rotate(a);
  KS.ak(g, KS.rect(-520, -12, 1040, 24));
  for (const s of [-1, 1]) {
    g.strokeStyle = '#fff'; g.lineWidth = 4; g.beginPath(); g.moveTo(s * 500, 0); g.lineTo(s * 500 - 110, 300); g.moveTo(s * 500, 0); g.lineTo(s * 500 + 110, 300); g.stroke();
    g.save(); g.translate(s * 500, 300); g.rotate(-a);
    const kef = new Path2D(); kef.ellipse(0, 0, 150, 30, 0, 0, Math.PI); KS.ak(g, kef);
    if (s < 0) { const fr = KS.rect(-70, -170, 140, 170); KS.ak(g, fr); g.fillStyle = '#000'; g.fillRect(-56, -156, 112, 142); const F = IN.insan({ x: 0, y: 40, h: 260, f: 1, tip: 'gregor' }); g.save(); g.beginPath(); g.rect(-56, -156, 112, 142); g.clip(); g.strokeStyle = '#fff'; g.lineWidth = 4; g.stroke(F.p); g.restore(); }
    else for (let j = 0; j < 9; j++) O.sikke(g, (j % 3 - 1) * 70, -18 - Math.floor(j / 3) * 18, 44);
    g.restore();
  }
  g.restore();
}));
// keman çalan Grete (pencere önü), Gregor (insan) dinliyor
function a4_keman(k, o = {}) {
  const g = k.m, lt = k.lt;
  O.pencere(k, 'keman', 760, 120, 420, 520, { gok: (k2, x, y, w, h) => { const gg = k2.m; gg.save(); gg.clip(KS.rect(x, y, w, h)); gg.strokeStyle = '#000'; gg.lineWidth = 3; for (let i = 0; i < 16; i++) { gg.beginPath(); gg.moveTo(x, y + h - i * 18); gg.lineTo(x + w, y + h - i * 20 - 30); gg.stroke(); } gg.restore(); } });
  KS.ak(g, KS.rect(58, 820, 1804, 10));
  const sw = Math.sin(lt * 3) * .12;
  const F = O.fig(k, { x: 1000, y: 820, h: 520, f: -1, tip: 'grete', bas: .25, kolN: [2.2 + sw, -1.6], kolF: [2.0, -2.2] }, { isik: [.2, -1] });
  const kem = new Path2D(); FG.ellipseInto(kem, F.bas[0] - 34, F.bas[1] + 50, 46, 26, -.5); FG.capsule(kem, [F.bas[0] - 40, F.bas[1] + 48], [F.bas[0] - 170, F.bas[1] + 120], 7, 6); KS.siluet(g, kem, { hale: 5, rim: 4, isik: [0, -1] });
  g.strokeStyle = '#fff'; g.lineWidth = 4; g.beginPath(); g.moveTo(F.elN[0] + 60, F.elN[1] - 80); g.lineTo(F.elN[0] - 120, F.elN[1] + 60); g.stroke();
  if (o.dinleyen !== false) O.fig(k, { x: 1500, y: 860, h: 560, f: -1, tip: o.dinleyenTip || 'gregor', otur: o.otur ?? false, bas: .1, kolN: [.1, -.1], kolF: [-.1, -.1] }, { isik: [-1, -.6] });
}
plan('P36', (ctx, st) => kes(ctx, st, { cx: 980 + 60 * st.p, cy: 470, z: 1.02 }, k => a4_keman(k)));
