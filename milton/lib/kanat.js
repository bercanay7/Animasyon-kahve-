// Kanat ilkelleri v2: tüylü melek kanadı (KN.feathered) ve yarasa kanadı (KN.bat).
// Yerel koordinat: omuz kökü (0,0), kanat +x yönüne açılır, y aşağı; dış dönüşüm GR.frame ile verilir (side = -1 ayna).
// Üslup ilkeleri (üslup kurulu tur 1):
//  - kanat üç kütle okunur: ışıklı sırt (küçük örtü tüyleri), orta sıra (büyük örtüler), sarkan uçuş tüyleri;
//  - tüyler tek tek değil 2-4'lük kümeler hâlinde; ayrım yalnız küme sınırında, ışık-gölge sınırında ve uçlarda;
//  - tüy içi tarama balıksırtı: sapın iki yanında ayrı açı, tüy kavsini izler;
//  - yanık kanat koyu kütledir, tüyler ışık alan kenarda ince kâğıt çizgisiyle ayrışır (GR.ox);
//    parlak kanat açık kütledir, tüyler gölge kenarında ince mürekkep çizgisiyle ayrışır.
// Rastgelelik yalnız rng(seed); tüy sayısı ve sırası parametreyle değişmez (animasyonda sıçrama yok).
'use strict';
const KN = (() => {
  const { tx, tone, fill } = GR;
  const dir = a => [Math.cos(a), Math.sin(a)];
  const nrm = v => { const l = Math.hypot(v[0], v[1]) || 1; return [v[0] / l, v[1] / l]; };
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
  const bell = (x, c, w) => Math.exp(-Math.pow((x - c) / w, 2));

  // ── iskelet: omuz → dirsek → bilek → el ucu ──
  function skel(o) {
    const S = o.span, op = clamp(o.open ?? 1), lf = (o.lift ?? .5) + (o.flap || 0), dr = clamp(o.droop || 0);
    const th = -lerp(.12, 1.3, lf);                       // kolun genel doğrultusu: 0 yatay … -1.3 dik
    const aH = lerp(-1.5, th - .32, op);
    let aF = lerp(-1.15, th + .1, op);
    let aM = lerp(aF + 2.75, th + .2 - .08 * lf, op);
    aF += (PI / 2 - aF) * dr * .22;                       // sarkma: ön kol hafif, el kemiği çok iner (kırık kanat)
    aM += (PI / 2 + .3 - aM) * dr * .75;
    const E = [S * .17 * Math.cos(aH), S * .17 * Math.sin(aH)];
    const Wr = [E[0] + S * .27 * Math.cos(aF), E[1] + S * .27 * Math.sin(aF)];
    const Tp = [Wr[0] + S * .2 * Math.cos(aM), Wr[1] + S * .2 * Math.sin(aM)];
    // u: 0 omuz … .25 dirsek … .65 bilek … 1 uç
    const bone = u => u < .25 ? [lerp(0, E[0], u / .25), lerp(0, E[1], u / .25), aH]
      : u < .65 ? [lerp(E[0], Wr[0], (u - .25) / .4), lerp(E[1], Wr[1], (u - .25) / .4), aF]
        : [lerp(Wr[0], Tp[0], (u - .65) / .35), lerp(Wr[1], Tp[1], (u - .65) / .35), aM];
    return { S, op, lf, dr, th, aH, aF, aM, E, Wr, Tp, bone };
  }
  // üç noktadan geçen çemberin merkezi (sırt taraması için eş merkezli yaylar); doğrusal ise null
  function circ(a, b, c) {
    const d = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]));
    if (Math.abs(d) < 1e-3) return null;
    const A = a[0] * a[0] + a[1] * a[1], B = b[0] * b[0] + b[1] * b[1], C = c[0] * c[0] + c[1] * c[1];
    return [(A * (b[1] - c[1]) + B * (c[1] - a[1]) + C * (a[1] - b[1])) / d, (A * (c[0] - b[0]) + B * (a[0] - c[0]) + C * (b[0] - a[0])) / d];
  }

  // ── tek tüy geometrisi ──
  // F: {bx, by, a (sap doğrultusu), L, w, lead (+1/-1: dar bayrağın yanı), bend, dm, kind, jag[], nf}
  function featherGeom(F) {
    const d = dir(F.a), n = [-d[1] * F.lead, d[0] * F.lead];          // n: dar (ön) bayrak yönü
    const sp = f => [F.bx + d[0] * F.L * f - n[0] * F.bend * F.L * f * f, F.by + d[1] * F.L * f - n[1] * F.bend * F.L * f * f];
    const tng = f => nrm([d[0] - n[0] * 2 * F.bend * f, d[1] - n[1] * 2 * F.bend * f]);
    const pe = F.pointed ? 1.6 : 2.2;
    const prof = f => f < .06 ? .45 + f / .06 * .55 : f < .62 ? 1 : Math.pow(Math.max(0, 1 - Math.pow((f - .62) / .38, 2)), 1 / pe);
    const N = 16, Lp = [], Tp = [], Sp = [];
    const sh = F.kind === 1 ? F.dm : 0, nt = F.kind === 2 ? F.dm : 0;
    for (let i = 0; i <= N; i++) {
      const f = i / N, p = sp(f), tg = tng(f), nn = [-tg[1] * F.lead, tg[0] * F.lead];
      let wl = F.w * .34 * prof(f), wt = F.w * .66 * prof(f);
      // yanık, düzensiz uç: düşük frekanslı yırtık (tüy başına sabit tablo)
      const rag = F.rag * inv(.55, 1, f);
      wl *= 1 - rag * F.jag[i % 7] * .8; wt *= 1 - rag * F.jag[(i + 3) % 7] * .9;
      // çentik: arka bayrakta V kesik
      if (nt > 0) wt *= 1 - nt * .85 * Math.max(0, 1 - Math.abs(f - F.nf) / .07);
      Lp.push([p[0] + nn[0] * wl, p[1] + nn[1] * wl]); Tp.push([p[0] - nn[0] * wt, p[1] - nn[1] * wt]); Sp.push(p);
    }
    // kırık uç: son noktaları kırpık, dişli bitir
    if (sh > 0) { const k = Math.round(N * (1 - .12 * sh)); for (let i = k; i <= N; i++) { const s = Sp[k - 1], j = (i - k) % 2 ? .5 : 1; Lp[i] = [lerp(Lp[i][0], s[0] + (Lp[k - 1][0] - s[0]) * j, sh), lerp(Lp[i][1], s[1] + (Lp[k - 1][1] - s[1]) * j, sh)]; Tp[i] = [lerp(Tp[i][0], s[0] + (Tp[k - 1][0] - s[0]) * (1.5 - j), sh), lerp(Tp[i][1], s[1] + (Tp[k - 1][1] - s[1]) * (1.5 - j), sh)]; } }
    const full = new Path2D(); spline(full, [...Lp, ...Tp.slice().reverse()], true, .8);
    const lv = new Path2D(); poly(lv, [...Lp, ...Sp.slice().reverse()], true);
    const tv = new Path2D(); poly(tv, [...Tp, ...Sp.slice().reverse()], true);
    return { full, lv, tv, Lp, Tp, Sp, sp, d, n };
  }

  // ── tüy çizimi: iki bayrak ayrı açıda taranır (balıksırtı); ton gradyanı tabandan uca ──
  function drawFeather(F, G, C) {
    const { full, lv, tv, sp } = G, tip = sp(1), b = [F.bx, F.by];
    const kk = -F.bend / F.L;
    // bindirme gölgesi: önceki (dış) tüyün üstüne düşen koyu bant; yalnız küme sınırında belirgin
    if (F.sep > .02) {
      tx.save(); tx.translate(G.n[0] * F.w * .32 + C.sh[0] * F.w * .2, G.n[1] * F.w * .32 + C.sh[1] * F.w * .2);
      tx.fillStyle = tone(Math.max(0, F.v1 - C.shadeDrop), F.sep); tx.fill(full); tx.restore();
    }
    const gr = (v0, v1) => { const g = tx.createLinearGradient(b[0], b[1], tip[0], tip[1]); g.addColorStop(0, tone(v0)); g.addColorStop(.55, tone(lerp(v0, v1, .6))); g.addColorStop(1, tone(v1)); return g; };
    const al = F.a + F.lead * F.beta, at = F.a - F.lead * F.beta * 1.15;
    fill(lv, gr(F.v0 + F.dv, F.v1 + F.dv), { type: 'bend', ox: b[0], oy: b[1], a: al, k: kk, id: 6, ph: F.ph });
    fill(tv, gr(F.v0 - F.dv * .5, F.v1 - F.dv * .5), { type: 'bend', ox: b[0], oy: b[1], a: at, k: kk, id: 6, ph: F.ph + .5 });
    // yanık uç: düzensiz sınırla koyulaşan uç (yalnız ton katmanı)
    if (F.burn > .02) {
      const f0 = 1 - .38 * F.burn, P = new Path2D(), pts = [];
      for (let i = 0; i <= 6; i++) { const s = i / 6, ff = f0 + F.jag[i] * .1 * F.burn; const p = sp(ff), w = (s - .5) * F.w * 1.6; pts.push([p[0] + G.n[0] * w, p[1] + G.n[1] * w]); }
      const far = sp(1.3); pts.push([far[0] - G.n[0] * F.w, far[1] - G.n[1] * F.w], [far[0] + G.n[0] * F.w, far[1] + G.n[1] * F.w]);
      // uçtan kenara uzanan sınır: noktaları sırala (sol → sağ → uç ötesi)
      poly(P, [pts[0], ...pts.slice(1, 7), pts[8], pts[7]], true);
      tx.save(); tx.clip(full); const g = tx.createLinearGradient(sp(f0)[0], sp(f0)[1], tip[0], tip[1]);
      g.addColorStop(0, tone(Math.min(F.v1, .25), .0)); g.addColorStop(.35, tone(.04, .85 * F.burn)); g.addColorStop(1, tone(0, F.burn));
      tx.fillStyle = g; tx.fill(P); tx.restore();
    }
  }

  // ── üst katman çizgileri: konik (uçlara doğru incelen) çizgi ──
  function taper(ox, pts, w0, w1, col, a) {
    if (a <= .01 || pts.length < 2) return;
    ox.strokeStyle = col; ox.globalAlpha = a; ox.lineCap = 'round';
    for (let i = 1; i < pts.length; i++) {
      const s = (i - .5) / (pts.length - 1); ox.lineWidth = lerp(w0, w1, Math.sin(s * PI)) ;
      ox.beginPath(); ox.moveTo(pts[i - 1][0], pts[i - 1][1]); ox.lineTo(pts[i][0], pts[i][1]); ox.stroke();
    }
    ox.globalAlpha = 1;
  }

  // ── tüylü kanat ──
  // o: {span, open, lift, flap, droop, t, seed, dark, rim, ruin, lit:[lx,ly], burn}
  function feathered(o) {
    const K = skel(o), { S, op, dr, bone, E, Wr, Tp } = K;
    const t = o.t || 0, dark = clamp(o.dark ?? 0), rim = o.rim ?? .5, ruin = clamp(o.ruin ?? 0), seed = o.seed || 1;
    const lit = nrm(o.lit || [.55, -.85]), shd = [-lit[0], -lit[1]];
    const r = rng(seed * 7919 + 13);
    // değer tablosu (parlak ↔ yanık): sırt, orta sıra, uçuş tüyü tabanı/ucu
    const V = (b, k) => lerp(b, k, dark);
    const vRidge = V(.97, .24), vMid = V(.92, .07), vFb = V(.86, .06), vFt = V(.66, .02);
    const C = { sh: [shd[0], shd[1]], shadeDrop: V(.3, .08) };
    const sc = Math.max(.5, S / 550);                       // çizgi kalınlık ölçeği
    // kanat merkezinden ışığa doğru konum: kütle içi ışık eğimi
    const cen = [(E[0] + Wr[0] + Tp[0]) / 3 + S * .12 * Math.cos(K.th + PI / 2), (E[1] + Wr[1] + Tp[1]) / 3 + S * .12 * Math.sin(K.th + PI / 2)];
    const lightAt = (x, y) => clamp(.5 + dot([(x - cen[0]) / (S * .45), (y - cen[1]) / (S * .45)], lit) * .5);
    const Fs = [];
    // grup: 0 birincil (el), 1 ikincil (ön kol), 2 üçüncül (omuz)
    const groups = [{ n: 10, u0: 1, u1: .67, g: 0 }, { n: 12, u0: .64, u1: .27, g: 1 }, { n: 4, u0: .24, u1: .05, g: 2 }];
    // kümeler: 2-4 tüy (tohuma bağlı, parametreye değil)
    let ci = 0, cLeft = 0, cSize = 1, cOff = 0;
    for (const G of groups) for (let i = 0; i < G.n; i++) {
      const q = i / (G.n - 1), u = lerp(G.u0, G.u1, q);
      const [bx, by, ba] = bone(u);
      let a;
      if (G.g === 0) { const rel = lerp(.1, PI / 2 - .12, Math.pow(q, .8)) * Math.pow(op, .6); a = K.aM + rel; }
      else { const ao = (G.g === 1 ? K.aF + PI / 2 + .08 + .14 * q : K.aH + PI / 2 + .5 + .25 * q), af = PI / 2 - .06 + .04 * q; a = lerp(af, ao, op); }
      a += (PI / 2 - a) * dr * (G.g === 0 ? .3 : .18);       // yerçekimi
      a += Math.sin(t * 1.3 + i * .55 + G.g) * .01 * op;     // canlılık
      const Lb = G.g === 0 ? lerp(.36, .44, bell(q, .25, .3) + .0) - .06 * q : G.g === 1 ? .35 - .02 * q : .31 - .04 * q;
      const h = r(), kind = r() < .3 && G.g < 2 ? 0 : r() < .55 ? 1 : 2; // 0 eksik, 1 kısa/kırık, 2 çentikli
      const dm = smooth(clamp((ruin * 1.25 - h) / .3));
      let L = S * Lb * (.96 + r() * .08), w = S * (G.g === 0 ? .072 : G.g === 1 ? .08 : .085);
      if (kind === 0) { L *= 1 - .8 * dm; w *= 1 - .3 * dm; }
      if (kind === 1) L *= 1 - .3 * dm;
      const jag = Array.from({ length: 7 }, () => r());
      if (cLeft <= 0) { ci++; cSize = 2 + Math.floor(r() * 3); cLeft = cSize; cOff = (r() - .5) * .12; }
      const cp = 1 - (cLeft - 1) / Math.max(1, cSize - 1); cLeft--;  // küme içindeki konum: 0 ilk … 1 son
      const tb = r(), burnR = r(), nf = .55 + r() * .3, ph = r();
      const lead = Math.sin(a - ba) >= 0 ? -1 : 1;            // dar bayrak kemik ucuna bakar
      const leadFix = dot([-Math.sin(a) * lead, Math.cos(a) * lead], dir(ba)) > 0 ? lead : -lead;
      Fs.push({ G: G.g, q, u, bx, by, a, ba, L, w, kind, dm, jag, ci, cp, cOff, tb, burnR, nf, ph, lead: leadFix, pointed: G.g === 0,
        bend: G.g === 0 ? .07 + .03 * q : .05, beta: G.g === 0 ? .15 : .17 });
    }
    // tonlar: kütle eğimi + küme yuvarlanması (küme ilk tüyü ışıklı, sonu gölgede); ayrım yalnız küme sınırında
    for (const F of Fs) {
      const m = F.L * .5, mx = F.bx + Math.cos(F.a) * m, my = F.by + Math.sin(F.a) * m, la = lightAt(mx, my);
      const roll = (.5 - F.cp) * V(.2, .04) + F.cOff * V(1, .25);
      const v0 = lerp(vFb, vMid, F.G === 2 ? .5 : 0), v1 = vFt;
      const lift = (la - .5) * V(.3, .07);
      F.v0 = clamp(v0 + lift + roll); F.v1 = clamp(v1 + lift + roll * .8 - .04 * F.tb);
      F.dv = V(.05, .03) * (dot(dir(F.a + PI / 2 * F.lead), lit) > 0 ? 1 : -1);
      const first = F.cp === 0;
      const mid = bell((F.v0 + F.v1) / 2, .5, .28);          // ışık-gölge sınırı
      F.sep = first ? lerp(.55, .85, mid) : .12 * mid;
      F.rag = F.G < 2 ? clamp(ruin * (.4 + .9 * F.burnR) + dark * .15 * F.burnR) * .5 : 0;
      F.burn = F.G < 2 ? clamp((ruin * 1.1 + dark * .25) * (.35 + .9 * F.burnR) - .15) : 0;
    }
    const geoms = Fs.map(featherGeom);
    // 0) zar: tüy tabanlarının arkasında, boşluk görünmesin
    const back = new Path2D();
    { const pts = [[0, 0], E, Wr]; for (let u = .66; u >= .05; u -= .06) { const [x, y, ba] = bone(u); const F = Fs.reduce((p, c) => Math.abs(c.u - u) < Math.abs(p.u - u) ? c : p); pts.push([x + Math.cos(F.a) * F.L * .5, y + Math.sin(F.a) * F.L * .5]); } pts.push([S * .02, S * .08]); spline(back, pts, true, .6); }
    fill(back, tone(V(.55, .03)), { type: 'bend', ox: 0, oy: 0, a: K.aF + PI / 2, k: 0, id: 6 });
    // 1) uçuş tüyleri: dıştan içe (içteki üstte)
    for (let i = 0; i < Fs.length; i++) drawFeather(Fs[i], geoms[i], C);
    // 2) örtü tüyleri: büyükler (orta sıra), sonra ortancalar
    const cov = [];
    const rowDef = [{ n: 13, u0: .93, u1: .1, Lk: .19, wk: .075, v: () => vMid, beta: .08, g: 3 }, { n: 10, u0: .82, u1: .12, Lk: .115, wk: .065, v: () => lerp(vMid, vRidge, .55), beta: .06, g: 4 }];
    const fa = u => { let best = Fs[0]; for (const F of Fs) if (Math.abs(F.u - u) < Math.abs(best.u - u)) best = F; return best.a; };
    for (const R of rowDef) {
      let cl = 0, cs = 1, co = 0;
      for (let i = 0; i < R.n; i++) {
        const q = i / (R.n - 1), u = lerp(R.u0, R.u1, q), [bx, by, ba] = bone(u);
        let a = fa(u) + (R.g === 4 ? -.08 : -.04) * op;
        const L = S * R.Lk * (.9 + r() * .2) * (u > .65 ? lerp(1, .55, (u - .65) / .35) : 1), w = S * R.wk;
        if (cl <= 0) { cs = 2 + Math.floor(r() * 3); cl = cs; co = (r() - .5) * .1; }
        const cp = 1 - (cl - 1) / Math.max(1, cs - 1); cl--;
        const lead = dot([-Math.sin(a), Math.cos(a)], dir(ba)) > 0 ? 1 : -1;
        const bxo = bx + Math.cos(a) * S * (R.g === 3 ? .035 : .015), byo = by + Math.sin(a) * S * (R.g === 3 ? .035 : .015);
        const mx = bxo + Math.cos(a) * L * .5, my = byo + Math.sin(a) * L * .5, la = lightAt(mx, my);
        const roll = (.5 - cp) * V(.1, .03) + co * V(1, .2), lft = (la - .5) * V(.24, .05);
        const v = R.v();
        const F = { G: R.g, bx: bxo, by: byo, a, L, w, lead, kind: 2, dm: 0, jag: Array.from({ length: 7 }, () => r()), nf: .7, ph: r(), pointed: false, bend: .04, beta: R.beta,
          cp, v0: clamp(v + lft + roll + V(.02, .05)), v1: clamp(v - V(.06, .03) + lft + roll), rag: 0, burn: R.g === 3 ? clamp(ruin * .5 * r() - .1) : 0 };
        F.dv = V(.04, .025) * (dot(dir(a + PI / 2 * lead), lit) > 0 ? 1 : -1);
        const mid = bell((F.v0 + F.v1) / 2, .5, .3);
        F.sep = cp === 0 ? lerp(.45, .8, mid) : .1;
        cov.push([F, featherGeom(F)]);
      }
      // sıra sınırı: bu sıranın üstüne bir sonraki sıra koyu bant bırakır (kütle ayrımı)
      for (const [F, G] of cov.filter(c => c[0].G === R.g)) drawFeather(F, G, C);
    }
    // 3) sırt: küçük örtü tüyleri ve ön kenar tek kütle; tarama kemik kavsini izler (eş merkezli yaylar)
    const ridge = new Path2D(), lead = [], trail = [];
    const sideN = u => { const [, , ba] = bone(u); return [Math.cos(ba - PI / 2), Math.sin(ba - PI / 2)]; }; // ön kenar normali
    for (let i = 0; i <= 24; i++) {
      const u = lerp(.0, .9, i / 24), [x, y, ba] = bone(u), nn = sideN(u);
      const th = S * (.028 + .012 * bell(u, .62, .1)) * (u > .75 ? lerp(1, .5, (u - .75) / .15) : 1);
      lead.push([x + nn[0] * th, y + nn[1] * th]);
      const a = fa(u), sc2 = i % 2 ? .75 : 1;   // pul pul arka kenar
      const dep = S * (.045 + .015 * bell(u, .4, .2)) * (u > .7 ? lerp(1, .35, (u - .7) / .2) : 1) * sc2;
      trail.push([x + Math.cos(a) * dep, y + Math.sin(a) * dep]);
    }
    lead.unshift([-S * .02, S * .05]); trail.unshift([S * .03, S * .1]);
    spline(ridge, [...lead, ...trail.reverse()], true, .7);
    const cc = circ([0, 0], E, Tp);
    const rh = cc && Math.hypot(cc[0], cc[1]) < S * 3 ? { type: 'rad', cx: cc[0], cy: cc[1], id: 6 } : { type: 'bend', ox: 0, oy: 0, a: K.aF, k: 0, id: 6 };
    // sırt gölgesi: orta sıraya düşen bant
    tx.save(); tx.translate(shd[0] * S * .012, shd[1] * S * .012 + S * .008); tx.fillStyle = tone(V(.45, .02), .8); tx.fill(ridge); tx.restore();
    { const g = tx.createLinearGradient(E[0] + sideN(.4)[0] * S * .04, E[1] + sideN(.4)[1] * S * .04, E[0] - sideN(.4)[0] * S * .08, E[1] - sideN(.4)[1] * S * .08);
      const rl = lightAt(E[0], E[1]) - .5;
      g.addColorStop(0, tone(clamp(vRidge + V(.03, .1) + rl * V(.1, .15)))); g.addColorStop(.45, tone(clamp(vRidge + rl * V(.1, .1)))); g.addColorStop(1, tone(clamp(lerp(vRidge, vMid, V(.5, .85)) + rl * V(.1, .05))));
      fill(ridge, g, rh); }

    // 4) üst katman: koyu kanatta ışık kenarına kâğıt çizgisi, parlak kanatta gölge kenarına mürekkep çizgisi
    const ox = GR.ox; ox.save(); ox.setTransform(tx.getTransform()); ox.lineJoin = 'round';
    const k = Math.hypot(ox.getTransform().a, ox.getTransform().b) || 1, lw = sc / k * (o.lw ?? 1); // çizgi kalınlığı ekranda sabit oranlı
    const all = Fs.map((F, i) => [F, geoms[i]]).concat(cov);
    for (const [F, G] of all) {
      const vm = (F.v0 + F.v1) / 2, dk = clamp(inv(.45, .15, vm)), lt = clamp(inv(.55, .85, vm));
      const ed = F.lead > 0 ? G.Lp : G.Lp; // görünen kenar: dar bayrak tarafı
      const ndir = G.n, face = dot(ndir, lit);
      const f0 = F.G < 3 ? 6 : 4;
      if (dk > 0 && rim > 0) { // kâğıt çizgisi: ışığa bakan kenar, yalnız küme başı ya da uç
        const a = rim * dk * clamp(face * 1.6 + .2) * (F.cp === 0 ? 1 : .0);
        taper(ox, ed.slice(f0), .4 * lw, 2.0 * lw, GR.paperCol, a * .95);
        const tipA = rim * dk * clamp(face + .6) * .8 * (F.G < 3 ? 1 : F.cp === 0 ? .6 : 0);      // uç kontur
        taper(ox, [...G.Lp.slice(-4), ...G.Tp.slice(-4).reverse()], .3 * lw, 1.4 * lw, GR.paperCol, tipA);
      }
      if (lt > 0) { // mürekkep çizgisi: gölgeye bakan kenar, küme başı
        const a = lt * clamp(-face * 1.4 + .35) * (F.cp === 0 ? 1 : .25);
        taper(ox, ed.slice(f0 - 1), .3 * lw, 1.6 * lw, GR.inkCol, a * .8);
        if (F.G < 3) taper(ox, [...G.Lp.slice(-3), ...G.Tp.slice(-5).reverse()], .3 * lw, 1.3 * lw, GR.inkCol, lt * .55);
      }
    }
    // sırt kenarı: ön kenar boyunca ışık (koyu kanat) ya da kontur (parlak kanat)
    { const dk = clamp(inv(.5, .15, vRidge)), lt = clamp(inv(.6, .9, vRidge));
      const seg = lead.slice(1), parts = [];
      for (let i = 1; i < seg.length; i++) { const e = nrm([seg[i][0] - seg[i - 1][0], seg[i][1] - seg[i - 1][1]]), nn = [e[1], -e[0]]; parts.push(dot(nn, lit)); }
      if (dk > 0) taper(ox, seg, .5 * lw, 2.2 * lw, GR.paperCol, rim * dk * clamp(Math.max(...parts) * 1.5 + .3));
      if (lt > 0) taper(ox, seg, .5 * lw, 1.8 * lw, GR.inkCol, lt * .7 * clamp(-Math.min(...parts) + .4)); }
    ox.restore();
    return { E, Wr, Tp, bone, back, ridge, feathers: Fs };
  }

  // ── yarasa kanadı ──
  // o: {span, open, lift, flap, droop, t, seed, dark, rim, lit}
  function bat(o) {
    const K = skel(Object.assign({}, o, { lift: (o.lift ?? .5) * .9 })), { S, op, bone, E, Wr } = K;
    const t = o.t || 0, dark = clamp(o.dark ?? .7), rim = o.rim ?? .5, r = rng((o.seed || 1) * 4513 + 7), dr = clamp(o.droop || 0);
    const lit = nrm(o.lit || [.55, -.85]), V = (b, k) => lerp(b, k, dark);
    // parmaklar: bilekten yelpaze; katlıyken ön kol boyunca geri yatar
    const rel = [-.2, .4, .95, 1.5], Ls = [.5, .46, .38, .3], fing = [];
    for (let j = 0; j < 4; j++) {
      let a = lerp(K.aF + 2.85 + j * .05, K.aF + rel[j] * (1 + .15 * K.lf) - .1, op);
      a += (PI / 2 - a) * dr * .3 + Math.sin(t * 1.2 + j) * .008 * op;
      const L = S * Ls[j] * (.97 + r() * .06), kn = [Wr[0] + Math.cos(a) * L * .48, Wr[1] + Math.sin(a) * L * .48];
      const a2 = a + (.12 + .05 * j) * op * (j === 0 ? -.5 : 1), tp = [kn[0] + Math.cos(a2) * L * .52, kn[1] + Math.sin(a2) * L * .52];
      fing.push({ a, a2, L, kn, tp });
    }
    const body = [S * .03, S * lerp(.42, .55, op)];
    const tips = [...fing.map(f => f.tp), body];
    // zar panelleri: parmak j ile j+1 arası; kenar kavisli oyuk
    const scallop = (P, a, b, dep) => { const m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], to = nrm([Wr[0] - m[0], Wr[1] - m[1]]), d = Math.hypot(b[0] - a[0], b[1] - a[1]) * dep;
      P.quadraticCurveTo(m[0] + to[0] * d * 2, m[1] + to[1] * d * 2, b[0], b[1]); };
    const vM = V(.62, .14), vEdge = V(.78, .3);
    for (let j = 0; j < 4; j++) {
      const P = new Path2D(), A = fing[j], B = j < 3 ? fing[j + 1] : null;
      P.moveTo(Wr[0], Wr[1]); P.lineTo(A.kn[0], A.kn[1]); P.lineTo(A.tp[0], A.tp[1]);
      if (B) { scallop(P, A.tp, B.tp, .2 + .05 * r()); P.lineTo(B.kn[0], B.kn[1]); P.closePath(); }
      else { scallop(P, A.tp, body, .14); P.quadraticCurveTo(S * .06, S * .2, 0, S * .04); P.lineTo(0, 0); P.lineTo(E[0], E[1]); P.closePath(); }
      const ea = B ? (A.a + B.a) / 2 : (A.a + PI / 2) / 2, mid = B ? [(A.tp[0] + B.tp[0]) / 2, (A.tp[1] + B.tp[1]) / 2] : [(A.tp[0] + body[0]) / 2, (A.tp[1] + body[1]) / 2];
      // ton: ışık alan parmağa yakın açık, zar kenarına doğru saydam (açık)
      const nA = dir(A.a + PI / 2), la = dot(nA, lit) > 0 ? 1 : -1;
      const g = tx.createLinearGradient(Wr[0], Wr[1], mid[0], mid[1]);
      const pv = vM + (j % 2 ? -.04 : .03) * (1 - dark * .5) + la * V(.04, .03);
      g.addColorStop(0, tone(clamp(pv - V(.12, .08)))); g.addColorStop(.7, tone(clamp(pv))); g.addColorStop(1, tone(clamp(lerp(pv, vEdge, .7))));
      fill(P, g, { type: 'bend', ox: Wr[0], oy: Wr[1], a: ea, k: (B ? .35 : .5) / S * (j % 2 ? 1 : -1) * .6, id: 6, ph: j * .3 });
      // parmak gölgesi: zarın parmağın gölge yanına düşen koyu bandı
      tx.save(); tx.clip(P); tx.strokeStyle = tone(V(.25, .02), .7); tx.lineWidth = S * .02; tx.lineCap = 'round';
      tx.beginPath(); tx.moveTo(Wr[0], Wr[1]); tx.lineTo(A.kn[0], A.kn[1]); tx.lineTo(A.tp[0], A.tp[1]); tx.stroke(); tx.restore();
    }
    // ön zar (omuz–bilek arası)
    { const P = new Path2D(), n = dir(K.aF - PI / 2); P.moveTo(0, 0); P.quadraticCurveTo(E[0] + n[0] * S * .06, E[1] + n[1] * S * .06, Wr[0], Wr[1]); P.lineTo(E[0], E[1]); P.closePath();
      fill(P, tone(V(.7, .2)), { type: 'bend', ox: 0, oy: 0, a: K.aF, k: 0, id: 6 }); }
    // kemikler: konik, eklem şişkin
    const boneP = (a, b, w0, w1) => { const d = nrm([b[0] - a[0], b[1] - a[1]]), n = [-d[1], d[0]], P = new Path2D();
      P.moveTo(a[0] + n[0] * w0, a[1] + n[1] * w0); P.lineTo(b[0] + n[0] * w1, b[1] + n[1] * w1); P.arc(b[0], b[1], w1, Math.atan2(n[1], n[0]), Math.atan2(-n[1], -n[0]));
      P.lineTo(a[0] - n[0] * w0, a[1] - n[1] * w0); P.arc(a[0], a[1], w0, Math.atan2(-n[1], -n[0]), Math.atan2(n[1], n[0])); P.closePath(); return [P, Math.atan2(d[1], d[0])]; };
    const bones = [boneP([0, 0], E, S * .03, S * .022), boneP(E, Wr, S * .022, S * .016)];
    for (const f of fing) { bones.push(boneP(Wr, f.kn, S * .011, S * .008)); bones.push(boneP(f.kn, f.tp, S * .008, S * .0025)); }
    const vb = V(.85, .05);
    for (const [P, a] of bones) fill(P, tone(vb), { type: 'bend', ox: 0, oy: 0, a, k: 0, id: 6 });
    // pençe (başparmak)
    const cl = new Path2D(), ca = K.aF - .9;
    cl.moveTo(Wr[0] - S * .01, Wr[1]); cl.quadraticCurveTo(Wr[0] + Math.cos(ca) * S * .05, Wr[1] + Math.sin(ca) * S * .05, Wr[0] + Math.cos(ca + .5) * S * .07, Wr[1] + Math.sin(ca + .5) * S * .07);
    cl.quadraticCurveTo(Wr[0] + Math.cos(ca) * S * .03, Wr[1] + Math.sin(ca) * S * .03, Wr[0] + S * .012, Wr[1] + S * .005); cl.closePath();
    fill(cl, tone(V(.3, .02)), { th: ca, id: 6 });
    // üst katman: kemiklerin ışık yanı ve zar kenarı
    const ox = GR.ox; ox.save(); ox.setTransform(tx.getTransform());
    const k = Math.hypot(tx.getTransform().a, tx.getTransform().b) || 1, lw = Math.max(.5, S / 550) / k * (o.lw ?? 1);
    const dk = clamp(inv(.5, .15, vM)), lt = clamp(inv(.5, .8, vM));
    const lineOn = (a, b, w, side) => { const d = nrm([b[0] - a[0], b[1] - a[1]]), n = [-d[1], d[0]], s = dot(n, lit) > 0 ? 1 : -1, ff = side * s;
      return [[a[0] + n[0] * w * ff, a[1] + n[1] * w * ff], [lerp(a[0], b[0], .5) + n[0] * w * ff, lerp(a[1], b[1], .5) + n[1] * w * ff], [b[0] + n[0] * w * .5 * ff, b[1] + n[1] * w * .5 * ff]]; };
    const segs = [[[0, 0], E, S * .025], [E, Wr, S * .018]]; for (const f of fing) segs.push([Wr, f.kn, S * .01], [f.kn, f.tp, S * .006]);
    for (const [a, b, w] of segs) {
      if (dk > 0) taper(ox, lineOn(a, b, w, 1), .5 * lw, 1.8 * lw, GR.paperCol, rim * dk);
      if (lt > 0) taper(ox, lineOn(a, b, w, -1), .5 * lw, 1.6 * lw, GR.inkCol, lt * .8);
    }
    // zar kenarı: kavisli oyuklar boyunca ince çizgi
    for (let j = 0; j < 4; j++) {
      const a = tips[j], b = tips[j + 1], m = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2], to = nrm([Wr[0] - m[0], Wr[1] - m[1]]), d = Math.hypot(b[0] - a[0], b[1] - a[1]) * (j < 3 ? .2 : .14);
      const c = [m[0] + to[0] * d * 2, m[1] + to[1] * d * 2], pts = [];
      for (let i = 0; i <= 10; i++) { const s = i / 10; pts.push([(1 - s) * (1 - s) * a[0] + 2 * s * (1 - s) * c[0] + s * s * b[0], (1 - s) * (1 - s) * a[1] + 2 * s * (1 - s) * c[1] + s * s * b[1]]); }
      const face = dot(nrm([-to[0], -to[1]]), lit);
      if (dk > 0) taper(ox, pts, .4 * lw, 1.5 * lw, GR.paperCol, rim * dk * clamp(face + .5));
      if (lt > 0) taper(ox, pts, .4 * lw, 1.4 * lw, GR.inkCol, lt * .7);
    }
    ox.restore();
    return { E, Wr, Tp: fing[0].tp, bone, fingers: fing };
  }
  return { feathered, bat, skel };
})();
