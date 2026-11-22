// Ana döngü (milton/lib/main.js'ten): kare çizimi, canlı önizleme; hazırlık: fontlar, dokular, gerçek görseller, portre levhaları.
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
cv.width = DW; cv.height = DH;
const Q = new URLSearchParams(location.search);
window.FPS = 30;
function renderFrame(t) {
  baseT(ctx); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
  drawFilm(ctx, t);
  drawOver(ctx, t);
  return cv;
}
window.renderFrame = renderFrame;
const GORSELLER = { sarony23: 'gorsel/wilde_sarony1882_met285691.jpg', sarony18: 'gorsel/wilde_sarony1882_met283247.jpg', lippBaslik: 'gorsel/lippincott1890_07_baslik.jpg', lippDilek: 'gorsel/lippincott1890_07_s19_dilek.jpg',
  dore169: 'gorsel/dore1872_s169.jpg', dore245: 'gorsel/dore1872_s245.jpg', dore263: 'gorsel/dore1872_s263.jpg', dore275: 'gorsel/dore1872_s275.jpg', dore035: 'gorsel/dore1872_s035.jpg' };
window.ready = (async () => {
  try {
    const TR = 'AaĞğİıŞşÖöÜüÇçÂâ“”’…–·';
    for (const f of ['400 40px Cinzel', '600 40px Cinzel', '700 40px Cinzel', 'italic 500 40px "Cormorant Garamond"', 'italic 600 40px "Cormorant Garamond"', '500 40px "Cormorant Garamond"', '600 40px "Cormorant Garamond"']) await document.fonts.load(f, TR);
    buildTextures();
    await Promise.all(Object.entries(GORSELLER).map(([k, u]) => SET.yukle(k, u)));
    while (!window.PORTRE) await new Promise(r => setTimeout(r, 30));
    await window.PORTRE.hazir;
    if (window.initScenes) initScenes();
    window.READY = true;
    return true;
  } catch (e) { window.HATA = String(e && e.stack || e); console.error(e); throw e; }
})();
if (!Q.has('render')) window.ready.then(() => {
  const t0 = performance.now() / 1000 - (+Q.get('t') || 0);
  const loop = () => { renderFrame(performance.now() / 1000 - t0); requestAnimationFrame(loop); };
  if (Q.has('still')) renderFrame(+Q.get('t') || 0); else loop();
});
