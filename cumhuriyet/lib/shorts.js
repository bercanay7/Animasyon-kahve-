// Dikey Shorts kurgusu: film karelerinden kesitler (EDL), 9:16 kırpma ve kelime kelime altyazı (taş baskı üslubu).
// shorts.html?rs=2&notext=1 ile; window.SHORT = { EDL, GROUPS, CTA, DUR } (shorts/edl.js)
'use strict';
const SHW = 1080, SHH = 1920;
const shortCv = makeCanvas(SHW, SHH), shx = shortCv.getContext('2d');
// YouTube Shorts arayüzü: üstte ~120 px, altta ~%25 ve sağda düğme sütunu kapanır → yazılar x ≤ 930, y ≤ 1420
const SH_CX = 495, SH_MAXW = 780, SH_BOT = 1420;
function shortClip(ts) {
  const E_ = window.SHORT.EDL; let i = 0;
  for (let k = 0; k < E_.length; k++) if (E_[k].s <= ts) i = k;
  return E_[i];
}
function renderShortFrame(ts, mb = 1) {
  const c = shortClip(ts), u = clamp((ts - c.s) / (c.e - c.s));
  const tf = c.f + (ts - c.s) * (c.speed || 1);
  if (mb > 1) renderFrameMB(tf, mb); else renderFrame(tf);
  const src = document.getElementById('c');
  shx.setTransform(1, 0, 0, 1, 0, 0); shx.globalAlpha = 1; shx.globalCompositeOperation = 'source-over';
  shx.imageSmoothingQuality = 'high';
  if (c.fit) {
    // fit: 16:9 karenin tamamı 1080×608, üst kenarı y 560 (altyazı bandı altına sığsın); üstü ve altı kâğıt
    shx.fillStyle = P.paper; shx.fillRect(0, 0, SHW, SHH);
    shx.drawImage(src, 0, 0, W * RS, H * RS, 0, 560, SHW, SHW * 9 / 16);
    inkStroke(shx, PL([[0, 560], [SHW, 560]], false), 4); inkStroke(shx, PL([[0, 560 + SHW * 9 / 16], [SHW, 560 + SHW * 9 / 16]], false), 4);
  } else {
    // 9:16 kırpma: mantıksal genişlik H*9/16 = 607.5; merkez (cx) ve yakınlık (z) zamanla değişebilir
    const z = lerp(c.z0 ?? 1, c.z1 ?? c.z0 ?? 1, E.io2(u));
    const cx = lerp(c.cx0, c.cx1 ?? c.cx0, E.io2(u)), cy = lerp(c.cy0 ?? H / 2, c.cy1 ?? c.cy0 ?? H / 2, E.io2(u));
    const cw = H * 9 / 16 / z, ch = H / z;
    const x0 = clamp(cx - cw / 2, 0, W - cw), y0 = clamp(cy - ch / 2, 0, H - ch);
    shx.drawImage(src, x0 * RS, y0 * RS, cw * RS, ch * RS, 0, 0, SHW, SHH);
  }
  shortOverlay(shx, ts, c);
  return shortCv;
}
// kâğıt künye kutusu (dikey kadraj ölçeğinde)
function shBox(g, x0, y0, w, h, seed) {
  g.save(); g.globalAlpha *= .4; g.fillStyle = P.ink; g.fillRect(x0 + 10, y0 + 12, w, h); g.restore();
  const box = PL(rough([[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]], 1, seed));
  knock(g, box); inkStroke(g, box, 4); inkStroke(g, PL([[x0 + 12, y0 + 12], [x0 + w - 12, y0 + 12], [x0 + w - 12, y0 + h - 12], [x0 + 12, y0 + h - 12]]), 1.6);
}
const shUp = s => s.replace(/'/g, '’').toLocaleUpperCase('tr');
// altyazı satırları: 78 px'te en çok 2 satıra sığmazsa 66 px; o da sığmazsa ikişer satırlık sayfalara bölünür
function shLines(g, words) {
  let r;
  for (const fs of [78, 66]) {
    g.font = FONT.slab(fs); const sp = g.measureText(' ').width, lines = []; let cur = [], wsum = 0;
    for (const w of words) { const ww = g.measureText(shUp(w.w)).width; if (cur.length && wsum + sp + ww > SH_MAXW) { lines.push(cur); cur = []; wsum = 0; } cur.push({ ...w, ww }); wsum += (cur.length > 1 ? sp : 0) + ww; }
    if (cur.length) lines.push(cur);
    r = { lines, fs, sp }; if (lines.length <= 2) return r;
  }
  return r;
}
// üst künye, altyazı (etkin kelime kırmızı), kapanış kesitinde kanal çağrısı
function shortOverlay(g, ts, clip) {
  const S_ = window.SHORT;
  const capY = clip.capY ?? (clip.fit ? 1400 : 1290);
  // kesmeden geçen grup kesmede kısa bir solmayla yeni yerine geçer
  const grNow = S_.GROUPS.find(gr => ts >= gr.s - .05 && ts < gr.e + .15);
  const reIn = grNow && grNow.s < clip.s ? (grNow.e <= clip.s + .03 ? 0 : clamp((ts - clip.s) / .16)) : 1;
  // üst künye: "29 EKİM 1923" + soru (Shorts arayüzü üstte ~120 px'i kapatır)
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
  shBox(g, 150, 150, 780, 200, 7);
  txt(g, '29 EKİM 1923', 540, 262, FONT.title(92), { align: 'center', ls: 3 });
  g.fillStyle = P.red; g.fillRect(200, 284, 680, 8);
  { g.font = FONT.mono(34); g.letterSpacing = '5px'; const tw = g.measureText('KURUCU KADRO NEREDE YETİŞTİ?').width; g.letterSpacing = '0px';
    txt(g, 'KURUCU KADRO NEREDE YETİŞTİ?', 540, 330, FONT.mono(34), { align: 'center', ls: tw > 740 ? 3 : 5 }); }
  g.restore();
  // altyazı
  // en son başlamış grup (bir sonraki başlayınca önceki hemen kalkar); ilk gruptan önce ilk grup görünür
  const groups = S_.GROUPS; let gi = -1;
  for (let k = 0; k < groups.length; k++) if (ts >= groups[k].s - .05) gi = k;
  if (gi < 0) gi = 0; else if (ts >= groups[gi].e + .15) gi = -1;
  if (gi >= 0) {
    const gr = groups[gi], a = (gi === 0 ? 1 : clamp((ts - gr.s + .05) / .12)) * reIn;
    if (a > 0) {
      g.save(); g.letterSpacing = '1px'; g.textAlign = 'left'; g.textBaseline = 'middle';
      const L = shLines(g, gr.words), fs = L.fs, sp = L.sp, lh = fs * 1.28;
      let lines = L.lines;
      if (lines.length > 2) { // sayfa: o an okunan sözcüğün bulunduğu iki satır
        const li = lines.findIndex(ln => ln.some(w => ts < w.e + .05)); const pg = Math.floor(Math.max(0, li < 0 ? lines.length - 1 : li) / 2);
        lines = lines.slice(pg * 2, pg * 2 + 2);
      }
      const bw = Math.min(SH_MAXW, Math.max(...lines.map(ln => ln.reduce((q, w) => q + w.ww, 0) + sp * (ln.length - 1)))) + 70;
      const bh = lines.length * lh + 34;
      let top = capY - (lines.length - 1) * lh / 2 - lh / 2 - 17; top = Math.min(top, SH_BOT - bh);
      const band = PL(rough([[SH_CX - bw / 2, top], [SH_CX + bw / 2, top], [SH_CX + bw / 2, top + bh], [SH_CX - bw / 2, top + bh]], 1.2, gi));
      g.globalAlpha = a; knock(g, band); inkStroke(g, band, 3); // opak kâğıt bant
      lines.forEach((ln, li) => {
        const tw = ln.reduce((q, w) => q + w.ww, 0) + sp * (ln.length - 1);
        let x = SH_CX - tw / 2; const y = top + 17 + lh / 2 + li * lh;
        for (const w of ln) {
          const on = ts >= w.s - .03, cur2 = on && ts < w.e + .05;
          const pop = cur2 ? 1 + .05 * clamp(1 - (ts - w.s) / .15) : 1;
          g.save(); g.translate(x + w.ww / 2, y); g.scale(pop, pop); g.globalAlpha = a; g.textAlign = 'center';
          g.fillStyle = cur2 ? P.red : (on ? P.ink : rgba(P.ink, .66)); g.fillText(shUp(w.w), 0, 0);
          g.restore();
          x += w.ww + sp;
        }
      });
      g.restore();
    }
  }
  // kapanış kesiti (döngü öncesi): tam videoya çağrı; altyazının üstünde, düğme sütununun dışında
  if (clip.cta) {
    const lt = ts - clip.s, q = clamp(lt / .35); g.save(); g.globalAlpha = q;
    const y0 = (clip.fit ? 376 : 950) + 14 * (1 - E.out3(q)); // fit: künye ile kare arasındaki kâğıtta
    shBox(g, 140, y0, 740, clip.fit ? 166 : 180, 11);
    txt(g, 'TAM HİKÂYE', 190, y0 + 86, FONT.title(60), { ls: 2 });
    txt(g, '6 DAKİKALIK VİDEO · AŞAĞIDA', 190, y0 + 140, FONT.mono(32), { ls: 2 });
    // çizilmiş aşağı ok (x 800, y 1000–1090), hafifçe zıplar
    const bob = 6 * Math.sin(lt * TAU * .9), ar = PL([[800, y0 + 50 + bob], [800, y0 + 130 + bob]], false);
    inkStroke(g, ar, 6); inkStroke(g, PL([[776, y0 + 106 + bob], [800, y0 + 134 + bob], [824, y0 + 106 + bob]], false), 6);
    g.fillStyle = P.red; g.fillRect(190, y0 + 100, 330 * E.out3(clamp(lt / .8)), 6);
    g.restore();
  }
}
window.renderShortFrame = renderShortFrame;
