// İskelet denemesi: göl sahnesi + bölüm kartı + alıntı (yalnız sınama; gerçek perdeler lib/acts/sNN.js)
'use strict';
plan('P004', (ctx, st) => levha(ctx, camLerp({ cx: 900, cy: 600, z: 1.5 }, { cx: 960, cy: 540, z: 1 }, st.lt / 6), () => cizGol(st.t)),
  { tr: { type: 'black', dur: 1.2 }, over: (ctx, st) => etiket(ctx, 'görünür karanlık', 960, 880, st.lt - 7, 4) });
plan('P005', (ctx, st) => levha(ctx, null, () => cizGol(st.t)), { tr: { type: 'fade', dur: 1 },
  over: (ctx, st) => quote(ctx, '“Cehennemde hükümdar olmak, cennette hizmetkâr olmaktan yeğdir.”', 960, 300, st.lt, { t0: .6, kaynak: 'KAYIP CENNET · I. 263' }) });
plan('P007', (ctx, st) => levha(ctx, { cx: 960, cy: 560, z: 1.1 }, () => cizGol(st.t, {})), { tr: { type: 'black', dur: 1.4, end: true },
  over: (ctx, st) => chapterCard(ctx, 'KÖR ŞAİR', 'Hiçbir şey göremeyen bir adam, cehennemi nasıl bu kadar iyi gördü?', st.lt - 1.4, 4.2) });
