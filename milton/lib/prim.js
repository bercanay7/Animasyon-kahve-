// Gravür ilkelleri (v2, üslup kurulu tur 1 sonrası): bulut/duman, alev, kaya, ışık huzmesi, göl yüzeyi, zincir.
// Hepsi GR (gravur.js) katmanlarına çizer: ton → GR.tx, tarama yaması → GR.px. Koordinatlar dünya birimidir.
// İlkeler: ton sert bantlarla verilir (bulanıklık yok); çizgi doğrultusu nesneyi izler (bulut yay, alev akış, kaya faset);
// durağan nesnenin çizgisi zamanla kaymaz; hareket yavaş ve süreklidir; rastgelelik yalnız rng(seed) ile.
'use strict';
const PR = (() => {
  const { tx, px, tone, fill, hatch } = GR;
  const nrm = (v) => { const l = Math.hypot(v[0], v[1]) || 1; return [v[0] / l, v[1] / l]; };
  // çok koyu ton düz siyaha çekilir (eşiğe yakın tonlarda çizgi kesik kesik kırılmasın)
  const snap = v => v < .2 ? .03 : v;
  const sstep = (a, b, x) => { const u = clamp((x - a) / (b - a)); return u * u * (3 - 2 * u); };

  // ── bulut / duman ──
  // Tek küme (yumru): hafif dalgalı daire. Ton üç sert bant: ışıklı sırt (rim), gövde (body), koyu çekirdek (core).
  // Tarama: kümenin gölge yanındaki bir merkez çevresinde yaylar; çizgiler kümenin kavsini izler.
  const FX = 1.18, FY = .84; // kümeler yatayda yassı
  // yumru yarıçapı (açıya göre hafif dalgalı)
  function puffRad(r, s) {
    const q = rng(s), a1 = q() * TAU, a2 = q() * TAU, k1 = .05 + q() * .05, k2 = .03 + q() * .03;
    return a => r * (1 + k1 * Math.sin(3 * a + a1) + k2 * Math.sin(5 * a + a2));
  }
  function puffPath(x, y, r, s) {
    const R = puffRad(r, s), n = 22, pts = [];
    for (let i = 0; i < n; i++) { const a = i / n * TAU, rr = R(a); pts.push([x + Math.cos(a) * rr * FX, y + Math.sin(a) * rr * FY]); }
    const P = new Path2D(); spline(P, pts, true); return P;
  }
  // "Beyaz çizgi" yumrusu (üslup kurulu tur 2): yumru tek ton kütledir; biçimi, ışık yanında kenarı izleyen ve
  // uçları sivrilen birkaç hilal çizgi verir (içe doğru kısalır ve incelir). Eş merkezli halka taraması yok.
  // Koyu yumruda (duman, gece bulutu) çizgiler kâğıt rengi; açık yumruda (cennet bulutu) gölge yanında mürekkep rengi.
  function drawPuff(p, L, id, tn, later) {
    const hidden = (x, y) => later && later.some(j => { const dx = (x - j.x) / (j.r * FX * 1.1), dy = (y - j.y) / (j.r * FY * 1.1); return dx * dx + dy * dy < 1; });
    const P = puffPath(p.x, p.y, p.r, p.s), R = puffRad(p.r, p.s), light = tn.core > .6;
    fill(P, tone(light ? tn.core : snap(tn.core)), { th: -.25, ph: p.ph, id });
    const v = light ? 1 - tn.rim : tn.rim;                         // doz: ışık (ya da gölge) şiddeti
    const la = Math.atan2(L[1], L[0]) + (light ? PI : 0), q = rng(p.s + 5), sc = clamp(p.r / 150, .5, 1.6);
    tx.save(); tx.clip(P); tx.fillStyle = tone(light ? .05 : 1);
    if (v > .08) {
      // kenar ışığı: tek ince hilal, uçları sivri
      const half = (.85 + .5 * v) * (.9 + q() * .2), th = Math.max(4.5, 11 * sc * (.5 + v)), n = 18, A = [], B = [];
      for (let i = 0; i <= n; i++) { const u = i / n, a = la - half + 2 * half * u, ro = R(a) - 5, w = th * Math.pow(Math.sin(PI * u), .8);
        A.push([p.x + Math.cos(a) * ro * FX, p.y + Math.sin(a) * ro * FY]); B.push([p.x + Math.cos(a) * (ro - w) * FX, p.y + Math.sin(a) * (ro - w) * FY]); }
      const vis = k => !hidden(A[k][0], A[k][1]);
      if (vis(n >> 1) && (vis(2) || vis(n - 2))) { tx.beginPath(); poly(tx, [...A, ...B.reverse()], true); tx.fill(); }
      // vuruşlar: ışık yanındaki dilimden kütlenin içine giren, kesit kavsini izleyen, sivrilen kısa çizgiler.
      // Uzunluk ve aralık düzensiz (eşit olursa tarak gibi durur); hepsi aynı yöne kıvrılır (bıçak izi).
      const ha = PI * (.2 + .14 * v), sg = q() < .5 ? -1 : 1, beta = .5 + q() * .25;
      let a = la - ha + q() * .1;
      while (a < la + ha) {
        if (hidden(p.x + Math.cos(a) * R(a) * FX, p.y + Math.sin(a) * R(a) * FY)) { a += (20 + q() * 34) / p.r; q(); q(); continue; }
        const edge = 1 - Math.pow(Math.abs(a - la) / ha, 2), len = (40 + q() * q() * 130) * sc * (.45 + .55 * edge) * (.7 + .5 * v), w0 = Math.max(3.6, 6.5 * sc), m = 9, A2 = [], B2 = [];
        for (let i = 0; i <= m; i++) {
          const u = i / m, s2 = len * u, aa = a + sg * s2 * Math.cos(beta) / p.r, rr = R(aa) - 9 - th - s2 * Math.sin(beta) * (1 + .5 * u), hw = Math.max(1, w0 * .5 * Math.pow(1 - u, 1.15));
          const cx = p.x + Math.cos(aa) * rr * FX, cy = p.y + Math.sin(aa) * rr * FY, nx = Math.cos(aa), ny = Math.sin(aa);
          A2.push([cx + nx * hw, cy + ny * hw]); B2.push([cx - nx * hw, cy - ny * hw]);
        }
        tx.beginPath(); poly(tx, [...A2, ...B2.reverse()], true); tx.fill();
        a += (20 + q() * 34) / p.r;
      }
    }
    tx.restore();
    return P;
  }
  // Bulut kümesi: birkaç büyük kütle; her kütlenin ışık yanında öne taşan küçük yumrular. Arkadakiler koyu.
  // o: {x, y, w, h, seed, lit: [lx, ly] (ışığın geldiği yön), base (gölge/gövde tonu), hi (ışıklı sırt tonu), core (gölge yanı tonu), id, drift, n,
  //     depth (arkadakilerin kararma oranı), back (false: arka koyu dolgu yok; ince duman için)}
  // Değişen anlamlar: th ve soft artık kullanılmıyor (çizgi kümenin kavsini izler, bulanıklık yok).
  function cloud(o) {
    const r = rng(o.seed || 1), L = nrm(o.lit || [0, -1]), id = o.id ?? 2, drift = o.drift || 0;
    const base = o.base ?? .25, hi = o.hi ?? .92, n = o.n || Math.max(2, Math.round(o.w / (o.h * .8)));
    const puffs = [], la = Math.atan2(L[1], L[0]), ex = o.x - o.w / 2 + drift;
    for (let i = 0; i < n; i++) {
      const f = (i + .5 + (r() - .5) * .5) / n, env = .6 + .4 * Math.sqrt(Math.sin(clamp(f) * PI));
      const R = o.h * (.36 + r() * .5) * env;
      const cx = ex + f * o.w, cy = o.y + (r() - .5) * o.h * .25 - L[1] * R * .15;
      puffs.push({ x: cx, y: cy, r: R, lay: 0 });
      // ışık yanına taşan yumrular: boyları ve aralıkları düzensiz (alt sıra eşit dizilmesin)
      const m = Math.floor(r() * 3);
      for (let j = 0; j < m; j++) {
        const a = la + (r() - .5) * 2.4, d = R * (.55 + r() * .3), rr = R * (.32 + r() * .3);
        puffs.push({ x: cx + Math.cos(a) * d, y: cy + Math.sin(a) * d, r: rr, lay: 1 });
      }
    }
    puffs.forEach((p, i) => { p.s = (o.seed || 1) * 977 + i * 31; }); // biçim tohumu konumdan bağımsız (kayınca titremesin)
    for (const p of puffs) { p.ph = r(); p.k = (p.x - o.x) * L[0] + (p.y - o.y) * L[1] + p.lay * o.h * .25; }
    puffs.sort((a, b) => a.k - b.k);
    // arka dolgu: kümelerin arasını kapatan koyu, sakin kütle (gök arada görünmesin)
    if (o.back !== false) {
      const B = new Path2D();
      for (const p of puffs) if (!p.lay) { B.moveTo(p.x + p.r * 1.05, p.y - L[1] * p.r * .25); B.ellipse(p.x, p.y - L[1] * p.r * .25, p.r * 1.05, p.r * .9, 0, 0, TAU); }
      fill(B, tone(snap(base * .45)), { type: 'rad', cx: o.x + drift, cy: o.y - L[1] * o.h, ph: r(), id });
    }
    const N = puffs.length, dep = o.depth ?? .45, U = new Path2D();
    puffs.forEach((p, i) => {
      const back = 1 - i / Math.max(1, N - 1); // 1 = en arka
      const dk = 1 - dep * back;
      const rim = hi * (1 - dep * .6 * back), body = lerp(base, hi, o.mid ?? .7) * dk, core = (o.core ?? lerp(base, lerp(base, hi, .7), .25)) * dk;
      U.addPath(drawPuff(p, L, id, { rim, body, core }, puffs.slice(i + 1)));
    });
    return { puffs, path: U };
  }
  // Duman sütunu: yükselen, genişleyen kümeler; alttan ateşle aydınlanır (ışık aşağıdan).
  // o: {x, y, h, r0, r1, sway, n, seed, t, glow (alttaki sırt tonu), base, id, rise (yükselme hızı, 0 = durağan)}
  function smoke(o) {
    const r = rng(o.seed || 3), n = o.n || 10, t = o.t || 0, id = o.id ?? 2, rise = o.rise || 0;
    const base = o.base ?? .2, glow = o.glow ?? .7, list = [];
    for (let i = 0; i < n; i++) {
      let f = i / n; const jx = r() - .5, jr = r(), ph = r();
      let grow = 1;
      if (rise) { f = (f + t * rise) % 1; grow = sstep(0, .12, f) * (1 - sstep(.88, 1, f)); }
      const yy = o.y - f * o.h, rr = (o.r0 + (o.r1 - o.r0) * f) * (.8 + jr * .4) * grow;
      if (rr < 1) continue;
      const xx = o.x + Math.sin(f * 3.1 + (o.seed || 0) + t * .12) * (o.sway || 0) * f + jx * rr * .5;
      list.push({ x: xx, y: yy, r: rr, f, ph, s: (o.seed || 3) * 131 + i });
    }
    list.sort((a, b) => a.f - b.f).reverse(); // üstteki (uzak) önce, alttaki öne
    for (const p of list) {
      const rim = lerp(glow, base * 1.4, Math.pow(p.f, .7));
      drawPuff(p, [0, 1], id, { rim, body: lerp(rim, base, .6), core: base * .35 });
    }
  }

  // ── alev ──
  // Bir dilin geometrisi: omurga, dış biçim (kenar kabuğu) ve iç biçim (temiz kâğıt). t ile uzar, eğilir; yan dişler yukarı akar.
  function tongue(x, y, hh, wid, t, seed, o) {
    const k = hash(seed * 1.37 + .5) * 40, sp = o.speed ?? 1, m = 18;
    const lean = (o.lean ?? 0) + (hash(seed + 2.1) - .5) * .45 + .14 * fbm1(t * .3 * sp + k, 3) * (o.sway ?? 1);
    const H = hh * (.86 + .1 * Math.sin(t * 1.15 * sp + k) + .12 * fbm1(t * .7 * sp + k * 1.3, 5));
    const curl = (hash(seed + 7.7) < .5 ? -1 : 1) * (o.curl ?? 1);
    const cl = Math.cos(lean), sl = Math.sin(lean);
    const spine = [];
    for (let i = 0; i <= m; i++) {
      const f = i / m;
      const off = wid * (.55 * curl * Math.sin(f * PI * 1.25 + k * .3 + t * .8 * sp) * f + .22 * Math.sin(f * PI * 2.4 - t * 2.1 * sp + k * 2) * f * f);   // S kavisli eksen
      spine.push([x + sl * f * H + cl * off, y - cl * f * H + sl * off]);
    }
    const edge = (ins, top) => {
      const Lp = [], Rp = [];
      for (let i = 0; i <= m; i++) {
        const f = i / m * top, j = Math.min(m, Math.round(f * m)), [sx, sy] = spine[j];
        const a = spine[Math.min(m, j + 1)], b = spine[Math.max(0, j - 1)];
        const tg = Math.atan2(a[1] - b[1], a[0] - b[0]) + PI / 2;
        const pr = f < .12 ? .7 + .3 * f / .12 : Math.pow(Math.max(0, (1 - f) / .88), 1.3);
        const tear = sstep(.22, .55, f);
        const wl = wid * .5 * pr * (1 + .2 * tear * Math.sin(f * 15 - t * 4.2 * sp + k * 3)) * ins;
        const wr = wid * .5 * pr * (1 + .2 * tear * Math.sin(f * 13 - t * 3.7 * sp + k * 5 + 1.7)) * ins;
        Lp.push([sx + Math.cos(tg) * wl, sy + Math.sin(tg) * wl]); Rp.push([sx - Math.cos(tg) * wr, sy - Math.sin(tg) * wr]);
      }
      const P = new Path2D(), all = [...Lp, ...Rp.reverse()];
      P.moveTo(all[0][0], all[0][1]);
      for (let i = 1; i < all.length; i++) { const a = all[i - 1], b = all[i]; P.quadraticCurveTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); }
      P.closePath(); return P;
    };
    const tip = spine[m], ax = Math.atan2(tip[1] - y, tip[0] - x);
    const res = { outer: edge(1, 1), inner: edge(o.inner ?? .55, .8), base: [x, y], spine, ax, H, wid, curl, seed, frags: [] };
    // kopan parçalar: dil ucundan ayrılıp yükselen, küçülen alev kırıntıları (büyüklük döngü sınırlarında sıfır: sıçrama yok)
    if (o.frags !== false && hash(seed + 3.3) > .45) {
      const c = (t * .42 * sp + hash(seed + 4.4) * 7) % 1, s = wid * .26 * Math.sin(PI * c) * (1 - .45 * c);
      if (s > 1) {
        const fx = tip[0] + Math.cos(ax) * (c * H * .4 + s) + Math.sin(c * 5 + k) * wid * .15, fy = tip[1] + Math.sin(ax) * (c * H * .4 + s);
        res.frags.push({ x: fx, y: fy, s });
      }
    }
    return res;
  }
  function fragPath(f, ins) {
    const P = new Path2D(), s = f.s * ins;
    P.moveTo(f.x, f.y - s * 1.9); P.quadraticCurveTo(f.x + s * 1.05, f.y - s * .2, f.x, f.y + s * .8);
    P.quadraticCurveTo(f.x - s * 1.05, f.y - s * .2, f.x, f.y - s * 1.9); P.closePath(); return P;
  }
  // Dil listesini tek kütle olarak bas: önce bütün dış kabuklar (taralı), sonra bütün iç biçimler (temiz kâğıt) → diller birbirine kaynar.
  function drawTongues(list, y, hgt, o) {
    const id = o.id ?? 3, edgeT = o.edge ?? .64, core = o.core ?? 1, U = new Path2D();
    for (const g of list) {
      // kabuk taraması: dilin ekseni boyunca akan, eğriliğini izleyen çizgiler
      // büyük dilde kabuk akış çizgileriyle taranır; küçük ve orta dilde (H < 240) tarama iki üç dikey çizgiye düşüp koni gibi okunduğu için dil bütünüyle kâğıt kalır
      fill(g.outer, tone(g.solid || g.H < (o.solidBelow ?? 240) ? 1 : edgeT), { type: 'bend', ox: g.base[0], oy: g.base[1], a: g.ax, k: -g.curl * .9 / Math.max(60, g.H), ph: hash(g.seed + 9.1), id });
      U.addPath(g.outer);
    }
    tx.fillStyle = tone(core);
    for (const g of list) { tx.fill(g.inner); for (const f of g.frags) tx.fill(fragPath(f, .8)); }
    // taramasız (kâğıt beyazı) dillerde biçimi içteki mürekkep vuruşları verir: dipten yukarı, omurgayı izleyen, sivrilen 2–4 çizgi
    for (const g of list) {
      if (!g.spine || g.H >= (o.solidBelow ?? 240) || g.H < 46) continue;
      const q = rng(g.seed * 7 + 3), nS = g.H > 130 ? 3 : 2, m = g.spine.length - 1;
      tx.save(); tx.clip(g.outer); tx.fillStyle = tone(.04);
      for (let k = 0; k < nS; k++) {
        const side = (k % 2 ? 1 : -1) * (g.curl > 0 ? 1 : -1), off = (.16 + .1 * q()) * (k === 2 ? .15 : 1), f0 = .04 + q() * .1, f1 = .42 + q() * .3, w0 = clamp(g.wid * .07, 3.4, 9), A = [], B = [], n = 9;
        for (let i = 0; i <= n; i++) {
          const u = i / n, f = lerp(f0, f1, u), j = f * m, j0 = Math.min(m - 1, j | 0), fr = j - j0, P0 = g.spine[j0], P1 = g.spine[j0 + 1];
          const tg = Math.atan2(P1[1] - P0[1], P1[0] - P0[0]), nx = -Math.sin(tg), ny = Math.cos(tg), wl = g.wid * .5 * Math.pow(Math.max(0, 1 - f), 1.2);
          const cx = lerp(P0[0], P1[0], fr) + nx * side * off * wl * 2, cy = lerp(P0[1], P1[1], fr) + ny * side * off * wl * 2, hw = Math.max(1, w0 * .5 * Math.pow(1 - u, 1.1));
          A.push([cx + nx * hw, cy + ny * hw]); B.push([cx - nx * hw, cy - ny * hw]);
        }
        tx.beginPath(); poly(tx, [...A, ...B.reverse()], true); tx.fill();
      }
      tx.restore();
    }
    // dip: koyuya gömülen taban (kısa tarama)
    const b = o.base ?? .25;
    if (b < 1 && hgt >= (o.solidBelow ?? 240)) {
      tx.save(); tx.clip(U); tx.globalCompositeOperation = 'darken';
      const yb = y + hgt * .06, g = tx.createLinearGradient(0, yb, 0, yb - hgt * (o.dip ?? .3));
      g.addColorStop(0, tone(b)); g.addColorStop(.55, tone(lerp(b, 1, .6))); g.addColorStop(1, tone(1));
      tx.fillStyle = g; tx.fillRect(-400, yb - hgt * 1.2, W + 800, hgt * 1.4); tx.restore();
    }
    return U;
  }
  // Tek alev dili: tabandan (x, y) yukarı, yükseklik hgt, genişlik wid.
  // o: {sway, speed, curl, lean, inner (iç kâğıt oranı), edge (kabuk tonu), core (iç ton), base (dip tonu), id}
  // Değişen anlamlar: tip ve vein artık kullanılmıyor (içi temiz kâğıt, koyu damar yok).
  function flame(x, y, hgt, wid, t, seed = 0, o = {}) {
    const g = tongue(x, y, hgt, wid, t, seed, o);
    drawTongues([g], y, hgt, o);
    return g.outer;
  }
  // Uzak alev sırası: tek tek dil değil, sürekli titrek ışık bandı; üstünde alttan aydınlanan ince duman.
  function flameBand(x0, x1, y, hgt, t, seed, o) {
    const id = o.id ?? 3, r = rng(seed + 51), env = o.env || (() => 1);
    if (o.smoke !== false) { // ince duman: yalnız ton katmanında topaklı bir pus şeridi; göğün çizgisi sürer, kalınlaşır (kabarcık deseni yok)
      const sy = y - hgt * (o.smokeY ?? .5), sh = hgt * (o.smokeH ?? 2.2), D = new Path2D();
      D.moveTo(x0, y);
      for (let x = x0; x <= x1 + 20; x += 20) {
        const f = clamp((x - x0) / (x1 - x0)), e = env(f);
        D.lineTo(x, sy - sh * e * (.35 + .65 * noise2(x / 140 + seed, t * .03, 7)) * (.6 + .4 * noise2(x / 47, seed, 8)));
      }
      D.lineTo(x1, y); D.lineTo(x0, y); D.closePath();
      // pus bandın arkasına, taban çizgisine kadar iner: parlak bant her zaman koyu dumanın önünde durur
      const g = tx.createLinearGradient(0, sy - sh, 0, y), A = o.smokeA ?? .55;
      g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(.45, `rgba(0,0,0,${A * .7})`); g.addColorStop(1, `rgba(0,0,0,${A})`);
      tx.save(); tx.globalCompositeOperation = 'multiply'; tx.fillStyle = g; tx.fill(D); tx.restore();
    }
    const step = 5, top = [], inn = [];
    for (let x = x0; x <= x1 + step; x += step) {
      const f = clamp((x - x0) / (x1 - x0)), e = env(f);
      const s1 = Math.pow(noise2(x / 34 + seed * 3.1, t * .55, 1), 1.8), s2 = Math.pow(noise2(x / 13 + seed, t * .9 + 4, 2), 3);
      const hh = hgt * e * (.22 + .95 * s1 + .35 * s2);
      top.push([x, y - hh]); inn.push([x, y - hh * .7 + hgt * .03]);
    }
    const yb = y + hgt * .1, P = new Path2D(), Q = new Path2D();
    P.moveTo(x0, yb); for (const [a, b] of top) P.lineTo(a, b); P.lineTo(x1 + step, yb); P.closePath();
    Q.moveTo(x0, yb); for (const [a, b] of inn) Q.lineTo(a, Math.min(b, yb - 1)); Q.lineTo(x1 + step, yb); Q.closePath();
    fill(P, tone(o.bandEdge ?? 1), { th: -PI / 2, ph: hash(seed), id });   // taramasız: dikey çizgiler küçük boyda çit gibi okunuyordu
    tx.fillStyle = tone(o.core ?? 1); tx.fill(Q);
    return P;
  }
  // Alev öbeği: bir çizgi boyunca birbirine kaynayan diller.
  // o: {n, env(f), wr (genişlik/boy), band (uzak sıra kipi; varsayılan hgt < 100 ise açık), lean, edge, core, base, smoke, ...flame seçenekleri}
  function flameBank(x0, x1, y, hgt, t, seed = 0, o = {}) {
    if (o.band ?? hgt < 100) return flameBand(x0, x1, y, hgt, t, seed, o);
    const r = rng(seed + 9), n = o.n || Math.max(2, Math.round((x1 - x0) / (hgt * .2))), list = [];
    for (let i = 0; i < n; i++) {
      const f = (i + .5 + (r() - .5) * .9) / n, big = r() < .25 ? 1.35 : 1;
      const hh = hgt * (.4 + r() * .7) * big * (o.env ? o.env(clamp(f)) : 1);
      const wr = (o.wr ?? .45) * .85 * (.7 + r() * .6);
      const bx = lerp(x0, x1, f), by = y + (r() - .5) * hgt * .12;
      const sd = seed * 31 + i;
      list.push(tongue(bx, by, hh, hh * wr, t + r() * 10, sd, o));
      if (r() < .62) { // çatal: ana dilin yanından kopan ikinci uç
        const g = list[list.length - 1], fx = bx + Math.cos(g.ax) * hh * .35, fy = by + Math.sin(g.ax) * hh * .35;
        list.push(tongue(fx, fy, hh * (.4 + r() * .2), hh * wr * .45, t + r() * 10, sd + 500, Object.assign({}, o, { lean: (o.lean ?? 0) + (r() < .5 ? -.45 : .45) })));
      }
    }
    // tabanda sürekli şerit: dilleri birbirine bağlar; uçlarda sıfıra iner (kutu gibi kesilmez)
    const strip = { outer: new Path2D(), inner: new Path2D(), base: [x0, y], ax: -PI / 2, H: hgt, curl: 0, seed, frags: [], solid: true };   // taban şeridi her boyda taramasız
    const sh = hgt * (o.strip ?? .3), sp2 = [], ip = [];   // taban şeridi dillerin arasını kapatır (kapalı siyah boşluk kalmaz)
    for (let x = x0; x <= x1 + 1; x += 10) {
      const f = (x - x0) / (x1 - x0), e = Math.sqrt(Math.max(0, Math.sin(f * PI))) * (o.env ? o.env(clamp(f)) : 1);
      const hh = sh * e * (.6 + .5 * noise2(x / 40, t * .5 + seed, 3));
      sp2.push([x, y - hh]); ip.push([x, y - hh * .35]);
    }
    strip.outer.moveTo(x0, y); for (const q of sp2) strip.outer.lineTo(q[0], q[1]); for (let x = x1; x >= x0; x -= 16) strip.outer.lineTo(x, y + sh * .12 * noise2(x / 23, seed, 6)); strip.outer.closePath();
    strip.inner.moveTo(x0, y); for (const q of ip) strip.inner.lineTo(q[0], q[1]); strip.inner.lineTo(x1, y); strip.inner.closePath();
    list.unshift(strip);
    return drawTongues(list, y, hgt, o);
  }

  // ── kaya ──
  // Köşeli kütle: dış çizgi (pts) Voronoi fasetlere bölünür; her faset tek ton ve kendi tarama doğrultusu.
  // Işığa bakan faset temiz kâğıt, gölgedeki çapraz taramalı. Kırıklar sivri uçlu koyu kamalardır.
  // o: {lit, hi, mid, lo (ışıklı/orta/gölge tonları), seed, facets (sayı), th (ana doğrultu), id, cracks (kama sayısı ≈ cracks/6), rim (ışıklı sırt kalınlığı px)}
  function clipHalf(poly, ax, ay, bx, by) { // |p-a| <= |p-b| yarı düzlemi
    const nx = bx - ax, ny = by - ay, c = (bx * bx + by * by - ax * ax - ay * ay) / 2, out = [];
    const inside = p => p[0] * nx + p[1] * ny <= c;
    for (let i = 0; i < poly.length; i++) {
      const p = poly[i], q = poly[(i + 1) % poly.length], ip = inside(p), iq = inside(q);
      if (ip) out.push(p);
      if (ip !== iq) { const dp = p[0] * nx + p[1] * ny - c, dq = q[0] * nx + q[1] * ny - c, u = dp / (dp - dq); out.push([lerp(p[0], q[0], u), lerp(p[1], q[1], u)]); }
    }
    return out;
  }
  function rock(pts, o = {}) {
    const P = new Path2D(); poly(P, pts, true);
    const L = nrm(o.lit || [-.6, -.8]), r = rng(o.seed || 5), id = o.id ?? 4;
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const [x, y] of pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, rr = Math.max(x1 - x0, y1 - y0) / 2;
    // tohumlar: kütlenin içinde
    const nf = o.facets || clamp(Math.round((x1 - x0) * (y1 - y0) / 9000), 7, 24), seeds = [];
    for (let g = 0; seeds.length < nf && g < nf * 60; g++) {
      const sx = lerp(x0, x1, r()), sy = lerp(y0, y1, r());
      if (tx.isPointInPath(P, sx * RS, sy * RS) && seeds.every(s => Math.hypot(s[0] - sx, s[1] - sy) > rr * .16)) seeds.push([sx, sy]);
    }
    const hiT = o.hi ?? .95, midT = o.mid ?? .4, loT = snap(o.lo ?? .1), th0 = o.th ?? -.7;
    const big = [[x0 - 50, y0 - 50], [x1 + 50, y0 - 50], [x1 + 50, y1 + 50], [x0 - 50, y1 + 50]];
    tx.save(); px.save(); tx.clip(P); px.clip(P);
    tx.fillStyle = tone(loT); tx.fill(P); // alt dolgu: faset dikişlerinde açık iz kalmasın
    const facets = [];
    seeds.forEach((s, i) => {
      let cell = big;
      for (let j = 0; j < seeds.length && cell.length; j++) if (j !== i) cell = clipHalf(cell, s[0], s[1], seeds[j][0], seeds[j][1]);
      if (cell.length < 3) return;
      // faset normali: kütlenin merkezinden dışa + rastgele eğim; ışıkla nokta çarpımı → üç basamaklı ton
      const ox = (s[0] - cx) / rr, oy = (s[1] - cy) / rr, n = nrm([ox * 1.4 + (r() - .5) * 1.1, oy * 1.4 + (r() - .5) * 1.1]);
      const lit = n[0] * L[0] + n[1] * L[1];
      const v = lit > .55 ? hiT : lit > .15 ? lerp(midT, hiT, .55) : lit > -.35 ? midT : loT; // dört basamak
      const th = th0 + Math.atan2(n[1], n[0]) * .5 + (r() - .5) * .5;
      const F = new Path2D(); poly(F, cell, true);
      fill(F, tone(v), { th, ph: r(), id });
      facets.push({ cell, v, n });
    });
    // kırıklar: faset sınırlarında sivri koyu kamalar
    const nw = o.wedges ?? Math.round((o.cracks ?? 30) / 6);
    tx.fillStyle = tone(.02);
    for (let i = 0; i < nw && facets.length; i++) {
      const fc = facets[Math.floor(r() * facets.length)].cell, k = Math.floor(r() * fc.length), a = fc[k], b = fc[(k + 1) % fc.length];
      const u0 = .15 + r() * .3, u1 = u0 + .3 + r() * .3, w = 2 + r() * 4, dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
      const p0 = [lerp(a[0], b[0], u0), lerp(a[1], b[1], u0)], p1 = [lerp(a[0], b[0], Math.min(1, u1)), lerp(a[1], b[1], Math.min(1, u1))], um = (u0 + Math.min(1, u1)) / 2;
      const nx = -dy / l * w, ny = dx / l * w, sd = r() < .5 ? 1 : -1;
      tx.beginPath(); tx.moveTo(p0[0], p0[1]); tx.lineTo(lerp(a[0], b[0], um) + nx * sd, lerp(a[1], b[1], um) + ny * sd); tx.lineTo(p1[0], p1[1]); tx.closePath(); tx.fill();
    }
    tx.restore(); px.restore();
    // ışıklı sırt: ışığa bakan dış kenarlarda sürekli ince açık bant (nokta ya da kesik yok)
    if (o.rim) {
      tx.save(); tx.clip(P); tx.strokeStyle = tone(1); tx.lineWidth = o.rim * 2; tx.lineJoin = 'round';
      for (let i = 0; i < pts.length - 1; i++) {
        const a = pts[i], b = pts[i + 1], en = nrm([b[1] - a[1], -(b[0] - a[0])]);
        if (en[0] * L[0] + en[1] * L[1] > .25) { tx.beginPath(); tx.moveTo(a[0], a[1]); tx.lineTo(b[0], b[1]); tx.stroke(); }
      }
      tx.restore();
    }
    return P;
  }

  // ── ışık huzmesi ──
  // Kaynaktan (sx, sy) inen, kenarları belli ışık kolonları. İçi ışın doğrultusunda seyrek çizgi, uç yumuşak söner.
  // o: {seed, t, str (parlaklık 0–1), w0 (kaynakta genişlik), width (kolon açısal genişlik oranı), pattern (false = yalnız ton), slit: {w, h, a} (tonozdaki yarık)}
  // Değişen anlamlar: blur kullanılmıyor (kenarlar keskin); pattern varsayılanı artık açık.
  function rays(sx, sy, a0, a1, n, reach, o = {}) {
    const r = rng(o.seed || 21), t = o.t || 0, str = o.str ?? .5, w0 = o.w0 ?? 8;
    for (let i = 0; i < n; i++) {
      const a = lerp(a0, a1, (i + .2 + r() * .6) / n), da = (a1 - a0) / n * (o.width ?? (.12 + r() * .22));
      const Lr = reach * (.65 + r() * .35), s = str * (.6 + r() * .4) * (.88 + .12 * Math.sin(t * .45 + i * 1.7));
      const c = Math.cos(a), sn = Math.sin(a), nx = -sn, ny = c, ww = w0 * (.5 + r());
      const P = new Path2D(), e = (u, sd) => { const hw = ww + Lr * u * Math.tan(da) * (u > .7 ? (1 - u) / .3 : 1); return [sx + c * Lr * u + sd * nx * hw, sy + sn * Lr * u + sd * ny * hw]; };
      P.moveTo(...e(0, 1)); for (const u of [.7, .85, 1]) P.lineTo(...e(u, 1)); for (const u of [.85, .7, 0]) P.lineTo(...e(u, -1)); P.closePath();
      const g = tx.createLinearGradient(sx, sy, sx + c * Lr, sy + sn * Lr), v0 = lerp(.45, .92, s);
      g.addColorStop(0, tone(v0)); g.addColorStop(.55, tone(v0 * .75)); g.addColorStop(1, tone(v0 * .3));
      tx.save(); tx.globalCompositeOperation = 'lighten'; tx.fillStyle = g; tx.fill(P); tx.restore();
      if (o.pattern !== false) { px.fillStyle = hatch({ th: a, ph: r(), id: 7 }); px.fill(P); }
    }
    if (o.slit) { // yarık: koyu tonozda dar, yırtık kenarlı açıklık
      const sl = o.slit === true ? {} : o.slit, w = sl.w ?? 220, h = sl.h ?? 26, aa = sl.a ?? -.08, q = rng((o.seed || 21) + 5), m = 14, up = [], dn = [];
      for (let i = 0; i <= m; i++) { const f = i / m, e = Math.sin(f * PI); up.push([(f - .5) * w, -h * .5 * e * (.6 + q() * .7)]); dn.push([(f - .5) * w, h * .5 * e * (.5 + q() * .6)]); }
      const P = new Path2D(), ca = Math.cos(aa), sa = Math.sin(aa), T = p => [sx + p[0] * ca - p[1] * sa, sy + p[0] * sa + p[1] * ca];
      const all = [...up, ...dn.reverse()].map(T); poly(P, all, true);
      fill(P, tone(1), { th: aa, id: 7 });
    }
  }
  // İnce huzmeler: yarıktan hedefe inen, uçları sivrilen birkaç açık çizgi ("beyaz çizgi" dili; bant ya da kurdele değil).
  // o: {n, w (kaynakta kalınlık px), spread (hedefteki yayılma px), slitW (kaynak boyunca dağılım), v (ton), seed, t}
  function shafts(sx, sy, ex, ey, o = {}) {
    const n = o.n || 4, r = rng(o.seed || 23), w = o.w ?? 9, t = o.t || 0, dx = ex - sx, dy = ey - sy, Lr = Math.hypot(dx, dy), nx = -dy / Lr, ny = dx / Lr;
    tx.save(); tx.globalCompositeOperation = 'lighten';
    for (let i = 0; i < n; i++) {
      const f = n > 1 ? i / (n - 1) - .5 : 0, s0 = f * (o.slitW ?? 120) + (r() - .5) * 20, e0 = f * (o.spread ?? 260) + (r() - .5) * 40, len = (o.len ?? [.62, 1])[0] + r() * ((o.len ?? [.62, 1])[1] - (o.len ?? [.62, 1])[0]), u0 = r() * .12;
      const ww = w * (.7 + r() * .6) * (.9 + .1 * Math.sin(t * .4 + i * 2.1)), A = [], B = [], m = 12;
      for (let k = 0; k <= m; k++) {
        const u = u0 + (len - u0) * k / m, cx = sx + dx * u + nx * lerp(s0, e0, u), cy = sy + dy * u + ny * lerp(s0, e0, u), hw = Math.max(1, ww * .5 * Math.min(1, k / m * 6 + .35) * Math.pow(1 - k / m, .9));
        A.push([cx + nx * hw, cy + ny * hw]); B.push([cx - nx * hw, cy - ny * hw]);
      }
      tx.fillStyle = tone(o.v ?? .96); tx.beginPath(); poly(tx, [...A, ...B.reverse()], true); tx.fill();
    }
    tx.restore();
  }
  // Kenar vuruşları: bir çokgen çizgisi boyunca, verilen yönde kütlenin içine giren sivri kısa çizgiler (koyu kütlede kâğıt rengi).
  // pts: kenar noktaları; dir: [dx, dy] içe doğru yön; o: {len: [en az, en çok], gap: [en az, en çok], w, v, seed, bend, clip (Path2D)}
  function cuts(pts, dir, o = {}) {
    const r = rng(o.seed || 31), d = nrm(dir), [l0, l1] = o.len || [22, 80], [g0, g1] = o.gap || [14, 34], w0 = o.w ?? 3.6, bend = o.bend ?? .25;
    tx.save(); if (o.clip) tx.clip(o.clip); tx.fillStyle = tone(o.v ?? 1);
    for (let i = 0; i < pts.length - 1; i++) {
      const a = pts[i], b = pts[i + 1], L = Math.hypot(b[0] - a[0], b[1] - a[1]); let s = r() * g1;
      while (s < L) {
        const x = lerp(a[0], b[0], s / L), y = lerp(a[1], b[1], s / L), len = l0 + r() * r() * (l1 - l0), an = Math.atan2(d[1], d[0]) + (r() - .5) * .3, m = 8, A = [], B = [];
        for (let k = 0; k <= m; k++) { const u = k / m, aa = an + bend * u, cx = x + Math.cos(an + bend * u * .5) * len * u + d[0] * 2, cy = y + Math.sin(an + bend * u * .5) * len * u + d[1] * 2, hw = Math.max(1, w0 * .5 * Math.pow(1 - u, 1.15)), nx = -Math.sin(aa), ny = Math.cos(aa);
          A.push([cx + nx * hw, cy + ny * hw]); B.push([cx - nx * hw, cy - ny * hw]); }
        tx.beginPath(); poly(tx, [...A, ...B.reverse()], true); tx.fill();
        s += g0 + r() * (g1 - g0);
      }
    }
    tx.restore();
  }
  // yumuşak ışık lekesi (ton katmanında aydınlatma ya da karartma)
  function glow(x, y, r0, r1, v, a = 1, op = 'lighter') {
    const g = tx.createRadialGradient(x, y, r0, x, y, r1);
    const c = Math.round(v * 255);
    g.addColorStop(0, `rgba(${c},${c},${c},${a})`); g.addColorStop(1, `rgba(${c},${c},${c},0)`);
    tx.save(); tx.globalCompositeOperation = op; tx.fillStyle = g; tx.fillRect(x - r1, y - r1, r1 * 2, r1 * 2); tx.restore();
  }

  // ── göl yüzeyi ──
  // Tek, sürekli yatay tarama (zamana bağlı evre yok). Hareket yalnız ton katmanında:
  // alev yansımalarının yavaşça uzayıp kısalan dikey sütunları (üst üste yatay açık tireler) ve ince açık dalga sırtları.
  // Perspektif: tireler ufka doğru kısalır, incelir ve sıklaşır.
  // o: {id, ph, seed, tone: [ufuk, yakın] (verilirse zemin tonu boyanır), crests (sırt sayısı), crestV (sırt parlaklığı),
  //     refl: [{x, w, v, len}] (yansıma sütunları; verilmezse nrefl kadar kendiliğinden), nrefl}
  // Değişen anlamlar: bands artık kullanılmıyor.
  function lake(y0, y1, t, o = {}) {
    const id = o.id ?? 8, r = rng(o.seed || 11), D = y1 - y0;
    const P = new Path2D(); P.rect(-200, y0, W + 400, D + 1);
    if (o.tone) { const g = tx.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, tone(o.tone[0])); g.addColorStop(1, tone(o.tone[1])); tx.fillStyle = g; tx.fill(P); }
    px.fillStyle = hatch({ type: 'persp', y0, D, p0: o.p0 ?? 7.5, p1: o.p1 ?? GR.STY[id].P, ph: o.ph ?? 0, id }); px.fill(P);   // ufukta sık, yakında seyrek
    tx.save(); tx.globalCompositeOperation = 'lighter';
    // dalga sırtları
    const nc = o.crests ?? 46, cv = o.crestV ?? .3;
    for (let i = 0; i < nc; i++) {
      const f = Math.pow(r(), 1.5), yy = y0 + 4 + f * (D - 8), ln = lerp(24, 280, f) * (.6 + r() * .8), th = lerp(1.6, 3.4, f);
      const xx = r() * W, a = cv * (.5 + r() * .5) * (.7 + .3 * Math.sin(t * .5 + i * 2.3));
      tx.fillStyle = `rgba(255,255,255,${a})`; tx.beginPath(); tx.ellipse(xx + Math.sin(t * .1 + i) * 6, yy, ln / 2, th, 0, 0, TAU); tx.fill();
    }
    // yansıma sütunları
    const refl = o.refl || Array.from({ length: o.nrefl ?? 6 }, () => ({ x: r() * W, w: 60 + r() * 120, v: .35 + r() * .3 }));
    refl.forEach((q, j) => {
      const len = (q.len ?? D * .55) * (.82 + .18 * Math.sin(t * .4 + j * 1.9)), K = q.rows ?? 22;
      for (let k = 0; k < K; k++) {
        const g = k / K, yy = y0 + 3 + Math.pow(g, 1.45) * len;
        if (yy > y1) break;
        const ww = q.w * (1 - .45 * g) * (.55 + .45 * (noise1(k * .9 + t * .35 + j * 7, j) * .5 + .5));
        const xx = q.x + q.w * .22 * noise1(k * .37 + t * .22 + j * 3, j + 9) * (.3 + g);
        const a = q.v * Math.pow(1 - g, .8), hh = lerp(1.4, 4, g);
        tx.fillStyle = `rgba(255,255,255,${a})`; tx.beginPath(); tx.ellipse(xx, yy, ww / 2, hh, 0, 0, TAU); tx.fill();
      }
    });
    tx.restore();
  }

  // ── zincir ──
  // Büyük, okunur halkalar: koyu halka gövdesi, ışığa bakan yanda açık kenar. Sarkma (sag) eğrisini izler.
  // o: {sag, v (ışıklı kenar tonu), dark (halka tonu), halo (ayırma halesi tonu; false = yok), lit: [lx, ly] (ışığın geldiği yön), over (true: keskin üst katmana, GR.ox)}
  // link varsayılanı 34 px (kurul: 32–36).
  function chain(x0, y0, x1, y1, link = 34, o = {}) {
    const Lc = Math.hypot(x1 - x0, y1 - y0), n = Math.max(2, Math.floor(Lc / (link * .74))), sag = o.sag || 0;
    const L = nrm(o.lit || [.6, -.8]), c = o.over ? GR.ox : tx;
    const dark = o.over ? GR.inkCol : tone(o.dark ?? .02), light = o.over ? GR.paperCol : tone(o.v ?? .97);
    const pos = f => [lerp(x0, x1, f), lerp(y0, y1, f) + Math.sin(f * PI) * sag];
    const halo = o.over ? GR.paperCol : tone(o.halo ?? .78);
    // geçişler: 0 = açık ayırma halesi (koyu zeminde halkayı ayırır), 1 = koyu halka, 2 = ışıklı kenar
    for (const pass of [0, 1, 2]) for (let i = 0; i < n; i++) {
      if (pass === 0 && o.halo === false) break;
      const f = (i + .5) / n, [cx, cy] = pos(f), p2 = pos(f + .01), p1 = pos(f - .01), a = Math.atan2(p2[1] - p1[1], p2[0] - p1[0]);
      const la = Math.atan2(L[1], L[0]) - a; // yerel ışık açısı
      c.save(); c.translate(cx, cy); c.rotate(a); c.lineCap = 'round';
      const col = [halo, dark, light][pass];
      c.strokeStyle = col;
      if (i % 2 === 0) { // yüzü dönük halka
        c.lineWidth = link * [.34, .2, .09][pass]; c.beginPath();
        if (pass < 2) c.ellipse(0, 0, link * .5, link * .3, 0, 0, TAU); else c.ellipse(0, 0, link * .5, link * .3, 0, la - 1, la + 1);
        c.stroke();
      } else { // yan dönük halka: kalın çubuk
        const ly = Math.sin(la) >= 0 ? 1 : -1;
        c.lineWidth = link * [.4, .26, .08][pass]; c.beginPath();
        if (pass < 2) { c.moveTo(-link * .4, 0); c.lineTo(link * .4, 0); } else { c.moveTo(-link * .3, ly * link * .05); c.lineTo(link * .3, ly * link * .05); }
        c.stroke();
      }
      c.restore();
    }
  }
  return { cloud, smoke, flame, flameBank, rock, rays, shafts, cuts, glow, lake, chain, puff: drawPuff };
})();
