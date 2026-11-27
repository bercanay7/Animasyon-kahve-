// Plan listesi, bölüm C–I. H: planlar.js yardımcıları ({kamYol, yigin, duser, bademDali, figurBas, yazi, tabloMaske, kareD}).
import { W, A, S, Se, plan, sm, clamp, lerp, io, hsh, ikiser, mRect, mDaire, mTam, mx, MW, ekrana } from './film_t.js';
import { nesneMaske, nesne } from './nesne.js';
import { tuvalK } from './set_masa.js';
import { SALON, cerceveListesi } from './set_salon.js';
import { ODA, TK } from './set_oda.js';
import { BRUSH, DAB, KNIFE } from '../../araclar/tablo/impasto.js';

export function planlar2(M, IMG, FIG, H) {
  const { kamYol, yigin, duser, bademDali, figurBas, yazi, tabloMaske, mSil } = H;
  const SE = SALON.ekr, OE = ODA.ekr;
  const cIdx = (st, at) => A(at) - st.at;                     // plan içi kelime zamanı
  const sabit = (x, y, z) => () => ({ x, y, z });
  // şövale (canlı darbeler; ekran koordinatı): iki ayak tepede birleşir (A), arka ayak kısa; tuval rafı yalnız ayakların arasında (kesişen çubuk = haç)
  const sovale = (S, x, y, h, k = 1) => { const c = [.16, .12, .09], tep = [x, y - h];
    for (const dx of [-.3, .3]) { const ax = x + dx * h * .55; S.push({ x: (ax + tep[0]) / 2, y: (y + tep[1]) / 2, ang: Math.atan2(tep[1] - y, tep[0] - ax), len: Math.hypot(tep[0] - ax, tep[1] - y), wid: 7 * k, c, c2: c, seed: dx * 9, type: KNIFE, alpha: 1, hgt: .5 }); }
    const ry = y - h * .38, sp = .3 * h * .55 * (1 - .38) * .96; S.push({ x, y: ry, ang: 0, len: sp * 2 * .92, wid: 7 * k, c, c2: c, seed: 3, type: KNIFE, alpha: 1, hgt: .5 }); };
  // beşik (canlı darbeler, yandan): açık ahşap yuvarlak gövde, kavisli sallanma ayakları, baş ucunda yarım kubbe, üstte yumuşak beyaz örtü.
  //   Çubuk, ızgara, kapalı kutu yok (çubuk + kuşak = haç; koyu kutu = tabut)
  const besik = (S, x, y, w, sal = 0) => { const h = w * .38, c = [.58, .48, .38], ac = sal * .04;
    const P_ = (u, v) => [x + u * Math.cos(ac) - v * Math.sin(ac), y + u * Math.sin(ac) + v * Math.cos(ac)];
    for (let i = 0; i <= 10; i++) { const u = -w / 2 + w * i / 10, v = -h * .25 - Math.sqrt(Math.max(0, 1 - (2 * u / w) ** 2)) * h * .55; const [px, py] = P_(u, v * .5);   // gövde: alt yarım elips
      S.push({ x: px, y: py, ang: ac + Math.PI / 2, len: h * .6 * Math.sqrt(Math.max(.15, 1 - (2 * u / w) ** 2)), wid: w / 10 * 1.3, c, c2: c.map(q => q * .82), seed: i, type: BRUSH, alpha: 1, hgt: .5 }); }
    for (let i = 0; i < 12; i++) { const u = -w * .55 + w * 1.1 * i / 11, v = h * .08 + (2 * u / w) ** 2 * h * .12; const [px, py] = P_(u, v);   // sallanma ayağı: kavis
      S.push({ x: px, y: py, ang: ac + Math.atan(2 * (2 * u / w) * .12 * 2 * h / w), len: w * .11, wid: 8, c: c.map(q => q * .7), seed: 20 + i, type: KNIFE, alpha: 1, hgt: .4 }); }
    for (let i = 0; i < 6; i++) { const t = Math.PI * (.5 + i / 10), [px, py] = P_(-w * .4 + Math.cos(t) * h * .5, -h * .45 - Math.sin(t) * h * .45);   // baş ucu kubbe
      S.push({ x: px, y: py, ang: t + Math.PI / 2 + ac, len: h * .35, wid: h * .3, c: c.map(q => q * .9), seed: 30 + i, type: BRUSH, alpha: 1, hgt: .5 }); }
    for (let i = 0; i < 3; i++) { const [px, py] = P_(-w * .18 + i * w * .2, -h * .5 - 4 * Math.sin(i * 1.7));   // örtü: tek yumuşak gri örtü (v3: dokuz beyaz top pamuk dizisi okunuyordu)
      S.push({ x: px, y: py, ang: ac + (i - 1) * .08, len: w * .34, wid: h * .28, c: [.68, .66, .62], c2: [.6, .58, .55], seed: 40 + i, type: BRUSH, alpha: .95, hgt: .4, taper: .3 }); } };
  // yıldızlar: küçük yuvarlak ışık noktaları (dört kollu ışın yok: haç), titreşir
  const yildizlar = (S, t, n = 40) => { for (let i = 0; i < n; i++) { const x = hsh(i, 1) * 1920, y = 60 + hsh(i, 2) * 420, f = .6 + .4 * Math.sin(t * (2 + 3 * hsh(i, 3)) + i);
    S.push({ x, y, ang: 0, len: 6 + 5 * hsh(i, 4), wid: 6 + 5 * hsh(i, 4), c: [1, .96, .84], seed: i, type: DAB, alpha: .8 * f, hgt: .2 }); } };
  // sandık (ODA'da taşınma): perspektifte kutu (ön ve üst yüz)
  const sandik = (S, x, y, w, h, sd) => { const c = [.3, .24, .18];
    S.push({ x, y: y - h / 2, ang: 0, len: w, wid: h, c, c2: c.map(v => v * .85), seed: sd, type: KNIFE, alpha: 1, hgt: .6 });
    S.push({ x: x + w * .06, y: y - h - h * .12, ang: 0, len: w * .95, wid: h * .25, c: c.map(v => v * 1.25), seed: sd + 1, type: KNIFE, alpha: 1, hgt: .5 });
    for (let i = 1; i < 3; i++) S.push({ x, y: y - h * i / 3, ang: 0, len: w * .96, wid: 3, c: c.map(v => v * .6), seed: sd + 2 + i, type: KNIFE, alpha: .8, hgt: .3 }); };
  const T = k => (IMG[k] ? k : null);
  // v3: el yazısı gibi soldan sağa açılan metin (ekran koordinatı; u 0..1)
  const murekkep = (ctx, s_, x, y, px, u, hiz = 'left', a = .92) => { if (u <= 0) return; ctx.save(); ctx.font = `italic 600 ${Math.round(px)}px 'Cormorant Garamond', serif`; ctx.textAlign = hiz; ctx.textBaseline = 'alphabetic';
    const w = ctx.measureText(s_).width, x0 = hiz === 'center' ? x - w / 2 : x; ctx.beginPath(); ctx.rect(x0 - 4, y - px * 1.1, (w + 8) * clamp(u), px * 1.5); ctx.clip(); ctx.globalAlpha = a; ctx.fillStyle = '#2a1f18'; ctx.fillText(s_, x, Math.min(y, 860)); ctx.restore(); };
  const tabloPlan = (id, at, ad, olcek, not, kam, o = {}) => plan({ id, at, sahne: 'tb_' + ad, olcek, not, kamera: kam, durum: o.durum, maske: o.maske || ((st, kam) => mTam(o.renk ? o.renk(st) : 1)), bitir: o.bitir, ust: o.ust });

  // ================= C: Sarı ev =================
  // C01 · yakin · MASA: gri bir zarfın adresi yazılır (el yok: yazı kendiliğinden belirir), zarf aşağı kayar (posta torbası)
  plan({ id: 'C01', at: 'C01', sahne: 'masa', olcek: 'yakin', not: 'Arles\'dan mektup: adres yazılır',
    kamera: kamYol([960, 420, 1.3], [960, 440, 1.4], u => u),
    durum: st => ({ cekmece: false, nesneler: t => { const u = clamp(t / 2.6), k = io(clamp((t - st.d + 1.3) / 1.1));
      return [{ tur: 'zarf', renk: 'gri', yuz: 'on', yazi: u, x: 960, y: 430 + 700 * k, w: 420, h: 260, rot: -.03, tohum: 120, golge: true, kalk: k * .5 }]; } }) });
  // C02 · ayrinti · MASA (v3): adres yazılır, zarf "yollar"da sağa kayıp kadrajdan çıkar; "ikincisi"nde açılmış, adresi karalanmış, kenarı yırtık geri döner
  plan({ id: 'C02', at: 'C02', sahne: 'masa', olcek: 'ayrinti', not: 'Eski adres: zarf gider, açılmış hâlde geri döner',
    kamera: kamYol([980, 420, 1.6], [960, 430, 1.7], u => u),
    durum: st => { const ty = cIdx(st, 'C02@yollar'), ti = cIdx(st, 'C02@ikincisi'), kx = t => (t < ti ? io(clamp((t - ty + .5) / 1.0)) : 1 - io(clamp((t - ti) / 1.2)));
      return { cekmece: false, nesneler: t => { const k = kx(t); return [{ tur: 'zarf', renk: 'gri', yuz: 'on', yazi: clamp(t / 1.6), x: 960 + 1300 * k, y: 430, w: 400, h: 250, rot: -.04 + .12 * k + (t > ti ? .02 * Math.sin(t * 2.3) : 0), tohum: 130, golge: true, kalk: k * .3 }]; },
        ust: (t, S) => { if (t < ti) return; const k = kx(t), x = 960 + 1300 * k; for (let i = 0; i < 3; i++) S.push({ x: x - 20 + i * 8, y: 430 + i * 14, ang: -.05 + i * .04, len: 190, wid: 4, c: [.12, .1, .09], seed: i, type: KNIFE, alpha: .85, hgt: .2 });   // karalama
          S.push({ x: x + 205, y: 430, ang: Math.PI / 2, len: 240, wid: 14, c: [.6, .58, .52], seed: 9, type: BRUSH, alpha: .9, hgt: .4 }); } }; } });   // yırtık kenar
  // C03 · genis · SALON (Bağımsızlar 1888, v3): cepheden bölme duvar; "üç"te üç gri çerçeve birer birer asılır (önleri gösterilmez; hangi tablolar olduğu iddia edilmez)
  //   F08'de aynı duvara on çerçeve asılır (eşleme). Yürüyen figür ve kopuk gölgesi kaldırıldı.
  const C3 = [760, 960, 1160].map((x, i) => ({ tur: 'cerceve', x, y: 470, w: 150, h: 118, tohum: 140 + i, ic: [.5 + .04 * i, .48, .43], cer: 9 }));
  plan({ id: 'C03', at: 'C03', sahne: 'salon', olcek: 'genis', not: 'Bağımsızlar 1888: üç tablo asılır',
    kamera: kamYol([960, 520, 1.12], [960, 510, 1.24], u => u),
    durum: st => { const tu = cIdx(st, 'C03@üç'); return { duvar: 'seyrek', bolme: true, nesneler: t => C3.map((c, i) => { const u = io(clamp((t - tu + .2 - i * .4) / .45)); return u > 0 ? { ...c, y: c.y - 40 * (1 - u), a: u, kalk: .3 * (1 - u), golge: true } : null; }).filter(Boolean) }; } });
  // C04 · orta · SARI EV (tablo dünyası, gri): siluet kapıyı açar; "sarı"da renk evden yayılır (plan içinde palet değişimi)
  tabloPlan('C04', 'C04', 'sari_ev', 'orta', 'Sarı ev: "sarı"da renk', kamYol([980, 560, 1.12], [1000, 540, 1.2], u => u),
    { renk: st => { const ts = cIdx(st, 'C04@sarı'); return 0; },
      maske: (st, kam) => { const ts = cIdx(st, 'C04@sarı'), c = M.camK(kam, .72); mDaire(c, 1060, 520, 1400 * io(clamp((st.lt - ts) / 1.6)), 1, 14); } });
  // C05 · genis · RHÔNE ÜZERİNDE YILDIZLI GECE (v3; Eylül 1888, mektubun anlattığı tablo): gri gece kıyısı; "yıldızları"nda renk gökten aşağı yayılır
  //   (v2: gri gece, boş şövale, 6 sn durgun)
  tabloPlan('C05', 'C05', 'rhone', 'genis', 'Geceleri yıldızları boyamak için: Rhône', kamYol([960, 470, 1.18], [960, 520, 1.06], u => u),
    { durum: st => ({ expo: () => 1.32 }), maske: (st, kam) => { const ty = cIdx(st, 'C05@yıldızları'), c = M.camK(kam, .72); mDaire(c, 900, -300, 1800 * io(clamp((st.lt - ty + .2) / 2.2)), 1, 18); } });
  // C06 · orta · ODA gece: Theo masaya eğilmiş mektup okur
  plan({ id: 'C06', at: 'C06', sahne: 'oda', olcek: 'orta', not: 'Sanatçılara para verirken sen de sanatçı işi yapıyorsun',
    kamera: kamYol([1180, 600, 1.35], [1220, 610, 1.45], u => u),
    durum: st => ({ tablo: 'oda_otoportre', isik: 'gece', figur: (t, S) => figurBas(S, FIG.theo_oku, t, [1260, 1160], 640, { gunes: ODA.LAMBA }) }) });
  // C07 · yakin · YATAK ODASI tablosu kadrajı doldurur, kamera yaklaşır (renkli)
  tabloPlan('C07', 'C07', 'yatak', 'yakin', 'Yatak Odası tablosu', kamYol([960, 540, 1.0], [960, 560, 1.18], u => u));
  // C08 · ayrinti · MASA gece (v3): mektup masada; "ikimizin"de bir sarı (Vincent'in) ve bir gri (Theo'nun) zarf iki yandan kayar, "birlikte"de yan yana durur.
  //   C06'yla aynı kare oluyordu (eğilen Theo); ölçek değişti
  plan({ id: 'C08', at: 'C08', sahne: 'masa', olcek: 'ayrinti', not: 'Bir yıl sonra birlikte: iki zarf yan yana',
    kamera: kamYol([960, 440, 1.45], [960, 450, 1.55], u => u),
    durum: st => { const ti = cIdx(st, 'C08@ikimizin'); return { cekmece: false, nesneler: t => { const u = io(clamp((t - ti + .3) / 1.4));
      return [{ tur: 'kagit', x: 960, y: 330, w: 560, h: 340, rot: -.02, tohum: 145, satir: 9, olc: 1, yazi: 1, golge: true },
        { tur: 'zarf', renk: 'sari', yuz: 'on', x: lerp(-200, 790, u), y: 640, w: 300, h: 180, rot: -.05 + .05 * u, tohum: 146, golge: true, kalk: .3 * (1 - u) },
        { tur: 'zarf', renk: 'gri', yuz: 'on', x: lerp(2120, 1130, u), y: 645, w: 300, h: 180, rot: .06 - .05 * u, tohum: 147, golge: true, kalk: .3 * (1 - u) }]; } }; },
    maske: (st, kam) => { const ti = cIdx(st, 'C08@ikimizin'), u = io(clamp((st.lt - ti + .3) / 1.4)); nesneMaske(M.camK(kam, 0), { x: lerp(-200, 790, u), y: 640, w: 300, h: 180, rot: -.05 + .05 * u }); } });
  // C09 · genis · SARI EV (gri): sabah, valizli siluet eve yürür (Gauguin)
  tabloPlan('C09', 'C09', 'sari_ev', 'genis', 'Gauguin gelir (Sarı Ev renkli kalır)', kamYol([960, 540, 1.0], [960, 540, 1.06], u => u),
    { durum: st => ({ figur: (t, S) => figurBas(S, FIG.gauguin_yuru, t, [760 + 60 * t, 1030 - 30 * t], 300 - 14 * t, { dongu: false, gunes: [1600, 200], hava: [.5, .48, .44], havaK: .15 }) }) });
  // C10 · ayrinti · MASA: iki gri zarf yan yana kapanır (iki ressam)
  plan({ id: 'C10', at: 'C10', sahne: 'masa', olcek: 'ayrinti', not: 'Zarflar güneyde iki ressamı geçindiriyor',
    kamera: kamYol([960, 420, 1.4], [960, 420, 1.48], u => u),
    durum: st => ({ cekmece: false, nesneler: t => [0, 1].flatMap(i => { const u = io(clamp((t - .4 - i * .5) / 1)); return [{ tur: 'zarf', renk: 'gri', yuz: 'arka', x: 720 + i * 480, y: 430, w: 380, h: 230, rot: -.04 + i * .06, tohum: 150 + i, golge: true },
      { tur: 'banknot', x: lerp(720 + i * 480 - 260, 720 + i * 480, u), y: lerp(250, 430, u), w: 260 * (1 - .3 * u), h: 130 * (1 - .3 * u), rot: -.2 + .2 * u, tohum: 160 + i, a: 1 - sm(.85, 1, u), kalk: .3 * (1 - u) }]; }) }) });

  // ================= D: Gece treni =================
  // D01 · orta · ODA (kış ışığı): Theo ve Jo yan yana, aralarındaki mesafe B07'dekinden az; kamera geri çekilir
  plan({ id: 'D01', at: 'D01', sahne: 'oda', olcek: 'orta', not: 'Nişan: Theo ve Jo yan yana',
    kamera: kamYol([700, 560, 1.45], [760, 560, 1.3], u => u),
    durum: st => ({ tablo: 'oda_otoportre', isik: 'kis', figur: (t, S) => { figurBas(S, FIG.theo_dur, t, [600, 1000], 520, { gunes: [350, 400] }); figurBas(S, FIG.jo_dur, t + 2, [820 - 60 * io(clamp((t - cIdx(st, 'D01@nişanlanır')) / 1.2)), 1000], 480, { gunes: [350, 400] }); } }) });
  // D02 · ayrinti · MASA gece (v3): Theo bir mektup yazıyor (satırlar ilerler, kalem kayar); "kriz"de kalem durur, ışık kısılır; "ertesi"de telgraf kâğıdı alttan kayar
  //   (boş masa 2,8 sn sürüyordu; yazı okunmaz; Arles, beden, oda gösterilmez)
  plan({ id: 'D02', at: 'D02', sahne: 'masa', olcek: 'ayrinti', not: 'Kriz: kalem durur; telgraf',
    kamera: kamYol([960, 430, 1.5], [960, 440, 1.58], u => u),
    durum: st => { const tk = cIdx(st, 'D02@kriz'), tg = cIdx(st, 'D02@ertesi'); return { cekmece: false, expo: t => .95 - .12 * sm(tk, tk + 1, t),
      nesneler: t => { const y = clamp(Math.min(t, tk) / (tk + .4)), k = 1 - io(clamp((t - tg) / 1.2));
        return [{ tur: 'kagit', x: 860, y: 420, w: 460, h: 560, rot: -.03, tohum: 168, satir: 12, yazi: 1, akis: .15 + .6 * y, olc: .95 },
          { tur: 'kalem', x: 760 + 300 * y + (t > tk ? 60 * io(clamp((t - tk) / .6)) : 0), y: 300 + 220 * y, w: 250, h: 10, rot: -.6, tohum: 169, kalk: t < tk ? .3 : .3 * (1 - io(clamp((t - tk) / .6))) },
          ...(t < tg ? [] : [{ tur: 'telgraf', x: 1100, y: 470 + 600 * k, w: 420, h: 300, rot: .05, tohum: 170, satir: 5, golge: true, kalk: k * .2 }])]; } }; } });
  // D03 · genis · TREN: gece soldan sağa; sabah ışığı; akşam sağdan sola geri
  plan({ id: 'D03', at: 'D03', sahne: 'tren', olcek: 'genis', not: 'Noel: gidiş ve aynı akşam dönüş',
    kamera: kamYol([960, 560, 1.04], [960, 560, 1.08], u => u),
    durum: st => { const ts = cIdx(st, 'D03@noel'), ta = cIdx(st, 'D03@aynı'); return { gun: t => sm(ts - .4, ts + .6, t) * (1 - sm(ta, ta + 1, t)),
      tren: t => (t < ta ? [[-300 + 700 * t, 1]] : [[2500 - 700 * (t - ta), -1]]) }; } });
  // D04 · yakin · MASA: iki tren bileti zarf yığınının yanına düşer; lamba titrer
  plan({ id: 'D04', at: 'D04', sahne: 'masa', olcek: 'yakin', not: 'Yolculuğun tutarı hiçbir zarfa yazılmaz',
    kamera: kamYol([960, 420, 1.3], [960, 430, 1.36], u => u),
    durum: st => ({ cekmece: false, nesneler: t => [...yigin(6, { x: 760, y: 460, dx: 120, dy: 60, renk: 'gri', tohum: 180 }), ...[0, 1].map(i => { const z = duser({ tur: 'bilet', x: 1180 + i * 70, y: 470 + i * 30, w: 170, h: 90, rot: .2 - i * .3, tohum: 190 + i }, t, .3 + i * .4, .5); return z; }).filter(Boolean)] }) });
  // D05 · orta · SARI EV (gri): Vincent eve yürür (hastaneden dönüş)
  tabloPlan('D05', 'D05', 'sari_ev', 'orta', 'Hastaneden çıkar (Sarı Ev renkli)', kamYol([900, 600, 1.18], [940, 590, 1.24], u => u),
    { durum: st => ({ figur: (t, S) => figurBas(S, FIG.vincent_yuru, t, [820 + 50 * t, 1060 - 20 * t], 340 - 12 * t, { dongu: false, gunes: [1600, 200], hava: [.5, .48, .44], havaK: .15 }) }) });
  // D06 · genis · ODA (sabah, v3): yeni daire; Theo ile Jo birbirine dönük (Jo yere basar, masanın önünde değil); "taşınırlar"da Theo yazı masasını gösterir (D07'ye köprü)
  plan({ id: 'D06', at: 'D06', sahne: 'oda', olcek: 'genis', not: 'Evlilik ve yeni daire: Theo masayı gösterir',
    kamera: kamYol([960, 540, 1.0], [980, 545, 1.06], u => u),
    durum: st => { const tt = cIdx(st, 'D06@taşınırlar'); return { tablo: 'oda_otoportre', isik: 'sabah', ust: (t, S) => { sandik(S, 240, 1040, 200, 130, 1); sandik(S, 1560, 1060, 220, 140, 3); sandik(S, 1700, 1040, 150, 100, 2); },
      figur: (t, S) => { figurBas(S, FIG.theo_goster, t - (tt - 2.1), [520, 1010], 470, { gunes: [350, 300], dongu: false }); figurBas(S, FIG.jo_yan, t + 3, [860, 1000], 430, { gunes: [350, 300] }); } }; } });
  // D07 · orta · MASA: çekmece açılır, içi gri zarflarla dolu (eski mektuplar); kamera masadan çekmeceye iner
  const D7g = yigin(30, { renk: 'gri', tohum: 400 });
  plan({ id: 'D07', at: 'D07', sahne: 'masa', olcek: 'orta', not: 'Jo çekmeceyi açar: mektuplarla dolu',
    kamera: kamYol([1000, 700, 1.55], [960, 760, 1.25]),   // A03'ün kamerasından açılır (çerçeve kapanır ve yeniden açılır)
    durum: st => { const ta = cIdx(st, 'D07@açar'); return { nesneler: () => D7g, cekmeceAc: t => .07 + .93 * io(clamp((t - ta) / 1.1)),
      golge: (t, S) => figurBas(S, FIG.jo_dur, t, [1640, 2900], 3000, { golge: .2 * (1 - sm(st.d - 1.5, st.d, t)), adim: 2, temas: false }) }; } });
  // D07b · yakin · MASA: "Sonra hafta hafta": filmin ilk sarı zarfları gri yığının üstüne düşer, çekmece kabarır
  const D7s = yigin(26, { tohum: 430, dy: 160, kat: .8 });
  plan({ id: 'D07b', at: 'D07@sonra', sahne: 'masa', olcek: 'yakin', not: 'Sarı zarflar başlar (ilk kez)',
    kamera: kamYol([960, 820, 1.3], [960, 790, 1.42], u => u),
    durum: st => { const ts = cIdx(st, 'D07@sarı'); return { nesneler: t => [...D7g, ...D7s.map((it, i) => duser(it, t, ts + i * .28, .45)).filter(Boolean)] }; },
    maske: (st, kam) => { const ts = cIdx(st, 'D07@sarı'), c = M.camK(kam, 0); D7s.forEach((it, i) => { const z = duser(it, st.lt, ts + i * .28, .45); if (z) nesneMaske(c, z); }); } });

  // ================= E: Bir yılda yüz elli resim =================
  // E01 · genis · SELVİLİ TARLA (gri dünya): duvarla çevrili hastane bahçesinin ötesi; kamera yavaş kayar
  tabloPlan('E01', 'E01', 'selvili_tarla', 'genis', 'Saint-Rémy: gri dünya; yürüyen siluet', kamYol([860, 560, 1.14], [1040, 530, 1.02], u => u), { maske: () => {},
    durum: st => ({ figur: (t, S) => figurBas(S, FIG.vincent_yuru, t * .55, [760 + 22 * t, 1020 - 14 * t], 400 - 12 * t, { dongu: false, gunes: [1600, 200], hava: [.5, .48, .44], havaK: .15 }) }) });   // v3: siluet okunur boyda (birkaç pikseldi)
  // E02 · ayrinti · MASA: makbuz ve banknotlar; başka bir el yazısıyla küçük bir zarf kadraja kayar (kız kardeşler)
  plan({ id: 'E02', at: 'E02', sahne: 'masa', olcek: 'ayrinti', not: 'Hastane parası; kız kardeşlerin katkısı',
    kamera: kamYol([960, 430, 1.5], [960, 440, 1.56], u => u),
    durum: st => { const tk = cIdx(st, 'E02@kız'); return { cekmece: false, nesneler: t => [{ tur: 'kagit', x: 820, y: 430, w: 300, h: 380, rot: -.05, tohum: 200, satir: 6, olc: .9 },
      { tur: 'banknot', x: 1100, y: 380, w: 260, h: 130, rot: .1, tohum: 201 }, ...(t > tk ? [{ tur: 'zarf', renk: 'gri', yuz: 'on', x: 1150 + 700 * (1 - io(clamp((t - tk) / 1))), y: 560, w: 260, h: 160, rot: -.08, tohum: 202, olc: .7, golge: true }] : [])] }; } });
  // E03 · orta · sözcüğe bağlı kesmeler: Selviler → Selvili Buğday Tarlası → Yıldızlı Gece (renkli, tam kare)
  tabloPlan('E03', 'E03', 'selviler', 'orta', 'Selviler', kamYol([960, 540, 1.04], [960, 520, 1.12], u => u));
  tabloPlan('E03b', 'E03@buğday', 'selvili_tarla', 'yakin', 'Selvili Buğday Tarlası', kamYol([1000, 560, 1.12], [960, 540, 1.04], u => u));
  tabloPlan('E03c', 'E03@yıldızlı', 'yildizli', 'orta', 'Yıldızlı Gece', kamYol([960, 520, 1.02], [980, 520, 1.1], u => u));
  // E03d · genis · MOZAİK: "yüz elli resim": duvar boyu Saint-Rémy tabloları; kamera geri çekilir
  plan({ id: 'E03d', at: 'E03@yüz', sahne: 'tb_mozaik', olcek: 'genis', not: 'Yaklaşık yüz elli resim', kamera: kamYol([960, 540, 1.5], [960, 540, 1.0]) });
  // E04 · yakin · SALON (Bağımsızlar 1889, seyrek): salonun ortasındaki bölme duvarda çerçeveli İrisler (renkli, yalnız tuval); Theo sağda omuz üstü, koyu
  const IR = (() => { const [x0, y0] = SE(-1.3, 2.7, -8), [x1, y1] = SE(1.3, .7, -8); return [x0, y0, x1 - x0, y1 - y0]; })();
  plan({ id: 'E04', at: 'E04', sahne: 'salon', olcek: 'yakin', not: 'Bağımsızlar 1889: İrisler (sergide)',
    kamera: kamYol([IR[0] + IR[2] / 2, IR[1] + IR[3] / 2, 1.75], [IR[0] + IR[2] / 2 + 60, IR[1] + IR[3] / 2 + 20, 1.5], u => u),
    durum: st => ({ duvar: 'seyrek', iris: true, figur: (t, S) => figurBas(S, FIG.theo_dur, t, [IR[0] + IR[2] + 200, 1180], 760, { gunes: [960, -300], adim: 2, hava: [.05, .05, .05], havaK: .35 }) }),
    maske: (st, kam) => mRect(M.camK(kam, .72), IR[0] + 6, IR[1] + 6, IR[2] - 12, IR[3] - 12, 1, 2) });

  // ================= F: Badem dalı =================
  // F01 · ayrinti · BADEM: tablonun köşesi (mavi gök, dal ucu); kamera yavaş kayar
  tabloPlan('F01', 'F01', 'badem', 'ayrinti', 'Badem Çiçeği köşesi', kamYol([1500, 300, 2.6], [1380, 330, 2.7], u => u));
  // F02 · orta · MASA (sabah, v3): dergi kapağında başlık (Mercure de France, Ocak 1890); açılır; "övgü"de bir satırın altı mürekkeple çizilir
  const F2k = kamYol([960, 420, 1.1], [960, 430, 1.18], u => u);
  plan({ id: 'F02', at: 'F02', sahne: 'masa', olcek: 'orta', not: 'İlk büyük övgü: Mercure de France', kamera: F2k,
    durum: st => { const tv = cIdx(st, 'F02@övgü'), ta = cIdx(st, 'F02@içinde') - .3; return { cekmece: false, expo: 1.15, nesneler: t => { const u = io(clamp((t - .3) / .8)), ac = io(clamp((t - ta) / 1));
      return [...yigin(10, { x: 520, y: 420, dx: 200, dy: 120, tohum: 500 }), ac < .5 ? { tur: 'dergi', x: 1150, y: 420 - 300 * (1 - u), w: 380, h: 520, rot: .0, tohum: 510, golge: true, kalk: .4 * (1 - u) } : { tur: 'acikdefter', x: 1150, y: 420, w: 760, h: 520, rot: .0, tohum: 511, satirL: 14, satirR: 14 }]; },
      ust: (t, S) => { const u = io(clamp((t - tv) / .9)); if (u <= 0) return; S.push({ x: 1180 + 150 * u, y: 312, ang: 0, len: 300 * u, wid: 4, c: [.16, .12, .1], seed: 5, type: KNIFE, alpha: .9, hgt: .2, taper: .2 }); } }; },
    maske: (st, kam) => { const c = M.camK(kam, 0); for (const it of yigin(10, { x: 520, y: 420, dx: 200, dy: 120, tohum: 500 })) nesneMaske(c, it); },
    ust: (ctx, st) => { const ta = cIdx(st, 'F02@içinde') - .3, u = io(clamp((st.lt - .3) / .8)), a = 1 - sm(ta + .3, ta + .5, st.lt); if (a <= 0) return; const c = M.camK(F2k(st.u), 0), [x, y] = ekrana(c, 1150, 230 - 300 * (1 - u));
      ctx.save(); ctx.globalAlpha = a * .9; ctx.font = `600 ${Math.round(30 * c.zoom)}px 'Cormorant Garamond', serif`; ctx.textAlign = 'center'; ctx.fillStyle = '#2a1f18'; ctx.fillText('MERCURE DE FRANCE', x, Math.min(y, 860));
      ctx.font = `italic 500 ${Math.round(20 * c.zoom)}px 'Cormorant Garamond', serif`; ctx.fillText('Janvier 1890', x, Math.min(y + 30 * c.zoom, 860)); ctx.restore(); } });
  // F03 · yakin · ODA (kış, v3): "oğlu doğar": Jo kucağında bebekle, Theo bebeğe eğilir (tek figür eğilir). Bebek burada ekilir (G02, G04, H01).
  plan({ id: 'F03', at: 'F03', sahne: 'oda', olcek: 'yakin', not: 'Oğul doğar: Jo kucağında bebek, Theo eğilir',
    kamera: kamYol([980, 640, 1.42], [1000, 650, 1.5], u => u),
    durum: st => ({ tablo: 'oda_otoportre', isik: 'kis', figur: (t, S) => { figurBas(S, FIG.theo_egil, t - (cIdx(st, 'F03@oğlu') - 1.2), [800, 1090], 640, { gunes: [350, 300], dongu: false, adim: 2 });
      figurBas(S, FIG.jo_bebek, t, [1170, 1090], 610, { gunes: [350, 300], adim: 2 }); } }) });
  // F03b · ayrinti · MASA (gece): Theo'nun Vincent'e mektubu (31 Ocak 1890); "amcasından"da ad satırların altında ayrı bir satıra mürekkeple yazılır: Vincent
  const F3k = kamYol([960, 430, 1.55], [960, 440, 1.62], u => u);
  plan({ id: 'F03b', at: 'F03@adını', sahne: 'masa', olcek: 'ayrinti', not: 'Mektupta "Vincent" adı yazılır', kamera: F3k,
    durum: st => ({ cekmece: false, nesneler: () => [{ tur: 'kagit', x: 960, y: 440, w: 620, h: 420, rot: -.03, tohum: 220, satir: 6, olc: 1.1, yazi: .9, golge: true }] }),
    ust: (ctx, st) => { const ta = cIdx(st, 'F03@amcasından'), tv = cIdx(st, 'F03@vincent'), k = M.camK(F3k(st.u), 0), [x, y] = ekrana(k, 980, 610);
      murekkep(ctx, 'Vincent', x, y, 72 * k.zoom, clamp((st.lt - ta) / Math.max(.6, tv - ta + .4)), 'center'); } });
  // F04 · genis · BADEM (renk doruğu): dal dal açılır: renk mektup kâğıdından (alt köşe) bütün tabloya yayılır; kamera geri çekilir
  tabloPlan('F04', 'F04', 'badem', 'genis', 'RENK DORUĞU: Badem Çiçeği', kamYol([960, 600, 1.35], [960, 540, 1.0]),
    { maske: (st, kam) => { const c = M.camK(kam, .72); mDaire(c, 600, 980, 2300 * io(clamp(st.lt / 3.2)), 1, 16); } });
  // F05 · ayrinti · BADEM: tek bir çiçeğe iniş; "hastalandım"da ışık çekilir, tablo renkli kalır
  tabloPlan('F05', 'F05', 'badem', 'ayrinti', 'Tek çiçek; hastalandım', kamYol([1080, 420, 1.9], [1100, 400, 2.2], u => u),   // v3: büyütme sınırlandı (çamurlu okunuyordu)
    { durum: st => { const th = cIdx(st, 'F05@hastalandım'); return { expo: t => 1.03 - .35 * sm(th, th + 1.5, t) }; } });
  // F06 · orta · SALON (Brüksel, v3): bölme duvarda Kırmızı Bağ, gri; "resimlerimden"de renklenir; "dört yüz"de çerçeveye "400 fr." kartı asılır (iki koridor boştu)
  const BG = (() => { const im = IMG.kirmizi_bag; if (!im) return null; const ar = im.width / im.height, hy = 1.3, hx = hy * ar, [x0, y0] = SE(-hx / 2, 1.1 + hy, -8), [x1, y1] = SE(hx / 2, 1.1, -8); return [x0, y0, x1 - x0, y1 - y0]; })();
  const F6k = BG ? kamYol([BG[0] + BG[2] / 2, BG[1] + BG[3] / 2 + 20, 1.55], [BG[0] + BG[2] / 2 + 20, BG[1] + BG[3] / 2 + 30, 1.7], u => u) : kamYol([600, 470, 1.9], [640, 470, 2.0], u => u);
  plan({ id: 'F06', at: 'F06', sahne: 'salon', olcek: 'orta', not: 'Brüksel: Kırmızı Bağ 400 franka satılır', kamera: F6k,
    durum: st => { const ts = cIdx(st, 'F06@dört'); return { duvar: 'seyrek', bag: !!BG, nesneler: t => (t < ts || !BG ? [] : [{ tur: 'bilet', x: BG[0] + BG[2] - 30, y: BG[1] + BG[3] + 34 - 24 * (1 - io(clamp((t - ts) / .5))), w: 96, h: 46, rot: .1 + .1 * Math.sin((t - ts) * 4) * Math.exp(-1.5 * (t - ts)), tohum: 520, golge: true, a: io(clamp((t - ts) / .4)) }]) }; },
    maske: (st, kam) => { if (!BG) return; const tr = cIdx(st, 'F06@resimlerimden'); mRect(M.camK(kam, .72), BG[0] + 4, BG[1] + 4, BG[2] - 8, BG[3] - 8, sm(tr - .2, tr + .9, st.lt), 3); },
    ust: (ctx, st) => { if (!BG) return; const ts = cIdx(st, 'F06@dört'), a = io(clamp((st.lt - ts) / .4)); if (a <= 0) return; const c = M.camK(F6k(st.u), .72), [x, y] = ekrana(c, BG[0] + BG[2] - 30, BG[1] + BG[3] + 34 - 24 * (1 - io(clamp((st.lt - ts) / .5))));
      ctx.save(); ctx.globalAlpha = a; ctx.translate(x, Math.min(y, 860)); ctx.rotate(.1 + .1 * Math.sin((st.lt - ts) * 4) * Math.exp(-1.5 * (st.lt - ts))); ctx.font = `italic 700 ${Math.round(26 * c.zoom)}px 'Cormorant Garamond', serif`; ctx.fillStyle = '#2a1f18'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText('400 fr.', 0, 2); ctx.restore(); } });
  // F07 · ayrinti · MASA (v3): hesap defteri; "deftere"de "400 fr." satırı mürekkeple yazılarak belirir
  const F7k = kamYol([960, 440, 1.5], [960, 450, 1.58], u => u);
  plan({ id: 'F07', at: 'F07', sahne: 'masa', olcek: 'ayrinti', not: 'Defterde satır yazılır', kamera: F7k,
    durum: st => ({ cekmece: false, nesneler: () => [{ tur: 'acikdefter', x: 960, y: 440, w: 900, h: 600, rot: -.02, tohum: 530, satirL: 12, satirR: 3, yazi: 1 }] }),
    ust: (ctx, st) => { const td = cIdx(st, 'F07@deftere'), k = M.camK(F7k(st.u), 0), [x, y] = ekrana(k, 1080, 540);
      murekkep(ctx, 'Bruxelles — 400 fr.', x - 90 * k.zoom, y, 48 * k.zoom, clamp((st.lt - td + .2) / 1.4), 'left'); } });
  // F08 · genis · SALON (Bağımsızlar 1890, v3): C03'ün bölme duvarı; on gri çerçeve birer birer asılır (C03'te üçtü; önleri gösterilmez)
  const F8 = Array.from({ length: 10 }, (_, i) => ({ tur: 'cerceve', x: 620 + (i % 5) * 170, y: i < 5 ? 380 : 545, w: 136, h: 108, tohum: 540 + i, ic: [.46 + .08 * hsh(i, 1), .44 + .06 * hsh(i, 2), .4], cer: 8 }));
  plan({ id: 'F08', at: 'F08', sahne: 'salon', olcek: 'genis', not: 'Bağımsızlar 1890: on tablo asılır',
    kamera: kamYol([960, 500, 1.2], [960, 495, 1.3], u => u),
    durum: st => { const t0 = cIdx(st, 'F08@bağımsızlar'), t1 = cIdx(st, 'F08@tablosunu'); return { duvar: 'seyrek', bolme: true, nesneler: t => F8.map((c, i) => { const u = io(clamp((t - t0 - (t1 - t0 + .4) * i / 10) / .35)); return u > 0 ? { ...c, y: c.y - 30 * (1 - u), a: u, kalk: .3 * (1 - u), golge: true } : null; }).filter(Boolean) }; } });

  // ================= G: Auvers'te bir yaz =================
  // G01 · orta · ODA (sabah): hasır şapkalı siluet; beşik önde
  plan({ id: 'G01', at: 'G01', sahne: 'oda', olcek: 'orta', not: 'Amca gelir: hasır şapka, beşik',
    kamera: kamYol([900, 600, 1.35], [930, 600, 1.42], u => u),
    durum: st => ({ tablo: 'oda_guller', isik: 'sabah', figur: (t, S) => figurBas(S, FIG.vincent_dur, t, [620, 1000], 560, { gunes: [300, 300] }) }) });
  // G02 · yakin · ODA (v3): beşiğin kenarı kadrajın altında; iki kardeş ayakta (ikisi birden eğilmez: namaz safı); yalnız Vincent başını eğer ve "tığ"da örtünün ucunu gösterir.
  //   Eller kol tonunda (açık eller kutu ya da şişe okunuyordu)
  plan({ id: 'G02', at: 'G02', sahne: 'oda', olcek: 'yakin', not: 'İki kardeş beşiğin başında; Vincent örtüyü gösterir',
    kamera: kamYol([1000, 660, 1.62], [1000, 670, 1.7], u => u),
    durum: st => { const tg = cIdx(st, 'G02@tığ'); return { tablo: 'oda_guller', isik: 'sabah',   /* v3: beşik kadraj dışında (alt kenarda yarım beşik beyaz kıvrım ve şerit okunuyordu); Vincent eliyle aşağıyı gösterir */
      figur: (t, S) => { figurBas(S, FIG.theo_dur, t, [760, 1290], 860, { gunes: [300, 200], adim: 2 }); figurBas(S, FIG.vincent_goster, t - (tg - 2.2), [1270, 1290], 860, { gunes: [300, 200], adim: 2, dongu: false }); } }; } });
  // G03 · orta · TARLA: tarla kenarında şövale; tuval hızlı kesmelerle gün gün değişir (Auvers 1890 işleri, renkli)
  const AUV = Object.keys(IMG).filter(k => k.startsWith('auvers')).sort();
  plan({ id: 'G03', at: 'G03', sahne: 'tarla', olcek: 'orta', not: 'Auvers: neredeyse her gün bir eser',
    kamera: kamYol([1100, 700, 1.4], [1100, 690, 1.46], u => u),
    durum: st => ({ agac: true, expo: t => 1.0 + .08 * Math.sin(t * 3), figur: (t, S) => sovale(S, 1180, 980, 300, 1.3) }),
    ust: (ctx, st) => { if (!AUV.length) return; const k = Math.min(AUV.length - 1, Math.floor(st.lt / (st.d / AUV.length))), im = IMG[AUV[k]], c = M.camK(kamYol([1100, 700, 1.4], [1100, 690, 1.46], u => u)(st.u), .6);
      const h = 150, w = h * im.width / im.height, [x, y] = ekrana(c, 1180 - w / 2, 760); ctx.save(); ctx.globalAlpha = .96; ctx.drawImage(im, x, y, w * c.zoom, h * c.zoom); ctx.restore(); } });
  // G04 · genis · TARLA: tarla kenarında dört küçük uzak siluet; rüzgârda başaklar, bulut gölgesi
  plan({ id: 'G04', at: 'G04', sahne: 'tarla', olcek: 'genis', not: '8 Haziran: Theo, Jo ve bebek Auvers\'te',
    kamera: kamYol([960, 540, 1.0], [960, 560, 1.08], u => u),
    durum: st => ({ agac: true, figur: (t, S) => { figurBas(S, FIG.vincent_dur, t, [700, 760], 120, { hava: [.4, .36, .38], havaK: .3 }); figurBas(S, FIG.theo_dis_dur, t + 1, [760, 760], 124, { hava: [.4, .36, .38], havaK: .3 }); figurBas(S, FIG.jo_bebek, t + 2, [815, 760], 112, { hava: [.4, .36, .38], havaK: .3 }); } }) });   // v3: Jo kucağında bebek
  // G05 · orta · ODA (öğle, v3): "hastalanır"da Jo beşiğe eğilir; "ayrılmayı"da Theo pencereye döner; "gergin"de Vincent kapıya yürür (üç figür yalnız yer değiştiriyordu)
  plan({ id: 'G05', at: 'G05', sahne: 'oda', olcek: 'orta', not: 'Temmuz: bebek hasta, zam, gergin gün',
    kamera: kamYol([1150, 640, 1.3], [880, 620, 1.36]),
    durum: st => { const th = cIdx(st, 'G05@hastalanır'), ta = cIdx(st, 'G05@ayrılmayı'), tg = cIdx(st, 'G05@gergin'), tz = cIdx(st, 'G05@zam'); return { tablo: 'oda_guller', isik: 'ogle', alev: () => .2,
      nesneler: t => (t > tz ? [{ tur: 'zarf', renk: 'gri', yuz: 'on', x: 1290, y: 872, w: 80, h: 34, rot: .1, tohum: 1800, kalinlik: false, a: sm(tz, tz + .5, t) }] : []),
      figur: (t, S) => { if (t < tg - .3) figurBas(S, FIG.vincent_dur, t, [420, 1000], 500); else figurBas(S, FIG.vincent_yuru, (t - tg + .3) * .9, [420, 1000], 500, { dongu: false });
        figurBas(S, FIG.theo_don, t - (ta - 2.2), [700, 1000], 520, { dongu: false }); figurBas(S, FIG.jo_egil, t - (th - 2.1), [1180, 995], 470, { dongu: false }); } }; } });   // Jo sola dönük, beşik önünde
  // G06 · genis · FIRTINALI GÖK ALTINDA BUĞDAY TARLASI: gri dünya; "tarlaları"nda renk tarladan yükselir
  tabloPlan('G06', 'G06', 'firtina', 'genis', 'Uçsuz bucaksız buğday tarlaları: renk', kamYol([960, 560, 1.06], [960, 540, 1.0], u => u),
    { maske: (st, kam) => { const tt = cIdx(st, 'G06@tarlaları'), c = M.camK(kam, .72); mDaire(c, 960, 1300, 1500 * io(clamp((st.lt - tt) / 2.4)), 1, 18); } });
  // G07 · ayrinti · MASA (gün ışığı): yarım mektup sayfası; satırlar ortada kesilir; kalem yanında. Zarf yok
  plan({ id: 'G07', at: 'G07', sahne: 'masa', olcek: 'ayrinti', not: 'Gönderilmeyen taslak',
    kamera: kamYol([960, 430, 1.4], [960, 450, 1.5], u => u),
    durum: st => { const tb = cIdx(st, 'G07@bitirmez'), tk = cIdx(st, 'G07@konuşturabiliriz'); return { cekmece: false, expo: t => 1.18 - .1 * sm(tk, tk + 2, t), nesneler: t => [{ tur: 'kagit', x: 920, y: 430, w: 520, h: 680, rot: -.03, tohum: 600, satir: 16, yazi: .5 * clamp(t / Math.max(.5, tb)), olc: 1.05 },
      t < tb ? { tur: 'kalem', x: 760 + 360 * clamp(t / Math.max(.5, tb)), y: 300 + 300 * clamp(t / Math.max(.5, tb)), w: 260, h: 10, rot: -.6, tohum: 601, kalk: .3 } : duser({ tur: 'kalem', x: 1330, y: 520, w: 260, h: 10, rot: -.6, tohum: 601 }, t, tb, .5) || { tur: 'kalem', x: 1330, y: 520, w: 260, h: 10, rot: -.6, tohum: 601 }] }; },
    // v3: taslaktaki cümle sayfada yazılarak belirir (Türkçesi bizim; özgün metin VGM RM25)
    ust: (ctx, st) => { const tz = cIdx(st, 'G07@biz'), te = cIdx(st, 'G07@konuşturabiliriz') + .6, k = M.camK(kamYol([960, 430, 1.4], [960, 450, 1.5], u => u)(st.u), 0), [x, y] = ekrana(k, 700, 600), [, y2] = ekrana(k, 700, 650);
      const u = clamp((st.lt - tz + .2) / (te - tz + .2)); murekkep(ctx, 'Biz ancak resimlerimizi', x, y, 40 * k.zoom, clamp(u * 1.8)); murekkep(ctx, 'konuşturabiliriz.', x, y2, 40 * k.zoom, clamp(u * 1.8 - .8)); } });
  // G08 · yakin · MASA (v2, EŞLEME KESMESİ: B04'ün kamerası ve yörüngesi): bu kez banknot değil, rulo bir tuval masaya açılır; "tuvallerin"de renklenir (Selvili Buğday Tarlası);
  //   "payın"da yandaki sarı yığın parlar
  const G8y = yigin(8, { x: 560, y: 420, dx: 160, dy: 100, tohum: 1600 });
  plan({ id: 'G08', at: 'G08', sahne: 'masa', olcek: 'yakin', not: 'Senin de payın var: tuval açılır, renklenir',
    kamera: kamYol([960, 400, 1.3], [960, 400, 1.36], u => u),
    durum: st => { const tt = cIdx(st, 'G08@tuvallerin'), tp = cIdx(st, 'G08@payın'); return { cekmece: false, isik: 'gece', tuval: t => sm(tt - .6, tt + .4, t), expo: t => 1 + .12 * Math.exp(-Math.pow((t - tp - .4) / .5, 2)),
      nesneler: t => { const u = io(clamp(t / 1.2)), ac = io(clamp((t - 1.0) / 1.0)); return [...G8y, { tur: 'zarf', renk: 'gri', yuz: 'arka', x: 1180, y: 520, w: 300, h: 180, rot: -.04, tohum: 1610, golge: true },
        ...(t < tt + .2 ? [{ tur: 'kagit', x: lerp(620, 960, u), y: lerp(330, 400, u), w: 60 + 380 * ac, h: 300, rot: -.3 + .3 * u, tohum: 1620, satir: 0, kalk: .3 * (1 - u), golge: true }] : [])]; } }; },
    maske: (st, kam) => { const c = M.camK(kam, 0), tt = cIdx(st, 'G08@tuvallerin'), tp = cIdx(st, 'G08@payın'); mRect(c, ...tuvalK(IMG), sm(tt, tt + .8, st.lt), 3); for (const it of G8y) nesneMaske(c, it); } });
  // G09 · genis · TARLA (sabah, gri, figürsüz): "öldü"de ışık bulutun ardına çekilir; ardından rüzgâr (sessizlik)
  plan({ id: 'G09', at: 'G09', sahne: 'tarla', olcek: 'genis', not: 'Ölüm: olay gösterilmez',
    kamera: kamYol([960, 560, 1.02], [960, 560, 1.06], u => u),
    durum: st => { const to = cIdx(st, 'G09@öldü'); return { agac: false, ruzgar: .6, expo: t => 1.04 - .22 * sm(to, to + 2, t) }; } });
  // G10 · orta · ODA gece (v2): Theo masada sırttan, baş ve omuz alt üçte birde; dirseğinin yanında lamba ışığında sarı zarf yığını; kamera omuz üstünden yığına kayar
  const G10z = Array.from({ length: 9 }, (_, i) => ({ tur: 'zarf', renk: 'sari', yuz: hsh(i, 4) < .5 ? 'on' : 'arka', x: 1430 + (hsh(i, 1) - .5) * 70, y: 872 + (hsh(i, 2) - .5) * 14 - i * 2, w: 74, h: 30, rot: (hsh(i, 3) - .5) * .3, tohum: 1500 + i, kalinlik: false }));
  plan({ id: 'G10', at: 'G10', sahne: 'oda', olcek: 'orta', not: 'Ah anneciğim: Theo ve sarı zarflar',
    kamera: kamYol([1150, 720, 1.25], [1330, 800, 1.6], u => u),
    durum: st => ({ tablo: 'oda_guller', isik: 'gece', nesneler: () => G10z, figur: (t, S) => figurBas(S, FIG.theo_oku, t + 1, [1000, 1180], 560, { gunes: ODA.LAMBA }) }),
    maske: (st, kam) => { const c = M.camK(kam, .3); for (const it of G10z) nesneMaske(c, it); } });
  // G11 · ayrinti · ODA (kış): G10'un ilk kamera noktası; Theo yok, zarflar yok; lamba cümle bitince söner; kış ışığı masada kayar
  plan({ id: 'G11', at: 'G11', sahne: 'oda', olcek: 'ayrinti', not: 'Theo da öldü: boş masa, lamba söner',
    kamera: kamYol([960 + (ODA.LAMBA[0] - 990) / .61, 540 + (ODA.LAMBA[1] - 500) / .61, 2.6], [960 + (ODA.LAMBA[0] - 975) / .61, 540 + (ODA.LAMBA[1] - 510) / .61, 2.95], u => u),   // oda katmanı d .3: kamera x = 960 + (k.x − 960)·0,61   // v3: lamba ayrıntı ölçeğinde (küçük karede sönüşü seçilmiyordu)
    durum: st => { const ts = Se('G11') - st.at + .3; return { tablo: 'oda_guller', isik: 'kis', alev: t => 1 - sm(ts, ts + 1.6, t) }; } });

  // ================= H: Çekmecedeki mektuplar =================
  // H01 · yakin · ODA (kış ışığı, v3): Jo ¾, kucağında bebek (gri battaniye, baş açıkta: kefen okunmasın); yanında sandıklar ve duvara dayalı tuvaller (arkaları, yalnız çevre çıtası)
  plan({ id: 'H01', at: 'H01', sahne: 'oda', olcek: 'yakin', not: 'Bir bebek, bir çekmece mektup, yüzlerce tablo: Jo',
    kamera: kamYol([760, 700, 1.55], [820, 690, 1.66], u => u),
    durum: st => ({ tablo: 'oda_guller', isik: 'kis', ust: (t, S) => { sandik(S, 1010, 1060, 220, 130, 11); sandik(S, 1200, 1080, 170, 110, 12);
        for (let i = 0; i < 4; i++) nesne(S, { tur: 'tuvalsirt', x: 470 + i * 46, y: 930 - i * 4, w: 150 - i * 8, h: 210 - i * 14, rot: .08 - i * .02, tohum: 20 + i }); },
      figur: (t, S) => figurBas(S, FIG.jo_bebek, t, [840, 1080], 640, { gunes: [350, 300] }) }) });
  // H01t · genis · TREN (gündüz): "Jo, 1891'de … Hollanda'ya döner": sağdan sola
  plan({ id: 'H01t', at: 'H01@jo', sahne: 'tren', olcek: 'genis', not: 'Hollanda dönüşü',
    kamera: kamYol([960, 560, 1.06], [960, 560, 1.0], u => u),
    durum: st => ({ gun: () => 1, tren: t => [[2300 - 300 * t, -1]] }) });
  // H02 · orta · SALON (seyrek): Jo bir çerçevenin önünde durur, geri çekilip bakar
  plan({ id: 'H02', at: 'H02', sahne: 'salon', olcek: 'orta', not: '1892: ilk sergiler',
    kamera: kamYol([760, 500, 1.6], [740, 500, 1.66], u => u),
    durum: st => ({ duvar: 'seyrek', figur: (t, S) => figurBas(S, FIG.jo_dur, t, SE(-1.6, 0, -6.5), 520, { gunes: [960, -300] }) }) });
  // H03 · ayrinti · MASA (v3): hesap defteri; "birer"den başlayarak sağ sayfanın satırları sırayla mürekkeple dolar; köşede sayaç 1'den 192'ye akar (boş defter 10 sn duruyordu)
  plan({ id: 'H03', at: 'H03', sahne: 'masa', olcek: 'ayrinti', not: '34 yılda en az 192 resim: satır satır',
    kamera: kamYol([960, 440, 1.45], [960, 470, 1.55], u => u),
    durum: st => { const tb = cIdx(st, 'H03@birer'); return { cekmece: false, nesneler: t => [{ tur: 'acikdefter', x: 960, y: 440, w: 900, h: 600, rot: -.02, tohum: 700, satirL: 13, satirR: 13, akis: clamp((t - tb) / (st.d - tb - .4)), yazi: 1 }] }; },
    ust: (ctx, st) => { const tb = cIdx(st, 'H03@birer'), t9 = cIdx(st, 'H03@iki') + .2, n = Math.max(1, Math.round(1 + 191 * io(clamp((st.lt - tb) / (t9 - tb))))), a = sm(tb - .2, tb + .2, st.lt);
      yazi(ctx, String(n), 1620, 210, 120, a); yazi(ctx, 'resim', 1620, 270, 48, a * sm(t9 - .3, t9 + .2, st.lt)); } });
  // H04 · yakin · MASA: çekmece: sarı zarflar içeride kalır, lamba ışığı aralıktan süzülür
  const H4 = yigin(36, { tohum: 800 });
  plan({ id: 'H04', at: 'H04', sahne: 'masa', olcek: 'yakin', not: 'Mektupları saklar',
    kamera: kamYol([960, 800, 1.4], [960, 820, 1.46], u => u),
    durum: st => { const ts = cIdx(st, 'H04@saklar'); return { nesneler: () => H4, expo: .95, cekmeceAc: t => 1 - .92 * io(clamp((t - ts) / 1.0)),
      golge: (t, S) => figurBas(S, FIG.jo_dur, t, [1640, 2900], 3000, { golge: (.36) * .55, adim: 2, temas: false }) }; },
    maske: (st, kam) => { const c = M.camK(kam, 0), ts = cIdx(st, 'H04@saklar'); for (const it of H4) nesneMaske(c, it); mSil(c, 0, 625, 1920, .92 * io(clamp((st.lt - ts) / 1.0)) * 575); } });
  // H05 · genis · SALON (1905, v2): G09'dan beri ilk geniş renk dönüşü: "en büyük"te yakın çerçevelerdeki tablolar yakından uzağa birer birer renge açılır; kamera yan duvar boyunca kayar
  const H5L = cerceveListesi('dolu').filter(f => f.z > -17);   // v3: iki duvar (sağ duvar hiç renklenmiyordu); set_salon g1905 ile aynı liste
  const H5k = kamYol([1240, 560, 1.15], [880, 540, 1.3], u => u);
  plan({ id: 'H05', at: 'H05', sahne: 'salon', olcek: 'genis', not: '1905: en büyük sergi; renk geri gelir', kamera: H5k,
    durum: st => ({ duvar: 'dolu', g1905: true, expo: 1.06 }),
    maske: (st, kam) => { const c = M.camK(kam, .72), tb = cIdx(st, 'H05@dört'), k = MW / 1920;   // v3: "484 eserlik"te başlar (cümle bittikten sonra başlıyordu)
      H5L.slice().sort((a, b) => b.z - a.z).forEach((f, i) => { const a = sm(tb + i * .14, tb + i * .14 + .5, st.lt); if (a <= 0) return; const x = f.s * (SALON.GX - .04);
        const Q = [SE(x, f.y + f.yuk, f.z + f.gen / 2), SE(x, f.y + f.yuk, f.z - f.gen / 2), SE(x, f.y, f.z - f.gen / 2), SE(x, f.y, f.z + f.gen / 2)];
        mx.save(); mx.globalAlpha = a; mx.fillStyle = '#fff'; mx.filter = 'blur(1.5px)'; mx.beginPath(); Q.forEach(([X0, Y0], j) => { const [X, Y] = ekrana(c, X0, Y0); j ? mx.lineTo(X * k, Y * k) : mx.moveTo(X * k, Y * k); }); mx.closePath(); mx.fill(); mx.restore(); }); } });
  // H06 · yakin · MASA (v3): sağda sarı zarf yığını; "kayboldu"da yarısı birer birer solar; "üç"te üç kitap (sırtı ve sayfa kenarı görünür) tek tek masaya konur; "girişini"de üstteki açılır.
  //   (tek çizgili koyu levha kara tahta okunuyordu; 7 sn donuktu)
  const H6z = yigin(24, { x: 1380, y: 470, dx: 320, dy: 200, tohum: 920 });
  const H6k = i => ({ tur: 'kitap', x: 700 + i * 14, y: 470 - i * 30, w: 380, h: 280, rot: -.06 + i * .05, tohum: 900 + i, golge: true, renkK: [[.62, .46, .32], [.55, .4, .28], [.66, .5, .34]][i] });
  const h6a = (st, t, i) => { const tk = cIdx(st, 'H06@kayboldu'); return i % 2 ? 1 - sm(tk - .3 + i * .05, tk + .3 + i * .05, t) : 1; };
  plan({ id: 'H06', at: 'H06', sahne: 'masa', olcek: 'yakin', not: 'Kaybolan mektuplar; 1914: üç cilt',
    kamera: kamYol([1000, 450, 1.2], [960, 450, 1.3], u => u),
    durum: st => { const tu = cIdx(st, 'H06@üç'), tg = cIdx(st, 'H06@girişini'); return { cekmece: false, nesneler: t => [
      ...H6z.map((it, i) => ({ ...it, a: h6a(st, t, i) })),
      ...[0, 1, 2].map(i => (i === 2 && t > tg ? { tur: 'acikdefter', x: 740, y: 410, w: 700, h: 280, rot: .02, tohum: 905, satirL: 10, satirR: 6, akis: clamp((t - tg) / 1.2) } : duser(H6k(i), t, tu - .3 + i * .45, .5))).filter(Boolean)] }; },
    maske: (st, kam) => { const c = M.camK(kam, 0); H6z.forEach((it, i) => nesneMaske(c, it, h6a(st, st.lt, i))); } });
  // H07 · genis · TARLA: buğday tarlaları, alçak taş duvar, sarmaşık (mezar taşı, haç, kilise yok)
  plan({ id: 'H07', at: 'H07', sahne: 'tarla', olcek: 'genis', not: 'Auvers: buğday tarlaları arasında',
    kamera: kamYol([960, 560, 1.02], [960, 570, 1.08], u => u), durum: st => ({ agac: false, duvar: true }) });
  // H08 · orta · TARLA: tarla kenarında Jo sırttan, rüzgârda başaklar
  plan({ id: 'H08', at: 'H08', sahne: 'tarla', olcek: 'orta', not: 'Birlikte yatıyorlar',
    kamera: kamYol([900, 700, 1.4], [920, 700, 1.46], u => u),
    durum: st => ({ agac: false, duvar: true, figur: (t, S) => figurBas(S, FIG.jo_dur, t, [860, 990], 430, { gunes: [1500, 500], hava: [.35, .33, .33], havaK: .2 }) }) });
  // H09 · ayrinti · MASA (lamba, v3): solda üç cilt, ortada çevrilmiş sayfa yığını büyür, kalem yazar; "üçte ikisi"nde iki cilde ayraç (çevrilen) girer; "öldüğünde" kalem bırakılır
  //   (G07'deki taslakla aynı kare oluyordu)
  const H9k = i => ({ tur: 'kitap', x: 520 + i * 10, y: 520 - i * 24, w: 300, h: 220, rot: -.05 + i * .04, tohum: 1030 + i, golge: true, renkK: [[.62, .46, .32], [.55, .4, .28], [.66, .5, .34]][i] });
  plan({ id: 'H09', at: 'H09', sahne: 'masa', olcek: 'ayrinti', not: 'Çeviri: üç ciltten ikisi',
    kamera: kamYol([980, 440, 1.32], [980, 450, 1.4], u => u),
    durum: st => { const tu = cIdx(st, 'H09@üçte'), to = cIdx(st, 'H09@öldüğünde'); return { cekmece: false, nesneler: t => { const n = Math.max(1, Math.min(9, 1 + Math.floor(Math.min(t, to) / .55)));
      return [...[0, 1, 2].map(i => ({ ...H9k(i), serit: i < 2 ? sm(tu + i * .3, tu + i * .3 + .4, t) : 0 })),
        ...Array.from({ length: n }, (_, i) => ({ tur: 'kagit', x: 1040 + (hsh(i) - .5) * 12, y: 450 - i * 4, w: 400, h: 540, rot: (hsh(i, 2) - .5) * .06, tohum: 1000 + i, satir: 15, olc: .85, akis: i === n - 1 && t < to ? clamp((t % .55) / .55) : 1 })),
        t < to ? { tur: 'kalem', x: 960 + 280 * clamp((t % .55) / .55), y: 300 + 300 * ((Math.floor(t / .55) % 3) / 3), w: 240, h: 10, rot: -.5, tohum: 1010, kalk: .3 } : (duser({ tur: 'kalem', x: 1330, y: 640, w: 240, h: 10, rot: -.5, tohum: 1010 }, t, to, .5) || { tur: 'kalem', x: 1330, y: 640, w: 240, h: 10, rot: -.5, tohum: 1010 })]; } }; } });
  // H10a · genis · SALON (bugün, v2): figürsüz; sol duvarda büyük Badem Çiçeği (perspektifle, renkli: karenin tek renkli ve en parlak yeri); kamera tabloya döner
  plan({ id: 'H10', at: 'H10', sahne: 'salon', olcek: 'genis', not: 'Bugünkü müze: Badem Çiçeği yan duvarda',
    kamera: kamYol([960, 540, 1.0], [560, 380, 1.55]),
    durum: st => ({ duvar: 'seyrek', bademDuvar: true, expo: .98 }),   // v3: kapı H05'teki gibi temiz (koyulaştırma yırtık kenar bırakıyordu)
    maske: (st, kam) => { const c = M.camK(kam, .72), Q = [SE(-4.46, 4.8, -9.6), SE(-4.46, 4.8, -14.2), SE(-4.46, 1.2, -14.2), SE(-4.46, 1.2, -9.6)], k = MW / 1920;
      mx.save(); mx.fillStyle = '#fff'; mx.filter = 'blur(1.5px)'; mx.beginPath(); Q.forEach(([x, y], i) => { const [X, Y] = ekrana(c, x, y); i ? mx.lineTo(X * k, Y * k) : mx.moveTo(X * k, Y * k); }); mx.closePath(); mx.fill(); mx.restore(); } });
  // H10b · orta · MASA (bugün, soğuk ışık): arşiv çekmecesinde sarı zarflı mektuplar; masada açık sergi kataloğunda Badem Çiçeği: iki motif aynı karede.
  //   "badem"de katalog sayfası ile zarflar birlikte renge açılır; "duruyor"da çekmece yavaşça kapanmaya başlar
  const H10z = yigin(22, { x: 880, y: 860, dx: 480, dy: 180, tohum: 1400 });
  plan({ id: 'H10b', at: 'H10@bugün', sahne: 'masa', olcek: 'orta', not: 'Mektuplar ve badem dalı aynı müzede',
    kamera: kamYol([1100, 560, 1.06], [1000, 600, 1.14], u => u),
    durum: st => ({ isik: 'bugun', katalog: true, nesneler: () => H10z }),
    maske: (st, kam) => { const c = M.camK(kam, 0), tb = cIdx(st, 'H10@badem#1'), a = sm(tb - .2, tb + .8, st.lt); for (const it of H10z) nesneMaske(c, it, .25 + .75 * a); mRect(c, 1470, 150, 310, 245, .3 + .7 * a, 2); } });

  // ================= I: Cevap =================
  // I01 · yakin · MASA (v3, B04 eşlemesi): "her ay bir zarf"ta banknot zarfa girer, zarf kapanır. Sonra sözcüğe bağlı iki kesme: I01b tablolar, I01c gece treni
  const I1y = yigin(8, { x: 560, y: 420, dx: 160, dy: 100, tohum: 1100 });
  plan({ id: 'I01', at: 'I01', sahne: 'masa', olcek: 'yakin', not: 'Önce Theo: her ay bir zarf',
    kamera: kamYol([960, 400, 1.3], [960, 410, 1.38], u => u),
    durum: st => { const tz = cIdx(st, 'I01@her'); return { cekmece: false, isik: 'gece', nesneler: t => {
      const u = io(clamp((t - tz) / 1.0)), kap = io(clamp((t - tz - 1.1) / .5));
      return [...I1y, { tur: 'zarf', renk: 'gri', yuz: kap > .5 ? 'on' : 'arka', x: 1000, y: 430, w: 360, h: 220, rot: -.04, tohum: 1110, golge: true },
        ...(u < 1 ? [{ tur: 'banknot', x: lerp(620, 1000, u), y: lerp(330, 430, u), w: 280 * (1 - .3 * u), h: 140 * (1 - .3 * u), rot: -.3 + .26 * u, tohum: 1115, a: 1 - sm(.85, 1, u), kalk: .3 * (1 - u) }] : [])]; } }; },
    maske: (st, kam) => { const c = M.camK(kam, 0); for (const it of I1y) nesneMaske(c, it); } });
  // I01b · orta · SALON: "sergilere giden tablolar": E04'ün İrisler'i bölme duvarda (renkli)
  plan({ id: 'I01b', at: 'I01@sergilere', sahne: 'salon', olcek: 'orta', not: 'Sergilere giden tablolar: İrisler',
    kamera: kamYol([IR[0] + IR[2] / 2, IR[1] + IR[3] / 2, 1.3], [IR[0] + IR[2] / 2, IR[1] + IR[3] / 2, 1.42], u => u),
    durum: st => ({ duvar: 'seyrek', iris: true }),
    maske: (st, kam) => mRect(M.camK(kam, .72), IR[0] + 6, IR[1] + 6, IR[2] - 12, IR[3] - 12, 1, 2) });
  // I01c · genis · TREN (gece): "nişanlandığı hafta bir gece treni" (D03'ün gidişi)
  plan({ id: 'I01c', at: 'I01@nişanlandığı', sahne: 'tren', olcek: 'genis', not: 'Gece treni',
    kamera: kamYol([960, 560, 1.04], [960, 560, 1.08], u => u),
    durum: st => ({ gun: () => 0, tren: t => [[-300 + 700 * t, 1]] }) });
  // I02 · orta · MASA (v2, gün ışığı; A03'ün karşılığı): Jo'nun gölgesi çekmecenin üstünde; "saklayan"da çekmece açık, sarı zarflar; "taşıyan"da bir zarf kalkar
  //   ve kameraya, bize doğru büyür; "kurye"de kadrajı doldurur (I03'e geçiş)
  const I2y = yigin(30, { tohum: 1700 });
  plan({ id: 'I02', at: 'I02', sahne: 'masa', olcek: 'orta', not: 'Sonra Jo: zarfı bize taşıyan kurye',
    kamera: kamYol([960, 700, 1.05], [960, 720, 1.12], u => u),
    durum: st => { const tt = cIdx(st, 'I02@taşıyan') - .3; return { isik: 'gun', nesneler: t => { const u = clamp((t - tt) / (st.d - tt - .1)), k = io(u);
        return [...I2y, ...(u > 0 ? [{ tur: 'zarf', renk: 'sari', yuz: 'on', x: lerp(1000, 960, k), y: lerp(820, 560, k), w: 240 * (1 + 7 * k * k), h: 146 * (1 + 7 * k * k), rot: .1 * (1 - k), kalk: .8 * k, tohum: 1720 }] : [])]; },
      golge: (t, S) => figurBas(S, FIG.jo_dur, t, [1960, 2900], 3000, { golge: (.3) * .55, adim: 2, temas: false }) }; },   // v3: gölge zarfların üstüne düşmez (sarıda yanık lekesi okunuyordu)
    maske: (st, kam) => { const c = M.camK(kam, 0), tt = cIdx(st, 'I02@taşıyan') - .3, u = clamp((st.lt - tt) / (st.d - tt - .1)), k = io(u);
      for (const it of I2y) nesneMaske(c, it); if (u > 0) nesneMaske(c, { x: lerp(1000, 960, k), y: lerp(820, 560, k), w: 240 * (1 + 7 * k * k), h: 146 * (1 + 7 * k * k), rot: .1 * (1 - k) }); } });
  // I03 · yakin · MASA (bugün): tek sarı zarf izleyiciye dönük açılır; içi boş beyaz kâğıt (≤ 2 sn), sonra kalem kayar
  plan({ id: 'I03', at: 'I03', sahne: 'masa', olcek: 'yakin', not: 'Sen kime inanıyorsun?',
    kamera: kamYol([960, 440, 1.3], [960, 440, 1.36], u => u),
    durum: st => ({ cekmece: false, nesneler: t => { const ac = io(clamp((t - .4) / 1)); return [{ tur: 'zarf', renk: 'sari', yuz: 'arka', x: 960, y: 520, w: 520, h: 320, rot: 0, tohum: 1200, golge: true },
      { tur: 'kagit', x: 960, y: 520 - 260 * ac, w: 460, h: 300, rot: 0, tohum: 1201, satir: 0, golge: true, a: ac }, ...(t > 2 ? [{ tur: 'kalem', x: 960 + 600 * (1 - io(clamp((t - 2) / .8))), y: 300, w: 260, h: 10, rot: -.3, tohum: 1202 }] : [])]; } }),
    maske: (st, kam) => nesneMaske(M.camK(kam, 0), { x: 960, y: 520, w: 520, h: 320, rot: 0 }) });
  // I04 · genis · MASA: bitiş ekranı (son 20 sn): zarf kapanır, kadraj geri çekilir; üst yarıda iki sarı zarf kartı (önerilen video ve abone)
  plan({ id: 'I04', at: 'I04', sahne: 'masa', olcek: 'genis', not: 'BİTİŞ EKRANI: iki sarı zarf kartı üst yarıda',
    kamera: kamYol([960, 480, 1.2], [960, 520, 1.0]),
    durum: st => ({ cekmece: false, nesneler: () => [{ tur: 'zarf', renk: 'sari', yuz: 'on', x: 560, y: 330, w: 560, h: 330, rot: -.02, tohum: 1300, golge: true }, { tur: 'zarf', renk: 'sari', yuz: 'on', x: 1360, y: 330, w: 560, h: 330, rot: .02, tohum: 1301, golge: true }] }),
    maske: (st, kam) => { const c = M.camK(kam, 0); nesneMaske(c, { x: 560, y: 330, w: 560, h: 330, rot: -.02 }); nesneMaske(c, { x: 1360, y: 330, w: 560, h: 330, rot: .02 }); } });
}
