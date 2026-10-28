// Dikey Shorts kurgusu: film karelerinden kesitler (EDL), 9:16 kırpma ve kelime kelime altyazı (taş baskı üslubu).
// shorts.html?rs=2&notext=1 ile; window.SHORT = { EDL, GROUPS, CTA, DUR } (shorts/edl.js)
'use strict';
const SHW = 1080, SHH = 1920;
const shortCv = makeCanvas(SHW, SHH), shx = shortCv.getContext('2d');
// YouTube Shorts arayüzü: üstte ~120 px, altta ~%25 ve sağda düğme sütunu kapanır → yazılar x ≤ 930, y ≤ 1420
const SH_CX = 492, SH_MAXW = 820, SH_PAD = 28, SH_BOT = 1420; // bant: metin + 2×28 → x 54–930
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
// altyazı (tipografi kurulu 2. tur): punto sabit 66 px; gruplar en çok 2 satıra sığacak biçimde ölçülerek kurulur
const SH_FS = 66;
function shMeasure(g) { g.font = FONT.slab(SH_FS); g.letterSpacing = '1px'; return { sp: g.measureText(' ').width, wd: w => g.measureText(shUp(w)).width }; }
// iki satıra dengeli bölme: iki satır da ≤ SH_MAXW, genişlik farkı en az; noktalama sonrası kırılım ödüllü
function shBreak(ws, sp) {
  const tot = ws.reduce((q, w) => q + w.ww, 0) + sp * (ws.length - 1);
  if (tot <= SH_MAXW || ws.length < 2) return tot <= SH_MAXW ? [ws] : null;
  let best = null, bc = 1e9;
  for (let k = 1; k < ws.length; k++) {
    const a = ws.slice(0, k), b = ws.slice(k), wa = a.reduce((q, w) => q + w.ww, 0) + sp * (a.length - 1), wb = tot - wa - sp;
    if (wa > SH_MAXW || wb > SH_MAXW) continue;
    const L = a[a.length - 1], R = b[0], name = !/[,.:;!?…]$/.test(L.w) && /^[A-ZÇĞİÖŞÜ“]/.test(L.w) && /^[A-ZÇĞİÖŞÜ]/.test(R.w);
    const c = Math.abs(wa - wb) - (/[,.:;!?…”]$/.test(L.w) ? 200 : 0) + (name ? 600 : 0); // satır adın ortasından kırılmaz
    if (c < bc) { bc = c; best = [a, b]; }
  }
  return best;
}
// grupları yeniden kur (tipografi kurulu 2. tur): akış önce kesit sınırlarında ve cümle sonlarında (. ! ? … : ”) öbeklere
// bölünür; öbek 2 satıra sığmıyorsa en az sayıda gruba, en dengeli biçimde bölünür. Ceza: 0,6 sn'den kısa grup,
// bağlaçla ya da "bir" ile biten grup, iki büyük harfli sözcük (ad) arasından bölmek; ödül: virgülden sonra bölmek.
function shRegroup(g) {
  const S_ = window.SHORT; if (S_._rg) return; S_._rg = 1;
  const { sp, wd } = shMeasure(g), clipOf = t => S_.EDL.findIndex(c => t >= c.s - .01 && t < c.e);
  const words = S_.GROUPS.flatMap(gr => gr.words).map(w => ({ ...w, ww: wd(w.w) }));
  const phrases = []; let cur = [];
  for (const w of words) {
    if (cur.length && clipOf(w.s) !== clipOf(cur[0].s)) { phrases.push(cur); cur = []; }
    cur.push(w);
    if (/[.!?…:”]$/.test(w.w)) { phrases.push(cur); cur = []; }
  }
  if (cur.length) phrases.push(cur);
  const weak = w => /^(bir|ve|ile|de|da|bu|ki|ama|ise)$/i.test(w.w);
  const out = [];
  for (const ph of phrases) {
    let best = null, bc = 1e9;
    for (let k = 1; k <= Math.min(4, ph.length) && !best; k++) {
      const rec = (start, left, acc) => {
        if (left === 1) {
          const gw = ph.slice(start); if (!shBreak(gw, sp)) return;
          const parts = [...acc, gw];
          const c = parts.reduce((q, p, j) => q + (p[p.length - 1].e - p[0].s < .6 && parts.length > 1 ? 100 + (p.length === 1 && /[.!?…:]$/.test(p[0].w) ? 30 : 0) : 0) + (j < parts.length - 1 && weak(p[p.length - 1]) ? 60 : 0) - (j < parts.length - 1 && /,$/.test(p[p.length - 1].w) ? 15 : 0), 0)
            + (parts.length > 1 ? Math.abs(parts[0].length - parts[parts.length - 1].length) * 3 : 0)
            + parts.slice(1).reduce((q, p, j) => { const L = parts[j][parts[j].length - 1]; return q + (L !== ph[0] && !/[,.:;!?…]$/.test(L.w) && /^[A-ZÇĞİÖŞÜ]/.test(L.w) && /^[A-ZÇĞİÖŞÜ]/.test(p[0].w) ? 150 : 0); }, 0); // ad bölünmez (Mustafa | Kemal); cümle başındaki büyük harf sayılmaz
          if (c < bc) { bc = c; best = parts; }
          return;
        }
        for (let e = start + 1; e <= ph.length - left + 1; e++) { const gw = ph.slice(start, e); if (shBreak(gw, sp)) rec(e, left - 1, [...acc, gw]); }
      };
      rec(0, k, []);
    }
    for (const gw of best || [ph]) out.push({ s: gw[0].s, e: gw[gw.length - 1].e, words: gw });
  }
  for (let i = 0; i < out.length - 1; i++) out[i].e = Math.min(out[i].e + .25, out[i + 1].s - .02);
  S_.GROUPS = out;
}
function shLines(g, words) {
  const { sp, wd } = shMeasure(g), ws = words.map(w => ({ ...w, ww: wd(w.w) }));
  return { lines: shBreak(ws, sp) || [ws], fs: SH_FS, sp };
}
// üst künye, altyazı (etkin kelime kırmızı), kapanış kesitinde kanal çağrısı
function shortOverlay(g, ts, clip) {
  const S_ = window.SHORT; shRegroup(g);
  const capY = clip.capY ?? (clip.fit ? 1400 : 1290);
  // kesmeden geçen grup kesmede kısa bir solmayla yeni yerine geçer
  const grNow = S_.GROUPS.find(gr => ts >= gr.s - .05 && ts < gr.e + .15);
  const reIn = grNow && grNow.s < clip.s ? (grNow.e <= clip.s + .03 ? 0 : clamp((ts - clip.s) / .16)) : 1;
  // üst künye: "29 EKİM 1923" + soru (Shorts arayüzü üstte ~120 px'i kapatır)
  g.save(); g.setTransform(1, 0, 0, 1, 0, 0);
  shBox(g, 110, 150, 860, 210, 7);
  txt(g, '29 EKİM 1923', 540, 262, FONT.title(92), { align: 'center', ls: 3 });
  g.fillStyle = P.red; g.fillRect(200, 284, 680, 8);
  { g.font = FONT.mono(42); g.letterSpacing = '2px'; const tw = g.measureText('KURUCU KADRO NEREDE YETİŞTİ?').width; g.letterSpacing = '0px';
    txt(g, 'KURUCU KADRO NEREDE YETİŞTİ?', 540, 334, FONT.mono(tw > 820 ? Math.floor(42 * 820 / tw) : 42), { align: 'center', ls: 2 }); }
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
      const lines = L.lines;
      const bw = Math.min(SH_MAXW, Math.max(...lines.map(ln => ln.reduce((q, w) => q + w.ww, 0) + sp * (ln.length - 1)))) + 2 * SH_PAD;
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
    txt(g, '6 DAKİKALIK VİDEO · AŞAĞIDA', 190, y0 + 142, FONT.mono(38), { ls: 1 });
    // çizilmiş aşağı ok (x 800, y 1000–1090), hafifçe zıplar
    // ok başlık satırının sağında, alt satıra inmez (tipografi: "AŞAĞIDA" ile çakışmasın)
    const bob = 4 * Math.sin(lt * TAU * .9), ar = PL([[800, y0 + 30 + bob], [800, y0 + 92 + bob]], false);
    inkStroke(g, ar, 6); inkStroke(g, PL([[778, y0 + 70 + bob], [800, y0 + 96 + bob], [822, y0 + 70 + bob]], false), 6);
    g.fillStyle = P.red; g.fillRect(190, y0 + 100, 330 * E.out3(clamp(lt / .8)), 6);
    g.restore();
  }
}
window.renderShortFrame = renderShortFrame;
