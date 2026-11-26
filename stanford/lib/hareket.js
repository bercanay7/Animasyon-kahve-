// Kopya: araclar/hareket/hareket.js (MIT; kaynak ve lisans orada). Sunucu kökü frankenstein/ olduğu için buraya alındı; değiştirilmez.
// araclar/hareket/hareket.js: yürüyüş/koşu çözücüsü ve deterministik yay/sarkaç izleri.
// Kaynak: JDhruv14/line-art-animation (MIT, commit c43d698), lib/gait.ts ve lib/motion.ts'den düz JS'ye uyarlandı.
// Lisans metni: araclar/vendor/line-art-animation/LICENSE. Uyarlamalar: Türkçe adlar; yay ve sarkaç t'nin saf
// fonksiyonu (önceden sabit adımla simüle edilir), çünkü render.js kareleri 4 işçide sırasız çizer.
//
// Mevcut motorlara dokunmaz: tek bir global (HAREKET) tanımlar, başka ad sızdırmaz. core.js'teki clamp/lerp/E ile çakışmaz.
//   <script src="../araclar/hareket/hareket.js"></script>   (film.html'de lib/core.js'ten sonra ya da önce; sıra fark etmez)
//
// FİGÜR UZAYI (bütün ölçüler bunu varsayar): ayaklar y = 120'de, kalça x = 40'ın üstünde, figür +x'e bakar, boy ≈ 95 birim.
// Sahneye HAREKET.yerlestir(ctx, x, zeminY, yon, olcek) ile konur; bütün çizimler bu dönüşümün içinde yapılır.
(function (kok) {
  'use strict';
  const sinirla = (x, a, b) => Math.max(a, Math.min(b, x));
  const yumusak = (e0, e1, x) => { const t = sinirla((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t); };
  const rampa = (t, a, b) => yumusak(a, b, t);
  const minJerk = s => s * s * s * (10 - 15 * s + 6 * s * s);

  // İki kemikli ters kinematik: diz hep öne kırılır (+x).
  function diz(kalca, bilek, l1, l2) {
    const dx = bilek[0] - kalca[0], dy = bilek[1] - kalca[1];
    const d = Math.min(Math.hypot(dx, dy), l1 + l2 - 0.01);
    const th = Math.atan2(dy, dx);
    const al = Math.acos(sinirla((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1));
    const c1 = [kalca[0] + l1 * Math.cos(th - al), kalca[1] + l1 * Math.sin(th - al)];
    const c2 = [kalca[0] + l1 * Math.cos(th + al), kalca[1] + l1 * Math.sin(th + al)];
    return c1[0] > c2[0] ? c1 : c2;
  }

  // tur: bir sol+sağ döngüsü (sn) · basma: ayağın yerde kaldığı pay · adim: basan ayağın gövde altında kat ettiği yol
  // kalkis: salınımda ayağın en yüksek kalkışı · topuk: topuk kalkarken ayak ucunun derece eğimi · tekme: koşuda topuğun geri savrulması
  // bilekY: düz ayakta bilek yüksekliği (ayakkabı 118.4; takunya/sandalet 116) · parmak: bilek-parmak ucu mesafesi
  const AYAR = {
    yuru:  { tur: 1.0, basma: 0.62, adim: 24, kalkis: 3.4, topuk: 15, tekme: 0,   uyluk: 23, baldir: 23, bilekY: 118.4, zemin: 120, parmak: 4.2 },
    surun: { tur: 0.9, basma: 0.64, adim: 18, kalkis: 2.4, topuk: 12, tekme: 0,   uyluk: 23, baldir: 23, bilekY: 116,   zemin: 120, parmak: 4.2 }, // uzun etek, chiton, sandalet, yaşlı
    kos:   { tur: 0.5, basma: 0.36, adim: 16, kalkis: 12,  topuk: 10, tekme: 3.5, uyluk: 13, baldir: 13, bilekY: 118,   zemin: 120, parmak: 3 },   // çocuk boyu bacak; yetişkinde uyluk/baldir 23 ver
  };

  // Dört kural: basan ayak tam yürüme hızında geri kayar (yerde sabit kalır); salınım minimum sarsıntı eğrisiyle;
  // topuk salınımdan önce kalkar (ayak ucunda döner); kalça yüksekliği sinüsle değil basan bacakların erişiminden çözülür.
  function yuruyus(o = {}) {
    const tip = o.tip || 'yuru';
    const p = Object.assign({}, AYAR[tip], o, { tip });
    const { tur, basma, adim: S, kalkis, topuk, tekme, uyluk, baldir, bilekY, zemin, parmak } = p;
    const erisim = (uyluk + baldir) * 0.983;          // basan bacak neredeyse düz, tam değil
    const dinlenKalca = bilekY - erisim;
    const hiz = S / (basma * tur);                      // figür birimi / sn

    const ayak = u => {
      u = ((u % 1) + 1) % 1;
      if (u < basma) {
        const x = 40 + S / 2 - (S * u) / basma;
        const soy = yumusak(basma - 0.14, basma, u);
        const th = (topuk * soy * Math.PI) / 180;
        const px = x + parmak, py = zemin, ox = -parmak, oy = bilekY - zemin;
        return { bilek: [px + ox * Math.cos(th) - oy * Math.sin(th), py + ox * Math.sin(th) + oy * Math.cos(th)], egim: topuk * soy, basiyor: true };
      }
      const s = (u - basma) / (1 - basma);
      const x = 40 - S / 2 + S * minJerk(s) - tekme * Math.sin(Math.PI * Math.min(1, s * 1.6));
      const y = bilekY - kalkis * Math.pow(Math.sin(Math.PI * Math.pow(s, tekme ? 0.7 : 1)), 1.2);
      return { bilek: [x, y], egim: topuk * Math.pow(1 - yumusak(0, 0.55, s), 1.4), basiyor: false };
    };

    return Object.assign(p, {
      hiz,
      // faz: döngü cinsinden; go ∈ [0,1] iki ayağı duruşa karıştırır (eğilmek, el sallamak için durma)
      poz(faz, go = 1) {
        const ham = [ayak(faz), ayak(faz + 0.5)];
        if (go < 1) ham.forEach((a, i) => {
          const r = 40 + (i ? -2 : 2);
          a.bilek = [r + (a.bilek[0] - r) * go, bilekY + (a.bilek[1] - bilekY) * go];
          a.egim *= go; a.basiyor = true;
        });
        let kY = dinlenKalca;
        const yarim = (((faz % 0.5) + 0.5) % 0.5);
        if (tekme && go >= 1) {
          kY = yarim < basma ? dinlenKalca + 1.4 * Math.sin((Math.PI * yarim) / basma)
                             : dinlenKalca - 2.6 * Math.sin((Math.PI * (yarim - basma)) / (0.5 - basma));
        } else {
          for (const a of ham) if (a.basiyor) {
            const dx = a.bilek[0] - 40;
            kY = Math.max(kY, a.bilek[1] - Math.sqrt(Math.max(1, erisim * erisim - dx * dx)));
          }
        }
        const kalca = [40, kY];
        const ayaklar = ham.map(a => Object.assign(a, { diz: diz(kalca, a.bilek, uyluk, baldir) }));
        const on = ayaklar[0].bilek[0] >= ayaklar[1].bilek[0] ? 0 : 1;   // öndeki bacak üstte çizilir
        return { kalca, ayaklar, on, inis: kY - dinlenKalca };
      },
    });
  }

  // Sabit adımlı örnek dizisinden doğrusal okuma (t aralık dışındaysa uçta kalır)
  const ornekle = (X, t0, fs) => t => {
    const f = (t - t0) * fs;
    if (f <= 0) return X[0];
    const i = Math.floor(f);
    if (i >= X.length - 1) return X[X.length - 1];
    return X[i] + (X[i + 1] - X[i]) * (f - i);
  };

  // Yürüyüş yolu: go(t) ∈ [0,1] (başlama/durma) integrali alınır; hem faz hem x aynı integralden gelir,
  // bu yüzden basan ayak yerde kayamaz. Saf fonksiyon: t'yi ver, konum + poz al.
  function yuruyusYolu(g, { t0 = 0, t1, x0 = 0, yon = 1, olcek = 1, go = () => 1, fs = 240 } = {}) {
    if (!(t1 > t0)) throw new Error('yuruyusYolu: t1 > t0 olmalı');
    const n = Math.ceil((t1 - t0) * fs) + 1, M = new Float64Array(n);
    let onceki = sinirla(go(t0), 0, 1);
    for (let i = 1; i < n; i++) { const gv = sinirla(go(t0 + i / fs), 0, 1); M[i] = M[i - 1] + (onceki + gv) / 2 / fs; onceki = gv; }
    const m = ornekle(M, t0, fs);
    return t => {
      const mt = m(t), gv = sinirla(go(sinirla(t, t0, t1)), 0, 1);
      return { x: x0 + yon * g.hiz * olcek * mt, faz: mt / g.tur, go: gv, hiz: yon * g.hiz * olcek * gv, poz: g.poz(mt / g.tur, gv) };
    };
  }

  // Sönümlü yay: hedef(t)'yi gecikerek izler (kol, kol yeni, pelerin ucu, şapka, kulak). itmeler: [[t, hız], ...]
  function yayIzi({ hedef, k = 40, d = 6, x0, v0 = 0, t0 = 0, t1, fs = 240, itmeler = [] }) {
    const n = Math.ceil((t1 - t0) * fs) + 1, X = new Float64Array(n), it = itmeler.slice().sort((a, b) => a[0] - b[0]);
    let x = x0 ?? hedef(t0), v = v0, j = 0; X[0] = x;
    for (let i = 1; i < n; i++) {
      const t = t0 + i / fs;
      while (j < it.length && it[j][0] <= t) v += it[j++][1];
      v += (k * (hedef(t) - x) - d * v) / fs; x += v / fs; X[i] = x;
    }
    return ornekle(X, t0, fs);
  }

  // Sarkaç (açı, radyan): asılı şeyler (fener, çanta, kandil, zincir, perde). kuvvet(t): rüzgâr, taşıyanın ivmesi
  function sarkacIzi({ kuvvet = () => 0, k = 10, d = 1.1, a0 = 0, v0 = 0, t0 = 0, t1, fs = 240, itmeler = [] }) {
    const n = Math.ceil((t1 - t0) * fs) + 1, A = new Float64Array(n), it = itmeler.slice().sort((a, b) => a[0] - b[0]);
    let a = a0, v = v0, j = 0; A[0] = a;
    for (let i = 1; i < n; i++) {
      const t = t0 + i / fs;
      while (j < it.length && it[j][0] <= t) v += it[j++][1];
      v += (-a * k + kuvvet(t) - v * d) / fs; a += v / fs; A[i] = a;
    }
    return ornekle(A, t0, fs);
  }

  // Taşıyanın ivmesi (sarkaca kuvvet olarak verilir): yol fonksiyonundan sayısal türev
  const ivme = (yol, h = 1 / 120) => t => (yol(t + h).hiz - yol(t - h).hiz) / (2 * h);

  // Adlı pozlar dizisi: [['otur', 0.7], ['esne', 0.9], ...] → t => { once, sonra, u } ya da null (bitti)
  function sira(adimlar) {
    const top = adimlar.reduce((a, s) => a + s[1], 0);
    return t => {
      if (t < 0 || t >= top) return null;
      let acc = 0, onceki = adimlar[0][0];
      for (const [ad, d] of adimlar) { if (t < acc + d) return { once: onceki, sonra: ad, u: (t - acc) / d }; acc += d; onceki = ad; }
      return null;
    };
  }

  // Katmanlı sinüs: döngü gibi okunmayan boşta salınım (nefes, alev, su)
  const kipir = (t, k = 1) => Math.sin(t * 1.3 * k) * 0.6 + Math.sin(t * 2.7 * k + 1.7) * 0.3 + Math.sin(t * 5.1 * k + 4.1) * 0.1;

  // Tohumlu rastgele: statik çizim her yüklemede aynı (render içinde Math.random yasak)
  function tohumlu(tohum = 11) { let s = tohum; return (a = 0, b = 1) => { s = (s * 16807) % 2147483647; return a + ((s - 1) / 2147483646) * (b - a); }; }

  // Figür uzayından sahneye: (40, 120) → (x, zeminY); yon = 1 sağa, -1 sola
  function yerlestir(ctx, x, zeminY, yon = 1, olcek = 1) { ctx.translate(x, zeminY); ctx.scale(yon * olcek, olcek); ctx.translate(-40, -120); }

  const HAREKET = { AYAR, yuruyus, yuruyusYolu, yayIzi, sarkacIzi, ivme, sira, kipir, tohumlu, yerlestir, diz, rampa, minJerk, yumusak };
  if (typeof module !== 'undefined' && module.exports) module.exports = HAREKET;
  kok.HAREKET = HAREKET;
})(typeof window !== 'undefined' ? window : globalThis);
