// YANKI seti, SAHİP-2: P082. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md.
'use strict';
(() => {
  // P082 · geniş · F04 · LEVHA · Bugün: siyah sır zemin; 'narsist' kelimesi Eko'nun yankısı gibi her yönden, farklı boylarda belirip solar. Kişi yok (parmakla gösterme, yüz, alay yok)
  plan('P082', (ctx, st) => {
    const t = st.t, t0 = PE('P082', 0), t1 = PE('P082', 1), t2 = PE('P082', 2);
    baseT(ctx); glaze(ctx, 960, 560, 1100, 'rgba(90,36,18,.35)');
    camAt(ctx, ...s2_cam(st, [920, 520, 1.0], [1000, 520, 1.0]));
    // yankı yazıları: belirlenimci yer ve boy; her biri doğar, büyür, solar (Eko'nun yankısı: tekrar ettikçe soluk)
    const r = rng(82), N = 34;
    for (let i = 0; i < N; i++) {
      const x = 120 + r() * 1700, y = 150 + r() * 690, px = 26 + Math.round(r() * 70), born = i === 0 ? t0 : i < 6 ? lerp(t0 + .2, t1, i / 6) : lerp(t1, t2 + .8, (i - 6) / (N - 6)) + r() * .3;
      const u = (t - born) / 2.4; if (u <= 0 || u >= 1) continue;
      const a = clamp(u / .12) * (1 - u) * (i === 0 ? 1 : .8), k = 1 + .08 * u;
      ctx.save(); ctx.translate(i === 0 ? 960 : x, i === 0 ? 470 : y); ctx.scale(k, k); ctx.globalAlpha = a;
      ctx.font = FONT.alinti(i === 0 ? 110 : px, 600); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = i % 3 === 0 ? '#E0905A' : '#F2E6CE';
      ctx.fillText('narsist', 0, 0); ctx.restore();
    }
    baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
  });
})();
