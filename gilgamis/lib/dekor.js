// Kabartma dekor ilkelleri: sur, tuğla, sedir, hurma, yılan, bitki, dalga, kayık, güneş, ceylan, yatak, çivi yazısı şeridi. ORTAK DOSYA: başkan.
'use strict';
const DK = {};
(() => {
  const { sekil, cizgi, uzuv } = FIG;
  // yatay friz şeridi (silindir mühür baskısının kenarı): üstte ve altta yükseltilmiş bant
  DK.friz = (R, x0, x1, y0, y1, o = {}) => {
    R.b.fillStyle = gv(o.bant ?? .5);
    R.b.fillRect(x0, y0 - 40, x1 - x0, 40); R.b.fillRect(x0, y1, x1 - x0, 40);
    for (const yy of [y0 - 20, y1 + 20]) cizgi(R, [[x0, yy], [x1, yy]], 3, -.5);
  };
  // tuğla duvarı (pişmiş tuğla için malzeme rengi verilebilir)
  DK.tugla = (R, x0, y0, x1, y1, o = {}) => {
    const bw = o.bw || 64, bh = o.bh || 26, z = o.z ?? .45;
    R.b.fillStyle = gv(z); R.b.fillRect(x0, y0, x1 - x0, y1 - y0);
    if (o.renk) { R.m.fillStyle = o.renk; R.m.fillRect(x0, y0, x1 - x0, y1 - y0); }
    const r = rng(o.tohum || 3);
    R.d.strokeStyle = dv(-.75); R.d.lineWidth = o.lw || 3;
    for (let y = y0, row = 0; y < y1; y += bh, row++) {
      R.d.beginPath(); R.d.moveTo(x0, y); R.d.lineTo(x1, y); R.d.stroke();
      for (let x = x0 + (row % 2) * bw / 2; x < x1; x += bw) { R.d.beginPath(); R.d.moveTo(x, y); R.d.lineTo(x, Math.min(y1, y + bh)); R.d.stroke(); }
      if (o.renk) for (let x = x0; x < x1; x += bw) { R.m.fillStyle = `rgba(${90 + r() * 40},${40 + r() * 25},${20 + r() * 15},${.12 + r() * .14})`; R.m.fillRect(x + (row % 2) * bw / 2, y, bw, bh); }
    }
  };
  // sur: burçlu duvar ve kuleler (yan görünüş)
  DK.sur = (R, x0, x1, yTaban, yUst, o = {}) => {
    const z = o.z ?? .5, kw = o.kule || 150, ara = o.ara || 520, burc = o.burc || 34;
    DK.tugla(R, x0, yUst, x1, yTaban, { z, bw: o.bw || 56, bh: o.bh || 24, renk: o.renk, tohum: 9 });
    // kuleler
    for (let x = x0 + (o.kayma || 80); x < x1; x += ara) {
      DK.tugla(R, x, yUst - 90, x + kw, yTaban, { z: z + .1, bw: o.bw || 56, bh: o.bh || 24, renk: o.renk, tohum: x | 0 });
      cizgi(R, [[x, yUst - 90], [x, yTaban]], 4, -.8); cizgi(R, [[x + kw, yUst - 90], [x + kw, yTaban]], 4, -.8);
      for (let b = x; b < x + kw - 10; b += burc * 1.6) { R.b.fillStyle = gv(z + .1); R.b.fillRect(b, yUst - 90 - burc, burc, burc); cizgi(R, [[b, yUst - 90], [b, yUst - 90 - burc], [b + burc, yUst - 90 - burc], [b + burc, yUst - 90]], 3, -.7); }
    }
    for (let b = x0; b < x1; b += burc * 1.6) { R.b.fillStyle = gv(z); R.b.fillRect(b, yUst - burc, burc, burc); cizgi(R, [[b, yUst], [b, yUst - burc], [b + burc, yUst - burc], [b + burc, yUst]], 3, -.7); if (o.renk) { R.m.fillStyle = o.renk; R.m.fillRect(b, yUst - burc, burc, burc); } }
  };
  // sedir: katmanlı yatay dallar (Mezopotamya kabartmasında koni biçimli)
  DK.sedir = (R, x, y, hh, o = {}) => {
    const z = o.z ?? .55, k = hh / 600;
    uzuv(R, [x, y], [x, y - hh * .95], 30 * k, 14 * k, z - .05);
    const n = o.kat || 8;
    for (let i = 0; i < n; i++) {
      const u = i / n, yy = y - hh * (.2 + u * .78), wd = (1 - u) * 190 * k + 30 * k;
      const pts = [[x - wd, yy + 14 * k], [x - wd * .6, yy - 22 * k], [x, yy - 40 * k], [x + wd * .6, yy - 22 * k], [x + wd, yy + 14 * k], [x, yy + 4 * k]];
      sekil(R, pts, z + u * .05, .5);
      for (let q = -3; q <= 3; q++) cizgi(R, [[x + q * wd * .12, yy - 8 * k], [x + q * wd * .27, yy + 8 * k]], Math.max(1, 2.5 * k), -.5);
    }
  };
  // hurma (palmet)
  DK.hurma = (R, x, y, hh, o = {}) => {
    const z = o.z ?? .55, k = hh / 500;
    const ust = [x + (o.egri || 0) * k, y - hh];
    for (let i = 0; i < 10; i++) { const u = i / 10; const p = [lerp(x, ust[0], u), lerp(y, ust[1], u)]; uzuv(R, p, [lerp(x, ust[0], u + .1), lerp(y, ust[1], u + .1)], 22 * k, 20 * k, z - .05, .7); }
    for (let i = 0; i < 9; i++) {
      const a = -PI * .95 + i * PI * .9 / 8, L = 150 * k;
      const e = [ust[0] + Math.cos(a) * L, ust[1] + Math.sin(a) * L * .75 + (Math.abs(Math.cos(a)) > .5 ? 40 * k : 0)];
      const m = [lerp(ust[0], e[0], .5), lerp(ust[1], e[1], .5) - 25 * k];
      const pts = [ust, m, e, [m[0], m[1] + 16 * k]];
      sekil(R, pts, z + .04, .5);
      cizgi(R, [ust, m, e], Math.max(1, 2.5 * k), -.6);
    }
    if (o.meyve) for (let i = 0; i < 7; i++) { R.b.fillStyle = gv(z + .08); R.b.beginPath(); R.b.arc(ust[0] - 20 * k + (i % 4) * 14 * k, ust[1] + 30 * k + Math.floor(i / 4) * 14 * k, 8 * k, 0, TAU); R.b.fill(); }
  };
  // kamış
  DK.kamis = (R, x, y, hh, n = 7, z = .5) => { for (let i = 0; i < n; i++) { const xx = x + i * 14, tt = hh * (.7 + hash(i * 3.1 + x) * .3); uzuv(R, [xx, y], [xx + (hash(i) - .5) * 20, y - tt], 6, 4, z, .5); sekil(R, [[xx - 4, y - tt], [xx + 5, y - tt - 40], [xx + 10, y - tt]], z + .03, .4); } };
  // dalga şeridi (spiral kıvrım)
  DK.dalga = (R, x0, x1, y, o = {}) => {
    const p = o.p || 120, a = o.a || 22, z = o.z ?? .4, faz = o.faz || 0;
    R.b.fillStyle = gv(z);
    R.b.beginPath(); R.b.moveTo(x0, y + 60);
    for (let x = x0; x <= x1; x += 6) R.b.lineTo(x, y + Math.sin((x / p) * TAU + faz) * a);
    R.b.lineTo(x1, y + 400); R.b.lineTo(x0, y + 400); R.b.closePath(); R.b.fill();
    for (let x = x0 - p + ((faz / TAU * p) % p); x < x1; x += p) { R.d.strokeStyle = dv(-.6); R.d.lineWidth = o.lw || 3.5; R.d.beginPath(); for (let t = 0; t < 1.7 * TAU; t += .2) { const r = 6 + t * 3.2; const px = x + p * .25 + Math.cos(t + PI) * r, py = y + 18 + Math.sin(t + PI) * r * .8; t === 0 ? R.d.moveTo(px, py) : R.d.lineTo(px, py); } R.d.stroke(); }
    if (o.renk) { R.m.fillStyle = o.renk; R.m.beginPath(); R.m.moveTo(x0, y + 60); for (let x = x0; x <= x1; x += 6) R.m.lineTo(x, y + Math.sin((x / p) * TAU + faz) * a); R.m.lineTo(x1, y + 400); R.m.lineTo(x0, y + 400); R.m.closePath(); R.m.fill(); }
  };
  // kayık (yüksek pruvalı kamış kayığı)
  DK.kayik = (R, x, y, L, o = {}) => {
    const z = o.z ?? .62, k = L / 600;
    const pts = [[x - L / 2, y - 120 * k], [x - L / 2 + 40 * k, y - 20 * k], [x - L * .3, y + 10 * k], [x + L * .3, y + 10 * k], [x + L / 2 - 40 * k, y - 20 * k], [x + L / 2, y - 140 * k], [x + L / 2 - 20 * k, y - 150 * k], [x + L * .38, y - 20 * k], [x - L * .38, y - 18 * k], [x - L / 2 + 22 * k, y - 132 * k]];
    sekil(R, pts, z, .55, null, .6);
    for (let i = -6; i <= 6; i++) cizgi(R, [[x + i * L * .06, y - 18 * k], [x + i * L * .06 + 6 * k, y + 6 * k]], Math.max(1, 3 * k), -.5);
  };
  // güneş kursu (Şamaş): disk + dalgalı ışınlar (yıldız biçimi yok: haç çağrışımından kaçınılır)
  DK.gunes = (R, x, y, r, o = {}) => {
    const z = o.z ?? .62;
    R.b.fillStyle = gv(z); R.b.beginPath(); R.b.arc(x, y, r, 0, TAU); R.b.fill();
    R.d.strokeStyle = dv(-.7); R.d.lineWidth = Math.max(2, r * .04); R.d.beginPath(); R.d.arc(x, y, r * .82, 0, TAU); R.d.stroke();
    for (let i = 0; i < 24; i++) { const a = i / 24 * TAU + (o.faz || 0); const pts = []; for (let t = 0; t <= 1; t += .1) { const rr = r * (1.1 + t * .55); pts.push([x + Math.cos(a + Math.sin(t * 6) * .05) * rr, y + Math.sin(a + Math.sin(t * 6) * .05) * rr]); } cizgi(R, pts, Math.max(2, r * .05), .7); }
  };
  // yılan (kalınlığı azalan eğri; pts: omurga noktaları, baştan kuyruğa)
  DK.yilan = (R, pts, w, o = {}) => {
    const z = o.z ?? .72, n = pts.length;
    for (let i = n - 1; i > 0; i--) { const u = i / (n - 1); uzuv(R, pts[i], pts[i - 1], w * (1 - u * .85), w * (1 - (i - 1) / (n - 1) * .85), z, i % 2 ? .35 : 0); }
    // pullar: sıra sıra küçük yaylar
    for (let i = 1; i < n - 1; i++) { const a = pts[i], b = pts[i + 1], ang = Math.atan2(b[1] - a[1], b[0] - a[0]), ww = w * (1 - i / (n - 1) * .85);
      R.d.save(); R.d.translate(a[0], a[1]); R.d.rotate(ang); R.d.strokeStyle = dv(-.55); R.d.lineWidth = Math.max(1, ww * .08);
      for (let q = -1; q <= 1; q++) { R.d.beginPath(); R.d.arc(0, q * ww * .25, ww * .18, -PI / 2, PI / 2); R.d.stroke(); }
      R.d.restore(); }
    const bh = pts[0], b2 = pts[1], ang = Math.atan2(bh[1] - b2[1], bh[0] - b2[0]);
    R.b.save(); R.b.translate(bh[0], bh[1]); R.b.rotate(ang); R.b.fillStyle = gv(z + .03); R.b.beginPath(); R.b.ellipse(w * .25, 0, w * .75, w * .5, 0, 0, TAU); R.b.fill(); R.b.restore();
    R.d.save(); R.d.translate(bh[0], bh[1]); R.d.rotate(ang); R.d.fillStyle = dv(-.9); R.d.beginPath(); R.d.arc(w * .45, -w * .2, w * .1, 0, TAU); R.d.fill(); R.d.restore();
  };
  // dikenli bitki
  DK.bitki = (R, x, y, s, o = {}) => {
    const z = o.z ?? .78;
    uzuv(R, [x, y], [x + s * .05, y - s], s * .05, s * .03, z, .5);
    for (let i = 0; i < 7; i++) { const u = .2 + i * .11, p = [x + s * .05 * u, y - s * u], sd = i % 2 ? 1 : -1;
      sekil(R, [p, [p[0] + sd * s * .2, p[1] - s * .12], [p[0] + sd * s * .32, p[1] - s * .05], [p[0] + sd * s * .18, p[1] + s * .02]], z + .02, .5);
      for (let q = 0; q < 3; q++) cizgi(R, [[p[0] + sd * s * (.1 + q * .07), p[1] - s * (.06 + q * .01)], [p[0] + sd * s * (.12 + q * .07), p[1] - s * (.12 + q * .01)]], Math.max(1, s * .012), .8);
    }
  };
  // ceylan (profil)
  DK.ceylan = (R, x, y, s, o = {}) => {
    const f = o.f ?? 1, z = o.z ?? .62, k = s;
    for (const c of [R.b, R.d, R.m]) { c.save(); c.translate(x, y); c.scale(f, 1); }
    const ac = o.kos ? Math.sin(o.kos) * .5 : 0;
    const leg = (hx, a) => { const knee = [hx + Math.sin(a) * k * .18, -k * .3 + Math.cos(a) * k * .02]; uzuv(R, [hx, -k * .42], knee, k * .05, k * .03, z - .05); uzuv(R, knee, [knee[0] + Math.sin(a * .5) * k * .1, 0], k * .03, k * .02, z - .05); };
    leg(-k * .2, -ac); leg(k * .2, ac);
    sekil(R, [[-k * .3, -k * .45], [-k * .2, -k * .58], [k * .15, -k * .6], [k * .3, -k * .7], [k * .38, -k * .88], [k * .48, -k * .86], [k * .42, -k * .74], [k * .32, -k * .45], [0, -k * .38]], z, .5);
    cizgi(R, [[k * .4, -k * .88], [k * .3, -k * 1.1], [k * .38, -k * 1.2]], Math.max(1.5, k * .025), .7);
    cizgi(R, [[k * .43, -k * .88], [k * .36, -k * 1.08], [k * .45, -k * 1.15]], Math.max(1.5, k * .022), .7);
    R.d.fillStyle = dv(-.9); R.d.beginPath(); R.d.arc(k * .42, -k * .82, k * .012, 0, TAU); R.d.fill();
    leg(-k * .16, ac * .7); leg(k * .24, -ac * .7);
    for (const c of [R.b, R.d, R.m]) c.restore();
  };
  // yatak (yatan beden için): sedir ayaklı karyola
  DK.yatak = (R, x0, x1, y, o = {}) => {
    const z = o.z ?? .55;
    R.b.fillStyle = gv(z); R.b.fillRect(x0, y, x1 - x0, 34);
    cizgi(R, [[x0, y + 34], [x1, y + 34]], 3, -.7);
    for (const xx of [x0 + 20, x1 - 60]) { uzuv(R, [xx + 20, y + 30], [xx + 20, y + 150], 30, 22, z, .6); sekil(R, [[xx, y + 150], [xx + 40, y + 150], [xx + 34, y + 175], [xx + 6, y + 175]], z, .5); }
    for (let x = x0 + 40; x < x1 - 40; x += 40) cizgi(R, [[x, y + 6], [x + 20, y + 28]], 2.5, -.5);
  };
  // çivi yazısı şeridi (süs; okunacak metin değildir): kama gruplarıyla dolu satırlar, dünya koordinatında
  DK.civi = (R, x0, y0, x1, y1, o = {}) => {
    const sh = o.sh || 46, r = rng(o.tohum || 5), sz = o.sz || 15;
    R.d.lineCap = 'butt';
    for (let y = y0 + sh * .6; y < y1; y += sh) {
      cizgi(R, [[x0, y + sh * .42], [x1, y + sh * .42]], 1.6, -.35);
      let x = x0 + r() * 8;
      while (x < x1 - 20) {
        const n = 1 + Math.floor(r() * 4);
        for (let i = 0; i < n; i++) {
          const t = r(); const cx = x + i * sz * .7, cy = y + (r() - .5) * sz * .4;
          R.d.fillStyle = dv(-.85);
          if (t < .55) { R.d.beginPath(); R.d.moveTo(cx - sz * .3, cy - sz * .5); R.d.lineTo(cx + sz * .3, cy - sz * .5); R.d.lineTo(cx, cy - sz * .1); R.d.fill(); cizgi(R, [[cx, cy - sz * .2], [cx, cy + sz * .5]], Math.max(1, sz * .12), -.75); }
          else if (t < .85) { R.d.beginPath(); R.d.moveTo(cx - sz * .5, cy - sz * .3); R.d.lineTo(cx - sz * .5, cy + sz * .3); R.d.lineTo(cx - sz * .1, cy); R.d.fill(); cizgi(R, [[cx - sz * .2, cy], [cx + sz * .5, cy]], Math.max(1, sz * .12), -.75); }
          else { R.d.beginPath(); R.d.moveTo(cx - sz * .3, cy - sz * .3); R.d.lineTo(cx + sz * .3, cy - sz * .1); R.d.lineTo(cx - sz * .1, cy + sz * .3); R.d.fill(); }
        }
        x += n * sz * .7 + sz * (.5 + r() * .7);
      }
    }
    R.d.lineCap = 'round';
  };
  // tablet: yuvarlak köşeli kil levha
  DK.tablet = (R, x, y, wdt, hgt, o = {}) => {
    const z = o.z ?? .55, r = Math.min(wdt, hgt) * .08;
    R.b.fillStyle = gv(z); R.b.beginPath(); R.b.roundRect(x - wdt / 2, y - hgt / 2, wdt, hgt, r); R.b.fill();
    if (o.renk) { R.m.fillStyle = o.renk; R.m.beginPath(); R.m.roundRect(x - wdt / 2, y - hgt / 2, wdt, hgt, r); R.m.fill(); }
    if (o.yazi !== false) DK.civi(R, x - wdt / 2 + wdt * .06, y - hgt / 2 + hgt * .04, x + wdt / 2 - wdt * .06, y + hgt / 2 - hgt * .06, { sh: o.sh || hgt / 14, sz: o.sz || hgt / 40, tohum: o.tohum || 2 });
    if (o.kirik) { R.b.fillStyle = gv(o.zemin ?? .18); R.b.beginPath(); poly(R.b, o.kirik); R.b.fill(); }
  };
})();
