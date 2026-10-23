// IV. İKİNCİ HİLE
'use strict';
// E1 — ölüm döşeğinde fısıltı
shot(S('E01') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt;
  // fısıltıda orta iki kişilik plana yaklaşma
  const gy = 880, tw = Wd('E01', 'kulağına'), two = ramp(t, tw - .45, tw + .45, E.io3);
  const c = { x: lerp(lerp(980, 930, st.p), 860, two), y: lerp(560, 520, two), z: lerp(lerp(1, 1.08, E.sine(st.p)), 1.9, two) };
  // oda (sütunlar, friz) .45 derinlikte: yaklaşmada figürlerden yavaş kayar, mekân derinlik kazanır
  ctx.save(); cam(ctx, { x: c.x, y: c.y, z: c.z + .06 }, .45); palace(ctx, t, { dark: .82, cols: [120, 1800] }); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  oilLamp(ctx, 1380, gy - 240, 2.4, t);
  ctx.fillStyle = C.ink; ctx.fillRect(1340, gy - 236, 80, 236);
  kline(ctx, 960, gy, 5.2, C.ink, C.clay);
  // animatör geçişi: anahtar pozlar. Sisifos döşekte, gözleri yarı kapalı; Merope'nin adını anarken gözlerini açar,
  // dirseğinin üstünde doğrulur (önce hafifçe geri çöker: hazırlık), elini Merope'nin omzuna koyar ve kulağına fısıldar.
  // Merope (E2'deki gibi sağa bakar) arkasına eğilip başını ona verir.
  const tO = Wd('E01', 'ölmeden'), tK = Wd('E01', 'karısı'), tM = Wd('E01', 'meropenin'), tE = Wd('E01', 'kulağına'), tF = Wd('E01', 'fısıldamıştı');
  const S1 = keyed(t, [
    [S('E01') - .3, { torso: -.62, neck: .3, head: .28, blink: .55, shN: .05, elN: 2.0 }],
    [tK - .1, { shN: .05, elN: 2.0 }],
    [tO, { head: .12, blink: .1 }],
    [tK - .1, { torso: -.68 }, E.io2],                       // hazırlık: geri çöker
    [tK + .45, { torso: -.4, neck: .2, head: .1 }, E.io2],   // dirseğinin üstünde doğrulur (~16 kare)
    [tM - .1, { shN: .05, elN: 2.0 }],
    [tM + .25, { torso: -.12, neck: .12, head: .06, shN: 1.35, elN: .55 }, E.io2],
    [tE + .2, { torso: -.04, neck: .05, head: .16 }],
    [tF + 1.2, { torso: -.06, head: .2 }],
  ]);
  const ms = keyed(t, [[S('E01') - .3, { torso: .02, neck: .05, head: .08, shN: .25, elN: .35, wrN: 0 }], [tE - .35, { torso: .02, neck: .05, head: .08, shN: .25, elN: .35, wrN: 0 }],
    [tE + .25, { torso: -.07, neck: -.12, head: -.08, shN: -.18, elN: 2.05, wrN: .55 }, E.outBack], [tF + 1.5, { torso: -.06, neck: -.1, head: -.05 }]]); // dinlerken eli göğsünde
  const whisper = t > tF - .1 && t < tF + 1.2 ? Math.max(0, Math.sin(t * 11)) * .45 : 0;
  // sıcak kandil ışığı Sisifos'un arkasında (siyah figür koyu duvarda kaybolmasın)
  glow(ctx, 790, 520, 420, 'rgba(255,170,90,.34)'); glow(ctx, 805, 480, 170, 'rgba(255,200,130,.28)');
  const mx = 948, my = gy - 46 * 5.0;
  let shM = null;
  // Merope'nin omuz noktası (Sisifos'un eli için) önce kuru hesaplanır
  const mPose = { ...ms, hipN: .12, hipF: -.1, shF: .15, elF: .5, handN: t > tE ? 'fist' : 'flat' }; // fısıltıyı dinlerken eli göğsünde, yumruk
  figure(ctx, { x: mx, y: my, s: 5.0, lk: LK.merope, p: mPose, alpha: 0, still: true, onJoints: (J, M) => { shM = jointPt(ctx, M, J.shoulder); } });
  figure(ctx, { x: 820, y: gy - 30 * 5.2 - 26, s: 5.2, lk: LK.sisKing, p: { ...S1, hipN: 1.6, knN: .05, hipF: 1.55, knF: .1, ankN: -.2, ankF: -.2, shF: lerp(-.9, .55, ramp(t, tK, tM)), elF: lerp(2.3, 1.6, ramp(t, tK, tM)), handN: 'open', breath: Math.sin(t * 1.1) * 1.3, mouthOpen: whisper },
    ik: shM && t > tM - .3 ? { hN: lerp2([900, gy - 300], [shM[0] - 18, shM[1] + 6], E.io2(ramp(t, tM - .3, tM + .35))) } : undefined });
  figure(ctx, { x: mx, y: my, s: 5.0, lk: LK.merope, p: mPose });
  ctx.restore();
  chapterCard(ctx, 'BÖLÜM IV', 'İKİNCİ HİLE', lt - .1, 3.0);
  nameTag(ctx, 'MEROPE', 'Sisifos\'un karısı', 140, 170, t - Wd('E01', 'merope') + .1, 3.0, { col: C.white });
}, { tr: { type: 'black', dur: .5 }, post: { tex: .6, vig: 1, grain: .07 } }); // D9b zaten iris ile kararır: "Ama"da görüntü açılmış olur

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
  // Sisifos'un arkasında sıcak ışık (siyah figür koyu duvarda kaybolmasın); başlar arasında boşluk kalır
  if (ear) glow(ctx, ear[0] - 230, ear[1] + 40, 420, 'rgba(255,170,90,.32)');
  if (ear) figure(ctx, { x: ear[0] - 600, y: ear[1] + 590, s: 15, dir: 1, lk: LK.sisKing, p: { torso: .3, neck: .1, head: -.14, shN: .1, shF: 0, blink: .3, mouthOpen: Math.max(0, Math.sin(t * 9)) * .35 * (t < S('E02') + 4.1 ? 1 : 0) }, margin: 40 });
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
}, { tr: { type: 'cut' }, post: { tex: .5, vig: 1, grain: .07 } });

// E3–E5 — Persefoni'nin huzurunda (kırmızı figür): geniş → Sisifos yakın → Persefoni & Hades → Persefoni'nin baş sallaması → ışık kapısı
function drawE3(ctx, t, c) {
  const lt = t - (S('E03') - .3), t4 = S('E04'), t5 = S('E05');
  underworld(ctx, t, { c, noFrame: true });
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
    p: { ...oturan(), torso: .05 + think * .1, head: .15 + nod + think * .08, shN: .3 + think * .9, elN: 1.9 + think * .6, handN: think > .5 ? 'open' : 'fist', shF: .3, elF: 1.2, smile: ramp(t, t5 - .1, t5 + .5, E.io2) * .7, brow: think * .5 } });
  figure(ctx, { x: 1520, y: gy - 27 * 6.0, s: 6.0, dir: -1, sty: R, cutCol: '#0B0605', lk: LK.hades, hold: { N: HOLD.scepter(80) },
    p: { ...oturan(), torso: .1, head: .25 + Math.sin(lt * .7) * .04 - think * .06, shN: .7, elN: .9, shF: .2, elF: 1.3, blink: Math.max(blinkAt(t, 41), ramp(t, t4, t4 + .6) * .35), brow: -.5 } });
  // Sisifos: girer, sonra el kol hareketleriyle şikâyet eder
  const enter = ramp(lt, 0, 2.2, E.io2), x = lerp(260, 640, enter);
  // şikâyet: el kol hareketleri yumuşakça başlar ve biter; uzak el göğsünde ("ben"), yakın kol Persefoni'ye uzanır, dirsekler bükük
  const rant = ramp(t, t4 - .15, t4 + .35, E.io2) * (1 - ramp(t, t5 - .3, t5 + .2, E.io2)), w = t * 7;
  if (enter < 1) walkScene(ctx, null, x, 5.6, t, 1, { noCam: true, ground: FLAT(gy), dist: x, sty: R, cutCol: '#0B0605', lk: LK.sis });
  else figure(ctx, { x, y: gy - 46.5 * 5.6, s: 5.6, sty: R, cutCol: '#0B0605', lk: LK.sis,
    p: { torso: rant * Math.sin(w * .5) * .12, neck: rant * Math.sin(w * .7) * .15, head: rant * -.1, hipN: .12, hipF: -.1,
      shN: lerp(.3, 1.35 + Math.sin(w) * .35, rant), elN: lerp(.4, .75 + Math.sin(w * 1.3) * .35, rant), shF: lerp(.2, .35 + Math.cos(w * .9) * .12, rant), elF: lerp(.6, 2.1, rant), wrF: rant * .4, handN: 'open', handF: 'open',
      brow: rant * 1.4, mouthOpen: rant * Math.max(0, Math.sin(w * 1.7)) * .8, smile: ramp(t, t5 + .3, t5 + .9, E.io2) } });
  ctx.restore();
  underworldFrame(ctx);
}
shot(S('E03') - .3, (ctx, st) => {
  drawE3(ctx, st.t, { x: 960, y: 540, z: 1 });
  // isimler figürlerin üstünde, anlatımdaki sırayla: önce Persefoni, sonra yanındaki Hades
  nameTag(ctx, 'PERSEFONİ', 'Ölülerin kraliçesi', 1150, 190, st.t - Wd('E03', 'ölülerin'), 3.6, { col: '#E9C29A', align: 'center' });
  nameTag(ctx, 'HADES', 'Yeraltının kralı', 1580, 190, st.t - Wd('E03', 'persefoninin') - .3, 2.4, { col: '#E9C29A', align: 'center' });
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
}, { tr: { type: 'white', dur: 1.0 }, post: { tex: .9, vig: .7 } });

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
  const grab = ramp(t, th + .55, th + 1.2, E.io2);
  const down = ramp(t, th + 1.4, th + 2.9, E.io2);
  // yerde açılan yarık: yeraltının kızıl ışığı; ikisi içine çekilir, yarık kapanır
  const gap = ramp(t, th + 1.1, th + 1.55, E.out3) * (1 - ramp(t, th + 2.85, th + 3.3, E.io2));
  if (gap > 0) {
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(ctx, 900, gy + 4, 420 * gap, `rgba(255,110,40,${.55 * gap})`);
    ctx.restore();
    // zikzaklı yarık: kenarları kor, içi karanlık
    const crack = (k, col) => { ctx.fillStyle = col; ctx.beginPath(); const n = 14;
      for (let i = 0; i <= n; i++) { const u = i / n, x = 900 + (u - .5) * 560 * gap, y = gy + 2 - (Math.sin(u * PI) * (16 + hash(i) * 14) * gap) * k; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
      for (let i = n; i >= 0; i--) { const u = i / n, x = 900 + (u - .5) * 520 * gap + (hash(i + 9) - .5) * 14, y = gy + 4 + (Math.sin(u * PI) * (10 + hash(i + 3) * 10) * gap) * k; ctx.lineTo(x, y); }
      ctx.closePath(); ctx.fill(); };
    crack(1.25, mixCol('#7A2A10', '#FF8A3A', gap)); crack(.75, '#0B0503');
  }
  // kaya hep yerinde kalır
  ctx.fillStyle = C.ink; ctx.beginPath(); spline(ctx, [[720, gy + 2], [730, gy - 96], [830, gy - 116], [900, gy - 80], [910, gy + 2]]); ctx.fill();
  const old = yrs > .5;
  // tutma noktası: Hermes Sisifos'un bileğini yakalar ve onu zorla yukarı/öne çeker
  const gP = [lerp(935, 905, grab), gy - 445 + grab * 25 + down * 560];
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, gy + 2); ctx.clip();
  // oturuştan ayağa: pozlar arasında yumuşak geçiş (sıçrama yok); kâse elinden düşer
  const seat = { ...oturan({ hipN: 1.5, knN: 1.2, hipF: 1.3, knF: 1.5 }), torso: -.1, neck: 0, head: -.1, shF: .2, elF: .4, brow: 0, mouthOpen: 0 };
  const stand = { hipN: .4, knN: .6, hipF: -.5, knF: .35, ankN: 0, ankF: 0, torso: -.38, neck: -.1, head: -.25, shF: -.9, elF: .7, brow: 1.4, mouthOpen: .7 };
  const pz = {}; for (const k in stand) pz[k] = lerp(seat[k] ?? 0, stand[k], grab);
  const hasCup = grab < .15;
  figure(ctx, { x: 820 + grab * 40, y: gy - 116 - lerp(3, 34, grab) * 5.4 + down * 540, s: 5.4, lk: old ? { ...LK.sis, beard: 'long', old: true } : LK.sis,
    p: { ...pz, shN: 1.4, elN: 1.4, handN: 'fist', handF: grab > .5 ? 'open' : 'fist', blink: .3 * (1 - grab) },
    ik: grab > 0 ? { hN: lerp2([872, gy - 330], gP, E.io2(clamp(grab * 1.4))) } : {},
    hold: hasCup ? { N: HOLD.kylix() } : null });
  // düşen kâse
  const cf = ramp(t, th + .62, th + 1.15, E.in2);
  if (cf > 0 && cf < 1.02) { ctx.save(); ctx.translate(lerp(880, 930, cf), lerp(gy - 300, gy - 8, cf)); ctx.rotate(cf * 2.4); ctx.fillStyle = C.ink;
    ctx.beginPath(); ctx.moveTo(-40, -8); ctx.quadraticCurveTo(0, 26, 40, -8); ctx.closePath(); ctx.fill(); ctx.fillRect(-5, 6, 10, 18); ctx.fillRect(-16, 22, 32, 6); ctx.restore(); }
  // Hermes uçarak iner, bileği yakalar
  const arr = ramp(t, th - .2, th + .7, E.out3);
  const hx = lerp(2100, 1060, arr) + grab * 30, hy = lerp(-200, 470, arr) + grab * 20 + down * 760;
  if (t > th - .3) figure(ctx, { x: hx, y: hy, s: 5.2, dir: -1, lk: LK.hermes, hold: { F: HOLD.caduceus() },
    p: { torso: lerp(1.2, .45, arr), neck: -.4, head: -.2, hipN: -.9, knN: .9, hipF: -.6, knF: 1.3, shN: 1.9, elN: .2, handN: 'fist', shF: .7, elF: .8, brow: -.4, smile: .1 },
    ik: arr > .5 ? { hN: grab > 0 ? gP : [lerp(1060, 960, arr), gy - 420] } : {} });
  ctx.restore();
  // yarık kapanınca karanlık
  const blk = ramp(t, th + 3.25, th + 3.65, E.io2);
  if (blk > 0) { ctx.fillStyle = `rgba(0,0,0,${blk})`; ctx.fillRect(0, 0, W, H); }
  if (yrs < 1 && t < th - .5) txt(ctx, 'yıllar…', W / 2, 160, { font: 'italic 600 72px "Cormorant Garamond"', col: C.ink, a: ramp(lt, .3, .9) * (1 - ramp(t, th - 1.2, th - .5)) });
  nameTag(ctx, 'HERMES', 'Tanrıların habercisi', 140, 160, t - th - .2, 2.5, { col: C.white });
}, { tr: { type: 'cut' }, post: { tex: .8, vig: .9 }, mb: 14 });
