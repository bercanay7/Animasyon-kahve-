// Dikey Shorts kurgusu: film karelerinden kesitler (EDL), 9:16 kırpma ve kelime kelime altyazı.
// film.html?shorts=1&rs=2&notext=1 ile; window.SHORT = { EDL, WORDS, DUR } (shorts/edl.js)
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
  shx.setTransform(1, 0, 0, 1, 0, 0); shx.globalAlpha = 1;
  shx.imageSmoothingQuality = 'high';
  shx.drawImage(document.getElementById('c'), x0 * RS, y0 * RS, cw * RS, ch * RS, 0, 0, SHW, SHH);
  // kesmede kısa beyaz parlama (isteğe bağlı)
  if (c.flash) { const f = clamp(1 - (ts - c.s) / .18); if (f > 0) { shx.fillStyle = `rgba(255,240,215,${f * .55})`; shx.fillRect(0, 0, SHW, SHH); } }
  shortOverlay(shx, ts);
  return shortCv;
}
// üst/alt vazo şeritleri, başlık ve altyazı
function shortOverlay(g, ts) {
  const S_ = window.SHORT, clip = S_.EDL.find(c => ts >= c.s && ts < c.e) || {};
  // capAt: kesit içinde altyazının yer değiştirdiği an (ör. kitap belirince boş kapak alanına iner)
  // altyazı yeri kesitin kendi yeridir; kesmeden geçen grup kesmede kısa bir solmayla yeni yerine geçer (kayarak zıplamaz, yeni kadrajda yüze binmez)
  const grNow = S_.GROUPS.find(gr => ts >= gr.s - .05 && ts < gr.e + .15);
  // capAt: altyazı kesit içinde yer değiştirir; yazıların üstünden kayarak geçmez, söner ve yeni yerinde belirir
  const capY = clip.capAt != null && ts >= clip.capAt ? clip.capY2 : (clip.capY ?? 1235), ctaY = clip.ctaY ?? 1330;
  const reIn = (grNow && grNow.s < clip.s ? (grNow.e <= clip.s + .03 ? 0 : clamp((ts - clip.s) / .16)) : 1) * (clip.capAt != null ? clamp(Math.abs(ts - clip.capAt) / .1) : 1);
  // üst şerit + başlık
  const top = g.createLinearGradient(0, 0, 0, 300); top.addColorStop(0, 'rgba(12,6,4,.75)'); top.addColorStop(1, 'rgba(12,6,4,0)');
  g.fillStyle = top; g.fillRect(0, 0, SHW, 300);
  meanderSaltire(g, -40, SHW + 40, 34, 40, PC.clayR, 'rgba(12,6,4,.0)');
  txt(g, window.SHORT.TITLE || 'PROMETHEUS', SHW / 2, 140, { font: '900 64px Cinzel', col: '#F6E3BE', ls: 14, force: true, shadow: 'rgba(0,0,0,.6)', blur: 12 });
  // altyazı bandı (parlak karelerde okunurluk)
  // YouTube Shorts arayüzü (başlık, kanal, düğmeler) alt ~%25'i ve sağ kenarı kapatır: altyazı 1080–1400 aralığında
  // açık zeminli (beyaz zemin, Camus) kesitlerde koyu bant yerine mürekkep renkli yazı + krem kontur (gri leke kalmaz)
  const light = !!clip.light;
  // açık zeminde de yazının arkasından geçen çizgiler (zincir, ip) yazıyı bölmesin: zemin renginde yumuşak bant
  const bc = light ? '246,236,214' : '12,6,4', ba = light ? .72 : .55;
  const cb = g.createLinearGradient(0, capY - 215, 0, capY + 205); cb.addColorStop(0, `rgba(${bc},0)`); cb.addColorStop(.3, `rgba(${bc},${ba})`); cb.addColorStop(.75, `rgba(${bc},${ba})`); cb.addColorStop(1, `rgba(${bc},0)`);
  g.fillStyle = cb; g.fillRect(0, capY - 215, SHW, 420);
  // altyazı: kelime grupları, etkin kelime altın
  const groups = S_.GROUPS, gi0 = groups.findIndex(gr => ts >= gr.s - .05 && ts < gr.e + .15), gi = gi0 < 0 && ts < groups[0].s ? 0 : gi0;
  if (gi >= 0) {
    // ilk grup ilk karede tam görünür (Shorts önizleme karesi); kanal çağrısı levhası gelince aynı metinli altyazı söner (çift yazı olmaz)
    const gr = groups[gi], a = (gi === 0 ? 1 : clamp((ts - gr.s + .05) / .12)) * reIn * (gr.e <= (S_.CTA ?? 1e9) + .05 ? 1 - clamp((ts - (S_.CTA ?? 1e9) + .2) / .15) : 1);
    g.save(); g.font = '800 84px Cinzel'; g.letterSpacing = '2px'; g.textAlign = 'left'; g.textBaseline = 'middle';
    // tek satıra az farkla sığmayan kısa grup ("SENİN KAYAN NE?") bölünmesin: yazı biraz küçülür
    // kelime arası boşluk + 16 px: etkin kelime büyüyüp kontur kalınlaşınca komşusuna yapışmasın
    const GAP = 16;
    { const tot = g.measureText(gr.words.map(w => w.w.toLocaleUpperCase('tr')).join(' ')).width + GAP * (gr.words.length - 1); if (tot > 830 && tot < 830 / .86) g.font = `800 ${Math.floor(84 * 830 / tot)}px Cinzel`; }
    const words = gr.words, sp = g.measureText(' ').width + GAP;
    // satırlara böl (en fazla 830 px; merkez 510: sağdaki Shorts düğme sütununa değmez)
    const lines = []; let cur = [], wsum = 0;
    for (const w of words) { const ww = g.measureText(w.w.toLocaleUpperCase('tr')).width; if (cur.length && wsum + sp + ww > 830) { lines.push(cur); cur = []; wsum = 0; } cur.push({ ...w, ww }); wsum += (cur.length > 1 ? sp : 0) + ww; }
    if (cur.length) lines.push(cur);
    const y0 = capY - (lines.length - 1) * 54;
    lines.forEach((ln, li) => {
      const tw = ln.reduce((q, w) => q + w.ww, 0) + sp * (ln.length - 1);
      let x = 510 - tw / 2;
      for (const w of ln) {
        const on = ts >= w.s - .03, cur2 = on && ts < w.e + .05;
        const pop = cur2 ? 1 + .06 * clamp(1 - (ts - w.s) / .15) : 1;
        g.save(); g.translate(x + w.ww / 2, y0 + li * 108); g.scale(pop, pop); g.globalAlpha = a;
        g.lineWidth = light ? 10 : 12; g.strokeStyle = light ? 'rgba(246,236,214,.95)' : 'rgba(15,7,4,.9)'; g.lineJoin = 'round'; g.textAlign = 'center';
        const T = w.w.toLocaleUpperCase('tr');
        g.strokeText(T, 0, 0);
        g.fillStyle = light ? (cur2 ? '#A2381F' : (on ? '#1E1611' : 'rgba(30,22,17,.62)')) : (cur2 ? '#F2C25A' : (on ? '#FFF4DE' : 'rgba(255,244,222,.78)')); g.fillText(T, 0, 0);
        g.restore();
        x += w.ww + sp;
      }
    });
    g.restore();
  }
  // son: kanal çağrısı
  const ce = S_.CTA ?? 1e9;
  if (ts > ce) { const q = clamp((ts - ce) / .4); g.save(); g.globalAlpha = q; g.fillStyle = 'rgba(12,6,4,.7)'; g.fillRect(120, ctaY, 780, 110); g.strokeStyle = PC.clayR; g.lineWidth = 4; g.strokeRect(120, ctaY, 780, 110);
    txt(g, 'TAM HİKÂYE KANALDA', 510, ctaY + 56, { font: '700 46px Cinzel', col: '#F6E3BE', ls: 4, force: true }); g.restore(); }
}
window.renderShortFrame = renderShortFrame;
