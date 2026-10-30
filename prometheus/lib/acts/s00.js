// ZİNCİRDEKİ TİTAN (açılış, A01–A05): ateşin çalınışı (kapak karesi), zincir, kylixteki kartal, başlık, Erhat'ın iddiası
'use strict';

// --- Olympos'tan inen koşu: kırmızı figür Prometheus, havaya kaldırılmış rezene sapı; ateş karenin en parlak noktası ---
const RUN = { sp: 270, s: 5.2, x0: 600 };
const runGround = x => 610 + x * .2 + fbm1(x * .004, 2) * 22;
function olymposRun(ctx, t, c, o = {}) {
  glazeBG(ctx, t, { gx: c.x + 300, gy: 300, gr: 1000, stars: false, warm: 'rgba(110,44,20,.35)' });
  ctx.save(); cam(ctx, c, .08); vaseStars(ctx, t, 55, 3, [-600, 40, 3600, 560], [], .42); ctx.restore();
  // uzakta Olympos: koyu kütle, kil kontur; en yüksek tepede tanrıların ocağının sönük parıltısı
  ctx.save(); cam(ctx, c, .25);
  const pk = x => 560 - 380 * Math.exp(-(((x - 220) / 260) ** 2)) - 170 * Math.exp(-(((x - 700) / 190) ** 2)) + fbm1(x * .01, 5) * 12;
  ctx.beginPath(); ctx.moveTo(-900, pk(-900)); for (let x = -900; x <= 3200; x += 16) ctx.lineTo(x, pk(x)); ctx.lineTo(3200, 1600); ctx.lineTo(-900, 1600); ctx.closePath();
  ctx.fillStyle = '#1A100B'; ctx.fill(); ctx.strokeStyle = 'rgba(201,112,63,.55)'; ctx.lineWidth = 3; ctx.stroke();
  glow(ctx, 220, 190, 190, 'rgba(255,200,120,.16)');
  temple(ctx, 220, pk(220) + 8, .32, 5, '#140B07', 'rgba(201,112,63,.6)');
  ctx.restore();
  // yamaç
  ctx.save(); cam(ctx, c, 1);
  ctx.beginPath(); ctx.moveTo(-600, runGround(-600)); for (let x = -600; x <= 4200; x += 16) ctx.lineTo(x, runGround(x)); ctx.lineTo(4200, 2200); ctx.lineTo(-600, 2200); ctx.closePath();
  ctx.fillStyle = '#2A170F'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3.5; ctx.stroke();
  ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 2; ctx.beginPath(); for (let x = -600; x <= 4200; x += 16) { const y = runGround(x) + 14; x > -600 ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
  // koşan Titan
  const x = RUN.x0 + RUN.sp * t;
  let wr = null, M = null, Jn = null;
  walkScene(ctx, c, x, RUN.s, t, 1, {
    noCam: true, ground: groundOf(runGround), stride: 52, lean: .26, sty: STY.red, lk: LK.prom, seed: 17,
    p: { shN: 2.45 + Math.sin(t * 9.6) * .05, elN: .25, handN: 'fist', mouthOpen: 0, smile: -1, headBack: o.back, wind: .9, scowl: .5 },
    onJoints: (J, m) => { Jn = J; M = m; },
  });
  wr = jointPt(ctx, M, Jn.AN.wr);
  // rezene sapı yumruktan yukarı-ileri; ucunda ateş (karenin tek parlak noktası)
  const a = -1.15 + Math.sin(t * 9.6) * .04, L = 190, tip = [wr[0] + Math.cos(a) * L, wr[1] + Math.sin(a) * L];
  // kıvılcım izi: önceki uç konumları geride kalır
  for (let i = 0; i < 26; i++) {
    const age = ((t * 1.7 + i / 26) % 1), bx = tip[0] - RUN.sp * age * .9 + noise1(i * 3.1 + t, 4) * 14, by = tip[1] - age * 70 + noise1(i * 1.7 + t, 8) * 10;
    ctx.globalAlpha = (1 - age) * .8; ctx.fillStyle = age < .3 ? PC.fire : PC.fireDeep; ctx.beginPath(); ctx.arc(bx, by, 3.2 * (1 - age) + .6, 0, TAU); ctx.fill();
  }
  ctx.globalAlpha = 1;
  fennel(ctx, wr[0] - Math.cos(a) * 30, wr[1] - Math.sin(a) * 30, tip[0], tip[1], t, { w: 10, fs: 1.35, haloR: 170 });
  ctx.restore();
  return { x, tip };
}
// P001: kapak karesi (koşu, ateş en parlak nokta), P003: yakın plan, baş geriye (Olympos'a) döner
shot(0, (ctx, st) => {
  const x = RUN.x0 + RUN.sp * st.t;
  olymposRun(ctx, st.t, { x: x + 120, y: 470 + x * .2 - 140, z: 1.0 + st.t * .01 });
}, { tr: { type: 'black', dur: .6 }, post: { tex: .55, vig: 1, grain: .06 } });
// P002: aşağıda karanlık ova; ateş ocaktan ocağa geçer, mağara ağızlarında insanların yüzleri aydınlanır
shot(A('A01@insanlara'), (ctx, st) => {
  const lt = st.lt;
  glazeBG(ctx, st.t, { gx: 960, gy: 900, gr: 1100, stars: false });
  const c = { x: 960, y: lerp(470, 560, E.io2(clamp(lt / 1.6))), z: 1.05 };
  ctx.save(); cam(ctx, c, .1); vaseStars(ctx, st.t, 40, 7, [0, 40, W, 420], [], .35); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  // mağaralı yamaç bandı
  const hy = x => 640 + fbm1(x * .004, 6) * 40;
  ctx.beginPath(); ctx.moveTo(-200, hy(-200)); for (let x = -200; x <= 2200; x += 16) ctx.lineTo(x, hy(x)); ctx.lineTo(2200, 1400); ctx.lineTo(-200, 1400); ctx.closePath();
  ctx.fillStyle = '#2A170F'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3.5; ctx.stroke();
  const caves = [[260, 760], [620, 800], [980, 770], [1340, 810], [1700, 780]];
  caves.forEach(([cx, cy], i) => {
    const ti = .15 + i * .2, k = E.outBack(ramp(lt, ti, ti + .35, E.lin));
    ctx.fillStyle = '#0E0907'; ctx.beginPath(); ctx.ellipse(cx, cy, 120, 86, 0, PI, TAU); ctx.lineTo(cx + 120, cy + 40); ctx.lineTo(cx - 120, cy + 40); ctx.fill();
    ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.ellipse(cx, cy, 120, 86, 0, PI, TAU); ctx.stroke();
    if (k > 0) {
      glow(ctx, cx, cy, 170 * k, `rgba(255,160,70,${.35 * k})`);
      humanFires(ctx, st.t, [[cx, cy + 34, 1.1 * k]], 1);
      seatedHuman(ctx, cx - 52, cy + 36, 1.3, 1, st.t); seatedHuman(ctx, cx + 52, cy + 36, 1.3, -1, st.t);
    }
  });
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });
shot(A('A01@titan'), (ctx, st) => {
  const t = st.t, x = RUN.x0 + RUN.sp * t, lt = st.lt;
  // yakın plan: baş ve rezene; baş geriye döner (bile bile)
  olymposRun(ctx, t, { x: x + 40, y: 470 + x * .2 - 330 + lt * 6, z: lerp(2.15, 2.3, E.io2(clamp(lt / 1.8))) }, { back: lt > .25 });
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P004: zincir kayaya çakılır (çekiç ve kazık yakın), P005: kamera zinciri buluta kadar izler ---
function hammerHit(ctx, x, y, tHit, t, s = 1) {
  // çekiç: siyah sır başlık, kil sap; vuruşta durur, sonra geri sıçrar
  const u = t - tHit, a = u < 0 ? lerp(-.2, -1.5, clamp(-u / .45)) : -.2 - settle(t, tHit, .5, 3.5, 7);
  ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s);
  ctx.fillStyle = PC.clayR; ctx.strokeStyle = C.ink; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.rect(6, -10, 230, 20); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#2B1A12'; ctx.beginPath(); ctx.rect(-40, -46, 64, 92); ctx.fill(); ctx.stroke();
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(-34, -38); ctx.lineTo(-34, 38); ctx.stroke();
  ctx.restore();
}
shot(A('A02'), (ctx, st) => {
  const t = st.t, lt = st.lt, tH = A('A02@mıhlatan');
  const sk = shake(t, tH, 14, 7);
  const c = { x: lerp(1430, 1330, E.io2(clamp(lt / st.d))), y: lerp(300, 380, E.io2(clamp(lt / st.d))), z: lerp(2.1, 1.7, E.io2(clamp(lt / st.d))), sx: sk[0], sy: sk[1] };
  const { wind } = kayaWorld(ctx, t, c, { skyChain: true });
  ctx.save(); cam(ctx, c, 1);
  promChained(ctx, t, { wind, look: -.05, pullK: .4 });
  const sF = PROM_KAYA.sF;
  hammerHit(ctx, sF[0] + 70, sF[1] - 150, tH, t, 1.2);
  if (t > tH) { dustBurst(ctx, t, tH, sF[0], sF[1], 26, 'rgba(201,112,63,.6)', 120, 4); if (t - tH < .5) sparkle(ctx, sF[0] - 6, sF[1], 26 * (1 - (t - tH) / .5), 1); }
  ctx.restore();
  // çakma: kısa beyaz parlama
  if (t > tH && t < tH + .18) { ctx.save(); baseT(ctx); ctx.fillStyle = '#FFF4DE'; ctx.globalAlpha = .55 * (1 - (t - tH) / .18); ctx.fillRect(0, 0, W, H); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'white', dur: .3 }, post: { tex: .55, vig: 1, grain: .06 } });
shot(A('A02@zeusun'), (ctx, st) => {
  const t = st.t, lt = st.lt, tT = A('A02@asıl');
  // kamera kazıktan yukarı, bulutlara doğru çevrinir; "asıl tutsak"ta zincir yukarıdan bir kez gerilir
  const u = E.io3(clamp(lt / (st.d * .85)));
  const tug = t > tT ? Math.exp(-(t - tT) * 5) * Math.sin((t - tT) * 22) : 0;
  const c = { x: lerp(1420, 1560, u), y: lerp(330, -420, u), z: lerp(1.6, 1.25, u), sy: tug * 6 };
  const { wind } = kayaWorld(ctx, t, c, { skyChain: true, chainTug: tug, glint: t > tT ? Math.exp(-(t - tT) * 2.2) : 0 });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, pullK: .5 }); ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P006–P010: Lakonya kylixi (siyah figür, Hesiodos): sütuna bağlı Prometheus, güneşten inen kartal, gece, şafak ---
function kylixScene(ctx, t, lt, o) {
  ctx.fillStyle = '#120B08'; ctx.fillRect(-50, -50, W + 100, H + 100);
  const R = 430, cx = W / 2, cy = H / 2 + 10;
  kylix(ctx, t, cx, cy, R, -.18 + lt * .035, (c, t, r) => {
    const night = o.night || 0, dawn = o.dawn ?? 1;
    // zemin çizgisi ve sütun
    c.fillStyle = C.ink; c.fillRect(-r, r * .58, 2 * r, 7);
    column(c, 175, r * .58, -r * .52, 34, C.ink, C.clay);
    // güneş diski (sol üst), şafakla doğar
    const sy = lerp(-r * .1, -r * .52, dawn);
    c.save(); c.globalAlpha = 1 - night * .85; c.fillStyle = '#D9A066'; c.beginPath(); c.arc(-210, sy, 78, 0, TAU); c.fill(); c.strokeStyle = C.ink; c.lineWidth = 5; c.stroke(); c.restore();
    // sütuna bağlı Prometheus (siyah figür): kollar arkada, sütunda
    const s = 4.1, px = 110, gy = r * .58;
    figure(c, { x: px, y: gy - 44.2 * s, s, dir: -1, sty: STY.black, lk: LK.prom, seed: 23,
      p: { torso: o.torso ?? -.05, neck: o.neck ?? -.1, head: o.head ?? -.1, handN: 'fist', handF: 'fist', mouthOpen: o.mouth || 0, blink: o.blink },
      ik: { hN: [px + 62, gy - 20 * s], hF: [px + 60, gy - 23 * s], fN: [px - 30, gy - 3 * s, 0], fF: [px + 28, gy - 3 * s, 0] } });
    // bağ (iki halka sütunda)
    c.strokeStyle = C.clay; c.lineWidth = 3; for (const yy of [gy - 21 * s, gy - 9 * s]) { c.beginPath(); c.ellipse(175, yy, 22, 6, 0, 0, TAU); c.stroke(); }
    // gece: tondo kararır, yıldızlar; böğürde altın ışık atar
    if (night > 0) {
      c.fillStyle = `rgba(14,8,5,${.62 * night})`; c.fillRect(-r, -r, 2 * r, 2 * r);
      c.save(); c.globalAlpha = night; vaseStars(c, t, 40, 9, [-r, -r, 2 * r, r * 1.4], [], .5); c.restore();
      const pul = .5 + .5 * Math.sin(t * 3.2);
      glow(c, px + 10, gy - 30 * s, 60, `rgba(255,190,90,${.55 * night * pul})`);
    }
    // kartal (siyah figür, kil kazıma)
    if (o.eagle) {
      const e = o.eagle;
      eagle2(c, e.x, e.y, e.s, e.dir || 1, { ang: e.ang ?? .9, angFar: e.angFar ?? .2, farOff: -.5, fsMin: .55, talon: e.talon ?? .6, beak: e.beak ?? .1, tilt: e.tilt ?? .3, headA: e.headA || 0,
        col: C.ink, line: C.clay, wingCol: C.ink, farCol: '#2A1C14', eye: C.clay, headS: 1.35, lw: 1.2 });
    }
    // yazıt: ΠΡΟΜΗΘΕΥΣ (eklenmiş kırmızı, Lakonya kylixlerinde ad yazıtı)
    dipinto(c, 'ΠΡΟΜΗΘΕΥΣ', -30, -r * .62, 26, { col: C.red, w: .11 });
  }, { tilt: .97 });
}
const KY = { sun: [-210, -200], chest: [70, -40] };
function eagleAt(t, t0, t1, from, to, s0, s1) {
  const u = E.io2(clamp((t - t0) / (t1 - t0)));
  return { x: lerp(from[0], to[0], u), y: lerp(from[1], to[1], u) - Math.sin(u * PI) * 40, s: lerp(s0, s1, u), u };
}
shot(A('A03'), (ctx, st) => {
  const t = st.t, lt = st.lt, tK = A('A03@kartal'), tL = A('A03@karaciğerini'), tN = A('A03@gece'), tS = A('A03@sabah');
  let eagle = null, o = {};
  const fl = (t * .9) % 1, gl = .5 + .5 * Math.cos(fl * TAU);
  if (t < tN) {
    if (t >= tK - .4) {
      const p = eagleAt(t, tK - .4, tL, [KY.sun[0], KY.sun[1]], KY.chest, .55, 1.25);
      const landed = t >= tL - .2;
      eagle = { x: p.x, y: p.y, s: p.s, ang: landed ? .95 - .05 * Math.sin(t * 6) : lerp(.65, .97, Math.pow(gl, .5)), angFar: landed ? .05 : .2, talon: landed ? 1 : .5, beak: landed ? .3 + .3 * Math.max(0, Math.sin(t * 7)) : .1, tilt: landed ? .55 : .25, headA: landed ? .25 + .1 * Math.sin(t * 7) : 0 };
      if (landed) o = { head: -.55, neck: -.25, mouth: .4 };
    }
    o.dawn = 1;
  } else if (t < tS) {
    o = { night: ramp(t, tN, tN + .6), dawn: 1 - ramp(t, tN, tN + .8), head: -.15, blink: .8 };
  } else {
    // şafak hızla gelir; kartal güneş diskinden yeniden çıkar
    const k = ramp(t, tS, tS + .7);
    o = { night: 1 - k, dawn: k, head: -.2 };
    if (t > tS + .3) { const p = eagleAt(t, tS + .3, tS + 2.6, KY.sun, [-60, -110], .35, .8); eagle = { x: p.x, y: p.y, s: p.s, ang: lerp(.65, .97, Math.pow(gl, .5)), talon: .6, tilt: .3 }; }
  }
  o.eagle = eagle;
  // kupa yavaşça döner; sonda kamera kartalın gözüne dalar (siyah göz bebeği başlığın siyah sırrı olur)
  const end = st.end, dz = ramp(t, end - 1.0, end, E.in3);
  ctx.save();
  if (dz > 0 && eagle) {
    const R = 430, cx = W / 2, cy = H / 2 + 10, rot = -.18 + lt * .035;
    const hS = 1.35, ex = eagle.x + (36 + (hS - 1.22) * 18 + 12.4 * hS) * eagle.s, ey = eagle.y + (-14 - (hS - 1.22) * 4 - 4.2 * hS) * eagle.s;
    const q = rot2([ex, ey * .97], rot), zx = cx + q[0], zy = cy + q[1];
    const z = lerp(1, 60, dz);
    ctx.translate(zx, zy); ctx.scale(z, z); ctx.translate(-zx, -zy);
  }
  kylixScene(ctx, t, lt, o);
  ctx.restore();
}, { tr: { type: 'negatif', dur: .8 }, post: { tex: .85, vig: .85, grain: .055 } });
function rot2(p, a) { const c = Math.cos(a), s = Math.sin(a); return [p[0] * c - p[1] * s, p[0] * s + p[1] * c]; }

// --- P011: başlık. Sır siyahı üstünde ΠΡΟΜΗΘΕΥΣ yazılır, harfler ateş alıp PROMETHEUS'a dönüşür ---
shot(A('A04') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tP = A('A04@prometeus');
  glazeBG(ctx, t, { gx: 960, gy: 760, gr: 900, stars: false, warm: 'rgba(120,48,22,.4)' });
  vaseStars(ctx, t, 40, 13, [0, 60, W, 500], [], .35);
  // arkada zincirli siluetin gölgesi
  ctx.save(); ctx.globalAlpha = .16 + .04 * Math.sin(t * 1.7); ctx.translate(960, 560); ctx.scale(.62, .62); ctx.translate(-1225, -560);
  figure(ctx, { x: 1225, y: 868 - 42.5 * 6.3, s: 6.3, dir: -1, sty: { ...STY.red, fill: '#5A2C18', dilute: '#5A2C18' }, lk: LK.prom, still: true, p: { torso: .12, head: -.1 },
    ik: { hF: [1425, 243], hN: [1410, 568], fN: [1155, 849, 0], fF: [1315, 849, .25] } });
  ctx.restore();
  const gk = 1 - ramp(t, tP - .1, tP + .6), lat = ramp(t, tP + .1, tP + .9);
  const z = 1 + lt * .012;
  ctx.save(); ctx.translate(960, 480); ctx.scale(z, z); ctx.translate(-960, -480);
  if (gk > 0) dipinto(ctx, 'ΠΡΟΜΗΘΕΥΣ', 960, 480, 120, { col: PC.clayR, a: gk, p: ramp(lt, .1, Math.max(.6, tP - st.at)), w: .09, ls: .3 });
  if (lat > 0) {
    glow(ctx, 960, 470, 700 * lat, `rgba(255,170,80,${.22 * lat})`);
    txt(ctx, 'PROMETHEUS', 960, 480, { font: '700 138px Cinzel', col: mixCol(PC.fireDeep, PC.fire, lat), ls: 16, a: lat, shadow: 'rgba(255,170,80,.8)', blur: 30 * lat, force: true });
    // harflerden yükselen kıvılcımlar
    motes(ctx, t, 40, 17, 'rgba(255,200,120,.9)', [480, 360, 960, 160], 40, 1.6, .7 * lat);
  }
  ctx.restore();
  friezeFrame(ctx, { col: mixCol(PC.clayR, PC.glaze, .3), h: 38, saltire: true, bandBg: PC.glaze, alpha: .9 });
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P012–P013: beyaz zemin, Erhat. Alev mürekkebe döner, bir kitap açılır: ÖNSÖZ, 1967 ---
function scribble(ctx, x, y, w, p, seed, o = {}) {
  // okunmayan el yazısı satırı (önsöz metni kopyalanmaz): ince sepya dalga, sözcük boşluklu
  const r = rng(seed), pts = [];
  let xx = x;
  while (xx < x + w) { const wl = 30 + r() * 70; for (let k = 0; k <= wl; k += 4) pts.push([xx + k, y + Math.sin((xx + k) * .45 + seed) * 4 + Math.sin((xx + k) * .13) * 2]); xx += wl + 14 + r() * 10; pts.push(null); }
  const n = Math.floor(pts.length * clamp(p));
  ctx.save(); ctx.strokeStyle = o.col || 'rgba(74,52,35,.7)'; ctx.lineWidth = o.w || 2.2; ctx.lineCap = 'round'; ctx.beginPath();
  let pen = false;
  for (let i = 0; i < n; i++) { const q = pts[i]; if (!q) { pen = false; continue; } pen ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); pen = true; }
  ctx.stroke(); ctx.restore();
}
shot(A('A06'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('A06@bin');
  const c = { x: W / 2 + lt * 4, y: H / 2, z: 1.02 + lt * .003 };
  ctx.save(); cam(ctx, c, 1);
  paperBG(ctx, t, { book: true, num: 'v' });
  penLine(ctx, 'ÖNSÖZ', W / 2, 190, ramp(lt, .2, .9), { font: '600 64px Cinzel', ls: 14, col: PW.line });
  for (let i = 0; i < 5; i++) scribble(ctx, 420, 290 + i * 56, 1080, ramp(lt, .7 + i * .35, 1.6 + i * .35), 40 + i);
  // 1967 ve künye
  const k = ramp(t, tB - .2, tB + .5);
  if (k > 0) {
    penLine(ctx, '1967', W / 2, 640, ramp(t, tB - .1, tB + .8), { font: 'italic 600 120px "Cormorant Garamond"', col: PW.red, nib: true });
    txt(ctx, 'Aiskhylos · Zincire Vurulmuş Prometheus', W / 2, 740, { font: 'italic 500 38px "Cormorant Garamond"', col: PW.ink, a: ramp(t, tB + .5, tB + 1.1) });
    txt(ctx, 'çeviren Sabahattin Eyüboğlu · Azra Erhat', W / 2, 790, { font: 'italic 500 34px "Cormorant Garamond"', col: PW.line, a: ramp(t, tB + .9, tB + 1.5) });
  }
  ctx.restore();
  nameTag(ctx, 'AZRA ERHAT', '1915–1982 · çevirmen, yazar', 120, 150, lt - .4, Math.max(3.2, tB - st.at), { col: PW.ink, line: PW.red });
}, { tr: { type: 'ink', dur: 1.0 }, post: { tex: .35, vig: .55, grain: .045 } });

// --- P014: sayfada iki uçlu zincir: bir ucu küçük zincirli figürde, öbürü bir tahtın içine; zincir soru işaretine kıvrılır ---
shot(A('A05'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  ctx.save(); cam(ctx, { x: W / 2, y: H / 2 - 20, z: 1 + lt * .01 }, 1);
  paperBG(ctx, t, { book: true, num: 'xiv' });
  marginBand(ctx, 260, 1660, 300, 760, ramp(lt, 0, .8));
  figure(ctx, { x: 520, y: 740 - 44.5 * 3.2, s: 3.2, dir: 1, sty: STY.lek, lk: LK.prom, p: { torso: .1, head: .05 }, ik: { hF: [600, 520], hN: [610, 640] } });
  throne(ctx, 1380, 740, 7, -1, PW.line, PW.paperL, { high: true });
  // zincir: figürden yukarı kavis çizip soru işareti gibi kıvrılır, tahta girer
  const pts = sampleF(u => { const a = lerp(PI * 1.05, -PI * .45, u); return u < .55 ? [lerp(610, 1000, u / .55), 600 - Math.sin(u / .55 * PI) * 210] : [1000 + Math.cos(a) * 140 * (1 - (u - .55)) + 160 * (u - .55) / .45 * 1.6, 470 + Math.sin(a) * 150]; }, 90);
  inkPoly(ctx, pts, ramp(lt, .3, 2.0), { col: PW.line, w: 5, jit: .6 });
  // halkalar çizgi boyunca
  const n = Math.floor(28 * ramp(lt, .3, 2.0));
  for (let i = 0; i < n; i++) { const q = pts[Math.floor(i / 28 * 89)]; ctx.strokeStyle = PW.line; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.ellipse(q[0], q[1], 9, 5, i % 2 ? .8 : -.8, 0, TAU); ctx.stroke(); }
  if (lt > 2.0) circleMark(ctx, 1385, 560, 120, 150, ramp(lt, 2.0, 2.8));
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .35, vig: .55, grain: .045 } });

// --- P015: avuçtaki alev (bir avuç ateş): profilden kavuşturulmuş eller, kıvılcım yükselir ---
function cuppedHands(ctx, x, y, s, t) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = PC.clayR; ctx.strokeStyle = C.ink; ctx.lineWidth = 3 / s; ctx.lineJoin = 'round';
  // iki avuç: alttaki çanak ve öndeki başparmaklar
  ctx.beginPath(); ctx.moveTo(-120, -10); ctx.quadraticCurveTo(-110, 60, -20, 70); ctx.quadraticCurveTo(70, 72, 118, 6); ctx.lineTo(104, -6); ctx.quadraticCurveTo(60, 40, -4, 42); ctx.quadraticCurveTo(-80, 40, -98, -16); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(-98, -16); ctx.quadraticCurveTo(-84, -40, -60, -30); ctx.quadraticCurveTo(-70, -10, -74, 6); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(104, -6); ctx.quadraticCurveTo(96, -34, 72, -28); ctx.quadraticCurveTo(80, -8, 82, 8); ctx.stroke();
  // bilekler
  ctx.beginPath(); ctx.moveTo(-120, -10); ctx.lineTo(-260, 60); ctx.lineTo(-250, 120); ctx.lineTo(-110, 60); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(118, 6); ctx.lineTo(260, 70); ctx.lineTo(250, 128); ctx.lineTo(96, 62); ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.restore();
}
shot(A('A05@ve'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  glazeBG(ctx, t, { gx: 960, gy: 560, gr: 700, stars: false, warm: 'rgba(150,62,28,.5)' });
  const z = 1 + lt * .03;
  ctx.save(); ctx.translate(960, 600); ctx.scale(z, z); ctx.translate(-960, -600);
  glow(ctx, 960, 540, 520, 'rgba(255,150,70,.18)');
  cuppedHands(ctx, 960, 640, 1.5, t);
  flame(ctx, 960, 650, 1.6, t, { haloR: 160 });
  motes(ctx, t, 30, 29, 'rgba(255,200,120,.9)', [860, 300, 200, 300], 50, 1.6, .7);
  ctx.restore();
}, { tr: { type: 'ink', dur: .7 }, post: { tex: .55, vig: 1, grain: .06 } });
