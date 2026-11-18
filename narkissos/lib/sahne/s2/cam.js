// CAM seti, SAHİP-2: P095. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. P001 (SAHİP-1) ile aynı eksen ve aynı animatik düzeltmeleri: telefon ~%15 küçük (pw 196), el camın sol kenarını kavrar (handY 400),
// ekran ışığı nötr/soğuk ve camın üst kenarından (phoneScene light 0 + kendi ışık katmanı; çene altında sıcak parıltı yok), yansıyan saçın ucu cam içinde yumuşak kararır.
'use strict';
(() => {
  const PW = 196;
  // P095 · orta-yakın · F11 · Çerçeve kapanır: havuzun kıyısı telefonun kenarına döner (kapı E); camda bugünün genci ve birebir yansıması; ekran ışığı kararmaya başlar. Ahlak dersi yok: el telefonu bırakmaz
  plan('P095', (ctx, st) => {
    const t = st.t, tC = PE('P095', 0), tB = PE('P095', 1), tY = PE('P095', 2), tR = PE('P095', 3);
    const u = ramp(t, tC, tB, E.io2), m = 1 - u;
    const z = lerp(1.22, .84, u) + .04 * ramp(t, tB, st.end, E.lin), fx = lerp(990, 720, u), fy = lerp(760, 652, u);
    const dim = ramp(t, tR - .1, tR + 1.8, E.io2);
    const f = phoneScene(ctx, t, { ...PH3, pw: PW, handY: 400, m, cam: [fx, fy, z], light: 0, refA: lerp(.26, .2, u) * (1 - .35 * dim), refDx: 240 * E.io2(m),
      headNod: .03 * Math.sin(t * .9) - .02 * ramp(t, tY - .2, tY + .6, E.io2),
      rings: (cx, wy) => [{ x: cx + 240, y: wy + 330, t0: st.at - .2, A: 7, sq: .32, v: 220, lam: 40, k: .7, reach: 1000, life: 3.5, mask: 80 }] });
    const { J, M } = joints(ctx, f), e = headPt(ctx, J, M, EYE_Q), eS = headPt(ctx, J, M, [EYE_Q[0] * LK_MOD.headS, EYE_Q[1] * LK_MOD.headS]), wy = PH3.wy, pcx = e[0] + PH3.phDx, ph = (1 - m) * (1 - .85 * dim);
    if (ph > .01) { // nötr ekran ışığı, yalnız figürün üstünde
      const T = ctx.getTransform(), L = layer('s2lit'); L.setTransform(1, 0, 0, 1, 0, 0); L.drawImage(LY.fig, 0, 0);
      L.globalCompositeOperation = 'source-in'; L.setTransform(T);
      const g = L.createRadialGradient(pcx - 40, wy + 10, 0, pcx - 40, wy + 10, 300); g.addColorStop(0, `rgba(214,224,230,${.26 * ph})`); g.addColorStop(.5, `rgba(214,224,230,${.1 * ph})`); g.addColorStop(1, 'rgba(214,224,230,0)');
      L.fillStyle = g; L.fillRect(pcx - 400, wy - 320, 760, 340);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'screen'; ctx.drawImage(LY.s2lit, 0, 0); ctx.restore();
      ctx.save(); ctx.globalAlpha = .5 * ph; ctx.strokeStyle = 'rgba(214,226,232,.6)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(pcx - PW + 50, wy + 3); ctx.lineTo(pcx + PW - 50, wy + 3); ctx.stroke(); ctx.restore();
    }
    const shape = morphPts(roundRectPts(pcx - PW, wy, pcx + PW, wy + 900, 56, 56), ellipsePts(pcx - 100, wy + 360, 1300, 360), m);
    const ry = 2 * wy - eS[1];
    ctx.save(); ctx.beginPath(); poly(ctx, shape); ctx.clip();
    const g2 = ctx.createLinearGradient(0, ry + 70, 0, ry + 250); g2.addColorStop(0, 'rgba(6,3,2,0)'); g2.addColorStop(1, 'rgba(6,3,2,.82)');
    ctx.fillStyle = g2; ctx.fillRect(pcx - 1600, ry + 70, 3200, 1400);
    if (dim > 0) { ctx.fillStyle = `rgba(6,3,2,${(.35 * dim).toFixed(3)})`; ctx.fillRect(pcx - 1600, wy - 10, 3200, 1600); }
    ctx.restore();
  });
})();
