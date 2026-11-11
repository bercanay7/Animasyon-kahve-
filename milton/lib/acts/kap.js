// kap grubu (KAP: cehennem kapısı): planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Set: zifiri karanlıkta dokuz katlı dev kapı (II.645–648: üç kat pirinç, üç kat demir, üç kat elmas; üst üste dokuz yatay bant),
// önünde alçak alevler (tek ışık kaynağı: kapının dibi; odak). İki bekçi: GÜNAH (örtülü, uzun pelerinli kadın silueti; eteği aşağıda
// yılan kıvrımına döner; yüz, çıplaklık yok) ve ÖLÜM (biçimsiz, taçlı koyu gölge; dumanlı kenarlar; elinde mızrak).
// II.760–814'ün ayrıntıları görsele girmez. Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd).
'use strict';
const kap_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));
function kap_yon(pts) { let a = 0; for (let i = 0; i < pts.length; i++) { const p = pts[i], q = pts[(i + 1) % pts.length]; a += p[0] * q[1] - q[0] * p[1]; } return a < 0 ? pts.slice().reverse() : pts; }
function kap_yol(pts, sp = .7) { const P = new Path2D(); spline(P, kap_yon(pts), true, sp); return P; }
const KAP_GY = 870;                                   // zemin
// kenar ışığı: yolu koyu bas, ışık yönünde (L: ışığa doğru birim vektör) w px bant bırak
function kap_kutle(P, L, w, v = .95, tn = .02) {
  const { tx, tone } = GR; GR.fill(P, null, { th: 0, id: 9 });
  tx.save(); tx.clip(P); tx.fillStyle = tone(v); tx.fill(P); tx.translate(-L[0] * w, -L[1] * w); tx.fillStyle = tone(tn); tx.fill(P); tx.restore();
}
// ── kapı ──
function kap_kapi(t, o = {}) {
  const { tx, tone } = GR, x0 = o.x0 ?? 660, x1 = o.x1 ?? 1260, top = -240, bot = KAP_GY, bh = (bot - top) / 9, lt = o.lt ?? 1;
  const lit = y => (.3 + .7 * clamp(1 - (bot - y) / 760)) * lt;                   // alttan gelen alev ışığı yukarı doğru söner
  // söveler: iki dev koyu ayak, iç kenarlarında ışık
  for (const [a, b, sd] of [[x0 - 170, x0, 1], [x1, x1 + 170, -1]]) {
    const P = new Path2D(); P.rect(a, top - 200, b - a, bot - top + 200); GR.fill(P, tone(.025), { th: -PI / 2, id: 4 });
    const xe = sd > 0 ? b - 4 : a + 4; tx.save(); tx.clip(P); gol_vurus(tx, [[xe, bot - 6], [xe, bot - 300], [xe, bot - 640]], 7 * lt, .95, .15); tx.restore();
  }
  // dokuz kat: alttan üç pirinç, üç demir, en üstte üç elmas
  const r = rng(91);
  for (let i = 0; i < 9; i++) {
    const yb = bot - i * bh, yt = yb - bh + 6, P = new Path2D(); P.rect(x0, yt, x1 - x0, yb - yt);
    const L = lit(yb), kind = i < 3 ? 0 : i < 6 ? 1 : 2;
    if (kind === 0) { const g = tx.createLinearGradient(0, yt, 0, yb); g.addColorStop(0, tone(.03 + .5 * L)); g.addColorStop(.5, tone(.03 + .22 * L)); g.addColorStop(1, tone(.03)); GR.fill(P, g, { th: 0, id: 9 }); }   // pirinç: parlak, yatay taramalı
    else GR.fill(P, tone(.025), { th: 0, id: 9 });
    tx.save(); tx.clip(P);
    gol_vurus(tx, [[x0 + 8, yt + 4], [(x0 + x1) / 2, yt + 5], [x1 - 8, yt + 4]], Math.max(3, 8 * L + 2), .96, .1);   // katın üst kenarı
    if (kind === 1) for (let k = 0; k < 7; k++) { const x = lerp(x0 + 50, x1 - 50, k / 6), y = (yt + yb) / 2, rr = 7, Q = new Path2D(); Q.arc(x, y, rr, 0, TAU); tx.fillStyle = tone(.2 + .7 * Math.max(L, .3)); tx.fill(Q); }   // demir: perçin sırası
    if (kind === 2) for (let k = 0; k < 9; k++) { const x = lerp(x0 + 40, x1 - 40, (k + r() * .4) / 9), y = yt + 14 + r() * (bh - 40), len = 30 + r() * 50; gol_vurus(tx, [[x, y], [x + len * .5, y + len * .35]], 5, .9, .7); }   // elmas: sivri yüz ışıkları
    tx.restore();
  }
  // orta çizgi (iki kanat)
  { const P = new Path2D(); P.rect((x0 + x1) / 2 - 5, top, 10, bot - top); tx.fillStyle = tone(.02); tx.fill(P); }
}
// ── zemin, ışık ve alevler ──
function kap_sahne(t, o = {}) {
  const { tx, tone } = GR, lt = o.lt ?? 1;
  tx.fillStyle = tone(.02); tx.fillRect(-400, -400, W + 800, H + 800);
  kap_kapi(t, o);
  PR.glow(960, KAP_GY + 10, 60, 800, 1, .9 * lt);                     // kapının dibinde alev ışığı (odak)
  const G = new Path2D(); G.rect(-400, KAP_GY, W + 800, 600);
  { const g = tx.createRadialGradient(960, KAP_GY, 0, 960, KAP_GY, 980); g.addColorStop(0, tone(.55 * lt)); g.addColorStop(.45, tone(.12 * lt)); g.addColorStop(1, tone(.02)); GR.fill(G, g, { type: 'persp', y0: KAP_GY, D: 300, p0: 9.5, p1: 12.5, id: 8 }); }
  if (o.mid) o.mid();
  PR.flameBank(520, 1400, KAP_GY + 14, 80, t, 37, { band: false, n: 8, wr: .6, curl: .4, speed: .55, solidBelow: 500, strip: .4, frags: false, env: f => .4 + .6 * Math.sin(f * PI) });
  if (o.fig) o.fig();
  if (o.front) o.front();
}
// ── GÜNAH: örtülü kadın silueti; eteği yılan kıvrımına döner (kuyruk zeminde sola kıvrılır). x: ayak hizasında merkez, s ölçek (1 ≈ 520 px boy), f bakış (±1)
function kap_gunah(t, x, s, f = -1, o = {}) {
  const gy = KAP_GY + 4, sw = Math.sin(t * .8) * 4 * s, X = (u) => x + u * s * f, Y = v => gy - v * s;
  // başlık (öne düşen örtü), dar omuz, yere doğru genişleyen pelerin; pelerinin dibi arkaya doğru kalın bir yılan gövdesine akar ve zeminde kıvrılır
  const pts = [[22, 540], [-20, 534], [-50, 506], [-60, 470], [-66, 440], [-92, 412], [-112, 350], [-122, 260], [-128, 170], [-132, 90], [-130, 40],
    [-160, 26], [-230, 18 + sw * .2], [-300, 26], [-350, 50], [-362, 86], [-334, 108], [-300, 96], [-312, 72], [-282, 58], [-220, 50], [-160, 56], [-120, 52],
    [-60, 22], [20, 10], [92, 14], [96, 80], [94, 170], [88, 260], [78, 350], [64, 408], [58, 432], [70, 458], [74, 490], [62, 520]].map(([u, v]) => [X(u + (v > 300 ? sw * .02 : 0)), Y(v)]);
  const P = kap_yol(pts, .6);
  const L = [(960 - x) / Math.hypot(960 - x, 300), -300 / Math.hypot(960 - x, 300)];
  kap_kutle(P, L, Math.max(4, 7 * s));
  GR.tx.save(); GR.tx.clip(P);   // örtünün kıvrımları: başlıktan aşağı inen birkaç uzun vuruş, kuyrukta pul vuruşları
  for (const [u0, v0, u1, v1] of [[-40, 480, -80, 330], [-40, 400, -80, 160], [30, 390, 50, 120]]) gol_vurus(GR.tx, [[X(u0), Y(v0)], [X((u0 + u1) / 2 - 6), Y((v0 + v1) / 2)], [X(u1), Y(v1)]], 6 * s, .9, .6);
  for (let k = 0; k < 5; k++) { const u = -150 - k * 38, v = 44 + (k > 3 ? 10 : 0); gol_vurus(GR.tx, [[X(u), Y(v + 12)], [X(u - 8), Y(v)]], 5 * s, .9, .6); }
  GR.tx.restore();
  return { head: [X(0), Y(470)], top: [X(0), Y(520)] };
}
// ── ÖLÜM: biçimsiz, taçlı koyu gölge; kenarları dumanlı (yavaşça kıpırdar); mızrak. x: taban merkezi, s ölçek, sp (0..1 mızrak kalkışı)
function kap_olum(t, x, s, f = 1, o = {}) {
  const { tx, tone } = GR, gy = KAP_GY + 6, hgt = 640 * s, n = 40, pts = [];
  // yarı genişlik profili (v: 0 zemin … 1 tepe): yere doğru dağılan etek, geniş omuz, dar baş; kenarlar duman gibi yavaşça kıpırdar
  const WP = [[0, 165], [.15, 128], [.45, 108], [.7, 122], [.78, 96], [.84, 64], [.95, 58], [1, 0]];
  const side = (sd) => { const out = []; for (let i = 0; i <= n; i++) { const v = i / n, w0 = mec_tab(WP, v) * s, amp = (v < .3 ? 22 : 9) * s * (1 - v * .5);
    const nz = fbm1(i * .7 + (sd > 0 ? 40 : 0) + t * .3, 7) + .4 * Math.sin(i * 2.3 + t * .8 + sd); out.push([x + sd * (w0 + amp * nz), gy - v * hgt + (v < .02 ? 0 : 0)]); } return out; };
  const Rt = side(1), Lf = side(-1).reverse();
  for (let k = 0; k < 7; k++) { const u = k / 6, xx = lerp(x + 150 * s, x - 150 * s, u), yy = gy + (k % 2 ? -18 : 6) * s + Math.sin(t * .9 + k) * 4 * s; Rt.unshift; Lf.push([xx, yy]); }   // yırtık etek
  pts.push(...Rt, ...Lf);
  const P = kap_yol(pts, .9);
  // taç: başın üstünde beş sivri uç (kâğıt kenarlı, koyu)
  const cx = x - 4 * s * f, cy = gy - hgt + 26 * s, C = [];
  for (let i = 0; i <= 10; i++) { const u = i / 10, xx = cx + (u - .5) * 104 * s, tip = i % 2 === 0; C.push([xx, cy - (tip ? (i === 0 || i === 10 ? 26 : i === 4 || i === 6 ? 56 : 70) * s : 16 * s)]); }
  C.push([cx + 62 * s, cy + 20 * s], [cx - 62 * s, cy + 20 * s]);
  P.addPath(kap_yol(C, 0));
  const L = [(960 - x) / Math.hypot(960 - x, 360), -360 / Math.hypot(960 - x, 360)];
  // mızrak: kolun yerine dumandan çıkan ince sap; sp ile kalkar
  const sp = clamp(o.sp || 0), ang = lerp(-.12, -.85, E.io2(sp)) * f, hx = x + 70 * s * f, hy = gy - hgt * lerp(.52, .66, sp), len = 560 * s, d = [Math.sin(-ang), -Math.cos(ang)];
  const a0 = [hx - d[0] * len * .35, hy - d[1] * len * .35], a1 = [hx + d[0] * len * .65, hy + d[1] * len * .65], nx = -d[1] * 5.5 * s, ny = d[0] * 5.5 * s;
  const S = new Path2D(); S.moveTo(a0[0] + nx, a0[1] + ny); S.lineTo(a1[0] + nx, a1[1] + ny); S.lineTo(a1[0] - nx, a1[1] - ny); S.lineTo(a0[0] - nx, a0[1] - ny); S.closePath();
  const tl = 46 * s; S.moveTo(a1[0] + d[0] * tl, a1[1] + d[1] * tl); S.lineTo(a1[0] + nx * 3.5, a1[1] + ny * 3.5); S.lineTo(a1[0] - nx * 3.5, a1[1] - ny * 3.5); S.closePath();
  P.addPath(S);
  kap_kutle(P, L, Math.max(4, 7 * s));
  // dumanlı kenar: gövdenin dışına taşan, uçları sivrilen koyu kıvrımlar (çizgi değil, kütle) + içeride birkaç kâğıt vuruş
  tx.save(); tx.clip(P);   // ışık yanında, kenardan içe giren iki uzun duman vuruşu
  for (const v of [.3, .58]) { const y = gy - hgt * v, xe = x - f * 100 * s; gol_vurus(tx, [[xe, y], [xe + f * 40 * s, y - 50 * s], [xe + f * 60 * s, y - 120 * s]], 6 * s, .85, .7); }
  tx.restore();
  return { top: [cx, cy - 64 * s], tip: a1 };
}
// Şeytan kapıda (kiy_seytan): x ayak, h baş boyu
function kap_seytan(t, x, h, o = {}) { return kiy_seytan(t, Object.assign({ x, gy: KAP_GY + 6, h, facing: 1, head: .12, lum: .25, cloak: 1.3, wingK: .8, lit: [.6, -.8], armN: [.3, .2], armF: [-.1, .15] }, o)); }

// ═════════ F01 (P056): bölüm kartı; karanlıkta dev kapı (ışıkla açılır) ═════════
plan('P056', (ctx, st) => {
  const t = st.t, L = E.io2(kap_u(t, st.at + .2, st.at + 3.2));
  const cam = camLerp({ cx: 960, cy: 520, z: 1 }, { cx: 960, cy: 560, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => { kap_sahne(t); if (L < 1) gol_isik(L, 960, KAP_GY); });
}, { tr: { type: 'black', dur: 1.4, end: true },
  over: (ctx, st) => chapterCard(ctx, 'KAPIDAKİ BEKÇİLER', 'Peki Şeytan onu neden tanımadı?', st.lt - 1.2, st.d - .8, { y: 300 }) });

// ═════════ F02 (P057): kapı ve iki bekçi; yavaş yatay kaydırma ═════════
plan('P057', (ctx, st) => {
  const t = st.t, w = k => Wd('F02', k);
  const cam = camLerp({ cx: 900, cy: 560, z: 1 }, { cx: 1020, cy: 560, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => kap_sahne(t, { fig: () => { kap_gunah(t, 700, 1, 1); kap_olum(t, 1230, 1, -1, { sp: 0 }); } }));
}, { tr: { type: 'fade', dur: .8 } });

// ═════════ F03 (P058): kadın araya girer; arkada anı: başmeleğin başının sol yanından doğan ışık ═════════
function kap_ani(a, g, cx, cy) {   // a: görünürlük, g: doğan biçimin büyümesi
  if (a <= .01) return;
  const { tx, tone } = GR;
  tx.save(); tx.globalAlpha = a;
  PR.glow(cx, cy, 30, 300, 1, .8);
  // profil silueti (sağa bakar): baş ve omuz; ayrıntı yok
  const P = kap_yol([[cx - 70, cy + 190], [cx - 60, cy + 120], [cx - 52, cy + 40], [cx - 58, cy - 20], [cx - 40, cy - 70], [cx, cy - 86], [cx + 38, cy - 64], [cx + 50, cy - 30], [cx + 66, cy - 6], [cx + 52, cy + 6], [cx + 54, cy + 30], [cx + 36, cy + 58], [cx + 20, cy + 70], [cx + 26, cy + 120], [cx + 120, cy + 150], [cx + 150, cy + 190]], .6);
  tx.fillStyle = tone(.03); tx.fill(P);
  // başın sol yanından (arkası, üstü) çıkan beyaz biçim: sivrilen ışık dili
  if (g > .01) { const b = [cx - 46, cy - 60], L = 210 * E.out3(g), an = -2.2, e = [b[0] + Math.cos(an) * L, b[1] + Math.sin(an) * L], wd = 46 * E.out3(g), nx = -Math.sin(an), ny = Math.cos(an);
    const F = kap_yol([[b[0] + nx * wd * .4, b[1] + ny * wd * .4], [lerp(b[0], e[0], .5) + nx * wd, lerp(b[1], e[1], .5) + ny * wd], e, [lerp(b[0], e[0], .5) - nx * wd * .7, lerp(b[1], e[1], .5) - ny * wd * .7], [b[0] - nx * wd * .3, b[1] - ny * wd * .3]], .7);
    tx.fillStyle = tone(.99); tx.fill(F); }
  tx.restore();
}
plan('P058', (ctx, st) => {
  const t = st.t, w = k => Wd('F03', k);
  const gi = E.io2(kap_u(t, w('kadın') - .2, w('girer') + .8)), aa = E.sine(kap_u(t, w('cennette') - .3, w('başının'))) * (1 - E.sine(kap_u(t, w('günah') + .2, w('dediler') + .9))), gg = kap_u(t, w('yarıldı') - .2, w('doğdum') + .4);
  levha(ctx, { cx: 960, cy: 560, z: 1 }, () => kap_sahne(t, { lt: .9, mid: () => kap_ani(aa, gg, 250, 230), fig: () => {
    kap_seytan(t, 300, 62, { armN: [lerp(.3, 1.1, E.io2(kap_u(t, w('dövüşmeye') - .3, w('hazırlanırken')))) * (1 - gi * .7), .3], spear: { grip: 'N', ang: .3, len: 7, up: .7 } });
    kap_olum(t, 1180, .95, -1, { sp: .15 });
    kap_gunah(t, lerp(1480, 720, gi), .9, -1);
  } }));
}, { tr: { type: 'cut' },
  over: (ctx, st) => etiket(ctx, 'GÜNAH', 720, 230, st.t - Wd('F03', 'günah'), 99, { px: 54, ls: 10 }) });

// ═════════ F04 (P059): gölge mızrağını kaldırır; iki profil karşı karşıya ═════════
plan('P059', (ctx, st) => {
  const t = st.t, w = k => Wd('F04', k), sp = E.io2(kap_u(t, w('dövüşmek') - .3, w('olduğu') + .4));
  const cam = camLerp({ cx: 990, cy: 560, z: 1 }, { cx: 930, cy: 560, z: 1 }, st.p, E.sine);
  levha(ctx, cam, () => kap_sahne(t, { lt: .85, fig: () => {
    kap_gunah(t, 960, .7, -1);
    kap_seytan(t, 470, 82, { head: .05, armN: [lerp(.6, 1.6, sp), .4], spear: { grip: 'N', ang: .6, len: 7, up: .7 }, wingK: .75, open: .3 * sp });
    kap_olum(t, 1430, 1.05, -1, { sp });
  } }));
}, { tr: { type: 'cut' },
  over: (ctx, st) => {
    if (NOTEXT) return;
    const t1 = st.t - Wd('F04', 'ölüm'), t2 = st.t - Wd('F04', 'kendi', 1);
    if (t1 <= 0) return;
    ctx.save(); ctx.font = FONT.baslik(56, 600); ctx.letterSpacing = '8px'; const a = ctx.measureText('ÖLÜM').width, b = ctx.measureText(' · kendi oğlu').width; ctx.restore();
    const x0 = 1000 - (a + b) / 2;
    etiket(ctx, 'ÖLÜM', x0 + a / 2, 105, t1, 99, { px: 56, ls: 8 });
    if (t2 > 0) etiket(ctx, ' · kendi oğlu', x0 + a + b / 2, 105, t2, 99, { px: 56, ls: 8, panel: 0 });
  } });
