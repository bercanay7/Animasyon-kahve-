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
  // belge sayfası (kâğıt): ust başlık satırları (daktilo değil, hep tam), satirlar p ile basılır; vurgu {satır: 0..1} kehribar şerit (yalnız yazının boyu)
  function sayfa(B, x, y, w, ust, satirlar, p, o = {}) {
    const k = B.k, l = B.l, px = o.px || 44, lh = px * 1.5, upx = Math.round(px * .66);
    const ustH = ust.length ? ust.length * upx * 1.5 + px * 1.2 : 0;
    const h = o.h || (ustH + satirlar.length * lh + px * 2.4);
    k.save(); k.fillStyle = T(B, o.golge ?? .6); k.fillRect(x + 14, y + 16, w, h); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
    l.save(); ink(l, 1.6); l.strokeRect(x, y, w, h); l.textBaseline = 'middle';
    l.font = `700 ${upx}px "Courier Prime"`;
    ust.forEach((s, i) => l.fillText(s, x + px * 1.2, y + px * 1.1 + i * upx * 1.5));
    if (ust.length) { l.lineWidth = 1.4; l.beginPath(); l.moveTo(x + px * 1.2, y + ustH - px * .35); l.lineTo(x + w - px * 1.2, y + ustH - px * .35); l.stroke(); }
    l.font = `700 ${px}px "Courier Prime"`;
    const top = satirlar.reduce((a, r) => a + r.length, 0); let kalan = Math.floor(top * clamp(p) + 1e-6);
    satirlar.forEach((r, i) => {
      const yy = y + ustH + px * 1.1 + i * lh, x0 = x + px * 1.2;
      const va = o.vurgu && o.vurgu[i];
      if (va > 0) { const tw = l.measureText(r).width; B.renkBoya(g => g.rect(x0 - 10, yy - px * .62, (tw + 20) * clamp(va), px * 1.24), .6, 0); }
      l.fillText(r.slice(0, Math.max(0, kalan)), x0, yy); kalan -= r.length;
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
  function sinav(B, x, y, s, h, f = 1) {
    const g = B.l, U = FIG.uzuv;
    g.save(); g.translate(x, y); g.scale(f * s, s); g.fillStyle = '#000';
    const omz = [56, -(8.5 + 11 * h)], ayak = [0, -1.6], kal = [24, lerp(ayak[1], omz[1], 24 / 56) - .6];
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
  }
  // tepside tabak ve yemek (video, ayrıntı): tek kenar çizgisi; yemek düzensiz biçim
  function tabak(B, x, y, rx, ry, yemek = 1, o = {}) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .1); k.beginPath(); k.ellipse(x, y, rx, ry, 0, 0, TAU); k.fill(); k.restore();
    l.save(); ink(l, Math.max(2, rx * .02)); l.beginPath(); l.ellipse(x, y, rx, ry, 0, 0, TAU); l.stroke(); l.restore();
    if (yemek > 0) yemekCiz(B, x, y, rx, ry, o.tohum || 21);
  }
  function yemekCiz(B, x, y, rx, ry, tohum) {
    const k = B.k, r = rng(tohum), pts = [];
    for (let i = 0; i < 11; i++) { const a = i / 11 * TAU, q = .52 + r() * .16; pts.push([x + Math.cos(a) * rx * q, y - ry * .05 + Math.sin(a) * ry * q * .9]); }
    k.save(); k.fillStyle = T(B, .62); k.beginPath(); spline(k, pts, true, .9); k.fill();
    k.fillStyle = T(B, .78); for (let i = 0; i < 9; i++) { k.beginPath(); k.ellipse(x + (r() - .5) * rx * .8, y + (r() - .5) * ry * .7, rx * (.04 + r() * .05), ry * (.04 + r() * .04), r() * 3, 0, TAU); k.fill(); }
    k.restore();
  }
  // hücre içinde oturan mahkûm (kucağında battaniye): kisi + açık tonlu battaniye + battaniyeyi saran ön kol
  function battaniyeli(B, x, y, boy, o = {}) {
    const f = o.f || 1;
    const r = FIG.kisi(B.l, x, y, boy, { tip: 'mahkum', f, numara: o.numara || '', kolO: [.32, 1.75], kolA: [.28, 1.85], bas: o.bas ?? .08, zincir: false, onlukRenk: '#8E8E88', serbest: 1 });
    const l = B.l, lift = (o.cek || 0) * boy * .05, w = boy * .3;
    const cx = r.kalca[0] + f * boy * .05, y0 = r.omuz[1] + boy * .07 - lift, y1 = r.kalca[1] + boy * .14;
    l.save(); l.fillStyle = '#CFCFC8'; l.beginPath(); l.roundRect(cx - w / 2, y0, w, y1 - y0, boy * .04); l.fill(); l.restore();
    l.save(); l.fillStyle = '#000'; FIG.uzuv(l, r.dirsekO, [lerp(r.dirsekO[0], r.elO[0], .5) + f * lift * .2, r.elO[1] - lift * .6], boy * .04, boy * .03); l.restore();
    return r;
  }

  // ── P21 ilk gün: sayım; gardiyanlar gülüşüyor (gövde geriye, baş geri), mahkûmlar solda dizili ──
  sahne('P21', 'C01', 'koridor', 'genis', (B, st) => {
    B.cam(lerp(960, 1040, E.io2(clamp(st.lt / 4))), 560, 1.03 + st.lt * .03);
    const g = ramp(st.t, tA('C01@gülüşüyor') - .25, tA('C01@gülüşüyor') + .3);
    const gul = i => Math.sin(st.t * 10.5 + i * 2.1);
    const gr = (z, u, f, i, kol) => ({ z, u, f, govde: g * (-.15 + .06 * gul(i)), bas: g * (-.42 + .08 * gul(i)), kol: g ? [lerp(.15, kol[0], g), lerp(.5, kol[1] + .15 * gul(i), g)] : null });
    bodrum(B, st, { sayim: 6, gardiyanlar: [gr(.3, .12, -1, 0, [.36, 1.9]), gr(.34, .38, -1, 1, [.34, 1.85]), gr(.4, .2, 1, 2, [.38, 1.95])].map(o => o.kol ? o : { ...o, kol: undefined }) });
  }, VID);

  // ── P22 ikinci gün sabahı: hücrede numara sökülür, yatak kapının önüne sürülür (barikat) ──
  sahne('P22', 'C01@ikinci', 'hucre', 'orta', (B, st) => {
    B.cam(960, 520, 1.04 + st.lt * .018);
    const G = 900, x0 = 470, x1 = 1450, yt = 110;
    tam(B, .5); yer(B, G, .64);
    const k = B.k; k.save(); k.fillStyle = T(B, .26); k.fillRect(x0, yt, x1 - x0, G - yt); k.fillStyle = T(B, .4); k.fillRect(x0, 760, x1 - x0, G - 760); k.restore();
    // arkada iki mahkûm (bir kademe açık)
    FIG.kisi(B.k, 1345, 850, 560, { tip: 'mahkum', f: -1, renk: T(B, .72), onlukRenk: T(B, .42), numara: NUM[3], bas: .05 + Math.sin(st.t * .9) * .03 });
    const tB = tA('C01@yataklarla');
    // öndeki mahkûm numarasını söker
    const tN = tA('C01@numaralarını'), tS = tA('C01@söküyor');
    const el = ramp(st.t, tN - .2, tN + .5), cek = ramp(st.t, tS - .05, tS + .25, E.out3);
    const kolO = cek > 0 ? [lerp(.55, .4, cek), lerp(1.75, .35, cek)] : [lerp(.1, .55, el), lerp(.3, 1.75, el)];
    const r = FIG.kisi(B.l, 1080, 870, 640, { tip: 'mahkum', f: 1, numara: cek > .2 ? '' : NUM[0], kolO, kolA: [-.1, .2], bas: .1 + .12 * el * (1 - cek), serbest: 1 });
    if (cek > .2) {   // sökülen numara düşer (dönerek), yerde kalır
      const tl = st.t - (tS + .1), yy = Math.min(870, r.elO[1] + 900 * tl * tl), xx = r.elO[0] + 40 * Math.min(tl, .7);
      const l = B.l; l.save(); l.translate(xx, yy - 18); l.rotate(Math.min(tl, .8) * 4.2); l.fillStyle = '#C6C6BE'; l.fillRect(-44, -24, 88, 48); l.fillStyle = '#000'; l.font = '700 30px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText(NUM[0], 0, 1); l.restore();
    }
    // yatak (dik, ucunun üstünde) kapının içine sürülür: barikat
    const p = ramp(st.t, tB - .1, tB + .9, E.out3), bx = lerp(130, 800, p), sars = Math.sin(clamp((st.t - tB - .9) / .5) * PI * 3) * (1 - clamp((st.t - tB - .9) / .5)) * .03;
    const kk = B.k, l = B.l;
    B.save(); for (const gg of [kk, l]) { gg.beginPath(); gg.rect(x0 + 6, yt, x1 - x0 - 12, G - yt); gg.clip(); }
    // yatağı iten mahkûm (yatağın solunda, bir kademe açık)
    FIG.kisi(B.k, bx - 250, 860, 540, { tip: 'mahkum', f: 1, renk: T(B, .72), onlukRenk: T(B, .42), govde: .18, kolO: [1.25, .45], kolA: [1.15, .55], zincir: false, serbest: 1 });
    for (const gg of [kk, l]) { gg.save(); gg.translate(bx, 880); gg.rotate(-.08 + sars); }
    kk.fillStyle = T(B, .6); kk.beginPath(); kk.roundRect(-165, -690, 330, 660, 40); kk.fill();
    ink(l, 8); l.beginPath(); l.roundRect(-165, -690, 330, 660, 40); l.stroke();
    l.fillStyle = '#D2D2CA'; l.beginPath(); l.roundRect(-120, -650, 240, 110, 30); l.fill(); l.lineWidth = 4; l.stroke();   // yastık: dik duran yatak okunsun
    l.fillStyle = '#000'; for (let i = 0; i < 4; i++) l.fillRect(-150 + i * 92, -30, 22, 30);
    l.lineWidth = 9; l.beginPath(); l.moveTo(-175, -700); l.lineTo(-175, -770); l.lineTo(175, -770); l.lineTo(175, -700); l.stroke();   // karyolanın başlığı (metal)
    l.lineWidth = 5; for (const xx of [-90, 0, 90]) { l.beginPath(); l.moveTo(xx, -770); l.lineTo(xx, -700); l.stroke(); }   // karyola ayakları (yere basan uçta)
    for (const gg of [kk, l]) gg.restore();
    B.restore();
    parmaklik(B, x0, x1, yt, G, 8);
  }, VID);

  // ── P23 söndürücü: gardiyan kapıya doğru sıkar, bulut koridoru doldurur ──
  sahne('P23', 'C02', 'koridor', 'genis', (B, st) => {
    B.cam(960, 520, 1.03 + st.lt * .03);
    const K = bodrum(B, st, {});
    const tS = tA('C02@söndürücüyle'), kalk = ramp(st.t, st.at, tS, E.io2);
    FIG.kisi(B.l, ...K.yer(.46, -.35), 700 * .54, { tip: 'gardiyan', f: 1, kolO: [.25, .4], kolA: [-.1, .2], bas: .05 });
    const p0 = K.yer(.27, -.1), r = FIG.kisi(B.l, p0[0], p0[1], 700 * .73, { tip: 'gardiyan', f: 1, kolO: [lerp(.3, 1.05, kalk), lerp(.4, .55, kalk)], kolA: [lerp(.1, .95, kalk), .7], bas: .08, serbest: 1 });
    // söndürücü tüpü (elde) ve hortum ağzı
    const l = B.l, e = r.elO, s = r.s;
    l.save(); l.fillStyle = '#000'; l.beginPath(); l.roundRect(e[0] - 3 * s, e[1] - 2 * s, 7 * s, 16 * s, 2.5 * s); l.fill(); l.lineWidth = 1.6 * s; l.strokeStyle = '#000'; l.beginPath(); l.moveTo(e[0] + 2 * s, e[1] - 2 * s); l.lineTo(e[0] + 8 * s, e[1] - 4.5 * s); l.stroke(); l.restore();
    const kp = K.kapilar.find(q => q.yan > 0 && q.i === 0) || K.kapilar[0];
    const hx = (kp.a[0] + kp.b[0] + kp.c[0] + kp.d[0]) / 4, hy = (kp.a[1] + kp.b[1] + kp.c[1] + kp.d[1]) / 4;
    const nx = e[0] + 8 * s, ny = e[1] - 4.5 * s, a = Math.atan2(hy - ny, hx - nx);
    SET.bulut(B, nx, ny, a, ramp(st.t, tS, tS + 1.8, E.out3), st.t);
  }, VID);

  // ── P24 iki gardiyan bir yatağı koridora sürükler; "dışarı"da arkadaki ucu bırakır, yatak yerde sürünür ──
  sahne('P24', 'C02@yatakları', 'koridor', 'orta', (B, st) => {
    B.cam(980 + st.lt * 20, 600, 1.16 + st.lt * .015);
    bodrum(B, st, { levha: false });
    const tl = st.lt, tD = tA('C02@dışarı'), bir = ramp(st.t, tD - .1, tD + .45, E.in2);
    const on = SET.yuru(B.l, 900, 1010, 610, tl, { tip: 'gardiyan', f: 1, kolO: [-.45, .1], kolA: [-.5, .1], bas: .06, govde: .08 });
    const ar = SET.yuru(B.l, 210, 1012, 600, tl, { tip: 'gardiyan', f: 1, kolO: [lerp(.95, .15, bir), lerp(.5, .3, bir)], kolA: [lerp(.85, -.1, bir), lerp(.6, .2, bir)], bas: .1, govde: .1 * (1 - bir), serbest: 1 });
    // yatak: öndeki gardiyanın elinden arkadakinin eline (bırakınca arka ucu yere düşer)
    const p1 = [on.elA[0] + 30, on.elA[1] + 6], p0 = [ar.elO[0] - 70, lerp(ar.elO[1], 985, bir)];
    const L = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]), ang = Math.atan2(p1[1] - p0[1], p1[0] - p0[0]);
    const k = B.k, l = B.l;
    for (const g of [k, l]) { g.save(); g.translate(p0[0], p0[1]); g.rotate(ang); }
    k.fillStyle = T(B, .5); k.beginPath(); k.roundRect(0, -40, L, 48, 14); k.fill(); ink(l, 6); l.beginPath(); l.roundRect(0, -40, L, 48, 14); l.stroke(); l.fillRect(10, 8, 10, 30); l.fillRect(L - 20, 8, 10, 30);
    l.fillStyle = '#D2D2CA'; l.beginPath(); l.roundRect(L - 130, -34, 110, 34, 12); l.fill(); l.lineWidth = 3; l.stroke();
    for (const g of [k, l]) g.restore();
  }, { ...VID, mb: 4 });

  // ── P25 karanlık dolap: kapı titrer, "bağırmaya"da sarsılır; "çıkarılıyor"da açılır, mahkûm dışarı alınır ──
  sahne('P25', 'C03', 'dolap', 'yakin', (B, st) => {
    B.cam(960, 540, 1.05 + st.lt * .02);
    const x0 = 560, w = 700, y0 = 90, y1 = 990, xR = x0 + w;
    tam(B, .4); yer(B, y1, .6);
    const tB = tA('C03@bağırmaya'), tC = tA('C03@çıkarılıyor');
    const amp = 1.5 + 9 * ramp(st.t, tB - .1, tB + .3) * (1 - ramp(st.t, tC - .4, tC));
    const sh = amp * Math.sin(st.t * 43) * (.6 + .4 * Math.sin(st.t * 7.3));
    const ac = ramp(st.t, tC - .1, tC + .45, E.out3), k = B.k, l = B.l;
    // kasa
    l.save(); ink(l, 14); l.strokeRect(x0 - 20, y0 - 20, w + 40, y1 - y0 + 20); l.restore();
    if (ac <= 0) {
      k.save(); k.fillStyle = T(B, .74); k.fillRect(x0 + sh, y0, w, y1 - y0); k.restore();
      l.save(); ink(l, 6); l.strokeRect(x0 + sh, y0, w, y1 - y0); l.strokeRect(x0 + 60 + sh, y0 + 70, w - 120, 300); l.strokeRect(x0 + 60 + sh, y0 + 470, w - 120, 360); l.beginPath(); l.arc(x0 + 70 + sh, (y0 + y1) / 2, 18, 0, TAU); l.fill(); l.restore();
      // kapının altından sızan çizgi (içerisi karanlık): ince koyu boşluk
      k.save(); k.fillStyle = T(B, .9); k.fillRect(x0 + sh, y1 - 8, w, 8); k.restore();
    } else {
      // açık: içerisi karanlık, koridorun ışığı kama gibi içeri düşer
      k.save(); k.fillStyle = T(B, .86); k.fillRect(x0, y0, w, y1 - y0);
      k.fillStyle = T(B, .55); k.beginPath(); k.moveTo(xR, y1); k.lineTo(lerp(xR, x0, .9 * ac), y1); k.lineTo(lerp(xR, x0, .5 * ac), y0 + 260); k.lineTo(xR, y0 + 120); k.closePath(); k.fill(); k.restore();
      // kanat: menteşe sağda, sol kenar izleyiciye doğru açılır (görünüşte sağa kayar, büyür)
      const xl = lerp(x0, xR - 90, ac), dy = 70 * ac;
      k.save(); k.fillStyle = T(B, .66); k.beginPath(); k.moveTo(xl, y0 - dy); k.lineTo(xR, y0); k.lineTo(xR, y1); k.lineTo(xl, y1 + dy); k.closePath(); k.fill(); k.restore();
      l.save(); ink(l, 6); l.beginPath(); l.moveTo(xl, y0 - dy); l.lineTo(xR, y0); l.lineTo(xR, y1); l.lineTo(xl, y1 + dy); l.closePath(); l.stroke(); l.restore();
      // mahkûm dışarı alınır: başı eğik, sola yürür
      const tl = st.t - (tC + .15);
      if (tl > -.2) SET.yuru(B.l, 1050, 1000, 860, Math.max(0, tl), { tip: 'mahkum', f: -1, numara: NUM[7], bas: .3, govde: .12, kolO: [.15, .3], kolA: [.2, .4], go: t => clamp(t / .25) });
    }
    // gardiyanın eli kolda (soldan); açılınca kolu bırakıp çekilir
    const hx = ac <= 0 ? x0 + 70 + sh : lerp(x0 + 70, x0 - 240, ramp(st.t, tC + .2, tC + .7)), hy = (y0 + y1) / 2 + 8;
    FIG.elYakin(B.l, hx, hy, 9, 1, false, ac <= 0 ? .7 : 0);
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
    const sol = ['En sert davranışlar', 'ilk akşam vardiyasında', '(18.00–02.00)'];
    const sag = ['Her vardiyada bir iki', 'gardiyan giderek', 'sertleşti.'];
    sayfa(B, 150, 190, 790, ['LE TEXIER · 2019'], sol, 1, { px: 46, vurgu: { 2: ramp(st.t, st.at + .2, st.at + .9, E.lin) }, h: 470 });
    sayfa(B, 980, 190, 790, ['ZIMBARDO · 2018'], sag, ramp(st.t, tZ + .1, tY - .2, E.lin), { px: 46, vurgu: { 2: ramp(st.t, tS, tS + .6, E.lin) }, h: 470 });
  }, { ...KAG, over: KU('Le Texier 2019, s. 8 · Zimbardo 2018 (çeviriler bizim)', { t0: .4 }) });

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
    for (let i = 0; i < 3; i++) { const z = .26 + i * .09, p = K.yer(z, -.74); FIG.kisi(B.l, p[0], p[1], 700 * (1 - z), { tip: 'mahkum', f: 1, numara: NUM[i + 2], bas: lerp(.25, -.05, don) + Math.sin(st.t * .6 + i) * .02, kolO: [-.05, .1], kolA: [-.08, .1] }); }
    // uzun boylu gardiyan: "öne"de yürümeye başlar, "Deyv"de durur
    const tt = P28t(st), g0 = K.yer(zg, -.82), s = 700 * (1 - zg) * 1.13;
    const gr = SET.yuru(B.l, g0[0], g0[1], s, st.lt, { tip: 'gardiyan', f: 1, go: yuruAra([[yerel(st, 'C05@öne'), tt.d + .2]]), kolO: [.2, .35], kolA: [-.05, .2], bas: -.04, parilti: st.t > tA('C05@con') ? '#FFFFFF' : '#C8CED0' });
    if (lamba > 0) {   // "tiyatro": tepesindeki floresan yanar, yerde dikdörtgen ışık (sahne ışığı; huzme ve halka yok)
      const u = (gr.kalca[0] - 960) / (760 * (1 - zg)), P = K.P;
      const q = (z0, z1, u0, u1, h) => { k.beginPath(); k.moveTo(...P(z0, u0, h)); k.lineTo(...P(z1, u0, h)); k.lineTo(...P(z1, u1, h)); k.lineTo(...P(z0, u1, h)); k.closePath(); k.fill(); };
      k.save(); k.fillStyle = '#fff'; k.globalAlpha = lamba; q(zg - .03, zg + .03, u - .08, u + .08, 1); k.globalAlpha = .55 * lamba; q(zg - .06, zg + .07, u - .3, u + .3, 0); k.restore();
    }
  }, { ...VID, mb: 2, over: (ctx, st) => { const tt = P28t(st); ETK('DAVE ESHELMAN', 960, 170, { video: 1, t0: tt.d, d: tt.c - tt.d + .2 })(ctx, st); ETK('JOHN WAYNE · DAVE ESHELMAN', 960, 170, { video: 1, t0: tt.c, d: 2.6 })(ctx, st); } });

  // ── P29 Eshelman ve şınav: tek mahkûm yandan; "şınav"da tempo artar, "keyfî"de gardiyan eğilip yeri gösterir ──
  sahne('P29', 'C06', 'koridor', 'orta', (B, st) => {
    B.cam(980, 560, 1.08 + st.lt * .01);
    D.koridor(B, st.t, { levha: false });
    const tS = tA('C06@şınav') - st.at, tK = tA('C06@keyfi'), tl = st.lt;
    const faz = .55 * tl + .55 * Math.max(0, tl - tS);   // tur/sn: önce yavaş, sonra iki kat
    const h = .5 + .5 * Math.cos(faz * TAU);
    sinav(B, 560, 1012, 6.4, h, 1);
    const egil = ramp(st.t, tK - .2, tK + .5), konus = 1 - ramp(st.t, tA('C06@zimbardonun') - .3, tA('C06@zimbardonun'));
    const say = ramp(st.lt, tS - .2, tS + .2) * (1 - egil);
    FIG.kisi(B.l, 1330, 1012, 800, { tip: 'gardiyan', f: -1, serbest: 1, govde: .04 + .14 * egil, bas: .2 + .05 * Math.sin(st.t * 7) * konus + .1 * egil,
      kolO: [lerp(lerp(.25, .55, say), .45, egil), lerp(lerp(1.6, 1.05 + .3 * Math.sin(faz * TAU), say), .45, egil)], kolA: [-.1, .3] });
  }, { ...VID, over: KU("Zimbardo'nun anlatımı (2018)", { video: 1, t0: .6 }) });

  // ── P30 tepsi: tabaktaki yemek yarıya iner (bir el yarısını alıp götürür) ──
  sahne('P30', 'C06@yemeği', 'tepsi', 'ayrinti', (B, st) => {
    B.cam(960, 540, 1.06 + st.lt * .05);
    tam(B, .6);
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .32); k.beginPath(); k.roundRect(280, 170, 1360, 760, 30); k.fill(); k.restore();
    l.save(); ink(l, 6); l.beginPath(); l.roundRect(280, 170, 1360, 760, 30); l.stroke(); l.restore();
    const tK = tA('C06@kısıyor'), gel = ramp(st.t, st.at, tK, E.out3), al = ramp(st.t, tK, tK + .9, E.io2);
    // tabak yerinde; yemeğin sol yarısı kalır, sağ yarısı elle gider
    tabak(B, 960, 550, 380, 250, 0);
    B.save(); for (const g of [B.k, B.l]) { g.beginPath(); g.rect(-500, -500, 1460, 2200); g.clip(); } yemekCiz(B, 960, 550, 380, 250, 21); B.restore();
    B.save(); for (const g of [B.k, B.l]) { g.beginPath(); g.rect(960, -500, lerp(500, 0, ramp(al, 0, .35, E.lin)), 2200); g.clip(); } yemekCiz(B, 960, 550, 380, 250, 21); B.restore();
    // el (kaşıkla): sağdan girer, yemeğin sağ yarısına; "kısıyor"da alıp götürür
    const hx = lerp(1900, 1180, gel) + 720 * al, hy = 560 - 380 * al;
    l.save(); ink(l, 16); l.beginPath(); l.moveTo(hx - 120, hy + 40); l.lineTo(hx + 40, hy - 10); l.stroke(); l.beginPath(); l.ellipse(hx - 150, hy + 48, 60, 30, -.3, 0, TAU); l.fill();
    if (al > .05) { l.fillStyle = '#77776F'; l.beginPath(); l.ellipse(hx - 150, hy + 30, 72 * Math.min(1, al * 3), 40 * Math.min(1, al * 3), -.3, PI, TAU); l.fill(); }   // kaşıktaki yemek
    l.restore();
    FIG.elYakin(B.l, hx + 60, hy - 20, 11, -1, false, .9);
  }, VID);

  // ── P31 416 hücrede oturuyor, önünde dokunulmamış tabak; "reddediyor"da başını göğsüne gömer, omuzlar kapanır ──
  sahne('P31', 'C07', 'hucre', 'orta', (B, st) => {
    B.cam(940, 560, 1.05 + st.lt * .018);
    const G = 940; tam(B, .44); yer(B, G, .6);
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .5); k.fillRect(-300, 80, 2600, 14); k.restore();
    // ranza kenarı (oturak)
    k.save(); k.fillStyle = T(B, .62); k.fillRect(180, 784, 560, 40); k.fillStyle = T(B, .72); k.fillRect(190, 824, 24, 116); k.fillRect(706, 824, 24, 116); k.restore();
    l.save(); ink(l, 4); l.strokeRect(180, 784, 560, 40); l.restore();
    const tR = tA('C07@reddediyor'), red = ramp(st.t, tR - .2, tR + .6);
    FIG.kisi(B.l, 520, G, 640, { tip: 'mahkum', f: 1, numara: '416', bacak: 'otur', sandalye: false, bas: lerp(.12, .55, red) + Math.sin(st.t * .8) * .02, govde: .1 + .12 * red, kolO: [lerp(.55, .15, red), lerp(.9, 1.35, red)], kolA: [lerp(.5, .1, red), lerp(.95, 1.45, red)], zincir: true, serbest: 1 });
    // tabak sağdan itilerek gelir (elin ucu), sonra yerinde kalır
    const gel = ramp(st.t, st.at, st.at + 1.4, E.out3), px = lerp(1500, 1080, gel);
    tabak(B, px, G - 16, 120, 32, 1, { tohum: 5 });
    if (gel < 1) FIG.elYakin(B.l, px + 150, G - 40, 7, -1, false, .4);
    parmaklik(B, 40, 1880, 60, 1100, 8, { cer: 0.01, cub: 15 });
    l.save(); ink(l, 22); l.beginPath(); l.moveTo(-200, 60); l.lineTo(2200, 60); l.stroke(); l.restore();
  }, { ...VID, over: (ctx, st) => ETK('416', 960, 170, { video: 1, px: 56, t0: yerel(st, 'C07@dört'), d: 3.2 })(ctx, st) });

  // ── P32 dolap kapısı + duvar saati: kuralda bir saat, gerçekte üç saat ──
  sahne('P32', 'C07@kuralda', 'dolap', 'ayrinti', (B, st) => {
    B.cam(960, 540, 1.04 + st.lt * .03);
    tam(B, .4);
    const p1 = ramp(st.t, st.at, tA('C07@yazan'), E.io2), p2 = ramp(st.t, tA('C07@üç') - .3, tA('C07@tutuluyor') + .5, E.io2);
    const sh = 2.2 * Math.sin(st.t * 37) * (1 - .8 * p2);
    SET.dolap(B, 260 + sh * 0, 150, 560, 820, sh);
    const s = 22 + p1 + 2 * p2;
    SET.saat(B, 1400, 420, 240, Math.floor(s), (s % 1) * 60);
  }, VID);

  // ── P33 hücreler: battaniyeli mahkûmlar parmaklık ardında; gardiyan seçimi sunar; "çoğu"nda battaniyeler sıkılır, dolap kapalı kalır ──
  sahne('P33', 'C08', 'hucre', 'genis', (B, st) => {
    B.cam(960, 520, 1.02 + st.lt * .012);
    const G = 880; tam(B, .46); yer(B, G, .62);
    const k = B.k; k.save(); k.strokeStyle = T(B, .5); k.lineWidth = 3; for (let i = 0; i < 6; i++) { k.beginPath(); k.moveTo(-200, 920 + i * i * 9); k.lineTo(2200, 920 + i * i * 9); k.stroke(); } k.restore();
    const tC = tA('C08@çoğu'), cek = ramp(st.t, tC - .1, tC + .7);
    const hucre = [[110, 520, [[215, 1, NUM[1]], [405, 1, NUM[4]]]], [610, 1020, [[715, -1, NUM[5]], [905, -1, NUM[6]]]], [1110, 1520, [[1215, 1, NUM[8]], [1405, 1, NUM[2]]]]];
    hucre.forEach(([x0, x1, ic], j) => {
      k.save(); k.fillStyle = T(B, .56); k.fillRect(x0, 150, x1 - x0, G - 150); k.fillStyle = T(B, .64); k.fillRect(x0, 760, x1 - x0, G - 760); k.restore();
      ic.forEach(([x, f, n], i) => battaniyeli(B, x, 862, 380 + ((i + j) % 2) * 26, { f, numara: n, cek, bas: .1 + Math.sin(st.t * .7 + i + j) * .03 }));
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
    if (tg > 0) SET.yuru(B.l, 900, G + 4, 540, tg, { tip: 'kadin', f: 1, desen: false, kolO: [.1, .3], kolA: [-.1, .2], go: yuruAra([[0, yerel(st, 'C09@iniyor') + .3 - (tP + .15 - st.at)]]) });
  }, { ...VID, mb: 2, over: KU('Christina Maslach', { video: 1, t0: 1.9 }) });

  // ── P35 tuvalet yürüyüşü: tek sıra, eller öndekinin omzunda, ayaklar zincirli (başlarda torba ÇİZİLMEZ); "zincirli"de kamera ayaklara iner ──
  sahne('P35', 'C09@mahkumların', 'koridor', 'genis', (B, st) => {
    const tZ = tA('C09@zincirli'), z = ramp(st.t, tZ - .2, tZ + 1.2, E.io2);
    B.cam(lerp(980, 1060, z) + st.lt * 12, lerp(540, 820, z), lerp(1.02, 1.42, z) + st.lt * .01);
    bodrum(B, st, { levha: false });
    const G = 1000, boy = 430, s = boy * .97 / 100, ara = 33 * s, tl = st.lt;
    const g = SET.yuru(B.l, 760, G, 470, tl, { tip: 'gardiyan', f: 1, kolO: [.2, .35], kolA: [-.05, .2], bas: .04 });
    const ks = [];
    for (let i = 0; i < 5; i++) ks.push(SET.yuru(B.l, 520 - i * ara, G, boy + (i % 2) * 14, tl, { tip: 'mahkum', f: 1, numara: NUM[i], kolO: i ? [1.12, .5] : [.1, .3], kolA: i ? [1.0, .55] : [-.05, .2], bas: .1 + Math.sin(i * 1.7) * .03 }));
    // ayak bileklerinden bir sonrakine sarkan zincir
    const l = B.l; l.save(); l.strokeStyle = '#000'; l.lineWidth = 3;
    for (let i = 0; i < 4; i++) { const a = ks[i + 1].kalca[0], b = ks[i].kalca[0]; l.beginPath(); l.moveTo(a + 4, G - 14); l.quadraticCurveTo((a + b) / 2, G + 4, b - 4, G - 14); l.stroke(); }
    l.restore();
  }, { ...VID, mb: 2 });

  // ── P36 kadın yakın, başı dönük; "Buna bakamıyorum." Arkada parmaklık ve yürüyen sıra (bir kademe açık) ──
  sahne('P36', 'C10', 'koridor', 'yakin', (B, st) => {
    B.cam(960, 540, 1.03 + st.lt * .02);
    tam(B, .52);
    const k = B.k; k.save(); k.fillStyle = T(B, .3); k.fillRect(-300, 120, 1180, 900); k.restore();
    for (let i = 0; i < 4; i++) { const x = ((st.lt * 120 + i * 230) % 1100) - 200; FIG.kisi(B.k, x, 980, 520, { tip: 'mahkum', f: 1, renk: T(B, .7), onlukRenk: T(B, .5), kolO: [1.1, .5], kolA: [1, .55] }); }
    parmaklik(B, -220, 880, 120, 1020, 8, { cer: 16, cub: 13 });
    const tB = tA('C10@bakamıyorum'), tT = tA('C10@tartışıyor');
    const eg = ramp(st.t, tB - .1, tB + .6), kalk = ramp(st.t, tT - .2, tT + .5);
    yakinFig(B, 'kadin', 1360, 400, 2050, { f: 1, desen: false, bas: lerp(.04, .32, eg) - .3 * kalk, govde: .05 * eg * (1 - kalk), kolO: [.1, .3], kolA: [-.1, .2] });
  }, { ...VID, over: QT('Buna bakamıyorum.', 'Christina Maslach, Stanford Magazine (2011)', { video: 1, x: 560, y: 330, px: 76, maxW: 820, t0: .25 }) });

  // ── P37 altıncı gün sabahı: boş koridor, lambalar tam, kapılar açık; "bitiyor"da son kapı da açılır ──
  sahne('P37', 'C10@ertesi', 'koridor', 'genis', (B, st) => {
    B.cam(960, 500, 1.0 + st.lt * .022);
    const lt = st.lt, yan = lt < .9 ? (Math.sin(lt * 50) > .2 ? .9 : .35) : 1;
    const tB = tA('C10@bitiyor');
    bodrum(B, st, { isik: yan, acik: (y, i) => !(y > 0 && i === 1) || st.t > tB });
  }, { ...VID, over: ETK('20 AĞUSTOS 1971 · ALTINCI GÜN', 960, 160, { video: 1, t0: .4, d: 4.4 }) });

  // ── P38 makale sayfası (Haney, Banks, Zimbardo 1973): "en az üçte biri" kehribar; "Makale"de kamera geri çekilir: sayfa masada, teybin yanında ──
  const P38c = st => ramp(st.t, tA('C11@makale#1') - .2, tA('C11@makale#1') + 2.4, E.io2);
  sahne('P38', 'C11', 'kart', 'kart', (B, st) => {
    const c = P38c(st);
    B.cam(lerp(960, 1420, c), lerp(470 + st.lt * 6, 600, c), lerp(1.1 + st.lt * .008, .56, c));
    const my = 900;
    SET.karanlik(B, .8);
    SET.koni(B, 2400, -900, 180, my + 10, 1300, { a: .9, tohum: 9 });
    const k = B.k; k.save(); k.fillStyle = T(B, .9); k.fillRect(-1400, my, 5200, 1400); k.fillStyle = '#fff'; for (const [a0, a1] of [[1700, 2100], [2130, 2800], [2830, 3000]]) k.fillRect(a0, my - 4, a1 - a0, 8); k.restore();
    SET.surtme(B.l, 1700, 3100, my + 20, 13, { n: 40, boy: 300 });
    SET.teyp(B, 2400, my - 800, 2.2, st.t, { kayit: 1, hz: .45 });
    const s1 = ['Gardiyanların', 'en az üçte biri,', 'bir canlandırmada beklenenden', 'çok daha saldırgan hâle geldi.'];
    const s2 = ['', 'İki gruba da rolleri için', 'özel bir eğitim verilmedi.'];
    const n1 = s1.join('').length, n2 = s2.join('').length;
    const p1 = ramp(st.t, st.at + .3, tA('C11@geldi') + .3, E.lin), p2 = ramp(st.t, tA('C11@iki#1'), tA('C11@verilmediğini') + .4, E.lin);
    const tU = tA('C11@üçte#1');
    sayfa(B, 300, 90, 1320, ['HANEY, BANKS, ZIMBARDO (1973) · s. 69', 'Interpersonal Dynamics in a Simulated Prison'], [...s1, ...s2], (n1 * p1 + n2 * p2) / (n1 + n2), { px: 46, golge: .95, vurgu: { 1: ramp(st.t, tU - .1, tU + .6, E.lin) } });
  }, { baski: st => ({ mod: 'kagit', kuru: .6 * P38c(st) }), over: KU('Haney, Banks ve Zimbardo 1973, s. 69 (çevirisi bizim)', { t0: .8 }) });

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
      FIG.kisi(B.k, o.x, G + o.y + 26 * one, o.b * .92 * (1 + .07 * one), { tip: 'gardiyan', f: o.f, renk: T(B, d), camRenk: T(B, d * .62), parilti: T(B, d * .55), kolO: o.kO, kolA: o.kA, bas: o.bs + sw, serbest: 1 });
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
