// gol grubu (GOL: yanan göl, KIY: yanan kıyı): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
// u(a, b): t'nin [a, b] aralığındaki konumu (0..1)
const gol_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));
// ekran koordinatında çizim (kamera dönüşümü yok): GR.tx'e; fn içinden çağrılır
function gol_ekran(fn) { const T = GR.tx; T.save(); T.setTransform(RS, 0, 0, RS, 0, 0); fn(T); T.restore(); }
// sivri uçlu dolgu çizgi (ton katmanına); pts dünya noktaları, w en kalın yer, v ton
function gol_vurus(c, pts, w, v = 1, uc = .55) {
  const n = 18, S = [], A = [], B = [], m = pts.length;
  const cr = (p0, p1, p2, p3, t) => { const t2 = t * t, t3 = t2 * t; return [0, 1].map(j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)); };
  for (let i = 0; i <= n; i++) { const u = i / n * (m - 1), s = Math.min(m - 2, Math.floor(u)); S.push(cr(pts[Math.max(0, s - 1)], pts[s], pts[s + 1], pts[Math.min(m - 1, s + 2)], u - s)); }
  for (let i = 0; i <= n; i++) {
    const a = S[Math.max(0, i - 1)], b = S[Math.min(n, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
    const ww = Math.max(1.2, w * .5 * Math.pow(Math.sin(PI * (.04 + .92 * i / n)), uc));
    A.push([S[i][0] - dy / L * ww, S[i][1] + dx / L * ww]); B.push([S[i][0] + dy / L * ww, S[i][1] - dx / L * ww]);
  }
  c.fillStyle = GR.tone(v); c.beginPath(); poly(c, [...A, ...B.reverse()], true); c.fill();
}

// ═════════ P004 (A04): karanlıkta açılan gözler → yanan göl ═════════
// İki göz: siyah karede yalnız iki ince ışık (kaşın gölgesinde, iç uçları hafif aşağıda: ağır, mağrur bakış). a: açıklık 0..1
function gol_gozler(T, a, al = 1) {
  if (a <= 0 || al <= 0) return;
  T.save(); baseT(T); T.globalAlpha = al; {
    for (const sd of [-1, 1]) {
      const cx = 960 + sd * 152, cy = 528, L = 150, ang = sd * .1;   // iç uç (merkeze yakın) aşağıda
      const c = Math.cos(ang), s = Math.sin(ang), P = (x, y) => [cx + x * c - y * s, cy + x * s + y * c];
      const th = 15 * a, n = 20, up = [], dn = [];
      for (let i = 0; i <= n; i++) {
        const u = i / n, x = (u - .5) * L, e = Math.pow(Math.sin(PI * u), .7);
        const k = sd < 0 ? u : 1 - u;                                 // dış uç biraz daha açık (badem)
        up.push(P(x, -th * .35 * e * (.8 + .4 * k)));               // üst kapak düz ve ağır
        dn.push(P(x, th * .65 * e * (.7 + .5 * k)));
      }
      T.fillStyle = PAPER_CSS; T.beginPath(); poly(T, [...up, ...dn.reverse()], true); T.fill();
    }
  } T.restore();
}
plan('P004', (ctx, st) => {
  const t = st.t, tG = Wd('A04', 'gözlerini'), tR = Wd('A04', 'yanan') - .3, tD = Wd('A04', 'dokuz');
  const open = E.out3(gol_u(t, tG, tG + .9)) * (1 - .75 * Math.sin(PI * gol_u(t, tG + 1.55, tG + 1.85)));   // açılır; bir kez ağır kırpar
  const rv = E.io2(gol_u(t, tR, tR + 1.8));                                // karanlıktan açılış
  const cam = camLerp({ cx: 878, cy: 520, z: 1.25 }, { cx: 960, cy: 540, z: 1 }, gol_u(t, tR, st.end), E.io2);
  if (rv > 0) levha(ctx, cam, () => cizGol(t, { head: lerp(.08, .5, E.io2(gol_u(t, tD, tD + 1.7))), sway: .025 }));
  else { ctx.save(); baseT(ctx); ctx.fillStyle = INK_CSS; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  // karanlıktan açılış: baskının üstüne mürekkep örtü (geçiş gibi), gözler örtünün üstünde
  if (rv < 1) { ctx.save(); baseT(ctx); ctx.globalAlpha = 1 - rv; ctx.fillStyle = INK_CSS; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  gol_gozler(ctx, open, 1 - E.sine(gol_u(t, tR, tR + .7)));
}, { tr: { type: 'cut' },
  over: (ctx, st) => { const t0 = Wd('A04', 'görünür'); etiket(ctx, 'görünür karanlık', 360, 150, st.t - t0, st.end - t0 + .3, { px: 42, ls: 4 }); } });

// ═════════ P005 (A04@zincirlerle): zincir yakın planı ═════════
// Yakın ölçekte çizilmiş ayrı kadraj: bilekten göle inen büyük halkalar, demir bilezik, su çizgisi.
function cizZincir(t) {
  const { tx, tone, fill } = GR, WY = 700;
  // gök ve ufuk: yakın planda ufuk su çizgisine iner; parıltı bileğin arkasında (odak)
  let g = tx.createLinearGradient(0, 0, 0, WY); g.addColorStop(0, tone(.02)); g.addColorStop(.62, tone(.05)); g.addColorStop(1, tone(.3));
  tx.fillStyle = g; tx.fillRect(-300, -300, W + 600, WY + 300);
  PR.glow(1080, WY - 20, 120, 620, 1, .95);
  PR.cloud({ x: 200, y: 150, w: 1000, h: 300, seed: 41, lit: [.7, .7], base: .02, hi: .8, core: .02, n: 4, drift: Math.sin(t * .1) * 8 });
  PR.cloud({ x: 1800, y: 110, w: 900, h: 260, seed: 19, lit: [-.7, .7], base: .02, hi: .75, core: .02, n: 3, drift: Math.sin(t * .08) * 8 });
  PR.lake(WY, H + 120, t, { tone: [.22, .02], crests: 18, p0: 10.5, refl: [{ x: 1080, w: 520, v: .9, len: 300, rows: 18 }, { x: 1560, w: 180, v: .5, len: 160 }] });
  PR.flameBank(-60, W + 60, WY + 2, 40, t, 3, { env: f => .25 + .75 * Math.pow(Math.sin(f * PI), 2) });
  // ön kol: yukarıdan suya inen kalın, kaslı koyu kütle (dirsek kadraj dışında); ışık arkadan sağ üstten
  const br = Math.sin(t * .6) * 3, X = x => x, Y = y => y + br * (1 - y / 900);
  tx.save(); { const C = new Path2D(); C.rect(-400, -400, W + 800, WY + 400 + 6); tx.clip(C); }   // kol ve bilezik su çizgisinde biter
  const arm = new Path2D();
  spline(arm, [[260, -60], [500, -60], [610, 110], [700, 290], [762, 450], [795, 600], [805, 760], [565, 760], [560, 610], [520, 480], [440, 330], [330, 150]].map(([x, y]) => [X(x), Y(y)]), true, .75);
  fill(arm, tone(.02), { th: .2, id: 5 });
  tx.save(); tx.clip(arm);
  gol_vurus(tx, [[500, -40], [610, 130], [700, 310], [758, 470]].map(([x, y]) => [x, Y(y)]), 11, .97);   // kenar ışığı: arka (sağ) kenar
  tx.restore();
  PR.cuts([[560, 60], [650, 210], [720, 350], [760, 470]].map(([x, y]) => [x, Y(y)]), [-.9, .45], { len: [20, 120], gap: [40, 110], w: 6, seed: 9, clip: arm, bend: -.25 });
  // demir bilezik: bileği saran kalın bant (silindir): üst kenar ışıklı, alt kenar koyu; üç perçin
  const cy0 = 520, cy1 = 640, cf = new Path2D();
  spline(cf, [[536, Y(cy0) + 10], [665, Y(cy0) - 14], [800, Y(cy0) + 2], [812, Y(cy1) - 6], [670, Y(cy1) + 18], [544, Y(cy1) + 2]], true, .5);
  fill(cf, tone(.03), { th: 0, id: 9 });
  tx.save(); tx.clip(cf);
  gol_vurus(tx, [[560, Y(cy0) + 12], [670, Y(cy0) - 4], [790, Y(cy0) + 8]], 13, .96);
  gol_vurus(tx, [[690, Y(cy0) + 40], [760, Y(cy0) + 48], [800, Y(cy0) + 70]], 7, .9);
  tx.restore();
  for (const x of [600, 670, 740]) { const y = Y(cy0 + 62) + (x - 670) * (x - 670) * .0012; tx.fillStyle = tone(.92); tx.beginPath(); tx.arc(x, y, 7.5, 0, TAU); tx.fill(); }
  tx.restore();
  // zincir: bilezikten sağa ve aşağı, beş büyük halka; suya dalar
  const sw = Math.sin(t * .5) * 5;
  tx.save(); { const C = new Path2D(); C.rect(-400, -400, W + 800, WY + 400 + 4); tx.clip(C); }
  PR.chain(808, Y(600), 1500 + sw, 800, 108, { sag: 10, v: .95, lit: [.4, -.9] });
  tx.restore();
  // halkanın ve kolun suya girdiği yerde açık su halkaları (yavaşça genişler)
  tx.save(); tx.globalCompositeOperation = 'lighter';
  for (const [cx, ph] of [[680, 0], [1236 + sw * .5, .5]]) for (let k = 0; k < 2; k++) { const f = ((t * .3 + k / 2 + ph) % 1), rx = 110 + 150 * f, a = .5 * (1 - f); tx.strokeStyle = `rgba(255,255,255,${a})`; tx.lineWidth = 5; tx.beginPath(); tx.ellipse(cx, WY + 8, rx, rx * .1, 0, 0, TAU); tx.stroke(); }
  tx.restore();
}
plan('P005', (ctx, st) => {
  const cam = camLerp({ cx: 900, cy: 520, z: 1.06 }, { cx: 990, cy: 520, z: 1.06 }, st.p, E.sine);
  levha(ctx, cam, () => cizZincir(st.t));
}, { tr: { type: 'cut' } });

// ═════════ D–E: göle dönüş, "Cehennemde Kral" bölümü ═════════
// Beelzebub: Şeytan'ın sağında, gölde yüzüstü yatan ikinci düşmüş melek (sırtı, başı ve tek kanadı suyun üstünde)
function gol_beel(t, o = {}) {
  const { tx, tone, fill } = GR, lf = o.lift || 0, br = Math.sin(t * .5 + 1) * 1.6;
  const k = 1.45, X0 = 1330, WY = 884, M = ([x, y]) => [X0 + (x - 1300) * k, WY + (y - 800) * k];   // çizim 800 su çizgisinde kurulur, öne (yakına) taşınır
  // arkasında alçak bir alev sırası: baş ve omuz ona karşı siluet okunur
  PR.flameBank(960, 1660, WY - 64, 170, t, 23, { band: false, n: 7, wr: .55, solidBelow: 500, speed: .5, strip: .35, frags: false, env: f => .35 + .65 * Math.sin(f * PI) });
  const hy = -10 * lf + br;                                  // baş biraz kalkar (kıpırdanış)
  // kanat: sırttan yükselip sağa sarkan, ucu suya giren kırık kanat (suyun altı çizilmez)
  GR.save(); { const C = new Path2D(); C.rect(-4000, -4000, 12000, 4000 + WY); for (const c of [GR.tx, GR.px, GR.ox]) c.clip(C); }
  { const q = M([1262, 772 + br * .5]); GR.frame(q[0], q[1], -.1, 1, .72 * k); }
  KN.feathered({ span: 520, open: .62, lift: .32, droop: .85, ruin: .7, dark: .92, rim: .7, t, seed: 44, root: .1, lit: [-.6, -.8] });
  GR.unframe(); GR.restore();
  // yüzüstü beden: suyun üstünde yalnız baş, omuz ve sırt; öne uzanmış kol suyun yüzünde
  const B = [[1070, 806], [1074, 795], [1100, 789], [1128, 788 + hy * .3], [1116, 774 + hy], [1114, 760 + hy], [1124, 746 + hy], [1146, 740 + hy], [1168, 746 + hy],
    [1186, 758 + hy * .6], [1214, 755], [1262, 757], [1330, 764], [1410, 776], [1480, 792], [1520, 806]].map(M);
  const P = new Path2D(); spline(P, B, true, .6);
  fill(P, tone(.02), { th: 0, id: 5 });
  tx.save(); tx.clip(P);
  gol_vurus(tx, [[1118, 768 + hy], [1121, 752 + hy], [1140, 745 + hy], [1160, 748 + hy]].map(M), 10, .96);       // başın ışık yanı
  gol_vurus(tx, [[1196, 762], [1250, 759], [1330, 766], [1420, 779]].map(M), 9, .92);                             // omuz ve sırt sırtı
  tx.restore();
}
// iki figürlü göl: Şeytan solda (bel hizası), Beelzebub sağda; ön alevler yalnız Şeytan'ın solunda
function gol_ikili(t, o) {
  return cizGol(t, Object.assign({ fx: 760, front: false, mid: () => {
    gol_beel(t, { lift: o.blift || 0 });
    PR.flameBank(760 - 340, 760 - 70, 840, 150, t, 7, { n: 4, env: f => .45 + .55 * (1 - f), wr: .6, solidBelow: 500, speed: .5, strip: .5, frags: false });
    const RK = [[-20, 556], [38, 566], [72, 584], [96, 612], [132, 640], [170, 648], [206, 664], [214, 700], [238, 732], [272, 748], [300, 772], [304, 818], [320, 862], [352, 884], [384, 916], [378, 968], [398, 1010], [404, H + 20], [-20, H + 20]];
    const RP = PR.rock(RK, { lit: [.85, -.45], hi: .05, mid: .03, lo: .02, seed: 2, th: -.9, rim: 6, facets: 10 });
    PR.cuts(RK.slice(0, 11), [-.5, .87], { len: [16, 190], gap: [44, 130], w: 6, seed: 5, clip: RP, bend: -.35 });
  } }, o));
}
plan('P039', (ctx, st) => {
  const cam = camLerp({ cx: 1010, cy: 560, z: 1.1 }, { cx: 930, cy: 560, z: 1.1 }, st.p, E.sine);
  levha(ctx, cam, () => cizGol(st.t, { sway: .025 }));
}, { tr: { type: 'black', dur: 1.4, end: true } });
plan('P040', (ctx, st) => {
  levha(ctx, { cx: 960, cy: 560, z: 1.04 }, () => cizGol(st.t, { head: .05, sway: .02 }));
}, { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => chapterCard(ctx, 'CEHENNEMDE KRAL', 'Her şeyini kaybeden biri, ilk olarak ne söyler?', st.lt, st.d + .4, { y: 250 }) });
plan('P041', (ctx, st) => {
  const t = st.t, tG = Wd('E02', 'görür');
  const cam = camLerp({ cx: 1000, cy: 560, z: 1 }, { cx: 1020, cy: 600, z: 1.1 }, st.p, E.sine);
  levha(ctx, cam, () => gol_ikili(t, { head: lerp(.42, -.32, E.io2(gol_u(t, tG - .3, tG + 1.1))), sway: .02 }));
}, { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => quote(ctx, '“Ah, ne kadar düşmüş, ne kadar değişmişsin!”', 960, 190, st.t - Wd('E02', 'ah'), { px: 68, maxW: 1500, panel: .8 }) });
// dört söz: kelimeleri anlatımla birlikte, tek satırda sırayla
function gol_dortSoz(ctx, t) {
  if (NOTEXT) return;
  const W4 = [['İRADE', 'irade'], ['İNTİKAM', 'intikam'], ['NEFRET', 'nefret'], ['YÜREKLİLİK', 'yüreklilik']], sep = '  ·  ';
  ctx.save(); ctx.font = FONT.baslik(54, 700); ctx.letterSpacing = '6px'; ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
  const ws = W4.map(w => ctx.measureText(w[0]).width), ss = ctx.measureText(sep).width, tot = ws.reduce((a, b) => a + b, 0) + ss * 3;
  let x = 960 - tot / 2; const y = 190;
  const a0 = clamp((t - Wd('E03', 'irade') + .2) / .5); if (a0 > 0) { ctx.globalAlpha = a0; softPanel(ctx, 960, y, tot / 2 + 90, 80, .78); }
  W4.forEach(([s, k], i) => {
    const a = E.sine(clamp((t - Wd('E03', k) + .1) / .5));
    ctx.globalAlpha = a; ctx.fillStyle = PAPER_CSS; ctx.fillText(s, x, y + (1 - a) * 8); x += ws[i];
    if (i < 3) { ctx.globalAlpha = a * .7; ctx.fillText(sep, x, y); x += ss; }
  });
  ctx.restore();
}
plan('P042', (ctx, st) => {
  const t = st.t, tT = Wd('E03', 'toparlanır'), u = E.io2(gol_u(t, tT - .2, tT + 1.8));
  const cam = camLerp({ cx: 1020, cy: 600, z: 1.1 }, { cx: 900, cy: 560, z: 1.18 }, st.p, E.sine);
  levha(ctx, cam, () => gol_ikili(t, { head: lerp(-.32, .62, u), rise: 46 * u, lean: lerp(.16, -.04, u), sway: .02, blift: .3 * u }));
}, { tr: { type: 'cut' }, over: (ctx, st) => gol_dortSoz(ctx, st.t) });
// gölden kalkış: "göklerin izniyle" (I.210–213) yarıktan inen ışık; zincirler kopup suya düşer, kanatlar açılır
plan('P045', (ctx, st) => {
  const t = st.t, tK = Wd('E05', 'kalkar'), tG = Wd('E05', 'göklerin');
  const r = E.io3(gol_u(t, tK - .4, tK + 2.6)), sh = .45 * E.sine(gol_u(t, st.at, tK)) + .55 * E.sine(gol_u(t, tG - .3, tG + .9));
  levha(ctx, { cx: 960, cy: 520, z: 1 }, () => cizGol(t, { rise: 236 * r, head: lerp(.42, .3, r), lean: lerp(.04, -.02, r), legs: true, open: E.io2(gol_u(t, tK + .4, tK + 2.6)), lift: .8 * E.io2(gol_u(t, tK + .6, tK + 2.8)),
    loose: gol_u(t, tK, tK + 1.3), shaft: sh, armN: [lerp(-.5, -.25, r), .22], armF: [lerp(.55, .3, r), -.2] }));
}, { tr: { type: 'fade', dur: .8 } });

// ═════════ KIY: yanan kıyı (E06–E12, L04) ═════════
const KIY_FX = 900;
// P046: kıyıya çıkar, cehennemi selamlar (kol cehenneme açılır)
plan('P046', (ctx, st) => {
  const t = st.t, tS = Wd('E06', 'selamlar'), a = E.io2(gol_u(t, tS - .2, tS + 1.6));
  const cam = camLerp({ cx: 960, cy: 540, z: 1 }, { cx: 930, cy: 520, z: 1.08 }, st.p, E.sine);
  levha(ctx, cam, () => cizKiyi(t, { fx: KIY_FX, fig: gy => kiy_seytan(t, { x: KIY_FX - 20, gy, h: 56, head: lerp(-.05, .22, a), armN: [lerp(.15, 1.75, a), lerp(.2, .05, a)], armF: [-.1, .2], lum: .05 }) }));
}, { tr: { type: 'fade', dur: .9 },
  over: (ctx, st) => quote(ctx, '“Zihin kendi dünyasıdır.”', 960, 115, st.t - Wd('E06', 'zihin'), { px: 70, kaynak: 'KAYIP CENNET · I. 254–255' }) });
// P047–P048: mızrağı yere saplar; filmin en ünlü dizesi (I.263)
const KIY_HZ = 600;
function gol_mizrak(t, tS) {
  // tS: darbe anı. Önce mızrak yanda dik; ön hazırlıkta kol kalkar, sonra hızla iner ve uç kıyıya saplanır
  const up = E.io2(gol_u(t, tS - 1.6, tS - .28)), dn = E.in3(gol_u(t, tS - .28, tS));
  const a = lerp(lerp(.25, 2.25, up), .7, dn), b = lerp(lerp(.15, -.35, up), .35, dn);
  return { armN: [a, b], hit: gol_u(t, tS, tS + .8) };
}
function gol_kiyMizrak(t, tS, o = {}) {
  const m = gol_mizrak(t, tS), GY = KIY_HZ + 220, X = KIY_FX - 20;
  return cizKiyi(t, { fx: KIY_FX, hz: KIY_HZ, fig: gy => {
    const J = kiy_seytan(t, { x: X, gy, h: 58, head: .18, armN: m.armN, armF: [-.15, .2], lum: .08, spear: { grip: 'N', ang: 0, len: 8.4, bottomY: gy + 24 } });
    // darbe: uçtan kıvılcım vuruşları (kısa, sivrilen; .8 sn'de söner) ve kıyıda iki çatlak
    if (m.hit > 0 && m.hit < 1) {
      const x0 = J.wrN[0], k = E.out3(m.hit), v = 1 - m.hit;
      GR.tx.save(); GR.tx.globalAlpha = v;
      for (let i = 0; i < 7; i++) { const an = -PI / 2 + (i - 3) * .36, L = (60 + 26 * (i % 3)) * k; gol_vurus(GR.tx, [[x0 + Math.cos(an) * 14, gy + 18 + Math.sin(an) * 14], [x0 + Math.cos(an) * (14 + L), gy + 18 + Math.sin(an) * (14 + L)]], 6, 1, .9); }
      GR.tx.restore();
    }
    if (m.hit > 0) for (const [dx, sg] of [[-1, 1], [1, -1]]) gol_vurus(GR.tx, [[J.wrN[0], gy + 22], [J.wrN[0] + dx * 60 * E.out3(m.hit), gy + 30 + sg * 4], [J.wrN[0] + dx * 120 * E.out3(m.hit), gy + 44]], 5, .85);
  } });
}
plan('P047', (ctx, st) => {
  const t = st.t, tS = Wd('E07', 'söyler');
  levha(ctx, { cx: 930, cy: 520, z: 1.04 }, () => gol_kiyMizrak(t, tS));
}, { tr: { type: 'cut' }, mb: 3,
  over: (ctx, st) => quote(ctx, '“Cehennemde hükümdar olmak, cennette hizmetkâr olmaktan yeğdir.”', 960, 125, st.t - Wd('E07', 'cehennemde') + .1, { px: 68, maxW: 1400, per: .8, kaynak: 'KAYIP CENNET · I. 263' }) });
plan('P048', (ctx, st) => {
  levha(ctx, { cx: 930, cy: 520, z: 1.06 }, () => gol_kiyMizrak(st.t, Wd('E07', 'söyler')));
}, { tr: { type: 'cut' },
  over: (ctx, st) => {
    quote(ctx, '“Cehennemde hükümdar olmak, cennette hizmetkâr olmaktan yeğdir.”', 960, 115, 9, { px: 58, maxW: 1300, panel: .8 });
    quote(ctx, 'cennette köle olacağıma, cehennemde kral olurum', 960, 262, st.t - Wd('E08', 'cennette') + .2, { px: 66, maxW: 1500, panel: .85 });
  } });

// P049: ölçek karesi. Omzunda ay gibi asılı kalkan; mızrağın dibinde, en büyük geminin direği bir değnek (I.284–294)
function gol_kalkan(J) {
  const { tx, tone } = GR, h = J.h, c = [J.shN[0] - 1.45 * h, J.shN[1] + .1 * h], R = 1.4 * h;
  const P = new Path2D(); P.arc(c[0], c[1], R, 0, TAU);
  GR.fill(P, tone(.96), { type: 'rad', cx: c[0], cy: c[1], id: 9 });
  tx.save(); tx.clip(P);
  // ay yüzü gibi: gölge yanında hilal biçimli koyu kenar ve birkaç eş merkezli kabartma halkası (mürekkep vuruşu)
  const S = new Path2D(); S.arc(c[0], c[1], R, 0, TAU); S.arc(c[0] + R * .22, c[1] - R * .16, R * 1.02, 0, TAU, true);
  tx.fillStyle = tone(.05); tx.fill(S, 'evenodd');
  for (const [r, a0, a1, w] of [[.78, 2.2, 4.1, 7], [.56, 2.5, 3.9, 6], [.3, 2.6, 3.7, 5]]) {
    const pts = []; for (let i = 0; i <= 10; i++) { const a = lerp(a0, a1, i / 10); pts.push([c[0] + Math.cos(a) * R * r, c[1] + Math.sin(a) * R * r]); }
    gol_vurus(tx, pts, w, .1);
  }
  tx.restore();
  tx.strokeStyle = tone(.02); tx.lineWidth = 7; tx.beginPath(); tx.arc(c[0], c[1], R - 3, 0, TAU); tx.stroke();
}
function gol_direk(x, y, s, t) {
  const { tx, tone } = GR, H0 = 250 * s;
  tx.fillStyle = tone(.03);
  tx.beginPath(); tx.moveTo(x - 4 * s, y); tx.lineTo(x - 2.4 * s, y - H0); tx.lineTo(x + 2.4 * s, y - H0); tx.lineTo(x + 4 * s, y); tx.fill();      // direk
  for (const [hy, w] of [[.62, 46], [.86, 30]]) { tx.fillRect(x - w * s, y - H0 * hy - 2.5 * s, 2 * w * s, 5 * s); }                                  // seren
  tx.fillRect(x - 9 * s, y - H0 * .74, 18 * s, 10 * s);                                                                                           // gözcü yeri
  const fl = Math.sin(t * 2.1) * 3 * s; tx.beginPath(); tx.moveTo(x + 2 * s, y - H0); tx.lineTo(x + 30 * s, y - H0 + 5 * s + fl); tx.lineTo(x + 2 * s, y - H0 + 11 * s); tx.fill();   // flama
  tx.strokeStyle = tone(.03); tx.lineWidth = 2.2 * s; tx.beginPath(); tx.moveTo(x, y - H0); tx.lineTo(x - 40 * s, y); tx.moveTo(x, y - H0); tx.lineTo(x + 40 * s, y); tx.stroke(); // halat
}
plan('P049', (ctx, st) => {
  const t = st.t, tM = Wd('E09', 'mızrağı'), tD = Wd('E09', 'direği');
  const cam = camLerp({ cx: 960, cy: 830, z: 1 }, { cx: 960, cy: 1190, z: 1 }, gol_u(t, tM - .2, tD + .6), E.io2);
  levha(ctx, cam, () => cizKiyi(t, { fx: 1020, hz: 1490, gy: 1700, front: false, fig: gy => {
    const J = kiy_seytan(t, { x: 820, gy, h: 122, head: .2, armN: [.95, .45], armF: [-.2, .2], lum: .1, cloak: 1.1, mid: gol_kalkan, spear: { grip: 'N', ang: 0, len: 11, bottomY: gy + 14 } });
    gol_direk(J.wrN[0] + 120, gy + 4, 1, t);
  } }));
}, { tr: { type: 'cut' } });

// P050: omuz üstü profil (h 150): yıldırım izleri, kaşta gurur, gözde pişmanlık
function gol_hl(J, x, y) { const hh = J.h * 1.04, f = J.f, tl = J.headTilt, c = Math.cos(-tl * f), s = Math.sin(-tl * f); x *= f * hh; y *= hh; return [J.hd[0] + x * c - y * s, J.hd[1] + x * s + y * c]; }
const GOL_IZ = [[[.04, -.42], [.13, -.27], [.07, -.18], [.19, -.02]], [[-.16, -.08], [-.04, .05], [-.09, .14], [.06, .3]], [[.22, -.36], [.3, -.24], [.25, -.16]]];
function cizProfil(t, o = {}) {
  const { tx, tone } = GR;
  let g = tx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, tone(.02)); g.addColorStop(.6, tone(.05)); g.addColorStop(1, tone(.2));
  tx.fillStyle = g; tx.fillRect(-300, -300, W + 600, H + 600);
  PR.glow(860, 640, 120, 470, 1, .95);
  PR.cloud({ x: 1700, y: 200, w: 900, h: 260, seed: 19, lit: [-.75, .65], base: .02, hi: .75, core: .02, n: 4, drift: Math.sin(t * .08) * 8 });
  PR.flameBank(-80, W + 80, 900, 80, t, 71, { env: f => .3 + .7 * Math.pow(Math.sin(f * PI), 1.4) });
  const J = SF.rig({ x: 800, y: 1010 + Math.sin(t * .6) * 2, h: 150, facing: 1, twist: .55, lean: .02, head: o.head ?? .1, shTilt: -.04, armN: [.05, .1], armF: [-.05, .1] });
  for (const [side, P] of [[-1, { span: 1050, open: .5, lift: .3, droop: .7, rot: .15, seed: 31, root: .1 }]]) {
    GR.frame(J.shF[0] + 40, J.shF[1] + 30, P.rot, side, 1);
    KN.feathered(Object.assign({ dark: .92, rim: .75, ruin: .6, t, lit: [-.35, -.94] }, P)); GR.unframe();
  }
  SF.draw(J, { lum: .15, lit: [.35, -.94], t, legs: false, skirt: false, eye: 1, wind: .6, cloak: 1, halo: 4, lines: 2 });
  // yıldırım izleri: yüzde kırık, ince beyaz vuruşlar; anlatımla sırayla çizilir
  const iz = o.iz ?? 1;
  GOL_IZ.forEach((pl, i) => { const u = clamp(iz * 3 - i); if (u <= 0) return; const pts = pl.map(([x, y]) => gol_hl(J, x, y)), m = 1 + u * (pts.length - 1), q = pts.slice(0, Math.ceil(m));
    const k = m - Math.floor(m); if (k > 0 && q.length < pts.length) { const a = pts[q.length - 1], b = pts[q.length]; q.push([lerp(a[0], b[0], k), lerp(a[1], b[1], k)]); }
    if (q.length > 1) { for (let j = 0; j < q.length - 1; j++) gol_vurus(tx, [q[j], q[j + 1]], i === 2 ? 4 : 5, .95, .4); } });
  return J;
}
let GOL_PJ = null;
plan('P050', (ctx, st) => {
  const t = st.t, tY = Wd('E10', 'yıldırımların');
  const cam = camLerp({ cx: 960, cy: 560, z: 1 }, { cx: 930, cy: 540, z: 1.08 }, st.p, E.sine);
  levha(ctx, cam, () => { GOL_PJ = { J: cizProfil(t, { iz: E.sine(gol_u(t, tY, tY + 1.8)), head: lerp(.05, .14, E.sine(gol_u(t, Wd('E10', 'görkemli') - .5, Wd('E10', 'görkemli') + 1))) }), cam }; });
}, { tr: { type: 'fade', dur: .8 },
  over: (ctx, st) => {
    if (!GOL_PJ) return;
    const { J, cam } = GOL_PJ, cm = camOf(cam), sc = p => [(p[0] - cm.x) * cm.s, (p[1] - cm.y) * cm.s];
    const kas = sc(gol_hl(J, .3, -.2)), goz = sc(gol_hl(J, .3, -.055));
    for (const [s, w, p, x, y] of [['GURUR', 'gurur', kas, 1350, 400], ['PİŞMANLIK', 'gözlerinde', goz, 1420, 640]]) {
      const lt = st.t - Wd('E10', w); if (lt <= 0) continue;
      etiket(ctx, s, x, y, lt, 99, { px: 46 });
      const a = E.sine(clamp(lt / .6)), x0 = x - ctx.measureText ? x - 170 - (s.length > 6 ? 70 : 0) : x;
      ctx.save(); ctx.globalAlpha = a * .9; ctx.strokeStyle = PAPER_CSS; ctx.lineWidth = 2.5; ctx.lineCap = 'round';
      const ex = lerp(x0, p[0] + 34, E.out3(clamp(lt / .8))), ey = lerp(y, p[1], E.out3(clamp(lt / .8)));
      ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(ex, ey); ctx.stroke(); ctx.restore();
    }
  } });

// P051 / P134: ordu. Önde Şeytan (sol, profil), karşısında yanık ama ayakta melek safları; saflar bir an yıldırım çarpmış ormana döner (I.612–615)
// Saflar: üst üste binen sıralar, uzaklaştıkça küçülür; her figür biraz farklı (boy, eğilme, kanat). Ucuz olsun diye basit siluet, ışık arkadan.
const GOL_SAF = (() => {
  const r = rng(77), L = [];
  const rows = [[606, 10, 44, 760, 1990], [626, 13, 34, 770, 1990], [656, 18, 25, 790, 1990], [700, 25, 17, 820, 1990], [770, 35, 11, 880, 1990]];
  rows.forEach(([y, h, n, x0, x1], ri) => {
    for (let i = 0; i < n; i++) L.push({ ri, x: lerp(x0, x1, (i + .2 + r() * .6) / n), y: y + (r() - .5) * h * .25, h: h * (.88 + r() * .24), lean: (r() - .5) * .14, wing: .25 + r() * .5, sp: r() < .35, ph: r() * TAU, br: 2 + Math.floor(r() * 3), s: r() });
  });
  return L;
})();
function gol_melek(f, a, t) {
  const { tx, tone } = GR, h = f.h, x = f.x, y = f.y, ln = f.lean + Math.sin(t * .4 + f.ph) * .01;
  const P = new Path2D(), X = (dx, dy) => [x + dx * h + ln * (y - (y + dy * h)) * -1, y + dy * h];
  const pts = [[-.42, 0], [-.36, -2.4], [-.62, -3.1], [-.3, -3.25], [-.2, -3.6], [0, -3.85], [.2, -3.6], [.3, -3.25], [.62, -3.1], [.36, -2.4], [.42, 0]];
  spline(P, pts.map(([dx, dy]) => X(dx, dy)), true, .5);
  // kanatlar: omuzdan yükselip sarkan kırık iki uç (yanık); kalkıklık figürden figüre değişir
  const wl = f.wing;
  for (const sd of [-1, 1]) { const Q = [X(sd * .25, -3.0), X(sd * (.9 + wl * .5), -3.9 - wl * 1.2), X(sd * (1.2 + wl * .3), -3.2 - wl * .6), X(sd * 1.05, -1.7), X(sd * .8, -2.1), X(sd * .55, -1.3)]; P.moveTo(...Q[0]); for (const q of Q.slice(1)) P.lineTo(...q); P.closePath(); }
  const hd = new Path2D(), c = X(0, -4.15); hd.arc(c[0], c[1], h * .33, 0, TAU); P.addPath(hd);
  if (f.sp) { const s0 = X(.5, .2), s1 = X(.62, -5.6); P.moveTo(s0[0] - h * .05, s0[1]); P.lineTo(s1[0] - h * .04, s1[1]); P.lineTo(s1[0] + h * .04, s1[1]); P.lineTo(s0[0] + h * .05, s0[1]); P.closePath(); }
  tx.save(); tx.globalAlpha = a;
  if (f.ri >= 2) { tx.save(); tx.translate(0, -3); tx.fillStyle = tone(.9); tx.fill(P); tx.restore(); }   // yakın sıralarda arkadan gelen ışığın ince üst kenarı
  tx.fillStyle = tone(.02); tx.fill(P); tx.restore();
}
function gol_agac(f, a, t) {
  const { tx, tone } = GR, h = f.h * 1.15, x = f.x + f.lean * h * 2, y = f.y, r = rng(f.s * 1e4 | 0);
  const P = new Path2D(), w0 = h * .32, top = y - h * (3.9 + f.s * .8);
  P.moveTo(x - w0, y); P.lineTo(x - w0 * .35, top + h * .5); P.lineTo(x - w0 * .1, top); P.lineTo(x + w0 * .25, top + h * .35); P.lineTo(x + w0 * .3, top + h * .6); P.lineTo(x + w0, y); P.closePath();
  for (let i = 0; i < f.br; i++) { const yy = lerp(y - h * 1.4, top + h * .6, (i + .5) / f.br + (r() - .5) * .1), sd = i % 2 ? 1 : -1, L = h * (.7 + r() * .7), an = -PI / 2 + sd * (.6 + r() * .4);
    const bx = x + sd * w0 * .3; P.moveTo(bx, yy + h * .12); P.lineTo(bx + Math.cos(an) * L, yy + Math.sin(an) * L); P.lineTo(bx, yy - h * .1); P.closePath(); }
  tx.save(); tx.globalAlpha = a;
  if (f.ri >= 2) { tx.save(); tx.translate(0, -3); tx.fillStyle = tone(.9); tx.fill(P); tx.restore(); }
  tx.fillStyle = tone(.02); tx.fill(P); tx.restore();
}
// o: {orman (0..1), head, gozyasi: [başlangıç zamanları], dener: [zamanlar]}
function cizOrdu(t, o = {}) {
  const { tx, tone } = GR, HZ = 600, FX = 560;
  let g = tx.createLinearGradient(0, 0, 0, HZ); g.addColorStop(0, tone(.02)); g.addColorStop(.6, tone(.03)); g.addColorStop(.88, tone(.14)); g.addColorStop(1, tone(.4));
  tx.fillStyle = g; tx.fillRect(-300, -300, W + 600, HZ + 300);
  PR.glow(FX, HZ - 30, 110, 520, 1, 1);
  PR.glow(1450, HZ - 10, 60, 420, 1, .5);
  PR.cloud({ x: 1700, y: 250, w: 1000, h: 250, seed: 19, lit: [-.75, .65], base: .02, hi: .75, core: .02, n: 4, drift: Math.sin(t * .08) * 8 });
  PR.flameBank(-80, W + 80, HZ + 2, 46, t, 81, { env: f => .35 + .65 * Math.pow(Math.sin(f * PI * .9 + .1), 1.5) });
  // kavrulmuş ova
  const G = new Path2D(); G.rect(-300, HZ, W + 600, H + 400); { const gg = tx.createLinearGradient(0, HZ, 0, HZ + 260); gg.addColorStop(0, tone(.34)); gg.addColorStop(1, tone(.03)); GR.fill(G, gg, { type: 'persp', y0: HZ, D: 400, p0: 9, p1: 12.5, id: 8 }); }
  const orm = clamp(o.orman || 0);
  for (const f of GOL_SAF) { if (orm < 1) gol_melek(f, 1 - orm, t); if (orm > 0) gol_agac(f, orm, t); }
  // önde Şeytan: belden yukarı (kadraj altı keser), sağa, ordusuna dönük
  const h = 118, br = Math.sin(t * .6) * 2;
  const J = SF.rig({ x: 470, y: 930 + br, h, facing: 1, twist: .3, lean: .02, head: o.head ?? -.02, shTilt: -.05, armN: [.08, .12], armF: [-.05, .1] });
  // kanat yok: pelerinle sarılı (kanat kökü başın arkasında kutu gibi okunuyordu)
  SF.draw(J, { lum: .2, lit: [.55, -.8], t, legs: true, skirt: true, eye: 1, wind: .6, cloak: 1.2, halo: 3.5, lines: 2 });
  // gözyaşları: gözden yanağa süzülen küçük, sade damla (kâğıt rengi), çene hizasında söner
  (o.yas || []).forEach((t0, i) => {
    const u = (t - t0) / 1.5; if (u <= 0) return;
    const e = gol_hl(J, .25 - .02 * i, .0), j = gol_hl(J, .2 - .02 * i, .36), k = E.in2(Math.min(u, 1)), p = [lerp(e[0], j[0], k), lerp(e[1], j[1], k)];
    // ıslak iz: gözden damlaya ince çizgi (kalır); damla çene hizasında söner
    if (k > .08) gol_vurus(tx, [e, [lerp(e[0], p[0], .5), lerp(e[1], p[1], .5)], p], 3.2, .95, .3);
    const s = u < 1 ? 1 : 0; if (!s) return;
    const D = new Path2D(); D.moveTo(p[0], p[1] - 12); D.quadraticCurveTo(p[0] + 6, p[1] + 2, p[0], p[1] + 6); D.quadraticCurveTo(p[0] - 6, p[1] + 2, p[0], p[1] - 12);
    tx.fillStyle = tone(.97); tx.fill(D);
  });
  return J;
}
plan('P051', (ctx, st) => {
  const t = st.t, tY = Wd('E11', 'yıldırım'), tA = Wd('E11', 'ayaktalar');
  const orman = E.io2(gol_u(t, tY - .2, tY + 1.1)) * (1 - E.io2(gol_u(t, tA - .4, tA + 1.0)));
  // üç kez dener: baş kalkar (konuşmaya hazırlanır), boğaz düğümlenir, düşer
  const dn = [Wd('E11', 'üç'), Wd('E11', 'üç', 1), Wd('E11', 'gururuna')];
  let hd = lerp(-.02, .05, E.sine(gol_u(t, Wd('E11', 'konuşmaya'), Wd('E11', 'hazırlanır') + .6)));
  for (const d of dn) hd += .14 * Math.sin(PI * gol_u(t, d - .1, d + .9));
  hd -= .08 * E.sine(gol_u(t, Wd('E11', 'gözlerinden') - .3, Wd('E11', 'gözlerinden') + .8));
  const cam = camLerp({ cx: 1000, cy: 560, z: 1 }, { cx: 880, cy: 600, z: 1.1 }, gol_u(t, Wd('E11', 'konuşmaya') - 1, Wd('E11', 'dener')), E.io2);
  levha(ctx, cam, () => cizOrdu(t, { orman, head: hd, yas: [Wd('E11', 'gözlerinden'), Wd('E11', 'yaşlar'), Wd('E11', 'boşanır')] }));
}, { tr: { type: 'fade', dur: .8 } });
plan('P134', (ctx, st) => {
  const t = st.t, tA = Wd('L04', 'ağlar');
  const cam = camLerp({ cx: 900, cy: 590, z: 1.05 }, { cx: 860, cy: 600, z: 1.12 }, st.p, E.sine);
  levha(ctx, cam, () => cizOrdu(t, { head: -.06, yas: [tA, Wd('L04', 'meleklerin')] }));
}, { tr: { type: 'fade', dur: .9 } });

// P052: şeytanlar toprağı kazar; yerden Dor sütunlu, altın tavanlı saray yükselir (I.670–730). Kubbe, minare, hilal, Osmanlı motifi yok.
// Saray: üç basamaklı krepis, 10 Dor sütunu (yivler beyaz vuruş), triglifli friz, alçak alınlık. İçerisi altın ışıkla parlar: sütun araları temiz kâğıt (odak).
function gol_saray(cx, gy, sc, rise) {
  const { tx, tone, fill } = GR, w = 980 * sc, hc = 330 * sc, dy = (1 - rise) * (hc + 300 * sc);
  tx.save(); { const C = new Path2D(); C.rect(-400, -800, W + 800, gy + 800); tx.clip(C); }
  GR.px.save(); { const C = new Path2D(); C.rect(-400, -800, W + 800, gy + 800); GR.px.clip(C); }
  const y0 = gy + dy, x0 = cx - w / 2, st = 18 * sc, top = y0 - 3 * st - hc;
  // iç ışık (altın tavanın parıltısı): sütunların arkasında düz kâğıt
  const IN = new Path2D(); IN.rect(x0 + 30 * sc, top - 10, w - 60 * sc, hc + 10); tx.fillStyle = tone(.97); tx.fill(IN);
  // basamaklar
  for (let i = 0; i < 3; i++) { const P = new Path2D(), e = (3 - i) * 22 * sc; P.rect(x0 - e, y0 - (i + 1) * st, w + 2 * e, st); fill(P, tone(.03), { th: 0, id: 4 }); gol_vurus(tx, [[x0 - e + 6, y0 - (i + 1) * st + 3], [x0 + w + e - 6, y0 - (i + 1) * st + 3]], 4, .9, .2); }
  // sütunlar: hafif entasis, yivler kenar ışığıyla
  const n = 10, cw = 46 * sc;
  for (let i = 0; i < n; i++) {
    const x = x0 + 50 * sc + (w - 100 * sc) * i / (n - 1), P = new Path2D(), b = y0 - 3 * st;
    P.moveTo(x - cw / 2, b); P.quadraticCurveTo(x - cw * .56, b - hc * .4, x - cw * .4, top + 14 * sc); P.lineTo(x + cw * .4, top + 14 * sc); P.quadraticCurveTo(x + cw * .56, b - hc * .4, x + cw / 2, b); P.closePath();
    P.rect(x - cw * .62, top, cw * 1.24, 14 * sc);                                                                      // başlık (abakus)
    fill(P, tone(.03), { th: -PI / 2, id: 9 });
    gol_vurus(tx, [[x - cw * .28, b - 6], [x - cw * .26, top + 22 * sc]], 4.5, .92, .2);                               // yiv ışığı
  }
  // friz ve alınlık
  const fr = new Path2D(), eh = 52 * sc; fr.rect(x0 - 10 * sc, top - eh, w + 20 * sc, eh); fill(fr, tone(.03), { th: 0, id: 9 });
  for (let i = 0; i < 2 * n - 1; i++) { if (i % 2) continue; const x = x0 + 50 * sc + (w - 100 * sc) * (i / 2) / (n - 1); for (const d of [-8, 0, 8]) gol_vurus(tx, [[x + d * sc, top - eh + 10 * sc], [x + d * sc, top - 14 * sc]], 3.5, .85, .2); }
  const pd = new Path2D(); pd.moveTo(x0 - 24 * sc, top - eh); pd.lineTo(cx, top - eh - 120 * sc); pd.lineTo(x0 + w + 24 * sc, top - eh); pd.closePath(); fill(pd, tone(.03), { th: 0, id: 9 });
  gol_vurus(tx, [[x0 - 10 * sc, top - eh - 6], [cx, top - eh - 112 * sc], [x0 + w + 10 * sc, top - eh - 6]], 6, .95, .15);
  tx.restore(); GR.px.restore();
}
// kazan şeytan: öne eğik, iki eliyle kazma sallar (her biri kendi ritminde); kazma ucu kaldırılınca yukarı, inince çukura
function gol_kazici(x, y, h, t, ph) {
  const sw = Math.sin(t * 2.0 + ph), up = E.sine((sw + 1) / 2), a = lerp(.75, 2.55, up);
  const J = SF.rig({ x, y: y - 3.6 * h, h, facing: 1, twist: .25, lean: .42 - .12 * up, head: -.25, shTilt: .05, armN: [a, .25], armF: [a - .15, .35], legN: [.35, -.4], legF: [-.2, -.15] });
  SF.draw(J, { lum: 0, lit: [-.3, -.95], t, legs: true, skirt: false, eye: 0, wind: .3, cloak: false, halo: 2.5, lines: 0, seed: 11 + ph * 3, spear: { grip: 'N', ang: a - PI / 2 + .3 + PI * .5, len: 2.2, up: .8 } });
}
plan('P052', (ctx, st) => {
  const t = st.t, tY = Wd('E12', 'yerden'), tK = Wd('E12', 'şeytanlar');
  const rise = E.out3(gol_u(t, tY - .3, tY + 2.4)), dig = E.sine(gol_u(t, tK - .6, tK + .6)) * (1 - .6 * rise);
  const cam = camLerp({ cx: 960, cy: 560, z: 1.06 }, { cx: 960, cy: 520, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => cizKiyi(t, { fx: 960, hz: 640, wall: .6, front: false, fig: gy => {
    gol_saray(960, 650, .9, rise);
    // kazılan çukurlarda erimiş altın parlar (I.700–704): her kazıcı kendi çukurunun ışığına karşı siluet okunur
    for (const [x, y, h, ph] of [[500, 930, 30, 0], [800, 975, 34, 3.1], [1140, 940, 31, .9], [1460, 990, 36, 2.4]]) {
      const v = clamp(dig * 1.4), P = new Path2D(); P.ellipse(x + 1.6 * h, y + 2, 1.9 * h * (.5 + .5 * v), .32 * h, 0, 0, TAU);
      GR.fill(P, GR.tone(.97), { th: 0, id: 3 });
      gol_kazici(x, y, h, t, ph);
    }
    // Şeytan solda, kayalıkta: konuşur (kolu kalkık), sonra izler
    kiy_seytan(t, { x: 230, gy: gy + 10, h: 44, head: .15, armN: [lerp(.2, 2.2, E.sine(gol_u(t, st.at, st.at + 1.2)) * (1 - E.sine(gol_u(t, tK, tK + 1.2)))), .1], lum: .1, cloak: 1.1 });
  } }));
}, { tr: { type: 'fade', dur: .9 },
  over: (ctx, st) => etiket(ctx, 'PANDEMONIUM', 960, 150, st.t - Wd('E12', 'pandemonyum'), 99, { px: 64, ls: 14 }) });
