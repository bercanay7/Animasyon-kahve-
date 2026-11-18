// HAVUZ ortak sahne kurucuları (52 plan, iki sahip). ORTAK DOSYA: yalnız başkan değiştirir; sahipler çağırır, kopyalayıp kendi set dosyalarında değiştirebilir.
// Kapı planları B (geniş pınar), C (orta: kıyıda uzanmış genç), D (yakın: yüz ve yansıması, gözyaşı halkası, tanıma hamlesi) kapı kodundan ayrıldı.
// Sabit saniye yok: bütün zamanlar çağırandan (A('E04@benim'), Wd('D03', 'âşık') …) gelir. Kamera [fx, fy, z] verilmezse kapıdaki kadraj.
'use strict';

// ---------------- geniş: orman kenarında pınar (kapı B) ----------------
// o: {cam: [fx,fy,z], fig: c => {…} (figür çizimi; yansıtılır), trees (true), nerg (nergis listesi [[x, seed, h]…]), refA (.4), pc, prx, pry, gy}
function havuzGenis(ctx, t, o = {}) {
  baseT(ctx);
  glaze(ctx, 1250, 900, 1200, 'rgba(120,48,22,.42)');
  const cam = o.cam || [980, 560, 1.0]; camAt(ctx, ...cam);
  const gy = o.gy ?? 760, pc = o.pc || [1290, 812], prx = o.prx ?? 380, pry = o.pry ?? 58;
  const trees = c => { if (o.trees === false) return;
    vaseTree(c, 150, gy, 1.75, 3, t, { branches: 7, reach: 110 }); vaseTree(c, 1720, gy, 1.9, 8, t, { branches: 7, reach: 120 });
    vaseTree(c, 1900, gy, 1.45, 5, t, { branches: 6 }); vaseTree(c, 1010, gy, 1.05, 11, t, { branches: 5, reach: 70 }); };
  const NL = o.nerg || [[1560, 5, 58], [1610, 8, 46], [1655, 2, 54], [975, 11, 50]];
  const nerg = c => { for (const [x, sd, h] of NL) narcissus(c, x, gy, 1.35, t, sd, { dir: x > pc[0] ? -1 : 1, h }); };
  const pool = c => c.ellipse(pc[0], pc[1], prx, pry, 0, 0, TAU);
  groundBand(ctx, gy);
  for (let i = 0; i < 9; i++) grass(ctx, 80 + i * 230 + (i % 2) * 70, gy + 2, 1.5, t, i + 3);
  ctx.save(); ctx.beginPath(); pool(ctx); ctx.fillStyle = '#050302'; ctx.fill(); ctx.restore();
  waterBody(ctx, pool, pc[1] - pry, t, { a: .22, seed: 9, span: [pc[0] - prx, pc[0] + prx - 120], n: 12, depth: pry * 1.6 });
  mirror(ctx, c => { trees(c); nerg(c); if (o.fig) o.fig(c); }, gy, pool, t, { a: o.refA ?? .4, calm: .8, rings: o.rings });
  ctx.save(); ctx.beginPath(); pool(ctx); ctx.lineWidth = 4; ctx.strokeStyle = PC.clayR; ctx.stroke(); ctx.restore();
  crag(ctx, [[pc[0] - prx - 70, gy + 4], [pc[0] - prx + 10, gy - 34], [pc[0] - prx + 80, gy - 30], [pc[0] - prx + 120, gy + 8]], { fill: '#5A2C16', seed: 4, wob: 4, strata: 2, lobes: 1 });
  trees(ctx); nerg(ctx); if (o.fig) o.fig(ctx);
  if (o.meander !== false) { ctx.save(); baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze); ctx.restore(); }
  return { gy, pc, prx, pry };
}
// pınara yürüyen avcı (kapı B): x0 → x1, tStop'ta durur, tLean'de eğilir. havuzGenis({fig: c => avciYuru(c, t, {...})})
function avciYuru(c, t, o) {
  const { tA, tStop, tLean0, tLean1 } = o, gy = o.gy ?? 760, s = o.s ?? 4.4, x0 = o.x0 ?? 260, x1 = o.x1 ?? 850;
  const stand = ramp(t, tStop - .3, tStop + .25, E.io2), xw = lerp(x0, x1, E.out2(clamp((t - tA) / (tStop - tA))));
  const lean = tLean0 != null ? ramp(t, tLean0, tLean1 + .3, E.io2) : 0;
  let J = null, M = null;
  walkScene(c, null, xw, s, t, 1, { ground: groundOf(() => gy), noCam: true, sty: STY.red, lk: LK_NK, dist: (xw - x0), stand, stripe: .5, lean: .06 + lean * .12, neck: lean * .25, head: lean * .35, onJoints: (j, m) => { J = j; M = m; }, p: { shF: -.55 + .15 * stand, elF: -.2 } });
  if (o.spear !== false && J) spear(c, jointPt(c, M, J.AF.wr), -1.2, 62 * s, s * .9);
}

// ---------------- orta: kıyıda uzanmış genç, dirsekleri kayada, başı suyun üstünde (kapı C) ----------------
// o: {cam, look (0..1 baş suya), reach (0..1 yakın el suya), smile, lag (yansıma gecikmesi sn; varsayılan refLag(t)), refA (.42), bank (karşı kıyı nergisleri), light (.3)}
const KIYI = { wy: 640, gy: 618, xe: 980, s: 6.0 };
function kiyiFig(t, o = {}) {
  const { wy, gy, xe, s } = KIYI, px = xe - 30 * s, look = o.look || 0, reach = o.reach || 0;
  const grip = [xe - 12, gy - .6];
  const hN = [lerp(grip[0] + 4, xe + 40, reach), lerp(grip[1], wy - 34, reach)];
  return { f: proneFig(px, gy, s, { ...pPose({ head: .08 * look, neck: .04 * look, handN: reach > .3 ? 'open' : 'flat', smile: o.smile ?? .25 * reach }), hemPerp: true, hemT: .62 }, { hN, hF: [grip[0] - 9, grip[1]], flatFeet: -2.9 }), aN: lerp(.12, .42, reach) };
}
function kiyiOrta(ctx, t, o = {}) {
  baseT(ctx);
  glaze(ctx, 1150, 900, 1150, 'rgba(130,52,24,.5)');
  camAt(ctx, ...(o.cam || [890, 610, 1.56]));
  const { wy, gy, xe, s } = KIYI, px = xe - 30 * s;
  const mk = tt => { const { f, aN } = kiyiFig(tt, typeof o.pose === 'function' ? o.pose(tt) : o); const { J } = joints(ctx, f); f.p = { ...f.p, wrN: aN - J.AN.foA, wrF: .12 - J.AF.foA }; return f; };
  const f = mk(t), lag = o.lag ?? refLag(t), fR = lag ? mk(t - lag) : f;
  const water = c => c.rect(xe - 10, wy, 4000, 2000);
  waterBody(ctx, water, wy, t, { a: .2, seed: 5, span: [xe, 2300], n: 28, depth: 380 });
  const bank = c => { if (o.bank !== false) for (const [x, sd, h] of [[1290, 5, 60], [1318, 8, 48], [1350, 2, 56]]) narcissus(c, x, wy - 14, .62, t, sd, { dir: -1, h }); };
  mirror(ctx, bank, wy, c => c.rect(1150, wy, 4000, 2000), t, { a: .45, calm: 1.1 });
  mirror(ctx, c => withFigT(t - lag, () => figure(c, fR)), wy, water, t, { a: o.refA ?? .42, calm: 1.1, rings: o.rings });
  farBank(ctx, 1180, 2600, wy, t, 17, { h: 22, grass: 7, fill: '#3A1B0D' }); bank(ctx);
  ledge(ctx, xe, gy, wy);
  for (let i = 0; i < 5; i++) { const gx = 120 + i * 160; if (gx > px - 50 * s && gx < xe) continue; grass(ctx, gx, gy + 2, 1.6, t, i + 11); }
  litFigure(ctx, f, { x: xe + 80, y: wy + 40, r: 520, c: 'rgba(255,205,150,A)', a: o.light ?? .3 });
  shoreLine(ctx, xe - 10, wy, { w: 2.6 });
  if (o.meander !== false) { ctx.save(); baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze); ctx.restore(); }
  return { f, wy };
}

// ---------------- yakın: yüz ve yansıması (kapı D: tanıma hamlesi, gözyaşı halkası) ----------------
// Zamanlar T = {son (el kalkar), ben (parmaklar buluşur; A('E04@benim')), tear (gözyaşı belirir), hit (suya değer), lean0 (eğilme başı), sad1 (hüzün oturur)}.
// Verilmeyen olay olmaz: T.ben yoksa el dinlenir; T.hit yoksa damla ve halka yok (gözyaşı halkası yalnız P062).
const D_WY = 630, D_GAP = 40, D_S = 26, D_XE = 640;
const D_TOUCH = { tip: [800, 630] }, D_REST = { w: [300, 590], a: 1.62, hand: 'flat' };
function dReach(t, T) {
  if (T.ben == null || T.son == null) return { ...D_REST, k: 0 };
  const son = T.son, ben = T.ben, tTouch = ben - .3, tBack = ben + .45;
  const rest = D_REST, mid = { w: [455, 545], a: 1.05, hand: 'point' }, touch = { w: [600, 520], a: 1.068, hand: 'point' };
  const t0 = son - .25, tm = t0 + .5;
  const mix = (P, Q, u) => ({ w: lerp2(P.w, Q.w, u), a: lerp(P.a, Q.a, u), hand: u < .35 ? P.hand : Q.hand });
  if (t < t0) return { ...rest, k: 0 };
  if (t < tm) return { ...mix(rest, mid, E.in2(clamp((t - t0) / (tm - t0)))), k: 1 };
  if (t < tTouch) return { ...mix(mid, touch, E.out2(clamp((t - tm) / (tTouch - tm)))), k: 2 };
  if (t < tBack) return { ...touch, k: 3 };
  if (t < tBack + .5) return { ...mix(touch, mid, E.io2(clamp((t - tBack) / .5))), k: 4 };
  return { ...mix(mid, rest, E.io2(clamp((t - tBack - .5) / .5))), k: 5 };
}
function dPoseO(t, T) {
  const big = 1e9, ben = T.ben ?? big, son = T.son ?? big, tear = T.tear ?? big;
  const lean0 = T.lean0 != null ? ramp(t, T.lean0, T.lean0 + .8, E.io2) * .04 : 0;
  const flinch = settle(t, tear + .05, .05, 1.2, 2.2);
  const leanIn = ramp(t, son, ben - .05, E.io2) * .05 * (1 - ramp(t, ben, ben + .35, E.out3));
  const recoil = ramp(t, ben - .02, ben + .22, E.out3) * .34 * (1 - .45 * ramp(t, ben + .5, ben + 1.4, E.io2));
  const sad = T.sad1 != null ? ramp(t, ben + .6, T.sad1, E.io2) : ramp(t, ben + .6, ben + 1.4, E.io2);
  const up = ramp(t, ben - .02, ben + .15, E.out3);
  return { neck: lean0 + leanIn * .5 - recoil * .6, head: lean0 + flinch + leanIn - recoil * .5,
    smile: -.2 - .3 * sad, brow: .3 + 1.1 * up - .45 * sad, mouthOpen: 2.1 * ramp(t, ben - .02, ben + .18, E.out3) * (1 - .6 * sad), browUp: .5 * up * (1 - .7 * sad),
    eyeWide: .55 * ramp(t, ben - .02, ben + .12, E.out3) * (1 - .8 * sad), blink: t > ben - .02 && t < ben + .12 ? 0 : undefined };
}
function dFig(ctx, t, NT, T, o = {}) {
  const s = D_S, gy = NT[1] - D_GAP + .2 * s, px = NT[0] - 30 * s;
  const q = o.pose ? o.pose(t) : dPoseO(t, T), pp = pPose(q);
  pp.neck = 1.0 + q.neck; pp.head = -.9 + q.head;
  const R = o.handOff ? { w: [140, 600], a: 1.62, hand: 'flat' } : dReach(t, T);
  pp.handN = R.hand; pp.handF = 'flat';
  const hN = [R.w[0] + (NT[0] - D_XE), R.w[1] + (NT[1] - D_WY)];
  const f = proneFig(px, gy, s, pp, { idle: .3, faceW: 1.5, stripe: .3, hN, hF: o.handOff ? [px + 12 * s, gy - .2 * s] : [px + 17 * s, gy - .4 * s] });
  f.noFarArm = true;
  const { J } = joints(ctx, f);
  f.p = { ...f.p, wrN: R.a - J.AN.foA, wrF: 1.62 - J.AF.foA };
  return f;
}
// yakinYuz(ctx, t, {T, cam, lag, refA, rings, noBank, noTear, handOff, pose}) → {f, eye, reye, J, M}
function yakinYuz(ctx, t, o = {}) {
  baseT(ctx);
  glaze(ctx, 900, 800, 1100, 'rgba(140,56,26,.55)');
  camAt(ctx, ...(o.cam || [D_XE + 330, D_WY - 22, .96]));
  const T = o.T || {}, wy = o.wy || D_WY, NT = [o.xe ?? D_XE, wy];
  const f = dFig(ctx, t, NT, T, o);
  const { J, M } = joints(ctx, f);
  const eye = headPt(ctx, J, M, EYE_Q);
  const lag = o.lag ?? refLag(t);
  const fR = lag ? dFig(ctx, t - lag, NT, T, o) : f;
  const lock = T.ben != null ? ramp(t, T.ben, T.ben + .45, E.out3) : 0;
  const brk = T.hit != null ? ramp(t, T.hit, T.hit + .15, E.out2) * (1 - ramp(t, T.hit + .7, T.hit + 1.6, E.io2)) : 0;
  const refA = o.refA ?? (lerp(.44, .84, lock) + .26 * brk);
  const tx = eye[0] + 4;
  const rings = o.rings || [
    ...(T.hit != null ? [{ x: tx, y: wy + 4, t0: T.hit, A: 80, sq: .62, v: 820, lam: 150, k: 1.4, reach: 1800, life: 4.5, shear: 3.2, noLines: true },
      { x: tx, y: wy + 4, t0: T.hit, A: 1, sq: .62, v: 1000, lam: 115, k: .8, reach: 2600, life: 4.5, mask: 80 }] : []),
    ...(T.ben != null ? [{ x: D_TOUCH.tip[0] + (NT[0] - D_XE), y: wy + 3, t0: T.ben - .3, A: 5, sq: .62, v: 260, lam: 34, k: 1.6, reach: 500, life: 2.2 }] : [])];
  const water = c => c.rect(NT[0] - 10, wy, 9000, 3000);
  waterBody(ctx, water, wy, t, { a: .16, seed: 3, n: 30, depth: 420 });
  const bank = c => { for (const [x, sd, h] of [[1290, 5, 64], [1350, 8, 52], [1420, 2, 60]]) narcissus(c, x, wy - 44, 2.3, t, sd, { dir: -1, h }); };
  if (!o.noBank) { ctx.save(); ctx.beginPath(); ctx.rect(1100, wy, 9000, 3000); ctx.clip(); ctx.globalAlpha = .45; ctx.translate(0, 2 * wy); ctx.scale(1, -1); bank(ctx); ctx.restore(); }
  mirror(ctx, c => withFigT(t - lag, () => figure(c, fR)), wy, water, t, { a: refA, rings, calm: 1.0, warpBox: [NT[0] - 10, wy, 1180 + (NT[0] - D_XE), wy + 720] });
  if (!o.noBank) { farBank(ctx, 1120, 2600, wy, t, 12, { h: 74, grass: 9, fill: '#3A1B0D' }); bank(ctx); }
  ledge(ctx, NT[0], wy - D_GAP + .2 * D_S, wy);
  litFigure(ctx, f, { x: eye[0] + 30, y: wy + 30, r: 440, c: 'rgba(255,214,160,A)', a: .32, dark: .3 });
  shoreLine(ctx, NT[0], wy);
  if (!o.noTear && T.tear != null && T.hit != null && t > T.tear && t < T.hit) {
    const form = ramp(t, T.tear, T.tear + .2, E.out2), fall = clamp((t - (T.tear + .14)) / (T.hit - T.tear - .14));
    const y = lerp(eye[1] + 16, wy - 6, fall * fall), r = 6.5 * form;
    ctx.save(); ctx.fillStyle = '#F2E6CE'; ctx.strokeStyle = C.ink; ctx.lineWidth = 1.8;
    ctx.beginPath(); ctx.moveTo(tx, y - r * 2.2); ctx.quadraticCurveTo(tx + r * 1.1, y - r * .2, tx, y + r); ctx.quadraticCurveTo(tx - r * 1.1, y - r * .2, tx, y - r * 2.2); ctx.fill(); ctx.stroke(); ctx.restore();
  }
  return { f, eye, reye: [eye[0], 2 * wy - eye[1]], J, M };
}
