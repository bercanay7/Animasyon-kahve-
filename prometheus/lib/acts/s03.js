// III. ZEUS'UN DİNMEZ ÖFKESİ (D01–D11): İapetos'un dört oğlu ve cezaları (Hesiodos, siyah figür), Erhat'ın sorusu:
// "Titan oldukları için mi? Hayır: zekâları", akıl gücünün tekeli, önceden düşünen, üçüncü devrimin hazırlanması, üç taht
'use strict';

// --- yardımcılar (D_ öneki) ---
// TAHT nesnesi (siyah figür): üç sabit taht x 560/960/1360, taban 760; tip: ilk iki tahtın devrilme oranı; crack: üçüncünün çatlağı
function D_thrones(ctx, t, o = {}) {
  const by = 760, s = o.s || 6.2;
  ctx.fillStyle = C.ink; ctx.fillRect(-400, by, W + 800, 8);
  const tip = o.tip || [1.2, 1.2];
  [560, 960].forEach((x, i) => { ctx.save(); ctx.globalAlpha *= o.a ?? 1; throneTip(ctx, x, by, s, tip[i], { col: C.ink, inc: C.clay }); ctx.restore(); });
  ctx.save(); if (o.shake) ctx.translate(Math.sin(t * 41) * o.shake, 0);
  throne(ctx, 1360, by, s, 1, C.ink, C.clay, { high: true });
  if (o.crack) crackLine(ctx, 1360 + 18 * s, by, 22 * s * Math.min(1, o.crack), Math.min(1, o.crack), { col: o.crackCol || PC.fire, w: 3, s: 1.2 });
  if (o.crack && o.crackCol !== C.ink) glow(ctx, 1360 + 18 * s, by - 8 * s * o.crack, 50 * o.crack, `rgba(255,190,90,${.35 * Math.min(1, o.crack) * (.8 + .2 * Math.sin(t * 5))})`);
  ctx.restore();
  // adlar devrik tahtların üstündeki boşlukta, Zeus'unki arkalığın sağında (y ≤ 700: altyazı bandına düşmez)
  if (o.names !== false) ['ΟΥΡΑΝΟΣ', 'ΚΡΟΝΟΣ', 'ΖΕΥΣ'].forEach((n, i) => dipinto(ctx, n, [560, 960, 1360][i] + 20 + (i === 2 ? 80 : 0), by - 230, 54, { col: C.ink, a: o.na ?? 1 }));
}
// METOP (siyah figür): tek uzun friz, panolar arasında triglif bantları (dikey çift çizgili koyu dikdörtgenler)
function D_metope(ctx, x0, x1, y0, y1, panels) {
  ctx.fillStyle = C.clay; ctx.fillRect(x0, y0, x1 - x0, y1 - y0);
  const pw = (x1 - x0) / panels;
  for (let i = 0; i <= panels; i++) { const x = x0 + i * pw; ctx.fillStyle = C.ink; ctx.fillRect(x - 30, y0, 60, y1 - y0); ctx.strokeStyle = C.clay; ctx.lineWidth = 3; for (const dx of [-12, 12]) { ctx.beginPath(); ctx.moveTo(x + dx, y0 + 10); ctx.lineTo(x + dx, y1 - 10); ctx.stroke(); } }
  ctx.fillStyle = C.ink; ctx.fillRect(x0 - 30, y0 - 26, x1 - x0 + 60, 26); ctx.fillRect(x0 - 30, y1, x1 - x0 + 60, 16);
  return pw;
}
// Lakonya kylixi: solda göğü taşıyan Atlas, sağda sütuna bağlı Prometheus ve kartal (Arkesilas Ressamı kupasının düzeni)
function D_kylixAP(ctx, t, lt, o = {}) {
  ctx.fillStyle = '#120B08'; ctx.fillRect(-50, -50, W + 100, H + 100);
  const R = 430, cx = W / 2, cy = H / 2 + 10;
  const z = o.z || 1, fx = o.fx || 0, fy = o.fy || 0;
  ctx.save(); ctx.translate(cx, cy); ctx.scale(z, z); ctx.translate(-cx - fx, -cy - fy);
  kylix(ctx, t, cx, cy, R, (o.rot || 0) + lt * .02, (c, t, r) => {
    c.fillStyle = C.ink; c.fillRect(-r, r * .58, 2 * r, 7);
    const gy = r * .58, s = 3.4;
    // Atlas: dizleri hafif bükük, iki kolu yukarıda, omzunda gök kubbesi (yıldızlı yay); yük altında titrer
    const tr = (o.tremble || 0) * Math.sin(t * 31) * .02;
    bf(c, -200, gy, s, 1, { beard: 'full', hair: 'long', garment: 'short' }, { torso: .15 + tr, neck: .15, head: .1, shN: -2.7, elN: .5, shF: -2.6, elF: .6, handN: 'open', handF: 'open', breath: Math.sin(t * 2) * .5 },
      { ik: { fN: [-170, gy - 3 * s, 0], fF: [-240, gy - 3 * s, .1] } });
    c.save(); c.fillStyle = C.ink; c.beginPath(); c.ellipse(-205, gy - 96 * s, 150, 70, 0, PI, TAU); c.fill(); c.strokeStyle = C.clay; c.lineWidth = 2; for (let k = 0; k < 5; k++) { const a = PI + (k + .5) / 5 * PI; c.beginPath(); c.arc(-205 + Math.cos(a) * 110, gy - 96 * s + Math.sin(a) * 44, 4, 0, TAU); c.stroke(); } c.restore();
    // sütun ve bağlı Prometheus
    column(c, 230, gy, -r * .52, 30, C.ink, C.clay);
    const px = 170;
    bf(c, px, gy, s, -1, LK.prom, { torso: -.05, neck: -.1, head: o.head ?? -.1, handN: 'fist', handF: 'fist', breath: Math.sin(t * 1.7) * .6 },
      { ik: { hN: [px + 52, gy - 20 * s], hF: [px + 50, gy - 23 * s], fN: [px - 24, gy - 3 * s, 0], fF: [px + 22, gy - 3 * s, 0] } });
    c.strokeStyle = C.clay; c.lineWidth = 3; for (const yy of [gy - 21 * s, gy - 9 * s]) { c.beginPath(); c.ellipse(230, yy, 20, 5, 0, 0, TAU); c.stroke(); }
    // kartal göğse iner, kanatlarıyla örter
    const k = o.eagle ?? 1, fl = .5 + .5 * Math.cos(t * 3.2);
    eagle2(c, lerp(60, 120, k), lerp(-220, -70, k), 1.05, -1, { ang: lerp(fl, .2, k * .6), angFar: .2, col: C.ink, wingCol: C.ink, farCol: '#3A2116', line: C.clay, eye: C.clay, tilt: lerp(.2, .5, k), talon: k });
  });
  ctx.restore();
}

// --- P056: bölüm kartı; yukarıdan bakılan kylix ayağı üstünde döner; tondoda Zeus'un öfkeli gözü kısılır ---
shot(PA('P056'), (ctx, st) => {
  const t = st.t, lt = st.lt, tK = A('D01@kin');
  ctx.fillStyle = '#120B08'; ctx.fillRect(0, 0, W, H);
  const z = lerp(1.0, 1.12, E.io2(clamp(lt / st.d)));
  ctx.save(); ctx.translate(960, 560); ctx.scale(z, z); ctx.translate(-960, -560);
  kylix(ctx, t, 960, 560, 430, lt * .06, (c, t, r) => {
    // Zeus'un profil gözü (siyah figür): badem göz, ağır kaş; "kin"de kısılır
    const sq = ramp(t, tK - .2, tK + .5), bl = 1 - .55 * sq;
    c.save(); c.scale(3.2, 3.2);
    c.fillStyle = C.ink; c.beginPath(); c.moveTo(-60, 0); c.quadraticCurveTo(0, -38 * bl, 64, -4); c.quadraticCurveTo(0, 30 * bl, -60, 0); c.fill();
    c.fillStyle = C.clay; c.beginPath(); c.moveTo(-50, 0); c.quadraticCurveTo(0, -30 * bl, 54, -3); c.quadraticCurveTo(0, 22 * bl, -50, 0); c.fill();
    c.fillStyle = C.ink; c.beginPath(); c.arc(14, -2, 16 * Math.min(1, bl + .2), 0, TAU); c.fill();
    c.fillStyle = C.clay; c.beginPath(); c.arc(18, -7, 3.2, 0, TAU); c.fill();
    c.strokeStyle = C.ink; c.lineWidth = 9; c.lineCap = 'round'; c.beginPath(); c.moveTo(-58, -44 + 10 * sq); c.quadraticCurveTo(0, -66 + 14 * sq, 66, -36 + 22 * sq); c.stroke();
    c.restore();
  });
  ctx.restore();
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => chapterCard(ctx, 'BÖLÜM III', "ZEUS'UN DİNMEZ ÖFKESİ", st.lt - .15, 3.4, { y: 170 }) });

// --- P057: amforada yaşlı İapetos; dört oğul sırayla belirir, her ad söylendiğinde dipinto adı yazılır ---
shot(PA('P057'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const sons = [['ΑΤΛΑΣ', 'D02@atlas', { beard: 'full', hair: 'long', garment: 'short' }], ['ΜΕΝΟΙΤΙΟΣ', 'D02@menoitios', { beard: 'short', hair: 'nape', garment: 'short', headgear: 'helmet' }],
    ['ΠΡΟΜΗΘΕΥΣ', 'D02@prometeus#1', LK.promFree], ['ΕΠΙΜΗΘΕΥΣ', 'D02@epimeteus', LK.epimetheus]];
  amphoraFrieze(ctx, t, 600 + lt * 22, (c, x0, x1, t) => {
    const by = 610; c.fillStyle = C.ink; c.fillRect(x0, by, x1 - x0, 6);
    // İapetos tahtında (yaşlı, uzun sakal), asası
    const sa = ramp(t, A('D02@iapetosun') - .2, A('D02@iapetosun') + .5);
    c.save(); c.globalAlpha = .35 + .65 * sa; throne(c, 140, by, 5.2, 1, C.ink, C.clay, { high: true });
    bfSeat(c, 140, by, 5.2, 5.2, 1, { ...LK.kronos, old: true }, { torso: -.05, head: .05, shN: .7, elN: 1.1, shF: .2, elF: .9, breath: Math.sin(t * 1.6) * .6 }, { hold: { N: HOLD.scepter(80) } });
    c.restore();
    dipinto(c, 'ΙΑΠΕΤΟΣ', 160, 30, 50, { col: C.ink, a: sa, vertical: false });
    sons.forEach(([n, w, lk], i) => {
      const a = ramp(t, A(w) - .15, A(w) + .45), x = 520 + i * 330;
      if (a <= 0) return;
      c.save(); c.globalAlpha = a;
      bf(c, x, by + (1 - a) * 20, 5.0, -1, lk, { torso: .02, head: i === 2 ? -.05 : .02, shN: i === 0 ? -.4 : .1, elN: .3, breath: Math.sin(t * 1.5 + i) * .5 });
      c.restore();
      dipinto(c, n, x - 120, 60 + n.length * 19, 50, { col: C.ink, a, vertical: true });
    });
  });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P058–P059, P061: Lakonya kylixi: Atlas ve Prometheus; kamera Atlas'a yaklaşır, sonra kupa Prometheus tarafına döner ---
shot(PA('P058'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('D03@atlas');
  const u = E.io2(ramp(t, tA - .4, tA + 1.0));
  D_kylixAP(ctx, t, lt, { z: lerp(1, 1.75, u), fx: lerp(0, -205 - 0, u) * .9, fy: lerp(0, 10, u), tremble: u, eagle: .2 });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P060: amforada yıldırım iner; Menoitios açılan yarıktan aşağı düşer ---
shot(PA('P060'), (ctx, st) => {
  const t = st.t, lt = st.lt, tY = A('D03@yıldırımla'), tG = A('D03@gömüldü');
  amphoraFrieze(ctx, t, 5200 + lt * 18, (c, x0, x1, t) => {
    const by = 610, x = 5200, crk = ramp(t, tY + .1, tY + .6), fall = ramp(t, tY + .4, tG + .4, E.in2);
    c.fillStyle = C.ink; c.fillRect(x0, by, x - 120 - x0, 6); c.fillRect(x + 120, by, x1 - x - 120, 6);
    // yarık: zemin açılır, altı karanlık
    c.fillStyle = C.ink; c.beginPath(); c.moveTo(x - 140 * crk, by); c.lineTo(x - 30 * crk, 660); c.lineTo(x + 40 * crk, 650); c.lineTo(x + 140 * crk, by); c.closePath(); c.fill();
    c.save(); c.beginPath(); c.rect(x0, -200, x1 - x0, by + 203 + 400 * (fall > 0 ? 1 : 0)); c.clip();
    if (fall > 0) { c.beginPath(); c.rect(x0, -200, x1 - x0, by + 200); c.rect(x - 140 * crk, by - 1, 280 * crk, 400); c.clip('evenodd'); }
    bf(c, x, by + fall * 520, 5.0, -1, { beard: 'short', hair: 'nape', garment: 'short', headgear: 'helmet' }, { torso: -.2 - .6 * fall, head: -.3, shN: -1.2 - fall, elN: .3, shF: -2.2, elF: .3, handN: 'open', handF: 'open' });
    c.restore();
    const f = Math.exp(-Math.pow((t - tY) / .08, 2));
    if (t > tY - .1 && t < tY + .5) lightning(c, x + 40, -20, x + 10, by - 20, 17, 7, C.clay);
    if (f > .02) { c.save(); c.globalAlpha = .4 * f; c.fillStyle = C.clayL; c.fillRect(x0, -50, x1 - x0, 900); c.restore(); }
    dipinto(c, 'ΜΕΝΟΙΤΙΟΣ', x - 260, 230, 50, { col: C.ink, vertical: true });
  });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

shot(PA('P061'), (ctx, st) => {
  const t = st.t, lt = st.lt, tK = A('D04@karaciğeri');
  D_kylixAP(ctx, t, lt, { rot: -.15 - E.io2(clamp(lt / 1.6)) * .25, z: lerp(1.2, 1.6, E.io2(clamp(lt / st.d))), fx: 170, fy: -40, eagle: ramp(t, tK - .6, tK + .4), head: -.2 });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P062: METOP: peçeli bir kadın kucağında küçük bir küple Epimetheus'a doğru kayar; D04@armağan'da kurdele, küpün kapağı titrer ---
shot(PA('P062'), (ctx, st) => {
  const t = st.t, lt = st.lt, tA = A('D04@armağan');
  clayBG(ctx, C.clayL, C.clayD);
  const c = { x: 960 + lt * 8, y: 540, z: 1.05 };
  ctx.save(); cam(ctx, c, 1);
  D_metope(ctx, 260, 1700, 160, 860, 1);
  const by = 820, k = E.io2(ramp(lt, .1, 3.2)), px = lerp(560, 860, k);
  ctx.fillStyle = C.ink; ctx.fillRect(290, by, 1380, 6);
  let J = null, M = null;
  figure(ctx, { x: px, y: by - 44.5 * 5.4, s: 5.4, dir: 1, sty: STY.black, lk: { ...LK.pandora, robe: true, himation: true }, seed: 8, p: { torso: .02, head: .12, shN: .9, elN: 1.4, shF: .8, elF: 1.5, handN: 'open', handF: 'open', breath: Math.sin(t * 1.4) * .5 },
    onJoints: (j, m) => { J = j; M = m; } });
  // peçe: başın üstünden sırta inen koyu örtü
  const hd = jointPt(ctx, M, J.neckT); ctx.fillStyle = 'rgba(14,9,7,.92)'; ctx.beginPath(); ctx.moveTo(hd[0] + 10, hd[1] - 70); ctx.quadraticCurveTo(hd[0] - 40, hd[1] - 80, hd[0] - 60, hd[1] + 60); ctx.lineTo(hd[0] - 30, hd[1] + 70); ctx.quadraticCurveTo(hd[0] - 10, hd[1] - 20, hd[0] + 22, hd[1] - 56); ctx.fill();
  // küçük küp kucağında; armağan kurdelesi ve titreyen kapak
  const wr = jointPt(ctx, M, J.AN.wr), jx = wr[0] + 30, jy = wr[1] - 10;
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.ellipse(jx, jy, 34, 40, 0, 0, TAU); ctx.fill(); ctx.fillRect(jx - 18, jy - 52, 36, 12);
  const lid = Math.max(0, Math.sin(t * 23)) * 3 * ramp(t, tA, tA + .3);
  ctx.fillRect(jx - 22, jy - 60 - lid, 44, 8);
  const rb = ramp(t, tA - .1, tA + .4);
  if (rb > 0) { ctx.strokeStyle = C.red; ctx.lineWidth = 5; ctx.globalAlpha = rb; ctx.beginPath(); ctx.moveTo(jx - 34, jy - 10); ctx.lineTo(jx + 34, jy - 10); ctx.moveTo(jx, jy - 10); ctx.quadraticCurveTo(jx + 20, jy - 40, jx + 32, jy - 22); ctx.quadraticCurveTo(jx + 14, jy - 20, jx, jy - 10); ctx.stroke(); ctx.globalAlpha = 1; }
  bf(ctx, 1380, by, 5.4, -1, LK.epimetheus, { torso: -.05, head: .1, shN: -.6 * k, elN: .6, breath: Math.sin(t * 1.6) * .5 });
  dipinto(ctx, 'ΕΠΙΜΗΘΕΥΣ', 1560, 480, 44, { col: C.ink, vertical: true });
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P063–P063b: amforada dört kardeş, başlarının üstünde kıvılcım; kenar şeridinde Erhat'ın sorusu, D05@hayır'da TİTAN → ZEKÂ ---
shot(PA('P063'), (ctx, st) => {
  const t = st.t, lt = st.lt, tH = A('D05@hayır');
  amphoraFrieze(ctx, t, 600 + lt * 16, (c, x0, x1, t) => {
    const by = 610; c.fillStyle = C.ink; c.fillRect(x0, by, x1 - x0, 6);
    [{ beard: 'full', hair: 'long', garment: 'short' }, { beard: 'short', hair: 'nape', garment: 'short', headgear: 'helmet' }, LK.promFree, LK.epimetheus].forEach((lk, i) => {
      const x = 180 + i * 380, a = ramp(lt, .2 + i * .3, .7 + i * .3);
      c.save(); c.globalAlpha = a; bf(c, x, by, 5.0, -1, lk, { torso: .02, head: -.04, breath: Math.sin(t * 1.5 + i) * .5 }); c.restore();
      // kıvılcım: zekânın işareti, D05@hayır'dan sonra parlar
      const gl = .45 + .55 * ramp(t, tH, tH + .6), fl = .8 + .2 * Math.sin(t * 7 + i * 2);
      if (a > .5) { glow(c, x + 10, 40, 60 * gl, `rgba(255,220,150,${.45 * gl * fl})`); c.fillStyle = C.white; c.beginPath(); c.arc(x + 10, 40, 6 * gl * fl, 0, TAU); c.fill(); }
    });
  });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => {
    const t = st.t, t0 = A('D05@titan') - .4, tH = A('D05@hayır');
    if (t < t0 || t > Se('D05') + 1.2) return;
    const lt = t - t0;
    erhatStrip(ctx, lt, Se('D05') - t0 + .4, null, 'ix');
    if (lt > .4 && lt < Se('D05') - t0 + .4) {
      ctx.save(); const font = 'italic 600 62px "Cormorant Garamond"';
      penLine(ctx, 'Titan oldukları için mi?', W / 2 + 40, 135, ramp(lt, .4, 1.4), { font, col: PW.ink, force: true });
      ctx.font = font; const w = ctx.measureText('Titan oldukları için mi?').width, wt = ctx.measureText('Titan').width, xs = W / 2 + 40 - w / 2;
      strike(ctx, xs - 6, 140, xs + wt + 6, 136, ramp(t, tH, tH + .4), { w: 6, force: true });
      const z = ramp(t, tH + .3, tH + 1.1);
      if (z > 0) penLine(ctx, 'ZEKÂ', xs + wt / 2, 78, z, { font: '700 54px Cinzel', col: PW.red, force: true });
      ctx.restore();
    }
  } });

// --- P064–P065: TAHT: Zeus'un yumruğunda tek kıvılcım (tekel); başka yerde Prometheus'un başında ikinci kıvılcım; tahttan koyu duman kaynar ---
shot(PA('P064'), (ctx, st) => {
  const t = st.t, lt = st.lt, tT = A('D07@tekelindedir'), tV = A('D07@ve'), tD = A('D07@dinmez');
  clayBG(ctx, C.clayL, C.clayD);
  const pan = E.io2(ramp(t, tV - .3, tV + 1.4));
  const c = { x: lerp(1330, 980, pan), y: lerp(400, 540, pan), z: lerp(1.35, 1.0, pan) };
  ctx.save(); cam(ctx, c, 1);
  D_thrones(ctx, t, { tip: [1.2, 1.2], na: .6 });
  // tahtta Zeus (siyah figür), kapalı yumruk öne uzanır; parmak arasından ışık sızar
  let J = null, M = null;
  figure(ctx, { x: 1360 + 2.5 * 6.2, y: 760 - 25 * 6.2 - 3.2 * 6.2, s: 6.2, dir: 1, sty: STY.black, lk: LK.zeus, seed: 5, hold: { F: HOLD.scepter(80) }, onJoints: (j, m) => { J = j; M = m; },
    p: { torso: -.05, neck: .05 - .15 * ramp(t, tV, tV + .6), head: .05 - .25 * ramp(t, tV, tV + .6), shN: -1.35, elN: .25, handN: 'fist', shF: .4, elF: 1.0, breath: Math.sin(t * 1.3) * .5 }, ik: { fN: [1360 + 25 * 6.2, 760 - 5 * 6.2 - 2.6 * 6.2, 0], fF: [1360 + 21 * 6.2, 760 - 5 * 6.2 - 2.6 * 6.2, .05] } }); // oturuş: kalça oturakta, ayaklar taburede
  const fs = jointPt(ctx, M, J.AN.wr), lk = .5 + .5 * ramp(t, tT - .3, tT + .4), fl = .85 + .15 * Math.sin(t * 9);
  glow(ctx, fs[0] + 10, fs[1], 80 * lk, `rgba(255,220,150,${.6 * lk * fl})`);
  for (let k = 0; k < 4; k++) { const a = -.6 + k * .4 + Math.sin(t * 3 + k) * .1; ctx.strokeStyle = `rgba(255,236,190,${.7 * lk})`; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(fs[0] + 10 + Math.cos(a) * 20, fs[1] + Math.sin(a) * 20); ctx.lineTo(fs[0] + 10 + Math.cos(a) * (40 + 20 * lk), fs[1] + Math.sin(a) * (40 + 20 * lk)); ctx.stroke(); }
  // dinmez öfke: tahttaki siluetten koyu duman kaynar
  const sm = ramp(t, tD - .4, tD + .8);
  if (sm > 0) smokeWisps(ctx, 1385, 236, 260 * sm, t, { n: 5, a: .85 * sm, w: 6, spread: 30, sway: 44 });
  // başka yerde: Prometheus'un başında ikinci kıvılcım
  const pa = ramp(t, tV, tV + .8);
  if (pa > 0) { ctx.save(); ctx.globalAlpha = pa; bf(ctx, 300, 760, 5.0, 1, LK.promFree, { torso: -.03, head: -.15, breath: Math.sin(t * 1.5) * .5 }); ctx.restore();
    glow(ctx, 318, 250, 70, `rgba(255,220,150,${.55 * pa * fl})`); ctx.fillStyle = C.white; ctx.beginPath(); ctx.arc(318, 250, 7 * pa, 0, TAU); ctx.fill(); }
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => erhatStrip(ctx, st.t - A('D07@erhatın') + .2, A('D07@ve') - A('D07@erhatın') + .2, '“Akıl gücüyse Zeus’un tekelindedir”', 'ix', { font: 'italic 600 56px "Cormorant Garamond"' }) });

// --- P066: amfora: dev Zeus'un karşısında küçük ama dik Prometheus; D08@geleceği'de gözünde kıvılcım ---
shot(PA('P066'), (ctx, st) => {
  const t = st.t, lt = st.lt, tG = A('D08@geleceği');
  amphoraFrieze(ctx, t, 2400 + lt * 14, (c, x0, x1, t) => {
    const by = 640; c.fillStyle = C.ink; c.fillRect(x0, by, x1 - x0, 6);
    bf(c, 2150, by, 6.6, 1, LK.zeus, { torso: .04, neck: .1, head: .15, shN: .3, elN: .4, shF: -.4, elF: .3, breath: Math.sin(t * 1.2) * .6 }, { hold: { F: HOLD.bolt() } });
    let PJ = null, PM = null;
    bf(c, 2700, by, 3.6, -1, LK.promFree, { torso: -.05, neck: -.18, head: -.3, shN: .1, elN: .2, breath: Math.sin(t * 1.6) * .5 }, { onJoints: (j, m) => { PJ = j; PM = m; } });
    const e = ramp(t, tG - .1, tG + .4);
    if (e > 0 && PJ) { const [ex, ey] = jointPt(c, PM, add(PJ.neckT, rot([3.75, -7.1], PJ.headA))); glow(c, ex, ey, 24 * e, `rgba(255,230,170,${.8 * e})`); c.fillStyle = C.white; c.beginPath(); c.arc(ex, ey, 3.2 * e, 0, TAU); c.fill(); }
  }, { light: .3 });
}, { tr: { type: 'clay', dur: .5, end: true }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P067: tek METOP frizi, üç pano art arda tam kare: aldatır / tedirgin eder / gülünç düşürür; sonda üçü yan yana ---
shot(PA('P067'), (ctx, st) => {
  const t = st.t, lt = st.lt, w1 = A('D08@aldatır'), w2 = A('D08@tedirgin'), w3 = A('D08@gülünç'), wE = A('D08@düşürür') + .3;
  clayBG(ctx, C.clayL, C.clayD);
  const pan = t < w2 ? 0 : t < w3 ? 1 : 2, back = E.io2(ramp(t, wE, wE + 1.2));
  const pw = 900, X0 = 960 - pw * 1.5;
  const cx = X0 + pw * (pan + .5), c = { x: lerp(cx, 960, back), y: 520, z: lerp(1.95, 1.0, back) * (1 + .01 * Math.sin(t)) };
  ctx.save(); cam(ctx, c, 1);
  D_metope(ctx, X0, X0 + pw * 3, 220, 820, 3);
  const by = 790; ctx.fillStyle = C.ink; ctx.fillRect(X0, by, pw * 3, 6);
  // 1: el çabukluğu: iki pay yer değiştirir
  { const x = X0 + pw * .5, sw = E.io2(ramp(t, w1 + .1, w1 + .7));
    bf(ctx, x - 160, by, 3.4, 1, LK.promFree, { torso: .3, shN: 1.2, elN: .4, shF: 1.0, elF: .5, handN: 'open', handF: 'open' });
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.ellipse(x + lerp(40, 200, sw), 640 - 40 * Math.sin(PI * sw), 50, 26, 0, 0, TAU); ctx.fill();
    ctx.fillStyle = C.white; ctx.beginPath(); ctx.ellipse(x + lerp(200, 40, sw), 640 + 30 * Math.sin(PI * sw), 50, 26, 0, 0, TAU); ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.stroke(); }
  // 2: Zeus omzunun üstünden tedirgin bakar; arkasında küçük Prometheus
  { const x = X0 + pw * 1.5, lk = ramp(t, w2 + .1, w2 + .5);
    bf(ctx, x - 40, by, 4.0, 1, LK.zeus, { torso: .05, neck: -.1 * lk, head: lk > .5 ? 0 : 0, shN: .2, elN: .3, headBack: lk > .5 }, { hold: { N: HOLD.scepter(70) } });
    bf(ctx, x - 300, by, 2.6, 1, LK.promFree, { torso: -.02, head: -.1 }); }
  // 3: Zeus'un çelengi yan yatar; arkadaki tanrı siluetlerinde omuz sarsıntısı (gülme)
  { const x = X0 + pw * 2.5, g = ramp(t, w3 + .05, w3 + .4);
    for (const [dx, i] of [[-300, 0], [-200, 1], [220, 2], [320, 3]]) bf(ctx, x + dx, by, 2.9, dx < 0 ? 1 : -1, { beard: i % 2 ? 'short' : 'full', hair: 'long', garment: 'robe' }, { torso: .05 + .05 * g * Math.sin(t * 20 + i), neck: .05 * g * Math.sin(t * 18 + i), head: .1 });
    let J = null, M = null;
    bf(ctx, x, by, 4.0, 1, LK.zeus, { torso: .1 * g, head: .15 * g, shN: .2, elN: .3 }, { onJoints: (j, m) => { J = j; M = m; } });
    if (J) { const h = jointPt(ctx, M, J.neckT); ctx.save(); ctx.translate(h[0] + 6, h[1] - 50); ctx.rotate(.5 * g); ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.beginPath(); ctx.ellipse(0, 0, 34, 9, 0, 0, TAU); ctx.stroke(); ctx.restore(); } }
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P068: amforadaki ΠΡΟΜΗΘΕΥΣ yazısı ΠΡΟ · ΜΗΘΕΥΣ diye ayrılır; altında "önceden düşünen" ---
shot(PA('P068'), (ctx, st) => {
  const t = st.t, lt = st.lt, tP = A('D09@prometeus'), tO = A('D09@önceden');
  amphoraFrieze(ctx, t, 4200 + lt * 10, (c, x0, x1, t) => {
    const by = 610; c.fillStyle = C.ink; c.fillRect(x0, by, x1 - x0, 6);
    bf(c, 4820, by, 5.2, -1, LK.promFree, { torso: -.03, head: -.12, breath: Math.sin(t * 1.5) * .5 });
    const sp = E.io2(ramp(t, tP + .3, tP + 1.1)), a = ramp(lt, .1, .7);
    // ΠΡΟ (3 harf ≈ 230 px) ve ΜΗΘΕΥΣ (6 harf ≈ 470 px) bitişik başlar, ayrılınca arada nokta
    dipinto(c, 'ΠΡΟ', 3830 - 90 * sp, 220, 110, { col: C.ink, a, align: 'center' });
    dipinto(c, 'ΜΗΘΕΥΣ', 4190 + 60 * sp, 220, 110, { col: C.ink, a, align: 'center' });
    if (sp > .5) { c.fillStyle = C.red; c.beginPath(); c.arc(3920, 222, 10, 0, TAU); c.fill(); }
  });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => { const tO = A('D09@önceden'); const a = ramp(st.t, tO - .1, tO + .5) * (1 - ramp(st.t, A('D09@erhatın') + .6, A('D09@erhatın') + 1.2)); if (a > 0) { txt(ctx, 'PRO · METHEUS', 960, 640, { font: '700 64px Cinzel', col: C.ink, ls: 8, a, shadow: 'rgba(242,214,170,.9)', blur: 14 }); txt(ctx, '“önceden düşünen”', 960, 712, { font: 'italic 600 56px "Cormorant Garamond"', col: C.ink, a, shadow: 'rgba(242,214,170,.9)', blur: 14 }); } } });

// --- P069: göze dalış: göz bebeğinin siyahı bir tondoya açılır; tondoda Zeus'un tahtı yerinde, sağ ayağında altın çatlak yanar ---
shot(PA('P069'), (ctx, st) => {
  const t = st.t, lt = st.lt, open = E.io2(ramp(lt, 0, .7));
  ctx.fillStyle = C.ink; ctx.fillRect(0, 0, W, H);
  const R = lerp(40, 430, open);
  ctx.save(); ctx.beginPath(); ctx.arc(960, 550, R, 0, TAU); ctx.clip();
  kylix(ctx, t, 960, 550, 430, lt * .05, (c, t, r) => {
    c.fillStyle = C.ink; c.fillRect(-r, r * .5, 2 * r, 7);
    throne(c, 0, r * .5, 7.4, 1, C.ink, C.clay, { high: true });
    crackLine(c, 18 * 7.4, r * .5, 70, ramp(t, A('D09@kahin'), A('D09@kahin') + .5), { col: PC.fire, w: 3 });
  });
  ctx.restore();
  // gözün kenarı (profil göz, siyah figür) dalışta büyüyüp kadrajdan çıkar
  const s = lerp(1, 9, open); ctx.save(); ctx.translate(960, 550); ctx.scale(s, s); ctx.strokeStyle = C.clay; ctx.lineWidth = 3 / s * 3; ctx.beginPath(); ctx.moveTo(-90, 0); ctx.quadraticCurveTo(0, -60, 100, -4); ctx.quadraticCurveTo(0, 46, -90, 0); ctx.stroke(); ctx.restore();
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });

// --- P070–P071: TAHT: geri çağrı: Gaia Kronos'a fısıldar ↔ Prometheus bilir; çatlak büyür; kenar şeridi: üçüncü devrimin hazırlanması ---
shot(PA('P070'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('D09@bilir'), tD = A('D10');
  clayBG(ctx, C.clayL, C.clayD);
  const c = { x: 960 + lt * 5, y: 520, z: 1.06 + lt * .004 };
  ctx.save(); cam(ctx, c, 1);
  D_thrones(ctx, t, { tip: [1.2, 1.2], crack: .2 + .5 * ramp(t, tB - .2, tB + .6) + .3 * ramp(t, tD + 1, tD + 3), na: .7 });
  // anı: Gaia Kronos'a fısıldar (soluk, sol üstte)
  const m = ramp(lt, .1, .8) * (1 - ramp(t, A('D09@prometeus#1') + .2, A('D09@prometeus#1') + 1.0));
  if (m > 0) { ctx.save(); ctx.globalAlpha = .55 * m; bf(ctx, 380, 520, 3.0, 1, LK_GAIA, { torso: .2, head: .3, shN: .8, elN: 1.4 }); bf(ctx, 560, 520, 3.0, -1, LK_KRONOS, { torso: -.05, head: .1 }); ctx.fillStyle = C.ink; ctx.fillRect(260, 520, 420, 4); ctx.restore(); }
  // Prometheus bilir: tahtın çatlağına bakar
  const pa = ramp(t, A('D09@prometeus#1') - .2, A('D09@prometeus#1') + .6);
  if (pa > 0) { ctx.save(); ctx.globalAlpha = pa; bf(ctx, 1000, 760, 4.6, 1, LK.promFree, { torso: -.02, head: .12 }); ctx.restore(); }
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 },
  over: (ctx, st) => erhatStrip(ctx, st.t - A('D10@üçüncü') + .3, 3.4, '“Üçüncü devrimin hazırlanması.”', 'x') });

// --- P072–P074: TAHT, tek kamera hareketi: devrik iki tahtın boyunca kayar (D11@devrilmişti #0 ve #1'de toz); üçüncüde durur: devrilmez, titrer ---
shot(PA('P072'), (ctx, st) => {
  const t = st.t, lt = st.lt, d0 = A('D11@devrilmişti'), d1 = A('D11@devrilmişti#1'), tS = A('D11@sıra');
  clayBG(ctx, C.clayL, C.clayD);
  const k = E.io2(ramp(t, PA('P072'), tS + .2, E.lin));
  const c = { x: lerp(500, 1360, k), y: lerp(560, 520, k), z: lerp(1.9, 2.1, k) + .15 * ramp(t, tS, tS + 2.5) };
  ctx.save(); cam(ctx, c, 1);
  D_thrones(ctx, t, { tip: [lerp(.85, 1.2, ramp(t, d0, d0 + .4)), lerp(.85, 1.2, ramp(t, d1, d1 + .4))], crack: .75, shake: 1.6 * ramp(t, tS, tS + .3), names: true });
  for (const [tt, x] of [[d0, 560], [d1, 960]]) if (t > tt && t - tt < 2.2) dustBurst(ctx, t, tt, x - 40, 760, 26, 'rgba(23,16,12,.45)', 160, 7);
  ctx.restore();
  friezeFrame(ctx, { col: C.ink, h: 44, bandBg: C.clay });
}, { tr: { type: 'cut' }, post: { tex: .85, vig: .85, grain: .055 } });
