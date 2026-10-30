// Çekim sistemi: çekimler anlatım işaretlerine bağlanır, geçişler ve son işlem burada.
'use strict';
const S = id => (CUES[id] ? CUES[id].s : 0);          // segment başlangıcı
const Se = id => (CUES[id] ? CUES[id].e : 0);         // segment bitişi
// segment içindeki bir kelimenin zamanı (n. geçiş)
function Wd(id, w, n = 0, end = false) {
  const nw = w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  let k = 0;
  for (const x of (window.WORDS || [])) if (x.id === id && x.w.startsWith(nw)) { if (k++ === n) return end ? x.e : x.s; }
  return S(id);
}
// plan çapası: 'A01' cümle başı, 'A01@kelime' kelime, 'A01@kelime#1' ikinci geçiş, '+0.3' kaydırma (animatik/planlar.json ile aynı yazım)
function A(at) {
  const m = at.match(/^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$/);
  if (!m) return 0;
  return (m[2] ? Wd(m[1], m[2], +(m[3] || 0)) : S(m[1])) + (m[4] ? +m[4] : 0);
}
// plan çapası kimlikle: PA('P016') = planlar.json'daki 'at' (animatik/planlar.js); off saniye kaydırma
function PA(id, off = 0) { const p = (window.PLAN || {})[id]; if (!p) { console.log('plan yok: ' + id); return 0; } return A(p.at) + off; }
const SHOTS = [];
let SHOTS_SORTED = false;
// shot(başlangıç, çizim, {tr:{type,dur,end}, post:{...}, over, mb})
// tr.end: yumuşak geçiş çapada BİTER (önceki sessizlikte oynar; plan v2 kuralı): çekim dur kadar önce başlar
function shot(at, draw, o = {}) { if (o.tr && o.tr.end && o.tr.type !== 'cut') at -= o.tr.dur; SHOTS.push({ at, draw, ...o }); }
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
  if (!SHOTS_SORTED) { SHOTS.sort((a, b) => a.at - b.at); SHOTS_SORTED = true; }
  let i = 0;
  for (let k = 0; k < SHOTS.length; k++) if (SHOTS[k].at <= t) i = k;
  return i;
}
function drawShot(ctx, i, t) {
  const sh = SHOTS[i]; if (!sh) return;
  const end = (SHOTS[i + 1] ? SHOTS[i + 1].at : DUR);
  const st = { t, at: sh.at, lt: t - sh.at, d: end - sh.at, p: clamp((t - sh.at) / (end - sh.at)), end };
  ctx.save();
  sh.draw(ctx, st);
  ctx.restore();
}
function drawFilm(ctx, t) {
  const sc = new URLSearchParams(location.search).get('scene');
  // deneme sahneleri de filmdeki son işlemden geçer (doku, vinyet, gren): kurul son yüzeyi görür
  if (sc && typeof SCENES !== 'undefined' && SCENES[sc]) { SCENES[sc](ctx, t); POST = { tex: .85, vig: .85, grain: .055, ...(SCENES[sc].post || {}) }; post(ctx, t); return; }
  const i = shotAt(t), sh = SHOTS[i];
  const tr = sh.tr;
  if (tr && i > 0 && t < sh.at + tr.dur && tr.type !== 'cut') {
    const p = clamp((t - sh.at) / tr.dur);
    drawShot(ctx, i, t);
    baseT(bufAx); bufAx.globalAlpha = 1; bufAx.globalCompositeOperation = 'source-over';
    bufAx.clearRect(0, 0, W, H);
    drawShot(bufAx, i - 1, t);
    composite(ctx, bufA, tr, p);
  } else drawShot(ctx, i, t);
  POST = { tex: .85, vig: .85, grain: .055, ...(sh.post || {}) };
  post(ctx, t);
}
// Üst katman (yazılar, etiketler, kenar şeritleri): hareket bulanıklığı ortalamasından ve son işlemden sonra, kamera
// dönüşümü olmadan kare başına bir kez çizilir; sarsıntı ve dönüş yalnız resme uygulanır (telefonda okunurluk).
function drawOver(ctx, t) {
  const i = shotAt(t), sh = SHOTS[i]; if (!sh || !sh.over) return;
  const end = (SHOTS[i + 1] ? SHOTS[i + 1].at : DUR);
  const st = { t, at: sh.at, lt: t - sh.at, d: end - sh.at, p: clamp((t - sh.at) / (end - sh.at)), end };
  ctx.save(); baseT(ctx); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
  if (sh.tr && sh.tr.type !== 'cut' && st.lt < sh.tr.dur) ctx.globalAlpha = clamp(st.lt / sh.tr.dur);
  sh.over(ctx, st);
  ctx.restore();
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
  } else if (tr.type === 'wipe') {
    const x = lerp(-200, W + 200, E.io3(p)), dir = tr.dir || 1;
    const g = bufAx.createLinearGradient(x - 120, 0, x + 120, 0);
    g.addColorStop(0, dir > 0 ? 'rgba(0,0,0,0)' : '#000'); g.addColorStop(1, dir > 0 ? '#000' : 'rgba(0,0,0,0)');
    bufAx.save(); baseT(bufAx); bufAx.globalCompositeOperation = 'destination-in'; bufAx.fillStyle = g; bufAx.fillRect(0, 0, W, H); bufAx.restore();
    ctx.drawImage(buf, 0, 0);
  } else if (tr.type === 'negatif') {
    // katman değişimi (kırmızı figür ↔ siyah figür): eski kare önce negatifine döner (sır kile, kil sıra), sonra çözülür.
    // Değer haritası: koyu → kil, açık → siyah sır; ateş gibi çok açık noktalar korunur
    const q = clamp(p * 2), g = bufAx.getImageData(0, 0, DW, DH), d = g.data, k = E.io2(q);
    const cl = [201, 112, 63], ik = [23, 16, 12];
    for (let i = 0; i < d.length; i += 4) {
      const L = (d[i] * .2126 + d[i + 1] * .7152 + d[i + 2] * .0722) / 255;
      if (L > .86) continue;
      const u = clamp(L * 1.8);
      for (let c = 0; c < 3; c++) d[i + c] = lerp(d[i + c], lerp(cl[c], ik[c], u), k);
    }
    bufAx.putImageData(g, 0, 0);
    if (p >= .5) {
      const nm = noiseMask(), id = maskX.createImageData(480, 270), dd = id.data, soft = .08, th = lerp(-soft, 1 + soft, E.io2((p - .5) * 2));
      for (let j = 0; j < nm.length; j++) dd[j * 4 + 3] = clamp((nm[j] - th) / soft + .5) * 255;
      maskX.putImageData(id, 0, 0);
      bufAx.save(); baseT(bufAx); bufAx.globalCompositeOperation = 'destination-in'; bufAx.drawImage(maskC, 0, 0, W, H); bufAx.restore();
    }
    ctx.drawImage(buf, 0, 0);
  } else if (tr.type === 'sir') {
    // kırmızı figüre giriş: siyah sır kenarlardan içeri akar (ressam zemini boyar, figür kilde kalır).
    // Eski kare, kenardan merkeze ilerleyen gürültülü bir sır cephesinin arkasında kalır; cephe çizgisi koyu bant olarak görünür
    const nm = noiseMask(), id = maskX.createImageData(480, 270), d = id.data, soft = .06, th = lerp(-.1, 1.15, E.io2(p));
    for (let y = 0; y < 270; y++) for (let x = 0; x < 480; x++) {
      const k = y * 480 + x, dx = (x - 240) / 240, dy = (y - 135) / 135, edge = 1 - Math.max(Math.abs(dx), Math.abs(dy)) * .7 - Math.hypot(dx, dy) * .3;
      const v = edge * .75 + nm[k] * .25;
      d[k * 4 + 3] = clamp((v - th) / soft + .5) * 255;
    }
    maskX.putImageData(id, 0, 0);
    bufAx.save(); baseT(bufAx); bufAx.globalCompositeOperation = 'destination-in'; bufAx.drawImage(maskC, 0, 0, W, H); bufAx.restore();
    ctx.save(); ctx.globalAlpha = Math.sin(clamp(p) * PI) * .35; ctx.fillStyle = '#0E0907'; ctx.fillRect(0, 0, DW, DH); ctx.restore();
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
// Son işlem: doku + vinyet + gren. Çekimler kendi stilini window.POST ile ayarlar.
let POST = { tex: .85, vig: .85, grain: .055 };
function setPost(o) { POST = { tex: .85, vig: .85, grain: .055, ...o }; }
function post(ctx, t) {
  if (POST.tex > 0) applyTexture(ctx, POST.tex);
  if (POST.vig > 0) applyVignette(ctx, POST.vig);
  if (POST.grain > 0) applyGrain(ctx, t, POST.grain);
  if (POST.flicker) { ctx.save(); baseT(ctx); ctx.fillStyle = '#000'; ctx.globalAlpha = (noise1(t * 9, 3) * .5 + .5) * POST.flicker; ctx.fillRect(0, 0, W, H); ctx.restore(); }
}
// Kamera: dünya koordinatından ekrana (merkez cx,cy, yakınlık z, dönüş r); katman derinliği k ile paralaks
function cam(ctx, c, k = 1) {
  // c.x, c.y: ekran merkezine gelen dünya noktası; k: paralaks derinliği (0 sabit, 1 tam)
  const z = 1 + ((c.z ?? 1) - 1) * k;
  const cx = W / 2 + ((c.x ?? W / 2) - W / 2) * k, cy = H / 2 + ((c.y ?? H / 2) - H / 2) * k;
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
// Metin yardımcıları
// Shorts gibi kurgularda film içi yazılar kapatılabilir (?notext=1)
const NOTEXT = typeof location !== 'undefined' && new URLSearchParams(location.search).has('notext');
function txt(ctx, s, x, y, o = {}) {
  if (NOTEXT && !o.force) return;
  s = L(s);
  ctx.save();
  ctx.font = o.font || '600 48px Cinzel';
  ctx.textAlign = o.align || 'center'; ctx.textBaseline = o.base || 'middle';
  if (o.ls) ctx.letterSpacing = o.ls + 'px';
  // o.maxW: yazı bu genişliğe sığmazsa punto küçülür (çeviride uzayan etiketler)
  if (o.maxW) { const w = ctx.measureText(s).width; if (w > o.maxW) ctx.font = ctx.font.replace(/([\d.]+)px/, (m, n) => (n * o.maxW / w).toFixed(1) + 'px'); }
  ctx.globalAlpha *= o.a ?? 1;
  if (o.shadow) { ctx.shadowColor = o.shadow; ctx.shadowBlur = o.blur || 18; }
  if (o.stroke) { ctx.lineWidth = o.sw || 6; ctx.strokeStyle = o.stroke; ctx.lineJoin = 'round'; ctx.strokeText(s, x, y); }
  ctx.fillStyle = o.col || C.ink; ctx.fillText(s, x, y);
  ctx.restore();
}
// Harf harf beliren metin (p: 0..1)
function txtReveal(ctx, s, x, y, p, o = {}) {
  s = L(s);
  ctx.save(); ctx.font = o.font || '600 48px Cinzel'; if (o.ls) ctx.letterSpacing = o.ls + 'px';
  const wTot = ctx.measureText(s).width; ctx.restore();
  let cx = x - (o.align === 'left' ? 0 : wTot / 2);
  const n = s.length;
  for (let i = 0; i < n; i++) {
    const ch = s[i];
    ctx.save(); ctx.font = o.font || '600 48px Cinzel'; if (o.ls) ctx.letterSpacing = o.ls + 'px';
    const cw = ctx.measureText(ch).width; ctx.restore();
    const q = clamp(p * (n + 6) / 6 - i / 6);
    if (q > 0) txt(ctx, ch, cx + cw / 2, y + (1 - E.out3(q)) * (o.rise ?? 14), { ...o, align: 'center', a: (o.a ?? 1) * q });
    cx += cw;
  }
}
// Bölüm kartı
function chapterCard(ctx, num, title, lt, d = 3.6, o = {}) {
  if (NOTEXT) return;
  num = L(num); title = L(title);
  // vazo etiketi gibi kil levha: her zeminde okunur
  const a = ramp(lt, 0, .5) * (1 - ramp(lt, d - .6, d));
  if (a <= 0) return;
  ctx.save(); baseT(ctx);
  ctx.font = '700 50px Cinzel'; ctx.letterSpacing = '4px';
  const tw = ctx.measureText(title).width;
  const pw = Math.max(520, tw + 150), ph = 136, y = o.y ?? 150;
  const sc = lerp(.92, 1, E.out3(ramp(lt, 0, .6)));
  ctx.translate(o.x ?? W / 2, y);
  if (o.swing !== false) { const drop = 1 - E.out3(ramp(lt, 0, .55)); ctx.translate(0, -260 * drop); ctx.rotate(Math.exp(-lt * 3.2) * Math.sin(lt * 9) * .12); }
  ctx.scale(sc, sc);
  ctx.globalAlpha = a;
  ctx.fillStyle = 'rgba(10,5,3,.35)'; ctx.fillRect(-pw / 2 + 8, -ph / 2 + 10, pw, ph);
  ctx.fillStyle = '#E3B98C'; ctx.fillRect(-pw / 2, -ph / 2, pw, ph);
  ctx.lineWidth = 5; ctx.strokeStyle = C.ink; ctx.strokeRect(-pw / 2 + 8, -ph / 2 + 8, pw - 16, ph - 16);
  ctx.lineWidth = 1.6; ctx.strokeRect(-pw / 2 + 16, -ph / 2 + 16, pw - 32, ph - 32);
  for (const sg of [-1, 1]) { ctx.fillStyle = C.ink; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.arc(sg * (pw / 2 - 42), -18 + k * 18, 4, 0, TAU); ctx.fill(); } }
  txt(ctx, num, 0, -32, { font: '700 30px Cinzel', col: C.red, ls: 9 });
  const q = ramp(lt, .15, .9);
  txt(ctx, title, 0, 16, { font: '700 50px Cinzel', col: C.ink, ls: 4, a: q });
  ctx.restore();
}
// Karakter adı etiketi
function nameTag(ctx, name, sub, x, y, lt, d = 3.2, o = {}) {
  if (NOTEXT) return;
  const a = ramp(lt, 0, .5) * (1 - ramp(lt, d - .6, d));
  if (a <= 0) return;
  ctx.save(); baseT(ctx); ctx.globalAlpha = a;
  const col = o.col || C.white, al = o.align || 'left';
  txt(ctx, name, x, y, { font: '700 40px Cinzel', col, align: al, ls: 6, shadow: 'rgba(0,0,0,.6)', blur: 12 });
  if (sub) txt(ctx, sub, x + (al === 'left' ? 2 : 0), y + 44, { font: 'italic 600 40px "Cormorant Garamond"', col, align: al, shadow: 'rgba(0,0,0,.85)', blur: 10 });
  const lw = lerp(0, 120, E.out3(ramp(lt, .2, .9)));
  ctx.fillStyle = o.line || C.gold; ctx.fillRect(al === 'left' ? x : x - lw / 2, y + 22 + (sub ? 46 : 0) + 4, lw, 2);
  ctx.restore();
}
// Yazının arkasına yumuşak, metin genişliğinde eliptik koyu zemin (tam genişlik şerit yerine)
function softPanel(ctx, x, y, rx, ry, a = .7, col = '20,8,4') {
  ctx.save(); ctx.translate(x, y); ctx.scale(1, ry / rx);
  const g = ctx.createRadialGradient(0, 0, 0, 0, 0, rx);
  g.addColorStop(0, `rgba(${col},${a})`); g.addColorStop(.55, `rgba(${col},${a * .75})`); g.addColorStop(1, `rgba(${col},0)`);
  ctx.fillStyle = g; ctx.fillRect(-rx, -rx, 2 * rx, 2 * rx); ctx.restore();
}
// Alıntı tipografisi (satır kırma ile)
function quote(ctx, s, x, y, maxW, lt, o = {}) {
  s = L(s);
  const font = o.font || 'italic 500 56px "Cormorant Garamond"', lh = o.lh || 70;
  ctx.save(); ctx.font = font;
  // \n ile verilen satır kırma (çeviride dengeli satırlar) yoksa genişliğe göre kır
  const words = s.includes('\n') ? [] : s.split(' '), lines = s.includes('\n') ? s.split('\n') : []; let cur = '';
  for (const w of words) { const tt = cur ? cur + ' ' + w : w; if (ctx.measureText(tt).width > maxW && cur) { lines.push(cur); cur = w; } else cur = tt; }
  if (cur) lines.push(cur);
  ctx.restore();
  const y0 = y - (lines.length - 1) * lh / 2;
  if (o.band) { ctx.save(); ctx.font = font; const ww = Math.max(...lines.map(l => ctx.measureText(l).width)); ctx.restore(); softPanel(ctx, x, y, ww / 2 + 200, lines.length * lh / 2 + 70, .6 * ramp(lt, o.delay || 0, (o.delay || 0) + .8)); }
  lines.forEach((ln, i) => {
    const q = ramp(lt, (o.delay || 0) + i * (o.stagger ?? .35), (o.delay || 0) + i * (o.stagger ?? .35) + .9);
    txt(ctx, ln, x, y0 + i * lh + (1 - q) * 12, { font, col: o.col || C.white, a: q * (o.a ?? 1), shadow: o.shadow, blur: o.blur, align: o.align });
  });
}

// Figür yerel noktasını (kafa yerel koordinatı) ctx koordinatına çevir
function headPt(ctx, J, M, q) {
  const hp = add(J.neckT, rot(q, J.headA));
  const sp = M.transformPoint(new DOMPoint(hp[0], hp[1]));
  const r = ctx.getTransform().inverse().transformPoint(sp);
  return [r.x, r.y];
}
function jointPt(ctx, M, q) { const sp = M.transformPoint(new DOMPoint(q[0], q[1])); const r = ctx.getTransform().inverse().transformPoint(sp); return [r.x, r.y]; }
// Parıltı yıldızı
function sparkle(ctx, x, y, r, a = 1, col = '#FFF4D8') {
  if (a <= 0) return;
  ctx.save(); ctx.translate(x, y); ctx.globalAlpha *= a; ctx.fillStyle = col;
  ctx.beginPath(); ctx.moveTo(0, -r); ctx.quadraticCurveTo(r * .12, -r * .12, r, 0); ctx.quadraticCurveTo(r * .12, r * .12, 0, r); ctx.quadraticCurveTo(-r * .12, r * .12, -r, 0); ctx.quadraticCurveTo(-r * .12, -r * .12, 0, -r); ctx.fill();
  glow(ctx, 0, 0, r * 1.6, 'rgba(255,240,200,.5)');
  ctx.restore();
}
const FLAT = y => groundOf(() => y);
