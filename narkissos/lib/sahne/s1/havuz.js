// HAVUZ seti, SAHİP-1: P002, P003, P004, P005, P007. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Ortak kurucular lib/havuz.js (kiyiOrta, havuzGenis, yakinYuz); yardımcılar S1 (s1/cam.js).
// A bölümü havuz planları tanınmadan önce: yansıma refLag(t) kadar (9 kare) geç izler, kilitlenme yok.
'use strict';
(() => {
  const S1 = window.S1;

  // ---- P002 · orta · A02@iki: antik pınar; efeb başlı genç kıyıda yüzüstü uzanmış; 'genç'te su durulur, 'baktı'da başını eğer, 'narkissos'ta adı yazılır ----
  let p002Ek = null; // dipintonun ekran yeri (over için)
  plan('P002', (ctx, st) => {
    const t = st.t, tG = PE('P002', 0), tB = PE('P002', 1), tN = PE('P002', 2);
    const fx = lerp(850, 940, E.sine(st.p)), look = ramp(t, tB, tB + .9, E.io2);
    const t0 = st.at - .9;
    kiyiOrta(ctx, t, {
      cam: [fx, 612, 1.56], look, reach: 0, refA: lerp(.3, .42, ramp(t, tG - .3, tG + .6, E.io2)),
      // P001'den süren halka: yansıyan başın sağında, 'genç'te söner (çizgiler başın çevresinde çizilmez)
      rings: [{ x: 1330, y: 700, t0, A: 7, sq: .36, v: 300, lam: 46, k: 1.1, reach: 900, life: tG - t0, mask: 80 }],
    });
    // vazo ressamının ad yazısı: figürün sırtının üstünde
    const p = ramp(t, tN, tN + .9, E.lin);
    dipintoYaz(ctx, 'ΝΑΡΚΙΣΣΟΣ', 790, 442, 30, p, { col: S1.KIL, w: .11 });
    p002Ek = S1.ekran(ctx, [790, 442]);
  }, { over: (ctx, st) => { const tN = PE('P002', 2); if (st.t > tN + .5 && p002Ek) etiket(ctx, 'NARKİSSOS', p002Ek[0], p002Ek[1] + 62, st.t - tN - .5, 99, { px: 40 }); } });

  // ---- P003 · geniş · A03: bilinen resim (kartpostal): orman kenarında pınar, kıyıda küçük uzanmış genç; 'herkes'te nergisler rüzgârla eğilir, 'unutulan'da rüzgâr durur ----
  const P3_NL = [[1560, 5, 58], [1610, 8, 46], [1655, 2, 54], [1200, 11, 50], [1720, 4, 44]];
  plan('P003', (ctx, st) => {
    const t = st.t, tH = PE('P003', 0), tU = PE('P003', 1);
    const wind = ramp(t, tH - .2, tH + .6, E.io2) * (1 - ramp(t, tU, tU + .8, E.io2)) + settle(t, tU + .5, .05, 1.4, 2.6);
    const gust = wind * (.28 + .05 * Math.sin(t * 5.1));
    const c0 = [980, 560, 1.0], c1 = [930, 590, 1.08];
    const cam = camMix(c0, [975, 565, 1.02], st.p * .6, E.lin);
    const cc = t > tU ? camMix(cam, c1, (t - tU) / (st.end - tU), E.io2) : cam;
    const gy = 760, s = 2.05, px = 905, hgy = 731;
    const fig = c => {
      for (const [x, sd, h] of P3_NL) { c.save(); c.translate(x, gy); c.rotate(gust * (.9 + .2 * hash(sd))); narcissus(c, 0, 0, 1.35, t, sd, { dir: x > 1290 ? -1 : 1, h }); c.restore(); }
      const lag = refLag(t), mk = tt => { const f = proneFig(px, hgy, s, { ...pPose({ head: .06, neck: .03 }), hemPerp: true, hemT: .62 }, { flatFeet: -2.9, hN: [px + 34 * s, hgy - .5 * s], hF: [px + 30 * s, hgy - 1.2 * s] });
        f.ik.fN = [px - 47 * s, gy - 2.4 * s, -2.6]; f.ik.fF = [px - 48 * s, gy - 2.8 * s, -2.6]; return f; };
      withFigT(c === ctx ? t : t - lag, () => figure(c, mk(c === ctx ? t : t - lag)));
    };
    havuzGenis(ctx, t, { cam: cc, fig, nerg: [], refA: .4 });
    // rüzgâr: çimen ve havada sürüklenen iki yaprak
    if (wind > .02) for (let i = 0; i < 4; i++) { const u = ((t - tH) * .45 + i * .27) % 1, x = lerp(300, 1900, u), y = 560 + 60 * Math.sin(u * 7 + i) + i * 30;
      ctx.save(); ctx.globalAlpha = wind * Math.sin(u * PI); ctx.translate(x, y); ctx.rotate(t * 3 + i); ctx.beginPath(); ctx.ellipse(0, 0, 11, 4, 0, 0, TAU); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.5; ctx.stroke(); ctx.restore(); }
  });

  // ---- P004 · yakın · A03@sudaki: yüz ve yansıması; 'anladı'da yansıyan göz karenin en parlak noktası; 'benim'de küçük irkilme (yansıma 9 kare geç) ----
  const p4Pose = t => {
    const tb = PE('P004', 1), rc = ramp(t, tb - .02, tb + .2, E.out3) * (1 - .5 * ramp(t, tb + .6, tb + 1.4, E.io2));
    return { neck: -.04 * rc, head: -.08 * rc + .02 * Math.sin(t * .7), smile: -.2, brow: .3 + .5 * rc, mouthOpen: .5 * rc, browUp: .2 * rc, eyeWide: .25 * rc };
  };
  plan('P004', (ctx, st) => {
    const t = st.t, tA = PE('P004', 0);
    const z = lerp(.96, 1.03, E.sine(st.p));
    const r = yakinYuz(ctx, t, { T: {}, cam: [D_XE + 330, D_WY - 18, z], pose: p4Pose });
    // yansıyan göz: 'anladı'da karenin en parlak noktası (küçük, sıcak; yansımanın içinde)
    const g = ramp(t, tA - .1, tA + .5, E.out3) * (1 - .45 * ramp(t, tA + 1.2, tA + 2.4, E.io2));
    if (g > .01) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, r.reye[0] + 2, r.reye[1], 34, `rgba(255,236,200,${(.55 * g).toFixed(3)})`); ctx.restore(); }
  }, { over: (ctx, st) => {
    const tb = PE('P004', 1);
    if (st.t > tb + .1) quote(ctx, '“O benim.”', 1240, 210, st.t - tb - .1, { px: 66, col: S1.SEPYA, panel: .45, per: .3 });
    kunye(ctx, 'Ovidius, Dönüşümler III 463', st.t - tb - .4, 99);
  } });

  // ---- P005 · ters açı · A04: arkadan ve yukarıdan; genç kıyıda, arkasında ormana açılan boş patika. 'neden'de patikaya güneş düşer; 'kalkıp'ta rüzgâr yaprakları sürükler; genç kıpırdamaz ----
  const P5 = { gy: 640, sh: 700, s: 4.2, px: 880 };
  const p5Fig = (tt, sc) => {
    const { gy, s, px } = P5;
    const f = proneFig(px, gy, s, { ...pPose({ head: .06, neck: .02 }), hemPerp: true, hemT: .62 }, { flatFeet: -2.9, dir: -1 });
    const mx = q => [2 * px - q[0], q[1], ...q.slice(2)];
    f.ik = { fN: mx(f.ik.fN), fF: mx(f.ik.fF), hN: mx([px + 34 * s, gy + 1.2 * s]), hF: mx([px + 30 * s, gy - .2 * s]) };
    return f;
  };
  const p5Patika = [[1270, 690], [1330, 610], [1300, 520], [1380, 440], [1460, 380], [1500, 330]];
  plan('P005', (ctx, st) => {
    const t = st.t, tN = PE('P005', 0), tK = PE('P005', 1), { gy, sh, s, px } = P5;
    baseT(ctx); glaze(ctx, 1300, 500, 1300, 'rgba(120,48,22,.42)');
    camAt(ctx, lerp(880, 1060, E.sine(st.p)), 560, 1.0);
    // uzak orman çizgisi (yukarıdan bakış: ufuk yüksek)
    groundBand(ctx, 330, -1000, 4000, { h: 1400, fill: '#4E2513' });
    for (const [x, sc, sd] of [[620, 1.0, 3], [900, 1.25, 8], [1180, 1.1, 5], [1700, 1.3, 11], [1960, 1.05, 2], [2200, 1.2, 7], [380, 1.15, 13]]) vaseTree(ctx, x, 334, sc, sd, t, { branches: 6, reach: 90 });
    // patika: genişten (genç'in arkası) ormanın boşluğuna daralan açık şerit; 'neden'de güneş düşer (rengi açılır, eğik ışık)
    const sun = ramp(t, tN - .1, tN + .7, E.io2);
    const L = [[1150, 760], [1210, 640], [1180, 540], [1300, 450], [1440, 380], [1478, 334]], R = [[1500, 334], [1520, 380], [1420, 460], [1330, 560], [1390, 660], [1470, 760]];
    ctx.save(); ctx.beginPath(); spline(ctx, L.concat(R), true, .8); ctx.fillStyle = mixCol('#8A4A26', '#C98650', sun); ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(30,14,8,.6)'; ctx.stroke();
    // patikada taş izleri
    ctx.fillStyle = 'rgba(40,18,9,.35)'; for (let i = 0; i < 10; i++) { const u = i / 9, q = lerp2(lerp2(L[Math.floor(u * 5)], L[Math.min(5, Math.floor(u * 5) + 1)], (u * 5) % 1), lerp2(R[5 - Math.floor(u * 5)], R[Math.max(0, 4 - Math.floor(u * 5))], (u * 5) % 1), .3 + .4 * hash(i)); ctx.beginPath(); ctx.ellipse(q[0], q[1], 9 - u * 5, 3.5 - u * 1.5, 0, 0, TAU); ctx.fill(); }
    if (sun > .01) { // eğik güneş: ormanın boşluğundan patikaya düşen tek yumuşak şerit
      const g = ctx.createLinearGradient(1560, 0, 1300, 760); g.addColorStop(0, `rgba(255,214,150,${(.2 * sun).toFixed(3)})`); g.addColorStop(1, 'rgba(255,214,150,0)');
      ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(1500, -100); ctx.lineTo(1640, -100); ctx.lineTo(1480, 780); ctx.lineTo(1170, 780); ctx.closePath(); ctx.fill(); }
    ctx.restore();
    for (let i = 0; i < 12; i++) grass(ctx, 1000 + i * 120 + (i % 3) * 30, 660 + (i % 4) * 90, 1.4, t, i + 21);
    // su: solda, kıyı çizgisi kayanın önünde (yansıma eksen sh)
    const water = c => { c.moveTo(-3000, sh); c.lineTo(px - 40 * s, sh); c.quadraticCurveTo(px - 30 * s, sh + 300, px - 120 * s, sh + 900); c.lineTo(-3000, sh + 900); c.closePath(); };
    waterBody(ctx, water, sh, t, { a: .2, seed: 7, span: [-400, px - 40 * s], n: 26, depth: 400 });
    const lag = refLag(t);
    mirror(ctx, c => withFigT(t - lag, () => figure(c, p5Fig(t - lag))), sh, water, t, { a: .38, calm: 1.0 });
    crag(ctx, [[px - 52 * s, gy + 4], [px - 30 * s, gy - 8], [px + 60 * s, gy - 4], [px + 64 * s, gy + 70], [px - 40 * s, sh + 60]], { fill: '#5A2C16', seed: 6, wob: 10, strata: 3, lobes: 2 });
    figure(ctx, p5Fig(t));
    shoreLine(ctx, -3000, sh, { x1: px - 40 * s, w: 2.6 });
    // rüzgâr ('kalkıp'): yapraklar patikadan uzağa, sağ üste sürüklenir; genç kıpırdamaz
    const w = ramp(t, tK - .1, tK + .4, E.io2);
    if (w > 0) for (let i = 0; i < 9; i++) { const u = clamp((t - tK - i * .06) * .55), x = lerp(1280 + i * 25, 2100 + i * 30, E.in2(u)), y = lerp(640 - i * 30, 260 - i * 10, u) + 30 * Math.sin(u * 6 + i);
      if (u <= 0 || u >= 1) continue; ctx.save(); ctx.globalAlpha = Math.sin(u * PI); ctx.translate(x, y); ctx.rotate(t * 4 + i * 1.3); ctx.beginPath(); ctx.ellipse(0, 0, 12, 4.5, 0, 0, TAU); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.6; ctx.stroke(); ctx.restore(); }
    S1.ustBant(ctx);
  });

  // ---- P007 · yakın · A05@peki: su yüzü ve yansıma; 'kendini'de esinti suyu ürpertir (halka yok), 'döner'de yansıma yerine oturur, kenarda bir yaprak kıyıya sürüklenir ----
  plan('P007', (ctx, st) => {
    const t = st.t, tK = PE('P007', 0), tD = PE('P007', 1);
    const z = lerp(1.18, 1.11, E.sine(st.p));
    const r = yakinYuz(ctx, t, { T: {}, cam: [D_XE + 380, D_WY + 150, z], pose: () => ({ neck: 0, head: .02 * Math.sin(t * .6), smile: -.25, brow: .25 }),
      rings: [{ x: D_XE + 380, y: D_WY + 4, t0: tK, A: 3.2, sq: .62, v: 900, lam: 260, k: 1.4, reach: 3200, life: tD - tK + .2, shear: 1.6, noLines: true }] });
    // esinti: ince yatay kırışıklar suyun üstünden soldan sağa geçer
    const e = ramp(t, tK - .05, tK + .3, E.io2) * (1 - ramp(t, tD - .4, tD + .3, E.io2));
    if (e > .01) { ctx.save(); ctx.beginPath(); ctx.rect(D_XE - 10, D_WY + 6, 4000, 1200); ctx.clip(); ctx.strokeStyle = `rgba(236,176,124,${(.8 * e).toFixed(3)})`; ctx.lineCap = 'round';
      const fr = lerp(D_XE - 200, D_XE + 1600, clamp((t - tK) / (tD - tK)));
      for (let i = 0; i < 22; i++) { const y = D_WY + 18 + i * 22 + 6 * Math.sin(i * 2.3), x = fr - hash(i * 3.3) * 700, L = 60 + hash(i * 1.7) * 160; ctx.lineWidth = 2 + hash(i) * 1.6;
        ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x + L / 2, y - 3, x + L, y); ctx.stroke(); }
      ctx.restore(); }
    // yaprak kıyıya sürüklenir ('döner')
    const u = ramp(t, tD - .2, st.end, E.out2), lx = lerp(1560, 1210, u), ly = D_WY + 36 + 6 * Math.sin(t * 1.3);
    ctx.save(); ctx.translate(lx, ly); ctx.rotate(-.2 + .15 * Math.sin(t)); ctx.scale(1, .45); ctx.beginPath(); ctx.ellipse(0, 0, 26, 9, 0, 0, TAU); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 2; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(-22, 0); ctx.lineTo(22, 0); ctx.lineWidth = 1.2; ctx.stroke(); ctx.restore();
  });
})();
