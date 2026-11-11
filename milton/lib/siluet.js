// Siluet figür: oranlı iskelet (rig) + parça parça dış hat. Parçalar koyu (ya da ışıklı) kütle olarak dolar;
// ışık yönünde ince kenar ışığı, gölge yönünde koyu kenar bırakılır; zırh ayrıntıları üst katmana beyaz/siyah çizgiyle çizilir.
// Şeytan'ın "ışığı" tek parametredir (lum: 1 cennetteki başmelek … 0 sönmüş): film boyunca azalır.
// Birim: h = baş yüksekliği (8 başlık kahraman oranı). Açıların sıfırı aşağıdır; + değer figürün baktığı yöne (facing) doğrudur.
'use strict';
const SF = (() => {
  const { tx, tone, fill } = GR;
  const dirv = (a, f) => [Math.sin(a) * f, Math.cos(a)];
  // poz → eklemler. p: {x, y (kalça ortası), h, facing (±1), lean (gövde eğimi, + öne), twist (0 önden/arkadan … 1 yandan),
  //   shTilt, head (baş eğimi, + yukarı bakar), armN/armF: [üst kol, dirsek bükümü], legN/legF: [uyluk, diz bükümü (− geriye)]}
  //   N = kameraya yakın taraf, F = uzak taraf.
  function rig(p) {
    const h = p.h, f = p.facing || 1, tw = p.twist ?? .35, lean = (p.lean || 0) * f;
    const up = [Math.sin(lean), -Math.cos(lean)], rt = [Math.cos(lean), Math.sin(lean)];
    const hip = [p.x, p.y], shC = [hip[0] + up[0] * 2.2 * h, hip[1] + up[1] * 2.2 * h];
    const sw = 1.95 * h * (1 - .62 * tw), hw = .95 * h * (1 - .55 * tw), st = p.shTilt || 0;
    // yakın taraf bakış yönünün tersinde (¾ görünüşte göğüs bakış yönüne döner)
    const shN = [shC[0] - rt[0] * sw / 2 * f + up[0] * st * h, shC[1] - rt[1] * sw / 2 * f - st * h], shF = [shC[0] + rt[0] * sw / 2 * f - up[0] * st * h, shC[1] + rt[1] * sw / 2 * f + st * h];
    const hpN = [hip[0] - hw / 2 * f, hip[1]], hpF = [hip[0] + hw / 2 * f, hip[1]];
    const nk = [shC[0] + up[0] * .28 * h, shC[1] + up[1] * .28 * h];
    const ha = lean + (p.head || 0) * -f * .0, hd = [nk[0] + up[0] * .62 * h + f * .1 * h, nk[1] + up[1] * .62 * h];
    const arm = (sh, a) => { const a1 = a[0] + lean * f, el = [sh[0] + dirv(a1, f)[0] * 1.45 * h, sh[1] + dirv(a1, f)[1] * 1.45 * h], a2 = a1 + a[1]; return [el, [el[0] + dirv(a2, f)[0] * 1.25 * h, el[1] + dirv(a2, f)[1] * 1.25 * h]]; };
    const leg = (hp, a) => { const kn = [hp[0] + dirv(a[0], f)[0] * 2.0 * h, hp[1] + dirv(a[0], f)[1] * 2.0 * h], a2 = a[0] + a[1]; return [kn, [kn[0] + dirv(a2, f)[0] * 2.0 * h, kn[1] + dirv(a2, f)[1] * 2.0 * h], a2]; };
    const [elN, wrN] = arm(shN, p.armN || [.12, .2]), [elF, wrF] = arm(shF, p.armF || [-.1, .15]);
    const [knN, anN, sN] = leg(hpN, p.legN || [.06, -.06]), [knF, anF, sF] = leg(hpF, p.legF || [-.06, -.04]);
    return { h, f, tw, lean, up, rt, hip, shC, shN, shF, hpN, hpF, nk, hd, elN, wrN, elF, wrF, knN, anN, knF, anF, shinN: sN, shinF: sF, headTilt: p.head || 0 };
  }
  // iki nokta arasında, iki yanında ayrı genişlik profili olan uzuv (wa: bakış yönündeki yan, wb: arka yan)
  function limb(p0, p1, wa, wb, n = 10) {
    const dx = p1[0] - p0[0], dy = p1[1] - p0[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L, A = [], B = [];
    for (let i = 0; i <= n; i++) { const t = i / n, x = p0[0] + dx * t, y = p0[1] + dy * t; A.push([x + nx * wa(t), y + ny * wa(t)]); B.push([x - nx * wb(t), y - ny * wb(t)]); }
    const P = new Path2D(); spline(P, [...A, ...B.reverse()], true, .7); return P;
  }
  const bump = (a, b, c, at = .3) => t => a + (b - a) * t + c * Math.exp(-Math.pow((t - at) / .22, 2));
  // parça doldur: çekirdek ton, ışık yönünde açık kenar (rw), gölge yönünde koyu kenar (dw)
  function part(P, o) {
    const { core, lit, rw, dw, hi, lo, hs } = o;
    fill(P, tone(rw > 0 ? hi : core), hs);
    tx.save(); tx.clip(P);
    if (rw > 0) { tx.save(); tx.translate(-lit[0] * rw, -lit[1] * rw); tx.fillStyle = tone(core); tx.fill(P); tx.restore(); }
    if (dw > 0) { const Q = new Path2D(); Q.rect(-4000, -4000, 12000, 12000); const m = new DOMMatrix().translate(lit[0] * dw, lit[1] * dw); Q.addPath(P, m); tx.fillStyle = tone(lo); tx.fill(Q, 'evenodd'); }
    tx.restore();
  }
  // baş profili (sağa bakar; dir ile aynalanır)
  function headPath(cx, cy, h, dir, tilt) {
    const U = [[-.38, -.1], [-.3, -.38], [-.04, -.5], [.22, -.43], [.33, -.26], [.32, -.13], [.36, -.06], [.47, .08], [.38, .13], [.4, .19], [.35, .24], [.39, .29], [.34, .35], [.36, .44], [.24, .52], [0, .44], [-.12, .36], [-.16, .7], [-.4, .7], [-.4, .2]];
    const c = Math.cos(-tilt * dir), s = Math.sin(-tilt * dir), P = new Path2D();
    spline(P, U.map(([x, y]) => { x *= dir * h; y *= h; return [cx + x * c - y * s, cy + x * s + y * c]; }), true, .55);
    return P;
  }
  // geriye savrulan saç: üç dört büyük, dalgalı tutam (alev gibi), kafatasıyla birleşik
  function hairPath(cx, cy, h, dir, tilt, t, wind = 1, len = 1, seed = 3) {
    const r = rng(seed), P = new Path2D(), c = Math.cos(-tilt * dir), s = Math.sin(-tilt * dir);
    const loc = (x, y) => [cx + (x * dir * c - y * s) * h, cy + (x * dir * s + y * c) * h];
    const k = loc(-.1, -.2); P.moveTo(k[0] + h * .36, k[1]); P.arc(k[0], k[1], h * .36, 0, TAU);
    for (let i = 0; i < 4; i++) {
      const fq = i / 3, b0 = loc(lerp(.1, -.34, fq), lerp(-.5, -.02, fq)), b1 = loc(lerp(-.12, -.42, fq), lerp(-.42, .26, fq));
      const ang = lerp(-.55, .35, fq) + Math.sin(t * .8 + i * 1.7) * .07 * wind, L = h * lerp(.75, 1.05, Math.sin(fq * PI)) * len * (.9 + r() * .2);
      const ax = -Math.cos(ang) * dir, ay = Math.sin(ang), tip = [(b0[0] + b1[0]) / 2 + ax * L, (b0[1] + b1[1]) / 2 + ay * L - h * .1 * Math.sin(t * .6 + i)];
      const m0 = [b0[0] + ax * L * .5, b0[1] + ay * L * .5 - h * .16], m1 = [b1[0] + ax * L * .55, b1[1] + ay * L * .55 + h * .1];
      P.moveTo(b0[0], b0[1]); P.quadraticCurveTo(m0[0], m0[1], tip[0], tip[1]); P.quadraticCurveTo(m1[0], m1[1], b1[0], b1[1]); P.closePath();
    }
    return P;
  }
  // figürü çiz. o: {lum (0..1), lit: [x,y] birim (ışığa doğru), t, anchor, eye (0..1), hair, wind, spear: {grip:'N'|'F', ang, len}, armor (varsayılan true),
  //   skirt (true), waterY (bu çizginin altı çizilmez)}
  function draw(J, o = {}) {
    const h = J.h, f = J.f, lum = o.lum ?? 0, lit = o.lit || [.7, -.7], t = o.t || 0;
    const core = lerp(.05, .93, lum), hi = Math.min(1, core + lerp(.9, .1, lum)), lo = Math.max(0, core - lerp(.03, .62, lum));
    const rw = h * (o.rim ?? .09) * lerp(1, .4, lum), dw = h * lerp(0, .16, lum);
    const an = o.anchor || J.hip, base = { core, lit, rw, dw, hi, lo };
    const HS = (th, id = 5) => ({ th, id, anchor: an });
    const far = Object.assign({}, base, { core: lerp(core, lum > .5 ? core - .25 : core + .06, 1), hi: hi * .85 });
    if (o.waterY != null) { tx.save(); GR.px.save(); const C = new Path2D(); C.rect(-4000, -4000, 12000, 4000 + o.waterY); tx.clip(C); GR.px.clip(C); }
    const parts = [];
    const armP = (sh, el, wr, pr) => {
      part(limb(sh, el, bump(.3 * h, .2 * h, .06 * h, .35), bump(.27 * h, .2 * h, .04 * h, .3)), Object.assign({ hs: HS(.9 * f) }, pr));
      part(limb(el, wr, bump(.2 * h, .13 * h, .05 * h, .25), bump(.2 * h, .12 * h, .03 * h, .2)), Object.assign({ hs: HS(.9 * f) }, pr));
      const a = Math.atan2(wr[1] - el[1], wr[0] - el[0]), H = new Path2D(); H.ellipse(wr[0] + Math.cos(a) * .16 * h, wr[1] + Math.sin(a) * .16 * h, .2 * h, .13 * h, a, 0, TAU);
      part(H, Object.assign({ hs: HS(.9 * f) }, pr));
    };
    const legP = (hp, kn, an2, sa, pr) => {
      part(limb(hp, kn, bump(.42 * h, .27 * h, .06 * h, .35), bump(.4 * h, .25 * h, .05 * h, .3)), Object.assign({ hs: HS(-.7 * f) }, pr));
      part(limb(kn, an2, bump(.25 * h, .13 * h, .03 * h, .2), bump(.24 * h, .12 * h, .1 * h, .3)), Object.assign({ hs: HS(-.7 * f) }, pr));
      const F = new Path2D(), d = dirv(sa, f); // ayak: bakış yönüne uzanan kama
      F.moveTo(an2[0] - f * .14 * h, an2[1] - .1 * h); F.lineTo(an2[0] + f * .16 * h, an2[1] - .12 * h); F.quadraticCurveTo(an2[0] + f * .62 * h, an2[1] + .1 * h, an2[0] + f * .66 * h, an2[1] + .22 * h);
      F.lineTo(an2[0] - f * .2 * h, an2[1] + .22 * h); F.closePath(); part(F, Object.assign({ hs: HS(0) }, pr));
    };
    // mızrak (uzak eldeyse en arkada)
    const spear = sp => { const g = J['wr' + sp.grip], a = (sp.ang ?? 0) * f, d = [Math.sin(a), -Math.cos(a)], L = (sp.len ?? 7.5) * h, up = sp.up ?? .62;
      const top = [g[0] + d[0] * L * up, g[1] + d[1] * L * up], bot = [g[0] - d[0] * L * (1 - up), g[1] - d[1] * L * (1 - up)], n = [d[1], -d[0]], w0 = .045 * h;
      const S = new Path2D(); S.moveTo(bot[0] + n[0] * w0, bot[1] + n[1] * w0); S.lineTo(top[0] + n[0] * w0, top[1] + n[1] * w0); S.lineTo(top[0] - n[0] * w0, top[1] - n[1] * w0); S.lineTo(bot[0] - n[0] * w0, bot[1] - n[1] * w0); S.closePath();
      const tipL = .75 * h, T = new Path2D(); T.moveTo(top[0] + d[0] * tipL, top[1] + d[1] * tipL); T.quadraticCurveTo(top[0] + n[0] * .2 * h + d[0] * .2 * h, top[1] + n[1] * .2 * h + d[1] * .2 * h, top[0] + n[0] * .06 * h, top[1] + n[1] * .06 * h);
      T.lineTo(top[0] - n[0] * .06 * h, top[1] - n[1] * .06 * h); T.quadraticCurveTo(top[0] - n[0] * .2 * h + d[0] * .2 * h, top[1] - n[1] * .2 * h + d[1] * .2 * h, top[0] + d[0] * tipL, top[1] + d[1] * tipL);
      part(S, Object.assign({ hs: HS(a + PI / 2) }, base, { rw: rw * .5 })); part(T, Object.assign({ hs: HS(a) }, base)); };
    if (o.spear && o.spear.grip === 'F') spear(o.spear);
    armP(J.shF, J.elF, J.wrF, far);
    if (o.legs !== false) legP(J.hpF, J.knF, J.anF, J.shinF, far);
    if (o.legs !== false) legP(J.hpN, J.knN, J.anN, J.shinN, base);
    // gövde: omuz başları, göğüs, bel; boyun ve trapez
    const { shN, shF, hpN, hpF, nk, up, rt } = J, sc = J.shC, hipC = J.hip;
    const P = (al, sd) => [sc[0] - up[0] * al * h + rt[0] * sd * h, sc[1] - up[1] * al * h + rt[1] * sd * h]; // al: omuzdan aşağı (baş), sd: yana (baş)
    const swH = Math.hypot(shF[0] - shN[0], shF[1] - shN[1]) / h / 2, hwH = Math.hypot(hpF[0] - hpN[0], hpF[1] - hpN[1]) / h / 2;
    const T = new Path2D();
    spline(T, [P(-.3, 0), P(-.22, swH * .5), P(-.02, swH + .28), P(.35, swH + .22), P(1.0, swH * .92 + .06), P(1.55, swH * .74 + .06), P(2.0, hwH + .3), P(2.2, hwH + .34),
      P(2.2, -hwH - .34), P(2.0, -hwH - .3), P(1.55, -swH * .74 - .06), P(1.0, -swH * .92 - .06), P(.35, -swH - .22), P(-.02, -swH - .28), P(-.22, -swH * .5)], true, .75);
    const Nk = limb(nk, [J.hd[0], J.hd[1] + .2 * h], () => .2 * h, () => .2 * h, 4);
    part(Nk, Object.assign({ hs: HS(.9 * f) }, base));
    part(T, Object.assign({ hs: HS(.5 * f, 9) }, base));
    // etek: belden uyluk ortasına açılan şeritler (pteruges)
    if (o.skirt !== false && o.legs !== false) {
      const K = new Path2D(), n = 7, y0 = 1.95, y1 = 3.05, w0 = hwH + .3, w1 = hwH + .52, pts = [P(y0, -w0)];
      for (let i = 0; i < n; i++) { const a = -w1 + (i / n) * 2 * w1, b = -w1 + ((i + 1) / n) * 2 * w1, sw2 = Math.sin(t * 1.1 + i) * .02; pts.push(P(y1 - .05 + sw2, a + .02), P(y1 + .1 + sw2, (a + b) / 2), P(y1 - .05 + sw2, b - .02), P(y1 - .22, b)); }
      pts.push(P(y0, w0)); poly(K, pts, true); part(K, Object.assign({ hs: HS(PI / 2 + J.lean, 9) }, base));
      parts.push({ k: 'skirt', n, y0, y1, w0, w1 });
    }
    // baş ve saç
    const hh = h * (o.headScale ?? 1.04), tilt = (o.tilt ?? J.headTilt);
    if (o.hair !== false) part(hairPath(J.hd[0], J.hd[1], hh, f, tilt, t, o.wind ?? 1, o.hair ?? 1, o.seed || 3), Object.assign({ hs: HS(-.4 * f) }, base, { rw: rw * .7 }));
    part(headPath(J.hd[0], J.hd[1], hh, f, tilt), Object.assign({ hs: HS(1.0 * f) }, base));
    armP(J.shN, J.elN, J.wrN, base);
    if (o.spear && o.spear.grip !== 'F') spear(o.spear);
    if (o.waterY != null) { tx.restore(); GR.px.restore(); }
    // ── üst katman: zırh çizgileri ve göz (basmadan sonra keskin kalır) ──
    const ox = GR.ox, lc = lum < .5 ? GR.paperCol : GR.inkCol;
    ox.save(); if (o.waterY != null) { const C = new Path2D(); C.rect(-4000, -4000, 12000, 4000 + o.waterY); ox.clip(C); }
    ox.strokeStyle = lc; ox.lineCap = 'round'; ox.lineJoin = 'round'; ox.lineWidth = Math.max(1.4, h * .028); ox.globalAlpha = lerp(.8, .7, lum);
    if (o.armor !== false) {
      const L2 = (a, b, c) => { ox.beginPath(); ox.moveTo(a[0], a[1]); if (c) ox.quadraticCurveTo(c[0], c[1], b[0], b[1]); else ox.lineTo(b[0], b[1]); ox.stroke(); };
      ox.save(); ox.clip(T);
      L2(P(.3, -swH - .3), P(.3, swH + .3), P(.62, 0));                                   // göğüslük üst kavsi
      L2(P(.1, 0), P(1.45, 0));                                                           // orta sırt
      for (let k = 0; k < 3; k++) L2(P(1.5 + k * .17, -swH - .2), P(1.5 + k * .17, swH + .2), P(1.58 + k * .17, 0)); // karın levhaları
      for (const s of [-1, 1]) L2(P(.42, s * (swH - .12)), P(-.02, s * (swH + .3)), P(.5, s * (swH + .34)));   // omuzluk kenarı
      ox.restore();
      const sk = parts.find(q => q.k === 'skirt');
      if (sk) for (let i = 1; i < sk.n; i++) { const a = -sk.w1 + (i / sk.n) * 2 * sk.w1; L2(P(sk.y0 + .1, a * (sk.w0 / sk.w1)), P(sk.y1 - .12, a)); }
      for (const [e, w] of [[J.elN, J.wrN], [J.elF, J.wrF]]) { const m = [lerp(e[0], w[0], .55), lerp(e[1], w[1], .55)], a = Math.atan2(w[1] - e[1], w[0] - e[0]) + PI / 2; L2([m[0] - Math.cos(a) * .15 * h, m[1] - Math.sin(a) * .15 * h], [m[0] + Math.cos(a) * .15 * h, m[1] + Math.sin(a) * .15 * h]); } // bileklik
    }
    const eo = o.eye ?? (lum < .5 ? 1 : 0);
    if (eo > 0) { const c = Math.cos(-tilt * f), s = Math.sin(-tilt * f), ex = J.hd[0] + (.2 * f * c + .07 * s) * hh, ey = J.hd[1] + (.2 * f * s - .07 * c) * hh;
      ox.globalAlpha = 1; ox.fillStyle = GR.paperCol; ox.beginPath(); ox.ellipse(ex, ey, hh * .065, hh * .028 * eo, -tilt * f, 0, TAU); ox.fill(); }
    ox.restore();
    return { T };
  }
  return { rig, draw, limb, part, headPath, hairPath };
})();
