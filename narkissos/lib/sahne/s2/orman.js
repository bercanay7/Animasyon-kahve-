// ORMAN seti, SAHİP-2: P057 (hatıra). Bu dosyayı yalnız bu sahip değiştirir.
// Hatıra dili: beyaz zemin lekythos paleti, solgun sepya çizgi (sessizde de 'geçmiş' okunur). C07'nin (P026, SAHİP-1) kompozisyonu: orman, iten el.
// SAHİP-1'in P026 çizimi henüz yokken kendi yeniden çizimimiz (ortak değişiklik önerisi: P026 kurucusu ortak yapılırsa buradan çağrılır).
'use strict';
(() => {
  const LK_EKO = { fem: true, hair: 'long', garment: 'robe', himation: true };
  // P057 · geniş · E08 · Hatıra: Narkissos Eko'yu eliyle iter; ağzından ANCAK BEN ÖLÜNCE BANA SAHİP OLURSUN ('SAHİP' P056'daki yerinde); yazı pınara doğru uçar
  plan('P057', (ctx, st) => {
    const t = st.t, tA = PE('P057', 0), tO = PE('P057', 1);
    baseT(ctx); whiteGround(ctx, { x: 960, y: 500 });
    camAt(ctx, ...s2_cam(st, [960, 560, 1.0], [1010, 560, 1.0]));
    const gy = 860;
    ctx.save(); ctx.globalAlpha = .55;
    for (const [x, s, sd] of [[120, 2.2, 3], [420, 1.8, 6], [1640, 2.3, 8], [1880, 1.9, 5]]) vaseTree(ctx, x, gy, s, sd, t, { branches: 7, reach: 110, fill: '#D9C7A6', ink: C.sepia });
    ctx.strokeStyle = C.sepia; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-400, gy); ctx.lineTo(2400, gy); ctx.stroke();
    ctx.restore();
    const push = ramp(t, st.at - .3, st.at + .4, E.out2);
    // Eko (yüzü açık; uzun giysi ve himation; baştan ayağa örtülü değil): kollarını açmış, itilince geri çekilir
    figure(ctx, { x: 760 - 30 * push, y: gy - 43 * 4.2, s: 4.2, dir: 1, sty: STY.white, lk: LK_EKO, seed: 57, idle: .5, alpha: .55,
      p: { torso: lerp(.14, -.04, push), neck: .1, head: .05, hipN: .12, knN: .05, hipF: -.12, knF: .04, shN: lerp(-1.1, -.5, push), elN: .4, shF: lerp(-.9, -.3, push), elF: .5, handN: 'open', handF: 'open', smile: -.2 } });
    // Narkissos geri çekilir, eliyle iter
    figure(ctx, { x: 1180, y: gy - 43 * 4.2, s: 4.2, dir: -1, sty: STY.white, lk: { ...LK_NK, khiton: null }, seed: 58, idle: .5, alpha: .6,
      p: { torso: -.08, neck: -.05, head: -.05, hipN: -.18, knN: .06, hipF: .22, knF: .1, shN: -1.25 * push, elN: .15, shF: .2, elF: .6, handN: 'open', handF: 'flat', mouthOpen: tO > t && t > tA - .1 ? .6 : 0 } });
    // dipinto: ağzından; 'SAHİP' P056'daki ekran yerinde (S2_SAHIP), olursun'da pınara (sağa) uçar
    const fly = ramp(t, tO + .1, tO + 1.2, E.in2), wr = ramp(t, tA - .05, tO + .1, E.lin);
    ctx.save(); baseT(ctx); ctx.font = FONT.baslik(46, 600); ctx.letterSpacing = '6px';
    const L = 'ANCAK BEN ÖLÜNCE BANA ', wL = ctx.measureText(L).width + 6 * 0, wS = ctx.measureText('SAHİP').width;
    const x0 = S2_SAHIP[0] - wL - wS / 2 + 1500 * fly, y0 = S2_SAHIP[1] - 120 * fly;
    ctx.restore();
    ctx.save(); baseT(ctx); ctx.globalAlpha = 1 - fly; txtDipinto(ctx, 'ANCAK BEN ÖLÜNCE BANA SAHİP OLURSUN', x0, y0, 46, wr, { col: '#9A3B25', align: 'left', ls: 6 }); ctx.restore();
  }, { post: { tex: .25, vig: .5 } });
})();
