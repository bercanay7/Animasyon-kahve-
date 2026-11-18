// film.js (Mary Stuart): Zaman Kuryesi çekim sistemi (S, Wd, AT, plan) + LemoLab silent-film birleştiricisi.
// Kare hattı: plan 4:3 ton resmini boyar (TC, gri değerler) → Redraw (mürekkep çizgisi, yıkama basamakları, kaynayan tarama)
// → "tek renk" (RC: yalnız kırmızı, çizginin altında kalır) → FilmPost (gümüş/sepya baskı, gren, titreme, kayma, çizik)
// → toz ve kıl → perdeler arasında 4:3 kapıya yansıtılır. Hareket elle çevrilen projektör gibi 15 kare/sn örneklenir; titreme 24.
// Plan: plan(id, 'A01@kelime', (G, st) => ({ look, kart, redraw, perde }), o)
'use strict';
const S = id => (window.CUES && CUES[id] ? CUES[id].s : 0);
const Se = id => (window.CUES && CUES[id] ? CUES[id].e : 0);
function Wd(id, w, n = 0, end = false) {
  const nw = w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
  let k = 0;
  for (const x of (window.WORDS || [])) if (x.id === id && x.w.startsWith(nw)) { if (k++ === n) return end ? x.e : x.s; }
  if (window.WORDS && WORDS.length) console.log('kelime yok: ' + id + '@' + w);
  return S(id);
}
function AT(at) {
  if (typeof at === 'number') return at;
  const m = at.match(/^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?([+-][\d.]+)?$/);
  if (!m) return 0;
  return (m[2] ? Wd(m[1], m[2], +(m[3] || 0)) : S(m[1])) + (m[4] ? +m[4] : 0);
}
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const ss = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const eio = x => { x = clamp(x); return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
const SHOTS = []; let SORTED = false;
function plan(id, at, fn, o = {}) { SHOTS.push({ id, at: AT(at), fn, ...o }); SORTED = false; }
function shotAt(t) { if (!SORTED) { SHOTS.sort((a, b) => a.at - b.at); SORTED = true; } let i = 0; for (let k = 0; k < SHOTS.length; k++) if (SHOTS[k].at <= t) i = k; return i; }
function shotState(i, t) { const sh = SHOTS[i], end = SHOTS[i + 1] ? SHOTS[i + 1].at : (window.DUR || sh.at + 10); return { id: sh.id, t, at: sh.at, lt: t - sh.at, d: end - sh.at, p: clamp((t - sh.at) / Math.max(.01, end - sh.at)), end }; }
const IMG = {};
function loadImg(k, src) { return new Promise(r => { const im = new Image(); im.onload = () => { IMG[k] = im; r(); }; im.onerror = () => { console.log('görsel yok ' + src); r(); }; im.src = src; }); }

// ── birleştirici ──
const FW = 1440, FH = 1080, GATE = { x: 240, y: 0, w: FW, h: FH };
const mk = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const TC = mk(FW, FH), tg = TC.getContext('2d');          // ton resmi
const RC = mk(FW, FH), rg = RC.getContext('2d');          // tek renk (kırmızı) katmanı: yalnız boyanan yerler
const MC = mk(FW, FH), mg = MC.getContext('2d');          // renk maskesi: kırmızı × çizim
const XC = mk(FW, FH), xg = XC.getContext('2d');
let RD = null, FP = null;
const LOOK0 = { strength: .34, sepia: .2, fps: 15 };
function renderFrameTo(g, t) {
  RD = RD || new SFR.Redraw(FW, FH); FP = FP || new SFP.FilmPost(FW, FH);
  const i = shotAt(t), st = shotState(i, t), sh = SHOTS[i];
  const fps = sh.fps || LOOK0.fps, ta = Math.floor(t * fps + 1e-6) / fps, frame = Math.floor(t * 24 + 1e-6);
  const sta = shotState(i, Math.max(sh.at, ta));
  for (const c of [tg, rg]) { c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.filter = 'none'; }
  tg.fillStyle = '#fff'; tg.fillRect(0, 0, FW, FH); rg.clearRect(0, 0, FW, FH);
  const G = BOYA.ctx(tg, rg, sta);
  let o = {};
  try { o = sh.fn(G, sta) || {}; } catch (e) { console.log('[plan ' + sh.id + '] ' + e.message); }
  let src = TC;
  if (o.kart) { tg.setTransform(1, 0, 0, 1, 0, 0); SFC.intertitle(tg, FW, FH, o.kart, st.lt); }
  else src = RD.render(TC, { frame, ...(o.redraw || {}) });
  // tek renk: kırmızı, çizimin koyuluğuyla çarpılır (çizgi kırmızının üstünde kalır)
  let mask = null;
  if (G.renkVar) {
    mg.setTransform(1, 0, 0, 1, 0, 0); mg.globalCompositeOperation = 'source-over'; mg.clearRect(0, 0, FW, FH);
    mg.drawImage(RC, 0, 0); mg.globalCompositeOperation = 'multiply'; mg.drawImage(src, 0, 0);
    mg.globalCompositeOperation = 'destination-in'; mg.drawImage(RC, 0, 0); mg.globalCompositeOperation = 'source-over';
    mask = MC;
  }
  const look = { ...LOOK0, ...(sh.look || {}), ...(o.look || {}) };
  const dev = FP.render(src, { frame, strength: look.strength, sepia: look.sepia, crank: look.crank ?? 1, exposure: o.exposure ?? 1, halation: o.kart ? 1.4 : 1 }, mask);
  g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over';
  const perde = o.perde ?? 1;
  SFC.theatre(g, 1920, 1080, GATE, Math.max(.3, FP.mean), 1);
  g.save(); g.beginPath(); g.roundRect(GATE.x, GATE.y, GATE.w, GATE.h, 22); g.clip();
  g.drawImage(dev, GATE.x, GATE.y);
  SFP.damage(g, GATE.x, GATE.y, FW, FH, frame, look.strength);
  g.restore();
  if (perde < 1) perdeOn(g, perde, Math.max(.55, FP.mean));
  return g.canvas;
}
// perdeler perdenin önünde: kapanırken görüntünün üstüne çizilir (perde = 1 açık, 0 kapalı)
function perdeOn(g, acik, isik) {
  xg.canvas.width = 1920; xg.canvas.height = 1080;
  SFC.theatre(xg, 1920, 1080, { x: 960, y: 0, w: 0, h: 1080 }, isik, 1);
  const w = (1 - acik) * 960;
  g.save(); g.beginPath(); g.rect(0, 0, w, 1080); g.rect(1920 - w, 0, w, 1080); g.clip(); g.drawImage(XC, 0, 0); g.restore();
}
