// Siluet figür v3: oranlı iskelet (rig) + TEK sürekli kütle.
// Parçalar (gövde, kol, bacak, baş, saç, pelerin) dört derinlik grubunda (pelerin, uzak, ana, yakın) çevrim dışı
// maske tuvallerine tek renk doldurulur; kenar ışığı, beyaz çizgiler, gölge kenarı ve mürekkep konturu parça başına
// değil GRUP MASKESİNE bir kez uygulanır: eklem yerinde iç çizgi kalmaz, yalnız gerçek örtüşme kenarları (öndeki kol
// gövdenin üstünde) ayrışır.
// Işık kenarı: maske ışık yönünde kaydırılıp çıkarılır; bant genişliği kenar normali ile ışık arasındaki açının
// kosinüsüyle değişir, teğet noktalarda sivrilerek biter. Koyu figürde bandın içinde 3 seyrek "beyaz çizgi"
// (gravürün beyaz çizgi tekniği) kenarı izler, içe doğru incelir ve ışık merkezinden uzaklaştıkça söner.
// Her şey ton katmanına (GR.tx; 1 = kâğıt) basılır, böylece çizim sırasına uyar (öndeki alev ya da kanat figürü örter).
// Şeytan'ın "ışığı" tek parametredir (lum: 1 cennetteki başmelek … 0 sönmüş, düz siyah siluet).
// Birim: h = baş yüksekliği (8 başlık kahraman oranı). Açıların sıfırı aşağıdır; + değer figürün baktığı yöne (facing).
// Kurallar: rastgelelik yalnız rng(seed); parça sayısı ve sırası parametreyle değişmez (animasyonda sıçrama yok).
'use strict';
const SF = (() => {
  const { tx, tone } = GR;
  const dirv = (a, f) => [Math.sin(a) * f, Math.cos(a)];
  const sst = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };

  // ── iskelet ──
  // p: {x, y (kalça ortası), h, facing (±1), lean (+ öne), twist (0 önden … 1 yandan), shTilt, head (baş eğimi, + yukarı),
  //     armN/armF: [üst kol açısı, dirsek bükümü], legN/legF: [uyluk, diz bükümü (− geriye)]}; N kameraya yakın, F uzak taraf.
  function rig(p) {
    const h = p.h, f = p.facing || 1, tw = p.twist ?? .35, lean = (p.lean || 0) * f;
    const up = [Math.sin(lean), -Math.cos(lean)], rt = [Math.cos(lean), Math.sin(lean)];
    const hip = [p.x, p.y], shC = [hip[0] + up[0] * 2.2 * h, hip[1] + up[1] * 2.2 * h];
    const sw = 1.8 * h * (1 - .6 * tw), hw = .95 * h * (1 - .55 * tw), st = p.shTilt || 0;
    const shN = [shC[0] - rt[0] * sw / 2 * f + up[0] * st * h, shC[1] - rt[1] * sw / 2 * f - st * h], shF = [shC[0] + rt[0] * sw / 2 * f - up[0] * st * h, shC[1] + rt[1] * sw / 2 * f + st * h];
    const hpN = [hip[0] - hw / 2 * f, hip[1]], hpF = [hip[0] + hw / 2 * f, hip[1]];
    // kısa, kalın boyun: çene omuz çizgisinin ~.3 baş üstünde
    const nk = [shC[0] + up[0] * .14 * h, shC[1] + up[1] * .14 * h];
    const hd = [nk[0] + up[0] * .64 * h + rt[0] * f * .1 * h, nk[1] + up[1] * .64 * h + rt[1] * f * .1 * h];
    const arm = (sh, a) => { const a1 = a[0] + lean * f, el = [sh[0] + dirv(a1, f)[0] * 1.35 * h, sh[1] + dirv(a1, f)[1] * 1.35 * h], a2 = a1 + a[1]; return [el, [el[0] + dirv(a2, f)[0] * 1.05 * h, el[1] + dirv(a2, f)[1] * 1.05 * h]]; };
    const leg = (hp, a) => { const kn = [hp[0] + dirv(a[0], f)[0] * 2.0 * h, hp[1] + dirv(a[0], f)[1] * 2.0 * h], a2 = a[0] + a[1]; return [kn, [kn[0] + dirv(a2, f)[0] * 1.95 * h, kn[1] + dirv(a2, f)[1] * 1.95 * h], a2]; };
    const [elN, wrN] = arm(shN, p.armN || [.12, .2]), [elF, wrF] = arm(shF, p.armF || [-.1, .15]);
    const [knN, anN, sN] = leg(hpN, p.legN || [.06, -.06]), [knF, anF, sF] = leg(hpF, p.legF || [-.06, -.04]);
    return { h, f, tw, lean, up, rt, hip, shC, shN, shF, hpN, hpF, nk, hd, elN, wrN, elF, wrF, knN, anN, knF, anF, shinN: sN, shinF: sF, headTilt: p.head || 0 };
  }

  // ── geometri ──
  // iki nokta arasında, iki yanında ayrı genişlik profili olan uzuv (wa: +normal yanı, wb: öbür yan); uçlar eklem dairesiyle örtülür
  function limb(p0, p1, wa, wb, n = 12) {
    const dx = p1[0] - p0[0], dy = p1[1] - p0[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L, A = [], B = [];
    for (let i = 0; i <= n; i++) { const t = i / n, x = p0[0] + dx * t, y = p0[1] + dy * t; A.push([x + nx * wa(t), y + ny * wa(t)]); B.push([x - nx * wb(t), y - ny * wb(t)]); }
    const P = new Path2D(); spline(P, [...A, ...B.reverse()], true, .8); return P;
  }
  // kas profili: a → b doğrusal + (at, c) konumunda yumuşak şişkinlik
  const bump = (a, b, c, at = .3, w = .25) => t => a + (b - a) * t + c * Math.exp(-Math.pow((t - at) / w, 2));
  const circ = (c, r) => { const P = new Path2D(); P.arc(c[0], c[1], r, 0, TAU); return P; };
  // kol: omuz–pazı–dirsek–ön kol tek akış (parçalar aynı maskeye birleşir); bakış yanında pazı, arkada arka kol
  function armPaths(sh, el, wr, h, f) {
    const sg = Math.sign((el[0] - sh[0]) * 0 + 1) * f, out = [];
    const s1 = ((wr[0] - sh[0]) * (el[1] - sh[1]) - (wr[1] - sh[1]) * (el[0] - sh[0])) >= 0 ? 1 : -1; // bükümün iç yanı
    const inA = s1 > 0; // limb'in +normal yanı bükümün içi mi
    { const P = new Path2D(); P.ellipse(sh[0], sh[1] - .01 * h, .25 * h, .23 * h, 0, 0, TAU); out.push(P); } // omuz başı (deltoid + omuzluk)
    out.push(limb(sh, el, inA ? bump(.23 * h, .2 * h, .11 * h, .45) : bump(.24 * h, .2 * h, .1 * h, .35), inA ? bump(.24 * h, .2 * h, .1 * h, .35) : bump(.23 * h, .2 * h, .11 * h, .45))); // uç omuz başının içinde kalır (köşe yok)
    out.push(circ(el, .2 * h));
    out.push(limb(el, wr, bump(.21 * h, .135 * h, .085 * h, .24), bump(.2 * h, .135 * h, .06 * h, .3)));
    // el: kapalı yumruk (kama), başparmak yumrusu
    const a = Math.atan2(wr[1] - el[1], wr[0] - el[0]), c = Math.cos(a), s = Math.sin(a), sd = sg;
    const loc = (x, y) => [wr[0] + (x * c - y * s * sd) * h, wr[1] + (x * s + y * c * sd) * h];
    const H = new Path2D();
    spline(H, [[-.3, -.11], [-.02, -.13], [.28, -.17], [.52, -.15], [.64, -.06], [.64, .07], [.54, .15], [.4, .17], [.3, .26], [.16, .27], [.06, .18], [-.3, .11]].map(([x, y]) => loc(x, y)), true, .8); // bileğe yumuşak bağlanan yumruk, başparmak çıkıntısı (~.8 baş)
    out.push(H);
    return out;
  }
  function legPaths(hp, kn, an, sa, h, f) {
    const out = [];
    out.push(limb(hp, kn, bump(.45 * h, .24 * h, .08 * h, .3), bump(.43 * h, .23 * h, .06 * h, .35)));
    out.push(circ(kn, .23 * h));
    // baldır arkada şişer (bakışın tersi); limb'in +normal yanı hangi yan?
    const nx = -(an[1] - kn[1]), back = (nx * f) < 0; // +normal bakışın tersine mi
    out.push(limb(kn, an, back ? bump(.22 * h, .11 * h, .12 * h, .28) : bump(.21 * h, .11 * h, .03 * h, .2), back ? bump(.21 * h, .11 * h, .03 * h, .2) : bump(.22 * h, .11 * h, .12 * h, .28)));
    const F = new Path2D(); // ayak: bakış yönüne uzanan kama (çarık)
    spline(F, [[-.16, -.16], [.12, -.18], [.4, .0], [.66, .14], [.66, .22], [-.2, .22], [-.22, .05]].map(([x, y]) => [an[0] + x * f * h, an[1] + y * h]), true, .6);
    out.push(F);
    return out;
  }
  // baş profili (sağa bakar; dir ile aynalanır): alın, kaş çıkıntısı, burun, dudak, çene, çene açısı
  const HEAD = [[-.45, -.04], [-.43, -.3], [-.26, -.5], [.02, -.56], [.24, -.47], [.34, -.32], [.37, -.17], [.385, -.1], [.4, -.05], [.475, .1], [.45, .145], [.39, .165],
    [.405, .215], [.39, .245], [.405, .28], [.375, .33], [.395, .41], [.34, .5], [.18, .52], [.02, .44], [-.14, .44], [-.32, .36], [-.44, .2]];
  function headLoc(cx, cy, h, dir, tilt) { const c = Math.cos(-tilt * dir), s = Math.sin(-tilt * dir); return (x, y) => { x *= dir * h; y *= h; return [cx + x * c - y * s, cy + x * s + y * c]; }; }
  function headPath(cx, cy, h, dir, tilt) { const L = headLoc(cx, cy, h, dir, tilt), P = new Path2D(); spline(P, HEAD.map(([x, y]) => L(x, y)), true, .55); return P; }
  // saç: kafatası örtüsü + geriye savrulan 7 sivri perçem (rüzgârla hafif oynar). Boncuk ve alın bandı yok.
  function hairPaths(cx, cy, h, dir, tilt, t, wind = 1, len = 1, seed = 3) {
    const r = rng(seed * 31 + 7), L = headLoc(cx, cy, h, dir, tilt), out = [];
    // başın arkasına akan tek yumuşak kütle; ucunda 3 yumuşak, kıvrık tutam (sivri diken yok). Salınım küçük.
    const sw = k => [Math.sin(t * .9 + k * 1.3) * .025 * wind - .03 * wind, Math.sin(t * .7 + k) * .02 * wind];
    const j = () => (r() - .5) * .03;
    const pts = [[.24, -.43], [.08, -.58], [-.16, -.62], [-.38, -.57], [-.53, -.46],
      [-.6 + j(), -.32], [-.6, -.2],                 // tek yumuşak dalga, sonra enseye iner
      [-.58 + j(), -.07], [-.54, .04],
      [-.5, .12], [-.44, .19],
      [-.38, .22], [-.3, .16], [-.24, -.04], [-.08, -.3], [.12, -.38]]
      .map((p, k) => { const w = k >= 4 && k <= 11 ? sw(k) : [0, 0], m = k >= 4 && k <= 11 ? 1 : 0; return L(p[0] + w[0] * m, p[1] + w[1] * m); });
    const P = new Path2D(); spline(P, pts, true, .85); out.push(P);
    return out;
  }

  // ── çevrim dışı tuvaller (yerel cihaz pikseli, figür kutusu) ──
  const CV = {}; let BW = 0, BH = 0;
  function cnv(k) { let c = CV[k]; if (!c || c.canvas.width < BW || c.canvas.height < BH) { const e = makeCanvas(Math.max(BW, c ? c.canvas.width : 0), Math.max(BH, c ? c.canvas.height : 0)); c = CV[k] = e.getContext('2d', { willReadFrequently: true }); } return c; }
  function clr(c) { c.setTransform(1, 0, 0, 1, 0, 0); c.globalCompositeOperation = 'source-over'; c.globalAlpha = 1; c.clearRect(0, 0, c.canvas.width, c.canvas.height); }
  // incelen çizgi (uçları sivri): pts dünya noktaları, wd en kalın yerdeki genişlik (cihaz px); ctx yerel dönüşümde
  function taper(c, pts, wd, k) {
    const n = 16, S = [], A = [], B = [];
    const cr = (p0, p1, p2, p3, t) => { const t2 = t * t, t3 = t2 * t; return [0, 1].map(j => .5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3)); };
    const m = pts.length;
    for (let i = 0; i <= n; i++) { const u = i / n * (m - 1), s = Math.min(m - 2, Math.floor(u)), tt = u - s; S.push(cr(pts[Math.max(0, s - 1)], pts[s], pts[s + 1], pts[Math.min(m - 1, s + 2)], tt)); }
    for (let i = 0; i <= n; i++) {
      const a = S[Math.max(0, i - 1)], b = S[Math.min(n, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], L = Math.hypot(dx, dy) || 1;
      const w = wd / k * .5 * Math.pow(Math.sin(PI * (.04 + .92 * i / n)), .55);
      A.push([S[i][0] - dy / L * w, S[i][1] + dx / L * w]); B.push([S[i][0] + dy / L * w, S[i][1] - dx / L * w]);
    }
    const Q = new Path2D(); poly(Q, [...A, ...B.reverse()], true); c.fill(Q);
  }

  // ── figürü çiz ──
  // o: {lum (0..1), lit: [x,y] (ışığa doğru), t, anchor, eye (0..1), hair (false | uzunluk), wind, spear: {grip:'N'|'F', ang, len, up},
  //   armor (true), skirt (true), legs (true), waterY (bu çizginin altı çizilmez), rim (kenar ışığı kalınlığı, baş biriminde; .07),
  //   tilt, headScale, seed,
  //   YENİ: cloak (false | uzunluk çarpanı, 1 ≈ dize kadar) pelerin, lines (vuruş yoğunluğu, 0 = yok … 4; 2), robe (true | uzunluk: bele oturan, bileğe inen uzun giysi; skirt yerine), armorAlpha (.85)}
  function draw(J, o = {}) {
    const h = J.h, f = J.f, lum = clamp(o.lum ?? 0), t = o.t || 0, wind = o.wind ?? 1;
    let lit = o.lit || [.7, -.7]; { const l = Math.hypot(lit[0], lit[1]) || 1; lit = [lit[0] / l, lit[1] / l]; }
    const { up, rt } = J, sc = J.shC, an = o.anchor || J.hip;
    const swH = Math.hypot(J.shF[0] - J.shN[0], J.shF[1] - J.shN[1]) / h / 2, hwH = Math.hypot(J.hpF[0] - J.hpN[0], J.hpF[1] - J.hpN[1]) / h / 2;
    const Q = (al, s) => [sc[0] - up[0] * al * h + rt[0] * s * f * h, sc[1] - up[1] * al * h + rt[1] * s * f * h]; // s > 0: bakış (göğüs) yanı
    const dn = [-up[0], -up[1]], tw = J.tw, cs = .22 * tw;                       // cs: göğüs orta çizgisinin yana kayması
    const hh = h * (o.headScale ?? 1.04), tilt = o.tilt ?? J.headTilt, legs = o.legs !== false;
    const G = [[], [], [], []];                                                    // 0 pelerin, 1 uzak, 2 ana, 3 yakın
    const HSs = [];                                                                // tarama: grup başına bir yama

    // pelerin
    let cloakP = null;
    if (o.cloak) {
      const r = rng((o.seed || 3) * 17 + 5), Lc = (o.cloak === true ? 1 : o.cloak), bill = al => wind * (.12 + .1 * Math.sin(t * .7 + al * .9)) * al;
      const bot = 2.15 + 1.05 * Lc;
      const back = [[.05, -(swH + .05)], [.45, -(swH + .32)], [1.1, -(swH + .5)], [1.8, -(swH + .68)], [bot - .1, -(swH + .85)]].map(([al, s]) => [al, s - bill(al)]);
      const N = 11, hem = [];
      const B0 = back[back.length - 1], F0 = [bot - .35, hwH + .2];
      for (let i = 1; i < N - 1; i++) {
        const u = i / (N - 1), al = lerp(B0[0], F0[0], u), s = lerp(B0[1], F0[1], u), sw = Math.sin(t * 1.15 + i * .9) * .07 * wind;
        const tip = i % 2 ? (.22 + .4 * r()) * (1 - .4 * u) : (.02 + .06 * r());
        hem.push([al + (i % 2 ? tip : -tip), s + sw - (i % 2 ? .1 * wind * u : 0)]);
      }
      const front = [[F0[0], F0[1]], [1.3, swH * .55], [.4, swH * .6], [-.02, swH * .45], [-.1, 0]];
      const P = new Path2D(), W = ([al, s]) => Q(al, s);
      const smooth = pts => { for (let i = 1; i < pts.length - 1; i++) { const a = W(pts[i]), b = W(pts[i + 1]); P.quadraticCurveTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); } const e = W(pts[pts.length - 1]); P.lineTo(e[0], e[1]); };
      const s0 = W([-.1, 0]); P.moveTo(s0[0], s0[1]);
      smooth([[-.1, 0], ...back]);
      for (const q of hem) { const p = W(q); P.lineTo(p[0], p[1]); }
      smooth(front);
      P.closePath();
      cloakP = P; G[0].push(P);
    }
    HSs[0] = { type: 'bend', ox: Q(0, 0)[0], oy: Q(0, 0)[1], a: Math.atan2(dn[1], dn[0]) + (-.25 * f), k: -.0015 * f, id: 0 };
    // uzak taraf: kol, bacak, (uzak elde) mızrak
    const spearP = sp => { const g = J['wr' + sp.grip], a = (sp.ang ?? 0) * f, d = [Math.sin(a), -Math.cos(a)], L = (sp.len ?? 7.5) * h, u = sp.up ?? .62;
      const top = [g[0] + d[0] * L * u, g[1] + d[1] * L * u], bot = [g[0] - d[0] * L * (1 - u), g[1] - d[1] * L * (1 - u)], n = [d[1], -d[0]], w0 = Math.max(.045 * h, 1.6);
      const S = new Path2D(); poly(S, [[bot[0] + n[0] * w0, bot[1] + n[1] * w0], [top[0] + n[0] * w0, top[1] + n[1] * w0], [top[0] - n[0] * w0, top[1] - n[1] * w0], [bot[0] - n[0] * w0, bot[1] - n[1] * w0]], true);
      const tl = .8 * h, T = new Path2D(); T.moveTo(top[0] + d[0] * tl, top[1] + d[1] * tl);
      T.quadraticCurveTo(top[0] + n[0] * .2 * h + d[0] * .2 * h, top[1] + n[1] * .2 * h + d[1] * .2 * h, top[0] + n[0] * .06 * h, top[1] + n[1] * .06 * h);
      T.lineTo(top[0] - n[0] * .06 * h, top[1] - n[1] * .06 * h);
      T.quadraticCurveTo(top[0] - n[0] * .2 * h + d[0] * .2 * h, top[1] - n[1] * .2 * h + d[1] * .2 * h, top[0] + d[0] * tl, top[1] + d[1] * tl); return { S, T, top, bot, n, d, w0, tl }; };
    const SP = o.spear ? spearP(o.spear) : null; // mızrak maske hattının dışında, doğrudan katmanlara (ince ve düz: kenar ışığı tek şerit)
    G[1].push(...armPaths(J.shF, J.elF, J.wrF, h, f));
    if (legs) G[1].push(...legPaths(J.hpF, J.knF, J.anF, J.shinF, h, f));
    // ana: bacak (yakın), gövde, boyun, etek, baş, saç
    if (legs) G[2].push(...legPaths(J.hpN, J.knN, J.anN, J.shinN, h, f));
    const T = new Path2D();
    spline(T, [[-.2, .23], [-.13, swH * .5 + .04], [-.06, swH * .85 + .04], [.08, swH + .1], [.4, swH + .16], [.64, swH + .08 + .1 * tw], [.95, swH * .9 + .1 + .08 * tw], [1.3, swH * .72 + .1], [1.68, hwH + .12], [2.05, hwH + .28], [2.32, hwH + .3],
      [2.32, -(hwH + .3)], [2.05, -(hwH + .27)], [1.68, -(hwH + .1)], [1.3, -(swH * .72 + .06)], [.9, -(swH * .9 + .06 + .1 * tw)], [.5, -(swH + .14)], [.2, -(swH + .14)], [-.05, -(swH * .85 + .04)], [-.13, -(swH * .5 + .04)], [-.2, -.24]].map(([a, s]) => Q(a, s)), true, .75);
    G[2].push(T);
    const hd = J.hd, HL = headLoc(hd[0], hd[1], hh, f, tilt);
    G[2].push(limb(Q(.16, .08), HL(-.02, .36), () => .27 * h, () => .26 * h, 4));    // boyun: kalın, öne eğik; çene altını doldurur
    const robe = !!o.robe && legs;
    if (robe) {
      // uzun giysi: bele oturur, ayak bileğine iner; alt kenar hafif dalgalı, iki bacağın arasında kırılır
      const Lr = o.robe === true ? 1 : o.robe, A1 = J.anN, A2 = J.anF, sx = (A1[0] - A2[0]) * rt[0] + (A1[1] - A2[1]) * rt[1];
      const [aL, aR] = sx < 0 ? [A1, A2] : [A2, A1], spread = Math.abs(sx) / h;
      const hemY = (p, k) => [p[0] + dn[0] * h * (.05 - .25 * (1 - Lr)) + rt[0] * k * h, p[1] + dn[1] * h * (.05 - .25 * (1 - Lr)) + rt[1] * k * h];
      const mid = [(aL[0] + aR[0]) / 2 - dn[0] * h * (.1 + .35 * clamp(spread - .3, 0, 1.5)), (aL[1] + aR[1]) / 2 - dn[1] * h * (.1 + .35 * clamp(spread - .3, 0, 1.5))];
      const wv = i => Math.sin(t * 1.2 + i * 1.9) * .03 * h * wind;
      const qq = (al, sd) => { const q = Q(al, sd * f); return q; };
      const pts = [qq(1.7, -(hwH + .26)), qq(2.15, -(hwH + .4)), qq(3.2, -(hwH + .55)), hemY(aL, -.68), hemY(aL, -.2), hemY(aL, .22), mid, hemY(aR, -.22), hemY(aR, .2), hemY(aR, .68), qq(3.2, hwH + .55), qq(2.15, hwH + .4), qq(1.7, hwH + .26)];
      for (let i = 3; i <= 9; i++) pts[i] = [pts[i][0] + dn[0] * wv(i), pts[i][1] + dn[1] * wv(i)];
      const K = new Path2D(); spline(K, pts, true, .55); G[2].push(K);
    }
    if (o.skirt !== false && legs && !robe) {
      const K = new Path2D(), n = 7, y0 = 1.95, y1 = 2.95, w0 = hwH + .3, w1 = hwH + .46, pts = [Q(y0, -w0)];
      for (let i = 0; i < n; i++) { const a = -w1 + (i / n) * 2 * w1, b = -w1 + ((i + 1) / n) * 2 * w1, sw = Math.sin(t * 1.1 + i * 1.7) * .015 + (i % 2) * .05; pts.push(Q(y1 + sw, a + .02), Q(y1 + sw, b - .02), Q(y1 - .08, b)); }
      pts.push(Q(y0, w0)); poly(K, pts, true); G[2].push(K);
    }
    if (o.hair !== false) G[2].push(...hairPaths(hd[0], hd[1], hh, f, tilt, t, wind, o.hair === true || o.hair == null ? 1 : o.hair, o.seed || 3));
    G[2].push(headPath(hd[0], hd[1], hh, f, tilt));
    // yakın: kol, (yakın elde) mızrak
    G[3].push(...armPaths(J.shN, J.elN, J.wrN, h, f));
    const thL = Math.atan2(lit[0], -lit[1]);                                       // ışığa dik çizgiler: ışık kenarında biçime koşut
    HSs[1] = { th: thL + .3, id: 0, anchor: an, ph: .5 };
    HSs[2] = { th: thL, id: 0, anchor: an };
    HSs[3] = { th: thL - .25, id: 0, anchor: an, ph: .25 };

    // ── kutu ve dönüşüm ──
    const M0 = tx.getTransform(), sc0 = Math.hypot(M0.a, M0.b), hd_ = h * sc0;  // hd_: cihaz pikselinde baş boyu
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    const ext = [J.hd, J.hip, J.shN, J.shF, J.elN, J.elF, J.wrN, J.wrF, J.knN, J.knF, J.anN, J.anF, Q(legs ? 2.9 : 2.3, -(swH + .5)), Q(legs ? 2.9 : 2.3, swH + .5)];
    if (o.cloak) { const Lc = o.cloak === true ? 1 : o.cloak; ext.push(Q(2.15 + 1.05 * Lc + .7, -(swH + 1.3 + .5 * wind)), Q(2.15 + 1.05 * Lc + .7, hwH + .4), Q(.5, -(swH + .7 + .3 * wind))); }
    for (const p of ext) { const q = M0.transformPoint(new DOMPoint(p[0], p[1])); x0 = Math.min(x0, q.x); y0 = Math.min(y0, q.y); x1 = Math.max(x1, q.x); y1 = Math.max(y1, q.y); }
    const mg = 1.1 * hd_ + 12;
    x0 = Math.max(0, Math.floor(x0 - mg)); y0 = Math.max(0, Math.floor(y0 - mg)); x1 = Math.min(GR.tc.width, Math.ceil(x1 + mg)); y1 = Math.min(GR.tc.height, Math.ceil(y1 + mg));
    if (o.waterY != null) { const wy = M0.transformPoint(new DOMPoint(J.hip[0], o.waterY)).y; y1 = Math.min(y1, Math.ceil(wy + 2)); }
    if (x1 <= x0 || y1 <= y0) return { T };
    BW = x1 - x0; BH = y1 - y0;
    const ML = new DOMMatrix().translate(-x0, -y0).multiply(M0);                  // dünya → yerel cihaz
    const lv = [M0.a * lit[0] + M0.c * lit[1], M0.b * lit[0] + M0.d * lit[1]]; { const l = Math.hypot(lv[0], lv[1]) || 1; lv[0] /= l; lv[1] /= l; }
    const toL = p => { const q = ML.transformPoint(new DOMPoint(p[0], p[1])); return [q.x, q.y]; };

    // ── tonlar ve etkiler (lum'a bağlı yumuşak geçişler) ──
    const core = lerp(.03, .97, sst(.47, .64, lum));
    const coreG = [core, lerp(core, core * .86, sst(.5, .9, lum)), core, core];
    const sRim = 1 - sst(.5, .8, lum), sLit = 0, sSh = 0, sInk = sst(.5, .75, lum);
    const light = lum >= .6, skTone = light ? 0 : 1, sgS = light ? -1 : 1;     // vuruşlar: koyu figürde ışık yanından beyaz, açıkta gölge yanından mürekkep
    const rw = Math.max(3, hd_ * (o.rim ?? .075));
    // ışık merkezi: kenar ışığı burada en kalın; uzaklaştıkça incelir (beyaz çizgiler incelip söner, saydamlaşmaz)
    const lc = toL([sc[0] + lit[0] * 1.1 * h - up[0] * .35 * h, sc[1] + lit[1] * 1.1 * h - up[1] * .35 * h]);

    // maskeler (grup başına), zırh/göz katmanı
    const Mk = [cnv('m0'), cnv('m1'), cnv('m2'), cnv('m3')], Z = cnv('Z'), F = cnv('F');
    const AM = [];
    for (let g = 0; g < 4; g++) {
      if (!G[g].length) { AM.push(null); continue; }
      const m = Mk[g]; clr(m); m.setTransform(ML.a, ML.b, ML.c, ML.d, ML.e, ML.f); m.fillStyle = '#fff';
      for (const P of G[g]) m.fill(P);
      AM.push(m.getImageData(0, 0, BW, BH).data);
    }
    // ── vuruşlar (beyaz çizgi tekniği): ışık yanındaki kenardan kütleye giren, kesit kavsini izleyen, içe sivrilen çizgiler ──
    // Çapalar gövde/uzuv yerel koordinatında (rng(seed) ile sabit); kenar her karede maskede yürüyerek bulunur, poz değişince kaymaz.
    const dens = clamp(o.lines ?? 2, 0, 4), sv = [lv[0] * sgS, lv[1] * sgS];               // vuruşun girdiği yan (koyu: ışık, açık: gölge)
    const ins = (a, x, y) => { const qx = x | 0, qy = y | 0; return qx >= 0 && qy >= 0 && qx < BW && qy < BH && a[(qy * BW + qx) * 4 + 3] >= 128; };
    const lin = v => { const w = [ML.a * v[0] + ML.c * v[1], ML.b * v[0] + ML.d * v[1]], l = Math.hypot(w[0], w[1]) || 1; return [w[0] / l, w[1] / l]; };
    const strk = (c, a, P, dOut, L, w, bend, bdir) => {                    // P: içerde çapa (yerel cihaz), dOut: dışa doğru
      if (!a || !ins(a, P[0], P[1])) return;
      let E = null; for (let s2 = 0; s2 < 4 * hd_; s2 += 1) { const x = P[0] + dOut[0] * s2, y = P[1] + dOut[1] * s2; if (!ins(a, x, y)) { E = [x, y]; break; } }
      if (!E) return;
      const n = 10, A = [], B = [], din = [-dOut[0], -dOut[1]], nn = [-din[1], din[0]];
      for (let i = 0; i <= n; i++) { const u = i / n, cx = E[0] + din[0] * L * u + bdir[0] * bend * L * u * u, cy = E[1] + din[1] * L * u + bdir[1] * bend * L * u * u, hw = w * .5 * Math.pow(1 - u, .85) + .15;
        A.push([cx + nn[0] * hw, cy + nn[1] * hw]); B.push([cx - nn[0] * hw, cy - nn[1] * hw]); }
      const Pp = new Path2D(); poly(Pp, [[E[0] + dOut[0] * 1.5, E[1] + dOut[1] * 1.5], ...A, ...B.reverse()], true); c.fill(Pp);
    };
    const SKc = cnv('K'); let SK = null;
    const rS = rng((o.seed || 3) * 101 + 13), minGap = 12 / hd_;              // aralık ≥ 12 px (baş biriminde)
    const torsoStrokes = [], limbStrokes = [];
    { // gövde: çapalar boy boyunca farklı aralık ve uzunlukta; kesit boyunca (yana) hafif aşağı kavisli
      const n = Math.round(dens * 2.5 * clamp(hd_ / 110, .45, 1)); let al = .12 + rS() * .1;
      for (let i = 0; i < 8; i++) { const step = Math.max(minGap, (1.7 / Math.max(1, n)) * (.6 + .8 * rS())), Ls = .18 + .6 * rS() * rS() + .12 * rS(), wj = rS();
        if (i < n && al < 1.9) torsoStrokes.push({ al, Ls, wj }); al += step; }
      // uzuvlar: kesit boyunca (eksene çapraz) 1–3 vuruş
      const segs = [[1, J.shF, J.elF], [1, J.elF, J.wrF], [3, J.shN, J.elN], [3, J.elN, J.wrN]];
      if (legs && !robe) segs.push([1, J.hpF, J.knF], [1, J.knF, J.anF], [2, J.hpN, J.knN], [2, J.knN, J.anN]);
      for (const [g, p0, p1] of segs) { const k = Math.round(dens * .75); let u = .2 + .15 * rS();
        for (let i = 0; i < 3; i++) { const segL = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]) / h, step = Math.max(minGap / Math.max(.3, segL), .22 + .25 * rS()), Ls = .16 + .2 * rS();
          if (i < k && u < .85) limbStrokes.push({ g, p0, p1, u, Ls }); u += step; } }
    }
    if (dens > 0 && hd_ > 34) {
      clr(SKc); SKc.fillStyle = '#fff'; let any = false;
      for (const S of limbStrokes) {
        const a = AM[S.g], P0 = toL(S.p0), P1 = toL(S.p1), ax = [P1[0] - P0[0], P1[1] - P0[1]], La = Math.hypot(ax[0], ax[1]) || 1, d = [ax[0] / La, ax[1] / La];
        let nrm = [-d[1], d[0]]; const dt = nrm[0] * sv[0] + nrm[1] * sv[1]; if (Math.abs(dt) < .3) continue; if (dt < 0) nrm = [-nrm[0], -nrm[1]];
        strk(SKc, a, [P0[0] + ax[0] * S.u, P0[1] + ax[1] * S.u], nrm, hd_ * S.Ls, Math.max(2.6, hd_ * .032), .12, d); any = true;
      }
      // pelerin: gölge/ışık yanından içeri birkaç uzun kıvrım vuruşu
      if (AM[0]) for (let i = 0; i < Math.round(dens * 2); i++) { const al = .6 + i * .55 + rS() * .2, P = toL(Q(al, -(swH + .2 + .2 * al))); strk(SKc, AM[0], P, sv, hd_ * (.5 + .4 * rS()), Math.max(3, hd_ * .035), .15, lin(dn)); any = true; }
      if (any) SK = SKc.getImageData(0, 0, BW, BH).data;
    }
    // zırh çizgileri ve göz: ana grubun tonuna karışır (öndeki kol ve sahnedeki önde çizilen her şey örter)
    let AR = null; const arTone = skTone;
    {
      clr(Z); Z.setTransform(ML.a, ML.b, ML.c, ML.d, ML.e, ML.f); Z.fillStyle = '#fff'; let any = false;
      if (o.armor !== false && hd_ > 40) {
        any = true; const k = sc0, wA = Math.max(3, hd_ * .034);
        for (let b2 = 0, nb = lum < .5 ? 0 : 1; b2 < nb; b2++) { const al = 1.45; taper(Z, [Q(al, -(swH * .72 + .05)), Q(al + .07, cs), Q(al, swH * .72 + .1)], wA * (1 - .12 * b2), k); } // lorika bantları
        taper(Z, [Q(1.98, -(hwH + .3)), Q(2.03, cs), Q(1.98, hwH + .3)], wA * 1.3, k);                        // kemer
        for (const sd of [-1, 1]) taper(Z, [Q(.02, sd * swH * .6), Q(.14, sd * (swH + .1)), Q(.4, sd * (swH + .2))], wA * .85, k); // omuzluk kenarı (omuz başına tek çizgi)
        if (o.skirt !== false && legs && !robe) for (let i = 1; i < 7; i += 2) { const a2 = -(hwH + .46) + (i / 7) * 2 * (hwH + .46); taper(Z, [Q(2.1, a2 * .85), Q(2.85, a2)], wA * .8, k); }
      }
      if (dens > 0 && hd_ > 34) {
        // gövde vuruşları: ışık (ya da gölge) yanındaki gövde kenarından içeri
        const side = (rt[0] * sv[0] + rt[1] * sv[1]) * 1 >= 0 ? 1 : -1, rD = lin([rt[0] * side, rt[1] * side]);
        if (Math.abs(lin(rt)[0] * sv[0] + lin(rt)[1] * sv[1]) > .2) for (const S of torsoStrokes) {
          const P = toL(Q(S.al, side * f * .15)); Z.save(); Z.setTransform(1, 0, 0, 1, 0, 0);
          strk(Z, AM[2], P, rD, hd_ * S.Ls, Math.max(2.8, hd_ * (.028 + .012 * S.wj)), .18, lin(dn)); Z.restore(); any = true;
        }
        // uzun giysi kıvrımları: etekten yukarı giren uzun, sivrilen vuruşlar (ışık ya da gölge yanında yoğun)
        if (robe) { const rF = rng((o.seed || 3) * 7 + 1), dD = lin(dn), dU = [-dD[0], -dD[1]];
          for (let i = 0; i < 2 + Math.round(dens); i++) { const sd = (side > 0 ? 1 : -1) * (.75 - i * (.45 + .2 * rF())) , P = toL(Q(4.8, sd * f * (hwH + .3)));
            Z.save(); Z.setTransform(1, 0, 0, 1, 0, 0); strk(Z, AM[2], P, dD, hd_ * (.7 + .8 * rF()), Math.max(3, hd_ * .038), .05, lin(rt)); Z.restore(); } }
        // saç telleri: ışık yanında 3–4 ince, kıvrık vuruş (yalnız koyu figür, ışık üstten)
        if (!light && lit[1] < 0 && o.hair !== false) {
          const sw2 = Math.sin(t * .8) * .02 * wind, k = sc0;
          for (const c of [[[.06, -.55], [-.06, -.53], [-.14, -.57]], [[-.22, -.55], [-.34, -.5], [-.42, -.54]], [[-.47, -.4], [-.55, -.32], [-.53, -.24]]])   // kısa, kıvrık teller: yalnız saç kütlesinin üst-arka kenarında
            taper(Z, c.map(([x, y]) => HL(x + sw2, y)), Math.max(2, hd_ * .02), k);
          any = true;
        }
      }
      const eo = o.eye ?? (lum < .5 ? 1 : 0);
      if (eo > 0 && hd_ > 24) {                                                    // göz: kaşın altında tek ince ışık
        any = true; const e0 = HL(.19, -.04), e1 = HL(.34, -.055), dx = e1[0] - e0[0], dy = e1[1] - e0[1], L = Math.hypot(dx, dy) || 1, th = Math.max(1.7 / sc0, h * .028) * eo;
        Z.beginPath(); Z.moveTo(e0[0], e0[1]);
        Z.quadraticCurveTo((e0[0] + e1[0]) / 2 + dy / L * th, (e0[1] + e1[1]) / 2 - dx / L * th, e1[0], e1[1]);
        Z.quadraticCurveTo((e0[0] + e1[0]) / 2 - dy / L * th * .5, (e0[1] + e1[1]) / 2 + dx / L * th * .5, e0[0], e0[1]); Z.fill();
      }
      if (any) AR = Z.getImageData(0, 0, BW, BH).data;
    }

    // ── piksel döngüsü: grup grup, arkadan öne ──
    const BW4 = BW * 4, lx = lv[0], ly = lv[1];
    const smp = (a, x, y) => {
      if (x < 0 || y < 0 || x >= BW - 1 || y >= BH - 1) return 0;
      const xi = x | 0, yi = y | 0, fx = x - xi, fy = y - yi, i = (yi * BW + xi) * 4 + 3;
      return ((a[i] * (1 - fx) + a[i + 4] * fx) * (1 - fy) + (a[i + BW4] * (1 - fx) + a[i + BW4 + 4] * fx) * fy) * (1 / 255);
    };
    const Dl = hd_ * lerp(.25, .45, lum), Ds = hd_ * .2, rI0 = 0, rI1 = Math.max(2, hd_ * .035);
    const DIR = Array.from({ length: 8 }, (_, k) => { const a = k * TAU / 8, dx = Math.cos(a), dy = Math.sin(a); return [dx, dy, rI0 + rI1 * Math.max(0, -(dx * lx + dy * ly))]; });
    const doRL = sRim > .01, Dmax = rw + 1.5;
    const rIm = rI0 + rI1 + 1;
    const full = (a, x, y) => { const qx = (x + .5) | 0, qy = (y + .5) | 0; return qx >= 0 && qy >= 0 && qx < BW && qy < BH && a[(qy * BW + qx) * 4 + 3] === 255; };
    const crisp = v => v <= .2 ? 0 : v >= .8 ? 1 : (v - .2) / .6;
    const R0 = .55 * hd_, R1 = 3.6 * hd_;
    let img = F.__img; if (!img || img.width !== BW || img.height !== BH) img = F.__img = F.createImageData(BW, BH);
    const O = img.data;
    for (let y = 0; y < BH; y++) for (let x = 0; x < BW; x++) {
      const i = (y * BW + x) * 4; let vp = 0, al = 0, g0 = 0;
      for (let g = 3; g > 0; g--) { const a = AM[g]; if (a && a[i + 3] === 255) { g0 = g; break; } } // öndeki tam örten grubun arkası hesaplanmaz
      for (let g = g0; g < 4; g++) {
        const a = AM[g]; if (!a) continue; const c = a[i + 3] * (1 / 255); if (c <= 0) continue;
        let tg = coreG[g];
        if (sLit > .01 && !full(a, x + lx * Dl, y + ly * Dl)) { let n = 0; for (let k = 1; k <= 4; k++) n += smp(a, x + lx * Dl * k / 4, y + ly * Dl * k / 4); tg += (Math.min(1, coreG[g] + .5) - tg) * sLit * (1 - n / 4); }
        const Dsg = g === 0 ? Ds * 2.4 : Ds;
        if (sSh > .01 && !full(a, x - lx * Dsg, y - ly * Dsg)) { let n = 0; for (let k = 1; k <= 4; k++) n += smp(a, x - lx * Dsg * k / 4, y - ly * Dsg * k / 4); tg += (Math.max(0, coreG[g] - (g === 0 ? .6 : .35)) - tg) * sSh * .85 * (1 - n / 4); }
        if (sInk > .01 && !(full(a, x + rIm, y) && full(a, x - rIm, y) && full(a, x, y + rIm) && full(a, x, y - rIm))) { let e = 1; for (let k = 0; k < 8 && e > 0; k++) { const D = DIR[k], s = smp(a, x + D[0] * D[2], y + D[1] * D[2]); if (s < e) e = s; } tg -= tg * sInk * crisp(1 - e); }
        if (doRL) {
          // hızlı ret: ışık yönünde en derin örnek de kütlenin içindeyse kenar ışığı ve beyaz çizgi yok
          const qx = (x + lx * Dmax + .5) | 0, qy = (y + ly * Dmax + .5) | 0;
          if (!(qx >= 0 && qy >= 0 && qx < BW && qy < BH && a[(qy * BW + qx) * 4 + 3] === 255)) {
            const ddx = x - lc[0], ddy = y - lc[1], dd = Math.sqrt(ddx * ddx + ddy * ddy);
            if (sRim > .01) { const fd = clamp(1 - (dd - R0) / (R1 - R0)), w = rw * (g < 2 ? .75 : 1) * (.3 + .7 * fd); tg += (1 - tg) * sRim * crisp(1 - smp(a, x + lx * w, y + ly * w)); }
            // (eko çizgiler kaldırıldı: yerlerine vuruşlar)
          }
        }
        if (g === 2 && AR) { const r = AR[i + 3] * (1 / 255); if (r > 0) tg += (arTone - tg) * crisp(r); }
        else if (g !== 2 && SK) { const r = SK[i + 3] * (1 / 255); if (r > 0) tg += (skTone - tg) * crisp(r); }
        vp = vp * (1 - c) + tg * c; al = al * (1 - c) + c;
      }
      if (al > 0) { const v = vp / al * 255; O[i] = O[i + 1] = O[i + 2] = v; O[i + 3] = al * 255; } else O[i + 3] = 0;
    }
    F.setTransform(1, 0, 0, 1, 0, 0); F.putImageData(img, 0, 0);

    // ── katmanlara bas ──
    const clipW = c => { if (o.waterY != null) { const C = new Path2D(); C.rect(-1e5, -1e5, 2e5, 1e5 + o.waterY); c.clip(C); } };
    const spear = () => {
      const { S, T: Tp, top, bot, n, d, w0, tl } = SP, gi = o.spear.grip === 'F' ? 1 : 3;
      tx.save(); clipW(tx); tx.fillStyle = tone(coreG[gi]); tx.fill(S); tx.fill(Tp);
      const sn = n[0] * lit[0] + n[1] * lit[1] > 0 ? 1 : -1, ew = Math.max(2.2 / sc0, w0 * .7);   // ışık yanındaki kenar şeridi
      if (sRim > .01) { tx.fillStyle = tone(lerp(coreG[gi], 1, sRim)); const e = (p, k) => [p[0] + n[0] * sn * k, p[1] + n[1] * sn * k], P = new Path2D();
        poly(P, [e(bot, w0), e(top, w0), e(top, w0 - ew), e(bot, w0 - ew)], true); tx.fill(P);
        const P2 = new Path2D(); const tp = [top[0] + d[0] * tl, top[1] + d[1] * tl]; poly(P2, [e(top, .2 * h * .55), tp, e(top, .2 * h * .3)], true); tx.fill(P2); }
      if (sInk > .01) { tx.strokeStyle = tone(lerp(coreG[gi], 0, sInk)); tx.lineWidth = Math.max(1.5 / sc0, h * .012); tx.stroke(S); tx.stroke(Tp); }
      tx.restore();
      const px = GR.px; px.save(); clipW(px); px.fillStyle = GR.hatch(HSs[gi] || HSs[2]); px.fill(S); px.fill(Tp); px.restore();
    };
    if (SP && o.spear.grip === 'F') spear();
    tx.save(); clipW(tx); tx.setTransform(1, 0, 0, 1, 0, 0); tx.drawImage(F.canvas, 0, 0, BW, BH, x0, y0, BW, BH); tx.restore();
    // üst katmanda (GR.ox) daha önce çizilmiş çizgiler (ör. arkadaki kanadın tüy çizgileri) figürün altında kalmalı: siluet onları siler
    const ox = GR.ox; ox.save(); clipW(ox); ox.setTransform(1, 0, 0, 1, 0, 0); ox.globalCompositeOperation = 'destination-out'; ox.drawImage(F.canvas, 0, 0, BW, BH, x0, y0, BW, BH); ox.restore();
    const px = GR.px; px.save(); clipW(px);
    for (let g = 0; g < 4; g++) { if (!G[g].length) continue; const col = GR.hatch(HSs[g]); px.fillStyle = col; for (const P of G[g]) px.fill(P); }
    px.restore();
    if (SP && o.spear.grip !== 'F') spear();
    return { T, cloak: cloakP };
  }
  return { rig, draw, limb, headPath, hairPaths };
})();
