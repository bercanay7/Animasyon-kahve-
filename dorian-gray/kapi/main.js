// Dorian Gray üslup kapısı: aday seçici ve İMPASTO çizici.
//   ?mod=gravur  milton/lib gravür motoru (gravur_mod.js)
//   ?mod=impasto Lemo-Opuscar impasto motoru (vendor/, MIT): bütün sahne bıçak darbesi yağlıboya
//   ?mod=karma   dünya gravür, yalnız portrenin tuvali impasto (tek renkli istisna)
//   ?kapak=1     kapak denemesi (t = 3,1 sn; yazı "KİMSE GÖRMEDİ")
// window.renderAt(t) → 1920×1080 tuval; window.READY.
import { Impasto, Strokes, DAB, KNIFE, hex } from './vendor/impasto.js';
import { Ref, paintRef } from './vendor/plate.js';

const Q = new URLSearchParams(location.search), MOD = Q.get('mod') || 'gravur';
const SH = window.SAHNE, out = document.getElementById('c'), ctx = out.getContext('2d');
const mul = (A, B) => [A[0] * B[0] + A[2] * B[1], A[1] * B[0] + A[3] * B[1], A[0] * B[2] + A[2] * B[3], A[1] * B[2] + A[3] * B[3], A[0] * B[4] + A[2] * B[5] + A[4], A[1] * B[4] + A[3] * B[5] + A[5]];
const TRm = (x, y) => [1, 0, 0, 1, x, y];
const TRf = T => { if (!T) return [1, 0, 0, 1, 0, 0]; const c = Math.cos(T.a || 0) * (T.k || 1), s = Math.sin(T.a || 0) * (T.k || 1); return [c, s, -s, c, T.x, T.y]; };

// ── impasto levhaları ──
// her levhanın yerel kapsamı (ox, oy: yerel → ref birimine kaydırma; w, h: ref birimi) ve ref ölçeği
const KAP = { oda: { ox: 40, oy: 40, w: 2000, h: 1160, s: .5, R: [30, 15, 7.5, 3.5], T: 14 },
  portre: { ox: -1080, oy: -110, w: 520, h: 740, s: 1.3, R: [26, 13, 6.5, 3.2, 1.8], T: 10 },
  ortu: { ox: 20, oy: 10, w: 580, h: 780, s: .7, R: [24, 12, 6, 3], T: 12 },
  dorian: { ox: 120, oy: 810, w: 240, h: 820, s: .9, R: [20, 10, 5, 2.6], T: 12 },
  kol: { ox: 20, oy: 30, w: 380, h: 60, s: 1.2, R: [10, 5, 2.6], T: 12 } };
let E, PL = {}, dyn, gl;
function refAdaptor(Rf) {
  return {
    fill(pf, o) { Rf.fill(pf, o.c, Object.assign({ seed: 1 }, o.p || {})); },
    line(pf, c, w, o = {}) { Rf.line(pf, c, w, Object.assign({}, o.p || {})); },
    tint(pf, f, comp) { Rf.tint(pf, f, comp); }
  };
}
function yapLevha(ad, isikli) {
  const K = KAP[ad], Rf = new Ref(K.w, K.h, K.s);
  Rf.ctx.translate(K.ox, K.oy); Rf.idc.translate(K.ox, K.oy);
  SH.LEV[ad].draw(refAdaptor(Rf));
  if (isikli) {   // lamba ışığı referansa işlenir (screen); levha yerel koordinatı dünya koordinatıyla aynı (oda, portre)
    const L = SH.LEV.oda.light, c = Rf.ctx; c.save(); c.globalCompositeOperation = 'source-atop';
    const g = c.createRadialGradient(L.x, L.y, L.r0, L.x, L.y, L.r1);
    g.addColorStop(0, 'rgba(255,200,120,.55)'); g.addColorStop(.3, 'rgba(255,180,100,.25)'); g.addColorStop(.7, 'rgba(255,160,90,.06)'); g.addColorStop(1, 'rgba(255,160,90,0)');
    c.globalCompositeOperation = 'screen'; c.fillStyle = g; c.fillRect(-200, -200, 2400, 1500); c.restore();
  }
  const st = paintRef(Rf, { R: K.R, T: K.T, seed: 7 + ad.length });
  return { b: E.batch(st.data()), tex: E.texture(Rf.ctx.canvas), K, n: st.n };
}
function impKur(canvas, adlar) {
  E = new Impasto(canvas, { W: 1920, H: 1080, ss: 2 }); dyn = new Strokes(256);
  for (const ad of adlar) PL[ad] = yapLevha(ad, ad === 'oda' || ad === 'portre');
}
function levhaCiz(ad, T, cam) {
  const pl = PL[ad], M = mul(TRf(T), TRm(-pl.K.ox, -pl.K.oy));
  E.under(pl.tex, pl.K.w, pl.K.h, { M, cam }); E.draw(pl.b, { M, cam, t: 10 });
}
function alevImp(t, cam) {
  const f = SH.alev(t); dyn.clear();
  dyn.push({ x: f.x, y: f.y - 10, ang: 0, len: 260, wid: 220, c: hex('#ffb060'), type: DAB, alpha: .10, seed: 1, hgt: 0 });
  dyn.push({ x: f.x, y: f.y - 14, ang: 0, len: 120, wid: 100, c: hex('#ffc070'), type: DAB, alpha: .22, seed: 2, hgt: 0 });
  dyn.push({ x: f.x + f.lean * 30, y: f.y - 18 * f.s, ang: -Math.PI / 2 + f.lean, len: 52 * f.s, wid: 20, c: hex('#ffd890'), c2: hex('#fff6dc'), type: KNIFE, seed: 3, hgt: .8, taper: .7 });
  dyn.push({ x: f.x + f.lean * 20, y: f.y - 12 * f.s, ang: -Math.PI / 2 + f.lean, len: 26 * f.s, wid: 10, c: hex('#fffbea'), type: DAB, seed: 4, hgt: 1 });
  E.drawNow(dyn.data(), { cam, t: 10 });
}
const POST = { expo: 1.05, sat: 1.04, contrast: 1.06, vig: .34, spec: .22, shin: 26, lightCol: [1, .93, .8], ground: [.12, .09, .07] };
function impCiz(t, adlar) {
  const c = SH.cam(t), cam = { x: c.cx, y: c.cy, zoom: c.z, rot: 0 };
  E.begin(POST.ground);
  for (const [ad, fn] of SH.SIRA) if (adlar.includes(ad)) levhaCiz(ad, fn ? fn(t) : null, cam);
  if (adlar.includes('oda')) alevImp(t, cam);
  E.finish(POST);
}

// ── karma: portre tuvali impasto, gerisi gravür; maske = tuval dikdörtgeni − örtü ──
const mask = document.createElement('canvas'); mask.width = 1920; mask.height = 1080; const mx = mask.getContext('2d');
function karmaBindir(t) {
  const c = SH.cam(t), z = c.z, V = [z, 0, 0, z, 960 - c.cx * z, 540 - c.cy * z];
  mx.setTransform(1, 0, 0, 1, 0, 0); mx.clearRect(0, 0, 1920, 1080); mx.globalCompositeOperation = 'source-over';
  mx.setTransform(...V); mx.fillStyle = '#fff'; mx.fillRect(SH.IN.x, SH.IN.y, SH.IN.w, SH.IN.h);
  const O = SH.ortuT(t), M = mul(V, TRf(O)); mx.setTransform(...M); mx.globalCompositeOperation = 'destination-out';
  mx.beginPath(); mx.moveTo(0, 0); mx.lineTo(SH.OW, 0); mx.lineTo(SH.OW + 6, SH.OH); mx.lineTo(-8, SH.OH); mx.closePath(); mx.fill();
  mx.globalCompositeOperation = 'source-in'; mx.setTransform(1, 0, 0, 1, 0, 0); mx.drawImage(gl, 0, 0);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(mask, 0, 0); ctx.restore();
}

function renderAt(t) {
  if (MOD === 'gravur') GRAVUR.draw(ctx, t);
  else if (MOD === 'impasto') { impCiz(t, ['oda', 'portre', 'ortu', 'dorian', 'kol']); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(gl, 0, 0); }
  else { GRAVUR.draw(ctx, t); impCiz(t, ['portre']); karmaBindir(t); }
  if (Q.get('kapak') === '1') kapakYazi();
  return out;
}
function kapakYazi() {
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.font = '300px "Bebas Neue"'; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
  ctx.lineWidth = 14; ctx.strokeStyle = 'rgba(10,8,6,.85)'; ctx.lineJoin = 'round';
  for (const [s, y] of [['KİMSE', 330], ['GÖRMEDİ', 600]]) { ctx.strokeText(s, 70, y); ctx.fillStyle = '#efe4cc'; ctx.fillText(s, 70, y); }
  ctx.restore();
}
(async () => {
  try {
    out.width = 1920; out.height = 1080;
    await document.fonts.load('300px "Bebas Neue"', 'KİMSE GÖRMEDİ');
    buildTextures();
    if (MOD !== 'gravur') { gl = document.createElement('canvas'); impKur(gl, MOD === 'impasto' ? ['oda', 'portre', 'ortu', 'dorian', 'kol'] : ['portre']); }
    window.renderAt = renderAt;
    window.STROKES = Object.fromEntries(Object.entries(PL).map(([k, v]) => [k, v.n]));
    if (!Q.has('render')) renderAt(+(Q.get('t') || 3.1));
    window.READY = true;
  } catch (e) { window.HATA = String(e && e.stack || e); console.error(e); }
})();
