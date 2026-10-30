// Dipinto: vazo ressamlarının fırçayla yazdığı Yunan ad yazıtları. Fontlarımızda Yunan harfleri yok;
// harfler tek kalınlıkta fırça çizgileriyle çizilir (arkaik/klasik vazo yazısı gibi, hafif düzensiz).
'use strict';
const _circ = (cx, cy, rx, ry, a0 = 0, a1 = TAU, n = 18) => Array.from({ length: n + 1 }, (_, i) => { const a = lerp(a0, a1, i / n); return [cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]; });
// her harf: [genişlik, [çizgiler]]; koordinatlar 0..1 yükseklik (üst 0)
const DIP = {
  'Α': [.8, [[[0, 1], [.4, 0], [.8, 1]], [[.18, .6], [.62, .6]]]],
  'Β': [.66, [[[0, 0], [0, 1]], [[0, 0], [.42, 0], [.58, .12], [.58, .34], [.42, .47], [0, .47]], [[.42, .47], [.64, .6], [.64, .86], [.46, 1], [0, 1]]]],
  'Γ': [.56, [[[0, 1], [0, 0], [.56, 0]]]],
  'Δ': [.8, [[[0, 1], [.4, 0], [.8, 1], [0, 1]]]],
  'Ε': [.56, [[[.56, 0], [0, 0], [0, 1], [.56, 1]], [[0, .5], [.42, .5]]]],
  'Ζ': [.62, [[[0, 0], [.62, 0], [0, 1], [.62, 1]]]],
  'Η': [.64, [[[0, 0], [0, 1]], [[.64, 0], [.64, 1]], [[0, .5], [.64, .5]]]],
  'Θ': [.78, [_circ(.39, .5, .39, .5), [[.39, .5], [.4, .5]]]],
  'Ι': [.14, [[[.07, 0], [.07, 1]]]],
  'Κ': [.64, [[[0, 0], [0, 1]], [[.62, 0], [0, .55], [.64, 1]]]],
  'Λ': [.78, [[[0, 1], [.39, 0], [.78, 1]]]],
  'Μ': [.86, [[[0, 1], [0, 0], [.43, .62], [.86, 0], [.86, 1]]]],
  'Ν': [.66, [[[0, 1], [0, 0], [.66, 1], [.66, 0]]]],
  'Ξ': [.62, [[[0, 0], [.62, 0]], [[.1, .5], [.52, .5]], [[0, 1], [.62, 1]]]],
  'Ο': [.78, [_circ(.39, .5, .39, .5)]],
  'Π': [.64, [[[0, 1], [0, 0], [.64, 0], [.64, 1]]]],
  'Ρ': [.62, [[[0, 1], [0, 0], [.44, 0], [.62, .13], [.62, .34], [.44, .47], [0, .47]]]],
  'Σ': [.64, [[[.64, 0], [0, 0], [.36, .5], [0, 1], [.64, 1]]]],
  'Τ': [.7, [[[0, 0], [.7, 0]], [[.35, 0], [.35, 1]]]],
  'Υ': [.72, [[[0, 0], [.36, .5], [.72, 0]], [[.36, .5], [.36, 1]]]],
  'Φ': [.78, [_circ(.39, .5, .39, .3), [[.39, 0], [.39, 1]]]],
  'Χ': [.7, [[[0, 0], [.7, 1]], [[.7, 0], [0, 1]]]],
  'Ψ': [.72, [[[0, .1], [0, .4], [.36, .56], [.72, .4], [.72, .1]], [[.36, 0], [.36, 1]]]],
  'Ω': [.82, [_circ(.41, .5, .34, .42, PI * .72, PI * 2.28, 20), [[0, 1], [.27, 1]], [[.55, 1], [.82, 1]]]],
  ' ': [.4, []],
  '·': [.3, [[[.15, .5], [.16, .5]]]],
};
// dipinto(ctx, 'ΠΡΟΜΗΘΕΥΣ', x, y, h, {col, a, align: 'center'|'left', vertical, p (yazılma oranı), w, seed})
function dipinto(ctx, s, x, y, h, o = {}) {
  const ls = o.ls ?? .22, glyphs = [...s].map(ch => DIP[ch] || DIP[' ']);
  const total = glyphs.reduce((a, g) => a + (g[0] + ls) * h, 0) - ls * h;
  const n = glyphs.length, p = o.p ?? 1;
  ctx.save(); ctx.translate(x, y); if (o.vertical) ctx.rotate(PI / 2);
  let cx = o.align === 'left' ? 0 : -total / 2;
  ctx.strokeStyle = o.col || C.red; ctx.lineWidth = h * (o.w ?? .1); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.globalAlpha *= o.a ?? 1;
  if (o.glow) { ctx.shadowColor = o.glow; ctx.shadowBlur = o.blur || 20; }
  const sd = o.seed || 3;
  glyphs.forEach(([gw, strokes], i) => {
    const q = clamp(p * n - i); if (q <= 0) { cx += (gw + ls) * h; return; }
    for (const st of strokes) {
      const m = Math.max(2, Math.ceil(st.length * q));
      ctx.beginPath();
      st.slice(0, m).forEach(([u, v], k) => { const px = cx + u * h + noise1(i * 7.3 + k * 1.7, sd) * h * .03, py = -h / 2 + v * h + noise1(i * 3.1 + k * 2.3, sd + 5) * h * .03; k ? ctx.lineTo(px, py) : ctx.moveTo(px, py); });
      ctx.stroke();
    }
    cx += (gw + ls) * h;
  });
  ctx.restore();
  return total;
}
