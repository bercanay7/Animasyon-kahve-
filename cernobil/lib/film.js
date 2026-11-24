// Çekim sistemi (Çernobil'in çayı; frankenstein/lib/film.js'ten: baskı motoruna bağlandı, geçişler sayfa ve merdane). ORTAK DOSYA: yalnız başkan değiştirir.
// Çekimler anlatım işaretlerine bağlanır (timeline.js: window.CUES, window.WORDS, window.DUR; seslendirme kesin).
// Plan listesi planlar.js (window.PLAN; kaynak tools/planlar_kaynak.py). Her set dosyası kendi plan('Pxxx', draw, o) çağrılarını yapar.
'use strict';

// ── zaman çapaları ──
const S = id => (window.CUES && CUES[id] ? CUES[id].s : 0);          // cümle başı
const Se = id => (window.CUES && CUES[id] ? CUES[id].e : 0);         // cümle sonu
// cümle içindeki bir kelimenin zamanı (n. geçiş; önek eşleşmesi); end: kelime sonu
function Wd(id, w, n = 0, end = false) {
  const nw = w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  let k = 0;
  for (const x of (window.WORDS || [])) if (x.id === id && x.w.startsWith(nw)) { if (k++ === n) return end ? x.e : x.s; }
  console.log('kelime yok: ' + id + '@' + w);
  return S(id);
}
// çapa: 'A01' cümle başı, 'A01@kelime' kelime, 'A01@kelime#1' ikinci geçiş, '+0.3' / '-0.4' kaydırma (planlar.json ile aynı yazım)
function A(at) {
  const m = String(at).match(/^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$/);
  if (!m) { console.log('çapa bozuk: ' + at); return 0; }
  return (m[2] ? Wd(m[1], m[2], +(m[3] || 0)) : S(m[1])) + (m[4] ? +m[4] : 0);
}
// plan çapası: PA('P016') = planlar.json'daki 'at'; off saniye kaydırma
function PA(id, off = 0) { const p = (window.PLAN || {})[id]; if (!p) { console.log('plan yok: ' + id); return 0; } return A(p.at) + off; }
// plan eylemlerinin zamanı: PE('P053', 1) = 2. eylemin çapası (planlar.json 'eylem'[1].at); bulunmazsa plan başı
function PE(id, k, off = 0) { const p = (window.PLAN || {})[id]; const e = p && p.eylem && p.eylem[k]; return (e ? A(e.at) : PA(id)) + off; }
// plan bilgisi
const PL = id => (window.PLAN || {})[id] || {};
const trOf = id => ({ ...(PL(id).tr || { type: 'cut' }) });

// ── çekimler ──
const SHOTS = [];
let SHOTS_SORTED = false;
// shot(başlangıç, çizim, {tr: {type: 'cut'|'fade'|'black'|'white'|'bloom', dur, end, keep}, over, post: {tex, vig, grain}, mb, id})
// tr.end: yumuşak geçiş çapada BİTER (önceki sessizlikte oynar); çekim dur kadar önce başlar
function shot(at, draw, o = {}) { if (o.tr && o.tr.end && o.tr.type !== 'cut') at -= o.tr.dur; SHOTS.push({ at, draw, ...o }); SHOTS_SORTED = false; }
// plan kimliğiyle çekim: plan('P016', (ctx, st) => {...}, { tr: trOf('P016'), over }). tr verilmezse planlar.json'daki geçiş.
function plan(id, draw, o = {}) {
  if (SHOTS.some(s => s.id === id)) { console.log('plan iki kez kaydedildi: ' + id); return; }
  const tr = o.tr || trOf(id);
  shot(PA(id, o.off || 0), draw, { id, ...o, tr });
}
// Geçiş politikası (Milton kurgu kurulu tur 1; CLAUDE.md "geçiş"): kayıttan sonra bir kez uygulanır.
//  - aynı set içinde fade → kesme (aynı mekânda kadraj değişimi kesmedir). İstisna: TR_SUREKLI setleri ve tr.keep.
//  - setler arası fade en çok 0,7 sn; öncesinde ≥ 0,7 sn sessizlik varsa o sessizlikte oynar (çapada biter).
//  - black / white / bloom / cut dokunulmaz.
const TR_SUREKLI = {};
function normTransitions() {
  const P = window.PLAN || {}, set = sh => (sh.id && P[sh.id] ? P[sh.id].set : null);
  const cues = Object.values(window.CUES || {}).sort((a, b) => a.s - b.s);
  const sessiz = t => { let pe = -1e9; for (const c of cues) { if (c.s > t + .06) break; if (c.s > t - .06) return c.s - pe; pe = c.e; } return 0; };
  SHOTS.sort((a, b) => a.at - b.at);
  for (let i = 1; i < SHOTS.length; i++) {
    const sh = SHOTS[i], tr = sh.tr; if (!tr || tr.type !== 'fade' || tr.keep || sh._n) continue; sh._n = 1;
    const a0 = tr.end ? sh.at + tr.dur : sh.at, s0 = set(SHOTS[i - 1]), s1 = set(sh);
    if (s0 && s0 === s1 && !TR_SUREKLI[s1]) { sh.tr = { type: 'cut' }; sh.at = a0; continue; }
    const dur = Math.min(tr.dur || .7, .7), end = tr.end || sessiz(a0) >= .7;
    sh.tr = { ...tr, dur, end }; sh.at = end ? a0 - dur : a0;
  }
}
function shotsReady() { if (!SHOTS_SORTED) { normTransitions(); SHOTS.sort((a, b) => a.at - b.at); SHOTS_SORTED = true; } }
function shotAt(t) {
  shotsReady();
  let i = 0;
  for (let k = 0; k < SHOTS.length; k++) if (SHOTS[k].at <= t) i = k;
  return i;
}
// st: {t (film zamanı), lt (çekim içi zaman), d (çekim süresi), p (0..1), at, end, id}
function shotState(i, t) {
  const sh = SHOTS[i], end = (SHOTS[i + 1] ? SHOTS[i + 1].at : (window.DUR || sh.at + 10));
  return { t, at: sh.at, lt: t - sh.at, d: end - sh.at, p: clamp((t - sh.at) / (end - sh.at)), end, id: sh.id };
}
// Çekim çizimi: sahne üç plakaya çizer (BASKI.k ton, .l çizgi, .c çay), sonra gölgelendirici gazete kâğıdına basar. o.duz: doğrudan 2B çizim.
// sh.baski: {kay, per, kagit, gate} ya da st → nesne.
function drawShot(ctx, i, t) {
  const sh = SHOTS[i]; if (!sh) return;
  window.FIG_T = t; const st = shotState(i, t);
  if (sh.duz) { ctx.save(); baseT(ctx); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none'; sh.draw(ctx, st); ctx.restore(); return; }
  BASKI.begin(typeof sh.baski === 'function' ? sh.baski(st) : (sh.baski || {}));
  sh.draw(BASKI, st);
  BASKI.compose(ctx);
}

// ── geçişler: 'cut' | 'fade' (gürültü eşikli çözülme) | 'black' | 'sayfa' (yeni sayfa sağdan gelir: mekân sıçraması) | 'merdane' (yeni kare soldan sağa basılır: zaman sıçraması) ──
const bufA = makeCanvas(DW, DH), bufAx = bufA.getContext('2d');
const maskC = makeCanvas(480, 270), maskX = maskC.getContext('2d');
let NOISE_MASK = null;
function noiseMask() {
  if (NOISE_MASK) return NOISE_MASK;
  const w = 480, h = 270, a = new Float32Array(w * h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { let v = 0, amp = .6, f = 1 / 60; for (let o = 0; o < 4; o++) { v += amp * noise2(x * f, y * f, 40 + o); amp *= .5; f *= 2.2; } a[y * w + x] = v; }
  let mn = 1e9, mx = -1e9; for (const v of a) { mn = Math.min(mn, v); mx = Math.max(mx, v); }
  for (let i = 0; i < a.length; i++) a[i] = (a[i] - mn) / (mx - mn);
  return (NOISE_MASK = a);
}
function maskFrom(p) {
  const nm = noiseMask(), id = maskX.createImageData(480, 270), d = id.data, soft = .05, th = lerp(-soft, 1 + soft, E.io2(p));
  for (let k = 0; k < nm.length; k++) d[k * 4 + 3] = clamp((nm[k] - th) / soft + .5) * 255;
  maskX.putImageData(id, 0, 0);
  bufAx.save(); bufAx.setTransform(1, 0, 0, 1, 0, 0); bufAx.globalCompositeOperation = 'destination-in'; bufAx.imageSmoothingQuality = 'high'; bufAx.drawImage(maskC, 0, 0, DW, DH); bufAx.restore();
}
function drawFilm(ctx, t) {
  if (!SHOTS.length) return;
  const i = shotAt(t), sh = SHOTS[i], tr = sh.tr;
  if (tr && i > 0 && t < sh.at + tr.dur && tr.type !== 'cut') {
    const p = clamp((t - sh.at) / tr.dur);
    if (tr.type === 'black') {
      drawShot(ctx, p < .5 ? i - 1 : i, t);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#1C1712';
      ctx.globalAlpha = p < .5 ? E.sine(p * 2) : 1 - E.sine((p - .5) * 2); ctx.fillRect(0, 0, DW, DH); ctx.restore();
    } else if (tr.type === 'sayfa') { // yeni sayfa sağdan üstüne kayar; kenarında ince gölge
      const e = E.io3(p), x0 = DW * (1 - e);
      drawShot(ctx, i - 1, t);
      bufAx.setTransform(1, 0, 0, 1, 0, 0); bufAx.globalAlpha = 1; bufAx.globalCompositeOperation = 'source-over'; bufAx.clearRect(0, 0, DW, DH); drawShot(bufAx, i, t);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
      const g = ctx.createLinearGradient(x0 - 40 * RS, 0, x0, 0); g.addColorStop(0, 'rgba(30,22,14,0)'); g.addColorStop(1, 'rgba(30,22,14,.35)');
      ctx.fillStyle = g; ctx.fillRect(x0 - 40 * RS, 0, 40 * RS, DH); ctx.drawImage(bufA, x0, 0); ctx.restore();
    } else if (tr.type === 'merdane') { // matbaa merdanesi: yeni kare soldan sağa basılır, sınırda koyu mürekkep bandı
      const e = E.io2(p), xs = DW * e, bant = 18 * RS;
      drawShot(ctx, i - 1, t);
      bufAx.setTransform(1, 0, 0, 1, 0, 0); bufAx.globalAlpha = 1; bufAx.globalCompositeOperation = 'source-over'; bufAx.clearRect(0, 0, DW, DH); drawShot(bufAx, i, t);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(bufA, 0, 0, xs, DH, 0, 0, xs, DH);
      const g = ctx.createLinearGradient(xs - bant, 0, xs + bant * .4, 0); g.addColorStop(0, 'rgba(34,28,23,0)'); g.addColorStop(.7, 'rgba(34,28,23,.55)'); g.addColorStop(1, 'rgba(34,28,23,0)');
      ctx.fillStyle = g; ctx.fillRect(xs - bant, 0, bant * 1.4, DH); ctx.restore();
    } else { // fade: eşikli çözülme
      drawShot(ctx, i, t);
      bufAx.setTransform(1, 0, 0, 1, 0, 0); bufAx.globalAlpha = 1; bufAx.globalCompositeOperation = 'source-over'; bufAx.clearRect(0, 0, DW, DH);
      drawShot(bufAx, i - 1, t); maskFrom(p);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(bufA, 0, 0); ctx.restore();
    }
  } else drawShot(ctx, i, t);
  post(ctx, t, sh.post);
}
// Son işlem: vinyet + gren (iki karede bir değişir). Çekim post: {vig, grain}
let VIG = null, GRAIN = [];
function postHazirla() {
  VIG = makeCanvas(DW, DH); const v = VIG.getContext('2d'), g = v.createRadialGradient(DW / 2, DH * .48, DH * .35, DW / 2, DH / 2, DW * .62);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(40,26,12,.45)'); v.fillStyle = g; v.fillRect(0, 0, DW, DH);
  for (let k = 0; k < 4; k++) { const c = makeCanvas(512, 512), x = c.getContext('2d'), id = x.createImageData(512, 512), r = rng(100 + k); for (let i = 0; i < id.data.length; i += 4) { const q = 128 + (r() - .5) * 120; id.data[i] = id.data[i + 1] = id.data[i + 2] = q; id.data[i + 3] = 255; } x.putImageData(id, 0, 0); GRAIN.push(c); }
}
function post(ctx, t, o = {}) {
  const fi = Math.round(t * 30), vig = o.vig ?? .35, gr = o.grain ?? 0;
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (vig > 0) { ctx.globalAlpha = vig; ctx.drawImage(VIG, 0, 0); }
  if (gr > 0) { const g = Math.floor(fi / 2), r = rng(g + 1); ctx.globalCompositeOperation = 'overlay'; ctx.globalAlpha = gr; const ox = -r() * 512, oy = -r() * 512, tile = GRAIN[g % 4]; for (let y = oy; y < DH; y += 512) for (let x = ox; x < DW; x += 512) ctx.drawImage(tile, x, y); }
  ctx.restore();
}

// ── üst katman (ekran yazıları): hareket bulanıklığından ve son işlemden sonra, kamera dönüşümü olmadan (telefonda okunurluk) ──
function drawOver(ctx, t) {
  if (!SHOTS.length) return;
  const i = shotAt(t), sh = SHOTS[i]; if (!sh) return;
  const pv = i > 0 ? SHOTS[i - 1] : null;
  if (pv && pv.over && sh.tr && sh.tr.type !== 'cut' && t - sh.at < sh.tr.dur) {
    ctx.save(); baseT(ctx); ctx.globalAlpha = 1 - E.sine(clamp((t - sh.at) / sh.tr.dur * 2));
    pv.over(ctx, { ...shotState(i - 1, t), end: sh.at }); ctx.restore();
  }
  if (!sh.over) return;
  const st = shotState(i, t);
  ctx.save(); baseT(ctx); ctx.globalAlpha = 1;
  if (sh.tr && sh.tr.type !== 'cut' && st.lt < sh.tr.dur) ctx.globalAlpha = clamp((st.lt / sh.tr.dur - .5) * 2);
  sh.over(ctx, st);
  ctx.restore();
}

// ── ekran yazıları ──
// Yazı dili 1986 gazetesi: manşet Anton (dar, kalın), metin ve alıntı Cormorant Garamond, belge ve sayı Courier Prime, kapak sözü Bebas Neue.
// Üst katmandaki yazılar (künye, etiket) kâğıt renkli yumuşak zemin üstüne mürekkep rengi. Sahnenin içindeki kupürler BASKI.l plakasına basılır (notext'te de kalır).
// Telefon kuralı: alıntı ≥ 64 px, etiket ve künye ≥ 40 px. Yerleşim: yazı x 120–1800, y 90–880; y > 880 ALTYAZININ YERİ.
const NOTEXT = typeof location !== 'undefined' && new URLSearchParams(location.search).has('notext');
const FONT = {
  manset: (px) => `400 ${px}px Anton`, baslik: (px, w = 400) => `400 ${px}px Anton`, alinti: (px, w = 600) => `italic ${w} ${px}px "Cormorant Garamond"`,
  metin: (px, w = 600) => `${w} ${px}px "Cormorant Garamond"`, daktilo: (px, w = 700) => `${w} ${px}px "Courier Prime"`, buyuk: px => `400 ${px}px "Bebas Neue"` };
const YAZI = { krem: '#221C17', kagit: '#ECE2C9', kirmizi: '#9A2E18', sepya: '#221C17', ymax: 880, xmin: 120, xmax: 1800 };
const C = { red: '#9A2E18' };
const yClamp = (y, hh = 0) => Math.min(y, YAZI.ymax - hh / 2);
function softPanel(ctx, x, y, rx, ry, a = .78, rgb = '236,226,201') {
  const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
  g.addColorStop(0, `rgba(${rgb},${a})`); g.addColorStop(.62, `rgba(${rgb},${a * .9})`); g.addColorStop(1, `rgba(${rgb},0)`);
  ctx.save(); ctx.translate(x, y); ctx.scale(rx, ry); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 1, 0, TAU); ctx.fill(); ctx.restore();
}
function wrapLines(ctx, s, maxW) {
  const out = []; for (const par of String(s).split('\n')) { let ln = ''; for (const w of par.split(' ')) { const tt = ln ? ln + ' ' + w : w; if (ctx.measureText(tt).width > maxW && ln) { out.push(ln); ln = w; } else ln = tt; } out.push(ln); }
  return out;
}
// txt(ctx, s, x, y, {font, px, col, a, align, ls (harf aralığı px), panel, force (notext'te de çiz)})
function txt(ctx, s, x, y, o = {}) {
  if ((NOTEXT && !o.force) || !s) return;
  const px = o.px || 48;
  ctx.save(); ctx.font = o.font || FONT.baslik(px); ctx.textAlign = o.align || 'center'; ctx.textBaseline = 'middle';
  if (o.ls) ctx.letterSpacing = o.ls + 'px';
  ctx.globalAlpha *= clamp(o.a ?? 1);
  y = yClamp(y, px);
  if (o.panel) { const wd = ctx.measureText(s).width, cx = o.align === 'left' ? x + wd / 2 : o.align === 'right' ? x - wd / 2 : x; softPanel(ctx, cx, y, wd * .5 + px * 1.6, px * 1.5, o.panel === true ? .78 : o.panel, o.panelRGB); }
  ctx.fillStyle = o.col || YAZI.krem; ctx.fillText(s, x, y);
  ctx.restore();
}
// alıntı: satır satır beliren italik metin. lt: çekim içi zaman; o: {px (≥64), maxW, col, t0 (başlama, çekim içi sn), per (satır başına sn), panel, kaynak (künye)}
function quote(ctx, s, x, y, lt, o = {}) {
  if (NOTEXT || !s) return;
  const px = o.px || 68, lh = px * 1.22;
  ctx.save(); const A0 = ctx.globalAlpha;
  ctx.font = FONT.alinti(px); const L = wrapLines(ctx, s, o.maxW || 1240);
  const kpx = Math.max(40, Math.round(px * .42)), kEk = o.kaynak ? kpx + 34 : 0, hh = L.length * lh + kEk;
  y = yClamp(y, hh); const y0 = y - (L.length - 1) * lh / 2 - kEk / 2;
  const t0 = o.t0 || 0, per = o.per ?? .5, aAll = clamp((lt - t0) / .5);
  if (o.panel !== false && aAll > 0) { let wd = 0; for (const l of L) wd = Math.max(wd, ctx.measureText(l).width); ctx.globalAlpha = A0 * aAll; softPanel(ctx, x, y, wd * .5 + px * 1.8, hh * .5 + px * 1.2, o.panel ?? .8); }
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = o.col || YAZI.krem;
  L.forEach((l, i) => { const a = clamp((lt - t0 - i * per) / .6); if (a <= 0) return; ctx.globalAlpha = A0 * E.sine(a); ctx.fillText(l, x, y0 + i * lh + (1 - E.out3(a)) * 10); });
  if (o.kaynak) { const a = clamp((lt - t0 - L.length * per) / .6); ctx.globalAlpha = A0 * E.sine(a); ctx.font = FONT.baslik(kpx, 600); ctx.letterSpacing = '3px'; ctx.fillText(o.kaynak, x, y0 + (L.length - 1) * lh + px * .62 + 30 + kpx / 2); }
  ctx.restore();
}
// etiket: küçük büyük harfli ad (kişi, yer, yıl). lt ile belirir, d sonunda söner
function etiket(ctx, s, x, y, lt, d = 4, o = {}) {
  if (NOTEXT || !s) return;
  const a = clamp(lt / .5) * clamp((d - lt) / .5); if (a <= 0) return;
  txt(ctx, s, x, y, { px: o.px || 44, ls: o.ls ?? 6, a: E.sine(a), panel: o.panel ?? .7, col: o.col, align: o.align, font: FONT.baslik(o.px || 44, 600) });
}
// künye: kaynak satırı (sol alt köşe, altyazı bandının üstünde; y ≤ 880). lt ile belirir; d verilirse sonunda söner
function kunye(ctx, s, lt, d = 99, o = {}) {
  if (NOTEXT || !s) return;
  const a = clamp((lt - (o.t0 || 0)) / .5) * clamp((d - lt) / .5); if (a <= 0) return;
  txt(ctx, s, o.x ?? 120, o.y ?? 846, { px: o.px || 40, ls: 2, a: E.sine(a) * (o.a ?? .92), align: o.align || 'left', font: FONT.metin(o.px || 40, 600), col: o.col || YAZI.krem, panel: o.panel ?? .55 });
}
// büyük tek söz (ör. P053 “O benim.”, Bebas, kırmızı): t0 (film zamanı) ile belirir; o: {px, col, y, x}
function buyukSoz(ctx, s, t, t0, o = {}) {
  if (NOTEXT || !s || t < t0) return;
  const a = E.out3(clamp((t - t0) / .25)), px = o.px || 150;
  txt(ctx, s, o.x ?? W / 2, o.y ?? 230, { font: FONT.buyuk(px), px, ls: o.ls ?? 4, col: o.col || YAZI.krem, a: a * (o.a ?? 1), panel: o.panel ?? .6 });
}
// sahne(id, çapa, set, ölçek, çizim, o): plan kaydı + çekim. ölçek: 'genis' | 'orta' | 'yakin' | 'ayrinti' | 'kart' (ardışık iki plan aynı ölçekte olmaz; tools/kontrol.js)
window.PLAN = window.PLAN || {};
function sahne(id, at, set, olcek, draw, o = {}) {
  PLAN[id] = { at, set, olcek, tr: o.tr || { type: 'cut' } };
  plan(id, draw, o);
}
