// üslup denemesi (silinecek)
sahne('P001', 'A01', 'koridor', 'genis', (B, st) => {
  const t = st.lt;
  B.cam(960 + t * 4, 540, 1 + t * .01);
  const K = D.koridor(B, t, { no: (y, i) => y < 0 ? '1' : '2' });
  const p = K.yer(.35, -.2), s = K.olc(.35);
  FIG.kisi(B.l, p[0], p[1], 520 * s, { tip: 'gardiyan', f: 1, kolO: [.3, .6] });
  const q = K.yer(.5, .25), s2 = K.olc(.5);
  FIG.kisi(B.l, q[0], q[1], 500 * s2, { tip: 'mahkum', f: -1, numara: '8612' });
}, { baski: { mod: 'video' } });
sahne('P002', 'A01+6', 'gozlem', 'orta', (B, st) => {
  const t = st.lt;
  B.cam(960, 540, 1.02 + t * .01);
  const k = B.k; k.fillStyle = B.ton(.5); k.fillRect(-200, 700, W + 400, 600); k.fillStyle = B.ton(.25); k.fillRect(-200, -200, W + 400, 900);
  D.teyp(B, 1350, 360, .9, t * 2, { kayit: 1, vu: .4 + .3 * Math.sin(t * 7) });
  D.monitor(B, 220, 180, 760, 520);
  FIG.kisi(B.l, 1000, 1100, 700, { tip: 'mudur', f: 1, bacak: 'otur', kolO: [.9, .8] });
}, { baski: { mod: 'kagit' } });
sahne('P003', 'A01+12', 'belge', 'yakin', (B, st) => {
  B.cam(960, 540, 1 + st.lt * .01);
  D.belge(B, 360, 140, 1200, ['JAFFE: ...every guard is going to be', 'what we call a "tough guard."', '', 'GUARD: I\'m not too much of a', 'tough guy.'], st.lt / 5, { vurgu: [1] });
}, { baski: { mod: 'kagit' } });
