// IV. İki gardiyan (E01–E14): iki monitör (gündüz ↔ gece) → Eshelman: 1971 son gün, 2011, gece koridoru, Zimbardo'nun övgüsü, pişmanlık, Zimbardo 2018, 2024 →
//   iki belge yan yana → Mark: gündüz sayımı, dolap, 2011, karlanan monitör, dökümdeki itirazlar → Zimbardo 2018 "hiçbiri araya girmedi" → gece koridoru ↔ gözlem odası.
// Bodrum yalnız monitörde (VID). Karanlık oda ve gözlem odası: kâğıt + kuru fırça (.6). Belge ve dergi sayfası: kâğıt, kuru yok.
// Renk yalnız teybin kehribar ışığında, kırmızı kayıt lambasında ve belgedeki kehribar vurgu şeridinde. Yüz yok; gardiyanın tek yüz öğesi aynalı gözlük.
// Gece: koridor ton plakasında çarpımla karartılır (tek lambalı sorgu mizanseni yok: kararma geniş, kişilerin üstünde ışık havuzu yok).
// Yazı levhası ≤ 8 sn (kanal kuralı): dergi ve belge sayfaları sözden hemen önce kadraja kayar (giris), plan sonuna en çok ~7,8 sn kalır; boş sayfa ≤ 1 sn.
// a.js'deki VID, KAG, bodrum(), yakinFig(), BODRUM_GAIT kullanılır. Bütün adlar bu kapsamın içinde (aynı sayfada beş sahne dosyası).
(() => {
  'use strict';
  const KK = { baski: { mod: 'kagit', kuru: .6 } };
  const ZUST = 'ZIMBARDO · PRISONEXP.ORG · HAZİRAN 2018';
  const SMK = 'Stanford Magazine, Temmuz/Ağustos 2011 (çevirisi bizim)';
  // üst katman: film zamanında bir çapadan başlar, d sn sonra söner (ekran yazısı ≤ 8 sn); içteki yazı lt'sini çapadan sayar
  const ZM = (f, at, d = 8) => (ctx, st) => {
    const t0 = (at == null ? st.at : typeof at === 'string' ? A(at) : at) - st.at, lt = st.lt - t0;
    if (lt < 0) return; const a = clamp((d - lt) / .5); if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a; f(ctx, { ...st, lt }); ctx.restore();
  };
  const R = (st, at, d = .6, e) => ramp(st.t, A(at), A(at) + d, e);   // sözcüğe bağlı geçiş 0→1
  // sayfanın kadraja girişi: sözden .45 sn önce yerine oturur, ama plan sonuna en çok son sn kalır (levha ≤ 8 sn); p kayma 0→1, cek tutan elin çekilmesi 0→1
  const GEC = .9;
  function giris(st, at, son = 7) {
    const tA = Math.max(A(at) - .45, st.end - son), t0 = tA - GEC;
    return { p: E.out3(clamp((st.t - t0) / GEC)), cek: E.in2(clamp((st.t - tA - .15) / .6)), tA };
  }
  // gözlem odası: kollar dirsekten bükük, önkol masada yatay (c.js ile aynı)
  const KOL = { kolO: [.45, 1.1], kolA: [.35, 1.18] };
  const oda = (B, st, o = {}) => SET.gozlemOdasi(B, st, { ...o, mudurO: { ...KOL, ...(o.mudurO || {}) }, markO: { ...KOL, ...(o.markO || {}) } });
  // koridorda kişi (z derinlik, u yan)
  const kisiK = (B, K, z, u, tip, oo = {}) => { const p = K.yer(z, u), s = K.olc(z); return FIG.kisi(B.l, p[0], p[1], 700 * s * (oo.boyK || 1), { tip, ...oo }); };
  // gece: ton plakası çarpımla kararır (geniş, yumuşak; kişilerin üstünde ışık havuzu değil)
  function gece(B, cx = 960, cy = 480, r0 = 300, r1 = 1150, d = .8) {
    const k = B.k; k.save(); k.globalCompositeOperation = 'multiply';
    const g = k.createRadialGradient(cx, cy, r0, cx, cy, r1); g.addColorStop(0, B.ton(.5)); g.addColorStop(1, B.ton(d));
    k.fillStyle = g; k.fillRect(-600, -600, W + 1200, H + 1200); k.restore();
  }
  // karanlık odada monitörün çevresine düşen soluk ışık (kâğıtta açık yıkama); başların yanında kullanılmaz
  function hale0(B, x, y, r, a = .45) {
    const k = B.k, g = k.createRadialGradient(x, y, r * .15, x, y, r); g.addColorStop(0, `rgba(255,255,255,${a})`); g.addColorStop(1, 'rgba(255,255,255,0)');
    k.save(); k.fillStyle = g; k.fillRect(x - r, y - r, 2 * r, 2 * r); k.restore();
  }
  // karanlık odada masa: koyu kütle, kırık açık üst kenar, çizgi plakasında koyu alt
  function masa(B, my, kenar = [[200, 520], [560, 1010], [1040, 1380], [1410, 1720]]) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = B.ton(.9); k.fillRect(-600, my, W + 1200, 900); k.fillStyle = '#fff'; for (const [a, b] of kenar) k.fillRect(a, my - 2, b - a, 7); k.restore();
    l.save(); l.fillStyle = '#000'; l.fillRect(-600, my + 26, W + 1200, 900); l.restore();
  }
  // iki monitör (gündüz solda, gece sağda) karanlık odada; gun(B2), gec(B2) monitör içini çizer (P65, P80)
  function ikiMonitor(B, gun, gec) {
    SET.karanlik(B, .82);
    hale0(B, 530, 450, 520, .22); hale0(B, 1390, 450, 520, .14);
    masa(B, 800, [[120, 460], [500, 900], [1000, 1460], [1500, 1800]]);
    SET.monitorIci(B, 180, 220, 700, 460, gun);
    SET.monitorIci(B, 1040, 220, 700, 460, gec);
  }
  // elde tutan el (yakın; dolgun avuç, kısa kalın başparmak): (x, y) sayfanın ALT kenarındaki tutma noktası, s ölçek, f 1 kol sol alttan / -1 sağ alttan gelir.
  //   Önkol kadrajın altından çapraz girer; avuç alt kenarın altında, parmaklar sayfanın arkasında; yalnız başparmak sayfanın önüne kıvrılır (açık parmak yok)
  function tutan(g, x, y, s = 1, f = 1) {
    g.save(); g.translate(x, y); g.scale(f * s, s); g.fillStyle = '#000';
    g.beginPath(); g.moveTo(-250, 760); g.lineTo(-62, 40); g.quadraticCurveTo(-20, 0, 40, 30); g.lineTo(-110, 790); g.closePath(); g.fill();   // önkol (kol ağzı geniş)
    g.beginPath(); g.ellipse(-6, 34, 62, 50, -.25, 0, TAU); g.fill();   // avuç: alt kenarın altında, parmaklar sayfanın arkasında
    g.beginPath(); g.moveTo(-34, 14); g.quadraticCurveTo(-22, -34, 6, -52); g.quadraticCurveTo(30, -62, 38, -42); g.quadraticCurveTo(36, -14, 18, 16); g.closePath(); g.fill();   // başparmak: sayfanın önünde, içe eğik
    g.restore();
  }
  // Stanford Magazine sayfası (canlandırma; logo ve sayfa düzeni kopyalanmaz): üstte dergi ve tarih, makalenin adı, italik alıntı satırları
  //   vurgu: [{i, s}] satır i'de s alt dizgisi (yoksa bütün satır) kehribar şeritle; şerit yalnız yazılmış harflerin üstüne açılır
  function dergi(B, kim, satirlar, p, o = {}) {
    const k = B.k, l = B.l, x = o.x ?? 320, y = o.y ?? 120, w = o.w ?? 1280, px = o.px ?? 60, lh = px * 1.32, h = o.h ?? (300 + satirlar.length * lh + 40);
    k.save(); k.fillStyle = B.ton(o.zemin ?? .4); k.fillRect(-600, -600, W + 1200, H + 1200); k.restore();
    if (x > W + 40) return { x, y, w, h, lh };
    k.save(); k.fillStyle = B.ton(.62); k.fillRect(x + 14, y + 16, w, h); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
    l.save(); l.strokeStyle = '#000'; l.fillStyle = '#000'; l.lineWidth = 1.6; l.strokeRect(x, y, w, h);
    l.font = '700 26px "Courier Prime"'; l.textBaseline = 'middle'; l.textAlign = 'left'; l.fillText(o.yayin || 'STANFORD MAGAZINE · TEMMUZ/AĞUSTOS 2011', x + 70, y + 58);
    l.textAlign = 'right'; l.fillText(kim, x + w - 70, y + 58); l.textAlign = 'left';
    l.font = 'italic 600 80px "Cormorant Garamond"'; l.fillText(o.baslik || 'The Menace Within', x + 66, y + 146);
    l.lineWidth = 2; l.beginPath(); l.moveTo(x + 70, y + 204); l.lineTo(x + w - 70, y + 204); l.stroke();
    l.font = `italic 600 ${px}px "Cormorant Garamond"`;
    const top = satirlar.reduce((a, r) => a + r.length, 0); let kalan = Math.floor(top * clamp(p));
    satirlar.forEach((r, i) => {
      const yy = y + 290 + i * lh, n = Math.max(0, Math.min(r.length, kalan));
      for (const v of (o.vurgu || [])) if (v.i === i && (v.a ?? 1) > 0) {
        const j = v.s ? Math.max(0, r.indexOf(v.s)) : 0, sLen = (v.s || r).length, yaz = clamp((n - j) / sLen);
        if (yaz <= 0) continue;
        const x0 = l.measureText(r.slice(0, j)).width, tw = l.measureText(v.s || r).width;
        B.renkBoya(g => g.rect(x + 70 + x0 - 14, yy - px * .56, (tw + 28) * Math.min(clamp(v.a ?? 1), yaz), px * 1.12), .6, 0);
      }
      l.fillText(r.slice(0, n), x + 70, yy); kalan -= r.length;
    });
    l.restore();
    return { x, y, w, h, lh };
  }
  // elde tutulan belge kartı (P74): başlık, çizgi, italik alıntı; vurgu satırı kehribar
  function kart(B, x, y, w, h, bas, sat, o = {}) {
    const k = B.k, l = B.l, px = o.px || 62;
    k.save(); k.fillStyle = B.ton(.66); k.fillRect(x + 16, y + 18, w, h); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
    l.save(); l.fillStyle = '#fff'; l.fillRect(x, y, w, h); l.strokeStyle = '#000'; l.lineWidth = 2; l.strokeRect(x, y, w, h);
    l.fillStyle = '#000'; l.font = '700 32px "Courier Prime"'; l.textBaseline = 'middle'; l.textAlign = 'left'; l.fillText(bas, x + 50, y + 62);
    l.lineWidth = 1.6; l.beginPath(); l.moveTo(x + 50, y + 100); l.lineTo(x + w - 50, y + 100); l.stroke();
    l.font = `italic 600 ${px}px "Cormorant Garamond"`;
    sat.forEach((s, i) => { const yy = y + 196 + i * px * 1.3;
      if (o.vurgu === i && (o.va || 0) > 0) { const tw = l.measureText(s).width; B.renkBoya(g => g.rect(x + 36, yy - px * .56, (tw + 28) * clamp(o.va), px * 1.12), .6, 0); }
      l.fillText(s, x + 50, yy); });
    l.restore();
  }
  // kahve fincanı (gözlem odası masasında; çalışma odası işareti): (x, y masa üstü), s ölçek, f kulp yönü; buhar tohumlu, ince, yukarı akar
  function fincan(B, x, y, s, f, t) {
    const l = B.l, k = B.k;
    l.save(); l.fillStyle = '#000'; l.beginPath(); l.moveTo(x - 24 * s, y - 58 * s); l.lineTo(x + 24 * s, y - 58 * s); l.lineTo(x + 21 * s, y); l.lineTo(x - 21 * s, y); l.closePath(); l.fill();
    l.strokeStyle = '#000'; l.lineWidth = 7 * s; l.beginPath(); l.ellipse(x + f * 27 * s, y - 32 * s, 11 * s, 15 * s, 0, -PI / 2, PI / 2, f < 0); l.stroke(); l.restore();
    k.save(); k.strokeStyle = 'rgba(255,255,255,.5)'; k.lineWidth = 2.5 * s; k.lineCap = 'round';
    for (let i = 0; i < 2; i++) { const u = ((t * .35 + i * .5) % 1), yy = y - 70 * s - u * 90 * s; k.globalAlpha = Math.sin(u * PI) * .8;
      k.beginPath(); k.moveTo(x - 6 * s + i * 10 * s, yy); k.bezierCurveTo(x + 10 * s, yy - 20 * s, x - 14 * s, yy - 36 * s, x + 4 * s + i * 6 * s, yy - 52 * s); k.stroke(); }
    k.restore();
  }

  // P65 orta: karanlık oda, iki monitör yan yana (solda gündüz sayımı, kahraman kapının dışında; sağda gece koridoru, gardiyan yürür ve mahkûmun önünde durur).
  //   "sertlik"te kamera gece monitörüne kayar, "bodrumdaki"nde gündüz monitörüne döner
  sahne('P65', 'E01', 'monitor2', 'orta', (B, st) => {
    const s1 = R(st, 'E01@sertlik', 1.3, E.io2), s2 = R(st, 'E01@bodrumdaki', 1.6, E.io2);
    B.cam(lerp(lerp(960, 1240, s1), 700, s2), 470, 1.02 + .1 * s1 + .06 * s2 + st.lt * .005);
    ikiMonitor(B, (B2) => bodrum(B2, st, { sayim: 4, gardiyanlar: [{ z: .32, u: .12, kol: [.1, .4] }], kose: { z: .5, u: .86 } }), (B2) => {
      const K = bodrum(B2, st, { isik: .3, levha: false });
      kisiK(B2, K, .36, -.3, 'mahkum', { f: 1, bas: .2, kolO: [-.05, .1], kolA: [-.06, .12] });
      const zy = K.yer(.3, 0)[1], boy = 700 * K.olc(.3), v = BODRUM_GAIT.hiz * boy / 100 * 1.05, tS = A('E01@sertlik') - st.at + .5;
      SET.yuru(B2.l, 900 + v * tS, zy, boy, st.lt, { tip: 'gardiyan', f: -1, go: u => u < tS ? 1 : 0, kolO: [.15, .4], kolA: [-.1, .3] });
      gece(B2, 960, 470);
    });
  }, { ...KK, over: OV(ZM(ETK('GÜNDÜZ VARDİYASI', 530, 150, { d: 3.6, px: 40 }), null, 4), ZM(ETK('GECE VARDİYASI', 1390, 150, { d: 3.6, px: 40 }), null, 4)) });

  // P66 yakın: Eshelman profil (gece). Arkada (sırtının gerisinde, başın yanında değil) bir kapı aralığının ışık şeridi.
  //   "müdüre"de kapı aralanır, şerit genişler; "aktördüm"de gözlükte parıltı çakar, baş kalkar; "abartıyordum"da kapı kapanır, şerit söner; "rol"de baş ve omuz düşer
  sahne('P66', 'E02', 'gece', 'yakin', (B, st) => {
    const ac = R(st, 'E02@müdüre', 1.2, E.io2), kap = R(st, 'E02@abartıyordum', 1.4, E.io2), don = R(st, 'E02@aktördüm', .9), rol = R(st, 'E02@rol', .9, E.io2);
    const cak = ramp(st.t, A('E02@aktördüm'), A('E02@aktördüm') + .25) * (1 - ramp(st.t, A('E02@aktördüm') + .5, A('E02@aktördüm') + 1.6));
    B.cam(lerp(960, 920, rol), 540, 1.02 + st.lt * .018);
    const k = B.k, sw = 40 + 150 * ac * (1 - kap) + 8 * Math.sin(st.t * 2.3);
    k.save(); k.fillStyle = B.ton(.84); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.3); k.fillRect(110, -300, sw, 1700); k.fillStyle = B.ton(.62); k.fillRect(110 + sw, -300, 30, 1700); k.restore();
    const gri = Math.round(lerp(150, 248, cak)), par = `rgb(${gri},${gri + 4},${gri + 6})`;
    yakinFig(B, 'gardiyan', 620, 360 + 24 * rol, 2300, { f: 1, bas: .14 - .16 * don + .16 * rol, govde: .05 * rol + Math.sin(st.t * 1.1) * .008, cop: false, kolO: [.2, .4], kolA: [-.1, .2], camRenk: '#6A7275', parilti: par, serbest: 1 });   // cam koyu; parıltı küçük
  }, { ...VID, over: ZM(QT('“Çalışma için daha iyi olur diye düşündüm. Deney boyunca bir aktördüm, abartıyordum; rol yapıyordum.”', 'Eshelman, deneyin son günü (Le Texier 2019, s. 8)', { video: 1, x: 1330, y: 360, maxW: 820, px: 62 }), 'E02@çalışma', 8) });

  // P67 kart: Stanford Magazine 2011 sayfası; bir el sayfayı sağdan masaya sürer ve çekilir, alıntı sözle yazılır;
  //   "zorladım"da şerit, "araştırmacıların"da kamera satıra iner
  sahne('P67', 'E03@planlıydı', 'dergi', 'kart', (B, st) => {
    const gr = giris(st, 'E03@planlıydı'), in1 = R(st, 'E03@araştırmacıların', 2, E.io2);
    B.cam(960, lerp(470, 540, in1), 1.02 + .06 * in1 + st.lt * .008);
    const x = lerp(2100, 320, gr.p), p0 = Math.max(A('E03@planlıydı') - .3, gr.tA), p = clamp((st.t - p0) / Math.max(2, A('E03@istedim') - p0));
    const d = dergi(B, 'ESHELMAN', ['“Planlıydı. Olayları zorladım;', 'araştırmacıların elinde çalışacak', 'bir şey olsun istedim.”'], p, { x, vurgu: [{ i: 0, s: 'Olayları zorladım;', a: R(st, 'E03@zorladım', 1, E.lin) }] });
    if (gr.cek < 1) tutan(B.l, x + d.w - 150 + gr.cek * 700, d.y + d.h + gr.cek * 500, 1.1, -1);
  }, { ...KAG, over: ZM(KU(SMK), 'E03@planlıydı', 8) });

  // P68 geniş: gece koridoru; Eshelman numaralı bir mahkûmun önünde, arkada iki gardiyan kıpırdamadan duruyor.
  //   "eziyete"de Eshelman (eller arkada) bir adım yaklaşıp mahkûmun üstüne eğilir (dokunma, uzanma yok); "kes"te mahkûm başını ve omzunu düşürür; "öteki"nde kamera arkadaki iki gardiyana kayar
  sahne('P68', 'E04', 'gece', 'genis', (B, st) => {
    const ot = R(st, 'E04@öteki', 2.2, E.io2), gir = E.io2(clamp(st.lt / 3));
    B.cam(lerp(lerp(860, 900, gir), 1130, ot), lerp(lerp(600, 580, gir), 500, ot), 1.08 + .1 * gir + .1 * ot + st.lt * .004);
    const K = bodrum(B, st, { isik: .35, levha: false, gardiyanlar: [{ z: .58, u: .5, f: -1, kol: [.1, .45], bas: .04 }, { z: .65, u: .76, f: -1, kol: [-.05, .2], bas: 0 }] });
    const ez = R(st, 'E04@eziyete', .8), ks = R(st, 'E04@kes', .8);
    kisiK(B, K, .3, -.3, 'mahkum', { f: 1, numara: '1037', onlukRenk: '#666864', bas: .16 + .16 * ks, govde: .04 + .07 * ks, kolO: [-.05, .1], kolA: [-.06, .12] });
    kisiK(B, K, .27, lerp(.1, .03, ez), 'gardiyan', { f: -1, govde: .14 * ez, kolO: [-.3, .55], kolA: [-.35, .6], bas: .02 - .08 * ez + Math.sin(st.t * .9) * .015, serbest: 1 });   // eller arkada: dokunma yok, yalnız yaklaşıp eğilir
    gece(B, 960, 470);
  }, { ...VID, over: ZM(QT('“Öteki gardiyanlar beni durdurmadı. Tek bir gardiyan bile \'bence bunu yapmamalıyız\' demedi.”', 'Stanford Magazine, 2011', { video: 1, y: 170, maxW: 1400 }), 'E04@öteki', 8) });

  // P69 orta: koridor (gündüz ışığı); takım elbiseli siluet (Zimbardo) soldan yürür, Eshelman'ın karşısında durur;
  //   "iyi"de el sıkışırlar (iki önkol bel hizasında buluşur), "hissediyor"da eller ayrılır, Eshelman göğsünü kabartıp başını kaldırır
  sahne('P69', 'E05', 'koridor', 'orta', (B, st) => {
    const K = bodrum(B, st, { levha: false });
    const zy = K.yer(.15, 0)[1], boy = 700 * K.olc(.15), v = BODRUM_GAIT.hiz * boy / 100 * 1.05, s = boy / 100;
    const xE = 1300, x1 = xE - 44 * s, tA = A('E05@yanına') - st.at + .9, x0 = Math.max(x1 - v * tA, 300), tS = tA - (x1 - x0) / v;
    const iyi = R(st, 'E05@iyi', .7, E.io2) * (1 - R(st, 'E05@hissediyor', .9, E.io2)), his = R(st, 'E05@hissediyor', 1);
    B.cam(lerp(1060, 1150, clamp(st.lt / 4)) + st.lt * 4, zy - boy * .6, 1.7 + st.lt * .012);
    FIG.kisi(B.l, xE, zy, boy, { tip: 'gardiyan', f: -1, kolO: [lerp(.12, .5, iyi), lerp(.45, 1.07, iyi)], kolA: [-.1, .3], govde: -.05 * his, bas: .14 - .24 * his + Math.sin(st.t * .8) * .015, serbest: 1 });
    SET.yuru(B.l, x0, zy, boy * 1.02, st.lt, { tip: 'takim', f: 1, go: u => (u >= tS && u < tA) ? 1 : 0, kolO: [lerp(.15, .5, iyi), lerp(.3, 1.07, iyi)], kolA: [.1, .3], serbest: 1 });
  }, { ...VID, mb: 4, over: ZM(KU("Eshelman'ın anlatımı (Blum 2018)", { video: 1 }), null, 8) });

  // P70 kart: Stanford Magazine 2011, pişmanlık; sayfa elle sürülür, "kesinlikle"de şerit, "buna"da kamera son satıra
  sahne('P70', 'E06@kimseye', 'dergi', 'kart', (B, st) => {
    const gr = giris(st, 'E06@kimseye'), in1 = R(st, 'E06@buna', 1.8, E.io2);
    B.cam(lerp(960, 900, in1), lerp(470, 560, in1), 1.02 + .12 * in1 + st.lt * .006);
    const x = lerp(2100, 320, gr.p), p0 = Math.max(A('E06@kimseye') - .3, gr.tA), p = clamp((st.t - p0) / Math.max(2, A('E06@pişmanım') - p0));
    const d = dergi(B, 'ESHELMAN', ['“Kimseye zarar verip vermediğimi', 'düşünmeden korkutmayı artırdım.', 'Buna kesinlikle pişmanım.”'], p, { x, vurgu: [{ i: 2, s: 'kesinlikle pişmanım.”', a: R(st, 'E06@kesinlikle', 1, E.lin) }] });
    if (gr.cek < 1) tutan(B.l, x + d.w - 150 + gr.cek * 700, d.y + d.h + gr.cek * 500, 1.1, -1);
  }, { ...KAG, over: ZM(KU(SMK), 'E06@kimseye', 8) });

  // P71a orta (rev3): karanlık masada kayıt monitörü; ekranda yalnız gren ve tarama bandı (olayın kendisi gösterilmez), köşede "5. GECE";
  //   kırmızı kayıt lambası yanar, sayaç "beşinci"de başlar ve "dakikaya"da 09:5x'e varır (sayı soldan sağa doğru akar, ara karede yanlış rakam yok: sayaç gerçek zaman)
  sahne('P71a', 'E07', 'monitor', 'orta', (B, st) => {
    B.cam(960, 480, 1.03 + st.lt * .014);
    SET.karanlik(B, .86);
    hale0(B, 960, 460, 700, .2);
    masa(B, 860, [[160, 640], [700, 1220], [1280, 1760]]);
    const t0 = A('E07@beşinci'), t1 = A('E07@dakikaya'), u = clamp((st.t - t0) / Math.max(1, t1 - t0));
    SET.monitorIci(B, 420, 150, 1080, 600, () => {
      const k = B.k, r = rng(3 + Math.floor(st.t * 15));
      k.save(); k.fillStyle = B.ton(.55); k.fillRect(-100, -100, 2120, 1300);
      for (let i = 0; i < 900; i++) { k.fillStyle = r() < .5 ? B.ton(.3) : B.ton(.75); k.fillRect(r() * 1920, r() * 1080, 6 + r() * 20, 3 + r() * 4); }
      k.restore();
    });
    if (st.t > t0 - .2) B.renkBoya(g => g.arc(1440, 200, 14, 0, TAU), .9 * (.6 + .4 * (Math.sin(st.t * 6) > 0 ? 1 : 0)), 1);
  }, { baski: st => ({ mod: 'kagit', kuru: .6, bant: [((st.lt * .25) % 1.25) - .12, .9] }),
    over: OV((ctx, st) => { const t0 = A('E07@beşinci'), t1 = A('E07@dakikaya'); if (st.t < t0 - .3) return;
      const sn = Math.floor(clamp((st.t - t0) / Math.max(1, t1 - t0)) * 590), s = 'KAYIT  ' + String(Math.floor(sn / 60)).padStart(2, '0') + ':' + String(sn % 60).padStart(2, '0');
      etiket(ctx, '5. GECE', 620, 230, st.t - t0 + .3, 99, { px: 44, col: '#E9EEF0', panelRGB: KOYU });
      etiket(ctx, s, 1300, 690, st.t - t0 + .3, 99, { px: 44, col: '#E9EEF0', panelRGB: KOYU }); },
      ZM(KU('Zimbardo 2018, prisonexp.org: kayıt on dakikaya yakın (olay gösterilmez)', { y: 120, x: 160, align: 'left' }), 'E07@beşinci', 6)) });

  // P71 ayrıntı: Zimbardo 2018 metni sağdan kayarak gelir, tek alıntı; "sert"te şerit, "ötesinde"de kamera satıra yaklaşır
  //   (yaklaşma sağ kenarda ≥ 150 px pay bırakır: TV taşma payı)
  sahne('P71', 'E07@ona', 'z2018', 'ayrinti', (B, st) => {
    const gr = giris(st, 'E07@ona'), ot = R(st, 'E07@ötesinde', 1.6, E.io2);
    B.cam(lerp(840, 870, ot), 452, 1.42 + .1 * ot + st.lt * .008);
    const x = lerp(2100, 310, gr.p);
    SET.belge(B, ZUST, ['[...] bu tür davranışlar,', 'sert gardiyanı oynamanın çok', 'ötesine geçiyor.'], clamp((st.t - gr.tA) / 2.2), { x, px: 46, w: 1300, y: 220, vurgu: [1], vurguA: R(st, 'E07@sert', 1.3, E.lin), zemin: .38 });
  }, { ...KAG, over: ZM(KU('Zimbardo 2018, prisonexp.org (çevirisi bizim)'), null, 8) });

  // P72a kart (rev3): Eshelman 2018, dergi sayfası sağdan kayar (Blum'un söyleşisi); "inandığını"da şerit
  sahne('P72a', 'E08', 'dergi', 'kart', (B, st) => {
    const gr = giris(st, 'E08');
    B.cam(960, 500, 1.02 + st.lt * .01);
    const x = lerp(2100, 320, gr.p), p = clamp((st.t - Math.max(A('E08') - .3, gr.tA)) / Math.max(2, A('E08@zimbardo') - A('E08') - .6));
    const d = dergi(B, 'ESHELMAN', ['“Araştırmacıların istediğini', 'yaptığıma inanıyordum.”'], p, { x, yayin: 'MEDIUM · 7 HAZİRAN 2018 · B. BLUM', baslik: 'The Lifespan of a Lie', vurgu: [{ i: 1, s: 'inanıyordum.”', a: R(st, 'E08@inandığını', 1, E.lin) }] });
    if (gr.cek < 1) tutan(B.l, x + d.w - 150 + gr.cek * 700, d.y + d.h + gr.cek * 500, 1.1, -1);
  }, { ...KAG, over: ZM(KU('Blum 2018, Medium (çevirisi bizim)'), 'E08', 6) });

  // P72 kart: koyu zeminde tek satır tarih; harfler yazılır, "öldü"de altına ince çizgi çekilir
  // P72 (başkan, levha bütçesi): düz tarih levhası yerine karanlık büroda boş sandalye, koninin kenarında; tarih küçük etiket
  sahne('P72', 'E08@zimbardo', 'sandalye', 'yakin', (B, st) => {
    B.cam(980, 560, 1.06 + Math.min(st.lt, 8) * .02);
    SET.karanlik(B, .82); SET.koni(B, 1180, -100, 120, 980, 620, { a: .5 * R(st, 'E08@öldü', 1.2, E.lin) + .25, tohum: 8 });
    const l = B.l; l.save(); l.fillStyle = '#000';
    l.beginPath(); l.moveTo(900, 520); l.quadraticCurveTo(880, 610, 905, 700); l.lineTo(930, 700); l.quadraticCurveTo(908, 610, 926, 520); l.closePath(); l.fill(); l.fillRect(900, 700, 260, 26); l.fillRect(1134, 700, 26, 280); l.fillRect(904, 700, 22, 280);   // boş sandalye (yan görünüş; sırt tek eğri dikme: üst yatay çubuk yok, ters L / darağacı okunmasın)
    l.restore();
  }, { baski: { mod: 'kagit', kuru: .6 }, over: ETK('14 EKİM 2024', 960, 200, { t0: .3, d: 99, px: 52 }) });

  // P73 orta: karanlık odada televizyon; belgesel görüntüsü: yan ışıklı duvar önünde oturan yaşlı siluet (yüz yok).
  //   rev3: ekranda söyleşi sayfası (kişi yok); "davranışlarımın"da kamera ekrana yaklaşır ve sözün satırı koyulaşır
  sahne('P73', 'E08@birkaç', 'tv', 'orta', (B, st) => {
    const yak = R(st, 'E08@davranışlarımın', 2.6, E.io2);
    B.cam(lerp(960, 760, yak), lerp(480, 460, yak), 1.02 + .1 * yak + st.lt * .006);
    SET.karanlik(B, .84);
    hale0(B, 580, 460, 620, .24);
    masa(B, 830, [[110, 470], [510, 1000], [1050, 1400]]);
    SET.monitorIci(B, 150, 190, 860, 520, () => {
      const k = B.k;
      // rev3: ekranda yayımlanmış söyleşi sayfası (sözün belgeselin içinde değil, tanıtım söyleşisinde geçtiği: Fable E2); kişi çizilmez
      k.fillStyle = B.ton(.9); k.fillRect(-100, -100, 2120, 1300);
      k.fillStyle = B.ton(.25); k.fillRect(160, 120, 1600, 70);
      const vy = R(st, 'E08@davranışlarımın', .9, E.io2);
      for (let i = 0; i < 9; i++) { const y = 290 + i * 78, w = i % 3 === 2 ? 1100 : 1500; k.fillStyle = B.ton(i === 5 ? lerp(.62, .2, vy) : .62); k.fillRect(200, y, w, i === 5 ? 34 : 22); }
      k.fillStyle = B.ton(.4); k.fillRect(200, 220 - 40 * R(st, 'E08@birkaç', 1.5, E.io2), 4, 4);
    });
  }, { ...KK, over: OV(ZM(ETK('KASIM 2024', 580, 130, { d: 5.5 }), null, 6), ZM(QT('“Davranışlarımın birçoğunu o yönlendirdi.”', null, { x: 1490, y: 430, maxW: 560, px: 64 }), 'E08@davranışlarımın', 7.5),
    ZM(KU('Eshelman, belgeselin tanıtım söyleşisi (Laughing Place, 12.11.2024)'), 'E08@davranışlarımın', 7.5)) });

  // P74 yakın: iki el iki belgeyi kameraya uzatır (eşit boy): sol Eshelman 2024 (plan başında girer), sağ Zimbardo 2018 ("istenenin"den hemen önce girer);
  //   "istendi" ve "ötesiydi"de ilgili satır şeritlenir, "ikisi"nde iki belge birlikte öne gelir. Eller dolgun avuç + başparmak (tutan)
  sahne('P74', 'E09', 'iki_belge', 'yakin', (B, st) => {
    const ik = R(st, 'E09@ikisi', 1.2, E.io2);
    B.cam(960, 500, 1.0 + .07 * ik + st.lt * .008);
    const k = B.k; k.save(); k.fillStyle = B.ton(.42); k.fillRect(-300, -300, 2600, 1700); k.restore();
    const gL = ramp(st.lt, 0, .8, E.out3), gR = R(st, 'E09@istenenin-0.7', .8, E.out3), y = 140 + Math.sin(st.t * 1.1) * 4;
    const xL = lerp(-760, 230, gL), xR = lerp(1960, 1050, gR), w = 640, h = 560;
    kart(B, xL, y, w, h, 'ESHELMAN · 2024', ['“Davranışlarımın', 'birçoğunu o', 'yönlendirdi.”'], { vurgu: 2, va: R(st, 'E09@istendi', .9, E.lin) });
    tutan(B.l, xL + 120, y + h - 6, 1, 1);
    if (gR > 0) { kart(B, xR, y - 6, w, h, 'ZIMBARDO · 2018', ['“…sert gardiyanı', 'oynamanın çok', 'ötesine geçiyor.”'], { vurgu: 2, va: R(st, 'E09@ötesiydi', .9, E.lin) });
      tutan(B.l, xR + w - 120, y - 12 + h, 1, -1); }
  }, { ...KAG, over: ZM(KU('Laughing Place, 12.11.2024 · Zimbardo, prisonexp.org, Haziran 2018 (çevirileri bizim)', { y: 84 }), null, 8) });   // künye üstte: eller alttan girer

  // P75 geniş: gündüz sayımı (A01'in geri çağrısı); dört mahkûm sol duvarda aralıklı (numaralar birbirine binmez, en uzaktaki numarasız),
  //   gardiyan sayım tahtasıyla yürüyerek sayar; kahraman sağ duvarın dibinde ayakta, kenarda; "markın"da kamera ona yaklaşır, "kimse"de başını eğer
  sahne('P75', 'E10', 'koridor', 'genis', (B, st) => {
    const yk = R(st, 'E10@markın', 3, E.io2);
    B.cam(lerp(960, 1170, yk), lerp(560, 600, yk), 1 + .24 * yk + st.lt * .004);
    const K = bodrum(B, st, { levha: false }), t = st.t;
    const sira = [[.68, -.73, '', .02, [.25, .9]], [.52, -.76, '', -.03, [-.05, .1]], [.33, -.6, '5704', .05, [-.2, .35]], [.14, -.75, '2093', 0, [-.05, .1]]];   // numara yalnız öndeki ikide
    sira.forEach(([z, u, no, b, kol], i) => kisiK(B, K, z, u, 'mahkum', { f: 1, numara: no, boyK: [1.02, .95, 1, .97][i], kolO: kol, kolA: [.05, .25], bas: b + Math.sin(t * .7 + i) * .03, govde: [.02, -.03, .04, 0][i] }));
    { const z = .3, s = K.olc(z), p0 = K.yer(z, 0), vv = 30, x = 520 + vv * st.lt, fz = BODRUM_GAIT.poz(st.lt * vv / (BODRUM_GAIT.hiz * 7.35 * s) / BODRUM_GAIT.tur, 1);
      FIG.kisi(B.l, x, p0[1], 700 * s, { tip: 'gardiyan', f: 1, bacak: fz, cop: false, kolO: [.95, 1.05], kolA: [-.1, .3], bas: .12,
        el: { on: (gg, e) => { gg.save(); gg.translate(e.e[0], e.e[1]); gg.rotate(-.3); gg.fillRect(-2, -9, 11, 14); gg.restore(); } } }); }   // sayım tahtası
    const ks = R(st, 'E10@kimse', 1);
    kisiK(B, K, .46, .84, 'gardiyan', { f: -1, cop: false, kolO: [.15, .5], kolA: [-.1, .3], bas: .08 + .12 * ks + Math.sin(st.t * .6) * .02 });
  }, { ...VID, over: ZM(QT('“Benim çalıştığım gündüz vardiyasında kimse, böyle bir durumda beklenenin ötesine geçmedi.”', 'Stanford Magazine, 2011', { video: 1, y: 180, maxW: 1300 }), 'E10@benim', 8) });

  // P76 yakın: dolap kapısı (karanlık hücre) kapanır; "kapattıklarında"da kanat menteşede döner ve oturur, "hiç"te kilitlenirken sarsılır
  sahne('P76', 'E10@birini', 'dolap', 'yakin', (B, st) => {
    B.cam(960, 540, 1.04 + st.lt * .02);
    const k = B.k, l = B.l, kp = R(st, 'E10@kapattıklarında', .8, E.in2), t0 = A('E10@hiç'), q = st.t - t0;
    const sh = q > 0 ? Math.sin(q * 42) * 7 * Math.exp(-q * 5) : 0;
    const x = 640, y = 120, w = 640, hh = 860;
    k.save(); k.fillStyle = B.ton(.42); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.55); k.fillRect(-300, 980, 2600, 500);
    k.fillStyle = B.ton(.97); k.fillRect(x, y, w, hh); k.restore();   // açık kapının ardındaki karanlık
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 14; l.strokeRect(x - 16, y - 16, w + 32, hh + 16); l.restore();   // kasa
    // kanat: menteşe solda; açıkken kameraya dönük (serbest kenar daha uzun ve kadrajın solunda), kapanınca kasaya oturur
    const cw = w * lerp(.2, 1, kp), ex = x + cw + sh, ek = (1 - kp) * .22 * hh;
    const yol = g => { g.beginPath(); g.moveTo(x + sh * .3, y); g.lineTo(ex, y - ek); g.lineTo(ex, y + hh + ek); g.lineTo(x + sh * .3, y + hh); g.closePath(); };
    k.save(); yol(k); k.fillStyle = B.ton(.66); k.fill(); k.restore();
    l.save(); l.fillStyle = '#fff'; yol(l); l.fill(); l.strokeStyle = '#000'; l.lineWidth = 7; yol(l); l.stroke();
    l.fillStyle = '#000'; l.beginPath(); l.arc(ex - 46 * lerp(.4, 1, kp), y + hh * .5, 15, 0, TAU); l.fill(); l.restore();   // tokmak
  }, VID);

  // P77 kart: Stanford Magazine 2011, Mark'ın Zimbardo hakkındaki sözü; sayfa elle sürülür, "baştan"da şerit, "uydurmaya"da kamera son satıra
  sahne('P77', 'E11@bana', 'dergi', 'kart', (B, st) => {
    const gr = giris(st, 'E11@bana'), in1 = R(st, 'E11@uydurmaya', 1.8, E.io2);
    B.cam(lerp(960, 920, in1), lerp(470, 550, in1), 1.02 + .1 * in1 + st.lt * .006);
    const x = lerp(2100, 320, gr.p), p0 = Math.max(A('E11@bana') - .3, gr.tA), p = clamp((st.t - p0) / Math.max(2, A('E11@çalıştı') - p0));
    const d = dergi(B, 'JOHN MARK', ['“Bana öyle geliyordu ki varmak', 'istediği sonucu baştan biliyordu', 've deneyi ona uydurmaya çalıştı.”'], p, { x, vurgu: [{ i: 1, s: 'sonucu baştan biliyordu', a: R(st, 'E11@baştan', 1, E.lin) }] });
    if (gr.cek < 1) tutan(B.l, x + d.w - 150 + gr.cek * 700, d.y + d.h + gr.cek * 500, 1.1, -1);
  }, { ...KAG, over: ZM(KU(SMK), 'E11@bana', 8) });

  // P78 orta (rev3): karanlık odada monitör: isyan günü gündüz sayımı; kahraman kenarda, kolları sarkık, ötekilerden geride.
  //   "isteksiz"de kamera ona yaklaşır ve monitörün köşesinde video notunun tek sözü belirir (üst katman, alt banda değil); tarama bandı aşağı kayar
  sahne('P78', 'E12', 'monitor', 'orta', (B, st) => {
    const ya = R(st, 'E12@isteksiz', 2.2, E.io2);
    B.cam(lerp(960, 1040, ya), lerp(470, 500, ya), 1.04 + .12 * ya + st.lt * .01);
    SET.karanlik(B, .84);
    hale0(B, 960, 460, 760, .22);
    masa(B, 860, [[160, 600], [640, 1240], [1290, 1760]]);
    SET.monitorIci(B, 420, 150, 1080, 600, () => {
      const K = bodrum(B, st, { sayim: 4, gardiyanlar: [{ z: .3, u: .1, kol: [.1, .4] }, { z: .35, u: .28, f: -1, kol: [.2, .5] }] });
      kisiK(B, K, .46, .86, 'gardiyan', { f: -1, cop: false, kolO: [.05, .1], kolA: [-.05, .1], bas: .2 + .03 * Math.sin(st.t * .6) });
    });
  }, { baski: st => ({ mod: 'kagit', kuru: .6, bant: [((st.lt * .2) % 1.25) - .12, .7] }),
    over: OV(ZM(ETK('VİDEO NOTU · 2. GÜN: “isteksiz”', 1240, 250, { px: 40 }), 'E12@isteksiz', 6), ZM(KU('Stanford arşivi SC0750, videonotes_day3 (Bruich ve Thompson, 2004)', { y: 120, x: 160, align: 'left' }), 'E12@notları', 6)) });

  // P80: iki bölüm. (1) "Zimbardo'ya göre … gösteriyor" (Zimbardo'nun yorumu, alıntı değil): karanlık odada iki monitör (P65'in geri çağrısı);
  //   "iyi"de kamera gündüz monitörüne (kenarda duran gardiyan), "zalim"de gece monitörüne kayar, Eshelman mahkûma doğru eğilir.
  //   (2) "metinde"de belgeye kesme: Zimbardo 2018'den tek alıntı iki satır, sözle yazılır; "hiçbiri"nde yazılmış harflerin üstünde kehribar şerit. Belge ≤ 8 sn.
  const P80K = () => A('E13@metinde');
  sahne('P80', 'E13@iyi#1', 'z2018', 'kart', (B, st) => {
    const sw = P80K();
    if (st.t < sw) {
      const iy = R(st, 'E13@iyi', 1.4, E.io2), za = R(st, 'E13@zalim', 1.4, E.io2), eg = R(st, 'E13@zalim', .9);
      B.cam(lerp(lerp(960, 560, iy), 1380, za), 450, 1.04 + .16 * Math.max(iy, za) + st.lt * .006);
      ikiMonitor(B, (B2) => {
        const K = bodrum(B2, st, { levha: false });
        kisiK(B2, K, .5, -.7, 'mahkum', { f: 1, numara: '', kolO: [-.05, .1], kolA: [.05, .25], bas: .05 + Math.sin(st.t * .7) * .03 });
        kisiK(B2, K, .36, -.74, 'mahkum', { f: 1, numara: '5704', boyK: .96, kolO: [.25, .9], kolA: [.05, .25], bas: -.02 });
        kisiK(B2, K, .34, .84, 'gardiyan', { f: -1, cop: false, kolO: [.15, .5], kolA: [-.1, .3], bas: .1 + .06 * iy + Math.sin(st.t * .6) * .02 });
      }, (B2) => {
        const K = bodrum(B2, st, { isik: .3, levha: false, gardiyanlar: [{ z: .58, u: .5, f: -1, kol: [.1, .45], bas: .04 }, { z: .65, u: .76, f: -1, kol: [-.05, .2], bas: 0 }] });
        kisiK(B2, K, .3, -.3, 'mahkum', { f: 1, numara: '1037', onlukRenk: '#666864', bas: .2 + .1 * eg, govde: .05 + .05 * eg, kolO: [-.05, .1], kolA: [-.06, .12] });
        kisiK(B2, K, .27, lerp(.1, .03, eg), 'gardiyan', { f: -1, govde: .14 * eg, kolO: [-.3, .55], kolA: [-.35, .6], bas: .02 - .08 * eg, serbest: 1 });
        gece(B2, 960, 470);
      });
      return;
    }
    const hc = R(st, 'E13@hiçbiri', 1.6, E.io2);
    B.cam(960, 470, 1.04 + .06 * hc + (st.t - sw) * .01);
    const sat = ['İyi gardiyanların hiçbiri, arkadaşlarının', 'zulmünü durdurmak için araya girmedi.'], px = 52, w = 1440, x = (W - w) / 2, y = 250, lh = px * 1.5;
    const b0 = Math.min(A('E13@iyi#1') - .3, sw + .4), b1 = A('E13@girmedi'), p = clamp((st.t - b0) / Math.max(1.5, b1 - b0));
    SET.belge(B, ZUST, sat, p, { px, w, x, y, zemin: .38 });
    const va = R(st, 'E13@hiçbiri', 1.6, E.lin);
    if (va > 0) { const l = B.l; l.save(); l.font = `700 ${px}px "Courier Prime"`;
      let kalan = Math.floor((sat[0].length + sat[1].length) * p);
      sat.forEach((r, i) => { const n = Math.max(0, Math.min(r.length, kalan)); kalan -= r.length; const a = clamp(va * 2 - i); if (!n || a <= 0) return;
        const tw = l.measureText(r.slice(0, n)).width, yy = y + px * 3.6 + i * lh;
        B.renkBoya(g => g.rect(x + px * 1.1, yy - px * .6, (tw + px * .6) * a, px * 1.2), .6, 0); });
      l.restore(); }
  }, { baski: st => (st.t < P80K() ? { mod: 'kagit', kuru: .6 } : { mod: 'kagit' }), over: ZM(KU('Zimbardo 2018, prisonexp.org (çevirisi bizim)'), 'E13@metinde', 8) });

  // P81 geniş: gece koridoru, başka açı (kaçış noktası solda); Eshelman koridorda yürüyüp durur, "vardiyası"nda başını eğer;
  //   geride kıpırdamayan iki gardiyan, "aynısını"da arkadaki gardiyan duvara döner
  sahne('P81', 'E14', 'gece', 'genis', (B, st) => {
    B.cam(1010 - st.lt * 14, 540, 1.06 + st.lt * .022);
    const ay = R(st, 'E14@aynısını', .4), vd = R(st, 'E14@vardiyası', 1);
    const K = bodrum(B, st, { vp: [700, 480], gen: 1100, isik: .3, levha: false, gardiyanlar: [{ z: .55, u: .6, f: ay > .5 ? 1 : -1, kol: [.05, .3], bas: .02 }, { z: .63, u: .22, f: -1, kol: [-.05, .2], bas: 0 }] });
    const q = K.yer(.2, -.42), boy = 700 * K.olc(.2), v = BODRUM_GAIT.hiz * boy / 100 * 1.05, tS = Math.max(1.2, A('E14@vardiyası') - st.at);
    SET.yuru(B.l, q[0] - v * tS, q[1], boy, st.lt, { tip: 'gardiyan', f: 1, go: u => u < tS ? 1 : 0, kolO: [.2, .5], kolA: [-.1, .3], bas: .04 + .14 * vd });
    gece(B, 820, 480);
  }, VID);

  // P82 orta: gözlem odası (çalışma odası, sorgu değil): kamera sola kaymış, monitör kadrajda; masada iki kahve fincanı (buhar), koni loş.
  //   Mark müdürün karşısında. "itirazını"nda Mark öne eğilir, önkolu kalkar; "müdürün"de müdür başını ona çevirip eğer
  sahne('P82', 'E14@mark', 'gozlem', 'orta', (B, st) => {
    const it = R(st, 'E14@itirazını', .9), md = R(st, 'E14@müdürün', .8);
    B.cam(lerp(1150, 1170, it), lerp(470, 490, it), 1.24 + .04 * it + st.lt * .008);
    oda(B, st, { isik: .3, markO: { govde: .14 * it, bas: .1 - .06 * it, kolO: [.45 + .4 * it, 1.1 - .1 * it] }, mudurO: { bas: .06 + .06 * md, govde: .08 * md },
      monitor: (B2) => { bodrum(B2, st, { isik: .3, levha: false, gardiyanlar: [{ z: .4, u: .2, kol: [.1, .4] }] }); gece(B2, 960, 470); } });   // monitörde gece koridoru: müdürün başının yanında açık ekran lekesi olmasın
    SET.teyp(B, 1060, 440, .62, st.t, { kayit: 1, sol: .97, sag: .97 });   // aynı teyp, makaralar dolu (iç içe halka görünmesin)
    fincan(B, 800, 690, 1, -1, st.t); fincan(B, 1330, 690, .95, 1, st.t + .4);
  }, KK);
})();
