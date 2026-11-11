// oku grubu: "İki okuma" (OKU) ve Cabanel (CAB) planları (bkz. lib/acts/KILAVUZ.md)
// Levha dili kit.js ile ortaktır (kit_* yardımcıları: çerçeve, yazı ton katmanına basılır, kelimeye bağlı beliriş).
// Bütün çekim içi olaylar anlatımdaki kelimelere bağlıdır (Wd); saniye yazılmaz.
'use strict';
const oku_u = (t, a, b) => clamp((t - a) / ((b - a) || 1));
// sivrilen vuruş (ton katmanına): pts boyunca, w genişlikten uca doğru incelir
function oku_vurus(pts, w, v, uc = .35, c = GR.tx) {
  const n = pts.length; if (n < 2) return;
  const A = [], B = [];
  for (let i = 0; i < n; i++) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, u = i / (n - 1);
    const hw = Math.max(1.3, w * .5 * (1 - (1 - uc) * u));
    A.push([pts[i][0] - dy / l * hw, pts[i][1] + dx / l * hw]); B.push([pts[i][0] + dy / l * hw, pts[i][1] - dx / l * hw]);
  }
  const P = new Path2D(); poly(P, [...A, ...B.reverse()], true);
  c.save(); c.fillStyle = typeof v === 'string' ? v : GR.tone(v); c.fill(P); c.restore();
}
// ışıkla açılış (KILAVUZ): ton katmanı önce karanlık; odak (cx, cy) çevresinden açılır. u: 0..1
function oku_isikAc(u, cx = 960, cy = 540) {
  if (u >= 1) return; const { tx } = GR, e = E.io2(clamp(u));
  tx.save(); tx.setTransform(RS, 0, 0, RS, 0, 0); tx.globalCompositeOperation = 'multiply';
  const g = tx.createRadialGradient(cx, cy, 0, cx, cy, 1300);
  g.addColorStop(0, GR.tone(clamp(e * 1.6))); g.addColorStop(.5, GR.tone(clamp(e * 1.25))); g.addColorStop(1, GR.tone(e));
  tx.fillStyle = g; tx.fillRect(0, 0, W, H); tx.restore();
}

// ═════════════════ CABANEL ═════════════════
// Bizim gravür yorumumuz: yalnız kavuşturulmuş kollar, kolların üstünden bakan göz, kaş, alın ve saç; gövde görünmez (kırmızı çizgi 7).
// Yakın kadraj dünya koordinatında (1920×1080): yakın göz (860, 455), uzak göz saç perçeminin altında.
const CAB = {
  yuz: [[340, 860], [330, 400], [520, 160], [960, 110], [1400, 160], [1640, 400], [1660, 860]],
  sacTaban: [[340, 1160], [330, 620], [352, 470], [430, 360], [540, 292], [680, 252], [830, 236], [980, 238], [1120, 256], [1250, 292], [1370, 352], [1460, 450], [1520, 600], [1550, 800], [1570, 1160]],
  percem: [[1200, 236], [1290, 300], [1370, 430], [1410, 580], [1420, 730], [1350, 735], [1320, 590], [1268, 450], [1196, 330], [1150, 270]],
  goz: { x: 880, y: 470, w: 380 }, yumru: [],
};
function cab_kol(p0, p1, w0, w1, hand) {   // ön kol: dirsekten bileğe incelen kütle; bilekte yuvarlak el
  const dx = p1[0] - p0[0], dy = p1[1] - p0[1], l = Math.hypot(dx, dy), ux = dx / l, uy = dy / l, nx = -uy, ny = ux, P = new Path2D();
  const at = (u, k) => [lerp(p0[0], p1[0], u) + nx * k, lerp(p0[1], p1[1], u) + ny * k];
  spline(P, [at(0, w0), at(.5, (w0 + w1) * .52), at(1, w1), [p1[0] + ux * hand * .7 + nx * w1 * .75, p1[1] + uy * hand * .7 + ny * w1 * .75], [p1[0] + ux * hand * 1.05, p1[1] + uy * hand * 1.05],
    [p1[0] + ux * hand * .7 - nx * w1 * .85, p1[1] + uy * hand * .7 - ny * w1 * .85], at(1, -w1), at(.5, -(w0 + w1) * .5), at(0, -w0)], true, .8);
  return { P, a: Math.atan2(dy, dx), n: [nx, ny], c: at(.6, 0) };
}
function cab_kollar() {
  const { tx } = GR;
  const K = [cab_kol([1990, 1000], [700, 722], 150, 104, 128), cab_kol([-70, 980], [1240, 704], 155, 106, 132)];   // arkadaki (sağdan), öndeki (soldan)
  K.forEach((k, i) => {
    const up = k.n[1] < 0 ? 1 : -1, ux = k.n[0] * up, uy = k.n[1] * up;   // üst yan normali
    const g = tx.createLinearGradient(k.c[0] + ux * 150, k.c[1] + uy * 150, k.c[0] - ux * 150, k.c[1] - uy * 150);
    g.addColorStop(0, GR.tone(.97)); g.addColorStop(.42, GR.tone(.95)); g.addColorStop(.75, GR.tone(.45)); g.addColorStop(1, GR.tone(.1));
    GR.fill(k.P, g, { th: k.a, id: 0 });
    if (i === 1) { const pts = []; for (let q = 0; q <= 20; q++) { const u = q / 20; pts.push([lerp(-70, 1240, u) + k.n[0] * up * lerp(155, 104, u) * (u < .98 ? 1 : .8), lerp(980, 704, u) + k.n[1] * up * lerp(155, 104, u)]); } oku_vurus(pts, 8, .02, .6); }
    if (i === 1) { tx.save(); tx.clip(K[0].P); tx.globalCompositeOperation = 'multiply'; tx.translate(10, 40); tx.fillStyle = GR.tone(.25); tx.fill(k.P); tx.restore(); }   // öndeki kolun gölgesi
  });
  return K;
}
// saç: düz siyah kütle; yumru yumru kıvırcık: her yumrunun ışık (sol üst) yanında sivrilen kâğıt rengi hilal
const CAB_PIP = makeCanvas(4, 4).getContext('2d');
// saç kütlesi: çerçevenin üstünü ve iki yanını kaplar; yüze bakan kenarı yumru yumru (kıvırcık)
function cab_sacYolu() {
  const B = CAB.sacTaban, Q = [], P = new Path2D();
  for (let i = 0; i < B.length - 1; i++) { const a = B[i], b = B[i + 1], n = Math.max(1, Math.round(Math.hypot(b[0] - a[0], b[1] - a[1]) / 62)); for (let k = 0; k < n; k++) Q.push([lerp(a[0], b[0], k / n), lerp(a[1], b[1], k / n)]); }
  Q.push(B[B.length - 1]); Q.reverse();
  CAB.yumru = [];
  P.moveTo(-200, 1160); P.lineTo(-200, -200); P.lineTo(2120, -200); P.lineTo(2120, 1160); P.lineTo(Q[0][0], Q[0][1]);
  const r = rng(17);
  for (let i = 0; i < Q.length - 1; i++) { const a = Q[i], b = Q[i + 1], m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
    let nx = -dy / l, ny = dx / l; if (nx * (950 - m[0]) + ny * (620 - m[1]) < 0) { nx = -nx; ny = -ny; }
    const bg = l * (.55 + .3 * r()); CAB.yumru.push([m[0] + nx * bg * .55, m[1] + ny * bg * .55, l * .5]); P.bezierCurveTo(a[0] + nx * bg, a[1] + ny * bg, b[0] + nx * bg, b[1] + ny * bg, b[0], b[1]); }
  P.closePath(); return P;
}
function cab_sac(SAC, seed, light, o = {}) {
  const { tx } = GR, r = rng(seed);
  // ışık yanında açılan ton: geçişte saçın akışını izleyen kavisli çizgiler (gravür saç taraması)
  const g = tx.createRadialGradient(light[0], light[1], 0, light[0], light[1], o.reach ?? 900);
  g.addColorStop(0, GR.tone(.42)); g.addColorStop(.4, GR.tone(.2)); g.addColorStop(.75, GR.tone(.02)); g.addColorStop(1, GR.tone(.02));
  GR.fill(SAC, g, { type: 'bend', ox: light[0], oy: light[1], a: 1.05, k: .0016, id: 0 });
  // yüze bakan yumrular: ışık yanında sivrilen hilal
  tx.save(); tx.clip(SAC);
  for (const [cx, cy, R] of CAB.yumru) {
    const d = Math.hypot(cx - light[0], cy - light[1]), k = clamp(1.1 - d / 900); if (k <= .15 || cx > 1100 || r() < .5) continue;
    const a0 = Math.atan2(light[1] - cy, light[0] - cx) + .5, sp = 1.4 + .6 * r(), pts = [];
    for (let i = 0; i <= 10; i++) { const an = a0 - sp / 2 + sp * i / 10; pts.push([cx + Math.cos(an) * R * .75, cy + Math.sin(an) * R * .75]); }
    oku_vurus(pts, 4 + 6 * k, .95, .25);
  }
  tx.restore();
}
// yakın kadraj: göz, kaş, alın, saç, kavuşturulmuş kollar. o: {yas (0..1 birikme), kay (0..1 süzülme), bg (false: zemin boyama)}
function cab_yakin(t, o = {}) {
  const { tx, px } = GR, G = CAB.goz;
  if (o.bg !== false) { tx.fillStyle = GR.tone(.03); tx.fillRect(-400, -400, W + 800, H + 800); }
  // yüz: soldan-üstten ışık; çizgiler alnın geniş kavsini izler; sağ yan karanlığa karışır
  const YZ = new Path2D(); spline(YZ, CAB.yuz, true, .85);
  let g = tx.createLinearGradient(560, 300, 1620, 640); g.addColorStop(0, GR.tone(.97)); g.addColorStop(.55, GR.tone(.93)); g.addColorStop(.78, GR.tone(.45)); g.addColorStop(1, GR.tone(.04));
  GR.fill(YZ, g, { type: 'rad', cx: 980, cy: 2100, id: 0 });
  tx.save(); tx.clip(YZ); tx.globalCompositeOperation = 'multiply';
  const mel = (x, y, rx, ry, rot, v0, f = .5) => { tx.save(); tx.translate(x, y); tx.rotate(rot); tx.scale(1, ry / rx); const q = tx.createRadialGradient(0, 0, 0, 0, 0, rx); q.addColorStop(0, GR.tone(v0)); q.addColorStop(f, GR.tone(v0)); q.addColorStop(1, GR.tone(1)); tx.fillStyle = q; tx.beginPath(); tx.arc(0, 0, rx, 0, TAU); tx.fill(); tx.restore(); };
  mel(G.x + 20, G.y - 2, 300, 150, -.06, .66, .45);          // göz çukuru
  mel(G.x + 40, 400, 230, 52, -.14, .42, .35);               // kaşın altı (öfke: kaş göze iner)
  mel(G.x + 70, 575, 190, 70, .05, .5, .4);                  // göz altı (damla için koyu zemin)
  mel(1120, 580, 70, 190, .1, .45, .3);                      // burun kökü
  tx.restore();
  // kaş: iç ucu aşağı ve içe (öfke), dış ucu yukarı; kaş arasında iki kısa çizgi
  oku_vurus([[1078, 402], [1000, 378], [900, 352], [800, 338], [710, 340], [646, 356]], 42, .02, .22);
  // göz: badem; üst kapak kalın ve aşağı iner (dik bakış), alt kapak ince; iris ışınsal taralı, tek parlak nokta
  const L = [G.x - G.w / 2, G.y], R = [G.x + G.w / 2, G.y + 18];
  const up = [[L[0], L[1]], [G.x - 90, G.y - 66], [G.x + 100, G.y - 62], [R[0], R[1]]], lo = [[R[0], R[1]], [G.x + 110, G.y + 66], [G.x - 90, G.y + 58], [L[0], L[1]]];
  const AK = new Path2D(); AK.moveTo(...up[0]); AK.bezierCurveTo(...up[1], ...up[2], ...up[3]); AK.bezierCurveTo(...lo[1], ...lo[2], ...lo[3]); AK.closePath();
  GR.fill(AK, GR.tone(.93), { th: 0, id: 0 });
  tx.save(); tx.clip(AK); px.save(); px.clip(AK);
  const ic = [G.x + 22, G.y + 8];
  const iris = new Path2D(); iris.arc(ic[0], ic[1], 74, 0, TAU); GR.fill(iris, GR.tone(.1), { th: 0, id: 0 });
  for (let k = 0; k < 7; k++) { const an = PI * .55 + k / 6 * PI * .9, r0 = 40 + (k % 2) * 6; oku_vurus([[ic[0] + Math.cos(an) * 70, ic[1] + Math.sin(an) * 70], [ic[0] + Math.cos(an) * r0, ic[1] + Math.sin(an) * r0]], 7, .85, .3); }
  const pp = new Path2D(); pp.arc(ic[0], ic[1], 32, 0, TAU); GR.fill(pp, GR.tone(.02), { th: 0, id: 0 });
  tx.globalCompositeOperation = 'multiply'; g = tx.createLinearGradient(0, G.y - 62, 0, G.y - 10); g.addColorStop(0, GR.tone(.04)); g.addColorStop(1, GR.tone(1)); tx.fillStyle = g; tx.fillRect(L[0], G.y - 80, G.w + 30, 72);   // kapağın gölgesi
  tx.restore(); px.restore();
  const hl = new Path2D(); hl.arc(ic[0] + 26, ic[1] - 26, 14, 0, TAU); GR.fill(hl, GR.tone(1), { th: 0, id: 0 });
  tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineCap = 'round';
  tx.lineWidth = 17; tx.beginPath(); tx.moveTo(L[0] - 10, L[1] + 4); tx.bezierCurveTo(G.x - 90, G.y - 70, G.x + 100, G.y - 66, R[0] + 12, R[1] - 4); tx.stroke();
  tx.lineWidth = 7; tx.beginPath(); tx.moveTo(G.x - 140, G.y - 64); tx.bezierCurveTo(G.x - 40, G.y - 112, G.x + 100, G.y - 104, G.x + 176, G.y - 50); tx.stroke();   // kapak kıvrımı
  tx.lineWidth = 6; tx.beginPath(); tx.moveTo(L[0] + 26, L[1] + 14); tx.bezierCurveTo(G.x - 70, G.y + 62, G.x + 80, G.y + 70, R[0] - 4, R[1] + 4); tx.stroke();
  tx.restore();
   // kirpikler (dış uç)
  // saç ve perçem
  const SAC = cab_sacYolu();
  cab_sac(SAC, 5, [380, -60], { reach: 900, step: 96 });
  const PC = new Path2D(); CAB.yumru = CAB.yumru || []; spline(PC, CAB.percem, true, .8); GR.fill(PC, GR.tone(.02), { th: 0, id: 0 });
  oku_vurus([[1196, 300], [1262, 420], [1300, 560], [1312, 690]], 10, .9, .3);
  // kollar (yüzün alt yarısını örter)
  cab_kollar();
  // gözyaşı: alt kapağın iç yanında birikir, sonra yanaktan kolun üstüne süzülür
  const yas = clamp(o.yas ?? 0), kay = clamp(o.kay ?? 0), D0 = [G.x + 86, G.y + 72], D1 = [G.x + 128, 650];
  if (yas > 0) {
    const q = E.io2(kay), pth = s => [lerp(D0[0], D1[0], s) + Math.sin(s * 3) * 10, lerp(D0[1], D1[1], s)], d = pth(q), r = 8 + 12 * E.out3(yas);
    if (kay > 0) { const pts = []; for (let k = 0; k <= 16; k++) pts.push(pth(k / 16 * q)); oku_vurus(pts, 15, .02, .75); oku_vurus(pts, 7, 1, .7); }
    const T = new Path2D(); T.moveTo(d[0], d[1] - r * 1.9); T.bezierCurveTo(d[0] + r * .5, d[1] - r * 1.1, d[0] + r, d[1] - r * .4, d[0] + r, d[1]); T.arc(d[0], d[1], r, 0, PI); T.bezierCurveTo(d[0] - r, d[1] - r * .4, d[0] - r * .5, d[1] - r * 1.1, d[0], d[1] - r * 1.9); T.closePath();
    tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 9; tx.stroke(T); tx.restore();
    GR.fill(T, GR.tone(1), { th: 0, id: 0 });
    const cr = new Path2D(); cr.arc(d[0], d[1], r * .66, .25, PI * .75); tx.save(); tx.strokeStyle = GR.tone(.15); tx.lineWidth = Math.max(3.5, r * .24); tx.lineCap = 'round'; tx.stroke(cr); tx.restore();
  }
}
// ── P133 (L03): göze yaklaşma; gözde damla birikir ve süzülür ──
plan('P133', (ctx, st) => {
  const t = st.t, tG = Wd('L03', 'gözleri'), tD = Wd('L03', 'dolu');
  const cam = camLerp({ cx: 940, cy: 520, z: 1 }, { cx: 900, cy: 500, z: 1.06 }, oku_u(t, st.at, st.at + Math.max(6, st.d)), E.io2);
  levha(ctx, cam, () => cab_yakin(t, { yas: oku_u(t, tG, tD + .2), kay: oku_u(t, tD + .25, tD + 2.2) }), [.03, 0, 1]);
}, { tr: { type: 'fade', dur: .8 } });

// ── P132 (L02): müze çerçevesinde levha ──
function cab_cerceve(x0, y0, x1, y1) {   // müze çerçevesi: koyu pervaz, iç kenarda kâğıt rengi ince yiv, pervazda boncuk sırası
  const { tx } = GR, B = 52, O = new Path2D(); O.rect(x0 - B, y0 - B, x1 - x0 + 2 * B, y1 - y0 + 2 * B); O.rect(x0, y0, x1 - x0, y1 - y0);
  GR.fill(O, GR.tone(.03), { th: 0, id: 0 }, 'evenodd');
  kit_kutu(x0 - B + 10, y0 - B + 10, x1 + B - 10, y1 + B - 10, 3, .95); kit_kutu(x0 - 9, y0 - 9, x1 + 9, y1 + 9, 3, .95);
  const dot = (x, y) => { const P = new Path2D(); P.arc(x, y, 4.5, 0, TAU); GR.fill(P, GR.tone(.95), { th: 0, id: 0 }); };
  const m = B * .55;
  for (let x = x0 - m + 14; x < x1 + m - 8; x += 26) { dot(x, y0 - m); dot(x, y1 + m); }
  for (let y = y0 - m + 26; y < y1 + m - 14; y += 26) { dot(x0 - m, y); dot(x1 + m, y); }
}
function cab_tablo(t) {
  const { tx } = GR, X0 = 470, Y0 = 150, X1 = 1450, Y1 = 720;
  kit_cerceve();
  cab_cerceve(X0, Y0, X1, Y1);
  GR.save(); { const C = new Path2D(); C.rect(X0, Y0, X1 - X0, Y1 - Y0); GR.tx.clip(C); GR.px.clip(C); GR.ox.clip(C); }
  // gök: koyu, sağ üstte açılan bulut ışığı; kayalar altta
  const g = tx.createLinearGradient(0, Y0, 0, Y1); g.addColorStop(0, GR.tone(.2)); g.addColorStop(.6, GR.tone(.06)); g.addColorStop(1, GR.tone(.03));
  tx.fillStyle = g; tx.fillRect(X0, Y0, X1 - X0, Y1 - Y0);
  PR.glow(1330, 200, 30, 330, 1, .75);
  PR.cloud({ x: 1180, y: 250, w: 520, h: 130, seed: 41, lit: [.6, -.7], base: .05, hi: .7, core: .04, n: 3, drift: 0 });
  // kanatlar: başın arkasından iki yana açılan koyu kütle
  for (const [side, P] of [[-1, { span: 520, open: .62, lift: .25, droop: .55, rot: -.25, seed: 51, root: .1 }], [1, { span: 470, open: .55, lift: .15, droop: .7, rot: .3, seed: 52, root: .12 }]]) {
    GR.frame(960 + side * 70, 400, P.rot, side, 1); KN.feathered(Object.assign({ dark: .92, rim: .7, ruin: .2, t: 0, lit: [.6 * side, -.8] }, P)); GR.unframe();
  }
  // figür grubu (yakın kadrajın küçültülmüşü): baş ve kollar
  GR.frame(960 - 1000 * .36, 430 - 520 * .36, 0, 1, .36); cab_yakin(t, { bg: false }); GR.unframe();
  // kaya: altta, kolların altını örter (gövde görünmez)
  const RK = [[X0 - 20, 640], [600, 610], [760, 668], [900, 640], [1080, 676], [1240, 630], [1460, 650], [1470, Y1 + 20], [X0 - 20, Y1 + 20]];
  const RP = PR.rock(RK, { lit: [.6, -.8], hi: .3, mid: .06, lo: .03, seed: 7, th: -.9, rim: 5, facets: 9 });
  GR.restore();
}
plan('P132', (ctx, st) => levha(ctx, camLerp({ cx: 950 }, { cx: 970 }, st.p, E.sine), () => {
  cab_tablo(st.t);
  kit_yaz('Alexandre Cabanel · Düşmüş Melek, 1847', 960, 852, { f: 'a', px: 58, a: kit_a(st.t, Wd('L02', 'aleksandr') - .3, 1.2), wipe: true });
}, [KIT_K, 0, 1]), { tr: { type: 'fade', dur: .8 } });

// ═════════════════ K11: küçülme merdiveni ═════════════════
// Yedi basamak soldan sağa iner; her basamakta bir siluet, sözle tek tek mürekkeplenir (yanar). Basamağın koyu yüzünde ad.
const OKU_BAS = (() => { const n = 7, x0 = 220, x1 = 1760, y0 = 410, dy = 62, w = (x1 - x0) / n; return Array.from({ length: n }, (_, i) => ({ x0: x0 + i * w, x1: x0 + (i + 1) * w, y: y0 + i * dy, cx: x0 + (i + .5) * w })); })();
function oku_merdiven() {
  const P = new Path2D(), B = OKU_BAS, pts = [[B[0].x0, 1100]];
  for (const b of B) pts.push([b.x0, b.y], [b.x1, b.y]);
  pts.push([B[B.length - 1].x1, 1100]); poly(P, pts, true);
  GR.fill(P, GR.tone(.03), { th: 0, id: 0 });
  for (const b of B) kit_hat(b.x0 + 4, b.y + 9, b.x1 - 4, b.y + 9, 3, .95);   // basamak burnu: ince kâğıt çizgisi
  return P;
}
function oku_kurbaga(x, y, s) {   // yandan oturan kurbağa (sağa bakar): basık gövde, göz tümseği, katlanmış iri arka bacak, ince ön bacak
  const L = (a, b) => [x + a * s, y + b * s], P = new Path2D();
  spline(P, [L(-.95, -.1), L(-1.0, -.45), L(-.75, -.72), L(-.2, -.8), L(.3, -.85), L(.48, -1.05), L(.66, -1.06), L(.78, -.88), L(1.05, -.7), L(1.22, -.5), L(1.1, -.38), L(.7, -.32), L(.62, -.1)], true, .7);
  const K = new Path2D(); spline(K, [L(-.95, -.2), L(-.55, -.62), L(-.15, -.45), L(-.3, -.1), L(.2, -.08), L(.32, 0), L(-.9, 0)], true, .6); P.addPath(K);   // arka bacak
  const F = new Path2D(); poly(F, [L(.62, -.35), L(.76, -.33), L(.8, 0), L(.98, 0), L(.98, .05), L(.6, .05)], true); P.addPath(F);   // ön bacak
  return P;
}
function oku_yilan(x, y, s, bak = 0) {   // çöreklenmiş yılan; baş yukarı kalkık (bak: 0 ileri … 1 yukarı-sola)
  const pts = [], n = 60;
  for (let i = 0; i <= n; i++) { const u = i / n, a = u * TAU * 1.15, r = s * (1 - .5 * u); pts.push([x + Math.cos(a) * r * 1.3, y - Math.abs(Math.sin(a)) * r * .25 - u * s * .1]); }
  const hx = x + s * .2, hb = [hx - s * .25 * bak, y - s * (1.2 + .5 * bak)];
  for (let i = 1; i <= 12; i++) { const u = i / 12; pts.push([lerp(pts[n][0], hb[0], u) + Math.sin(u * PI) * s * .35, lerp(pts[n][1], hb[1], u)]); }
  return { pts, head: hb, dir: [-.6 * bak + .9 * (1 - bak), -.8 * bak + .1] };
}
function oku_yilanCiz(Y, s, v = .02) {
  const { tx } = GR, pts = Y.pts, A = [], B = [], n = pts.length;
  for (let i = 0; i < n; i++) { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n - 1, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, w = s * lerp(.06, .2, Math.min(1, i / (n * .5)) * (i > n - 10 ? .8 : 1));
    A.push([pts[i][0] - dy / l * w, pts[i][1] + dx / l * w]); B.push([pts[i][0] + dy / l * w, pts[i][1] - dx / l * w]); }
  const P = new Path2D(); poly(P, [...A, ...B.reverse()], true);
  const d = Y.dir, l = Math.hypot(d[0], d[1]) || 1, ux = d[0] / l, uy = d[1] / l;
  P.moveTo(Y.head[0] + ux * s * .45, Y.head[1] + uy * s * .45); P.ellipse(Y.head[0] + ux * s * .15, Y.head[1] + uy * s * .15, s * .3, s * .19, Math.atan2(uy, ux), 0, TAU);
  GR.fill(P, GR.tone(v), { th: 0, id: 0 });
  return P;
}
// pencere: dikmeli küçük pencere çerçevesi (yalnız pencere; içi boş)
function oku_pencere(x, y, w, h) { kit_kutu(x, y, x + w, y + h, 6); kit_hat(x + w / 2, y, x + w / 2, y + h, 5); kit_hat(x, y + h * .45, x + w, y + h * .45, 5); const S = new Path2D(); S.rect(x - 10, y + h, w + 20, 12); kit_dol(S, .02); }
// yedi siluet; a[i]: 0..1 mürekkeplenme (soluk, taralı → düz siyah)
function oku_siluetler(a, t, o = {}) {
  const B = OKU_BAS, f = (i, J, op) => kit_fig(J, Object.assign({ lum: 0, lit: [-.5, -.8], t, lines: 0, eye: 0, wind: .4, seed: 3 + i }, op), .2 + .8 * E.sine(a[i]));
  const G = i => B[i].y + 2;
  // 1 kahraman: zırhlı başmelek, mızrak dik, kanatlı
  { const h = 31, b = B[0], J = SF.rig({ x: b.cx, y: G(0) - 3.95 * h, h, facing: 1, twist: .35, head: .12, armN: [.5, -.9], armF: [.15, .2] });
    const al = .2 + .8 * E.sine(a[0]); GR.tx.save(); GR.tx.globalAlpha = al;
    for (const [side, P] of [[-1, { span: 230, open: .7, lift: .7, droop: .2, rot: -.2, seed: 61, root: .1 }], [1, { span: 270, open: .6, lift: .6, droop: .25, rot: .15, seed: 62, root: .12 }]]) {
      const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
      GR.frame(sh[0] - side * h * .25, sh[1] + h * .15, P.rot, side, 1); KN.feathered(Object.assign({ dark: .93, rim: 0, ruin: 0, t: 0, lit: [.5 * side, -.8] }, P)); GR.unframe(); }
    GR.tx.restore();
    f(0, J, { spear: { grip: 'N', ang: .02, len: 8, up: .7 }, cloak: 1 }); }
  // 2 general: pelerin, mareşal asası
  { const h = 25, b = B[1], J = SF.rig({ x: b.cx, y: G(1) - 3.95 * h, h, facing: 1, twist: .4, head: .05, armN: [1.2, -.5], armF: [.25, .9] }); f(1, J, { cloak: 1.3 });
    const w = J.wrN, P = new Path2D(); poly(P, [[w[0] - 6, w[1] + 10], [w[0] + 36, w[1] - 34], [w[0] + 41, w[1] - 29], [w[0] - 1, w[1] + 15]], true); P.moveTo(w[0] + 44, w[1] - 33); P.arc(w[0] + 39, w[1] - 32, 6, 0, TAU); GR.tx.save(); GR.tx.globalAlpha = .2 + .8 * E.sine(a[1]); kit_dol(P, .02); GR.tx.restore(); }
  // 3 politikacı: kürsüde, kol açık
  { const h = 20, b = B[2], J = SF.rig({ x: b.cx - 14, y: G(2) - 3.95 * h, h, facing: 1, twist: .3, head: .15, armN: [2.2, .3], armF: [.6, .7] }); f(2, J, { cloak: false });
    const K = new Path2D(); poly(K, [[b.cx + 2, G(2)], [b.cx + 12, G(2) - 92], [b.cx + 66, G(2) - 92], [b.cx + 76, G(2)]], true); poly(K, [[b.cx - 2, G(2) - 104], [b.cx + 82, G(2) - 104], [b.cx + 80, G(2) - 90], [b.cx, G(2) - 90]], true);
    GR.tx.save(); GR.tx.globalAlpha = .2 + .8 * E.sine(a[2]); kit_dol(K, .02); GR.tx.restore(); kit_hat(b.cx + 4, G(2) - 97, b.cx + 78, G(2) - 97, 3, .95); }
  // 4 casus: pelerinli, öne eğik, sinsi adım
  { const h = 16.5, b = B[3], J = SF.rig({ x: b.cx, y: G(3) - 3.6 * h, h, facing: 1, twist: .5, lean: .55, head: .25, armN: [.9, 1.3], armF: [.4, 1.1], legN: [.7, -.9], legF: [-.4, -.5] }); f(3, J, { cloak: 1.6, wind: .2 }); }
  // 5 pencereden bakan biçim: iki büklüm, pencerenin önünde
  { const h = 13, b = B[4], J = SF.rig({ x: b.cx - 34, y: G(4) - 3.3 * h, h, facing: 1, twist: .6, lean: .85, head: .6, armN: [1.5, .4], armF: [1.2, .6], legN: [.8, -1.3], legF: [.3, -1.2] });
    GR.tx.save(); GR.tx.globalAlpha = .2 + .8 * E.sine(a[4]); oku_pencere(b.cx + 18, G(4) - 128, 66, 86); GR.tx.restore(); f(4, J, { cloak: 1.3 }); }
  // 6 kurbağa
  { const b = B[5]; GR.tx.save(); GR.tx.globalAlpha = .2 + .8 * E.sine(a[5]); kit_dol(oku_kurbaga(b.cx - 10, G(5), 52), .02); GR.tx.restore(); }
  // 7 yılan
  { const b = B[6]; GR.tx.save(); GR.tx.globalAlpha = .2 + .8 * E.sine(a[6]); oku_yilanCiz(oku_yilan(b.cx - 10, G(6) - 10, 58, o.bak ?? 0), 58); GR.tx.restore(); }
}
const OKU_AD = ['kahraman', 'general', 'politikacı', 'casus', null, 'kurbağa', 'yılan'];
function oku_k11(st) {
  const t = st.t, tw = [['kahramandan', 0], ['generale', 0], ['politikacıya', 0], ['casusa', 0], ['bakan', 0], ['kurbağaya', 0], ['yılana', 0]].map(([w]) => Wd('K11', w));
  const a = tw.map(x => kit_a(t, x - .25, .9));
  kit_cerceve();
  kit_kirp(() => { oku_merdiven(); oku_siluetler(a, t); });
  OKU_AD.forEach((s, i) => { if (s) kit_yaz(s, OKU_BAS[i].cx, OKU_BAS[i].y + 64, { f: 'a', px: 50, v: .975, bg: .03, a: a[i], wipe: true }); });
}
plan('P124', (ctx, st) => levha(ctx, camLerp({ cx: 940 }, { cx: 980 }, st.p, E.sine), () => oku_k11(st), [KIT_K, 0, 1]), { tr: KIT_TR });
