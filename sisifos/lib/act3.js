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
  const dark = ramp(lt, .5, 4) * .7;
  clayBG(ctx, mixCol('#C9733F', '#5A2A18', dark), mixCol('#8E4022', '#2A120A', dark));
  const gy = 880;
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  throne(ctx, 300, gy, 6, 1, C.ink, C.clay, { high: true });
  // Zeus: tahtta, elinde yıldırım (C3'teki gibi) — Sisifos'un tahtıyla karışmasın
  figure(ctx, { x: 400, y: gy - 27 * 6, s: 6, lk: LK.zeus, hold: { F: HOLD.scepter(80), N: HOLD.bolt() },
    p: { ...oturan(), torso: .05, head: .05, shN: lerp(.4, 1.75, ramp(lt, .3, 1.1, E.outBack)), elN: .15, handN: 'fist', shF: .3, elF: 1.2, brow: -1 } });
  { const bl = ramp(lt, .9, 1.3) * (1 - ramp(lt, 1.3, 2.2)); if (bl > 0) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, 520, gy - 520, 240, `rgba(255,220,140,${.5 * bl})`); ctx.restore(); } }
  nameTag(ctx, 'ZEUS', 'Tanrıların kralı', 140, 250, lt - 3.3, 3.0, { col: C.white }); // bölüm kartından sonra (yeterince uzun kalır)
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
  nameTag(ctx, 'THANATOS', 'Ölüm', 1140, 150, t - Wd('D01', 'kendisini') + .2, 3.8, { col: C.white, align: 'center' });
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
  // varınca ayaklar yan yana durur (adım ortasında donmaz); D5 kesmesinden 0.5 sn önce zinciri bel hizasına indirir (D5'in ilk pozu)
  const drop = ramp(t, S('D05') - .8, S('D05') - .3, E.io2), lift = ramp(t, tg - .2, tg + .5, E.outBack) * (1 - drop), sdT = ramp(lt, 2.3, 2.9, E.io2);
  let hN = null, hF = null;
  walkScene(ctx, null, ax, 6.4, t, -1, { noCam: true, ground: FLAT(gy), dist: ax, stand: sdT, lk: LK.thanatos, ...THS, cutCol: '#3A1A10',
    p: { wingSpread: .45, wingF: t * .25, shN: lerp(lerp(.6, 1.3, lift), .55, drop), elN: lerp(lerp(.8, 1.2, lift), .45, drop), shF: lerp(lerp(.3, 1.2, lift), .7, drop), elF: lerp(lerp(.6, 1.3, lift), .4, drop), handN: 'fist', handF: 'fist', head: .25 * lift + .35 * drop, brow: lerp(-1, .3, lift) },
    onJoints: (J, M) => { hN = wrW(ctx, M, J, 'N'); hF = wrW(ctx, M, J, 'F'); } });
  if (hN && hF) { chain(ctx, [hN, [lerp(hN[0], hF[0], .5), Math.max(hN[1], hF[1]) + 150 - lift * 80], hF], 18, '#E1B07A', '#5A2A16', 6); }
}
shot(S('D03') - .2, (ctx, st) => drawD3(ctx, st), { tr: { type: 'cut' }, post: { tex: .75, vig: .95 } });
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
  chain(ctx, [[1262, 250], [1260 + sw * .5, 520], [1260 + sw, 840]], 46, '#E1B07A', '#5A2A16', 15);
  // zinciri tutan Thanatos'un eli (kırmızı figür): kadrajın üstünden giren ön kol ve yumruk
  ctx.save(); ctx.translate(1262, 215); ctx.rotate(Math.sin(lt * 1.6) * .03);
  ctx.fillStyle = '#C7683C'; ctx.strokeStyle = '#1E0E09'; ctx.lineWidth = 6;
  ctx.beginPath(); ctx.moveTo(-36, -330); ctx.lineTo(36, -330); ctx.lineTo(44, -30); ctx.lineTo(-44, -30); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.scale(22, 22); ctx.beginPath(); HAND.fist.forEach((q, i) => i ? ctx.lineTo(q[0], q[1] - 2.2) : ctx.moveTo(q[0], q[1] - 2.2)); ctx.closePath();
  ctx.fill(); ctx.lineWidth = 6 / 22; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(-1.2, .6); ctx.lineTo(1.6, .6); ctx.moveTo(-1.4, 1.6); ctx.lineTo(1.8, 1.6); ctx.stroke();
  ctx.restore();
  for (let i = 0; i < 3; i++) { const u = (lt * .5 + i / 3) % 1; sparkle(ctx, 1260 + sw * u, 120 + u * 640, 26 * Math.sin(u * PI), Math.sin(u * PI)); }
}, { tr: { type: 'cut' }, post: { tex: .7, vig: .95 } });
shot(S('D04') - .15, (ctx, st) => drawD3(ctx, st), { tr: { type: 'cut' }, post: { tex: .75, vig: .95 } });

// D5 — kendi bileklerine geçirir; kilit kapanır (orta plan → kilit yakın planı → iki kişilik plan)
const D5W = [1040, 560];
function drawD5(ctx, t, c, phase) {
  const tk = Wd('D05', 'kilidi'), gy = 880, wr = D5W;
  palace(ctx, t, { dark: .5, cols: [30, 1890] }); // sütunlar kenarda: yürüyen Sisifos'la birleşmez
  ctx.save(); cam(ctx, c, 1);
  const on = ramp(t, S('D05') + .1, Wd('D05', 'bileklerine') + .3, E.io2);
  figure(ctx, { x: 1180, y: gy - 47 * 6.4, s: 6.4, dir: -1, lk: LK.thanatos, ...THS, cutCol: '#3A1A10',
    p: { wingSpread: .4, wingF: t * .2, torso: .15, neck: .25, head: .4, handN: 'fist', handF: 'fist', brow: phase === 2 ? 1.2 : .3, hipN: .1, hipF: -.1, mouthOpen: phase === 2 ? .3 : 0 },
    ik: { hN: [wr[0] + 14 + (1 - on) * 50, wr[1] + 4 + (1 - on) * 30], hF: [wr[0] + 30 + (1 - on) * 80, wr[1] + 12 + (1 - on) * 40] } });
  throne(ctx, 360, gy, 5.6, 1, C.ink, C.clay, { high: true });
  if (phase === 0) {
    // tahttan kalkar ve merakla Thanatos'a doğru yürür (kilit planındaki yerine gelir)
    // kalkış: önce gövde öne eğilir (ağırlık ayaklara), kalça ancak sonra yükselir; doğrulurken baş öne bakar
    const t0s = S('D05') - .15;
    const lean = keyed(t, [[t0s, { torso: .2, head: .05 }], [t0s + .38, { torso: .66, head: -.12 }, E.io2], [t0s + 1.0, { torso: .12, head: .08 }, E.io2]]);
    const su = ramp(t, t0s + .28, t0s + 1.0, E.io2), wk = ramp(t, t0s + .9, Wd('D05', 've') - .25, E.io2);
    if (wk <= 0) { const o = oturan(), k = 1 - su; figure(ctx, { x: 455 + su * 24, y: lerp(gy - 27 * 5.6, gy - 46.5 * 5.6, su), s: 5.6, lk: LK.sisKing,
      p: { ...o, hipN: o.hipN * k, knN: o.knN * k, hipF: o.hipF * k, knF: o.knF * k, torso: lean.torso, head: lean.head, shN: lerp(1.2, .3, su), elN: .6, smile: .6 } }); }
    else { const x = lerp(479, 860, wk); walkScene(ctx, null, x, 5.6, t, 1, { noCam: true, ground: FLAT(gy), dist: x, lk: LK.sisKing, stride: lerp(6, 30, ramp(wk, 0, .2)), stand: 1 - ramp(wk, 0, .15), p: { smile: .6, head: .08, shN: Math.sin(x / 40) * .25, shF: -Math.sin(x / 40) * .25 } }); }
  }
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
  const c = { x: lerp(915, 950, st.p), y: 560, z: lerp(1.45, 1.6, st.p) }; // tahtın yüksek arkalığı kadrajın kenarında görünür (aynı taht)
  drawD5(ctx, st.t, c, 0);
}, { tr: { type: 'cut' }, post: { tex: .75, vig: .95 } });
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
  // diz çökmüş Ölüm: gövde dik, baş eğik, bilekleri sütundaki halkaya zincirli; kanatlar sırtta toplu (yavaş, ağır nefes)
  ctx.save(); ctx.strokeStyle = '#2A140C'; ctx.lineWidth = 12; ctx.beginPath(); ctx.arc(992, 560, 22, 0, TAU); ctx.stroke(); ctx.strokeStyle = '#8A4A2A'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(992, 560, 22, 0, TAU); ctx.stroke(); ctx.restore();
  const br = Math.sin(lt * 1.3);
  let wN = null, wF = null;
  figure(ctx, { x: 800, y: gy - 25.5 * 6.6, s: 6.6, lk: LK.thanatos, sty: STY.red, cutCol: '#0D0605',
    p: { torso: .12 + br * .02, neck: .32, head: .38, hipN: 1.35, knN: 1.45, hipF: -.05, knF: 1.62, ankF: -.5, wingSpread: .22, wingF: .55, handN: 'fist', handF: 'fist', brow: -1, blink: .45, breath: br * 1.4 },
    ik: { hN: [940, 588], hF: [956, 600] }, onJoints: (J, M) => { wN = wrW(ctx, M, J, 'N'); wF = wrW(ctx, M, J, 'F'); } });
  if (wN && wF) {
    chain(ctx, [wN, [lerp(wN[0], 992, .5), 600], [992, 572]], 22, '#E1B07A', '#5A2A16', 6);
    chain(ctx, [wF, [wF[0] + 20, 760], [960, gy - 4]], 22, '#E1B07A', '#5A2A16', 6);
    shackle(ctx, wN[0], wN[1], 17, .2, '#E1B07A'); shackle(ctx, wF[0], wF[1], 17, .2, '#E1B07A');
  }
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .5, vig: 1, grain: .07 } });

// D7 — ölümsüz savaş ve kesilemeyen kurban
shot(S('D07') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tk = Wd('D07', 'kalkıyor'), ts = Wd('D07', 'sunaklarda');
  daySky(ctx);
  const gy = 880;
  const pan = ramp(t, ts, ts + 1.0, E.io3);
  const pin = ramp(t, ts + .3, ts + 1.4, E.io2); // sunakta yakınlaşma: kurban şakası okunsun
  const c = { x: lerp(lerp(820, 2120, pan), 2110, pin), y: lerp(540, 690, pin), z: lerp(1, 1.4, pin) };
  ctx.save(); cam(ctx, c, 1);
  ctx.fillStyle = C.ink; ctx.fillRect(-400, gy, 4600, 400);
  // savaş: biri saplanır, düşer, kalkar
  const hitT = S('D07') + 1.3;
  const fall = ramp(t, hitT, hitT + .5, E.in2) * (1 - ramp(t, tk - .3, tk + .6, E.io2));
  figure(ctx, { x: 560, y: gy - 46 * 5.2, s: 5.2, lk: LK.hoplite, hold: { N: HOLD.spear(95), F: HOLD.shield(17) },
    p: { torso: .25, hipN: .7, knN: .5, hipF: -.6, knF: .1, shN: lerp(1.6, .9, ramp(t, hitT - .3, hitT)), elN: .4, shF: .9, elF: 1.4, handN: 'fist', handF: 'fist', brow: -1 } });
  const pel = lerp(gy - 46 * 5.2, gy - 9 * 5.2, fall), x0 = 860 + fall * 60;
  // ayaklar hep zeminde: ayakta duruştan sırtüstü yatışa (bacaklar yerde öne uzanır)
  const ikF = fall > 0 ? { fN: [lerp(x0 - 48, x0 - 205, fall), gy - 3 * 5.2, 0], fF: [lerp(x0 + 30, x0 - 180, fall), gy - 3 * 5.2, 0] } : undefined;
  // düşerken mızrak ve kalkan elinden yere düşer
  if (fall > .35) { ctx.save(); ctx.strokeStyle = C.ink; ctx.lineWidth = 7; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x0 - 330, gy - 5); ctx.lineTo(x0 + 40, gy - 9); ctx.stroke();
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.ellipse(x0 + 120, gy - 20, 64, 18, 0, 0, TAU); ctx.fill(); ctx.strokeStyle = C.clay; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(x0 + 120, gy - 22, 48, 11, 0, 0, TAU); ctx.stroke(); ctx.restore(); }
  figure(ctx, { x: x0, y: pel, s: 5.2, dir: -1, lk: LK.hoplite, hold: fall > .35 ? null : { N: HOLD.spear(95), F: HOLD.shield(17) }, ik: ikF,
    p: { torso: lerp(.1, -1.3, fall), neck: -.2 * fall, hipN: lerp(.3, 1.4, fall), knN: lerp(.2, .1, fall), hipF: lerp(-.3, 1.2, fall), knF: .2, shN: lerp(1.0, 2.6, fall), elN: .5, shF: 1.0, elF: 1.2, handN: 'fist', handF: 'fist', brow: 1, mouthOpen: fall * .6 } });
  if (t > tk) txt(ctx, '?', 900, gy - 520, { font: '700 80px Cinzel', col: C.ink, a: ramp(t, tk, tk + .4) * (1 - ramp(t, ts - .5, ts)) });
  // sunak: rahip bıçağı kaldırır, "kesilemiyordu"da indirir — bıçak boğanın boynundan seker (kıvılcım), boğa başını kaldırır, yarasız
  altar(ctx, 2470, gy, 2.2, C.ink, C.clay, 1, t);
  const tK = Wd('D07', 'kesilemiyordu');
  const kn = ramp(t, ts + .2, ts + .9, E.outBack), strike = ramp(t, tK - .28, tK - .02, E.in3), rec = ramp(t, tK + .02, tK + .4, E.io2); // geri sekme: ~10 karede bıçak başın yanına, gövde geriye (ikinci darbe yok)
  figure(ctx, { x: 1930, y: gy - 47 * 5.2, s: 5.2, lk: LK.priest, hold: { N: G => { G.part(c => { c.moveTo(-1, -2); c.lineTo(1, -2); c.lineTo(.6, 12); c.lineTo(-.6, 12); c.closePath(); }, { fill: '#D9C9A8', cut: false }); } },
    p: { torso: .05 + strike * .5 - rec * .65, head: .1 + strike * .2 - rec * .55, shN: lerp(1.0, 3.0, kn) - strike * 2.2 + rec * 1.9, elN: lerp(lerp(lerp(1.2, .3, kn), .15, strike), 1.5, rec), shF: lerp(.7, .1, rec), elF: lerp(1.3, 2.1, rec), handN: 'fist',
      brow: ramp(t, tK + .05, tK + .5) * 1.4, mouthOpen: ramp(t, tK + .05, tK + .5) * .6 } });
  const sp = clamp(1 - Math.abs(t - tK - .04) * 6) * (t > tK - .03 ? 1 : 0);
  if (sp > 0) sparkle(ctx, 2080, 728, 70 * sp, sp);
  cow(ctx, 2250, gy, 2.6, -1, 0, { walk: 0, head: -.1 + Math.sin(t * .8) * .05 + ramp(t, tK + .05, tK + .5, E.out3) * .45, col: C.ink, inc: C.clay });
  ctx.restore();
}, { tr: { type: 'clay', dur: .8 }, post: { tex: .9, vig: .8 }, mb: 12 });

// D8 — Ares öfkeden deliye döner; arkada canı sıkılan askerler zar oynar (Exekias'a selam)
shot(S('D08') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  daySky(ctx, .2);
  const gy = 880;
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  // zar oynayan iki asker: bloklara oturmuş, aradaki taşa eğilmiş
  ctx.fillStyle = C.ink; ctx.fillRect(1490, gy - 70, 90, 70); ctx.fillStyle = C.clay; ctx.fillRect(1492, gy - 72, 86, 3);
  // zarlar (atılınca zıplar)
  { const thr = (lt % 1.4) / 1.4, hop = Math.max(0, Math.sin(thr * PI * 2)) * (thr < .5 ? 1 : 0);
    [[1512, 0], [1548, 1]].forEach(([dx, k]) => { const y = gy - 72 - 22 - hop * (40 + k * 16), a = hop * (2 + k) ;
      ctx.save(); ctx.translate(dx, y + 11); ctx.rotate(a); ctx.fillStyle = '#F1E4C6'; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.fillRect(-11, -11, 22, 22); ctx.strokeRect(-11, -11, 22, 22);
      ctx.fillStyle = C.ink; for (const [px, py] of [[-5, -5], [0, 0], [5, 5]].slice(0, 2 + k)) { ctx.beginPath(); ctx.arc(px, py, 2.4, 0, TAU); ctx.fill(); } ctx.restore(); }); }
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
}, { tr: { type: 'cut' }, post: { tex: .9, vig: .85 } });
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
  clayBG(ctx, '#8A4326', '#4A2214', { x: 960, y: 460, r: 1000, c: 'rgba(240,150,90,.45)' });
  const gy = 900;
  ctx.fillStyle = '#1A0D09'; ctx.fillRect(0, gy, W, 300); ctx.fillStyle = 'rgba(214,130,80,.5)'; ctx.fillRect(0, gy, W, 3);
  const broken = t > tb;
  const free = ramp(t, tb + .15, tb + 1.1, E.out3);
  column(ctx, 1070, 80, gy, 80, '#2A140C', '#6A3020');
  // demir halka zemine çakılı (zincir yüzün önünden geçmez)
  ctx.save(); ctx.fillStyle = '#2A140C'; ctx.fillRect(799, gy - 10, 42, 12); ctx.strokeStyle = '#2A140C'; ctx.lineWidth = 11; ctx.beginPath(); ctx.ellipse(820, gy - 26, 20, 18, 0, 0, TAU); ctx.stroke(); ctx.strokeStyle = '#8A4A2A'; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(820, gy - 26, 20, 18, 0, 0, TAU); ctx.stroke(); ctx.restore();
  // D8'deki mızrak ve kalkan: Ares onları kenara bırakmış (süreklilik)
  ctx.save(); ctx.strokeStyle = C.ink; ctx.lineWidth = 9; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(60, gy - 7); ctx.lineTo(430, gy - 12); ctx.stroke();
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(430, gy - 22); ctx.lineTo(472, gy - 12); ctx.lineTo(430, gy - 2); ctx.closePath(); ctx.fill();
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.ellipse(250, gy - 74, 30, 76, -.18, 0, TAU); ctx.fill(); ctx.strokeStyle = '#C7683C'; ctx.lineWidth = 4; ctx.beginPath(); ctx.ellipse(250, gy - 74, 22, 62, -.18, 0, TAU); ctx.stroke(); ctx.restore();
  const ring = [820, gy - 26];
  // Ares yürür, ayağını kaldırır ve zemindeki halkaya bağlı zincire basarak koparır (savaş tanrısının gücü)
  const ax = lerp(360, 620, ramp(t, tb - 1.5, tb - .6, E.io2));
  const lift = ramp(t, tb - .55, tb - .15, E.io2), stomp = ramp(t, tb - .15, tb, E.in3), rec2 = ramp(t, tb + .25, tb + .8, E.io2);
  const sp = [lerp(lerp(ax + 120, 780, lift), 808, stomp), lerp(lerp(gy - 18, gy - 190, lift), gy - 18, stomp)];
  const footT = rec2 > 0 ? lerp2([808, gy - 18], [ax + 60, gy - 18], rec2) : sp;
  // Thanatos: diz çökmüş, bilekleri zemindeki halkaya zincirli; kurtulunca ayağa kalkar
  const tx = 1060, ty = gy - lerp(25.5, 47, free) * 6.6;
  let wN = null, wF = null;
  figure(ctx, { x: tx, y: ty, s: 6.6, dir: -1, lk: LK.thanatos, ...THS, cutCol: '#140A07',
    p: { torso: lerp(.25, .05, free), neck: lerp(.1, 0, free), head: lerp(.12, .05, free), hipN: lerp(1.35, .1, free), knN: lerp(1.45, .05, free), hipF: lerp(-.05, -.1, free), knF: lerp(1.62, .05, free), ankF: lerp(-.5, 0, free),
      wingSpread: lerp(.38, 1.0, free), wingF: t * .5, handN: 'fist', handF: 'fist', brow: -1 },
    ik: { hN: lerp2([985, 690], [tx - 60, ty + 30], free), hF: lerp2([1000, 700], [tx + 20, ty + 40], free) },
    onJoints: (J, M) => { wN = wrW(ctx, M, J, 'N'); wF = wrW(ctx, M, J, 'F'); } });
  if (wN && wF) {
    shackle(ctx, wN[0], wN[1], 17, .2, '#E1B07A'); shackle(ctx, wF[0], wF[1], 17, .2, '#E1B07A');
    const w = lerp2(wN, wF, .5);
    if (!broken) chain(ctx, [w, [lerp(w[0], ring[0], .5) - 6, lerp(w[1], ring[1], .5) + 10], ring], 22, '#E1B07A', '#5A2A16', 6);
    else {
      // kopan zincir bilekten sarkar, halkalar sıçrar
      const u = t - tb;
      chain(ctx, [w, [w[0] - 14, w[1] + 70 + Math.sin(u * 9) * 8 * Math.exp(-u * 2)], [w[0] - 8, w[1] + 130]], 22, '#E1B07A', '#5A2A16', 6);
      for (let i = 0; i < 3; i++) { const x = ring[0] + 20 + (i - 1) * 60 * u, y = Math.min(gy - 8, ring[1] - 10 - 380 * u + 1500 * u * u);
        ctx.save(); ctx.translate(x, y); ctx.rotate(u * (4 + i)); chain(ctx, [[-20, 0], [20, 0]], 20, '#E1B07A', '#5A2A16', 6); ctx.restore(); }
      if (u < .3) sparkle(ctx, ring[0] + 10, ring[1] - 10, 80 * (1 - u * 3.3), 1 - u * 3.3);
    }
  }
  // Ares: ayak kalkar, iner (arka kolu dengede), sonra geri çekilir
  walkScene(ctx, null, ax, 6.4, t, 1, { noCam: true, ground: FLAT(gy), dist: ax, lk: LK.ares, lean: -.08 * lift + .12 * stomp,
    p: { brow: -1.4, mouthOpen: stomp * (1 - rec2) * .6, handN: 'fist', handF: 'fist', shN: .6 + lift * .5, elN: 1.2, shF: -.3 - lift * .3, elF: .8 },
    ik: lift > 0 ? { fN: [footT[0], footT[1], 0] } : {} });
  const fl = clamp(1 - Math.abs(t - tb - .05) * 5) * (t > tb - .02 ? 1 : 0);
  if (fl > 0) { ctx.save(); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgba(255,220,170,${fl * .35})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}, { tr: { type: 'cut' }, post: { tex: .5, vig: 1, grain: .07 }, mb: 12 });
// D9b — …ve Sisifos'u kendi elleriyle Ölüm'e teslim eder: Ares iter, Thanatos bileğinden yakalar; kanatlar kapanır
shot(Wd('D09', 'sisifos') - .15, (ctx, st) => {
  const t = st.t, lt = st.lt, tg = Wd('D09', 'teslim');
  clayBG(ctx, '#8A4326', '#4A2214', { x: 1100, y: 460, r: 1000, c: 'rgba(240,150,90,.45)' });
  const gy = 900;
  // D9'dan farklı açı: daha yakın kadraj; aynı salon
  const c9 = { x: 1020, y: 562, z: 1.2, r: 0 }; // figürler kamera dönüşüyle dönmediği için zemin düz
  ctx.save(); cam(ctx, c9, 1);
  ctx.fillStyle = '#1A0D09'; ctx.fillRect(-400, gy, W + 800, 600); ctx.fillStyle = 'rgba(214,130,80,.5)'; ctx.fillRect(-400, gy, W + 800, 3);
  // zorla teslim: Ares ilk kareden omzunu kavrar ve sürükler; Sisifos geriye yaslanır, topukları kayar, kolu savunmada; son itiş "teslim"de
  column(ctx, 250, 0, gy, 80, '#2A140C', '#6A3020'); // aynı salon: D9'daki sütunlardan biri kadrajın kenarında
  const t0 = st.start ?? (Wd('D09', 'sisifos') - .15), drag = ramp(t, t0, tg - .5, E.io2), shove = ramp(t, tg - .5, tg + .1, E.in2), pull = ramp(t, tg + .3, tg + 1.3, E.io2);
  const xs = lerp(760, 900, drag) + shove * 110 + pull * 110;
  const strug = (1 - shove) * Math.sin(t * 9) * .05;
  let wrS = null, shS = null;
  // topuklar sürtünür: toz
  for (let k = 0; k < 4; k++) dustBurst(ctx, t, t0 + .3 + k * .45, xs + 30, gy, 6, 'rgba(120,64,36,.4)', 60, 70 + k);
  figure(ctx, { x: xs, y: gy - 45 * 5.6 + shove * 14, s: 5.6, lk: LK.sisKing, shadowBlur: 22, shadowCol: 'rgba(255,170,90,.85)',
    p: { torso: lerp(-.22, .2, shove) + strug, neck: -.1, head: lerp(-.25, .15, shove), shN: 2.25, elN: 1.45, handN: 'open', shF: lerp(-.9, -1.2, shove), elF: .4, handF: 'open',
      hipN: lerp(.55, .5, shove), knN: lerp(.15, .5, shove), hipF: lerp(.2, -.5, shove), knF: lerp(.1, .7, shove), ankN: -.3 * (1 - shove), ankF: -.3 * (1 - shove), brow: 1.6, mouthOpen: .5 + Math.max(0, Math.sin(t * 7)) * .3 },
    onJoints: (J, M) => { wrS = wrW(ctx, M, J, 'N'); const tr = ctx.getTransform().inverse(); const q = tr.transformPoint(M.transformPoint(new DOMPoint(J.shoulder[0], J.shoulder[1]))); shS = [q.x, q.y]; } });
  // Ares: arkasında; eli ilk kareden Sisifos'un omzunda, adım adım sürükler
  const ax = xs - 300 - pull * 110, AS2 = 30 * 6.4, gN = gait(ax, AS2, 5 * 6.4, 0), gF = gait(ax, AS2, 5 * 6.4, .5);
  const fy = gy - 3 * 6.4;
  figure(ctx, { x: ax, y: gy - 44 * 6.4, s: 6.4, lk: LK.ares,
    p: { torso: .3 + shove * .15, neck: -.1, head: -.1, handN: 'open', shF: .3, elF: 1.4, brow: -1.2, mouthOpen: shove * (1 - pull) * .4 },
    ik: { hN: shS ? lerp2([shS[0] - 10, shS[1] + 6], [ax + 70, gy - 330], pull) : [xs - 60, gy - 380], fN: [gN.x, fy - gN.lift, -gN.heel], fF: [gF.x, fy - gF.lift, -gF.heel] } }); // yürüme döngüsü: basan ayak yerinde, adımlar sırayla (bacaklar çapraz geçmez)
  // Thanatos: kanatlar açık, Sisifos'un bileğini yakalar
  const grab = ramp(t, tg - .2, tg + .3, E.out3);
  figure(ctx, { x: 1420 - pull * 40, y: gy - 47 * 6.6, s: 6.6, dir: -1, lk: LK.thanatos, ...THS, cutCol: '#140A07',
    p: { torso: .1 - pull * .1, head: .05, wingSpread: 1.0 - grab * .2 - pull * .55, wingF: t * .5, handN: 'open', handF: 'fist', shF: .3, elF: .5, brow: -1 },
    ik: wrS ? { hN: [lerp(1372, wrS[0] + 10, grab), lerp(650, wrS[1], grab)] } : {},
    onJoints: (J, M) => { // kırık kelepçeler ve sarkan halkalar bileklerinde kalır (D9 sürekliliği)
      for (const sd of ['N', 'F']) { const q = wrW(ctx, M, J, sd); shackle(ctx, q[0], q[1], 16, .2, '#E1B07A'); chain(ctx, [q, [q[0] - 6, q[1] + 60], [q[0] - 2, q[1] + 110]], 18, '#E1B07A', '#5A2A16', 5); } } }); // el ancak "teslim"de uzanır
  // kanatlar ekranı kaplar
  // temiz iris kapanışı: Ölüm ve kurbanı üzerinde daralan daire
  const ic = ctx.getTransform().transformPoint(new DOMPoint(1220, 560));
  ctx.restore();
  const icS = ctx.getTransform().inverse().transformPoint(ic); // iris merkezi ekran koordinatında
  const env = ramp(t, tg + 1.0, st.end, E.in2);
  if (env > 0) { const r = lerp(1600, 0, env); ctx.save(); ctx.fillStyle = '#000'; ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.arc(icS.x, icS.y, Math.max(0, r), 0, TAU, true); ctx.fill('evenodd'); ctx.restore(); }
}, { tr: { type: 'cut' }, post: { tex: .5, vig: 1, grain: .07 } });
