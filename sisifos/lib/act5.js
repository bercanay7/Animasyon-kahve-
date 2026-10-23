// V. CEZA (Tartaros)
'use strict';
const TP = { tex: .55, vig: 1, grain: .06 };
// F1 — dev kaya düşer
shot(S('F01') - .6, (ctx, st) => {
  const t = st.t, lt = st.lt, tc = Wd('F01', 'ceza');
  const fall = ramp(t, tc - .9, tc, E.in2);
  const c = { x: 160, y: 560, z: .72 };
  const [sx, sy] = shake(t, tc, 24, 5); c.sx = sx; c.sy = sy;
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: 0 });
  ctx.save(); cam(ctx, c, 1);
  const xr = -300, R = 150, n = hillN(xr);
  const ry = lerp(-900, hillY(xr) + n[1] * R, fall);
  boulder(ctx, xr + n[0] * R, ry, R, fall * 2, { shadow: false, light: -1.2 });
  dustBurst(ctx, t, tc, xr, hillY(xr), 40, 'rgba(110,60,35,.45)', 380, 12);
  ctx.restore();
  walkScene(ctx, c, -760, 4.0, t, 1, { dist: 0, neck: -.1, head: -.2 - (1 - fall) * .3, lean: -.06 + ramp(t, tc, tc + .2) * -.1, p: { brow: 1 } });
  chapterCard(ctx, 'BÖLÜM V', 'CEZA', lt - .2, 3.0);
}, { tr: { type: 'fade', dur: .6 }, post: TP });

// F2 — tepeye doğru kaydırma ve geri
shot(S('F02') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tb = Wd('F02', 'tepenin');
  const up = ramp(lt, 0, 2.8, E.io3) * (1 - ramp(t, tb - .3, tb + 1.6, E.io3));
  const c = { x: lerp(-200, 1450, up), y: lerp(hillY(-200) - 200, 260, up), z: lerp(.85, .75, up) };
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: 0 });
  ctx.save(); cam(ctx, c, 1);
  const xr = -300, R = 150, n = hillN(xr);
  boulder(ctx, xr + n[0] * R, hillY(xr) + n[1] * R, R, 2, { shadow: false, light: -1.2 });
  ctx.restore();
  walkScene(ctx, c, -620, 4.0, t, 1, { dist: 0, neck: -.3, head: -.45 * (1 - up * .3), p: { brow: .6 } });
  txt(ctx, 'TARTAROS', W / 2 - 380, 170, { font: '700 54px Cinzel', col: '#E9C29A', ls: 16, a: ramp(lt, .3, 1) * (1 - ramp(lt, 2.4, 3)) });
}, { tr: { type: 'fade', dur: .4 }, post: TP });

// F3 — görev: kayayı zirveye
shot(S('F03') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tz = Wd('F03', 'zirveye');
  const c = { x: 500, y: 430, z: .5 };
  tartarosBG(ctx, t, c, { diskY: -40 }); // ay zirveye değmesin
  tartarosHill(ctx, c, { groove: 0 });
  // kesik yol çizgisi zirveye
  const q = ramp(t, tz - .2, tz + 1.2, E.io2);
  ctx.save(); cam(ctx, c, 1);
  ctx.setLineDash([22, 22]); ctx.strokeStyle = 'rgba(240,210,160,.85)'; ctx.lineWidth = 7;
  ctx.beginPath(); let first = true;
  for (let x = -250; x <= lerp(-250, HILL.sx, q); x += 20) { const y = hillY(x) - 18; first ? ctx.moveTo(x, y) : ctx.lineTo(x, y); first = false; } // yol yamacın üstünden zirveye
  ctx.stroke(); ctx.setLineDash([]);
  if (q > .95) txt(ctx, 'ZİRVE', HILL.sx - 560, HILL.sy - 130, { font: '700 64px Cinzel', col: '#F3E2BC', ls: 14, a: ramp(t, tz + 1, tz + 1.5) }); // ay diskinin üstüne binmez
  ctx.restore();
  pushScene(ctx, c, -300, 150, 4.0, t, { dist: -300, handsOff: 1 - ramp(lt, .1, .8), strain: .5 });
}, { tr: { type: 'fade', dur: .4 }, post: TP });

// F4 — omuz verir, iter, kayar, titrer, bir adım kala…
shot(S('F04') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, ti = Wd('F04', 'itti'), tk = Wd('F04', 'kaydı'), tt = Wd('F04', 'titredi'), tz = Wd('F04', 'zirveye');
  const slipA = ramp(t, tk - .05, tk + .2, E.out3) * (1 - ramp(t, tk + .45, tk + 1.3, E.io2));
  let xr = 1150 + ramp(t, ti - .1, tk - .2, E.io2) * 60 - slipA * 45 + ramp(t, tt + .2, tz + .6, E.io2) * 120;
  const pull = ramp(t, tz - .3, st.end, E.io3);
  const c = { x: lerp(xr - 40, xr + 120, pull), y: lerp(hillY(xr) - 160, hillY(xr) - 260, pull), z: lerp(1.25, .78, pull) };
  const tr = ramp(t, tt - .15, tt + .2) * (1 - ramp(t, st.end - .3, st.end));
  const [jx, jy] = shake(t, tk + .02, 14, 4);
  c.sx = jx + tr * noise1(t * 40, 1) * 7; c.sy = jy + tr * noise1(t * 40, 2) * 6;
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: .4 });
  ctx.save(); cam(ctx, c, 1);
  dustBurst(ctx, t, tk + .02, xr - 250, hillY(xr - 250), 26, 'rgba(120,64,36,.5)', 170, 22);
  ctx.restore();
  pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr + slipA * 45, strain: 1 + tr * .9, slip: slipA * 1.0, mouthOpen: Math.max(tr * .5, slipA * .8), T: 1.3 + tr * .08 + slipA * .18, jitter: tr * 1.1,
    rockAng: xr / 150 + tr * Math.sin(t * 30) * .015 });
}, { tr: { type: 'cut' }, post: TP, mb: 12 });

// F5 — kaya elinden kurtulur: eller kayar, Sisifos yere kapanır, kaya sırtından sekip aşar, yamaçtan gürleyerek dibe iner.
// Tek kesintisiz plan: yakın plandan kayayı izleyen kamerayla tüm yamacı gösteren geniş plana açılır.
const F5 = (() => {
  const t0 = S('F05') + .05, tc = t0 + .42, tend = Se('F05') + .3, x1 = -980;
  const ro = rockOver(1290, 150, 4.0, tc, { dist: 1330, T: 1.48, pre: .5, fly: .55, hop: 40, nb: 1 });
  const xs = ro.xd, td = ro.td, U = tend - td, v0 = 320, acc = 2 * (xs - x1 - v0 * U) / (U * U);
  // inişte ilk sekme, ardından hızlanan iniş boyunca ayrık temaslar
  const B = [{ t: td + .42, h: 34 }];
  let tb = td + .42 + .5, h = 18;
  while (tb < tend - .15) { B.push({ t: tb, h }); const gap = lerp(.48, .28, clamp((tb - td) / U)); tb += gap; h = Math.min(56, h * 1.16); }
  const xAt = t => t < td ? ro.xAt(t) : xs - v0 * (t - td) - .5 * acc * (t - td) * (t - td);
  const hopAt = t => { if (t < td) return ro.hopAt(t); for (let i = 0; i < B.length; i++) { const a = i ? B[i - 1].t : td, b = B[i].t; if (t >= a && t < b) { const v = (t - a) / (b - a); return 4 * B[i].h * v * (1 - v); } } return 0; };
  return { t0, tc, tend, xs, x1, B, xAt, hopAt, ro, td };
})();
window.F5_BOUNCES = [F5.td, ...F5.B.map(b => b.t)];
window.ROCK_OVER = Object.assign(window.ROCK_OVER || {}, { F5: F5.ro });
shot(S('F05') - .1, (ctx, st) => {
  const t = st.t, R = 150, { ro } = F5;
  const u = ramp(t, F5.t0 - .05, F5.tc, E.in2), xr = F5.xAt(t), crash = t > F5.tend;
  // kamera: yakın (kayma) → kayayı izler → sabit geniş plan ("gürleyerek")
  const fol = ramp(t, ro.tl, ro.td + .5, E.io2), wide = ramp(t, Wd('F05', 've') - .35, Wd('F05', 'gürleyerek') + .3, E.io2);
  const fx = Math.max(xr + 260, F5.x1 + 260);
  let c = { x: lerp(1290 + 120, fx, fol), y: lerp(hillY(1290) - 260, hillY(fx) - 220, fol), z: lerp(.78, .68, fol) };
  c = { x: lerp(c.x, 330, wide), y: lerp(c.y, 520, wide), z: lerp(c.z, .47, wide) };
  const pre = t < F5.tc ? 1 - ramp(t, F5.tc - .1, F5.tc) : 0;
  c.sx = pre * noise1(t * 40, 1) * 6; c.sy = pre * noise1(t * 40, 2) * 5;
  { const [sx, sy] = shake(t, F5.tend, 26, 4); c.sx += sx; c.sy += sy; }
  { const [sx, sy] = shake(t, F5.td, 12, 5); c.sx += sx; c.sy += sy; }
  for (const b of F5.B) { const [bx, by] = shake(t, b.t, 2 + b.h * .06, 7); c.sx += bx; c.sy += by; }
  tartarosBG(ctx, t, c, {}); tartarosHill(ctx, c, { groove: .4 });
  ctx.save(); cam(ctx, c, 1);
  dustBurst(ctx, t, ro.tl, ro.xl, hillY(ro.xl), 12, 'rgba(110,60,35,.4)', 110, 6);
  dustBurst(ctx, t, F5.td, F5.xs, hillY(F5.xs), 20, 'rgba(120,64,36,.45)', 170, 7);
  for (const b of F5.B) { const bx = F5.xAt(b.t); dustBurst(ctx, t, b.t, bx, hillY(bx), 9, 'rgba(110,60,35,.34)', 100, Math.floor(b.t * 10)); }
  dustBurst(ctx, t, F5.tend, F5.x1, hillY(F5.x1), 60, 'rgba(120,64,36,.55)', 520, 41);
  ctx.restore();
  const n = hillN(xr), rk = t < F5.tc ? null : [xr + n[0] * R, hillY(xr) + n[1] * R - F5.hopAt(t), xr / R - .4];
  // Sisifos: yere kapanır, dört ayak üstünde doğrulur; geniş planda ayağa kalkıp aşağı, kayaya döner
  const tStand = Wd('F05', 'en') - .1;
  if (t < tStand) {
    const pr = ro.prone(t);
    pushScene(ctx, c, 1330 - u * 40, R, 4.0, t, { dist: 1330, strain: 2, slip: 1.0, handsOff: Math.max(u, pr), mouthOpen: .8, T: 1.48,
      rockAng: (1330 - u * 40) / R - u * .4, prone: pr, rise: ro.rise(t), proneX: ro.X, rock: rk, cover: ro.cover(t), bounce: ro.bounce(t), squash: ro.squash(t) });
  } else {
    if (rk) { ctx.save(); cam(ctx, c, 1); boulder(ctx, rk[0], rk[1], R, rk[2], { shadow: false, light: -1.2 }); ctx.restore(); }
    const up = ramp(t, tStand, tStand + .9, E.io2);
    walkScene(ctx, c, ro.X + 30, 4.0, t, -1, { dist: 0, lean: lerp(.6, .15, up), neck: .3, head: .45, p: { shN: lerp(.4, 1.2, up), elN: .6, shF: lerp(.2, 2.1, up), elF: 1.0, handN: 'open', handF: 'open', brow: 1.2, mouthOpen: .55, hipN: lerp(1.0, .1, up), knN: lerp(1.6, .1, up), hipF: lerp(.6, -.1, up), knF: lerp(1.4, .1, up) } });
  }
}, { tr: { type: 'cut' }, post: TP, mb: 14 });

shot(S('F06') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, ty = Wd('F06', 'yeniden');
  if (t < ty - .2) {
    const x = lerp(700, 200, ramp(lt, 0, ty - S('F06'), E.lin));
    const c = { x: x - 60, y: hillY(x) - 200, z: .9 };
    tartarosBG(ctx, t, c, {}); tartarosHill(ctx, c, { groove: .45 });
    walkScene(ctx, c, x, 4.0, t, -1, { lean: -.04, neck: .15, head: .25, stride: 30 });
  } else {
    const xr = -470 + ramp(t, ty, st.end, E.io2) * 30;
    const c = { x: xr - 100, y: hillY(xr) - 200, z: 1 };
    tartarosBG(ctx, t, c, {}); tartarosHill(ctx, c, { groove: .45 });
    pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr, handsOff: 1 - ramp(t, ty - .1, ty + .4, E.out3) });
  }
}, { tr: { type: 'cut' }, post: TP });

// F7 — tekrar: ertesi gün, sonraki gün, yüz yıl, bin yıl
shot(S('F07') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  const b1 = Wd('F07', 'ondan'), b2 = Wd('F07', 'yüz'), b3 = Wd('F07', 'bin');
  let stage = t < b1 - .15 ? 0 : t < b2 - .15 ? 1 : t < b3 - .15 ? 2 : 3;
  const sTime = [st.t - (S('F07') - .2), t - (b1 - .15), t - (b2 - .15), t - (b3 - .15)][stage];
  const groove = [.5, .6, .8, 1][stage];
  if (stage < 2) {
    const xr = stage === 0 ? 300 + sTime * 40 : 800 + sTime * 40;
    const c = stage === 0 ? { x: xr + 80, y: hillY(xr) - 220, z: .95 } : { x: xr - 300, y: hillY(xr) - 140, z: 1.1 };
    tartarosBG(ctx, t, c, {}); tartarosHill(ctx, c, { groove });
    pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr });
    txt(ctx, ['2. GÜN', '3. GÜN'][stage], 160, 120, { font: '700 48px Cinzel', col: '#F0D2A8', ls: 10, align: 'left', a: .95, shadow: 'rgba(0,0,0,.6)', blur: 10 });
  } else if (stage === 2) {
    // yıldızlar döner; döngü hızlı
    const c = { x: 700, y: 380, z: .5 };
    tartarosBG(ctx, t, c, {});
    stars(ctx, t, 300, 17, 'rgba(255,240,210,.9)', [-400, -600, W + 800, H * 1.4], sTime * .6, [W / 2, H * .9]);
    tartarosHill(ctx, c, { groove });
    const cyc = (sTime * .9) % 1, xr = lerp(-300, 1300, cyc);
    pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr * 2 });
    txt(ctx, '100. YIL', 160, 120, { font: '700 48px Cinzel', col: '#F0D2A8', ls: 10, align: 'left', a: .95, shadow: 'rgba(0,0,0,.6)', blur: 10 });
  } else {
    // kozmik geri çekilme
    const z = lerp(.5, .12, ramp(sTime, 0, 3.2, E.io3));
    const c = { x: lerp(700, 600, ramp(sTime, 0, 3)), y: lerp(380, 700, ramp(sTime, 0, 3)), z };
    ctx.fillStyle = '#070403'; ctx.fillRect(0, 0, W, H);
    stars(ctx, t, 500, 23, 'rgba(255,240,210,.85)');
    tartarosHill(ctx, c, { groove, wide: true });
    const vg = ctx.createRadialGradient(W / 2, H / 2, H * .3, W / 2, H / 2, H * .95); vg.addColorStop(0, 'rgba(7,4,3,0)'); vg.addColorStop(1, 'rgba(7,4,3,1)'); ctx.fillStyle = vg; ctx.fillRect(0, 0, W, H);
    const cyc = (sTime * 1.8) % 1, xr = lerp(-300, 1300, cyc);
    pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr * 2 });
    txt(ctx, '1000. YIL', 160, 120, { font: '700 48px Cinzel', col: '#F0D2A8', ls: 10, align: 'left', a: .95, shadow: 'rgba(0,0,0,.6)', blur: 10 });
  }
}, { tr: { type: 'cut' }, post: TP });

// F8 — yakın plan ve alıntı
shot(S('F08') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  // Tartaros'un kızıl göğü önünde siyah figür yakın plan (tepedeki Sisifos'la aynı çizim kuralı); yavaş içeri itiş
  clayBG(ctx, '#7E3A22', '#2A120B', { x: 600, y: 380, r: 820, c: 'rgba(214,120,70,.45)' });
  const bow = ramp(t, Wd('F08', 'umutsuz') - .2, Wd('F08', 'emekten'), E.io2), shut = ramp(t, Wd('F08', 'ceza') - .1, Wd('F08', 'yoktur') + .3, E.io2);
  const blink = (lt % 2.9 > 2.78 && shut < .5) ? 1 : 0;
  ctx.save(); const z = lerp(1, 1.16, E.io2(clamp(lt / st.d))); ctx.translate(480, 760); ctx.scale(z, z); ctx.translate(-480, -760);
  figure(ctx, { x: 480, y: 1080 + bow * 10, s: 15, lk: LK.sis, p: { torso: .3 + bow * .04, neck: .15 + bow * .05, head: .12 + bow * .12, blink: Math.max(blink, .25 + shut * .75), brow: -.8 - bow * .4,
    shN: .3, shF: .1, breath: Math.sin(t * 1.5) * 1.2 }, margin: 40 });
  ctx.restore();
  quote(ctx, '“Hiçbir işe yaramayan, umutsuz bir emekten daha korkunç bir ceza yoktur.”', 1430, 500, 780, t - Wd('F08', 'hiçbir') + .2, { font: 'italic 500 66px "Cormorant Garamond"', col: '#F0DEC0', lh: 84, stagger: .6 });
}, { tr: { type: 'black', dur: .8 }, post: { tex: .4, vig: 1, grain: .07 } });
