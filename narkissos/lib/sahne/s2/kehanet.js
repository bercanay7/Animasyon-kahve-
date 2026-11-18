// KEHANET seti, SAHİP-2: P060 (hatıra). Bu dosyayı yalnız bu sahip değiştirir.
// Hatıra dili: beyaz zemin, solgun sepya (P057 ile aynı). B02'nin (P010, SAHİP-1) kompozisyonu: kör kâhin Tiresias'ın profili, ağzından Türkçe dipinto.
'use strict';
(() => {
  // P060 · yakın · E10 · Hatıra: Tiresias'ın profili (sakallı, gözleri kapalı, asalı); KENDİNİ TANIMAZSA yeniden belirir
  plan('P060', (ctx, st) => {
    const t = st.t, tK = PE('P060', 0);
    baseT(ctx); whiteGround(ctx, { x: 900, y: 420 });
    camAt(ctx, ...s2_cam(st, [920, 470, 1.18], [940, 480, 1.08]));
    ctx.save(); ctx.strokeStyle = C.sepia; ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.globalAlpha = .7; ctx.beginPath(); ctx.moveTo(470, 120); ctx.lineTo(500, 1200); ctx.stroke(); ctx.restore(); // asa
    figure(ctx, { x: 640, y: 960, s: 13, dir: 1, sty: STY.white, lk: { beard: 'long', hair: 'long', garment: 'robe', himation: true }, seed: 60, idle: .5, alpha: .85,
      p: { torso: .06, neck: .18, head: .12, shN: -.4, elN: .6, shF: .2, elF: .8, handN: 'fist', handF: 'flat', blink: 1, mouthOpen: t > tK - .1 && t < tK + 1.6 ? .5 + .4 * Math.sin((t - tK) * 9) : 0 } });
    txtDipinto(ctx, 'KENDİNİ TANIMAZSA', 900, 410, 60, ramp(t, tK - .05, tK + 1.6, E.lin), { col: '#9A3B25', align: 'left', ls: 7 });
  }, { post: { tex: .25, vig: .5 } });
})();
