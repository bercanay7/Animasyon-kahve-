// İkaros Shorts: film karelerinden 9:16 kesit (shorts.html?rs=2&notext=1) + başlık, kanca, kelime vurgulu altyazı, kanal çağrısı.
'use strict';
const SHW = 1080, SHH = 1920, SH_INK = '#1E3B3F', SH_PAPER = '#F3E6CC', SH_ACC = '#F2B27A';
const shortCv = makeCanvas(SHW, SHH), shx = shortCv.getContext('2d');
function shTxt(g, s, x, y, px, col, o = {}) { g.save(); g.font = `400 ${px}px "Bebas Neue"`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.letterSpacing = (o.ls ?? 3) + 'px';
  if (o.maxW) while (g.measureText(s).width > o.maxW && px > 30) { px -= 2; g.font = `400 ${px}px "Bebas Neue"`; }
  if (o.stroke) { g.lineWidth = o.sw || 14; g.lineJoin = 'round'; g.strokeStyle = o.stroke; g.strokeText(s, x, y); } g.fillStyle = col; g.fillText(s, x, y); g.restore(); }
function renderShortFrame(ts, mb = 1) {
  const S_ = window.SHORT, E_ = S_.EDL; let i = 0; for (let k = 0; k < E_.length; k++) if (E_[k].s <= ts) i = k;
  const c = E_[i], u = clamp((ts - c.s) / (c.e - c.s)), tf = c.f + (ts - c.s);
  renderFrame(tf);
  const z = lerp(c.z0, c.z1, E.io2(u)), cx = lerp(c.cx0, c.cx1, E.io2(u)), cw = H * 9 / 16 / z, ch = H / z;
  const x0 = clamp(cx - cw / 2, 0, W - cw), y0 = clamp(H / 2 - ch / 2, 0, H - ch);
  shx.setTransform(1, 0, 0, 1, 0, 0); shx.imageSmoothingQuality = 'high';
  shx.drawImage(document.getElementById('c'), x0 * RS, y0 * RS, cw * RS, ch * RS, 0, 0, SHW, SHH);
  shortOverlay(shx, ts);
  return shortCv;
}
function shortOverlay(g, ts) {
  const S_ = window.SHORT;
  // üst bant (bilgi bandı gibi düz mürekkep): başlık
  g.fillStyle = SH_INK; g.fillRect(0, 0, SHW, 170); g.fillStyle = SH_ACC; g.fillRect(0, 170, SHW, 8);
  shTxt(g, S_.TITLE, 500, 92, 74, SH_PAPER, { ls: 8, maxW: 820 });
  // kanca: ilk kesit boyunca, kapak A ile aynı söz
  if (ts < S_.HOOK.e) { shTxt(g, S_.HOOK.l1, 500, 420, 190, SH_INK, { ls: 4, stroke: SH_PAPER, sw: 18 }); shTxt(g, S_.HOOK.l2, 500, 590, 190, SH_INK, { ls: 4, stroke: SH_PAPER, sw: 18 }); }
  // altyazı: grup, etkin kelime vurgu renginde; x 100–900 (sağdaki düğme sütunu boş)
  const gr = S_.GROUPS.find(q => ts >= q.s - .05 && ts < q.e + .2);
  if (gr) {
    g.save(); g.font = '400 104px "Bebas Neue"'; g.letterSpacing = '3px'; g.textBaseline = 'middle'; g.textAlign = 'left';
    const ws = gr.words.map(x => ({ ...x, T: x.w.toLocaleUpperCase('tr') })); ws.forEach(x => x.ww = g.measureText(x.T).width);
    const sp = 28, lines = []; let cur = [], cw = 0;
    for (const x of ws) { if (cur.length && cw + sp + x.ww > 800) { lines.push(cur); cur = []; cw = 0; } cur.push(x); cw += (cur.length > 1 ? sp : 0) + x.ww; } if (cur.length) lines.push(cur);
    const y0 = 1330 - (lines.length - 1) * 60;
    lines.forEach((ln, li) => { const tw = ln.reduce((q, x) => q + x.ww, 0) + sp * (ln.length - 1); let x = 500 - tw / 2;
      for (const wd of ln) { const on = ts >= wd.s - .03, cur2 = on && ts < wd.e + .05; g.lineWidth = 16; g.lineJoin = 'round'; g.strokeStyle = SH_INK; g.strokeText(wd.T, x, y0 + li * 120);
        g.fillStyle = cur2 ? SH_ACC : on ? SH_PAPER : 'rgba(243,230,204,.7)'; g.fillText(wd.T, x, y0 + li * 120); x += wd.ww + sp; } });
    g.restore();
  }
  // kanal çağrısı
  if (ts > S_.CTA) { const q = clamp((ts - S_.CTA) / .3); g.save(); g.globalAlpha = q; g.fillStyle = SH_INK; g.fillRect(100, 1530, 800, 120); shTxt(g, 'TAM HİKÂYE KANALDA', 470, 1592, 64, SH_PAPER, { ls: 4 }); g.fillStyle = SH_ACC; g.beginPath(); g.moveTo(800, 1575); g.lineTo(840, 1575); g.lineTo(820, 1605); g.closePath(); g.fill(); g.restore(); }
}
window.renderShortFrame = renderShortFrame;
