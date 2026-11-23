// Dekor (Frankenstein): boyalı cam slaytın sahne parçaları. ORTAK DOSYA: yalnız başkan değiştirir.
// Kurallar: pencere kayıtları haç kurmaz (yalnız dikey kayıt ya da kemer), ağaç kat kat sivri değil (Noel ağacı okunur), yuvarlak nesneye halka tarama yok.
'use strict';
const DK = (() => {
  const P = (g, pts, k = 1, kap = true) => { g.beginPath(); spline(g, pts, kap, k); };
  // dağ silsilesi: x0..x1, taban y, tepeler [[x, y], ...]; o.kar: tepelerde açık boya
  function daglar(R, x0, x1, taban, tepe, renk, o = {}) {
    const pts = [[x0, taban]]; for (const p of tepe) pts.push(p); pts.push([x1, taban]);
    R.yika(g => { g.moveTo(x0, taban + 400); for (const p of pts) g.lineTo(p[0], p[1]); g.lineTo(x1, taban + 400); g.closePath(); }, renk, { kay: 2, ...o });
    if (o.kar) for (const p of tepe) R.isikli(g => { g.moveTo(p[0], p[1]); g.lineTo(p[0] + 38, p[1] + 46); g.lineTo(p[0] + 12, p[1] + 38); g.lineTo(p[0] - 6, p[1] + 52); g.lineTo(p[0] - 30, p[1] + 40); g.closePath(); }, o.kar);
  }
  // ay: saydam disk (ışığın en parlak yeri) + çevresinde boya halesi; o.bulut: önünden geçen koyu bulut payı
  function ay(R, x, y, r, o = {}) {
    R.halka(x, y, r * .9, r * 4.2, [[0, 'rgba(255,240,200,1)'], [.35, 'rgba(210,200,170,1)'], [1, 'rgba(255,255,255,1)']], { a: .5 });
    R.isikli(g => g.arc(x, y, r, 0, TAU), o.renk || '#FFF7E2');
    R.yika(g => { g.arc(x - r * .25, y - r * .1, r * .32, 0, TAU); g.moveTo(x + r * .4, y + r * .3); g.arc(x + r * .3, y + r * .3, r * .18, 0, TAU); }, 'rgba(225,212,180,.55)', { kay: 0, firca: 0 });
  }
  // göl: dikey boya geçişi + ışık yansıma çizgileri (kazı); y0 kıyı çizgisi
  function gol(R, x0, x1, y0, y1, renk1, renk2, o = {}) {
    R.gok(x0, y0, x1, y1, [[0, renk1], [1, renk2]], { firca: .8 });
    const t = o.t || 0, r = rng(o.tohum || 5);
    for (let i = 0; i < (o.n ?? 26); i++) { const yy = y0 + 10 + r() * (y1 - y0 - 20), xx = (o.yx ?? (x0 + x1) / 2) + (r() - .5) * (o.yw ?? 260) * (1 + (yy - y0) / 300), l = 20 + r() * 80;
      const kay = Math.sin(t * .8 + i) * 10; R.kazi([[xx - l / 2 + kay, yy], [xx + l / 2 + kay, yy]], 2 + r() * 2, o.yansima || 'rgba(255,236,190,.55)'); }
  }
  // çam ve kayın siluetleri: düzensiz, sarkık dallı (kat kat sivri koni değil)
  function cam(R, x, y, h, o = {}) {
    // düzensiz, sarkık dallı köknar: tek parça dış hat (katlar asimetrik, uçlar aşağı sarkar)
    const r = rng(o.tohum || Math.round(x * 7 + h)), sw = o.sal || 0, n = 8 + Math.floor(r() * 3), sol = [], sag = [];
    for (let i = 0; i < n; i++) {
      const u = i / n, yy = y - h * (.12 + u * .84), w = h * (.27 * Math.pow(1 - u, 1.1) + .03), sl = sw * (1 - u) * 5;
      const wl = w * (.65 + r() * .55), wr = w * (.65 + r() * .55), dr = h * (.035 + r() * .03);
      sol.push([x - wl * .35 + sl, yy - h * .05], [x - wl + sl, yy + dr], [x - wl * .55 + sl, yy + dr * .2]);
      sag.push([x + wr * .35 + sl, yy - h * .05], [x + wr + sl, yy + dr], [x + wr * .55 + sl, yy + dr * .2]);
    }
    R.kara(g => { g.moveTo(x - h * .025, y); for (let i = 0; i < sol.length; i++) g.lineTo(sol[i][0], sol[i][1]); g.lineTo(x + sw * 5, y - h); for (let i = sag.length - 1; i >= 0; i--) g.lineTo(sag[i][0], sag[i][1]); g.lineTo(x + h * .025, y); g.closePath(); });
  }
  function kayin(R, x, y, h, o = {}) {
    const r = rng(o.tohum || Math.round(x * 3 + h)), sw = o.sal || 0;
    R.cizgi([[x, y], [x + h * .02, y - h * .5], [x - h * .01, y - h * .75]], h * .05, { egri: true });
    for (let i = 0; i < 6; i++) { const a = -PI / 2 + (r() - .5) * 2.2, l = h * (.25 + r() * .25), sx = x + (r() - .5) * h * .03, sy = y - h * (.45 + r() * .3);
      R.cizgi([[sx, sy], [sx + Math.cos(a) * l * .6, sy + Math.sin(a) * l * .6], [sx + Math.cos(a + .3) * l + sw * 5, sy + Math.sin(a + .3) * l]], h * .018, { egri: true }); }
    for (let i = 0; i < 11; i++) { const cx = x + (r() - .5) * h * .7 + sw * 6, cy = y - h * (.62 + r() * .36), rr = h * (.1 + r() * .1);
      R.kara(g => { const pts = []; for (let k = 0; k < 9; k++) { const a = k / 9 * TAU, q = rr * (.7 + r() * .45); pts.push([cx + Math.cos(a) * q, cy + Math.sin(a) * q * .8]); } spline(g, pts, true); }); }
  }
  // villa (Diodati): iki katlı, önünde sütunlu balkon; pencereler dikey kayıtlı (haç değil); o.isik: pencere ışığı
  function villa(R, x, y, w, o = {}) {
    const h = w * .55, g = R.g, isik = o.isik || '#F6CF7A';
    R.kara(g => { g.rect(x - w / 2, y - h, w, h); g.moveTo(x - w / 2 - w * .04, y - h); g.lineTo(x, y - h - w * .16); g.lineTo(x + w / 2 + w * .04, y - h); g.closePath(); });
    // balkon sütunları (önde, ince): aralarındaki boşluk koyu mavi gece
    for (let i = 0; i < 5; i++) R.kara(g => g.rect(x - w * .4 + i * w * .2 - w * .015, y - h * .52, w * .03, h * .52));
    R.kara(g => g.rect(x - w * .46, y - h * .56, w * .92, h * .06));
    // pencereler: iki katta, kemerli, tek dikey kayıt
    const pen = (px, py, pw, ph, yan) => { if (!yan) return; R.isikli(g => { g.moveTo(px - pw / 2, py + ph / 2); g.lineTo(px - pw / 2, py - ph / 2 + pw / 2); g.arc(px, py - ph / 2 + pw / 2, pw / 2, PI, 0); g.lineTo(px + pw / 2, py + ph / 2); g.closePath(); }, isik);
      R.cizgi([[px, py - ph / 2 + 2], [px, py + ph / 2]], pw * .09); };
    const yan = o.yanan || [1, 0, 1, 1, 0, 1, 0, 1];
    for (let i = 0; i < 4; i++) { pen(x - w * .36 + i * w * .24, y - h * .78, w * .07, h * .2, yan[i]); pen(x - w * .36 + i * w * .24, y - h * .28, w * .07, h * .22, yan[4 + i]); }
  }
  // mum: şamdan + alev (saydam) + çevresine sıcak ışık (sonra katmanında); döndürdüğü ekran noktası alev
  function mum(R, x, y, s, o = {}) {
    const t = o.t || 0, tit = 1 + .08 * noise1(t * 7, 3) + .05 * Math.sin(t * 23);
    R.kara(g => { g.rect(x - s * .07, y - s * .5, s * .14, s * .5); g.ellipse(x, y, s * .3, s * .06, 0, 0, TAU); g.rect(x - s * .03, y - s * .05, s * .06, s * .07); });
    R.kara(g => { g.ellipse(x, y + s * .01, s * .2, s * .07, 0, 0, TAU); });
    if ((o.yan ?? 1) <= 0) return;
    const fy = y - s * .5, fh = s * .28 * tit * (o.yan ?? 1), sal = noise1(t * 3, 9) * s * .02;
    R.isikli(g => { g.moveTo(x - s * .045, fy - 1); g.quadraticCurveTo(x - s * .06, fy - fh * .55, x + sal, fy - fh); g.quadraticCurveTo(x + s * .06, fy - fh * .5, x + s * .045, fy - 1); g.closePath(); }, '#FFF4D0');
    R.yika(g => g.ellipse(x, fy - fh * .2, s * .035, fh * .22, 0, 0, TAU), '#E08A2A', { kay: 0, firca: 0 });
    const [ex, ey] = R.ekr(x, fy - fh * .5), sz = s * R._cam.s;
    R.sonra(ctx => { const gr = ctx.createRadialGradient(ex, ey, 0, ex, ey, sz * 2.6 * tit); gr.addColorStop(0, `rgba(255,190,90,${.32 * (o.yan ?? 1)})`); gr.addColorStop(1, 'rgba(255,150,60,0)'); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = gr; ctx.fillRect(ex - sz * 3, ey - sz * 3, sz * 6, sz * 6); });
    return [x, fy - fh * .5];
  }
  // ateş (köz ve odun): genişçe tabanlı, yana kıvrılan dil + kıvılcım (Lale dersi: tek simetrik alev mızrak okunur)
  function ates(R, x, y, s, o = {}) {
    const t = o.t || 0, r = rng(3);
    for (let i = 0; i < 4; i++) R.cizgi([[x - s * .5 + i * s * .1, y], [x + s * .5 - i * s * .15, y - s * .12 + i * s * .04]], s * .08);
    const dil = (dx, hh, ph) => { const k = noise1(t * 4 + ph, 7) * s * .12; R.isikli(g => { g.moveTo(x + dx - s * .22, y - s * .05); g.bezierCurveTo(x + dx - s * .26, y - hh * .5, x + dx + k, y - hh * .7, x + dx + s * .12 + k, y - hh); g.bezierCurveTo(x + dx + s * .04 + k, y - hh * .6, x + dx + s * .26, y - hh * .4, x + dx + s * .22, y - s * .05); g.closePath(); }, '#FFE9B0'); };
    dil(-s * .12, s * (.7 + .1 * Math.sin(t * 5)), 0); dil(s * .16, s * (.48 + .08 * Math.sin(t * 6 + 1)), 2); dil(-s * .32, s * .32, 4);
    R.yika(g => g.ellipse(x, y - s * .25, s * .45, s * .3, 0, 0, TAU), 'rgba(225,120,40,.85)', { kay: 0, firca: 0 });
    for (let i = 0; i < 7; i++) { const u = ((t * .7 + r()) % 1), kx = x + (r() - .5) * s * .6 + Math.sin(t * 2 + i) * s * .08, ky = y - s * .4 - u * s * 1.4; R.nokta(kx, ky, s * .018 * (1 - u), '#FFD890'); }
    const [ex, ey] = R.ekr(x, y - s * .3), sz = s * R._cam.s;
    R.sonra(ctx => { const gr = ctx.createRadialGradient(ex, ey, 0, ex, ey, sz * 2.8); gr.addColorStop(0, 'rgba(255,160,70,.32)'); gr.addColorStop(1, 'rgba(255,120,40,0)'); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = gr; ctx.fillRect(ex - sz * 3, ey - sz * 3, sz * 6, sz * 6); });
  }
  // yağmur: ekrana sabit eğik ince çizgiler (slaytın üstündeki ikinci hareketli cam gibi) — kaydırmalı slayt
  function yagmur(R, t, o = {}) {
    const r = rng(o.tohum || 9), n = o.n || 160, a = o.a ?? .32;
    R.sonra(ctx => { ctx.globalCompositeOperation = 'screen'; ctx.strokeStyle = `rgba(200,210,230,${a})`; ctx.lineWidth = 1.6; ctx.beginPath();
      for (let i = 0; i < n; i++) { const x0 = r() * 2200 - 100, sp = 900 + r() * 500, y0 = ((r() * 1300 + t * sp) % 1300) - 110, l = 30 + r() * 40; ctx.moveTo(x0 - y0 * .18, y0); ctx.lineTo(x0 - (y0 + l) * .18, y0 + l); } ctx.stroke(); });
  }
  // şimşek: gökte kırık ışık çizgisi + bütün slaytın parlaması; p 0..1 (çakış anından itibaren)
  function simsek(R, x, y0, y1, p, o = {}) {
    if (p < 0 || p > 1) return 0;
    const fl = p < .08 ? 1 : p < .18 ? .3 : p < .26 ? .9 : Math.max(0, 1 - (p - .26) / .74) * .5;
    const r = rng(o.tohum || 4), pts = [[x, y0]]; let xx = x; for (let i = 1; i <= 9; i++) { xx += (r() - .5) * 90; pts.push([xx, y0 + (y1 - y0) * i / 9]); }
    if (fl > .25) R.kazi(pts, 5, '#FFFFF4');
    return fl;
  }
  // pencere (oda içinden): kemersiz, iki kanatlı, yalnız dikey kayıt; arkası gece mavisi; kepenk aralığından ay ışığı
  function pencere(R, x, y, w, h, o = {}) {
    R.yika(g => g.rect(x - w / 2, y - h / 2, w, h), o.gece || '#5D7398', { firca: .9 });
    if (o.ay) { R.isikli(g => g.arc(x + w * .18, y - h * .22, w * .1, 0, TAU), '#FFF6DE'); }
    R.kara(g => { g.rect(x - w / 2 - 14, y - h / 2 - 14, w + 28, 14); g.rect(x - w / 2 - 14, y + h / 2, w + 28, 16); g.rect(x - w / 2 - 14, y - h / 2, 14, h); g.rect(x + w / 2, y - h / 2, 14, h); g.rect(x - 5, y - h / 2, 10, h); });
    if (o.kepenk != null) { const k = o.kepenk; R.kara(g => { g.rect(x - w / 2, y - h / 2, w / 2 * (1 - k), h); g.rect(x + w / 2 - w / 2 * (1 - k), y - h / 2, w / 2 * (1 - k), h); }); }
  }
  // yatak perdesi: tavandan sarkan ağır kumaş (boya + kıvrım çizgileri); a: aralanma (0 kapalı … 1 açık)
  function perde(R, x0, x1, ust, alt, renk, o = {}) {
    const n = o.kivrim || 7, w = x1 - x0, t = o.t || 0;
    R.yika(g => { g.moveTo(x0, ust); g.lineTo(x1, ust); for (let i = n; i >= 0; i--) { const u = i / n; g.lineTo(x0 + w * u + Math.sin(i * 1.9 + t) * 6, alt + (i % 2) * 14); } g.closePath(); }, renk, { firca: 1, fa: PI / 2 });
    for (let i = 1; i < n; i++) { const xx = x0 + w * i / n; R.cizgi([[xx, ust + 10], [xx + Math.sin(i + t) * 8, (ust + alt) / 2], [xx + Math.sin(i * 1.9 + t) * 6, alt]], 3.2, { egri: true, a: .55 }); }
  }
  // ---- eşyalar ----
  function masa(R, x, y, w, o = {}) { R.kara(g => { g.rect(x - w / 2, y, w, 22); g.rect(x - w / 2 + 20, y + 18, 18, o.h || 300); g.rect(x + w / 2 - 38, y + 18, 18, o.h || 300); }); }
  function sandalye(R, x, y, s, f = 1) { R.kara(g => { g.rect(x - 60 * s * f - (f < 0 ? 0 : 14 * s), y - 140 * s, 14 * s, 290 * s); g.rect(x - 60 * s, y, 120 * s, 14 * s); g.rect(x - 56 * s, y, 12 * s, 150 * s); g.rect(x + 44 * s, y, 12 * s, 150 * s); }); }
  // kitap ya da defter (açık): sayfalar saydam krem, satırlar ince
  function defter(R, x, y, w, o = {}) { const h = w * .62; R.kara(g => g.rect(x - w / 2 - 6, y - 4, w + 12, 8));
    R.isikli(g => { g.moveTo(x - w / 2, y); g.quadraticCurveTo(x - w / 4, y - h * .12, x, y - 2); g.quadraticCurveTo(x + w / 4, y - h * .12, x + w / 2, y); g.lineTo(x + w / 2, y - h * .06); g.lineTo(x - w / 2, y - h * .06); g.closePath(); }, o.renk || '#EFE4C6'); }
  // beşik (boş ya da örtülü): sallanma a
  function besik(R, x, y, s, o = {}) { const a = o.a || 0; R.g.save(); R.g.translate(x, y); R.g.rotate(a);
    R.kara(g => { g.moveTo(-90 * s, -60 * s); g.lineTo(90 * s, -60 * s); g.lineTo(80 * s, 0); g.lineTo(-80 * s, 0); g.closePath(); g.moveTo(-100 * s, 0); g.quadraticCurveTo(0, 50 * s, 100 * s, 0); g.lineTo(100 * s, 10 * s); g.quadraticCurveTo(0, 60 * s, -100 * s, 10 * s); g.closePath(); });
    R.kara(g => { g.moveTo(-90 * s, -60 * s); g.quadraticCurveTo(-100 * s, -130 * s, -40 * s, -130 * s); g.lineTo(-40 * s, -110 * s); g.quadraticCurveTo(-78 * s, -108 * s, -72 * s, -60 * s); g.closePath(); });
    if (o.ortu) R.yika(g => { g.moveTo(-70 * s, -60 * s); g.quadraticCurveTo(0, -84 * s, 70 * s, -60 * s); g.closePath(); }, o.ortu, { kay: 1 });
    R.g.restore(); }
  // oval çerçeveli siluet portre (1790'ların siluet portresi): kadın profili, saçları başlıklı
  function portre(R, x, y, s, o = {}) {
    R.yika(g => g.ellipse(x, y, 120 * s, 150 * s, 0, 0, TAU), o.zemin || '#E9DFC6', { kay: 0 });
    const g = R.g; g.save(); g.beginPath(); g.ellipse(x, y, 120 * s, 150 * s, 0, 0, TAU); g.clip();
    const b = 900 * s, k = b * .93 / 100;   // baş ovalin ortasında
    FIG.kisi(R, x - 10 * s, y + 92.6 * k - 4 * s, b, { tip: o.tip || 'mary', f: o.f || 1, kolO: [0, 0], kolA: [0, 0] });
    g.restore();
    g.save(); g.strokeStyle = R.KARA; g.lineWidth = 16 * s; g.beginPath(); g.ellipse(x, y, 128 * s, 158 * s, 0, 0, TAU); g.stroke(); g.restore();
  }
  // yanardağ (Tambora): koni + kül bulutu (p: patlamanın gelişimi 0..1)
  function yanardag(R, x, y, s, p, t = 0) {
    R.kara(g => { g.moveTo(x - 520 * s, y); g.lineTo(x - 90 * s, y - 300 * s); g.lineTo(x + 90 * s, y - 300 * s); g.lineTo(x + 520 * s, y); g.closePath(); });
    if (p <= 0) return;
    for (let i = 0; i < 14; i++) { const u = i / 13, rr = (60 + u * 260) * s * (.4 + .6 * p), yy = y - 300 * s - u * 900 * s * p, xx = x + Math.sin(i * 1.7 + t * .3) * 80 * s * u + u * 160 * s * p;
      R.yika(g => g.ellipse(xx, yy, rr * 1.3, rr, 0, 0, TAU), `rgba(${110 - u * 30},${90 - u * 30},${80 - u * 20},.85)`, { kay: 0 }); }
    R.isikli(g => { g.moveTo(x - 60 * s, y - 300 * s); g.lineTo(x, y - 360 * s - 60 * s * p); g.lineTo(x + 60 * s, y - 300 * s); g.closePath(); }, '#FFC870');
    R.yika(g => g.ellipse(x, y - 320 * s, 110 * s, 60 * s, 0, 0, TAU), 'rgba(230,110,40,.9)', { kay: 0, firca: 0 });
  }
  return { daglar, ay, gol, cam, kayin, villa, mum, ates, yagmur, simsek, pencere, perde, masa, sandalye, defter, besik, portre, yanardag, P };
})();
