// Kanat ilkelleri: tüylü melek kanadı ve (düşüşten sonrası için) yarasa kanadı.
// Yerel koordinat: omuz (0,0), kanat +x yönüne açılır, y aşağı. Kanat yukarı kalkıkken ön kenar üstte, tüyler aşağı sarkar.
// Dış dönüşüm (konum, açı, ayna) GR.frame ile verilir.
'use strict';
const KN = (() => {
  const { tx, px, tone, pat, fill } = GR;
  // tek tüy: taban (bx,by), doğrultu a, uzunluk L, genişlik w, kavis k (+ arka kenara doğru)
  // v0 taban tonu, v1 uç tonu; kenarlar ton katmanında: alt kenar gölge, üst kenar ışık
  function feather(bx, by, a, L, w, k, v0, v1, o = {}) {
    const c = Math.cos(a), s = Math.sin(a), nx = -s, ny = c;
    // omurga: hafif kavisli; uç yuvarlak
    const sp = f => [bx + c * L * f + nx * k * L * Math.sin(f * PI) * .5 + nx * k * L * f * .4, by + s * L * f + ny * k * L * Math.sin(f * PI) * .5 + ny * k * L * f * .4];
    const wd = f => w * (f < .1 ? .35 + f * 6.5 : f < .78 ? 1 : Math.sqrt(Math.max(0, 1 - Math.pow((f - .78) / .22, 2))));
    const Lp = [], Rp = [], n = 10;
    for (let i = 0; i <= n; i++) {
      const f = i / n, [x, y] = sp(f), ww = wd(f) * .5;
      const [x2, y2] = sp(Math.min(1, f + .01)), ta = Math.atan2(y2 - y, x2 - x) + PI / 2;
      Lp.push([x - Math.cos(ta) * ww * 1.1, y - Math.sin(ta) * ww * 1.1]); Rp.push([x + Math.cos(ta) * ww * .9, y + Math.sin(ta) * ww * .9]);
    }
    const P = new Path2D(); spline(P, [...Lp, ...Rp.reverse()], true, .9);
    const [tipx, tipy] = sp(1), [mx, my] = sp(.5);
    const g = tx.createLinearGradient(bx, by, tipx, tipy);
    g.addColorStop(0, tone(v0)); g.addColorStop(.5, tone(lerp(v0, v1, .85))); g.addColorStop(1, tone(v1));
    const th = Math.atan2(tipy - by, tipx - bx);
    fill(P, g, { fill: GR.patGrad(bx, by, tipx, tipy, [[0, th + k * 1.4], [1, th - k * 1.4]], o.ph || 0, o.id ?? 6) });
    // ışık ve gölge kenarları: tüyleri ayıran ton farkı
    tx.save(); tx.clip(P); tx.lineCap = 'round'; tx.lineJoin = 'round';
    tx.strokeStyle = tone(o.shade ?? .06, .8); tx.lineWidth = Math.max(1.5, w * .2);
    tx.beginPath(); poly(tx, Rp, false); tx.stroke();
    if (o.rim) { tx.strokeStyle = tone(1, o.rim); tx.lineWidth = Math.max(1.3, w * .14); tx.beginPath(); poly(tx, Lp.slice(1, -1), false); tx.stroke(); }
    tx.strokeStyle = tone(Math.min(1, v1 + .2), .5); tx.lineWidth = Math.max(.8, w * .045);
    tx.beginPath(); poly(tx, [0, .2, .4, .6, .8, .95].map(sp), false); tx.stroke();
    tx.restore();
    return P;
  }
  // Tüylü kanat. o: {span, open (0..1: 1 açık, 0 katlı), lift (radyan, kalkış), flap (çırpış), t, dark (0..1 yanık), rim (kenar ışığı), seed}
  function feathered(o) {
    const S = o.span, op = o.open ?? 1, r = rng(o.seed || 1), t = o.t || 0;
    const lift = (o.lift ?? .5) + (o.flap || 0), dark = o.dark ?? 0, rim = o.rim ?? 0;
    // kemikler: omuz → dirsek (yukarı) → bilek (kanadın tepesi) → uç (dışa, aşağı)
    // lift 0: yatay açılmış (uçuş), lift 1: dikine kalkık (melek kanadı). op 0: katlı, sırta yapışık
    const aE = lerp(-1.25, lerp(-.9, -1.5, lift), op);
    const aW = lerp(-1.45, lerp(-.35, -1.0, lift), op);
    const aT = lerp(-1.3, lerp(.05, -1.2, lift), op);
    const E = [S * .24 * Math.cos(aE), S * .24 * Math.sin(aE)];
    const Wr = [E[0] + S * .30 * Math.cos(aW), E[1] + S * .30 * Math.sin(aW)];
    const Tp = [Wr[0] + S * .2 * Math.cos(aT), Wr[1] + S * .2 * Math.sin(aT)];
    const bone = u => u < .3 ? [lerp(0, E[0], u / .3), lerp(0, E[1], u / .3), aE]
      : u < .72 ? [lerp(E[0], Wr[0], (u - .3) / .42), lerp(E[1], Wr[1], (u - .3) / .42), aW]
        : [lerp(Wr[0], Tp[0], (u - .72) / .28), lerp(Wr[1], Tp[1], (u - .72) / .28), aT];
    const vD = lerp(.42, .1, dark), vL = lerp(.96, .5, dark);
    const paths = [];
    // 0) zar: tüylerin arkasında kalan gölgeli gövde (boşluk görünmesin)
    const back = new Path2D();
    const tipF = [Tp[0] + S * .5 * Math.cos(aT + .5 * op + .9 * (1 - op)), Tp[1] + S * .5 * Math.sin(aT + .5 * op + .9 * (1 - op))];
    back.moveTo(0, 0); back.lineTo(E[0], E[1]); back.lineTo(Wr[0], Wr[1]); back.lineTo(Tp[0], Tp[1]); back.lineTo(tipF[0], tipF[1]);
    back.quadraticCurveTo(S * .45, S * .55, S * .02, S * .6 * op + S * .3); back.closePath();
    // 1) uçuş tüyleri: uçtan omuza (dıştakiler arkada kalır)
    const N = 30;
    for (let i = 0; i < N; i++) {
      const u = 1 - i / (N - 1) * .95;
      const [bx, by, ba] = bone(u);
      const isP = u > .72, q = isP ? (u - .72) / .28 : (u - .05) / .67;
      const rel = isP ? lerp(lerp(1.4, 1.1, lift), .15, Math.pow(q, .85)) : lerp(lerp(1.75, 2.35, lift), lerp(1.5, 1.55, lift), q);
      const a = ba + rel * lerp(.35, 1, op) + (1 - op) * 2.6 + Math.sin(t * 1.2 + i * .6) * .012 * op;
      const L = S * (isP ? lerp(.5, .42, Math.pow(q, 2.2)) : lerp(.36, .5, q)) * (.95 + r() * .1);
      const w = S * (isP ? .085 : .095);
      const v1 = lerp(vL, vD, .15 + .35 * r() * (1 - u)), v0 = lerp(vD, vL, .15);
      paths.push(feather(bx, by, a, L, w, (isP ? .06 : .035) + r() * .02, v0, v1, { ph: r(), rim: rim * (isP ? 1 : .7) }));
    }
    // 2) örtü tüyleri: üç sıra; büyükler arkada
    for (let row = 2; row >= 0; row--) {
      const n = 18 - row * 4;
      for (let i = 0; i < n; i++) {
        const u = .03 + (1 - i / (n - 1)) * (.76 - row * .05);
        const [bx, by, ba] = bone(u);
        const a = ba + lerp(.9, lerp(1.55, 1.9, lift), op) + (1 - op) * 2.6 + .1;
        const L = S * (.16 - row * .04) * (.9 + r() * .2);
        paths.push(feather(bx, by, a, L, S * (.085 - row * .015), .07, lerp(vD, vL, .3 + row * .12), lerp(vL, vD, .1 + row * .08), { ph: r(), rim: rim * .9, shade: .14 }));
      }
    }
    // 3) ön kenar: kemik üstündeki kas ve ince tüy kütlesi
    const LE = new Path2D();
    LE.moveTo(-S * .04, S * .06);
    LE.quadraticCurveTo(-S * .04, E[1] * .4 - S * .02, E[0] - S * .03, E[1] - S * .02);
    LE.quadraticCurveTo(lerp(E[0], Wr[0], .5), lerp(E[1], Wr[1], .5) - S * .05, Wr[0] + S * .02, Wr[1] - S * .015);
    LE.quadraticCurveTo(Wr[0] + S * .05, Wr[1] + S * .03, Wr[0] - S * .01, Wr[1] + S * .045);
    LE.quadraticCurveTo(E[0] + S * .04, E[1] + S * .07, S * .05, S * .1); LE.closePath();
    const g = tx.createLinearGradient(E[0] - S * .05, E[1] - S * .05, E[0] + S * .05, E[1] + S * .06);
    g.addColorStop(0, tone(Math.min(1, vL + .03))); g.addColorStop(1, tone(lerp(vD, vL, .3)));
    fill(LE, g, { th: aW + PI / 2, id: 6 });
    paths.push(LE);
    return { paths, E, Wr, Tp, bone, back };
  }
  return { feather, feathered };
})();
