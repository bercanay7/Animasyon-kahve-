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
    const arm = (sh, a) => { const a1 = a[0] + lean * f, el = [sh[0] + dirv(a1, f)[0] * 1.45 * h, sh[1] + dirv(a1, f)[1] * 1.45 * h], a2 = a1 + a[1]; return [el, [el[0] + dirv(a2, f)[0] * 1.2 * h, el[1] + dirv(a2, f)[1] * 1.2 * h]]; };
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
    out.push(limb(sh, el, inA ? bump(.26 * h, .16 * h, .06 * h, .42) : bump(.28 * h, .16 * h, .05 * h, .3), inA ? bump(.28 * h, .16 * h, .05 * h, .3) : bump(.26 * h, .16 * h, .06 * h, .42)));
    out.push(circ(el, .165 * h));
    out.push(limb(el, wr, bump(.18 * h, .115 * h, .06 * h, .22), bump(.175 * h, .115 * h, .045 * h, .3)));
    // el: kapalı yumruk (kama), başparmak yumrusu
    const a = Math.atan2(wr[1] - el[1], wr[0] - el[0]), c = Math.cos(a), s = Math.sin(a), sd = sg;
    const loc = (x, y) => [wr[0] + (x * c - y * s * sd) * h, wr[1] + (x * s + y * c * sd) * h];
    const H = new Path2D();
    spline(H, [[-.06, -.11], [.12, -.14], [.3, -.14], [.41, -.07], [.43, .04], [.37, .13], [.2, .17], [.04, .16], [-.06, .11]].map(([x, y]) => loc(x, y)), true, .8);
    out.push(H);
    return out;
  }
  function legPaths(hp, kn, an, sa, h, f) {
    const out = [];
    out.push(limb(hp, kn, bump(.37 * h, .2 * h, .05 * h, .3), bump(.35 * h, .19 * h, .04 * h, .35)));
    out.push(circ(kn, .19 * h));
    // baldır arkada şişer (bakışın tersi); limb'in +normal yanı hangi yan?
    const nx = -(an[1] - kn[1]), back = (nx * f) < 0; // +normal bakışın tersine mi
    out.push(limb(kn, an, back ? bump(.19 * h, .1 * h, .08 * h, .28) : bump(.18 * h, .1 * h, .02 * h, .2), back ? bump(.18 * h, .1 * h, .02 * h, .2) : bump(.19 * h, .1 * h, .08 * h, .28)));
    const F = new Path2D(); // ayak: bakış yönüne uzanan kama (çarık)
    spline(F, [[-.16, -.16], [.12, -.18], [.4, .0], [.66, .14], [.66, .22], [-.2, .22], [-.22, .05]].map(([x, y]) => [an[0] + x * f * h, an[1] + y * h]), true, .6);
    out.push(F);
    return out;
  }
  // baş profili (sağa bakar; dir ile aynalanır): alın, kaş çıkıntısı, burun, dudak, çene, çene açısı
  const HEAD = [[-.4, -.06], [-.33, -.36], [-.06, -.52], [.22, -.46], [.34, -.3], [.38, -.16], [.42, -.09], [.38, -.03], [.45, .1], [.5, .15], [.4, .18],
    [.41, .22], [.37, .25], [.4, .3], [.35, .35], [.38, .44], [.28, .53], [.12, .5], [-.02, .4], [-.2, .42], [-.36, .26]];
  function headLoc(cx, cy, h, dir, tilt) { const c = Math.cos(-tilt * dir), s = Math.sin(-tilt * dir); return (x, y) => { x *= dir * h; y *= h; return [cx + x * c - y * s, cy + x * s + y * c]; }; }
  function headPath(cx, cy, h, dir, tilt) { const L = headLoc(cx, cy, h, dir, tilt), P = new Path2D(); spline(P, HEAD.map(([x, y]) => L(x, y)), true, .55); return P; }
  // saç: kafatası örtüsü + geriye savrulan 7 sivri perçem (rüzgârla hafif oynar). Boncuk ve alın bandı yok.
  function hairPaths(cx, cy, h, dir, tilt, t, wind = 1, len = 1, seed = 3) {
    const r = rng(seed * 31 + 7), L = headLoc(cx, cy, h, dir, tilt), out = [];
    const cap = new Path2D(); // kafatasını arkadan ve üstten taşan saç kütlesi (alın çizgisi açık kalır)
    spline(cap, [[.24, -.44], [.02, -.6], [-.3, -.55], [-.5, -.32], [-.52, -.05], [-.42, .18], [-.28, .22], [-.16, .02], [0, -.22], [.2, -.32]].map(([x, y]) => L(x, y)), true, .8);
    out.push(cap);
    const n = 6;
    for (let i = 0; i < n; i++) {
      // kökler saç kütlesinin arka kenarında; perçemler geriye (rüzgâr yönüne) akar, uçları hafif kıvrılır
      const u = i / (n - 1), phi = lerp(-.15, 1.85, u) + (r() - .5) * .1;
      const root = [-.1 - Math.sin(phi) * .3, -.14 - Math.cos(phi) * .32];
      const sway = Math.sin(t * (1.1 + .19 * i) + i * 1.7) * .07 * wind + Math.sin(t * .43 + i * 2.1) * .04 * wind;
      let d = [-1, lerp(-.5, .55, u) - .1 * wind]; { const l = Math.hypot(d[0], d[1]); d = [d[0] / l, d[1] / l]; }
      const ca = Math.cos(sway), sa = Math.sin(sway); d = [d[0] * ca - d[1] * sa, d[0] * sa + d[1] * ca];
      const Ln = (.42 + .2 * r()) * lerp(1.1, .7, u) * (len > 1 ? 1 + .4 * (len - 1) : 1), w = .14 + .05 * r();
      const nn = [-d[1], d[0]], tip = [root[0] + d[0] * Ln, root[1] + d[1] * Ln - .07], curl = (.07 + .05 * r()) * (u < .5 ? -1 : 1);
      const mid = [root[0] + d[0] * Ln * .5 + nn[0] * curl, root[1] + d[1] * Ln * .5 + nn[1] * curl];
      const a0 = L(root[0] + nn[0] * w, root[1] + nn[1] * w), a1 = L(root[0] - nn[0] * w, root[1] - nn[1] * w);
      const m0 = L(mid[0] + nn[0] * w * .75, mid[1] + nn[1] * w * .75), m1 = L(mid[0] - nn[0] * w * .6, mid[1] - nn[1] * w * .6), T = L(tip[0], tip[1]);
      const P = new Path2D(); P.moveTo(a0[0], a0[1]); P.quadraticCurveTo(m0[0], m0[1], T[0], T[1]); P.quadraticCurveTo(m1[0], m1[1], a1[0], a1[1]); P.closePath();
      out.push(P);
    }
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
  //   YENİ: cloak (false | uzunluk çarpanı, 1 ≈ dize kadar) pelerin, lines (beyaz çizgi sayısı, 0–4; 3), armorAlpha (.85)}
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
    HSs[0] = { type: 'bend', ox: Q(0, 0)[0], oy: Q(0, 0)[1], a: Math.atan2(dn[1], dn[0]) + (-.25 * f), k: -.0015 * f, id: 9 };
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
    G[2].push(limb(Q(.15, .02), HL(-.04, .38), () => .22 * h, () => .21 * h, 4));    // boyun: başın ~%50'si kalınlığında
    if (o.skirt !== false && legs) {
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
    const core = lerp(.03, .97, sst(.1, .9, lum) ** 1.3);
    const coreG = [lerp(.03, .62, sst(.1, .9, lum)), lum < .2 ? core : lerp(core, core * .72, sst(.2, .8, lum)), core, core];
    const sRim = 1 - sst(.45, .85, lum), sWL = 1 - sst(.12, .4, lum), sLit = sst(.06, .35, lum) * (1 - sst(.75, 1, lum)), sSh = sst(.3, .7, lum), sInk = sst(.35, .75, lum);
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
    // zırh çizgileri ve göz: ana grubun tonuna karışır (öndeki kol ve sahnedeki önde çizilen her şey örter)
    let AR = null; const arTone = lum < .5 ? 1 : 0;
    {
      clr(Z); Z.setTransform(ML.a, ML.b, ML.c, ML.d, ML.e, ML.f); Z.fillStyle = '#fff'; let any = false;
      if (o.armor !== false && hd_ > 40) {
        any = true; const k = sc0, wA = Math.max(3, hd_ * .034);
        taper(Z, [Q(.1, cs - .46), Q(.27, cs - .14), Q(.29, cs + .1), Q(.12, cs + .44)], wA, k);                 // yaka
        taper(Z, [Q(.34, cs), Q(.75, cs + .02), Q(1.2, cs * .9)], wA * .9, k);                                // ortadan inen tek sırt çizgisi
        for (let b2 = 0, nb = lum < .5 ? 2 : 3; b2 < nb; b2++) { const al = 1.36 + b2 * (lum < .5 ? .3 : .22); taper(Z, [Q(al, -(swH * .72 + .05)), Q(al + .07, cs), Q(al, swH * .72 + .1)], wA * (1 - .12 * b2), k); } // lorika bantları
        taper(Z, [Q(1.98, -(hwH + .3)), Q(2.03, cs), Q(1.98, hwH + .3)], wA * 1.3, k);                        // kemer
        for (const sd of [-1, 1]) taper(Z, [Q(-.04, sd * swH * .55), Q(.1, sd * (swH + .12)), Q(.42, sd * (swH + .24))], wA * .9, k); // omuzluk kenarı
        if (o.skirt !== false && legs) for (let i = 1; i < 7; i += 2) { const a2 = -(hwH + .46) + (i / 7) * 2 * (hwH + .46); taper(Z, [Q(2.1, a2 * .85), Q(2.85, a2)], wA * .8, k); }
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
    const nWL = hd_ > 40 ? Math.round(clamp(o.lines ?? 3, 0, 4)) : 0, gapWL = Math.max(9, hd_ * .11);
    const WL = []; { let a = rw; for (let j = 0; j < nWL; j++) { const w = Math.max(3.2, hd_ * (.052 - .008 * j)); a += gapWL * (1 + .35 * j); WL.push([a, w]); a += w; } }
    const Dl = hd_ * lerp(.25, .45, lum), Ds = hd_ * .2, rI0 = Math.max(1.4, hd_ * .016), rI1 = Math.max(1.6, hd_ * .04);
    const DIR = Array.from({ length: 8 }, (_, k) => { const a = k * TAU / 8, dx = Math.cos(a), dy = Math.sin(a); return [dx, dy, rI0 + rI1 * Math.max(0, -(dx * lx + dy * ly))]; });
    const doRL = sRim > .01 || sWL > .01, Dmax = (WL.length && sWL > .01 ? WL[WL.length - 1][0] + WL[WL.length - 1][1] : rw) + 1.5;
    const rIm = rI0 + rI1 + 1;
    const full = (a, x, y) => { const qx = (x + .5) | 0, qy = (y + .5) | 0; return qx >= 0 && qy >= 0 && qx < BW && qy < BH && a[(qy * BW + qx) * 4 + 3] === 255; };
    const crisp = v => v <= .2 ? 0 : v >= .8 ? 1 : (v - .2) / .6;
    const nkL = toL(Q(-.08, 0)), upL = (() => { const v = [ML.a * up[0] + ML.c * up[1], ML.b * up[0] + ML.d * up[1]], l = Math.hypot(v[0], v[1]) || 1; return [v[0] / l, v[1] / l]; })();
    const R0 = .55 * hd_, R1 = 3.6 * hd_, Q0 = .25 * hd_, Q1 = 2.0 * hd_;
    let img = F.__img; if (!img || img.width !== BW || img.height !== BH) img = F.__img = F.createImageData(BW, BH);
    const O = img.data;
    for (let y = 0; y < BH; y++) for (let x = 0; x < BW; x++) {
      const i = (y * BW + x) * 4; let vp = 0, al = 0, g0 = 0;
      for (let g = 3; g > 0; g--) { const a = AM[g]; if (a && a[i + 3] === 255) { g0 = g; break; } } // öndeki tam örten grubun arkası hesaplanmaz
      for (let g = g0; g < 4; g++) {
        const a = AM[g]; if (!a) continue; const c = a[i + 3] * (1 / 255); if (c <= 0) continue;
        let tg = coreG[g];
        if (sLit > .01 && !full(a, x + lx * Dl, y + ly * Dl)) { let n = 0; for (let k = 1; k <= 4; k++) n += smp(a, x + lx * Dl * k / 4, y + ly * Dl * k / 4); tg += (Math.min(1, coreG[g] + .5) - tg) * sLit * (1 - n / 4); }
        if (sSh > .01 && !full(a, x - lx * Ds, y - ly * Ds)) { let n = 0; for (let k = 1; k <= 4; k++) n += smp(a, x - lx * Ds * k / 4, y - ly * Ds * k / 4); tg += (Math.max(0, coreG[g] - .35) - tg) * sSh * .85 * (1 - n / 4); }
        if (sInk > .01 && !(full(a, x + rIm, y) && full(a, x - rIm, y) && full(a, x, y + rIm) && full(a, x, y - rIm))) { let e = 1; for (let k = 0; k < 8 && e > 0; k++) { const D = DIR[k], s = smp(a, x + D[0] * D[2], y + D[1] * D[2]); if (s < e) e = s; } tg -= tg * sInk * (1 - e); }
        if (doRL) {
          // hızlı ret: ışık yönünde en derin örnek de kütlenin içindeyse kenar ışığı ve beyaz çizgi yok
          const qx = (x + lx * Dmax + .5) | 0, qy = (y + ly * Dmax + .5) | 0;
          if (!(qx >= 0 && qy >= 0 && qx < BW && qy < BH && a[(qy * BW + qx) * 4 + 3] === 255)) {
            const ddx = x - lc[0], ddy = y - lc[1], dd = Math.sqrt(ddx * ddx + ddy * ddy);
            if (sRim > .01) { const fd = clamp(1 - (dd - R0) / (R1 - R0)), w = rw * (g < 2 ? .75 : 1) * (.3 + .7 * fd); tg += (1 - tg) * sRim * crisp(1 - smp(a, x + lx * w, y + ly * w)); }
            if (g === 2 && sWL > .01 && (x - nkL[0]) * upL[0] + (y - nkL[1]) * upL[1] < 0) { const fq = clamp(1 - (dd - Q0) / (Q1 - Q0)); for (let j = 0; j < nWL; j++) { const a0 = WL[j][0], w = WL[j][1] * clamp((fq - .22 * j) / (1 - .22 * j)); if (w < .9) continue; const s0 = smp(a, x + lx * a0, y + ly * a0); if (s0 <= 0) continue; tg += (1 - tg) * sWL * crisp(s0 * (1 - smp(a, x + lx * (a0 + w), y + ly * (a0 + w)))); } }
          }
        }
        if (g === 2 && AR) { const r = AR[i + 3] * (1 / 255); if (r > 0) tg += (arTone - tg) * crisp(r); }
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
