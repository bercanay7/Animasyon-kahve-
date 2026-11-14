// Çekim sistemi (İkaros): Milton'ın çekim sistemi (S, Wd, A, PA, plan) + serigrafi baskısı.
// Her çekim bir baskıdır: draw(ctx, st) içinde baski(ctx, st, cam, fn) çağrılır; fn(pr) dünya koordinatında mürekkep basar.
// Üslup yasası (cinecode silkscreen-poster): opak düz mürekkep, gradyan yok (bantlar), çizgi yok, her katman 1–3 px kayık,
// kâğıt bir renktir, tek vurgu mürekkebi (güneş). Saydamlıkla geçiş yok: kesme, mürekkep çekişi (pull) ya da yeniden mürekkepleme.
'use strict';
const S = id => (window.CUES && CUES[id] ? CUES[id].s : 0);
const Se = id => (window.CUES && CUES[id] ? CUES[id].e : 0);
function Wd(id, w, n = 0, end = false) {
  const nw = w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  let k = 0;
  for (const x of (window.WORDS || [])) if (x.id === id && x.w.startsWith(nw)) { if (k++ === n) return end ? x.e : x.s; }
  return S(id);
}
function A(at) {
  if (typeof at === 'number') return at;
  const m = at.match(/^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$/);
  if (!m) return 0;
  return (m[2] ? Wd(m[1], m[2], +(m[3] || 0)) : S(m[1])) + (m[4] ? +m[4] : 0);
}
function PA(id, off = 0) { const p = (window.PLAN || {})[id]; if (!p) { console.log('plan yok: ' + id); return 0; } return A(p.at) + off; }

// ── Paletler: rol → mürekkep. sky1 açık gök, sky2 koyu gök/bant, far uzak, mid orta, near en koyu (yakın, bilgi bandı),
// acc tek vurgu (güneş), lit ışıklı yüz, paper kâğıt. Günün saati = hikâyenin saati.
const PAL = {
  SAFAK: { paper: '#F3E6CC', sky1: '#F6CD98', sky2: '#EE9A73', far: '#9A7FA8', mid: '#3E7079', near: '#1E3B3F', acc: '#FBE6B4', lit: '#F2B27A' },
  OGLE:  { paper: '#F4ECD8', sky1: '#E8F0F2', sky2: '#7FB3C8', far: '#D9C7A3', mid: '#2F6E8E', near: '#173247', acc: '#F7E3A1', lit: '#E9C98C' },
  BATIS: { paper: '#F1E2C6', sky1: '#F4B25E', sky2: '#D9583B', far: '#8C3B4E', mid: '#4A2D52', near: '#1F1630', acc: '#FCE39A', lit: '#F08C4A' },
  ALACA: { paper: '#EDE3D0', sky1: '#B8C9D9', sky2: '#8B9BB0', far: '#6A6F8E', mid: '#4A5D78', near: '#1F2A3C', acc: '#F2B134', lit: '#C9B79A' },
  BRUEGEL: { paper: '#F2EAD3', sky1: '#EEE6B8', sky2: '#C9D3A0', far: '#8FB0A4', mid: '#4F7A5A', near: '#2B2A1E', acc: '#F2A33A', lit: '#D9B866' },
  GECE:  { paper: '#E9E1CF', sky1: '#3B4C6B', sky2: '#26324B', far: '#1E2840', mid: '#141B2E', near: '#0B0F1C', acc: '#F2D27A', lit: '#7A8BAE' },
};
// Film boyunca palet saati: [{at, pal, dur}] — at çapası, dur yeniden mürekkepleme (çapraz rakle) süresi. Planlarda PALT doldurulur.
const PALT = [];
// plan listesindeki 'pal' alanı palet saatini kurar (plan başında değişim = kesmeyle; çekim içindeyse çapraz rakle)
if (window.PLAN) { PALT.push({ at: -1e9, pal: 'SAFAK' }); for (const p of Object.values(window.PLAN)) if (p.pal) PALT.push({ at: p.palat || p.at, pal: p.pal, dur: .4 }); }
function palAt(t) { let cur = PALT.length ? PALT[0] : { pal: 'SAFAK', at: -1e9 }, prev = null; for (const p of PALT) { const a = A(p.at); if (a <= t) { prev = cur; cur = { ...p, a }; } } return { cur, prev }; }

const SHOTS = [];
let SHOTS_SORTED = false;
// shot(başlangıç, çizim, {tr: {type: 'cut'|'pull', dur, dir}, over, mb, id, pal})
function shot(at, draw, o = {}) { SHOTS.push({ at, draw, ...o }); SHOTS_SORTED = false; }
function plan(id, draw, o = {}) { shot(PA(id, o.off || 0), draw, { id, ...o }); }
function shotAt(t) {
  if (!SHOTS_SORTED) { SHOTS.sort((a, b) => a.at - b.at); SHOTS_SORTED = true; }
  let i = 0;
  for (let k = 0; k < SHOTS.length; k++) if (SHOTS[k].at <= t) i = k;
  return i;
}
function shotState(i, t) {
  const sh = SHOTS[i], end = (SHOTS[i + 1] ? SHOTS[i + 1].at : (window.DUR || sh.at + 10));
  return { t, at: sh.at, lt: t - sh.at, d: end - sh.at, p: clamp((t - sh.at) / (end - sh.at)), end, seed: (i + 1) * 7.31 };
}
function camOf(c) { if (!c) return { x: 0, y: 0, s: 1 }; const z = c.z ?? 1, cx = c.cx ?? W / 2, cy = c.cy ?? H / 2; return { x: cx - W / 2 / z, y: cy - H / 2 / z, s: z }; }
function camLerp(a, b, p, ease = E.io2) { const u = ease(clamp(p)); return { cx: lerp(a.cx ?? W / 2, b.cx ?? W / 2, u), cy: lerp(a.cy ?? H / 2, b.cy ?? H / 2, u), z: lerp(a.z ?? 1, b.z ?? 1, u) }; }

// ── Baskı ──
let TEX = null;
function buildTextures() { TEX = SK.makeTextures('#F3E6CC', 7); }
// pr: bir çekimin baskı bağlamı. pr.ink(path, rol ya da '#renk', {knock, reg, sheen, trap, rule, dx, dy}) bir mürekkep katmanı basar.
// Her katman sırasıyla kendi kayıklığını alır (çekim tohumundan, belirlenimci); 'reg: 0' kaymayı kapatır (yazı vb.).
function makePrinter(ctx, st, pal, cam) {
  let k = 0;
  const pr = {
    ctx, st, pal, cam, t: st.t, lt: st.lt,
    col: r => (r && r[0] === '#' ? r : pal[r] || r),
    ink(path, role, o = {}) {
      const n = k++, s = st.seed * 13.7 + n * 3.1, amp = o.regAmp ?? 2.2;
      const reg = o.reg === 0 ? [0, 0] : (o.reg || [(hash(s) - .5) * 2 * amp, (hash(s + 1.7) - .5) * 2 * amp]);
      SK.ink(ctx, { path, knock: o.knock, rule: o.rule, paint: o.paint }, { color: pr.col(role), reg: [reg[0] / cam.s, reg[1] / cam.s], sheen: o.sheen ?? .35, trap: o.trap ?? .6, lw: 1.4 / cam.s, clip: o.clip });
    },
    // tam kare zemin bandı (gök): dünya koordinatında geniş dikdörtgen
    fillAll(role, o = {}) { const p = new Path2D(); p.rect(cam.x - 400, cam.y - 400, W / cam.s + 800, H / cam.s + 800); pr.ink(p, role, { sheen: 0, trap: 0, ...o }); },
    // basamaklı gök: y0'dan y1'e A rengi üstüne B bantları
    // gök: üstte düz koyu bant (0..y0), y0..y1 arası incelen basamaklar, altı açık gök
    sky(top, bottom, y0, y1, n = 5) { pr.fillAll(bottom); const p = new Path2D(); p.rect(cam.x - 400, cam.y - 400, W / cam.s + 800, y0 - cam.y + 400); pr.ink(p, top, { sheen: 0, trap: 0 }); pr.bands(top, y0, y1, n); },
    // basamaklı bantlar (SK.bandSteps'in bizim sürümü): en ince bant 7 px (360p'de titremesin; kurul D)
    bands(roleB, y0, y1, n = 5, curve = 0, o = {}) { const p = new Path2D(), x = cam.x - 400, w = W / cam.s + 800, cell = (y1 - y0) / n;
      for (let i = 0; i < n; i++) { const th = Math.max(7, cell * (1 - (i + .5) / n) * .95), top = y0 + cell * i; p.rect(x, top, w, th); }
      pr.ink(p, roleB, { sheen: 0, trap: .3, ...o }); },
  };
  return pr;
}
// baski(ctx, st, cam, fn, o): kâğıt + mürekkepler + baskı sonu dokusu. o.pal zorla palet ('OGLE' ya da nesne).
function baskiPal(ctx, st, cam, fn, pal) {
  const c = camOf(cam);
  ctx.save(); baseT(ctx);
  SK.paperSheet(ctx, TEX, 0, 0, W, H, .6);
  ctx.translate(-c.x * c.s, -c.y * c.s); ctx.scale(c.s, c.s);
  const pr = makePrinter(ctx, st, pal, c);
  fn(pr);
  ctx.restore();
}
function baski(ctx, st, cam, fn, o = {}) {
  if (!cam && !o.sabit) cam = { cx: o.fx ?? 960, cy: o.fy ?? 540, z: 1 + (o.nefes ?? .035) * clamp(st.p ?? 0) };   // doğrusal: hareket ilk karede başlar (freezedetect)   // kurgu kurulu E: donuk kare yok
  if (o.pal) { baskiPal(ctx, st, cam, fn, typeof o.pal === 'string' ? PAL[o.pal] : o.pal); return; }
  const { cur, prev } = palAt(st.t), dur = cur.dur ?? .4;
  baskiPal(ctx, st, cam, fn, PAL[cur.pal]);
  // yeniden mürekkepleme (tarif §5): geniş rakle ~0,4 sn'de kareyi çapraz geçer; önünde eski palet, arkasında yeni. Bıçak ve boncuk görünür.
  if (prev && st.t < cur.a + dur && cur.a > st.at + .05) {
    const p = clamp((st.t - cur.a) / dur), ang = -.32, L = 2600;
    const fx = lerp(-700, W + 700, p);                                           // döndürülmüş çerçevede cephe
    ctx.save(); baseT(ctx); ctx.translate(W / 2, H / 2); ctx.rotate(ang);
    const clip = new Path2D(); clip.rect(fx - W / 2, -L / 2, L, L);            // cephenin önü: eski palet
    ctx.clip(clip); ctx.rotate(-ang); ctx.translate(-W / 2, -H / 2);
    baskiPal(ctx, st, cam, fn, PAL[prev.pal]); ctx.restore();
    ctx.save(); baseT(ctx); ctx.translate(W / 2, H / 2); ctx.rotate(ang);
    const np = PAL[cur.pal];
    SK.squeegee(ctx, [fx - W / 2, -900], [fx - W / 2, 900], [1, 0], { scale: 1.6, roll: st.t * 6, handle: .25, beads: [{ t0: 0, t1: .45, color: np.sky2 }, { t0: .45, t1: .7, color: np.mid }, { t0: .7, t1: 1, color: np.near }], bead: 30 });
    ctx.restore();
  }
}

const bufA = makeCanvas(DW, DH), bufAx = bufA.getContext('2d');
function drawShot(ctx, i, t) { const sh = SHOTS[i]; if (!sh) return; ctx.save(); sh.draw(ctx, shotState(i, t)); ctx.restore(); }
function drawFilm(ctx, t) {
  const sc = new URLSearchParams(location.search).get('scene');
  if (sc && typeof SCENES !== 'undefined' && SCENES[sc]) { SCENES[sc](ctx, t); post(ctx, t); return; }
  if (!SHOTS.length) return;
  const i = shotAt(t), sh = SHOTS[i], tr = sh.tr;
  drawShot(ctx, i, t);
  // mürekkep çekişi: yeni baskı, parçalı bir rakle cephesiyle eskisinin üstüne iner (saydamlık yok)
  if (tr && tr.type === 'pull' && i > 0 && t < sh.at + (tr.dur || .6)) {
    const p = clamp((t - sh.at) / (tr.dur || .6));
    drawShot(bufAx, i - 1, t);
    const clip = SK.wipeRegion([0, 0, W, H], tr.dir || 'down', p, i, 46, 7);
    const inv = new Path2D(); inv.rect(-1e4, -1e4, 2e4, 2e4); inv.addPath(clip);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.scale(RS, RS); ctx.clip(inv, 'evenodd'); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(bufA, 0, 0); ctx.restore();
  }
  post(ctx, t);
}
// Son işlem: mürekkep benekleri ve iğne delikleri bütün sayfaya (kâğıtta görünmez, mürekkepte görünür)
function post(ctx, t) { ctx.save(); baseT(ctx); SK.inkFinish(ctx, TEX, 0, 0, W, H, .6, 1); ctx.restore(); }

// ── Ekran yazıları (baskıdan sonra; yazı da bir mürekkeptir: kaymasız, düz) ──
const NOTEXT = typeof location !== 'undefined' && new URLSearchParams(location.search).has('notext');
const FONT = { baslik: (px) => `400 ${px}px "Bebas Neue"`, metin: (px, w = 600) => `${w} ${px}px "Hanken Grotesk"` };
function drawOver(ctx, t) {
  if (!SHOTS.length) return;
  const i = shotAt(t), sh = SHOTS[i]; if (!sh || !sh.over) return;
  const st = shotState(i, t), pal = PAL[palAt(t).cur.pal];
  ctx.save(); baseT(ctx); sh.over(ctx, st, pal); ctx.restore();
}
function wrapLines(ctx, s, maxW) {
  const out = []; for (const par of String(s).split('\n')) { let ln = ''; for (const w of par.split(' ')) { const tt = ln ? ln + ' ' + w : w; if (ctx.measureText(tt).width > maxW && ln) { out.push(ln); ln = w; } else ln = tt; } out.push(ln); }
  return out;
}
// Yazı basımı: soldan sağa mürekkep çekişiyle belirir (silme cephesi), kesmeyle gider. o: {px, font, col, ls, align, t0, dur, maxW}
function basYazi(ctx, s, x, y, lt, o = {}) {
  if (NOTEXT || !s) return;
  ctx.save(); ctx.font = o.font || FONT.baslik(o.px || 120); ctx.textAlign = o.align || 'center'; ctx.textBaseline = 'middle';
  if (o.ls) ctx.letterSpacing = o.ls + 'px';
  const L = wrapLines(ctx, s, o.maxW || 1500), lh = (o.px || 120) * (o.lh || 1.02);
  let wd = 0; for (const l of L) wd = Math.max(wd, ctx.measureText(l).width);
  const p = clamp((lt - (o.t0 || 0)) / (o.dur || .45)); if (p <= 0) { ctx.restore(); return; }
  const x0 = (o.align === 'left' ? x : o.align === 'right' ? x - wd : x - wd / 2) - 20, y0 = y - L.length * lh / 2 - 20;
  ctx.clip(SK.wipeRegion([x0, y0, wd + 40, L.length * lh + 40], 'right', p, 5, 24, 5));
  ctx.fillStyle = o.col || '#1E3B3F';
  L.forEach((l, k) => ctx.fillText(l, x, y - (L.length - 1) * lh / 2 + k * lh));
  ctx.restore();
}
// Bölüm başlığı: gökyüzüne basılmış büyük başlık + altında küçük merak sorusu
function bolumBasligi(ctx, title, soru, lt, pal, o = {}) {
  basYazi(ctx, title, o.x ?? W / 2, o.y ?? 230, lt, { px: o.px || 150, ls: 8, col: o.col || pal.near });
  if (soru) basYazi(ctx, soru, o.x ?? W / 2, (o.y ?? 230) + 118, lt, { font: FONT.metin(o.soruPx || 52), col: o.col || pal.near, t0: .35, ls: 1 });
}
