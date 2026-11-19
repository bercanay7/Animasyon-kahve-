// Portrenin tuvali: düz, değer planlı resim (impasto motoru bunu bıçak darbelerine çevirir). Klasik betik.
// Yerel çerçeve: çerçevenin dış köşesi (0,0), 500×720; tuval IN (46,46)–(454,674). Çerçeveyi gravür çizer (setler.js), burası yalnız tuval.
// Durumlar: G genç · Z zalimlik çizgisi (VII) · Y yıllar · C çökmüş (XIII) · I ikiyüzlülük kıvrımı (XX).
// Kaynak tarifi: genç = "dürüst mavi gözler, gür altın saç, ince kıvrımlı kırmızı dudaklar" (II); çökmüş = "incelen saçta hâlâ biraz altın,
// ağız ağır ve şehvetli, sulu gözlerde mavinin kalıntısı, kırışan alın" (XIII, 5800–5804; XI, 4878–4880).
// İmza: sol alt köşede kırmızı uzun harflerle BASIL HALLWARD (XIII, 5808–5809).
'use strict';
(function (g) {
  const PI = Math.PI;
  const P = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
  const Ell = (x, y, rx, ry, r = 0) => c => { c.moveTo(x + rx * Math.cos(r), y + rx * Math.sin(r)); c.ellipse(x, y, rx, ry, r, 0, PI * 2); };
  const S = pts => c => { const n = pts.length; c.moveTo(pts[0][0], pts[0][1]);
    for (let i = 0; i < n; i++) { const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      c.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]); }
    c.closePath(); };
  const IN = { x: 46, y: 46, w: 408, h: 628 };
  const DUR = { G: { k: 0 }, Z: { k: .06, zalim: 1 }, Y: { k: .5, zalim: 1 }, C: { k: 1, zalim: 1 }, I: { k: 1, zalim: 1, ikiyuz: 1 } };
  const hx = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
  const mixc = (a, b, k) => { const A = hx(a), B = hx(b); return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, '0')).join(''); };

  // R: { fill(pathFn, renk, props), line(pathFn, renk, kalınlık, props), text(s, x, y, font, renk, props) } (impasto Ref arayüzü)
  function tuval(R, durum) {
    const d = DUR[durum] || DUR.G, k = d.k, mix = (a, b) => mixc(a, b, k);
    const ix = IN.x, iy = IN.y, iw = IN.w, ih = IN.h, cx = ix + iw * .52, hy = iy + 236;
    // zemin: koyu sıcak kahve; resmin içindeki ışık sol üstten
    R.fill(P([[ix - 4, iy - 4], [ix + iw + 4, iy - 4], [ix + iw + 4, iy + ih + 4], [ix - 4, iy + ih + 4]]), mix('#4c3421', '#2c2a1c'), { dir: 30, maxR: 22, group: 'tuval', detail: 1.2 });
    R.fill(Ell(ix + 120, iy + 150, 190, 220), mix('#6a4a2c', '#3a3424'), { dir: 30, maxR: 22, group: 'tuval' });
    // gövde: koyu redingot, beyaz yaka, koyu kravat; geniş omuz (erkek)
    R.fill(S([[cx - 190, iy + ih + 10], [cx - 178, hy + 190], [cx - 110, hy + 132], [cx - 36, hy + 114], [cx + 52, hy + 118], [cx + 132, hy + 142], [cx + 182, hy + 200], [cx + 196, iy + ih + 10]]), mix('#17120f', '#121410'), { dir: 70, maxR: 12, group: 'ceket' });
    R.fill(P([[cx - 30, hy + 112], [cx + 38, hy + 114], [cx + 30, hy + 150], [cx - 24, hy + 150]]), mix('#eee4ce', '#bab49c'), { dir: 0, maxR: 4, group: 'yaka' });
    R.fill(P([[cx - 16, hy + 122], [cx + 22, hy + 123], [cx + 12, hy + 196], [cx - 2, hy + 198]]), mix('#2c1e30', '#211b1b'), { dir: 90, maxR: 4, group: 'kravat' });
    R.fill(P([[cx - 36, hy + 112], [cx - 16, hy + 122], [cx - 6, hy + 236], [cx - 60, hy + 160]]), mix('#221a16', '#1a1814'), { dir: 70, maxR: 5, group: 'ceket' });   // yaka devrik kenarı
    // boyun
    R.fill(P([[cx - 32, hy + 60], [cx + 22, hy + 64], [cx + 28, hy + 116], [cx - 32, hy + 114]]), mix('#b8875e', '#6e6a4e'), { dir: 80, maxR: 5, group: 'boyun' });
    // baş: ¾, izleyicinin soluna bakar; çene köşeli (erkek), çökmüşte gıdı sarkar
    const ten = mix('#e6bf98', '#b2a27a'), tenG = mix('#b48460', '#786a4a'), tenK = mix('#9a6a48', '#5a4c34');
    const sark = 8 * k;
    const yuz = [[cx - 10, hy - 110], [cx - 50, hy - 98], [cx - 62, hy - 60], [cx - 64, hy - 22], [cx - 60, hy + 8], [cx - 56, hy + 40 + sark], [cx - 44, hy + 66 + sark], [cx - 22, hy + 82 + sark], [cx + 12, hy + 84 + sark], [cx + 40, hy + 64 + sark], [cx + 56, hy + 26], [cx + 62, hy - 26], [cx + 54, hy - 82], [cx + 26, hy - 104]];
    R.fill(S(yuz), ten, { dir: 'edge', maxR: 6, group: 'yuz', detail: .7 });
    R.fill(S([[cx + 22, hy - 98], [cx + 54, hy - 82], [cx + 62, hy - 26], [cx + 56, hy + 26], [cx + 40, hy + 64 + sark], [cx + 12, hy + 84 + sark], [cx + 4, hy + 62], [cx + 24 - 6 * k, hy + 26], [cx + 30, hy - 10], [cx + 28, hy - 62]]), tenG, { dir: 'edge', maxR: 5, group: 'yuz' });
    R.fill(S([[cx - 50, hy + 54 + sark], [cx - 20, hy + 74 + sark], [cx + 14, hy + 76 + sark], [cx + 34, hy + 62 + sark], [cx + 12, hy + 86 + sark], [cx - 24, hy + 84 + sark]]), mix('#c99a74', '#6e6248'), { dir: 0, maxR: 4, group: 'yuz' });   // çene altı gölgesi
    if (k > .3) R.fill(S([[cx + 20, hy + 6], [cx + 44, hy - 4], [cx + 48, hy + 30], [cx + 30, hy + 50], [cx + 16, hy + 40]]), mix('#b48460', '#5c4e36'), { maxR: 4, group: 'yuz' });
    // saç: kısa yanlar, üstte dalga; genç gür altın, çökmüş incelmiş grileşmiş altın; favori
    const ac = 14 * k;
    R.fill(S([[cx - 62, hy - 44], [cx - 70, hy - 92], [cx - 46, hy - 132 + ac * .3], [cx - 4, hy - 146 + ac], [cx + 42, hy - 136 + ac * .6], [cx + 66, hy - 100], [cx + 66, hy - 58], [cx + 58, hy - 34], [cx + 54, hy - 76], [cx + 30, hy - 100 + ac], [cx + 2, hy - 104 + ac], [cx - 24, hy - 96 + ac], [cx - 46, hy - 88 + ac * .5], [cx - 56, hy - 62]]),
      mix('#ae8636', '#8c8468'), { dir: 'edge', maxR: 6, group: 'sac' });
    R.fill(P([[cx + 52, hy - 40], [cx + 62, hy - 38], [cx + 60, hy + 6], [cx + 52, hy + 4]]), mix('#8a6a2c', '#7a7462'), { dir: 90, maxR: 3, group: 'favori' });
    for (const [x0, y0, x1, y1] of [[cx - 38, hy - 128, cx - 54, hy - 86], [cx - 2, hy - 138 + ac, cx - 20, hy - 104 + ac], [cx + 32, hy - 128 + ac * .6, cx + 18, hy - 100 + ac]])
      R.line(c => { c.moveTo(x0, y0); c.quadraticCurveTo((x0 + x1) / 2 + 10, (y0 + y1) / 2, x1, y1); }, mix('#6a4c1c', '#5c584a'), 4, { maxR: 2, group: 'sacc' + x0 });
    // kaşlar: kalın, düz (erkek); çökmüşte iç uç aşağı
    const ey = hy - 24;
    R.line(c => { c.moveTo(cx - 58, ey - 13 + 3 * k); c.quadraticCurveTo(cx - 42, ey - 21, cx - 22, ey - 17 - 3 * k); }, mix('#6a4818', '#4a4436'), 7, { maxR: 2, group: 'kas1' });
    R.line(c => { c.moveTo(cx - 2, ey - 17 - 3 * k); c.quadraticCurveTo(cx + 18, ey - 23, cx + 42, ey - 15); }, mix('#5c3e14', '#3e3a2e'), 7, { maxR: 2, group: 'kas2' });
    // gözler: badem, kapak çizgisi, iris (genç mavi; çökmüş soluk ve ağır kapaklı: "sinsilik bakışı" I'de daha kısık)
    const kis = d.ikiyuz ? 1.4 : 0;
    for (const [ex, w, gid] of [[cx - 38, 12, 'g1'], [cx + 14, 14, 'g2']]) {
      R.fill(Ell(ex, ey, w, Math.max(2.2, 5.6 - 1.6 * k - kis), 0), mix('#ece2d0', '#c8bc96'), { maxR: 2, group: 'ak' + gid });
      R.fill(Ell(ex - 2, ey + .5, 4.6, Math.max(2, 4.6 - 1.4 * k - kis), 0), mix('#3a5a8a', '#4a5250'), { maxR: 2, group: 'ir' + gid });
      R.line(c => { c.moveTo(ex - w - 2, ey + 1); c.quadraticCurveTo(ex, ey - 8 + 3 * k + kis * 2, ex + w + 2, ey); }, mix('#3a2414', '#2a2418'), 3 + 2 * k, { maxR: 2, group: 'kp' + gid });
      if (k > .3) R.line(c => { c.moveTo(ex - w, ey + 9); c.quadraticCurveTo(ex, ey + 15, ex + w, ey + 8); }, '#6a5c40', 2.5, { maxR: 2, group: 'tk' + gid });
    }
    // burun: sırt ve sağında ince gölge, burun deliği
    R.fill(S([[cx - 22, ey + 6], [cx - 14, ey + 8], [cx - 12, hy + 26], [cx - 20, hy + 33], [cx - 30, hy + 30]]), tenG, { maxR: 3, group: 'burun' });
    R.fill(Ell(cx - 24, hy + 33, 7, 3.5, 0), tenK, { maxR: 2, group: 'delik' });
    // ağız: genç ince kıvrımlı (soluk gül rengi); Z: bir köşe aşağı, sert çizgi; I: diğer köşe yukarı kıvrılır (ikiyüzlülük)
    const ay = hy + 52, z = d.zalim ? 1 : 0, iy2 = d.ikiyuz ? 1 : 0;
    R.fill(S([[cx - 34, ay + 2 * z], [cx - 20, ay - 5], [cx - 12, ay - 3], [cx - 2, ay - 5], [cx + 10, ay - 1 - 7 * iy2], [cx - 12, ay + 1]]), mix('#9a4a3e', '#6a3a2c'), { maxR: 2, group: 'ustdudak' });
    R.fill(S([[cx - 30, ay + 2 + 2 * z], [cx - 12, ay + 2], [cx + 8, ay - 7 * iy2], [cx - 4, ay + 9 + 4 * k], [cx - 22, ay + 9 + 4 * k]]), mix('#b46a5c', '#7c4c3a'), { maxR: 2, group: 'altdudak' });
    if (z) R.line(c => { c.moveTo(cx - 34, ay + 2); c.quadraticCurveTo(cx - 40, ay + 8, cx - 42, ay + 16); }, mix('#7a4a34', '#3e3226'), 3, { maxR: 2, group: 'zalim' });   // zalimlik çizgisi: sol köşe aşağı
    if (iy2) R.line(c => { c.moveTo(cx + 9, ay - 6); c.quadraticCurveTo(cx + 20, ay - 12, cx + 22, ay - 24); }, '#3e3024', 3.2, { maxR: 2, group: 'kivrim' });  // ikiyüzlülük kıvrımı
    if (k > .3) {
      R.line(c => { c.moveTo(cx - 36, hy + 28); c.quadraticCurveTo(cx - 46, ay, cx - 40, ay + 20); }, '#6a5c40', 2.5, { maxR: 2, group: 'kir1' });
      for (const yy of [hy - 76, hy - 64]) R.line(c => { c.moveTo(cx - 44, yy); c.quadraticCurveTo(cx - 6, yy - 5, cx + 34, yy); }, '#7c6e4c', 2.2, { maxR: 2, group: 'alin' + yy });
    }
    // imza (kırmızı, uzun harfler; sol alt)
    R.text('BASIL HALLWARD', ix + 104, iy + ih - 22, 'italic 600 21px "Cormorant Garamond", serif', '#c0392b', { align: 'center', maxR: 1.2, group: 'imza', hgt: 1.2 });
  }
  g.PORTRE_CIZ = { tuval, IN, DUR, W: 500, H: 720 };
})(window);
