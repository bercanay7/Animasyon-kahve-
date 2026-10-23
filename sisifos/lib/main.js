// Ana döngü: kare çizimi, hareket bulanıklığı, canlı önizleme
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const Q = new URLSearchParams(location.search);
window.FPS = 30;
const acc = makeCanvas(W, H), accx = acc.getContext('2d');
function renderFrame(t) {
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
  drawFilm(ctx, t);
}
// 180° obtüratör: kare süresinin yarısı içinde n alt kare ortalaması
function renderFrameMB(t, n) {
  const dt = 1 / FPS * .5;
  accx.setTransform(1, 0, 0, 1, 0, 0); accx.globalAlpha = 1; accx.globalCompositeOperation = 'source-over';
  for (let i = 0; i < n; i++) {
    renderFrame(t + dt * (i / n - .5));
    accx.globalAlpha = 1 / (i + 1);
    accx.drawImage(cv, 0, 0);
  }
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
  ctx.drawImage(acc, 0, 0);
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
