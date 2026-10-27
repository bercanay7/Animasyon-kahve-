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
