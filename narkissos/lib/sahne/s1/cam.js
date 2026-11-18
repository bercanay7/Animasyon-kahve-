// CAM seti, SAHİP-1: P001. Bu dosyayı yalnız bu sahip değiştirir.
// Bu dosya SAHİP-1 setlerinin ilk yüklenenidir: ortak yardımcılar (window.S1) burada tanımlanır; öteki s1 dosyaları S1.* kullanır.
// Kurallar: lib/sahne/KILAVUZ.md. Belirlenimci: rastgelelik yalnız rng/hash/noise; sabit saniye yok (zamanlar PA/PE/Wd).
'use strict';
(() => {
  // ================= SAHİP-1 ortak yardımcıları (yalnız s1 dosyaları kullanır) =================
  const S1 = window.S1 = {};
  // kırmızı figür kadın teni: kil (beyaz değil); saç siyah sır
  S1.RFF = { ...STY.red, white: STY.red.fill };
  // Eko: dağ perisi; uzun khiton (robe) + himation, saçı arkada toplu (HAIR_F), yüz açık, kollar görünür
  S1.LK_EKO = { fem: true, hair: 'long', garment: 'robe', himation: true, rf: true, earHidden: true, robeCol: '#A65A32', himCol: '#7A3B1D' };
  // periler (nehir, anne): Eko'dan ayrı renk
  S1.LK_PERI = { fem: true, hair: 'long', garment: 'robe', rf: true, earHidden: true, robeCol: '#9C4E2B' };
  S1.LK_ANNE = { fem: true, hair: 'long', garment: 'robe', himation: true, rf: true, earHidden: true, robeCol: '#B4683B', himCol: '#83421F' };
  // Tiresias: yaşlı, uzun sakallı, uzun giysili kâhin (gözler kapalı: p.blink = 1)
  S1.LK_TIR = { beard: 'long', old: true, hair: 'nape', garment: 'robe', himation: true, rf: true, robeCol: '#8E4A28', himCol: '#6E331B' };
  // delikanlılar / kızlar (friz)
  S1.LK_GENC = { hair: 'short', rf: true, garment: 'short', noCurls: true, efeb: true, hairPts: HAIR_EF, khiton: { col: '#A0552F', edge: 1.2, sleeve: false }, noBelt: true };
  S1.LK_KIZ = { fem: true, hair: 'long', garment: 'robe', rf: true, earHidden: true, robeCol: '#A9603A' };
  // yazı renkleri (sahne içi dipinto): Narkissos'un sesi kil, Eko'nun yankısı kırmızı
  S1.KIL = '#E39A62'; S1.KIRMIZI = '#D2492E'; S1.SEPYA = '#C9A27A';

  // ayakta figür: ayak tabanı gy'de
  S1.ayakta = (ctx, o) => figure(ctx, { x: o.x, y: o.gy - 44.5 * o.s, s: o.s, dir: o.dir || 1, sty: o.sty || STY.red, lk: o.lk, seed: o.seed ?? 5, stripe: o.stripe ?? .45, idle: o.idle ?? .8,
    p: o.p || {}, ik: o.ik, hold: o.hold, extra: o.extra, alpha: o.alpha, onJoints: o.onJoints, noFarArm: o.noFarArm, still: o.still });
  // figürün eklemleri ve baş yerelindeki bir noktanın sahne koordinatı (ör. ağız [6.0,-3.9], göz EYE_Q)
  S1.eklem = (ctx, f) => joints(ctx, f);
  S1.basNok = (ctx, f, q) => { const { J, M } = joints(ctx, f); return headPt(ctx, J, M, q); };
  S1.AGIZ = [6.1, -3.9];
  S1.figY = (gy, s) => gy - 44.5 * s;

  // ---- yazı bir yol boyunca (dipinto şeridi): pts çoklu çizgi; p yazılma oranı (harf harf); o: {px, col, a, font, ls, rise (harf belirirken yükselme), fade: [harf başına saydamlık]} ----
  S1.yolYazi = (ctx, s, pts, p, o = {}) => {
    const ch = [...s], n = ch.length, px = o.px || 40;
    ctx.save(); ctx.font = o.font || FONT.baslik(px, o.w || 700); ctx.textBaseline = 'middle'; ctx.textAlign = 'left';
    ctx.fillStyle = o.col || S1.KIL; const A0 = ctx.globalAlpha * (o.a ?? 1);
    // yol uzunluğu
    const L = [0]; for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    const at = d => { let j = 0; while (j < pts.length - 2 && L[j + 1] < d) j++; const u = clamp((d - L[j]) / ((L[j + 1] - L[j]) || 1)); const P0 = pts[j], P1 = pts[j + 1] || pts[j];
      return [lerp(P0[0], P1[0], u), lerp(P0[1], P1[1], u), Math.atan2(P1[1] - P0[1], P1[0] - P0[0])]; };
    const ls = o.ls ?? px * .14;
    let d = o.d0 || 0; const k = p * n;
    for (let i = 0; i < n; i++) {
      const w = ctx.measureText(ch[i]).width, q = clamp(k - i);
      if (q > 0 && d + w / 2 <= L[L.length - 1] + 200) {
        const [x, y, an] = at(d + w / 2), fa = o.fade ? o.fade(i, n) : 1;
        const of = o.off ? o.off(i, n) : null;
        ctx.save(); ctx.translate(x + (of ? of[0] : 0), y + (of ? of[1] : 0)); ctx.rotate(an + (o.rot ? o.rot(i, n) : 0)); const sc = lerp(.6, 1, E.out3(q)); ctx.scale(sc, sc * (o.flipY ? o.flipY(i, n) : 1));
        ctx.globalAlpha = A0 * E.sine(q) * fa; ctx.fillText(ch[i], -w / 2, -(1 - E.out3(q)) * (o.rise ?? 6)); ctx.restore();
      }
      d += w + ls;
    }
    ctx.restore();
    return d;
  };
  // ağızdan çıkan konuşma şeridi: (x0, y0)'dan ang yönünde, hafif dalgalı; uzunluk len. dir -1 sola
  S1.konusmaYolu = (x0, y0, ang, L, t, o = {}) => {
    const P = [], n = 40; let x = x0, y = y0;
    for (let i = 0; i <= n; i++) {
      const s = L * i / n, a = ang + (o.curl || 0) * (s / L) * (s / L);
      const w = (o.amp ?? 14) * Math.sin(s * (o.k ?? .02) - t * 1.3 + (o.ph || 0)) * clamp(s / 120);
      P.push([x - Math.sin(a) * w, y + Math.cos(a) * w]);
      x += Math.cos(a) * L / n; y += Math.sin(a) * L / n;
    }
    return P;
  };
  // yankı dili: aynı sözün solarak tekrarı (BURADA · burada · rada); t0 ilk tekrarın zamanı, dt aralık. pts yolunu uzatarak dizilir
  S1.yanki = (ctx, s, x, y, t, t0, o = {}) => {
    const reps = o.reps || [s, s.toLocaleLowerCase('tr'), s.toLocaleLowerCase('tr').slice(Math.ceil(s.length / 2))];
    const dt = o.dt ?? .45, px = o.px || 46, dx = o.dx ?? 1, ang = o.ang ?? 0;
    let cx = x, cy = y;
    reps.forEach((r, i) => {
      const ti = t0 + i * dt; if (t < ti) return;
      const age = t - ti, life = o.life ?? 2.4, a = clamp(age / .3) * (1 - ramp(age, life * .55, life, E.io2)) * Math.pow(o.decay ?? .62, i);
      if (a <= .003) { cx += Math.cos(ang) * px * (r.length * .62 + 1.4) * dx; cy += Math.sin(ang) * px * (r.length * .62 + 1.4); return; }
      ctx.save(); ctx.font = FONT.baslik(Math.round(px * Math.pow(o.shrink ?? .86, i)), 700); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = o.col || S1.KIRMIZI;
      ctx.globalAlpha *= a; ctx.letterSpacing = Math.round(px * .14) + 'px';
      if (o.glow) { ctx.shadowColor = o.glow; ctx.shadowBlur = 18; }
      ctx.translate(cx, cy + Math.sin(age * 2 + i) * 3); ctx.rotate(ang * .3); ctx.fillText(r, 0, 0); ctx.restore();
      cx += Math.cos(ang) * px * (r.length * .62 + 1.4) * dx; cy += Math.sin(ang) * px * (r.length * .62 + 1.4);
    });
  };

  // ---- yapraklı dal (zeytin yaprağı; kil dolgu, siyah kontur). koyu: ön plan siluet (sır dolgu, kil kontur) ----
  S1.dal = (ctx, x, y, s, ang, t, seed, o = {}) => {
    const r = rng(seed), L = o.L || 220, sway = Math.sin(t * (o.sp ?? .9) + seed) * (o.sw ?? .03);
    const fill = o.koyu ? '#1A0E08' : (o.fill || PC.clayR), ink = o.koyu ? 'rgba(201,112,63,.55)' : C.ink;
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang + sway); ctx.scale(s, s); ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.globalAlpha *= o.a ?? 1;
    const P = [[0, 0], [L * .35, -L * .06 * (o.bend ?? 1)], [L * .7, -L * .05 * (o.bend ?? 1)], [L, L * .04 * (o.bend ?? 1)]];
    ctx.beginPath(); spline(ctx, P, false); ctx.strokeStyle = ink; ctx.lineWidth = 7; ctx.stroke(); ctx.strokeStyle = fill; ctx.lineWidth = 3.4; ctx.stroke();
    const n = o.n || 9;
    for (let k = 0; k < n; k++) {
      const v = (k + .6) / (n + .2), q = [lerp(0, L, v), Math.sin(v * PI) * -L * .05 * (o.bend ?? 1)], lw = (o.leaf || 40) * (1.05 - v * .35) * (.85 + r() * .3);
      for (const sd of [-1, 1]) {
        const a = sd * (.75 - v * .25) + Math.sin(t * 1.4 + k + seed) * .05 + (o.droop || 0);
        ctx.save(); ctx.translate(q[0], q[1]); ctx.rotate(a); ctx.beginPath(); ctx.ellipse(lw / 2, 0, lw / 2, lw * .2, 0, 0, TAU);
        ctx.fillStyle = fill; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = ink; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(lw * .1, 0); ctx.lineTo(lw * .85, 0); ctx.lineWidth = 1.2; ctx.stroke(); ctx.restore();
      }
    }
    ctx.beginPath(); ctx.ellipse(L + 6, L * .04 * (o.bend ?? 1), (o.leaf || 40) * .45, (o.leaf || 40) * .14, -.2, 0, TAU); ctx.fillStyle = fill; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = ink; ctx.stroke();
    ctx.restore();
  };
  // ön plan yaprak perdesi (paralaks): bir kenardan giren koyu dallar
  S1.perde = (ctx, t, x0, y0, n, seed, o = {}) => {
    const r = rng(seed);
    for (let i = 0; i < n; i++) S1.dal(ctx, x0 + (r() - .5) * (o.sx ?? 160), y0 + i * (o.dy ?? 120) + (r() - .5) * 40, (o.s || 1.6) * (.8 + r() * .4), (o.ang ?? 0) + (r() - .5) * .6, t, seed * 10 + i, { koyu: o.koyu ?? true, L: o.L || 300, leaf: o.leaf || 46, sw: .02 });
  };

  // ---- orman: siyah sır zemin, alttan sıcak ışık, toprak bandı, vazo ağaçları (uzaklar soluk) ----
  // o: {gy, trees: [[x, s, seed, branches, reach, a]], glow: [gx, gy, r], meander, farA}
  S1.orman = (ctx, t, o = {}) => {
    const gy = o.gy ?? 820, gl = o.glow || [960, 900, 1300];
    glaze(ctx, gl[0], gl[1], gl[2], o.warm || 'rgba(120,48,22,.4)');
    for (const tr of (o.far || [])) { ctx.save(); ctx.globalAlpha = tr[5] ?? .35; vaseTree(ctx, tr[0], gy - 6, tr[1], tr[2], t, { branches: tr[3] || 6, reach: tr[4] || 90, fill: '#7A3D20' }); ctx.restore(); }
    groundBand(ctx, gy, -3000, 6000, { h: 1400 });
    for (let i = 0; i < (o.grassN ?? 14); i++) grass(ctx, (o.gx0 ?? -200) + i * (o.gdx ?? 210) + (i % 3) * 40, gy + 2, 1.6, t, i + (o.seed || 3));
    for (const tr of (o.trees || [])) vaseTree(ctx, tr[0], gy, tr[1], tr[2], t, { branches: tr[3] || 7, reach: tr[4] || 110 });
    return gy;
  };
  // meander bandı ekranın üstünde (kamera dışında)
  S1.ustBant = (ctx, o = {}) => { ctx.save(); baseT(ctx); meander(ctx, -400, 2400, o.y ?? 0, o.h ?? 36, PC.clayR, PC.glaze); ctx.restore(); };
  S1.altBant = (ctx, o = {}) => { ctx.save(); baseT(ctx); meander(ctx, -400, 2400, o.y ?? 1044, o.h ?? 36, PC.clayR, PC.glaze); ctx.restore(); };

  // ---- vazo resmi geyik (dörtnala, 'uçan dörtnal'); kil gövde, siyah kontur, boynuzlar. ph: koşu evresi ----
  S1.geyik = (ctx, x, y, s, ph, dir = 1) => {
    ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    const k = Math.sin(ph), ext = .5 + .5 * k, ink = C.ink, fill = PC.clayR;
    const leg = (hx, hy, a1, a2, L1, L2) => { const kx = hx + Math.sin(a1) * L1, ky = hy + Math.cos(a1) * L1, fx = kx + Math.sin(a2) * L2, fy = ky + Math.cos(a2) * L2;
      ctx.beginPath(); ctx.moveTo(hx, hy); ctx.lineTo(kx, ky); ctx.lineTo(fx, fy); ctx.strokeStyle = ink; ctx.lineWidth = 7; ctx.stroke(); ctx.strokeStyle = fill; ctx.lineWidth = 4; ctx.stroke();
      ctx.beginPath(); ctx.ellipse(fx, fy, 3.2, 2, a2, 0, TAU); ctx.fillStyle = ink; ctx.fill(); };
    // arka bacaklar (uzak)
    leg(-34, 4, -.9 - .5 * ext, -.2 - .6 * ext, 20, 24); leg(30, 6, .9 + .5 * ext, .6 + .5 * ext, 18, 22);
    // gövde
    const by = -3 * k;
    ctx.beginPath(); ctx.moveTo(-44, by - 6); ctx.bezierCurveTo(-30, by - 22, 22, by - 24, 38, by - 14); ctx.bezierCurveTo(46, by - 8, 44, by + 10, 34, by + 12);
    ctx.bezierCurveTo(10, by + 18, -20, by + 18, -38, by + 12); ctx.bezierCurveTo(-48, by + 8, -50, by - 2, -44, by - 6); ctx.closePath();
    ctx.fillStyle = fill; ctx.fill(); ctx.strokeStyle = ink; ctx.lineWidth = 3.2; ctx.stroke();
    // boyun ve baş
    ctx.beginPath(); ctx.moveTo(30, by - 16); ctx.quadraticCurveTo(44, by - 40, 52, by - 52); ctx.lineTo(62, by - 50); ctx.quadraticCurveTo(52, by - 30, 42, by - 4); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.ellipse(62, by - 54, 13, 7, .35, 0, TAU); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(70, by - 50); ctx.lineTo(80, by - 44); ctx.lineTo(72, by - 46); ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.arc(64, by - 57, 1.6, 0, TAU); ctx.fillStyle = ink; ctx.fill();
    ctx.beginPath(); ctx.moveTo(56, by - 58); ctx.lineTo(50, by - 66); ctx.lineTo(54, by - 60); ctx.fillStyle = fill; ctx.fill(); ctx.stroke(); // kulak
    // boynuzlar
    ctx.strokeStyle = ink; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(58, by - 60); ctx.quadraticCurveTo(50, by - 84, 38, by - 94); ctx.moveTo(53, by - 74); ctx.lineTo(62, by - 86); ctx.moveTo(47, by - 84); ctx.lineTo(50, by - 98); ctx.moveTo(45, by - 87); ctx.lineTo(32, by - 92); ctx.stroke();
    // benekler ve kuyruk
    for (const [px, py] of [[-20, -8], [-6, -10], [8, -11], [-12, 2], [4, 0], [18, -2]]) { ctx.beginPath(); ctx.arc(px, by + py, 2.2, 0, TAU); ctx.fillStyle = C.white; ctx.fill(); }
    ctx.beginPath(); ctx.moveTo(-46, by - 4); ctx.lineTo(-56, by - 14); ctx.lineTo(-50, by - 2); ctx.fillStyle = fill; ctx.fill(); ctx.strokeStyle = ink; ctx.lineWidth = 2.4; ctx.stroke();
    // yakın bacaklar
    leg(-30, 8, -1.1 - .45 * ext, -.5 - .6 * ext, 22, 26); leg(34, 8, 1.0 + .45 * ext, .5 + .6 * ext, 20, 24);
    ctx.restore();
  };
  // çelenk (kur armağanı): yaprak halkası; açık (yan görünüş) elips
  S1.celenk = (ctx, x, y, r, a = 0, o = {}) => {
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); ctx.scale(1, o.sq ?? .45);
    ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(0, 0, r, 0, TAU); ctx.stroke(); ctx.strokeStyle = C.red; ctx.lineWidth = 2.5; ctx.stroke();
    for (let i = 0; i < 16; i++) { const an = i / 16 * TAU; ctx.save(); ctx.rotate(an); ctx.translate(r, 0); ctx.rotate(.9);
      ctx.beginPath(); ctx.ellipse(0, 0, r * .28, r * .09, 0, 0, TAU); ctx.fillStyle = o.fill || PC.clayR; ctx.fill(); ctx.lineWidth = 1.6; ctx.strokeStyle = C.ink; ctx.stroke(); ctx.restore(); }
    ctx.restore();
  };
  // bölüm kartı: üst yarıda, ilk ~3 sn, tek başına (Cinzel)
  S1.bolumKarti = (ctx, s, lt, d = 3) => {
    if (NOTEXT) return; const a = clamp(lt / .5) * clamp((d - lt) / .6); if (a <= 0) return;
    txt(ctx, s, W / 2, 250, { px: 92, ls: 18, a: E.sine(a), panel: .6, font: FONT.baslik(92, 700), col: YAZI.krem });
  };
  // yerel kamera: [fx, fy, z] kare listesi arasında yumuşak
  S1.kam = (ctx, keys, t) => { let c = keys[0][1]; for (let i = 1; i < keys.length; i++) if (t >= keys[i - 1][0]) c = camMix(keys[i - 1][1], keys[i][1], (t - keys[i - 1][0]) / ((keys[i][0] - keys[i - 1][0]) || 1), keys[i][2] || E.io2); camAt(ctx, ...c); return c; };
  // dünya noktasının ekran (mantıksal) koordinatı
  S1.ekran = (ctx, q) => { const m = ctx.getTransform(), r = m.transformPoint(new DOMPoint(q[0], q[1])); return [r.x / RS, r.y / RS]; };

  // ================= P001 · orta-yakın · CAM =================
  // Kanca: bugünün genci kararmış telefon camına bakar; camda yüzünün birebir, soluk aynası tam altında; akış kartları kayar ve söner;
  // 'baktın'dan sonraki sessizlikte cam havuza döner (kapı A, tur 3 geometrisi PH3). Animatik düzeltmeleri (FABLE tur 3):
  //  1. havuz ara hâlinde yansıma soluk kalır (≤ .26), gövdeden açılır (refDx), halka yansımanın üstünden geçer ama çizgileri başın çevresinde çizilmez (mask; hale yok)
  //  2. yansıyan saçın alt ucu cam içinde yumuşak karartmayla biter ('uzun tutam' okunmasın)
  //  3. telefon ~%15 küçük (pw 196), el camın sol kenarını görünür kavrar (handY 400)
  //  4. çene altındaki sıcak parıltı yok: ekran ışığı nötr/soğuk ve camın üst kenarından (kendi ışık katmanımız; phoneScene light 0)
  const PW = 196;
  plan('P001', (ctx, st) => {
    const t = st.t;
    const tF1 = PE('P001', 0), tF2 = PE('P001', 1), tB = PE('P001', 2), m0 = PE('P001', 3), m1 = PE('P001', 4);
    const fl = [tF1, tF2, lerp(tF2, tB, .5)];
    const th = thumbFlick(t, fl), feed = feedOffset(t, fl);
    const m = ramp(t, m0, m1, E.io2);
    const z = t < m0 ? lerp(.82, .86, E.sine(clamp(t / m0))) : lerp(.86, 1.24, ramp(t, m0, m1, E.in2));
    const u = ramp(t, m0, m1, E.in2), fx = lerp(720, 990, u), fy = lerp(650, 770, u);
    const dxR = 240 * E.io2(m); // gövdeden açıl
    const f = phoneScene(ctx, t, {
      ...PH3, pw: PW, handY: 400, m, thumb: th, cam: [fx, fy, z], light: 0, refA: lerp(.2, .26, m), refDx: dxR, feed, feedA: 1 - ramp(t, tF2, tB, E.io2),
      headNod: .04 * Math.sin(t * 1.1) - .04 * ramp(t, Wd('A01', 'kendine'), tB, E.io2),
      // halka: yansıyan başın sağ altından doğar; çizgiler yansıyan figürün 80 birim çevresinde çizilmez (hale okunmasın)
      rings: (cx, wy) => [{ x: cx + 240, y: wy + 330, t0: m0 + .1, A: 9, sq: .32, v: 330, lam: 46, k: .9, reach: 1200, life: 3.4, mask: 80 }],
    });
    // nötr ekran ışığı: camın üst kenarından yukarı, yalnız figürün üstünde (çene altında sıcak parıltı yok)
    const { J, M } = joints(ctx, f), e = headPt(ctx, J, M, EYE_Q), eS = headPt(ctx, J, M, [EYE_Q[0] * LK_MOD.headS, EYE_Q[1] * LK_MOD.headS]), wy = PH3.wy, pcx = e[0] + PH3.phDx, ph = 1 - m;
    if (ph > .01) {
      const T = ctx.getTransform(), L = layer('s1lit'); L.setTransform(1, 0, 0, 1, 0, 0); L.drawImage(LY.fig, 0, 0);
      L.globalCompositeOperation = 'source-in'; L.setTransform(T); // L = ışık, figürün biçiminde
      const g = L.createRadialGradient(pcx - 40, wy + 10, 0, pcx - 40, wy + 10, 300); g.addColorStop(0, `rgba(214,224,230,${.26 * ph})`); g.addColorStop(.5, `rgba(214,224,230,${.1 * ph})`); g.addColorStop(1, 'rgba(214,224,230,0)');
      L.fillStyle = g; L.fillRect(pcx - 400, wy - 320, 760, 340);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'screen'; ctx.drawImage(LY.s1lit, 0, 0); ctx.restore();
      // camın üst kenarında ince soğuk ışık çizgisi
      ctx.save(); ctx.globalAlpha = .5 * ph; ctx.strokeStyle = 'rgba(214,226,232,.6)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(pcx - PW + 50, wy + 3); ctx.lineTo(pcx + PW - 50, wy + 3); ctx.stroke(); ctx.restore();
    }
    // yansıyan saçın ucu: cam içinde yumuşak karartma (yansıyan başın alt yarısı)
    const shape = morphPts(roundRectPts(pcx - PW, wy, pcx + PW, wy + 900, 56, 56), ellipsePts(pcx - 100, wy + 360, 1300, 360), m);
    const ry = 2 * wy - eS[1];
    ctx.save(); ctx.beginPath(); poly(ctx, shape); ctx.clip();
    const g2 = ctx.createLinearGradient(0, ry + 70, 0, ry + 250); g2.addColorStop(0, 'rgba(6,3,2,0)'); g2.addColorStop(1, 'rgba(6,3,2,.82)');
    ctx.fillStyle = g2; ctx.fillRect(pcx - 1600, ry + 70, 3200, 1400);
    // yansıyan göz bir an parlar ('baktın'; tek odak)
    const gl = ramp(t, tB - .05, tB + .25, E.out3) * (1 - .7 * ramp(t, tB + .5, tB + 1.3, E.io2)) * (1 - m);
    if (gl > .01) { ctx.globalCompositeOperation = 'lighter'; glow(ctx, eS[0] + dxR, ry, 40, `rgba(255,240,215,${(.42 * gl).toFixed(3)})`); }
    ctx.restore();
  });
})();
