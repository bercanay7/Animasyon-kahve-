// Çekim sistemi (Milton): çekimler anlatım işaretlerine bağlanır; geçişler, kâğıt dokusu ve ekran yazıları burada.
// Her çekim bir gravür levhasıdır: draw(ctx, st) içinde levha(ctx, cam, fn) çağrılır; fn dünya koordinatında çizer.
'use strict';
const S = id => (window.CUES && CUES[id] ? CUES[id].s : 0);          // cümle başlangıcı
const Se = id => (window.CUES && CUES[id] ? CUES[id].e : 0);         // cümle bitişi
// cümle içindeki bir kelimenin zamanı (n. geçiş)
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
// plan kimliğiyle çapa: PA('P016') = planlar.json'daki 'at'; off saniye kaydırma
function PA(id, off = 0) { const p = (window.PLAN || {})[id]; if (!p) { console.log('plan yok: ' + id); return 0; } return A(p.at) + off; }

const SHOTS = [];
let SHOTS_SORTED = false;
// shot(başlangıç, çizim, {tr: {type: 'cut'|'fade'|'black'|'paper', dur, end}, over, mb, id})
// tr.end: yumuşak geçiş çapada BİTER (önceki sessizlikte oynar); çekim dur kadar önce başlar
function shot(at, draw, o = {}) { if (o.tr && o.tr.end && o.tr.type !== 'cut') at -= o.tr.dur; SHOTS.push({ at, draw, ...o }); SHOTS_SORTED = false; }
// plan kimliğiyle çekim: plan('P016', draw, o)
function plan(id, draw, o = {}) { shot(PA(id, o.off || 0), draw, { id, ...o }); }
function shotAt(t) {
  if (!SHOTS_SORTED) { SHOTS.sort((a, b) => a.at - b.at); SHOTS_SORTED = true; }
  let i = 0;
  for (let k = 0; k < SHOTS.length; k++) if (SHOTS[k].at <= t) i = k;
  return i;
}
function shotState(i, t) {
  const sh = SHOTS[i], end = (SHOTS[i + 1] ? SHOTS[i + 1].at : (window.DUR || sh.at + 10));
  return { t, at: sh.at, lt: t - sh.at, d: end - sh.at, p: clamp((t - sh.at) / (end - sh.at)), end };
}
// Levha: gravür motorunu açar, fn'yi çizer, basar. cam: {cx, cy, z} (ekran merkezine gelen dünya noktası ve yakınlık) ya da null.
// bg: [zemin tonu, zemin tarama açısı, üslup kimliği]
function camOf(c) { if (!c) return null; const z = c.z ?? 1, cx = c.cx ?? W / 2, cy = c.cy ?? H / 2; return { x: cx - W / 2 / z, y: cy - H / 2 / z, s: z }; }
function levha(ctx, cam, fn, bg = [.04, 0, 1]) {
  GR.begin(bg[0], bg[1], bg[2], camOf(cam));
  fn();
  GR.engrave(ctx);
}
// kamera hareketi: iki durum arasında yumuşak geçiş (p: 0..1)
function camLerp(a, b, p, ease = E.io2) { const u = ease(clamp(p)); return { cx: lerp(a.cx ?? W / 2, b.cx ?? W / 2, u), cy: lerp(a.cy ?? H / 2, b.cy ?? H / 2, u), z: lerp(a.z ?? 1, b.z ?? 1, u) }; }

const bufA = makeCanvas(DW, DH), bufAx = bufA.getContext('2d');
function drawShot(ctx, i, t) { const sh = SHOTS[i]; if (!sh) return; ctx.save(); sh.draw(ctx, shotState(i, t)); ctx.restore(); }
const PAPER_CSS = `rgb(${GR.PAPER})`, INK_CSS = `rgb(${GR.INK})`;
function drawFilm(ctx, t) {
  const sc = new URLSearchParams(location.search).get('scene');
  if (sc && typeof SCENES !== 'undefined' && SCENES[sc]) { SCENES[sc](ctx, t); post(ctx, t); return; }
  if (!SHOTS.length) return;
  const i = shotAt(t), sh = SHOTS[i], tr = sh.tr;
  if (tr && i > 0 && t < sh.at + tr.dur && tr.type !== 'cut') {
    const p = clamp((t - sh.at) / tr.dur);
    if (tr.type === 'fade') {
      drawShot(bufAx, i - 1, t); drawShot(ctx, i, t);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1 - E.sine(p); ctx.drawImage(bufA, 0, 0); ctx.restore();
    } else { // 'black' ya da 'paper': önce eski levha kapanır, sonra yenisi açılır
      const col = tr.type === 'paper' ? PAPER_CSS : INK_CSS;
      drawShot(ctx, p < .5 ? i - 1 : i, t);
      ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = col; ctx.globalAlpha = p < .5 ? E.sine(p * 2) : 1 - E.sine((p - .5) * 2); ctx.fillRect(0, 0, DW, DH); ctx.restore();
    }
  } else drawShot(ctx, i, t);
  post(ctx, t);
}
// Son işlem: kâğıt dokusu + vinyet (baskı yüzeyi). Çekimler bunu kendileri uygulamaz.
function post(ctx, t) { applyPaper(ctx, .8); applyVignette(ctx, .45); }

// Üst katman (ekran yazıları): baskıdan sonra, kamera dönüşümü olmadan çizilir (telefonda okunurluk).
function drawOver(ctx, t) {
  if (!SHOTS.length) return;
  const i = shotAt(t), sh = SHOTS[i]; if (!sh) return;
  const pv = i > 0 ? SHOTS[i - 1] : null;
  if (pv && pv.over && sh.tr && sh.tr.type !== 'cut' && t - sh.at < sh.tr.dur) { // çıkan planın yazısı söner
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

// ── Ekran yazıları ──
// Yazı dili: başlık ve etiketler Cinzel (büyük harf, aralıklı); alıntılar Cormorant Garamond italik.
// Koyu levhada kâğıt rengi harf, açık levhada mürekkep rengi harf; arkasında gerekirse yumuşak koyu zemin.
// Telefon kuralı: alıntı ≥ 64 px, etiket ≥ 40 px; yazı x 120–1800, y 90–880 (alt bant altyazıya ayrılır).
const NOTEXT = typeof location !== 'undefined' && new URLSearchParams(location.search).has('notext');
const FONT = { baslik: (px, w = 700) => `${w} ${px}px Cinzel`, alinti: (px, w = 600) => `italic ${w} ${px}px "Cormorant Garamond"`, metin: (px, w = 600) => `${w} ${px}px "Cormorant Garamond"` };
function softPanel(ctx, x, y, rx, ry, a = .78) {
  const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
  g.addColorStop(0, `rgba(${GR.INK},${a})`); g.addColorStop(.62, `rgba(${GR.INK},${a * .9})`); g.addColorStop(1, `rgba(${GR.INK},0)`);
  ctx.save(); ctx.translate(x, y); ctx.scale(rx, ry); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 1, 0, TAU); ctx.fill(); ctx.restore();
}
// satır kırma: en çok maxW genişliğinde satırlar
function wrapLines(ctx, s, maxW) {
  const out = []; for (const par of String(s).split('\n')) { let ln = ''; for (const w of par.split(' ')) { const tt = ln ? ln + ' ' + w : w; if (ctx.measureText(tt).width > maxW && ln) { out.push(ln); ln = w; } else ln = tt; } out.push(ln); }
  return out;
}
// txt(ctx, s, x, y, {font, px, col, a, align, ls (harf aralığı px), panel})
function txt(ctx, s, x, y, o = {}) {
  if (NOTEXT || !s) return;
  ctx.save(); ctx.font = o.font || FONT.baslik(o.px || 48); ctx.textAlign = o.align || 'center'; ctx.textBaseline = 'middle';
  if (o.ls) ctx.letterSpacing = o.ls + 'px';
  ctx.globalAlpha *= clamp(o.a ?? 1);
  if (o.panel) { const wd = ctx.measureText(s).width; softPanel(ctx, x, y, wd * .5 + (o.px || 48) * 1.6, (o.px || 48) * 1.5, o.panel === true ? .78 : o.panel); }
  ctx.fillStyle = o.col || PAPER_CSS; ctx.fillText(s, x, y);
  ctx.restore();
}
// Alıntı: satır satır beliren italik metin. lt: çekim içi zaman; o: {px, maxW, col, t0 (başlama), per (satır başına sn), panel, kaynak}
function quote(ctx, s, x, y, lt, o = {}) {
  if (NOTEXT || !s) return;
  const px = o.px || 68, lh = px * 1.22;
  ctx.save(); ctx.font = FONT.alinti(px); const L = wrapLines(ctx, s, o.maxW || 1240), y0 = y - (L.length - 1) * lh / 2;
  const t0 = o.t0 || 0, per = o.per ?? .5, aAll = clamp((lt - t0) / .5);
  const kpx = Math.max(40, Math.round(px * .42)), kEk = o.kaynak ? kpx + 34 : 0;   // künye: telefon kuralı ≥ 40 px; panel künyeyi de kapsar
  if (o.panel !== false && aAll > 0) { let wd = 0; for (const l of L) wd = Math.max(wd, ctx.measureText(l).width); ctx.globalAlpha = aAll; softPanel(ctx, x, y + kEk / 2, wd * .5 + px * 1.8, L.length * lh * .5 + px * 1.2 + kEk / 2, o.panel ?? .8); }
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = o.col || PAPER_CSS;
  L.forEach((l, i) => { const a = clamp((lt - t0 - i * per) / .6); if (a <= 0) return; ctx.globalAlpha = E.sine(a); ctx.fillText(l, x, y0 + i * lh + (1 - E.out3(a)) * 10); });
  if (o.kaynak) { const a = clamp((lt - t0 - L.length * per) / .6); ctx.globalAlpha = E.sine(a); ctx.font = FONT.baslik(kpx, 600); ctx.letterSpacing = '3px'; ctx.fillText(o.kaynak, x, y0 + (L.length - 1) * lh + px * .62 + 30 + kpx / 2); }
  ctx.restore();
}
// Bölüm kartı: ince çizgi + büyük harfli başlık + altında bölümün merak sorusu. lt: çekim içi zaman, d: süre
function chapterCard(ctx, title, soru, lt, d = 3.6, o = {}) {
  if (NOTEXT) return;
  const a = clamp(lt / .6) * clamp((d - lt) / .6); if (a <= 0) return;
  const x = o.x ?? W / 2, y = o.y ?? 430, px = o.px || 92;
  ctx.save(); ctx.globalAlpha = E.sine(a);
  softPanel(ctx, x, y + 40, 900, 300, .9);
  const u = E.out3(clamp(lt / 1.1)), lw = 250 * u;
  ctx.strokeStyle = PAPER_CSS; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x - lw, y - px * .82); ctx.lineTo(x + lw, y - px * .82); ctx.stroke();
  txt(ctx, title, x, y, { px, ls: 10 });
  if (soru) { const sp = o.soruPx || 64; ctx.font = FONT.alinti(sp); ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillStyle = PAPER_CSS; ctx.globalAlpha *= clamp((lt - .5) / .6); wrapLines(ctx, soru, o.soruW || Math.min(1400, 2 * (Math.min(x, W - x) - 110))).forEach((l, i) => ctx.fillText(l, x, y + px * 1.02 + i * sp * 1.18)); }   // soru ≥ 64 px (telefon)
  ctx.restore();
}
// Etiket: küçük büyük harfli ad (kişi, yer, yıl). lt ile belirir, d sonunda söner.
function etiket(ctx, s, x, y, lt, d = 4, o = {}) {
  if (NOTEXT || !s) return;
  const a = clamp(lt / .5) * clamp((d - lt) / .5); if (a <= 0) return;
  txt(ctx, s, x, y, { px: o.px || 44, ls: o.ls ?? 6, a: E.sine(a), panel: o.panel ?? .7, col: o.col, align: o.align, font: FONT.baslik(o.px || 44, 600) });
}
