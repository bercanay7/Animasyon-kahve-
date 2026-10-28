// Taş baskı üslubu: kâğıt, renk kalıpları (multiply + sabit kayık baskı), yarım ton, kırık mürekkep, taş greni
// Çizim modeli: her nesne önce kâğıt rengiyle "boşaltılır" (knock), sonra kalıpları çarpma ile basılır, en son is (mürekkep) çizgisi gelir.
'use strict';
const P = {
  paper: '#EEE4CD', paperD: '#DCCFB2', ink: '#211D1B', red: '#B3332B', navy: '#273650', khaki: '#867A50',
  ochre: '#C4903F', gold: '#E2B04A', teal: '#3E7774', skin: '#E7BC96', grey: '#5E5A55', sepia: '#6E4C33',
  eye: '#8FB3CF',
};
function makeCanvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function hexRGB(c) { const n = parseInt(c.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function rgba(c, a) { const [r, g, b] = hexRGB(c); return `rgba(${r},${g},${b},${a})`; }

// ——— kayık baskı: her kalıbın çekim boyunca sabit küçük kayması ———
const REG = { seed: 1, amt: 2, boost: 1 };
function setReg(seed, amt = 2) { REG.seed = seed; REG.amt = amt; }
function regOf(plate) {
  if (plate === 'ink' || plate === 'paper') return [0, 0];
  const r = rng(REG.seed * 131 + plate.length * 17 + plate.charCodeAt(0) * 7);
  const k = 3.6 * REG.amt * REG.boost; return [(r() - .5) * k, (r() - .5) * k];
}
// yol: Path2D ya da (ctx)=>{...} çizim fonksiyonu
function _path(ctx, p) { if (p instanceof Path2D) return p; const q = new Path2D(); p(q); return q; }
// kâğıt rengiyle boşalt (arkadakini örter)
function knock(ctx, p, col = P.paper) { ctx.save(); ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = col; ctx.fill(_path(ctx, p)); ctx.restore(); }
// kalıp bas: çarpma, kayık; n=2 ikinci baskı (koyu ton)
// taş baskı mürekkebi: düz renk yerine hafif benekli (alfa .78–1) karo; kalıp başına ayrı ofset
const MOT = {};
function mottle(ctx, name) {
  const col = P[name] || name;
  if (!MOT[col]) {
    const n = 384, c = makeCanvas(n, n), x = c.getContext('2d'), id = x.createImageData(n, n), [r, g, b] = hexRGB(col);
    for (let y = 0; y < n; y++) for (let X = 0; X < n; X++) {
      // döşemede dikiş olmasın diye periyodik gürültü (karo kenarları sarılır)
      const u = X / n * TAU, v = y / n * TAU;
      const f = .5 + .25 * Math.sin(u * 3 + Math.sin(v * 2) * 1.3) * Math.cos(v * 4 + Math.cos(u * 3)) + .25 * (hash2(X % n, y % n, 7) - .5);
      const k = (y * n + X) * 4; id.data[k] = r; id.data[k + 1] = g; id.data[k + 2] = b; id.data[k + 3] = 255 * (.8 + .2 * clamp(f));
    }
    x.putImageData(id, 0, 0); MOT[col] = c;
  }
  const pat = ctx.createPattern(MOT[col], 'repeat');
  const sd = name.charCodeAt(0) * 37 + name.length * 91; pat.setTransform(new DOMMatrix().translateSelf(sd % 384, (sd * 7) % 384));
  return pat;
}
function plate(ctx, name, p, o = {}) {
  const q = _path(ctx, p), [dx, dy] = regOf(name);
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha *= (o.a ?? 1); /* kapsayıcının saydamlığı korunur */ ctx.translate(dx, dy);
  ctx.fillStyle = (name === 'ink' || o.flat) ? (P[name] || name) : mottle(ctx, name);
  for (let i = 0; i < (o.n || 1); i++) ctx.fill(q);
  ctx.restore();
}
// yarım ton kalıbı: yol içinde sabit yoğunluklu nokta deseni
const HT = {};
function htPattern(ctx, col, dens, cell, ang) {
  const key = [col, dens.toFixed(2), cell, ang, RS].join('|');
  if (!HT[key]) {
    const c = makeCanvas(Math.ceil(cell * RS), Math.ceil(cell * RS)), x = c.getContext('2d');
    x.scale(RS, RS); x.fillStyle = col;
    const rr = cell * Math.sqrt(clamp(dens, 0, .78) / PI);
    x.beginPath(); x.arc(cell / 2, cell / 2, rr, 0, TAU); x.fill();
    if (dens > .78) { x.fillRect(0, 0, cell, cell); }
    const pat = x.createPattern(c, 'repeat');
    HT[key] = { c };
  }
  const pat = ctx.createPattern(HT[key].c, 'repeat');
  const m = new DOMMatrix(); m.rotateSelf(ang); m.scaleSelf(1 / RS, 1 / RS); pat.setTransform(m);
  return pat;
}
function halftone(ctx, name, p, dens, o = {}) {
  const q = _path(ctx, p), [dx, dy] = regOf(name);
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha *= (o.a ?? 1); /* kapsayıcının saydamlığı korunur */ ctx.translate(dx, dy);
  ctx.fillStyle = htPattern(ctx, P[name] || name, dens, o.cell || 12, o.ang ?? (name === 'ink' ? 45 : 15));
  ctx.fill(q); ctx.restore();
}
// ışığa göre değişen raster (hale): merkezde d0, dışta d1 yoğunluk; sonuç önbelleğe alınabilir
function radialHT(ctx, name, cx, cy, r0, r1, d0, d1, o = {}) {
  const [dx, dy] = regOf(name), cell = o.cell || 13, ang = (o.ang ?? 15) * PI / 180, ca = Math.cos(ang), sa = Math.sin(ang);
  const R = Math.max(o.extent || r1, 10);
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = P[name] || name; ctx.translate(dx, dy);
  if (o.clip) ctx.clip(_path(ctx, o.clip));
  ctx.beginPath();
  const x0 = o.box ? o.box[0] : cx - R, y0 = o.box ? o.box[1] : cy - R, x1 = o.box ? o.box[2] : cx + R, y1 = o.box ? o.box[3] : cy + R;
  const span = Math.hypot(x1 - x0, y1 - y0);
  for (let v = -span; v <= span; v += cell) for (let u = -span; u <= span; u += cell) {
    const x = (x0 + x1) / 2 + u * ca - v * sa, y = (y0 + y1) / 2 + u * sa + v * ca;
    if (x < x0 - cell || x > x1 + cell || y < y0 - cell || y > y1 + cell) continue;
    const d = Math.hypot((x - cx) / (o.sx || 1), (y - cy) / (o.sy || 1));
    const dens = lerp(d0, d1, smooth(inv(r0, r1, d)));
    if (dens <= .015) continue;
    const rr = cell * Math.sqrt(Math.min(dens, .9) / PI);
    ctx.moveTo(x + rr, y); ctx.arc(x, y, rr, 0, TAU);
  }
  ctx.fill(); ctx.restore();
}
// mürekkep çizgisi (is) ve kazıma (kâğıt rengi çizgi, koyu kütle içinde)
function inkStroke(ctx, p, w, o = {}) {
  ctx.save(); ctx.globalCompositeOperation = o.mode || 'source-over'; ctx.strokeStyle = o.col || P.ink; ctx.lineWidth = w;
  ctx.lineCap = o.cap || 'round'; ctx.lineJoin = 'round'; ctx.globalAlpha *= (o.a ?? 1); /* kapsayıcının saydamlığı korunur */
  ctx.stroke(_path(ctx, p)); ctx.restore();
}
function inkFill(ctx, p, o = {}) { ctx.save(); ctx.globalAlpha *= (o.a ?? 1); /* kapsayıcının saydamlığı korunur */ ctx.fillStyle = o.col || P.ink; ctx.fill(_path(ctx, p)); ctx.restore(); }
function cut(ctx, p, w, o = {}) { inkStroke(ctx, p, w, { col: o.col || P.paper, ...o }); }

// ——— kırık kenar: nokta listesine sabit tohumlu gürültü ———
function rough(pts, amp = 1.2, seed = 1) {
  const r = rng(seed);
  return pts.map(([x, y]) => [x + (r() - .5) * 2 * amp, y + (r() - .5) * 2 * amp]);
}
// Catmull-Rom → bezier
function spl(p, pts, closed = true, k = 1) {
  const n = pts.length; if (n < 2) return p;
  const P_ = i => pts[closed ? (i + n) % n : clamp(i, 0, n - 1)];
  p.moveTo(pts[0][0], pts[0][1]);
  const m = closed ? n : n - 1;
  for (let i = 0; i < m; i++) {
    const p0 = P_(i - 1), p1 = P_(i), p2 = P_(i + 1), p3 = P_(i + 2);
    p.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k, p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k, p2[0], p2[1]);
  }
  if (closed) p.closePath();
  return p;
}
const SP = (pts, closed = true, k = 1) => spl(new Path2D(), pts, closed, k);
const PL = (pts, closed = true) => { const p = new Path2D(); pts.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); if (closed) p.closePath(); return p; };
// yerel dönüşümlü nokta listesi
function tf(pts, x, y, s, dir = 1, rot = 0) { const c = Math.cos(rot), sn = Math.sin(rot); return pts.map(([a, b]) => { const u = a * dir * s, v = b * s; return [x + u * c - v * sn, y + u * sn + v * c]; }); }

// ——— dokular ———
const TEX = {};
function buildPaper() {
  const r = rng(11);
  const c = makeCanvas(W, H), x = c.getContext('2d');
  const big = makeCanvas(W / 4, H / 4), bx = big.getContext('2d'), id = bx.createImageData(big.width, big.height);
  for (let y = 0; y < big.height; y++) for (let X = 0; X < big.width; X++) {
    let v = 0, a = .55, f = 1 / 60;
    for (let o = 0; o < 4; o++) { v += a * noise2(X * f, y * f, o + 21); a *= .5; f *= 2.1; }
    const k = (y * big.width + X) * 4, g = 247 + (v - .5) * 26;
    id.data[k] = g; id.data[k + 1] = g * .992; id.data[k + 2] = g * .978; id.data[k + 3] = 255;
  }
  bx.putImageData(id, 0, 0); x.imageSmoothingQuality = 'high'; x.drawImage(big, 0, 0, W, H);
  for (let i = 0; i < 1600; i++) { // lifler
    const px = r() * W, py = r() * H, L = 5 + r() * 24, a = r() * TAU;
    x.strokeStyle = `rgba(${r() < .5 ? '140,118,92' : '255,253,248'},${.05 + r() * .09})`; x.lineWidth = .5 + r() * .8;
    x.beginPath(); x.moveTo(px, py); x.quadraticCurveTo(px + Math.cos(a) * L * .5 + (r() - .5) * 5, py + Math.sin(a) * L * .5 + (r() - .5) * 5, px + Math.cos(a) * L, py + Math.sin(a) * L); x.stroke();
  }
  const sp = x.getImageData(0, 0, W, H), d = sp.data;
  for (let i = 0; i < d.length; i += 4) { const n = (r() - .5) * 9; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
  x.putImageData(sp, 0, 0);
  TEX.paper = c;
  // taş greni: mürekkebin tutmadığı benekler (lighten ile kâğıt rengi; kâğıtta etkisiz, boyalı yerde açık benek)
  const g = makeCanvas(W, H), gx = g.getContext('2d'), gd = gx.createImageData(W, H);
  const [pr, pg, pb] = hexRGB(P.paper);
  for (let y = 0; y < H; y++) for (let X = 0; X < W; X++) {
    const v = noise2(X / 2.3, y / 2.3, 51) * .55 + noise2(X / 9, y / 9, 52) * .45;
    const a = clamp((v - .765) / .05);
    if (a > 0) { const k = (y * W + X) * 4; gd.data[k] = pr; gd.data[k + 1] = pg; gd.data[k + 2] = pb; gd.data[k + 3] = a * 235; }
  }
  gx.putImageData(gd, 0, 0); TEX.stone = g;
  TEX.grain = [];
  for (let k = 0; k < 6; k++) {
    const gc = makeCanvas(512, 512), q = gc.getContext('2d'), im = q.createImageData(512, 512);
    for (let i = 0; i < im.data.length; i += 4) { const v = 128 + (r() + r() + r() - 1.5) * 60; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
    q.putImageData(im, 0, 0); TEX.grain.push(gc);
  }
  const vg = makeCanvas(W, H), vx = vg.getContext('2d');
  const gr = vx.createRadialGradient(W / 2, H * .5, H * .38, W / 2, H * .5, H * 1.08);
  gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(.7, 'rgba(40,26,12,.08)'); gr.addColorStop(1, 'rgba(30,18,8,.32)');
  vx.fillStyle = gr; vx.fillRect(0, 0, W, H); TEX.vig = vg;
}
function paperBG(ctx, col = P.paper) { ctx.fillStyle = col; ctx.fillRect(-20, -20, W + 40, H + 40); }
// son işlem: taş greni (mürekkepte açık benek), kâğıt lifi, gren, vinyet. ox,oy: doku kayması (katmana bağlı doku için)
// kamera dönüşümünde ekranın dört köşesi dokunun pay bırakılmış alanında mı (değilse doku ekrana sabit çizilir)
function texCamOk(c) {
  const co = Math.cos(-c.r), si = Math.sin(-c.r);
  return [[0, 0], [W, 0], [0, H], [W, H]].every(([x, y]) => {
    const dx = x - W / 2 - c.sx, dy = y - H / 2 - c.sy, wx = (dx * co - dy * si) / c.z + c.cx, wy = (dx * si + dy * co) / c.z + c.cy;
    return wx > -155 && wx < W + 155 && wy > -155 && wy < H + 155;
  });
}
function pressFinish(ctx, t, o = {}) {
  ctx.save(); baseT(ctx);
  const ox = o.ox || 0, oy = o.oy || 0;
  // taş greni ve kâğıt lifi sahneyle aynı kamera hareketini izler (sanat yönetmeni: "doku kâğıda bağlı"); vinyet ekrana sabit
  ctx.save(); const dr = o.drift, cm = o.cam && texCamOk(o.cam) ? o.cam : null;
  if (dr) { ctx.translate(W / 2, H / 2); ctx.scale(dr.z, dr.z); ctx.translate(-W / 2 - dr.px, -H / 2 - dr.py); }
  else if (cm) { ctx.translate(W / 2 + cm.sx, H / 2 + cm.sy); ctx.rotate(cm.r); ctx.scale(cm.z, cm.z); ctx.translate(-cm.cx, -cm.cy); }
  // çekimin kendi kamerası varsa doku pay bırakılarak (±TM) çizilir ki kayan kamerada kenar açılmasın
  const TM = cm ? 160 : 0;
  if (o.stone !== 0) { ctx.globalCompositeOperation = 'lighten'; ctx.globalAlpha = o.stone ?? .25;
    if (TM) ctx.drawImage(TEX.stone, -TM, -TM, W + 2 * TM, H + 2 * TM);
    else { ctx.drawImage(TEX.stone, ox % W, oy % H); if (ox) ctx.drawImage(TEX.stone, ox % W + (ox > 0 ? -W : W), oy % H); } }
  ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = o.paper ?? 1;
  if (TM) ctx.drawImage(TEX.paper, -TM, -TM, W + 2 * TM, H + 2 * TM); else ctx.drawImage(TEX.paper, 0, 0);
  ctx.restore();
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = o.vig ?? .9; ctx.drawImage(TEX.vig, 0, 0);
  ctx.restore();
  const amt = o.grain ?? .045;
  if (amt > 0) {
    const L = TEX.grain.length, i = ((Math.floor(t * 24) % L) + L) % L, r = rng(Math.floor(t * 24) + 1);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = amt;
    const gx = -r() * 512, gy = -r() * 512;
    for (let y = gy; y < DH; y += 512) for (let x = gx; x < DW; x += 512) ctx.drawImage(TEX.grain[i], x, y);
    ctx.restore();
  }
}

// ——— yazı ———
// yazı tiplerinde olmayan işaretler (→ ● ■ ▌) vektörle çizilir (tipografi kurulu: yedek yazı tipine düşmesin)
const TXT_GLYPH = /[→●■▌]/;
function txt(ctx, s, x, y, font, o = {}) {
  ctx.save(); ctx.font = font; ctx.textAlign = o.align || 'left'; ctx.textBaseline = o.base || 'alphabetic';
  if (o.ls) ctx.letterSpacing = o.ls + 'px';
  if (o.ws) ctx.wordSpacing = o.ws;
  let dx = 0, dy = 0;
  if (o.plate) { [dx, dy] = regOf(o.plate); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = P[o.plate]; }
  else { ctx.fillStyle = o.col || P.ink; ctx.globalAlpha *= (o.a ?? 1); /* kapsayıcının saydamlığı korunur */ }
  if (!TXT_GLYPH.test(s)) { ctx.fillText(s, x + dx, y + dy); ctx.restore(); return; }
  // parçala: düz metin + çizilen işaretler; hizalama toplam genişliğe göre
  const em = parseFloat((/(\d+(?:\.\d+)?)px/.exec(font) || [0, 40])[1]);
  const gw = { '→': .95 * em, '●': .62 * em, '■': .62 * em, '▌': .6 * em };
  const segs = s.split(/([→●■▌])/).filter(q => q !== '');
  const wOf = q => gw[q] ?? ctx.measureText(q).width;
  const tot = segs.reduce((a, q) => a + wOf(q), 0);
  let cx = (o.align === 'center' ? x - tot / 2 : o.align === 'right' ? x - tot : x) + dx;
  const by = y + dy, mid = o.base === 'middle' ? by : by - .34 * em;
  ctx.textAlign = 'left';
  for (const q of segs) {
    const w = wOf(q);
    if (q === '→') {
      ctx.save(); ctx.strokeStyle = ctx.fillStyle; ctx.lineWidth = Math.max(2.6, em * .075); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      const x0 = cx + .1 * em, x1 = cx + w - .12 * em; ctx.beginPath(); ctx.moveTo(x0, mid); ctx.lineTo(x1, mid); ctx.moveTo(x1 - .26 * em, mid - .2 * em); ctx.lineTo(x1, mid); ctx.lineTo(x1 - .26 * em, mid + .2 * em); ctx.stroke(); ctx.restore();
    } else if (q === '●') { ctx.beginPath(); ctx.arc(cx + w / 2, mid, .22 * em, 0, TAU); ctx.fill(); }
    else if (q === '■') ctx.fillRect(cx + w / 2 - .21 * em, mid - .21 * em, .42 * em, .42 * em);
    else if (q === '▌') ctx.fillRect(cx + .05 * em, (o.base === 'middle' ? by + .36 * em : by) - .75 * em, .55 * em, .75 * em);
    else ctx.fillText(q, cx, by);
    cx += w;
  }
  ctx.restore();
}
// soyut Osmanlıca yazı izi: sağdan sola kısa kıvrımlar ve noktalar (okunur bir metin değildir)
function scriptLine(ctx, x1, y, len, h, seed, o = {}) {
  const r = rng(seed), p = new Path2D(); let x = x1;
  while (x > x1 - len) {
    const w = h * (.6 + r() * 1.6), k = r();
    p.moveTo(x, y);
    if (k < .35) { p.quadraticCurveTo(x - w * .5, y + h * .25, x - w, y); }
    else if (k < .6) { p.lineTo(x - w * .3, y); p.lineTo(x - w * .3, y - h * (.8 + r() * .6)); p.moveTo(x - w * .3, y); p.quadraticCurveTo(x - w * .7, y + h * .45, x - w, y); }
    else if (k < .8) { p.bezierCurveTo(x - w * .2, y - h * .5, x - w * .6, y - h * .5, x - w * .5, y); p.lineTo(x - w, y); }
    else { p.quadraticCurveTo(x - w * .4, y + h * .7, x - w * .8, y + h * .2); }
    if (r() < .35) p.moveTo(x - w * .5 + h * .15, y - h * .55), p.arc(x - w * .5, y - h * .55, h * .12, 0, TAU);
    if (r() < .25) p.moveTo(x - w * .4 + h * .15, y + h * .55), p.arc(x - w * .4, y + h * .55, h * .12, 0, TAU);
    x -= w + (r() < .3 ? h * .8 : h * .12);
  }
  inkStroke(ctx, p, o.w || Math.max(1.6, h * .16), { col: o.col, a: o.a });
}
