// ZİNCİRDEKİ TİTAN (açılış, A01–A05): ateşin çalınışı (kapak karesi), zincir, kylixteki kartal, başlık, Erhat'ın iddiası
'use strict';

// --- Olympos'tan inen koşu: kırmızı figür Prometheus, havaya kaldırılmış rezene sapı; ateş karenin en parlak noktası ---
const RUN = { sp: 250, s: 6.4, x0: 600 };
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
  ctx.beginPath(); ctx.moveTo(-600, runGround(-600)); for (let x = -600; x <= 4200; x += 16) ctx.lineTo(x, runGround(x));
  for (let x = 4200; x >= -600; x -= 24) ctx.lineTo(x, runGround(x) + 230 + fbm1(x * .01, 3) * 60); ctx.closePath();
  ctx.fillStyle = '#2A170F'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3.5; ctx.stroke();
  ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 2; ctx.beginPath(); for (let x = -600; x <= 4200; x += 16) { const y = runGround(x) + 14; x > -600 ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
  if (o.terrace !== undefined) caveTerrace(ctx, t, o.terrace);
  // koşan Titan
  const x = RUN.x0 + RUN.sp * t;
  let wr = null, M = null, Jn = null;
  walkScene(ctx, c, x, RUN.s, t, 1, {
    noCam: true, ground: groundOf(runGround), stride: 52, lean: .26, sty: STY.red, lk: LK.promFree, seed: 17, stripe: .55,
    p: { shN: 2.2 + Math.sin(t * 9.6) * .05, elN: .2, handN: 'fist', mouthOpen: 0, smile: -1, headBack: o.back, wind: .9, scowl: .5 },
    onJoints: (J, m) => { Jn = J; M = m; },
  });
  wr = jointPt(ctx, M, Jn.AN.wr);
  // rezene sapı yumruktan yukarı-ileri; ucunda ateş (karenin tek parlak noktası)
  const a = -.72 + Math.sin(t * 9.6) * .04, L = 175, tip = [wr[0] + Math.cos(a) * L, wr[1] + Math.sin(a) * L];
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
// P001–P003: tek sürekli plan. Kapak karesiyle açılır (kararma yok); "bile bile"de baş omzun üstünden Olympos'a döner;
// "insanlara"da kamera aşağıdaki ovaya iner, ocaklar sırayla yanar; "Titan düşün"de yakın plana, kaldırılmış ateşe döner.
const TERRACE = 1450;
function caveTerrace(ctx, t, ignite) {
  const hy = x => TERRACE + fbm1(x * .004, 6) * 40;
  ctx.beginPath(); ctx.moveTo(-600, hy(-600)); for (let x = -600; x <= 4200; x += 16) ctx.lineTo(x, hy(x)); ctx.lineTo(4200, 2600); ctx.lineTo(-600, 2600); ctx.closePath();
  ctx.fillStyle = '#2A170F'; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3.5; ctx.stroke();
  const caves = [[1120, 1560], [1480, 1600], [1840, 1570], [2200, 1610], [2560, 1580]];
  caves.forEach(([cx, cy], i) => {
    const k = E.outBack(clamp(ignite - i * .18) / 1, E.lin), kk = clamp(k * 1.6);
    ctx.fillStyle = '#0E0907'; ctx.beginPath(); ctx.ellipse(cx, cy, 120, 86, 0, PI, TAU); ctx.lineTo(cx + 120, cy + 40); ctx.lineTo(cx - 120, cy + 40); ctx.fill();
    ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.ellipse(cx, cy, 120, 86, 0, PI, TAU); ctx.stroke();
    seatedHuman(ctx, cx - 50, cy + 36, 1.25, 1, t); seatedHuman(ctx, cx + 50, cy + 36, 1.25, -1, t);
    if (kk > 0) { glow(ctx, cx, cy, 170 * kk, `rgba(255,160,70,${.35 * kk})`); humanFires(ctx, t, [[cx, cy + 34, 1.1 * clamp(kk)]], 1); }
  });
}
shot(0, (ctx, st) => {
  const t = st.t, x = RUN.x0 + RUN.sp * t, gy = runGround(x);
  const tB = A('A01@bile'), tI = A('A01@insanlara'), tT = A('A01@titan');
  const c1 = { x: x + 200, y: gy - 360, z: .98 + t * .012 }, c2 = { x: x + 560, y: TERRACE - 90, z: .95 }, c3 = { x: x + 110, y: gy - 560, z: 1.8 };
  const tE = Se('A01'), d = E.io3(ramp(t, tI - .35, tI + .45, E.lin)), u = E.io3(ramp(t, tT - .1, tT + .55, E.lin));
  const c = mix(mix(c1, c2, d), c3, u);
  olymposRun(ctx, t, c, { back: t > tB + .1 && t < tI - .1 || t > tT + .2, terrace: ramp(t, tI + .05, tI + .95, E.lin) * 1.8 });
  kayaFrame(ctx, t);
}, { post: { tex: .55, vig: 1, grain: .06 } });
// --- P004: zincir kayaya çakılır (çekiç ve kazık yakın), P005: kamera zinciri buluta kadar izler ---
function hammerHit(ctx, tx, ty, tHit, t, s = 1) {
  // çekiç: sap sağ üstteki pivot (görünmeyen el) çevresinde döner; vuruş anında baş kazığın başına oturur, sonra geri sıçrar
  const P = [tx + 200 * s, ty - 210 * s], L = Math.hypot(200, 210) * s, ah = Math.atan2(ty - P[1], tx - P[0]);
  const u = t - tHit, a = u < 0 ? ah - 1.25 * E.io2(clamp(-u / .5)) : ah - .35 * Math.abs(settle(t, tHit, 1, 3.2, 6));
  ctx.save(); ctx.translate(P[0], P[1]); ctx.rotate(a);
  ctx.fillStyle = PC.clayR; ctx.strokeStyle = C.ink; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.rect(-30 * s, -9 * s, L, 18 * s); ctx.fill(); ctx.stroke();
  ctx.fillStyle = '#2B1A12'; ctx.beginPath(); ctx.rect(L - 30 * s, -44 * s, 60 * s, 88 * s); ctx.fill(); ctx.stroke();
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(L - 24 * s, -36 * s); ctx.lineTo(L - 24 * s, 36 * s); ctx.stroke();
  ctx.restore();
}
shot(PA('P004'), (ctx, st) => {
  const t = st.t, lt = st.lt, tH = st.at + .12, tH2 = A('A02@mıhlatan'), hit = t < (tH + tH2) / 2 ? tH : tH2;
  const sk = shake(t, tH, 14, 7), sk2 = shake(t, tH2, 10, 7), back = E.out3(ramp(t, tH2, tH2 + .5));
  const c = { x: lerp(1430, 1330, E.io2(clamp(lt / st.d))), y: lerp(300, 380, E.io2(clamp(lt / st.d))), z: lerp(2.1, 1.7, E.io2(clamp(lt / st.d))) * lerp(1, .88, back), sx: sk[0] + sk2[0], sy: sk[1] + sk2[1] };
  const { wind } = kayaWorld(ctx, t, c, { skyChain: true });
  ctx.save(); cam(ctx, c, 1);
  promChained(ctx, t, { wind, look: -.05, pullK: .4 });
  const sF = PROM_KAYA.sF;
  hammerHit(ctx, sF[0] - 22, sF[1], hit, t, 1.1);
  for (const h of [tH, tH2]) if (t > h && t < h + 4) { dustBurst(ctx, t, h, sF[0], sF[1], 26, 'rgba(201,112,63,.6)', 120, 4); if (t - h < .5) sparkle(ctx, sF[0] - 6, sF[1], 26 * (1 - (t - h) / .5), 1); }
  ctx.restore();
  // çakma: kısa beyaz parlama
  for (const [h, d] of [[tH, .15], [tH2, .1]]) if (t > h && t < h + d) { ctx.save(); baseT(ctx); ctx.fillStyle = '#FFF4DE'; ctx.globalAlpha = .55 * (1 - (t - h) / d); ctx.fillRect(0, 0, W, H); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });
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
// kırmızı figür vinyet: sayfaya yapıştırılmış küçük levha; zincirli Prometheus zincire asılmayı sürdürür
function promVignette(ctx, t, x, y, w, h, o = {}) {
  ctx.save(); ctx.translate(x, y);
  ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, w, h); ctx.strokeStyle = PW.line; ctx.lineWidth = 5; ctx.strokeRect(0, 0, w, h);
  ctx.beginPath(); ctx.rect(0, 0, w, h); ctx.clip();
  const k = Math.min(w / 1100, h / 980);
  ctx.translate(w / 2, h / 2); ctx.scale(k, k); ctx.translate(-1290, -560);
  promChained(ctx, t, { wind: .4, pull: .2 + .15 * Math.max(0, Math.sin(t * 1.4)) });
  ctx.restore();
}
// P012–P013: kitap kapağı (zincirli Prometheus vinyetiyle), 1967 damgası, kapak açılır: ÖNSÖZ sayfası
shot(A('A06'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('A06@bin'), tO = A('A06@oyunun');
  ctx.save(); cam(ctx, { x: W / 2 + lt * 4, y: H / 2, z: 1.02 + lt * .003 }, 1);
  paperBG(ctx, t, { book: true });
  const open = ramp(t, tO - .2, tO + .7);
  if (open < 1) {
    // kapak: kil renkli cilt, başlık, ortada küçük kırmızı figür levha; açılırken sola katlanır
    ctx.save(); ctx.translate(560, 0); ctx.scale(1 - open, 1); ctx.translate(-560, 0);
    ctx.fillStyle = '#B8693F'; ctx.fillRect(560, 120, 800, 560); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.strokeRect(560, 120, 800, 560);
    meanderSaltire(ctx, 580, 1340, 140, 26, C.ink, '#B8693F');
    txt(ctx, 'AISKHYLOS', 960, 214, { font: '700 40px Cinzel', col: C.ink, ls: 10 });
    txt(ctx, 'ZİNCİRE VURULMUŞ PROMETHEUS', 960, 268, { font: '700 36px Cinzel', col: C.ink, ls: 2, maxW: 740 });
    promVignette(ctx, t, 780, 310, 360, 300);
    const k = ramp(t, tB - .15, tB + .05, E.in2);
    if (k > 0) stamp(ctx, '1967', 1240, 590, t - tB, { col: PW.red, font: '700 84px Cinzel', h: 112, rot: -.12, a: .92 }); // 'Azra Erhat'ın sağında, ada binmez
    const tT = A('A06@tuhaf'), tAz = A('A06@azra'), wf = 'italic 600 54px "Cormorant Garamond"';
    ctx.save(); ctx.font = wf; const ww = ctx.measureText(L('Azra Erhat')).width; ctx.restore();
    const wp = ramp(t, tAz, A('A06@erhat') + .5, E.lin), wx0 = 960 - ww / 2, fall = ramp(t, tT - .4, tT + .4, E.in2);
    penLine(ctx, 'Azra Erhat', 960, 648, wp, { font: wf, col: PW.ink });
    if (fall > 0) { const nx = fall < 1 ? lerp(1150, wx0, fall) : wx0 + ww * wp, ny = fall < 1 ? lerp(-60, 658, fall) : 658 + Math.sin(wp * 40) * 5;
      if (fall >= 1) M_pen(ctx, nx, ny, -.55, 1.1);
      glow(ctx, nx, ny, 40, 'rgba(255,190,100,.6)'); sparkle(ctx, nx, ny, fall < 1 ? 22 : 12, 1, '#FFE2A8'); }
    ctx.restore();
  }
  if (open > 0) {
    ctx.save(); ctx.globalAlpha = open;
    penLine(ctx, 'ÖNSÖZ', W / 2, 190, ramp(t, tO + .3, tO + .9), { font: '600 64px Cinzel', ls: 14, col: PW.line });
    for (let i = 0; i < 5; i++) scribble(ctx, 600, 290 + i * 56, 900, ramp(t, tO + .6 + i * .3, tO + 1.4 + i * .3), 40 + i);
    promVignette(ctx, t, 90, 300, 300, 250);
    ctx.restore();
  }
  ctx.restore();
}, { tr: { type: 'ink', dur: .5 }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => erhatTag(ctx, st.lt, 'AZRA ERHAT · 1967') });
// P014: kenardaki vinyetin zinciri sayfaya taşar, soru işaretine kıvrılır ve sayfanın üst kenarından çıkar (öbür ucu görünmez)
shot(A('A05'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  ctx.save(); cam(ctx, { x: W / 2 + lt * 3, y: H / 2 - 10, z: 1 + lt * .008 }, 1);
  paperBG(ctx, t, { book: true });
  for (let i = 0; i < 5; i++) scribble(ctx, 600, 290 + i * 56, 900, 1, 40 + i, { col: 'rgba(74,52,35,.35)' });
  promVignette(ctx, t, 90, 300, 300, 250);
  // zincir: vinyetin üst kazığından sarkarak çıkar, sayfanın ortasında temiz bir soru işareti çizer (kanca + sap); kırmızı nokta altına düşer
  const pts = sampleF(u => {
    if (u < .4) { const v = u / .4; return [lerp(380, 850, v), lerp(330, 290, v) + Math.sin(v * PI) * 70]; }
    if (u < .86) { const v = (u - .4) / .46, a = lerp(PI, PI * 2.25, v); return [1000 + Math.cos(a) * 150, 290 + Math.sin(a) * 125]; }
    const v = (u - .86) / .14, x0 = 1000 + Math.cos(PI * 2.25) * 150, y0 = 290 + Math.sin(PI * 2.25) * 125;
    return [(1 - v) * (1 - v) * x0 + 2 * v * (1 - v) * 1000 + v * v * 1000, (1 - v) * (1 - v) * y0 + 2 * v * (1 - v) * 410 + v * v * 480];
  }, 140);
  const k = ramp(lt, .15, 1.9, E.lin);
  inkPoly(ctx, pts, k, { col: PW.line, w: 5, jit: .6 });
  const n = Math.floor(48 * k);
  for (let i = 0; i < n; i++) { const q = pts[Math.floor(i / 48 * 139)]; ctx.strokeStyle = PW.line; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.ellipse(q[0], q[1], 9, 5, i % 2 ? .8 : -.8, 0, TAU); ctx.stroke(); }
  // soru işaretinin noktası
  if (k > .97) { ctx.fillStyle = PW.red; ctx.beginPath(); ctx.arc(1000, 560, 17 * ramp(lt, 1.85, 2.1, E.outBack), 0, TAU); ctx.fill(); }
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .35, vig: .55, grain: .045 } });

// --- P015: "bir avuç ateş mi?": karanlıkta küçücük bir alev; kamera yukarı kalkınca karanlıktan dev, boş bir taht belirir ---
shot(A('A05@ve'), (ctx, st) => {
  const t = st.t, lt = st.lt, u = E.io2(clamp(lt / st.d));
  glazeBG(ctx, t, { gx: 960, gy: 900, gr: 600, stars: false, warm: 'rgba(150,62,28,.45)' });
  const c = { x: 960, y: lerp(760, 470, u), z: lerp(1.35, 1.0, u) };
  ctx.save(); cam(ctx, c, 1);
  // dev taht: siyah sır kütle, kil kontur; yavaşça görünür
  ctx.save(); ctx.globalAlpha = .4 + .5 * u;
  throneRim(ctx, 960 - 60, 820, 14, 1, { high: true, stool: false });
  ctx.restore();
  // iki uzak şimşek titremesi (Zeus görünmez)
  for (const [tt, x] of [[.9, 620], [2.0, 1320]]) { const f = Math.exp(-Math.pow((lt - tt) / .07, 2)); if (f > .02) { ctx.save(); ctx.globalAlpha = .5 * f; lightning(ctx, x, 80, x + 60, 420, 7 + tt * 10, 4, '#E8ECFF'); ctx.restore(); } }
  // küçücük alev: karenin tek parlak noktası
  humanFires(ctx, t, [[960, 900, 1.15]], 1);
  motes(ctx, t, 16, 29, 'rgba(255,200,120,.9)', [900, 700, 120, 200], 30, 1.3, .7);
  ctx.restore();
  const sr = ramp(t, Se('A05') - .9, PA('P016') + .05, E.io2);
  if (sr > 0) { const x = lerp(960, 1350, sr) + Math.sin(sr * 9) * 18 * (1 - sr), y = lerp(760, 140, sr); glow(ctx, x, y, 50, 'rgba(255,200,120,.55)'); sparkle(ctx, x, y, 16 + 8 * sr, 1, '#FFE9C4'); }
  kayaFrame(ctx, t);
}, { tr: { type: 'ink', dur: .7 }, post: { tex: .55, vig: 1, grain: .06 } });
