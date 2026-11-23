// A: kanca (A01–A05). Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  // Victor'un yatak odası, gece: kepenk aralığından ay ışığı, perdeli yatak (sağda), kapı (solda)
  window.ODA_GECE = (R, st, o = {}) => {
    R.gok(-400, -300, 2400, 1400, [[0, '#4F6699'], [.6, '#6378A6'], [1, '#4A5272']], { firca: 1 });       // gece mavisi oda
    R.yika(g => g.rect(-400, 900, 2800, 600), '#7A5E48', { firca: .8 });                                   // döşeme
    DK.pencere(R, 560, 300, 260, 360, { gece: '#9DB2DA', kepenk: .55, ay: true });
    // kepenk aralığından yere düşen ışık şeridi (saydam, mavi)
    R.yika(g => { g.moveTo(530, 480); g.lineTo(590, 480); g.lineTo(820, 1100); g.lineTo(560, 1100); g.closePath(); }, 'rgba(225,232,250,.65)', { kay: 0, firca: 0 });
    // yatak (sağ): ağır perde, karyola
    R.kara(g => { g.rect(1260, 40, 26, 980); g.rect(1880, 40, 26, 980); g.rect(1240, 20, 700, 40); });
    R.kara(g => { g.rect(1270, 700, 640, 140); g.rect(1270, 830, 30, 190); g.rect(1880, 830, 30, 190); });
    R.yika(g => g.rect(1290, 640, 600, 70), '#B9B2A6', { firca: .6 });                                    // çarşaf
  };
  sahne('A01a', 'A01', 'oda', 'yakin', (R, st) => {
    const tU = rel(st, 'A01@uzatıyor'), tP = rel(st, 'A01@perdeyi');
    const z = 1.02 + st.lt * .01;
    R.cam(1200, 520, z);
    ODA_GECE(R, st);
    // Victor yatakta, uykuda; perdenin ardında yarı görünür
    FIG.yatan(R, 1600, 662, 560, { f: 1, nefes: Math.sin(st.lt * 1.6) * 1.2 });
    const pa = E.io3(clamp((st.lt - tP + .3) / 1.2));      // perde aralanır
    DK.perde(R, 1286 + pa * 230, 1520, 60, 700, '#B0433A', { t: st.lt * .3, kivrim: 6 });
    // yaratık: solda, perdeyi tutan arka kol ve uzanan ön kol (dirsek bükük)
    const ue = E.io3(clamp((st.lt - tU + .2) / 1.4));
    FIG.kisi(R, 1060, 1000, 700, { tip: 'yaratik', f: 1, govde: .1, bas: .08,
      kolA: [lerp(.9, 1.55, pa), lerp(.5, .1, pa)], kolO: [lerp(.2, 1.15, ue), lerp(.25, .45, ue)], sac: .2, goz: 1 });
  }, { fener: { isik: { x: 1100, y: 420, r: 560, sic: [1, .92, .78] }, kadraj: { tip: 'daire', x: 1010, y: 520, r: 520, yum: 30 } } });
})();
