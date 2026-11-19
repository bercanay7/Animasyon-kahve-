// DAG seti, SAHİP-1: P029, P030, P031. Bu dosyayı yalnız bu sahip değiştirir.
// Eko yüzünü YALNIZ yapraklı bir dalla örter (başörtüsü, çarşaf, baştan ayağa örtü yok). Erime renk ve biçimle: kemik, iskelet, zayıflamış beden çizimi yok.
// Taşa dönüş anlatıda "söylerler": belirsiz bırakılır (kaya biçimi ve soluk bir profil çizgisi; ses dalgası kalır).
'use strict';
(() => {
  const S1 = window.S1;
  // Eko: ayakta (sit 0) → girişte oturur (sit 1); ortu (0..1) dal yüzüne kalkar
  const ekoDal = (ctx, t, o) => {
    const { x, gy, s } = o, sit = o.sit || 0, ortu = o.ortu || 0, dir = 1;
    const py = lerp(gy - 44.5 * s, gy - 30 * s, sit);
    const fN = [lerp(x + 3 * s, x + 20 * s, sit), gy - 3 * s, 0], fF = [lerp(x - 3 * s, x + 16 * s, sit), gy - 3 * s, 0];
    const f0 = { x, y: py, s, dir, sty: S1.RFF, lk: S1.LK_EKO, seed: 71, stripe: .45, idle: .6, p: { torso: .05 * sit, neck: .12 + .1 * ortu, head: .1 + .1 * ortu, handN: 'fist', shF: .2, elF: .5 + .4 * sit }, ik: { fN, fF } };
    const { J, M } = joints(ctx, f0);
    const yuz = headPt(ctx, J, M, [8.5, -5.5]), kalca = jointPt(ctx, M, add(J.shoulder, [5, 20]));
    const h = lerp2(kalca, yuz, E.io2(ortu));
    const f = { ...f0, ik: { ...f0.ik, hN: h }, alpha: o.alpha };
    figure(ctx, f);
    // Fable tur 1: oturunca etek "saydam" okunuyordu (bacaklar eteğin içinden görünüyor) → otururken kucağa ve dizden aşağı dökülen dolu etek (ayaklar dışarıda)
    const ea = clamp((sit - .25) / .45);
    if (ea > 0) { const J2 = joints(ctx, f).J, M2 = joints(ctx, f).M, P = q => jointPt(ctx, M2, q);
      const H = P(J2.hip), K = P(J2.LN.knee), A = P(J2.LN.ank), K2 = P(J2.LF.knee), Kx = Math.max(K[0], K2[0]), Ky = Math.min(K[1], K2[1]), u = s;
      // kucak → dizin önü (yuvarlak) → dizden etek ucuna dökülen kumaş; dizle oturak arasında asılı kumaş (vazo resminde oturan kadın)
      ctx.save(); ctx.globalAlpha *= ea * (o.alpha ?? 1); ctx.beginPath();
      ctx.moveTo(H[0] - 9 * u, H[1] - 6 * u);
      ctx.quadraticCurveTo(H[0] + 2 * u, H[1] - 9.5 * u, Kx - 2 * u, Ky - 5.2 * u);
      ctx.quadraticCurveTo(Kx + 5.5 * u, Ky - 4.8 * u, Kx + 5.4 * u, Ky + 1.5 * u);
      ctx.quadraticCurveTo(A[0] + 4.6 * u, lerp(Ky, A[1], .6), A[0] + 6.2 * u, A[1] - 2.4 * u);
      ctx.quadraticCurveTo(A[0], A[1] - 1.2 * u, A[0] - 7.5 * u, A[1] - 2.2 * u);
      ctx.quadraticCurveTo(lerp(H[0], A[0], .5), lerp(H[1], A[1], .55), H[0] - 2 * u, H[1] + 8 * u);
      ctx.quadraticCurveTo(H[0] - 8 * u, H[1] + 8 * u, H[0] - 10 * u, H[1] + 3 * u);
      ctx.closePath();
      ctx.fillStyle = S1.LK_EKO.robeCol; ctx.fill(); ctx.lineJoin = 'round'; ctx.lineWidth = .45 * u; ctx.strokeStyle = C.ink; ctx.stroke();
      // kıvrımlar: dizden etek ucuna, uyluk üstünde iki uzun kıvrım; etek ucunda kırmızı bant
      ctx.lineWidth = .26 * u; ctx.lineCap = 'round';
      for (let i = 0; i < 5; i++) { const v = (i + .5) / 5; ctx.beginPath(); ctx.moveTo(lerp(Kx - 4 * u, Kx + 4 * u, v), Ky + 1.5 * u); ctx.quadraticCurveTo(lerp(Kx - 5 * u, Kx + 4.6 * u, v), lerp(Ky, A[1], .55), lerp(A[0] - 6.2 * u, A[0] + 4.8 * u, v), A[1] - 3.6 * u); ctx.stroke(); }
      for (let i = 0; i < 2; i++) { ctx.beginPath(); ctx.moveTo(H[0] - 2 * u, H[1] - (3 - 3 * i) * u); ctx.quadraticCurveTo(lerp(H[0], Kx, .5), lerp(H[1], Ky, .5) - (4 - 2.5 * i) * u, Kx - 3 * u, Ky - (2 - 2 * i) * u); ctx.stroke(); }
      ctx.lineWidth = 1.3 * u; ctx.strokeStyle = C.red; ctx.beginPath(); ctx.moveTo(A[0] - 6.8 * u, A[1] - 3.4 * u); ctx.quadraticCurveTo(A[0], A[1] - 2.6 * u, A[0] + 5.6 * u, A[1] - 3.6 * u); ctx.stroke(); ctx.restore(); }
    // yapraklı dal: elden yukarı; örtünce yaprak kümesi yüzün önünde (yalnız yüz)
    S1.dal(ctx, h[0] - 4, h[1] + 6, s / 6.2, lerp(-1.0, -1.62, ortu), t, 77, { L: 130, leaf: 44, n: 8, bend: .6 });
    return { f, J, M, yuz };
  };
  const dagZemin = (ctx, t, gy) => {
    glaze(ctx, 1100, 900, 1300, 'rgba(110,46,22,.4)');
    crag(ctx, [[-800, gy], [-400, 380], [100, 300], [500, 460], [800, gy]], { fill: '#3A1B0D', seed: 3, wob: 14, strata: 4, lobes: 3 });
    groundBand(ctx, gy, -3000, 6000, { h: 1400 });
  };
  // mağara kayası ve ağzı (sağda)
  const magara = (ctx, gy, cx = 1500) => {
    crag(ctx, [[cx - 330, gy + 4], [cx - 260, 300], [cx + 40, 120], [cx + 500, 160], [cx + 900, 420], [cx + 1000, gy + 4]], { fill: '#5A2C16', seed: 11, wob: 12, strata: 5, lobes: 4 });
    ctx.save(); ctx.beginPath(); ctx.moveTo(cx - 140, gy + 2); ctx.bezierCurveTo(cx - 150, gy - 300, cx + 210, gy - 330, cx + 220, gy + 2); ctx.closePath(); ctx.fillStyle = '#080402'; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = C.ink; ctx.stroke(); ctx.restore();
  };

  // ---- P029 · orta · C10: reddedilen Eko yüzünü yapraklı bir dalla örter ve mağaraya çekilir; 'yapraklarla'da dal yüze kalkar, 'mağaralarda'da kamera mağara ağzına kayar, Eko girişte oturur; 'büyür'de gölge büyür ----
  plan('P029', (ctx, st) => {
    const t = st.t, tY = PE('P029', 0), tM = PE('P029', 1), tB = PE('P029', 2), gy = 900, s = 7;
    baseT(ctx);
    const kay = ramp(t, tM - .1, tM + 1.6, E.io2);
    camAt(ctx, lerp(1000, 1300, kay) + 20 * E.sine(st.p), 520, lerp(1.0, 1.06, E.sine(st.p)));
    dagZemin(ctx, t, gy);
    magara(ctx, gy);
    const ortu = ramp(t, tY - .1, tY + .7, E.io2);
    const sit = ramp(t, tM + .4, tM + 1.8, E.io2), x = lerp(1060, 1230, ramp(t, tM - .2, tM + .9, E.io2)) - 140 * (1 - ramp(t, st.at - .7, tY, E.out2));
    ekoDal(ctx, t, { x, gy, s, sit, ortu });
    // mağaranın gölgesi büyür ('büyür')
    const g = ramp(t, tB - 2.2, st.end + .3, E.io2);
    if (g > 0) { ctx.save(); const gr = ctx.createRadialGradient(1540, gy - 120, 40, 1540, gy - 120, lerp(200, 620, g)); gr.addColorStop(0, 'rgba(6,3,2,.85)'); gr.addColorStop(.7, `rgba(6,3,2,${(.6 * g).toFixed(3)})`); gr.addColorStop(1, 'rgba(6,3,2,0)');
      ctx.fillStyle = gr; ctx.fillRect(700, 0, 1800, 1200); ctx.restore(); }
  }, { tr: trOf('P029') });

  // ---- P030 · yakın · C11: Eko'nun bedeni erir: 'eritir'de renk solar; 'kemikleri'nde yerinde kaya biçimi belirir; 'taşa'da kaya tamamlanır, yüzünde soluk bir profil çizgisi. Ses kalır ----
  plan('P030', (ctx, st) => {
    const t = st.t, tE = PE('P030', 0), tK = PE('P030', 1), tT = PE('P030', 2), gy = 1180, s = 14;
    baseT(ctx); glaze(ctx, 900, 900, 1200, 'rgba(100,42,20,.4)');
    camAt(ctx, 1010, lerp(450, 690, ramp(t, st.at, st.end, E.lin)), lerp(1.0, 1.08, ramp(t, st.at, st.end, E.lin)));
    ctx.save(); ctx.beginPath(); ctx.moveTo(1500, 1400); ctx.bezierCurveTo(1520, 500, 1800, 120, 2400, 100); ctx.lineTo(2400, 1400); ctx.closePath(); ctx.fillStyle = '#080402'; ctx.fill(); ctx.restore();
    const k1 = ramp(t, tE - .1, tK, E.io2), k2 = ramp(t, tK - .2, tT + .2, E.io2), k3 = ramp(t, tT, tT + 1.0, E.io2);
    // beden: ayrı katmanda; kaya rengine solar
    const L = layer('s1eri'); L.setTransform(ctx.getTransform());
    const r = ekoDal(L, t, { x: 800, gy, s, sit: 1, ortu: 1 });
    L.globalCompositeOperation = 'source-atop'; L.fillStyle = `rgba(90,44,22,${(.85 * k1).toFixed(3)})`; L.fillRect(-1000, -1000, 4000, 4000); L.globalCompositeOperation = 'source-over';
    // kaya: bedenin yerinde oturan bir kütle (belirsiz biçim)
    if (k2 > 0) { ctx.save(); ctx.globalAlpha = k2;
      crag(ctx, [[560, gy + 6], [600, 620], [760, 420], [930, 300], [1080, 330], [1180, 520], [1230, 760], [1300, gy + 6]], { fill: '#5A2C16', seed: 19, wob: 12, strata: 4, lobes: 3 }); ctx.restore(); }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1 - k2; ctx.drawImage(LY.s1eri, 0, 0); ctx.restore();
    // kayanın yüzünde soluk profil çizgisi (alın-burun-dudak)
    if (k3 > 0) { const y0 = r.yuz[1] - 90; ctx.save(); ctx.globalAlpha = .38 * k3; ctx.strokeStyle = '#E39A62'; ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.beginPath();
      ctx.moveTo(r.yuz[0] - 70, y0 - 40); ctx.quadraticCurveTo(r.yuz[0] - 20, y0, r.yuz[0] - 10, y0 + 50); ctx.lineTo(r.yuz[0] + 14, y0 + 92); ctx.lineTo(r.yuz[0] - 6, y0 + 100); ctx.quadraticCurveTo(r.yuz[0] + 4, y0 + 120, r.yuz[0] - 8, y0 + 132); ctx.quadraticCurveTo(r.yuz[0] - 2, y0 + 150, r.yuz[0] - 22, y0 + 170); ctx.stroke(); ctx.restore(); }
    // kayadan yükselen toz (taşa dönüşün belirsizliği; hareket)
    if (k2 > 0) motesN(ctx, t, 40, 33, 920, 700, 420, 380, .6 * k2, '230,170,120');
    // ses dalgası: ağzın önünden sağa yaylar (başı çevrelemez), beden solduktan sonra da sürer
    const sx = r.yuz[0] + 60, sy = r.yuz[1] + 40;
    ctx.save(); ctx.strokeStyle = S1.KIRMIZI; ctx.lineCap = 'round';
    for (let i = 0; i < 4; i++) { const u = ((t - tE) * .55 + i / 4) % 1; if (t < tE - .3) continue; const R = 60 + u * 360;
      ctx.globalAlpha = .85 * Math.sin(u * PI) * ramp(t, tE - .3, tE + .5, E.lin); ctx.lineWidth = 5 - 3 * u; ctx.beginPath(); ctx.arc(sx, sy, R, -.42, .42); ctx.stroke(); }
    ctx.restore();
  });

  // ---- P031 · geniş · C11@ise-0.25: dağ sırası, kimse yok; yamaçlarda dipinto yazılar solarak belirip söner. 'görünmez'de kamera vadide kayar, 'herkes'te yamaçtan yamaca yankılanır, 'duyar'da son yazı söner ----
  const YAZ = [['BURADA', 420, 470, 52], ['GEL', 1100, 380, 46], ['BULUŞALIM', 1560, 520, 48], ['OLURSUN', 820, 600, 44], ['BURADA', 1980, 430, 40]];
  plan('P031', (ctx, st) => {
    const t = st.t, tG = PE('P031', 0), tH = PE('P031', 1), tD = PE('P031', 2);
    baseT(ctx); glaze(ctx, 1100, 800, 1400, 'rgba(110,46,22,.38)');
    glow(ctx, 1100, 330, 1300, 'rgba(230,140,80,.32)'); // Fable tur 1: çok karanlıktı → dağların ardında sıcak gök, yamaçlar bir değer açık
    camAt(ctx, lerp(720, 1280, ramp(t, st.at, st.end, E.sine)), 540, lerp(1.0, 1.05, ramp(t, st.at, st.end, E.sine)));
    crag(ctx, [[-800, 900], [-300, 420], [300, 330], [700, 470], [1200, 300], [1700, 380], [2300, 290], [2900, 520], [2900, 900]], { fill: '#4E2614', seed: 41, wob: 16, strata: 3, lobes: 3 });
    crag(ctx, [[-800, 900], [-200, 560], [400, 520], [900, 640], [1400, 540], [2000, 600], [2700, 520], [2900, 900]], { fill: '#6A3319', seed: 43, wob: 14, strata: 3, lobes: 3 });
    crag(ctx, [[-800, 1000], [-100, 720], [600, 700], [1100, 780], [1700, 700], [2400, 760], [2900, 1000]], { fill: '#86431F', seed: 45, wob: 12, strata: 4, lobes: 3 });
    YAZ.forEach(([s, x, y, px], i) => {
      const t0 = i < 1 ? st.at + .4 : i < 2 ? tG - .2 : tH + (i - 2) * .22;
      const a = ramp(t, t0, t0 + .35, E.out3) * (1 - ramp(t, Math.max(t0 + .9, i === YAZ.length - 1 ? tD : t0 + .9), Math.max(t0 + 1.8, tD + .6), E.io2)) * Math.pow(.82, i);
      if (a > .01) txtDipinto(ctx, s, x, y, px, 1, { col: '#F06A44', a }); // açılan yamaçlarda okunur kalsın diye bir ton parlak kırmızı
    });
  });
})();
