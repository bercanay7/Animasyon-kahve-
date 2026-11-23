// E: Dünyanın ucu (E01–E11). Sahibi: başkan.
'use strict';
(() => {
  const K = SET.kam, rel = (st, at) => A(at) - st.at, yur = (t, k = 4) => ({ bacak: [[Math.sin(t * k) * .32, -.1], [-Math.sin(t * k) * .32, .05]] });
  // E01: dünyanın ucu: friz boyunca uzak deniz, ufukta tek yaşlı adam
  sahne('E01a', 'E01', 'ucu', 'genis', (R, st) => {
    K(R, st, [700, 540, .8], [1250, 540, .8]);
    SET.zemin(R); DK.friz(R, -800, 3000, 140, 940);
    SET.tepeler(R, -800, 1500, 820, { h: 200, z: .28 });
    SET.yer(R, -800, 1700, 820, { z: .34 });
    SET.su(R, 1700, 3000, 760, { faz: st.lt * .8 });
    FIG.fig(R, 2500, 760, 200, { tip: 'utna', f: -1, z: .64 });
    FIG.fig(R, 200 + st.lt * 60, 830, 250, { tip: 'gilgamis', giysi: 'post', f: 1, ...yur(st.lt) });
    R.L.dir = [-.6, -.5, .6];
  }, { over: (c, st) => etiket(c, 'UTNAPİŞTİM', 1500, 210, st.lt - rel(st, 'E01@utnapiştim'), 4) });
  // E02: Maşu dağı, kapıda akrep insanlar uyarır
  sahne('E02a', 'E02', 'masu', 'orta', (R, st) => {
    K(R, st, [900, 620, 1.12], [920, 640, 1.18]);
    SET.zemin(R); SET.masu(R, 960, 880, {});
    SET.yer(R, -900, 2900, 880, { z: .36 });
    const ku = rel(st, 'E02@uyardı'), k = clamp((st.lt - ku) / .6);
    YAR.akrep(R, 760, 885, 330, { f: 1, kol: [[lerp(.3, 1.3, k), lerp(.3, 1.0, k)], [.3, .3]] });
    YAR.akrep(R, 1160, 885, 330, { f: -1, kol: [[lerp(.3, 1.3, k), lerp(.3, 1.0, k)], [.3, .3]] });
    FIG.fig(R, 300 + Math.min(st.lt, 2.5) * 80, 885, 280, { tip: 'gilgamis', giysi: 'post', f: 1, ...yur(Math.min(st.lt, 2.5)) });
    R.L.dir = [.75, -.4, .45]; R.L.col = [1.1, .76, .55]; R.L.int = .85;
  }, { tr: { type: 'muhur', dur: .8 } });
  // E03: güneşin geceleri geçtiği yol: zifiri karanlık; yalnız kenarlar seçilir
  sahne('E03a', 'E03', 'karanlik', 'genis', (R, st) => {
    K(R, st, [960 + st.lt * 30, 540, 1.0], [960 + st.lt * 30, 540, 1.0]);
    SET.zemin(R);
    for (let i = -2; i < 12; i++) DK.tugla(R, i * 400, 140, i * 400 + 380, 260, { z: .3, bw: 80, bh: 30 });
    SET.yer(R, -900, 4900, 860, { z: .3, cimen: false });
    FIG.fig(R, 900 + st.lt * 60, 865, 420, { tip: 'gilgamis', giysi: 'post', f: 1, ...yur(st.lt, 2.6), kol: [[1.3, .2], [.6, .3]] });
    const k = clamp((st.lt - rel(st, 'E03@karanlık')) / 1.2);
    R.L.int = lerp(.5, .05, k); R.L.amb = lerp(.2, .035, k); R.L.dir = [.0, -.3, .9]; R.L.col = [.6, .62, .8];
    R.L.pts.push({ x: 1000, y: 500, z: 500, r: 700, i: .25 * k, col: [.5, .55, .8] });
  }, { tr: { type: 'black', dur: 1.0 }, post: { vig: 1.0 } });
  // E04: karanlığın sonunda mücevher bahçesi; durmadan geçer
  sahne('E04a', 'E04', 'bahce', 'orta', (R, st) => {
    K(R, st, [800, 520, 1.0], [1150, 520, 1.0]);
    SET.zemin(R); SET.yer(R, -900, 2900, 880, { z: .34 });
    for (let i = 0; i < 6; i++) SET.mucevherAgaci(R, 150 + i * 330, 880, 520 + (i % 2) * 80);
    FIG.fig(R, 500 + st.lt * 110, 885, 400, { tip: 'gilgamis', giysi: 'post', f: 1, ...yur(st.lt, 4.5), bas: .05 });
    const k = clamp(st.lt / 1.5); R.L.int = lerp(.3, 1.0, k); R.L.amb = lerp(.1, .32, k); R.L.dir = [-.4, -.7, .55];
  }, { tr: { type: 'fade', dur: .6 } });
  // E05: deniz kıyısında meyhane; Siduri kapıyı sürgüler
  sahne('E05a', 'E05', 'meyhane', 'genis', (R, st) => {
    const ts = rel(st, 'E05@sürgüledi');
    K(R, st, [960, 520, .9], [980, 540, .96]);
    SET.zemin(R); SET.su(R, -900, 2900, 620, { faz: st.lt * .7, alt: 160 }); R.b.fillStyle = gv(.34); R.b.fillRect(-900, 770, 3800, 600);
    SET.yer(R, -900, 2900, 860, { z: .36 });
    SET.ev(R, 700, 860, 640, 430, { kapi: .3 });
    const kp = clamp((st.lt - ts) / .6); R.b.fillStyle = gv(.6); R.b.fillRect(892 + (1 - kp) * 80, 624, 80 * kp + 4, 236);
    DK.hurma(R, 1450, 880, 360, {});
    FIG.fig(R, 830, 865, 300, { tip: 'siduri', f: 1, z: .7, kol: [[1.5, .1], [.2, .2]] });
    FIG.fig(R, 1700 - Math.min(st.lt, 2.5) * 70, 865, 330, { tip: 'gilgamis', giysi: 'post', f: -1, ...yur(Math.min(st.lt, 2.5)) });
    R.L.dir = [-.6, -.5, .6];
  }, { over: (c, st) => etiket(c, 'SİDURİ', 830, 200, st.lt - .8, 4) });
  // E06: Siduri konuşur (yakın; alıntı ekranda)
  sahne('E06a', 'E06', 'meyhane', 'orta', (R, st) => {
    K(R, st, [880, 520, 1.25], [900, 520, 1.3]);
    SET.zemin(R); SET.ev(R, 300, 860, 900, 640, { kapi: .55 });
    SET.yer(R, -900, 2900, 860, { z: .36 });
    FIG.fig(R, 700, 875, 560, { tip: 'siduri', f: 1, kol: [[.9 + Math.sin(st.lt * 1.3) * .15, .7], [.2, .2]] });
    FIG.fig(R, 1260, 875, 580, { tip: 'gilgamis', giysi: 'post', f: -1, kol: [[.2, .3], [.1, .2]], bas: .1 });
    R.L.dir = [-.55, -.55, .6];
  }, { over: (c, st) => quote(c, '“Aradığın hayatı bulamayacaksın.”', 960, 170, st.lt, { t0: rel(st, 'E06@aradığın'), px: 64 }) });
  // E07: öğüdün görüntüsü: sofra, temiz giysi, elini tutan çocuk
  sahne('E07a', 'E07', 'aile', 'genis', (R, st) => {
    K(R, st, [960, 540, .88], [960, 540, .93]);
    SET.zemin(R); DK.friz(R, -600, 2600, 130, 940);
    SET.yer(R, -900, 2900, 890, { z: .36, cimen: false });
    const tk = rel(st, 'E07@karnını'), tc = rel(st, 'E07@çocuğa');
    YAR.ekmek(R, 520, 860, 60, 0); YAR.testi(R, 660, 890, 140);
    FIG.fig(R, 380, 895, 420, { tip: 'adam', f: 1, otur: 1, kol: [[1.3, .3], [.3, .3]] });
    FIG.fig(R, 1180, 895, 460, { tip: 'adam', f: 1, kol: [[.15, .1], [0, .2]], ...yur(st.lt > tc ? st.lt * .7 : 0, 3) });
    FIG.fig(R, 1350, 895, 300, { tip: 'cocuk', f: -1, kol: [[.55, .1], [0, .2]], z: .74 });
    FIG.fig(R, 1560, 895, 440, { tip: 'kadin', f: -1, kol: [[.4, .4], [0, .2]] });
    R.L.dir = [-.55, -.55, .6]; R.L.col = [1.05, .97, .85];
  }, { over: (c, st) => kunye(c, 'Eski Babil sürümü · Sippar tableti, ~MÖ 1700', st.lt, 99) });
  // E08: dinlemedi, yolu sordu
  sahne('E08a', 'E08', 'meyhane', 'yakin', (R, st) => {
    K(R, st, [1240, 420, 1.7], [1250, 420, 1.78]);
    SET.zemin(R); SET.ev(R, 300, 860, 900, 640, { kapi: .55 });
    SET.yer(R, -900, 2900, 860, { z: .36 });
    FIG.fig(R, 700, 875, 560, { tip: 'siduri', f: 1, kol: [[.3, .3], [.1, .2]] });
    const p = clamp(st.lt / 1.5);
    FIG.fig(R, 1260, 875, 580, { tip: 'gilgamis', giysi: 'post', f: p > .5 ? 1 : -1, kol: [[p > .5 ? 1.25 : .2, .35], [.1, .2]] });
    SET.su(R, 1500, 2900, 560, { faz: st.lt, alt: 120 });
    R.L.dir = [-.55, -.55, .6];
  });
  // E09: kayıkçı Urşanabi
  sahne('E09a', 'E09', 'kiyi', 'genis', (R, st) => {
    K(R, st, [1050, 540, .95], [1100, 540, 1.0]);
    SET.zemin(R); SET.yer(R, -900, 900, 860, { z: .36 });
    SET.su(R, 800, 2900, 820, { faz: st.lt * .8 });
    DK.kayik(R, 1450, 840 + Math.sin(st.lt * 1.5) * 6, 640, {});
    FIG.fig(R, 1450, 790 + Math.sin(st.lt * 1.5) * 6, 360, { tip: 'ursa', f: -1, kol: [[2.7, .2], [2.5, .3]], el: { yakin: (R, e, S) => FIG.uzuv(R, [e[0] + S * .25, e[1] + S * .65], [e[0] - S * .1, e[1] - S * .55], S * .03, S * .025, .88) } });
    FIG.fig(R, 520, 870, 360, { tip: 'gilgamis', giysi: 'post', f: 1, kol: [[.9, .5], [.1, .2]] });
    R.L.dir = [-.55, -.55, .6];
  }, { over: (c, st) => etiket(c, 'KAYIKÇI URŞANABİ', 1450, 200, st.lt - .8, 4.5) });
  // E10: ölüm suları: sırıklar birer birer bırakılır
  sahne('E10a', 'E10', 'olumsuyu', 'orta', (R, st) => {
    K(R, st, [900 + st.lt * 40, 540, 1.05], [900 + st.lt * 40, 540, 1.05]);
    SET.zemin(R); R.b.fillStyle = gv(.12); R.b.fillRect(-900, 700, 4800, 600); R.m.fillStyle = '#273E6B'; R.m.fillRect(-900, 700, 4800, 600);
    SET.su(R, -900, 3900, 720, { faz: st.lt * .5, renk: '#2B4476', z: .2 });
    const x = 900 + st.lt * 90;
    DK.kayik(R, x, 760, 620, {});
    const ph = (st.lt * .8) % 1;
    FIG.fig(R, x + 120, 715, 340, { tip: 'gilgamis', f: 1, egilme: .3, kol: [[2.4 - ph * 1.2, .2], [2.2 - ph, .3]], el: { yakin: (R, e, S) => FIG.uzuv(R, [e[0] + S * .4, e[1] + S * .9], [e[0] - S * .2, e[1] - S * .6], S * .03, S * .025, .9) } });
    FIG.fig(R, x - 150, 715, 330, { tip: 'ursa', f: 1 });
    for (let i = 0; i < Math.floor(st.lt * .8); i++) { const px = x - 300 - i * 140; FIG.uzuv(R, [px, 760], [px - 80, 690], 14, 12, .5); }
    R.L.dir = [-.4, -.6, .6]; R.L.int = .7; R.L.amb = .24; R.L.col = [.85, .9, 1.05];
  }, { tr: { type: 'muhur', dur: .8 } });
  // E11: giysi yelken olur
  sahne('E11a', 'E11', 'olumsuyu', 'genis', (R, st) => {
    K(R, st, [960, 540, .9], [1000, 540, .92]);
    SET.zemin(R); R.b.fillStyle = gv(.12); R.b.fillRect(-900, 700, 4800, 600); R.m.fillStyle = '#273E6B'; R.m.fillRect(-900, 700, 4800, 600);
    SET.su(R, -900, 3900, 720, { faz: st.lt * .5, renk: '#2B4476', z: .2 });
    const x = 900 + st.lt * 60, p = E.out3(clamp(st.lt / 1.8));
    DK.kayik(R, x, 760, 620, {});
    FIG.uzuv(R, [x, 740], [x, 260], 18, 14, .62);
    FIG.uzuv(R, [x - 150 * p, 300], [x + 150 * p, 300], 14, 14, .7); FIG.sekil(R, [[x - 140 * p, 306], [x + 140 * p, 306], [x + 165 * p, 600], [x - 165 * p, 600]], .64, .5); for (let k = -2; k <= 2; k++) FIG.cizgi(R, [[x + k * 50 * p, 310], [x + k * 58 * p, 595]], 3, -.4);
    FIG.fig(R, x - 120, 715, 320, { tip: 'gilgamis', f: 1, giysi: 'pecek', kol: [[2.8, .2], [.3, .2]] });
    FIG.fig(R, x - 260, 715, 310, { tip: 'ursa', f: 1 });
    R.L.dir = [-.4, -.6, .6]; R.L.int = .75; R.L.amb = .25; R.L.col = [.88, .92, 1.05];
  });
})();
