// node araclar/hareket/test.js : yürüyüş çözücüsünün temel sözleşmesini sınar (ayak kayması, kalça, determinizm)
const H = require('./hareket.js');
let hata = 0; const ok = (k, m) => { console.log((k ? 'TAMAM ' : 'HATA  ') + m); if (!k) hata++; };
for (const tip of ['yuru', 'surun', 'kos']) {
  const g = H.yuruyus({ tip }), olcek = 4.5;
  const yol = H.yuruyusYolu(g, { t0: 0, t1: 6, x0: 300, olcek, go: t => H.rampa(t, 0, .5) * (1 - H.rampa(t, 3.5, 4)) });
  // basan ayağın dünya x'i: ardışık karelerde (1/240 sn) ikisi de basıyorsa kayma
  let enKayma = 0;
  for (let t = 1; t < 3.4; t += 1 / 240) {
    const a = yol(t), b = yol(t + 1 / 240);
    for (const i of [0, 1]) if (a.poz.ayaklar[i].basiyor && b.poz.ayaklar[i].basiyor && a.poz.ayaklar[i].egim === 0 && b.poz.ayaklar[i].egim === 0) {
      const wa = a.x + (a.poz.ayaklar[i].bilek[0] - 40) * olcek, wb = b.x + (b.poz.ayaklar[i].bilek[0] - 40) * olcek;
      enKayma = Math.max(enKayma, Math.abs(wb - wa));
    }
  }
  ok(enKayma < 1e-6, `${tip}: düz basan ayak dünyada sabit (en büyük kayma ${enKayma.toExponential(1)} px)`);
  const iniş = []; for (let t = 1; t < 3; t += 1 / 60) iniş.push(yol(t).poz.inis);
  ok(Math.max(...iniş) - Math.min(...iniş) > .3, `${tip}: kalça yükselip iniyor (genlik ${(Math.max(...iniş) - Math.min(...iniş)).toFixed(2)} birim)`);
  const dur = yol(5);
  ok(dur.go === 0 && Math.abs(yol(5.5).x - dur.x) < 1e-9, `${tip}: durunca yerinde kalıyor (x=${dur.x.toFixed(1)})`);
  ok(JSON.stringify(yol(2.345)) === JSON.stringify(H.yuruyusYolu(g, { t0: 0, t1: 6, x0: 300, olcek, go: t => H.rampa(t, 0, .5) * (1 - H.rampa(t, 3.5, 4)) })(2.345)), `${tip}: deterministik`);
}
const yay = H.yayIzi({ hedef: t => t < 1 ? 0 : 1, k: 40, d: 6, t0: 0, t1: 4 });
ok(yay(1.3) > 0.2 && Math.abs(yay(4) - 1) < .05, `yay: hedefe gecikerek oturuyor (1,3 sn: ${yay(1.3).toFixed(2)}, 4 sn: ${yay(4).toFixed(3)})`);
const s = H.sarkacIzi({ t0: 0, t1: 6, itmeler: [[1, 2]] });
ok(Math.abs(s(.9)) < 1e-12 && Math.abs(s(1.5)) > .1 && Math.abs(s(6)) < Math.abs(s(1.5)), `sarkaç: itmeyle salınıp sönüyor`);
process.exit(hata ? 1 : 0);
