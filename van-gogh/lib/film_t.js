// Van Gogh filmi: tablo motoru üstünde çekim sistemi (lale-cilginligi/lib/film.js'in fikirleri: plan cümleye ya da kelimeye bağlanır).
// Plan = {id, at: 'A01' | 'A01@kelime' | 'A01@kelime#1' | '+0.3', sahne, olcek, kamera(u, lt, st), durum(st), maske(m, st, kam), ust(ctx, st), gecis}
// Ses değişince planlar kendiliğinden kayar (timeline.js: CUES, WORDS, DUR). Belirlenimci: Math.random yok.
// Renk kuralı (karma üslup): dünya grisaille; yalnız Vincent'in tabloları ve zarfları renkli. Renk, ekran uzayındaki örtüyle (finish maske) korunur.
export const W = 1920, H = 1080;
export const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
export const sm = (a, b, x) => { const u = clamp((x - a) / (b - a)); return u * u * (3 - 2 * u); };
export const lerp = (a, b, u) => a + (b - a) * u;
export const hsh = (a, b = 0, c = 0) => { const x = Math.sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453; return x - Math.floor(x); };
export const io = u => (u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2);
export const ikiser = t => Math.floor(t * 15 + 1e-6) / 15;   // canlı darbeler 15 çizim/sn (dosya boyu ve boya titreşimi)

// ---------- zaman ----------
const nrm = w => w.toLocaleLowerCase('tr').replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u').replace(/[^\wçğıöşü]/g, '');
export const S = id => (window.CUES && CUES[id] ? CUES[id].s : 0);
export const Se = id => (window.CUES && CUES[id] ? CUES[id].e : 0);
export function Wd(id, w, n = 0, end = false) {
  const q = nrm(w); let k = 0;
  for (const x of (window.WORDS || [])) if (x.id === id && nrm(x.w).startsWith(q)) { if (k++ === n) return end ? x.e : x.s; }
  console.log('kelime yok: ' + id + '@' + w); return S(id);
}
export function A(at) {
  const m = String(at).match(/^([A-Z]\d+[a-z]?)(?:@([^#+-]+)(?:#(\d+))?)?(~)?([+-][\d.]+)?$/);
  if (!m) { console.log('çapa yok: ' + at); return 0; }
  return (m[2] ? Wd(m[1], m[2], +(m[3] || 0), !!m[4]) : (m[4] ? Se(m[1]) : S(m[1]))) + (m[5] ? +m[5] : 0);
}

// ---------- planlar ----------
const PL = [];
let sirali = false;
export function plan(p) { PL.push(p); sirali = false; }
export function planlar() { return PL; }
function sirala() {
  for (const p of PL) p._at = typeof p.at === 'number' ? p.at : A(p.at) + (p.off || 0);
  PL.sort((a, b) => a._at - b._at);
  PL[0]._at = 0; sirali = true;
}
export function planBul(t) {
  if (!sirali) sirala();
  let i = 0; for (let k = 0; k < PL.length; k++) if (PL[k]._at <= t + 1e-6) i = k;
  const p = PL[i], son = PL[i + 1] ? PL[i + 1]._at : (window.DUR || p._at + 8);
  return { p, i, st: { t, at: p._at, lt: t - p._at, d: son - p._at, u: clamp((t - p._at) / (son - p._at)), son } };
}
export function planTablosu() { if (!sirali) sirala(); return PL.map((p, i) => ({ id: p.id, sahne: p.sahne, olcek: p.olcek, s: +p._at.toFixed(2), d: +((PL[i + 1] ? PL[i + 1]._at : window.DUR) - p._at).toFixed(2), not: p.not || '' })); }

// ---------- renk örtüsü ----------
export const MW = 480, MH = 270;
const mc = document.createElement('canvas'); mc.width = MW; mc.height = MH;
export const mx = mc.getContext('2d');
export function maskeBasla() { mx.setTransform(1, 0, 0, 1, 0, 0); mx.globalCompositeOperation = 'source-over'; mx.globalAlpha = 1; mx.fillStyle = '#000'; mx.fillRect(0, 0, MW, MH); return mc; }
// dünya → ekran (bir katmanın kamerasıyla; sahne.js camK ile aynı dönüşüm)
export const ekrana = (c, x, y) => [(x - c.x) * c.zoom + W / 2, (y - c.y) * c.zoom + H / 2];
// örtüye yumuşak kenarlı dikdörtgen (dünya koordinatı, katman kamerası c): a = 0..1 açıklık
export function mRect(c, x, y, w, h, a = 1, yum = 6) {
  if (a <= 0) return; const [x0, y0] = ekrana(c, x, y), [x1, y1] = ekrana(c, x + w, y + h), k = MW / W;
  mx.save(); mx.globalAlpha = clamp(a); mx.filter = `blur(${yum}px)`; mx.fillStyle = '#fff';
  mx.fillRect(x0 * k, y0 * k, (x1 - x0) * k, (y1 - y0) * k); mx.restore();
}
// örtüye fırça kenarlı daire (renk bir noktadan yayılır): r dünya pikseli
export function mDaire(c, x, y, r, a = 1, yum = 10) {
  if (a <= 0 || r <= 0) return; const [X, Y] = ekrana(c, x, y), k = MW / W;
  mx.save(); mx.globalAlpha = clamp(a); mx.filter = `blur(${yum}px)`; mx.fillStyle = '#fff'; mx.beginPath();
  for (let i = 0; i <= 48; i++) { const t = i / 48 * Math.PI * 2, rr = r * c.zoom * (1 + .08 * Math.sin(t * 5 + 1) + .05 * Math.sin(t * 11)); mx.lineTo((X + Math.cos(t) * rr) * k, (Y + Math.sin(t) * rr) * k); }
  mx.fill(); mx.restore();
}
export function mTam(a = 1) { if (a <= 0) return; mx.save(); mx.globalAlpha = clamp(a); mx.fillStyle = '#fff'; mx.fillRect(0, 0, MW, MH); mx.restore(); }

// ---------- gerçek tablo → yağlıboya katmanı ----------
// img (ImageBitmap) dünya dikdörtgenine (x, y, w, h) "kapla" (cover) ya da "sigdir" ile yerleşir; darbe yönü resmin değer kenarlarını izler (dir yok).
export function tabloCiz(img, x, y, w, h, o = {}) {
  return R => {
    const P = c => { c.moveTo(x, y); c.lineTo(x + w, y); c.lineTo(x + w, y + h); c.lineTo(x, y + h); c.closePath(); };
    R.fill(P, '#000', { maxR: o.maxR ?? 14, type: o.type ?? 1, len: o.len ?? 1.6, wid: o.wid ?? .7, hgt: o.hgt ?? .55, group: o.grup || 'tablo', jit: o.jit ?? .03, aj: o.aj ?? .25, detail: o.detail ?? .8 });
    const c = R.ref.ctx, iw = img.width, ih = img.height;
    let sx = 0, sy = 0, sw = iw, sh = ih;
    if (o.kirp) [sx, sy, sw, sh] = o.kirp.map((v, i) => v * (i % 2 ? ih : iw));
    else { const ar = w / h, ia = sw / sh; if (ia > ar) { const n = sh * ar; sx += (sw - n) / 2; sw = n; } else { const n = sw / ar; sy += (sh - n) / 2; sh = n; } }
    c.save(); c.beginPath(); P(c); c.clip(); c.drawImage(img, sx, sy, sw, sh, x, y, w, h); c.restore();
  };
}
// tam kare tablo sahnesi (renk doruğu ve tablo planları): tablo kadrajı doldurur, kenarı biraz taşar (kamera yaklaşınca kenar görünmesin).
// o.dunya: Vincent'in tablosu gri dünya olarak (grisaille; renk örtüyle açılır), üstünde canlı katmanlar (figür, nesne, üst).
export function tabloSahnesi(M, ad, img, o = {}) {
  const pay = o.pay ?? 60, d = o.d ?? .72;
  const canli = (k, kap = 12000) => ({ ad: k, d, canli: (t, S, c, x, du) => { if (du && du[k]) du[k](t, S); }, kap, wet: .2, run: 0 });
  M.tanimla(ad, { zemin: o.zemin || [.08, .07, .06], kamera: () => ({ x: W / 2, y: H / 2, z: 1 }),
    katmanlar: [{ ad: 'tablo', d, ciz: tabloCiz(img, -pay, -pay, W + 2 * pay, H + 2 * pay, o), R: o.R || [22, 11, 5.5, 2.8, 1.5], T: o.T ?? 9, olcek: o.olcek ?? .5 }, ...(o.ek || []), canli('nesne', 4000), canli('figur', 16000), canli('ust', 4000)],
    bitir: o.bitir || ((t, du) => ({ light: [-.5, -.6, .7], norm: 2.2, expo: du && du.expo ? du.expo(t) : 1.03, sat: 1.05, contrast: 1.04, vig: .25, spec: .12, shin: 26, weave: .05,
      mono: o.dunya ? 1 : 0, monoK: [.05, .045, .045], monoA: [.96, .94, .9] })) });
}
