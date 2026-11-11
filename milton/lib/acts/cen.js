// cen grubu (CEN: cennet): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Açık anahtar: kâğıt beyazı kütleler, ışık merkezine göre eş merkezli tarama, %15–25 koyu çapa.
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const cen_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));

// ═════════ P019 (C02): melek safları arasında başmelek (açık tariflerin üslup karesi) ═════════
function cen_c02(t, o = {}) {
  const L = { x: 1380, y: 110 }, dr = Math.sin(t * .07) * 6;
  cen_gok(L, { r0: 330, r1: 1300, v: .64, n: 96, kama: [{ a: PI * .83, w: .03, len: 1100 }] });
  // sol: başmeleğin arkasındaki koyu bulut duvarı (sakin, geniş kabarımlı)
  cen_bank({ x0: -120, x1: 980, y: 300, amp: 70, wl: 420, seed: 3, L, cuts: .8, drift: dr });
  // sağ: basamaklı saflar: koyu bank, beyaz saf, koyu bank ... (uzaklaştıkça küçülür)
  cen_bank({ x0: 820, x1: 2060, y: 470, amp: 22, wl: 300, seed: 5, L, cuts: .5, drift: -dr });
  cen_safKutle({ x0: 900, x1: 2000, y: 560, h: 6.5, seed: 11, nSp: 12 });
  cen_bank({ x0: 780, x1: 2080, y: 556, amp: 16, wl: 260, seed: 6, L, cuts: .6, ends: false });
  cen_safKutle({ x0: 870, x1: 2000, y: 668, h: 10, seed: 12, nSp: 11 });
  cen_bank({ x0: 740, x1: 2100, y: 664, amp: 18, wl: 300, seed: 7, L, cuts: .7, ends: false });
  cen_safKutle({ x0: 860, x1: 2000, y: 818, h: 15.5, seed: 13, nSp: 9 });
  cen_bank({ x0: 700, x1: 2120, y: 812, amp: 20, wl: 340, seed: 8, L, cuts: .8, ends: false });
  // başmelek: kalça (640, 560), koyu duvarın önünde; ayakları ön terasta
  cen_basmelek({ x: 600, y: 560, h: 76, facing: 1, L, t, head: .2, twist: .32, armN: [-.08, .3], armF: [.2, 1.3], lift: .45, open: .75, wingS: 4.6 });
  // ön teras: kâğıt üst yüz, koyu ön yüz (karenin alt çapası)
  cen_teras({ x0: -140, x1: 2100, y: 862, d: 34, seed: 9, L, cuts: .8 });
}
plan('P019', (ctx, st) => {
  const cam = camLerp({ cx: 1000, cy: 540, z: 1.05 }, { cx: 920, cy: 540, z: 1.05 }, st.p, E.io2);
  levha(ctx, cam, () => cen_c02(st.t), [.8, 0, 1]);
}, { tr: { type: 'fade', dur: .8 } });

// ═════════ P002 (A02): eşleme kesmesi: Nifates silueti → ışıklı başmelek (aynı duruş, aynı kadraj) ═════════
// Yerleşim NIF ile ortak: kalça (860, 560), h 96, facing 1, kanatlar yarı açık. Işık 1 sn'de açılır, cümle sonunda söner.
function cen_a02(t) {
  const s0 = S('A02'), s1 = Se('A02'), on = E.io2(cen_u(t, s0, s0 + 1)), off = E.io2(cen_u(t, s1 - .2, s1 + .9)), a = on * (1 - .85 * off);
  const L = { x: 1360, y: 240 };
  cen_gok(L, { r0: 150, a, v: lerp(.4, .72, a), mid: lerp(.55, .9, a), dark: 1 - a, kama: [{ a: PI * .86, w: .04, len: 1300 }, { a: PI * .62, w: .03, len: 900 }] });
  cen_bulut({ x: 1300, y: 900, w: 1700, h: 150, seed: 51, L, sh: .95, n: 10, len: 1.8 });
  cen_basmelek({ x: 860, y: 560, h: 96, facing: 1, L, t, lum: lerp(.12, 1, smooth(inv(.42, .58, a))), head: .22, twist: .3, armN: [-.1, .25], armF: [.35, .6], spear: false, open: -.25, lift: -.2, cloak: .7 });
  cen_bulut({ x: 560, y: 1100, w: 2300, h: 130, seed: 52, L, sh: 1, n: 12, len: 1.5, by: -.2 });
}
plan('P002', (ctx, st) => levha(ctx, null, () => cen_a02(st.t), [.8, 0, 1]), { tr: { type: 'cut' } });

// ═════════ P017 (B10): sayfadaki güneş büyür, cennetin ışığına açılır ═════════
function cen_b10(t) {
  const { tx, ox, tone } = GR, s0 = S('B10'), u = E.io2(cen_u(t, s0 - .2, Se('B10') + .9)), v = E.io2(cen_u(t, s0 + .9, Se('B10') + 1.6));
  const L = { x: lerp(863, 960, u), y: lerp(184, 200, u) }, R = lerp(128, 2000, u);
  // güneş çizimi büyür: halkası açılıp göğün eş merkezli taramasına dönüşür
  GR.fill(new Path2D('M-500 -500 H2500 V1600 H-500 Z'), tone(lerp(.975, .74, E.sine(cen_u(u, .1, .8)))), { type: 'rad', cx: L.x, cy: L.y, id: 1 });
  const g = tx.createRadialGradient(L.x, L.y, R * .3, L.x, L.y, R);
  g.addColorStop(0, tone(1)); g.addColorStop(.25, tone(lerp(.4, .97, u))); g.addColorStop(.6, tone(lerp(.72, .86, u))); g.addColorStop(1, tone(lerp(.975, .76, u)));
  const D = new Path2D(); D.arc(L.x, L.y, R, 0, TAU); GR.fill(D, g, { type: 'rad', cx: L.x, cy: L.y, id: 1 });
  { const ka = E.sine(cen_u(u, .3, .9)); if (ka > 0) { tx.save(); tx.globalCompositeOperation = 'lighten'; tx.fillStyle = tone(1);
    for (const [an, wd] of [[PI * .68, .05], [PI * .5, .035], [PI * .3, .045]]) { const P = new Path2D(), Lk = 1300 * ka, n = 12, A = [], B = [];
      for (let i = 0; i <= n; i++) { const q = i / n, r = 40 + Lk * q, w = wd * (q < .35 ? Math.pow(q / .35, .6) : Math.pow(1 - (q - .35) / .65, 1.4)); A.push([L.x + Math.cos(an - w) * r, L.y + Math.sin(an - w) * r]); B.push([L.x + Math.cos(an + w) * r, L.y + Math.sin(an + w) * r]); }
      poly(P, [[L.x, L.y], ...A, ...B.reverse()], true); tx.fill(P); } tx.restore(); } }
  if (u > .6) { const k = (u - .6) / .4; tx.save(); tx.globalAlpha = k; const g2 = tx.createRadialGradient(L.x, L.y, R * .5, L.x, L.y, R * 1.2); g2.addColorStop(0, 'rgba(0,0,0,0)'); g2.addColorStop(1, tone(.72)); tx.fillStyle = g2; tx.fillRect(-500, -500, W + 1000, H + 1000); tx.restore(); }
  // çizilmiş halka ve ışınlar: büyüdükçe incelir, söner
  const fa = 1 - E.sine(cen_u(u, .25, .7));
  if (fa > 0) { ox.save(); ox.globalAlpha = fa; ox.strokeStyle = GR.inkCol; ox.lineCap = 'round'; ox.lineWidth = 3.4; const r0 = 30 * (1 + 9 * u);
    ox.beginPath(); ox.arc(L.x, L.y, r0, 0, TAU); ox.stroke();
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU + .1, l = (i % 2 ? 16 : 26) * (1 + 9 * u); ox.beginPath(); ox.moveTo(L.x + Math.cos(a) * r0 * 1.33, L.y + Math.sin(a) * r0 * 1.33); ox.lineTo(L.x + Math.cos(a) * (r0 * 1.33 + l), L.y + Math.sin(a) * (r0 * 1.33 + l)); ox.stroke(); }
    ox.restore(); }
  // bulut terasları alttan yükselir
  if (v > 0) {
    const dy = (1 - v) * 420;
    cen_bulut({ x: 380, y: 860 + dy, w: 1000, h: 170, seed: 61, L, sh: .9, n: 7, len: 2 });
    cen_bulut({ x: 1560, y: 840 + dy * 1.2, w: 1000, h: 160, seed: 62, L, sh: .9, n: 7, len: 2 });
    cen_bulut({ x: 960, y: 1130 + dy * .7, w: 2400, h: 130, seed: 63, L, sh: 1, n: 12, len: 1.6, by: -.2 });
  }
}
plan('P017', (ctx, st) => levha(ctx, null, () => cen_b10(st.t), [.975, 0, 1]), { tr: { type: 'paper', dur: 1.0 } });

// ═════════ P018 (C01): bölüm kartı "IŞIK TAŞIYAN": ışık sütunları, bulut terasları ═════════
function cen_c01(t) {
  const L = { x: 960, y: 200 };
  cen_gok(L, { r0: 360, r1: 1500, v: .7, mid: .9, kama: [{ a: PI * .62, w: .05, len: 1100, at: .5 }, { a: PI * .5, w: .04, len: 1000, at: .5 }, { a: PI * .38, w: .05, len: 1100, at: .5 }] });
  cen_bulut({ x: 260, y: 760, w: 900, h: 180, seed: 71, L, sh: .95, n: 6, len: 2.6, drift: Math.sin(t * .1) * 6 });
  cen_bulut({ x: 1680, y: 740, w: 900, h: 170, seed: 72, L, sh: .95, n: 6, len: 2.6, drift: -Math.sin(t * .1) * 6 });
  cen_bulut({ x: 960, y: 1080, w: 2600, h: 140, seed: 73, L, sh: 1, n: 12, len: 1.4, by: -.2 });
}
// açık kart: ince mürekkep çizgi + başlık + soru (kâğıt zeminde mürekkep harf)
function cen_kart(ctx, title, soru, lt, d) {
  if (NOTEXT) return;
  const a = clamp(lt / .6) * clamp((d - lt) / .6); if (a <= 0) return;
  const x = 960, y = 400, px = 92;
  ctx.save(); ctx.globalAlpha *= E.sine(a);
  const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 1); g.addColorStop(0, `rgba(${GR.PAPER},.95)`); g.addColorStop(.62, `rgba(${GR.PAPER},.9)`); g.addColorStop(1, `rgba(${GR.PAPER},0)`);
  ctx.save(); ctx.translate(x, y + 40); ctx.scale(780, 250); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 1, 0, TAU); ctx.fill(); ctx.restore();
  const lw = 250 * E.out3(clamp(lt / 1.1)); ctx.strokeStyle = INK_CSS; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x - lw, y - px * .82); ctx.lineTo(x + lw, y - px * .82); ctx.stroke();
  txt(ctx, title, x, y, { px, ls: 10, col: INK_CSS });
  ctx.font = FONT.alinti(54); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = INK_CSS; ctx.globalAlpha *= clamp((lt - .5) / .6);
  wrapLines(ctx, soru, 1200).forEach((l, i) => ctx.fillText(l, x, y + px * .98 + i * 62));
  ctx.restore();
}
plan('P018', (ctx, st) => levha(ctx, null, () => cen_c01(st.t), [.8, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => cen_kart(ctx, 'IŞIK TAŞIYAN', 'Her şeye sahip olan biri, neden başkaldırır?', st.lt, st.end - st.at) });

// ═════════ P020 (C03): profil, alnının üstünde sabah yıldızı; "LUCIFER · ışık taşıyan" ═════════
function cen_c03(t) {
  const L = { x: 1900, y: 60 }, tL = Wd('C03', 'lüsifer'), sa = .35 + .65 * E.out3(cen_u(t, tL - .3, tL + .9));
  cen_gok(L, { r0: 160, a: .8, v: .66, mid: .86, kama: [{ a: PI * .78, w: .035, len: 1400 }] });
  cen_bulut({ x: 1500, y: 960, w: 1300, h: 150, seed: 81, L, sh: .95, n: 8, len: 2 });
  const J = cen_basmelek({ x: 900, y: 1070, h: 140, wingSpan: 4.4 * 140, facing: -1, L, t, lum: 1, head: .28, twist: .22, armN: [.05, .3], armF: [-.1, .4], spear: false, open: -.3, lift: .1, wingRot: .1, cloak: .4, shade: .1, legs: false });
  const hd = J.hd; cen_yildiz(hd[0] - 30, hd[1] - 1.5 * 140 + Math.sin(t * .8) * 2, 30, sa);
  cen_bulut({ x: 300, y: 1110, w: 1300, h: 120, seed: 82, L, sh: 1, n: 8, len: 1.4, by: -.2 });
}
plan('P020', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 930, cy: 520, z: 1.06 }, st.p, E.io2), () => cen_c03(st.t), [.8, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => {
    const t0 = Wd('C03', 'lüsifer') - .1, a = E.sine(clamp((st.t - t0) / .6)) * clamp((st.end - st.t) / .5);
    cen_yazi(ctx, 'LUCIFER · ışık taşıyan', 1340, 200, a, { px: 58, ls: 5 }); } });

// ═════════ P021 (C04): iki ışık (Tanrı ve Oğul yalnız ışıktır); melekler saray selamıyla eğilir; başmelek dik durur ═════════
function cen_c04(t) {
  const { tx, tone } = GR, tO = Wd('C04', 'oğulu'), tD = Wd('C04', 'diz'), L = { x: 560, y: 120 };
  const o2 = E.io2(cen_u(t, tO - .4, tO + 1.4)), dl = E.io2(cen_u(t, tD - .5, Se('C04')));
  cen_gok(L, { r0: 110, r1: 1500, v: .6, mid: .82, kama: [{ a: PI * .7, w: .04, len: 1150 * (.6 + .4 * o2) }, { a: PI * .4, w: .035, len: 1000 * (.6 + .4 * o2) }] });
  // ikinci ışık (Oğul): figürsüz, yalnız kâğıt parıltı; birincinin yanında, daha küçük
  if (o2 > 0) cen_isik(1060, 210, 44 * o2, o2);
  // ışınlar açılır: kama boyu ilk sözle büyür (cen_gok içinde sabit; ek ince kama)
  cen_bulut({ x: 960, y: 760, w: 2200, h: 110, seed: 91, L, sh: .9, n: 14, len: 1.2, by: .2 });
  // dağınık gruplar: Batı saray selamı (tek diz, baş eğik); her grup kendi zamanında eğilir
  const G = [[200, 860, 30, 4, 1], [560, 800, 22, 5, 1], [820, 780, 18, 5, -1], [1130, 830, 26, 4, -1], [420, 1010, 44, 3, 1], [960, 1000, 40, 3, -1]];
  G.forEach(([x0, y0, h, n, f], gi) => { const q = rng(gi * 13 + 5);
    for (let i = 0; i < n; i++) { const x = x0 + (i - n / 2) * h * 2.3 + (q() - .5) * h * 1.2, y = y0 + (q() - .5) * h * .8, b = E.io2(cen_u(dl, gi * .08 + q() * .1, gi * .08 + q() * .1 + .45));
      let lx = L.x - x, ly = L.y - (y - 5 * h); const l = Math.hypot(lx, ly); cen_melek({ x, y, h: h * (.92 + q() * .16), f, lx: lx / l, ly: ly / l, bow: b, spear: null, seed: gi * 17 + i, wing: .8 }); } });
  cen_bulut({ x: 1500, y: 930, w: 900, h: 120, seed: 92, L, sh: .95, n: 7, len: 1.6, by: .1 });
  // başmelek: sağ kenarda dik; gölgesi bulut zemininde uzar
  const fx = 1610, fy = 920, sl = lerp(140, 520, dl);
  { const P = new Path2D(); P.moveTo(fx - 40, fy - 4); P.quadraticCurveTo(fx + sl * .5, fy + 10, fx + sl, fy + 30); P.lineTo(fx + sl - 20, fy + 52); P.quadraticCurveTo(fx + sl * .45, fy + 40, fx + 30, fy + 14); P.closePath();
    tx.fillStyle = tone(.04); tx.fill(P); GR.px.fillStyle = GR.hatch({ th: .05, id: 9 }); GR.px.fill(P); }
  cen_basmelek({ x: fx, y: fy - 3.95 * 66, h: 66, facing: -1, L, t, lum: .92, head: .1, twist: .3, armN: [-.05, .2], armF: [.2, 1.3], shade: lerp(.13, .2, dl), wingRot: -.1, fold: .4 });
  cen_bulut({ x: 900, y: 1130, w: 2600, h: 120, seed: 93, L, sh: 1, n: 12, len: 1.4, by: -.2 });
}
plan('P021', (ctx, st) => levha(ctx, null, () => cen_c04(st.t), [.8, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// ═════════ P022 (C05): cennetin alacakaranlığı; başmelek yardımcısının kulağına eğilir; uzakta kuzeye yürüyen saflar, tepede saray ═════════
function cen_c05(t) {
  const L = { x: 1640, y: 330 }, s0 = S('C05');
  cen_gok(L, { r0: 70, a: .55, v: .5, mid: .7, dark: .55 });
  // tepede saray (kuzey)
  cen_bulut({ x: 1640, y: 470, w: 520, h: 110, seed: 101, L, sh: .9, n: 5, len: 2.4, cuts: .4 });
  cen_saray(1640, 405, 170, 1, .95);
  // kuzeye yürüyen saflar: sağa doğru küçülür
  const mv = (t - s0) * 9;
  cen_bulut({ x: 1250, y: 640, w: 1500, h: 70, seed: 102, L, sh: .9, n: 10, len: 2.2, cuts: 0 });
  cen_saflar([{ y: 600, h: 8, x0: 760 + mv, x1: 1500 + mv, n: 30, facing: 1, seed: 21, sh: .14, v: .9 }], { t, L });
  cen_saflar([{ y: 680, h: 12, x0: 640 + mv * 1.3, x1: 1560 + mv * 1.3, n: 26, facing: 1, seed: 22, v: .93 }], { t, L });
  cen_bulut({ x: 1300, y: 760, w: 1700, h: 90, seed: 103, L, sh: .95, n: 12, len: 2.2 });
  // ön sol: iki figür; başmelek arkadan yardımcısının kulağına eğilir
  cen_bulut({ x: 420, y: 960, w: 1100, h: 160, seed: 104, L, sh: .95, n: 7, len: 1.6 });
  cen_basmelek({ x: 600, y: 600, h: 70, facing: 1, L, t, lum: .86, head: -.05, twist: .35, armN: [.1, .3], armF: [.3, .4], spear: false, wingRot: .1, fold: .8, seed: 9, cloak: .3 });
  cen_basmelek({ x: 450, y: 580 + Math.sin(t * .5) * 2, h: 72, facing: 1, L, t, lum: .88, head: -.32, lean: .22, twist: .3, armN: [.35, .4], armF: [.5, .5], spear: false, fold: .7, wingRot: .15, cloak: .8 });
  cen_bulut({ x: 700, y: 1120, w: 2400, h: 120, seed: 105, L, sh: 1, n: 12, len: 1.4, by: -.2 });
}
plan('P022', (ctx, st) => levha(ctx, null, () => cen_c05(st.t), [.6, 0, 1]), { tr: { type: 'fade', dur: 1.0 } });

// ═════════ P023 (C06): yüksek tepede ordusuna hitap; kolu havada; "özgürlük" ═════════
function cen_c06(t) {
  const L = { x: 1500, y: 140 }, tK = Wd('C06', 'konuşur'), up = E.out3(cen_u(t, tK - .2, tK + .9));
  cen_gok(L, { r0: 110, a: .75, v: .56, mid: .78, dark: .3, kama: [{ a: PI * .75, w: .035, len: 1300 }] });
  // tepe: yükselen bulut kayası; üstünde figür
  cen_bulut({ x: 720, y: 660, w: 820, h: 170, seed: 111, L, sh: .85, n: 7, len: 2.2, cuts: .7 });
  cen_basmelek({ x: 720, y: 640 - 3.95 * 58 + 10, h: 58, facing: 1, L, t, lum: .85, head: .2 + .1 * up, twist: .35, armN: [lerp(-.1, 2.15, up), lerp(.3, .35, up)], armF: [.1, .5], wingRot: .2, fold: .9, spear: false });
  // aşağıda ordu: başlar ve mızraklar, tepeye dönük
  cen_bulut({ x: 1400, y: 760, w: 1300, h: 70, seed: 112, L, sh: .9, n: 12, len: 4, cuts: 0, base: false });
  cen_saflar([{ y: 820, h: 11, x0: 1000, x1: 1990, n: 30, facing: -1, seed: 31, dy: .6 }, { y: 930, h: 17, x0: 1050, x1: 1990, n: 18, facing: -1, seed: 32, dy: .5 }], { t, L });
  cen_saflar([{ y: 960, h: 16, x0: -40, x1: 380, n: 8, facing: 1, seed: 34, dy: .5 }], { t, L });
  cen_bulut({ x: 900, y: 1110, w: 2600, h: 130, seed: 113, L, sh: 1, n: 12, len: 1.4, by: -.2 });
}
plan('P023', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 860, cy: 500, z: 1.12 }, st.p, E.io2), () => cen_c06(st.t), [.7, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => {
    const t0 = Wd('C06', 'özgürlük') - .1, a = E.sine(clamp((st.t - t0) / .7)) * clamp((st.end - st.t) / .4);
    cen_yazi(ctx, 'özgürlük', 1340, 300, a, { px: 104, font: FONT.alinti(104), ls: 2 }); } });

// ═════════ P024 (C07): alttan bakış: dinleyen saflar, mızrak ormanı; mızraklar tek tek kalkar ═════════
function cen_c07(t) {
  const L = { x: 1380, y: 70 }, t0 = Wd('C07', 'biz'), t1 = Wd('C07', 'koyabilir');
  cen_gok(L, { r0: 120, a: .8, v: .58, mid: .82, dark: .25, kama: [{ a: PI * .72, w: .035, len: 1200 }, { a: PI * .55, w: .03, len: 900 }] });
  // mızrak açısı: her mızrak kendi anında yatıktan dikeye
  const ang = (i, x, sd) => { const q = hash(i * 7.31 + sd), tt = lerp(t0, t1, q); return lerp(-.95, 0, E.out3(cen_u(t, tt, tt + .8))); };
  cen_bulut({ x: 960, y: 760, w: 2400, h: 70, seed: 121, L, sh: .95, n: 16, len: 3, cuts: 0, base: false });
  cen_saflar([{ y: 790, h: 13, x0: -20, x1: 1960, n: 40, facing: 1, seed: 41, dy: .5, spearAng: (i, x) => ang(i, x, 1) }], { t, L });
  cen_saflar([{ y: 930, h: 22, x0: -40, x1: 1980, n: 22, facing: 1, seed: 42, dy: .4, spearAng: (i, x) => ang(i, x, 2) }], { t, L });
  cen_saflar([{ y: 1200, h: 42, x0: -60, x1: 2000, n: 10, facing: 1, seed: 43, dy: .3, spearAng: (i, x) => ang(i, x, 3) }], { t, L });
}
plan('P024', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 560, z: 1.04 }, { cx: 960, cy: 520, z: 1.04 }, st.p, E.io2), () => cen_c07(st.t), [.7, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// ═════════ P025 (C08): gökte ışık noktaları: üçte biri ayrılıp onun peşine kayar ═════════
function cen_c08(t) {
  const { tx, tone } = GR, L = { x: 1560, y: 230 }, tY = Wd('C08', 'yalanlarıyla'), tU = Wd('C08', 'üçte'), s0 = S('C08');
  const go = E.io2(cen_u(t, tY, Se('C08') + 1.2)), lead = E.io2(cen_u(t, s0, Se('C08') + 1.5));
  cen_gok(L, { r0: 120, a: .85, v: .5, mid: .8, dark: .35 });
  cen_bulut({ x: 1500, y: 1060, w: 1500, h: 120, seed: 131, L, sh: 1, n: 10, len: 1.4 });
  // önder: sabah yıldızı, sola ve aşağı (ışıktan uzağa) kayar
  const lx = lerp(1100, 360, lead), ly = lerp(520, 640, lead);
  const q = rng(77), N = 130;
  for (let i = 0; i < N; i++) {
    const a = q() * TAU, r = Math.sqrt(q()) * 1, x0 = 1250 + Math.cos(a) * r * 560, y0 = 470 + Math.sin(a) * r * 300, fol = (i % 3) === 0, ph = q(), sz = 5 + q() * 4;
    let x = x0, y = y0;
    if (fol) { const k = E.io2(clamp(go * 1.25 - ph * .25)); x = lerp(x0, lx - 60 - (x0 - 1250) * .45 + 120, k); y = lerp(y0, ly + (y0 - 470) * .55, k); }
    const K = new Path2D(); K.arc(x, y, sz * 1.5 + 2, 0, TAU); tx.fillStyle = tone(.05); tx.fill(K);
    const D = new Path2D(); poly(D, [[x, y - sz * 2], [x + sz * .45, y - sz * .45], [x + sz * 2, y], [x + sz * .45, y + sz * .45], [x, y + sz * 2], [x - sz * .45, y + sz * .45], [x - sz * 2, y], [x - sz * .45, y - sz * .45]], true); tx.fillStyle = tone(1); tx.fill(D);
  }
  cen_yildiz(lx, ly, 22, 1);
}
plan('P025', (ctx, st) => levha(ctx, null, () => cen_c08(st.t), [.6, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => { const t0 = Wd('C08', 'üçte') - .1; etiket(ctx, 'üçte biri', 560, 300, st.t - t0, st.end - t0 + .2, { px: 48, ls: 4 }); } });

// ═════════ P027 (C10): sönük kalabalıkta tek parlak figür ayağa kalkar: Abdiel ═════════
function cen_c10(t) {
  const tK = Wd('C10', 'kalkar'), up = E.io2(cen_u(t, tK - .6, tK + .7)), gl = E.io2(cen_u(t, tK - .3, Se('C10') + .5));
  const AX = 1000, L = { x: AX, y: 520 };
  cen_gok(L, { r0: lerp(40, 150, gl), a: .3 + .7 * gl, v: .44, mid: lerp(.6, .82, gl), dark: .6 });
  // sönük kalabalık: hafif taralı gövdeler (ton .62); uzak sıralar önce
  const crowd = (y, h, n, sd, v) => cen_saflar([{ y, h, x0: -40, x1: 1980, n, facing: 1, seed: sd, v: v * .2, sh: .1, spear: false, dy: .4, wing: .5 }], { t, L });
  cen_bulut({ x: 960, y: 640, w: 2400, h: 60, seed: 141, L, sh: .9, n: 16, len: 4, cuts: 0, base: false });
  crowd(700, 12, 36, 51, .66); crowd(800, 17, 26, 52, .64);
  // Abdiel: diz çökmüş hâlden kalkar; ışık onda toplanır
  let lx = 0, ly = -1; cen_melek({ x: AX, y: 900, h: 42, f: -1, lx: .2, ly: -.98, bow: 1 - up, spear: null, seed: 5, v: .99, sh: .16 });
  crowd(960, 26, 16, 53, .6); crowd(1130, 38, 11, 54, .58);
}
plan('P027', (ctx, st) => levha(ctx, null, () => cen_c10(st.t), [.6, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => { const t0 = Wd('C10', 'abdiyeldir') - .1; etiket(ctx, 'ABDIEL', 1000, 150, st.t - t0, st.end - t0 + .3, { px: 48 }); } });

// ═════════ P028 (C11): Abdiel açılan safların arasından tek başına yürüyüp gider (yandan kaydırma) ═════════
function cen_c11(t) {
  const s0 = S('C11'), tY = Wd('C11', 'yürüyüp'), w = cen_u(t, s0, Se('C11') + 1), AX = lerp(560, 1900, w), L = { x: AX + 80, y: 300 };
  cen_gok(L, { r0: 90, a: .7, v: .46, mid: .74, dark: .55 });
  cen_bulut({ x: 1200, y: 660, w: 2800, h: 60, seed: 151, L, sh: .9, n: 20, len: 4, cuts: 0, base: false });
  // arka saf: ona dönük, sönük; geçtiği yerde hafif geri çekilir
  cen_saflar([{ y: 760, h: 16, x0: 0, x1: 2400, n: 40, facing: -1, seed: 61, v: .14, sh: .1, spear: false, dy: .3 }], { t, L });
  // Abdiel: yürüyüş (bacak salınımı), dik baş
  const ph = (t - s0) * 3.4, sw = Math.sin(ph) * .38;
  cen_basmelek({ x: AX, y: 900 - 3.95 * 40 + Math.abs(Math.cos(ph)) * -3, h: 40, facing: 1, L: { x: AX + 400, y: 100 }, t, lum: 1, head: .12, twist: .55, armN: [-sw * .6, .2], armF: [sw * .6, .2], legN: [sw, -.1 - .2 * Math.max(0, -Math.sin(ph))], legF: [-sw, -.1 - .2 * Math.max(0, Math.sin(ph))], spear: false, fold: 1, wingRot: .3, cloak: .5 });
  // ön saf: kadrajı kesen sönük bedenler, aralanmış
  const R = rng(62);
  for (let i = 0; i < 12; i++) { const x = -100 + i * 230 + (R() - .5) * 60, gap = Math.exp(-Math.pow((x - AX) / 260, 2)) * 70; cen_melek({ x: x + Math.sign(x - AX) * gap, y: 1180 + (R() - .5) * 30, h: 46, f: x < AX ? 1 : -1, lx: .3, ly: -.95, spear: null, v: .12, sh: .12, seed: 70 + i, wing: .6 }); }
}
plan('P028', (ctx, st) => levha(ctx, camLerp({ cx: 760, cy: 560, z: 1.05 }, { cx: 1160, cy: 560, z: 1.05 }, st.p, E.sine), () => cen_c11(st.t), [.6, 0, 1]),
  { tr: { type: 'fade', dur: .8 }, over: (ctx, st) => { const t0 = Wd('C11', 'binlerce') - .2; quote(ctx, '“binlerce hainin arasında sadık kalan tek kişi”', 960, 190, st.t - t0, { px: 66, per: .45 }); } });
