// Baskı yazısı katmanı: belgelerdeki yazılar (defter, broşür, sözleşme, gazete) gravür geçişinde kuyruğa yazılır,
// basmadan sonra mürekkep renginde, kamera dönüşümüyle ve hafif baskı pürüzüyle basılır (çizgiye çevrilmez, okunur kalır).
// YAZI.ekle(s, x, y, {px, font: 'serif'|'baslik'|'el', align, a, renk: [r,g,b], rot})  (dünya koordinatı)
// YAZI.bas(ctx, cam)  levhadan sonra; LALE.boya'dan önce ya da sonra fark etmez (çarpma)
'use strict';
const YAZI = (() => {
  let Q = [];
  const F = { serif: (px, w = 600) => `${w} ${px}px "Cormorant Garamond"`, italik: (px, w = 600) => `italic ${w} ${px}px "Cormorant Garamond"`, baslik: (px, w = 700) => `${w} ${px}px Cinzel`, el: (px) => `italic 500 ${px}px "Cormorant Garamond"` };
  function ekle(s, x, y, o = {}) { Q.push({ s: String(s), x, y, o }); }
  function bas(ctx, cam) {
    if (!Q.length) return;
    const c = camOf(cam) || { x: 0, y: 0, s: 1 }, z = c.s * RS;
    ctx.save(); ctx.setTransform(z, 0, 0, z, -c.x * z, -c.y * z); ctx.globalCompositeOperation = 'multiply';
    for (const { s, x, y, o } of Q) {
      const px = o.px || 32, rn = o.renk || GR.INK;
      ctx.save(); ctx.translate(x, y); if (o.rot) ctx.rotate(o.rot);
      ctx.font = (F[o.font] || F.serif)(px, o.w); ctx.textAlign = o.align || 'left'; ctx.textBaseline = 'alphabetic';
      if (o.ls) ctx.letterSpacing = o.ls + 'px';
      ctx.globalAlpha = clamp(o.a ?? .92);
      ctx.fillStyle = `rgb(${rn[0]},${rn[1]},${rn[2]})`;
      if (o.kadar != null) { // yazılarak beliren metin (el yazısı): ilk 'kadar' oranı kadar karakter
        const n = Math.round(s.length * clamp(o.kadar)); ctx.fillText(s.slice(0, n), 0, 0);
      } else ctx.fillText(s, 0, 0);
      ctx.restore();
    }
    ctx.restore();
  }
  return { ekle, bas, sifirla: () => { Q = []; } };
})();
