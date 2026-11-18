// Narkissos risograf adayı: beş plan (A–E) + kapak. Her plan: ciz(t, tc) plaka ve maskeyi çizer, param(t) baskı ayarlarını verir.
// Olaylar sabit saniyeye değil S()/Wd()'ye bağlıdır (../ortak/zaman.js).
import { W, H, g, setG, S as SM, rect, poly, blob, ellipse, circle, line, curve, layer, fill } from './vendor/draw.js';
import { C, clamp, ss, seg, lerp, bas, basMatris, avci, uzanan } from './figur.js';

const Z = () => window.ZAMAN;
const wd = (id, k) => window.Wd(id, k).t0;
const rnd = (i, s = 0) => { const x = Math.sin(i * 12.9898 + s * 78.233) * 43758.5453; return x - Math.floor(x); };

// ───── maske tuvali: R = su/cam, G = piksel ızgarası, B = parıltı ─────
export const maskC = document.createElement('canvas'); maskC.width = W; maskC.height = H;
export const MG = maskC.getContext('2d', { alpha: false });
export function maskeTemizle() { MG.setTransform(1, 0, 0, 1, 0, 0); MG.globalCompositeOperation = 'source-over'; MG.fillStyle = '#000'; MG.fillRect(0, 0, W, H); }
const mr = (r, p = 0, b = 0) => `rgb(${Math.round(r * 255)},${Math.round(p * 255)},${Math.round(b * 255)})`;
function maske(fn) { const T = g.getTransform(); const prev = setG(MG); MG.setTransform(T); try { fn(); } finally { setG(prev); } }
function maskeSil(fn) { const m0 = SM.mask; SM.mask = [0, 0, 0]; try { maske(fn); } finally { SM.mask = m0; } }
function parilti(x, y, r) { maske(() => { MG.globalCompositeOperation = 'lighter'; MG.beginPath(); MG.arc(x, y, r, 0, 7); MG.fillStyle = 'rgb(0,0,255)'; MG.fill(); MG.globalCompositeOperation = 'source-over'; }); }

function kamera(s, fx, fy, dx = 0, dy = 0) { const T = [s, 0, 0, s, fx * (1 - s) + dx, fy * (1 - s) + dy]; g.setTransform(...T); return T; }
const ekranY = (T, y) => T[3] * y + T[5];
const ekranX = (T, x) => T[0] * x + T[4];

// ───── manzara ilkelleri ─────
function kanopi(x, y, r, sd, renk, golge) {   // yuvarlak taç: gürültülü kapalı biçim (bukle değil, yaprak kütlesi)
  const n = 14, pts = [];
  for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2; const rr = r * (0.82 + rnd(i, sd) * .3) * (a > 0 && a < Math.PI ? .78 : 1); pts.push([x + Math.cos(a) * rr * 1.1, y + Math.sin(a) * rr]); }
  blob(pts, renk);
  if (golge) { const p2 = pts.map(([px, py]) => [px + (px - x) * -.12 + r * .12, py + (py - y) * -.1 + r * .22]); g.save(); g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.clip(); blob(p2.map(([px, py]) => [px, py + r * .25]), golge); g.restore(); }
}
function selvi(x, y, h, w, renk) { blob([[x, y - h], [x + w * .45, y - h * .7], [x + w * .55, y - h * .3], [x + w * .3, y], [x - w * .3, y], [x - w * .55, y - h * .3], [x - w * .45, y - h * .7]], renk); }
function govde(x, y0, y1, w, renk) { poly([[x - w / 2, y1], [x - w * .3, y0], [x + w * .3, y0], [x + w / 2, y1]], renk); }
function nergis(x, y, r, egik = 0) {
  curve([[x, y + r * 4.5], [x - r * .3, y + r * 2], [x + egik * r, y]], r * .28, C(0, 0, .9));
  g.beginPath(); g.ellipse(x + egik * r, y, r, r * .78, egik * .3, 0, 7); fill(C(0, 0, 0));       // kâğıt beyazı taç
  circle(x + egik * r + r * .12, y + r * .05, r * .38, C(0, 1, .05));                              // safran göbek
}
function cimen(x0, x1, y, n, h, sd, renk) { for (let i = 0; i < n; i++) { const x = lerp(x0, x1, rnd(i, sd)); const hh = h * (.5 + rnd(i, sd + 1)); curve([[x, y], [x + hh * .15, y - hh * .6], [x + hh * .35 * (rnd(i, sd + 2) - .3), y - hh]], 3, renk); } }

// ───── orman gölgesi arka planı (D ve kapak) ─────
function golgeOrman(x0, y0, x1, y1, t, sd = 3) {
  rect(x0, y0, x1 - x0, y1 - y0, C(.85, 0, .45));
  for (let i = 0; i < 9; i++) {
    const x = lerp(x0, x1, rnd(i, sd)), y = lerp(y0, y1 * .9, rnd(i, sd + 1)), r = 120 + rnd(i, sd + 2) * 160;
    kanopi(x + Math.sin(t * .4 + i) * 6, y, r, i + sd, C(.55, 0, 1), null);
  }
  // benekli ışık: yumuşak, yuvarlak lekeler (yıldız değil)
  for (let i = 0; i < 6; i++) {
    const x = lerp(x0, x1, rnd(i, sd + 7)), y = lerp(y0, y1 * .75, rnd(i, sd + 8)), r = 22 + rnd(i, sd + 9) * 40;
    ellipse(x + Math.sin(t * .6 + i * 2) * 10, y, r * 1.5, r, .3, C(.25, .35, .3));
  }
}

// ═════════ A: telefon camı → havuz (0–3,5) ═════════
const A = {
  WY: 640,
  sekil(k) {  // cam (yuvarlak köşeli dikdörtgen) ile havuz (elips) arası biçim, k: 0 cam → 1 havuz
    const n = 72, pts = [];
    const cx = 960, cyR = 900, rw = 560, rh = 260, rr = 70;          // cam: üst kenar WY'de, alt kadraj dışında
    const ex = 960, ey = 845, erx = 600, ery = 205;                  // havuz: kadraj içinde
    for (let i = 0; i < n; i++) {
      const a = i / n * Math.PI * 2, ca = Math.cos(a), sa = Math.sin(a);
      // yuvarlak dikdörtgen üzerinde aynı açıdaki nokta (süperelips yaklaşımı)
      const p = 8, sx = Math.sign(ca) * Math.pow(Math.abs(ca), 2 / p), sy = Math.sign(sa) * Math.pow(Math.abs(sa), 2 / p);
      const r0 = [cx + sx * rw, cyR + sy * rh];
      const r1 = [ex + ca * erx, ey + sa * ery];
      pts.push([lerp(r0[0], r1[0], k), lerp(r0[1], r1[1], k)]);
    }
    return pts;
  },
  ciz(t, tc) {
    const k = ss(seg(t, 2.85, 3.45));
    const T = kamera(1 + .045 * ss(seg(t, 0, 3.5)), 930, 600);
    // oda: koyu (Federal Blue); geçişte yapraklar üst baskıyla büyür (oda → orman gölgesi)
    rect(-100, -100, W + 200, H + 200, C(.92, 0, .12 * (1 - k) + .45 * k));
    if (k > 0) for (let i = 0; i < 7; i++) { const x = 120 + i * 290, y = 120 + rnd(i, 4) * 300; kanopi(x, y, (110 + rnd(i, 5) * 90) * k, i + 9, C(.55, 0, 1), null); }
    // ekran ışığı odayı aşağıdan hafifçe aydınlatır
    ellipse(960, A.WY + 30, 720, 120, 0, C(.6, 0, .25 * (1 - k)));
    // masa → kıyı (cam/havuz dışında kalan alt bölge)
    rect(-100, A.WY, W + 200, H, C(.55 + .2 * k, .0 + .25 * k, .1 + .5 * k));
    // genç: kapüşonlu, cama eğik
    const bl = Math.abs(tc - 1.25) < .1 ? .1 : 1;  // göz kırpma
    layer(() => bas({ x: 905, y: 575 + Math.sin(tc * 2.2) * 3, s: 430, r: .52, tip: 'modern', goz: bl, isik: .9 * (1 - k) + .5 * k, yaka: 'kapsonlu', ten: C(0, .30, .06) }), 4);
    // telefon gövdesi / havuz taşları: çerçeve (gövde boynu örter)
    const pts = A.sekil(k);
    const cer = 16 * (1 - k) + 10 * k;
    g.save(); g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath();
    g.lineWidth = cer * 2; g.strokeStyle = `rgb(${255},${Math.round(60 * k)},${255})`; g.stroke();
    g.fillStyle = 'rgb(0,0,0)'; g.fill(); g.restore();
    if (k > .3) for (let i = 0; i < 12; i++) { const p = pts[Math.floor(i / 12 * 72 + 30) % 72]; if (p[1] > A.WY + 20) ellipse(p[0], p[1] + 6, 36 * k, 18 * k, 0, C(.75, .1, .3)); }
    maske(() => { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath(); g.fillStyle = mr(1, 1 - ss(seg(t, 2.9, 3.4))); g.fill(); });
    return T;
  },
  param(t) {
    const k = ss(seg(t, 2.85, 3.45));
    const T = [1 + .045 * ss(seg(t, 0, 3.5))]; const s = T[0];
    const wy = A.WY * s + 600 * (1 - s);
    const tr = wd('S1', 'camın'), dt = t - tr;
    const ring = dt > 0 ? { x: 1010 * s + 930 * (1 - s), y: (A.WY + 120) * s + 600 * (1 - s), r: 40 + dt * 330, amp: 9 * Math.exp(-dt / .7), wl: 30, sq: 2.4, step: 8 } : null;
    const sep = [[-6, 2], [0, 0], [6, -2]];
    return { water: { y: wy, amp: .6 + 2.2 * k, t, refl: .72, sep, ink: [lerp(.42, 0, k), 0, lerp(.38, .62, k)], ring }, pixP: 13 };
  },
};

// ═════════ B: orman kenarında pınar, gelen genç (3,5–7) ═════════
const B = {
  WY: 742, P: [1190, 820, 360, 78],
  ciz(t, tc) {
    const T = kamera(1 + .05 * ss(seg(t, 3.5, 7)), 960, 740);
    rect(-100, -100, W + 200, H + 200, C(0, 0, 0));
    rect(-100, 230, W + 200, 300, C(0, .18, 0));
    rect(-100, 330, W + 200, 200, C(0, .34, 0));
    blob([[-100, 560], [-100, 450], [300, 410], [700, 440], [1100, 400], [1500, 430], [2020, 400], [2020, 560]], C(0, 0, .32));
    // uzak orman (havuzun arkası)
    for (let i = 0; i < 16; i++) { const x = 560 + i * 72 + rnd(i, 2) * 30, h = 150 + rnd(i, 3) * 110; govde(x, 700 - h * .3, 742, 10, C(1, 0, .2)); if (i % 3 === 1) selvi(x, 712, h * 1.25, 70, C(.35, 0, 1)); else kanopi(x, 712 - h * .55, 62 + rnd(i, 4) * 26, i + 30, C(.25, 0, .85), C(.7, 0, .9)); }
    // çayır
    blob([[-100, 1180], [-100, 742], [400, 728], [900, 738], [1500, 732], [2020, 745], [2020, 1180]], C(0, .30, .12));
    // sol ve sağ orman kütleleri
    for (let i = 0; i < 6; i++) { const x = -60 + i * 105, h = 520 + rnd(i, 7) * 160; govde(x + 20, 860 - h * .4, 880, 24, C(1, 0, .3)); kanopi(x + 20, 860 - h * .7, 150 + rnd(i, 8) * 40, i + 50, C(.35, 0, 1), C(.8, 0, .9)); }
    for (let i = 0; i < 5; i++) { const x = 1640 + i * 90, h = 500 + rnd(i, 9) * 160; govde(x, 860 - h * .4, 870, 22, C(1, 0, .3)); kanopi(x, 860 - h * .7, 140 + rnd(i, 10) * 40, i + 70, C(.35, 0, 1), C(.8, 0, .9)); }
    cimen(0, 1920, 900, 60, 28, 3, C(0, .3, .8));
    // havuz (kâğıda boşaltılır; suyun rengi baskıda)
    const [px, py, rx, ry] = B.P;
    ellipse(px, py, rx + 16, ry + 8, 0, C(.7, .08, .35));
    ellipse(px, py, rx, ry, 0, C(0, 0, 0));
    for (let i = 0; i < 14; i++) { const a = Math.PI * (.05 + .9 * i / 13); ellipse(px + Math.cos(a) * (rx + 6), py + Math.sin(a) * (ry + 5), 26 + rnd(i, 11) * 14, 12, 0, C(.8, .1, .3)); }
    blob([[px + rx - 40, py - ry - 10], [px + rx + 30, py - ry - 60], [px + rx + 80, py - ry - 20], [px + rx + 40, py - ry + 20]], C(.8, .1, .3));   // pınarın taşı
    for (const [x, y, r, e] of [[px - rx - 10, py - 30, 13, -.5], [px - rx + 30, py + 50, 11, .3], [px - 200, py + ry + 20, 12, 0], [px + 80, py + ry + 22, 10, .4], [px + rx - 30, py + 60, 11, -.3]]) nergis(x, y, r, e);
    maske(() => { g.beginPath(); g.ellipse(px, py, rx, ry, 0, 0, 7); g.fillStyle = mr(1); g.fill(); });
    // genç: soldan gelir, 'eğildi'de durur ve suya eğilir
    const tb = 3.5, te = wd('S2', 'pınara') + .05, tl = wd('S2', 'eğildi');
    const kk = seg(tc, tb, te), yolX = lerp(-120, 760, 1 - Math.pow(1 - kk, 1.6));
    const d = yolX + 120, yuru = tc < te ? 1 : Math.max(0, 1 - (tc - te) * 4);
    const eg = ss(seg(tc, tl - .05, tl + .5));
    layer(() => avci({ x: yolX, gy: 905, u: 29, d, t: tc, yuru, lean: .28 * eg, bakis: .55 * eg }), 4);
    return T;
  },
  param(t) {
    const s = 1 + .05 * ss(seg(t, 3.5, 7));
    return { water: { y: B.WY * s + 740 * (1 - s), amp: 1.6, t, refl: .85, sep: [[-2, 0], [0, 0], [2, 0]], ink: [0, 0, .45] } };
  },
};

// ═════════ C: uzanan genç, yansıması görünür (7–10,5) ═════════
const C_ = {
  WY: 660, P: [1250, 860, 640, 200],
  ciz(t, tc) {
    const T = kamera(1 + .06 * ss(seg(t, 7, 10.5)), 1000, 620);
    rect(-100, -100, W + 200, H + 200, C(0, .2, 0));
    rect(-100, -100, W + 200, 200, C(0, .08, 0));
    // arka orman gölgesi
    for (let i = 0; i < 12; i++) { const x = -40 + i * 175, r = 150 + rnd(i, 12) * 70; govde(x + 30, 300, 660, 26, C(1, 0, .3)); kanopi(x, 180 + rnd(i, 13) * 120, r, i + 90, C(.45, 0, 1), C(.85, 0, .85)); }
    rect(-100, 380, W + 200, 300, C(.8, 0, .55));
    for (let i = 0; i < 10; i++) { const x = rnd(i, 14) * 1920; kanopi(x, 420 + rnd(i, 15) * 120, 90 + rnd(i, 16) * 60, i + 120, C(.5, 0, 1), null); }
    // karşı kıyı şeridi
    blob([[-100, 700], [-100, 610], [600, 600], [1300, 612], [2020, 600], [2020, 700]], C(0, .3, 1));
    cimen(500, 1900, 650, 40, 30, 5, C(.7, 0, 1));
    for (const [x, y, r, e] of [[1500, 628, 14, -.3], [1580, 640, 12, .4], [1720, 625, 13, 0], [1100, 635, 12, .2]]) nergis(x, y, r, e);
    // havuz
    const [px, py, rx, ry] = C_.P;
    ellipse(px, py, rx, ry, 0, C(0, 0, 0));
    maske(() => { g.beginPath(); g.ellipse(px, py, rx, ry, 0, 0, 7); g.fillStyle = mr(1); g.fill(); });
    // yakın kıyı (genç bunun üstünde uzanır); maskeden düşülür
    const kiyi = [[-100, 1180], [-100, 620], [300, 612], [700, 628], [960, 640], [1010, 700], [930, 820], [760, 1000], [700, 1180]];
    poly(kiyi, C(.7, .15, .35));
    blob([[-100, 650], [-100, 600], [400, 595], [800, 610], [985, 630], [990, 665], [700, 670], [300, 668]], C(.15, .25, 1));
    maskeSil(() => poly(kiyi, C(1, 1, 1)));
    cimen(0, 980, 640, 50, 30, 7, C(.6, .1, 1));
    // genç
    const tl = wd('S3', 'âşık');
    const uz = ss(seg(tc, tl, tl + .9)) * .55;
    const nef = Math.sin(tc * 2.4);
    let bm;
    layer(() => { bm = uzanan({ x: 840, y: 640, u: 92, t: tc, nefes: nef, uzan: uz, basX: 1.25, basY: -1.0, basR: .78 + .05 * ss(seg(tc, 8.38, 9.2)), goz: .85 }); }, 4);
    maskeSil(() => uzanan({ x: 840, y: 640, u: 92, t: tc, nefes: nef, uzan: uz, basX: 1.25, basY: -1.0, basR: .78 + .05 * ss(seg(tc, 8.38, 9.2)), goz: .85 }));
    nergis(980, 760, 14, .5); nergis(930, 805, 12, -.2);
    return T;
  },
  param(t) {
    const s = 1 + .06 * ss(seg(t, 7, 10.5));
    return { water: { y: C_.WY * s + 620 * (1 - s), amp: 1.4, t, refl: .9, sep: [[-5, 1], [0, 0], [5, -1]], ink: [.12, 0, .55] } };
  },
};

// ═════════ D: öpüşme ekseni (10,5–16) ═════════
function dDuzen() {
  if (H > W) return { WY: 1000, bx: 600, by: 958, bs: 560, br: .55, kiyiX: 300, fx: 560, fy: 1000 };   // dikey
  return { WY: 585, bx: 760, by: 548, bs: 440, br: .55, kiyiX: 470, fx: 760, fy: 585 };
}
function gozYasiZaman() { const t0 = wd('S4', 'gözyaşı'); return { t0, tf: t0 + .18 }; }
const D = {
  bm: null,
  ciz(t, tc, kapak) {
    const L = dDuzen();
    const T = kapak ? kamera(1, 0, 0) : kamera(1 + .075 * ss(seg(t, 10.5, 16)), L.fx, L.fy);
    rect(-100, -100, W + 200, H + 200, C(0, 0, 0));
    golgeOrman(-100, -100, W + 100, L.WY + 2, t, 3);
    // su yüzeyi (kâğıda boşalt; renk baskıda)
    rect(-100, L.WY, W + 200, H + 200, C(0, 0, 0));
    maske(() => { g.fillStyle = mr(1); g.fillRect(-200, L.WY, W + 400, H + 400); });
    // tanıma: göz açılır, kaş kalkar
    const tb = wd('S4', 'benim'), ta = wd('S4', 'anladı');
    const tan = kapak ? 0 : ss(seg(tc, ta, tb + .2));
    const goz = .78 + .22 * tan;
    const bo = { x: L.bx, y: L.by + Math.sin(tc * 1.9) * 2.5 - tan * 6, s: L.bs, r: L.br - tan * .03, tip: 'antik', goz, kas: tan * .012, isik: kapak ? 0 : .85, sw: Math.sin(tc * 2.2) * .02, yaka: 'khlamys', ten: kapak ? C(0, .5, 0) : undefined };
    layer(() => { D.bm = bas(bo); }, kapak ? 3 : 4);
    maskeSil(() => bas(bo));
    // yakın kıyı (boyun ve omzu örter)
    const kx = L.kiyiX;
    const kiyi = [[-100, H + 100], [-100, L.WY - 10], [kx * .6, L.WY - 18], [kx, L.WY - 4], [kx + 60, L.WY + 40], [kx + 20, L.WY + 140], [kx - 120, L.WY + 300], [kx - 260, H + 100]];
    poly(kiyi, C(.85, .1, .6));
    blob([[-100, L.WY + 10], [-100, L.WY - 40], [kx * .5, L.WY - 46], [kx + 10, L.WY - 30], [kx + 50, L.WY + 6], [kx * .4, L.WY + 20]], C(.2, .25, 1));
    maskeSil(() => poly(kiyi, C(1, 1, 1)));
    cimen(-40, kx + 30, L.WY - 20, 26, 46, 9, C(.6, .1, 1));
    nergis(kx - 90, L.WY - 60, 22, .3); nergis(kx - 10, L.WY - 30, 18, -.4); nergis(kx - 190, L.WY - 48, 16, .1);
    // gözyaşı: göz pınarından düşer
    if (!kapak) {
      const { t0, tf } = gozYasiZaman();
      const M = basMatris(bo.x, bo.y, bo.s, bo.r, 1);
      const e = M.transformPoint(new DOMPoint(.70, .482));
      if (t > t0 - .05) {
        const tt = t - tf;
        const r0 = 7 * ss(seg(t, t0, tf));
        let y = e.y, x = e.x;
        if (tt > 0) { y = e.y + 1600 * tt * tt + 60 * tt; x = e.x + 40 * tt; }
        if (y < L.WY) { g.beginPath(); g.ellipse(x, y, r0, r0 * (tt > 0 ? 1.35 : 1.1), 0, 0, 7); fill(C(0, 0, 0)); g.beginPath(); g.ellipse(x - r0 * .2, y + r0 * .2, r0 * .55, r0 * .7, 0, 0, 7); fill(C(0, 0, .45)); }
      }
    }
    if (kapak) {   // kapak: yansıyan gözün parıltısı (karenin en parlak noktası)
      const M = basMatris(bo.x, bo.y, bo.s, bo.r, 1);
      const e = M.transformPoint(new DOMPoint(.672, .468));
      parilti(e.x + 4, 2 * L.WY - e.y + 2, 11);
    }
    return T;
  },
  carpma() {   // gözyaşının suya değdiği an ve yer
    const L = dDuzen();
    const { tf } = gozYasiZaman();
    const M = basMatris(L.bx, L.by, L.bs, L.br, 1);
    const e = M.transformPoint(new DOMPoint(.70, .482));
    const h = L.WY - e.y; const a = 1600, b = 60; const tt = (-b + Math.sqrt(b * b + 4 * a * h)) / (2 * a);
    return { th: tf + tt, x: e.x + 40 * tt };
  },
  param(t, kapak) {
    const L = dDuzen();
    const s = kapak ? 1 : 1 + .075 * ss(seg(t, 10.5, 16));
    const fx = kapak ? 0 : L.fx, fy = kapak ? 0 : L.fy;
    const X = x => x * s + fx * (1 - s), Y = y => y * s + fy * (1 - s);
    const tb = wd('S4', 'benim');
    const { th, x: hx } = D.carpma();
    let amp = 2.2, sepK = 1, ring = null, refl = .8, ink = [.05, 0, .62];
    if (kapak) {
      return { water: { y: Y(L.WY), amp: 1.2, t: 3.1, refl: .9, sep: [[-4, 1], [0, 0], [4, -1]], ink: [.05, 0, .5], ring: { x: X(L.bx + 60), y: Y(L.WY + 40), r: 190, amp: 7, wl: 40, sq: 2.6, step: 9 } } };
    }
    if (t > th) {
      const dt = t - th;
      amp += 15 * Math.exp(-dt / .55) * ss(seg(dt, 0, .12));
      sepK += 1.6 * Math.exp(-dt / .8) * ss(seg(dt, 0, .2));
      ring = { x: X(hx), y: Y(L.WY + 6), r: 10 + dt * 300, amp: 13 * Math.exp(-dt / .9), wl: 38, sq: 2.6, step: 9 };
    }
    if (t >= tb) {   // TANIMA: plakalar tek vuruşta yerine oturur, yansıma keskinleşir
      const dt = t - tb;
      const sn = Math.exp(-dt / .07) * Math.cos(dt * 42);
      sepK = sepK * sn;
      amp = lerp(amp, .35, ss(seg(dt, 0, .15)));
      refl = lerp(refl, 1, ss(seg(dt, 0, .1)));
      ink = [lerp(.05, .02, ss(seg(dt, 0, .1))), 0, lerp(.62, .32, ss(seg(dt, 0, .1)))];
    }
    const sep = [[-9 * sepK, 3 * sepK], [0, 0], [9 * sepK, -3 * sepK]];
    return { water: { y: Y(L.WY), amp, t, refl, sep, ink, ring } };
  },
  parilti(t) {   // 'benim' anından sonra yansıyan gözde parıltı
    const tb = wd('S4', 'benim');
    if (t < tb) return;
    const L = dDuzen();
    const M = basMatris(L.bx, L.by, L.bs, L.br, 1);
    const e = M.transformPoint(new DOMPoint(.672, .468));
    parilti(e.x + 4, 2 * L.WY - e.y + 2, 9 * ss(seg(t, tb, tb + .12)));
  },
};

// ═════════ E: su kenarı → telefon kenarı (16–19,5) ═════════
const E = {
  WY: 470,
  kenar(k) {   // su bölgesinin sınırı: k=0 doğal kıyı, k=1 telefon camı (düz üst kenar, yuvarlak sol köşe)
    const pts = [];
    const n = 48;
    for (let i = 0; i <= n; i++) {   // üst kenar soldan sağa
      const u = i / n, x = lerp(380, 2020, u);
      const y0 = E.WY + Math.sin(u * 9.0 + 1) * 14 + Math.sin(u * 23) * 6 + (u < .12 ? (0.12 - u) * 500 : 0);
      pts.push([x + (1 - k) * Math.sin(u * 13) * 8, lerp(y0, E.WY, k)]);
    }
    pts.push([2020, H + 100]);
    // sol kenar aşağı: doğal kıyı eğrisi → düz kenar + yuvarlak köşe
    const m = 24;
    for (let i = 0; i <= m; i++) {
      const u = i / m;
      const yy = lerp(H + 100, E.WY, u);
      const x0 = 380 - (1 - u) * 160 + Math.sin(u * 7) * 30;
      let x1 = 380; const rr = 120; if (yy < E.WY + rr) { const dy = (E.WY + rr - yy) / rr; x1 = 380 + rr * (1 - Math.sqrt(Math.max(0, 1 - dy * dy))); }
      pts.push([lerp(x0, x1, k), yy]);
    }
    return pts;
  },
  ciz(t, tc) {
    const tB = wd('S5', 'bakmayı'), tY = wd('S5', 'yine'), tR = wd('S5', 'bırakamadı');
    const k = ss(seg(t, tB, tB + .9));
    const T = kamera(1 + .04 * ss(seg(t, 16, 19.5)), 900, 470);
    const isik = ss(seg(tc, tR - .4, tR + .6));
    // üst: orman gölgesi → oda karanlığı (Federal Blue)
    rect(-100, -100, W + 200, H + 200, C(.88, 0, .5 * (1 - k) + .12 * k));
    if (k < 1) for (let i = 0; i < 6; i++) kanopi(200 + i * 330, 60 + rnd(i, 21) * 200, (130 + rnd(i, 22) * 70) * (1 - k), i + 200, C(.55, 0, 1), null);
    // kıyı/masa: alt bölge
    rect(-100, E.WY - 40, W + 200, H + 200, C(.75 - .15 * k, .12 + .15 * k, .55 - .45 * k));
    // yüz (alt yarısı): eski genç → bugünün genci ('yine'de, plaka tepmesiyle)
    const modern = tc >= tY;
    const bo = { x: 980, y: 400 + Math.sin(tc * 1.7) * 3 + isik * 6, s: 900, r: .62, tip: modern ? 'modern' : 'antik', goz: .85, isik: .35 + .65 * isik, sw: 0, ten: modern ? C(0, .30, .06) : undefined };
    layer(() => bas(bo), 5);
    maskeSil(() => bas(bo));
    // su/cam bölgesi
    const pts = E.kenar(k);
    g.save(); g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath();
    g.lineWidth = 8 + 20 * k; g.strokeStyle = `rgb(255,${Math.round(30 * (1 - k))},${Math.round(255 * (.6 + .4 * k))})`; g.stroke();
    g.fillStyle = 'rgb(0,0,0)'; g.fill(); g.restore();
    if (k < .7) for (let i = 0; i < 9; i++) { const p = pts[Math.floor(i * 5 + 2)]; ellipse(p[0], p[1] - 4, 34 * (1 - k), 16 * (1 - k), 0, C(.8, .1, .3)); }
    if (k < .5) { nergis(300, 420, 20 * (1 - 2 * k), .3); nergis(220, 470, 17 * (1 - 2 * k), -.2); }
    const pix = ss(seg(t, tB + .2, tY + .6));
    maske(() => { g.beginPath(); pts.forEach((p, i) => i ? g.lineTo(...p) : g.moveTo(...p)); g.closePath(); g.fillStyle = mr(1, pix); g.fill(); });
    // ekran ışığı: camın kenarlarından yükselen soğuk ışık (yüzü aşağıdan aydınlatır)
    if (isik > 0) { g.save(); g.globalCompositeOperation = 'source-over'; ellipse(1100, E.WY - 10, 760 * isik, 40 * isik, 0, C(.3, .05, .35)); g.restore(); }
    return T;
  },
  param(t) {
    const tB = wd('S5', 'bakmayı'), tY = wd('S5', 'yine'), tR = wd('S5', 'bırakamadı');
    const k = ss(seg(t, tB, tB + .9));
    const s = 1 + .04 * ss(seg(t, 16, 19.5));
    const X = x => x * s + 900 * (1 - s), Y = y => y * s + 470 * (1 - s);
    const isik = ss(seg(t, tR - .4, tR + .6));
    const dt = t - tY;
    const ring = dt > 0 ? { x: X(1120), y: Y(E.WY + 150), r: 10 + dt * 300, amp: 12 * Math.exp(-dt / .9), wl: 36, sq: 2.2, step: 9 } : null;
    return {
      water: { y: Y(E.WY), amp: 1.4 * (1 - k) + .3, t, refl: lerp(.9, .62, isik), sep: [[-7, 2], [0, 0], [7, -2]], ink: [lerp(.05, .55, k) - .25 * isik, 0, lerp(.6, .5, k) - .2 * isik], ring },
      pixP: lerp(9, 15, ss(seg(t, tB + .2, tY + .6))),
    };
  },
};

export const PLAN = { A, B, C: C_, D, E };

// Kayıt (plaka) vuruşları: belli sözcüklerde ~10 px tepme, ~0,25 sn'de söner
export function kayit(t, id) {
  const taban = { A: [[0, 0], [3, -2], [-3, 2]], B: [[0, 0], [-2, 3], [3, -1]], C: [[0, 0], [3, 2], [-2, -3]], D: [[0, 0], [2, -3], [-3, 1]], E: [[0, 0], [-3, -2], [2, 3]] }[id] || [[0, 0], [0, 0], [0, 0]];
  const vur = [[wd('S1', 'camın'), 6], [D.carpma().th, 7], [wd('S4', 'benim'), 11], [wd('S5', 'yine'), 9]];
  const off = taban.map(p => p.slice());
  for (const [tv, a] of vur) {
    const dt = t - tv; if (dt < 0 || dt > .5) continue;
    const e = a * Math.exp(-dt / .08) * Math.cos(dt * 38);
    off[1][0] += e * .8; off[1][1] -= e * .5; off[2][0] -= e * .6; off[2][1] += e * .7;
  }
  return off;
}

export function kapakCiz(yazi) {
  const T = D.ciz(3.1, 3.1, true);
  if (yazi) {
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.font = '400 300px "Bebas Neue"'; g.textAlign = 'left'; g.textBaseline = 'alphabetic';
    const x = 1010, y = 420;
    g.fillStyle = 'rgb(0,0,255)'; g.fillText('O BENİM', x + 9, y + 9);      // Teal ikinci vuruş (kayık)
    g.fillStyle = 'rgb(0,255,0)'; g.fillText('O BENİM', x, y);              // Sunflower
  }
  return T;
}
export const kapakParam = () => D.param(3.1, true);
