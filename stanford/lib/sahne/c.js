// III. Bant (D01–D19). Deneme: gözlem odası (silinecek bölüm altta)
'use strict';
sahne('P40', 'D02', 'gozlemOdasi', 'genis', (B, st) => {
  B.cam(960, 500, 1.02 + Math.min(st.lt, 12) * .01);
  SET.gozlemOdasi(B, st, {});
}, { baski: { mod: 'kagit', kuru: .6 } });
