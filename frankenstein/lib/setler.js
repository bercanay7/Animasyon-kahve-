// Ortak setler ve slayt yazıları (Frankenstein). ORTAK DOSYA: yalnız başkan değiştirir.
'use strict';
const SET = (() => {
  // slayta yazılmış ışık harfleri (fener başlık slaytı gibi; sahnenin parçası, ışıkla birlikte titrer). Ekran koordinatı.
  // p: yazılma (0..1, harf harf), o: {px, font, renk, align, ls}
  function camYazi(R, s, x, y, o = {}) {
    if (NOTEXT && !o.force) return;
    const p = o.p ?? 1, n = [...s].length, k = Math.ceil(n * clamp(p)); if (k <= 0) return;
    R.ekran(g => { g.save(); g.font = o.font || FONT.baslik(o.px || 80, o.w || 700); g.textAlign = o.align || 'center'; g.textBaseline = 'middle'; if (o.ls != null) g.letterSpacing = o.ls + 'px';
      g.globalCompositeOperation = 'source-over'; g.fillStyle = o.renk || '#F6E7C4'; g.globalAlpha = o.a ?? 1;
      const full = g.measureText(s).width, x0 = (o.align || 'center') === 'center' ? x - full / 2 : o.align === 'right' ? x - full : x;
      g.textAlign = 'left'; g.fillText([...s].slice(0, k).join(''), x0, y); g.restore(); });
  }
  // bölüm kartı: koyu cam, oyma çerçeve, Romen rakamı, başlık, merak sorusu (≤ 8 sn)
  function kart(R, st, rakam, baslik, soru) {
    R.kara(g => g.rect(-2000, -2000, 6000, 6000), { renk: '#140C07' });
    const a = E.out3(clamp(st.lt / .8));
    R.ekran(g => { g.save(); g.strokeStyle = '#B88A4A'; g.globalAlpha = .85 * a; g.lineWidth = 3; g.beginPath(); g.ellipse(960, 470, 560, 300, 0, 0, TAU); g.stroke();
      g.lineWidth = 1.5; g.beginPath(); g.ellipse(960, 470, 540, 282, 0, 0, TAU); g.stroke(); g.restore(); });
    camYazi(R, rakam, 960, 300, { px: 64, a, renk: '#C99A55', ls: 10 });
    camYazi(R, baslik, 960, 420, { px: 96, a, ls: 8 });
    if (soru) camYazi(R, soru, 960, 560, { font: FONT.alinti(68), a: clamp((st.lt - .6) / .7), renk: '#EAD7B0' });
  }
  // el yazısı satırları (kâğıtta): s metni p oranında yazılır; mürekkep koyu
  function elYazisi(R, s, x, y, px, p, o = {}) {
    const g = R.g; g.save(); g.font = FONT.alinti(px, 500); g.textBaseline = 'alphabetic'; g.fillStyle = o.renk || '#2A1A10'; g.globalCompositeOperation = 'source-over';
    const L = wrapLines(g, s, o.maxW || 700), lh = px * 1.3, tot = [...s].length; let kalan = Math.ceil(tot * clamp(p));
    L.forEach((l, i) => { if (kalan <= 0) return; const part = [...l].slice(0, kalan).join(''); kalan -= [...l].length + 1; g.fillText(part, x, y + i * lh); });
    g.restore();
  }
  // Diodati salonu: şömine (sol), pencere (sağ), yağmur; ateş ışığı
  function salon(R, st, o = {}) {
    R.gok(-600, -400, 2600, 1500, [[0, '#9A6A44'], [1, '#6E4830']], { firca: 1.2 });
    DK.pencere(R, 1480, 360, 330, 470, { gece: '#5C6F9A' });
    R.yika(g => g.rect(-600, 880, 3200, 700), '#4E3424', { firca: 1 });
    // şömine
    R.kara(g => { g.rect(140, 380, 440, 40); g.rect(160, 420, 60, 470); g.rect(500, 420, 60, 470); g.rect(140, 880, 440, 20); });
    R.yika(g => g.rect(220, 420, 280, 460), '#2A1810', { firca: 0 });
    DK.ates(R, 360, 870, 200, { t: st.t });
  }
  // Mary'nin masası (Diodati, gece): pencere, mum, kâğıt
  function masa(R, st, o = {}) {
    R.gok(-600, -400, 2600, 1500, [[0, '#8C6A4A'], [1, '#6A4E38']], { firca: 1.2 });
    DK.pencere(R, 1420, 360, 340, 500, { gece: o.gece || '#5A6E9C', ay: o.ay });
    R.yika(g => g.rect(-600, 900, 3200, 700), '#5A4030', { firca: 1 });
    DK.masa(R, 960, 640, 760, { h: 300 });
  }
  return { camYazi, kart, elYazisi, salon, masa };
})();
