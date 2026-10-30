// Karakter görünümleri ve elde taşınan nesneler
'use strict';
const LK = {
  prom: { beard: 'pointed', hair: 'nape', garment: 'hipwrap', anat: true, rf: true, earHidden: true, sevEye: true, flatChest: true, legIrons: true, scowl: .6 },
  zeus: { beard: 'full', hair: 'long', headgear: 'wreath', garment: 'robe', himation: true, robeDots: true, eyeS: 1.3, brow: -.6 },
  hermes: { beard: 'pointed', hair: 'long', headgear: 'petasos', garment: 'short', cape: true, wingedFeet: true },
};
LK.promFree = { ...LK.prom, legIrons: false }; // zincirlenmeden önce (ateşin çalınışı)
// --- elde taşınanlar (G: figür çizim bağlamı, el yerel koordinatı: bilek orijin, +y parmak yönü) ---
// dik tutulan nesneler el açısını geri alır (asa her zaman dik)
const up = (G, f) => { G.g.save(); G.g.rotate(G.handA || 0); f(); G.g.restore(); };
const HOLD = {
  scepter: (L = 70) => G => up(G, () => { G.part(c => { c.rect(-1, -L * .55, 2, L); }, { cutW: .3 }); G.part(c => { c.arc(0, -L * .55, 2.4, 0, TAU); }, { cutW: .3 }); G.paint(c => { c.arc(0, -L * .55, 1.2, 0, TAU); }, G.sty.red); }),
  spear: (L = 95) => G => up(G, () => { G.part(c => { c.rect(-.9, -L * .6, 1.8, L); }, { cutW: .3 }); G.part(c => { c.moveTo(0, -L * .6 - 9); c.lineTo(2.6, -L * .6 - 1); c.lineTo(-2.6, -L * .6 - 1); c.closePath(); }, { cutW: .3 }); }),
  shield: (r = 17) => G => {
    G.at([0, 3], 0, () => {
      G.part(c => c.arc(0, 0, r, 0, TAU), { cutW: .6 });
      G.cut(c => c.arc(0, 0, r - 2.2, 0, TAU), .5);
      // amblem: akrep/yılan yerine sade bir göz/sarmal
      G.paint(c => { c.arc(0, 0, r * .35, 0, TAU); }, G.sty.red);
      G.cut(c => { for (let a = 0; a < TAU * 1.5; a += .2) { const rr = r * .3 * (1 - a / (TAU * 1.6)); const x = Math.cos(a) * rr, y = Math.sin(a) * rr; a ? c.lineTo(x, y) : c.moveTo(x, y); } }, .4);
    });
  },
  bolt: () => G => { G.at([0, 4], .2, () => { G.paint(c => { c.moveTo(0, -18); c.lineTo(2.4, -8); c.lineTo(.8, -7); c.lineTo(3, 0); c.lineTo(.8, 1); c.lineTo(2.2, 9); c.lineTo(0, 18); c.lineTo(-2.2, 9); c.lineTo(-.8, 1); c.lineTo(-3, 0); c.lineTo(-.8, -7); c.lineTo(-2.4, -8); c.closePath(); }, C.gold); }); },
  caduceus: () => G => up(G, () => { G.part(c => c.rect(-.7, -30, 1.4, 52), { cutW: .3 }); G.part(c => { c.arc(-2.2, -32, 2.2, 0, TAU); c.moveTo(4.4, -32); c.arc(2.2, -32, 2.2, 0, TAU); }, { cutW: .3 }); }),
  key: () => G => { G.part(c => { c.rect(-.6, -2, 1.2, 12); c.moveTo(2.6, -3); c.arc(0, -3, 2.6, 0, TAU); c.rect(0, 7, 3.4, 1.4); c.rect(0, 9.5, 2.6, 1.2); }, { cutW: .3 }); },
  kylix: () => G => up(G, () => { G.at([0, -6], 0, () => { G.part(c => { c.moveTo(-9, -2); c.quadraticCurveTo(0, 6, 9, -2); c.closePath(); c.rect(-.8, 1, 1.6, 4); c.rect(-3.5, 4.5, 7, 1.2); }, { cutW: .3 }); }); }),
  torch: () => G => up(G, () => { G.part(c => c.rect(-.9, -18, 1.8, 26), { cutW: .3 }); G.paint(c => { c.moveTo(0, -30 + Math.sin(performance.now()) * 0); c.quadraticCurveTo(4.5, -22, 2, -17); c.lineTo(-2, -17); c.quadraticCurveTo(-4.5, -22, 0, -30); }, C.gold); }),
  hydria: () => G => { G.at([0, -4], 0, () => { G.part(c => { c.moveTo(-3, -8); c.lineTo(3, -8); c.quadraticCurveTo(11, -4, 10, 6); c.quadraticCurveTo(8, 14, 3, 16); c.lineTo(-3, 16); c.quadraticCurveTo(-8, 14, -10, 6); c.quadraticCurveTo(-11, -4, -3, -8); }, { cutW: .4 }); G.cut(c => { c.moveTo(-9, 2); c.lineTo(9, 2); }, .35); }); },
  chisel: () => G => { G.part(c => { c.rect(-.7, -8, 1.4, 12); c.moveTo(-1.4, -8); c.lineTo(1.4, -8); c.lineTo(0, -12); c.closePath(); }, { cutW: .3 }); },
  hammer: () => G => { G.part(c => { c.rect(-.7, -6, 1.4, 14); c.rect(-4, -9, 8, 4); }, { cutW: .3 }); },
  book: () => G => { G.at([2, 5], .2, () => G.part(c => c.rect(-5, -7, 10, 13), { fill: G.sty.white, outline: G.sty.line, cut: false })); },
  pen: () => G => { G.part(c => c.rect(-.4, -6, .8, 9), { cutW: .2 }); },
  cig: () => G => { G.paint(c => c.rect(1.6, 3.6, 5, .9), G.sty.white); },
  bag: () => G => { G.at([0, 9], 0, () => { G.part(c => { c.rect(-7, 0, 14, 9); c.moveTo(-3, 0); c.lineTo(-3, -2.4); c.lineTo(3, -2.4); c.lineTo(3, 0); }, { cutW: .35 }); }); },
  many: (...fs) => G => fs.forEach(f => f(G)),
};
