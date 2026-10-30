// VIII. TAHTI SALLAYAN SIR (I01–I07b): kapalı dudaklar ve soğuk mühür, düğün ve babasını aşan oğul, üç taht ve beşik,
// üçüncü devrimin hazırlanması, kuşkunun baskısı, mühürlü ad, Hermes (polis müdürü), alay ve üç tahtın görüntüsü,
// uşaklık tasması, "Eyvah!", yaşlanan zaman, şart
'use strict';

// --- yardımcılar (I_ öneki) ---
const I_SKY = 'gunbatimi';
const I_IKI = { x: 900, y: 600, z: 1.3 };
const I_HX = 640; // Hermes'in kayadaki yeri (dünya x)
// Hermes: petasos, kanatlı çizmeler, kerykeion (kırmızı figür). o.fly: 0 yerde, 1 uçuşta; o.raise: kerykeion kalkışı; o.point: işaret eden kol
function I_hermes(ctx, x, gy, s, t, o = {}) {
  const dir = o.dir || 1, fly = o.fly || 0, rz = o.raise || 0, pt = o.point || 0;
  let J = null, M = null;
  const lk = { ...LK.hermes, rf: true, earHidden: true };
  const p = { torso: lerp(.05, .35, fly) + (o.lean || 0), neck: -.05, head: -.08 - .1 * pt, shN: lerp(.3, 2.3, rz), elN: lerp(.9, .2, rz), handN: 'fist', shF: lerp(-.1, 1.45, pt) + (o.shF || 0), elF: lerp(.6, .08, pt), handF: pt > .5 ? 'point' : (o.handF || 'open'), breath: Math.sin(t * 1.7) * .5, wind: .4 + .4 * fly };
  const hy = gy - 44.5 * s - fly * 30 * s;
  const ik = fly > 0 ? { fN: [x - dir * lerp(8, 20, fly) * s, hy + lerp(41, 38, fly) * s, .4 * fly], fF: [x - dir * lerp(-6, 28, fly) * s, hy + lerp(41, 32, fly) * s, .7 * fly] } : { fN: [x + dir * 8 * s, gy - 3 * s, 0], fF: [x - dir * 7 * s, gy - 3 * s, 0] };
  figure(ctx, { x, y: hy, s, dir, sty: { ...STY.red, white: STY.red.fill }, lk, seed: 33, stripe: .4, hold: { N: HOLD.caduceus() }, p, ik, onJoints: (j, m) => { J = j; M = m; } });
  // çizmelerdeki kanatlar çırpar
  const fl = (o.flap ?? fly) > 0 ? Math.sin(t * 22) * (o.flap ?? fly) : 0;
  if (J) for (const L of [J.LN, J.LF]) { const a = jointPt(ctx, M, L.ank); ctx.save(); ctx.strokeStyle = PC.clayRL; ctx.lineWidth = .7 * s; ctx.lineCap = 'round'; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.moveTo(a[0], a[1] - 2 * s); ctx.lineTo(a[0] - dir * (5 + k * 2.5) * s, a[1] - (6 + k * 2 + fl * 3) * s); ctx.stroke(); } ctx.restore(); }
  return J ? { J, M, hand: jointPt(ctx, M, J.AF.wr), head: jointPt(ctx, M, add(J.neckT, rot([2, -6], J.headA))), wN: jointPt(ctx, M, J.AN.wr) } : null;
}
// karanlıkta kısılan soğuk gözler (taht kuşkusu); n: çift sayısı, nar: 0 açık → 1 kısık
function I_eyes(ctx, t, x, y, R, a, nar = 0, n = 6) {
  if (a <= 0) return;
  ctx.save(); ctx.fillStyle = '#E6ECFF';
  for (let i = 0; i < n; i++) { const ang = -PI + (i + .5) / n * PI * 1.0 - .1, ex = x + Math.cos(ang) * R * (1 + .15 * (i % 2)), ey = y + Math.sin(ang) * R * .55, bl = (.35 + .65 * Math.abs(Math.sin(t * 1.1 + i * 1.9))) * (1 - .8 * nar);
    ctx.globalAlpha = a * (.55 + .45 * bl); for (const dx of [-24, 24]) { ctx.beginPath(); ctx.ellipse(ex + dx, ey, 16, Math.max(1.2, 5.5 * bl), 0, 0, TAU); ctx.fill(); } }
  ctx.restore();
}
// TAHT (kırmızı figür türevi): üç sabit taht x 560/960/1360, taban 760; ghost: devrilme görüntüleri (soluk)
function I_thrones(ctx, t, o = {}) {
  const by = 760, s = o.s || 6.2, col = '#C9703F';
  ctx.fillStyle = PC.clayR; ctx.fillRect(-400, by, W + 800, 6);
  const tip = o.tip || [0, 0];
  [560, 960].forEach((x, i) => { ctx.save(); ctx.globalAlpha *= tip[i] > 0 ? lerp(1, .35, clamp(tip[i])) : 1; throneTip(ctx, x, by, s, tip[i], { col, inc: C.ink, dir: 1 }); ctx.restore(); });
  ctx.save(); if (o.shake) ctx.translate(Math.sin(t * 41) * o.shake, 0);
  throne(ctx, 1360, by, s, 1, col, C.ink, { high: true });
  crackLine(ctx, 1360 + 18 * s, by, 22 * s * .35, 1, { col: '#E6ECFF', w: 3, s: 1.2 });
  ctx.restore();
  if (o.ghost > 0) { ctx.save(); ctx.globalAlpha *= .32 * o.ghost; throneTip(ctx, 1360, by, s, o.ghostTip || 0, { col: '#E6ECFF', inc: PC.glaze }); ctx.restore(); }
  ['ΟΥΡΑΝΟΣ', 'ΚΡΟΝΟΣ', 'ΖΕΥΣ'].forEach((n, i) => dipinto(ctx, n, [560, 960, 1360][i] + 20 + (i === 2 ? 80 : 0), by - 230, 54, { col: PC.clayRL, a: o.na ?? .9 }));
}
// gökteki boş taht: koyu siluet, soğuk beyaz kenar ışığı (karanlıkta okunsun)
function I_skyThrone(ctx, x, y, s, t, o = {}) {
  glow(ctx, x + 40, y - 120, 420, 'rgba(230,236,255,.16)');
  ctx.save(); ctx.shadowColor = 'rgba(230,236,255,.9)'; ctx.shadowBlur = 26; F_throne(ctx, x, y, s, 1, t, o); ctx.restore();
  F_throne(ctx, x, y, s, 1, t, o);
}
// soğuk beyaz mühür (sır): yuvarlak balmumu, ortasında yıldırım
function I_seal(ctx, x, y, r, a, t) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a; glow(ctx, x, y, r * 2.4, `rgba(230,236,255,${.28 + .08 * Math.sin(t * 3)})`);
  ctx.fillStyle = '#DDE4F6'; ctx.beginPath(); for (let k = 0; k <= 24; k++) { const an = k / 24 * TAU, rr = r * (1 + .06 * Math.sin(an * 7)); k ? ctx.lineTo(x + Math.cos(an) * rr, y + Math.sin(an) * rr) : ctx.moveTo(x + Math.cos(an) * rr, y + Math.sin(an) * rr); } ctx.closePath(); ctx.fill();
  ctx.strokeStyle = 'rgba(90,100,130,.8)'; ctx.lineWidth = r * .06; ctx.beginPath(); ctx.arc(x, y, r * .72, 0, TAU); ctx.stroke();
  ctx.fillStyle = 'rgba(90,100,130,.85)'; ctx.beginPath(); ctx.moveTo(x + r * .08, y - r * .5); ctx.lineTo(x - r * .2, y + r * .05); ctx.lineTo(x + r * .02, y + r * .05); ctx.lineTo(x - r * .1, y + r * .52); ctx.lineTo(x + r * .24, y - r * .08); ctx.lineTo(x + r * .02, y - r * .08); ctx.closePath(); ctx.fill();
  ctx.restore();
}
// Prometheus'un gözü (dünya koordinatı): ekran dışı küçük tuvalde kuru çizimle ölçülür
let I_EYEC = null;
function I_eyeAt(t) {
  if (!I_EYEC) I_EYEC = makeCanvas(32, 32).getContext('2d');
  I_EYEC.setTransform(1, 0, 0, 1, 0, 0);
  const R = promChained(I_EYEC, t, { wind: 0 });
  return R && R.J ? jointPt(I_EYEC, R.M, add(R.J.neckT, rot([3.75, -7.1], R.J.headA))) : [1172, 318];
}

// --- P211: bölüm kartı; yukarıda hafifçe titreyen boş taht, aşağıda küçük zincirli figür ---
shot(PA('P211'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { x: 1180 + lt * 5, y: 120 + lt * 6, z: .72 + lt * .006 };
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY, skyChain: true });
  ctx.save(); cam(ctx, c, 1);
  ctx.save(); ctx.translate(Math.sin(t * 37) * 1.8, 0); I_skyThrone(ctx, 1720, -230, 4.4, t); ctx.restore();
  promChained(ctx, t, { wind, look: -.25, pose: 'gok' });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => chapterCard(ctx, 'BÖLÜM VIII', 'TAHTI SALLAYAN SIR', st.lt - .15, 3.3, { y: 170, x: 760 }) });

// --- P212: yakın: kapalı dudaklar; önünde soğuk beyaz bir mühür parlar ---
shot(PA('P212'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { ...G_YK, z: 3.2 + lt * .04 };
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: .02, pose: 'sessiz', p: { mouthOpen: 0 } }); ctx.restore();
  kayaFront(ctx, t, c, wind);
  I_seal(ctx, 600, 420, 80, ramp(t, A('I02@sır') - .2, A('I02@sır') + .5), t);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P213: madalyon: düğün; duvak kaldırma (anakalypsis), yüzler çerçevenin dışında kalır ---
shot(PA('P213'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  glazeBG(ctx, t, { gx: 960, gy: 540, gr: 900, stars: false, warm: 'rgba(120,50,22,.4)' });
  G_medal(ctx, t, 960, 540, 440, Math.sin(t * .3) * .03, (c, t, r) => {
    const gy = r * 1.25, s = 12.5, v = E.io2(ramp(t, A('I02@evlilik') - .3, A('I02@yapacaktı') + .6));
    G_rf(c, -170, gy, s, 1, { beard: 'full', hair: 'long', garment: 'robe', himation: true }, { torso: .05, shF: .5, elF: 1.2, handF: 'open' }, { seed: 91, sty: { ...STY.red, white: STY.red.fill } });
    let J = null, M = null;
    G_rf(c, 190, gy, s * .95, -1, { fem: true, hair: 'long', garment: 'robe' }, { torso: -.02, shN: lerp(.6, 1.9, v), elN: lerp(1.6, .9, v), handN: 'open' }, { seed: 92, onJoints: (j, m) => { J = j; M = m; } });
    // duvak: gelinin kaldırdığı elinden omzuna inen kumaş; yükseldikçe kıvrımları açılır
    if (J) { const h = jointPt(c, M, J.AN.wr), sh = jointPt(c, M, J.neckB);
      c.fillStyle = '#B05A30'; c.strokeStyle = C.ink; c.lineWidth = 4; c.beginPath(); c.moveTo(h[0], h[1]); c.quadraticCurveTo(h[0] + 60, (h[1] + sh[1]) / 2, sh[0] + 90, sh[1] + 140); c.lineTo(sh[0] + 30, sh[1] + 160); c.quadraticCurveTo(h[0] - 20, (h[1] + sh[1]) / 2 + 40, h[0] - 14, h[1] + 10); c.closePath(); c.fill(); c.stroke();
      for (let k = 1; k < 4; k++) { c.beginPath(); c.moveTo(h[0] + k * 4, h[1] + k * 6); c.quadraticCurveTo(h[0] + 30 + k * 10, (h[1] + sh[1]) / 2 + k * 10, sh[0] + 30 + k * 18, sh[1] + 150); c.stroke(); } }
  }, ramp(lt, 0, .4));
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P214: madalyon: bir çocuk silueti büyüyüp babasının gölgesini geçer ---
shot(PA('P214'), (ctx, st) => {
  const t = st.t, lt = st.lt, g = E.io2(ramp(t, A('I02@babasından') - .2, A('I02@doğacaktı') + .6));
  glazeBG(ctx, t, { gx: 960, gy: 540, gr: 900, stars: false, warm: 'rgba(120,50,22,.4)' });
  G_medal(ctx, t, 960, 540, 440, 0, (c, t, r) => {
    const gy = r * .62; c.fillStyle = PC.clayR; c.fillRect(-r, gy, 2 * r, 5);
    // babanın gölgesi: soğuk kontürlü koyu siluet (Zeus kırmızı figürde görünmez; yalnız gölgesi)
    glow(c, 110, gy - 250, 260, 'rgba(230,236,255,.1)');
    c.save(); c.globalAlpha = .95; figure(c, { x: 90, y: gy - 44.5 * 5.6, s: 5.6, dir: -1, sty: { fill: '#0A0605', cut: 'rgba(230,236,255,.0)', red: '#0A0605', white: '#0A0605', line: 'rgba(230,236,255,.85)' }, lk: { beard: 'full', hair: 'long', garment: 'robe' }, seed: 5, still: true, p: { torso: .02 } }); c.restore();
    // oğul: küçükten büyür, sonunda gölgeden uzun
    const s = lerp(1.8, 6.4, g);
    G_rf(c, -120, gy, s, 1, LK.human, { torso: -.04, head: -.08 - .1 * g }, { seed: 93, sty: { ...STY.red, white: STY.red.fill } });
  }, ramp(lt, 0, .3));
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P215–P216: TAHT (siyah figür): Uranos'un ve Kronos'un tahtları devrik, Zeus'un gölgesi beşiğe düşer; kil → kâğıt; üçüncü devrimin hazırlanması ---
shot(PA('P215'), (ctx, st) => {
  const t = st.t, lt = st.lt, tE = A('I03@erhat'), pk = E.io2(ramp(t, tE - .2, tE + 1.0));
  clayBG(ctx, C.clayL, C.clayD);
  if (pk > 0) { ctx.save(); ctx.globalAlpha = pk; paperBG(ctx, t, { book: false, seed: 31 }); ctx.restore(); }
  const c = { x: 960 + lt * 4, y: 520, z: 1.04 + lt * .004 };
  ctx.save(); cam(ctx, c, 1);
  D_thrones(ctx, t, { tip: [1.2, 1.2], crack: .2 + .6 * ramp(t, tE, A('I03@hazırlanması') + .6), crackCol: pk > .5 ? PW.red : PC.fire, na: .7 });
  // beşik (liknon): sallanır; Zeus'un gölgesi üstüne uzanır
  const by = 760, rk = Math.sin(t * 2.2) * .09;
  ctx.save(); ctx.translate(1090, by - 6); ctx.rotate(rk); ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-90, -46); ctx.quadraticCurveTo(-96, 0, -40, 0); ctx.lineTo(70, 0); ctx.quadraticCurveTo(100, -10, 96, -60); ctx.quadraticCurveTo(10, -30, -90, -46); ctx.fill();
  ctx.strokeStyle = C.clay; ctx.lineWidth = 2.5; for (let k = 0; k < 4; k++) { ctx.beginPath(); ctx.moveTo(-70 + k * 40, -38 + k * 3); ctx.lineTo(-60 + k * 40, -4); ctx.stroke(); } ctx.restore();
  const sh = ramp(t, A('I03@şimdi') - .3, A('I03@korkan') + .4);
  if (sh > 0) { ctx.save(); ctx.globalAlpha = .45 * sh; ctx.fillStyle = '#1A0E08'; ctx.beginPath(); ctx.moveTo(1450, by); ctx.lineTo(1430, by - 40); ctx.quadraticCurveTo(1250, by - 120 * sh, 1010, by - 60); ctx.quadraticCurveTo(980, by - 20, 1000, by); ctx.closePath(); ctx.fill(); ctx.restore(); }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'clay', dur: .6, end: true }, post: { tex: .5, vig: .8, grain: .05 },
  over: (ctx, st) => { const t = st.t, tE = A('I03@erhat'); if (t > tE - .1) { erhatStrip(ctx, t - tE, st.end - tE - .3, '“üçüncü devrimin hazırlanması”', 'x'); K_nasil(ctx, 1680, 330, .7, -.06, ramp(t, tE + .4, tE + 1)); } } });

// --- P217: sert kesme: karanlıkta boş taht, çevresinde gözler; uzun gölgeler, sinirli şimşek titremeleri ---
shot(PA('P217'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { x: 1450 - lt * 6, y: -180, z: 1.15 };
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY, skyChain: true });
  ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(14,9,7,.55)'; ctx.fillRect(0, 0, W, H); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  const fl = Math.max(0, Math.sin(t * 6.3) * Math.sin(t * 2.9)), bolt = fl > .55 ? (fl - .55) * 2.2 : 0;
  // uzun gölgeler: tahttan aşağı uzanan koyu çizgiler
  ctx.fillStyle = 'rgba(0,0,0,.4)'; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.moveTo(1480 + k * 40, -230); ctx.lineTo(1100 - k * 160, 400); ctx.lineTo(1160 - k * 160, 400); ctx.closePath(); ctx.fill(); }
  I_skyThrone(ctx, 1480, -230, 3.6, t, { bolt });
  I_eyes(ctx, t, 1540, -330, 330, ramp(t, A('I03@kuşkunun') - .4, A('I03@kuşkunun') + .4), ramp(t, A('I03@baskısı'), A('I03@baskısı') + .6) * .6);
  ctx.restore();
  if (bolt > 0) { ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(230,236,255,${.12 * bolt})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P218: Prometheus'un gözüne dalılır; göz bebeği tondoya açılır: mühürlü bir ad (okunmaz) ---
shot(PA('P218'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('I04@yalnızca');
  const dive = E.in3(ramp(lt, .2, 1.8, E.lin)), e = I_eyeAt(t);
  const c = { x: lerp(G_YK.x, e[0], Math.min(1, dive * 1.6)), y: lerp(G_YK.y, e[1], Math.min(1, dive * 1.6)), z: lerp(3.2, 60, dive) };
  const ta = ramp(lt, 1.5, 2.0);
  if (ta < 1) { const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY }); ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, p: { blink: 0 } }); ctx.restore(); kayaFront(ctx, t, c, wind); }
  if (ta > 0) { ctx.save(); ctx.globalAlpha = ta; ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
    kylix(ctx, t, 960, 540, lerp(380, 430, ta), lt * .03, (k, t, r) => {
      k.fillStyle = PC.glaze; k.beginPath(); k.arc(0, 0, r, 0, TAU); k.fill();
      // kil levhada bir ad: harfler bulanık çizgiler, üstüne soğuk mühür basılır
      k.fillStyle = '#B05A30'; k.fillRect(-260, -90, 520, 180); k.strokeStyle = C.ink; k.lineWidth = 4; k.strokeRect(-260, -90, 520, 180);
      for (let i = 0; i < 2; i++) scribble(k, -220, -30 + i * 60, 440, 1, 70 + i, { w: 6, col: C.ink });
      I_seal(k, 30, 10, 96, ramp(t, A('I04@prometeus') - .2, A('I04@prometeus') + .3), t);
    }); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P219–P221: Hermes uçarak iner (ΕΡΜΗΣ); mühür: POLİS MÜDÜRÜ (Erhat, s. xv; P118 ile kafiye); parmak: SIRRI SÖYLE. ---
shot(PA('P219'), (ctx, st) => {
  const t = st.t, lt = st.lt, tH = A('I05@hermesi'), tE = A('I05@erhatın');
  const c = F_cam(t, [[PA('P219'), { ...CAMS.genis, x: 820, y: 520, z: 1.0 }], [tE, { x: 420, y: 560, z: 1.5 }]], 1.0, 3);
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY });
  ctx.save(); cam(ctx, c, 1);
  const land = E.out3(ramp(t, PA('P219'), tH + .9, E.lin)), fly = 1 - ramp(t, tH + .5, tH + 1.1);
  const hx = lerp(-150, I_HX, land), hgy = lerp(-120, 868, E.io2(land));
  const pt = ramp(t, A('I05@sırrı') - .3, A('I05@sırrı') + .2);
  const R = I_hermes(ctx, hx, hgy, 5.6, t, { fly, flap: Math.max(fly, .3), point: pt, lean: .05 * pt });
  promChained(ctx, t, { wind, look: .1 });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tH = A('I05@hermesi'), tP = A('I05@polis'), tS = A('I05@sırrı');
    const n = ramp(t, tH + .6, tH + 1.1) * (1 - ramp(t, A('I05@erhatın') - .3, A('I05@erhatın')));
    if (n > 0) dipinto(ctx, 'ΕΡΜΗΣ', 520, 330, 56, { col: PC.clayRL, a: n });
    erhatTag(ctx, t - A('I05@erhatın'), 'ERHAT · ÖNSÖZ · S. XV', { d: st.end - A('I05@erhatın') });
    if (t > tP - .3) stamp(ctx, 'POLİS MÜDÜRÜ', 560, 330, t - tP, { col: '#E6ECFF', font: '700 70px Cinzel', h: 116, a: .9 * (1 - ramp(t, tS - .5, tS - .1)) });
    if (t > tS - .3) stamp(ctx, 'SIRRI SÖYLE.', 560, 470, t - tS, { col: '#E6ECFF', font: '700 80px Cinzel', h: 126, rot: .05, a: .92 });
  } });

// --- P222: Prometheus alay eder; süs Yunan harf akışı, baş hareketi ---
shot(PA('P222'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { ...CAMS.orta, x: 1240 - lt * 4 };
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: .05, pose: 'alay', p: { head: -.15 + .12 * Math.sin(ramp(t, A('I06@siz'), A('I06@sanıyorsunuz') + .4) * PI * 2) } }); ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => F_greek(ctx, 'ΝΕΟΝ ΝΕΟΙ ΚΡΑΤΕΙΤΕ ΚΑΙ ΔΟΚΕΙΤΕ ΔΗ', 1080, 300, ramp(st.t, A('I06@siz'), A('I06@sanıyorsunuz') + .4), 1 - ramp(st.t, st.end - .5, st.end), { len: 860 }) });

// --- P223–P224: TAHT (kırmızı figür): üç taht; I06@iki'de iki tahtın devrilişi soluk görüntü; üçüncüsü titrer; düşüşü yalnız soluk bir görüntü, söner; taht yerinde kalır ---
shot(PA('P223'), (ctx, st) => {
  const t = st.t, lt = st.lt, tI = A('I06@iki'), tU = A('I06@üçüncüsünün'), tD = A('I06@düşüşünü'), tC = A('I06@çabuk');
  glazeBG(ctx, t, { gx: 960, gy: 760, gr: 1000, stars: false, warm: 'rgba(150,62,28,.42)' });
  const c = { x: 960 + lt * 4, y: 520, z: 1.04 + lt * .003 };
  ctx.save(); cam(ctx, c, 1);
  const k = ramp(t, tI - .1, A('I06@düştüğünü') + .8);
  I_thrones(ctx, t, { tip: [k * 1.2, clamp(k * 1.2 - .15) * 1.2], shake: 1.6 * ramp(t, tU, tU + .4) * (1 - ramp(t, tC + .2, tC + .8)), ghost: ramp(t, tD - .1, tD + .2) * (1 - ramp(t, tC - .1, tC + .5)), ghostTip: ramp(t, tD, tD + 1.4) * 1.2 });
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'sir', dur: .6, end: true }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P225–P227: sert kesme: Hermes suçlar, elini kaldırır; bileğinden tahta giden soğuk tasma ipi gerilir (söz); Hermes çevresinde döner ---
shot(PA('P225'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('I07@bu'), tO = A('I08');
  const c = F_cam(t, [[PA('P225'), { ...I_IKI, x: 980 }], [tO, { ...I_IKI, x: 1120, z: 1.15 }]], 1.0, 3);
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY });
  ctx.save(); cam(ctx, c, 1);
  // yörünge: I08'den sonra Hermes figürün çevresinde döner (arkadayken önce çizilir)
  const orb = ramp(t, tO, tO + .6), ang = PI + (t - tO) * 1.25 * orb;
  const hx = orb > 0 ? 1180 + Math.cos(ang) * 560 : I_HX, hy = orb > 0 ? 868 + Math.sin(ang) * 90 - 60 * orb : 868, hdir = orb > 0 ? (Math.sin(ang) > 0 ? 1 : -1) * -1 : 1;
  const behind = orb > 0 && Math.sin(ang) < 0;
  let R = null;
  const drawH = () => { R = I_hermes(ctx, hx, hy, 5.6 * (behind ? .9 : 1), t, { fly: orb, dir: orb > 0 ? hdir : 1, point: ramp(t, A('I07@suçlar') - .3, A('I07@suçlar') + .2) * (1 - orb), flap: Math.max(orb, .2) }); };
  if (behind) drawH();
  promChained(ctx, t, { wind, look: t > tB ? -.05 : .08, pose: t > tB && t < tO ? 'direnis' : 'sessiz' });
  if (!behind) drawH();
  // uşaklık: Hermes'in bileğinden göğe (tahta) giden ince soğuk ip; I07@bu'da gerilir
  if (R && orb < 1) { const w = R.wN, sl = 1 - E.out3(ramp(t, tB - .1, tB + .4)); ctx.save(); ctx.globalAlpha = 1 - orb; ctx.strokeStyle = 'rgba(230,236,255,.85)'; ctx.lineWidth = 2.6; ctx.beginPath(); ctx.moveTo(w[0], w[1]); ctx.quadraticCurveTo(w[0] - 60 + 120 * sl, w[1] - 300 + 160 * sl, w[0] - 260, -400); ctx.stroke(); glow(ctx, w[0], w[1], 30, 'rgba(230,236,255,.35)'); ctx.restore(); }
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tB = A('I07@bu'), a = 1 - ramp(t, A('I08') - .3, A('I08') + .2);
    if (t > tB && a > 0) { ctx.save(); ctx.globalAlpha = a; const f = { font: '700 46px Cinzel' };
      speechFlow(ctx, 'BU FELAKETİMİ', u => [lerp(1150, 680, u), 260], ramp(t, tB, A('I07@felaketimi') + .5, E.lin), f);
      speechFlow(ctx, 'SENİN UŞAKLIĞINA', u => [lerp(1150, 630, u), 330], ramp(t, A('I07@senin'), A('I07@uşaklığına') + .5, E.lin), f);
      speechFlow(ctx, 'DEĞİŞMEM.', u => [lerp(1150, 830, u), 400], ramp(t, A('I07@değişmem'), A('I07@değişmem') + .5, E.lin), { ...f, col: '#FFC867' }); ctx.restore(); }
  } });

// --- P228: yakın: EYVAH: rüzgâr 0,7 sn kesilir, figürün kenarından toz kopar, tek zincir halkası sarsılır, 0,1 sn beyaz çakma (kartal gölgesi yok) ---
shot(PA('P228'), (ctx, st) => {
  const t = st.t, lt = st.lt, tE = A('I08@eyvah');
  const c = { ...G_YK, z: 3.3 };
  const still = ramp(t, tE - .05, tE + .05) * (1 - ramp(t, tE + .7, tE + .8));
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY, wind: lerp(.5, 0, still), chainTug: Math.exp(-Math.max(0, t - tE) * 6) * (t > tE ? 1 : 0) });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind: lerp(wind, 0, still), look: .02, pose: 'sessiz', pullAdd: .25 * Math.exp(-Math.max(0, t - tE) * 5) * (t > tE ? 1 : 0), dust: ramp(t, tE, tE + .3) * (1 - ramp(t, tE + .8, tE + 1.2)), p: { mouthOpen: .4 * ramp(t, tE - .1, tE + .1) } });
  motes(ctx, t, 14, 61, 'rgba(201,112,63,.85)', [1060, 280, 300, 420], -20, 1.6, .9 * still);
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  if (t > tE && t < tE + .1) { ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(255,250,240,.55)'; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const tE = A('I08@eyvah'); if (st.t > tE) speechFlow(ctx, 'EYVAH!', u => [lerp(820, 380, u), 400], ramp(st.t, tE, tE + .5, E.lin), { font: '700 84px Cinzel', follow: 0 }); } });

// --- P229: Hermes kendinden memnun eğilir ve havadaki sözü avucuna yakalar ---
shot(PA('P229'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('I08@yakalar');
  const c = { ...I_IKI, x: 900 + lt * 4 };
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY });
  ctx.save(); cam(ctx, c, 1);
  const lean = ramp(t, A('I08@hermes') - .1, tY) * (1 - ramp(t, tY + .5, tY + 1.3));
  const R = I_hermes(ctx, I_HX + 40 * lean, 868, 5.6, t, { lean: .35 * lean, point: lean * .8, handF: t > tY ? 'fist' : 'open', shF: .2 * lean, flap: .4 + .4 * lean });
  if (R) window.I_HAND = H_scr(c, R.hand);
  promChained(ctx, t, { wind, look: .06, pose: 'sessiz' });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tY = A('I08@yakalar'), h = window.I_HAND || [700, 450], k = E.io3(ramp(t, PA('P229'), tY, E.lin)), gone = ramp(t, tY, tY + .25);
    if (gone < 1) { ctx.save(); ctx.globalAlpha = 1 - gone; ctx.font = '700 72px Cinzel'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = PC.clayRL; ctx.shadowColor = 'rgba(255,170,80,.55)'; ctx.shadowBlur = 14;
      [...L('EYVAH!')].forEach((ch, i) => { const x0 = 1080 + i * 52, y0 = 260 + Math.sin(t * 2 + i) * 6, x = lerp(x0, h[0] + (i - 2.5) * 6 * (1 - k), k), y = lerp(y0, h[1], k); ctx.fillText(ch, x, y); }); ctx.restore(); }
    if (t > tY) { const s = Math.exp(-(t - tY) * 4); if (s > .05) sparkle(ctx, h[0], h[1], 40 * s, s, '#FFE9C4'); }
  } });

// --- P230: geniş: sakin cevap; arkada güneş diski gece-gündüz hızla döner (yaşlanan zaman) ---
shot(PA('P230'), (ctx, st) => {
  const t = st.t, lt = st.lt, tZ = A('I08@yaşlanan');
  const c = { ...CAMS.genis, x: 880 + lt * 5 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'gece', clouds: 2 });
  const sp = ramp(t, tZ - .3, tZ + .6) * (1 - ramp(t, st.end - .8, st.end)), ph = (t - tZ) * 1.6;
  // güneş: göğü yay çizerek hızla geçer; gündüz/gece kaplaması onunla nefes alır
  if (sp > 0) { const a = PI + (ph % 1) * PI, x = 960 + Math.cos(a) * 820, y = 760 + Math.sin(a) * 600, day = Math.max(0, -Math.sin(a));
    ctx.save(); baseT(ctx); ctx.globalAlpha = sp; ctx.fillStyle = `rgba(150,66,30,${.35 * day})`; ctx.fillRect(0, 0, W, H); J_notRock(ctx, c);
    for (let k = 1; k < 8; k++) { const aa = a - k * .05; ctx.fillStyle = `rgba(201,112,63,${.25 * (1 - k / 8)})`; ctx.beginPath(); ctx.arc(960 + Math.cos(aa) * 820, 760 + Math.sin(aa) * 600, 70, 0, TAU); ctx.fill(); }
    glow(ctx, x, y, 200, 'rgba(255,190,110,.18)'); sunDisk(ctx, x, y, 70); ctx.restore(); }
  ctx.save(); cam(ctx, c, 1);
  I_hermes(ctx, I_HX, 868, 5.6, t, { flap: .2, lean: -.05 });
  promChained(ctx, t, { wind, look: .04, pose: 'sessiz' });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P231: alttan kahraman karesi; zincirler ışıkta; şart: BU AŞAĞILAYICI ZİNCİRLER ÇÖZÜLMEDEN… ---
shot(PA('P231'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('I07b@bu');
  const c = { ...CAMS.alt, z: 1.45 + lt * .01 };
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY, skyChain: true, glint: .5 + .5 * Math.sin(t * 2) });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: -.12, pose: 'direnis', pullAdd: .2 * ramp(t, tB, tB + .8) }); ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tB = A('I07b@bu'), a = 1 - ramp(t, A('I07b@zeus') + .2, A('I07b@zeus') + .8);
    if (t > tB && a > 0) { ctx.save(); ctx.globalAlpha = a; speechFlow(ctx, 'BU AŞAĞILAYICI ZİNCİRLER', u => [lerp(980, 70, u), 250], ramp(t, tB, A('I07b@zincirler') + .5, E.lin), { font: '700 54px Cinzel', follow: 0 });
      speechFlow(ctx, 'ÇÖZÜLMEDEN…', u => [lerp(980, 560, u), 330], ramp(t, A('I07b@çözülmeden'), A('I07b@çözülmeden') + .6, E.lin), { font: '700 54px Cinzel', follow: 0, col: '#FFC867' }); ctx.restore(); }
  } });

// --- P232: Hermes geri çekilir, kerykeion'unu yeniden kaldırmaya başlar, çizme kanatları çırpar; yukarıda boş tahtın gözleri kısılır (J01@durduralım'da yarıda kalır) ---
shot(PA('P232'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { ...I_IKI, y: 560, z: 1.25 };
  const { wind } = kayaWorld(ctx, t, c, { sky: I_SKY });
  ctx.save(); cam(ctx, c, 1);
  const back = E.io2(ramp(lt, 0, 1.2)), rz = E.in2(ramp(lt, .6, st.d + 1.2, E.lin));
  I_hermes(ctx, I_HX - 70 * back, 868, 5.6, t, { raise: rz * .7, flap: .9, lean: -.08 * back });
  promChained(ctx, t, { wind, look: .02, pose: 'direnis' });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  I_eyes(ctx, t, 960, 200, 400, ramp(lt, .3, 1.0), ramp(t, A('I07b@hileyle') - .3, A('I07b@hileyle') + .6), 5);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const t = st.t, t0 = A('I07b@zeus'); if (t > t0 - .2) F_greek(ctx, 'ΟΥΤΕ ΒΙΑ ΟΥΤΕ ΔΟΛΩι', 1180, 320, ramp(t, A('I07b@ne'), A('I07b@hileyle') + .3), 1 - ramp(t, st.end - .4, st.end), { len: 560 }); } });
