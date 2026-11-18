// SON seti, SAHİP-2: P098. Bu dosyayı yalnız bu sahip değiştirir.
// Bitiş ekranı (son 20 sn): siyah sır zemin; solda küçük Sisifos frizi ağır ağır döner, altta ince meander bandı; orta-sağ ve üst YouTube öğelerine boş.
// Yerleşim (S2_SON): video kutusu 860–1760 × 150–656 (16:9), abone düğmesi merkezi (1310, 790) r 78. Yazı ve figür bu alanlara girmez; ekran yazısı yok.
'use strict';
const S2_SON = { friz: [110, 560, 620, 240], vid: [860, 150, 1760, 656], abone: [1310, 790, 78] };
(() => {
  // P098 · geniş · F12@ekranda-0.22 · Bitiş ekranı: kırmızı nokta video kutusunun altına koşar, arkasında meander bandı bırakır, abone düğmesinin altında nabız atar; friz döner (taş tepeye, sonra geri)
  plan('P098', (ctx, st) => {
    const t = st.t, tE = PE('P098', 0), tG = PE('P098', 1), tD = PE('P098', 2), tA = PE('P098', 3), tT = PE('P098', 4), tR = PE('P098', 5);
    baseT(ctx); ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
    const g = ctx.createRadialGradient(420, 700, 0, 420, 700, 700); g.addColorStop(0, 'rgba(110,44,20,.28)'); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    const [fx, fy, fw, fh] = S2_SON.friz, [vx0, vy0, vx1, vy1] = S2_SON.vid, [ax, ay, ar] = S2_SON.abone;
    // friz: taş tepeye ulaşır (ol+4), sonra geri yuvarlanır (ol+8.5) — sessiz döngü
    const up = .9 + .1 * ramp(t, st.at, tT, E.io2), down = ramp(t, tR, tR + 3.5, E.in2);
    const u = up * (1 - down) + .08 * down;
    s2_sisifosFriz(ctx, t, fx, fy, fw, fh, u, { off: (t - st.at) * 6, pushing: 1 - down });
    // nokta ve meander bandı: frizin altından video kutusunun altına, soldan sağa, sonra abone düğmesinin altına
    const yb = vy1 + 26, P0 = [fx + fw * .5, fy + fh + 18], P1 = [vx0, yb], P2 = [vx1 + 30, yb], P3 = [ax, ay + ar + 26];
    const a1 = ramp(t, tE - .1, tE + .8, E.io2), a2 = ramp(t, tG - .1, tD + .2, E.io2), a3 = ramp(t, tD + .2, tA, E.io2);
    let dot = P0;
    if (a1 < 1) dot = [lerp(P0[0], P1[0], a1), lerp(P0[1], P1[1], a1) - Math.sin(PI * a1) * 60];
    else if (a2 < 1) dot = lerp2(P1, P2, a2);
    else dot = [lerp(P2[0], P3[0] + 120, a3), lerp(P2[1], P3[1], a3)];
    const bandEnd = a1 < 1 ? vx0 : a2 < 1 ? dot[0] : vx1 + 30;
    if (a1 >= 1) { ctx.save(); ctx.beginPath(); ctx.rect(vx0, yb - 20, bandEnd - vx0, 40); ctx.clip(); meander(ctx, vx0, vx1 + 30, yb - 12, 24, PC.clayR, null); ctx.restore(); }
    meander(ctx, -400, 2400, H - 150, 22, 'rgba(201,112,63,.6)', null);
    const pulse = settle(t, tA + .1, .5, 2.2, 3);
    if (a1 > 0) { ctx.save(); ctx.fillStyle = '#C2412A'; ctx.beginPath(); ctx.arc(dot[0], dot[1], 11 * (1 + Math.max(0, pulse)), 0, TAU); ctx.fill(); ctx.restore(); }
  }, { post: { tex: .4, vig: .7 } });
})();
