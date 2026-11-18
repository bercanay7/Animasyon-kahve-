// YAZI seti, SAHİP-2: P081. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Belge setinin yardımcıları (s2_cerceve, s2_sepNark; lib/sahne/s2/belge.js) çizim anında kullanılır.
'use strict';
(() => {
  // P081 · yakın · F03@bir#2 · LEVHA · 1899'da ona olan: sepya Narkissos'un yanında ad etiketi değişir: ΝΑΡΚΙΣΣΟΣ → Narcismus → narsisizm
  plan('P081', (ctx, st) => {
    const t = st.t, tA = PE('P081', 0), tN = PE('P081', 1);
    s2_belgeZemin(ctx, s2_cam(st, [900, 560, 1.55], [900, 560, 1.64]));
    s2_sepNark(ctx, t, 700, 640, { s: 4.2, lean: 1 });
    const gr = 1 - ramp(t, tN - .1, tN + .4, E.io2) * .65;
    dipintoYaz(ctx, 'ΝΑΡΚΙΣΣΟΣ', 900, 420, 34, 1, { col: C.sepia, a: gr });
    const w1 = ramp(t, tA - .05, tA + 1.0, E.lin), sw = ramp(t, tN - .1, tN + .25, E.io2);
    ctx.save(); ctx.font = FONT.alinti(52, 600); ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillStyle = C.sepia;
    const A1 = 'Narcismus', n = [...A1].length;
    if (sw < .5 && w1 > 0) { ctx.globalAlpha = 1 - 2 * sw; ctx.fillText([...A1].slice(0, Math.ceil(n * w1)).join(''), 760, 486); }
    if (sw > .5) { ctx.globalAlpha = 2 * sw - 1; ctx.fillStyle = '#9A3B25'; ctx.fillText('narsisizm', 760, 486); }
    ctx.restore();
  }, { post: { tex: .25, vig: .55 }, over: (ctx, st) => kunye(ctx, 'Paul Näcke · 1899', st.lt - .3, st.d) });
})();
