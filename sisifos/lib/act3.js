// III. ÖLÜMÜ ZİNCİRLEYEN ADAM
'use strict';
// Thanatos her sahnede kırmızı figür: siyah figürler arasında tek "kırmızı" figür olan Ölüm
const THS = { sty: STY.red, cutCol: '#1E0E09' };
// elde sarkan altın zincir (dünya koordinatında)
function handChain(ctx, p, len, t, k = 0, size = 16) {
  const sw = Math.sin(t * 2.1 + k) * len * .08;
  chain(ctx, [p, [p[0] + sw * .6, p[1] + len * .5], [p[0] + sw, p[1] + len]], size, '#E1B07A', '#5A2A16', size * .32);
}
const wrW = (ctx, M, J, side) => jointPt(ctx, M, (side === 'N' ? J.AN : J.AF).wr);
const chainHold = (len = 30) => G => { for (let i = 0; i < len / 3; i++) G.part(c => { c.ellipse(Math.sin(i * .9) * 1.2, 4 + i * 3, i % 2 ? .7 : 1.6, 1.6, 0, 0, TAU); }, { cutW: .25 }); };

// D1 — Zeus Thanatos'u gönderir
shot(S('D01') - .25, (ctx, st) => {
  const t = st.t, lt = st.lt, tt = Wd('D01', 'tanatos');
  const dark = ramp(lt, .5, 4);
  clayBG(ctx, mixCol('#C9733F', '#4A2216', dark), mixCol('#8E4022', '#1A0B07', dark));
  const gy = 880;
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  throne(ctx, 300, gy, 6, 1, C.ink, C.clay, { high: true });
  figure(ctx, { x: 400, y: gy - 27 * 6, s: 6, lk: LK.zeus, hold: { F: HOLD.scepter(80) },
    p: { ...oturan(), torso: .05, head: .05, shN: lerp(.4, 1.75, ramp(lt, .3, 1.1, E.outBack)), elN: .15, handN: 'point', shF: .3, elF: 1.2, brow: -1 } });
  // duman sütunu ve Thanatos'un yükselişi
  const rise = ramp(t, tt - 2.4, tt + .2, E.io3);
  ctx.save(); ctx.fillStyle = `rgba(6,2,1,${.7 * ramp(lt, 0, 1.5)})`; ctx.beginPath(); ctx.ellipse(1300, gy + 4, 260, 22, 0, 0, TAU); ctx.fill(); ctx.restore();
  // yerden yükselen kor kıvılcımları
  for (let i = 0; i < 18; i++) { const ph = (lt * .45 + hash(i)) % 1, a = Math.sin(ph * PI) * ramp(lt, 0, 1.2);
    ctx.fillStyle = `rgba(214,110,60,${a * .8})`; ctx.beginPath(); ctx.arc(1300 + (hash(i + 3) - .5) * 420 + Math.sin(lt * 2 + i) * 12, gy - 10 - ph * 520, 2.5 + hash(i + 7) * 3, 0, TAU); ctx.fill(); }
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, gy + 3); ctx.clip();
  let hp = null;
  figure(ctx, { x: 1300, y: gy - 47 * 7 + (1 - rise) * 420, s: 7, dir: -1, lk: LK.thanatos, alpha: clamp(rise * 1.4), ...THS,
    p: { torso: .05, head: .1, wingF: t * .4, wingSpread: ramp(t, tt - .3, tt + 1.2, E.outBack), shN: .3, elN: .4, shF: .1, elF: .3, hipN: .05, hipF: -.05, brow: -1, handN: 'fist' }, margin: 120,
    onJoints: (J, M) => { hp = wrW(ctx, M, J, 'N'); } });
  if (hp && rise > .3) { ctx.save(); ctx.globalAlpha = clamp(rise * 1.4); handChain(ctx, hp, Math.min(220, gy - hp[1] + 3), t); ctx.restore(); }
  ctx.restore();
  nameTag(ctx, 'THANATOS', 'Ölüm', 140, 170, t - Wd('D01', 'kendisini') + .2, 3.8, { col: C.white });
  chapterCard(ctx, 'BÖLÜM III', 'ÖLÜMÜ ZİNCİRLEYEN ADAM', lt - .1, 3.2);
}, { tr: { type: 'black', dur: 1.0 }, post: { tex: .7, vig: .95 } });

// D2 — sarayın kapısında
shot(S('D02') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  const op = ramp(lt, .1, 1.2, E.io2);
  palace(ctx, t, { dark: .75, door: op, cols: [160, 520, 1400, 1760] });
  const gy = 880, step = ramp(lt, 1.2, 3.6, E.io2);
  const raise = ramp(t, Wd('D02', 'zincirlerle') - .3, Wd('D02', 'zincirlerle') + .4, E.outBack);
  let hp = null;
  walkScene(ctx, null, lerp(960, 1080, step), 6.4, t, -1, { noCam: true, ground: FLAT(gy), dist: step * 120, lk: LK.thanatos, alpha: ramp(lt, .4, 1.0), ...THS, cutCol: '#2A140C',
    p: { wingSpread: .55, wingF: t * .3, shN: lerp(.2, 1.35, raise), elN: lerp(.35, .7, raise), handN: 'fist', brow: -1 }, onJoints: (J, M) => { hp = wrW(ctx, M, J, 'N'); } });
  if (hp) { ctx.save(); ctx.globalAlpha = ramp(lt, .4, 1.0); handChain(ctx, hp, Math.min(300, gy - hp[1] - 4), t, 0, 20); ctx.restore(); if (raise > .5) sparkle(ctx, hp[0] + 6, hp[1] + 120, 22 * clamp(1 - Math.abs(t - Wd('D02', 'zincirlerle') - .3) * 2), 1); }
}, { tr: { type: 'cut' }, post: { tex: .6, vig: 1 } });

// D3–D4 — Sisifos sakin; "Bunlar nasıl takılıyor?" (araya zincir yakın planı)
function drawD3(ctx, st) {
  const t = st.t, lt = t - (S('D03') - .2), tq = S('D04'), tg = Wd('D04', 'gösterir');
  palace(ctx, t, { dark: .45, cols: [120, 1800] });
  const gy = 880;
  throne(ctx, 360, gy, 5.6, 1, C.ink, C.clay, { high: true });
  const cur = ramp(t, Wd('D03', 'merakla') - .2, Wd('D03', 'merakla') + .6);
  const ask = ramp(t, tq - .1, tq + .5, E.outBack);
  const calm = Math.sin(lt * 1.1);
  figure(ctx, { x: 455, y: gy - 27 * 5.6, s: 5.6, lk: LK.sisKing,
    p: { ...oturan(), torso: .1 + cur * .18 + calm * .02, neck: .1 * cur, head: .15 * cur - .05 + calm * .03, shN: lerp(.4, 1.5, ask), elN: lerp(1.3, .35, ask), handN: 'open', shF: .3, elF: 1.3, smile: .3 + ask * .4, brow: .6 * cur, blink: (lt % 3.1 > 2.98) ? 1 : 0 } });
  const ax = lerp(1500, 1180, ramp(lt, 0, 2.6, E.io2));
  const lift = ramp(t, tg - .2, tg + .5, E.outBack);
  let hN = null, hF = null;
  walkScene(ctx, null, ax, 6.4, t, -1, { noCam: true, ground: FLAT(gy), dist: ax, lk: LK.thanatos, ...THS, cutCol: '#3A1A10',
    p: { wingSpread: .45, wingF: t * .25, shN: lerp(.6, 1.3, lift), elN: lerp(.8, 1.2, lift), shF: lerp(.3, 1.2, lift), elF: lerp(.6, 1.3, lift), handN: 'fist', handF: 'fist', head: .25 * lift, brow: lerp(-1, .3, lift) },
    onJoints: (J, M) => { hN = wrW(ctx, M, J, 'N'); hF = wrW(ctx, M, J, 'F'); } });
  if (hN && hF) { chain(ctx, [hN, [lerp(hN[0], hF[0], .5), Math.max(hN[1], hF[1]) + 150 - lift * 80], hF], 18, '#E1B07A', '#5A2A16', 6); }
}
shot(S('D03') - .2, (ctx, st) => drawD3(ctx, st), { tr: { type: 'fade', dur: .5 }, post: { tex: .75, vig: .95 } });
// ara plan: Sisifos'un meraklı yüzü ve önde sallanan altın zincir
shot(Wd('D03', 'sadece') - .15, (ctx, st) => {
  const t = st.t, lt = st.lt;
  palace(ctx, t, { dark: .6, cols: [] });
  glow(ctx, 1250, 420, 700, 'rgba(255,190,110,.18)');
  const z = lerp(1, 1.06, st.p);
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  figure(ctx, { x: 520, y: 1420, s: 21, lk: LK.sisKing, p: { torso: .12, neck: .1, head: .12 + Math.sin(lt * 1.3) * .03, shN: .3, shF: 0, brow: .9, smile: .45, blink: (lt > 1.6 && lt < 1.72) ? 1 : 0 }, margin: 60 });
  ctx.restore();
  const sw = Math.sin(lt * 1.6) * 40;
  chain(ctx, [[1260, -40], [1260 + sw * .5, 360], [1260 + sw, 780]], 46, '#E1B07A', '#5A2A16', 15);
  for (let i = 0; i < 3; i++) { const u = (lt * .5 + i / 3) % 1; sparkle(ctx, 1260 + sw * u, 120 + u * 640, 26 * Math.sin(u * PI), Math.sin(u * PI)); }
}, { tr: { type: 'cut' }, post: { tex: .7, vig: .95 } });
shot(S('D04') - .15, (ctx, st) => drawD3(ctx, st), { tr: { type: 'cut' }, post: { tex: .75, vig: .95 } });

// D5 — kendi bileklerine geçirir; kilit kapanır (orta plan → kilit yakın planı → iki kişilik plan)
const D5W = [1040, 560];
function drawD5(ctx, t, c, phase) {
  const tk = Wd('D05', 'kilidi'), gy = 880, wr = D5W;
  palace(ctx, t, { dark: .5, cols: [120, 1800] });
  ctx.save(); cam(ctx, c, 1);
  const on = ramp(t, S('D05') + .1, Wd('D05', 'bileklerine') + .3, E.io2);
  figure(ctx, { x: 1180, y: gy - 47 * 6.4, s: 6.4, dir: -1, lk: LK.thanatos, ...THS, cutCol: '#3A1A10',
    p: { wingSpread: .4, wingF: t * .2, torso: .15, neck: .25, head: .4, handN: 'fist', handF: 'fist', brow: phase === 2 ? 1.2 : .3, hipN: .1, hipF: -.1, mouthOpen: phase === 2 ? .3 : 0 },
    ik: { hN: [wr[0] + 14 + (1 - on) * 50, wr[1] + 4 + (1 - on) * 30], hF: [wr[0] + 30 + (1 - on) * 80, wr[1] + 12 + (1 - on) * 40] } });
  throne(ctx, 360, gy, 5.6, 1, C.ink, C.clay, { high: true });
  if (phase === 0) figure(ctx, { x: 455, y: gy - 27 * 5.6, s: 5.6, lk: LK.sisKing, p: { ...oturan(), torso: .2, head: .05, shN: 1.2, elN: .6, smile: .6 } });
  else {
    const turn = phase === 1 ? ramp(t, tk - .1, tk + .25, E.out3) : 1;
    figure(ctx, { x: 860, y: gy - 47 * 5.6, s: 5.6, lk: LK.sisKing, hold: { N: HOLD.key() },
      p: { torso: .2, neck: .1, head: .15, handN: 'fist', smile: phase === 2 ? 1.4 : .9, hipN: .25, knN: .1, hipF: -.25, knF: .1 },
      ik: { hN: [wr[0] - 6, wr[1] + 2 - turn * 6], hF: [wr[0] - 20, wr[1] + 30] } });
  }
  const sz = 20;
  shackle(ctx, wr[0] + 8 + (1 - on) * 50, wr[1] + 4 + (1 - on) * 30, sz, .2, '#E1B07A', 1 - on);
  shackle(ctx, wr[0] + 26 + (1 - on) * 80, wr[1] + 12 + (1 - on) * 40, sz, .2, '#E1B07A', 1 - on);
  chain(ctx, [[wr[0] + 20, wr[1] + 20], [wr[0] + 60, wr[1] + 160], [wr[0] + 30, gy]], 20, '#E1B07A', '#5A2A16', 6);
  ctx.restore();
}
shot(S('D05') - .2, (ctx, st) => {
  const c = { x: lerp(1010, 1040, st.p), y: 560, z: lerp(1.45, 1.6, st.p) };
  drawD5(ctx, st.t, c, 0);
}, { tr: { type: 'fade', dur: .4 }, post: { tex: .75, vig: .95 } });
shot(Wd('D05', 'sisifos') - .25, (ctx, st) => {
  const t = st.t, tk = Wd('D05', 'kilidi');
  drawD5(ctx, t, { x: D5W[0] - 10, y: D5W[1] + 10, z: lerp(2.9, 3.1, st.p) }, 1);
  const fl = clamp(1 - Math.abs(t - tk - .12) * 5);
  if (fl > 0) { sparkle(ctx, W / 2 - 20, H / 2 - 10, 130 * fl, fl); ctx.save(); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgba(255,236,190,${fl * .25})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}, { tr: { type: 'cut' }, post: { tex: .75, vig: .95 } });
shot(Wd('D05', 'kilidi') + .9, (ctx, st) => {
  drawD5(ctx, st.t, { x: 1000, y: 540, z: lerp(1.15, 1.2, st.p) }, 2);
}, { tr: { type: 'cut' }, post: { tex: .75, vig: .95 } });

// D6 — Ölüm zincirde
shot(S('D06') - .25, (ctx, st) => {
  const t = st.t, lt = st.lt;
  ctx.fillStyle = '#0D0605'; ctx.fillRect(0, 0, W, H);
  const c = { x: 960, y: 520, z: lerp(1, 1.15, E.sine(st.p)) };
  ctx.save(); cam(ctx, c, 1);
  glow(ctx, 960, 480, 700, 'rgba(160,70,30,.35)');
  const gy = 900;
  ctx.fillStyle = '#1A0D09'; ctx.fillRect(-300, gy, W + 600, 400);
  column(ctx, 1010, 80, gy, 80, '#2A140C', '#6A3020');
  // zincirler bileklerden sütuna ve yere bağlı (figürün arkasından geçer)
  chain(ctx, [[1004, 604], [1012, 520], [1012, 300]], 22, '#E1B07A', '#5A2A16', 6);
  chain(ctx, [[1010, 612], [1060, 760], [1010, gy]], 22, '#E1B07A', '#5A2A16', 6);
  figure(ctx, { x: 960, y: gy - 25.5 * 6.6, s: 6.6, lk: LK.thanatos, sty: STY.red, cutCol: '#0D0605',
    p: { torso: .45, neck: .4, head: .5, hipN: 1.35, knN: 1.45, hipF: -.05, knF: 1.62, ankF: -1.4, wingSpread: .38, wingF: 0, handN: 'fist', handF: 'fist', brow: -1, blink: .4 },
    ik: { hN: [1000, 600], hF: [1016, 612] } });
  shackle(ctx, 1018, 614, 17, .2, '#E1B07A');
  shackle(ctx, 1004, 604, 17, .2, '#E1B07A');
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .5, vig: 1, grain: .07 } });

// D7 — ölümsüz savaş ve kesilemeyen kurban
shot(S('D07') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tk = Wd('D07', 'kalkıyor'), ts = Wd('D07', 'sunaklarda');
  daySky(ctx);
  const gy = 880;
  const pan = ramp(t, ts, ts + 1.0, E.io3);
  const c = { x: lerp(820, 1900, pan), y: 540, z: 1 };
  ctx.save(); cam(ctx, c, 1);
  ctx.fillStyle = C.ink; ctx.fillRect(-400, gy, 3400, 400);
  // savaş: biri saplanır, düşer, kalkar
  const hitT = S('D07') + 1.3;
  const fall = ramp(t, hitT, hitT + .5, E.in2) * (1 - ramp(t, tk - .3, tk + .6, E.io2));
  figure(ctx, { x: 560, y: gy - 46 * 5.2, s: 5.2, lk: LK.hoplite, hold: { N: HOLD.spear(95), F: HOLD.shield(17) },
    p: { torso: .25, hipN: .7, knN: .5, hipF: -.6, knF: .1, shN: lerp(1.6, .9, ramp(t, hitT - .3, hitT)), elN: .4, shF: .9, elF: 1.4, handN: 'fist', handF: 'fist', brow: -1 } });
  const pel = lerp(gy - 46 * 5.2, gy - 10 * 5.2, fall);
  figure(ctx, { x: 860 + fall * 60, y: pel, s: 5.2, dir: -1, lk: LK.hoplite, hold: { N: HOLD.spear(95), F: HOLD.shield(17) },
    p: { torso: lerp(.1, -1.3, fall), neck: -.2 * fall, hipN: lerp(.3, 1.4, fall), knN: lerp(.2, .1, fall), hipF: lerp(-.3, 1.2, fall), knF: .2, shN: lerp(1.0, 2.6, fall), elN: .5, shF: 1.0, elF: 1.2, handN: 'fist', handF: 'fist', brow: 1, mouthOpen: fall * .6 } });
  if (t > tk) txt(ctx, '?', 900, gy - 520, { font: '700 80px Cinzel', col: C.ink, a: ramp(t, tk, tk + .4) * (1 - ramp(t, ts - .5, ts)) });
  // sunak
  altar(ctx, 1900, gy, 2.2, C.ink, C.clay, 1, t);
  const kn = ramp(t, ts + .2, ts + .9, E.outBack);
  figure(ctx, { x: 1700, y: gy - 47 * 5.2, s: 5.2, lk: LK.priest, hold: { N: G => { G.part(c => { c.moveTo(-1, -2); c.lineTo(1, -2); c.lineTo(.6, 12); c.lineTo(-.6, 12); c.closePath(); }, { fill: '#D9C9A8', cut: false }); } },
    p: { torso: .05, head: .1, shN: lerp(1.0, 3.0, kn), elN: lerp(1.2, .3, kn), shF: .7, elF: 1.3, handN: 'fist', brow: ramp(t, ts + 1.5, ts + 2) * 1.2, mouthOpen: ramp(t, ts + 1.5, ts + 2) * .5 } });
  cow(ctx, 2160, gy, 2.6, -1, 0, { walk: 0, head: -.1 + Math.sin(t * .8) * .05, col: C.ink, inc: C.clay });
  ctx.restore();
}, { tr: { type: 'clay', dur: .8 }, post: { tex: .9, vig: .8 } });

// D8 — Ares öfkeden deliye döner; arkada canı sıkılan askerler zar oynar (Exekias'a selam)
shot(S('D08') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  daySky(ctx, .2);
  const gy = 880;
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  // zar oynayan iki asker: bloklara oturmuş, aradaki taşa eğilmiş
  ctx.fillStyle = C.ink; ctx.fillRect(1490, gy - 70, 90, 70); ctx.fillStyle = C.clay; ctx.fillRect(1492, gy - 72, 86, 3);
  for (const [x, d, k] of [[1300, 1, 0], [1770, -1, 1]]) {
    ctx.fillStyle = C.ink; ctx.fillRect(x - 70 * d - 40, gy - 60, 80, 60);
    const mv = k === Math.floor(lt / 1.4) % 2 ? Math.max(0, Math.sin(lt * 4.5)) : 0;
    figure(ctx, { x, y: gy - 60 - 4 * 4.2, s: 4.2, dir: d, lk: LK.hoplite, hold: { F: HOLD.spear(90) },
      p: { ...oturan({ hipN: 1.45, knN: 1.5, hipF: 1.4, knF: 1.6 }), torso: .42, neck: .25, head: .3, shN: 1.1 + mv * .5, elN: .6 - mv * .3, handN: 'open', shF: .2, elF: 1.2, blink: .5 } });
  }
  const stomp = Math.abs(Math.sin(lt * 4.5));
  const [sx, sy] = [noise1(t * 30, 1) * 7, noise1(t * 30, 2) * 7];
  ctx.save(); ctx.translate(sx, sy);
  figure(ctx, { x: 640, y: gy - 46 * 6.4 - stomp * 22, s: 6.4, lk: LK.ares, hold: { F: HOLD.shield(17), N: HOLD.spear(100) },
    p: { torso: .12 + Math.sin(lt * 9) * .05, neck: -.15, head: -.25, shN: 3.05 + Math.sin(lt * 11) * .18, elN: .25 + Math.sin(lt * 11) * .15, handN: 'fist', shF: .5, elF: 1.1, handF: 'fist',
      hipN: .3 + stomp * .6, knN: stomp * .9, hipF: -.25, knF: .1, brow: -1.6, mouthOpen: .5 + Math.max(0, Math.sin(lt * 8)) * .4 } });
  ctx.restore();
  nameTag(ctx, 'ARES', 'Savaş tanrısı', 140, 170, t - S('D08') + .1, 3.4, { col: C.ink, line: C.ink });
}, { tr: { type: 'fade', dur: .4 }, post: { tex: .9, vig: .85 } });
// D8b — "Kimsenin ölmediği bir savaşın ne anlamı vardı?": Ares'in yüzü, bağırır
shot(Wd('D08', 'kimsenin') - .15, (ctx, st) => {
  const t = st.t, lt = st.lt;
  clayBG(ctx, '#B4532C', '#5E2414');
  glow(ctx, 760, 420, 900, 'rgba(255,160,90,.25)');
  const [sx, sy] = [noise1(t * 26, 3) * 9, noise1(t * 26, 4) * 9];
  ctx.save(); ctx.translate(sx, sy);
  const z = lerp(1, 1.08, st.p);
  ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  figure(ctx, { x: 820, y: 1060, s: 11, lk: LK.ares, hold: { F: HOLD.shield(17) }, p: { torso: .22, neck: .05, head: .02 + Math.sin(lt * 6) * .04, shN: 1.55 + Math.sin(lt * 9) * .18, elN: 1.15, handN: 'fist', shF: .35, elF: 1.3, handF: 'fist', brow: -1.8, mouthOpen: .55 + Math.max(0, Math.sin(lt * 7)) * .45 }, margin: 60 });
  ctx.restore();
  friezeFrame(ctx, { h: 40 });
}, { tr: { type: 'cut' }, post: { tex: .8, vig: .9 } });

// D9 — Ares zinciri kırar, Thanatos serbest kalır…
shot(S('D09') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tb = Wd('D09', 'kurtardı') - .2;
  ctx.fillStyle = '#3A1C12'; ctx.fillRect(0, 0, W, H);
  glow(ctx, 960, 480, 1000, 'rgba(210,110,60,.42)');
  const gy = 900;
  ctx.fillStyle = '#1A0D09'; ctx.fillRect(0, gy, W, 300);
  const broken = t > tb;
  const free = ramp(t, tb + .1, tb + 1.0, E.out3);
  column(ctx, 1010, 80, gy, 80, '#2A140C', '#6A3020');
  figure(ctx, { x: 980, y: gy - lerp(25.5, 47, free) * 6.6, s: 6.6, dir: -1, lk: LK.thanatos, ...THS, cutCol: '#140A07',
    p: { torso: lerp(.45, .05, free), neck: lerp(.4, 0, free), head: lerp(.5, .05, free), hipN: lerp(1.35, .1, free), knN: lerp(1.45, .05, free), hipF: lerp(-.05, -.1, free), knF: lerp(1.62, .05, free), ankF: lerp(-1.4, 0, free),
      wingSpread: lerp(.38, 1.0, free), wingF: t * .5, handN: 'fist', handF: 'fist', brow: -1, shN: lerp(.4, .2, free), elN: .3 } });
  if (!broken) { chain(ctx, [[1000, 600], [1010, 520], [1010, 300]], 22, '#E1B07A', '#5A2A16', 6); shackle(ctx, 1004, 604, 17, .2, '#E1B07A'); }
  else for (let i = 0; i < 12; i++) { const u = t - tb; sparkle(ctx, 1000 + Math.cos(i) * u * 420, 560 + Math.sin(i * 2.3) * u * 300 + u * u * 300, 16, clamp(1 - u * 1.5)); }
  const swing = ramp(t, tb - .5, tb, E.in3);
  figure(ctx, { x: 560, y: gy - 46 * 6.4, s: 6.4, lk: LK.ares, hold: { N: HOLD.spear(100) },
    p: { torso: .2 + swing * .3, shN: lerp(3.0, 1.2, swing), elN: lerp(.8, .1, swing), handN: 'fist', shF: .6, elF: 1.5, hipN: .5, knN: .3, hipF: -.4, knF: .1, brow: -1.2 } });
  const fl = clamp(1 - Math.abs(t - tb - .05) * 5) * (t > tb - .02 ? 1 : 0);
  if (fl > 0) { ctx.save(); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgba(255,220,170,${fl * .35})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}, { tr: { type: 'cut' }, post: { tex: .5, vig: 1, grain: .07 } });
// D9b — …ve Sisifos'u kendi elleriyle Ölüm'e teslim eder: Ares iter, Thanatos bileğinden yakalar; kanatlar kapanır
shot(Wd('D09', 'sisifos') - .15, (ctx, st) => {
  const t = st.t, lt = st.lt, tg = Wd('D09', 'teslim');
  ctx.fillStyle = '#3A1C12'; ctx.fillRect(0, 0, W, H);
  glow(ctx, 1100, 480, 1000, 'rgba(210,110,60,.42)');
  const gy = 900;
  ctx.fillStyle = '#1A0D09'; ctx.fillRect(0, gy, W, 300);
  const shove = ramp(t, tg - .9, tg + .1, E.io2);
  const xs = lerp(820, 1010, shove);
  // Sisifos (önce): öne doğru tökezler, kolu Ölüm'e uzanmış
  let wrS = null;
  figure(ctx, { x: xs, y: gy - 46 * 5.6 + shove * 14, s: 5.6, lk: LK.sisKing,
    p: { torso: .25 + shove * .25, neck: -.1, head: -.15, shN: lerp(.9, 1.4, shove), elN: .3, handN: 'open', shF: lerp(-.6, -1.2, shove), elF: .4, handF: 'open',
      hipN: .5 * shove, knN: .5 * shove, hipF: -.5 * shove, knF: .7 * shove, brow: 1.6, mouthOpen: .8 },
    onJoints: (J, M) => { wrS = wrW(ctx, M, J, 'N'); } });
  // Ares: arkadan iter (eli Sisifos'un sırtında)
  figure(ctx, { x: xs - 330, y: gy - 46 * 6.4, s: 6.4, lk: LK.ares,
    p: { torso: .3, neck: -.1, head: -.1, handN: 'open', shF: .3, elF: 1.4, hipN: .6, knN: .4, hipF: -.5, knF: .1, brow: -1.2 },
    ik: { hN: [xs - 70, gy - 46 * 5.6 - 120 + shove * 10] } });
  // Thanatos: kanatlar açık, Sisifos'un bileğini yakalar
  const grab = ramp(t, tg - .2, tg + .3, E.out3);
  figure(ctx, { x: 1420, y: gy - 47 * 6.6, s: 6.6, dir: -1, lk: LK.thanatos, ...THS, cutCol: '#140A07',
    p: { torso: .1, head: .05, wingSpread: 1.0 - grab * .2, wingF: t * .5, handN: 'open', handF: 'fist', shF: .3, elF: .5, brow: -1 },
    ik: wrS ? { hN: [lerp(1260, wrS[0] + 10, grab), lerp(560, wrS[1], grab)] } : {} });
  // kanatlar ekranı kaplar
  const env = ramp(t, tg + .6, st.end, E.in3);
  if (env > 0) { ctx.save(); ctx.fillStyle = '#000'; ctx.globalAlpha = env; ctx.beginPath(); ctx.arc(1250, 520, lerp(0, 1500, env), 0, TAU); ctx.fill(); ctx.restore(); }
}, { tr: { type: 'cut' }, post: { tex: .5, vig: 1, grain: .07 } });
