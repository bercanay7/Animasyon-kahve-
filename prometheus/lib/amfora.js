// Siyah figür katmanı (Hesiodos): dönen amfora frizi. Friz içeriği düz bir şeride çizilir,
// sonra silindir yüzeyine dikey dilimlerle sarılır (kenarlara doğru daralma + gölge). Dönüş = sahne geçişi.
'use strict';
const AMF = { R: 1150, band: [250, 900], circ: 2 * PI * 1150 };
let AMF_STRIP = null;
// rotX: ekran ortasına gelen şerit koordinatı (px). draw(sctx, x0, x1, t): şeridin [x0,x1) aralığını çizer
// (kil zemin hazır gelir; çizim y'si bant içi: 0..bandH). o: {bandTop, bandBot, glaze, clay, light}
function amphoraFrieze(ctx, t, rotX, draw, o = {}) {
  const R = o.R || AMF.R, top = o.top ?? AMF.band[0], bot = o.bot ?? AMF.band[1], bh = bot - top;
  // şerit, bandın üstündeki dil frizini ve altındaki ışın frizini de taşır: hepsi silindirle birlikte döner
  const pt = 130, pb = 190, sh = bh + pt + pb;
  const half = Math.asin(Math.min(1, (W / 2 + 40) / R)), arc = half * R;
  const sw = Math.ceil(arc * 2 + 8);
  if (!AMF_STRIP || AMF_STRIP.width < sw * RS || AMF_STRIP.height !== Math.ceil(sh * RS)) AMF_STRIP = makeCanvas(Math.ceil(sw * RS), Math.ceil(sh * RS));
  const sc = AMF_STRIP.getContext('2d');
  sc.setTransform(1, 0, 0, 1, 0, 0); sc.clearRect(0, 0, AMF_STRIP.width, AMF_STRIP.height);
  sc.setTransform(RS, 0, 0, RS, 0, 0);
  const x0 = rotX - arc - 4;
  sc.fillStyle = o.glaze || C.ink; sc.fillRect(0, 0, sw, sh);
  sc.save(); sc.translate(-x0, 0);
  // süs bantları (şerit koordinatında, çevreye göre sabit)
  if (o.tongues !== false) tongues(sc, x0 - 60, x0 + sw + 60, 20, 80, C.clay, C.red);
  sc.fillStyle = C.clay; sc.fillRect(x0, pt - 14, sw, 4); sc.fillRect(x0, pt + bh + 10, sw, 4);
  if (o.rays !== false) rays(sc, x0 - 60, x0 + sw + 60, pt + bh + 40, 120, C.clay);
  // kil bant
  const g = sc.createLinearGradient(0, pt, 0, pt + bh);
  g.addColorStop(0, o.clayTop || C.clayL); g.addColorStop(1, o.clayBot || C.clay);
  sc.fillStyle = g; sc.fillRect(x0, pt, sw, bh);
  sc.save(); sc.beginPath(); sc.rect(x0, pt, sw, bh); sc.clip(); sc.translate(0, pt); draw(sc, x0, x0 + sw, t); sc.restore();
  sc.restore();
  // gövde: siyah sır
  ctx.fillStyle = o.glaze || C.ink; ctx.fillRect(-50, -50, W + 100, H + 100);
  // dilimleri silindire sar
  const step = 3, y = top - pt;
  for (let sx = -W / 2 - 20; sx < W / 2 + 20; sx += step) {
    const a0 = Math.asin(clamp(sx / R, -1, 1)), a1 = Math.asin(clamp((sx + step) / R, -1, 1));
    const u0 = (a0 + half) * R + 4, u1 = (a1 + half) * R + 4;
    if (u1 <= u0) continue;
    ctx.drawImage(AMF_STRIP, u0 * RS, 0, (u1 - u0) * RS, sh * RS, W / 2 + sx, y, step + .6, sh);
  }
  // silindir gölgesi: ışık sol üstten, kenarlar koyu
  const lg = ctx.createLinearGradient(0, 0, W, 0), lx = o.light ?? .38;
  lg.addColorStop(0, 'rgba(10,5,2,.78)'); lg.addColorStop(.12, 'rgba(10,5,2,.32)');
  lg.addColorStop(lx, 'rgba(255,235,200,.08)'); lg.addColorStop(.86, 'rgba(10,5,2,.34)'); lg.addColorStop(1, 'rgba(10,5,2,.82)');
  ctx.fillStyle = lg; ctx.fillRect(-50, -50, W + 100, H + 100);
  // parlama şeridi (sır yansıması, yumuşak)
  const hx = W * lx, hg = ctx.createLinearGradient(hx - 90, 0, hx + 90, 0);
  hg.addColorStop(0, 'rgba(255,240,220,0)'); hg.addColorStop(.5, 'rgba(255,240,220,.07)'); hg.addColorStop(1, 'rgba(255,240,220,0)');
  ctx.fillStyle = hg; ctx.fillRect(hx - 90, -50, 180, H + 100);
}
// Şeritte yinelenen sahne: x konumu şerit çevresine göre sarılır (sahneler çember üstünde sabit yerlerde)
function amfWrap(x, ref) { const c = AMF.circ; return x + Math.round((ref - x) / c) * c; }
// Kylix tondosu (Lakonya kupası, yukarıdan): daire içinde siyah figür sahne, çevresinde kupa ağzı.
// rot: tondo dönüşü (rad), tilt: 1 = tam yukarıdan, <1 eğik bakış. draw(c, t): tondo yerel koordinatı (merkez 0,0, yarıçap r)
function kylix(ctx, t, x, y, r, rot, draw, o = {}) {
  const tilt = o.tilt ?? 1;
  ctx.save(); ctx.translate(x, y); ctx.scale(1, tilt);
  // kupa gövdesi ve ağız halkaları
  glow(ctx, 0, r * .1, r * 1.9, 'rgba(0,0,0,.55)');
  ctx.fillStyle = o.glaze || C.ink; ctx.beginPath(); ctx.arc(0, 0, r * 1.42, 0, TAU); ctx.fill();
  ctx.strokeStyle = C.clayD; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(0, 0, r * 1.4, 0, TAU); ctx.stroke();
  // sır parıltısı: ince düzgün yay değil, kenarda geniş ve düşük kontrastlı bir hilal (uçlara doğru incelip söner)
  { const g = ctx.createRadialGradient(-r * .75, -r * .85, 0, -r * .75, -r * .85, r * 1.1); g.addColorStop(0, 'rgba(255,232,205,.12)'); g.addColorStop(1, 'rgba(255,232,205,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, r * 1.39, PI * .95, PI * 1.72); ctx.arc(r * .09, r * .1, r * 1.32, PI * 1.72, PI * .95, true); ctx.closePath(); ctx.fill(); }
  ctx.save(); ctx.rotate(rot);
  // tondo bordürü: nar (Lakonya) yerine dil frizi halkası
  ctx.fillStyle = C.clay; ctx.beginPath(); ctx.arc(0, 0, r * 1.08, 0, TAU); ctx.fill();
  ctx.fillStyle = C.ink;
  for (let i = 0; i < 48; i++) { ctx.save(); ctx.rotate(i / 48 * TAU); ctx.beginPath(); ctx.ellipse(0, -r * 1.04, r * .035, r * .045, 0, 0, TAU); ctx.fill(); ctx.restore(); }
  ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(0, 0, r * 1.0, 0, TAU); ctx.stroke();
  // sahne
  ctx.save(); ctx.beginPath(); ctx.arc(0, 0, r * .985, 0, TAU); ctx.clip();
  const g = ctx.createRadialGradient(-r * .3, -r * .3, r * .1, 0, 0, r);
  g.addColorStop(0, C.clayL); g.addColorStop(1, C.clay);
  ctx.fillStyle = g; ctx.fillRect(-r, -r, 2 * r, 2 * r);
  draw(ctx, t, r);
  ctx.restore();
  ctx.restore();
  // sır parlaması (dönmez)
  ctx.fillStyle = 'rgba(255,240,220,.06)'; ctx.beginPath(); ctx.ellipse(-r * .45, -r * .55, r * .5, r * .2, -.6, 0, TAU); ctx.fill();
  ctx.restore();
}
