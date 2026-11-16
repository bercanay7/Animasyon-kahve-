// Ana döngü (Ran): render=1 ile yalnız window.renderFrame; yoksa canlı önizleme (?t= ?still)
'use strict';
const Q = new URLSearchParams(location.search);
const CV = document.getElementById('c'), COMP = INKC.makeComp(CV), LA = INKC.layerSet();
window.FPS = 30;
function renderFrame(t) {
  LA.clear(); cam(LA);
  const i = shotAt(t), st = shotState(i, t);
  let o = {}; try { o = SHOTS[i].fn(LA, st) || {}; } catch (e) { console.log('[plan ' + SHOTS[i].id + '] ' + e.message); }
  COMP(LA, null, o);
  return CV;
}
window.renderFrame = renderFrame;
window.ready = (async () => {
  const TR = 'AaĞğİıŞşÖöÜüÇçÂâ“”’…–·';
  for (const f of ['400 40px "Bebas Neue"', '600 40px "Cormorant Garamond"', 'italic 500 40px "Cormorant Garamond"', '500 40px "Cormorant Garamond"']) await document.fonts.load(f, TR);
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
