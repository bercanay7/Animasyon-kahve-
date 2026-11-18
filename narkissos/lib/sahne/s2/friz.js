// FRIZ seti, SAHİP-2: P097. Bu dosyayı yalnız bu sahip değiştirir.
// Vazo frizi: Sisifos taşı yokuşa iter (kanalın Sisifos videosunun silueti, aynı vazo dili). s2_sisifosFriz SON setinde (P098) de kullanılır.
'use strict';
// friz: (x, y) sol üst, w×h; u 0..1 taşın yokuştaki yeri (1 tepe); off: frizin dönmesi (bant kayması)
function s2_sisifosFriz(ctx, t, x, y, w, h, u, o = {}) {
  ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
  ctx.fillStyle = '#C9703F'; ctx.fillRect(x, y, w, h);
  const off = o.off || 0;
  ctx.save(); ctx.translate(-((off % 80) + 80) % 80, 0); meander(ctx, x - 80, x + w + 160, y + 4, h * .1, C.ink, null); tongues(ctx, x - 80, x + w + 160, y + h - h * .1, h * .1, C.ink); ctx.restore();
  const k = h / 400, gx0 = x + w * .08, gy0 = y + h * .82, gx1 = x + w * .9, gy1 = y + h * .32;
  const slope = c => { c.beginPath(); c.moveTo(gx0 - 40, gy0 + 10); c.lineTo(gx1, gy1); c.lineTo(gx1 + 200, gy1); c.lineTo(gx1 + 200, y + h); c.lineTo(gx0 - 40, y + h); c.closePath(); };
  ctx.fillStyle = C.ink; slope(ctx); ctx.fill();
  const ang = Math.atan2(gy1 - gy0, gx1 - gx0), P = q => [lerp(gx0, gx1, q), lerp(gy0, gy1, q)];
  const R = 46 * k, rq = clamp(u) * .9 + .02, rc = P(rq), rN = [Math.sin(ang), -Math.cos(ang)];
  const rock = add(rc, scl(rN, R));
  // Sisifos: siyah figür, kollar ileri, gövde yokuşa eğik (taşın arkasında)
  const man = add(P(Math.max(0, rq - .11)), [0, 0]), s = 2.35 * k;
  const pushing = o.pushing ?? 1;
  walkScene(ctx, null, man[0], s, t, 1, { ground: groundOf(xx => lerp(gy0, gy1, (xx - gx0) / (gx1 - gx0))), noCam: true, sty: STY.black, lk: { beard: 'pointed', hair: 'long', garment: 'short' },
    dist: (man[0] - gx0) * 1.1, stand: 1 - pushing, lean: .35 * pushing + .05, neck: .1, head: .1, stride: 26, p: { shN: -1.25 * pushing, elN: .25, shF: -1.1 * pushing, elF: .3, handN: 'open', handF: 'open' } });
  ctx.save(); ctx.translate(...rock); ctx.rotate(u * 9); ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(0, 0, R, 0, TAU); ctx.fill(); ctx.strokeStyle = '#C9703F'; ctx.lineWidth = 2.2 * k; ctx.beginPath(); ctx.arc(0, 0, R * .55, .3, 2.2); ctx.stroke(); ctx.beginPath(); ctx.moveTo(-R * .3, R * .5); ctx.lineTo(R * .2, R * .2); ctx.stroke(); ctx.restore();
  ctx.restore();
  ctx.save(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.strokeRect(x, y, w, h); ctx.restore();
}
(() => {
  // P097 · orta · F12@sisifosa · Frizde Sisifos taşı yokuşa iter; taş tepeye yaklaşır; friz küçülerek sol alta (bitiş ekranındaki yerine) kayar; zemin kararır
  plan('P097', (ctx, st) => {
    const t = st.t, tY = PE('P097', 0), tM = PE('P097', 1), tH = PE('P097', 2);
    const sh = ramp(t, tM - .1, tH, E.io2);
    baseT(ctx); glaze(ctx, 960, 600, 1100, `rgba(110,44,20,${(.4 * (1 - sh)).toFixed(3)})`);
    const F0 = [160, 250, 1600, 560], F1 = S2_SON.friz, F = F0.map((v, i) => lerp(v, F1[i], sh));
    const u = lerp(.55, .86, ramp(t, st.at, tY + .6, E.io2)) + .04 * ramp(t, tY + .6, st.end, E.lin);
    s2_sisifosFriz(ctx, t, F[0], F[1], F[2], F[3], u, { off: (t - st.at) * 30 * (1 - sh) });
    meander(ctx, -400, 2400, 0, 36 * (1 - sh), PC.clayR, PC.glaze);
  });
})();
