// Setler ve sahne yardımcıları (Stanford 1971). ORTAK DOSYA: yalnız başkan değiştirir.
// D (dekor.js), FIG (figur.js), HAREKET (hareket.js) üstüne kurulur; hepsi EKRAN (BASKI) plakalarına çizer.
// Ekran yazısı (üst katman) yardımcıları da burada: Q (alıntı), KU (künye), ET (etiket); video planlarında koyu panel, kâğıtta açık panel.
'use strict';
const SET = (() => {
  const T = (B, d) => B.ton(d);
  const ink = (g, w = 2) => { g.strokeStyle = '#000'; g.fillStyle = '#000'; g.lineWidth = w; g.lineCap = 'round'; g.lineJoin = 'round'; };
  // yürüyen figür: x0'dan yon yönünde, t (sn) anında; boy px. o: FIG.kisi seçenekleri + go(t) (başla/dur), tip ('yuru' | 'kos')
  const GAIT = {};
  function yuru(g, x0, y, boy, t, o = {}) {
    const tip = o.gait || 'yuru', gg = GAIT[tip] || (GAIT[tip] = HAREKET.yuruyus({ tip }));
    const s = boy / 100 * 1.05, yon = o.f || 1;
    const go = o.go || (() => 1);
    // go'nun integrali (basit sayısal; deterministik)
    let m = 0; const n = Math.max(1, Math.ceil(t * 60)); for (let i = 0; i < n; i++) m += Math.max(0, Math.min(1, go(i / 60))) / 60 * (t > 0 ? t * 60 / n : 0);
    const x = x0 + yon * gg.hiz * s * m;
    const poz = gg.poz(m / gg.tur, Math.max(0, Math.min(1, go(t))));
    return FIG.kisi(g, x, y, boy, { ...o, bacak: poz });
  }
  // ── kâğıt dünyası ──
  // gözlem odası duvarı + masa (kâğıt): duvar tonu, masa üstü y
  function oda(B, o = {}) {
    const k = B.k, l = B.l, my = o.masa ?? 760;
    k.save(); k.fillStyle = T(B, o.duvar ?? .2); k.fillRect(-600, -600, W + 1200, my + 600);
    k.fillStyle = T(B, .12); for (let i = 0; i < 6; i++) k.fillRect(-200 + i * 420, -600, 10, my + 600);   // duvar panoları (dikey; yatayla kesişmez)
    k.fillStyle = T(B, o.masaD ?? .45); k.fillRect(-600, my, W + 1200, 900); k.restore();
    l.save(); ink(l, 3); l.beginPath(); l.moveTo(-600, my); l.lineTo(W + 600, my); l.stroke(); l.restore();
    return my;
  }
  // monitörün içine çiz: (x,y,w,h) ekran dikdörtgeni; ciz(B, sx) dünya 1920×1080'i ekrana sığdırılmış olarak çizer
  function monitorIci(B, x, y, w, h, ciz, o = {}) {
    D.monitor(B, x, y, w, h, o);
    for (const g of [B.k, B.l]) { g.save(); g.beginPath(); g.roundRect(x, y, w, h, 16); g.clip(); g.fillStyle = '#fff'; g.fillRect(x, y, w, h); }
    B.c.save(); B.c.beginPath(); B.c.roundRect(x, y, w, h, 16); B.c.clip();
    const sx = w / W, sy = h / H, s = Math.max(sx, sy);
    for (const g of [B.k, B.l, B.c]) { g.translate(x + w / 2, y + h / 2); g.scale(s, s); g.translate(-W / 2, -H / 2); }
    ciz(B, s);
    // maske: çizilen her şeyin üstüne yeniden mavi (renk plakasındaki lamba rengi korunur: yalnız mavi kanalı eklenir)
    B.c.restore(); B.c.save(); B.c.globalCompositeOperation = 'lighter'; B.c.fillStyle = 'rgb(0,0,255)'; B.c.beginPath(); B.c.roundRect(x, y, w, h, 16); B.c.fill(); B.c.restore();
    B.k.restore(); B.l.restore();
  }
  // figürün renk plakası izi: kâğıt sahnede monitörün önünden geçen figür maskeyi siler (yoksa video basılır)
  function onde(B, fn) { fn(B.l); const c = B.c; c.save(); c.globalCompositeOperation = 'source-over'; fn(c, '#000'); c.restore(); }
  // makaralı teyp masada; dönüş hızı hz (tur/sn), oynuyor mu
  function teyp(B, x, y, s, t, o = {}) {
    const hz = o.hz ?? .45, ang = (o.ang != null ? o.ang : t * hz * TAU);
    return D.teyp(B, x, y, s, ang, { kayit: o.kayit ?? 1, vu: o.vu ?? (.35 + .3 * Math.abs(Math.sin(t * 5.3) * Math.sin(t * 2.1))), vuIsik: o.vuIsik, sol: o.sol, sag: o.sag });
  }
  // belge kartı (kâğıt): ortada bir sayfa; ust: başlık satırı (kaynak, tarih); satirlar daktilo; p yazılma ilerlemesi
  function belge(B, ust, satirlar, p, o = {}) {
    const w = o.w || 1300, x = o.x ?? (W - w) / 2, y = o.y ?? 150, px = o.px || 38;
    const k = B.k, l = B.l;
    // masa zemini
    k.save(); k.fillStyle = T(B, o.zemin ?? .35); k.fillRect(-600, -600, W + 1200, H + 1200); k.restore();
    const lh = px * 1.5, h = o.h || (satirlar.length * lh + px * 4.6 + 60);
    k.save(); k.fillStyle = T(B, .55); k.fillRect(x + 14, y + 16, w, h); k.fillStyle = '#fff'; k.fillRect(x, y, w, h); k.restore();
    l.save(); ink(l, 1.6); l.strokeRect(x, y, w, h);
    if (ust) { l.font = `700 ${Math.round(px * .72)}px "Courier Prime"`; l.textBaseline = 'middle'; l.fillText(ust, x + px * 1.4, y + px * 1.5); l.lineWidth = 1.4; l.beginPath(); l.moveTo(x + px * 1.4, y + px * 2.4); l.lineTo(x + w - px * 1.4, y + px * 2.4); l.stroke(); }
    l.font = `${o.kalin === false ? 400 : 700} ${px}px "Courier Prime"`; l.textBaseline = 'middle';
    const top = satirlar.reduce((a, r) => a + r.length, 0); let kalan = Math.floor(top * clamp(p));
    satirlar.forEach((r, i) => {
      const yy = y + px * 3.6 + i * lh;
      if (o.vurgu && o.vurgu.includes(i) && (o.vurguA ?? 1) > 0) B.renkBoya(g => g.rect(x + px * 1.1, yy - px * .6, (w - px * 2.2) * clamp(o.vurguA ?? 1), px * 1.2), .6, 0);
      const s = r.slice(0, Math.max(0, kalan)); kalan -= r.length; l.fillText(s, x + px * 1.4, yy);
    });
    l.restore();
    return { x, y, w, h };
  }
  // yazı tahtası (kâğıt): koyu tahta, tebeşir yazısı (ton plakasında açık), el yazısı ilerlemesi
  function tahta(B, satirlar, p, o = {}) {
    const k = B.k, l = B.l, x = o.x ?? 260, y = o.y ?? 120, w = o.w ?? 1400, h = o.h ?? 620;
    k.save(); k.fillStyle = T(B, .25); k.fillRect(-600, -600, W + 1200, H + 1200); k.fillStyle = T(B, .82); k.fillRect(x, y, w, h); k.restore();
    l.save(); ink(l, 8); l.strokeRect(x - 8, y - 8, w + 16, h + 16); l.restore();
    k.save(); k.fillStyle = T(B, .08); k.font = `600 ${o.px || 64}px "Courier Prime"`; k.textBaseline = 'middle';
    const top = satirlar.reduce((a, r) => a + r.length, 0); let kalan = Math.floor(top * clamp(p));
    satirlar.forEach((r, i) => { const s = r.slice(0, Math.max(0, kalan)); kalan -= r.length; k.fillText(s, x + 70, y + 110 + i * (o.lh || 110)); });
    k.restore();
    return { x, y, w, h };
  }
  // ── video dünyası (bodrum ve dışı) ──
  // 1971 Amerikan polis arabası (yandan siluet; tavanda tek lamba, kapıda "POLICE"): (x, y zemin), s ölçek
  function polisArabasi(B, x, y, s, o = {}) {
    const l = B.l, k = B.k;
    l.save(); l.fillStyle = '#000'; l.beginPath();
    l.moveTo(x - 300 * s, y - 40 * s); l.lineTo(x - 300 * s, y - 110 * s); l.lineTo(x - 150 * s, y - 120 * s); l.lineTo(x - 100 * s, y - 190 * s); l.lineTo(x + 120 * s, y - 190 * s);
    l.lineTo(x + 190 * s, y - 120 * s); l.lineTo(x + 310 * s, y - 110 * s); l.lineTo(x + 310 * s, y - 40 * s); l.closePath(); l.fill();
    l.fillStyle = '#fff'; l.beginPath(); l.moveTo(x - 85 * s, y - 175 * s); l.lineTo(x + 5 * s, y - 175 * s); l.lineTo(x + 5 * s, y - 125 * s); l.lineTo(x - 125 * s, y - 125 * s); l.closePath(); l.fill();
    l.beginPath(); l.moveTo(x + 20 * s, y - 175 * s); l.lineTo(x + 110 * s, y - 175 * s); l.lineTo(x + 160 * s, y - 125 * s); l.lineTo(x + 20 * s, y - 125 * s); l.closePath(); l.fill();
    l.fillStyle = '#000'; l.fillRect(x - 20 * s, y - 214 * s, 50 * s, 24 * s);   // tavan lambası
    l.beginPath(); l.arc(x - 190 * s, y - 40 * s, 52 * s, 0, TAU); l.arc(x + 200 * s, y - 40 * s, 52 * s, 0, TAU); l.fill(); l.restore();
    k.save(); k.fillStyle = T(B, .1); k.fillRect(x - 140 * s, y - 112 * s, 280 * s, 56 * s); k.restore();   // kapıda açık şerit (yazı alanı)
    l.save(); l.font = `700 ${40 * s}px "Courier Prime"`; l.textAlign = 'center'; l.textBaseline = 'middle'; l.fillStyle = '#000'; l.fillText('POLICE', x, y - 84 * s); l.restore();
    if (o.lamba) B.renkBoya(g => g.rect(x - 20 * s, y - 214 * s, 50 * s, 24 * s), o.lamba, 1);   // döner lamba (tek kırmızı)
  }
  // ev cephesi (1971 Kaliforniya, tek katlı): (x, y zemin)
  function ev(B, x, y, s) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .3); k.fillRect(x, y - 300 * s, 760 * s, 300 * s); k.fillStyle = T(B, .6); k.beginPath(); k.moveTo(x - 40 * s, y - 300 * s); k.lineTo(x + 380 * s, y - 420 * s); k.lineTo(x + 800 * s, y - 300 * s); k.closePath(); k.fill();
    k.fillStyle = T(B, .75); k.fillRect(x + 90 * s, y - 220 * s, 180 * s, 120 * s); k.fillRect(x + 500 * s, y - 220 * s, 180 * s, 120 * s); k.fillStyle = T(B, .55); k.fillRect(x + 330 * s, y - 230 * s, 110 * s, 230 * s); k.restore();
    l.save(); ink(l, 3); l.strokeRect(x, y - 300 * s, 760 * s, 300 * s); l.restore();
  }
  // dolap kapısı (koridorda, karanlık hücre): perspektifsiz ön görünüş; titreme sh
  function dolap(B, x, y, w, h, sh = 0, o = {}) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .3); k.fillRect(x - 200, y - 100, w + 400, h + 200); k.fillStyle = T(B, o.acik ? .95 : .7); k.fillRect(x + sh, y, w, h); k.restore();
    l.save(); ink(l, 5); l.strokeRect(x + sh, y, w, h); l.beginPath(); l.arc(x + w - 40 + sh, y + h / 2, 12, 0, TAU); l.fill(); l.restore();
  }
  // duvar saati: akrep/yelkovan (saat h, dakika m); halka tarama yok (tek çevre çizgisi + 12 çentik)
  function saat(B, x, y, r, h, m) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, .02); k.beginPath(); k.arc(x, y, r, 0, TAU); k.fill(); k.restore();
    l.save(); ink(l, r * .06); l.beginPath(); l.arc(x, y, r, 0, TAU); l.stroke();
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; l.lineWidth = r * (i % 3 ? .02 : .045); l.beginPath(); l.moveTo(x + Math.sin(a) * r * .82, y - Math.cos(a) * r * .82); l.lineTo(x + Math.sin(a) * r * .94, y - Math.cos(a) * r * .94); l.stroke(); }
    const ah = (h % 12 + m / 60) / 12 * TAU, am = m / 60 * TAU;
    l.lineWidth = r * .07; l.beginPath(); l.moveTo(x, y); l.lineTo(x + Math.sin(ah) * r * .5, y - Math.cos(ah) * r * .5); l.stroke();
    l.lineWidth = r * .04; l.beginPath(); l.moveTo(x, y); l.lineTo(x + Math.sin(am) * r * .78, y - Math.cos(am) * r * .78); l.stroke();
    l.restore();
  }
  // yatak (yandan): (x, y zemin), w uzunluk, eğim a
  function yatak(B, x, y, w, a = 0) {
    const k = B.k, l = B.l; for (const g of [k, l]) { g.save(); g.translate(x, y); g.rotate(a); }
    k.fillStyle = T(B, .35); k.fillRect(-w / 2, -70, w, 30); ink(l, 4); l.strokeRect(-w / 2, -70, w, 30); l.fillRect(-w / 2, -40, 8, 40); l.fillRect(w / 2 - 8, -40, 8, 40);
    for (const g of [k, l]) g.restore();
  }
  // söndürücü bulutu (video: açık ton, ışıma); kaynak (x,y), yön a, ilerleme p
  function bulut(B, x, y, a, p, t) {
    const k = B.k; k.save();
    for (let i = 0; i < 26; i++) { const u = (i / 26) * p, d = u * 700, r = 20 + u * 160; const jx = Math.sin(i * 7.3 + t * 3) * u * 50, jy = Math.cos(i * 4.1 + t * 2) * u * 40;
      k.fillStyle = T(B, .0); k.globalAlpha = .55 * (1 - u * .6); k.beginPath(); k.arc(x + Math.cos(a) * d + jx, y + Math.sin(a) * d + jy, r, 0, TAU); k.fill(); }
    k.restore();
  }

  // ── karanlık gözlem odası (r8/r1 örneklerinden; uslup_ornekleri_fable.md) ──
  // Kural: oda koyu (≥ %60), ışık konisi TEYBİN üstüne düşer (sorgu mizanseni yok: kimse ışığın altında oturmaz), iki siluet koninin iki yanında eşit yükseklikte.
  // Parıltı insanda değil nesnede (makara, VU, masa kenarı). Kâğıt modunda o.kuru ile kullanılır.
  function karanlik(B, d = .74) { const k = B.k; k.save(); k.setTransform(1, 0, 0, 1, 0, 0); k.fillStyle = T(B, d); k.fillRect(0, 0, k.canvas.width, k.canvas.height); k.restore(); }
  // ışık konisi: tepe (x, y) dar w0, taban y1'de w1; gradyan tepe açık → taban; kenar sert, bir kenarı kuru fırçayla dağılır
  function koni(B, x, y, w0, y1, w1, o = {}) {
    const k = B.k, a = o.a ?? 1, tohum = o.tohum || 3;
    const g = k.createLinearGradient(0, y, 0, y1); g.addColorStop(0, `rgba(255,255,255,${.9 * a})`); g.addColorStop(1, `rgba(255,255,255,${(o.taban ?? .55) * a})`);
    k.save(); k.fillStyle = g; k.beginPath(); k.moveTo(x - w0 / 2, y); k.lineTo(x + w0 / 2, y); k.lineTo(x + w1 / 2, y1); k.lineTo(x - w1 / 2, y1); k.closePath(); k.fill();
    // yumuşak kenar boyunca kuru fırça darbeleri (tohumlu)
    const r = rng(tohum); k.strokeStyle = `rgba(255,255,255,${.35 * a})`;
    for (let i = 0; i < 26; i++) { const u = r(), yy = lerp(y, y1, u), xx = x + lerp(w0, w1, u) / 2 * (r() < .5 ? -1 : 1); k.lineWidth = 1 + r() * 4; k.beginPath(); k.moveTo(xx, yy); k.lineTo(xx + (r() - .5) * 30, yy + 40 + r() * 120); k.stroke(); }
    k.restore();
  }
  // düşey sürtme: koyu kütlenin alt kenarından aşağı ince tohumlu şeritler (açık: beyaz boya)
  function surtme(g, x0, x1, y, tohum = 7, o = {}) {
    const r = rng(tohum), n = o.n || 40; g.save();
    for (let i = 0; i < n; i++) { g.globalAlpha = .4 + r() * .5; g.fillStyle = o.acik ? '#fff' : '#000'; g.fillRect(lerp(x0, x1, r()), y - 10, 1 + r() * 3, (o.boy || 220) * (.2 + r() * .8)); }
    g.restore();
  }
  // gözlem odası: koyu duvar, monitör (içinde bodrum), masa, teyp, konide ışık; iki oturan siluet (sol müdür, sağ Mark) eşit yükseklikte.
  // o: { t, ang (makara açısı), kayit, vu, mudur, mark (true | false), markGozluk (elinde gözlük), monitor (çizim fn), cam: [x,y,z] }
  function gozlemOdasi(B, st, o = {}) {
    const t = st.t, my = 690;
    karanlik(B, o.koyu ?? .76);
    const k = B.k, l = B.l;
    // monitör arka duvarda solda (soğuk ışık kaynağı), içinde bodrum
    if (o.monitor !== false) monitorIci(B, 150, 150, 520, 380, o.monitor || ((B2) => { const KK = D.koridor(B2, t, { levha: false }); }));
    // koni: tavandan teybin üstüne
    koni(B, 1060, -60, 120, my + 10, 760, { a: o.isik ?? 1, tohum: 5 });
    // masa: koyu kütle + sert açık üst kenar (karenin en açık çizgisi), kenar 3-4 parçaya kırık
    k.save(); k.fillStyle = T(B, .9); k.fillRect(260, my + 8, 1500, 400); k.restore();
    l.save(); l.fillStyle = '#000'; l.fillRect(260, my + 30, 1500, 500); l.restore();
    k.save(); k.fillStyle = '#fff'; for (const [a0, a1] of [[560, 830], [850, 1290], [1310, 1480], [1500, 1560]]) k.fillRect(a0, my + 6, a1 - a0, 8); k.restore();
    surtme(B.l, 300, 1700, my + 30, 11, { n: 50, boy: 260, acik: false });
    // teyp masada, ışığın altında
    const tp = teyp(B, 1060, my - 250, .62, t, { ang: o.ang, kayit: o.kayit ?? 1, vu: o.vu, hz: o.hz });
    // siluetler: koninin iki yanında, eşit boyda oturur; ışığa bakan yanda tek orta ton leke (ton plakasında)
    // kollar dirsekten bükük, önkol masada (düz uzanan kol yok); figür renk plakasında siyah: monitör maskesini siler
    const kisiCiz = (x, f, tip, oo) => { const op = { tip, f, bacak: 'otur', sandalye: true, kolO: [.95, .75], kolA: [.7, .95], bas: .08, gozluk: false, ...oo };
      FIG.kisi(B.c, x, my + 330, 760, { ...op, renk: '#000', sandalyeRenk: '#000' }); return FIG.kisi(B.l, x, my + 330, 760, op); };
    if (o.mudur !== false) kisiCiz(560, 1, 'mudur', o.mudurO || {});
    if (o.mark !== false) kisiCiz(1560, -1, 'gardiyan', { gozluk: false, ...(o.markO || {}) });
    return { masaY: my, teyp: tp };
  }
  // kamera sallantısı yok; yavaş yaklaşma varsayılan: zoom(st, a, b)
  const yak = (st, z0 = 1, hiz = .012) => z0 + st.lt * hiz;
  return { yuru, oda, monitorIci, onde, teyp, belge, tahta, polisArabasi, ev, dolap, saat, yatak, bulut, yak, ink, karanlik, koni, surtme, gozlemOdasi };
})();

// ── ekran yazısı yardımcıları (üst katman) ──
const KOYU = '28,30,31', ACIK = '236,226,201';
// video planı için koyu panel + açık yazı; kâğıt planı için açık panel + koyu yazı
function QT(s, kaynak, o = {}) {
  return (ctx, st) => quote(ctx, s, o.x ?? W / 2, o.y ?? 300, st.lt, { px: o.px || 64, maxW: o.maxW || 1300, t0: o.t0 ?? .2, per: o.per ?? .45, kaynak, panel: o.panel ?? .82, col: o.video ? '#E9EEF0' : undefined, panelRGB: o.video ? KOYU : undefined });
}
function KU(s, o = {}) { return (ctx, st) => kunye(ctx, s, st.lt, o.d ?? 99, { y: o.y ?? 846, x: o.x, align: o.align, px: o.px, panel: o.panel, col: o.video ? '#E9EEF0' : undefined, panelRGB: o.video ? KOYU : undefined, t0: o.t0 }); }
function ETK(s, x, y, o = {}) { return (ctx, st) => etiket(ctx, s, x, y, st.lt - (o.t0 || 0), o.d ?? 4, { px: o.px, col: o.video ? '#E9EEF0' : undefined, panelRGB: o.video ? KOYU : undefined }); }
// birden çok üst katman
const OV = (...fs) => (ctx, st) => { for (const f of fs) if (f) f(ctx, st); };
