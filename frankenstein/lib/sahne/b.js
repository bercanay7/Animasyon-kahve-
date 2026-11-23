// B: Yazsız yıl (B01–B16). Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  // Cenevre Gölü, 1816 Haziran gecesi: Jura'nın arkasında fırtına, göl, kıyıda villa
  window.GOL_GECE = (R, st, o = {}) => {
    const fl = o.simsek || 0;
    R.gok(-600, -400, 2600, 640, [[0, '#3C4C78'], [.55, '#6A7FAE'], [1, '#9AA6C4']], { firca: 1.2 });
    if (fl > 0) R.gok(-600, -400, 2600, 640, [[0, `rgba(255,255,255,${fl})`], [1, `rgba(255,255,255,${fl * .6})`]], { firca: 0, kay: 0 });
    // bulutlar (koyu boya, kat kat)
    for (let i = 0; i < 6; i++) { const cx = -300 + i * 480 + Math.sin(st.t * .05 + i) * 40, cy = 60 + (i % 2) * 70;
      R.yika(g => { g.ellipse(cx, cy, 380, 90, 0, 0, TAU); g.ellipse(cx + 200, cy + 40, 300, 80, 0, 0, TAU); }, 'rgba(70,78,110,.75)', { kay: 0 }); }
    DK.daglar(R, -600, 2600, 560, [[-300, 420], [200, 360], [700, 400], [1200, 330], [1700, 390], [2200, 350]], '#2E3654', {});
    DK.gol(R, -600, 2600, 560, 900, '#5D6F9E', '#2E3A5E', { t: st.t, yx: 1180, yw: 500, n: 30, yansima: 'rgba(255,226,160,.6)' });
    // kıyı ve villa (sağ)
    R.kara(g => { g.moveTo(700, 900); g.quadraticCurveTo(1100, 760, 1500, 740); g.lineTo(2600, 720); g.lineTo(2600, 1400); g.lineTo(700, 1400); g.closePath(); });
    DK.villa(R, 1560, 760, 520, {});
    for (const [x, h] of [[1180, 260], [1960, 320], [2100, 280]]) DK.cam(R, x, 770, h, { sal: Math.sin(st.t * .7) });
  };
  sahne('B01a', 'B01', 'gol', 'genis', (R, st) => {
    const tS = rel(st, 'B02@şimşek');
    R.cam(980 + st.lt * 9, 540, 1);
    const fl = DK.simsek(R, 760, -100, 420, (st.lt - tS) / 1.4, {});
    GOL_GECE(R, st, { simsek: fl });
    DK.simsek(R, 760, -100, 420, (st.lt - tS) / 1.4, {});
    DK.yagmur(R, st.t, { a: .28 });
  }, { fener: { isik: { x: 960, y: 480, r: 900, sic: [1, .93, .8] }, kadraj: { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 } } });
  // Mary masada, mum ışığında; arkada yağmurlu pencere (ışık dairesi Mary'de)
  window.ODA_DIODATI = (R, st) => {
    R.gok(-400, -300, 2400, 1400, [[0, '#8C6A4A'], [1, '#6A4E38']], { firca: 1.2 });
    DK.pencere(R, 1380, 380, 360, 520, { gece: '#5A6E9C' });
    R.yika(g => g.rect(-400, 880, 2800, 600), '#5A4030', { firca: 1 });
  };
  sahne('B03a', 'B03', 'oda', 'orta', (R, st) => {
    R.cam(980, 560, 1.05 + st.lt * .008);
    ODA_DIODATI(R, st);
    DK.yagmur(R, st.t, { a: .14, n: 60 });
    // masa
    R.kara(g => { g.rect(560, 640, 760, 26); g.rect(590, 660, 22, 330); g.rect(1270, 660, 22, 330); });
    const yaz = Math.sin(st.lt * 5) * .05;
    FIG.kisi(R, 520, 990, 520, { tip: 'mary', f: 1, bacak: 'otur', govde: .22, bas: .25, kolO: [1.25 + yaz, .9], kolA: [.95, 1.1] });
    R.kara(g => { g.rect(400, 700, 140, 18); g.rect(410, 600, 18, 390); g.rect(500, 710, 18, 280); });   // sandalye
    R.yika(g => g.rect(760, 628, 160, 12), '#EDE3C8', { kay: 0 });                                         // kâğıt
    DK.mum(R, 1080, 640, 150, { t: st.t });
  }, { fener: { isik: { x: 880, y: 560, r: 640, sic: [1, .88, .66] }, kadraj: { tip: 'oval', x: 900, y: 540, w: 1500, h: 980, yum: 40 } } });
})();
