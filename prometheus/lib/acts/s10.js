// X. KARTAL, FIRTINA VE SON SÖZ (I08a–I12): donmuş sorgu çözülür; Hermes'in son tehdidi; yeraltı ve kartal; açılışın eşi (negatif);
// "beni öldüremez"; periler kalır; yıldırım ve fırtına (sözde değil gerçekte); fırtınanın gözünde Themis; kaya yarılır ve kapanır; son söz özgür düşüncenindir
'use strict';

// --- yardımcılar (X_ öneki) ---
const X_TF = () => A('J01@durduralım'); // IX'te donan dünyanın saati
const X_HF = { x: I_HX + 30, gy: 790 }; // Hermes'in donduğu yer (ana katmanda), kerykeion yarı kalkık
// havada asılı kıvılcım ve tozlar: donmuşken yerinde durur, çözülünce düşer (fall: çözülmeden beri geçen süre)
function X_hang(ctx, t, fall, a = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  for (let i = 0; i < 34; i++) { const r = rng(i + 401), x = 700 + r() * 900, y0 = 300 + r() * 500, sp = i % 3 === 0;
    const y = y0 + (fall > 0 ? 420 * fall * fall + 60 * fall : 0); if (y > 1100) continue;
    if (sp) { glow(ctx, x, y, 10, 'rgba(255,190,110,.6)'); ctx.fillStyle = '#FFE2A8'; } else ctx.fillStyle = 'rgba(201,112,63,.75)';
    ctx.beginPath(); ctx.arc(x, y, sp ? 2.6 : 2.2 + r() * 1.5, 0, TAU); ctx.fill(); }
  ctx.restore();
}
// kayada duran peri (kırmızı figür, uzun giysili)
function X_nymph(ctx, x, gy, s, t, i, o = {}) {
  figure(ctx, { x, y: gy - 44.5 * s, s, dir: o.dir || -1, sty: { ...STY.red, white: STY.red.fill }, lk: { fem: true, hair: 'long', garment: 'robe', rf: true, earHidden: true }, seed: 80 + i, stripe: .4,
    p: { torso: o.torso ?? .04, neck: o.neck ?? .05, head: o.head ?? .05, shN: o.shN ?? .4, elN: o.elN ?? .9, shF: .2, elF: .8, breath: Math.sin(t * 1.6 + i) * .5, wind: o.wind || 0 } });
}
// kayayı yaran çatlak: üstten aşağı zikzak yarık; w açıklık (px), glow ateş rengi kenar
function X_crack(ctx, t, w, a, o = {}) {
  if (a <= 0) return;
  const pts = []; for (let k = 0; k <= 40; k++) { const u = k / 40; pts.push([1300 + noise1(u * 3, 7) * 70 + noise1(u * 17, 3) * 14 - u * 120, lerp(60, 1100, u)]); }
  ctx.save(); ctx.globalAlpha *= a;
  if (w > 1) { ctx.fillStyle = PC.glaze; ctx.beginPath(); pts.forEach(([x, y], i) => i ? ctx.lineTo(x - w / 2, y) : ctx.moveTo(x - w / 2, y)); for (let i = pts.length - 1; i >= 0; i--) ctx.lineTo(pts[i][0] + w / 2, pts[i][1]); ctx.closePath(); ctx.fill(); }
  ctx.strokeStyle = o.col || 'rgba(255,170,80,.9)'; ctx.lineWidth = o.lw || 5; ctx.shadowColor = o.col || 'rgba(255,170,80,.9)'; ctx.shadowBlur = 18;
  for (const sg of w > 1 ? [-1, 1] : [0]) { ctx.beginPath(); pts.forEach(([x, y], i) => i ? ctx.lineTo(x + sg * w / 2, y) : ctx.moveTo(x + sg * w / 2, y)); ctx.stroke(); }
  ctx.restore();
}
// sarsıntı: kameraya küçük titreşim
const X_shake = (c, t, k) => ({ ...c, sx: (c.sx || 0) + noise1(t * 23, 3) * 14 * k, sy: (c.sy || 0) + noise1(t * 21, 5) * 10 * k });
// Prometheus'un fırtınadaki sözü (Yunanca süs: "sözde değil, gerçekte": PV 1080): rüzgârda parçalanır ama akar
function X_stormWords(ctx, t, x, y, len, p, a, tear) {
  if (a <= 0 || p <= 0) return;
  const s = 'ΚΑΙ ΜΗΝ ΕΡΓΩι ΚΟΥΚΕΤΙ ΜΥΘΩι';
  ctx.save(); ctx.globalAlpha *= a; ctx.font = '600 50px Cinzel'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = PC.clayRL; ctx.shadowColor = 'rgba(255,170,80,.55)'; ctx.shadowBlur = 14;
  const n = s.length;
  for (let i = 0; i < n; i++) { const q = clamp(p * (n + 4) / 4 - i / 4); if (q <= 0) continue; const u = i / (n - 1), jx = noise1(t * 2 + i * .7, 3) * 60 * tear, jy = noise1(t * 2.3 + i * .9, 8) * 80 * tear, rt = noise1(t * 3 + i, 2) * 1.2 * tear;
    ctx.save(); ctx.translate(x - u * len + jx, y - Math.sin(u * PI) * 40 + jy); ctx.rotate(rt); ctx.globalAlpha *= q; ctx.fillText(s[i], 0, 0); ctx.restore(); }
  ctx.restore();
}

// --- P245: donmuş karede bölüm levhası; renk önce gökteki bulutlara gelir ---
shot(PA('P245'), (ctx, st) => {
  const t = st.t, lt = st.lt, tF = X_TF();
  const c = { ...CAMS.genis, x: 860 + lt * 4, y: 540 };
  kayaWorld(ctx, tF, c, { sky: J_SKY, wind: 0 });
  ctx.save(); cam(ctx, c, 1); J_skyChain(ctx, tF, 0); I_hermes(ctx, X_HF.x, X_HF.gy, 5.6, tF, { fly: 1, raise: .45, flap: .5 }); ctx.restore();
  kayaFront(ctx, tF, c, 0);
  X_hang(ctx, t, 0);
  J_freezeLook(ctx, t, c, 1);
  // renk önce bulutlara: gökte vazo bulutları yavaşça döner
  const ca = ramp(lt, 1.2, 3.6);
  if (ca > 0) { ctx.save(); cam(ctx, c, .2); ctx.globalAlpha = ca; for (let i = 0; i < 5; i++) cloud(ctx, 120 + i * 420 + Math.sin(t * .4 + i) * 30, 130 + (i % 2) * 60 + Math.cos(t * .5 + i) * 10, 1.6, '#24150E', 'rgba(201,112,63,.6)', i + 21); ctx.restore(); }
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind: .1, look: -.1, pose: 'direnis' }); ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => chapterCard(ctx, 'BÖLÜM X', 'KARTAL, FIRTINA VE SON SÖZ', st.lt - .15, 3.3, { y: 170 }) });

// --- P246: I08b@sorguya'da donmuş kare çözülür: renk geri gelir, parçacıklar düşer, Hermes yarım kalan hareketini tamamlar; tehdit; kayanın yarılması yalnız bir görüntü ---
shot(PA('P246'), (ctx, st) => {
  const t = st.t, lt = st.lt, tF = X_TF(), tS = A('I08b@sorguya'), tV = A('I08b@savurur'), tK = A('I08b@kaya');
  const fz = 1 - ramp(t, tS, tS + .8), tw = tF + Math.max(0, t - tS);
  // tehdit planı: Prometheus'un başının tepesi y ≥ 200 (mühür üstte, başa değmez)
  const c = F_cam(t, [[PA('P246'), { ...CAMS.genis, x: 880, y: 540 }], [tV, { ...I_IKI, x: 920, y: I_IKI.y - 47 }]], 1.0, 3);
  const { wind } = kayaWorld(ctx, tw, c, { sky: J_SKY, clouds: 3, wind: lerp(windAt(tw), 0, fz) });
  ctx.save(); cam(ctx, c, 1);
  J_skyChain(ctx, tw, 0);
  // Hermes: kerykeion'u tümüyle kaldırır, yere iner; I08b@savurur'da tehdit
  const go = E.io2(ramp(t, tS + .2, tS + 1.6)), th = ramp(t, tV - .3, tV + .3);
  // mühür süresince (kaya → gömüleceksin) kol bükülür: kerykeion'un tepesi mührün altında kalır
  const bend = ramp(t, tK - .4, tK) * (1 - ramp(t, A('I08b@gömüleceksin') + .3, A('I08b@gömüleceksin') + .9));
  I_hermes(ctx, lerp(X_HF.x, I_HX, go), lerp(X_HF.gy, 868, go), 5.6, tw, { fly: 1 - go, raise: lerp(.45, 1, ramp(t, tS, tS + 1.2)) * (1 - .72 * bend), point: th, lean: .1 * th, flap: lerp(.5, .2, go) });
  // tehdidin görüntüsü (kurulum): soğuk bir yıldırım kayaya iner, kaya yarılır gibi olur; yalnız soluk bir hayal, söner
  const gi = ramp(t, tK - .1, A('I08b@parçalanacak')) * (1 - ramp(t, A('I08b@sen') + .2, A('I08b@gömüleceksin') + .4));
  if (gi > 0) { ctx.save(); ctx.globalAlpha = .45 * gi; lightning(ctx, 1500, -200, 1320, 300, 41, 6, '#E6ECFF'); X_crack(ctx, t, 26 * gi, 1, { col: 'rgba(230,236,255,.8)', lw: 4 }); ctx.restore(); }
  promChained(ctx, tw, { wind, look: .05, pose: 'direnis' });
  ctx.restore();
  kayaFront(ctx, tw, c, wind);
  X_hang(ctx, t, Math.max(0, t - tS), 1 - ramp(t, tS + 1.6, tS + 2.0));
  J_freezeLook(ctx, t, c, fz);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const t = st.t, tV = A('I08b@savurur'); if (t > A('I08b@kaya') - .3) stamp(ctx, 'KAYA PARÇALANACAK', 1000, 110, t - A('I08b@kaya'), { col: '#E6ECFF', font: '700 60px Cinzel', h: 96, rot: .03, a: .9 * (1 - ramp(t, A('I08b@gömüleceksin') + .4, A('I08b@uzun'))) }); } });

// --- P247: yeraltında uzun zaman: karanlık, dönen yıldızlar; sonra ışığa dönüş ---
shot(PA('P247'), (ctx, st) => {
  const t = st.t, lt = st.lt, tI = A('I08b@ışığa');
  const c = { ...CAMS.genis, x: 900, y: 520, z: 1.0 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'gece', starRot: lt * 1.6, fires: false });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, pose: 'sessiz', look: .05, p: { blink: .9 } }); ctx.restore();
  const dk = 1 - ramp(t, tI - .1, A('I08b@döndüğünde') + .4);
  ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(6,4,3,${.82 * dk})`; ctx.fillRect(0, 0, W, H);
  // karanlıkta da dönen yıldızlar (yeraltının üstünde geçen günler)
  ctx.translate(960, 540); ctx.rotate(lt * .9); for (let i = 0; i < 70; i++) { const r = rng(i + 77), rr = 140 + r() * 900, a = r() * TAU; ctx.fillStyle = `rgba(242,214,170,${(.25 + .5 * r()) * dk})`; ctx.beginPath(); ctx.arc(Math.cos(a) * rr, Math.sin(a) * rr, 1.6 + r() * 1.6, 0, TAU); ctx.fill(); }
  ctx.restore();
  if (dk < 1) { ctx.save(); baseT(ctx); glow(ctx, 960, 200, 900 * (1 - dk), `rgba(255,190,110,${.25 * (1 - dk)})`); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P248: gök: Zeus'un kanatlı köpeği: kartal gölgesi göğe yayılır ---
shot(PA('P248'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { ...CAMS.gok, x: 1000 + lt * 6 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'safak', clouds: 4 });
  ctx.save(); cam(ctx, c, .3);
  const g = E.out2(ramp(t, A('I08b@kanatlı') - .3, A('I08b@gelecek') + .4));
  // keskin kenarlı, kanatları açık kartal silueti (kylix kartalıyla aynı biçim), göğe yayılır
  eagleShadow(ctx, lerp(1250, 900, g), lerp(220, 320, g), lerp(2.4, 7.3, g), { a: .62 * g, rot: -.2, blur: 3 });
  ctx.restore();
  ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(8,4,3,${.35 * g})`; ctx.fillRect(0, 0, W, H); ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P249: ÜST kamera (kartal bakışı): gökten zincirli figüre sarmal iniş; I08b@çağrılmamış'ta kısa bir pençe silueti; I08b@ziyafet'te gölge gövdeyi örter ---
shot(PA('P249'), (ctx, st) => {
  const t = st.t, lt = st.lt, tC = A('I08b@çağrılmamış'), tZ = A('I08b@ziyafet');
  const c = CAMS.ust(E.io2(clamp(lt / st.d)));
  const { wind } = kayaWorld(ctx, t, c, { sky: 'safak' });
  ctx.save(); cam(ctx, c, 1);
  promChained(ctx, t, { wind, look: -.3, pose: 'gok', pull: .3 + .3 * ramp(t, tZ, tZ + .6) });
  // gölge: ziyafet'te gövdeyi tümüyle örter
  const sh = ramp(t, tZ - 1.2, tZ + .2);
  if (sh > 0) eagleShadow(ctx, lerp(900, 1150, sh), lerp(200, 600, sh), lerp(3, 6.4, sh), { a: .66 * sh, rot: -.35, blur: 3 });
  ctx.restore();
  // pençe silueti: kameranın önünden hızla geçer
  const pk = ramp(t, tC - .1, tC + .5, E.lin);
  if (pk > 0 && pk < 1) { ctx.save(); baseT(ctx); ctx.translate(lerp(-300, 2200, pk), lerp(780, 300, pk)); ctx.rotate(-.4); ctx.fillStyle = '#050201';
    for (let k = 0; k < 4; k++) { ctx.save(); ctx.rotate((k - 1.5) * .35); ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(90, 30, 170, 150); ctx.quadraticCurveTo(110, 70, 0, 26); ctx.closePath(); ctx.fill(); ctx.restore(); }
    ctx.beginPath(); ctx.ellipse(-60, 0, 120, 60, 0, 0, TAU); ctx.fill(); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P250: açılışın eşi: kupadaki siyah figür kartal (P006), negatif geçişle kırmızı figür göğüne döner; yalnız gölgesi kayar ve I08c@bedeli'de göğüste durur ---
shot(PA('P250'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  kylixScene(ctx, t, lt, { eagle: { x: KY.chest[0], y: KY.chest[1], s: 1.25, ang: .95 - .05 * Math.sin(t * 6), angFar: .05, talon: 1, beak: .3 + .3 * Math.max(0, Math.sin(t * 7)), tilt: .3 }, head: -.55, neck: -.25, mouth: .4, dawn: 1 });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });
shot(A('I08c@ayshilosta') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('I08c@bedeli');
  const c = { ...CAMS.orta, x: 1150, y: 520, z: 1.3 + lt * .01 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'sabah' });
  ctx.save(); cam(ctx, c, 1);
  promChained(ctx, t, { wind, look: -.05, pose: 'direnis' });
  const g = E.out3(ramp(t, A('I08c@işte') - .4, tB, E.lin));
  eagleShadow(ctx, lerp(400, 1296, g), lerp(120, 535, g), lerp(2.4, 3.6, g), { a: .6, rot: lerp(-.5, -.15, g), flap: .08 * Math.sin(t * 3) * (1 - g), blur: 3 });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'negatif', dur: .8 }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P251: alttan: meydan okuyan Prometheus; söz: NE YAPARSA YAPSIN… BENİ ÖLDÜREMEZ. ---
shot(PA('P251'), (ctx, st) => {
  const t = st.t, lt = st.lt, tN = A('I08c@ne');
  const c = { ...CAMS.alt, z: 1.45 + lt * .012 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'sabah', skyChain: true });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: -.18, pose: 'direnis', expr: 'direnc', pullAdd: .25 * ramp(t, A('I08c@öldüremez'), A('I08c@öldüremez') + .5) }); ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tN = A('I08c@ne'), a = 1 - ramp(t, st.end - .6, st.end);
    if (t > tN && a > 0) { ctx.save(); ctx.globalAlpha = a; speechFlow(ctx, 'NE YAPARSA YAPSIN…', u => [lerp(920, 240, u), 250], ramp(t, tN, A('I08c@yapsın') + .4, E.lin), { font: '700 58px Cinzel', follow: 0 });
      speechFlow(ctx, 'BENİ ÖLDÜREMEZ.', u => [lerp(920, 320, u), 340], ramp(t, A('I08c@beni'), A('I08c@öldüremez') + .5, E.lin), { font: '700 64px Cinzel', follow: 0, col: '#FFC867' }); ctx.restore(); }
  } });

// --- P252–P253: Hermes perileri kovar; periler kalır, kayada Prometheus'un çevresinde sıkı sıra olur; söz: HAİNLERDEN NEFRET ETMEYİ ÖĞRENDİK. ---
shot(PA('P252'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('I09@ama'), tY = A('I09@yanında');
  const c = F_cam(t, [[PA('P252'), { x: 620, y: 600, z: 1.2 }], [tA + 1.4, { x: 1160, y: 560, z: 1.25 }]], 1.6, 3);
  const { wind } = kayaWorld(ctx, t, c, { sky: 'sabah' });
  ctx.save(); cam(ctx, c, 1);
  // periler: önce denizde; I09@kalır'dan sonra kayaya, Prometheus'un çevresine gelirler
  const mv = E.io2(ramp(t, A('I09@kalır'), tY + .3, E.lin));
  if (mv < .02) G_nymphs(ctx, t, 1, { wind });
  else [[260, 660, 1060], [420, 690, 1125], [580, 655, 1440]].forEach(([x0, y0, x1], i) => { const k = clamp(mv * 1.2 - i * .1); X_nymph(ctx, lerp(x0, x1, k), lerp(y0 + 50, 870, k), lerp(3.2, 3.9, k), t, i, { dir: x1 > 1300 ? -1 : 1, wind, head: -.04 }); });
  // Hermes: el sallayıp perileri kovar
  const wv = ramp(t, A('I09@perilere') - .2, A('I09@perilere') + .3) * (1 - ramp(t, tA, tA + .6));
  I_hermes(ctx, I_HX + 60 * mv, 868, 5.6, t, { dir: -1, point: wv * .6, shF: .4 * wv * Math.sin(t * 9), flap: .3, lean: -.05 });
  promChained(ctx, t, { wind, look: .05, pose: 'direnis' });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tH = A('I09@hainlerden'), a = 1 - ramp(t, A('I09@dururlar'), A('I09@dururlar') + .6), sea = '#EBD9B4';
    if (t > tH && a > 0) { ctx.save(); ctx.globalAlpha = a; speechFlow(ctx, 'HAİNLERDEN NEFRET', u => [lerp(800, 170, u), 128], ramp(t, tH, A('I09@nefret') + .4, E.lin), { font: '700 54px Cinzel', follow: 0, col: sea, glow: 'rgba(110,52,22,.65)' });
      speechFlow(ctx, 'ETMEYİ ÖĞRENDİK.', u => [lerp(800, 190, u), 200], ramp(t, A('I09@etmeyi'), A('I09@öğrendik') + .4, E.lin), { font: '700 54px Cinzel', follow: 0, col: sea, glow: 'rgba(110,52,22,.65)' }); ctx.restore(); }
  } });

// --- P254: gök: bulutlarda dev bir yıldırım kalkar (Zeus görünmez); fırtına başlar ---
shot(PA('P254'), (ctx, st) => {
  const t = st.t, lt = st.lt, tK = A('I10@kaba');
  const c = { x: 1250, y: -260 + lt * 6, z: 1.0 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'firtina', skyChain: true });
  ctx.save(); cam(ctx, c, 1);
  const up = E.out3(ramp(t, A('I10@zeusa') - .2, tK + 1.0));
  glow(ctx, 1500, -560, 600 * up, `rgba(230,236,255,${.25 * up})`);
  bolt(ctx, 1500, lerp(-200, -600, up), lerp(1.2, 4.4, up), -.2, '#E6ECFF', 'rgba(210,220,255,.5)');
  ctx.restore();
  if ((t * 3 | 0) % 4 === 0 && lt > 1.5 && noise1(t * 2, 5) > .2) { ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(230,236,255,.08)'; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P255–P258: F13'ün yıkılmış kadrajları: toprak sarsılır ve taşlar düşer; gök gürler, şimşek çakar; rüzgârlar girdaba döner; gök denize karışır ---
// Prometheus'un sözü (Yunanca süs) rüzgârda parçalanır ama akmaya devam eder
shot(PA('P255'), (ctx, st) => {
  const t = st.t, lt = st.lt, tG = A('I10@gerçekte'), tY = A('I10@yer');
  const c = X_shake({ x: 1300, y: 860, z: 1.25 }, t, ramp(t, tY - .2, tY + .3));
  const { wind } = kayaWorld(ctx, t, c, { sky: 'firtina' });
  ctx.save(); cam(ctx, c, 1);
  // toprak kabarır, taşlar düşer (yarılma yok)
  const hv = ramp(t, tY, tY + .5) * (1 - ramp(t, tY + 1.6, tY + 2.4));
  for (let i = 0; i < 10; i++) { const r = rng(i + 91), x0 = 1050 + r() * 900, td = tY + r() * .9; if (t < td) continue; const u = t - td, y = 400 + r() * 200 + 900 * u * u, rot = u * (3 + r() * 4);
    ctx.save(); ctx.translate(x0 + u * 60 * (r() - .5), y); ctx.rotate(rot); ctx.fillStyle = '#4A2918'; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-26, -10); ctx.lineTo(4, -24); ctx.lineTo(28, -4); ctx.lineTo(14, 20); ctx.lineTo(-20, 16); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore(); }
  ctx.strokeStyle = `rgba(201,112,63,${.7 * hv})`; ctx.lineWidth = 4; ctx.beginPath(); for (let x = 1000; x <= 2400; x += 20) { const y = 900 - hv * 40 * Math.max(0, Math.sin((x - 1000) * .008 + t * 5)); x > 1000 ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
  promChained(ctx, t, { wind, look: -.2, pose: 'direnis' });
  ctx.restore();
  if (t > tG && t < tG + .07) { ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(240,244,255,.6)'; ctx.fillRect(0, 0, W, H); lightning(ctx, 300, -50, 520, 700, 17, 7, '#F4F7FF'); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => X_stormWords(ctx, st.t, 1500, 360, 900, ramp(st.t, A('I10@artık'), A('I10@yer') + .6, E.lin), 1, .25) });
shot(PA('P256'), (ctx, st) => {
  const t = st.t, lt = st.lt, tS = A('I10@şimşekler');
  const c = X_shake({ x: 1100, y: 160, z: 1.0 }, t, Math.exp(-lt * 2.5));
  kayaWorld(ctx, t, c, { sky: 'firtina', clouds: 6 });
  // şimşek: saniyede en çok 3 çakma
  if (t > tS && ((t - tS) * 3 % 1) < .08) { ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(230,236,255,.35)'; ctx.fillRect(0, 0, W, H); lightning(ctx, 500 + ((t * 3 | 0) % 3) * 420, 40, 620 + ((t * 3 | 0) % 2) * 300, 640, (t * 3 | 0) + 5, 7, '#F4F7FF'); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => X_stormWords(ctx, st.t, 1600, 520, 1000, 1, 1, .5) });
shot(PA('P257'), (ctx, st) => {
  const t = st.t, lt = st.lt, tR = A('I10@rüzgarlar');
  const c = { x: 700, y: 260, z: .9 };
  kayaWorld(ctx, t, c, { sky: 'firtina', wind: 1 });
  // iki karşıt rüzgâr sarmalı çarpışır ve girdaba döner
  const k = E.io2(ramp(t, tR, A('I10@saldırıyor') + .4));
  ctx.save(); baseT(ctx); ctx.lineCap = 'round';
  for (const [sg, cx0] of [[1, 300], [-1, 1620]]) { const cx = lerp(cx0, 960, k * .85), cy = 440;
    for (let j = 0; j < 5; j++) { ctx.strokeStyle = `rgba(242,214,170,${.55 - j * .08})`; ctx.lineWidth = 4 - j * .5; ctx.beginPath();
      for (let a = 0; a < TAU * 1.6; a += .08) { const rr = 40 + a * 46 + j * 18, an = sg * (a + t * 2.6) + j; const x = cx + Math.cos(an) * rr, y = cy + Math.sin(an) * rr * .55; a ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); } }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => X_stormWords(ctx, st.t, 1700, 320, 1400, 1, 1, 1.4) });
shot(PA('P258'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = X_shake({ x: 900, y: 760, z: 1.0 }, t, .4);
  kayaWorld(ctx, t, c, { sky: 'firtina' });
  // deniz kuşağı yükselir, gök kuşağı iner: kadrajın kuşakları birbirine karışır
  const k = E.io3(ramp(lt, .2, st.d));
  ctx.save(); baseT(ctx);
  const col = mixCol(PC.clayR, PC.glaze, .3);
  for (let i = 0; i < 4; i++) { const y = lerp(H - 40 - i * 46, 560 + i * 24, k); runningWave(ctx, -10, W + 10, y, 40, col, t * 60 + i * 30, PC.glaze); }
  for (let i = 0; i < 3; i++) { const y = lerp(i * 40, 480 - i * 30, k); meanderSaltire(ctx, -80, W + 80, y, 38, col, PC.glaze); }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => X_stormWords(ctx, st.t, 1500, 640, 1000, 1, 1 - ramp(st.t, st.end - .4, st.end), .9) });

// --- P259–P260: fırtınanın gözünde durgun yakın plan, yüzü göğe dönük; I11@adalet'te ΘΕΜΙΣ madalyonu soluk belirir, terazisi bir an dengelenir;
//     son söz harfleri ağızdan göğe, madalyona yükselir: GÖRÜYOR MUSUN, HAKSIZ YERE NELER ÇEKİYORUM. ---
shot(PA('P259'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('I11@adalet'), tG = A('I11@görüyor');
  const c = X_shake({ ...G_YK, z: 3.2 + lt * .02 }, t, .15 * ramp(t, tG - .2, tG + .3));
  const { wind } = kayaWorld(ctx, t, c, { sky: 'firtina', wind: .12 });
  ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(10,6,5,.35)'; ctx.fillRect(0, 0, W, H); ctx.restore();
  // ΘΕΜΙΣ madalyonu: fırtına bulutlarında soluk; terazi bir an dengelenir
  const ma = ramp(t, tA - .3, tA + .8) * .75;
  if (ma > 0) G_medal(ctx, t, 300, 190, 130, 0, (c2, t2, r) => {
    const bal = Math.exp(-Math.pow((t - tA - 1.0) / .7, 2)), til = lerp(.22 * Math.sin(t * 1.3), 0, bal);
    c2.strokeStyle = PC.clayR; c2.lineWidth = 4; c2.beginPath(); c2.moveTo(0, 90); c2.lineTo(0, -60); c2.stroke();
    const e = [-1, 1].map(sg => [sg * 80 * Math.cos(til), -60 + sg * 80 * Math.sin(til)]); c2.beginPath(); c2.moveTo(...e[0]); c2.lineTo(...e[1]); c2.stroke();
    e.forEach(([x, y]) => { c2.lineWidth = 2; c2.beginPath(); c2.moveTo(x, y); c2.lineTo(x - 18, y + 34); c2.moveTo(x, y); c2.lineTo(x + 18, y + 34); c2.stroke(); c2.beginPath(); c2.arc(x, y + 34, 22, 0, PI); c2.stroke(); });
    dipinto(c2, 'ΘΕΜΙΣ', 0, -96, 22, { col: PC.clayRL });
  }, ma);
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: -.24, pose: 'direnis', expr: 'goge', p: { torso: .04 } }); ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tG = A('I11@görüyor'), f = { font: '700 48px Cinzel' };
    // satırlar ağızdan çıkar, dizilince madalyona doğru yükselip solar
    const rise = (t0) => ramp(t, t0, t0 + 2.2, E.io2), fa = 1 - ramp(t, st.end - .5, st.end);
    if (t > tG && fa > 0) { ctx.save(); ctx.globalAlpha = fa;
      const r1 = rise(A('I11@musun') + .5), r2 = rise(A('I11@çekiyorum') + .5);
      ctx.save(); ctx.globalAlpha *= 1 - .6 * r1; speechFlow(ctx, 'GÖRÜYOR MUSUN,', u => [lerp(800, 230, u), 420 - 110 * r1 - u * 40 * r1], ramp(t, tG, A('I11@musun') + .4, E.lin), f); ctx.restore();
      ctx.save(); ctx.globalAlpha *= 1 - .6 * r2; speechFlow(ctx, 'HAKSIZ YERE', u => [lerp(800, 380, u), 500 - 120 * r2], ramp(t, A('I11@haksız'), A('I11@yere') + .4, E.lin), { ...f, col: '#FFC867' });
      speechFlow(ctx, 'NELER ÇEKİYORUM.', u => [lerp(800, 240, u), 580 - 120 * r2], ramp(t, A('I11@neler'), A('I11@çekiyorum') + .5, E.lin), { ...f, col: '#FFC867' }); ctx.restore(); ctx.restore(); }
  } });

// --- P261–P262: kaya ilk ve tek kez yarılır (I12@yıkılana), Prometheus ve perilerle birlikte kapanır (I12@gömülene), yazı çatlaktan parlar (I12@konuşmakta);
//     kenar şeridinde susan → konuşan panoları; I12@son'da kare sır siyahına döner, yalnız son sözün ateş renkli harfleri havada kalır ---
shot(PA('P261'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('I12@yıkılana'), tG = A('I12@gömülene'), tK = A('I12@konuşmakta'), tS = A('I12@son');
  const op = E.out3(ramp(t, tY - .1, tY + .5)) * (1 - E.in2(ramp(t, tG - .2, tG + .5))), shk = ramp(t, tY - .2, tY) * (1 - ramp(t, tG + .6, tG + 1.2)) + .25;
  const c = X_shake({ x: 1180, y: 560, z: 1.25 }, t, shk);
  const { wind } = kayaWorld(ctx, t, c, { sky: 'firtina' });
  ctx.save(); cam(ctx, c, 1);
  [[960, 1], [1040, 1], [1540, -1]].forEach(([x, dir], i) => X_nymph(ctx, x, 870, 3.9, t, i, { dir, wind, head: -.1, neck: -.05 }));
  promChained(ctx, t, { wind, look: -.25, pose: 'direnis' });
  ctx.restore();
  // yarık: ekran uzayında kayanın üstünden aşağı; açılır, sonra kapanır; kapandıktan sonra çatlaktan yazı ışığı
  // yarılma: soğuk beyaz kenar ve 0,12 sn çakma (Zeus'un yıldırımı); kapanınca çatlak sönük kalır, altın ışık yalnız I12@konuşmakta'da yazıyla gelir
  ctx.save(); baseT(ctx); X_crack(ctx, t, 220 * op, ramp(t, tY - .1, tY + .1), { col: 'rgba(230,236,255,.9)' }); ctx.restore();
  if (t > tY && t < tY + .12) { ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(240,244,255,.55)'; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  const cl = ramp(t, tG - .2, tG + .6), kk = ramp(t, tK, tK + .5);
  if (cl > 0) { ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(14,9,7,${.9 * cl})`; ctx.fillRect(0, 0, W, H); X_crack(ctx, t, 0, cl * (.35 + .65 * kk), { lw: 3 + 6 * kk, col: kk > 0 ? 'rgba(255,170,80,.95)' : 'rgba(120,90,70,.6)' }); ctx.restore(); }
  const bl = ramp(t, tS - .1, tS + .5);
  if (bl > 0) { ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(23,16,12,${bl})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tE = A('I12'), tK = A('I12@konuşmakta'), tS = A('I12@son');
    // kenar şeridi (x 1500–1880, y 60–300): SUSAN → KONUŞAN
    const pa = ramp(t, A('I12@başta') - .2, A('I12@başta') + .3) * (1 - ramp(t, tS - .3, tS + .2));
    if (pa > 0) { ctx.save(); ctx.globalAlpha = pa; ctx.fillStyle = PW.paper; ctx.fillRect(1440, 56, 450, 300); ctx.strokeStyle = PW.line; ctx.lineWidth = 3; ctx.strokeRect(1440, 56, 450, 300);
      [[1553, 'SUSAN', A('I12@başta')], [1777, 'KONUŞAN', tK]].forEach(([x, s, t0], i) => { const a = ramp(t, t0 - .1, t0 + .4); if (a <= 0) return; ctx.save(); ctx.globalAlpha *= a;
        ctx.strokeStyle = PW.line; ctx.lineWidth = 2; ctx.strokeRect(x - 100, 72, 200, 220);
        figure(ctx, { x, y: 282 - 44.5 * 2.15, s: 2.15, dir: -1, sty: STY.lek, lk: LK.promFree, seed: 17 + i, still: true, p: { torso: .05, shN: i ? 1.9 : .2, elN: .2, mouthOpen: i ? .5 : 0 } });
        if (i) for (let k = 0; k < 3; k++) { ctx.strokeStyle = PW.red; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(x - 44, 130, 12 + k * 11, PI * .8, PI * 1.2); ctx.stroke(); }
        txt(ctx, s, x, 328, { font: '700 36px Cinzel', col: i ? PW.red : PW.line, ls: 3 }); ctx.restore(); });
      erhatTag(ctx, t - tE, 'ERHAT · ÖNSÖZ · S. XV', { d: tS - tE }); ctx.restore(); }
    // I12@konuşmakta: yazı çatlaktan parlar; I12@son: havada yalnız son sözün ateş renkli harfleri
    const sp = ramp(t, tK, tK + .8, E.lin);
    if (sp > 0) speechFlow(ctx, 'SON SÖZ ONUNDUR', u => [lerp(1260, 560, u), lerp(560, 450, u)], sp, { font: '700 72px Cinzel', follow: 0, col: '#FFC867', glow: 'rgba(255,150,60,.85)' });
  } });

// --- P263: havadaki harfler sayfadaki alıntıya dönüşür; I12@özgür'de 'özgür' ateş rengiyle parlar; sonra mürekkep geri çekilir, yalnız 'özgür' yanar;
//     son 0,8 sn'de harfler kıvılcım olup fırlar ve P264'teki ok ucuna (≈ 835,383) bağlanır ---
const X_Q1 = 'Kıyamet de kopsa', X_Q2a = 'son söz ', X_Q2b = 'özgür', X_Q2c = ' düşüncenindir.';
shot(PA('P263'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  ctx.save(); cam(ctx, { x: 960 + lt * 2, y: 540, z: 1.02 + lt * .003 }, 1);
  paperBG(ctx, t, { seed: 91 });
  ctx.restore();
}, { tr: { type: 'bloom', dur: .9, end: true, cx: 960, cy: 450 }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => {
    const t = st.t, lt = st.lt, tO = A('I12@özgür'), tE = Se('I12'), end = st.end;
    const back = E.io2(ramp(t, tE + .4, tE + 1.6)), fly = ramp(t, end - .8, end, E.lin), mv = E.io3(ramp(t, tE + 1.0, end - 1.0));
    const font = 'italic 500 92px "Cormorant Garamond"';
    ctx.save(); ctx.font = font; const w1 = ctx.measureText(L(X_Q1)).width, wa = ctx.measureText(L(X_Q2a)).width, wb = ctx.measureText(L(X_Q2b)).width, wc = ctx.measureText(L(X_Q2c)).width; ctx.restore();
    const x2 = 960 - (wa + wb + wc) / 2, inkA = (1 - back) * ramp(lt, .1, .9);
    // alıntı: iki satır; mürekkep geri çekilirken 'özgür' dışında her şey solar
    txt(ctx, X_Q1, 960, 360, { font, col: PW.ink, a: inkA });
    txt(ctx, X_Q2a, x2 + wa / 2, 470, { font, col: PW.ink, a: inkA });
    txt(ctx, X_Q2c, x2 + wa + wb + wc / 2, 470, { font, col: PW.ink, a: inkA });
    txt(ctx, 'A. ERHAT · ÖNSÖZ · S. XV', 960, 580, { font: '600 40px Cinzel', col: PW.line, ls: 4, a: inkA * ramp(lt, .8, 1.4) });
    // 'özgür': I12@özgür'de ateş rengine döner; sonra ortaya gelip büyür (x 700–1220, y 380–520); sonda kıvılcım olup ok ucuna uçar
    const hot = ramp(t, tO - .1, tO + .4), bx = lerp(x2 + wa + wb / 2, 960, mv), by = lerp(470, 450, mv), sc = lerp(1, 2.3, mv);
    if (fly < 1) { ctx.save(); ctx.translate(bx, by); ctx.scale(sc, sc); ctx.globalAlpha = ramp(lt, .1, .9) * (1 - fly);
      txt(ctx, X_Q2b, 0, 0, { font, col: hot > 0 ? mixCol(PW.ink, '#FFB347', hot) : PW.ink, shadow: hot > 0 ? `rgba(255,140,50,${.9 * hot})` : null, blur: 26 * hot }); ctx.restore(); }
    if (fly > 0) { for (let i = 0; i < 26; i++) { const r = rng(i + 501), sx = bx + (r() - .5) * wb * sc, sy = by + (r() - .5) * 70, u = E.in2(clamp(fly * 1.3 - r() * .3)), x = lerp(sx, 835, u) + Math.sin(u * PI) * (r() - .5) * 160, y = lerp(sy, 383, u) - Math.sin(u * PI) * 120 * r(); sparkle(ctx, x, y, 10 + 10 * (1 - u), 1 - u * .3, '#FFE2A8'); } }
  } });
