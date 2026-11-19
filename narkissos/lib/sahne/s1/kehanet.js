// KEHANET seti, SAHİP-1: P009, P010. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Yardımcılar S1 (s1/cam.js, s1/nehir.js: anneBebek). Kehanet sahnesinde ilahi ışık/hale YOK; kâhin profil, gözleri kapalı.
'use strict';
(() => {
  const S1 = window.S1;
  // Tiresias: yaşlı kâhin, asalı, gözleri kapalı (p.blink 1). up: baş kaldırma (0..1), konus: ağız aralığı
  S1.tiresias = (ctx, t, o) => {
    const { x, gy, s } = o, up = o.up || 0;
    let J = null, M = null;
    const f = { x, y: gy - 44.5 * s, s, dir: o.dir ?? 1, sty: STY.red, lk: S1.LK_TIR, seed: 61, stripe: .45, idle: .5,
      p: { torso: .08, neck: .22 - .3 * up, head: .18 - .32 * up, blink: 1, shN: .35, elN: .9, handN: 'open', handF: 'fist', brow: .3 },
      ik: { hF: [x + (o.dir ?? 1) * 11 * s, gy - 26 * s] }, onJoints: (j, m) => { J = j; M = m; } };
    figure(ctx, f);
    // asa: uzak elden yere
    if (J) { const w = jointPt(ctx, M, J.AF.wr); ctx.save(); ctx.lineCap = 'round'; ctx.strokeStyle = C.ink; ctx.lineWidth = 2.6 * s / 5; ctx.beginPath(); ctx.moveTo(w[0] + (o.dir ?? 1) * 1 * s, w[1] - 12 * s); ctx.lineTo(w[0] + (o.dir ?? 1) * 3 * s, gy); ctx.stroke();
      ctx.strokeStyle = PC.clayR; ctx.lineWidth = 1.1 * s / 5; ctx.stroke(); ctx.restore(); }
    return f;
  };
  // kayalık yamaç + tek zeytin ağacı
  const yamac = (ctx, t, gy) => {
    glaze(ctx, 900, 900, 1300, 'rgba(118,48,22,.42)');
    crag(ctx, [[-600, gy + 10], [-300, gy - 260], [80, gy - 330], [360, gy - 200], [560, gy - 40], [620, gy + 10]], { fill: '#4E2615', seed: 7, wob: 10, strata: 4, lobes: 3 });
    groundBand(ctx, gy, -3000, 6000, { h: 1400 });
    vaseTree(ctx, 200, gy, 2.1, 17, t, { branches: 7, reach: 120 });
    for (let i = 0; i < 10; i++) grass(ctx, -200 + i * 260 + (i % 2) * 70, gy + 2, 1.6, t, i + 31);
  };

  // ---- P009 · orta · B01@annesi: kayalık yamaçta kör kâhin Tiresias; anne bebekle karşısında. 'kör'de başını kaldırır (gözler kapalı), 'oğlum'da anne bebeği uzatır ----
  plan('P009', (ctx, st) => {
    const t = st.t, tK = PE('P009', 0), tO = PE('P009', 1), gy = 860, s = 8.4;
    baseT(ctx); camAt(ctx, lerp(1080, 930, E.sine(st.p)), 560, 1.0);
    yamac(ctx, t, gy);
    const up = ramp(t, tK - .1, tK + .8, E.io2);
    S1.tiresias(ctx, t, { x: 720, gy, s, up });
    dipintoYaz(ctx, 'ΤΕΙΡΕΣΙΑΣ', 560, 400, 34, ramp(t, st.at + .3, st.at + 1.3, E.lin), { col: S1.KIL, w: .11, vertical: true });
    S1.anneBebek(ctx, t, { x: 1330, gy, s: s * .98, dir: -1, uz: ramp(t, tO - .1, tO + .9, E.io2) });
  }, { over: (ctx, st) => etiket(ctx, 'TİRESİAS', 470, 250, st.lt - 1.0, 99, { px: 42 }) });

  // ---- P010 · yakın · B02 · LEVHA: Tiresias'ın profili yakın; ağzından dipinto KENDİNİ TANIMAZSA akar; kamera yazıyla sağa kayar. 'tanımazsa'da annenin eli bebeği göğsüne çeker ----
  plan('P010', (ctx, st) => {
    const t = st.t, tK = PE('P010', 0), tT = PE('P010', 1);
    baseT(ctx);
    const fx = lerp(760, 1000, ramp(t, tK - .3, tT + .9, E.io2)) + 20 * E.sine(st.p);
    glaze(ctx, 700, 900, 1300, 'rgba(118,48,22,.45)');
    camAt(ctx, fx, 470, 1.0);
    crag(ctx, [[-900, 1150], [-500, 760], [200, 700], [500, 900], [700, 1150]], { fill: '#4E2615', seed: 8, wob: 10, strata: 3, lobes: 2 });
    // Fable tur 1: künye (sol alt, y ≈ 846) sakalın üstüne biniyordu → kâhin biraz küçük ve yukarıda; sakal y < 760'ta biter
    const s = 21, gy = 330 + 37 * s + 44.5 * s;
    const konus = Math.max(0, Math.sin((t - tK) * 9)) * ramp(t, tK - .1, tK, E.lin) * (1 - ramp(t, tT + .5, tT + .7, E.lin));
    const f = S1.tiresias(ctx, t, { x: 360, gy, s, up: .55 + .05 * Math.sin(t * .8) });
    const m = S1.basNok(ctx, f, S1.AGIZ);
    // ağızdan çıkan fırça yazısı (Türkçe dipinto), hafif dalgalı şerit
    const p = ramp(t, tK - .05, tT + .55, E.lin);
    const yol = S1.konusmaYolu(m[0] + 40, m[1] + 10, -.04, 1500, t, { amp: 10, k: .012 });
    S1.yolYazi(ctx, 'KENDİNİ TANIMAZSA', yol, p, { px: 70, col: S1.KIL, rise: 10 });
    // kenarda annenin eli bebeği göğsüne çeker ('tanımazsa'): kundak sağ kenardan dışarı çekilir
    const ce = ramp(t, tT + .1, tT + 1.0, E.io2);
    const bx = lerp(1880, 2180, ce), by = 640;
    S1.bebek(ctx, bx, by, 9, -.1, -1);
    ctx.save(); ctx.translate(bx + 70, by + 50); ctx.rotate(-.3); ctx.beginPath(); ctx.ellipse(0, 0, 70, 22, 0, 0, TAU); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke(); ctx.restore();
  }, { over: (ctx, st) => kunye(ctx, 'Ovidius, Dönüşümler III 348 · si se non noverit', st.lt - 2.2, 99) });
})();
