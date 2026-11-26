// Dekor (Stanford 1971): bodrum koridoru, hücre kapıları, gözlem masası, makaralı teyp, monitör, belge. ORTAK DOSYA: yalnız başkan değiştirir.
// Hepsi EKRAN (BASKI) plakalarına çizer: B.k ton, B.l çizgi, B.c renk (yalnız teyp ışığı, kayıt lambası ve belge mürekkebi).
// Hassasiyet: hücre parmaklıkları dikey (yatay kuşakla haç olmasın: kuşak iki tane ve kapı kenarına kadar); sıra hâlinde eğilen figür yok;
//   koridor tavanındaki lambalar uzun dikdörtgen floresan (kandil değil); işaret levhası İngilizce özgün adıyla (STANFORD COUNTY JAIL).
'use strict';
const D = (() => {
  const T = (B, d) => B.ton(d);
  const ink = (g, w = 2, c = '#000') => { g.strokeStyle = c; g.fillStyle = c; g.lineWidth = w; g.lineCap = 'round'; g.lineJoin = 'round'; };
  // ── bodrum koridoru (gözlem kamerasının yerinden: koridorun ucundan, hafif yüksekten) ──
  // o.vp [x,y] kaçış noktası · o.gen yarı genişlik (önde) · o.tavan / o.zemin önde y · o.isik floresan parlaklığı (0..1) · o.kapilar kapı sayısı her yanda
  // dönüş: { yer(z, u) → [x,y] (z 0 önde → 1 uzakta, u -1 sol duvar → 1 sağ duvar, zemin hizası), olc(z) ölçek, kapi(i, yan) → kapı ortası }
  function koridor(B, t, o = {}) {
    const k = B.k, l = B.l, vp = o.vp || [960, 470], gen = o.gen ?? 760, ty = o.tavan ?? -40, zy = o.zemin ?? 1120;
    const zMax = .86;
    const P = (z, u, h) => { const f = 1 - z; const x = vp[0] + u * gen * f, yz = vp[1] + (zy - vp[1]) * f, yt = vp[1] + (ty - vp[1]) * f; return [x, lerp(yz, yt, h)]; };
    // duvarlar, tavan, zemin (ton)
    const quad = (g, a, b, c, d, fill) => { g.fillStyle = fill; g.beginPath(); g.moveTo(...a); g.lineTo(...b); g.lineTo(...c); g.lineTo(...d); g.closePath(); g.fill(); };
    k.save();
    quad(k, P(0, -1, 0), P(zMax, -1, 0), P(zMax, -1, 1), P(0, -1, 1), T(B, o.solD ?? .42));
    quad(k, P(0, 1, 0), P(zMax, 1, 0), P(zMax, 1, 1), P(0, 1, 1), T(B, o.sagD ?? .48));
    quad(k, P(0, -1, 1), P(zMax, -1, 1), P(zMax, 1, 1), P(0, 1, 1), T(B, .62));
    quad(k, P(0, -1, 0), P(zMax, -1, 0), P(zMax, 1, 0), P(0, 1, 0), T(B, .3));
    quad(k, P(zMax, -1, 0), P(zMax, 1, 0), P(zMax, 1, 1), P(zMax, -1, 1), T(B, o.sonD ?? .7));   // koridorun ucu (karanlık)
    // zemin karoları (derinlik çizgileri)
    k.strokeStyle = T(B, .4); k.lineWidth = 2;
    for (let i = 1; i < 12; i++) { const z = 1 - Math.pow(1 - zMax, i / 12); k.beginPath(); k.moveTo(...P(z, -1, 0)); k.lineTo(...P(z, 1, 0)); k.stroke(); }
    for (let u = -.6; u <= .61; u += .4) { k.beginPath(); k.moveTo(...P(0, u, 0)); k.lineTo(...P(zMax, u, 0)); k.stroke(); }
    // duvar alt şeridi (süpürgelik)
    for (const s of [-1, 1]) quad(k, P(0, s, 0), P(zMax, s, 0), P(zMax, s, .1), P(0, s, .1), T(B, .62));
    k.restore();
    // floresan lambalar (tavanda iki sıra, uzun dikdörtgen); titreme o.isik
    const isik = o.isik ?? 1;
    for (let i = 0; i < 5; i++) {
      const z0 = .08 + i * .16, z1 = z0 + .06;
      for (const u of [-.35, .35]) {
        const a = P(z0, u - .07, 1), b = P(z1, u - .07, 1), c = P(z1, u + .07, 1), d = P(z0, u + .07, 1);
        k.save(); quad(k, a, b, c, d, T(B, .02 + (1 - isik) * .5)); k.restore();
      }
    }
    // kapılar
    const nK = o.kapilar ?? 3, kapiZ = i => .12 + i * (.62 / Math.max(1, nK - 1)) * (nK > 1 ? 1 : 0);
    const kapilar = [];
    for (const yan of [-1, 1]) for (let i = 0; i < nK; i++) {
      if (o.kapiYok && o.kapiYok.includes(`${yan > 0 ? 'R' : 'L'}${i}`)) continue;
      const z0 = kapiZ(i), z1 = z0 + .07;
      const a = P(z0, yan, 0), b = P(z1, yan, 0), c = P(z1, yan, .72), d = P(z0, yan, .72);
      kapilar.push({ yan, i, a, b, c, d });
      hucreKapisi(B, a, b, c, d, { no: o.no ? o.no(yan, i) : null, acik: o.acik && o.acik(yan, i) });
    }
    // levha
    if (o.levha !== false) {
      const a = P(.45, -1, .86), b = P(.6, -1, .86), c = P(.6, -1, .78), d = P(.45, -1, .78);
      k.save(); quad(k, a, b, c, d, T(B, .05)); k.restore();
      l.save(); ink(l, 2); l.beginPath(); l.moveTo(...a); l.lineTo(...b); l.lineTo(...c); l.lineTo(...d); l.closePath(); l.stroke();
      // levha yazısı perspektifte: yatay sıkıştırma
      const cx = (a[0] + b[0]) / 2, cy = (a[1] + d[1]) / 2, w = Math.abs(b[0] - a[0]), h = Math.abs(d[1] - a[1]);
      l.translate(cx, cy); l.transform(1, (b[1] - a[1]) / (b[0] - a[0]), 0, 1, 0, 0); l.font = `700 ${h * .5}px "Courier Prime"`; l.textAlign = 'center'; l.textBaseline = 'middle';
      l.save(); l.scale(Math.min(1, w / (h * 6.4)), 1); l.fillText('STANFORD COUNTY JAIL', 0, 0); l.restore(); l.restore();
    }
    return { yer: (z, u) => P(z, u, 0), olc: z => 1 - z, P, kapilar };
  }
  // hücre kapısı: dörtgen (perspektifli), dikey parmaklıklar, iki yatay kuşak (kapı kenarından kenarına), numara levhası
  function hucreKapisi(B, a, b, c, d, o = {}) {
    const k = B.k, l = B.l;
    k.save(); k.fillStyle = T(B, o.acik ? .9 : .82); k.beginPath(); k.moveTo(...a); k.lineTo(...b); k.lineTo(...c); k.lineTo(...d); k.closePath(); k.fill(); k.restore();
    l.save(); const w = Math.max(1.5, Math.abs(b[0] - a[0]) * .05); ink(l, w * 1.6);
    l.beginPath(); l.moveTo(...a); l.lineTo(...b); l.lineTo(...c); l.lineTo(...d); l.closePath(); l.stroke();
    if (!o.acik) {
      l.lineWidth = w;
      for (let i = 1; i < 7; i++) { const u = i / 7, p = [lerp(a[0], b[0], u), lerp(a[1], b[1], u)], q = [lerp(d[0], c[0], u), lerp(d[1], c[1], u)]; l.beginPath(); l.moveTo(...p); l.lineTo(...q); l.stroke(); }
      for (const v of [.3, .7]) { const p = [lerp(a[0], d[0], v), lerp(a[1], d[1], v)], q = [lerp(b[0], c[0], v), lerp(b[1], c[1], v)]; l.lineWidth = w * 1.3; l.beginPath(); l.moveTo(...p); l.lineTo(...q); l.stroke(); }
    }
    l.restore();
  }
  // makaralı teyp (önden): gövde, iki makara (dönüyor: ang), bant, kehribar VU göstergesi, kırmızı kayıt lambası. (x,y) gövdenin orta-üstü, s ölçek
  function teyp(B, x, y, s, ang, o = {}) {
    const k = B.k, l = B.l, w = 520 * s, h = 360 * s;
    k.save(); k.fillStyle = T(B, .78); k.fillRect(x - w / 2, y, w, h); k.fillStyle = T(B, .6); k.fillRect(x - w / 2 + 16 * s, y + 16 * s, w - 32 * s, h * .62); k.restore();
    l.save(); ink(l, 3 * s); l.strokeRect(x - w / 2, y, w, h); l.restore();
    const mr = 98 * s, my = y + 125 * s;
    for (const sx of [-1, 1]) {
      const mx = x + sx * 128 * s, dolu = sx < 0 ? (o.sol ?? .8) : (o.sag ?? .4);
      k.save(); k.fillStyle = T(B, .95); k.beginPath(); k.arc(mx, my, mr * (.45 + .5 * dolu), 0, TAU); k.fill(); k.restore();   // sarılı bant
      l.save(); ink(l, 3 * s); l.beginPath(); l.arc(mx, my, mr, 0, TAU); l.stroke();
      l.translate(mx, my); l.rotate(ang * (sx < 0 ? 1 : 1.25));
      for (let i = 0; i < 3; i++) { l.rotate(TAU / 3); l.beginPath(); l.ellipse(0, -mr * .62, mr * .16, mr * .26, 0, 0, TAU); l.fillStyle = '#fff'; l.fill(); l.stroke(); }
      l.beginPath(); l.arc(0, 0, mr * .12, 0, TAU); l.fillStyle = '#000'; l.fill(); l.restore();
    }
    // bant yolu (iki makara arasında, kafaların üstünden)
    l.save(); ink(l, 2.2 * s); l.beginPath(); l.moveTo(x - 128 * s, my + mr * .8); l.lineTo(x - 30 * s, y + 236 * s); l.lineTo(x + 30 * s, y + 236 * s); l.lineTo(x + 128 * s, my + mr * .6); l.stroke(); l.restore();
    // VU göstergesi (kehribar) ve kayıt lambası (kırmızı)
    const vx = x - 120 * s, vy = y + 270 * s, vw = 150 * s, vh = 70 * s;
    B.renkBoya(g => g.rect(vx, vy, vw, vh), o.vuIsik ?? .85, 0);
    l.save(); ink(l, 2 * s); l.strokeRect(vx, vy, vw, vh); const ia = -PI / 2 + lerp(-.9, .7, clamp(o.vu ?? .3)); l.beginPath(); l.moveTo(vx + vw / 2, vy + vh - 6 * s); l.lineTo(vx + vw / 2 + Math.cos(ia) * vh * .8, vy + vh - 6 * s + Math.sin(ia) * vh * .8); l.stroke(); l.restore();
    const rx = x + 150 * s, ry = y + 305 * s;
    if (o.kayit) B.renkBoya(g => g.arc(rx, ry, 16 * s, 0, TAU), o.kayit, 1);
    l.save(); ink(l, 2 * s); l.beginPath(); l.arc(rx, ry, 16 * s, 0, TAU); l.stroke();
    for (let i = 0; i < 3; i++) { l.strokeRect(x + 30 * s + i * 44 * s, y + 280 * s, 32 * s, 50 * s); } l.restore();
    return { mx: [x - 128 * s, x + 128 * s], my, mr };
  }
  // monitör (1971 kapalı devre): kasa + ekran dikdörtgeni; ekran ölçüsünü döndürür (EKRAN.begin({ekran}) için)
  function monitor(B, x, y, w, h, o = {}) {
    const k = B.k, l = B.l, m = 34;
    if (o.maske !== false) B.ekranMaske(g => g.roundRect(x, y, w, h, 16));
    k.save(); k.fillStyle = T(B, .72); k.beginPath(); k.roundRect(x - m, y - m, w + 2 * m, h + 2 * m + 40, 18); k.fill(); k.restore();
    l.save(); ink(l, 3); l.beginPath(); l.roundRect(x - m, y - m, w + 2 * m, h + 2 * m + 40, 18); l.stroke(); l.beginPath(); l.roundRect(x - 6, y - 6, w + 12, h + 12, 22); l.stroke();
    l.beginPath(); l.arc(x + w - 30, y + h + 30, 8, 0, TAU); l.stroke(); l.restore();
    return { x, y, w, h };
  }
  // daktilo belgesi (kâğıt sahnede): satırlar soldan sağa basılır (p 0..1). Metin çizgi plakasına; vurgu satırı (o.vurgu) renk plakasına kehribar şerit
  function belge(B, x, y, w, satirlar, p, o = {}) {
    const k = B.k, l = B.l, px = o.px || 34, lh = px * 1.45, h = o.h || (satirlar.length * lh + px * 3.6);
    k.save(); k.fillStyle = T(B, .06); k.fillRect(x + 10, y + 12, w, h); k.restore();   // gölge
    l.save(); ink(l, 1.6); l.strokeRect(x, y, w, h);
    l.font = `700 ${px}px "Courier Prime"`; l.textBaseline = 'middle';
    const top = satirlar.reduce((s, r) => s + r.length, 0); let kalan = Math.floor(top * clamp(p));
    satirlar.forEach((r, i) => {
      const yy = y + px * 1.8 + i * lh;
      if (o.vurgu && o.vurgu.includes(i)) B.renkBoya(g => g.rect(x + px * 1.1, yy - px * .55, w - px * 2.2, px * 1.1), .55, 0);
      const s = r.slice(0, Math.max(0, kalan)); kalan -= r.length; l.fillText(s, x + px * 1.4, yy);
    });
    l.restore();
    return { h };
  }
  // yazı tura: dönen bozuk para (ang dönme), (x,y), r
  function para(B, x, y, r, ang, o = {}) {
    const k = B.k, l = B.l, sx = Math.max(.06, Math.abs(Math.cos(ang)));
    k.save(); k.fillStyle = T(B, Math.cos(ang) > 0 ? .25 : .45); k.beginPath(); k.ellipse(x, y, r * sx, r, 0, 0, TAU); k.fill(); k.restore();
    l.save(); ink(l, 3); l.beginPath(); l.ellipse(x, y, r * sx, r, 0, 0, TAU); l.stroke();
    l.restore();
  }
  return { koridor, hucreKapisi, teyp, monitor, belge, para, ink };
})();
