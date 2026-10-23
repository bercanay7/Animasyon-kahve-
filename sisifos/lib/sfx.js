// Ses efekti işaretleri: görüntüdeki olaylarla aynı zaman ifadeleri (tools/export_sfx.js → audio/sfx_events.json → tools/mix.py)
'use strict';
const SFX = [];
// sfx(zaman, ad, {g: dB, at: 'start'|'peak', off, len, fi, fo, pan, rate})
function sfx(t, name, o = {}) { SFX.push({ t: +t.toFixed(3), name, ...o }); }
// ortam döngüsü: t0–t1 arası, uçlarda yumuşak geçiş
function amb(t0, t1, name, g, fi = 1, fo = 1, o = {}) { SFX.push({ t: +t0.toFixed(3), name, loop: true, len: +(t1 - t0).toFixed(3), g, fi, fo, ...o }); }
const chapter = (shotAt, lt0) => sfx(shotAt + lt0 + .1, 'chime', { g: -14, note: 'chapter' });

(() => {
  // — AÇILIŞ —
  const tz = Wd('A01', 'zincire'), snap = tz + .32;
  amb(0, S('A02') - .12, 'wind', -26, .4, .4);
  sfx(tz - .3, 'whoosh', { g: -12, len: .6 });
  sfx(snap, 'chains', { at: 'peak', g: -2 });
  sfx(Wd('A02', 'bir') - .15, 'knock', { g: -12 });
  sfx(Wd('A02', 'iki') - .15, 'knock', { g: -12, rate: 1.12 });
  const tA3 = S('A03') - .35, tg = Wd('A04', 'geri') - .05, tw = Wd('A04', 'aşağı') - .1, ty = Wd('A04', 'yeniden') - .15;
  amb(tA3, S('A05') - .6, 'wind', -18, .9, .6);
  amb(tA3, tg + .1, 'stone_scrape', -16, .6, .15);
  sfx(tg - .45, 'scrape', { g: -9 });
  const RA = (window.ROCK_OVER || {}).A4;
  sfx(RA.tg + .04, 'thud', { g: -14, rate: 1.3 });                   // yere kapanış (gövdenin yere değdiği an)
  sfx(RA.tl - .25, 'whoosh', { g: -21, len: .6 });                   // kaya üstünden aşar ("yuvarlanır" altında kısık)
  sfx(RA.td, 'thud', { g: -16 });                                    // iniş
  RA.bounces.slice(1).forEach((b, k) => { sfx(b, 'thud', { g: -19 - k * 3 }); sfx(b, 'scrape', { g: -14 - k * 3, len: .25, fo: .15 }); });
  sfx(RA.td, 'scrape', { g: -12, len: .3, fo: .2 });                   // iniş: orta frekans çakıl katmanı (küçük hoparlörde duyulsun)
  sfx(RA.td, 'rock_roll', { g: -12, len: tw - RA.td + .4, fi: .5, fo: .5 });
  amb(tw, ty, 'footsteps', -12, .2, .3);
  amb(ty, S('A05') - .6, 'stone_scrape', -18, .4, .4);
  const tt = Wd('A05', 'sisifos');
  sfx(S('A05') - .6, 'whoosh', { g: -16, len: .9, rev: true });
  sfx(tt + 1.5, 'chime', { g: -16 });
  sfx(S('A06') - .25, 'thunder', { g: -20, off: .1, fi: .6 });
  const tb = Wd('A06', 'binlerce') - .2;
  sfx(tb, 'whoosh', { g: -14, len: .7 });
  sfx(tb + .6, 'pen', { g: -14, len: 2.0 });

  // — I. KORİNT —
  const tB1 = S('B01') - .45;
  amb(tB1, S('B03') - .3, 'sea', -17, 1.2, .5);
  amb(tB1, S('B03') - .3, 'wind', -30, 1.2, .5);
  chapter(tB1, 0);
  sfx(Wd('B03', 'zeka') + .3, 'chime', { g: -15, rate: 1.5 });
  const tB4 = S('B04') - .3, tr = Wd('B04', 'rengini');
  amb(tB4, S('B05') - .3, 'wind', -28, .8, .6);
  amb(tB4, tB4 + 3.4, 'footsteps', -22, .5, .5, { rate: .85 });
  sfx(tr, 'shimmer', { g: -16 });
  const tB5 = S('B05') - .3, tw5 = Wd('B05', 'sığırlar', 1) - .1;
  // keski vuruşları: |sin(5·lt)|³ tepe noktaları
  for (let k = 0; ; k++) { const lt = (Math.PI / 2 + k * Math.PI) / 5; if (lt < 1.0) continue; if (tB5 + lt > tw5 - .1) break; sfx(tB5 + lt, 'tick', { g: -14 + (k % 2) * 2, rate: 1 + (k % 3) * .06 }); }
  // toynak izleri (inek adımı ~ her 0.35 sn)
  for (let u = .2; tw5 + u < S('B06') - .4; u += .38) sfx(tw5 + u, 'hoof', { g: -14 });
  const tB6 = S('B06') - .3, tn = Wd('B06', 'ne');
  sfx(tB6 + 1.0, 'sting', { g: -14 });
  sfx(tn + 2.0, 'thunder', { at: 'peak', g: -8 });
  amb(tn + .4, S('C01') - .35, 'wind', -22, 1.4, .8);

  // — II. KARTAL VE PINAR —
  const tC1 = S('C01') - .35;
  chapter(tC1, 0);
  amb(tC1, S('C03') - .2, 'wind', -22, 1, .1);
  sfx(S('C02') - .1, 'eagle', { g: -11 });
  sfx(S('C02') + 1.6, 'wings', { g: -8 });
  sfx(S('C02') + 2.8, 'eagle', { g: -16, rate: .94, off: .1 });
  sfx(Wd('C03', 'zeus', 0, true) + .15, 'thunder', { at: 'peak', g: -10 });
  const tC4 = S('C04') - .25;
  amb(tC4, S('C05') - .2, 'sea', -20, .6, .5);
  amb(tC4, S('C05') - .2, 'water', -26, .6, .5);
  const tf = Wd('C06', 'fışkırttı') - .25;
  sfx(tf - 1.0, 'whoosh', { g: -18, len: .5 });
  sfx(tf, 'knock', { g: -12, rate: .7 });
  sfx(tf, 'thud', { g: -13 });
  sfx(tf, 'rock_crash', { g: -22 });
  sfx(tf + .05, 'water', { at: 'peak', g: -14 });
  sfx(Wd('C06', 'fışkırttı', 0, true) + .05, 'water', { g: -10, fi: .25, len: 1.6, fo: .8 });
  amb(tf + 1, S('C08') - .25, 'water', -22, 1, .3);
  sfx(Wd('C07', 'ama') + .6, 'thunder', { g: -20, off: .4, fi: .8 });
  const tz8 = Wd('C08', 'unutmazdı', 0, true) + .1;
  amb(S('C08') - .25, S('D01') - .25, 'wind', -20, .2, .8);
  sfx(tz8, 'thunder', { at: 'peak', g: -1 });
  sfx(tz8 + .4, 'thunder', { at: 'peak', g: -9, rate: .9 });

  // — III. ÖLÜMÜ ZİNCİRLEYEN ADAM —
  const tD1 = S('D01') - .25, tt1 = Wd('D01', 'tanatos');
  chapter(tD1, 0);
  amb(tD1, S('D02') - .2, 'wind', -24, 1, .3);
  sfx(tt1 - 2.2, 'riser', { g: -14, len: 2.4 });
  sfx(tt1 - .1, 'wings', { g: -14 });
  const tD2 = S('D02') - .2;
  amb(tD2, S('D06') - .25, 'torches', -14, .5, .4);
  sfx(tD2 + 1.2, 'door', { at: 'peak', g: -6 });
  sfx(Wd('D02', 'zincirlerle') - .15, 'chains', { g: -12, len: 1.8, fo: .6 });
  sfx(Wd('D03', 'sadece') - .1, 'chains', { g: -17, len: 1.6, fo: .7, rate: 1.1 });
  sfx(Wd('D04', 'gösterir') - .2, 'chains', { g: -16, len: 1.2, fo: .5 });
  const tk = Wd('D05', 'kilidi');
  sfx(S('D05') + .2, 'chains', { g: -14, len: 1.4, fo: .6 });
  sfx(tk + .12, 'lock', { at: 'peak', g: -2 });
  sfx(tk + .14, 'chime', { g: -18, rate: 2 });
  sfx(S('D06') + .1, 'chains', { g: -20, len: 1.2, fo: .6, rate: .9 });
  const tD7 = S('D07') - .2, ts7 = Wd('D07', 'sunaklarda');
  amb(tD7, ts7 - .3, 'battle', -14, .4, .8);
  sfx(S('D07') + 1.3, 'thud', { g: -8 });
  sfx(Wd('D07', 'kalkıyor') - .2, 'sting', { g: -16, rate: 1.2 });
  sfx(Wd('D07', 'kesilemiyordu'), 'knock', { g: -15, rate: 1.7 });   // bıçak boğanın boynundan seker
  const tD8 = S('D08') - .2;
  for (let k = 1; tD8 + k * Math.PI / 4.5 < Wd('D08', 'kimsenin') - .2; k++) sfx(tD8 + k * Math.PI / 4.5, 'thud', { g: -11 });
  amb(tD8, S('D09') - .2, 'battle', -22, .4, .4, { off: 1.5 });
  const tbk = Wd('D09', 'kurtardı') - .2, tgv = Wd('D09', 'teslim');
  sfx(tbk - .45, 'whoosh', { g: -10, len: .5 });
  sfx(tbk, 'chains', { at: 'peak', g: -3 });
  sfx(tbk, 'boom', { g: -8 });
  sfx(tgv - .2, 'wings', { g: -9 });
  sfx(tgv + .1, 'thud', { g: -12 });
  sfx(tgv + 1.0, 'riser', { g: -16, len: S('E01') - .3 - tgv - 1.0 });
  sfx(S('E01') - .3, 'boom', { g: -8 });

  // — IV. İKİNCİ HİLE —
  const tE1 = S('E01') - .3;
  chapter(tE1, 0);
  amb(tE1, S('E03') - .3, 'torches', -12, 1, .5);
  for (const w of ['bedenimi', 'tören', 'adak']) { const ti = Wd('E02', w); sfx(ti + .35, 'knock', { g: -20 }); sfx(ti + .55, 'scratch', { g: -15 }); sfx(ti + .75, 'scratch', { g: -13, rate: 1.1 }); }
  const tE3 = S('E03') - .3;
  amb(tE3, S('E06') - .2, 'wind', -22, .9, .4, { rate: .8 });
  amb(tE3, S('E06') - .2, 'torches', -10, .9, .4);
  sfx(S('E05') + .6, 'shimmer', { g: -11, len: 1.6 });
  const tE6 = S('E06') - .2;
  amb(tE6, S('E07') - .2, 'sea', -16, .7, .6);
  sfx(Wd('E06', 've') + .2, 'clink', { g: -14 });
  const th = Wd('E07', 'hermes');
  amb(S('E07') - .2, th + 1.6, 'sea', -24, .3, 1.2);
  sfx(th - .2, 'wings', { g: -6 });
  sfx(th + .6, 'thud', { g: -12 });
  sfx(th + 1.6, 'whoosh', { g: -12, len: 1.4, down: true });
  sfx(th + 3.0, 'boom', { g: -10 });

  // — V. CEZA —
  const tF1 = S('F01') - .3, tc = Wd('F01', 'ceza');
  chapter(tF1, .2);
  amb(tF1, S('G01') - .35, 'wind', -17, 1.2, 1.5);
  sfx(tc - .9, 'whoosh', { g: -8, len: .9, down: true });
  sfx(tc + .4, 'rock_crash', { at: 'peak', g: -10 });
  sfx(tc + .05, 'boom', { g: -10 });
  sfx(Wd('F03', 'zirveye') + 1.0, 'chime', { g: -16 });
  const tF4 = S('F04') - .2, tk4 = Wd('F04', 'kaydı');
  amb(Wd('F04', 'itti') - .2, S('F05') - .1, 'stone_scrape', -12, .3, .1);
  sfx(tk4, 'scrape', { g: -6 });
  sfx(Wd('F04', 'titredi') - .1, 'riser', { g: -14, len: Wd('F04', 'zirveye') + .4 - Wd('F04', 'titredi') });
  const t0 = S('F05') + .05, tend = Se('F05') + .3;
  const RF = (window.ROCK_OVER || {}).F5;
  sfx(t0 - .05, 'scrape', { g: -8 });
  sfx(RF.tg + .09, 'thud', { g: -14, rate: 1.3 });
  sfx(RF.tl - .3, 'whoosh', { g: -14, len: .7 });
  sfx(RF.td, 'rock_roll', { g: -8, len: tend - RF.td + .2, fi: 1.2, fo: .3 });
  (window.F5_BOUNCES || []).forEach((tb, k, arr) => { sfx(tb, 'thud', { g: -15 + 6 * k / arr.length }); sfx(tb, 'scrape', { g: -13 + 4 * k / arr.length, len: .25, fo: .15 }); });
  sfx(tend, 'rock_crash', { at: 'peak', g: 0 });
  const ty6 = Wd('F06', 'yeniden');
  amb(S('F06') - .2, ty6 - .2, 'footsteps', -12, .3, .3);
  amb(ty6, S('F07') - .2, 'stone_scrape', -18, .4, .2);
  const b1 = Wd('F07', 'ondan') - .15, b2 = Wd('F07', 'yüz') - .15, b3 = Wd('F07', 'bin') - .15;
  amb(S('F07') - .2, b3, 'stone_scrape', -18, .2, .4);
  for (const b of [b1, b2, b3]) sfx(b - .2, 'whoosh', { g: -14, len: .5 });
  sfx(b3, 'riser', { g: -16, len: S('F08') - .2 - b3 });
  sfx(S('F08') - .2, 'boom', { g: -14 });

  // — VI. CAMUS —
  const tG1 = S('G01') - .35, td = Wd('G01', 'dokuz') - .3, ta = Wd('G01', 'albert'), tsg = Wd('G01', 'sisifos'), tbg = Wd('G01', 'bambaşka');
  sfx(tG1, 'riser', { g: -12, len: td - tG1 });
  amb(tG1 + .3, td, 'ticks', -16, .3, .2);
  sfx(td, 'boom', { g: -12 });
  amb(td, tsg + .3, 'planes', -21, .4, 1.2);
  amb(ta - 1.2, ta + .4, 'footsteps', -16, .2, .3, { rate: 1.1 });
  sfx(tsg - .4, 'knock', { g: -14 });
  sfx(tbg - .2, 'page', { g: -10 });
  const tG3 = S('G03') - .3, tq = Wd('G03', 'bir', 1) - .1;
  sfx(tG3 + .2, 'alarm', { g: -16, len: 1.6, fo: .4 });
  amb(tG3 + 1, tq - .3, 'typewriter', -20, .5, .3);
  amb(tG3, tq, 'footsteps', -16, .3, .2, { rate: 1.15 });
  amb(tG3, tq, 'ticks', -22, .5, .2);
  sfx(tq - .3, 'stop', { g: -12 });
  const tG4 = S('G04') - .2, tc4 = Wd('G04', 'çatlağa') - .2;
  amb(tG4, S('G05') - .3, 'wind', -32, 1.2, .6, { rate: .7 });
  sfx(tc4, 'crack', { g: -14 });
  sfx(Wd('G04', 'der', 0, true) + .05, 'shimmer', { g: -16, len: 2.2 });
  const tG5 = S('G05') - .3, tk5 = Wd('G05', 'kaya') - .2, ta5 = Wd('G05', 'ağır');
  amb(tG5, S('G08') - .2, 'wind', -22, 1, .4);
  amb(tG5, tk5, 'stone_scrape', -20, .5, .1);
  const RG = (window.ROCK_OVER || {}).G5;
  sfx(RG.tg + .05, 'thud', { g: -16, rate: 1.3 });
  sfx(RG.tl - .25, 'whoosh', { g: -17, len: .6 });
  sfx(RG.td, 'thud', { g: -10 }); sfx(RG.td, 'scrape', { g: -13, len: .3, fo: .2 });
  RG.bounces.slice(1).forEach((b, k) => sfx(b, 'thud', { g: -21 - k * 3 }));
  sfx(RG.td, 'rock_roll', { g: -7, len: ta5 - RG.td + .6, fi: .4, fo: .5 });
  amb(ta5 - .2, S('G07') - .2, 'footsteps', -15, .4, .5, { rate: .92 });
  sfx(S('G07') + .3, 'shimmer', { g: -16 });
  sfx(S('G08') - .2, 'page', { g: -11 });
  amb(S('G09') - .25, S('G10') - .3, 'stone_scrape', -22, .6, .4);
  amb(S('G09') - .25, S('H01') - .45, 'wind', -26, .8, 1);
  sfx(Se('G10') + .15, 'chime', { g: -16, rate: .75 });

  // — KAPANIŞ —
  const tH1 = S('H01') - .45;
  amb(tH1, DUR, 'room', -30, 1.2, 3);
  sfx(tH1, 'whoosh', { g: -14, len: 1.6, rev: true });
  sfx(S('H03') - .4, 'whoosh', { g: -16, len: 1.2 });
  sfx(S('H04') - .3 + .6, 'chime', { g: -16, rate: .75 });
})();
window.SFX = SFX;
