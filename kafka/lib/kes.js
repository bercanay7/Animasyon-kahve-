// Ağaç baskı çekim sistemi (Kafka, Dönüşüm). Motor: LemoLab woodcut (MIT; lib/woodcut.bundle.js → WC).
// Her kare bir baskıdır: maske (siyah = oyulmamış blok, beyaz = bıçağın oyduğu yer) + tek renk levhası (kırmızı elma)
// → WebGL baskı (kâğıt, mürekkep, çapak, kayık levha). Kenar boşluğu kâğıttır ve hiç kıpırdamaz; alt boşluk altyazının yeri.
// Üslup yasası (cinecode styles/woodcut.md): iki değer (mürekkep, kâğıt) + en çok bir renk, yalnız oyulmuş beyazda; ışık oyulur;
// çizgi yönü biçimi izler; figür = siyah siluet + beyaz bıçak halesi + yalnız ışıklı kenarda kesikler. Geçiş: kesme (yeni baskı), saydamlık yok.
'use strict';
const KAGIT = '#E9E1CF', MUREKKEP = '#16130F', KIRMIZI = '#B3241C';
const BLOK = { x0: 58, y0: 40, x1: 1862, y1: 900 };            // basılı alan; y > 900 kâğıt (altyazı bandı)
let MASK, MX, PLATE, PX, PRN, KENAR = null;
const MEMO = new Map();
// her önbellek ilk kullanımda kendini kurar (işçiden bağımsız, belirlenimci: tohumlar sabit)
function memo(key, fn) { let v = MEMO.get(key); if (v === undefined) { v = fn(); MEMO.set(key, v); } return v; }

function initKes() {
  [MASK, MX] = WC.canvas(1920, 1080); [PLATE, PX] = WC.canvas(1920, 1080); PRN = WC.makePrinter(1920, 1080);
  // blok kenarı: el oyması, düzensiz (sabit tohum); dışı kâğıt
  const r = rng(77), pts = [], jit = (a) => (r() - .5) * a;
  const { x0, y0, x1, y1 } = BLOK;
  for (let x = x0; x < x1; x += 22) pts.push([x, y0 + jit(5)]);
  for (let y = y0; y < y1; y += 22) pts.push([x1 + jit(5), y]);
  for (let x = x1; x > x0; x -= 22) pts.push([x, y1 + jit(5)]);
  for (let y = y1; y > y0; y -= 22) pts.push([x0 + jit(5), y]);
  KENAR = new Path2D(); KENAR.rect(-50, -50, 2020, 1180); pts.forEach((p, i) => i ? KENAR.lineTo(p[0], p[1]) : KENAR.moveTo(p[0], p[1])); KENAR.closePath();
}

// kes(ctx, st, cam, fn, o): fn(k) dünya koordinatında maskeye (k.m) ve levhaya (k.c) çizer.
// cam: {cx, cy, z}; verilmezse varsayılan yavaş yaklaşma (donuk plan yok: hareket ilk karede başlar).
function kes(ctx, st, cam, fn, o = {}) {
  if (!cam) cam = { cx: o.fx ?? 960, cy: o.fy ?? 470, z: (o.z0 ?? 1) + (o.nefes ?? .045) * clamp(st.p ?? 0) };
  const c = camOf(cam);
  for (const g of [MX, PX]) g.setTransform(1, 0, 0, 1, 0, 0);
  MX.globalCompositeOperation = 'source-over'; MX.globalAlpha = 1;
  MX.fillStyle = '#000'; MX.fillRect(0, 0, 1920, 1080); PX.clearRect(0, 0, 1920, 1080);
  for (const g of [MX, PX]) g.setTransform(c.s, 0, 0, c.s, -c.x * c.s, -c.y * c.s);
  const k = { m: MX, c: PX, t: st.t, lt: st.lt, st, cam: c, s: c.s };
  fn(k);
  for (const g of [MX, PX]) { g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; }
  if (!o.tamKare) { MX.fillStyle = '#fff'; MX.fill(KENAR, 'evenodd'); PX.save(); PX.globalCompositeOperation = 'destination-out'; PX.fill(KENAR, 'evenodd'); PX.restore(); }
  // kesme = yeni baskı: ilk iki karede levha birkaç piksel kayık, sonra yerine oturur
  const f0 = st.lt < 2 / 30 ? 1 : 0;
  const img = PRN.render(MASK, PLATE, { seed: 7, inkSeed: (st.seed || 1) + (o.inkSeed || 0), plate: KIRMIZI, paper: KAGIT, ink: MUREKKEP,
    reg: f0 ? [7, -4] : [2.2, 1.4], edge: 1, sheen: .1 });
  ctx.save(); baseT(ctx); ctx.drawImage(img, 0, 0, W, H); ctx.restore();
}

// ── Maske ilkelleri (k.m üzerinde; dünya koordinatı) ──
const KS = {
  ak(g, path, rule = 'nonzero') { g.fillStyle = '#fff'; g.fill(path, rule); },             // oy: açık alan
  kara(g, path, rule = 'nonzero') { g.fillStyle = '#000'; g.fill(path, rule); },
  poly(pts) { const p = new Path2D(); pts.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); p.closePath(); return p; },
  rect(x, y, w, h) { const p = new Path2D(); p.rect(x, y, w, h); return p; },
  // bölgeyi açıyla taranmış kesiklerle oy (ton: 0 kara … 1 ak). Kesikler bir kez kurulur.
  tara(g, key, polys, o = {}, t = 1e9) {
    const S = memo('tara:' + key, () => WC.hatch(new WC.Region(polys, { res: o.res ?? 3 }), {
      dir: typeof o.dir === 'function' ? o.dir : WC.dirAngle(o.aci ?? 0), tone: o.ton || (() => o.v ?? .5), sp: o.sp ?? 10, wmax: o.wmax ?? 6,
      lo: o.lo ?? .05, hi: o.hi ?? .98, seg: o.seg || [60, 220], gap: o.gap || [3, 12], kind: o.kind || 'v', seed: o.seed ?? 3, jit: o.jit ?? .15, reveal: o.reveal }));
    WC.drawStrokes(g, S, { t, color: o.renk || '#fff' });
  },
  // biçimli oyma (WC.shape): siyah siluet + hale + biçimi izleyen kesikler
  sekil(g, key, polys, o = {}, t = 1e9) { const S = memo('sekil:' + key, () => WC.shape(polys, { seed: 5, ...o })); S.draw(g, t, o.drawOpts || {}); return S; },
  // yol boyunca el kesikleri (kontur, ip, çatlak)
  kenar(g, key, pts, o = {}, t = 1e9) { const S = memo('kenar:' + key, () => WC.cutAlong(pts, { w: 3, seed: 9, ...o })); WC.drawStrokes(g, S, { t, color: o.renk || '#fff' }); },
  isin(g, key, cx, cy, o = {}, t = 1e9) { const S = memo('isin:' + key, () => WC.rays(cx, cy, { seed: 4, ...o })); WC.drawStrokes(g, S, { t, color: o.renk || '#fff' }); },
  benek(g, key, pts, o = {}, t = 1e9) { const S = memo('benek:' + key, () => WC.flecks(pts, { seed: 11, ...o })); WC.drawStrokes(g, S, { t, color: o.renk || '#fff' }); },
  // yatay ışık şeridi (kapı aralığından düşen): oyulmuş ak üçgen + kenarında bıçak izleri
  // siyah siluet + bıçak halesi + ışık yönünde kenar ışığı (oyulmuş, kesikli). path: Path2D (nonzero). o: {hale, isik:[lx,ly], rim, kes}
  siluet(g, path, o = {}) {
    const hale = o.hale ?? 7, L = o.isik || [-1, -.3], ln = Math.hypot(L[0], L[1]) || 1, lx = L[0] / ln, ly = L[1] / ln, rim = o.rim ?? 6;
    if (hale > 0) { g.save(); g.strokeStyle = '#fff'; g.lineWidth = hale * 2; g.lineJoin = 'round'; g.stroke(path); g.restore(); }
    g.fillStyle = '#000'; g.fill(path);
    if (rim > 0) {
      g.save(); g.clip(path);
      g.fillStyle = '#fff'; g.fill(path);
      g.translate(-lx * rim, -ly * rim); g.fillStyle = '#000'; g.fill(path);
      g.restore();
      // kenar ışığını kesiklere böl: ışığa dik ince kara çizgiler (bıçak arası)
      if (o.kes !== false) { g.save(); g.clip(path); g.strokeStyle = '#000'; g.lineWidth = o.kesW ?? 2.2; const sp = o.kesSp ?? 9, ang = Math.atan2(ly, lx) + Math.PI / 2, bb = o.bb || [-3000, -3000, 6000, 6000];
        g.beginPath(); for (let d = -2600; d < 2600; d += sp) { const cx = Math.cos(ang), cy = Math.sin(ang), px = -cy * d, py = cx * d; g.moveTo(px - cx * 3000, py - cy * 3000); g.lineTo(px + cx * 3000, py + cy * 3000); } g.stroke(); g.restore(); }
    }
  },
};

// ── Ekran yazısı (oyulmuş başlık ve alıntı; altyazı bandına inmez) ──
const NOTEXT = typeof location !== 'undefined' && new URLSearchParams(location.search).has('notext');
const YF = { serif: (px, w = 600) => `${w} ${px}px "Cormorant Garamond"`, italik: (px, w = 500) => `italic ${w} ${px}px "Cormorant Garamond"`, kunye: (px) => `600 ${px}px "Cormorant Garamond"` };
// maskeye (blok içine) oyulmuş yazı: k.m'ye, ekran koordinatında. Görünme: harf harf oyulur (t0'dan itibaren)
function oyYazi(k, s, x, y, o = {}) {
  if (NOTEXT || !s) return;
  const g = k.m; g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
  g.font = o.font || YF.serif(o.px || 64); g.textAlign = o.align || 'center'; g.textBaseline = 'middle';
  if (o.ls) g.letterSpacing = o.ls + 'px';
  const lines = String(s).split('\n'), lh = (o.px || 64) * (o.lh || 1.18);
  const p = clamp(((k.lt) - (o.t0 || 0)) / (o.dur || .7));
  if (p <= 0) { g.restore(); return; }
  if (o.panel) { // kara panel (yazının altı oyulmamış blok kalsın): panel = oyulmamış, çevresi ince bıçak çerçeve
    const [px0, py0, pw, ph] = o.panel; g.fillStyle = '#000'; g.fillRect(px0, py0, pw, ph);
    g.strokeStyle = '#fff'; g.lineWidth = 3; g.strokeRect(px0 + 10, py0 + 10, pw - 20, ph - 20);
  }
  // soldan sağa oyulma (bıçak ilerler)
  let wd = 0; for (const l of lines) wd = Math.max(wd, g.measureText(l).width);
  const xl = (o.align === 'left' ? x : o.align === 'right' ? x - wd : x - wd / 2) - 10;
  g.beginPath(); g.rect(xl, 0, (wd + 20) * p, 1080); g.clip();
  g.fillStyle = o.renk || '#fff';
  lines.forEach((l, i) => g.fillText(l, x, y - (lines.length - 1) * lh / 2 + i * lh));
  g.restore();
}
// alt kâğıt bandına mürekkeple künye (baskıdan sonra, ekran üstüne)
function kunye(ctx, s, lt, o = {}) {
  if (NOTEXT || !s) return;
  const a = clamp((lt - (o.t0 || 0)) / .12) * (1 - clamp((lt - (o.t1 || 1e9)) / .15));
  if (a <= 0) return;
  ctx.save(); baseT(ctx); ctx.globalAlpha = a; ctx.font = YF.kunye(o.px || 34); ctx.letterSpacing = '4px'; ctx.textAlign = o.align || 'right'; ctx.textBaseline = 'middle';
  ctx.fillStyle = MUREKKEP; ctx.fillText(s, o.x ?? 1858, o.y ?? 932); ctx.restore();
}
