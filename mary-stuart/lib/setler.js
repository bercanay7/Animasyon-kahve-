// setler.js (Mary Stuart): yeniden kullanılan sahne setleri. Hepsi ton resmi boyar (boya.js), motor onu mürekkebe çevirir.
// İçerik: gerçek görsel planı (fotoP), ışıklı masa (masaP), künye ve etiket katmanı, harita, deniz ve tekneler, at ve binici,
// beşik ve taç, arma. Sahne fonksiyonu (G, st) alır; st.t mutlak sn, st.lt plan içi sn, st.p plan ilerlemesi (0..1).
'use strict';
const TAU = Math.PI * 2;
const ust2 = (...fs) => (g, st) => { for (const f of fs) if (f) f(g, st); };   // birden çok katman
// ── künye (kaynak satırı, sol üst) ve etiket (orta-alt, y < 880) ──
const kunye = (txt, o = {}) => (g, st) => {
  const a = clamp((st.lt - (o.gec ?? .5)) / .6) * (o.a ?? .82); if (a <= 0) return;
  g.font = 'italic 500 25px "Cormorant Garamond"'; g.textBaseline = 'middle'; g.textAlign = 'left';
  const w = g.measureText(txt).width; g.fillStyle = `rgba(10,9,8,${a * .55})`; g.fillRect(34, 30, w + 30, 40);
  g.fillStyle = `rgba(236,229,213,${a})`; g.fillText(txt, 49, 51);
};
const etiket = (satirlar, o = {}) => (g, st) => {
  let y = o.y ?? 760;
  for (const l of satirlar) {
    const a = clamp((st.t - (l.at ?? st.at)) / .5); if (a <= 0) { y += l.size * 1.25; continue; }
    g.font = `${l.italic ? 'italic ' : ''}${l.weight ?? 400} ${l.size}px "${l.font ?? 'Cinzel'}"`; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.letterSpacing = (l.spacing ?? 0) + 'px'; g.shadowColor = 'rgba(0,0,0,.85)'; g.shadowBlur = 18;
    g.fillStyle = `rgba(240,234,220,${a})`; g.fillText(l.text, 720, y); g.shadowBlur = 0; g.letterSpacing = '0px';
    y += l.size * 1.25;
  }
};
// zaman yardımcıları: mutlak an (AT biçimi) → plan içinde 0..1
const ac = (st, at, d = .8) => clamp((st.t - AT(at)) / d);
const acS = (st, at, d = .8) => ss((st.t - AT(at)) / d);

// ── gerçek görsel planı: kamera görüntü üzerinde a → b ([cx, cy, w] görüntü kesri; w = genişlik kesri) ──
// o: kontrast, parlak, zemin, look, redraw, kunye, etiket, kirmizi {poly, a(st) | sil(st) (0..1 alttan yukarı)}, ciz (görüntü pikselinde ek çizim), u (ilerleme)
function fotoP(key, a, b, o = {}) {
  return (G, st) => {
    const im = IMG[key]; G.zemin(o.zemin ?? .1); if (!im) return {};
    const W = im.naturalWidth, H = im.naturalHeight, u = o.u ? o.u(st) : eio(st.p);
    const cx = lerp(a[0], b[0], u) * W, cy = lerp(a[1], b[1], u) * H, w = lerp(a[2], b[2], u) * W, k = 1440 / w, h = 1080 / k;
    for (const c of [G.g, G.r]) c.setTransform(k, 0, 0, k, -(cx - w / 2) * k, -(cy - h / 2) * k);
    G.g.save(); if (o.klip) { const [x0, y0, x1, y1] = o.klip; G.g.beginPath(); G.g.rect(x0 * W, y0 * H, (x1 - x0) * W, (y1 - y0) * H); G.g.clip(); }
    G.g.drawImage(BOYA.griOn(im, o.kontrast ?? 1.12, o.parlak ?? 1.03), 0, 0); G.g.restore();
    if (o.ciz) o.ciz(G, st, W, H);
    if (o.kirmizi) {
      const P = G.pathOf(o.kirmizi.poly.map(([x, y]) => [x * W, y * H]), true, .45), ys = o.kirmizi.poly.map(p => p[1] * H), y0 = Math.min(...ys), y1 = Math.max(...ys);
      const al = o.kirmizi.a ? o.kirmizi.a(st) : 1, sil = o.kirmizi.sil ? o.kirmizi.sil(st) : 1;
      if (al > 0 && sil > 0) G.kirmiziCiz(r => { const yf = lerp(y1 + 40, y0 - 40, sil), gr = r.createLinearGradient(0, yf - 60, 0, yf + 60); gr.addColorStop(0, 'rgba(176,22,30,0)'); gr.addColorStop(1, `rgba(176,22,30,${al})`); r.fillStyle = gr; r.fill(P); });
    }
    for (const c of [G.g, G.r]) c.setTransform(1, 0, 0, 1, 0, 0);
    if (o.ust2) o.ust2(G, st);
    return { look: { sepia: .22, strength: .3, ...(o.look || {}) }, redraw: o.redraw, renkTon: o.renkTon, iris: o.iris ? o.iris(st) : undefined, karart: o.karart ? o.karart(st) : 0,
      ust: ust2(o.kunye ? kunye(o.kunye) : null, o.etiket ? etiket(o.etiket) : null, o.ust || null) };
  };
}

// ── ışıklı masa (archive-lighttable): baskı masada, lamba ışığı, büyüteç ──
// o: rot, boy (kâğıt yüksekliği), k0/k1 kamera [cx, cy, z], lens {at, u:[x,y], z, r}, nesne(G, st), kunye, look
function masaP(key, o = {}) {
  return (G, st) => {
    const g = G.g, im = IMG[key], q = G.rng(o.seed || 11);
    const k0 = o.k0 || [720, 540, 1], k1 = o.k1 || [720, 520, 1.1], u = eio(st.p);
    G.kamera(lerp(k0[0], k1[0], u), lerp(k0[1], k1[1], u), lerp(k0[2], k1[2], u));
    // masa: koyu ahşap, uzun damarlar
    g.fillStyle = G.gri(.24); g.fillRect(-600, -600, 2700, 2300);
    for (let i = 0; i < 70; i++) { const y = -500 + q() * 2100, v = .16 + q() * .14; g.fillStyle = G.gri(v, .55); g.beginPath(); g.ellipse(q() * 1440, y, 400 + q() * 900, 3 + q() * 10, (q() - .5) * .03, 0, TAU); g.fill(); }
    const L = o.isik || [430, 250], lg = g.createRadialGradient(L[0], L[1], 30, L[0], L[1], 1100); lg.addColorStop(0, G.gri(1, .5)); lg.addColorStop(1, G.gri(0, .25)); g.fillStyle = lg; g.fillRect(-600, -600, 2700, 2300);
    if (o.altNesne) o.altNesne(G, st);
    if (im) {
      const W = im.naturalWidth, H = im.naturalHeight, ar = W / H; let ph = o.boy ?? 900, pw = ph * ar; if (pw > 1180) { pw = 1180; ph = pw / ar; }
      const cx = o.cx ?? 720, cy = o.cy ?? 540, rot = o.rot ?? -.025;
      g.save(); g.translate(cx, cy); g.rotate(rot);
      BOYA.golge(g, -pw / 2 + 18, -ph / 2 + 26, pw, ph, .7);
      g.drawImage(BOYA.griOn(im, o.kontrast ?? 1.08, o.parlak ?? 1.06), -pw / 2, -ph / 2, pw, ph);
      if (o.lens) {
        const ln = o.lens, a = ss((st.t - AT(ln.at)) / 1.1), R = ln.r ?? 200, z = ln.z ?? 2.2;
        if (a > 0) {
          const tx = (ln.u[0] - .5) * pw, ty = (ln.u[1] - .5) * ph, sx = lerp(pw * .7, tx, a), sy = lerp(ph * .75, ty, a);
          { const sg = g.createRadialGradient(sx + 30, sy + 40, R * .8, sx + 30, sy + 40, R + 40); sg.addColorStop(0, G.gri(0, .5)); sg.addColorStop(1, G.gri(0, 0)); g.fillStyle = sg; g.fillRect(sx - R, sy - R, R * 2 + 120, R * 2 + 120); }
          g.save(); g.beginPath(); g.arc(sx, sy, R, 0, TAU); g.clip();
          const ux = (sx + pw / 2) / pw, uy = (sy + ph / 2) / ph;   // merceğin altındaki nokta (görüntü kesri)
          g.drawImage(BOYA.griOn(im, (o.kontrast ?? 1.08) + .06, 1.1), sx - ux * pw * z, sy - uy * ph * z, pw * z, ph * z);
          const sh = g.createRadialGradient(sx - R * .3, sy - R * .35, R * .1, sx, sy, R); sh.addColorStop(0, G.gri(1, .18)); sh.addColorStop(.85, G.gri(1, 0)); sh.addColorStop(1, G.gri(0, .35)); g.fillStyle = sh; g.fillRect(sx - R, sy - R, R * 2, R * 2);
          g.restore();
          g.strokeStyle = G.gri(.14); g.lineWidth = 22; g.beginPath(); g.arc(sx, sy, R + 9, 0, TAU); g.stroke();
          g.strokeStyle = G.gri(.75); g.lineWidth = 3; g.beginPath(); g.arc(sx, sy, R + 2, -2.4, -1.2); g.stroke();
          g.strokeStyle = G.gri(.1); g.lineWidth = 38; g.lineCap = 'round'; const hx = Math.cos(.75), hy = Math.sin(.75); g.beginPath(); g.moveTo(sx + hx * (R + 22), sy + hy * (R + 22)); g.lineTo(sx + hx * (R + 330), sy + hy * (R + 330)); g.stroke();
        }
      }
      g.restore();
    }
    if (o.nesne) o.nesne(G, st);
    return { look: { sepia: .3, strength: .26, ...(o.look || {}) }, redraw: o.redraw, ust: ust2(o.kunye ? kunye(o.kunye) : null, o.ust || null), renkTon: o.renkTon };
  };
}

// ── harita (1560'lar; Britanya adaları, Fransa kıyısı): eşdikdörtgen izdüşüm ──
const HARITA = {
  bri: [[-3.0, 58.65], [-3.1, 58.4], [-3.9, 57.85], [-4.2, 57.5], [-3.3, 57.68], [-2.0, 57.7], [-2.08, 57.15], [-2.45, 56.7], [-2.9, 56.45], [-2.6, 56.28], [-3.0, 56.1], [-3.4, 56.02], [-3.2, 55.98], [-2.55, 56.0], [-2.15, 55.9], [-2.0, 55.77], [-1.6, 55.4], [-1.42, 55.0], [-1.1, 54.6], [-0.6, 54.48], [-0.08, 54.12], [0.12, 53.6], [0.25, 53.1], [0.2, 52.9], [0.9, 52.95], [1.7, 52.75], [1.75, 52.45], [1.6, 52.1], [1.28, 51.95], [0.9, 51.75], [0.6, 51.52], [1.44, 51.38], [1.32, 51.13], [0.95, 50.92], [0.25, 50.74], [-0.79, 50.73], [-1.6, 50.72], [-2.45, 50.58], [-3.4, 50.62], [-3.64, 50.22], [-4.4, 50.35], [-5.2, 49.96], [-5.7, 50.07], [-5.0, 50.5], [-4.5, 51.0], [-3.5, 51.2], [-2.75, 51.5], [-3.17, 51.45], [-3.95, 51.6], [-4.8, 51.65], [-5.3, 51.88], [-4.6, 52.1], [-4.08, 52.4], [-4.1, 52.75], [-4.75, 52.8], [-4.3, 53.15], [-4.6, 53.35], [-4.1, 53.3], [-3.05, 53.4], [-3.05, 53.8], [-2.85, 54.1], [-3.3, 54.2], [-3.55, 54.64], [-3.3, 54.95], [-3.6, 54.9], [-4.0, 54.78], [-4.4, 54.7], [-4.85, 54.64], [-5.0, 54.9], [-4.9, 55.1], [-4.65, 55.47], [-4.9, 55.75], [-4.5, 55.92], [-5.0, 55.85], [-5.4, 55.6], [-5.8, 55.3], [-5.6, 55.8], [-5.6, 56.2], [-5.5, 56.45], [-6.2, 56.7], [-5.75, 56.95], [-6.3, 57.3], [-5.7, 57.6], [-5.8, 57.85], [-5.3, 58.25], [-5.0, 58.6], [-4.4, 58.55], [-3.6, 58.62]],
  irl: [[-7.4, 55.38], [-6.15, 55.22], [-5.6, 54.75], [-5.9, 54.6], [-5.55, 54.3], [-6.1, 54.0], [-6.2, 53.35], [-6.0, 52.95], [-6.4, 52.3], [-6.36, 52.17], [-7.0, 52.15], [-8.3, 51.8], [-9.0, 51.55], [-9.8, 51.45], [-10.3, 51.85], [-10.3, 52.1], [-9.8, 52.4], [-9.6, 52.6], [-9.3, 52.9], [-9.2, 53.2], [-10.1, 53.5], [-9.9, 53.9], [-10.1, 54.2], [-9.0, 54.25], [-8.5, 54.3], [-8.8, 54.65], [-8.3, 55.15], [-7.6, 55.25]],
  fra: [[4.8, 53.1], [4.75, 52.95], [4.5, 52.3], [4.0, 51.95], [3.6, 51.5], [2.9, 51.23], [2.37, 51.04], [1.85, 50.95], [1.6, 50.73], [1.6, 50.2], [1.08, 49.93], [0.1, 49.5], [-0.3, 49.3], [-1.2, 49.38], [-1.6, 49.65], [-1.85, 49.4], [-1.5, 48.65], [-2.0, 48.65], [-3.0, 48.85], [-4.75, 48.4], [-4.35, 47.8], [-3.4, 47.7], [-2.2, 47.25], [-1.2, 46.15], [-1.1, 45.6], [-1.3, 44.5], [-2.0, 43.5], [8, 43.5], [8, 53.1]],
  P: (lon, lat) => [720 + (lon + 3.5) * 42.3 * 1.6, 540 - (lat - 53.5) * 72 * 1.6],
  yer: { edinburgh: [-3.19, 55.95], londra: [-0.12, 51.5], calais: [1.85, 50.95], paris: [2.35, 48.86], solway: [-3.6, 54.8], dundrennan: [-3.95, 54.81], workington: [-3.55, 54.64], carlisle: [-2.94, 54.9], tutbury: [-1.69, 52.86], sheffield: [-1.47, 53.38], chartley: [-1.98, 52.85], fotheringhay: [-0.44, 52.53], leith: [-3.17, 55.98], lochleven: [-3.38, 56.2], dunbar: [-2.52, 56.0], york: [-1.08, 53.96], nottingham: [-1.15, 52.95], greenwich: [0.0, 51.48], westminster: [-0.13, 51.5] },
};
function kismiYol(pts, p) { if (p >= 1) return pts; const L = [0]; for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const tl = L[L.length - 1] * clamp(p), out = [pts[0]]; for (let i = 1; i < pts.length; i++) { if (L[i] <= tl) out.push(pts[i]); else { const f = (tl - L[i - 1]) / (L[i] - L[i - 1]); out.push([lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f)]); break; } } return out; }
// o: kamera [lon, lat, z] (k0 → k1), yollar [{pts:[[lon,lat]...], p, kirmizi, kesik, w}], yazilar [[metin, lon, lat, boy]], isaretler [{yer, a, tur:'kale'|'nokta'|'muhur', kirmizi}]
function harita(G, st, o = {}) {
  const g = G.g, P = HARITA.P, u = o.u ?? eio(st.p), k0 = o.k0 || [-3.2, 53.6, 1], k1 = o.k1 || k0;
  const c = P(lerp(k0[0], k1[0], u), lerp(k0[1], k1[1], u)), z = lerp(k0[2], k1[2], u); G.kamera(c[0], c[1], z);
  g.fillStyle = G.gri(.8); g.fillRect(-3000, -3000, 8000, 8000);    // deniz (parşömen tonu)
  const kara = [HARITA.bri, HARITA.irl, HARITA.fra].map(L => G.pathOf(L.map(p => P(...p)), true, .5));
  // kıyı boyunca açılan dalga çizgileri (eski harita oyması)
  for (let i = 6; i >= 1; i--) { g.strokeStyle = G.gri(.62 + i * .03, .9); g.lineWidth = i * 14 / z + 2; for (const K of kara) g.stroke(K); g.strokeStyle = G.gri(.8); g.lineWidth = i * 14 / z - 2; for (const K of kara) g.stroke(K); }
  g.fillStyle = G.gri(.93); for (const K of kara) g.fill(K);
  g.strokeStyle = G.gri(.22); g.lineWidth = 3 / z + 1; for (const K of kara) g.stroke(K);
  // kara içinde yumuşak kabartma lekeleri (dağlar)
  const q = G.rng(5); for (let i = 0; i < 40; i++) { const lon = -6 + q() * 5, lat = 54.5 + q() * 3.6, p = P(lon, lat); if (!g.isPointInPath(kara[0], p[0], p[1])) continue; g.fillStyle = G.gri(.78, .5); g.beginPath(); g.ellipse(p[0], p[1], 24 + q() * 30, 8 + q() * 6, 0, 0, TAU); g.fill(); }
  // sınır (İskoçya / İngiltere), kesik
  g.save(); g.setLineDash([10 / z + 4, 8 / z + 3]); g.strokeStyle = G.gri(.35); g.lineWidth = 2.5 / z + 1; g.beginPath(); for (const [i, p] of [[-3.05, 54.98], [-2.6, 55.15], [-2.2, 55.4], [-2.0, 55.77]].entries()) { const xy = P(...p); i ? g.lineTo(...xy) : g.moveTo(...xy); } g.stroke(); g.restore();
  for (const y of (o.yollar || [])) {
    const pts = kismiYol(y.pts.map(p => P(...p)), y.p ?? 1); if (pts.length < 2) continue;
    const ciz = c2 => { c2.save(); c2.lineCap = 'round'; c2.lineJoin = 'round'; c2.lineWidth = (y.w ?? 7) / z + 2; if (y.kesik) c2.setLineDash([16 / z + 6, 12 / z + 5]); c2.beginPath(); pts.forEach((p, i) => i ? c2.lineTo(...p) : c2.moveTo(...p)); c2.stroke(); c2.setLineDash([]);
      if ((y.p ?? 1) > .02 && y.ok !== false) { const a = pts[pts.length - 1], b = pts[Math.max(0, pts.length - 2)], an = Math.atan2(a[1] - b[1], a[0] - b[0]), L = 26 / z + 8; c2.beginPath(); c2.moveTo(a[0] + Math.cos(an) * L * .6, a[1] + Math.sin(an) * L * .6); c2.lineTo(a[0] + Math.cos(an + 2.5) * L, a[1] + Math.sin(an + 2.5) * L); c2.lineTo(a[0] + Math.cos(an - 2.5) * L, a[1] + Math.sin(an - 2.5) * L); c2.closePath(); c2.fill(); } c2.restore(); };
    g.strokeStyle = g.fillStyle = G.gri(y.v ?? .15, y.alfa ?? 1); ciz(g);
    if (y.kirmizi) G.kirmiziCiz(r => ciz(r));
  }
  for (const m of (o.isaretler || [])) {
    const a = m.a ?? 1; if (a <= 0) continue; const p = P(...(HARITA.yer[m.yer] || m.ll)), s = (m.s ?? 16) / z + 4;
    if (m.tur === 'kale') { g.fillStyle = G.gri(.12, a); g.fillRect(p[0] - s, p[1] - s * 1.2, s * 2, s * 1.2); for (let i = -1; i <= 1; i++) g.fillRect(p[0] + i * s * .7 - s * .25, p[1] - s * 1.6, s * .5, s * .5); g.fillRect(p[0] - s * .3, p[1] - s * 2.1, s * .6, s); }
    else { g.fillStyle = G.gri(.1, a); g.beginPath(); g.arc(p[0], p[1], s * .55, 0, TAU); g.fill(); }
    if (m.kirmizi) G.kirmizi((() => { const Q = new Path2D(); Q.arc(p[0], p[1], s * .9, 0, TAU); return Q; })(), a);
  }
  g.textAlign = 'center'; g.textBaseline = 'middle';
  for (const [txt, lon, lat, boy, a] of (o.yazilar || [])) { if ((a ?? 1) <= 0) continue; const p = P(lon, lat); g.font = `600 ${(boy || 30) / Math.sqrt(z)}px "Cinzel"`; g.letterSpacing = '4px'; g.fillStyle = G.gri(.18, a ?? 1); g.fillText(txt, p[0], p[1]); g.letterSpacing = '0px'; }
  // pusula gülü (sağ alt köşe, kameraya göre değil haritaya göre)
  if (o.pusula !== false) { const p = P(3.2, 56.8), R = 90; g.save(); g.translate(...p); g.fillStyle = G.gri(.25); for (let i = 0; i < 8; i++) { const a = i * TAU / 8 - Math.PI / 2, rr = i % 2 ? R * .5 : R; g.beginPath(); g.moveTo(Math.cos(a) * rr, Math.sin(a) * rr); g.lineTo(Math.cos(a + .32) * R * .16, Math.sin(a + .32) * R * .16); g.lineTo(Math.cos(a - .32) * R * .16, Math.sin(a - .32) * R * .16); g.fill(); } g.strokeStyle = G.gri(.3); g.lineWidth = 2; g.beginPath(); g.arc(0, 0, R * .62, 0, TAU); g.stroke(); g.font = '600 30px "Cinzel"'; g.fillText('N', 0, -R - 22); g.restore(); }
  for (const c2 of [g, G.r]) c2.setTransform(1, 0, 0, 1, 0, 0);
  // eski kâğıt: kenarlara doğru koyulaşan leke
  const vg = g.createRadialGradient(720, 540, 380, 720, 540, 900); vg.addColorStop(0, G.gri(1, 0)); vg.addColorStop(1, G.gri(.35, .55)); g.fillStyle = vg; g.fillRect(0, 0, 1440, 1080);
}

// ── at ve binici (siluet; dörtnal döngüsü). o: x, y (zemin), s (at boyu px), f (yön ±1), ph (faz), binici {kind,...}|null ──
function at(G, o) {
  const g = G.g, s = o.s, f = o.f || 1, ph = o.ph || 0, X = o.x, Y = o.y, bob = Math.sin(ph * TAU * 2) * .012, pit = Math.sin(ph * TAU) * .03;
  const T = (x, y) => { const c = Math.cos(pit), sn = Math.sin(pit); const qx = x * c - (y + .6) * sn, qy = x * sn + (y + .6) * c - .6; return [X + qx * s * f, Y + (qy + bob) * s]; };
  const P = pts => G.pathOf(pts.map(([x, y]) => T(x, y)), true, .55);
  const parts = [];
  parts.push(P([[-.52, -.62], [-.44, -.73], [-.2, -.77], [.1, -.75], [.28, -.74], [.38, -.64], [.35, -.5], [.15, -.45], [-.15, -.46], [-.42, -.5], [-.53, -.56]]));   // gövde
  const nb = Math.sin(ph * TAU) * .02;
  parts.push(P([[.22, -.72], [.36, -.92 + nb], [.45, -1.03 + nb], [.53, -1.02 + nb], [.5, -.9], [.4, -.6]]));   // boyun
  parts.push(P([[.44, -1.04 + nb], [.47, -1.12 + nb], [.5, -1.05 + nb], [.55, -1.05 + nb], [.68, -.92 + nb], [.7, -.87 + nb], [.64, -.85 + nb], [.52, -.92 + nb]]));   // baş
  const tl = Math.sin(ph * TAU + 1) * .05;
  parts.push(P([[-.5, -.7], [-.62, -.66 + tl], [-.74, -.54 + tl * 1.5], [-.8, -.44 + tl * 2], [-.72, -.48 + tl], [-.62, -.58], [-.5, -.62]]));   // kuyruk
  // bacaklar: dörtnal (ön çift ve arka çift, aralarında faz farkı)
  const leg = (hx, hy, a, k, L1, L2, w) => { const kn = [hx + Math.sin(a) * L1, hy + Math.cos(a) * L1], an = [kn[0] + Math.sin(a + k) * L2, kn[1] + Math.cos(a + k) * L2];
    parts.push(G.pathOf([...[[hx - w, hy], [kn[0] - w * .6, kn[1]], [an[0] - w * .35, an[1]], [an[0] + w * .5, an[1] + .03], [an[0] + w * .35, an[1]], [kn[0] + w * .6, kn[1]], [hx + w, hy]].map(([x, y]) => T(x, y))], true, .4)); };
  const run = o.dur ? 0 : 1;
  for (const [hx, off, front] of [[.24, 0, 1], [.3, .12, 1], [-.36, .45, 0], [-.3, .57, 0]]) {
    const w = Math.sin((ph + off) * TAU), a = run * w * (front ? .75 : .7) + (front ? .05 : -.05), k = front ? -Math.max(0, -w) * 1.4 * run : Math.max(0, w) * 1.1 * run;
    leg(hx, -.52, a, front ? k : k, .26, .28, .045);
  }
  g.fillStyle = G.gri(o.v ?? .1); for (const p of parts) g.fill(p);
  if (o.binici) { const b = T(-.04, -.74); G.figur({ poz: 'otur', kol: 'tut', ...o.binici, x: b[0], y: b[1] + s * .17, s: s * (o.binici.h ?? .82), f, t: o.t, wind: 1 }); }
}

// ── tekneler ──
// kadırga (Fransız, 1561): uzun alçak gövde, kürek sıraları, iki latin yelken, kıçta tente
function kadirga(G, o) {
  const g = G.g, s = o.s, f = o.f || 1, X = o.x, Y = o.y, t = o.t || 0, rk = Math.sin(t * .9) * .008;
  const T = (x, y) => { const c = Math.cos(rk), sn = Math.sin(rk); return [X + (x * c - y * sn) * s * f, Y + (x * sn + y * c) * s]; };
  g.strokeStyle = G.gri(.12); g.lineWidth = Math.max(1.5, s * .004);
  for (let i = 0; i < 16; i++) { const x = -.36 + i * .045, a = Math.sin(t * 1.6 * (o.kurek ?? 1) - i * .25) * .05; const p0 = T(x, -.03), p1 = T(x - .05 + a, .07); g.beginPath(); g.moveTo(...p0); g.lineTo(...p1); g.stroke(); }
  g.fillStyle = G.gri(.13); g.fill(G.pathOf([[-.5, -.07], [-.3, -.05], [.2, -.05], [.46, -.07], [.56, -.1], [.5, -.04], [.38, .0], [-.3, .01], [-.46, -.01], [-.52, -.04]].map(([x, y]) => T(x, y)), true, .4));
  g.fill(G.pathOf([[-.5, -.07], [-.48, -.15], [-.36, -.16], [-.32, -.07]].map(([x, y]) => T(x, y)), true, .3));    // kıç köşkü
  g.fillStyle = G.gri(.55); g.fill(G.pathOf([[-.49, -.15], [-.44, -.22], [-.36, -.2], [-.34, -.15]].map(([x, y]) => T(x, y)), true, .5));   // tente
  for (const [mx, h, yl] of [[.12, .46, 1], [-.12, .36, .8]]) {
    const m0 = T(mx, -.05), m1 = T(mx, -.05 - h); g.strokeStyle = G.gri(.1); g.lineWidth = Math.max(2, s * .006); g.beginPath(); g.moveTo(...m0); g.lineTo(...m1); g.stroke();
    const b = Math.sin(t * 1.3 + mx * 9) * .01, ya = T(mx - .2 * yl, -.05 - h * .25), yb = T(mx + .22 * yl, -.05 - h * 1.05);
    g.beginPath(); g.moveTo(...ya); g.lineTo(...yb); g.stroke();
    g.fillStyle = G.gri(o.yelken ?? .82); g.fill(G.pathOf([[mx - .19 * yl, -.05 - h * .27], [mx + .21 * yl, -.05 - h * 1.02], [mx + (.16 + b) * yl, -.05 - h * .5], [mx + .02, -.05 - h * .12]].map(([x, y]) => T(x, y)), true, .5));
  }
  for (const k of (o.kisi || [])) { const p = T(k.x, -.07); G.figur({ ...k, x: p[0], y: p[1], s: s * (k.h ?? .1), f: k.f ?? f, t, wind: .7 }); }
}
// uzak gemi (karaka): batma (b: 0..1)
function karaka(G, o) {
  const g = G.g, s = o.s, X = o.x, b = o.b || 0, Y = o.y + b * s * .5, rk = b * .5;
  const T = (x, y) => { const c = Math.cos(rk), sn = Math.sin(rk); return [X + (x * c - y * sn) * s, Y + (x * sn + y * c) * s]; };
  g.save(); g.beginPath(); g.rect(X - s * 2, Y - s * 3 - b * s, s * 4, (o.y - (Y - s * 3 - b * s)) + 1); g.clip();
  g.fillStyle = G.gri(o.v ?? .3); g.fill(G.pathOf([[-.5, -.18], [-.3, -.1], [.3, -.1], [.5, -.25], [.42, .02], [-.4, .02]].map(([x, y]) => T(x, y)), true, .3));
  g.strokeStyle = G.gri(o.v ?? .3); g.lineWidth = Math.max(1.5, s * .03); for (const mx of [-.15, .12]) { g.beginPath(); g.moveTo(...T(mx, -.1)); g.lineTo(...T(mx, -.95)); g.stroke(); }
  g.fillStyle = G.gri((o.v ?? .3) + .35); for (const [mx, y0, w] of [[-.15, -.85, .2], [.12, -.9, .24], [-.15, -.5, .24], [.12, -.55, .28]]) g.fill(G.pathOf([[mx - w / 2, y0], [mx + w / 2, y0], [mx + w * .55, y0 + .28], [mx - w * .55, y0 + .28]].map(([x, y]) => T(x, y)), true, .4));
  g.restore();
}

// ── beşik (Linlithgow, 1542; Stirling, 1566): panelli ahşap beşik, köşe direkleri, başlık, sarkan örtü; ışık soldan ──
function besik(G, o) {
  const g = G.g, s = o.s, X = o.x, Y = o.y, rk = Math.sin((o.t || 0) * 1.1) * (o.salla ?? .02);
  const T = (x, y) => { const c = Math.cos(rk), sn = Math.sin(rk); return [X + (x * c - (y + .1) * sn) * s, Y + (x * sn + (y + .1) * c - .1) * s]; };
  const P = (pts, k = .5) => G.pathOf(pts.map(([x, y]) => T(x, y)), true, k), poly = pts => G.polyP(pts.map(([x, y]) => T(x, y)));
  const yan = (x0, x1, v0, v1) => { const a = T(x0, 0), b = T(x1, 0), gr = g.createLinearGradient(a[0], 0, b[0], 0); gr.addColorStop(0, G.gri(v0)); gr.addColorStop(1, G.gri(v1)); return gr; };
  // gölge
  g.fillStyle = G.gri(0, .45); g.beginPath(); g.ellipse(...T(0, .07), s * .62, s * .05, 0, 0, TAU); g.fill();
  // kızaklar
  g.fillStyle = G.gri(.12); for (const dx of [-.34, .3]) g.fill(P([[dx - .26, -.02], [dx - .12, .045], [dx + .12, .045], [dx + .26, -.02], [dx + .22, .0], [dx + .1, .02], [dx - .1, .02], [dx - .22, .0]], .6));
  // gövde yan yüzü (panelli)
  g.fillStyle = yan(-.5, .5, .46, .2); g.fill(poly([[-.5, -.42], [.5, -.42], [.5, -.04], [-.5, -.04]]));
  for (let i = 0; i < 4; i++) { const x0 = -.45 + i * .235, x1 = x0 + .2;
    g.fillStyle = yan(x0, x1, .38 - i * .05, .3 - i * .05); g.fill(poly([[x0, -.37], [x1, -.37], [x1, -.09], [x0, -.09]]));
    g.fillStyle = G.gri(.62 - i * .08); g.fill(poly([[x0, -.37], [x1, -.37], [x1 - .015, -.355], [x0 + .015, -.355]]));    // üst pah (ışık)
    g.fillStyle = G.gri(.1); g.fill(poly([[x0 + .015, -.105], [x1 - .015, -.105], [x1, -.09], [x0, -.09]])); }       // alt pah (gölge)
  g.fillStyle = G.gri(.16); g.fill(poly([[-.52, -.44], [.52, -.44], [.52, -.41], [-.52, -.41]]));   // kenar pervazı
  // başlık (baş ucunda; içi karanlık)
  g.fillStyle = yan(.2, .52, .3, .14); g.fill(P([[.2, -.42], [.2, -.7], [.27, -.8], [.52, -.84], [.52, -.42]], .3));
  g.fillStyle = G.gri(.06); g.fill(P([[.2, -.42], [.2, -.69], [.25, -.75], [.27, -.72], [.27, -.44]], .3));
  g.fillStyle = G.gri(.5); g.fill(P([[.18, -.7], [.27, -.82], [.54, -.86], [.54, -.83], [.27, -.79], [.2, -.69]], .3));
  // köşe direkleri ve topuzlar
  for (const dx of [-.5, .5]) { g.fillStyle = yan(dx - .03, dx + .03, .5, .14); g.fill(poly([[dx - .028, -.04], [dx + .028, -.04], [dx + .028, -.5], [dx - .028, -.5]]));
    g.fillStyle = G.gri(.4); g.fill(G.ell(T(dx, -.54), s * .038, s * .038)); g.fillStyle = G.gri(.75); g.fill(G.ell(T(dx - .012, -.553), s * .012, s * .012)); }
  // örtü: kenardan sarkar, kıvrımlı alt kenar; bebek varsa üstte kabarık
  const ort = [[-.46, -.43], [-.3, -.47], [-.05, -.48], [.2, -.45], [.21, -.3], [.17, -.22], [.12, -.27], [.05, -.2], [-.04, -.26], [-.13, -.19], [-.22, -.25], [-.31, -.18], [-.4, -.24], [-.47, -.2]];
  g.fillStyle = yan(-.47, .21, .95, .7); g.fill(P(ort, .55));
  g.strokeStyle = G.gri(.6); g.lineWidth = s * .004; for (const x of [-.36, -.18, 0, .12]) { g.beginPath(); g.moveTo(...T(x, -.44)); g.quadraticCurveTo(...T(x + .02, -.33), ...T(x - .01, -.22)); g.stroke(); }
  if (o.bebek) { g.fillStyle = G.gri(.92); g.fill(P([[-.1, -.47], [0, -.56], [.12, -.58], [.18, -.5], [.18, -.45], [-.1, -.45]], .7)); g.fillStyle = G.gri(.82); g.fill(G.ell(T(.13, -.55), s * .05, s * .045)); }
}
// taç (kapalı kemerli İskoç/İngiliz tacı, sade)
function tac(G, x, y, s, o = {}) {
  const g = G.g; g.save(); g.translate(x, y); g.rotate(o.rot || 0); g.scale(s, s);
  g.fillStyle = G.gri(o.v ?? .3); g.fill(G.pathOf([[-.5, 0], [.5, 0], [.48, -.16], [-.48, -.16]], true, .2));
  for (let i = -2; i <= 2; i++) { g.fill(G.pathOf([[i * .22 - .07, -.15], [i * .22, -.36 - (i % 2 ? 0 : .06)], [i * .22 + .07, -.15]], true, .4)); g.beginPath(); g.arc(i * .22, -.4 - (i % 2 ? 0 : .06), .045, 0, TAU); g.fill(); }
  g.strokeStyle = G.gri(o.v ?? .3); g.lineWidth = .05; g.beginPath(); g.moveTo(-.45, -.16); g.quadraticCurveTo(-.4, -.6, 0, -.62); g.quadraticCurveTo(.4, -.6, .45, -.16); g.stroke();
  g.beginPath(); g.arc(0, -.68, .06, 0, TAU); g.fill(); g.fillRect(-.015, -.86, .03, .16); g.fillRect(-.07, -.8, .14, .03);
  g.fillStyle = G.gri(.92); for (let i = -2; i <= 2; i++) { g.beginPath(); g.arc(i * .2, -.08, .035, 0, TAU); g.fill(); }
  g.restore();
}

// ── arma: kalkan, aslanlar ──
const ASLAN_D = [[.06, .17], [.08, .12], [.12, .08], [.15, .04], [.18, .07], [.24, .03], [.3, .07], [.33, .04], [.38, .11], [.42, .1], [.44, .18], [.48, .24], [.47, .3], [.53, .4], [.6, .5], [.68, .56], [.72, .62], [.76, .58], [.8, .46], [.84, .34], [.82, .24], [.86, .16], [.93, .1], [.96, .16], [.91, .2], [.95, .25], [.89, .25], [.88, .32], [.86, .44], [.82, .58], [.78, .68],
  [.76, .76], [.72, .86], [.74, .92], [.8, .97], [.84, .99], [.76, 1], [.66, .99], [.64, .95], [.68, .92], [.66, .86], [.62, .76], [.55, .7], [.5, .74], [.44, .82], [.36, .86], [.3, .84], [.26, .88], [.25, .82], [.3, .78], [.38, .76], [.44, .7], [.42, .6], [.38, .5],
  [.3, .5], [.2, .53], [.13, .52], [.09, .56], [.08, .5], [.12, .47], [.22, .45], [.33, .42], [.3, .36], [.22, .33], [.14, .3], [.08, .27], [.04, .3], [.04, .24], [.1, .22], [.2, .25], [.28, .27], [.24, .22], [.18, .22], [.12, .24], [.08, .22], [.11, .19]];
const ASLAN_Y = [[.16, .16], [.3, .12], [.55, .13], [.75, .12], [.84, .16], [.88, .1], [.86, .02], [.78, 0], [.72, .04], [.76, .05], [.8, .04], [.82, .1], [.8, .16], [.84, .24], [.86, .34], [.85, .44], [.9, .48], [.82, .48], [.8, .36], [.76, .3], [.74, .36], [.72, .46], [.76, .49], [.68, .49], [.68, .36], [.6, .3], [.4, .3],
  [.36, .38], [.35, .46], [.39, .49], [.3, .49], [.29, .36], [.26, .32], [.2, .33], [.12, .3], [.08, .34], [.07, .28], [.14, .25], [.2, .26], [.18, .2]];
function aslan(G, P0, x, y, w, h, v, renk) { const P = G.pathOf(P0.map(([a, b]) => [x + a * w, y + b * h]), true, .35);
  if (P0 === ASLAN_Y) { P.addPath(G.ell([x + .13 * w, y + .12 * h], w * .085, h * .19)); }   // önden bakan baş (yürüyen aslan)
  G.g.fillStyle = G.gri(v); G.g.fill(P); if (renk) G.kirmizi(P, renk); return P; }
const kalkanYol = (x, y, w, h) => { const P = new Path2D(); P.moveTo(x - w / 2, y - h / 2); P.lineTo(x + w / 2, y - h / 2); P.lineTo(x + w / 2, y + h * .1); P.quadraticCurveTo(x + w / 2, y + h * .42, x, y + h / 2); P.quadraticCurveTo(x - w / 2, y + h * .42, x - w / 2, y + h * .1); P.closePath(); return P; };
// o: ing (0..1 İngiltere yarısı kayar), ingKirmizi (0..1), tac (0..1)
function arma(G, x, y, w, h, o = {}) {
  const g = G.g, K = kalkanYol(x, y, w, h);
  BOYA.golge(g, x - w / 2 + 14, y - h / 2 + 22, w, h, .6);
  g.fillStyle = G.gri(.86); g.fill(K); g.save(); g.clip(K);
  // sol: İskoçya (dikilmiş aslan, çift çiçekli bordür)
  const bw = w * .07; g.strokeStyle = G.gri(.35); g.lineWidth = bw * .25; const B = kalkanYol(x - w * (o.ing > 0 ? .25 : 0), y, w * (o.ing > 0 ? .5 : 1) - bw * 2, h - bw * 2); g.stroke(B);
  const sw = o.ing > 0 ? w * .44 : w * .7; aslan(G, ASLAN_D, x - (o.ing > 0 ? w * .25 : 0) - sw / 2, y - h * .33, sw, h * .62, .2);
  // sağ: İngiltere (üç yürüyen aslan), kayarak gelir
  if (o.ing > 0) {
    const off = (1 - ss(o.ing)) * w * .6; g.save(); g.beginPath(); g.rect(x, y - h, w, h * 2); g.clip(); g.translate(off, 0);
    g.fillStyle = G.gri(.7); g.fillRect(x, y - h, w, h * 2);
    if (o.ingKirmizi) G.kirmiziCiz(r => { r.save(); r.clip(K); r.globalAlpha = o.ingKirmizi * .85; r.fillRect(x + off, y - h, w, h * 2); r.restore(); });
    for (let i = 0; i < 3; i++) aslan(G, ASLAN_Y, x + w * .06, y - h * .38 + i * h * .25, w * .38, h * .2, .14);
    g.restore();
    g.fillStyle = G.gri(.2); g.fillRect(x - w * .006, y - h / 2, w * .012, h);
  }
  g.restore();
  g.strokeStyle = G.gri(.15); g.lineWidth = w * .02; g.stroke(K);
  if (o.tac > 0) tac(G, x, y - h / 2 - h * .06, w * .55, { v: lerp(.6, .25, o.tac) });
}

// ── kale / şehir silueti: parçalar listesi. {t:'sur'|'kule'|'yuv'|'kilise'|'ev', x, w, h, cati:'konik'|'mazgal'|'sivri'|'beşik'} (x, w, h birim: s) ──
// Işık soldan: her parçanın sol şeridi açık ton. y = taban çizgisi.
function kale(G, X, Y, s, parcalar, o = {}) {
  const g = G.g, v = o.v ?? .2, vI = o.isik ?? Math.min(.9, v + .22);
  const dik = (x, y, w, h, vv) => { g.fillStyle = G.gri(vv); g.fillRect(X + x * s, Y - (y + h) * s, w * s, h * s); };
  for (const p of parcalar) {
    const x = p.x - p.w / 2, h = p.h, w = p.w, y0 = p.y || 0;
    dik(x, y0, w, h, v); dik(x, y0, w * .28, h, lerp(v, vI, .55));
    if (p.cati === 'mazgal' || (!p.cati && p.t !== 'ev')) { const n = Math.max(2, Math.round(w / .06)); for (let i = 0; i < n; i += 2) dik(x + i * w / n, y0 + h, w / n, .035, i ? v : lerp(v, vI, .55)); }
    if (p.cati === 'konik' || p.cati === 'sivri') { const hh = p.cati === 'sivri' ? p.ch ?? w * 2.6 : p.ch ?? w * 1.1; g.fillStyle = G.gri(v - .04); g.beginPath(); g.moveTo(X + (x - .01) * s, Y - (y0 + h) * s); g.lineTo(X + (x + w / 2) * s, Y - (y0 + h + hh) * s); g.lineTo(X + (x + w + .01) * s, Y - (y0 + h) * s); g.closePath(); g.fill();
      g.fillStyle = G.gri(lerp(v, vI, .5)); g.beginPath(); g.moveTo(X + (x - .01) * s, Y - (y0 + h) * s); g.lineTo(X + (x + w / 2) * s, Y - (y0 + h + hh) * s); g.lineTo(X + (x + w * .3) * s, Y - (y0 + h) * s); g.closePath(); g.fill(); }
    if (p.cati === 'beşik') { g.fillStyle = G.gri(v - .04); g.beginPath(); g.moveTo(X + x * s, Y - (y0 + h) * s); g.lineTo(X + (x + w / 2) * s, Y - (y0 + h + w * .45) * s); g.lineTo(X + (x + w) * s, Y - (y0 + h) * s); g.closePath(); g.fill(); }
    // pencereler (ışıklı ya da karanlık)
    if (p.pen) { const q = G.rng(Math.round(p.x * 100) + 7); for (let i = 0; i < p.pen; i++) { const px = x + w * (.2 + q() * .6), py = y0 + h * (.25 + q() * .6); dik(px, py, .014, .03, o.gece ? (q() < .5 ? .85 : .1) : .08); } }
  }
}
