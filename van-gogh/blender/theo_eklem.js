// Theo'nun odası (üslup kapısı): Theo şövaledeki tabloya bakar; nefes, ağırlık aktarımı, baş yavaşça tabloya döner ve eğilir.
// node van-gogh/blender/theo_eklem.js → van-gogh/blender/eklem_oda.json (kurye_bpy.py ile aynı yapı), kamera_oda.json
const I = require('../../araclar/manken/iskelet.js'), V = I.V, fs = require('fs'), path = require('path');
const sm = (a, b, x) => { const u = Math.max(0, Math.min(1, (x - a) / (b - a))); return u * u * (3 - 2 * u); };
const YER = [-.6, -2.35], YAW = Math.atan2(.92, -1.1);           // kameraya yakın, solda; tabloya dönük: sırtı yarı dönük (¾ arka)
const DUR = 8, out = [];
for (let k = 0; k <= DUR * 15; k++) {
  const t = k / 15;
  const p = I.POZ.dur(YER, YAW, { basEgim: .1 });
  const w = Math.sin(t * .7);
  p.kok = [p.kok[0] + .015 * w, p.kok[1] - .004, p.kok[2]]; p.yan = (p.yan || 0) + .025 * w;
  p.gogusEgim = (p.gogusEgim || 0) + .012 * Math.sin(t * 1.6) + .04 * sm(3, 5.5, t);     // tabloya doğru hafif eğilir
  p.basEgim = (p.basEgim || 0) + .12 * sm(2.5, 5, t); p.basDon = (p.basDon || 0) + .18 * sm(1, 4, t);
  const K = I.kemikler(p), cer = c => ({ o: c.o, x: c.x, y: c.y, z: c.z });
  out.push({ t, pelvis: cer(K.pelvis), gogus: cer(K.gogus), boyun: cer(K.boyun), bas: cer(K.bas),
    bacak: K.bacak.map(b => ({ kalca: b.kalca, diz: b.diz, bilek: b.bilek, ayak: cer(b.ayak) })), kol: K.kol.map(c => ({ omuz: c.omuz, dirsek: c.dirsek, bilek: c.bilek, el: cer(c.el) })),
    canta: { kok: K.pelvis.o, asagi: V.mul(K.pelvis.y, -1) } });
}
fs.writeFileSync(path.join(__dirname, 'eklem_oda.json'), JSON.stringify(out));
// kamera: göz hizası 1.5 m, düz bakış (ufuk y = 540), dikey görüş 40°
fs.writeFileSync(path.join(__dirname, 'kamera_oda.json'), JSON.stringify({ konum: [0, 1.5, 0], hedef: [0, 1.5, -10], fov: 40, isik: { konum: [.62, 1.12, -3.0], guc: 45, renk: [1, .8, .55], ortam: .025, gunes: 0, boy: .04 } }));
fs.writeFileSync(path.join(__dirname, 'kostum_theo.json'), JSON.stringify({ giysi: 'ceket', sapka: false, atki: false, canta: false,
  renk: { palto: [.09, .085, .1], pantolon: [.08, .075, .085], sac: [.09, .07, .055] } }));
console.log(out.length, 'kare');
