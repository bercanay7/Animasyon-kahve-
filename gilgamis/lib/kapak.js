// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir). A: "ortadan başlamak" (bitki elde, yılan kapıyor). B: "karşıtlık" (örtülü dost / başını ellerine almış adam, duvarda 7 çentik).
// Kapak sistemi (kanal/KAPAK_SISTEMI.md, 27 Kasım): yazı sol üst, figür sağ; Bebas fildişi, 2 satır, tek kelime vurgu renginde; font ≥ 290 px; tek odak (yazı hariç en parlak yer); sağ alt süre rozeti bölgesi (x>1440, y>829) boş.
// Son kapaklar (27 Kasım). Her biri ayrı süreçte çekilir: sayfanın ilk çizimi sonrakilerden yatak ayağında birkaç yüz pikselde ayrılıyor, yazısız farkla yazı ölçümü bozuluyordu.
//   A: '{"dx":260,"satir":["BİR AN","ELİNDEYDİ"],"vurgu":"ELİNDEYDİ","vcol":"#E2B04F","y":290,"px":300}'  (+ "ad":"A_yazisiz","yazisiz":1)
//   B: '{"satir":["7 GECE","GÖMMEDİ"],"vurgu":"GÖMMEDİ","vcol":"#F2A04A","px":300,"y":300,"son":0.45,"isik":[1150,700,240,600,1.8]}'  (+ "ad":"B_yazisiz","yazisiz":1)
'use strict';
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
// Kapak sistemi (kanal/KAPAK_SISTEMI.md): fildişi #F3EAD7, tek kelime vurgu renginde (o.vurgu: kelime, o.vcol: renk).
function yazi(c, satirlar, x, y, px, o = {}) {
  c.save(); c.font = `400 ${px}px "Bebas Neue"`; c.textAlign = 'left'; c.textBaseline = 'alphabetic'; c.letterSpacing = (o.ls ?? 4) + 'px';
  const bosluk = c.measureText(' ').width;
  satirlar.forEach((s, i) => {
    const yy = y + i * px * (o.ara ?? .9);
    let xx = x;
    for (const k of s.split(' ')) {
      c.fillStyle = 'rgba(20,8,2,.85)'; for (const [dx, dy] of [[0, 10], [6, 8], [-4, 8]]) c.fillText(k, xx + dx, yy + dy);
      c.fillStyle = (o.vurgu && k === o.vurgu) ? (o.vcol || '#E2B04F') : (o.col || '#F3EAD7'); c.fillText(k, xx, yy);
      xx += c.measureText(k).width + bosluk;
    }
  });
  c.restore();
}
const KAPAK = {
  A(o) {
    const R = KIL; R.begin({ zemin: .2 }); R.cam(960, 540, 1); SET.zemin(R);
    DK.tugla(R, -400, -400, 2400, 640, { z: .26, bw: 200, bh: 80, lw: 4 });
    R.b.fillStyle = gv(.14); R.b.fillRect(-400, 820, 2800, 600); R.m.fillStyle = '#3B5C99'; R.m.fillRect(-400, 820, 2800, 600);
    for (let i = 0; i < 5; i++) { const y = 860 + i * 50; R.d.strokeStyle = dv(.4); R.d.lineWidth = 5; R.d.beginPath(); for (let x = -400; x < 2400; x += 24) { const yy = y + Math.sin(x / 120 + i) * 8; x === -400 ? R.d.moveTo(x, yy) : R.d.lineTo(x, yy); } R.d.stroke(); }
    const g = FIG.fig(R, 1520 + (o.dx ?? 0), 1900, 1550, { tip: 'gilgamis', f: -1, giysi: 'pecek', kol: [[1.5, .2], [.4, .4]], bas: .1 });
    const el = g.elN;
    DK.bitki(R, el[0] - 10, el[1] - 10, 330, { z: .95 });
    const bas = [el[0] - 150, el[1] + 40];
    const pts = []; for (let i = 0; i < 22; i++) { const u = i / 21; pts.push([bas[0] - u * 380 + Math.sin(u * 5) * 60 * u, bas[1] + u * 760]); }
    DK.yilan(R, pts, 88, { z: .92 });
    R.L.dir = [-.5, -.6, .6]; R.L.int = .78; R.L.amb = .2; R.L.col = [1.05, .92, .8];
    R.L.pts.push({ x: el[0] - 20, y: el[1] - 180, z: 260, r: 560, i: 1.1, col: [.6, .8, 1.25] });
    R.after(c => { c.globalCompositeOperation = 'screen'; const gg = c.createRadialGradient(el[0] - 20, el[1] - 180, 10, el[0] - 20, el[1] - 180, 300); gg.addColorStop(0, 'rgba(140,180,255,.55)'); gg.addColorStop(1, 'rgba(60,100,200,0)'); c.fillStyle = gg; c.fillRect(el[0] - 340, el[1] - 500, 680, 640); });
    R.compose(ctx);
    const v = ctx.createRadialGradient(960, 520, 300, 960, 540, 1150); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(10,4,0,.7)'); ctx.fillStyle = v; ctx.fillRect(0, 0, 1920, 1080);
    if (!o.yazisiz) yazi(ctx, o.satir || ['ELİNDEYDİ'], o.x ?? 90, o.y ?? 330, o.px || 300, o);
    return cv;
  },
  B(o) {
    const R = KIL; R.begin({ zemin: .2 }); R.cam(960, 540, 1); SET.zemin(R);
    SET.oda(R, { kapi: false });
    DK.yatak(R, 260, 1150, 790, {});
    FIG.yatan(R, 290, 790, 820, { tip: 'enkidu', ortu: 1 });
    FIG.fig(R, 1390, 1010, 600, { tip: 'gilgamis', f: -1, otur: 1, egilme: .55, bas: .6, kol: [[2.15, 1.5], [1.95, 1.5]] });
    for (let i = 0; i < 7; i++) FIG.cizgi(R, [[1120 + i * 46, 150], [1120 + i * 46, 300]], 13, -.98);
    SET.mesale(R, 1720, 420, { i: 1.9 * (o.mi ?? 1), son: o.son ?? 1 });
    if (o.isik) R.L.pts.push({ x: o.isik[0], y: o.isik[1], z: o.isik[2] ?? 300, r: o.isik[3] ?? 700, i: o.isik[4] ?? 1, col: [1.15, .72, .4] });
    R.L.int = .3; R.L.amb = .13; R.L.col = [.6, .56, .64]; R.L.dir = [-.4, -.6, .7];
    R.compose(ctx);
    if (!o.yazisiz) yazi(ctx, o.satir || ['7 GECE', 'GÖMMEDİ'], o.x ?? 80, o.y ?? 300, o.px || 280, o);
    return cv;
  },
};
window.kapak = (v, o = {}) => KAPAK[v](o);
(async () => { await document.fonts.load('400 200px "Bebas Neue"', 'ELİNDEYDİ GECE GÜN GÖMMEDİ ŞÜ'); KIL.init(); window.READY = true; })();
