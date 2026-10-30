// Ana döngü: kare çizimi, hareket bulanıklığı, canlı önizleme
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
cv.width = DW; cv.height = DH;
const Q = new URLSearchParams(location.search);
window.FPS = 30;
const acc = makeCanvas(DW, DH), accx = acc.getContext('2d');
function renderFrame(t) {
  window.FIG_T = t;
  baseT(ctx);
  ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
  drawFilm(ctx, t);
  if (!window.IN_MB && typeof drawOver === 'function' && !Q.get('scene')) drawOver(ctx, t);
}
// hızlı kamera hareketleri: fazla alt kare ve 360° obtüratör (dört alt karede hareket dört ayrı kopya görünmesin)
// [başlangıç, bitiş, alt kare]; zamanlar kilitli zaman çizelgesine göre (üslup kurulu tur 3)
let _mbWin = null;
function mbWindows() {
  if (_mbWin) return _mbWin;
  const J4 = typeof A === 'function' ? A('J04@prometeus') : 1081.45;
  return (_mbWin = [[4.75, 5.05, 12], [23.0, 23.55, 12], [87.85, 88.65, 12], [J4 - .02, J4 + .6, 16]]);
}
// 180° obtüratör: kare süresinin yarısı içinde n alt kare ortalaması
function renderFrameMB(t, n) {
  const si = typeof SHOTS !== 'undefined' ? shotAt(t) : -1, sh = si >= 0 ? SHOTS[si] : null;
  if (sh && sh.mb) n = Math.max(n, sh.mb);
  let wide = false;
  for (const [a, b, m] of mbWindows()) if (t >= a && t <= b) { n = Math.max(n, m); wide = true; }
  const dt = 1 / FPS * (wide ? 1 : .5);
  // alt kareler kesmenin öbür yanına taşmaz: her örnek o anki planın [başlangıç, sonraki plan) aralığına kısılır (kesmede tek karelik bindirme olmaz)
  const lo = sh ? sh.at : 0, hi = si >= 0 && si + 1 < SHOTS.length ? SHOTS[si + 1].at - 1e-4 : Infinity;
  accx.setTransform(1, 0, 0, 1, 0, 0); accx.globalAlpha = 1; accx.globalCompositeOperation = 'source-over';
  window.FRAME_T = t; // ayrık değişen öğeler (sayaçlar) alt karelerde değil karenin kendisinde değişsin
  window.IN_MB = true;
  for (let i = 0; i < n; i++) {
    renderFrame(Math.max(0, Math.min(hi, Math.max(lo, t + dt * (i / n - .5)))));
    accx.globalAlpha = 1 / (i + 1);
    accx.drawImage(cv, 0, 0);
  }
  window.FRAME_T = null; window.IN_MB = false;
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  ctx.drawImage(acc, 0, 0);
  if (typeof drawOver === 'function' && !new URLSearchParams(location.search).get('scene')) { window.FIG_T = t; drawOver(ctx, t); }
}
window.renderFrame = renderFrame; window.renderFrameMB = renderFrameMB;
window.ready = (async () => {
  // unicode-range ile bölünmüş yüzler (latin + latin-ext) Türkçe harflerle birlikte önceden yüklenir
  const TR = 'AaĞğİıŞşÖöÜüÇçÂâ“”’…–·';
  for (const f of ['400 40px Cinzel', '600 40px Cinzel', '700 40px Cinzel', '900 40px Cinzel',
    'italic 500 40px "Cormorant Garamond"', 'italic 600 40px "Cormorant Garamond"', '500 40px "Cormorant Garamond"', '600 40px "Cormorant Garamond"',
    '400 40px "Courier Prime"', '700 40px "Courier Prime"']) await document.fonts.load(f, TR);
  buildTextures();
  if (window.initScenes) initScenes();
  return true;
})();
if (!Q.has('render')) {
  window.ready.then(() => {
    const t0 = performance.now() / 1000 - (+Q.get('t') || 0);
    const loop = () => { renderFrame(performance.now() / 1000 - t0); requestAnimationFrame(loop); };
    if (Q.has('still')) renderFrame(+Q.get('t') || 0); else loop();
  });
}
