// Dikey Shorts (Narkissos, 23 Kasım 2026). İlk dikey deneme: yatay filmden kırpma değil, filmin planları
// dikey tuvale yeniden çizilir (shorts/core_dikey.js: mantıksal dünya 1920×1080, tuval 1080×1920, plan başına mercek).
// Neden: Elizabeth Shorts'unda izlemeye devam eden %27, Milton %32–38 (kırpma: küçük figür, üst bant, ilk karede hareket yok).
// Kurallar: ilk saniyede soru (sesli ve yazılı) + hareket; üstte künye bandı yok; altyazı ortada, sağ sütun (beğen/yorum) ve alt bant boş.
// Ölçüt (analiz/tahminler.md): izlemeye devam eden ≥ %60.
'use strict';
(() => {
  // ── kesitler: film zamanı [s0, s1]; mercek film zamanına göre (ilk eşleşen 'from'dan itibaren) ──
  const KESIT = [
    { s0: 0.25, s1: 3.45, lens: [{ from: 0, cx: 1120, cy: 560, k: 1.55 }] },                     // A01 "Bugün bir camda kendine kaç kez baktın?"
    { s0: 262.75, s1: 267.95, lens: [{ from: 0, cx: 1010, cy: 540, k: 1.78 }, { from: 265.7, cx: 1000, cy: 540, k: 1.78 }] }, // E02 uzatır / gülümser
    { s0: 275.80, s1: 282.05, lens: [{ from: 0, cx: 900, cy: 540, k: 1.78 }] },                    // E03 "Ve anlar." E04 "O benim…"
    { s0: 284.95, s1: 288.05, lens: [{ from: 0, cx: 960, cy: 720, k: 3.0 }] },                     // E05 "Artık yanılmıyor. Ama yine de gidemiyor."
    { s0: 501.45, s1: 506.60, lens: [{ from: 0, cx: 1120, cy: 560, k: 1.55 }] },                   // F11 "Peki bilmek… yeter mi? Cevabını yorumlara yaz."
  ];
  const SON = 1.6; // kapanış kartı (son karede durur)
  let acc = 0;
  for (const K of KESIT) { K.t0 = acc; acc += K.s1 - K.s0; }
  const DUR_S = acc + SON;
  window.SHORTS = { KESIT, DUR: DUR_S };

  function eslem(ts) { // Shorts zamanı → {film zamanı, kesit}
    for (const K of KESIT) if (ts < K.t0 + (K.s1 - K.s0)) return { t: K.s0 + Math.max(0, ts - K.t0), K };
    const K = KESIT[KESIT.length - 1]; return { t: K.s1 - 1e-3, K, son: ts - (K.t0 + K.s1 - K.s0) };
  }
  function mercek(K, t) { let L = K.lens[0]; for (const l of K.lens) if (t >= l.from) L = l; LENS.cx = L.cx; LENS.cy = L.cy; LENS.k = L.k; }

  // ── altyazı: kesitlerdeki sözcükler, Shorts zamanına; 3 sözcüklük ya da noktalamada biten öbekler ──
  const SOZ = [];
  for (const K of KESIT) for (const w of (window.WORDS || [])) if (w.s >= K.s0 - .02 && w.e <= K.s1 + .02) SOZ.push({ d: w.d, s: w.s - K.s0 + K.t0, e: w.e - K.s0 + K.t0 });
  const OBEK = []; let cur = [];
  for (const w of SOZ) {
    if (cur.length && w.s - cur[cur.length - 1].e > .45) { OBEK.push(cur); cur = []; }
    cur.push(w);
    const sonraki = SOZ[SOZ.indexOf(w) + 1], ek = sonraki && /^(mi|mı|mu|mü)[?.,]?$/i.test(sonraki.d); // soru eki tek kalmasın
    if (!ek && (cur.length >= 3 || /[.?!,:”]$/.test(w.d))) { OBEK.push(cur); cur = []; }
  }
  if (cur.length) OBEK.push(cur);
  for (let i = 0; i < OBEK.length; i++) { const o = OBEK[i]; o.a = o[0].s; o.b = Math.min(o[o.length - 1].e + .35, OBEK[i + 1] ? OBEK[i + 1][0].s : 1e9); }

  const KREM = '#F4E6C8', KIRMIZI = '#E0643A', GOLGE = 'rgba(8,4,2,.85)';
  const temiz = s => s.replace(/[“”"]/g, '').toLocaleUpperCase('tr');
  function yaz(ctx, s, x, y, px, col, align = 'center', font = 'Bebas Neue') {
    ctx.font = `400 ${px}px "${font}"`; ctx.textAlign = align; ctx.textBaseline = 'alphabetic';
    ctx.lineJoin = 'round'; ctx.lineWidth = px * .16; ctx.strokeStyle = GOLGE; ctx.strokeText(s, x, y);
    ctx.fillStyle = col; ctx.fillText(s, x, y);
  }
  function altyazi(ctx, ts) {
    if (ts < 3.2) return; // kanca yazısı ekrandayken aynı cümle altyazıda tekrarlanmaz
    const o = OBEK.find(o => ts >= o.a && ts < o.b); if (!o) return;
    const px = 104, y = 1330, gap = px * .28;
    ctx.font = `400 ${px}px "Bebas Neue"`;
    const ws = o.map(w => temiz(w.d)), wd = ws.map(s => ctx.measureText(s).width);
    let tot = wd.reduce((a, b) => a + b, 0) + gap * (ws.length - 1), sc = Math.min(1, 760 / tot); // sağ sütundaki düğmeler (x > 950) boş kalır
    ctx.save(); ctx.translate(520, y); ctx.scale(sc, sc);
    let x = -tot / 2;
    const giris = E.out3(clamp((ts - o.a) / .12));
    ctx.globalAlpha = giris; ctx.translate(0, (1 - giris) * 18);
    o.forEach((w, i) => { const on = ts >= w.s && ts < Math.max(w.e, w.s + .12); yaz(ctx, ws[i], x, 0, px, on ? KIRMIZI : KREM, 'left'); x += wd[i] + gap; });
    ctx.restore();
  }
  function kanca(ctx, ts) { // ilk 2,8 sn: kapağın sorusu, ilk karede tam görünür (giriş animasyonu yok)
    if (ts > 3.2) return;
    const a = 1 - clamp((ts - 2.8) / .4);
    ctx.save(); ctx.globalAlpha = a;
    const g = ctx.createLinearGradient(0, 0, 0, 640); g.addColorStop(0, 'rgba(6,3,2,.78)'); g.addColorStop(.75, 'rgba(6,3,2,.45)'); g.addColorStop(1, 'rgba(6,3,2,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, 1080, 640);
    yaz(ctx, 'BUGÜN KENDİNE', 540, 300, 150, KREM);
    yaz(ctx, 'KAÇ KEZ BAKTIN?', 540, 460, 150, KIRMIZI);
    ctx.restore();
  }
  function kapanis(ctx, son) {
    const a = E.out3(clamp(son / .35));
    ctx.save(); ctx.globalAlpha = a * .72; ctx.fillStyle = '#060302'; ctx.fillRect(0, 0, 1080, 1920); ctx.globalAlpha = a;
    yaz(ctx, 'BİLMEK', 540, 760, 190, KREM);
    yaz(ctx, 'YETER Mİ?', 540, 950, 190, KIRMIZI);
    yaz(ctx, 'Narkissos ve Eko · tam hikâye kanalda', 540, 1100, 46, KREM, 'center', 'Cormorant Garamond');
    ctx.restore();
  }
  window.renderShort = (ts, mb = 1) => {
    const m = eslem(ts); mercek(m.K, m.t);
    const cv = renderAt(m.t, mb), c = cv.getContext('2d');
    c.save(); c.setTransform(RS, 0, 0, RS, 0, 0);
    if (m.son != null) kapanis(c, m.son); else { kanca(c, ts); altyazi(c, ts); }
    c.restore();
    return cv;
  };
  window.lensAt = (t, cx, cy, k) => { LENS.cx = cx; LENS.cy = cy; LENS.k = k; return renderAt(t, 1); };
})();
