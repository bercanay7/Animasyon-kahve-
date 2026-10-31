// 3. tur kapak (yayın sonrası, TO %1,1): "Sultanın öğrencisi" paradoksu tek karede.
// Lamba ışığında ders çalışan fesli öğrenci (Mustafa Kemal, 12); duvara düşen gölgesi kalpaklı Mustafa Kemal (1923).
// ?scene=kapakD (SULTANIN / ÖĞRENCİSİ) | kapakD2 (SULTANIN / OKULUNDA)
'use strict';
// masa lambası: hazne, bilezik, şişe, alev
function kpd_lamp(ctx, x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const lw = px => px / s;
  const foot = SP([[-46, 0], [46, 0], [34, -14], [16, -20], [-16, -20], [-34, -14]], true, .7);
  knock(ctx, foot); plate(ctx, 'ochre', foot, { n: 2 }); plate(ctx, 'sepia', foot, { a: .45 }); inkStroke(ctx, foot, lw(3));
  const font = SP([[-12, -20], [-38, -44], [-40, -72], [-22, -92], [22, -92], [40, -72], [38, -44], [12, -20]], true, .8);
  knock(ctx, font); plate(ctx, 'ochre', font, { n: 2 }); inkStroke(ctx, font, lw(3.2));
  cut(ctx, SP([[-28, -76], [-18, -84]], false), lw(2.4), { a: .8 });
  const collar = PL([[-24, -92], [24, -92], [20, -104], [-20, -104]]); knock(ctx, collar); plate(ctx, 'sepia', collar, { n: 2 }); inkStroke(ctx, collar, lw(2.6));
  const glass = SP([[-14, -104], [-26, -132], [-24, -158], [-12, -176], [-12, -228], [12, -228], [12, -176], [24, -158], [26, -132], [14, -104]], true, .8);
  knock(ctx, glass, '#FBF4E4'); plate(ctx, 'gold', glass, { a: .35 }); inkStroke(ctx, glass, lw(2.8));
  const flame = SP([[0, -118], [9, -136], [0, -168], [-9, -136]], true); knock(ctx, flame, P.gold); knock(ctx, SP([[0, -126], [4, -136], [0, -152], [-4, -136]], true), '#FFF6DE');
  ctx.restore();
}
// açık kitap
function kpd_book(ctx, x, y, s) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  const lw = px => px / s;
  const L = SP([[0, 0], [-120, -10], [-128, 34], [0, 40]], true, .4), R = SP([[0, 0], [120, -10], [128, 34], [0, 40]], true, .4);
  for (const p of [L, R]) { knock(ctx, p, P.paperD); inkStroke(ctx, p, lw(2.6)); }
  plate(ctx, 'sepia', SP([[0, 0], [-16, -2], [-16, 38], [0, 40]], true), { a: .35 });          // sırt oluğu
  inkStroke(ctx, SP([[0, -2], [0, 42]], false), lw(2.4));
  for (const sx of [-1, 1]) inkStroke(ctx, SP([[sx * 118, -8], [sx * 126, 4], [sx * 124, 18]], false), lw(1.6), { a: .7 });   // kıvrık sayfa kenarı
  ctx.restore();
  for (let i = 0; i < 4; i++) { scriptLine(ctx, x - 18 * s, y + (2 + i * 8) * s, 90 * s, 4 * s, 70 + i, { a: .55 }); scriptLine(ctx, x + 110 * s, y + (2 + i * 8) * s, 90 * s, 4 * s, 80 + i, { a: .55 }); }
}
// figür(ler)i ayrı katmanda çizip tek renkli düz gölgeye çevirir (gradyan yok: taş baskı kuralı)
const kpdLayer = makeCanvas(DW, DH), kpdLx = kpdLayer.getContext('2d');
function kpd_shadow(ctx, col, a, fn) {
  kpdLx.setTransform(1, 0, 0, 1, 0, 0); kpdLx.clearRect(0, 0, DW, DH); baseT(kpdLx); fn(kpdLx);
  kpdLx.save(); kpdLx.setTransform(1, 0, 0, 1, 0, 0); kpdLx.globalCompositeOperation = 'source-in'; kpdLx.fillStyle = col; kpdLx.fillRect(0, 0, DW, DH); kpdLx.restore();
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = a; ctx.drawImage(kpdLayer, 0, 0); ctx.restore();
}
// kalpaklı profil silueti (sağa bakar): hafifçe geriye yatık kalpak, yüksek alın, düz burun, belirgin çene, kaputun yüksek yakası.
// Karikatür değil: oranlar 1920'lerin profil fotoğraflarına göre ölçülü (burun ucu alından en çok 16 birim ileride).
function kpd_profile(g, x, y, s) {
  // kalpak: kuzu postu; kafatasından ≈%18 geniş (önde ≈9, arkada ≈12 birim taşar), alında belirgin basamak, tüylü kenar
  const cap = rough([[-60, -40], [-66, -48], [-69, -66], [-71, -81], [-66, -88], [-52, -90], [-36, -91], [-20, -90.5], [-4, -91.5], [12, -90.5], [28, -91], [44, -89], [55, -85], [57, -79], [57, -64], [56, -52], [52, -46], [46, -42]], 1.6, 23);   // yumuşak köşeli, hafif genişleyen silindir; post dokusu kenar pürüzüyle
  const pts = [
    ...cap,
    // alında basamak, kaş çıkıntısı, göz çentiği, uzun düz burun, bıyık, dudaklar, sağlam çene
    [45, -44], [46, -34], [48, -24], [44, -16], [47, -11], [53, -2], [59, 6], [49, 10], [52, 13], [53, 17], [48, 19], [49, 23], [48, 26], [46, 30], [49, 37], [47, 44], [38, 50], [24, 54],
    // boğaz ve kaputun yüksek yakası (önde basamak)
    [18, 64], [22, 76], [44, 84],
    // göğüs ve ön omuz
    [60, 98], [84, 130], [118, 150], [136, 200], [140, 340],
    // arka: sırt, omuz, ense, yuvarlak kafatası arkası
    [-150, 340], [-146, 206], [-130, 128], [-96, 98], [-58, 76], [-48, 52], [-46, 30], [-52, 8], [-58, -8], [-62, -26], [-60, -40]];
  const p = SP(tf(pts, x, y, s), true, .55);
  g.fillStyle = '#000'; g.fill(p);
}
function kapakD(ctx, t, lines) {
  setReg(97, .8); paperBG(ctx);
  // lambanın aydınlattığı duvar: kâğıt + okra; lambadan uzaklaştıkça sepya yarım ton koyulaşır
  const wall = PL([[-20, -20], [W + 20, -20], [W + 20, H + 20], [-20, H + 20]]);
  plate(ctx, 'ochre', wall, { a: .62 });
  radialHT(ctx, 'sepia', 1700, 560, 1000, 1700, 0, .36, { box: [-20, -20, W + 20, H + 20], cell: 13, sy: 4 });
  // duvardaki gölge: kalpaklı, kaputlu Mustafa Kemal (1923), sağa (çocuğa ve ışığa) bakar
  kpd_shadow(ctx, '#2A1E19', .9, g => {
    kpd_profile(g, 590, 470, 2.62);
    g.fillStyle = '#000'; g.fill(PL([[770, 934], [560, 962], [560, 1100], [770, 1100]]));   // masanın duvara düşen gölgesi
  });
  // masa
  const desk = PL(rough([[770, 924], [1680, 916], [1680, 1100], [770, 1100]], 1.2, 4));
  knock(ctx, desk); plate(ctx, 'ochre', desk, { n: 2 }); plate(ctx, 'sepia', desk, { a: .45 });
  inkStroke(ctx, PL([[770, 924], [1680, 916]], false), 6);
  ctx.save(); ctx.clip(desk); plate(ctx, 'gold', SP([[1330, 930], [1560, 922], [1700, 940], [1700, 990], [1450, 994], [1300, 980]], true, .8), { a: .55 }); ctx.restore();   // lamba ışığının masadaki havuzu
  inkStroke(ctx, desk, 4);
  // öğrenci: Mustafa Kemal (12), fes, lacivert setre; kitaba eğilmiş, yüzü lambaya dönük; karenin en parlak yüzü
  kp_bright(() => {
    const o = { x: 1120, y: 700, s: 2.45, dir: 1 };
    bust(ctx, { ...o, coat: 'setre', col: 'navy', w: .9, seed: 12, len: 300, sep: true });
    const ra = REG.amt; REG.amt = 0;
    head3q(ctx, { ...o, who: 'mk', id: { mus: null, jaw: 1.0, cheek: 1.1, HY: .9, eyeOpen: .62, brow: -.08, bags: 0, lines: 0, cheekWedge: 0 }, gear: 'fes', light: 'front', look: [.7, 1.2], age: 16, skin: true, tilt: .24 });
    REG.amt = ra;
  }, '#FBF4E4', '#F6D8BA');
  // masanın ön kenarı figürün önünden geçer
  const deskF = PL(rough([[770, 996], [1680, 990], [1680, 1100], [770, 1100]], 1.2, 6));
  knock(ctx, deskF); plate(ctx, 'ochre', deskF, { n: 2 }); plate(ctx, 'sepia', deskF, { a: .6 }); inkStroke(ctx, PL([[770, 996], [1680, 990]], false), 5);
  kpd_book(ctx, 1140, 952, 1.22);
  kp_bright(() => {
    const A = arm(ctx, [935, 950], [1000, 968], { upper: 16, fore: 54, w: 56, col: 'navy', bend: -1, lw: 4 });
    handDraw(ctx, A.wr[0], A.wr[1], A.ang, 1.45, 'rest', { side: 1, skin: true });
    const B = arm(ctx, [1290, 946], [1254, 962], { upper: 10, fore: 30, w: 56, col: 'navy', bend: 1, lw: 4 });   // gövde kenarından içeri
    handDraw(ctx, B.wr[0], B.wr[1], Math.PI - .2, 1.45, 'rest', { side: -1, skin: true });   // sağ sayfanın üstünde, soldakinin aynası
  }, '#FBF4E4', '#F6D8BA');
  { const m = new Path2D(); m.rect(-20, -20, W + 40, H + 40); m.addPath(desk);   // yalnız masanın olduğu yer kırpılır
    ctx.save(); ctx.clip(m, 'evenodd');
    { const q = new Path2D(); q.arc(1560, 795, 190, 0, TAU); knock(ctx, q); plate(ctx, 'ochre', q, { a: .38 }); }
    radialHT(ctx, 'gold', 1560, 795, 186, 262, .2, 0, { cell: 11 });   // diskin kenarında yoğun, dışa doğru söner
    ctx.restore(); }
  kpd_lamp(ctx, 1560, 968, 1.25);
  // yazı: koyu is, aydınlık duvarın üstünde, sağ üst (x ≤ 1880); kırmızı çizgi altında
  const s1 = kp_fit(ctx, lines[0], 230, 1110), s2 = kp_fit(ctx, lines[1], 260, 1110);
  kp_text(ctx, lines[0], 1880, 44 + s1 * .74, s1, P.ink, 'right');
  kp_text(ctx, lines[1], 1880, 44 + s1 * .74 + 34 + s2 * .96, s2, P.red, 'right');   // ikinci satırın Ö/Ğ/İ işaretleri için pay
  pressFinish(ctx, t, { grain: 0, vig: .45, stone: .1 });
}
SCENES.kapakD = (ctx, t) => kapakD(ctx, t, ['SULTANIN', 'ÖĞRENCİSİ']);
SCENES.kapakD2 = (ctx, t) => kapakD(ctx, t, ['SULTANIN', 'OKULUNDA']);
