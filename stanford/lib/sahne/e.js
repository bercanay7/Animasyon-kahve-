// V. Cevap (F01–F05, bitiş ekranı): müdürün yazısı → bant geri sarılır → döküm (iki "deneyeceğim", "kendim olarak") → "Peki." ve bant biter → koridorda kararsız gardiyan → boş oda, masada aynalı gözlük (bitiş ekranı).
// Bodrum yalnız monitörde (VID). Gözlem odası: kâğıt + kuru fırça (.6), ışık konisi teybin üstünde; kimse ışığın altında oturmaz. Belge/döküm: kâğıt, kuru yok.
// Renk yalnız teybin kehribar ışığında, kırmızı kayıt lambasında ve belgedeki kehribar vurgu şeridinde. Yüz yok; makaralar tek tonlu disk (halka yok).
// a.js'deki VID, KAG, bodrum(), yakinFig() kullanılır. Bütün adlar bu kapsamın içinde (aynı sayfada beş sahne dosyası).
(() => {
  'use strict';
  const KK = { baski: { mod: 'kagit', kuru: .6 } };
  const UST = 'STANFORD ARŞİVİ · SC0750 · BANT A';
  // üst katman: film zamanında bir çapadan başlar, d sn sonra söner (ekran yazısı ≤ 8 sn)
  const ZM = (f, at, d = 8) => (ctx, st) => {
    const t0 = (at == null ? st.at : typeof at === 'string' ? A(at) : at) - st.at, lt = st.lt - t0;
    if (lt < 0) return; const a = clamp((d - lt) / .5); if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a; f(ctx, { ...st, lt }); ctx.restore();
  };
  const R = (st, at, d = .6, e) => ramp(st.t, A(at), A(at) + d, e);   // sözcüğe bağlı geçiş 0→1
  const KOL = { kolO: [.45, 1.1], kolA: [.35, 1.18] };                 // önkol masada, dirsek bükük
  const oda = (B, st, o = {}) => SET.gozlemOdasi(B, st, { ...o, mudurO: { ...KOL, ...(o.mudurO || {}) }, markO: { ...KOL, ...(o.markO || {}) } });
  const DOLU = { sol: .97, sag: .97 };                                  // sarılı bant makarayı doldurur: iç içe halka yok

  // ── döküm sayfası (c.js ile aynı düzen): satır başına çapa; vurgu satırları kehribar şerit ──
  function dokum(B, st, id, satirlar, zaman, o = {}) {
    const top = satirlar.reduce((a, r) => a + r.length, 0); let yaz = 0;
    for (let i = 0; i < satirlar.length; i++) {
      if (!satirlar[i].length) continue;
      const a0 = A(zaman[i]); let a1 = Se(id) - .3;
      for (let j = i + 1; j < satirlar.length; j++) if (zaman[j]) { a1 = A(zaman[j]); break; }
      yaz += satirlar[i].length * clamp((st.t - a0) / Math.max(.4, a1 - a0));
    }
    const p = yaz / top;
    const c = [lerp(850, 880, st.p), lerp(400, 400 + Math.min(110, satirlar.length * 16), E.io2(p)), 1.12 + st.lt * .012];
    if (o.cam) o.cam(c); B.cam(c[0], c[1], c[2]);
    const r = SET.belge(B, UST, satirlar, p, { px: 38, w: 1100, x: 200, y: 170, zemin: .72, vurgu: o.vurgu, vurguA: o.vurguA, h: Math.max(470, satirlar.length * 57 + 230) });
    SET.teyp(B, 1520, 180, .45, st.t, { hz: .45, vu: o.vu, kayit: 1, vuIsik: .7, ...DOLU });
    return { ...r, p };
  }
  // ── karanlık oda yakın planı: Mark (baş-omuz, profil sola); ışık yalnız masada (alt), başın yanında açık leke yok ──
  function markYakin(B, st, o = {}) {
    SET.karanlik(B, .8);
    const k = B.k, my = o.masaY ?? 930, ix = o.isikX ?? 900;
    k.save(); k.fillStyle = B.ton(.18); k.beginPath(); k.moveTo(-300, my); k.lineTo(ix, my); k.lineTo(ix + 160, 1400); k.lineTo(-300, 1400); k.closePath(); k.fill(); k.restore();
    SET.surtme(B.k, -200, ix, my + 4, 13, { n: 30, boy: 120, acik: false });
    yakinFig(B, 'gardiyan', o.x ?? 1220, o.y ?? 380, o.boy ?? 2200, { f: -1, gozluk: false, cop: false, bas: o.bas ?? .06, govde: o.govde ?? 0, kolO: o.kolO || [.5, 1.1], kolA: o.kolA || [.3, .9], serbest: 1 });
  }
  // ── masada katlı aynalı gözlük (P50'nin çizimi, ölçekli): (cx, cy) merkez, s ölçek; kay 0..1 camda parıltı şeridinin yeri ──
  function gozluk(B, cx, cy, s, kay) {
    const k = B.k, l = B.l, sy = .78;
    const cam = sx => g2 => { g2.save(); g2.translate(cx, cy); g2.scale(s, s * sy); g2.beginPath(); g2.moveTo(sx * 16, -58); g2.bezierCurveTo(sx * 70, -66, sx * 112, -58, sx * 118, -40);
      g2.bezierCurveTo(sx * 122, -12, sx * 100, 8, sx * 74, 8); g2.bezierCurveTo(sx * 44, 8, sx * 18, -18, sx * 16, -58); g2.closePath(); g2.restore(); };
    k.save(); k.fillStyle = B.ton(.55, .8); k.beginPath(); k.ellipse(cx + 15 * s, cy + 11 * s, 112 * s, 12 * s, 0, 0, TAU); k.fill(); k.restore();   // gölge
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3.4 * s; l.lineCap = 'round';
    for (const sx of [-1, 1]) { l.beginPath(); l.moveTo(cx + sx * 116 * s, cy - 44 * s * sy); l.lineTo(cx - sx * 30 * s, cy - 26 * s * sy); l.stroke(); }   // katlı saplar
    l.restore();
    for (const sx of [-1, 1]) {
      l.save(); cam(sx)(l); l.fillStyle = '#fff'; l.fill(); l.restore();
      k.save(); cam(sx)(k); k.clip(); const gg = k.createLinearGradient(0, cy - 70 * s, 0, cy + 12 * s); gg.addColorStop(0, B.ton(.9)); gg.addColorStop(1, B.ton(.62)); k.fillStyle = gg; k.fillRect(cx - 150 * s, cy - 82 * s, 300 * s, 104 * s);
      const px = lerp(cx - 140 * s, cx + 155 * s, kay); k.fillStyle = B.ton(.02); k.beginPath(); k.moveTo(px - 4 * s, cy - 74 * s); k.lineTo(px + 15 * s, cy - 74 * s); k.lineTo(px - 19 * s, cy + 15 * s); k.lineTo(px - 37 * s, cy + 15 * s); k.closePath(); k.fill(); k.restore();
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 2.6 * s; cam(sx)(l); l.stroke(); l.restore();
    }
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 2.6 * s; l.beginPath(); l.moveTo(cx - 16 * s, cy - 50 * s * sy); l.quadraticCurveTo(cx, cy - 58 * s * sy, cx + 16 * s, cy - 50 * s * sy); l.stroke(); l.beginPath(); l.moveTo(cx - 18 * s, cy - 61 * s * sy); l.lineTo(cx + 18 * s, cy - 61 * s * sy); l.stroke(); l.restore();
  }
  // koridorun kapı eşiğindeki gardiyan (P89; P90'da monitörde aynı yerde durur). lt: P89'un iç zamanı
  const ESIK = { z: .46, u: .5 };
  function esikGardiyan(B2, K, lt, t, o = {}) {
    const p = K.yer(ESIK.z, ESIK.u), boy = 700 * K.olc(ESIK.z);
    const t1 = A('F04@biri') - A('F04');
    const go = u => (u > t1 && u < t1 + 1.1 ? 1 : 0);
    const u = Math.max(0, lt);
    if (!o.don) return SET.yuru(B2.l, p[0], p[1], boy, u, { tip: 'gardiyan', f: 1, go, kolO: o.kolO || [.1, .3], kolA: [.04, .28], bas: o.bas ?? .04, serbest: o.serbest });
    // geri döner: aynı yerde durur, yüzü öteki yana (SET.yuru'nun yol integrali aynen: x = x0 + hiz·s·m)
    let m = 0; const n = Math.max(1, Math.ceil(u * 60)); for (let i = 0; i < n; i++) m += clamp(go(i / 60)) / 60 * (u > 0 ? u * 60 / n : 0);
    const d = YURU.hiz * boy / 100 * 1.05 * m;
    return SET.yuru(B2.l, p[0] + 2 * d, p[1], boy, u, { tip: 'gardiyan', f: -1, go, kolO: o.kolO || [.1, .3], kolA: [.04, .28], bas: o.bas ?? .04 });
  }
  const YURU = HAREKET.yuruyus({ tip: 'yuru' });

  // ── daktilo (P85): silindir, düğmeler, dönüş kolu, gövde, tuş sıraları (yuvarlak değil, yassı dikdörtgen); (dx) şaryo kayması ──
  function daktilo(B, ry, dx) {
    const k = B.k, l = B.l;
    // silindirin altı masa zemini: sayfanın arkaya sarılan kısmı görünmez (zemin tonu SET.belge'deki zemin .66 ile aynı)
    k.save(); k.fillStyle = B.ton(.66); k.fillRect(-900, ry + 40, 3800, 1400); k.restore(); l.save(); l.fillStyle = '#fff'; l.fillRect(-900, ry + 40, 3800, 1400); l.restore();
    // gövde (koyu ton + kontur), önde yazısız açık levha, tuş sıraları
    k.save(); k.fillStyle = B.ton(.86); k.beginPath(); k.moveTo(250, ry + 70); k.lineTo(1670, ry + 70); k.lineTo(1860, ry + 520); k.lineTo(60, ry + 520); k.closePath(); k.fill();
    k.fillStyle = B.ton(.97); k.fillRect(560, ry + 95, 800, 60);   // yazı kılavuzu yuvası
    for (let j = 0; j < 4; j++) { const yy = ry + 200 + j * 70, n = 11 - (j === 3 ? 2 : 0), sp = 112 + j * 12, x0 = 960 - (n - 1) * sp / 2 + (j % 2) * 18;
      k.fillStyle = B.ton(.42); for (let i = 0; i < n; i++) { k.beginPath(); k.roundRect(x0 + i * sp - 36, yy - 20, 72, 40, 6); k.fill(); } }
    k.fillStyle = B.ton(.42); k.beginPath(); k.roundRect(620, ry + 470, 680, 34, 6); k.fill();   // boşluk çubuğu
    k.restore();
    l.save(); l.fillStyle = '#fff'; l.strokeStyle = '#000'; l.lineWidth = 4; l.beginPath(); l.moveTo(250, ry + 70); l.lineTo(1670, ry + 70); l.lineTo(1860, ry + 520); l.lineTo(60, ry + 520); l.closePath(); l.fill(); l.stroke(); l.restore();   // gövde: altındaki sayfa çizgileri silinir
    // şaryo: silindir + iki düğme + sol dönüş kolu (dx ile kayar); silindirin ton plakası da koyu (arkasındaki sayfa açık basmasın)
    k.save(); k.fillStyle = B.ton(.92); k.beginPath(); k.roundRect(180 + dx, ry - 6, 1560, 82, 30); k.fill(); k.restore();
    l.save(); l.fillStyle = '#000'; l.beginPath(); l.roundRect(180 + dx, ry - 6, 1560, 82, 30); l.fill();
    for (const x of [150, 1770]) { l.beginPath(); l.ellipse(x + dx, ry + 35, 46, 62, 0, 0, TAU); l.fill(); }
    l.lineWidth = 12; l.lineCap = 'round'; l.strokeStyle = '#000'; l.beginPath(); l.moveTo(150 + dx, ry - 10); l.lineTo(90 + dx, ry - 90); l.lineTo(10 + dx, ry - 84); l.stroke();
    l.lineWidth = 5; l.beginPath(); l.moveTo(220 + dx, ry - 16); l.lineTo(1700 + dx, ry - 16); l.stroke();   // kâğıt bastırma çubuğu
    l.restore();
    k.save(); k.fillStyle = B.ton(.55); k.fillRect(200 + dx, ry + 6, 1520, 10); k.restore();   // silindirde ışık (orta ton)
  }

  // P85 kart: müdürün deney sonrası yazısı. Önce daktilonun başı (geniş): "müdür"de kâğıt silindire sarılarak yükselir, "yazmış"ta şaryo geri döner;
  //   "iyi"de yazı başlar ve kamera sayfaya iner (yazı ≈ 8 sn). “iyi bir amaç” tırnak içinde, "amaç"ta kehribar vurgu; "ürkütüyor"da kamera satırlara iner.
  sahne('P85', 'F01@iyi', 'rapor', 'kart', (B, st) => {
    const t0 = A('F01@iyi') - .1, t1 = Se('F01') - .3, p = clamp((st.t - t0) / Math.max(2, t1 - t0));
    const w = E.io2(clamp((st.t - st.at) / Math.max(1, t0 + 1 - st.at)));
    const foc = R(st, 'F01@ürkütüyor', 2.2, E.io2);
    B.cam(960, lerp(700, 520, w) - 50 * foc, lerp(.7, 1.0, w) + .07 * foc + .008 * Math.max(0, st.t - t0));
    const feed = R(st, 'F01@müdür', 1.4, E.io2), ret = R(st, 'F01@yazmış', .45, E.out2);
    const dx = lerp(-150, 0, ret), ry = 700;
    const px = 52, sat = ['“İyi bir amaç” uğruna duyarlılığımı,', 'başkalarını düşünmeyi ne kadar kolay', 'kapatabildiğimi görmek beni ürkütüyor.'];
    const r = SET.belge(B, 'MÜDÜRÜN DENEY SONRASI YAZISI', sat, p, { px, w: 1360, x: 280 + dx, y: 250 + lerp(330, 0, feed), zemin: .66, h: 620 });
    const yy = r.y + px * 3.6, cw = px * .6, va = R(st, 'F01@amaç', .9, E.lin);
    if (va > 0) B.renkBoya(g => g.rect(r.x + px * 1.4 - 8, yy - px * .62, (14 * cw + 16) * va, px * 1.24), .62, 0);
    // harf vuruşu: yazı sürerken her yeni harfte kılavuzdan harfin yerine kısa bir çubuk kalkar (imleç yok)
    const top = sat.reduce((a, s) => a + s.length, 0), q = top * p, n = Math.floor(q);
    if (p > 0 && p < 1 && q - n < .45) { let i = 0, c = n; while (i < sat.length - 1 && c > sat[i].length) { c -= sat[i].length; i++; }
      const hx = r.x + px * 1.4 + c * cw + cw / 2, hy = r.y + px * 3.6 + i * px * 1.5 + px * .5, l = B.l;
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 6; l.lineCap = 'round'; l.beginPath(); l.moveTo(hx + 30, ry + 40); l.lineTo(hx + 6, hy + 4); l.stroke(); l.restore(); }
    daktilo(B, ry, dx);
  }, { ...KAG, over: ZM(KU('Jaffe, deney sonrası yazı (Blum 2018; çevirisi bizim)', { y: 190 }), 'F01@iyi', 8) });

  // P86 geniş: gözlem odası (sorgu mizanseni değil): iki siluet masanın aynı yanında, yan yana, ikisi de monitöre ve teybe bakar; ışık yumuşak.
  //   Makaralar hızla geri sarar (monitörde gardiyan geri geri yürür, tarama bandı), "dönelim"de durup normal çalar; ikisi başını kaldırır.
  sahne('P86', 'F02', 'gozlem', 'genis', (B, st) => {
    B.cam(960, 520, 1 + st.lt * .012);
    const tr = A('F02@dönelim') + .15;
    const v = t => t < tr - .25 ? -1.4 : t > tr + .25 ? .45 : lerp(-1.4, .45, E.io2((t - tr + .25) / .5));   // makara hızı (tur/sn)
    let a = 0; const n = Math.max(1, Math.ceil(st.lt * 60)), dt = st.lt / n; for (let i = 0; i < n; i++) a += v(st.at + (i + .5) * dt) * dt;
    const geri = 1 - ramp(st.t, tr - .25, tr + .25);
    const r = oda(B, st, { ang: 2.1 + a * TAU, kayit: 1, isik: .5, koyu: .7, vu: lerp(.35 + .3 * Math.abs(Math.sin(st.t * 5.3)), .04, geri), ...DOLU, mudur: false, mark: false,
      monitor: (B2) => { const K = bodrum(B2, st, { levha: false }); const p = K.yer(.32, -.1);
        SET.yuru(B2.l, p[0] - 900, p[1], 700 * K.olc(.32), 6.2 + a / .45, { tip: 'gardiyan', f: 1, kolO: [.15, .3], kolA: [.1, .3] }); } });
    // iki siluet sağda, ışığın dışında, eşit boyda; ikisi de sola (monitöre/teybe) bakar; dirsekler bükük, önkollar masada
    const kalk = R(st, 'F02@dönelim', .8);
    const kisi = (x, tip, bas) => FIG.kisi(B.l, x, r.masaY + 330, 760, { tip, f: -1, bacak: 'otur', sandalye: true, ...KOL, bas, gozluk: false });
    kisi(1745, 'gardiyan', .16 - .08 * kalk);
    kisi(1515, 'mudur', .1 - .05 * kalk);
  }, { baski: st => { const tr = A('F02@dönelim') + .15, g = 1 - ramp(st.t, tr - .25, tr + .25); return { mod: 'kagit', kuru: .6, bant: [.14 + .36 * ((st.t * 1.6) % 1), 1.3 * g], sarsinti: g }; } });

  // P87 ayrıntı: önce teybin yakını (yazı yok): makaralar döner, "iki" ve "deneyeceğim"de VU ibresi iki kez sıçrar, "itiraz"da çırpınır.
  //   "bir yerde"de kamera geri çekilip döküme iner: önceki iki "deneyeceğim" satırı yazılmış, 22:33 satırı yazılır; kehribar vurgu satır satır uzar (yazı ≈ 7,5 sn).
  sahne('P87', 'F02@bir', 'dokum', 'ayrinti', (B, st) => {
    const sat = ['15:12  MARK:  Deneyeceğim.', '18:55  MARK:  Tamam, deneyeceğim.', '              [...]', '22:33  MARK:  Elimden gelen tek şey,', '              kendim olarak elimden', '              gelenin en iyisini yapmak.'];
    const tb = A('F02@bir') - .6, u = E.io2(clamp((st.t - tb) / 1.2));
    const kick = (w) => { const d = st.t - A(w); return d > 0 ? Math.exp(-d * 3) * Math.min(1, d * 12) : 0; };
    const itz = st.t - A('F02@itiraz'), cirp = itz > 0 && itz < 1.4 ? Math.sin(itz / 1.4 * PI) * Math.abs(Math.sin(st.t * 17)) : 0;
    const vu = clamp(.2 + .12 * Math.abs(Math.sin(st.t * 4.1)) + .7 * kick('F02@iki') + .7 * kick('F02@deneyeceğim') + .65 * cirp);
    const r = dokum(B, st, 'F02', sat, ['F02@mark', 'F02@deneyeceğim', 'F02@itiraz', 'F02@bir', 'F02@kendim', 'F02@gelenin'], { vu,
      cam: c => { const z0 = 3.8 + st.lt * .05; c[0] = lerp(1525, c[0], u); c[1] = lerp(262, c[1], u); c[2] = Math.exp(lerp(Math.log(z0), Math.log(c[2]), u)); } });
    // kehribar vurgu yalnız sözün kendisinde (sütun 14'ten), yazılan harfle birlikte uzar
    let kalan = Math.floor(sat.reduce((a, x) => a + x.length, 0) * r.p);
    sat.forEach((x, i) => { const n = clamp(kalan, 0, x.length); kalan -= x.length; if (i < 3 || n <= 14) return;
      const yy = r.y + 38 * 3.6 + i * 57; B.renkBoya(g => g.rect(r.x + 38 * 1.4 + 14 * 22.8 - 6, yy - 23, (n - 14) * 22.8 + 12, 46), .6, 0); });
  }, { ...KAG, over: ZM(KU('Stanford arşivi, Bant A, 15:12 · 18:55 · 22:33 (çevirisi bizim)'), 'F02@bir', 8) });

  // P88 yakın: Mark karanlıkta, teyp masada ışıkta; "girmesini"nde başı öne düşer, "peki"de başını bir kez sallar → "PEKİ."; bant biter: sol makara boşalır, bant ucu sağ makarada döner
  sahne('P88', 'F03', 'gozlem', 'yakin', (B, st) => {
    B.cam(960, 540, 1.02 + st.lt * .018);
    const tp = A('F03@peki'), q = st.t - tp, nod = q > 0 && q < .9 ? Math.sin(q / .9 * PI) * .12 : 0;
    markYakin(B, st, { x: 1260, y: 360, boy: 2250, bas: .05 + .1 * R(st, 'F03@girmesini', 1) + nod, masaY: 900, isikX: 880 });
    // teyp: bant tp + .6'da biter; makaralar dönmeyi sürdürür, VU söner
    const te = tp + .6, bos = ramp(st.t, tp - 1.2, te, E.in2), bitti = st.t > te;
    const tx = 430, ty = 540, s = 1, ang = st.t * .45 * TAU;
    SET.teyp(B, tx, ty, s, st.t, { ang, kayit: 1, vuIsik: lerp(.75, .3, ramp(st.t, te, te + .8)), vu: bitti ? lerp(.3, 0, clamp((st.t - te) / .4)) : undefined, ...DOLU });
    // sol (veren) makarayı yeniden çiz: gri flanş + küçülen koyu bant + dönen üç delik (iç içe çizgi yok)
    const k = B.k, l = B.l, mr = 98 * s, my = ty + 125 * s, mx = tx - 128 * s;
    for (const g of [k, l]) { g.save(); g.fillStyle = '#fff'; g.beginPath(); g.arc(mx, my, mr + 5 * s, 0, TAU); g.fill(); g.restore(); }
    k.save(); k.fillStyle = B.ton(.6); k.fillRect(mx - mr - 6 * s, my - mr - 6 * s, 2 * mr + 12 * s, 2 * mr + 12 * s);   // gövde paneli (silinen yer)
    k.fillStyle = B.ton(.86); k.beginPath(); k.arc(mx, my, mr, 0, TAU); k.fill();
    k.restore();
    const delik = g => { g.save(); g.translate(mx, my); g.rotate(ang); for (let i = 0; i < 3; i++) { g.rotate(TAU / 3); g.beginPath(); g.ellipse(0, -mr * .62, mr * .14, mr * .24, 0, 0, TAU); g.fillStyle = g === k ? B.ton(.6) : '#fff'; g.fill(); if (g === l) { g.strokeStyle = '#000'; g.lineWidth = 3 * s; g.stroke(); } } g.restore(); };
    const rb = lerp(mr * .93, 0, bos);
    if (rb > mr * .2) { k.save(); k.fillStyle = B.ton(.95); k.beginPath(); k.arc(mx, my, rb, 0, TAU); k.fill(); k.restore(); }
    // flanş çevresi + üç delik + göbek: sağ makarayla aynı çizim (bant doluyken de görünür; makara dönerken okunur)
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3 * s; l.beginPath(); l.arc(mx, my, mr, 0, TAU); l.stroke(); l.restore();
    delik(l);
    l.save(); l.fillStyle = '#000'; l.beginPath(); l.arc(mx, my, mr * .12, 0, TAU); l.fill(); l.restore();
    // bant yolu: bitmeden önce sol makaradan kafaya; bitince yol boş, bant ucu sağ makarada savrulur
    if (!bitti) { l.save(); l.strokeStyle = '#000'; l.lineWidth = 2.2 * s; l.beginPath(); l.moveTo(mx, my + Math.max(rb, mr * .2)); l.lineTo(tx - 30 * s, ty + 236 * s); l.stroke(); l.restore(); }
    else {
      l.save(); l.strokeStyle = '#fff'; l.lineWidth = 6 * s; l.beginPath(); l.moveTo(tx - 128 * s + mr * .2, my + mr * .8); l.lineTo(tx - 30 * s, ty + 236 * s); l.lineTo(tx + 30 * s, ty + 236 * s); l.lineTo(tx + 128 * s, my + mr * .6); l.stroke(); l.restore();
      const rx = tx + 128 * s, ra = ang * 1.25 + PI * .2, rr = mr * .93, sw = Math.sin(st.t * 9) * .25;
      const p0 = [rx + Math.cos(ra) * rr, my + Math.sin(ra) * rr], tg = ra + PI / 2;
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 3.4 * s; l.lineCap = 'round'; l.beginPath(); l.moveTo(...p0);
      l.quadraticCurveTo(p0[0] + Math.cos(tg + sw) * 70 * s, p0[1] + Math.sin(tg + sw) * 70 * s, p0[0] + Math.cos(tg + .6 + sw * 2) * 130 * s, p0[1] + Math.sin(tg + .6 + sw * 2) * 130 * s); l.stroke(); l.restore();
    }
  }, { ...KK, over: OV((ctx, st) => { const t0 = A('F03@peki'); if (st.t > t0 + 7) return; buyukSoz(ctx, 'PEKİ.', st.t, t0, { px: 170, x: 520, y: 210, col: YAZI.kagit, panelRGB: KOYU, panel: .55 }); },
    ZM(KU('Bant A, 26:52 (çevirisi bizim)', { x: 520, y: 370, align: 'center', video: 1 }), 'F03@peki', 7)) });

  // P89 geniş (video): gözlem kamerasından koridor; açık hücre kapısının eşiğinde bir gardiyan. "zalim"de eli kalçadaki copa iner (kol aşağıda, dirsek bükük; yatay kol yok), "biri"de iki adım eşiğe yürür,
  //   "diyeceğini"de durur, eli bırakır, başı öne eğilir. Yavaş yaklaşma ona; plan sonunda tarama bandı geçer.
  sahne('P89', 'F04', 'koridor', 'genis', (B, st) => {
    const u = E.io2(clamp(st.lt / 12));
    B.cam(lerp(960, 1080, u), lerp(520, 500, u), 1 + .32 * u);
    const K = bodrum(B, st, { acik: (yan, i) => yan > 0 && i === 1 });
    const kc = R(st, 'F04@zalim', .7) * (1 - R(st, 'F04@diyeceğini', .9));
    esikGardiyan(B, K, st.lt, st.t, { kolO: [lerp(.02, -.3, kc), lerp(.12, .45, kc)], serbest: 1, bas: .04 + .14 * R(st, 'F04@diyeceğini', 1.1) });
  }, { baski: st => { const u = clamp((st.lt - (st.d - 1.5)) / 1.5); return { mod: 'video', bant: [lerp(-.05, 1.05, u), u > 0 && u < 1 ? 1.4 * Math.sin(u * PI) : 0] }; } });

  // P90 orta (bitiş ekranı dahil, filmin sonuna kadar): karanlık oda, kimse yok. Monitörde koridor ve eşikte duran gardiyan; ışık konisi teybin üstünde,
  //   masada aynalı gözlük. Öğeler sol üstte, grup sol üçte bir çizgisine yakın; sağ yarı ve alt üçte bir koyu ve sade (bitiş ekranı öğeleri). Ekran yazısı yok.
  //   Sözcüğe bağlı eylemler: "peki"de camda parıltı kayar; "başka"da monitördeki gardiyan öteki yana döner; "sonrakini"nde kayıt lambası yanar ve
  //   duran makaralar yeniden dönmeye başlar (yeni bant). Anlatım bitince de hareket sürer: makaralar, VU, monitörde ara ara tarama bandı, yavaş yaklaşma.
  sahne('P90', 'F05', 'gozlem', 'orta', (B, st) => {
    const z = 1 + st.lt * .003, F = [560, 400], C0 = [860, 540];
    B.cam(F[0] + (C0[0] - F[0]) / z, F[1] + (C0[1] - F[1]) / z, z);
    SET.karanlik(B, .84);
    const k = B.k, l = B.l, my = 548;
    SET.koni(B, 700, -60, 90, my + 4, 300, { a: .5, tohum: 9, taban: .45 });
    // monitör masada (soğuk ışık), içinde koridor: gardiyan eşikte; "başka"da öteki yana döner
    l.save(); l.fillStyle = '#000'; l.fillRect(318, 500, 44, my - 500); l.fillRect(270, my - 12, 140, 12); l.restore();
    const isik = 1 - .3 * (Math.sin(st.t * 29) > .93 ? 1 : 0), don = st.t > A('F05@başka');
    const tb0 = Math.max(Se('F05'), st.at + 3), bq = st.t > tb0 ? ((st.t - tb0) % 6.5) / 1.6 : 2;   // anlatımdan sonra her 6,5 sn'de bir tarama bandı
    SET.monitorIci(B, 130, 120, 420, 300, (B2) => { const K = bodrum(B2, st, { acik: (yan, i) => yan > 0 && i === 1, isik });
      esikGardiyan(B2, K, A('F04@biri') - A('F04') + 3, st.t, { bas: .18 + Math.sin(st.t * .5) * .03, don });
      if (bq < 1) { const g = B2.k; g.save(); g.fillStyle = B2.ton(0, .6); g.fillRect(-200, lerp(-200, 1280, bq) - 100, 2400, 200); g.restore(); } });
    // masa: koyu kütle; ışık havuzu yalnız sol yarıda, alt üçte bire inmeden söner
    k.save(); k.fillStyle = B.ton(.9); k.fillRect(-900, my, 3400, 1000);
    const g = k.createRadialGradient(600, my + 20, 20, 600, my + 20, 270); g.addColorStop(0, B.ton(.1)); g.addColorStop(.5, B.ton(.5)); g.addColorStop(1, B.ton(.9, 0));
    k.fillStyle = g; k.fillRect(-900, my, 3400, 380);
    k.fillStyle = '#fff'; for (const [a0, a1] of [[180, 420], [440, 760], [780, 860]]) k.fillRect(a0, my - 3, a1 - a0, 5); k.restore();
    SET.surtme(B.k, 260, 860, my + 14, 21, { n: 22, boy: 70, acik: false });
    // teyp ışıkta (küçük): bant bitmiş, makaralar durur; "sonrakini"nde kayıt lambası yanar, makaralar yavaşça hızlanıp sona kadar döner
    const ts = A('F05@sonrakini'), lam = R(st, 'F05@sonrakini', .25);
    const d = Math.max(0, st.t - ts), ang = 1.3 + TAU * .45 * (d < 1.2 ? d * d / 2.4 : d - .6);   // 1,2 sn'de .45 tur/sn'ye çıkar
    SET.teyp(B, 700, my - 146, .4, st.t, { ang, kayit: lam > 0 ? (.55 + .45 * lam) : 0, vu: lam > 0 ? lam * (.35 + .3 * Math.abs(Math.sin(st.t * 5.3) * Math.sin(st.t * 2.1))) : .02, vuIsik: lerp(.35, .75, lam), ...DOLU });
    // aynalı gözlük masada, monitörün önünde; "peki"de camda parıltı kayar, "abone"de ağır ağır geri döner
    const kay = R(st, 'F05@peki', 2.4, E.io2) - .5 * R(st, 'F05@abone', 6, E.io2);
    gozluk(B, 450, my + 78, 1.35, kay);
  }, KK);
})();
