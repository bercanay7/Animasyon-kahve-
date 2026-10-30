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
// zincirin öbür ucu (R = zincirin halkası): tahtın sarmallı kolu, profilden yumruk, buluttan inen dolu önkol, demir kelepçe (yüz ve gövde yok)
// açılım karesinde R ekranda ≈ (1150, 470): yumruk ≈ (1040, 480), kelepçe ≈ (1165, 428), taht kolu x 620–1500, y 580–630; ZEUS · KÖLE mührü solda boş gökte
function J_zeusWrist(ctx, t, a, glint = 0) {
  if (a <= 0) return;
  const [x, y] = J_TOP, cold = '#E6ECFF', dark = '#1A100B';
  ctx.save(); ctx.globalAlpha *= a; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  glow(ctx, x + 80, y - 60, 460, 'rgba(230,236,255,.13)');
  // bulut kümesi: önkol içinden çıkar
  for (let k = 0; k < 4; k++) cloud(ctx, x + 260 + k * 110, y - 330 + k * 28 - (k % 2) * 40, 2.1, '#1E120C', 'rgba(201,112,63,.5)', 77 + k);
  // tahtın kolu: kalın koyu kiriş, önde sarmal uç, arkada aslan pençeli ayak
  const ed = (fn, w) => { ctx.strokeStyle = cold; ctx.lineWidth = w + 8; fn(); ctx.stroke(); ctx.strokeStyle = dark; ctx.lineWidth = w; fn(); ctx.stroke(); };
  ed(() => { ctx.beginPath(); ctx.moveTo(x - 300, y + 86); ctx.lineTo(x + 210, y + 86); }, 30);
  ed(() => { ctx.beginPath(); ctx.moveTo(x + 190, y + 90); ctx.lineTo(x + 196, y + 420); }, 26);
  ctx.save(); ctx.translate(x - 318, y + 84); ctx.strokeStyle = cold; ctx.lineWidth = 6; ctx.beginPath(); for (let a2 = 0; a2 < TAU * 1.6; a2 += .1) { const r = 34 - a2 * 3; a2 ? ctx.lineTo(Math.cos(a2) * r, Math.sin(a2) * r) : ctx.moveTo(r, 0); } ctx.stroke(); ctx.restore();
  // önkol: buluttan bileğe; dolu koyu, soğuk kenar
  ed(() => { ctx.beginPath(); ctx.moveTo(x + 470, y - 360); ctx.quadraticCurveTo(x + 230, y - 170, x + 20, y - 30); }, 70);
  // yumruk: profilden, tahtın kolunun üstünde; dört boğum çizgisi, başparmak
  ctx.save(); ctx.translate(x - 70, y + 8);
  ctx.beginPath(); ctx.moveTo(-82, -40); ctx.quadraticCurveTo(-90, 30, -60, 62); ctx.lineTo(60, 66); ctx.quadraticCurveTo(92, 30, 80, -30); ctx.quadraticCurveTo(40, -66, -30, -62); ctx.closePath();
  ctx.fillStyle = dark; ctx.fill(); ctx.strokeStyle = cold; ctx.lineWidth = 5; ctx.stroke();
  ctx.lineWidth = 3; for (let k = 0; k < 4; k++) { ctx.beginPath(); ctx.moveTo(-62 + k * 30, 18); ctx.quadraticCurveTo(-50 + k * 30, 40, -46 + k * 30, 62); ctx.stroke(); }
  ctx.beginPath(); ctx.moveTo(-74, -18); ctx.quadraticCurveTo(-20, -2, 14, -24); ctx.stroke();
  ctx.restore();
  // kelepçe: bilekte demir halka, soğuk beyaz parlar; zincir alttaki halkadan (R) aşağı iner
  ctx.save(); ctx.translate(x + 10, y - 28); ctx.rotate(-.62); glow(ctx, 0, 0, 110, `rgba(230,236,255,${.32 + .45 * glint})`);
  ctx.fillStyle = '#2A2C33'; ctx.strokeStyle = cold; ctx.lineWidth = 5; ctx.beginPath(); ctx.rect(-26, -46, 52, 92); ctx.fill(); ctx.stroke();
  ctx.lineWidth = 2.5; for (const yy of [-26, 0, 26]) { ctx.beginPath(); ctx.moveTo(-26, yy); ctx.lineTo(26, yy); ctx.stroke(); }
  ctx.restore();
  // zincirin üst parçası önde: halkadan çıkar, tahtın kolunun önünden aşağı iner (yumruğun altından sarkıyor gibi okunmaz)
  { const aP = J_A(), d = sub(aP, J_TOP), L = len(d), u = Math.min(1, 260 / L); ironChain(ctx, [x, y + 14], [x + d[0] * u, y + d[1] * u], { L0: L * u * 1.003, w: 6, link: 24, col: '#2E2E33', hi: '#9A9CA6', bandCol: '#55565C' }); }
  ctx.strokeStyle = cold; ctx.lineWidth = 6; ctx.beginPath(); ctx.ellipse(x, y, 13, 18, 0, 0, TAU); ctx.stroke();
  if (glint > 0) sparkle(ctx, x + 30, y - 50, 50 * glint, glint, cold);
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
// kaya poligonunun dışına kırpar (gökte ve ovada çizilenler kayanın ve üstündeki figürün arkasında kalır); ctx.save() içinde çağrılır
const J_ROCK = [[1000, 1500], [1020, 900], [1040, 700], [1080, 560], [1130, 430], [1200, 300], [1290, 190], [1350, 120], [1420, 150], [1500, 95], [1580, 175], [1720, 240], [1990, 290], [2600, 230], [2600, 1500]];
function J_notRock(ctx, c) { cam(ctx, c, 1); ctx.beginPath(); ctx.rect(-6000, -6000, 14000, 14000); ctx.moveTo(J_ROCK[0][0] - 30, J_ROCK[0][1]); J_ROCK.forEach(([x, y]) => ctx.lineTo(x - 30, y)); ctx.closePath(); ctx.clip('evenodd'); baseT(ctx); }
// donma: renk solar, kil solgunlaşır; ateş canlı kalır (kare yeniden renkli çizilir)
function J_freezeLook(ctx, t, c, fz, o = {}) {
  if (fz <= 0) return;
  ctx.save(); baseT(ctx); ctx.globalCompositeOperation = 'saturation'; ctx.globalAlpha = .88 * fz; ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, W, H);
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = .05 * fz; ctx.fillStyle = '#D8C8B0'; ctx.fillRect(0, 0, W, H); ctx.restore();
  if (o.fires === false) return;
  ctx.save(); J_notRock(ctx, c);
  baseT(ctx); cam(ctx, c, .35); humanFires(ctx, t, [[95, 630, .38], [215, 644, .46], [505, 666, .62], [860, 690, 1.6]], fz, { wind: 0, people: [] }); ctx.restore();
}
// tepe etiketleri: ZEUS · KÖLE (J04@köle) ve PROMETHEUS · ÖZGÜR (J04@özgürdür); J05@uşaklarına'da birlikte söner
function J_labels(ctx, t) {
  const tK = A('J04@köle'), tO = A('J04@özgürdür'), off = 1 - ramp(t, PA('P239') - .05, PA('P239') + .25); // P239 kesmesinde 0,3 sn içinde söner (eğilen uşaklara değmez)
  if (t > tK - .3 && off > 0) { const dn = E.io2(ramp(t, A('J04@prometeus'), tO)); ctx.save(); ctx.translate(lerp(560, 560, dn), lerp(230, 262, dn)); ctx.scale(lerp(1, .72, dn), lerp(1, .72, dn));
    stamp(ctx, 'ZEUS · KÖLE', 0, 0, t - tK, { col: '#E6ECFF', font: '700 84px Cinzel', h: 132, rot: -.04, a: .92 * lerp(1, .5, dn) * off }); ctx.restore(); }
  if (t > tO - .1 && off > 0) txt(ctx, 'PROMETHEUS · ÖZGÜR', 100, 420, { font: '700 52px Cinzel', col: '#FFC867', ls: 5, align: 'left', a: ramp(t, tO - .1, tO + .4) * off, shadow: 'rgba(255,170,80,.7)', blur: 22 });
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
  // donma IX boyunca sürer (X'te I08b@sorguya'da çözülür); J04@özgürdür'den sonra yalnız Prometheus, altın ışık ve ateş renklidir
  const fz = ramp(t, tFz - .05, tFz + .3), tw = Math.min(t, tFz), pc = ramp(t, tO - .1, tO + .3);
  const wrist = { x: J_TOP[0] - 119, y: J_TOP[1] + 44, z: 1.6 };
  const c = J_path(t, [
    [PA('P233'), { x: 700, y: 560, z: 1.1 }], [tFz, { x: 760, y: 560, z: 1.1 }, E.lin], [tAs, { x: 1100, y: 520, z: 1.2 }],
    [tZn, { x: 1418, y: 190, z: 3.0 }], [tAm, { x: 1424, y: 184, z: 3.1 }, E.lin], [tJ4, { x: 1440, y: -120, z: 2.4 }, E.in2],
    [tG, { x: 1480, y: -820, z: 1.75 }, E.lin], [tZ, wrist, E.out3], [tP, { ...wrist, z: 1.66 }, E.lin], [tO, { x: 900, y: 470, z: 1.5 }, E.io2], [st.end, { x: 896, y: 472, z: 1.52 }, E.lin]]);
  const { wind } = kayaWorld(ctx, tw, c, { sky: J_SKY, wind: lerp(windAt(tw), 0, fz) });
  ctx.save(); cam(ctx, c, 1);
  const part = E.io2(ramp(t, A('J04@verir') - .2, tG + .2));
  J_skyChain(ctx, tw, part);
  if (pc < 1) promChained(ctx, tw, { wind: 0, look: .05, pose: 'sessiz', dust: fz > .5 ? .6 : 0 });
  ctx.restore();
  // Hermes: ön katmanda (paralaks 1,6) havada; kerykeion yarı kalkık; donunca asılı kalır
  ctx.save(); cam(ctx, c, 1.6);
  const hu = E.io2(ramp(tw, PA('P233'), tFz + .3, E.lin)), ha = 1 - ramp(t, tP, tP + .4);
  if (ha > 0) { ctx.globalAlpha = ha; I_hermes(ctx, lerp(520, 716, hu), lerp(960, 840, hu), 5.6, tw, { fly: lerp(.4, 1, hu), raise: .45, flap: .5, dir: 1 }); }
  ctx.restore();
  kayaFront(ctx, tw, c, wind);
  J_freezeLook(ctx, t, c, fz);
  ctx.save(); cam(ctx, c, 1);
  J_zeusWrist(ctx, t, ramp(t, tG - .2, tZ) * (1 - ramp(t, tO + .3, tO + .7)), Math.exp(-Math.max(0, t - A('J04@köle')) * 2.5) * (t > A('J04@köle') ? 1 : 0));
  // altın ışık: J04@prometeus'ta kameranın önünde zincir boyunca aşağı iner; sonra zincirde aşağı doğru akar
  const dn = ramp(t, tP, tO, E.lin);
  if (t > tP && t < tO + .1) { const p = J_chainPt(1 - dn); glow(ctx, p[0], p[1], 160, 'rgba(255,200,110,.6)'); for (let k = 1; k < 10; k++) { const q = J_chainPt(Math.min(1, 1 - dn + k * .03)); glow(ctx, q[0], q[1], 70, `rgba(255,190,100,${.35 * (1 - k / 10)})`); } }
  J_goldFlow(ctx, t, ramp(t, tO - .1, tO + .5), -1, 3, .7);
  // kelepçenin kilidi: Prometheus tarafında parlar (J02@özgürlüğü); asılı bir kıvılcım kilide düşüp söner (J02@yok)
  const lk = PROM_KAYA.sF, lg = ramp(t, A('J02@özgürlüğü') - .1, A('J02@özgürlüğü') + .5) * (1 - ramp(t, tAm, tAm + 1));
  if (lg > 0) { glow(ctx, lk[0] - 14, lk[1] + 22, 46, `rgba(255,200,120,${.55 * lg})`); ctx.fillStyle = `rgba(255,226,168,${lg})`; ctx.fillRect(lk[0] - 22, lk[1] + 14, 16, 18); }
  const tY = A('J02@yok'); if (t > tY - 1.2 && t < tY + .6) { const u = ramp(t, tY - 1.2, tY, E.in2), x = lk[0] - 14 + Math.sin(u * 6) * 6, y = lerp(lk[1] - 120, lk[1] + 22, u), s = t < tY ? 1 : Math.exp(-(t - tY) * 6); sparkle(ctx, x, y, 14 * s, s, '#FFE2A8'); }
  // renge dönüş: renkli figür tek parça (ayrı tamponda opak) belirir, ilk anda gri figürle aynı pozda; sonra direnişe geçer
  // (parça parça saydam çizim siyah alt katmanı öne çıkarıp figürü 3–4 kare çamur rengi yapıyordu)
  if (pc > 0) solidAlpha(ctx, pc, o => promChained(o, tFz + Math.max(0, t - tO), { wind: .15, look: lerp(.05, -.3, ramp(t, tO - .2, tO + .5)), poseMix: ['sessiz', 'direnis', ramp(t, tO + .1, tO + .7)], pullAdd: .25 * ramp(t, tO - .1, tO + .4) * (1 - ramp(t, tO + .8, tO + 1.8)) }));
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t;
    chapterCard(ctx, 'BÖLÜM IX', 'ZİNCİRİN ÖBÜR UCU', st.lt - .15, 3.3, { y: 170 });
    // P234: donmuş karede Güç'ün kil levhası (P127): döner, altı çizilir
    const tG = A('J02@güçün'), ta = 1 - ramp(t, A('J02@prometeus') - .2, A('J02@prometeus') + .5);
    if (t > tG - .2 && ta > 0) { ctx.save(); ctx.globalAlpha = ta; carvedTablet(ctx, ['ZEUS’TAN BAŞKA HİÇ KİMSE', 'ÖZGÜR DEĞİLDİR.'], 960, 330, 1240, t - tG, { font: '700 62px Cinzel', lh: 78 });
      if (!NOTEXT) inkPoly(ctx, [[700, 400], [1220, 396]], ramp(t, A('J02@özgür') - .1, A('J02@değildir') + .3, E.lin), { col: '#E8A04C', w: 6, jit: .6 }); ctx.restore(); }
    // P236: kenar şeridi: soru; şeritteki soru işareti P014'ün zincir-soru işaretidir, soru biterken düzelip zincire döner
    const tE = A('J02@erhat'), tAm = A('J02@ama');
    erhatStrip(ctx, t - tE, A('J04') - tE - .2, '“Ama bakalım, gerçekten de öyle mi?”', 'xiii', { icon: (c, p) => {
      const s = E.io2(ramp(t, tAm + .4, A('J02@mi') + .5));
      const q = u => { const Q = u < .55 ? (() => { const a = lerp(PI * 1.05, -PI * .4, u / .55); return [Math.cos(a) * 34, -18 + Math.sin(a) * 30]; })() : [lerp(Math.cos(-PI * .4) * 34, 0, (u - .55) / .45 * 1.6 > 1 ? 1 : (u - .55) / .45 * 1.6), lerp(-18 + Math.sin(-PI * .4) * 30, 40, (u - .55) / .45)]; return [lerp(Q[0], 0, s), lerp(Q[1], lerp(-60, 60, u), s)]; };
      c.save(); c.globalAlpha = p; c.strokeStyle = PW.line; c.lineWidth = 2.6; for (let i = 0; i < 12; i++) { const a = q(i / 12), b = q((i + 1) / 12), m = lerp2(a, b, .5), an = Math.atan2(b[1] - a[1], b[0] - a[0]); c.save(); c.translate(...m); c.rotate(an); c.beginPath(); c.ellipse(0, 0, 7.5, 4.2, 0, 0, TAU); c.stroke(); c.restore(); }
      if (s < .9) { c.fillStyle = PW.red; c.globalAlpha = p * (1 - s); c.beginPath(); c.arc(0, 68, 6, 0, TAU); c.fill(); } c.restore(); } });
    J_labels(ctx, t);
    erhatTag(ctx, t - A('J04@özgürdür'), 'ERHAT · ÖNSÖZ · S. XIV', { d: A('J05@uşaklarına') - A('J04@özgürdür') + .3, delay: .8 });
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
  figure(ctx, { x: sx, y: seatY - 4 * s, s, dir: -1, still: true, shadowBlur: 22, shadowCol: 'rgba(230,236,255,.75)', sty: { fill: '#0A0605', cut: '#0A0605', red: '#0A0605', white: '#0A0605', line: '#0A0605' }, lk: { hair: 'nape', garment: 'robe', beard: null, faceless: true }, seed: 5,
    p: { torso: lerp(-.05, .15, sh), neck: lerp(0, .25, sh), head: lerp(0, .2, sh), handN: 'press' }, ik: { fN: [sx - 20 * s, seatY + lerp(24, 10, sh) * s, 0], fF: [sx - 16 * s, seatY + lerp(24, 10, sh) * s, .2], hN: [sx - lerp(18, 26, sh) * 6.4 * .3 - 40 * sh, seatY - 10 * s] } });
  // eğilen uşaklar: iki yanda, domino gibi tahta doğru
  const sty = { ...STY.red, white: STY.red.fill };
  [[220, 1, LK.kratos], [370, 1, LK.bia], [520, 1, LK.hephaistos], [1400, -1, LK.hermes], [1560, -1, { beard: 'full', hair: 'long', garment: 'robe' }]].forEach(([x, dir, lk], i) => {
    const del = (1 - Math.abs(x - 960) / 700) * .8, b = E.out2(ramp(t, tU + del, tU + del + .7));
    H_rf(ctx, x, gy, 4.0, dir, lk, { torso: .55 * b, neck: .25 * b, head: .2 * b, shN: .2 + .3 * b, elN: .4 }, { sty, hold: lk === LK.hermes ? { N: HOLD.caduceus() } : undefined });
  });
  ctx.restore();
  J_freezeLook(ctx, t, c, 1, { fires: false });
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 }, over: (ctx, st) => J_labels(ctx, st.t) });

// --- P240: dikey dünyada zincir: altın ışık Prometheus'un ucundan Zeus'un soğuk beyaz ucuna akar (bağımlılık) ---
shot(PA('P240'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { x: 1470, y: -480 - lt * 8, z: .74 }, tF = A('J01@durduralım');
  kayaWorld(ctx, tF, c, { sky: J_SKY, wind: 0 });
  ctx.save(); cam(ctx, c, 1); J_skyChain(ctx, tF, 1); ctx.restore();
  J_freezeLook(ctx, t, c, 1);
  ctx.save(); cam(ctx, c, 1); J_zeusWrist(ctx, t, 1, .2 + .2 * Math.sin(t * 2));
  J_goldFlow(ctx, t, ramp(t, A('J05@onu'), A('J05@kurtarabilecek')), 1, 4, .32);
  promChained(ctx, t, { wind: .15, look: -.35, pose: 'gok' });
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
  const ends = J_scale(ctx, 960, 430, half, tilt, c => { c.strokeStyle = mixCol(PC.clayR, PC.glaze, .35); c.lineWidth = 5; c.beginPath(); c.moveTo(-30, -150); c.quadraticCurveTo(-60, -40, -90, 10); c.stroke(); },
    c => { c.save(); c.shadowColor = 'rgba(230,236,255,.7)'; c.shadowBlur = 14; throne(c, 0, 20, 3.0, -1, '#120A07', 'rgba(201,112,63,.5)', { high: true }); c.restore(); });
  ctx.restore();
  // donma sürer (IX): terazi ve taht gri; özgür olan Prometheus renkli kalır (SANIK altın, YARGIÇ soğuk beyaz yazılarla)
  const cc = { x: 960, y: 520, z: 1.0 + lt * .004 };
  J_freezeLook(ctx, t, cc, 1, { fires: false });
  ctx.save(); cam(ctx, cc, 1); H_rf(ctx, ends[0][0], ends[0][1] + 148, 3.4, 1, LK.promFree, { torso: -.04, head: -.06 - .1 * ramp(t, tS, tS + .6) }, { sty }); ctx.restore();
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
  const c = { ...CAMS.orta, x: 1250 - lt * 4, y: 520, z: 1.4 }, tF = A('J01@durduralım');
  kayaWorld(ctx, tF, c, { sky: J_SKY, wind: 0 });
  kayaFront(ctx, tF, c, 0);
  J_freezeLook(ctx, t, c, 1);
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind: .15, look: .04, pose: 'direnis' }); ctx.restore();
  // köle frizi: kırmızı figür şerit, başları eğik, bilekleri bağlı; biri başını kaldırır
  // köle frizi: Prometheus'a değmeyen sol pano (x 0–640, y 470–650)
  ctx.save(); baseT(ctx); const fy = 470, fh = 180, FW2 = 640, a = ramp(lt, .2, .8);
  ctx.globalAlpha = a; ctx.fillStyle = PC.glaze; ctx.fillRect(0, fy, FW2, fh); meanderSaltire(ctx, 0, FW2, fy, 18, PC.clayR, PC.glaze); meanderSaltire(ctx, 0, FW2, fy + fh - 18, 18, PC.clayR, PC.glaze);
  ctx.beginPath(); ctx.rect(0, fy + 18, FW2, fh - 36); ctx.clip();
  for (let i = 0; i < 6; i++) { const x = 50 + i * 110 + ((t * 20) % 110), up = i === 3 ? E.out3(ramp(t, tH - .1, tH + .7)) : 0;
    H_rf(ctx, x, fy + fh - 20, 1.45, 1, i % 2 ? LK.humanF : LK.human, { torso: .35 - .4 * up, neck: .35 - .5 * up, head: .3 - .45 * up, shN: -.2, elN: .5, shF: -.3, elF: .6, handN: 'fist', handF: 'fist' }, { sty: { ...STY.red, white: STY.red.fill }, seed: 120 + i }); }
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
