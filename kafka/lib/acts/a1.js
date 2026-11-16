// Perde 1 (P01–P09): Bir sabah. Kamera çoğunlukla yerden (Gregor'un bakışı); böcek hiç görünmez.
'use strict';
const ZY = 640;   // oda planlarında zemin çizgisi
// açılış karesi (kapak A ile aynı): karanlık oda, aralık kapı, ışık şeridinde kırmızı elma
function a1_kapiKaresi(k, o = {}) {
  const ac = o.ac ?? 46, key = o.key || 'kapi';
  // duvar: kapının çevresinde ışıktan doğan seyrek dikey kesikler (duvar kâğıdı), uzakta blok
  KS.tara(k.m, key + ':duvar', [[[58, 40], [1862, 40], [1862, ZY], [58, ZY]]], { aci: Math.PI / 2, sp: 17, wmax: 4.5, seg: [30, 120], gap: [8, 30], seed: 21,
    ton: (x, y) => clamp(1 - Math.abs(x - 1270) / 520 - Math.abs(y - 380) / 900) * .7 });
  KS.kenar(k.m, key + ':supurge', [[58, ZY - 30], [1862, ZY - 30]], { w: 2.2, seg: [70, 240], gap: [6, 20], seed: 23 });
  // zemin: kaçış noktasına koşan derzler, ışık şeridinin iki yanında sönen
  KS.tara(k.m, key + ':zemin', [[[58, ZY], [1862, ZY], [1862, 900], [58, 900]]], { dir: (x, y) => Math.atan2(y - (ZY - 300), x - 1270), sp: 15, wmax: 5, seg: [40, 180], gap: [5, 20], seed: 27,
    ton: (x, y) => clamp(1 - Math.abs(x - 1270 - (y - ZY) * .2) / (180 + (y - ZY) * 1.4)) * .55 });
  O.kapi(k, key, { ac, gx: 1250, y0: 70, zemY: ZY, x0: 1040, x1: 1470, serW: 520, serX: 1220, vx: 1270 });
  if (o.elma !== false) {
    const ex = o.ex ?? 1215, ey = o.ey ?? 772, er = o.er ?? 54;
    k.m.fillStyle = '#000'; k.m.beginPath(); k.m.ellipse(ex + 26, ey + er * .92, er * 1.25, er * .24, 0, 0, TAU); k.m.fill();
    O.elma(k, ex, ey, er, { rot: -.2 });
  }
}
plan('P01', (ctx, st) => kes(ctx, st, { cx: 1100, cy: 470, z: 1.04 + .05 * E.io2(st.p) }, k => a1_kapiKaresi(k, { ac: 30 + 26 * E.io2(clamp(st.lt / 5)) })));

// kapı boşluğunda aile (aşağıdan bakış); arkalarında ışık
function a1_aileKapida(k, o = {}) {
  const g = k.m, x0 = 520, x1 = 1400, y0 = 40, zy = 900;
  const bos = KS.rect(x0, y0, x1 - x0, zy - y0); KS.ak(g, bos);
  g.save(); g.clip(bos); KS.isin(g, 'aile:arka', 960, 300, { n: 40, r0: 260, r1: [700, 1000], w: 14, renk: '#000', seed: 12 }); g.restore();
  KS.kenar(g, 'aile:kasa', [[x0, zy], [x0, y0]], { w: 5, seed: 72 }); KS.kenar(g, 'aile:kasa2', [[x1, y0], [x1, zy]], { w: 5, seed: 73 });
  const bob = Math.sin(k.lt * .9) * .01, ba = o.bas ?? .3;
  O.fig(k, { x: 690, y: zy + 30, h: 760, f: 1, tip: 'anne', bas: ba + .05, kolN: [.4, 1.0], kolF: [.25, 1.1] }, { isik: [.6, -1] });
  O.fig(k, { x: 1210, y: zy + 30, h: 720, f: -1, tip: 'grete', bas: ba + .1 + Math.sin(k.lt * .6) * .02, kolN: [.3, .7], kolF: [.1, .4] }, { isik: [-.6, -1] });
  O.fig(k, { x: 950, y: zy + 60, h: 860, f: -1, tip: 'baba', bas: ba + bob, kep: !!o.kep, kolN: [.08, -.05], kolF: [-.06, -.05] }, { isik: [0, -1] });
}
plan('P02', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470 - 24 * E.io2(st.p), z: 1.0 + .05 * st.p }, k => a1_aileKapida(k)));

// başlık levhası: kara blok, oyulmuş başlık; kenarda ince oyma çerçeve
function a1_levha(k, baslik, alt, o = {}) {
  KS.kenar(k.m, 'levha:cerceve', [[150, 120], [1770, 120], [1770, 820], [150, 820], [150, 120]], { w: 3, seg: [80, 260], gap: [4, 12], seed: 81 });
  KS.kenar(k.m, 'levha:cerceve2', [[176, 146], [1744, 146], [1744, 794], [176, 794], [176, 146]], { w: 1.8, seg: [60, 200], gap: [5, 14], seed: 82 });
  oyYazi(k, baslik, 960, o.y ?? 420, { font: YF.serif(o.px ?? 170, 600), ls: 18, t0: .15, dur: 1.0 });
  if (alt) oyYazi(k, alt, 960, (o.y ?? 420) + 150, { font: YF.serif(46, 600), ls: 10, t0: .9, dur: .8 });
}
plan('P03', (ctx, st) => kes(ctx, st, null, k => a1_levha(k, 'DÖNÜŞÜM', 'FRANZ KAFKA · 1915'), { nefes: .03 }));

// yüksekten oda: yatak, kabarık yorgan yavaşça inip kalkar (altında ne olduğu görünmez), pencerede yağmur, duvarda resim
function a1_oda(k, o = {}) {
  const g = k.m, nef = Math.sin(k.lt * 1.3) * 6;
  O.pencere(k, 'oda', 230, 120, 330, 400, { yagmur: o.yagmur !== false, gece: o.gece });
  // duvarda çerçeveli resim (kürklü kadın, uzaktan küçük leke; ayrıntı yok)
  KS.kenar(g, 'oda:resim', [[760, 150], [930, 150], [930, 330], [760, 330], [760, 150]], { w: 3.4, seed: 91 });
  // zemin: seyrek tahta kesikleri (pencere ışığı)
  KS.tara(g, 'oda:zemin', [[[58, 640], [1862, 640], [1862, 900], [58, 900]]], { aci: .08, sp: 16, wmax: 4.5, seg: [80, 260], gap: [6, 24], seed: 93, ton: (x, y) => clamp(1 - Math.abs(x - 520) / 900) * .55 });
  // yatak: başlık tahtası, şilte, kabaran yorgan (oyulmuş kıvrımlar biçimi sarar)
  const bx = 1000, by = 520;
  g.fillStyle = '#000';
  KS.kenar(g, 'oda:yatakBas', [[bx + 620, by - 200], [bx + 620, by + 200]], { w: 5, seed: 94 });
  const yor = new Path2D(); yor.moveTo(bx - 120, by + 120); yor.bezierCurveTo(bx + 40, by - 40 - nef, bx + 300, by - 70 - nef * 1.4, bx + 560, by - 20); yor.lineTo(bx + 600, by + 140); yor.lineTo(bx - 140, by + 160); yor.closePath();
  KS.ak(g, yor);
  g.save(); g.clip(yor); g.strokeStyle = '#000';
  for (let i = 0; i < 16; i++) { g.lineWidth = 3 + i * .5; g.beginPath(); const yy = by - 60 + i * 15 - nef * (1 - i / 16); g.moveTo(bx - 160, yy + 90); g.bezierCurveTo(bx + 60, yy - 10, bx + 330, yy - 20, bx + 640, yy + 40); g.stroke(); }
  g.restore();
  g.fillStyle = '#000'; g.fillRect(bx - 150, by + 150, 760, 26); g.fillRect(bx - 140, by + 170, 20, 150); g.fillRect(bx + 580, by + 170, 20, 150);
  KS.kenar(g, 'oda:yatakAlt', [[bx - 150, by + 178], [bx + 610, by + 178]], { w: 3, seed: 95 });
  // kumaş örnekleri sandığı (masada, satıcının işi)
  KS.kenar(g, 'oda:sandik', [[300, 700], [560, 700], [560, 800], [300, 800], [300, 700]], { w: 3, seed: 96 });
}
plan('P04', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .04 * st.p }, k => a1_oda(k)));

// çalar saat: altı buçuk; saniye ibresi
function a1_saat(k, t, o = {}) {
  const g = k.m, cx = 960, cy = 470, R = 300;
  const kad = new Path2D(); kad.arc(cx, cy, R, 0, TAU); KS.ak(g, kad);
  g.strokeStyle = '#000'; g.lineWidth = 16; g.beginPath(); g.arc(cx, cy, R - 8, 0, TAU); g.stroke();
  for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; g.lineWidth = i % 3 ? 7 : 14; g.beginPath(); g.moveTo(cx + Math.sin(a) * (R - 30), cy - Math.cos(a) * (R - 30)); g.lineTo(cx + Math.sin(a) * (R - (i % 3 ? 62 : 85)), cy - Math.cos(a) * (R - (i % 3 ? 62 : 85))); g.stroke(); }
  // zil çanları ve ayaklar (kara, ak hale)
  for (const s of [-1, 1]) { const b = new Path2D(); b.arc(cx + s * 210, cy - 300, 92, Math.PI, 0); b.closePath(); KS.siluet(g, b, { hale: 8, isik: [0, -1], rim: 7 }); g.strokeStyle = '#fff'; g.lineWidth = 6; g.beginPath(); g.moveTo(cx + s * 220, cy + 270); g.lineTo(cx + s * 300, cy + 380); g.stroke(); }
  const ang = (h, m) => ((h % 12) + m / 60) / 12 * TAU;
  const yel = (o.dk ?? 30) / 60 * TAU, akr = ang(o.sa ?? 6, o.dk ?? 30);
  g.strokeStyle = '#000'; g.lineCap = 'round';
  g.lineWidth = 22; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.sin(akr) * 160, cy - Math.cos(akr) * 160); g.stroke();
  g.lineWidth = 14; g.beginPath(); g.moveTo(cx, cy); g.lineTo(cx + Math.sin(yel) * 240, cy - Math.cos(yel) * 240); g.stroke();
  const sn = Math.floor(t) / 60 * TAU * 1; g.lineWidth = 5; g.beginPath(); g.moveTo(cx - Math.sin(sn) * 40, cy + Math.cos(sn) * 40); g.lineTo(cx + Math.sin(sn) * 260, cy - Math.cos(sn) * 260); g.stroke();
  g.fillStyle = '#000'; g.beginPath(); g.arc(cx, cy, 22, 0, TAU); g.fill();
}
plan('P05', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .08 * E.io2(st.p) }, k => a1_saat(k, k.lt * 1.0 + 12)));

// istasyon: tren kalkıyor, buhar oyulur
function a1_tren(k, o = {}) {
  const g = k.m, lt = k.lt, dx = -E.in2(clamp(lt / 6)) * 900;
  // gök: üstte geniş U-oyma süpürmeler
  KS.tara(g, 'tren:gok', [[[58, 40], [1862, 40], [1862, 430], [58, 430]]], { aci: -.05, sp: 22, wmax: 13, kind: 'u', seg: [140, 420], gap: [10, 40], seed: 101, ton: (x, y) => clamp(1 - y / 520) * .9 });
  // peron: ak şerit + kenar
  KS.ak(g, KS.poly([[58, 700], [1862, 640], [1862, 690], [58, 760]]));
  KS.tara(g, 'tren:peron', [[[58, 760], [1862, 690], [1862, 900], [58, 900]]], { aci: -.03, sp: 18, wmax: 4, seg: [60, 200], gap: [10, 30], seed: 103, ton: () => .25 });
  // tren: lokomotif + vagonlar (kara siluet, pencereler ak)
  g.save(); g.translate(dx, 0);
  const lok = new Path2D(); lok.rect(300, 470, 420, 200); lok.rect(560, 360, 160, 130); lok.rect(340, 400, 70, 80);
  for (let i = 0; i < 4; i++) lok.rect(740 + i * 380, 470, 360, 200);
  KS.siluet(g, lok, { hale: 7, isik: [-.2, -1], rim: 6 });
  for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const w = KS.rect(770 + i * 380 + j * 84, 500, 56, 60); KS.ak(g, w); }
  for (let i = 0; i < 9; i++) { const wh = new Path2D(); wh.arc(330 + i * 175, 680, 34, 0, TAU); g.fillStyle = '#000'; g.fill(wh); g.strokeStyle = '#fff'; g.lineWidth = 4; g.stroke(wh); }
  g.restore();
  // buhar: bacadan yükselen oyulmuş bulutlar (yerinde kalır, tren çıkar)
  const r = rng(7);
  for (let i = 0; i < 7; i++) { const bx = 375 + dx * .2 - i * 40 + r() * 30, by = 380 - i * 48, br = 50 + i * 20; const b = new Path2D(); b.arc(bx, by, br, 0, TAU); KS.ak(g, b); g.save(); g.clip(b); g.strokeStyle = '#000'; g.lineWidth = 3; for (let j = 0; j < 6; j++) { g.beginPath(); g.arc(bx + br * .3, by + br * .3, br * (1.2 - j * .12), Math.PI * .9, Math.PI * 1.5); g.stroke(); } g.restore(); }
}
plan('P06', (ctx, st) => kes(ctx, st, null, k => a1_tren(k), { nefes: .03 }));

// aşağıdan patron: yüksek kürsü, öne eğilmiş siluet
function a1_patron(k) {
  const g = k.m;
  KS.isin(g, 'patron:isik', 1300, 120, { n: 26, r0: 60, r1: [500, 900], w: 12, a0: 1.6, a1: 3.0, seed: 111 });
  const kursu = KS.poly([[600, 900], [1400, 900], [1340, 420], [660, 420]]); KS.siluet(g, kursu, { hale: 8, isik: [.6, -1], rim: 7 });
  KS.tara(g, 'patron:kursu', [[[660, 440], [1340, 440], [1390, 880], [610, 880]]], { aci: 0, sp: 26, wmax: 3, seg: [200, 600], gap: [20, 60], seed: 113, ton: () => .25 });
  O.fig(k, { x: 1000, y: 700, h: 640, f: -1, tip: 'mudur', melon: false, egil: .5 + Math.sin(k.lt * 2.4) * .04, bas: .2, kolN: [1.3, .2], kolF: [.6, .6] }, { isik: [.6, -1] });
}
plan('P07', (ctx, st) => kes(ctx, st, { cx: 980, cy: 470, z: 1.0 + .04 * st.p }, k => a1_patron(k)));

// boş çerçeve: bıçak içini oymaya başlar ve durur (böceği görmeyeceğiz)
function a1_cerceve(k) {
  const g = k.m, lt = k.lt;
  KS.tara(g, 'cerceve:duvar', [[[58, 40], [1862, 40], [1862, 900], [58, 900]]], { aci: Math.PI / 2, sp: 20, wmax: 3.5, seg: [40, 140], gap: [10, 34], seed: 121, ton: () => .3 });
  const fr = KS.poly([[640, 160], [1280, 160], [1280, 780], [640, 780]]); g.fillStyle = '#000'; g.fill(fr);
  KS.ak(g, KS.rect(600, 120, 720, 40)); KS.ak(g, KS.rect(600, 780, 720, 40)); KS.ak(g, KS.rect(600, 120, 40, 700)); KS.ak(g, KS.rect(1280, 120, 40, 700));
  g.save(); g.clip(KS.rect(600, 120, 720, 700)); g.strokeStyle = '#000'; g.lineWidth = 4; for (let i = 0; i < 40; i++) { g.beginPath(); g.moveTo(560 + i * 22, 100); g.lineTo(560 + i * 22 - 120, 860); g.stroke(); } g.restore();
  g.fillStyle = '#000'; g.fillRect(640, 160, 640, 620);
  // bıçak içeri girer: birkaç kesik başlar ve yarıda kalır
  const pr = clamp((lt - .6) / 2.2), r = rng(4);
  g.strokeStyle = '#fff'; g.lineCap = 'round';
  for (let i = 0; i < 9; i++) { const y = 230 + i * 58, L = 380 * clamp(pr * 1.6 - i * .12) * (.4 + r() * .4); if (L <= 0) continue; g.lineWidth = 6 - i * .3; g.beginPath(); g.moveTo(700, y); g.lineTo(700 + L, y + 8); g.stroke(); }
}
plan('P08', (ctx, st) => kes(ctx, st, { cx: 960, cy: 470, z: 1.0 + .06 * E.io2(st.p) }, k => a1_cerceve(k)));

// aile portresi: baba (oturan), anne arkasında, Grete yanında; Grete'ye ışık
function a1_portre(k) {
  const g = k.m;
  KS.tara(g, 'portre:fon', [[[58, 40], [1862, 40], [1862, 900], [58, 900]]], { dir: WC.dirRadial(1180, 330), sp: 16, wmax: 7, seg: [60, 260], gap: [6, 22], seed: 131, ton: (x, y) => clamp(1 - Math.hypot(x - 1180, y - 330) / 760) * .9 });
  O.fig(k, { x: 760, y: 840, h: 640, f: 1, tip: 'anne', bas: .05, kolN: [.3, .9], kolF: [.2, 1.0] }, { isik: [1, -.6] });
  O.fig(k, { x: 920, y: 860, h: 700, f: 1, tip: 'baba', otur: true, kolN: [.6, -.9], kolF: [.5, -.8] }, { isik: [1, -.6] });
  O.fig(k, { x: 1240, y: 850, h: 600, f: -1, tip: 'grete', bas: .1 + Math.sin(k.lt * .8) * .03, kolN: [.2, .5], kolF: [.1, .3] }, { isik: [-1, -.6], rim: 10 });
}
plan('P09', (ctx, st) => kes(ctx, st, { cx: 960 + 60 * E.io2(st.p), cy: 470, z: 1.02 + .04 * st.p }, k => a1_portre(k)));
