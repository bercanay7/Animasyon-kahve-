// Ana döngü (Gılgamış; narkissos/lib/main.js'ten). ORTAK DOSYA (başkan).
// film.html?t=…&mb=… tek kare; window.renderAt(t, mb) → tuval; window.READY (true olunca hazır). ?notext=1 ekran yazısız; ?rs=0.5 animatik çözünürlüğü.
// Hareket bulanıklığı: 180° obtüratör, kare süresinin yarısında mb alt kare ortalaması; alt kareler kesmenin öbür yanına taşmaz.
// Çekim kendi mb'sini verebilir (plan(..., {mb: 8}): hızlı hareket); yazılar (drawOver) bulanıklıktan sonra bir kez çizilir.
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
cv.width = DW; cv.height = DH;
const Q = new URLSearchParams(location.search);
window.FPS = 30;
const acc = makeCanvas(DW, DH), accx = acc.getContext('2d');
function renderFrame(t) {
  window.FIG_T = t;
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
  ctx.fillStyle = '#000'; ctx.fillRect(0, 0, DW, DH);
  drawFilm(ctx, t);
  if (!window.IN_MB) drawOver(ctx, t);
}
function renderFrameMB(t, n) {
  const si = SHOTS.length ? shotAt(t) : -1, sh = si >= 0 ? SHOTS[si] : null;
  if (sh && sh.mb) n = Math.max(n, sh.mb);
  if (n <= 1) { renderFrame(t); return; }
  const dt = 1 / FPS * .5, lo = sh ? sh.at : 0, hi = si >= 0 && si + 1 < SHOTS.length ? SHOTS[si + 1].at - 1e-4 : Infinity;
  accx.setTransform(1, 0, 0, 1, 0, 0); accx.globalAlpha = 1; accx.globalCompositeOperation = 'source-over';
  window.IN_MB = true;
  for (let i = 0; i < n; i++) { renderFrame(Math.max(0, Math.min(hi, Math.max(lo, t + dt * (i / n - .5))))); accx.globalAlpha = 1 / (i + 1); accx.drawImage(cv, 0, 0); }
  window.IN_MB = false;
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.drawImage(acc, 0, 0);
  window.FIG_T = t; drawOver(ctx, t);
}
function renderAt(t, mb = 1) { if (mb > 1) renderFrameMB(t, mb); else renderFrame(t); return cv; }
window.renderFrame = renderFrame; window.renderFrameMB = renderFrameMB; window.renderAt = renderAt;
window.READY = false;
// kurgu araçları için: normalleştirilmiş çekim listesi [{id, at, end, tr}]
window.shotList = () => { shotsReady(); return SHOTS.map((s, i) => ({ id: s.id || null, at: +s.at.toFixed(3), end: +(SHOTS[i + 1] ? SHOTS[i + 1].at : DUR).toFixed(3), tr: s.tr ? s.tr.type : 'cut' })); };
window.ready = (async () => {
  const TR = 'AaĞğİıŞşÖöÜüÇçÂâ“”’…–·';
  for (const f of ['400 40px "Bebas Neue"', '400 40px Cinzel', '600 40px Cinzel', '700 40px Cinzel',
    'italic 500 40px "Cormorant Garamond"', 'italic 600 40px "Cormorant Garamond"', '500 40px "Cormorant Garamond"', '600 40px "Cormorant Garamond"']) await document.fonts.load(f, TR);
  KIL.init();
  postHazirla();
  shotsReady();
  window.READY = true;
  return true;
})();
window.ready.then(() => {
  if (Q.has('t')) { renderAt(+Q.get('t') || 0, +Q.get('mb') || 1); return; }
  if (Q.has('render')) return;
  const t0 = performance.now() / 1000; // canlı önizleme (yalnız tarayıcıda; render ve kare araçları renderAt kullanır)
  const loop = () => { renderFrame((performance.now() / 1000 - t0) % DUR); requestAnimationFrame(loop); };
  loop();
});
