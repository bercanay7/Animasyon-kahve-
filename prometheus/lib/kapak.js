// YouTube kapakları (1920×1080'de çizilir, 1280×720'ye küçültülür). Sisifos kapaklarının dili: solda iki satır büyük
// yazı, sağda büyük kırmızı figür baş. Tek odak karenin en parlak noktası (A: ateş, B: soğuk beyaz kelepçe).
// Sağ alt köşe (süre rozeti) boş kalır. SCENE=kapakA node shot.js out 2
'use strict';
function kapakBG(ctx, t, glowAt, warm = true) {
  ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
  const g = ctx.createRadialGradient(glowAt[0], glowAt[1], 0, glowAt[0], glowAt[1], 1300);
  g.addColorStop(0, warm ? 'rgba(150,62,28,.75)' : 'rgba(60,70,95,.5)'); g.addColorStop(.45, warm ? 'rgba(70,28,12,.35)' : 'rgba(30,24,30,.3)'); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  vaseStars(ctx, t, 26, 5, [0, 40, W, 700], [[glowAt[0], glowAt[1], 380]], .4);
}
function kapakText(ctx, l1, l2, col2, o = {}) {
  ctx.save();
  const x = o.x ?? 90;
  txt(ctx, l1, x, o.y1 ?? 250, { font: `900 ${o.s1 || 150}px Cinzel`, col: '#F1E4C8', align: 'left', ls: 2, stroke: 'rgba(14,9,7,.9)', sw: 16, shadow: 'rgba(0,0,0,.7)', blur: 24, force: true });
  txt(ctx, l2, x, o.y2 ?? 440, { font: `900 ${o.s2 || 210}px Cinzel`, col: col2, align: 'left', ls: 3, stroke: 'rgba(14,9,7,.9)', sw: 18, shadow: o.glow || 'rgba(0,0,0,.7)', blur: o.blur || 26, force: true });
  ctx.restore();
}
// Kapak kurulu tur 1 sonrası: akışta karanlık kalmasın (ortalama parlaklık ≈ 70, köşeler ≥ 30), tek odak karenin en parlak noktası,
// büyük harf ≥ %18 (≥ 195 px, 1920'de), figür büyük (baş ≥ 435 px). Film P292 eski kapakBG/kapakText'i kullanır; onlara dokunulmaz.
function kapakBG2(ctx, t, glowAt, o = {}) {
  ctx.fillStyle = o.base || '#2A1912'; ctx.fillRect(0, 0, W, H);
  const g = ctx.createRadialGradient(glowAt[0], glowAt[1], 0, glowAt[0], glowAt[1], o.r || 1125);
  g.addColorStop(0, o.c0 || 'rgba(201,112,63,.62)'); g.addColorStop(.5, o.c1 || 'rgba(140,62,30,.32)'); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  // sol altta sıcak taban ışığı (ölü alan kalmasın), yazının arkası
  glow(ctx, o.bx ?? 260, o.by ?? 1080, o.br ?? 780, o.bc || 'rgba(150,66,30,.42)');
}
function kapakText2(ctx, l1, l2, c1, c2, o = {}) {
  ctx.save(); const x = o.x ?? 90;
  txt(ctx, l1, x, o.y1 ?? 300, { font: `900 ${o.s1 || 150}px Cinzel`, col: c1, align: 'left', ls: 2, stroke: 'rgba(14,9,7,.92)', sw: 16, shadow: 'rgba(0,0,0,.7)', blur: 20, force: true });
  txt(ctx, l2, x, o.y2 ?? 560, { font: `900 ${o.s2 || 280}px Cinzel`, col: c2, align: 'left', ls: 3, stroke: 'rgba(14,9,7,.92)', sw: 20, shadow: o.glow || 'rgba(0,0,0,.7)', blur: o.blur || 22, force: true });
  ctx.restore();
}
// A: "BİLE BİLE ÇALDI": ateşi kaldırmış büyük Prometheus, bakışı aleve; ateş karenin en parlak noktası (çekirdek beyaz)
SCENES.kapakA = (ctx, t) => {
  const fire = [1050, 215];
  kapakBG2(ctx, t, fire);
  const s = 21, px = 1545, py = 1080 + 14 * s;
  const pose = { torso: -.03, neck: -.12, head: -.3, shF: 2.7, elF: .28, shN: -.15, elN: .2, handN: 'fist', handF: 'fist', mouthOpen: 0, smile: -.4, scowl: .45, wind: .6 };
  const lk = { ...LK.promFree, eyeS: 1.3 };
  let J = null, M = null;
  figure(ctx, { x: px, y: py, s, dir: -1, sty: STY.red, lk, still: true, p: pose, onJoints: (j, m) => { J = j; M = m; }, alpha: 0 });
  const wr = jointPt(ctx, M, J.AF.wr), a = Math.atan2(fire[1] - wr[1], fire[0] - wr[0]);
  fennel(ctx, wr[0] - Math.cos(a) * 70, wr[1] - Math.sin(a) * 70, fire[0], fire[1] + 40, t, { w: 26, fire: false });
  // sırtta kil kenar ışığı (koyu zeminden ayrılsın), sonra figür
  ctx.save(); ctx.globalAlpha = .55; figure(ctx, { x: px + 7, y: py - 4, s, dir: -1, sty: { ...STY.red, fill: '#E08A52', cut: '#E08A52', line: '#E08A52' }, lk, still: true, p: pose, stripe: .5 }); ctx.restore();
  figure(ctx, { x: px, y: py, s, dir: -1, sty: STY.red, lk, still: true, stripe: .5, faceW: 1.5, p: pose });
  // ateş: büyük alev (≈ 135×255), beyaz çekirdek, geniş hâle
  glow(ctx, fire[0], fire[1] - 40, 460, 'rgba(255,190,100,.42)');
  flame(ctx, fire[0], fire[1] + 40, 5.1, t, { haloR: 60 });
  glow(ctx, fire[0], fire[1] - 20, 70, 'rgba(255,255,255,.95)');
  motes(ctx, t, 40, 9, 'rgba(255,200,120,.9)', [980, 40, 420, 300], 40, 2.4, .8);
  kapakText2(ctx, 'BİLE BİLE', 'ÇALDI', '#D6C29C', '#F2B453', { y1: 300, y2: 560, s1: 148, s2: 276, glow: 'rgba(255,150,60,.3)', blur: 26 });
};
// B: "ZEUS DA TUTSAK": zincirli Prometheus sağ üste bakar; zincir, kadrajın içinde, kelepçeli bir yumruğa (Zeus) gider;
// yumruk soğuk beyaz yıldırımı tutar: yıldırım ve kelepçe karenin en parlak noktası
SCENES.kapakB = (ctx, t) => {
  const F = [1665, 172];
  kapakBG2(ctx, t, [1480, 650], { r: 900, c0: 'rgba(201,112,63,.5)', c1: 'rgba(120,52,24,.3)', bc: 'rgba(150,66,30,.38)' });
  glow(ctx, F[0] + 40, F[1] + 40, 520, 'rgba(150,170,225,.30)');
  glow(ctx, 1640, 320, 375, 'rgba(201,112,63,.22)');
  // tek düz bulut silueti sağ kenarda: Zeus'un önkolu buradan yatay çıkar
  ctx.fillStyle = '#2A1A12'; ctx.strokeStyle = 'rgba(201,112,63,.55)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(1990, -20); ctx.lineTo(1990, 270);
  ctx.quadraticCurveTo(1900, 290, 1870, 230); ctx.quadraticCurveTo(1820, 200, 1850, 140); ctx.quadraticCurveTo(1815, 80, 1870, 40); ctx.quadraticCurveTo(1860, 0, 1900, -20); ctx.closePath(); ctx.fill(); ctx.stroke();
  // önkol (kil, siyah kontur) buluttan yumruğa
  ctx.save(); ctx.lineCap = 'round';
  ctx.strokeStyle = C.ink; ctx.lineWidth = 84; ctx.beginPath(); ctx.moveTo(1900, F[1] - 40); ctx.lineTo(F[0] + 40, F[1] - 4); ctx.stroke();
  ctx.strokeStyle = STY.red.fill; ctx.lineWidth = 72; ctx.stroke(); ctx.restore();
  // yıldırım (keraunos) ortasından kavranır: önce yıldırım, üstüne yumruk
  bolt(ctx, F[0], F[1], 2.1, .2, '#FFFFFF', 'rgba(225,232,255,.75)');
  ctx.save(); ctx.translate(F[0], F[1]);
  ctx.fillStyle = STY.red.fill; ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.beginPath(); ctx.ellipse(0, 4, 58, 52, 0, 0, TAU); ctx.fill(); ctx.stroke();
  ctx.lineWidth = 4; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.moveTo(-44, -22 + k * 22); ctx.quadraticCurveTo(-24, -18 + k * 22, -8, -20 + k * 22); ctx.stroke(); }
  // bilekte soğuk beyaz kelepçe (önkola dik bant) ve altından sarkan halka
  ctx.translate(84, -6); glow(ctx, 0, 0, 120, 'rgba(225,232,255,.6)');
  ctx.fillStyle = '#E6ECFF'; ctx.lineWidth = 5; ctx.beginPath(); ctx.rect(-17, -50, 34, 100); ctx.fill(); ctx.stroke();
  ctx.restore();
  const ring = [F[0] + 88, F[1] + 66];
  ctx.strokeStyle = '#F2F5FF'; ctx.lineWidth = 9; ctx.beginPath(); ctx.ellipse(ring[0], ring[1], 17, 23, .2, 0, TAU); ctx.stroke();
  const s = 17, px = 1580, py = 1080 + 13.5 * s;
  let J = null, M = null;
  figure(ctx, { x: px, y: py, s, dir: 1, sty: STY.red, lk: { ...LK.prom, eyeS: 1.3 }, still: true, stripe: .5, faceW: 1.5,
    p: { torso: -.06, neck: -.14, head: -.24, shN: 2.5, elN: .2, shF: -.25, elF: .5, handN: 'fist', handF: 'fist', mouthOpen: .15, scowl: .75 },
    hold: { N: CUFF, F: CUFF }, onJoints: (j, m) => { J = j; M = m; } });
  const wN = jointPt(ctx, M, J.AN.wr);
  ironChain(ctx, [wN[0], wN[1] - 30], [ring[0], ring[1] + 18], { L0: len(sub(ring, wN)) * 1.02, w: 16, link: 56, col: '#4A3426', hi: '#C9A888', bandCol: '#9C7B62' });
  kapakText2(ctx, 'ZEUS DA', 'TUTSAK', '#DCE3F6', '#D6C29C', { y1: 300, y2: 560, s1: 168, s2: 266, glow: 'rgba(170,190,240,.3)', blur: 24 });
};
