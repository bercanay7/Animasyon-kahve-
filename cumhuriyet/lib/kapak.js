// YouTube kapakları (1920×1080 çizilir, 1280×720 dışa aktarılır): ?scene=kapakA | kapakB
// Kurallar (CLAUDE.md kapak dersleri): ¾ yüz, tek odak = karenin en parlak noktası, büyük harf yüksekliği ≥ %18,
// figürlere ≥30 px boşluk, sağ alt köşe (süre rozeti) boş, videonun üslubu.
'use strict';
function kp_title(ctx, lines, x, y, size, o = {}) {
  lines.forEach((s, i) => {
    const yy = y + i * size * 1.02;
    // kâğıt çerçeve (okunurluk): harflerin altına kalın kâğıt konturu
    ctx.save(); ctx.font = FONT.slab(size); ctx.textAlign = o.align || 'left'; ctx.lineJoin = 'round';
    ctx.lineWidth = size * .16; ctx.strokeStyle = o.halo || P.paper; ctx.strokeText(s, x, yy); ctx.restore();
    txt(ctx, s, x, yy, FONT.slab(size), { align: o.align || 'left', col: (o.cols && o.cols[i]) || P.ink });
  });
}
SCENES.kapakA = (ctx, t) => {
  setReg(81, 1.4); paperBG(ctx);
  plate(ctx, 'ochre', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .55 });
  // sağda kara tahta ve sıradaki fesli öğrenciler (1890'lar), sepya ve küçük
  const bb = PL(rough([[980, 560], [1860, 560], [1860, 820], [980, 820]], 1.5, 3)); knock(ctx, bb, '#34302C'); inkStroke(ctx, bb, 6);
  inkStroke(ctx, (() => { const p = new Path2D(); p.arc(1150, 690, 70, 0, TAU); p.moveTo(1080, 690); p.lineTo(1220, 690); return p; })(), 3, { col: '#E8E0CE' });
  for (let i = 0; i < 3; i++) {
    const o = { x: 1180 + i * 210, y: 760, s: .95, dir: -1 };
    bust(ctx, { ...o, coat: 'setre', col: 'navy', w: .88, seed: i + 2, len: 260, sep: true });
    head3q(ctx, { ...o, who: i === 0 ? 'ismet' : i === 1 ? 'mk' : 'alifuat', gear: 'fes', light: 'front', look: [1, .3], age: i === 1 ? 14 : 13 });
  }
  const desk = PL([[960, 930], [1900, 916], [1900, 1100], [960, 1100]]); knock(ctx, desk); plate(ctx, 'ochre', desk, { n: 2 }); plate(ctx, 'sepia', desk, { a: .5 }); inkStroke(ctx, PL([[960, 930], [1900, 916]], false), 5);
  // solda büyük ¾ Mustafa Kemal (40): kalpak, kaput; yüz karenin en parlak yeri (ten kalıbı)
  const mk = { x: 520, y: 470, s: 3.0, dir: 1 };
  bust(ctx, { ...mk, coat: 'kaput', col: 'khaki', w: .95, seed: 3, len: 260, sep: true, arms: 'back', skin: true });
  head3q(ctx, { ...mk, who: 'mk', gear: 'kalpak', gearCol: 'ink', light: 'front', look: [1.2, .2], age: 40, skin: true });
  // yazı
  kp_title(ctx, ['AYNI', 'SIRADAN'], 880, 250, 178);
  plate(ctx, 'red', PL([[904, 474], [1860, 474], [1860, 488], [904, 488]]), { flat: true });
  pressFinish(ctx, t, { grain: 0 });
};
SCENES.kapakB = (ctx, t) => {
  setReg(83, 1.4); paperBG(ctx);
  plate(ctx, 'navy', PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), { a: .82 });
  // arkada Abdülhamid'in büyük, koyu silueti (fes ve sakal; yüz seçilmez)
  ctx.save();
  const ah = { x: 1460, y: 520, s: 4.2, dir: -1 };
  bust(ctx, { ...ah, coat: 'setre', col: 'ink', w: 1.0, seed: 21, len: 200 });
  head3q(ctx, { ...ah, who: 'abdulhamid', gear: 'fes', light: 'back', look: [1, .3], age: 60 });
  plate(ctx, 'navy', PL([[900, -20], [W + 20, -20], [W + 20, H + 20], [900, H + 20]]), { a: .75 });
  ctx.restore();
  // önde kadro: MK (¾, en parlak), arkasında İsmet ve Fevzi
  for (const p of [{ who: 'fevzi', x: 760, y: 560, s: 1.6, age: 45, gc: 'grey', back: true }, { who: 'ismet', x: 300, y: 600, s: 1.6, age: 36, gc: 'ink', back: true }]) {
    bust(ctx, { x: p.x, y: p.y, s: p.s, dir: 1, coat: 'kaput', col: 'khaki', w: .95, seed: p.age, len: 400, back: true, arms: 'back' });
    head3q(ctx, { x: p.x, y: p.y, s: p.s, dir: 1, who: p.who, gear: 'kalpak', gearCol: p.gc, light: 'front', look: [1, .1], age: p.age });
  }
  const mk = { x: 560, y: 520, s: 2.5, dir: 1 };
  bust(ctx, { ...mk, coat: 'kaput', col: 'khaki', w: .95, seed: 3, len: 300, sep: true, arms: 'back', skin: true });
  head3q(ctx, { ...mk, who: 'mk', gear: 'kalpak', gearCol: 'ink', light: 'front', look: [1.2, .1], age: 40, skin: true });
  kp_title(ctx, ['SULTANIN', 'ÖĞRENCİLERİ'], 1880, 230, 150, { align: 'right', halo: P.navy, cols: [P.paper, P.paper] });
  plate(ctx, 'red', PL([[1110, 410], [1880, 410], [1880, 424], [1110, 424]]), { flat: true });
  pressFinish(ctx, t, { grain: 0 });
};

// ---- 2. tur (kapak kurulu): A′ "AYNI SIRADA", B′ "SULTANIN OKULU", C "AYNI OKULDAN" ----
// Mustafa Kemal'in yüzü karenin en parlak görüntü öğesi (L≥200): yalnız onun için açık kâğıt + açık ten; arkasına ışık yok
function kp_bright(fn, pap = '#FBF4E4', skn = '#F6D8BA') { const ps = P.paper, sk = P.skin; P.paper = pap; P.skin = skn; try { fn(); } finally { P.paper = ps; P.skin = sk; } }
// ikinci plan figürleri ayrı katmanda çizilip koyulaştırılır (yüzler L≈140)
const kpLayer = makeCanvas(DW, DH), kpLx = kpLayer.getContext('2d');
function kp_dim(ctx, k, fn, sat = 1) {
  kpLx.setTransform(1, 0, 0, 1, 0, 0); kpLx.clearRect(0, 0, DW, DH); baseT(kpLx); fn(kpLx);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.filter = `brightness(${k}) saturate(${sat})`; ctx.drawImage(kpLayer, 0, 0); ctx.restore();
}
function kp_haze(ctx, col, a, fn) {
  kpLx.setTransform(1, 0, 0, 1, 0, 0); kpLx.clearRect(0, 0, DW, DH); baseT(kpLx); fn(kpLx);
  kpLx.save(); kpLx.setTransform(1, 0, 0, 1, 0, 0); kpLx.globalCompositeOperation = 'source-atop'; kpLx.globalAlpha = a; kpLx.fillStyle = col; kpLx.fillRect(0, 0, DW, DH); kpLx.restore();
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(kpLayer, 0, 0); ctx.restore();
}
// yazıyı kutuya sığdır: en büyük boy ≤ size, genişlik ≤ maxW
function kp_fit(ctx, s, size, maxW) { ctx.save(); ctx.font = FONT.slab(size); const w = ctx.measureText(s).width; ctx.restore(); return w > maxW ? Math.floor(size * maxW / w) : size; }
function kp_text(ctx, s, x, y, size, col, align = 'left') {
  ctx.save(); ctx.font = FONT.slab(size); ctx.textAlign = align; ctx.fillStyle = col; ctx.letterSpacing = '0px'; ctx.fillText(s, x, y); ctx.restore();
}
// üst satır (konu künyesi): kırmızı şerit + ay yıldız + "CUMHURİYET'İ KURANLAR"; sağ kenar maxR'yi geçmez
function kp_crescent(ctx, cx, cy, G, col) {
  // Türk bayrağı oranlarına yakın: dış daire 0.5G, iç daire 0.4G (0.0625G sağda), yıldız 0.25G çaplı dairede
  ctx.save(); ctx.fillStyle = col;
  const m = new Path2D(); m.arc(cx, cy, .25 * G, 0, TAU); m.arc(cx + .0625 * G, cy, .2 * G, 0, TAU, true); ctx.fill(m, 'evenodd');
  const sx = cx + .5 * G - .0625 * G, R = .125 * G, r = R * .382, st = new Path2D();
  for (let i = 0; i < 10; i++) { const a = Math.PI + i * Math.PI / 5, q = i % 2 ? r : R; i ? st.lineTo(sx + q * Math.cos(a), cy + q * Math.sin(a)) : st.moveTo(sx + q * Math.cos(a), cy + q * Math.sin(a)); }
  st.closePath(); ctx.fill(st); ctx.restore();
}
function kp_kicker(ctx, x0, y0, maxR, s = "CUMHURİYET'İ KURANLAR") {
  const h = 116, G = h * .9;
  let size = 70; ctx.save(); ctx.font = FONT.slab(size); let tw = ctx.measureText(s).width; ctx.restore();
  const room = maxR - x0 - G * .95 - 56; if (tw > room) { size = Math.floor(size * room / tw); tw = room; }
  const w = G * .95 + tw + 56;
  const band = PL(rough([[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]], 1, 9));
  knock(ctx, band, P.red);
  kp_crescent(ctx, x0 + 24 + .3 * G, y0 + h / 2, G, P.paper);
  kp_text(ctx, s, x0 + G * .95 + 28, y0 + h / 2 + size * .36, size, P.paper);
  return { w, h, size };
}
// iki satırlık künye: "CUMHURİYET'İ / KURANLAR", solda ay yıldız
function kp_kicker2(ctx, x0, y0, size = 92) {
  ctx.save(); ctx.font = FONT.slab(size); const tw = Math.max(ctx.measureText("CUMHURİYET'İ").width, ctx.measureText('KURANLAR').width); ctx.restore();
  const G = size * 1.5, pad = 30, h = size * 2.2 + pad, w = G * .9 + tw + pad * 2;
  const band = PL(rough([[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]], 1, 9));
  knock(ctx, band, P.red);
  kp_crescent(ctx, x0 + pad + .28 * G, y0 + h / 2, G, P.paper);
  kp_text(ctx, "CUMHURİYET'İ", x0 + G * .9 + pad, y0 + pad / 2 + size * .98, size, P.paper);
  kp_text(ctx, 'KURANLAR', x0 + G * .9 + pad, y0 + pad / 2 + size * 2.05, size, P.paper);
  return { w, h };
}
function kp_board(ctx, col) {
  knock(ctx, PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]), col);
}
SCENES.kapakA2 = (ctx, t) => {
  setReg(91, 1.2); paperBG(ctx);
  // bütün kare kara tahta (is, L≈58); tebeşir silinti izleri çok hafif
  kp_board(ctx, '#3A3633');
  ctx.save(); ctx.globalAlpha = .03; ctx.strokeStyle = P.paper; ctx.lineCap = 'round';
  for (let i = 0; i < 7; i++) { ctx.lineWidth = 70 + 30 * hash(i, 3); ctx.beginPath(); const y = 120 + i * 130 + 40 * hash(i, 5); ctx.moveTo(900 + 200 * hash(i, 7), y); ctx.bezierCurveTo(1200, y - 30, 1500, y + 40, 1880, y - 10); ctx.stroke(); }
  ctx.restore();
  // sağda mektep sırası, 1893 (filmde 0:19'daki sınıf, act0 A0_K93): İsmet (11), Mustafa Kemal (12, ortada), sınıf arkadaşı (13); bıyıksız, fes, lacivert setre
  kp_haze(ctx, '#3A3633', .16, g => kp_bright(() => {
    const cad = [{ who: 'ismet', id: { mus: null }, x: 1030, age: 11, look: [-1, .2] }, { who: 'anon', id: { mus: null, jaw: 1.0, WD: 1.08, seed: 31 }, x: 1550, age: 13, look: [-.9, .35] }, { who: 'mk', id: { mus: null }, x: 1295, age: 12, look: [-1.1, .1] }];
    for (const c of cad) {
      const o = { x: c.x, y: 740, s: 1.6, dir: -1 };
      bust(g, { ...o, coat: 'setre', col: 'navy', w: .9, seed: c.age + c.x, len: 300, sep: true });
      head3q(g, { ...o, who: c.who, id: c.id, gear: 'fes', light: 'front', look: c.look, age: c.age, skin: true });
    }
    // ortak sıra (ön tahtası), x ≤ 1700: süre rozeti boş kalır
    const desk = PL(rough([[880, 1004], [1700, 996], [1700, 1100], [880, 1100]], 1.2, 4)); knock(g, desk); plate(g, 'ochre', desk); plate(g, 'sepia', desk, { a: .55 });
    inkStroke(g, PL([[880, 1004], [1700, 996]], false), 6); inkStroke(g, desk, 4);
    for (const x of [1000, 1290, 1580]) cut(g, PL([[x - 60, 1046], [x + 60, 1044]], false), 2.4);
  }, '#F8F2E3', '#EFD8C2'));
  // solda büyük ¾ Mustafa Kemal (1923): kalpak, kaput; genç hâline (sıraya) bakar
  kp_bright(() => {
    const mk = { x: 470, y: 590, s: 3.0, dir: 1 };
    bust(ctx, { ...mk, y: mk.y - 8 * mk.s, coat: 'kaput', col: 'khaki', w: .95, seed: 3, len: 300, sep: true, arms: 'back', skin: true });
    head3q(ctx, { ...mk, who: 'mk', gear: 'kalpak', gearCol: 'ink', light: 'front', look: [1.3, .35], age: 42, skin: true });
  });
  // yazı: AYNI / SIRADA (Alfa Slab, büyük harf ≈ %18), kâğıt rengi, x 830–1880
  kp_kicker2(ctx, 56, 44, 86);
  const s1 = kp_fit(ctx, 'SIRADA', 264, 1110);
  kp_text(ctx, 'AYNI', 1880, 250, s1, P.paper, 'right');
  kp_text(ctx, 'SIRADA', 1880, 490, s1, P.paper, 'right');
  pressFinish(ctx, t, { grain: 0, vig: .5, stone: .12 });
};
function kp_cadre(ctx, o = {}) {
  // arkada İsmet (36) ve Fevzi (45): aynı ten ailesi (L* ≈67), derinlik %12 lacivert pusla; ölçek 2.0, omuzları Mustafa Kemal'le örtüşür
  kp_haze(ctx, '#2E3D58', o.haze ?? .12, g => kp_bright(() => {
    for (const p of [{ who: 'fevzi', x: 800, y: 560, age: 45, gc: 'grey' }, { who: 'ismet', x: 290, y: 600, age: 36, gc: 'ink' }]) {
      bust(g, { x: p.x, y: p.y, s: 2.0, dir: 1, coat: 'kaput', col: 'khaki', w: .95, seed: p.age, len: 420, back: true, arms: 'back', skin: true });
      head3q(g, { x: p.x, y: p.y, s: 2.0, dir: 1, who: p.who, gear: 'kalpak', gearCol: p.gc, light: 'front', look: [1, .1], age: p.age, skin: true });
    }
  }, o.pap ?? '#F7F0DF', o.skn ?? '#F2D2B1'));
  kp_bright(() => {
    const mk = { x: 560, y: 540, s: 2.5, dir: 1 };
    bust(ctx, { ...mk, y: mk.y - 8 * mk.s, coat: 'kaput', col: 'khaki', w: .95, seed: 3, len: 360, sep: false, arms: 'back', skin: true });
    head3q(ctx, { ...mk, who: 'mk', gear: 'kalpak', gearCol: 'ink', light: 'front', look: [1.2, .1], age: 42, skin: true });
  });
}
SCENES.kapakB2 = (ctx, t) => {
  setReg(93, 1.2); paperBG(ctx);
  kp_board(ctx, '#2E3D58');
  // Abdülhamid: küçük, nötr ışık, sağ altta; başı Mustafa Kemal'inkinin ≈ %76'sı
  kp_dim(ctx, .76, g => {
    const ah = { x: 1420, y: 700, s: 1.9, dir: -1 };
    bust(g, { ...ah, coat: 'setre', col: 'ink', w: 1.0, seed: 21, len: 380 });
    head3q(g, { ...ah, who: 'abdulhamid', gear: 'fes', light: 'front', look: [-1, .2], age: 60 });
  });
  kp_cadre(ctx);
  kp_kicker2(ctx, 56, 44, 86);
  kp_text(ctx, 'SULTANIN', 1880, 190, kp_fit(ctx, 'SULTANIN', 150, 900), P.paper, 'right');
  kp_text(ctx, 'OKULU', 1880, 450, kp_fit(ctx, 'OKULU', 264, 940), P.paper, 'right');
  pressFinish(ctx, t, { grain: 0, vig: .5, stone: .12 });
};
SCENES.kapakC = (ctx, t) => {
  setReg(95, 1.2); paperBG(ctx);
  kp_board(ctx, '#2E3D58');
  // sağ altta Mekteb-i Harbiye cephesi (koyu, düşük karşıtlık): uzun neoklasik bina, alınlık, kemerli pencere sıraları
  {
    const x0 = 980, x1 = 1700, y0 = 800, y1 = 1100;
    const sil = PL([[x0, y0], [1270, y0], [1270, y0 - 30], [1340, y0 - 92], [1410, y0 - 30], [1410, y0], [x1, y0], [x1, y1], [x0, y1]]);
    knock(ctx, sil, '#1E2839'); inkStroke(ctx, sil, 3, { a: .5 });
    for (let r = 0; r < 2; r++) for (let i = 0; i < 12; i++) {
      const x = x0 + 40 + i * 57, y = y0 + 46 + r * 110;
      const win = new Path2D(); win.moveTo(x, y + 62); win.lineTo(x, y + 13); win.arc(x + 13, y + 13, 13, Math.PI, 0); win.lineTo(x + 26, y + 62); win.closePath(); knock(ctx, win, '#33435F');
    }
    for (let i = 0; i < 5; i++) knock(ctx, PL([[1290 + i * 24, y0 - 4], [1300 + i * 24, y0 - 4], [1300 + i * 24, y0 + 300], [1290 + i * 24, y0 + 300]]), '#28344B');
  }
  kp_cadre(ctx);
  kp_text(ctx, 'AYNI', 1880, 300, kp_fit(ctx, 'AYNI', 264, 940), P.paper, 'right');
  kp_text(ctx, 'OKULDAN', 1880, 520, kp_fit(ctx, 'OKULDAN', 250, 900), P.paper, 'right');
  pressFinish(ctx, t, { grain: 0, vig: .5, stone: .12 });
};
