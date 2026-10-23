// YouTube kapak görseli: film.html?scene=kapak (tools ile 1280×720'ye küçültülür)
'use strict';
SCENES.kapak = (ctx, t) => {
  const xr = 330, po = { dist: xr, smile: 1.5, strain: .4, look: -.3, reach: 19, T: 1.12 };
  const P = pushScene(ctx, null, xr, 150, 4.0, 5, { ...po, dry: true });
  const z = 1.6, c = { x: P.head[0] - (1240 - W / 2) / z, y: P.head[1] - (490 - H / 2) / z, z };
  // güneş diski kayanın arkasında (paralaks k=.15 katmanında ekran konumundan geri hesaplanır)
  const zk = 1 + (z - 1) * .15, cxk = W / 2 + (c.x - W / 2) * .15, cyk = H / 2 + (c.y - H / 2) * .15;
  tartarosBG(ctx, 5, c, { warm: 1, diskX: cxk + (1590 - W / 2) / zk, diskY: cyk + (380 - H / 2) / zk, diskR: 300 });
  tartarosHill(ctx, c, { groove: .9, warm: 1 });
  pushScene(ctx, c, xr, 150, 4.0, 5, po);
  motes(ctx, 5, 40, 33, 'rgba(255,225,160,.8)', [0, 0, W, H], 12, 2.2, .7);
  // sol: başlık bloğu (koyu zemin üzerinde)
  const g = ctx.createLinearGradient(0, 0, W * .62, 0);
  g.addColorStop(0, 'rgba(14,6,4,.86)'); g.addColorStop(.75, 'rgba(14,6,4,.55)'); g.addColorStop(1, 'rgba(14,6,4,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W * .62, H);
  txt(ctx, 'SİSİFOS', 90, 430, { font: '900 196px Cinzel', col: '#F6E3BE', align: 'left', ls: 10, shadow: 'rgba(0,0,0,.6)', blur: 24 });
  ctx.fillStyle = C.gold; ctx.fillRect(98, 548, 560, 6);
  txt(ctx, 'Ölümü zincirleyen adam', 96, 630, { font: 'italic 600 84px "Cormorant Garamond"', col: '#F2C878', align: 'left', shadow: 'rgba(0,0,0,.6)', blur: 16 });
  txt(ctx, 'neden mutlu?', 96, 740, { font: 'italic 600 84px "Cormorant Garamond"', col: '#F6E3BE', align: 'left', shadow: 'rgba(0,0,0,.6)', blur: 16 });
  meander(ctx, 0, W, 18, 44, '#E7B85E');
  applyVignette(ctx, .6);
};
