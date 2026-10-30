// Beyaz zemin katmanı (Erhat'ın okuması): lekythos beyazı kâğıt, sepya çizgi, tek vurgu kırmızı.
// Yaşayan sayfa ilkeleri: elle yazılan satır, alıntı kartı, üstü çizme, mürekkep çizgisi, daire, mühür, daktilo.
'use strict';
const PW = { paper: '#EEE5D1', paperL: '#F6EFE0', paperD: '#DCCFB4', line: '#4A3423', lineL: 'rgba(74,52,35,.55)', red: '#9A3B25', ink: '#2B1D14' };
// beyaz zemin figür üslubu: dolgu kâğıt, kesik çizgiler sepya → çizgi resim
STY.lek = { fill: PW.paperL, cut: PW.line, red: PW.red, white: '#FFFDF6', line: PW.line };

// Sayfa zemini. o: {book: kitap sayfası (cilt gölgesi, sayfa numarası), num: 'xiv', rule: çizgili, glow}
function paperBG(ctx, t, o = {}) {
  ctx.fillStyle = PW.paper; ctx.fillRect(-200, -200, W + 400, H + 400);
  const g = ctx.createRadialGradient(W * .5, H * .42, 100, W * .5, H * .5, 1250);
  g.addColorStop(0, 'rgba(255,250,238,.55)'); g.addColorStop(1, 'rgba(150,120,85,.22)');
  ctx.fillStyle = g; ctx.fillRect(-200, -200, W + 400, H + 400);
  // kâğıt lifi: seyrek kısa sepya çizgiler (sabit tohum, kıpırdamaz)
  const r = rng(o.seed || 21);
  ctx.strokeStyle = 'rgba(110,80,50,.07)'; ctx.lineWidth = 1;
  for (let i = 0; i < 420; i++) { const x = r() * W, y = r() * H, a = r() * PI, l = 6 + r() * 18; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l); ctx.stroke(); }
  if (o.rule) { ctx.strokeStyle = 'rgba(120,90,60,.10)'; ctx.lineWidth = 1.2; for (let y = 160; y < H - 60; y += 64) { ctx.beginPath(); ctx.moveTo(140, y); ctx.lineTo(W - 140, y); ctx.stroke(); } }
  if (o.book) {
    // cilt gölgesi solda, sayfa kenarı sağda
    const gg = ctx.createLinearGradient(0, 0, 220, 0);
    gg.addColorStop(0, 'rgba(70,45,25,.38)'); gg.addColorStop(1, 'rgba(70,45,25,0)');
    ctx.fillStyle = gg; ctx.fillRect(-200, -200, 420, H + 400);
    ctx.strokeStyle = 'rgba(120,90,60,.25)'; ctx.lineWidth = 1;
    for (let k = 0; k < 5; k++) { ctx.beginPath(); ctx.moveTo(W - 26 + k * 4, -10); ctx.lineTo(W - 26 + k * 4, H + 10); ctx.stroke(); }
  }
  if (o.num) txt(ctx, '— ' + o.num + ' —', W / 2, H - 46, { font: 'italic 500 30px "Cormorant Garamond"', col: PW.lineL, force: true });
}

// Elle yazılan satır: soldan sağa açılır, ucunda kalem ucu. p: 0..1
function penLine(ctx, s, x, y, p, o = {}) {
  if (p <= 0 || (NOTEXT && !o.force)) return;
  s = L(s);
  const font = o.font || 'italic 500 54px "Cormorant Garamond"';
  ctx.save(); ctx.font = font; if (o.ls) ctx.letterSpacing = o.ls + 'px';
  const w = ctx.measureText(s).width, al = o.align || 'center';
  const x0 = al === 'left' ? x : al === 'right' ? x - w : x - w / 2, fs = +font.match(/([\d.]+)px/)[1];
  const xe = x0 + w * clamp(p);
  ctx.beginPath(); ctx.rect(x0 - 20, y - fs * 1.2, xe - x0 + 20, fs * 2.4); ctx.clip();
  ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.globalAlpha *= o.a ?? 1;
  ctx.fillStyle = o.col || PW.ink; ctx.fillText(s, x0, y);
  ctx.restore();
  if (p < 1 && o.nib !== false) { ctx.save(); ctx.globalAlpha *= (o.a ?? 1) * .8; ctx.fillStyle = o.col || PW.ink; ctx.beginPath(); ctx.arc(xe + 4, y + fs * .28 + Math.sin(p * 90) * 3, 3.2, 0, TAU); ctx.fill(); ctx.restore(); }
  return w;
}
// Çok satırlı paragraf: satırlar sırayla yazılır (dur: toplam süre). Satır kırma maxW'ye göre.
function penPara(ctx, s, x, y, maxW, lt, dur, o = {}) {
  const font = o.font || 'italic 500 50px "Cormorant Garamond"', lh = o.lh || 66;
  const lines = wrapLines(ctx, L(s), font, maxW);
  const tot = lines.reduce((a, l) => a + l.length, 0); let acc = 0;
  lines.forEach((ln, i) => {
    const a = acc / tot, b = (acc + ln.length) / tot; acc += ln.length;
    penLine(ctx, ln, x, y + i * lh, inv(a * dur, b * dur, lt), { ...o, font });
  });
  return lines.length * lh;
}
function wrapLines(ctx, s, font, maxW) {
  if (s.includes('\n')) return s.split('\n');
  ctx.save(); ctx.font = font;
  const out = []; let cur = '';
  for (const w of s.split(' ')) { const tt = cur ? cur + ' ' + w : w; if (ctx.measureText(tt).width > maxW && cur) { out.push(cur); cur = w; } else cur = tt; }
  if (cur) out.push(cur);
  ctx.restore(); return out;
}

// Alıntı kartı: büyük tırnaklar kırmızı, metin satır satır mürekkep gibi belirir, altında kaynak.
// src: 'A. Erhat, önsöz, s. xiv'. Üst 2/3'e yerleştir (alt üçte bir altyazının).
function quoteCard(ctx, q, src, x, y, maxW, lt, o = {}) {
  if (NOTEXT && !o.force) return;
  const font = o.font || 'italic 500 62px "Cormorant Garamond"', lh = o.lh || 78;
  const lines = wrapLines(ctx, L(q), font, maxW), n = lines.length, y0 = y - (n - 1) * lh / 2, d = o.delay || 0;
  const a0 = ramp(lt, d, d + .5) * (o.a ?? 1);
  if (a0 <= 0) return;
  ctx.save(); ctx.globalAlpha *= a0;
  ctx.font = '600 150px "Cormorant Garamond"'; ctx.fillStyle = PW.red; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.save(); ctx.font = font; const ww = Math.max(...lines.map(l => ctx.measureText(l).width)); ctx.restore();
  ctx.fillText('“', x - ww / 2 - 46, y0 + 6);
  ctx.restore();
  lines.forEach((ln, i) => {
    const t0 = d + .15 + i * (o.stagger ?? .45);
    const k = ramp(lt, t0, t0 + .9, E.out2);
    if (k <= 0) return;
    ctx.save(); ctx.globalAlpha *= (o.a ?? 1);
    // mürekkep yayılması: önce bulanık ve açık, sonra keskin
    ctx.filter = k < 1 ? `blur(${((1 - k) * 6).toFixed(1)}px)` : 'none';
    txt(ctx, ln, x, y0 + i * lh, { font, col: o.col || PW.ink, a: k });
    ctx.restore();
  });
  if (src) {
    const k = ramp(lt, d + .3 + n * .45, d + 1.1 + n * .45);
    const ys = y0 + (n - 1) * lh + lh * .95;
    ctx.save(); ctx.globalAlpha *= (o.a ?? 1) * k;
    ctx.fillStyle = PW.red; ctx.fillRect(x - 60 * E.out3(k), ys - 30, 120 * E.out3(k), 2.4);
    txt(ctx, src, x, ys + 8, { font: '600 30px Cinzel', col: PW.line, ls: 3, force: o.force });
    ctx.restore();
  }
}

// Mürekkep çizgisi: nokta dizisi boyunca p oranında çizilir (el çizimi titremesiyle). pts: [[x,y],...]
function inkPoly(ctx, pts, p, o = {}) {
  if (p <= 0 || pts.length < 2) return;
  const L = [0]; for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + len(sub(pts[i], pts[i - 1])));
  const end = L[L.length - 1] * clamp(p), j = o.jit ?? 1.2, sd = o.seed || 3;
  ctx.save(); ctx.strokeStyle = o.col || PW.line; ctx.lineWidth = o.w || 4; ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.globalAlpha *= o.a ?? 1;
  ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
  for (let i = 1; i < pts.length && L[i - 1] < end; i++) {
    const u = L[i] <= end ? 1 : (end - L[i - 1]) / (L[i] - L[i - 1]);
    const q = add(pts[i - 1], scl(sub(pts[i], pts[i - 1]), u));
    ctx.lineTo(q[0] + noise1(L[i] * .05, sd) * j, q[1] + noise1(L[i] * .05, sd + 9) * j);
  }
  ctx.stroke(); ctx.restore();
}
// Bir yolu örnekleyip noktaya çevirir: ctx yolu yerine fonksiyon f(u)→[x,y]
function sampleF(f, n = 80) { const out = []; for (let i = 0; i <= n; i++) out.push(f(i / n)); return out; }
// El çizimi daire/elips (bir şeyi işaretlemek için), hafif taşarak kapanır
function circleMark(ctx, x, y, rx, ry, p, o = {}) {
  const a0 = o.a0 ?? -2.2, pts = sampleF(u => { const a = a0 + u * TAU * 1.08, w = 1 + .04 * Math.sin(u * 9 + 1); return [x + Math.cos(a) * rx * w, y + Math.sin(a) * ry * w]; }, 90);
  inkPoly(ctx, pts, p, { col: PW.red, w: 5, ...o });
}
// Üstünü çizme: dalgalı tek çizgi
function strike(ctx, x0, y0, x1, y1, p, o = {}) {
  const pts = sampleF(u => [lerp(x0, x1, u), lerp(y0, y1, u) + Math.sin(u * 14) * (o.wave ?? 4)], 40);
  inkPoly(ctx, pts, p, { col: PW.red, w: 6, ...o });
}
// Mühür: çerçeveli büyük harfler, çarparak iner (lt: mührün vurduğu andan beri geçen süre)
function stamp(ctx, s, x, y, lt, o = {}) {
  if (lt < -.25 || (NOTEXT && !o.force)) return;
  const k = ramp(lt, -.25, 0, E.in2), sc = lerp(1.8, 1, k), a = (o.a ?? .85) * k;
  ctx.save(); ctx.translate(x, y); ctx.rotate(o.rot ?? -.08); ctx.scale(sc, sc); ctx.globalAlpha *= a;
  ctx.font = o.font || '700 74px Cinzel'; ctx.letterSpacing = '8px';
  const w = ctx.measureText(L(s)).width + 60, h = (o.h || 112);
  ctx.strokeStyle = o.col || PW.red; ctx.lineWidth = 6; ctx.strokeRect(-w / 2, -h / 2, w, h);
  ctx.lineWidth = 2; ctx.strokeRect(-w / 2 + 10, -h / 2 + 10, w - 20, h - 20);
  ctx.fillStyle = o.col || PW.red; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(L(s), 0, 4);
  // aşınmış mürekkep: rastgele boşluklar
  ctx.globalCompositeOperation = 'destination-out'; const r = rng(o.seed || 4);
  for (let i = 0; i < 70; i++) { ctx.beginPath(); ctx.arc((r() - .5) * w, (r() - .5) * h, 1 + r() * 3.5, 0, TAU); ctx.fill(); }
  ctx.restore();
}
// Daktilo: harf harf, imleçle (Courier Prime). p: 0..1
function typed(ctx, s, x, y, p, o = {}) {
  if (NOTEXT && !o.force) return;
  s = L(s); const n = Math.floor(s.length * clamp(p)), font = o.font || '400 46px "Courier Prime"';
  ctx.save(); ctx.font = font; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillStyle = o.col || PW.ink;
  const w = ctx.measureText(s).width, x0 = o.align === 'left' ? x : x - w / 2;
  ctx.fillText(s.slice(0, n), x0, y);
  const cw = ctx.measureText(s.slice(0, n)).width;
  if (o.cursor !== false && (p < 1 || Math.floor((window.FIG_T || 0) * 2) % 2 === 0)) ctx.fillRect(x0 + cw + 3, y - 22, 3, 44);
  ctx.restore();
}
// Sayfa kenar şeridi: figürlerin üstünde ve altında ince çift çizgi (lekythos omzundaki gibi)
function marginBand(ctx, x0, x1, y0, y1, p = 1, o = {}) {
  const col = o.col || PW.line;
  inkPoly(ctx, [[x0, y0], [x1, y0]], p, { col, w: 2.4, jit: .5 });
  inkPoly(ctx, [[x0, y0 + 8], [x1, y0 + 8]], p, { col, w: 1.2, jit: .5 });
  inkPoly(ctx, [[x1, y1], [x0, y1]], p, { col, w: 2.4, jit: .5 });
  inkPoly(ctx, [[x1, y1 - 8], [x0, y1 - 8]], p, { col, w: 1.2, jit: .5 });
}

// Erhat'ın kenar şeridi: tek cümlelik Erhat yorumu, katman değiştirmeden o anki karenin üstüne inen krem şerit.
// Solda "ERHAT · s. x" künyesi, ortada 2–5 kelimelik anahtar söz (el yazısı), sağda sepya simge çizimi (icon(ctx, p)).
// Üst 2/3'te kalır (altyazı bandına inmez). lt: şeridin başından beri geçen süre, d: kalış süresi.
function erhatStrip(ctx, lt, d, words, page, o = {}) {
  if (lt < 0 || lt > d + .6) return;
  const k = E.out3(ramp(lt, 0, .55)) * (1 - E.in2(ramp(lt, d, d + .6))), y0 = 40, h = o.h || 190;
  ctx.save(); baseT(ctx);
  ctx.translate(0, -h * (1 - k));
  ctx.fillStyle = 'rgba(20,10,5,.35)'; ctx.fillRect(0, y0 + 6, W, h);
  ctx.fillStyle = PW.paper; ctx.fillRect(0, y0, W, h);
  const g = ctx.createLinearGradient(0, y0, 0, y0 + h); g.addColorStop(0, 'rgba(255,250,238,.5)'); g.addColorStop(1, 'rgba(150,120,85,.15)');
  ctx.fillStyle = g; ctx.fillRect(0, y0, W, h);
  ctx.strokeStyle = PW.line; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(0, y0 + h - 4); ctx.lineTo(W, y0 + h - 4); ctx.stroke();
  ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(0, y0 + h - 12); ctx.lineTo(W, y0 + h - 12); ctx.stroke();
  txt(ctx, 'ERHAT', 80, y0 + h / 2 - 16, { font: '700 34px Cinzel', col: PW.red, align: 'left', ls: 6, force: o.force });
  if (page) txt(ctx, 'önsöz · s. ' + page, 82, y0 + h / 2 + 26, { font: 'italic 600 30px "Cormorant Garamond"', col: PW.line, align: 'left', force: o.force });
  if (words) penLine(ctx, words, o.wx ?? W / 2 + 40, y0 + h / 2, ramp(lt, .35, .35 + Math.min(1.6, words.length * .06)), { font: o.font || 'italic 600 62px "Cormorant Garamond"', col: PW.ink, force: o.force });
  if (o.icon) { ctx.save(); ctx.translate(W - 190, y0 + h / 2); o.icon(ctx, ramp(lt, .6, 1.6), lt); ctx.restore(); }
  ctx.restore();
}
// Görünür söz: Prometheus'un sözleri ağzından akan kil renkli harfler (ateşe dönük kenar ışığı), havada kalır.
// pts: harflerin dizileceği yol f(u)→[x,y]; p: akış oranı; o.fade: silinme (P147'de yarım kalıp silinir)
function speechFlow(ctx, s, f, p, o = {}) {
  if (NOTEXT && !o.force) return;
  s = L(s); const n = s.length, font = o.font || '600 46px Cinzel';
  ctx.save(); ctx.font = font; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  const ws = [...s].map(ch => ctx.measureText(ch).width), tot = ws.reduce((a, b) => a + b, 0);
  // sola akan yol (ağız sağda): harfler yine soldan sağa okunur; her harf ağızdan çıkıp yerine uçar
  const [mx, my] = f(0), left = f(1)[0] < mx, g = left ? u => f(1 - u) : f;
  let acc = 0;
  for (let i = 0; i < n; i++) {
    const u = (acc + ws[i] / 2) / tot; acc += ws[i];
    const q = clamp(p * (n + 4) / 4 - i / 4); if (q <= 0) continue;
    const a = q * (1 - (o.fade ? clamp(o.fade * (n + 4) / 4 - (n - i) / 4) : 0)); if (a <= 0) continue;
    let [x, y] = g(u); const [x2, y2] = g(Math.min(1, u + .01)), ang = Math.atan2(y2 - y, x2 - x);
    if (left) { const k = E.out3(q); x = lerp(mx, x, k); y = lerp(my, y, k); } else y -= (1 - E.out3(q)) * 18;
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang * (o.follow ?? .6)); ctx.globalAlpha *= a;
    ctx.shadowColor = o.glow || 'rgba(255,170,80,.55)'; ctx.shadowBlur = 14;
    ctx.fillStyle = o.col || PC.clayRL; ctx.fillText(s[i], 0, 0);
    ctx.restore();
  }
  ctx.restore();
}
// Güç'ün (Kratos) sözü: kil levhaya kazınmış, katı ve donmuş harfler
function carvedTablet(ctx, lines, x, y, w, lt, o = {}) {
  if (NOTEXT && !o.force) return;
  const k = E.outBack(ramp(lt, 0, .5, E.lin)), lh = o.lh || 64, h = lines.length * lh + 70;
  ctx.save(); ctx.translate(x, y); ctx.scale(k, k); ctx.rotate(o.rot ?? -.02);
  ctx.fillStyle = 'rgba(0,0,0,.4)'; ctx.fillRect(-w / 2 + 10, -h / 2 + 12, w, h);
  ctx.fillStyle = '#B8693F'; ctx.fillRect(-w / 2, -h / 2, w, h);
  ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.strokeRect(-w / 2, -h / 2, w, h);
  lines.forEach((ln, i) => {
    const q = ramp(lt, .3 + i * .5, .9 + i * .5);
    txt(ctx, ln, 0, -h / 2 + 35 + lh * (i + .5), { font: o.font || '700 44px Cinzel', col: 'rgba(40,20,10,.92)', a: q, ls: 3, force: o.force });
    txt(ctx, ln, 1.5, -h / 2 + 36.5 + lh * (i + .5), { font: o.font || '700 44px Cinzel', col: 'rgba(255,220,180,.25)', a: q, ls: 3, force: o.force });
  });
  ctx.restore();
}

// Yaşayan sayfa yolculuğu: Erhat bloğu tek ve uzun bir sayfadır (açık kitap). Plan sınırları kameranın duraklarıdır;
// kesme yoktur. stations: [{at, x, y?, z?, draw(ctx, lt, t)}], her durağın içeriği sayfa koordinatında x çevresine çizilir.
// Kamera bir durağa, o durağın 'at' anından .9 sn önce kaymaya başlar. o: {num: sayfa no, w: sayfa genişliği}
function pageJourney(ctx, t, stations, o = {}) {
  let i = 0; for (let k = 0; k < stations.length; k++) if (t >= stations[k].at - .9) i = k;
  const a = stations[Math.max(0, i - 1)], b = stations[i];
  const u = i === 0 ? 1 : E.io3(ramp(t, b.at - .9, b.at + .1, E.lin));
  const sx = s => s.x, sy = s => s.y ?? H / 2, sz = s => s.z ?? 1;
  const drift = (t - b.at) * 4;
  const c = { x: lerp(sx(a), sx(b), u) + drift, y: lerp(sy(a), sy(b), u), z: lerp(sz(a), sz(b), u) * (1 + .004 * Math.sin(t * .7)) };
  ctx.save(); cam(ctx, c, 1);
  // sayfa zemini: bütün durakların altında süren tek kâğıt; kâğıt hafifçe nefes alır
  ctx.save(); ctx.translate(c.x - W / 2, 0); paperBG(ctx, t, { book: false, seed: 21 }); ctx.restore();
  for (const s of stations) if (Math.abs(s.x - c.x) < W * 1.4) { ctx.save(); s.draw(ctx, t - s.at, t); ctx.restore(); }
  ctx.restore();
  if (o.num) txt(ctx, '— ' + o.num + ' —', W / 2, H - 46, { font: 'italic 500 30px "Cormorant Garamond"', col: PW.lineL, force: true });
  return c;
}

// Tutarlı Erhat köşe etiketi (sol üst, YouTube üst katmanının altında): "ERHAT · s. x" ya da kısa bir künye
function erhatTag(ctx, lt, s, o = {}) {
  if (NOTEXT && !o.force) return;
  const a = ramp(lt, o.delay || .2, (o.delay || .2) + .5) * (o.d ? 1 - ramp(lt, o.d - .5, o.d) : 1);
  if (a <= 0) return;
  ctx.save(); ctx.globalAlpha *= a;
  ctx.font = '700 40px Cinzel'; ctx.letterSpacing = '4px'; const w = ctx.measureText(L(s)).width;
  ctx.fillStyle = o.bg || 'rgba(238,229,209,.92)'; ctx.fillRect(80, 66, w + 44, 64);
  ctx.strokeStyle = PW.red; ctx.lineWidth = 3; ctx.strokeRect(80, 66, w + 44, 64);
  txt(ctx, s, 102, 99, { font: '700 40px Cinzel', col: o.col || PW.ink, align: 'left', ls: 4, force: o.force });
  ctx.restore();
}
