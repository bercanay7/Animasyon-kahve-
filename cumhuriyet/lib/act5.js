// V · ANADOLU (F01–F06): Samsun, Amasya, gizli geçiş, Halide Edib, kongreler → Büyük Taarruz montajı, kuşak hazır
'use strict';

// ——— yardımcılar ———
// gök bantları (düz kalıp, gradyansız): üstten alta [kalıp, alfa, y-sınır]
function a5_sky(ctx, bands) {
  let y0 = -20;
  for (const [pl, a, y1] of bands) { if (pl) plate(ctx, pl, PL([[-20, y0], [W + 20, y0], [W + 20, y1], [-20, y1]]), { a }); y0 = y1; }
}
// deniz: turkuaz düz şeritler + akan kısa dalga çizgileri
function a5_sea(ctx, y0, t, o = {}) {
  const sea = PL([[-40, y0], [W + 40, y0], [W + 40, H + 40], [-40, H + 40]]);
  plate(ctx, 'teal', sea, { a: o.a ?? .75 });
  plate(ctx, 'teal', PL([[-40, y0 + 120], [W + 40, y0 + 110], [W + 40, H + 40], [-40, H + 40]]), { a: .35 });
  const r = rng(o.seed || 5);
  for (let i = 0; i < 46; i++) {
    const yy = y0 + 18 + r() * (H - y0), sp = 6 + (yy - y0) * .04, x = ((r() * W * 1.4 + t * sp) % (W + 200)) - 100, L = 30 + (yy - y0) * .12;
    cut(ctx, SP([[x, yy], [x + L * .5, yy - 3], [x + L, yy]], false), 1.6 + (yy - y0) * .004, { a: .55 });
  }
}
// uzak kıyı sırtı (haki)
function a5_hills(ctx, y, amp, seed, a = 1) {
  const pts = [[-40, H]]; for (let x = -40; x <= W + 40; x += 60) pts.push([x, y - amp * (.5 + .5 * Math.sin(x * .004 + seed) * Math.cos(x * .0017 + seed * 2))]);
  pts.push([W + 40, H]); const p = PL(pts); plate(ctx, 'khaki', p, { a }); return p;
}
// Bandırma vapuru silueti (is), sağa ya da sola bakar
function a5_steamer(ctx, x, y, s, t) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const hull = PL([[-230, -10], [210, -10], [180, 34], [-200, 34]]);
  inkFill(ctx, hull);
  inkFill(ctx, PL([[-120, -10], [100, -10], [96, -46], [-110, -46]]));                // üst yapı
  inkFill(ctx, PL([[-40, -46], [-10, -46], [-12, -120], [-38, -120]]));               // baca
  cut(ctx, PL([[-37, -100], [-13, -100]], false), 3, { a: .7 });
  for (const mx of [-170, 150]) inkStroke(ctx, PL([[mx, -10], [mx, -150]], false), 4);  // direkler
  inkStroke(ctx, PL([[-170, -150], [150, -150]], false), 1.6, { a: .6 });
  for (let i = 0; i < 9; i++) { const wx = -96 + i * 22; const w = new Path2D(); w.arc(wx, -28, 4, 0, TAU); cut(ctx, w, 2, { a: .8 }); }
  // duman: düz halka kümeleri, rüzgârla geriye
  for (let k = 0; k < 6; k++) { const u = ((t * .18 + k / 6) % 1), r = 18 + u * 46; const p = new Path2D(); p.arc(-26 - u * 260, -130 - u * 90, r, 0, TAU); plate(ctx, 'ink', p, { a: .22 * (1 - u) }); }
  ctx.restore();
}
// damga kalabalık: baş-omuz siluetleri; kinds: fes, kalpak, basortu, sapka, carsaf, kabalak
function a5_crowd(ctx, x0, x1, y, rows, seed, t, o = {}) {
  const r = rng(seed), kinds = o.kinds || ['fes', 'kalpak', 'basortu', 'carsaf', 'fes', 'sapka'];
  for (let row = 0; row < rows; row++) {
    const yy = y + row * (o.dy || 46), sc = (o.s || 1) * (1 + row * .14), gap = 34 * sc;
    // sanat kurulu A7: her derinlik sırası tek yolda birleşir ve bir kez basılır (çakışan yerler koyulaşmaz)
    const rowP = new Path2D(), reds = [], back = row < rows - 1 && rows > 1;
    for (let x = x0 + (row % 2) * gap * .5; x < x1; x += gap * (.85 + r() * .3)) {
      const k = kinds[Math.floor(r() * kinds.length)], bob = Math.sin(Math.floor(t * 6) * .9 + x * .03) * 1.4 * (o.bob ?? 1);
      const m = new DOMMatrix().translateSelf(x, yy + bob).scaleSelf(sc, sc);
      const p = new Path2D();
      p.ellipse(0, -30, 10, 12, 0, 0, TAU); p.moveTo(-24, 20); p.quadraticCurveTo(-22, -10, 0, -14); p.quadraticCurveTo(22, -10, 24, 20); p.closePath();
      if (k === 'fes') p.rect(-8, -52, 16, 14); else if (k === 'kalpak') p.rect(-11, -54, 22, 16); else if (k === 'sapka') { p.rect(-15, -42, 30, 4); p.rect(-8, -54, 16, 13); }
      else if (k === 'basortu' || k === 'carsaf') { p.moveTo(-13, -26); p.quadraticCurveTo(-14, -46, 0, -47); p.quadraticCurveTo(14, -46, 13, -26); p.lineTo(16, 10); p.lineTo(-16, 10); p.closePath(); }
      else if (k === 'kabalak') p.ellipse(0, -40, 12, 9, 0, PI, TAU);
      rowP.addPath(p, m);
      if (k === 'fes' && !back && o.fesRed) { const q = new Path2D(); q.addPath(PL([[-8, -52], [8, -52], [8, -38], [-8, -38]]), m); reds.push(q); }
    }
    if (back && o.fade !== false) plate(ctx, o.backPlate || 'ink', rowP, { a: .55 - (rows - 1 - row) * .12 }); else inkFill(ctx, rowP);
    for (const q of reds) plate(ctx, 'red', q, { flat: true, a: .9 });
  }
}
// kâğıt kart (çerçeveli iç pano): içine çizim fonksiyonu
function a5_card(ctx, x, y, w, h, rot, draw) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
  plate(ctx, 'ink', PL([[-w / 2 + 10, -h / 2 + 12], [w / 2 + 10, -h / 2 + 12], [w / 2 + 10, h / 2 + 12], [-w / 2 + 10, h / 2 + 12]]), { a: .35 });
  const box = PL(rough([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]], 1.2, w));
  knock(ctx, box); ctx.save(); ctx.clip(box); ctx.translate(-w / 2, -h / 2); draw(ctx, w, h); ctx.restore(); inkStroke(ctx, box, 3.2);
  ctx.restore();
}
// cami silueti (kubbe + minareler), is
function a5_mosque(ctx, cx, y, s, a = 1) {
  ctx.save(); ctx.translate(cx, y); ctx.scale(s, s);
  const p = new Path2D();
  p.rect(-260, -60, 520, 60); p.ellipse(0, -60, 150, 110, 0, PI, TAU); p.ellipse(-170, -60, 70, 50, 0, PI, TAU); p.ellipse(170, -60, 70, 50, 0, PI, TAU);
  p.rect(-6, -205, 12, 40);
  for (const mx of [-300, -230, 230, 300, -380, 380]) { p.rect(mx - 8, -280, 16, 280); p.moveTo(mx - 8, -280); p.lineTo(mx, -320); p.lineTo(mx + 8, -280); p.closePath(); p.rect(mx - 12, -200, 24, 6); }
  plate(ctx, 'ink', p, { a }); ctx.restore();
}
// el sıkışma (yakın plan, iki kaput kolu)
function a5_handshake(ctx, x, y, s, t) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  for (const sg of [-1, 1]) {
    const sl = PL([[sg * 620, -70], [sg * 120, -46], [sg * 110, 40], [sg * 620, 70]]); knock(ctx, sl); plate(ctx, sg < 0 ? 'khaki' : 'grey', sl, { a: sg < 0 ? 1 : .8 }); inkStroke(ctx, sl, 5);
    const cuff = PL([[sg * 150, -50], [sg * 110, -46], [sg * 106, 42], [sg * 146, 46]]); knock(ctx, cuff); plate(ctx, sg < 0 ? 'khaki' : 'grey', cuff, { n: 2 }); inkStroke(ctx, cuff, 4);
    inkStroke(ctx, SP([[sg * 400, -20], [sg * 340, 10], [sg * 300, -10]], false), 3, { a: .55 });
  }
  // kenetlenmiş eller
  const hands = SP([[-112, -40], [-40, -62], [30, -58], [108, -40], [112, 30], [60, 54], [-20, 58], [-110, 36]], true, .9);
  knock(ctx, hands); plate(ctx, 'ochre', PL([[-120, 4], [120, 4], [120, 70], [-120, 70]]), { a: .38 }); inkStroke(ctx, hands, 5);
  for (let i = 0; i < 4; i++) inkStroke(ctx, SP([[-30 + i * 20, -56], [-24 + i * 20, -20], [-30 + i * 20, 10]], false), 3, { a: .8 });
  inkStroke(ctx, SP([[40, -50], [70, -26], [90, -36]], false), 3.5); // başparmak
  ctx.restore();
}
// kalıp parçası: okul sırası (yandan) ve fesli çocuk büstü
function a5_desk(ctx, x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const top = PL([[-120, -10], [120, -18], [120, 0], [-120, 8]]); knock(ctx, top); plate(ctx, 'ochre', top, { n: 2 }); inkStroke(ctx, top, 3);
  const front = PL([[-120, 8], [120, 0], [120, 90], [-120, 98]]); knock(ctx, front); plate(ctx, 'sepia', front, { a: .7 }); inkStroke(ctx, front, 3);
  for (const k of [-60, 0, 60]) cut(ctx, PL([[k, 14], [k, 88]], false), 2, { a: .4 });
  ctx.restore();
}

// ——— çekimler ———
// F01 · Samsun, şafak: vapur, iskele; "yalnız değildi" → arkasında kurmay heyeti belirir
shot(S('F01') - .7, (ctx, st) => {
  setReg(51); const t = st.t, lt = st.lt;
  paperBG(ctx);
  const c = { x: W / 2 + lt * 6, y: H / 2, z: 1 + lt * .006 };
  ctx.save(); cam(ctx, c, .3);
  a5_sky(ctx, [['gold', .55, 230], ['gold', .3, 390], ['ochre', .22, 520], [null, 0, 600]]);
  const sun = new Path2D(); sun.ellipse(1520, 600, 120, 120, 0, PI, TAU); knock(ctx, sun, '#F6EBD0'); plate(ctx, 'gold', sun, { a: .35 });
  ctx.restore();
  ctx.save(); cam(ctx, c, .5); a5_hills(ctx, 610, 50, 2.2, .7); ctx.restore();
  ctx.save(); cam(ctx, c, .7); a5_sea(ctx, 640, t, { seed: 3 }); a5_steamer(ctx, 1260 - lt * 18, 655, 1.0, t); ctx.restore();
  // iskele (sol ön)
  ctx.save(); cam(ctx, c, 1);
  const pier = PL([[-40, 780], [700, 760], [700, 800], [-40, 830]]); knock(ctx, pier); plate(ctx, 'ochre', pier, { n: 2 }); plate(ctx, 'ink', pier, { a: .3 }); inkStroke(ctx, pier, 4);
  for (let x = 40; x < 700; x += 90) { const pl = PL([[x, 800], [x + 14, 800], [x + 14, 1100], [x, 1100]]); knock(ctx, pl); plate(ctx, 'ochre', pl, { n: 2 }); inkStroke(ctx, pl, 3); }
  for (let i = 0; i < 9; i++) cut(ctx, PL([[-40 + i * 84, 772 - i * 2], [-40 + i * 84, 820 - i * 2]], false), 1.6, { a: .4 });
  // kurmay heyeti silueti (yalnız değildi)
  const ya = ramp(t, Wd('F01', 'yalnız') - .2, Wd('F01', 'yalnız') + .5);
  if (ya > 0) { ctx.save(); ctx.globalAlpha = ya; REG.boost = 1 + 4 * (1 - ya);
    for (const [x, y, s] of [[520, 470, 1.05], [660, 480, 1.0], [790, 488, .95]]) { bust(ctx, { x, y, s, dir: -1, coat: 'kaput', col: 'khaki', w: .9, seed: x, len: 400, back: true, arms: 'back' }); head3q(ctx, { x, y, s, dir: -1, who: 'anon', id: { seed: x }, gear: 'kalpak', light: 'front', look: [1, .2], age: 34 }); }
    REG.boost = 1; ctx.restore(); }
  // iskele güvertesi: heyetin önünden geçer (havada durmazlar), Mustafa Kemal güvertenin önünde
  { const deck = PL([[-40, 862], [930, 850], [930, 1100], [-40, 1100]]); knock(ctx, deck); plate(ctx, 'ochre', deck, { n: 2 }); plate(ctx, 'ink', deck, { a: .3 }); inkStroke(ctx, PL([[-40, 862], [930, 850], [930, 1100]], false), 4);
    for (let i = 1; i < 6; i++) cut(ctx, PL([[-40, 862 + i * 40], [930, 850 + i * 40]], false), 1.8, { a: .35 }); }
  // Mustafa Kemal (38): iskelede, kalpak ve kaput; karaya (sola) bakar
  const mk = { x: 330, y: 440, s: 1.6, dir: -1 };
  const id = idleOffsets(Math.floor(t * 15) / 15, 3, .6);
  bust(ctx, { ...mk, coat: 'kaput', col: 'khaki', w: .96, seed: 3, len: 520, turn: .25, sep: true, arms: 'back' });
  head3q(ctx, { ...mk, who: 'mk', gear: 'kalpak', gearCol: 'ink', light: 'front', look: [1.2, .2], age: 38, tilt: -.03 + (id.head || 0) * .2 });
  ctx.restore();
  chapterCard(ctx, 'V', 'ANADOLU', '1919 · CUMHURİYET’E 4 YIL', lt - .3, 3.4, { side: 'right' });
  stamp(ctx, 'SAMSUN · 19 MAYIS 1919', 114, 112, lt - 3.75, 2.6); // kart kalkınca, standart sol üst yuvada
}, { tr: { type: 'press', dur: .7 } });

// F02 · Amasya: masa başında dört arkadaş; Karabekir telgrafla doğudan
function a5_amasya(ctx, t, lt, camx) {
  ctx.fillStyle = P.paper; ctx.fillRect(-20, -20, W + 700, H + 40);
  plate(ctx, 'navy', PL([[-20, -20], [W + 700, -20], [W + 700, H + 20], [-20, H + 20]]), { a: .5 });
  plate(ctx, 'ochre', PL([[-20, -20], [W + 700, -20], [W + 700, H + 20], [-20, H + 20]]), { a: .3 });
  // duvarda pencere: gece ve Amasya kayalıkları silueti
  const win = PL([[150, 150], [470, 150], [470, 520], [150, 520]]); knock(ctx, win); plate(ctx, 'navy', win, { a: .85 });
  ctx.save(); ctx.clip(win); plate(ctx, 'ink', PL([[140, 520], [140, 360], [220, 300], [300, 340], [380, 260], [480, 330], [480, 520]]), { a: .8 });
  const moon = new Path2D(); moon.arc(400, 220, 30, 0, TAU); knock(ctx, moon, '#F3E9D2'); ctx.restore();
  inkStroke(ctx, win, 6); inkStroke(ctx, PL([[310, 150], [310, 520]], false), 5);
  gasLamp(ctx, 1000, 130, 1.0, t);
  for (const [r, a] of [[170, .18], [110, .3]]) { const g = new Path2D(); g.ellipse(1000, 140, r * 1.2, r * .8, 0, 0, TAU); plate(ctx, 'gold', g, { a }); }
  const S_ = 1.2;
  // Refet ve Rauf arkada, Ali Fuat ile MK önde
  const P4 = [
    { who: 'refet', x: 640, y: 360, dir: 1, coat: 'kaput', col: 'khaki', back: true },
    { who: 'rauf', x: 1370, y: 352, dir: -1, coat: 'civil', col: 'navy', back: true, gear: 'fes' },
    { who: 'alifuat', x: 830, y: 392, dir: 1, coat: 'kaput', col: 'khaki', sep: true },
    { who: 'mk', x: 1150, y: 386, dir: -1, coat: 'kaput', col: 'khaki', sep: true, arms: 'back' },
  ];
  const focus = [1000, 760];
  for (const p of P4) {
    const id = idleOffsets(Math.floor(t * 15) / 15, p.who.length, .5);
    // yürüyüş: adım başına inip kalkma, 15 fps poz (Fevzi yarım adım geriden)
    const ph = (Math.floor(t * 15) / 15) * 1.7 * TAU + (p.who === 'fevzi' ? PI : 0), bob = -Math.abs(Math.sin(ph)) * 7;
    p.y = (p.y0 ??= p.y) + bob;
    bust(ctx, { x: p.x, y: p.y, s: S_, dir: p.dir, coat: p.coat, col: p.col, w: .96, seed: p.who.length, len: (900 - p.y) / S_, turn: .3, sep: p.sep, back: p.back, arms: p.arms });
    head3q(ctx, { x: p.x, y: p.y, s: S_, dir: p.dir, who: p.who, gear: p.gear || 'kalpak', gearCol: 'ink', light: 'front', lookAt: focus, age: { alifuat: 36, rauf: 37, refet: 38, mk: 38 }[p.who], tilt: (id.head || 0) * .2 });
  }
  // masa ve genelge
  ctx.save(); ctx.translate(0, 0); woodTable(ctx, 760, { seed: 7 }); ctx.restore();
  ctx.save(); ctx.translate(W - 20, 0); woodTable(ctx, 760, { seed: 8 }); ctx.restore();
  paperSheet(ctx, 990, 860, 300, 150, -.04, 33, { rows: 6, header: true });
}
shot(S('F02') - .15, (ctx, st) => {
  setReg(53); const t = st.t, lt = st.lt;
  const pan = ramp(t, Wd('F02', 'doğudan') - .2, Wd('F02', 'doğudan') + 1.1, E.io3);
  ctx.save(); ctx.translate(-pan * 520, 0);
  a5_amasya(ctx, t, lt);
  // telgraf teli doğuya
  const wl = pan * 600;
  ctx.save(); ctx.setLineDash([wl, 9999]); inkStroke(ctx, SP([[1700, 300], [1960, 320], [2160, 300]], false), 3); ctx.restore();
  for (const px of [1700, 2160]) { if (px - 1700 < wl) { inkFill(ctx, PL([[px - 6, 300], [px + 6, 300], [px + 4, 900], [px - 4, 900]])); inkStroke(ctx, PL([[px - 26, 312], [px + 26, 312]], false), 4); } }
  // Karabekir (37): Erzurum, telgraf kartında
  if (pan > .3) {
    const ka = ramp(pan, .3, .8);
    ctx.save(); ctx.globalAlpha = ka;
    a5_card(ctx, 2140, 560, 420, 520, .02, (g, w, h) => {
      plate(g, 'grey', PL([[0, 0], [w, 0], [w, h], [0, h]]), { a: .35 });
      plate(g, 'ink', PL([[0, 300], [80, 250], [160, 280], [260, 220], [w, 270], [w, h], [0, h]]), { a: .3 });
      bust(g, { x: 210, y: 210, s: 1.05, dir: -1, coat: 'kaput', col: 'khaki', w: .95, seed: 11, len: 300, sep: true, arms: 'back' });
      head3q(g, { x: 210, y: 210, s: 1.05, dir: -1, who: 'karabekir', gear: 'kalpak', gearCol: 'ink', light: 'front', look: [1, .2], age: 36 });
    });
    ctx.restore();
  }
  ctx.restore();
  // masadaki iki kişi önce (kendi başlarının altında); anlatıcı "Ali Fuat" dediğinde ekranda yalnız onun levhası
  const ta = Wd('F02', 'ali');
  nameTag(ctx, 640, 520, 'REFET', '1881 doğumlu', t - (S('F02') + .3), ta - .15 - (S('F02') + .3), { align: 'center' });
  nameTag(ctx, 1370, 520, 'RAUF', '37 yaşında', t - (S('F02') + .45), ta - .15 - (S('F02') + .45), { align: 'center' });
  nameTag(ctx, 830, 520, 'ALİ FUAT', '36 yaşında · sınıf arkadaşı', t - ta, 3.2, { align: 'center' }); // kendi başının altında (Refet ve Rauf gibi)
  stamp(ctx, 'AMASYA · 22 HAZİRAN 1919', 114, 112, lt - .2, 2.0);
  tickerTape(ctx, 'ERZURUM → AMASYA · TELGRAF', 1010, t - Wd('F02', 'doğudan'), 3.2);
  nameTag(ctx, 1800, 640, 'KÂZIM KARABEKİR', '36 yaşında', t - Wd('F02', 'karabekir') + .2, 2.8, { align: 'right' });
}, { tr: { type: 'cut', dur: .01 } });

// F03 · Gece, İstanbul'dan Ankara'ya gizli geçiş: İsmet (35) ve Fevzi (44)
shot(S('F03') - .25, (ctx, st) => {
  setReg(55); const t = st.t, lt = st.lt;
  paperBG(ctx);
  a5_sky(ctx, [['navy', .7, 520], ['navy', .55, 700]]);
  const moon = new Path2D(); moon.arc(300, 190, 70, 0, TAU); knock(ctx, moon, '#F3E9D2'); plate(ctx, 'gold', moon, { a: .25 });
  const cx = lt * 46; // kamera yürüyenlerle birlikte kayar
  ctx.save(); ctx.translate(-cx * .3, 0); a5_hills(ctx, 690, 70, 4.1, 1); plate(ctx, 'navy', PL([[-40, 700], [W + 40, 700], [W + 40, H], [-40, H]]), { a: .5 }); ctx.restore();
  // yol ve kağnı
  ctx.save(); ctx.translate(-cx, 0);
  inkStroke(ctx, SP([[-40, 900], [600, 860], [1300, 880], [2000, 840]], false), 30, { col: P.ochre, mode: 'multiply', a: .5 });
  stampOxcart(ctx, 1640 + lt * 30, 860, 1.4, Math.floor(t * 6) % 2);
  ctx.restore();
  // iki büst: ay ışığı arkadan
  const S_ = 1.35;
  for (const p of [{ who: 'ismet', x: 720, y: 430, age: 35, gc: 'ink' }, { who: 'fevzi', x: 1080, y: 410, age: 44, gc: 'grey' }]) {
    const id = idleOffsets(Math.floor(t * 15) / 15, p.who.length, .5);
    // yürüyüş: adım başına inip kalkma, 15 fps poz (Fevzi yarım adım geriden)
    const ph = (Math.floor(t * 15) / 15) * 1.7 * TAU + (p.who === 'fevzi' ? PI : 0), bob = -Math.abs(Math.sin(ph)) * 7;
    p.y = (p.y0 ??= p.y) + bob;
    bust(ctx, { x: p.x, y: p.y, s: S_, dir: 1, coat: 'kaput', col: 'grey', w: .95, seed: p.who.length, len: 420, turn: .2, sep: true, arms: 'back' });
    head3q(ctx, { x: p.x, y: p.y, s: S_, dir: 1, who: p.who, gear: 'kalpak', gearCol: p.gc, light: 'back', lookAt: [1900, 380], age: p.age, tilt: (id.head || 0) * .2 });
  }
  // ön planda yol şevi: figürler havada durmaz
  { const bank = SP([[-40, H + 20], [-40, 950], [500, 940], [1100, 958], [1600, 944], [W + 40, 952], [W + 40, H + 20]], true, .7); knock(ctx, bank); plate(ctx, 'navy', bank, { a: .62 }); plate(ctx, 'ochre', bank, { a: .25 }); inkStroke(ctx, PL([[-40, 950], [500, 940], [1100, 958], [1600, 944], [W + 40, 952]], false), 4); }
  plate(ctx, 'navy', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .12 });
  // rota: İstanbul → Ankara, şevin üstünde kâğıt renginde 40 px yol bandı (gece istisnasının açık değeri)
  const rp = ramp(t, Wd('F03', 'gizlice') - .1, Wd('F03', 'ankaraya') + .5, E.io2);
  if (rp > 0) {
    ctx.save(); const road = new Path2D(); road.moveTo(200, 1030); road.bezierCurveTo(600, 1004, 1200, 1050, 200 + 1480 * rp, 1022);
    inkStroke(ctx, road, 40, { col: '#EDE2C6' }); ctx.setLineDash([22, 16]); ctx.lineDashOffset = -t * 30; inkStroke(ctx, road, 3, { a: .7 }); ctx.restore();
    label(ctx, 'İSTANBUL', 140, 990, FONT.mono(40), { col: P.paper, a: 1 });
    label(ctx, 'ANKARA', 1660, 990, FONT.mono(40), { col: P.paper, a: ramp(rp, .85, 1) });
  }
  nameTag(ctx, 640, 300, 'İSMET', '35 yaşında', t - Wd('F03', 'ismet') + .2, 3.2, { align: 'right' });
  nameTag(ctx, 1824, 60, 'FEVZİ PAŞA', '44 yaşında · eski Harbiye Nazırı', t - Wd('F03', 'fevzi') + .2, 2.8, { align: 'right' });
}, { tr: { type: 'fade', dur: .5 } });

// F04a · Sultanahmet mitingi, 23 Mayıs 1919: Halide Edib çarşafla kürsüde
shot(S('F04') - .2, (ctx, st) => {
  setReg(57); const t = st.t, lt = st.lt;
  paperBG(ctx);
  a5_sky(ctx, [['ochre', .3, 360], ['ochre', .15, 600]]);
  ctx.save(); const z = 1 + lt * .008; ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  a5_mosque(ctx, 760, 600, 1.15, .55);
  a5_crowd(ctx, -40, W + 40, 640, 4, 91, t, { s: 1.15, dy: 70, backPlate: 'sepia' });
  // kürsü ve Halide Edib (35)
  const pod = PL([[1180, 760], [1600, 760], [1580, 1100], [1200, 1100]]); knock(ctx, pod); plate(ctx, 'sepia', pod, { a: .8 }); inkStroke(ctx, pod, 4);
  for (let i = 0; i < 5; i++) cut(ctx, PL([[1220 + i * 80, 780], [1230 + i * 78, 1090]], false), 2, { a: .35 });
  const h = { x: 1390, y: 470, s: 1.5, dir: -1 };
  bust(ctx, { ...h, coat: 'civil', col: 'ink', w: .9, seed: 19, len: 200, sep: true });
  head3q(ctx, { ...h, who: 'halide', gear: 'carsaf', light: 'front', look: [1, .1], age: 35, tilt: -.04 });
  ctx.restore();
  stamp(ctx, 'SULTANAHMET · 23 MAYIS 1919', 80, 110, lt - .3, 5);
  nameTag(ctx, 1860, 860, 'HALİDE EDİB', 'Amerikan Kız Koleji mezunu', t - Wd('F04', 'halide') + .1, 3.4, { size: 50, sub: 30, align: 'right' });
}, { tr: { type: 'press', dur: .6 } });

// F04b · Anadolu'da: haki ceket, başörtüsü; onbaşı → çavuş
shot(Wd('F04', 'sonra') - .1, (ctx, st) => {
  setReg(59); const t = st.t, lt = st.lt;
  paperBG(ctx);
  a5_sky(ctx, [['ochre', .35, 420], ['ochre', .18, 640]]);
  a5_hills(ctx, 690, 40, 1.3, .8);
  plate(ctx, 'ochre', PL([[-40, 700], [W + 40, 690], [W + 40, H], [-40, H]]), { a: .6 });
  const ph = Math.floor(t * 6) % 2;
  for (let i = 0; i < 5; i++) { const x = ((180 + i * 330 + lt * 40) % (W + 300)) - 150; i % 2 ? stampWoman(ctx, x, 700, 1.6, ph) : stampOxcart(ctx, x, 700, 1.25, ph); }
  const h = { x: 980, y: 430, s: 1.6, dir: -1 };
  bust(ctx, { ...h, coat: 'setre', col: 'khaki', w: .88, seed: 19, len: 420, sep: true });
  head3q(ctx, { ...h, who: 'halide', gear: 'basortu', light: 'front', look: [1, .1], age: 37, tilt: -.03 });
  // rütbe: kol üstünde şeritler (onbaşı iki, çavuş üç)
  // rütbe yalnız damgayla (kol şeritleri dönem belgesiyle doğrulanamadı: tarih danışmanı)
  const n = t > Wd('F04', 'çavuşluğa') ? 3 : 2;
  bigStamp(ctx, n === 3 ? 'ÇAVUŞ' : 'ONBAŞI', 1500, 300, t - (n === 3 ? Wd('F04', 'çavuşluğa') : Wd('F04', 'orduya')), 2.4, { size: 110, font: FONT.title });
}, { tr: { type: 'cut', dur: .01 } });

// F05 · montaj: kongreler, Meclis, Sakarya, Büyük Taarruz; sıra ve siper; harita, örgütlenme, güven
// onaylı Alagöz karesi ≥1,6 sn kalır: Meclis'ten 0,3 sn alır, Büyük Taarruz 'büyük' kelimesinden 0,3 sn sonra başlar
// montaj kesmeleri kelimeden 0,1 sn önce (yönetmenlik kurulu, 2. tur): Meclis 0,8 / Sakarya 1,0 / Kocatepe 1,3 sn
const A5_M = () => [Wd('F05', 'kongreler') - .1, Wd('F05', 'meclis') - .1, Wd('F05', 'sakarya') - .1, Wd('F05', 'büyük') - .1, Wd('F05', 'bu') - .05, Wd('F05', 'harita') - .1, Wd('F05', 'örgütlenmeyi') - .1, Wd('F05', 'birbirine') - .1];
function a5_year(ctx, s) {
  if (NOTEXT) return;
  // standart sol üst yuva (damga yuvası): Alagöz karesinde lambayla çakışmaz
  const band = PL(rough([[96, 52], [400, 52], [400, 150], [96, 150]], .8, 31)); knock(ctx, band); inkStroke(ctx, band, 2.6);
  txt(ctx, s, 248, 128, FONT.title(78), { align: 'center', ls: 4 });
}
shot(A5_M()[0], (ctx, st) => { // kongre salonu
  setReg(61); const t = st.t, lt = st.lt;
  paperBG(ctx); plate(ctx, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .35 });
  // pencerelerde Erzurum–Sivas dağları (boş çerçeve kalmaz)
  for (let i = 0; i < 4; i++) {
    const x0 = 200 + i * 420, w = PL([[x0, 180], [x0 + 220, 180], [x0 + 220, 460], [x0, 460]]); knock(ctx, w); plate(ctx, 'gold', w, { a: .3 });
    ctx.save(); ctx.clip(w); plate(ctx, 'grey', SP([[x0 - 10, 470], [x0 - 10, 380], [x0 + 50, 330 - i * 6], [x0 + 110, 372], [x0 + 160, 318 + i * 5], [x0 + 230, 362], [x0 + 230, 470]], true, .6), { a: .75 });
    plate(ctx, 'paperD', SP([[x0 + 40, 342 - i * 6], [x0 + 50, 330 - i * 6], [x0 + 64, 344 - i * 6]], true), { a: .9 }); ctx.restore();
    inkStroke(ctx, w, 4); inkStroke(ctx, PL([[x0 + 110, 180], [x0 + 110, 460]], false), 3);
  }
  ctx.save(); const z = 1.02 + lt * .02; ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  a5_crowd(ctx, 60, 1860, 620, 3, 61, t, { kinds: ['kalpak', 'kalpak', 'fes', 'sarik', 'kalpak'], s: 1.4, dy: 90, backPlate: 'sepia', bob: .4 });
  const tb = PL([[0, 830], [W, 820], [W, H], [0, H]]); knock(ctx, tb); plate(ctx, 'khaki', tb); inkStroke(ctx, PL([[0, 830], [W, 820]], false), 4);
  for (let i = 0; i < 6; i++) paperSheet(ctx, 260 + i * 280, 900, 160, 90, (i % 2 ? .05 : -.04), 70 + i, { rows: 3, shadow: false });
  ctx.restore();
  a5_year(ctx, '1919');
}, { tr: { type: 'press', dur: .4 } });
shot(A5_M()[1], (ctx, st) => { // TBMM binası
  setReg(63); const t = st.t, lt = st.lt;
  paperBG(ctx); a5_sky(ctx, [['gold', .35, 300], ['ochre', .2, 700]]);
  ctx.save(); const z = 1 + lt * .03; ctx.translate(W / 2, 700); ctx.scale(z, z); ctx.translate(-W / 2, -700);
  // Birinci Meclis binası (tarih danışmanı): andezit kesme taş (gri-pembe), kırma kiremit çatı, giriş merdiveni
  const roof = PL([[400, 380], [560, 300], [1360, 300], [1520, 380]]); knock(ctx, roof); plate(ctx, 'ochre', roof, { a: .55 }); plate(ctx, 'red', roof, { a: .35 }); plate(ctx, 'sepia', roof, { a: .35 }); inkStroke(ctx, roof, 4);
  for (let i = 1; i < 5; i++) cut(ctx, PL([[400 + i * 32, 380 - i * 16], [1520 - i * 32, 380 - i * 16]], false), 1.6, { a: .35 });
  const b = PL([[420, 380], [1500, 380], [1500, 820], [420, 820]]); knock(ctx, b); plate(ctx, '#A88780', b, { a: .8 }); inkStroke(ctx, b, 5);
  for (let r = 0; r < 11; r++) cut(ctx, PL([[424, 420 + r * 38], [1496, 420 + r * 38]], false), 1.4, { a: .3 }); // taş sıraları
  inkStroke(ctx, PL([[420, 600], [1500, 600]], false), 4); // kat silmesi
  for (let r = 0; r < 2; r++) for (let i = 0; i < 9; i++) { if (r === 1 && (i === 4)) continue; const w = PL([[480 + i * 112, 440 + r * 200], [540 + i * 112, 440 + r * 200], [540 + i * 112, 560 + r * 200], [480 + i * 112, 560 + r * 200]]); knock(ctx, w); plate(ctx, 'navy', w, { a: .5 }); inkStroke(ctx, w, 3); cut(ctx, PL([[510 + i * 112, 440 + r * 200], [510 + i * 112, 560 + r * 200]], false), 2, { a: .6 }); inkStroke(ctx, PL([[472 + i * 112, 440 + r * 200], [548 + i * 112, 440 + r * 200]], false), 5); }
  const door = PL([[910, 650], [1010, 650], [1010, 820], [910, 820]]); knock(ctx, door); inkFill(ctx, door);
  const ped = PL([[880, 640], [960, 604], [1040, 640]]); knock(ctx, ped); plate(ctx, '#A88780', ped); inkStroke(ctx, ped, 3);
  for (let k = 0; k < 4; k++) { const st = PL([[880 - k * 18, 820 + k * 16], [1040 + k * 18, 820 + k * 16], [1040 + k * 18, 836 + k * 16], [880 - k * 18, 836 + k * 16]]); knock(ctx, st); plate(ctx, 'grey', st, { a: .5 }); inkStroke(ctx, st, 2.4); }
  plate(ctx, 'ochre', PL([[0, 820], [W, 820], [W, H], [0, H]]), { a: .5 }); inkStroke(ctx, PL([[0, 820], [W, 820]], false), 4);
  a5_crowd(ctx, 300, 1620, 900, 1, 63, t, { kinds: ['kalpak', 'fes', 'kalpak'], s: 1.3, bob: .3 });
  ctx.restore();
  a5_year(ctx, '1920');
}, { tr: { type: 'cut', dur: .01 } });
shot(A5_M()[2], (ctx, st) => { // Sakarya: onaylı Alagöz karesi
  const z = 1.06 - st.lt * .03; ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  alagozScene(ctx, st.t, { captions: false }); ctx.restore();
  a5_year(ctx, '1921');
}, { tr: { type: 'cut', dur: .01 } });
shot(A5_M()[3], (ctx, st) => { // Büyük Taarruz: Kocatepe şafağı
  setReg(65); const t = st.t, lt = st.lt;
  paperBG(ctx);
  a5_sky(ctx, [['gold', .7, 260], ['gold', .45, 420], ['ochre', .3, 560], [null, 0, 640]]);
  const sun = new Path2D(); sun.ellipse(1300, 640 - 20 * E.out3(clamp(lt / 1.3)), 160, 160, 0, PI, TAU); knock(ctx, sun, '#F6EBD0'); plate(ctx, 'gold', sun, { a: .3 });
  // ufukta top ateşi (2 karelik yıldız) ve yükselen yarım ton duman: kare hiç durmaz
  for (const [x, ph] of [[1300, .1], [1500, .55], [1700, .9]]) {
    const u = (lt + ph) % 1.1, fl = u < .07;
    if (fl) { const st_ = new Path2D(); for (let k = 0; k < 10; k++) { const a = k * PI / 5, r = k % 2 ? 9 : 26; k ? st_.lineTo(x + r * Math.cos(a), 700 + r * Math.sin(a)) : st_.moveTo(x + r, 700); } st_.closePath(); knock(ctx, st_, '#FBF0D4'); plate(ctx, 'gold', st_, { a: .6 }); }
    const pf = new Path2D(), r0 = 18 + u * 34, cx_ = x - u * 26, cy_ = 704 - u * 70; // düz baskı duman bulutu (hareketli alanda yarım ton yok)
    for (const [ox, oy, k] of [[0, 0, 1], [-.8, .35, .7], [.85, .3, .75], [.2, -.6, .6]]) pf.ellipse(cx_ + ox * r0, cy_ + oy * r0, r0 * k, r0 * k * .8, 0, 0, TAU);
    plate(ctx, 'grey', pf, { a: .42 * (1 - u / 1.1) });
  }
  a5_hills(ctx, 690, 60, 5.3, .55);
  const ridge = SP([[-40, H], [-40, 820], [400, 760], [800, 790], [1200, 740], [1600, 800], [W + 40, 770], [W + 40, H]], true, .7); inkFill(ctx, ridge);
  // tepede siluetler (dürbünlü subaylar)
  for (const [x, y, s] of [[640, 760, 2.2], [760, 768, 2.0], [880, 774, 2.1]]) {
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
    const p = new Path2D(); p.ellipse(0, -60, 9, 11, 0, 0, TAU); p.rect(-10, -84, 20, 14); p.moveTo(-20, 0); p.quadraticCurveTo(-22, -40, 0, -46); p.quadraticCurveTo(22, -40, 20, 0); p.closePath();
    if (x === 640) p.rect(4, -66, 20, 7);
    inkFill(ctx, p); ctx.restore();
  }
  // sis bandı (yarım ton yok, düz)
  plate(ctx, 'paperD', PL([[-40, 700], [W + 40, 690], [W + 40, 740], [-40, 750]]), { a: .5 });
  a5_year(ctx, '1922');
}, { tr: { type: 'cut', dur: .01 } });
shot(A5_M()[4], (ctx, st) => { // sıralarda ve siperlerde: bölünmüş kare birleşir
  setReg(67); const t = st.t, lt = st.lt;
  paperBG(ctx);
  const zc = 1 + .04 * E.io2(clamp(lt / st.d)); ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(zc, zc); ctx.translate(-W / 2, -H / 2);
  const tsp = Wd('F05', 'siperlerde');
  const split = 0;
  // sol: okul sırası, fesli çocuklar (1890'lar)
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W / 2 + split * W / 2, H); ctx.clip();
  plate(ctx, 'sepia', PL([[0, 0], [W, 0], [W, H], [0, H]]), { a: .35 });
  const bb = PL([[80, 120], [880, 120], [880, 440], [80, 440]]); knock(ctx, bb, '#3B3632'); inkStroke(ctx, bb, 6);
  inkStroke(ctx, (() => { const p = new Path2D(); p.arc(300, 290, 90, 0, TAU); p.moveTo(210, 290); p.lineTo(390, 290); p.moveTo(300, 200); p.lineTo(420, 380); return p; })(), 3, { col: '#EDE6D6' });
  for (let i = 0; i < 4; i++) {
    const o = { x: 150 + i * 220, y: 620, s: .95, dir: 1 };
    bust(ctx, { ...o, coat: 'setre', col: 'navy', w: .9, seed: i, len: 300, sep: true });
    head3q(ctx, { ...o, who: 'anon', id: { mus: null, seed: 30 + i, WD: 1.05 + i * .02 }, gear: 'fes', light: 'front', look: Math.floor(t * 15) / 15 > tsp + i * .1 ? [1.3, .1] : [1, .5], age: 13 + (i % 2) });
  }
  a5_desk(ctx, 450, 900, 3.4);
  ctx.restore();
  // sağ: siper, kabalaklı subaylar
  ctx.save(); ctx.beginPath(); ctx.rect(W / 2 + split * W / 2, 0, W, H); ctx.clip();
  plate(ctx, 'khaki', PL([[0, 0], [W, 0], [W, H], [0, H]]), { a: .35 });
  plate(ctx, 'ochre', PL([[W / 2, 760], [W, 740], [W, H], [W / 2, H]]), { n: 2 });
  for (let i = 0; i < 4; i++) {
    const o = { x: 1080 + i * 220, y: 600, s: .95, dir: -1 };
    bust(ctx, { ...o, coat: 'setre', col: 'khaki', w: .95, seed: i + 5, len: 300, sep: true });
    head3q(ctx, { ...o, who: ['karabekir', 'ismet', 'fevzi', 'alifuat'][i], gear: 'kabalak', light: 'front', look: Math.floor(t * 15) / 15 > tsp + (4 + i) * .1 ? [1.3, -.1] : [1, .3], age: [33, 31, 39, 33][i] });
  }
  const sand = PL([[W / 2 - 20, 780], [W + 20, 760], [W + 20, H], [W / 2 - 20, H]]); knock(ctx, sand); plate(ctx, 'ochre', sand, { n: 2 }); inkStroke(ctx, PL([[W / 2 - 20, 780], [W + 20, 760]], false), 4);
  for (let i = 0; i < 8; i++) { const sb = SP([[W / 2 + i * 120, 790], [W / 2 + 60 + i * 120, 770], [W / 2 + 120 + i * 120, 790], [W / 2 + 60 + i * 120, 820]], true); knock(ctx, sb); plate(ctx, 'khaki', sb); inkStroke(ctx, sb, 3); }
  ctx.restore();
  if (split < 1) inkStroke(ctx, PL([[W / 2 + split * W / 2, 0], [W / 2 + split * W / 2, H]], false), 6);
  ctx.restore();
  for (const [s_, x_, al, aa] of [['SIRA', 120, 'left', env(lt, .1, .4)], ['SİPER', W - 120, 'right', env(t - Wd('F05', 'siperlerde'), 0, .3)]]) {
    if (aa <= 0 || NOTEXT) continue;
    ctx.save(); ctx.globalAlpha = aa; ctx.font = FONT.title(80); const tw = ctx.measureText(s_).width; const bx = al === 'left' ? x_ - 20 : x_ - tw - 20;
    const bd = PL(rough([[bx, 926], [bx + tw + 40, 926], [bx + tw + 40, 1018], [bx, 1018]], .8, s_.length)); knock(ctx, bd); inkStroke(ctx, bd, 2.6);
    ctx.restore(); label(ctx, s_, x_, 1000, FONT.title(80), { align: al, a: aa });
  }
}, { tr: { type: 'press', dur: .4 } });
shot(A5_M()[5], (ctx, st) => { // harita okumayı: yakın plan kurmay haritası, pergel
  setReg(69); const t = st.t, lt = st.lt;
  paperBG(ctx);
  const z = 1.6 + lt * .05; ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-560, -380);
  staffMap(ctx, { x: 100, y: 100, w: 900, rot: 0, front: ramp(lt, .1, 1.1), arrows: 1, focus: [640, 330] });
  ctx.restore();
  handDraw(ctx, 1240 - lt * 40, 640 + lt * 10, PI * .95, 2.2, 'point', { side: -1 });
}, { tr: { type: 'cut', dur: .01 } });
// Anadolu taslağı (boylam/enlem → ekran): x = 150 + (λ − 26)·85, y = 140 + (42,2 − φ)·125
const A5_LL = (lon, lat) => [150 + (lon - 26) * 85, 140 + (42.2 - lat) * 125];
const A5_ANA = [[29.1, 41.2], [30, 41.15], [31.4, 41.3], [32.6, 41.85], [33.5, 42], [34.9, 42.05], [35.2, 41.7], [36.3, 41.35], [37.5, 41.1], [38.4, 40.95], [39.7, 41], [40.6, 41.05], [41.5, 41.5], [42.8, 41.5], [43.5, 41.1], [43.6, 40.1], [44.8, 39.7], [44.2, 39], [44.3, 38.4], [44.8, 37.2], [42.4, 37.1], [40.5, 37], [38.2, 36.9], [36.6, 36.8], [36.2, 36.6], [35.9, 36.85], [35.3, 36.6], [34.6, 36.8], [33.6, 36.15], [32.5, 36.1], [31, 36.8], [30.5, 36.4], [29.6, 36.2], [28.3, 36.75], [27.4, 37], [27.2, 37.9], [26.3, 38.3], [26.9, 38.75], [26.8, 39.4], [26.1, 39.5], [26.2, 40], [27, 40.4], [28, 40.4], [29, 40.95]];
const A5_TEL = { ankara: [32.85, 39.93], sivas: [37, 39.75], erzurum: [41.27, 39.9], samsun: [36.33, 41.29], kayseri: [35.48, 38.73], konya: [32.48, 37.87], eskisehir: [30.52, 39.78], amasya: [35.83, 40.65], trabzon: [39.72, 41], diyarbakir: [40.2, 37.9], adana: [35.3, 37] };
const A5_LINES = [['ankara', 'sivas'], ['sivas', 'erzurum'], ['ankara', 'eskisehir'], ['ankara', 'konya'], ['ankara', 'kayseri'], ['sivas', 'amasya'], ['amasya', 'samsun'], ['erzurum', 'trabzon'], ['sivas', 'diyarbakir'], ['kayseri', 'adana']];
shot(A5_M()[6], (ctx, st) => { // örgütlenmeyi: Anadolu'da yanıp sönen telgraf hatları (dönemin örgütlenme aracı)
  setReg(71); const t = st.t, lt = st.lt;
  paperBG(ctx); plate(ctx, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .6 }); // mantar pano okrası
  const z = 1.02 + lt * .03; ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  const land = PL(rough(A5_ANA.map(([a, b]) => A5_LL(a, b)), 1.2, 71)); knock(ctx, land); plate(ctx, 'ochre', land, { a: .35 }); inkStroke(ctx, land, 3.4);
  A5_LINES.forEach(([a, b], i) => {
    const [x0, y0] = A5_LL(...A5_TEL[a]), [x1, y1] = A5_LL(...A5_TEL[b]), k = E.out3(ramp(lt, i * .08, i * .08 + .35)); if (k <= 0) return;
    ctx.save(); ctx.setLineDash([14, 8]); inkStroke(ctx, PL([[x0, y0], [x0 + (x1 - x0) * k, y0 + (y1 - y0) * k]], false), 4.4); ctx.restore();
    if (k >= 1) { const u = ((Math.floor(t * 15) / 15) * .9 + i * .23) % 1, pl = new Path2D(); pl.arc(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 10, 0, TAU); knock(ctx, pl, '#F6EBD0'); inkStroke(ctx, pl, 2); }
  });
  for (const [k, ll] of Object.entries(A5_TEL)) { const [x, y] = A5_LL(...ll), on = Math.floor(t * 6 + x * .01) % 3 !== 0, c = new Path2D(); c.arc(x, y, k === 'ankara' ? 18 : 12, 0, TAU); knock(ctx, c, on ? '#F6EBD0' : P.paper); if (on) plate(ctx, 'gold', c, { a: .5 }); inkStroke(ctx, c, 2.6); }
  ctx.restore();
  const [ax, ay] = A5_LL(...A5_TEL.ankara); label(ctx, 'ANKARA', ax * z + (1 - z) * W / 2 - 60, ay * z + (1 - z) * H / 2 - 30, FONT.mono(40), { align: 'right' });
}, { tr: { type: 'cut', dur: .01 } });
shot(A5_M()[7], (ctx, st) => { // birbirine güvenmeyi: siperde omuz omuza, bir el ötekinin omzunda
  setReg(73); const t = st.t, lt = st.lt;
  paperBG(ctx); plate(ctx, 'khaki', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .3 });
  a5_sky(ctx, [['ochre', .25, 420]]);
  const z = 1 + lt * .02; ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  const A = { x: 760, y: 420, s: 1.7, dir: 1 }, B = { x: 1150, y: 410, s: 1.7, dir: 1 };
  bust(ctx, { ...B, coat: 'setre', col: 'khaki', w: .95, seed: 4, len: 420, back: true, arms: 'back' });
  head3q(ctx, { ...B, who: 'anon', id: { seed: 44, mus: 'gur' }, gear: 'kalpak', light: 'front', look: [1, -.1], age: 32 });
  bust(ctx, { ...A, coat: 'setre', col: 'khaki', w: .95, seed: 2, len: 420, sep: true });
  head3q(ctx, { ...A, who: 'anon', id: { seed: 42 }, gear: 'kalpak', light: 'front', look: [1, -.1], age: 30 });
  const ar = arm(ctx, [850, 620], [1040, 600], { upper: 120, fore: 115, w: 62, col: 'khaki', bend: -1 });
  handDraw(ctx, ar.wr[0], ar.wr[1], ar.ang + .3, ar.w2 / 20, 'rest', { side: 1 });
  const sand = PL([[-20, 900], [W + 20, 880], [W + 20, H + 20], [-20, H + 20]]); knock(ctx, sand); plate(ctx, 'ochre', sand, { n: 2 }); inkStroke(ctx, PL([[-20, 900], [W + 20, 880]], false), 4);
  ctx.restore();
}, { tr: { type: 'cut', dur: .01 } });

// F06 · "Kuşak hazırdı": A05 dizilişindeki yedi kişi eşit aralıkta, Mustafa Kemal ortada ve aynı ölçekte; önde uzun okul sırası
// (1893 sınıfı ve "AYNI SIRADA" kapağıyla kafiye). "onu"da Mustafa Kemal ortadaki boşluğa basılır, "birleştiren"de başlar şafağa döner,
// "mustafa"da kamera merkeze ≤%7 yaklaşır. Hale yok: şafak ışığı karenin sağ kenarında, başlardan uzak.
const A5_SEVEN = [['halide', 'basortu', 'setre', 'khaki', 38], ['karabekir', 'kalpak', 'kaput', 'khaki', 40], ['alifuat', 'kalpak', 'kaput', 'khaki', 40], ['mk', 'kalpak', 'kaput', 'khaki', 41], ['ismet', 'kalpak', 'kaput', 'khaki', 38], ['fevzi', 'kalpak', 'kaput', 'khaki', 46], ['rauf', 'fes', 'civil', 'navy', 41]] // Rauf fesli: Sivas, Eylül 1919 fotoğrafı (tarih danışmanı; madalyon ve öteki dizilerle tutarlı);
shot(S('F06') - .25, (ctx, st) => {
  setReg(75); const t = st.t, lt = st.lt;
  paperBG(ctx);
  a5_sky(ctx, [['ochre', .45, 300], ['ochre', .25, 560]]);
  for (const [x0, a] of [[1460, .1], [1640, .12], [1800, .14]]) plate(ctx, 'gold', PL(rough([[x0, -20], [W + 20, -20], [W + 20, 840], [x0 - 300, 840]], 1.2, x0)), { a }); // şafak sağ üstten, eğik basamaklı ışık
  const join = ramp(t, Wd('F06', 'onu') - .1, Wd('F06', 'onu') + .5, E.io3);
  const turn = ramp(t, Wd('F06', 'birleştiren') - .1, Wd('F06', 'birleştiren') + .3);
  const zz = 1 + .07 * E.io2(ramp(t, Wd('F06', 'mustafa') - .1, Se('F06') + .2));
  ctx.save(); ctx.translate(960, 520); ctx.scale(zz, zz); ctx.translate(-960, -520);
  const tf = Math.floor(t * 15) / 15, y = 470, s = 1.0;
  A5_SEVEN.forEach(([who, gear, coat, col, age], i) => {
    const isMK = who === 'mk'; if (isMK && join <= 0) return;
    const x = 960 + (i - 3) * 226, id = idleOffsets(tf, i + 3, .6);
    // önce ortadaki boşluğa (sonra Mustafa Kemal'e), "birleştiren"de şafağa bakarlar
    const tdh = Wd('F06', 'deha'), rank = Math.abs(i - 3);
    const atMK = !isMK && tf > tdh + rank * .08, look = atMK ? [960, 430] : turn >= 1 ? [2200, 380] : [960, 420];
    ctx.save(); if (isMK) { ctx.globalAlpha = join; REG.boost = 1 + 4 * (1 - join); }
    bust(ctx, { x, y, s, dir: 1, coat, col, w: .92, seed: i + 7, len: 420, turn: .2, sep: i > 0 ? 'L' : false, arms: 'back' });
    // "dehası"nda sağdakiler başlarını Mustafa Kemal'e çevirir, soldakiler hafifçe ona eğilir
    const hd = atMK && i > 3 ? -1 : 1, lean = atMK ? (i < 3 ? .05 : -.05) : 0;
    head3q(ctx, { x: x - (hd < 0 ? 12 * s : 0), y, s, dir: hd, who, gear, gearCol: who === 'fevzi' ? 'grey' : undefined, light: 'front', lookAt: look, age, tilt: (id.head || 0) * .5 + lean, blink: blinkAt(t, i * 3 + 1) });
    REG.boost = 1; ctx.restore();
  });
  // uzun okul sırası (figürlerin önünde)
  const desk = PL(rough([[-40, 822], [W + 40, 812], [W + 40, H + 20], [-40, H + 20]], 1, 77)); knock(ctx, desk); plate(ctx, 'ochre', desk); plate(ctx, 'sepia', desk, { a: .55 });
  inkStroke(ctx, PL([[-40, 822], [W + 40, 812]], false), 6); inkStroke(ctx, PL([[-40, 858], [W + 40, 848]], false), 2.4, { a: .6 });
  for (let i = 0; i < 9; i++) cut(ctx, PL([[60 + i * 220, 900], [190 + i * 220, 898]], false), 2.2, { a: .35 });
  ctx.restore();
  const ka = env(lt, .2, .6) * (1 - join);
  if (ka > 0 && !NOTEXT) { ctx.save(); ctx.globalAlpha = ka; ctx.font = FONT.title(80); const tw = ctx.measureText('KUŞAK HAZIRDI').width; const bd = PL(rough([[96, 922], [156 + tw, 922], [156 + tw, 1020], [96, 1020]], .8, 9)); knock(ctx, bd); inkStroke(ctx, bd, 2.6); ctx.restore(); }
  label(ctx, 'KUŞAK HAZIRDI', 126, 1000, FONT.title(80), { a: ka });
}, { tr: { type: 'press', dur: .6 } });
