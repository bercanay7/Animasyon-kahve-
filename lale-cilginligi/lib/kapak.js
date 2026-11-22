// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir). kapak.html?render=1 → window.kapak('A'|'B', o)
// A "karşıtlık": terazi; kefede renkli lale (tek renk) ve soğan ağır basar, öbür kefede ev havada. Yazı: BİR EV FİYATINA (iki satır).
// B "hareket oku": karanlık meyhane; dirsekten kırık, yukarı uzanan eller tek renkli laleye; lalenin sapı yukarı tırmanan bir fiyat çizgisi. Yazı: HERKES ALIYORDU.
// Kurallar: renk yalnız lalede; harf yüksekliği ≥ %18 (Bebas büyük harf ≈ 0,70 em → font ≥ 280 px); sağ alt süre rozeti (x 1440–1874, y 829–1034) boş.
'use strict';
(function () {
  function yazi(ctx, satirlar, x, y, px, o = {}) {
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.textAlign = o.align || 'left'; ctx.textBaseline = 'alphabetic';
    ctx.font = `400 ${px}px "Bebas Neue"`; if (o.ls) ctx.letterSpacing = o.ls + 'px'; const lh = px * (o.lh || .9);
    satirlar.forEach((s, i) => { ctx.shadowColor = o.golge || 'rgba(0,0,0,.6)'; ctx.shadowBlur = px * .1; ctx.fillStyle = (o.renk && o.renk[i]) || o.col || '#1a1715'; ctx.fillText(s, x, y + i * lh); });
    ctx.restore();
  }
  const cam0 = { cx: 960, cy: 540, z: 1 };
  // asılı terazi (ayaksız: sağ alt rozet alanı boş kalsın): kanca (hx, hy), kol L, eğim a (+ sağ aşağı)
  function asiliTerazi(hx, hy, L, a) {
    const F = INSAN.F, fill = INSAN.fill;
    fill(SET.R(hx - 4, -100, 8, hy + 100), .1, { th: Math.PI / 2, id: 9 });
    fill(SET.E2(hx, hy, 18, 18), .25, { type: 'rad', cx: hx, cy: hy, id: 9 });
    const c = Math.cos(a), s = Math.sin(a), lx = hx - c * L, ly = hy - s * L, rx = hx + c * L, ry = hy + s * L;
    fill(F([[lx - s * 9, ly + c * 9], [rx - s * 9, ry + c * 9], [rx + s * 9, ry - c * 9], [lx + s * 9, ly - c * 9]]), .08, { th: a, id: 9 });
    const ip = asiliTerazi.ip || 300, kef = [];
    for (const [ex, ey] of [[lx, ly], [rx, ry]]) { const kx = ex, ky = ey + ip;
      for (const d of [-1, 1]) fill(F([[ex - 2, ey], [ex + 2, ey], [kx + d * 130 + 2, ky], [kx + d * 130 - 2, ky]]), .1, { th: Math.PI / 2, id: 9 });
      fill(INSAN.Sm([[kx - 150, ky], [kx + 150, ky], [kx + 118, ky + 36], [kx - 118, ky + 36]]), .18, { th: 0, id: 9 }); kef.push([kx, ky]); }
    return kef;
  }
  function A(o = {}) {
    const cam = { cx: 960, cy: 540, z: 1 };
    LALE.sifirla(); YAZI.sifirla();
    levha(ctx, cam, () => {
      GR.fill(SET.R(-400, -400, 2800, 1900), GR.tone(.84), { th: 0, id: 10 });   // zemin bir kademe koyu (Fable: kapak akışta soluk)
      asiliTerazi.ip = o.ip ?? 380; const [K1, K2] = asiliTerazi(o.hx ?? 1320, o.hy ?? 260, o.L ?? 340, o.a ?? .3); asiliTerazi.ip = 300;
      // sol kefe yukarıda: ev; sağ kefe aşağıda: soğan + çiçek
      SET.ev(K1[0] - 120, K1[1], 240, 180, { ton: .3, basamak: 3, kat: 1 });
      LALE.sogan(K2[0], K2[1] - 50, 1.8); LALE.ciz(K2[0], K2[1] - 186, 2.6, { sap: 56, cesit: 'semper', ac: .35 });   // lale ve soğan ~%25 büyük: tek odak
      SET.isik({ x: K2[0], y: K2[1] - 300, r1: 460, a: .75 });
    }, [.84, 0, 10]);
    YAZI.bas(ctx, cam); LALE.boya(ctx, cam, 1, { kay: 2.5, alevK: 2.3, alevN: 1 }); LALE.boya(ctx, cam, .4, { kay: 2.5, alevK: 2.3, alevN: 1 });   // kapakta alevler kalın, ikinci kat boya: küçük boyda kırmızı görünsün
    post(ctx, 0);
    yazi(ctx, ['BİR EV', 'FİYATINA'], 70, o.ty ?? 450, o.px ?? 300, { col: '#1a1715', golge: 'rgba(0,0,0,0)', lh: 1.0 });   // satır arası açık: İ noktaları üst üste binmesin
  }
  function B(o = {}) {
    const cam = { cx: o.cx ?? 1060, cy: o.cy ?? 560, z: o.z ?? 1.25 };
    LALE.sifirla(); YAZI.sifirla();
    levha(ctx, cam, () => {
      GR.fill(SET.R(-400, -400, 2800, 1900), GR.tone(.06), { th: 0, id: 0 });
      for (let x = -300; x < 2400; x += 260) GR.fill(INSAN.F([[x, -60], [x + 70, -60], [x + 50, 150], [x + 20, 150]]), GR.tone(.03), { th: Math.PI / 2, id: 9 });
      SET.masa(1000, 640, 420); SET.saksi(1210, 640, 1.25); LALE.ciz(1210, 480, 1.95, { sap: 90, cesit: 'semper', ac: .3 });
      SET.isik({ x: 1210, y: 500, r1: 560, a: 1 });
      INSAN.adam({ x: 1500, y: 900, h: 560, yon: -1, sapka: 'genis', yaka: 'duz', kenar: .6, kenarYan: -1, kolOn: { a: 2.0, b: .9 }, biyik: true, sakal: true });
      const A = [[850, 1180, 760, 1, 2.1, 1.0], [1040, 1230, 820, -1, 2.55, .55], [1700, 1220, 800, 1, 2.15, .95], [1960, 1180, 760, -1, 2.05, 1.0]];
      A.forEach(([x, y, h, yon, a, b]) => INSAN.adam({ x, y, h, yon, arka: true, sapka: 'genis', yaka: 'duz', kenar: .5, kenarYan: yon, giysi: 'pelerin', kolOn: { a, b } }));
    }, [.06, 0, 0]);
    YAZI.bas(ctx, cam); LALE.boya(ctx, cam, 1, { kay: 2.5, alevK: 2.3, alevN: 1 });
    post(ctx, 0);
    yazi(ctx, ['HERKES', 'ALIYORDU'], 60, o.ty ?? 300, o.px ?? 285, { col: '#efe6d2', golge: 'rgba(0,0,0,.9)' });
  }
  window.kapak = (v, o = {}) => { baseT(ctx); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H); (v === 'A' ? A : B)(o); return cv; };
})();
