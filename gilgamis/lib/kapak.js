// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir). A: "ortadan başlamak" (bitki elde, yılan kapıyor). B: "karşıtlık" (örtülü dost / başında oturan adam, eli dostunun göğsünde).
// Kapak sistemi (kanal/KAPAK_SISTEMI.md, 27 Kasım): yazı sol üst, figür sağ; Bebas fildişi, 2 satır, tek kelime vurgu renginde; font ≥ 290 px; tek odak (yazı hariç en parlak yer); sağ alt süre rozeti bölgesi (x>1440, y>829) boş.
// Son kapaklar (27 Kasım, Fable düzeltmesi). Her biri ayrı süreçte çekilir: sayfanın ilk çizimi sonrakilerden yatak ayağında birkaç yüz pikselde ayrılıyor, yazısız farkla yazı ölçümü bozuluyordu.
//   A: '{"dx":260,"satir":["BİR AN","ELİNDEYDİ"],"vurgu":"ELİNDEYDİ","vcol":"#E2B04F","y":290,"px":300,"yilanS":[-150,30,88,-0.6],"su":"#3D5275","suAlti":["rgba(30,42,70,0.6)",2800]}'  (+ "ad":"A_yazisiz","yazisiz":1)
//      yılan tek S kıvrımıyla sudan çıkar, açık ağzı bitkinin sapında; su biraz soluk, suyun altındaki gövde su rengiyle örtülü.
//   B: '{"satir":["7 GECE","GÖMMEDİ"],"vurgu":"GÖMMEDİ","vcol":"#F2A04A","px":300,"y":300,"son":0.45,"centik":0,"yatak":[140,980,800,170,790],"fig":[1350,1050,800],"tabure":[[1300,1050],[1300,880],[1430,880],[1430,1050]],"basO":{"kapali":1},"eg":0.6,"bas":0.9,"kol":[[1.1,0.3],[0.5,0.9]],"isik":[1100,680,280,650,1.6]}'  (+ "ad":"B_yazisiz","yazisiz":1)
//      duvardaki yedi çentik kaldırıldı (pencere parmaklığı okunuyordu); oturan adam büyük (s 800), başı eğik, gözü kapalı, eli örtülü dostun göğsünde.
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
// A'nın yılanı (Fable, 27 Kasım: küçük boyda zincir/halat okunuyordu): sudan tek S kıvrımıyla yükselir; baş koyu konturla ayrılır, açık ağız bitkinin sapına döner.
// y: [baş ofseti x, y, ölçek w, açı]; baş el'e göre konur.
function yilanS(R, el, y) {
  const [ox, oy, w, ang0] = y, H = [el[0] + ox, el[1] + oy];
  // omurga: baştan kuyruğa; boyun bitkiye dönük, gövde sola kıvrılıp suya iner
  const yol = [H, [H[0] - 70, H[1] + 40], [H[0] - 150, H[1] + 120], [H[0] - 190, H[1] + 230], [H[0] - 140, H[1] + 330], [H[0] - 40, H[1] + 410], [H[0] + 10, H[1] + 510], [H[0] - 30, H[1] + 620], [H[0] - 120, H[1] + 720]];
  const pts = []; for (let i = 0; i < 26; i++) { const t = i / 25 * (yol.length - 1), k = Math.min(yol.length - 2, Math.floor(t)), f = t - k;
    const p0 = yol[Math.max(0, k - 1)], p1 = yol[k], p2 = yol[k + 1], p3 = yol[Math.min(yol.length - 1, k + 2)];
    const cr = (a, b, c, d) => .5 * ((2 * b) + (-a + c) * f + (2 * a - 5 * b + 4 * c - d) * f * f + (-a + 3 * b - 3 * c + d) * f * f * f);
    pts.push([cr(p0[0], p1[0], p2[0], p3[0]), cr(p0[1], p1[1], p2[1], p3[1])]); }
  DK.yilan(R, pts, w, { z: .92 });
  // baş: açık çene (üst ve alt), koyu kontur, küçük koyu göz; DK.yilan'ın başının üstüne
  const T = (x, yy) => [H[0] + (x * Math.cos(ang0) - yy * Math.sin(ang0)) * w, H[1] + (x * Math.sin(ang0) + yy * Math.cos(ang0)) * w];
  const ust = [T(-.35, -.5), T(.3, -.62), T(1.05, -.62), T(1.55, -.5), T(1.6, -.32), T(.55, -.08), T(-.35, -.02)];
  const alt = [T(-.35, .02), T(.5, .1), T(1.35, .45), T(1.3, .62), T(.4, .52), T(-.35, .45)];
  for (const j of [alt, ust]) FIG.sekil(R, j, .97, .5, null, .6);
  // ağız içi: çenelerin arasındaki kama koyu (oyuk)
  const kama = [T(.15, -.06), T(1.6, -.3), T(1.32, .42)];
  R.b.fillStyle = gv(.55); R.b.beginPath(); kama.forEach((p, i) => i ? R.b.lineTo(p[0], p[1]) : R.b.moveTo(p[0], p[1])); R.b.fill();
  R.d.fillStyle = dv(-.95); R.d.beginPath(); kama.forEach((p, i) => i ? R.d.lineTo(p[0], p[1]) : R.d.moveTo(p[0], p[1])); R.d.fill();
  // dil: çatallı, sapa doğru
  const d0 = T(.4, .0), d1 = T(1.9, -.05), d2 = T(2.15, -.2), d3 = T(2.15, .1);
  R.d.strokeStyle = dv(-.9); R.d.lineWidth = Math.max(2, w * .07); R.d.beginPath(); R.d.moveTo(d0[0], d0[1]); R.d.lineTo(d1[0], d1[1]); R.d.lineTo(d2[0], d2[1]); R.d.moveTo(d1[0], d1[1]); R.d.lineTo(d3[0], d3[1]); R.d.stroke();
  // baş konturu: koyu, kalın (zeminden ayrılsın)
  R.d.strokeStyle = dv(-.95); R.d.lineWidth = Math.max(3, w * .08); R.d.lineJoin = 'round';
  for (const j of [ust, alt]) { R.d.beginPath(); j.forEach((p, i) => i ? R.d.lineTo(p[0], p[1]) : R.d.moveTo(p[0], p[1])); R.d.closePath(); R.d.stroke(); }
  const g = T(.55, -.33); R.d.fillStyle = dv(-.95); R.d.beginPath(); R.d.arc(g[0], g[1], w * .085, 0, TAU); R.d.fill();
}
const KAPAK = {
  A(o) {
    const R = KIL; R.begin({ zemin: .2 }); R.cam(960, 540, 1); SET.zemin(R);
    DK.tugla(R, -400, -400, 2400, 640, { z: .26, bw: 200, bh: 80, lw: 4 });
    R.b.fillStyle = gv(.14); R.b.fillRect(-400, 820, 2800, 600); R.m.fillStyle = o.su || '#3B5C99'; R.m.fillRect(-400, 820, 2800, 600);
    for (let i = 0; i < 5; i++) { const y = 860 + i * 50; R.d.strokeStyle = dv(.4); R.d.lineWidth = 5; R.d.beginPath(); for (let x = -400; x < 2400; x += 24) { const yy = y + Math.sin(x / 120 + i) * 8; x === -400 ? R.d.moveTo(x, yy) : R.d.lineTo(x, yy); } R.d.stroke(); }
    const g = FIG.fig(R, 1520 + (o.dx ?? 0), 1900, 1550, { tip: 'gilgamis', f: -1, giysi: 'pecek', kol: [[1.5, .2], [.4, .4]], bas: .1 });
    const el = g.elN;
    DK.bitki(R, el[0] - 10, el[1] - 10, 330, { z: .95 });
    if (!o.yilanS) {
      const bas = [el[0] - 150, el[1] + 40];
      const pts = []; for (let i = 0; i < 22; i++) { const u = i / 21; pts.push([bas[0] - u * 380 + Math.sin(u * 5) * 60 * u, bas[1] + u * 760]); }
      DK.yilan(R, pts, 88, { z: .92 });
    } else yilanS(R, el, o.yilanS);
    R.L.dir = [-.5, -.6, .6]; R.L.int = .78; R.L.amb = .2; R.L.col = [1.05, .92, .8];
    R.L.pts.push({ x: el[0] - 20, y: el[1] - 180, z: 260, r: 560, i: 1.1, col: [.6, .8, 1.25] });
    R.after(c => { c.globalCompositeOperation = 'screen'; const gg = c.createRadialGradient(el[0] - 20, el[1] - 180, 10, el[0] - 20, el[1] - 180, 300); gg.addColorStop(0, 'rgba(140,180,255,.55)'); gg.addColorStop(1, 'rgba(60,100,200,0)'); c.fillStyle = gg; c.fillRect(el[0] - 340, el[1] - 500, 680, 640); });
    // suyun altında kalan gövde: su rengiyle örtülür (yılan sudan çıkıyor; ısı haritasının tepesi suyun içindeki pullardan bitkiye döner)
    if (o.suAlti) R.after(c => { c.globalCompositeOperation = 'source-over'; c.fillStyle = o.suAlti[0]; c.fillRect(-400, 832, o.suAlti[1], 600); });
    R.compose(ctx);
    const v = ctx.createRadialGradient(960, 520, 300, 960, 540, 1150); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(10,4,0,.7)'); ctx.fillStyle = v; ctx.fillRect(0, 0, 1920, 1080);
    if (!o.yazisiz) yazi(ctx, o.satir || ['ELİNDEYDİ'], o.x ?? 90, o.y ?? 330, o.px || 300, o);
    return cv;
  },
  B(o) {
    const R = KIL; R.begin({ zemin: .2 }); R.cam(960, 540, 1); SET.zemin(R);
    SET.oda(R, { kapi: false });
    const yt = o.yatak || [260, 1150, 790, 290, 820];   // yatak x0, x1, y; yatan x, boy
    DK.yatak(R, yt[0], yt[1], yt[2], {});
    FIG.yatan(R, yt[3], yt[2], yt[4], { tip: 'enkidu', ortu: 1 });
    const fg = o.fig || [1390, 1010, 600];
    if (o.tabure) FIG.sekil(R, o.tabure, .48, .5, null, 0);
    FIG.fig(R, fg[0], fg[1], fg[2], { tip: 'gilgamis', f: -1, otur: 1, egilme: o.eg ?? .55, bas: o.bas ?? .6, kol: o.kol || [[2.15, 1.5], [1.95, 1.5]], bacak: o.bacak, basO: o.basO });
    if (o.centik !== 0) for (let i = 0; i < 7; i++) FIG.cizgi(R, [[1120 + i * 46, 150], [1120 + i * 46, 300]], 13, -.98);
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
