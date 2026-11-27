// Van Gogh figür klipleri: Blender'da tekrar kullanılan, sahneye 2B olarak yerleştirilen (figurDarbe konum) siluet klipleri.
// node van-gogh/blender/klip.js [ad,…] → klip_<ad>/eklem.json, kamera.json, kostum.json; sonra: bash van-gogh/blender/klip.sh <ad>
// Her klip 8 sn, 15 kare/sn (121 kare); duruş klipleri 8 sn'de döngü yapar (nefes ve ağırlık aktarımı periyodik).
// Kamera: göz 1.6 m, figür 4 m ötede; sırttan ¾ (yüz görünmez). Işık: önden-yandan yumuşak gün ışığı (iç mekânda da aynı; kenar ışığını figurDarbe verir).
const I = require('../../araclar/manken/iskelet.js'), HR = require('../../araclar/hareket/hareket.js'), V = I.V, fs = require('fs'), path = require('path');
const sm = (a, b, x) => { const u = Math.max(0, Math.min(1, (x - a) / (b - a))); return u * u * (3 - 2 * u); };
const TAU = Math.PI * 2, N = 121;
const KOS = {
  theo: { giysi: 'ceket', sapka: false, atki: false, canta: false, renk: { palto: [.09, .085, .1], pantolon: [.08, .075, .085], sac: [.09, .07, .055] } },
  theo_dis: { giysi: 'palto', sapka: true, atki: false, canta: false, renk: { palto: [.1, .095, .11], pantolon: [.08, .075, .085], sapka: [.08, .07, .07], sac: [.09, .07, .055] } },
  vincent: { giysi: 'ceket', sapka: 'hasir', atki: false, canta: false, renk: { palto: [.16, .17, .2], pantolon: [.12, .11, .1], sac: [.28, .16, .08] } },
  gauguin: { giysi: 'palto', sapka: true, atki: false, canta: true, renk: { palto: [.13, .11, .1], pantolon: [.1, .09, .08], sac: [.1, .08, .06] } },
  jo: { giysi: 'elbise', sapka: false, atki: false, canta: false, sac: 'topuz', renk: { palto: [.42, .4, .38], pantolon: [.3, .28, .27], sac: [.16, .11, .08] } },
};
const ISIK = { gunes: { yon: [-.5, .7, .5], guc: 1.3, renk: [1, .95, .88] }, ortam: .12 };   // koyu siluet: biçim yalnız yumuşak bir yan ışıkla
// klip: {kos, kamera (konum/hedef/fov), poz(t) → poz}
const YER = [0, -4], ARKA = Math.PI * .82;   // figür kameraya sırtı ¾ dönük (yaw: yüzün baktığı yön; π = kameradan uzağa)
const nefes = (p, t, a = 1) => { const w = Math.sin(t * TAU / 8); p.kok = [p.kok[0] + .014 * w * a, p.kok[1] - .003, p.kok[2]]; p.yan = (p.yan || 0) + .02 * w * a; p.gogusEgim = (p.gogusEgim || 0) + .01 * Math.sin(t * TAU / 4) * a; return p; };
const KAM = { konum: [0, 1.45, -1], hedef: [0, .95, -4], fov: 40 };   // figür 3 m ötede: karenin ~%80'i
const g = HR.yuruyus({ tip: 'yuru' });
const yuru = (yaw, bas, hiz = 1) => { const yol = HR.yuruyusYolu(g, { t0: -1, t1: 9, x0: 0, olcek: hiz, go: () => 1 }); return t => I.yuruyus3B(yol, t, { bas, yaw, kolGenlik: .26 }); };
const KLIP = {
  theo_dur: { kos: 'theo', poz: t => nefes(I.POZ.dur(YER, ARKA, { basEgim: .1, basDon: .06 * Math.sin(t * TAU / 8) }), t) },
  theo_dis_dur: { kos: 'theo_dis', poz: t => nefes(I.POZ.dur(YER, ARKA, { basEgim: .06 }), t) },
  vincent_dur: { kos: 'vincent', poz: t => nefes(I.POZ.dur(YER, Math.PI * .9, { basEgim: .04, basDon: -.05 * Math.sin(t * TAU / 8) }), t) },
  jo_dur: { kos: 'jo', poz: t => nefes(I.POZ.dur(YER, Math.PI * .78, { basEgim: .08 }), t, .7) },
  theo_oku: { kos: 'theo', poz: t => nefes(I.POZ.oku([0, -3.6], Math.PI * .85, .76, (t % 8) / 8, { basEgim: .5 }), t, .4) },
  // yürüyenler: kameradan uzaklaşan çapraz yol (sırttan); 8 sn'de ~8 m
  theo_yuru: { kos: 'theo', poz: yuru(Math.PI * .86, [-.6, -2.6]) },
  jo_yuru: { kos: 'jo', poz: yuru(Math.PI * .8, [-.4, -2.8], .9) },
  gauguin_yuru: { kos: 'gauguin', poz: yuru(Math.PI * .9, [-.8, -2.4]) },
  vincent_yuru: { kos: 'vincent', poz: yuru(Math.PI * .88, [-.6, -2.6]) },
  // sahneye özgü: set kamerasıyla (göz 1.6 m, düz bakış, 40°; SALON ve ODA ile aynı) çizilir, konumsuz basılır
  theo_louvre: { kos: 'theo_dis', kamera: { konum: [0, 1.6, 0], hedef: [0, 1.6, -10], fov: 40 }, poz: yuru(Math.PI * 1.02, [.9, -3.2], .85) },
  vincent_louvre: { kos: 'vincent', kamera: { konum: [0, 1.6, 0], hedef: [0, 1.6, -10], fov: 40 }, poz: t => nefes(I.POZ.dur([-.6, -19], Math.PI * .5, { basEgim: .02, basDon: .5 * sm(5, 7, t) }), t) },
};
const secili = process.argv[2] ? process.argv[2].split(',') : Object.keys(KLIP);
for (const ad of secili) {
  const k = KLIP[ad], dir = path.join(__dirname, 'klip_' + ad); fs.mkdirSync(dir, { recursive: true });
  const out = [];
  for (let i = 0; i < N; i++) {
    const t = i / 15, K = I.kemikler(k.poz(t)), cer = c => ({ o: c.o, x: c.x, y: c.y, z: c.z });
    out.push({ t, pelvis: cer(K.pelvis), gogus: cer(K.gogus), boyun: cer(K.boyun), bas: cer(K.bas),
      bacak: K.bacak.map(b => ({ kalca: b.kalca, diz: b.diz, bilek: b.bilek, ayak: cer(b.ayak) })), kol: K.kol.map(c => ({ omuz: c.omuz, dirsek: c.dirsek, bilek: c.bilek, el: cer(c.el) })),
      canta: { kok: K.pelvis.o, asagi: V.mul(K.pelvis.y, -1) } });
  }
  fs.writeFileSync(path.join(dir, 'eklem.json'), JSON.stringify(out));
  fs.writeFileSync(path.join(dir, 'kamera.json'), JSON.stringify({ ...KAM, ...(k.kamera || {}), dis: ISIK }));
  fs.writeFileSync(path.join(dir, 'kostum.json'), JSON.stringify(KOS[k.kos]));
  console.log(ad, out.length, 'kare');
}
