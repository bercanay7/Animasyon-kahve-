// Kare döngüsü: index.html?t=…&mb=… tek kare çizer; window.renderAt(t, mb) ve window.READY (render betiği için).
// Hareket bulanıklığı: 180° obtüratör, kare süresinin yarısında mb alt kare (milton/lib/main.js renderFrameMB gibi); alt kareler plan sınırını aşmaz.
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
cv.width = CW; cv.height = CH;
const FPS = 30;
const acc = makeCanvas(CW, CH), accx = acc.getContext('2d');
function renderSub(t) {
  window.FIG_T = t;
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, CW, CH);
  drawScene(ctx, t);
}
function renderAt(t, mb = 1) {
  const fi = Math.round(t * FPS);
  if (Qs.get('kapak')) { renderKapak(ctx, Qs.get('kapak')); return cv; }
  if (mb <= 1) renderSub(t);
  else {
    const p = DIKEY ? { t0: 10.5, t1: 16 } : ZAMAN.plan(t), lo = p.t0, hi = p.t1 - 1e-4, dt = 1 / FPS * .5;
    accx.setTransform(1, 0, 0, 1, 0, 0); accx.globalAlpha = 1; accx.globalCompositeOperation = 'source-over';
    for (let i = 0; i < mb; i++) {
      renderSub(clamp(t + dt * (i / mb - .5), lo, hi));
      accx.globalAlpha = 1 / (i + 1); accx.drawImage(cv, 0, 0);
    }
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.drawImage(acc, 0, 0);
  }
  post(ctx, fi);
  return cv;
}
window.renderAt = renderAt;
window.READY = false;
(async () => {
  const j = await (await fetch('../ortak/zaman.json')).json(); ZAMAN.yukle(j);
  await document.fonts.load('400 100px "Bebas Neue"', 'O BENİM');
  buildTextures();
  window.READY = true;
  if (Qs.has('t') || Qs.has('kapak')) renderAt(+Qs.get('t') || 0, +Qs.get('mb') || 1);
})();
