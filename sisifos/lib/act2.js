// II. KARTAL VE PINAR
'use strict';
// Akrokorint zirvesi zemini
const acroY = x => 700 + Math.pow(Math.abs(x - 900) / 900, 2.2) * 420;
const ACRO = groundOf(acroY);

// C1 — zirvede gökyüzünü izleyen Sisifos
shot(S('C01') - .35, (ctx, st) => {
  const t = st.t, lt = st.lt;
  daySky(ctx, .3);
  const c = { x: 960, y: lerp(560, 470, E.io2(st.p)), z: lerp(1.05, .95, st.p) };
  ctx.save(); cam(ctx, c, .3); for (let i = 0; i < 5; i++) cloud(ctx, ((i * 520 + t * 25) % 2600) - 300, 150 + (i % 2) * 120, 1.1, 'rgba(255,230,205,.4)', null, i); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-600, 1600); for (let x = -600; x <= 2600; x += 10) ctx.lineTo(x, acroY(x)); ctx.lineTo(2600, 1600); ctx.fill();
  temple(ctx, 1350, acroY(1350) + 4, .9, 6, C.ink, C.clay);
  const look = ramp(lt, .6, 2.2);
  walkScene(ctx, null, 760, 5.2, t, 1, { noCam: true, ground: ACRO, dist: 0, lk: LK.sisKing, lean: -.08,
    neck: -.2 * look, head: -.45 * look, p: { shN: lerp(.2, 2.1, look), elN: lerp(.3, 1.75, look), shF: .1, elF: .4, handN: 'flat', brow: .3, hipN: .08, hipF: -.08 } }); // el alnın üstünde, profil açıkta
  ctx.restore();
  chapterCard(ctx, 'BÖLÜM II', 'KARTAL VE PINAR', lt - .1, 3.4, { x: 1430, y: 270 }); // figürün başının üstünde değil
}, { tr: { type: 'black', dur: .9 }, post: { tex: .9, vig: .8 } });

// C2 — kartal ve Egina gökyüzünde
function eagleWithGirl(ctx, x, y, s, t, o = {}) {
  eagle(ctx, x, y, s, 1, t * 1.1, { tilt: o.tilt || -.05 });
  // pençede Egina (beyaz ten), rüzgârla savrulan elbise — kartaldan sonra çizilir ki kanat örtmesin
  const tx = x + 2 * s, ty = y + 30 * s;
  const gs = s * .78;
  figure(ctx, { x: tx - 4 * gs, y: ty + 33 * gs, s: gs, lk: LK.aegina, p: { torso: .1 + Math.sin(t * 2) * .05, neck: .25, head: .35, shN: 3.05, elN: .15, shF: 1.25 + Math.sin(t * 3) * .25, elF: .6,
    hipN: .15 + Math.sin(t * 2.4) * .12, knN: .3, hipF: -.15 + Math.sin(t * 2.4 + 1) * .12, knF: .5, ankN: .2, ankF: .3, handN: 'open', handF: 'open', mouthOpen: .6 }, margin: 50 });
  // pençeler omuzları kavrar
  ctx.save(); ctx.strokeStyle = C.ink; ctx.lineWidth = 2.2 * s; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x, y + 8 * s); ctx.lineTo(tx - 3 * s, ty - 4 * s); ctx.moveTo(x + 8 * s, y + 8 * s); ctx.lineTo(tx + 4 * s, ty - 4 * s); ctx.stroke();
  ctx.lineWidth = 1.2 * s;
  for (const fx of [-3, 4]) { ctx.beginPath(); ctx.arc(tx + fx * s, ty - 1 * s, 3.4 * s, PI * 1.1, PI * 2.1); ctx.stroke(); }
  ctx.restore();
}
shot(S('C02') - .25, (ctx, st) => {
  const t = st.t, lt = st.lt;
  daySky(ctx, .3);
  const c = { x: lerp(820, 1100, st.p), y: 540, z: 1 };
  ctx.save(); cam(ctx, c, .3); for (let i = 0; i < 6; i++) cloud(ctx, ((i * 480 + t * 40) % 2800) - 300, 220 + (i % 3) * 140, 1.2, 'rgba(255,230,205,.4)', null, i + 4); ctx.restore();
  // rüzgâr çizgileri
  ctx.save(); ctx.strokeStyle = 'rgba(255,240,220,.35)'; ctx.lineWidth = 3;
  for (let i = 0; i < 9; i++) { const y = 200 + i * 90, x = ((i * 377 + t * 900) % 2600) - 400; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 180, y); ctx.stroke(); }
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-600, 1600); for (let x = -600; x <= 2600; x += 10) ctx.lineTo(x, acroY(x - 900) + 260); ctx.lineTo(2600, 1600); ctx.fill();
  walkScene(ctx, null, 120, 3.0, t, 1, { noCam: true, ground: groundOf(x => acroY(x - 900) + 260), dist: 0, lk: LK.sisKing, neck: -.3, head: -.55, p: { shN: 2.6, elN: 1.9, handN: 'flat' } });
  const ex = lerp(-200, 2100, E.lin(st.p));
  eagleWithGirl(ctx, ex, 330 + Math.sin(t * 2.2) * 30, 4.2, t);
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .9, vig: .8 } });

// C3 — şimşek: kartal = Zeus; Egina
shot(S('C03') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tz = Wd('C03', 'zeus'), te = Wd('C03', 'egina');
  clayBG(ctx, '#B86A44', '#6E3019');
  const flash = Math.max(0, 1 - Math.abs(t - (tz - .25)) * 4);
  ctx.save(); for (let i = 0; i < 6; i++) cloud(ctx, i * 360 - 80, 160 + (i % 2) * 100, 1.5, 'rgba(60,25,15,.55)', 'rgba(220,150,100,.3)', i + 11); ctx.restore();
  const rev = ramp(t, tz - .3, tz + .3);
  // kartal silueti → Zeus
  ctx.save(); ctx.globalAlpha = 1 - rev; eagleWithGirl(ctx, 980, 380, 4.2, t); ctx.restore();
  if (rev > 0) {
    ctx.save(); ctx.globalAlpha = rev;
    // Egina kaçar (sağa), Zeus bileğini yakalar
    let wr = null;
    const run = Math.sin(t * 5);
    figure(ctx, { x: 1180, y: 570, s: 5.0, dir: 1, lk: LK.aegina,
      p: { torso: .32, neck: -.1, head: -.15, shN: 2.5 + run * .1, elN: .5, handN: 'open', shF: -1.15, elF: -.05, handF: 'open',
        hipN: .55, knN: .4, hipF: -.32, knF: .55, ankF: -.2, mouthOpen: .5 }, // adım elbisenin içinde kalır
      onJoints: (J, M) => { const q = M.transformPoint(new DOMPoint(...J.AF.wr)); const r = ctx.getTransform().inverse().transformPoint(q); wr = [r.x, r.y]; } });
    figure(ctx, { x: 820, y: 530, s: 6.0, lk: LK.zeus, hold: { F: HOLD.bolt() },
      p: { torso: .18, neck: .05, head: .05, hipN: .75, knN: .85, hipF: -.5, knF: .35, ankF: -.4, shF: 2.05, elF: 1.25, handN: 'open', handF: 'fist', brow: -.4 },
      ik: wr ? { hN: [wr[0] - 6, wr[1] + 4] } : {} });
    ctx.restore();
  }
  if (flash > 0) { lightning(ctx, 300, -50, 700, 600, 5, 7); ctx.save(); ctx.fillStyle = `rgba(255,245,220,${flash * .75})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  nameTag(ctx, 'ZEUS', 'Tanrıların kralı', 140, 760, t - tz, 3.4, { col: C.white });
  nameTag(ctx, 'EGİNA', "Irmak tanrısı Asopos'un kızı", 1780, 760, t - Wd('C03', 'ise') + .1, 3.4, { col: C.white, align: 'right' });
}, { tr: { type: 'cut' }, post: { tex: .8, vig: .9 } });

// C4 — Asopos kızını arar
function asoposWaves(G, J) {
  // gövdesinde akan su kazımaları
  for (let k = 0; k < 6; k++) G.cut(c => { const y0 = -26 + k * 9; c.moveTo(-8, y0); for (let x = -8; x <= 8; x += 2) c.lineTo(x, y0 + Math.sin(x * .8 + k + performance.now() * 0) * 1.2); }, .35);
}
shot(S('C04') - .25, (ctx, st) => {
  const t = st.t, lt = st.lt, tk = Wd('C04', 'korint');
  daySky(ctx, .2);
  const pan = lt * 160;
  // uzak dağlar (paralaks)
  ctx.save(); ctx.translate(-pan * .2, 0); ctx.fillStyle = '#8E4426';
  ctx.beginPath(); ctx.moveTo(-100, 900); for (let x = -100; x <= 4000; x += 30) ctx.lineTo(x, 520 + fbm1(x * .003, 21) * 160); ctx.lineTo(4000, 1200); ctx.lineTo(-100, 1200); ctx.fill(); ctx.restore();
  ctx.save(); ctx.translate(-pan * .5, 0); ctx.fillStyle = '#5E2A16';
  ctx.beginPath(); ctx.moveTo(-100, 900); for (let x = -100; x <= 5000; x += 30) ctx.lineTo(x, 660 + fbm1(x * .004, 23) * 120); ctx.lineTo(5000, 1200); ctx.lineTo(-100, 1200); ctx.fill(); ctx.restore();
  // şehir kapısı belirir
  const ca = ramp(t, tk - 1.2, tk + .2, E.out3);
  if (ca > 0) city(ctx, lerp(2300, 1500, ca), 860, 1.1, C.ink, C.clay, 7);
  // ırmak
  ctx.fillStyle = C.ink; ctx.fillRect(0, 860, W, 220);
  sea(ctx, -200, 2200, 900, 3, 34, t * 1.6, '#24150F', C.ink);
  const gy = 860;
  walkScene(ctx, null, 760, 5.6, t, 1, { noCam: true, ground: FLAT(gy), dist: lt * 90, stride: 34, lk: LK.asopos, lean: .06, neck: -.05, head: Math.sin(lt * 1.3) * .15,
    p: { shN: 2.55, elN: 1.95, handN: 'flat', shF: Math.sin(lt * 2) * .3 - .1, elF: .5, brow: 1, mouthOpen: 0 }, extra: asoposWaves, hold: { F: HOLD.scepter(80) } });
  // saç/sakaldan damlayan su
  for (let i = 0; i < 8; i++) { const ph = (t * .9 + hash(i)) % 1; ctx.fillStyle = 'rgba(244,238,221,.8)'; ctx.beginPath(); ctx.arc(700 + hash(i * 2) * 60, 360 + ph * 300, 4, 0, TAU); ctx.fill(); }
  nameTag(ctx, 'ASOPOS', 'Irmak tanrısı', 140, 160, t - S('C04'), 3.4, { col: C.ink, line: C.ink });
}, { tr: { type: 'fade', dur: .6 }, post: { tex: .9, vig: .8 } });

// C5 — pazarlık
shot(S('C05') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tp = Wd('C05', 'pınar');
  daySky(ctx);
  const gy = 880;
  city(ctx, 960, gy, 1.6, '#7A3A1E', '#9C4A27', 9);
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  const c = { x: 960, y: 540, z: lerp(1, 1.08, st.p) };
  ctx.save(); cam(ctx, c, 1);
  figure(ctx, { x: 1240, y: gy - 47 * 6.4, s: 6.4, dir: -1, lk: LK.asopos, extra: asoposWaves, hold: { F: HOLD.scepter(80) },
    p: { torso: .12, neck: .1, head: .15, shN: .4, elN: 1.2, shF: .1, elF: .3, hipN: .08, hipF: -.06, brow: -.6, blink: (lt > 2 && lt < 2.12) ? 1 : 0 } });
  const fing = ramp(t, tp - 1.2, tp - .7, E.outBack);
  figure(ctx, { x: 640, y: gy - 47 * 5.2, s: 5.2, lk: LK.sisKing,
    p: { torso: -.04, head: -.12, shN: lerp(.3, 1.9, fing), elN: lerp(.3, 1.2, fing), handN: fing > .5 ? 'point' : 'open', shF: .5, elF: 2.0, handF: 'fist', smile: 1.2, hipN: .1, hipF: -.08, brow: .5 } });
  ctx.restore();
}, { tr: { type: 'fade', dur: .4 }, post: { tex: .9, vig: .8 } });

// C6 — su fışkırır, sır fısıldanır
shot(S('C06') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tf = Wd('C06', 'fışkırttı') - .25, ts = Wd('C06', 'sisifos');
  daySky(ctx);
  const gy = 880;
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  // kaya öbeği
  ctx.fillStyle = C.ink; ctx.beginPath(); spline(ctx, [[780, gy + 4], [800, gy - 90], [880, gy - 150], [980, gy - 120], [1040, gy - 40], [1060, gy + 4]]); ctx.fill();
  // asa kalkar, kayaya iner (temas karesi + parlama), su vuruş noktasından fışkırır
  // vuruştan sonra asa kalkar, Asopos geri çekilir (Sisifos'la siluetleri karışmasın)
  const rel = ramp(t, tf + .5, tf + 1.1, E.io2), lift = ramp(t, tf - 1.1, tf - .45, E.io2) * (1 - rel), strike = ramp(t, tf - .14, tf, E.in3) * (1 - rel);
  const ax = lerp(1110, 1360, ramp(t, tf + .9, ts - .3, E.io2)), dxA = ax - 1110;
  const hand = [lerp(lerp(990, 968, lift), 948, strike) + dxA, lerp(lerp(500, 360, lift), 470, strike)];
  // Asopos geri geri adımlarla çekilir (ayaklar zeminde kilitli; kayma yok)
  walkScene(ctx, null, ax, 6.0, t, -1, { noCam: true, ground: FLAT(gy), dist: -ax, stride: 30, lk: LK.asopos, extra: asoposWaves,
    p: { torso: .12 + strike * .12, neck: .1, head: .25, shF: .2, elF: .4, handN: 'fist', brow: -.3 }, ik: { hN: hand } });
  // asa (dünya koordinatında): ucu vuruşta kayanın tepesine değer
  { const tip = [hand[0] - 6, hand[1] + 258], dx = hand[0] - tip[0], dy = hand[1] - tip[1], L = Math.hypot(dx, dy);
    const top = [tip[0] + dx / L * 520, tip[1] + dy / L * 520];
    ctx.save(); ctx.strokeStyle = C.ink; ctx.lineWidth = 12; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(tip[0], tip[1]); ctx.lineTo(top[0], top[1]); ctx.stroke();
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(top[0], top[1], 15, 0, TAU); ctx.fill(); ctx.fillStyle = C.red; ctx.beginPath(); ctx.arc(top[0], top[1], 7, 0, TAU); ctx.fill(); ctx.restore(); }
  const fl = clamp(1 - Math.abs(t - tf - .04) * 7) * (t > tf - .02 ? 1 : 0);
  if (fl > 0) { sparkle(ctx, 932, gy - 146, 70 * fl, fl); ctx.save(); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgba(255,240,210,${fl * .3})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  spring(ctx, 930, gy - 140, t, tf, '#F4EEDD', .7);
  dustBurst(ctx, t, tf, 930, gy - 120, 14, 'rgba(70,40,25,.4)', 120, 4);
  // Sisifos yaklaşır, fısıldar ve yukarıyı gösterir
  const lean = ramp(t, ts - .2, ts + .5, E.io2);
  const sx = lerp(220, 470, ramp(t, tf + .6, ts, E.io2)); // pınarın solunda durur (fıskiyelerin içine girmez)
  if (t < ts - .1) walkScene(ctx, null, sx, 5.0, t, 1, { noCam: true, ground: FLAT(gy), dist: sx, lk: LK.sisKing, p: { smile: .6 } });
  else figure(ctx, { x: 470, y: gy - 47 * 5.0, s: 5.0, lk: LK.sisKing, p: { torso: .25 * lean, neck: .1, head: -.1, shN: lerp(.2, 2.9, lean), elN: .2, handN: 'point', shF: .4, elF: 1.6, smile: 1, hipN: .1, hipF: -.1 } });
}, { tr: { type: 'cut' }, post: { tex: .9, vig: .8 } });

// C7 — çeşme evi, mutlu şehir; sonra gök kararır
shot(S('C07') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, ta = Wd('C07', 'ama');
  const dk = ramp(t, ta - .2, ta + 2.2);
  daySky(ctx);
  ctx.save(); for (let i = 0; i < 7; i++) cloud(ctx, i * 300 - 60 + Math.sin(t * .3 + i) * 20, lerp(-200, 120, dk) + (i % 2) * 70, 1.4, mixCol('rgba(120,60,35,.3)', 'rgba(25,12,8,.95)', dk), null, i + 31); ctx.restore();
  const gy = 900;
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  fountainHouse(ctx, 960, gy, 1.5, t);
  figure(ctx, { x: 960 - 70, y: gy - 47 * 4.4, s: 4.4, lk: LK.woman, hold: { N: HOLD.hydria() },
    p: { torso: .3, neck: .1, head: .2, shN: 1.2, elN: .5, shF: .8, elF: 1.0, hipN: .1, hipF: -.1 } });
  const wx = lerp(1250, 1600, ramp(lt, .2, 4.2, E.lin));
  // başında testi: tabanı başına oturur, elleri testiyi tutar
  walkScene(ctx, null, wx, 4.4, t, 1, { noCam: true, ground: FLAT(gy), dist: wx, lk: LK.woman, p: { handN: 'flat', handF: 'flat', head: -.05, smile: .5 },
    ik: { hN: [wx + 30, gy - 101 * 4.4], hF: [wx - 22, gy - 100 * 4.4] } });
  ctx.save(); ctx.translate(wx + 4, gy - 96 * 4.4); amphora(ctx, 0, 0, 1.1, C.ink, C.red); ctx.restore();
  if (dk > 0) { ctx.fillStyle = `rgba(15,6,4,${dk * .45})`; ctx.fillRect(0, 0, W, H); }
}, { tr: { type: 'fade', dur: .5 }, post: { tex: .9, vig: .85 } });

// C8 — Zeus unutmaz: fırtınada dev yüz
shot(S('C08') - .25, (ctx, st) => {
  const t = st.t, lt = st.lt;
  clayBG(ctx, '#7A3A22', '#2E140C');
  for (let i = 0; i < 8; i++) cloud(ctx, i * 280 - 100 + Math.sin(t * .5 + i) * 30, 120 + (i % 3) * 300, 1.8, 'rgba(10,4,3,.85)', 'rgba(140,70,40,.4)', i + 51);
  const nar = ramp(t, Wd('C08', 'unutmazdı') - .2, Wd('C08', 'unutmazdı') + .6);
  ctx.save(); ctx.globalAlpha = ramp(lt, 0, .8);
  figure(ctx, { x: 820, y: 1480, s: 26, lk: LK.zeus, sty: { ...STY.black, fill: '#120806', cut: '#A0522D' }, cutCol: '#A0522D',
    p: { torso: .02, neck: 0, head: .05, brow: -1.2 * nar, blink: nar * .55, shN: 0, shF: 0 }, margin: 30 });
  ctx.restore();
  const tz = Wd('C08', 'unutmazdı', 0, true) + .1;
  for (const [k, x] of [[0, 1500], [1, 1250]]) { const tt = tz + k * .35; if (t > tt && t < tt + .25) { lightning(ctx, x, -40, x - 200, 900, 7 + k, 8); ctx.fillStyle = 'rgba(255,240,210,.35)'; ctx.fillRect(0, 0, W, H); } }
}, { tr: { type: 'cut' }, post: { tex: .6, vig: 1, grain: .07 } });
