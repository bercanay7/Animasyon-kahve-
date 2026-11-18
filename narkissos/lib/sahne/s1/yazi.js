// YAZI seti, SAHİP-1: P006. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Yardımcılar S1 (s1/cam.js).
'use strict';
(() => {
  // ---- P006 · ayrıntı · A05 · LEVHA: dönen bir vazonun omzunda kırmızı figür yazı ΝΑΡΚΙΣΣΟΣ; 'kelimede' yazı ön yüze gelir, 'narsisizm'de harfler dönüp NARSİSİZM olur ----
  const GR = [...'ΝΑΡΚΙΣΣΟΣ'], TR = [...'NARSİSİZM'];
  const R = 1000, CX = 960, YT = 520, HT = 116, DA = .118;
  plan('P006', (ctx, st) => {
    const t = st.t, tK = PE('P006', 0), tN = PE('P006', 1);
    // dönüş açısı: plan başında yazı sağ yanda, 'kelimede' ön yüzde; sonra çok yavaş sürüklenir (donuk değil)
    const phi = lerp(1.05, 0, ramp(t, st.at, tK + .25, E.out3)) - .045 * (t - tK) * (t > tK ? 1 : 0);
    baseT(ctx);
    // arka: sıcak karanlık (atölye), vazonun iki yanı kenar ışığıyla
    ctx.fillStyle = '#1B0F0A'; ctx.fillRect(0, 0, W, H);
    glow(ctx, 960, 540, 1100, 'rgba(110,52,26,.45)');
    camAt(ctx, 960, 540, lerp(1.0, 1.04, E.sine(st.p)));
    // vazo gövdesi (omuz): geniş sır kütle, üstte boyun
    ctx.save();
    ctx.beginPath(); ctx.moveTo(-200, 1300); ctx.lineTo(-120, 330); ctx.quadraticCurveTo(200, 150, 700, 130); ctx.lineTo(700, -100); ctx.lineTo(1220, -100); ctx.lineTo(1220, 130); ctx.quadraticCurveTo(1720, 150, 2040, 330); ctx.lineTo(2120, 1300); ctx.closePath();
    const g = ctx.createLinearGradient(-120, 0, 2040, 0); g.addColorStop(0, '#050302'); g.addColorStop(.3, '#120B08'); g.addColorStop(.5, '#1A110C'); g.addColorStop(.7, '#120B08'); g.addColorStop(1, '#050302');
    ctx.fillStyle = g; ctx.fill(); ctx.clip();
    // kil bant (yazının zemini, ayrılmış) ve dil motifleri: silindir üstünde, dönüşle kayar
    const cyl = th => [CX + R * Math.sin(th), Math.cos(th)];
    ctx.fillStyle = PC.clayR; ctx.fillRect(-300, 300, 2600, 6); ctx.fillRect(-300, 744, 2600, 6);
    for (let k = -40; k <= 40; k++) { const th = k * .055 + phi * 1.0 + (t * .01); const [x, c] = cyl(th); if (c < .05) continue;
      ctx.save(); ctx.translate(x, 268); ctx.scale(c, 1); ctx.beginPath(); ctx.ellipse(0, 0, 21, 26, 0, PI, TAU); ctx.lineTo(21, 22); ctx.lineTo(-21, 22); ctx.closePath(); ctx.fillStyle = k % 2 ? C.red : PC.clayR; ctx.globalAlpha = .4 + .6 * c; ctx.fill(); ctx.restore(); }
    for (let k = -30; k <= 30; k++) { const th = k * .09 + phi; const [x, c] = cyl(th); if (c < .05) continue;
      ctx.save(); ctx.translate(x, 790); ctx.scale(c, 1); ctx.globalAlpha = .35 + .65 * c; ctx.strokeStyle = PC.clayR; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(-34, 0); ctx.lineTo(34, 0); ctx.moveTo(-34, 0); ctx.lineTo(-34, 30); ctx.lineTo(20, 30); ctx.lineTo(20, 12); ctx.lineTo(-8, 12); ctx.stroke(); ctx.restore(); }
    // yazı: harf harf silindir üstünde; 'narsisizm'de her harf dikey ekseninde döner ve yeni harfe geçer (sırayla)
    for (let i = 0; i < 9; i++) {
      const th = (i - 4) * DA + phi, [x, c] = cyl(th); if (c < .04) continue;
      const u = ramp(t, tN + i * .085, tN + i * .085 + .42, E.io2), flip = Math.abs(Math.cos(u * PI)), lat = u > .5;
      ctx.save(); ctx.translate(x, YT + (lat ? 0 : 0) - 10 * Math.sin(u * PI)); ctx.scale(c * Math.max(.04, flip), 1); ctx.globalAlpha = .3 + .7 * c;
      if (!lat) dipinto(ctx, GR[i], 0, 0, HT, { col: PC.clayRL, w: .12, seed: 3 + i });
      else { ctx.font = FONT.baslik(HT * 1.12, 700); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = PC.clayRL; ctx.fillText(TR[i], 0, 6); }
      ctx.restore();
    }
    // dönen yüzeyin parlaması (ışık sabit, vazo döner: yansıyan şerit yerinde, dokular kayar)
    const sg = ctx.createLinearGradient(1150, 0, 1420, 0); sg.addColorStop(0, 'rgba(255,220,180,0)'); sg.addColorStop(.5, 'rgba(255,220,180,.07)'); sg.addColorStop(1, 'rgba(255,220,180,0)');
    ctx.fillStyle = sg; ctx.fillRect(1150, 0, 270, 1300);
    ctx.restore();
    // omuz çizgisi
    ctx.save(); ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-120, 330); ctx.quadraticCurveTo(200, 150, 700, 130); ctx.moveTo(1220, 130); ctx.quadraticCurveTo(1720, 150, 2040, 330); ctx.stroke(); ctx.restore();
  }, { post: { tex: .45 } });
})();
