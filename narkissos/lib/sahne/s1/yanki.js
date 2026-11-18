// YANKI seti, SAHİP-1: P018, P019. Bu dosyayı yalnız bu sahip değiştirir.
// Soyut vazo yüzeyi: siyah sır zemin, kırmızı figür Eko ve dipinto yazılar. Juno figürle çizilmez: yalnız tavus kuşu kuyruğu ve sıcak ışık (gözler damla biçimli tüy gözü, 'nazar' değil).
'use strict';
(() => {
  const S1 = window.S1;
  const zemin = (ctx, gx = 960) => { glaze(ctx, gx, 900, 1300, 'rgba(110,46,22,.35)'); };
  // tavus kuşu kuyruğu (yelpaze): merkez (cx, cy), açılma u (0..1), ışık a
  const tavus = (ctx, cx, cy, u, t, a = 1) => {
    const n = 15, L = 560;
    ctx.save(); ctx.globalAlpha *= a; ctx.lineCap = 'round';
    for (let i = 0; i < n; i++) {
      const an = lerp(-PI * .62, lerp(-PI * .62, -PI * 1.02 + i * PI * .5 / (n - 1) + PI * .02, 1), u) + (u < 1 ? 0 : 0) + .02 * Math.sin(t * 1.3 + i);
      const fa = lerp(-PI * .62, -PI * 1.0 + i * (PI * .52) / (n - 1), u) + .015 * Math.sin(t * 1.3 + i);
      const ex = cx + Math.cos(fa) * L, ey = cy + Math.sin(fa) * L;
      ctx.strokeStyle = C.ink; ctx.lineWidth = 7; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(ex, ey); ctx.stroke();
      ctx.strokeStyle = PC.clayR; ctx.lineWidth = 3; ctx.stroke();
      // tüy saçakları
      ctx.strokeStyle = 'rgba(201,112,63,.55)'; ctx.lineWidth = 1.6;
      for (let k = 3; k < 12; k++) { const q = k / 12, px = cx + Math.cos(fa) * L * q, py = cy + Math.sin(fa) * L * q, w = 14 + 26 * q;
        ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px + Math.cos(fa - .9) * w, py + Math.sin(fa - .9) * w); ctx.moveTo(px, py); ctx.lineTo(px + Math.cos(fa + .9) * w, py + Math.sin(fa + .9) * w); ctx.stroke(); }
      // tüy gözü: uzun damla (kil dış, kırmızı halka, koyu iç)
      ctx.save(); ctx.translate(ex, ey); ctx.rotate(fa + PI / 2);
      const dm = (w, h) => { ctx.beginPath(); ctx.moveTo(0, -h); ctx.bezierCurveTo(w, -h * .5, w, h * .6, 0, h); ctx.bezierCurveTo(-w, h * .6, -w, -h * .5, 0, -h); };
      dm(30, 44); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 2.5; ctx.stroke();
      dm(19, 30); ctx.fillStyle = C.red; ctx.fill(); dm(10, 17); ctx.fillStyle = '#1A0E08'; ctx.fill();
      ctx.restore();
    }
    ctx.restore();
  };
  const SOZ = 'VE SONRA · DAHA DA · BİR DE · SONRA DA · VE O ZAMAN · DAHA DA · BİR DE · ';

  // ---- P018 · geniş · C02: geçmiş; Eko konuşur, ağzından uzun kıvrılan bir dipinto şeridi akar; 'junoyu'da sağdan tavus kuşu kuyruğu ve sıcak ışık;
  //      'kandırdığı'da şerit tüy gözleri arasında dolanır; 'cezalandırıldı'da ışık kesilir, şerit kopar, harfler yere dökülür ----
  plan('P018', (ctx, st) => {
    const t = st.t, tK = PE('P018', 0), tJ = PE('P018', 1), tD = PE('P018', 2), tC = PE('P018', 3), gy = 900;
    baseT(ctx); zemin(ctx);
    const isik = ramp(t, tJ - .1, tJ + .8, E.io2) * (1 - ramp(t, tC, tC + .25, E.lin));
    if (isik > .01) glow(ctx, 1500, 520, 900, `rgba(255,190,120,${(.28 * isik).toFixed(3)})`);
    camAt(ctx, lerp(900, 1060, E.sine(st.p)), 540, 1.0);
    meander(ctx, -800, 3000, 70, 40, PC.clayR, PC.glaze); ctx.save(); ctx.fillStyle = PC.clayR; ctx.fillRect(-800, gy, 3800, 5); ctx.restore();
    const ac = ramp(t, tJ - .1, tJ + .9, E.out3);
    if (ac > 0) tavus(ctx, 1820, gy - 10, ac, t, .55 + .45 * Math.max(isik, .35) * (1 - .5 * ramp(t, tC, tC + .4, E.lin)));
    const konus = t > st.at && t < tC + .2 ? .5 + .5 * Math.sin(t * 15) : 0;
    const r = (() => { let J = null, M = null; figure(ctx, { x: 380, y: gy - 44.5 * 8, s: 8, dir: 1, sty: S1.RFF, lk: S1.LK_EKO, seed: 71, stripe: .45, p: { shN: .5, elN: .9, handN: 'open', head: -.05, smile: .3 }, onJoints: (j, m) => { J = j; M = m; } }); return { J, M }; })();
    const m = headPt(ctx, r.J, r.M, [6.3, -3.9]);
    if (konus > .05) { ctx.save(); ctx.fillStyle = '#2A140A'; ctx.beginPath(); ctx.ellipse(m[0] - 6, m[1], 5, 4 * konus, 0, 0, TAU); ctx.fill(); ctx.restore(); }
    // şerit: uzar, kıvrılır; 'kandırdığı'da tüylerin arasına dolanır
    const sar = ramp(t, tD - .2, tD + .9, E.io2);
    const P = S1.konusmaYolu(m[0] + 30, m[1] - 10, -.18, lerp(1100, 1500, sar), t, { amp: lerp(26, 60, sar), k: lerp(.012, .02, sar), curl: lerp(.4, 1.2, sar) });
    const p = ramp(t, st.at, tD + .6, E.lin);
    const tc = Math.max(0, t - tC);
    S1.yolYazi(ctx, SOZ, P, p, { px: 34, col: S1.KIL,
      off: tc > 0 ? (i => [0, 900 * tc * tc * (.6 + .8 * hash(i * 1.7)) + 20 * tc]) : null, rot: tc > 0 ? (i => tc * 3 * (hash(i) - .5)) : null, fade: tc > 0 ? (i => 1 - clamp((tc - .4 - hash(i) * .3) / .5)) : null });
  });

  // ---- P019 · yakın · C02@günden-0.65: Eko'nun profili yakın; başka bir ağızdan gelen yazı ona akar; 'son'da yalnız son kelime kırmızı yanar; 'verebilir'de Eko onu geri verir, solarak uzaklaşır ----
  plan('P019', (ctx, st) => {
    const t = st.t, tS = PE('P019', 0), tV = PE('P019', 1), s = 22;
    baseT(ctx); zemin(ctx, 1300);
    camAt(ctx, lerp(1000, 940, ramp(t, st.at, st.end, E.io2)), 540, 1.0);
    S1.ustBant(ctx);
    let J = null, M = null;
    figure(ctx, { x: 1420, y: 430 + 37 * s, s, dir: -1, sty: S1.RFF, lk: S1.LK_EKO, seed: 71, stripe: .45, idle: .5, p: { neck: .05, head: .02 }, onJoints: (j, m) => { J = j; M = m; } });
    const m = headPt(ctx, J, M, [6.4, -3.9]);
    const ag = Math.max(0, Math.sin((t - tV) * PI / .5)) * (t > tV && t < tV + 1 ? 1 : 0);
    if (ag > .03) { ctx.save(); ctx.fillStyle = '#2A140A'; ctx.beginPath(); ctx.ellipse(m[0] + 6, m[1] + 2, 9, 7 * ag, 0, 0, TAU); ctx.fill(); ctx.restore(); }
    // gelen yazı: soldan akar, ağzın önünde durur
    const gel = ramp(t, st.at - .3, tS - .2, E.out2), x1 = lerp(-1200, m[0] - 1000, gel), y = m[1] - 40;
    const fd = 1 - ramp(t, tV + .4, tV + 1.2, E.io2);
    const d = S1.yolYazi(ctx, 'BİRİ BENİ ', [[x1, y], [x1 + 2000, y]], 1, { px: 58, col: S1.KIL, a: fd });
    const yan = ramp(t, tS - .05, tS + .3, E.out3);
    ctx.save(); if (yan > 0) { ctx.shadowColor = 'rgba(255,110,70,.6)'; ctx.shadowBlur = 24 * yan; }
    S1.yolYazi(ctx, 'DUYSUN', [[x1 + d, y], [x1 + d + 1200, y]], 1, { px: 58, col: mixCol(S1.KIL, '#F06A44', yan), a: 1 - ramp(t, tV, tV + .4, E.io2) });
    ctx.restore();
    if (t > tV) S1.yanki(ctx, 'DUYSUN', m[0] - 260, m[1] + 70, t, tV, { dx: -1, px: 62, dt: .45, col: '#E8583A', reps: ['DUYSUN', 'duysun', 'sun'], life: 2.4 });
  });
})();
