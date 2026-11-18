// Kapak taslağı (1920×1080'de çizilir, 1280×720'ye küçültülür). Kompozisyon "ortadan başlamak": yüz ve yansıması solda,
// tek odak yansımadaki göz (karenin en parlak noktası), alttaki yüz halkayla hafif bozulmuş. Yazı Bebas Neue "O BENİM".
// Süre rozeti bölgesi (1920 ölçeğinde x 1440–1875, y 830–1035) boş.
'use strict';
function renderKapak(ctx, v) {
  ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, CW, CH);
  baseView(ctx);
  glaze(ctx, 460, 820, 1150, 'rgba(190,82,36,.85)');
  // sağda yazının arkası: sıcak taban (koyu akışta kapak sönmesin; ortalama parlaklık ~50), başın arkasında ışık yok
  glow(ctx, 1420, 330, 1150, 'rgba(190,84,36,.85)');
  glow(ctx, 1300, 800, 900, 'rgba(120,48,22,.5)');
  const t = 13.25, wy = 560;
  ctx.save();
  camAt(ctx, D_XE + 330, D_WY, 1.04, 610, wy);
  const tHit = 12.55; // halka ~0,7 sn yaşında: alttaki yüz hafif bozulmuş
  const r = dScene(ctx, t, { lag: 0, refA: .92, axis: 0, noTear: true,
    rings: [{ x: 0, y: 0, t0: tHit, A: 24, sq: .62, v: 430, lam: 78, k: .9, reach: 1600, life: 4 }], ringFix: true, noBank: true, handOff: true, ringStyle: { a: .6 } });
  const T = ctx.getTransform();
  ctx.restore();
  // yansımadaki göz: tek odak (karenin en parlak noktası)
  const P = q => { const d = T.transformPoint(new DOMPoint(q[0], q[1])); return [d.x / RS, d.y / RS]; };
  const re = P([r.reye[0] + 6, r.reye[1] - 2]);
  ctx.save(); baseView(ctx);
  ctx.globalCompositeOperation = 'lighter';
  // suyun yüzeyine düşen sıcak ışık (su ölü siyah kalmasın; ortalama parlaklık ~50); yazı suya yansımaz (yansıma yalnız figürden)
  glow(ctx, 1150, 640, 1250, 'rgba(110,44,18,.55)');
  glow(ctx, re[0], re[1], 170, 'rgba(255,200,140,.38)');
  glow(ctx, re[0], re[1], 44, 'rgba(255,244,220,.8)');
  ctx.globalCompositeOperation = 'source-over';
  ctx.fillStyle = '#FFFFFF'; ctx.beginPath(); ctx.arc(re[0] + 3, re[1] - 1, 7, 0, TAU); ctx.fill();
  ctx.restore();
  if (v !== 'yazisiz') {
    ctx.save(); baseView(ctx);
    ctx.font = '400 318px "Bebas Neue"'; ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic';
    const x = 1080, y = 470;
    ctx.lineJoin = 'round'; ctx.strokeStyle = 'rgba(14,9,7,.92)'; ctx.lineWidth = 22; ctx.strokeText('O BENİM', x, y);
    ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 24; ctx.fillStyle = '#CDB48A'; ctx.fillText('O BENİM', x, y);
    ctx.restore();
  }
  // kenar: ince kil çizgi (koyu akışta kapağın kenarı kaybolmasın); süre rozeti bölgesinin altından geçer, rozetin içine bir şey konmaz
  ctx.save(); baseView(ctx); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 7; ctx.strokeRect(16, 16, 1888, 1048);
  ctx.strokeStyle = 'rgba(14,9,7,.9)'; ctx.lineWidth = 3; ctx.strokeRect(27, 27, 1866, 1026); ctx.restore();
  post(ctx, 0);
}
