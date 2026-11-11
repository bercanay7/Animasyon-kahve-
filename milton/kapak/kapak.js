// Kapak sahneleri (Milton: Kayıp Cennet). Yalnız kapak klasörü; ortak dosyalara dokunmaz, sahne işlevlerini çağırır.
// Sorgu: v=a|b (A: "BEN CEHENNEMİM", B: Cabanel'in gözü), renk=0 (siyah-beyaz) | 1 (tek vurgu: A alev, B damla) | 2 (B: iris),
//        font=cinzel|bebas|anton, yazi=0|1 (yazı adayı), notext (yazısız), t (alev evresi)
// Çizim sırası: gravür sahnesi motorla (levha) → vurgu rengi (baskının üstüne, yalnız odak bölgesinde, multiply) → kâğıt + vinyet → yazı.
'use strict';
const KQ = new URLSearchParams(location.search);
const KPK = { v: KQ.get('v') || 'a', renk: +(KQ.get('renk') || 0), font: KQ.get('font') || 'cinzel', yazi: +(KQ.get('yazi') || 0), t: +(KQ.get('t') || 3.2), a: KQ.has('a') ? +KQ.get('a') : 1.3, notext: KQ.has('notext') };
const KPK_PAPER = `rgb(${GR.PAPER})`, KPK_INK = `rgb(${GR.INK})`;
const KPK_YAZI = {
  a: [['BEN', 'CEHENNEMİM']],
  b: [['ŞEYTAN', 'AĞLADI'], ['TEK DAMLA', 'YAŞ']],
};
const KPK_FONT = {
  cinzel: px => `900 ${px}px Cinzel`, bebas: px => `400 ${px}px "Bebas Neue"`, anton: px => `400 ${px}px Anton`,
};

// ── yazı: satırlar; büyük harf yüksekliği hedefi (cap, px), en geniş satır maxW; x hizası ──
// o: {x, y (blok merkezi), cap, maxW, align, ls (harf aralığı, em), gap (satır arası, cap oranı), col, cols (satır renkleri)}
function kpk_yazi(ctx, lines, o) {
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  const F = KPK_FONT[KPK.font] || KPK_FONT.cinzel;
  const capOf = px => { ctx.font = F(px); return ctx.measureText('H').actualBoundingBoxAscent; };
  let px = 200; px = px * o.cap / capOf(px);
  const ls = o.ls ?? (KPK.font === 'cinzel' ? -.02 : 0);
  const wOf = (s, p) => { ctx.font = F(p); ctx.letterSpacing = (ls * p) + 'px'; return ctx.measureText(s).width - ls * p; };
  let wmax = Math.max(...lines.map(s => wOf(s, px)));
  if (wmax > o.maxW) { px *= o.maxW / wmax; wmax = o.maxW; }
  const cap = capOf(px), gap = (o.gap ?? .32) * cap, bh = lines.length * cap + (lines.length - 1) * gap;
  ctx.font = F(px); ctx.letterSpacing = (ls * px) + 'px'; ctx.textBaseline = 'alphabetic'; ctx.textAlign = 'left';
  const boxes = [];
  lines.forEach((s, i) => {
    const w = wOf(s, px), yb = o.y - bh / 2 + cap + i * (cap + gap);
    const x = o.align === 'right' ? o.x - w : o.align === 'center' ? o.x - w / 2 : o.x;
    ctx.font = F(px); ctx.letterSpacing = (ls * px) + 'px';
    if (o.shadow) { ctx.fillStyle = KPK_INK; for (const [dx, dy] of o.shadow) ctx.fillText(s, x + dx, yb + dy); }
    ctx.fillStyle = (o.cols && o.cols[i]) || o.col || KPK_PAPER; ctx.fillText(s, x, yb);
    const m = ctx.measureText(s);
    boxes.push([x - m.actualBoundingBoxLeft, yb - m.actualBoundingBoxAscent, x + w, yb + m.actualBoundingBoxDescent]);
  });
  ctx.restore();
  console.log(`yazi ${KPK.font} px=${px.toFixed(0)} cap=${cap.toFixed(0)} (%${(cap / H * 100).toFixed(1)}) w=${wmax.toFixed(0)} kutular=${JSON.stringify(boxes.map(b => b.map(Math.round)))}`);
  return { px, cap, boxes };
}

// ═════════ KAPAK A: güneşin önünde kanatlı kara siluet, göğsünde alev ═════════
// Kadraj: figür sağda, büyük (ayaklar kadrajın hemen altında); güneş başın ve göğsün arkasında; solda yazı için koyu bulut kütlesi.
const KPK_A = { K: { x: 1560, y: 1072, U: 900 }, sun: { x: 1560, y: 545, r: 272 }, dark: [1.02, 1.42] };   // dark: güneş yarıçapı biriminde karartma başlangıcı ve sonu
function kpk_aSahne(t) {
  const { K, sun } = KPK_A, { tx } = GR;
  nif_gok(sun, { beams: [], t: 0 });
  // sol: ışınlar kalınlaşarak karanlığa karışır (multiply); yazının zemini düz siyah
  tx.save(); tx.globalCompositeOperation = 'multiply';
  const g = tx.createRadialGradient(sun.x, sun.y, sun.r * KPK_A.dark[0], sun.x, sun.y, sun.r * KPK_A.dark[1]); g.addColorStop(0, GR.tone(1)); g.addColorStop(.55, GR.tone(.55)); g.addColorStop(1, GR.tone(.03));
  tx.fillStyle = g; tx.fillRect(-100, -100, W + 200, H + 200); tx.restore();
  nif_siralar({ hz: 1010 });
  nif_tepe({ x: K.x, y: K.y + 6, s: K.U / 640, seed: 3, lit: [0, -1] });
  return nif_kancaSiluet(t, KPK.a ?? 1, K);
}
// alev vurgusu: göğüsteki alevin bölgesi (pelerinle kesişen elips) multiply ile kor rengine boyanır; siyah çizgiler siyah kalır.
// renkle: maske (Path2D'ler, dünya = ekran ölçeğinde M dönüşümüyle) içinde, parlak (kâğıt) pikseller renk alır; mürekkep olduğu gibi kalır.
const KPK_MC = makeCanvas(DW, DH), KPK_mc = KPK_MC.getContext('2d', { willReadFrequently: true });
function kpk_renkle(ctx, M, maskFn, colFn, box) {
  const m = KPK_mc; m.setTransform(1, 0, 0, 1, 0, 0); m.clearRect(0, 0, DW, DH); m.setTransform(M); maskFn(m);
  const [x0, y0, x1, y1] = box.map(Math.round), w = x1 - x0, h = y1 - y0;
  const C = makeCanvas(w, h), cx = C.getContext('2d'); cx.translate(-x0, -y0); colFn(cx);
  const MD = m.getImageData(x0, y0, w, h).data, CD = cx.getImageData(0, 0, w, h).data, I = ctx.getImageData(x0, y0, w, h), D = I.data;
  for (let i = 0; i < D.length; i += 4) {
    const a = MD[i + 3] / 255; if (!a) continue;
    const L = (D[i] + D[i + 1] + D[i + 2]) / 3, k = a * clamp((L - 70) / 120);
    for (let j = 0; j < 3; j++) D[i + j] = lerp(D[i + j], D[i + j] * CD[i + j] / 255, k);
  }
  ctx.putImageData(I, x0, y0);
}
function kpk_aRenk(ctx, F) {
  const { K } = KPK_A, U = K.U, c = F.P(0, -.55);
  kpk_renkle(ctx, new DOMMatrix([RS, 0, 0, RS, 0, 0]), m => {
    m.fillStyle = '#fff'; m.fill(F.cloak);
    m.globalCompositeOperation = 'destination-out'; m.lineWidth = .03 * U; m.stroke(F.cloak); for (const w of F.wings) m.stroke(w.path);   // kenar ışıkları renk almaz
  }, cx => {
    const g = cx.createLinearGradient(0, c[1] + .04 * U, 0, c[1] - .27 * U);
    g.addColorStop(0, '#ffd56e'); g.addColorStop(.3, '#ff9a30'); g.addColorStop(.7, '#ec4a1c'); g.addColorStop(1, '#c42414');
    cx.fillStyle = g; cx.fillRect(0, 0, DW, DH);
  }, [c[0] - .2 * U, c[1] - .32 * U, c[0] + .2 * U, c[1] + .1 * U]);
}
async function kpk_a(ctx) {
  let F;
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => { F = kpk_aSahne(KPK.t); }, NIF_BG);
  if (KPK.renk) kpk_aRenk(ctx, F);
  applyPaper(ctx, .8); applyVignette(ctx, .45);
  if (!KPK.notext) kpk_yazi(ctx, KPK_YAZI.a[KPK.yazi] || KPK_YAZI.a[0], { x: 60, y: 520, cap: 200, maxW: 1150 - 60, align: 'left', gap: .3 });
}

// ═════════ KAPAK B: Cabanel'in gözü ve tek damla yaş ═════════
// Film sahnesi cab_yakin (damlasız) yakın kadrajda; ton katmanı damlanın çevresinden dışa karartılır (düşük anahtar ışık),
// sonra büyük tek damla ve göz kapağından inen ıslak iz çizilir. Damla karenin en parlak, en karşıt noktası olur.
const KPK_B = { cam: { cx: 1092, cy: 514, z: 1.6 }, D: [966, 600], r: 39 };
function kpk_damlaYol(d, r) {
  const T = new Path2D(); T.moveTo(d[0], d[1] - r * 2.1); T.bezierCurveTo(d[0] + r * .45, d[1] - r * 1.2, d[0] + r, d[1] - r * .45, d[0] + r, d[1]);
  T.arc(d[0], d[1], r, 0, PI); T.bezierCurveTo(d[0] - r, d[1] - r * .45, d[0] - r * .45, d[1] - r * 1.2, d[0], d[1] - r * 2.1); T.closePath(); return T;
}
function kpk_bSahne(t) {
  const { tx } = GR, G = CAB.goz, { D, r } = KPK_B;
  cab_yakin(t, { yas: 0 });
  // düşük anahtar: göz ve damla çevresi açık kalır, dış kenarlar kararır (multiply, dünya koordinatında)
  tx.save(); tx.globalCompositeOperation = 'multiply';
  const g = tx.createRadialGradient(G.x + 50, G.y + 50, 140, G.x + 50, G.y + 50, 560);
  g.addColorStop(0, GR.tone(1)); g.addColorStop(.35, GR.tone(.62)); g.addColorStop(.7, GR.tone(.22)); g.addColorStop(1, GR.tone(.04));
  tx.fillStyle = g; tx.fillRect(-400, -400, W + 800, H + 800);
  const g2 = tx.createLinearGradient(0, 640, 0, 760); g2.addColorStop(0, GR.tone(1)); g2.addColorStop(1, GR.tone(.4));   // kollar: orta ton kütle
  tx.fillStyle = g2; tx.fillRect(-400, 640, W + 800, H); tx.restore();
  // ıslak iz: alt kapaktan damlaya
  const D0 = [G.x + 70, G.y + 64], pts = [];
  for (let k = 0; k <= 12; k++) { const u = k / 12; pts.push([lerp(D0[0], D[0], u) + Math.sin(u * 3) * 6, lerp(D0[1], D[1] - r * 1.6, u)]); }
  oku_vurus(pts, 16, .02, .8); oku_vurus(pts, 7, 1, .7);
  const T = kpk_damlaYol(D, r);
  tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 10; tx.stroke(T); tx.restore();
  GR.fill(T, GR.tone(1), { th: 0, id: 0 });
  const cr = new Path2D(); cr.arc(D[0], D[1], r * .64, .3, PI * .72); tx.save(); tx.strokeStyle = GR.tone(.15); tx.lineWidth = r * .22; tx.lineCap = 'round'; tx.stroke(cr); tx.restore();
}
function kpk_w2s(p) { const c = camOf(KPK_B.cam); return [(p[0] - c.x) * c.s, (p[1] - c.y) * c.s]; }
function kpk_bRenk(ctx) {
  const c = camOf(KPK_B.cam), { D, r } = KPK_B, G = CAB.goz;
  const M = new DOMMatrix([c.s * RS, 0, 0, c.s * RS, -c.x * c.s * RS, -c.y * c.s * RS]);
  const ic = [G.x + 22, G.y + 8], s2 = p => M.transformPoint(new DOMPoint(p[0], p[1]));
  if (KPK.renk === 2) {   // yalnız iris
    const I = new Path2D(); I.arc(ic[0], ic[1], 74, 0, TAU);
    const a = s2([ic[0] - 80, ic[1] - 80]), b = s2([ic[0] + 80, ic[1] + 80]);
    kpk_renkle(ctx, M, m => { m.fillStyle = '#fff'; m.fill(I); }, cx => { cx.fillStyle = '#3d9be0'; cx.fillRect(a.x, a.y, b.x - a.x, b.y - a.y); }, [a.x, a.y, b.x, b.y]);
  } else {               // yalnız damla
    const T = kpk_damlaYol(D, r);
    const a = s2([D[0] - r * 1.2, D[1] - r * 2.3]), b = s2([D[0] + r * 1.2, D[1] + r * 1.2]);
    kpk_renkle(ctx, M, m => { m.fillStyle = '#fff'; m.fill(T); }, cx => {
      const g = cx.createLinearGradient(a.x, a.y, b.x, b.y); g.addColorStop(0, '#e6f6ff'); g.addColorStop(.55, '#7cc8f7'); g.addColorStop(1, '#2f86d0');
      cx.fillStyle = g; cx.fillRect(a.x, a.y, b.x - a.x, b.y - a.y); }, [a.x, a.y, b.x, b.y]);
  }
}
async function kpk_b(ctx) {
  levha(ctx, KPK_B.cam, () => kpk_bSahne(KPK.t), [.03, 0, 1]);
  if (KPK.renk) kpk_bRenk(ctx);
  applyPaper(ctx, .8); applyVignette(ctx, .45);
  if (!KPK.notext) kpk_yazi(ctx, KPK_YAZI.b[KPK.yazi] || KPK_YAZI.b[0], { x: 1850, y: 370, cap: 200, maxW: 1850 - 1190, align: 'right', gap: .4 });
}

window.kapakCiz = async () => {
  for (const f of ['400 80px "Bebas Neue"', '400 80px Anton', '900 80px Cinzel']) await document.fonts.load(f, 'BENCHİMŞYTAĞLDIKMÇÖÜ');
  const cv = document.getElementById('c'), ctx = cv.getContext('2d');
  baseT(ctx); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
  if (KPK.v === 'b') await kpk_b(ctx); else await kpk_a(ctx);
  return true;
};
