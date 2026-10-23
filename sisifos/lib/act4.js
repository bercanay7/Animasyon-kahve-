// IV. İKİNCİ HİLE
'use strict';
// E1 — ölüm döşeğinde fısıltı
shot(S('E01') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt;
  palace(ctx, t, { dark: .82, cols: [120, 1800] });
  const gy = 880, c = { x: lerp(980, 900, st.p), y: 560, z: lerp(1, 1.12, E.sine(st.p)) };
  ctx.save(); cam(ctx, c, 1);
  oilLamp(ctx, 1380, gy - 240, 2.4, t);
  ctx.fillStyle = C.ink; ctx.fillRect(1340, gy - 236, 80, 236);
  kline(ctx, 960, gy, 5.2, C.ink, C.clay);
  const lean = ramp(t, Wd('E01', 'kulağına') - .8, Wd('E01', 'kulağına'), E.io2);
  figure(ctx, { x: 820, y: gy - 30 * 5.2 - 26, s: 5.2, lk: LK.sisKing, p: { torso: -.55, neck: .3, head: .2 - lean * .25, hipN: 1.6, knN: .05, hipF: 1.55, knF: .1, ankN: -.2, ankF: -.2, shN: .4, elN: 1.8, shF: .8, elF: .5, blink: .45, breath: Math.sin(t * 1.2) } });
  figure(ctx, { x: 560, y: gy - 46 * 5.0, s: 5.0, lk: LK.merope, p: { torso: .35 + lean * .35, neck: .2, head: .3 + lean * .1, shN: .9, elN: .7, shF: .6, elF: 1.0, hipN: .15, hipF: -.1, blink: (lt > 2.2 && lt < 2.34) ? 1 : 0 } });
  ctx.restore();
  chapterCard(ctx, 'BÖLÜM IV', 'İKİNCİ HİLE', lt - .1, 3.0);
  nameTag(ctx, 'MEROPE', 'Sisifos\'un karısı', 140, 170, t - Wd('E01', 'merope') + .1, 3.0, { col: C.white });
}, { tr: { type: 'black', dur: 1.0 }, post: { tex: .6, vig: 1, grain: .07 } });

// E2 — fısıltı: üç yasak (gömme, tören, adak)
shot(S('E02') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  palace(ctx, t, { dark: .88, cols: [] });
  glow(ctx, 600, 520, 600, 'rgba(255,180,100,.25)');
  // iki yakın baş (beyaz Merope, siyah Sisifos)
  // Merope sola bakar (gözleri açılır); Sisifos arkasından kulağına fısıldar
  let ear = null;
  const hear = ramp(t, Wd('E02', 'bedenimi') - .2, Wd('E02', 'bedenimi') + .4);
  figure(ctx, { x: 820, y: 1170, s: 15, dir: 1, lk: LK.merope, p: { torso: .02, neck: .02, head: .05 + hear * .05, shN: .1, shF: 0, brow: hear * .8 + ramp(t, Wd('E02', 'adak'), Wd('E02', 'adak') + .4) * .6, blink: (lt > 2.4 && lt < 2.52) ? 1 : 0 }, margin: 40,
    onJoints: (J, M) => { ear = headPt(ctx, J, M, [-1.2, -6.2]); } });
  if (ear) figure(ctx, { x: ear[0] - 372, y: ear[1] + 520, s: 15, dir: 1, lk: LK.sisKing, p: { torso: .38, neck: .25, head: .22, shN: .1, shF: 0, blink: .35, mouthOpen: Math.max(0, Math.sin(t * 9)) * .35 * (t < S('E02') + 4.1 ? 1 : 0) }, margin: 40 });
  // simgeler
  const icons = [
    [Wd('E02', 'bedenimi'), 'GÖMME', (c) => { c.fillStyle = C.ink; c.beginPath(); c.moveTo(-70, 40); c.quadraticCurveTo(0, -60, 70, 40); c.fill(); c.fillRect(-12, -70, 24, 50); c.beginPath(); c.arc(0, -72, 14, PI, TAU); c.fill(); }],
    [Wd('E02', 'tören'), 'TÖREN', (c) => { c.fillStyle = C.ink; c.fillRect(-70, 0, 140, 10); c.fillRect(-60, 10, 8, 30); c.fillRect(52, 10, 8, 30); c.beginPath(); c.ellipse(0, -10, 58, 12, 0, 0, TAU); c.fill(); for (const x of [-50, -20, 10, 40]) { c.beginPath(); c.moveTo(x, -20); c.quadraticCurveTo(x + 6, -60, x, -80); c.lineTo(x + 6, -80); c.quadraticCurveTo(x + 12, -60, x + 8, -20); c.fill(); } }],
    [Wd('E02', 'adak'), 'ADAK', (c) => { amphora(c, 0, 10, 1.4, C.ink, C.red); }],
  ];
  icons.forEach(([ti, label, draw], i) => {
    const a = ramp(t, ti - .1, ti + .35, E.outBack); if (a <= 0) return;
    const x = 1400, y = 260 + i * 250;
    ctx.save(); ctx.translate(x, y); ctx.scale(a, a);
    ctx.fillStyle = C.clayL; ctx.beginPath(); ctx.arc(0, 0, 100, 0, TAU); ctx.fill(); ctx.lineWidth = 5; ctx.strokeStyle = C.ink; ctx.stroke();
    ctx.save(); ctx.scale(.9, .9); draw(ctx); ctx.restore();
    const xs = ramp(t, ti + .4, ti + .75);
    ctx.strokeStyle = C.red; ctx.lineWidth = 14; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(-70, -70); ctx.lineTo(-70 + 140 * xs, -70 + 140 * xs); ctx.stroke();
    if (xs > .5) { const x2 = ramp(t, ti + .6, ti + .9); ctx.beginPath(); ctx.moveTo(70, -70); ctx.lineTo(70 - 140 * x2, -70 + 140 * x2); ctx.stroke(); }
    ctx.restore();
    txt(ctx, label, x + 160, y, { font: '700 40px Cinzel', col: C.white, align: 'left', ls: 6, a: a });
  });
}, { tr: { type: 'fade', dur: .4 }, post: { tex: .5, vig: 1, grain: .07 } });

// E3–E5 — Persefoni'nin huzurunda (kırmızı figür): geniş → Sisifos yakın → Persefoni & Hades → Persefoni'nin baş sallaması → ışık kapısı
function drawE3(ctx, t, c) {
  const lt = t - (S('E03') - .3), t4 = S('E04'), t5 = S('E05');
  underworld(ctx, t);
  const gy = 880, R = STY.red;
  ctx.save(); cam(ctx, c, 1);
  // ışık kapısı: zemine oturan kemerli açıklık, Sisifos'un arkasında açılır
  const g = ramp(t, t5 + .6, t5 + 1.8, E.io2);
  if (g > 0) { ctx.save(); ctx.globalAlpha = g; glow(ctx, 300, gy - 220, 520, 'rgba(255,220,150,.55)'); ctx.fillStyle = '#F6E2B4'; ctx.beginPath(); ctx.moveTo(220, gy); ctx.lineTo(220, gy - 300); ctx.quadraticCurveTo(300, gy - 430 * g, 380, gy - 300); ctx.lineTo(380, gy); ctx.closePath(); ctx.fill(); ctx.restore(); }
  throne(ctx, 1300, gy, 5.6, -1, '#C7683C', '#0B0605', { high: true });
  throne(ctx, 1620, gy, 6.0, -1, '#C7683C', '#0B0605', { high: true });
  const nod = Math.sin(clamp((t - t5) / .9) * PI * 2) * .22 * (t > t5 ? 1 : 0);
  const think = ramp(t, Wd('E04', 'izin') - .3, Wd('E04', 'izin') + .4, E.io2) * (1 - ramp(t, t5 - .2, t5 + .2));
  figure(ctx, { x: 1210, y: gy - 27 * 5.6, s: 5.6, dir: -1, sty: R, cutCol: '#0B0605', lk: LK.persephone, hold: { F: HOLD.torch() },
    p: { ...oturan(), torso: .05 + think * .1, head: .15 + nod + think * .08, shN: .3 + think * .9, elN: 1.9 + think * .6, handN: think > .5 ? 'open' : 'fist', shF: .3, elF: 1.2, smile: t > t5 ? .7 : 0, brow: think * .5, blink: (lt % 3.3 > 3.18) ? 1 : 0 } });
  figure(ctx, { x: 1520, y: gy - 27 * 6.0, s: 6.0, dir: -1, sty: R, cutCol: '#0B0605', lk: LK.hades, hold: { N: HOLD.scepter(80) },
    p: { ...oturan(), torso: .1, head: .25 + Math.sin(lt * .7) * .04 - think * .06, shN: .7, elN: .9, shF: .2, elF: 1.3, blink: (lt % 2.7 > 2.58) ? 1 : (t > t4 ? .35 : 0), brow: -.5 } });
  // Sisifos: girer, sonra el kol hareketleriyle şikâyet eder
  const enter = ramp(lt, 0, 2.2, E.io2), x = lerp(260, 640, enter);
  const rant = t > t4 && t < t5 ? 1 : 0, w = t * 7;
  if (enter < 1) walkScene(ctx, null, x, 5.6, t, 1, { noCam: true, ground: FLAT(gy), dist: x, sty: R, cutCol: '#0B0605', lk: LK.sis });
  else figure(ctx, { x, y: gy - 46.5 * 5.6, s: 5.6, sty: R, cutCol: '#0B0605', lk: LK.sis,
    p: { torso: rant * Math.sin(w * .5) * .12, neck: rant * Math.sin(w * .7) * .15, head: rant * -.1, hipN: .12, hipF: -.1,
      shN: rant ? 2.2 + Math.sin(w) * .7 : .3, elN: rant ? .5 + Math.sin(w * 1.3) * .4 : .4, shF: rant ? 1.6 + Math.cos(w * .9) * .8 : .2, elF: .6, handN: 'open', handF: 'open',
      brow: rant ? 1.4 : 0, mouthOpen: rant ? Math.max(0, Math.sin(w * 1.7)) * .8 : 0, smile: t > t5 + .4 ? 1 : 0 } });
  ctx.restore();
}
shot(S('E03') - .3, (ctx, st) => {
  drawE3(ctx, st.t, { x: 960, y: 540, z: 1 });
  nameTag(ctx, 'PERSEFONİ', 'Ölülerin kraliçesi', 140, 170, st.t - Wd('E03', 'persefoni'), 3.4, { col: '#E9C29A' });
  nameTag(ctx, 'HADES', 'Yeraltının kralı', 140, 290, st.t - S('E03') - 1.0, 3.2, { col: '#E9C29A' });
}, { tr: { type: 'clay', dur: .9 }, post: { tex: .45, vig: 1, grain: .07 } });
shot(S('E04') - .1, (ctx, st) => drawE3(ctx, st.t, { x: 700, y: 520, z: lerp(1.55, 1.65, st.p) }), { tr: { type: 'cut' }, post: { tex: .45, vig: 1, grain: .07 } });
shot(Wd('E04', 'izin') - .15, (ctx, st) => drawE3(ctx, st.t, { x: 1480, y: 600, z: lerp(1.45, 1.55, st.p) }), { tr: { type: 'cut' }, post: { tex: .45, vig: 1, grain: .07 } });
shot(S('E05') - .1, (ctx, st) => drawE3(ctx, st.t, { x: 1170, y: 520, z: lerp(2.3, 2.45, st.p) }), { tr: { type: 'cut' }, post: { tex: .45, vig: 1, grain: .07 } });
shot(S('E05') + 1.2, (ctx, st) => drawE3(ctx, st.t, { x: 860, y: 540, z: 1.05 }), { tr: { type: 'cut' }, post: { tex: .45, vig: 1, grain: .07 } });

// E6 — güneşe dönüş, şarap, deniz: "Ve geri dönmedi."
shot(S('E06') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tw = Wd('E06', 've');
  daySky(ctx, .6);
  disk(ctx, 1500, 230, 110, '#FFF0C8', 'rgba(255,230,160,.5)');
  const gy = 860;
  sea(ctx, 900, 2200, gy + 6, 3, 40, t, C.ink, '#2B1A12');
  city(ctx, 1660, gy - 4, .7, '#5A2A18', '#8E4426', 4);
  ship(ctx, 1550 + lt * 10, gy, .8, t, C.ink, C.clay);
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-50, gy); ctx.lineTo(1000, gy); ctx.quadraticCurveTo(1060, gy + 40, 1000, H); ctx.lineTo(-50, H); ctx.fill();
  const rise = ramp(lt, 0, 1.2, E.out3);
  // yer yarığı
  const crack = 1 - ramp(t, tw + .2, tw + 1.2);
  if (crack > 0) {
    ctx.save(); ctx.globalAlpha = crack;
    glow(ctx, 380, gy - 40, 260, 'rgba(255,225,160,.55)');
    ctx.strokeStyle = '#FFE6B0'; ctx.lineWidth = 7; ctx.lineJoin = 'miter'; ctx.beginPath();
    const r = rng(9); ctx.moveTo(250, gy + 4); for (let k = 1; k <= 8; k++) ctx.lineTo(250 + k * 33, gy + 4 + (r() - .5) * 14); ctx.stroke();
    for (let k = 0; k < 5; k++) { ctx.strokeStyle = `rgba(255,230,170,${.25 * crack})`; ctx.lineWidth = 16; ctx.beginPath(); ctx.moveTo(290 + k * 45, gy); ctx.lineTo(260 + k * 60, gy - 260); ctx.stroke(); }
    ctx.restore();
  }
  if (t < tw - .2) {
    const str = ramp(lt, 1.0, 2.2, E.io2);
    figure(ctx, { x: 380, y: gy - 46.5 * 5.4 + (1 - rise) * 300, s: 5.4, lk: LK.sis, alpha: clamp(rise * 2),
      p: { torso: -.1 * str, neck: -.3 * str, head: -.3 * str, shN: lerp(.5, 2.9, str), elN: .3, shF: lerp(.2, 2.6, str), elF: .3, handN: 'open', handF: 'open', smile: str, blink: str > .5 ? .8 : 0, hipN: .08, hipF: -.08 } });
  } else {
    ctx.fillStyle = '#2A1810'; ctx.beginPath(); spline(ctx, [[470, gy + 2], [488, gy - 42], [590, gy - 56], [690, gy - 40], [712, gy + 2]]); ctx.fill();
    ctx.strokeStyle = C.clayD; ctx.lineWidth = 3; ctx.beginPath(); spline(ctx, [[488, gy - 42], [590, gy - 56], [690, gy - 40]], false); ctx.stroke();
    figure(ctx, { x: 600, y: gy - 22 * 5.4, s: 5.4, lk: LK.sis, hold: { N: HOLD.kylix() },
      p: { ...oturan({ hipN: 1.5, knN: 1.2, hipF: 1.3, knF: 1.5 }), torso: -.15, neck: -.1, head: -.25, shN: 1.5 + Math.sin(lt * 2) * .05, elN: 1.4, handN: 'fist', shF: lerp(.3, -1.2, ramp(t, tw, tw + .4, E.outBack)), elF: .6, handF: 'open', smile: 1.3 } });
  }
}, { tr: { type: 'iris', dur: 1.1, x: 372, y: 670 }, post: { tex: .9, vig: .7 } });

// E7 — yıllar geçer; Hermes gelir
shot(S('E07') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, th = Wd('E07', 'hermes');
  const yrs = clamp(lt / 2.8);
  const ang = PI + (lt * .9 % 1) * PI;
  const dk = ramp(t, th - 1.2, th + 1.6);
  clayBG(ctx, mixCol('#E09A68', '#9A5232', dk), mixCol('#B85C33', '#4E2216', dk));
  if (dk < .6) { ctx.save(); ctx.globalAlpha = 1 - dk / .6; disk(ctx, W / 2 + Math.cos(ang) * 820, 860 + Math.sin(ang) * 640, 80, '#FFF0C8'); ctx.restore(); }
  const gy = 860;
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  const grab = ramp(t, th + .6, th + 1.4, E.io2);
  const down = ramp(t, th + 1.6, th + 3.2, E.in2);
  // yaşlanan Sisifos (kaya üstünde oturur)
  const old = yrs > .5;
  if (down < .05) { ctx.fillStyle = C.ink; ctx.beginPath(); spline(ctx, [[720, gy + 2], [730, gy - 96], [830, gy - 116], [900, gy - 80], [910, gy + 2]]); ctx.fill(); }
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, gy + 2); ctx.clip();
  figure(ctx, { x: 820, y: gy - 116 - lerp(14, 32, grab) * 5.4 + down * 620, s: 5.4, lk: old ? { ...LK.sis, beard: 'long', old: true } : LK.sis,
    p: grab > 0 ? { torso: -.2, neck: -.2, head: -.3, shN: 3.0, elN: .1, handN: 'open', shF: .5, elF: .4, hipN: .2, hipF: -.3, knF: .2, brow: 1.4, mouthOpen: .7 } : { ...oturan({ hipN: 1.5, knN: 1.2, hipF: 1.3, knF: 1.5 }), torso: -.1, head: -.1, shN: 1.4, elN: 1.4, handN: 'fist', blink: .3 },
    hold: grab > 0 ? null : { N: HOLD.kylix() } });
  // Hermes uçarak iner
  const hx = lerp(2100, 980, ramp(t, th - .2, th + .7, E.out3)), hy = lerp(-200, 240, ramp(t, th - .2, th + .7, E.out3)) + down * 640;
  if (t > th - .3) figure(ctx, { x: hx, y: hy, s: 5.2, dir: -1, lk: LK.hermes, hold: { F: HOLD.caduceus() },
    p: { torso: lerp(1.2, .3, grab), neck: -.4, head: -.2, hipN: -.9, knN: .9, hipF: -.6, knF: 1.3, shN: 1.9, elN: .2, handN: 'fist', shF: .7, elF: .8, brow: -.4, smile: .3 },
    ik: grab > 0 ? { hN: [820 + 10, gy - 46 * 5.4 - 46 * 5.4 * .1 - 60 + down * 520] } : {} });
  ctx.restore();
  if (yrs < 1 && t < th - .5) txt(ctx, 'yıllar…', W / 2, 160, { font: 'italic 500 56px "Cormorant Garamond"', col: C.ink, a: ramp(lt, .3, .9) * (1 - ramp(t, th - 1.2, th - .5)) });
  nameTag(ctx, 'HERMES', 'Tanrıların habercisi', 140, 160, t - th - .2, 3, { col: C.white });
}, { tr: { type: 'fade', dur: .5 }, post: { tex: .8, vig: .9 }, mb: 10 });
