// III. Bant (D01–D19): arşiv kutusu → gözlem odası (ilk kez, ters açı) → bantın dökümü → müdürün yazısı, yurt, kurallar → Zimbardo 2018 ↔ Le Texier 2019.
// Gözlem odası ve masa: kâğıt + kuru fırça (.6), ışık konisi teybin üstünde, iki siluet eşit yükseklikte; kimse ışığın altında oturmaz.
// Belge ve döküm: kâğıt, kuru yok. Renk yalnız teybin kehribar ışığında, kırmızı kayıt lambasında ve belgedeki kehribar vurgu şeridinde.
// Başın yanında açık leke yok: alıntı panelleri ve etiketler başlardan uzakta. Makaralar tek tonlu disk (halka yok).
// a.js'deki VID, KAG, bodrum(), yakinFig() kullanılır. Bütün adlar bu kapsamın içinde (aynı sayfada beş sahne dosyası).
(() => {
  'use strict';
  const KK = { baski: { mod: 'kagit', kuru: .6 } };
  const UST = 'STANFORD ARŞİVİ · SC0750 · BANT A';
  // üst katman: film zamanında bir çapadan başlar, d sn sonra söner (ekran yazısı ≤ 8 sn); içteki yazı lt'sini çapadan sayar
  const ZM = (f, at, d = 8) => (ctx, st) => {
    const t0 = (at == null ? st.at : typeof at === 'string' ? A(at) : at) - st.at, lt = st.lt - t0;
    if (lt < 0) return; const a = clamp((d - lt) / .5); if (a <= 0) return;
    ctx.save(); ctx.globalAlpha *= a; f(ctx, { ...st, lt }); ctx.restore();
  };
  const R = (st, at, d = .6, e) => ramp(st.t, A(at), A(at) + d, e);   // sözcüğe bağlı geçiş 0→1
  // gözlem odası: kollar dirsekten bükük, önkol masada yatay
  const KOL = { kolO: [.45, 1.1], kolA: [.35, 1.18] };
  const oda = (B, st, o = {}) => SET.gozlemOdasi(B, st, { ...o, mudurO: { ...KOL, ...(o.mudurO || {}) }, markO: { ...KOL, ...(o.markO || {}) } });
  // makara açısı: ts (film zamanı) anında yavaşlayıp durur
  const aci = (t, hz, ts = 1e9) => TAU * hz * (t < ts ? t : ts + (1 - Math.exp(-(t - ts) * 2.5)) / 2.5);
  const DOLU = { sol: .97, sag: .97 };   // sarılı bant makarayı doldurur: iç içe halka görünmez

  // ── döküm sayfası: masada daktilo sayfası, sağ üstünde küçük teyp (makaralar döner, kayıt lambası). zaman: satır başına çapa (boş satır null) ──
  function dokum(B, st, id, satirlar, zaman, o = {}) {
    const top = satirlar.reduce((a, r) => a + r.length, 0); let yaz = 0;
    for (let i = 0; i < satirlar.length; i++) {
      if (!satirlar[i].length) continue;
      const a0 = A(zaman[i]); let a1 = Se(id) - .3;
      for (let j = i + 1; j < satirlar.length; j++) if (zaman[j]) { a1 = A(zaman[j]); break; }
      yaz += satirlar[i].length * clamp((st.t - a0) / Math.max(.4, a1 - a0));
    }
    const p = yaz / top;
    const c = [lerp(850, 880, st.p), lerp(400, 400 + Math.min(110, satirlar.length * 16), E.io2(p)), 1.12 + st.lt * .012];   // kamera yazılan satırı izler
    if (o.kam) { const u = o.kam[3]; B.cam(lerp(c[0], o.kam[0], u), lerp(c[1], o.kam[1], u), lerp(c[2], o.kam[2], u)); } else B.cam(...c);
    const r = SET.belge(B, UST, satirlar, p, { px: 38, w: 1100, x: 200, y: 170, zemin: .72, vurgu: o.vurgu, vurguA: o.vurguA, h: Math.max(470, satirlar.length * 57 + 230) });
    if (o.imlec && Math.floor(st.t * 2.2) % 2 === 0) { const l = B.l, x = r.x + 38 * 1.4 + o.imlec[1] * 22.8, y = r.y + 38 * 3.6 + o.imlec[0] * 57; l.save(); l.fillStyle = '#000'; l.fillRect(x, y - 18, 20, 36); l.restore(); }
    SET.teyp(B, 1520, 180, .45, st.t, { ang: o.ang, hz: .45, vu: o.vu, kayit: 1, vuIsik: .7, ...DOLU });
    return r;
  }
  // ── gözlem odası yakın planı: Mark (baş-omuz, profil sola), karanlık; ışık yalnız masada (alt), başın yanında açık leke yok ──
  function markYakin(B, st, o = {}) {
    SET.karanlik(B, .8);
    const k = B.k, my = o.masaY ?? 930, ix = o.isikX ?? 900;
    k.save(); k.fillStyle = B.ton(.18); k.beginPath(); k.moveTo(-300, my); k.lineTo(ix, my); k.lineTo(ix + 160, 1400); k.lineTo(-300, 1400); k.closePath(); k.fill(); k.restore();
    SET.surtme(B.k, -200, ix, my + 4, 13, { n: 30, boy: 120, acik: false });
    if (o.teyp) SET.teyp(B, o.teyp[0], o.teyp[1], o.teyp[2], st.t, { hz: .45, kayit: 1, vuIsik: .75, ...DOLU });
    yakinFig(B, 'gardiyan', o.x ?? 1220, o.y ?? 380, o.boy ?? 2200, { f: -1, gozluk: false, cop: false, bas: o.bas ?? .06, govde: o.govde ?? 0, kolO: o.kolO || [.5, 1.1], kolA: o.kolA || [.3, .9], serbest: 1 });
  }
  const quad = (g, a, b, c, d) => { g.beginPath(); g.moveTo(...a); g.lineTo(...b); g.lineTo(...c); g.lineTo(...d); g.closePath(); };
  // yurt koridoru (Mayıs 1971, video): düz tavan (floresan sırası yok), parmaklıksız ahşap kapılar, uçta jaluzili pencere, panoda kâğıtlar
  function yurt(B, st) {
    const K = D.koridor(B, st.t, { kapilar: 0, levha: false, sonD: .1, solD: .5, sagD: .56, isik: .8 });
    const k = B.k, l = B.l, zM = .86;
    k.save(); k.fillStyle = B.ton(.22); quad(k, K.P(0, -1, 1), K.P(zM, -1, 1), K.P(zM, 1, 1), K.P(0, 1, 1)); k.fill();   // tavan düz
    // pencere: uçta, yalnız dikey jaluzi çizgileri (kesişen kayıt yok)
    k.fillStyle = B.ton(.28); for (let i = 1; i < 9; i++) { const u = -1 + i * .22; quad(k, K.P(zM, u - .012, .12), K.P(zM, u + .012, .12), K.P(zM, u + .012, .9), K.P(zM, u - .012, .9)); k.fill(); }
    k.restore();
    for (const yan of [-1, 1]) for (const z0 of [.1, .38, .62]) {
      const z1 = z0 + .085, a = K.P(z0, yan, 0), b = K.P(z1, yan, 0), c = K.P(z1, yan, .66), d = K.P(z0, yan, .66);
      k.save(); k.fillStyle = B.ton(.7); quad(k, a, b, c, d); k.fill(); k.restore();
      l.save(); l.strokeStyle = '#000'; l.lineWidth = Math.max(1.5, Math.abs(b[0] - a[0]) * .05); quad(l, a, b, c, d); l.stroke();
      const kn = K.P(z0 + .065, yan, .32); l.beginPath(); l.arc(kn[0], kn[1], Math.max(2, Math.abs(b[0] - a[0]) * .05), 0, TAU); l.fill(); l.restore();
    }
    k.save(); k.fillStyle = B.ton(.6); quad(k, K.P(.22, -1, .42), K.P(.32, -1, .42), K.P(.32, -1, .62), K.P(.22, -1, .62)); k.fill(); k.fillStyle = B.ton(.06);
    for (const [u0, h0, u1, h1] of [[.23, .46, .26, .58], [.27, .48, .3, .56], [.235, .6, .29, .61]]) { quad(k, K.P(u0, -1, h0), K.P(u1, -1, h0), K.P(u1, -1, h1), K.P(u0, -1, h1)); k.fill(); }
    k.restore();
    return K;
  }

  // P41 orta: arşiv kutusu (SC0750) açılır; "deneyin arşivinden"de kapak devrilir, içinde düz makara kutuları; "yayımladı"da biri yukarı kalkar
  sahne('P41', 'D01', 'arsiv', 'orta', (B, st) => {
    B.cam(960, 500, 1.02 + st.lt * .018);
    const k = B.k, l = B.l, ac = R(st, 'D01@deneyin', 1.3, E.io3), kalk = R(st, 'D01@yayımladı', .6, E.out3);
    k.save(); k.fillStyle = B.ton(.72); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.5); k.fillRect(-300, 740, 2600, 900); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.moveTo(-300, 740); l.lineTo(2300, 740); l.stroke(); l.restore();
    const x0 = 580, x1 = 1280, yt = 470, yb = 800, dx = 110, dy = 70;
    const ON = [[x0, yt], [x1, yt], [x1, yb], [x0, yb]], YAN = [[x1, yt], [x1 + dx, yt - dy], [x1 + dx, yb - dy], [x1, yb]], AG = [[x0, yt], [x1, yt], [x1 + dx, yt - dy], [x0 + dx, yt - dy]];
    const yol = (g, P) => { g.beginPath(); poly(g, P, true); };
    l.save(); l.fillStyle = '#fff'; for (const P of [ON, YAN, AG]) { yol(l, P); l.fill(); } l.restore();   // kutunun arkasındaki zemin çizgisi silinir
    // kapak: arka kenar menteşe; th 0 kapalı → 1,9 rad açık (arkaya yaslanır)
    const th = ac * 1.9, v = [-dx * Math.cos(th), dy * Math.cos(th) - 230 * Math.sin(th)];
    const KAP = [[x0 + dx, yt - dy], [x1 + dx, yt - dy], [x1 + dx + v[0], yt - dy + v[1]], [x0 + dx + v[0], yt - dy + v[1]]];
    const kapak = () => { k.save(); yol(k, KAP); k.fillStyle = B.ton(th < PI / 2 ? .52 : .62); k.fill(); k.restore(); l.save(); l.fillStyle = '#fff'; yol(l, KAP); l.fill(); l.strokeStyle = '#000'; l.lineWidth = 3; yol(l, KAP); l.stroke(); l.restore(); };
    k.save(); yol(k, AG); k.fillStyle = B.ton(.88); k.fill(); k.restore();   // iç (koyu)
    if (th >= PI / 2) kapak();
    // makara kutuları: dik, düz tepeli, farklı eğim ve yükseklik (yuvarlak tepe yok); alt yarıları ön yüzün arkasında
    const kut = [[650, .03, 'A'], [730, -.02, 'B'], [805, .05, 'C'], [880, -.03, 'D'], [955, .02, 'E'], [1035, -.05, 'F'], [1110, .03, 'G'], [1185, -.02, 'H']];
    kut.forEach(([x, a, ad], i) => {
      const ky = yt - 46 + (i % 3) * 7 - (i === 0 ? 170 * kalk : 0);
      for (const g of [k, l]) { g.save(); g.translate(x + 30, ky); g.rotate(a); }
      k.fillStyle = B.ton(.3 + (i % 2) * .12); k.fillRect(-30, 0, 62, 170);
      l.fillStyle = '#fff'; l.fillRect(-30, 0, 62, 170); l.strokeStyle = '#000'; l.lineWidth = 2.5; l.strokeRect(-30, 0, 62, 170);
      l.fillStyle = '#000'; l.font = '700 24px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText(ad, 1, 22);
      for (const g of [k, l]) g.restore();
    });
    // ön ve yan yüz (karton), etiket
    k.save(); yol(k, ON); k.fillStyle = B.ton(.42); k.fill(); yol(k, YAN); k.fillStyle = B.ton(.56); k.fill(); k.fillStyle = '#fff'; k.fillRect(800, 560, 280, 120); k.restore();
    l.save(); l.fillStyle = '#fff'; yol(l, ON); l.fill(); yol(l, YAN); l.fill(); l.strokeStyle = '#000'; l.lineWidth = 3; yol(l, ON); l.stroke(); yol(l, YAN); l.stroke(); l.beginPath(); l.moveTo(x0 + dx, yt - dy); l.lineTo(x1 + dx, yt - dy); l.stroke();
    l.lineWidth = 2; l.strokeRect(800, 560, 280, 120); l.fillStyle = '#000'; l.font = '700 58px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText('SC0750', 940, 620); l.restore();
    if (th < PI / 2) kapak();
  }, { ...KAG, over: KU('Stanford Üniversitesi arşivi, SC0750 (Stanford Prison Experiment)', { t0: 1.2 }) });

  // P42 ayrıntı: makara kutusu, el yazısı etiket "Tape A"; "banda"da makara çıkarılır, "dakikalık"ta bant ucu sarkar
  sahne('P42', 'D01@aynı', 'arsiv', 'ayrinti', (B, st) => {
    B.cam(960, 520, 1.05 + st.lt * .02);
    const k = B.k, l = B.l, cik = R(st, 'D01@banda', 1.2, E.io3), don = R(st, 'D01@dakikalık', 1.5, E.lin);
    k.save(); k.fillStyle = B.ton(.55); k.fillRect(-300, -300, 2600, 1700); k.restore();
    const bx = 560, by = 330, bw = 800, bh = 540;
    k.save(); k.fillStyle = B.ton(.8); k.fillRect(bx + 16, by + 18, bw, bh); k.fillStyle = B.ton(.85); k.fillRect(bx, by, bw, bh); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(bx, by, bw, bh); l.restore();
    // makara: tek tonlu disk, üç oval delik, göbek (halka tarama yok)
    const mx = 960 + cik * 140, my = 600 - cik * 250, mr = 240, an = .3 + don * 1.2 + cik * .5;
    k.save(); k.fillStyle = B.ton(.3); k.beginPath(); k.arc(mx, my, mr, 0, TAU); k.fill(); k.restore();
    l.save(); l.fillStyle = '#fff'; l.beginPath(); l.arc(mx, my, mr, 0, TAU); l.fill(); l.strokeStyle = '#000'; l.lineWidth = 5; l.stroke(); l.translate(mx, my); l.rotate(an);
    k.save(); k.translate(mx, my); k.rotate(an);
    for (let i = 0; i < 3; i++) { l.rotate(TAU / 3); k.rotate(TAU / 3); k.beginPath(); k.ellipse(0, -mr * .55, mr * .16, mr * .25, 0, 0, TAU); k.fillStyle = B.ton(.85); k.fill(); l.beginPath(); l.ellipse(0, -mr * .55, mr * .16, mr * .25, 0, 0, TAU); l.stroke(); }
    k.restore(); l.beginPath(); l.arc(0, 0, mr * .1, 0, TAU); l.fillStyle = '#000'; l.fill(); l.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.moveTo(mx + mr * .8, my + mr * .2); l.quadraticCurveTo(mx + mr * 1.15, my + 200, mx + mr * .95 + 120 * don, my + 230 + 170 * don); l.stroke(); l.restore();
    // kutunun ön kapağı (alt yarı, makaranın önünde) ve el yazısı etiket
    const cy = by + bh * .55, ch = bh * .45;
    k.save(); k.fillStyle = B.ton(.4); k.fillRect(bx, cy, bw, ch); k.fillStyle = '#fff'; k.fillRect(bx + 240, cy + 40, 320, 130); k.restore();
    l.save(); l.fillStyle = '#fff'; l.fillRect(bx, cy, bw, ch); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(bx, cy, bw, ch); l.lineWidth = 2; l.strokeRect(bx + 240, cy + 40, 320, 130);
    l.translate(bx + 400, cy + 106); l.rotate(-.05); l.fillStyle = '#000'; l.font = 'italic 600 84px "Cormorant Garamond"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText('Tape A', 0, 0); l.restore();
  }, { ...KAG, over: ZM(KU('Bant A · yaklaşık 18 dakika'), 'D01@on#1', 6) });

  // P43 geniş, DÖNÜŞ: gözlem odası ilk kez; ışık plan başında yanar, makaralar dönmeye başlar, monitörde koridor
  sahne('P43', 'D02', 'gozlem', 'genis', (B, st) => {
    B.cam(960, 520, 1 + st.lt * .012);
    oda(B, st, { isik: ramp(st.lt, .15, 1.3, E.out3), ang: aci(st.t - st.at - .6 > 0 ? st.t - st.at - .6 : 0, .45),
      mudurO: { bas: .08 + .06 * R(st, 'D02@gündüz', .8) }, markO: { bas: .12 - .08 * R(st, 'D02@zimbardo', .8) },
      monitor: (B2) => bodrum(B2, st, { gardiyanlar: [{ z: .4, u: .15 }] }) });
  }, { ...KK, over: OV(ZM(ETK('MÜDÜR · DAVID JAFFE', 520, 760, { d: 4.5 }), 'D02@müdür', 5), ZM(ETK('GÜNDÜZ VARDİYASI GARDİYANI', 1440, 760, { d: 4.5 }), 'D02@gündüz', 5),
    ZM(KU("Gün: Le Texier'ye göre üçüncü, Zimbardo'ya göre ilk"), 'D02@lö', 7)) });

  // P44 yakın: Mark, karanlık oda; adı söylenince başını kaldırır, "yirmi"de hafif eğer
  sahne('P44', 'D03', 'gozlem', 'yakin', (B, st) => {
    B.cam(960, 540, 1.02 + st.lt * .02);
    const kalk = R(st, 'D03@mark', .7);
    markYakin(B, st, { bas: lerp(.2, .04, kalk) + .05 * R(st, 'D03@yirmi', .8), govde: lerp(.08, 0, kalk), teyp: [380, 760, .9] });
  }, { ...KK, over: ZM(ETK('MARK', 560, 400, { d: 4 }), 'D03@mark', 4.5) });

  // P45 ayrıntı: döküm D04 (müdür söze girer), satırlar sözle yazılır
  sahne('P45', 'D04', 'dokum', 'ayrinti', (B, st) => {
    dokum(B, st, 'D04', ['MÜDÜR: Bu sabah işe pek karışmadığını', '       fark ettik. Biraz da benim', '       suçum; sayım yapılırken dışarıda', '       oturmak istediğinde ses', '       çıkarmadım.'],
      ['D04@bu', 'D04@fark', 'D04@suçum', 'D04@oturmak', 'D04@çıkarmadım']);
  }, { ...KAG, over: ZM(KU('Stanford arşivi, Bant A, 8:39–9:21 (çeviri ve konuşan adları bizim)'), 'D04@bu', 8) });

  // P46 orta: "her"de müdür öne eğilir; "olacak"ta Mark başını önüne eğer; teyp ışıkta
  sahne('P46', 'D05', 'gozlem', 'orta', (B, st) => {
    B.cam(800, 520, 1.42 + st.lt * .015);
    const e = R(st, 'D05@her', .9);
    oda(B, st, { mudurO: { govde: .2 * e, bas: .06 + .06 * e, kolO: [.45 + .15 * e, 1.1 - .1 * e] }, markO: { bas: .1 + .12 * R(st, 'D05@olacak', .8) },
      monitor: (B2) => bodrum(B2, st, { sayim: 3, gardiyanlar: [{ z: .35, u: .2 }] }) });
  }, { ...KK, over: ZM(QT('“Ama gardiyanların şunu bilmesi gerek: her gardiyan, bizim sert gardiyan dediğimiz şey olacak.”', 'Bant A, 9:27', { y: 190, maxW: 1400 }), null, 7.5) });

  // P47 ayrıntı: döküm D06 (Mark: "Ben pek sert değilim."); "kararlı"da müdürün tanımı kehribar şeritle
  sahne('P47', 'D06', 'dokum', 'ayrinti', (B, st) => {
    dokum(B, st, 'D06', ['MARK:  Ben pek sert değilim.', '', 'MÜDÜR: Biraz denemen, bunu içine', '       sindirmen gerek. Sert derken şunu', '       kastediyorum: kararlı olacaksın,', '       işin içinde olacaksın.'],
      ['D06@ben', null, 'D06@biraz', 'D06@sindirmen', 'D06@kastediyorum', 'D06@işin'], { vurgu: st.t > A('D06@işin') ? [4, 5] : [4], vurguA: R(st, 'D06@kararlı', 1.2, E.lin) });
  }, { ...KAG, over: ZM(KU('Bant A, 9:36–9:51'), 'D06@ben', 8) });

  // P48 yakın: Mark polisi düşünür; başı önde başlar, "benden"de kalkar, "bağırmaya"da önkolu göğüs hizasına kalkar (dirsek bükük), "kısır"da baş öne
  sahne('P48', 'D07', 'gozlem', 'yakin', (B, st) => {
    B.cam(1000, 560, 1.1 + st.lt * .01);
    const kalk = R(st, 'D07@benden', .8), el = R(st, 'D07@bağırmaya', .7) * (1 - R(st, 'D07@kısır', 1));
    markYakin(B, st, { x: 1470, y: 400, boy: 2000, bas: lerp(.24, .05, kalk) + .1 * R(st, 'D07@kısır', 1), kolO: [lerp(.5, 1.0, el), lerp(1.1, 1.0, el)], isikX: 820, masaY: 960 });
  }, { ...KK, over: ZM(QT('“Benden istediğin şey, bence polisle hep bu kadar sorun çıkmasının sebebi.”', 'Bant A, 10:44', { y: 220, x: 600, maxW: 860 }), 'D07@benden', 8) });

  // P49 ayrıntı: döküm D08
  sahne('P49', 'D08', 'dokum', 'ayrinti', (B, st) => {
    dokum(B, st, 'D08', ['MARK:  Bana kalsa hiçbir şey yapmazdım.', '       Kendi hâline bırakırdım.', '', '       [...]'], ['D08@bana', 'D08@kendi', null, 'D08@biraz']);
  }, { ...KAG, over: ZM(KU('Bant A, 11:10'), 'D08@bana', 7) });

  // P50 yakın: ışıkta masada duran aynalı gözlük; "üniformasını"nda parıltı camda kayar (el yok, kişi yok)
  sahne('P50', 'D08@sadece', 'gozlem', 'yakin', (B, st) => {
    B.cam(960, 560, 1.04 + st.lt * .025);
    SET.karanlik(B, .84);
    const k = B.k, l = B.l, my = 470;
    // masa üstü ışıkta (perspektif), uzak kenarı sert açık çizgi
    k.save(); const g = k.createRadialGradient(960, 760, 80, 960, 760, 900); g.addColorStop(0, B.ton(.02)); g.addColorStop(1, B.ton(.55)); k.fillStyle = g; k.fillRect(-300, my, 2600, 1100);
    k.fillStyle = '#fff'; k.fillRect(-300, my - 4, 2600, 8); k.restore();
    const cx = 960, cy = 720, s = 2.7, sy = .78;
    const cam = sx => g2 => { g2.save(); g2.translate(cx, cy); g2.scale(s, s * sy); g2.beginPath(); g2.moveTo(sx * 16, -58); g2.bezierCurveTo(sx * 70, -66, sx * 112, -58, sx * 118, -40);
      g2.bezierCurveTo(sx * 122, -12, sx * 100, 8, sx * 74, 8); g2.bezierCurveTo(sx * 44, 8, sx * 18, -18, sx * 16, -58); g2.closePath(); g2.restore(); };
    // gölge
    k.save(); k.fillStyle = B.ton(.5, .8); k.beginPath(); k.ellipse(cx + 40, cy + 30, 300, 30, 0, 0, TAU); k.fill(); k.restore();
    // saplar (camların arkasında, katlı)
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 9; l.lineCap = 'round';
    for (const sx of [-1, 1]) { l.beginPath(); l.moveTo(cx + sx * 116 * s, cy - 44 * s * sy); l.lineTo(cx - sx * 30 * s, cy - 26 * s * sy); l.stroke(); }
    l.restore();
    const kay = R(st, 'D08@üniformasını', 2.2, E.io2);
    for (const sx of [-1, 1]) {
      l.save(); cam(sx)(l); l.fillStyle = '#fff'; l.fill(); l.restore();   // sapları camın arkasında bırak
      k.save(); cam(sx)(k); k.clip(); const gg = k.createLinearGradient(0, cy - 180, 0, cy + 30); gg.addColorStop(0, B.ton(.9)); gg.addColorStop(1, B.ton(.62)); k.fillStyle = gg; k.fillRect(cx - 400, cy - 220, 800, 280);
      // parıltı nesnede: eğik açık şerit soldan sağa kayar
      const px = lerp(cx - 380, cx + 420, kay); k.fillStyle = B.ton(.02); k.beginPath(); k.moveTo(px - 10, cy - 200); k.lineTo(px + 40, cy - 200); k.lineTo(px - 50, cy + 40); k.lineTo(px - 100, cy + 40); k.closePath(); k.fill(); k.restore();
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 7; cam(sx)(l); l.stroke(); l.restore();
    }
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 7; l.beginPath(); l.moveTo(cx - 16 * s, cy - 50 * s * sy); l.quadraticCurveTo(cx, cy - 58 * s * sy, cx + 16 * s, cy - 50 * s * sy); l.stroke(); l.beginPath(); l.moveTo(cx - 18 * s, cy - 61 * s * sy); l.lineTo(cx + 18 * s, cy - 61 * s * sy); l.stroke(); l.restore();
  }, { ...KK, over: ZM(QT('“Sadece bu gardiyan üniformasını giymek bile benim için ağır bir şey.”', 'Bant A, 13:51', { y: 200, maxW: 1300 }), 'D08@sadece', 7) });

  // P51 orta: müdür konuşur, monitörde bodrum (sayım); "reform"da önkolu kalkar, "bakın"da monitöre döner (dirsek bükük)
  sahne('P51', 'D09', 'gozlem', 'orta', (B, st) => {
    B.cam(560, 430, 1.4 + st.lt * .012);
    const e1 = R(st, 'D09@reform', .7) * (1 - R(st, 'D09@dünyaya', .7)), e2 = R(st, 'D09@bakın', .6);
    oda(B, st, { mark: false, mudurO: { bas: .06 - .1 * e2, kolO: [.45 + .3 * e1 + .35 * e2, 1.1 + .2 * e1 + .1 * e2] },
      monitor: (B2) => bodrum(B2, st, { sayim: 5, gardiyanlar: [{ z: .3, u: .1, kol: [.9 + Math.sin(st.t * 2) * .15, .9] }] }) });
  }, { ...KK, over: OV(ZM(QT('“Umarız bu çalışmadan çok ciddi reform önerileri çıkar.”', 'Bant A, 12:22', { y: 170, x: 1300, maxW: 900 }), 'D09@umarız', 5.2),
    ZM(QT('“Bakın, böyle davranan gardiyanlarınız olunca ne oluyor.”', 'Bant A, 23:45', { y: 170, x: 1300, maxW: 900 }), 'D09@dünyaya', 7)) });

  // P52 ayrıntı: VU göstergesi ve makaranın kenarı; "olmalı"da ibre sıçrar, kehribar ışık parlar
  sahne('P52', 'D10', 'teyp', 'ayrinti', (B, st) => {
    B.cam(880, 640, 2.1 + st.lt * .03);
    const k = B.k; k.save(); k.fillStyle = B.ton(.85); k.fillRect(-300, -300, 2600, 1700); k.restore();
    const sic = R(st, 'D10@olmalı', .12, E.out3) * (1 - ramp(st.t, A('D10@olmalı') + .5, A('D10@olmalı') + 1.6));
    SET.teyp(B, 960, 300, 1.25, st.t, { hz: .45, kayit: 1, vuIsik: .55 + .35 * sic, vu: .35 + .25 * Math.abs(Math.sin(st.t * 5.3) * Math.sin(st.t * 2.1)) * (1 - sic) + .62 * sic, ...DOLU });
  }, { ...KAG, over: OV((ctx, st) => { const t0 = A('D10@öyle'); if (st.t > t0 + 8) return; buyukSoz(ctx, 'ÖYLE DAVRANAN', st.t, t0, { px: 140, y: 190 }); buyukSoz(ctx, 'GARDİYANLARIMIZ OLMALI', st.t, t0 + .5, { px: 140, y: 330 }); },
    ZM(KU('Bant A, 23:58'), 'D10@öyle', 6)) });

  // P53 geniş: iki kişi; "değilim"de Mark geriye yaslanır, "mahkûm"da müdür başını ona çevirir
  sahne('P53', 'D11', 'gozlem', 'genis', (B, st) => {
    B.cam(960, 520, 1.04 + st.lt * .01);
    const y = R(st, 'D11@değilim', 1);
    oda(B, st, { markO: { govde: -.18 * y, bas: .08 - .1 * y, kolO: [lerp(.45, .2, y), lerp(1.1, 1.5, y)] }, mudurO: { bas: .08 - .08 * R(st, 'D11@mahkum', .8) },
      monitor: (B2) => bodrum(B2, st, { sayim: 3 }) });
  }, { ...KK, over: ZM(QT('Mark: “Bu deney için iyi bir gardiyan değilim. Mahkûm olsam, gerçekten iyi bir mahkûm olurdum.”', 'Bant A, 15:28', { y: 170, maxW: 1500 }), 'D11@mark', 8) });

  // P54 ayrıntı: ışıkta masada dönen bozuk para; "rastgele"de devrilip yalpalayarak yatar (yazı tura)
  sahne('P54', 'D11@müdürün', 'gozlem', 'ayrinti', (B, st) => {
    B.cam(960, 640, 1.1 + st.lt * .025);
    const k = B.k, l = B.l, my = 560;
    k.save(); k.fillStyle = B.ton(.85); k.fillRect(-300, -300, 2600, my + 300); const g = k.createRadialGradient(960, 780, 60, 960, 780, 900); g.addColorStop(0, B.ton(.02)); g.addColorStop(1, B.ton(.5)); k.fillStyle = g; k.fillRect(-300, my, 2600, 1200); k.restore();
    l.save(); l.fillStyle = '#000'; l.fillRect(-300, my - 4, 2600, 6); l.restore();
    const ts = A('D11@rastgele') - st.at, r = 150, y0 = 790;
    if (st.lt < ts) {   // dik dönüş (yavaşlar)
      const u = st.lt / Math.max(.5, ts), ang = 26 * st.lt * (1 - .45 * u);
      k.save(); k.fillStyle = B.ton(.45, .6); k.beginPath(); k.ellipse(960, y0 + 12, r * .9, 18, 0, 0, TAU); k.fill(); k.restore();
      D.para(B, 960, y0 - r + 4, r, ang);
    } else {             // devrilir, yalpalar, yatar
      const q = st.lt - ts, sn = Math.exp(-q * 2.2), w = Math.sin(q * 18) * sn, eg = clamp(q / .35);
      const ry = lerp(r, r * .3, E.out3(eg)) + Math.abs(w) * r * .25, cy = lerp(y0 - r + 4, y0, E.out3(eg));
      k.save(); k.fillStyle = B.ton(.45, .6); k.beginPath(); k.ellipse(970, cy + ry * .5 + 12, r * 1.05, ry * .55 + 6, 0, 0, TAU); k.fill(); k.restore();
      k.save(); k.fillStyle = B.ton(.6); k.beginPath(); k.ellipse(960, cy + 12, r, ry, w * .2, 0, TAU); k.fill(); k.fillStyle = B.ton(.32); k.beginPath(); k.ellipse(960, cy, r, ry, w * .2, 0, TAU); k.fill(); k.restore();
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.ellipse(960, cy, r, ry, w * .2, 0, TAU); l.stroke(); l.restore();
    }
  }, { ...KAG, over: ZM(QT('Müdür: “Evet, ama bu rastgele seçimin bir parçası.\nVe önemli.”', 'Bant A, 15:37', { y: 200, maxW: 1500 }), 'D11@müdürün', 7) });

  // P55 orta: müdür önde, monitörde koridorda tek gardiyan; "polise"de gardiyan döner, "kafasındaki"nde eli beline iner; "küçültücü"de müdür eğilir
  sahne('P55', 'D12', 'gozlem', 'orta', (B, st) => {
    B.cam(430, 390, 1.78 + st.lt * .012);
    const don = R(st, 'D12@polise', .5), el = R(st, 'D12@kafasındaki', .7), eg = R(st, 'D12@küçültücü', 1);
    oda(B, st, { mark: false, mudurO: { govde: .1 + .12 * eg, bas: .1 + .05 * eg },
      monitor: (B2) => bodrum(B2, st, { gardiyanlar: [{ z: .3, u: .05, f: don > .5 ? -1 : 1, kol: [lerp(.15, -.06, el), lerp(.5, .2, el)], bas: .05 }] }) });
  }, KK);

  // P56 yakın: Mark (daha sıkı kadraj, teybin kehribar ışığı kadraj kenarında); "başka başka"da başını sallar, "müdür"de başı öne
  sahne('P56', 'D13', 'gozlem', 'yakin', (B, st) => {
    B.cam(900, 520, 1.06 + st.lt * .015);
    const s0 = A('D13@başka'), sal = st.t > s0 && st.t < s0 + 1.4 ? Math.sin((st.t - s0) * 9) * .08 * (1 - (st.t - s0) / 1.4) : 0;
    markYakin(B, st, { x: 1480, y: 340, boy: 2500, bas: .04 + sal + .12 * R(st, 'D13@müdür', .8), teyp: [240, 700, 1.1], isikX: 820 });
  }, { ...KK, over: ZM(QT('Mark: “Ben çok polis gördüm; hepsi başka başka davranıyor.”\nMüdür: “Biz kalıp bir gardiyan kurmaya çalışıyoruz.”', 'Bant A, 25:59–26:12', { y: 230, x: 620, px: 60, maxW: 860 }), 'D13@markın', 8) });

  // P57 ayrıntı: döküm D14; Mark'ın satırı boş, imleç bekler; "döneceğiz"de kamera teybe kayar, makaralar durur, kayıt lambası yanık kalır
  sahne('P57', 'D14', 'dokum', 'ayrinti', (B, st) => {
    const ts = A('D14@döneceğiz');
    dokum(B, st, 'D14', ['MÜDÜR: Şimdiye kadar tarzın biraz fazla', '       yumuşaktı. Biraz daha işin içine', '       girmeni istiyoruz.', '', 'MARK:  '], ['D14@şimdiye', 'D14@yumuşaktı', 'D14@girmeni', null, 'D14@markın'],
      { ang: aci(st.t, .45, ts), vu: st.t < ts ? undefined : lerp(.35, 0, clamp((st.t - ts) / .6)), imlec: st.t > A('D14@markın') ? [4, 7] : null, kam: [1420, 330, 1.9, R(st, 'D14@döneceğiz', 1.4, E.io3)] });
  }, { ...KAG, over: ZM(KU('Bant A, 26:24'), 'D14@şimdiye', 7) });

  // P58 kart: müdürün deney sonrası yazısı (daktilo, Türkçe); "sert"te vurgu şeridi, kamera vurguya iner
  sahne('P58', 'D15', 'rapor', 'kart', (B, st) => {
    B.cam(960, lerp(450, 540, ramp(st.t, A('D15@sert'), A('D15@sert') + 2)), 1.02 + st.lt * .01);
    const p0 = A('D15@zimbardo') - .6, p = clamp((st.t - p0) / Math.max(2, A('D15@sert') - p0));
    SET.belge(B, 'MÜDÜRÜN DENEY SONRASI YAZISI', ['Dr. Zimbardo, en zor sorunun', 'gardiyanları gardiyan gibi davranmaya', 'ikna etmek olacağını söyledi. [...]', '', 'Bana "sert gardiyan" davranışını ortaya', 'çıkarmaya çalışma sorumluluğu verildi.'], p,
      { px: 42, w: 1300, y: 150, vurgu: [4, 5], vurguA: R(st, 'D15@sert', 1.8, E.lin) });
  }, { ...KAG, over: ZM(KU('Le Texier 2019, s. 7 (çevirisi bizim)'), 'D15@zimbardo', 8) });

  // P59 geniş (video): Mayıs 1971 yurt koridoru; gündelik giysili öğrenciler; gardiyan rolündeki sopa değil not defteri tutuyor.
  //   "arkadaşlarıyla"da uzakta bir öğrenci kapıdan çıkıp koridoru geçer; "canlandırması"nda not defteri kalkar
  sahne('P59', 'D16', 'yurt', 'genis', (B, st) => {
    B.cam(960 + st.lt * 6, 520, 1.02 + st.lt * .012);
    const K = yurt(B, st);
    const kisi = (z, u, tip, oo = {}) => { const p = K.yer(z, u), s = K.olc(z); return FIG.kisi(B.l, p[0], p[1], 700 * s, { tip, ...oo }); };
    const g0 = A('D16@arkadaşlarıyla') - st.at;
    if (st.lt > g0) { const p = K.yer(.6, .9); SET.yuru(B.l, p[0], p[1], 700 * K.olc(.6), st.lt - g0, { tip: 'gazeteci', f: -1, kolO: [.15, .3], kolA: [.1, .3] }); }
    kisi(.42, -.6, 'gazeteci', { f: 1, kolO: [-.05, .1], kolA: [-.08, .12], bas: .04, govde: -.04 });
    kisi(.5, .55, 'takim', { f: -1, kolO: [.4, 1.2], kolA: [.3, .9], bas: .08 });
    const def = R(st, 'D16@canlandırması', .8);
    kisi(.2, .35, 'arastirmaci', { f: -1, bas: .12 - .08 * def, kolO: [.5 + .4 * def, 1.2], kolA: [.2, .3], serbest: 1,
      el: { on: (g, e) => { g.save(); g.fillStyle = '#B4B4AE'; g.translate(e.e[0], e.e[1]); g.rotate(-e.a + .3); g.fillRect(-1, -9, 7, 10); g.restore(); } } });
  }, { ...VID, over: ZM(ETK('MAYIS 1971 · STANFORD YURDU', 960, 130, { video: 1, d: 6 }), null, 7) });

  // P60 ayrıntı: 17 satırlık kural listesi (yalnız numara + çizgi; kural metni yok); "on biri"nde 11'i kehribar şeritle, sayaç
  sahne('P60', 'D16@lö', 'kurallar', 'ayrinti', (B, st) => {
    B.cam(960, 440, 1.12 + st.lt * .015);
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = B.ton(.4); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.6); k.fillRect(374, 126, 1000, 590); k.fillStyle = '#fff'; k.fillRect(360, 110, 1000, 590); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 1.6; l.strokeRect(360, 110, 1000, 590); l.restore();
    const r = rng(41), uz = Array.from({ length: 17 }, () => .45 + r() * .5), V = [0, 1, 2, 4, 5, 7, 8, 10, 12, 13, 15];
    const g0 = A('D16@lö'), g1 = A('D16@yedi') + .3, v0 = A('D16@on#1') - .2, v1 = A('D16@oradan');
    let n = 0;
    for (let i = 0; i < 17; i++) {
      const col = i < 9 ? 0 : 1, row = i < 9 ? i : i - 9, x = 420 + col * 480, y = 170 + row * 58;
      const a = clamp((st.t - lerp(g0, g1, i / 17)) / .25); if (a <= 0) continue;
      const vi = V.indexOf(i);
      if (vi >= 0) { const va = clamp((st.t - lerp(v0, v1, vi / 11)) / .25); if (va > 0) { n++; B.renkBoya(g => g.rect(x - 14, y - 19, (70 + 340 * uz[i]) * va + 14, 38), .6, 0); } }
      l.save(); l.fillStyle = '#000'; l.font = '700 34px "Courier Prime"'; l.textBaseline = 'middle'; l.textAlign = 'right'; l.fillText((i + 1) + '.', x + 50, y);
      l.strokeStyle = '#000'; l.lineWidth = 5; l.lineCap = 'round'; l.beginPath(); l.moveTo(x + 70, y); l.lineTo(x + 70 + 330 * uz[i] * a, y); l.stroke(); l.restore();
    }
    if (st.t > v0) { l.save(); l.fillStyle = '#000'; l.font = '400 120px "Bebas Neue"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText(n + ' / 17', 1570, 420); l.restore(); }
  }, { ...KAG, over: ZM(KU("Le Texier'nin sayımı (2019, s. 3–4)", { x: 1800, align: 'right' }), 'D16@lö', 7) });

  // P61 kart: Zimbardo 2018 metni; "hafif"te vurgu; "bantta"da P47'deki döküm şeridi sağdan kayar (müdürün kendi tanımı)
  sahne('P61', 'D17', 'z2018', 'kart', (B, st) => {
    const ks = R(st, 'D17@bantta', 1, E.io3);
    B.cam(960, 470, 1.02 + st.lt * .008);
    const p = clamp((st.t - A('D17@bir') + .3) / Math.max(2, A('D17@hafif') - A('D17@bir') + .6));
    SET.belge(B, 'ZIMBARDO · PRISONEXP.ORG · HAZİRAN 2018', ['Gardiyan rolündeki birinden "kararlı"', 've "işin içinde" olmasını istemek,', 'gerçek cezaevlerinde müdürlerin', 'yaptığı baskının yanında hafif kalır.'], p,
      { px: 42, w: 1240, x: lerp(340, 200, ks), y: lerp(150, 110, ks), vurgu: [3], vurguA: R(st, 'D17@hafif', 1, E.lin), zemin: .38 });
    if (ks > 0) {   // döküm şeridi (Bant A, 9:45) sağdan girer, belgenin altına
      const x = lerp(2000, 720, ks), y = 610, w = 1000, h = 150, k = B.k, l = B.l;
      k.save(); k.fillStyle = B.ton(.55); k.fillRect(x + 12, y + 14, w, h); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
      B.renkBoya(g => g.rect(x + 34, y + 80, w - 68, 44), .6, 0);
      l.save(); l.fillStyle = '#fff'; l.fillRect(x, y, w, h); l.strokeStyle = '#000'; l.lineWidth = 1.6; l.strokeRect(x, y, w, h); l.fillStyle = '#000'; l.font = '700 26px "Courier Prime"'; l.textBaseline = 'middle'; l.fillText('BANT A · 9:45', x + 40, y + 36);
      l.font = '700 30px "Courier Prime"'; l.fillText('MÜDÜR: kararlı olacaksın, işin içinde olacaksın.', x + 40, y + 102); l.restore();
    }
  }, { ...KAG, over: ZM(KU('Zimbardo 2018, prisonexp.org (çevirisi bizim)'), 'D17@bir', 8) });

  // P62 orta: iki belge yan yana, eşit büyüklük: Zimbardo 2018 ↔ Le Texier 2019; sağdaki "lö"de gelir; "ayrıntılı" ve "doğrudan"da vurgu
  sahne('P62', 'D18', 'karsi', 'orta', (B, st) => {
    B.cam(960, 470, 1 + st.lt * .01);
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = B.ton(.36); k.fillRect(-300, -300, 2600, 1700); k.restore();
    const sag = R(st, 'D18@lö', .8, E.out3), pL = clamp((st.lt - .2) / 3.5), pR = clamp((st.t - A('D18@lö') - .3) / 2.2);
    const sayfa = (x, y, bas, sat, p, vurgu, va) => {
      const w = 760, h = 470;
      k.save(); k.fillStyle = B.ton(.6); k.fillRect(x + 12, y + 14, w, h); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
      l.save(); l.fillStyle = '#fff'; l.fillRect(x, y, w, h); l.strokeStyle = '#000'; l.lineWidth = 1.6; l.strokeRect(x, y, w, h); l.fillStyle = '#000'; l.font = '700 28px "Courier Prime"'; l.textBaseline = 'middle'; l.fillText(bas, x + 50, y + 56);
      l.lineWidth = 1.4; l.beginPath(); l.moveTo(x + 50, y + 88); l.lineTo(x + w - 50, y + 88); l.stroke();
      l.font = '700 38px "Courier Prime"'; const top = sat.reduce((a, s) => a + s.length, 0); let kalan = Math.floor(top * p);
      sat.forEach((s, i) => { const yy = y + 160 + i * 64; if (vurgu.includes(i) && va > 0) B.renkBoya(g => g.rect(x + 36, yy - 24, (w - 72) * va, 48), .6, 0); l.fillText(s.slice(0, Math.max(0, kalan)), x + 50, yy); kalan -= s.length; });
      l.restore();
    };
    sayfa(160, 200, 'ZIMBARDO · 2018', ['Etkili bir gardiyan olmak', 'için resmî ya da ayrıntılı', 'hiçbir talimat vermedik.'], pL, [1, 2], R(st, 'D18@ayrıntılı', .6));
    if (sag > 0) sayfa(lerp(1500, 1000, sag), 200, 'LE TEXIER · 2019, s. 7', ['Yukarıda sunulan kanıtlar', 'bu ifadeyle doğrudan', 'çelişiyor.'], pR, [1, 2], R(st, 'D18@doğrudan', .6));
  }, { ...KAG, over: ZM(KU('Zimbardo 2018, prisonexp.org · Le Texier 2019, s. 7 (çevirileri bizim)'), null, 8) });

  // P63 geniş: gözlem odası; monitörde sakin sayım (ilk vardiyalar); geri çekilme; "rağmen"de müdür geriye yaslanır, "baskın"da Mark başını eğer
  sahne('P63', 'D19', 'gozlem', 'genis', (B, st) => {
    B.cam(960, 520, 1.12 - .1 * E.io2(clamp(st.lt / 10)));
    const y = R(st, 'D19@rağmen', 1), d = R(st, 'D19@baskın', .8);
    oda(B, st, { mudurO: { govde: -.12 * y, bas: .08 - .06 * y, kolO: [lerp(.45, .25, y), lerp(1.1, 1.4, y)] }, markO: { bas: .12 + .08 * d },
      monitor: (B2) => bodrum(B2, st, { sayim: 6, gardiyanlar: [{ z: .3, u: .1, kol: [.1, .4] }], kose: { z: .55, u: .8 } }) });
  }, { ...KK, over: ZM(KU('Zimbardo 2018, prisonexp.org'), 'D19@zimbardoya', 8) });
})();
