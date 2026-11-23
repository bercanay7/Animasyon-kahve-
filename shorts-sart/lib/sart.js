// Şart Shorts'u: ortak çalışma zamanı (seri: shorts-sart/README.md). ORTAK DOSYA: yalnız başkan değiştirir.
// İki kip:
//   mod 'film'  : filmin planları film zamanında çizilir; Shorts zamanı → film zamanı kesit kesit (KURGU.kesit[i].v, yoksa a0).
//                 Mercek (LENS, motorun core_dikey.js'i) kesit içinde anahtar karelerle: lens: [[u, cx, cy, k], ...] (u: kesit içi sn).
//   mod 'yerli' : dikey için yazılmış planlar Shorts zamanında çizilir (renderAt(ts)); mercek yok.
// Üstüne: kanca yazısı (ilk karede tam görünür, giriş animasyonu yok), sözcük sözcük altyazı, isteğe bağlı kapanış.
// Güvenli alan (Shorts arayüzü): üst 0–200 arama çubuğu, sağ sütun x > 950 (beğen/yorum), alt y > 1480 (başlık, kanal adı). Yazılar x 140–940, y 220–1440.
'use strict';
(() => {
  const K = window.KURGU, Z = window.SZ;
  const KES = Z.KESIT.map((z, i) => ({ ...K.kesit[i], ...z }));
  const DUR = Z.DUR;
  window.SHORTS = { KES, DUR };

  function eslem(ts) {
    for (const k of KES) if (ts < k.t1) return { k, u: Math.max(0, ts - k.t0) };
    const k = KES[KES.length - 1]; return { k, u: ts - k.t0 };
  }
  function filmZamani(k, u) { const v0 = k.v ?? k.a0 ?? 0; return v0 + u * (k.hiz ?? 1); }
  function mercek(k, u) {
    const L = k.lens || [[0, 960, 540, 1.78]];
    const keys = L.map(([t, cx, cy, kk]) => [t, { cx, cy, k: kk }, E.sine]);
    const m = kf(u, keys); LENS.cx = m.cx; LENS.cy = m.cy; LENS.k = m.k;
  }

  // ── altyazı öbekleri: ≤ 3 sözcük ya da noktalamada biter; soru eki tek kalmaz ──
  const SOZ = Z.WORDS.filter(w => w.d);
  const OBEK = []; let cur = [];
  SOZ.forEach((w, i) => {
    if (cur.length && w.s - cur[cur.length - 1].e > .45) { OBEK.push(cur); cur = []; }
    cur.push(w);
    const ek = SOZ[i + 1] && /^(mi|mı|mu|mü)[?.,]?$/i.test(SOZ[i + 1].d);
    if (!ek && (cur.length >= (K.obek || 3) || /[.?!,:”]$/.test(w.d))) { OBEK.push(cur); cur = []; }
  });
  if (cur.length) OBEK.push(cur);
  OBEK.forEach((o, i) => { o.a = o[0].s; o.b = Math.min(o[o.length - 1].e + .35, OBEK[i + 1] ? OBEK[i + 1][0].s : 1e9); });
  window.SHORTS.OBEK = OBEK;

  const R = K.renk || {}, KREM = R.krem || '#F4E6C8', VURGU = R.vurgu || '#E0643A', GOLGE = R.golge || 'rgba(8,4,2,.85)';
  const buyuk = s => s.replace(/[“”"]/g, '').toLocaleUpperCase('tr');
  function yaz(ctx, s, x, y, px, col, align = 'center', font = 'Bebas Neue', w = 400) {
    ctx.font = `${w} ${px}px "${font}"`; ctx.textAlign = align; ctx.textBaseline = 'alphabetic';
    ctx.lineJoin = 'round'; ctx.lineWidth = px * .16; ctx.strokeStyle = GOLGE; ctx.strokeText(s, x, y);
    ctx.fillStyle = col; ctx.fillText(s, x, y);
  }
  window.SART_YAZ = yaz;
  // ara yazılar: KURGU.yazilar = [{t0, t1, satir: [[metin, renk, px], ...], y, ara, altyok (sn; bu zamana dek altyazı gizli)}]
  // Kancanın tipografisiyle aynı: şart Shorts içinde geri döndüğünde ilk kareyle aynı görünür (döngü ve hatırlatma).
  function arayazi(ctx, ts) {
    for (const Y of (K.yazilar || [])) {
      if (ts < Y.t0 || ts > Y.t1) continue;
      const a = E.out3(clamp((ts - Y.t0) / .15)) * (1 - E.in2(clamp((ts - (Y.t1 - .3)) / .3)));
      ctx.save(); ctx.globalAlpha = a; let y = Y.y ?? 300;
      Y.satir.forEach(([s, c, px], i) => { if (i) y += px * (Y.ara ?? .9); yaz(ctx, s, 540, y, px, c === 'vurgu' ? VURGU : KREM); });
      ctx.restore();
    }
  }
  const altGizli = ts => (K.yazilar || []).some(Y => ts >= Y.t0 && ts < (Y.altyok ?? -1));
  function altyazi(ctx, ts) {
    const A = K.altyazi || {};
    if (ts < (A.bas ?? 0) || altGizli(ts)) return;
    const o = OBEK.find(o => ts >= o.a && ts < o.b); if (!o) return;
    const k = eslem(ts).k; const px = A.px || 100, y = k.altY ?? A.y ?? 1300, gap = px * .28;
    ctx.font = `400 ${px}px "Bebas Neue"`;
    const ws = o.map(w => buyuk(w.d)), wd = ws.map(s => ctx.measureText(s).width);
    const tot = wd.reduce((a, b) => a + b, 0) + gap * (ws.length - 1), sc = Math.min(1, 780 / tot);
    ctx.save(); ctx.translate(540, y); ctx.scale(sc, sc);
    let x = -tot / 2;
    const giris = E.out3(clamp((ts - o.a) / .12));
    ctx.globalAlpha = giris; ctx.translate(0, (1 - giris) * 16);
    o.forEach((w, i) => { const on = ts >= w.s && ts < Math.max(w.e, w.s + .12); yaz(ctx, ws[i], x, 0, px, on ? VURGU : KREM, 'left'); x += wd[i] + gap; });
    ctx.restore();
  }
  // kanca: KURGU.kanca = {satir: [[metin, 'krem'|'vurgu', px], ...], y (ilk satırın taban çizgisi), ara (satır arası çarpanı), bitis (sn), panel (üst karartma yüksekliği)}
  function kanca(ctx, ts) {
    const H = K.kanca; if (!H) return;
    const b = H.bitis ?? 3; if (ts > b + .4) return;
    const a = 1 - clamp((ts - b) / .4);
    ctx.save(); ctx.globalAlpha = a;
    if (H.panel) {
      const g = ctx.createLinearGradient(0, 0, 0, H.panel); g.addColorStop(0, 'rgba(6,3,2,.72)'); g.addColorStop(.7, 'rgba(6,3,2,.4)'); g.addColorStop(1, 'rgba(6,3,2,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, 1080, H.panel);
    }
    let y = H.y ?? 300;
    H.satir.forEach(([s, c, px], i) => { if (i) y += px * (H.ara ?? 1.0); yaz(ctx, s, 540, y, px, c === 'vurgu' ? VURGU : KREM); });
    ctx.restore();
  }
  // isteğe bağlı kapanış yazısı: KURGU.kapanis = {satir: [...], t0 (sn), y}
  function kapanis(ctx, ts) {
    const H = K.kapanis; if (!H || ts < H.t0) return;
    const a = E.out3(clamp((ts - H.t0) / .35));
    ctx.save(); ctx.globalAlpha = a;
    let y = H.y ?? 800;
    H.satir.forEach(([s, c, px, font], i) => { if (i) y += px * (H.ara ?? 1.0); yaz(ctx, s, 540, y, px, c === 'vurgu' ? VURGU : KREM, 'center', font || 'Bebas Neue'); });
    ctx.restore();
  }
  window.renderShort = (ts, mb = 1) => {
    let cv;
    if (K.mod === 'film') { const { k, u } = eslem(ts); mercek(k, u); cv = renderAt(filmZamani(k, u), mb); }
    else cv = renderAt(ts, mb);
    const c = cv.getContext('2d');
    c.save(); c.setTransform(RS, 0, 0, RS, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.filter = 'none';
    if (!window.SART_YAZISIZ) { kanca(c, ts); arayazi(c, ts); altyazi(c, ts); kapanis(c, ts); }
    c.restore();
    return cv;
  };
})();
