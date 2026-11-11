// Animatik yer tutucusu: henüz çizilmemiş her plan için kâğıt üstünde plan kartı gösterir (kimlik, set, kadraj, hareket, ekran yazısı).
// Bütün perdelerden SONRA yüklenir; bir plan gerçek çekimle kaydedildiyse (plan('Pxxx', ...)) kartı eklenmez.
// Böylece film her aşamada baştan sona oynatılabilir: çizilen yerler gerçek, kalanı animatik.
'use strict';
(() => {
  const done = new Set(SHOTS.map(s => s.id).filter(Boolean));
  const INK = `rgb(${GR.INK})`;
  for (const id of Object.keys(window.PLAN || {})) {
    if (done.has(id)) continue;
    const p = PLAN[id], koyu = ['GOL', 'KIY', 'MEC', 'KAP', 'KAO', 'SAV'].includes(p.set);
    plan(id, (ctx, st) => levha(ctx, null, () => { }, [koyu ? .04 : .97, 0, 1]), {
      tr: { type: 'cut' },
      over: (ctx, st) => {
        const col = koyu ? PAPER_CSS : INK;
        txt(ctx, `${id} · ${p.at} · ${p.set}${p.lum != null ? ' · ışık ' + p.lum : ''}`, 120, 110, { px: 34, align: 'left', col, font: FONT.baslik(34, 600), ls: 3 });
        ctx.save(); ctx.font = FONT.metin(50); ctx.fillStyle = col; ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
        let y = 230; for (const l of wrapLines(ctx, p.kadraj || '', 1640)) { ctx.fillText(l, 120, y); y += 62; }
        ctx.font = FONT.alinti(40); ctx.globalAlpha = .8; y += 20; for (const l of wrapLines(ctx, p.hareket ? 'hareket: ' + p.hareket : '', 1640)) { ctx.fillText(l, 120, y); y += 50; }
        ctx.restore();
        if (p.yazi) quote(ctx, p.yazi, 960, 760, st.lt, { px: 56, col, panel: false, t0: .2 });
      } });
  }
})();
