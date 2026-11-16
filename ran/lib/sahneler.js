// sahneler.js (Ran): 63 plan, planlar.md ile aynı numaralar. Her plan ilk saniyeden hareket eder (yavaş yaklaşma + sözcüğe bağlı eylem).
// Kırmızı yalnız ateş, kor, düşen resmin şeridi ve künye kartındaki küçük kare. Figürler yüzsüz (xieyi). Filmden tasarım yok.
'use strict';
window.GORSEL = {
  lear: 'kaynak/gorsel/met707787_garrick_lear_1761.jpg', cordelia: 'kaynak/gorsel/met713083_lear_cordelia_1783.jpg',
  noh: 'kaynak/gorsel/met60220_noh_maskesi.jpg', kuro37: 'kaynak/gorsel/commons_kurosawa_naruse_1937.jpg', mori: 'kaynak/gorsel/commons_mori_motonari.jpg',
};
const { ss, seg, lerp, clamp, vnoise, eio, eo } = LIB;
const TN = INK.TONE;
const H = (() => {
  const cache = {};
  // gece: üstte koyu, aşağı açılan ıslak yıkama
  const gece = (L, k = .66, alt = .38) => INK.mass(L.cw, [[-300, -300], [2300, -300], [2300, 1400], [-300, 1400]], k, 0, 1, [0, 0, 0, 1080, 1, alt]);
  const sis = (L, y, k = .12, sd = 1) => INK.mass(L.cw, [[-300, y - 60], [2300, y - 80], [2300, y + 70], [-300, y + 50]], k, 30, sd, [0, y - 80, 0, y + 70, 0, 1]);
  function dag(L, key, peaks, base, o = {}) {
    if (!cache[key]) cache[key] = INKL.mountainLayer({ W: 2400, H: 1300, ridge: INKL.ridgeFn(peaks, base, o.seed || 4, o.rough || 20), depth: o.depth || 240, tone: o.tone || .35, rim: o.rim ?? .5, mist: o.mist ?? 1.2, seed: o.seed || 4 });
    L.cw.drawImage(cache[key], -240, -110);
  }
  // ekran yazısı: kuru katmana mürekkep; harf harf değil satır satır belirir. y < 880 (altyazı bandı boş)
  function yazi(L, lines, x, y, o = {}) {
    const c = L.cd, a = o.a ?? 1, px = o.px || 54, lh = o.lh || px * 1.25;
    c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.textAlign = o.align || 'center'; c.textBaseline = 'alphabetic';
    lines.forEach((ln, i) => {
      const k = clamp((a * (lines.length + .6) - i)); if (k <= 0) return;
      c.globalAlpha = k * (o.tone ?? .9); c.fillStyle = '#000'; c.font = (o.font || '600 ') + px + 'px "Cormorant Garamond", serif';
      if (o.bebas) c.font = px + 'px "Bebas Neue"';
      if (o.ls) c.letterSpacing = o.ls + 'px';
      c.fillText(ln, x, y + i * lh);
    });
    if (o.kunye) { c.globalAlpha = a * .7; c.font = 'italic 500 ' + Math.round(px * .5) + 'px "Cormorant Garamond", serif'; c.letterSpacing = '1px'; c.fillText(o.kunye, x, y + lines.length * lh + px * .1); }
    c.restore();
    if (o.muhur !== false && o.align === 'left' && a > .2) { const cc = L.cc; cc.save(); cc.setTransform(1, 0, 0, 1, 0, 0); cc.fillStyle = `rgba(176,46,34,${.9 * clamp(a)})`; cc.fillRect(x - 34, y - px * .55, px * .32, px * .32); cc.restore(); }
  }
  const bolum = (L, ad, st) => { const a = Math.min(clamp(st.lt / .6), clamp((3.6 - st.lt) / .8)); if (a > 0) yazi(L, [ad], 120, 130, { px: 40, align: 'left', a, ls: 6, font: '600 ' }); };
  // gerçek görsel: kâğıt paspartu + künye kartı; yavaş yaklaşma; kâğıt tonunda masa
  function arsiv(L, im, kart, st, o = {}) {
    const z = 1 + (o.z ?? .06) * eio(st.p), fx = o.fx ?? 960, fy = o.fy ?? 520, ain = o.ain ? clamp(st.lt / o.ain) : 1;
    INK.mass(L.cw, [[-80, -80], [2000, -80], [2000, 1160], [-80, 1160]], .26 * ain, 0, 1, [0, 0, 1920, 1080, 1, .55]);
    if (!im) return;
    const hgt = o.h || 720, w = hgt * im.width / im.height, x = (o.x ?? (960 - (w + 420) / 2)), y = o.y ?? (470 - hgt / 2);
    const c = L.cc; c.save(); c.setTransform(z, 0, 0, z, fx * (1 - z), fy * (1 - z));
    c.globalAlpha = ain; c.shadowColor = 'rgba(0,0,0,.35)'; c.shadowBlur = 30; c.shadowOffsetY = 12; c.fillStyle = '#efe6d2'; c.fillRect(x - 26, y - 26, w + 52, hgt + 52); c.shadowColor = 'transparent';
    c.drawImage(im, x, y, w, hgt);
    if (kart) {
      const kx = x + w + 60, ky = Math.min(y + hgt - 220, 640), ka = clamp((st.lt - .5) / .6);
      c.globalAlpha = ka; c.fillStyle = '#f4eddc'; c.fillRect(kx, ky, 380, 220);
      c.fillStyle = 'rgb(176,46,34)'; c.fillRect(kx + 24, ky + 28, 14, 14);
      c.fillStyle = '#1b1a18'; c.font = '600 29px "Cormorant Garamond", serif'; c.fillText(kart[0], kx + 50, ky + 43);
      c.font = '500 25px "Cormorant Garamond", serif'; (kart[1] || []).forEach((s, i) => c.fillText(s, kx + 24, ky + 92 + i * 36));
      c.fillStyle = '#5a554d'; c.font = 'italic 500 21px "Cormorant Garamond", serif'; c.fillText(kart[2] || '', kx + 24, ky + 192);
    }
    c.restore();
  }
  function oklar(L, x, y, s, o = {}) {   // üç ok demeti; o.kir: kırılma 0..1, o.tek: yalnız biri
    const n = o.tek ? 1 : 3, bend = o.bend || 0, kir = o.kir || 0;
    for (let i = 0; i < n; i++) {
      const dx = (i - (n - 1) / 2) * 18 * s, len = 520 * s;
      const mid = [x + dx + bend * 60 * s, y - len * .5], top = [x + dx, y - len];
      if (kir > 0) {   // kırık: iki parça, ortadan açılır
        const a = kir * .5;
        RC.S(L, [[x + dx, y], [mid[0] - Math.sin(a) * 40 * s, mid[1] + 10 * s]], { w: 9 * s, tone: TN.nong, dry: .3, seed: 300 + i, prof: 'even' });
        RC.S(L, [[mid[0] + Math.sin(a) * 40 * s, mid[1] - 10 * s], [top[0] + Math.sin(a) * 160 * s, top[1] + kir * 60 * s]], { w: 9 * s, tone: TN.nong, dry: .3, seed: 310 + i, prof: 'even' });
      } else RC.S(L, [[x + dx, y], mid, top], { w: 11 * s, tone: TN.nong, dry: .3, seed: 300 + i, prof: 'even' });
      const t0 = kir > 0 ? [top[0] + Math.sin(kir * .5) * 160 * s, top[1] + kir * 60 * s] : top;
      INK.mass(L.cw, [[t0[0] - 13 * s, t0[1] + 30 * s], [t0[0], t0[1] - 16 * s], [t0[0] + 13 * s, t0[1] + 30 * s]], .9, 1, 320 + i);   // uç: üçgen demir
      for (const d of [-1, 1]) RC.S(L, [[x + dx, y - 20 * s], [x + dx + d * 22 * s, y + 4 * s]], { w: 9 * s, tone: TN.nong, dry: .45, seed: 330 + i + d, prof: 'fan' });   // tüyler
      for (const d of [-1, 1]) RC.S(L, [[x + dx, y - 60 * s], [x + dx + d * 22 * s, y - 36 * s]], { w: 9 * s, tone: TN.nong, dry: .45, seed: 340 + i + d, prof: 'fan' });
    }
  }
  function sancak(L, x, y, h, t, sd) {   // nobori: direk + dikey bayrak (renksiz, desensiz)
    RC.S(L, [[x, y], [x, y - h]], { w: 4, tone: TN.nong, dry: .4, seed: sd, prof: 'even' });
    const wv = k => Math.sin(t * 2.2 + sd + k * 2) * 8;
    INK.mass(L.cw, [[x, y - h], [x + 46 + wv(0), y - h + 4], [x + 48 + wv(1), y - h * .45], [x, y - h * .45]], .4, 2, sd);
  }
  function yagmur(L, t, k = 1) { const tq = Math.floor(t * 12) / 12; for (let i = 0; i < 70; i++) { const x = ((i * 137.5 + tq * 900) % 2200) - 140, y = ((i * 71.3 + tq * 1700) % 1300) - 140; RC.S(L, [[x, y], [x - 30, y + 110]], { w: 1.6, tone: .4 * k, dry: .8, seed: 900 + i, prof: 'tip' }); } }
  function agac(L, x, y, s, sd = 5, rz = 0) {
    RC.S(L, [[x, y], [x + 10 * s, y - 160 * s], [x - 20 * s + rz * 20, y - 330 * s]], { w: 30 * s, tone: TN.nong, dry: .45, seed: sd, prof: 'robe' });
    for (let k = 0; k < 5; k++) { const yy = y - (160 + k * 35) * s, d = k % 2 ? 1 : -1; RC.S(L, [[x, yy], [x + d * (90 + k * 10) * s + rz * 30, yy - 60 * s], [x + d * (150 + k * 12) * s + rz * 50, yy - 50 * s]], { w: 8 * s, tone: TN.zhong, dry: .55, seed: sd + k * 7, prof: 'tip' }); }
  }
  function tomar(L, x, y, s, rot, am = 1) {   // sarılı resim: kumaş tomar + kırmızı şerit (figür yok)
    const ca = Math.cos(rot), sa = Math.sin(rot), P = (u, v) => [x + (u * ca - v * sa) * s, y + (u * sa + v * ca) * s];
    INK.mass(L.cw, [P(-120, -22), P(120, -22), P(120, 22), P(-120, 22)], .35 * am, 1, 77);
    RC.S(L, [P(-130, 0), P(130, 0)], { w: 10 * s, tone: TN.nong, dry: .3, seed: 78, prof: 'even', am });
    const c = L.cc; c.save(); c.fillStyle = `rgba(176,46,34,${.9 * am})`; c.beginPath(); const a = P(20, -26), b = P(34, -26), d = P(40, 70), e = P(26, 76); c.moveTo(...a); c.lineTo(...b); c.lineTo(...d); c.lineTo(...e); c.fill(); c.restore();
  }
  function kulube(L) {   // kulübe içi (üslup orta planı)
    RC.S(L, [[230, 40], [220, 1010]], { w: 26, tone: .6, dry: .5, seed: 3, prof: 'robe' });
    RC.S(L, [[1700, 80], [1710, 1010]], { w: 22, tone: .5, dry: .6, seed: 4, prof: 'robe' });
    RC.S(L, [[60, 170], [960, 40], [1860, 190]], { w: 30, tone: .7, dry: .4, seed: 5, prof: 'tip' });
    for (let k = 0; k < 14; k++) RC.S(L, [[300 + k * 95, 260 + (k % 3) * 20], [310 + k * 95, 760]], { w: 5, tone: .22, dry: .9, seed: 200 + k, prof: 'tip' });
    RC.ground(L, 1010, 0, 1920, 1, 9);
  }
  function kale(L, X, t, yangin = 0) {
    const K = RC.castle(L, X);
    if (yangin > 0) {
      RC.smoke(L, X.x, K.top - 20, 360 * X.s, 520 * X.s, t, yangin, 3);
      RC.fire(L, [[X.x, K.top + 40 * X.s, 42 * X.s], [K.win[1][0], K.win[1][1] + 14 * X.s, 14 * X.s], [K.win[5][0], K.win[5][1] + 12 * X.s, 16 * X.s], [X.x + 120 * X.s, K.top + 120 * X.s, 22 * X.s]], .95 * yangin, t);
    }
    return K;
  }
  const lekeler = (L, n, x, y, gap, koyu = -1, k = 0) => { for (let i = 0; i < n; i++) INK.blot(L.cw, x + (i - (n - 1) / 2) * gap, y, 60 + (i === koyu ? 40 * k : 0), (i === koyu ? .3 + .5 * k : .3), 0, 1, 40 + i); };
  return { gece, sis, dag, yazi, bolum, arsiv, oklar, sancak, yagmur, agac, tomar, kulube, kale, lekeler };
})();
const NIGHT = { bleed: 7, vig: .35, warm: .55 }, DAY = { bleed: 6, vig: .22, warm: .5 };
const push = (L, st, cx = 960, cy = 540, z0 = 1, z1 = 1.06) => cam(L, cx, cy, lerp(z0, z1, eio(st.p)));

// ================= A: Yanan kale =================
function kancaKaresi(L, st, o = {}) {   // açılış = kapak A; E04'te yakın sürümüyle döner
  const u = o.u ?? clamp(st.lt / 15), t = st.t;
  H.gece(L); H.dag(L, 'gece', [[300, 120, 260], [820, 90, 300], [1500, 140, 280]], 700, { tone: .35, mist: 1.2, seed: 4 });
  H.kale(L, { x: 1180, y: 700, s: 1.15, seed: 11 }, t, 1);
  for (let k = 0; k < 3; k++) RC.S(L, [[560 + k * 40, 1090], [820 + k * 20, 900], [1040 + k * 10, 760], [1150, 706]], { w: 10, tone: .7, dry: .75, seed: 77 + k, prof: 'robe' });
  RC.ground(L, 706, 600, 1760, 1, 8);
  RC.figure(L, { x: lerp(1020, 760, u), y: lerp(790, 980, u), s: 1.5 + u * .7, dir: -1, pose: 'walk', t, hair: 'old', bowed: .3, seed: 5, headTone: .55 });
}
plan('P01', 'A01', (L, st) => { push(L, st, 960, 620, 1, 1.05); kancaKaresi(L, st, { u: clamp(st.t / 30) }); return NIGHT; });
plan('P02', 'A02', (L, st) => {   // "oğullarına vermişti": yerde üç ok, biri kırık; ateş ışığı (kapak B'nin vaadi ilk saniyelerde)
  push(L, st, 960, 600, 1.02, 1.1); H.gece(L, .55, .5);
  kapakOklar(L, st.t, clamp((st.t - AT('A02@oğullarına')) / .4));
  RC.ground(L, 900, -200, 2200, 1, 12);
  return NIGHT;
});
function rot(L, cx, cy, a, fn) { const cs = [L.cw, L.cd, L.cc]; cs.forEach(c => { c.save(); c.translate(cx, cy); c.rotate(a); c.translate(-cx, -cy); }); fn(); cs.forEach(c => c.restore()); }
function kapakOklar(L, t, kir = 1) {
  rot(L, 900, 760, -1.25, () => H.oklar(L, 900, 1000, 1.2, {}));
  rot(L, 1150, 780, 1.1, () => H.oklar(L, 1150, 1020, 1.1, { tek: true, kir: .9 * kir + .1 }));
  RC.fire(L, [[1650, 900, 34], [260, 930, 22]], .7, t);
}
plan('P03', 'A03', (L, st) => {   // yerde kırık kılıç; alev yansısı
  push(L, st, 960, 600, 1.05, 1.15); H.gece(L, .5, .5);
  RC.S(L, [[420, 760], [900, 700]], { w: 22, tone: TN.nong, dry: .3, seed: 51, prof: 'even' });            // kın
  RC.S(L, [[940, 690], [1260, 655], [1330, 650]], { w: 14, tone: .7, dry: .4, seed: 52, prof: 'tip' });       // kırık namlu
  RC.S(L, [[900, 660], [905, 740]], { w: 18, tone: TN.jiao, dry: .2, seed: 53, prof: 'even' });               // tsuba
  RC.fire(L, [[1500, 880, 30]], .7, st.t); RC.fire(L, [[300, 900, 20]], .5, st.t + 3);
  RC.ground(L, 800, 0, 1920, 1, 12);
  return NIGHT;
});
plan('P04', 'A04', (L, st) => {   // künye: kâğıt boşluğu
  cam(L, 960 + 40 * st.p, 540, 1 + .08 * eio(st.p)); H.sis(L, 620 - 60 * st.p, .14, 2); H.sis(L, 380 + 50 * st.p, .08, 5);
  H.yazi(L, ['AKIRA KUROSAWA'], 960, 430, { px: 46, ls: 14, a: clamp(st.lt / .8) });
  H.yazi(L, ['RAN'], 960, 580, { px: 150, ls: 40, a: clamp((st.lt - .5) / .8), bebas: true });
  H.yazi(L, ['1985 · “kargaşa”'], 960, 660, { px: 34, ls: 4, a: clamp((st.lt - 1.4) / .8), font: 'italic 500 ' });
  return DAY;
});
plan('P05', 'A05', (L, st) => {   // fırça kâğıda kale çizer (yeni sırada E06'nın ardından: yanan kaleden resme)
  push(L, st, 960, 540, 1, 1.04); H.bolum(L, 'RESİMLERLE ÇEKİLEN FİLM', st);
  const p = clamp(st.lt / Math.max(1, st.d - .3));
  L.cw.save(); L.cw.globalAlpha = 1; RC.castle(L, { x: 960, y: 760, s: 1.1, seed: 11, am: Math.min(1, p * 1.6) }); L.cw.restore();
  RC.S(L, [[1400, 300 + 400 * p], [1470, 250 + 400 * p]], { w: 18, tone: TN.jiao, dry: .2, seed: 61, prof: 'cone' });   // fırça ucu
  return DAY;
});

// ================= B: Resimlerle çekilen film =================
plan('P06', 'B01', (L, st) => { H.arsiv(L, IMG.kuro37, ['Akira Kurosawa (solda), 1937', ['Mikio Naruse ile, Nadare çekimi', 'arkada Nagoya Kalesi'], 'Wikimedia Commons · kamu malı'], st, { h: 760 }); return DAY; });
plan('P07', 'B02', (L, st) => {   // üst üste kâğıtlar, her birinde bizim taslağımız
  push(L, st, 960, 540, 1, 1.05);
  for (let k = 0; k < 5; k++) {
    const x = 380 + k * 260 + Math.sin(st.t * .4 + k) * 8, y = 300 + (k % 2) * 90, sl = clamp((st.lt - k * .5) / .6);
    if (sl <= 0) continue;
    INK.mass(L.cw, [[x - 160, y - 110], [x + 160, y - 105], [x + 158, y + 120], [x - 162, y + 116]], .08 * sl, 1, 70 + k);
    RC.S(L, [[x - 160, y - 110], [x + 160, y - 105], [x + 158, y + 120], [x - 162, y + 116], [x - 160, y - 110]], { w: 3, tone: .5, dry: .6, seed: 80 + k, prof: 'even', am: sl });
    if (k % 2 === 0) RC.castle(L, { x, y: y + 80, s: .32, seed: 11 + k, am: sl }); else { RC.figure(L, { x: x - 40, y: y + 90, s: 1.2, pose: 'walk', t: 0, hair: 'old', seed: k, am: sl }); RC.S(L, [[x - 150, y + 92], [x + 150, y + 92]], { w: 3, tone: .6, dry: .7, seed: 90 + k, prof: 'even', am: sl }); }
  }
  return DAY;
});
plan('P08', 'B03', (L, st) => {   // gözleri zayıflamıştı: aynı fotoğraf, kenarlar bulanır (sis)
  H.arsiv(L, IMG.kuro37, null, st, { h: 860, x: 960 - 860 * 500 / 700 / 2, z: .12, fy: 300 });
  const b = clamp((st.t - AT('B03@gözleri')) / 1.2);
  if (b > 0) { INK.mass(L.cw, [[-200, -200], [2120, -200], [2120, 1280], [-200, 1280]], .35 * b, 0, 1, [0, 0, 0, 1080, .9, .9]); H.sis(L, 300, .25 * b, 3); H.sis(L, 800, .25 * b, 4); }
  return { ...DAY, bleed: 6 + 10 * b };
});
plan('P09', 'B04', (L, st) => {   // taslak → sahne: tepe, sancak sırası (renksiz)
  push(L, st, 960, 560, 1, 1.05);
  H.dag(L, 'gun1', [[400, 160, 300], [1100, 200, 340], [1700, 140, 260]], 640, { tone: .3, seed: 6 });
  for (let k = 0; k < 14; k++) H.sancak(L, 300 + k * 100, 820 + (k % 2) * 20, 260, st.t, 400 + k);
  RC.ground(L, 840, 0, 1920, 1, 14);
  return DAY;
});
plan('P10', 'B05', (L, st) => {   // fırça kalkar; "Onları kendi fırçamızla…"da fırça yanan kaleyi ve inen yaşlı adamı yeniden boyar (E07'ye köprü)
  push(L, st, 960, 600, 1.04, 1);
  const up = clamp(st.lt / 2), t0 = AT('B05@onları'), p = clamp((st.t - t0) / Math.max(1.5, st.end - t0 - .3));
  if (p <= 0) RC.S(L, [[700, 620], [1100, 600]], { w: 26, tone: TN.nong, dry: .6, seed: 101, prof: 'brush', p: .6 });
  if (p > 0) {
    H.gece(L, .66 * p, .38 * p); RC.castle(L, { x: 1180, y: 700, s: 1.15, seed: 11, am: Math.min(1, p * 1.4) });
    RC.fire(L, [[1180, 330, 40]], p, st.t); RC.ground(L, 706, 600, 1760, p, 8);
    RC.figure(L, { x: 900, y: 880, s: 1.9, dir: -1, pose: 'walk', t: st.t, hair: 'old', bowed: .3, seed: 5, headTone: .55, am: clamp(p * 2 - 1) });
  }
  const bx = p > 0 ? lerp(1300, 820, p) : 1150 + up * 80, by = p > 0 ? 300 + 520 * p : 560 - up * 300;
  RC.S(L, [[bx, by], [bx + 70, by - 60]], { w: 22, tone: TN.jiao, dry: .2, seed: 61, prof: 'cone' });
  return p > .3 ? NIGHT : DAY;
});
plan('P11', 'B06', (L, st) => { H.arsiv(L, IMG.lear, ['Kral Lear rolünde David Garrick', ['James McArdell, 1761', 'Shakespeare, III. perde'], 'The Met · kamu malı (CC0)'], st, { h: 640, ain: .6 }); return DAY; });
plan('P12', 'B07', (L, st) => {   // boş sayfaya tek damla
  push(L, st, 960, 540, 1, 1.08);
  const d = clamp((st.lt - .4) / .5), sp = clamp((st.lt - .9) / 2.5);
  if (d < 1) INK.blot(L.cw, 960, lerp(-40, 540, eo(d)), 10, .9, 0, 1.6, 3);
  else { INK.blot(L.cw, 960, 540, 18 + 120 * eo(sp), .7, 0, 1, 4); INK.blot(L.dry ? L.cd : L.cw, 960, 540, 14 + 40 * eo(sp), .5, 0, 1, 5); }
  return { ...DAY, bleed: 6 + 8 * sp };
});

// ================= C: Üç ok =================
plan('P13', 'C01', (L, st) => {   // gündüz: sıradağlar, tepede kale; el tomarı gibi kayma
  cam(L, lerp(900, 1060, eio(st.p)), 540, 1);
  const gi = ss(clamp(st.lt / 1.2));   // B07'nin damlasından sonra dağlar boyanarak belirir (yumuşak giriş)
  L.cw.globalAlpha = gi; H.dag(L, 'gun2', [[200, 260, 300], [800, 330, 380], [1500, 280, 340], [2100, 240, 300]], 720, { tone: .38, seed: 8, mist: 1.4 }); L.cw.globalAlpha = 1;
  RC.castle(L, { x: 1250, y: 470, s: .42, seed: 12 });
  for (let k = 0; k < 9; k++) RC.figure(L, { x: 300 + k * 60 + st.t * 6, y: 900, s: .7, pose: 'walk', t: st.t + k * .3, hair: 'young', seed: 20 + k });
  RC.ground(L, 905, -200, 2200, 1, 15); H.bolum(L, 'ÜÇ OK', st);
  return DAY;
});
plan('P14', 'C02', (L, st) => {   // Hidetora oturur, üç oğul (sırtlar)
  push(L, st, 960, 600, 1, 1.05);
  RC.figure(L, { x: 960, y: 640, s: 3.2, dir: 1, pose: 'sit', t: st.t, hair: 'old', bowed: -.1 + .1 * Math.sin(st.t * .5), seed: 5, headTone: .3 });
  for (let k = 0; k < 3; k++) RC.figure(L, { x: 560 + k * 400, y: 1100, s: 3.8, dir: k === 2 ? -1 : 1, pose: 'kneel', t: st.t, hair: 'young', seed: 31 + k, headTone: .4 });
  RC.ground(L, 650, 300, 1620, 1, 16);
  return DAY;
});
plan('P15', 'C03', (L, st) => {   // tek ok kırılır, üçü kırılmaz
  push(L, st, 960, 540, 1.02, 1.08);
  const tk = clamp((st.t - AT('C03@kırılır')) / .25), uc = clamp((st.t - AT('C03@üç')) / .4);
  if (uc <= 0) H.oklar(L, 960, 900, 1.4, { tek: true, kir: tk });
  else { H.oklar(L, 600, 900, 1.1, { tek: true, kir: 1 }); H.oklar(L, 1240, 900, 1.4, { bend: .3 * Math.sin(Math.min(1, uc) * Math.PI) }); }
  return DAY;
});
plan('P16', 'C04', (L, st) => { H.arsiv(L, IMG.mori, ['Mōri Motonari (1497–1571)', ['Momoyama/Edo dönemi portresi', '“üç ok” efsanesinin beyi'], 'Wikimedia Commons · kamu malı'], st, { h: 820, y: 40 }); return DAY; });
plan('P17', 'C05', (L, st) => {   // demetteki bir ok gölgede kalır
  push(L, st, 960, 540, 1, 1.06); H.oklar(L, 960, 820, 1);
  const g = clamp(st.lt / 2);
  INK.mass(L.cw, [[960 - 90, 200], [960 + 30, 200], [960 + 20, 840], [960 - 100, 840]], .35 * g, 8, 9);
  return { ...DAY, bleed: 6 + 6 * g };
});
plan('P18', 'C06', (L, st) => {   // Saburo okları dizinde kırar
  push(L, st, 960, 600, 1, 1.05);
  const k = clamp((st.t - AT('C06@dizinde')) / .3);
  RC.figure(L, { x: 820, y: 1120, s: 6, dir: 1, pose: 'kneel', t: st.t, hair: 'young', seed: 33, headTone: .45, bowed: .2 });
  H.oklar(L, 1180, 900, .9, { kir: k });
  return { ...DAY, flash: .25 * Math.max(0, 1 - Math.abs(st.t - AT('C06@dizinde') - .3) * 6) };
});
plan('P19', 'C07', (L, st) => {   // Saburo boş ovada uzaklaşır
  cam(L, 960, 540, 1 + .03 * st.p); H.sis(L, 600, .1, 5);
  RC.ground(L, 760, -200, 2200, 1, 17);
  RC.figure(L, { x: lerp(980, 1500, st.p), y: lerp(900, 770, st.p), s: lerp(1.6, .7, st.p), dir: 1, pose: 'walk', t: st.t, hair: 'young', seed: 33 });
  return DAY;
});
plan('P20', 'C08', (L, st) => {   // Lear ve Cordelia (mürekkep), alıntı
  push(L, st, 960, 560, 1, 1.04);
  RC.figure(L, { x: 640, y: 860, s: 4, dir: 1, pose: 'stand', t: st.t, hair: 'old', seed: 41, headTone: .3, bowed: -.1 });
  RC.figure(L, { x: 1120, y: 860, s: 3.6, dir: -1, pose: 'stand', t: st.t, hair: 'woman', seed: 42, headTone: .25, bowed: .3 });
  RC.ground(L, 870, 300, 1500, 1, 18);
  H.yazi(L, ['“Hiçten hiç çıkar.”'], 1540, 360, { px: 56, align: 'left', a: clamp((st.t - AT('C08@hiçten')) / .6), kunye: 'Kral Lear, I. perde' });
  return DAY;
});
plan('P21', 'C09', (L, st) => {   // üç kız → üç oğul
  push(L, st, 960, 600, 1, 1.04);
  const m = clamp((st.t - AT('C09@kurosawa')) / 1.2);
  for (let k = 0; k < 3; k++) {
    RC.figure(L, { x: 600 + k * 360, y: 840, s: 3, dir: 1, pose: 'stand', t: st.t, hair: 'woman', seed: 50 + k, am: 1 - m });
    RC.figure(L, { x: 600 + k * 360, y: 840, s: 3, dir: 1, pose: 'stand', t: st.t, hair: 'young', seed: 60 + k, am: m });
  }
  RC.ground(L, 850, 300, 1620, 1, 19);
  return DAY;
});

// ================= D: Kapılar =================
function kapi(L, x, y, w, h, ac, sd = 1) {   // iki kanatlı ahşap kale kapısı; ac 0 kapalı .. 1 açık (kanatlar menteşede daralır)
  INK.mass(L.cw, [[x - w / 2, y], [x + w / 2, y], [x + w / 2, y - h], [x - w / 2, y - h]], .62, 2, sd + 3);   // içerisi karanlık
  RC.S(L, [[x - w * .62, y], [x - w * .62, y - h], [x + w * .62, y - h], [x + w * .62, y]], { w: 26, tone: TN.nong, dry: .35, seed: sd, prof: 'robe' });
  RC.S(L, [[x - w * .75, y - h - 30], [x, y - h - 70], [x + w * .75, y - h - 30]], { w: 22, tone: TN.jiao, dry: .3, seed: sd + 1, prof: 'tip' });
  for (const d of [-1, 1]) {
    const ww = w / 2 * (1 - ac * .8), x0 = x + d * w / 2, x1 = x + d * (w / 2 - ww);
    L.cw.save(); L.cw.globalCompositeOperation = 'destination-out'; INK.mass(L.cw, [[x0, y], [x1, y], [x1, y - h], [x0, y - h]], 1, 0, 1); L.cw.restore();
    INK.mass(L.cw, [[x0, y], [x1, y], [x1, y - h], [x0, y - h]], .32, 2, sd + 5 + d);
    for (let k = 1; k < 4; k++) RC.S(L, [[x0, y - h * k / 4], [x1, y - h * k / 4]], { w: 4, tone: .6, dry: .6, seed: sd + 10 + k + d * 5, prof: 'even' });
    RC.S(L, [[x1, y], [x1, y - h]], { w: 6, tone: TN.nong, dry: .4, seed: sd + 20 + d, prof: 'even' });
  }
}
plan('P22', 'D01', (L, st) => {   // birinci kale kapısı; Hidetora ve maiyeti yürür
  push(L, st, 960, 560, 1, 1.05);
  kapi(L, 1300, 860, 380, 420, .6, 10); RC.ground(L, 860, 0, 1920, 1, 20);
  for (let k = 0; k < 5; k++) RC.figure(L, { x: 300 + k * 110 + st.t * 10, y: 880 + (k % 2) * 10, s: k ? 1.6 : 1.9, dir: 1, pose: 'walk', t: st.t + k * .4, hair: k ? 'young' : 'old', seed: 70 + k });
  H.bolum(L, 'KAPILAR', st);
  return DAY;
});
plan('P23', 'D02', (L, st) => {   // Kaede dimdik; Taro başını eğer
  push(L, st, 960, 600, 1, 1.05);
  RC.figure(L, { x: 760, y: 1000, s: 5, dir: 1, pose: 'sit', t: st.t, hair: 'woman', seed: 81, headTone: .3, bowed: -.15 });
  RC.figure(L, { x: 1250, y: 1000, s: 5.2, dir: -1, pose: 'sit', t: st.t, hair: 'young', seed: 82, headTone: .35, bowed: .1 + .35 * ss(clamp(st.lt / 3)) });
  RC.ground(L, 1005, 0, 1920, 1, 21);
  return DAY;
});
plan('P24', 'D03', (L, st) => {   // Kaede yakından: sırtı ve uzun saçı; önünde soluk eski kale (geçmişe bakış)
  push(L, st, 960, 560, 1.02, 1.1);
  RC.castle(L, { x: 1300, y: 640, s: .55, seed: 19, am: .35 }); H.sis(L, 620, .1, 7);
  RC.figure(L, { x: 640, y: 1560, s: 10, dir: 1, pose: 'sit', t: st.t, hair: 'woman', seed: 81, headTone: .3, bowed: -.05 + .05 * Math.sin(st.t * .6) });
  return DAY;
});
plan('P25', 'D04', (L, st) => {   // geri dönüş: yıllar önce yanan başka kale (soluk)
  push(L, st, 960, 540, 1, 1.05);
  H.sis(L, 700, .15, 9); H.kale(L, { x: 960, y: 760, s: .9, seed: 19, am: .45 }, st.t, .6);
  INK.mass(L.cw, [[-200, -200], [2120, -200], [2120, 1280], [-200, 1280]], .15, 0, 1);
  return { ...DAY, warm: .7, bleed: 9 };
});
plan('P26', 'D05', (L, st) => { push(L, st, 960, 540, 1, 1.14); const g = clamp(st.lt / 2.5); H.lekeler(L, 3, 960 + 30 * Math.sin(st.t * .5), 520, 320 * (.7 + .3 * g), 0, clamp((st.t - AT('D05@canavara')) / 1)); return { ...DAY, bleed: 6 + 6 * g }; });
plan('P27', 'D06', (L, st) => { H.arsiv(L, IMG.lear, null, st, { h: 640, x: 340 }); H.yazi(L, ['GEÇMİŞ'], 1500, 520, { px: 120, bebas: true, ls: 10, a: clamp((st.t - AT('D06@geçmiş')) / .5) }); return DAY; });
plan('P28', 'D08', (L, st) => {   // kapı kapanır; Hidetora dışarıda (D07 = P27'nin devamı ses olarak)
  push(L, st, 960, 600, 1, 1.04);
  const ac = 1 - ss(clamp(st.lt / 2.5));
  kapi(L, 960, 860, 520, 520, ac, 30); RC.ground(L, 860, 0, 1920, 1, 22);
  RC.figure(L, { x: 960, y: 1060, s: 3.4, dir: 1, pose: 'stand', t: st.t, hair: 'old', seed: 5, headTone: .45, bowed: .2 });
  return DAY;
});
plan('P29', 'D09', (L, st) => {   // Lear'ın yılan dişi: kıvrılan çizgi + alıntı
  cam(L, 900 + 120 * eio(st.p), 560, 1 + .1 * eio(st.p));
  const p = clamp(st.lt / Math.max(2.5, st.d * .8));
  RC.S(L, [[220, 700], [420, 560], [620, 760], [820, 560], [1000, 720]], { w: 22, tone: TN.nong, dry: .45, seed: 111, prof: 'cone', p });
  H.yazi(L, ['“Nankör bir evladın acısı', 'yılan dişinden keskindir.”'], 1130, 470, { px: 52, align: 'left', a: clamp((st.t - AT('D09@nankör')) / .8), kunye: 'Kral Lear, I. perde' });
  return DAY;
});

// ================= E: Üçüncü kale =================
plan('P30', 'E01', (L, st) => {   // boş kale; Hidetora girer
  push(L, st, 960, 560, 1, 1.06); H.sis(L, 760, .12, 11);
  RC.castle(L, { x: 960, y: 700, s: 1, seed: 13 }); RC.ground(L, 706, 300, 1620, 1, 23);
  RC.figure(L, { x: lerp(700, 900, st.p), y: lerp(980, 760, st.p), s: lerp(1.8, 1, st.p), dir: 1, pose: 'walk', t: st.t, hair: 'old', seed: 5 });
  H.bolum(L, 'ÜÇÜNCÜ KALE', st);
  return DAY;
});
plan('P31', 'E02', (L, st) => {   // sancak ormanı: iki sıra, arkada soluk duvar ve sis (renksiz, desensiz)
  cam(L, lerp(880, 1040, st.p), 560, 1.05);
  INK.mass(L.cw, [[-200, 360], [2200, 340], [2200, 620], [-200, 640]], .2, 6, 31); H.sis(L, 640, .14, 21);
  for (let k = 0; k < 18; k++) H.sancak(L, -60 + k * 125 + (k % 3) * 20, 760, 240 + (k % 4) * 25, st.t, 700 + k);
  for (let k = 0; k < 11; k++) H.sancak(L, -100 + k * 220 + (k % 2) * 60, 1080, 520 + (k % 3) * 60, st.t + 1, 500 + k);
  return DAY;
});
plan('P32', 'E03', (L, st) => {   // oklar yağar, pencerede ateş başlar
  push(L, st, 960, 520, 1, 1.06); H.gece(L, .45, .3);
  const K = RC.castle(L, { x: 960, y: 900, s: 1.4, seed: 13 });
  const f = clamp((st.t - AT('E03@yanar')) / 1);
  if (f > 0) { RC.smoke(L, 960, K.top, 400, 500, st.t, f, 4); RC.fire(L, [[K.win[0][0], K.win[0][1] + 10, 18], [K.win[2][0], K.win[2][1] + 10, 18], [960, K.top + 60, 40 * f]], f, st.t); }
  const tq = Math.floor(st.t * 12) / 12;
  for (let i = 0; i < 16; i++) { const u = (i * .137 + tq * .7) % 1, x = 100 + i * 120 + u * 300, y = -100 + u * 900; RC.S(L, [[x, y], [x + 60, y + 90]], { w: 3, tone: .8, dry: .5, seed: 600 + i, prof: 'nail' }); }
  return NIGHT;
});
plan('P33', 'E04', (L, st) => { push(L, st, 900, 700, 1.25, 1.35); kancaKaresi(L, st, { u: clamp(st.lt / Math.max(4, st.d)) }); return NIGHT; });
plan('P34', 'E05', (L, st) => {   // yüzsüz baş; duman geçer
  cam(L, 960, 540, 1 + .03 * st.p); H.gece(L, .55, .45);
  RC.figure(L, { x: 900, y: 2300, s: 18, dir: -1, pose: 'stand', t: st.t, hair: 'old', bowed: .2, seed: 5, headTone: .5 });
  RC.smoke(L, 1300, 1100, 900, 1400, st.t * 3, .8, 6); RC.fire(L, [[1700, 1080, 40]], .5, st.t);
  return NIGHT;
});
plan('P35', 'E06', (L, st) => {   // Fuji eteğinde gerçek yangın
  push(L, st, 960, 560, 1, 1.05); H.gece(L, .45, .35);
  H.dag(L, 'fuji', [[960, 520, 520]], 760, { tone: .4, rough: 8, seed: 10, mist: .8 });
  H.kale(L, { x: 960, y: 880, s: .6, seed: 14 }, st.t, 1);
  RC.ground(L, 885, -200, 2200, 1, 24);
  return NIGHT;
});
plan('P36', 'E07', (L, st) => {   // Lear fırtınada (yeni bölüm: Lear'ın fırtınası)
  push(L, st, 960, 560, 1, 1.05); H.gece(L, .4, .5); H.yagmur(L, st.t); H.bolum(L, 'LEAR’IN FIRTINASI', st);
  H.agac(L, 1450, 900, 1.6, 7, Math.sin(st.t * 2) * .4);
  RC.figure(L, { x: 800, y: 900, s: 3.4, dir: 1, pose: 'stand', t: st.t, hair: 'old', bowed: -.2, seed: 41, headTone: .45 });
  RC.ground(L, 905, -200, 2200, 1, 25);
  H.yazi(L, ['“Esin rüzgârlar,', 'patlatın yanaklarınızı!”'], 220, 250, { px: 52, align: 'left', a: clamp((st.t - AT('E07@esin')) / .6), kunye: 'Kral Lear, III. perde' });
  return { ...NIGHT, shake: [Math.sin(st.t * 40) * .6, 0] };
});
plan('P37', 'E08', (L, st) => {   // Lear'ın açılmış kolları + alıntı
  push(L, st, 1000, 540, 1.02, 1.08); H.gece(L, .3, .5); H.yagmur(L, st.t, .6);
  const x = 600, y = 1100, s = 7;
  RC.figure(L, { x, y, s, dir: 1, pose: 'stand', t: st.t, hair: 'old', bowed: -.25, seed: 41, headTone: .45 });
  RC.S(L, [[x + 8 * s, y - 80 * s], [x + 30 * s, y - 104 * s], [x + 46 * s, y - 126 * s]], { w: 5 * s, tone: TN.zhong, dry: .45, seed: 140, prof: 'lens' }); RC.S(L, [[x - 2 * s, y - 80 * s], [x - 22 * s, y - 106 * s], [x - 30 * s, y - 128 * s]], { w: 5 * s, tone: TN.zhong, dry: .5, seed: 141, prof: 'lens' });
  H.yazi(L, ['“Günah işlediğinden çok', 'kendisine günah işlenmiş', 'bir adamım.”'], 1180, 330, { px: 50, align: 'left', a: clamp((st.t - AT('E08@ben')) / .8), kunye: 'Kral Lear, III. perde' });
  return NIGHT;
});
plan('P38', 'E09', (L, st) => {   // terazi: bir kefe ağır
  push(L, st, 960, 540, 1, 1.05);
  const k = ss(clamp((st.t - AT('E09@hidetora')) / .8)), a = -.05 + .22 * k;
  const l = [960 - Math.cos(a) * 420, 360 - Math.sin(a) * 420], r = [960 + Math.cos(a) * 420, 360 + Math.sin(a) * 420];
  RC.S(L, [[960, 860], [960, 340]], { w: 14, tone: TN.nong, dry: .3, seed: 151, prof: 'even' });
  RC.S(L, [l, r], { w: 12, tone: TN.nong, dry: .3, seed: 152, prof: 'even' });
  for (const [p, sz, sd] of [[l, 30, 1], [r, 30 + 60 * k, 2]]) { RC.S(L, [p, [p[0], p[1] + 180]], { w: 3, tone: .6, dry: .5, seed: 160 + sd, prof: 'even' }); INK.blot(L.cw, p[0], p[1] + 210, sz + 30, .6, 0, .5, sd); }
  H.yazi(L, ['LEAR'], l[0], l[1] + 320, { px: 44, bebas: true, ls: 6, a: clamp(st.lt / .6) }); H.yazi(L, ['HİDETORA'], r[0], r[1] + 320, { px: 44, bebas: true, ls: 6, a: clamp((st.lt - .6) / .6) });
  return DAY;
});
plan('P39', 'E10', (L, st) => {   // abartılı jest: ağır, donuk hareket
  cam(L, 960, 560, 1 + .05 * eio(st.p));
  const g = ss(clamp(st.lt / 3));
  RC.figure(L, { x: 960, y: 1000, s: 5.2, dir: 1, pose: 'stand', t: 0, hair: 'old', bowed: -.3 * g, seed: 5, headTone: .5 });
  RC.S(L, [[1010, 600], [1100, 470 - 60 * g], [1180, 420 - 80 * g]], { w: 46, tone: TN.zhong, dry: .45, seed: 171, prof: 'lens' });
  RC.ground(L, 1005, 0, 1920, 1, 26);
  return DAY;
});
plan('P40', 'E11', (L, st) => { H.arsiv(L, IMG.noh, ['Nō maskesi', ['Muromachi dönemi, 1336–1573', 'Japonya, oyma ve boyalı ahşap'], 'The Met · kamu malı (CC0)'], st, { h: 760, y: 70 }); return DAY; });

// ================= F: Flüt =================
plan('P41', 'F01', (L, st) => {   // harabeler gece; kulübe ışığı
  push(L, st, 960, 560, 1, 1.06); H.gece(L, .6, .4);
  for (let k = 0; k < 5; k++) RC.S(L, [[200 + k * 330, 900], [210 + k * 330, 900 - 120 - (k % 3) * 70]], { w: 30, tone: TN.nong, dry: .6, seed: 180 + k, prof: 'robe' });
  INK.mass(L.cw, [[1150, 900], [1450, 900], [1450, 760], [1300, 700], [1150, 760]], .6, 3, 181);
  RC.fire(L, [[1300, 850, 9]], .6, st.t);
  RC.figure(L, { x: lerp(500, 1000, st.p), y: 905, s: 1.3, dir: 1, pose: 'walk', t: st.t, hair: 'old', seed: 5, headTone: .5 });
  RC.ground(L, 905, -200, 2200, 1, 27); H.bolum(L, 'FLÜT', st);
  return NIGHT;
});
plan('P42', 'F02', (L, st) => {   // kulübe içi (üslup orta planı)
  push(L, st, 960, 600, 1, 1.05); H.kulube(L);
  RC.fire(L, [[960, 1000, 13]], .55, st.t); INK.blot(L.cw, 960, 1010, 60, .35, 0, .25, 2);
  RC.figure(L, { x: 560, y: 1010, s: 4.4, dir: 1, pose: 'sit', t: st.t, hair: 'old', bowed: .25, seed: 5 });
  const ts = RC.figure(L, { x: 1400, y: 1010, s: 4.2, dir: -1, pose: 'kneel', t: st.t, hair: 'young', seed: 6, bowed: -.1 * ss(clamp(st.lt / 2)) });
  return DAY;
});
plan('P43', 'F03', (L, st) => { cam(L, 960, 540, 1 + .05 * eio(st.p)); RC.fluteClose(L, { x: 260, y: 640, s: 1, t: st.t, play: 1, seed: 21 }); return DAY; });
plan('P44', 'F04', (L, st) => {   // Hidetora başını eğer, ellerini yüzüne kapatır
  push(L, st, 960, 600, 1.02, 1.08); H.kulube(L);
  const g = ss(clamp(st.lt / 2));
  const hd = RC.figure(L, { x: 900, y: 1010, s: 6, dir: 1, pose: 'sit', t: st.t, hair: 'old', bowed: .2 + .6 * g, seed: 5, headTone: .3 });
  RC.S(L, [[hd.head[0] + 60, hd.head[1] + 140], [hd.head[0] + 50, hd.head[1] + 40 * (1 - g) + 20], [hd.head[0] + 30, hd.head[1] + 10]], { w: 34, tone: TN.zhong, dry: .4, seed: 191, prof: 'lens' });
  return DAY;
});
plan('P45', 'F05', (L, st) => {   // Sue ve Tsurumaru, yıkık sur
  push(L, st, 960, 560, 1, 1.05); H.sis(L, 650, .12, 13);
  INK.mass(L.cw, [[300, 900], [1500, 900], [1450, 700], [1200, 640], [900, 690], [500, 660]], .45, 8, 201);
  RC.figure(L, { x: 900, y: 690, s: 1.7, dir: 1, pose: 'stand', t: st.t, hair: 'woman', seed: 92 });
  RC.figure(L, { x: 1000, y: 692, s: 1.6, dir: -1, pose: 'stand', t: st.t, hair: 'young', seed: 93 });
  return DAY;
});
plan('P46', 'F06', (L, st) => {   // Sue'nün eşiği: sakin duruş, eller kucakta (dinî jest abartılmaz)
  push(L, st, 960, 600, 1, 1.05);
  RC.figure(L, { x: 960, y: 1040, s: 6.2, dir: 1, pose: 'sit', t: st.t, hair: 'woman', seed: 92, headTone: .25, bowed: .25 });
  RC.ground(L, 1045, 0, 1920, 1, 28);
  return DAY;
});
plan('P47', 'F07', (L, st) => { push(L, st, 960, 540, 1, 1.08); const k = clamp(st.lt / 2.5); INK.blot(L.cw, 960, 520, 40 + 260 * eo(k), .75, 0, 1, 11); return { ...DAY, bleed: 6 + 10 * k }; });

// ================= G: Dönüş =================
plan('P48', 'G01', (L, st) => {   // volkanik ova; Saburo gelir
  push(L, st, 960, 560, 1, 1.05);
  H.dag(L, 'ova', [[600, 120, 500], [1500, 90, 400]], 760, { tone: .3, rough: 10, seed: 15 });
  RC.ground(L, 800, -200, 2200, 1, 29);
  RC.figure(L, { x: lerp(1500, 1050, st.p), y: lerp(800, 880, st.p), s: lerp(1.1, 1.9, st.p), dir: -1, pose: 'walk', t: st.t, hair: 'young', seed: 33 });
  RC.figure(L, { x: 700, y: 880, s: 1.9, dir: 1, pose: 'sit', t: st.t, hair: 'old', bowed: .4, seed: 5 });
  H.bolum(L, 'DÖNÜŞ', st);
  return DAY;
});
plan('P49', 'G02', (L, st) => { H.arsiv(L, IMG.cordelia, ['Kral Lear ve Cordelia', ['Francesco Bartolozzi, ~1783', 'Shakespeare, IV. perde'], 'The Met · kamu malı (CC0)'], st, { h: 640 }); return DAY; });
plan('P50', 'G03', (L, st) => {   // baba ve oğul yan yana (silüet)
  push(L, st, 960, 600, 1, 1.05); H.sis(L, 700, .1, 16);
  RC.figure(L, { x: 860, y: 900, s: 3.4, dir: 1, pose: 'stand', t: st.t, hair: 'old', seed: 5, headTone: .4, bowed: .1 });
  RC.figure(L, { x: 1080, y: 900, s: 3.6, dir: -1, pose: 'stand', t: st.t, hair: 'young', seed: 33, headTone: .4 });
  RC.ground(L, 905, -200, 2200, 1, 30);
  return DAY;
});
plan('P51', 'G04', (L, st) => {   // uzak duman; Saburo düşer — gösterilmez: tek figür kalır
  push(L, st, 960, 560, 1, 1.04); H.sis(L, 700, .12, 17);
  const k = clamp((st.t - AT('G04@kurşun')) / .4);
  INK.blot(L.cw, 1600, 520, 30 + 40 * k, .3 * k, 0, .5, 9);
  RC.figure(L, { x: 860, y: 900, s: 3.4, dir: 1, pose: k > .5 ? 'kneel' : 'stand', t: st.t, hair: 'old', seed: 5, headTone: .4, bowed: .1 + .5 * k });
  if (k < .5) RC.figure(L, { x: 1080, y: 900, s: 3.6, dir: -1, pose: 'stand', t: st.t, hair: 'young', seed: 33, headTone: .4 });
  RC.ground(L, 905, -200, 2200, 1, 30);
  return { ...DAY, flash: .3 * Math.max(0, 1 - Math.abs(st.t - AT('G04@kurşun')) * 5) };
});
plan('P52', 'G05', (L, st) => {   // Lear kollarında kızı (uzak silüet)
  push(L, st, 960, 600, 1, 1.05); H.gece(L, .3, .4);
  RC.figure(L, { x: 960, y: 880, s: 2.8, dir: 1, pose: 'stand', t: st.t, hair: 'old', seed: 41, bowed: .35 });
  INK.mass(L.cw, [[930, 700], [1110, 690], [1120, 720], [930, 735]], .55, 3, 211);
  RC.ground(L, 885, -200, 2200, 1, 31);
  H.yazi(L, ['“Asla, asla, asla, asla, asla!”'], 960, 300, { px: 48, a: clamp((st.t - AT('G05@asla')) / .5), kunye: 'Kral Lear, V. perde' });
  return NIGHT;
});
plan('P53', 'G06', (L, st) => {   // boş kapı; düşmüş sancak
  push(L, st, 960, 600, 1, 1.05);
  kapi(L, 960, 860, 520, 520, .9, 40); RC.ground(L, 860, 0, 1920, 1, 32);
  RC.S(L, [[1150, 960], [1600, 900]], { w: 5, tone: TN.nong, dry: .5, seed: 221, prof: 'even' });
  INK.mass(L.cw, [[1500, 905], [1600, 900], [1590, 960], [1480, 965]], .35, 3, 222);
  return DAY;
});
plan('P54', 'G07', (L, st) => {   // Sue geri dönüş yolunda, kaybolur
  push(L, st, 960, 560, 1, 1.05); H.sis(L, 620, .14, 18);
  RC.S(L, [[960, 1100], [1000, 860], [1060, 700], [1100, 620]], { w: 40, tone: .3, dry: .8, seed: 231, prof: 'cone' });
  const k = clamp((st.t - AT('G07@gelmedi')) / 1.2);
  RC.figure(L, { x: lerp(980, 1090, st.p), y: lerp(940, 650, st.p), s: lerp(2.6, 1, st.p), dir: 1, pose: 'walk', t: st.t, hair: 'woman', seed: 92, am: 1 - k });
  return DAY;
});

// ================= H: Surdaki adam =================
function surKaresi(L, st, z = 1) {
  cam(L, 960, 540, z);
  INK.mass(L.cw, [[-200, -200], [2120, -200], [2120, 700], [-200, 700]], .25, 0, 1, [0, 0, 0, 700, .2, 1]);
  INK.mass(L.cw, [[-200, 1300], [-200, 780], [700, 760], [1180, 700], [1240, 720], [1250, 1300]], .7, 10, 241);
  RC.S(L, [[-200, 780], [700, 760], [1180, 700], [1240, 720]], { w: 18, tone: TN.jiao, dry: .4, seed: 242, prof: 'robe' });
  RC.figure(L, { x: 1150, y: 706, s: 1.5, dir: 1, pose: 'stand', t: 0, hair: 'young', seed: 93, headTone: .5 });
}
plan('P55', 'H01', (L, st) => { surKaresi(L, st, 1.08 - .06 * eio(st.p)); H.bolum(L, 'SURDAKİ ADAM', st); return { ...DAY, warm: .7 }; });
plan('P56', 'H02', (L, st) => {   // düşen resim (sarılı kumaş, kırmızı şerit)
  cam(L, 960, 540 + 160 * eio(st.p), 1 + .05 * st.p); const d = clamp((st.t - AT('H02@düşer') + .6) / Math.max(1.4, st.end - AT('H02@düşer')));
  INK.mass(L.cw, [[600, -200], [1300, -200], [1300, 1300], [600, 1300]], .2, 10, 251);
  H.tomar(L, 960 + 60 * d, lerp(380, 1060, d * d), 1.3, .3 + d * 2.2, 1);
  return { ...DAY, warm: .7 };
});
plan('P57', 'H03', (L, st) => { surKaresi(L, st, 1.02); return { ...DAY, warm: .75 }; });
plan('P58', 'H04', (L, st) => {   // üç ayrı kâğıt: Kaede, Sue, Tsurumaru
  push(L, st, 960, 540, 1, 1.04);
  const names = ['KAEDE', 'SUE', 'TSURUMARU'], words = ['kaede', 'sue', 'tsurumaru'];
  for (let k = 0; k < 3; k++) {
    const a = clamp((st.t - AT('H04@' + words[k])) / .5), x = 420 + k * 540;
    if (a <= 0) continue;
    INK.mass(L.cw, [[x - 220, 160], [x + 220, 170], [x + 215, 780], [x - 225, 770]], .06 * a, 2, 260 + k);
    if (k === 0) { RC.fire(L, [[x + 140, 700, 24]], .8 * a, st.t); RC.figure(L, { x, y: 700, s: 2.8, dir: 1, pose: 'sit', t: 0, hair: 'woman', seed: 81, am: a }); }
    if (k === 1) RC.figure(L, { x, y: 700, s: 2.8, dir: 1, pose: 'sit', t: 0, hair: 'woman', seed: 92, bowed: .25, am: a });
    if (k === 2) { INK.mass(L.cw, [[x - 210, 175], [x + 210, 180], [x + 205, 760], [x - 215, 755]], .55 * a, 3, 270); RC.figure(L, { x, y: 700, s: 2.8, dir: 1, pose: 'stand', t: 0, hair: 'young', seed: 93, am: a, headTone: .5 }); }
    H.yazi(L, [names[k]], x, 850, { px: 40, bebas: true, ls: 8, a });
  }
  return DAY;
});
plan('P59', 'H06', (L, st) => { H.arsiv(L, IMG.kuro37, null, st, { h: 820, x: 960 - 820 * 500 / 700 / 2, z: .05 }); return DAY; });
plan('P60', 'H07', (L, st) => {   // fırça üç ok çizer + soru
  push(L, st, 960, 560, 1, 1.04);
  const p = clamp(st.lt / 2.5);
  for (let i = 0; i < 3; i++) RC.S(L, [[700 + i * 40, 900], [740 + i * 40, 300]], { w: 12, tone: TN.nong, dry: .35, seed: 280 + i, prof: 'even', p: clamp(p * 3 - i) });
  H.yazi(L, ['YAPTIKLARIN BİR GÜN', 'SANA DÖNER Mİ?'], 1300, 470, { px: 84, bebas: true, ls: 4, a: clamp((st.t - AT('H08')) / .6) });
  H.yazi(L, ['Hidetora için: evet.'], 1300, 690, { px: 42, font: 'italic 500 ', a: clamp((st.t - AT('H08@evet')) / .5) });
  return DAY;
});
plan('P61', 'H09', (L, st) => {   // asıl soru: sisler kayar, yavaş yaklaşma
  cam(L, 960, 520, 1 + .1 * eio(st.p)); H.sis(L, 760 - 80 * st.p, .12, 6); H.sis(L, 260 + 60 * st.p, .07, 8);
  H.yazi(L, ['SANA YAPILANLA', 'NE YAPARSIN?'], 960, 440, { px: 130, bebas: true, ls: 6, a: clamp((st.lt - .2) / .8) });
  return DAY;
});
plan('P62', 'H10', (L, st) => {   // kurye: yol, sırt çantalı küçük figür; abone
  push(L, st, 960, 560, 1, 1.05); H.sis(L, 700, .1, 19);
  RC.ground(L, 820, -200, 2200, 1, 33);
  RC.figure(L, { x: lerp(500, 1300, st.p), y: 820, s: 1.8, dir: 1, pose: 'walk', t: st.t, hair: 'young', seed: 300 });
  H.yazi(L, ['ZAMAN KURYESİ'], 960, 330, { px: 60, ls: 14, a: clamp(st.lt / .8) });
  return DAY;
});
plan('P63', 'H11', (L, st) => {   // bitiş ekranı: sol yarı boş kâğıt (öğeler için), sağda küçük kaya ve figür
  cam(L, 960, 540, 1);
  INK.mass(L.cw, [[1300, 760], [1500, 520], [1650, 470], [1820, 760]], .45, 8, 311);
  RC.figure(L, { x: 1560, y: 520, s: 1, dir: 1, pose: 'walk', t: st.t, hair: 'young', seed: 312 });
  H.yazi(L, ['ZAMAN KURYESİ'], 960, 140, { px: 50, ls: 14, a: 1 });
  return DAY;
});

// ================= Kapaklar (?kapak=A|B) =================
function kapakYazi(L, lines, x, y, px = 300) {   // col katmanına kâğıt tonunda Bebas; koyu gölge
  const c = L.cc; c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.font = px + 'px "Bebas Neue"'; c.letterSpacing = '4px'; c.textBaseline = 'alphabetic';
  lines.forEach((ln, i) => { c.shadowColor = 'rgba(0,0,0,.75)'; c.shadowBlur = 26; c.fillStyle = '#f3ecdc'; c.fillText(ln, x, y + i * px * .86); });
  c.restore();
}
window.KAPAK = {
  A(L) {   // filmin ilk karesi: yanan kale, kapıdan inen yaşlı figür; yazı solda, sağ alt boş
    cam(L, 960, 560, 1);
    H.gece(L, .7, .42); H.dag(L, 'gece', [[300, 120, 260], [820, 90, 300], [1500, 140, 280]], 700, { tone: .35, mist: 1.2, seed: 4 });
    H.kale(L, { x: 1400, y: 720, s: 1.2, seed: 11 }, 2.3, 1);
    for (let k = 0; k < 3; k++) RC.S(L, [[960 + k * 40, 1090], [1150 + k * 20, 900], [1300 + k * 10, 790], [1370, 726]], { w: 10, tone: .7, dry: .75, seed: 77 + k, prof: 'robe' });
    RC.ground(L, 726, 600, 1920, 1, 8);
    RC.figure(L, { x: 1250, y: 830, s: 2.3, dir: -1, pose: 'walk', t: .4, hair: 'old', bowed: .3, seed: 5, headTone: .65 });
    kapakYazi(L, ['EKTİĞİNİ', 'BİÇTİ'], 70, 420);
    return { ...NIGHT, vig: .45 };
  },
  B(L) {   // üç ok demeti ortadan kırılmış; ateş ışığı solda alçakta; sağ alt (süre rozeti) boş
    cam(L, 960, 560, 1); H.gece(L, .62, .5);
    RC.fire(L, [[1330, 980, 70]], .9, 1.7);
    H.oklar(L, 1330, 990, 1.75, { kir: 1 }); RC.ground(L, 985, 800, 1700, 1, 12);
    kapakYazi(L, ['KIRILMAZ', 'SANDI'], 70, 420);
    return { ...NIGHT, vig: .45 };
  },
};

// A2 ve C (16 Kasım; kullanıcının isteği: büyük insan unsuru + daha yüksek kontrast; C tık tuzağı tarzı ama doğru: Taro ile Jiro'nun orduları babalarının kalesini kuşatır)
function kapakSahne(L, o = {}) {
  cam(L, 960, 560, 1);
  H.gece(L, o.gece ?? .82, .6);
  H.dag(L, 'gece', [[300, 120, 260], [820, 90, 300], [1500, 140, 280]], 700, { tone: .35, mist: 1.2, seed: 4 });
  const K = RC.castle(L, { x: 1560, y: 660, s: .78, seed: 11 });
  RC.smoke(L, 1560, K.top - 10, 300, 420, 2.3, 1, 3);
  RC.fire(L, [[1560, K.top + 30, 46], [K.win[1][0], K.win[1][1] + 10, 16], [K.win[5][0], K.win[5][1] + 10, 18], [1640, K.top + 100, 26]], 1, 2.3);
  if (o.parilti) { const c = L.cc; c.save(); c.setTransform(1, 0, 0, 1, 0, 0); const g = c.createRadialGradient(1560, 420, 20, 1560, 420, 700); g.addColorStop(0, 'rgba(255,110,30,.38)'); g.addColorStop(1, 'rgba(255,110,30,0)'); c.fillStyle = g; c.fillRect(0, 0, 1920, 1080); c.restore(); }
  if (o.oklar) { const tq = 2.3; for (let i = 0; i < 9; i++) { const x = 1150 + i * 70, y = 120 + (i % 3) * 60; RC.S(L, [[x, y], [x + 70, y + 110]], { w: 5, tone: .95, dry: .3, seed: 700 + i, prof: 'nail' }); } for (let k = 0; k < 6; k++) H.sancak(L, 1330 + k * 75, 700 + (k % 2) * 12, 170, 1 + k, 820 + k); }
  RC.ground(L, 690, 1100, 1920, 1, 8);
  // yaşlı adam: önde, büyük, kaleye dönük (yüzsüz); başı koyu
  return RC.figure(L, { x: 1215, y: 1270, s: 6.4, dir: 1, pose: 'stand', t: .4, hair: 'old', bowed: .22, seed: 5, headTone: .85, robeTone: .82 });
}
function kapakYaziC(L, lines, x, y, px = 300) {   // tık tuzağı: sarı, kalın siyah kontur
  const c = L.cc; c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.font = px + 'px "Bebas Neue"'; c.letterSpacing = '4px'; c.lineJoin = 'round';
  lines.forEach((ln, i) => { const yy = y + i * px * .86; c.lineWidth = 22; c.strokeStyle = '#0b0a08'; c.strokeText(ln, x, yy); c.fillStyle = '#ffd21f'; c.fillText(ln, x, yy); });
  c.restore();
}
window.KAPAK.A2 = L => { kapakSahne(L); kapakYazi(L, ['EKTİĞİNİ', 'BİÇTİ'], 60, 420); return { ...NIGHT, vig: .5 }; };
window.KAPAK.C = L => {
  const f = kapakSahne(L, { gece: .75, parilti: true, oklar: true });
  const c = L.cc; c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
  // kırmızı halka yaşlı adamın başı ve omzu çevresinde; yazıdan ona kıvrık ok
  c.strokeStyle = '#ff2a1a'; c.lineWidth = 14; c.beginPath(); c.ellipse(f.head[0] + 10, f.head[1] + 60, 150, 175, -.15, 0, Math.PI * 2); c.stroke();
  c.lineCap = 'round'; c.beginPath(); c.moveTo(860, 760); c.quadraticCurveTo(930, 900, f.head[0] - 150, f.head[1] + 110); c.stroke();
  const ax = f.head[0] - 150, ay = f.head[1] + 110; c.beginPath(); c.moveTo(ax, ay); c.lineTo(ax - 52, ay - 14); c.moveTo(ax, ay); c.lineTo(ax - 30, ay + 44); c.stroke();
  c.restore();
  kapakYaziC(L, ['OĞULLARI', 'SALDIRDI!'], 60, 400);
  return { ...NIGHT, vig: .4, warm: .7 };
};
