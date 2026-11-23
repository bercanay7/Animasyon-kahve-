// D: Duvardaki yarık (D01–D13; yaratığın kendi ağzından: ışığın merkezi onda). Sahibi: başkan.
'use strict';
(() => {
  const rel = (st, at) => A(at) - st.at;
  window.ORMAN_GECE = (R, st, o = {}) => {
    R.gok(-800, -400, 3600, 1000, [[0, '#2C3A66'], [.7, '#4C5E8E'], [1, '#6E7B9E']], { firca: 1.1 });
    if (o.ay) DK.ay(R, o.ay[0], o.ay[1], o.ay[2] || 60);
    for (let i = 0; i < 9; i++) DK.cam(R, -600 + i * 430 + (i % 3) * 60, 900, 520 + (i % 4) * 90, { tohum: 30 + i, sal: Math.sin(st.t * .6 + i) * .5 });
    R.yika(g => g.rect(-800, 880, 4400, 600), '#3A4A3A', { firca: 1 });
    R.kara(g => { g.moveTo(-800, 900); for (let x = -800; x <= 3600; x += 80) g.lineTo(x, 890 + Math.sin(x * .013) * 10); g.lineTo(3600, 1400); g.lineTo(-800, 1400); g.closePath(); });
  };
  // D02: ormanda yürür; "yükseldi"de ay ağaçların arasından yükselir; yaratık durur ve bakar
  sahne('D02a', 'D02', 'orman', 'genis', (R, st) => {
    const tY = rel(st, 'D02@yükseldi'), tA = rel(st, 'D02@ayıramadım');
    const go = t => HAREKET.rampa(t, 0, .4) * (1 - HAREKET.rampa(t, tY + .2, tY + .9));
    const g = HAREKET.yuruyus({ tip: 'yuru', tur: 1.25 });
    const yol = HAREKET.yuruyusYolu(g, { t0: 0, t1: 30, x0: 420, olcek: 7.4, go });
    const y = yol(st.lt);
    const ayY = lerp(780, 300, E.out3(clamp((st.lt - tY) / 2.6)));
    R.cam(900 + y.x * .3, 540, 1);
    ORMAN_GECE(R, st, { ay: [1320, ayY, 70] });
    const bak = E.io3(clamp((st.lt - tY - .4) / 1.2));
    FIG.kisi(R, y.x, 900, 640, { tip: 'yaratik', f: 1, bacak: y.poz, bas: -bak * .35, govde: .08 - bak * .06, kolO: [.15 + Math.sin(TAU * y.faz) * .3 * y.go + bak * .25, .35], kolA: [-.1 - Math.sin(TAU * y.faz) * .3 * y.go, .3], pel: Math.sin(st.lt * 2) * .5 });
    window.SERIT_ODAK = () => [y.x - (900 + y.x * .3) + 960, 680];
  }, { fener: st => ({ isik: { x: 960, y: 520, r: 760, sic: [.95, .95, 1] }, kadraj: { tip: 'kare', x: 960, y: 520, w: 1760, h: 960, r: 70, yum: 24 } }) });
})();
