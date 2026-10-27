// Baskı üslubu ilkelleri: kâğıt, renk plakaları (multiply + kayık baskı), yarım ton (raster) karoları, kırık mürekkep kenarı
'use strict';
const P = {
  paper: '#EEE4CC', paperD: '#D8C9A8', paperDirty: '#E2D5B8',
  ink: '#1E1B18', fes: '#8C2A2A', mustard: '#D49A2A', khaki: '#7A7448',
  sea: '#3F6670', night: '#22283A', flag: '#E30A17',
};
function makeCanvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function hexRGB(c) { const n = parseInt(c.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
function rgba(c, a) { const [r, g, b] = hexRGB(c); return `rgba(${r},${g},${b},${a})`; }
function mixHex(a, b, t) { const A = hexRGB(a), B = hexRGB(b); return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, '0')).join(''); }

const TEX = {};
// Kâğıt: lif, diş ve hafif lekeler; çarpma ile basılır (beyaz = etkisiz)
function buildPaper() {
  const r = rng(11), c = makeCanvas(W, H), x = c.getContext('2d');
  const big = makeCanvas(W / 4, H / 4), bx = big.getContext('2d'), id = bx.createImageData(big.width, big.height);
  for (let y = 0; y < big.height; y++) for (let X = 0; X < big.width; X++) {
    let v = 0, a = .55, f = 1 / 70;
    for (let o = 0; o < 4; o++) { v += a * noise2(X * f, y * f, o + 21); a *= .5; f *= 2.1; }
    const k = (y * big.width + X) * 4, g = 246 + (v - .5) * 22;
    id.data[k] = g; id.data[k + 1] = g * .99; id.data[k + 2] = g * .975; id.data[k + 3] = 255;
  }
  bx.putImageData(id, 0, 0);
  x.imageSmoothingQuality = 'high'; x.drawImage(big, 0, 0, W, H);
  // lifler
  for (let i = 0; i < 1400; i++) {
    const px = r() * W, py = r() * H, L = 6 + r() * 26, a = r() * TAU;
    x.strokeStyle = `rgba(${r() < .5 ? '120,100,80' : '255,252,245'},${.05 + r() * .08})`; x.lineWidth = .6 + r() * .8;
    x.beginPath(); x.moveTo(px, py); x.quadraticCurveTo(px + Math.cos(a) * L * .5 + (r() - .5) * 6, py + Math.sin(a) * L * .5 + (r() - .5) * 6, px + Math.cos(a) * L, py + Math.sin(a) * L); x.stroke();
  }
  // diş (ince benek)
  const sp = x.getImageData(0, 0, W, H), d = sp.data;
  for (let i = 0; i < d.length; i += 4) { const n = (r() - .5) * 10; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
  x.putImageData(sp, 0, 0);
  TEX.paper = c;
  // mürekkep diş maskesi: kâğıt dişinin mürekkebi tutmadığı küçük boşluklar (destination-out)
  const m = makeCanvas(W, H), mx = m.getContext('2d'), mid = mx.createImageData(W, H);
  for (let y = 0; y < H; y++) for (let X = 0; X < W; X++) {
    const v = noise2(X / 3.1, y / 3.1, 77) * .6 + noise2(X / 11, y / 11, 78) * .4;
    mid.data[(y * W + X) * 4 + 3] = v > .74 ? 255 * clamp((v - .74) / .08) : 0;
  }
  mx.putImageData(mid, 0, 0);
  TEX.tooth = m;
  // gren
  TEX.grain = [];
  for (let g = 0; g < 6; g++) {
    const gc = makeCanvas(512, 512), gx = gc.getContext('2d'), im = gx.createImageData(512, 512);
    for (let i = 0; i < im.data.length; i += 4) { const v = 128 + (r() + r() + r() - 1.5) * 70; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
    gx.putImageData(im, 0, 0); TEX.grain.push(gc);
  }
  const vg = makeCanvas(W, H), vx = vg.getContext('2d');
  const gr = vx.createRadialGradient(W / 2, H * .48, H * .3, W / 2, H * .5, H * 1.05);
  gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(.65, 'rgba(30,20,10,.12)'); gr.addColorStop(1, 'rgba(20,12,6,.5)');
  vx.fillStyle = gr; vx.fillRect(0, 0, W, H); TEX.vig = vg;
}

// Yarım ton karosu: hücre boyu cell (≥10 px), yoğunluk dens (0..1 → nokta alanı), açı ang (derece). Önbellekli desen.
const HT = {};
function halftone(ctx, col, dens, cell = 12, ang = 45) {
  const key = col + '|' + dens.toFixed(2) + '|' + cell + '|' + ang;
  if (!HT[key]) {
    const c = makeCanvas(cell * RS, cell * RS), x = c.getContext('2d');
    x.scale(RS, RS);
    const rr = cell * Math.sqrt(clamp(dens) / PI);
    x.fillStyle = col;
    // kare ızgara: hücre merkezinde ve köşelerde (dama) nokta → kesintisiz karo
    for (const [px, py] of [[cell / 2, cell / 2], [0, 0], [cell, 0], [0, cell], [cell, cell]]) {
      const rad = (px === cell / 2) ? rr : rr * .0;
      if (rad > 0) { x.beginPath(); x.arc(px, py, rad, 0, TAU); x.fill(); }
    }
    const pat = ctx.createPattern(c, 'repeat');
    const m = new DOMMatrix(); m.rotateSelf(ang); m.scaleSelf(1 / RS, 1 / RS);
    pat.setTransform(m);
    HT[key] = pat;
  }
  return HT[key];
}
// Işıkla değişen raster: merkezden dışa nokta yarıçapı azalır (ör. lamba halesi). Çekim başına önbelleğe alınabilir.
function radialHalftone(g, cx, cy, r0, r1, col, d0, d1, cell = 14, ang = 15, clip = null) {
  g.save(); if (clip) g.clip(clip);
  g.fillStyle = col;
  const ca = Math.cos(ang * PI / 180), sa = Math.sin(ang * PI / 180), R = r1 + cell;
  for (let v = -R; v <= R; v += cell) for (let u = -R; u <= R; u += cell) {
    const x = cx + u * ca - v * sa, y = cy + u * sa + v * ca, d = Math.hypot(x - cx, y - cy);
    if (d > r1) continue;
    const dens = lerp(d0, d1, smooth(inv(r0, r1, d)));
    if (dens <= .01) continue;
    g.beginPath(); g.arc(x, y, cell * Math.sqrt(dens / PI), 0, TAU); g.fill();
  }
  g.restore();
}

// Plakalar: her renk ayrı katmana çizilir, sonra kâğıda multiply ile basılır; her plaka çekim boyunca sabit küçük kayma alır.
const PLATES = {};
function plateCtx(name) {
  if (!PLATES[name]) { const c = makeCanvas(DW, DH); PLATES[name] = { c, x: c.getContext('2d') }; }
  const p = PLATES[name]; p.x.setTransform(1, 0, 0, 1, 0, 0); p.x.clearRect(0, 0, DW, DH); baseT(p.x);
  p.x.globalAlpha = 1; p.x.globalCompositeOperation = 'source-over';
  return p.x;
}
// seed'li kayma (px); amt 0 → kayma yok (baskı geçişinin sonunda sıfıra oturur)
function regOffset(seed, amt = 1) { const r = rng(seed * 97 + 13); return [(r() - .5) * 5 * amt, (r() - .5) * 5 * amt]; }
function pressPlate(ctx, name, o = {}) {
  const p = PLATES[name]; if (!p) return;
  const [dx, dy] = o.off || [0, 0];
  if (o.tooth !== false) { // kırık baskı kenarı
    p.x.save(); p.x.setTransform(1, 0, 0, 1, 0, 0); p.x.globalCompositeOperation = 'destination-out';
    p.x.globalAlpha = o.tooth ?? .9; p.x.drawImage(TEX.tooth, (dx * 7) % 40 - 20, (dy * 7) % 40 - 20, DW, DH); p.x.restore();
  }
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalCompositeOperation = o.mode || 'multiply'; ctx.globalAlpha = o.alpha ?? 1;
  ctx.drawImage(p.c, dx * RS, dy * RS);
  ctx.restore();
}
function paperBG(ctx, col = P.paper) { ctx.fillStyle = col; ctx.fillRect(0, 0, W, H); }
function applyPaper(ctx, amt = 1) { ctx.save(); baseT(ctx); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = amt; ctx.drawImage(TEX.paper, 0, 0); ctx.restore(); }
function applyGrain(ctx, t, amt = .05) {
  const L = TEX.grain.length, i = ((Math.floor(t * 24) % L) + L) % L, r = rng(Math.floor(t * 24) + 1);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = amt;
  const ox = -r() * 512, oy = -r() * 512;
  for (let y = oy; y < DH; y += 512) for (let x = ox; x < DW; x += 512) ctx.drawImage(TEX.grain[i], x, y);
  ctx.restore();
}
function applyVignette(ctx, amt = 1) { ctx.save(); baseT(ctx); ctx.globalAlpha = amt; ctx.drawImage(TEX.vig, 0, 0); ctx.restore(); }
