// Üslup karesi: yanan göl (A02). Dünya koordinatı 1920×1080.
// Değer planı (göz yormasın diye üç büyük kütle): zifiri tonoz (düz siyah), ufukta figürün arkasında tek parlak leke,
// koyu göl. Tarama yalnız geçişlerde; çizgi doğrultusu az (yatay göl, kavisli duman, ışın).
'use strict';
// cizGol: açık levhaya çizer (GR.begin/engrave çağırmaz).
// o: {eyes (göz açıklığı 0–1), chains (false: zincir yok), fig (false: figür yok),
//     head (baş eğimi; .42), lean (.04), rise (figürün sudan yükselişi, px), fx (figür ekseni), sway (kanat salınımı, 0 = yok),
//     open/lift (kanat açılışı için 0..1 ek: 0 = üslup karesi), legs (true: bacaklar; ayağa kalkış), loose (0..1 zincirlerin kopup düşmesi),
//     shaft (0..1 üstten figüre inen izin huzmesi), mid (figürün yanında çizilecek ek: (J) => {}, göl ile ön alevler arasında),
//     dim (0..1: sahneyi karanlığa gömer; açılış için), front (false: ön alevler ve kaya yok)}
function cizGol(t, o = {}) {
  const { tx, tone, fill } = GR;
  const FX = o.fx ?? 880, HZ = 600, WY = 800;         // figür ekseni, ufuk, su çizgisi (figürün beli)
  // ── gök: zifiri; yalnız ufka yakın dar bir kuşak aydınlık ──
  let g = tx.createLinearGradient(0, 0, 0, HZ);
  g.addColorStop(0, tone(.02)); g.addColorStop(.55, tone(.04)); g.addColorStop(.84, tone(.14)); g.addColorStop(1, tone(.34));
  tx.fillStyle = g; tx.fillRect(-200, -400, W + 400, HZ + 400);
  PR.glow(880 + 30, HZ - 10, 150, 700, 1, 1);          // ufuk parıltısı: karenin odağı, figürün arkası
  PR.glow(880 + 30, HZ - 40, 60, 340, 1, .8);
  // yitik cennetin yarığı: sağ üstte keskin, dar bir yırtık; oradan başa inen birkaç ince huzme
  PR.rays(1610, 30, 0, 0, 0, 0, { seed: 4, slit: { w: 210, h: 22, a: -.12 } });
  PR.shafts(1590, 44, 880 + 120, 500, { n: 6, w: 17, slitW: 70, spread: 560, seed: 6, t, v: .94, len: [.3, .92] });
  // duman tonozu: iki koyu kütle; yalnız ufuk ışığına bakan yumruların kenarında birer ikişer açık hilal; orta açık kalır (odak)
  PR.cloud({ x: 250, y: 330, w: 900, h: 230, seed: 12, lit: [.8, .6], base: .02, hi: .85, core: .02, n: 4, drift: Math.sin(t * .1) * 10 });
  // sağ küme: tohum 19 (17'de sağ uçta salyangoz gibi kıvrık hilal vardı; kurul tur 6)
  PR.cloud({ x: 1640, y: 350, w: 800, h: 210, seed: 19, lit: [-.8, .6], base: .02, hi: .8, core: .02, n: 4, drift: Math.sin(t * .08 + 1) * 10 });
  // ── göl ──
  PR.lake(HZ, H, t, { tone: [.2, .02], crests: 26, p0: 9.5, refl: [{ x: 880 + 30, w: 460, v: .95, len: 380, rows: 26 }, { x: 340, w: 200, v: .6, len: 220 }, { x: 1440, w: 240, v: .65, len: 240 }] });
  PR.flameBank(-60, W + 60, HZ + 2, 30, t, 1, { env: f => .2 + .8 * Math.pow(Math.sin(f * PI), 2) });
  // sağ uzak alevler: dil kütlesi taban şeridinin birkaç katı yükselir (beyaz şerit üstünde diken okuması olmasın; kurul tur 6)
  PR.flameBank(1250, 1690, 674, 125, t, 5, { n: 5, wr: .55, curl: .6, speed: .6, solidBelow: 500, strip: .16, frags: false, env: f => .4 + .6 * Math.sin(f * PI) });
  // sol uzak alev öbeği kaldırıldı: kanadın tüy aralığından mum alevi gibi görünüyordu (kurul tur 6); sol yanı ufuk bandı ve ön alev taşır
  if (o.shaft) gol_izin(FX, o.shaft, t);
  // ── Şeytan: belden yukarısı gölün üstünde; arkadan aydınlanan koyu kütle, yüzü yarığa dönük ──
  const br = Math.sin(t * .6) * 2, h = 98, rise = o.rise || 0;
  let J = null;
  const LIT = [.55, -.8];
  if (o.fig !== false) {
    J = SF.rig({ x: FX, y: WY + 26 + br * .3 - rise, h, facing: 1, twist: .3, lean: o.lean ?? .04, head: o.head ?? .42, shTilt: -.06,
      armN: o.armN || [-.5, .22], armF: o.armF || [.55, -.2], legN: [.04, -.05], legF: [-.08, -.03] });
    // kanatlar suyun üstünde kalan kısmıyla çizilir (uçları suya girer)
    const sw = (o.sway ?? 0) * Math.sin(t * .42), op = o.open || 0, lf = o.lift || 0;
    GR.save(); { const C = new Path2D(); C.rect(-4000, -4000, 12000, 4000 + WY); for (const c of [GR.tx, GR.px, GR.ox]) c.clip(C); }
    for (const [side, P] of [[-1, { span: 640, open: .78, lift: .5, droop: .25, rot: -.1, seed: 31, root: .1 }], [1, { span: 560, open: .7, lift: .2, droop: .8, rot: .12, seed: 32, root: .12 }]]) {
      const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
      const Q = Object.assign({}, P, { open: lerp(P.open, 1, op), lift: lerp(P.lift, .85, lf), droop: lerp(P.droop, .1, lf), span: P.span * (1 + .12 * lf) });
      GR.frame(sh[0] - side * h * .25, sh[1] + h * .15 + br, P.rot + sw * (side < 0 ? 1 : -.7) - side * .25 * lf, side, 1);
      KN.feathered(Object.assign({ dark: .92, rim: .75, ruin: .65, t, lit: [LIT[0] * side, LIT[1]] }, Q));
      GR.unframe();
    }
    GR.restore();
    PR.glow(FX, WY + 10, 6, 170, 1, .2);                 // su çizgisinde ateş ışığı (figürün arkasında kalır)
    const leg = !!o.legs;
    SF.draw(J, { lum: o.lum ?? 0, lit: LIT, t, legs: leg, skirt: leg, waterY: WY, eye: o.eyes ?? 1, wind: .6, cloak: 1.2, halo: 3.5, lines: 2 });
    // zincirler (kırılmaz zincir; I.48): ön kolun suya girdiği noktadan çıkar, su yüzeyinde dışa uzanır
    if (o.chains !== false) {
      const lo = clamp(o.loose || 0);
      GR.tx.save(); { const C = new Path2D(); C.rect(-4000, -4000, 12000, 4000 + WY + 16); GR.tx.clip(C); }
      for (const [el, wr, dx] of [[J.elN, J.wrN, -120], [J.elF, J.wrF, 120]]) {
        if (!lo) { const u = clamp((WY - 30 - el[1]) / ((wr[1] - el[1]) || 1)), x0 = lerp(el[0], wr[0], u); PR.chain(x0, WY - 30, x0 + dx, WY + 46, 34, { sag: -8, v: .9 }); }
        else { // kopan zincir: bilekten ayrılıp suya düşer (yerçekimi), halkalar suya girer
          const fall = lo * lo * 260, x0 = wr[0] + dx * .2 * lo, y0 = Math.max(wr[1], WY - 60) + fall;
          PR.chain(x0, y0, x0 + dx * (1 - .4 * lo), y0 + 70 + fall * .2, 34, { sag: 10 + 30 * lo, v: .9 });
        }
      }
      GR.tx.restore();
    }
  }
  if (o.mid) o.mid(J);
  if (o.front !== false) {
    // bel hizası: su çizgisinde ince ışık ve figürü saran alevler (öndeki kütle). Kopuk alev uçları yok (frags: false):
    // kanadın önünde damla gibi asılı kalan uç 'mum alevi' okuması veriyordu (kurul tur 6)
    PR.flameBank(FX - 340, FX - 70, WY + 40, 150, t, 7, { n: 4, env: f => .45 + .55 * (1 - f), wr: .6, solidBelow: 500, speed: .5, strip: .5, frags: false });
    PR.flameBank(FX + 80, FX + 370, WY + 38, 170, t, 8, { n: 4, env: f => .45 + .55 * f, wr: .6, solidBelow: 500, speed: .5, strip: .5, frags: false });
    // sağ ön: büyük alev dilleri (çerçeve; tohum 27: diller tek kütle hâlinde yukarı akar, X biçimli çift yok; kurul tur 6); sol ön: kaya kıyısı (koyu kütle, ışıklı sırt)
    PR.flameBank(1480, W + 120, H + 30, 380, t, 27, { env: f => .5 + .5 * f, wr: .5, base: .3, edge: .4, core: .8, frags: false, speed: .55, curl: .45, lean: -.1 });
    const RK = [[-20, 556], [38, 566], [72, 584], [96, 612], [132, 640], [170, 648], [206, 664], [214, 700], [238, 732], [272, 748], [300, 772], [304, 818], [320, 862], [352, 884], [384, 916], [378, 968], [398, 1010], [404, H + 20], [-20, H + 20]];
    const RP = PR.rock(RK, { lit: [.85, -.45], hi: .05, mid: .03, lo: .02, seed: 2, th: -.9, rim: 6, facets: 10 });
    PR.cuts(RK.slice(0, 11), [-.5, .87], { len: [16, 190], gap: [44, 130], w: 6, seed: 5, clip: RP, bend: -.35 });
  }
  if (o.dim) { tx.save(); tx.globalAlpha = clamp(o.dim); tx.fillStyle = tone(.02); tx.fillRect(-400, -800, W + 800, H + 1600); tx.restore(); }
  return J;
}
// "göklerin izniyle" (I.210–213): yarıktan figüre inen dar, keskin kenarlı ışık sütunu; a: 0..1 şiddet
function gol_izin(fx, a, t) {
  const { tx, tone } = GR;
  const sx = 1610, sy = 30, ex = fx + 10, ey = 820, w0 = 34, w1 = 150 * a + 40;
  const P = new Path2D(), dx = ex - sx, dy = ey - sy, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L;
  P.moveTo(sx + nx * w0 / 2, sy + ny * w0 / 2); P.lineTo(ex + nx * w1 / 2, ey + ny * w1 / 2); P.lineTo(ex - nx * w1 / 2, ey - ny * w1 / 2); P.lineTo(sx - nx * w0 / 2, sy - ny * w0 / 2); P.closePath();
  const g = tx.createLinearGradient(sx, sy, ex, ey);
  g.addColorStop(0, tone(.3 + .66 * a)); g.addColorStop(.6, tone(.2 + .5 * a)); g.addColorStop(1, tone(.08 + .3 * a));
  tx.save(); tx.globalCompositeOperation = 'lighten'; tx.fillStyle = g; tx.fill(P); tx.restore();
  GR.px.fillStyle = GR.hatch({ th: Math.atan2(dy, dx), id: 7 }); GR.px.fill(P);
}
// tek başına üslup karesi (uslup.html)
function sahneGol(t, o = {}) {
  GR.begin(.04, 0, 1, o.cam); cizGol(t, o); GR.engrave(o.out || ctx);
  applyPaper(o.out || ctx, .8); applyVignette(o.out || ctx, .45);
}

// ═════════ Kıyı seti (KIY): yanan kıyı ═════════
// Değer planı: zifiri tonoz; ufukta, figürün arkasında alev duvarının parıltısı (tek odak); ortada dar göl şeridi;
// önde koyu, kırık kıyı (ışığa bakan sırtında ince kenar ışığı, içinde düzensiz beyaz vuruşlar); kıyıda seyrek alçak alevler.
// o: {fx (odak ve figür ekseni), gy (kıyı sırtı y), wall (alev duvarı boyu), fig: (gy) => {} figür çizimi, front (false: ön kaya yok), hz (ufuk)}
function cizKiyi(t, o = {}) {
  const { tx, tone } = GR, FX = o.fx ?? 900, HZ = o.hz ?? 560, GY = o.gy ?? (HZ + 220);
  let g = tx.createLinearGradient(0, -400, 0, HZ);
  g.addColorStop(0, tone(.02)); g.addColorStop(.6, tone(.03)); g.addColorStop(.88, tone(.12)); g.addColorStop(1, tone(.3));
  tx.fillStyle = g; tx.fillRect(-400, -800, W + 800, HZ + 800);
  PR.glow(FX, HZ - 10, 100, 400, 1, 1);
  PR.glow(FX, HZ - 50, 50, 280, 1, .8);
  PR.cloud({ x: 60, y: HZ - 290, w: 900, h: 230, seed: 12, lit: [.75, .65], base: .02, hi: .8, core: .02, n: 4, drift: Math.sin(t * .1) * 10 });
  PR.cloud({ x: 1760, y: HZ - 330, w: 960, h: 240, seed: 19, lit: [-.75, .65], base: .02, hi: .75, core: .02, n: 4, drift: Math.sin(t * .08 + 1) * 10 });
  // göl şeridi ve uzak alev duvarı (göl kıyısının ötesinde; I.61–62: "her yanı yanan bir fırın")
  PR.lake(HZ, GY + 60, t, { tone: [.22, .04], crests: 14, p0: 9.5, refl: [{ x: FX, w: 420, v: .9, len: 200, rows: 14 }] });
  const wl = o.wall ?? 1;
  PR.flameBank(-80, W + 80, HZ + 4, 70 * wl, t, 61, { env: f => { const d = Math.abs(f * (W + 160) - 80 - FX) / 420; return .25 + .75 * Math.min(1, d * d); } });
  PR.flameBank(-40, FX - 330, HZ + 10, 190 * wl, t, 62, { band: false, n: 4, wr: .7, curl: .4, speed: .55, solidBelow: 500, strip: .5, frags: false, env: f => .4 + .6 * f });
  PR.flameBank(FX + 340, W + 40, HZ + 10, 200 * wl, t, 63, { band: false, n: 4, wr: .7, curl: .4, speed: .55, solidBelow: 500, strip: .5, frags: false, env: f => .4 + .6 * (1 - f) });
  // kıyı: koyu, kırık sırt; ışık arkadan (alev duvarı), sırtta ince kenar ışığı
  const R = rng(7), K = [[-200, GY + 20]];
  for (let x = -120; x <= W + 200; x += 80) K.push([x, GY + Math.sin(x * .004 + 1) * 16 + (R() - .5) * 18 - 10 * Math.exp(-Math.pow((x - FX) / 260, 2))]);
  K.push([W + 200, H + 300], [-200, H + 300]);
  const KP = PR.rock(K, { lit: [0, -1], hi: .04, mid: .03, lo: .02, seed: 9, th: -.15, rim: 5, facets: 9 });
  // sol önde kırık kaya çıkıntısı (göldeki kayanın eşi): koyu kütle, ışıklı sırt, içe giren vuruşlar
  if (o.front !== false) {
    const dy = HZ - 560, RK = [[-20, 600], [60, 612], [118, 640], [150, 676], [196, 690], [232, 724], [262, 770], [300, 800], [318, 846], [356, 880], [372, 930], [396, 990], [404, H + 20], [-20, H + 20]].map(([x, y]) => [x, y + dy]);
    const RP = PR.rock(RK, { lit: [.85, -.5], hi: .05, mid: .03, lo: .02, seed: 4, th: -.9, rim: 6, facets: 9 });
    PR.cuts(RK.slice(0, 10), [-.5, .87], { len: [16, 170], gap: [50, 130], w: 6, seed: 6, clip: RP, bend: -.35 });
  }
  if (o.fig) o.fig(GY);
  // ön çerçeve: sağ altta büyük alev dilleri (göldeki çerçevenin eşi)
  if (o.front !== false) PR.flameBank(1500, W + 120, H + 40, 340, t, 27, { env: f => .5 + .5 * f, wr: .5, base: .3, edge: .4, core: .8, frags: false, speed: .55, curl: .45, lean: -.1 });
  return { GY, HZ, FX };
}
// Şeytan kıyıda ayakta (orta plan). p: {x, gy, h, armN, armF, head, open, lift, spear, lum, t}
function kiy_seytan(t, p) {
  const h = p.h ?? 56, J = SF.rig({ x: p.x, y: p.gy - 3.95 * h, h, facing: p.facing ?? 1, twist: p.twist ?? .3, lean: p.lean ?? -.02, head: p.head ?? .1, shTilt: p.shTilt ?? -.04,
    armN: p.armN || [.15, .2], armF: p.armF || [-.12, .15], legN: p.legN || [.12, -.05], legF: p.legF || [-.1, -.03] });
  const LIT = p.lit || [.3, -.95];
  if (p.wings !== false) for (const [side, P] of [[-1, { span: 9.2 * h, open: .62, lift: .45, droop: .55, rot: -.06, seed: 31, root: .1 }], [1, { span: 8.2 * h, open: .58, lift: .3, droop: .75, rot: .1, seed: 32, root: .12 }]]) {
    const sh = side < 0 ? (J.shN[0] < J.shF[0] ? J.shN : J.shF) : (J.shN[0] < J.shF[0] ? J.shF : J.shN);
    GR.frame(sh[0] - side * h * .25, sh[1] + h * .15, P.rot, side, 1);
    KN.feathered(Object.assign({ dark: .92, rim: .75, ruin: .6, t, lit: [LIT[0] * side, LIT[1]] }, P, { open: lerp(P.open, 1, p.open || 0), lift: lerp(P.lift, .8, p.lift || 0) }));
    GR.unframe();
  }
  if (p.mid) p.mid(J);
  let sp = p.spear;
  if (sp && sp.bottomY != null) { const g = J['wr' + (sp.grip || 'N')], L = (sp.len ?? 7.5) * h; sp = Object.assign({}, sp, { up: clamp(1 - (sp.bottomY - g[1]) / L, .2, .95) }); }
  SF.draw(J, { lum: p.lum ?? 0, lit: LIT, t, legs: p.legs ?? true, skirt: true, eye: p.eye ?? 1, wind: .7, cloak: p.cloak ?? 1.3, halo: 3.5, lines: 2, spear: sp, seed: p.seed || 3 });
  return J;
}
