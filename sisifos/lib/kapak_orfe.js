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

// ——— Sulu boya sürümü (Orpheus videosunun üslubu: sulu boya, canlı renkler) ———
// organik kenarlı leke: kenarlar gürültüyle bozulur, birkaç yarı saydam katman üst üste (ıslak kenar koyulaşması dahil)
function wcBlob(ctx, x, y, rx, ry, col, o = {}) {
  const r = rng(o.seed ?? 1), n = 48, layers = o.layers ?? 6, a = o.a ?? .14;
  for (let L = 0; L < layers; L++) {
    const pts = [];
    for (let i = 0; i < n; i++) { const t = i / n * TAU, k = 1 + (noise1(i * .35 + L * 3.1, (o.seed ?? 1) + L) * .22) + (r() - .5) * .05;
      pts.push([x + Math.cos(t) * rx * k * (1 - L * .04), y + Math.sin(t) * ry * k * (1 - L * .04)]); }
    ctx.save(); ctx.filter = `blur(${o.blur ?? 6}px)`; ctx.globalAlpha = a; ctx.fillStyle = col;
    ctx.beginPath(); spline(ctx, pts); ctx.fill();
    if (L === 0) { ctx.filter = 'blur(4px)'; ctx.globalAlpha = a * .9; ctx.strokeStyle = col; ctx.lineWidth = 10; ctx.stroke(); } // ıslak kenar (yumuşak, tek kat: çizgi gibi okunmaz)
    ctx.restore();
  }
}
// kâğıt dokusu: ince benek + lif, çarpma ile
let WC_PAPER = null;
function wcPaper() {
  if (WC_PAPER) return WC_PAPER;
  const c = makeCanvas(960, 540), x = c.getContext('2d'), r = rng(77);
  x.fillStyle = '#fff'; x.fillRect(0, 0, 960, 540);
  const id = x.getImageData(0, 0, 960, 540), d = id.data;
  for (let i = 0; i < d.length; i += 4) { const v = 236 + (r() * 19) | 0; d[i] = v; d[i + 1] = v - 2; d[i + 2] = v - 8; }
  x.putImageData(id, 0, 0);
  x.globalAlpha = .07; x.strokeStyle = '#6a5a4a';
  for (let i = 0; i < 900; i++) { const px = r() * 960, py = r() * 540, l = 3 + r() * 9, a = r() * PI; x.beginPath(); x.moveTo(px, py); x.lineTo(px + Math.cos(a) * l, py + Math.sin(a) * l); x.stroke(); }
  WC_PAPER = c; return c;
}
// figürü sulu boyaya çevir: düz renkle ayrı tuvale çizer, içte açık–koyu dalga (ıslak üstüne ıslak), dışa sızma ve koyu ıslak kenar
function wcFigure(ctx, f, cols, o = {}) {
  const T = ctx.getTransform();
  const oc = makeCanvas(DW, DH), ox = oc.getContext('2d'); ox.setTransform(T); figure(ox, f);
  ox.setTransform(1, 0, 0, 1, 0, 0); ox.globalCompositeOperation = 'source-atop';
  const b = o.box || [0, 0, W, H];
  const g = ox.createLinearGradient(b[0] * RS, b[1] * RS, b[2] * RS, b[3] * RS);
  cols.forEach((c, i) => g.addColorStop(i / (cols.length - 1), c));
  ox.globalAlpha = .55; ox.fillStyle = g; ox.fillRect(0, 0, DW, DH); ox.globalAlpha = 1;
  { const r = rng(o.seed ?? 3); for (let i = 0; i < 40; i++) { ox.save(); ox.filter = 'blur(18px)'; ox.globalAlpha = .18; ox.fillStyle = r() < .5 ? 'rgba(255,255,255,1)' : cols[(r() * cols.length) | 0];
    ox.beginPath(); ox.arc(r() * DW, r() * DH, (20 + r() * 70) * RS, 0, TAU); ox.fill(); ox.restore(); } }
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (o.alphaMask) { const m = makeCanvas(DW, DH), mx = m.getContext('2d'); mx.drawImage(oc, 0, 0); mx.globalCompositeOperation = 'destination-in'; mx.fillStyle = o.alphaMask(mx); mx.fillRect(0, 0, DW, DH); ox.globalCompositeOperation = 'copy'; ox.drawImage(m, 0, 0); }
  ctx.filter = `blur(${7 * RS}px)`; ctx.globalAlpha = .45; ctx.drawImage(oc, 0, 0);            // pigment sızması
  ctx.filter = 'none'; ctx.globalAlpha = o.a ?? .92; ctx.drawImage(oc, 0, 0);
  ctx.filter = `blur(${1.2 * RS}px) brightness(.55)`; ctx.globalAlpha = .35; ctx.globalCompositeOperation = 'multiply';
  ctx.drawImage(oc, 0, 0);                                                                       // koyu ıslak kenar
  ctx.restore();
}
function orfeWater(ctx, o) {
  ctx.drawImage(wcPaper(), 0, 0, W, H);
  // gökyüzü ve ışık: solda altın–turuncu çıkış ışığı, sağda mor–çivit yeraltı; aralarda turkuaz sis
  ctx.save(); ctx.globalCompositeOperation = 'multiply';
  wcBlob(ctx, 330, 420, 720, 640, '#FFC44D', { seed: 2, a: .2, blur: 14 });
  wcBlob(ctx, 250, 380, 420, 380, '#FF8A3D', { seed: 3, a: .16, blur: 10 });
  wcBlob(ctx, 1500, 420, 760, 700, '#3B2A8C', { seed: 4, a: .2, blur: 14, layers: 8 });
  wcBlob(ctx, 1650, 820, 560, 380, '#1B1650', { seed: 5, a: .22, blur: 12 });
  wcBlob(ctx, 1240, 300, 420, 300, '#8A3FA8', { seed: 6, a: .14, blur: 12 });
  wcBlob(ctx, 960, 700, 520, 260, '#2AA5A0', { seed: 7, a: .12, blur: 16 });
  wcBlob(ctx, 980, 1040, 1300, 200, '#2B1B3A', { seed: 8, a: .2, blur: 10 });
  ctx.restore();
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, 230, 420, 520, 'rgba(255,214,140,.55)'); ctx.restore();
  // kâğıt üstünde serpilmiş boya damlaları
  { const r = rng(31); ctx.save(); ctx.globalCompositeOperation = 'multiply'; for (let i = 0; i < 60; i++) { ctx.globalAlpha = .25 + r() * .3; ctx.fillStyle = r() < .5 ? '#3B2A8C' : '#8A3FA8'; ctx.beginPath(); ctx.arc(1150 + r() * 760, 60 + r() * 980, 1.5 + r() * 5, 0, TAU); ctx.fill(); } ctx.restore(); }
  ctx.save(); cam(ctx, { x: 980, y: 600, z: 1.38 }, 1);
  const ex = 1430, es = 10.5, ey = 1010;
  // Eurydike: ışıyan hayalet, alt yarısı mor sise karışır
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, ex - 40, ey - 360, 360, 'rgba(160,220,255,.35)'); ctx.restore();
  wcFigure(ctx, { x: ex, y: ey, s: es, dir: -1, lk: LK_EUR, sty: { fill: '#BFE6F5', cut: '#25407A', red: '#7A5FD0', white: '#FFFFFF', line: '#25407A' }, cutCol: '#25407A', margin: 160, faceW: 1.5,
    p: { torso: .16, neck: .12, head: .06, shN: 1.8, elN: .5, shF: 1.3, elF: .8, handN: 'open', handF: 'open', brow: 1.8, smile: -.7, mouthOpen: .3, hipN: .1, hipF: -.1 } },
    ['#E8F7FF', '#9FD6F0', '#B8A2F0'], { seed: 9, box: [ex - 300, ey - 520, ex + 200, ey + 50], a: .9,
      alphaMask: c => { const g = c.createLinearGradient(0, ((ey - 470 - 600) * 1.38 + 600) * RS, 0, ((ey - 110 - 600) * 1.38 + 600) * RS); g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(.45, 'rgba(0,0,0,.8)'); g.addColorStop(1, 'rgba(0,0,0,0)'); return g; } });
  // eteği mor sise karışır: altta sis lekeleri
  ctx.save(); ctx.globalCompositeOperation = 'screen'; wcBlob(ctx, ex + 20, ey - 90, 260, 120, '#7C6BD6', { seed: 15, a: .16, blur: 18 }); wcBlob(ctx, ex + 120, ey - 20, 300, 110, '#5AC8D8', { seed: 16, a: .1, blur: 20 }); ctx.restore();
  // Orpheus: canlı kırmızı–turuncu pelerin, altın lir
  let wF = null;
  wcFigure(ctx, { x: 560, y: 960, s: 12.5, lk: LK_ORF, sty: { fill: '#D9452B', cut: '#5A1408', red: '#FFC44D', white: '#FFF4E0', line: '#5A1408' }, cutCol: '#5A1408', margin: 160, faceW: 1.5,
    p: { torso: -.08, neck: .05, head: -.08, shN: 1.35, elN: .35, handN: 'open', shF: .55, elF: 1.6, handF: 'fist', brow: 2.4, smile: -.9, mouthOpen: 1.0, hipN: .3, knN: .15, hipF: -.35, knF: .2 },
    onJoints: (J, M) => { const rr = ctx.getTransform().inverse().transformPoint(M.transformPoint(new DOMPoint(J.AF.wr[0], J.AF.wr[1]))); wF = [rr.x, rr.y]; } },
    ['#FFB347', '#E8452C', '#B0203A', '#6B1D4A'], { seed: 12, box: [300, 300, 800, 1000] });
  if (!wF) figure(ctx, { x: 560, y: 960, s: 12.5, lk: LK_ORF, alpha: 0, p: { shF: .55, elF: 1.6 }, onJoints: (J, M) => { const rr = ctx.getTransform().inverse().transformPoint(M.transformPoint(new DOMPoint(J.AF.wr[0], J.AF.wr[1]))); wF = [rr.x, rr.y]; } });
  if (wF) lyre(ctx, wF[0] + 10, wF[1] - 10, 2.3, -.25);
  // Eurydike'den kopan ışık zerreleri
  { const r = rng(5); ctx.save(); ctx.globalCompositeOperation = 'lighter'; for (let i = 0; i < 46; i++) { const px = ex + 40 + r() * 330, py = ey - 470 + r() * 520, rr = 2 + r() * 5;
    ctx.fillStyle = `rgba(190,235,255,${.25 + r() * .55})`; ctx.beginPath(); ctx.arc(px, py, rr, 0, TAU); ctx.fill(); } ctx.restore(); }
  ctx.restore();
  ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = .55; ctx.drawImage(wcPaper(), 0, 0, W, H); ctx.restore(); // kâğıt dokusu her şeyin üstünde
  const sh = { shadow: 'rgba(20,10,40,.85)', blur: 22 };
  txt(ctx, o.L1, 1880, 140, { font: `900 ${o.f1 ?? 138}px Cinzel`, col: '#FFFFFF', align: 'right', ls: 4, stroke: '#1B1650', sw: 16, ...sh });
  txt(ctx, o.L2, 1880, 290, { font: `900 ${o.f2 ?? 162}px Cinzel`, col: '#FFD23F', align: 'right', ls: 4, stroke: '#1B1650', sw: 18, ...sh });
}
SCENES.orfe_wa = ctx => orfeWater(ctx, { L1: 'ARKANA', L2: 'BAKMA!' });
SCENES.orfe_wb = ctx => orfeWater(ctx, { L1: 'NEDEN', L2: 'BAKTI?', f1: 150, f2: 170 });
