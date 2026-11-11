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

// ═════════════════ bölüm kartları (açık ve koyu levha; yazı ton katmanına basılır, sahne ışıkla açılır) ═════════════════
function oku_kart(st, baslik, soru, koyu, tBas, tSoru, motif) {
  const t = st.t, v = koyu ? .975 : .02, bg = koyu ? .03 : KIT_K;
  kit_cerceve(koyu ? .95 : .02);
  if (motif) motif();
  kit_cizgi(960, 330, 230, { v, a: kit_a(t, tBas - .4, 1) });
  kit_yaz(baslik, 960, 440, { f: 'b', px: 104, ls: 16, v, bg, a: kit_a(t, tBas - .2, 1.2), wipe: true });
  kit_yaz(soru, 960, 590, { f: 'a', px: 72, v, bg, a: kit_a(t, tSoru - .2, 1), wipe: true });
  oku_isikAc(oku_u(t, st.at, st.at + 1.4), 960, 480);
}
plan('P119', (ctx, st) => levha(ctx, null, () => oku_kart(st, 'İKİ OKUMA', 'Bu destanın kahramanı kim?', false, st.at + .3, Wd('K05', 'bu')), [KIT_K, 0, 1]),
  { tr: { type: 'black', dur: 1.4, end: true } });
plan('P131', (ctx, st) => levha(ctx, null, () => oku_kart(st, 'BİR DAMLA YAŞ', 'Peki ya o gözyaşları?', true, st.at + .3, Wd('L01', 'peki'), () => {
  const x = 960, y = 230, r = 16, T = new Path2D(); T.moveTo(x, y - r * 2.2); T.bezierCurveTo(x + r * .6, y - r * 1.2, x + r, y - r * .5, x + r, y); T.arc(x, y, r, 0, PI); T.bezierCurveTo(x - r, y - r * .5, x - r * .6, y - r * 1.2, x, y - r * 2.2); T.closePath();
  GR.fill(T, GR.tone(.975), { th: 0, id: 0 });
}), [.03, 0, 1]), { tr: { type: 'black', dur: 1.4, end: true } });

// ═════════════════ K07: Blake'in masası ═════════════════
// ilmekli serbest çizgi (uzamış sikloit) bir yol boyunca; frac: 0..1 çizilen kısım; keskin üst katmana
function oku_ilmek(c, pts, R, K, frac, w = 3) {
  const S = [0]; for (let i = 1; i < pts.length; i++) S.push(S[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const Ltot = S[S.length - 1], at = s => { let i = 1; while (i < S.length - 1 && S[i] < s) i++; const u = (s - S[i - 1]) / ((S[i] - S[i - 1]) || 1), a = pts[i - 1], b = pts[i], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1; return [lerp(a[0], b[0], u), lerp(a[1], b[1], u), dx / l, dy / l]; };
  const th1 = Ltot / K * frac; if (th1 <= 0) return;
  c.save(); c.strokeStyle = GR.inkCol; c.lineWidth = w; c.lineCap = 'round'; c.lineJoin = 'round'; c.beginPath();
  for (let th = 0; th <= th1; th += .2) { const [x, y, tx, ty] = at(th * K), sx = x - tx * R * Math.sin(th) - ty * R * (1 - Math.cos(th)), sy = y - ty * R * Math.sin(th) + tx * R * (1 - Math.cos(th)); th ? c.lineTo(sx, sy) : c.moveTo(sx, sy); }
  c.stroke(); c.restore();
}
const oku_daire = (cx, cy, r, n = 16) => Array.from({ length: n + 1 }, (_, i) => [cx + Math.cos(i / n * TAU - PI / 2) * r, cy + Math.sin(i / n * TAU - PI / 2) * r]);
// melek (sert): cüppe, baş, dimdik iki kanat; dik ve sık düz çizgilerle (soldan sağa sırayla) doldurulur
function oku_melekSert(c, x, y, s, frac) {
  const L = (a, b) => [x + a * s, y + b * s], P = new Path2D();
  poly(P, [L(-.35, 1), L(-.22, -.55), L(.22, -.55), L(.35, 1)], true);
  P.moveTo(...L(.2, -.82)); P.arc(...L(0, -.82), .2 * s, 0, TAU);
  poly(P, [L(-.25, -.5), L(-.62, -1.45), L(-.5, .45), L(-.28, .2)], true); poly(P, [L(.25, -.5), L(.62, -1.45), L(.5, .45), L(.28, .2)], true);
  const x0 = x - .65 * s, x1 = x + .65 * s, n = Math.floor((x1 - x0) / 9);
  c.save(); c.clip(P); c.strokeStyle = GR.inkCol; c.lineWidth = 3; c.beginPath();
  for (let i = 0; i < n * frac; i++) { const xx = x0 + i * 9 + 4; c.moveTo(xx, y - 1.6 * s); c.lineTo(xx, y + 1.05 * s); }
  c.stroke(); c.restore();
  if (frac > .05) { c.save(); c.globalAlpha = clamp(frac * 3); c.strokeStyle = GR.inkCol; c.lineWidth = 3.5; c.stroke(P); c.restore(); }
}
// şeytan (serbest): yarasa kanatlı figür, kıvrak ilmekli çizgilerle
function oku_seytanSerbest(c, x, y, s, frac, seed) {
  const L = (a, b) => [x + a * s, y + b * s], r = rng(seed);
  const govde = [L(0, -.6), L(.3, -.3), L(.25, .4), L(.45, 1), L(-.45, 1), L(-.25, .4), L(-.3, -.3), L(0, -.6)];
  const bas = oku_daire(x, y - .85 * s, .22 * s, 12), boynuz = [L(-.16, -1.0), L(-.3, -1.3), L(-.06, -1.06)], boynuz2 = [L(.16, -1.0), L(.3, -1.3), L(.06, -1.06)];
  const kanat = sd => [L(.25 * sd, -.3), L(.9 * sd, -1.2), L(1.25 * sd, -.75), L(1.05 * sd, -.55), L(1.12 * sd, -.2), L(.85 * sd, -.1), L(.85 * sd, .2), L(.35 * sd, .1)];
  const parts = [bas, boynuz, boynuz2, govde, kanat(-1), kanat(1)];
  parts.forEach((p, i) => oku_ilmek(c, p, 9 + 4 * r(), 5.5, clamp(frac * parts.length - i), 3));
  // çevresinde serbest kıvrımlar (alev gibi)
  for (let k = 0; k < 3; k++) { const a = r() * TAU, cx = x + Math.cos(a) * 1.2 * s, cy = y + .3 * s + Math.sin(a) * .5 * s, sp = []; for (let q = 0; q <= 20; q++) { const u = q / 20; sp.push([cx + Math.cos(u * 5 + a) * 26 * (1 - u), cy - u * 70 + Math.sin(u * 5 + a) * 14]); }
    oku_ilmek(c, sp, 6, 5, clamp(frac * 3 - 2 - k * .2), 3); }
}
function oku_k07(st) {
  const t = st.t, { tx, ox } = GR;
  // masa: koyu ahşap, kâğıt rengi seyrek damar vuruşları
  const M = new Path2D(); M.rect(62, 62, W - 124, H - 124); GR.fill(M, GR.tone(.06), { th: -.08, id: 4 });
  { const r = rng(71); for (let i = 0; i < 9; i++) { const y = 110 + i * 105 + r() * 30, x0 = 80 + r() * 300, pts = []; for (let k = 0; k <= 20; k++) { const u = k / 20; pts.push([x0 + u * (500 + r() * 400), y + Math.sin(u * 4 + i) * 8 - u * 30]); } oku_vurus(pts, 5, .9, .2); } }
  kit_cerceve(.95);
  // açık defter (iki sayfa), masaya gölge
  const Bk = (dx, dy) => { const P = new Path2D(); spline(P, [[300 + dx, 168 + dy], [800 + dx, 150 + dy], [820 + dx, 160 + dy], [1320 + dx, 150 + dy], [1320 + dx, 752 + dy], [820 + dx, 742 + dy], [800 + dx, 752 + dy], [300 + dx, 760 + dy]], true, .25); return P; };
  GR.fill(Bk(18, 20), GR.tone(.03), { th: 0, id: 0 });
  const Bp = Bk(0, 0); GR.fill(Bp, GR.tone(.975), { th: 0, id: 1 });
  tx.save(); tx.clip(Bp); tx.globalCompositeOperation = 'multiply'; const g = tx.createLinearGradient(760, 0, 860, 0); g.addColorStop(0, GR.tone(1)); g.addColorStop(.5, GR.tone(.55)); g.addColorStop(1, GR.tone(1)); tx.fillStyle = g; tx.fillRect(740, 100, 140, 700); tx.restore();
  tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 4; tx.stroke(Bp); tx.restore();
  // bakır levha ve kalem (burin)
  const Cu = new Path2D(); Cu.rect(1400, 180, 380, 320);
  const cg = tx.createLinearGradient(1400, 180, 1780, 500); cg.addColorStop(0, GR.tone(.8)); cg.addColorStop(.5, GR.tone(.5)); cg.addColorStop(1, GR.tone(.68));
  GR.fill(Cu, cg, { th: -.6, id: 0 }); tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 4; tx.stroke(Cu); tx.restore();
  { const P = new Path2D(); poly(P, [[1450, 600], [1700, 380], [1708, 388], [1462, 610]], true); P.moveTo(1488, 590); P.ellipse(1470, 604, 30, 20, -.72, 0, TAU); GR.fill(P, GR.tone(.03), { th: 0, id: 0 }); oku_vurus([[1478, 586], [1690, 392]], 3, .9, .5); }
  // künye plakası
  const Pl = new Path2D(); Pl.rect(470, 786, 680, 88); GR.fill(Pl, GR.tone(.975), { th: 0, id: 1 }); kit_kutu(470, 786, 1150, 874, 4); kit_kutu(482, 798, 1138, 862, 2.6);
  kit_yaz('WILLIAM BLAKE · 1793', 810, 830, { f: 'b', px: 42, w: 700, ls: 6, a: kit_a(t, Wd('K07', 'vilyım') - .3, 1.1), wipe: true });
  // çizimler: solda sert çizgili melekler ("zincirliydi"), sağda serbest çizgili şeytanlar ("özgür")
  const fa = oku_u(t, Wd('K07', 'melekleri') - .3, Wd('K07', 'zincirliydi', 0, true) + .3), fs = oku_u(t, Wd('K07', 'şeytanları') - .2, Wd('K07', 'özgür', 0, true) + 1.2);
  [[420, 470], [550, 470], [680, 470]].forEach(([x, y], i) => oku_melekSert(ox, x, y, 120, clamp(fa * 3 - i)));
  [[960, 480, 3], [1180, 470, 8]].forEach(([x, y, sd], i) => oku_seytanSerbest(ox, x, y, 100, clamp(fs * 2 - i), sd));
}
plan('P121', (ctx, st) => levha(ctx, camLerp({ cx: 940 }, { cx: 990 }, st.p, E.sine), () => oku_k07(st), [.06, 0, 1]), { tr: KIT_TR });

// ═════════════════ K10: Lewis'in kitabının kapağı (portre yok) ═════════════════
function oku_k10(st) {
  const t = st.t, { tx } = GR, X0 = 660, X1 = 1260, Y0 = 110, Y1 = 860;
  kit_cerceve();
  const Sh = new Path2D(); Sh.rect(X0 + 22, Y0 + 22, X1 - X0, Y1 - Y0); GR.fill(Sh, GR.tone(.4), { th: -.8, id: 0 });
  const C = new Path2D(); C.rect(X0, Y0, X1 - X0, Y1 - Y0); GR.fill(C, GR.tone(.04), { th: 0, id: 0 });
  const Sp = new Path2D(); Sp.rect(X0, Y0, 46, Y1 - Y0); GR.fill(Sp, GR.tone(.02), { th: 0, id: 0 });
  kit_hat(X0 + 46, Y0, X0 + 46, Y1, 3, .9);
  kit_kutu(X0 + 76, Y0 + 30, X1 - 30, Y1 - 30, 4, .95); kit_kutu(X0 + 90, Y0 + 44, X1 - 44, Y1 - 44, 2.6, .95);
  const xc = (X0 + 46 + X1) / 2, k = { v: .975, bg: .04 };
  kit_yaz('C. S. LEWIS', xc, 260, { f: 'b', px: 66, ls: 8, ...k, a: kit_a(t, Wd('K10', 'si') - .2, 1.2), wipe: true });
  kit_cizgi(xc, 360, 120, { v: .95, a: kit_a(t, Wd('K10', 'luis'), 1) });
  kit_yaz('Kayıp Cennet\'e', xc, 470, { f: 'a', px: 72, ...k, a: kit_a(t, Wd('K10', 'kayıp') - .2, 1), wipe: true });
  kit_yaz('Önsöz', xc, 560, { f: 'a', px: 72, ...k, a: kit_a(t, Wd('K10', 'önsöz') - .2, .9), wipe: true });
  kit_yaz('1942', xc, 730, { f: 'b', px: 48, w: 600, ls: 10, ...k, a: kit_a(t, Wd('K10', 'önsöz') + .4, .9), wipe: true });
}
plan('P123', (ctx, st) => levha(ctx, null, () => oku_k10(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ═════════════════ K12: yılan en üste bakar ═════════════════
function oku_k12(st) {
  const t = st.t, bak = E.io2(oku_u(t, Wd('K12', 'yılana') - .2, Wd('K12', 'girmeden') + .6));
  kit_cerceve();
  kit_kirp(() => { oku_merdiven(); oku_siluetler([1, 0, 0, 0, 0, 0, 1], t, { bak }); });
  if (bak > .3) {   // bakış çizgisi: yılanın başından en üst basamağa seyrek noktalar
    const B = OKU_BAS, a = [B[6].cx - 10, B[6].y - 10 - 58 * (1.2 + .5 * bak)], b = [B[0].cx + 40, B[0].y - 140], { ox } = GR, n = 26;
    ox.save(); ox.fillStyle = GR.inkCol; for (let i = 2; i < n * E.io2(clamp((bak - .3) / .7)); i++) { const u = i / n; ox.beginPath(); ox.arc(lerp(a[0], b[0], u), lerp(a[1], b[1], u) - Math.sin(u * PI) * 120, 3.6, 0, TAU); ox.fill(); } ox.restore();
  }
  kit_yaz('“yükseldiği kadar alçalır”', 1240, 210, { f: 'a', px: 80, a: kit_a(t, Wd('K12', 'yükseldiği') - .5, 1.2), wipe: true });
}
plan('P125', (ctx, st) => levha(ctx, camLerp({ cx: 980 }, { cx: 940 }, st.p, E.sine), () => oku_k12(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ═════════════════ K13: devrilmiş taç | taht kuran melek ═════════════════
function oku_taht(x, yG, s, ad, mucevher) {   // sade, yüksek arkalıklı, basamaklı taht (belirli bir kültürü çağrıştırmaz)
  const L = (a, b) => [x + a * s, yG + b * s], P = new Path2D();
  const nb = Math.round(3 * clamp(ad));
  for (let i = 0; i < nb; i++) poly(P, [L(-1.3 + i * .22, -i * .22), L(1.3 - i * .22, -i * .22), L(1.3 - i * .22, -(i + 1) * .22), L(-1.3 + i * .22, -(i + 1) * .22)], true);
  const yb = -.66; poly(P, [L(-.62, yb), L(-.62, yb - .7), L(-.75, yb - .72), L(-.75, yb - .82), L(.75, yb - .82), L(.75, yb - .72), L(.62, yb - .7), L(.62, yb)], true);   // oturak ve kolluklar
  poly(P, [L(-.55, yb - .8), L(-.55, yb - 2.9), L(-.4, yb - 3.25), L(0, yb - 3.45), L(.4, yb - 3.25), L(.55, yb - 2.9), L(.55, yb - .8)], true);              // yüksek arkalık
  GR.fill(P, GR.tone(.03), { th: 0, id: 0 });
  for (let i = 0; i < nb; i++) kit_hat(L(-1.3 + i * .22 + .04, 0)[0], L(0, -i * .22 - .03)[1], L(1.3 - i * .22 - .04, 0)[0], L(0, -i * .22 - .03)[1], 3, .95);
  kit_hat(L(-.5, 0)[0], L(0, yb - 2.95)[1], L(.5, 0)[0], L(0, yb - 2.95)[1], 3, .95);
  if (mucevher > 0) { const r = rng(5); for (let i = 0; i < 9; i++) { const pos = [r(), r()]; if (i / 9 > mucevher) continue; const p = L((pos[0] - .5) * .8, yb - 1.1 - pos[1] * 1.9), D = new Path2D(); poly(D, [[p[0], p[1] - 9], [p[0] + 7, p[1]], [p[0], p[1] + 9], [p[0] - 7, p[1]]], true); GR.fill(D, GR.tone(.975), { th: 0, id: 0 }); } }
  return { oturak: L(0, yb - .82) };
}
function oku_k13(st) {
  const t = st.t, { tx } = GR;
  kit_cerceve();
  kit_yaz('Blake mi, Lewis mi?', 960, 168, { f: 'a', px: 84, a: kit_a(t, Wd('K13', 'bleyk') - .2, 1.2), wipe: true });
  kit_hat(140, 800, 1780, 800, 4);
  // sol: yere devrilmiş, yan yatmış taç
  const ac = kit_a(t, Wd('K13', 'kralların') - .3, 1.1);
  if (ac > 0) { GR.save(); GR.frame(520, 730, -1.32 + .25 * (1 - E.out3(ac)), 1, 1); tx.globalAlpha = ac; const Cp = kit_tac(0, 0, 115); GR.fill(Cp, GR.tone(.975), { th: 0, id: 1 }); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 7; tx.lineJoin = 'round'; tx.stroke(Cp); kit_hat(-115, 8, 115, 8, 6); GR.unframe(); GR.restore();
    const S = new Path2D(); S.ellipse(560, 812, 170, 12, 0, 0, TAU); GR.fill(S, GR.tone(.35), { th: 0, id: 0 }); }
  // sağ: taht ve üstünde kanatlı koyu melek; taht 'kendine'den 'kuruyor'a basamak basamak kurulur, mücevherler 'hazinelerinden'de
  const am = kit_a(t, Wd('K13', 'meleği') - .2, 1.2);
  if (am > 0) {
    GR.tx.save(); GR.tx.globalAlpha = am;
    const T = oku_taht(1450, 800, 140, .34 + .66 * oku_u(t, Wd('K13', 'kendine'), Wd('K13', 'kuruyor')), oku_u(t, Wd('K13', 'hazinelerinden') - .2, Wd('K13', 'taht')));
    const h = 38, J = SF.rig({ x: 1460, y: T.oturak[1] - 6, h, facing: -1, twist: .4, head: .15, armN: [.9, .4], armF: [.6, .7], legN: [1.45, -1.45], legF: [1.35, -1.4] });
    for (const [side, P] of [[-1, { span: 360, open: .55, lift: .65, droop: .3, rot: -.15, seed: 71, root: .1 }], [1, { span: 330, open: .5, lift: .55, droop: .35, rot: .15, seed: 72, root: .12 }]]) {
      const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
      GR.frame(sh[0] - side * h * .25, sh[1] + h * .15, P.rot, side, 1); KN.feathered(Object.assign({ dark: .93, rim: 0, ruin: .1, t: 0, lit: [.5 * side, -.8] }, P)); GR.unframe(); }
    GR.tx.restore();
    kit_fig(J, { lum: 0, lit: [-.6, -.8], t, legs: true, cloak: 1.1, lines: 0, seed: 9 }, am);
  }
}
plan('P126', (ctx, st) => levha(ctx, null, () => oku_k13(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ═════════════════ K15: kırılan zincir; halkalar bir taht biçiminde yeniden dizilir ═════════════════
const OKU_ZN = 53, OKU_ZK = 27;   // halka sayısı, kırılma yeri
function oku_yolNokta(P, u) { const S = [0]; for (let i = 1; i < P.length; i++) S.push(S[i - 1] + Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1])); const s = u * S[S.length - 1]; let i = 1; while (i < S.length - 1 && S[i] < s) i++; const v = (s - S[i - 1]) / ((S[i] - S[i - 1]) || 1); return [lerp(P[i - 1][0], P[i][0], v), lerp(P[i - 1][1], P[i][1], v), Math.atan2(P[i][1] - P[i - 1][1], P[i][0] - P[i - 1][0])]; }
function oku_halka(x, y, a, i) {   // sırayla yüzü ve yanı görünen halka
  const { tx } = GR; tx.save(); tx.translate(x, y); tx.rotate(a);
  const P = new Path2D(); if (i % 2 === 0) { P.ellipse(0, 0, 25, 15, 0, 0, TAU); P.ellipse(0, 0, 15, 6, 0, 0, TAU); } else { P.roundRect(-25, -6, 50, 12, 6); }
  GR.fill(P, GR.tone(.02), { th: a, id: 0 }, 'evenodd'); tx.restore();
}
function oku_k15(st) {
  const t = st.t;
  kit_cerceve();
  const tK = Wd('K15', 'özgürlükleri'), kr = E.out3(oku_u(t, tK - .2, tK + .6)), mf = oku_u(t, Wd('K15', 'bazıları') - .2, Wd('K15', 'kurdu', 0, true) + .5);
  const A = [[840, 610], [840, 330], [890, 278], [960, 258], [1030, 278], [1080, 330], [1080, 610]], B = [[790, 850], [790, 618], [1130, 618], [1130, 850]];
  for (let i = 0; i < OKU_ZN; i++) {
    const half = i < OKU_ZK ? -1 : 1, x0 = 165 + i * 30 + half * 60 * kr, y0 = 480 + kr * 18 * Math.abs(i - OKU_ZK + .5) / OKU_ZK * 2, a0 = 0;
    const q = i < OKU_ZK ? oku_yolNokta(A, i / (OKU_ZK - 1)) : oku_yolNokta(B, (i - OKU_ZK) / (OKU_ZN - OKU_ZK - 1));
    const u = E.io3(clamp(mf * 1.6 - (i < OKU_ZK ? i / OKU_ZK : (i - OKU_ZK) / (OKU_ZN - OKU_ZK)) * .6));
    oku_halka(lerp(x0, q[0], u), lerp(y0, q[1], u) - Math.sin(u * PI) * 60, lerp(a0, q[2], u), i);
  }
  if (kr > 0 && kr < 1) { const { ox } = GR; ox.save(); ox.strokeStyle = GR.inkCol; ox.lineWidth = 4; ox.lineCap = 'round'; for (let k = 0; k < 10; k++) { const a = k / 10 * TAU, r0 = 30 + 40 * kr, r1 = r0 + 40 * (1 - kr) + 10; ox.beginPath(); ox.moveTo(960 + 2 + Math.cos(a) * r0, 480 + Math.sin(a) * r0); ox.lineTo(960 + Math.cos(a) * r1, 480 + Math.sin(a) * r1); ox.stroke(); } ox.restore(); }
  if (mf > .9) kit_hat(700, 856, 1220, 856, 4);
}
plan('P128', (ctx, st) => levha(ctx, null, () => oku_k15(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ═════════════════ K15b: geri itilen taç; Cromwell (dönem silueti, portre değil) ═════════════════
function oku_k15b(st) {
  const t = st.t, { tx } = GR, G = 800;
  kit_cerceve();
  kit_hat(140, G, 1780, G, 4);
  // yüksek arkalıklı koltuk
  const K = new Path2D(); poly(K, [[590, G], [590, 236], [578, 220], [618, 196], [658, 220], [646, 236], [646, 590], [800, 590], [800, 612], [784, 612], [784, G], [768, G], [768, 612], [646, 612], [646, G]], true);
  GR.fill(K, GR.tone(.03), { th: 0, id: 0 }); kit_kutu(604, 250, 632, 576, 3, .95);
  // Cromwell: oturan koyu siluet, uzun saç, geniş beyaz yaka; kolu öne uzanmış, avuç dışa (geri iter)
  const h = 38, push = E.io2(oku_u(t, Wd('K15b', 'reddetti') - .4, Wd('K15b', 'reddetti') + .6));
  const J = SF.rig({ x: 712, y: 584, h: 38, facing: 1, twist: .55, lean: -.05 - .05 * push, head: .05, armN: [1.55 - .1 * push, -.2 - .3 * push], armF: [.6, .9], legN: [1.5, -1.5], legF: [1.4, -1.45] });
  kit_fig(J, { lum: 0, lit: [.6, -.8], t, legs: true, skirt: false, cloak: .8, lines: 0, hair: 1.5, armor: false, seed: 7, halo: 5 });
  { const c = J.nk, Y = new Path2D(); spline(Y, [[c[0] - 28, c[1] - 4], [c[0] + 30, c[1] - 6], [c[0] + 46, c[1] + 22], [c[0] + 12, c[1] + 40], [c[0] - 34, c[1] + 34], [c[0] - 46, c[1] + 12]], true, .8); GR.fill(Y, GR.tone(.975), { th: 0, id: 1 }); tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 3.5; tx.stroke(Y); tx.restore(); }
  // yastık üstünde taç: masacığın üstünde, 'reddetti'de geri itilir
  const dx = 150 * push, mx = 1010 + dx;
  const Tb = new Path2D(); poly(Tb, [[920 + dx, 640], [1100 + dx, 640], [1100 + dx, 656], [1080 + dx, 656], [1070 + dx, G], [1054 + dx, G], [1062 + dx, 656], [958 + dx, 656], [966 + dx, G], [950 + dx, G], [940 + dx, 656], [920 + dx, 656]], true); GR.fill(Tb, GR.tone(.03), { th: 0, id: 0 });
  const Ys = new Path2D(); spline(Ys, [[mx - 105, 634], [mx - 60, 604], [mx + 60, 604], [mx + 105, 634], [mx + 60, 646], [mx - 60, 646]], true, .8); GR.fill(Ys, GR.tone(.975), { th: 0, id: 1 }); tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 4.5; tx.stroke(Ys); tx.restore();
  const Cp = kit_tac(mx, 578, 44); GR.fill(Cp, GR.tone(.975), { th: 0, id: 1 }); tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 4.5; tx.lineJoin = 'round'; tx.stroke(Cp); tx.restore();
  // yanında genç siluet: 'oğluna'da belirginleşir
  const ao = kit_a(t, Wd('K15b', 'oğluna') - .4, 1.2), h2 = 32;
  const J2 = SF.rig({ x: 470, y: G - 3.95 * h2, h: h2, facing: 1, twist: .4, head: .02, armN: [.1, .2], armF: [-.1, .2] });
  kit_fig(J2, { lum: 0, lit: [.6, -.8], t, legs: true, cloak: 1, lines: 0, hair: 1.2, armor: false, seed: 11 }, .22 + .78 * ao);
  kit_yaz('Cromwell, 1657', 960, 900 - 40, { f: 'a', px: 68, a: kit_a(t, Wd('K15b', 'kromvel') - .2, 1), wipe: true });
}
plan('P129', (ctx, st) => levha(ctx, null, () => oku_k15b(st), [KIT_K, 0, 1]), { tr: KIT_TR });
