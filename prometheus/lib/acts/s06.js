// VI. SAVUNMA: "BİLE BİLE YAPTIM" (G01–G13b): bilinç ve özgürlük, Okeanos'un kızları, Themis'in kehaneti ve Prometheus'un rolü,
// zorbanın hastalığı, insanların kurtarılışı, ateşin anlamı ve uygarlık şeridi, "isteyerek suç işledim", bilmek ile yaşamak
'use strict';

// --- yardımcılar (G_ öneki) ---
const G_SKY = 'sabah';
// Okeanos'un kızları: dalga kuşağından yükselen kırmızı figür periler (up 0..1), soldaki denizin üstünde oturur
function G_nymphs(ctx, t, up, o = {}) {
  if (up <= 0) return;
  const sty = { ...STY.red, white: STY.red.fill };
  [[260, 660], [420, 690], [580, 655]].forEach(([x, y], i) => {
    const k = clamp(up * 1.3 - i * .15), yy = y + (1 - E.out3(k)) * 260;
    if (k <= 0) return;
    ctx.save(); ctx.globalAlpha *= k; ctx.beginPath(); ctx.rect(-500, -500, 2000, y + 20 + 500); ctx.clip();
    figure(ctx, { x, y: yy - 44.5 * 3.2 + 60, s: 3.2, dir: 1, sty, lk: { fem: true, hair: 'long', garment: 'robe', rf: true, earHidden: true }, seed: 80 + i, stripe: .4,
      p: { torso: .05 + (o.bow || 0) * .4, neck: (o.bow || 0) * .3, head: .05 + (o.bow || 0) * .25, shN: .4 + .1 * Math.sin(t * 1.3 + i), elN: .8, breath: Math.sin(t * 1.6 + i) * .5, wind: o.wind || 0 } });
    ctx.restore();
    // dalga köpüğü
    ctx.strokeStyle = 'rgba(242,214,170,.5)'; ctx.lineWidth = 3; ctx.beginPath(); for (let u = -1; u <= 1; u += .1) { const xx = x + u * 70, wy = y + 18 + Math.sin(u * 8 + t * 3 + i) * 5; u > -1 ? ctx.lineTo(xx, wy) : ctx.moveTo(xx, wy); } ctx.stroke();
  });
}
// kırmızı figür madalyon (gökte bir tondo): draw(c, t, r) tondo içi
function G_medal(ctx, t, x, y, r, rot, draw, a = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  glow(ctx, x, y, r * 1.6, 'rgba(0,0,0,.55)');
  ctx.fillStyle = PC.glaze; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
  ctx.save(); ctx.beginPath(); ctx.arc(x, y, r - 6, 0, TAU); ctx.clip(); ctx.translate(x, y); ctx.rotate(rot); draw(ctx, t, r); ctx.restore();
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke();
  ctx.lineWidth = 14; ctx.setLineDash([4, 18]); ctx.beginPath(); ctx.arc(x, y, r + 16, 0, TAU); ctx.stroke(); ctx.setLineDash([]);
  ctx.restore();
}
const G_YK = { ...CAMS.yakin, x: 1170 }; // söz anlarında yakın plan: yüz sağa kayar, sözün önünde 800 px boşluk kalır
const G_rf = (c, x, gy, s, dir, lk, p = {}, o = {}) => figure(c, { x, y: gy - 44.5 * s, s, dir, sty: o.sty || { ...STY.red, white: STY.red.fill }, lk: { ...lk, rf: true, earHidden: true }, seed: o.seed ?? ((x * 7) | 0), stripe: .4, p: { breath: Math.sin((window.FIG_T || 0) * 1.5 + x) * .5, ...p }, ...o });

// --- P148–P150: bölüm kartı; kayanın üstünde mahkeme şeridi: SAVUNMA; kenar şeridi: bilinç · özgürlük; sanık başını kaldırır ---
shot(PA('P148'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('G02@yani');
  const c = F_cam(t, [[PA('P148'), { ...CAMS.alt }], [A('G02'), { ...CAMS.genis, x: 980 }], [tY, { ...CAMS.orta, z: 1.7 }]], 1.0);
  const { wind } = kayaWorld(ctx, t, c, { sky: G_SKY });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: lerp(.1, -.18, ramp(t, tY - .2, tY + .8)), pose: t < tY ? 'sessiz' : 'direnis' }); ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, t2 = A('G02@bilinç');
    chapterCard(ctx, 'BÖLÜM VI', 'SAVUNMA: “BİLE BİLE YAPTIM”', st.lt - .15, 3.3, { y: 170 });
    F_court(ctx, t, [['SAVUNMA', 'sanık kendini savunur', A('G01@savunur') - .2]], ramp(t, A('G01'), A('G01') + .4) * (1 - ramp(t, A('G02') - .2, A('G02') + .3)));
    erhatStrip(ctx, t - t2 + .4, A('G03') - t2, 'bilinç · özgürlük', 'xi', { icon: (c, p, lt) => { const g = ramp(st.t, A('G02@yani'), A('G02@yani') + .8); for (const sx of [-50, 50]) { c.save(); c.globalAlpha = p; c.fillStyle = g > 0 ? mixCol(PW.line, '#E8A04C', g) : PW.line; c.fillRect(sx - 16, 60 - 110 * p, 32, 110 * p); c.fillRect(sx - 24, 60 - 116 * p, 48, 8); c.restore(); } } });
  } });

// --- P151–P152: sert kesme: Okeanos'un kızları dalga kuşağından yükselir; Prometheus anlatır, periler dalgaların üstünde oturup dinler ---
shot(PA('P151'), (ctx, st) => {
  const t = st.t, lt = st.lt, tP = A('G03@prometeus');
  const c = F_cam(t, [[PA('P151'), { x: 620, y: 600, z: 1.35 }], [tP, { x: 900, y: 560, z: 1.05 }]], 1.2, -6);
  const { wind } = kayaWorld(ctx, t, c, { sky: G_SKY });
  ctx.save(); cam(ctx, c, 1);
  G_nymphs(ctx, t, ramp(t, A('G03@perileri') - .3, A('G03@gelir') + .4), { wind });
  promChained(ctx, t, { wind, look: .08, pose: t > tP ? 'alay' : 'direnis', expr: 'direnc' });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P153–P157: gökte kırmızı figür hatıra madalyonu: Themis'in kehaneti, GÜÇ ↔ KURNAZLIK terazisi, Titanların sırtı ve boş tahtın gölgesi, Kronos'un batışı, rol ---
shot(PA('P153'), (ctx, st) => {
  const t = st.t, lt = st.lt, tZ = A('G03b@zafer'), tT = A('G05'), tK = A('G05@kronosu'), tE = A('G05@erhatın');
  const c = { x: 900 + lt * 4, y: 470, z: 1.0 };
  const { wind } = kayaWorld(ctx, t, { ...CAMS.genis, x: 900 + lt * 4 }, { sky: G_SKY });
  ctx.save(); baseT(ctx); ctx.fillStyle = 'rgba(14,9,7,.62)'; ctx.fillRect(0, 0, W, H); ctx.restore();
  const sc = (a, b) => ramp(t, a - .25, a + .35) * (1 - ramp(t, b - .25, b + .2));
  G_medal(ctx, t, 960, 450, 360, Math.sin(t * .3) * .04, (c, t, r) => {
    const gy = r * .62;
    c.fillStyle = PC.clayR; c.fillRect(-r, gy, 2 * r, 5);
    // 1: Themis (Toprak) genç Prometheus'a kehaneti fısıldar
    let a = sc(PA('P153'), tZ); if (a > 0) { c.save(); c.globalAlpha = a; G_rf(c, -120, gy, 4.6, 1, { fem: true, hair: 'long', garment: 'robe', headgear: 'diadem' }, { torso: .2, neck: .3, head: .3, shN: .7, elN: 1.5 }); G_rf(c, 130, gy, 4.3, -1, LK.promFree, { head: .15 });
      speechFlow(c, 'ΟΥ ΚΑΤ ΙΣΧΥΝ ΑΛΛΑ ΔΟΛΩι', u => [lerp(-60, 300, u), -250 - Math.sin(u * PI) * 40], ramp(t, A('G03b@geleceği'), A('G03b@söylemişti') + .5), { font: '600 26px Cinzel' }); c.restore(); }
    // 2: terazi: GÜÇ ↔ KURNAZLIK; kurnazlık ağır basar
    a = sc(tZ, tT); if (a > 0) { c.save(); c.globalAlpha = a; const til = lerp(.15, -.22, E.outBack(ramp(t, A('G03b@kurnazlığın'), A('G03b@kurnazlığın') + .9, E.lin)));
      c.strokeStyle = PC.clayR; c.lineWidth = 6; c.beginPath(); c.moveTo(0, gy); c.lineTo(0, -160); c.stroke(); const e = [-1, 1].map(sg => [sg * 200 * Math.cos(til), -160 + sg * 200 * Math.sin(til)]);
      c.beginPath(); c.moveTo(...e[0]); c.lineTo(...e[1]); c.stroke(); e.forEach(([x, y], i) => { c.lineWidth = 2.5; c.beginPath(); c.moveTo(x, y); c.lineTo(x - 40, y + 80); c.moveTo(x, y); c.lineTo(x + 40, y + 80); c.stroke(); c.beginPath(); c.arc(x, y + 80, 48, 0, PI); c.stroke();
        if (i === 0) { c.fillStyle = PC.clayR; c.fillRect(x - 24, y + 54, 48, 26); } else { glow(c, x, y + 66, 40, 'rgba(255,200,110,.6)'); c.fillStyle = PC.fireCore; c.beginPath(); c.arc(x, y + 66, 8, 0, TAU); c.fill(); } }); c.restore(); }
    // 3: Titanlar sırtlarını döner; Prometheus boş tahtın uzun gölgesine yürür ve gölgenin içine girer (Zeus yalnız gölge)
    a = sc(tT, tK); if (a > 0) { c.save(); c.globalAlpha = a; const w = ramp(t, A('G05@prometeus'), A('G05@geçti') + .4);
      c.fillStyle = 'rgba(14,9,7,.7)'; c.beginPath(); c.moveTo(60, gy); c.lineTo(r, gy); c.lineTo(r, -r); c.lineTo(120, -r); c.closePath(); c.fill();
      for (let i = 0; i < 3; i++) G_rf(c, -270 + i * 85, gy, 3.6, -1, { beard: 'full', hair: 'long', garment: 'short' }, { torso: .05 }, { seed: 40 + i });
      G_rf(c, lerp(-40, 170, w), gy, 4.2, 1, LK.promFree, { torso: .05 }, { seed: 17 }); c.restore(); }
    // 4: Kronos Tartaros'a batar; Prometheus fısıldar
    a = sc(tK, Se('G05') + 2); if (a > 0) { c.save(); c.globalAlpha = a; const sink = ramp(t, A('G05@tartarosa'), A('G05@gömen') + .6);
      c.save(); c.beginPath(); c.rect(-r, -r, 2 * r, r + gy); c.clip(); G_rf(c, -110, gy + sink * 380, 4.4, 1, LK.kronos, { torso: -.2 - .3 * sink, shN: -2 * sink, shF: -2.3 * sink, elN: .3, elF: .3, handN: 'open', handF: 'open' }); c.restore();
      c.fillStyle = PC.glaze; c.beginPath(); c.ellipse(-110, gy + 6, 150 * sink, 20 * sink, 0, 0, TAU); c.fill();
      G_rf(c, 170, gy, 4.2, -1, LK.promFree, { torso: .2, neck: .2, head: .15 }, { seed: 17 });
      if (t > tE) circleMark(c, 170, gy - 200, 110, 240, ramp(t, tE + .1, tE + .9), { col: '#E6A35A', w: 4 }); c.restore(); }
  }, ramp(lt, 0, .6));
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, a = ramp(st.lt, .6, 1.2) * (1 - ramp(t, A('G03b@zafer') - .3, A('G03b@zafer')));
    if (a > 0) txt(ctx, 'ΘΕΜΙΣ · Adalet', 960, 880 - 50, { font: '700 54px Cinzel', col: '#F1E4C8', ls: 6, a, shadow: 'rgba(0,0,0,.8)', blur: 14 });
    const z = ramp(t, A('G03b@zafer'), A('G03b@zafer') + .5) * (1 - ramp(t, A('G05') - .3, A('G05')));
    if (z > 0) { txt(ctx, 'GÜÇ', 760, 800, { font: '700 52px Cinzel', col: '#F1E4C8', ls: 4, a: z, shadow: 'rgba(0,0,0,.8)', blur: 12 }); txt(ctx, 'KURNAZLIK', 1180, 800, { font: '700 52px Cinzel', col: '#FFC867', ls: 4, a: z, shadow: 'rgba(0,0,0,.8)', blur: 12 }); }
    const tE = A('G05@erhatın');
    if (t > tE - .2) { K_nasil(ctx, 1650, 330, .8, -.06, .9); erhatStrip(ctx, t - tE + .1, st.end - tE - .2, '“o rol, işte buydu”', 'viii'); }
  } });

// --- P158–P159: sert kesme: bileğinden yükselen zincir bulutlara girer; bulutlar kapanır, soğuk pırıltı; boş tahtın çevresinde karanlıkta kısılan gözler ---
shot(PA('P158'), (ctx, st) => {
  const t = st.t, lt = st.lt, tZ = A('G06@zincirindeydi'), tS = A('G06@zorbalığın');
  const c = F_cam(t, [[PA('P158'), { x: 1420, y: 380, z: 1.5 }], [tZ, { x: 1520, y: -380, z: 1.25 }], [tS, { x: 1480, y: -520, z: 1.0 }]], 1.4, 0);
  const { wind } = kayaWorld(ctx, t, c, { sky: G_SKY, skyChain: true, glint: Math.exp(-Math.max(0, t - tZ - .2) * 2) * (t > tZ ? 1 : 0) });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind }); ctx.restore();
  // karanlıkta kısılan gözler (kuşku): boş tahtın çevresinde; yüz yok
  const ey = ramp(t, tS - .2, tS + .8);
  if (ey > 0) { ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(14,9,7,${.55 * ey})`; ctx.fillRect(0, 0, W, 520);
    for (let i = 0; i < 5; i++) { const x = 380 + i * 300 + Math.sin(i * 4) * 60, y = 180 + (i % 2) * 120, bl = .3 + .7 * Math.abs(Math.sin(t * 1.2 + i * 1.7)); ctx.globalAlpha = ey * (.6 + .4 * bl); ctx.fillStyle = '#E6ECFF';
      for (const dx of [-28, 28]) coldEye(ctx, x + dx, y, 20, bl); }
    ctx.restore(); }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const t0 = A('G06@zorbalığın'); const p = ramp(st.t, t0, Se('G06') + .2, E.lin); if (p > 0) speechFlow(ctx, 'ZORBALIĞIN BİR HASTALIĞI VARDIR: DOSTLARINA GÜVENMEZ', u => [lerp(150, 1770, u), 640 - Math.sin(u * PI) * 50], p, { font: '600 44px Cinzel', follow: .3 }); } });

// --- P160–P161: kırmızı figür tondo: küçük insanlar; G07@yok'ta ıslak sünger gibi bir silme geçer, G07@yeni'de yeni kil figürler; Prometheus önlerine geçip kollarını açar ---
shot(PA('P160'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('G07@yok'), tN = A('G07@yeni'), tB = A('G07@buna');
  ctx.fillStyle = '#120B08'; ctx.fillRect(0, 0, W, H);
  const z = lerp(1, 1.1, E.io2(clamp(lt / st.d)));
  ctx.save(); ctx.translate(960, 550); ctx.scale(z, z); ctx.translate(-960, -550);
  kylix(ctx, t, 960, 550, 430, -.05 + lt * .02, (c, t, r) => {
    c.fillStyle = PC.glaze; c.beginPath(); c.arc(0, 0, r, 0, TAU); c.fill();
    const gy = r * .55; c.fillStyle = PC.clayR; c.fillRect(-r, gy, 2 * r, 5);
    const wipe = lerp(-r - 200, r + 200, ramp(t, tY - .1, tY + 1.2, E.lin)), np = ramp(t, tN, tN + 1.0);
    for (let i = 0; i < 6; i++) { const x = -290 + i * 116;
      const old = x > wipe ? 1 : 0;
      if (old) G_rf(c, x, gy, 2.3, i % 2 ? -1 : 1, i % 2 ? LK.humanF : LK.human, { torso: .05 });
      else if (np > 0) { c.save(); c.globalAlpha = np * .9; G_rf(c, x, gy, 2.3, i % 2 ? -1 : 1, { hair: 'nape', garment: 'short' }, {}, { sty: { ...STY.red, fill: '#E0955E', white: '#E0955E' } }); c.restore(); }
    }
    // ıslak sünger: silme maskesi (yumuşak kenarlı koyu şerit)
    if (t > tY - .1 && t < tY + 1.3) { const g = c.createLinearGradient(wipe - 120, 0, wipe + 40, 0); g.addColorStop(0, 'rgba(14,9,7,0)'); g.addColorStop(.7, 'rgba(14,9,7,.9)'); g.addColorStop(1, 'rgba(14,9,7,0)'); c.fillStyle = g; c.fillRect(wipe - 120, -r, 160, 2 * r); }
    // Prometheus insanların önüne geçer, kollarını açar: tek kişi
    const pb = ramp(t, tB - .2, tB + .8);
    if (pb > 0) { c.save(); c.globalAlpha = pb; G_rf(c, lerp(-60, 30, pb), gy, 3.6, -1, LK.promFree, { shN: lerp(.2, 1.6, pb), elN: .15, shF: lerp(-.1, 1.4, pb), elF: .15, handN: 'open', handF: 'open' }, { seed: 17 }); c.restore(); }
  });
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .7, vig: .9, grain: .055 } });

// --- P162–P163: profil; söz: "Ölümlülere acıdım"; G07b@ama'da kamera geriye ve yukarıya, ÜST açıya (kartal bakışı) çekilir; periler kadrajdan çıkar ---
shot(PA('P162'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('G07b@ama');
  const u = E.io3(ramp(t, tA - .1, tA + 2.4, E.lin));
  const c = u > 0 ? CAMS.ust(1 - u * .7) : { ...G_YK, z: 3.3 + lt * .05 };
  const cc = u > 0 ? { ...c, x: lerp(G_YK.x, c.x, Math.min(1, u * 2)), y: lerp(G_YK.y, c.y, Math.min(1, u * 2)), z: lerp(3.3, c.z, Math.min(1, u * 1.6)) } : c;
  const { wind } = kayaWorld(ctx, t, cc, { sky: G_SKY });
  ctx.save(); cam(ctx, cc, 1); G_nymphs(ctx, t, 1 - ramp(t, tA + .4, tA + 1.6), { wind }); promChained(ctx, t, { wind, look: .05 }); ctx.restore();
  kayaFront(ctx, t, cc, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const t0 = A('G07b@ölümlülere'); const p = ramp(st.t, t0, A('G07b@acıdım') + .5, E.lin); if (p > 0) { ctx.save(); ctx.globalAlpha = 1 - ramp(st.t, A('G07b@ama') + .6, A('G07b@ama') + 1.4); speechFlow(ctx, 'ÖLÜMLÜLERE ACIDIM', u => [lerp(780, 40, u), 380 - Math.sin(u * PI) * 40], p, { font: '700 60px Cinzel' }); ctx.restore(); } } });

// küçük kanatlı Ker (ölüm ruhu): koyu gövde, kil kontür, iki kanat; a: görünürlük
// Ker (ölüm eidolonu): insanın omzunun arkasında süzülen küçük kanatlı siluet (≈ 120 px); siyah, kil kazıma, iki açık kanat
function G_ker(ctx, x, y, dir, t, a = 1) {
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  const s = 1.3, bob = Math.sin(t * 2.2) * 6, hy = y + bob;
  figure(ctx, { x, y: hy, s, dir, sty: { ...STY.black, cut: '#B85E37' }, lk: { hair: 'long', wings: 'ker' }, seed: 91, still: true, stripe: .9,
    p: { torso: .3, neck: .15, head: .1, shN: 1.1, elN: .9, shF: .7, elF: 1.0, handN: 'open', handF: 'open', wingF: (t * .7) % 1, wingSpread: .9 },
    ik: { fN: [x - dir * 10 * s, hy + 40 * s, .9], fF: [x - dir * 18 * s, hy + 36 * s, 1.1] } });
  ctx.restore();
}
// --- P164–P166: ova: her insanın arkasında küçük bir ölüm gölgesi; ışık süpürmesi gölgeleri siler; göğüslerinde soluk umut ışıkları; rezene ocağı tutuşturur ---
shot(PA('P164'), (ctx, st) => {
  const t = st.t, lt = st.lt, tO = A('G08@ölümlerini'), tI = A('G08@içlerine'), tS = A('G08@sonra'), tA = A('G08@ateşi');
  ctx.fillStyle = PC.glaze; ctx.fillRect(0, 0, W, H);
  const c = { x: 960 + lt * 6, y: 540, z: 1.0 };
  glazeBG(ctx, t, { gx: 960, gy: 900, gr: 900, stars: false, warm: 'rgba(150,62,28,.4)' });
  ctx.save(); cam(ctx, c, 1);
  const gy = 820; ctx.strokeStyle = 'rgba(201,112,63,.6)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-200, gy); ctx.lineTo(2200, gy); ctx.stroke();
  const sweep = lerp(-300, 2300, ramp(t, tO, tO + 1.6, E.lin)), lit = ramp(t, tA - .1, tA + .5);
  // ocak: rezene ile tutuşur
  if (lit > 0) { glow(ctx, 960, gy - 40, 400 * lit, `rgba(255,170,80,${.35 * lit})`); flame(ctx, 960, gy, 1.6 * lit, t, { haloR: 200 }); }
  ctx.fillStyle = PC.clayR; ctx.fillRect(920, gy - 4, 80, 10);
  const fp = ramp(t, tS - .3, tA);
  if (fp > 0 && lit < 1) fennel(ctx, lerp(1400, 1060, fp), lerp(500, gy - 70, fp), lerp(1250, 980, fp), lerp(600, gy - 20, fp), t, { col: C.ink, inc: PC.clayR, w: 10, fs: .8 });
  for (let i = 0; i < 6; i++) {
    const x = 380 + i * 230 + (i > 2 ? 120 : 0), dir = x < 960 ? 1 : -1;
    // ölüm gölgesi: arkasında küçük koyu kanatlı siluet; ışık süpürmesi geçince söner
    if (x > sweep) G_ker(ctx, x - dir * 78, gy - 250, dir, t + i);
    else if (x > sweep - 220) G_ker(ctx, x - dir * 78, gy - 250 - (sweep - x) * .4, dir, t + i, 1 - (sweep - x) / 220);
    G_rf(ctx, x, gy, 3.8, dir, i % 2 ? LK.humanF : LK.human, { torso: .05 + .1 * lit, head: -.05 + .1 * lit });
    // umut ışığı (ELPİS biçimi): göğüste küçük, soluk, soğuk
    const h = ramp(t, tI + i * .12, tI + .5 + i * .12), hy = gy - 245, hx = x + dir * 8; if (h > 0) { glow(ctx, hx, hy, 60, `rgba(205,218,235,${.4 * h})`); ctx.fillStyle = `rgba(226,234,242,${.9 * h})`; ctx.beginPath(); ctx.arc(hx, hy, 8 + Math.sin(t * 3 + i) * .8, 0, TAU); ctx.fill(); }
  }
  // ışık süpürmesi: ateşten yayılan sıcak şerit
  if (t > tO - .1 && t < tO + 1.8) { const g = ctx.createLinearGradient(sweep - 160, 0, sweep + 60, 0); g.addColorStop(0, 'rgba(255,190,110,0)'); g.addColorStop(.75, 'rgba(255,200,120,.3)'); g.addColorStop(1, 'rgba(255,190,110,0)'); ctx.fillStyle = g; ctx.fillRect(sweep - 160, 0, 220, 1100); }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P167–P168: sayfa: Erhat'ın sorusu; bir efsane rulosu sarılıp rafa kaldırılır; rezene alevi kâğıdı yakar, yanık delikten uygarlık frizi ---
shot(PA('P167'), (ctx, st) => {
  const t = st.t, lt = st.lt, tO = A('G09@ona'), tA = A('G09@ayshilos');
  // efsane rulosu: büyük açık tomar (ΜΥΘΟΣ); G09@ona'da sarılır, rafa yatar; kamera rafa kayar ("efsane olarak bırakmıştı")
  const tE = A('G09@efsane'), tB = A('G09@bırakmıştı'), op = E.out3(ramp(t, tO + .15, tO + .8)), rl = E.io2(ramp(t, tE - .1, tE + .6)), sh = E.io2(ramp(t, tE + .55, tB + .3));
  const c = { x: lerp(960, 1380, sh) + lt * 3, y: lerp(540, 600, sh), z: lerp(1.02, 1.35, sh) };
  ctx.save(); cam(ctx, c, 1);
  ctx.save(); ctx.translate(c.x - W / 2, c.y - H / 2); paperBG(ctx, t, { seed: 74 }); ctx.restore();
  // raf: üstünde yatık, sarılı eski tomarlar
  const SY = 780; ctx.strokeStyle = PW.line; ctx.lineWidth = 3;
  ctx.fillStyle = 'rgba(70,45,25,.18)'; ctx.fillRect(1160, SY, 760, 16); ctx.strokeRect(1160, SY, 760, 16);
  for (const e of [1200, 1880]) { ctx.beginPath(); ctx.moveTo(e, SY + 16); ctx.lineTo(e - 20 * Math.sign(e - 1540), SY + 70); ctx.stroke(); }
  const scrollH = (x, y, L, col = PW.paperD) => { ctx.fillStyle = col; ctx.fillRect(x - L / 2, y - 26, L, 52); ctx.strokeRect(x - L / 2, y - 26, L, 52); ctx.fillStyle = PW.paperL; for (const e of [-1, 1]) { ctx.beginPath(); ctx.ellipse(x + e * L / 2, y, 12, 26, 0, 0, TAU); ctx.fill(); ctx.stroke(); } inkPoly(ctx, [[x - 40, y - 26], [x - 40, y + 26]], 1, { col: PW.red, w: 3 }); };
  scrollH(1360, SY - 26, 330); scrollH(1700, SY - 26, 290); scrollH(1520, SY - 78, 360);
  // açık tomar → sarılır → rafa uçup yatar
  const w = lerp(900, 0, rl) * op, rx = 510, ry = 520, H2 = 214;
  if (op > 0 && sh <= 0) {
    if (w > 4) { ctx.fillStyle = PW.paperL; ctx.fillRect(rx, ry - H2, w, 2 * H2); ctx.strokeRect(rx, ry - H2, w, 2 * H2);
      ctx.save(); ctx.beginPath(); ctx.rect(rx, ry - H2, w, 2 * H2); ctx.clip();
      dipinto(ctx, 'ΜΥΘΟΣ', rx + 450, ry - 130, 64, { col: PW.red });
      for (let i = 0; i < 6; i++) scribble(ctx, rx + 60, ry - 50 + i * 40, 780, 1, 150 + i, { w: 1.8 });
      ctx.restore(); }
    ctx.fillStyle = PW.paperD; ctx.beginPath(); ctx.ellipse(rx, ry, 26, H2, 0, 0, TAU); ctx.fill(); ctx.stroke();
    if (rl < 1) { ctx.beginPath(); ctx.ellipse(rx + w, ry, 26, H2, 0, 0, TAU); ctx.fill(); ctx.stroke(); }
  } else if (sh > 0) {
    // sarılı tomar: yaydan rafa iner, dikten yataya döner
    const px = lerp(rx, 1560, sh), py = lerp(ry, SY - 130, sh) - Math.sin(sh * PI) * 120, rot = lerp(0, PI / 2, sh);
    ctx.save(); ctx.translate(px, py); ctx.rotate(rot); ctx.fillStyle = PW.paperD; ctx.fillRect(-26, -H2, 52, 2 * H2); ctx.strokeRect(-26, -H2, 52, 2 * H2);
    ctx.fillStyle = PW.paperL; for (const e of [-1, 1]) { ctx.beginPath(); ctx.ellipse(0, e * H2, 26, 12, 0, 0, TAU); ctx.fill(); ctx.stroke(); }
    inkPoly(ctx, [[-26, -30], [26, -30]], 1, { col: PW.red, w: 3 }); ctx.restore();
  }
  ctx.restore();
  // yanık delik: rezenenin alevi kâğıdı yakar, delikten sır siyahı ve frizin ilk karesi görünür (geçişin kendisi)
  const b = E.in2(ramp(t, tA - 1.1, tA + .05));
  if (b > 0) { ctx.save(); baseT(ctx); const R = 30 + 1300 * b; ctx.beginPath(); for (let k = 0; k <= 48; k++) { const a = k / 48 * TAU, rr = R * (1 + .12 * noise1(a * 3 + t, 5)); k ? ctx.lineTo(960 + Math.cos(a) * rr, 520 + Math.sin(a) * rr) : ctx.moveTo(960 + Math.cos(a) * rr, 520 + Math.sin(a) * rr); } ctx.closePath();
    ctx.fillStyle = PC.glaze; ctx.fill(); ctx.strokeStyle = 'rgba(255,170,80,.9)'; ctx.lineWidth = 8; ctx.stroke(); ctx.strokeStyle = 'rgba(70,30,10,.7)'; ctx.lineWidth = 20; ctx.stroke(); ctx.restore(); }
}, { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => { const q = A('G09@ateşi'); if (st.t > q - .2) { ctx.save(); ctx.globalAlpha = 1 - ramp(st.t, A('G09@ona') - .15, A('G09@ona') + .3); quoteCard(ctx, 'Ateşi tanrılardan çalıp insanlara vermek ne demektir?', 'A. ERHAT · ÖNSÖZ · S. XI', 960, 300, 1500, st.t - q, { font: 'italic 500 76px "Cormorant Garamond"', lh: 88 }); ctx.restore(); } } });

// --- P169: Aiskhylos aynı ruloyu uzun bir frize açar: uygarlığın tarihi (kırmızı figür şerit) ---
const G_GIFTS = [
  { w: 'G10b@yıldızları', draw: (c, t) => { const pts = [[-160, -60], [-60, -120], [40, -70], [120, -150], [180, -40], [60, 40]]; c.strokeStyle = PC.clayR; c.lineWidth = 3; c.beginPath(); pts.forEach((p, i) => i ? c.lineTo(...p) : c.moveTo(...p)); c.stroke(); pts.forEach(p => { glow(c, p[0], p[1], 26, 'rgba(255,220,160,.5)'); c.fillStyle = PC.fireCore; c.beginPath(); c.arc(p[0], p[1], 7, 0, TAU); c.fill(); }); } },
  { w: 'G10b@sayıları', draw: (c, t) => { [1, 2, 3].forEach((n, i) => { for (let k = 0; k < n; k++) { c.fillStyle = PC.clayR; c.beginPath(); c.arc(-150 + i * 150, 60 - k * 46, 16, 0, TAU); c.fill(); } }); dipinto(c, 'Ι ΙΙ ΙΙΙ Π Δ', 0, -150, 40, { col: 'rgba(201,112,63,.45)' }); } },
  { w: 'G10b@harfleri', draw: (c, t, lt) => { c.fillStyle = '#5A311D'; c.fillRect(-165, -130, 330, 250); c.strokeStyle = PC.clayR; c.lineWidth = 4; c.strokeRect(-165, -130, 330, 250); dipinto(c, 'ΑΒΓΔ', 0, -5, 76, { col: PC.clayRL, p: clamp(lt / .9) }); } },
  { w: 'G10b@hayvanları', draw: (c, t) => { cow(c, -10, 120, 2.6, 1, t * 2, { col: PC.clayR, inc: C.ink }); c.strokeStyle = PC.clayR; c.lineWidth = 6; c.beginPath(); c.moveTo(-100, 30); c.lineTo(-250, 110); c.lineTo(-280, 135); c.stroke(); } },
  { w: 'G10b@gemiyi', draw: (c, t) => { ship(c, 0, 80 + Math.sin(t * 2) * 6, 1.6, t, PC.clayR, C.ink, PC.clayRL); c.strokeStyle = 'rgba(201,112,63,.6)'; c.lineWidth = 3; for (let k = 0; k < 3; k++) { c.beginPath(); for (let x = -260; x <= 260; x += 20) { const y = 140 + k * 22 + Math.sin(x * .04 + t * 3 + k) * 6; x > -260 ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke(); } } },
  { w: 'G10b@ilacı', draw: (c, t) => { c.strokeStyle = PC.clayR; c.lineWidth = 5; for (let k = 0; k < 5; k++) { const a = -PI / 2 + (k - 2) * .3; c.beginPath(); c.moveTo(0, 140); c.quadraticCurveTo(Math.cos(a) * 80, 40, Math.cos(a) * 140, -120 + Math.abs(k - 2) * 30); c.stroke(); c.fillStyle = PC.clayR; c.beginPath(); c.ellipse(Math.cos(a) * 140, -120 + Math.abs(k - 2) * 30, 18, 34, a + PI / 2, 0, TAU); c.fill(); } } },
  { w: 'G10b@madenleri', draw: (c, t, lt) => { c.fillStyle = PC.clayR; c.beginPath(); c.moveTo(-160, 40); c.lineTo(160, 40); c.lineTo(110, 80); c.lineTo(60, 80); c.lineTo(60, 150); c.lineTo(-60, 150); c.lineTo(-60, 80); c.lineTo(-180, 70); c.closePath(); c.fill(); const s = Math.exp(-((lt % .5) * 8)); for (let k = 0; k < 8; k++) { const a = -PI / 2 + (k - 3.5) * .3; c.strokeStyle = `rgba(255,210,140,${.9 * s})`; c.lineWidth = 3; c.beginPath(); c.moveTo(0, 30); c.lineTo(Math.cos(a) * 110 * (1.2 - s), 30 + Math.sin(a) * 110 * (1.2 - s)); c.stroke(); } } },
];
function G_panel(ctx, x, y, w, h, t, lt, g, k = 1) {
  ctx.fillStyle = PC.glaze; ctx.fillRect(x - w / 2, y - h / 2, w, h); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 6; ctx.strokeRect(x - w / 2, y - h / 2, w, h);
  ctx.save(); ctx.beginPath(); ctx.rect(x - w / 2, y - h / 2, w, h); ctx.clip(); ctx.translate(x, y + 10 * k * w / 700); ctx.scale(k * w / 700, k * w / 700); g.draw(ctx, t, lt); ctx.restore();
}
shot(PA('P169'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  glazeBG(ctx, t, { gx: 960, gy: 700, gr: 900, stars: false, warm: 'rgba(140,58,26,.45)' });
  const un = E.io2(ramp(lt, 0, 2.6));
  ctx.save(); cam(ctx, { x: 960 + lt * 20, y: 520, z: 1.0 }, 1);
  // rulo: soldan sağa açılır, açıldıkça friz panoları görünür
  const x0 = 260, x1 = lerp(300, 2600, un);
  ctx.save(); ctx.beginPath(); ctx.rect(x0, 300, x1 - x0, 440); ctx.clip();
  G_GIFTS.forEach((g, i) => G_panel(ctx, 470 + i * 330, 520, 300, 300, t, lt, g, 1.3));
  ctx.restore();
  ctx.fillStyle = '#E2D3B5'; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; for (const x of [x0, x1]) { ctx.beginPath(); ctx.ellipse(x, 520, 22, 240, 0, 0, TAU); ctx.fill(); ctx.stroke(); }
  meanderSaltire(ctx, x0, x1, 300, 26, PC.clayR, PC.glaze); meanderSaltire(ctx, x0, x1, 714, 26, PC.clayR, PC.glaze);
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => erhatTag(ctx, st.lt, 'AİSKHYLOS · UYGARLIĞIN TARİHİ', { d: st.d, bg: 'rgba(238,229,209,.9)' }) });

// --- P170: karanlık mağara: karıncalar gibi minik insanlar, açık ama görmeyen gözler; G10b@gözleri'de tek bir başa ≥ 450 px kesme; G10b@prometeus'ta ışık girer ---
shot(PA('P170'), (ctx, st) => {
  const t = st.t, lt = st.lt, tG = A('G10b@gözleri'), tM = A('G10b@mağaralarda'), tP = A('G10b@prometeus');
  ctx.fillStyle = '#0A0605'; ctx.fillRect(0, 0, W, H);
  const light = ramp(t, tP - .2, tP + .8);
  if (t > tG && t < tM) {
    // tek bir baş: profil, açık ama boş göz (göz bebeği yok); baş yüksekliği ~ 13 birim × 38 ≈ 500 px
    G_bigHead(ctx, 960, 480, 38, 1, { hair: 'nape', blind: true }, { sty: { ...STY.red, fill: '#8A4724', white: '#8A4724' }, seed: 3 }, lt);
  } else {
    const c = { x: 960 + lt * 5, y: 560, z: 1.0 };
    ctx.save(); cam(ctx, c, 1);
    // mağara ağzı: kayanın içi, girişten ışık (Prometheus)
    ctx.fillStyle = '#1A100B'; ctx.beginPath(); ctx.ellipse(960, 560, 900, 420, 0, 0, TAU); ctx.fill();
    if (light > 0) { const g = ctx.createLinearGradient(1800, 300, 900, 700); g.addColorStop(0, `rgba(255,200,120,${.5 * light})`); g.addColorStop(1, 'rgba(255,200,120,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(1900, 200); ctx.lineTo(1900, 500); ctx.lineTo(700, 900); ctx.lineTo(500, 600); ctx.closePath(); ctx.fill(); }
    for (let i = 0; i < 26; i++) { const r = rng(i + 11), x = 300 + r() * 1300, y = 760 + r() * 120, ph = r() * 9, mv = Math.sin(t * .8 + ph) * 20;
      ctx.fillStyle = '#5A311D'; ctx.beginPath(); ctx.ellipse(x + mv, y, 8, 18, 0, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.arc(x + mv, y - 24, 7, 0, TAU); ctx.fill();
      ctx.fillStyle = light > 0 ? `rgba(255,220,160,${light})` : 'rgba(201,112,63,.5)'; ctx.beginPath(); ctx.arc(x + mv + 3, y - 25, 1.8 + light, 0, TAU); ctx.fill(); }
    ctx.restore();
  }
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// büyük baş: figürü boyun ucu ölçülerek çizer, başın ortası (cx, cy)'ye gelir
let G_NECK = null;
function G_bigHead(ctx, cx, cy, s, dir, lk, o = {}, lt = 0) {
  const f = (c, x, y, ss, cb) => figure(c, { x, y, s: ss, dir, sty: o.sty || { ...STY.red, white: STY.red.fill }, lk: { ...lk, rf: true, earHidden: true }, seed: o.seed || 3, still: true, p: { blink: 0, head: 0, breath: 0 }, onJoints: cb });
  if (!G_NECK) { const cv = makeCanvas(64, 64), c = cv.getContext('2d'); f(c, 0, 0, 1, (J, M) => { G_NECK = jointPt(c, M, J.neckT); }); }
  const hx = G_NECK[0] + 1.5 * dir, hy = G_NECK[1] - 5.5;
  ctx.save(); ctx.translate(cx, cy + Math.sin(lt * .9) * 4); ctx.scale(s, s); f(ctx, -hx, -hy, 1); ctx.restore();
}
// --- P171–P178: montaj: tek şerit, yedi pano, her biri kendi kelimesinde (sert kesmeler); G10b@tek'te geri çekilme: yedi pano tek frizin yan yana kareleri, başında Prometheus'un ateşi ---
shot(PA('P171'), (ctx, st) => {
  const t = st.t, lt = st.lt, tT = A('G10b@tek');
  glazeBG(ctx, t, { gx: 960, gy: 600, gr: 900, stars: false, warm: 'rgba(140,58,26,.45)' });
  let i = 0; G_GIFTS.forEach((g, k) => { if (t >= A(g.w)) i = k; });
  const back = E.io3(ramp(t, tT, tT + 1.6, E.lin));
  const PWD = 900, X = k => 960 + (k - i) * PWD;
  ctx.save();
  // geri çekilme: önce tek pano tam kare (simge ≥ %50 boy, merkez 960,470), sonra yedisi ve başlarındaki ateş tek friz
  const z = lerp(1, .255, back);
  ctx.translate(960, 470); ctx.scale(z, z); ctx.translate(-lerp(X(i), X(2.6), back), -470);
  G_GIFTS.forEach((g, k) => { const lt2 = t - A(g.w); if (back <= 0 && k !== i) return; G_panel(ctx, X(k), 470, 820, 820, t, Math.max(0, lt2), g, 1.75); });
  if (back > 0) { // başında Prometheus'un ateşi: rezene sapında
    const fx = X(-.8); ctx.globalAlpha = back; glow(ctx, fx, 380, 520, 'rgba(255,170,80,.4)'); flame(ctx, fx, 400, 4.2, t, { haloR: 300 }); ctx.fillStyle = PC.clayR; ctx.fillRect(fx - 18, 400, 36, 480); }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P179–P180: sert kesme: mahkeme şeridi; sanık başını kaldırır; büyük söz: İSTEYEREK, İSTEYEREK ---
shot(PA('P179'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('G11@bunların');
  const c = F_cam(t, [[PA('P179'), { ...CAMS.orta }], [tB, { ...G_YK, z: 3.0 }]], 1.0);
  const { wind } = kayaWorld(ctx, t, c, { sky: G_SKY });
  ctx.save(); cam(ctx, c, 1); promChained(ctx, t, { wind, look: lerp(.15, -.2, ramp(t, A('G11@etmez'), A('G11@etmez') + .8)) }); ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t;
    F_court(ctx, t, [['SANIK', 'suçunu inkâr etmez', A('G11@sanık') - .1]], ramp(t, PA('P179'), PA('P179') + .4) * (1 - ramp(t, A('G11@bunların') - .2, A('G11@bunların') + .3)));
    const i1 = A('G11@isteyerek'), i2 = A('G11@isteyerek#1');
    const p1 = ramp(t, i1 - .05, i1 + .45, E.out2), p2 = ramp(t, i2 - .05, i2 + .45, E.out2), a = 1 - ramp(t, A('G11@erhata') - .2, A('G11@erhata') + .3);
    if (p1 > 0 && a > 0) { ctx.save(); ctx.globalAlpha = a; speechFlow(ctx, 'İSTEYEREK,', u => [lerp(820, 110, u), 330], p1, { font: '700 88px Cinzel', follow: 0 }); if (p2 > 0) speechFlow(ctx, 'İSTEYEREK', u => [lerp(820, 140, u), 460], p2, { font: '700 88px Cinzel', follow: 0, col: '#FFC867' }); ctx.restore(); }
  } });

// --- P181: daktilo tutanağı: bugünkü bir sanığın ifadesi ("Ne yaptımsa bile bile yaptım"), G11@ne'ye kadar biter ---
shot(PA('P181'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  ctx.save(); cam(ctx, { x: 960, y: 540, z: 1.02 + lt * .006 }, 1);
  paperBG(ctx, t, { seed: 75, rule: true });
  typed(ctx, 'TUTANAK', 260, 200, ramp(lt, 0, .5), { font: '700 56px "Courier Prime"', align: 'left', cursor: lt < .5 });
  typed(ctx, 'Sanık ifadesinde:', 260, 300, ramp(lt, .4, 1.6), { font: '400 56px "Courier Prime"', align: 'left', cursor: lt > .4 && lt < 1.6 });
  ctx.restore();
}, { tr: { type: 'ink', dur: .5, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => {
    const t = st.t, t0 = A('G11@erhata') + .3, tN = A('G11@ne');
    typed(ctx, '“Ne yaptımsa bile bile yaptım.”', 960, 470, ramp(t, t0, tN, E.lin), { font: '700 70px "Courier Prime"' });
    txt(ctx, 'A. ERHAT · ÖNSÖZ · S. XI', 960, 580, { font: '600 40px Cinzel', col: PW.line, ls: 4, a: ramp(t, tN, tN + .6) });
  } });

// --- P182–P185: alttan gururlu duruş; perilere döner, itiraf eder; kil kenarları rüzgârda toz olup kopar; iç ses: soluk görüntüler dolar; geri adım atmaz ---
shot(PA('P182'), (ctx, st) => {
  const t = st.t, lt = st.lt, t12 = A('G12b'), tB = A('G12b@böyle'), tY = A('G13b@yani'), tYa = A('G13b@yaşamak'), tYi = A('G13b@yine');
  const still = ramp(t, tY - .1, tY + .3) * (1 - ramp(t, tYi - .1, tYi + .3));
  const c = F_cam(t, [[PA('P182'), { ...CAMS.alt }], [t12, { x: 900, y: 560, z: 1.25 }], [tB, { ...CAMS.yakin, z: 3.1 }], [tY - .6, { ...G_YK, z: 3.3 }], [tYi, { ...CAMS.orta }]], 1.0, 2);
  const wind = lerp(.6 + .3 * ramp(t, tB, tB + 1) * (1 - ramp(t, tY - .5, tY)), 0, still);
  kayaWorld(ctx, t, c, { sky: G_SKY, wind });
  if (still > 0) { ctx.save(); baseT(ctx); ctx.fillStyle = `rgba(14,9,7,${.55 * still})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  // P145'in soluk görüntüleri bu kez dolu ve ağır geri gelir (bilmek soluk, yaşamak dolu)
  const full = ramp(t, tYa - .1, tYa + .6) * (1 - ramp(t, tYi, tYi + .8));
  // bakış yönünde, yüzün önündeki boşlukta (ekran uzayı): fırtına bulutları, şimşek, kartal; tam renk ve ağır
  if (full > 0) { ctx.save(); baseT(ctx); ctx.globalAlpha = .85 * full; const dr = (t - tYa) * 14;
    for (let i = 0; i < 4; i++) cloud(ctx, 170 + i * 170 + dr, 230 + (i % 2) * 36, 1.5, '#2A170F', 'rgba(201,112,63,.75)', i + 31);
    if (Math.sin(t * 9) > .6) lightning(ctx, 520 + dr, 260, 460 + dr, 560, ((t * 4) | 0) + 7, 5, '#F2D6AA');
    eagle2(ctx, 430 - dr, 470, 2.3, 1, { ang: .5 + .5 * Math.cos(t * 2.2), angFar: .3, col: '#A85A32', wingCol: mixCol(PC.clayR, PC.glaze, .32), farCol: mixCol(PC.clayR, PC.glaze, .5), eye: '#E39A4E' }); ctx.restore(); }
  ctx.save(); cam(ctx, c, 1);
  G_nymphs(ctx, t, ramp(t, t12 - .5, t12 + .5), { wind, bow: ramp(t, A('G12b@itiraf'), A('G12b@itiraf') + .8) });
  const tN = ramp(t, A('G12b@prometeus'), A('G12b@prometeus') + .6), push = ramp(t, tYi, tYi + .5) * (1 - ramp(t, tYi + 1.2, tYi + 2.2));
  promChained(ctx, t, { wind, look: lerp(-.05, .1, tN) - .15 * ramp(t, PA('P182'), PA('P182') + .6) * (1 - tN), pullAdd: .35 * push, dust: push });
  // kil kenarları rüzgârda toz olup kopar
  const ds = ramp(t, tB + .4, tB + 1.4) * (1 - ramp(t, tY - .3, tY + .2));
  if (ds > 0) motes(ctx, t, 30, 91, 'rgba(201,112,63,.85)', [1080, 260, 420, 640], -40, 2.2, .8 * ds);
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });
