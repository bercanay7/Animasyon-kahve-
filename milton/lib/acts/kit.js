// kit grubu: planlar burada kaydedilir (bkz. lib/acts/KILAVUZ.md)
// Kitap sayfası / gravür levhası: kâğıt ağırlıklı, nefes alan kareler; ekran tipografisinin evi.
// Yazı yolu (b): yazılar ton katmanına (GR.tx) basılır; levhanın parçasıdırlar (gravür titremesi, kâğıt dokusu ve vinyet
// onları da tutar; geçişte levhayla birlikte söner). Beliriş "mürekkep": harf soldan sağa yazılır (silme) ya da harfin içi
// çapraz tarama ile dolar (geçiş tonları gravür çizgisi olur, gri yok).
'use strict';
const KIT_K = .975;                                     // levha kâğıdı (temiz)
const KIT_TR = { type: 'fade', dur: .8 };
const kit_a = (t, t0, dur = .9) => clamp((t - t0) / dur);   // kelimeye bağlı beliriş 0..1

// ════════ levha ilkelleri ════════
// ince çizgi: ton + tarama yaması çizgi doğrultusunda (kenar yumuşatması kesik çizgiye dönmesin)
function kit_hat(x0, y0, x1, y1, w = 3, v = .02) {
  const { tx, px } = GR, P = new Path2D(), dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1, nx = -dy / L * w / 2, ny = dx / L * w / 2;
  poly(P, [[x0 + nx, y0 + ny], [x1 + nx, y1 + ny], [x1 - nx, y1 - ny], [x0 - nx, y0 - ny]], true);
  tx.fillStyle = GR.tone(v); tx.fill(P); px.fillStyle = GR.hatch({ th: Math.atan2(dy, dx), id: 0 }); px.fill(P);
}
function kit_kutu(x0, y0, x1, y1, w = 3, v = .02) { kit_hat(x0 - w / 2, y0, x1 + w / 2, y0, w, v); kit_hat(x0 - w / 2, y1, x1 + w / 2, y1, w, v); kit_hat(x0, y0, x0, y1, w, v); kit_hat(x1, y0, x1, y1, w, v); }
// çift çizgili baskı çerçevesi (levha izi): dış 5 px, iç 3 px, aralık 12 px
function kit_cerceve(v = .02, m = 44) { kit_kutu(m, m, W - m, H - m, 5, v); kit_kutu(m + 16, m + 16, W - m - 16, H - m - 16, 3, v); }
// yatay süs çizgisi: ortada baklava, iki yana incelen kol; w yarım genişlik
function kit_cizgi(x, y, w, o = {}) {
  const { tx, px } = GR, v = o.v ?? .02, a = clamp(o.a ?? 1); if (a <= 0) return;
  const hw = w * E.out3(a), th = o.th ?? 5, r = o.r ?? 9;
  const P = new Path2D();
  const bar = (x0, x1) => poly(P, [[x0, y - th / 2], [x1, y - th * .2], [x1, y + th * .2], [x0, y + th / 2]], true);
  if (o.lozenge !== false) { poly(P, [[x, y - r], [x + r * 1.5, y], [x, y + r], [x - r * 1.5, y]], true); bar(x - r * 2.3, x - r * 2.3 - hw); bar(x + r * 2.3, x + r * 2.3 + hw); }
  else { bar(x, x - hw); bar(x, x + hw); }
  tx.fillStyle = GR.tone(v); tx.fill(P); px.fillStyle = GR.hatch({ th: 0, id: 0 }); px.fill(P);
}
// ════════ yazı ════════
// kit_yaz(s, x, y, {f: 'b' Cinzel | 'a' italik | 'm' düz, px, w, ls, align, a (0..1), wipe (soldan yazılır), v (harf tonu), bg (zemin), rot})
// y: harflerin görsel ortası
function kit_font(o) { return o.f === 'b' ? FONT.baslik(o.px, o.w ?? 700) : o.f === 'm' ? FONT.metin(o.px, o.w ?? 600) : FONT.alinti(o.px, o.w ?? 600); }
function kit_olc(s, o) { const { tx } = GR; tx.save(); tx.font = kit_font(o); tx.letterSpacing = (o.ls || 0) + 'px'; const w = tx.measureText(s).width - (o.ls || 0); tx.restore(); return w; }
function kit_yaz(s, x, y, o = {}) {
  if (NOTEXT || !s) return;
  const a = clamp(o.a ?? 1); if (a <= 0) return;
  const { tx, px } = GR, v = o.v ?? .02, bg = o.bg ?? KIT_K, al = o.align || 'center';
  const set = c => { c.font = kit_font(o); c.textAlign = al; c.textBaseline = 'alphabetic'; c.letterSpacing = (o.ls || 0) + 'px'; if (o.rot) { c.translate(x, y); c.rotate(o.rot); c.translate(-x, -y); } };
  tx.save(); set(tx);
  const wd = tx.measureText(s).width - (o.ls || 0), xl = al === 'center' ? x - wd / 2 : al === 'right' ? x - wd : x;
  const yb = y + o.px * (o.f === 'b' ? .36 : .27);
  if (o.wipe && a < 1) {
    const F = o.px * 1.6, L = wd + F, q = E.io2(a) * L, g = tx.createLinearGradient(xl - F, 0, xl + wd, 0);
    g.addColorStop(0, GR.tone(v)); g.addColorStop(clamp((q - F) / L), GR.tone(v)); g.addColorStop(clamp(q / L), GR.tone(bg)); g.addColorStop(1, GR.tone(bg));
    tx.fillStyle = g;
  } else tx.fillStyle = GR.tone(lerp(bg, v, E.sine(a)));
  tx.fillText(s, x, yb); tx.restore();
  px.save(); set(px); px.fillStyle = GR.hatch({ th: o.th ?? -.8, id: 0 }); px.fillText(s, x, yb); px.restore();
}
// satırlar: L dizisi, satır aralığı lh; her satır kendi zamanında (ts[i]) belirir
function kit_satirlar(L, x, y, lh, ts, t, o = {}) { const y0 = y - (L.length - 1) * lh / 2; L.forEach((s, i) => kit_yaz(s, x, y0 + i * lh, { ...o, a: kit_a(t, ts[Math.min(i, ts.length - 1)], o.dur ?? 1.1) })); }

// ════════ figür yardımcıları ════════
// koyu (lum 0) ya da açık (lum 1) siluet; a < 1 iken ton katmanında saydam basılır (geçiş tonu tarama olur)
function kit_fig(J, o = {}, a = 1) {
  if (a <= 0) return;
  const { tx, px } = GR; tx.save(); px.save(); tx.globalAlpha = a;
  SF.draw(J, Object.assign({ lum: 0, lit: [.6, -.8], t: 0, lines: 1, eye: 0, wind: .3, halo: 0 }, o));
  tx.restore(); px.restore();
}
// dolu yol (ton + tarama)
function kit_dol(P, v, hs = { th: 0, id: 0 }) { GR.fill(P, GR.tone(v), hs); }
// sahne zemini: hafif taralı yer bandı (figürlerin bastığı yer)
function kit_yer(x0, x1, y, o = {}) {
  kit_hat(x0, y, x1, y, o.w ?? 4);
  if (o.sx != null) { const P = new Path2D(); P.ellipse(o.sx, y + (o.sh ?? 18) * .55, o.sw ?? 160, o.sh ?? 18, 0, 0, TAU); const C = new Path2D(); C.rect(x0, y + 2, x1 - x0, 400); GR.tx.save(); GR.tx.clip(C); GR.px.save(); GR.px.clip(C); GR.fill(P, GR.tone(.3), { th: 0, id: 0 }); GR.tx.restore(); GR.px.restore(); }
}

// ════════ P006 (A05): 1667 başlık sayfası; «kaleminden»de tüy kalem sayfanın alt yarısına açılış figürünü çizer ════════
// Yazılar ilk ~5 sn'de biter (üst yarı); alt yarı (x 700–1220, y 590–880) figür vinyetine ayrılır. Kamera z 1,00 → 1,08 (15 sn).
const KIT_P6K = { x: 960, y: 872, U: 290 };   // figür: ayak hizası ve boy (nif_yol7 ölçüsü)
// kalemin izlediği yol (kapak/figür koordinatında: sol kanat ucu → baş → sağ kanat → etek → geri)
const KIT_P6Y = [[-300, 960], [-292, 460], [-206, 140], [-120, 220], [-40, 300], [0, 330], [40, 300], [120, 220], [206, 140], [292, 460], [300, 960],
  [170, 860], [120, 560], [60, 420], [0, 600], [-60, 420], [-120, 560], [-170, 860], [-120, 980], [0, 985], [120, 980], [0, 760], [-90, 700], [90, 700]];
function kit_kalem(x, y, a = 1) {   // tüy kalem: sivri uç + gövde + tüy silueti (el yok); ucu (x, y)
  if (a <= 0) return; const { tx } = GR, an = -.95;
  tx.save(); tx.translate(x, y); tx.rotate(an); tx.scale(.72, .72);
  const U = new Path2D(); poly(U, [[0, 0], [16, -7], [40, -7], [40, 7], [16, 7]], true); GR.fill(U, GR.tone(.02), { th: 0, id: 0 });
  const T = new Path2D(); spline(T, [[40, 0], [70, -12], [150, -34], [250, -40], [320, -22], [262, -6], [180, 10], [100, 12], [60, 8]], true, .8); GR.fill(T, GR.tone(.03), { th: 0, id: 0 });
  oku_vurus([[44, 0], [140, -10], [250, -22], [312, -20]], 4, .95, .4);
  for (let k = 0; k < 6; k++) { const u = .25 + k * .12; oku_vurus([[lerp(60, 300, u), -lerp(6, 24, u)], [lerp(60, 300, u) + 30, -lerp(6, 24, u) - 22]], 3.4, .95, .3); }
  tx.restore();
}
function kit_baslikSayfasi(st) {
  const t = st.t, s0 = S('A05');
  kit_cerceve();
  const ar = kit_a(t, s0 + .1, 1.2);
  if (ar > 0) { const w = 320 * E.out3(ar); kit_hat(960 - w, 112, 960 + w, 112, 4); kit_hat(960 - w, 126, 960 + w, 126, 3); }
  kit_yaz('PARADISE LOST.', 960, 196, { f: 'b', px: 96, ls: 14, a: kit_a(t, s0 + .2, 1.4), wipe: true });
  kit_yaz('A POEM', 960, 272, { f: 'b', px: 42, w: 600, ls: 18, a: kit_a(t, s0 + .9, .8), wipe: true });
  kit_cizgi(960, 314, 100, { a: kit_a(t, s0 + 1.2, .9) });
  kit_yaz('JOHN MILTON', 960, 364, { f: 'b', px: 58, w: 600, ls: 14, a: kit_a(t, Wd('A05', 'con') - .2, 1), wipe: true });
  const tk = Wd('A05', 'kayıp'), ak = kit_a(t, tk - .5, 1);
  if (ak > 0) { const w = 380 * E.out3(ak); kit_hat(960 - w, 414, 960 + w, 414, 3); kit_hat(960 - w, 425, 960 + w, 425, 3); }
  kit_yaz('KAYIP CENNET · John Milton, 1667', 960, 482, { f: 'b', px: 56, w: 700, ls: 6, a: kit_a(t, tk - .15, 1.1), wipe: true });
  // figür vinyeti: kalem dış hattı yol boyunca çizer (ilerleyen maske), kanat vuruşları gelir, göğüs alevi en son «karakter»de yanar
  const tK = Wd('A05', 'kaleminden') - .15, tC = Wd('A05', 'karakter'), u = oku_u(t, tK, tK + 1.5), F = nif_yol7(KIT_P6K, NIF_EGIM), M = F.M;
  const Y = KIT_P6Y.map(([x, y]) => M(x, y)), at = q => oku_yolNokta(Y, clamp(q));
  if (u > 0) {
    const C = new Path2D(), n = 90, R = 46; for (let i = 0; i <= n * u; i++) { const q = at(i / n); C.moveTo(q[0] + R, q[1]); C.arc(q[0], q[1], R, 0, TAU); }
    if (u >= 1) C.rect(0, 0, W, H);
    // vinyet zemini: ayak altında taralı gölge
    const Sh = new Path2D(); Sh.ellipse(960, 878, 250 * E.out3(u), 13, 0, 0, TAU); GR.fill(Sh, GR.tone(.35), { th: 0, id: 0 });
    GR.save(); for (const c of [GR.tx, GR.px]) c.clip(C);
    nif_siluet7(t, 0, KIT_P6K, { alev: false });
    GR.restore();
  }
  const fa = E.out3(kit_a(t, Math.max(tC, tK + 1.3), 1.1));
  if (fa > 0) nif_alev7(t, F, 0, fa);
  // kalem: yolun ucunda; iş bitince sağ üste çekilir
  if (u > 0) { const q = at(u), go = E.in2(oku_u(t, tK + 1.5, tK + 2.3)); if (go < 1) kit_kalem(q[0] + go * 900, q[1] - go * 700, 1); }
  kit_yaz('bir destanın okuması', 1470, 760, { f: 'a', px: 66, a: kit_a(t, Wd('A05', 'değil') - .1, 1.1), wipe: true });
}
plan('P006', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 560, z: 1 }, { cx: 960, cy: 560, z: 1.08 }, st.p, E.sine), () => kit_baslikSayfasi(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P016 (B09): taslak sayfası, güneş çizimi ════════
// sayfa yerel koordinatı: merkez (0,0)
function kit_sayfaYolu(w, h, seed) {
  const r = rng(seed), P = new Path2D(), pts = [], n = 10;
  for (let i = 0; i <= n; i++) pts.push([-w / 2 + w * i / n, -h / 2 + (r() - .5) * 4]);
  for (let i = 1; i <= n; i++) pts.push([w / 2 + (r() - .5) * 4, -h / 2 + h * i / n]);
  for (let i = n - 1; i >= 0; i--) pts.push([-w / 2 + w * i / n, h / 2 + (r() - .5) * 4]);
  for (let i = n - 1; i >= 1; i--) pts.push([-w / 2 + (r() - .5) * 4, -h / 2 + h * i / n]);
  poly(P, pts, true); return P;
}
// el yazısı (okunmaz): kelime kelime ilmekli bitişik yazı (uzamış sikloit); keskin üst katmana (GR.ox) mürekkeple
function kit_karalama(c, x0, x1, y, seed, o = {}) {
  const r = rng(seed);
  c.save(); c.strokeStyle = GR.inkCol; c.lineWidth = o.w ?? 2.6; c.lineCap = 'round'; c.lineJoin = 'round';
  let x = x0 + (o.indent ?? 0);
  while (x < x1 - 40) {
    const wl = 40 + r() * 100, xe = Math.min(x1, x + wl), R = 5 + r() * 2, K = 2.7 + r() * .6;
    c.beginPath(); let first = true;
    for (let s = 0; ; s += .25) {
      const xx = x + s * K - R * Math.sin(s) * .9; if (xx > xe) break;
      const tall = (Math.floor(s / TAU) * 7 + seed) % 5 === 0 ? 1.9 : 1;
      const yy = y - R * (1 - Math.cos(s)) * (Math.cos(s) < 0 ? tall : 1) * .8;
      if (first) { c.moveTo(xx, yy); first = false; } else c.lineTo(xx, yy);
    }
    c.stroke(); x = xe + 16 + r() * 16;
  }
  if (o.strike) { c.lineWidth = 3.4; c.beginPath(); c.moveTo(x0 - 6, y - 6 + r() * 3); c.quadraticCurveTo((x0 + x1) / 2, y - 11, Math.min(x, x1) + 8, y - 5); c.stroke(); }
  c.restore();
}
function kit_taslak(st) {
  const t = st.t, s0 = S('B09'), { tx, px, ox } = GR;
  kit_cerceve();
  const PX = 700, PY = 478, PW = 620, PH = 770, rot = -.025;
  const pt = kit_a(t, s0 + .15, 1.3), k = Math.cos(E.io2(pt) * PI / 2);       // üstteki boş sayfanın çevrilme oranı
  GR.save(); GR.frame(PX + 16, PY + 14, rot); kit_dol(kit_sayfaYolu(PW, PH, 3), .45, { th: -.8, id: 0 }); GR.unframe(); GR.restore();  // gölge
  GR.save(); GR.frame(PX, PY, rot);
  const SP = kit_sayfaYolu(PW, PH, 5);
  kit_dol(SP, .975, { th: 0, id: 1 });
  tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 4; tx.stroke(SP); tx.restore();
  // güneş (sağ üst): 'güneşe'de çevresi eş merkezli taramayla koyulaşır, güneş kâğıt beyazı parlar
  const SX = 170, SY = -290, sg = kit_a(t, Wd('B09', 'güneşe') - .1, 1.4);
  if (sg > 0) { const e = E.out3(sg), rr2 = rng(29); ox.save(); ox.strokeStyle = GR.inkCol; ox.lineCap = 'round'; ox.lineWidth = 2.6;
    for (let i = 0; i < 20; i++) { const a = i / 20 * TAU + .05, l = (40 + rr2() * 60) * e; ox.beginPath(); ox.moveTo(SX + Math.cos(a) * 74, SY + Math.sin(a) * 74); ox.lineTo(SX + Math.cos(a) * (74 + l), SY + Math.sin(a) * (74 + l)); ox.stroke(); } ox.restore(); }
  // üst katman çizgileri yalnız çevrilen sayfanın açtığı yerde görünür
  ox.save(); { const C = new Path2D(); C.rect(-PW / 2 + PW * k - 2, -PH / 2 - 60, PW + 80, PH + 120); ox.clip(C); }
  // satırlar sırayla yazılır (her satır soldan sağa), sayfa çevrildikten sonra
  const sat = (i, y, fn) => { const u = oku_u(t, s0 + 1.3 + i * .55, s0 + 1.3 + i * .55 + .7); if (u <= 0) return; ox.save(); const C = new Path2D(); C.rect(-280, y - 40, 40 + 540 * E.io2(u), 70); ox.clip(C); fn(); ox.restore(); };
  sat(0, -300, () => { kit_karalama(ox, -110, 110, -300, 7, { w: 3.2 }); ox.save(); ox.strokeStyle = GR.inkCol; ox.lineWidth = 3; ox.beginPath(); ox.moveTo(-95, -282); ox.lineTo(95, -282); ox.stroke(); ox.restore(); });
  for (let i = 0; i < 13; i++) sat(i + 1, -212 + i * 42, () => kit_karalama(ox, -250, i === 12 ? 30 : 250, -212 + i * 42, 50 + i, { indent: i % 4 === 0 ? 40 : 0, strike: i === 3 || i === 7 || i === 8 }));
  ox.strokeStyle = GR.inkCol; ox.lineWidth = 3.4; ox.lineCap = 'round';
  ox.beginPath(); ox.arc(SX, SY, 30, 0, TAU); ox.stroke();
  const rr = rng(21);
  for (let i = 0; i < 12; i++) { const a = i / 12 * TAU + .1, l = i % 2 ? 16 : 26; ox.beginPath(); ox.moveTo(SX + Math.cos(a) * 40, SY + Math.sin(a) * 40); ox.lineTo(SX + Math.cos(a) * (40 + l + rr() * 5), SY + Math.sin(a) * (40 + l + rr() * 5)); ox.stroke(); }
  ox.restore();
  GR.unframe(); GR.restore();
  // sayfa çevrilir: üstteki boş sayfa sol kenarı çevresinde kapanır
  if (pt < 1) {
    GR.save(); GR.frame(PX - PW / 2, PY, rot); tx.scale(k, 1); px.scale(k, 1);
    const Q = kit_sayfaYolu(PW, PH, 9), Q2 = new Path2D(); Q2.addPath(Q, new DOMMatrix().translate(PW / 2, 0));
    kit_dol(Q2, lerp(.975, .6, E.io2(pt)), { th: PI / 2, id: 0 });
    tx.strokeStyle = GR.tone(.02); tx.lineWidth = 4 / Math.max(k, .2); tx.stroke(Q2);
    GR.unframe(); GR.restore();
  }
  // sağ yarı: «tiyatro oyununun»da sahne (perde, döşeme) ve tek küçük siluet; «güneşe»de sayfadaki güneşten siluete ışın çizgileri
  const tT = Wd('B09', 'tiyatro') - .2, as = kit_a(t, tT, 1.2), af = kit_a(t, tT + .7, 1.2);
  if (as > 0) {
    const X0 = 1170, X1 = 1760, Yt = 150, Yf = 500, e = E.io2(as);
    kit_hat(X0 - 10, Yf, X1 + 10, Yf, 6); kit_hat(X0 + 10, Yf + 14, X1 - 10, Yf + 14, 3);
    const V = new Path2D(); poly(V, [[X0, Yt], [X1, Yt], [X1, Yt + 40]].concat(Array.from({ length: 7 }, (_, k) => [lerp(X1, X0, (k + .5) / 7), Yt + 40 + (k % 2 ? 0 : 22)])).concat([[X0, Yt + 40]]), true);
    tx.save(); tx.globalAlpha = e; kit_dol(V, .03); tx.restore();
    for (const sd of [-1, 1]) {   // yana toplanmış perdeler: kıvrımlı koyu kütle, kâğıt rengi kıvrım vuruşları
      const xo = sd < 0 ? X0 : X1, w = 120 * e, P = new Path2D();
      spline(P, [[xo, Yt + 30], [xo - sd * w, Yt + 30], [xo - sd * w * .55, Yt + 200], [xo - sd * w * .8, Yf], [xo, Yf]], true, .6); kit_dol(P, .03);
      if (e > .5) for (let k = 0; k < 3; k++) oku_vurus([[xo - sd * (20 + k * 28) * e, Yt + 60], [xo - sd * (14 + k * 20) * e, Yt + 230], [xo - sd * (24 + k * 30) * e, Yf - 10]], 5, .95, .3);
    }
    if (af > 0) { GR.tx.save(); GR.tx.globalAlpha = E.sine(af); kit_bas(kit_pelerinli(1468, Yf - 2, 30, -1, { tilt: .34, seed: 13 }), .02); GR.tx.restore(); }
    const ag = kit_a(t, Wd('B09', 'güneşe') - .1, 1.3);
    if (ag > 0) {   // güneşten siluetin başına seyrek ışın çizgileri (üst katman)
      const sx = PX + Math.cos(rot) * SX - Math.sin(rot) * SY, sy = PY + Math.sin(rot) * SX + Math.cos(rot) * SY, hd = [1450, Yf - 7.25 * 30], u = E.io2(ag);
      ox.save(); ox.strokeStyle = GR.inkCol; ox.lineCap = 'round';
      for (let k = -2; k <= 2; k++) { const a0 = Math.atan2(hd[1] - sy, hd[0] - sx) + k * .05, L = Math.hypot(hd[0] - sx, hd[1] - sy) - 60, r0 = 56;
        ox.lineWidth = k ? 2.6 : 3.4; ox.beginPath(); ox.moveTo(sx + Math.cos(a0) * r0, sy + Math.sin(a0) * r0); ox.lineTo(sx + Math.cos(a0) * (r0 + L * u * (k ? .9 : 1)), sy + Math.sin(a0) * (r0 + L * u * (k ? .9 : 1))); ox.stroke(); }
      ox.restore();
    }
  }
  kit_yaz('Oraya geleceğiz.', 1465, 650, { f: 'a', px: 84, a: kit_a(t, Wd('B09', 'oraya') - .15, 1), wipe: true });
}
plan('P016', (ctx, st) => levha(ctx, camLerp({ cx: 945 }, { cx: 985 }, st.p, E.sine), () => kit_taslak(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P026 (C09): yarı ışık yarı gölge profil; iki cevap ════════
// büst: baş (SF.headPath) + saç + boyun + omuz; dir -1 sola bakar
function kit_bustYollari(cx, cy, h, dir, tilt = 0, t = 0, sw = 1) {
  const out = [];
  const L = (x, y) => [cx + x * dir * h, cy + y * h];
  out.push(...SF.hairPaths(cx, cy, h, dir, tilt, t, .2, 1, 3));
  const N = new Path2D(); spline(N, [L(.18, .3), L(-.3, .25), L(-.42, .7), L(-.5, 1.05), L(.42, 1.1), L(.3, .62)].map(p => p), true, .7); out.push(N);
  const B = new Path2D(); spline(B, [L(-.46, .82), L(-.95 * sw, .98), L(-1.5 * sw, 1.2), L(-1.8 * sw, 1.6), L(-1.95 * sw, 2.4), L(1.7 * sw, 2.4), L(1.55 * sw, 1.5), L(1.25 * sw, 1.18), L(.75 * sw, 1.0), L(.36, .9)], true, .8); out.push(B);
  out.push(SF.headPath(cx, cy, h, dir, tilt));
  return out;
}
function kit_ikiCevap(st) {
  const t = st.t, { tx, px } = GR, XS = 960 - 60 * E.sine(oku_u(t, Wd('C09', 'kendini') - .3, Wd('C09', 'yürüyecek', 0, true)));
  // sol yarı gece (düz siyah), sağ yarı kâğıt
  const Lh = new Path2D(); Lh.rect(-10, -10, XS + 10, H + 20); kit_dol(Lh, .02);
  kit_cerceve(.02);
  // çerçevenin sol yarısı kâğıt rengi
  tx.save(); tx.clip(Lh); px.save(); px.clip(Lh); kit_cerceve(.97); tx.restore(); px.restore();
  const cx = 900, cy = 330, h = 270, ps = kit_bustYollari(cx, cy, h, -1, .06, t);
  const IC = new Path2D(); IC.rect(62, 62, W - 124, H - 124); GR.save(); GR.tx.clip(IC); GR.px.clip(IC);
  const Rh = new Path2D(); Rh.rect(XS, -10, W, H + 20);
  // ışık yanı (yüz, sol): kâğıt; ayrım çizgisine doğru taramayla gölgelenir
  tx.save(); px.save(); tx.clip(Lh); px.clip(Lh);
  const g = tx.createLinearGradient(XS - 240, 0, XS, 0); g.addColorStop(0, GR.tone(.97)); g.addColorStop(.55, GR.tone(.9)); g.addColorStop(1, GR.tone(.42));
  for (const P of ps) GR.fill(P, g, { type: 'bend', ox: XS, oy: cy - h, a: PI / 2, k: .0008, id: 0 });
  tx.restore(); px.restore();
  // gölge yanı (ense, sağ): düz siyah; ışığa bakan ince kenar yok (tam gölge)
  tx.save(); px.save(); tx.clip(Rh); px.clip(Rh);
  for (const P of ps) GR.fill(P, GR.tone(.02), { th: 0, id: 0 });
  tx.restore(); px.restore();
  GR.restore();
  // yazılar: söylendikçe
  kit_yaz('özgürlük', 400, 440, { f: 'a', px: 96, v: .975, bg: .02, a: kit_a(t, Wd('C09', 'özgürlük') - .1, .9), wipe: true });
  const tk = Wd('C09', 'kıskançlık') - .1;
  kit_yaz('kıskançlık', 1500, 400, { f: 'a', px: 96, a: kit_a(t, tk, .9), wipe: true });
  kit_yaz('ve gurur', 1500, 506, { f: 'a', px: 96, a: kit_a(t, Wd('C09', 'gurur') - .3, .8), wipe: true });
}
plan('P026', (ctx, st) => levha(ctx, camLerp({ cx: 975 }, { cx: 945 }, st.p, E.lin), () => kit_ikiCevap(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ kendi siluetlerimiz (şemalar için sade, okunur biçimler) ════════
// Pelerinli ayakta figür: ayak ortası (x, yF), boy Hh = baş birimi (toplam ~7,7 baş), dir yüz yönü.
// o: {tilt (baş: + yukarı), arm: 'up' (ön kol yukarı), walk (adım; pelerin geriye), lean, seed}
function kit_pelerinli(x, yF, hh, dir = 1, o = {}) {
  const L = (a, b) => [x + a * dir * hh + (o.lean || 0) * (yF - (yF + b * hh)) * dir * .12, yF + b * hh];
  const out = [], wk = o.walk ? 1 : 0;
  const tilt = o.tilt ?? .2, hc = L(.12, -7.25);
  out.push(...SF.hairPaths(hc[0], hc[1], hh, dir, tilt, 0, .2, 1, o.seed || 3));
  out.push(SF.headPath(hc[0], hc[1], hh, dir, tilt));
  const N = new Path2D(); spline(N, [L(-.22, -6.95), L(.22, -6.9), L(.3, -6.35), L(-.32, -6.35)], true, .6); out.push(N);
  const B = new Path2D();
  spline(B, [L(-.25, -6.72), L(-.95, -6.4), L(-1.15, -5.7), L(-1.18 - .1 * wk, -4.1), L(-1.3 - .35 * wk, -2.2), L(-1.5 - .6 * wk, -.45),
    L(-1.05 - .45 * wk, -.3), L(-.62 - .3 * wk, -.5), L(-.2 - .15 * wk, -.3), L(.25, -.5), L(.66 + .1 * wk, -.34), L(1.0 + .15 * wk, -.52),
    L(.95, -2.3), L(.82, -3.8), L(1.02, -5.25), L(.88, -6.15), L(.28, -6.7)], true, .85);
  out.push(B);
  // ayaklar: hem altından
  const F1 = new Path2D(), F2 = new Path2D(), s1 = wk * .55, s2 = -wk * .7;
  poly(F1, [L(-.2 + s1, -.55), L(.12 + s1, -.55), L(.62 + s1, -.1), L(.66 + s1, 0), L(-.22 + s1, 0)].map(p => p), true);
  poly(F2, [L(-.75 + s2, -.55), L(-.42 + s2, -.55), L(-.02 + s2, -.12), L(0 + s2, 0), L(-.78 + s2, 0)], true);
  out.push(F1, F2);
  if (o.arm === 'up') { const A = new Path2D(); spline(A, [L(.55, -6.25), L(1.25, -7.3), L(1.75, -8.6), L(1.98, -8.75), L(2.08, -8.55), L(1.6, -7.2), L(.95, -5.7)], true, .7); out.push(A); }
  return out;
}
// pelerin kıvrım vuruşları: hem çizgisinden yukarı giren, sivrilen kâğıt rengi çizgiler
function kit_kivrim(x, yF, hh, dir, seed, v = .97, n = 4) {
  const r = rng(seed), { tx } = GR; tx.save(); tx.fillStyle = GR.tone(v);
  for (let i = 0; i < n; i++) {
    const u = -1.05 + i * (1.75 / Math.max(1, n - 1)) + (r() - .5) * .2, len = (1.6 + r() * 2.2) * hh, w = Math.max(3, hh * .06), A = [], B = [];
    for (let k = 0; k <= 10; k++) { const s = k / 10, xx = x + (u + .12 * Math.sin(s * 2 + i)) * dir * hh, yy = yF - .5 * hh - s * len, hw = Math.max(1.2, w * (1 - s)); A.push([xx - hw, yy]); B.push([xx + hw, yy]); }
    const P = new Path2D(); poly(P, [...A, ...B.reverse()], true); tx.fill(P);
  }
  tx.restore();
}
// çökmüş (diz çöken, başı eğik) kütle: taban ortası (x, yB), birim s
function kit_cokmus(x, yB, s, dir = 1) {
  const L = (a, b) => [x + a * dir * s, yB + b * s], out = [];
  const B = new Path2D(); spline(B, [L(-1.0, 0), L(-1.08, -.5), L(-.95, -1.1), L(-.6, -1.55), L(-.12, -1.74), L(.3, -1.6), L(.52, -1.2), L(.85, -.75), L(1.04, -.3), L(1.02, 0)], true, .8); out.push(B);
  const hc = L(.36, -1.72); out.push(SF.headPath(hc[0], hc[1], s * .78, dir, -.95));
  return out;
}
// kıvrılmış figür (dizler göğüste, kollar dizleri sarar): merkez (x, y), birim s
function kit_kivrik(x, y, s, dir = 1) {
  const L = (a, b) => [x + a * dir * s, y + b * s], out = [];
  const hc = L(.3, -.78); out.push(SF.headPath(hc[0], hc[1], s * .62, dir, -.75));
  const B = new Path2D(); spline(B, [L(.05, -.62), L(-.35, -.62), L(-.7, -.32), L(-.8, .1), L(-.72, .45), L(-.5, .7), L(-.1, .8), L(.42, .82), L(.74, .78), L(.76, .62), L(.6, .5), L(.66, .2), L(.8, -.12), L(.74, -.38), L(.52, -.48), L(.3, -.44)], true, .85); out.push(B);
  return out;
}
// kıvrık figürün kolu (dizleri saran) — figürle zıt tonda ince çizgi
function kit_kivrikKol(x, y, s, dir, v) { const L = (a, b) => [x + a * dir * s, y + b * s], { tx } = GR; tx.save(); tx.strokeStyle = GR.tone(v); tx.lineWidth = Math.max(3.5, s * .06); tx.lineCap = 'round'; tx.beginPath(); tx.moveTo(...L(-.38, -.42)); tx.quadraticCurveTo(...L(.05, -.05), ...L(.64, .02)); tx.stroke(); tx.restore(); }
// yolları tek tonda bas (a < 1: geçiş tonu taramayla); sep: kâğıt rengi ayırma çizgisi (öndeki figür arkadakinden ayrılsın)
function kit_bas(paths, v, a = 1, sep = 0, hs = { th: 0, id: 0 }) {
  if (a <= 0) return; const { tx } = GR;
  if (sep > 0) { tx.save(); tx.strokeStyle = GR.tone(KIT_K); tx.lineWidth = sep * 2; tx.lineJoin = 'round'; for (const P of paths) tx.stroke(P); tx.restore(); }
  const bg = v < .5 ? KIT_K : .02;
  for (const P of paths) GR.fill(P, GR.tone(lerp(bg, v, E.sine(a))), hs);
}
// iç alan kırpması (çerçevenin içi)
function kit_kirp(fn, m = 62) { const C = new Path2D(); C.rect(m, m, W - 2 * m, H - 2 * m); GR.save(); for (const c of [GR.tx, GR.px, GR.ox]) c.clip(C); fn(); GR.restore(); }

// ════════ P029 (C12): iki siluet: önder ve tek yürüyen ════════
// kalabalık: üst üste binen sıralar (arkadakiler küçük ve yukarıda), boy ve duruş değişken; dir yüz yönü
function kit_kalabalik(x0, x1, yb, hh, dir, seed, a) {
  const r = rng(seed), rows = [[.74, -hh * .9, 9], [.86, -hh * .45, 8], [1, 0, 6]];
  for (const [k, dy, n] of rows) for (let i = 0; i < n; i++) {
    const h = hh * k * (.92 + .16 * r()), x = lerp(x0, x1, (i + .5 + (r() - .5) * .6) / n);
    kit_bas(kit_pelerinli(x, yb + dy, h, dir, { tilt: (r() - .5) * .3, seed: 3 + i }), .02, a, 3);
  }
}
function kit_ikiPano(st, o = {}) {
  const P1 = [150, 116, 930, 706], P2 = [990, 116, 1770, 706];
  const a1 = o.a1 ?? 1, a2 = o.a2 ?? 1, G = 640;
  for (const [x0, y0, x1, y1] of [P1, P2]) { kit_kutu(x0, y0, x1, y1, 4); kit_kutu(x0 + 13, y0 + 13, x1 - 13, y1 - 13, 2.6); }
  const pano = (P, fn) => { const C = new Path2D(); C.rect(P[0] + 15, P[1] + 15, P[2] - P[0] - 30, P[3] - P[1] - 30); GR.save(); for (const c of [GR.tx, GR.px]) c.clip(C); fn(); GR.restore(); };
  // sol: önder önde, kol kalkık; kalabalık arkasında, hepsi aynı yöne (sağa)
  if (a1 > 0) pano(P1, () => {
    kit_yer(P1[0], P1[2], G + 6, { w: 3 });
    kit_kalabalik(200, 620, G, 50, 1, 11, a1);
    kit_bas(kit_pelerinli(760, G + 8, 56, 1, { tilt: .3, arm: 'up', walk: true, seed: 7 }), .02, a1, 4);
    if (a1 >= 1) kit_kivrim(760, G + 8, 56, 1, 5, .97, 3);
  });
  // sağ: kalabalık sola gider; tek figür sağa yürür, sırtı kalabalığa dönük
  if (a2 > 0) pano(P2, () => {
    kit_yer(P2[0], P2[2], G + 6, { w: 3 });
    kit_kalabalik(1040, 1420, G, 50, -1, 23, a2 * (1 - .72 * (o.sonuk || 0)));
    kit_bas(kit_pelerinli(1640, G + 8, 56, 1, { tilt: .05, walk: true, seed: 9 }), .02, a2, 4);
    if (a2 >= 1) kit_kivrim(1640, G + 8, 56, 1, 6, .97, 3);
  });
}
function kit_kimBaskaldiran(st) {
  const t = st.t;
  kit_cerceve();
  kit_ikiPano(st, { a1: kit_a(t, Wd('C12', 'kalabalığı') - .3, 1), a2: kit_a(t, Wd('C12', 'kalabalığa') - .3, 1) });
  kit_yaz('Asıl başkaldıran kim?', 960, 800, { f: 'a', px: 84, a: kit_a(t, Wd('C12', 'asıl') - .1, 1), wipe: true });
}
plan('P029', (ctx, st) => levha(ctx, null, () => kit_kimBaskaldiran(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P043 (E04): dış siluet dik ve mağrur; altındaki su yansıması başka bir duruşta (iki büklüm, başı ellerinin arasında) ════════
// Karın ve göğüste figür yok (kurul tur 1, hassasiyet). «ama içi»de yansıma dikten çökmüşe döner (yavaş).
// yere çökmüş, iki büklüm oturan figür; başı ellerinin arasında (yandan): taban (x, yB), birim s, dir yüz yönü
function kit_basEller(x, yB, s, dir = 1) {
  const L = (a, b) => [x + a * dir * s, yB + b * s], P = new Path2D();
  spline(P, [L(-.62, 0), L(-.8, -.55), L(-.68, -1.15), L(-.38, -1.55), L(-.02, -1.62), L(.22, -1.45), L(.5, -1.3), L(.7, -1.08), L(.82, -.98), L(.98, -.62), L(1.02, -.1), L(1.22, -.02), L(1.2, 0)], true, .75);
  const hc = L(.36, -1.12); P.moveTo(hc[0] + .3 * s, hc[1]); P.ellipse(hc[0], hc[1], .3 * s, .27 * s, 0, 0, TAU);   // baş: dizlere doğru düşmüş
  return [P];
}
function kit_icFigur(t, ic) {
  const { tx, px } = GR, x = 960, yG = 560, hh = 60;
  // su: zemin çizgisinin altı; yatay, perspektifli tarama, aşağı doğru koyulaşır
  const Wt = new Path2D(); Wt.rect(0, yG, W, H - yG);
  const g = tx.createLinearGradient(0, yG, 0, H); g.addColorStop(0, GR.tone(.82)); g.addColorStop(1, GR.tone(.4));
  GR.fill(Wt, g, { type: 'persp', y0: yG, D: H - yG, p0: 9, p1: 12.5, id: 8 });
  kit_hat(62, yG, W - 62, yG, 4);
  kit_bas(kit_pelerinli(x, yG, hh, -1, { tilt: .32, seed: 5 }), .02);
  kit_kivrim(x, yG, hh, -1, 8, .97, 4);
  // yansıma: suya ters düşen koyu biçim; dik (ayna) → çökmüş (iki büklüm, baş eller arasında). Yatay kâğıt dalga kesikleriyle bölünür.
  GR.save(); { const C = new Path2D(); C.rect(0, yG + 3, W, H); tx.clip(C); px.clip(C); }
  tx.save(); tx.translate(0, 2 * yG + 6); tx.scale(1, -1);
  const dik = kit_pelerinli(x, yG, hh, -1, { tilt: .32, seed: 5 }), cok = kit_basEller(x + 30, yG, 150, -1);
  const v1 = lerp(.12, .82, E.sine(ic)), v2 = lerp(.82, .12, E.sine(ic));
  for (const P of dik) { tx.fillStyle = GR.tone(lerp(v1, .82, 0)); tx.globalAlpha = 1 - E.sine(ic); tx.fill(P); }
  tx.globalAlpha = E.sine(ic);
  for (const P of cok) { tx.fillStyle = GR.tone(.12); tx.fill(P); }
  { const L = (a, b) => [x + 30 + a * -150, yG + b * 150]; tx.lineCap = 'round'; tx.strokeStyle = GR.tone(.12); tx.lineWidth = 24;   // önkol: dizden başa
    tx.beginPath(); tx.moveTo(...L(.86, -.95)); tx.quadraticCurveTo(...L(.66, -1.25), ...L(.5, -1.3)); tx.stroke(); }
  tx.restore();
  { const r = rng(44); tx.fillStyle = GR.tone(.85); for (let y = yG + 16; y < H; y += 20 + r() * 16) { const xl = 620 + r() * 200, L = 160 + r() * 420; tx.fillRect(xl, y, L, 4 + r() * 3); } }   // dalga kesikleri
  GR.restore();
}
plan('P043', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 520, z: 1 }, { cx: 960, cy: 540, z: 1.05 }, st.p, E.sine), () => {
  kit_cerceve(); kit_kirp(() => kit_icFigur(st.t, oku_u(st.t, Wd('E04', 'ama') - .1, Wd('E04', 'kıvranıyordu', 0, true) + .4)));
}, [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P071 (G06): karşı karşıya iki aynı profil ════════
function kit_ikiProfil(st) {
  const t = st.t;
  kit_cerceve();
  kit_kirp(() => { for (const [x, d] of [[640, 1], [1280, -1]]) kit_bas(kit_bustYollari(x, 500, 180, d, .04, 0, .72), .02); });
  kit_yaz('“O hâlde kimi suçlayacaksın?”', 960, 168, { f: 'a', px: 80, a: kit_a(t, Wd('G06', 'halde') - .35, 1.1), wipe: true });
}
plan('P071', (ctx, st) => levha(ctx, camLerp({ z: 1 }, { z: 1.03 }, st.p, E.lin), () => kit_ikiProfil(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P073 (G08): dibin altında dip: yandan kesit; her dip bir öncekinin tabanında, kaydırılmış ve kaya kenarlı açılır ════════
// Toprak taralı orta ton, oyuklar düz karanlık; kenarda küçük kanatlı figür. «açan»da ikinci dip ağzını açar, «dip»te üçüncüsü karanlığa açılır.
function kit_oyuk(x0, x1, yT, yB, seed, ac) {   // kaya kenarlı oyuk: üst ağız (x0..x1, yT), taban yB; ac: 0..1 açılma (ağız genişler, derinleşir)
  const r = rng(seed), cx = (x0 + x1) / 2, hw = (x1 - x0) / 2 * E.out3(ac), d = (yB - yT) * E.out2(ac), L = [], Rr = [];
  for (let i = 0; i <= 8; i++) { const u = i / 8, w = hw * (1 - .35 * u * u) * (1 + (r() - .5) * .18), y = yT + d * u; L.push([cx - w + (r() - .5) * 18, y]); Rr.push([cx + w + (r() - .5) * 18, y]); }
  const P = new Path2D(); poly(P, [...L, ...Rr.reverse()], true); return { P, L, R: Rr };
}
function kit_dip(st) {
  const t = st.t, { tx } = GR, yS = 330;
  kit_cerceve();
  kit_kirp(() => {
    const Y = new Path2D(); Y.rect(0, yS, W, H); GR.fill(Y, GR.tone(.62), { th: -.75, id: 4 });   // toprak (kesit)
    kit_hat(62, yS, W - 62, yS, 5);
    const a2 = kit_a(t, Wd('G08', 'açan') - .4, 1.4), a3 = kit_a(t, Wd('G08', 'dip', 1) - .2, 1.6);
    const O1 = kit_oyuk(620, 1260, yS, 560, 3, 1), O2 = kit_oyuk(880, 1200, 555, 770, 7, a2), O3 = kit_oyuk(960, 1150, 765, 1120, 11, a3);
    for (const O of [O1, O2, O3]) {
      GR.fill(O.P, GR.tone(.02), { th: 0, id: 0 });
      // kaya ağzı: ışık (üstten) yanında oyuğun içine giren kısa beyaz vuruşlar
      tx.save(); tx.clip(O.P); const pts = O.L.slice(0, 5); for (let i = 0; i < pts.length - 1; i++) { const p = pts[i]; oku_vurus([[p[0] + 2, p[1] + 6], [p[0] + 30, p[1] + 26], [p[0] + 52, p[1] + 34]], 6, .95, .3); } tx.restore();
    }
    // kenarda küçük kanatlı figür (açılış figürünün küçüğü), aşağı eğilmiş
    nif_siluet7(t, 0, { x: 560, y: yS - 2, U: 150 }, { alev: false, tilt: -.7 });
  });
}
plan('P073', (ctx, st) => levha(ctx, camLerp({ cx: 960, cy: 500, z: 1 }, { cx: 960, cy: 600, z: 1 }, oku_u(st.t, st.at, st.at + Math.max(6, st.d)), E.sine), () => kit_dip(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P077 (G11): terazi: taç ve asa yükselir, figür aşağı iner ════════
function kit_tac(x, y, s) { // taç: düz bant + beş uç (ortadaki ve kenardakiler uzun), uçlarda top
  const L = (a, b) => [x + a * s, y + b * s], P = new Path2D();
  poly(P, [[-1, .35], [-1, -.7], [-.78, -.2], [-.5, -.5], [-.24, -.2], [0, -.8], [.24, -.2], [.5, -.5], [.78, -.2], [1, -.7], [1, .35]].map(([a, b]) => L(a, b)), true);
  for (const [a, b, r] of [[-1, -.8, .11], [-.5, -.6, .085], [0, -.9, .12], [.5, -.6, .085], [1, -.8, .11]]) { const c = L(a, b); P.moveTo(c[0] + r * s, c[1]); P.arc(c[0], c[1], r * s, 0, TAU); }
  return P;
}
function kit_terazi(st) {
  const t = st.t, { tx } = GR, PX = 960, PY = 250, L = 430;
  kit_cerceve();
  const th = lerp(0, .2, ramp(t, Wd('G11', 'tacım') - .2, Wd('G11', 'düşüyorum', 0, true) + .2, E.io3));
  const c = Math.cos(th), s = Math.sin(th);
  kit_yer(62, W - 62, 802, { sx: PX, sw: 230, sh: 16 });
  // ayak: gövde ve basamaklı taban; ışık yanında ince kâğıt vuruşu
  const Bs = new Path2D(); poly(Bs, [[PX - 15, PY], [PX + 15, PY], [PX + 22, 740], [PX - 22, 740]], true);
  poly(Bs, [[PX - 70, 740], [PX + 70, 740], [PX + 70, 762], [PX - 70, 762]], true); poly(Bs, [[PX - 140, 762], [PX + 140, 762], [PX + 150, 802], [PX - 150, 802]], true);
  kit_dol(Bs, .02); kit_hat(PX - 8, PY + 40, PX - 11, 720, 3, .97);
  // kefeler: uçlardan sarkan üç ip, sığ tas
  const pans = [];
  for (const sd of [-1, 1]) {
    const ex = PX + sd * L * c, ey = PY + sd * L * s, py = ey + 270;
    for (const dx of [-122, 0, 122]) kit_hat(ex, ey + 6, ex + dx, py, 3.4);
    const P = new Path2D(); P.moveTo(ex - 150, py - 3); P.quadraticCurveTo(ex, py + 72, ex + 150, py - 3); P.closePath();
    kit_dol(P, .02); kit_hat(ex - 128, py + 6, ex + 128, py + 6, 3, .97);
    pans.push([ex, py - 3]);
  }
  // kiriş
  const Bm = new Path2D(), nx = -s * 9, ny = c * 9;
  poly(Bm, [[PX - L * c + nx, PY - L * s + ny], [PX + L * c + nx, PY + L * s + ny], [PX + L * c - nx, PY + L * s - ny], [PX - L * c - nx, PY - L * s - ny]], true);
  for (const sd of [-1, 1]) { Bm.moveTo(PX + sd * L * c + 14, PY + sd * L * s); Bm.arc(PX + sd * L * c, PY + sd * L * s, 14, 0, TAU); }
  Bm.moveTo(PX + 26, PY); Bm.arc(PX, PY, 26, 0, TAU); kit_dol(Bm, .02);
  kit_hat(PX, PY - 4, PX + Math.sin(th) * 120, PY - Math.cos(th) * 120, 7, .02);             // ibre
  // sol kefe: taç ve asa (kâğıt beyazı, mürekkep kontur)
  const [lx, ly] = pans[0];
  const Cp = kit_tac(lx - 34, ly - 40, 58), Sp = new Path2D();
  poly(Sp, [[lx + 50, ly - 2], [lx + 110, ly - 196], [lx + 121, ly - 193], [lx + 63, ly]], true);
  Sp.moveTo(lx + 136, ly - 212); Sp.arc(lx + 118, ly - 212, 18, 0, TAU);
  for (const P of [Sp, Cp]) { GR.fill(P, GR.tone(.975), { th: 0, id: 1 }); tx.save(); tx.strokeStyle = GR.tone(.02); tx.lineWidth = 5; tx.lineJoin = 'round'; tx.stroke(P); tx.restore(); }
  kit_hat(lx - 34 - 58, ly - 40 + 6, lx - 34 + 58, ly - 40 + 6, 4);                              // taç bandı
  // sağ kefe: çökmüş figür (koyu)
  const [rx, ry] = pans[1];
  kit_bas(kit_cokmus(rx - 6, ry + 2, 40, -1), .02);
}
plan('P077', (ctx, st) => levha(ctx, null, () => kit_terazi(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P078 (G12): döngü: diz çöken → yükselen → başı dönen → düşen ════════
const KIT_POZ = [
  { twist: .45, lean: .2, head: -.5, armN: [.9, 1.1], armF: [.7, 1.2], legN: [1.5, -1.5], legF: [-.35, -1.35], dy: 1.7 },        // diz çöken (pişman)
  { twist: .4, lean: -.05, head: .4, armN: [2.5, .15], armF: [2.2, .25], legN: [.28, -.15], legF: [-.22, -.05], dy: 0 },         // yükselen
  { twist: .4, lean: -.2, head: .6, shTilt: .1, armN: [2.6, 2.1], armF: [-.5, .4], legN: [.15, -.05], legF: [-.32, -.1], dy: 0 },   // başı dönen
  { twist: .5, lean: .95, head: -.25, armN: [2.9, .2], armF: [2.4, .5], legN: [-.5, -.6], legF: [.4, -.9], dy: .7 },           // düşen
];
function kit_dongu(st) {
  const t = st.t, cx = 960, cy = 700, rx = 540, ry = 128, { tx } = GR;
  kit_cerceve();
  const rot = lerp(-.25, .45, clamp(st.lt / Math.max(1, st.d)));         // yavaş, tek yönlü
  const arc = (a0, a1) => { const P = new Path2D(), n = 72, A = [], B = [];
    for (let i = 0; i <= n; i++) { const a = lerp(a0, a1, i / n), x = cx + Math.sin(a) * rx, y = cy + Math.cos(a) * ry; A.push([x, y - 9]); B.push([x, y + 9]); }
    poly(P, [...A, ...B.reverse()], true); return P; };
  const chev = (a0, a1) => { for (let k = 0; k < 10; k++) { const a = rot + k / 10 * TAU; const aa = ((a - a0) % TAU + TAU) % TAU + a0; if (aa > a1) continue;
    const x = cx + Math.sin(aa) * rx, y = cy + Math.cos(aa) * ry, dx = Math.cos(aa) * rx, dy = -Math.sin(aa) * ry, l = Math.hypot(dx, dy), ux = dx / l, uy = dy / l;
    const P = new Path2D(); poly(P, [[x - ux * 9 - uy * 6, y - uy * 9 + ux * 6 - 0], [x + ux * 7, y + uy * 7], [x - ux * 9 + uy * 6, y - uy * 9 - ux * 6], [x - ux * 4, y - uy * 4]], true); kit_dol(P, .975, { th: 0, id: 1 }); } };
  kit_dol(arc(PI / 2, PI * 1.5), .02); chev(PI / 2, PI * 1.5);
  const tw = [Wd('G12', 'pişman'), Wd('G12', 'yükselince'), Wd('G12', 'başımı'), Wd('G12', 'geri')];
  const figs = KIT_POZ.map((pz, i) => { const a = rot + PI * 1.72 + i * PI / 2; return { i, pz, d: Math.cos(a), x: cx + Math.sin(a) * rx, y: cy + Math.cos(a) * ry - 6 }; });
  const draw = F => {
    const k = lerp(.8, 1.08, (F.d + 1) / 2), h = 40 * k, ap = kit_a(t, tw[F.i] - .35, 1.2);
    const J = SF.rig(Object.assign({ x: F.x, y: F.y - 3.95 * h + F.pz.dy * h, h, facing: F.d >= 0 ? 1 : -1 }, F.pz));
    kit_fig(J, { lum: 0, lit: [-.5, -.8], t, lines: 1, cloak: .9, wind: .6, seed: 11 + F.i, skirt: true }, .3 + .7 * ap);
  };
  for (const F of figs.filter(F => F.d < 0).sort((a, b) => a.d - b.d)) draw(F);
  kit_dol(arc(-PI / 2, PI / 2), .02); chev(-PI / 2, PI / 2);
  for (const F of figs.filter(F => F.d >= 0).sort((a, b) => a.d - b.d)) draw(F);
}
plan('P078', (ctx, st) => levha(ctx, null, () => kit_dongu(st), [KIT_K, 0, 1]), { tr: { type: 'fade', dur: .6 } });

// ════════ P089 (H07): sayfa kenarına düşülmüş not ════════
function kit_dizgi(x0, x1, y0, n, lh, seed, o = {}) { // basılı satırlar (okunmaz): kelime boyu kısa koyu tireler
  const r = rng(seed), P = new Path2D();
  for (let i = 0; i < n; i++) {
    const y = y0 + i * lh, end = (o.verse ? x1 - r() * (x1 - x0) * .35 : x1);
    let x = x0 + (o.verse && i % 7 === 0 ? 30 : 0);
    while (x < end - 20) { const wl = Math.min(end - x, 16 + r() * 64); P.roundRect(x, y - 3.5, wl, 7, 3.5); x += wl + 12; }
  }
  return P;
}
function kit_kenarNotu(st) {
  const t = st.t, { tx } = GR;
  kit_cerceve();
  // sayfa: sol iki sütun boyu basılı metin; işaretli satırın altı çizilir
  const X0 = 170, X1 = 980, Y0 = 150, LH = 40, N = 18, MARK = 8;
  kit_dol(kit_dizgi(X0, X1, Y0, N, LH, 17, { verse: true }), .02, { th: 0, id: 0 });
  const tz = Wd('H07', 'zorbaların') - .2, an = kit_a(t, Wd('H07', 'böyle') - .2, .9);
  // kenar çizgisi (sayfa kenarı): ince düşey
  kit_hat(1040, 120, 1040, 860, 3);
  // not: altı çizilen satır, köşeli ayraç ve el yazısı not
  if (an > 0) { const y = Y0 + MARK * LH + 14; const u = E.io2(an); tx.save(); tx.strokeStyle = GR.tone(.03); tx.lineWidth = 4; tx.lineCap = 'round'; tx.beginPath();
    for (let x = X0; x <= lerp(X0, X1 - 120, u); x += 8) tx.lineTo(x, y + Math.sin(x * .02) * 2.5); tx.stroke(); tx.restore(); }
  const ab = kit_a(t, tz - .3, .8);
  if (ab > 0) { tx.save(); tx.strokeStyle = GR.tone(.03); tx.lineWidth = 4; tx.lineCap = 'round'; const y = Y0 + MARK * LH, k = E.io2(ab);
    tx.beginPath(); tx.moveTo(1010, y - 70); tx.quadraticCurveTo(1030, y - 66, 1030, lerp(y - 50, y - 10, k)); tx.stroke();
    if (k > .5) { tx.beginPath(); tx.moveTo(1030, y - 10); tx.quadraticCurveTo(1032, y, 1050, y + 2); tx.moveTo(1030, y + 14); tx.quadraticCurveTo(1032, y + 4, 1050, y + 2); tx.stroke(); }
    if (k > .5) { tx.beginPath(); tx.moveTo(1030, y + 14); tx.quadraticCurveTo(1030, lerp(y + 14, y + 70, (k - .5) * 2), 1010, lerp(y + 14, y + 74, (k - .5) * 2)); tx.stroke(); }
    tx.restore(); }
  kit_yaz('“zorbaların', 1100, 330, { f: 'a', px: 80, align: 'left', a: kit_a(t, tz, 1.1), wipe: true, rot: -.04 });
  kit_yaz('bahanesi:', 1130, 428, { f: 'a', px: 80, align: 'left', a: kit_a(t, Wd('H07', 'bahaneyle') - .25, 1), wipe: true, rot: -.04 });
  kit_yaz('zorunluluk”', 1160, 526, { f: 'a', px: 80, align: 'left', a: kit_a(t, Wd('H07', 'zorunlulukla') - .2, 1.1), wipe: true, rot: -.04 });
}
plan('P089', (ctx, st) => levha(ctx, null, () => kit_kenarNotu(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P112 (J09): kural, levha yazısı (koyu levha) ════════
function kit_yilanCizgi(x0, x1, y, a, v = .975) { // kuyruktan başa kalınlaşan, kıvrılan yılan (kâğıt rengi)
  if (a <= 0) return;
  const n = 120, A = [], B = [], u1 = E.io2(a), f = u => [lerp(x0, x1, u), y + Math.sin(u * PI * 3) * 22 * (.35 + .65 * u)];
  for (let i = 0; i <= n; i++) { const u = i / n * u1, p = f(u), q = f(u + .002), an = Math.atan2(q[1] - p[1], q[0] - p[0]), nx = -Math.sin(an), ny = Math.cos(an), w = lerp(1.6, 11, Math.pow(u, .6));
    A.push([p[0] + nx * w, p[1] + ny * w]); B.push([p[0] - nx * w, p[1] - ny * w]); }
  const P = new Path2D(); poly(P, [...A, ...B.reverse()], true);
  const h = f(u1), q = f(u1 - .004), an = Math.atan2(h[1] - q[1], h[0] - q[0]);
  P.moveTo(h[0] + Math.cos(an) * 28, h[1] + Math.sin(an) * 28); P.ellipse(h[0] + Math.cos(an) * 10, h[1] + Math.sin(an) * 10, 20, 13, an, 0, TAU);
  GR.fill(P, GR.tone(v), { th: 0, id: 0 });
  if (a >= 1) { const e = new Path2D(), ex = h[0] + Math.cos(an) * 16 - Math.sin(an) * 4, ey = h[1] + Math.sin(an) * 16 + Math.cos(an) * 4 - 5; e.arc(ex, ey, 3.2, 0, TAU); kit_dol(e, .02); }
}
function kit_kural(st) {
  const t = st.t;
  kit_cerceve(.97);
  kit_cizgi(960, 250, 220, { v: .97, a: kit_a(t, S('J09'), 1) });
  const L1 = 'günah hangi kılıkta,'.toLocaleUpperCase('tr'), L2 = 'ceza o kılıkta'.toLocaleUpperCase('tr');
  kit_yaz(L1, 960, 410, { f: 'b', px: 84, ls: 8, v: .975, bg: .02, a: kit_a(t, Wd('J09', 'günahı') - .2, 1.2), wipe: true });
  kit_yaz(L2, 960, 540, { f: 'b', px: 84, ls: 8, v: .975, bg: .02, a: kit_a(t, Wd('J09', 'cezasını') - .2, 1.2), wipe: true });
  kit_yilanCizgi(660, 1240, 690, kit_a(t, Wd('J09', 'zafer') - .3, 2.4));
}
plan('P112', (ctx, st) => levha(ctx, null, () => kit_kural(st), [.02, 0, 1]), { tr: KIT_TR });

// ════════ P117 (K03): iki sütunlu levha ════════
function kit_ok(x, y0, y1, a) { // aşağı inen ok (mürekkep vuruşu)
  if (a <= 0) return; const y = lerp(y0, y1, E.io2(a)); kit_hat(x, y0, x, y, 5);
  if (a >= 1) { const P = new Path2D(); poly(P, [[x - 20, y1 - 28], [x, y1 + 4], [x + 20, y1 - 28], [x, y1 - 18]], true); kit_dol(P, .02); }
}
function kit_ikiSutun(st) {
  const t = st.t;
  kit_cerceve();
  kit_hat(960, 150, 960, 820, 3); kit_hat(974, 150, 974, 820, 3);
  const tI = Wd('K03', 'insan') - .2, tM = Wd('K03', 'merhamet') - .2, tA = Wd('K03', 'asi') - .2, tY = Wd('K03', 'bulamayacak') - .1;
  // sol
  kit_satirlar(['İnsan aldatıldı'], 540, 290, 84, [tI], t, { f: 'a', px: 80, wipe: true });
  kit_ok(540, 380, 560, kit_a(t, tI + 1, 1.2));
  kit_yaz('MERHAMET', 540, 660, { f: 'b', px: 92, ls: 10, a: kit_a(t, tM, 1), wipe: true });
  // sağ
  kit_satirlar(['Asi melek', 'kendi kendini ayarttı'], 1394, 290, 88, [tA, tA + .6], t, { f: 'a', px: 80, wipe: true });
  kit_ok(1394, 380, 560, kit_a(t, tA + 1.4, 1.2));
  kit_yaz('YOK', 1394, 660, { f: 'b', px: 92, ls: 10, a: kit_a(t, tY - .4, .5), wipe: true });   // vuruş anında ('bulamayacak' başlarken) tam yazılmış
}
plan('P117', (ctx, st) => levha(ctx, null, () => kit_ikiSutun(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P120 (K06): destanın ilk sayfası ════════
function kit_ilkSayfa(st) {
  const t = st.t, { tx } = GR;
  kit_cerceve();
  // sayfa (sol): süslü baş harf kutusu + dize satırları; 26. dize işaretli
  const X0 = 190, Y0 = 170, LH = 30;
  kit_cizgi(470, 140, 200, { lozenge: false, th: 4 });
  const Bx = new Path2D(); Bx.rect(X0, Y0 - 12, 92, 92); GR.fill(Bx, GR.tone(.3), { th: -.8, id: 0 });
  kit_kutu(X0, Y0 - 12, X0 + 92, Y0 + 80, 3);
  kit_dol(kit_dizgi(X0 + 110, 760, Y0, 3, LH, 31), .02, { th: 0, id: 0 });
  kit_dol(kit_dizgi(X0, 760, Y0 + 3 * LH, 20, LH, 37, { verse: true }), .02, { th: 0, id: 0 });
  const y26 = Y0 + 21 * LH, am = kit_a(t, Wd('K06', 'tanrının') - .5, .8);
  if (am > 0) { kit_hat(X0 - 12, y26 + 12, lerp(X0 - 12, 700, E.io2(am)), y26 + 12, 4); }
  // dize (sağ)
  const tq = Wd('K06', 'tanrının') - .15;
  kit_satirlar(['Tanrı’nın yollarının', 'adil olduğunu göstermek'], 1320, 420, 92, [tq, Wd('K06', 'adil') - .3], t, { f: 'a', px: 80, wipe: true });
  kit_yaz('KAYIP CENNET · I. 26', 1320, 590, { f: 'b', px: 40, w: 600, ls: 3, a: kit_a(t, Wd('K06', 'göstermek') - .1, .9) });
}
plan('P120', (ctx, st) => levha(ctx, null, () => kit_ilkSayfa(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P127 (K14): levha yazısı ════════
function kit_levhaYazisi(st) {
  const t = st.t, tq = Wd('K14', 'tanrı') - .2;
  kit_cerceve();
  kit_cizgi(960, 310, 180, { a: kit_a(t, S('K14') + .2, 1) });
  kit_satirlar(['“Tanrı insanı,', 'insanın efendisi yapmadı.”'], 960, 470, 104, [tq, Wd('K14', 'insanın') - .25], t, { f: 'a', px: 92, wipe: true });
  kit_cizgi(960, 640, 180, { a: kit_a(t, S('K14') + .2, 1) });
}
plan('P127', (ctx, st) => levha(ctx, null, () => kit_levhaYazisi(st), [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P139 (L08b): siyah zeminde tek satır (en sessiz an) ════════
plan('P139', (ctx, st) => levha(ctx, null, () => {
  const t = st.t;
  kit_satirlar(['Belki herkesin, söylemeyi kendine', 'yasakladığı bir söz vardır.'], 960, 470, 100, [S('L08b') - .1, Wd('L08b', 'yasakladığı') - .35], t, { f: 'a', px: 80, v: .975, bg: .02, dur: 1.8 });
}, [.02, 0, 1]), { tr: { type: 'fade', dur: 1.0 } });

// ════════ P141 (L10): iki soru ════════
plan('P141', (ctx, st) => levha(ctx, null, () => {
  const t = st.t;
  kit_cerceve();
  kit_yaz('O gözyaşı pişmanlık mıydı, gurur mu?', 960, 340, { f: 'a', px: 84, a: kit_a(t, Wd('L10', 'gözyaşı') - .45, 1.2), wipe: true });
  kit_cizgi(960, 470, 150, { a: kit_a(t, Wd('L10', 've') - .2, .9) });
  kit_yaz('Başkaldırı ne zaman özgürlük?', 960, 600, { f: 'a', px: 84, a: kit_a(t, Wd('L10', 'başkaldırı') - .25, 1.2), wipe: true });
}, [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P142 (L11): bitiş ekranı ════════
// Yuvaların içi boş kalır (YouTube öğeleri gelecek): video 150–930 × 232–671 (780×439, 16:9), abone merkez (1470, 452) çap 280.
plan('P142', (ctx, st) => levha(ctx, null, () => {
  const t = st.t, { tx, px } = GR;
  kit_cerceve();
  // video kutusu tam 16:9 (780×439), abone dairesi çap 280; ikisi güvenli alanda (x 120–1800), aralarında 240 px; grup ortalı
  kit_kutu(164, 240, 916, 663, 4); kit_kutu(150, 232, 930, 671, 2.6);
  const ring = (r, w) => { const P = new Path2D(); P.arc(1470, 452, r + w / 2, 0, TAU); P.arc(1470, 452, r - w / 2, 0, TAU, true); kit_dol(P, .02); };
  ring(132, 4); ring(139, 2.6);
  kit_cizgi(960, 735, 260, { a: 1 });
  kit_yaz('ZAMAN KURYESİ', 960, 790, { f: 'b', px: 64, ls: 16, a: kit_a(t, S('L11') + .2, 1.2), wipe: true });
}, [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════════════ BİLEŞİK LEVHALAR ════════════════
// Her pano kendi gravür geçişiyle (kendi kamerasıyla) ayrı bir tuvale basılır, sonra levhanın üstüne kendi dikdörtgenine kırpılarak konur.
// Böylece başka setlerin çizicileri (iç içe GR.frame kullananlar dahil) hiç değiştirilmeden yarım ya da üçte bir levhaya girer.
const KIT_BUF = [0, 1, 2].map(() => { const c = makeCanvas(DW, DH); return c.getContext('2d', { willReadFrequently: true }); });
function kit_pano(ctx, i, cam, fn, r, bg = [.04, 0, 1]) {   // r: [x, y, w, h] ekran px
  if (r[2] <= 1 || r[3] <= 1) return;
  const b = KIT_BUF[i]; levha(b, cam, fn, bg);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.beginPath(); ctx.rect(r[0] * RS, r[1] * RS, r[2] * RS, r[3] * RS); ctx.clip(); ctx.drawImage(b.canvas, 0, 0); ctx.restore();
}
// pano kamerası: dünya noktası (wx, wy), panonun ortasına (r) gelsin; z yakınlık
const kit_panoKam = (wx, wy, r, z = 1) => ({ cx: wx - (r[0] + r[2] / 2 - W / 2) / z, cy: wy - (r[1] + r[3] / 2 - H / 2) / z, z });

// ════════ P015 (B08): ikiye bölünmüş levha: karanlıkta kör şair | gölde melek; iki yarı ortadan açılır ════════
plan('P015', (ctx, st) => {
  const t = st.t, u = E.io2(kit_a(t, S('B08') - .1, 1.3)), w = 880 * u;
  levha(ctx, null, () => { const B = new Path2D(); B.rect(-10, -10, W + 20, H + 20); kit_dol(B, .03); kit_cerceve(.95); }, [.03, 0, 1]);
  const RL = [960 - 8 - w, 62, w, H - 124], RR = [968, 62, w, H - 124];
  kit_pano(ctx, 0, kit_panoKam(720, 520, [80, 62, 880, H - 124]), () => cizOda(t, { sair: { bas: .5 } }), RL, [.03, 0, 1]);
  kit_pano(ctx, 1, kit_panoKam(900, 560, [968, 62, 880, H - 124]), () => cizGol(t, { head: .5, sway: .02 }), RR);
}, { tr: KIT_TR });

// ════════ P111 (J06): Nifates'te dik duran siluet | tıslayan salon ════════
function kit_salon(t, uz) {   // sade salon: üstten sızan ışık, iki sütun; boyunları uzayan koyu kalabalık kütlesi, açık ağızlar
  const { tx } = GR;
  tx.fillStyle = GR.tone(.04); tx.fillRect(-200, -200, W + 400, H + 400);
  PR.glow(1440, 360, 60, 560, 1, .95); PR.glow(1440, 360, 20, 260, 1, .8);
  for (const x of [1080, 1800]) { const C = new Path2D(); C.rect(x - 38, 60, 76, 1000); GR.fill(C, GR.tone(.03), { th: 0, id: 0 }); kit_hat(x - 30, 70, x - 30, 1000, 4, .9); }
  const r = rng(91), rows = [[640, 30, .7], [720, 40, .85], [820, 52, 1]];
  for (const [yb, s, k] of rows) {
    const U = new Path2D(); let x = 960 - s;
    const heads = [];
    while (x < 1960) { const hgt = s * (1.6 + 2.6 * uz * (.6 + .6 * r())) * k, lean = (r() - .5) * .8 + (x < 1440 ? .4 : -.4), ph = r() * TAU; heads.push([x, hgt, lean, ph]); x += s * (1.1 + .5 * r()); }
    const B = new Path2D(); B.rect(940, yb, 1000, 400);
    for (const [hx, hgt, lean, ph] of heads) {
      B.moveTo(hx + s * .7, yb + 4); B.ellipse(hx, yb + 4, s * .7, s * .55, 0, PI, TAU);   // omuz yumrusu
      const sw = Math.sin(t * 1.3 + ph) * s * .15 * uz, top = [hx + lean * hgt * .5 + sw, yb - hgt], pts = [];
      for (let q = 0; q <= 10; q++) { const v = q / 10; pts.push([lerp(hx, top[0], v) + Math.sin(v * PI * 1.5 + ph) * s * .25 * uz, lerp(yb, top[1], v)]); }
      oku_vurus(pts, s * .5, .03, .7);
      const d = lean >= 0 ? 1 : -1, Hd = new Path2D(); Hd.ellipse(top[0] + d * s * .2, top[1], s * .42, s * .26, d * .2, 0, TAU); GR.fill(Hd, GR.tone(.03), { th: 0, id: 0 });
      if (uz > .4) oku_vurus([[top[0] + d * s * .1, top[1] + 2], [top[0] + d * s * .55, top[1] + s * .12 * uz]], Math.max(3, s * .1), .97, .3);   // açık ağız
    }
    GR.fill(B, GR.tone(.03), { th: 0, id: 0 });
  }
}
plan('P111', (ctx, st) => {
  const t = st.t, uz = E.io2(kit_a(t, Wd('J06', 'şimdi') - .2, 2.6));
  levha(ctx, null, () => { const B = new Path2D(); B.rect(-10, -10, W + 20, H + 20); kit_dol(B, .03); kit_cerceve(.95); }, [.03, 0, 1]);
  const RL = [80, 62, 872, H - 124], RR = [968, 62, 872, H - 124];
  kit_pano(ctx, 0, kit_panoKam(900, 600, RL), () => cizNifates(t, { fig: (tp, S0) => nif_seytan({ x: tp[0], y: 0, ground: tp[1] + 2, h: 44, facing: 1, twist: .35, head: .2, t, lum: .2, lit: nif_isik(S0, tp[0], tp[1] - 100) }) }), RL, [.5, 0, 1]);
  kit_pano(ctx, 1, null, () => kit_salon(t, .15 + .85 * uz), RR, [.04, 0, 1]);
}, { tr: KIT_TR });

// ════════ P122 (K08): filmde duyduğumuz Şeytan sözleri sayfada birikir (yalnız senaryodaki sözler, kelimesi değişmeden) ════════
const KIT_SOZ = [
  ['“Cehennemde hükümdar olmak,', 'cennette hizmetkâr olmaktan yeğdir.”', 520, 210, -.02],
  ['“Zihin kendi dünyasıdır.”', null, 1400, 250, .03],
  ['“Meydanı kaybettik; ne çıkar?”', null, 640, 450, .02],
  ['“Ben cehennemim.”', null, 1380, 480, -.03],
  ['“Elveda umut.”', null, 540, 660, -.015],
  ['“Kötülük: sen benim iyiliğim ol.”', null, 1300, 720, .02],
];
plan('P122', (ctx, st) => levha(ctx, null, () => {
  const t = st.t, t0 = S('K08') + .1, dt = Math.max(.5, (Se('K08') - t0 - .6) / KIT_SOZ.length);
  kit_cerceve();
  KIT_SOZ.forEach(([a, b, x, y, rot], i) => {
    const ai = kit_a(t, t0 + i * dt, 1);
    kit_yaz(a, x, y, { f: 'a', px: 66, a: ai, wipe: true, rot });
    if (b) kit_yaz(b, x + 10, y + 80, { f: 'a', px: 66, a: kit_a(t, t0 + i * dt + .45, 1), wipe: true, rot });
  });
}, [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P130 (K16): C12'nin iki silueti geri gelir; Abdiel'in sözünde tek yürüyen vurgulanır ════════
plan('P130', (ctx, st) => levha(ctx, null, () => {
  const t = st.t, v = E.io2(kit_a(t, Wd('K16', 'sen') - .2, 1.2));
  kit_cerceve();
  kit_ikiPano(st, { a1: 1 - .72 * v, a2: 1, sonuk: v });
  kit_yaz('Başkaldırı her zaman özgürlük müdür?', 960, 800, { f: 'a', px: 80, a: kit_a(t, Wd('K16', 'başkaldırı') - .2, 1.2), wipe: true });
}, [KIT_K, 0, 1]), { tr: KIT_TR });

// ════════ P135 (L05): aynı profil, iki etiket; altında kilitli söz ════════
let KIT_P135 = null;
plan('P135', (ctx, st) => {
  const t = st.t;
  levha(ctx, { cx: 940, cy: 550, z: 1.04 }, () => {
    const J = cizProfil(t, { iz: 1, head: .1 }), { ox } = GR;
    KIT_P135 = J;
    const lab = [[gol_hl(J, .3, -.055), 'pişmanlık mı,', 1430, 560, Wd('L05', 'pişmanlık')], [gol_hl(J, .3, -.2), 'gurur mu?', 1430, 330, Wd('L05', 'gurur')]];
    for (const [p, s, x, y, tw] of lab) {
      const a = kit_a(t, tw - .2, .9); if (a <= 0) continue;
      kit_yaz(s, x, y, { f: 'a', px: 76, v: .975, bg: .03, a, wipe: true, align: 'left' });
      const e = E.out3(a); ox.save(); ox.strokeStyle = GR.paperCol; ox.lineWidth = 3; ox.lineCap = 'round'; ox.beginPath(); ox.moveTo(x - 24, y); ox.lineTo(lerp(x - 24, p[0] + 40, e), lerp(y, p[1], e)); ox.stroke(); ox.restore();
    }
  });
}, { tr: KIT_TR,
  over: (ctx, st) => { const t = st.t, tB = Wd('L05', 'boyun'), tY = Wd('L05', 'yasaklıyor');
    nif_kilitliSoz(ctx, 'boyun eğmek', 1440, 780, clamp((t - tB + .3) / .6) * clamp((st.end - t) / .5), clamp((t - tY + .2) / .7)); } });

// ════════ P136 (L06): üç pano: göl | kaçış | içteki göl ════════
plan('P136', (ctx, st) => {
  const t = st.t, P = [[120, 250, 540, 600], [690, 250, 540, 600], [1260, 250, 540, 600]];
  const tw = [S('L06'), Wd('L06', 'kaçan') - .3, Wd('L06', 'cehennemi') - .3];
  levha(ctx, null, () => {
    kit_cerceve();
    P.forEach(([x, y, w, h]) => { kit_kutu(x - 14, y - 14, x + w + 14, y + h + 14, 4); });
    kit_yaz('Onu orada tutan neydi?', 960, 150, { f: 'a', px: 80, a: kit_a(t, Wd('L06', 'orada') - .3, 1.1), wipe: true });
  }, [KIT_K, 0, 1]);
  const ac = i => { const a = kit_a(t, tw[i], 1.2); return a; };
  const op = (i, r) => { const a = E.io2(ac(i)), hh = r[3] * a; return [r[0], r[1] + (r[3] - hh) / 2, r[2], hh]; };   // pano ortadan açılır
  kit_pano(ctx, 0, kit_panoKam(900, 600, P[0], .9), () => cizGol(t, { sway: .02 }), op(0, P[0]));
  kit_pano(ctx, 1, kit_panoKam(960, 520, P[1], .9), () => { kao_bosluk(t, { lt: t - S('L06'), cx: 960, cy: 120, r0: 140, r1: 1100, sy: .8 }); kao_ucan(t, { x: 960, y: 640 - 60 * kit_a(t, tw[1], 8), h: 34, lean: -.2, head: .35, open: .95, lift: .7, flap: Math.sin(t * 1.6) * .15, lum: .08, lit: [0, -1], seed: 9 }); }, op(1, P[1]));
  kit_pano(ctx, 2, kit_panoKam(860, 560, P[2], .9), () => nif_kancaA01(t, 1), op(2, P[2]), [.5, 0, 1]);
}, { tr: KIT_TR });
