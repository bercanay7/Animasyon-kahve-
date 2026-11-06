// Gravür ilkelleri: bulut/duman, alev, kaya, ışık huzmesi, göl yüzeyi, zincir.
// Hepsi GR (gravur.js) katmanlarına çizer: ton → GR.tx, desen → GR.px. Koordinatlar dünya birimidir.
'use strict';
const PR = (() => {
  const { tx, px, tone, pat, fill } = GR;

  // ── bulut / duman ──
  // Kabarık bulut: üst kenarı yuvarlak kümelerden, altı yassı. Işık yönü (lx, ly) ile her küme ayrı gölgelenir.
  // o: {x, y, w, h, seed, lit: [lx, ly] (birim), base (gölge tonu), hi (ışıklı ton), th (çizgi doğrultusu), id, ph, drift}
  function cloud(o) {
    const r = rng(o.seed || 1), n = o.n || Math.max(6, Math.round(o.w / (o.h * .45)));
    const puffs = [];
    for (let i = 0; i < n; i++) {
      const f = (i + .5) / n, edge = Math.pow(Math.sin(f * PI), .7);
      const rr = o.h * (.28 + .4 * edge) * (.7 + r() * .6);
      puffs.push({ x: o.x - o.w / 2 + f * o.w + (r() - .5) * o.w / n * .8, y: o.y - rr * (.25 + r() * .45) * edge, r: rr });
      if (r() < .6) { const rr2 = rr * (.45 + r() * .3); puffs.push({ x: puffs[puffs.length - 1].x + (r() - .5) * rr, y: puffs[puffs.length - 1].y - rr * (.5 + r() * .4), r: rr2 }); }
    }
    for (let i = 0; i < n; i++) puffs.push({ x: o.x - o.w / 2 + (i + r()) / n * o.w, y: o.y + o.h * (.05 + r() * .12), r: o.h * (.3 + r() * .18) });
    const [lx, ly] = o.lit || [0, -1];
    const base = o.base ?? .25, hi = o.hi ?? .92, th = o.th ?? 0, id = o.id ?? 2, ph = o.ph ?? 0, drift = o.drift || 0;
    const U = new Path2D();
    for (const p of puffs) { U.moveTo(p.x + drift + p.r, p.y); U.arc(p.x + drift, p.y, p.r, 0, TAU); }
    // desen: bütün bulut tek doğrultu (Doré: bulut, göğün yatay çizgileriyle örülür)
    px.fillStyle = pat(th, ph, id); px.fill(U);
    // ton: yumuşak kenarlı gövde + ışık yönünden gelen kabartı
    tx.save();
    tx.filter = `blur(${(o.soft ?? 5)}px)`;
    tx.fillStyle = tone(base); tx.fill(U);
    tx.filter = 'none';
    tx.clip(U);
    for (const p of puffs.sort((a, b) => (a.x * lx + a.y * ly) - (b.x * lx + b.y * ly))) {
      const cx = p.x + drift + lx * p.r * .35, cy = p.y + ly * p.r * .35;
      const g = tx.createRadialGradient(cx, cy, p.r * .05, cx, cy, p.r * 1.05);
      g.addColorStop(0, tone(hi, .85)); g.addColorStop(.5, tone(lerp(hi, base, .5), .45)); g.addColorStop(1, tone(base, 0));
      tx.fillStyle = g; tx.fillRect(cx - p.r * 1.1, cy - p.r * 1.1, p.r * 2.2, p.r * 2.2);
      // kümenin gölge tarafı: ışığın tersinde koyu hilal
      const sx = p.x + drift - lx * p.r * .55, sy = p.y - ly * p.r * .55;
      const sg = tx.createRadialGradient(sx, sy, p.r * .1, sx, sy, p.r * .9);
      sg.addColorStop(0, tone(base * .6, .5)); sg.addColorStop(1, tone(base, 0));
      tx.fillStyle = sg; tx.fillRect(sx - p.r, sy - p.r, p.r * 2, p.r * 2);
    }
    tx.restore();
    return { puffs, path: U };
  }
  // Duman sütunu: yükselen, genişleyen, kıvrılan kümeler (alttan ateşle aydınlanır)
  function smoke(o) {
    const r = rng(o.seed || 3), n = o.n || 14, t = o.t || 0;
    for (let i = 0; i < n; i++) {
      const f = i / (n - 1);
      const yy = o.y - f * o.h, rr = o.r0 + (o.r1 - o.r0) * f;
      const xx = o.x + Math.sin(f * 3.1 + (o.seed || 0) + t * .15) * o.sway * f + (r() - .5) * rr * .4;
      const P = new Path2D(); P.arc(xx, yy, rr * (.8 + r() * .4), 0, TAU);
      const g = tx.createRadialGradient(xx, yy + rr * .5, rr * .1, xx, yy, rr);
      const below = lerp(o.glow ?? .7, o.base ?? .2, f);
      g.addColorStop(0, tone(below)); g.addColorStop(1, tone((o.base ?? .2) * .8));
      fill(P, g, { th: (o.th ?? 0) + (r() - .5) * .25, ph: r(), id: 2 });
    }
  }

  // ── alev ──
  // Alev dili: tabandan (x, y) yukarı, yükseklik hgt, genişlik wid; t ile kıvrılır. Çizgiler alevin akışı yönünde.
  function flame(x, y, hgt, wid, t, seed = 0, o = {}) {
    const k = seed * 1.7, sway = o.sway ?? .45, sp = o.speed ?? 1;
    const m = 14, L = [], R = [];
    const curl = (o.curl ?? 1) * (hash(seed + .5) < .5 ? -1 : 1);
    const H0 = hgt * (.82 + .18 * Math.sin(t * 2.7 * sp + k * 2) + .08 * fbm1(t * 1.3 * sp + k, 2));
    let cx = x;
    const spine = [];
    for (let i = 0; i <= m; i++) {
      const f = i / m;
      // gövde: yukarı doğru kıvrılan S eğrisi; dalgalar yukarı akar (t ile)
      cx = x + Math.sin(f * 2.4 * PI * .5 + k) * wid * .35 * f * curl + Math.sin(f * 6.0 - t * 5.5 * sp + k) * wid * .22 * f * sway + fbm1(t * .8 * sp + k + f * 2, 3) * wid * .3 * f;
      spine.push([cx, y - f * H0]);
    }
    for (let i = 0; i <= m; i++) {
      const f = i / m, [sx, sy] = spine[i];
      const ww = wid * .5 * Math.pow(1 - f, .9) * (1 + .3 * Math.sin(f * 9 - t * 7 * sp + k * 3)) * (f < .12 ? .8 + f * 1.6 : 1);
      const j = i < m ? spine[i + 1] : spine[i], q = i > 0 ? spine[i - 1] : spine[i];
      const tg = Math.atan2(j[1] - q[1], j[0] - q[0]) + PI / 2;
      L.push([sx + Math.cos(tg) * ww, sy + Math.sin(tg) * ww]); R.push([sx - Math.cos(tg) * ww, sy - Math.sin(tg) * ww]);
    }
    const P = new Path2D(), all = [...L, ...R.reverse()];
    P.moveTo(all[0][0], all[0][1]);
    for (let i = 1; i < all.length; i++) { const a = all[i - 1], b = all[i]; P.quadraticCurveTo(a[0], a[1], (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); }
    P.closePath();
    const tip = spine[m];
    const g = tx.createLinearGradient(0, y, 0, tip[1]);
    g.addColorStop(0, tone(o.base ?? .5)); g.addColorStop(.25, tone(o.core ?? .96)); g.addColorStop(.75, tone(o.core ?? .96)); g.addColorStop(1, tone(o.tip ?? .7));
    const th = Math.atan2(tip[1] - y, tip[0] - x);
    fill(P, g, { fill: GR.patGrad(x, y, tip[0], tip[1], [[0, th + .3 * curl], [.5, th], [1, th - .35 * curl]], seed * .37, 3) });
    // iç gölge damarı: alev dilinin ortasında koyu, kıvrık iz (gravürde alevi alev yapan)
    tx.save(); tx.clip(P);
    tx.strokeStyle = tone(o.vein ?? .35, .55); tx.lineWidth = wid * .14; tx.lineCap = 'round';
    tx.beginPath(); spline(tx, spine.slice(2, m - 2).map(([sx, sy], i) => [sx + Math.sin(i * 1.3 + t * 3 + k) * wid * .12, sy]), false); tx.stroke();
    tx.restore();
    return P;
  }
  // Alev öbeği: bir çizgi boyunca birçok dil
  function flameBank(x0, x1, y, hgt, t, seed = 0, o = {}) {
    const r = rng(seed + 9), n = o.n || Math.round((x1 - x0) / (hgt * .35));
    for (let i = 0; i < n; i++) {
      const f = (i + r() * .8) / n, hh = hgt * (.45 + r() * .75) * (o.env ? o.env(f) : 1);
      flame(lerp(x0, x1, f), y + r() * hgt * .1, hh, hh * (o.wr ?? (.42 + r() * .22)), t + r() * 10, seed * 31 + i, o);
    }
  }

  // ── kaya ──
  // Köşeli kaya kütlesi: dış çizgi noktaları (pts), ışık yönü; ton + benekli çapraz tarama
  function rock(pts, o = {}) {
    const P = new Path2D(); poly(P, pts, true);
    const [lx, ly] = o.lit || [-.6, -.8];
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const [x, y] of pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2, rr = Math.max(x1 - x0, y1 - y0) / 2;
    const g = tx.createLinearGradient(cx + lx * rr, cy + ly * rr, cx - lx * rr, cy - ly * rr);
    g.addColorStop(0, tone(o.hi ?? .7)); g.addColorStop(.5, tone(o.mid ?? .35)); g.addColorStop(1, tone(o.lo ?? .08));
    fill(P, g, { th: o.th ?? -.7, ph: o.ph ?? 0, id: o.id ?? 4 });
    // yüzey kırıkları: kısa koyu çatlaklar ve açık sırtlar (ton katmanına)
    const r = rng(o.seed || 5);
    tx.save(); tx.clip(P); tx.lineCap = 'round';
    for (let i = 0; i < (o.cracks ?? 40); i++) {
      const sx = lerp(x0, x1, r()), sy = lerp(y0, y1, r()), a = (r() - .5) * 2.2 + (o.crackA ?? -.4), l = 10 + r() * rr * .25;
      tx.strokeStyle = tone(r() < .55 ? .05 : .85, .6); tx.lineWidth = 1 + r() * 2.5;
      tx.beginPath(); tx.moveTo(sx, sy);
      tx.quadraticCurveTo(sx + Math.cos(a + .4) * l * .5, sy + Math.sin(a + .4) * l * .5, sx + Math.cos(a) * l, sy + Math.sin(a) * l); tx.stroke();
    }
    tx.restore();
    return P;
  }

  // ── ışık huzmesi ──
  // Kaynak (sx, sy) çevresinde yayılan ışınlar: ton katmanında aydınlatır, desen katmanında çizgileri kaynağa doğru çevirir.
  function rays(sx, sy, a0, a1, n, reach, o = {}) {
    const r = rng(o.seed || 21), t = o.t || 0;
    for (let i = 0; i < n; i++) {
      const a = lerp(a0, a1, (i + r()) / n), da = (a1 - a0) / n * (.25 + r() * .5);
      const L = reach * (.6 + r() * .4), str = (o.str ?? .5) * (.5 + r() * .5) * (.75 + .25 * Math.sin(t * .7 + i * 1.3));
      tx.save(); tx.filter = `blur(${o.blur ?? 18}px)`;
      const P = new Path2D(); P.moveTo(sx, sy); P.lineTo(sx + Math.cos(a - da) * L, sy + Math.sin(a - da) * L);
      P.lineTo(sx + Math.cos(a + da) * L, sy + Math.sin(a + da) * L); P.closePath();
      const g = tx.createLinearGradient(sx, sy, sx + Math.cos(a) * L, sy + Math.sin(a) * L);
      g.addColorStop(0, `rgba(255,255,255,${str})`); g.addColorStop(1, 'rgba(255,255,255,0)');
      tx.globalCompositeOperation = 'lighter'; tx.fillStyle = g; tx.fill(P); tx.restore();
      if (o.pattern === true) { px.fillStyle = pat(a, 0, 7); px.fill(P); }
    }
  }
  // yumuşak ışık lekesi (ton katmanında aydınlatma ya da karartma)
  function glow(x, y, r0, r1, v, a = 1, op = 'lighter') {
    const g = tx.createRadialGradient(x, y, r0, x, y, r1);
    const c = Math.round(v * 255);
    g.addColorStop(0, `rgba(${c},${c},${c},${a})`); g.addColorStop(1, `rgba(${c},${c},${c},0)`);
    tx.save(); tx.globalCompositeOperation = op; tx.fillStyle = g; tx.fillRect(x - r1, y - r1, r1 * 2, r1 * 2); tx.restore();
  }

  // ── göl yüzeyi ──
  // Yatay dalgalı çizgiler; perspektifle uzakta sıklaşır (evre ve doğrultu gradyanı ile değil, katmanlı bantlarla)
  function lake(y0, y1, t, o = {}) {
    const bands = o.bands || 10;
    for (let i = 0; i < bands; i++) {
      const f0 = i / bands, f1 = (i + 1) / bands;
      const ya = lerp(y0, y1, Math.pow(f0, 1.7)), yb = lerp(y0, y1, Math.pow(f1, 1.7));
      const P = new Path2D(); P.rect(-200, ya, W + 400, yb - ya + 1);
      px.fillStyle = pat(Math.sin(i * 1.9 + t * .3) * .03, i * .37 + t * .05, 8); px.fill(P);
    }
  }

  // ── zincir ──
  function chain(x0, y0, x1, y1, link = 26, o = {}) {
    const L = Math.hypot(x1 - x0, y1 - y0), n = Math.floor(L / (link * .8)), a = Math.atan2(y1 - y0, x1 - x0);
    for (let i = 0; i < n; i++) {
      const f = (i + .5) / n, cx = lerp(x0, x1, f), cy = lerp(y0, y1, f) + Math.sin(f * PI) * (o.sag || 0);
      tx.save(); tx.translate(cx, cy); tx.rotate(a); if (i % 2) tx.scale(1, .35);
      tx.lineWidth = link * .18; tx.strokeStyle = tone(o.v ?? .15);
      tx.beginPath(); tx.ellipse(0, 0, link * .5, link * .3, 0, 0, TAU); tx.stroke(); tx.restore();
    }
  }
  return { cloud, smoke, flame, flameBank, rock, rays, glow, lake, chain };
})();
