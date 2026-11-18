// DAG seti, SAHİP-2: P066, P069, P091. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Eko görünmez ya da yalnız kayaya karışmış karanlık siluet (yüzü yapraklı dalla örtülü); yankı Türkçe dipinto, her tekrarda solar.
'use strict';
// dağ sırtları: arkadan öne koyulaşan kayalık katmanlar (dünya koordinatı)
function s2_daglar(ctx, t, o = {}) {
  const L = o.katman || [[520, '#1B0D07', 61, 160], [640, '#2A140A', 62, 200], [780, '#3A1B0D', 63, 240]];
  for (const [y, col, sd, hh] of L) {
    const r = rng(sd), P = [[-600, 1300]];
    for (let x = -600; x <= 2600; x += 180) P.push([x, y - hh * (.3 + .7 * Math.abs(Math.sin(x * .0021 + sd))) - r() * 40]);
    P.push([2600, 1300]);
    crag(ctx, P, { fill: col, seed: sd, wob: 6, strata: 2, lobes: 1 });
  }
}
(() => {
  // P066 · ters açı · E14 · Eko'nun bakışı: iki kayanın arasından uzaktaki kıyı; kayanın yüzünde soluk kırmızı profil; küçük bir taş düşer
  plan('P066', (ctx, st) => {
    const t = st.t, tB = PE('P066', 0), tK = PE('P066', 1), tU = PE('P066', 2);
    s2_genis(ctx, t, { cam: s2_cam(st, [1060, 600, .8], [1160, 600, .8]), midTree: false, refA: .35, ground: c => s2_rafW(c),
      fig: (c, refl) => withFigT(t, () => s2_litFig(c, s2_proneW(c, t, { head: .2, neck: .2 }), null, { fade: 1 })) });
    baseT(ctx); const dx = lerp(30, -40, st.p);
    // ön plan kayaları (ekran): solda ve sağda, arada yarık
    ctx.save(); ctx.translate(dx, 0);
    crag(ctx, [[-200, -100], [560, -100], [600, 200], [540, 420], [620, 700], [560, 1200], [-200, 1200]], { fill: '#120805', seed: 71, wob: 10, strata: 4, lobes: 3 });
    crag(ctx, [[2200, -100], [1420, -100], [1380, 260], [1460, 520], [1360, 820], [1440, 1200], [2200, 1200]], { fill: '#120805', seed: 72, wob: 10, strata: 4, lobes: 3 });
    // kayanın yüzünde soluk kırmızı profil (Eko'nun yüzü kayada; beden yok)
    const pr = ramp(t, tK - .1, tK + 1.4, E.io2);
    if (pr > 0) { ctx.save(); ctx.strokeStyle = `rgba(200,70,45,${(.55 * pr).toFixed(3)})`; ctx.lineWidth = 4; ctx.lineCap = 'round'; const P = [[592, 250], [600, 300], [632, 342], [604, 356], [618, 384], [606, 396], [612, 420], [592, 450], [576, 500]];
      ctx.beginPath(); P.slice(0, Math.max(2, Math.ceil(P.length * pr))).forEach((q, i) => i ? ctx.lineTo(...q) : ctx.moveTo(...q)); ctx.stroke(); ctx.restore(); }
    // kayadan küçük bir taş düşer
    const u = clamp((t - tU) / .9); if (u > 0 && u < 1) { ctx.save(); ctx.translate(1400 + 30 * u, 300 + 760 * u * u); ctx.rotate(u * 5); ctx.fillStyle = '#5A2C16'; ctx.strokeStyle = C.ink; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(-14, -6); ctx.lineTo(4, -14); ctx.lineTo(16, 2); ctx.lineTo(2, 12); ctx.lineTo(-12, 8); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore(); }
    ctx.restore();
    meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
  });

  // P069 · geniş · E15@eko · Dağlar: ELVEDA yankısı yamaçtan yamaca, her tekrarda solarak (ELVEDA · elveda · eda)
  plan('P069', (ctx, st) => {
    const t = st.t, tE = PE('P069', 0);
    baseT(ctx); glaze(ctx, 960, 900, 1300, 'rgba(110,44,20,.4)');
    camAt(ctx, ...s2_cam(st, [860, 540, 1.0], [1100, 540, 1.04]));
    s2_daglar(ctx, t);
    for (const [k, s, x, y, h, a] of [[0, 'ELVEDA', 640, 330, 64, .9], [1, 'ELVEDA', 1180, 420, 44, .55], [2, 'EDA', 1560, 300, 30, .3]]) {
      const t0 = tE + k * .55, al = ramp(t, t0, t0 + .3) * (1 - ramp(t, t0 + 1.4, t0 + 2.2)); if (al <= 0) continue;
      txtDipinto(ctx, s, x, y - 20 * ramp(t, t0, t0 + 2), h, ramp(t, t0, t0 + .5, E.lin), { col: '#E0573A', a: a * al });
    }
    baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
  });

  // P091 · orta · F09@onu · Eko'nun kayası yakından (karanlık, kayaya karışmış siluet); AH yankıları kayadan kıyıya doğru akar
  plan('P091', (ctx, st) => {
    const t = st.t, tS = PE('P091', 0), tA = PE('P091', 1);
    baseT(ctx); glaze(ctx, 1300, 900, 1200, 'rgba(110,44,20,.42)');
    camAt(ctx, ...camMix([700, 560, 1.15], [1150, 560, 1.15], ramp(t, st.at, st.end, E.sine)));
    groundBand(ctx, 780, -400, 2600);
    crag(ctx, [[200, 790], [240, 520], [360, 330], [520, 260], [700, 300], [800, 470], [840, 790]], { fill: '#24110A', seed: 91, wob: 7, strata: 4, lobes: 2 });
    s2_eko(ctx, 560, 784, 4.0, t, .38);
    // uzakta kıyı: havuz ve uzanan genç (küçük)
    ctx.save(); ctx.beginPath(); ctx.ellipse(1720, 800, 260, 26, 0, 0, TAU); ctx.fillStyle = '#050302'; ctx.fill(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 3; ctx.stroke(); ctx.restore();
    crag(ctx, [[1240, 790], [1300, 762], [1480, 758], [1520, 790]], { fill: '#5A2C16', seed: 92, wob: 3, strata: 1, lobes: 1 });
    withFigT(t, () => figure(ctx, proneFig(1478 - 30 * 2.2, 762, 2.2, { ...pPose({ head: .05 }), hemPerp: true, hemT: .62 }, { hN: [1478, 762], hF: [1474, 762], flatFeet: -2.9, idle: .3 })));
    for (let i = 0; i < 4; i++) grass(ctx, 900 + i * 120, 782, 1.6, t, 120 + i);
    // yankılar: kayadan kıyıya
    for (let k = 0; k < 4; k++) { const t0 = (k === 0 ? tS : tA) + k * .4, u = ramp(t, t0, t0 + 2.6, E.io2), al = ramp(t, t0, t0 + .3) * (1 - ramp(t, t0 + 2.2, t0 + 2.9)); if (al <= 0) continue;
      txtDipinto(ctx, 'AH', lerp(720, 1460, u), 420 + k * 34 + Math.sin(u * 6 + k) * 16, 46 - k * 6, ramp(t, t0, t0 + .3, E.lin), { col: '#E0573A', a: (.75 - k * .12) * al }); }
    baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
  });
})();
