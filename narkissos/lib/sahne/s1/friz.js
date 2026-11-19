// FRIZ seti, SAHİP-1: P014, P015, P032, P033. Bu dosyayı yalnız bu sahip değiştirir.
// Kurallar: lib/sahne/KILAVUZ.md. Kalabalık vazo bandı gibi; figürler dağınık gruplar hâlinde ve ayakta (sıra hâlinde eğilen dizi yok).
// P033 beddua: ayakta, bir kol göğe uzanır, el yarı açık; yumruk (siyasi selam), iki avuç göğe açık dua duruşu, diz çökme, secde yok.
'use strict';
(() => {
  const S1 = window.S1;
  // friz zemini: siyah sır, üstte ve altta meander bandı (dünya koordinatında; kamerayla kayar), zemin çizgisi
  const friz = (ctx, t, gy, o = {}) => {
    glaze(ctx, o.gx ?? 960, gy, 1300, 'rgba(110,46,22,.35)');
    meander(ctx, -1200, 3200, o.top ?? 90, 40, PC.clayR, PC.glaze);
    ctx.save(); ctx.fillStyle = PC.clayR; ctx.fillRect(-1200, gy, 4400, 5); ctx.restore();
    meander(ctx, -1200, 3200, gy + 22, 40, PC.clayR, PC.glaze);
  };
  // küçük armağanlar: tavşan (kucakta), çiçek
  const tavsan = (ctx, x, y, s) => { ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.beginPath(); ctx.ellipse(0, 0, 9, 5.5, -.1, 0, TAU); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = .7; ctx.stroke();
    ctx.beginPath(); ctx.ellipse(8, -4, 4, 3, -.3, 0, TAU); ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.ellipse(6, -9, 1.2, 4.5, -.4, 0, TAU); ctx.fill(); ctx.stroke(); ctx.beginPath(); ctx.ellipse(8.5, -9.4, 1.2, 4.5, -.1, 0, TAU); ctx.fill(); ctx.stroke(); ctx.restore(); };
  const cicek = (ctx, x, y, s, a = -.6) => { ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(s, s); ctx.strokeStyle = C.ink; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, -16); ctx.stroke();
    for (let k = 0; k < 5; k++) { ctx.save(); ctx.translate(0, -18); ctx.rotate(k * TAU / 5); ctx.beginPath(); ctx.ellipse(0, -2.4, 1.4, 2.6, 0, 0, TAU); ctx.fillStyle = C.red; ctx.fill(); ctx.restore(); } ctx.restore(); };
  const fig = (ctx, x, gy, s, dir, lk, p, seed, sty) => { let J = null, M = null; figure(ctx, { x, y: gy - 44.5 * s, s, dir, sty: sty || (lk.fem ? S1.RFF : STY.red), lk, seed, stripe: .45, idle: .8, p, onJoints: (j, m) => { J = j; M = m; } }); return { J, M }; };
  const el = (ctx, r, side = 'AN') => jointPt(ctx, r.M, r.J[side].wr);

  // ---- P014 · geniş · B04@delikanlılar: delikanlılar ve kızlar dağınık gruplar hâlinde ona armağan uzatır; 'kızlar'da çelenk uzatılır, 'gönül'de bütün başlar ona döner ----
  plan('P014', (ctx, st) => {
    const t = st.t, tK = PE('P014', 0), tG = PE('P014', 1), gy = 860, s = 5.4;
    baseT(ctx); camAt(ctx, lerp(760, 1180, E.sine(st.p)), 520, 1.0);
    friz(ctx, t, gy);
    const don = k => t < tG + k * .12; // 'gönül'e kadar bazı başlar geriye bakar
    const kz = ramp(t, tK - .1, tK + .5, E.out3);
    // grup 1: iki delikanlı (tavşan, çiçek)
    let r = fig(ctx, 260, gy, s, 1, S1.LK_GENC, { shN: 1.1, elN: .4, handN: 'open', headBack: don(0), headBackA: .1 }, 91); tavsan(ctx, ...add(el(ctx, r), [10, -6]), s * .9);
    r = fig(ctx, 420, gy, s * .97, 1, { ...S1.LK_GENC, khiton: { col: '#8E4626', edge: 1.2, sleeve: false } }, { shN: 1.3, elN: .2, handN: 'fist' }, 92); cicek(ctx, ...el(ctx, r), 2.2);
    // grup 2: iki kız (çelenk 'kızlar'da)
    fig(ctx, 760, gy, s * .95, 1, S1.LK_KIZ, { shN: .3, elN: .3, handN: 'open', headBack: don(1), headBackA: .1 }, 93);
    r = fig(ctx, 900, gy, s * .95, 1, { ...S1.LK_KIZ, robeCol: '#97502C' }, { shN: lerp(.4, 1.55, kz), elN: lerp(.5, .1, kz), handN: 'open' }, 94); S1.celenk(ctx, ...add(el(ctx, r), [26, -4]), 26, -.1);
    // grup 3: bir delikanlı, bir kız
    r = fig(ctx, 1180, gy, s, 1, S1.LK_GENC, { shN: 1.2, elN: .3, handN: 'fist', headBack: don(2), headBackA: .1 }, 95); cicek(ctx, ...el(ctx, r), 2.2, -.9);
    fig(ctx, 1420, gy, s * .95, 1, { ...S1.LK_KIZ, robeCol: '#B06A3E' }, { shN: .5, elN: .6, handN: 'open' }, 96);
    // Narkissos sağda, sola bakar, çenesi yukarıda
    fig(ctx, 1760, gy, s * 1.02, -1, LK_NK, { neck: -.12, head: -.1, shF: -.2, elF: -.3 }, 23);
  });

  // ---- P015 · yakın · B05: Narkissos'un profili, çene yukarı; önüne çelenk uzatılır; 'gururludur'da başını çevirir, 'kazanamaz'da çelenk elden kayar, düşer ----
  plan('P015', (ctx, st) => {
    const t = st.t, tG = PE('P015', 0), tK = PE('P015', 1), s = 20;
    baseT(ctx); glaze(ctx, 1000, 900, 1200, 'rgba(110,46,22,.4)');
    camAt(ctx, 960, lerp(620, 520, E.sine(st.p)), 1.0);
    const hy = 420, gy = hy + 37 * s + 44.5 * s;
    const don = t > tG + .15;
    fig(ctx, 1320, gy, s, -1, LK_NK, { neck: -.18, head: don ? .22 : -.16, headBack: don, headBackA: 0, shF: -.1, elF: -.2, shN: .1, elN: .3 }, 23);
    // soldan uzanan el ve çelenk ('kazanamaz'da düşer)
    const dus = ramp(t, tK, tK + .9, E.in2);
    const hx = 640, hyy = 600;
    // çelengi uzatan kız: sol kenarda, kolu öne uzanır; 'kazanamaz'da eli açılır
    figure(ctx, { x: 60, y: gy - 44.5 * s * .95, s: s * .95, dir: 1, sty: S1.RFF, lk: { ...S1.LK_KIZ, robeCol: '#97502C' }, seed: 94, stripe: .45, idle: .8, p: { neck: .05, head: .05, handN: 'open' }, ik: { hN: [hx + 20, hyy + 30 + 30 * dus] } });
    S1.celenk(ctx, hx + 140 + 60 * dus, hyy - 40 + 700 * dus * dus, 90, -.2 + 1.1 * dus);
    S1.ustBant(ctx);
  });

  // ---- P032 · orta · C12: geri çevrilen başkaları, dağınık, başları öne düşük; 'değildi'de bir bir başını kaldırır; 'küçümsenenlerden'de biri öne çıkar ----
  const RED = [[300, 1, S1.LK_KIZ, 101], [520, 1, S1.LK_GENC, 102], [760, -1, { ...S1.LK_KIZ, robeCol: '#97502C' }, 103], [1060, 1, { ...S1.LK_GENC, khiton: { col: '#8E4626', edge: 1.2, sleeve: false } }, 104], [1640, -1, { ...S1.LK_KIZ, robeCol: '#B06A3E' }, 105]];
  plan('P032', (ctx, st) => {
    const t = st.t, tD = PE('P032', 0), tK = PE('P032', 1), gy = 900, s = 7.2;
    baseT(ctx); camAt(ctx, lerp(840, 1000, E.sine(st.p)), 540, 1.0);
    friz(ctx, t, gy, { top: 70 });
    RED.forEach(([x, dir, lk, sd], i) => {
      const up = ramp(t, tD + i * .28, tD + i * .28 + .6, E.io2);
      if (i === 3) { const u = ramp(t, tK - .1, tK + 1.0, E.io2); if (u > 0 && u < 1) { walkScene(ctx, null, lerp(x, x + 260, u), s, t, 1, { ground: groundOf(() => gy), noCam: true, sty: STY.red, lk, dist: lerp(x, x + 260, u), stripe: .45, p: { neck: .1 * (1 - up), head: .05 } }); return; }
        x += 260 * u; }
      fig(ctx, x, gy, s * (lk.fem ? .95 : 1), dir, lk, { neck: lerp(.38, .02, up), head: lerp(.32, -.04, up), shN: .1, elN: .3, shF: -.1, elF: .2, handN: 'open', handF: 'open' }, sd);
    });
  });

  // ---- P033 · ters açı · C12@ellerini: aşağıdan, gök önünde siluet; öne çıkan genç bir kolunu göğe uzatır (ayakta), ağzından O DA BÖYLE SEVSİN göğe yükselir; 'kavuşamasın'da bulutlara ulaşır ----
  //      Fable tur 1: yumruk (siyasi selam) kalktı; iki avuç göğe açık dua duruşu da yok (hassasiyet). Uzak kol (gövdenin ardından; yüzü örtmez) neredeyse dik göğe uzanır, el yarı açık; yakın kol aşağıda. Kalkarken dirsek bükük (düz kol hiçbir anda öne uzanmaz); 45° düz kol selam gibi okunur, kaçınılır.
  //      Yazı 'o'da yazılmaya başlar, 'sevsin'de tamamdır ve plan sonuna dek (≥ 1,5 sn) TAM kalır; 'kavuşamasın'da bütün olarak bulutlara yükselir (harf silinmez, kesik okunmaz).
  plan('P033', (ctx, st) => {
    const t = st.t, tK = PE('P033', 0), tV = PE('P033', 2), tO = Wd('C12', 'o'), tS = Wd('C12', 'sevsin', 0, true), gy = 1010, s = 6.2;
    baseT(ctx);
    camAt(ctx, 960, lerp(600, 530, ramp(t, st.at, st.end, E.io2)), 1.0);
    // gök: kil (ters tonlu), koyu sarmal bulutlar; aşağıda yer çizgisi
    ctx.fillStyle = '#B9653A'; ctx.fillRect(-1000, -1000, 4000, 3000);
    glow(ctx, 1300, 180, 900, 'rgba(240,170,110,.35)');
    for (const [x, y, sc, sd] of [[260, -20, 2.6, 1], [1250, -10, 3.0, 2], [1820, 30, 2.4, 3], [760, -200, 2.2, 4]]) cloud(ctx, x + 10 * Math.sin(t * .3 + sd), y, sc, '#3A1C10', 'rgba(201,112,63,.5)', sd);
    ctx.fillStyle = '#1A0E08'; ctx.fillRect(-1000, gy, 4000, 600);
    const k = ramp(t, tK - .1, tK + .8, E.io2), v = ramp(t, tV, tV + 1.1, E.io2);
    let J = null, M = null;
    figure(ctx, { x: 640, y: gy - 44.5 * s, s, dir: 1, sty: STY.black, lk: { ...S1.LK_GENC, khiton: { col: '#24150E', edge: 1.2, sleeve: false } }, seed: 104, stripe: 0, idle: .6,
      p: { torso: .06 * k, neck: -.22 * k, head: -.22 * k, shN: lerp(.15, -.15, k), elN: lerp(.3, .3, k), handN: 'open', shF: lerp(-.1, 3.1, k), elF: lerp(.2, -.28, k) + 1.5 * Math.sin(PI * k), handF: 'flat' }, onJoints: (j, m) => { J = j; M = m; } });
    if (J) { const m = headPt(ctx, J, M, [6.6, -4.2]);
      // söz yolu: ağızdan sağ-yukarı, kolun yönünde göğe; 'kavuşamasın'da bütün yazı bulutlara kalkar
      const P = S1.konusmaYolu(m[0] + 60, m[1] - 10 - 100 * v, -.3 - .05 * v, 1000, t, { amp: 12, k: .015, curl: .12 });
      S1.yolYazi(ctx, 'O DA BÖYLE SEVSİN', P, ramp(t, tO - .05, Math.min(tS, st.end - 1.6), E.lin), { px: 62, col: '#3A0E06', a: 1 - .25 * v }); }
  });
})();
