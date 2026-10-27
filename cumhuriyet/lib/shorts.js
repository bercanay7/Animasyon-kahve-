// Dikey Shorts kurgusu: film karelerinden kesitler (EDL), 9:16 kırpma ve kelime kelime altyazı (taş baskı üslubu).
// shorts.html?rs=2&notext=1 ile; window.SHORT = { EDL, GROUPS, CTA, DUR } (shorts/edl.js)
'use strict';
const SHW = 1080, SHH = 1920;
const shortCv = makeCanvas(SHW, SHH), shx = shortCv.getContext('2d');
function shortClip(ts) {
  const E_ = window.SHORT.EDL; let i = 0;
  for (let k = 0; k < E_.length; k++) if (E_[k].s <= ts) i = k;
  return E_[i];
}
function renderShortFrame(ts, mb = 1) {
  const c = shortClip(ts), u = clamp((ts - c.s) / (c.e - c.s));
  const tf = c.f + (ts - c.s) * (c.speed || 1);
  if (mb > 1) renderFrameMB(tf, mb); else renderFrame(tf);
  // 9:16 kırpma: mantıksal genişlik H*9/16 = 607.5; merkez (cx) ve yakınlık (z) zamanla değişebilir
  const z = lerp(c.z0 ?? 1, c.z1 ?? c.z0 ?? 1, E.io2(u));
  const cx = lerp(c.cx0, c.cx1 ?? c.cx0, E.io2(u)), cy = lerp(c.cy0 ?? H / 2, c.cy1 ?? c.cy0 ?? H / 2, E.io2(u));
  const cw = H * 9 / 16 / z, ch = H / z;
  const x0 = clamp(cx - cw / 2, 0, W - cw), y0 = clamp(cy - ch / 2, 0, H - ch);
  shx.setTransform(1, 0, 0, 1, 0, 0); shx.globalAlpha = 1; shx.globalCompositeOperation = 'source-over';
  shx.imageSmoothingQuality = 'high';
  shx.drawImage(document.getElementById('c'), x0 * RS, y0 * RS, cw * RS, ch * RS, 0, 0, SHW, SHH);
  shortOverlay(shx, ts);
  return shortCv;
}
// kâğıt künye kutusu (dikey kadraj ölçeğinde)
function shBox(g, x0, y0, w, h, seed) {
  g.save(); g.globalAlpha *= .4; g.fillStyle = P.ink; g.fillRect(x0 + 10, y0 + 12, w, h); g.restore();
  const box = PL(rough([[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]], 1, seed));
  knock(g, box); inkStroke(g, box, 4); inkStroke(g, PL([[x0 + 12, y0 + 12], [x0 + w - 12, y0 + 12], [x0 + w - 12, y0 + h - 12], [x0 + 12, y0 + h - 12]]), 1.6);
}
// üst künye, altyazı (etkin kelime kırmızı), sonda kanal çağrısı
function shortOverlay(g, ts) {
  const S_ = window.SHORT, clip = S_.EDL.find(c => ts >= c.s && ts < c.e) || S_.EDL[S_.EDL.length - 1];
  const capY = clip.capY ?? 1280, ctaY = clip.ctaY ?? 1210;
  const grNow = S_.GROUPS.find(gr => ts >= gr.s - .05 && ts < gr.e + .15);
  // kesmeden geçen grup kesmede kısa bir solmayla yeni yerine geçer
  const reIn = grNow && grNow.s < clip.s ? (grNow.e <= clip.s + .03 ? 0 : clamp((ts - clip.s) / .16)) : 1;
  // üst künye: "29 EKİM 1923" + alt satır (Shorts arayüzü üstte ~120 px'i kapatır)
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
  shBox(g, 150, 150, 780, 200, 7);
  txt(g, '29 EKİM 1923', SHW / 2, 262, FONT.title(92), { align: 'center', ls: 3 });
  g.fillStyle = P.red; g.fillRect(200, 284, 680, 8);
  txt(g, 'BİR KUŞAĞIN HİKÂYESİ', SHW / 2, 330, FONT.mono(34), { align: 'center', ls: 5 });
  g.restore();
  // altyazı: YouTube Shorts arayüzü alt ~%25'i ve sağ kenarı kapatır; merkez x 510, genişlik ≤ 830
  const groups = S_.GROUPS, gi0 = groups.findIndex(gr => ts >= gr.s - .05 && ts < gr.e + .15), gi = gi0 < 0 && ts < groups[0].s ? 0 : gi0;
  const ce = S_.CTA ?? 1e9;
  if (gi >= 0) {
    const gr = groups[gi], a = (gi === 0 ? 1 : clamp((ts - gr.s + .05) / .12)) * reIn * (1 - clamp((ts - ce + .1) / .2));
    if (a > 0) {
      g.save(); g.font = FONT.slab(78); g.letterSpacing = '1px'; g.textAlign = 'left'; g.textBaseline = 'middle';
      const up = s => s.toLocaleUpperCase('tr');
      { const tot = g.measureText(gr.words.map(w => up(w.w)).join(' ')).width; if (tot > 830 && tot < 830 / .86) g.font = FONT.slab(Math.floor(78 * 830 / tot)); }
      const words = gr.words, sp = g.measureText(' ').width;
      const lines = []; let cur = [], wsum = 0;
      for (const w of words) { const ww = g.measureText(up(w.w)).width; if (cur.length && wsum + sp + ww > 830) { lines.push(cur); cur = []; wsum = 0; } cur.push({ ...w, ww }); wsum += (cur.length > 1 ? sp : 0) + ww; }
      if (cur.length) lines.push(cur);
      const y0 = capY - (lines.length - 1) * 50;
      // okunurluk: kâğıt bant (taş baskı künyesi gibi), kenarları kırık
      const bw = Math.max(...lines.map(ln => ln.reduce((q, w) => q + w.ww, 0) + sp * (ln.length - 1))) + 70, bh = lines.length * 100 + 34;
      g.globalAlpha = a * .9; knock(g, PL(rough([[510 - bw / 2, y0 - 67], [510 + bw / 2, y0 - 67], [510 + bw / 2, y0 - 67 + bh], [510 - bw / 2, y0 - 67 + bh]], 1.2, gi)));
      g.globalAlpha = a; inkStroke(g, PL(rough([[510 - bw / 2, y0 - 67], [510 + bw / 2, y0 - 67], [510 + bw / 2, y0 - 67 + bh], [510 - bw / 2, y0 - 67 + bh]], 1.2, gi)), 3);
      lines.forEach((ln, li) => {
        const tw = ln.reduce((q, w) => q + w.ww, 0) + sp * (ln.length - 1);
        let x = 510 - tw / 2;
        for (const w of ln) {
          const on = ts >= w.s - .03, cur2 = on && ts < w.e + .05;
          const pop = cur2 ? 1 + .05 * clamp(1 - (ts - w.s) / .15) : 1;
          g.save(); g.translate(x + w.ww / 2, y0 + li * 100); g.scale(pop, pop); g.globalAlpha = a; g.textAlign = 'center';
          g.fillStyle = cur2 ? P.red : (on ? P.ink : rgba(P.ink, .45)); g.fillText(up(w.w), 0, 0);
          g.restore();
          x += w.ww + sp;
        }
      });
      g.restore();
    }
  }
  // son: kanal çağrısı
  if (ts > ce) {
    const q = clamp((ts - ce) / .4); g.save(); g.globalAlpha = q;
    shBox(g, 110, ctaY, 800, 190, 11);
    txt(g, 'TAM HİKÂYE KANALDA', 510, ctaY + 96, FONT.title(64), { align: 'center', ls: 2 });
    g.fillStyle = P.red; g.fillRect(170, ctaY + 118, 680 * E.out3(clamp((ts - ce) / .8)), 7);
    txt(g, 'ZAMAN KURYESİ', 510, ctaY + 160, FONT.mono(32), { align: 'center', ls: 6 });
    g.restore();
  }
}
window.renderShortFrame = renderShortFrame;
