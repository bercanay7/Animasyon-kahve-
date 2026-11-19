// Kapaklar (1920×1080 çizilir, 1280×720 kaydedilir). Kullanım: kapak.html?render=1 → window.kapak('A'|'B', o)
// A "ortadan başlamak": kilitli odada örtünün köşesi kalkmış; altında renkli tuvalde çökmüş yüzün bir gözü (tek renk = portre). Yazı: KİMSE GÖRMEDİ.
// B "A, B'yi etkiliyor": Lord Henry'nin sigara dumanı genç Dorian'ın kulağına uzanır; arkada şövalede genç portre. Yazı (4–6 kelime denemesi): HER ŞEY BİR CÜMLEYLE BAŞLADI.
'use strict';
(function () {
  const ST = { t: 2.2, lt: 2.2, p: .5, d: 4, at: 0 };
  function yazi(ctx, satirlar, x, y, px, o = {}) {
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.textAlign = o.align || 'left'; ctx.textBaseline = 'alphabetic';
    ctx.font = `400 ${px}px "Bebas Neue"`; if (o.ls) ctx.letterSpacing = o.ls + 'px'; const lh = px * (o.lh || .92);
    satirlar.forEach((s, i) => {
      ctx.shadowColor = 'rgba(0,0,0,.85)'; ctx.shadowBlur = px * .12; ctx.fillStyle = (o.renk && o.renk[i]) || '#efe6d2'; ctx.fillText(s, x, y + i * lh);
    });
    ctx.restore();
  }
  // örtü: yerel 0..540 × 0..760 (perde() ile aynı), sol üst köşe katlanmış; katlama çizgisi A→B
  function perdeKalkik(x, y, A, B, kenarTon = .62) {
    GR.save(); GR.frame(x, y, 0, 1, 1);
    const kalan = [A, [540, 0], [546, 760], [-8, 760], B];
    INSAN.fill(INSAN.F(kalan), .14, { th: Math.PI / 2, id: 9 });
    for (let i = 0; i < 7; i++) { const xx = 40 + i * 74 + (i % 2) * 12, w = 22 + (i % 3) * 9; const pol = [[xx, 0], [xx + w, 0], [xx + w + 10, 380], [xx + w + 18, 760], [xx - 4, 760], [xx + 4, 380]];
      GR.tx.save(); GR.px.save(); for (const c of [GR.tx, GR.px]) { c.beginPath(); c.moveTo(...A); c.lineTo(540, 0); c.lineTo(546, 760); c.lineTo(-8, 760); c.lineTo(...B); c.closePath(); c.clip(); }
      INSAN.fill(INSAN.Sm(pol), i % 2 ? .05 : .3, { th: Math.PI / 2, id: 9 }); GR.tx.restore(); GR.px.restore(); }
    INSAN.fill(INSAN.F([[-8, 714], [546, 714], [546, 760], [-8, 760]]), kenarTon, { th: 0, id: 9 });
    // katlanan kanat: (0,0) köşesinin A–B çizgisine göre yansıması; alt yüzü daha açık
    const [ax, ay] = A, [bx, by] = B, dx = bx - ax, dy = by - ay, L2 = dx * dx + dy * dy, t = ((0 - ax) * dx + (0 - ay) * dy) / L2, px = ax + t * dx, py = ay + t * dy;
    const K = [2 * px * .82, 2 * py * .82];   // biraz kalkık: tam yansımadan kısa
    INSAN.fill(INSAN.F([A, K, B]), .3, { th: Math.atan2(dy, dx), id: 9 });
    INSAN.fill(INSAN.F([A, [ax + (K[0] - ax) * .08, ay + (K[1] - ay) * .08], [bx + (K[0] - bx) * .08, by + (K[1] - by) * .08], B]), .55, { th: 0, id: 9 });
    GR.restore();
    return [x + K[0], y + K[1]];
  }
  function kapakA(ctx, o) {
    const cam = CAM(o.cx ?? 1170, o.cy ?? 430, o.z ?? 1.7); let Mf;
    levha(ctx, cam, () => { SET.oda(); Mf = SET.cerceve(ODA_FR.x, ODA_FR.y, ODA_FR.s); SET.isik({ x: o.lx ?? 1260, y: o.ly ?? 380, r1: o.r1 ?? 620, a: o.ia ?? .7 }); }, [.02, 0, 0]);
    PORTRE.ciz(ctx, { M: Mf(cam), durum: o.durum || 'C', t: 10, expo: o.expo ?? 1.35 });
    const A = o.A || [470, 0], B = o.B || [0, 700];
    onKatman(ctx, cam, () => {
      const uc = perdeKalkik(1070, 100, A, B);
      // perdeyi tutan el (sol alttan uzanan kol, yüz yok)
      GR.save(); GR.frame(uc[0], uc[1], o.elA ?? .9, 1, 1);
      INSAN.fill(INSAN.F([[30, -34], [620, -60], [620, 60], [30, 38]]), .02);
      INSAN.fill(INSAN.F([[22, -36], [40, -36], [40, 40], [22, 40]]), .45, { th: 0, id: 9 });
      INSAN.fill(INSAN.Sm([[24, -30], [-30, -40], [-66, -30], [-84, -8], [-70, 10], [-40, 6], [-54, 26], [-20, 34], [24, 32]]), .06);
      INSAN.fill(INSAN.Sm([[-30, -40], [-66, -30], [-84, -8], [-80, -14], [-62, -34], [-30, -44]]), .7, { th: 0, id: 10 });
      for (const [y0, x1] of [[-21, -80], [-3, -74], [15, -60]]) INSAN.fill(INSAN.F([[-26, y0 - 2], [x1, y0 - 4], [x1, y0], [-26, y0 + 2]]), .62, { th: 0, id: 10 });   // parmak aralıkları (Fable: "parmaksız eldiven")
      GR.restore();
      
    });
    yazi(ctx, ['KİMSE', 'GÖRMEDİ'], o.tx ?? 44, o.ty ?? 430, o.px ?? 290, { ls: o.ls ?? -7 });   // İ çerçeve kenarına binmesin (Fable)
  }
  function kapakB(ctx, o) {
    const cam = CAM(o.cx ?? 1040, o.cy ?? 420, o.z ?? .95); let Mf;
    levha(ctx, cam, () => { Mf = stuArka(ST, { isik: o.isik ?? .35 }); }, [.03, 0, 0]);
    PORTRE.ciz(ctx, { M: Mf(cam), durum: 'G', t: 10, expo: .95 });
    onKatman(ctx, cam, () => {
      const h = HENRY(o.hx ?? 330, { yon: 1, h: 1040, y: 1300, kolOn: { a: o.ka ?? .25, b: o.kb ?? .35 }, kolArka: { a: -.1, b: .3 }, sigara: true, kenar: .6, egim: .02 });
      const d = DOR(o.dx ?? 1080, { y: 1300, h: 1000, arka: false, yon: -1, kenar: .55, kenarYan: -1, bas: .1, kolOn: { a: .05, b: .1 } });
      // duman: sigaradan Dorian'ın kulağına giden tek çizgi
      const x0 = o.sx ?? 482, y0 = o.sy ?? 300, x1 = o.kx ?? 1030, y1 = o.ky ?? 390; 
      for (let k = 0; k <= 70; k++) { const q = k / 70, x = x0 + (x1 - x0) * q, y = y0 + (y1 - y0) * q - Math.sin(q * Math.PI) * (o.kav ?? 90) + Math.sin(q * 13) * 9;
        INSAN.fill(SET.E2(x, y, 10 + 6 * Math.sin(q * Math.PI), 4 + 2 * Math.sin(q * Math.PI), .3 + q), .92 - .15 * q, { th: 0, id: 10 }); }
    });
    if (o.bant !== 0) { ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); const g = ctx.createLinearGradient(0, 0, 0, o.bant ?? 430); g.addColorStop(0, 'rgba(0,0,0,.78)'); g.addColorStop(.8, 'rgba(0,0,0,.6)'); g.addColorStop(1, 'rgba(0,0,0,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, W, o.bant ?? 430); ctx.restore(); }   // yazı altına koyu bant (Fable)
    yazi(ctx, o.satir || ['HER ŞEY BİR', 'CÜMLEYLE BAŞLADI'], o.tx ?? 960, o.ty ?? 175, o.px ?? 190, { align: 'center' });
  }
  window.kapak = (v, o = {}) => {
    const cv = document.getElementById('c'), ctx = cv.getContext('2d'); baseT(ctx); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, H);
    (v === 'A' ? kapakA : kapakB)(ctx, o); return cv;
  };
})();
