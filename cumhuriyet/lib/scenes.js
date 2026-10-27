// İnceleme sahneleri (?scene=...): üslup karesi, yaş şeridi
'use strict';
const SCENES = {};

// İsim levhası: kâğıt etiket, is çerçeve; ad (Abril Fatface) + yaş (Courier Prime)
function nameplate(ctx, x, y, name, sub, o = {}) {
  ctx.save(); ctx.font = `400 ${o.size || 44}px "Abril Fatface"`; ctx.letterSpacing = '1px';
  const w1 = ctx.measureText(name).width; ctx.font = `700 ${o.sub || 30}px "Courier Prime"`; const w2 = ctx.measureText(sub).width; ctx.restore();
  const w = Math.max(w1, w2) + 44, h = (o.size || 44) + (o.sub || 30) + 34;
  const x0 = o.align === 'center' ? x - w / 2 : x;
  plate(ctx, 'ink', PL([[x0 + 7, y + 9], [x0 + w + 7, y + 9], [x0 + w + 7, y + h + 9], [x0 + 7, y + h + 9]]), { a: .35 });
  const box = PL(rough([[x0, y], [x0 + w, y], [x0 + w, y + h], [x0, y + h]], .8, name.length));
  knock(ctx, box); inkStroke(ctx, box, 3.2);
  plate(ctx, o.accent || 'red', PL([[x0, y + h - 7], [x0 + w, y + h - 7], [x0 + w, y + h], [x0, y + h]]));
  txt(ctx, name, x0 + 22, y + 14 + (o.size || 44) * .78, `400 ${o.size || 44}px "Abril Fatface"`, { ls: 1 });
  txt(ctx, sub, x0 + 22, y + 22 + (o.size || 44) + (o.sub || 30) * .7, `700 ${o.sub || 30}px "Courier Prime"`);
}

// Üslup karesi: Alagöz karargâhı, Sakarya, Eylül 1921 akşamı
SCENES.alagoz = (ctx, t) => {
  setReg(21, 1);
  paperBG(ctx);
  // —— duvar: okra kalıbı + lamba halesi (is yarım tonu dışa doğru koyulaşır)
  const wall = PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]);
  plate(ctx, 'ochre', wall, { a: .55 });
  // tavan kirişi
  const beam = PL(rough([[-20, 0], [W + 20, 0], [W + 20, 58], [-20, 64]], 1.5, 3));
  plate(ctx, 'ochre', beam); plate(ctx, 'ink', beam, { a: .5 }); inkStroke(ctx, PL([[-20, 64], [W + 20, 58]], false), 4);
  for (let i = 0; i < 6; i++) { const yy = 12 + i * 8; cut(ctx, SP([[-20, yy], [600, yy + 2], [1300, yy - 1], [W + 20, yy + 1]], false), 1.4, { a: .3 }); }
  // —— pencere (sağda): alacakaranlık, Sakarya sırtları, kağnılar ve kadınlar
  const wx0 = 1610, wx1 = 1870, wy0 = 150, wy1 = 560;
  const win = PL([[wx0, wy0], [wx1, wy0], [wx1, wy1], [wx0, wy1]]);
  knock(ctx, win);
  ctx.save(); ctx.clip(win);
  radialHT(ctx, 'ochre', 1740, 470, 30, 380, .12, .62, { cell: 11, box: [wx0, wy0, wx1, wy1], sy: .6 });
  const far = SP([[wx0 - 10, 452], [1660, 432], [1720, 440], [1780, 424], [1840, 436], [wx1 + 10, 430], [wx1 + 10, wy1 + 10], [wx0 - 10, wy1 + 10]], true, .7);
  plate(ctx, 'khaki', far, { a: .6 });
  const near = SP([[wx0 - 10, 486], [1680, 470], [1760, 478], [1830, 462], [wx1 + 10, 470], [wx1 + 10, wy1 + 10], [wx0 - 10, wy1 + 10]], true, .7);
  plate(ctx, 'khaki', near); plate(ctx, 'khaki', near, { a: .5 });
  // sırtta damga siluetler: soldan sağa küçülen kafile
  const ph = Math.floor(t * 6) % 2;
  const caravan = [['w', 1640, 470, 1.0], ['c', 1690, 470, .62], ['w', 1712, 472, .9], ['c', 1752, 474, .54], ['w', 1772, 474, .78], ['w', 1790, 471, .74], ['c', 1822, 466, .46], ['w', 1840, 467, .64], ['w', 1856, 468, .6]];
  for (const [k, x, y, sc] of caravan) k === 'c' ? stampOxcart(ctx, x, y, sc, ph) : stampWoman(ctx, x, y, sc * .9, ph);
  ctx.restore();
  // çerçeve
  const frame = new Path2D(); frame.rect(wx0 - 22, wy0 - 22, wx1 - wx0 + 44, wy1 - wy0 + 44); frame.rect(wx0, wy0, wx1 - wx0, wy1 - wy0);
  ctx.save(); ctx.fillStyle = 'rgba(0,0,0,0)'; ctx.restore();
  const fr = new Path2D(); fr.rect(wx0 - 22, wy0 - 22, wx1 - wx0 + 44, 22); fr.rect(wx0 - 22, wy1, wx1 - wx0 + 44, 26); fr.rect(wx0 - 22, wy0, 22, wy1 - wy0); fr.rect(wx1, wy0, 22, wy1 - wy0);
  fr.rect((wx0 + wx1) / 2 - 7, wy0, 14, wy1 - wy0); fr.rect(wx0, 330, wx1 - wx0, 12);
  knock(ctx, fr); plate(ctx, 'ochre', fr, { n: 2 }); plate(ctx, 'ink', fr, { a: .25 }); inkStroke(ctx, fr, 3);
  // —— kurmay haritası (duvarda, hafif eğik)
  const map = staffMap(ctx, { x: 110, y: 112, w: 760, rot: -.021, front: 1, arrows: 1 });
  // —— lamba halesi: duvarda ve haritada is yarım tonu, merkez açık (odak: haritadaki cephe noktası)
  const F = map.toWorld(640, 330); // İsmet'in gösterdiği nokta (Duatepe önü)
  radialHT(ctx, 'ink', F[0] + 120, F[1] - 60, 330, 1250, 0, .34, { cell: 14, ang: 45, box: [-20, 60, W + 20, 860], sx: 1.2 });
  gasLamp(ctx, 760, 150, 1.0, t);
  // —— kişiler (arkadan öne): Fevzi, Mustafa Kemal, İsmet
  // Fevzi: sağda, telgrafname elinde, haritaya bakıyor
  const fz = { x: 1478, y: 338, s: 1.18, dir: -1 };
  bust(ctx, { ...fz, coat: 'kaput', col: 'khaki', w: 1.02, seed: 7, len: 460 });
  head3q(ctx, { ...fz, who: 'fevzi', gear: 'kalpak', gearCol: 'grey', light: 'front', look: [2.2, .9], age: 45 });
  const tg = [1428, 655];
  paperSheet(ctx, tg[0], tg[1], 170, 128, .08, 13, { header: true });
  handDraw(ctx, tg[0] - 92, tg[1] + 6, -.15, 1.25, 'hold', { side: 1 });
  handDraw(ctx, tg[0] + 92, tg[1] + 16, PI + .1, 1.25, 'hold', { side: -1 });
  // Mustafa Kemal: ortada, ¾ haritaya dönük, yüzü lamba ışığında; masaya yaslanan el
  const mk = { x: 1188, y: 300, s: 1.3, dir: -1 };
  bust(ctx, { ...mk, coat: 'kaput', col: 'khaki', w: 1.04, seed: 3, len: 440 });
  head3q(ctx, { ...mk, who: 'mk', gear: 'kalpak', gearCol: 'ink', light: 'front', look: [2.4, 1.1], age: 40 });
  // İsmet: haritanın yanında, kısa boylu; parmağıyla cephe hattını gösteriyor
  const is = { x: 930, y: 372, s: 1.16, dir: -1 };
  bust(ctx, { ...is, coat: 'kaput', col: 'khaki', w: .96, seed: 5, len: 440 });
  head3q(ctx, { ...is, who: 'ismet', gear: 'kalpak', gearCol: 'ink', light: 'front', look: [2.6, .2], age: 36 });
  const isArm = arm(ctx, [862, 476], [F[0] + 60, F[1] + 24], { upper: 155, fore: 145, w: 50, col: 'khaki', bend: 1 });
  handDraw(ctx, isArm.wr[0], isArm.wr[1], isArm.ang, 1.15, 'point', { side: -1 });
  // —— ön masa: dürbün, pusula, evrak
  woodTable(ctx, 836);
  paperSheet(ctx, 760, 920, 200, 130, -.06, 21, { rows: 5 });
  compass(ctx, 960, 950, 50);
  binoculars(ctx, 1330, 912, 1.25, .08);
  // —— yazılar: bölüm başlığı (sol alt), yer/tarih damgası, isim levhaları
  // bölüm başlığı: kâğıt künye kutusu (masanın önünde, okunur)
  const cap = PL(rough([[76, 868], [640, 868], [640, 1040], [76, 1040]], 1, 9));
  plate(ctx, 'ink', PL([[86, 880], [650, 880], [650, 1052], [86, 1052]]), { a: .4 });
  knock(ctx, cap); inkStroke(ctx, cap, 3.6); inkStroke(ctx, PL([[88, 880], [628, 880], [628, 1028], [88, 1028]]), 1.4);
  txt(ctx, 'V · ANADOLU', 110, 960, '400 80px "Abril Fatface"', { ls: 2 });
  plate(ctx, 'red', PL([[112, 976], [604, 976], [604, 983], [112, 983]]));
  txt(ctx, 'ALAGÖZ · EYLÜL 1921', 112, 1016, '700 30px "Courier Prime"', { ls: 3 });
  nameplate(ctx, 900, 736, 'İSMET', '36 yaşında', { align: 'center', size: 38, sub: 26 });
  nameplate(ctx, 1190, 736, 'MUSTAFA KEMAL', '40 yaşında', { align: 'center', size: 38, sub: 26 });
  nameplate(ctx, 1490, 736, 'FEVZİ', '45 yaşında', { align: 'center', size: 38, sub: 26 });
  pressFinish(ctx, t, {});
};

// Yaş şeridi: aynı baş modülüyle Mustafa Kemal'in beş dönemi
SCENES.yas = (ctx, t) => {
  setReg(5, 1);
  paperBG(ctx);
  const stages = [
    { age: 18, gear: 'fes', coat: 'setre', col: 'navy', lab: 'HARBİYE · 1899' },
    { age: 30, gear: 'kabalak', coat: 'setre', col: 'khaki', lab: 'DERNE · 1911' },
    { age: 34, gear: 'kabalak', coat: 'setre', col: 'khaki', lab: 'ARIBURNU · 1915' },
    { age: 40, gear: 'kalpak', coat: 'kaput', col: 'khaki', lab: 'SAKARYA · 1921' },
    { age: 42, gear: null, coat: 'civil', col: 'ink', lab: 'ÇANKAYA · 1923' },
  ];
  // kuşak şeridi zemini
  plate(ctx, 'ochre', PL([[0, 170], [W, 170], [W, 760], [0, 760]]), { a: .55 });
  stages.forEach((st, i) => {
    const x = 210 + i * 375, y = 420;
    const o = { x, y, s: 1.32, dir: -1 };
    bust(ctx, { ...o, coat: st.coat, col: st.col, w: .98, seed: 3, len: 250 });
    head3q(ctx, { ...o, who: 'mk', gear: st.gear, gearCol: 'ink', light: 'front', look: [2.2, .6], age: st.age });
    txt(ctx, String(st.age), x, 880, '400 96px "Abril Fatface"', { align: 'center' });
    txt(ctx, st.lab, x, 940, '700 30px "Courier Prime"', { align: 'center', ls: 2 });
  });
  inkStroke(ctx, PL([[0, 170], [W, 170]], false), 4); inkStroke(ctx, PL([[0, 760], [W, 760]], false), 4);
  txt(ctx, 'AYNI YÜZ, BEŞ DÖNEM', W / 2, 110, '400 64px "Abril Fatface"', { align: 'center', ls: 2 });
  pressFinish(ctx, t, {});
};

// Yüz inceleme: üç baş büyük ölçekte
SCENES.heads = (ctx, t) => {
  setReg(5, 1); paperBG(ctx);
  plate(ctx, 'ochre', PL([[0, 0], [W, 0], [W, H], [0, H]]), { a: .45 });
  const L = [['mk', 'kalpak', 'ink', 40], ['ismet', 'kalpak', 'ink', 36], ['fevzi', 'kalpak', 'grey', 45]];
  L.forEach(([who, gear, gc, age], i) => {
    const o = { x: 330 + i * 630, y: 470, s: 3.2, dir: -1 };
    bust(ctx, { ...o, coat: 'kaput', col: 'khaki', w: 1, seed: 3, len: 200 });
    head3q(ctx, { ...o, who, gear, gearCol: gc, light: 'front', look: [2.2, .6], age });
  });
  pressFinish(ctx, t, {});
};
