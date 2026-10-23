// Renk paleti, kil/kağıt dokusu, gren, vinyet ve vazo süsleri (meander, ışın, dil frizleri)
'use strict';
const C = {
  clay: '#C8693D', clayL: '#DB8655', clayD: '#A24E2B', clayDD: '#7E3920',
  ink: '#17100C', inkSoft: '#241812',
  red: '#8E2F1F', white: '#EFE4CC', bone: '#E2D3B5',
  gold: '#E7B85E', night: '#120C10', umber: '#2A1912',
  paper: '#ECE3D0', paperD: '#D9CCB1', sepia: '#3B2A1E',
};
// Sahne stilleri: siyah figür, kırmızı figür (yeraltı), beyaz zemin (modern)
const STY = {
  black: { fill: C.ink, cut: C.clay, red: C.red, white: C.white, line: C.ink },
  blackNight: { fill: C.ink, cut: '#B85E37', red: C.red, white: C.white, line: C.ink },
  red: { fill: '#C7683C', cut: C.ink, red: C.red, white: C.white, line: C.ink },
  white: { fill: C.inkSoft, cut: C.paper, red: '#9A3B25', white: '#FFF8EA', line: C.inkSoft },
};

function makeCanvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }

// Kil dokusu: büyük lekeler (fırınlama farkları) + ince benekler + fırça izleri. Çarpma (multiply) ile uygulanır.
let TEX = {};
function buildTextures() {
  const r = rng(7);
  // fırın lekeleri
  const big = makeCanvas(W / 4, H / 4), bx = big.getContext('2d');
  const id = bx.createImageData(big.width, big.height);
  for (let y = 0; y < big.height; y++) for (let x = 0; x < big.width; x++) {
    let v = 0, a = .55, f = 1 / 90;
    for (let o = 0; o < 4; o++) { v += a * noise2(x * f, y * f, o + 3); a *= .5; f *= 2.1; }
    const k = (y * big.width + x) * 4, g = 236 + (v - .5) * 46;
    id.data[k] = g; id.data[k + 1] = g * .985; id.data[k + 2] = g * .965; id.data[k + 3] = 255;
  }
  bx.putImageData(id, 0, 0);
  const clay = makeCanvas(W, H), cx = clay.getContext('2d');
  cx.imageSmoothingQuality = 'high';
  cx.drawImage(big, 0, 0, W, H);
  // yatay çark izleri (çömlekçi çarkı)
  for (let i = 0; i < 260; i++) {
    const y = r() * H, a = r() * .05;
    cx.strokeStyle = `rgba(${r() < .5 ? '255,250,240' : '120,90,70'},${a})`;
    cx.lineWidth = .6 + r() * 2.4;
    cx.beginPath(); cx.moveTo(-10, y);
    for (let x = 0; x <= W + 20; x += 60) cx.lineTo(x, y + Math.sin(x * .004 + i) * 3);
    cx.stroke();
  }
  // benekler
  const sp = cx.getImageData(0, 0, W, H), d = sp.data;
  for (let i = 0; i < d.length; i += 4) {
    const n = (r() - .5) * 14;
    d[i] = clamp(d[i] + n, 0, 255); d[i + 1] = clamp(d[i + 1] + n, 0, 255); d[i + 2] = clamp(d[i + 2] + n, 0, 255);
  }
  for (let i = 0; i < 2600; i++) {
    const x = (r() * W) | 0, y = (r() * H) | 0, k = (y * W + x) * 4, s = r() < .5 ? -50 : 25;
    for (let j = 0; j < 3; j++) d[k + j] = clamp(d[k + j] + s, 0, 255);
  }
  cx.putImageData(sp, 0, 0);
  TEX.clay = clay;
  // gren karoları
  TEX.grain = [];
  for (let g = 0; g < 6; g++) {
    const c = makeCanvas(512, 512), x = c.getContext('2d'), im = x.createImageData(512, 512);
    for (let i = 0; i < im.data.length; i += 4) {
      const v = 128 + (r() + r() + r() - 1.5) * 70;
      im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255;
    }
    x.putImageData(im, 0, 0);
    TEX.grain.push(c);
  }
  // vinyet
  const vg = makeCanvas(W, H), vx = vg.getContext('2d');
  const gr = vx.createRadialGradient(W / 2, H * .48, H * .25, W / 2, H * .5, H * 1.05);
  gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(.6, 'rgba(20,8,4,.18)'); gr.addColorStop(1, 'rgba(10,4,2,.7)');
  vx.fillStyle = gr; vx.fillRect(0, 0, W, H);
  TEX.vig = vg;
}

// Kil zemin: renk geçişi + doku
function clayBG(ctx, top = C.clayL, bot = C.clayD, glow = null) {
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, top); g.addColorStop(1, bot);
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  if (glow) {
    const rg = ctx.createRadialGradient(glow.x, glow.y, 0, glow.x, glow.y, glow.r);
    rg.addColorStop(0, glow.c); rg.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = rg; ctx.fillRect(0, 0, W, H);
  }
}
function applyTexture(ctx, amt = 1) {
  ctx.save(); baseT(ctx);
  ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = amt;
  ctx.drawImage(TEX.clay, 0, 0);
  ctx.restore();
}
function applyGrain(ctx, t, amt = .07) {
  const i = Math.floor(t * 24) % TEX.grain.length, r = rng(Math.floor(t * 24) + 1);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = amt;
  const ox = -r() * 512, oy = -r() * 512;
  for (let y = oy; y < DH; y += 512) for (let x = ox; x < DW; x += 512) ctx.drawImage(TEX.grain[i], x, y);
  ctx.restore();
}
function applyVignette(ctx, amt = 1) {
  ctx.save(); baseT(ctx);
  ctx.globalAlpha = amt; ctx.drawImage(TEX.vig, 0, 0); ctx.restore();
}

// Meander (Yunan anahtarı) şeridi: x0..x1 arası, üst kenarı y, yükseklik h
function meander(ctx, x0, x1, y, h, col, bg = null) {
  if (bg) { ctx.fillStyle = bg; ctx.fillRect(x0, y, x1 - x0, h); }
  const u = h / 5, cell = h; // her desen birimi kare
  ctx.fillStyle = col;
  ctx.fillRect(x0, y, x1 - x0, u * .55);
  ctx.fillRect(x0, y + h - u * .55, x1 - x0, u * .55);
  ctx.save(); ctx.beginPath(); ctx.rect(x0, y, x1 - x0, h); ctx.clip();
  const lw = u * .62;
  ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.lineCap = 'butt'; ctx.lineJoin = 'miter';
  const start = Math.floor(x0 / cell) * cell;
  for (let x = start; x < x1 + cell; x += cell) {
    const a = y + u * 1.15, b = y + h - u * 1.15;
    ctx.beginPath();
    ctx.moveTo(x, b);
    ctx.lineTo(x, a); ctx.lineTo(x + cell * .82, a); ctx.lineTo(x + cell * .82, b);
    ctx.lineTo(x + cell * .3, b); ctx.lineTo(x + cell * .3, a + u * 1.3); ctx.lineTo(x + cell * .55, a + u * 1.3);
    ctx.stroke();
  }
  ctx.restore();
}
// Dil (tongue) frizi
function tongues(ctx, x0, x1, y, h, col, alt = null) {
  const w = h * .62;
  ctx.save(); ctx.beginPath(); ctx.rect(x0, y, x1 - x0, h); ctx.clip();
  ctx.fillStyle = col; ctx.fillRect(x0, y, x1 - x0, h * .12);
  let i = 0;
  for (let x = Math.floor(x0 / w) * w; x < x1 + w; x += w, i++) {
    ctx.fillStyle = (alt && i % 2) ? alt : col;
    ctx.beginPath();
    ctx.moveTo(x + w * .08, y + h * .1);
    ctx.lineTo(x + w * .92, y + h * .1);
    ctx.quadraticCurveTo(x + w * .92, y + h * .95, x + w * .5, y + h * .95);
    ctx.quadraticCurveTo(x + w * .08, y + h * .95, x + w * .08, y + h * .1);
    ctx.fill();
  }
  ctx.restore();
}
// Işın frizi (vazo dibi)
function rays(ctx, x0, x1, y, h, col) {
  const w = h * .42;
  ctx.fillStyle = col; ctx.beginPath();
  for (let x = Math.floor(x0 / w) * w; x < x1 + w; x += w) {
    ctx.moveTo(x, y + h); ctx.lineTo(x + w / 2, y); ctx.lineTo(x + w, y + h);
  }
  ctx.fill();
}
// Nokta-çizgi bordür
function dotBand(ctx, x0, x1, y, r, gap, col) {
  ctx.fillStyle = col;
  for (let x = x0 + gap / 2; x < x1; x += gap) { ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); }
}
// Palmet-lotus frizi (sadeleştirilmiş)
function palmettes(ctx, x0, x1, y, h, col) {
  const w = h * 1.1;
  ctx.save(); ctx.fillStyle = col; ctx.strokeStyle = col; ctx.lineWidth = h * .05;
  let i = 0;
  for (let x = Math.floor(x0 / w) * w; x < x1 + w; x += w, i++) {
    const cx = x + w / 2, by = y + h * .92;
    if (i % 2 === 0) { // palmet: yelpaze yaprakları
      for (let k = -3; k <= 3; k++) {
        const a = k * .28, L = h * (.78 - Math.abs(k) * .06);
        ctx.beginPath(); ctx.ellipse(cx + Math.sin(a) * L * .5, by - Math.cos(a) * L * .5, h * .07, L * .5, a, 0, TAU); ctx.fill();
      }
    } else { // lotus
      ctx.beginPath(); ctx.moveTo(cx, by - h * .85);
      ctx.quadraticCurveTo(cx + h * .2, by - h * .3, cx, by);
      ctx.quadraticCurveTo(cx - h * .2, by - h * .3, cx, by - h * .85); ctx.fill();
      ctx.beginPath(); ctx.moveTo(cx - h * .32, by - h * .55); ctx.quadraticCurveTo(cx - h * .05, by - h * .2, cx, by); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(cx + h * .32, by - h * .55); ctx.quadraticCurveTo(cx + h * .05, by - h * .2, cx, by); ctx.stroke();
    }
    // bağlayıcı kıvrım
    ctx.beginPath(); ctx.moveTo(cx, by); ctx.quadraticCurveTo(cx + w * .5, by + h * .08, cx + w, by); ctx.stroke();
  }
  ctx.restore();
}
// Vazo kuşağı çerçevesi: sahnenin üstüne ve altına süs bantları
function friezeFrame(ctx, opt = {}) {
  const col = opt.col || C.ink, bg = opt.bg || null, th = opt.h || 54, a = opt.alpha ?? 1, off = opt.off || 0;
  if (a <= 0) return;
  ctx.save(); baseT(ctx); ctx.globalAlpha = a;
  ctx.translate(0, 0);
  ctx.save(); ctx.translate(-off % (th * 2), 0);
  meander(ctx, -th * 2, W + th * 2, -th * (opt.hideTop || 0), th, col, bg);
  ctx.restore();
  ctx.save(); ctx.translate(off % (th * 2), 0);
  tongues(ctx, -th * 2, W + th * 2, H - th * .9 + th * (opt.hideBot || 0), th * .9, col);
  ctx.restore();
  ctx.restore();
}
