// F: Tufandan kurtulan adam (F01–F12). Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at;
  const kiyi = (R, st) => { SET.zemin(R); SET.su(R, -900, 2900, 640, { faz: st.lt * .6, alt: 150 }); R.b.fillStyle = gv(.34); R.b.fillRect(-900, 780, 3800, 600); FIG.cizgi(R, [[-900, 780], [2900, 780]], 4, -.6); SET.yer(R, -900, 2900, 880, { z: .36 }); };
  // F01: kıyıda Utnapiştim; ikisi yüz yüze, aynı boyda
  sahne('F01a', 'F01', 'utna', 'orta', (R, st) => {
    K(R, st, [960, 520, 1.1], [960, 520, 1.16]);
    kiyi(R, st);
    FIG.fig(R, 1200, 880, 540, { tip: 'utna', f: -1, kol: [[.3, .4], [.1, .2]] });
    FIG.fig(R, 720, 880, 550, { tip: 'gilgamis', giysi: 'post', f: 1, kol: [[.2, .3], [.1, .2]] });
    R.L.dir = [-.55, -.55, .6];
  }, { tr: { type: 'muhur', dur: .8 } });
  sahne('F02a', 'F02', 'utna', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'gilgamis', f: 1, arka: 'su', kay: 30, fig: { giysi: 'post', bas: -.05 } });
    R.L.dir = [-.55, -.55, .6];
  });
  // F03: hatıra: tanrıların kararı, kamış duvardan fısıltı, ev söküldü, gemi
  sahne('F03a', 'F03', 'tufan', 'orta', (R, st) => {
    const tk = rel(st, 'F03@fısıldadı'), tg = rel(st, 'F03@gemi');
    K(R, st, [1250, 640, 1.2], [1300, 640, 1.25]);
    SET.zemin(R); DK.friz(R, -600, 2600, 120, 960);
    for (let i = 0; i < 4; i++) SET.tac(R, 400 + i * 230, 470, 180);
    DK.kamis(R, 1250, 870, 330, 9, .55);
    const p = clamp((st.lt - tg) / 2);
    if (p < .5) SET.ev(R, 1450, 870, 360, 300, {}); else DK.kayik(R, 1640, 860, 600 * E.out3((p - .5) * 2), {});
    FIG.fig(R, 1200, 875, 330, { tip: 'utna', f: -1, kol: [[st.lt > tk ? 1.0 : .2, .5], [.1, .2]] });
    SET.yer(R, -900, 2900, 870, { z: .36 });
    R.L.dir = [-.55, -.55, .6];
  }, { post: { vig: .95 } });
  // F04: tufan; "kile dönmüştü"de insanlar kile gömülür
  sahne('F04a', 'F04', 'tufan', 'genis', (R, st) => {
    const tk = rel(st, 'F04@kile'), p = clamp((st.lt - tk + .3) / 1.6);
    K(R, st, [960, 540, .88], [960, 540, .95]);
    SET.zemin(R);
    const POZ = [[[2.6, .5], [.4, .6]], [[.6, 1.4], [.2, .3]], [[2.9, .2], [2.4, .6]], [[1.0, 1.6], [.5, 1.2]], [[.3, .2], [2.7, .4]], [[2.2, 1.0], [.1, .2]]];
    for (let i = 0; i < 6; i++) FIG.fig(R, 180 + i * 300 + (i % 2) * 60, 820 + (i % 3) * 45, 210 + (i % 2) * 30, { tip: i % 3 ? 'adam' : 'kadin', f: i % 2 ? 1 : -1, z: lerp(.68, .2, E.in2(p)), kol: POZ[i], bas: (i % 3 - 1) * .3, egilme: (i % 2 ? .3 : -.2) });
    const wy = lerp(980, 700, clamp(st.lt / 3));
    SET.su(R, -900, 2900, wy, { faz: st.lt * 2.5, a: 34, p: 220 });
    DK.kayik(R, 960 + Math.sin(st.lt) * 80, wy - 10 + Math.sin(st.lt * 2) * 20, 520, { z: .7 });
    const sim = Math.sin(st.lt * 11) > .92 && st.lt < tk ? 1 : 0;
    R.L.dir = [sim ? .3 : -.3, -.8, .5]; R.L.int = .45 + sim * 1.1; R.L.amb = .16; R.L.col = [.75, .8, .95];
  }, { mb: 2 });
  // F05: tanrılar ölümsüzlüğü bir kez verdi: güneşin altında Utnapiştim ve karısı
  sahne('F05a', 'F05', 'utna', 'orta', (R, st) => {
    K(R, st, [960, 520, 1.05], [960, 500, 1.1]);
    kiyi(R, st);
    DK.gunes(R, 960, 150, 70, { z: .55 });
    FIG.fig(R, 740, 880, 500, { tip: 'utna', f: 1, kol: [[.2, .3], [.1, .2]] });
    FIG.fig(R, 1180, 880, 470, { tip: 'kadin', f: -1, kol: [[.2, .3], [.1, .2]] });
    R.L.dir = [0, -.85, .5]; R.L.int = 1.1;
  });
  // F06: sınav
  sahne('F06a', 'F06', 'utna', 'yakin', (R, st) => {
    K(R, st, [1150, 470, 1.6], [1140, 470, 1.68]);
    kiyi(R, st);
    FIG.fig(R, 1200, 880, 540, { tip: 'utna', f: -1, kol: [[1.2 + Math.sin(st.lt * 2) * .1, .5], [.1, .2]] });
    FIG.fig(R, 720, 880, 550, { tip: 'gilgamis', giysi: 'post', f: 1, kol: [[.2, .3], [.1, .2]] });
    R.L.dir = [-.55, -.55, .6];
  }, { over: (c, st) => quote(c, '“Altı gün yedi gece uyumadan dur.”', 960, 170, st.lt, { t0: rel(st, 'F06@haydi'), px: 62 }) });
  // F07: oturur ve uykuya dalar; sis
  window.UYKU = (R, st, o = {}) => {
    SET.zemin(R); SET.oda(R, { kapi: false });
    FIG.fig(R, 820, 870, 540, { tip: 'gilgamis', giysi: 'post', f: 1, otur: 1, egilme: o.uyku ? .5 : .1, bas: o.uyku ? .6 : 0, kol: [[.8, .6], [.5, .5]], basO: { kapali: !!o.uyku } });
    if (o.ekmek) for (let i = 0; i < o.ekmek; i++) YAR.ekmek(R, 1080 + i * 110, 860, 46, [1, 2, 3, 4, 5, 0, 6][i]);
    if (o.centik) for (let i = 0; i < 7; i++) { const p = clamp(o.centik * 7 - i); if (p > 0) FIG.cizgi(R, [[1150 + i * 40, 250], [1150 + i * 40, 250 + 110 * p]], 9, -.95); }
    R.L.dir = [-.5, -.6, .6];
  };
  sahne('F07a', 'F07', 'uyku', 'orta', (R, st) => {
    K(R, st, [900, 540, 1.1], [880, 560, 1.2]);
    const p = clamp(st.lt / 1.5); UYKU(R, st, { uyku: p > .5 });
    R.L.int = lerp(1, .55, p);
    R.after(c => { c.globalCompositeOperation = 'screen'; c.fillStyle = `rgba(220,210,200,${.25 * p})`; for (let i = 0; i < 5; i++) { c.beginPath(); c.ellipse(500 + i * 300 + Math.sin(st.t * .3 + i) * 60, 600 + Math.sin(i) * 120, 340, 120, 0, 0, TAU); c.fill(); } });
  });
  // F08: karısı her gün bir ekmek pişirir, duvara çizer
  sahne('F08a', 'F08', 'uyku', 'genis', (R, st) => {
    K(R, st, [960, 520, .95], [980, 520, 1.0]);
    const p = clamp((st.lt - rel(st, 'F08@her')) / Math.max(1.5, st.d - rel(st, 'F08@her')));
    UYKU(R, st, { uyku: true, ekmek: Math.floor(p * 7), centik: p });
    FIG.fig(R, 1550, 870, 480, { tip: 'kadin', f: -1, kol: [[1.4, .3], [.2, .2]] });
    FIG.fig(R, 1780, 870, 500, { tip: 'utna', f: -1, kol: [[.5, .5], [.1, .2]] });
  });
  // F09: uyanır
  sahne('F09a', 'F09', 'uyku', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'gilgamis', f: 1, arka: 'oda', kay: 25, fig: { giysi: 'post', bas: lerp(.5, 0, clamp((st.lt - .4) / .6)), basO: { kapali: st.lt < .6 } } });
    R.L.dir = [-.5, -.6, .6];
  });
  // F10: yedi ekmek (ayrıntı; kamera soldan sağa)
  sahne('F10a', 'F10', 'ekmekler', 'ayrinti', (R, st) => {
    K(R, st, [560, 600, 1.6], [1400, 600, 1.6], E.lin);
    SET.zemin(R); DK.tugla(R, -800, 100, 2800, 700, { z: .3, bw: 100, bh: 40 });
    R.b.fillStyle = gv(.42); R.b.fillRect(-800, 700, 3600, 400); FIG.cizgi(R, [[-800, 700], [2800, 700]], 4, -.7);
    for (let i = 0; i < 7; i++) YAR.ekmek(R, 360 + i * 190, 700, 76, [1, 2, 3, 4, 5, 0, 6][i]);
    R.L.dir = [-.6, -.45, .6];
  });
  sahne('F11a', 'F11', 'uyku', 'orta', (R, st) => {
    K(R, st, [960, 540, 1.0], [960, 540, 1.06]);
    UYKU(R, st, { ekmek: 7, centik: 1 });
    R.L.int = .7; R.L.amb = .25;
  });
  // F12: "Yatak odamda ölüm oturuyor": yakın yüz, oda kararır
  sahne('F12a', 'F12', 'uyku', 'yakin', (R, st) => {
    SET.yakin(R, st, { tip: 'gilgamis', f: 1, arka: 'oda', kay: -30, fig: { giysi: 'post', bas: .2 } });
    R.L.dir = [-.5, -.6, .6]; R.L.int = lerp(.75, .3, clamp(st.lt / st.d)); R.L.amb = .18;
  });
})();
