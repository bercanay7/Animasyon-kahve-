// Ana döngü (Mary Stuart): render=1 ile yalnız window.renderFrame; yoksa canlı önizleme (?t= ?still)
'use strict';
const Q = new URLSearchParams(location.search);
const CV = document.getElementById('c'), CG = CV.getContext('2d');
window.FPS = 30;
function renderFrame(t) { renderFrameTo(CG, t); return CV; }
window.renderFrame = renderFrame;
window.ready = (async () => {
  const TR = 'AaĞğİıŞşÖöÜüÇçÂâ“”’…–·';
  for (const f of ['400 40px Cinzel', '700 40px Cinzel', 'italic 500 40px "Cormorant Garamond"', 'italic 600 40px "Cormorant Garamond"', '600 40px "Cormorant Garamond"']) await document.fonts.load(f, TR);
  await Promise.all(Object.entries(window.GORSEL || {}).map(([k, v]) => loadImg(k, v)));
  if (window.initSahne) initSahne();
  return true;
})();
if (!Q.has('render')) window.ready.then(() => {
  if (Q.has('still')) { renderFrame(+Q.get('t') || 0); window.READY = true; return; }
  const t0 = performance.now() / 1000 - (+Q.get('t') || 0);
  const loop = () => { renderFrame(performance.now() / 1000 - t0); requestAnimationFrame(loop); }; loop();
});
else window.ready.then(() => { window.READY = true; });
