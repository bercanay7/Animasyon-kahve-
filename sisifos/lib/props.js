// Nesneler: kaya, tepe, kartal, sığır, gemi, tapınak, zincir, yıldırım...
'use strict';
// Kaya: düzensiz yuvarlak; açık taş rengi, siyah kazıma çatlaklar ve tarama gölgesi
function boulderShape(seed = 3, n = 14) {
  const r = rng(seed), pts = [];
  for (let i = 0; i < n; i++) {
    const a = i / n * TAU, rr = 1 + (r() - .5) * .16 + Math.sin(a * 3 + seed) * .04;
    pts.push([Math.cos(a) * rr, Math.sin(a) * rr * .94]);
  }
  return pts;
}
const BOULDER = boulderShape(5);
let BOULDER_TEX = null;
function boulderTex() {
  // vazo üslubu: eklenmiş beyaz astar (düz krem), kazıma çatlaklar, el çizimi kontur
  if (BOULDER_TEX) return BOULDER_TEX;
  const S = 700, R = 300, c = makeCanvas(S, S), x = c.getContext('2d'), r = rng(21);
  x.translate(S / 2, S / 2);
  const path = () => { x.beginPath(); spline(x, BOULDER.map(q => [q[0] * R, q[1] * R])); };
  path(); x.fillStyle = '#E4D3AE'; x.fill();
  x.save(); path(); x.clip();
  // çok hafif fırça dalgalanması (astarın düzensizliği)
  for (let i = 0; i < 26; i++) {
    const a = r() * TAU, d = Math.sqrt(r()) * R, px = Math.cos(a) * d, py = Math.sin(a) * d;
    x.fillStyle = r() < .5 ? 'rgba(150,110,70,.06)' : 'rgba(255,250,235,.10)';
    x.beginPath(); x.ellipse(px, py, 30 + r() * 70, 14 + r() * 30, r() * PI, 0, TAU); x.fill();
  }
  // küçük kazıma işaretleri (taş gözenekleri, kısa kavisler)
  x.strokeStyle = 'rgba(40,24,14,.55)'; x.lineCap = 'round';
  for (let i = 0; i < 16; i++) {
    const a = r() * TAU, d = Math.sqrt(r()) * R * .82, px = Math.cos(a) * d, py = Math.sin(a) * d, rr = 6 + r() * 10, a0 = r() * TAU;
    x.lineWidth = 3; x.beginPath(); x.arc(px, py, rr, a0, a0 + 1.6 + r()); x.stroke();
  }
  // çatlaklar: kenardan içe, sivrilen, az ve ince
  x.strokeStyle = C.ink; x.lineJoin = 'round';
  const crack = (px, py, a, w, n) => {
    for (let s2 = 0; s2 < n; s2++) {
      const L = 20 + r() * 26; a += (r() - .5) * .9;
      const nx = px + Math.cos(a) * L, ny = py + Math.sin(a) * L;
      x.lineWidth = w; x.beginPath(); x.moveTo(px, py); x.lineTo(nx, ny); x.stroke();
      if (r() < .25 && w > 2) crack(nx, ny, a + (r() < .5 ? 1 : -1) * (.6 + r() * .6), w * .6, 3);
      px = nx; py = ny; w *= .78;
    }
  };
  for (const a0 of [.5, 2.4, 4.4]) crack(Math.cos(a0) * R, Math.sin(a0) * R * .94, a0 + PI + (r() - .5) * .5, 5, 6);
  x.restore();
  path(); x.lineWidth = 8; x.strokeStyle = C.ink; x.stroke();
  BOULDER_TEX = { c, S, R };
  return BOULDER_TEX;
}
function boulder(ctx, x, y, R, ang, opt = {}) {
  const T = boulderTex(), k = R / T.R, light = opt.light ?? -2.3;
  ctx.save(); ctx.translate(x, y);
  if (opt.shadow !== false) {
    ctx.fillStyle = 'rgba(20,8,4,.32)';
    ctx.beginPath(); ctx.ellipse(R * .1, R * .93, R * 1.1, R * .13, 0, 0, TAU); ctx.fill();
  }
  ctx.save(); ctx.rotate(ang); ctx.drawImage(T.c, -T.S / 2 * k, -T.S / 2 * k, T.S * k, T.S * k);
  ctx.beginPath(); spline(ctx, BOULDER.map(q => [q[0] * R * .985, q[1] * R * .985])); ctx.rotate(-ang); ctx.clip();
  // sabit ışık: gölge tarafında forma uyan kavisli tarama (ışık kaynağına bakan merkezli yaylar)
  const lx = Math.cos(light), ly = Math.sin(light);
  const sg = ctx.createLinearGradient(lx * R, ly * R, -lx * R, -ly * R);
  sg.addColorStop(0, 'rgba(255,250,235,.16)'); sg.addColorStop(.5, 'rgba(120,80,50,0)'); sg.addColorStop(1, 'rgba(90,55,30,.36)');
  ctx.fillStyle = sg; ctx.fillRect(-R * 1.3, -R * 1.3, R * 2.6, R * 2.6);
  ctx.strokeStyle = 'rgba(23,16,12,.62)'; ctx.lineCap = 'round';
  const ox = lx * R * .55, oy = ly * R * .55;
  for (let i = 0; i < 9; i++) {
    const u = i / 8, rr = R * (1.05 + u * .55);
    ctx.lineWidth = Math.max(1, R * (.016 - u * .006));
    ctx.beginPath(); ctx.arc(ox, oy, rr, light + PI - .9 + u * .25, light + PI + .9 - u * .25); ctx.stroke();
  }
  ctx.restore();
  ctx.restore();
}
