// node araclar/manken/test.js : 3B mankenin sözleşmesi. araclar/hareket/test.js ölçütü 3B'de:
// düz basan ayak (eğim 0) dünyada sabit; kemik boyları korunur; diz öne kırılır; ayak zeminin altına inmez; belirlenimci.
const H = require('../hareket/hareket.js');
const I = require('./iskelet.js');
const { V, OLCU } = I;
let hata = 0; const ok = (k, m) => { console.log((k ? 'TAMAM ' : 'HATA  ') + m); if (!k) hata++; };

for (const tip of ['yuru', 'surun']) for (const yaw of [0, .7, -2.2]) {
  const g = H.yuruyus({ tip });
  const go = t => H.rampa(t, 0, .5) * (1 - H.rampa(t, 3.5, 4));
  const yol = H.yuruyusYolu(g, { t0: 0, t1: 6, x0: 0, olcek: 1, go });
  let kayma = 0, rampaKayma = 0, boy = 0, dizGeri = 0, zemin = Infinity;
  for (let t = .2; t < 5.5; t += 1 / 240) {
    const pa = I.yuruyus3B(yol, t, { bas: [1, -2], yaw }), pb = I.yuruyus3B(yol, t + 1 / 240, { bas: [1, -2], yaw });
    const ka = I.kemikler(pa), kb = I.kemikler(pb);
    for (const i of [0, 1]) {
      const aa = pa.ayak[i], ab = pb.ayak[i];
      if (aa.basiyor && ab.basiyor && aa.egim === 0 && ab.egim === 0) {
        const k = V.len(V.sub(kb.bacak[i].bilek, ka.bacak[i].bilek));
        if (t > 1 && t < 3.4) kayma = Math.max(kayma, k); else rampaKayma = Math.max(rampaKayma, k);   // 2B test.js ile aynı aralık
      }
      const b = ka.bacak[i];
      boy = Math.max(boy, Math.abs(V.len(V.sub(b.diz, b.kalca)) - OLCU.uyluk), Math.abs(V.len(V.sub(b.bilek, b.diz)) - OLCU.baldir));
      // diz, kalça-bilek doğrusunun önünde mi (f yönünde)
      const f = [Math.sin(yaw), 0, Math.cos(yaw)], orta = V.lerp(b.kalca, b.bilek, .5);
      dizGeri = Math.min(dizGeri, V.dot(V.sub(b.diz, orta), f));
      zemin = Math.min(zemin, b.bilek[1]);
    }
  }
  const ad = `${tip} yaw=${yaw}`;
  ok(kayma < 1e-6, `${ad}: düz basan ayak dünyada sabit (en büyük kayma ${kayma.toExponential(1)} m = ${(kayma * 480).toExponential(1)} px, 1 m ≈ 480 px)`);
  console.log(`      bilgi: başlama/durma rampasında kare başına en büyük kayma ${(rampaKayma * 1000).toFixed(2)} mm (çözücünün go < 1 karışımı; 2B'de de var)`);
  ok(boy < 1e-6, `${ad}: uyluk ve baldır boyu korunuyor (sapma ${boy.toExponential(1)} m)`);
  ok(dizGeri > -1e-6, `${ad}: diz hiç geriye kırılmıyor (${dizGeri.toExponential(1)})`);
  ok(zemin > 0, `${ad}: bilek zeminin üstünde (en alçak ${zemin.toFixed(4)} m)`);
  const a = JSON.stringify(I.kemikler(I.yuruyus3B(yol, 2.345, { yaw })));
  const b = JSON.stringify(I.kemikler(I.yuruyus3B(H.yuruyusYolu(g, { t0: 0, t1: 6, x0: 0, olcek: 1, go }), 2.345, { yaw })));
  ok(a === b, `${ad}: belirlenimci`);
}
// poz kütüphanesi: kollar boyunu korur, eller masada
for (const [ad, p] of Object.entries({ dur: I.POZ.dur([0, 0], .3), egil: I.POZ.egil([0, 0], .3, .76), oku: I.POZ.oku([0, 0], .3, .76, .5) })) {
  const K = I.kemikler(p);
  let s = 0; for (const k of K.kol) s = Math.max(s, Math.abs(V.len(V.sub(k.dirsek, k.omuz)) - OLCU.pazu), Math.abs(V.len(V.sub(k.bilek, k.dirsek)) - OLCU.onkol));
  ok(s < 1e-6, `poz ${ad}: kol boyları korunuyor`);
  // havaya kalkmış düz kol yok: bilek omuzdan yukarıda değil
  ok(K.kol.every(k => k.bilek[1] < k.omuz[1]), `poz ${ad}: el omuz hizasının altında (selam / alna el yok)`);
  if (p.kol[0].hedef) ok(K.kol.every((k, i) => V.len(V.sub(k.bilek, p.kol[i].hedef)) < 1e-3), `poz ${ad}: eller hedefe (masaya) ulaşıyor`);
}
process.exit(hata ? 1 : 0);
