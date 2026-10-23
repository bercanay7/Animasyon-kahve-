// AÇILIŞ: zincirlenen ölüm, iki hile, kaya, başlık, sorular
'use strict';
function oturan(p = {}) { return { hipN: 1.5, knN: 1.5, hipF: 1.42, knF: 1.6, ankN: 0, ankF: 0, ...p }; }

// A1 — Thanatos zincirleniyor (kırmızı figür, karanlık)
shot(0, (ctx, st) => {
  const t = st.t, tz = Wd('A01', 'zincire'), snap = tz + .32;
  ctx.fillStyle = '#0B0605'; ctx.fillRect(0, 0, W, H);
  const c = { x: 960, y: 520, z: lerp(.86, .96, E.sine(st.p)) };
  const [shx, shy] = shake(t, snap, 16, 7);
  c.sx = shx; c.sy = shy;
  ctx.save(); cam(ctx, c, 1);
  glow(ctx, 960, 520, 820, 'rgba(150,60,25,.38)');
  motes(ctx, t, 70, 4, '#E08A4A', [0, 0, W, H], 30, 2, .55);
  // zemin çizgisi
  ctx.fillStyle = '#1A0E0A'; ctx.fillRect(-200, 905, W + 400, 400);
  ctx.fillStyle = C.clayD; ctx.fillRect(-200, 903, W + 400, 3);
  let wr = null;
  const pull = ramp(t, snap, snap + .7, E.out3);
  const jerk = Math.sin(clamp((t - snap) / .6) * PI * 3) * Math.exp(-(t - snap) * 4) * (t > snap ? 1 : 0);
  const S7 = 6.2, gx = 900, gy = 905;
  const stand = { torso: .12, neck: 0, head: .1, hipN: .25, knN: .15, hipF: -.25, knF: .1, ankN: 0, ankF: 0 };
  const kneel = { torso: .22, neck: .2, head: .35, hipN: 1.35, knN: 1.45, hipF: -.05, knF: 1.62, ankN: 0, ankF: -1.4 };
  const P = mix(stand, kneel, pull);
  const pelY = gy - lerp(46.5, 25.5, pull) * S7;
  figure(ctx, {
    x: gx + pull * 30, y: pelY, s: S7, sty: STY.red, cutCol: '#0B0605', lk: LK.thanatos,
    p: { ...P, wingF: t * .5, wingSpread: .8 + jerk * .2 - pull * .25, handN: 'fist', handF: 'fist', brow: -1, mouthOpen: jerk > .2 ? .8 : 0 },
    ik: { hN: [gx + lerp(330, 190, pull) + jerk * 14, lerp(430, 650, pull)], hF: [gx + lerp(300, 175, pull) + jerk * 14, lerp(470, 665, pull)] },
    onJoints: (J, M) => { const a = M.transformPoint(new DOMPoint(...J.AN.wr)), b = M.transformPoint(new DOMPoint(...J.AF.wr)); const inv = ctx.getTransform().inverse(); const pa = inv.transformPoint(a), pb = inv.transformPoint(b); wr = [[pa.x, pa.y], [pb.x, pb.y]]; },
    margin: 110,
  });
  // zincirler: kenarlardan bileklere uçar
  const fly = ramp(t, tz - .25, snap, E.in2);
  if (wr && fly > 0) {
    // zincir yukarıdan iner, sonra yere çivili halkalara gerilir
    for (const [k, from, anchor] of [[0, [W + 200, 120], [1460, 905]], [1, [-200, 140], [520, 905]]]) {
      const src = lerp2(from, anchor, pull);
      const end = lerp2(src, wr[k], fly);
      const mid = [lerp(src[0], end[0], .5), lerp(src[1], end[1], .5) + 90 * (1 - pull) * (1 - fly * .6)];
      chain(ctx, [src, mid, end], 28, '#E1B07A', '#5A2A16', 7);
      if (t > snap) shackle(ctx, wr[k][0], wr[k][1], 18, k ? -.3 : .3, '#E1B07A');
      if (pull > .05) { ctx.fillStyle = '#E1B07A'; ctx.beginPath(); ctx.arc(anchor[0], anchor[1] - 6, 14, PI, TAU); ctx.fill(); }
    }
  }
  ctx.restore();
  // çarpma parlaması
  const fl = clamp(1 - (t - snap) / .35) * (t > snap ? 1 : 0);
  if (fl > 0) { ctx.save(); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgba(255,210,150,${fl * .5})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}, { post: { tex: .5, vig: 1, grain: .07 } });

// A2 — iki hile: iki vazo panosu
shot(S('A02') - .12, (ctx, st) => {
  const t = st.t, t1 = Wd('A02', 'bir'), t2 = Wd('A02', 'iki');
  clayBG(ctx, C.clayL, C.clayD);
  friezeFrame(ctx, { h: 44 });
  const panel = (k, x, y, w, h, tin, draw) => {
    const q = ramp(t, tin - .15, tin + .45, E.outBack);
    if (q <= 0) return;
    ctx.save(); ctx.translate(x, y); ctx.scale(lerp(.85, 1, q), lerp(.85, 1, q)); ctx.globalAlpha = clamp(q * 1.4);
    ctx.fillStyle = C.clayL; ctx.fillRect(-w / 2, -h / 2, w, h);
    ctx.save(); ctx.beginPath(); ctx.rect(-w / 2, -h / 2, w, h); ctx.clip(); draw(ctx, w, h); ctx.restore();
    ctx.lineWidth = 6; ctx.strokeStyle = C.ink; ctx.strokeRect(-w / 2, -h / 2, w, h);
    meander(ctx, -w / 2, w / 2, -h / 2 - 40, 36, C.ink);
    txt(ctx, k, 0, h / 2 + 56, { font: '700 44px Cinzel', col: C.ink, ls: 8 });
    ctx.restore();
  };
  const lt = st.lt;
  // iki pano da kırmızı figür (ölüm ve yeraltı kuralı): siyah zemin, kil renkli figürler
  const RF = { sty: STY.red, cutCol: C.ink };
  panel('I', 520, 520, 700, 520, t1, (c, w, h) => {
    c.fillStyle = C.ink; c.fillRect(-w / 2, -h / 2, w, h);
    c.fillStyle = '#C7683C'; c.fillRect(-w / 2, 200, w, 4);
    column(c, 40, -200, 200, 46, '#C7683C', C.ink);
    figure(c, { x: 60, y: 200 - 40 * 4.2, s: 4.2, dir: -1, lk: LK.thanatos, ...RF, p: { ...oturan({ hipN: 1.2, knN: 1.9, hipF: 1.1, knF: 2.0 }), torso: .25, head: .3, shN: .2, elN: 1.4, shF: .1, elF: 1.5, handN: 'fist', handF: 'fist', wingSpread: .25 } });
    chain(c, [[30, 10], [10, 60], [-20, 40]], 16, '#E1B07A', '#5A2A16', 4);
    figure(c, { x: -170, y: 200 - 47 * 4.2, s: 4.2, lk: LK.sisKing, ...RF, p: { shN: .9 + Math.sin(lt * 3) * .1, elN: .6, shF: -.1, elF: .4, smile: 1, hipN: .05, hipF: -.05, handN: 'fist' }, hold: { N: HOLD.key() } });
  });
  panel('II', 1400, 520, 700, 520, t2, (c, w, h) => {
    c.fillStyle = C.ink; c.fillRect(-w / 2, -h / 2, w, h);
    c.fillStyle = '#C7683C'; c.fillRect(-w / 2, 200, w, 4);
    glow(c, 250, 40, 260, 'rgba(255,236,190,.6)');
    c.fillStyle = '#F6E6C0'; c.beginPath(); c.moveTo(190, 200); c.lineTo(190, -60); c.quadraticCurveTo(250, -150, 310, -60); c.lineTo(310, 200); c.fill();
    throne(c, -250, 200, 4.2, 1, '#C7683C', C.ink, { high: true });
    figure(c, { x: -228, y: 200 - 27 * 4.2, s: 4.2, lk: LK.persephone, ...RF, p: { ...oturan(), shN: .9, elN: .5, shF: .2, elF: 1.2, head: .1 } });
    const wx = 40 + lt * 30;
    figure(c, { x: wx, y: 200 - 46 * 4.2, s: 4.2, lk: LK.sis, ...RF, p: { torso: .06, shN: Math.sin(lt * 5) * .4, elN: .3, shF: -Math.sin(lt * 5) * .4 - .3, elF: .2, hipN: Math.sin(lt * 5) * .35, knN: .3 + Math.max(0, Math.cos(lt * 5)) * .5, hipF: -Math.sin(lt * 5) * .35, knF: .3 + Math.max(0, -Math.cos(lt * 5)) * .5, smile: 1, head: -.1 } });
  });
}, { tr: { type: 'fade', dur: .35 }, post: { tex: .9, vig: .8 } });

// A3 — Tartaros, geniş plan: itiyor
shot(S('A03') - .35, (ctx, st) => {
  const t = st.t, xr = 820 + st.lt * 22;
  const c = { x: lerp(760, 820, E.sine(st.p)), y: lerp(430, 400, E.sine(st.p)), z: lerp(.52, .6, E.sine(st.p)) };
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: .4 });
  ctx.save(); cam(ctx, c, 1); dustBurst(ctx, t, t - 1, xr - 200, hillY(xr - 200), 6, 'rgba(90,50,30,.18)', 60, Math.floor(t)); ctx.restore();
  pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr });
  motes(ctx, t, 40, 8, 'rgba(240,170,110,.6)', [0, 0, W, H], 14, 1.6, .5);
}, { tr: { type: 'fade', dur: .6 }, post: { tex: .55, vig: 1, grain: .06 } });

// A4 — zirveye yakın: kaya sallanır, ayaklar kayar; kaya geri kaçar, Sisifos yere kapanır, kaya sırtından sekerek aşar
const A4 = (() => { const t0 = S('A04') - .2, tg = Wd('A04', 'geri') - .05; const pushAt = t => 1180 + (Math.min(t, tg) - t0) * 26;
  return { t0, tg, pushAt, ro: rockOver(pushAt(tg) - 16, 150, 4.0, tg, { pre: .34, fly: .44, hop: 88 }) }; })();
window.ROCK_OVER = { A4: A4.ro };
shot(S('A04') - .2, (ctx, st) => {
  const t = st.t, { tg, ro } = A4, R = 150, pushX = A4.pushAt(t);
  const ant = ramp(t, tg - .6, tg, E.in2) * (1 - ramp(t, tg, tg + .2));
  const rx = ro.xAt(t), fol = ramp(t, ro.tl, ro.td + .9, E.io2);
  const c = { x: lerp(1080, Math.max(rx + 380, -200), fol), y: lerp(hillY(1080) - 120, hillY(Math.max(rx + 380, -200)) - 170, fol), z: lerp(.9, .66, ramp(t, tg, ro.td + .6, E.io2)) };
  c.sx = ant * noise1(t * 40, 1) * 7; c.sy = ant * noise1(t * 40, 2) * 4;
  for (const tb of ro.bounces) { const [bx, by] = shake(t, tb, tb === ro.td ? 12 : 5, 5); c.sx += bx; c.sy += by; }
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: .4 });
  ctx.save(); cam(ctx, c, 1);
  dustBurst(ctx, t, tg - .35, pushX - 230, hillY(pushX - 230), 10, 'rgba(110,60,35,.4)', 90, 5);
  dustBurst(ctx, t, ro.tl, ro.xl, hillY(ro.xl), 12, 'rgba(110,60,35,.4)', 110, 6);
  for (const tb of ro.bounces) { const bx = ro.xAt(tb); dustBurst(ctx, t, tb, bx, hillY(bx), tb === ro.td ? 18 : 8, 'rgba(110,60,35,.38)', tb === ro.td ? 150 : 80, Math.floor(tb * 10)); }
  ctx.restore();
  const pr = ro.prone(t), rk = t < tg ? null : ro.rockAt(t);
  pushScene(ctx, c, pushX - ant * 16, R, 4.0, t, { dist: pushX, strain: 1 + ant * .9, slip: ant, mouthOpen: Math.max(ant * .6, pr * .5 * (1 - ro.rise(t))),
    handsOff: pr, prone: pr, rise: ro.rise(t), proneX: ro.X, rock: rk, cover: ro.cover(t), bounce: ro.bounce(t),
    rockAng: pushX / R - ant * .1 + Math.sin(t * 34) * .025 * ant, T: 1.3 + Math.sin(t * 40) * .02 * ant });
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 }, mb: 14 });

shot(Wd('A04', 'aşağı') - .1, (ctx, st) => {
  const t = st.t;
  const x = lerp(1050, 700, st.lt / 3);
  const c = { x: x - 80, y: hillY(x) - 200, z: .85 };
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: .4 });
  walkScene(ctx, c, x, 4.0, t, -1, { lean: -.05, neck: .1, head: .2, p: { brow: 0 }, stride: 30 });
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

shot(Wd('A04', 'yeniden') - .15, (ctx, st) => {
  const t = st.t;
  const xr = -240 + ramp(st.lt, .5, 2.5, E.io2) * 40;
  const c = { x: xr - 120, y: hillY(xr) - 220, z: .85 };
  tartarosBG(ctx, t, c, {});
  tartarosHill(ctx, c, { groove: .4 });
  pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr, handsOff: 1 - ramp(st.lt, 0, .45, E.out3) });
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// A5 — BAŞLIK
shot(S('A05') - .6, (ctx, st) => {
  const t = st.t, lt = st.lt, tw = Wd('A05', 'sisifos');
  clayBG(ctx, '#D9895A', '#A9532E');
  friezeFrame(ctx, { h: 48, alpha: ramp(lt, 0, .6) });
  // vinyet: tepe ve itme (vazo panosu gibi)
  const vy = 560, x0 = W / 2 - 600, sx = W / 2 + 330, x1 = W / 2 + 600;
  const vf = x => x < x0 ? vy : x < sx ? vy - 250 * Math.pow(smooth((x - x0) / (sx - x0)), 1.15) : vy - 250 + 250 * Math.min(1, Math.pow((x - sx) / (x1 - sx), 2));
  const vg = groundOf(vf);
  ctx.save();
  const rev = ramp(lt, .1, 1.1, E.io3);
  ctx.globalAlpha = rev; // dikdörtgen perde yerine yumuşak beliriş
  ctx.fillStyle = C.ink;
  ctx.beginPath(); ctx.moveTo(x0 - 40, vy + 6); for (let x = x0 - 40; x <= x1 + 40; x += 6) ctx.lineTo(x, vf(x)); ctx.lineTo(x1 + 40, vy + 6); ctx.closePath(); ctx.fill();
  ctx.fillRect(x0 - 40, vy, x1 - x0 + 80, 6);
  const xr = W / 2 + 40 + lt * 9;
  pushScene(ctx, null, xr, 64, 2.0, t, { noCam: true, ground: vg, dist: xr, cutCol: '#C46A3E', light: -2.2 });
  ctx.restore();
  // başlık harfleri
  const q = clamp((t - tw + .1) / 1.1);
  txtReveal(ctx, 'SİSİFOS', W / 2, 740, q, { font: '900 168px Cinzel', col: C.ink, ls: 26, rise: 30 });
  const sq = ramp(lt, 1.6, 2.6);
  txt(ctx, 'Tanrıları kandıran adam', W / 2, 860, { font: 'italic 500 52px "Cormorant Garamond"', col: C.ink, a: sq });
  ctx.fillStyle = C.ink; const lw = 300 * E.out3(sq); ctx.fillRect(W / 2 - lw, 812, lw * 2, 3);
}, { tr: { type: 'black', dur: .7 }, post: { tex: .95, vig: .7 }, mb: 12 });

// A6 — Olimpos: neden bu ceza? / binlerce yıl sonra bir düşünür
shot(S('A06') - .25, (ctx, st) => {
  const t = st.t, lt = st.lt;
  clayBG(ctx, C.clayL, C.clayD);
  const c = { x: lerp(1000, 920, E.sine(st.p)), y: 560, z: lerp(1.0, 1.06, st.p) };
  ctx.save(); cam(ctx, c, 1);
  const gy = 860;
  ctx.fillStyle = C.ink; ctx.fillRect(-200, gy, W + 400, 6);
  for (const cx of [120, 1800]) column(ctx, cx, 150, gy, 60);
  // tanrılar sırası (oturan)
  const gods = [
    { x: 270, lk: LK.hermes, hold: { N: HOLD.caduceus() }, d: 1 },
    { x: 610, lk: LK.ares, hold: { N: HOLD.spear(90) }, d: 1 },
    { x: 960, lk: LK.zeus, hold: { N: HOLD.bolt(), F: HOLD.scepter(80) }, d: 1, big: 1.2 },
    { x: 1340, lk: LK.persephone, hold: { N: HOLD.torch() }, d: -1 },
    { x: 1680, lk: LK.hades, hold: { N: HOLD.scepter(70) }, d: -1 },
  ];
  for (const g of gods) {
    const s = 4.1 * (g.big || 1);
    throne(ctx, g.x - 16 * s * g.d, gy, s, g.d, C.ink, C.clayL, { high: !!g.big });
    figure(ctx, { x: g.x, y: gy - 27 * s, s, dir: g.d, lk: g.lk, hold: g.hold,
      p: { ...oturan(), torso: .05, head: .25 + Math.sin(t * .8 + g.x) * .04, shN: .35, elN: 1.25, shF: .2, elF: 1.4, handN: 'fist', brow: g.big ? -1 : -.3, blink: (Math.sin(t * 1.3 + g.x) > .97) ? 1 : 0 } });
  }
  // gök gürültüsü: Zeus yıldırımı parlar
  ctx.restore();
  txt(ctx, 'NEDEN?', W / 2, 150, { font: '700 64px Cinzel', col: C.ink, ls: 14, a: ramp(lt, .5, 1.2) * (1 - ramp(t, Wd('A06', 'binlerce') - .6, Wd('A06', 'binlerce') - .2)) });
}, { tr: { type: 'clay', dur: .8 }, post: { tex: .9, vig: .8 } });

shot(Wd('A06', 'binlerce') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  // beyaz zemin: 1942, yazan bir düşünür
  ctx.fillStyle = C.paper; ctx.fillRect(0, 0, W, H);
  const gy = 860;
  ctx.fillStyle = C.inkSoft; ctx.fillRect(0, gy, W, 4);
  // masa ve daktilo yerine kâğıt
  ctx.fillStyle = C.inkSoft;
  ctx.fillRect(740, gy - 200, 560, 14); ctx.fillRect(770, gy - 190, 12, 190); ctx.fillRect(1260, gy - 190, 12, 190);
  // masada kâğıt destesi, kitaplar ve lamba
  ctx.fillStyle = '#FFFBF0'; ctx.beginPath(); ctx.moveTo(790, gy - 200); ctx.lineTo(1010, gy - 200); ctx.lineTo(990, gy - 212); ctx.lineTo(810, gy - 212); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = C.inkSoft; ctx.lineWidth = 2; ctx.stroke();
  for (let k = 0; k < 3; k++) { ctx.fillStyle = k % 2 ? '#8E2F1F' : C.inkSoft; ctx.fillRect(1120 - k * 6, gy - 214 - k * 22, 120 + k * 10, 20); }
  ctx.fillStyle = C.inkSoft; ctx.fillRect(1220, gy - 340, 8, 140); ctx.beginPath(); ctx.moveTo(1180, gy - 330); ctx.lineTo(1270, gy - 330); ctx.lineTo(1250, gy - 380); ctx.lineTo(1200, gy - 380); ctx.closePath(); ctx.fill();
  glow(ctx, 1225, gy - 300, 260, 'rgba(255,235,190,.35)');
  throne(ctx, 650, gy, 5, 1, C.inkSoft, C.paper, { stool: false });
  // yazan el kâğıt üzerinde satır satır ilerler
  const wx = 830 + ((lt * 40) % 100), wy = gy - 214 - Math.abs(Math.sin(t * 17)) * 4;
  let cigP = null;
  // masaya yakın oturur: yazan el kâğıtta (dirsek bükük), sigaralı el çenesinde; duman sigaranın ucundan yükselir
  const puff = ramp(lt % 4.2, 3.2, 3.6, E.io2) * (1 - ramp(lt % 4.2, 3.7, 4.1, E.io2));
  figure(ctx, { x: 728, y: gy - 27 * 5, s: 5, sty: STY.white, lk: LK.camus, hold: { N: HOLD.pen(), F: HOLD.cig() },
    p: { ...oturan({ hipN: 1.45, knN: 1.4 }), torso: .4, neck: .12, head: .22 - puff * .12, handN: 'fist', handF: 'fist', blink: (Math.sin(t * 2.1) > .96) ? 1 : 0 },
    ik: { hN: [wx, wy], hF: [lerp(892, 870, puff), lerp(gy - 300, gy - 322, puff)] },
    onJoints: (J, M) => { const tp = add(J.AF.wr, rot([6.6, 4.05], -J.AF.haA)), q = M.transformPoint(new DOMPoint(tp[0], tp[1])); const r = ctx.getTransform().inverse().transformPoint(q); cigP = [r.x, r.y]; } });
  // sigara dumanı: sigaranın ucundan
  if (cigP) { ctx.save(); ctx.strokeStyle = 'rgba(40,30,25,.32)'; ctx.lineWidth = 2;
    ctx.beginPath(); for (let k = 0; k < 40; k++) { const u = k / 39, x = cigP[0] + Math.sin(u * 7 + t * 1.4) * 16 * u, y = cigP[1] - u * 240; k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); ctx.restore(); }
  // havada beliren el yazısı
  txtReveal(ctx, 'mutlu?', 1250, 360, ramp(st.t, Wd('A06', 'neden', 1) - .45, Wd('A06', 'mutlu') + .3, E.lin), { font: 'italic 600 150px "Cormorant Garamond"', col: C.inkSoft, rise: 10 });
  txt(ctx, '1942', 1600, 560, { font: '600 40px "Courier Prime"', col: C.inkSoft, a: ramp(lt, 1.2, 2) });
}, { tr: { type: 'white', dur: .5 }, post: { tex: .35, vig: .55, grain: .05 } });
