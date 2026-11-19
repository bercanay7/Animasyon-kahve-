// HAVUZ seti, SAHİP-2: P035, P036, P037, P038, P039, P040, P041, P042, P043, P044, P045, P046, P047, P048, P049, P050, P051, P052, P053, P054, P055, P056, P058, P059, P061, P062, P063, P064, P065, P067, P068, P070, P072, P073, P074, P075, P076, P083, P084, P087, P088, P089, P090, P092, P093, P094, P096. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Sabit saniye yok: her olay PE(id, k) / Wd() / A() çapasından.
// Bu dosyanın üstündeki s2_… işlevleri SAHİP-2'nin öbür set dosyalarınca da (çizim anında) kullanılır.
// Ortak kurucuların (lib/havuz.js kiyiOrta, yakinYuz, havuzGenis) set içi kopyaları: soluma (fade), mermer, siyah yansıma, ek katman kancaları için.
'use strict';

// ───────────────────────── SAHİP-2 ortak yardımcıları ─────────────────────────
// plan içi kamera: c0 → c1 (st.p boyunca, yumuşak)
function s2_cam(st, c0, c1, e = E.sine) { return camMix(c0, c1, st.p, e); }
// olay rampası: plan eylemi k'dan başlayıp d sn
function s2_r(t, id, k, d = .6, off = 0, e = E.io2) { const a = PE(id, k, off); return ramp(t, a, a + d, e); }
// bölüm kartı (yalnız başlık, 2–3 sn, sahnenin üstünde tek başına)
function s2_bolum(ctx, s, lt, d = 2.6, x = W / 2, y = 170) {
  if (NOTEXT) return;
  const a = clamp(lt / .4) * clamp((d - lt) / .5); if (a <= 0) return;
  txt(ctx, s, x, y, { font: FONT.baslik(78, 700), px: 78, ls: 14, a: E.sine(a), panel: .7 });
}
// figürü ayrı katmanda çizip ışık, soluma (fade 0..1), mermer (0..1) ile basar
function s2_litFig(ctx, f, light, o = {}) {
  const T = ctx.getTransform(), lx = layer('fig');
  lx.setTransform(T); const J = figure(lx, f);
  lx.globalCompositeOperation = 'source-atop';
  if (light && light.a > 0) {
    const g = lx.createRadialGradient(light.x, light.y, 0, light.x, light.y, light.r);
    g.addColorStop(0, light.c.replace('A', light.a.toFixed(3))); g.addColorStop(1, light.c.replace('A', '0'));
    lx.fillStyle = g; lx.fillRect(-3000, -3000, 9000, 9000);
  }
  const fade = o.fade || 0;
  if (fade > 0) { lx.fillStyle = `rgba(232,214,184,${(.55 * fade).toFixed(3)})`; lx.fillRect(-3000, -3000, 9000, 9000); }
  lx.globalCompositeOperation = 'source-over';
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  const A0 = ctx.globalAlpha * (o.alpha ?? 1) * (1 - .38 * fade);
  const mar = o.marble || 0;
  if (fade > .02) ctx.filter = `blur(${(fade * 2.4 * RS).toFixed(2)}px)`;
  if (mar < 1) { ctx.globalAlpha = A0 * (1 - mar * .999); ctx.drawImage(LY.fig, 0, 0); }
  if (mar > 0) { ctx.globalAlpha = A0 * mar; ctx.filter = 'grayscale(1) sepia(.18) brightness(2.05) contrast(1.15)'; ctx.drawImage(LY.fig, 0, 0); }
  ctx.restore();
  return J;
}
// ışık noktaları (incelme): beden çevresinde, belirlenimci
function s2_motes(ctx, t, n, seed, cx, cy, rx, ry, a) { if (a > .005) motesN(ctx, t, n, seed, cx, cy, rx, ry, a); }
// karşı kıyıdan (eksen değişimi, tur 2): sahne kendi katmanına çizilir ve yatayda aynalanarak basılır (kaya sağda, su solda, genç sola bakar).
// fn(g) sahneyi g'ye çizer (meander: false verin; bordür aynalanmadan sonra çizilir). Sahnedeki yazılar aynalanmasın diye s2_scr ile ekran yerini alıp sonra çizin.
function s2_flip(ctx, fn, o = {}) {
  const g = layer('s2flip'); const r = fn(g);
  ctx.save(); ctx.setTransform(-1, 0, 0, 1, CW, 0); ctx.drawImage(LY.s2flip, 0, 0); ctx.restore();
  baseT(ctx); if (o.meander !== false) meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
  return r;
}
// dünya noktasının mantıksal ekran yeri (1920×1080); flip: aynalanmış sahnede
function s2_scr(c, p, flip = false) { const q = c.getTransform().transformPoint(new DOMPoint(p[0], p[1])); const x = q.x / RS, y = q.y / RS; return [flip ? W - x : x, y]; }
// aynalanmış sahnede dipinto yazısı (yazı ters okunmasın): sahne içinde kuyruğa alınır (dünya noktası → ekran), aynalamadan sonra basılır.
// Q: dizi; o.align 'left' (dünyada sağa uzanan) aynalanınca sağa hizalanır; o.clipY (dünya y): bunun altında kalan kısım görünür (suya giren yazı)
function s2_yazQ(c, Q, s, wp, px, p, o = {}) { const z = Math.hypot(c.getTransform().a, c.getTransform().b) / RS; Q.push({ s, at: s2_scr(c, wp, true), px: px * z, p, o, cy: o.clipY != null ? s2_scr(c, [0, o.clipY], true)[1] : null }); }
function s2_yazBas(ctx, Q) {
  baseT(ctx);
  for (const q of Q) { const o = { ...q.o }; let x = q.at[0];
    ctx.save(); ctx.font = FONT.baslik(q.px, o.w || 600); ctx.letterSpacing = (o.ls ?? Math.round(q.px * .12)) + 'px'; const wd = ctx.measureText(q.s).width; ctx.restore();
    if (o.align === 'left') x -= wd;
    if (o.align === 'left') x = clamp(x, 120, 1800 - wd); else x = clamp(x, 120 + wd / 2, 1800 - wd / 2); // yazı x 120–1800 içinde
    ctx.save(); if (q.cy != null) { ctx.beginPath(); ctx.rect(0, q.cy + 1, W, H); ctx.clip(); }
    txtDipinto(ctx, q.s, x, q.at[1], q.px, q.p, { ...o, align: o.align === 'left' ? 'left' : o.align, ls: o.ls != null ? o.ls : undefined }); ctx.restore(); }
}
// yansıma kilitlenme parıltısı (P053 'benim'): temas noktasında kısa ışık ve yüzeyde kısa ışık çizgisi; a 0..1
function s2_parilti(ctx, x, y, a) {
  if (a <= .01) return;
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  const g = ctx.createRadialGradient(x, y, 0, x, y, 90); g.addColorStop(0, `rgba(255,236,200,${(.75 * a).toFixed(3)})`); g.addColorStop(.35, `rgba(255,214,160,${(.25 * a).toFixed(3)})`); g.addColorStop(1, 'rgba(255,214,160,0)');
  ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, y, 90, 40, 0, 0, TAU); ctx.fill();
  ctx.strokeStyle = `rgba(255,236,200,${(.7 * a).toFixed(3)})`; ctx.lineWidth = 3; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x - 160 * a - 20, y); ctx.lineTo(x + 160 * a + 20, y); ctx.stroke();
  ctx.restore();
}

// ---- orta: kıyıda uzanmış genç (lib/havuz.js kiyiOrta kopyası + kancalar) ----
// o: {cam, look, reach, smile, lag, refA, rings, pose(tt) → poz alanları, hN, hF, head, neck, handN, fade, marble, light, fig:false,
//     warm, pre(ctx) (kıyı ve sudan önce, dünya koordinatı), refl(c, tt) (yansıyan ek), reflTint(c) (yansıyan figürü boyar), post(ctx), waterFx(ctx, wy), bankOff}
function s2_kiyiFig(t, o = {}) {
  const { wy, gy, xe, s } = KIYI, px = xe - 30 * s, look = o.look || 0, reach = o.reach || 0;
  const grip = [xe - 12, gy - .6];
  const hN = o.hN || [lerp(grip[0] + 4, xe + 40, reach), lerp(grip[1], wy - 34, reach)];
  const pp = { ...pPose({ head: .08 * look + (o.head || 0), neck: .04 * look + (o.neck || 0), handN: o.handN || (reach > .3 ? 'open' : 'flat'), smile: o.smile ?? .25 * reach,
    brow: o.brow, mouthOpen: o.mouthOpen, eyeWide: o.eyeWide, blink: o.blink }), mouthFlat: !!o.mouthFlat, hemPerp: true, hemT: .62 };
  return { f: proneFig(px, gy, s, pp, { hN, hF: o.hF || [grip[0] - 9, grip[1]], flatFeet: -2.9 }), aN: o.wrA ?? lerp(.12, .42, reach) };
}
function s2_kiyi(ctx, t, o = {}) {
  baseT(ctx);
  glaze(ctx, 1150, 900, 1150, o.warm || 'rgba(130,52,24,.5)');
  if (o.bg) { ctx.save(); o.bg(ctx); ctx.restore(); }
  camAt(ctx, ...(o.cam || [890, 610, 1.56]));
  const { wy, gy, xe, s } = KIYI, px = xe - 30 * s;
  const P = tt => (typeof o.pose === 'function' ? { ...o, ...o.pose(tt) } : o);
  const mk = tt => { const q = P(tt); const { f, aN } = s2_kiyiFig(tt, q); const { J } = joints(ctx, f); f.p = { ...f.p, wrN: aN - J.AN.foA, wrF: .12 - J.AF.foA }; if (q.sty) f.sty = q.sty; return f; };
  const lag = o.lag ?? refLag(t);
  const f = o.fig === false ? null : mk(t), fR = o.fig === false ? null : (lag ? mk(t - lag) : f);
  const water = c => c.rect(xe - 10, wy, 4000, 2000);
  waterBody(ctx, water, wy, t, { a: .2, seed: 5, span: [xe, 2300], n: 28, depth: 380 });
  if (o.waterFx) { ctx.save(); ctx.beginPath(); water(ctx); ctx.clip(); o.waterFx(ctx, wy); ctx.restore(); }
  const bank = c => { if (o.bank !== false) for (const [x, sd, h] of (o.bankN || [[1290, 5, 60], [1318, 8, 48], [1350, 2, 56]])) narcissus(c, x, wy - 14, .62, t, sd, { dir: -1, h }); };
  mirror(ctx, bank, wy, c => c.rect(1150, wy, 4000, 2000), t, { a: .45, calm: 1.1 });
  if (fR || o.refl) mirror(ctx, c => { if (fR) withFigT(t - lag, () => { figure(c, fR); if (o.reflTint) { c.save(); c.globalCompositeOperation = 'source-atop'; o.reflTint(c); c.restore(); } }); if (o.refl) o.refl(c, t - lag); }, wy, water, t, { a: o.refA ?? .42, calm: o.calm ?? 1.1, rings: o.rings, warpBox: o.warpBox, dx: o.rdx || 0 });
  if (o.pre) o.pre(ctx);
  farBank(ctx, 1180, 2600, wy, t, 17, { h: 22, grass: 7, fill: '#3A1B0D' }); bank(ctx);
  ledge(ctx, xe, gy, wy);
  for (let i = 0; i < 5; i++) { const gx = 120 + i * 160; if (gx > px - 50 * s && gx < xe) continue; grass(ctx, gx, gy + 2, 1.6, t, i + 11); }
  if (o.under) o.under(ctx);
  if (f) withFigT(o.figT ?? t, () => s2_litFig(ctx, f, { x: xe + 80, y: wy + 40, r: 520, c: 'rgba(255,205,150,A)', a: o.light ?? .3 }, { fade: o.fade, marble: o.marble, alpha: o.figA }));
  shoreLine(ctx, xe - 10, wy, { w: 2.6 });
  if (o.post) o.post(ctx, f);
  if (o.meander !== false) { ctx.save(); baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze); ctx.restore(); }
  return { f, wy, lag };
}

// ---- yakın plan figürü (lib/havuz.js dFig/dReach kopyası): T.back verilirse el 'ben'den sonra o ana kadar suda kalır ----
function s2_dReach(t, T) {
  if (T.ben == null || T.son == null) return { ...D_REST, k: 0 };
  const son = T.son, ben = T.ben, tTouch = ben - .3, tBack = T.back ?? ben + .45;
  const hh = T.hand || 'point', rest = D_REST, mid = { w: [455, 545], a: 1.05, hand: hh }, touch = { w: [600, 520], a: 1.068, hand: hh };
  const t0 = son - .25, tm = t0 + .5;
  const mix = (P, Q, u) => ({ w: lerp2(P.w, Q.w, u), a: lerp(P.a, Q.a, u), hand: u < .35 ? P.hand : Q.hand });
  if (t < t0) return { ...rest, k: 0 };
  if (t < tm) return { ...mix(rest, mid, E.in2(clamp((t - t0) / (tm - t0)))), k: 1 };
  if (t < tTouch) return { ...mix(mid, touch, E.out2(clamp((t - tm) / (tTouch - tm)))), k: 2 };
  if (t < tBack) return { ...touch, k: 3 };
  if (t < tBack + .5) return { ...mix(touch, mid, E.io2(clamp((t - tBack) / .5))), k: 4 };
  return { ...mix(mid, rest, E.io2(clamp((t - tBack - .5) / .5))), k: 5 };
}
function s2_dFig(ctx, t, NT, T, o = {}) {
  const s = D_S, gy = NT[1] - D_GAP + .2 * s, px = NT[0] - 30 * s;
  const q = o.pose ? o.pose(t) : dPoseO(t, T), pp = pPose(q);
  pp.neck = 1.0 + q.neck; pp.head = -.9 + q.head;
  if (q.mouthFlat) pp.mouthFlat = true;
  const R = o.handOff ? { w: [140, 600], a: 1.62, hand: 'flat' } : s2_dReach(t, T);
  pp.handN = R.hand; pp.handF = 'flat';
  const hN = [R.w[0] + (NT[0] - D_XE), R.w[1] + (NT[1] - D_WY)];
  const f = proneFig(px, gy, s, pp, { idle: .3, faceW: 1.5, stripe: .3, hN, hF: o.handOff ? [px + 12 * s, gy - .2 * s] : [px + 17 * s, gy - .4 * s] });
  f.noFarArm = true;
  const hh = typeof o.handHead === 'function' ? o.handHead(t) : (o.handHead || 0); // tur 2 (P055): el şakağa gider (0..1)
  if (hh > .001) { const { J: J0, M: M0 } = joints(ctx, f), tp = headPt(ctx, J0, M0, [-.2, -7.6]); f.ik = { ...f.ik, hN: lerp2(f.ik.hN, tp, E.io2(clamp(hh))) }; pp.handN = hh > .4 ? 'flat' : pp.handN; }
  const { J } = joints(ctx, f);
  f.p = { ...f.p, wrN: lerp(R.a - J.AN.foA, J.AN.foA * 0 - .4, clamp(hh)), wrF: 1.62 - J.AF.foA };
  return f;
}

// ---- yakın: yüz ve yansıması (lib/havuz.js yakinYuz kopyası + kancalar) ----
// o: yakinYuz seçenekleri + {fade, motes, refl(c, tt, fR), reflTint(c), post(ctx, info), pre(ctx), tearEye (0..1 gözde yaş), tearEyeR (yansımada), light}
function s2_yakin(ctx, t, o = {}) {
  baseT(ctx);
  glaze(ctx, 900, 800, 1100, o.warm || 'rgba(140,56,26,.55)');
  camAt(ctx, ...(o.cam || [D_XE + 330, D_WY - 22, .96]));
  const T = o.T || {}, wy = o.wy || D_WY, NT = [o.xe ?? D_XE, wy];
  const f = s2_dFig(ctx, t, NT, T, o);
  const { J, M } = joints(ctx, f);
  const eye = headPt(ctx, J, M, EYE_Q);
  const lag = o.lag ?? refLag(t);
  let fR = lag ? s2_dFig(ctx, t - lag, NT, T, o) : f;
  if (o.reflNoJaw) fR = { ...fR, lk: { ...fR.lk, jaw: false, earHidden: true } }; // tur 2 (P046): ters yansımada kulak ve çene kazıması sırıtma gibi okunuyordu
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
  if (o.waterFx) { ctx.save(); ctx.beginPath(); water(ctx); ctx.clip(); o.waterFx(ctx, wy, eye); ctx.restore(); }
  const bank = c => { for (const [x, sd, h] of [[1290, 5, 64], [1350, 8, 52], [1420, 2, 60]]) narcissus(c, x, wy - 44, 2.3, t, sd, { dir: -1, h }); };
  if (!o.noBank) { ctx.save(); ctx.beginPath(); ctx.rect(1100, wy, 9000, 3000); ctx.clip(); ctx.globalAlpha = .45; ctx.translate(0, 2 * wy); ctx.scale(1, -1); bank(ctx); ctx.restore(); }
  mirror(ctx, c => { withFigT(t - lag, () => { figure(c, fR); if (o.reflTint) { c.save(); c.globalCompositeOperation = 'source-atop'; o.reflTint(c); c.restore(); } if (o.tearEyeR) s2_tearAt(c, fR, o.tearEyeR); }); if (o.refl) o.refl(c, t - lag, fR); },
    wy, water, t, { a: refA, rings, calm: o.calm ?? 1.0, dx: o.rdx || 0, warpBox: [NT[0] - 10, wy, 1180 + (NT[0] - D_XE), wy + 720], calmAt: o.calmAt });
  if (!o.noBank) { farBank(ctx, 1120, 2600, wy, t, 12, { h: 74, grass: 9, fill: '#3A1B0D' }); bank(ctx); }
  if (o.pre) o.pre(ctx, { eye, wy });
  ledge(ctx, NT[0], wy - D_GAP + .2 * D_S, wy);
  if (!o.noReal) s2_litFig(ctx, f, { x: eye[0] + 30, y: wy + 30, r: 440, c: 'rgba(255,214,160,A)', a: o.light ?? .32, dark: .3 }, { fade: o.fade, alpha: o.figA });
  if (o.tearEye) s2_tearAt(ctx, f, o.tearEye);
  shoreLine(ctx, NT[0], wy);
  if (!o.noTear && T.tear != null && T.hit != null && t > T.tear && t < T.hit) {
    const form = ramp(t, T.tear, T.tear + .2, E.out2), fall = clamp((t - (T.tear + .14)) / (T.hit - T.tear - .14));
    const y = lerp(eye[1] + 16, wy - 6, fall * fall), r = 6.5 * form;
    ctx.save(); ctx.fillStyle = '#F2E6CE'; ctx.strokeStyle = C.ink; ctx.lineWidth = 1.8;
    ctx.beginPath(); ctx.moveTo(tx, y - r * 2.2); ctx.quadraticCurveTo(tx + r * 1.1, y - r * .2, tx, y + r); ctx.quadraticCurveTo(tx - r * 1.1, y - r * .2, tx, y - r * 2.2); ctx.fill(); ctx.stroke(); ctx.restore();
  }
  const info = { f, eye, reye: [eye[0], 2 * wy - eye[1]], J, M, wy, lag };
  if (o.post) o.post(ctx, info);
  return info;
}
// gözde yaş (düşmeyen): figürün göz noktasının altında küçük krem damla; a 0..1
function s2_tearAt(c, f, a) {
  if (a <= .01) return;
  const { J, M } = joints(c, f), e = headPt(c, J, M, EYE_Q), sc = f.s / 26;
  c.save(); c.globalAlpha *= clamp(a); c.fillStyle = '#F2E6CE'; c.strokeStyle = C.ink; c.lineWidth = 1.6 * sc;
  const x = e[0] + 3 * sc, y = e[1] + (12 + 10 * a) * sc, r = 5.5 * sc;
  c.beginPath(); c.moveTo(x, y - r * 2.2); c.quadraticCurveTo(x + r * 1.1, y - r * .2, x, y + r); c.quadraticCurveTo(x - r * 1.1, y - r * .2, x, y - r * 2.2); c.fill(); c.stroke();
  c.restore();
}

// ---- geniş: orman kenarında pınar (lib/havuz.js havuzGenis kopyası + kancalar) ----
// o: havuzGenis seçenekleri + {sky(ctx) (dünya koord., zeminden önce), ground(ctx) (zemin bandından sonra), post(ctx), dark (0..1 karartma), treesA}
function s2_genis(ctx, t, o = {}) {
  baseT(ctx);
  glaze(ctx, 1250, 900, 1200, o.warm || 'rgba(120,48,22,.42)');
  const cam = o.cam || [980, 560, 1.0]; camAt(ctx, ...cam);
  if (o.sky) o.sky(ctx);
  const gy = o.gy ?? 760, pc = o.pc || [1290, 812], prx = o.prx ?? 380, pry = o.pry ?? 58;
  const trees = c => { if (o.trees === false) return;
    vaseTree(c, 150, gy, 1.75, 3, t, { branches: 7, reach: 110 }); vaseTree(c, 1720, gy, 1.9, 8, t, { branches: 7, reach: 120 });
    vaseTree(c, 1900, gy, 1.45, 5, t, { branches: 6 }); if (o.midTree !== false) vaseTree(c, 1010, gy, 1.05, 11, t, { branches: 5, reach: 70 });
    if (o.moreTrees) for (const [x, s2, sd] of o.moreTrees) vaseTree(c, x, gy, s2, sd, t, { branches: 6 }); };
  const NL = o.nerg || [[1560, 5, 58], [1610, 8, 46], [1655, 2, 54], [975, 11, 50]];
  const nerg = c => { for (const [x, sd, h] of NL) narcissus(c, x, gy, 1.35, t, sd, { dir: x > pc[0] ? -1 : 1, h }); };
  const pool = c => c.ellipse(pc[0], pc[1], prx, pry, 0, 0, TAU);
  groundBand(ctx, gy);
  if (o.ground) o.ground(ctx, gy);
  for (let i = 0; i < 9; i++) grass(ctx, 80 + i * 230 + (i % 2) * 70, gy + 2, 1.5, t, i + 3);
  ctx.save(); ctx.beginPath(); pool(ctx); ctx.fillStyle = '#050302'; ctx.fill(); ctx.restore();
  waterBody(ctx, pool, pc[1] - pry, t, { a: .22, seed: 9, span: [pc[0] - prx, pc[0] + prx - 120], n: 12, depth: pry * 1.6 });
  if (o.waterFx) { ctx.save(); ctx.beginPath(); pool(ctx); ctx.clip(); o.waterFx(ctx, pc, prx, pry); ctx.restore(); }
  mirror(ctx, c => { trees(c); nerg(c); if (o.fig) o.fig(c, true); }, gy, pool, t, { a: o.refA ?? .4, calm: .8, rings: o.rings });
  ctx.save(); ctx.beginPath(); pool(ctx); ctx.lineWidth = 4; ctx.strokeStyle = PC.clayR; ctx.stroke(); ctx.restore();
  crag(ctx, [[pc[0] - prx - 70, gy + 4], [pc[0] - prx + 10, gy - 34], [pc[0] - prx + 80, gy - 30], [pc[0] - prx + 120, gy + 8]], { fill: '#5A2C16', seed: 4, wob: 4, strata: 2, lobes: 1 });
  trees(ctx); nerg(ctx); if (o.fig) o.fig(ctx, false);
  if (o.post) o.post(ctx, { gy, pc, prx, pry });
  if (o.dark) { ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(8,4,8,${clamp(o.dark).toFixed(3)})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  if (o.meander !== false) { ctx.save(); baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze); ctx.restore(); }
  return { gy, pc, prx, pry };
}
// geniş planda kıyı kayasında yüzüstü uzanan Narkissos (havuzun sol kıyısı). o: {s, look, reach, head, neck, fade}
const S2W = { gy: 728, xe: 1000, s: 3.0 };
function s2_proneW(c, t, o = {}) {
  const s = o.s || S2W.s, xe = o.xe ?? S2W.xe, gy = o.gy ?? S2W.gy, px = xe - 30 * s, reach = o.reach || 0;
  const grip = [xe - 2 * s, gy - .1 * s];
  const hN = [lerp(grip[0], xe + 7 * s, reach), lerp(grip[1], gy + 5 * s, reach)];
  const f = proneFig(px, gy, s, { ...pPose({ head: o.head || 0, neck: o.neck || 0, handN: 'flat' }), hemPerp: true, hemT: .62 }, { hN, hF: [grip[0] - 1.5 * s, grip[1]], flatFeet: -2.9, idle: .3 });
  const { J } = joints(c, f); f.p = { ...f.p, wrN: lerp(.12, .42, reach) - J.AN.foA, wrF: .12 - J.AF.foA };
  return f;
}
// sol kıyı rafı: geniş planda figürün yattığı kaya
function s2_rafW(c) { crag(c, [[560, 762], [600, S2W.gy + 2], [880, S2W.gy - 4], [1012, S2W.gy + 2], [1030, 770], [560, 770]], { fill: '#5A2C16', seed: 21, wob: 3, strata: 2, lobes: 1, flat: [0, 5] }); }
// togalı şair (Ovidius; vazo silueti, portre değil): ayakta, himationlu uzun giysi, kısa sakal. o: {arm (0..1 kol uzatma), lean, walk, dist, s, dir, alpha}
const LK_OV = { beard: 'short', hair: 'short', garment: 'robe', himation: true, robeCol: '#C9703F', himCol: '#7E3920' };
function s2_ovid(c, x, gy, s, t, o = {}) {
  const arm = o.arm || 0;
  if (o.walk != null && o.walk < 1) {
    return walkScene(c, null, x, s, t, o.dir || 1, { ground: groundOf(() => gy), noCam: true, sty: STY.red, lk: LK_OV, dist: o.dist ?? x, stand: o.walk, stripe: .5, lean: .04, alpha: o.alpha,
      p: { shN: lerp(-.1, -1.25, arm), elN: lerp(.35, .1, arm), handN: arm > .4 ? 'open' : 'open' } });
  }
  return figure(c, { x, y: gy - 43 * s, s, dir: o.dir || 1, sty: STY.red, lk: LK_OV, seed: 41, idle: .5, stripe: .5, alpha: o.alpha,
    p: { torso: o.lean ?? .03, neck: .08, head: .1 + (o.head || 0), hipN: .06, knN: .04, hipF: -.08, knF: .02, ankN: 0, ankF: 0,
      shN: lerp(-.05, -.95, arm), elN: lerp(.45, .3, arm), shF: .12, elF: .9, handN: 'open', handF: 'flat' } });
}

// ön plan: şairin omzu ve başının arkası (omuz üstü çekim; ekran koordinatı, sol alt). dx: yatay kayma
function s2_omuz(c, t, dx = 0, o = {}) {
  c.save(); baseT(c); c.translate(dx + Math.sin(t * .5) * 3, Math.sin(t * .7) * 2);
  const ink = o.col || '#0B0605';
  c.fillStyle = ink; c.beginPath(); c.moveTo(-40, H + 20); c.bezierCurveTo(60, 860, 250, 800, 380, 760); c.bezierCurveTo(430, 740, 450, 700, 452, 660);
  c.bezierCurveTo(470, 560, 440, 470, 360, 440); c.bezierCurveTo(260, 400, 160, 440, 140, 530); c.bezierCurveTo(130, 600, 160, 650, 190, 690);
  c.bezierCurveTo(120, 720, 30, 760, -40, 780); c.closePath(); c.fill();
  // kısa saç bukleleri (kazıma: kil çizgi) ve himation kıvrımları
  c.strokeStyle = 'rgba(201,112,63,.55)'; c.lineWidth = 3; c.lineCap = 'round';
  for (let i = 0; i < 9; i++) { const a = PI * 1.05 + i * .2, cx = 300 + Math.cos(a) * 130, cy = 545 + Math.sin(a) * 105; c.beginPath(); c.arc(cx, cy, 14, a - 1.2, a + 1.2); c.stroke(); }
  c.lineWidth = 3.5; for (const k of [0, 1, 2]) { c.beginPath(); c.moveTo(20 + k * 70, H); c.bezierCurveTo(120 + k * 70, 900, 220 + k * 60, 840, 340 + k * 30, 790); c.stroke(); }
  c.restore();
}

// tepeden (ters açı) dili: sahne kendi katmanına çizilip 90° döndürülür; su çizgisi dikey, gerçek baş solda, yansıma sağda
function s2_rot(ctx, fn) {
  const g = layer('s2rot'); fn(g);
  baseT(ctx); ctx.fillStyle = '#050302'; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.translate(DW / 2, DH / 2); ctx.rotate(-PI / 2); ctx.scale(DW / DH, DW / DH); ctx.drawImage(LY.s2rot, -DW / 2, -DH / 2); ctx.restore();
  baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
}
// geniş planda arkadaki patika (P054; DERE P086 ile aynı biçim): zeminde ormana kıvrılan açık şerit; li 0..1 ışık
function s2_patika(c, gy, li) {
  const P = [[960, 1080], [820, 960], [560, 880], [380, 810], [250, gy + 4]], Wd2 = [120, 90, 60, 36, 14];
  c.save(); c.beginPath();
  P.forEach((q, i) => (i ? c.lineTo(q[0] + Wd2[i], q[1]) : c.moveTo(q[0] + Wd2[i], q[1])));
  for (let i = P.length - 1; i >= 0; i--) c.lineTo(P[i][0] - Wd2[i], P[i][1]);
  c.closePath(); c.fillStyle = mixCol('#7E3920', '#E8B07A', li); c.fill(); c.strokeStyle = 'rgba(14,9,7,.6)'; c.lineWidth = 2; c.stroke();
  if (li > .01) { const g = c.createLinearGradient(250, 300, 700, 1000); g.addColorStop(0, `rgba(255,226,170,${(.28 * li).toFixed(3)})`); g.addColorStop(1, 'rgba(255,226,170,0)');
    c.fillStyle = g; c.beginPath(); c.moveTo(130, 120); c.lineTo(330, 120); c.lineTo(900, 1080); c.lineTo(560, 1080); c.closePath(); c.fill(); }
  c.restore();
}
// omuz üstü çekim (P055, tur 2): sağ ön planda gencin başının arkası, kulağı ve omzu (ekran koordinatı); hale yok: başın çevresinde ışık ya da halka yok, ışık yalnız suda.
// hands 0..1: yakın kol kalkar, el şakağa; öbür elin parmakları başın sol yanında görünür (başını iki elinin arasına alır)
function s2_omuzNk(ctx, t, hands) {
  ctx.save(); baseT(ctx); const by = Math.sin(t * .8) * 3, hx = 1640, hy = 330 + by;
  const ink = C.ink;
  // omuz ve khiton (sağ alttan yükselen kütle)
  ctx.fillStyle = '#93492A'; ctx.strokeStyle = ink; ctx.lineWidth = 6;
  ctx.beginPath(); ctx.moveTo(1180, H + 30); ctx.bezierCurveTo(1250, 820, 1380, 640, 1560, 600); ctx.bezierCurveTo(1700, 570, 1860, 560, W + 40, 600); ctx.lineTo(W + 40, H + 30); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.strokeStyle = 'rgba(14,9,7,.5)'; ctx.lineWidth = 3.5; for (const k of [0, 1, 2, 3]) { ctx.beginPath(); ctx.moveTo(1330 + k * 120, H + 10); ctx.bezierCurveTo(1380 + k * 110, 880, 1450 + k * 100, 720, 1540 + k * 110, 640); ctx.stroke(); }
  // boyun (kil) ve başın arkası (siyah sır saç, kısa bukle kazımaları)
  ctx.fillStyle = '#C9703F'; ctx.strokeStyle = ink; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(1500, 610); ctx.bezierCurveTo(1520, 520, 1560, 470, 1620, 450); ctx.lineTo(1760, 470); ctx.bezierCurveTo(1760, 540, 1740, 590, 1730, 610); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#C9703F'; ctx.beginPath(); ctx.ellipse(hx - 168, hy + 50, 24, 40, -.25, 0, TAU); ctx.fill(); ctx.stroke(); // kulak (suya dönük yan)
  ctx.beginPath(); ctx.moveTo(hx - 150, hy + 10); ctx.bezierCurveTo(hx - 190, hy + 120, hx - 140, hy + 190, hx - 70, hy + 200); ctx.lineTo(hx - 20, hy + 120); ctx.closePath(); ctx.fill(); // yanak kenarı (yüz suya dönük, yalnız kenarı)
  ctx.fillStyle = '#0E0907'; ctx.beginPath(); ctx.ellipse(hx, hy, 170, 158, .15, 0, TAU); ctx.fill();
  ctx.strokeStyle = 'rgba(201,112,63,.6)'; ctx.lineWidth = 3.5; for (let i = 0; i < 18; i++) { const a = i / 18 * TAU, rr = 40 + (i % 3) * 38; ctx.beginPath(); ctx.arc(hx + Math.cos(a) * rr, hy + Math.sin(a) * rr * .9, 16, a - 1.2, a + 1.2); ctx.stroke(); }
  if (hands > .02) {
    const limb = (a2, b2, w0, w1) => { const d = sub(b2, a2), n = [-d[1] / len(d), d[0] / len(d)]; ctx.beginPath(); ctx.moveTo(a2[0] + n[0] * w0, a2[1] + n[1] * w0); ctx.lineTo(b2[0] + n[0] * w1, b2[1] + n[1] * w1); ctx.lineTo(b2[0] - n[0] * w1, b2[1] - n[1] * w1); ctx.lineTo(a2[0] - n[0] * w0, a2[1] - n[1] * w0); ctx.closePath(); ctx.fill(); ctx.stroke(); };
    const el = [lerp(1900, 1880, hands), lerp(1100, 470, hands)], hd = [lerp(1880, 1520, hands), lerp(1150, 320, hands)];
    ctx.fillStyle = '#C9703F'; ctx.strokeStyle = ink; ctx.lineWidth = 5; limb([1980, 1000], el, 52, 42); limb(el, hd, 42, 32); ctx.beginPath(); ctx.arc(el[0], el[1], 42, 0, TAU); ctx.fill();
    ctx.save(); ctx.translate(hd[0], hd[1]); ctx.rotate(-2.6); ctx.beginPath(); ctx.ellipse(0, 0, 58, 34, 0, 0, TAU); ctx.fill(); ctx.stroke(); ctx.lineWidth = 2.5; for (const k of [-1, 0, 1]) { ctx.beginPath(); ctx.moveTo(10, k * 12); ctx.lineTo(50, k * 13); ctx.stroke(); } ctx.restore();
    // öbür elin parmakları başın sol yanında (yalnız uçlar)
    ctx.save(); ctx.globalAlpha *= clamp(hands * 1.4 - .3); ctx.fillStyle = '#C9703F'; ctx.lineWidth = 4; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.ellipse(hx - 150 + k * 18, hy - 120 + k * 22, 13, 30, .9, 0, TAU); ctx.fill(); ctx.stroke(); } ctx.restore();
  }
  ctx.restore();
}
// P056 alıntısı: 'Sahip' kelimesi ekranın üst yarısında ortada (P057'ye eşleme kesmesi: aynı yerde SAHİP)
const S2_SAHIP = [960, 250];
function s2_sahipSatir(ctx, st) {
  if (NOTEXT) return;
  const t = st.t, a = E.sine(ramp(t, st.at + .2, st.at + .8, E.lin)), red = ramp(t, PE('P056', 1) - .05, PE('P056', 1) + .3);
  ctx.save(); ctx.font = FONT.alinti(74); ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
  const p0 = '“', w0 = ctx.measureText(p0).width, w1 = ctx.measureText('Sahip').width, r1 = ' olduğum şey', w2 = ctx.measureText(r1).width, l2 = 'beni yoksul etti.”';
  const x0 = S2_SAHIP[0] - w0 - w1 / 2, cx = x0 + (w0 + w1 + w2) / 2, y1 = S2_SAHIP[1], y2 = y1 + 92;
  ctx.globalAlpha = a; softPanel(ctx, cx, (y1 + y2) / 2, (w0 + w1 + w2) / 2 + 120, 150, .78);
  ctx.fillStyle = YAZI.krem; ctx.fillText(p0, x0, y1); ctx.fillStyle = mixCol('#F2E6CE', '#E0573A', red); ctx.fillText('Sahip', x0 + w0, y1); ctx.fillStyle = YAZI.krem; ctx.fillText(r1, x0 + w0 + w1, y1);
  ctx.globalAlpha = a * ramp(t, st.at + .7, st.at + 1.3); ctx.textAlign = 'center'; ctx.fillText(l2, cx, y2);
  ctx.restore();
  kunye(ctx, 'Ovidius, Dönüşümler III 466 · inopem me copia fecit', st.lt - 1.2, st.d);
}
// P063: suyun içinden yukarı bakış. Yakın sahne kendi katmanına çizilir; yüzeyin üstü kırılarak (satır satır yatay dalga) görünür, altı karanlık su
function s2_altSu(ctx, t, st, calm, hand) {
  const tK = PE('P063', 0), g = layer('s2alt'), cam = [D_XE + 330, D_WY - 120 + lerp(0, -30, st.p), 1.08];
  s2_yakin(g, t, { cam, lag: 0, noBank: true, refA: 0, light: .2, T: { son: tK - 1.0, ben: tK - .1, back: 1e9, hand: 'open' }, pose: tt => ({ ...dPoseO(tt, {}), smile: -.3 }) });
  baseT(ctx); ctx.fillStyle = '#060404'; ctx.fillRect(0, 0, W, H);
  const yW = 540 + (D_WY - cam[1]) * cam[2] + 6; // yüzeyin ekrandaki yeri
  const amp = lerp(9, 2, calm), step = 4; // tur 2: kırılma hafif (beden 'erimiş kütle' okunmasın)
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = lerp(.72, .92, calm);
  for (let y = 0; y < yW * RS; y += step * RS) { const dx = amp * RS * Math.sin(y / RS * .045 + t * 2.1) * (.4 + .6 * (1 - y / (yW * RS))); ctx.drawImage(LY.s2alt, 0, y, DW, step * RS, dx, y, DW, step * RS); }
  ctx.restore();
  baseT(ctx);
  const gr = ctx.createLinearGradient(0, 0, 0, yW); gr.addColorStop(0, 'rgba(10,6,6,.15)'); gr.addColorStop(1, 'rgba(20,12,10,.45)'); ctx.fillStyle = gr; ctx.fillRect(0, 0, W, yW);
  // yüzey çizgisi (dalgalı, açık kil) ve altta karanlık su; dağılmış yansımadan kalan koyu leke söner
  ctx.strokeStyle = 'rgba(232,160,104,.85)'; ctx.lineWidth = 4; ctx.beginPath(); for (let x = 0; x <= W; x += 20) { const y = yW + Math.sin(x * .02 + t * 2) * lerp(8, 1.5, calm); x ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
  const g2 = ctx.createLinearGradient(0, yW, 0, H); g2.addColorStop(0, '#120a07'); g2.addColorStop(1, '#030202'); ctx.fillStyle = g2; ctx.fillRect(0, yW + 2, W, H);
  ctx.save(); ctx.globalAlpha = .55 * (1 - calm); ctx.fillStyle = '#000'; ctx.beginPath(); ctx.ellipse(1000, yW + 120, 300, 70, 0, 0, TAU); ctx.fill(); ctx.restore();
  for (let i = 0; i < 5; i++) { const x = 300 + i * 330 + Math.sin(t * .4 + i) * 30; const g3 = ctx.createLinearGradient(x, yW, x + 120, H); g3.addColorStop(0, 'rgba(230,170,110,.12)'); g3.addColorStop(1, 'rgba(230,170,110,0)'); ctx.fillStyle = g3; ctx.beginPath(); ctx.moveTo(x, yW); ctx.lineTo(x + 60, yW); ctx.lineTo(x + 260, H); ctx.lineTo(x + 120, H); ctx.closePath(); ctx.fill(); }
  // parmak uçlarının gölgesi yüzeyde (el dokunmaz)
  if (hand > .01) { ctx.save(); ctx.globalAlpha = .5 * hand; ctx.fillStyle = '#000'; for (let k = 0; k < 4; k++) { ctx.beginPath(); ctx.ellipse(880 + k * 34, yW + 10, 14, 5, 0, 0, TAU); ctx.fill(); } ctx.restore(); }
  meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
}
// P064: ot yaprağında kırağı. sun 0..1 ışık ulaşır, melt 0..1 erime; tE: damla düşer
function s2_kiragi(ctx, t, st, sun, melt, tE) {
  baseT(ctx); glaze(ctx, 900, 900, 1200, 'rgba(120,48,22,.45)');
  const dx = lerp(40, -120, st.p); ctx.translate(dx, 0);
  // altta bulanık su ve karşı kıyı
  ctx.fillStyle = '#050302'; ctx.fillRect(-200, 820, 2400, 400); ctx.strokeStyle = 'rgba(201,112,63,.25)'; ctx.lineWidth = 3; for (let i = 0; i < 9; i++) { const y = 850 + i * 24, x = 200 + hash(i) * 1400; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 160, y); ctx.stroke(); }
  ctx.strokeStyle = 'rgba(232,160,104,.9)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(-200, 820); ctx.lineTo(2400, 820); ctx.stroke();
  // ışık şeridi (eğik; hale değil)
  if (sun > .01) { const g = ctx.createLinearGradient(400, 0, 1300, 800); g.addColorStop(0, 'rgba(255,226,170,0)'); g.addColorStop(1, `rgba(255,226,170,${(.22 * sun).toFixed(3)})`); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(300, -40); ctx.lineTo(520, -40); ctx.lineTo(lerp(700, 1180, sun), 820); ctx.lineTo(lerp(600, 1060, sun), 820); ctx.closePath(); ctx.fill(); }
  // tur 2: ince, yeşil-gri ot yaprakları (kuyruklu yıldız okunmasın): arkada iki koyu yaprak, önde yakın tek yaprak; kırağı kenarlarda küçük beyaz taneler
  const sw = Math.sin(t * .9) * 5;
  const blade = (B, w0, fill, ink, swk) => {
    const pt = u => { const a = lerp2(B[0], B[1], u), b = lerp2(B[1], B[2], u), c2 = lerp2(B[2], B[3], u); const ab = lerp2(a, b, u), bc = lerp2(b, c2, u); return add(lerp2(ab, bc, u), [0, sw * swk * u]); };
    const wid = u => w0 * (1 - Math.pow(u, 1.6)) + 1.5;
    const nrm = u => { const q = sub(pt(Math.min(1, u + .01)), pt(Math.max(0, u - .01))); return [-q[1] / len(q), q[0] / len(q)]; };
    ctx.beginPath(); for (let i = 0; i <= 50; i++) { const u = i / 50, p = pt(u), n = nrm(u), w = wid(u); i ? ctx.lineTo(p[0] + n[0] * w, p[1] + n[1] * w) : ctx.moveTo(p[0] + n[0] * w, p[1] + n[1] * w); }
    for (let i = 50; i >= 0; i--) { const u = i / 50, p = pt(u), n = nrm(u), w = wid(u); ctx.lineTo(p[0] - n[0] * w, p[1] - n[1] * w); }
    ctx.closePath(); ctx.fillStyle = fill; ctx.fill(); ctx.strokeStyle = ink; ctx.lineWidth = 3; ctx.stroke();
    ctx.beginPath(); for (let i = 0; i <= 50; i++) { const p = pt(i / 50); i ? ctx.lineTo(...p) : ctx.moveTo(...p); } ctx.strokeStyle = 'rgba(220,226,200,.35)'; ctx.lineWidth = 1.6; ctx.stroke();
    return { pt, wid, nrm };
  };
  // kıyı (solda): koyu toprak sırt, yapraklar ondan çıkar ve suyun üstüne eğilir
  crag(ctx, [[-400, 1200], [-400, 700], [120, 690], [330, 730], [470, 800], [520, 830], [560, 1200]], { fill: '#4A2412', seed: 64, wob: 4, strata: 3, lobes: 2 });
  for (let i = 0; i < 4; i++) grass(ctx, 40 + i * 110, 700 + i * 12, 2.2, t, 150 + i);
  blade([[260, 720], [420, 470], [700, 330], [860, 400]], 13, '#3E4536', C.ink, .5);
  blade([[340, 740], [560, 560], [820, 520], [960, 600]], 11, '#3A4033', C.ink, .4);
  const L = blade([[300, 730], [560, 380], [1060, 300], [1400, 600]], 28, '#7F8A6C', C.ink, 1);
  const pt = L.pt;
  // kırağı: kenar boyunca küçük beyaz taneler (yıldız değil); ışıkla parlar, erir (küçülür ve söner)
  const r = rng(64); ctx.save();
  for (let i = 0; i < 160; i++) { const u = .05 + r() * .9, side = r() < .5 ? -1 : 1, p = pt(u), n = L.nrm(u), w = L.wid(u) * side * (.55 + .4 * r()), sz = (1.6 + r() * 2.6) * (1 - melt * (.6 + .4 * r())), bright = .6 + .4 * sun;
    if (sz <= .3) continue; ctx.globalAlpha = clamp((1 - melt * 1.1) + .2) * bright; ctx.fillStyle = '#F6F0E2';
    ctx.beginPath(); ctx.arc(p[0] + n[0] * w, p[1] + n[1] * w, sz, 0, TAU); ctx.fill(); }
  ctx.restore();
  // ucunda damla: erirken büyür, 'erirse'de suya düşer
  const tip = pt(1), form = clamp(melt * 1.3), fall = clamp((t - tE) / .45);
  if (form > .05 && fall < 1) { const y = lerp(tip[1] + 14, 820, fall * fall), rr = 7 + 6 * form; ctx.fillStyle = '#F2E6CE'; ctx.strokeStyle = C.ink; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(tip[0], y - rr * 2); ctx.quadraticCurveTo(tip[0] + rr, y, tip[0], y + rr); ctx.quadraticCurveTo(tip[0] - rr, y, tip[0], y - rr * 2); ctx.fill(); ctx.stroke(); }
  baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
}
// karşı kıyıda yankının döndüğü kayalar (orta planlarda; dünya koordinatı)
function s2_uzakKaya(c, x, wy) {
  crag(c, [[x - 160, wy], [x - 120, wy - 150], [x - 30, wy - 230], [x + 90, wy - 260], [x + 220, wy - 180], [x + 330, wy - 120], [x + 420, wy]], { fill: '#2E160B', seed: 31, wob: 6, strata: 3, lobes: 2 });
}
// ağıt yakan peri (ayakta, elleri başında: Yunan ağıt jesti; saç yolma yok). h 0..1 kollar kalkar
const LK_PERI = { fem: true, hair: 'long', garment: 'robe', himation: true, robeCol: '#C9703F', himCol: '#8E2F1F' };
const S2_TEN = { ...STY.red, white: '#DDA77B' }; // tur 2: kadın teni açık kil (beyaz ten kolları başörtü gibi okutuyordu); Eko'nun koyu hâli s2_eko'da
function s2_peri(c, x, gy, s, t, seed, h, dir = 1, o = {}) {
  return figure(c, { x, y: gy - 43 * s, s, dir, sty: S2_TEN, lk: LK_PERI, seed, idle: .6, stripe: .5, alpha: o.alpha,
    p: { torso: .02 + .04 * h, neck: .1 + .15 * h, head: .12 + .12 * h, hipN: .04, knN: .02, hipF: -.05, knF: .02,
      shN: lerp(.1, -2.45, h), elN: lerp(.3, 2.05, h), shF: lerp(-.1, -2.3, h), elF: lerp(.3, 2.15, h), handN: 'flat', handF: 'flat' } });
}
// P073: ot yatağı yakın. part 0..1 peri otları aralar; gone 0..1 son nokta söner, el boş yere değer
function s2_otYatak(ctx, t, st, part, gone, tA) {
  baseT(ctx); glaze(ctx, 900, 900, 1100, 'rgba(110,44,20,.45)');
  camAt(ctx, ...s2_cam(st, [920, 600, 2.0], [980, 605, 2.0]));
  const { wy, gy, xe } = KIYI;
  waterBody(ctx, c => c.rect(xe - 10, wy, 4000, 2000), wy, t, { a: .16, seed: 5, span: [xe, 2300], n: 18, depth: 300 });
  ledge(ctx, xe, gy, wy); shoreLine(ctx, xe - 10, wy, { w: 2.6 });
  // ışık noktaları: yatağın üstünde; aralanınca havalanır ve söner
  const n = 24, r = rng(73);
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) { const x0 = 760 + r() * 240, y0 = 600 + r() * 14, die = tA + .2 + r() * 1.6, last = i === 0, td = last ? lerp(die, die + 1.2, 1) : die;
    const up = part * (40 + r() * 60), al = last ? (1 - gone) : clamp(1 - (t - td) / .4) * (1 - .3 * part);
    if (al <= .01) continue; const x = x0 + Math.sin(t * .6 + i) * 6, y = y0 - up - Math.sin(t + i) * 3, k = .5 + .5 * Math.sin(t * 1.7 + i * 2.1);
    ctx.fillStyle = `rgba(255,226,170,${(.8 * al * k).toFixed(3)})`; ctx.beginPath(); ctx.arc(x, y, 1.6 + r() * 1.8, 0, TAU); ctx.fill(); }
  ctx.restore();
  // ot tutamları (aralanır)
  for (let i = 0; i < 9; i++) { const x = 740 + i * 32, sp = part * (i < 4 ? -1 : 1) * 14; ctx.save(); ctx.translate(x + sp, gy - 2); grass(ctx, 0, 0, 2.6, t, 80 + i); ctx.restore(); }
  // tur 2: perinin önkolu ve eli soldan, yere paralel girer (üstten inen kol bacak gibi okunuyordu): kırmızı himation yeni, açık ten önkol, dört ayrık parmak otları aralar
  if (part > .01) { const hx = lerp(560, 860, part), hy = lerp(560, 612 - 6 * (1 - gone), part), el = [hx - 300, hy - 70];
    ctx.save(); ctx.lineJoin = 'round'; ctx.lineCap = 'round'; ctx.strokeStyle = C.ink; ctx.lineWidth = 3;
    // önkol (bilekte incelir)
    ctx.fillStyle = '#DDA77B'; ctx.beginPath(); ctx.moveTo(el[0], el[1] - 20); ctx.quadraticCurveTo(hx - 150, hy - 50, hx - 44, hy - 15); ctx.lineTo(hx - 40, hy + 3); ctx.quadraticCurveTo(hx - 160, hy - 18, el[0], el[1] + 22); ctx.closePath(); ctx.fill(); ctx.stroke();
    // yen: kırmızı himation kenarı, kadraj dışından
    ctx.fillStyle = '#8E2F1F'; ctx.beginPath(); ctx.moveTo(el[0] - 200, el[1] - 60); ctx.lineTo(el[0] + 20, el[1] - 36); ctx.quadraticCurveTo(el[0] + 34, el[1], el[0] + 14, el[1] + 38); ctx.lineTo(el[0] - 200, el[1] + 70); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = 'rgba(14,9,7,.6)'; ctx.lineWidth = 2; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.moveTo(el[0] - 120 + k * 40, el[1] - 44 + k * 6); ctx.lineTo(el[0] - 110 + k * 40, el[1] + 50 - k * 4); ctx.stroke(); }
    // el: avuç ve dört parmak (yere doğru, aralık), başparmak üstte
    ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.fillStyle = '#DDA77B';
    ctx.beginPath(); ctx.ellipse(hx - 22, hy - 6, 30, 17, .12, 0, TAU); ctx.fill(); ctx.stroke();
    for (let k = 0; k < 4; k++) { const a = -.28 + k * .2, L = 38 - Math.abs(k - 1.4) * 5, bx = hx + 2, by = hy - 14 + k * 8;
      ctx.save(); ctx.translate(bx, by); ctx.rotate(a); ctx.beginPath(); ctx.roundRect(0, -5.5, L, 11, 5.5); ctx.fill(); ctx.stroke(); ctx.restore(); }
    ctx.save(); ctx.translate(hx - 18, hy - 20); ctx.rotate(-.75); ctx.beginPath(); ctx.roundRect(0, -6, 30, 12, 6); ctx.fill(); ctx.stroke(); ctx.restore();
    ctx.restore(); }
  baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
}
// nergis yakın (P074, P075, P076, P084, P096): kıyı kayasının ucunda büyük nergis ve sudaki yansıması
// o: {open, lean (suya eğilme), refA, cam, saffron, s, x, calm, extra(ctx) (dünya koord. son katman), refl(c)}
function s2_nergisYakin(ctx, t, st, o = {}) {
  baseT(ctx); glaze(ctx, 1000, 900, 1100, o.warm || 'rgba(130,52,24,.5)');
  camAt(ctx, ...(o.cam || [1000, 600, 1.0]));
  const wy = 640, xe = 900, gy = 600, nx = o.x ?? 860, s = o.s ?? 5.2, lean = o.lean || 0;
  const flower = c => { c.save(); c.translate(nx, gy); c.rotate(.12 + .32 * lean); narcissus(c, 0, 0, s, t, o.seed ?? 7, { dir: 1, h: 64, open: o.open ?? 1, tilt: .2 * lean }); c.restore(); };
  waterBody(ctx, c => c.rect(xe - 10, wy, 4000, 2000), wy, t, { a: .2, seed: 15, span: [xe, 2400], n: 24, depth: 380 });
  farBank(ctx, 1150, 2600, wy, t, 19, { h: 30, grass: 8, fill: '#3A1B0D' });
  if (o.refA > .01) mirror(ctx, c => { flower(c); if (o.refl) o.refl(c); }, wy, c => c.rect(xe - 10, wy, 4000, 2000), t, { a: o.refA, calm: o.calm ?? 1.0 });
  crag(ctx, [[-400, gy + 4], [xe - 300, gy - 4], [xe - 30, gy - 2], [xe + 4, gy + 14], [xe - 6, wy + 30], [xe - 40, wy + 700], [-400, wy + 700]], { fill: '#5A2C16', seed: 9, flat: [0, 5, 6], wob: 4, strata: 4, lobes: 3 });
  for (let i = 0; i < 6; i++) grass(ctx, 300 + i * 110, gy + 2, 1.8, t, i + 31);
  const ang = .12 + .32 * lean, hp = add([nx, gy], rot([19 * s, -56 * s], ang));
  if (o.saffron > 0) { const g = ctx.createRadialGradient(hp[0], hp[1], 0, hp[0], hp[1], 120); g.addColorStop(0, `rgba(255,200,90,${(.14 * o.saffron).toFixed(3)})`); g.addColorStop(1, 'rgba(255,200,90,0)'); ctx.fillStyle = g; ctx.fillRect(hp[0] - 130, hp[1] - 130, 260, 260); }
  flower(ctx);
  shoreLine(ctx, xe - 10, wy, { w: 3 });
  if (o.extra) o.extra(ctx, { wy, nx, gy, hp });
  baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
}

// tepeden bakış (ters açı: P041, P059, P093): kıyı taşı solda, su çizgisi dikey; solda başın tepesi ve omuzlar (khiton), sağda suda yüzün soluk yansıması (önden, alnı kıyıya dönük)
// o: {lA (gerçek başa ışık), rA (yansımaya ışık), refA, drift (yansıma sağa kayar, px), reach (0..1 el suya), wob (dalga), ring (0..1 iki bedenin çevresinde kapanan halka), close (0..1 havuz kenarı içe kapanır), leaf(ctx), dx (kamera kayması)}
function s2_tepe(ctx, t, o = {}) {
  baseT(ctx); ctx.fillStyle = '#050302'; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.translate(o.dx || 0, o.dy || 0); ctx.translate(900, 540); ctx.scale(1.45, 1.45); ctx.translate(-900, -540);
  const ex = 900, hy = 540 + Math.sin(t * .5) * 4, br = Math.sin(t * 1.1) * 2;
  // su (sağ): koyu sır, yatay kısa çizgiler
  ctx.fillStyle = '#060303'; ctx.fillRect(ex, -200, 2400, 1500);
  const r = rng(93); ctx.strokeStyle = 'rgba(201,112,63,.2)'; ctx.lineCap = 'round';
  for (let i = 0; i < 40; i++) { const x = ex + 20 + r() * 1300, y = r() * 1080, L = 40 + r() * 140, d = Math.sin(t * .6 + i) * 6; ctx.lineWidth = 1.6 + r() * 1.2; ctx.beginPath(); ctx.moveTo(x + d, y); ctx.lineTo(x + L + d, y); ctx.stroke(); }
  // sudaki yüz (önden, alnı kıyıya dönük): soluk, satır satır dalgalı
  const fx = ex + 300 + (o.drift || 0), L = layer('s2tepe'); L.setTransform(ctx.getTransform());
  s2_onYuz(L, fx, hy, 1.15, t);
  const A = (o.refA ?? .55) * (.75 + .25 * (o.rA || 0));
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = A;
  const step = 3 * RS, wob = o.wob ?? 1;
  for (let y = 0; y < DH; y += step) { const dx = (4 + 6 * wob) * RS * Math.sin(y / RS * .05 + t * 1.6); ctx.drawImage(LY.s2tepe, 0, y, DW, step, dx, y, DW, step); }
  ctx.restore();
  if (o.rA > .01) { const g = ctx.createRadialGradient(fx, hy, 0, fx, hy, 260); g.addColorStop(0, `rgba(255,214,160,${(.16 * o.rA).toFixed(3)})`); g.addColorStop(1, 'rgba(255,214,160,0)'); ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = g; ctx.fillRect(fx - 300, hy - 300, 600, 600); ctx.restore(); }
  if (o.leaf) o.leaf(ctx);
  // kıyı taşı (sol)
  crag(ctx, [[-400, -200], [ex - 10, -200], [ex + 6, 200], [ex - 8, 520], [ex + 8, 860], [ex - 6, 1300], [-400, 1300]], { fill: '#5A2C16', seed: 44, wob: 5, strata: 3, lobes: 2 });
  ctx.strokeStyle = 'rgba(232,160,104,.9)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(ex + 2, -200); ctx.lineTo(ex + 2, 1300); ctx.stroke();
  // sırt ve khiton (soldan), kollar kıyıya; el suya uzanabilir
  ctx.save(); ctx.translate(0, br);
  ctx.fillStyle = '#93492A'; ctx.strokeStyle = C.ink; ctx.lineWidth = 5;
  ctx.beginPath(); ctx.moveTo(-200, hy - 170); ctx.bezierCurveTo(300, hy - 200, 560, hy - 210, 690, hy - 150); ctx.bezierCurveTo(730, hy - 60, 730, hy + 60, 690, hy + 150); ctx.bezierCurveTo(560, hy + 210, 300, hy + 200, -200, hy + 170); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.strokeStyle = 'rgba(14,9,7,.5)'; ctx.lineWidth = 3; for (let i = 0; i < 7; i++) { ctx.beginPath(); ctx.moveTo(-150 + i * 110, hy - 160 + i * 4); ctx.quadraticCurveTo(-120 + i * 110, hy, -150 + i * 110, hy + 160 - i * 4); ctx.stroke(); }
  if (o.lA > .01) { const g = ctx.createLinearGradient(200, 0, 700, 0); g.addColorStop(0, 'rgba(255,214,160,0)'); g.addColorStop(1, `rgba(255,214,160,${(.22 * o.lA).toFixed(3)})`); ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-200, hy - 170); ctx.bezierCurveTo(300, hy - 200, 560, hy - 210, 690, hy - 150); ctx.bezierCurveTo(730, hy - 60, 730, hy + 60, 690, hy + 150); ctx.bezierCurveTo(560, hy + 210, 300, hy + 200, -200, hy + 170); ctx.closePath(); ctx.fill(); ctx.restore(); }
  const reach = o.reach || 0;
  for (const sd of [-1, 1]) { // kollar: omuz → dirsek (kıyıda) → el; yakın kol (sd=1) suya uzanır
    const sh = [650, hy + sd * 150], el = [790, hy + sd * 230], rc = sd > 0 ? reach : 0, hd = [lerp(870, 1060 + (o.drift || 0) * .6, rc), lerp(hy + sd * 175, hy + 110, rc)];
    ctx.fillStyle = '#C9703F'; ctx.strokeStyle = C.ink; ctx.lineWidth = 4;
    const limb = (a, b, w0, w1) => { const d = sub(b, a), n = [-d[1] / len(d), d[0] / len(d)]; ctx.beginPath(); ctx.moveTo(a[0] + n[0] * w0, a[1] + n[1] * w0); ctx.lineTo(b[0] + n[0] * w1, b[1] + n[1] * w1); ctx.lineTo(b[0] - n[0] * w1, b[1] - n[1] * w1); ctx.lineTo(a[0] - n[0] * w0, a[1] - n[1] * w0); ctx.closePath(); ctx.fill(); ctx.stroke(); };
    limb(sh, el, 34, 26); limb(el, hd, 26, 19); for (const [q, rr] of [[el, 26], [sh, 34]]) { ctx.beginPath(); ctx.arc(q[0], q[1], rr, 0, TAU); ctx.fill(); } ctx.beginPath(); ctx.arc(el[0], el[1], 26, sd > 0 ? -1.2 : 1.2 - PI, sd > 0 ? 1.4 : PI - 1.4 + PI); ctx.stroke();
    ctx.beginPath(); ctx.ellipse(hd[0] + 18, hd[1], 30, 22, Math.atan2(hd[1] - el[1], hd[0] - el[0]), 0, TAU); ctx.fill(); ctx.stroke();
  }
  // başın tepesi: koyu sır saç, bukle kazımaları; kulaklar iki yanda (başın çevresinde halka ya da bant yok)
  ctx.fillStyle = '#C9703F'; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; for (const sd of [-1, 1]) { ctx.beginPath(); ctx.ellipse(770, hy + sd * 108, 22, 14, 0, 0, TAU); ctx.fill(); ctx.stroke(); }
  ctx.fillStyle = '#0E0907'; ctx.beginPath(); ctx.ellipse(760, hy, 128, 112, 0, 0, TAU); ctx.fill();
  ctx.strokeStyle = 'rgba(201,112,63,.7)'; ctx.lineWidth = 3; for (let i = 0; i < 22; i++) { const a = i / 22 * TAU, rr = 40 + (i % 3) * 26; ctx.beginPath(); ctx.arc(760 + Math.cos(a) * rr, hy + Math.sin(a) * rr * .85, 13, a, a + 2.4); ctx.stroke(); }
  ctx.restore();
  // iki bedenin çevresinde kapanan halka (P093; tek başın çevresinde değil: hale okunmasın)
  if (o.ring > .01) { ctx.save(); ctx.strokeStyle = 'rgba(226,150,96,.9)'; ctx.lineWidth = 6; ctx.lineCap = 'round'; ctx.beginPath(); ctx.ellipse(ex + 30 + (o.drift || 0) * .5, hy, 700, 330, 0, PI, PI + TAU * o.ring); ctx.stroke(); ctx.restore(); }
  ctx.restore();
  if (o.close > .01) { ctx.save(); baseT(ctx); const g = ctx.createRadialGradient(W / 2, H / 2, lerp(1100, 380, o.close), W / 2, H / 2, lerp(1300, 620, o.close)); g.addColorStop(0, 'rgba(5,3,2,0)'); g.addColorStop(1, 'rgba(5,3,2,.95)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
}
// önden yüz (yalnız sudaki yansıma için; soluk, vazo dilinde sade): alnı sola dönük
function s2_onYuz(c, x, y, s, t) {
  c.save(); c.translate(x, y); c.rotate(-PI / 2); c.scale(s, s);
  c.fillStyle = '#C9703F'; c.strokeStyle = C.ink; c.lineWidth = 4;
  c.beginPath(); c.ellipse(0, 10, 100, 128, 0, 0, TAU); c.fill(); c.stroke();
  c.fillStyle = '#0E0907'; c.beginPath(); c.moveTo(-104, 0); c.bezierCurveTo(-120, -110, -40, -150, 0, -150); c.bezierCurveTo(40, -150, 120, -110, 104, 0); c.bezierCurveTo(90, -60, 40, -86, 0, -84); c.bezierCurveTo(-40, -86, -90, -60, -104, 0); c.fill();
  c.strokeStyle = 'rgba(201,112,63,.7)'; c.lineWidth = 3; for (let i = 0; i < 9; i++) { const a = PI + .2 + i * .34; c.beginPath(); c.arc(Math.cos(a) * 100, -40 + Math.sin(a) * 80, 12, a, a + 2.2); c.stroke(); }
  c.strokeStyle = C.ink; c.lineWidth = 4; c.lineCap = 'round';
  const bl = blinkAt(t, 5);
  for (const sd of [-1, 1]) { c.beginPath(); c.moveTo(sd * 62, -22); c.quadraticCurveTo(sd * 38, -36, sd * 16, -26); c.stroke();
    c.beginPath(); c.moveTo(sd * 62, -6); c.quadraticCurveTo(sd * 38, -22 * (1 - bl) - 6, sd * 14, -6); c.quadraticCurveTo(sd * 38, 8 * (1 - bl) - 6, sd * 62, -6); c.stroke(); if (bl < .5) { c.fillStyle = C.ink; c.beginPath(); c.arc(sd * 36, -7, 7, 0, TAU); c.fill(); } }
  c.beginPath(); c.moveTo(0, -12); c.lineTo(-4, 40); c.quadraticCurveTo(4, 50, 12, 42); c.stroke();
  c.beginPath(); c.moveTo(-22, 74); c.quadraticCurveTo(0, 80, 22, 74); c.stroke();
  c.restore();
}
// kapalı pınar (P087), tur 2: organik kıyılı pınar (dik yamuk küvet/mezar gibi okunuyordu). level 0..1 su yükselir (iç duvar örtülür);
// notch 0..1 su sağ kıyıdaki kuru oluğa dil gibi uzanır ama oluğun ağzındaki taş onu kapatır, geri çekilir; inward: halkalar içe döner. push 0..1 kamera oluğa yaklaşır (ikinci ölçek)
function s2_pinar(ctx, t, st, o) {
  baseT(ctx); glaze(ctx, 960, 760, 1100, 'rgba(120,48,22,.45)');
  camAt(ctx, ...camMix(s2_cam(st, [920, 600, 1.12], [1010, 610, 1.16]), [1530, 690, 2.05], E.io2(clamp(o.push || 0))));
  const gy = 560, cx = 940, cy = 730, rx = 600, ry = 128;
  const rim = (k = 1, dy = 0) => { const P = []; for (let i = 0; i < 48; i++) { const a = i / 48 * TAU, n = .5 * Math.sin(a * 3 + 1) + .35 * Math.sin(a * 5 + 2.3) + .2 * Math.sin(a * 9 + .4); /* kapalı (periyodik) kıyı dalgası */ P.push([cx + Math.cos(a) * rx * k * (1 + .07 * n), cy + dy + Math.sin(a) * ry * k * (1 + .14 * n)]); } return P; };
  const shape = (c, P) => { c.beginPath(); P.forEach((q, i) => i ? c.lineTo(...q) : c.moveTo(...q)); c.closePath(); };
  groundBand(ctx, gy, -600, 2800, { h: 1000 });
  for (const [x, sc, sd] of [[140, 1.8, 3], [420, 1.4, 6], [1780, 1.9, 8], [2050, 1.5, 5]]) vaseTree(ctx, x, gy, sc, sd, t, { branches: 7, reach: 110 });
  // oluk: sağ kıyıdan dışarı (kuru, kil rengi), ağzında kapatan taş
  const R = [cx + rx - 6, cy + 4], oy = x => cy + 4 + Math.sin((x - R[0]) * .006) * 18;
  ctx.save(); ctx.beginPath(); ctx.moveTo(R[0] - 30, oy(R[0]) - 22); for (let x = R[0]; x <= 2400; x += 30) ctx.lineTo(x, oy(x) - 22); for (let x = 2400; x >= R[0] - 30; x -= 30) ctx.lineTo(x, oy(x) + 22); ctx.closePath();
  ctx.fillStyle = '#3A1B0D'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke(); ctx.restore();
  // pınarın iç duvarı (su alçakken görünür) ve kıyı çizgisi
  const P = rim(); shape(ctx, P); ctx.fillStyle = '#2A140A'; ctx.fill();
  ctx.save(); shape(ctx, P); ctx.clip();
  const k = lerp(.66, .985, o.level), W2 = rim(k, (1 - k) * ry * .55);
  shape(ctx, W2); ctx.fillStyle = '#050302'; ctx.fill();
  ctx.save(); shape(ctx, W2); ctx.clip();
  waterBody(ctx, c => shape(c, W2), cy - ry, t, { a: .2, seed: 87, span: [cx - rx, cx + rx], n: 20, depth: ry * 1.8 });
  mirror(ctx, c => { for (const [x, sc, sd] of [[420, 1.4, 6], [1780, 1.9, 8]]) vaseTree(c, x, gy, sc, sd, t, { branches: 7, reach: 110 }); }, gy, c => shape(c, W2), t, { a: .22, calm: .9 });
  if (t > o.inward) for (let j = 0; j < 4; j++) { const u = ((t - o.inward) * .45 + j / 4) % 1, r2 = lerp(rx * k * .92, 30, u), a = (1 - u) * clamp((t - o.inward) / .6);
    ctx.strokeStyle = `rgba(226,150,96,${(.7 * a).toFixed(3)})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(cx, cy + (1 - k) * ry * .55, r2, r2 * ry / rx, 0, 0, TAU); ctx.stroke(); }
  ctx.restore();
  shape(ctx, W2); ctx.strokeStyle = 'rgba(232,160,104,.85)'; ctx.lineWidth = 3; ctx.stroke();
  ctx.restore();
  // suyun oluğa uzanan dili: taşa dayanır, geri çekilir
  if (o.notch > .01 && o.level > .8) { const L = 70 * o.notch; ctx.save(); ctx.fillStyle = '#050302'; ctx.strokeStyle = 'rgba(232,160,104,.85)'; ctx.lineWidth = 2.5;
    ctx.beginPath(); ctx.moveTo(R[0] - 20, oy(R[0]) - 16); ctx.quadraticCurveTo(R[0] + L, oy(R[0] + L) - 18, R[0] + L + 8, oy(R[0] + L)); ctx.quadraticCurveTo(R[0] + L, oy(R[0] + L) + 18, R[0] - 20, oy(R[0]) + 16); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore(); }
  shape(ctx, P); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 4; ctx.stroke();
  // oluğun ağzındaki taş (kapalı)
  crag(ctx, [[R[0] + 70, oy(R[0] + 90) + 30], [R[0] + 64, oy(R[0] + 90) - 26], [R[0] + 96, oy(R[0] + 90) - 44], [R[0] + 140, oy(R[0] + 90) - 36], [R[0] + 150, oy(R[0] + 90) + 30]], { fill: '#7E3920', seed: 86, wob: 3, strata: 2, lobes: 1 });
  for (let i = 0; i < 8; i++) { const a = PI * (1.08 + i * .12); grass(ctx, cx + Math.cos(a) * rx * 1.04, cy + Math.sin(a) * ry * 1.06 - 2, 1.5, t, 90 + i); }
  narcissus(ctx, cx - rx * .62, cy - ry * .86, 1.5, t, 5, { dir: 1, h: 56 });
  baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
}
// zeminde akan dere (P088): x0 → x1, flow 0..1 (açılma ve akış), y kanal ekseni
function s2_dere(c, t, flow, x0, x1, y) {
  if (flow <= .005) return;
  const xe = lerp(x0, x1, flow);
  c.save(); c.beginPath(); c.moveTo(x0, y - 12); for (let x = x0; x <= xe; x += 20) c.lineTo(x, y - 12 + Math.sin(x * .01) * 10); for (let x = xe; x >= x0; x -= 20) c.lineTo(x, y + 14 + Math.sin(x * .01) * 10); c.closePath();
  c.fillStyle = '#050302'; c.fill(); c.strokeStyle = PC.clayR; c.lineWidth = 3; c.stroke(); c.clip();
  c.strokeStyle = 'rgba(236,232,222,.5)'; c.lineWidth = 2; for (let i = 0; i < 30; i++) { const x = x0 + ((i * 97 + t * 160) % (x1 - x0)); c.beginPath(); c.moveTo(x, y + Math.sin(x * .01) * 10); c.lineTo(x + 30, y + Math.sin(x * .01) * 10); c.stroke(); }
  c.restore();
}
// taşa takılan akıntı (P089), tur 2: büyük kaya (Eko'nun kayasına benziyordu) yerine dar akıntının içinde küçük, yuvarlak bir çakıl.
// sh 0..1 su çakıla çarpıp geri döner, cl 0..1 yüzey kapanır (yalnız yansıma); çakılın ötesinde oluk kuru
function s2_tasAkinti(ctx, t, st, sh, cl) {
  baseT(ctx); glaze(ctx, 960, 900, 1100, 'rgba(120,48,22,.45)');
  camAt(ctx, ...s2_cam(st, [900, 640, 1.25], [1020, 650, 1.32]));
  const gy = 520, y0 = 640, y1 = 770, xs = 1200, pr = 58, yc = (y0 + y1) / 2;
  groundBand(ctx, gy, -600, 2800, { h: 1000 });
  for (const [x, sc, sd] of [[380, 1.3, 3], [760, 1.0, 8], [1650, 1.4, 6]]) vaseTree(ctx, x, gy, sc, sd, t, { branches: 6 });
  const ch = (xa, xb) => { ctx.beginPath(); ctx.moveTo(xa, y0 + Math.sin(xa * .004) * 8); for (let x = xa; x <= xb; x += 20) ctx.lineTo(x, y0 + Math.sin(x * .004) * 8); for (let x = xb; x >= xa; x -= 20) ctx.lineTo(x, y1 + Math.sin(x * .004 + 1) * 8); ctx.closePath(); };
  ch(xs, 2600); ctx.fillStyle = '#3A1B0D'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke(); // kuru oluk
  ctx.save(); ch(-600, xs + 10); ctx.fillStyle = '#050302'; ctx.fill(); ctx.clip();
  if (cl > .01) { ctx.save(); ctx.globalAlpha = .5 * cl; ctx.translate(0, 2 * y0); ctx.scale(1, -1); vaseTree(ctx, 380, y0, .9, 3, t, { branches: 6 }); vaseTree(ctx, 760, y0, .7, 8, t, { branches: 5 }); ctx.restore(); }
  const dir = lerp(1, -1, sh), sp = 170 * (1 - cl);
  ctx.strokeStyle = `rgba(236,232,222,${(.6 * (1 - cl)).toFixed(3)})`; ctx.lineWidth = 2.4;
  for (let i = 0; i < 22; i++) { const yy = y0 + 14 + (i % 5) * 24, x = ((i * 131 + dir * t * sp) % 1800 + 1800) % 1800 - 600; if (x > xs - pr - 40) continue; ctx.beginPath(); ctx.moveTo(x, yy); ctx.lineTo(x + 36, yy); ctx.stroke(); }
  if (sh > .01 && cl < 1) for (let k = 0; k < 3; k++) { const u = ((t * .8 + k / 3) % 1); ctx.strokeStyle = `rgba(226,150,96,${(.7 * (1 - u) * sh * (1 - cl)).toFixed(3)})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(xs - pr, yc, 20 + u * 110, PI * .6, PI * 1.4); ctx.stroke(); }
  ctx.restore();
  ch(-600, xs + 10); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 3; ctx.stroke();
  // çakıl: yassı, düzensiz (top ya da meyve okunmasın), koyu kil, ince ışık kenarı
  crag(ctx, [[xs - 70, yc + 34], [xs - 66, yc - 6], [xs - 30, yc - 34], [xs + 26, yc - 38], [xs + 64, yc - 12], [xs + 72, yc + 34]], { fill: '#6E331B', seed: 89, wob: 4, strata: 2, lobes: 1 });
  ctx.save(); ctx.strokeStyle = 'rgba(240,190,140,.55)'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(xs - 50, yc - 14); ctx.quadraticCurveTo(xs - 10, yc - 34, xs + 30, yc - 32); ctx.stroke(); ctx.restore();
  for (let i = 0; i < 6; i++) grass(ctx, 120 + i * 300, y0 - 10, 1.6, t, 95 + i);
  baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
}
// Eko (P090, P091), tur 2: kayaya karışmış karanlık kadın figürü (ten koyu kil, gri/beyaz değil; kontur ince kil); yakın kolu yüzünün önünde yapraklı bir dal tutar
// (kol başın arkasında tuhaf duruyordu). Baştan ayağa örtülü değil: yüzün yalnız önünde dal
const S2_EKO = { ...STY.red, fill: '#3A1B0D', white: '#4A2414', red: '#6E2A18', line: '#B9653A', dilute: '#5A2C16' };
function s2_eko(c, x, gy, s, t, a) {
  const f = { x, y: gy - 43 * s, s, dir: -1, sty: S2_EKO, lk: { fem: true, hair: 'long', garment: 'robe', himation: true, robeCol: '#2A140A', himCol: '#4A2214' }, seed: 61, idle: .5, stripe: .4, alpha: a,
    p: { torso: .05, neck: .12, head: .18, hipN: .02, knN: .02, hipF: -.04, knF: .02, shN: .45, elN: 2.2, shF: .12, elF: .4, handN: 'flat', handF: 'flat' } }; // kol gövdenin önünde katlı, el çene hizasında (yumruk ya da kalkık kol yok)
  figure(c, f);
  const { J, M } = joints(c, f), w = jointPt(c, M, J.AN.wr), hd = headPt(c, J, M, [3.2, -5.6]);
  // dal: elden yukarı, yüzün önünden geçer
  const ang = Math.atan2(hd[1] - 40 - w[1], hd[0] - 10 - w[0]) + Math.sin(t * .8) * .03, L = Math.hypot(hd[1] - 40 - w[1], hd[0] - 10 - w[0]) + 30 * s / 3.4;
  c.save(); c.globalAlpha *= Math.min(1, a + .3); c.translate(w[0], w[1]); c.rotate(ang);
  c.strokeStyle = C.ink; c.lineWidth = 4; c.beginPath(); c.moveTo(0, 0); c.lineTo(L, 0); c.stroke();
  for (let k = 0; k < 8; k++) { const xx = L * (.25 + .75 * k / 7); for (const sd of [-1, 1]) { c.save(); c.translate(xx, 0); c.rotate(sd * .9 - .3); c.beginPath(); c.ellipse(13, 0, 14, 5.5, 0, 0, TAU); c.fillStyle = '#7E3920'; c.fill(); c.lineWidth = 1.6; c.stroke(); c.restore(); } }
  c.restore();
}

(() => {
  // ═════════════ D · HAVUZ ═════════════
  // P035 · orta · D01 · Işık şeridi pınara değer: dokunulmamış, gümüş gibi parlak kaynak. Bölüm kartı HAVUZ (ilk 3 sn)
  plan('P035', (ctx, st) => {
    const t = st.t, k0 = PE('P035', 0), k1 = PE('P035', 1);
    const hit = ramp(t, k0 - .4, k0 + .8, E.out2), sil = ramp(t, k1 - .2, k1 + 1.2, E.io2);
    s2_kiyi(ctx, t, { fig: false, cam: s2_cam(st, [1250, 600, 1.12], [1270, 620, 1.2]), lag: 0, bank: true,
      bg: c => { // ağaçların arasından inen ince ışık şeridi (dünyada değil ekranda; hale değil, eğik şerit)
        baseT(c); const g = c.createLinearGradient(1080, 0, 1320, 640); g.addColorStop(0, 'rgba(255,230,180,0)'); g.addColorStop(.5, `rgba(255,226,170,${(.12 * hit).toFixed(3)})`); g.addColorStop(1, `rgba(255,236,190,${(.22 * hit).toFixed(3)})`);
        c.fillStyle = g; c.beginPath(); c.moveTo(1010, 0); c.lineTo(1120, 0); c.lineTo(1420, 640); c.lineTo(1250, 640); c.closePath(); c.fill(); },
      waterFx: (c, wy) => { // ışık suya değip yatay şeritlerle yayılır, sonra gümüş parlar
        const cx = 1330, w = lerp(30, 900, hit);
        const g = c.createLinearGradient(cx - w, 0, cx + w, 0); g.addColorStop(0, 'rgba(230,226,215,0)'); g.addColorStop(.5, `rgba(236,232,222,${(.16 + .3 * sil).toFixed(3)})`); g.addColorStop(1, 'rgba(230,226,215,0)');
        c.fillStyle = g; c.fillRect(cx - w, wy, 2 * w, 420);
        c.strokeStyle = `rgba(245,242,232,${(.25 + .55 * sil).toFixed(3)})`; c.lineCap = 'round';
        for (let i = 0; i < 16; i++) { const y = wy + 10 + i * 22 + i * i * 1.2, L = (60 + hash(i * 3.7) * 220) * hit, x = cx - L / 2 + (hash(i) - .5) * 300 + Math.sin(t * .8 + i) * 8; c.lineWidth = 2 + hash(i * 1.3) * 2; c.beginPath(); c.moveTo(x, y); c.lineTo(x + L, y); c.stroke(); }
      } });
  }, { over: (ctx, st) => s2_bolum(ctx, 'HAVUZ', st.lt, 2.8) });

  // P036 · ayrıntı · D01@ona · Kıyının yakını: hiçbir şey suya değmez (çoban ve keçinin gölgesi, kuş, dal)
  plan('P036', (ctx, st) => {
    const t = st.t, tC = PE('P036', 0), tK = PE('P036', 1), tD = PE('P036', 2);
    s2_kiyi(ctx, t, { fig: false, lag: 0, cam: s2_cam(st, [1240, 640, 2.15], [1460, 640, 2.15]),
      bg: c => { baseT(c); const g = c.createLinearGradient(0, 260, 0, 560); g.addColorStop(0, 'rgba(170,86,44,0)'); g.addColorStop(1, 'rgba(190,100,52,.42)'); c.fillStyle = g; c.fillRect(0, 260, W, 300); }, // ufuk aydınlık: karşı kıyıdan geçen siluetler okunur
      bankN: [[1290, 5, 60], [1318, 8, 48], [1350, 2, 56], [1520, 3, 52]],
      waterFx: (c, wy) => { // tur 2: su yüzü hafif gümüş parlar (P035'in devamı)
        const g = c.createLinearGradient(0, wy, 0, wy + 330); g.addColorStop(0, 'rgba(236,232,222,.16)'); g.addColorStop(1, 'rgba(236,232,222,0)'); c.fillStyle = g; c.fillRect(900, wy, 1200, 330);
        c.strokeStyle = 'rgba(245,242,232,.4)'; c.lineCap = 'round'; for (let i = 0; i < 10; i++) { const y = wy + 14 + i * 26, x = 980 + hash(i * 2.3) * 700 + Math.sin(t * .7 + i) * 6, L = 50 + hash(i * 4.1) * 140; c.lineWidth = 2; c.beginPath(); c.moveTo(x, y); c.lineTo(x + L, y); c.stroke(); } },
      under: c => { // tur 2: çoban (asalı, siyah figür) ve keçisi karşı kıyıdan geçer; kara suda görünmeyen gölge yerine siluet. Kimse suya inmez
        const u = ramp(t, tC - .4, tC + 4.2, E.lin); if (u <= 0 || u >= 1) return;
        const a = clamp(u / .08) * clamp((1 - u) / .08), gyF = KIYI.wy - 16, xs = lerp(1100, 1560, u), s = 1.45;
        c.save(); c.globalAlpha *= a;
        walkScene(c, null, xs, s, t, 1, { ground: groundOf(() => gyF), noCam: true, sty: STY.black, lk: { beard: 'short', hair: 'short', garment: 'short' }, dist: (xs - 1100), stride: 34, lean: .05, seed: 36 });
        // asa
        c.strokeStyle = C.ink; c.lineWidth = 4; c.lineCap = 'round'; c.beginPath(); c.moveTo(xs + 14 * s, gyF - 56 * s); c.lineTo(xs + 20 * s, gyF); c.stroke();
        // keçi: önde, adımları mesafeye bağlı
        const gx = xs + 34 * s, ph = (xs - 1100) / (9 * s) * PI;
        c.fillStyle = C.ink; c.beginPath(); c.ellipse(gx, gyF - 13 * s, 10 * s, 4.6 * s, 0, 0, TAU); c.fill();
        c.beginPath(); c.ellipse(gx + 11 * s, gyF - 18 * s, 3.4 * s, 2.4 * s, -.5, 0, TAU); c.fill();
        c.lineWidth = 1.4 * s; c.beginPath(); c.moveTo(gx + 10 * s, gyF - 20 * s); c.quadraticCurveTo(gx + 8 * s, gyF - 26 * s, gx + 4 * s, gyF - 25 * s); c.stroke(); // boynuz
        c.beginPath(); c.moveTo(gx - 10 * s, gyF - 15 * s); c.lineTo(gx - 13 * s, gyF - 19 * s); c.stroke(); // kuyruk
        for (const [lx, o] of [[-7, 0], [-4, .5], [5, .5], [8, 0]]) { const sw = Math.sin(ph + o * PI) * 1.8 * s; c.beginPath(); c.moveTo(gx + lx * s, gyF - 10 * s); c.lineTo(gx + lx * s + sw, gyF); c.stroke(); }
        c.restore(); },
      post: c => {
        // kuş: suyun üstünden geçer, inmez (vazo kuşu: iki kanat yayı)
        const u = ramp(t, tK - .3, tK + 1.6, E.lin); if (u > 0 && u < 1) { const x = lerp(1060, 1760, u), y = 540 - 30 * Math.sin(PI * u), fl = Math.sin(t * 16) * 7;
          c.save(); c.strokeStyle = C.ink; c.lineWidth = 5; c.lineCap = 'round'; c.beginPath(); c.moveTo(x - 26, y - fl); c.quadraticCurveTo(x - 10, y - 12 - fl, x, y); c.quadraticCurveTo(x + 10, y - 12 - fl, x + 26, y - fl); c.stroke(); c.restore(); }
        // dal: üstten sarkar, sallanır ama düşmez
        const sw = settle(t, tD, .09, 1.6, 1.4) + Math.sin(t * .9) * .015;
        c.save(); c.translate(1560, 500); c.rotate(.55 + sw); c.strokeStyle = C.ink; c.lineWidth = 9; c.lineCap = 'round';
        c.beginPath(); c.moveTo(-300, -40); c.quadraticCurveTo(-120, 0, 60, 70); c.stroke(); c.strokeStyle = PC.clayR; c.lineWidth = 4; c.stroke();
        for (let k = 0; k < 9; k++) { const u2 = k / 9, px = lerp(-280, 50, u2), py = lerp(-36, 66, u2 * u2); for (const sd of [-1, 1]) { c.save(); c.translate(px, py); c.rotate(.5 + sd * .8); c.beginPath(); c.ellipse(13, 0, 13, 4.4, 0, 0, TAU); c.fillStyle = PC.clayR; c.fill(); c.lineWidth = 1.8; c.strokeStyle = C.ink; c.stroke(); c.restore(); } }
        c.restore();
      } });
  });

  // P037 · orta · D02 · Yorgun Narkissos gelir, mızrağını bırakır; ön plandaki gövde kadrajı geçerken uzanmış hâli (kapı C pozu) açılır
  plan('P037', (ctx, st) => {
    const t = st.t, tY = PE('P037', 0), tU = PE('P037', 1), tS = PE('P037', 2), tB = PE('P037', 3);
    const wipe = tU - .15; // ön plan gövdesi ekranın ortasındayken poz değişir
    if (t < wipe) { // yürüyüş: kıyıya gelir, durur, mızrağı yere bırakır
      baseT(ctx); glaze(ctx, 1150, 900, 1150, 'rgba(130,52,24,.5)');
      camAt(ctx, ...s2_cam({ p: ramp(t, st.at, wipe, E.lin) }, [700, 470, .9], [860, 500, .98]));
      const { wy, gy, xe } = KIYI;
      waterBody(ctx, c => c.rect(xe - 10, wy, 4000, 2000), wy, t, { a: .2, seed: 5, span: [xe, 2300], n: 28, depth: 380 });
      farBank(ctx, 1180, 2600, wy, t, 17, { h: 22, grass: 7, fill: '#3A1B0D' });
      ledge(ctx, xe, gy, wy); for (let i = 0; i < 6; i++) grass(ctx, 120 + i * 150, gy + 2, 1.6, t, i + 11);
      const stop = tY - .2, x = lerp(230, 820, E.out2(clamp((t - st.at + .8) / (stop - st.at + .8)))), sd = ramp(t, stop - .3, stop + .25, E.io2);
      let J = null, M = null; const s = 4.4, drop = ramp(t, tY, tY + .7, E.io2);
      walkScene(ctx, null, x, s, t, 1, { ground: groundOf(() => gy), noCam: true, sty: STY.red, lk: LK_NK, dist: x - 230, stand: sd, stripe: .5, lean: .1 + .06 * sd, neck: .12 * sd, head: .2 * sd,
        onJoints: (j, m) => { J = j; M = m; }, p: { shF: lerp(-.55, .1, drop), elF: lerp(-.2, .3, drop) } });
      if (J) { const h = jointPt(ctx, M, J.AF.wr); if (drop < 1) spear(ctx, h, lerp(-1.2, -.2, drop), 62 * s * .9, s * .9); }
      if (drop >= 1 || t > tY + .7) spear(ctx, [x + 40, gy - 3], -.02, 230, 3.6);
      // kıyıya yaklaşırken ışık: su yüzünde gümüş
      ctx.save(); ctx.fillStyle = 'rgba(236,232,222,.08)'; ctx.fillRect(xe, wy, 1400, 300); ctx.restore();
    } else {
      s2_kiyi(ctx, t, { cam: s2_cam({ p: ramp(t, wipe, st.end, E.lin) }, [860, 600, 1.4], [920, 610, 1.48]), lag: refLag(t),
        refA: lerp(.08, .42, ramp(t, tB - .2, tB + 1.0, E.io2)),
        pose: tt => ({ look: ramp(tt, tU, tS, E.io2), reach: ramp(tt, tS, tS + .6, E.io2) * (1 - ramp(tt, tB + .4, tB + 1.2, E.io2)) * .9 }),
        rings: [{ x: 1030, y: KIYI.wy + 3, t0: tS + .55, A: 4, sq: .5, v: 240, lam: 30, k: 1.7, reach: 500, life: 2.0, mask: 30 }],
        under: c => spear(c, [560, KIYI.gy - 3], -.02, 330, 5.2) });
    }
    // ön plan ağaç gövdesi kadrajı soldan sağa geçer (gizli kesme): kaydırmanın parçası
    const u = ramp(t, wipe - .45, wipe + .4, E.io2);
    if (u > 0 && u < 1) { ctx.save(); baseT(ctx); const x = lerp(-420, W + 420, u); ctx.fillStyle = '#0B0605'; ctx.beginPath(); ctx.moveTo(x - 260, -20); ctx.bezierCurveTo(x - 200, 400, x - 300, 700, x - 240, H + 20); ctx.lineTo(x + 250, H + 20); ctx.bezierCurveTo(x + 300, 700, x + 200, 400, x + 270, -20); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = 'rgba(201,112,63,.35)'; ctx.lineWidth = 4; for (const dx of [-140, 30, 160]) { ctx.beginPath(); ctx.moveTo(x + dx, -10); ctx.bezierCurveTo(x + dx + 30, 400, x + dx - 20, 700, x + dx + 10, H + 10); ctx.stroke(); } ctx.restore(); }
  });

  // P038 · yakın · D03 · Yüz ve yansıması: âşık oluş. Yansıma gecikmesi buradan başlar (9 kare)
  plan('P038', (ctx, st) => {
    const t = st.t, tA = PE('P038', 0), tO = PE('P038', 1);
    s2_yakin(ctx, t, { T: { lean0: st.at }, cam: s2_cam(st, [D_XE + 300, D_WY - 120, 1.02], [D_XE + 300, D_WY + 30, 1.06]),
      pose: tt => { const q = dPoseO(tt, { lean0: st.at }); const op = ramp(tt, tA - .05, tA + .25, E.out3); return { ...q, eyeWide: .45 * op, browUp: .35 * op, blink: tt > tA - .35 && tt < tA - .05 ? 1 : (tt < tA - .35 ? undefined : 0), smile: .05 }; },
      rings: [{ x: 1150, y: D_WY + 3, t0: tO, A: 9, sq: .6, v: 300, lam: 60, k: 1.0, reach: 900, life: 3, noLines: true, shear: 1.0 }] });
  });

  // P039 · orta · D04 · Mermer heykel gibi: figür kil kırmızısından lekythos beyazına döner; yalnız doğa kıpırdar
  plan('P039', (ctx, st) => {
    const t = st.t, tH = PE('P039', 0), tK = PE('P039', 1);
    const mar = ramp(t, tH - .1, tH + 1.1, E.io2), tf = Math.min(t, tH - .1); // heykel olunca figürün kendi kıpırtısı durur
    s2_kiyi(ctx, t, { cam: s2_cam(st, [820, 600, 1.42], [960, 600, 1.42]), look: 1, marble: mar, figT: tf, lag: 0,
      pose: () => ({ look: 1, reach: 0 }), refA: .42,
      post: c => { // yapraklar kıpırdar: ön planda sarkan zeytin dalı
        const sw = Math.sin(t * 1.4) * .05 + settle(t, tK, .05, 1.2, 1.2);
        c.save(); c.translate(1180, 330); c.rotate(.35 + sw); c.strokeStyle = C.ink; c.lineWidth = 7; c.lineCap = 'round'; c.beginPath(); c.moveTo(-260, -60); c.quadraticCurveTo(-100, -10, 40, 60); c.stroke(); c.strokeStyle = PC.clayR; c.lineWidth = 3; c.stroke();
        for (let k = 0; k < 8; k++) { const u = k / 8, px = lerp(-240, 30, u), py = lerp(-54, 56, u * u); for (const sd of [-1, 1]) { c.save(); c.translate(px, py); c.rotate(.5 + sd * .8 + Math.sin(t * 2 + k) * .06); c.beginPath(); c.ellipse(11, 0, 11, 3.8, 0, 0, TAU); c.fillStyle = PC.clayR; c.fill(); c.lineWidth = 1.6; c.strokeStyle = C.ink; c.stroke(); c.restore(); } }
        c.restore(); } });
    // figür heykel: tf ile dondurulmuş zaman yalnız figüre etki etsin diye FIG_T sabitlenir (yukarıda pose sabit)
    void tf;
  });

  // P040 · ayrıntı · D04@yıldız · Onun gözünden yansıma: kamera yansıyan yüzün üstünde gezinir (göz → bukleler → boyun)
  plan('P040', (ctx, st) => {
    const t = st.t, tG = PE('P040', 0), tB = PE('P040', 1), tN = PE('P040', 2);
    // yansıyan baş ~ (eye.x, 2*wy - eye.y); kamera yansımanın üstünde: göz → saç → boyun
    const camE = [905, 750, 2.6], camB = [860, 770, 2.6], camN = [935, 700, 2.5];
    const c = tt => tt < tB ? camMix(camE, camB, ramp(tt, tB - .2, tB + 1.2, E.io2)) : camMix(camB, camN, ramp(tt, tN - .2, tN + 1.4, E.io2));
    const cm = t < tB - .2 ? camMix([915, 745, 2.45], camE, st.p * 3) : c(t);
    s2_yakin(ctx, t, { cam: cm, noBank: true, pose: tt => ({ ...dPoseO(tt, {}), smile: .02, eyeWide: .35 }),
      refA: .62, calm: .5,
      refl: (rc, tt, fR) => { const g = ramp(t, tG - .1, tG + .5, E.out2) * (1 - .4 * ramp(t, tB, tB + 1, E.io2)); if (g <= 0) return; const { J, M } = joints(rc, fR), e = headPt(rc, J, M, EYE_Q);
        rc.save(); rc.globalCompositeOperation = 'lighter'; const gr = rc.createRadialGradient(e[0], e[1], 0, e[0], e[1], 26); gr.addColorStop(0, `rgba(255,236,200,${(.55 * g).toFixed(3)})`); gr.addColorStop(1, 'rgba(255,236,200,0)'); rc.fillStyle = gr; rc.beginPath(); rc.arc(e[0], e[1], 26, 0, TAU); rc.fill(); rc.restore(); } });
  });

  // P041 · ters açı · D05 · Tepeden: su çizgisi dikey eksen, kıyının taşı solda; solda gerçek baş, sağda yansıyan yüz (yakın sahne 90° döndürülür)
  plan('P041', (ctx, st) => {
    // tur 2: tepeden açı kaldırıldı (secde/maske okunuyordu). Ters açı = karşı kıyıdan yan bakış: su çizgisi kadrajın tam ortasında, üstte gerçek yüz, altta yansıması;
    // dirsekler kıyıda, baş kalkık; kamera su çizgisi boyunca yavaş kayar. 'seven'de gerçek yüz, 'sevilen'de (9 kare geç) yansıma ışıklanır
    const t = st.t, tS = PE('P041', 0), tV = PE('P041', 1);
    const l1 = ramp(t, tS - .1, tS + .5, E.out2), l2 = ramp(t, tV - .1 + REF_LAG, tV + .5 + REF_LAG, E.out2);
    s2_flip(ctx, g => s2_yakin(g, t, { cam: s2_cam(st, [D_XE + 250, D_WY + 10, .97], [D_XE + 360, D_WY + 10, 1.0]), noBank: true, light: .12 + .4 * l1, refA: .46 + .3 * l2,
      pose: tt => ({ ...dPoseO(tt, {}), smile: .1, mouthFlat: true, eyeWide: .2 }),
      refl: (rc, tt, fR) => { if (l2 <= .01) return; const { J, M } = joints(rc, fR), e = headPt(rc, J, M, [2.5, -6]);
        rc.save(); rc.globalCompositeOperation = 'lighter'; const gr = rc.createRadialGradient(e[0], e[1], 0, e[0], e[1], 260); gr.addColorStop(0, `rgba(255,214,160,${(.22 * l2).toFixed(3)})`); gr.addColorStop(1, 'rgba(255,214,160,0)'); rc.fillStyle = gr; rc.fillRect(e[0] - 300, e[1] - 300, 600, 600); rc.restore(); } }), { meander: false });
  });

  // P042 · orta · D06 · Suya eğilip yaklaşır (değmeden), kollarını daldırır; yansıma halkalarla kırılır; eller boş çıkar, damlalar
  plan('P042', (ctx, st) => {
    const t = st.t, tY = PE('P042', 0), tK = PE('P042', 1), tB = PE('P042', 2);
    const dive = tt => ramp(tt, tK - .2, tK + .35, E.io2) * (1 - ramp(tt, tB, tB + .7, E.io2));
    const rings = [{ x: 1090, y: KIYI.wy + 3, t0: tK + .1, A: 40, sq: .55, v: 600, lam: 120, k: 1.1, reach: 1400, life: 4, shear: 2.2, noLines: true },
      { x: 1090, y: KIYI.wy + 3, t0: tK + .1, A: 1, sq: .55, v: 700, lam: 90, k: .9, reach: 1600, life: 3.5, mask: 60 },
      { x: 1080, y: KIYI.wy + 3, t0: tB + .55, A: 4, sq: .55, v: 260, lam: 30, k: 1.6, reach: 500, life: 2, mask: 30 }];
    s2_kiyi(ctx, t, { cam: s2_cam(st, [900, 620, 1.52], [960, 625, 1.52]), rings, warpBox: [970, 640, 1700, 1300],
      pose: tt => { const dv = dive(tt), lean = ramp(tt, tY - .1, tY + .9, E.io2) * (1 - .3 * dv);
        return { look: 1, head: .1 * lean, neck: .08 * lean, hN: [lerp(970, 1095, dv), lerp(617, 690, dv)], hF: [lerp(959, 1060, dv), lerp(618, 688, dv)], handN: 'open', wrA: lerp(.12, 1.3, dv) }; },
      post: c => { // eller çıkınca damlalar
        for (let i = 0; i < 4; i++) { const t0 = tB + .45 + i * .13, u = clamp((t - t0) / .35); if (u <= 0 || u >= 1) continue; c.save(); c.fillStyle = '#F2E6CE'; c.strokeStyle = C.ink; c.lineWidth = 1.2; c.beginPath(); c.ellipse(1060 + i * 12, lerp(608, 640, u * u), 3, 4.5, 0, 0, TAU); c.fill(); c.stroke(); c.restore(); } } });
  });

  // P043 · yakın · D07 · Yansıma toparlanır; kamera yansımadan gerçek yüze çıkar. Soru (üst yarı)
  plan('P043', (ctx, st) => {
    const t = st.t, tBz = PE('P043', 0), tBs = PE('P043', 1);
    const up = ramp(t, tBs - .2, tBs + 1.4, E.io2);
    s2_yakin(ctx, t, { cam: camMix([D_XE + 330, D_WY + 120, 1.02], [D_XE + 320, D_WY - 60, 1.02], up), pose: tt => ({ ...dPoseO(tt, {}), smile: -.1, brow: .1 }),
      rings: [{ x: 1080, y: D_WY + 4, t0: st.at - 2.0, A: 30, sq: .62, v: 500, lam: 120, k: 1.2, reach: 1500, life: 3.6 + (tBz - st.at), shear: 1.4, noLines: true }] });
  }, { over: (ctx, st) => quote(ctx, 'Bilse, kalkıp gider miydi?', 1480, 170, st.t - PE('P043', 1) + .2, { px: 72, maxW: 640 }) });

  // P044 · geniş · D08 · Kıyının kenarına hikâyenin dışından biri gelir: togalı şair silueti (Ovidius); durur, elini gence uzatır
  plan('P044', (ctx, st) => {
    const t = st.t, tO = PE('P044', 0), tD = PE('P044', 1), tS = PE('P044', 2);
    const x = lerp(-120, 470, E.out2(clamp((t - tO + .4) / (tD - tO + .6)))), stand = ramp(t, tD - .3, tD + .3, E.io2), arm = ramp(t, tS - .1, tS + .9, E.io2);
    const lag = refLag(t);
    s2_genis(ctx, t, { cam: s2_cam(st, [900, 560, 1.0], [1000, 560, 1.0]), refA: .42, midTree: false, ground: () => s2_rafW(ctx),
      fig: (c, refl) => {
        const tt = refl ? t - lag : t;
        withFigT(tt, () => figure(c, s2_proneW(c, tt, { reach: 0, head: .05 })));
        if (stand < 1) s2_ovid(c, x, 760, 3.3, t, { walk: stand, dist: x + 400, arm }); else s2_ovid(c, x, 760, 3.3, t, { arm, lean: .02 + .03 * arm });
      } });
  }, { over: (ctx, st) => etiket(ctx, 'OVİDİUS · Dönüşümler, MS 8', 560, 300, st.t - PE('P044', 0), 5.5) });

  // P045 · ters açı · D09 · Şairin omzunun üstünden genç: yine suya uzanır, eli suda boşa kapanır
  plan('P045', (ctx, st) => {
    const t = st.t, tK = PE('P045', 0), tY = PE('P045', 1);
    const reach = tt => ramp(tt, tK - .1, tK + .7, E.io2) * (1 - .35 * ramp(tt, tY + .5, tY + 1.2, E.io2));
    s2_kiyi(ctx, t, { cam: s2_cam(st, [980, 590, 1.38], [1000, 600, 1.46]),
      pose: tt => ({ look: 1, reach: reach(tt), handN: tt > tY ? 'fist' : 'open' }),
      rings: [{ x: 1022, y: KIYI.wy + 3, t0: tY, A: 6, sq: .5, v: 260, lam: 34, k: 1.5, reach: 500, life: 2.2, mask: 30 }],
      post: c => s2_omuz(c, t, 0) });
  }, { over: (ctx, st) => kunye(ctx, 'Ovidius, Dönüşümler III 432–434', st.lt, st.d, { x: 1800, align: 'right' }) });

  // P046 · ayrıntı · D09@gördüğün · Yansıma 'gölge'ye döner: kırmızı figürden siyah figüre; su kil rengine açılır
  plan('P046', (ctx, st) => {
    const t = st.t, tY = PE('P046', 0), tG = PE('P046', 1);
    const u = ramp(t, tY - .1, tG + .2, E.io2);
    s2_yakin(ctx, t, { cam: s2_cam(st, [905, 790, 2.05], [905, 780, 1.88]), noBank: true, reflNoJaw: true, pose: tt => ({ ...dPoseO(tt, {}), smile: 0, mouthFlat: true }), // tur 2: yansıma nötr (gülümseyen gölge-ikiz ürkütücüydü)
      refA: lerp(.55, .95, u),
      waterFx: (c, wy) => { c.fillStyle = `rgba(201,112,63,${(.62 * u).toFixed(3)})`; c.fillRect(-3000, wy, 9000, 3000); },
      reflTint: c => { c.fillStyle = `rgba(14,9,7,${(.96 * u).toFixed(3)})`; c.fillRect(-3000, -3000, 9000, 9000); } });
  });

  // P047 · orta · D10 · Konuşan şair solda önde; omzunun yanından kıyıda genç ve yansıması; her kıpırtıda yansıma 9 kare geç
  plan('P047', (ctx, st) => {
    const t = st.t, tG = PE('P047', 0), tK = PE('P047', 1), tGi = PE('P047', 2), tGb = PE('P047', 3);
    const arm = ramp(t, tG - .2, tG + .6, E.io2) * (1 - ramp(t, tGb, tGb + .8, E.io2));
    s2_kiyi(ctx, t, { cam: s2_cam(st, [700, 470, 1.16], [820, 480, 1.16]),
      pose: tt => { const nod = ramp(tt, tG, tG + .5, E.io2) * (1 - ramp(tt, tK, tK + .4, E.io2)); const rise = ramp(tt, tGi - .1, tGi + .5, E.out2) * (1 - ramp(tt, tGb - .1, tGb + .6, E.io2));
        return { look: 1, head: .14 * nod - .5 * rise, neck: .05 * nod - .5 * rise }; },
      post: c => { s2_ovid(c, 300, KIYI.gy + 110, 6.0, t, { arm, head: -.05 }); } });
  });

  // P048 · geniş · D11 · Zaman geçer, o aynı yerde: gün batar, gece (yıldızlar nokta), şafak; yanında dokunulmamış ekmek ve meyve
  plan('P048', (ctx, st) => {
    const t = st.t, tB = PE('P048', 0), tA = PE('P048', 1), tU = PE('P048', 2), tK = PE('P048', 3);
    const set = ramp(t, tB - .2, tB + 1.4, E.io2), night = ramp(t, tU - .4, tU + .5, E.io2) * (1 - ramp(t, tK - .1, tK + 1.2, E.io2)), dawn = ramp(t, tK - .1, tK + 1.4, E.io2);
    const lag = refLag(t);
    s2_genis(ctx, t, { cam: s2_cam(st, [940, 560, 1.0], [1020, 560, 1.0]), midTree: false,
      warm: `rgba(${lerp(170, 60, night) | 0},${lerp(70, 40, night) | 0},${lerp(30, 50, night) | 0},${(.5 - .2 * night).toFixed(2)})`,
      sky: c => { // güneş batar (sol üst), gece noktalar, şafak sağdan
        const sy = lerp(300, 700, set), sa = 1 - night;
        if (sa > .02 && set < 1) { c.save(); c.globalAlpha = sa; disk(c, 380, sy, 46, '#E7A04E'); c.restore(); }
        if (night > .02) { c.save(); c.globalAlpha = night; const r = rng(77); c.fillStyle = '#F3E6C8'; for (let i = 0; i < 70; i++) { const x = r() * 2200 - 140, y = 60 + r() * 600, s = 1.2 + r() * 1.8; c.beginPath(); c.arc(x, y, s * (.7 + .3 * Math.sin(t * 2 + i)), 0, TAU); c.fill(); } c.restore(); }
        if (dawn > .02) { const g = c.createLinearGradient(2100, 700, 1100, 300); g.addColorStop(0, `rgba(232,150,90,${(.5 * dawn).toFixed(3)})`); g.addColorStop(1, 'rgba(232,150,90,0)'); c.fillStyle = g; c.fillRect(-500, -300, 3000, 1100); } },
      ground: () => { s2_rafW(ctx);
        // dokunulmamış ekmek ve meyve (kayanın yanında)
        const a = ramp(t, tA - .3, tA + .4, E.out2); ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = '#B9653A'; ctx.strokeStyle = C.ink; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.ellipse(610, 744, 34, 15, 0, 0, TAU); ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.moveTo(588, 740); ctx.lineTo(632, 740); ctx.stroke();
        for (const [x, y] of [[660, 750], [680, 748], [670, 738]]) { ctx.beginPath(); ctx.arc(x, y, 9, 0, TAU); ctx.fillStyle = '#8E2F1F'; ctx.fill(); ctx.stroke(); } ctx.restore(); },
      dark: .38 * night + .14 * set * (1 - dawn),
      fig: (c, refl) => { const tt = refl ? t - lag : t; withFigT(tt, () => figure(c, s2_proneW(c, tt, { head: .05 }))); } });
  });

  // ═════════════ E · O BENİM ═════════════
  // P049 · ayrıntı · E01 · Yansımanın gözü: gerçek göz kısılır, yansımanın gözü 9 kare sonra. Ön plan sazları kayar (paralaks). Bölüm kartı O BENİM
  plan('P049', (ctx, st) => {
    const t = st.t, tD = PE('P049', 0);
    s2_yakin(ctx, t, { cam: [905 - 280, 580, 1.3], noBank: true, refA: .6,
      pose: tt => ({ ...dPoseO(tt, {}), smile: -.05, brow: .1 + .25 * ramp(tt, tD, tD + .3), blink: .5 * ramp(tt, tD - .05, tD + .25, E.out2) }) });
    // tur 2: ön planda kalın siyah sazlar yansımada 'çubuk' okunuyordu; yerine alt kenarda ince ot tutamları kayar (paralaks), yansımanın yüzüne binmez
    baseT(ctx); const dx = lerp(60, -200, st.p);
    for (let i = 0; i < 5; i++) grass(ctx, 1380 + i * 120 + dx * (1.2 + .1 * i), H + 30, 5.2 + hash(i) * 1.4, t, 140 + i);
  }, { over: (ctx, st) => s2_bolum(ctx, 'BİLMEK', st.lt, 2.5, 470, 760) }); // kart kıyı kayasının üstünde (omuza ve yüzlere binmez) // tur 2: bölüm kartı 'O BENİM' ifşadan 18 sn önce aynı sözü veriyordu

  // P050 · orta · E02 · Tanıma hamlesinin hazırlığı: el kayadan kalkar, yansımanın eli 9 kare geç gelir (iki el aynı karede)
  plan('P050', (ctx, st) => {
    const t = st.t, tU = PE('P050', 0);
    s2_kiyi(ctx, t, { cam: s2_cam(st, [1010, 640, 1.85], [1050, 645, 1.85]), lag: REF_LAG, refA: .5,
      pose: tt => ({ look: 1, reach: ramp(tt, tU - .1, tU + 1.0, E.io2) * .85, handN: 'point' }) });
  });

  // P051 · yakın · E02@gülümseyince · Gülümser, ağlar; yansıma 9 kare geç; gözde yaş, sonra yansımanın gözünde
  plan('P051', (ctx, st) => {
    const t = st.t, tG = PE('P051', 0), tA = PE('P051', 1), tY = PE('P051', 2);
    const tear = ramp(t, tA, tA + .8, E.out2), tearR = ramp(t, tY - .2 + REF_LAG, tY + .6 + REF_LAG, E.out2);
    s2_yakin(ctx, t, { cam: s2_cam(st, [D_XE + 300, D_WY + 110, 1.18], [D_XE + 300, D_WY - 60, 1.18]), tearEye: tear, tearEyeR: tearR,
      pose: tt => { const sm = ramp(tt, tG - .1, tG + .5, E.out2) * (1 - ramp(tt, tA - .2, tA + .5, E.io2)), cr = ramp(tt, tA - .2, tA + .6, E.io2);
        return { ...dPoseO(tt, {}), smile: .55 * sm - .35 * cr, brow: .2 + .5 * cr, browUp: .25 * cr }; } });
  });

  // P052 · ayrıntı · E02@sudaki#1 · Yansımanın dudakları kıpırdar: ağzından çıkan (harfsiz) yazı şeridi yüzeye çarpıp dağılır
  plan('P052', (ctx, st) => {
    const t = st.t, tK = PE('P052', 0), tU = PE('P052', 1);
    s2_yakin(ctx, t, { cam: s2_cam(st, [905, 700, 2.0], [905, 690, 2.12]), noBank: true, refA: .66,
      pose: tt => ({ ...dPoseO(tt, {}), smile: -.1, mouthOpen: tt > tK - .2 && tt < tU + .6 ? 1.1 * Math.max(0, Math.sin((tt - tK) * 11)) : 0 }),
      post: (c, I) => { // yazı şeridi: yansıyan ağızdan yüzeye doğru; yüzeyi geçemez, dağılır
        const mo = headPt(c, I.J, I.M, [5.4, -3.2]), mx = mo[0], my = 2 * I.wy - mo[1], wy = I.wy, u = ramp(t, tK, tU, E.lin), hit = ramp(t, tU - .1, tU + .9, E.out2);
        c.save(); c.beginPath(); c.rect(0, wy + 2, 4000, 2000); c.clip(); c.strokeStyle = 'rgba(226,150,96,.75)'; c.lineCap = 'round'; c.lineWidth = 5;
        if (hit <= 0) { const L = u; c.beginPath(); for (let k = 0; k <= 24 * L; k++) { const v = k / 24, x = mx + v * 140 + Math.sin(v * 9 + t * 4) * 10, y = lerp(my, wy + 8, v); k ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke(); }
        else for (let k = 0; k < 9; k++) { const a = (k - 4) * .35, d = hit * (60 + 14 * k), x = mx + 140 + Math.sin(a) * d, y = wy + 10 + Math.abs(Math.cos(a)) * 10 * hit; c.globalAlpha = 1 - hit; c.beginPath(); c.moveTo(x - 10, y); c.lineTo(x + 10, y + 2); c.stroke(); }
        c.restore(); } });
  });

  // P053 · yakın · E03 · Tanıma hamlesi (kapı D_benim): parmak suya değer, 'benim'de iki parmak buluşur, gecikme sıfırlanır; irkilme. Sessizlikte kilitli yansıma
  plan('P053', (ctx, st) => {
    // tur 2: iki yüz de tam kadrajda (kamera su çizgisinde); 'benim'e kadar âşık gülümseme, 'benim'de gülümseme düşer, göz açılır ve açık kalır;
    // yansıma aynı kareye oturur: gecikme sıfırlanır, yansıma bir an parlar (temas noktasında ışık, yüzeyde ışık çizgisi)
    const t = st.t, T = { son: PE('P053', 0), ben: PE('P053', 1), back: PE('P053', 3), lean0: st.at }, b = T.ben;
    const flash = ramp(t, b - .04, b + .1, E.out2) * (1 - ramp(t, b + .35, b + 1.5, E.io2)), lock = ramp(t, b, b + .45, E.out3);
    s2_yakin(ctx, t, { T, cam: s2_cam(st, [D_XE + 450, D_WY + 6, .84], [D_XE + 440, D_WY + 6, .9]), refA: lerp(.46, .86, lock) + .14 * flash,
      pose: tt => { const q = dPoseO(tt, T), pre = 1 - ramp(tt, b - .05, b + .12, E.out3), op = ramp(tt, b - .02, b + .12, E.out3);
        return { ...q, smile: lerp(-.9, .45, pre), eyeWide: Math.max(q.eyeWide || 0, .6 * op), browUp: Math.max(q.browUp || 0, .35 * op), blink: tt > b - .3 && tt < b + 3.2 ? 0 : q.blink }; },
      post: (c, I) => { s2_parilti(c, D_TOUCH.tip[0] + 4, I.wy + 2, flash); } });
  }, { over: (ctx, st) => { const b = PE('P053', 1);
    // 'O benim.' sağdaki boş alanda, vazo ressamının fırça yazısı (dipinto), büyük kırmızı; yüzün üstüne binmez
    if (!NOTEXT && st.t > b) txtDipinto(ctx, 'O BENİM.', 1455, 235, 112, ramp(st.t, b, b + .3, E.lin), { col: '#D2492E', w: 700, ls: 12, a: 1 - ramp(st.t, PE('P053', 3) + 1.2, PE('P053', 3) + 1.8) });
    kunye(ctx, 'Ovidius, Dönüşümler III 463 · iste ego sum', st.t - b - .4, st.end - b - .3, { x: 1800, align: 'right' }) } });

  // P054 · geniş · E05 · Geri çekilmiş manzara: o hâlâ kıyıda; arkasındaki patika ışıkla açılır ve söner
  plan('P054', (ctx, st) => {
    const t = st.t, tA = PE('P054', 0), tM = PE('P054', 1), tG = PE('P054', 2);
    const li = ramp(t, tM - .1, tM + .8, E.out2) * (1 - ramp(t, tG, tG + 1.0, E.io2));
    s2_genis(ctx, t, { cam: camMix([940, 560, 1.06], [760, 540, 1.0], ramp(t, tA - .2, st.end, E.sine)), midTree: false,
      ground: (c, gy) => { s2_rafW(c); s2_patika(c, gy, li); },
      fig: (c, refl) => withFigT(t, () => figure(c, s2_proneW(c, t, { head: .05 }))) });
  });

  // P055 · ters açı · E06 · Sırttan: kamera omzunun arkasında; yüzü yalnız yansımada. Su parıltısı yükselir, yüzün kenarını ısıtır; başını ellerinin arasına alır
  plan('P055', (ctx, st) => {
    // tur 2: omuz üstü (karşı kıyı ekseni: yansıma solda, genç sağ ön planda); başın arkasında disk ya da ışık yok, ışık yalnız suda
    const t = st.t, tY = PE('P055', 0), tP = PE('P055', 1);
    const glow = ramp(t, tY - .2, tY + 1.2, E.io2), hands = ramp(t, tP - .2, tP + .7, E.io2);
    s2_flip(ctx, g => s2_yakin(g, t, { cam: s2_cam(st, [960, 770, 1.12], [960, 755, 1.18]), noBank: true, refA: .72, noReal: true, lag: 0,
      waterFx: (c, wy) => { const gr = c.createRadialGradient(1000, wy + 160, 0, 1000, wy + 160, 560); gr.addColorStop(0, `rgba(255,214,150,${(.08 + .26 * glow).toFixed(3)})`); gr.addColorStop(1, 'rgba(255,214,150,0)'); c.fillStyle = gr; c.fillRect(0, wy, 3000, 900); },
      handHead: tt => ramp(tt, tP - .2, tP + .7, E.io2), pose: tt => ({ ...dPoseO(tt, {}), smile: 0, mouthFlat: true, brow: -.1 + .3 * hands, browUp: .15 }) }), { meander: false });
    s2_omuzNk(ctx, t, hands);
    baseT(ctx); meander(ctx, -400, 2400, 0, 36, PC.clayR, PC.glaze);
  }, { over: (ctx, st) => kunye(ctx, 'Ovidius, Dönüşümler III 464', st.lt, st.d) });

  // P056 · orta · E07 · Kıyıyı kavramış; eli yansımanın yüzüne çok yakın, değmez; 'SAHİP' yazıda kırmızı yanar; el boş kapanır
  plan('P056', (ctx, st) => {
    // tur 2: tanımadan sonra eksen değişir (karşı kıyıdan): kaya sağda, su solda
    const t = st.t, tI = PE('P056', 0), tS = PE('P056', 1), tY = PE('P056', 2);
    s2_flip(ctx, g => s2_kiyi(g, t, { cam: s2_cam(st, [930, 545, 1.42], [1000, 545, 1.42]), meander: false,
      pose: tt => ({ look: 1, reach: ramp(tt, tI - .1, tI + 1.2, E.io2) * .95, handN: tt > tY + .1 ? 'fist' : 'open' }) }));
  }, { over: (ctx, st) => s2_sahipSatir(ctx, st) });

  // P058 · ayrıntı · E08@söz · LEVHA · Uçan 'SAHİP' suya düşer, yansımanın dudaklarında durur. Söz geri döndü
  plan('P058', (ctx, st) => {
    const t = st.t, tD = PE('P058', 0), Q = [];
    s2_flip(ctx, g => s2_yakin(g, t, { cam: s2_cam(st, [920, 690, 1.9], [920, 690, 2.0]), noBank: true, refA: .66, pose: tt => ({ ...dPoseO(tt, {}), smile: 0, mouthFlat: true }),
      post: (c, I) => { // SAHİP yukarıdan iner, su yüzünü geçer ve yansıyan dudaklara oturur (yazı aynalanmaz)
        const mo = headPt(c, I.J, I.M, [5.4, -3.2]), m = [mo[0], 2 * I.wy - mo[1]], u = ramp(t, st.at, tD + .1, E.in2), y = lerp(m[1] - 520, m[1], u), wob = settle(t, tD + .1, 6, 2.4, 3);
        s2_yazQ(c, Q, 'SAHİP', [m[0] + 20, y - 12 + wob], 58, 1, { col: '#E0573A', a: y > I.wy ? .9 : 1, clipY: y > I.wy ? I.wy : null }); } }), { meander: false });
    s2_yazBas(ctx, Q);
  }, { over: (ctx, st) => kunye(ctx, 'copia · Ovidius, Dönüşümler III 391 / 466', st.lt, st.d, { y: 150 }) });

  // P059 · ters açı · E09 · Tepeden (su çizgisi dikey): akıntı yansımayı uzaklaştırır, figür ona uzanır; yaprak düşer; yansıma geri gelir, el çekilir
  plan('P059', (ctx, st) => {
    // tur 2: tepeden açı kaldırıldı. Karşı kıyı ekseni, yandan geniş-orta: dirsekler kıyıda, baş kalkık; akıntı yansımayı uzaklaştırır, genç ona uzanır;
    // 'dilek'te suya bir yaprak düşer (halka yok), 'uzak'ta yansıma geri gelir, el çekilir
    const t = st.t, tA = PE('P059', 0), tD = PE('P059', 1), tU = PE('P059', 2);
    const drift = ramp(t, tA - .3, tA + 1.4, E.io2) * (1 - ramp(t, tU - .2, tU + 1.2, E.io2));
    const reach = tt => ramp(tt, tA, tA + 1.2, E.io2) * (1 - ramp(tt, tU, tU + 1.0, E.io2));
    s2_flip(ctx, g => s2_kiyi(g, t, { cam: s2_cam(st, [1020, 650, 1.24], [1080, 655, 1.28]), meander: false, rdx: 150 * drift, calm: 1.1 + 2.2 * drift, refA: .45 - .12 * drift,
      pose: tt => ({ look: 1, reach: .85 * reach(tt), head: -.06 * reach(tt), handN: 'open' }),
      waterFx: (c, wy) => { // akıntı: suyun yüzünde sağa kayan kısa çizgiler (yalnız uzaklaşırken)
        if (drift <= .01) return; c.strokeStyle = `rgba(236,232,222,${(.35 * drift).toFixed(3)})`; c.lineWidth = 2.4; c.lineCap = 'round';
        for (let i = 0; i < 14; i++) { const y = wy + 20 + (i % 7) * 34, x = 1000 + ((i * 173 + t * 120) % 900); c.beginPath(); c.moveTo(x, y); c.lineTo(x + 50, y); c.stroke(); } },
      post: c => { const u = ramp(t, tD - .7, tD + .1, E.in2); if (u <= 0) return; // yaprak: yukarıdan salınarak iner, suya değer ve akıntıyla kayar
        const x = lerp(1380, 1300, u) + Math.sin(u * 7) * 40 * (1 - u) + 160 * ramp(t, tD + .1, st.end, E.lin), y = lerp(220, KIYI.wy - 4, u) + (u >= 1 ? Math.sin(t * 2) * 2 : 0);
        c.save(); c.translate(x, y); c.rotate(u < 1 ? Math.sin(u * 9) * .8 : .05); c.beginPath(); c.ellipse(0, 0, 30, 10, 0, 0, TAU); c.fillStyle = PC.clayR; c.fill(); c.strokeStyle = C.ink; c.lineWidth = 2.4; c.stroke(); c.beginPath(); c.moveTo(-26, 0); c.lineTo(26, 0); c.lineWidth = 1.4; c.stroke(); c.restore(); } }));
  }, { over: (ctx, st) => kunye(ctx, 'Ovidius, Dönüşümler III 467', st.lt, st.d, { x: 1800, align: 'right' }) });

  // P061 · orta · E10@şimdi · LEVHA · KENDİNİ TANIMAZSA suda ters yansır; sonu düşer: TANIDI; yazı halkasız batar ve söner
  plan('P061', (ctx, st) => {
    // tur 2: karşı kıyı ekseni; yazı büyük ve parlak. Önce suda ters (yansımış) KENDİNİ / TANIMAZSA; 'tanıdı'da MAZSA düşer, DI gelir ve yazı dikey eksende döner:
    // KENDİNİ TANIDI düz okunur. 'kurtarmadı'da halkasız batar ve söner
    const t = st.t, tT = PE('P061', 0), tK = PE('P061', 1);
    const ap = ramp(t, st.at, st.at + .9, E.out2), drop = ramp(t, tT - .1, tT + .6, E.in2), turn = ramp(t, tT + .1, tT + .9, E.io2), sink = ramp(t, tK - .1, tK + 1.6, E.io2);
    let wyS = 600;
    s2_flip(ctx, g => s2_kiyi(g, t, { cam: s2_cam(st, [1120, 610, 1.0], [1120, 650, 1.0]), meander: false, look: 1, pose: () => ({ look: 1 }), lag: 0, refA: .5,
      post: c => { wyS = s2_scr(c, [0, KIYI.wy], true)[1]; } }));
    const a = ap * (1 - sink); if (a > .01) { // yazı bloğu ekranda (suyun içinde, sol yarı)
      const cx = 560, cy = wyS + 170 + 140 * sink, sy = lerp(-1, 1, turn), px = 96;
      ctx.save(); baseT(ctx); ctx.beginPath(); ctx.rect(0, wyS + 2, W, H); ctx.clip();
      softPanel(ctx, cx, cy, 520, 190, .35 * a);
      ctx.translate(cx, cy); ctx.scale(1, Math.abs(sy) < .04 ? .04 * Math.sign(sy || 1) : sy); ctx.globalAlpha = a;
      const col = mixCol('#E8603F', '#FF8A5C', turn);
      txtDipinto(ctx, 'KENDİNİ', 0, -62, px, 1, { col, w: 700, ls: 10 });
      ctx.font = FONT.baslik(px, 700); ctx.letterSpacing = '10px'; const wT = ctx.measureText('TANI').width, wM = ctx.measureText('TANIMAZSA').width, wD = ctx.measureText('TANIDI').width;
      const L = lerp(wM, wD, drop), x0 = -L / 2;
      txtDipinto(ctx, 'TANI', x0, 62, px, 1, { col, w: 700, ls: 10, align: 'left' });
      ctx.globalAlpha = a * (1 - drop); txtDipinto(ctx, 'MAZSA', x0 + wT, 62 + 160 * drop * (sy < 0 ? -1 : 1), px, 1, { col, w: 700, ls: 10, align: 'left' });
      ctx.globalAlpha = a * drop; txtDipinto(ctx, 'DI', x0 + wT, 62, px, 1, { col, w: 700, ls: 10, align: 'left' });
      ctx.restore(); }
  });

  // P062 · yakın · E11 · Gözyaşı halkası (kapı D_halka): damla düşer, halka doğar, yansıma yatay dalga kaydırmasıyla koyu lekeye dağılır
  plan('P062', (ctx, st) => {
    const t = st.t, T = { tear: PE('P062', 0), hit: PE('P062', 1), lean0: st.at - 1 };
    const brk = ramp(t, T.hit, T.hit + .25, E.out2) * (1 - .5 * ramp(t, T.hit + 1.5, T.hit + 3.5, E.io2)), dark = ramp(t, PE('P062', 2) - .2, PE('P062', 2) + .8, E.io2);
    const tx = D_XE + 270, rings = [{ x: tx, y: D_WY + 4, t0: T.hit, A: 70, sq: .62, v: 820, lam: 150, k: 1.4, reach: 1800, life: 4.5, shear: .9, noLines: true },
      { x: tx, y: D_WY + 4, t0: T.hit, A: 1, sq: .62, v: 1000, lam: 115, k: .8, reach: 2600, life: 4.5, mask: 80 }];
    s2_flip(ctx, g => s2_yakin(g, t, { T, rings, cam: camMix([D_XE + 300, D_WY - 60, 1.12], [D_XE + 300, D_WY + 90, 1.12], ramp(t, T.tear, T.hit + .3, E.io2)),
      calm: 1 + 11 * brk, refA: .5 + .3 * (1 - dark),
      pose: tt => ({ ...dPoseO(tt, T), smile: -.45, brow: -.1 }),
      reflTint: c => { c.fillStyle = `rgba(14,9,7,${(.7 * dark).toFixed(3)})`; c.fillRect(-3000, -3000, 9000, 9000); } }), { meander: false });
  });

  // P063 · ters açı · E12 · Suyun içinden yukarı: yüzeyin üstünde açık avuç (dokunmaz), parmak gölgeleri suya düşer; yüzey durulur, el ve yüz toparlanır
  plan('P063', (ctx, st) => {
    const t = st.t, tK = PE('P063', 0), tB = PE('P063', 1);
    const calm = ramp(t, tB - .2, tB + 1.4, E.io2), hand = ramp(t, tK - .4, tK + .4, E.out2);
    s2_flip(ctx, g => s2_altSu(g, t, st, calm, hand));
  });

  // P064 · ayrıntı · E13 · Kıyıdaki ot yaprağında kırağı: güneş vurur, kırağı erir, damla suya düşer
  plan('P064', (ctx, st) => {
    const t = st.t, tB = PE('P064', 0), tK = PE('P064', 1), tE = PE('P064', 2);
    s2_kiragi(ctx, t, st, ramp(t, tB - .2, tB + 1.0, E.io2), ramp(t, tK, tE + .4, E.io2), tE);
  });

  // P065 · orta · E13@o · İncelme: renk solar, kenarlar yumuşar, ışık noktaları; beden yerinde
  plan('P065', (ctx, st) => {
    const t = st.t, tA = PE('P065', 0), tI = PE('P065', 1), tE = PE('P065', 2);
    const fade = .45 * ramp(t, tA - .1, tA + 1.2, E.io2) + .55 * ramp(t, tI, tE + .6, E.io2), mo = ramp(t, tI - .1, tI + 1.0, E.out2);
    s2_flip(ctx, g => s2_kiyi(g, t, { cam: s2_cam(st, [870, 600, 1.5], [870, 600, 1.42]), meander: false, fade, light: .3 * (1 - fade), pose: () => ({ look: 1 }), lag: 0,
      post: c => s2_motes(c, t, 26, 65, 760, 560, 300, 70, .8 * mo) }));
  });

  // P067 · orta · E14@narkissos · İncelmiş Narkissos 'ah' der; kayalardan soluk yankı döner
  plan('P067', (ctx, st) => {
    // tur 2: karşı kıyı ekseni, daha geniş: kıyıdaki soluk beden küçük, karşıda yankının döndüğü kayalar büyük; AH yazıları aynalanmaz
    const t = st.t, tA = PE('P067', 0), tE = PE('P067', 1), Q = [];
    s2_flip(ctx, g => s2_kiyi(g, t, { cam: s2_cam(st, [1140, 520, .98], [1200, 520, .98]), meander: false, fade: 1, light: 0, lag: 0,
      pose: tt => ({ look: 1, mouthOpen: 1.4 * ramp(tt, tA - .1, tA + .15) * (1 - ramp(tt, tA + .6, tA + .9)) }),
      pre: c => s2_uzakKaya(c, 1640, KIYI.wy),
      post: c => { s2_motes(c, t, 22, 66, 760, 560, 300, 70, .6);
        const a1 = ramp(t, tA, tA + .3) * (1 - ramp(t, tA + 1.6, tA + 2.4)); if (a1 > 0) s2_yazQ(c, Q, 'AH', [1080, 470 - 30 * ramp(t, tA, tA + 2)], 70, ramp(t, tA, tA + .4), { col: '#E0573A', a: a1 });
        const a2 = ramp(t, tE, tE + .4) * (1 - ramp(t, tE + 1.6, tE + 2.6)); if (a2 > 0) s2_yazQ(c, Q, 'AH', [1640 - 360 * ramp(t, tE, tE + 2.4), 400], 60, ramp(t, tE, tE + .4), { col: '#E0573A', a: .6 * a2 }); } }));
    s2_yazBas(ctx, Q);
  });

  // P068 · yakın · E15 · Son bakış: incelmiş beden suya son sözü söyler; ELVEDA suya iner
  plan('P068', (ctx, st) => {
    const t = st.t, tA = PE('P068', 0), tE = PE('P068', 1), Q = [];
    s2_flip(ctx, g => s2_yakin(g, t, { cam: camMix([D_XE + 380 - 40 * st.p, D_WY - 50, 1.0 + .06 * st.p], [D_XE + 380 - 40 * st.p, D_WY + 120, 1.0 + .06 * st.p], ramp(t, tE - .3, tE + 1.6, E.io2)), fade: 1, light: 0, lag: 0, refA: .3, noBank: true,
      reflTint: c => { c.fillStyle = 'rgba(232,214,184,.5)'; c.fillRect(-3000, -3000, 9000, 9000); },
      pose: tt => ({ ...dPoseO(tt, {}), smile: -.3, mouthOpen: (tt > tA - .1 && tt < tE + .5 ? .9 * Math.max(0, Math.sin((tt - tA) * 7)) : 0) }),
      post: (c, I) => {
        s2_motes(c, t, 18, 68, I.eye[0] - 120, I.eye[1] + 40, 220, 80, .5);
        const a1 = ramp(t, tA, tA + .3) * (1 - ramp(t, tE - .3, tE + .3)); if (a1 > 0) s2_yazQ(c, Q, 'AH, BOŞUNA SEVİLEN ÇOCUK!', [I.eye[0] + 120, I.eye[1] - 230], 48, ramp(t, tA, tE - .4, E.lin), { col: '#E0573A', a: a1, align: 'left' });
        const u = ramp(t, tE, tE + 1.6, E.io2), a2 = ramp(t, tE, tE + .3) * (1 - ramp(t, tE + 2.2, tE + 3)); if (a2 > 0) { const y = lerp(I.eye[1] + 60, I.wy + 130, u);
          s2_yazQ(c, Q, 'ELVEDA', [I.eye[0] + 150, y], 52, ramp(t, tE, tE + .5), { col: '#E0573A', a: a2 * (y > I.wy ? .75 : 1), clipY: y > I.wy ? I.wy : null }); } } }), { meander: false });
    s2_yazBas(ctx, Q);
  });

  // P070 · orta · E16 · İncelmiş beden başını otların üstüne bırakır; ışık söner, su kararır
  plan('P070', (ctx, st) => {
    // tur 2: karşı kıyı ekseni, alçak kamera (ön planda otlar): baş otlara iner, ışık söner
    const t = st.t, tB = PE('P070', 0), tO = PE('P070', 1);
    const down = ramp(t, tB - .3, tB + 1.4, E.io2), off = ramp(t, tO - .2, tO + 1.6, E.io2);
    s2_flip(ctx, g => s2_kiyi(g, t, { cam: s2_cam(st, [820, 560, 1.34], [900, 570, 1.44]), meander: false, fade: 1, light: 0, lag: 0, refA: .3 * (1 - off),
      pose: () => ({ look: 1 - down, head: 1.0 * down, neck: .9 * down, hN: [lerp(968, 900, down), lerp(617, 611, down)] }),
      under: c => { for (const [x, sd] of [[930, 1], [965, 2], [1000, 3], [895, 4]]) grass(c, x, KIYI.gy - 2, 2.2, t, 70 + sd); },
      post: c => { s2_motes(c, t, 16, 70, 760, 560, 300, 70, .55 * (1 - .6 * off));
        for (let i = 0; i < 7; i++) grass(c, 560 + i * 70, KIYI.gy + 40, 4.2, t, 140 + i); // ön plan otları (alçak kamera)
        c.save(); baseT(c); c.fillStyle = `rgba(6,3,4,${(.35 * off).toFixed(3)})`; c.fillRect(0, 0, W, H); c.restore(); } }));
  });

  // P072 · orta · E17 · Kıyıda periler ağıt yakar (ayakta, elleri başlarında); yamaçlardan soluk dipinto yankı
  plan('P072', (ctx, st) => {
    const t = st.t, tA = PE('P072', 0), tY = PE('P072', 1);
    const h = ramp(t, tA - .3, tA + .8, E.io2);
    s2_genis(ctx, t, { cam: s2_cam(st, [760, 560, 1.55], [860, 560, 1.55]), midTree: false, refA: .38,
      ground: c => s2_rafW(c),
      sky: c => { const a = ramp(t, tY, tY + .5) * (1 - ramp(t, tY + 1.6, tY + 2.6)); if (a > 0) { txtDipinto(c, 'AH', 1240, 380, 40, 1, { col: '#E0573A', a: .5 * a }); txtDipinto(c, 'AH', 1420, 330, 30, 1, { col: '#E0573A', a: .3 * a }); } },
      fig: (c, refl) => { withFigT(t, () => s2_litFig(c, s2_proneW(c, t, { head: .3, neck: .3 }), null, { fade: 1 }));
        // tur 2: üçü de kıyıda (sağdaki suyun içindeydi), dağınık: farklı derinlik, yön ve an
        for (const [x, gy, sc, sd, k, d] of [[372, 772, 3.2, 51, .3, 1], [548, 754, 2.85, 52, 0, 1], [706, 766, 3.05, 53, .55, -1]]) s2_peri(c, x, gy, sc, t, sd, ramp(t, tA - .3 + k, tA + .7 + k, E.io2), d); } });
  });

  // P073 · yakın · E17@bedeni · Kayboluş: ot yatağında yalnız ışık noktaları; peri otları aralar, noktalar havalanır ve söner; el boş yere değer
  plan('P073', (ctx, st) => {
    const t = st.t, tA = PE('P073', 0), tY = PE('P073', 1);
    s2_otYatak(ctx, t, st, ramp(t, tA - .3, tA + .6, E.io2), ramp(t, tY - .2, tY + .5, E.io2), tA);
  });

  // P074 · ayrıntı · E17@yerinde · Son noktanın yerinde nergis açar (beyaz, düzensiz oval taç; safran göbek), suya eğilir ve yansır
  plan('P074', (ctx, st) => {
    const t = st.t, tS = PE('P074', 0), tB = PE('P074', 1), tC = PE('P074', 2);
    s2_nergisYakin(ctx, t, st, { open: ramp(t, tS - .4, tB + .9, E.io2), lean: ramp(t, tC - .1, tC + 1.2, E.io2), refA: .55 * ramp(t, tC, tC + 1.0, E.io2), cam: s2_cam(st, [990, 620, 1.27], [990, 615, 1.35]), saffron: ramp(t, tS - .3, tS + .5) });
  });
  // ═════════════ F · AD ═════════════
  // P075 · yakın · F01 · Nergis kıyıda; bölüm kartı AD; dipinto ΝΑΡΚΙΣΣΟΣ çiçeğin yanında belirir, aynı yerde Latince Narcissus'a döner (ekranda tek ad)
  plan('P075', (ctx, st) => {
    const t = st.t, tN = PE('P075', 0), tL = PE('P075', 1);
    s2_nergisYakin(ctx, t, st, { cam: s2_cam(st, [1030, 470, 1.55], [1030, 470, 1.62]), lean: .25, refA: .45,
      extra: c => { const sw = ramp(t, tL - .1, tL + .25, E.io2);
        if (sw < 1) dipintoYaz(c, 'ΝΑΡΚΙΣΣΟΣ', 1180, 300, 40, ramp(t, tN, tN + 1.0, E.lin) * 1, { col: '#E0573A', a: 1 - sw });
        if (sw > 0) { c.save(); c.globalAlpha = sw; c.font = FONT.alinti(58, 600); c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillStyle = '#E0573A'; c.fillText('Narcissus', 1180, 300); c.restore(); } } });
  }, { over: (ctx, st) => s2_bolum(ctx, 'AD', st.lt, 2.0) });

  // P076 · orta · F01@peki · Kamera nergisten geri çekilir; soru üst yarıda; ad harfleri gevşer, suya dökülür, akıntıyla sağa (belgelere) gider
  plan('P076', (ctx, st) => {
    const t = st.t, tG = PE('P076', 0), tK = PE('P076', 1);
    const loose = ramp(t, tG - .1, tG + .6, E.io2), fall = ramp(t, tK - .2, tK + .9, E.in2), flow = ramp(t, tK + .5, st.end + .5, E.in2);
    s2_nergisYakin(ctx, t, st, { cam: s2_cam(st, [1080, 520, 1.25], [1140, 560, .98]), lean: .25, refA: .5,
      extra: (c, I) => { const s = 'ΝΑΡΚΙΣΣΟΣ', h = 40; let x = 1180 - 150;
        for (let i = 0; i < s.length; i++) { const ch = s[i], w = dipinto(c, ch, -9999, 0, h, { a: 0 }), jit = loose * Math.sin(t * 7 + i * 1.7) * 5, d = hash(i * 3.3);
          const y = lerp(300 + jit, I.wy + 30 + d * 40, fall * clamp(fall * 1.3 - d * .3)), xx = x + w / 2 + flow * (500 + d * 300) + loose * (d - .5) * 10;
          c.save(); if (y > I.wy) { c.beginPath(); c.rect(0, I.wy + 1, 4000, 2000); c.clip(); }
          dipinto(c, ch, xx, y, h, { col: '#E0573A', a: (y > I.wy ? .7 : 1) * (1 - .5 * flow) }); c.restore(); x += w + .22 * h; } } });
  }, { over: (ctx, st) => quote(ctx, 'Bir gencin adı nasıl bir kelimeye dönüştü?', W / 2, 190, st.lt - .2, { px: 66, maxW: 1300 }) });

  // P083 · orta · F04@ama · Alacakaranlıkta pınar; 'narsist' yazıları düşer, hiçbir şeye yapışmadan suya değer ve söner (halka yok). Figür yok
  plan('P083', (ctx, st) => {
    const t = st.t, t0 = st.at, tU = PE('P083', 1), tT = PE('P083', 2);
    s2_kiyi(ctx, t, { fig: false, lag: 0, cam: s2_cam(st, [1250, 560, 1.15], [1350, 560, 1.15]), warm: 'rgba(150,72,46,.6)', // tur 2: alacakaranlık ama okunur (8 sn neredeyse siyahtı)
      bg: c => { baseT(c); const g = c.createRadialGradient(1000, 520, 60, 1000, 520, 900); g.addColorStop(0, 'rgba(196,110,70,.38)'); g.addColorStop(1, 'rgba(196,110,70,0)'); c.fillStyle = g; c.fillRect(0, 0, W, H); },
      post: c => { c.save(); const n = 14;
        for (let i = 0; i < n; i++) { const d = hash(i * 5.1), t1 = t0 - .6 + i * ((tT - t0 + .2) / n), u = clamp((t - t1) / 2.2); if (u <= 0 || u >= 1) continue;
          const x = 1000 + d * 820 + Math.sin(t + i) * 10, y = lerp(230, KIYI.wy + 12, E.in2(u)), a = u < .85 ? 1 : 1 - (u - .85) / .15;
          c.globalAlpha = a * .9; c.font = FONT.alinti(46 + Math.round(d * 34), 600); c.textAlign = 'center'; c.fillStyle = '#F2E6CE'; c.fillText('narsist', x, y); }
        c.restore();
        c.save(); baseT(c); c.fillStyle = `rgba(20,12,24,${(.06 + .12 * ramp(t, tU, tT + .5)).toFixed(3)})`; c.fillRect(0, 0, W, H); c.restore(); } });
  });

  // P084 · ayrıntı · F04@bu#1 · Kıyıdaki nergis; su durulur, yansıma netleşir; nergis hafifçe suya eğilir
  plan('P084', (ctx, st) => {
    const t = st.t, tK = PE('P084', 0), tO = PE('P084', 1);
    const net = ramp(t, tK - .2, tK + 1.0, E.io2);
    s2_nergisYakin(ctx, t, st, { cam: s2_cam(st, [1000, 650, 1.7], [1000, 650, 1.8]), lean: .2 + .25 * ramp(t, tO - .1, tO + 1.0, E.io2), refA: lerp(.3, .75, net), calm: lerp(5, .4, net) });
  });

  // P087 · orta-yakın · F07 · Kapalı pınar: su kıyıya kadar yükselir, oluk açılmaya çalışır ama akamaz, halkalar içe döner. Freud'un ilk cümlesi suyun üstünde
  plan('P087', (ctx, st) => {
    const t = st.t, tO = PE('P087', 0), tD = PE('P087', 1), tA = PE('P087', 2), tK = PE('P087', 4);
    // tur 2: iki ölçek tek planda: orta-yakın pınar → 'dışarıya'da kamera oluğa yaklaşır (ayrıntı: su taşa dayanır) → 'akamadığında' geri çekilir, halkalar içe döner
    s2_pinar(ctx, t, st, { level: ramp(t, st.at, tO + 1.5, E.io2) * (1 - .05 * ramp(t, tK, tK + 1)), notch: ramp(t, tD - .1, tD + 1.0, E.io2) * (1 - ramp(t, tA, tA + .8, E.io2)), inward: tA,
      push: ramp(t, tD - .5, tD + .8, E.io2) * (1 - ramp(t, tA + .3, tA + 1.6, E.io2)) });
  }, { over: (ctx, st) => { const g = PE('P087', 3); quote(ctx, 'Güçlü bir benlik sevgisi insanı hastalığa karşı korur.', W / 2, 250, st.t - g, { px: 68, maxW: 1300 }); kunye(ctx, 'Freud, 1914 · s. 11 (çevirimiz)', st.t - PE('P087', 4), 99) } });

  // P088 · geniş · F08@ama · Aynı pınar, geniş: oluk açılır, su dışarı, ormana doğru akar
  plan('P088', (ctx, st) => {
    const t = st.t, tS = PE('P088', 0), tG = PE('P088', 1);
    const flow = ramp(t, tS - .2, tG + .4, E.io2);
    s2_genis(ctx, t, { cam: s2_cam(st, [1100, 560, 1.0], [1260, 560, 1.0]), midTree: false, moreTrees: [[2150, 1.6, 13], [2350, 1.8, 14]],
      ground: c => s2_dere(c, t, flow, 1670, 2400, 790) });
  }, { over: (ctx, st) => quote(ctx, 'Ama sonunda, hastalanmamak için sevmeye başlamak gerekir.', W / 2, 220, st.lt - .3, { px: 66, maxW: 1400 }) });

  // P089 · yakın · F08@engellendiği · Akıntı bir taşa takılır, geri döner; yüzey kapanır, yalnız yansıma kalır
  plan('P089', (ctx, st) => {
    const t = st.t, tS = PE('P089', 0), tH = PE('P089', 1);
    s2_tasAkinti(ctx, t, st, ramp(t, tS - .2, tS + .6, E.io2), ramp(t, tH - .2, tH + 1.4, E.io2));
  }, { over: (ctx, st) => kunye(ctx, 'Freud, 1914', st.lt - .3, st.d) });

  // P090 · geniş · F09 · Karşıtlık (kapak B): solda ışıkta suya bakan Narkissos, sağda karanlıkta kayaya karışmış Eko (yüzü yapraklarla örtülü)
  plan('P090', (ctx, st) => {
    const t = st.t, tB = PE('P090', 0), tI = PE('P090', 1);
    const both = ramp(t, tB - .3, tB + 1.6, E.io2), sh = ramp(t, tI - .2, tI + 1.0, E.io2);
    s2_genis(ctx, t, { cam: camMix([900, 560, 1.35], [1180 + 80 * st.p, 560, 1.0 + .05 * st.p], both), trees: false, refA: .42, nerg: [[975, 11, 50], [1560, 5, 58]],
      ground: (c, gy) => { s2_rafW(c); vaseTree(c, 150, gy, 1.75, 3, t, { branches: 7, reach: 110 }); vaseTree(c, 420, gy, 1.5, 6, t, { branches: 6 }); crag(c, [[1680, 770], [1720, 560], [1820, 420], [1960, 380], [2120, 440], [2240, 620], [2300, 770]], { fill: '#24110A', seed: 55, wob: 6, strata: 3, lobes: 2 }); },
      fig: (c, refl) => { withFigT(t, () => figure(c, s2_proneW(c, t, { head: .05 }))); if (!refl) s2_eko(c, 1900, 768, 3.4, t, 1); },
      post: c => { const g = c.createRadialGradient(1000, 740, 0, 1000, 740, 380); g.addColorStop(0, 'rgba(255,214,160,.16)'); g.addColorStop(1, 'rgba(255,214,160,0)'); c.save(); c.globalCompositeOperation = 'lighter'; c.fillStyle = g; c.fillRect(500, 400, 1000, 700); c.restore();
        const g2 = c.createLinearGradient(1600, 0, 2300, 0); g2.addColorStop(0, 'rgba(5,3,2,0)'); g2.addColorStop(1, `rgba(5,3,2,${(.45 + .2 * sh).toFixed(3)})`); c.fillStyle = g2; c.fillRect(1500, -200, 1200, 1400); } });
  });

  // P092 · yakın · F09@oysa · Narkissos'un gözü suda; arkasında yankı yazıları kayar ve söner
  plan('P092', (ctx, st) => {
    const t = st.t, tA = PE('P092', 0), fd = 1 - ramp(t, tA - .3, tA + 1.0, E.io2);
    s2_yakin(ctx, t, { cam: [D_XE + 300, D_WY - 50, 1.25], lag: 0, refA: .8, pose: tt => ({ ...dPoseO(tt, {}), smile: -.1 }),
      pre: () => { if (fd <= .01) return; const dx = lerp(0, -260, st.p);
        for (const [s, x, y, h, a] of [['AH', 1300, 380, 40, .5], ['ELVEDA', 1500, 300, 30, .35], ['BURADA', 1160, 250, 26, .3], ['AH', 1700, 420, 30, .3]]) txtDipinto(ctx, s, x + dx * (h / 40), y, h, 1, { col: '#E0573A', a: a * fd }); } });
  });

  // P093 · ters açı · F10 · Tepeden: figür ve yansıması kapalı bir halka gibi; havuzun kenarı içe kapanır
  plan('P093', (ctx, st) => {
    // tur 2: tepeden açı kaldırıldı. Üst çapraz geniş: pınar zeminde elips, genç kıyı kayasında, yansıması suda. Su çizgisi pınarın kenarından taşar ve zeminde
    // ikisinin çevresinde (başın değil, iki bedenin) dolanıp kapanır: 'kendini'de başlar, 'sevgisi'nde çevre kararır, 'çıkamadı'da halka kapanır
    const t = st.t, tK = PE('P093', 0), tS = PE('P093', 1), tC = PE('P093', 2);
    const ring = ramp(t, tK - .2, tC + .3, E.io2), close = ramp(t, tS - .2, tC + .8, E.io2) * .8;
    const R = { cx: 1140, cy: 800, rx: 640, ry: 104 };
    const arc = (c, top) => { if (ring <= .005) return; const a1 = (top ? -1 : 1) * PI * ring; c.save(); c.lineCap = 'round';
      c.strokeStyle = 'rgba(5,3,2,.95)'; c.lineWidth = 14; c.beginPath(); c.ellipse(R.cx, R.cy, R.rx, R.ry, 0, Math.min(0, a1), Math.max(0, a1)); c.stroke();
      c.strokeStyle = 'rgba(232,160,104,.95)'; c.lineWidth = 4; c.beginPath(); c.ellipse(R.cx, R.cy, R.rx + 8, R.ry + 6, 0, Math.min(0, a1), Math.max(0, a1)); c.stroke(); c.restore(); };
    s2_genis(ctx, t, { cam: s2_cam(st, [1080, 730, 1.24], [1130, 740, 1.3]), midTree: false, refA: .5,
      ground: c => { s2_rafW(c); arc(c, true); },
      fig: (c, refl) => withFigT(t, () => figure(c, s2_proneW(c, t, { head: .05 }))),
      post: c => { arc(c, false);
        if (close > .01) { c.save(); baseT(c); const g = c.createRadialGradient(W / 2, 600, lerp(1100, 520, close), W / 2, 600, lerp(1300, 900, close)); g.addColorStop(0, 'rgba(5,3,2,0)'); g.addColorStop(1, 'rgba(5,3,2,.9)'); c.fillStyle = g; c.fillRect(0, 0, W, H); c.restore(); } } });
  });

  // P094 · orta · F10@ovidius · Togalı şair kıyının kenarında; elini gence uzatır, sonra döner ve gider; genç kıpırdamaz
  plan('P094', (ctx, st) => {
    const t = st.t, tS = PE('P094', 0), tG = PE('P094', 1);
    const arm = ramp(t, tS - .2, tS + .6, E.io2) * (1 - ramp(t, tG - .2, tG + .3, E.io2)), go = clamp((t - tG - .2) / 2.4);
    s2_kiyi(ctx, t, { cam: s2_cam(st, [760, 480, 1.16], [820, 480, 1.16]), pose: () => ({ look: 1 }), lag: 0,
      post: c => { if (go <= 0) s2_ovid(c, 300, KIYI.gy + 110, 6.0, t, { arm }); else { const x = 300 - 520 * E.in2(go); s2_ovid(c, x, KIYI.gy + 110, 6.0, t, { walk: 0, dist: 300 - x, dir: -1 }); } } });
  }, { over: (ctx, st) => { quote(ctx, '“Seninle gider; eğer sen gidebilirsen.”', 1180, 200, st.t - PE('P094', 0) + .2, { px: 66, maxW: 1100 }); kunye(ctx, 'Ovidius, Dönüşümler III 436', st.t - PE('P094', 0) - .4, 99, { x: 1800, align: 'right' }) } });

  // P096 · ayrıntı · F12 · Kıyıdaki nergis suya eğik: bilmek yetmedi
  plan('P096', (ctx, st) => {
    const t = st.t, tY = PE('P096', 0);
    s2_nergisYakin(ctx, t, st, { cam: s2_cam(st, [1000, 520, 1.8], [1000, 640, 1.8]), lean: .45 + .35 * ramp(t, tY - .1, tY + 1.2, E.io2), refA: .6 });
  });
})();
