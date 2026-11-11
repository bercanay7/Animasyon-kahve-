// cen grubu (CEN: cennet): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Açık anahtar: kâğıt beyazı kütleler, ışık merkezine göre eş merkezli tarama, %15–25 koyu çapa.
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const cen_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));
let CEN_YOL = (typeof location !== 'undefined' && new URLSearchParams(location.search).get('cenyol')) || 'b';   // a: ışıklı çizgili figür, b: ters ışık

// ═════════ P019 (C02): melek safları arasında başmelek (açık tariflerin üslup karesi) ═════════
// (b) ters ışık: ışık merkezi başmeleğin alnının üstündeki sabah yıldızıdır ("ışık taşıyan"); gök ondan ışınsal açılır.
function cen_c02(t, o = {}) {
  const back = (o.yol ?? CEN_YOL) === 'b', FX = 560, FY = 540, h = 66, SX = FX + 14, SY = FY - 6.3 * h, L = back ? { x: SX, y: SY } : { x: 1380, y: 110 };
  cen_gok(L, back ? { r0: 280, r1: 1300, v: .7, n: 100 } : { r0: 330, r1: 1300, v: .72, n: 96 });
  // bulut terasları: sakin katlar (kenar hilali, damla yok), ufukta küçülür; saflar katların üstünde beyaz kütle
  cen_bank({ x0: 820, x1: 2120, y: 560, amp: 24, wl: 260, seed: 21, L, rim: 1, cuts: 0, endW: 160, endD: 120 });
  cen_safKutle({ x0: 900, x1: 2000, y: 640, h: 9, seed: 11, nSp: 12, spV: 0 });
  cen_bank({ x0: 760, x1: 2140, y: 650, amp: 34, wl: 340, seed: 22, L, rim: 1, cuts: 0, endW: 200, endD: 160 });
  cen_safKutle({ x0: 860, x1: 2000, y: 800, h: 15, seed: 12, nSp: 10, spV: 0 });
  cen_bank({ x0: 700, x1: 2160, y: 800, amp: 46, wl: 420, seed: 23, L, rim: 1, cuts: 0, endW: 240, endD: 200 });
  // ön plan: büyük koyu bulut kümeleri (Nifates dili)
  cen_bulutKat({ x0: 960, x1: 2300, y: 1010, h: 260, seed: 26, L, t, n: 4 });
  if (!back) cen_bulutKat({ x0: -200, x1: 900, y: 300, h: 330, yb: H + 100, seed: 24, L, t, n: 3 });
  cen_aydin({ x: FX, y: FY, h, facing: 1, L, t, back, head: .2, twist: .32, armN: [-.08, .3], armF: [.2, 1.3], lift: .55, open: .85, wingS: 7.5 });
  if (back) cen_yildiz(SX, SY, 46, .85 + .15 * Math.sin(t * .9), { ink: 5 });
  cen_bulutKat({ x0: -300, x1: 1100, y: 960, h: 280, seed: 25, L, t, n: 4 });
}
plan('P019', (ctx, st) => {
  const cam = camLerp({ cx: 1000, cy: 540, z: 1.05 }, { cx: 920, cy: 540, z: 1.05 }, st.p, E.io2);
  levha(ctx, cam, () => cen_c02(st.t), [.8, 0, 1]);
}, { tr: { type: 'fade', dur: .8 } });

// P002 (A02) nif.js'e taşındı (kanca çifti A01/A02 tek elde).

// ═════════ P017 (B10): sayfadaki güneş büyür, cennetin ışığına açılır ═════════
function cen_b10(t) {
  const { ox } = GR, s0 = S('B10'), u = E.io2(cen_u(t, s0 - .2, Se('B10') + 1.2)), v = E.io2(cen_u(t, s0 + .2, Se('B10') + 1.6));
  const L = { x: lerp(863, 960, u), y: lerp(184, 160, u) };
  // ışınlar en baştan: güneşin çevresi temiz kâğıt (büyür), dışı seyrek ışınlı
  cen_gok(L, { r0: lerp(150, 380, u), r1: lerp(700, 1400, u), v: lerp(.8, .7, u), n: 96 });
  // çizilmiş halka ve ışınlar: büyüdükçe söner
  const fa = 1 - E.sine(cen_u(u, .15, .55));
  if (fa > 0) { ox.save(); ox.globalAlpha = fa; ox.strokeStyle = GR.inkCol; ox.lineCap = 'round'; ox.lineWidth = 3.4; const r0 = 30 * (1 + 5 * u);
    ox.beginPath(); ox.arc(L.x, L.y, r0, 0, TAU); ox.stroke();
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU + .1, l = (i % 2 ? 16 : 26) * (1 + 5 * u); ox.beginPath(); ox.moveTo(L.x + Math.cos(a) * r0 * 1.33, L.y + Math.sin(a) * r0 * 1.33); ox.lineTo(L.x + Math.cos(a) * (r0 * 1.33 + l), L.y + Math.sin(a) * (r0 * 1.33 + l)); ox.stroke(); }
    ox.restore(); }
  // koyu bulut bankları alttan yükselir
  const dy = (1 - v) * 520;
  cen_bank({ x0: -120, x1: 820, y: 560 + dy, amp: 60, wl: 360, seed: 61, L, cuts: .8 });
  cen_bank({ x0: 1100, x1: 2040, y: 540 + dy * 1.15, amp: 60, wl: 360, seed: 62, L, cuts: .8 });
  cen_teras({ x0: -140, x1: 2060, y: 860 + dy * .6, d: 40, seed: 63, L, cuts: .7 });
}
plan('P017', (ctx, st) => levha(ctx, null, () => cen_b10(st.t), [.975, 0, 1]), { tr: { type: 'paper', dur: 1.0 } });

// ═════════ P018 (C01): bölüm kartı "IŞIK TAŞIYAN": ışık, bulut terasları ═════════
function cen_c01(t) {
  const L = { x: 960, y: 210 }, dr = Math.sin(t * .1) * 6;
  cen_gok(L, { r0: 520, r1: 1400, v: .72, n: 100 });
  cen_bank({ x0: -140, x1: 700, y: 600, amp: 70, wl: 380, seed: 71, L, cuts: .8, drift: dr });
  cen_bank({ x0: 1220, x1: 2060, y: 590, amp: 70, wl: 380, seed: 72, L, cuts: .8, drift: -dr });
  cen_teras({ x0: -140, x1: 2060, y: 880, d: 46, seed: 73, L, cuts: .7 });
}
// açık kart: ince mürekkep çizgi + başlık + soru (temiz kâğıt bölgede mürekkep harf; panel yok)
function cen_kart(ctx, title, soru, lt, d) {
  if (NOTEXT) return;
  const a = clamp(lt / .6) * clamp((d - lt) / .6); if (a <= 0) return;
  const x = 960, y = 330, px = 92;
  ctx.save(); ctx.globalAlpha *= E.sine(a);
  const lw = 250 * E.out3(clamp(lt / 1.1)); ctx.strokeStyle = INK_CSS; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x - lw, y - px * .82); ctx.lineTo(x + lw, y - px * .82); ctx.stroke();
  txt(ctx, title, x, y, { px, ls: 10, col: INK_CSS });
  ctx.font = FONT.alinti(56); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = INK_CSS; ctx.globalAlpha *= clamp((lt - .5) / .6);
  wrapLines(ctx, soru, 1200).forEach((l, i) => ctx.fillText(l, x, y + px * 1.0 + i * 62));
  ctx.restore();
}
plan('P018', (ctx, st) => levha(ctx, null, () => cen_c01(st.t), [.8, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => cen_kart(ctx, 'IŞIK TAŞIYAN', 'Her şeye sahip olan biri, neden başkaldırır?', st.lt, st.end - st.at) });

// ═════════ P020 (C03): profil (belden yukarı), alnının üstünde sabah yıldızı; "LUCIFER · ışık taşıyan" ═════════
function cen_c03(t) {
  const L = { x: 1760, y: 90 }, tL = Wd('C03', 'lüsifer'), sa = .4 + .6 * E.out3(cen_u(t, tL - .3, tL + .9));
  cen_gok(L, { r0: 360, r1: 1300, v: .72, n: 96 });
  cen_bank({ x0: -140, x1: 1240, y: 220, amp: 80, wl: 460, seed: 81, L, cuts: .8, drift: Math.sin(t * .07) * 6 });
  const J = cen_basmelek({ x: 860, y: 1080, h: 138, facing: -1, L, t, head: .3, twist: .2, armN: [.05, .3], armF: [-.1, .4], spear: false, lift: .55, open: .55, wingS: 4.2, legs: false });
  const hd = J.hd; cen_yildiz(hd[0] - 34, hd[1] - 1.6 * 138 + Math.sin(t * .8) * 2, 78, sa);
}
plan('P020', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 940, cy: 530, z: 1.06 }, st.p, E.io2), () => cen_c03(st.t), [.8, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => {
    const t0 = Wd('C03', 'lüsifer') - .1, a = E.sine(clamp((st.t - t0) / .6)) * clamp((st.end - st.t) / .5);
    cen_yazi(ctx, 'LUCIFER · ışık taşıyan', 1480, 800, a, { px: 46, ls: 4 }); } });

// ═════════ P021 (C04): iki ışık (yalnız ışık); melekler Batı saray selamıyla eğilir; başmelek dik durur, gölgesi uzar ═════════
function cen_c04(t) {
  const { tx, px, tone } = GR, tO = Wd('C04', 'oğulu'), tD = Wd('C04', 'diz'), L = { x: 520, y: 130 };
  const o2 = E.io2(cen_u(t, tO - .4, tO + 1.4)), dl = E.io2(cen_u(t, tD - .5, Se('C04')));
  cen_gok(L, { r0: 300, r1: 1500, v: .72, n: 100 });
  if (o2 > 0) cen_isik(1010, 190, 46 * o2, o2);
  // arka: koyu kalabalık bankı; önünde eğilen beyaz saf
  cen_bank({ x0: -120, x1: 1320, y: 560, amp: 26, wl: 300, seed: 91, L, cuts: .6 });
  cen_safKutle({ x0: -60, x1: 1250, y: 700, h: 13, seed: 92, nSp: 0, bow: E.io2(cen_u(dl, .1, .7)) });
  cen_bank({ x0: -140, x1: 1340, y: 700, amp: 18, wl: 300, seed: 93, L, cuts: .7, ends: false });
  // ön plan: üç büyükçe figür tek diz üstünde (her biri kendi anında), koyu bankın önünde
  [[200, 980, 64, .0], [520, 1000, 70, .12], [880, 990, 62, .22]].forEach(([x, y, h, d], i) =>
    cen_melek({ x, y, h, f: 1, bow: E.io2(cen_u(dl, d, d + .45)), spear: null, seed: 30 + i, wing: 0 }));
  // sağ: başmelek, koyu duvarın önünde dik; zemin açık teras, gölgesi üstünde uzar
  cen_bank({ x0: 1340, x1: 2060, y: 330, amp: 50, wl: 300, seed: 94, L, cuts: .8 });
  cen_teras({ x0: 1280, x1: 2060, y: 900, d: 110, seed: 95, L, cuts: .6 });
  const fx = 1620, fy = 930, sl = lerp(120, 420, dl);
  { const P = new Path2D(); P.moveTo(fx - 36, fy - 2); P.quadraticCurveTo(fx + sl * .5, fy + 12, fx + sl, fy + 34); P.lineTo(fx + sl - 24, fy + 56); P.quadraticCurveTo(fx + sl * .45, fy + 44, fx + 26, fy + 16); P.closePath();
    tx.fillStyle = tone(.02); tx.fill(P); px.fillStyle = GR.hatch({ th: .05, id: 0 }); px.fill(P); }
  cen_basmelek({ x: fx, y: fy - 3.95 * 66, h: 66, facing: -1, L, t, head: .12, twist: .3, armN: [-.05, .2], armF: [.2, 1.3], lift: .35, open: .5, wingS: 4.2 });
  cen_bank({ x0: -140, x1: 1300, y: 1040, amp: 14, wl: 300, seed: 96, L, cuts: .5, ends: false });
}
plan('P021', (ctx, st) => levha(ctx, null, () => cen_c04(st.t), [.8, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// ═════════ P022 (C05): cennetin alacakaranlığı; başmelek yardımcısının kulağına eğilir; uzakta kuzeye yürüyen saflar, tepede saray ═════════
function cen_c05(t) {
  const L = { x: 1700, y: 300 }, s0 = S('C05'), mv = (t - s0) * 10;
  cen_gok(L, { r0: 170, r1: 900, v: .62, n: 84 });
  // tepede saray: koyu tepenin üstünde koyu siluet
  cen_bank({ x0: 1380, x1: 2060, y: 420, amp: 30, wl: 240, seed: 101, L, cuts: .6 });
  cen_saray(1650, 400, 200, -1);
  // kuzeye yürüyen beyaz saflar (koyu bankların önünde)
  cen_bank({ x0: 520, x1: 2080, y: 520, amp: 18, wl: 300, seed: 102, L, cuts: .5 });
  cen_safKutle({ x0: 620 + mv * .7, x1: 1500 + mv * .7, y: 610, h: 8, seed: 103, nSp: 10 });
  cen_bank({ x0: 480, x1: 2080, y: 606, amp: 16, wl: 280, seed: 104, L, cuts: .6, ends: false });
  cen_safKutle({ x0: 560 + mv, x1: 1600 + mv, y: 740, h: 12.5, seed: 105, nSp: 9 });
  cen_bank({ x0: 440, x1: 2080, y: 736, amp: 18, wl: 300, seed: 106, L, cuts: .7, ends: false });
  // ön sol: koyu duvarın önünde iki beyaz figür; başmelek arkadan yardımcısının kulağına eğilir
  cen_bank({ x0: -140, x1: 700, y: 330, amp: 60, wl: 380, seed: 107, L, cuts: .8 });
  cen_basmelek({ x: 560, y: 610, h: 70, facing: 1, L, t, head: -.05, twist: .35, armN: [.1, .3], armF: [.3, .4], spear: false, lift: .25, open: .35, wingS: 4, seed: 9 });
  cen_basmelek({ x: 410, y: 590 + Math.sin(t * .5) * 2, h: 72, facing: 1, L, t, head: -.32, lean: .22, twist: .3, armN: [.35, .4], armF: [.5, .5], spear: false, lift: .3, open: .4, wingS: 4.2 });
  cen_teras({ x0: -140, x1: 2080, y: 900, d: 36, seed: 108, L, cuts: .8 });
}
plan('P022', (ctx, st) => levha(ctx, null, () => cen_c05(st.t), [.6, 0, 1]), { tr: { type: 'fade', dur: 1.0 } });

// ═════════ P023 (C06): yüksek tepede ordusuna hitap; kolu havada; "özgürlük" ═════════
function cen_c06(t) {
  const L = { x: 1560, y: 130 }, tK = Wd('C06', 'konuşur'), up = E.out3(cen_u(t, tK - .2, tK + .9));
  cen_gok(L, { r0: 300, r1: 1300, v: .7, n: 96 });
  // tepenin arkasında koyu bulut duvarı; tepe basamaklı koyu kütle
  cen_bank({ x0: -140, x1: 1240, y: 300, amp: 40, wl: 380, seed: 111, L, cuts: .8 });
  cen_bank({ x0: 420, x1: 1000, y: 660, amp: 14, wl: 200, seed: 112, L, cuts: .7 });
  cen_basmelek({ x: 710, y: 660 - 3.95 * 58 + 6, h: 58, facing: 1, L, t, head: .2 + .1 * up, twist: .35, armN: [lerp(-.1, 2.15, up), lerp(.3, .35, up)], armF: [.1, .5], lift: .3, open: .45, wingS: 4, spear: false });
  // aşağıda ordu: beyaz saflar tepeye dönük, koyu bankların önünde
  cen_bank({ x0: 900, x1: 2080, y: 700, amp: 16, wl: 280, seed: 113, L, cuts: .5 });
  cen_safKutle({ x0: 980, x1: 2000, y: 800, h: 10, seed: 114, nSp: 10 });
  cen_bank({ x0: -140, x1: 2080, y: 798, amp: 16, wl: 300, seed: 115, L, cuts: .6, ends: false });
  cen_safKutle({ x0: -60, x1: 2000, y: 950, h: 16, seed: 116, nSp: 12 });
  cen_bank({ x0: -140, x1: 2080, y: 946, amp: 18, wl: 300, seed: 117, L, cuts: .8, ends: false });
}
plan('P023', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 900, cy: 520, z: 1.08 }, st.p, E.io2), () => cen_c06(st.t), [.7, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => {
    const t0 = Wd('C06', 'özgürlük') - .1, a = E.sine(clamp((st.t - t0) / .7)) * clamp((st.end - st.t) / .4);
    cen_yazi(ctx, 'özgürlük', 1420, 330, a, { px: 104, font: FONT.alinti(104), ls: 2 }); } });

// ═════════ P024 (C07): alttan bakış: dinleyen saflar; mızraklar tek tek kalkar (az ve boyları farklı) ═════════
function cen_c07(t) {
  const L = { x: 1300, y: 60 }, t0 = Wd('C07', 'biz'), t1 = Wd('C07', 'koyabilir');
  cen_gok(L, { r0: 340, r1: 1300, v: .72, n: 100 });
  const ang = (i, sd) => { const q = hash(i * 7.31 + sd), tt = lerp(t0, t1, q); return lerp(-1.0, 0, E.out3(cen_u(t, tt, tt + .8))); };
  cen_bank({ x0: -140, x1: 2080, y: 560, amp: 40, wl: 360, seed: 121, L, cuts: .7 });
  cen_safKutle({ x0: -60, x1: 2000, y: 700, h: 13, seed: 122, nSp: 10, spAng: i => ang(i, 1) });
  cen_bank({ x0: -140, x1: 2080, y: 696, amp: 18, wl: 300, seed: 123, L, cuts: .6, ends: false });
  cen_safKutle({ x0: -60, x1: 2000, y: 880, h: 22, seed: 124, nSp: 9, spAng: i => ang(i, 2) });
  cen_bank({ x0: -140, x1: 2080, y: 876, amp: 20, wl: 320, seed: 125, L, cuts: .7, ends: false });
  cen_safKutle({ x0: -100, x1: 2040, y: 1150, h: 38, seed: 126, nSp: 8, spAng: i => ang(i, 3) });
}
plan('P024', (ctx, st) => levha(ctx, camLerp({ cx: 940, cy: 540, z: 1.04 }, { cx: 1000, cy: 540, z: 1.04 }, st.p, E.io2), () => cen_c07(st.t), [.7, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// ═════════ P025 (C08): koyu bulut kütlesinde ışık noktaları: üçte biri ayrılıp onun peşine kayar ═════════
function cen_c08(t) {
  const { tx, px, tone } = GR, L = { x: 1640, y: 120 }, tY = Wd('C08', 'yalanlarıyla'), s0 = S('C08');
  const go = E.io2(cen_u(t, tY, Se('C08') + 1.2)), lead = E.io2(cen_u(t, s0, Se('C08') + 1.5));
  cen_gok(L, { r0: 300, r1: 1200, v: .72, n: 96 });
  cen_bank({ x0: -160, x1: 2080, y: 400, amp: 44, wl: 420, seed: 131, L, cuts: .6, yb: 700, ends: false });
  cen_teras({ x0: -160, x1: 2080, y: 900, d: 50, seed: 132, L, cuts: .6 });
  const lx = lerp(1050, 300, lead), ly = lerp(520, 640, lead), q = rng(77), N = 130;
  for (let i = 0; i < N; i++) {
    const a = q() * TAU, r = Math.sqrt(q()), x0 = 1300 + Math.cos(a) * r * 520, y0 = 560 + Math.sin(a) * r * 100, fol = (i % 3) === 0, ph = q(), sz = 4 + q() * 4;
    let x = x0, y = y0;
    if (fol) { const k = E.io2(clamp(go * 1.25 - ph * .25)); x = lerp(x0, lx + 60 + (x0 - 1300) * .45, k); y = lerp(y0, ly + (y0 - 540) * .55, k); }
    const D = new Path2D(); poly(D, [[x, y - sz * 2], [x + sz * .45, y - sz * .45], [x + sz * 2, y], [x + sz * .45, y + sz * .45], [x, y + sz * 2], [x - sz * .45, y + sz * .45], [x - sz * 2, y], [x - sz * .45, y - sz * .45]], true);
    tx.fillStyle = tone(1); tx.fill(D);
  }
  cen_yildiz(lx, ly, 34, 1);
}
plan('P025', (ctx, st) => levha(ctx, null, () => cen_c08(st.t), [.7, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => { const t0 = Wd('C08', 'üçte') - .1, a = clamp((st.t - t0) / .5) * clamp((st.end - st.t) / .5);
    cen_yazi(ctx, 'üçte biri', 500, 480, E.sine(a), { px: 50, ls: 4, col: PAPER_CSS }); } });

// ═════════ P027 (C10): koyu kalabalığın içinde tek beyaz figür ayağa kalkar: Abdiel ═════════
function cen_c10(t) {
  const tK = Wd('C10', 'kalkar'), up = E.io2(cen_u(t, tK - .6, tK + .7)), gl = E.io2(cen_u(t, tK - .3, Se('C10') + .5));
  const AX = 1000, L = { x: AX, y: 470 };
  cen_gok(L, { r0: lerp(120, 320, gl), r1: 1100, v: .66, n: 90 });
  const crowd = (y, h, n, sd) => { const q = rng(sd); for (let i = 0; i < n; i++) { const x = -40 + (i + .5 + (q() - .5) * .8) / n * 2020; if (Math.abs(x - AX) < h * 1.6 && h > 20) continue;
    let lx = L.x - x, ly = L.y - (y - 6 * h); const l = Math.hypot(lx, ly); cen_melek({ x, y: y + (q() - .5) * h * .4, h: h * (.9 + q() * .2), f: x < AX ? 1 : -1, lx: lx / l, ly: ly / l, v: .03, spear: null, seed: sd * 50 + i, wing: .5 }); } };
  cen_bank({ x0: -140, x1: 2080, y: 530, amp: 24, wl: 300, seed: 55, L, cuts: .5, ends: false });
  crowd(700, 12, 40, 51); crowd(800, 17, 28, 52);
  cen_melek({ x: AX, y: 900, h: 42, f: -1, bow: 1 - up, spear: null, seed: 5, v: .99, wing: .9 });
  crowd(960, 26, 17, 53); crowd(1130, 38, 11, 54);
}
plan('P027', (ctx, st) => levha(ctx, null, () => cen_c10(st.t), [.7, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => { const t0 = Wd('C10', 'abdiyeldir') - .1, a = clamp((st.t - t0) / .5) * clamp((st.end - st.t) / .5);
    cen_yazi(ctx, 'ABDIEL', 1000, 250, E.sine(a), { px: 50 }); } });

// ═════════ P028 (C11): Abdiel açılan safların arasından tek başına yürüyüp gider (yandan kaydırma) ═════════
function cen_c11(t) {
  const s0 = S('C11'), w = cen_u(t, s0, Se('C11') + 1), AX = lerp(560, 1900, w), L = { x: AX + 60, y: 260 };
  cen_gok(L, { r0: 260, r1: 1100, v: .66, n: 90 });
  cen_bank({ x0: -140, x1: 2500, y: 560, amp: 24, wl: 300, seed: 65, L: { x: 1200, y: 260 }, cuts: .5, ends: false });
  const q0 = rng(61);
  for (let i = 0; i < 44; i++) { const x = -60 + i * 58 + (q0() - .5) * 30, d = x - AX, h = 16 * (.9 + q0() * .2);
    let lx = L.x - x, ly = L.y - 600; const l = Math.hypot(lx, ly); cen_melek({ x: x + Math.sign(d) * Math.exp(-d * d / 9000) * 18, y: 770 + (q0() - .5) * 8, h, f: d < 0 ? 1 : -1, lx: lx / l, ly: ly / l, v: .03, spear: null, seed: 70 + i, wing: .5 }); }
  const ph = (t - s0) * 3.4, sw = Math.sin(ph) * .38;
  cen_basmelek({ x: AX, y: 900 - 3.95 * 40 - Math.abs(Math.cos(ph)) * 3, h: 40, facing: 1, L: { x: AX + 400, y: 100 }, t, head: .12, twist: .55, armN: [-sw * .6, .2], armF: [sw * .6, .2],
    legN: [sw, -.1 - .2 * Math.max(0, -Math.sin(ph))], legF: [-sw, -.1 - .2 * Math.max(0, Math.sin(ph))], spear: false, lift: .2, open: .2, wingS: 3.6 });
  const R = rng(62);
  for (let i = 0; i < 12; i++) { const x = -100 + i * 230 + (R() - .5) * 60, gap = Math.exp(-Math.pow((x - AX) / 260, 2)) * 70; let lx = L.x - x, ly = L.y - 900; const l = Math.hypot(lx, ly);
    cen_melek({ x: x + Math.sign(x - AX) * gap, y: 1180 + (R() - .5) * 30, h: 46, f: x < AX ? 1 : -1, lx: lx / l, ly: ly / l, spear: null, v: .03, seed: 90 + i, wing: .6 }); }
}
plan('P028', (ctx, st) => levha(ctx, camLerp({ cx: 760, cy: 560, z: 1.05 }, { cx: 1160, cy: 560, z: 1.05 }, st.p, E.sine), () => cen_c11(st.t), [.7, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => { const t0 = Wd('C11', 'binlerce') - .2; quote(ctx, '“binlerce hainin arasında sadık kalan tek kişi”', 960, 190, st.t - t0, { px: 66, per: .45, panel: false, col: INK_CSS }); } });
