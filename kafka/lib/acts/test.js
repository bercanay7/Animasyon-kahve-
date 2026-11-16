// Deneme sayfaları: ?scene=figurler
var SCENES = window.SCENES || {}; window.SCENES = SCENES;
SCENES.figurler = (ctx, t) => kes(ctx, { t, lt: t, p: 0, seed: 1 }, { cx: 960, cy: 470, z: 1 }, k => {
  KS.ak(k.m, KS.rect(58, 40, 1804, 860));
  k.m.fillStyle = '#000'; k.m.fillRect(58, 800, 1804, 100);
  const tips = ['baba', 'anne', 'grete', 'mudur', 'kiraci', 'gregor', 'kafka', 'bugun'];
  tips.forEach((tp, i) => O.fig(k, { x: 170 + i * 225, y: 800, h: 560, f: i % 2 ? -1 : 1, tip: tp, kep: tp === 'baba' }, { isik: [-1, -.5] }));
  // karanlık zeminde ışıklı kenar denemesi
  const F = IN.insan({ x: 960, y: 780, h: 300, f: 1, tip: 'grete', otur: true, kolN: [1.2, -.4] });
}, { tamKare: false });
