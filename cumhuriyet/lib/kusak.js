// Kuşak şeridi (izleyici katmanı): A05'teki yedi büst, sağ altta küçük madalyonlar. Kişi anlatıda ilk tanıtıldığında
// yuvası dolar; bölüm kartlarında ve dolma anlarında görünür. Yönetmenlik kurulu önerisi: açık döngü + isimlerin akılda kalması.
'use strict';
const KUSAK = [ // A05 dizilişi (act0 A0_SEVEN) sırasıyla
  { who: 'halide', gear: 'basortu', age: 35, at: () => Wd('F04', 'halide') },
  { who: 'karabekir', gear: 'kalpak', age: 36, at: () => Wd('D03', 'karabekir') },
  { who: 'alifuat', gear: 'kalpak', age: 36, at: () => Wd('C06', 'ali') },
  { who: 'mk', gear: 'kalpak', age: 38, at: () => Wd('B06', 'kemal') },
  { who: 'ismet', gear: 'kalpak', age: 34, at: () => Wd('F03', 'ismet') },
  { who: 'fevzi', gear: 'kalpak', gearCol: 'grey', age: 43, at: () => Wd('F03', 'fevzi') },
  { who: 'rauf', gear: 'fes', age: 37, at: () => Wd('F02', 'ali') + .8 }, // Amasya'da isim levhasıyla (anlatıda adı G03'te)
];
// görünme pencereleri: bölüm kartları, dolma anları, "Kuşak hazırdı"
function kusakWins() {
  if (kusakWins.c) return kusakWins.c;
  const w = [];
  // bölüm kartı bittikten sonra (kart ≈ S+3,6'ya dek): kart + 0,3 → + 3,3 sn (tipografi kurulu)
  // D01 yok: öğrencilerin gövdesi alt bantta (animasyon uzmanı)
  for (const [id, off] of [['B01', 5.1], ['C01', 4.6], ['E01', 3.9], ['F01', 3.3]]) w.push([S(id) + off, S(id) + off + 3]);
  for (const k of KUSAK) { const t = k.at(); w.push([t - .5, t + 2.8]); }
  const hz = Wd('F06', 'hazır'); w.push([hz - .4, Se('F06') + .3]);
  w.sort((a, b) => a[0] - b[0]);
  const m = []; for (const x of w) { if (m.length && x[0] <= m[m.length - 1][1] + .8) m[m.length - 1][1] = Math.max(m[m.length - 1][1], x[1]); else m.push([...x]); }
  return (kusakWins.c = m);
}
// şerit o anda görünüyor mu (isim levhaları ve damgalar bölgesinden kaçar: x > 1020, y > 935)
function kusakVisible(t) { return !NOTEXT && typeof Wd === 'function' && t != null && kusakWins().some(([a, b]) => t >= a - .3 && t <= b + .3); }
function kusakBar(ctx, t) {
  if (NOTEXT || typeof Wd !== 'function') return;
  if (window.LOWBAND_AT === t && (window.LOWBAND_X1 ?? W) > 1100) return; // alt bantta şeride uzanan bir yazı (telgraf şeridi vb.) varken çizilmez
  const win = kusakWins().find(([a, b]) => t >= a - .3 && t <= b + .3); if (!win) return;
  const a = clamp((t - win[0] + .3) / .3) * clamp((win[1] + .3 - t) / .3); if (a <= 0) return;
  const hz = Wd('F06', 'hazır'), full = t >= hz;
  const n = KUSAK.filter(k => t >= k.at()).length;
  const sw = 74, x1 = 1812, x0 = x1 - KUSAK.length * sw, y0 = 930, h = 80;
  ctx.save(); ctx.globalAlpha = a;
  // zemin şerit
  const bx0 = x0 - 170, box = PL(rough([[bx0, y0 - 8], [x1 + 12, y0 - 8], [x1 + 12, y0 + h + 8], [bx0, y0 + h + 8]], .8, 17));
  plate(ctx, 'ink', PL([[bx0 + 6, y0], [x1 + 18, y0], [x1 + 18, y0 + h + 16], [bx0 + 6, y0 + h + 16]]), { a: .3 });
  knock(ctx, box); inkStroke(ctx, box, 2.6);
  txt(ctx, 'KUŞAK', bx0 + 16, y0 + 30, FONT.mono(32), { ls: 3 });
  txt(ctx, `${full ? 7 : n}/7`, bx0 + 16, y0 + 80, FONT.title(52), { col: full ? P.red : P.ink });
  KUSAK.forEach((k, i) => {
    const cx = x0 + sw * (i + .5), cy = y0 + h / 2, tf = k.at(), on = t >= tf || full;
    const pop = on ? 1 + .22 * (1 - E.out3(clamp((t - Math.max(tf, full ? hz : tf)) / .35))) : 1;
    ctx.save(); ctx.translate(cx, cy); ctx.scale(pop, pop);
    const ov = new Path2D(); ov.ellipse(0, 0, 31, 37, 0, 0, TAU);
    knock(ctx, ov, on ? P.paper : P.paperD);
    ctx.save(); ctx.clip(ov);
    if (on) {
      const tfig = Math.floor(t * 15) / 15;
      bust(ctx, { x: 0, y: 4, s: .36, dir: 1, coat: k.who === 'halide' ? 'kaput' : 'kaput', col: 'khaki', w: .95, seed: i + 3, len: 140, arms: 'back' });
      head3q(ctx, { x: 0, y: 4, s: .36, dir: 1, who: k.who, gear: k.gear, gearCol: k.gearCol || 'ink', light: 'front', look: [1, .1], age: k.age, eyeOpen: (tfig * 7 + i * 1.3) % 4.5 < .12 ? .1 : undefined });
    } else {
      // boş yuva: baş ve omuz silueti
      const sil = new Path2D(); sil.ellipse(0, -6, 12, 15, 0, 0, TAU); sil.moveTo(-26, 40); sil.quadraticCurveTo(-24, 12, 0, 10); sil.quadraticCurveTo(24, 12, 26, 40); sil.closePath();
      plate(ctx, 'ink', sil, { a: .28 });
    }
    ctx.restore();
    inkStroke(ctx, ov, on ? 2.6 : 1.8);
    const pulse = k.who === 'mk' ? Math.max(0, Math.sin(clamp((t - Wd('F06', 'deha')) / 1.5) * PI * 3)) * (t > Wd('F06', 'deha') && t < Wd('F06', 'deha') + 1.5) : 0;
    if (on) plate(ctx, 'red', PL([[-22, 42], [22, 42], [22, 47 + 3 * pulse], [-22, 47 + 3 * pulse]]), { a: clamp((t - tf) / .3) });
    ctx.restore();
  });
  ctx.restore();
}
