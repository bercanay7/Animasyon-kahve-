// CAM seti, SAHİP-2: P095. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. P001 (SAHİP-1) ile aynı eksen ve aynı animatik düzeltmeleri: telefon ~%15 küçük (pw 196), el camın sol kenarını kavrar (handY 400),
// ekran ışığı nötr/soğuk ve camın üst kenarından (phoneScene light 0 + kendi ışık katmanı; çene altında sıcak parıltı yok), yansıyan saçın ucu cam içinde yumuşak kararır.
'use strict';
(() => {
  const PW = 196;
  // tur 2 (Fable animatik tur 1: camda baş aşağı yansıma "mantıksız"): SAHİP-1'in P001'deki s1PhoneScene'inin birebir kopyası (lib/cam.js phoneScene + dik ayna yansıması).
  // flip 0: camda dik ayna yansıması; 1: su aynası. Ters dönme yalnız cam suya dönerken (burada su cama dönerken) olur. Ortak değişiklik önerisi: bu işlev lib/cam.js'e taşınırsa iki set de oradan çağırır.
  const s2PhoneScene = (ctx, t, o) => {
    const m = o.m, fl = o.flip ?? m;
    baseT(ctx);
    glaze(ctx, 1100, 820, 1100, `rgba(${lerp(80, 120, m) | 0},${lerp(42, 48, m) | 0},${lerp(28, 22, m) | 0},.45)`);
    const p = { torso: .3, neck: o.neckA ?? .42, head: (o.headA ?? .55) + (o.headNod || 0), shN: .38, elN: .5, shF: .32, elF: .55, handN: 'fist', handF: 'fist', smile: 0, brow: .15, mouthOpen: 0, blink: o.blink,
      mouthFlat: !!o.neutral, eyeWide: o.neutral ? .3 : 0 };
    let f = { x: 0, y: 0, s: 20.5, dir: 1, sty: STY.red, lk: LK_MOD, seed: 31, idle: .6, p, faceW: 1.35, stripe: .35 };
    f = placeNeck(ctx, f, o.neck || [640, 370]);
    const { J: J0, M: M0 } = joints(ctx, f), e = headPt(ctx, J0, M0, [3.7, -6.75]);
    const wy = o.wy ?? 600, pcx = e[0] + (o.phDx ?? 330), pw = o.pw ?? 270;
    const dxR = o.refDx != null ? o.refDx : lerp(pcx - e[0] - 20, 0, m);
    const hy = o.handY ?? 340;
    if (o.armToPhone) { f.ik = { hN: [pcx - pw - 70, wy + hy + 120 + 420 * m] }; f.noFarArm = true; }
    camAt(ctx, ...o.cam);
    const shape = morphPts(roundRectPts(pcx - pw, wy, pcx + pw, wy + 900, 56, 56), ellipsePts(pcx - 100, wy + 360, 1300, 360), m);
    const clip = c => poly(c, shape);
    waterBody(ctx, clip, wy, t, { a: .2 * m, seed: 6, span: [300, 2100], n: 40 });
    if (o.feedA > .005) phoneFeed(ctx, clip, pcx, pw, wy, o.feed || 0, o.feedA * (1 - m));
    const rings = typeof o.rings === 'function' ? o.rings(pcx, wy, e) : o.rings;
    // yansıma çapası: camda gözün dik aynası camın ortasında; suda su aynasının göz noktası
    const C0 = [pcx - 18, wy + 275], C1 = [e[0] + dxR, 2 * wy - e[1]], C = lerp2(C0, C1, E.io2(fl)), th = PI * E.io2(fl), ca = Math.cos(th), sa = Math.sin(th);
    const refMap = q => { const vx = -(q[0] - e[0]), vy = q[1] - e[1]; return [C[0] + ca * vx - sa * vy, C[1] + sa * vx + ca * vy]; };
    mirror(ctx, c => { c.scale(1, -1); c.translate(-dxR, -2 * wy); c.translate(C[0], C[1]); c.rotate(th); c.scale(-1, 1); c.translate(-e[0], -e[1]); figure(c, f); },
      wy, clip, t, { a: o.refA ?? .42, rings, calm: lerp(.15, 1.2, m), dx: dxR, calmAt: o.eyeCalm ? { x: C[0], y: C[1], r: o.eyeCalm } : null });
    const ph = 1 - m;
    if (o.glare && ph > .01) glassGlare(ctx, clip, pcx, wy, pw, ph * o.glare, t);
    if (ph > .01) {
      ctx.save(); ctx.beginPath(); clip(ctx); ctx.clip();
      const g = ctx.createLinearGradient(pcx - 200, wy, pcx + 250, wy + 600); g.addColorStop(0, 'rgba(255,240,215,0)'); g.addColorStop(.45, `rgba(255,240,215,${.07 * ph})`); g.addColorStop(.55, `rgba(255,240,215,${.07 * ph})`); g.addColorStop(1, 'rgba(255,240,215,0)');
      ctx.fillStyle = g; ctx.fillRect(600, wy, 1100, 900); ctx.restore();
      ctx.save(); ctx.globalAlpha = ph; ctx.fillStyle = '#21160f';
      ctx.beginPath(); ctx.roundRect(pcx - 50, wy + 20, 100, 13, 6.5); ctx.fill();
      ctx.beginPath(); ctx.arc(pcx + 78, wy + 26, 7, 0, TAU); ctx.fill(); ctx.restore();
    }
    ctx.save(); ctx.beginPath(); poly(ctx, shape); ctx.lineWidth = lerp(4.5, 6, m); ctx.strokeStyle = mixCol('#B9653A', '#C9703F', m); ctx.lineJoin = 'round'; ctx.stroke(); ctx.restore();
    if (o.light > 0) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, pcx - 120, wy, 420, `rgba(255,220,170,${.14 * o.light})`); ctx.restore(); }
    litFigure(ctx, f, { x: e[0] + 120, y: wy + 20, r: 430, c: 'rgba(255,226,186,A)', a: .34 * o.light, dark: .25 + .25 * o.light });
    if (ph > .02) phoneHand(ctx, pcx - pw, wy, t, ph, o.thumb || 0, o.light, hy);
    return { f, refMap, shape, e, pcx, C, fl };
  };
  // P095 · orta-yakın · F11 · Çerçeve kapanır: havuzun kıyısı telefonun kenarına döner (kapı E); camda bugünün genci ve birebir yansıması; ekran ışığı kararmaya başlar. Ahlak dersi yok: el telefonu bırakmaz
  plan('P095', (ctx, st) => {
    const t = st.t, tC = PE('P095', 0), tB = PE('P095', 1), tY = PE('P095', 2), tR = PE('P095', 3);
    const u = ramp(t, tC, tB, E.io2), m = 1 - u;
    const z = lerp(1.22, .84, u) + .04 * ramp(t, tB, st.end, E.lin), fx = lerp(990, 720, u), fy = lerp(760, 652, u);
    const dim = ramp(t, tR - .1, tR + 1.8, E.io2);
    const R = s2PhoneScene(ctx, t, { ...PH3, pw: PW, handY: 400, m, flip: m, cam: [fx, fy, z], light: 0, refA: lerp(.26, .2, u) * (1 - .35 * dim), refDx: 240 * E.io2(m),
      headNod: .03 * Math.sin(t * .9) - .02 * ramp(t, tY - .2, tY + .6, E.io2),
      rings: (cx, wy) => [{ x: cx + 240, y: wy + 330, t0: st.at - .2, A: 7, sq: .32, v: 220, lam: 40, k: .7, reach: 1000, life: 3.5, mask: 80 }] });
    const f = R.f, { J, M } = joints(ctx, f), eS = headPt(ctx, J, M, [EYE_Q[0] * LK_MOD.headS, EYE_Q[1] * LK_MOD.headS]), wy = PH3.wy, pcx = R.pcx, ph = (1 - m) * (1 - .85 * dim);
    if (ph > .01) { // nötr ekran ışığı, yalnız figürün üstünde
      const T = ctx.getTransform(), L = layer('s2lit'); L.setTransform(1, 0, 0, 1, 0, 0); L.drawImage(LY.fig, 0, 0);
      L.globalCompositeOperation = 'source-in'; L.setTransform(T);
      const g = L.createRadialGradient(pcx - 40, wy + 10, 0, pcx - 40, wy + 10, 300); g.addColorStop(0, `rgba(214,224,230,${.26 * ph})`); g.addColorStop(.5, `rgba(214,224,230,${.1 * ph})`); g.addColorStop(1, 'rgba(214,224,230,0)');
      L.fillStyle = g; L.fillRect(pcx - 400, wy - 320, 760, 340);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'screen'; ctx.drawImage(LY.s2lit, 0, 0); ctx.restore();
      ctx.save(); ctx.globalAlpha = .5 * ph; ctx.strokeStyle = 'rgba(214,226,232,.6)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(pcx - PW + 50, wy + 3); ctx.lineTo(pcx + PW - 50, wy + 3); ctx.stroke(); ctx.restore();
    }
    // yansımanın uzak ucu: cam içinde yumuşak karartma; yön yansımanın dönüşünü izler (P001 ile aynı)
    const rE = R.refMap(eS), off = lerp(150, 70, R.fl), shape = R.shape;
    ctx.save(); ctx.beginPath(); poly(ctx, shape); ctx.clip();
    const g2 = ctx.createLinearGradient(0, rE[1] + off, 0, rE[1] + off + 180); g2.addColorStop(0, 'rgba(6,3,2,0)'); g2.addColorStop(1, 'rgba(6,3,2,.82)');
    ctx.fillStyle = g2; ctx.fillRect(pcx - 1600, rE[1] + off, 3200, 1400);
    if (dim > 0) { ctx.fillStyle = `rgba(6,3,2,${(.35 * dim).toFixed(3)})`; ctx.fillRect(pcx - 1600, wy - 10, 3200, 1600); }
    ctx.restore();
  });
})();
