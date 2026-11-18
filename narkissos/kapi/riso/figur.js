// Narkissos risograf adayı: figür çizimi (plaka yoğunluklarıyla). Mürekkepler: R = Federal Blue, G = Sunflower, B = Teal.
// Baş: dergi illüstrasyonu inceliğinde genç profil (alın, burun, dudak, çene, göz, kaş, kulak, saç). Yerel birim: baş yüksekliği = 1 (tepe 0, çene ~0.955).
import { g, layer, ik, line, curve, fill } from './vendor/draw.js';

export const C = (b = 0, s = 0, t = 0) => [b, s, t];
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const ss = x => { x = clamp(x); return x * x * (3 - 2 * x); };
export const seg = (t, a, b) => clamp((t - a) / (b - a));
export const lerp = (a, b, k) => a + (b - a) * k;

export const RENK = {
  ten: C(0, .34, 0),        // açık ten: yalnız Sunflower tonu
  tenAcik: C(0, .2, 0),     // aşağıdan gelen ışığın vurduğu yüzeyler
  tenKoyu: C(0, .5, 0),
  dudak: C(.06, .52, 0),
  sac: C(1, .38, .12),      // koyu kahve-siyah: Blue + Sunflower üst baskı
  sacTel: C(.82, .5, .06),
  cizgi: C(.95, 0, .5),
  khlamys: C(0, 0, 1),      // Teal pelerin
  khiton: C(0, .24, .0),    // keten
  kapsonlu: C(1, 0, .15),   // bugünün genci: Federal Blue kapüşonlu
};

// Yerel → çizim matrisi. Pivot = alt dudak/çene noktası (0.75, 0.80).
export function basMatris(x, y, s, r, flip = 1) {
  return new DOMMatrix().translate(x, y).rotate(r * 180 / Math.PI).scale(s * flip, s).translate(-.75, -.80);
}

function profilYolu() {
  g.beginPath();
  g.moveTo(0.60, 0.10);
  g.bezierCurveTo(0.68, 0.16, 0.725, 0.27, 0.73, 0.36);
  g.quadraticCurveTo(0.745, 0.405, 0.737, 0.427);
  g.quadraticCurveTo(0.716, 0.452, 0.721, 0.472);
  g.lineTo(0.797, 0.603);
  g.quadraticCurveTo(0.822, 0.638, 0.800, 0.656);
  g.quadraticCurveTo(0.776, 0.669, 0.749, 0.668);
  g.quadraticCurveTo(0.752, 0.700, 0.767, 0.727);
  g.quadraticCurveTo(0.763, 0.747, 0.748, 0.753);
  g.quadraticCurveTo(0.767, 0.766, 0.761, 0.787);
  g.quadraticCurveTo(0.751, 0.810, 0.729, 0.824);
  g.bezierCurveTo(0.748, 0.860, 0.760, 0.915, 0.742, 0.942);
  g.quadraticCurveTo(0.715, 0.968, 0.650, 0.962);
  g.quadraticCurveTo(0.590, 0.958, 0.562, 0.975);
  g.quadraticCurveTo(0.552, 1.03, 0.572, 1.075);
  g.quadraticCurveTo(0.585, 1.10, 0.570, 1.13);
  g.quadraticCurveTo(0.560, 1.20, 0.575, 1.32);
  g.lineTo(0.30, 1.32);
  g.quadraticCurveTo(0.29, 1.02, 0.22, 0.86);
  g.bezierCurveTo(0.08, 0.78, 0.02, 0.55, 0.06, 0.38);
  g.bezierCurveTo(0.10, 0.12, 0.35, 0.0, 0.48, 0.02);
  g.quadraticCurveTo(0.56, 0.04, 0.60, 0.10);
  g.closePath();
}

function sacAntik(sw) {   // efeb: kısa, dalgalı, kulak açık; alında birkaç kısa perçem
  const w = sw || 0;
  g.beginPath();
  g.moveTo(0.705, 0.245);
  g.quadraticCurveTo(0.715, 0.15, 0.63, 0.075);
  g.bezierCurveTo(0.53, -0.025, 0.31, -0.045, 0.16, 0.045);
  g.bezierCurveTo(0.03, 0.13, -0.015, 0.35, 0.025, 0.50);
  g.quadraticCurveTo(0.05 + w, 0.61, 0.13 + w, 0.665);
  g.quadraticCurveTo(0.155, 0.60, 0.205, 0.635);
  g.quadraticCurveTo(0.24, 0.56, 0.30, 0.585);
  g.quadraticCurveTo(0.33, 0.50, 0.395, 0.47);
  g.quadraticCurveTo(0.47, 0.435, 0.505, 0.50);
  g.lineTo(0.535, 0.53);
  g.quadraticCurveTo(0.53, 0.44, 0.575, 0.385);
  g.quadraticCurveTo(0.595, 0.30, 0.64, 0.275);
  g.quadraticCurveTo(0.675, 0.27, 0.705, 0.245);
  g.closePath();
  fill(RENK.sac);
  // alına düşen kısa perçem
  g.beginPath(); g.moveTo(0.66, 0.15); g.quadraticCurveTo(0.735, 0.21, 0.725, 0.29); g.quadraticCurveTo(0.70, 0.24, 0.655, 0.235); g.closePath(); fill(RENK.sac);
  const tel = (p, wd) => curve(p, wd, RENK.sacTel);
  tel([[0.60, 0.08], [0.46, 0.03], [0.30, 0.05], [0.17, 0.13]], .010);
  tel([[0.58, 0.20], [0.46, 0.14], [0.32, 0.16], [0.18, 0.26], [0.10, 0.40]], .009);
  tel([[0.55, 0.32], [0.44, 0.27], [0.31, 0.32], [0.20, 0.45], [0.16 + w, 0.58]], .009);
}

function sacModern() {     // kısa, yanları ve ensesi kısa; önde dağınık kâkül
  g.beginPath();
  g.moveTo(0.72, 0.265);
  g.quadraticCurveTo(0.735, 0.17, 0.66, 0.09);
  g.bezierCurveTo(0.56, -0.02, 0.33, -0.05, 0.18, 0.03);
  g.bezierCurveTo(0.05, 0.11, 0.02, 0.30, 0.05, 0.44);
  g.quadraticCurveTo(0.10, 0.50, 0.20, 0.49);
  g.quadraticCurveTo(0.30, 0.47, 0.39, 0.45);
  g.quadraticCurveTo(0.47, 0.43, 0.51, 0.48);
  g.lineTo(0.53, 0.47);
  g.quadraticCurveTo(0.545, 0.39, 0.585, 0.35);
  g.quadraticCurveTo(0.62, 0.30, 0.66, 0.29);
  g.quadraticCurveTo(0.70, 0.29, 0.72, 0.265);
  g.closePath();
  fill(RENK.sac);
  curve([[0.66, 0.12], [0.54, 0.04], [0.38, 0.03]], .010, RENK.sacTel);
  curve([[0.62, 0.22], [0.48, 0.13], [0.30, 0.13], [0.16, 0.24]], .009, RENK.sacTel);
}

// o: {x,y,s,r,flip, tip:'antik'|'modern', goz (0 kapalı..1 açık), isik (0..1 aşağıdan ışık), sw (saç salınımı), yaka: 'khlamys'|'kapsonlu'|null, kaybol}
export function bas(o) {
  const m = basMatris(o.x, o.y, o.s, o.r || 0, o.flip || 1);
  g.save();
  g.setTransform(g.getTransform().multiply(m));
  // boyun altı giysi (yaka)
  if (o.yaka === 'khlamys') {
    g.beginPath(); g.moveTo(0.18, 1.14); g.quadraticCurveTo(0.42, 1.06, 0.66, 1.16); g.lineTo(0.86, 1.45); g.lineTo(0.05, 1.45); g.closePath(); fill(RENK.khiton);
    g.beginPath(); g.moveTo(0.12, 1.10); g.quadraticCurveTo(0.30, 1.04, 0.40, 1.12); g.quadraticCurveTo(0.52, 1.24, 0.70, 1.30); g.lineTo(0.80, 1.45); g.lineTo(-.05, 1.45); g.closePath(); fill(RENK.khlamys);
    g.beginPath(); g.arc(0.40, 1.15, 0.035, 0, 7); fill(C(0, 1, 0));
    g.beginPath(); g.arc(0.40, 1.15, 0.014, 0, 7); fill(C(.7, .6, 0));
  } else if (o.yaka === 'kapsonlu') {
    g.beginPath(); g.moveTo(0.02, 1.02); g.bezierCurveTo(0.04, 0.86, 0.20, 0.86, 0.30, 0.98); g.quadraticCurveTo(0.42, 1.14, 0.60, 1.12); g.quadraticCurveTo(0.70, 1.14, 0.78, 1.22); g.lineTo(0.92, 1.45); g.lineTo(-.08, 1.45); g.closePath(); fill(RENK.kapsonlu);
    curve([[0.60, 1.14], [0.63, 1.26], [0.62, 1.40]], .012, C(0, .1, 0));
    curve([[0.68, 1.16], [0.72, 1.28], [0.72, 1.40]], .012, C(0, .1, 0));
  }
  // baş ve boyun
  profilYolu(); fill(o.ten || RENK.ten);
  // aşağıdan ışık: alt yüzeyler açık (burun altı, çene altı, boyun önü)
  if ((o.isik ?? 1) > 0) {
    g.save(); profilYolu(); g.clip();
    const k = o.isik ?? 1;
    const lit = C(0, lerp((o.ten || RENK.ten)[1], RENK.tenAcik[1], k), 0);
    g.beginPath(); g.ellipse(0.64, 1.06, 0.14, 0.07, -0.15, 0, 7); fill(lit);
    g.beginPath(); g.ellipse(0.79, 0.668, 0.035, 0.010, 0.2, 0, 7); fill(lit);
    g.restore();
  }
  // kulak
  g.beginPath(); g.moveTo(0.455, 0.50); g.bezierCurveTo(0.38, 0.47, 0.37, 0.60, 0.40, 0.64); g.quadraticCurveTo(0.43, 0.67, 0.465, 0.63); g.closePath(); fill(RENK.tenKoyu);
  curve([[0.445, 0.53], [0.405, 0.55], [0.41, 0.61], [0.44, 0.62]], .008, C(.25, .6, 0));
  // çene hattı
  curve([[0.665, 0.952], [0.56, 0.90], [0.47, 0.80]], .007, C(.12, .5, 0));
  // göz (profil: bademsi, küçük; ak kısmı kâğıda yakın ama küçük)
  const op = clamp(o.goz ?? 1, 0.05, 1);
  g.save();
  g.beginPath(); g.moveTo(0.632, 0.470); g.quadraticCurveTo(0.66, 0.470 - .020 * op, 0.693, 0.466); g.quadraticCurveTo(0.67, 0.483, 0.632, 0.470); g.closePath();
  fill(C(0, .07, 0)); g.clip();
  g.beginPath(); g.ellipse(0.678, 0.470, 0.013, 0.018, 0, 0, 7); fill(C(1, 0, .55));
  g.restore();
  curve([[0.628, 0.471], [0.655, 0.470 - .024 * op], [0.695, 0.465]], .010, RENK.cizgi);   // üst kapak
  curve([[0.694, 0.465], [0.705, 0.458]], .006, RENK.cizgi);                               // kirpik ucu
  curve([[0.64, 0.478], [0.67, 0.484], [0.69, 0.472]], .004, C(.3, .5, 0));                // alt kapak
  curve([[0.635, 0.452 - .01 * op], [0.665, 0.442 - .012 * op], [0.695, 0.452]], .004, C(.2, .55, 0)); // kapak kıvrımı
  // kaş
  const kl = o.kas || 0;
  curve([[0.60, 0.420 - kl], [0.655, 0.404 - kl * 1.4], [0.718, 0.414 - kl]], .021, RENK.sac);
  // burun deliği
  curve([[0.762, 0.646], [0.778, 0.655], [0.786, 0.652]], .006, C(.4, .55, 0));
  // dudaklar
  g.beginPath(); g.moveTo(0.718, 0.752); g.quadraticCurveTo(0.740, 0.722, 0.756, 0.716); g.quadraticCurveTo(0.766, 0.722, 0.767, 0.728); g.quadraticCurveTo(0.763, 0.747, 0.748, 0.753); g.closePath(); fill(RENK.dudak);
  g.beginPath(); g.moveTo(0.718, 0.754); g.lineTo(0.748, 0.754); g.quadraticCurveTo(0.767, 0.766, 0.761, 0.787); g.quadraticCurveTo(0.735, 0.79, 0.718, 0.756); g.closePath(); fill(RENK.dudak);
  curve([[0.712, 0.755], [0.732, 0.755], [0.750, 0.753]], .006, C(.7, .4, .2));
  // saç
  if (o.tip === 'modern') sacModern(); else sacAntik(o.sw);
  g.restore();
  return m;
}

// ───── Tam boy figür (yan profil, sağa bakar). u = baş yüksekliği (px). ─────
function kapsul(a, b, w, c) { line([a, b], w, c); }

// Yürüyen avcı. x: kalça x, gy: zemin, d: alınan yol (px), lean: öne eğilme (rad), bakis: baş eğimi
export function avci(o) {
  const u = o.u, gy = o.gy, d = o.d, S = 2.7 * u;
  const ph = d / S;
  const ayak = (off) => {
    const p = ph + off, c = Math.floor(p), f = p - c;
    const x0 = o.x - d;   // yolun başı
    if (f < .5) return [x0 + (c + .25) * S, gy - .12 * u, 0];
    const k = (f - .5) / .5;
    return [x0 + (c + .25 + k) * S, gy - .12 * u - Math.sin(Math.PI * k) * .38 * u, k];
  };
  const hiz = o.yuru ?? 1;
  const bob = Math.abs(Math.cos(ph * Math.PI * 2)) * .07 * u * hiz;
  const hip = [o.x, gy - 3.72 * u + bob];
  const lean = o.lean || 0;
  const sh = [hip[0] + Math.sin(lean) * 2.55 * u + .1 * u, hip[1] - Math.cos(lean) * 2.55 * u];
  const neck = [sh[0] + .12 * u + Math.sin(lean) * .3 * u, sh[1] - .32 * u];
  const f1 = hiz > 0 ? ayak(0) : [o.x + .35 * u, gy - .12 * u, 0], f2 = hiz > 0 ? ayak(.5) : [o.x - .35 * u, gy - .12 * u, 0];
  const L1 = 1.92 * u, L2 = 1.86 * u;
  const [k1] = ik(hip, f1, L1, L2, -1), [k2] = ik(hip, f2, L1, L2, -1);
  const sw = Math.sin(ph * Math.PI * 2) * hiz;
  const tenB = C(0, .40, 0), tenU = C(.18, .40, 0);
  // uzak bacak ve kol (biraz koyu)
  kapsul(hip, k2, .40 * u, tenU); kapsul(k2, f2, .30 * u, tenU);
  kapsul([f2[0] - .1 * u, f2[1] + .05 * u], [f2[0] + .32 * u, f2[1] + .08 * u], .2 * u, RENK.sac);
  const e2 = [sh[0] - sw * .45 * u - .05 * u, sh[1] + 1.25 * u], h2 = [e2[0] - sw * .35 * u + .1 * u, e2[1] + 1.1 * u];
  kapsul(sh, e2, .30 * u, tenU); kapsul(e2, h2, .25 * u, tenU);
  // pelerin (arkada dalgalanır)
  const fl = t => Math.sin(o.t * 5.2 - t * 2.6) * .22 * u;
  g.beginPath(); g.moveTo(neck[0] + .1 * u, neck[1] + .05 * u);
  g.quadraticCurveTo(sh[0] - .55 * u, sh[1] + .05 * u, sh[0] - .95 * u + fl(1), sh[1] + 1.3 * u);
  g.quadraticCurveTo(sh[0] - 1.45 * u + fl(2), sh[1] + 2.2 * u, hip[0] - 1.1 * u + fl(3), hip[1] + .9 * u);
  g.lineTo(hip[0] - .25 * u, hip[1] + .55 * u);
  g.quadraticCurveTo(sh[0] - .2 * u, sh[1] + 1.2 * u, sh[0] + .3 * u, sh[1] + .1 * u);
  g.closePath(); fill(C(1, 0, 0));
  // yakın bacak
  kapsul(hip, k1, .42 * u, tenB); kapsul(k1, f1, .32 * u, tenB);
  kapsul([f1[0] - .1 * u, f1[1] + .05 * u], [f1[0] + .34 * u, f1[1] + .08 * u], .2 * u, RENK.sac);
  // khiton: omuzdan kalça altına, kemerli
  g.beginPath();
  g.moveTo(sh[0] - .42 * u, sh[1] + .05 * u); g.lineTo(sh[0] + .42 * u, sh[1] - .02 * u);
  g.quadraticCurveTo(sh[0] + .58 * u, sh[1] + 1.2 * u, hip[0] + .45 * u, hip[1] - .2 * u);
  g.lineTo(hip[0] + .62 * u + sw * .08 * u, hip[1] + .85 * u);
  g.quadraticCurveTo(hip[0], hip[1] + 1.0 * u, hip[0] - .62 * u, hip[1] + .80 * u);
  g.lineTo(hip[0] - .42 * u, hip[1] - .2 * u);
  g.quadraticCurveTo(sh[0] - .6 * u, sh[1] + 1.2 * u, sh[0] - .42 * u, sh[1] + .05 * u);
  g.closePath(); fill(RENK.khiton);
  line([[hip[0] - .45 * u, hip[1] - .35 * u], [hip[0] + .48 * u, hip[1] - .4 * u]], .14 * u, C(.9, 0, .3));
  // baş
  bas({ x: neck[0] + .52 * u, y: neck[1] - .38 * u, s: u, r: (o.bakis || 0) + lean * .5, tip: 'antik', goz: 1, isik: 0, sw: Math.sin(o.t * 4) * .02, ten: tenB });
  // yakın kol + iki mızrak
  const e1 = [sh[0] + sw * .35 * u + .25 * u, sh[1] + 1.2 * u], h1 = [e1[0] + .55 * u, e1[1] + .6 * u];
  const ma = -1.12 + sw * .05;
  for (const dd of [0, .22 * u]) {
    const a = [h1[0] - Math.cos(ma) * 1.4 * u + dd, h1[1] - Math.sin(ma) * 1.4 * u], b = [h1[0] + Math.cos(ma) * 4.0 * u + dd, h1[1] + Math.sin(ma) * 4.0 * u];
    line([a, b], .09 * u, C(1, .2, 0));
    const tx = Math.cos(ma), ty = Math.sin(ma);
    g.beginPath(); g.moveTo(b[0] + tx * .55 * u, b[1] + ty * .55 * u); g.lineTo(b[0] - ty * .1 * u, b[1] + tx * .1 * u); g.lineTo(b[0] + ty * .1 * u, b[1] - tx * .1 * u); g.closePath(); fill(C(1, 0, .2));
  }
  kapsul(sh, e1, .32 * u, tenB); kapsul(e1, h1, .27 * u, tenB);
  g.beginPath(); g.arc(h1[0], h1[1], .17 * u, 0, 7); fill(tenB);
  // omuzdaki pelerin önü + toka
  g.beginPath(); g.moveTo(sh[0] - .5 * u, sh[1] - .05 * u); g.quadraticCurveTo(sh[0] + .1 * u, sh[1] - .25 * u, sh[0] + .45 * u, sh[1]); g.lineTo(sh[0] + .1 * u, sh[1] + .45 * u); g.quadraticCurveTo(sh[0] - .3 * u, sh[1] + .4 * u, sh[0] - .5 * u, sh[1] - .05 * u);
  fill(C(1, 0, 0));
  g.beginPath(); g.arc(sh[0] + .25 * u, sh[1] - .02 * u, .11 * u, 0, 7); fill(C(0, 1, 0));
  return { hip, sh, neck };
}

// Uzanmış genç: yüzüstü, dirseklere dayanmış, başı suya eğik. (x,y): yakın dirseğin zemindeki noktası. u: baş yüksekliği.
export function uzanan(o) {
  const u = o.u, x = o.x, y = o.y, nf = o.nefes || 0;
  const P = (a, b) => [x + a * u, y + b * u];
  const tenB = C(0, .38, 0), tenU = C(.2, .42, 0);
  const sh = P(-.8, -1.32 - nf * .03), hip = P(-3.3, -.5);
  // uzak bacak: dizden hafif bükük, alt bacak kalkık (dinlenen)
  const k2 = P(-5.15, -.36), f2 = P(-6.2, -1.05 + Math.sin(o.t * 1.1) * .05);
  kapsul(hip, k2, .56 * u, tenU); kapsul(k2, f2, .40 * u, tenU);
  kapsul(f2, [f2[0] - .05 * u, f2[1] - .32 * u], .24 * u, RENK.sac);
  // uzak kol: önkol yerde
  kapsul(sh, P(-.45, -.2), .36 * u, tenU); kapsul(P(-.45, -.2), P(.65, -.17), .30 * u, tenU);
  // yakın bacak düz
  const k1 = P(-5.2, -.3), f1 = P(-7.05, -.28);
  kapsul(hip, k1, .58 * u, tenB); kapsul(k1, f1, .42 * u, tenB);
  kapsul(f1, [f1[0] - .08 * u, f1[1] - .34 * u], .24 * u, RENK.sac);
  // gövde (khiton): kalçadan göğse yükselen dolgun biçim
  g.beginPath();
  g.moveTo(...P(-4.15, -.12));
  g.bezierCurveTo(...P(-3.9, -1.05), ...P(-2.4, -1.55), ...P(-1.0, -2.0 - nf * .05));
  g.quadraticCurveTo(...P(-.25, -2.15 - nf * .05), ...P(-.05, -1.6));
  g.quadraticCurveTo(...P(.0, -1.0), ...P(-.55, -.62));
  g.bezierCurveTo(...P(-1.4, -.2), ...P(-2.6, -.02), ...P(-4.15, -.12));
  g.closePath(); fill(RENK.khiton);
  line([P(-2.95, -.08), P(-2.75, -1.25)], .16 * u, C(.9, 0, .3));
  // pelerin: omuzdan sırta, kalçaya dökülür
  g.beginPath();
  g.moveTo(...P(-.25, -2.05 - nf * .05));
  g.bezierCurveTo(...P(-1.3, -2.25), ...P(-2.6, -1.75), ...P(-3.45, -1.05));
  g.quadraticCurveTo(...P(-3.95, -.6), ...P(-3.85, -.12));
  g.lineTo(...P(-2.7, -.1));
  g.quadraticCurveTo(...P(-2.2, -.7), ...P(-1.2, -1.0));
  g.quadraticCurveTo(...P(-.55, -1.1), ...P(-.25, -2.05 - nf * .05));
  g.closePath(); fill(RENK.khlamys);
  curve([P(-.6, -1.95), P(-1.8, -1.7), P(-2.9, -1.0)], .05 * u, C(.6, 0, 1));
  // baş: suya eğik (pivot = çene/dudak)
  const bx = x + (o.basX ?? .55) * u, by = y + (o.basY ?? -1.25) * u;
  const bm = bas({ x: bx, y: by, s: u, r: o.basR ?? .95, tip: 'antik', goz: o.goz ?? .8, isik: .8, sw: Math.sin(o.t * 2.1) * .015, ten: tenB });
  g.beginPath(); g.arc(...P(-.45, -1.95), .08 * u, 0, 7); fill(C(0, 1, 0));
  // yakın kol: dirsek omzun altında yerde, önkol ileri; 'âşık'ta el suya doğru uzanır (o.uzan 0..1)
  const uz = o.uzan || 0;
  const dj = [x + lerp(-.25, .35, uz) * u, y + lerp(-.18, -.3, uz) * u];
  const el = [x + lerp(.95, 1.75, uz) * u, y + lerp(-.15, .3, uz) * u];
  kapsul(sh, dj, .40 * u, tenB); kapsul(dj, el, .32 * u, tenB);
  g.beginPath(); g.ellipse(el[0] + .12 * u, el[1], .22 * u, .13 * u, uz * .5, 0, 7); fill(tenB);
  return bm;
}
