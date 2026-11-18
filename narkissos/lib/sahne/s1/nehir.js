// NEHIR seti, SAHİP-1: P008. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Yardımcılar S1 (s1/cam.js).
'use strict';
(() => {
  const S1 = window.S1;
  // kundaktaki bebek (profil; kil kundak, küçük baş): (x, y) kundağın ortası, s ölçek, a eğim, dir yüz yönü
  S1.bebek = (ctx, x, y, s, a = 0, dir = 1) => {
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s * dir, s); ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.ellipse(-2, 0, 10, 4.6, 0, 0, TAU); ctx.fillStyle = '#B4683B'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = .6; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-8, -2.5); ctx.quadraticCurveTo(-3, 1, 3, -3.4); ctx.moveTo(-10, 1.5); ctx.quadraticCurveTo(-4, 4, 2, 1); ctx.lineWidth = .35; ctx.stroke();
    ctx.beginPath(); ctx.arc(9.2, -1.4, 3.4, 0, TAU); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.lineWidth = .5; ctx.stroke();
    ctx.beginPath(); ctx.arc(8.6, -2.2, 3.5, PI * .95, PI * 1.75); ctx.lineWidth = 1.6; ctx.strokeStyle = C.ink; ctx.stroke();
    ctx.beginPath(); ctx.arc(10.6, -1.9, .42, 0, TAU); ctx.fillStyle = C.ink; ctx.fill();
    ctx.restore();
  };
  // sarmaşık dalı (kalp biçimli yapraklar): a noktasından ang yönünde
  S1.sarmasik = (ctx, x, y, s, ang, t) => {
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang + Math.sin(t * 2) * .05); ctx.scale(s, s); ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.bezierCurveTo(10, -6, 20, 6, 32, 0); ctx.strokeStyle = C.ink; ctx.lineWidth = 2.6; ctx.stroke(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 1.2; ctx.stroke();
    for (const [u, sd] of [[.3, -1], [.55, 1], [.8, -1], [1, 1]]) { ctx.save(); ctx.translate(32 * u, (u < .9 ? 2 : 0) * sd); ctx.rotate(sd * .9);
      ctx.beginPath(); ctx.moveTo(0, 0); ctx.bezierCurveTo(-5, -4, -3, -9, 0, -7); ctx.bezierCurveTo(3, -9, 5, -4, 0, 0); ctx.fillStyle = C.red; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = .8; ctx.stroke(); ctx.restore(); }
    ctx.restore();
  };
  // bebeği kucağında tutan figür: kundağı göğsün önünde tutar; uz (0..1) bebeği öne uzatma
  S1.anneBebek = (ctx, t, o) => {
    const { x, gy, s, dir } = o, uz = o.uz || 0;
    const f0 = { x, y: gy - 44.5 * s, s, dir, sty: S1.RFF, lk: o.lk || S1.LK_ANNE, seed: o.seed ?? 12, stripe: .45, idle: .7, p: { neck: (o.neck || 0) + .12, head: (o.head || 0) + .18 } };
    const { J, M } = joints(ctx, f0), sh = jointPt(ctx, M, J.shoulder);
    const bx = sh[0] + dir * s * lerp(7, 20, uz), by = sh[1] + s * lerp(12, 5, uz);
    const f = { ...f0, ik: { hN: [bx + dir * s * 2.5, by + s * 3.2], hF: [bx - dir * s * 4, by + s * 3.6] } };
    figure(ctx, f);
    S1.bebek(ctx, bx, by, s * .95, dir * (-.15 + .1 * uz), dir);
    return { f, b: [bx, by] };
  };
  // nehir kıyısı (yan görünüş): kıyı gy, önde akan su, sazlar
  S1.nehir = (ctx, t, gy) => {
    glaze(ctx, 960, 900, 1300, 'rgba(110,46,22,.42)');
    groundBand(ctx, gy, -3000, 6000, { h: 60 });
    const water = c => c.rect(-3000, gy + 60, 9000, 2000);
    waterBody(ctx, water, gy + 60, t * 2.2, { a: .3, seed: 14, n: 60, depth: 300, span: [-600, 2600] });
    shoreLine(ctx, -3000, gy + 60, { x1: 6000, w: 3 });
    // sazlar: öbek öbek uzun, kıvrık yapraklar ve püsküller (kıyının iki ucunda)
    for (let i = 0; i < 16; i++) { const xx = -300 + i * 170 + (i % 3) * 23; if (xx > 420 && xx < 1480) continue;
      for (let k = 0; k < 6; k++) { const h = 120 + hash(i * 3.7 + k) * 110, sw = Math.sin(t * 1.2 + i + k * .4) * 6, lean = (k - 2.5) * 9;
        ctx.save(); ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(xx + k * 5, gy + 50); ctx.quadraticCurveTo(xx + k * 5 + lean * .3, gy - h * .5, xx + k * 5 + lean + sw, gy - h + 10);
        ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.stroke(); ctx.strokeStyle = k % 2 ? PC.clayR : '#A85A30'; ctx.lineWidth = 3; ctx.stroke();
        if (k % 2 === 0) { ctx.beginPath(); ctx.ellipse(xx + k * 5 + lean + sw, gy - h - 4, 5, 15, lean * .01, 0, TAU); ctx.fillStyle = '#2A130A'; ctx.fill(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 1.2; ctx.stroke(); }
        ctx.restore(); } }
  };

  // ---- P008 · geniş · B01: nehir kıyısı, vazo frizi gibi: anne bebeği kucağında; periler bebeğe bakar. 'perilerin'de başlarını eğerler, 'güzeldir'de biri sarmaşık dalı uzatır ----
  plan('P008', (ctx, st) => {
    const t = st.t, tP = PE('P008', 0), tG = PE('P008', 1), gy = 740, s = 5.4;
    baseT(ctx); camAt(ctx, lerp(900, 1040, E.sine(st.p)), 560, 1.0);
    S1.nehir(ctx, t, gy);
    const bow = ramp(t, tP - .1, tP + .7, E.io2);
    // periler: iki solda (sağa bakar), biri arkada sağda
    S1.ayakta(ctx, { x: 1420, gy, s: s * .96, dir: -1, sty: S1.RFF, lk: S1.LK_PERI, seed: 41, p: { neck: .18 * bow, head: .15 * bow, shN: .2, elN: .4, shF: -.2, elF: .3, handN: 'open', handF: 'open' } });
    S1.ayakta(ctx, { x: 640, gy, s, dir: 1, sty: S1.RFF, lk: { ...S1.LK_PERI, robeCol: '#A75A31' }, seed: 43, p: { neck: .2 * bow, head: .16 * bow, shN: .25, elN: .5, shF: .1, elF: .4, handN: 'open', handF: 'open' } });
    // sarmaşık uzatan peri ('güzeldir')
    const uz = ramp(t, tG - .15, tG + .6, E.out3);
    let J = null, M = null;
    const fP = { x: 820, y: gy - 44.5 * s, s, dir: 1, sty: S1.RFF, lk: { ...S1.LK_PERI, robeCol: '#8F4626' }, seed: 44, stripe: .45, idle: .7, p: { neck: .2 * bow, head: .18 * bow, shF: .1, elF: .5, handN: 'open', handF: 'open' },
      ik: { hN: [lerp(870, 905, uz), lerp(gy - 22 * s, gy - 30 * s, uz)] }, onJoints: (j, m) => { J = j; M = m; } };
    figure(ctx, fP);
    if (J) { const w = jointPt(ctx, M, J.AN.wr); S1.sarmasik(ctx, w[0] + 4, w[1] + 2, 2.2 * s / 5.4, lerp(.6, -.25, uz), t); }
    // anne (sola bakar), bebek kucağında
    S1.anneBebek(ctx, t, { x: 1120, gy, s: s * 1.04, dir: -1, neck: .06 * bow, head: .05 * bow });
    S1.ustBant(ctx);
  }, { over: (ctx, st) => S1.bolumKarti(ctx, 'KEHANET', st.lt, 3) });
})();
