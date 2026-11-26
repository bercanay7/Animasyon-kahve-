// II. Altı gün (C01–C13): P21–P40. Bodrum yalnız monitörde (VID); belgeler ve oturma odası kâğıtta (KAG).
// a.js'in VID, KAG, NUM, bodrum(), yakinFig() yardımcılarını kullanır. Yeni üst düzey ad yok (her şey bu kapanışın içinde).
// Hassasiyet: şınav yandan ve tek mahkûm; tuvalet yürüyüşünde baş torbası çizilmez; parmaklıkta yalnız dikey çubuk ve kenardan kenara kuşak;
//   tabakta tek kenar çizgisi (halka yok); dokuz gardiyan farklı boy, duruş ve aralıkta (mezar taşı sırası okunmasın); kimse ışığın altında oturmaz.
(() => {
  'use strict';
  const T = (B, d) => B.ton(d);
  const ink = SET.ink;
  const tam = (B, d) => { const k = B.k; k.save(); k.fillStyle = T(B, d); k.fillRect(-900, -900, W + 1800, H + 1800); k.restore(); };
  const yer = (B, y, d) => { const k = B.k; k.save(); k.fillStyle = T(B, d); k.fillRect(-900, y, W + 1800, H + 900); k.restore(); };
  // çapa zamanı (film) ve plan içi zaman
  const tA = at => A(at);
  const yerel = (st, at) => A(at) - st.at;
  // yürüyüş için go(t): [a, b] aralıklarında yürür (plan içi sn), arada durur; geçişler yumuşak
  const yuruAra = (araliklar, yum = .35) => tl => { let v = 0; for (const [a, b] of araliklar) v = Math.max(v, Math.min(inv(a - yum, a, tl), 1 - inv(b - yum, b, tl))); return v; };
  // opak dolgu: ton plakası beyaz + çizgi plakası gri (video = ton × çizgi; yalnız çizgi plakasına açık boya arkadakini gösterir)
  const dol = (B, yol, renk) => { const k = B.k, l = B.l; k.save(); k.fillStyle = '#fff'; k.beginPath(); yol(k); k.fill(); k.restore(); l.save(); l.fillStyle = renk; l.beginPath(); yol(l); l.fill(); l.restore(); };
  // arka dolgulu figür: önlük çizgi plakasında açık gri; ton plakası figürün biçiminde beyazlanmazsa duvar ve kapı önlüğün içinden görünür (hayalet okuması)
  const BEYAZ = { renk: '#fff', onlukRenk: '#fff', camRenk: '#fff', parilti: '#fff', sandalyeRenk: '#fff' };
  const kisiD = (B, x, y, boy, o) => { FIG.kisi(B.k, x, y, boy, { ...o, ...BEYAZ }); return FIG.kisi(B.l, x, y, boy, o); };
  const yuruD = (B, x, y, boy, t, o) => { SET.yuru(B.k, x, y, boy, t, { ...o, ...BEYAZ }); return SET.yuru(B.l, x, y, boy, t, o); };
  // sayım sırası (a.js bodrum() o.sayim ile aynı dizilim ve tohum; arka dolgulu)
  function sayimD(B, st, K, n, o = {}) {
    const r = rng(17), t = st.t;
    for (let i = 0; i < n; i++) {
      const z = .18 + i * .088 + (r() - .5) * .05, u = -.74 + (r() - .5) * .12, poz = r(), p = K.yer(z, u), s = K.olc(z);
      const boyK = .9 + r() * .18, kolA = [-.08 + r() * .2, .1 + r() * .4], bas = (r() - .5) * .14 + Math.sin(t * .7 + i) * .03 + (o.basEgik || 0), govde = (r() - .5) * .08;
      kisiD(B, p[0], p[1], 700 * s * boyK, { tip: 'mahkum', f: 1, numara: NUM[i % NUM.length], kolO: poz < .4 ? [-.05, .1] : poz < .7 ? [.25, .9] : [-.2, .35], kolA, bas, govde });
    }
  }
  // karyola (yandan; 1971 hücre yatağı). Yerel (0,0): baş ucu direğinin zemine bastığı yer, +x ayak ucu; B.k ve B.l'de dönüşüm hazır olmalı.
  // Yatak okunsun diye: baş ucunda yüksek direk, ayak ucunda alçak direk, metal yan kayıt, şilte, yastık, ayak ucunda katlı battaniye. Dolgular opak.
  function karyola(B, L, o = {}) {
    const l = B.l, h = o.h ?? 110, m = o.m ?? 46, yb = -h - m, cz = o.cz ?? 4, ub = o.bas ?? 130, ua = o.ayak ?? 50;
    l.save(); l.fillStyle = '#000'; l.fillRect(0, -h - 4, L, 14); l.restore();                                  // yan kayıt (çerçeve)
    const sil = g => g.roundRect(10, yb, L - 22, m + 2, m * .4), bat = g => g.roundRect(L * .56, yb - 10, L * .44 - 16, m + 16, 14), yas = g => g.roundRect(20, yb - 30, L * .2, 38, 16);
    const rk = o.renk || ['#A2A29B', '#5E5E58', '#E2E2DA']; dol(B, sil, rk[0]); dol(B, bat, rk[1]); if (o.yastik !== false) dol(B, yas, rk[2]);
    l.save(); ink(l, cz); for (const y of (o.yastik !== false ? [sil, bat, yas] : [sil, bat])) { l.beginPath(); y(l); l.stroke(); }
    l.lineWidth = cz * .8; l.beginPath(); l.moveTo(L * .56 + 14, yb + m * .45); l.quadraticCurveTo(L * .75, yb + m * .3, L - 30, yb + m * .5); l.stroke();   // battaniyenin katı
    l.fillStyle = '#000'; l.fillRect(-6, yb - ub, 18, -yb + ub); l.fillRect(L - 14, yb - ua, 18, -yb + ua);           // baş ve ayak direkleri (metal)
    l.beginPath(); l.arc(3, yb - ub, 13, 0, TAU); l.fill(); if (o.ayakBas !== false) { l.beginPath(); l.arc(L - 5, yb - ua, 12, 0, TAU); l.fill(); }                        // direk başlıkları
    l.restore();
  }
  // belge sayfası (kâğıt): ust başlık satırları (daktilo değil, hep tam), satirlar p ile basılır; vurgu {satır: 0..1} kehribar şerit (yalnız yazının boyu)
  //   o.ta yazı saydamlığı (1), o.gr uzak görünüm: satırların yerine gri çubuklar (0); uzaktan okunmaya çalışılan küçük yazı kalmasın
  function sayfa(B, x, y, w, ust, satirlar, p, o = {}) {
    const k = B.k, l = B.l, px = o.px || 44, lh = px * 1.5, upx = Math.round(px * .66), ta = o.ta ?? 1, gr = o.gr ?? 0;
    const ustH = ust.length ? ust.length * upx * 1.5 + px * 1.2 : 0;
    const h = o.h || (ustH + satirlar.length * lh + px * 2.4);
    k.save(); k.fillStyle = T(B, o.golge ?? .6); k.fillRect(x + 14, y + 16, w, h); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
    l.save(); ink(l, 1.6); l.strokeRect(x, y, w, h); l.textBaseline = 'middle';
    l.font = `700 ${upx}px "Courier Prime"`;
    if (ta > 0) { l.globalAlpha = ta; ust.forEach((s, i) => l.fillText(s, x + px * 1.2, y + px * 1.1 + i * upx * 1.5)); l.globalAlpha = 1; }
    if (gr > 0) { l.save(); l.globalAlpha = gr * .45; ust.forEach((s, i) => l.fillRect(x + px * 1.2, y + px * 1.1 + i * upx * 1.5 - upx * .09, l.measureText(s).width, upx * .18)); l.restore(); }
    if (ust.length) { l.lineWidth = 1.4; l.beginPath(); l.moveTo(x + px * 1.2, y + ustH - px * .35); l.lineTo(x + w - px * 1.2, y + ustH - px * .35); l.stroke(); }
    l.font = `700 ${px}px "Courier Prime"`;
    const top = satirlar.reduce((a, r) => a + r.length, 0); let kalan = Math.floor(top * clamp(p) + 1e-6);
    satirlar.forEach((r, i) => {
      const yy = y + ustH + px * 1.1 + i * lh, x0 = x + px * 1.2;
      const va = o.vurgu && o.vurgu[i];
      if (va > 0) { const tw = l.measureText(r).width; B.renkBoya(g => g.rect(x0 - 10, yy - px * .62, (tw + 20) * clamp(va), px * 1.24), .6, 0); }
      if (ta > 0) { l.globalAlpha = ta; l.fillText(r.slice(0, Math.max(0, kalan)), x0, yy); l.globalAlpha = 1; }
      if (gr > 0 && r) { l.save(); l.globalAlpha = gr * .45; l.fillRect(x0, yy - px * .1, l.measureText(r).width, px * .2); l.restore(); }
      kalan -= r.length;
    });
    l.restore();
    return { x, y, w, h };
  }
  // önden hücre kapısı (video): çerçeve, dikey çubuklar, üstte ve altta ray (ortada kuşak yok)
  function parmaklik(B, x0, x1, yt, yb, n = 7, o = {}) {
    const l = B.l; l.save(); ink(l, o.cer || 20);
    l.strokeRect(x0, yt, x1 - x0, yb - yt);
    l.lineWidth = o.cub || 11;
    for (let i = 1; i < n; i++) { const x = lerp(x0, x1, i / n); l.beginPath(); l.moveTo(x, yt); l.lineTo(x, yb); l.stroke(); }
    l.restore();
  }
  // yanlamasına şınav (tek mahkûm): ayaklar (x, y) zeminde, f baş yönü, s birim px, h 0 aşağı .. 1 yukarı
  //   iniş ve kalkış belirgin (omuz 6 → 25 birim): yere yığılmış beden okunmasın
  function sinav(B, x, y, s, h, f = 1) {
    const g = B.l, U = FIG.uzuv;
    g.save(); g.translate(x, y); g.scale(f * s, s); g.fillStyle = '#000';
    const omz = [56, -(6 + 19 * h)], ayak = [0, -1.6], kal = [24, lerp(ayak[1], omz[1], 24 / 56) - .6];
    const el = [57.5, -1.2];
    // dirsek: omuz–el arasında, ayak yönüne doğru bükük (iki kemik)
    const L1 = 15, L2 = 13.5, dx = el[0] - omz[0], dy = el[1] - omz[1], d = Math.min(Math.hypot(dx, dy), L1 + L2 - .2);
    const th = Math.atan2(dy, dx), al = Math.acos(clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1));
    const dir = [omz[0] + L1 * Math.cos(th + al), omz[1] + L1 * Math.sin(th + al)];
    U(g, ayak, kal, 5.2, 8.4);                                   // bacaklar (birleşik, yandan)
    g.beginPath(); g.moveTo(ayak[0] - 3, ayak[1] + 1.4); g.lineTo(ayak[0] + 2, ayak[1] - 4.6); g.lineTo(ayak[0] + 3, ayak[1] + 1.4); g.closePath(); g.fill();   // ayak ucu
    U(g, kal, omz, 10, 11.5);                                    // gövde
    g.save(); g.fillStyle = '#B2B2AA'; U(g, [kal[0] - 4, kal[1] + .4], [omz[0] - 3.5, omz[1] + .2], 8.2, 9.4); g.restore();   // önlük
    U(g, omz, [omz[0] + 6, omz[1] - 2.2], 5, 5.4);               // boyun
    g.beginPath(); g.ellipse(omz[0] + 9.5, omz[1] - 3.4, 6.2, 5.6, .25, 0, TAU); g.fill();   // baş (bereli; yüz yok)
    U(g, omz, dir, 4.4, 3.6); U(g, dir, el, 3.6, 2.8);           // kol: dirsekten bükük
    g.beginPath(); g.ellipse(el[0] + 1.2, el[1], 2.6, 1.3, 0, 0, TAU); g.fill();
    g.restore();
    // önlüğün ton plakası beyaz (arkadaki zemin önlüğün içinden görünmesin)
    const k = B.k; k.save(); k.translate(x, y); k.scale(f * s, s); k.fillStyle = '#fff'; U(k, [kal[0] - 4, kal[1] + .4], [omz[0] - 3.5, omz[1] + .2], 8.2, 9.4); k.restore();
  }
  // tepside tabak ve yemek (video, ayrıntı): tek kenar çizgisi; yemek düzensiz biçim
  function tabak(B, x, y, rx, ry, yemek = 1, o = {}) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .1); k.beginPath(); k.ellipse(x, y, rx, ry, 0, 0, TAU); k.fill(); k.restore();
    l.save(); ink(l, Math.max(2, rx * .02)); l.beginPath(); l.ellipse(x, y, rx, ry, 0, 0, TAU); l.stroke(); l.restore();
    if (yemek > 0) yemekCiz(B, x, y, rx, ry, o.tohum || 21);
  }
  // yemek: düzensiz biçim; kal (1 → .5) kaşık aldıkça sağ yandan yuvarlak bir kenarla çekilir (düz kesik yok)
  function yemekCiz(B, x, y, rx, ry, tohum, kal = 1) {
    const k = B.k, r = rng(tohum), pts = [], c = (1 - kal) * 1.3;
    for (let i = 0; i < 11; i++) { const a = i / 11 * TAU, q = (.52 + r() * .16) * (1 - c * (.5 + .5 * Math.cos(a))); pts.push([x + Math.cos(a) * rx * q - c * rx * .08, y - ry * .05 + Math.sin(a) * ry * q * .9]); }
    k.save(); k.fillStyle = T(B, .62); k.beginPath(); spline(k, pts, true, .9); k.fill();
    k.fillStyle = T(B, .78);
    for (let i = 0; i < 9; i++) { const dx = (r() - .5) * .8, dy = (r() - .5) * ry * .7, ex = rx * (.04 + r() * .05), ey = ry * (.04 + r() * .04), ro = r() * 3;
      if (dx < .4 - c * .8) { k.beginPath(); k.ellipse(x + dx * rx, y + dy, ex, ey, ro, 0, TAU); k.fill(); } }
    k.restore();
  }
  // hücrede battaniyeye sarınmış mahkûm: battaniye omuzlardan pelerin gibi sırta ve dize iner (belde oval ya da şeritli biçim yok: kalkan okunmasın),
  //   öndeki el göğüste kenarı tutar; o.cek (çoğu battaniyesini seçiyor) ön kenarı kapatır, el çeneye çıkar
  function battaniyeli(B, x, y, boy, o = {}) {
    const f = o.f || 1, c = o.cek || 0;
    const r = kisiD(B, x, y, boy, { tip: 'mahkum', f, numara: o.numara || '', kolO: [0, 2.4], kolA: [0, .2], bas: o.bas ?? .08, zincir: false, onlukRenk: '#8E8E88', serbest: 1 });   // kollar battaniyenin içinde
    const l = B.l, b = boy, om = r.omuz, ka = r.kalca, X = u => om[0] + f * u * b;
    const on = lerp(.075, .095, c);
    const pts = [[X(-.02), om[1] - b * .035], [X(.05), om[1] - b * .02], [X(on), om[1] + b * .06], [X(on + .005), ka[1] - b * .02], [X(.08), ka[1] + b * .16], [X(-.02), ka[1] + b * .21],
      [X(-.1), ka[1] + b * .2], [X(-.11), ka[1] - b * .05], [X(-.085), om[1] + b * .04]];
    dol(B, g => spline(g, pts, true, .85), '#9C9C94');
    l.save(); ink(l, Math.max(1.5, b * .005)); l.beginPath(); spline(l, pts, true, .85); l.stroke();
    l.lineWidth = Math.max(1, b * .0035);
    for (const u of [-.07, -.035]) { l.beginPath(); l.moveTo(X(u + .01), om[1] + b * .07); l.quadraticCurveTo(X(u - .008), ka[1], X(u), ka[1] + b * .17); l.stroke(); }   // sırtta düşey kıvrımlar
    l.fillStyle = '#000'; l.beginPath(); l.ellipse(X(on - .004), lerp(om[1] + b * .09, om[1] + b * .035, c), b * .016, b * .022, 0, 0, TAU); l.fill();   // kenarı tutan el
    l.restore();
    return r;
  }

  // ── P21 ilk gün: sayım; gardiyanlar gülüşüyor (gövde sallanır, baş hafif geri), mahkûmlar solda dizili (önlükler opak) ──
  sahne('P21', 'C01', 'koridor', 'genis', (B, st) => {
    B.cam(lerp(960, 1040, E.io2(clamp(st.lt / 4))), 560, 1.03 + st.lt * .03);
    const g = ramp(st.t, tA('C01@gülüşüyor') - .25, tA('C01@gülüşüyor') + .3);
    const gul = i => Math.sin(st.t * 10.5 + i * 2.1);
    // baş fazla geri atılınca saç kütlesi başın üstünde yumru gibi duruyordu: baş geri payı küçük, gülüş gövdede ve kolda
    const gr = (z, u, f, i, kol) => ({ z, u, f, govde: g * (-.1 + .06 * gul(i)), bas: g * (-.16 + .06 * gul(i)), kol: g ? [lerp(.15, kol[0], g), lerp(.5, kol[1] + .15 * gul(i), g)] : undefined });
    const K = bodrum(B, st, { gardiyanlar: [gr(.3, .12, -1, 0, [.36, 1.9]), gr(.34, .38, -1, 1, [.34, 1.85]), gr(.4, .2, 1, 2, [.38, 1.95])] });
    sayimD(B, st, K, 6);
  }, VID);

  // ── P22 ikinci gün sabahı: hücrede numara sökülür, yatak kapının önüne sürülür (barikat) ──
  sahne('P22', 'C01@ikinci', 'hucre', 'orta', (B, st) => {
    B.cam(960, 520, 1.04 + st.lt * .018);
    const G = 900, x0 = 470, x1 = 1450, yt = 110;
    tam(B, .5); yer(B, G, .64);
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .26); k.fillRect(x0, yt, x1 - x0, G - yt); k.fillStyle = T(B, .4); k.fillRect(x0, 760, x1 - x0, G - 760); k.restore();
    const tB = tA('C01@yataklarla'), tN = tA('C01@numaralarını'), tS = tA('C01@söküyor');
    B.save(); for (const gg of [k, l]) { gg.beginPath(); gg.rect(x0 + 6, yt, x1 - x0 - 12, G - yt + 20); gg.clip(); }
    // arkada ikinci mahkûm (bir kademe açık); ilk saniyeden başını kapıya çevirir
    FIG.kisi(B.k, 1345, 850, 560, { tip: 'mahkum', f: -1, renk: T(B, .72), onlukRenk: T(B, .42), numara: NUM[3], bas: .05 + Math.sin(st.t * .9) * .03 - .1 * ramp(st.lt, .2, 1.2) });
    // öndeki mahkûm numarasını söker
    const el = ramp(st.t, tN - .2, tN + .5), cek = ramp(st.t, tS - .05, tS + .25, E.out3);
    const kolO = cek > 0 ? [lerp(.55, .4, cek), lerp(1.75, .35, cek)] : [lerp(.1, .55, el), lerp(.3, 1.75, el)];
    const r = kisiD(B, 1080, 870, 640, { tip: 'mahkum', f: 1, onlukRenk: '#8A8A84', numara: cek > .2 ? '' : NUM[0], kolO, kolA: [-.1, .2], bas: .1 + .12 * el * (1 - cek), serbest: 1 });
    if (cek > .2) {   // sökülen numara düşer (dönerek) ve yere ters düşer: yazı yalnız düşerken (alt banda yazı inmesin)
      const tl = st.t - (tS + .1), yy = Math.min(872, r.elO[1] + 900 * tl * tl), xx = r.elO[0] + 40 * Math.min(tl, .7);
      l.save(); l.translate(xx, yy - 14); l.rotate(yy >= 872 ? .05 : Math.min(tl, .8) * 4.2); l.fillStyle = '#C6C6BE'; l.fillRect(-44, yy >= 872 ? -8 : -24, 88, yy >= 872 ? 16 : 48);
      if (yy < 780) { l.fillStyle = '#000'; l.font = '700 30px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText(NUM[0], 0, 1); }
      l.restore();
    }
    // yatak (karyola, yandan) soldan kapının dibine sürülür ve parmaklığa dayanır: barikat; iten mahkûm yatağın ardında (bir kademe açık)
    const p = ramp(st.t, tB - .1, tB + 1.1, E.out3), bx = lerp(-260, 610, p);
    const otur = clamp((st.t - tB - 1.1) / .5), sars = Math.sin(otur * PI * 3) * (1 - otur) * .012;
    FIG.kisi(B.k, bx - 70, 862, 560, { tip: 'mahkum', f: 1, renk: T(B, .72), onlukRenk: T(B, .42), govde: .3 * (1 - otur * .6), kolO: [1.05, .55], kolA: [.95, .65], zincir: false, serbest: 1 });
    for (const gg of [k, l]) { gg.save(); gg.translate(bx, 892); gg.rotate(sars); }
    karyola(B, 640, { h: 150, m: 60, bas: 170, ayak: 70, cz: 6, renk: ['#77776F', '#3E3E3A', '#D6D6CE'] });
    for (const gg of [k, l]) gg.restore();
    B.restore();
    parmaklik(B, x0, x1, yt, G, 8);
  }, VID);

  // ── P23 söndürücü: gardiyan arka elinde tüpü taşır, ön elindeki hortumu kapıya doğrultur; bulut koridoru doldurur ──
  sahne('P23', 'C02', 'koridor', 'genis', (B, st) => {
    B.cam(960, 520, 1.03 + st.lt * .03);
    const K = bodrum(B, st, {});
    const tS = tA('C02@söndürücüyle'), kalk = ramp(st.t, st.at, tS, E.io2);
    FIG.kisi(B.l, ...K.yer(.46, -.35), 700 * .54, { tip: 'gardiyan', f: 1, kolO: [.25, .4], kolA: [-.1, .2], bas: .05 });
    const p0 = K.yer(.27, -.1), r = FIG.kisi(B.l, p0[0], p0[1], 700 * .73, { tip: 'gardiyan', f: 1, kolO: [lerp(.3, 1.05, kalk), lerp(.4, .55, kalk)], kolA: [.42, .3], bas: .08, serbest: 1 });
    const l = B.l, s = r.s, e = r.elO, a2 = r.elA;
    const kp = K.kapilar.find(q => q.yan > 0 && q.i === 0) || K.kapilar[0];
    const hx = (kp.a[0] + kp.b[0] + kp.c[0] + kp.d[0]) / 4, hy = (kp.a[1] + kp.b[1] + kp.c[1] + kp.d[1]) / 4;
    const a = Math.atan2(hy - e[1], hx - e[0]), nx = e[0] + Math.cos(a) * 7 * s, ny = e[1] + Math.sin(a) * 7 * s;
    // tüp: tutamaktan sarkan, bacaktan geniş, yuvarlak omuzlu silindir; üstte valf ve tetik kolu; ortada açık etiket kuşağı (yalnız yatay)
    const cx = a2[0] + 4 * s, cy = a2[1] + 1.5 * s;
    l.save(); l.fillStyle = '#000';
    l.beginPath(); l.roundRect(cx - 6 * s, cy, 12 * s, 31 * s, [5 * s, 5 * s, 1.6 * s, 1.6 * s]); l.fill();
    l.fillRect(cx - 1.6 * s, cy - 4.5 * s, 3.2 * s, 5 * s); l.lineWidth = 1.6 * s; l.lineCap = 'round'; l.strokeStyle = '#000';
    l.beginPath(); l.moveTo(cx - 1.4 * s, cy - 4.2 * s); l.lineTo(cx - 7.5 * s, cy - 2.6 * s); l.stroke();   // tetik kolu (tutamak)
    // hortum: valften aşağı sarkar, kıvrılıp ön eldeki ağza gider
    l.lineWidth = 1.5 * s; l.beginPath(); l.moveTo(cx + 1.4 * s, cy - 3.6 * s); l.bezierCurveTo(cx + 9 * s, cy + 2 * s, cx + 8 * s, cy + 22 * s, (cx + e[0]) / 2 + 6 * s, (cy + 20 * s + e[1]) / 2 + 8 * s); l.quadraticCurveTo(e[0] - 2 * s, e[1] + 6 * s, e[0], e[1]); l.stroke();
    // ağız: elde koni biçimli huni
    l.beginPath(); const px_ = -Math.sin(a), py_ = Math.cos(a);
    l.moveTo(e[0] + px_ * .9 * s, e[1] + py_ * .9 * s); l.lineTo(nx + px_ * 2.6 * s, ny + py_ * 2.6 * s); l.lineTo(nx - px_ * 2.6 * s, ny - py_ * 2.6 * s); l.lineTo(e[0] - px_ * .9 * s, e[1] - py_ * .9 * s); l.closePath(); l.fill();
    l.restore();
    dol(B, g => g.rect(cx - 6 * s, cy + 13 * s, 12 * s, 3.4 * s), '#B4B4AC');
    const pb = ramp(st.t, tS, tS + 1.8, E.out3); if (pb > 0) SET.bulut(B, nx, ny, a, pb, st.t);
  }, VID);

  // ── P24 iki gardiyan bir karyolayı koridora taşır; "dışarı"da arkadaki ucu bırakır, karyolanın ayağı yerde sürünür ──
  sahne('P24', 'C02@yatakları', 'koridor', 'orta', (B, st) => {
    B.cam(980 + st.lt * 20, 600, 1.16 + st.lt * .015);
    bodrum(B, st, { levha: false });
    const tl = st.lt, tD = tA('C02@dışarı'), bir = ramp(st.t, tD - .1, tD + .45, E.in2), h = 100;
    const on = SET.yuru(B.l, 900, 1010, 610, tl, { tip: 'gardiyan', f: 1, kolO: [-.45, .1], kolA: [-.5, .1], bas: .06, govde: .08 });
    const ar = SET.yuru(B.l, 210, 1012, 600, tl, { tip: 'gardiyan', f: 1, kolO: [lerp(.95, .15, bir), lerp(.5, .3, bir)], kolA: [lerp(.85, -.1, bir), lerp(.6, .2, bir)], bas: .1, govde: .1 * (1 - bir), serbest: 1 });
    // karyola eller hizasında, ayakları aşağıda (sedye değil: baş direği, yastık, battaniye); bırakılınca baş ucu ayağı yere değer
    const p1 = [on.elA[0] + 10, on.elA[1] + 4], p0 = [ar.elO[0] - 20, lerp(ar.elO[1], 1012 - h, bir)];
    const L = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]), ang = Math.atan2(p1[1] - p0[1], p1[0] - p0[0]);
    const k = B.k, l = B.l;
    for (const g of [k, l]) { g.save(); g.translate(p0[0], p0[1]); g.rotate(ang); g.translate(0, h); }
    karyola(B, L, { h, m: 40, bas: 120, ayak: 22, ayakBas: false, cz: 4, yastik: false });   // yastıksız: sedye/ceset okunmasın
    for (const g of [k, l]) g.restore();
    // öndeki gardiyanın eli karyolanın ayak direğinde (çizgi plakasında tekrar: direğin önünde)
    l.save(); l.fillStyle = '#000'; l.beginPath(); l.ellipse(on.elA[0], on.elA[1], 13, 9, 0, 0, TAU); l.fill(); l.restore();
  }, { ...VID, mb: 4 });

  // ── P25 karanlık dolap: içeriden darbeler, "bağırmaya"da sarsıntı; gardiyanın kolu kadraj dışından gelir, "çıkarılıyor"da kapıyı açar, mahkûm çıkarılır ──
  sahne('P25', 'C03', 'dolap', 'yakin', (B, st) => {
    B.cam(960, 540, 1.05 + st.lt * .02);
    const x0 = 560, w = 700, y0 = 90, y1 = 990, xR = x0 + w, ym = (y0 + y1) / 2;
    tam(B, .4); yer(B, y1, .6);
    const tB = tA('C03@bağırmaya'), tC = tA('C03@çıkarılıyor');
    const darbe = [.15, .95, 1.6].reduce((a_, a) => { const u = st.lt - a; return a_ + (u > 0 && u < .4 ? (1 - u / .4) * 8 : 0); }, 0);
    const amp = 1 + darbe + 10 * ramp(st.t, tB - .1, tB + .3) * (1 - ramp(st.t, tC - .9, tC - .5));
    const sh = amp * Math.sin(st.t * 43) * (.6 + .4 * Math.sin(st.t * 7.3));
    const ac = ramp(st.t, tC - .1, tC + .45, E.out3), k = B.k, l = B.l;
    // kasa
    l.save(); ink(l, 14); l.strokeRect(x0 - 20, y0 - 20, w + 40, y1 - y0 + 20); l.restore();
    let topX;
    if (ac <= 0) {
      k.save(); k.fillStyle = T(B, .74); k.fillRect(x0 + sh, y0, w, y1 - y0); k.restore();
      l.save(); ink(l, 6); l.strokeRect(x0 + sh, y0, w, y1 - y0); l.strokeRect(x0 + 60 + sh, y0 + 70, w - 120, 300); l.strokeRect(x0 + 60 + sh, y0 + 470, w - 120, 360); l.beginPath(); l.arc(x0 + 70 + sh, ym, 18, 0, TAU); l.fill(); l.restore();
      k.save(); k.fillStyle = T(B, .9); k.fillRect(x0 + sh, y1 - 8, w, 8); k.restore();
      topX = x0 + 70 + sh;
    } else {
      // açık: içerisi karanlık, koridorun ışığı kama gibi içeri düşer
      k.save(); k.fillStyle = T(B, .86); k.fillRect(x0, y0, w, y1 - y0);
      k.fillStyle = T(B, .55); k.beginPath(); k.moveTo(xR, y1); k.lineTo(lerp(xR, x0, .9 * ac), y1); k.lineTo(lerp(xR, x0, .5 * ac), y0 + 260); k.lineTo(xR, y0 + 120); k.closePath(); k.fill(); k.restore();
      // kanat: menteşe sağda, sol kenar izleyiciye doğru açılır (görünüşte sağa kayar, büyür)
      const xl = lerp(x0, xR - 90, ac), dy = 70 * ac;
      k.save(); k.fillStyle = T(B, .66); k.beginPath(); k.moveTo(xl, y0 - dy); k.lineTo(xR, y0); k.lineTo(xR, y1); k.lineTo(xl, y1 + dy); k.closePath(); k.fill(); k.restore();
      l.save(); ink(l, 6); l.beginPath(); l.moveTo(xl, y0 - dy); l.lineTo(xR, y0); l.lineTo(xR, y1); l.lineTo(xl, y1 + dy); l.closePath(); l.stroke(); l.beginPath(); l.arc(xl + 70 * (1 - ac * .6), ym, 18, 0, TAU); l.fill(); l.restore();
      topX = xl + 70 * (1 - ac * .6);
      // mahkûm dışarı alınır: başı eğik, sola yürür (önlük opak)
      const tl = st.t - (tC + .15);
      if (tl > -.2) yuruD(B, 1050, 1000, 860, Math.max(0, tl), { tip: 'mahkum', f: -1, numara: NUM[7], bas: .3, govde: .12, kolO: [.15, .3], kolA: [.2, .4], go: t => clamp(t / .25) });
    }
    // gardiyan kadrajın sol kenarında durur (gövde, gözlük; kopuk kol yok); "çıkarılıyor"dan az önce kolunu uzatıp tokmağı tutar, kapıyı çeker, sonra bırakır
    const gx = 250, gy = 1580, gb = 1500, gs = gb / 100, sp = [gx + gs, gy - 79 * gs];
    const uz = ramp(st.t, tC - 1.1, tC - .35, E.io2) * (1 - ramp(st.t, tC - .1, tC + .5, E.io2));
    const L1 = 16, L2 = 14.5, tx = (x0 + 70 - sp[0]) / gs, ty = (ym + 4 - sp[1]) / gs, Dd = Math.min(Math.hypot(tx, ty), L1 + L2 - .3);
    const phi = Math.atan2(tx, ty), alf = Math.acos(clamp((L1 * L1 + Dd * Dd - L2 * L2) / (2 * L1 * Dd), -1, 1)), bet = Math.acos(clamp((L1 * L1 + L2 * L2 - Dd * Dd) / (2 * L1 * L2), -1, 1));
    const kolO = [lerp(.12, phi - alf, uz), lerp(.3, PI - bet, uz)];
    FIG.kisi(B.l, gx, gy, gb, { tip: 'gardiyan', f: 1, kolO, kolA: [-.08, .2], bas: .1 - .06 * uz + Math.sin(st.t * .7) * .015, serbest: 1 });
  }, VID);

  // ── P26 duvar saati: altıdan ikiye döner; vardiya gölgeleri duvardan geçer ──
  sahne('P26', 'C04', 'saat', 'ayrinti', (B, st) => {
    B.cam(960, 520, 1.06 + st.lt * .022);
    tam(B, .42);
    const k = B.k; k.save(); k.fillStyle = T(B, .5); for (let i = 0; i < 5; i++) k.fillRect(-300 + i * 640, -300, 12, 1700); k.restore();   // duvar panoları (dikey)
    // gölgeler (saatin arkasında, duvarda): "tek"te biri sağa, "ikiye"de öteki sola
    const g1 = st.t - tA('C04@tek#1'), g2 = st.t - tA('C04@ikiye');
    if (g1 > 0 && g1 < 6) SET.yuru(B.k, -560, 1480, 1500, g1, { tip: 'gardiyan', f: 1, renk: T(B, .64), camRenk: T(B, .64), parilti: T(B, .64), onlukRenk: T(B, .64) });
    if (g2 > 0) SET.yuru(B.k, 2400, 1480, 1500, g2, { tip: 'gardiyan', f: -1, renk: T(B, .64), camRenk: T(B, .64), parilti: T(B, .64) });
    const p = ramp(st.t, tA('C04@altıdan') - .1, tA('C04@ikiye') + .4, E.io2), saat = 18 + 8 * p;
    SET.saat(B, 960, 520, 330, Math.floor(saat), (saat % 1) * 60);
    // saniye kolu: her saniye bir çentik (dönüşte hızlı süpürür)
    const sa = p > 0 && p < 1 ? (st.t * 6) % 1 : Math.floor(st.lt) / 60, l = B.l;
    l.save(); ink(l, 4); l.beginPath(); l.moveTo(960, 520); l.lineTo(960 + Math.sin(sa * TAU) * 300, 520 - Math.cos(sa * TAU) * 300); l.stroke(); l.beginPath(); l.arc(960, 520, 16, 0, TAU); l.fill(); l.restore();
  }, VID);

  // ── P27 iki belge yan yana, aynı ağırlıkta: Le Texier (ilk akşam vardiyası) / Zimbardo (her vardiyada bir iki gardiyan) ──
  sahne('P27', 'C04@zimbardo', 'kart', 'kart', (B, st) => {
    B.cam(960, 500, 1.02 + st.lt * .014);
    tam(B, .38);
    const tZ = tA('C04@zimbardo'), tY = tA('C04@yazıyor'), tS = tA('C04@sertleştiğini');
    const sol = ['En sert davranışlar', 'tek vardiyada:', 'akşam (18.00–02.00)'];
    const sag = ['Her vardiyada bir iki', 'gardiyan giderek', 'sertleşti.'];
    sayfa(B, 150, 190, 790, ['LE TEXIER · 2019'], sol, 1, { px: 46, vurgu: { 2: ramp(st.t, st.at + .2, st.at + .9, E.lin) }, h: 470 });
    sayfa(B, 980, 190, 790, ['ZIMBARDO · 2018'], sag, ramp(st.t, tZ + .1, tY - .2, E.lin), { px: 46, vurgu: { 2: ramp(st.t, tS, tS + .6, E.lin) }, h: 470 });
  }, { ...KAG, over: KU('Le Texier 2019 · Zimbardo 2018 (çeviriler bizim)', { t0: .4 }) });

  // ── P28 loş gece koridoru: uzun boylu gardiyan öne çıkar, durur; "tiyatro"da tepesindeki lamba yanar, "John Wayne"de gözlük parlar ──
  const P28t = st => ({ d: yerel(st, 'C05@deyv'), c: yerel(st, 'C05@con') });
  sahne('P28', 'C05', 'koridor', 'genis', (B, st) => {
    B.cam(960, 530, 1.02 + st.lt * .014);
    const titre = Math.sin(st.t * 31) > .93 ? .15 : 0;
    const K = D.koridor(B, st.t, { isik: .3 - titre, sonD: .86, solD: .6, sagD: .64 });
    const k = B.k; k.save(); k.fillStyle = 'rgba(0,0,0,.42)'; k.fillRect(-900, -900, W + 1800, H + 1800); k.restore();   // gece: her şey bir kademe koyu
    const tTi = tA('C05@tiyatro'), lamba = ramp(st.t, tTi - .1, tTi + .15, E.lin) * (Math.sin(st.t * 60) > -.6 || st.t > tTi + .5 ? 1 : .4);
    const zg = .32;
    // solda duvar dibinde üç mahkûm (gece sayımı); "mahkûmlar"da başlarını ona çevirir
    const tM = tA('C05@mahkumlar'), don = ramp(st.t, tM, tM + .6);
    for (let i = 0; i < 3; i++) { const z = .26 + i * .09, p = K.yer(z, -.74); kisiD(B, p[0], p[1], 700 * (1 - z), { tip: 'mahkum', f: 1, numara: NUM[i + 2], bas: lerp(.25, -.05, don) + Math.sin(st.t * .6 + i) * .02, kolO: [-.05, .1], kolA: [-.08, .1] }); }
    // uzun boylu gardiyan: "öne"de yürümeye başlar, "Deyv"de durur
    const tt = P28t(st), g0 = K.yer(zg, -.82), s = 700 * (1 - zg) * 1.13;
    const gr = SET.yuru(B.l, g0[0], g0[1], s, st.lt, { tip: 'gardiyan', f: 1, go: yuruAra([[yerel(st, 'C05@öne'), tt.d + .2]]), kolO: [.2, .35], kolA: [-.05, .2], bas: -.04, parilti: st.t > tA('C05@con') ? '#FFFFFF' : '#C8CED0' });
    if (lamba > 0) {   // "tiyatro": tepesindeki floresan yanar, yerde dikdörtgen ışık (sahne ışığı; huzme ve halka yok)
      const u = (gr.kalca[0] - 960) / (760 * (1 - zg)), P = K.P;
      const q = (z0, z1, u0, u1, h) => { k.beginPath(); k.moveTo(...P(z0, u0, h)); k.lineTo(...P(z1, u0, h)); k.lineTo(...P(z1, u1, h)); k.lineTo(...P(z0, u1, h)); k.closePath(); k.fill(); };
      k.save(); k.fillStyle = '#fff'; k.globalAlpha = lamba; q(zg - .03, zg + .03, u - .08, u + .08, 1); k.globalAlpha = .55 * lamba; q(zg - .06, zg + .07, u - .3, u + .3, 0); k.restore();
    }
  }, { ...VID, mb: 2, over: (ctx, st) => { const tt = P28t(st); ETK('DAVE ESHELMAN', 960, 170, { video: 1, t0: tt.d, d: tt.c - tt.d + .2 })(ctx, st); ETK('JOHN WAYNE · DAVE ESHELMAN', 960, 170, { video: 1, t0: tt.c, d: 2.6 })(ctx, st); } });

  // ── P29 Eshelman ve şınav: tek mahkûm yandan, iniş-kalkış belirgin; "şınav"da tempo artar, "keyfî"de gardiyan eğilip yeri gösterir ──
  sahne('P29', 'C06@zimbardonun', 'koridor', 'orta', (B, st) => {
    B.cam(980, 720, 1.0 + st.lt * .01);   // zemin altyazı bandının üstünde, gardiyanın başı kadrajda
    D.koridor(B, st.t, { levha: false });
    const tS = tA('C06@şınav') - st.at, tK = tA('C06@keyfi'), tl = st.lt;
    const faz = .55 * tl + .55 * Math.max(0, tl - tS);   // tur/sn: önce yavaş, sonra iki kat
    const h = .9 + .1 * Math.cos(faz * TAU);   // gövde hiç yere yapışmaz: kollar gergin şınav (yerde yatan beden okunuyordu)
    sinav(B, 470, 1012, 9, h, 1);
    const egil = ramp(st.t, tK - .2, tK + .5), konus = 1 - ramp(st.t, tA('C06@zimbardonun') - .3, tA('C06@zimbardonun'));
    const say = ramp(st.lt, tS - .2, tS + .2) * (1 - egil);
    FIG.kisi(B.l, 1330, 1012, 800, { tip: 'gardiyan', f: -1, serbest: 1, govde: .04 + .14 * egil, bas: .2 + .05 * Math.sin(st.t * 7) * konus + .1 * egil,
      kolO: [lerp(lerp(.2, .4, say), .35, egil), lerp(lerp(.5, .7, say), .4, egil)], kolA: [-.1, .3] });   // yumruk kalkmaz
  }, { ...VID, over: KU("Zimbardo'nun anlatımı (2018)", { video: 1, t0: .6 }) });

  // ── P30 tepsi: kaşıklı el girer, "kısıyor"da yemeğin yarısını alır ve kadrajın sağından çıkar; yemek sağ yandan yuvarlak kenarla azalır ──
  sahne('P30', 'C06@yemeği', 'tepsi', 'ayrinti', (B, st) => {
    B.cam(960, 540, 1.06 + st.lt * .05);
    tam(B, .6);
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .32); k.beginPath(); k.roundRect(280, 170, 1360, 760, 30); k.fill(); k.restore();
    l.save(); ink(l, 6); l.beginPath(); l.roundRect(280, 170, 1360, 760, 30); l.stroke(); l.restore();
    const tK = tA('C06@kısıyor'), gel = ramp(st.t, st.at, tK, E.out3), al = ramp(st.t, tK, tK + .85, E.io2);
    tabak(B, 960, 550, 380, 250, 0);
    yemekCiz(B, 960, 550, 380, 250, 21, 1 - .5 * ramp(al, .05, .4, E.out3));
    // el (kaşıkla): sağdan girer, yemeğin sağ kenarına dalar, kaşık dolu sağa doğru kadrajdan çıkar (yatay; tepsinin dışına sıçramaz)
    const hx = lerp(1900, 1170, gel) + 1150 * ramp(al, .35, 1, E.in2), hy = 570 - 50 * Math.sin(PI * clamp(al / .5));
    l.save(); ink(l, 16); l.beginPath(); l.moveTo(hx - 120, hy + 40); l.lineTo(hx + 40, hy - 10); l.stroke(); l.beginPath(); l.ellipse(hx - 150, hy + 48, 60, 30, -.3, 0, TAU); l.fill();
    if (al > .08) { l.fillStyle = '#77776F'; const q = Math.min(1, (al - .08) * 4); l.beginPath(); l.ellipse(hx - 150, hy + 34, 70 * q, 34 * q, -.3, PI, TAU); l.fill(); }   // kaşıktaki yemek
    l.restore();
    FIG.elYakin(B.l, hx + 60, hy - 20, 11, -1, false, .9);
  }, VID);

  // ── P31 416 hücrede oturuyor; tabak kadraj dışından itilir ve kayar; "yemek"te tabağa bakar, "reddediyor"da geri yaslanır, kollarını kavuşturur ──
  sahne('P31', 'C07', 'hucre', 'orta', (B, st) => {
    B.cam(940, 560, 1.05 + st.lt * .018);
    const G = 940; tam(B, .44); yer(B, G, .6);
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .5); k.fillRect(-300, 80, 2600, 14); k.restore();
    // ranza kenarı (oturak)
    k.save(); k.fillStyle = T(B, .62); k.fillRect(180, 784, 560, 40); k.fillStyle = T(B, .72); k.fillRect(190, 824, 24, 116); k.fillRect(706, 824, 24, 116); k.restore();
    l.save(); ink(l, 4); l.strokeRect(180, 784, 560, 40); l.restore();
    const tY = tA('C07@yemek'), tR = tA('C07@reddediyor');
    const bak = ramp(st.t, tY - .2, tY + .5) * (1 - ramp(st.t, tR - .2, tR + .4)), red = ramp(st.t, tR - .2, tR + .6);
    kisiD(B, 520, G, 640, { tip: 'mahkum', f: 1, numara: '416', bacak: 'otur', sandalye: false, bas: .12 + .26 * bak - .2 * red + Math.sin(st.t * .8) * .02, govde: .1 + .08 * bak - .16 * red,
      kolO: [lerp(.55, .25, red), lerp(.9, 1.55, red)], kolA: [lerp(.5, .3, red), lerp(.95, 1.5, red)], zincir: true, serbest: 1 });
    // tabak sağdan itilir, el bırakınca kayarak önünde durur; el kadraj dışına çekilir (kol omuzdan kadraj dışında)
    const pp = ramp(st.t, st.at + .05, st.at + 1.5, E.out3), px = lerp(1660, 1080, pp);
    const geri = ramp(st.t, st.at + 1.2, st.at + 2.1, E.in2), hx = Math.max(px + 150, 1580) + 900 * geri, hy = G - 40;
    tabak(B, px, G - 16, 120, 32, 1, { tohum: 5 });
    parmaklik(B, 40, 1880, 60, 1100, 8, { cer: 0.01, cub: 15 });
    l.save(); ink(l, 22); l.beginPath(); l.moveTo(-200, 60); l.lineTo(2200, 60); l.stroke(); l.restore();
    if (geri < 1) {
      l.save(); l.fillStyle = '#000'; FIG.uzuv(l, [hx + 182, hy + 21], [hx + 560, hy - 380], 44, 54); l.restore();
      FIG.elYakin(B.l, hx, hy, 7, -1, false, .4);
    }
  }, { ...VID, over: (ctx, st) => ETK('416', 960, 170, { video: 1, px: 56, t0: yerel(st, 'C07@dört'), d: 3.2 })(ctx, st) });

  // ── P32 dolap kapısı + duvar saati: kuralda bir saat, gerçekte üç saat; içeriden darbeler saat ilerledikçe seyrelir ve zayıflar ──
  sahne('P32', 'C07@kuralda', 'dolap', 'ayrinti', (B, st) => {
    B.cam(960, 540, 1.04 + st.lt * .03);
    tam(B, .4);
    const p1 = ramp(st.t, st.at, tA('C07@yazan'), E.io2), p2 = ramp(st.t, tA('C07@üç') - .3, tA('C07@tutuluyor') + .5, E.io2);
    const kn = [[.2, 10], [1.25, 7], [2.5, 4], [3.6, 2]].reduce((a_, [a, g]) => { const u = st.lt - a; return a_ + (u > 0 && u < .45 ? (1 - u / .45) * g : 0); }, 0);
    const sh = (kn + .6) * Math.sin(st.t * 47);
    SET.dolap(B, 260, 150, 560, 820, sh);
    // kapının altındaki aralık: darbede içerideki gölge kıpırdar
    const k = B.k; k.save(); k.fillStyle = T(B, .95); k.fillRect(260 + sh, 962, 560, 8); k.fillStyle = T(B, .2); k.fillRect(260 + 200 + kn * 18, 962, 90 + kn * 6, 8); k.restore();
    const s = 22 + p1 + 2 * p2;
    SET.saat(B, 1400, 420, 240, Math.floor(s), (s % 1) * 60);
  }, VID);

  // ── P33 hücreler: battaniyeli mahkûmlar parmaklık ardında; "seçim"de başlar gardiyana döner, "çoğu"nda battaniyeler göğse çekilir; dolap kapalı kalır ──
  sahne('P33', 'C08', 'hucre', 'genis', (B, st) => {
    B.cam(960, 520, 1.02 + st.lt * .012);
    const G = 880; tam(B, .46); yer(B, G, .62);
    const k = B.k; k.save(); k.strokeStyle = T(B, .5); k.lineWidth = 3; for (let i = 0; i < 6; i++) { k.beginPath(); k.moveTo(-200, 920 + i * i * 9); k.lineTo(2200, 920 + i * i * 9); k.stroke(); } k.restore();
    const tC = tA('C08@çoğu'), cek = ramp(st.t, tC - .1, tC + .7), sec = ramp(st.t, tA('C08@seçim') - .1, tA('C08@seçim') + .5) * (1 - cek);
    const hucre = [[110, 520, [[215, 1, NUM[1]], [405, 1, NUM[4]]]], [610, 1020, [[715, -1, NUM[5]], [905, -1, NUM[6]]]], [1110, 1520, [[1215, 1, NUM[8]], [1405, 1, NUM[2]]]]];
    hucre.forEach(([x0, x1, ic], j) => {
      k.save(); k.fillStyle = T(B, .56); k.fillRect(x0, 150, x1 - x0, G - 150); k.fillStyle = T(B, .64); k.fillRect(x0, 760, x1 - x0, G - 760); k.restore();
      ic.forEach(([x, f, n], i) => battaniyeli(B, x, 862, 380 + ((i + j) % 2) * 26, { f, numara: n, cek, bas: .12 - .22 * sec + .12 * cek + Math.sin(st.t * .7 + i + j) * .03 }));
      parmaklik(B, x0, x1, 150, G, 6, { cer: 14, cub: 9 });
    });
    // dolap: başta hafif titrer (içeride 416), "çoğu"ndan sonra kıpırtısız
    const sh = 1.6 * Math.sin(st.t * 41) * (1 - cek);
    k.save(); k.fillStyle = T(B, .74); k.fillRect(1640 + sh, 260, 220, G - 260); k.restore();
    const l = B.l; l.save(); ink(l, 6); l.strokeRect(1640 + sh, 260, 220, G - 260); l.beginPath(); l.arc(1662 + sh, 580, 9, 0, TAU); l.fill(); l.restore();
    // gardiyan koridorda yürür, "seçim"de durur, "vazgeçerlerse"de dolaba doğru yürür, "çoğu"nda durur
    SET.yuru(B.l, 40, 1010, 520, st.lt, { tip: 'gardiyan', f: 1, kolO: [.2, .35], kolA: [-.05, .2], bas: .04, go: yuruAra([[0.01, yerel(st, 'C08@seçim') + .3], [yerel(st, 'C08@vazgeçerlerse'), yerel(st, 'C08@çoğu') + .2]]) });
  }, { ...VID, mb: 2 });

  // ── P34 koridorun ucunda kapı açılır; kadın silueti girer, durur ──
  sahne('P34', 'C09', 'koridor', 'orta', (B, st) => {
    B.cam(960, 540, 1.03 + st.lt * .02);
    const G = 900, dx0 = 800, dx1 = 1040, dyt = 330;
    tam(B, .56); yer(B, G, .64);
    const k = B.k, l = B.l;
    // yan duvarlar (perspektif kenar) ve tavan floresanı
    k.save(); k.fillStyle = T(B, .44); k.beginPath(); k.moveTo(-100, -100); k.lineTo(300, 120); k.lineTo(300, G); k.lineTo(-100, 1180); k.closePath(); k.fill();
    k.fillStyle = T(B, .5); k.beginPath(); k.moveTo(2020, -100); k.lineTo(1620, 120); k.lineTo(1620, G); k.lineTo(2020, 1180); k.closePath(); k.fill();
    k.fillStyle = T(B, .3); k.beginPath(); k.moveTo(-100, -100); k.lineTo(2020, -100); k.lineTo(1620, 120); k.lineTo(300, 120); k.closePath(); k.fill();
    k.fillStyle = T(B, .05); k.fillRect(700, 40, 520, 22); k.restore();
    l.save(); ink(l, 3); l.beginPath(); l.moveTo(300, 120); l.lineTo(300, G); l.lineTo(1620, G); l.lineTo(1620, 120); l.stroke(); l.restore();
    const tP = tA('C09@psikolog'), ac = ramp(st.t, tP - .3, tP + .5, E.out3);
    // kapının altından gelen ışık (başta), sonra açılan kapı: içerisi aydınlık merdiven
    const alt = ramp(st.t, st.at, tP - .3, E.lin);
    k.save(); k.fillStyle = T(B, .78); k.fillRect(dx0, dyt, dx1 - dx0, G - dyt); k.fillStyle = '#fff'; k.globalAlpha = .4 + .6 * alt; k.fillRect(dx0, G - 6, dx1 - dx0, 6); k.restore();
    if (ac > 0) {
      const xr = lerp(dx1, dx1 + 150, ac);
      k.save(); k.fillStyle = T(B, .06); k.fillRect(dx0, dyt, (dx1 - dx0) * ac, G - dyt);
      k.globalAlpha = .55; k.beginPath(); k.moveTo(dx0, G); k.lineTo(dx0 + (dx1 - dx0) * ac, G); k.lineTo(dx0 + (dx1 - dx0) * ac + 260 * ac, 1080); k.lineTo(dx0 - 120 * ac, 1080); k.closePath(); k.fill(); k.restore();   // yere düşen ışık
      k.save(); k.fillStyle = T(B, .7); k.beginPath(); k.moveTo(dx0 + (dx1 - dx0) * ac, dyt); k.lineTo(xr, dyt - 30 * ac); k.lineTo(xr, G + 30 * ac); k.lineTo(dx0 + (dx1 - dx0) * ac, G); k.closePath(); k.fill(); k.restore();
    }
    l.save(); ink(l, 6); l.strokeRect(dx0, dyt, dx1 - dx0, G - dyt); l.restore();
    // kadın: kapıdan çıkar, kapının yanına yürür ve durur
    const tg = st.t - (tP + .15);
    if (tg > 0) SET.yuru(B.l, 900, G + 4, 540, tg, { tip: 'kadin', f: 1, desen: false, etek: 15, kolO: [.1, .3], kolA: [-.1, .2], go: yuruAra([[0, yerel(st, 'C09@iniyor') + .3 - (tP + .15 - st.at)]]) });
  }, { ...VID, mb: 2, over: KU('Christina Maslach', { video: 1, t0: 1.9 }) });

  // ── P35 tuvalet yürüyüşü: tek sıra, bir el öndekinin sırtında (dirsek aşağıda, kol yatay uzanmaz), ayaklar zincirli (başlarda torba ÇİZİLMEZ); gardiyan sıranın arkasından gelir; "zincirli"de kamera ayaklara iner ──
  sahne('P35', 'C09@mahkumların', 'koridor', 'genis', (B, st) => {
    const tZ = tA('C09@zincirli'), z = ramp(st.t, tZ - .2, tZ + 1.2, E.io2);
    B.cam(lerp(980, 1060, z) + st.lt * 12, lerp(540, 820, z), lerp(1.02, 1.42, z) + st.lt * .01);
    bodrum(B, st, { levha: false });
    const G = 1000, boy = 430, s = boy * .97 / 100, ara = 26.5 * s, tl = st.lt;
    const ks = [];
    for (let i = 0; i < 5; i++) ks.push(yuruD(B, 560 - i * ara, G, boy + (i % 2) * 14, tl, { tip: 'mahkum', f: 1, numara: NUM[i], kolO: [.12, .3], kolA: [-.05, .2], bas: .1 + Math.sin(i * 1.7) * .03 }));   // kollar aşağıda (başkan: uzanan kol dizisi selam okunmasın)
    SET.yuru(B.l, 560 - 4 * ara - 260, G, 470, tl, { tip: 'gardiyan', f: 1, kolO: [.2, .35], kolA: [-.05, .2], bas: .04 });
    // ayak bileklerinden bir sonrakine sarkan zincir
    const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 3;
    for (let i = 0; i < 4; i++) { const a = ks[i + 1].kalca[0], b = ks[i].kalca[0]; l.beginPath(); l.moveTo(a + 4, G - 14); l.quadraticCurveTo((a + b) / 2, G + 4, b - 4, G - 14); l.stroke(); }
    l.restore();
  }, { ...VID, mb: 2 });

  // ── P36 kadın yakın, başı dönük; "Buna bakamıyorum." Arkada kapı aralığından görülen yürüyen sıra (bir kademe açık): eller öndekinin omzunda, dirsek düşük; parmaklık yok ──
  sahne('P36', 'C10', 'koridor', 'yakin', (B, st) => {
    B.cam(960, 540, 1.03 + st.lt * .02);
    tam(B, .52);
    const k = B.k, l = B.l, xj = 930;
    B.save(); for (const g of [k, l]) { g.beginPath(); g.rect(-400, -200, xj + 400, 1500); g.clip(); }
    k.fillStyle = T(B, .3); k.fillRect(-400, -200, xj + 400, 1500); k.fillStyle = T(B, .4); k.fillRect(-400, 930, xj + 400, 400);
        const boy = 520, s = boy * .97 / 100, ara = 26.5 * s, ks = [];
    for (let i = 0; i < 5; i++) ks.push(SET.yuru(k, 640 - i * ara, 960, boy, st.lt, { tip: 'mahkum', f: 1, renk: T(B, .72), onlukRenk: T(B, .44), numara: NUM[i + 3], kolO: [.12, .3], kolA: [-.05, .2], bas: .12 + Math.sin(i * 1.3) * .03, zincir: false }));
    k.save(); k.strokeStyle = T(B, .72); k.lineWidth = 3; for (let i = 0; i < 4; i++) { const a = ks[i + 1].kalca[0], b = ks[i].kalca[0]; k.beginPath(); k.moveTo(a + 4, 946); k.quadraticCurveTo((a + b) / 2, 962, b - 4, 946); k.stroke(); } k.restore();
    B.restore();
    // kapı pervazı (koyu, dikey); kadın pervazın berisinde
    l.save(); l.fillStyle = '#000'; l.fillRect(xj, -100, 56, 1300); l.restore();   // yalnız dikey pervaz (üst kirişle ters L / darağacı okunmasın)
    const tB = tA('C10@bakamıyorum'), tT = tA('C10@tartışıyor');
    const eg = ramp(st.t, tB - .1, tB + .6), kalk = ramp(st.t, tT - .2, tT + .5);
    yakinFig(B, 'kadin', 1380, 400, 2050, { f: 1, desen: false, bas: lerp(.04, .32, eg) - .3 * kalk, govde: .05 * eg * (1 - kalk), kolO: [.1, .3], kolA: [-.1, .2] });
  }, { ...VID, over: QT('Buna bakamıyorum.', 'Christina Maslach, Stanford Magazine (2011)', { video: 1, x: 560, y: 330, px: 76, maxW: 820, t0: .25 }) });

  // ── P37 altıncı gün sabahı: boş koridor; lambalar titreyerek tam yanar; "bitiyor"da hücre kapıları birer birer açılır (parmaklıklı kanat koridora döner) ──
  sahne('P37', 'C10@ertesi', 'koridor', 'genis', (B, st) => {
    B.cam(960, 500, 1.0 + st.lt * .022);
    const lt = st.lt, yan = lt < .9 ? (Math.sin(lt * 50) > .2 ? .9 : .35) : 1;
    const tB = tA('C10@bitiyor');
    const acil = (y, i) => { const n = i * 2 + (y > 0 ? 1 : 0); return ramp(st.t, tB - .15 + n * .22, tB + .4 + n * .22, E.out3); };
    const K = bodrum(B, st, { isik: yan, acik: (y, i) => acil(y, i) > .02 });
    const k = B.k, l = B.l;
    [...K.kapilar].sort((a, b) => b.i - a.i).forEach(q => {
      const p = acil(q.yan, q.i); if (p <= .02) return;
      const z0 = .12 + q.i * .31, th = p * 1.35, zf = z0 + .07 * Math.cos(th), uf = q.yan * (1 - .2 * Math.sin(th));
      const e = K.P(zf, uf, 0), f = K.P(zf, uf, .72), a = q.a, d = q.d;
      k.save(); k.fillStyle = T(B, .8); k.beginPath(); k.moveTo(...a); k.lineTo(...e); k.lineTo(...f); k.lineTo(...d); k.closePath(); k.fill(); k.restore();
      const w = Math.max(1.5, Math.abs(q.b[0] - q.a[0]) * .05);
      l.save(); ink(l, w * 1.6); l.beginPath(); l.moveTo(...a); l.lineTo(...e); l.lineTo(...f); l.lineTo(...d); l.closePath(); l.stroke();
      l.lineWidth = w; for (let i = 1; i < 7; i++) { const u = i / 7; l.beginPath(); l.moveTo(lerp(a[0], e[0], u), lerp(a[1], e[1], u)); l.lineTo(lerp(d[0], f[0], u), lerp(d[1], f[1], u)); l.stroke(); }
      l.restore();
    });
  }, { ...VID, over: ETK('20 AĞUSTOS 1971 · ALTINCI GÜN', 960, 160, { video: 1, t0: .4, d: 4.4 }) });

  // ── P38 masada makale ve teyp (geniş); "göre"de kamera sayfaya iner: Haney, Banks, Zimbardo 1973, "en az üçte biri" kehribar; "geldi"den sonra geri çekilir ──
  //   Yazı levhası yalnız yakın evrede (≈ 7 sn); uzak görünümde satırlar gri çubuk (okunmaya çalışılan küçük yazı yok)
  const P38c = st => { const g0 = tA('C11@göre'), g1 = tA('C11@geldi'); return ramp(st.t, g0 - 1.7, g0 - .1, E.io2) * (1 - ramp(st.t, g1 + .05, g1 + 2.2, E.io2)); };
  sahne('P38', 'C11@gardiyanların', 'kart', 'kart', (B, st) => {
    const c = P38c(st), u = 1 - c;
    B.cam(lerp(960, 1440 - st.lt * 5, u), lerp(470 + st.lt * 3, 610, u), lerp(1.1, .55 + st.lt * .003, u));
    const my = 900;
    SET.karanlik(B, .8);
    SET.koni(B, 2400, -900, 180, my + 10, 1300, { a: .9, tohum: 9 });
    const k = B.k; k.save(); k.fillStyle = T(B, .9); k.fillRect(-1400, my, 5200, 1400); k.fillStyle = '#fff'; for (const [a0, a1] of [[1700, 2100], [2130, 2800], [2830, 3000]]) k.fillRect(a0, my - 4, a1 - a0, 8); k.restore();
    SET.surtme(B.l, 1700, 3100, my + 20, 13, { n: 40, boy: 300 });
    SET.teyp(B, 2400, my - 800, 2.2, st.t, { kayit: 1, hz: .45 });
    const s1 = ['Gardiyanların', 'en az üçte biri,', 'bir canlandırmada beklenenden', 'çok daha saldırgan hâle geldi.'];
    const s2 = ['', 'İki gruba da rolleri için', 'özel bir eğitim verilmedi.'];
    const n1 = s1.join('').length, n2 = s2.join('').length;
    const p1 = ramp(st.t, tA('C11@göre') - .05, tA('C11@geldi') + .2, E.lin);
    const tU = tA('C11@üçte#1'), ta = clamp((c - .72) / .28), gr = clamp((.6 - c) / .3);
    sayfa(B, 300, 90, 1320, ['HANEY, BANKS, ZIMBARDO (1973) · s. 69', 'Interpersonal Dynamics in a Simulated Prison'], [...s1, ...s2], n1 * p1 / (n1 + n2), { px: 46, golge: .95, ta, gr, vurgu: { 1: ramp(st.t, tU - .1, tU + .6, E.lin) } });
  }, { baski: st => ({ mod: 'kagit', kuru: .6 * (1 - P38c(st)) }), over: KU('Haney, Banks ve Zimbardo 1973, s. 69 (çevirisi bizim)', { t0: .8 }) });

  // ── P39 dokuz gardiyan: önce üçü koyu ("en az üçte bir"), "üçte"de öbür altısı öne çıkar ("üçte iki") ──
  const P39t = st => yerel(st, 'C12@üçte');
  sahne('P39', 'C12', 'gardiyanlar', 'orta', (B, st) => {
    B.cam(960, 520, 1.02 + st.lt * .012);
    const G = 765; yer(B, G, .16);
    const k = B.k; k.save(); k.fillStyle = T(B, .3); k.fillRect(-900, G, W + 1800, 6); k.restore();
    const tU = tA('C12@üçte'), p = ramp(st.t, tU - .3, tU + .6);
    const dz = [   // farklı boy, duruş ve aralık: sıra hâlinde eşit dikili biçim okunmasın; komşular yüz yüze bakmaz, kollar gövdeye yakın
      { x: 160, b: 545, y: 6, f: -1, kO: [.1, .3], kA: [-.08, .2], bs: .02 }, { x: 330, b: 500, y: -14, f: -1, kO: [.2, .7], kA: [.15, .75], bs: -.04 }, { x: 505, b: 565, y: 10, f: 1, kO: [-.3, .1], kA: [-.35, .1], bs: .08 },
      { x: 745, b: 520, y: -8, f: 1, kO: [.12, .35], kA: [-.1, .2], bs: .05 }, { x: 905, b: 578, y: 14, f: 1, kO: [.2, .7], kA: [.15, .75], bs: -.02 }, { x: 1065, b: 488, y: -18, f: 1, kO: [.1, .3], kA: [.2, .6], bs: .1 },
      { x: 1240, b: 548, y: 4, f: 1, kO: [-.25, .1], kA: [-.3, .1], bs: .0 }, { x: 1400, b: 506, y: -10, f: 1, kO: [.2, .7], kA: [.15, .75], bs: .06 }, { x: 1585, b: 556, y: 12, f: 1, kO: [.15, .4], kA: [-.1, .2], bs: .03 },
    ];
    dz.forEach((o, i) => {
      const uc = i < 3, d = uc ? lerp(1, .42, p) : lerp(.3, 1, p), one = uc ? 0 : p;
      const sw = Math.sin(st.t * .8 + i * 1.3) * .02;
      // gözlük gövdeye yakın tonda, parıltı küçük ve sönük (küçük boyda "beyaz göz" okunmasın)
      FIG.kisi(B.k, o.x, G + o.y + 26 * one, o.b * .92 * (1 + .07 * one), { tip: 'gardiyan', f: o.f, renk: T(B, d), camRenk: T(B, d * .8), parilti: T(B, d * .62), kolO: o.kO, kolA: o.kA, bas: o.bs + sw, serbest: 1 });
    });
  }, { ...KAG, over: (ctx, st) => { const u = P39t(st); ETK('EN AZ ÜÇTE BİR', 352, 130, { t0: .3, d: Math.min(4.6, u) })(ctx, st); ETK('ÜÇTE İKİ', 1150, 130, { t0: u, d: 3.4 })(ctx, st); KU('Erich Fromm, The Anatomy of Human Destructiveness (1973), s. 57–58', { t0: yerel(st, 'C12@fromm') })(ctx, st); } });

  // ── P40 karanlık oturma odası: eski televizyonda koridor; "üniforma"da gözlüklü gardiyan, "bodrum"da yine koridor ──
  sahne('P40', 'C13', 'oda', 'genis', (B, st) => {
    B.cam(lerp(960, 1080, E.io2(clamp(st.lt / 7))), 540, 1.0 + st.lt * .02);
    SET.karanlik(B, .78);
    const k = B.k, l = B.l, G = 1000;
    k.save(); k.fillStyle = T(B, .9); k.fillRect(-900, G, W + 1800, 900); k.fillStyle = T(B, .7); k.fillRect(-900, -900, 980, 1900); k.restore();
    // TV ışığının yere düşen kaması (yalnız zeminde)
    k.save(); k.fillStyle = 'rgba(255,255,255,.4)'; k.beginPath(); k.moveTo(1040, G); k.lineTo(1700, G); k.lineTo(1500, 1180); k.lineTo(560, 1180); k.closePath(); k.fill(); k.restore();
    // dolap (TV sehpası)
    k.save(); k.fillStyle = T(B, .62); k.fillRect(1000, 790, 740, 190); k.restore();
    l.save(); ink(l, 4); l.strokeRect(1000, 790, 740, 190); l.fillRect(1020, 980, 16, 20); l.fillRect(1704, 980, 16, 20); l.beginPath(); l.moveTo(1370, 800); l.lineTo(1370, 970); l.stroke(); l.restore();
    const tU = tA('C13@üniforma'), tB = tA('C13@bodrum');
    SET.monitorIci(B, 1090, 290, 560, 420, (B2) => {
      if (st.t >= tU && st.t < tB) { tam(B2, .5); const kk = B2.k; kk.save(); kk.fillStyle = T(B2, .8); kk.fillRect(240, -300, 240, 1700); kk.restore(); yakinFig(B2, 'gardiyan', 1000, 330, 2300, { f: -1, bas: .08 + Math.sin(st.t * .8) * .02, parilti: '#FFFFFF' }); }
      else bodrum(B2, st, st.t < tU ? { sayim: 4, gardiyanlar: [{ z: .34, u: .2 }, { z: .5, u: -.1, f: 1 }] } : { gardiyanlar: [{ z: .3 + (st.t - tB) * .05, u: .1, f: 1 }] });
    });
    // kanepe ve izleyen (kontursuz koyu kütleler; kimse ışığın altında değil)
    k.save(); k.fillStyle = T(B, .6); k.beginPath(); k.roundRect(60, 610, 780, 260, 30); k.fill(); k.fillStyle = T(B, .68); k.beginPath(); k.roundRect(40, 820, 820, 180, 24); k.fill(); k.restore();
    FIG.kisi(B.l, 540, G, 640, { tip: 'takim', f: 1, bacak: 'otur', sandalye: false, kolO: [.3, .5], kolA: [.25, .55], bas: .04 + Math.sin(st.t * .4) * .015, serbest: 1 });
  }, { baski: { mod: 'kagit', kuru: .5 } });
})();
