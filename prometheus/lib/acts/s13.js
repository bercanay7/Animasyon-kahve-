// XIII. ÇEVİRMENLERİN DİLEĞİ (M00–M03): çevirmenlerin masası, coşkuyla uçuşan sayfalar, modern sahnede Prometheus,
// izleyiciye uzanan ateş (kapak karesinin son kullanımı), bitiş ekranı (Sisifos ve abone öğesi)
'use strict';

// --- P289–P290: çevirmenlerin masası (portre yok): iki fincan, iki kalem, müsvedde, lamba; sayfalar çoğalıp uçuşur ---
function M_cup(ctx, x, y, s, t, seed) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.strokeStyle = PW.line; ctx.lineWidth = 2.4; ctx.fillStyle = PW.paperL;
  ctx.beginPath(); ctx.moveTo(-26, -40); ctx.lineTo(-20, 0); ctx.quadraticCurveTo(0, 8, 20, 0); ctx.lineTo(26, -40); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.ellipse(0, -40, 26, 6, 0, 0, TAU); ctx.stroke();
  ctx.beginPath(); ctx.ellipse(0, 4, 40, 8, 0, 0, TAU); ctx.stroke();
  // buhar: yükselen kıvrımlar
  ctx.lineWidth = 1.8;
  for (let k = 0; k < 2; k++) { const ph = (t * .4 + k * .5 + seed) % 1; ctx.globalAlpha = .5 * Math.sin(PI * ph); ctx.beginPath(); for (let u = 0; u <= 1; u += .1) { const yy = -50 - ph * 60 - u * 50, xx = Math.sin(u * 5 + t * 1.5 + k) * 8; u ? ctx.lineTo(xx, yy) : ctx.moveTo(xx, yy); } ctx.stroke(); }
  ctx.restore();
}
function M_pen(ctx, x, y, a, s = 1) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s); ctx.fillStyle = PW.ink;
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(8, -14); ctx.lineTo(16, -150); ctx.lineTo(4, -150); ctx.lineTo(-2, -14); ctx.closePath(); ctx.fill(); ctx.restore();
}
shot(PA('P289'), (ctx, st) => {
  const t = st.t, lt = st.lt, tC = A('M00@çevrilemeyeceğini'), tS = A('M00@sahnelenemeyeceğini'), tV = A('M00@çevirdikçe'), tD = A('M00@dilekleri');
  const c = { x: 960 + lt * 3, y: 540, z: 1.04 + lt * .004 };
  ctx.save(); cam(ctx, c, 1);
  paperBG(ctx, t, { seed: 61 });
  // masa çizgisi ve müsvedde
  inkPoly(ctx, [[160, 760], [1760, 760]], 1, { col: PW.line, w: 4 });
  ctx.fillStyle = PW.paperL; ctx.strokeStyle = PW.lineL; ctx.lineWidth = 2;
  ctx.save(); ctx.translate(960, 560); ctx.rotate(-.03); ctx.fillRect(-330, -240, 660, 420); ctx.strokeRect(-330, -240, 660, 420); ctx.restore();
  for (let i = 0; i < 5; i++) {
    scribble(ctx, 670, 380 + i * 52, 560, 1, 90 + i, { col: 'rgba(43,29,20,.7)' });
    strike(ctx, 660, 380 + i * 52, 1240, 378 + i * 52, ramp(t, tC + i * .12, tC + .35 + i * .12), { w: 4 });
  }
  // kenarda küçük sahne çizimi (skene ve figür): M00@sahnelenemeyeceğini'de silinir
  const er = ramp(t, tS, tS + .9);
  ctx.save(); ctx.globalAlpha = 1 - er; ctx.strokeStyle = PW.line; ctx.lineWidth = 2.5;
  ctx.strokeRect(1160, 610, 150, 70); ctx.beginPath(); ctx.ellipse(1235, 690, 100, 20, 0, 0, PI); ctx.stroke();
  figure(ctx, { x: 1235, y: 678 - 44.5 * 1.1, s: 1.1, dir: -1, sty: STY.lek, lk: LK.prom, seed: 2, still: true, p: {} });
  ctx.restore();
  if (er > 0 && er < 1) { ctx.fillStyle = 'rgba(246,239,224,.9)'; ctx.beginPath(); ctx.ellipse(1235 + Math.sin(t * 20) * 50, 650, 60, 40, 0, 0, TAU); ctx.fill(); }
  // iki kalem sırayla, kendiliğinden yazar (el yok); yeni satırlar müsveddenin altına
  const wr = ramp(t, tS + .8, tD, E.lin), line = Math.floor(wr * 6), u = (wr * 6) % 1;
  for (let i = 0; i < Math.min(line, 6); i++) scribble(ctx, 670, 640 + i * 18, 280, 1, 120 + i, { col: 'rgba(154,59,37,.8)', w: 1.6 });
  if (wr > 0 && wr < 1) { scribble(ctx, 670, 640 + line * 18, 280, u, 120 + line, { col: 'rgba(154,59,37,.8)', w: 1.6 }); M_pen(ctx, 670 + 280 * u, 640 + line * 18, line % 2 ? .35 : .2); }
  else M_pen(ctx, 880, 560, .3);
  M_pen(ctx, 1080, 520, -.25);
  M_cup(ctx, 430, 750, 1.2, t, 0); M_cup(ctx, 1520, 750, 1.2, t, .37);
  oilLamp(ctx, 300, 720, 2.6, t);
  // M00@çevirdikçe: sayfalar çoğalıp sevinçle uçuşur
  const fl = ramp(t, tV, tV + 4, E.lin);
  if (fl > 0) for (let k = 0; k < 14; k++) {
    const r = rng(k + 7), x0 = 700 + r() * 520, y0 = 560 + r() * 60, d = clamp(fl * 1.4 - k * .05);
    if (d <= 0) continue;
    const x = x0 + (r() - .5) * 1200 * d + Math.sin(t * 2 + k) * 30, y = y0 - 700 * d + Math.sin(t * 3 + k) * 20, a = (r() - .5) * 6 * d + Math.sin(t * 4 + k) * .3;
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.fillStyle = PW.paperL; ctx.strokeStyle = PW.lineL; ctx.lineWidth = 2; ctx.fillRect(-60, -80, 120, 160); ctx.strokeRect(-60, -80, 120, 160);
    for (let i = 0; i < 4; i++) { ctx.fillStyle = 'rgba(43,29,20,.35)'; ctx.fillRect(-44, -54 + i * 28, 88, 3); }
    ctx.restore();
  }
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => erhatTag(ctx, st.lt, 'ERHAT · EYÜBOĞLU', { d: 4.2 }) });

// --- P291: modern sahne: perde yerine bir ışık dairesi açılır; ışıkta kırmızı figür Prometheus; seyirci tek sıra siluet ---
shot(PA('P291'), (ctx, st) => {
  const t = st.t, lt = st.lt, op = E.io2(ramp(lt, .1, 1.6));
  ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
  const c = { x: 960, y: 520, z: 1 + lt * .01 };
  ctx.save(); cam(ctx, c, 1);
  // ışık dairesi: sahne tabanında elips ve yukarıdan inen huzme
  const g = ctx.createLinearGradient(0, 0, 0, 820); g.addColorStop(0, 'rgba(255,215,150,0)'); g.addColorStop(1, `rgba(255,205,140,${.28 * op})`);
  ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(900, -40); ctx.lineTo(1020, -40); ctx.lineTo(1260, 820); ctx.lineTo(660, 820); ctx.closePath(); ctx.fill();
  ctx.fillStyle = `rgba(255,215,160,${.35 * op})`; ctx.beginPath(); ctx.ellipse(960, 820, 300 * op + 1, 60 * op + 1, 0, 0, TAU); ctx.fill();
  ctx.save(); ctx.beginPath(); ctx.rect(560, -100, 800, 1000); ctx.clip(); ctx.globalAlpha = op;
  ctx.translate(960, 820); ctx.scale(.62, .62); ctx.translate(-1225, -868);
  promChained(ctx, t, { wind: .1 });
  ctx.restore();
  // seyirci: tek sıra baş ve omuz silueti (önde, kadrajın altında; altyazı bandının kenarında kalır)
  ctx.fillStyle = '#0A0605';
  for (let i = 0; i < 16; i++) { const x = 60 + i * 120 + (i % 2) * 20, y = 1000 + Math.sin(t * .8 + i) * 2; ctx.beginPath(); ctx.arc(x, y - 70, 34, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.ellipse(x, y + 10, 70, 60, 0, PI, TAU); ctx.fill(); }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'sir', dur: .6, end: true }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P292: kapak karesinin son kullanımı (el yok): Prometheus alevi kameraya uzatır; alev objektife yaklaşır ve kareyi altınla doldurur ---
shot(PA('P292'), (ctx, st) => {
  const t = st.t, lt = st.lt, tO = A('M02@olsan'), tA = A('M02@ateşi'), tY = A('M02@yorumlarda');
  const fire = [1060, 250];
  kapakBG(ctx, t, fire);
  const ext = E.io2(ramp(t, tO - .3, tO + .9));
  const s = 16, px = 1480 + ext * 40, py = 1080 + 8 * s;
  let J = null, M = null;
  const pose = { torso: -.02 - .05 * ext, neck: -.04, head: .02 + .05 * ext, shF: lerp(2.65, 1.75, ext), elF: lerp(.3, .1, ext), shN: -.15, elN: .2, handN: 'fist', handF: 'fist', mouthOpen: 0, smile: -.6, scowl: .3, wind: .6, breath: .6 * Math.sin(t * 1.5) };
  figure(ctx, { x: px, y: py, s, dir: -1, sty: STY.red, lk: LK.promFree, still: true, p: pose, onJoints: (j, m) => { J = j; M = m; }, alpha: 0 });
  const wr = jointPt(ctx, M, J.AF.wr), tip = [lerp(fire[0], 860, ext), lerp(fire[1], 380, ext)], a = Math.atan2(tip[1] - wr[1], tip[0] - wr[0]);
  // alev yaklaşınca (M02@ateşi) ölçek büyür ve kare altınla dolar; M02@yorumlarda'da küçülüp bitiş ekranının alevine iner
  const near = E.in2(ramp(t, tA - .2, tA + 1.0)), back = E.io2(ramp(t, tY - .2, tY + 1.2));
  const fs = lerp(2.6, 16, near * (1 - back)), fx = lerp(tip[0], 960, near), fy = lerp(tip[1], 420, near);
  if (near * (1 - back) < .5) fennel(ctx, wr[0] - Math.cos(a) * 60, wr[1] - Math.sin(a) * 60, tip[0], tip[1], t, { w: 22, fs: 2.6, haloR: 330, fire: false });
  figure(ctx, { x: px, y: py, s, dir: -1, sty: STY.red, lk: LK.promFree, still: true, stripe: .5, faceW: 1.5, p: pose });
  motes(ctx, t, 40, 9, 'rgba(255,200,120,.9)', [fx - 200, fy - 220, 400, 260], 40, 2.4, .8);
  ctx.save(); ctx.globalAlpha = .9 * near * (1 - back); ctx.fillStyle = '#F6B35A'; ctx.fillRect(0, 0, W, H); ctx.restore();
  const ex = lerp(fx, 1060, back), ey = lerp(fy, 470, back);
  flame(ctx, ex, ey + 30, lerp(fs, 1.6, back), t, { haloR: 200 });
  glow(ctx, ex, ey - 20, 260 + 400 * near * (1 - back), `rgba(255,210,140,${.5 + .3 * near})`);
}, { tr: { type: 'cut' }, post: { tex: .4, vig: .8, grain: .05 },
  over: (ctx, st) => { const a = ramp(st.lt, .1, .6) * (1 - ramp(st.t, A('M02@ateşi') - .1, A('M02@ateşi') + .4)); // yazı solda üç satır: meşale sapının ve alevin solunda kalır (soru işareti sapa binmez), y ≤ 700
    if (a > 0) { ctx.save(); ctx.globalAlpha = a; kapakText(ctx, 'PEKİ', 'SEN', '#FFC867', { x: 80, y1: 300, y2: 450, s1: 104, s2: 150, glow: 'rgba(255,150,60,.55)', blur: 30 });
      txt(ctx, 'OLSAN?', 80, 610, { font: '900 150px Cinzel', col: '#FFC867', align: 'left', ls: 3, stroke: 'rgba(14,9,7,.9)', sw: 18, shadow: 'rgba(255,150,60,.55)', blur: 30, force: true }); ctx.restore(); } } });

// --- P293: bitiş ekranı (son 20 sn): solda Sisifos çerçevesi (video öğesi x 150–870, y 180–585), sağda abone alanı (x 1250–1650, y 230–630); alev sürer ---
shot(PA('P293'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  clayBG(ctx, C.clayL, C.clayD);
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
  // video öğesinin çerçevesi ve içinde Sisifos döngüsü (YouTube öğesi bunun üstüne gelir; gelmezse sahne yine anlamlıdır)
  const x0 = 150, y0 = 180, x1 = 870, y1 = 585;
  ctx.fillStyle = C.clayD; ctx.fillRect(x0, y0, x1 - x0, y1 - y0);
  ctx.save(); ctx.beginPath(); ctx.rect(x0, y0, x1 - x0, y1 - y0); ctx.clip();
  const slope = x => lerp(560, 300, (x - x0) / (x1 - x0));
  ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x0, slope(x0)); ctx.lineTo(x1, slope(x1)); ctx.stroke();
  const cyc = (lt % 7) / 7, up = cyc < .8 ? cyc / .8 : 1, roll = cyc < .8 ? 0 : (cyc - .8) / .2;
  const sx = lerp(260, 700, up), br = 46, bx = sx + 70 + (roll > 0 ? -E.out2(roll) * 440 : 0), by = slope(bx) - br;
  boulder(ctx, bx, by, br, -bx / br, { light: -2.3 });
  if (roll === 0) walkScene(ctx, null, sx, 2.4, t, turnDir(clamp(up / .03), -1, 1), { noCam: true, ground: groundOf(slope), stride: 22, lean: .45, dist: sx * 1.4, sty: STY.black, lk: { beard: 'pointed', hair: 'long', garment: 'short', torn: true }, p: { shN: -1.4, elN: .5, shF: -1.2, elF: .6, handN: 'open', handF: 'open' } });
  // kaya yuvarlanınca Sisifos döner (birkaç karede) ve ardından yokuş aşağı yürür; döngü başında dipte olur (ışınlanma yok)
  else { const w = E.io2(clamp((roll - .15) / .85)), wx = lerp(700, 260, w);
    walkScene(ctx, null, wx, 2.4, t, turnDir(clamp(roll / .12)), { noCam: true, ground: groundOf(slope), stand: w > 0 ? 0 : 1, stride: 22, lean: .1, dist: (700 - wx) * 1.4, sty: STY.black, lk: { beard: 'pointed', hair: 'long', garment: 'short', torn: true }, p: { head: .25 } }); }
  ctx.restore();
  meander(ctx, x0, x1, y0 - 26, 26, C.ink); meander(ctx, x0, x1, y1, 26, C.ink);
  ctx.strokeStyle = C.ink; ctx.lineWidth = 5; ctx.strokeRect(x0, y0, x1 - x0, y1 - y0);
  // abone alanı: halka (YouTube öğesi bunun içine gelir)
  ctx.strokeStyle = C.ink; ctx.lineWidth = 8; ctx.beginPath(); ctx.arc(1450, 430, 200, 0, TAU); ctx.stroke();
  ctx.lineWidth = 2.5; ctx.beginPath(); ctx.arc(1450, 430, 216, 0, TAU); ctx.stroke();
  // Prometheus'un ateşi iki öğenin arasında sürer
  ctx.fillStyle = C.ink; ctx.fillRect(1052, 480, 16, 150); altar(ctx, 1060, 640, 1.1, C.ink, C.clay, 0, t);
  flame(ctx, 1060, 480, 1.6, t, { haloR: 140 });
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => {
    const a = ramp(st.lt, .3, 1.0);
    txt(ctx, 'SIRADAKİ · SİSİFOS', 510, 128, { font: '700 46px Cinzel', col: C.ink, ls: 5, a });
    txt(ctx, 'ABONE OL', 1450, 690, { font: '700 46px Cinzel', col: C.ink, ls: 6, a });
  } });
