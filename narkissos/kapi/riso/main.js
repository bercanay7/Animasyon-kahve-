// Narkissos risograf adayı: kare üretimi. window.renderAt(t, mb) tek kare basar; window.READY / window.HAZIR hazır işaretidir.
// ?t=…&mb=… ile açılışta o kare basılır; ?kapak=1 (yazılı) / ?kapak=0 (yazısız); ?w=1080&h=1920 dikey (D planı).
import { makeRiso } from './vendor/riso.js';
import { W, H, plate, g, clear } from './vendor/draw.js';
import { PLAN, kayit, maskC, maskeTemizle, kapakCiz, kapakParam } from './sahne.js';

const Q = new URLSearchParams(location.search);
const out = document.getElementById('c'); out.width = W; out.height = H;
const print = makeRiso(out, W, H);
const INKS = [[61, 85, 136], [255, 181, 17], [0, 131, 138]];   // Federal Blue, Sunflower, Teal
const FPS = 30;

// hareket bulanıklığı: plaka ve maske tuvalleri alt karelerde çizilip ortalanır, baskı bir kez yapılır
const mk = () => { const c = document.createElement('canvas'); c.width = W; c.height = H; return [c, c.getContext('2d', { alpha: false })]; };
const [accP, AP] = mk(), [accM, AM] = mk();

function cizAlt(t, tc, id) {
  clear(); maskeTemizle();
  g.setTransform(1, 0, 0, 1, 0, 0);
  PLAN[id].ciz(t, tc);
  if (id === 'D') PLAN.D.parilti(t);
  g.setTransform(1, 0, 0, 1, 0, 0);
}

window.renderAt = function (t, mb) {
  const n = Math.max(1, mb ?? +(Q.get('mb') || 1));
  const f = Math.round(t * FPS);
  const tc = Math.floor(f / 2) * 2 / FPS;                // karakterler ikişerli (15 fps)
  const p = window.ZAMAN.plan(t), id = p.id;
  if (Q.has('kapak')) {
    clear(); maskeTemizle(); kapakCiz(Q.get('kapak') === '1'); g.setTransform(1, 0, 0, 1, 0, 0);
    const o = kapakParam();
    print(plate, maskC, { inks: INKS, seed: 7, sheet: 2.5, off: [[0, 0], [2, -2], [-2, 2]], rot: [0, .0004, -.0003], period: 7, grain: .5, boil: .35, ...o });
    return out;
  }
  const lo = p.t0, hi = p.t1 - 1e-4;
  if (n <= 1) cizAlt(t, tc, id);
  else {
    const dt = 1 / FPS * .5;   // 180° obtüratör
    for (let i = 0; i < n; i++) {
      const ts = Math.min(hi, Math.max(lo, t + dt * ((i + .5) / n - .5)));
      cizAlt(ts, tc, id);
      AP.globalAlpha = 1 / (i + 1); AP.drawImage(plate, 0, 0);
      AM.globalAlpha = 1 / (i + 1); AM.drawImage(maskC, 0, 0);
    }
  }
  const o = PLAN[id].param(t);
  print(n <= 1 ? plate : accP, n <= 1 ? maskC : accM, {
    inks: INKS, seed: Math.floor(f / 2), sheet: 'ABCDE'.indexOf(id) * 3.7 + 1, off: kayit(t, id), rot: [0, .0005, -.0004],
    period: 7, grain: .55, boil: .35, ...o,
  });
  return out;
};

(async () => {
  await Promise.all(['400 300px "Bebas Neue"'].map(f => document.fonts.load(f, 'O BENİM')));
  const j = await (await fetch('../ortak/zaman.json')).json();
  window.ZAMAN.yukle(j);
  if (Q.has('t') || Q.has('kapak')) window.renderAt(+(Q.get('t') || 0));
  window.READY = window.HAZIR = true;
})().catch(e => { window.HATA = String(e && e.stack || e); console.error(e); });
