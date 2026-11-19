// Dorian Gray üslup kapısı: ORTAK SAHNE (üç aday aynı sahneyi çizer).
// Sahne: XX. bölüm (1891), çatı katındaki eski okul odası. Lamba masada; Dorian sırtı dönük, sağ eliyle
// "altın işlemeli mor saten örtüyü" (X. bölüm) portrenin üstünden çeker; portrede çökmüş yüz.
// Sahne "düz, değer planlı bir resim" olarak tanımlanır: her parça bir yol + renk (+ gravür taraması + impasto fırça ayarı).
//   gravür adayı: ton = rengin parlaklığı (ya da parçanın `ton` alanı), tarama `h`;
//   impasto adayı: renk `c`, fırça ayarı `p` (Lemo plate.js Ref.fill props);
//   karma aday: dünya gravür, yalnız `portre` levhası impasto.
// Levhalar (plates): her biri kendi yerel koordinatında çizilir ve zamanla bir dönüşüm alır ({x, y, a, k}).
'use strict';
(function (g) {
  const PI = Math.PI;
  const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const ss = t => { t = cl(t); return t * t * (3 - 2 * t); };
  const seg = (t, a, b) => cl((t - a) / (b - a));
  const io3 = t => { t = cl(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
  const in2 = t => { t = cl(t); return t * t; };
  const P = pts => c => { c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); };
  const Ell = (x, y, rx, ry, r = 0) => c => { c.moveTo(x + rx * Math.cos(r), y + rx * Math.sin(r)); c.ellipse(x, y, rx, ry, r, 0, PI * 2); };
  const Rc = (x, y, w, h) => P([[x, y], [x + w, y], [x + w, y + h], [x, y + h]]);
  // pürüzsüz kapalı eğri (Catmull-Rom → Bézier)
  const S = pts => c => {
    const n = pts.length; c.moveTo(pts[0][0], pts[0][1]);
    for (let i = 0; i < n; i++) {
      const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n], p3 = pts[(i + 2) % n];
      c.bezierCurveTo(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]);
    }
    c.closePath();
  };
  const lum = hex => { const v = parseInt(hex.slice(1), 16); return ((v >> 16 & 255) * .3 + (v >> 8 & 255) * .59 + (v & 255) * .11) / 255; };

  // ── ölçüler ──
  const FR = { x: 1090, y: 120, w: 500, h: 720, b: 46 };          // altın çerçeve (dış)
  const IN = { x: FR.x + FR.b, y: FR.y + FR.b, w: FR.w - 2 * FR.b, h: FR.h - 2 * FR.b };   // tuval
  const LAMP = { x: 905, y: 650 };                                  // lamba alevi (masada)
  const FLOOR = 905;
  // tarama doğrultuları (radyan)
  const H0 = 0, HV = PI / 2, HD = .55, HD2 = -.55;

  // Bir levha: draw(R) R.fill(pathFn, { c, h, p, ton }) ve R.line(pathFn, c, w, { h, p }) çağırır.
  const LEV = {};

  // 1) ODA (durağan): arka duvar, eğik tavan kirişi, lambri, döşeme, kitaplık, masa ve lamba gövdesi
  LEV.oda = { draw(R) {
    R.fill(Rc(-40, -40, 2000, 1160), { c: '#15100c', h: { th: H0, id: 0 }, p: { dir: 4, maxR: 40, group: 'duvar', detail: 1.3, jit: .05 } });
    R.fill(P([[-40, -40], [2000, -40], [2000, 60], [-40, 190]]), { c: '#0a0806', h: { th: -.07, id: 0 }, p: { dir: -4, maxR: 30, group: 'tavan' } });           // eğik tavan
    R.fill(P([[-40, 190], [2000, 60], [2000, 84], [-40, 222]]), { c: '#1e160f', h: { th: -.07, id: 9 }, p: { dir: -4, maxR: 10, group: 'kiris' } });          // kiriş alt yüzü
    R.fill(Rc(-40, 640, 2000, 265), { c: '#120d0a', h: { th: H0, id: 0 }, p: { dir: 90, maxR: 24, group: 'lambri' } });                                    // lambri
    for (let x = 60; x < 1960; x += 230) R.fill(Rc(x, 668, 170, 210), { c: '#0e0b08', h: { th: H0, id: 0 }, p: { dir: 90, maxR: 14, group: 'pano' + x } });  // lambri panoları
    R.fill(Rc(-40, 632, 2000, 14), { c: '#30251a', h: { th: H0, id: 9 }, p: { dir: 0, maxR: 6, group: 'pervaz' } });
    R.fill(P([[-40, FLOOR], [2000, FLOOR], [2000, 1120], [-40, 1120]]), { c: '#0c0907', h: { type: 'persp', y0: FLOOR, D: 200, p0: 7, p1: 14, id: 8 }, p: { dir: 2, maxR: 30, group: 'zemin' } });
    // kitaplık (solda; okul kitapları, X. bölüm)
    R.fill(Rc(40, 250, 330, 655), { c: '#0a0806', h: { th: HV, id: 4 }, p: { dir: 90, maxR: 16, group: 'kitaplik' } });
    for (let r = 0; r < 4; r++) { const y = 290 + r * 150;
      R.fill(Rc(62, y, 286, 118), { c: '#050403', h: { th: H0, id: 4 }, p: { dir: 0, maxR: 10, group: 'raf' + r } });
      let x = 70; for (let k = 0; x < 330; k++) { const w = 14 + ((k * 37 + r * 11) % 17), hh = 78 + ((k * 23 + r * 7) % 34); if (x + w > 340) break;
        const cc = ['#1e160e', '#18130d', '#22150f', '#161611'][(k + r) % 4];
        R.fill(Rc(x, y + 118 - hh, w - 3, hh), { c: cc, h: { th: HV, id: 9 }, p: { dir: 90, maxR: 5, group: `kt${r}_${k}` } }); x += w; } }
    // masa (lambanın altı)
    R.fill(P([[790, 735], [1030, 735], [1022, 752], [798, 752]]), { c: '#3c2a1a', h: { th: H0, id: 9 }, p: { dir: 0, maxR: 6, group: 'masa' } });
    R.fill(Rc(808, 752, 14, 153), { c: '#22180f', h: { th: HV, id: 9 }, p: { dir: 90, maxR: 5, group: 'ayak1' } });
    R.fill(Rc(998, 752, 14, 153), { c: '#22180f', h: { th: HV, id: 9 }, p: { dir: 90, maxR: 5, group: 'ayak2' } });
    // lamba gövdesi (pirinç gövde + cam şişe)
    R.fill(S([[868, 735], [942, 735], [936, 712], [918, 700], [922, 676], [888, 676], [892, 700], [874, 712]]), { c: '#8a6a32', h: { type: 'rad', cx: 905, cy: 712, id: 9 }, p: { dir: 'edge', maxR: 6, group: 'lamba' } });
    R.fill(S([[884, 676], [926, 676], [934, 650], [922, 612], [888, 612], [876, 650]]), { c: '#e9cf8e', ton: .9, h: { th: HV, id: 7 }, p: { dir: 90, maxR: 5, group: 'sise' } });
  },
  // lamba ışığı: ışık kaynağı çevresinde aydınlatma (gravürde ton katmanına "screen", impastoda referansa)
  light: { x: LAMP.x, y: LAMP.y, r0: 20, r1: 640, col: 'rgba(255,196,110,', a: .62 } };

  // 2) PORTRE (durağan, çerçevede). Basil'in "olağanüstü güzellikteki genç adam"ı (I. bölüm); burada çökmüş hâli (XX. bölüm).
  //    Yüz ¾, lamba solda aşağıdan aydınlatır. `curu` 0 genç, 1 çökmüş: yalnız renk ve birkaç biçim değişir (aynı parça sırası).
  function portre(R, curu) {
    const k = curu, mix = (a, b) => { const A = parseInt(a.slice(1), 16), B = parseInt(b.slice(1), 16);
      const r = (A >> 16 & 255) + ((B >> 16 & 255) - (A >> 16 & 255)) * k, gg = (A >> 8 & 255) + ((B >> 8 & 255) - (A >> 8 & 255)) * k, bb = (A & 255) + ((B & 255) - (A & 255)) * k;
      return '#' + [r, gg, bb].map(v => Math.round(v).toString(16).padStart(2, '0')).join(''); };
    const ix = IN.x, iy = IN.y, iw = IN.w, ih = IN.h, cx = ix + iw * .52, hy = iy + 230;
    // çerçeve (altın varak): dış kenar, iç oluk
    R.fill(Rc(FR.x, FR.y, FR.w, FR.h), { c: '#7a5c26', ton: .34, h: { th: HV, id: 9 }, p: { dir: 'edge', maxR: 7, group: 'cerceve', hgt: 1.5 } });
    R.fill(Rc(FR.x + 14, FR.y + 14, FR.w - 28, FR.h - 28), { c: '#3a2a10', ton: .12, h: { th: HV, id: 9 }, p: { dir: 'edge', maxR: 5, group: 'oluk' } });
    R.line(Rc(FR.x + 34, FR.y + 34, FR.w - 68, FR.h - 68), '#d8b060', 7, { ton: .9, h: { th: HV, id: 9 }, p: { maxR: 3, group: 'yaldiz', hgt: 1.5 } });
    // tuval zemini: koyu sıcak kahve; ışık sol üstten (resmin içindeki ışık)
    R.fill(Rc(ix, iy, iw, ih), { c: mix('#4a3320', '#2c2a1c'), h: { th: HD, id: 0 }, p: { dir: 30, maxR: 22, group: 'tuval', detail: 1.2 } });
    // gövde: koyu redingot, beyaz yaka ve kravat
    R.fill(S([[cx - 175, iy + ih + 10], [cx - 160, hy + 190], [cx - 92, hy + 128], [cx - 30, hy + 112], [cx + 50, hy + 116], [cx + 122, hy + 140], [cx + 168, hy + 200], [cx + 185, iy + ih + 10]]),
      { c: mix('#16120f', '#121410'), h: { th: HV - .2, id: 9 }, p: { dir: 70, maxR: 12, group: 'ceket' } });
    R.fill(P([[cx - 34, hy + 112], [cx + 40, hy + 114], [cx + 18, hy + 230], [cx - 6, hy + 236]]), { c: mix('#ece2cc', '#b8b29a'), ton: .92, h: { th: HV, id: 5 }, p: { dir: 90, maxR: 5, group: 'yaka' } });
    R.fill(P([[cx - 14, hy + 120], [cx + 22, hy + 121], [cx + 10, hy + 190], [cx - 2, hy + 192]]), { c: mix('#2a1c2c', '#201a1a'), h: { th: HV, id: 9 }, p: { dir: 90, maxR: 4, group: 'kravat' } });
    // boyun
    R.fill(P([[cx - 30, hy + 62], [cx + 22, hy + 66], [cx + 26, hy + 118], [cx - 30, hy + 116]]), { c: mix('#b8875e', '#6e6a4e'), h: { th: HD, id: 5 }, p: { dir: 80, maxR: 5, group: 'boyun' } });
    // baş (¾, izleyicinin soluna bakar): yüz düzlemi (ışıkta) + gölge düzlemi
    const cave = k * 9;
    const yuz = [[cx - 62, hy - 70], [cx - 66, hy - 10], [cx - 58 + cave * .4, hy + 30], [cx - 40, hy + 66], [cx - 8, hy + 84], [cx + 30, hy + 72], [cx + 54, hy + 30], [cx + 60, hy - 30], [cx + 50, hy - 92], [cx - 10, hy - 110], [cx - 50, hy - 100]];
    R.fill(S(yuz), { c: mix('#e4b98d', '#9c9a74'), ton: .86 - .2 * k, h: { th: HD, id: 5 }, p: { dir: 'edge', maxR: 6, group: 'yuz', detail: .8 } });
    R.fill(S([[cx + 12, hy - 96], [cx + 50, hy - 92], [cx + 60, hy - 30], [cx + 54, hy + 30], [cx + 30, hy + 72], [cx + 8, hy + 82], [cx + 20, hy + 20], [cx + 22, hy - 40]]),
      { c: mix('#a8754f', '#5c5a42'), ton: .5 - .2 * k, h: { th: HD, id: 5 }, p: { dir: 'edge', maxR: 5, group: 'yuz' } });                                            // gölge yanağı (aynı grup: yumuşak kenar)
    // saç: genç = gür, koyu altın; çökmüş = seyrek, gri
    R.fill(S([[cx - 70, hy - 52], [cx - 74, hy - 104], [cx - 40, hy - 136], [cx + 14, hy - 140], [cx + 58, hy - 118], [cx + 70, hy - 70], [cx + 60, hy - 40], [cx + 46, hy - 84], [cx + 4, hy - 100 + 10 * k], [cx - 40, hy - 90 + 12 * k], [cx - 58, hy - 60]]),
      { c: mix('#7a5a2a', '#6a665c'), h: { type: 'bend', ox: cx - 60, oy: hy - 120, a: .3, k: .004, id: 6 }, p: { dir: 'edge', maxR: 6, group: 'sac' } });
    // göz çukurları, gözler (çökmüşte derin ve kısık: "sinsilik bakışı")
    const ey = hy - 26, gz = 1 + .5 * k;
    R.fill(Ell(cx - 30, ey, 15 * gz, 9 * gz, -.1), { c: mix('#8a5a3c', '#3a3424'), h: { th: HD, id: 5 }, p: { maxR: 3, group: 'cukur1' } });
    R.fill(Ell(cx + 22, ey + 2, 12 * gz, 8 * gz, .1), { c: mix('#6a442c', '#2c281c'), h: { th: HD, id: 5 }, p: { maxR: 3, group: 'cukur2' } });
    R.fill(Ell(cx - 30, ey + 1, 8, 4.5 - 2 * k, -.1), { c: mix('#2a2a3a', '#14140c'), h: { th: H0, id: 5 }, p: { maxR: 2, group: 'goz1' } });
    R.fill(Ell(cx + 22, ey + 3, 6.5, 4 - 1.8 * k, .1), { c: mix('#2a2a3a', '#14140c'), h: { th: H0, id: 5 }, p: { maxR: 2, group: 'goz2' } });
    // kaş (çökmüşte iç uç aşağı)
    R.line(c => { c.moveTo(cx - 50, ey - 20 + 4 * k); c.quadraticCurveTo(cx - 32, ey - 30, cx - 12, ey - 22 - 6 * k); }, mix('#4a3418', '#3a382c'), 6, { h: { th: H0, id: 5 }, p: { maxR: 2, group: 'kas1' } });
    R.line(c => { c.moveTo(cx + 8, ey - 22 - 6 * k); c.quadraticCurveTo(cx + 26, ey - 28, cx + 40, ey - 18); }, mix('#3a2a14', '#2c2a20'), 5, { h: { th: H0, id: 5 }, p: { maxR: 2, group: 'kas2' } });
    // burun gölgesi
    R.fill(P([[cx - 6, ey + 4], [cx + 6, ey + 40], [cx - 10, ey + 50], [cx - 20, ey + 46]]), { c: mix('#9a6844', '#4c4834'), h: { th: HD, id: 5 }, p: { maxR: 3, group: 'burun' } });
    // ağız: genç = düz, dolgun; çökmüş = "ikiyüzlülüğün kıvrık çizgisi" (bir uç yukarı)
    R.line(c => { c.moveTo(cx - 28, hy + 46 + 4 * k); c.quadraticCurveTo(cx - 6, hy + 50 - 2 * k, cx + 18, hy + 44 - 12 * k); }, mix('#7a3a2a', '#2a2018'), 5, { h: { th: H0, id: 5 }, p: { maxR: 2, group: 'agiz' } });
    // çökmüş yüzün kırışıkları ve çökük yanak (genç hâlde yüz renginde, görünmez)
    if (k > 0) {
      R.line(c => { c.moveTo(cx - 52, hy + 4); c.quadraticCurveTo(cx - 40, hy + 40, cx - 24, hy + 60); }, mix('#e4b98d', '#3e3a28'), 4, { h: { th: H0, id: 5 }, p: { maxR: 2, group: 'kir1' } });
      R.line(c => { c.moveTo(cx - 22, ey + 18); c.quadraticCurveTo(cx - 34, ey + 30, cx - 44, ey + 30); }, mix('#e4b98d', '#4a4630'), 3, { h: { th: H0, id: 5 }, p: { maxR: 2, group: 'kir2' } });
      R.line(c => { c.moveTo(cx - 44, ey - 40); c.lineTo(cx + 10, ey - 44); }, mix('#e4b98d', '#5a5640'), 3, { h: { th: H0, id: 5 }, p: { maxR: 2, group: 'kir3' } });
      R.fill(S([[cx - 56, hy + 6], [cx - 44, hy - 4], [cx - 36, hy + 26], [cx - 46, hy + 44]]), { c: mix('#e4b98d', '#6c6a4c'), h: { th: HD, id: 5 }, p: { maxR: 4, group: 'yanak' } });
    }
  }
  LEV.portre = { draw(R) { portre(R, 1); } };
  LEV.portreGenc = { draw(R) { portre(R, 0); } };

  // 3) ÖRTÜ: mor saten, altın işleme kenarı, dikey kıvrımlar. Yerel koordinat: sol üst (0,0), 540×760.
  const OW = 540, OH = 760;
  LEV.ortu = { draw(R) {
    R.fill(P([[0, 0], [OW, 0], [OW + 6, OH], [-8, OH]]), { c: '#4e2552', h: { th: HV, id: 9 }, p: { dir: 90, maxR: 18, group: 'ortu', detail: 1.2 } });
    // kıvrımlar: koyu ve açık şeritler (aynı grup içinde)
    for (let i = 0; i < 7; i++) { const x = 40 + i * 74 + (i % 2) * 12, w = 22 + (i % 3) * 9;
      R.fill(S([[x, 0], [x + w, 0], [x + w + 10, OH * .5], [x + w + 18, OH], [x - 4, OH], [x + 4, OH * .5]]), { c: i % 2 ? '#2c1230' : '#6e3a72', h: { th: HV, id: 9 }, p: { dir: 90, maxR: 8, group: 'ortu' } }); }
    // altın işlemeli kenar (alt ve yanlar)
    R.fill(P([[-8, OH - 46], [OW + 6, OH - 46], [OW + 6, OH], [-8, OH]]), { c: '#a88438', ton: .62, h: { th: H0, id: 9 }, p: { dir: 0, maxR: 6, group: 'isleme', hgt: 1.4 } });
    for (let x = 6; x < OW; x += 34) R.fill(Ell(x + 10, OH - 23, 9, 9), { c: '#5e3a14', h: { th: H0, id: 9 }, p: { maxR: 3, group: 'motif' + x } });
    R.fill(P([[0, 0], [22, 0], [14, OH - 46], [-8, OH - 46]]), { c: '#a88438', ton: .62, h: { th: HV, id: 9 }, p: { dir: 90, maxR: 5, group: 'isleme2' } });
  } };

  // 4) DORIAN: sırtı dönük ¾, redingot. Yerel koordinat: ayak tabanı orta (0,0), boy ~760 px, yüzü sağa (portreye).
  LEV.dorian = { draw(R) {
    const sil = '#0e0b09', kenar = '#4a3a2a';
    // pantolon ve ayakkabılar
    R.fill(P([[-62, -330], [-8, -330], [-14, -8], [-52, -8]]), { c: '#120e0b', h: { th: HV, id: 9 }, p: { dir: 90, maxR: 10, group: 'bacak1' } });
    R.fill(P([[2, -330], [56, -330], [62, -6], [22, -8]]), { c: '#0f0c0a', h: { th: HV, id: 9 }, p: { dir: 90, maxR: 10, group: 'bacak2' } });
    R.fill(S([[-60, -14], [-6, -14], [4, 0], [-62, 2]]), { c: '#060504', h: { th: H0, id: 9 }, p: { maxR: 5, group: 'ayak1' } });
    R.fill(S([[18, -12], [70, -12], [90, 2], [18, 2]]), { c: '#060504', h: { th: H0, id: 9 }, p: { maxR: 5, group: 'ayak2' } });
    // redingot: omuzdan dize; omuz eğimli, bel hafif içeride, etek düz (dize kadar), arkada yırtmaç
    R.fill(S([[-70, -628], [-28, -656], [36, -656], [80, -628], [90, -560], [84, -470], [88, -380], [96, -282], [-86, -282], [-78, -380], [-72, -470], [-80, -560]]),
      { c: sil, h: { th: HV - .1, id: 9 }, p: { dir: 92, maxR: 14, group: 'ceket' } });
    R.line(c => { c.moveTo(4, -440); c.lineTo(6, -284); }, '#000000', 4, { h: { th: HV, id: 9 }, p: { maxR: 2, group: 'ceket' } });                       // yırtmaç
    // lamba ışığının vurduğu sağ kenar (ince açık şerit)
    R.fill(S([[78, -626], [90, -560], [84, -470], [88, -380], [96, -284], [86, -284], [78, -380], [74, -470], [80, -560], [70, -620]]), { c: kenar, ton: .4, h: { th: HV, id: 9 }, p: { dir: 92, maxR: 4, group: 'ceket' } });
    // dik yaka (Viktorya), ense
    R.fill(S([[-24, -676], [30, -676], [36, -650], [-28, -650]]), { c: '#cfc4ae', ton: .88, h: { th: H0, id: 5 }, p: { maxR: 3, group: 'yaka' } });
    R.fill(P([[-16, -704], [26, -704], [28, -674], [-18, -674]]), { c: '#7a5a40', ton: .3, h: { th: HV, id: 5 }, p: { maxR: 3, group: 'ense' } });
    // baş (arkadan ¾, sağa dönük): kafatası + saç kütlesi; sağda kulak ve yanak kenarı ışıkta
    R.fill(S([[-30, -704], [-38, -744], [-30, -786], [2, -808], [38, -804], [60, -776], [62, -738], [52, -708], [24, -698]]), { c: '#1a130d', h: { th: .9, id: 6 }, p: { dir: 'edge', maxR: 5, group: 'bas' } });
    R.fill(S([[54, -748], [64, -740], [62, -716], [52, -706], [48, -728]]), { c: '#b08058', ton: .62, h: { th: HV, id: 5 }, p: { maxR: 3, group: 'yanak' } });
    R.fill(Ell(46, -734, 7, 12, .1), { c: '#6a4a30', ton: .3, h: { th: HV, id: 5 }, p: { maxR: 2, group: 'kulak' } });
    // sol kol (sarkık, ön yüzde koyu)
    R.fill(S([[-74, -612], [-92, -520], [-96, -420], [-84, -390], [-66, -396], [-66, -500], [-58, -590]]), { c: '#0a0807', h: { th: HV, id: 9 }, p: { dir: 90, maxR: 8, group: 'kol1' } });
  } };
  // 5) DORIAN'IN SAĞ KOLU (örtüyü çeken): yerel koordinat omuz (0,0), kol +x yönünde 300 px.
  LEV.kol = { draw(R) {
    R.fill(S([[-10, -22], [120, -24], [210, -16], [290, -14], [298, 10], [210, 14], [120, 22], [-12, 26]]), { c: '#0d0a08', h: { th: H0, id: 9 }, p: { dir: 0, maxR: 8, group: 'kol' } });
    R.fill(S([[120, -24], [210, -16], [290, -14], [292, -6], [210, -8], [120, -14]]), { c: '#4a3a2a', ton: .42, h: { th: H0, id: 9 }, p: { dir: 0, maxR: 3, group: 'kol' } });
    R.fill(P([[288, -14], [302, -16], [304, 12], [288, 12]]), { c: '#cfc4ae', ton: .86, h: { th: HV, id: 5 }, p: { maxR: 3, group: 'manset' } });
    R.fill(S([[302, -12], [336, -16], [352, -4], [344, 14], [304, 12]]), { c: '#c08a62', ton: .62, h: { th: HD, id: 5 }, p: { maxR: 3, group: 'el' } });
  } };

  // ── zaman çizelgesi (8,0 sn; deneme sahnesi, anlatımsız) ──
  const DUR = 8.0;
  // Dorian'ın ayak noktası ve hafif salınım (soluk alış)
  const dorianT = t => ({ x: 700 + 6 * Math.sin(t * 1.1), y: FLOOR + 92, a: .006 * Math.sin(t * 1.3), k: 1.0 });
  // kol: 0–2,4 sn uzanır (omuzdan örtünün sol üst köşesine), 2,4–4,2 çeker (aşağı), sonra iner
  const kolT = t => { const d = dorianT(t), sx = d.x + 70, sy = d.y - 600;
    const uz = io3(seg(t, .3, 2.4)), cek = io3(seg(t, 2.5, 4.0)), in_ = io3(seg(t, 4.6, 6.2));
    // açı (0 = sağa, + = aşağı): dinlenme 1,25 → örtünün sol kenarına uzanma −0,05 → çekerken 0,47 (el çerçeve kenarında) → bırakıp dinlenme 1,25
    const a = 1.25 - 1.30 * uz + .52 * cek + .78 * in_;
    return { x: sx, y: sy, a, k: .96 + .04 * uz }; };
  // örtü: 2,5–4,4 sn aşağı kayar (ivmelenerek), hafif döner
  const ortuT = t => { const p = in2(seg(t, 2.55, 4.4)); return { x: FR.x - 20 + 40 * p, y: FR.y - 20 + 820 * p, a: .06 * p, k: 1 }; };
  // kamera: yavaş yaklaşma (yakınlık ≤ %6, 8 sn), odak portreye kayar
  const cam = t => { const p = io3(seg(t, 0, 8)); return { cx: 1040 + 110 * p, cy: 520 - 10 * p, z: 1.0 + .06 * p }; };
  const alev = t => ({ x: LAMP.x, y: LAMP.y, s: 1 + .12 * Math.sin(t * 9.1) + .07 * Math.sin(t * 15.7 + 1.3), lean: .08 * Math.sin(t * 3.7) });

  // levha sırası (arkadan öne)
  const SIRA = [['oda', null], ['portre', null], ['ortu', ortuT], ['dorian', dorianT], ['kol', kolT]];
  g.SAHNE = { LEV, SIRA, DUR, FR, IN, LAMP, FLOOR, cam, alev, lum, seg, ss, io3, P, S, Ell, Rc, ortuT, OW, OH };
})(window);
