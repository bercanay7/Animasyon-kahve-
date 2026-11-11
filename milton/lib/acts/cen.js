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
  cen_bank({ x0: 820, x1: 2120, y: 560, amp: 24, wl: 260, seed: 21, L, rim: 1, rim: 1, cuts: 0, endW: 120, endD: 60 });
  cen_safKutle({ x0: 900, x1: 2000, y: 646, h: 12, seed: 11, nSp: 12, spV: 0 });
  cen_bank({ x0: 760, x1: 2140, y: 650, amp: 34, wl: 340, seed: 22, L, rim: 1, rim: 1, cuts: 0, endW: 140, endD: 70 });
  cen_safKutle({ x0: 860, x1: 2000, y: 810, h: 20, seed: 12, nSp: 10, spV: 0 });
  cen_bank({ x0: 700, x1: 2160, y: 800, amp: 46, wl: 420, seed: 23, L, rim: 1, rim: 1, cuts: 0, endW: 160, endD: 80 });
  // ön plan: büyük koyu bulut kümeleri (Nifates dili)
  cen_bulutKat({ x0: 960, x1: 2300, y: 1010, h: 260, seed: 26, L, t, n: 4 });
  if (!back) cen_bulutKat({ x0: -200, x1: 900, y: 300, h: 330, yb: H + 100, seed: 24, L, t, n: 3 });
  cen_aydin({ x: FX, y: FY, h, facing: 1, L, t, back, head: .2, twist: .32, armN: [-.08, .3], armF: [.2, 1.3], lift: .55, open: .85, wingS: 7.5 });
  if (back) cen_yildiz(SX, SY, 62, .85 + .15 * Math.sin(t * .9), { ink: 5 });
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
  // koyu bulut terasları alttan yükselir (iki yanda katlı küme, önde alçak kat)
  const dy = (1 - v) * 520;
  cen_bulutKat({ x0: -400, x1: 760, y: 700 + dy, h: 400, yb: H + 200, seed: 61, L, t, n: 4 });
  cen_bulutKat({ x0: 1160, x1: 2320, y: 680 + dy * 1.15, h: 400, yb: H + 200, seed: 62, L, t, n: 4 });
  cen_bulutKat({ x0: -300, x1: 2220, y: 960 + dy * .6, h: 200, yb: H + 200, seed: 63, L, t, n: 7 });
}
plan('P017', (ctx, st) => levha(ctx, null, () => cen_b10(st.t), [.975, 0, 1]), { tr: { type: 'paper', dur: 1.0 } });

// ═════════ P018 (C01): bölüm kartı "IŞIK TAŞIYAN": ışık, bulut terasları ═════════
function cen_c01(t) {
  const L = { x: 960, y: 210 }, dr = Math.sin(t * .1) * 6;
  cen_gok(L, { r0: 520, r1: 1400, v: .72, n: 100 });
  cen_bulutKat({ x0: -400, x1: 680, y: 720, h: 400, yb: H + 200, seed: 71, L, t, n: 4 });
  cen_bulutKat({ x0: 1240, x1: 2320, y: 700, h: 400, yb: H + 200, seed: 72, L, t, n: 4 });
  cen_bulutKat({ x0: -300, x1: 2220, y: 960, h: 190, yb: H + 200, seed: 73, L, t, n: 7 });
}
// açık kart: ince mürekkep çizgi + başlık + soru (temiz kâğıt bölgede mürekkep harf; panel yok)
function cen_kart(ctx, title, soru, lt, d) {
  if (NOTEXT) return;
  const a = clamp(lt / .6) * clamp((d - lt) / .6); if (a <= 0) return;
  const x = 960, y = 330, px = 92;
  ctx.save(); ctx.globalAlpha *= E.sine(a);
  const lw = 250 * E.out3(clamp(lt / 1.1)); ctx.strokeStyle = INK_CSS; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x - lw, y - px * .82); ctx.lineTo(x + lw, y - px * .82); ctx.stroke();
  txt(ctx, title, x, y, { px, ls: 10, col: INK_CSS });
  ctx.font = FONT.alinti(64); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = INK_CSS; ctx.globalAlpha *= clamp((lt - .5) / .6);   // soru ≥ 64 px (telefon)
  wrapLines(ctx, soru, 1300).forEach((l, i) => ctx.fillText(l, x, y + px * 1.02 + i * 76));
  ctx.restore();
}
plan('P018', (ctx, st) => levha(ctx, null, () => cen_c01(st.t), [.8, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => cen_kart(ctx, 'IŞIK TAŞIYAN', 'Her şeye sahip olan biri, neden başkaldırır?', st.lt - .7, st.end - st.at - .7) });   // önceki yazı söndükten ≥ 0,3 sn sonra

// ═════════ P020 (C03): profil (belden yukarı), alnının üstünde sabah yıldızı; "LUCIFER · ışık taşıyan" ═════════
function cen_c03(t) {
  // ters ışık profil: baş-omuz koyu siluet, arkasında büyük kanat kemeri; ışık alnının üstündeki sabah yıldızından açılır
  const tL = Wd('C03', 'lüsifer'), sa = .45 + .55 * E.out3(cen_u(t, tL - .3, tL + .9)), h = 150, FX = 900, FY = 1120;
  const J0 = SF.rig({ x: FX, y: FY, h, facing: -1, twist: .15, head: .3 }), SX = J0.hd[0] - 40, SY = J0.hd[1] - 1.75 * h, L = { x: SX, y: SY };
  cen_gok(L, { r0: lerp(420, 640, sa), r1: 1500, v: .72, n: 100 });
  cen_bulutKat({ x0: 1150, x1: 2300, y: 980, h: 260, seed: 81, L, t, n: 4 });
  cen_bulutKat({ x0: -300, x1: 600, y: 1010, h: 240, seed: 82, L, t, n: 3 });
  cen_aydin({ x: FX, y: FY, h, facing: -1, L, t, back: true, head: .3, twist: .15, armN: [.05, .3], armF: [-.1, .4], spear: false, legs: false, lift: .85, open: .95, wingS: 5.6, cloak: .6 });
  cen_yildiz(SX, SY, 70 * (.8 + .2 * sa), sa, { ink: 6 });
}
plan('P020', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 960, cy: 540, z: 1.06 }, st.p, E.io2), () => cen_c03(st.t), [.8, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => {
    const t0 = Wd('C03', 'lüsifer') - .1, a = E.sine(clamp((st.t - t0) / .6)) * clamp((st.end - st.t) / .5);
    cen_yazi(ctx, 'LUCIFER', 1300, 230, a, { px: 76, ls: 10 }); cen_yazi(ctx, 'ışık taşıyan', 1300, 320, a, { px: 64, font: FONT.alinti(64), ls: 1 }); } });

// ═════════ P021 (C04): iki ışık (yalnız ışık); melekler Batı saray selamıyla eğilir; başmelek dik durur, gölgesi uzar ═════════
// Batı saray selamı (şövalye selamı): TEK diz yerde, gövde dik (≤ 14° öne), baş hafif eğik, yakın el göğüste ya da kılıç öne.
// Koyu siluet + kenar ışığı; kanatlar yarı kapalı (KN.feathered). b: 0 ayakta … 1 selamda. sw: kılıç öne uzatılmış
function cen_selam(x, gy, h, f, b, L, t, seed, o = {}) {
  // ara pozda uzun hamle adımı yok: önce kalça iner (iki diz hafif bükülür), öndeki uyluk geç öne gelir (bF), arka diz yere iner
  const bF = E.in2(b), hipY = gy - lerp(4.05, 2.15, b) * h, tw = o.tw ?? .45, hd = (o.head ?? .05);
  const J = SF.rig({ x, y: hipY, h, facing: f, twist: tw, lean: .24 * b, head: lerp(hd, -.28, b), shTilt: -.02,
    armN: o.sw ? [lerp(.1, .5, b), lerp(.2, .9, b)] : [lerp(.1, -.1, b), lerp(.2, 2.35, b)], armF: [lerp(-.05, -.15, b), .3],
    legN: [lerp(.05, 1.5, bF), lerp(-.05, -1.5, bF) - .5 * Math.sin(PI * b)], legF: [lerp(-.05, -.05, b), lerp(-.03, -1.55, b)] });
  let lx = L.x - J.shC[0], ly = L.y - J.shC[1]; { const l = Math.hypot(lx, ly) || 1; lx /= l; ly /= l; }
  if (o.wings !== false) for (const [side, sd0] of [[-1, 71], [1, 72]]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    if (h < 30) { cen_kanatKoyu(sh[0] - side * h * .2, sh[1] + h * .2, side, (side < 0 ? 3.4 : 3.0) * h, { lift: 1.1, open: .9, seed: seed * 7 + sd0, t, L }); continue; }   // uzak: ucuz kapalı kanat
    GR.frame(sh[0] - side * h * .25, sh[1] + h * .15, (side < 0 ? -.05 : .08), side, 1);
    KN.feathered({ span: (side < 0 ? 5.4 : 4.8) * h, open: .32, lift: .72, droop: .2, ruin: 0, dark: .93, rim: .8, t, seed: seed * 7 + sd0, root: .1, lit: [lx * side, ly] });
    GR.unframe();
  }
  SF.draw(J, { lum: .12, lit: [lx, ly], t, legs: true, skirt: true, eye: 0, wind: .3, cloak: .5, halo: 3, lines: h > 40 ? 1.5 : 0, seed, armor: true });
  // kılıç: her an dik, ucu aşağıda (teslim/selam); kabzası elde, ucu öne dizin yanında yere iner. Hiçbir an yatay değil, komşuya doğrulmaz.
  if (o.sw) { const w = J.wrN; cen_mizrak(w[0], w[1] - .1 * h, PI - .12 * f, 3.4 * h, .9, Math.max(2, h * .06), h * .7, 0); }
}
function cen_c04(t) {
  const { tx, px, tone } = GR, tO = Wd('C04', 'oğulu'), tD = Wd('C04', 'diz'), L = { x: 820, y: 150 };
  const tG = Wd('C04', 'tanrı'), tT = Wd('C04', 'toplar');
  const o2 = E.out2(cen_u(t, tO, tO + .8)), dl = E.io2(cen_u(t, tD - .5, Se('C04'))), g1 = E.io2(cen_u(t, tG - .3, tG + 1.4));
  cen_gok(L, { r0: lerp(200, 320, g1), r1: 1500, v: .7, n: 100 });   // "Tanrı"da ışık açılır
  if (o2 > 0) cen_isik(1170, 220, 46 * o2, o2);                        // "oğulu"da ikinci ışık doğar
  // uzak kalabalık: alçak kütle (dalgayla eğilir), ufukta; zemin alçak tutulur ki selam verenlerin başı ışığa karşı okunsun
  cen_bank({ x0: -200, x1: 1500, y: 835, amp: 12, wl: 260, seed: 91, L, rim: 1, cuts: 0, endW: 140, endD: 40 });
  cen_safKutle({ x0: 0, x1: 1300, y: 880, h: 5, seed: 92, nSp: 0, bow: .5 * E.io2(cen_u(t, tD + .3, tD + 1.6)) });
  // açık bulut zemini (kâğıt, seyrek perspektifli yatay çizgi): diz çökenlerin tek dizi ve gövdesi bütün siluetiyle okunur
  { const Z = new Path2D(); Z.rect(-300, 878, W + 600, 400); GR.fill(Z, tone(.9), { type: 'persp', y0: 878, D: 300, p0: 16, p1: 40, id: 10 }); }
  // derinlikte düzensiz kalabalık: arkadan öne (küçükten büyüğe), karışık yönler; her biri 'diz'den sonra kendi gecikmesiyle (dalga) diz çöker
  // [x, zemin y, h, gecikme (sn), bakış, kılıç]
  const G = [[330, 905, 15, .5, 1], [520, 900, 14, .7, -1], [690, 910, 16, .3, 1], [1000, 902, 15, .9, -1], [1170, 912, 16, .6, -1], [190, 918, 18, .8, 1],
    [840, 922, 18, .2, -1], [420, 938, 22, .45, 1], [1090, 945, 24, .75, -1],
    [150, 1010, 40, 0, 1, true], [560, 990, 38, .35, 1], [1210, 1035, 44, .6, -1, true], [900, 1065, 52, .15, -1]];
  // "toplar"da başlar ışığa kalkar, "oğulu"da ikinci ışığa döner (baş eğimi); kanatlar hafif kıpırdar (KN t)
  G.forEach(([x, gy, h, d, f, sw], i) => { const b = E.io2(cen_u(t, tD + d, tD + d + .9)), hu = E.io2(cen_u(t, tT + .05 * i, tT + .6 + .05 * i)) * .22 + E.io2(cen_u(t, tO + .1 + .06 * i, tO + .8 + .06 * i)) * (f > 0 ? .1 : -.06);
    cen_selam(x, gy, h, f, b, L, t, 40 + i, { sw, tw: .3 + .12 * (i % 3), wings: h > 14, head: .05 + hu }); });
  // sağ: başmelek dik duruyor (tek eğilmeyen), alnının üstünde yıldız; gölgesi açık terasta uzar
  const fx = 1600, fy = 950, sl = lerp(140, 480, dl);
  { const P = new Path2D(); P.moveTo(fx - 40, fy - 2); P.quadraticCurveTo(fx + sl * .5, fy + 8, fx + sl, fy + 26); P.lineTo(fx + sl - 20, fy + 44); P.quadraticCurveTo(fx + sl * .45, fy + 34, fx + 24, fy + 14); P.closePath();
    tx.fillStyle = tone(.02); tx.fill(P); px.fillStyle = GR.hatch({ th: .05, id: 0 }); px.fill(P); }
  const J = cen_aydin({ x: fx, y: fy - 4.05 * 76, h: 76, facing: -1, L, t, back: true, head: .15, twist: .6, armN: [-.05, .2], armF: [.2, 1.3], lift: .5, open: .7, wingS: 6.4 });
  cen_yildiz(J.hd[0] - 4, J.hd[1] - 1.35 * 76, 30, .7, { ink: 3 });
  cen_bulutKat({ x0: -500, x1: 520, y: 1080, h: 240, seed: 96, L, t, n: 3 });
  cen_bulutKat({ x0: 1250, x1: 2400, y: 1100, h: 220, seed: 98, L, t, n: 3 });
}
plan('P021', (ctx, st) => levha(ctx, null, () => cen_c04(st.t), [.8, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// ═════════ P022 (C05): cennetin alacakaranlığı; başmelek yardımcısının kulağına eğilir; uzakta kuzeye yürüyen saflar, tepede saray ═════════
function cen_c05(t) {
  // orta plan, aynalı yerleşim (C02/C04'ten farklı): sağda iki büyük siluet (başmelek yardımcısının kulağına eğilmiş);
  // solda uzakta alacakaranlık ışığı, tepede kristal saray, oraya (kuzeye, sola) yürüyen küçük saflar
  const L = { x: 330, y: 360 }, s0 = S('C05'), mv = (t - s0) * 10;
  cen_gok(L, { r0: 200, r1: 1000, v: .62, n: 90 });
  cen_bank({ x0: -200, x1: 620, y: 470, amp: 30, wl: 240, seed: 101, L, rim: 1, cuts: 0, endW: 120, endD: 60 });
  cen_saray(300, 452, 190, 1);
  cen_bank({ x0: -200, x1: 1300, y: 600, amp: 16, wl: 300, seed: 102, L, rim: 1, cuts: 0, endW: 120, endD: 60 });
  cen_safKutle({ x0: 380 - mv * .7, x1: 1200 - mv * .7, y: 680, h: 8, seed: 103, nSp: 10, spV: 0 });
  cen_bank({ x0: -200, x1: 1400, y: 690, amp: 22, wl: 280, seed: 104, L, rim: 1, cuts: 0, endW: 140, endD: 70 });
  cen_safKutle({ x0: 300 - mv, x1: 1300 - mv, y: 830, h: 13, seed: 105, nSp: 9, spV: 0 });
  cen_bank({ x0: -200, x1: 1500, y: 830, amp: 30, wl: 320, seed: 106, L, rim: 1, cuts: 0, endW: 160, endD: 80 });
  // sağ: bulut terası ve iki büyük siluet
  cen_bulutKat({ x0: 1050, x1: 2400, y: 1000, h: 260, seed: 107, L, t, n: 4 });
  cen_aydin({ x: 1560, y: 560, h: 104, facing: -1, L, t, back: true, head: .05, twist: .7, armN: [.1, .3], armF: [.3, .4], spear: false, lift: .25, open: .4, wingS: 4.6, seed: 9 });
  const J = cen_aydin({ x: 1730, y: 545 + Math.sin(t * .5) * 2, h: 108, facing: -1, L, t, back: true, head: -.3, lean: .24, twist: .6, armN: [.35, .4], armF: [.6, .9], spear: false, lift: .35, open: .5, wingS: 5 });
  cen_yildiz(J.hd[0] + 10, J.hd[1] - 1.25 * 108, 26, .45, { ink: 3 });
}
plan('P022', (ctx, st) => levha(ctx, null, () => cen_c05(st.t), [.6, 0, 1]), { tr: { type: 'fade', dur: 1.0 } });

// ═════════ P023 (C06): yüksek tepede ordusuna hitap; kolu havada; "özgürlük" ═════════
function cen_c06(t) {
  // ters açı: dinleyen kalabalığın arkasından yukarı bakış. Önde büyük koyu sırtlar ve mızraklar; yukarıda yüksek bulut terasının
  // kenarında, ışığın önünde, kolu havada başmelek (ayakları terasın üst yüzünde)
  const L = { x: 1000, y: 240 }, tK = Wd('C06', 'konuşur'), up = E.out3(cen_u(t, tK - .2, tK + .9));
  cen_gok(L, { r0: 320, r1: 1300, v: .7, n: 100 });
  // terası: sağdan uzanan koyu bulut kütlesi, figür kenarında
  cen_bulutKat({ x0: 760, x1: 2300, y: 680, h: 260, seed: 112, L, t, n: 5 });
  cen_aydin({ x: 900, y: 610 - 4.05 * 62, h: 62, facing: -1, L, t, back: true, head: .25 + .1 * up, twist: .5, armN: [lerp(-.1, 2.3, up), .3], armF: [.1, .4], lift: .45, open: .6, wingS: 5.5, spear: false });
  // alt: dinleyen kalabalık sırtları (koyu, büyük, üç derinlik), başlar yukarıya; seyrek mızrak
  const crowd = (y, h, n, sd, sp) => { const q = rng(sd); for (let i = 0; i < n; i++) { const x = -60 + (i + .5 + (q() - .5) * .9) / n * 2040; let lx = L.x - x, ly = L.y - (y - 6 * h); const l = Math.hypot(lx, ly);
    cen_melek({ x, y: y + (q() - .5) * h * .5, h: h * (.85 + q() * .3), f: x < L.x ? 1 : -1, lx: lx / l, ly: ly / l, v: .03, spear: q() < sp ? (q() - .5) * .12 : null, spV: 0, sl: 6 + q() * 3, seed: sd * 40 + i, wing: .6 }); } };
  crowd(860, 18, 26, 61, .25); crowd(980, 30, 15, 62, .3); crowd(1180, 52, 9, 63, .35);
}
plan('P023', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 960, cy: 540, z: 1.06 }, st.p, E.io2), () => cen_c06(st.t), [.7, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => {
    const t0 = Wd('C06', 'özgürlük') - .1, a = E.sine(clamp((st.t - t0) / .7)) * clamp((st.end - st.t) / .4);
    cen_yazi(ctx, 'özgürlük', 1420, 330, a, { px: 104, font: FONT.alinti(104), ls: 2 }); } });

// ═════════ P024 (C07): alttan bakış: dinleyen saflar; mızraklar tek tek kalkar (az ve boyları farklı) ═════════
function cen_c07(t) {
  // yakın yan bakış: dinleyen saflar bireyler olarak (barkod gibi şerit değil). Konuşan kadraj dışında sağda (ışık oradan);
  // iki-üç derinlikte koyu siluetler sağa bakar; mızraklar yatık durur, sözle tek tek dikilir.
  const L = { x: 2050, y: 260 }, t0 = Wd('C07', 'biz'), t1 = Wd('C07', 'koyabilir');
  cen_gok(L, { r0: 420, r1: 1500, v: .7, n: 100 });
  const ang = (i, sd) => { const q = hash(i * 7.31 + sd), tt = lerp(t0, t1, q); return lerp(-.75, (q - .5) * .08, E.out3(cen_u(t, tt, tt + .8))); };
  { const Z = new Path2D(); Z.rect(-300, 800, W + 600, 500); GR.fill(Z, GR.tone(.9), { type: 'persp', y0: 800, D: 300, p0: 16, p1: 40, id: 10 }); }
  cen_bank({ x0: -200, x1: 2200, y: 800, amp: 8, wl: 360, seed: 121, L, rim: 1, cuts: 0, ends: false, yb: 812 });
  const row = (y, h, n, sd, x0, x1) => { const q = rng(sd); for (let i = 0; i < n; i++) { const x = lerp(x0, x1, (i + .5 + (q() - .5) * .8) / n), hh = h * (.88 + q() * .24);
    let lx = L.x - x, ly = L.y - (y - 6 * hh); const l = Math.hypot(lx, ly);
    cen_melek({ x, y: y + (q() - .5) * h * .5, h: hh, f: 1, lx: lx / l, ly: ly / l, v: .03, spear: q() < .55 ? ang(i, sd) : null, spV: 0, sl: 6.5 + q() * 2.5, seed: sd * 40 + i, wing: .5 + .4 * q() }); } };
  row(830, 20, 16, 1, -60, 1980); row(950, 34, 9, 2, -80, 1980); row(1170, 58, 5, 3, -120, 1900);
}
plan('P024', (ctx, st) => levha(ctx, camLerp({ cx: 920, cy: 540, z: 1.04 }, { cx: 1000, cy: 540, z: 1.04 }, st.p, E.io2), () => cen_c07(st.t), [.7, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// ═════════ P025 (C08): koyu bulut kütlesinde ışık noktaları: üçte biri ayrılıp onun peşine kayar ═════════
function cen_c08(t) {
  const { tx, px, tone } = GR, L = { x: 1640, y: 120 }, tY = Wd('C08', 'yalanlarıyla'), s0 = S('C08');
  const go = E.io2(cen_u(t, tY, Se('C08') + 1.2)), lead = E.io2(cen_u(t, s0, Se('C08') + 1.5));
  cen_gok(L, { r0: 300, r1: 1200, v: .72, n: 96 });
  cen_bank({ x0: -160, x1: 2080, y: 400, amp: 44, wl: 420, seed: 131, L, rim: 1, cuts: 0, yb: 700, ends: false });
  cen_teras({ x0: -160, x1: 2080, y: 900, d: 50, seed: 132, L, rim: 1, cuts: 0 });
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
  cen_bank({ x0: -140, x1: 2080, y: 530, amp: 24, wl: 300, seed: 55, L, rim: 1, cuts: 0, ends: false });
  crowd(700, 12, 40, 51); crowd(800, 17, 28, 52);
  cen_melek({ x: AX, y: 930, h: 58, f: -1, bow: 1 - up, spear: null, seed: 5, v: .99, wing: .9 });
  crowd(960, 26, 17, 53); crowd(1130, 38, 11, 54);
}
plan('P027', (ctx, st) => levha(ctx, null, () => cen_c10(st.t), [.7, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => { const t0 = Wd('C10', 'abdiyeldir') - .1, a = clamp((st.t - t0) / .5) * clamp((st.end - st.t) / .5);
    cen_yazi(ctx, 'ABDIEL', 1000, 250, E.sine(a), { px: 50 }); } });

// ═════════ P028 (C11): Abdiel açılan safların arasından tek başına yürüyüp gider (yandan kaydırma) ═════════
function cen_c11(t) {
  const s0 = S('C11'), w = cen_u(t, s0, Se('C11') + 1), AX = lerp(560, 1900, w), L = { x: AX + 60, y: 260 };
  cen_gok(L, { r0: 260, r1: 1100, v: .66, n: 90 });
  cen_bank({ x0: -140, x1: 2500, y: 560, amp: 24, wl: 300, seed: 65, L: { x: 1200, y: 260 }, rim: 1, cuts: 0, ends: false });
  const q0 = rng(61);
  for (let i = 0; i < 44; i++) { const x = -60 + i * 58 + (q0() - .5) * 30, d = x - AX, h = 16 * (.9 + q0() * .2);
    let lx = L.x - x, ly = L.y - 600; const l = Math.hypot(lx, ly); cen_melek({ x: x + Math.sign(d) * Math.exp(-d * d / 9000) * 18, y: 770 + (q0() - .5) * 8, h, f: d < 0 ? 1 : -1, lx: lx / l, ly: ly / l, v: .03, spear: null, seed: 70 + i, wing: .5 }); }
  const ph = (t - s0) * 3.4, sw = Math.sin(ph) * .38;
  cen_basmelek({ x: AX, y: 920 - 3.95 * 54 - Math.abs(Math.cos(ph)) * 3, h: 54, facing: 1, L: { x: AX + 400, y: 100 }, t, head: .12, twist: .55, armN: [-sw * .6, .2], armF: [sw * .6, .2],
    legN: [sw, -.1 - .2 * Math.max(0, -Math.sin(ph))], legF: [-sw, -.1 - .2 * Math.max(0, Math.sin(ph))], spear: false, lift: .2, open: .2, wingS: 3.6 });
  const R = rng(62);
  for (let i = 0; i < 12; i++) { const x = -100 + i * 230 + (R() - .5) * 60, gap = Math.exp(-Math.pow((x - AX) / 260, 2)) * 70; let lx = L.x - x, ly = L.y - 900; const l = Math.hypot(lx, ly);
    cen_melek({ x: x + Math.sign(x - AX) * gap, y: 1180 + (R() - .5) * 30, h: 46, f: x < AX ? 1 : -1, lx: lx / l, ly: ly / l, spear: null, v: .03, seed: 90 + i, wing: .6 }); }
}
plan('P028', (ctx, st) => levha(ctx, camLerp({ cx: 760, cy: 560, z: 1.05 }, { cx: 1160, cy: 560, z: 1.05 }, st.p, E.sine), () => cen_c11(st.t), [.7, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => { const t0 = Wd('C11', 'binlerce') - .2; quote(ctx, '“binlerce hainin arasında sadık kalan tek kişi”', 960, 190, st.t - t0, { px: 72, per: .45, panel: false, col: INK_CSS }); } });
