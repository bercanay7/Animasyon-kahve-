// Gılgamış, şart Shorts'u: dikey için yazılmış planlar (dünya 1080×1920; kil motoru, filmin SET/FIG/DK/YAR kurucuları).
// Her plan bir kesitle başlar (SZ.KESIT[i].t0); içteki olaylar kelimelere bağlı (A('F07@uyku')): ses değişirse görüntü kayar.
// Dikey kuralı: düşüş (baş öne düşer, sis yukarıdan iner), yedi ekmek tablet gibi üst üste (kamera yukarıdan aşağı okur).
// Ölçek sırası: orta → yakın → geniş → yakın → ayrıntı → orta (ardışık iki plan aynı ölçekte değil).
'use strict';
// Kenar kararması dikey tuvale göre (filmin postHazirla'sı 1920×1080 oranıyla kurulu: dikeyde iç yarıçap dış yarıçapı geçiyor ve
// üstte kemer biçimli gölge çıkıyordu; kemer mihrap okunabilir). Elips: kare dokuda radyal gradyan, tuvale gerilerek. Gren aynı.
postHazirla = function () {
  const q = makeCanvas(512, 512), x = q.getContext('2d'), g = x.createRadialGradient(256, 246, 150, 256, 256, 330);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(12,5,1,.55)'); x.fillStyle = g; x.fillRect(0, 0, 512, 512);
  VIG = makeCanvas(DW, DH); VIG.getContext('2d').drawImage(q, 0, 0, DW, DH);
  for (let k = 0; k < 4; k++) { const c = makeCanvas(512, 512), y = c.getContext('2d'), id = y.createImageData(512, 512), r = rng(100 + k); for (let i = 0; i < id.data.length; i += 4) { const v = 128 + (r() - .5) * 120; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; } y.putImageData(id, 0, 0); GRAIN.push(c); }
};
(() => {
  const KS = i => SZ.KESIT[i].t0, KE = i => SZ.KESIT[i].t1;
  const kay = (R, st, a, b, e = E.sine) => { const p = e(clamp(st.lt / Math.max(.5, st.d))); R.cam(lerp(a[0], b[0], p), lerp(a[1], b[1], p), lerp(a[2], b[2], p)); };
  const { sekil, cizgi } = FIG;
  const KAYIT = (i, id, olcek, draw, o = {}) => { PLAN[id] = { at: SZ.KESIT[i].ad, set: 'oda', olcek }; shot(KS(i) + (o.off || 0), draw, { id, tr: { type: 'cut' }, ...o }); };

  // ── oda: tuğla duvar, zemin, sedir (bank), meşale, duvardaki çentikler, öndeki ekmek sırası, oturan Gılgamış ──
  const FY = 1500, FX = 430, FS = 1000, KK = FS / 540;   // ayak tabanı, figür boyu; film oranı (UYKU: s 540, bank x −120…+80, üstü −135)
  const EKMEK = [1, 2, 3, 4, 5, 0, 6];                    // filmin sırası: kurumuş, kösele, nemli, beyaz, küflü, taze, közde
  function oda(R, st, o = {}) {
    SET.zemin(R);
    DK.tugla(R, -600, -900, 1700, FY, { z: .3, bw: 100, bh: 40, lw: 2.5 });
    R.b.fillStyle = gv(.38); R.b.fillRect(-600, FY, 2300, 900); cizgi(R, [[-600, FY], [1700, FY]], 4, -.7);
    sekil(R, [[FX - 120 * KK, FY], [FX - 120 * KK, FY - 135 * KK], [FX + 80 * KK, FY - 135 * KK], [FX + 80 * KK, FY]], .5, .5, null, 0);
    cizgi(R, [[FX - 120 * KK, FY - 130 * KK], [FX + 80 * KK, FY - 130 * KK]], 5, .5);
    SET.mesale(R, 120, 760, { son: o.mesale ?? 1, i: 1.4 });
    // çentikler: geçen günler, başın sağında duvara kazınmış kısa, eğik, düzensiz izler.
    // (İlk sürümde yedi uzun dikey oluk parmaklıklı hücre penceresi okundu; bağımsız okuma, 23 Kasım.)
    const c = o.centik || 0;
    for (let i = 0; i < 7; i++) { const p = clamp(c * 7 - i); if (p <= 0) continue;
      const x = 660 + i * 34 + (hash(i * 3.7) - .5) * 10, y = 800 + (hash(i * 5.1) - .5) * 22, L = 62 + hash(i * 2.3) * 26, eg = (hash(i * 7.9) - .3) * .35;
      cizgi(R, [[x, y], [x + Math.sin(eg) * L * E.out2(p), y + Math.cos(eg) * L * E.out2(p)]], 7, -.9); }
    // ekmekler: önde, zeminde tek sıra (gün gün belirir: kabartma zeminden yükselir)
    const n = o.ekmek || 0;
    for (let i = 0; i < 7; i++) { const p = clamp(n - i); if (p > 0) YAR.ekmek(R, 130 + i * 136, FY + 170, 52 * (.6 + .4 * E.outBack(p)), EKMEK[i]); }
    const P = o.poz || {};
    FIG.fig(R, FX, FY, FS, { tip: 'gilgamis', giysi: 'post', f: 1, otur: 1, egilme: P.egilme ?? .08, bas: P.bas ?? 0, kol: [[.8, .6], [.5, .5]], basO: { kapali: !!P.kapali } });
    R.L.dir = o.isik || [-.55, -.55, .6];
  }
  // uyku pozu: u 0 (uyanık, dik) → 1 (baş göğüste, gözler kapalı)
  const uyku = u => ({ egilme: lerp(.08, .42, u), bas: lerp(0, .7, u), kapali: u > .35 });
  // sis: yukarıdan aşağı inen ışık bantları (p 0..1 iner, a görünürlük)
  function sis(R, p, a) {
    R.after(c => {
      c.globalCompositeOperation = 'screen';
      for (let i = 0; i < 6; i++) {
        const yy = lerp(-500, 200, p) + i * 260 + Math.sin(FIG_T * .5 + i) * 24, g = c.createLinearGradient(0, yy - 130, 0, yy + 130);
        const k = a * clamp(p * 6 - i * .6) * (.10 + .03 * (i % 2));
        g.addColorStop(0, 'rgba(225,214,200,0)'); g.addColorStop(.5, `rgba(225,214,200,${k.toFixed(3)})`); g.addColorStop(1, 'rgba(225,214,200,0)');
        c.fillStyle = g; c.fillRect(-800, yy - 130, 2700, 260);
      }
    });
  }

  // P1 · orta · F06 · şart: dik oturuyor, gözleri açık; nefes; bir kez ağır kırpar (u≈2,2). Üstte kanca yazısı için boş tuğla duvar.
  KAYIT(0, 'G1', 'orta', (R, st) => {
    kay(R, st, [520, 880, 1.0], [520, 930, 1.06]);
    // uykuyla boğuşma: baş yavaşça düşer, silkinip kalkar (u 0,9–1,9); ikinci düşüş şartın sonunda başlar (P2'ye bağlanır)
    const nef = Math.sin(st.t * 2.1) * .012, u = st.lt;
    const dus = ramp(u, .9, 1.75, E.in2) * (1 - ramp(u, 1.75, 1.95, E.out3)) + ramp(u, 2.6, 3.3, E.in2) * .55;
    oda(R, st, { poz: { egilme: .08 + nef + dus * .12, bas: .02 + dus * .38, kapali: dus > .55 } });
  });
  // P2 · yakın · F07 · 'uyku'da baş düşer; 'sis'te sis yukarıdan iner; meşale söner
  KAYIT(1, 'G2', 'yakin', (R, st) => {
    const tu = A('F07@uyku'), ts = A('F07@sis');
    const u = ramp(st.t, tu - .15, tu + .9, E.io2);
    kay(R, st, [600, 900, 1.55], [620, 990, 1.75]);
    oda(R, st, { poz: uyku(u), mesale: lerp(1, .45, ramp(st.t, ts, KE(1), E.io2)) });
    sis(R, ramp(st.t, ts - .3, KE(1) + .4, E.lin), 1);
    R.L.int = lerp(1, .6, u);
  });
  // P3 · geniş · F08 · günler geçer: ışık bir kez döner, duvara yedi çentik, önde yedi ekmek; o uyuyor
  KAYIT(2, 'G3', 'genis', (R, st) => {
    kay(R, st, [540, 1020, .92], [540, 1000, .96]);
    const p = clamp(st.lt / (st.d - .15));
    const a = lerp(-.9, .9, E.io2(p));
    oda(R, st, { poz: uyku(1), centik: p, ekmek: p * 7, mesale: .45, isik: [Math.sin(a) * .7, -.6, .55] });
    sis(R, 1, .55);
    R.L.int = .8;
  });
  // P4 · yakın · F09 · uyanır: baş kalkar, gözler açılır; üstte çentikler (o henüz bakmadı)
  KAYIT(3, 'G4', 'yakin', (R, st) => {
    const tu = A('F09@uyandığında');
    const u = 1 - ramp(st.t, tu - .1, tu + .7, E.out3);
    kay(R, st, [620, 900, 1.65], [600, 880, 1.72]);
    oda(R, st, { poz: { ...uyku(u), kapali: u > .5 }, centik: 1, ekmek: 7, mesale: lerp(.45, 1, 1 - u) });
  });
  // P5 · ayrıntı · F10 · yedi ekmek tablet gibi üst üste: her sıra bir gün (solda çivi sayısı), kamera yukarıdan aşağı okur;
  // anılan ekmeğe meşale ışığı; yedincisi közde parlar.
  const SIRA = ['birincisi', 'ikincisi', 'üçüncüsü', 'dördüncüsü', 'beşincisi', 'altıncısı', 'yedincisi'];
  const RY = i => 300 + i * 230, RX = 640;
  function civi(R, x, y, n) { // çivi yazısı sayı işareti: dikey kamalar (üstte geniş, aşağı sivrilen üçgen; yatay çubuk yok), dörtlü sıralar
    for (let k = 0; k < n; k++) { const cx = x + (k % 4) * 40, cy = y + Math.floor(k / 4) * 84;
      R.d.fillStyle = dv(-.9); R.d.beginPath(); R.d.moveTo(cx - 15, cy - 32); R.d.lineTo(cx + 15, cy - 32); R.d.lineTo(cx, cy + 34); R.d.closePath(); R.d.fill(); }
  }
  KAYIT(4, 'G5', 'ayrinti', (R, st) => {
    const T = SIRA.map(w => A('F10@' + w));
    let y = RY(0);
    for (let i = 1; i < 7; i++) y = lerp(y, RY(i), ramp(st.t, T[i] - .55, T[i] - .05, E.io3));
    const cur = T.reduce((k, t, i) => (st.t >= t - .3 ? i : k), 0);
    R.cam(545, clamp(y + 40, 120 - 30 + 960 / 1.55, 1560), 1.55);   // tabletin üstünden ve kor yatağının altından dışarı bakmaz
    SET.zemin(R);
    R.b.fillStyle = gv(.34); R.b.fillRect(80, 120, 940, 1720);                       // tablet yüzü (hafif kabarık)
    cizgi(R, [[80, 120], [1020, 120], [1020, 1840], [80, 1840], [80, 120]], 6, -.7);
    // kor yatağı: tabletin altında ocak; yedincisi bunun üstünde
    R.b.fillStyle = gv(.22); R.b.fillRect(60, 1840, 980, 420); R.m.fillStyle = '#5A3422'; R.m.fillRect(60, 1840, 980, 420);
    for (let k = 0; k < 26; k++) { const x = 120 + hash(k * 1.3) * 860, yy = 1880 + hash(k * 2.9) * 300, r = 14 + hash(k * 4.1) * 22;
      R.b.fillStyle = gv(.3 + hash(k) * .1); R.b.beginPath(); R.b.arc(x, yy, r, 0, TAU); R.b.fill(); }
    R.after(c => { c.globalCompositeOperation = 'screen'; const fl = .8 + .2 * Math.sin(st.t * 5.3);
      for (let k = 0; k < 26; k++) { const x = 120 + hash(k * 1.3) * 860, yy = 1880 + hash(k * 2.9) * 300, r = 10 + hash(k * 4.1) * 16;
        const g = c.createRadialGradient(x, yy, 0, x, yy, r * 2.2); g.addColorStop(0, `rgba(255,140,50,${(.55 * fl * (.5 + hash(k * 9) * .5)).toFixed(3)})`); g.addColorStop(1, 'rgba(255,90,20,0)');
        c.fillStyle = g; c.beginPath(); c.arc(x, yy, r * 2.2, 0, TAU); c.fill(); } });
    for (let i = 0; i < 7; i++) {
      const yy = RY(i);
      cizgi(R, [[100, yy + 85], [1000, yy + 85]], 5, -.85);                          // sıra çizgisi (tabletin satırı)
      civi(R, 250, yy - 10 - (i >= 4 ? 30 : 0), i + 1);
      YAR.ekmek(R, RX, yy + 70, 150, EKMEK[i]);
    }
    const [sx, sy] = R.scr(RX, RY(cur));
    R.L.pts.push({ x: sx, y: sy - 120, z: 260 * R.z, r: 700 * R.z, i: .6, col: [1.15, .78, .45] });   // anılan ekmek (beyazda parlayan kemerli niş okunmasın diye ölçülü)
    // yedincisi közde: kor ışığı anıldığında büyür
    const kor = ramp(st.t, T[6] - .3, T[6] + .6, E.io2);
    if (kor > 0) { const [kx, ky] = R.scr(RX, RY(6) + 85); R.L.pts.push({ x: kx, y: ky, z: 50 * R.z, r: 520 * R.z, i: 1.6 * kor, col: [1.3, .5, .15] }); }
    R.L.dir = [-.5, -.6, .6]; R.L.int = .75; R.L.amb = .26;
  });
  // P6 · orta · F11 · geri çekilir: uyanık, başı hafif eğik; yedi çentik, yedi ekmek (yedincisi közde). Kuyrukta ışık azalır.
  KAYIT(5, 'G6', 'orta', (R, st) => {
    kay(R, st, [560, 1250, 1.3], [540, 1010, 1.0], E.io2);
    oda(R, st, { poz: { egilme: .16, bas: .32 + .06 * ramp(st.t, Se('F11'), DUR, E.io2), kapali: false }, centik: 1, ekmek: 7, mesale: lerp(1, .7, ramp(st.t, Se('F11'), DUR)) });
  });
})();
