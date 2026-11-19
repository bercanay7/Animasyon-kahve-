// DERE seti, SAHİP-2: P086. Bu dosyayı yalnız bu sahip değiştirir.
// Köy kenarında sığ, çakıllı dere (saz yok, bir iki söğüt); arkada köye giden patika (P054'teki patikanın biçiminde). Mitte yok: temsilî görsel.
// Çocuk: 7–8 yaş oranı (baş büyük, boy gencin yarısı), kısa düz saç, alında bant yok, kemerli kısa tunik, elinde çember (trokhos). Arkadaşları baştan sona patikada.
'use strict';
(() => {
  // tur 2: kel manken okunuyordu: siyah sır kısa saç (rf + HAIR_MOD; modern: alında kırmızı bant çizilmez), kemerli kısa tunik (koyu kil), büyük baş
  const LK_COC = { hair: 'short', rf: true, modern: true, hairPts: HAIR_MOD, noCurls: true, garment: 'short', headS: 1.5, jaw: false, khiton: { col: '#7E3920', edge: 1.2, sleeve: false } };
  const cocuk = (c, x, gy, s, t, p, dir = 1, o = {}) => figure(c, { x, y: gy - 43 * s * (o.bend ? .97 : 1), s, dir, sty: STY.red, lk: LK_COC, seed: o.seed ?? 86, idle: .6, stripe: .5, p });
  const cember = (c, x, y, r, a = 0) => { c.save(); c.strokeStyle = C.ink; c.lineWidth = 6; c.beginPath(); c.arc(x, y, r, 0, TAU); c.stroke(); c.strokeStyle = PC.clayR; c.lineWidth = 2.5; c.stroke();
    c.strokeStyle = C.ink; c.lineWidth = 3; c.beginPath(); c.moveTo(x - r * .2, y - r * .9); c.lineTo(x - r * 1.3 * Math.cos(a), y - r * 1.8); c.stroke(); c.restore(); };
  // P086 · orta · F06 · Adsız çocuk dereye eğilir, yansımasına güler, çemberini alır ve patikadaki arkadaşlarına koşar; kıyıda yalnız dalgalanan su
  plan('P086', (ctx, st) => {
    const t = st.t, tB = PE('P086', 0), tK = PE('P086', 1), tH = PE('P086', 2), tO = PE('P086', 3);
    const gy = 640, wy = 700, s = 3.0;
    const bend = ramp(t, tB - .4, tB + .6, E.io2) * (1 - ramp(t, tH - .3, tH + .2, E.io2)), laugh = ramp(t, tK - .1, tK + .3, E.out2);
    const run = clamp((t - tH - .1) / (tO - tH + .4)), xr = lerp(980, 260, E.in2(run) * .5 + run * .5);
    baseT(ctx); glaze(ctx, 1000, 760, 1200, 'rgba(140,64,30,.45)');
    // tur 2: 'bakar, güler' yakında (kamera çocuğa ve yansımasına yaklaşır), 'gider'de geri çekilir: eylem büyür
    const near = ramp(t, tB - .6, tB + .8, E.io2);
    camAt(ctx, ...camMix(camMix([1060, 560, 1.05], [1010, 640, 1.75], near), [620, 520, 1.05], ramp(t, tH - .1, tO + .3, E.io2)));
    groundBand(ctx, gy, -800, 2600);
    // patika (köye), tur 2: kıyı şeridinde soldan çocuğun yerine kadar uzanan açık toprak yol (ince çizgi anlaşılmıyordu); kenarları kesik çizgi, üstünde çakıl
    ctx.save(); const pg = ctx.createLinearGradient(-300, 0, 1050, 0); pg.addColorStop(0, '#C47A4A'); pg.addColorStop(.85, '#B9653A'); pg.addColorStop(1, 'rgba(185,101,58,0)');
    ctx.fillStyle = pg; ctx.beginPath(); ctx.moveTo(-300, gy + 4); ctx.lineTo(1050, gy + 10); ctx.lineTo(1050, gy + 52); ctx.lineTo(-300, gy + 56); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = 'rgba(14,9,7,.45)'; ctx.lineWidth = 2; ctx.setLineDash([18, 12]); for (const y of [gy + 8, gy + 52]) { ctx.beginPath(); ctx.moveTo(-300, y); ctx.lineTo(980, y + 2); ctx.stroke(); } ctx.setLineDash([]);
    const pr = rng(861); ctx.fillStyle = 'rgba(90,44,22,.6)'; for (let i = 0; i < 26; i++) { ctx.beginPath(); ctx.ellipse(-260 + pr() * 1250, gy + 16 + pr() * 30, 4 + pr() * 5, 2 + pr() * 2, 0, 0, TAU); ctx.fill(); }
    ctx.restore();
    // söğütler ve uzakta köy
    for (const [x, sc, sd] of [[1480, 1.7, 21], [1800, 1.4, 22], [-120, 1.5, 23]]) vaseTree(ctx, x, gy, sc, sd, t, { branches: 7, reach: 120 });
    city(ctx, -260, gy - 4, .7, '#3A1B0D', PC.clayR, 4);
    // dere: sığ, çakıllı (ön planda)
    ctx.save(); ctx.beginPath(); ctx.rect(-800, wy, 3600, 400); ctx.fillStyle = '#0A0605'; ctx.fill(); ctx.clip();
    const rr = rng(86); for (let i = 0; i < 60; i++) { ctx.fillStyle = `rgba(185,101,58,${(.25 + rr() * .3).toFixed(2)})`; ctx.beginPath(); ctx.ellipse(-400 + rr() * 2800, wy + 30 + rr() * 300, 10 + rr() * 16, 5 + rr() * 6, 0, 0, TAU); ctx.fill(); }
    ctx.restore();
    // çocuğun yansıması (eğilince görünür), kalkınca su dalgalanır
    mirror(ctx, c => { if (run <= 0) cocuk(c, 1000, wy, s, t, { torso: .7 * bend, neck: .4 * bend, head: .3 * bend, hipN: .05, hipF: -.05, shN: -.6 * bend, elN: .3, shF: -.4 * bend, elF: .3, smile: .7 * laugh, mouthOpen: .8 * laugh * (.6 + .4 * Math.sin(t * 14)) }); },
      wy, c => c.rect(-800, wy, 3600, 400), t, { a: .5, calm: 1 + 6 * ramp(t, tH, tH + .5) * (1 - ramp(t, tO, tO + 1.5)) });
    ctx.strokeStyle = 'rgba(232,160,104,.9)'; ctx.lineWidth = 3.4; ctx.beginPath(); ctx.moveTo(-800, wy); ctx.lineTo(2800, wy); ctx.stroke();
    // kıyı şeridi (dere ile zemin arası)
    ctx.fillStyle = '#5A2C16'; ctx.fillRect(-800, gy + 60, 3600, wy - gy - 60);
    // arkadaşlar patikada (baştan sona kadrajda)
    for (const [x, sd, d] of [[180, 87, 1], [300, 88, -1]]) cocuk(ctx, x, gy + 20, s * .92, t, { torso: .02, hipN: .05, hipF: -.05, shN: d > 0 ? -.4 : .2, elN: .5, shF: .1, elF: .4, smile: .4, head: .05 * Math.sin(t * 2 + sd) }, d, { seed: sd });
    // çocuk: eğilir, güler, çemberi alır, koşar
    if (run <= 0) { cocuk(ctx, 1000, wy - 2, s, t, { torso: .7 * bend, neck: .4 * bend, head: .3 * bend, hipN: .05, hipF: -.05, shN: -.6 * bend, elN: .3, shF: -.4 * bend, elF: .3, smile: .7 * laugh, mouthOpen: .8 * laugh * (.6 + .4 * Math.sin(t * 14)) });
      cember(ctx, 1110, wy - 50, 46, 0); }
    else { let J = null, M = null; walkScene(ctx, null, xr, s, t, -1, { ground: groundOf(x => lerp(wy - 2, gy + 20, clamp((1000 - x) / 700))), noCam: true, sty: STY.red, lk: LK_COC, dist: (1000 - xr) * 1.2, stride: 40, lean: .16, stripe: .5,
        onJoints: (j, m) => { J = j; M = m; }, p: { smile: .5 } });
      const hx = xr - 60; cember(ctx, hx - 20, lerp(wy, gy + 20, clamp((1000 - hx) / 700)) - 48, 46, t * 3); }
  });
})();
