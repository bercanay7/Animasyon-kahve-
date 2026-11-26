// araclar/manken/iskelet.js: 3B manken iskeleti, ters kinematik ve poz kütüphanesi (saf matematik; tarayıcı + node).
// Çizim yok: poz → kemik çerçeveleri (dünya uzayı). Çizimi manken.js yapar. Tek global: ISKELET.
//
// Dünya: metre, Y yukarı. Figür yaw açısıyla döner: ileri f = (sin yaw, 0, cos yaw), yan y = (cos yaw, 0, -sin yaw).
// Yürüyüş araclar/hareket/hareket.js'ten gelir (2B çözücü, figür birimi); ISKELET.yuruyus3B onu 3B'ye taşır.
// Ölçek: çözücünün uyluk/baldır 23 birimi = 0,44 m, yani S = 0,44 / 23 m/birim. Bacak boyları aynı tutulduğu için
// çözücünün bilek konumları 3B'de de bacak boyuyla tutarlıdır; basan ayak dünyada sabit kalır (test.js).
(function (kok) {
  'use strict';
  // ---------- vektör ----------
  const V = {
    add: (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]],
    sub: (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]],
    mul: (a, k) => [a[0] * k, a[1] * k, a[2] * k],
    dot: (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2],
    cross: (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]],
    len: a => Math.hypot(a[0], a[1], a[2]),
    norm: a => { const l = Math.hypot(a[0], a[1], a[2]) || 1; return [a[0] / l, a[1] / l, a[2] / l]; },
    lerp: (a, b, u) => [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u],
    // Rodrigues: v'yi birim eksen k etrafında a radyan döndür
    rot: (v, k, a) => { const c = Math.cos(a), s = Math.sin(a), d = V.dot(k, v), x = V.cross(k, v);
      return [v[0] * c + x[0] * s + k[0] * d * (1 - c), v[1] * c + x[1] * s + k[1] * d * (1 - c), v[2] * c + x[2] * s + k[2] * d * (1 - c)]; },
  };
  const UP = [0, 1, 0];
  // çerçeve: {o, x, y, z} (dik birim eksenler). Döndürme yerel eksen etrafında.
  const cer = (o, x, y, z) => ({ o, x, y, z });
  const cerDon = (c, k, a) => cer(c.o, V.rot(c.x, k, a), V.rot(c.y, k, a), V.rot(c.z, k, a));
  // a→b doğrultusunda kemik çerçevesi: y = doğrultu, x = ref'in dik bileşeni
  function kemik(a, b, ref) {
    const y = V.norm(V.sub(b, a));
    let x = V.sub(ref, V.mul(y, V.dot(ref, y)));
    if (V.len(x) < 1e-6) x = Math.abs(y[0]) < .9 ? [1, 0, 0] : [0, 0, 1];
    x = V.norm(x); const z = V.cross(x, y);
    return cer(a, x, y, z);
  }
  // İki kemikli 3B ters kinematik: kök A, hedef T, boylar l1 l2, kutup p (eklemin kıvrılacağı yön)
  function ik2(A, T, l1, l2, p) {
    const dv = V.sub(T, A), d0 = V.len(dv), d = Math.max(Math.abs(l1 - l2) + 1e-4, Math.min(d0, l1 + l2 - 1e-4));
    const u = V.norm(dv);
    let pp = V.sub(p, V.mul(u, V.dot(p, u)));
    if (V.len(pp) < 1e-6) pp = Math.abs(u[1]) < .9 ? [0, 1, 0] : [1, 0, 0];
    pp = V.norm(pp);
    const a = (l1 * l1 + d * d - l2 * l2) / (2 * d), h = Math.sqrt(Math.max(0, l1 * l1 - a * a));
    const J = V.add(V.add(A, V.mul(u, a)), V.mul(pp, h));
    const uc = V.add(A, V.mul(u, d));                 // erişilemeyen hedefte uç: kol doğrultusunda en uzak nokta
    return { J, uc };
  }

  // ---------- ölçüler (metre) ----------
  const S = 0.44 / 23;                                  // çözücü birimi → metre
  const OLCU = {
    S, uyluk: 0.44, baldir: 0.44, kalcaYan: 0.085, ayakYan: 0.085,
    karin: 0.24, gogus: 0.28, boyun: 0.07, bas: 0.25,
    omuzYan: 0.165, omuzY: 0.235, pazu: 0.30, onkol: 0.26, el: 0.17,
    kalcaY: (120 - (118.4 - 46 * 0.983)) * S,            // duruşta kalça eklemi yüksekliği (~0,895 m)
  };

  // ---------- poz → kemikler ----------
  // poz: { kok:[x,y,z] pelvis ortası (kalça eklemleri hizası), yaw, egim (karın öne eğim, rad), gogusEgim, burk (göğüs burkulma),
  //        yan (yana eğim), basEgim (+ aşağı bakar), basDon, ayak:[{bilek, egim(°)}, {…}],
  //        kol:[{hedef:[x,y,z]} | {salla, dirsek, aci}, …]   (0 = sağ yan, 1 = sol yan; yan = +y ekseni sağ kabul)
  function kemikler(poz) {
    const O = OLCU, yaw = poz.yaw || 0;
    const f = [Math.sin(yaw), 0, Math.cos(yaw)], r = [Math.cos(yaw), 0, -Math.sin(yaw)];
    let pel = cer(poz.kok, r, UP, f);
    pel = cerDon(pel, r, poz.egim || 0);              // öne eğilme: y ekseni f'ye doğru (sağ el kuralı r etrafında)
    if (poz.yan) pel = cerDon(pel, pel.z, poz.yan);
    if (poz.kalcaBurk) pel = cerDon(pel, UP, poz.kalcaBurk);
    const gb = V.add(pel.o, V.mul(pel.y, O.karin));
    let gog = cer(gb, pel.x, pel.y, pel.z);
    gog = cerDon(gog, gog.x, poz.gogusEgim || 0);
    gog = cerDon(gog, gog.y, poz.burk || 0);
    const boyunA = V.add(gog.o, V.mul(gog.y, O.gogus));
    let boy = cer(boyunA, gog.x, gog.y, gog.z);
    boy = cerDon(boy, boy.x, (poz.basEgim || 0) * .35);
    const basA = V.add(boy.o, V.mul(boy.y, O.boyun));
    let bas = cer(basA, boy.x, boy.y, boy.z);
    bas = cerDon(bas, bas.y, poz.basDon || 0);
    bas = cerDon(bas, bas.x, (poz.basEgim || 0) * .65);
    if (poz.basYan) bas = cerDon(bas, bas.z, poz.basYan);
    const K = { pelvis: pel, gogus: gog, boyun: boy, bas, bacak: [], kol: [] };
    // bacaklar: diz öne (pelvis z) kıvrılır
    for (let i = 0; i < 2; i++) {
      const sg = i ? -1 : 1;
      const kal = V.add(pel.o, V.mul(pel.x, sg * O.kalcaYan));
      const a = poz.ayak[i], b = a.bilek;
      const kut = V.add(V.mul([Math.sin(yaw), 0, Math.cos(yaw)], 1), V.mul(UP, .05));
      const { J: diz, uc } = ik2(kal, b, O.uyluk, O.baldir, kut);
      const fy = [Math.sin(yaw + (a.don || 0)), 0, Math.cos(yaw + (a.don || 0))], ry = [fy[2], 0, -fy[0]];
      let ay = cer(uc, ry, UP, fy);
      ay = cerDon(ay, ry, -(a.egim || 0) * Math.PI / 180);       // topuk kalkar: ayak ucu aşağı
      K.bacak.push({ kalca: kal, diz, bilek: uc, uyluk: kemik(kal, diz, pel.x), baldir: kemik(diz, uc, pel.x), ayak: ay });
    }
    // kollar
    for (let i = 0; i < 2; i++) {
      const sg = i ? -1 : 1, k = (poz.kol && poz.kol[i]) || {};
      const om = V.add(V.add(gog.o, V.mul(gog.y, O.omuzY)), V.mul(gog.x, sg * O.omuzYan));
      let dirsek, bilek;
      if (k.hedef) {
        const kut = V.norm(V.add(V.add(V.mul(gog.z, -.7), V.mul(gog.x, sg * .55)), V.mul(gog.y, -.25)));
        const s = ik2(om, k.hedef, O.pazu, O.onkol, k.kutup || kut);
        dirsek = s.J; bilek = s.uc;
      } else {
        // ileri-geri sallanma (göğüs x ekseni etrafında) + yana açılma; dirsek öne kıvrılır
        let d = V.mul(gog.y, -1);
        d = V.rot(d, gog.z, sg * (k.aci ?? .07));
        d = V.rot(d, gog.x, -(k.salla || 0));
        dirsek = V.add(om, V.mul(d, O.pazu));
        const d2 = V.rot(d, gog.x, -(k.dirsek ?? .25));
        bilek = V.add(dirsek, V.mul(d2, O.onkol));
      }
      const ond = V.norm(V.sub(bilek, dirsek));
      const elUc = V.add(bilek, V.mul(ond, O.el));
      K.kol.push({ omuz: om, dirsek, bilek, pazu: kemik(om, dirsek, gog.z), onkol: kemik(dirsek, bilek, gog.z), el: kemik(bilek, elUc, gog.x) });
    }
    return K;
  }

  // ---------- yürüyüş: HAREKET (2B, figür birimi) → 3B ----------
  // yol: HAREKET.yuruyusYolu(g, {x0: 0, olcek: 1, ...}) (x figür biriminde); bas: [x, z] başlangıç; yaw: yürüme yönü
  function yuruyus3B(yol, t, { bas = [0, 0], yaw = 0, kolGenlik = .32 } = {}) {
    const y = yol(t), p = y.poz;
    const f = [Math.sin(yaw), 0, Math.cos(yaw)], r = [Math.cos(yaw), 0, -Math.sin(yaw)];
    const G = [bas[0] + f[0] * y.x * S, 0, bas[1] + f[2] * y.x * S];
    const kok = [G[0], (120 - p.kalca[1]) * S, G[2]];
    const ayak = p.ayaklar.map((a, i) => {
      const sg = i ? -1 : 1, ileri = (a.bilek[0] - 40) * S;
      return { bilek: [G[0] + f[0] * ileri + r[0] * sg * OLCU.ayakYan, (120 - a.bilek[1]) * S, G[2] + f[2] * ileri + r[2] * sg * OLCU.ayakYan], egim: a.egim, basiyor: a.basiyor };
    });
    // kol karşı bacakla sallanır (bacağın ileri konumu oranında); kalça adımla hafif burkulur, göğüs ters
    const ad = 12;
    const ileri = i => (p.ayaklar[i].bilek[0] - 40) / ad;
    const kol = [0, 1].map(i => ({ salla: kolGenlik * ileri(1 - i), dirsek: .22 + .18 * Math.max(0, ileri(1 - i)) }));
    const burk = .07 * (ileri(0) - ileri(1)) * .5;
    return { kok, yaw, egim: .05 * y.go, gogusEgim: .02, kalcaBurk: -burk, burk: burk * 1.6, ayak, kol, basEgim: .06, _y: y };
  }

  // ---------- poz karıştırma (iki poz arasında; bilek ve kök doğrusal, açılar doğrusal) ----------
  const SAY = ['yaw', 'egim', 'gogusEgim', 'burk', 'yan', 'kalcaBurk', 'basEgim', 'basDon', 'basYan'];
  function karistir(a, b, u) {
    const o = { kok: V.lerp(a.kok, b.kok, u) };
    for (const k of SAY) o[k] = (a[k] || 0) + ((b[k] || 0) - (a[k] || 0)) * u;
    o.ayak = [0, 1].map(i => ({ bilek: V.lerp(a.ayak[i].bilek, b.ayak[i].bilek, u), egim: (a.ayak[i].egim || 0) * (1 - u) + (b.ayak[i].egim || 0) * u, don: (a.ayak[i].don || 0) * (1 - u) + (b.ayak[i].don || 0) * u }));
    o.kol = [0, 1].map(i => {
      const ka = (a.kol || [])[i] || {}, kb = (b.kol || [])[i] || {};
      // hedefli ve açılı kolu karıştırmak için iki ucu da bilek konumuna çevir
      if (ka.hedef || kb.hedef) {
        const ha = ka.hedef || kemikler(a).kol[i].bilek, hb = kb.hedef || kemikler(b).kol[i].bilek;
        return { hedef: V.lerp(ha, hb, u) };
      }
      return { salla: (ka.salla || 0) * (1 - u) + (kb.salla || 0) * u, dirsek: (ka.dirsek ?? .25) * (1 - u) + (kb.dirsek ?? .25) * u, aci: (ka.aci ?? .07) * (1 - u) + (kb.aci ?? .07) * u };
    });
    return o;
  }

  // ---------- poz kütüphanesi (hepsi tam boy karede taranır: deneme.html?poz=ad) ----------
  // yer: [x, z] ayakların ortası; yaw
  function ileriYan(yaw) { return { f: [Math.sin(yaw), 0, Math.cos(yaw)], r: [Math.cos(yaw), 0, -Math.sin(yaw)] }; }
  const ayakDur = (yer, yaw, adimFark = 0) => { const { f, r } = ileriYan(yaw);
    return [0, 1].map(i => { const sg = i ? -1 : 1, il = (i ? -adimFark : adimFark) * .5; return { bilek: [yer[0] + r[0] * sg * OLCU.ayakYan + f[0] * il, (120 - 118.4) * S, yer[1] + r[2] * sg * OLCU.ayakYan + f[2] * il], egim: 0 }; }); };
  const POZ = {
    // ayakta duruş: kollar yanda, ağırlık hafif bir bacakta
    dur(yer, yaw, o = {}) {
      return { kok: [yer[0], OLCU.kalcaY - .012, yer[1]], yaw, egim: .02, yan: .025, gogusEgim: -.02, basEgim: o.basEgim ?? .08, basDon: o.basDon || 0,
        ayak: ayakDur(yer, yaw, .06), kol: [{ salla: .02, dirsek: .18 }, { salla: -.03, dirsek: .2 }] };
    },
    // masaya eğilme: iki el masada, kalça geri, baş aşağı (okur). masa: {y: üst yükseklik, on: masanın önüne olan uzaklık}
    egil(yer, yaw, masaY, o = {}) {
      const { f, r } = ileriYan(yaw), d = o.derin ?? .62, eg = o.egim ?? .78;
      const kok = [yer[0] - f[0] * .06, OLCU.kalcaY - .035, yer[1] - f[2] * .06];
      const el = (sg, ileri, yanA) => [yer[0] + f[0] * ileri + r[0] * sg * yanA, masaY + .015, yer[1] + f[2] * ileri + r[2] * sg * yanA];
      return { kok, yaw, egim: eg, gogusEgim: .14, yan: 0, basEgim: o.basEgim ?? .55, basDon: o.basDon || 0,
        ayak: ayakDur(yer, yaw, .1), kol: [{ hedef: el(1, d, .26) }, { hedef: el(-1, d - .04, .3) }] };
    },
    // eğilmiş, tek el sayfada ilerler (okuma): elX 0..1 sayfa boyunca
    oku(yer, yaw, masaY, elX = 0, o = {}) {
      const p = POZ.egil(yer, yaw, masaY, o), { f, r } = ileriYan(yaw);
      p.kol[0] = { hedef: [yer[0] + f[0] * (.5 + .12 * elX) + r[0] * (.12 - .1 * elX), masaY + .02 + .03 * Math.sin(Math.PI * elX), yer[1] + f[2] * (.5 + .12 * elX) + r[2] * (.12 - .1 * elX)] };
      return p;
    },
  };

  const ISKELET = { V, UP, OLCU, S, ik2, kemik, kemikler, yuruyus3B, karistir, POZ };
  if (typeof module !== 'undefined' && module.exports) module.exports = ISKELET;
  kok.ISKELET = ISKELET;
})(typeof window !== 'undefined' ? window : globalThis);
