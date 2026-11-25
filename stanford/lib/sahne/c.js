// III. Bant (D01–D19): arşiv kutusu → gözlem odası (ilk kez, ters açı) → bantın dökümü → müdürün yazısı, yurt, kurallar → Zimbardo 2018 ↔ Le Texier 2019.
// Gözlem odası ve masa: kâğıt + kuru fırça (.6). Işık MASA LAMBASINDAN teybin üstüne düşer (tavandan sarkan tek koni yok: sorgu mizanseni okunuyordu).
//   İki siluet eşit yükseklikte; kimse ışığın altında oturmaz. Siluetler üç plakaya basılır (çizgi + ton + renk): monitörün ve ışığın önünde opak.
//   Oda her dönüşte başka açıdan: P43 önden geniş · P46 Mark'ın omzu üstünden · P51 monitör kadrajı doldurur · P53 tepeden · P55 müdür monitör önünde · P63 arkadan, ikisi monitöre bakar.
// Belge ve döküm: kâğıt, kuru yok. Yazı levhası plan içinde ≤ 8 sn kesintisiz; uzun cümlelerde levhanın önüne ya da arasına görüntü girer (monitör, daktilo, 2018 ekranı, arşiv kutusu, teyp).
// Renk yalnız teybin kehribar ışığında, kırmızı kayıt lambasında ve belgedeki kehribar vurgu şeridinde.
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
  // makara açısı: ts (film zamanı) anında yavaşlayıp durur
  const aci = (t, hz, ts = 1e9) => TAU * hz * (t < ts ? t : ts + (1 - Math.exp(-(t - ts) * 2.5)) / 2.5);
  const DOLU = { sol: .97, sag: .97 };   // sarılı bant makarayı doldurur: iç içe halka görünmez
  const quad = (g, a, b, c, d) => { g.beginPath(); g.moveTo(...a); g.lineTo(...b); g.lineTo(...c); g.lineTo(...d); g.closePath(); };
  const tumZemin = (B, d) => { const k = B.k; k.save(); k.fillStyle = B.ton(d); k.fillRect(-900, -900, 3800, 2900); k.restore(); };
  // Zaman çizelgesi sürümü: eski tahmini çizelgede D03, D18, D19 var; senaryo rev2'de D03 yok, D17–D19 tek cümle (D17), D01–D02 kısaldı.
  //   Çapalar ikisinde de çalışır: VAR(id, kelime…) çizelgede bulunan ilk kelimenin çapasını verir (yoksa cümle başı; "kelime yok" yazmaz).
  const ESKI = !!(window.CUES && CUES.D18);
  const nW = w => w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  const VAR = (id, ...ws) => { for (const w of ws) { const [x, n = 0] = w.split('#'); let c = 0; for (const q of (window.WORDS || [])) if (q.id === id && q.w.startsWith(nW(x)) && c++ === +n) return id + '@' + w; } return id; };

  // ── opak siluet: çizgi plakası + ton plakası (siyah) + renk plakası (siyah: monitör maskesini siler). Yarı saydam baş hatası buradan. ──
  const kisi3 = (B, x, y, boy, op) => {
    const s = { ...op, renk: '#000', sandalyeRenk: '#000' };
    FIG.kisi(B.k, x, y, boy, s); FIG.kisi(B.c, x, y, boy, s); return FIG.kisi(B.l, x, y, boy, op);
  };
  const yakin3 = (B, tip, x, y, boy, o) => {
    FIG.kisi(B.k, x, y + boy * .96, boy, { tip, f: o.f ?? 1, kolO: o.kolO || [.1, .3], kolA: o.kolA || [-.1, .2], bas: o.bas || 0, ...o, renk: '#000' });
    return yakinFig(B, tip, x, y, boy, o);
  };
  // arkadan baş-omuz (P63): baş (x, y) merkez, r yarıçap; o.dy baş öne eğik (+), o.dx yana; kulaklar başı torbadan ayırır
  function sirt(B, x, y, r, o = {}) {
    const hx = x + (o.dx || 0) * r, hy = y + (o.dy || 0) * r, yx = o.yaslan || 0;
    const parca = [
      g => { g.moveTo(x - 3.2 * r, y + 7 * r); g.lineTo(x - 3 * r, y + 2.7 * r + yx * r); g.quadraticCurveTo(x - 2.8 * r, y + 1.6 * r + yx * r, x - 1.6 * r, y + 1.4 * r + yx * r);
        g.quadraticCurveTo(x - .75 * r, y + 1.25 * r, x - .5 * r, y + .55 * r); g.lineTo(x + .5 * r, y + .55 * r); g.quadraticCurveTo(x + .75 * r, y + 1.25 * r, x + 1.6 * r, y + 1.4 * r + yx * r);
        g.quadraticCurveTo(x + 2.8 * r, y + 1.6 * r + yx * r, x + 3 * r, y + 2.7 * r + yx * r); g.lineTo(x + 3.2 * r, y + 7 * r); g.closePath(); },
      g => g.ellipse(hx, hy, .8 * r, r, (o.dx || 0) * .3, 0, TAU),
      g => g.ellipse(hx - .8 * r, hy + .12 * r, .16 * r, .3 * r, -.15, 0, TAU),
      g => g.ellipse(hx + .8 * r, hy + .12 * r, .16 * r, .3 * r, .15, 0, TAU),
      g => { g.moveTo(hx - .78 * r, hy - .25 * r); g.quadraticCurveTo(hx - .4 * r, hy - 1.18 * r, hx + .2 * r, hy - 1.06 * r); g.quadraticCurveTo(hx + .75 * r, hy - .9 * r, hx + .8 * r, hy - .2 * r); g.closePath(); },   // kısa saç (tepe hafif kabarık)
    ];
    for (const g of [B.l, B.k, B.c]) { g.save(); g.fillStyle = '#000'; for (const p of parca) { g.beginPath(); p(g); g.fill(); } g.restore(); }
  }
  // ── masa lambası (ayarlı kol): taban masada (bx, my), başlık teybe eğik; ışık kaması başlığın ağzından masaya (ton plakasında açık) ──
  //   yon 1: başlık sola. Tavandan sarkan lamba değil: alçak, masada duran bir çalışma lambası.
  function lamba(B, bx, my, a, yon, hedef, zy = my, ol = 1) {
    const k = B.k, l = B.l, P = (dx, dy) => [bx - yon * dx * ol, my + dy * ol];
    const b0 = P(0, -8), el = P(-70, -250), J = P(70, -400);
    let d = [hedef[0] - J[0], hedef[1] - J[1]]; const dl = Math.hypot(...d); d = [d[0] / dl, d[1] / dl]; const n = [-d[1], d[0]];
    const M = [J[0] + d[0] * 120, J[1] + d[1] * 120], ap = [J[0] - d[0] * 40, J[1] - d[1] * 40];
    const m1 = [M[0] + n[0] * 78, M[1] + n[1] * 78], m2 = [M[0] - n[0] * 78, M[1] - n[1] * 78];
    const yer = q => { const u = (zy - ap[1]) / (q[1] - ap[1]); return [ap[0] + (q[0] - ap[0]) * u, zy]; };
    const d1 = yer(m1), d2 = yer(m2);
    if (a > 0) {
      const g = k.createLinearGradient(M[0], M[1], M[0], zy); g.addColorStop(0, `rgba(255,255,255,${.92 * a})`); g.addColorStop(1, `rgba(255,255,255,${.5 * a})`);
      k.save(); k.fillStyle = g; quad(k, m1, m2, d2, d1); k.fill();
      const r = rng(5); k.strokeStyle = `rgba(255,255,255,${.3 * a})`;   // kaynak kenarda kuru fırça
      for (let i = 0; i < 20; i++) { const u = r(), s = r() < .5, A0 = s ? m1 : m2, A1 = s ? d1 : d2, xx = lerp(A0[0], A1[0], u), yy = lerp(A0[1], A1[1], u); k.lineWidth = 1 + r() * 3; k.beginPath(); k.moveTo(xx, yy); k.lineTo(xx + (r() - .5) * 26, yy + 30 + r() * 80); k.stroke(); }
      k.restore();
    }
    return { ciz: () => {
      l.save(); l.strokeStyle = '#000'; l.fillStyle = '#000'; l.lineCap = 'round'; l.lineJoin = 'round';
      l.beginPath(); l.ellipse(b0[0], b0[1], 78 * ol, 15 * ol, 0, 0, TAU); l.fill();
      l.lineWidth = 11; l.beginPath(); l.moveTo(...b0); l.lineTo(...el); l.lineTo(...J); l.stroke();
      l.beginPath(); l.arc(el[0], el[1], 12, 0, TAU); l.fill();
      const j1 = [J[0] + n[0] * 22, J[1] + n[1] * 22], j2 = [J[0] - n[0] * 22, J[1] - n[1] * 22];
      quad(l, j1, m1, m2, j2); l.fill(); l.restore();
    }, d1, d2 };
  }
  // ── gözlem odası (önden): koyu duvar, monitör, masa, teyp, masa lambası; iki oturan siluet (sol müdür, sağ Mark) eşit yükseklikte ──
  // o: { monitor (çizim fn | false), mon [x,y,w,h], isik, ang, vu, mudur/mark (false), mudurO, markO, onPlan(B) }
  function oda(B, st, o = {}) {
    const t = st.t, my = 690, k = B.k, l = B.l, tx = 1060;
    SET.karanlik(B, o.koyu ?? .78);
    k.save(); k.fillStyle = B.ton(.86); for (let i = 0; i < 6; i++) k.fillRect(-200 + i * 420, -600, 10, my + 600); k.restore();   // duvar panoları (yalnız dikey)
    if (o.monitor !== false) { const m = o.mon || [150, 150, 520, 380]; SET.monitorIci(B, m[0], m[1], m[2], m[3], o.monitor || (B2 => bodrum(B2, st, {}))); }
    const L = lamba(B, 1190, my - 60, o.isik ?? 1, 1, [tx - 20, my - 240], my);
    k.save(); k.fillStyle = B.ton(.9); k.fillRect(260, my + 8, 1500, 400); k.restore();
    l.save(); l.fillStyle = '#000'; l.fillRect(260, my + 30, 1500, 500); l.restore();
    const ia = o.isik ?? 1;   // masanın üst kenarı yalnız lambanın havuzunda açık
    if (ia > 0) { k.save(); k.globalAlpha = ia; k.fillStyle = '#fff'; k.fillRect(L.d1[0] - 40, my + 4, L.d2[0] - L.d1[0] + 80, 10); k.restore(); }
    SET.surtme(B.l, 300, 1700, my + 30, 11, { n: 50, boy: 260, acik: false });
    L.ciz();   // lamba teybin arkasında durur (tabanı teyple örtülür)
    const tp = SET.teyp(B, tx, my - 250, .62, t, { ang: o.ang, kayit: o.kayit ?? 1, vu: o.vu, hz: o.hz, ...DOLU });
    const kisiCiz = (x, f, tip, oo) => kisi3(B, x, my + 330, 760, { tip, f, bacak: 'otur', sandalye: true, ...KOL, bas: .08, gozluk: false, cop: false, ...oo });
    SET.fincan(B, 1420, my, t, 1); SET.fincan(B, 1720, my, t, 2);   // büro: sorgu odası okunmasın
    // iki kişi aynı tarafta, yan yana, ikisi de monitörlere bakar (karşılıklı oturuş yok; başkan kararı, üç okuyucunun ortak bulgusu)
    if (o.mark !== false) kisiCiz(1680, -1, 'gardiyan', o.markO || {});
    if (o.mudur !== false) kisiCiz(1380, -1, 'mudur', o.mudurO || {});
    return { masaY: my, teyp: tp };
  }
  // monitör kadrajı doldurur (kâğıt planında ekran maskesi): bezel ve masa kenarı görünür
  function monitorTam(B, st, ciz) {
    tumZemin(B, .82);
    SET.monitorIci(B, 230, 70, 1460, 820, ciz);
  }
  // yazılma ilerlemesi: zaman[i] satır başı çapası ('on': önceden basılı, null: boş satır); son: son satırın bitişi
  function ilerle(st, satirlar, zaman, son) {
    const top = satirlar.reduce((a, r) => a + r.length, 0); let yaz = 0, c = 0;
    for (let i = 0; i < satirlar.length; i++) {
      if (!satirlar[i].length) { if (yaz > 0) c = i; continue; }
      if (zaman[i] === 'on') { yaz += satirlar[i].length; c = i + 1; continue; }
      const a0 = A(zaman[i]); let a1 = A(son);
      for (let j = i + 1; j < satirlar.length; j++) if (zaman[j] && zaman[j] !== 'on') { a1 = A(zaman[j]); break; }
      const q = clamp((st.t - a0) / Math.max(.4, a1 - a0)); yaz += satirlar[i].length * q; if (q > 0) c = i + q;
    }
    return { p: yaz / top, c };
  }

  // ── döküm sayfası: masada daktilo sayfası, sağ üstünde küçük teyp (makaralar döner, kayıt lambası). o.kam [x,y,z,u]: kamerayı u ile oraya götürür ──
  function dokum(B, st, satirlar, zaman, son, o = {}) {
    const { p } = ilerle(st, satirlar, zaman, son);
    const c = [lerp(850, 880, st.p), lerp(400, 400 + Math.min(110, satirlar.length * 16), E.io2(p)), 1.12 + st.lt * .012];   // kamera yazılan satırı izler
    if (o.kam) { const u = o.kam[3]; B.cam(lerp(c[0], o.kam[0], u), lerp(c[1], o.kam[1], u), lerp(c[2], o.kam[2], u)); } else B.cam(...c);
    const r = SET.belge(B, UST, satirlar, p, { px: 38, w: 1100, x: 200, y: 170, zemin: .72, vurgu: o.vurgu, vurguA: o.vurguA, h: Math.max(470, satirlar.length * 57 + 230) });
    if (o.imlec && Math.floor(st.t * 2.2) % 2 === 0) { const l = B.l, x = r.x + 38 * 1.4 + o.imlec[1] * 22.8, y = r.y + 38 * 3.6 + o.imlec[0] * 57; l.save(); l.fillStyle = '#000'; l.fillRect(x, y - 18, 20, 36); l.restore(); }
    SET.teyp(B, 1520, 180, .45, st.t, { ang: o.ang, hz: .45, vu: o.vu, kayit: 1, vuIsik: .7, ...DOLU });
    return r;
  }
  // ── Mark yakın planı: baş-omuz profil, karanlık; ışık yalnız masada (alt), başın yanında açık leke yok. o.f 1: sağa bakar ──
  function markYakin(B, st, o = {}) {
    SET.karanlik(B, .8);
    const k = B.k, my = o.masaY ?? 930, ix = o.isikX ?? 900, f = o.f ?? -1;
    k.save(); k.fillStyle = B.ton(.18); k.beginPath();
    if (f < 0) { k.moveTo(-300, my); k.lineTo(ix, my); k.lineTo(ix + 160, 1400); k.lineTo(-300, 1400); }
    else { k.moveTo(2300, my); k.lineTo(ix, my); k.lineTo(ix - 160, 1400); k.lineTo(2300, 1400); }
    k.closePath(); k.fill(); k.restore();
    if (f < 0) SET.surtme(B.k, -200, ix, my + 4, 13, { n: 30, boy: 120, acik: false }); else SET.surtme(B.k, ix, 2100, my + 4, 13, { n: 30, boy: 120, acik: false });
    if (o.teyp) SET.teyp(B, o.teyp[0], o.teyp[1], o.teyp[2], st.t, { hz: .45, kayit: 1, vuIsik: .75, ...DOLU });
    yakin3(B, 'gardiyan', o.x ?? 1220, o.y ?? 380, o.boy ?? 2200, { f, gozluk: false, cop: false, bas: o.bas ?? .06, govde: o.govde ?? 0, kolO: o.kolO || [.5, 1.1], kolA: o.kolA || [.3, .9], serbest: 1 });
  }
  // yurt koridoru (Mayıs 1971, video): düz tavan (floresan sırası yok), parmaklıksız ahşap kapılar, uçta jaluzili pencere, panoda kâğıtlar
  function yurt(B, st) {
    const K = D.koridor(B, st.t, { kapilar: 0, levha: false, sonD: .1, solD: .5, sagD: .56, isik: .8 });
    const k = B.k, l = B.l, zM = .86;
    k.save(); k.fillStyle = B.ton(.22); quad(k, K.P(0, -1, 1), K.P(zM, -1, 1), K.P(zM, 1, 1), K.P(0, 1, 1)); k.fill();   // tavan düz
    k.fillStyle = B.ton(.28); for (let i = 1; i < 9; i++) { const u = -1 + i * .22; quad(k, K.P(zM, u - .012, .12), K.P(zM, u + .012, .12), K.P(zM, u + .012, .9), K.P(zM, u - .012, .9)); k.fill(); }   // pencere: yalnız dikey jaluzi
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
  // arşiv kutusu (SC0750): ac kapak 0→1, kalk ilk makara kutusunun yükselmesi 0→1 (P41; P62'de geri döner)
  function kutu(B, ac, kalk) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = B.ton(.72); k.fillRect(-300, -300, 2600, 1700); k.fillStyle = B.ton(.5); k.fillRect(-300, 740, 2600, 900); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.moveTo(-300, 740); l.lineTo(2300, 740); l.stroke(); l.restore();
    const x0 = 580, x1 = 1280, yt = 470, yb = 800, dx = 110, dy = 70;
    const ON = [[x0, yt], [x1, yt], [x1, yb], [x0, yb]], YAN = [[x1, yt], [x1 + dx, yt - dy], [x1 + dx, yb - dy], [x1, yb]], AG = [[x0, yt], [x1, yt], [x1 + dx, yt - dy], [x0 + dx, yt - dy]];
    const yol = (g, P) => { g.beginPath(); poly(g, P, true); };
    l.save(); l.fillStyle = '#fff'; for (const P of [ON, YAN, AG]) { yol(l, P); l.fill(); } l.restore();
    const th = ac * 1.9, v = [-dx * Math.cos(th), dy * Math.cos(th) - 230 * Math.sin(th)];
    const KAP = [[x0 + dx, yt - dy], [x1 + dx, yt - dy], [x1 + dx + v[0], yt - dy + v[1]], [x0 + dx + v[0], yt - dy + v[1]]];
    const kapak = () => { k.save(); yol(k, KAP); k.fillStyle = B.ton(th < PI / 2 ? .52 : .62); k.fill(); k.restore(); l.save(); l.fillStyle = '#fff'; yol(l, KAP); l.fill(); l.strokeStyle = '#000'; l.lineWidth = 3; yol(l, KAP); l.stroke(); l.restore(); };
    k.save(); yol(k, AG); k.fillStyle = B.ton(.88); k.fill(); k.restore();
    if (th >= PI / 2) kapak();
    const kut = [[650, .03, 'A'], [730, -.02, 'B'], [805, .05, 'C'], [880, -.03, 'D'], [955, .02, 'E'], [1035, -.05, 'F'], [1110, .03, 'G'], [1185, -.02, 'H']];
    kut.forEach(([x, a, ad], i) => {
      const ky = yt - 46 + (i % 3) * 7 - (i === 0 ? 170 * kalk : 0);
      for (const g of [k, l]) { g.save(); g.translate(x + 30, ky); g.rotate(a); }
      k.fillStyle = B.ton(.3 + (i % 2) * .12); k.fillRect(-30, 0, 62, 170);
      l.fillStyle = '#fff'; l.fillRect(-30, 0, 62, 170); l.strokeStyle = '#000'; l.lineWidth = 2.5; l.strokeRect(-30, 0, 62, 170);
      l.fillStyle = '#000'; l.font = '700 24px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText(ad, 1, 22);
      for (const g of [k, l]) g.restore();
    });
    k.save(); yol(k, ON); k.fillStyle = B.ton(.42); k.fill(); yol(k, YAN); k.fillStyle = B.ton(.56); k.fill(); k.fillStyle = '#fff'; k.fillRect(800, 560, 280, 120); k.restore();
    l.save(); l.fillStyle = '#fff'; yol(l, ON); l.fill(); yol(l, YAN); l.fill(); l.strokeStyle = '#000'; l.lineWidth = 3; yol(l, ON); l.stroke(); yol(l, YAN); l.stroke(); l.beginPath(); l.moveTo(x0 + dx, yt - dy); l.lineTo(x1 + dx, yt - dy); l.stroke();
    l.lineWidth = 2; l.strokeRect(800, 560, 280, 120); l.fillStyle = '#000'; l.font = '700 58px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText('SC0750', 940, 620); l.restore();
    if (th < PI / 2) kapak();
  }
  // daktilo (önden): merdane ry'de; vur 0..1 harf çubuğu vuruşu; hx vuruş noktası. Kâğıt merdanenin arkasından çıkar (gövde kâğıdın altını örter)
  function daktilo(B, cx, ry, vur, hx) {
    const k = B.k, l = B.l;
    const govde = [[cx - 650, ry + 36], [cx + 650, ry + 36], [cx + 780, ry + 600], [cx - 780, ry + 600]];
    B.renkOrt(g => g.rect(cx - 900, ry + 10, 1800, 800));   // altta kalan vurgu şeridi gövdeden görünmesin
    k.save(); k.fillStyle = B.ton(.74); quad(k, ...govde); k.fill(); k.fillStyle = B.ton(.9); k.fillRect(cx - 900, ry + 600, 1800, 400); k.restore();
    l.save(); l.fillStyle = '#fff'; quad(l, ...govde); l.fill(); l.strokeStyle = '#000'; l.lineWidth = 4; quad(l, ...govde); l.stroke();
    // merdane ve topuzlar (dolu disk; halka yok)
    l.fillStyle = '#000'; l.beginPath(); l.roundRect(cx - 720, ry - 24, 1440, 56, 26); l.fill();
    for (const s of [-1, 1]) { l.beginPath(); l.arc(cx + s * 760, ry + 4, 46, 0, TAU); l.fill(); }
    // şerit makaraları (dolu, koyu)
    for (const s of [-1, 1]) { k.save(); k.fillStyle = B.ton(.88); k.beginPath(); k.ellipse(cx + s * 360, ry + 120, 110, 42, 0, 0, TAU); k.fill(); k.restore(); l.lineWidth = 3; l.beginPath(); l.ellipse(cx + s * 360, ry + 120, 110, 42, 0, 0, TAU); l.stroke(); }
    // çubuk sepeti ve vuran çubuk
    k.save(); k.fillStyle = B.ton(.92); k.beginPath(); k.ellipse(cx, ry + 230, 240, 110, 0, PI, TAU); k.fill(); k.restore();
    const ux = lerp(cx - 60, hx, vur), uy = lerp(ry + 200, ry + 6, vur);
    l.lineWidth = 9; l.lineCap = 'round'; l.beginPath(); l.moveTo(cx, ry + 300); l.lineTo(ux, uy); l.stroke();
    // tuşlar: dört sıra dolu koyu disk + ara çubuğu
    for (let r = 0; r < 4; r++) for (let i = 0; i < 11 - (r === 3 ? 1 : 0); i++) {
      const x = cx - 520 + r * 26 + i * 104, y = ry + 340 + r * 62, bas = vur > .5 && (i * 7 + r * 3 + Math.floor(hx)) % 11 === 0;
      l.beginPath(); l.ellipse(x, y + (bas ? 6 : 0), 30, 22, 0, 0, TAU); l.fill();
    }
    l.beginPath(); l.roundRect(cx - 320, ry + 560, 640, 30, 14); l.fill();
    l.restore();
  }

  // P41 orta: arşiv kutusu (SC0750) açılır; "deneyin arşivinden"de kapak devrilir, içinde düz makara kutuları; "yayımladı"da biri yukarı kalkar
  sahne('P41', 'D01', 'arsiv', 'orta', (B, st) => {
    B.cam(960, 500, 1.02 + st.lt * .018);
    kutu(B, R(st, VAR('D01', 'deneyin', 'peki'), 1.3, E.io3), R(st, VAR('D01', 'yayımladı', 'iki'), .6, E.out3));
  }, { ...KAG, over: KU('Stanford Üniversitesi arşivi, SC0750 (Stanford Prison Experiment)', { t0: 1.2 }) });

  // P42 ayrıntı: makara kutusu, el yazısı özgün etiket "Tape A" (künye: Bant A); "banda"da makara çıkarılır, "dakikalık"ta bant ucu sarkar
  sahne('P42', VAR('D01', 'aynı', 'araştırmacılar'), 'arsiv', 'ayrinti', (B, st) => {
    B.cam(960, 520, 1.05 + st.lt * .02);
    const k = B.k, l = B.l, cik = R(st, 'D01@banda', 1.2, E.io3), don = R(st, 'D01@dakikalık', 1.5, E.lin);
    k.save(); k.fillStyle = B.ton(.55); k.fillRect(-300, -300, 2600, 1700); k.restore();
    const bx = 560, by = 330, bw = 800, bh = 540;
    k.save(); k.fillStyle = B.ton(.8); k.fillRect(bx + 16, by + 18, bw, bh); k.fillStyle = B.ton(.85); k.fillRect(bx, by, bw, bh); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(bx, by, bw, bh); l.restore();
    const mx = 960 + cik * 140, my = 600 - cik * 250, mr = 240, an = .3 + don * 1.2 + cik * .5;
    k.save(); k.fillStyle = B.ton(.3); k.beginPath(); k.arc(mx, my, mr, 0, TAU); k.fill(); k.restore();
    l.save(); l.fillStyle = '#fff'; l.beginPath(); l.arc(mx, my, mr, 0, TAU); l.fill(); l.strokeStyle = '#000'; l.lineWidth = 5; l.stroke(); l.translate(mx, my); l.rotate(an);
    k.save(); k.translate(mx, my); k.rotate(an);
    for (let i = 0; i < 3; i++) { l.rotate(TAU / 3); k.rotate(TAU / 3); k.beginPath(); k.ellipse(0, -mr * .55, mr * .16, mr * .25, 0, 0, TAU); k.fillStyle = B.ton(.85); k.fill(); l.beginPath(); l.ellipse(0, -mr * .55, mr * .16, mr * .25, 0, 0, TAU); l.stroke(); }
    k.restore(); l.beginPath(); l.arc(0, 0, mr * .1, 0, TAU); l.fillStyle = '#000'; l.fill(); l.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.moveTo(mx + mr * .8, my + mr * .2); l.quadraticCurveTo(mx + mr * 1.15, my + 200, mx + mr * .95 + 120 * don, my + 230 + 170 * don); l.stroke(); l.restore();
    const cy = by + bh * .55, ch = bh * .45;
    k.save(); k.fillStyle = B.ton(.4); k.fillRect(bx, cy, bw, ch); k.fillStyle = '#fff'; k.fillRect(bx + 240, cy + 40, 320, 130); k.restore();
    l.save(); l.fillStyle = '#fff'; l.fillRect(bx, cy, bw, ch); l.strokeStyle = '#000'; l.lineWidth = 4; l.strokeRect(bx, cy, bw, ch); l.lineWidth = 2; l.strokeRect(bx + 240, cy + 40, 320, 130);
    l.translate(bx + 400, cy + 106); l.rotate(-.05); l.fillStyle = '#000'; l.font = 'italic 600 84px "Cormorant Garamond"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText('Tape A', 0, 0); l.restore();
  }, { ...KAG, over: ZM(KU('Özgün etiket “Tape A”: Bant A · yaklaşık 18 dakika'), 'D01@on#1', 6) });

  // P43 geniş, DÖNÜŞ: gözlem odası ilk kez, önden; masa lambası plan başında yanar, makaralar dönmeye başlar, monitörde koridor
  sahne('P43', 'D02', 'gozlem', 'genis', (B, st) => {
    B.cam(960, 520, 1 + st.lt * .012);
    oda(B, st, { isik: ramp(st.lt, .15, .5, E.out3), ang: aci(st.t - st.at - .6 > 0 ? st.t - st.at - .6 : 0, .45),
      mudurO: { bas: .08 + .06 * R(st, 'D02@gündüz', .8) }, markO: { bas: .12 - .08 * R(st, VAR('D02', 'zimbardo', 'gardiyan'), .8) },
      monitor: (B2) => bodrum(B2, st, { gardiyanlar: [{ z: .4, u: .15 }] }) });
  }, { ...KK, over: OV(ZM(ETK('MÜDÜR · DAVID JAFFE', 520, 760, { d: 4.5 }), 'D02@müdür', 5), ZM(ETK('GÜNDÜZ VARDİYASI GARDİYANI', 1440, 760, { d: 4.5 }), 'D02@gündüz', 5),
    ZM(KU("Gün: Le Texier'ye göre üçüncü, Zimbardo'ya göre ilk"), VAR('D02', 'lö', 'müdür'), 6)) });

  // P44 yakın: Mark, karanlık oda; adı söylenince başını kaldırır, "yirmi"de hafif eğer. (rev2'de D03 yok: plan "Mark" sözcüğüne bağlanır, ≈ 1 sn)
  const M3 = ESKI ? 'D03@mark' : 'D02@mark';
  sahne('P44', ESKI ? 'D03' : 'D02@gardiyan', 'gozlem', 'yakin', (B, st) => {
    B.cam(960, 540, 1.02 + st.lt * .02);
    const kalk = R(st, M3, .7);
    markYakin(B, st, { bas: lerp(.2, .04, kalk) + .05 * (ESKI ? R(st, 'D03@yirmi', .8) : 0), govde: lerp(.08, 0, kalk), teyp: [380, 760, .9] });
  }, { ...KK, over: ZM(ETK('MARK', 560, 400, { d: 4 }), M3, 4.5) });

  // P45 ayrıntı: teyp (kayıt lambası) → "bu"da kamera döküm sayfasına iner, ilk satırlar sözle yazılır → "sayım"da monitör: sayım sürerken kapının dışında oturan gardiyan
  sahne('P45', 'D04', 'dokum', 'ayrinti', (B, st) => {
    if (st.t >= A('D04@sayım')) {
      const u = R(st, 'D04@oturmak', 2.2, E.io2);
      B.cam(lerp(960, 1080, u), lerp(480, 470, u), 1.02 + .1 * u + (st.t - A('D04@sayım')) * .01);
      monitorTam(B, st, B2 => bodrum(B2, st, { sayim: 5, sayan: { z: .32, x0: 480, v: 30 }, kose: { z: .5, u: .86 } }));
      return;
    }
    const u = 1 - R(st, 'D04@giriyor', .9, E.io3);
    dokum(B, st, ['MÜDÜR: Bu sabah işe pek karışmadığını', '       fark ettik. Biraz da benim', '       suçum; [...]'], ['D04@bu', 'D04@fark', 'D04@suçum'], 'D04@sayım',
      { kam: [1520, 262, 2.6, u] });
  }, { ...KAG, over: ZM(KU('Stanford arşivi, Bant A, 8:39–9:21 (çeviri ve konuşan adları bizim)'), 'D04@bu', 6) });

  // P46 orta: Mark'ın omzu üstünden müdür (monitörün önünde); "her"de müdür öne eğilir; "olacak"ta Mark (önde, koyu) başını önüne eğer
  sahne('P46', 'D05', 'gozlem', 'orta', (B, st) => {
    B.cam(700, 500, 1.45 + st.lt * .015);
    const e = R(st, 'D05@her', .9), eg = R(st, 'D05@olacak', .8);
    oda(B, st, { mark: false, mudurO: { govde: .2 * e, bas: .06 + .06 * e, kolO: [.45 + .15 * e, 1.1 - .1 * e] },
      monitor: (B2) => bodrum(B2, st, { sayim: 3, gardiyanlar: [{ z: .35, u: .2 }] }) });
    kisi3(B, 1265, 1720, 1700, { tip: 'gardiyan', f: -1, bacak: 'otur', sandalye: false, gozluk: false, cop: false, kolO: [.6, 1.1], kolA: [.4, 1.1], bas: .04 + .16 * eg, govde: .04 * eg });
  }, { ...KK, over: ZM(QT('“Ama gardiyanların şunu bilmesi gerek: her gardiyan, bizim sert gardiyan dediğimiz şey olacak.”', 'Bant A, 9:27', { y: 170, x: 820, maxW: 1100 }), null, 7.5) });

  // P47 ayrıntı: monitör: duvara yaslanmış tek gardiyan ("Ben pek sert değilim"); "denemen"de doğrulur, "sindirmen"de başını kaldırıp elleri beline
  //   → "sert derken"de döküm: MARK satırı basılı gelir, müdürün tanımı sözle yazılır, "kararlı"da kehribar şerit
  sahne('P47', 'D06', 'dokum', 'ayrinti', (B, st) => {
    if (st.t < A('D06@sert#1') - .15) {
      const d = R(st, 'D06@denemen', .9, E.io2), s = R(st, 'D06@sindirmen', .8, E.io2);
      B.cam(lerp(1060, 1140, st.lt / 6), 470, 1.05 + st.lt * .03);
      monitorTam(B, st, B2 => bodrum(B2, st, { gardiyanlar: [{ z: .22, u: .8, f: -1, govde: lerp(-.13, 0, d), bas: lerp(.16, -.02, s), kol: [lerp(-.05, .2, s), lerp(.1, .6, s)] }], kapiYok: ['R0'] }));
      return;
    }
    dokum(B, st, ['MARK:  Ben pek sert değilim.', '       [...]', 'MÜDÜR: Sert derken şunu kastediyorum:', '       kararlı olacaksın,', '       işin içinde olacaksın.'],
      ['on', 'on', 'D06@sert#1', 'D06@kararlı', 'D06@işin'], 'D06@olacaksın#1+0.5', { vurgu: st.t > A('D06@işin') ? [3, 4] : [3], vurguA: R(st, 'D06@kararlı', 1.2, E.lin) });
  }, { ...KAG, over: ZM(KU('Bant A, 9:36–9:51'), 'D06@sert#1', 5.5) });

  // P48 yakın: Mark polisi düşünür; başı önde başlar, "benden"de kalkar, "bağırmaya"da önkolu göğüs hizasına kalkar (dirsek bükük), "kısır"da baş öne
  sahne('P48', 'D07', 'gozlem', 'yakin', (B, st) => {
    B.cam(1000, 560, 1.1 + st.lt * .01);
    const kalk = R(st, 'D07@benden', .8), el = R(st, 'D07@bağırmaya', .7) * (1 - R(st, 'D07@kısır', 1));
    markYakin(B, st, { x: 1470, y: 400, boy: 2000, bas: lerp(.24, .05, kalk) + .1 * R(st, 'D07@kısır', 1), kolO: [lerp(.5, 1.0, el), lerp(1.1, 1.0, el)], isikX: 820, masaY: 960 });
  }, { ...KK, over: ZM(QT('“Benden istediğin şey, bence polisle hep bu kadar sorun çıkmasının sebebi.”', 'Bant A, 10:44', { y: 220, x: 600, maxW: 860 }), 'D07@benden', 8) });

  // P49 ayrıntı: döküm D08 (≈ 6 sn)
  sahne('P49', 'D08', 'dokum', 'ayrinti', (B, st) => {
    dokum(B, st, ['MARK:  Bana kalsa hiçbir şey yapmazdım.', '       Kendi hâline bırakırdım.', '', '       [...]'], ['D08@bana', 'D08@kendi', null, 'D08@biraz'], 'D08@sadece');
  }, { ...KAG, over: ZM(KU('Bant A, 11:10'), 'D08@bana', 6) });

  // P50 yakın: ışıkta masada duran aynalı gözlük; camlarda monitörün yansıması; "gardiyan"da yansımada küçük bir siluet yürür, "üniformasını"nda parıltı camda kayar
  sahne('P50', 'D08@sadece', 'gozlem', 'yakin', (B, st) => {
    B.cam(960 + st.lt * 6, 560, 1.04 + st.lt * .035);
    SET.karanlik(B, .84);
    const k = B.k, l = B.l, my = 470;
    k.save(); const g = k.createRadialGradient(960, 760, 80, 960, 760, 900); g.addColorStop(0, B.ton(.02)); g.addColorStop(1, B.ton(.55)); k.fillStyle = g; k.fillRect(-300, my, 2600, 1100);
    k.fillStyle = '#fff'; k.fillRect(-300, my - 4, 2600, 8); k.restore();
    const cx = 960, cy = 720, s = 2.7, sy = .78;
    const cam = sx => g2 => { g2.save(); g2.translate(cx, cy); g2.scale(s, s * sy); g2.beginPath(); g2.moveTo(sx * 16, -58); g2.bezierCurveTo(sx * 70, -66, sx * 112, -58, sx * 118, -40);
      g2.bezierCurveTo(sx * 122, -12, sx * 100, 8, sx * 74, 8); g2.bezierCurveTo(sx * 44, 8, sx * 18, -18, sx * 16, -58); g2.closePath(); g2.restore(); };
    k.save(); k.fillStyle = B.ton(.5, .8); k.beginPath(); k.ellipse(cx + 40, cy + 30, 300, 30, 0, 0, TAU); k.fill(); k.restore();
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 9; l.lineCap = 'round';
    for (const sx of [-1, 1]) { l.beginPath(); l.moveTo(cx + sx * 116 * s, cy - 44 * s * sy); l.lineTo(cx - sx * 30 * s, cy - 26 * s * sy); l.stroke(); }
    l.restore();
    const kay = R(st, 'D08@üniformasını', 2.2, E.io2), y0 = A('D08@gardiyan') - st.at;
    for (const sx of [-1, 1]) {
      l.save(); cam(sx)(l); l.fillStyle = '#fff'; l.fill(); l.restore();
      k.save(); cam(sx)(k); k.clip(); const gg = k.createLinearGradient(0, cy - 180, 0, cy + 30); gg.addColorStop(0, B.ton(.9)); gg.addColorStop(1, B.ton(.62)); k.fillStyle = gg; k.fillRect(cx - 400, cy - 220, 800, 280);
      // yansıma: monitörün dikdörtgeni (açık, eğik) ve içinde yürüyen küçük siluet
      const rx = cx + sx * 175 - 70, ry = cy - 120;
      k.fillStyle = B.ton(.38); k.beginPath(); k.roundRect(rx, ry, 150, 86, 12); k.fill();
      if (st.lt > y0) { k.save(); k.beginPath(); k.rect(rx, ry, 150, 86); k.clip(); SET.yuru(k, rx + 10, ry + 80, 58, st.lt - y0, { tip: 'gardiyan', f: 1, renk: B.ton(.85), gozluk: false, kolO: [.1, .2], kolA: [-.1, .2] }); k.restore(); }
      const px = lerp(cx - 380, cx + 420, kay); k.fillStyle = B.ton(.02); k.beginPath(); k.moveTo(px - 10, cy - 200); k.lineTo(px + 40, cy - 200); k.lineTo(px - 50, cy + 40); k.lineTo(px - 100, cy + 40); k.closePath(); k.fill(); k.restore();
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 7; cam(sx)(l); l.stroke(); l.restore();
    }
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 7; l.beginPath(); l.moveTo(cx - 16 * s, cy - 50 * s * sy); l.quadraticCurveTo(cx, cy - 58 * s * sy, cx + 16 * s, cy - 50 * s * sy); l.stroke(); l.beginPath(); l.moveTo(cx - 18 * s, cy - 61 * s * sy); l.lineTo(cx + 18 * s, cy - 61 * s * sy); l.stroke(); l.restore();
  }, { ...KK, over: ZM(QT('“Sadece bu gardiyan üniformasını giymek bile benim için ağır bir şey.”', 'Bant A, 13:51', { y: 200, maxW: 1300 }), 'D08@sadece', 7) });

  // P51 orta: monitör kadrajı doldurur (sayım: sayım tahtasıyla yürüyen gardiyan); müdür solda ona dönük; "reform"da önkolu kalkar, "bakın"da ekrana gösterir (dirsek bükük)
  sahne('P51', 'D09', 'gozlem', 'orta', (B, st) => {
    B.cam(980, 520, 1.02 + st.lt * .012);
    SET.karanlik(B, .82);
    const k = B.k, l = B.l, my = 930;
    SET.monitorIci(B, 690, 110, 1060, 640, B2 => bodrum(B2, st, { sayim: 5, sayan: { z: .3, x0: 470, v: 34 } }));
    k.save(); k.fillStyle = B.ton(.9); k.fillRect(-300, my + 8, 2600, 400); k.fillStyle = '#fff'; k.globalAlpha = .55; k.fillRect(700, my + 4, 1100, 8); k.restore();   // masa kenarı: monitörün ışığında
    l.save(); l.fillStyle = '#000'; l.fillRect(-300, my + 30, 2600, 500); l.restore();
    const e1 = R(st, 'D09@reform', .7) * (1 - R(st, 'D09@dünyaya', .7)), e2 = R(st, 'D09@bakın', .6);
    kisi3(B, 300, my + 480, 1150, { tip: 'mudur', f: 1, bacak: 'otur', sandalye: true, gozluk: false, kolA: [.35, 1.18],
      kolO: [.45 + .3 * e1 + .4 * e2, 1.1 + .2 * e1 - .2 * e2], bas: .06 - .08 * e2, govde: .05 * e1 + .08 * e2 });
  }, { ...KK, over: OV(ZM(QT('“Umarız bu çalışmadan çok ciddi reform önerileri çıkar.”', 'Bant A, 12:22', { y: 200, x: 1220, maxW: 900 }), 'D09@umarız', 5.2),
    ZM(QT('“Bakın, böyle davranan gardiyanlarınız olunca ne oluyor.”', 'Bant A, 23:45', { y: 200, x: 1220, maxW: 900 }), 'D09@dünyaya', 7)) });

  // P52 ayrıntı: teyp kadrajın ortasında (makaralar, VU, kayıt lambası); "olmalı"da ibre sıçrar, kehribar ışık parlar
  sahne('P52', 'D10', 'teyp', 'ayrinti', (B, st) => {
    B.cam(960, 545, 1.5 + st.lt * .03);
    const k = B.k; k.save(); k.fillStyle = B.ton(.85); k.fillRect(-300, -300, 2600, 1700); k.restore();
    const sic = R(st, 'D10@olmalı', .12, E.out3) * (1 - ramp(st.t, A('D10@olmalı') + .5, A('D10@olmalı') + 1.6));
    SET.teyp(B, 960, 300, 1.25, st.t, { hz: .45, kayit: 1, vuIsik: .55 + .35 * sic, vu: .35 + .25 * Math.abs(Math.sin(st.t * 5.3) * Math.sin(st.t * 2.1)) * (1 - sic) + .62 * sic, ...DOLU });
  }, { ...KAG, over: OV((ctx, st) => { const t0 = A('D10@öyle'); if (st.t > t0 + 8) return; buyukSoz(ctx, 'ÖYLE DAVRANAN', st.t, t0, { px: 140, y: 150 }); buyukSoz(ctx, 'GARDİYANLARIMIZ OLMALI', st.t, t0 + .5, { px: 140, y: 290 }); },
    ZM(KU('Bant A, 23:58'), 'D10@öyle', 6)) });

  // P53 geniş, KAPI ARALIĞINDAN: oda geride ve küçük, önde koyu kapı pervazı (gözlemcileri gözleyen bakış); müdür sol, Mark sağ (önceki planlarla aynı taraf).
  //   "değilim"de Mark geriye yaslanır (önkolları masa kenarında kalır), "mahkûm"da müdür başını ona çevirip öne eğilir; kamera kapıdan içeri yavaşça ilerler
  sahne('P53', 'D11', 'gozlem', 'genis', (B, st) => {
    const z = .74 + st.lt * .016;
    B.cam(960, 470, z);
    const y = R(st, 'D11@değilim', 1, E.io2), e = R(st, 'D11@mahkum', .8, E.io2);
    oda(B, st, { markO: { govde: -.16 * y, bas: .08 - .1 * y, kolO: [lerp(.45, .75, y), lerp(1.1, 1.35, y)], kolA: [lerp(.35, .6, y), lerp(1.18, 1.3, y)] },
      mudurO: { govde: .1 * e, bas: .08 + .04 * e }, monitor: (B2) => bodrum(B2, st, { sayim: 3 }) });
    // kapı pervazı: iki yan ve üst kasa koyu (ekrana göre sabit genişlik), içte ince açık kenar
    const k = B.k, l = B.l, sx = v => 960 + (v - 960) / z, sy = v => 470 + (v - 540) / z;
    const xL = sx(250), xR = sx(1670), yT = sy(95);
    for (const g of [l, k, B.c]) { g.save(); g.fillStyle = '#000'; g.fillRect(xL - 2000, -2000, 2000, 6000); g.fillRect(xR, -2000, 2000, 6000); g.fillRect(xL - 10, yT - 2000, xR - xL + 20, 2000); g.restore(); }
    k.save(); k.fillStyle = B.ton(.55); k.fillRect(xL, yT, 8 / z, 3000); k.fillRect(xR - 8 / z, yT, 8 / z, 3000); k.restore();
  }, { ...KK, over: ZM(QT('Mark: “Bu deney için iyi bir gardiyan değilim. Mahkûm olsam, gerçekten iyi bir mahkûm olurdum.”', 'Bant A, 15:28', { y: 190, maxW: 1300 }), 'D11@mark', 8) });

  // P54 ayrıntı: ışıkta masada dönen bozuk para (kenar tırtıllı, kalın, yüzünde 1971; halka yok); "rastgele"de devrilip yalpalayarak yatar (yazı tura)
  sahne('P54', 'D11@müdürün', 'gozlem', 'ayrinti', (B, st) => {
    B.cam(960, 640, 1.1 + st.lt * .025);
    const k = B.k, l = B.l, my = 560;
    k.save(); k.fillStyle = B.ton(.85); k.fillRect(-300, -300, 2600, my + 300); const g = k.createRadialGradient(960, 780, 60, 960, 780, 900); g.addColorStop(0, B.ton(.02)); g.addColorStop(1, B.ton(.5)); k.fillStyle = g; k.fillRect(-300, my, 2600, 1200); k.restore();
    l.save(); l.fillStyle = '#000'; l.fillRect(-300, my - 4, 2600, 6); l.restore();
    const ts = A('D11@rastgele') - st.at, r = 150, y0 = 790, th = 26;
    const yuz = (cx, cy, rx, ry, ton, yazi, rot = 0) => {   // para yüzü: metal ton + çapraz parıltı + "1971"
      k.save(); k.beginPath(); k.ellipse(cx, cy, Math.max(1, rx), ry, rot, 0, TAU); k.fillStyle = B.ton(ton); k.fill(); k.clip();
      const pa = (st.t * .9) % 2 - .5; k.fillStyle = B.ton(.03, .8); k.beginPath(); k.moveTo(cx - r + pa * 2 * r, cy - r); k.lineTo(cx - r * .6 + pa * 2 * r, cy - r); k.lineTo(cx - r * 1.1 + pa * 2 * r, cy + r); k.lineTo(cx - r * 1.5 + pa * 2 * r, cy + r); k.closePath(); k.fill(); k.restore();
      if (yazi && rx > 12) { l.save(); l.translate(cx, cy); l.rotate(rot); l.scale(rx / r, ry / r); l.fillStyle = '#000'; l.font = '700 64px "Courier Prime"'; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillText('1971', 0, 40); l.font = '700 34px "Courier Prime"'; l.fillText('LIBERTY', 0, -48); l.restore(); }
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.ellipse(cx, cy, Math.max(1, rx), ry, rot, 0, TAU); l.stroke(); l.restore();
    };
    const kenar = (x0, x1, yUst, h) => {   // dik duran paranın görünen kenarı: kalın şerit + tırtıl
      k.save(); k.fillStyle = B.ton(.55); k.fillRect(Math.min(x0, x1), yUst, Math.abs(x1 - x0), h); k.restore();
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 2.5; l.strokeRect(Math.min(x0, x1), yUst, Math.abs(x1 - x0), h); l.lineWidth = 1.6;
      for (let yy = yUst + 8; yy < yUst + h - 4; yy += 11) { l.beginPath(); l.moveTo(Math.min(x0, x1) + 3, yy); l.lineTo(Math.max(x0, x1) - 3, yy); l.stroke(); } l.restore();
    };
    if (st.lt < ts) {   // dik dönüş (yavaşlar): yüz daralır, kenar görünür
      const u = st.lt / Math.max(.5, ts), ang = 26 * st.lt * (1 - .45 * u), c = Math.cos(ang), sn = Math.abs(Math.sin(ang)), cy = y0 - r + 4;
      k.save(); k.fillStyle = B.ton(.45, .6); k.beginPath(); k.ellipse(960, y0 + 12, r * .9, 18, 0, 0, TAU); k.fill(); k.restore();
      const ex = 960 + Math.sign(c || 1) * (Math.abs(c) * r), w = th * sn;
      kenar(960 - w / 2, 960 + w / 2, cy - r * .97, r * 1.94);
      yuz(960 + (c > 0 ? -w / 2 : w / 2) * 0, cy, Math.abs(c) * r, r, c > 0 ? .28 : .42, c > 0);
    } else {             // devrilir, yalpalar, yatar: üst yüz + altta kalınlık (tırtıllı kenar)
      const q = st.lt - ts, sn = Math.exp(-q * 2.2), w = Math.sin(q * 18) * sn, eg = clamp(q / .35);
      const ry = lerp(r, r * .3, E.out3(eg)) + Math.abs(w) * r * .25, cy = lerp(y0 - r + 4, y0 - th * .6, E.out3(eg));
      k.save(); k.fillStyle = B.ton(.45, .6); k.beginPath(); k.ellipse(970, cy + ry * .5 + th + 8, r * 1.05, ry * .55 + 6, 0, 0, TAU); k.fill(); k.restore();
      k.save(); k.fillStyle = B.ton(.55); k.beginPath(); k.ellipse(960, cy + th, r, ry, w * .2, 0, PI); k.lineTo(960 - r * Math.cos(w * .2), cy - r * Math.sin(w * .2)); k.ellipse(960, cy, r, ry, w * .2, PI, 0, true); k.closePath(); k.fill(); k.restore();
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 2.5; l.beginPath(); l.ellipse(960, cy + th, r, ry, w * .2, 0, PI); l.stroke(); l.lineWidth = 1.6;
      for (let i = 1; i < 28; i++) { const a = i / 28 * PI, x = 960 + r * Math.cos(a), y = cy + ry * Math.sin(a); l.beginPath(); l.moveTo(x, y + 2); l.lineTo(x, y + th - 2); l.stroke(); } l.restore();
      yuz(960, cy, r, ry, .3, true, w * .2);
    }
  }, { ...KAG, over: ZM(QT('Müdür: “Evet, ama bu rastgele seçimin bir parçası.\nVe önemli.”', 'Bant A, 15:37', { y: 200, maxW: 1500 }), 'D11@müdürün', 7) });

  // P55 orta: müdür monitörün önünde (opak siluet); monitörde koridorda tek gardiyan; "polise"de gardiyan döner, "kafasındaki"nde eli beline iner; "küçültücü"de müdür eğilir
  sahne('P55', 'D12', 'gozlem', 'orta', (B, st) => {
    B.cam(430, 390, 1.78 + st.lt * .012);
    const don = R(st, 'D12@polise', .5), el = R(st, 'D12@kafasındaki', .7), eg = R(st, 'D12@küçültücü', 1);
    oda(B, st, { mark: false, mudurO: { govde: .1 + .12 * eg, bas: .1 + .05 * eg },
      monitor: (B2) => bodrum(B2, st, { gardiyanlar: [{ z: .3, u: .05, f: don > .5 ? -1 : 1, kol: [lerp(.15, -.06, el), lerp(.5, .2, el)], bas: .05 }] }) });
  }, KK);

  // P56 yakın: Mark bu kez sağa bakar (P44'ün ters açısı), teyp sağ altta; "başka başka"da başını iki yana sallar, "müdür"de başı öne, "kalıp"ta geriye yaslanır
  sahne('P56', 'D13', 'gozlem', 'yakin', (B, st) => {
    B.cam(1000, 520, 1.06 + st.lt * .015);
    const s0 = A('D13@başka'), sal = st.t > s0 && st.t < s0 + 1.6 ? Math.sin((st.t - s0) * 8) * .13 * (1 - (st.t - s0) / 1.6) : 0, y = R(st, 'D13@kalıp', 1.2, E.io2);
    markYakin(B, st, { f: 1, x: 520, y: 340, boy: 2400, bas: .04 + sal + .14 * R(st, 'D13@müdür', .8) - .1 * y, govde: -.08 * y, teyp: [1600, 700, 1.1], isikX: 1120 });
  }, { ...KK, over: ZM(QT('Mark: “Ben çok polis gördüm; hepsi başka başka davranıyor.”\nMüdür: “Biz kalıp bir gardiyan kurmaya çalışıyoruz.”', 'Bant A, 25:59–26:12', { y: 220, x: 1340, px: 60, maxW: 860 }), 'D13@markın', 8) });

  // P57 ayrıntı: döküm D14; "markın"da Mark'ın satırı boş, imleç bekler, kamera teybe kayar; "döneceğiz"de makaralar durur, kayıt lambası yanık kalır
  sahne('P57', 'D14', 'dokum', 'ayrinti', (B, st) => {
    const ts = A('D14@döneceğiz');
    dokum(B, st, ['MÜDÜR: Şimdiye kadar tarzın biraz fazla', '       yumuşaktı. Biraz daha işin içine', '       girmeni istiyoruz.', '', 'MARK:  '], ['D14@şimdiye', 'D14@yumuşaktı', 'D14@girmeni', null, 'D14@markın'], 'D14@markın',
      { ang: aci(st.t, .45, ts), vu: st.t < ts ? undefined : lerp(.35, 0, clamp((st.t - ts) / .6)), imlec: st.t > A('D14@markın') - .2 ? [4, 7] : null, kam: [1600, 262, 2.6, R(st, 'D14@markın+0.5', 1.3, E.io3)] });
  }, { ...KAG, over: ZM(KU('Bant A, 26:24'), 'D14@şimdiye', 6.5) });

  // P58 kart (rev3): müdürün deney sonrası öz değerlendirmesi, daktilo. Kâğıt merdaneden çıkar, harf çubuğu vurur; "zimbardo"da vurgu şeridi
  sahne('P58', 'D15@markla', 'rapor', 'kart', (B, st) => {
    const SAT = ["Pazartesi (isyan günü) John Mark'la", 'konuşup onu işin içine sokmam söylendi.', 'O an konuşmak istemedim, ama', 'Dr. Zimbardo istediği için yine de konuştum.'];
    const Z = ['D15@markla', 'D15@o', 'D15@konuşmak', 'D15@zimbardo'];
    const { p, c } = ilerle(st, SAT, Z, 'D15@konuşmuş+0.3');
    const ry = 700, px = 42, lh = px * 1.5, besle = lerp(-3.4, 0, ramp(st.t, A('D15@markla') - 1.3, A('D15@markla') - .1, E.io2));
    const pTop = ry - px * 3.6 - (c + besle) * lh - 22;
    const yaz = st.t > A('D15@markla') - .1 && st.t < A('D15@konuşmuş') + .5;
    const vur = yaz ? Math.pow(Math.abs(Math.sin(st.t * PI * 6.5)), 6) : 0;
    const ci = Math.floor(clamp(c, 0, SAT.length - 1)), hx = 310 + px * 1.4 + (SAT[ci] || '').length * clamp(c - ci) * px * .6;
    const u = R(st, 'D15@zimbardo', 1.5, E.io3);
    B.cam(960, lerp(830, pTop + 300, u), lerp(1.2 + st.lt * .012, 1.0, u));
    SET.belge(B, 'MÜDÜRÜN DENEY SONRASI NOTU', SAT, p, { px, w: 1300, x: 310, y: pTop, h: SAT.length * lh + px * 4.6 + 60, zemin: .5, vurgu: [3].filter(i => i <= c + .3), vurguA: R(st, 'D15@zimbardo', 1.8, E.lin) });
    daktilo(B, 960, ry, vur, hx);
  }, { ...KAG, over: ZM(KU('Jaffe, deney sonrası öz değerlendirme · Stanford arşivi SC0750 (çevirisi bizim)'), 'D15@markla', 6) });

  // P58c orta (rev3): gözlem odası, müdür yalnız; monitörde sayım. "Sert gardiyana kendisi de inanıyordu": müdür monitöre eğilir;
  //   "kurallar"da monitörde kurallar listesi yanıp söner (kayıt lambası), "yaz"da koni ısınır (kehribar); ekran yazısı yok
  sahne('P58c', 'D15@sert', 'gozlem', 'orta', (B, st) => {
    B.cam(1000, 470, SET.yak(st, 1.1, .014));
    const e = R(st, 'D15@sert', 2.5, E.io2), y = R(st, 'D15@kampına', 2, E.io2);
    SET.gozlemOdasi(B, st, { mark: false, isik: .75 + .25 * y, kayit: R(st, 'D15@kurallar', .4), vu: .25 + .2 * Math.abs(Math.sin(st.t * 3.1)), mudurO: { bas: .08 + .1 * e, kolO: [.95, .75 + .1 * e] } });
  }, KK);

  // P59 geniş (video): Mayıs 1971 yurt koridoru; gündelik giysili öğrenciler, figürler ayrık (üst üste binen kol yok).
  //   Gardiyan rolündeki öğrenci sopa değil not defteri tutar; "arkadaşlarıyla"da uzakta bir öğrenci koridoru geçer; "canlandırması"nda not defteri kalkar
  sahne('P59', 'D16', 'yurt', 'genis', (B, st) => {
    B.cam(960 + st.lt * 6, 520, 1.02 + st.lt * .012);
    const K = yurt(B, st);
    const kisi = (z, u, tip, oo = {}) => { const p = K.yer(z, u), s = K.olc(z); return FIG.kisi(B.l, p[0], p[1], 700 * s, { tip, ...oo }); };
    const g0 = A('D16@arkadaşlarıyla') - st.at;
    kisi(.62, -.4, 'takim', { f: 1, kolO: [.22, .35], kolA: [-.2, .25], serbest: 1, bas: .02 });
    if (st.lt > g0) { const p = K.yer(.76, .35); SET.yuru(B.l, p[0], p[1], 700 * K.olc(.76), st.lt - g0, { tip: 'gazeteci', f: -1, kolO: [.15, .3], kolA: [.1, .3] }); }
    kisi(.4, -.62, 'gazeteci', { f: 1, kolO: [.25, .4], kolA: [-.2, .25], serbest: 1, bas: .04 });
    const def = R(st, 'D16@canlandırması', .8, E.io2);
    kisi(.22, .42, 'arastirmaci', { f: -1, bas: .12 - .08 * def, kolO: [.7 + .2 * def, 1.5 + .15 * def], kolA: [-.2, .25], serbest: 1,
      el: { on: (g, e) => { g.save(); g.fillStyle = '#B4B4AE'; g.translate(e.e[0], e.e[1]); g.rotate(-e.a + .3); g.fillRect(-1, -10, 8, 11); g.restore(); } } });
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
  }, { ...KAG, over: ZM(KU("Le Texier'nin sayımı (2019, s. 3–4)", { x: 1800, align: 'right' }), 'D16@lö', 6) });

  // P61 kart: 2018 ekranı (karanlıkta düz ekran, sayfa çubukları kayar; okunur yazı yok), kamera ekrana girer
  //   → "gardiyandan"da Zimbardo 2018 sayfası, satırlar sözle; "hafif"te vurgu → "kalır"da teyp sağdan girer, "tanımı"nda VU sıçrar
  sahne('P61', 'D17@gardiyanlara', 'z2018', 'kart', (B, st) => {
    const k = B.k, l = B.l, tK = A(ESKI ? 'D17@gardiyandan' : 'D17@gardiyanlara') - .15, tT = ESKI ? A('D17@kalır') - .25 : 1e9;
    if (st.t < tK) {
      const u = E.io2(clamp(st.lt / Math.max(1, tK - st.at)));
      B.cam(960, lerp(500, 450, u), lerp(1.0, 1.75, u));
      tumZemin(B, .88);
      k.save(); k.fillStyle = B.ton(.72); k.fillRect(-900, 820, 3800, 900); k.fillStyle = '#fff'; k.globalAlpha = .5; k.beginPath(); k.ellipse(960, 830, 520, 40, 0, 0, TAU); k.fill(); k.restore();
      const x = 470, y = 170, w = 980, h = 552;
      k.save(); k.fillStyle = B.ton(.95); k.beginPath(); k.roundRect(x - 18, y - 18, w + 36, h + 36, 10); k.fill(); k.fillStyle = B.ton(.9); k.beginPath(); k.moveTo(920, y + h + 18); k.lineTo(1000, y + h + 18); k.lineTo(1030, 812); k.lineTo(890, 812); k.closePath(); k.fill();
      k.beginPath(); k.ellipse(960, 818, 170, 16, 0, 0, TAU); k.fill(); k.restore();
      k.save(); k.beginPath(); k.rect(x, y, w, h); k.clip(); k.fillStyle = B.ton(.03); k.fillRect(x, y, w, h);
      k.fillStyle = B.ton(.5); k.fillRect(x, y, w, 54); k.fillStyle = B.ton(.25); k.fillRect(x + 30, y + 16, 260, 22);
      const r = rng(77), kay = st.lt * 22;
      for (let i = 0; i < 40; i++) { const yy = y + 100 + i * 34 - kay; if (i % 7 === 6) continue; if (yy < y + 60 || yy > y + h) continue; k.fillStyle = B.ton(i % 7 === 0 ? .5 : .32); k.fillRect(x + 90, yy, (i % 7 === 0 ? 380 : 560 + r() * 240), i % 7 === 0 ? 20 : 12); }
      k.restore();
      l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.roundRect(x - 18, y - 18, w + 36, h + 36, 10); l.stroke();
      const mx = x + 640 + Math.sin(st.lt * .9) * 40, myy = y + 330 + st.lt * 4; l.fillStyle = '#000'; l.beginPath(); l.moveTo(mx, myy); l.lineTo(mx, myy + 34); l.lineTo(mx + 9, myy + 26); l.lineTo(mx + 17, myy + 40); l.lineTo(mx + 22, myy + 37); l.lineTo(mx + 15, myy + 24); l.lineTo(mx + 26, myy + 23); l.closePath(); l.fill(); l.restore();   // fare imleci
      return;
    }
    const SAT = ESKI ? ['Gardiyan rolündeki birinden "kararlı"', 've "işin içinde" olmasını istemek,', 'gerçek cezaevlerinde müdürlerin', 'yaptığı baskının yanında hafif kalır.']
      : ['Gardiyanlara hiçbir zaman', 'vahşet emredilmedi.'];   // rev2 D17: "gardiyanlara hiçbir zaman vahşet emredilmedi"
    const { p } = ESKI ? ilerle(st, SAT, ['D17@gardiyandan', 'D17@işin', 'D17@gerçek', 'D17@yaptığı'], 'D17@kalır') : ilerle(st, SAT, ['D17@gardiyanlara', 'D17@vahşet'], 'D17@ve');
    B.cam(960, 470, 1.04 + (st.t - tK) * .008);
    SET.belge(B, 'ZIMBARDO · PRISONEXP.ORG · HAZİRAN 2018', SAT, p, { px: 42, w: 1240, x: 340, y: 150, vurgu: [ESKI ? 3 : 1], vurguA: R(st, ESKI ? 'D17@hafif' : 'D17@vahşet', 1, E.lin), zemin: .38 });
    if (st.t > tT) {   // teyp sağdan girer, kâğıdı örter ("bantta müdürün kendi tanımı da buydu")
      const ks = E.io3(clamp((st.t - tT) / .8)), x0 = lerp(2100, -300, ks);
      B.renkOrt(g => g.rect(x0, -400, 3000, 2000));
      k.save(); k.fillStyle = B.ton(.86); k.fillRect(x0, -400, 3000, 2000); k.restore();
      l.save(); l.fillStyle = '#fff'; l.fillRect(x0, -400, 3000, 2000); l.fillStyle = '#000'; l.fillRect(x0, -400, 8, 2000); l.restore();
      const sic = R(st, 'D17@tanımı', .15, E.out3) * (1 - ramp(st.t, A('D17@tanımı') + .6, A('D17@tanımı') + 1.6));
      SET.teyp(B, x0 + 1260, 210, 1.05, st.t, { hz: .45, kayit: 1, vuIsik: .55 + .35 * sic, vu: .3 + .2 * Math.abs(Math.sin(st.t * 5)) * (1 - sic) + .62 * sic, ...DOLU });
    }
  }, { ...KAG, over: ZM(KU('Zimbardo 2018, prisonexp.org (çevirisi bizim)'), ESKI ? 'D17@gardiyandan' : 'D17@gardiyanlara', 7.5) });

  // P62 orta: Zimbardo 2018 sayfası tek başına ("ayrıntılı"da vurgu) → "lö"de arşiv kutusu geri döner, "arşivdeki"nde bir makara kutusu kalkar
  //   → "belgeler"de iki belge yan yana, eşit büyüklük; sağdaki Le Texier 2019, "doğrudan"da vurgu
  if (ESKI) sahne('P62', 'D18', 'karsi', 'orta', (B, st) => {   // rev2'de D18 yok: plan kaydedilmez (başkanın plan listesine not)
    const k = B.k, l = B.l, tL = A('D18@lö') - .1, tB = A('D18@belgeler') - .1;
    if (st.t >= tL && st.t < tB) { B.cam(lerp(930, 900, (st.t - tL) / 2.4), 470, 1.3 + (st.t - tL) * .05); kutu(B, 1, R(st, 'D18@arşivdeki', .7, E.out3)); return; }
    const sayfa = (x, y, w, bas, sat, p, vurgu, va, px = 38) => {
      const h = 160 + sat.length * px * 1.68 + 70;
      k.save(); k.fillStyle = B.ton(.6); k.fillRect(x + 12, y + 14, w, h); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
      l.save(); l.fillStyle = '#fff'; l.fillRect(x, y, w, h); l.strokeStyle = '#000'; l.lineWidth = 1.6; l.strokeRect(x, y, w, h); l.fillStyle = '#000'; l.font = '700 28px "Courier Prime"'; l.textBaseline = 'middle'; l.fillText(bas, x + 50, y + 56);
      l.lineWidth = 1.4; l.beginPath(); l.moveTo(x + 50, y + 88); l.lineTo(x + w - 50, y + 88); l.stroke();
      l.font = `700 ${px}px "Courier Prime"`; const top = sat.reduce((a, s) => a + s.length, 0); let kalan = Math.floor(top * p);
      sat.forEach((s, i) => { const yy = y + 160 + i * px * 1.68; if (vurgu.includes(i) && va > 0) B.renkBoya(g => g.rect(x + 36, yy - px * .63, (w - 72) * va, px * 1.26), .6, 0); l.fillText(s.slice(0, Math.max(0, kalan)), x + 50, yy); kalan -= s.length; });
      l.restore();
    };
    const SOL = ['Etkili bir gardiyan olmak', 'için resmî ya da ayrıntılı', 'hiçbir talimat vermedik.'];
    tumZemin(B, .36);
    if (st.t < tL) {
      B.cam(960, 470, 1.02 + st.lt * .01);
      sayfa(460, 170, 1000, 'ZIMBARDO · 2018', SOL, clamp((st.t - A('D18@gardiyanlara') + .2) / Math.max(1, A('D18@yazdı') - A('D18@gardiyanlara'))), [1, 2], R(st, 'D18@ayrıntılı', .6), 46);
      return;
    }
    B.cam(960, 470, 1 + (st.t - tB) * .012);
    const sag = E.out3(clamp((st.t - tB) / .6));
    sayfa(160, 200, 760, 'ZIMBARDO · 2018', SOL, 1, [1, 2], 1);
    sayfa(lerp(1500, 1000, sag), 200, 760, 'LE TEXIER · 2019, s. 7', ['Yukarıda sunulan kanıtlar', 'bu ifadeyle doğrudan', 'çelişiyor.'], clamp((st.t - tB - .2) / 1.4), [1, 2], R(st, 'D18@doğrudan', .6));
  }, { ...KAG, over: OV(ZM(KU('Zimbardo 2018, prisonexp.org (çevirisi bizim)'), null, 6.5), ZM(KU('Le Texier 2019, s. 7 (çevirisi bizim)'), 'D18@belgeler', 3.4)) });

  // P63 geniş: ARKADAN: ikisi yan yana monitöre bakar (birlikte izleme); monitörde sakin sayım (ilk vardiyalar), masa lambası teypte.
  //   Monitörden geri çekilme; "rağmen"de müdür geriye yaslanır, "baskın"da Mark başını eğer
  const D19 = ESKI ? 'D19' : 'D17';
  sahne('P63', ESKI ? 'D19' : 'D17@müdürün', 'gozlem', 'genis', (B, st) => {
    const u = E.io2(clamp(st.lt / 9));
    B.cam(960, lerp(390, 520, u), lerp(1.6, 1.0, u));
    const k = B.k, l = B.l, my = 700;
    SET.karanlik(B, .82);
    k.save(); k.fillStyle = B.ton(.86); for (let i = 0; i < 6; i++) k.fillRect(-200 + i * 420, -600, 10, my + 600); k.restore();
    SET.monitorIci(B, 600, 110, 720, 470, B2 => bodrum(B2, st, { sayim: 6, gardiyanlar: [{ z: .3, u: .1, kol: [.1, .4] }], kose: { z: .55, u: .8 } }));
    k.save(); k.fillStyle = B.ton(.62); k.beginPath(); k.moveTo(200, my); k.lineTo(1720, my); k.lineTo(2200, 1100); k.lineTo(-280, 1100); k.closePath(); k.fill(); k.restore();   // masa üstü (arkadan, hafif yüksekten)
    l.save(); l.strokeStyle = '#000'; l.lineWidth = 3; l.beginPath(); l.moveTo(200, my); l.lineTo(1720, my); l.stroke(); l.restore();
    const L = lamba(B, 900, 860, 1, -1, [1100, 790], 905, .72);   // lamba iki başın arasında, başlık teybe
    L.ciz();
    SET.teyp(B, 1110, 770, .4, st.t, { hz: .45, kayit: 1, vuIsik: .7, ...DOLU });
    const y = R(st, D19 + '@rağmen', 1.2, E.io2), d = R(st, D19 + '@baskın', .8, E.io2);
    sirt(B, 520, 820 - 40 * y, 92, { dy: .05, yaslan: -.3 * y });
    sirt(B, 1300, 815, 96, { dy: .05 + .4 * d, dx: -.05 });
  }, { ...KK, over: ZM(KU('Zimbardo 2018, prisonexp.org'), ESKI ? 'D19@zimbardoya' : null, 7) });

  // ── rev3: F03b "O pekiden sonra ne yaptı?" (müdürün deney sonrası notu, SC0750_s5_b09_f40) ──
  // P88b geniş (video): isyan günü bodrum; sayım sürerken kahraman kenarda oturur. "kenarda"da kamera ona yaklaşır, "şunu"da tarama bandı geçer
  sahne('P88b', 'F03b', 'koridor', 'genis', (B, st) => {
    const u = R(st, 'F03b@kenarda', 2.4, E.io2);
    B.cam(lerp(960, 1200, u), lerp(540, 600, u), 1 + .3 * u + st.lt * .006);
    bodrum(B, st, { sayim: 5, sayan: { z: .3, x0: 560, v: 30 }, kose: { z: .5, u: .86 } });
  }, { baski: st => { const q = clamp((st.t - A('F03b@şunu')) / 1.2); return { mod: 'video', bant: [lerp(-.05, 1.05, q), q > 0 && q < 1 ? 1.2 * Math.sin(q * PI) : 0] }; } });

  // P88c kart: müdürün notu, daktilo (≤ 8 sn); "hatırlamıyorum"da vurgu şeridi
  sahne('P88c', 'F03b@bu', 'rapor', 'kart', (B, st) => {
    const SAT = ['Bu konuşmadan sonra bile onun', 'bir sayım yönettiğini ya da emir', 'yağdırdığını hatırlamıyorum.'];
    const Z = ['F03b@bu', 'F03b@sayım', 'F03b@yağdırdığını'];
    const { p, c } = ilerle(st, SAT, Z, 'F03b@hatırlamıyorum+0.4');
    const ry = 700, px = 44, lh = px * 1.5, besle = lerp(-3.4, 0, ramp(st.t, A('F03b@bu') - 1.1, A('F03b@bu') - .1, E.io2));
    const pTop = ry - px * 3.6 - (c + besle) * lh - 22;
    const yaz = st.t > A('F03b@bu') - .1 && st.t < A('F03b@hatırlamıyorum') + .5, vur = yaz ? Math.pow(Math.abs(Math.sin(st.t * PI * 6.5)), 6) : 0;
    const ci = Math.floor(clamp(c, 0, SAT.length - 1)), hx = 330 + px * 1.4 + (SAT[ci] || '').length * clamp(c - ci) * px * .6;
    B.cam(960, lerp(760, pTop + 280, R(st, 'F03b@sayım', 1.5, E.io3)), 1.15 + st.lt * .015);
    SET.belge(B, 'MÜDÜRÜN DENEY SONRASI NOTU', SAT, p, { px, w: 1260, x: 330, y: pTop, h: SAT.length * lh + px * 4.6 + 60, zemin: .5, vurgu: [2].filter(i => i <= c + .3), vurguA: R(st, 'F03b@hatırlamıyorum', 1.2, E.lin) });
    daktilo(B, 960, ry, vur, hx);
  }, { ...KAG, over: ZM(KU('Jaffe, deney sonrası not · Stanford arşivi SC0750 (çevirisi bizim)', { y: 160 }), 'F03b@bu', 6) });

  // P88d ayrıntı: Mark'ın şartlı tahliye görüşü (18.8.1971), daktilo dökümünden tek satır; "sertti"de kehribar şerit, "durdurmaya"da kamera kâğıttan geri çekilir
  sahne('P88d', 'F03b@yazdığı#1', 'dokum', 'ayrinti', (B, st) => {
    const sat = ['8/18  ŞARTLI TAHLİYE GÖRÜŞÜ', '', '"3401\'in şartlı tahliyeyi hak etmesi', 'için hiçbir sebep görmüyorum."'];
    const px = 44, x = 260, y = 200, lh = px * 1.5;
    const p = clamp((st.t - A('F03b@yazdığı#1') + .2) / 2.4), geri = R(st, 'F03b@durdurmaya', 2, E.io2);
    B.cam(960, lerp(420, 470, geri), lerp(1.3, 1.08, geri) + st.lt * .01);
    SET.belge(B, 'STANFORD ARŞİVİ · GARDİYAN RAPORLARI DÖKÜMÜ · MARK', sat, p, { px, w: 1400, x, y, zemin: .72 });
    const va = R(st, 'F03b@sertti', 1, E.lin);
    if (va > 0) B.renkBoya(g => g.rect(x + px * 1.4 - 6, y + px * 3.6 + 2 * lh - px * .6, 1180 * va, px * 1.2), .6, 0);
  }, { ...KAG, over: ZM(KU('Questions on guard shift report (1971), s. 4; adı NBC günlüğü veriyor · çevirisi bizim', { y: 150 }), 'F03b@yazdığı#1', 6) });

  // P88e orta: gözlem odası, müdür yalnız; "hepimiz"de kamera geri çekilir (boş sandalyeler, monitör), koni genişler
  sahne('P88e', 'F03b@müdür#1', 'gozlem', 'orta', (B, st) => {
    const g = R(st, 'F03b@hepimiz', 2.2, E.io2);
    B.cam(lerp(1300, 960, g), lerp(520, 500, g), lerp(1.35, 1.0, g));
    SET.gozlemOdasi(B, st, { mark: false, isik: .7 + .3 * g, vu: .1 });
  }, { ...KK, over: ZM(QT('“Aynı suçlama hepimiz için geçerli.”', null, { x: 960, y: 250, px: 64 }), 'F03b@aynı', 6) });
})();
