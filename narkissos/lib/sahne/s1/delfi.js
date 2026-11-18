// DELFI seti, SAHİP-1: P011, P012. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Tanrı figürü, sunak, tapınan kalabalık yok. Yazıt metni planlar.json'dan: ΓΝΩΘΙ ΣΕΑΥΤΟΝ (taş) · KENDİNİ TANI.
'use strict';
(() => {
  const S1 = window.S1;
  const YAZIT = 'ΓΝΩΘΙ ΣΕΑΥΤΟΝ', TR = 'KENDİNİ TANI';
  // taş levha (stel): x merkez, gy taban, w, h
  const stel = (ctx, x, gy, w, h, o = {}) => {
    ctx.save(); ctx.beginPath(); ctx.moveTo(x - w / 2, gy); ctx.lineTo(x - w / 2 + 6, gy - h); ctx.lineTo(x + w / 2 - 6, gy - h); ctx.lineTo(x + w / 2, gy); ctx.closePath();
    ctx.fillStyle = o.fill || '#B9653A'; ctx.fill(); ctx.lineWidth = o.lw || 4; ctx.strokeStyle = C.ink; ctx.stroke();
    ctx.fillStyle = 'rgba(40,18,9,.18)'; for (let i = 0; i < 26; i++) { ctx.beginPath(); ctx.arc(x - w / 2 + hash(i * 1.3) * w, gy - hash(i * 2.9) * h, 2 + hash(i * 4.1) * 5 * (o.k || 1), 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  // ---- P011 · geniş · B03: Delfi; dağ yamacında Dor sütunlu tapınak, girişte taş. 'yazılı'da kamera taşa kayar; harfler henüz boş çizgi ----
  plan('P011', (ctx, st) => {
    const t = st.t, tY = PE('P011', 0), gy = 800;
    baseT(ctx); glaze(ctx, 1100, 700, 1400, 'rgba(120,50,24,.45)');
    const u = ramp(t, tY - .2, st.end, E.io2);
    camAt(ctx, lerp(900, 1270, u) + 25 * E.sine(st.p), lerp(540, 600, u), lerp(1.0, 1.1, u));
    crag(ctx, [[-700, gy], [-300, 330], [200, 210], [520, 380], [760, 520], [1500, 470], [1900, 250], [2500, 380], [2700, gy]], { fill: '#43200F', seed: 12, wob: 14, strata: 6, lobes: 5 });
    groundBand(ctx, gy, -3000, 6000, { h: 1400, fill: '#5A2C16' });
    // teras ve tapınak (kil, kazıma çizgiler)
    ctx.save(); ctx.fillStyle = '#6E3A1F'; ctx.fillRect(560, gy - 36, 760, 36); ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.strokeRect(560, gy - 36, 760, 36); ctx.restore();
    temple(ctx, 940, gy - 36, 1.75, 6, PC.clayR, C.ink);
    vaseTree(ctx, 380, gy, 1.5, 21, t, { branches: 6 }); vaseTree(ctx, 1640, gy, 1.7, 23, t, { branches: 7 });
    for (let i = 0; i < 9; i++) grass(ctx, 100 + i * 230, gy + 2, 1.5, t, i + 41);
    // girişteki taş: boş satır çizgileri
    stel(ctx, 1380, gy, 120, 210);
    ctx.save(); ctx.strokeStyle = 'rgba(30,14,8,.55)'; ctx.lineWidth = 2; for (const yy of [gy - 170, gy - 130, gy - 90]) { ctx.beginPath(); ctx.moveTo(1336, yy); ctx.lineTo(1424, yy); ctx.stroke(); } ctx.restore();
  }, { over: (ctx, st) => kunye(ctx, 'Delfi, Apollon tapınağı', st.lt - .4, 99) });

  // ---- P012 · ayrıntı · B03@kendini · LEVHA: yazıtın yakını ve altındaki su birikintisi. 'kendini'de ΓΝΩΘΙ ΣΕΑΥΤΟΝ harf harf belirir, altında KENDİNİ TANI;
  //      'tersine'de Türkçe satırın suyun içindeki görüntüsü harf harf döner (ayna); 'ölüm'de halkalarla dağılır ----
  const WY = 640;
  plan('P012', (ctx, st) => {
    const t = st.t, tK = PE('P012', 0), tT = PE('P012', 1), tO = PE('P012', 2);
    baseT(ctx); glaze(ctx, 960, 700, 1300, 'rgba(120,50,24,.4)');
    camAt(ctx, 960, lerp(430, 590, ramp(t, st.at, st.end, E.io2)), 1.0);
    // taş yüzü
    stel(ctx, 960, WY - 8, 1480, 760, { lw: 6, k: 2 });
    const pG = ramp(t, tK, tK + 1.8, E.lin), pT = ramp(t, tK + 1.2, tK + 2.2, E.lin);
    // kazıma yazıt: koyu çizgi, altında açık kenar (oyuk)
    ctx.save(); ctx.translate(2, 3); dipintoYaz(ctx, YAZIT, 960, 230, 104, pG, { col: 'rgba(255,214,170,.35)', w: .1 }); ctx.restore();
    dipintoYaz(ctx, YAZIT, 960, 230, 104, pG, { col: '#2A140A', w: .1 });
    txtDipinto(ctx, TR, 960, 420, 74, pT, { col: '#2A140A', w: 700 });
    // su birikintisi (taşın dibinde)
    const pool = c => c.rect(-400, WY, 2800, 1000);
    ctx.save(); ctx.beginPath(); pool(ctx); ctx.fillStyle = '#060302'; ctx.fill(); ctx.restore();
    waterBody(ctx, pool, WY, t, { a: .18, seed: 21, n: 30, depth: 380, span: [0, 1920] });
    const rings = [{ x: 1010, y: WY + 60, t0: tO, A: 12, sq: .34, v: 320, lam: 46, k: .8, reach: 1300, life: 3, shear: 1.2 }, { x: 760, y: WY + 110, t0: tO + .25, A: 8, sq: .34, v: 300, lam: 40, k: .9, reach: 900, life: 2.6 }];
    const rA = ramp(t, tK + 1.6, tK + 2.6, E.io2);
    mirror(ctx, c => {
      stel(c, 960, WY - 8, 1480, 760, { lw: 6, k: 2 });
      // satırın görüntüsü: 'tersine'den önce dik okunur; sonra harfler tek tek döner (ayna)
      S1.yolYazi(c, TR, [[960 - 290, 420], [960 + 400, 420]], 1, { px: 74, col: '#2A140A', font: FONT.baslik(74, 700), ls: 74 * .12, rise: 0,
        flipY: (i, n) => -Math.cos(PI * ramp(t, tT + i * .12, tT + i * .12 + .45, E.io2)) });
    }, WY, pool, t, { a: .5 * rA, calm: 1.4, rings: t > tO ? rings : null });
    shoreLine(ctx, -400, WY, { x1: 2400, w: 3 });
  }, { post: { tex: .5 }, over: (ctx, st) => kunye(ctx, 'Delfi, Apollon tapınağı', st.lt - 2.4, 99) });
})();
