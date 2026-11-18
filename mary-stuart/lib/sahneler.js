// Sahneler (Mary Stuart): şimdilik üslup denemesi; plan listesi seslendirme kurulunca yazılır.
'use strict';
window.GORSEL = { clouet: 'kaynak/gorsel/mary_clouet_beyazyas_resim.jpg', depasse: 'kaynak/gorsel/elizabeth_depasse_1592.jpg', profil: 'kaynak/gorsel/mary_peceli_profil.jpg' };
// 0–5: kırmızı açılış (siyah elbise, altından kırmızı)
plan('T1', 0, (G, st) => {
  G.zemin(.16);
  const lg = G.g.createRadialGradient(720, 300, 50, 720, 400, 700); lg.addColorStop(0, G.gri(.62)); lg.addColorStop(1, G.gri(.12)); G.g.fillStyle = lg; G.g.fillRect(0, 0, 1440, 1080);
  G.dik(0, 860, 1440, 300, .3);
  const ac = ss((st.lt - .8) / 2.5);
  G.figur({ x: 760, y: 900, s: 780, f: -1, kind: 'mary', kol: 'onde', t: st.t, v: .1, veil: .9, veilV: .78, kirmizi: 'etek', kirmiziA: ac });
  return { look: { sepia: .16, strength: .3 } };
});
// 5–10: Solway
plan('T2', 5, (G, st) => {
  G.gok(600, { ust: .55, alt: .92, isik: [300, 520, 420, 1] });
  G.bulut(760, 220, 1300, 170, { seed: 4, govde: .5, drift: st.t * 4 });
  G.kiyi(780, 1600, 600, 110, { seed: 7, v: .3 });
  G.deniz(600, 1080, { t: st.t, ufuk: .8, on: .32, yansima: [300, 200, .97] });
  G.tekne({ x: 600 + st.lt * 30, y: 790, s: 360, f: 1, t: st.t, kisi: [{ kind: 'erkek', x: .3, h: .3, poz: 'otur', kol: 'kurek', f: -1 }, { kind: 'mary', x: -.33, h: .5, pelerin: true, kirmizi: 'astar', f: -1 }] });
  return { look: { sepia: .1, strength: .4 } };
});
// 10–15: gerçek portre (Clouet), yavaş yaklaşma
plan('T3', 10, (G, st) => {
  const im = IMG.clouet; if (!im) return {};
  const z = 1 + .06 * eio(st.lt / 5); G.kamera(720, 500, z);
  G.zemin(.1); G.foto(im, 220, -60, 1000, 1000 * im.naturalHeight / im.naturalWidth, { kontrast: 1.15 });
  return { look: { sepia: .22, strength: .3 } };
});
// 15–20: ara yazı (Mary'nin kendi sözü)
plan('T4', 15, (G, st) => ({ kart: { lines: [{ text: '“Kaçmış tutsak, Mary.”', font: 'Cormorant Garamond', italic: true, weight: 600, size: 96 }, { text: 'Workington, 17 Mayıs 1568', font: 'Cinzel', size: 34, spacing: 4 }], level: 1 }, look: { sepia: .2 } }));
// 20–25: Lochleven penceresi
plan('T5', 20, (G, st) => {
  G.pencere({ x: 900, y: 160, w: 460, h: 640, d: 120, dis: () => { G.gok(640, { ust: .85, alt: .98 }); G.kiyi(600, 1300, 600, 90, { v: .5, seed: 3 }); G.deniz(600, 900, { t: st.t, ufuk: .9, on: .65, n: 40 }); } });
  G.dik(-100, 980, 1700, 300, .08);
  G.figur({ x: 600, y: 1010, s: 800, f: 1, kind: 'mary', kol: 'yan', t: st.t, v: .1, veil: .75, head: -.05 });
  return { look: { sepia: .14, strength: .35 } };
});
// 25–30: mektup + kırmızı mühür
plan('T6', 25, (G, st) => {
  G.zemin(.12); G.mum(1200, 980, 330, st.t, { r: 900 });
  G.mektup(620, 520, 860, 1000, -.04, { px: 40, lh: 56, yazi: ['Monsieur mon beau frere, estant par la permission', 'de Dieu, pour mes pechez comme je croy, venue', 'me jetter entre les bras de ceste Royne ma cousine,', 'ou j\'ay eu beaucoup d\'ennuis et passe pres de vingt', 'ans, je suis enfin par elle et ses Estats', 'condamnee a la mort…'], prog: clamp(st.lt / 3) });
  G.muhur(930, 930, 58, { acil: ss((st.lt - 2) / 1.5) });
  return { look: { sepia: .24, strength: .3 } };
});
