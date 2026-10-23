// VI. CAMUS — beyaz zemin (modern) ve altınlaşan Tartaros
'use strict';
const WG = STY.white;
const paperBG = (ctx) => { ctx.fillStyle = C.paper; ctx.fillRect(0, 0, W, H); glow(ctx, W / 2, H * .45, 1100, 'rgba(255,250,235,.55)'); };
// G1 — zaman atlaması, 1942, Camus, kitap
shot(S('G01') - .35, (ctx, st) => {
  const t = st.t, lt = st.lt, td = Wd('G01', 'dokuz'), ta = Wd('G01', 'albert'), ts = Wd('G01', 'sisifos'), tb = Wd('G01', 'bambaşka');
  if (t < td - .3) {
    // yüzyıllar akar: kil frizden kâğıda
    const p = clamp((t - (S('G01') - .35)) / (td - .3 - (S('G01') - .35)));
    clayBG(ctx, mixCol(C.clayL, C.paper, E.io2(p)), mixCol(C.clayD, C.paperD, E.io2(p)));
    const pq = clamp((Math.floor((window.FRAME_T ?? t) * 30 + 1e-6) / 30 - (S('G01') - .35)) / (td - .3 - (S('G01') - .35)));
    const yr = Math.round(lerp(-700, 1942, E.in2(pq)) / 10) * 10;
    const lab = yr < 0 ? `MÖ ${-yr}` : `MS ${Math.max(1, yr)}`;
    ctx.save(); ctx.translate(-((lt * 900) % 1600), 0);
    for (let k = 0; k < 4; k++) { meander(ctx, k * 1600, k * 1600 + 1600, 300, 46, mixCol(C.ink, C.inkSoft, p)); tongues(ctx, k * 1600, k * 1600 + 1600, 734, 46, mixCol(C.ink, C.inkSoft, p)); }
    ctx.restore();
    // akan küçük siluetler
    for (let i = 0; i < 9; i++) { const x = ((i * 260 - lt * 900) % 2340 + 2340) % 2340 - 200; figure(ctx, { x, y: 700 - 46 * 3.4, s: 3.4, sty: p < .6 ? STY.black : WG, lk: i % 3 === 0 ? LK.sis : i % 3 === 1 ? LK.hoplite : LK.woman, alpha: .55, p: { hipN: .3, hipF: -.3, knF: .2, shN: .3, shF: -.3 } }); }
    ctx.fillStyle = mixCol('rgba(227,185,140,.92)', 'rgba(244,236,220,.92)', p); ctx.fillRect(W / 2 - 330, 450, 660, 150); ctx.strokeStyle = mixCol(C.ink, C.inkSoft, p); ctx.lineWidth = 4; ctx.strokeRect(W / 2 - 320, 460, 640, 130);
    txt(ctx, lab, W / 2, 540, { font: '700 120px Cinzel', col: mixCol(C.ink, C.inkSoft, p), ls: 10, force: true });
  } else {
    paperBG(ctx);
    const gy = 880;
    const war = 1 - ramp(t, ts - .5, ts + .3);
    // savaş: şehir silueti, uçaklar, ışıldaklar
    ctx.save(); ctx.globalAlpha = war;
    // ışıldaklar: binaların arkasından, zemin çizgisinin üstünde kırpılı
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, gy - 60); ctx.clip(); ctx.globalAlpha *= .3;
    for (const [x, a] of [[420, .4], [1500, -.3]]) { const g = ctx.createLinearGradient(x, gy, x + Math.sin(a + t * .4) * 900, -100); g.addColorStop(0, 'rgba(36,24,18,.9)'); g.addColorStop(1, 'rgba(36,24,18,0)'); ctx.strokeStyle = g; ctx.lineWidth = 70; ctx.beginPath(); ctx.moveTo(x, gy - 60); ctx.lineTo(x + Math.sin(a + t * .4) * 900, -100); ctx.stroke(); }
    ctx.restore();
    skyline(ctx, -20, W + 20, gy, '#CFC3AA', 11, 280);
    skyline(ctx, -40, W + 20, gy, '#B3A68D', 7, 190, 'rgba(236,227,208,.55)');
    for (let i = 0; i < 5; i++) plane(ctx, ((i * 430 + t * 160) % 2400) - 240, 330 + (i % 3) * 60, .8, '#6B5E4E');
    ctx.restore();
    ctx.fillStyle = C.inkSoft; ctx.fillRect(0, gy, W, 4);
    txt(ctx, '1942', W / 2, 150, { font: '700 72px "Courier Prime"', col: C.inkSoft, a: ramp(t, td - .2, td + .5) * war });
    // Camus yürür
    // sabit hızda (~330 px/sn) yürür, son 0.6 sn'de iki adımla yavaşlar, sonra düz bacaklı duruşa geçip hafifçe nefes alır
    const tw0 = ta - 2.6, tw1 = ta + .9, dd = .6 / (tw1 - tw0), uw = clamp((t - tw0) / (tw1 - tw0));
    const pw = (uw < 1 - dd ? uw : (1 - dd) + (uw - 1 + dd) - (uw - 1 + dd) ** 2 / (2 * dd)) / (1 - dd / 2);
    if (t < ts + .2) {
      const x = lerp(-220, 820, pw), sd = ramp(t, tw1 - .15, tw1 + .45, E.io2);
      walkScene(ctx, null, x, 5.4, t, 1, { noCam: true, ground: FLAT(gy), dist: x, sty: WG, lk: LK.camus, stride: 32, stand: sd, lean: sd * Math.sin(t * 1.3) * .012, hold: { F: HOLD.cig() }, p: { shN: Math.sin(x / 50) * .3 * (1 - sd), shF: 1.2, elF: 1.9, handF: 'fist', head: .02, breath: Math.sin(t * 1.6) * .8 } });
      ctx.save(); ctx.strokeStyle = 'rgba(40,30,25,.3)'; ctx.lineWidth = 2; ctx.beginPath(); for (let k = 0; k < 30; k++) { const u = k / 29; const px = x + 40 + Math.sin(u * 6 + t * 1.5) * 10 * u, py = gy - 300 - u * 160; k ? ctx.lineTo(px, py) : ctx.moveTo(px, py); } ctx.stroke(); ctx.restore();
    }
    nameTag(ctx, 'ALBERT CAMUS', '1913 – 1960 · yazar, düşünür', 140, 200, t - ta, 4.2, { col: C.inkSoft, line: C.inkSoft });
    // kitap
    const bk = ramp(t, ts - .4, ts + .4, E.outBack);
    if (bk > 0) {
      ctx.save(); ctx.translate(1180, 560); ctx.scale(bk, bk); ctx.rotate(-.04);
      const open = ramp(t, tb - .2, tb + .8, E.io2);
      ctx.fillStyle = 'rgba(0,0,0,.18)'; ctx.fillRect(-250 + 14, -330 + 18, 500, 640);
      // kapak (açılınca sola katlanır)
      ctx.fillStyle = '#FFFBF1'; ctx.fillRect(-250, -330, 500, 640);
      if (open > 0) { // iç sayfa: minik Sisifos
        ctx.strokeStyle = C.inkSoft; ctx.lineWidth = 2;
        for (let k = 0; k < 7; k++) { ctx.beginPath(); ctx.moveTo(-190, -240 + k * 36); ctx.lineTo(190 - (k === 6 ? 160 : 0), -240 + k * 36); ctx.stroke(); }
        ctx.save(); ctx.globalAlpha = open;
        const vg = groundOf(x => 230 - (x + 200) * .32);
        ctx.fillStyle = C.inkSoft; ctx.beginPath(); ctx.moveTo(-210, 260); for (let x = -210; x <= 210; x += 10) ctx.lineTo(x, vg.y(x)); ctx.lineTo(210, 260); ctx.fill();
        pushScene(ctx, null, 60, 40, 1.1, t, { noCam: true, ground: vg, dist: 60 + lt * 3, sty: WG, cutCol: '#FFFBF1' });
        ctx.restore();
      }
      ctx.save(); ctx.translate(-250, 0); ctx.scale(Math.cos(open * PI * .95), 1);
      ctx.fillStyle = '#E9DEC6'; ctx.fillRect(0, -330, 500, 640); ctx.strokeStyle = C.inkSoft; ctx.lineWidth = 6; ctx.strokeRect(14, -316, 472, 612);
      if (open < .5) { // kitap kapağı sahnenin parçasıdır: Shorts'ta (notext) da görünür
        txt(ctx, 'ALBERT CAMUS', 250, -230, { font: '600 34px Cinzel', col: C.inkSoft, ls: 6, force: true });
        txt(ctx, 'Le Mythe', 250, -120, { font: 'italic 600 70px "Cormorant Garamond"', col: '#8E2F1F', force: true });
        txt(ctx, 'de Sisyphe', 250, -50, { font: 'italic 600 70px "Cormorant Garamond"', col: '#8E2F1F', force: true });
        txt(ctx, 'Sisifos Söyleni', 250, 60, { font: '600 36px Cinzel', col: C.inkSoft, ls: 2, force: true });
        txt(ctx, '1942', 250, 250, { font: '400 40px "Courier Prime"', col: C.inkSoft, force: true });
      }
      ctx.restore();
      ctx.restore();
    }
  }
  chapterCard(ctx, 'BÖLÜM VI', 'CAMUS VE ABSÜRT', st.lt - .25, 3.4);
}, { tr: { type: 'white', dur: 1.2 }, post: { tex: .3, vig: .5, grain: .045 }, mb: 16 });

// G3 — modern hayatın döngüsü: "Bütün bunlar ne için?"
shot(S('G03') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt, tq = Wd('G03', 'bir', 1) - .1, tb = Wd('G03', 'bütün');
  paperBG(ctx);
  const gy = 820;
  ctx.fillStyle = C.inkSoft; ctx.fillRect(0, gy, W, 4);
  meander(ctx, 0, W, 120, 40, C.inkSoft); tongues(ctx, 0, W, gy + 70, 40, C.inkSoft);
  const stop = ramp(t, tq - .3, tq + .5, E.out2);
  const spd = lerp(260, 900, ramp(lt, 0, tq - S('G03'), E.in2)) * (1 - stop);
  // sahne kaydırma: integral yaklaşık
  const tt = Math.min(t, tq + .5) - (S('G03') - .3);
  const scroll = 260 * tt + (900 - 260) * Math.pow(Math.min(tt, tq - S('G03')) , 3) / (3 * Math.pow(tq - S('G03'), 2) + 1e-6);
  const L = 2400;
  ctx.save(); ctx.beginPath(); ctx.rect(0, 164, W, gy - 164 + 66); ctx.clip();
  for (let k = -1; k < 3; k++) {
    const ox = k * L - (scroll % L);
    // ev: yatak ve saat (arka plan: soluk mürekkep)
    const BGI = '#B3A68E', WGB = { ...WG, fill: BGI, line: BGI };
    ctx.fillStyle = BGI; ctx.fillRect(ox + 120, gy - 90, 300, 14); ctx.fillRect(ox + 120, gy - 140, 12, 140); ctx.fillRect(ox + 408, gy - 76, 12, 76);
    clock(ctx, ox + 520, gy - 200, 34, t, BGI, '#FFF9EC', 1);
    ctx.fillStyle = BGI; ctx.fillRect(ox + 490, gy - 160, 60, 160);
    // sokak: lambalar
    for (const lx of [800, 1040]) { ctx.fillStyle = BGI; ctx.fillRect(ox + lx, gy - 320, 8, 320); ctx.beginPath(); ctx.arc(ox + lx + 4, gy - 326, 16, 0, TAU); ctx.fill(); }
    // ofis
    for (let i = 0; i < 3; i++) { desk(ctx, ox + 1380 + i * 260, gy, 2.1, BGI); figure(ctx, { x: ox + 1310 + i * 260, y: gy - 27 * 3.6, s: 3.6, sty: WGB, lk: LK.modern, p: { ...oturan(), torso: .2, head: .2, shN: 1.4, elN: .8, shF: 1.2, elF: .9, handN: 'fist', handF: 'fist' } }); }
    // diğer yürüyenler
    for (let i = 0; i < 2; i++) walkScene(ctx, null, ox + 760 + i * 300, 3.8, t, 1, { noCam: true, ground: FLAT(gy), dist: t * 120 + i * 30, sty: WGB, lk: LK.modern, hold: { N: HOLD.bag() }, stride: 30 });
  }
  ctx.restore();
  // kahraman: yerinde yürür, durur, yukarı bakar
  const look = ramp(t, tq, tq + .8, E.io2);
  walkScene(ctx, null, 960, 5.0, t, 1, { noCam: true, ground: FLAT(gy), dist: scroll, sty: WG, lk: LK.modern, hold: { N: HOLD.bag() }, neck: -.3 * look, head: -.45 * look, stand: look,
    p: { brow: look * .8, shN: Math.sin(scroll / 52) * .3 * (1 - look), shF: -Math.sin(scroll / 52) * .3 * (1 - look) } });
  quote(ctx, '“Bütün bunlar ne için?”', W / 2, 250, 1200, t - tb + .1, { font: 'italic 600 84px "Cormorant Garamond"', col: C.inkSoft });
}, { tr: { type: 'fade', dur: .6 }, post: { tex: .3, vig: .5, grain: .045 }, mb: 12 });

// G4 — sessiz evren, çatlak: ABSÜRT
shot(S('G04') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, tc = Wd('G04', 'çatlağa') - .2;
  const g = ctx.createLinearGradient(0, 0, 0, H); g.addColorStop(0, '#0A0B10'); g.addColorStop(1, '#1A1612'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  stars(ctx, t * .3, 420, 31, 'rgba(240,235,220,.9)', [0, 0, W, H * .85]);
  const gy = 900;
  ctx.fillStyle = '#0E0C0A'; ctx.fillRect(0, gy, W, H - gy);
  ctx.fillStyle = '#3A3128'; ctx.fillRect(0, gy, W, 2);
  glow(ctx, 470, gy - 220, 480, 'rgba(240,220,180,.16)');
  figure(ctx, { x: 470, y: gy - 46.5 * 6.2, s: 6.2, lk: LK.modern, sty: { ...STY.white, fill: '#0E0C0A', cut: '#BCA98A' }, cutCol: '#BCA98A', p: { neck: -.35, head: -.55, hipN: .05, hipF: -.05, shN: .1, shF: -.1 } });
  // çatlak: ekranı insanla gökyüzü arasında böler
  const q = ramp(t, tc, tc + 1.4, E.io2);
  if (q > 0) {
    const r = rng(77), pts = [];
    for (let i = 0; i <= 16; i++) { const u = i / 16; pts.push([lerp(600, 1500, u) + (r() - .5) * 60, lerp(H + 20, -20, u) + (r() - .5) * 30]); }
    const n = Math.max(2, Math.ceil(pts.length * q));
    ctx.save(); ctx.strokeStyle = '#F3E6C8'; ctx.shadowColor = '#FFE9B8'; ctx.shadowBlur = 30; ctx.lineWidth = 5; ctx.lineJoin = 'miter';
    ctx.beginPath(); poly(ctx, pts.slice(0, n), false); ctx.stroke(); ctx.restore();
    txtReveal(ctx, 'ABSÜRT', 1570, 440, ramp(t, tc + .5, tc + 2.0, E.lin), { font: '700 110px Cinzel', col: '#F3E6C8', ls: 30, rise: 0 });
  }
  quote(ctx, 'anlam arayan insan  ·  sessiz kalan dünya', W / 2 - 170, 160, 1400, t - Wd('G04', 'anlam') + .1, { font: 'italic 600 56px "Cormorant Garamond"', col: '#E2D6BC', shadow: 'rgba(0,0,0,.5)', blur: 10 });
}, { tr: { type: 'black', dur: .8 }, post: { tex: .2, vig: .9, grain: .06 } });

// G5 — Tartaros'a dönüş: kaya yuvarlanır, ağır ama kararlı iniş
const warmAt = t => ramp(t, S('G05'), S('G10'), E.io2);
const G5 = (() => { const t0 = S('G05') - .3, tk = Wd('G05', 'kaya') - .2, xAt = t => 1100 + (Math.min(t, tk) - t0) * 25;
  return { t0, tk, xAt, ro: rockOver(xAt(tk), 150, 4.0, tk, { pre: .36, fly: .46, hop: 36 }) }; })();
window.ROCK_OVER = Object.assign(window.ROCK_OVER || {}, { G5: G5.ro });
function drawG5(ctx, st) {
  const t = st.t, { tk, ro } = G5, ta = Wd('G05', 'ağır');
  const w = warmAt(t) * .45;
  if (t < ta - .2) {
    // tek plan: kaya kaçar, Sisifos yere kapanır, kaya sırtından aşar; doğrulur, ayağa kalkıp aşağı döner
    const xr = G5.xAt(t), rx = ro.xAt(t), fol = ramp(t, ro.td - .2, ro.td + 1.2, E.io2);
    const c = { x: lerp(900, 760, fol), y: lerp(380, 430, fol), z: lerp(.55, .6, fol) };
    for (const tb of ro.bounces) { const [bx, by] = shake(t, tb, tb === ro.td ? 9 : 4, 5); c.sx = (c.sx || 0) + bx; c.sy = (c.sy || 0) + by; }
    tartarosBG(ctx, t, c, { warm: w }); tartarosHill(ctx, c, { groove: .9, warm: w });
    ctx.save(); cam(ctx, c, 1);
    dustBurst(ctx, t, ro.tl, ro.xl, hillY(ro.xl), 12, 'rgba(110,60,35,.4)', 110, 6);
    for (const tb of ro.bounces) { const bx = ro.xAt(tb); dustBurst(ctx, t, tb, bx, hillY(bx), tb === ro.td ? 18 : 8, 'rgba(110,60,35,.36)', tb === ro.td ? 150 : 80, Math.floor(tb * 10)); }
    ctx.restore();
    const tStand = ta - 1.0, rk = t < tk ? null : ro.rockAt(t);
    if (t < tStand) {
      const pr = ro.prone(t);
      pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr, handsOff: pr, prone: pr, rise: ro.rise(t), proneX: ro.X, rock: rk, cover: ro.cover(t), bounce: ro.bounce(t), squash: ro.squash(t) });
    } else {
      if (rk) { ctx.save(); cam(ctx, c, 1); boulder(ctx, rk[0], rk[1], 150, rk[2], { shadow: false }); ctx.restore(); }
      const up = ramp(t, tStand, ta - .25, E.io2);
      walkScene(ctx, c, ro.X + 30, 4.0, t, -1, { dist: 0, neck: .3, head: .45, lean: lerp(.6, .05, up), p: { shN: .5, elN: .4, shF: .3, elF: .5, brow: .2, hipN: lerp(1.0, .05, up), knN: lerp(1.6, .05, up), hipF: lerp(.6, -.05, up), knF: lerp(1.4, .05, up) } });
    }
  } else {
    const x = lerp(G5.ro.X + 30, 640, ramp(t, ta - .2, S('G06') - .2, E.lin)), xm = (G5.ro.X + 30 + 640) / 2;
    const c = { x: xm - 40, y: hillY(xm) - 230, z: .95 }; // sabit kamera: yamaçtan aşağı inişi kadrajın içinde görürüz (yerinde yürüme etkisi yok)
    tartarosBG(ctx, t, c, { warm: w }); tartarosHill(ctx, c, { groove: .9, warm: w });
    walkScene(ctx, c, x, 4.0, t, -1, { lean: -.04, neck: .05, head: .05, stride: 26, p: { brow: 0 } });
  }
}
shot(S('G05') - .3, drawG5, { tr: { type: 'clay', dur: 1.0 }, post: TP, mb: 14 });
// "ağır ama kararlı adımlarla": ayak yakın planı (ayaklar yamaca basar), sonra iniş sürer
shot(Wd('G05', 'kararlı') - .05, (ctx, st) => {
  const t = st.t, ta = Wd('G05', 'ağır'), x = lerp(G5.ro.X + 30, 640, ramp(t, ta - .2, S('G06') - .2, E.lin));
  const w = warmAt(t) * .45, c = { x: x - 10, y: hillY(x) - 40, z: 3.4 };
  tartarosBG(ctx, t, c, { warm: w }); tartarosHill(ctx, c, { groove: .9, warm: w });
  walkScene(ctx, c, x, 4.0, t, -1, { lean: -.04, neck: .05, head: .05, stride: 26, p: { brow: 0 } });
}, { tr: { type: 'cut' }, post: TP });
shot(Wd('G05', 'aşağı') - .1, drawG5, { tr: { type: 'cut' }, post: TP });

// G6 — iniş: orta plan → ayaklar ("bilincin saati") → yüz ("farkındadır") → geniş: aşağıda bekleyen kaya ("kayasından daha güçlüdür")
function drawG6(ctx, t, cf, kp) {
  const t0 = S('G06') - .2, t1 = S('G07') - .2, lt = t - t0;
  const w = .3 + warmAt(t) * .5;
  const x = lerp(640, 120, clamp((t - t0) / (t1 - t0)));
  const c = cf(x);
  tartarosBG(ctx, t, c, { warm: w, diskX: x + 300, diskY: hillY(x) - 900 });
  tartarosHill(ctx, c, { groove: .9, warm: w });
  ctx.save(); cam(ctx, c, 1); const n = hillN(-470); boulder(ctx, -470 + n[0] * 150, hillY(-470) + n[1] * 150, 150, -3.1, { shadow: false }); ctx.restore();
  walkScene(ctx, c, x, 4.0, t, -1, { lean: -.02, neck: kp?.neck ?? .02, head: kp?.head ?? -.05, stride: 24, p: { breath: Math.sin(t * 1.6) * 1.4, blink: kp?.blink, brow: 0 } });
  return x;
}
shot(S('G06') - .2, (ctx, st) => drawG6(ctx, st.t, x => ({ x: x - 30, y: hillY(x) - 205, z: 2.0 })), { tr: { type: 'cut' }, post: TP }); // boydan, az baş boşluğu
// "Camus'ye göre bu, bilincin saatidir … Sisifos o an kaderinin tamamen farkındadır": göğüs planından yüze tek, yavaş itiş (atlama kesmesi yok).
// Alıntı itiş hızlanmadan söner; "farkındadır"da başını kaldırır, gözleri açılır; yüz "tam"a kadar tutulur.
shot(Wd('G06', 'kamü') - .15, (ctx, st) => {
  const t = st.t, t0 = t - st.lt, t1 = Wd('G06', 'tam', 1) - .1, tf = Wd('G06', 'farkındadır'), ts = Wd('G06', 'sisifos');
  const u = E.io2(clamp((t - t0) / (t1 - t0)));
  const kf = keyed(t, [[t0, { head: -.05, neck: .02, blink: 0 }], [ts - .2, { blink: 0 }], [ts + .3, { blink: .35 }], [tf - .3, { head: .02, neck: .04, blink: .45 }], [tf + .4, { head: -.18, neck: -.06, blink: 0 }, E.outBack]]);
  // alıntı söndükten sonra kadraj sağa kayar: sola bakan yüzün önünde boşluk kalır (baş ≈ x 1200'de biter)
  const pan = E.io2(ramp(t, ts - .3, t1));
  drawG6(ctx, t, x => ({ x: lerp(x + 60, x - 40, pan), y: hillY(x) - lerp(300, 322, u), z: lerp(3.2, 5.2, u) }), kf);
  quote(ctx, 'bilincin saati', 1400, 330, 820, t - Wd('G06', 'bilincin'), { font: 'italic 600 76px "Cormorant Garamond"', col: '#F7E2B8', shadow: 'rgba(0,0,0,.6)', blur: 14, a: 1 - ramp(t, ts - .5, ts) });
}, { tr: { type: 'cut' }, post: TP });
shot(Wd('G06', 'tam', 1) - .1, (ctx, st) => {
  const pull = E.io3(clamp(st.lt / 2.4));
  drawG6(ctx, st.t, x => ({ x: lerp(x - 40, x - 330, pull), y: lerp(hillY(x) - 250, hillY(x) - 200, pull), z: lerp(1.6, .75, pull) }));
}, { tr: { type: 'cut' }, post: TP });

// G7 — kayaya el koyar: "Kaya onundur."
shot(S('G07') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt, te = Wd('G07', 'ezemediler');
  const w = .55 + warmAt(t) * .35;
  const xr = -470, c = { x: xr - 80, y: hillY(xr) - 240, z: 1.05 };
  tartarosBG(ctx, t, c, { warm: w });
  tartarosHill(ctx, c, { groove: .9, warm: w });
  ctx.save(); cam(ctx, c, 1); const n = hillN(xr); glow(ctx, xr + n[0] * 150, hillY(xr) + n[1] * 150, 330, `rgba(255,200,110,${.25 + .25 * ramp(lt, 0, 2)})`); ctx.restore();
  const hand = ramp(lt, .3, 1.3, E.io2), tall = ramp(t, te - .4, te + .6, E.io2);
  const rc = [xr + n[0] * 150, hillY(xr) + n[1] * 150];
  ctx.save(); cam(ctx, c, 1); boulder(ctx, rc[0], rc[1], 150, -3.1, { shadow: false, light: -1.2 }); ctx.restore();
  // "Tanrılar ona bir anlam vermedi": eli kayaya oturduktan sonra ağırlığını verip kayaya yaslanır (G7b'deki itişe hazırlık)
  const lean = ramp(t, Wd('G07', 'tanrılar') - .2, Wd('G07', 'ama') - .1, E.io2);
  const xs = rc[0] - 215 + lean * 18, contact = [rc[0] + Math.cos(PI + .55) * 156, rc[1] + Math.sin(PI + .55) * 156];
  walkScene(ctx, c, xs, 4.0, t, 1, { dist: 0, lean: .04 + lean * .3 - tall * .06, neck: -.1 + lean * .12 - tall * .15, head: -.15 + lean * .1 - tall * .25,
    p: { shF: .1, elF: .3, handN: 'flat', brow: .2 - tall * .3, smile: tall * .3, breath: Math.sin(t * 1.4) * 1.0 },
    ik: { hN: [lerp(xs + 60, contact[0], hand), lerp(hillY(xs) - 100, contact[1], hand)] } });
}, { tr: { type: 'cut' }, post: TP });
// G7b — "ama onu ezemediler de": eylem üstünde kesme; omzunu verir, tüm ağırlığıyla iter, kaya yerinden oynar
shot(Wd('G07', 'ama') - .12, (ctx, st) => {
  const t = st.t, lt = st.lt, te = Wd('G07', 'ezemediler');
  const w = .6 + warmAt(t) * .35;
  // "ezeMEdiler"de: küçük geri çekiliş (hazırlık), sonra omuz darbesiyle kaya ~60 px kayar ve yerine oturur
  // 0.3 sn hazırlık (omuzlar çöker, kaya hafif geri), sonra 0.6 sn yumuşak bitişli ilerleme; ani sıçrama yok
  const tE2 = te + .18, mv = keyed(t, [[te - .3, { d: 0 }], [tE2 - .3, { d: 0 }], [tE2, { d: -8 }, E.io2], [tE2 + .6, { d: 60 }, E.out2], [tE2 + 1.4, { d: 66 }]]).d, xr = -470 + mv;
  // farklı açı (daha yakın, alçak) ve sabit kamera: kayanın yerinden oynaması kadrajda görünür
  const c = { x: -470 + 20, y: hillY(-470) - 150, z: lerp(1.85, 1.95, E.sine(clamp(lt / st.d))) };
  c.sx = noise1(t * 30, 1) * 2 * ramp(t, te - .3, te); c.sy = 0;
  tartarosBG(ctx, t, c, { warm: w }); tartarosHill(ctx, c, { groove: .9, warm: w });
  ctx.save(); cam(ctx, c, 1); dustBurst(ctx, t, te + .2, xr - 60, hillY(xr - 60), 14, 'rgba(110,60,35,.4)', 110, 9); dustBurst(ctx, t, te + .2, xr - 230, hillY(xr - 230), 10, 'rgba(110,60,35,.35)', 90, 19); ctx.restore();
  const set = lerp(.94, 1, ramp(lt, 0, .3, E.out3)); // plan, eller zaten kayadayken açılır (eylem üstünde kesme)
  pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr, strain: lerp(.4, 1.2, set) * (1 - ramp(t, te + .5, te + 1.2) * .4), hA: .62, hB: .68, reach: 15, handsOff: 1 - set,
    rockAng: -3.1 + mv / 150, jitter: ramp(t, te - .3, te + .15) * (1 - ramp(t, te + .5, te + 1.0)) * .8, T: 1.12 + ramp(t, tE2 - .3, tE2, E.io2) * .05 * (1 - ramp(t, tE2, tE2 + .3)) + ramp(t, tE2, tE2 + .35, E.out2) * .1 * (1 - ramp(t, te + .8, te + 1.6)), light: -1.2 });
}, { tr: { type: 'cut' }, post: TP });

// G8 — kitabın son sayfası
shot(S('G08') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  paperBG(ctx);
  ctx.save(); ctx.translate(W / 2, 560); ctx.rotate(-.02);
  ctx.fillStyle = 'rgba(0,0,0,.12)'; ctx.fillRect(-620 + 16, -390 + 20, 1240, 780);
  ctx.fillStyle = '#FFFBF1'; ctx.fillRect(-620, -390, 1240, 780);
  ctx.fillStyle = '#E8DCC2'; ctx.fillRect(-4, -390, 8, 780);
  ctx.strokeStyle = 'rgba(40,30,25,.55)'; ctx.lineWidth = 3;
  for (let side = 0; side < 2; side++) for (let k = 0; k < 13; k++) { const x0 = side ? 70 : -560, w = 490 - (k === 12 && side ? 300 : 0) - hash(k + side * 20) * 40; ctx.beginPath(); ctx.moveTo(x0, -320 + k * 52); ctx.lineTo(x0 + w, -320 + k * 52); ctx.stroke(); }
  const hl = ramp(lt, .6, 1.8);
  ctx.fillStyle = `rgba(231,184,94,${.45 * hl})`; ctx.fillRect(66, -320 + 11 * 52 - 22, 500 * hl, 44);
  ctx.restore();
  txt(ctx, '— son satırlar —', W / 2, 1010, { font: 'italic 500 34px "Cormorant Garamond"', col: C.inkSoft, a: ramp(lt, .4, 1.2) });
}, { tr: { type: 'white', dur: .6 }, post: { tex: .3, vig: .55, grain: .045 } });

// G9 — altın ışıkta tırmanış ve alıntı
shot(S('G09') - .25, (ctx, st) => {
  const t = st.t, lt = st.lt;
  const w = .85 + warmAt(t) * .15;
  const xr = -200 + lt * 26, c = { x: 600, y: 300, z: .55 };
  // ışık diski sağ altta: alıntı koyu gökyüzünde okunur
  tartarosBG(ctx, t, c, { warm: w, diskX: 1480, diskY: 560, diskR: 230 }); tartarosHill(ctx, c, { groove: .9, warm: w });
  pushScene(ctx, c, xr, 150, 4.0, t, { dist: xr, strain: .6 });
  motes(ctx, t, 60, 12, 'rgba(255,220,150,.8)', [0, 0, W, H], 16, 2, .6);
  quote(ctx, '“Zirvelere doğru verilen mücadelenin kendisi,\nbir insan yüreğini doldurmaya yeter.”', W / 2, 190, 1500, lt - .3, { font: 'italic 600 64px "Cormorant Garamond"', col: '#FFF0D0', lh: 80, shadow: 'rgba(40,15,5,.7)', blur: 16, stagger: .9 });
}, { tr: { type: 'fade', dur: .7 }, post: TP });

// G10 — doruk: gülümseme
shot(S('G10') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt, tm = Wd('G10', 'mutlu');
  const xr = 260 + lt * 12;
  // animatör geçişi: "mutlu"da itmeyi bir an bırakır, başını kaldırır, gözlerini yumup açar, nefesini verir; gülümseme yavaşça yayılır
  const sm = ramp(t, tm - .3, tm + 1.6, E.io2);
  // baş kaldırma, yakınlaşmanın ~%70'i bittikten sonra (≈1 sn, yumuşak bitiş); gövde dönüşü ≤3°
  const k10 = keyed(t, [[S('G10') - .3, { look: -.15, blink: 0, T: 1.13, strain: .3 }], [tm + .45, { look: -.13, T: 1.12 }],
    [tm + 1.4, { look: -.42, blink: .78, T: 1.09, strain: 0 }, E.out3], [tm + 2.2, { blink: .3 }], [tm + 3.0, { look: -.34, T: 1.1 }]]);
  const po = { dist: xr, smile: sm * 2.2, blink: k10.blink, strain: k10.strain, look: k10.look, reach: 17.5, T: k10.T, hA: 0, hB: 0, wrN: .6, wrF: .6, hIn: 3, hFrel: [0, 0], handN: 'press', handF: 'press', breath: Math.sin(t * 1.3) * 1.2 }; // avuç kayanın yan yüzüne bastırır (dirsek bükük), uzak el yakın elin arkasında: baş ve gülümseme açıkta
  const P = pushScene(ctx, null, xr, 150, 4.0, t, { ...po, dry: true });
  // "mutlu"da yüze kadar itiş: gülümseme telefonda da okunur
  const push = ramp(t, S('G10') - .25, tm + 1.6, E.io2); // 2.7 sn yumuşak itiş (ani yakınlaşma yok)
  const z = lerp(2.5, 2.7, E.sine(clamp(lt / st.d))) + push * 2.5;
  const c = { x: P.head[0] + lerp(70, 26, push), y: P.head[1] + lerp(70, -6, push), z };
  // güneş G9'daki gibi ekranın sağında kalır (paralaks .15 katmanında ekran konumundan geri hesaplanır)
  const zk = 1 + (c.z - 1) * .15, cxk = W / 2 + (c.x - W / 2) * .15, cyk = H / 2 + (c.y - H / 2) * .15;
  tartarosBG(ctx, t, c, { warm: 1, diskX: cxk + (1560 - W / 2) / zk, diskY: cyk + (330 - H / 2) / zk, diskR: 300 });
  tartarosHill(ctx, c, { groove: .9, warm: 1 });
  // avuç ile kaya arasında koyu temas çizgisi (el kayaya bastırıyor, havada değil)
  pushScene(ctx, c, xr, 150, 4.0, t, { ...po, afterRock: (g, q) => { const a0 = Math.atan2(q.hN[1] - q.cy, q.hN[0] - q.cx); g.save(); g.strokeStyle = 'rgba(25,12,6,.75)'; g.lineWidth = 1.1; g.lineCap = 'round'; g.beginPath(); g.arc(q.cx, q.cy, 150 + 1.2, a0 - .05, a0 + .05); g.stroke(); g.restore(); } });
  motes(ctx, t, 50, 33, 'rgba(255,225,160,.85)', [0, 0, W, H], 12, 2.2, .7);
  // alıntı üstte (YouTube altyazı bölgesi olan alt kısım boş kalır); sonraki geçişten önce söner
  const qa = 1 - ramp(t, S('H01') - .85, S('H01') - .5);
  ctx.save(); ctx.globalAlpha = qa * ramp(t, S('G10') - .1, S('G10') + .5);
  // alıntı sol üstte koyu gökyüzünde (sağ üstte açık renkli kaya var); zemin paneli yok
  ctx.globalAlpha = qa;
  quote(ctx, '“Sisifos’u mutlu\nhayal etmek gerekir.”', 470, 118, 900, t - S('G10') + .1, { font: 'italic 600 80px "Cormorant Garamond"', col: '#FFF3D8', lh: 86, shadow: 'rgba(30,10,4,.9)', blur: 16, stagger: .2 });
  txt(ctx, 'Il faut imaginer Sisyphe heureux.  — Albert Camus', 470, 252, { font: 'italic 600 38px "Cormorant Garamond"', col: '#FFF0D2', a: ramp(t, Se('G10') + .3, Se('G10') + 1.3), shadow: 'rgba(30,10,4,.9)', blur: 6 });
  ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .5, vig: .9, grain: .05 } });
