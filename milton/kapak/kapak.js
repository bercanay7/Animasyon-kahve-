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
  b: [['PİŞMAN', 'MIYDI?'], ['GURUR', 'MU?'], ['ŞEYTAN', 'AĞLADI'], ['TEK DAMLA', 'YAŞ']],
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
const KPK_A = { K: { x: 1560, y: 1072, U: 900 }, sun: { x: 1590, y: 545, r: 300 }, dark: [1.02, 1.36] };   // dark: güneş yarıçapı biriminde karartma başlangıcı ve sonu
const KPK_SUN = { alcak: { sun: { x: 1560, y: 760, r: 370 }, dark: [1.02, 1.3] }, genis: { sun: { x: 1590, y: 545, r: 300 }, dark: [1.02, 1.36] } };
function kpk_aSahne(t) {
  if (KQ.get('sun') && KPK_SUN[KQ.get('sun')]) Object.assign(KPK_A, KPK_SUN[KQ.get('sun')]);
  const { K, sun } = KPK_A, { tx } = GR;
  if (!KQ.has('koyu')) return kpk_aAcik(t);
  nif_gok(sun, { beams: [], t: 0 });
  // sol: ışınlar kalınlaşarak karanlığa karışır (multiply); yazının zemini düz siyah
  tx.save(); tx.globalCompositeOperation = 'multiply';
  const g = tx.createRadialGradient(sun.x, sun.y, sun.r * KPK_A.dark[0], sun.x, sun.y, sun.r * KPK_A.dark[1]); g.addColorStop(0, GR.tone(1)); g.addColorStop(.55, GR.tone(.55)); g.addColorStop(1, GR.tone(.03));
  tx.fillStyle = g; tx.fillRect(-100, -100, W + 200, H + 200); tx.restore();
  nif_siralar({ hz: 1010 });
  nif_tepe({ x: K.x, y: K.y + 6, s: K.U / 640, seed: 3, lit: [0, -1] });
  return nif_kancaSiluet(t, KPK.a ?? 1, K);
}
// açık A (yönetmen notu, tur 5): filmdeki A01 değerleri. Kâğıt gök, seyrek ışınlar, büyük temiz güneş; önünde düz siyah figür;
// yazının arkasında ışınlar seyrelir (ton 1'e 'lighten': temiz kâğıt); köşelerde koyu bulut kütleleri kareyi açık akışta da çerçeveler.
const KPK_AA = { K: { x: 1505, y: 1078, U: 880 }, sun: { x: 1505, y: 500, r: 390 }, yazi: { x: 60, y: 560, w: 1110 } };
function kpk_aAcik(t) {
  const { K, sun } = KPK_AA, { tx } = GR;
  KPK_A.K = K;
  const bulut = KQ.get('bulut') === '0' ? [] : [{ x: -160, y: -60, w: 760, h: 300, seed: 12, n: 3 }, { x: 2080, y: -40, w: 900, h: 340, seed: 19, n: 4 }];
  nif_gok(sun, { beams: [], t: 0 });
  // yazı bölgesi: ışınlar seyrelir (yumuşak kenarlı temiz kâğıt)
  tx.save(); tx.globalCompositeOperation = 'lighten';
  const Y = KPK_AA.yazi; tx.translate(Y.x + Y.w * .45, Y.y); tx.scale(1, .5);
  const g = tx.createRadialGradient(0, 0, Y.w * .62, 0, 0, Y.w * 1.0); g.addColorStop(0, GR.tone(1)); g.addColorStop(1, GR.tone(.6));
  tx.fillStyle = g; tx.beginPath(); tx.arc(0, 0, Y.w * 1.0, 0, TAU); tx.fill(); tx.restore();
  for (const c of bulut) PR.cloud({ x: c.x, y: c.y, w: c.w, h: c.h, seed: c.seed, lit: nif_isik(sun, c.x, c.y), base: .03, hi: .85, core: .02, n: c.n });
  nif_siralar({ hz: 1040 });
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
// ═════════ A, tur 6 (kurul P-TO): alev tek ve en parlak odak; zemin %10 sıcak gri; çerçeve; bulut yok; isteğe bağlı eğik baş ═════════
const KPK_A6 = { K: { x: 1530, y: 1078, U: 880 }, sun: { x: 1530, y: 500, r: 390 }, yazi: { x: 60, y: 560, w: 1150 } };
// siluet (nif_kancaSiluet'in kapak eşi): kanat + pelerin yolu motordan; baş isteğe bağlı eğik (tilt, radyan); alev ayrı çizilir
function kpk_siluet(t, K, tilt = 0) {
  const F = nif_kancaYol(0, K), { P } = F, U = K.U, ks = U / 640;
  const pv = P(0, -.79), h0 = P(.004, -.855), rot = (q) => { const dx = q[0] - pv[0], dy = q[1] - pv[1], c = Math.cos(tilt), sn = Math.sin(tilt); return [pv[0] + dx * c - dy * sn, pv[1] + dx * sn + dy * c + Math.abs(tilt) * .1 * U * .12]; };
  const hc = rot(h0), HE = new Path2D(); HE.ellipse(hc[0], hc[1], .043 * U, .055 * U, -.08 + tilt, 0, TAU);
  const Hd = new Path2D(); Hd.moveTo(hc[0] + .043 * U, hc[1]); Hd.ellipse(hc[0], hc[1], .043 * U, .055 * U, -.08 + tilt, 0, TAU, true);
  { const q = [P(-.024, -.83), P(-.024, -.775), P(.024, -.775), P(.024, -.83)].map(rot); Hd.moveTo(...q[0]); for (const v of q.slice(1)) Hd.lineTo(...v); Hd.closePath(); }
  const all = new Path2D(); for (const w of F.wings) all.addPath(w.path); all.addPath(F.cloak); all.addPath(Hd);
  GR.fill(all, GR.tone(.02), { th: 0, id: 0 });
  { const ow = Math.max(3, 6 * ks), O = GR.ox; O.save(); O.clip(all); O.strokeStyle = GR.paperCol; O.lineWidth = ow; for (const w of F.wings) O.stroke(w.path); O.stroke(HE);
    O.restore(); O.save(); O.clip(F.cloak); O.lineWidth = ow; O.strokeStyle = GR.paperCol; O.stroke(F.cloak); O.restore(); }
  nif_kanatVurus(F, 1, 6, ks);
  // alev: eskisinden ~%35 büyük alan (genişlik 1,35×, boy 1,12×), tabanı biraz aşağıda; omuz çizgisinin altında kalır
  const b = P(0, -.45), L = .335 * U, wd = .064 * U;
  GR.tx.save(); GR.tx.clip(F.cloak); nif_gogusAlev(b[0], b[1], L, wd, t); GR.tx.restore();
  return Object.assign(F, { all, base: b, L, wd });
}
function kpk_a6Sahne(t) {
  const { K, sun } = KPK_A6, { tx } = GR;
  nif_gok(sun, { beams: [], t: 0 });
  tx.save(); tx.globalCompositeOperation = 'lighten';
  const Y = KPK_A6.yazi; tx.translate(Y.x + Y.w * .45, Y.y); tx.scale(1, .5);
  const g = tx.createRadialGradient(0, 0, Y.w * .62, 0, 0, Y.w * 1.0); g.addColorStop(0, GR.tone(1)); g.addColorStop(1, GR.tone(.6));
  tx.fillStyle = g; tx.beginPath(); tx.arc(0, 0, Y.w * 1.0, 0, TAU); tx.fill(); tx.restore();
  nif_siralar({ hz: 1040 });
  nif_tepe({ x: K.x, y: K.y + 6, s: K.U / 640, seed: 3, lit: [0, -1] });
  return kpk_siluet(t, K, KQ.has('bas') ? +KQ.get('bas') || .19 : 0);
}
// alevin rengi: kâğıt pikseller gradyan rengine (parlatarak: L/185 ile; çekirdek ≥ 230), mürekkep kalır
function kpk_alevRenk(ctx, F) {
  const U = KPK_A6.K.U, b = F.base, L = F.L;
  const box = [b[0] - .2 * U, b[1] - L - .03 * U, b[0] + .2 * U, b[1] + .06 * U].map(Math.round), [x0, y0, x1, y1] = box, w = x1 - x0, h = y1 - y0;
  const m = KPK_mc; m.setTransform(1, 0, 0, 1, 0, 0); m.clearRect(0, 0, DW, DH); m.setTransform(RS, 0, 0, RS, 0, 0);
  m.fillStyle = '#fff'; m.fill(F.cloak); m.globalCompositeOperation = 'destination-out'; m.lineWidth = .03 * U; m.stroke(F.cloak); for (const wg of F.wings) m.stroke(wg.path); m.globalCompositeOperation = 'source-over';
  const C = makeCanvas(w, h), cx = C.getContext('2d'); cx.translate(-x0, -y0);
  const g = cx.createLinearGradient(0, b[1] + .03 * U, 0, b[1] - L);
  g.addColorStop(0, '#fffbe8'); g.addColorStop(.28, '#ffe08a'); g.addColorStop(.5, '#ffa63a'); g.addColorStop(.78, '#ee5420'); g.addColorStop(1, '#c42a14');
  cx.fillStyle = g; cx.fillRect(x0, y0, w, h);
  const MD = m.getImageData(x0, y0, w, h).data, CD = cx.getImageData(0, 0, w, h).data, I = ctx.getImageData(x0, y0, w, h), D = I.data;
  for (let i = 0; i < D.length; i += 4) {
    const a = MD[i + 3] / 255; if (!a) continue;
    const Lp = (D[i] + D[i + 1] + D[i + 2]) / 3, k = a * clamp((Lp - 70) / 100), f = clamp(Lp / 175, 0, 1.0);
    for (let j = 0; j < 3; j++) D[i + j] = lerp(D[i + j], CD[i + j] * f, k);
  }
  ctx.putImageData(I, x0, y0);
}
// kor halesi: pelerinin karası üstünde yumuşak turuncu ışıma (screen); figürün dışına ve kenar ışığına taşmaz
function kpk_korHale(ctx, F) {
  const U = KPK_A6.K.U, b = F.base, c = [b[0], b[1] - F.L * .3];
  const G = makeCanvas(DW, DH), g = G.getContext('2d'); g.setTransform(RS, 0, 0, RS, 0, 0);
  g.save(); g.translate(c[0], c[1]); g.scale(1, 1.25);
  const r = .15 * U, q = g.createRadialGradient(0, 0, r * .2, 0, 0, r); q.addColorStop(0, 'rgba(255,120,30,.6)'); q.addColorStop(.4, 'rgba(235,85,20,.22)'); q.addColorStop(1, 'rgba(200,50,10,0)');
  g.fillStyle = q; g.beginPath(); g.arc(0, 0, r, 0, TAU); g.fill(); g.restore();
  g.globalCompositeOperation = 'destination-in'; g.fillStyle = '#fff'; g.fill(F.cloak);
  g.globalCompositeOperation = 'destination-out'; g.lineWidth = .045 * U; g.stroke(F.cloak); for (const wg of F.wings) g.stroke(wg.path);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'screen'; ctx.drawImage(G, 0, 0); ctx.restore();
}
async function kpk_a6(ctx) {
  let F;
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => { F = kpk_a6Sahne(KPK.t); }, NIF_BG);
  // zemin ve güneş ~%10 koyu, sıcak gri (alev bundan sonra boyanır: en parlak yer alev kalır)
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = KQ.get('kis') === '0' ? '#fff' : '#e6ded0'; ctx.fillRect(0, 0, DW, DH); ctx.restore();
  applyPaper(ctx, .8); applyVignette(ctx, .45);
  if (KPK.renk) { kpk_korHale(ctx, F); kpk_alevRenk(ctx, F); }
  if (!KQ.has('cercevesiz')) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.strokeStyle = KPK_INK; ctx.lineWidth = 2 * 7 * 1.5 * RS; ctx.strokeRect(0, 0, DW, DH); ctx.restore(); }
  if (KPK.notext) return;
  const Y = KPK_A6.yazi;
  kpk_yazi(ctx, KPK_YAZI.a[0], { x: Y.x, y: Y.y, cap: 210, maxW: Y.w, align: 'left', gap: .3, col: KPK_INK });
}
async function kpk_a(ctx) {
  if (!KQ.has('koyu') && !KQ.has('tur5')) return kpk_a6(ctx);
  let F;
  levha(ctx, { cx: 960, cy: 540, z: 1 }, () => { F = kpk_aSahne(KPK.t); }, NIF_BG);
  if (KPK.renk) kpk_aRenk(ctx, F);
  applyPaper(ctx, .8); applyVignette(ctx, .45);
  if (KQ.has('cerceve')) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.strokeStyle = KPK_INK; ctx.lineWidth = 2 * 7 * 1.5; ctx.strokeRect(0, 0, DW, DH); ctx.restore(); }
  if (KPK.notext) return;
  if (KQ.has('koyu')) { kpk_yazi(ctx, KPK_YAZI.a[KPK.yazi] || KPK_YAZI.a[0], { x: 60, y: 520, cap: 200, maxW: 1150 - 60, align: 'left', gap: .3 }); return; }
  const Y = KPK_AA.yazi, yr = KQ.get('yrenk') === '1';
  kpk_yazi(ctx, KPK_YAZI.a[KPK.yazi] || KPK_YAZI.a[0], { x: Y.x, y: Y.y, cap: 200, maxW: Y.w, align: 'left', gap: .3, col: KPK_INK, cols: [KPK_INK, yr ? '#d8461b' : KPK_INK] });
}

// ═════════ KAPAK B: Cabanel'in gözü ve tek damla yaş ═════════
// Film sahnesi cab_yakin (damlasız) yakın kadrajda; ton katmanı damlanın çevresinden dışa karartılır (düşük anahtar ışık),
// sonra büyük tek damla ve göz kapağından inen ıslak iz çizilir. Damla karenin en parlak, en karşıt noktası olur.
const KPK_B = { cam: { cx: 1092, cy: 514, z: 1.6 }, D: [974, 662], r: 25 };
// gözyaşı: ince, uzun, hafif asimetrik (uç sola-yukarı yatık, karın sağda biraz dolgun); boy ~3,6 r
function kpk_damlaYol(d, r) {
  const [x, y] = d, T = new Path2D(), top = [x - r * .28, y - r * 3.0];
  T.moveTo(...top);
  T.bezierCurveTo(x - r * .05, y - r * 1.9, x + r * 1.02, y - r * .95, x + r * .96, y + r * .05);
  T.bezierCurveTo(x + r * .9, y + r * .82, x + r * .3, y + r * 1.02, x - r * .12, y + r * .98);
  T.bezierCurveTo(x - r * .72, y + r * .92, x - r * .98, y + r * .4, x - r * .88, y - r * .25);
  T.bezierCurveTo(x - r * .78, y - r * 1.0, x - r * .42, y - r * 1.9, top[0], top[1]);
  T.closePath(); return T;
}
function kpk_damlaIz(G, D, r) { const D0 = [G.x + 64, G.y + 62], pts = []; for (let k = 0; k <= 14; k++) { const u = k / 14; pts.push([lerp(D0[0], D[0] - r * .28, u) + Math.sin(u * 3.1) * 7, lerp(D0[1], D[1] - r * 2.6, u)]); } return pts; }
function kpk_bSahne(t) {
  const { tx } = GR, G = CAB.goz, { D, r } = KPK_B;
  cab_yakin(t, { yas: 0 });
  // düşük anahtar: göz ve damla çevresi açık kalır, dış kenarlar kararır (multiply, dünya koordinatında)
  tx.save(); tx.globalCompositeOperation = 'multiply';
  const g = tx.createRadialGradient(G.x + 50, G.y + 50, 140, G.x + 50, G.y + 50, 560);
  g.addColorStop(0, GR.tone(1)); g.addColorStop(.35, GR.tone(.62)); g.addColorStop(.7, GR.tone(.22)); g.addColorStop(1, GR.tone(.04));
  tx.fillStyle = g; tx.fillRect(-400, -400, W + 800, H + 800);
  const g2 = tx.createLinearGradient(0, 640, 0, 760); g2.addColorStop(0, GR.tone(1)); g2.addColorStop(1, GR.tone(.4));   // kollar: orta ton kütle
  tx.fillStyle = g2; tx.fillRect(-400, 640, W + 800, H);
  const g3 = tx.createLinearGradient(1100, 0, 1190, 0); g3.addColorStop(0, GR.tone(1)); g3.addColorStop(1, GR.tone(.03));   // sağ: yazının zemini düz siyah
  tx.fillStyle = g3; tx.fillRect(1100, -400, W, H + 800);
  const g4 = tx.createLinearGradient(520, 0, 660, 0); g4.addColorStop(0, GR.tone(.03)); g4.addColorStop(1, GR.tone(1));   // sol kenar: nefes payı (yüz karanlıktan çıkar)
  tx.fillStyle = g4; tx.fillRect(-400, -400, 1060, H + 800); tx.restore();
  // ıslak iz: alt kapaktan damlaya (koyu gölge + parlak çizgi)
  const pts = kpk_damlaIz(G, D, r);
  oku_vurus(pts, 13, .02, .9); oku_vurus(pts, 7.5, 1, .8);
  const T = kpk_damlaYol(D, r);
  tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 3.2; tx.stroke(T); tx.restore();   // ince kontur (1280'de ~3 px)
  GR.fill(T, GR.tone(1), { th: 0, id: 0 });
  // gölge yanı: sol altta ince hilal; tek küçük parlama noktası sağ üstte
  tx.save(); tx.clip(T); tx.strokeStyle = GR.tone(.03); tx.lineWidth = r * .13; tx.lineCap = 'round';
  tx.beginPath(); tx.arc(D[0] - r * .02, D[1] + r * .02, r * .86, PI * .62, PI * 1.12); tx.stroke(); tx.restore();
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
    const pts = kpk_damlaIz(G, D, r), a0 = s2([G.x + 40, G.y + 40]);
    kpk_renkle(ctx, M, m => { m.fillStyle = '#fff'; m.fill(T); m.strokeStyle = '#fff'; m.lineWidth = 9; m.lineCap = 'round'; m.beginPath(); poly(m, pts, false); m.stroke(); }, cx => {
      const g = cx.createLinearGradient(a.x, a.y, b.x, b.y); g.addColorStop(0, '#eefaff'); g.addColorStop(.5, '#9fdcff'); g.addColorStop(1, '#4aa6e6');
      cx.fillStyle = '#bfe8ff'; cx.fillRect(a0.x, a0.y, b.x - a0.x, b.y - a0.y); cx.fillStyle = g; cx.fillRect(a.x, a.y, b.x - a.x, b.y - a.y); }, [Math.min(a.x, a0.x), Math.min(a.y, a0.y), b.x, b.y]);
  }
}
// ═════════ B, tur 6: daha sıkı göz kadrajı (1280'de göz ~560 px), saç kenarı ve kollar düz koyu kütle, kontrast eğrisiyle az tarama,
// damla 1,5×, içinde ≥ 240 parlama; yazı kısık kâğıt (#CFC7B8) ═════════
const KPK_B6 = { cam: { cx: 1080, cy: 520, z: 2.2 }, D: [972, 700], r: 37 };
function kpk_b6Sahne(t) {
  const { tx } = GR, G = CAB.goz, { D, r } = KPK_B6;
  cab_yakin(t, { yas: 0 });
  tx.save(); tx.globalCompositeOperation = 'multiply';
  // eliptik ışık: göz ve kaş aydınlık, çevresi yumuşakça düz karaya (kare levha kenarı yok)
  tx.save(); tx.translate(G.x - 20, G.y - 10); tx.scale(1, .52);
  const g = tx.createRadialGradient(0, 0, 230, 0, 0, 430); g.addColorStop(0, GR.tone(1)); g.addColorStop(.45, GR.tone(.75)); g.addColorStop(1, GR.tone(.02));
  tx.fillStyle = g; tx.fillRect(-3000, -3000, 6000, 6000); tx.restore();
  { const q = tx.createLinearGradient(1070, 0, 1125, 0); q.addColorStop(0, GR.tone(1)); q.addColorStop(1, GR.tone(.02)); tx.fillStyle = q; tx.fillRect(1070, -400, W, H + 800); }   // sağ: yazının zemini
  tx.restore();
  // kontrast eğrisi: ara tonlar azalır (üç değer: düz siyah, temiz kâğıt, dar geçişte tarama) → 168 px'te "bozuk ekran" çizgileri azalır
  { tx.save(); tx.setTransform(1, 0, 0, 1, 0, 0); const I = tx.getImageData(0, 0, DW, DH), A = I.data, LUT = new Uint8Array(256);
    for (let i = 0; i < 256; i++) { const v = i / 255, u = clamp((v - .32) / (.74 - .32)); LUT[i] = Math.round(255 * u * u * (3 - 2 * u)); }
    for (let i = 0; i < A.length; i += 4) { const v = LUT[A[i]]; A[i] = A[i + 1] = A[i + 2] = v; }
    tx.putImageData(I, 0, 0); tx.restore(); }
  // ıslak iz + damla
  const D0 = [G.x + 64, G.y + 62], pts = []; for (let k = 0; k <= 16; k++) { const u = k / 16; pts.push([lerp(D0[0], D[0] - r * .28, u) + Math.sin(u * 3.1) * 7, lerp(D0[1], D[1] - r * 2.6, u)]); }
  KPK_B6.iz = pts;
  oku_vurus(pts, 13, .02, .9); oku_vurus(pts, 7, 1, .8);
  const T = kpk_damlaYol(D, r);
  tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 2.6; tx.stroke(T); tx.restore();
  GR.fill(T, GR.tone(1), { th: 0, id: 0 });
  tx.save(); tx.clip(T); tx.strokeStyle = GR.tone(.03); tx.lineWidth = r * .12; tx.lineCap = 'round'; tx.beginPath(); tx.arc(D[0] - r * .02, D[1] + r * .02, r * .86, PI * .62, PI * 1.12); tx.stroke(); tx.restore();
}
function kpk_b6M() { const c = camOf(KPK_B6.cam); return new DOMMatrix([c.s * RS, 0, 0, c.s * RS, -c.x * c.s * RS, -c.y * c.s * RS]); }
async function kpk_b6(ctx) {
  levha(ctx, KPK_B6.cam, () => kpk_b6Sahne(KPK.t), [.03, 0, 1]);
  applyPaper(ctx, .8); applyVignette(ctx, .45);
  const M = kpk_b6M(), { D, r } = KPK_B6, s2 = p => M.transformPoint(new DOMPoint(p[0], p[1]));
  if (KPK.renk) {
    const T = kpk_damlaYol(D, r), a = s2([D[0] - r * 1.2, D[1] - r * 3.2]), b = s2([D[0] + r * 1.2, D[1] + r * 1.2]), pts = KPK_B6.iz, a0 = s2(pts[0]);
    const m = KPK_mc; m.setTransform(1, 0, 0, 1, 0, 0); m.clearRect(0, 0, DW, DH); m.setTransform(M); m.fillStyle = '#fff'; m.fill(T); m.strokeStyle = '#fff'; m.lineWidth = 8; m.lineCap = 'round'; m.beginPath(); poly(m, pts, false); m.stroke();
    const x0 = Math.round(Math.min(a.x, a0.x - 30)), y0 = Math.round(Math.min(a.y, a0.y - 10)), x1 = Math.round(b.x), y1 = Math.round(b.y), w = x1 - x0, h = y1 - y0;
    const C = makeCanvas(w, h), cx = C.getContext('2d'); cx.translate(-x0, -y0);
    const g = cx.createLinearGradient(a.x, a.y, b.x, b.y); g.addColorStop(0, '#e2f5ff'); g.addColorStop(.55, '#a8defc'); g.addColorStop(1, '#5fb4ea');
    cx.fillStyle = '#c4ebff'; cx.fillRect(x0, y0, w, h); cx.fillStyle = g; cx.fillRect(a.x, a.y, b.x - a.x, b.y - a.y);
    const MD = m.getImageData(x0, y0, w, h).data, CD = cx.getImageData(0, 0, w, h).data, I = ctx.getImageData(x0, y0, w, h), Dd = I.data;
    for (let i = 0; i < Dd.length; i += 4) { const al = MD[i + 3] / 255; if (!al) continue; const Lp = (Dd[i] + Dd[i + 1] + Dd[i + 2]) / 3, k = al * clamp((Lp - 70) / 100), f = clamp(Lp / 180, 0, 1);
      for (let j = 0; j < 3; j++) Dd[i + j] = lerp(Dd[i + j], CD[i + j] * f, k); }
    ctx.putImageData(I, x0, y0);
  }
  // parlama: tek, belirgin, saf beyaz (≥ 240)
  ctx.save(); ctx.setTransform(M); ctx.fillStyle = '#fffefa'; ctx.beginPath(); ctx.ellipse(D[0] + r * .36, D[1] - r * .3, r * .2, r * .36, -.35, 0, TAU); ctx.fill();
  ctx.beginPath(); ctx.arc(D[0] + r * .5, D[1] + r * .2, r * .08, 0, TAU); ctx.fill(); ctx.restore();
  if (KPK.notext) return;
  kpk_yazi(ctx, KPK_YAZI.b[KPK.yazi] || KPK_YAZI.b[0], { x: 1868, y: 350, cap: 205, maxW: 720, align: 'right', gap: .42, col: '#cfc7b8' });
}
async function kpk_b(ctx) {
  if (!KQ.has('tur5')) return kpk_b6(ctx);
  levha(ctx, KPK_B.cam, () => kpk_bSahne(KPK.t), [.03, 0, 1]);
  if (KPK.renk) kpk_bRenk(ctx);
  if (KPK.renk !== 2) { const c = camOf(KPK_B.cam), { D, r } = KPK_B; ctx.save(); ctx.setTransform(c.s * RS, 0, 0, c.s * RS, -c.x * c.s * RS, -c.y * c.s * RS);
    ctx.fillStyle = KPK_PAPER; ctx.beginPath(); ctx.ellipse(D[0] + r * .4, D[1] - r * .35, r * .17, r * .26, -.4, 0, TAU); ctx.fill(); ctx.restore(); }
  applyPaper(ctx, .8); applyVignette(ctx, .45);
  if (!KPK.notext) kpk_yazi(ctx, KPK_YAZI.b[KPK.yazi] || KPK_YAZI.b[0], { x: 1868, y: 350, cap: 200, maxW: 700, align: 'right', gap: .42 });
}

window.kapakCiz = async () => {
  for (const f of ['400 80px "Bebas Neue"', '400 80px Anton', '900 80px Cinzel']) await document.fonts.load(f, 'BENCHİMŞYTAĞLDIKMÇÖÜ');
  const cv = document.getElementById('c'), ctx = cv.getContext('2d');
  baseT(ctx); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
  if (KPK.v === 'b') await kpk_b(ctx); else await kpk_a(ctx);
  return true;
};
