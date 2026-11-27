// Van Gogh figür klipleri: Blender'da tekrar kullanılan, sahneye 2B olarak yerleştirilen (figurDarbe konum) siluet klipleri.
// node van-gogh/blender/klip.js [ad,…] → klip_<ad>/eklem.json, kamera.json, kostum.json; sonra: bash van-gogh/blender/klip.sh <ad>
// Her klip 8 sn, 15 kare/sn (121 kare); duruş klipleri 8 sn'de döngü yapar (nefes ve ağırlık aktarımı periyodik).
// Kamera: göz 1.6 m, figür 4 m ötede; sırttan ¾ (yüz görünmez). Işık: önden-yandan yumuşak gün ışığı (iç mekânda da aynı; kenar ışığını figurDarbe verir).
const I = require('../../araclar/manken/iskelet.js'), HR = require('../../araclar/hareket/hareket.js'), V = I.V, fs = require('fs'), path = require('path');
const sm = (a, b, x) => { const u = Math.max(0, Math.min(1, (x - a) / (b - a))); return u * u * (3 - 2 * u); };
const TAU = Math.PI * 2, N = 121;
const KOS = {
  theo: { giysi: 'ceket', sapka: false, atki: false, canta: false, renk: { palto: [.09, .085, .1], pantolon: [.08, .075, .085], sac: [.09, .07, .055] } },
  theo_dis: { giysi: 'palto', sapka: false, atki: false, canta: false, renk: { palto: [.1, .095, .11], pantolon: [.08, .075, .085], sapka: [.08, .07, .07], sac: [.09, .07, .055] } },
  vincent: { giysi: 'ceket', sapka: 'hasir', atki: false, canta: false, renk: { palto: [.16, .17, .2], pantolon: [.12, .11, .1], sac: [.28, .16, .08] } },
  gauguin: { giysi: 'ceket', sapka: 'bere', atki: false, canta: true, renk: { palto: [.2, .16, .12], pantolon: [.13, .12, .11], sapka: [.12, .1, .09], sac: [.1, .08, .06] } },   // v3: kalçada biten ceket, bere (bileğe inen palto + düz geniş şapka papaz okunuyordu)
  jo: { giysi: 'elbise', sapka: false, atki: false, canta: false, sac: 'topuz', renk: { elbise: [.22, .21, .2], palto: [.22, .21, .2], pantolon: [.18, .17, .16], sac: [.12, .08, .06] } },   // v2: koyu siluet (açık gri elbise hayalet okunuyordu)
  jo_b: { giysi: 'elbise', sapka: false, atki: false, canta: false, sac: 'topuz', bebek: true, renk: { elbise: [.22, .21, .2], palto: [.22, .21, .2], pantolon: [.18, .17, .16], sac: [.12, .08, .06] } },
};
const ISIK = { gunes: { yon: [-.5, .7, .5], guc: 1.3, renk: [1, .95, .88] }, ortam: .12 };   // koyu siluet: biçim yalnız yumuşak bir yan ışıkla
// klip: {kos, kamera (konum/hedef/fov), poz(t) → poz}
const YER = [0, -4], ARKA = Math.PI * .82;   // figür kameraya sırtı ¾ dönük (yaw: yüzün baktığı yön; π = kameradan uzağa)
const nefes = (p, t, a = 1) => { const w = Math.sin(t * TAU / 8); p.kok = [p.kok[0] + .014 * w * a, p.kok[1] - .003, p.kok[2]]; p.yan = (p.yan || 0) + .02 * w * a; p.gogusEgim = (p.gogusEgim || 0) + .01 * Math.sin(t * TAU / 4) * a; return p; };
const KAM = { konum: [0, 1.45, -1], hedef: [0, .95, -4], fov: 40 };   // figür 3 m ötede: karenin ~%80'i
const g = HR.yuruyus({ tip: 'yuru' });
const yuru = (yaw, bas, hiz = 1) => { const yol = HR.yuruyusYolu(g, { t0: -1, t1: 9, x0: 0, olcek: hiz, go: () => 1 }); return t => I.yuruyus3B(yol, t, { bas, yaw, kolGenlik: .26 }); };
// v3 yardımcıları: yaw yönünde ileri (f) ve sağ (r); kol hedefi dünya koordinatında
const FR = yaw => ({ f: [Math.sin(yaw), 0, Math.cos(yaw)], r: [Math.cos(yaw), 0, -Math.sin(yaw)] });
const nok = (yer, yaw, ileri, yan, y) => { const { f, r } = FR(yaw); return [yer[0] + f[0] * ileri + r[0] * yan, y, yer[1] + f[2] * ileri + r[2] * yan]; };
const lerp3 = (a, b, u) => a.map((v, i) => v + (b[i] - v) * u);
const KLIP = {
  theo_dur: { kos: 'theo', poz: t => nefes(I.POZ.dur(YER, ARKA, { basEgim: .1, basDon: .06 * Math.sin(t * TAU / 8) }), t) },
  theo_dis_dur: { kos: 'theo_dis', poz: t => nefes(I.POZ.dur(YER, ARKA, { basEgim: .06 }), t) },
  vincent_dur: { kos: 'vincent', poz: t => nefes(I.POZ.dur(YER, Math.PI * .9, { basEgim: .04, basDon: -.05 * Math.sin(t * TAU / 8) }), t) },
  jo_dur: { kos: 'jo', poz: t => nefes(I.POZ.dur(YER, Math.PI * .78, { basEgim: .08 }), t, .7) },
  theo_oku: { kos: 'theo', poz: t => nefes(I.POZ.oku([0, -3.6], Math.PI * .85, .76, (t % 8) / 8, { basEgim: .5 }), t, .4) },
  vincent_oku: { kos: 'vincent', poz: t => nefes(I.POZ.oku([0, -3.6], Math.PI * .8, .7, (t % 8) / 8, { basEgim: .55 }), t, .4) },   // G02: beşiğe eğilir (beşik kadraj dışında)
  // v3: Jo bebeği omzunda taşır (sırttan ¾; bebeğin başı omzun üstünden görünür)
  jo_bebek: { kos: 'jo_b', poz: t => { const yaw = Math.PI * .86, p = nefes(I.POZ.dur(YER, yaw, { basEgim: .12, basDon: .15 }), t, .7); p.kol = [{ hedef: nok(YER, yaw, .12, .2, 1.1) }, { hedef: nok(YER, yaw, .14, .1, 1.36) }]; return p; } },
  // v3 G05: Jo beşiğe eğilir (2–3,5 sn arası eğilir, kalır)
  jo_egil: { kos: 'jo', poz: t => { const yaw = Math.PI * 1.2, u = sm(2, 3.5, t), p = nefes(I.POZ.dur(YER, yaw, { basEgim: .08 + .45 * u }), t, .5); p.egim = .02 + .42 * u; p.gogusEgim = .1 * u;
    p.kol = [{ hedef: lerp3(nok(YER, yaw, .04, .22, .8), nok(YER, yaw, .5, .12, .62), u) }, { hedef: lerp3(nok(YER, yaw, .04, -.22, .8), nok(YER, yaw, .5, -.12, .64), u) }]; return p; } },
  // v3 G05: Theo pencereye (ekranın soluna) döner (2–4 sn)
  theo_don: { kos: 'theo', poz: t => nefes(I.POZ.dur(YER, ARKA + (Math.PI * 1.25 - ARKA) * sm(2, 4, t), { basEgim: .1 }), t) },
  // v3 G02: Vincent başını beşiğe eğer, 2–3,2 sn arası sol eliyle örtünün ucunu gösterir (beşik ekranda solunda)
  vincent_goster: { kos: 'vincent', poz: t => { const yaw = Math.PI * .9, u = sm(2, 3.2, t), p = nefes(I.POZ.dur(YER, yaw, { basEgim: .22 + .12 * u }), t);
    p.kol[0] = { hedef: lerp3(nok(YER, yaw, .02, .21, .8), nok(YER, yaw, .2, .5, .74), u) }; return p; } },
  // v3 D06: Theo Jo'ya (ekranın sağına) dönük; 2–3 sn arası sağ koluyla yazı masasını gösterir
  theo_goster: { kos: 'theo', poz: t => { const yaw = Math.PI * .66, u = sm(2, 3, t), p = nefes(I.POZ.dur(YER, yaw, { basEgim: .06 }), t);
    p.kol[1] = { hedef: lerp3(nok(YER, yaw, .02, -.21, .8), nok(YER, yaw, .42, -.34, .98), u) }; return p; } },
  // v3 D06: Jo Theo'ya (ekranın soluna) dönük
  jo_yan: { kos: 'jo', poz: t => nefes(I.POZ.dur(YER, Math.PI * 1.25, { basEgim: .1 }), t, .7) },
  // v3 F03: Theo eğilip bebeğe bakar (ekranın sağına dönük; tek figür eğilir)
  theo_egil: { kos: 'theo', poz: t => { const yaw = Math.PI * .68, u = sm(1, 2.5, t), p = nefes(I.POZ.dur(YER, yaw, { basEgim: .1 + .4 * u }), t, .5); p.egim = .02 + .25 * u; return p; } },
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
