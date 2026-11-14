// Kapaklar (1280×720'ye küçültülür). ?scene=kapakA|kapakB. Kurallar: tek odak, harf ≥ %18 (Bebas), sağ alt (rozet) boş.
'use strict';
function kapakYazi(ctx, lines, x, y, px, col, align = 'left') { ctx.save(); baseT(ctx); ctx.font = FONT.baslik(px); ctx.textAlign = align; ctx.textBaseline = 'alphabetic'; ctx.letterSpacing = '4px'; ctx.fillStyle = col; lines.forEach((l, i) => ctx.fillText(l, x, y + i * px * .9)); ctx.restore(); }
// A: açılış karesinin aynası: İkaros sağda, sola güneşe bakıyor; yazı sol altta (büyük harf ≥ %18: Bebas 290 px ≈ 135 px / 720'de)
SCENES.kapakA = (ctx, t) => {
  baski(ctx, kSt(4, 4), null, pr => {
    pr.sky('sky2', 'sky1', 260, 470, 4);
    const s = FG.sunRings(400, 150, 110, 2); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, '#FAF0CF');
    const J = FG.rig({ x: 1250, y: 1160, h: 215, f: -1, lean: .05, head: -.62, armN: [.1, 0], armF: [.1, 0] });
    kanatliFigur(pr, J, { w: { ang: -.8, bend: .32, span: 540, chord: 230, side: 1, seed: 12 }, armInWing: false, kosum: true, kosumRole: 'sky2', light: [-1, -.7], litD: 4, farOff: [40, 10], faceFill: false, look: { curls: true, chest: true, face: true, belt: false } });
  }, { pal: 'SAFAK', sabit: true });
  kapakYazi(ctx, ['İKİ UYARI', 'VARDI'], 80, 720, 290, PAL.SAFAK.near);
};
// B: kanat ucu denize değer; en parlak öğe temas noktasındaki sıçrama; suda tek tük tüyler; yazı sağ üstte
SCENES.kapakB = (ctx, t) => {
  baski(ctx, kSt(3, 6), null, pr => {
    pr.sky('sky2', 'sky1', 60, 300, 4);
    const s = FG.sunRings(1700, 120, 56, 1); s.rings.forEach(q => pr.ink(q, 'lit', { sheen: 0 })); pr.ink(s.disk, 'lit');
    const wn = FG.wing({ root: [-60, 140], ang: .56, bend: .32, span: 1080, chord: 300, f: 1, seed: 21 });
    litInk(pr, wn.all, 'lit', 'near', 1, -.6, 9); pr.ink(wn.cov, 'mid', { sheen: .1 });
    const yW = 830, sea = new Path2D(); sea.moveTo(-50, yW); for (let x = -50; x <= 1970; x += 20) sea.lineTo(x, yW + Math.sin(x / 90 + 1.2) * 9); sea.lineTo(1970, 1200); sea.lineTo(-50, 1200); sea.closePath(); pr.ink(sea, 'mid', { sheen: .2 });
    const tx = wn.tip[0];
    for (let k = 0; k < 3; k++) { const r = 80 + k * 90, ring = SK.ringPath(0, 0, r, r + 9), q = new Path2D(); q.addPath(ring, new DOMMatrix().translate(tx, yW + 14).scale(1, .22)); pr.ink(q, 'sky1', { sheen: 0, reg: 0 }); }
    const sp = new Path2D(); for (let i = 0; i < 7; i++) { const a = -Math.PI + i * .52; FG.ellipseInto(sp, tx + Math.cos(a) * 46, yW - 6 + Math.sin(a) * 38, 14, 22, a + Math.PI / 2, 12); } pr.ink(sp, '#FAF0CF', { sheen: 0, reg: 0 });
    const tu = new Path2D(); [[1180, 905, .25], [1460, 975, -.35], [880, 1010, 2.8]].forEach(([x, y, a]) => a2_tuy(tu, x, y, 170, a, .2)); litInk(pr, tu, 'lit', 'near', 1, -.6, 5);
  }, { pal: 'SAFAK', sabit: true });
  kapakYazi(ctx, ['UNUTULAN', 'UYARI'], 1860, 500, 290, PAL.SAFAK.near, 'right');
};
