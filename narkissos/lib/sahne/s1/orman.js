// ORMAN seti, SAHİP-1: P013, P016, P017, P020, P021, P022, P023, P024, P025, P026, P027, P028, P034. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Yardımcılar S1 (s1/cam.js). Yön düzeni: Narkissos solda sağa bakar, Eko sağda sola bakar (konuşma yazısı soldan sağa okunur;
// Eko'nun yankısı sola akar). Eko giyinik (khiton + himation), yüz ve kollar açık; sarılma gösterilmez.
'use strict';
(() => {
  const S1 = window.S1;
  const NK = (o) => S1.ayakta(o.ctx, { sty: STY.red, lk: LK_NK, seed: 23, ...o });
  // Eko (ayakta): o: {x, gy, s, dir, p, ik, agiz (0..1 ağız aralığı), gul (gülümseme 0..2)}; döner {f, J, M}
  S1.eko = (ctx, o) => {
    let J = null, M = null;
    const f = { x: o.x, y: o.gy - 44.5 * o.s, s: o.s, dir: o.dir ?? -1, sty: S1.RFF, lk: S1.LK_EKO, seed: o.seed ?? 71, stripe: .45, idle: o.idle ?? .8,
      p: { smile: o.gul || 0, ...(o.p || {}) }, ik: o.ik, alpha: o.alpha, onJoints: (j, m) => { J = j; M = m; } };
    figure(ctx, f);
    if (o.agiz > .02 && J) { const q = headPt(ctx, J, M, [5.25, -3.75]); ctx.save(); ctx.translate(q[0], q[1]); ctx.rotate(J.headA * (o.dir ?? -1)); ctx.beginPath(); ctx.ellipse(0, 0, .55 * o.s, .38 * o.s * o.agiz, 0, 0, TAU); ctx.fillStyle = '#2A140A'; ctx.globalAlpha *= (o.alpha ?? 1); ctx.fill(); ctx.restore(); }
    return { f, J, M };
  };
  const agizNok = (ctx, r) => headPt(ctx, r.J, r.M, [6.2, -3.9]);
  // sola akan söz (Eko ya da sola bakan konuşan): metin sağa hizalı, ağzın solunda; p ile belirir
  const sozSola = (ctx, s, x, y, px, p, o = {}) => { if (p <= 0) return; ctx.save(); ctx.font = FONT.baslik(px, 700); ctx.textAlign = 'right'; ctx.textBaseline = 'middle'; ctx.letterSpacing = Math.round(px * .14) + 'px';
    ctx.fillStyle = o.col || S1.KIL; ctx.globalAlpha *= E.sine(clamp(p)) * (o.a ?? 1); if (o.glow) { ctx.shadowColor = o.glow; ctx.shadowBlur = 20; }
    ctx.translate(x - (1 - E.out3(clamp(p))) * -30, y); ctx.scale(lerp(.7, 1, E.out3(clamp(p))), lerp(.7, 1, E.out3(clamp(p)))); ctx.fillText(s, 0, 0); ctx.restore(); };
  // ön plan ağaç gövdesi (paralaks): koyu, kil konturlu
  const govde = (ctx, x, w = 120) => { ctx.save(); ctx.beginPath(); ctx.moveTo(x - w / 2, 1300); ctx.bezierCurveTo(x - w * .45, 700, x - w * .7, 300, x - w * .4, -300); ctx.lineTo(x + w * .4, -300); ctx.bezierCurveTo(x + w * .6, 300, x + w * .45, 700, x + w / 2, 1300); ctx.closePath();
    ctx.fillStyle = '#120906'; ctx.fill(); ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 4; ctx.stroke();
    ctx.strokeStyle = 'rgba(201,112,63,.22)'; ctx.lineWidth = 3; for (let i = 0; i < 6; i++) { ctx.beginPath(); ctx.moveTo(x - w * .2 + i * 8, 100 + i * 150); ctx.quadraticCurveTo(x, 160 + i * 150, x + w * .2, 120 + i * 150); ctx.stroke(); } ctx.restore(); };
  const AGACLAR = [[120, 2.0, 3], [520, 1.6, 8, 6], [1380, 1.9, 5], [1800, 2.1, 11], [2250, 1.7, 13, 6], [-260, 1.8, 2]];
  const UZAK = [[300, 1.3, 31, 5], [800, 1.2, 33, 5], [1100, 1.4, 35, 6], [1600, 1.25, 37, 5], [2000, 1.35, 39, 6], [2500, 1.3, 41, 5]];

  // ---- P013 · orta · B04: on altı yaşında Narkissos avcı, orman kenarında yürür; 'narkissos'ta kadraja yürür, 'on'da durur, mızrağı omzuna alır, başını çevirir ----
  plan('P013', (ctx, st) => {
    const t = st.t, tN = PE('P013', 0), tO = PE('P013', 1), gy = 900, s = 7.2;
    const t0 = tN - 1.1, xw = lerp(-120, 1000, E.out2(clamp((t - t0) / (tO + .1 - t0)))), stand = ramp(t, tO - .2, tO + .3, E.io2);
    baseT(ctx); camAt(ctx, lerp(760, 920, ramp(t, t0, tO + .6, E.io2)) + 18 * E.sine(st.p), 520, 1.0);
    S1.orman(ctx, t, { gy, trees: [[60, 2.4, 3, 7, 120], [1500, 2.6, 5, 7, 130], [1880, 2.2, 11]], far: UZAK });
    const sh = ramp(t, tO + .05, tO + .7, E.io2), turn = t > tO + .55;
    let J = null, M = null;
    walkScene(ctx, null, xw, s, t, 1, { ground: groundOf(() => gy), noCam: true, sty: STY.red, lk: LK_NK, dist: xw, stand, stripe: .5, lean: .06,
      onJoints: (j, m) => { J = j; M = m; }, p: { shF: lerp(-.55, -2.5, sh), elF: lerp(-.2, -1.9, sh), headBack: turn, headBackA: .1 } });
    if (J) spear(ctx, jointPt(ctx, M, J.AF.wr), lerp(-1.2, -2.25, sh), 62 * s, s * .9);
    // yaprak düşer (hareket)
    for (let i = 0; i < 3; i++) { const u = ((t - st.at) * .25 + i * .33) % 1; ctx.save(); ctx.translate(lerp(300 + i * 500, 420 + i * 500, u) + 40 * Math.sin(u * 9), lerp(80, gy, u)); ctx.rotate(u * 9); ctx.beginPath(); ctx.ellipse(0, 0, 14, 5, 0, 0, TAU); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.6; ctx.stroke(); ctx.restore(); }
  });

  // ---- P016 · geniş · B06: geyik ağaçların arasından fırlar, Narkissos mızrakla peşinde koşar; 'biri'de ön planda yaprakların arasında biri durur: yalnız gözü seçilir (Eko) ----
  plan('P016', (ctx, st) => {
    const t = st.t, tG = PE('P016', 0), tB = PE('P016', 1), gy = 820, s = 4.4;
    const dx = clamp((t - (tG - .5)) / 2.3), dxN = clamp((t - (tG + .25)) / 2.6);
    baseT(ctx); camAt(ctx, lerp(820, 1120, E.io2(clamp((t - tG + .5) / 3))), 520, 1.0);
    S1.orman(ctx, t, { gy, trees: [[-80, 1.9, 3], [430, 1.5, 8, 6], [1050, 1.7, 5], [1620, 1.8, 11], [2160, 1.6, 13]], far: UZAK });
    if (dx > 0 && dx < 1) S1.geyik(ctx, lerp(-260, 2500, dx), gy - 108, 1.55, t * 13);
    if (dxN > 0 && dxN < 1) { const xw = lerp(-260, 2300, dxN); let J = null, M = null;
      walkScene(ctx, null, xw, s, t, 1, { ground: groundOf(() => gy), noCam: true, sty: STY.red, lk: LK_NK, stride: 72, /* dist = x·yön: basan ayak yerde sabit (kayma yok) */ stripe: .5, lean: .28, onJoints: (j, m) => { J = j; M = m; }, p: { shF: .9, elF: -.6, shN: -.6, elN: 1.2 } });
      if (J) spear(ctx, jointPt(ctx, M, J.AF.wr), -.35, 62 * s, s * .9); }
    // ön plan (kamera dışı, paralaks): sağda yaprak perdesi; 'biri'de aralanır, gölgede bir göz açılır (Eko)
    baseT(ctx);
    const ac = ramp(t, tB - .3, tB + .5, E.io2), px = 1500 - 60 * E.sine(st.p);
    const L = layer('s1eko'); L.setTransform(ctx.getTransform());
    const r = S1.eko(L, { x: px + 190, gy: 440 + 37 * 28 + 44.5 * 28, s: 28, dir: -1, p: { blink: 1 - ramp(t, tB - .05, tB + .2, E.out3), neck: .05, head: .05 } });
    const e = headPt(L, r.J, r.M, [3.9, -7.05]);
    // yaprak gölgesi yalnız figürün üstünde: yüz karanlık, göz çevresi seçilir
    L.globalCompositeOperation = 'source-atop'; const g = L.createRadialGradient(e[0], e[1], 20, e[0], e[1], 190); // Fable tur 1: göz küçük kalıyordu → gözün çevresi açık, yüz yaprak gölgesinde g.addColorStop(0, 'rgba(8,4,2,0)'); g.addColorStop(.16, 'rgba(8,4,2,.08)'); g.addColorStop(.4, 'rgba(8,4,2,.8)'); g.addColorStop(1, 'rgba(8,4,2,.96)');
    L.fillStyle = g; L.fillRect(-500, -500, 3000, 2500);
    // yalnız baş görünür: yaprakların arasından (yumuşak kenarlı maske)
    L.globalCompositeOperation = 'destination-in'; const g2 = L.createRadialGradient(e[0] - 40, e[1] + 20, 90, e[0] - 40, e[1] + 20, 340); g2.addColorStop(0, '#000'); g2.addColorStop(1, 'rgba(0,0,0,0)');
    L.fillStyle = g2; L.fillRect(-500, -500, 3000, 2500); L.globalCompositeOperation = 'source-over';
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(LY.s1eko, 0, 0); ctx.restore();
    for (let i = 0; i < 5; i++) S1.dal(ctx, 1980 - i * 40 + 70 * ac * (i % 2 ? 1 : -.3), 160 + i * 150 + (160 + i * 150 < 360 ? -120 : 130) * ac, 1.9, PI + (i - 2) * .25 + ac * (i % 2 ? -.25 : .2), t, 90 + i, { koyu: true, L: 320, leaf: 50 });
  }, { mb: 6 });

  // ---- P017 · orta · C01: Eko ağacın arkasından çıkar; 'eko'da ΗΧΩ yazılır; 'susmayı'da ağzı aralanıp kapanır; 'konuşmayı'da eli dudağına gider ----
  plan('P017', (ctx, st) => {
    const t = st.t, tE = PE('P017', 0), tS = PE('P017', 1), tK = PE('P017', 2), gy = 900, s = 7.4;
    const fx = lerp(900, 1010, E.sine(st.p));
    baseT(ctx); camAt(ctx, fx, 520, 1.0);
    S1.orman(ctx, t, { gy, trees: [[300, 2.2, 3], [1650, 2.4, 5, 7, 130], [2100, 2.0, 11]], far: UZAK });
    const xw = lerp(800, 1180, E.out2(ramp(t, st.at, tE + .2, E.lin))), stand = ramp(t, tE - .3, tE + .2, E.io2);
    const ag = Math.max(0, Math.sin((t - tS) * PI / .45)) * (t > tS && t < tS + .9 ? 1 : 0);
    const el = ramp(t, tK - .1, tK + .6, E.io2);
    let r;
    if (stand < 1) { let J = null, M = null; walkScene(ctx, null, xw, s, t, -1, { ground: groundOf(() => gy), noCam: true, sty: S1.RFF, lk: S1.LK_EKO, dist: -xw, stand, stripe: .45, onJoints: (j, m) => { J = j; M = m; } }); }
    else {
      const f0 = { x: xw, y: gy - 44.5 * s, s, dir: -1, sty: S1.RFF, lk: S1.LK_EKO, seed: 71 };
      const { J, M } = joints(ctx, f0), lip = headPt(ctx, J, M, [7.6, -3.4]);
      r = S1.eko(ctx, { x: xw, gy, s, dir: -1, agiz: ag, ik: el > 0 ? { hN: lerp2(jointPt(ctx, M, add(J.shoulder, [6, 24])), lip, el) } : undefined, p: { handN: 'open', shF: .1, elF: .3 } });
    }
    dipintoYaz(ctx, 'ΗΧΩ', xw + 120, 330, 40, ramp(t, tE, tE + .7, E.lin), { col: S1.KIL, w: .11 });
    // ön plan gövdesi (paralaks): sola kayar, Eko onun arkasından çıkar
    baseT(ctx); govde(ctx, 980 - (fx - 900) * 2.6 - 260 * ramp(t, st.at, tE, E.io2), 180);
  }, { over: (ctx, st) => { S1.bolumKarti(ctx, 'YANKI', st.lt, 3); const tE = PE('P017', 0); if (st.t > tE + .5) etiket(ctx, 'EKO', 1320, 250, st.t - tE - .5, 99, { px: 42 }); } });

  // ---- P020 · ters açı · C03: Eko'nun omzunun üstünden açıklıkta uzakta Narkissos. 'aşık'ta dalı aralar, 'söylemek'te ağzından harfsiz bir şerit çıkar, 'söyleyemez'de söner, 'başkasının'da geri çekilir ----
  plan('P020', (ctx, st) => {
    const t = st.t, tA = PE('P020', 0), tS = PE('P020', 1), tY = PE('P020', 2), tB = PE('P020', 3), gy = 760;
    const geri = ramp(t, tB, tB + .9, E.io2);
    baseT(ctx); camAt(ctx, lerp(960, 1040, E.sine(st.p)), 540, 1.0);
    S1.orman(ctx, t, { gy, trees: [[1000, 1.3, 31, 6], [1850, 1.4, 33, 6], [2200, 1.2, 35]], far: [[1300, 1.0, 37, 5], [1600, .9, 39, 5]] });
    // uzakta açıklıkta Narkissos (küçük), mızrağıyla
    NK({ ctx, x: 1420, gy, s: 2.6, dir: -1, p: { shF: -.3, elF: -.4 } });
    const ar = ramp(t, tA - .2, tA + .6, E.io2);
    // aralanan dallar: sağdan Eko'ya doğru sarkar; 'aşık'ta eli dalları yukarı iter
    for (let i = 0; i < 3; i++) S1.dal(ctx, 1150, 470 + i * 75, 1.4, PI - .05 + i * .06 + ar * (.55 - i * .1), t, 60 + i, { L: 300, leaf: 42 });
    // Eko ön planda (büyük, sol alt), sağa bakar
    const s = 15, ex = 440 - 90 * geri;
    const r = S1.eko(ctx, { x: ex, gy: 470 + 44.5 * s + 36 * s, s, dir: 1, p: { neck: .1 * geri, head: .1 * geri, handN: 'open' }, ik: { hN: [lerp(ex + 260, ex + 330, ar) - 120 * geri, lerp(640, 520, ar)] } });
    // harfsiz şerit ('söylemek'): ağızdan uzar, 'söyleyemez'de söner
    const m = headPt(ctx, r.J, r.M, [6.4, -3.9]), uz = ramp(t, tS, tS + 1.1, E.out2), son = 1 - ramp(t, tY - .1, tY + .5, E.io2);
    if (uz > 0 && son > 0) { const P = S1.konusmaYolu(m[0] + 30, m[1], -.08, 700 * uz, t, { amp: 16, k: .02 });
      // boş yazı şeridi: iki ince kil çizgi arasında harf yeri boş (söz söylenemez)
      ctx.save(); ctx.globalAlpha = son * .75; ctx.lineCap = 'round'; ctx.strokeStyle = S1.KIRMIZI; ctx.lineWidth = 2.5;
      for (const o of [-22, 22]) { ctx.beginPath(); P.forEach((q, i) => { const a2 = i ? Math.atan2(q[1] - P[i - 1][1], q[0] - P[i - 1][0]) : 0, x = q[0] - Math.sin(a2) * o, y = q[1] + Math.cos(a2) * o; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke(); }
      ctx.setLineDash([6, 30]); ctx.lineWidth = 3; ctx.beginPath(); P.forEach((q, i) => i ? ctx.lineTo(...q) : ctx.moveTo(...q)); ctx.stroke(); ctx.restore(); }
  }, { tr: trOf('P020') });

  // ---- P021 · geniş · C04: arkadaşları ağaçların ardında kaybolur, Narkissos yalnız kalır ve seslenir; 'kim'de KİM VAR BURADA? ağaçlara akar ----
  plan('P021', (ctx, st) => {
    const t = st.t, tA = PE('P021', 0), tS = PE('P021', 1), tK = PE('P021', 2), gy = 820, s = 4.6;
    baseT(ctx); camAt(ctx, lerp(900, 1000, E.sine(st.p)), 520, 1.0);
    S1.orman(ctx, t, { gy, trees: AGACLAR, far: UZAK });
    // arkadaşlar sağa yürüyüp ağaçların ardında kaybolur
    for (const [x0, sd, k] of [[1000, 81, 0], [1150, 83, .35]]) { const u = ramp(t, tA - 1.2 + k, tA + 1.3 + k, E.lin), xw = lerp(x0, x0 + 900, u);
      if (u < 1) walkScene(ctx, null, xw, s * .95, t, 1, { ground: groundOf(() => gy), noCam: true, sty: STY.red, lk: S1.LK_GENC, dist: xw, stripe: .45, alpha: 1 - ramp(u, .75, 1, E.lin) }); }
    vaseTree(ctx, 1800, gy, 2.1, 11, t, { branches: 7, reach: 110 }); // arkadaşlar bu ağacın ardında kaybolur
    const el = ramp(t, tS - .1, tS + .5, E.io2);
    const f0 = { x: 620, y: gy - 44.5 * s, s, dir: 1, sty: STY.red, lk: LK_NK, seed: 23 };
    const { J, M } = joints(ctx, f0), lip = headPt(ctx, J, M, [6.6, -2.4]);
    const f = NK({ ctx, x: 620, gy, s, dir: 1, p: { head: -.12 * el, neck: -.08 * el, handN: 'open', shF: -.4, elF: -.3 }, ik: el > .01 ? { hN: lerp2(jointPt(ctx, M, add(J.shoulder, [5, 26])), lip, el) } : undefined });
    spear(ctx, [560, gy - 30 * s], -1.35, 62 * s, s * .9);
    const m = headPt(ctx, J, M, [7.5, -3.6]);
    const p = ramp(t, tK - .05, tK + 1.0, E.lin);
    S1.yolYazi(ctx, 'KİM VAR BURADA?', S1.konusmaYolu(m[0] + 40, m[1] - 10, -.12, 1100, t, { amp: 12 }), p, { px: 46, col: S1.KIL });
  });

  // ---- P022 · yakın · C04@bir: Eko'nun yüzü yaprakların arasında; gelen yazı ulaşır, 'cevap'ta KİM VAR söner, 'burada'da BURADA! Eko'dan solarak tekrar eder ----
  const ekoYakin = (ctx, t, o) => { const s = o.s || 22; return S1.eko(ctx, { x: o.x ?? 1300, gy: (o.hy ?? 420) + 37 * s + 44.5 * s, s, dir: -1, gul: o.gul, agiz: o.agiz, idle: .5, p: { neck: .05 + (o.neck || 0), head: .02 + (o.head || 0), shN: o.shN ?? .3, elN: .4, shF: o.shF ?? .2, handN: 'open', handF: 'open' } }); };
  plan('P022', (ctx, st) => {
    const t = st.t, tC = PE('P022', 0), tB = PE('P022', 1);
    baseT(ctx); glaze(ctx, 1200, 800, 1200, 'rgba(110,46,22,.42)');
    for (const [x, sc, sd] of [[300, 1.6, 31], [800, 1.4, 33], [1700, 1.5, 35]]) { ctx.save(); ctx.globalAlpha = .35; vaseTree(ctx, x, 1100, sc, sd, t, { fill: '#7A3D20' }); ctx.restore(); }
    const r = ekoYakin(ctx, t, { x: 1380, agiz: Math.max(0, Math.sin((t - tB) * PI / .5)) * (t > tB && t < tB + 1 ? 1 : 0) });
    const m = agizNok(ctx, r);
    // gelen yazı: soldan gelir; 'cevap'ta KİM VAR söner
    const gel = ramp(t, st.at - .4, tC, E.out2), fd = 1 - ramp(t, tC, tC + .6, E.io2), fd2 = 1 - ramp(t, tB + .6, tB + 1.4, E.io2);
    const x1 = lerp(-500, m[0] - 80, gel);
    S1.yolYazi(ctx, 'KİM VAR BURADA?', [[x1 - 900, m[1] - 30], [x1, m[1] - 30]], 1, { px: 52, col: S1.KIL, fade: i => (i < 8 ? fd : fd2) });
    if (t > tB) S1.yanki(ctx, 'BURADA!', m[0] - 220, m[1] + 80, t, tB, { dx: -1, px: 60, dt: .5, col: S1.KIRMIZI, reps: ['BURADA!', 'burada', 'rada'], life: 2.6 });
    // ön plan yapraklar (paralaks)
    const k = (t - st.at) * 22;
    S1.perde(ctx, t, 2080 - k, 60, 2, 7, { ang: PI - .5, s: 1.1, dy: 90 }); S1.perde(ctx, t, 2060 - k * .8, 760, 2, 8, { ang: PI + .3, s: 1.2 }); S1.perde(ctx, t, -60 + k * .6, 650, 3, 9, { ang: 0, s: 1.7 });
  });

  // ---- P023 · orta · C05: Narkissos ağaçlara seslenir (GEL!); yankı başka yönden gelir, başını çevirir; 'burada'da BURADA BULUŞALIM! ----
  plan('P023', (ctx, st) => {
    const t = st.t, tG = PE('P023', 0), tG2 = PE('P023', 1), tBu = PE('P023', 2), gy = 920, s = 7.4;
    baseT(ctx); camAt(ctx, lerp(940, 1020, E.sine(st.p)), 520, 1.0);
    S1.orman(ctx, t, { gy, trees: [[150, 2.3, 3], [1700, 2.4, 5], [2150, 2.1, 11]], far: UZAK });
    const turn = t > tG2 + .25;
    const f0 = { x: 900, y: gy - 44.5 * s, s, dir: -1, sty: STY.red, lk: LK_NK, seed: 23, p: { headBack: turn, headBackA: .05 } };
    const { J, M } = joints(ctx, f0);
    NK({ ctx, x: 900, gy, s, dir: -1, p: { headBack: turn, headBackA: .05, head: -.1, shF: -.3, elF: -.3, shN: turn ? .5 : 1.3, elN: turn ? .4 : .3, handN: 'open' } });
    spear(ctx, [940, gy - 30 * s], -1.75, 62 * s, s * .9);
    const m = headPt(ctx, J, M, [7.5, -3.6]);
    // GEL! sola (ağaçlara)
    if (!turn || t < tG2 + .8) sozSola(ctx, 'GEL!', m[0] - 40, m[1] - 20, 64, ramp(t, tG, tG + .3, E.out2) * (1 - ramp(t, tG2 + .2, tG2 + .8, E.io2)), { col: S1.KIL });
    // yankı: sağdaki ağaçların arasından
    if (t > tG2) S1.yanki(ctx, 'GEL!', 1660, 600, t, tG2, { dx: -1, px: 64, dt: .4, reps: ['GEL!', 'gel', 'el'], life: 2.2 });
    // başını çevirdi: BURADA BULUŞALIM! sağa
    if (turn) { const nk = jointPt(ctx, M, J.neckT), xm = 2 * nk[0] - m[0] + 40;
      S1.yolYazi(ctx, 'BURADA BULUŞALIM!', S1.konusmaYolu(xm, m[1] - 20, -.1, 1100, t, { amp: 10 }), ramp(t, tBu - .05, tBu + 1.1, E.lin), { px: 50, col: S1.KIL }); }
  });

  // ---- P024 · yakın · C06@eko: Eko'nun yüzü: 'sevinçle' gülümser; 'buluşalım'da BULUŞALIM! en büyük ve en parlak yankı ----
  plan('P024', (ctx, st) => {
    const t = st.t, tS = PE('P024', 0), tB = PE('P024', 1);
    baseT(ctx); glaze(ctx, 1200, 800, 1200, 'rgba(120,50,24,.48)');
    camAt(ctx, 1100, 520, lerp(1.06, .97, E.sine(st.p)));
    for (const [x, sc, sd] of [[250, 1.6, 31], [700, 1.3, 33], [1900, 1.5, 35]]) { ctx.save(); ctx.globalAlpha = .35; vaseTree(ctx, x, 1150, sc, sd, t, { fill: '#7A3D20' }); ctx.restore(); }
    const gul = ramp(t, tS - .1, tS + .6, E.io2);
    const r = ekoYakin(ctx, t, { x: 1460, hy: 430, gul: 1.6 * gul, head: -.12 * gul, neck: -.05 * gul, agiz: .6 * Math.max(0, Math.sin((t - tB) * PI / .6)) * (t > tB && t < tB + 1.2 ? 1 : 0) });
    const m = agizNok(ctx, r);
    if (t > tB) S1.yanki(ctx, 'BULUŞALIM!', m[0] - 440, m[1] - 30, t, tB, { dx: -1, px: 92, dt: .55, col: '#F06A44', glow: 'rgba(255,120,70,.55)', reps: ['BULUŞALIM!', 'buluşalım', 'lım'], life: 3, decay: .7 });
    S1.perde(ctx, t, 2120 - (t - st.at) * 15, 780, 2, 17, { ang: PI + .3, s: 1.2 }); S1.perde(ctx, t, -80 + (t - st.at) * 12, 700, 3, 19, { ang: 0, s: 1.6 });
  });

  // ---- P025 · geniş · C06@ormandan: Eko ağaçların arasından çıkıp kollarını açarak ona koşar; 'boynuna'da neredeyse ulaşır (sarılma yok, plan kesilir) ----
  plan('P025', (ctx, st) => {
    const t = st.t, tK = PE('P025', 0), tB = PE('P025', 1), gy = 830, s = 4.8;
    const xw = lerp(2000, 910, E.out2(clamp((t - st.at + .2) / (tB + .6 - st.at)))), stand = ramp(t, tB + .1, tB + .7, E.io2);
    baseT(ctx); camAt(ctx, lerp(1150, 900, E.io2(clamp((t - st.at) / (tB + .8 - st.at)))), 520, 1.0);
    S1.orman(ctx, t, { gy, trees: [[-60, 1.9, 3], [380, 1.6, 8, 6], [1300, 1.8, 5], [2150, 1.9, 11], [2550, 1.7, 13]], far: UZAK });
    const geri = ramp(t, tB, tB + .8, E.io2);
    NK({ ctx, x: 560, gy, s, dir: 1, p: { torso: -.12 * geri, neck: -.1 * geri, head: -.06 * geri, shF: -.3, elF: -.4 } });
    // Fable tur 1: mızrak başın önünden geçiyordu → arkada, yere dayalı ve geriye yatık
    spear(ctx, [455, gy - 1 * s], -1.82, 62 * s, s * .9);
    // kollar dümdüz ("uyurgezer") değil: açık yay, dirsekler bükük, iki kol farklı; koşu x·yön mesafesiyle (ayak kaymaz)
    const kol = ramp(t, tK - .15, tK + .5, E.out3);
    walkScene(ctx, null, xw, s, t, -1, { ground: groundOf(() => gy), noCam: true, sty: S1.RFF, lk: S1.LK_EKO, stride: 44, stand, stripe: .45, lean: .18 * (1 - stand),
      p: { smile: 1.2, shN: lerp(.2, 1.25, kol), elN: lerp(.5, .75, kol), shF: lerp(-.2, .95, kol), elF: lerp(.4, .95, kol), wrN: -.2 * kol, handN: 'open', handF: 'open' } });
  }, { mb: 6 });

  // ---- P026 · orta · C07: Narkissos geri çekilir, eliyle iter; ANCAK BEN ÖLÜNCE BANA SAHİP OLURSUN; 'olursun'da döner, kaçar ----
  // P026 söz yolu: ağızdan yukarı-sola, sonra başın üstünden sağa (Eko'ya) düz şerit
  let p26M = null;
  const p26Yol = (m, t) => { const P = [], a = [m[0] - 10, m[1] - 20], c = [m[0] - 120, m[1] - 230], b = [m[0] + 160, m[1] - 250];
    for (let i = 0; i <= 16; i++) { const u = i / 16; P.push([(1 - u) * (1 - u) * a[0] + 2 * u * (1 - u) * c[0] + u * u * b[0], (1 - u) * (1 - u) * a[1] + 2 * u * (1 - u) * c[1] + u * u * b[1]]); }
    for (let i = 1; i <= 20; i++) P.push([b[0] + i * 70, b[1] + 6 * Math.sin(i * .6 + t * 1.3)]);
    return P; };
  plan('P026', (ctx, st) => {
    const t = st.t, tC = PE('P026', 0), tA = PE('P026', 1), tO = PE('P026', 2), gy = 920, s = 7.2;
    baseT(ctx); camAt(ctx, lerp(900, 960, E.sine(st.p)), 520, 1.0);
    S1.orman(ctx, t, { gy, trees: [[120, 2.3, 3], [1750, 2.3, 5], [2200, 2.0, 11]], far: UZAK });
    // Eko sağda: kollar açık yay hâlinden iner (dümdüz değil)
    const in_ = ramp(t, tC, tO + .5, E.io2);
    S1.eko(ctx, { x: 1500, gy, s, dir: -1, p: { shN: lerp(1.2, .35, in_), elN: lerp(.7, .3, in_), shF: lerp(1.0, .3, in_), elF: lerp(.9, .4, in_), handN: 'open', handF: 'open', neck: .08 * in_, head: .05 * in_ } });
    // Fable tur 1: reddediş okunmuyordu (karşılıklı uzanma) → Narkissos gövdesi ve başı Eko'dan dönük (sola, başı biraz kalkık),
    // yakın kol geriye uzanır, avuç Eko'ya dönük iter ('çek'); 'olursun'da kaçar (yürüyüş x·yön mesafesiyle, ayak kaymaz)
    const it = ramp(t, tC - .15, tC + .35, E.out3), kac = ramp(t, tO + .1, st.end, E.in2);
    const nx = 860 - 700 * kac - 40 * it;
    const pz = { torso: .16 * it, neck: -.06 * it, head: -.1 * it, shN: lerp(.1, -1.45, it), elN: lerp(.2, -.05, it), handN: 'flat', wrN: -1.45 * it, shF: .5, elF: .9 };
    if (kac < .05) {
      const f0 = { x: nx, y: gy - 44.5 * s, s, dir: -1, sty: STY.red, lk: LK_NK, seed: 23, p: pz }, { J, M } = joints(ctx, f0);
      // adım: öndeki ayak sola (uzaklaşma yönüne) atılmış
      NK({ ctx, x: nx, gy, s, dir: -1, p: pz, ik: { fN: [nx - 9 * s * it - 3 * s, gy - 3 * s, 0], fF: [nx + 6 * s * it + 2 * s, gy - 3 * s, 0] } });
      spear(ctx, jointPt(ctx, M, J.AF.wr), -1.75, 62 * s, s * .9);
      // söz: yüz sola dönük; şerit ağızdan yukarı çıkıp başın üstünden geriye, Eko'ya doğru kıvrılır (sözü arkasına atar)
      const m = headPt(ctx, J, M, [7.5, -3.6]); p26M = m;
      S1.yolYazi(ctx, 'ANCAK BEN ÖLÜNCE BANA SAHİP OLURSUN', p26Yol(m, t), ramp(t, tA - .05, tO + .55, E.lin), { px: 38, col: S1.KIL });
    } else {
      let J = null, M = null;
      walkScene(ctx, null, nx, s, t, -1, { ground: groundOf(() => gy), noCam: true, sty: STY.red, lk: LK_NK, stride: 44, stripe: .5, lean: .22, onJoints: (j, m) => { J = j; M = m; } });
      if (J) spear(ctx, jointPt(ctx, M, J.AF.wr), -2.0, 62 * s, s * .9);
      S1.yolYazi(ctx, 'ANCAK BEN ÖLÜNCE BANA SAHİP OLURSUN', p26Yol(p26M || [nx, 300], t), 1, { px: 38, col: S1.KIL, a: 1 - .3 * kac });
    }
  }, { mb: 6 });

  // ---- P027 · yakın · C08: Eko kollarını indirir; 'son'da ANCAK BEN ÖLÜNCE söner; 'bana'da BANA SAHİP OLURSUN Eko'dan çıkar (kırmızı) ----
  plan('P027', (ctx, st) => {
    const t = st.t, tS = PE('P027', 0), tB = PE('P027', 1);
    baseT(ctx); glaze(ctx, 1200, 800, 1200, 'rgba(110,46,22,.42)');
    camAt(ctx, 1080, 540, lerp(1.04, .95, E.sine(st.p)));
    for (const [x, sc, sd] of [[250, 1.6, 31], [800, 1.3, 33], [2000, 1.5, 35]]) { ctx.save(); ctx.globalAlpha = .35; vaseTree(ctx, x, 1150, sc, sd, t, { fill: '#7A3D20' }); ctx.restore(); }
    const in_ = ramp(t, st.at, tB, E.io2);
    const r = ekoYakin(ctx, t, { x: 1420, hy: 400, shN: lerp(1.3, .1, in_), shF: lerp(1.1, .05, in_), neck: .12 * in_, head: .1 * in_, agiz: .5 * Math.max(0, Math.sin((t - tB) * PI / .5)) * (t > tB && t < tB + 1 ? 1 : 0) });
    const m = agizNok(ctx, r);
    // havada asılı ret cümlesi: 'son'da ilk yarısı söner
    const fd = 1 - ramp(t, tS, tS + .6, E.io2);
    S1.yolYazi(ctx, 'ANCAK BEN ÖLÜNCE BANA SAHİP OLURSUN', [[-120, 200], [1300, 170]], 1, { px: 42, col: S1.KIL, a: .9, fade: (i) => (i < 17 ? fd : 1 - .85 * ramp(t, tB - .2, tB + .5, E.io2)) });
    if (t > tB) S1.yanki(ctx, 'BANA SAHİP OLURSUN', m[0] - 520, m[1] + 30, t, tB, { dx: -1, px: 56, dt: .7, col: '#E8583A', glow: 'rgba(255,110,70,.4)', reps: ['BANA SAHİP OLURSUN'], life: 4 });
  }, { over: (ctx, st) => kunye(ctx, 'Ovidius, Dönüşümler III 391–392', st.t - PE('P027', 1) - .2, 99) });

  // ---- P028 · ayrıntı · C09 · LEVHA: havada asılı BANA SAHİP OLURSUN; 'tut'ta parlar, 'sahibine'de ağaçların arasından uzaklaşır, 'dönecek'te son harf uzakta bir su yüzüne düşer ve yansır ----
  plan('P028', (ctx, st) => {
    const t = st.t, tT = PE('P028', 0), tS = PE('P028', 1), tD = PE('P028', 2);
    baseT(ctx); glaze(ctx, 1300, 700, 1300, 'rgba(110,46,22,.45)');
    const u = ramp(t, tS - .1, tD + .2, E.io2);
    camAt(ctx, lerp(900, 1160, u) + 60 * E.sine(st.p), 540, lerp(1.0, 1.05, E.sine(st.p)));
    // derinlik: uzak ağaçlar (soluk), uzakta küçük su yüzü
    for (const [x, sc, sd] of [[200, 1.1, 31], [700, .9, 33], [1250, 1.0, 35], [1900, .85, 37], [2400, 1.0, 39]]) { ctx.save(); ctx.globalAlpha = .45; vaseTree(ctx, x, 820, sc, sd, t, { fill: '#7A3D20' }); ctx.restore(); }
    const wy = 820, pool = c => c.ellipse(1720, wy + 14, 170, 18, 0, 0, TAU);
    ctx.save(); ctx.beginPath(); pool(ctx); ctx.fillStyle = '#050302'; ctx.fill(); ctx.lineWidth = 2.5; ctx.strokeStyle = PC.clayR; ctx.stroke(); ctx.restore();
    // yazı: yakında büyük, 'sahibine'de uzaklaşır (küçülür, sağa ve aşağı)
    const k = lerp(1, .3, u) * (1 + .04 * Math.sin(t * .9)), cx = lerp(880, 1560, u) + 18 * Math.sin(t * .7), cy = lerp(420, 690, u) + 16 * Math.sin(t * 1.3);
    const par = ramp(t, tT - .1, tT + .4, E.io2) * (1 - .5 * ramp(t, tT + .8, tT + 1.6, E.io2));
    const dus = ramp(t, tD, tD + .7, E.in2);
    ctx.save(); ctx.translate(cx, cy); ctx.scale(k, k);
    const dEnd = S1.yolYazi(ctx, 'BANA SAHİP OLURSU', [[-720, 0], [900, -10]], 1, { px: 80, col: '#E8583A' });
    ctx.restore();
    if (par > .01) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.translate(cx, cy); ctx.scale(k, k); ctx.globalAlpha = .5 * par; ctx.filter = 'blur(8px)'; S1.yolYazi(ctx, 'BANA SAHİP OLURSU', [[-720, 0], [900, -10]], 1, { px: 80, col: '#FF8A5A' }); ctx.restore(); }
    // son harf: düşer, su yüzünde yansır
    const lx = lerp(cx + (-720 + dEnd + 26) * k, 1720, dus), ly = lerp(cy + 28 * k, wy - 22, dus);
    ctx.save(); ctx.font = FONT.baslik(Math.round(80 * lerp(k, .3, dus)), 700); ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic'; ctx.fillStyle = '#E8583A'; ctx.fillText('N', lx, ly);
    if (dus >= 1) { ctx.save(); ctx.beginPath(); pool(ctx); ctx.clip(); ctx.translate(0, 2 * wy + 8); ctx.scale(1, -1); ctx.globalAlpha = .5 * ramp(t, tD + .7, tD + 1.2, E.io2); ctx.fillText('N', lx, ly + 8); ctx.restore(); }
    ctx.restore();
    // ön plan gövdeler (paralaks)
    const pr = (t - st.at) * 40; baseT(ctx); govde(ctx, 60 - u * 520 - pr, 150); govde(ctx, 1880 - u * 300 - pr * .7, 110);
  });

  // ---- P034 · geniş · C12@haklı: ormanın üstünde bulutlu gök; 'tanrıçası'nda bulutlar aralanır, tek ince ışık şeridi; 'kabul'de şerit ormandaki pınara iner. Tanrıça figürü yok ----
  plan('P034', (ctx, st) => {
    const t = st.t, tT = PE('P034', 0), tK = PE('P034', 1);
    baseT(ctx); glaze(ctx, 960, 200, 1200, 'rgba(90,40,20,.35)');
    camAt(ctx, 960, lerp(380, 640, ramp(t, st.at, st.end, E.io2)), 1.0);
    const ac = ramp(t, tT - .2, tT + 1.2, E.io2);
    // ışık huzmesi (Fable tur 1: "asılı çubuk" okunuyordu): bulut aralığından aşağı GENİŞLEYEN tek huzme, yumuşak kenarlı; 'kabul'de ucu pınara kadar iner.
    // Bulutların ardında başlar (üst ucu bulut aralığında görünür). Tek huzme: haç, ışın yelpazesi, hale yok.
    const L = ramp(t, tT + .1, tT + 1.0, E.out2), dn = ramp(t, tK - .1, tK + 1.2, E.io2);
    if (L > 0) { const yT = 150, y1 = lerp(420, 960, dn), wT = 34, wB = lerp(90, 250, dn), xc = 960 + 6 * Math.sin(t * .4);
      ctx.save(); ctx.globalCompositeOperation = 'screen';
      const gv = ctx.createLinearGradient(0, yT, 0, y1); gv.addColorStop(0, 'rgba(255,226,170,1)'); gv.addColorStop(.75, 'rgba(255,214,150,.75)'); gv.addColorStop(1, 'rgba(255,200,140,0)');
      for (let k = 0; k < 12; k++) { const e = 1 + k * .11; // iç içe yamuklar: kenara doğru söner
        ctx.globalAlpha = L * .075; ctx.fillStyle = gv; ctx.beginPath();
        ctx.moveTo(xc - wT * e / 2, yT); ctx.lineTo(xc + wT * e / 2, yT); ctx.lineTo(xc + wB * e / 2, y1); ctx.lineTo(xc - wB * e / 2, y1); ctx.closePath(); ctx.fill(); }
      motesN(ctx, t, 18, 7, xc, (yT + y1) / 2, wB * .35, (y1 - yT) * .45, .5 * L); // huzmede süzülen toz
      ctx.restore(); }
    for (const [x, y, sc, sd, d] of [[500, 160, 2.4, 1, -1], [960, 120, 2.8, 2, 1], [1450, 170, 2.5, 3, 1], [200, 300, 2.0, 4, -1], [1750, 300, 2.1, 5, 1], [760, 330, 1.9, 6, -1], [1180, 320, 2.0, 7, 1]])
      cloud(ctx, x + d * (220 + 60 * hash(sd)) * ac + 14 * Math.sin(t * .3 + sd), y, sc, '#3A1C10', 'rgba(201,112,63,.4)', sd);
    // orman üstü (ağaç tepeleri) ve aradaki pınar
    groundBand(ctx, 950, -1000, 4000, { h: 800, fill: '#3A1B0D' });
    for (let i = 0; i < 12; i++) { const x = -150 + i * 200; if (Math.abs(x - 960) < 140) continue; vaseTree(ctx, x, 960, 1.15 + .2 * hash(i), 50 + i, t, { branches: 6, reach: 80 }); }
    const pg = ramp(t, tK + .7, tK + 1.5, E.io2);
    ctx.save(); ctx.beginPath(); ctx.ellipse(960, 950, 110, 14, 0, 0, TAU); ctx.fillStyle = '#050302'; ctx.fill(); ctx.lineWidth = 2.5; ctx.strokeStyle = PC.clayR; ctx.stroke();
    if (pg > 0) { ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgba(255,220,160,${(.5 * pg).toFixed(3)})`; ctx.fill(); }
    ctx.restore();
  });
})();
