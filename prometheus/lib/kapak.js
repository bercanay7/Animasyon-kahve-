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
// A: "BİLE BİLE ÇALDI": ateşi kaldırmış Prometheus, baş büyük; ateş karenin en parlak noktası
SCENES.kapakA = (ctx, t) => {
  const fire = [1060, 250];
  kapakBG(ctx, t, fire);
  const s = 16, px = 1480, py = 1080 + 8 * s;
  // ateşi uzak kol kaldırır: kol başın arkasından geçer, yüz açık kalır; rezene figürün arkasında çizilir
  let J = null, M = null;
  const pose = { torso: -.02, neck: -.04, head: .02, shF: 2.65, elF: .3, shN: -.15, elN: .2, handN: 'fist', handF: 'fist', mouthOpen: 0, smile: -.6, scowl: .6, wind: .6 };
  figure(ctx, { x: px, y: py, s, dir: -1, sty: STY.red, lk: LK.promFree, still: true, p: pose, onJoints: (j, m) => { J = j; M = m; }, alpha: 0 });
  const wr = jointPt(ctx, M, J.AF.wr), a = Math.atan2(fire[1] - wr[1], fire[0] - wr[0]);
  fennel(ctx, wr[0] - Math.cos(a) * 60, wr[1] - Math.sin(a) * 60, fire[0], fire[1], t, { w: 22, fs: 2.6, haloR: 330 });
  figure(ctx, { x: px, y: py, s, dir: -1, sty: STY.red, lk: LK.promFree, still: true, stripe: .5, faceW: 1.5, p: pose });
  motes(ctx, t, 40, 9, 'rgba(255,200,120,.9)', [880, 60, 360, 260], 40, 2.4, .8);
  kapakText(ctx, 'BİLE BİLE', 'ÇALDI', '#FFC867', { y1: 330, y2: 560, glow: 'rgba(255,150,60,.55)', blur: 34 });
};
// B: "ASIL TUTSAK ZEUS": zincirli Prometheus göğe meydan okur; zincir sağ üstte karanlıktan uzanan soğuk beyaz kelepçeli bileğe gider
SCENES.kapakB = (ctx, t) => {
  const cuff = [1760, 120];
  kapakBG(ctx, t, [1400, 300], false);
  glow(ctx, 1150, 1000, 900, 'rgba(150,62,28,.45)');
  // bulut bankası ve karanlıktan uzanan bilek (yüz ve gövde görünmez)
  for (let i = 0; i < 5; i++) cloud(ctx, 1380 + i * 140, 60 + (i % 2) * 50, 1.6, '#1A100B', 'rgba(201,112,63,.35)', i + 2);
  ctx.save(); ctx.translate(cuff[0], cuff[1]); ctx.rotate(.9);
  ctx.fillStyle = PC.clayR; ctx.strokeStyle = C.ink; ctx.lineWidth = 5; ctx.beginPath(); ctx.rect(-40, -260, 80, 260); ctx.fill(); ctx.stroke();
  glow(ctx, 0, 0, 220, 'rgba(225,232,255,.55)');
  ctx.fillStyle = '#E6ECFF'; ctx.beginPath(); ctx.rect(-52, -40, 104, 56); ctx.fill(); ctx.lineWidth = 5; ctx.stroke();
  ctx.restore();
  const s = 15, px = 1250, py = 1080 + 7 * s;
  // sağa, kelepçeli bileğe (Zeus'a) bakan, göğe meydan okuyan Prometheus; yakın kol zincirle yukarı çekili
  let J = null, M = null;
  figure(ctx, { x: px, y: py, s, dir: 1, sty: STY.red, lk: LK.prom, still: true, stripe: .5, faceW: 1.5,
    p: { torso: -.06, neck: -.14, head: -.22, shN: 2.55, elN: .2, shF: .9, elF: .6, handN: 'fist', handF: 'fist', mouthOpen: .2, scowl: .75 },
    hold: { N: CUFF, F: CUFF }, onJoints: (j, m) => { J = j; M = m; } });
  const wN = jointPt(ctx, M, J.AN.wr);
  ironChain(ctx, [wN[0], wN[1] - 30], [cuff[0] - 60, cuff[1] + 60], { L0: len(sub(cuff, wN)) * 1.02, w: 16, link: 56 });
  kapakText(ctx, 'ASIL TUTSAK', 'ZEUS', '#E6ECFF', { y1: 330, y2: 560, s1: 130, glow: 'rgba(200,215,255,.5)', blur: 30 });
};
