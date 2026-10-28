// Çekim sistemi: çekimler anlatım işaretlerine bağlanır, geçişler ve son işlem burada.
'use strict';
const S = id => (CUES[id] ? CUES[id].s : 0);          // segment başlangıcı
const Se = id => (CUES[id] ? CUES[id].e : 0);         // segment bitişi
// segment içindeki bir kelimenin zamanı (n. geçiş)
function Wd(id, w, n = 0, end = false) {
  const nw = w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  let k = 0;
  for (const x of (window.WORDS || [])) if (x.id === id && x.w.startsWith(nw)) { if (k++ === n) return end ? x.e : x.s; }
  // bulunamayan kelime sessizce cümle başına düşmesin: konsolda uyarı (ç, ş, ğ, ı, ö, ü korunur; yalnız â î û sadeleşir)
  const wk = id + '/' + w + '/' + n; if (!(Wd.warned ||= {})[wk]) { Wd.warned[wk] = 1; console.warn(`Wd: "${w}" (${n}) ${id} cümlesinde yok, cümle başı kullanıldı`); }
  return S(id);
}
const SHOTS = [];
// shot(başlangıç, çizim, {tr:{type,dur}, post:{...}})
function shot(at, draw, o = {}) { SHOTS.push({ at, draw, ...o }); }
const bufA = makeCanvas(DW, DH), bufAx = bufA.getContext('2d');
const maskC = makeCanvas(480, 270), maskX = maskC.getContext('2d');
let NOISE_MASK = null;
function noiseMask() {
  if (NOISE_MASK) return NOISE_MASK;
  const w = 480, h = 270, a = new Float32Array(w * h);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    let v = 0, amp = .6, f = 1 / 60;
    for (let o = 0; o < 4; o++) { v += amp * noise2(x * f, y * f, 40 + o); amp *= .5; f *= 2.2; }
    a[y * w + x] = v;
  }
  let mn = 1e9, mx = -1e9; for (const v of a) { mn = Math.min(mn, v); mx = Math.max(mx, v); }
  for (let i = 0; i < a.length; i++) a[i] = (a[i] - mn) / (mx - mn);
  NOISE_MASK = a; return a;
}
function shotAt(t) {
  let i = 0;
  for (let k = 0; k < SHOTS.length; k++) if (SHOTS[k].at <= t) i = k;
  return i;
}
function drawShot(ctx, i, t) {
  const sh = SHOTS[i]; if (!sh) return;
  const end = (SHOTS[i + 1] ? SHOTS[i + 1].at : DUR);
  const st = { t, lt: t - sh.at, d: end - sh.at, p: clamp((t - sh.at) / (end - sh.at)), end };
  ctx.save();
  // kullanıcı isteği "görüntü hiç durmasın": her çekimde sürekli, gözle seçilir kamera hareketi. Yakınlaşma ilk saniyelerde
  // ~%0,7/sn hızla başlar, %6'ya doğru yavaşlar; kenar payı içinde tek yönlü kayma (sh.focus varsa ona doğru).
  // Kendi cam() yakınlaşması olan çekimlerde (sh._own, bir kez ölçülür) genel hareket hiç uygulanmaz: üst üste binmez.
  // Ekran yazıları (ui.js) bu hareketi geri alır; doku (taş, kâğıt) aynı dönüşümle kâğıda bağlı kalır (pressFinish).
  // Bitiş ekranı (YouTube öğeleri) ve sh.still sabit.
  window.DRIFT = null;
  if (sh._own === undefined) sh._own = probeOwnCam(sh, i);
  if (!sh.still && !sh._own && !(window.CUES && CUES.G06 && sh.at >= Se('G06') - .5)) {
    const a = .06 * (1 - Math.exp(-st.lt / 9)), z = 1 + a, m = a * .5;
    const ang = sh.focus ? Math.atan2(sh.focus[1] - H / 2, sh.focus[0] - W / 2) : hash(i * 7.31 + 3.7) * TAU;
    const px = Math.cos(ang) * .6 * m * W, py = Math.sin(ang) * .6 * m * H;
    ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2 - px, -H / 2 - py);
    window.DRIFT = { z, px, py };
  }
  sh._drift = window.DRIFT;
  sh.draw(ctx, st);
  window.DRIFT = null;
  ctx.restore();
}
// çekimin kendi kamera yakınlaşması var mı: üç anda küçük bir tuvale çizilip cam() çağrıları ölçülür (belirlenimci;
// her render işçisinde aynı sonuç). Çizimin yan etkileri (REG, alt bant, yüz saati) geri alınır.
const PROBE = makeCanvas(8, 8).getContext('2d');
function probeOwnCam(sh, i) {
  const end = (SHOTS[i + 1] ? SHOTS[i + 1].at : DUR), d = end - sh.at, keep = [REG.boost, window.LOWBAND_AT, window.FIG_T, window.DRIFT];
  let mx = 0;
  for (const u of [.15, .5, .85]) {
    const t = sh.at + d * u; window.__camz = 1; window.DRIFT = null;
    try { PROBE.save(); sh.draw(PROBE, { t, lt: t - sh.at, d, p: u, end }); } catch (e) { /* ölçüm çizimi */ } finally { PROBE.restore(); }
    mx = Math.max(mx, Math.abs(window.__camz - 1));
  }
  [REG.boost, window.LOWBAND_AT, window.FIG_T, window.DRIFT] = keep; window.__camz = 1;
  return mx > .012;
}
function drawFilm(ctx, t) {
  const sc = new URLSearchParams(location.search).get('scene');
  if (sc && typeof SCENES !== 'undefined' && SCENES[sc]) return SCENES[sc](ctx, t);
  const i = shotAt(t), sh = SHOTS[i];
  if (!sh) { paperBG(ctx); return; }
  const tr = sh.tr;
  if (tr && i > 0 && t < sh.at + tr.dur && tr.type === 'reg') {
    // kayık baskı oturması (imza geçiş): yeni kare doğrudan gelir; kalıplar kayık basılıp yerine oturur, üstünde kayan bir çarpma gölgesi söner
    const p = clamp((t - sh.at) / tr.dur);
    REG.boost = 1 + 3 * (1 - E.out3(p)); drawShot(ctx, i, t); REG.boost = 1;
    bufAx.setTransform(1, 0, 0, 1, 0, 0); bufAx.globalAlpha = 1; bufAx.globalCompositeOperation = 'copy'; bufAx.drawImage(ctx.canvas, 0, 0); bufAx.globalCompositeOperation = 'source-over';
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = .45 * (1 - E.out3(p));
    ctx.drawImage(bufA, 12 * RS * (1 - p), 7 * RS * (1 - p)); ctx.restore();
  } else if (tr && i > 0 && t < sh.at + tr.dur && tr.type !== 'cut') {
    const p = clamp((t - sh.at) / tr.dur);
    // baskı geçişi: yeni sahnenin kalıpları kayık basılır, sonra yerine oturur
    if (tr.type === 'press') REG.boost = 1 + 5 * (1 - E.out3(p));
    drawShot(ctx, i, t);
    REG.boost = 1;
    baseT(bufAx); bufAx.globalAlpha = 1; bufAx.globalCompositeOperation = 'source-over';
    bufAx.clearRect(0, 0, W, H);
    drawShot(bufAx, i - 1, t);
    composite(ctx, bufA, tr, p);
  } else drawShot(ctx, i, t);
  // film boyu izleyici katmanı (kuşak şeridi vb.): çekimlerden bağımsız, baskı bitişinden önce
  if (typeof kusakBar === 'function') { ctx.save(); baseT(ctx); kusakBar(ctx, t); ctx.restore(); }
  POST = { ...(sh.post || {}), drift: sh._drift }; // doku, gelen çekimin kamera hareketiyle kâğıda bağlı
  post(ctx, t);
}
// önceki çekimi (buf) mevcut kareye geçiş maskesiyle bindir
function composite(ctx, buf, tr, p) {
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  if (tr.type === 'fade') { ctx.globalAlpha = 1 - E.sine(p); ctx.drawImage(buf, 0, 0); }
  else if (tr.type === 'black') {
    // önce eski kararır, sonra yeni açılır
    if (p < .5) { ctx.drawImage(buf, 0, 0); ctx.fillStyle = '#000'; ctx.globalAlpha = E.sine(p * 2); ctx.fillRect(0, 0, DW, DH); }
    else { ctx.fillStyle = '#000'; ctx.globalAlpha = 1 - E.sine((p - .5) * 2); ctx.fillRect(0, 0, DW, DH); }
  } else if (tr.type === 'white') {
    if (p < .5) { ctx.drawImage(buf, 0, 0); ctx.fillStyle = '#F4E9D2'; ctx.globalAlpha = E.sine(p * 2); ctx.fillRect(0, 0, DW, DH); }
    else { ctx.fillStyle = '#F4E9D2'; ctx.globalAlpha = 1 - E.sine((p - .5) * 2); ctx.fillRect(0, 0, DW, DH); }
  } else if (tr.type === 'clay' || tr.type === 'ink') {
    // organik çözülme: gürültü eşiği ile yumuşak kenarlı maske
    const nm = noiseMask(), id = maskX.createImageData(480, 270), d = id.data;
    const soft = .08, th = lerp(-soft, 1 + soft, E.io2(p));
    for (let k = 0; k < nm.length; k++) {
      const v = clamp((nm[k] - th) / soft + .5);
      d[k * 4 + 3] = v * 255;
    }
    maskX.putImageData(id, 0, 0);
    bufAx.save(); baseT(bufAx); bufAx.globalCompositeOperation = 'destination-in';
    bufAx.imageSmoothingQuality = 'high'; bufAx.drawImage(maskC, 0, 0, W, H); bufAx.restore();
    ctx.drawImage(buf, 0, 0);
  } else if (tr.type === 'press') {
    // baskı merdanesi: soldan sağa yumuşak kenarlı silme; kenarda is izi
    const x = lerp(-160, W + 160, E.io2(p));
    const g = bufAx.createLinearGradient(x - 60, 0, x + 60, 0);
    g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, '#000');
    bufAx.save(); baseT(bufAx); bufAx.globalCompositeOperation = 'destination-in'; bufAx.fillStyle = g; bufAx.fillRect(0, 0, W, H); bufAx.restore();
    ctx.drawImage(buf, 0, 0);
    ctx.save(); baseT(ctx); ctx.globalAlpha = .55 * Math.sin(PI * p); ctx.fillStyle = P.ink;
    for (let k = 0; k < 3; k++) ctx.fillRect(x - 64 + k * 9 + noise1(p * 40, k) * 3, 0, 3.2, H);
    ctx.restore();
  } else if (tr.type === 'wipe') {
    const x = lerp(-200, W + 200, E.io3(p)), dir = tr.dir || 1;
    const g = bufAx.createLinearGradient(x - 120, 0, x + 120, 0);
    g.addColorStop(0, dir > 0 ? 'rgba(0,0,0,0)' : '#000'); g.addColorStop(1, dir > 0 ? '#000' : 'rgba(0,0,0,0)');
    bufAx.save(); baseT(bufAx); bufAx.globalCompositeOperation = 'destination-in'; bufAx.fillStyle = g; bufAx.fillRect(0, 0, W, H); bufAx.restore();
    ctx.drawImage(buf, 0, 0);
  } else if (tr.type === 'iris') {
    const cx = tr.x ?? W / 2, cy = tr.y ?? H / 2, r = lerp(0, 1300, E.io3(p));
    bufAx.save(); baseT(bufAx); bufAx.globalCompositeOperation = 'destination-out';
    const g = bufAx.createRadialGradient(cx, cy, Math.max(0, r - 60), cx, cy, r);
    g.addColorStop(0, '#000'); g.addColorStop(1, 'rgba(0,0,0,0)');
    bufAx.fillStyle = g; bufAx.beginPath(); bufAx.arc(cx, cy, r + 2, 0, TAU); bufAx.fill(); bufAx.restore();
    ctx.drawImage(buf, 0, 0);
  }
  ctx.restore();
}
// Son işlem: taş greni + kâğıt + vinyet + gren. Çekimler kendi ayarını sh.post ile verir.
let POST = {};
function post(ctx, t) { pressFinish(ctx, t, POST); }
// Kamera: dünya koordinatından ekrana (merkez cx,cy, yakınlık z, dönüş r); katman derinliği k ile paralaks
function cam(ctx, c, k = 1) {
  // c.x, c.y: ekran merkezine gelen dünya noktası; k: paralaks derinliği (0 sabit, 1 tam)
  const z = 1 + ((c.z ?? 1) - 1) * k;
  const cx = W / 2 + ((c.x ?? W / 2) - W / 2) * k, cy = H / 2 + ((c.y ?? H / 2) - H / 2) * k;
  if (Math.abs(z - 1) > Math.abs((window.__camz ?? 1) - 1)) window.__camz = z; // probeOwnCam ölçümü
  ctx.translate(W / 2 + (c.sx || 0), H / 2 + (c.sy || 0));
  ctx.rotate((c.r || 0) * k);
  ctx.scale(z, z);
  ctx.translate(-cx, -cy);
}
function shake(t, t0, amp, dec = 6, f = 23) {
  if (t < t0) return [0, 0];
  const e = Math.exp(-(t - t0) * dec) * amp;
  return [noise1(t * f, 1) * e, noise1(t * f, 2) * e];
}
// Shorts gibi kurgularda film içi yazılar kapatılabilir (?notext=1)
const NOTEXT = typeof location !== 'undefined' && new URLSearchParams(location.search).has('notext');
