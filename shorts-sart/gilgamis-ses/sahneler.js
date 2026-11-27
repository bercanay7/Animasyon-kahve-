// Gılgamış, Shorts'a özel seslendirme: dikey planlar (dünya 1080×1920; kil motoru, filmin SET/FIG/DK/YAR kurucuları).
// Set ve figür ../gilgamis/sahneler.js'ten (oda, uyku pozu, sis, ekmek tableti); planlar bu Shorts'un metnine göre yeniden dizildi.
// Her plan bir kesitle başlar (SZ.KESIT[i].t0, cümleler arası duraklamanın ortası); içteki olaylar sözcüklere bağlı (A('C5@yedincisi')).
// Ölçek sırası: orta → yakın → ayrıntı → geniş → orta → yakın → orta (döngüde H1'in kadrajına varır) (ardışık iki plan aynı ölçekte değil).
// Zaman: şimdi (H1–H4, H6: yedi gün geçmiş; meşale kısık, sis, ekmekler) ↔ geri dönüş (H5, H7: şartın verildiği an; meşale tam, ekmek yok).
// Zaman sıçramalarında kısa çözülme (filmin 'fade'i, gürültü eşikli; duraklamada), mekân içinde kesme.
'use strict';
postHazirla = function () {   // kenar kararması dikey tuvale göre elips (bkz. ../gilgamis/sahneler.js: kemer gölgesi mihrap okunuyordu)
  const q = makeCanvas(512, 512), x = q.getContext('2d'), g = x.createRadialGradient(256, 246, 150, 256, 256, 330);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(12,5,1,.55)'); x.fillStyle = g; x.fillRect(0, 0, 512, 512);
  VIG = makeCanvas(DW, DH); VIG.getContext('2d').drawImage(q, 0, 0, DW, DH);
  for (let k = 0; k < 4; k++) { const c = makeCanvas(512, 512), y = c.getContext('2d'), id = y.createImageData(512, 512), r = rng(100 + k); for (let i = 0; i < id.data.length; i += 4) { const v = 128 + (r() - .5) * 120; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; } y.putImageData(id, 0, 0); GRAIN.push(c); }
};
(() => {
  const KS = i => SZ.KESIT[i].t0, KE = i => SZ.KESIT[i].t1;
  const kay = (R, st, a, b, e = E.sine) => { const p = e(clamp(st.lt / Math.max(.5, st.d))); R.cam(lerp(a[0], b[0], p), lerp(a[1], b[1], p), lerp(a[2], b[2], p)); };
  const { sekil, cizgi } = FIG;
  const COZ = { type: 'fade', dur: .35 };
  const KAYIT = (i, id, olcek, draw, o = {}) => { PLAN[id] = { at: SZ.KESIT[i].ad, set: 'oda', olcek }; shot(KS(i) + (o.off || 0), draw, { id, tr: { type: 'cut' }, ...o }); };

  // ── oda: tuğla duvar, zemin, sedir, meşale, duvardaki çentikler, öndeki ekmek sırası, oturan Gılgamış ──
  const FY = 1500, FX = 430, FS = 1000, KK = FS / 540;
  const EKMEK = [1, 2, 3, 4, 5, 0, 6];                    // filmin sırası: kurumuş, kösele, nemli, beyaz, küflü, taze, közde
  function oda(R, st, o = {}) {
    SET.zemin(R);
    DK.tugla(R, -600, -900, 1700, FY, { z: .3, bw: 100, bh: 40, lw: 2.5 });
    R.b.fillStyle = gv(.38); R.b.fillRect(-600, FY, 2300, 900); cizgi(R, [[-600, FY], [1700, FY]], 4, -.7);
    sekil(R, [[FX - 120 * KK, FY], [FX - 120 * KK, FY - 135 * KK], [FX + 80 * KK, FY - 135 * KK], [FX + 80 * KK, FY]], .5, .5, null, 0);
    cizgi(R, [[FX - 120 * KK, FY - 130 * KK], [FX + 80 * KK, FY - 130 * KK]], 5, .5);
    SET.mesale(R, 120, 760, { son: o.mesale ?? 1, i: 1.4 });
    const c = o.centik || 0;   // kısa, eğik, düzensiz kazıma izleri (uzun dikey oluk parmaklık okunuyordu, 23 Kasım)
    for (let i = 0; i < 7; i++) { const p = clamp(c * 7 - i); if (p <= 0) continue;
      const x = 660 + i * 34 + (hash(i * 3.7) - .5) * 10, y = 800 + (hash(i * 5.1) - .5) * 22, L = 62 + hash(i * 2.3) * 26, eg = (hash(i * 7.9) - .3) * .35;
      cizgi(R, [[x, y], [x + Math.sin(eg) * L * E.out2(p), y + Math.cos(eg) * L * E.out2(p)]], 7, -.9); }
    const n = o.ekmek || 0;
    for (let i = 0; i < 7; i++) { const p = clamp(n - i); if (p > 0) YAR.ekmek(R, 130 + i * 136, FY + 150, 64 * (.6 + .4 * E.outBack(p)), EKMEK[i]); }   // ilk karede okunsun diye filmden büyük (52 → 64)
    // yedincisi közde: önde, son ekmeğin altında kor (şimdi planlarında tek renkli nesne; kapak ve yazı vurgusuyla aynı renk)
    if (o.kor && n >= 7) { const [kx, ky] = R.scr(130 + 6 * 136, FY + 185); R.L.pts.push({ x: kx, y: ky, z: 40 * R.z, r: 330 * R.z, i: o.kor * (.82 + .18 * Math.sin(TAU * FIG_T / DUR * 24) * Math.sin(TAU * FIG_T / DUR * 9 + 1))   /* döngüde sürekli: süreye tam sayı kez */, col: [1.3, .5, .15] }); }
    const P = o.poz || {};
    const ku = clamp(((P.egilme ?? .08) - .08) / .16);   // 0 uyanık … 1 uyuyor
    FIG.fig(R, FX, FY, FS, { tip: 'gilgamis', giysi: 'etek', f: 1, otur: 1, egilme: P.egilme ?? .08, bas: P.bas ?? 0, kol: kolPoz(ku), basO: { kapali: !!P.kapali } });
    R.L.dir = o.isik || [-.55, -.55, .6];
  }
  // kollar: eller ayrı, dizlerin üstünde (uyanık) ya da gevşek sarkık (uyuyor). Bağımsız okuma (27 Kasım): eski pozda iki halka el
  // önde birleşiyor, yakın koldaki bilezik çizgisiyle kelepçe okunuyordu; tuğla duvar ve çentiklerle birlikte "hücre".
  // İkinci okuma: derin öne eğilme + dizlerin arasında sarkan el, küçük boyda tuvalette oturuş okundu. Uyku pozu artık dik gövde,
  // göğse düşen çene (eğilme .42 → .24); yakın ön kol uyluğun üstünde yatar, uzak el arkada sedire dayanır.
  const kolPoz = u => [[lerp(.55, .05, u), lerp(.75, 1.0, u)], [lerp(.2, -.3, u), lerp(.5, .25, u)]];   // uyurken el kucakta (üçüncü okuma: havada duran ön kol uyurgezer okundu)
  const uyku = u => ({ egilme: lerp(.08, .24, u), bas: lerp(0, .78, u), kapali: u > .35 });
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
  const nefes = t => Math.sin(t * 1.9) * .012;
  const ILK = [545, 1215, 1.0], ILK2 = [548, 1190, 1.07];   // H1 bu kadrajla açılır (baş, duvar, ekmek sırası, közdeki yedinci); H7 buna döner (döngü)
  const SIS0 = .32, SIS1 = .58;

  // H1 · orta · C1 · uyuyor: baş göğüste, gözler kapalı; önde yedi ekmek, yedincisi közde (tek renkli nesne, yazı vurgusuyla aynı renk).
  // İlk kareden hareket: sis iner, kamera yaklaşır, nefes, kor ve meşale titrer. Üstte kanca yazısı için tuğla duvar boş.
  KAYIT(0, 'H1', 'orta', (R, st) => {
    kay(R, st, ILK, ILK2, E.lin);
    const p = clamp(st.lt / st.d), dal = ramp(st.t, A('C1@uyuyorsun'), Se('C1') + .3, E.io2) * .05;
    oda(R, st, { poz: { egilme: .24 + nefes(st.t) + dal, bas: .78 + dal, kapali: true }, centik: 1, ekmek: 7, mesale: .45, kor: 1.2 });
    sis(R, lerp(SIS0, SIS1, p), 1); R.L.int = .62;
  });
  // H2 · yakın · C2 · ekmek sırası: kamera soldan sağa yedi ekmeğin üstünden geçer; 'yedi'de anılan ekmeğe ışık, sonunda közdeki yedinci.
  KAYIT(1, 'H2', 'yakin', (R, st) => {
    const q = ramp(st.t, KS(1), A('C2@var') + .3, E.io2), xs = lerp(250, 860, q);
    R.cam(xs, FY + 150, 2.4);
    oda(R, st, { poz: { ...uyku(1), egilme: .24 + nefes(st.t) }, centik: 1, ekmek: 7, mesale: .45, kor: 1.4 });
    const [sx, sy] = R.scr(xs, FY + 120); R.L.pts.push({ x: sx, y: sy - 80, z: 200 * R.z, r: 420 * R.z, i: .5, col: [1.15, .8, .5] });
    sis(R, SIS1, .5); R.L.int = .7;
  });
  // H3 · ayrıntı · C3–C5 · ekmekler tablet satırları gibi üst üste: her sıra bir gün (solda çivi sayısı); kamera anılan satıra iner
  // (birincisi → beşincisi → yedincisi; aradaki satırlar geçerken okunur). Anılan ekmeğe meşale ışığı; yedincisi közde parlar.
  const RY = i => 300 + i * 230, RX = 640;
  function civi(R, x, y, n) {
    for (let k = 0; k < n; k++) { const cx = x + (k % 4) * 40, cy = y + Math.floor(k / 4) * 84;
      R.d.fillStyle = dv(-.9); R.d.beginPath(); R.d.moveTo(cx - 15, cy - 32); R.d.lineTo(cx + 15, cy - 32); R.d.lineTo(cx, cy + 34); R.d.closePath(); R.d.fill(); }
  }
  KAYIT(2, 'H3', 'ayrinti', (R, st) => {
    const DUR_ = [['C3@birincisi', 0], ['C4@beşincisi', 4], ['C5@yedincisi', 6]].map(([a, r]) => [A(a), r]);
    let y = RY(0) - 120 + 120 * ramp(st.t, KS(2), DUR_[0][0], E.out3), cur = 0;
    for (let k = 1; k < 3; k++) { const [t, r] = DUR_[k], [tp, rp] = DUR_[k - 1]; y = lerp(y, RY(r), ramp(st.t, t - 1.1, t - .05, E.io3)); if (st.t >= t - .3) cur = r; else if (st.t >= tp - .3) cur = rp; }
    R.cam(545, clamp(y + 40, 90 + 960 / 1.55, 1560), 1.55);
    SET.zemin(R);
    R.b.fillStyle = gv(.34); R.b.fillRect(80, 120, 940, 1720);
    cizgi(R, [[80, 120], [1020, 120], [1020, 1840], [80, 1840], [80, 120]], 6, -.7);
    R.b.fillStyle = gv(.22); R.b.fillRect(60, 1840, 980, 420); R.m.fillStyle = '#5A3422'; R.m.fillRect(60, 1840, 980, 420);
    for (let k = 0; k < 26; k++) { const x = 120 + hash(k * 1.3) * 860, yy = 1880 + hash(k * 2.9) * 300, r = 14 + hash(k * 4.1) * 22;
      R.b.fillStyle = gv(.3 + hash(k) * .1); R.b.beginPath(); R.b.arc(x, yy, r, 0, TAU); R.b.fill(); }
    R.after(c => { c.globalCompositeOperation = 'screen'; const fl = .8 + .2 * Math.sin(st.t * 5.3);
      for (let k = 0; k < 26; k++) { const x = 120 + hash(k * 1.3) * 860, yy = 1880 + hash(k * 2.9) * 300, r = 10 + hash(k * 4.1) * 16;
        const g = c.createRadialGradient(x, yy, 0, x, yy, r * 2.2); g.addColorStop(0, `rgba(255,140,50,${(.55 * fl * (.5 + hash(k * 9) * .5)).toFixed(3)})`); g.addColorStop(1, 'rgba(255,90,20,0)');
        c.fillStyle = g; c.beginPath(); c.arc(x, yy, r * 2.2, 0, TAU); c.fill(); } });
    for (let i = 0; i < 7; i++) {
      const yy = RY(i);
      cizgi(R, [[100, yy + 85], [1000, yy + 85]], 5, -.85);
      civi(R, 250, yy - 10 - (i >= 4 ? 30 : 0), i + 1);
      YAR.ekmek(R, RX, yy + 70, 150, EKMEK[i]);
    }
    const [sx, sy] = R.scr(RX, RY(cur));
    R.L.pts.push({ x: sx, y: sy - 120, z: 260 * R.z, r: 700 * R.z, i: .6, col: [1.15, .78, .45] });
    const kor = ramp(st.t, DUR_[2][0] - .3, DUR_[2][0] + .6, E.io2);
    if (kor > 0) { const [kx, ky] = R.scr(RX, RY(6) + 85); R.L.pts.push({ x: kx, y: ky, z: 50 * R.z, r: 520 * R.z, i: 1.6 * kor, col: [1.3, .5, .15] }); }
    R.L.dir = [-.5, -.6, .6]; R.L.int = .75; R.L.amb = .26;
  });
  // H4 · geniş · C6 · hızlandırılmış günler: ışık bir kez döner, duvara yedi çentik kazınır, önde yedi ekmek gün gün belirir; o uyuyor.
  KAYIT(3, 'H4', 'genis', (R, st) => {
    kay(R, st, [540, 1020, .9], [540, 1000, .97]);
    const p = ramp(st.t, A('C6@her') - .1, Se('C6') + .1, E.lin), a = lerp(-.9, .9, E.io2(p));
    oda(R, st, { poz: { ...uyku(1), egilme: .24 + nefes(st.t) }, centik: p, ekmek: p * 7, mesale: .45, isik: [Math.sin(a) * .7, -.6, .55], kor: p > .98 ? 1 : 0 });
    sis(R, 1, .5); R.L.int = .8;
  });
  // H5 · orta · C7 · geri dönüş, şartın verildiği an: ekmek ve çentik yok, meşale tam. Dik oturur, gözler açık;
  // 'şart'ta ağır bir kırpma, 'yedi gece'de baş düşer ve silkinip kalkar, 'uyumamak'ta yeniden ağırlaşır.
  KAYIT(4, 'H5', 'orta', (R, st) => {
    kay(R, st, [520, 900, 1.02], [525, 950, 1.12]);
    const kirp = ramp(st.t, A('C7@şart') - .05, A('C7@şart') + .12, E.lin) * (1 - ramp(st.t, A('C7@şart') + .2, A('C7@şart') + .35, E.lin));
    const dus = ramp(st.t, A('C7@yedi') - .2, A('C7@gece') + .15, E.in2) * (1 - ramp(st.t, A('C7@gece') + .15, A('C7@gece') + .35, E.out3))
              + ramp(st.t, A('C7@uyumamak'), KE(4), E.in2) * .5;
    oda(R, st, { poz: { egilme: .08 + nefes(st.t) + dus * .14, bas: .02 + dus * .4, kapali: kirp > .5 || dus > .55 }, mesale: 1 });
    R.L.int = 1;
  }, { tr: COZ });
  // H6 · yakın · C8–C9 · şimdi: uyanır; baş kalkar, gözler açılır ('ölümü'); 'yenemedin'de baş yeniden eğilir (yenilgi). Sis dağılır.
  KAYIT(5, 'H6', 'yakin', (R, st) => {
    kay(R, st, [615, 930, 1.66], [600, 900, 1.76]);
    const u = 1 - ramp(st.t, A('C8@ölümü') - .1, A('C8@ölümü') + .8, E.out3), egik = ramp(st.t, A('C9@yenemedin') - .1, Se('C9') + .4, E.io2);
    oda(R, st, { poz: { egilme: lerp(.08, .24, u) + egik * .1, bas: lerp(0, .78, u) + egik * .22, kapali: u > .5 }, centik: 1, ekmek: 7, mesale: lerp(.45, .8, 1 - u), kor: 1 });
    sis(R, lerp(SIS1, 1.1, 1 - u), lerp(1, .25, 1 - u)); R.L.int = lerp(.62, .85, 1 - u);
  }, { tr: COZ });
  // H7 · orta → yakın · C10 · geri dönüş: 'oturdun'da dik oturuyor (ekmek yok); 'gözünü'de baş düşer, gözler kapanır; sis iner,
  // meşale kısılır; kamera H1'in kadrajına yaklaşır: son kare ilk kareye bağlanır (döngü). Kuyrukta cevap yazısı (kurgu.yazilar).
  KAYIT(6, 'H7', 'orta', (R, st) => {
    const t0 = A('C10@gözünü') - .15, u = ramp(st.t, t0, A('C10@kapadın', 0) + .2, E.io2);
    const z = ramp(st.t, A('C10@ve') - .2, DUR - .2, E.io2);
    R.cam(lerp(525, ILK[0], z), lerp(940, ILK[1], z), lerp(1.08, ILK[2], z));
    // 'bir an' yedi gün olur: gözler kapanınca çentikler bir bir kazınır, H1'in duvarına varır (döngü dikişi)
    const cen = ramp(st.t, A('C10@kapadın') + .25, DUR - .25, E.lin);
    oda(R, st, { poz: { ...uyku(u), egilme: lerp(.08, .24, u) + nefes(st.t) }, mesale: lerp(1, .45, u), centik: cen, ekmek: Math.min(7, cen * 7.4), kor: 1.2 * ramp(st.t, DUR - .9, DUR - .25, E.io2) });
    sis(R, lerp(-.1, SIS0, ramp(st.t, t0, DUR, E.lin)), 1); R.L.int = lerp(1, .62, u);
  }, { tr: COZ });
})();
