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

// Üslup karesi: Alagöz karargâhı, Sakarya, Eylül 1921 akşamı (filmde de kullanılır: o.captions=false)
SCENES.alagoz = (ctx, t) => { alagozScene(ctx, t, { captions: true }); pressFinish(ctx, t, {}); };
function alagozScene(ctx, t, o = {}) {
  setReg(21);
  paperBG(ctx);
  const wx0 = 1610, wx1 = 1870, wy0 = 150, wy1 = 560;
  const win = PL([[wx0, wy0], [wx1, wy0], [wx1, wy1], [wx0, wy1]]);
  // —— duvar: okra; lamba halesi duvarda (pencere hariç): içte altın, dışta sepya yarım ton
  const wall = PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]);
  plate(ctx, 'ochre', wall, { a: .38 });
  const L0 = [970, 112];
  const wallOnly = new Path2D(); wallOnly.rect(-20, 60, W + 40, 800); wallOnly.rect(wx0 - 22, wy0 - 22, wx1 - wx0 + 44, wy1 - wy0 + 48);
  // lamba ışığı: düz altın halkalar (yarım ton değil); dışta sepya yarım ton, başların çevresi ve harita hariç
  for (const [r, a] of [[150, .16], [95, .3]]) { const g = new Path2D(); g.ellipse(L0[0], L0[1] + 10, r * 1.15, r * .8, 0, 0, TAU); plate(ctx, 'gold', g, { a }); } // yalnız lambanın çevresi (başların arkasında ışık yok)
  const htClip = new Path2D(); htClip.rect(-20, 60, W + 40, 800); htClip.rect(wx0 - 22, wy0 - 22, wx1 - wx0 + 44, wy1 - wy0 + 48);
  for (const [hx, hy] of [[940, 300], [1150, 270], [1430, 290]]) htClip.ellipse(hx, hy, 210, 210, 0, 0, TAU);
  ctx.save(); ctx.clip(htClip, 'evenodd');
  radialHT(ctx, 'sepia', L0[0], L0[1] + 140, 140, 1100, 0, .18, { cell: 11, box: [-20, 60, W + 20, 860], sx: 1.25 });
  ctx.restore();
  // tavan kirişi
  const beam = PL(rough([[-20, 0], [W + 20, 0], [W + 20, 58], [-20, 64]], 1.5, 3));
  plate(ctx, 'ochre', beam); plate(ctx, 'ink', beam, { a: .45 }); inkStroke(ctx, PL([[-20, 64], [W + 20, 58]], false), 4);
  for (let i = 0; i < 6; i++) { const yy = 12 + i * 8; cut(ctx, SP([[-20, yy], [600, yy + 2], [1300, yy - 1], [W + 20, yy + 1]], false), 1.4, { a: .3 }); }
  // —— pencere: düz gök bantları, ufuk açık; sırtta kafile (2 kağnı, 3 kadın)
  knock(ctx, win);
  ctx.save(); ctx.clip(win);
  plate(ctx, 'gold', PL([[wx0, wy0], [wx1, wy0], [wx1, 300], [wx0, 300]]), { a: .55 });
  plate(ctx, 'ochre', PL([[wx0, wy0], [wx1, wy0], [wx1, 300], [wx0, 300]]), { a: .3 });
  plate(ctx, 'ochre', PL([[wx0, 300], [wx1, 300], [wx1, 418], [wx0, 418]]), { a: .5 });
  plate(ctx, 'gold', PL([[wx0, 418], [wx1, 418], [wx1, 452], [wx0, 452]]), { a: .25 });
  const ridgeP = SP([[wx0 - 10, 508], [1680, 500], [1760, 506], [1840, 498], [wx1 + 10, 502], [wx1 + 10, wy1 + 10], [wx0 - 10, wy1 + 10]], true, .7);
  plate(ctx, 'khaki', ridgeP); plate(ctx, 'khaki', ridgeP, { a: .4 });
  const ph = Math.floor(t * 6) % 2;
  stampOxcart(ctx, 1806, 505, 1.15, ph); stampWoman(ctx, 1664, 504, 1.5, 1 - ph);
  ctx.restore();
  const fr = new Path2D(); fr.rect(wx0 - 22, wy0 - 22, wx1 - wx0 + 44, 22); fr.rect(wx0 - 22, wy1, wx1 - wx0 + 44, 26); fr.rect(wx0 - 22, wy0, 22, wy1 - wy0); fr.rect(wx1, wy0, 22, wy1 - wy0);
  fr.rect((wx0 + wx1) / 2 - 7, wy0, 14, wy1 - wy0); fr.rect(wx0, 330, wx1 - wx0, 12);
  knock(ctx, fr); plate(ctx, 'ochre', fr, { n: 2 }); inkStroke(ctx, fr, 3);
  // —— kurmay haritası
  const map = staffMap(ctx, { x: 62, y: 150, w: 820, rot: -.021, front: 1, arrows: 1, focus: [640, 330] });
  const F = map.toWorld(640, 330); // İsmet'in parmağının gösterdiği nokta (Duatepe önü)
  gasLamp(ctx, L0[0], L0[1], 1.0, t);
  // —— kişiler: aynı ölçek; Fevzi en arkada, Mustafa Kemal ortada, İsmet önde (omzu MK'nin kaputunu örter)
  const S_ = 1.24, look = F;
  // Fevzi: "tutma" pozu, ön kollar kaputun önünden telgrafnameye
  const fz = { x: 1430, y: 322, s: S_, dir: -1 };
  bust(ctx, { ...fz, coat: 'kaput', col: 'khaki', w: 1.0, seed: 7, len: (900 - fz.y) / S_, tilt: .02, turn: .3, back: true });
  head3q(ctx, { ...fz, who: 'fevzi', gear: 'kalpak', gearCol: 'grey', light: 'front', lookAt: look, age: 45, tilt: -.035 });
  const tg = [1416, 650];
  const fA1 = arm(ctx, [1362, 606], [tg[0] - 72, tg[1] + 8], { upper: 30, fore: 28, w: 46, col: 'khaki', bend: -1 });
  const fA2 = arm(ctx, [1494, 612], [tg[0] + 76, tg[1] + 14], { upper: 30, fore: 28, w: 48, col: 'khaki', bend: 1 });
  paperSheet(ctx, tg[0], tg[1], 170, 124, .06, 13, { header: true });
  handDraw(ctx, fA1.wr[0], fA1.wr[1], fA1.ang, fA1.w2 / 20, 'hold', { side: 1 });
  handDraw(ctx, fA2.wr[0], fA2.wr[1], fA2.ang, fA2.w2 / 20, 'hold', { side: -1 });
  // Mustafa Kemal: "arkada" pozu (kollar arkada, kol çizilmez), haritaya dönük
  const mk = { x: 1160, y: 306, s: S_, dir: -1 };
  bust(ctx, { ...mk, coat: 'kaput', col: 'khaki', w: .96, seed: 3, len: (900 - mk.y) / S_, tilt: .07, turn: .3, sep: true, arms: 'back' });
  head3q(ctx, { ...mk, who: 'mk', gear: 'kalpak', gearCol: 'ink', light: 'front', lookAt: look, age: 40, tilt: -.05 });
  // İsmet: önde; işaret eden kol omuz ekleminden (siluetin içinden)
  const is = { x: 978, y: 340, s: S_, dir: -1 };
  bust(ctx, { ...is, coat: 'kaput', col: 'khaki', w: .86, seed: 5, len: (900 - is.y) / S_, tilt: -.06, turn: .6, sep: true });
  head3q(ctx, { ...is, who: 'ismet', gear: 'kalpak', gearCol: 'ink', light: 'front', lookAt: look, age: 36, tilt: .04 });
  const isArm = arm(ctx, [930, 462], [F[0] + 64, F[1] + 26], { upper: 142, fore: 132, w: 52, col: 'khaki', bend: 1 });
  handDraw(ctx, isArm.wr[0], isArm.wr[1], isArm.ang, isArm.w2 / 20, 'point', { side: -1 });
  // —— ön masa: el, dürbün, pusula, evrak
  woodTable(ctx, 836);
  paperSheet(ctx, 760, 924, 200, 130, -.06, 21, { rows: 5 });
  compass(ctx, 930, 958, 48);
  binoculars(ctx, 1150, 940, 1.15, .08);
  if (!o.captions) return;
  // —— yazılar: bölüm künyesi (sol alt) ve tek isim levhası (sağ alt)
  const cap = PL(rough([[76, 868], [640, 868], [640, 1040], [76, 1040]], 1, 9));
  plate(ctx, 'ink', PL([[86, 880], [650, 880], [650, 1052], [86, 1052]]), { a: .4 });
  knock(ctx, cap, P.paperD); inkStroke(ctx, cap, 3.6); inkStroke(ctx, PL([[88, 880], [628, 880], [628, 1028], [88, 1028]]), 1.4);
  txt(ctx, 'V · ANADOLU', 110, 960, FONT.title(80), { ls: 2 });
  plate(ctx, 'red', PL([[112, 976], [604, 976], [604, 983], [112, 983]]));
  txt(ctx, 'ALAGÖZ · EYLÜL 1921', 112, 1016, FONT.mono(30), { ls: 3 });
  nameTag(ctx, 1860, 880, 'MUSTAFA KEMAL', '40 yaşında', 1, 99, { align: 'right', size: 56, sub: 38, bg: P.paperD });
}

// Yaş şeridi: aynı baş modülüyle Mustafa Kemal'in beş dönemi
SCENES.yas = (ctx, t) => {
  setReg(5, 1);
  paperBG(ctx);
  const stages = [
    { age: 18, gear: 'fes', coat: 'setre', col: 'navy', lab: 'HARBİYE · 1899' },
    { age: 30, gear: 'kefiye', coat: 'setre', col: 'khaki', lab: 'DERNE · 1911' },
    { age: 34, gear: 'kabalak', coat: 'setre', col: 'khaki', lab: 'ARIBURNU · 1915' },
    { age: 40, gear: 'kalpak', coat: 'kaput', col: 'khaki', lab: 'SAKARYA · 1921' },
    { age: 42, gear: null, coat: 'civil', col: 'ink', lab: 'ÇANKAYA · 1923' },
  ];
  // kuşak şeridi zemini
  plate(ctx, 'ochre', PL([[0, 170], [W, 170], [W, 760], [0, 760]]), { a: .55 });
  stages.forEach((st, i) => {
    const x = 210 + i * 375, y = 420;
    const o = { x, y, s: 1.32, dir: -1 };
    ctx.save(); ctx.beginPath(); ctx.rect(0, 170, W, 590); ctx.clip();
    bust(ctx, { ...o, coat: st.coat, col: st.col, w: .98, seed: 3, len: 280 });
    head3q(ctx, { ...o, who: 'mk', gear: st.gear, gearCol: 'ink', light: 'front', look: [1, .3], age: st.age });
    ctx.restore();
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
    const o = { x: 330 + i * 630, y: 470, s: 3.2, dir: -1 }; ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, H); ctx.clip();
    bust(ctx, { ...o, coat: 'kaput', col: 'khaki', w: 1, seed: 3, len: 200 });
    head3q(ctx, { ...o, who, gear, gearCol: gc, light: 'front', look: [1, .3], age }); ctx.restore();
  });
  pressFinish(ctx, t, {});
};

// Ortak kimlikler (yakın plan)
SCENES.kadro = (ctx, t) => {
  setReg(9); paperBG(ctx); plate(ctx, 'ochre', PL([[0, 0], [W, 0], [W, H], [0, H]]), { a: .4 });
  const L = [['karabekir', 'kalpak', 'kaput', 'khaki', 39], ['alifuat', 'kalpak', 'kaput', 'khaki', 39], ['rauf', 'kalpak', 'civil', 'navy', 39], ['refet', 'kalpak', 'kaput', 'khaki', 39], ['halide', 'carsaf', 'civil', 'ink', 35], ['abdulhamid', 'fes', 'setre', 'ink', 60]];
  L.forEach(([who, gear, coat, col, age], i) => {
    const o = { x: 170 + i * 316, y: 500, s: 1.9, dir: -1 };
    ctx.save(); ctx.beginPath(); ctx.rect(i * 316 + 12, 0, 304, H); ctx.clip();
    bust(ctx, { ...o, coat, col, w: .95, seed: i, len: 260 });
    head3q(ctx, { ...o, who, gear, gearCol: 'ink', light: 'front', look: [1, .3], age });
    ctx.restore();
    txt(ctx, PEOPLE[who].name, o.x, 1000, FONT.mono(28), { align: 'center' });
  });
  pressFinish(ctx, t, {});
};
