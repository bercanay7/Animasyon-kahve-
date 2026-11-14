// Ana döngü: kare çizimi, (isteğe bağlı) hareket bulanıklığı, canlı önizleme
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
cv.width = DW; cv.height = DH;
const Q = new URLSearchParams(location.search);
window.FPS = 30;
const acc = makeCanvas(DW, DH), accx = acc.getContext('2d');
function renderFrame(t) {
  baseT(ctx); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = '#F3E6CC'; ctx.fillRect(0, 0, W, H);
  drawFilm(ctx, t);
  if (!window.IN_MB && !Q.get('scene')) drawOver(ctx, t);
}
// Hareket bulanıklığı yalnız çekim mb: n verirse (hızlı düşüş); düz mürekkep kenarı keskin kalır.
function renderFrameMB(t, n) {
  const si = SHOTS.length ? shotAt(t) : -1, sh = si >= 0 ? SHOTS[si] : null;
  n = sh && sh.mb ? sh.mb : 1;
  if (n <= 1) { renderFrame(t); return; }
  const dt = 1 / FPS * .5, lo = sh.at, hi = si + 1 < SHOTS.length ? SHOTS[si + 1].at - 1e-4 : Infinity;
  accx.setTransform(1, 0, 0, 1, 0, 0); accx.globalAlpha = 1; accx.globalCompositeOperation = 'source-over';
  window.IN_MB = true;
  for (let i = 0; i < n; i++) { renderFrame(Math.max(0, Math.min(hi, Math.max(lo, t + dt * (i / n - .5))))); accx.globalAlpha = 1 / (i + 1); accx.drawImage(cv, 0, 0); }
  window.IN_MB = false;
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.drawImage(acc, 0, 0);
  if (!Q.get('scene')) drawOver(ctx, t);
}
window.renderFrame = renderFrame; window.renderFrameMB = renderFrameMB;
window.ready = (async () => {
  const TR = 'AaĞğİıŞşÖöÜüÇçÂâ“”’…–·';
  for (const f of ['400 40px "Bebas Neue"', '500 40px "Hanken Grotesk"', '600 40px "Hanken Grotesk"']) await document.fonts.load(f, TR);
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
