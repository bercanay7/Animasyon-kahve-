// Dikey Shorts kurgusu: film karelerinden kesitler (EDL), 9:16 kırpma ve kelime kelime altyazı.
// Milton uyarlaması (gravür): shorts.html?rs=2&notext=1 ile; window.SHORT = { EDL, WORDS, DUR } (shorts/edl.js)
'use strict';
function stx(g, s, x, y, o = {}) {
  g.save(); g.font = o.font; g.textAlign = 'center'; g.textBaseline = 'middle'; if (o.ls) g.letterSpacing = o.ls + 'px';
  if (o.maxW) { let px = +o.font.match(/(\d+)px/)[1]; while (g.measureText(s).width > o.maxW && px > 20) { px -= 2; g.font = o.font.replace(/\d+px/, px + 'px'); } }
  g.globalAlpha *= (o.a ?? 1);
  if (o.shadow) { g.shadowColor = o.shadow; g.shadowBlur = o.blur || 10; }
  if (o.stroke) { g.lineWidth = o.sw || 10; g.lineJoin = 'round'; g.strokeStyle = o.stroke; g.strokeText(s, x, y); }
  g.shadowBlur = 0; g.fillStyle = o.col || '#F3EBDD'; g.fillText(s, x, y); g.restore();
}
const INK = '#16120E', KAGIT = '#F1E9DA', VURGU = '#9E2B1E';
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
  shx.setTransform(1, 0, 0, 1, 0, 0); shx.globalAlpha = 1;
  shx.imageSmoothingQuality = 'high';
  shx.drawImage(document.getElementById('c'), x0 * RS, y0 * RS, cw * RS, ch * RS, 0, 0, SHW, SHH);
  // kesmede kısa beyaz parlama (isteğe bağlı)
  if (c.flash) { const f = clamp(1 - (ts - c.s) / .18); if (f > 0) { shx.fillStyle = `rgba(255,240,215,${f * .55})`; shx.fillRect(0, 0, SHW, SHH); } }
  shortOverlay(shx, ts);
  return shortCv;
}
// üst/alt vazo şeritleri, başlık ve altyazı
// satır bölme: tek satıra sığmıyorsa iki satırın genişlik farkını en aza indiren bölme (üç ve üstü satırda açgözlü)
function shortLines(words, sp, maxW) {
  const tot = words.reduce((q, w) => q + w.ww, 0) + sp * (words.length - 1);
  if (tot <= maxW) return [words];
  let best = null, bw = 1e9;
  for (let k = 1; k < words.length; k++) {
    const a = words.slice(0, k), b = words.slice(k);
    const wa = a.reduce((q, w) => q + w.ww, 0) + sp * (a.length - 1), wb = b.reduce((q, w) => q + w.ww, 0) + sp * (b.length - 1);
    if (wa <= maxW && wb <= maxW && Math.max(wa, wb) < bw) { bw = Math.max(wa, wb); best = [a, b]; }
  }
  if (best) return best;
  const lines = []; let cur = [], wsum = 0;
  for (const w of words) { if (cur.length && wsum + sp + w.ww > maxW) { lines.push(cur); cur = []; wsum = 0; } cur.push(w); wsum += (cur.length > 1 ? sp : 0) + w.ww; }
  if (cur.length) lines.push(cur);
  return lines;
}
function shortOverlay(g, ts) {
  const S_ = window.SHORT, ci = Math.max(0, S_.EDL.findIndex(c => ts >= c.s && ts < c.e)), clip = S_.EDL[ci] || {}, prev = S_.EDL[ci - 1];
  const CX = 500, MAXW = 800;   // altyazı x 100–900: sağdaki Shorts düğme sütununa (x ≈ 930) 30 px pay
  const grNow = S_.GROUPS.find(gr => ts >= gr.s - .05 && ts < gr.e + .15);
  const capY = clip.capY ?? 1235, ctaY = clip.ctaY ?? 1330;
  // kesitten geçen grup yalnız altyazının yeri ya da zemin türü değişince kısa bir solmayla yeniden belirir;
  // aynı yerde süren kesitlerde (görüntüde kesme yokken) yazı yanıp sönmez (Shorts kurulu tur 1)
  const moved = !!prev && ((prev.capY ?? 1235) !== capY || !!prev.light !== !!clip.light);
  const reIn = moved && grNow && grNow.s < clip.s ? (grNow.e <= clip.s + .03 ? 0 : clamp((ts - clip.s) / .16)) : 1;
  const light = !!clip.light;
  // açık zeminde YouTube'un beyaz arayüz yazıları (başlık, kanal adı) okunsun: altta hafif koyu geçiş
  if (light) {
    const gb = g.createLinearGradient(0, 1480, 0, SHH); gb.addColorStop(0, 'rgba(20,10,5,0)'); gb.addColorStop(1, 'rgba(20,10,5,.55)'); g.fillStyle = gb; g.fillRect(0, 1480, SHW, SHH - 1480);
  }
  // üst şerit + başlık
  const top = g.createLinearGradient(0, 0, 0, 300); top.addColorStop(0, 'rgba(12,8,5,.9)'); top.addColorStop(.7, 'rgba(12,8,5,.55)'); top.addColorStop(1, 'rgba(12,6,4,0)');
  g.fillStyle = top; g.fillRect(0, 0, SHW, 300);
  g.strokeStyle = 'rgba(241,233,218,.8)'; g.lineWidth = 2; g.strokeRect(60, 70, 840, 0.01); g.strokeRect(60, 206, 840, 0.01);
  const tOff = (S_.TITLE_OFF || []).reduce((m, o) => Math.max(m, clamp((ts - o.s) / .25) * (1 - clamp((ts - o.e) / .25))), 0);
  if (tOff < 1) stx(g, S_.TITLE || 'MILTON', 480, 140, { a: 1 - tOff, font: '700 52px Cinzel', col: KAGIT, ls: 8, maxW: 780, force: true, shadow: 'rgba(0,0,0,.6)', blur: 12 });
  // künye: başlığın altında; filmde silinen Erhat künyesi ve adların karşılığı (kim konuşuyor, kaynak sayfa)
  const tq = (S_.TAGS || []).map(tg => clamp((ts - tg.s) / .25) * (1 - clamp((ts - tg.e) / .25)));
  const tqMax = Math.max(0, ...tq);
  if (tqMax > 0) {
    g.save(); g.globalAlpha = tqMax; g.fillStyle = 'rgba(12,6,4,.85)'; g.fillRect(60, 188, 840, 56); g.restore();
    S_.TAGS.forEach((tg, i) => { if (tq[i] > 0) { g.save(); g.globalAlpha = tq[i]; stx(g, tg.t, 480, 217, { font: '700 36px Cinzel', col: KAGIT, ls: 3, force: true }); g.restore(); } });
  }
  // kanca: ilk karede soru (ses kapalı izleyen için), anlatımda cevap başlayınca söner
  if (S_.HOOK && ts < S_.HOOK.e + .3) {
    const q = 1 - clamp((ts - S_.HOOK.e) / .3);
    g.save(); g.globalAlpha = q;
    const hb = g.createLinearGradient(0, 170, 0, 560); hb.addColorStop(0, 'rgba(12,6,4,0)'); hb.addColorStop(.2, 'rgba(12,6,4,.55)'); hb.addColorStop(.85, 'rgba(12,6,4,.55)'); hb.addColorStop(1, 'rgba(12,6,4,0)');
    g.fillStyle = hb; g.fillRect(0, 170, SHW, 390);
    stx(g, S_.HOOK.l1, 540, 285, { font: '900 150px Cinzel', col: KAGIT, ls: 4, maxW: 960, force: true, stroke: 'rgba(14,9,7,.92)', sw: 14, shadow: 'rgba(0,0,0,.7)', blur: 18 });
    stx(g, S_.HOOK.l2, 540, 425, { font: '900 170px Cinzel', col: '#E9B44C', ls: 6, maxW: 960, force: true, stroke: 'rgba(14,9,7,.92)', sw: 16, shadow: 'rgba(0,0,0,.7)', blur: 18 });
    g.restore();
  }
  // damga: filmdeki ZEUS · KÖLE / PROMETHEUS · ÖZGÜR levhası (notext ile silinir); dikey kadrajın üstünde
  const st = S_.STAMP;
  if (st && ts >= st.s - .05 && ts < st.e) {
    const q = clamp((ts - st.s) / .2), q2 = clamp((ts - st.s2) / .3);
    // kutu ikinci satırla büyür; alt kenar y 440 (doruk planında Prometheus'un başı y ≈ 490)
    const bh = 110 + 72 * E.io2(q2);
    g.save(); g.globalAlpha = q; g.fillStyle = 'rgba(12,6,4,.7)'; g.fillRect(100, 258, 800, bh); g.strokeStyle = VURGU; g.lineWidth = 4; g.strokeRect(100, 258, 800, bh);
    stx(g, 'ZEUS · KÖLE', 500, 314, { font: '800 66px Cinzel', col: '#CFC6B8', ls: 6, force: true });
    g.globalAlpha = q * q2; stx(g, 'PROMETHEUS · ÖZGÜR', 500, 396, { font: '800 48px Cinzel', col: '#F2C25A', ls: 4, force: true });
    g.restore();
  }
  // altyazı bandı (parlak karelerde okunurluk); açık zeminde zemin renginde yumuşak bant (arkadan geçen zincir yazıyı bölmesin)
  const gd = S_.GROUPS.reduce((m, gr) => Math.min(m, ts < gr.s ? gr.s - ts : ts > gr.e + .15 ? ts - gr.e - .15 : 0), 1e9);
  const bandA = 1 - clamp((gd - .1) / .3);
  const bc = '12,6,4', ba = 0 * bandA;   // Milton: bantsız (gri leke)
  const cb = g.createLinearGradient(0, capY - 215, 0, capY + 205); cb.addColorStop(0, `rgba(${bc},0)`); cb.addColorStop(.3, `rgba(${bc},${ba})`); cb.addColorStop(.75, `rgba(${bc},${ba})`); cb.addColorStop(1, `rgba(${bc},0)`);
  g.fillStyle = cb; g.fillRect(0, capY - 215, SHW, 420);
  // altyazı: anlam birimi grupları, etkin kelime altın
  const groups = S_.GROUPS, gi0 = groups.findIndex(gr => ts >= gr.s - .05 && ts < gr.e + .15), gi = gi0 < 0 && ts < groups[0].s ? 0 : gi0;
  if (gi >= 0) {
    // ilk grup ilk karede tam görünür (Shorts önizleme karesi)
    const gr = groups[gi], a = (gi === 0 ? 1 : clamp((ts - gr.s + .05) / .12)) * reIn;
    g.save(); g.font = '900 80px Cinzel'; g.letterSpacing = '2px'; g.textAlign = 'left'; g.textBaseline = 'middle';
    // kelime arası boşluk + 16 px: etkin kelime büyüyüp kontur kalınlaşınca komşusuna yapışmasın
    const GAP = 16;
    // tek satıra az farkla sığmayan kısa grup bölünmesin: yazı biraz küçülür
    { const tot = g.measureText(gr.words.map(w => w.w.toLocaleUpperCase('tr')).join(' ')).width + GAP * (gr.words.length - 1); if (tot > MAXW && tot < MAXW / .86) g.font = `900 ${Math.floor(84 * MAXW / tot)}px Cinzel`; }
    let sp = g.measureText(' ').width + GAP, ws = gr.words.map(w => ({ ...w, ww: g.measureText(w.w.toLocaleUpperCase('tr')).width }));
    // iki satıra az farkla sığmayan grup üçe bölünmesin ("GÖRÜNMEYEN / YARGIÇ / TUTSAK."): yazı biraz küçülür
    if (ws.length > 1 && shortLines(ws, sp, MAXW).length > 2) {
      let bw = 1e9;
      for (let k = 1; k < ws.length; k++) { const w2 = [ws.slice(0, k), ws.slice(k)].map(l => l.reduce((q, w) => q + w.ww, 0) + sp * (l.length - 1)); bw = Math.min(bw, Math.max(...w2)); }
      if (bw < MAXW / .86) {
        let px = parseFloat(g.font.match(/(\d+)px/)[1]);
        while (shortLines(ws, sp, MAXW).length > 2 && px > 60) { px -= 2; g.font = `900 ${px}px Cinzel`; sp = g.measureText(' ').width + GAP; ws = ws.map(w => ({ ...w, ww: g.measureText(w.w.toLocaleUpperCase('tr')).width })); }
      }
    }
    const lines = shortLines(ws, sp, MAXW);
    const y0 = capY - (lines.length - 1) * 54;
    lines.forEach((ln, li) => {
      const tw = ln.reduce((q, w) => q + w.ww, 0) + sp * (ln.length - 1);
      let x = CX - tw / 2;
      for (const w of ln) {
        const on = ts >= w.s - .03, cur2 = on && ts < w.e + .05;
        const pop = cur2 ? 1 + .06 * clamp(1 - (ts - w.s) / .15) : 1;
        g.save(); g.translate(x + w.ww / 2, y0 + li * 104); g.scale(pop, pop); g.globalAlpha = a;
        g.lineWidth = 20; g.strokeStyle = light ? 'rgba(246,236,214,.95)' : 'rgba(15,7,4,.9)'; g.lineJoin = 'round'; g.textAlign = 'center';
        const T = w.w.toLocaleUpperCase('tr');
        g.strokeText(T, 0, 0);
        g.fillStyle = light ? (cur2 ? VURGU : (on ? '#1E1611' : 'rgba(30,22,17,.62)')) : (cur2 ? '#E9B44C' : (on ? '#FFF6E6' : 'rgba(255,246,230,.8)')); g.fillText(T, 0, 0);
        g.restore();
        x += w.ww + sp;
      }
    });
    g.restore();
  }
  // son: kanal çağrısı (açık bırakılan merak + İlgili video bağlantısına işaret eden ok)
  const ce = S_.CTA ?? 1e9, L = S_.CTA_L || ['TAM HİKÂYE KANALDA'];
  if (ts > ce) {
    const q = clamp((ts - ce) / .4), h = L.length > 1 ? 150 : 110;
    g.save(); g.globalAlpha = q; g.fillStyle = 'rgba(12,6,4,.74)'; g.fillRect(100, ctaY, 800, h); g.strokeStyle = VURGU; g.lineWidth = 4; g.strokeRect(100, ctaY, 800, h);
    if (L.length > 1) {
      stx(g, L[0], CX, ctaY + 52, { font: '900 40px Cinzel', col: '#E9B44C', maxW: 760, ls: 2, force: true });
      stx(g, L[1], CX - 22, ctaY + 108, { font: '700 36px Cinzel', col: KAGIT, ls: 3, force: true });
      // aşağı ok: Shorts arayüzünde başlığın üstündeki "İlgili video" bağlantısı
      const ax = CX + 330, ay = ctaY + 96; g.fillStyle = KAGIT; g.beginPath(); g.moveTo(ax - 14, ay); g.lineTo(ax + 14, ay); g.lineTo(ax, ay + 22); g.closePath(); g.fill();
    } else stx(g, L[0], CX, ctaY + 56, { font: '700 46px Cinzel', col: '#F6E3BE', ls: 4, force: true });
    g.restore();
  }
}
window.renderShortFrame = renderShortFrame;
