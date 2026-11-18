// boya.js (Mary Stuart): ton resmi araç kutusu. Sahne gri değerlerle boyanır (1 = kâğıt beyazı, 0 = mürekkep);
// sessiz film motorunun Redraw geçişi onu mürekkep çizgisi, beş yıkama basamağı ve taramaya çevirir.
// Kural (tarif): değer yapısı net olsun (en az üç değer); yumuşak ışık geçişleri serbest, doku yok (doku motorun işi).
// Tek renk: G.kirmizi(...) yalnız RC katmanına boyar (Mary'nin kırmızısı). Rastgelelik yalnız rng(seed).
'use strict';
const BOYA = (() => {
  const TAU = Math.PI * 2, PI = Math.PI;
  function rng(seed) { let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const hash = n => { const s = Math.sin(n * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
  const noise1 = (x, s = 0) => { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return lerp(hash(i + s * 57.3), hash(i + 1 + s * 57.3), u) * 2 - 1; };
  const gri = (v, a = 1) => { const c = Math.round(clamp(v) * 255); return a >= 1 ? `rgb(${c},${c},${c})` : `rgba(${c},${c},${c},${a})`; };
  function spline(P, pts, closed = true, k = .8) {
    const n = pts.length; if (n < 2) return; const Q = i => closed ? pts[(i + n) % n] : pts[clamp(i, 0, n - 1)];
    P.moveTo(pts[0][0], pts[0][1]); const last = closed ? n : n - 1;
    for (let i = 0; i < last; i++) { const p0 = Q(i - 1), p1 = Q(i), p2 = Q(i + 1), p3 = Q(i + 2);
      P.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k, p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k, p2[0], p2[1]); }
    if (closed) P.closePath();
  }
  const pathOf = (pts, closed = true, k = .8) => { const P = new Path2D(); spline(P, pts, closed, k); return P; };
  const polyP = pts => { const P = new Path2D(); P.moveTo(...pts[0]); for (const p of pts.slice(1)) P.lineTo(...p); P.closePath(); return P; };
  const ell = (c, rx, ry, a = 0) => { const P = new Path2D(); P.ellipse(c[0], c[1], rx, ry, a, 0, TAU); return P; };
  function limb(p0, p1, w0, w1) {
    const dx = p1[0] - p0[0], dy = p1[1] - p0[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L, A = [], B = [];
    for (let i = 0; i <= 6; i++) { const t = i / 6, w = lerp(w0, w1, t) / 2, x = p0[0] + dx * t, y = p0[1] + dy * t; A.push([x + nx * w, y + ny * w]); B.push([x - nx * w, y - ny * w]); }
    const P = pathOf([...A, ...B.reverse()], true, .7); P.addPath(ell(p0, w0 / 2, w0 / 2)); P.addPath(ell(p1, w1 / 2, w1 / 2)); return P;
  }

  // ── figür (1560–1587): koyu kütle; yüz yok, kimlik siluetten ──
  // o: {x, y (ayak), s (boy px), f (±1 bakış), kind: mary|eliz|kadin|erkek, poz: ayakta|yuru|otur|diz, walk, lean, head, kol, t, wind, veil, pelerin, v (ton), kirmizi: 'etek'|'astar'}
  function figur(G, o) {
    const g = G.g, s = o.s, f = o.f || 1, X = o.x, Y = o.y, kind = o.kind || 'mary', poz = o.poz || 'ayakta', t = o.t || 0, wind = o.wind ?? .35;
    const T = (x, y) => [X + x * s * f, Y + y * s];
    const ph = o.walk || 0, sw = poz === 'yuru' ? Math.sin(ph * TAU) : 0, bob = poz === 'yuru' ? Math.abs(Math.cos(ph * TAU)) * .006 : 0;
    const W0 = poz === 'otur' ? [-.02, -.36] : poz === 'diz' ? [0, -.34] : [-.008, -.585 + bob];
    const lean = (o.lean || 0) + (poz === 'otur' ? .14 : 0), cl = Math.cos(lean), sl = Math.sin(lean);
    const UB = (x, y) => { const dx = x + .008, dy = y + .585; return T(W0[0] + dx * cl - dy * sl, W0[1] + dx * sl + dy * cl); };
    const parts = [], female = kind !== 'erkek'; let veil = null, fan = null, etek = null, astar = null;
    if (female) {
      if (kind === 'eliz') etek = pathOf([[.05, -.6], [.16, -.605], [.215, -.595], [.225, -.575], [.21, -.555], [.19, -.53], [.2, -.25], [.23, -.02], [.15, .004], [0, .008], [-.15, .004], [-.23, -.02], [-.2, -.25], [-.19, -.53], [-.21, -.555], [-.225, -.575], [-.215, -.595], [-.16, -.605], [-.06, -.6]].map(([x, y]) => T(x, y)), true, .45);
      else if (poz === 'otur') etek = pathOf([[.03, -.38], [.12, -.37], [.2, -.355], [.235, -.33], [.24, -.25], [.25, -.12], [.27, -.01], [.12, .005], [-.05, .004], [-.17, -.005], [-.15, -.12], [-.12, -.26], [-.09, -.36], [-.04, -.39]].map(([x, y]) => T(x, y)), true, .6);
      else if (poz === 'diz') etek = pathOf([[.04, -.34], [.1, -.28], [.16, -.16], [.22, -.05], [.27, .0], [.1, .008], [-.1, .008], [-.26, .0], [-.2, -.08], [-.13, -.2], [-.07, -.31], [-.04, -.345]].map(([x, y]) => T(x, y)), true, .6);
      else { const a = sw * .016, kz = kind === 'kadin' ? .82 : 1;
        etek = pathOf([[.052, -.585], [.08, -.46], [.115 * kz + a * .3, -.3], [.155 * kz + a * .6, -.12], [.19 * kz + a, -.02], [.19 * kz + a, .004], [.08, .009], [-.04, .009], [-.16 * kz, .005], [-.25 * kz - a, -.002], [-.29 * kz - a * 1.3, -.012], [-.21 * kz - a, -.07], [-.15 * kz - a * .6, -.24], [-.11, -.42], [-.066, -.585]].map(([x, y]) => T(x, y)), true, .55); }
      parts.push(etek);
      parts.push(pathOf([[-.066, -.585], [-.076, -.66], [-.08, -.74], [-.068, -.795], [-.03, -.81], [.028, -.806], [.06, -.775], [.07, -.72], [.066, -.67], [.05, -.61], [.034, -.55], [.016, -.585]].map(([x, y]) => UB(x, y)), true, .6));
      if (kind === 'eliz') parts.push(pathOf([[-.05, -.6], [.0, -.5], [.05, -.6]].map(([x, y]) => UB(x, y)), true, .3));
    } else {
      const th = poz === 'yuru' ? sw * .32 : (poz === 'otur' ? 1.35 : .04), th2 = poz === 'yuru' ? -sw * .32 : (poz === 'otur' ? 1.35 : -.04);
      const hip = [0, -.5], leg = (a, k2, sd) => { const kn = [hip[0] + Math.sin(a) * .25 + sd * .02, hip[1] + Math.cos(a) * .25], an = [kn[0] + Math.sin(a + k2) * .24, kn[1] + Math.cos(a + k2) * .24]; return [kn, an]; };
      const k2a = poz === 'otur' ? -1.35 : (poz === 'yuru' ? -Math.max(0, -sw) * .5 : 0), k2b = poz === 'otur' ? -1.35 : (poz === 'yuru' ? -Math.max(0, sw) * .5 : 0);
      for (const [a, k2, sd] of [[th2, k2b, -1], [th, k2a, 1]]) {
        const [kn, an] = leg(a, k2, sd);
        parts.push(limb(T(hip[0] + sd * .02, hip[1]), T(kn[0], kn[1]), .065 * s, .045 * s), limb(T(kn[0], kn[1]), T(an[0], an[1]), .045 * s, .03 * s));
        parts.push(pathOf([[an[0] - .02, an[1] - .01], [an[0] + .07, an[1] - .005], [an[0] + .075, an[1] + .01], [an[0] - .025, an[1] + .01]].map(([x, y]) => T(x, y)), true, .5));
      }
      parts.push(pathOf([[-.075, -.6], [.075, -.6], [.1, -.54], [.09, -.45], [.03, -.43], [-.03, -.43], [-.09, -.45], [-.1, -.54]].map(([x, y]) => T(x, y)), true, .7));
      parts.push(pathOf([[-.08, -.6], [-.09, -.7], [-.1, -.8], [-.07, -.835], [.0, -.84], [.07, -.83], [.1, -.8], [.09, -.7], [.08, -.6], [.06, -.55], [-.06, -.55]].map(([x, y]) => UB(x, y)), true, .6));
    }
    const nk = female ? [.003, -.82] : [.003, -.855];
    parts.push(pathOf([[nk[0] - .022, nk[1] + .02], [nk[0] + .026, nk[1] + .02], [nk[0] + .026, nk[1] - .03], [nk[0] - .022, nk[1] - .03]].map(([x, y]) => UB(x, y)), true, .5));
    const hc = female ? [.012, -.888] : [.012, -.92], hd = o.head || 0, chs = Math.cos(hd), shs = Math.sin(hd);
    const HB = (x, y) => UB(hc[0] + x * chs - y * shs, hc[1] + x * shs + y * chs);
    parts.push(pathOf([[-.047, -.012], [-.04, -.045], [-.012, -.06], [.022, -.055], [.042, -.036], [.05, -.016], [.058, .004], [.05, .01], [.052, .02], [.046, .03], [.044, .042], [.03, .052], [.012, .055], [-.012, .048], [-.035, .03]].map(([x, y]) => HB(x, y)), true, .8));
    if (kind === 'mary') {
      parts.push(pathOf([[.056, -.04], [.054, -.078], [.036, -.09], [.018, -.074], [.0, -.098], [-.034, -.094], [-.062, -.066], [-.076, -.024], [-.072, .024], [-.056, .044], [-.046, .004], [-.034, -.04], [-.006, -.056], [.03, -.052]].map(([x, y]) => HB(x, y)), true, .7));   // kalp başlık (attifet)
      const vl = o.veil ?? .85, wv = k => (Math.sin(t * 1.1 + k * 2.1) * .018 + .02) * wind * k, stand = poz === 'ayakta' || poz === 'yuru';
      const VP = ([x, y]) => stand ? UB(x, y) : UB(x * .9, lerp(y, -.45, .5));
      if (vl > 0) veil = pathOf([...[[-.02, -.075], [-.06, -.06], [-.075, -.02]].map(([x, y]) => HB(x, y)), ...[[-.1 - wv(.2), -.8], [-.15 - wv(.4), -.62], [-.2 - wv(.6), -.4], [-.25 - wv(.8), -.18], [-.29 - wv(1), -.02 + (1 - vl) * .4]].map(VP), ...[[-.12 - wv(.9), -.02 + (1 - vl) * .4], [-.1 - wv(.6), -.3], [-.07 - wv(.3), -.6], [-.05, -.78]].map(VP), HB(-.02, .03)], true, .6);
      parts.push(ell(UB(.004, -.822), .046 * s, .015 * s));
    } else if (kind === 'eliz') {
      const c = UB(-.004, -.84), P = new Path2D(); P.moveTo(c[0], c[1]);
      for (let i = 0; i <= 24; i++) { const a = PI + i / 24 * PI, r = (.115 + .008 * Math.cos(i * PI)) * s; P.lineTo(c[0] + Math.cos(a) * r, c[1] + Math.sin(a) * r * 1.05); }
      P.closePath(); fan = P;
      parts.push(ell(UB(.004, -.822), .05 * s, .017 * s));
      parts.push(pathOf([[-.034, -.056], [-.03, -.09], [-.012, -.072], [.004, -.098], [.02, -.072], [.036, -.088], [.04, -.052]].map(([x, y]) => HB(x, y)), true, .35));
      for (const d of [-1, 1]) parts.push(ell(UB(d * .07 * f - .004, -.75), .055 * s, .065 * s));
    } else if (kind === 'kadin') {
      parts.push(pathOf([[.05, -.04], [.03, -.072], [-.02, -.078], [-.058, -.05], [-.07, .01], [-.08, .07], [-.05, .08], [-.03, .03], [-.01, -.03], [.03, -.045]].map(([x, y]) => HB(x, y)), true, .7));
    } else {
      if (o.sapka !== false) { parts.push(pathOf([[-.085, -.03], [-.07, -.055], [-.02, -.07], [.05, -.068], [.095, -.05], [.1, -.035], [.04, -.04], [-.03, -.035]].map(([x, y]) => HB(x, y)), true, .7)); parts.push(pathOf([[-.03, -.06], [-.07, -.1], [-.1, -.11], [-.085, -.085], [-.05, -.06]].map(([x, y]) => HB(x, y)), true, .7)); }
      if (o.sakal) parts.push(pathOf([[.045, .025], [.05, .055], [.03, .085], [.0, .07], [-.01, .04]].map(([x, y]) => HB(x, y)), true, .7));
      parts.push(ell(UB(.003, -.84), .042 * s, .012 * s));
      if (o.pelerin !== false) { const wv = Math.sin(t * 1.2) * .012 * wind; parts.push(pathOf([[-.07, -.83], [-.12 - wv, -.7], [-.15 - wv * 2, -.5], [-.16 - wv * 3, -.32], [-.06, -.36], [-.03, -.6], [.0, -.82]].map(([x, y]) => UB(x, y)), true, .6)); }
    }
    // kollar
    const shN = female ? [-.004, -.778] : [.0, -.8], kol = o.kol || 'onde', ln = female ? [.15, .13] : [.17, .15];
    const KOL = { onde: [.1, -1.0], yan: [.06, -.12], kaldir: [.5, -1.75], uzat: [1.1, -.25], dua: [.2, -2.05], yaz: [.75, -1.0], pencere: [.9, -.7], tut: [.3, -1.2], kurek: [1.3, -.6], yanak: [.35, -2.6], dans: [2.2, -.5], isaret: [1.5, -.05], egik: [-.1, -.3] }[kol] || [.1, -1.0];
    const a1 = KOL[0], el = [shN[0] + Math.sin(a1) * ln[0], shN[1] + Math.cos(a1) * ln[0]], wr = [el[0] + Math.sin(a1 - KOL[1]) * ln[1], el[1] + Math.cos(a1 - KOL[1]) * ln[1]];
    parts.push(limb(UB(...shN), UB(...el), (female ? .064 : .055) * s, .03 * s), limb(UB(...el), UB(...wr), (female ? .04 : .032) * s, .024 * s), ell(UB(wr[0] + Math.sin(a1 - KOL[1]) * .01, wr[1] + Math.cos(a1 - KOL[1]) * .01), .014 * s, .012 * s, a1 - KOL[1]));
    if (['dua', 'onde', 'yan', 'pencere', 'yaz'].includes(kol)) { const b1 = kol === 'yan' ? -.05 : a1 - .1, elF = [shN[0] - .015 + Math.sin(b1) * ln[0], shN[1] + Math.cos(b1) * ln[0]], wrF = [elF[0] + Math.sin(b1 - KOL[1]) * ln[1], elF[1] + Math.cos(b1 - KOL[1]) * ln[1]]; parts.push(limb(UB(...elF), UB(...wrF), .028 * s, .02 * s)); }
    if (o.pelerin === true && female) {
      const wv = k => Math.sin(t * 1.3 + k * 1.7) * .02 * wind * k;
      parts.push(pathOf([[.02, -.975], [.062, -.955], [.078, -.9], [.07, -.85], [.085, -.8], [.1, -.7], [.13, -.5], [.165 + wv(.6), -.25], [.2 + wv(1), -.02], [-.27 - wv(1), -.01], [-.23 - wv(.8), -.3], [-.17 - wv(.5), -.6], [-.11, -.86], [-.075, -.95], [-.03, -.985]].map(([x, y]) => UB(x, y)), true, .55));
      astar = pathOf([[.07, -.86], [.09, -.74], [.115, -.5], [.15 + wv(.6), -.25], [.185 + wv(1), -.03], [.13, -.03], [.08, -.3], [.05, -.6], [.045, -.8]].map(([x, y]) => UB(x, y)), true, .6);
    }
    // boya: önce gazlı bez (tül, yelpaze yaka), sonra koyu kütle
    if (veil) { g.save(); g.fillStyle = gri(o.veilV ?? .7, o.veilA ?? .5); g.fill(veil); g.strokeStyle = gri(.92, .7); g.lineWidth = Math.max(1, s * .004); g.stroke(veil); g.restore(); }
    if (fan) { g.fillStyle = gri(o.veilV ?? .72); g.fill(fan); }
    g.fillStyle = gri(o.v ?? .1); for (const P of parts) g.fill(P);
    // kırmızı kumaşın ton resmi orta değerde olur (kırmızı çizimle çarpılır; koyu kalırsa okunmaz)
    if (o.kirmizi === 'etek' && etek) { const a = o.kirmiziA ?? 1; if (a > 0) { g.fillStyle = gri(.36, a); g.fill(etek); } G.kirmizi(etek, a); }
    if (o.kirmizi === 'astar' && astar) { const a = o.kirmiziA ?? 1; if (a > 0) { g.fillStyle = gri(.4, a); g.fill(astar); } G.kirmizi(astar, a); }
    return { T, UB, HB, etek, astar };
  }

  function bulutCiz(G, x, y, w, h, o = {}) { const g = G.g, q = rng(o.seed || 3), n = o.n || Math.round(w / h * 5), dr = o.drift || 0, bl = o.blur ?? h * .12;
      g.save(); if (!G.yumusakYok) g.filter = `blur(${bl}px)`;
      // gövde (alt, koyu) sonra ışık (üst, açık): iki katman, düzensiz dağılım
      for (const [kat, v, dy, k] of [[0, o.govde ?? .58, .12, 1], [1, o.isik ?? .9, -.12, .72]]) {
        g.fillStyle = gri(v);
        for (let i = 0; i < n; i++) { const fx = q(), env = Math.pow(Math.sin(PI * fx), .7), cx = x - w / 2 + fx * w + dr * (1 + kat * .1), cy = y + (q() - .5) * h * .5 * env + dy * h - env * h * .18, rr = h * (.18 + q() * .3) * (.4 + .6 * env) * k;
          g.beginPath(); g.ellipse(cx, cy, rr * (1.3 + q() * .8), rr * .75, 0, 0, TAU); g.fill(); }
      }
      g.restore(); }
  const BULUT_ON = {}, GRI_ON = new Map(); let YUM = null;
  // gri + kontrast süzgeci her karede pahalı: görüntü başına bir kez uygulanır
  function griOn(im, k, b) { const key = (im.src || '') + '|' + k + '|' + b; let c = GRI_ON.get(key); if (c) return c;
    c = document.createElement('canvas'); c.width = im.naturalWidth || im.width; c.height = im.naturalHeight || im.height; const x = c.getContext('2d'); x.filter = `grayscale(1) contrast(${k}) brightness(${b})`; x.drawImage(im, 0, 0); GRI_ON.set(key, c); return c; }
  // yumuşak gölge (bulanık dikdörtgen) hazır doku: ölçeklenerek çizilir
  let GOLGE = null; function golge(g, x, y, w, h, a = .6) { if (!GOLGE) { GOLGE = document.createElement('canvas'); GOLGE.width = GOLGE.height = 256; const q = GOLGE.getContext('2d'); q.filter = 'blur(22px)'; q.fillStyle = '#000'; q.fillRect(56, 56, 144, 144); }
    g.save(); g.globalAlpha = a; g.drawImage(GOLGE, x - w * 56 / 144, y - h * 56 / 144, w * 256 / 144, h * 256 / 144); g.restore(); }
  // ── bağlam ──
  function ctx(g, r, st) {
    const G = { g, r, st, renkVar: false, gri, rng, noise1, pathOf, polyP, ell, TAU, PI };
    G.kamera = (cx = 720, cy = 540, z = 1) => { for (const c of [g, r]) c.setTransform(z, 0, 0, z, 720 - cx * z, 540 - cy * z); };
    G.kirmizi = (P, a = 1) => { G.renkVar = true; r.save(); r.globalAlpha = a; r.fillStyle = 'rgb(176,22,30)'; r.fill(P); r.restore(); };
    G.zemin = v => { g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = gri(v); g.fillRect(0, 0, 1440, 1080); g.restore(); };
    G.dik = (x, y, w, h, v) => { g.fillStyle = gri(v); g.fillRect(x, y, w, h); };
    // gök: dikey geçiş + ışık lekesi
    G.gok = (y1, o = {}) => { const gr = g.createLinearGradient(0, -200, 0, y1); gr.addColorStop(0, gri(o.ust ?? .55)); gr.addColorStop(1, gri(o.alt ?? .9)); g.fillStyle = gr; g.fillRect(-2000, -2000, 6000, y1 + 2000);
      if (o.isik) { const [x, y, rr, v] = o.isik, rg2 = g.createRadialGradient(x, y, 0, x, y, rr); rg2.addColorStop(0, gri(v ?? 1, 1)); rg2.addColorStop(1, gri(v ?? 1, 0)); g.fillStyle = rg2; g.fillRect(x - rr, y - rr, rr * 2, rr * 2); } };
    // bulut kümesi: yumuşak lekeler; alt yanı koyu, ışık yanı açık

    // bulut örtüsü: ufka doğru incelen katmanlar. Bulanıklaştırma pahalı (yazılımsal çizim): katman bir kez önbelleğe çizilir, sonra kaydırılır
    G.bulutlar = (y0, y1, o = {}) => { const key = JSON.stringify([y0, y1, { ...o, drift: 0 }]); let c = BULUT_ON[key];
      if (!c) { const K = 6; c = document.createElement('canvas'); c.width = 3200 / K; c.height = 1300 / K; const g2 = c.getContext('2d'); g2.scale(1 / K, 1 / K); g2.translate(900, 300);
        const G2 = { ...G, g: g2, yumusakYok: true }; const k = o.n ?? 5;
        for (let i = 0; i < k; i++) { const u = i / Math.max(1, k - 1), yy = lerp(y0, y1, u), hh = lerp(o.h0 ?? 170, o.h1 ?? 50, u), q = rng((o.seed || 1) * 31 + i);
          bulutCiz(G2, 720 + (q() - .5) * 900, yy, lerp(o.w0 ?? 1500, o.w1 ?? 2200, u), hh, { seed: (o.seed || 1) * 7 + i, govde: lerp(o.govde ?? .55, o.ufukV ?? .82, u), isik: lerp(o.isik ?? .9, .95, u) }); }
        BULUT_ON[key] = c; }
      g.save(); g.imageSmoothingQuality = 'high'; g.drawImage(c, -900 + ((o.drift || 0) % 600), -300, 3200, 1300); g.restore(); };
    G.bulut = (x, y, w, h, o = {}) => bulutCiz(G, x, y, w, h, o);
    G.kirmiziT = (P, a = 1) => { G.renkVar = true; r.save(); r.setTransform(g.getTransform()); r.globalAlpha = a; r.fillStyle = 'rgb(176,22,30)'; r.fill(P); r.restore(); };   // yol g'nin o anki dönüşümünde
    G.kirmiziCiz = fn => { G.renkVar = true; r.save(); r.fillStyle = r.strokeStyle = 'rgb(176,22,30)'; fn(r); r.restore(); };
    // deniz: ufuktan öne koyulaşan yüzey + hareketli dalga çizgileri (Redraw onları tarama yapar)
    G.deniz = (y0, y1, o = {}) => { const t = o.t || 0, gr = g.createLinearGradient(0, y0, 0, y1); gr.addColorStop(0, gri(o.ufuk ?? .78)); gr.addColorStop(1, gri(o.on ?? .35)); g.fillStyle = gr; g.fillRect(-2000, y0, 6000, y1 - y0 + 2000);
      const q = rng(o.seed || 9), D = y1 - y0;
      for (let i = 0; i < (o.n ?? 90); i++) { const u = Math.pow(q(), 1.6), yy = y0 + 4 + u * D, ln = lerp(30, 260, u) * (.5 + q()), xx = ((q() * 2600 + t * (8 + u * 30) * (q() < .5 ? 1 : -.4)) % 2600) - 600, th = lerp(1.2, 5, u);
        g.fillStyle = gri(q() < .5 ? (o.ufuk ?? .78) * .7 + .2 * u : .95, .55 + .4 * u); g.beginPath(); g.ellipse(xx, yy + Math.sin(t * .8 + i) * 2 * u, ln / 2, th, 0, 0, TAU); g.fill(); }
      if (o.yansima) { const [x, w, v] = o.yansima; for (let k = 0; k < 26; k++) { const u = k / 26, yy = y0 + 3 + Math.pow(u, 1.4) * D * .7, ww = w * (1 - .5 * u) * (.6 + .4 * Math.sin(t * .7 + k * 1.7)); g.fillStyle = gri(v ?? .98, .9 * (1 - u)); g.fillRect(x - ww / 2 + noise1(k * .4 + t * .3, 3) * 20, yy, ww, lerp(2, 6, u)); } } };
    // uzak kıyı / dağ sırtı
    G.kiyi = (x0, x1, y, h, o = {}) => { const q = rng(o.seed || 4), pts = [[x0, y + 8]], n = 28;
      for (let i = 0; i <= n; i++) { const f = i / n, m = Math.pow(Math.sin(PI * clamp((f - (o.d0 ?? 0)) / ((o.d1 ?? 1) - (o.d0 ?? 0)))), 1.2); pts.push([lerp(x0, x1, f), y - h * (.15 + .85 * m * (.55 + .45 * noise1(f * (o.k || 4) + (o.seed || 0), 2))) - q() * h * .05]); }
      pts.push([x1, y + 8]); g.fillStyle = gri(o.v ?? .45); g.fill(pathOf(pts, true, .5)); };
    // gerçek görsel (kamu malı): gri, kontrast; kırpma {x,y,w,h} kaynağın pikselinde; hedef kutu (x, y, w, h)
    G.foto = (im, x, y, w, h, o = {}) => { if (!im) return; const c = o.crop || { x: 0, y: 0, w: im.naturalWidth || im.width, h: im.naturalHeight || im.height };
      g.save(); if (o.clip) g.clip(o.clip); g.drawImage(griOn(im, o.kontrast ?? 1.1, o.parlak ?? 1.05), c.x, c.y, c.w, c.h, x, y, w, h); g.restore(); };
    // tekne: açık balıkçı teknesi, tek direk, kare yelken; kürekler; kişiler (figur)
    G.tekne = o => { const s = o.s, f = o.f || 1, X = o.x, Y = o.y, t = o.t || 0, rk = Math.sin(t * 1.3) * .025, sail = o.sail ?? 1;
      const T = (x, y) => { const c = Math.cos(rk), sn = Math.sin(rk), qx = x * c - y * sn, qy = x * sn + y * c; return [X + qx * s * f, Y + qy * s]; };
      g.save(); g.strokeStyle = gri(.08); g.lineCap = 'round'; g.lineWidth = Math.max(3, s * .014);
      for (const k of [-.15, .08]) { const a = Math.sin((o.oar ?? t * 1.2) * TAU + k * 5) * .35, p0 = T(k, -.06), p1 = T(k - .12 * Math.cos(a), .1 + .05 * Math.sin(a)); g.beginPath(); g.moveTo(...p0); g.lineTo(...p1); g.stroke(); }
      g.restore();
      for (const k of (o.kisi || [])) { const p = T(k.x, -.035); figur(G, { ...k, x: p[0], y: p[1] + s * (k.dip ?? .05), s: s * (k.h ?? .3), f: k.f ?? f, t, wind: .6 }); }
      g.fillStyle = gri(.12); g.fill(pathOf([[-.5, -.08], [-.3, -.04], [0, -.035], [.3, -.045], [.52, -.12], [.48, -.06], [.38, .02], [.1, .055], [-.25, .05], [-.45, .02]].map(([x, y]) => T(x, y)), true, .6));
      if (o.direk !== false) { const m0 = T(.05, -.04), m1 = T(.05, -.78); g.strokeStyle = gri(.1); g.lineWidth = Math.max(3, s * .014); g.beginPath(); g.moveTo(...m0); g.lineTo(...m1); g.stroke(); }
      if (sail > 0) { const b = .1 * sail * (1 + .12 * Math.sin(t * 2.1)), top = -.74, bot = -.2;
        g.fillStyle = gri(o.yelken ?? .8); g.fill(pathOf([[.05, top], [.25 + b, top + .02], [.31 + b * 1.4, (top + bot) / 2], [.27 + b, bot], [.05, bot + .02], [-.11 - b * .5, bot], [-.15 - b * .8, (top + bot) / 2], [-.1 - b * .4, top + .02]].map(([x, y]) => T(x, y)), true, .5)); } };
    // taş duvar + derin pencere oyuğu; içi dış manzara (dis fonksiyonu, kırpılır)
    G.pencere = o => { const { x, y, w, h } = o, a = w / 2, d = o.d ?? 90;
      const ac = new Path2D(); ac.moveTo(x - a, y + h); ac.lineTo(x - a, y + a); ac.arc(x, y + a, a, PI, 0); ac.lineTo(x + a, y + h); ac.closePath();
      g.save(); g.clip(ac); if (o.dis) o.dis(); g.restore();
      const wall = new Path2D(); wall.rect(-2000, -2000, 6000, 6000); wall.addPath(ac); g.fillStyle = gri(o.duvar ?? .16); g.fill(wall, 'evenodd');
      const a2 = a + d * .5, band = new Path2D(); band.moveTo(x - a2, y + h + d * .3); band.lineTo(x - a2, y + a); band.arc(x, y + a, a2, PI, 0); band.lineTo(x + a2, y + h + d * .3); band.lineTo(x + a, y + h); band.lineTo(x + a, y + a); band.arc(x, y + a, a, 0, PI, true); band.lineTo(x - a, y + h); band.closePath();
      const lg = g.createLinearGradient(x - a2, 0, x + a2, 0); lg.addColorStop(0, gri(.72)); lg.addColorStop(.5, gri(.5)); lg.addColorStop(1, gri(.24)); g.fillStyle = lg; g.fill(band);
      g.fillStyle = gri(.8); g.fill(polyP([[x - a2 - 10, y + h + d * .3], [x + a2 + 10, y + h + d * .3], [x + a + 6, y + h], [x - a - 6, y + h]]));
      // ışık: pencereden içeri düşen yumuşak leke
      const lgt = g.createRadialGradient(x, y + h + 260, 20, x, y + h + 260, 520); lgt.addColorStop(0, gri(.5, .5)); lgt.addColorStop(1, gri(.5, 0)); g.fillStyle = lgt; g.fillRect(x - 600, y + h, 1200, 900);
      return ac; };
    // mektup kâğıdı + el yazısı satırları (okunur metin)
    G.mektup = (x, y, w, h, ang, o = {}) => { g.save(); g.translate(x, y); g.rotate(ang); g.fillStyle = gri(o.v ?? .96); g.fillRect(-w / 2, -h / 2, w, h);
      g.fillStyle = gri(.12); g.font = `italic 500 ${o.px || 44}px "Cormorant Garamond"`; g.textBaseline = 'alphabetic';
      (o.yazi || []).forEach((l, i) => { const k = clamp((o.prog ?? 1) * o.yazi.length - i); if (k <= 0) return; g.save(); g.beginPath(); g.rect(-w / 2, -h / 2, 70 + (w - 90) * k, h); g.clip(); g.fillText(l, -w / 2 + 70, -h / 2 + 110 + i * (o.lh || 62)); g.restore(); });
      g.restore(); };
    G.mum = (x, y, h, t, o = {}) => { const w = o.w ?? h * .17, rr = o.r || 700, lg = g.createRadialGradient(x, y - h - 40, 0, x, y - h - 40, rr); lg.addColorStop(0, gri(1, .55)); lg.addColorStop(1, gri(1, 0)); g.fillStyle = lg; g.fillRect(x - rr, y - h - 40 - rr, rr * 2, rr * 2);
      const gr = g.createLinearGradient(x - w / 2, 0, x + w / 2, 0); gr.addColorStop(0, gri(.98)); gr.addColorStop(1, gri(.6)); g.fillStyle = gr; g.fillRect(x - w / 2, y - h, w, h);
      const fl = h * .42, sw = Math.sin(t * 9) * w * .08 + noise1(t * 3, 5) * w * .1; g.fillStyle = gri(1); g.fill(pathOf([[x, y - h], [x + w * .45, y - h - fl * .3], [x + sw, y - h - fl], [x - w * .45, y - h - fl * .3]], true, .9)); g.fillStyle = gri(.3); g.fill(ell([x, y - h - fl * .15], w * .1, fl * .14)); };
    G.muhur = (x, y, rr, o = {}) => { const q = rng(o.seed || 5), pts = []; for (let i = 0; i < 18; i++) { const a = i / 18 * TAU, k = 1 + (q() - .5) * .22 + (i % 5 === 0 ? .12 : 0); pts.push([x + Math.cos(a) * rr * k, y + Math.sin(a) * rr * k]); }
      const P = pathOf(pts, true, .8); g.fillStyle = gri(.62); g.fill(P); g.strokeStyle = gri(.3); g.lineWidth = rr * .07; g.beginPath(); g.arc(x, y, rr * .6, .3, TAU - .5); g.stroke();
      if (o.renk !== false) G.kirmizi(o.acil != null ? (() => { const Q = new Path2D(); Q.arc(x, y, rr * 1.3 * o.acil, 0, TAU); const R2 = new Path2D(); R2.addPath(P); return R2; })() : P, o.acil ?? 1); return P; };
    G.figur = o => figur(G, o);
    // yumuşak(k, fn): fn düşük çözünürlüklü tuvale çizilir (1/k), sonra büyütülerek bulanık gölge gibi görünür
    G.yumusak = (k, fn, a = 1) => { const W = 1440 / k, H = 1080 / k; if (!YUM || YUM.width !== W) { YUM = document.createElement('canvas'); YUM.width = W; YUM.height = H; } const y = YUM.getContext('2d');
      y.setTransform(1, 0, 0, 1, 0, 0); y.clearRect(0, 0, W, H); const m = g.getTransform(); y.setTransform(m.a / k, m.b / k, m.c / k, m.d / k, m.e / k, m.f / k); fn({ ...G, g: y });
      g.save(); g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = a; g.imageSmoothingQuality = 'high'; g.drawImage(YUM, 0, 0, 1440, 1080); g.restore(); };
    return G;
  }
  // koyuluk maskesi: görüntünün koyu yerleri opak (kırmızı yalnız koyu kumaşa düşer); görüntü başına bir kez
  const KOYU_ON = new Map();
  function koyuOn(im, esik = .5, yum = .22) { const key = (im.src || '') + '|' + esik; let c = KOYU_ON.get(key); if (c) return c;
    const W = im.naturalWidth, H = im.naturalHeight; c = document.createElement('canvas'); c.width = W; c.height = H; const x = c.getContext('2d'); x.filter = 'blur(2px)'; x.drawImage(im, 0, 0);
    const d = x.getImageData(0, 0, W, H), p = d.data; for (let i = 0; i < p.length; i += 4) { const Lm = (p[i] * .3 + p[i + 1] * .59 + p[i + 2] * .11) / 255, a = Math.max(0, Math.min(1, (esik - Lm) / yum + .5)); p[i] = p[i + 1] = p[i + 2] = 0; p[i + 3] = a * 255; }
    x.putImageData(d, 0, 0); KOYU_ON.set(key, c); return c; }
  return { ctx, figur, gri, rng, pathOf, griOn, golge, koyuOn };
})();
