// Orpheus videosu için kapaklar (film.html?scene=orfe_a / orfe_b): vazo üslubunda, kanca = "arkana bakma" anı
'use strict';
const LK_ORF = { hair: 'long', headgear: 'wreath', garment: 'robe', himation: true };
const LK_EUR = { fem: true, garment: 'robe', earring: true };
const STY_GHOST = { fill: '#DDE7EA', cut: '#2B3A44', red: '#7FA6B8', white: '#FFFFFF', line: '#2B3A44' };
// altın lir: kaplumbağa kabuğu gövde, iki kıvrık kol, boyunduruk ve teller
function lyre(ctx, x, y, s, a = 0) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s);
  glow(ctx, 0, -20, 70, 'rgba(255,214,120,.55)');
  ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  ctx.strokeStyle = '#3A1A0C'; ctx.lineWidth = 9;
  const arms = c => { c.beginPath(); c.moveTo(-16, 8); c.bezierCurveTo(-34, -12, -30, -44, -18, -58); c.moveTo(16, 8); c.bezierCurveTo(34, -12, 30, -44, 18, -58); c.moveTo(-24, -50); c.lineTo(24, -50); };
  arms(ctx); ctx.stroke(); ctx.strokeStyle = '#F2C66E'; ctx.lineWidth = 5; arms(ctx); ctx.stroke();
  ctx.fillStyle = '#F2C66E'; ctx.strokeStyle = '#3A1A0C'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.ellipse(0, 12, 22, 14, 0, 0, TAU); ctx.fill(); ctx.stroke();
  ctx.strokeStyle = '#7A4A1C'; ctx.lineWidth = 1.4; for (const k of [-1, 0, 1]) { ctx.beginPath(); ctx.ellipse(0, 12, 22 - 7 * (k + 1), 14 - 4.5 * (k + 1), 0, 0, TAU); ctx.stroke(); }
  ctx.strokeStyle = '#FFF2C8'; ctx.lineWidth = 1.2; for (let k = -2; k <= 2; k++) { ctx.beginPath(); ctx.moveTo(k * 4.5, -50); ctx.lineTo(k * 3.5, 6); ctx.stroke(); }
  ctx.restore();
}
// figürü ayrı tuvale çizip yön gradyanıyla solduran yardımcı (Eurydike'nin dumana karışması)
function ghostFigure(ctx, f, fade) {
  const oc = makeCanvas(DW, DH), ox = oc.getContext('2d');
  ox.setTransform(ctx.getTransform()); figure(ox, f);
  ox.setTransform(1, 0, 0, 1, 0, 0); ox.globalCompositeOperation = 'destination-in';
  ox.fillStyle = fade(ox); ox.fillRect(0, 0, DW, DH);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(oc, 0, 0); ctx.restore();
}
function smoke(ctx, x, y, w, h, seed, col) {
  const r = rng(seed);
  for (let i = 0; i < 26; i++) { const px = x + (r() - .5) * w, py = y + (r() - .5) * h, rr = 40 + r() * 110; glow(ctx, px, py, rr, col); }
}
function orfeDraw(ctx, o) {
  // sol: yukarı dünyanın çıkışı (sıcak ışık); sağ: yeraltının karanlığı
  ctx.fillStyle = '#070405'; ctx.fillRect(0, 0, W, H);
  const lg = ctx.createLinearGradient(0, 0, W, 0);
  lg.addColorStop(0, '#F6D9A0'); lg.addColorStop(.28, '#D9874C'); lg.addColorStop(.55, '#3A1710'); lg.addColorStop(1, '#070405');
  ctx.fillStyle = lg; ctx.fillRect(0, 0, W, H);
  glow(ctx, 120, 470, 760, 'rgba(255,236,190,.65)');
  // mağara ağzı kemeri ve zemin
  ctx.fillStyle = '#120807'; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(W, 0); ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.lineTo(0, 1010);
  ctx.quadraticCurveTo(40, 180, 470, 120); ctx.quadraticCurveTo(620, 100, 700, 0); ctx.closePath();
  ctx.save(); ctx.globalAlpha = .55; ctx.fill(); ctx.restore();
  ctx.fillStyle = '#140908'; ctx.fillRect(0, 1000, W, 80);
  // yakın plan: yüzler küçük boyutta da okunsun (figürler kamerayla büyütülür, yazı ve arka plan sabit)
  ctx.save(); cam(ctx, { x: o.cx ?? 980, y: o.cy ?? 600, z: o.z ?? 1.38 }, 1);
  // Eurydike: sağda, soluk hayalet; elleri Orpheus'a uzanır, alt yarısı ve sağı dumana karışır
  smoke(ctx, 1500, 760, 700, 520, 11, 'rgba(120,150,165,.10)');
  const ex = o.ex ?? 1430, es = o.es ?? 10.5, ey = o.ey ?? 1010;
  glow(ctx, ex - 40, ey - 360, 380, 'rgba(170,205,220,.32)');
  ghostFigure(ctx, { x: ex, y: ey, s: es, dir: -1, lk: LK_EUR, sty: STY_GHOST, cutCol: '#2B3A44', margin: 160,
    p: { torso: .16, neck: .12, head: .06, shN: 1.8, elN: .5, shF: 1.3, elF: .8, handN: 'open', handF: 'open', brow: 1.8, smile: -.7, mouthOpen: .3, hipN: .1, hipF: -.1 }, faceW: 1.5 },
    c => { const g = c.createLinearGradient(0, (ey - 300) * RS, 0, (ey + 120) * RS); g.addColorStop(0, 'rgba(0,0,0,.92)'); g.addColorStop(.45, 'rgba(0,0,0,.7)'); g.addColorStop(1, 'rgba(0,0,0,0)'); return g; });
  smoke(ctx, ex + 40, 900, 520, 260, 17, 'rgba(12,8,9,.55)');
  // Orpheus: solda, büyük; ışığa giderken başını geriye çevirmiş (sağa bakar), yakın eli ona uzanır, uzak elinde lir
  let wF = null;
  figure(ctx, { x: o.ox ?? 560, y: o.oy ?? 960, s: o.os ?? 12.5, lk: LK_ORF, margin: 160, faceW: 1.5,
    p: { torso: -.08, neck: .05, head: -.08, shN: 1.35, elN: .35, handN: 'open', shF: .55, elF: 1.6, handF: 'fist', brow: 2.4, smile: -.9, mouthOpen: 1.0, hipN: .3, knN: .15, hipF: -.35, knF: .2 },
    onJoints: (J, M) => { const r = ctx.getTransform().inverse().transformPoint(M.transformPoint(new DOMPoint(J.AF.wr[0], J.AF.wr[1]))); wF = [r.x, r.y]; } });
  if (wF) lyre(ctx, wF[0] + 10, wF[1] - 10, o.ls ?? 2.3, -.25);
  // karanlıktan uzanan gölge eller Eurydike'yi geri çeker (kanca: geri dönüyor)
  if (o.shade) { // deneme: küçük boyutta kara şerit gibi okunduğu için kapalı
    const arm = (x0, y0, x1, y1, w, seed) => {
      ctx.save(); ctx.shadowColor = 'rgba(90,140,165,.55)'; ctx.shadowBlur = 26;
      ctx.fillStyle = '#040203'; ctx.beginPath();
      ctx.moveTo(x0, y0 - w); ctx.bezierCurveTo(lerp(x0, x1, .4), y0 - w * 1.4, lerp(x0, x1, .7), y1 - w * .8, x1 + 30, y1 - w * .5);
      for (let k = 0; k < 4; k++) { const fy = y1 - w * .5 + k * w * .33; ctx.lineTo(x1 - 28 - (k === 1 || k === 2 ? 14 : 0), fy - 6); ctx.lineTo(x1 - 24 - (k === 1 || k === 2 ? 14 : 0), fy + 8); ctx.lineTo(x1 + 20, fy + 10); }
      ctx.lineTo(x1 + 24, y1 + w * .7); ctx.bezierCurveTo(lerp(x0, x1, .7), y1 + w, lerp(x0, x1, .4), y0 + w * 1.2, x0, y0 + w);
      ctx.closePath(); ctx.fill(); ctx.restore();
    };
    arm(2200, 560, ex + 70, ey - 360, 34, 1);
    arm(2200, 820, ex + 90, ey - 200, 40, 2);
  }
  // Eurydike'den kopan kıvılcımlar karanlığa savrulur (kayboluyor)
  { const r = rng(5); for (let i = 0; i < 46; i++) { const px = ex + 40 + r() * 330, py = ey - 470 + r() * 520, rr = 2 + r() * 5;
    ctx.fillStyle = `rgba(215,232,240,${.25 + r() * .55})`; ctx.beginPath(); ctx.arc(px, py, rr, 0, TAU); ctx.fill(); } }
  ctx.restore();
  // yazı
  const sh = { shadow: 'rgba(0,0,0,.85)', blur: 26 };
  if (o.L1) txt(ctx, o.L1, o.tx ?? 1880, o.ty1 ?? 140, { font: `900 ${o.f1 ?? 138}px Cinzel`, col: '#FFF1D2', align: 'right', ls: 4, stroke: 'rgba(10,4,3,.9)', sw: 14, ...sh });
  if (o.L2) txt(ctx, o.L2, o.tx ?? 1880, o.ty2 ?? 290, { font: `900 ${o.f2 ?? 162}px Cinzel`, col: '#E2483A', align: 'right', ls: 4, stroke: 'rgba(10,4,3,.95)', sw: 16, ...sh });
  applyVignette(ctx, .45);
}
SCENES.orfe_a = ctx => orfeDraw(ctx, { L1: 'ARKANA', L2: 'BAKMA!' });
SCENES.orfe_b = ctx => orfeDraw(ctx, { L1: 'NEDEN', L2: 'BAKTI?', f1: 150, f2: 170 });
