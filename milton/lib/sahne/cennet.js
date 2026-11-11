// Cennet seti (CEN), açık tarif v2 (yönetmen kararı): beyaz figür KOYU KÜTLENİN önünde.
//  - Gök: eş merkezli halka yok. Işık merkezinin çevresi geniş temiz kâğıt; dışa doğru seyrek ışınsal tarama (üslup 10).
//    Gök tonu .6'nın altına inmez. Işık kaması en çok iki. Tanrı ve Oğul yalnız ışıktır (yüz, el, hale, haç yok).
//  - Koyu kütleler cehennemdeki dille: düz siyah + ışık yanında kenar hilali + içe giren beyaz vuruşlar; biçimleri sakin ve mimari
//    (yatay bulut bankları, basamaklı teraslar, uzak Dor sütun sıraları).
//  - Açık figür: düz kâğıt beyazı siluet (SF plain), iç ayrıntı birkaç mürekkep vuruşu; kanat beyaz kütle (cen_kanat).
//  - Saflar: tek tek figür dizisi değil, beyaz kütle (baş ve omuz yumrularından düzensiz üst kenar) + seyrek mızrak.
// Bütün işlevler açık levhaya çizer (GR.begin/engrave çağırmaz). Dünya koordinatı 1920×1080.
'use strict';

// ── gök ──
// L: {x, y}; o: {r0 (temiz kâğıt yarıçapı), r1 (en koyu tona varılan uzaklık), v (en koyu ton ≥ .6), n (ışın sayısı), ph, kama: [{a, w, len}] (≤ 2)}
function cen_gok(L, o = {}) {
  const { tx, px, tone } = GR, r0 = o.r0 ?? 300, r1 = o.r1 ?? 1500, v = Math.max(.6, o.v ?? .72);
  const g = tx.createRadialGradient(L.x, L.y, r0 * .7, L.x, L.y, Math.max(r0 + 10, r1));
  g.addColorStop(0, tone(1)); g.addColorStop(.2, tone(.97)); g.addColorStop(.55, tone(lerp(.97, v, .7))); g.addColorStop(1, tone(v));
  tx.fillStyle = g; tx.fillRect(-1600, -1600, W + 3200, H + 3200);
  px.fillStyle = GR.hatch({ type: 'ray', cx: L.x, cy: L.y, n: o.n ?? 96, id: 10, w: 3, ph: o.ph || 0 }); px.fillRect(-1600, -1600, W + 3200, H + 3200);
  if (o.kama) {
    tx.save(); tx.globalCompositeOperation = 'lighten'; tx.fillStyle = tone(1);
    for (const K of o.kama.slice(0, 2)) {
      const n = 14, A = [], B = [], at = K.at ?? .35;
      for (let i = 0; i <= n; i++) { const u = i / n, r = 30 + K.len * u, wv = K.w * (u < at ? Math.pow(u / at, .6) : Math.pow(1 - (u - at) / (1 - at), 1.4));
        A.push([L.x + Math.cos(K.a - wv) * r, L.y + Math.sin(K.a - wv) * r]); B.push([L.x + Math.cos(K.a + wv) * r, L.y + Math.sin(K.a + wv) * r]); }
      const P = new Path2D(); poly(P, [[L.x, L.y], ...A, ...B.reverse()], true); tx.fill(P);
    }
    tx.restore();
  }
}

// Sivri vuruş: pts boyunca, kalından inceye; tarama yaması vuruş doğrultusunda (ince uç kesik kesik basılmaz). v: ton
function cen_vurus(pts, w0, v = .02) {
  const { tx, px, tone } = GR, n = pts.length - 1, A = [], B = [];
  for (let i = 0; i <= n; i++) { const a = pts[Math.max(0, i - 1)], b = pts[Math.min(n, i + 1)], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, hw = Math.max(1.2, w0 * .5 * Math.pow(1 - i / n, 1.1));
    A.push([pts[i][0] - dy / l * hw, pts[i][1] + dx / l * hw]); B.push([pts[i][0] + dy / l * hw, pts[i][1] - dx / l * hw]); }
  const P = new Path2D(); poly(P, [...A, ...B.reverse()], true);
  tx.fillStyle = tone(v); tx.fill(P); px.fillStyle = GR.hatch({ th: Math.atan2(pts[n][1] - pts[0][1], pts[n][0] - pts[0][0]), id: 0 }); px.fill(P);
}
// ── koyu bulut bankı / teras ──
// Yatay, sakin üst kenar (birkaç geniş, alçak kabarım); düz siyah gövde; üst kenarda ışığa bakan yerde ince kâğıt hilal,
// kenardan içeri giren, sivrilen, düzensiz beyaz vuruşlar.
// o: {x0, x1, y (üst kenar ortalaması), amp (kabarım yüksekliği), wl (kabarım dalga boyu), yb (alt kenar; yoksa kadraj altı), seed, L,
//     cuts (vuruş yoğunluğu 0..1), rim (0..1), ends (uçlar yuvarlak kapanır: true), v (gövde tonu; .02), drift}
function cen_bank(o) {
  const { tx, px, tone } = GR, q = rng(o.seed || 1), L = o.L || { x: W / 2, y: -300 };
  const x0 = o.x0, x1 = o.x1, amp = o.amp ?? 26, wl = o.wl ?? 260, yb = o.yb ?? H + 400, dr = o.drift || 0;
  const ph1 = q() * TAU, ph2 = q() * TAU, ph3 = q() * TAU, step = 14, top = [];
  for (let x = x0; x <= x1 + .1; x += step) {
    const u = (x - x0) / Math.max(1, x1 - x0);
    // kabarımlar: yuvarlak tepeler (|sin|) — blob değil, geniş ve alçak
    let y = o.y - amp * (.55 * Math.abs(Math.sin((x + dr) / wl * PI + ph1)) + .3 * Math.abs(Math.sin((x + dr) / (wl * .53) * PI + ph2)) + .15 * Math.sin((x + dr) / (wl * 2.1) * PI + ph3));
    if (o.ends !== false) { const e = Math.min(u, 1 - u) * (x1 - x0) / (o.endW ?? 280); if (e < 1) y += Math.pow(1 - e, 2.2) * (o.endD ?? 380); }
    top.push([x, y]);
  }
  const P = new Path2D(); P.moveTo(x0, yb); for (const p of top) P.lineTo(p[0], p[1]); P.lineTo(x1, yb); P.closePath();
  tx.fillStyle = tone(o.v ?? .02); tx.fill(P); px.fillStyle = GR.hatch({ th: PI / 2, id: 0 }); px.fill(P);
  // kenar hilali: üst kenarın ışığa bakan yerlerinde, kalınlığı açıyla değişen ince kâğıt şerit
  const rim = o.rim ?? 0;
  if (rim > 0) {
    tx.save(); tx.clip(P); tx.fillStyle = tone(.97);
    let seg = [];
    const flush = () => { if (seg.length > 3) { const A = seg.map(s => s[0]), B = seg.map(s => s[1]).reverse(); tx.beginPath(); poly(tx, [...A, ...B], true); tx.fill(); } seg = []; };
    for (let i = 1; i < top.length - 1; i++) {
      const a = top[i - 1], b = top[i + 1], dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1, nx = dy / l, ny = -dx / l;   // dışa (yukarı) normal
      let lx = L.x - top[i][0], ly = L.y - top[i][1]; { const m = Math.hypot(lx, ly) || 1; lx /= m; ly /= m; }
      const f = nx * lx + ny * ly, wv = 7.5 * rim * Math.pow(Math.max(0, f), .8) * (.75 + .5 * noise1(i * .21, o.seed || 1));
      if (wv < 2.2) { flush(); continue; }
      seg.push([[top[i][0] + nx * 2, top[i][1] + ny * 2], [top[i][0] - nx * wv, top[i][1] - ny * wv]]);
    }
    flush(); tx.restore();
  }
  // içe giren beyaz vuruşlar
  const ck = o.cuts ?? 1;
  if (ck > 0) {
    const pts = top.filter((_, i) => i % 3 === 0), mx = pts.map(p => [p[0], p[1] + 9]);
    PR.cuts(mx, [L.x > (x0 + x1) / 2 ? -.25 : .25, 1], { len: [20, 50 + 130 * ck], gap: [50, 160 / Math.max(.4, ck)], w: 7, v: .97, seed: (o.seed || 1) + 7, clip: P, bend: .3 * (L.x > (x0 + x1) / 2 ? -1 : 1) });
  }
  return { path: P, top, yAt: x => { const i = clamp(Math.round((x - x0) / step), 0, top.length - 1); return top[i][1]; } };
}

// ── açık teras: kâğıt üst yüz, koyu ön yüz (basamak). Gölge düşebilen zemin. ──
// o: {x0, x1, y (üst yüz arka kenarı), d (üst yüz derinliği), seed, L, ...cen_bank seçenekleri (ön yüz)}
function cen_teras(o) {
  const { tx, px, tone } = GR, q = rng((o.seed || 1) + 3), d = o.d ?? 40, P = new Path2D(), top = [];
  for (let x = o.x0; x <= o.x1 + .1; x += 20) top.push([x, o.y + Math.sin(x * .006 + q() * .2 + (o.seed || 1)) * 5]);
  P.moveTo(o.x0, o.y + d + 30); for (const p of top) P.lineTo(p[0], p[1]); P.lineTo(o.x1, o.y + d + 30); P.closePath();
  tx.fillStyle = tone(.985); tx.fill(P); px.fillStyle = GR.hatch({ th: 0, id: 10 }); px.fill(P);
  return cen_bank(Object.assign({}, o, { y: o.y + d, amp: o.amp ?? 8, wl: o.wl ?? 340, rim: o.rim ?? 0, ends: o.ends ?? false, cuts: o.cuts ?? .5 }));
}

// ── uzak Dor sütun sırası (koyu kütle) ──
// x0..x1, y taban, h sütun boyu; ışık yanında ince kâğıt kenar; üstte düz arşitrav
function cen_sutunlar(o) {
  const { tx, px, tone } = GR, n = o.n || Math.round((o.x1 - o.x0) / (o.h * .32)), L = o.L || { x: W / 2, y: -300 }, w = o.h * .11, P = new Path2D(), R = new Path2D();
  P.rect(o.x0 - w, o.y - o.h - o.h * .1, o.x1 - o.x0 + 2 * w, o.h * .1);
  for (let i = 0; i <= n; i++) { const x = lerp(o.x0, o.x1, i / n), sd = L.x > x ? 1 : -1; P.rect(x - w / 2, o.y - o.h, w, o.h); R.rect(sd > 0 ? x + w / 2 - 3 : x - w / 2, o.y - o.h, 3, o.h * .9); }
  P.rect(o.x0 - w * 1.4, o.y - o.h * .04, o.x1 - o.x0 + w * 2.8, o.h * .06);
  tx.fillStyle = tone(.03); tx.fill(P); px.fillStyle = GR.hatch({ th: 0, id: 0 }); px.fill(P);
  if (o.h > 120) { tx.fillStyle = tone(.95); tx.fill(R); }
}

// ── beyaz kanat ──
// Kök (rx, ry), side ±1 (dışa açıldığı yön), S boy; lift 0 yatay … 1 dik; open 0 kapalı (aşağı sarkık) … 1 açık; seed.
// Kâğıt beyazı kütle; birincil tüy uçları arka kenarda düzensiz dişler; gölge yanında arka kenardan içe giren 4–6 mürekkep vuruşu; kökte küçük koyu çapa.
function cen_kanat(rx, ry, side, S, o = {}) {
  const { tx, px, tone } = GR, q = rng((o.seed || 1) * 97 + 3), K = cen_kanat._yol(rx, ry, side, S, o), { P, trail, ax, nd, W2, th } = K;
  tx.fillStyle = tone(.985); tx.fill(P); px.fillStyle = GR.hatch({ th: th * side, id: 6 }); px.fill(P);
  // gölge yanı vuruşları: arka kenar çentiklerinden kanadın içine (öne kenara doğru), sivrilen
  GR.save(); tx.clip(P); px.clip(P); tx.fillStyle = tone(.02);
  for (let k = 0; k < (o.strokes ?? 5); k++) {
    const p0 = trail[Math.floor(q() * trail.length)], len = S * (.1 + q() * .18), bend = (q() - .5) * .25, pts = [];
    for (let j = 0; j <= 8; j++) { const u = j / 8; pts.push(W2(p0[0] - nd[0] * len * u + ax[0] * bend * len * u * u + ax[0] * 2, p0[1] - nd[1] * len * u + ax[1] * bend * len * u * u)); }
    cen_vurus(pts, Math.max(4, S * .014));
  }
  // kök çapası: kanadın gövdeye bağlandığı alt köşede küçük koyu kama
  if ((o.anchor ?? 0) > 0) { const C = [[0, S * .02], [S * .16 * ax[0] + nd[0] * S * .1, S * .16 * ax[1] + nd[1] * S * .1], [nd[0] * S * .2, S * .14]].map(p => W2(p[0], p[1])); tx.beginPath(); spline(tx, C, true, .5); tx.fill(); }
  GR.restore();
  return P;
}

// ── başmelek / açık figür ──
// p: {x, y (kalça), h, facing, L, t, head, twist, lean, armN, armF, legN, legF, legs, cloak, spear ({grip, ang, len, up} | false), wing (false), wingS (boy, h), lift, open,
//     dark (true: koyu siluet sürümü; A02 için), robe}
function cen_basmelek(p) {
  const h = p.h, t = p.t || 0;
  const J = SF.rig({ x: p.x, y: p.y, h, facing: p.facing ?? 1, twist: p.twist ?? .3, lean: p.lean ?? 0, head: p.head ?? .15, shTilt: p.shTilt ?? -.03,
    armN: p.armN || [-.1, .3], armF: p.armF || [.45, .8], legN: p.legN || [.1, -.05], legF: p.legF || [-.08, -.02] });
  let lx = p.L.x - J.shC[0], ly = p.L.y - J.shC[1]; { const l = Math.hypot(lx, ly) || 1; lx /= l; ly /= l; }
  const LIT = p.lit || [lx, ly], dk = !!p.dark;
  if (p.wing !== false) {
    const S = (p.wingS ?? 5.2) * h, f = J.f;
    // arka kanat (bakış yönünde, gövdenin arkasında) önce, yakın kanat sonra; ikisi de gövdenin arkasında
    for (const side of [f, -f]) {
      const sh = side === f ? [J.shC[0] - side * h * .2, J.shC[1]] : J.shN, rx = sh[0] - side * h * .1, ry = sh[1] + h * .25;
      if (dk) { cen_kanatKoyu(rx, ry, side, S * (side === f ? .95 : 1), { lift: (p.lift ?? .55) + (side === f ? .08 : 0), open: p.open ?? .8, seed: side > 0 ? 12 : 11, t, L: p.L }); }
      else cen_kanat(rx, ry, side, S * (side === f ? .95 : 1), { lift: (p.lift ?? .55) + (side === f ? .08 : 0), open: p.open ?? .8, seed: side > 0 ? 12 : 11, t, strokes: p.wStrokes ?? 5 });
    }
  }
  if (p.mid) p.mid(J);
  const so = dk ? { lum: 0, lit: LIT, t, cloak: p.cloak ?? .55, legs: p.legs ?? true, skirt: true, lines: 2, eye: 1, wind: .5, seed: p.seed || 3, halo: 3, robe: p.robe }
    : { lum: 1, plain: true, armor: false, lit: LIT, t, cloak: p.cloak ?? false, legs: p.legs ?? true, skirt: true, lines: p.lines ?? 0, eye: 0, wind: .5, seed: p.seed || 3, robe: p.robe, hair: p.hair };
  const sp = p.spear === false ? null : Object.assign({ grip: 'F', ang: .03, len: 7.8, up: .66 }, p.spear || {});
  const spear = () => { const g = J['wr' + sp.grip], a = (sp.ang || 0) * J.f; cen_mizrak(g[0] + J.f * h * .2, g[1] + h * .08, a, sp.len * h, sp.up, Math.max(1.8, h * .05), h, dk ? 0 : (p.spV ?? 1)); };
  if (sp && sp.grip === 'F') spear();
  SF.draw(J, so);
  if (sp && sp.grip !== 'F') spear();
  return J;
}
// Koyu kanat (A02 başı/sonu: Nifates silueti): aynı biçim, düz siyah; ışık yanında ince kâğıt kenar
function cen_kanatKoyu(rx, ry, side, S, o) {
  const { tx, px, tone } = GR, { P } = cen_kanat._yol(rx, ry, side, S, o), L = o.L || { x: W / 2, y: 0 };
  let lx = L.x - rx, ly = L.y - ry; { const l = Math.hypot(lx, ly) || 1; lx /= l; ly /= l; }
  tx.save(); tx.translate(lx * 3.5, ly * 3.5); tx.fillStyle = tone(.95); tx.fill(P); tx.restore();
  tx.fillStyle = tone(.02); tx.fill(P); px.fillStyle = GR.hatch({ th: 0, id: 0 }); px.fill(P);
}
// kanat yolu (çizmeden): cen_kanat ile aynı geometri
cen_kanat._yol = (rx, ry, side, S, o = {}) => {
  // ekseni kökten uca hafif yukarı kavisli uzun damla; ön kenar ince, arka kenar geniş (kökte), uca doğru sivrilir; arka kenarda uca doğru eğik küçük tüy dişleri
  const lift = o.lift ?? .55, op = o.open ?? .8, t = o.t || 0;
  const th = -lerp(.1, 1.15, lift) + (1 - op) * 1.3 + Math.sin(t * .6 + (o.seed || 1)) * .012;
  const W2 = (x, y) => [rx + side * x, ry + y], ax = [Math.cos(th), Math.sin(th)], nd = [-ax[1], ax[0]];
  const c = u => [ax[0] * S * u - nd[0] * S * .13 * Math.sin(PI * u), ax[1] * S * u - nd[1] * S * .13 * Math.sin(PI * u)];
  const wl = u => S * .045 * Math.pow(Math.sin(PI * Math.min(1, u * 1.1)), .6) + S * .03 * (1 - u);
  const wt = u => S * (.16 + .26 * Math.sin(PI * Math.min(1, u * 1.35))) * Math.pow(1 - u, .55) * (.6 + .4 * op);
  const n = 30, lead = [], trail = [], q = rng((o.seed || 1) * 31 + 1), nt = 9;
  for (let i = 0; i <= n; i++) { const u = i / n, p = c(u), w = wl(u); lead.push([p[0] - nd[0] * w, p[1] - nd[1] * w]); }
  for (let i = n; i >= 0; i--) {
    const u = i / n, p = c(u), w = wt(u), ph = (u * nt) % 1, tooth = S * .03 * (1 - Math.abs(ph - .5) * 2) * Math.min(1, u * 4) * (1 - u * .4);
    trail.push([p[0] + nd[0] * (w + tooth) + ax[0] * tooth * .9, p[1] + nd[1] * (w + tooth) + ax[1] * tooth * .9]);
  }
  const P = new Path2D(); poly(P, [...lead, ...trail].map(p => W2(p[0], p[1])), true);
  // vuruş çapaları: diş dipleri (arka kenar)
  const nts = []; for (let k = 1; k < nt; k++) { const u = k / nt, p = c(u), w = wt(u); nts.push([p[0] + nd[0] * w, p[1] + nd[1] * w]); }
  return { P, trail: nts, ax, nd, W2, th };
};

// Mızrak: düz sap, yaprak biçimli demir. v: 0 mürekkep (açık figürde), 1 kâğıt (koyu zemin önünde, uzak saflarda)
function cen_mizrak(gx, gy, a, L, up, w, h, v = 0) {
  const { tx, px, tone } = GR, c = Math.sin(a), s = -Math.cos(a), n = [-s, c], tl = h * .8;
  const b0 = [gx - c * L * (1 - up), gy - s * L * (1 - up)], t0 = [gx + c * L * up, gy + s * L * up];
  const SP = new Path2D(); poly(SP, [[b0[0] + n[0] * w, b0[1] + n[1] * w], [t0[0] + n[0] * w, t0[1] + n[1] * w], [t0[0] + n[0] * w * 2.4 + c * tl * .3, t0[1] + n[1] * w * 2.4 + s * tl * .3], [t0[0] + c * tl, t0[1] + s * tl],
    [t0[0] - n[0] * w * 2.4 + c * tl * .3, t0[1] - n[1] * w * 2.4 + s * tl * .3], [t0[0] - n[0] * w, t0[1] - n[1] * w], [b0[0] - n[0] * w, b0[1] - n[1] * w]], true);
  if (v) { tx.save(); tx.lineWidth = 3; tx.strokeStyle = tone(0); tx.stroke(SP); tx.restore(); }
  tx.fillStyle = tone(v ? .98 : 0); tx.fill(SP); px.fillStyle = GR.hatch({ th: a - PI / 2, id: 7 }); px.fill(SP);
}

// ── saf kütlesi: beyaz (koyu zemin önünde) ya da koyu (açık zemin önünde) ──
// Baş ve omuz yumrularından düzensiz üst kenar, altı birleşik; sırtta yer yer kapalı kanat ucu; seyrek mızrak (sayısı nSp).
// o: {x0, x1, y (ayak çizgisi; alt kenar bunun altına iner), h (baş boyu), seed, v (.985 beyaz | .03 koyu), nSp (8–14), spAng (i, x) → açı, spV (mızrak tonu),
//     bow (0..1: başlar öne eğik, omuzlar alçak), folds (beyaz kütlede alttan giren vuruş sayısı oranı)}
function cen_safKutle(o) {
  const { tx, px, tone } = GR, q = rng(o.seed || 1), h = o.h, P = new Path2D(), heads = [];
  const bw = o.bow || 0, yb = o.yb ?? (o.y + h * 3);
  let x = o.x0 - h * q();
  while (x < o.x1 + h) {
    const hh = h * (.9 + q() * .22), top = o.y - 7.1 * hh * (1 - .28 * bw) + (q() - .5) * hh * .6, f = q() < .5 ? 1 : -1;
    const st = q() < .5 ? 0 : hh * (.5 + q() * .7);
    heads.push({ x: x + bw * hh * .5 * f, y: top + st + .62 * hh + bw * hh * .7, r: .34 * hh, sh: top + st + 1.05 * hh + bw * hh * .5, w: .9 * hh, wing: q() < .3, f, hh });
    x += hh * (.8 + q() * 1.0);
  }
  // gövde: omuz hattından aşağı birleşik
  const sh = [[o.x0 - h * 2, yb]];
  for (const H of heads) { sh.push([H.x - H.w, H.sh + H.hh * .25]); sh.push([H.x - H.w * .7, H.sh]); sh.push([H.x + H.w * .7, H.sh]); sh.push([H.x + H.w, H.sh + H.hh * .25]); }
  sh.push([o.x1 + h * 2, yb]);
  const B = new Path2D(); spline(B, sh, true, .35); P.addPath(B);
  for (const H of heads) { const C = new Path2D(); C.ellipse(H.x, H.y, H.r, H.r * 1.22, bw * .5 * H.f, 0, TAU); P.addPath(C);
    if (H.wing) { const Wg = new Path2D(); const bx = H.x - H.f * H.w * .8; poly(Wg, [[bx - H.f * H.hh * .1, H.sh + H.hh], [bx - H.f * H.hh * .55, H.sh - H.hh * 1.5], [bx + H.f * H.hh * .35, H.sh + H.hh * .2]], true); P.addPath(Wg); } }
  const v = o.v ?? .985, light = v > .5;
  tx.fillStyle = tone(v); tx.fill(P); px.fillStyle = GR.hatch({ th: PI / 2, id: 10 }); px.fill(P);
  // beyaz kütlede: aralarda alttan giren sivri mürekkep vuruşları (bedenleri ayırır), seyrek
  if (light && h > 7) {
    GR.save(); tx.clip(P); px.clip(P);
    heads.forEach((H, i) => { if (q() > (o.folds ?? .45)) return; const x0 = H.x + H.f * H.w * (.6 + q() * .4), L = (yb - H.sh) * (.4 + q() * .35), pts = [];
      for (let j = 0; j <= 8; j++) pts.push([x0 + (q() - .5) * .4, yb + 2 - L * j / 8]);
      cen_vurus(pts, Math.max(3.2, h * .2)); });
    GR.restore();
  }
  // mızraklar: seyrek, boyları farklı
  const nSp = o.nSp ?? 10;
  if (nSp > 0) { const idx = heads.map((_, i) => i).sort((a, b) => hash(a * 3.7 + (o.seed || 1)) - hash(b * 3.7 + (o.seed || 1))).slice(0, nSp);
    for (const i of idx) { const H = heads[i], a = (hash(i * 1.3 + (o.seed || 1)) - .5) * .1 + (o.spAng ? o.spAng(i, H.x) : 0), Ls = H.hh * (8 + 3.5 * hash(i * 5.1 + 2));
      cen_mizrak(H.x + H.f * H.w * .9, H.sh + H.hh * 1.3, a, Ls, .72, Math.max(1.5, H.hh * .07), H.hh, o.spV ?? (light ? 0 : 1)); } }
  return { path: P, heads };
}

// ── küçük melek (tek figür; C04 ön plan, C10–C11 kalabalık) ──
// p: {x, y (ayak), h, f, bow (0..1 saray selamı: tek diz, baş eğik), v (gövde tonu), spear (açı | null), wing, seed, ink (true: düz koyu siluet; ışık yanında ince kâğıt kenar)}
function cen_melekYol(p) {
  const h = p.h, f = p.f, b = clamp(p.bow || 0), q = rng(p.seed || 1);
  const wy = lerp(-4.3, -2.75, b), an = b * .62, ca = Math.cos(an), sa = Math.sin(an);
  const up = (x, y) => { const dy = y + 4.3; return [x * ca - dy * sa, wy + x * sa + dy * ca]; };
  const W2 = ([x, y]) => [p.x + x * f * h, p.y + y * h], j = () => (q() - .5) * .08;
  const LS = [[-.62, -4.3], [-.8, -2.6], [-1.0, -.6], [-1.06, 0], [-.5, .04], [0, -.03], [.5, .05], [.98, 0], [.9, -.8], [.68, -2.66], [.56, -4.3]];
  const LK = [[-.62, -2.75], [-.95, -1.7], [-1.5, -.5], [-1.8, 0], [-.9, .04], [0, -.02], [.9, .04], [1.35, 0], [1.42, -.9], [1.5, -1.85], [.56, -2.75]];
  const lo = LS.map((a, i) => [lerp(a[0], LK[i][0], b) + (i === 3 || i === 7 ? j() : 0), lerp(a[1], LK[i][1], b)]);
  const tp = [[.56, -4.3], [.74, -5.25], [.78, -5.95], [.25, -6.35], [-.25, -6.35], [-.82, -6.0], [-.86, -5.35], [-.62, -4.3]].map(([x, y]) => up(x, y));
  const P = new Path2D(); spline(P, [...lo, ...tp].map(W2), true, .55);
  const hd = up(.12 + .25 * b, -6.92 + .15 * b), hb = new Path2D(); hb.ellipse(...W2(hd), .37 * h, .47 * h, an * f * 1.2, 0, TAU); P.addPath(hb);
  const sh = up(.5, -5.95), el = up(.82, -4.75), hn = b > .3 ? up(.45, -5.25) : up(1.32, -4.5);
  const arm = new Path2D(), aw = .21; { const A = [], B = [], seg = [sh, el, hn];
    for (let i = 0; i < 3; i++) { const p0 = seg[Math.max(0, i - 1)], p1 = seg[Math.min(2, i + 1)], dx = p1[0] - p0[0], dy = p1[1] - p0[1], l = Math.hypot(dx, dy) || 1, w = aw * (i === 2 ? .8 : 1);
      A.push([seg[i][0] - dy / l * w, seg[i][1] + dx / l * w]); B.push([seg[i][0] + dy / l * w, seg[i][1] - dx / l * w]); }
    spline(arm, [...A, ...B.reverse()].map(W2), true, .5); }
  const wg = (p.wing ?? 1) * (1 - .75 * b); let Wp = null;
  const upW = (x, y) => { const dy = y + 4.3, c2 = Math.cos(an * .55), s2 = Math.sin(an * .55); return [x * c2 - dy * s2 - .3 * b, wy + x * s2 + dy * c2]; };
  if (p.wing !== 0) { Wp = new Path2D(); spline(Wp, [[-.55, -6.0], [-.9, -6.9 - .5 * wg], [-1.12, -7.6 - 1.0 * wg], [-1.5, -6.5], [-1.42, -4.6], [-1.12, -2.4], [-.92, -1.5], [-.8, -3.4], [-.66, -5.2]].map(([x, y]) => W2(upW(x, y))), true, .6); }
  return { P, arm, Wp, hd: W2(hd), hand: W2(hn), k: 1 - .36 * b };
}
function cen_melek(p) {
  const { tx, px, tone } = GR, h = p.h, Y = cen_melekYol(p), v = p.v ?? .985, light = v > .5;
  const all = new Path2D(); all.addPath(Y.P); all.addPath(Y.arm); if (Y.Wp) all.addPath(Y.Wp);
  if (light) {
    if (Y.Wp) { tx.fillStyle = tone(v); tx.fill(Y.Wp); px.fillStyle = GR.hatch({ th: -1.1 * p.f, id: 6 }); px.fill(Y.Wp); }
    tx.fillStyle = tone(v); tx.fill(Y.P); px.fillStyle = GR.hatch({ th: PI / 2, id: 10 }); px.fill(Y.P);
    // kanat ile beden, kol ile beden arasında ince ayırma: yalnız büyük boyda, kısa sivri vuruş
    if (h > 18) { tx.save(); tx.translate(-p.f * h * .06, 0); tx.fillStyle = tone(.03); tx.fill(Y.arm); tx.restore(); }
    tx.fillStyle = tone(v); tx.fill(Y.arm);
    if (h > 16) { const q = rng((p.seed || 1) * 7 + 3), nn = h > 30 ? 3 : 2;
      GR.save(); tx.clip(Y.P); px.clip(Y.P);
      for (let i = 0; i < nn; i++) { const fx = -(.62 - i * (.3 + .1 * q())), L0 = (1.4 + q() * 1.6) * h * Y.k, x0 = p.x + fx * p.f * h, bend = (q() - .5) * .3 * h, pts = [];
        for (let m = 0; m <= 8; m++) { const u = m / 8; pts.push([x0 + bend * u * u, p.y + 4 - L0 * u]); }
        cen_vurus(pts, Math.max(3.2, h * .09)); }
      GR.restore(); }
  } else {
    // koyu siluet: ışık yanında ince kâğıt kenar (kaydırılmış kâğıt kopya altta)
    if (p.lx != null && h > 10) { tx.save(); tx.translate(p.lx * 2.5, p.ly * 2.5); tx.fillStyle = tone(.9); tx.fill(all); tx.restore(); }
    tx.fillStyle = tone(v); tx.fill(all); px.fillStyle = GR.hatch({ th: PI / 2, id: 10 }); px.fill(all);
  }
  if (p.spear != null) cen_mizrak(Y.hand[0], Y.hand[1], p.spear, (p.sl ?? 7.5) * h, .7, Math.max(1.4, h * .055), h, light ? 0 : 1);
  return Y;
}

// Sabah yıldızı: sade sekiz kollu kâğıt beyazı ışık (koyu kütlenin önünde çizilir). r: uzun kol boyu; a: 0..1 parlama
function cen_yildiz(x, y, r, a = 1) {
  const { tx, tone } = GR; if (a <= 0) return;
  const S = new Path2D(), pts = [];
  for (let i = 0; i < 16; i++) { const an = i / 16 * TAU - PI / 2, rr = i % 2 ? r * .1 : (i % 4 === 0 ? r * (.55 + .45 * a) : r * .42 * (.6 + .4 * a)); pts.push([x + Math.cos(an) * rr, y + Math.sin(an) * rr]); }
  poly(S, pts, true); tx.fillStyle = tone(1); tx.fill(S);
}
// İkinci ışık (Oğul): figürsüz temiz kâğıt disk ve parıltı. Yüz, el, hale, haç yok.
function cen_isik(x, y, r, a = 1) {
  const { tx, tone } = GR; if (a <= 0) return;
  PR.glow(x, y, r, r * 2.6, 1, a * .8);
  const C = new Path2D(); C.arc(x, y, r, 0, TAU); tx.fillStyle = tone(1); tx.fill(C);
}
// Uzak saray: Dor sütunlu, alınlıklı tapınak (kubbe yok). Koyu kütle; ışık yanında kâğıt kenar. x, y taban ortası; s taban genişliği
function cen_saray(x, y, s, lx = 1) {
  const { tx, px, tone } = GR, u = s / 10, B = new Path2D(), R = new Path2D();
  B.rect(x - 5 * u, y - .6 * u, 10 * u, .6 * u); B.rect(x - 4.6 * u, y - 1 * u, 9.2 * u, .4 * u);
  B.rect(x - 4.3 * u, y - 5.4 * u, 8.6 * u, .8 * u);
  B.moveTo(x - 4.7 * u, y - 5.4 * u); B.lineTo(x, y - 7.3 * u); B.lineTo(x + 4.7 * u, y - 5.4 * u); B.closePath();
  for (let i = 0; i < 6; i++) { const cx = x - 3.8 * u + i * 1.52 * u; B.rect(cx - .32 * u, y - 4.6 * u, .64 * u, 3.6 * u); R.rect(cx + lx * .32 * u - (lx > 0 ? .18 * u : 0), y - 4.5 * u, .18 * u, 3.4 * u); }
  R.moveTo(x, y - 7.3 * u); R.lineTo(x + lx * 4.7 * u, y - 5.4 * u); R.lineTo(x + lx * 4.4 * u, y - 5.4 * u); R.lineTo(x, y - 7.0 * u); R.closePath();
  tx.fillStyle = tone(.03); tx.fill(B); px.fillStyle = GR.hatch({ th: 0, id: 0 }); px.fill(B);
  tx.fillStyle = tone(.95); tx.fill(R);
}
// Açık levhada yazı: panel yok; mürekkep harf (temiz kâğıt bölgeye) ya da kâğıt harf (koyu kütle üstüne). col: INK_CSS | PAPER_CSS
function cen_yazi(ctx, s, x, y, a, o = {}) {
  if (NOTEXT || !s || a <= 0) return;
  txt(ctx, s, x, y, { px: o.px || 56, font: o.font || FONT.baslik(o.px || 56, 600), ls: o.ls ?? 6, a, col: o.col || INK_CSS });
}

// ── kaba eskiz uyumu: cizCennet(t, o) = C02 levhası ──
function cizCennet(t, o = {}) { return cen_c02(t, o); }
function sahneCennet(t, o = {}) { GR.begin(.9, 0, 1, o.cam); cizCennet(t, o); GR.engrave(o.out || ctx); applyPaper(o.out || ctx, .8); applyVignette(o.out || ctx, .25); }
