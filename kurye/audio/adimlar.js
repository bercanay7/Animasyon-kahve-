// Kuryenin ayak basma anları (ses için): tablo.html'deki yürüyüşün aynısı, node'da.
// node kurye/audio/adimlar.js > kurye/audio/adimlar.json
const HR = require('../../araclar/hareket/hareket.js'), I = require('../../araclar/manken/iskelet.js');
const g = HR.yuruyus({ tip: 'yuru' }), tDur = 7.0, KAY = 1.0;
const go = t => HR.rampa(t, -.6, .1) * (1 - HR.rampa(t, tDur - .8, tDur));
const yol = HR.yuruyusYolu(g, { t0: -1.5, t1: 26, x0: 0, olcek: 1, go });
const A0 = [-5.6, -5.6], YAW = Math.atan2(3.85, -4.0);
const out = []; let onc = [1, 1], kalk = [-9, -9];   // en az 0.25 sn havada kalan ayağın inişi = adım
for (let f = 0; f <= 7.5 * 240; f++) { const t = f / 240, p = I.yuruyus3B(yol, t + KAY, { bas: A0, yaw: YAW });
  p.ayak.forEach((a, i) => { const h = a.bilek[1], yere = h < .034; if (!yere && onc[i]) kalk[i] = t;
    if (yere && !onc[i] && t - kalk[i] > .25) out.push({ t: +t.toFixed(3), ayak: i, x: +a.bilek[0].toFixed(2), z: +a.bilek[2].toFixed(2) }); onc[i] = yere; }); }
// ikinci kısa yürüyüş (çiçek açınca ağaca doğru; tablo.html yol2)
const tAd = 18.4, yol2 = HR.yuruyusYolu(g, { t0: -1, t1: 26, x0: 0, olcek: 1, go: t => HR.rampa(t, tAd, tAd + .45) * (1 - HR.rampa(t, tAd + 1.1, tAd + 1.9)) });
onc = [1, 1]; kalk = [-9, -9];
for (let f = Math.round(tAd * 240); f <= 21 * 240; f++) { const t = f / 240, p = I.yuruyus3B(yol2, t, { bas: [0, 0], yaw: 0 });
  p.ayak.forEach((a, i) => { const yere = a.bilek[1] < .034; if (!yere && onc[i]) kalk[i] = t; if (yere && !onc[i] && t - kalk[i] > .25) out.push({ t: +t.toFixed(3), ayak: i, ikinci: true }); onc[i] = yere; }); }
console.log(JSON.stringify(out));
