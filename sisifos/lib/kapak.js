// YouTube kapak görseli: film.html?scene=kapak (tools ile 1280×720'ye küçültülür)
// Kurul notu: kayayı iten klişe yerine filmin özgün imgesi; başlığa eklenen 2 sözcük: "ÖLÜMÜ ZİNCİRLEDİ"
'use strict';
function kapakDraw(ctx, L1, L2, f1 = 168, f2 = 132) {
  // sol yarı kil zemin (siyah figür Sisifos), sağ yarı kara sır (kırmızı figür Ölüm): vazo resminin iki tekniği karşı karşıya
  clayBG(ctx, '#D98A55', '#9A4826', { x: 560, y: 520, r: 760, c: 'rgba(255,214,150,.45)' });
  ctx.save(); ctx.beginPath(); ctx.moveTo(1090, 0); ctx.lineTo(W, 0); ctx.lineTo(W, H); ctx.lineTo(960, H); ctx.closePath(); ctx.clip();
  ctx.fillStyle = '#0D0605'; ctx.fillRect(0, 0, W, H); glow(ctx, 1450, 520, 700, 'rgba(190,80,35,.45)');
  const gy = 1010;
  column(ctx, 1640, 60, gy, 90, '#2A140C', '#6A3020');
  // zincirli Thanatos: diz çökmüş, kanatlar açık, bileklerinde altın kelepçe
  let hN = null, hF = null;
  figure(ctx, { x: 1480, y: gy - 25.5 * 11, s: 11, dir: -1, lk: LK.thanatos, sty: STY.red, cutCol: '#1E0E09', margin: 120,
    p: { torso: .35, neck: .3, head: .35, hipN: 1.35, knN: 1.45, hipF: -.05, knF: 1.62, ankF: -.5, wingSpread: .85, wingF: .4, shN: .55, elN: 1.0, shF: .35, elF: 1.2, handN: 'fist', handF: 'fist', brow: 1.2, mouthOpen: .3 },
    onJoints: (J, M) => { const tr = ctx.getTransform().inverse(); const f = q => { const r = tr.transformPoint(M.transformPoint(new DOMPoint(q[0], q[1]))); return [r.x, r.y]; }; hN = f(J.AN.wr); hF = f(J.AF.wr); } });
  if (hN && hF) {
    chain(ctx, [hN, [1600, hN[1] - 120], [1640, 300]], 30, '#E9BC7E', '#5A2A16', 9);
    chain(ctx, [hF, [lerp(hF[0], 1640, .5), gy - 40], [1640, gy - 6]], 30, '#E9BC7E', '#5A2A16', 9);
    shackle(ctx, hN[0], hN[1], 30, .2, '#F0C886'); shackle(ctx, hF[0], hF[1], 30, .2, '#F0C886');
    // kelepçeleri birleştiren altın asma kilit
    const lk = [lerp(hN[0], hF[0], .5) - 10, Math.max(hN[1], hF[1]) + 58];
    ctx.save(); ctx.translate(lk[0], lk[1]); ctx.strokeStyle = '#F2C66E'; ctx.lineWidth = 12; ctx.beginPath(); ctx.arc(0, -34, 26, PI, TAU); ctx.stroke();
    ctx.fillStyle = '#F2C66E'; ctx.strokeStyle = '#5A2A16'; ctx.lineWidth = 5; ctx.beginPath(); ctx.roundRect(-40, -36, 80, 66, 10); ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#5A2A16'; ctx.beginPath(); ctx.arc(0, -12, 8, 0, TAU); ctx.fill(); ctx.fillRect(-3, -10, 6, 22); ctx.restore();
  }
  ctx.restore();
  // ayırma çizgisi: altın şerit
  ctx.strokeStyle = '#E7B85E'; ctx.lineWidth = 10; ctx.beginPath(); ctx.moveTo(1090, 0); ctx.lineTo(960, H); ctx.stroke();
  // Sisifos: tacıyla, sinsice gülümser; elinde anahtar
  let kh = null;
  figure(ctx, { x: 640, y: 1340, s: 17, lk: LK.sisKing, margin: 80,
    p: { torso: .05, neck: -.05, head: -.12, shN: 1.25, elN: 1.75, handN: 'fist', shF: .2, elF: .5, smile: 1.6, brow: .8 },
    onJoints: (J, M) => { const r = ctx.getTransform().inverse().transformPoint(M.transformPoint(new DOMPoint(J.AN.wr[0], J.AN.wr[1]))); kh = [r.x, r.y]; } });
  // altın anahtar (büyük, kenar ışıklı): küçük boyutta da anahtar olarak okunur
  if (kh) { ctx.save(); ctx.translate(kh[0] + 30, kh[1] + 20); ctx.rotate(-.5);
    glow(ctx, 0, -60, 190, 'rgba(255,214,120,.55)');
    ctx.fillStyle = '#F2C66E'; ctx.strokeStyle = '#3A1A0C'; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.arc(0, -150, 46, 0, TAU); ctx.moveTo(18, -150); ctx.arc(0, -150, 18, 0, TAU, true); ctx.fill('evenodd'); ctx.stroke();
    ctx.beginPath(); ctx.rect(-11, -106, 22, 190); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.rect(11, 40, 42, 18); ctx.rect(11, 70, 30, 16); ctx.fill(); ctx.stroke();
    ctx.restore(); }
  // başlık: iki satır, kalın
  const sh = { shadow: 'rgba(0,0,0,.75)', blur: 22 };
  txt(ctx, L1, 60, 190, { font: `900 ${f1}px Cinzel`, col: '#FFF1D2', align: 'left', ls: 6, ...sh });
  txt(ctx, L2, 60, 345, { font: `900 ${f2}px Cinzel`, col: '#FFD27A', align: 'left', ls: 2, ...sh });
  applyVignette(ctx, .5);
}
SCENES.kapak = ctx => kapakDraw(ctx, 'ÖLÜMÜ', 'ZİNCİRLEDİ', 168, 118);
SCENES.kapak_en = ctx => kapakDraw(ctx, 'HE CHAINED', 'DEATH', 112, 176);
// B kapağı (YouTube "Test ve Karşılaştır" için): yüz yakın planı — kayaya omuz vermiş, gülümseyen Sisifos; "NEDEN GÜLÜYOR?"
SCENES.kapak_b = ctx => {
  const xr = 330, po = { dist: xr, smile: 2.4, blink: .45, strain: .2, look: -.35, reach: 19, T: 1.12, hA: -.55, hB: -.62 };
  const P = pushScene(ctx, null, xr, 150, 4.0, 5, { ...po, dry: true });
  const z = 7.6, c = { x: P.head[0] + (W / 2 - 1180) / z, y: P.head[1] + (H / 2 - 600) / z, z };
  const zk = 1 + (z - 1) * .15, cxk = W / 2 + (c.x - W / 2) * .15, cyk = H / 2 + (c.y - H / 2) * .15;
  tartarosBG(ctx, 5, c, { warm: 1, diskX: cxk + (1500 - W / 2) / zk, diskY: cyk + (300 - H / 2) / zk, diskR: 360 });
  tartarosHill(ctx, c, { groove: .9, warm: 1 });
  ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, 1180, 600, 520, 'rgba(255,190,110,.22)'); ctx.restore(); // yüzde sıcak ışık
  pushScene(ctx, c, xr, 150, 4.0, 5, po);
  motes(ctx, 5, 40, 33, 'rgba(255,225,160,.8)', [0, 0, W, H], 12, 2.2, .7);
  const g = ctx.createLinearGradient(0, 0, W * .62, 0);
  g.addColorStop(0, 'rgba(14,6,4,.88)'); g.addColorStop(.7, 'rgba(14,6,4,.55)'); g.addColorStop(1, 'rgba(14,6,4,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W * .62, H);
  const sh = { shadow: 'rgba(0,0,0,.75)', blur: 22 };
  txt(ctx, 'NEDEN', 70, 300, { font: '900 190px Cinzel', col: '#FFF1D2', align: 'left', ls: 8, ...sh });
  txt(ctx, 'GÜLÜYOR?', 70, 500, { font: '900 150px Cinzel', col: '#FFD27A', align: 'left', ls: 4, ...sh });
  applyVignette(ctx, .55);
};
