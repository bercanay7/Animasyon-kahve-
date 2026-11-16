// 1910'lar Prag figürleri (ağaç baskı siluet). Her şey Path2D (nonzero) döner; basımı KS.siluet yapar (hale + kenar ışığı).
// Yüz yakın planı yok, gerçekçi portre yok (Kafka ve babası dönem silueti). Böcek hiç çizilmez.
// insan(o): o = {x, y (ayak tabanı), h (boy), f (1 sağa, -1 sola), tip, egil (öne eğilme, rad), bas (baş eğimi), kolN, kolF: [omuz, dirsek] (aşağıdan açı; + yüz yönü),
//   otur (oturuyor), adim (bacak açıklığı), kep, melon, sapka:false}
// tip: 'baba' (gür bıyık, geniş), 'anne' (topuz, uzun etek), 'grete' (kurdeleli saç, uzun etek), 'mudur' (melon şapka, uzun palto),
//      'kiraci' (gür sakal), 'gregor' (genç, takım), 'kafka' (ince, koyu takım, melon), 'bugun' (bugünün adamı: kapüşonlu)
'use strict';
const IN = (() => {
  const add = (a, b, k = 1) => [a[0] + b[0] * k, a[1] + b[1] * k];
  const cap = FG.capsule, poly = FG.polyInto, ell = FG.ellipseInto;
  function insan(o) {
    const h = o.h, u = h / 7.5, f = o.f || 1, eg = o.egil || 0, tip = o.tip || 'gregor';
    const kadin = tip === 'anne' || tip === 'grete';
    const p = new Path2D(), kp = new Path2D();
    const up = [Math.sin(eg) * f, -Math.cos(eg)], fw = [Math.cos(eg) * f, Math.sin(eg)];
    const otur = !!o.otur;
    const kal = otur ? [o.x, o.y - 2.25 * u] : [o.x, o.y - 3.75 * u];
    const omuz = add(kal, up, 2.75 * u), boyun = add(omuz, up, .32 * u);
    const bt = eg + (o.bas || 0), basM = add(boyun, [Math.sin(bt) * f, -Math.cos(bt)], .52 * u), r = .5 * u;
    const genis = tip === 'baba' ? 1.12 : tip === 'kafka' ? .88 : kadin ? .86 : 1;
    // ── bacaklar ──
    const ayakL = (k, sx) => { const ay = add(k, [f * .32 * u, 0]); cap(p, k, ay, .17 * u, .13 * u); };
    if (otur) {
      const diz = add(kal, [f * 1.9 * u, -.05 * u]); const ayak = [diz[0] + f * .15 * u, o.y - .1 * u];
      if (!kadin) { cap(p, kal, diz, .36 * u, .28 * u); cap(p, diz, ayak, .27 * u, .2 * u); ayakL(ayak); }
      else { poly(p, [add(kal, [-f * .7 * u, -.6 * u]), add(diz, [f * .25 * u, -.35 * u]), add(diz, [f * .45 * u, o.y - diz[1] - .05 * u]), [kal[0] - f * .8 * u, o.y - .05 * u]]); }
    } else if (!kadin) {
      const ad = (o.adim ?? .12) * u;
      for (const s of [-1, 1]) { const kk = add(kal, [s * .32 * u * genis, 0]), ay = [kal[0] + s * (.34 * u + ad) + f * .0, o.y - .12 * u]; cap(p, kk, ay, .33 * u * genis, .2 * u); ayakL(ay); }
    }
    // ── gövde / giysi ── (omuz eğimli, bel dar, etek ya da palto hafif açılır)
    const om = .9 * u * genis, bel = .55 * u * genis;
    const L = (pt, a, b) => add(add(pt, fw, a), up, b);                           // yerel: fw ileri, up yukarı
    if (kadin) {
      const hem = tip === 'anne' ? 1.25 : 1.05;
      poly(p, [L(omuz, -om * .55, .18 * u), L(omuz, om * .6, .16 * u), L(omuz, om * 1.0, -.12 * u), L(omuz, om * .95, -.7 * u), L(kal, bel + .05 * u, .75 * u), L(kal, bel * .9, .55 * u), L(kal, -bel * .9, .55 * u), L(kal, -bel - .05 * u, .75 * u), L(omuz, -om * .9, -.7 * u), L(omuz, -om * .95, -.12 * u)]);
      if (!otur) poly(p, [L(kal, -bel * .95, .62 * u), L(kal, bel * 1.0, .62 * u), L(kal, bel * 1.25, -.4 * u), [o.x + f * hem * u, o.y], [o.x + f * hem * u * .3, o.y + .04 * u], [o.x - f * hem * u * .9, o.y], L(kal, -bel * 1.25, -.4 * u)]);
      else poly(p, [L(kal, -bel, .7 * u), L(kal, bel + .2 * u, .7 * u), add(kal, [f * 1.3 * u, .1 * u]), add(kal, [-f * 1.0 * u, .3 * u])]);
    } else {
      const ceket = (tip === 'baba' || tip === 'mudur' || tip === 'kiraci') ? 1.7 : tip === 'bugun' ? .35 : .85;
      const ac = (tip === 'baba' || tip === 'mudur') ? .2 : .1;
      poly(p, [L(omuz, -om * .55, .2 * u), L(omuz, om * .6, .18 * u), L(omuz, om * 1.02, -.1 * u), L(omuz, om * .9, -.8 * u), L(kal, bel + .1 * u, .6 * u), L(kal, bel + (ac + .1) * u, -ceket * u * .5), L(kal, bel + (ac + .2) * u, -ceket * u),
        L(kal, -bel - (ac + .2) * u, -ceket * u), L(kal, -bel - (ac + .1) * u, -ceket * u * .5), L(kal, -bel - .1 * u, .6 * u), L(omuz, -om * .9, -.8 * u), L(omuz, -om * .98, -.1 * u)]);
      if (tip === 'baba' && o.kep) poly(p, [L(omuz, -om * 1.05, .05 * u), L(omuz, om * 1.1, .05 * u), L(omuz, om * 1.0, -.22 * u), L(omuz, -om * .98, -.22 * u)]);   // apolet
    }
    // ── kollar ──
    const kol = (ang, yan) => {
      const s0 = L(omuz, yan * om * 1.0, -.25 * u);
      const a1 = (ang ? ang[0] : .1 * Math.sign(yan)) - eg, a2 = a1 + (ang ? ang[1] : -.08 * Math.sign(yan));
      const dir = a => [Math.sin(a) * f, Math.cos(a)];
      const dz = add(s0, dir(a1), 1.45 * u), el = add(dz, dir(a2), 1.35 * u);
      cap(kp, s0, dz, .22 * u * genis, .19 * u); cap(kp, dz, el, .19 * u, .14 * u); ell(kp, el[0], el[1], .15 * u, .13 * u, a2, 12);
      return el;
    };
    const elF = kol(o.kolF, -.6), elN = kol(o.kolN, .7);
    // ── baş ──
    ell(p, basM[0], basM[1], r * .95, r * 1.05, bt);
    cap(p, boyun, add(basM, [0, .25 * u]), .24 * u, .22 * u);
    const T = (x, y) => [basM[0] + (x * Math.cos(bt) - y * Math.sin(bt)) * f, basM[1] + (x * Math.sin(bt) + y * Math.cos(bt))];
    poly(p, [T(.6 * r, -.5 * r), T(.98 * r, -.1 * r), T(1.2 * r, .2 * r), T(.98 * r, .32 * r), T(.94 * r, .62 * r), T(.7 * r, .95 * r), T(.2 * r, .9 * r)]);   // yüz profili, burun
    if (tip === 'baba') poly(p, [T(.75 * r, .38 * r), T(1.18 * r, .5 * r), T(1.05 * r, .62 * r), T(.6 * r, .58 * r)]);                                           // gür bıyık
    if (tip === 'kiraci') poly(p, [T(.9 * r, .45 * r), T(1.0 * r, .9 * r), T(.75 * r, 1.55 * r), T(.25 * r, 1.4 * r), T(-.2 * r, .5 * r)]);                       // gür sakal
    if (tip === 'anne') { ell(p, ...T(-.85 * r, -.55 * r), r * .48, r * .42, 0, 16); }                                                                             // topuz
    if (tip === 'grete') { ell(p, ...T(-.7 * r, -.2 * r), r * .55, r * .7, 0, 16); poly(p, [T(-.9 * r, -.9 * r), T(-1.6 * r, -1.35 * r), T(-1.45 * r, -.6 * r)]); poly(p, [T(-.9 * r, -.9 * r), T(-.3 * r, -1.55 * r), T(-.55 * r, -.95 * r)]); }  // saç + kurdele
    const kep = o.kep ?? false, melon = o.melon ?? (tip === 'mudur' || tip === 'kafka');
    if (kep) { poly(p, [T(-1.0 * r, -.55 * r), T(.9 * r, -.6 * r), T(.95 * r, -1.0 * r), T(-1.05 * r, -1.05 * r)]); poly(p, [T(.6 * r, -.6 * r), T(1.55 * r, -.48 * r), T(1.5 * r, -.38 * r), T(.6 * r, -.45 * r)]); }
    if (melon) { const bp = []; for (let i = 0; i <= 10; i++) { const a = Math.PI + Math.PI * i / 10; bp.push(T(Math.cos(a) * .85 * r, -.55 * r + Math.sin(a) * .9 * r)); } poly(p, bp); poly(p, [T(-1.25 * r, -.5 * r), T(1.3 * r, -.5 * r), T(1.25 * r, -.38 * r), T(-1.2 * r, -.38 * r)]); }
    if (tip === 'bugun') { ell(p, ...T(-.25 * r, -.1 * r), r * 1.15, r * 1.25, 0, 20); }                                                                          // kapüşon
    // düğmeler (baba üniforması): oyulmuş ak noktalar için konumlar
    const dug = []; if (tip === 'baba' && kep) for (let i = 0; i < 5; i++) dug.push(L(omuz, om * .55, -(.5 + i * .55) * u));
    return { p, kp, bas: basM, elN, elF, omuz, kal, dug, u };
  }
  return { insan };
})();
