// IX. ZİNCİRİN ÖBÜR UCU (J01–J10, doruk): sorgu donar; asıl tutsak kim? Güç'ün levhası; zincirdeki Prometheus;
// "Ama bakalım, gerçekten de öyle mi?"; açılım: zincirin öbür ucunda soğuk bilek (ZEUS · KÖLE), altın ışıkla dönüş (PROMETHEUS · ÖZGÜR);
// çocuk gibi zayıf tiran; bağımlılık; "tutukladığı düşmanının elinde tutukludur"; terazi döner; hakkın köleden yana olduğu; yalnız Aiskhylos
'use strict';

// --- yardımcılar (J_ öneki) ---
const J_SKY = 'gunbatimi';
// anahtar kareli kamera yolu: K = [[zaman, {x,y,z}, yumuşatma?], ...]; her geçiş kendi süresinde
function J_path(t, K) {
  if (t <= K[0][0]) return { ...K[0][1] };
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) { const a = K[i - 1][1], b = K[i][1], u = (K[i][2] || E.io3)(clamp((t - K[i - 1][0]) / (K[i][0] - K[i - 1][0]))); return { x: lerp(a.x, b.x, u), y: lerp(a.y, b.y, u), z: lerp(a.z ?? 1, b.z ?? 1, u) }; }
  return { ...K[K.length - 1][1] };
}
// göğe giden zincir: üst kazığın halkasından bulutların içinden tahtın koluna; bulutlar 'part' ile aralanır
const J_A = () => [PROM_KAYA.sF[0] - 30, PROM_KAYA.sF[1] - 4], J_TOP = [1505, -1150];
const J_chainPt = u => { const a = J_A(); return [lerp(a[0], J_TOP[0], u), lerp(a[1], J_TOP[1], u)]; };
function J_skyChain(ctx, t, part = 0, o = {}) {
  const a = J_A();
  ironChain(ctx, a, J_TOP, { L0: len(sub(J_TOP, a)) * 1.005, w: 6, link: 24 });
  // alçak bulut kuşağı (A02'deki) ve yüksek bulut kuşağı: zincirin iki yanına aralanır
  for (let i = 0; i < 6; i++) { const x = PROM_KAYA.sF[0] - 260 + i * 120 + Math.sin(t * .2 + i) * 20, sg = x < 1470 ? -1 : 1; cloud(ctx, x + sg * part * 380, -560 + (i % 2) * 70, 1.5, '#1A100B', 'rgba(201,112,63,.4)', i + 3); }
  for (let i = 0; i < 7; i++) { const x = 1100 + i * 130 + Math.sin(t * .15 + i * 2) * 16, sg = x < 1500 ? -1 : 1; cloud(ctx, x + sg * part * 520, -880 + (i % 3) * 50, 1.9, '#160D09', 'rgba(201,112,63,.3)', i + 13); }
}
// zincirin öbür ucu: tahtın kolu, buluttan uzanan tek bilek, soğuk beyaz kelepçe (yüz ve gövde yok)
function J_zeusWrist(ctx, t, a, glint = 0) {
  if (a <= 0) return;
  const [x, y] = J_TOP;
  ctx.save(); ctx.globalAlpha *= a;
  glow(ctx, x + 60, y - 40, 420, 'rgba(230,236,255,.14)');
  // tahtın kolu: koyu, kenarı soğuk ışıklı, ucunda sarmal
  ctx.save(); ctx.shadowColor = 'rgba(230,236,255,.8)'; ctx.shadowBlur = 18; ctx.fillStyle = '#120A07';
  ctx.fillRect(x - 260, y + 34, 560, 30); ctx.beginPath(); ctx.arc(x - 260, y + 49, 28, 0, TAU); ctx.fill(); ctx.fillRect(x + 200, y + 60, 26, 300); ctx.restore();
  ctx.strokeStyle = 'rgba(201,112,63,.55)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(x - 260, y + 49, 14, 0, PI * 1.6); ctx.stroke();
  // önkol: sağ üstteki buluttan iner, el kolun üstünde durur (soğuk kontürlü koyu siluet)
  ctx.lineCap = 'round'; const arm = () => { ctx.beginPath(); ctx.moveTo(x + 470, y - 330); ctx.quadraticCurveTo(x + 230, y - 150, x + 20, y - 8); ctx.stroke(); };
  ctx.strokeStyle = 'rgba(230,236,255,.75)'; ctx.lineWidth = 78; arm(); ctx.strokeStyle = '#3E2C24'; ctx.lineWidth = 70; arm();
  // el: tahtın kolunu kavrar; parmaklar kolun üstünden aşağı iner
  ctx.fillStyle = '#3E2C24'; ctx.strokeStyle = 'rgba(230,236,255,.75)'; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.moveTo(x + 40, y - 30); ctx.quadraticCurveTo(x - 40, y - 26, x - 96, y + 24); ctx.quadraticCurveTo(x - 104, y + 46, x - 80, y + 62); ctx.lineTo(x + 40, y + 60); ctx.quadraticCurveTo(x + 60, y + 20, x + 40, y - 30); ctx.closePath(); ctx.fill(); ctx.stroke();
  for (let k = 0; k < 4; k++) { ctx.beginPath(); ctx.moveTo(x - 78 + k * 26, y + 36); ctx.lineTo(x - 80 + k * 26, y + 62); ctx.stroke(); }
  for (let k = 0; k < 3; k++) cloud(ctx, x + 300 + k * 120, y - 250 - k * 40, 2.0, '#1E120C', 'rgba(201,112,63,.45)', 77 + k);
  // kelepçe: soğuk beyaz halka, zincir buradan aşağı iner
  ctx.save(); ctx.translate(x + 10, y - 6); ctx.rotate(-.75); glow(ctx, 0, 0, 90, `rgba(230,236,255,${.3 + .4 * glint})`); ctx.fillStyle = '#E6ECFF'; ctx.fillRect(-14, -34, 28, 68); ctx.strokeStyle = 'rgba(90,100,130,.9)'; ctx.lineWidth = 3; ctx.strokeRect(-14, -34, 28, 68); ctx.restore();
  if (glint > 0) sparkle(ctx, x + 22, y - 30, 46 * glint, glint, '#E6ECFF');
  ctx.restore();
}
// zincir boyunca akan altın ışık: u0 başlangıç (0 Prometheus, 1 Zeus), yön; birkaç atım
function J_goldFlow(ctx, t, a, dir = 1, n = 3, sp = .55) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  for (let k = 0; k < n; k++) { const ph = ((t * sp + k / n) % 1), u = dir > 0 ? ph : 1 - ph, p = J_chainPt(u);
    glow(ctx, p[0], p[1], 80, 'rgba(255,200,110,.55)'); ctx.fillStyle = '#FFE2A8'; ctx.beginPath(); ctx.arc(p[0], p[1], 7, 0, TAU); ctx.fill(); }
  ctx.restore();
}
// donma: renk solar, kil solgunlaşır; ateş canlı kalır (kare yeniden renkli çizilir)
function J_freezeLook(ctx, t, c, fz) {
  if (fz <= 0) return;
  ctx.save(); baseT(ctx); ctx.globalCompositeOperation = 'saturation'; ctx.globalAlpha = .88 * fz; ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, W, H);
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = .1 * fz; ctx.fillStyle = '#D8C8B0'; ctx.fillRect(0, 0, W, H); ctx.restore();
  const R = [[1000, 1500], [1020, 900], [1040, 700], [1080, 560], [1130, 430], [1200, 300], [1290, 190], [1350, 120], [1420, 150], [1500, 95], [1580, 175], [1720, 240], [1990, 290], [2600, 230], [2600, 1500]];
  ctx.save(); cam(ctx, c, 1); ctx.beginPath(); ctx.rect(-6000, -6000, 14000, 14000); ctx.moveTo(R[0][0] - 30, R[0][1]); R.forEach(([x, y]) => ctx.lineTo(x - 30, y)); ctx.closePath(); ctx.clip('evenodd');
  baseT(ctx); cam(ctx, c, .35); humanFires(ctx, t, [[95, 630, .38], [215, 644, .46], [505, 666, .62], [860, 690, 1.6]], fz, { wind: 0, people: [] }); ctx.restore();
}
// tepe etiketleri: ZEUS · KÖLE (J04@köle) ve PROMETHEUS · ÖZGÜR (J04@özgürdür); J05@uşaklarına'da birlikte söner
function J_labels(ctx, t) {
  const tK = A('J04@köle'), tO = A('J04@özgürdür'), off = 1 - ramp(t, A('J05@uşaklarına') - .1, A('J05@uşaklarına') + .5);
  if (t > tK - .3 && off > 0) { const dn = ramp(t, A('J04@prometeus'), tO), y = lerp(220, 190, dn); stamp(ctx, 'ZEUS · KÖLE', 960, y, t - tK, { col: '#E6ECFF', font: '700 84px Cinzel', h: 132, rot: -.04, a: .92 * lerp(1, .42, dn) * off }); }
  if (t > tO - .1 && off > 0) txt(ctx, 'PROMETHEUS · ÖZGÜR', 560, 420, { font: '700 64px Cinzel', col: '#FFC867', ls: 5, a: ramp(t, tO - .1, tO + .4) * off, shadow: 'rgba(255,170,80,.7)', blur: 22 });
}
// kölelik/özgürlük terazisi (P046 ve P154 ile aynı çizim): direk, kiriş, iplerle asılı iki kefe; tilt: kirişin açısı
function J_scale(ctx, px, py, half, tilt, drawL, drawR, col = PC.clayR) {
  const e = [-1, 1].map(sg => [px + sg * half * Math.cos(tilt), py + sg * half * Math.sin(tilt)]);
  ctx.save(); ctx.strokeStyle = col; ctx.lineCap = 'round';
  ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(px, py + 420); ctx.lineTo(px, py - 30); ctx.stroke();
  ctx.fillStyle = col; ctx.beginPath(); ctx.moveTo(px - 70, py + 420); ctx.lineTo(px + 70, py + 420); ctx.lineTo(px, py + 360); ctx.fill();
  ctx.lineWidth = 8; ctx.beginPath(); ctx.moveTo(...e[0]); ctx.lineTo(...e[1]); ctx.stroke();
  ctx.beginPath(); ctx.arc(px, py, 16, 0, TAU); ctx.fill();
  e.forEach(([x, y], i) => { ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - 90, y + 120); ctx.moveTo(x, y); ctx.lineTo(x + 90, y + 120); ctx.stroke();
    ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(x - 110, y + 120); ctx.quadraticCurveTo(x, y + 170, x + 110, y + 120); ctx.stroke();
    ctx.save(); ctx.translate(x, y + 128); (i === 0 ? drawL : drawR)(ctx); ctx.restore(); });
  ctx.restore();
  return e;
}

// --- P233–P238: tek kesintisiz plan: sorgu donar; kamera iki figürün arasından geçip bileğe iter; Güç'ün levhası; kilit ve kıvılcım;
//     "Ama bakalım…"; açılım: zincir boyunca yukarı, bulutlar aralanır, soğuk bilek (ZEUS · KÖLE); altın ışıkla aşağı (PROMETHEUS · ÖZGÜR) ---
shot(PA('P233'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const tFz = A('J01@durduralım'), tAs = A('J01@asıl'), tZn = A('J02@zincirde'), tAm = A('J02@ama'), tJ4 = A('J04'), tG = A('J04@gerçekte'), tZ = A('J04@zeus'), tP = A('J04@prometeus'), tO = A('J04@özgürdür');
  const fz = ramp(t, tFz - .05, tFz + .3) * (1 - ramp(t, tP, tP + .6));
  const tw = t < tFz ? t : (t < tP ? tFz : tFz + (t - tP)); // dünyanın saati: donmuşken durur
  const wrist = { x: J_TOP[0], y: J_TOP[1] + 140 / 1.6, z: 1.6 };
  const c = J_path(t, [
    [PA('P233'), { x: 700, y: 560, z: 1.1 }], [tFz, { x: 760, y: 560, z: 1.1 }, E.lin], [tAs, { x: 1100, y: 520, z: 1.2 }],
    [tZn, { x: 1418, y: 190, z: 3.0 }], [tAm, { x: 1424, y: 184, z: 3.1 }, E.lin], [tJ4, { x: 1440, y: -120, z: 2.4 }, E.in2],
    [tG, { x: 1480, y: -820, z: 1.75 }, E.lin], [tZ, wrist, E.out3], [tP, { ...wrist, z: 1.66 }, E.lin], [tO, { x: 1050, y: 560, z: 1.5 }, E.io2], [st.end, { x: 1046, y: 562, z: 1.52 }, E.lin]]);
  const { wind } = kayaWorld(ctx, tw, c, { sky: J_SKY, wind: lerp(windAt(tw), 0, fz) });
  ctx.save(); cam(ctx, c, 1);
  const part = E.io2(ramp(t, A('J04@verir') - .2, tG + .2));
  J_skyChain(ctx, tw, part);
  J_zeusWrist(ctx, t, ramp(t, tG - .2, tZ), Math.exp(-Math.max(0, t - A('J04@köle')) * 2.5) * (t > A('J04@köle') ? 1 : 0));
  // altın ışık: J04@prometeus'ta kameranın önünde zincir boyunca aşağı iner; sonra zincirde aşağı doğru akar
  const dn = ramp(t, tP, tO, E.lin);
  if (t > tP && t < tO + .1) { const p = J_chainPt(1 - dn); glow(ctx, p[0], p[1], 160, 'rgba(255,200,110,.6)'); for (let k = 1; k < 10; k++) { const q = J_chainPt(Math.min(1, 1 - dn + k * .03)); glow(ctx, q[0], q[1], 70, `rgba(255,190,100,${.35 * (1 - k / 10)})`); } }
  J_goldFlow(ctx, t, ramp(t, tO - .1, tO + .5), -1, 3, .7);
  // kelepçenin kilidi: Prometheus tarafında parlar (J02@özgürlüğü); asılı bir kıvılcım kilide düşüp söner (J02@yok)
  const lk = PROM_KAYA.sF, lg = ramp(t, A('J02@özgürlüğü') - .1, A('J02@özgürlüğü') + .5) * (1 - ramp(t, tAm, tAm + 1));
  if (lg > 0) { glow(ctx, lk[0] - 14, lk[1] + 22, 46, `rgba(255,200,120,${.55 * lg})`); ctx.fillStyle = `rgba(255,226,168,${lg})`; ctx.fillRect(lk[0] - 22, lk[1] + 14, 16, 18); }
  const tY = A('J02@yok'); if (t > tY - 1.2 && t < tY + .6) { const u = ramp(t, tY - 1.2, tY, E.in2), x = lk[0] - 14 + Math.sin(u * 6) * 6, y = lerp(lk[1] - 120, lk[1] + 22, u), s = t < tY ? 1 : Math.exp(-(t - tY) * 6); sparkle(ctx, x, y, 14 * s, s, '#FFE2A8'); }
  promChained(ctx, tw, { wind: lerp(wind, 0, fz), look: lerp(.05, -.3, ramp(t, tO - .2, tO + .5)), pose: t > tO ? 'direnis' : 'sessiz', pullAdd: .25 * ramp(t, tO - .1, tO + .4) * (1 - ramp(t, tO + .8, tO + 1.8)), dust: fz > .5 ? .6 : 0 });
  ctx.restore();
  // Hermes: ön katmanda (paralaks 1,6) havada; kerykeion yarı kalkık; donunca asılı kalır
  ctx.save(); cam(ctx, c, 1.6);
  const hu = E.io2(ramp(tw, PA('P233'), tFz + .3, E.lin)), ha = 1 - ramp(t, tAs + 2, tAs + 3.5);
  if (ha > 0) { ctx.globalAlpha = ha; I_hermes(ctx, lerp(520, 716, hu), lerp(960, 840, hu), 5.6, tw, { fly: lerp(.4, 1, hu), raise: .45, flap: .5, dir: 1 }); }
  ctx.restore();
  kayaFront(ctx, tw, c, wind);
  J_freezeLook(ctx, t, c, fz);
  kayaFrame(ctx, t);
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t;
    chapterCard(ctx, 'BÖLÜM IX', 'ZİNCİRİN ÖBÜR UCU', st.lt - .15, 3.3, { y: 170 });
    // P234: donmuş karede Güç'ün kil levhası (P127): döner, altı çizilir
    const tG = A('J02@güçün'), ta = 1 - ramp(t, A('J02@prometeus') - .2, A('J02@prometeus') + .5);
    if (t > tG - .2 && ta > 0) { ctx.save(); ctx.globalAlpha = ta; carvedTablet(ctx, ['ZEUS’TAN BAŞKA HİÇ KİMSE', 'ÖZGÜR DEĞİLDİR.'], 960, 330, 1240, t - tG, { font: '700 62px Cinzel', lh: 78 });
      inkPoly(ctx, [[700, 400], [1220, 396]], ramp(t, A('J02@özgür') - .1, A('J02@değildir') + .3, E.lin), { col: '#E8A04C', w: 6, jit: .6 }); ctx.restore(); }
    // P236: kenar şeridi: soru; şeritteki soru işareti P014'ün zincir-soru işaretidir, soru biterken düzelip zincire döner
    const tE = A('J02@erhat'), tAm = A('J02@ama');
    erhatStrip(ctx, t - tE, A('J04') - tE - .2, '“Ama bakalım, gerçekten de öyle mi?”', 'xiii', { icon: (c, p) => {
      const s = E.io2(ramp(t, tAm + .4, A('J02@mi') + .5));
      const q = u => { const Q = u < .55 ? (() => { const a = lerp(PI * 1.05, -PI * .4, u / .55); return [Math.cos(a) * 34, -18 + Math.sin(a) * 30]; })() : [lerp(Math.cos(-PI * .4) * 34, 0, (u - .55) / .45 * 1.6 > 1 ? 1 : (u - .55) / .45 * 1.6), lerp(-18 + Math.sin(-PI * .4) * 30, 40, (u - .55) / .45)]; return [lerp(Q[0], 0, s), lerp(Q[1], lerp(-60, 60, u), s)]; };
      c.save(); c.globalAlpha = p; c.strokeStyle = PW.line; c.lineWidth = 2.6; for (let i = 0; i < 12; i++) { const a = q(i / 12), b = q((i + 1) / 12), m = lerp2(a, b, .5), an = Math.atan2(b[1] - a[1], b[0] - a[0]); c.save(); c.translate(...m); c.rotate(an); c.beginPath(); c.ellipse(0, 0, 7.5, 4.2, 0, 0, TAU); c.stroke(); c.restore(); }
      if (s < .9) { c.fillStyle = PW.red; c.globalAlpha = p * (1 - s); c.beginPath(); c.arc(0, 68, 6, 0, TAU); c.fill(); } c.restore(); } });
    J_labels(ctx, t);
    erhatTag(ctx, t - A('J04@özgürdür'), 'ERHAT · ÖNSÖZ · S. XIV', { d: A('J05@uşaklarına') - A('J04@özgürdür') + .3, delay: .4 });
  } });

// --- P239: tahtın içinde yüzsüz bir gölge; J05@çocuk'ta çocuk boyuna küçülür, koltuğun koluna yapışmış küçük el; boş tahta eğilen uşaklar (P188'in kırmızı figür kopyası) ---
shot(PA('P239'), (ctx, st) => {
  const t = st.t, lt = st.lt, tU = A('J05@uşaklarına'), tC = A('J05@çocuk');
  glazeBG(ctx, t, { gx: 960, gy: 700, gr: 1000, stars: false, warm: 'rgba(120,50,22,.42)' });
  const c = { x: 960 + lt * 3, y: 540, z: 1.0 + lt * .006 };
  ctx.save(); cam(ctx, c, 1);
  const gy = 820; ctx.fillStyle = PC.clayR; ctx.fillRect(-200, gy, 2400, 6);
  // taht: büyük, kenarı soğuk ışıklı
  ctx.save(); ctx.shadowColor = 'rgba(230,236,255,.7)'; ctx.shadowBlur = 20; throne(ctx, 960, gy, 6.4, -1, '#120A07', 'rgba(201,112,63,.5)', { high: true }); ctx.restore();
  // yüzsüz gölge: oturur; J05@çocuk'ta küçülür, eli koltuğun koluna yapışır
  const sh = E.io2(ramp(t, tC - .2, tC + 1.0)), s = lerp(6.0, 2.7, sh), seatY = gy - 26 * 6.4, sx = 1000;
  figure(ctx, { x: sx, y: seatY - 4 * s, s, dir: -1, still: true, sty: { fill: '#0A0605', cut: 'rgba(0,0,0,0)', red: '#0A0605', white: '#0A0605', line: 'rgba(230,236,255,.8)' }, lk: { hair: 'long', garment: 'robe', beard: sh > .5 ? null : 'full' }, seed: 5,
    p: { torso: lerp(-.05, .15, sh), neck: lerp(0, .25, sh), head: lerp(0, .2, sh), handN: 'press' }, ik: { fN: [sx - 20 * s, seatY + lerp(24, 10, sh) * s, 0], fF: [sx - 16 * s, seatY + lerp(24, 10, sh) * s, .2], hN: [sx - lerp(18, 26, sh) * 6.4 * .3 - 40 * sh, seatY - 10 * s] } });
  // eğilen uşaklar: iki yanda, domino gibi tahta doğru
  const sty = { ...STY.red, white: STY.red.fill };
  [[220, 1, LK.kratos], [370, 1, LK.bia], [520, 1, LK.hephaistos], [1400, -1, LK.hermes], [1560, -1, { beard: 'full', hair: 'long', garment: 'robe' }]].forEach(([x, dir, lk], i) => {
    const del = (1 - Math.abs(x - 960) / 700) * .8, b = E.out2(ramp(t, tU + del, tU + del + .7));
    H_rf(ctx, x, gy, 4.0, dir, lk, { torso: .55 * b, neck: .25 * b, head: .2 * b, shN: .2 + .3 * b, elN: .4 }, { sty, hold: lk === LK.hermes ? { N: HOLD.caduceus() } : undefined });
  });
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 }, over: (ctx, st) => J_labels(ctx, st.t) });

// --- P240: dikey dünyada zincir: altın ışık Prometheus'un ucundan Zeus'un soğuk beyaz ucuna akar (bağımlılık) ---
shot(PA('P240'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { x: 1470, y: -480 - lt * 8, z: .74 };
  const { wind } = kayaWorld(ctx, t, c, { sky: J_SKY });
  ctx.save(); cam(ctx, c, 1);
  J_skyChain(ctx, t, 1);
  J_zeusWrist(ctx, t, 1, .2 + .2 * Math.sin(t * 2));
  J_goldFlow(ctx, t, ramp(t, A('J05@onu'), A('J05@kurtarabilecek')), 1, 4, .32);
  promChained(ctx, t, { wind, look: -.35, pose: 'gok' });
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P241: tam sayfa alıntı: “Zeus tutukladığı düşmanının elinde tutukludur aslında.”; sayfada iki uç arasındaki zincirin kilidi Zeus tarafına geçer ---
shot(PA('P241'), (ctx, st) => {
  const t = st.t, lt = st.lt, tT = A('J06@tutukludur');
  ctx.save(); cam(ctx, { x: 960 + lt * 3, y: 540, z: 1.02 }, 1);
  paperBG(ctx, t, { seed: 81 });
  const gy = 860;
  inkPoly(ctx, [[140, gy], [1780, gy]], ramp(lt, 0, 1), { w: 3, jit: .6 });
  H_lek(ctx, 380, gy, 3.6, 1, LK.promFree, { torso: -.05, head: -.1, shN: .9, elN: .3, handN: 'fist' });
  throne(ctx, 1560, gy, 3.0, -1, PW.line, PW.paper, { high: true });
  // zincir: Prometheus'un bileğinden tahtın koluna; kilit ortadan Zeus tarafına kayar
  const pts = sampleF(u => [lerp(470, 1480, u), lerp(600, 680, u) + Math.sin(u * PI) * 60], 50);
  inkPoly(ctx, pts, ramp(lt, .2, 1.2, E.lin), { w: 4, jit: .4 });
  for (let i = 0; i < 22; i++) { const q = pts[Math.floor(i / 22 * 49)]; ctx.strokeStyle = PW.line; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.ellipse(q[0], q[1], 11, 6, i % 2 ? .5 : -.5, 0, TAU); ctx.stroke(); }
  const m = E.io3(ramp(t, tT - .3, tT + 1.0)), q = pts[Math.floor(lerp(.12, .9, m) * 49)];
  ctx.save(); ctx.translate(q[0], q[1] + 22); ctx.strokeStyle = PW.red; ctx.fillStyle = PW.paperL; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(0, -16, 14, PI, TAU); ctx.stroke(); ctx.fillRect(-20, -16, 40, 34); ctx.strokeRect(-20, -16, 40, 34); ctx.beginPath(); ctx.arc(0, 0, 4, 0, TAU); ctx.fillStyle = PW.red; ctx.fill(); ctx.restore();
  ctx.restore();
}, { tr: { type: 'ink', dur: .5, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => { const q = A('J06@zeus'); quoteCard(ctx, 'Zeus tutukladığı düşmanının elinde tutukludur aslında.', 'A. ERHAT · ÖNSÖZ · S. XIV', 960, 250, 1600, st.t - q + .3, { font: 'italic 500 80px "Cormorant Garamond"', lh: 92 }); } });

// --- P242: sert kesme: dikey eksen bir teraziye döner (pivot 960,430); J06@sanık'ta kaya ucu yükselir (SANIK: özgür), J06@yargıç'ta taht ucu iner (YARGIÇ: tutsak); figürler dik ---
shot(PA('P242'), (ctx, st) => {
  const t = st.t, lt = st.lt, tR = A('J06@roller'), tS = A('J06@sanık'), tY = A('J06@yargıç');
  glazeBG(ctx, t, { gx: 960, gy: 600, gr: 1000, stars: false, warm: 'rgba(140,58,26,.45)' });
  ctx.save(); cam(ctx, { x: 960, y: 520, z: 1.0 + lt * .004 }, 1);
  const a0 = Math.atan2(220 - 640, 1500 - 420), half = Math.hypot(1080, 420) / 2;
  const tilt = lerp(a0, -a0, E.io3(ramp(t, tR, tS + .2, E.lin))) + Math.sin(t * 1.4) * .01 * ramp(t, tS, tS + 1);
  const sty = { ...STY.red, white: STY.red.fill };
  J_scale(ctx, 960, 430, half, tilt, c => { H_rf(c, 0, 20, 3.4, 1, LK.promFree, { torso: -.04, head: -.06 - .1 * ramp(t, tS, tS + .6) }, { sty }); c.strokeStyle = mixCol(PC.clayR, PC.glaze, .35); c.lineWidth = 5; c.beginPath(); c.moveTo(-30, -150); c.quadraticCurveTo(-60, -40, -90, 10); c.stroke(); },
    c => { c.save(); c.shadowColor = 'rgba(230,236,255,.7)'; c.shadowBlur = 14; throne(c, 0, 20, 3.0, -1, '#120A07', 'rgba(201,112,63,.5)', { high: true }); c.restore(); });
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tS = A('J06@sanık'), tY = A('J06@yargıç');
    txt(ctx, 'SANIK: özgür', 420, 460, { font: '700 64px Cinzel', col: '#FFC867', ls: 3, a: ramp(t, tS - .1, tS + .4), shadow: 'rgba(0,0,0,.8)', blur: 12 });
    txt(ctx, 'YARGIÇ: tutsak', 1500, 520, { font: '700 64px Cinzel', col: '#E6ECFF', ls: 3, a: ramp(t, tY - .1, tY + .4), shadow: 'rgba(0,0,0,.8)', blur: 12 });
  } });

// --- P243: KAYA; köle frizi: kölelerden biri başını kaldırır; şerit: “hakkın köleden yana olduğu” (s. xiii), terazi köleden yana eğilir ---
shot(PA('P243'), (ctx, st) => {
  const t = st.t, lt = st.lt, tH = A('J10@hakkın');
  const c = { ...CAMS.orta, x: 1250 - lt * 4, y: 520, z: 1.4 };
  const { wind } = kayaWorld(ctx, t, c, { sky: J_SKY });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: .04, pose: 'direnis' }); ctx.restore();
  kayaFront(ctx, t, c, wind);
  // köle frizi: kırmızı figür şerit, başları eğik, bilekleri bağlı; biri başını kaldırır
  ctx.save(); baseT(ctx); const fy = 560, fh = 230, a = ramp(lt, .2, .8);
  ctx.globalAlpha = a; ctx.fillStyle = PC.glaze; ctx.fillRect(0, fy, 1060, fh); meanderSaltire(ctx, 0, 1060, fy, 22, PC.clayR, PC.glaze); meanderSaltire(ctx, 0, 1060, fy + fh - 22, 22, PC.clayR, PC.glaze);
  ctx.beginPath(); ctx.rect(0, fy + 22, 1060, fh - 44); ctx.clip();
  for (let i = 0; i < 6; i++) { const x = 90 + i * 170 + ((t * 26) % 170), up = i === 3 ? E.out3(ramp(t, tH - .1, tH + .7)) : 0;
    H_rf(ctx, x, fy + fh - 26, 1.9, 1, i % 2 ? LK.humanF : LK.human, { torso: .35 - .4 * up, neck: .35 - .5 * up, head: .3 - .45 * up, shN: -.2, elN: .5, shF: -.3, elF: .6, handN: 'fist', handF: 'fist' }, { sty: { ...STY.red, white: STY.red.fill }, seed: 120 + i }); }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tH = A('J10@hakkın');
    erhatStrip(ctx, t - tH + .3, st.end - tH - .1, '“hakkın köleden yana olduğu”', 'xiii', { icon: (c, p) => { const k = E.io2(ramp(t, A('J10@köleden'), A('J10@yana') + .4)), tl = lerp(0, .32, k); c.save(); c.globalAlpha = p; c.strokeStyle = PW.line; c.lineWidth = 4; c.beginPath(); c.moveTo(0, 70); c.lineTo(0, -20); c.stroke();
      const e = [-1, 1].map(sg => [sg * 50 * Math.cos(tl), -20 + sg * 50 * Math.sin(tl)]); c.beginPath(); c.moveTo(...e[0]); c.lineTo(...e[1]); c.stroke(); e.forEach(([x, y], i) => { c.beginPath(); c.moveTo(x - 18, y + 24); c.quadraticCurveTo(x, y + 36, x + 18, y + 24); c.stroke(); if (i === 0) { c.fillStyle = PW.red; c.beginPath(); c.arc(x, y + 14, 6, 0, TAU); c.fill(); } }); c.restore(); } });
  } });

// --- P244: sert kesme: boş tiyatroda tek kandil ışığında Aiskhylos yazar; yapayalnız ---
shot(PA('P244'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { x: 960 + lt * 4, y: 560, z: 1.06 + lt * .01 };
  theatre(ctx, t, c, { day: 0, crowd: false });
  ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(8,5,4,.55)'; ctx.fillRect(0, 0, W, H); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  const gy = 820, fl = .85 + .15 * noise1(t * 5, 3);
  glow(ctx, 1080, gy - 200, 420 * fl, 'rgba(255,170,80,.22)');
  ctx.fillStyle = PC.clayR; ctx.fillRect(1020, gy - 150, 160, 10); ctx.fillRect(1090, gy - 140, 14, 140);
  flame(ctx, 1150, gy - 150, .55, t, { haloR: 120 });
  figure(ctx, { x: 900, y: gy - 26 * 5.4, s: 5.4, dir: 1, sty: STY.red, lk: AISKH, seed: 31, stripe: .5, p: { torso: .3, neck: .25, head: .2, shN: 1.2 + .1 * Math.sin(t * 3), elN: 1.1, handN: 'fist', breath: .5 * Math.sin(t * 1.5) }, ik: { fN: [900 + 20 * 5.4, gy - 3 * 5.4, 0], fF: [900 + 15 * 5.4, gy - 3 * 5.4, 0] } });
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });
