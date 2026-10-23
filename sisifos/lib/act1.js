// I. KORİNT'İN KURNAZ KRALI
'use strict';
const flatWalk = (ctx, x, y, s, t, dir, o = {}) => walkScene(ctx, null, x, s, t, dir, { noCam: true, ground: FLAT(y), ...o });

// B1 — iki deniz arasında Efira/Korint panoraması
shot(S('B01') - .45, (ctx, st) => {
  const t = st.t, lt = st.lt, tk = Wd('B01', 'korint');
  daySky(ctx);
  const c = { x: lerp(1500, 2050, E.io2(st.p)), y: lerp(520, 560, st.p), z: lerp(.62, .82, E.io2(st.p)) };
  ctx.save(); cam(ctx, c, .25); disk(ctx, 2300, 230, 120, '#F3E2BC', 'rgba(255,230,170,.35)'); ctx.restore();
  ctx.save(); cam(ctx, c, .4);
  for (let i = 0; i < 5; i++) cloud(ctx, 600 + i * 700 + Math.sin(t * .1 + i) * 30, 220 + (i % 2) * 60, .9, 'rgba(255,230,200,.35)', null, i);
  ctx.restore();
  ctx.save(); cam(ctx, c, .7);
  ctx.fillStyle = '#7E3A1F';
  ctx.beginPath(); ctx.moveTo(-800, 900); for (let x = -800; x <= 4800; x += 40) ctx.lineTo(x, 640 + fbm1(x * .002, 11) * 120); ctx.lineTo(4800, 1400); ctx.lineTo(-800, 1400); ctx.fill();
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  // kıstak ve Akrokorint: kıyıdan yükselen düzensiz kaya kütlesi
  ctx.fillStyle = C.ink;
  const land = x => {
    if (x < 1180 || x > 2900) return 2000;
    const shore = Math.min(1, (x - 1180) / 160, (2900 - x) / 160);
    let y = 880 - 20 * shore;
    const hm = Math.exp(-Math.pow((x - 1960) / 300, 2));
    y -= 400 * Math.pow(hm, .8) + fbm1(x * .012, 3) * 16 * hm;
    return Math.min(y, 860 + (1 - shore) * 60);
  };
  ctx.beginPath(); ctx.moveTo(1150, 1400); for (let x = 1150; x <= 2930; x += 8) ctx.lineTo(x, Math.min(land(x), 1400)); ctx.lineTo(2930, 1400); ctx.fill();
  ctx.strokeStyle = C.clay; ctx.lineWidth = 2;
  for (let k = 1; k < 6; k++) { ctx.beginPath(); for (let x = 1500; x <= 2420; x += 10) { const y = land(x) + k * 34 + fbm1(x * .01, k) * 6; x === 1500 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); } ctx.stroke(); }
  temple(ctx, 1960, 492, .62, 6, C.ink, C.clay);
  sea(ctx, -1200, 1250, 840, 4, 46, t, C.ink, '#2B1A12');
  sea(ctx, 2850, 5200, 840, 4, 46, t + 3, C.ink, '#2B1A12');
  city(ctx, 1380, 880, .9, C.ink, C.clay, 3);
  city(ctx, 2560, 885, .8, C.ink, C.clay, 5);
  ship(ctx, 700 + lt * 25, 850, .9, t, C.ink, C.clay);
  ship(ctx, 3300 - lt * 20, 855, .8, t + 1, C.ink, C.clay);
  ship(ctx, 250 + lt * 18, 880, .6, t + 2, C.ink, C.clay);
  ctx.restore();
  // etiketler
  const a1 = ramp(t, Wd('B01', 'efira') - .2, Wd('B01', 'efira') + .4) * (1 - ramp(t, tk - .3, tk + .1));
  const a2 = ramp(t, tk - .1, tk + .5);
  txt(ctx, 'EFİRA', W / 2, 250, { font: '700 72px Cinzel', col: C.ink, ls: 18, a: a1 });
  txt(ctx, 'KORİNT', W / 2, 250, { font: '700 72px Cinzel', col: C.ink, ls: 18, a: a2 });
  txt(ctx, 'iki deniz arasında', W / 2, 315, { font: 'italic 500 36px "Cormorant Garamond"', col: C.ink, a: Math.max(a1, a2) * .9 });
  chapterCard(ctx, 'BÖLÜM I', "KORİNT'İN KURNAZ KRALI", lt - .2, 3.4);
}, { tr: { type: 'clay', dur: 1.0 }, post: { tex: .9, vig: .75 } });

// B2 — kral Sisifos, liman ve ticaret
shot(S('B02') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt, gy = 860;
  daySky(ctx);
  const c = { x: lerp(1000, 920, st.p), y: 540, z: 1.0 };
  ctx.save(); cam(ctx, c, .5); disk(ctx, 1500, 260, 90, '#F3E2BC', 'rgba(255,230,170,.3)'); ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  sea(ctx, 1150, 2500, gy - 10, 3, 40, t, C.ink, '#2B1A12');
  ship(ctx, 1700 - lt * 40, gy - 6, 1.1, t, C.ink, C.clay);
  ship(ctx, 2250 - lt * 26, gy + 10, .8, t + 1.5, C.ink, C.clay);
  ctx.fillStyle = C.ink; ctx.fillRect(-300, gy, 1500, 300);
  ctx.fillStyle = C.clayD; ctx.fillRect(-300, gy, 1500, 3);
  // iskele
  ctx.fillStyle = C.ink; ctx.fillRect(1100, gy - 8, 220, 12); for (let k = 0; k < 5; k++) ctx.fillRect(1110 + k * 48, gy, 8, 60);
  // amfora yığınları
  for (let i = 0; i < 6; i++) amphora(ctx, 820 + (i % 3) * 46, gy - 16 - Math.floor(i / 3) * 70, 1.0, C.ink, C.red);
  throne(ctx, 260, gy, 5.2, 1, C.ink, C.clay, { high: true });
  figure(ctx, { x: 345, y: gy - 27 * 5.2, s: 5.2, lk: LK.sisKing, hold: { F: HOLD.scepter(85) },
    p: { ...oturan(), torso: .02, head: .05, shN: .9 + Math.sin(lt * 1.3) * .08, elN: .55, shF: .55, elF: 1.1, handN: 'open', handF: 'fist', smile: .4, blink: (Math.sin(t * 1.7) > .97) ? 1 : 0 } });
  // amfora taşıyan tüccarlar (krala doğru yürür), amfora omuzda (figürün arkasında, kil kenar çizgisiyle ayrılır)
  for (const [x0, ph] of [[1180, 0], [1470, 17]]) {
    const x = x0 - lt * 70;
    if (x < 560) continue;
    const ax = x + 9 * 4.4, ay = gy - 83 * 4.4;
    ctx.save(); ctx.translate(ax, ay); ctx.rotate(1.05);
    ctx.lineWidth = 7; ctx.strokeStyle = C.clayL; ctx.save(); ctx.scale(1.25, 1.25); ctx.beginPath(); ctx.ellipse(0, -20, 26, 34, 0, 0, TAU); ctx.stroke(); ctx.restore();
    amphora(ctx, 0, 0, 1.25, C.ink, C.red); ctx.restore();
    walkScene(ctx, null, x, 4.4, t, -1, { noCam: true, ground: FLAT(gy), lk: LK.citizen, dist: lt * 70 + ph, stride: 30, lean: .14,
      p: { shF: .3, elF: .4, handN: 'fist', handF: 'open', head: .08 },
      ik: { hN: [ax - 4, ay + 10] } });
  }
  ctx.restore();
}, { tr: { type: 'fade', dur: .5 }, post: { tex: .9, vig: .75 } });

// B3 — büst yakın plan: "insanların en kurnazı"
shot(S('B03') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt, tz = Wd('B03', 'zeka');
  daySky(ctx, .4);
  ctx.save();
  const z = lerp(1, 1.05, st.p);
  ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  let J0, M0;
  figure(ctx, { x: 600, y: 1400, s: 21, lk: LK.sisKing, p: { torso: .02, neck: -.02, head: -.05 + Math.sin(lt * .8) * .02, shN: .2, elN: .3, shF: -.1, elF: .2, smile: ramp(t, tz - .2, tz + .6) * 1.3, brow: ramp(t, tz, tz + .5) * .6, blink: (lt > 1.2 && lt < 1.32) ? 1 : 0 },
    onJoints: (J, M) => { J0 = J; M0 = M; }, margin: 60 });
  // göz parıltısı
  if (J0) { const e = headPt(ctx, J0, M0, [4.6, -7.6]); sparkle(ctx, e[0], e[1], 46 * (1 - Math.abs(t - tz - .35) * 2.2), clamp(1 - Math.abs(t - tz - .35) * 2.2)); }
  ctx.restore();
  friezeFrame(ctx, { h: 44 });
  txt(ctx, 'ZEKÂ', 1400, 470, { font: '700 96px Cinzel', col: C.ink, ls: 30, a: ramp(t, tz - .1, tz + .5) });
  ctx.fillStyle = C.ink; const lw = 260 * E.out3(ramp(t, tz + .1, tz + .9)); ctx.fillRect(1400 - lw, 545, lw * 2, 4);
}, { tr: { type: 'fade', dur: .45 }, post: { tex: .9, vig: .8 } });

// B3b — Homeros ara planı: kör ozan ve alıntı
shot(Wd('B03', 'homeros') - .2, (ctx, st) => {
  const t = st.t, lt = st.lt;
  clayBG(ctx, C.clayL, C.clayD);
  friezeFrame(ctx, { h: 44 });
  const z = lerp(1, 1.04, st.p);
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  figure(ctx, { x: 470, y: 1330, s: 19, lk: { ...LK.sisOld, beard: 'long', headgear: 'wreath', robeDots: true },
    p: { torso: .02, neck: .02, head: -.12 + Math.sin(lt * .9) * .03, shN: .3, elN: .2, shF: -.1, elF: .2, blink: 1, mouthOpen: Math.max(0, Math.sin(lt * 7)) * .3 * (1 - ramp(lt, 2.2, 2.6)) }, margin: 60 });
  ctx.restore();
  txt(ctx, 'κέρδιστος ἀνδρῶν', 1300, 330, { font: 'italic 500 44px "Cormorant Garamond"', col: C.ink, a: .65 * ramp(lt, .1, .7) });
  quote(ctx, '“insanların en kurnazı”', 1300, 460, 900, t - Wd('B03', 'insanların') + .15, { font: 'italic 600 88px "Cormorant Garamond"', col: C.ink, lh: 96 });
  txt(ctx, '— HOMEROS, İLYADA VI.153', 1300, 580, { font: '600 28px Cinzel', col: C.ink, ls: 6, a: ramp(t, Wd('B03', 'der') - .3, Wd('B03', 'der') + .5) });
}, { tr: { type: 'fade', dur: .35 }, post: { tex: .9, vig: .8 } });

// B4 — gece: Autolykos ve renk değiştiren inek
shot(S('B04') - .85, (ctx, st) => {
  const t = st.t, lt = st.lt, tr = Wd('B04', 'rengini'), ts = Wd('B04', 'sisifosun');
  if (t >= ts - .1) return drawB4b(ctx, st, ts);
  nightSky(ctx);
  stars(ctx, t, 180, 9, 'rgba(255,230,190,.8)', [0, 0, W, H * .55]);
  disk(ctx, 1520, 200, 70, '#F2E3C2', 'rgba(255,235,190,.25)');
  const gy = 860;
  ctx.fillStyle = '#140A07'; ctx.fillRect(0, gy, W, H - gy); ctx.fillStyle = '#6A3220'; ctx.fillRect(0, gy, W, 3);
  // çit
  ctx.fillStyle = '#140A07'; for (let k = 60; k < 1300; k += 90) ctx.fillRect(k, gy - 90, 10, 90); ctx.fillRect(40, gy - 76, 1270, 8); ctx.fillRect(40, gy - 40, 1270, 8);
  const cows = [[190, 0], [520, .3], [850, .6]];
  for (const [cx, ph] of cows) cow(ctx, cx, gy, 2.4, 1, ph, { walk: 0, head: .25 + Math.sin(t + ph * 5) * .08, col: '#140A07', inc: '#8E4A2E' });
  // Autolykos sağdan sinsice gelir
  const ax = lerp(1750, 1260, ramp(lt, 0, 3.4, E.io2));
  const sneak = { lean: .35, neck: -.2, head: .1, stride: 40, p: { shN: .9, elN: 1.3, shF: -.4, elF: 1.4, handN: 'open', handF: 'open', brow: -.5 } };
  const gone = ramp(t, tr + 1.2, tr + 3.2, E.io2);
  // çalınan inek: renk değiştirir
  const col = t < tr ? '#140A07' : mixCol('#140A07', C.white, ramp(t, tr, tr + .8));
  const ccx = 1120 + gone * 520;
  cow(ctx, ccx, gy, 2.6, gone > 0 ? 1 : -1, gone > 0 ? lt * .7 : 0, { walk: gone > 0 ? 1 : 0, col, inc: t < tr ? '#8E4A2E' : C.ink, farCol: col });
  if (t > tr && t < tr + 1.2) for (let i = 0; i < 10; i++) sparkle(ctx, ccx - 120 + hash(i) * 240, gy - 160 + hash(i + 9) * 120, 14, clamp(1 - Math.abs(t - tr - .4 - hash(i) * .5) * 3));
  flatWalk(ctx, ax + gone * 520, gy, 4.2, t, gone > 0 ? 1 : -1, { lk: LK.autolykos, dist: lt * 50, ...sneak });
  nameTag(ctx, 'AUTOLYKOS', 'Ünlü hırsız', 120, 140, t - Wd('B04', 'otolikos') + .1, 3.0, { col: C.white });
}, { tr: { type: 'black', dur: .7 }, post: { tex: .6, vig: 1, grain: .07 } });
function drawB4b(ctx, st, ts) {
  const t = st.t, lt2 = t - ts;
  // gün-gece döngüsü ve azalan sürü
  const cyc = clamp(lt2 / 4.2) * 3;
  const night = .5 + .5 * Math.cos(cyc * TAU);
  clayBG(ctx, mixCol('#4A2117', '#E09A68', night), mixCol('#24100B', '#B85C33', night));
  const gy = 860;
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  const sunA = PI + (cyc % 1) * PI;
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, gy); ctx.clip();
  disk(ctx, W / 2 + Math.cos(sunA) * 820, 1000 + Math.sin(sunA) * 720, 70, night > .5 ? '#F3E2BC' : '#EADBBE');
  ctx.restore();
  ctx.fillStyle = C.ink; ctx.fillRect(0, gy, W, H - gy);
  const n = 6 - Math.min(3, Math.floor(cyc + .2));
  for (let i = 0; i < 6; i++) {
    const vis = i < n;
    cow(ctx, 230 + i * 250, gy, 1.9, 1, 0, { walk: 0, head: .2, col: vis ? C.ink : 'rgba(23,16,12,0)', inc: vis ? C.clay : 'rgba(0,0,0,0)', farCol: vis ? C.ink : 'rgba(0,0,0,0)' });
    if (!vis) { ctx.save(); ctx.setLineDash([10, 10]); ctx.strokeStyle = 'rgba(23,16,12,.5)'; ctx.lineWidth = 3; ctx.strokeRect(230 + i * 250 - 100, gy - 140, 200, 140); ctx.restore(); }
  }
  // Sisifos şaşkın
  const tk = Wd('B04', 'kimse');
  const a = ramp(t, tk - .5, tk);
  if (a > 0) {
    flatWalk(ctx, 1720, gy, 4.2, t, -1, { lk: LK.sisKing, dist: 0, lean: .05, head: .2, p: { shN: 1.9, elN: 2.3, shF: .1, elF: .3, handN: 'fist', brow: 1, mouthOpen: .3 }, alpha: a });
    txt(ctx, '?', 1660, 330, { font: '700 110px Cinzel', col: C.ink, a: a * (.6 + .4 * Math.sin(t * 4)) });
  }
  txt(ctx, 'GECE ' + ['I', 'II', 'III'][Math.min(2, Math.floor(cyc))], W / 2, 140, { font: '600 40px Cinzel', col: C.white, ls: 10, a: .85 * clamp((.55 - night) * 4) });
}

// B5 — toynak altına harf kazımak, sonra izlerden cümle
shot(S('B05') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt, tw = Wd('B05', 'sığırlar', 1) - .1;
  daySky(ctx);
  const gy = 880;
  if (t < tw) {
    // inek durur, Sisifos arka toynağı dizine almış, keskiyle harf kazır; yuvarlak pano içinde toynak tabanı
    ctx.fillStyle = '#9C4A27'; ctx.fillRect(0, gy, W, 50); ctx.fillStyle = C.ink; ctx.fillRect(0, gy + 50, W, H);
    const cs = 3.2, cx = 900;
    const hoofL = [-64, -30];
    cow(ctx, cx, gy, cs, 1, 0, { walk: 0, head: .15 + Math.sin(t * .7) * .05, col: C.ink, inc: C.clay, legOverride: { 3: hoofL }, tailWag: Math.sin(t * 2) * .3 });
    const hoofW = [cx + hoofL[0] * cs, gy + hoofL[1] * cs + 8];
    const hit = Math.pow(Math.abs(Math.sin(lt * 5)), 3);
    figure(ctx, { x: cx - 128 * cs * .9 + 40, y: gy - 27 * 4.6, s: 4.6, lk: LK.sisKing,
      p: { ...oturan({ hipN: 1.55, knN: 1.6, hipF: 1.3, knF: 1.5 }), torso: .55, neck: .2, head: .4, handN: 'fist', handF: 'fist', smile: .9, brow: -.4 },
      ik: { hF: [hoofW[0] - 24, hoofW[1] + 6], hN: [hoofW[0] - 14 - hit * 18, hoofW[1] - 30 - hit * 20] }, hold: { N: HOLD.hammer(), F: HOLD.chisel() } });
    throne(ctx, cx - 128 * cs * .9 - 20, gy, 4.6, 1, C.ink, C.clay, { stool: false, seat: 18 });
    // tondo
    const ta = ramp(lt, .3, .9, E.outBack);
    if (ta > 0) {
      ctx.save(); ctx.translate(1470, 380); ctx.scale(ta, ta);
      ctx.fillStyle = C.clayL; ctx.beginPath(); ctx.arc(0, 0, 250, 0, TAU); ctx.fill();
      ctx.lineWidth = 10; ctx.strokeStyle = C.ink; ctx.stroke();
      ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(0, 0, 228, 0, TAU); ctx.stroke();
      ctx.save(); ctx.beginPath(); ctx.arc(0, 0, 225, 0, TAU); ctx.clip();
      ctx.fillStyle = C.ink; ctx.beginPath(); ctx.ellipse(0, 30, 190, 150, 0, 0, TAU); ctx.fill();
      ctx.fillStyle = '#4A2C1C'; ctx.beginPath(); ctx.ellipse(-82, 30, 80, 120, -.12, 0, TAU); ctx.ellipse(82, 30, 80, 120, .12, 0, TAU); ctx.fill();
      const q = ramp(lt, 1.0, 5.0, E.lin);
      const word = ['AUTO', 'LYKOS'];
      ctx.save(); ctx.beginPath(); ctx.rect(-170, -100, 340 * Math.min(1, q * 2), 140); ctx.clip();
      txt(ctx, word[0], -82, 30, { font: '700 44px Cinzel', col: '#E8C9A0', ls: 2 }); ctx.restore();
      ctx.save(); ctx.beginPath(); ctx.rect(-10, -100, 340 * Math.max(0, q * 2 - 1), 140); ctx.clip();
      txt(ctx, word[1], 82, 30, { font: '700 44px Cinzel', col: '#E8C9A0', ls: 2 }); ctx.restore();
      const kx = q < .5 ? lerp(-150, -14, q * 2) : lerp(10, 160, q * 2 - 1);
      ctx.save(); ctx.translate(kx, 10 - hit * 10); ctx.rotate(.5); ctx.fillStyle = '#2A1A10'; ctx.fillRect(-6, -150, 12, 140); ctx.fillStyle = '#BBA27A'; ctx.beginPath(); ctx.moveTo(-6, -10); ctx.lineTo(6, -10); ctx.lineTo(0, 10); ctx.fill(); ctx.restore();
      if (hit > .6) for (let i = 0; i < 5; i++) sparkle(ctx, kx + (hash(i + Math.floor(lt * 2)) - .5) * 60, 30 + (hash(i * 3) - .5) * 40, 12, .9);
      ctx.restore();
      ctx.restore();
    }
  } else {
    // geniş: inek yürür, izler cümle yazar
    const u = t - tw;
    const c = { x: lerp(700, 1220, clamp(u / 5)), y: 600, z: .9 };
    ctx.save(); cam(ctx, c, 1);
    ctx.fillStyle = '#9C4A27'; ctx.fillRect(-500, gy, 3200, 70);
    ctx.fillStyle = C.ink; ctx.fillRect(-500, gy + 70, 3200, 400);
    const words = ['BENİ', 'AUTOLYKOS', 'ÇALDI'];
    const cx = 200 + u * 260;
    // her kelime, toynak geçince damgalanır
    let wx = 300;
    for (let i = 0; i < 3; i++) {
      ctx.save(); ctx.font = '700 64px Cinzel'; const ww = ctx.measureText(words[i]).width; ctx.restore();
      const a = ramp(cx, wx + ww * .2, wx + ww * .6);
      txt(ctx, words[i], wx + ww / 2 + 2, gy + 40, { font: '700 64px Cinzel', col: 'rgba(20,8,4,.75)', ls: 6, a });
      txt(ctx, words[i], wx + ww / 2, gy + 38, { font: '700 64px Cinzel', col: '#EBCB9E', ls: 6, a });
      for (let k = 0; k < 3; k++) { const px = wx + k * ww / 3 + 20; if (cx > px) hoofPrint(ctx, px, gy + 12, 3); }
      wx += ww + 90;
    }
    cow(ctx, cx, gy, 2.6, 1, u * .9, { walk: 1, col: C.white, inc: C.ink, farCol: '#CDBFA4' });
    ctx.restore();
    const qv = ramp(t, Wd('B05', 'beni') - .1, Wd('B05', 'beni') + .6);
    txt(ctx, '“Beni Autolykos çaldı.”', W / 2, 200, { font: 'italic 600 64px "Cormorant Garamond"', col: C.ink, a: qv });
  }
}, { tr: { type: 'clay', dur: .8 }, post: { tex: .9, vig: .8 } });

// B6 — izler ahıra çıkar; sonra gökyüzü kararır
shot(S('B06') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt, tn = Wd('B06', 'ne');
  const tilt = ramp(t, tn - .2, tn + 2.4, E.io3);
  daySky(ctx);
  const gy = 880;
  const c = { x: 960, y: lerp(560, 300, tilt), z: lerp(1, .9, tilt) };
  ctx.save(); cam(ctx, c, .3);
  const dark = ramp(t, tn + .4, tn + 3.2);
  // üç sıra fırtına bulutu: kamera yukarı döndükçe kadrajı doldurur
  for (let row = 0; row < 4; row++) for (let i = 0; i < 7; i++) {
    const cx = -60 + i * 330 + (row % 2) * 165 + Math.sin(t * .3 + i + row) * 40 + (row - 1) * t * 6;
    cloud(ctx, cx, -200 + row * 170, 1.4 + row * .2, mixCol('rgba(120,60,35,.5)', 'rgba(30,14,10,.94)', dark), mixCol('rgba(0,0,0,0)', 'rgba(200,120,70,.5)', dark), i + 3 + row * 7);
  }
  // şimşek: gök gürültüsü sesiyle aynı anda (tn + 2.0)
  const tl = tn + 2.0;
  if (t > tl - .02 && t < tl + .22) lightning(ctx, 820, -60, 1120, 860, 13, 7);
  if (t > tl + .55 && t < tl + .68) lightning(ctx, 1500, -40, 1380, 600, 17, 4);
  ctx.restore();
  ctx.save(); cam(ctx, c, 1);
  ctx.fillStyle = '#9C4A27'; ctx.fillRect(-500, gy, 3000, 60); ctx.fillStyle = C.ink; ctx.fillRect(-500, gy + 60, 3000, 500);
  for (let k = 0; k < 14; k++) hoofPrint(ctx, 120 + k * 70, gy + 22 + (k % 2) * 10, 3);
  barn(ctx, 1450, gy, 1.5, C.ink, C.clay, ramp(lt, .4, 1.4));
  const caught = ramp(lt, .9, 1.4, E.outBack);
  figure(ctx, { x: 1300, y: gy - 46 * 4.4, s: 4.4, dir: -1, lk: LK.autolykos, p: { torso: -.1 * caught, head: -.1, shN: 2.6 * caught, elN: .3, shF: 2.4 * caught, elF: .4, handN: 'open', handF: 'open', mouthOpen: caught * .8, brow: 1, hipN: .1, hipF: -.1 } });
  cow(ctx, 1560, gy, 2.4, -1, 0, { walk: 0, col: C.white, inc: C.ink, farCol: '#CDBFA4', head: .1 });
  flatWalk(ctx, lerp(700, 960, ramp(lt, 0, 1.3, E.out2)), gy, 4.4, t, 1, { lk: LK.sisKing, dist: ramp(lt, 0, 1.3, E.out2) * 260, p: { shN: lerp(-.3, .55, caught), elN: lerp(.3, 2.05, caught), shF: lerp(.3, .5, caught), elF: lerp(.3, 2.15, caught), smile: 1, handN: 'fist', handF: 'fist', head: -.05 } });
  ctx.restore();
  const fl = clamp(1 - Math.abs(t - (tn + 2.04)) * 5) * (t > tn + 1.98 ? 1 : 0);
  if (fl > 0) { ctx.save(); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgba(255,236,200,${fl * .45})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
  const dk = ramp(t, tn + .2, tn + 3.2);
  if (dk > 0) { ctx.save(); ctx.fillStyle = `rgba(20,8,5,${dk * .55})`; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}, { tr: { type: 'fade', dur: .5 }, post: { tex: .9, vig: .85 } });
