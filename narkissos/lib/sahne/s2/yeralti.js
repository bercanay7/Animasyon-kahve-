// YERALTI seti, SAHİP-2: P071. Bu dosyayı yalnız bu sahip değiştirir.
// Styks: figürsüz ve simgesel (kayıkçı, kafatası, iblis yok): karanlık su, yatay dalga çizgileri, suyun yüzünde soluk bir yüz parıltısı.
'use strict';
(() => {
  // P071 · geniş · E16@ölüler · Styks: karanlık su; etiket; soluk oval parıltı (yüz) kaybolmaz, yerinde titrer
  plan('P071', (ctx, st) => {
    const t = st.t, tS = PE('P071', 0), tK = PE('P071', 1), tE = PE('P071', 2);
    baseT(ctx); ctx.fillStyle = '#0C0608'; ctx.fillRect(0, 0, W, H);
    { const g = ctx.createLinearGradient(0, 300, 0, 560); g.addColorStop(0, 'rgba(70,40,52,0)'); g.addColorStop(1, 'rgba(96,56,64,.55)'); ctx.fillStyle = g; ctx.fillRect(0, 300, W, 260); } // tur 2: karşı kıyının ardında soluk ışık (siyah ekran okunuyordu)
    camAt(ctx, ...s2_cam(st, [860, 540, 1.0], [1160, 540, 1.05]));
    // uzak karşı kıyı: alçak, kapkara şerit
    ctx.fillStyle = '#1A0E10'; ctx.beginPath(); ctx.moveTo(-600, 470); for (let x = -600; x <= 2600; x += 60) ctx.lineTo(x, 470 - 22 * (.5 + .5 * noise1(x * .004, 7))); ctx.lineTo(2600, 470); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = 'rgba(201,112,63,.75)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-600, 471); ctx.lineTo(2600, 471); ctx.stroke(); // kıyı çizgisi
    // yatay dalga çizgileri (kil, çok soluk), yavaş kayar
    const kp = ramp(t, tS - .5, tS + .8);
    ctx.lineCap = 'round';
    for (let i = 0; i < 26; i++) { const y = 480 + i * 22 + i * i * .9, ph = t * (.6 + (i % 3) * .15) + i * 1.7, a = (.18 + .26 * (i / 26)) * (.6 + .4 * kp);
      ctx.strokeStyle = `rgba(201,112,63,${a.toFixed(3)})`; ctx.lineWidth = 1.4 + i * .08; ctx.beginPath();
      for (let x = -600; x <= 2600; x += 24) { const yy = y + Math.sin(x * .012 + ph) * (3 + i * .3); x === -600 ? ctx.moveTo(x, yy) : ctx.lineTo(x, yy); } ctx.stroke(); }
    // soluk oval parıltı: kendine bakan yüzün izi (figür yok)
    const g0 = ramp(t, tK - .1, tK + 1.2, E.io2), tr = ramp(t, tE - .2, tE + .4), wob = 1 + .04 * Math.sin(t * 9) * tr + .02 * Math.sin(t * 2.3);
    if (g0 > 0) { ctx.save(); ctx.translate(980, 720); ctx.scale(wob, 1 / wob);
      const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 120); g.addColorStop(0, `rgba(236,222,196,${(.6 * g0).toFixed(3)})`); g.addColorStop(.6, `rgba(236,222,196,${(.26 * g0).toFixed(3)})`); g.addColorStop(1, 'rgba(236,222,196,0)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(0, 0, 130, 54, 0, 0, TAU); ctx.fill();
      ctx.strokeStyle = `rgba(236,222,196,${(.55 * g0).toFixed(3)})`; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.ellipse(0, 0, 118, 48, 0, 0, TAU); ctx.stroke(); ctx.restore(); } // ovalin kenarı belirgin
    baseT(ctx); meander(ctx, -400, 2400, 0, 36, '#5A2C16', PC.glaze);
  }, { post: { vig: 1 }, over: (ctx, st) => etiket(ctx, 'STYKS', W / 2, 220, st.t - PE('P071', 0), 3.5) });
})();
