// II. TANRILARIN TAHT KAVGASI (C01–C18): Hesiodos'un anlattığı soy ve iki devrim dönen siyah figür amforada;
// Erhat'ın tek cümlelik yorumları kenar şeridi, iki devrimin ayrımı (C12–C14) tek sürekli beyaz zemin sayfası.
'use strict';

// --- yardımcılar: tırpan (harpe), kundak, dünya diski, amfora durakları ---
function harpe(c, x, y, s, a, col = C.ink, inc = C.clay) {
  c.save(); c.translate(x, y); c.rotate(a); c.scale(s, s);
  c.fillStyle = col; c.strokeStyle = inc; c.lineWidth = 1.2 / s;
  c.fillRect(-2, 0, 4, 60);
  c.beginPath(); c.moveTo(-2, 0); c.quadraticCurveTo(-40, -8, -46, 28); c.quadraticCurveTo(-30, 6, 2, 8); c.closePath(); c.fill();
  c.beginPath(); c.moveTo(-6, 4); c.quadraticCurveTo(-34, -2, -42, 22); c.stroke();
  c.restore();
}
function bundle(c, x, y, s, col = C.white, line = C.ink) {
  c.save(); c.translate(x, y); c.scale(s, s);
  c.fillStyle = col; c.strokeStyle = line; c.lineWidth = 1.6 / s;
  c.beginPath(); c.ellipse(0, 0, 18, 10, -.2, 0, TAU); c.fill(); c.stroke();
  for (const dx of [-8, 0, 8]) { c.beginPath(); c.moveTo(dx - 3, -8); c.lineTo(dx + 3, 8); c.stroke(); }
  c.restore();
}
// amfora dönüşü durak durak: rotX, durakların şerit x'leri arasında kelimelere bağlı kayar (dönüşün kendisi geçiştir)
function stationRot(t, st, lead = 1.0) {
  let i = 0; for (let k = 0; k < st.length; k++) if (t >= st[k][0] - lead) i = k;
  const a = st[Math.max(0, i - 1)], b = st[i], u = i === 0 ? 1 : E.io3(ramp(t, b[0] - lead, b[0], E.lin));
  return lerp(a[1], b[1], u) + (t - b[0]) * 12;
}
const BLACK = STY.black;
const bf = (c, x, gy, s, dir, lk, p = {}, o = {}) => figure(c, { x, y: gy - 44.5 * s, s, dir, sty: o.sty || BLACK, lk, p, ...o });
// oturan figür: kalça oturakta (throne() oturağı 25·ts), uyluk yatay, baldır dik, ayaklar tabureye. tx, by: tahtın x'i ve tabanı, ts: tahtın ölçeği
function bfSeat(c, tx, by, ts, s, dir, lk, p = {}, o = {}) {
  const ik = { fN: [tx + dir * 25 * ts, by - 5 * ts - 2.6 * s, 0], fF: [tx + dir * 21 * ts, by - 5 * ts - 2.6 * s, .05], ...(o.ik || {}) };
  return figure(c, { x: tx + dir * 2.5 * ts, y: by - 25 * ts - 3.2 * s, s, dir, sty: o.sty || BLACK, seed: o.seed ?? ((tx * 7) | 0), ...o, lk, p, ik });
}
const LK_GAIA = { fem: true, hair: 'long', garment: 'robe', robeDots: true }, LK_RHEA = { fem: true, hair: 'long', garment: 'robe' };
const LK_KRONOS = { beard: 'full', hair: 'long', garment: 'robe', himation: true }, LK_URANOS = { beard: 'long', hair: 'long', garment: 'robe', old: true };
const LK_TITAN = { beard: 'short', hair: 'nape', garment: 'short' };

// --- P025: Olympos'un tepesinde boş taht (siyah figür) + bölüm kartı; "Kayadaki Titan": kayada profil, gökte tahtın soluk görüntüsü ---
shot(A('C01') - 1.8, (ctx, st) => {
  const t = st.t, lt = st.lt;
  clayBG(ctx, C.clayL, C.clayD);
  const z = 1 + lt * .02;
  ctx.save(); ctx.translate(960, 640); ctx.scale(z, z); ctx.translate(-960, -640);
  // Olympos: üç tepeli siyah kütle, kazıma katmanlar
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(-100, 1100); ctx.lineTo(300, 760); ctx.lineTo(620, 820); ctx.lineTo(960, 640); ctx.lineTo(1300, 820); ctx.lineTo(1620, 760); ctx.lineTo(2100, 1100); ctx.fill();
  ctx.strokeStyle = C.clay; ctx.lineWidth = 2; for (let k = 1; k < 5; k++) { ctx.beginPath(); ctx.moveTo(960 - k * 130, 640 + k * 70); ctx.lineTo(960, 640 + k * 40); ctx.lineTo(960 + k * 130, 640 + k * 70); ctx.stroke(); }
  for (let i = 0; i < 4; i++) cloud(ctx, 260 + i * 470 + Math.sin(t * .2 + i) * 30, 360 + (i % 2) * 60, 1.2, 'rgba(23,16,12,.18)', 'rgba(23,16,12,.25)', i);
  throne(ctx, 960 - 10, 642, 7, 1, C.ink, C.clay, { high: true });
  glow(ctx, 960, 460, 260, 'rgba(255,240,200,.12)');
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'clay', dur: .8 }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => chapterCard(ctx, 'BÖLÜM II', 'TANRILARIN TAHT KAVGASI', st.lt - .1, 4.2, { y: 170 }) });
shot(A('C01@kayadaki'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { ...CAMS.yakin, x: 1250 + lt * 6, z: CAMS.yakin.z - .1 - lt * .02 };
  const { wind } = kayaWorld(ctx, t, c, {});
  ctx.save(); cam(ctx, c, .15); ctx.globalAlpha = .22 * ramp(lt, .3, 1.2); throne(ctx, 760, 260, 5.5, 1, '#6C3C23', 'rgba(255,220,180,.4)', { high: true }); ctx.restore();
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: -.18 }); ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'sir', dur: .6 }, post: { tex: .55, vig: 1, grain: .06 } });

// --- C02–C10: amfora durakları (şerit x): darbe, kuşaklar, Hesiodos, Khaos, Gaia, Uranos, devler, tırpan, Titanlar, Kronos, pusu, devrim, yutma, Rheia, taş, Girit, kusma ---
const AMX = { darbe: 0, kusak: 1400, hes: 2800, kaos: 4200, gaia: 5600, uranos: 7000, devler: 8400, tirpan: 9800, titan: 11200, kronos: 12600,
  pusu: 14000, yutma: 15400, rheia: 16800, tas: 18200, girit: 19600, kusma: 21000 };
function amforaII(c, x0, x1, t) {
  const by = 600, s = 4.6;
  c.fillStyle = C.ink; c.fillRect(x0, by, x1 - x0, 6);
  const vis = x => x > x0 - 600 && x < x1 + 600, T = id => t - A(id);
  // darbe: bir figür tahtı ötekinin altından çeker
  if (vis(AMX.darbe)) {
    const k = ramp(T('C02@hükümet'), 0, .9);
    throneTip(c, AMX.darbe + 80 + k * 120, by, 4.6, k * 1.1, { col: C.ink, inc: C.clay });
    bf(c, AMX.darbe - 140, by, s, 1, LK_TITAN, { shN: 1.2 + k * .4, elN: .4, torso: .25 });
    bf(c, AMX.darbe + 340, by + 30 * k, s, -1, LK_KRONOS, { torso: -.4 * k, shN: -1.5 * k, elN: .5 });
  }
  // kuşaklar: dede, baba, oğul basamaklarda; her biri öncekini iter
  if (vis(AMX.kusak)) {
    [[-420, 0], [0, 1], [420, 2]].forEach(([dx, i]) => {
      const step = by - i * 70, push = ramp(T('C02@bir#1') - i * .6, 0, .6);
      c.fillStyle = C.ink; c.fillRect(AMX.kusak + dx - 160, step, 320, 8);
      bf(c, AMX.kusak + dx - (i < 2 ? 0 : 0) - push * 40, step, s * (1 - i * .08), 1, i === 0 ? LK_URANOS : i === 1 ? LK_KRONOS : { beard: 'short', hair: 'long', garment: 'robe' }, { shN: 1.4 * push, elN: .3, torso: .2 * push });
    });
  }
  // Hesiodos: asalı rapsod; ağzından çıkan yazıt girdaba dönüşür
  if (vis(AMX.hes)) {
    bf(c, AMX.hes - 120, by, s, 1, { beard: 'long', hair: 'long', garment: 'robe', himation: true }, { shN: .6, elN: 1.3, torso: .05, head: -.05 }, { hold: { N: HOLD.scepter(80) } });
    dipinto(c, 'ΗΣΙΟΔΟΣ', AMX.hes - 110, 120, 30, { col: C.ink });
    const k = ramp(T('C04@kaos'), -1.2, .2, E.lin);
    for (let i = 0; i < 18; i++) { const u = i / 18, a = u * 8 + t * .8; c.fillStyle = C.ink; c.globalAlpha = clamp(k * 1.4 - u); c.beginPath(); c.arc(AMX.hes + 40 + u * 640 + Math.cos(a) * u * 60, 300 + Math.sin(a) * u * 60, 5 * (1 - u * .5), 0, TAU); c.fill(); }
    c.globalAlpha = 1;
  }
  // Khaos: kıvrılan meander girdabı
  if (vis(AMX.kaos)) {
    c.strokeStyle = C.ink; c.lineWidth = 16;
    c.beginPath(); for (let a = 0; a < TAU * 4; a += .08) { const r = 20 + a * 26; const px = AMX.kaos + Math.cos(a + t * .6) * r, py = 330 + Math.sin(a + t * .6) * r * .75; a ? c.lineTo(px, py) : c.moveTo(px, py); } c.stroke();
    dipinto(c, 'ΧΑΟΣ', AMX.kaos, 70, 34, { col: C.ink });
  }
  // Gaia: yatan toprak-kadın; gövdesinden tepeler yükselir
  if (vis(AMX.gaia)) {
    const k = ramp(T('C04@toprak'), 0, 1.2);
    c.fillStyle = C.ink; c.beginPath(); c.moveTo(AMX.gaia - 600, by); for (let x = -600; x <= 600; x += 20) c.lineTo(AMX.gaia + x, by - k * (90 * Math.exp(-(((x + 150) / 220) ** 2)) + 60 * Math.exp(-(((x - 260) / 160) ** 2)))); c.lineTo(AMX.gaia + 600, by); c.fill();
    c.save(); c.translate(AMX.gaia - 330, by - 70); c.rotate(-1.35);
    figure(c, { x: 0, y: -44.5 * 4, s: 4, dir: 1, sty: BLACK, lk: LK_GAIA, p: { torso: .1, head: .2, shN: .3, elN: 1.2 } });
    c.restore();
    dipinto(c, 'ΓΑΙΑ', AMX.gaia - 330, 112, 56, { col: C.ink });
  }
  // Uranos: yıldızlı kemer Gaia'nın üstüne kapanır
  if (vis(AMX.uranos)) {
    const k = ramp(T('C04@gökü'), -.5, 1.4), cx = AMX.uranos;
    c.fillStyle = C.ink; c.beginPath(); c.ellipse(cx, by, 560, lerp(120, 470, k), 0, PI, TAU); c.ellipse(cx, by, 470, lerp(80, 395, k), 0, TAU, PI, true); c.fill();
    c.fillStyle = C.clay; for (let i = 0; i < 16; i++) { const a = PI + (i + .5) / 16 * PI, r = 515; sparkle(c, cx + Math.cos(a) * r, by + Math.sin(a) * lerp(100, 432, k), 9 + Math.sin(t * 3 + i) * 2, .9, C.clay); }
    // altında Gaia: kemer (Gök) onun üstüne kalkar (P032); ad kemerin omzunda
    bf(c, cx - 40, by, 3.6, 1, LK_GAIA, { torso: .05, head: -.25, shN: .6, elN: .9 });
    dipinto(c, 'ΟΥΡΑΝΟΣ', cx + 470, 140, 56, { col: C.ink, a: ramp(T('C04@uranosu'), -.3, .4) });
  }
  // devler doğar doğmaz toprağa geri tıkılır: küçük figürler zemin çizgisinin altına batar
  if (vis(AMX.devler)) {
    c.save(); c.beginPath(); c.rect(AMX.devler - 700, -200, 1400, by + 200); c.clip();
    for (let i = 0; i < 5; i++) { const sink = ramp(T('C04@geri') + i * .25 - .6, 0, .7); bf(c, AMX.devler - 460 + i * 230, by + sink * 260, 3.4, i % 2 ? 1 : -1, { hair: 'long', beard: i % 2 ? 'short' : null }, { shN: 2.6, shF: 2.4, elN: .2, elF: .3 }); }
    c.restore();
  }
  // Gaia tırpanı döver; çocuklar başlarını çevirir; en küçükleri Kronos tırpanı alır
  if (vis(AMX.tirpan)) {
    const hit = Math.max(0, Math.sin(T('C06') * 6));
    bf(c, AMX.tirpan - 200, by, s, 1, LK_GAIA, { shN: 1.6 + hit * .6, elN: .3 });
    c.fillStyle = C.ink; c.fillRect(AMX.tirpan + 40, by - 120, 120, 120);
    harpe(c, AMX.tirpan + 100, by - 150, 2.2, -.4);
    if (hit > .9) sparkle(c, AMX.tirpan + 70, by - 150, 18, .9, C.white);
  }
  if (vis(AMX.titan)) {
    for (let i = 0; i < 5; i++) { const turn = ramp(T('C06@hiçbiri') - i * .3, 0, .4); bf(c, AMX.titan - 480 + i * 200, by, 4.2, turn > .5 ? -1 : 1, LK_TITAN, { torso: .05, head: turn * .2 }); }
    const k = ramp(T('C06@en'), 0, .8);
    bf(c, AMX.titan + 560 - 120 * k, by, 3.9, 1, { beard: 'short', hair: 'nape', garment: 'short' }, { shN: 2.2 * k, elN: .4 }, { hold: k > .6 ? { N: G => G.at([0, 3], 0, () => { G.part(cc => { cc.rect(-1.2, -2, 2.4, 14); }, { cutW: .3 }); G.part(cc => { cc.moveTo(0, -2); cc.quadraticCurveTo(-9, -4, -10, 4); cc.quadraticCurveTo(-6, -1, 1, 0); cc.closePath(); }, { cutW: .3 }); }) } : null });
    dipinto(c, 'ΚΡΟΝΟΣ', AMX.titan + 440, 140, 30, { col: C.ink, a: k });
  }
  return by;
}
// Kronos ve Uranos: pusu, savurma, gök geri çekilir; tahtta Kronos çocuklarını yutar; Rheia, taş, Girit, kusma
function amforaIIb(c, x0, x1, t) {
  const by = 600, s = 4.6, vis = x => x > x0 - 600 && x < x1 + 600, T = id => t - A(id);
  c.fillStyle = C.ink; c.fillRect(x0, by, x1 - x0, 6);
  if (vis(AMX.pusu)) {
    const sw = ramp(T('C07@tırpanı'), -.1, .25, E.out3), up = ramp(T('C07@savurdu'), 0, 1.4);
    c.fillStyle = C.ink; c.beginPath(); c.ellipse(AMX.pusu + 250, by, 540, 380 + up * 220, 0, PI, TAU); c.ellipse(AMX.pusu + 250, by, 460, 300 + up * 220, 0, TAU, PI, true); c.fill();
    c.fillStyle = 'rgba(23,16,12,.35)'; c.fillRect(AMX.pusu - 700, 0, 1400, by);
    c.fillStyle = C.ink; c.beginPath(); c.ellipse(AMX.pusu - 260, by, 120, 80, 0, PI, TAU); c.fill();
    bf(c, AMX.pusu - 300 + sw * 120, by - (1 - sw) * 30, s, 1, { beard: 'short', hair: 'nape', garment: 'short' }, { torso: lerp(.6, -.2, sw), shN: lerp(1.0, 2.9, sw), elN: .2, kn: .8 * (1 - sw) },
      { hold: { N: G => G.at([0, 3], 0, () => { G.part(cc => { cc.rect(-1.2, -2, 2.4, 14); }, { cutW: .3 }); G.part(cc => { cc.moveTo(0, -2); cc.quadraticCurveTo(-9, -4, -10, 4); cc.quadraticCurveTo(-6, -1, 1, 0); cc.closePath(); }, { cutW: .3 }); }) } });
    if (sw > 0 && sw < 1) { c.strokeStyle = 'rgba(23,16,12,.5)'; c.lineWidth = 10; c.beginPath(); c.arc(AMX.pusu - 200, by - 260, 260, -2.4, -2.4 + sw * 2.2); c.stroke(); }
  }
  if (vis(AMX.yutma)) {
    throne(c, AMX.yutma - 140, by, 5.4, 1, C.ink, C.clay, { high: true });
    const n = Math.floor(ramp(T('C09@yuttu'), 0, 2.2, E.lin) * 5), lift = (T('C09@yuttu') * 2.2) % 1;
    bfSeat(c, AMX.yutma - 140, by, 5.4, s, 1, LK_KRONOS, { torso: -.1, shN: 2.0 - lift * .6, elN: 1.4, head: -.15 });
    for (let i = n; i < 5; i++) bundle(c, AMX.yutma + 300 + i * 60, by - 20, 1.3);
    const g = ramp(T('C09@oğullarından'), 0, .5) * (1 - ramp(T('C09@kronos'), 0, .5));
    if (g > 0) { bf(c, AMX.yutma - 520, by, s, 1, LK_GAIA, { torso: .15, shN: 1.4, elN: .9 }); dipinto(c, 'ΓΑΙΑ', AMX.yutma - 520, 140, 30, { col: C.ink, a: g }); }
  }
  if (vis(AMX.rheia)) {
    ship(c, AMX.rheia + T('C10') * 30, by - 10, 1.4, t, C.ink, C.clay);
    bf(c, AMX.rheia - 60 + T('C10') * 30, by - 60, 3.6, 1, LK_RHEA, { shN: .9, elN: 1.4 });
    bundle(c, AMX.rheia + 20 + T('C10') * 30, by - 240, 1.2);
    dipinto(c, 'ΡΕΑ', AMX.rheia - 60, 140, 30, { col: C.ink });
  }
  if (vis(AMX.tas)) {
    const k = ramp(T('C10@kundağa'), 0, 1.2);
    throne(c, AMX.tas + 120, by, 5.4, -1, C.ink, C.clay, { high: true });
    bfSeat(c, AMX.tas + 120, by, 5.4, s, -1, LK_KRONOS, { torso: .1, shN: 1.6 + k * .4, elN: 1.2 });
    bf(c, AMX.tas - 330, by, s, 1, LK_RHEA, { shN: 1.5 - k * .2, elN: .3 });
    bundle(c, lerp(AMX.tas - 210, AMX.tas - 70, k), by - 250 - k * 30, 1.3, C.clayD);
  }
  if (vis(AMX.girit)) {
    c.fillStyle = C.ink; c.beginPath(); c.ellipse(AMX.girit, by, 420, 300, 0, PI, TAU); c.fill();
    c.fillStyle = C.clay; c.beginPath(); c.ellipse(AMX.girit, by, 300, 200, 0, PI, TAU); c.fill();
    ram(c, AMX.girit + 90, by - 4, 1.5, -1, {});
    // mağaranın içinde kundaktaki bebek tek parlak nokta; adı mağaranın üstünde, küçük boyda da okunur
    const zg = ramp(T('C10@çocuk'), 0, .5);
    glow(c, AMX.girit - 90, by - 50, 90 + 40 * zg, `rgba(255,232,180,${.25 + .35 * zg})`);
    bundle(c, AMX.girit - 90, by - 42, 2.0, C.white);
    dipinto(c, 'ΖΕΥΣ', AMX.girit - 90, by - 360, 60, { col: C.ink, a: zg });
  }
  if (vis(AMX.kusma)) {
    const k = ramp(T('C10@kusturdu'), 0, 1.6), fall = ramp(T('C10@indirdi'), 0, .9);
    throneTip(c, AMX.kusma + 260, by, 5.4, fall * 1.15, { col: C.ink, inc: C.clay });
    bf(c, AMX.kusma - 300, by, s * 1.05, 1, { beard: 'short', hair: 'long', garment: 'robe', himation: true, headgear: 'wreath' }, { shN: 1.7, elN: .2, torso: .1 });
    bf(c, AMX.kusma + 160 + fall * 80, by + fall * 40, s, -1, LK_KRONOS, { torso: .7 + fall * .5, neck: .4, head: .3 });
    for (let i = 0; i < 5; i++) { const q = clamp(k * 5 - i); if (q > 0) bundle(c, AMX.kusma + 40 - q * (90 + i * 40), by - 200 + q * 180 - Math.sin(q * PI) * 60, 1.2, i === 4 ? C.clayD : C.white); }
  }
}
shot(A('C02'), (ctx, st) => {
  const t = st.t;
  const r = stationRot(t, [[A('C02'), AMX.darbe], [A('C02@bir#1'), AMX.kusak], [A('C04'), AMX.hes], [A('C04@kaos'), AMX.kaos], [A('C04@toprak'), AMX.gaia], [A('C04@gaya#1'), AMX.uranos], [A('C04@ama'), AMX.devler],
    [A('C06'), AMX.tirpan], [A('C06@hiçbiri'), AMX.titan]]);
  amphoraFrieze(ctx, t, r, (c, x0, x1, t) => amforaII(c, x0, x1, t));
}, { tr: { type: 'clay', dur: .7 }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => {
    erhatStrip(ctx, st.t - A('C02@hükümet') + .6, 4.2, '“hükümet darbesi”', 'vi');
    if (st.t > A('C04') - .2 && st.t < A('C04@kaos')) nameTag(ctx, 'HESİODOS', 'Theogonia · İÖ ~700', 110, 760 - 40, st.t - A('C04'), 4.2, { col: C.ink, line: C.red });
  } });
shot(A('C07'), (ctx, st) => {
  const t = st.t;
  const r = stationRot(t, [[A('C07'), AMX.pusu], [A('C09'), AMX.yutma], [A('C10'), AMX.rheia], [A('C10@kundağa'), AMX.tas], [A('C10@o#1'), AMX.girit], [A('C10@babasına'), AMX.kusma]], .9);
  const night = 1 - ramp(t, A('C07@erhat'), A('C07@erhat') + .8);
  amphoraFrieze(ctx, t, r, (c, x0, x1, t) => amforaIIb(c, x0, x1, t), night > 0 ? { clayTop: mixCol(C.clayL, '#5A2C18', .55 * night), clayBot: mixCol(C.clay, '#3A1C0F', .55 * night) } : {});
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => erhatStrip(ctx, st.t - A('C07@erhat') + .3, 3.6, 'DEVRİM', 'vii', { icon: (c, p, lt) => throneTip(c, -10, 60, 3.2, p * 1.15, { col: PW.line, inc: PW.paperL }) }) });

// --- C12–C14: iki devrimin ayrımı, tek sürekli beyaz zemin sayfası ---
const C_ST = () => [
  { at: A('C12') - .2, x: 960, draw: (ctx, lt, t) => {
    const p2 = ramp(t, A('C12@ikincisi'), A('C12@ikincisi') + 1.0);
    // iki taht ve terazi: tırpan (kaba kuvvet) ↔ kundak taşı (akıl); akıl ağır basar
    throneTip(ctx, 560, 470, 4.2, 1.15, { col: PW.line, inc: PW.paperL }); throneTip(ctx, 1360, 470, 4.2, 1.15 * p2, { col: PW.line, inc: PW.paperL });
    dipinto(ctx, 'Ι', 560, 540, 44, { col: PW.red }); dipinto(ctx, 'ΙΙ', 1360, 540, 44, { col: PW.red, a: p2 });
    const tilt = lerp(0, .16, p2) + Math.sin(t * 1.3) * .015;
    ctx.save(); ctx.translate(960, 700); ctx.strokeStyle = PW.line; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(0, -120); ctx.lineTo(0, 120); ctx.stroke();
    ctx.rotate(tilt); ctx.beginPath(); ctx.moveTo(-300, -120); ctx.lineTo(300, -120); ctx.stroke();
    for (const [sx, d] of [[-300, -1], [300, 1]]) { ctx.beginPath(); ctx.moveTo(sx, -120); ctx.lineTo(sx - 60, -40); ctx.lineTo(sx + 60, -40); ctx.closePath(); ctx.stroke(); }
    ctx.restore();
    ctx.save(); ctx.translate(960, 700); ctx.rotate(tilt); harpe(ctx, -300, -110, 1.4, .3, PW.line, PW.paperL); bundle(ctx, 300, -60, 1.6, PW.paperL, PW.line); ctx.restore();
  } },
  { at: A('C12@bu#1'), x: 2900, draw: (ctx, lt, t) => {
    // kâğıda yapıştırılmış siyah figür madalyon: yaşlı Uranos ve Gaia genç Zeus'a öğüt verir
    ctx.save(); ctx.translate(2900, 440); ctx.fillStyle = C.clay; ctx.beginPath(); ctx.arc(0, 0, 330, 0, TAU); ctx.fill(); ctx.strokeStyle = PW.line; ctx.lineWidth = 6; ctx.stroke();
    ctx.beginPath(); ctx.arc(0, 0, 326, 0, TAU); ctx.clip();
    const gy = 220; ctx.fillStyle = C.ink; ctx.fillRect(-330, gy, 660, 6);
    bf(ctx, -150, gy, 3.4, 1, LK_URANOS, { shN: 1.3 + Math.sin(t * 1.5) * .15, elN: .6 });
    bf(ctx, -30, gy, 3.2, 1, LK_GAIA, { shN: 1.2, elN: .9 });
    bf(ctx, 170, gy, 3.3, -1, { beard: 'short', hair: 'long', garment: 'robe' }, { head: .1 });
    ctx.restore();
  } },
  { at: A('C14') - .1, x: 4800, draw: (ctx, lt, t) => {
    // kenar frizi: Zeus'un arkasındaki kalabalıkta küçük bir figür; Erhat'ın kalemi onu daire içine alır
    const y1 = 760; marginBand(ctx, 4050, 5550, 380, y1, ramp(lt, 0, 1));
    bf(ctx, 4300, y1 - 14, 4.2, 1, { beard: 'short', hair: 'long', garment: 'robe', himation: true, headgear: 'wreath' }, {}, { sty: STY.lek });
    for (let i = 0; i < 5; i++) bf(ctx, 4560 + i * 190, y1 - 14, 3.6, -1, i === 2 ? LK.promFree : { beard: i % 2 ? 'short' : null, hair: 'nape', garment: 'short' }, { torso: .05 }, { sty: STY.lek });
    circleMark(ctx, 4940, y1 - 190, 120, 230, ramp(t, A('C14@prometeus'), A('C14@prometeus') + .9));
  } },
];
let C_STATIONS = null;
shot(A('C12') - .2, (ctx, st) => {
  if (!C_STATIONS) C_STATIONS = C_ST();
  const c = pageJourney(ctx, st.t, C_STATIONS);
}, { tr: { type: 'ink', dur: .7 }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => { quoteCard(ctx, 'kaba kuvvetin akılla yenilmesi', null, W / 2, 200, 1500, st.t - A('C12@akılla') + .4, { a: 1 - ramp(st.t, A('C12@bu#1') - .6, A('C12@bu#1')) }); erhatTag(ctx, st.t - A('C14'), 'ERHAT · s. viii'); } });
// C14@onu: kayada Prometheus'un kapalı dudakları, geri çekilme: "kendi ağzından duyacağız"
shot(A('C14@onu'), (ctx, st) => {
  const t = st.t, lt = st.lt, u = E.io2(clamp(lt / st.d));
  const c = { x: lerp(1300, 1150, u), y: lerp(330, 520, u), z: lerp(3.4, 1.3, u) };
  const { wind } = kayaWorld(ctx, t, c, {});
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind }); ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'sir', dur: .6 }, post: { tex: .55, vig: 1, grain: .06 } });

// --- C17–C18: Titanomakhia, Tartaros, Zeus tahtta, dünya paylaşılır; önüne tek engel çıkar: Prometheus ---
const AMY = { savas: 0, devler: 1400, tartaros: 2800, akil: 4200, zeus: 5600, pay: 7000, engel: 8400 };
// çatallı asa (üç dişli / iki dişli): yatık sap, uçta dik çapraz kol ve ileri bakan dişler
function worldFork(c, x, y, r, rot, n, col) {
  c.save(); c.translate(x, y); c.rotate(rot); c.strokeStyle = col; c.lineCap = 'round'; c.lineJoin = 'round'; c.lineWidth = Math.max(4, r * .03);
  const hx = r * .36, sp = r * (n === 3 ? .11 : .08);
  c.beginPath(); c.moveTo(-r * .58, 0); c.lineTo(hx, 0); c.moveTo(hx, -sp); c.lineTo(hx, sp);
  for (let i = 0; i < n; i++) { const yy = n === 3 ? (i - 1) * sp : (i ? sp : -sp); c.moveTo(hx, yy); c.lineTo(hx + r * .2, yy); c.moveTo(hx + r * .2, yy); c.lineTo(hx + r * .15, yy + (yy <= 0 ? -r * .035 : r * .035)); }
  c.stroke(); c.restore();
}
// dünya kalkanı (aspis): üç bölge (yıldızlı gök, dalgalı deniz, karanlık yeraltı), her birinde arması (yıldırım, üç dişli, iki dişli);
// paylaştırmada (split) bölgeler birbirinden ayrılır
function worldDisk(c, x, y, r, split, t) {
  c.save(); c.translate(x, y);
  const off = split * 54, b1 = -r / 3, b2 = r / 3;
  const zone = (y0, y1, dy, fill, draw) => { c.save(); c.translate(0, dy); c.beginPath(); c.arc(0, 0, r, 0, TAU); c.clip(); c.beginPath(); c.rect(-r, y0, 2 * r, y1 - y0); c.clip();
    c.fillStyle = fill; c.fillRect(-r, -r, 2 * r, 2 * r); draw(); c.restore();
    c.save(); c.translate(0, dy); c.strokeStyle = C.clay; c.lineWidth = 3; c.beginPath(); const h0 = Math.max(-r, y0), h1 = Math.min(r, y1);
    for (const yy of [h0, h1]) if (Math.abs(yy) < r - 1) { const hw = Math.sqrt(r * r - yy * yy); c.moveTo(-hw, yy); c.lineTo(hw, yy); } c.stroke(); c.restore(); };
  // gök: siyah, eklenmiş beyaz yıldızlar, ortada eklenmiş beyaz yıldırım
  zone(-r, b1, -off, C.ink, () => { c.fillStyle = C.white; for (let i = 0; i < 14; i++) { const rr = rng(i + 7), sx = (rr() * 2 - 1) * r * .8, sy = -r + rr() * (r * .62); c.beginPath(); c.arc(sx, sy, 2.2 + rr() * 1.6, 0, TAU); c.fill(); }
    bolt(c, 0, -r * .62, r / 300, .35, C.white, 'rgba(0,0,0,0)'); });
  // deniz: kil, siyah dalgalı çizgiler, siyah üç dişli
  zone(b1, b2, 0, C.clay, () => { c.strokeStyle = C.ink; c.lineWidth = 3; for (let k = 0; k < 3; k++) { const yy = b1 + (k + .5) * (b2 - b1) / 3; c.beginPath(); for (let q = 0; q <= 40; q++) { const xx = -r + q / 40 * 2 * r; c.lineTo(xx, yy + Math.sin(q * .9 + t * 1.2 + k) * 6); } c.stroke(); }
    worldFork(c, 0, 0, r, -.08, 3, C.ink); });
  // yeraltı: koyu toprak, kil iki dişli
  zone(b2, r, off, '#2A160E', () => worldFork(c, 0, r * .6, r * .8, .06, 2, C.clay));
  // kalkan kenarı: kalın siyah çember, üstünde kil nokta dizisi (yalnız bütünken)
  c.globalAlpha = 1 - clamp(split * 1.5);
  c.strokeStyle = C.ink; c.lineWidth = 22; c.beginPath(); c.arc(0, 0, r + 10, 0, TAU); c.stroke();
  c.fillStyle = C.clay; for (let i = 0; i < 28; i++) { const a = i / 28 * TAU; c.beginPath(); c.arc(Math.cos(a) * (r + 10), Math.sin(a) * (r + 10), 3, 0, TAU); c.fill(); }
  c.restore();
}
function amforaIIc(c, x0, x1, t) {
  const by = 600, s = 4.4, vis = x => x > x0 - 600 && x < x1 + 600, T = id => t - A(id);
  c.fillStyle = C.ink; c.fillRect(x0, by, x1 - x0, 6);
  if (vis(AMY.savas)) for (let i = 0; i < 6; i++) { const left = i < 3, ph = t * 2 + i; bf(c, AMY.savas - 560 + i * 220, by, s, left ? 1 : -1, left ? LK_TITAN : { beard: 'short', hair: 'long', garment: 'short', headgear: 'helmet' }, { shN: 1.8 + Math.sin(ph) * .5, elN: .3, torso: .2 * (left ? 1 : -1) }, { hold: { N: HOLD.spear(80) } }); }
  if (vis(AMY.devler)) {
    // yerin altından yüz kollu devler çıkar, kaya fırlatır
    const k = ramp(T('C17@yüz'), -.3, .8);
    c.save(); c.beginPath(); c.rect(AMY.devler - 700, -200, 1400, by + 200); c.clip();
    for (let i = 0; i < 2; i++) { const gx = AMY.devler - 220 + i * 440; bf(c, gx, by + (1 - k) * 300, 5.2, i ? -1 : 1, { beard: 'long', hair: 'long' }, { shN: 2.8, shF: 2.6, elN: .1, elF: .2 }); for (let a = 0; a < 6; a++) { c.save(); c.translate(gx, by - 300 + (1 - k) * 300); c.rotate(-1.2 + a * .45 + Math.sin(t * 3 + a) * .1); c.fillStyle = C.ink; c.fillRect(0, -6, 150, 12); c.restore(); } }
    c.restore();
    for (let j = 0; j < 5; j++) { const q = ((t * .6 + j * .2) % 1); c.fillStyle = C.ink; c.beginPath(); c.arc(AMY.devler - 400 + q * 900, 200 + Math.sin(q * PI) * -120 + 120, 22, 0, TAU); c.fill(); }
  }
  if (vis(AMY.tartaros)) {
    // Tartaros: çukurun ağzında çift kanatlı tunç kapı (kazıma panolar, eklenmiş beyaz çiviler); içeride Titanlar düşer; "kapatıldı"da kanatlar kapanır
    const gx = AMY.tartaros, k = ramp(T('C17@tartarosa'), -.1, .6, E.in2), fl = T('C17@titanlar#1');
    c.fillStyle = C.ink; c.beginPath(); c.ellipse(gx, by + 3, 400, 46, 0, 0, PI); c.fill();
    c.fillStyle = '#3A2116'; c.fillRect(gx - 290, by - 300, 580, 300);
    c.save(); c.beginPath(); c.rect(gx - 290, by - 300, 580, 300); c.clip();
    for (let i = 0; i < 3; i++) { const q = fl * .55 - i * .28; if (q > 0 && q < 1.2) bf(c, gx - 150 + i * 150, by - 260 + q * 420, 1.9, i % 2 ? -1 : 1, LK_TITAN, { torso: .5, shN: 2.6, shF: 2.4, elN: .2, elF: .3, kn: .6 }); }
    c.restore();
    for (const e of [-1, 1]) { const w = 290 * lerp(.22, 1, k), x0 = e < 0 ? gx - 290 : gx + 290 - w;
      c.fillStyle = C.ink; c.fillRect(x0, by - 300, w, 300);
      c.strokeStyle = C.clay; c.lineWidth = 2.4; for (let r = 0; r < 3; r++) for (let q = 0; q < 2; q++) { const px = x0 + w * (.1 + q * .44), py = by - 284 + r * 96; c.strokeRect(px, py, w * .36, 80); }
      c.fillStyle = C.white; for (let r = 0; r < 4; r++) for (let q = 0; q < 3; q++) { c.beginPath(); c.arc(x0 + w * (.05 + q * .45), by - 290 + r * 96, 3.6, 0, TAU); c.fill(); } }
    c.fillStyle = C.ink; c.fillRect(gx - 330, by - 300, 40, 300); c.fillRect(gx + 290, by - 300, 40, 300); c.fillRect(gx - 352, by - 336, 704, 38);
    c.strokeStyle = C.clay; c.lineWidth = 2.4; c.beginPath(); c.moveTo(gx - 340, by - 317); c.lineTo(gx + 340, by - 317); c.stroke();
    dipinto(c, 'ΤΑΡΤΑΡΟΣ', gx, by - 390, 60, { col: C.ink });
  }
  if (vis(AMY.akil)) { c.fillStyle = 'rgba(23,16,12,.2)'; for (let i = 0; i < 12; i++) { c.beginPath(); c.arc(AMY.akil - 500 + i * 90, by - 10 - (i % 3) * 8, 30, PI, TAU); c.fill(); } }
  if (vis(AMY.zeus)) {
    throne(c, AMY.zeus - 60, by, 5.6, 1, C.ink, C.clay, { high: true });
    bfSeat(c, AMY.zeus - 60, by, 5.6, s * 1.08, 1, { beard: 'full', hair: 'long', headgear: 'wreath', garment: 'robe', himation: true, robeDots: true }, { torso: -.05, shN: 1.9, elN: .8 });
    bolt(c, AMY.zeus + 210, by - 330, 1.8, -.4, C.white, 'rgba(0,0,0,0)');
    dipinto(c, 'ΖΕΥΣ', AMY.zeus, 120, 34, { col: C.ink, a: ramp(T('C17@yıldırım'), .3, .9) });
  }
  if (vis(AMY.pay)) worldDisk(c, AMY.pay, 330, 220, ramp(T('C17@paylaştırmaya'), 0, 1.2), t);
  if (vis(AMY.engel)) {
    const sh = ramp(T('C18'), 0, 2.0), up = ramp(T('C18@prometeus'), -.3, .4);
    worldDisk(c, AMY.engel - 300, 330, 180, 1, t);
    c.fillStyle = `rgba(23,16,12,${.45 * sh})`; c.beginPath(); c.ellipse(AMY.engel - 200, 330, 260 * sh, 160, -.3, 0, TAU); c.fill();
    bf(c, AMY.engel + 260, by, s * 1.1, -1, LK.promFree, { torso: -.04, head: -.05, scowl: .5 }, { alpha: lerp(.15, 1, up) });
    if (up > .5) sparkle(c, AMY.engel + 205, by - 44.5 * s * 1.1 - 20, 10, up, '#FFE2A0');
  }
}
shot(A('C17'), (ctx, st) => {
  const t = st.t;
  const r = stationRot(t, [[A('C17'), AMY.savas], [A('C17@yüz'), AMY.devler], [A('C17@titanlar#1'), AMY.tartaros], [A('C17@erhata'), AMY.akil], [A('C17@yıldırım'), AMY.zeus], [A('C17@paylaştırmaya'), AMY.pay], [A('C18@tek'), AMY.engel]], .9);
  const sk = shake(t, A('C17@yüz'), 10, 5);
  ctx.save(); ctx.translate(sk[0], sk[1]);
  amphoraFrieze(ctx, t, r, (c, x0, x1, t) => amforaIIc(c, x0, x1, t));
  ctx.restore();
  if (t > A('C17@yıldırım') - .1 && t < A('C17@yıldırım') + .15) { ctx.save(); baseT(ctx); ctx.fillStyle = '#FFF4DE'; ctx.globalAlpha = .35; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}, { tr: { type: 'clay', dur: .7 }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => erhatStrip(ctx, st.t - A('C17@erhata') + .2, 5.4, 'geriye yalnız AKIL kaldı', 'viii') });
