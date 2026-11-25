// Bölme planları (başkan): yazı levhası ≤ 8 sn/plan ve toplamda ≤ 1/5 (CLAUDE.md). Uzun levhalı cümlelerde levha yalnız alıntının kendisi kadar kalır;
// cümlenin öbür kısmı bir sahneye keser. Sahneler mevcut setlerden: bodrum (a.js), SET.gozlemOdasi, yakinFig.
(() => {
  'use strict';
  const KK = { baski: { mod: 'kagit', kuru: .6 } };
  const yak = (st, z0 = 1.02, k = .012) => z0 + Math.min(st.lt, 14) * k;
  // C11 başı: gece koridoru, hareketsiz duran gardiyanlar (makale cümlesine giriş)
  sahne('P37b', 'C11', 'koridor', 'orta', (B, st) => {
    B.cam(1000, 560, yak(st, 1.12, .015));
    bodrum(B, st, { isik: .7, gardiyanlar: [{ z: .3, u: .15, f: -1, kol: [.1, .3] }, { z: .42, u: -.25, f: 1, kol: [-.1, .25] }, { z: .55, u: .4, f: -1, kol: [.2, .5] }] });
  }, VID);
  // C11 sonu ("Makale, iki gruba da..."): sayım, yürüyen sayan gardiyan
  sahne('P38b', 'C11@makale#1', 'koridor', 'genis', (B, st) => {
    B.cam(960, 540, yak(st, 1.0, .012));
    bodrum(B, st, { sayim: 5, sayan: { z: .32, x0: 700, v: 30 } });
  }, VID);
  // D04 ikinci yarısı: gözlem odası geniş; müdür konuşur (baş hafif oynar)
  sahne('P45b', 'D04@biraz', 'gozlem', 'genis', (B, st) => {
    B.cam(980, 500, yak(st));
    SET.gozlemOdasi(B, st, { mudurO: { bas: .06 + Math.sin(st.t * 2.2) * .03 } });
  }, KK);
  // D06 ikinci yarısı ("Sert derken..."): monitörde, sayımda dışarıda oturan gardiyan (geri çağrı)
  sahne('P47b', 'D06@sert#1', 'monitor', 'orta', (B, st) => {
    B.cam(960, 520, yak(st, 1.05, .015));
    SET.karanlik(B, .8);
    SET.monitorIci(B, 360, 140, 1200, 780, B2 => bodrum(B2, st, { sayim: 4, sayan: { z: .32, x0: 600, v: 30 }, kose: { z: .5, u: .86 } }));
  }, KK);
  // D14 sonu ("Mark'ın son cevabına ... döneceğiz"): gözlem odası; makaralar durur, lamba yanık kalır
  sahne('P57b', 'D14@markın', 'gozlem', 'orta', (B, st) => {
    B.cam(1060, 480, yak(st, 1.25, .01));
    const dur = st.at + .6, ang = Math.min(st.t, dur) * .45 * TAU + (st.t > dur ? (1 - Math.exp(-(st.t - dur) * 2)) * .4 : 0);
    SET.gozlemOdasi(B, st, { ang, vu: st.t > dur ? .05 : .4 });
  }, KK);
  // D15 başı: müdür yalnız, karanlıkta (yazdıklarına giriş)
  sahne('P58a', 'D15', 'mudur', 'yakin', (B, st) => {
    B.cam(960, 540, yak(st, 1.02, .015));
    SET.karanlik(B, .8); SET.koni(B, 1500, -100, 120, 1000, 700, { a: .55, tohum: 6 });
    yakinFig(B, 'mudur', 820, 330, 2200, { f: 1, bas: .14 + Math.sin(st.t * .7) * .02 });
  }, KK);
  // D17 başı: gözlem odası boş masa, monitörde sakin sayım (Zimbardo'nun cevabına giriş)
  sahne('P60b', 'D17', 'gozlem', 'orta', (B, st) => {
    B.cam(900, 480, yak(st, 1.12, .012));
    SET.gozlemOdasi(B, st, { mudur: false, mark: false, isik: .7 });
  }, KK);
  // E03 başı ("Kırk yıl sonra, 2011'de"): gece koridoru, tek uzun siluet uzaklaşır
  sahne('P66b', 'E03', 'gece', 'genis', (B, st) => {
    B.cam(960, 540, yak(st));
    const K = bodrum(B, st, { isik: .55 });
    const z = .3 + st.lt * .04, p = K.yer(z, .1);
    FIG.kisi(B.l, p[0], p[1], 760 * K.olc(z), { tip: 'gardiyan', f: -1, kolO: [.1, .3], kolA: [-.1, .25], bas: .03 });
  }, VID);
  // E06 başı: Eshelman yakın, gece (pişmanlık alıntısına giriş)
  sahne('P69b', 'E06', 'gece', 'yakin', (B, st) => {
    B.cam(960, 540, yak(st, 1.02, .015));
    const k = B.k; k.save(); k.fillStyle = B.ton(.62); k.fillRect(-300, -300, 2600, 1700); k.restore();
    yakinFig(B, 'gardiyan', 900, 330, 2300, { f: 1, bas: .16 + Math.sin(st.t * .6) * .02 });
  }, VID);
  // E11 başı: gündüz koridoru, dışarıda oturan gardiyan (Mark)
  sahne('P76b', 'E11', 'koridor', 'orta', (B, st) => {
    B.cam(1150, 560, yak(st, 1.25, .015));
    bodrum(B, st, { sayim: 3, kose: { z: .5, u: .86 } });
  }, VID);
  // E13 başı: gündüz koridoru; gardiyanlar sakin (iyi gardiyanlar), sayım
  sahne('P79b', 'E13', 'koridor', 'genis', (B, st) => {
    B.cam(960, 540, yak(st));
    bodrum(B, st, { sayim: 5, gardiyanlar: [{ z: .5, u: .3, f: -1, kol: [.1, .3] }], sayan: { z: .3, x0: 650, v: 26 } });
  }, VID);
  // F01 başı ("Bu sertliği isteyen müdür ... şunu yazmış"): gözlem odasında müdür yalnız
  sahne('P84a', 'F01', 'gozlem', 'genis', (B, st) => {
    B.cam(1000, 500, yak(st));
    SET.gozlemOdasi(B, st, { mark: false, isik: .8 });
  }, KK);
})();
