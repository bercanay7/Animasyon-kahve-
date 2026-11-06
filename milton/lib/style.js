// Ortak yardımcılar: tuval, kâğıt dokusu, vinyet, kumlanma (gravür baskısı için)
'use strict';
function makeCanvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
const TEX = {};
function buildTextures() {
  // kâğıt lifi: düşük frekanslı leke + ince lif, çarpma ile uygulanır
  const s = 512, c = makeCanvas(s, s), x = c.getContext('2d'), d = x.createImageData(s, s), r = rng(3);
  for (let i = 0; i < s * s; i++) {
    const px = i % s, py = (i / s) | 0;
    const v = 238 + (noise2(px / 64, py / 64, 1) - .5) * 14 + (noise2(px / 9, py / 3, 2) - .5) * 8 + (r() - .5) * 6;
    d.data[i * 4] = d.data[i * 4 + 1] = d.data[i * 4 + 2] = clamp(v, 0, 255); d.data[i * 4 + 3] = 255;
  }
  x.putImageData(d, 0, 0); TEX.paper = c;
}
function applyPaper(ctx, amt = 1) {
  ctx.save(); ctx.setTransform(RS, 0, 0, RS, 0, 0);
  ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = .55 * amt;
  ctx.fillStyle = ctx.createPattern(TEX.paper, 'repeat'); ctx.fillRect(0, 0, W, H);
  ctx.restore();
}
function applyVignette(ctx, amt = 1) {
  ctx.save(); ctx.setTransform(RS, 0, 0, RS, 0, 0);
  const g = ctx.createRadialGradient(W / 2, H / 2, H * .35, W / 2, H / 2, H * 1.05);
  g.addColorStop(0, 'rgba(20,16,12,0)'); g.addColorStop(1, `rgba(20,16,12,${.55 * amt})`);
  ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  ctx.restore();
}
