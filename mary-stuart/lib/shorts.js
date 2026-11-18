// Shorts (Mary Stuart): filmden kesitler (shorts/edl.json), dikey 1080×1920. Kare: film kadrajının ortası (810×1080 → 1080×1440).
// Üstte kanca yazısı (kapak B'nin sözü, ilk saniyeden), altta sözcük vurgulu altyazı; sonda kanal kartı.
'use strict';
let EDL = null; fetch('shorts/edl.json').then(r => r.json()).then(j => { EDL = j; });
const SC = document.getElementById('s'), sg = SC.getContext('2d');
const ALT = {}; fetch('senaryo.json').then(r => r.json()).then(j => { for (const s of j.segments) ALT[s.id] = s.alt; });
const ALTID = id => id.replace(/k$/, '');
function shortsYazi(t, k) {   // sözcük vurgulu altyazı: alt metnin sözcükleri ↔ kelime zamanları (sıra ile)
  if (/k$/.test(k.id)) return;   // ilk saniye (kırmızı): yalnız kanca yazısı
  const toks = (ALT[ALTID(k.id)] || '').split(/\s+/).filter(Boolean), ws = WORDS.filter(w => w.id === ALTID(k.id)); if (!toks.length) return;
  const src = k.src0 + (t - k.t0), n = Math.min(toks.length, ws.length); let cur = -1; for (let i = 0; i < n; i++) if (ws[i].s <= src) cur = i;
  if (cur < 0) return; const parts = []; let p = [], len = 0;
  for (let i = 0; i < n; i++) { if (len + toks[i].length > 18 && p.length) { parts.push(p); p = []; len = 0; } p.push(i); len += toks[i].length + 1; if (/[.?!:]$/.test(toks[i])) { parts.push(p); p = []; len = 0; } }
  if (p.length) parts.push(p); const grp = parts.find(q => q.includes(cur)); if (!grp) return;
  sg.font = '700 58px "Cinzel"'; sg.textAlign = 'left'; sg.textBaseline = 'middle'; const txt = grp.map(i => toks[i]).join(' '), w = sg.measureText(txt).width, x0 = 540 - w / 2, y = 1500;
  sg.fillStyle = 'rgba(10,9,8,.72)'; sg.fillRect(x0 - 30, y - 56, w + 60, 112);
  let x = x0; for (const i of grp) { const s2 = toks[i] + ' '; sg.fillStyle = i === cur ? '#f6efe0' : 'rgba(236,229,213,.55)'; sg.fillText(s2, x, y); x += sg.measureText(s2).width; }
}
window.renderShortFrame = t => {
  sg.setTransform(1, 0, 0, 1, 0, 0); sg.fillStyle = '#0b0a09'; sg.fillRect(0, 0, 1080, 1920);
  if (!EDL) return SC;
  const k = EDL.kesit.slice().reverse().find(x => t >= x.t0);
  if (t < EDL.son.t0 && k) {
    const src = k.src0 + (t - k.t0), fc = renderFrame(src);
    sg.drawImage(fc, 240 + 315, 0, 810, 1080, 0, 330, 1080, 1440);
    const vg = sg.createLinearGradient(0, 330, 0, 1770); vg.addColorStop(0, 'rgba(11,10,9,.9)'); vg.addColorStop(.12, 'rgba(11,10,9,0)'); vg.addColorStop(.85, 'rgba(11,10,9,0)'); vg.addColorStop(1, 'rgba(11,10,9,.95)'); sg.fillStyle = vg; sg.fillRect(0, 330, 1080, 1440);
    shortsYazi(t, k);
  } else {
    const u = clamp((t - EDL.son.t0) / .6); sg.globalAlpha = u; sg.textAlign = 'center'; sg.textBaseline = 'middle';
    sg.fillStyle = '#ece5d5'; sg.font = '400 120px "Bebas Neue"'; sg.fillText('KALBİNLE Mİ,', 540, 820); sg.fillText('AKLINLA MI?', 540, 950);
    sg.font = 'italic 600 52px "Cormorant Garamond"'; sg.fillText('Tam hikâye kanalda: Mary Stuart ve I. Elizabeth', 540, 1110);
    sg.font = '700 40px "Cinzel"'; sg.fillStyle = 'rgba(236,229,213,.8)'; sg.fillText('ZAMAN KURYESİ', 540, 1240); sg.globalAlpha = 1;
  }
  // kanca (kapak B'nin sözü) ilk kesit boyunca; sonra künye
  sg.textAlign = 'center'; sg.textBaseline = 'alphabetic';
  if (t < EDL.son.t0) {
    if (t < EDL.kesit[2].t0) { sg.font = '400 128px "Bebas Neue"'; sg.fillStyle = '#ece5d5'; sg.fillText('İDAMINA', 540, 150); sg.fillStyle = 'rgb(206,34,40)'; sg.fillText('KIRMIZI GİYDİ', 540, 285); }
    else { sg.font = '700 44px "Cinzel"'; sg.fillStyle = '#ece5d5'; sg.fillText('MARY STUART', 540, 140); sg.font = 'italic 600 40px "Cormorant Garamond"'; sg.fillStyle = 'rgba(236,229,213,.85)'; sg.fillText('Fotheringhay · 8 Şubat 1587', 540, 200); }
  }
  return SC;
};
window.ready.then(async () => { while (!EDL || !Object.keys(ALT).length) await new Promise(r => setTimeout(r, 50)); await document.fonts.load('400 120px "Bebas Neue"', 'İDAMINKRZGY'); window.SHORTS_HAZIR = true; window.READY = true; });
