// 29 Ekim · story.html ve zumba.html için ortak yardımcılar (tuval 1080x1920)
const W = 1080, H = 1920;
const cv = document.getElementById('c');
const ctx = cv.getContext('2d');

const C = {
  red: '#E30A17', redD: '#B8000F', navy: '#202F50', cream: '#F4EEE4', creamD: '#E9DFD0',
  white: '#FFFFFF', ink: '#1B1B1F', gold: '#C9A15B',
};
const SERIF = "'Instrument Serif'", SANS = 'Inter';
const TAU = Math.PI * 2;

const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, a, b) => clamp((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
const easeOutExpo = x => x >= 1 ? 1 : 1 - Math.pow(2, -10 * x);
const easeInExpo = x => x <= 0 ? 0 : Math.pow(2, 10 * x - 10);
const easeOutCubic = x => 1 - Math.pow(1 - x, 3);
const easeInCubic = x => x * x * x;
const easeInOutCubic = x => x < .5 ? 4 * x ** 3 : 1 - Math.pow(-2 * x + 2, 3) / 2;
const easeOutBack = (x, s = 1.70158) => 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2);

function rng(seed) {
  return () => {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let r = Math.imul(seed ^ seed >>> 15, 1 | seed);
    r = r + Math.imul(r ^ r >>> 7, 61 | r) ^ r;
    return ((r ^ r >>> 14) >>> 0) / 4294967296;
  };
}
function loadImage(src) {
  return new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = () => rej(new Error(src)); i.src = src; });
}
// Türkçe harfler latin-ext alt kümesindedir; ikisinin de yüklendiğinden emin ol
async function loadFonts() {
  const s = 'AZaz0129 İıŞşĞğÜüÖöÇç·—';
  await Promise.all([
    document.fonts.load(`900 100px ${SANS}`, s), document.fonts.load(`800 100px ${SANS}`, s),
    document.fonts.load(`600 100px ${SANS}`, s), document.fonts.load(`italic 400 100px ${SERIF}`, s),
  ]);
  await document.fonts.ready;
}

// ---------- tipografi ----------
function setFont(style, weight, size, family, ls = 0) {
  ctx.font = `${style} ${weight} ${size}px ${family}`; ctx.letterSpacing = ls + 'px';
}
function fitSize(str, style, weight, family, size, maxW, ls = 0) {
  setFont(style, weight, size, family, ls);
  const w = ctx.measureText(str).width;
  return w > maxW ? size * maxW / w : size;
}
// Ortalanmış tek satır; letterSpacing son harften sonra da boşluk bıraktığı için yarısı kadar kaydırılır
function text(str, x, y, { size, color, weight = 900, family = SANS, style = '', ls = 0, maxW = 960, align = 'center' }) {
  const fs = fitSize(str, style, weight, family, size, maxW, ls);
  setFont(style, weight, fs, family, ls);
  ctx.textAlign = align; ctx.textBaseline = 'alphabetic'; ctx.fillStyle = color;
  ctx.fillText(str, x + (align === 'center' ? ls / 2 : 0), y);
  return fs;
}

// ---------- Türk bayrağı ----------
// 2893 sayılı Türk Bayrağı Kanunu ölçüleri (G = bayrağın eni):
//   boy 1.5G; dış hilal Ø 0.5G, merkezi uçkur kenarından 0.5G; iç hilal Ø 0.4G, merkezler arası 1/16 G;
//   iç hilal ile yıldızı çevreleyen çember arası 1/3 G; yıldız çemberi Ø 1/4 G, bir ucu uçkura bakar.
// Bayrağın üzerine hiçbir yazı ya da işaret konmaz; yazılar her zaman bayrağın dışında durur.
function flatFlag(G) {
  const c = document.createElement('canvas'); c.width = Math.round(1.5 * G); c.height = Math.round(G);
  const x = c.getContext('2d'), cy = G / 2;
  x.fillStyle = C.red; x.fillRect(0, 0, c.width, c.height);
  x.fillStyle = '#fff'; x.beginPath(); x.arc(0.5 * G, cy, 0.25 * G, 0, TAU); x.fill();
  x.fillStyle = C.red; x.beginPath(); x.arc(0.5625 * G, cy, 0.2 * G, 0, TAU); x.fill();
  const sx = (0.5625 - 0.2 + 1 / 3 + 0.125) * G, R = 0.125 * G, r = R * Math.cos(TAU / 5) / Math.cos(Math.PI / 5);
  x.fillStyle = '#fff'; x.beginPath();
  for (let i = 0; i < 10; i++) {
    const a = Math.PI + i * Math.PI / 5, rr = i % 2 ? r : R;
    x.lineTo(sx + Math.cos(a) * rr, cy + Math.sin(a) * rr);
  }
  x.closePath(); x.fill();
  return c;
}
const FLAG = flatFlag(800);
// Dalgalanan bayrak: uçkur kenarı sabit, dalga boyu uca doğru büyür; eğime göre gölge/ışık.
// (cx, cy) bayrağın ortası, w genişliği. Gönder (direk) çizilmez.
const _wave = document.createElement('canvas');
function wavingFlag(cx, cy, w, t, o = {}) {
  const { amp = 0.055, waves = 1.2, speed = 0.85, alpha = 1, rot = 0, scale = 1, shadow = 'rgba(70,10,10,0.30)' } = o;
  if (scale <= 0 || alpha <= 0) return;
  const h = w * FLAG.height / FLAG.width, A = amp * w, pad = Math.ceil(A * 1.2 + 6);
  _wave.width = Math.ceil(w); _wave.height = Math.ceil(h + 2 * pad);
  const x = _wave.getContext('2d');
  const off = u => A * Math.pow(u, 0.85) * Math.sin(TAU * (waves * u - speed * t));
  const N = Math.ceil(w / 2), sw = w / N, srcW = FLAG.width / N;
  // Kumaş kıvrıldıkça önden bakınca kısalır: şerit genişliği eğimle daralır, bayrak ortalanır
  const slopes = [], widths = [];
  for (let i = 0; i < N; i++) {
    const u = (i + 0.5) / N, e = 0.5 / N;
    slopes[i] = (off(u + e) - off(u - e)) / (2 * e * w);
    widths[i] = sw / Math.sqrt(1 + slopes[i] * slopes[i]);
  }
  let px = (w - widths.reduce((a, b) => a + b, 0)) / 2;
  const xs = widths.map(d => (px += d) - d);
  for (let i = 0; i < N; i++)
    x.drawImage(FLAG, i * srcW, 0, srcW, FLAG.height, xs[i], pad + off((i + 0.5) / N), widths[i] + 0.7, h);
  x.globalCompositeOperation = 'source-atop';
  for (let i = 0; i < N; i++) {
    const s = slopes[i];
    x.fillStyle = s > 0 ? `rgba(40,0,0,${clamp(s * 0.8, 0, 0.36)})` : `rgba(255,236,230,${clamp(-s * 0.5, 0, 0.2)})`;
    x.fillRect(xs[i], 0, widths[i] + 0.7, _wave.height);
  }
  x.globalCompositeOperation = 'source-over';
  ctx.save(); ctx.globalAlpha *= alpha; ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(scale, scale);
  if (shadow) { ctx.shadowColor = shadow; ctx.shadowBlur = 36; ctx.shadowOffsetY = 18; }
  ctx.drawImage(_wave, -w / 2, -_wave.height / 2);
  ctx.restore();
}

// ---------- fotoğraflar ----------
// Görseli kutuya "cover" sığdır; (fx, fy) odak noktası 0..1
function drawCover(img, x, y, w, h, fx = 0.5, fy = 0.5, zoom = 1) {
  const iw = img.naturalWidth || img.width, ih = img.naturalHeight || img.height;
  const s = Math.max(w / iw, h / ih) * zoom, dw = iw * s, dh = ih * s;
  ctx.drawImage(img, x + (w - dw) * fx, y + (h - dh) * fy, dw, dh);
}
function archPath(x, y, w, h) {
  const r = w / 2;
  ctx.beginPath(); ctx.moveTo(x, y + h); ctx.lineTo(x, y + r);
  ctx.arc(x + r, y + r, r, Math.PI, 0); ctx.lineTo(x + w, y + h); ctx.closePath();
}
// Kemer pencereli fotoğraf: beyaz çerçeve + yumuşak gölge
function archPhoto(img, x, y, w, h, { fx = 0.5, fy = 0.5, border = 10, zoom = 1 } = {}) {
  ctx.save();
  ctx.shadowColor = 'rgba(60,30,10,0.22)'; ctx.shadowBlur = 40; ctx.shadowOffsetY = 16;
  archPath(x - border, y - border, w + 2 * border, h + 2 * border); ctx.fillStyle = C.white; ctx.fill();
  ctx.restore();
  ctx.save(); archPath(x, y, w, h); ctx.clip(); drawCover(img, x, y, w, h, fx, fy, zoom); ctx.restore();
}

// ---------- logo ----------
let LOGO_IMG, LOGO_W_IMG;
async function loadLogos() {
  [LOGO_IMG, LOGO_W_IMG] = await Promise.all([loadImage(window.LOGO.src), loadImage(window.LOGO_WHITE.src)]);
}
function logo(cx, cy, w, white = false, alpha = 1) {
  const img = white ? LOGO_W_IMG : LOGO_IMG, h = w * window.LOGO.h / window.LOGO.w;
  ctx.save(); ctx.globalAlpha *= alpha; ctx.drawImage(img, cx - w / 2, cy - h / 2, w, h); ctx.restore();
}
