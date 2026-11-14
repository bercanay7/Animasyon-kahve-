// Kapaklar (1280×720'ye küçültülür). ?scene=kapakA|kapakB. Kurallar: tek odak, harf ≥ %18 (Bebas), sağ alt (rozet) boş.
'use strict';
function kapakYazi(ctx, lines, x, y, px, col, align = 'left') { ctx.save(); baseT(ctx); ctx.font = FONT.baslik(px); ctx.textAlign = align; ctx.textBaseline = 'alphabetic'; ctx.letterSpacing = '4px'; ctx.fillStyle = col; lines.forEach((l, i) => ctx.fillText(l, x, y + i * px * .9)); ctx.restore(); }
// A: açılış karesinin aynası: İkaros sağda, sola güneşe bakıyor; yazı sol altta
SCENES.kapakA = (ctx, t) => {
  baski(ctx, kSt(4, 4), null, pr => {
    pr.sky('sky2', 'sky1', 70, 300, 4);
    gunes(pr, 420, 250, 120, 3);
    const J = FG.rig({ x: 1330, y: 1160, h: 215, f: -1, lean: .05, head: -.62, armN: [.1, 0], armF: [.1, 0] });
    kanatliFigur(pr, J, { w: { ang: -.6, bend: .3, span: 1000, chord: 370, side: 1, seed: 12 }, armInWing: false, kosum: true, light: [-1, -.7], litD: 4, farOff: [50, 10], faceFill: false, look: { curls: true, chest: true, face: true, belt: false } });
  }, { pal: 'SAFAK' });
  kapakYazi(ctx, ['İKİ UYARI', 'VARDI'], 90, 760, 250, PAL.SAFAK.near);
};
// B: kanat ucu denize değer; yazı üstte
SCENES.kapakB = (ctx, t) => {
  baski(ctx, kSt(3, 6), null, pr => {
    pr.sky('sky2', 'sky1', 60, 300, 4);
    gunes(pr, 1560, 230, 90, 3);
    const wn = FG.wing({ root: [-240, 60], ang: .5, bend: .3, span: 1450, chord: 330, f: 1, seed: 21 });
    litInk(pr, wn.all, 'lit', 'near', 1, -.6, 9); pr.ink(wn.cov, 'mid', { sheen: .1 });
    const yW = 830, sea = new Path2D(); sea.moveTo(-50, yW); for (let x = -50; x <= 1970; x += 20) sea.lineTo(x, yW + Math.sin(x / 90 + 1.2) * 9); sea.lineTo(1970, 1200); sea.lineTo(-50, 1200); sea.closePath(); pr.ink(sea, 'mid', { sheen: .2 });
    for (let k = 0; k < 3; k++) { const r = 70 + k * 80, ring = SK.ringPath(0, 0, r, r + 7), q = new Path2D(); q.addPath(ring, new DOMMatrix().translate(wn.tip[0], yW + 14).scale(1, .22)); pr.ink(q, 'sky1', { sheen: 0, reg: 0 }); }
  }, { pal: 'SAFAK' });
  kapakYazi(ctx, ['UNUTULAN', 'UYARI'], 1850, 470, 250, PAL.SAFAK.near, 'right');
};
