// Shorts (Mary Stuart): filmden kesitler, dikey 1080×1920. Kare: film kadrajından 810×1080 → 1080×1440 (kesit başına `cx`: kırpma merkezi, varsayılan 720 = orta).
// Kurgu dosyası: shorts.html?edl=AD → shorts/edl_AD.json (yoksa shorts/edl.json). Dosyada isteğe bağlı: kanca {satir:[2], bitis: kesit sırası},
// ust {baslik, alt}, son {satir:[2], alt}, kesit başına kunye, vsrc0 (görüntünün kaynak anı; yoksa src0), altY (altyazı yüksekliği). Yoksa birinci Shorts'un değerleri kullanılır (geriye dönük aynı çıktı).
// Üstte kanca yazısı, altta sözcük vurgulu altyazı; sonda kanal kartı.
'use strict';
window.SHORTS_UST_YOK = true;   // filmin üst katmanı (künye, etiket) dikey kırpmada kesik kalıyordu; Shorts kendi künyesini yazar
const EDLAD = new URLSearchParams(location.search).get('edl');
let EDL = null; fetch(EDLAD ? `shorts/edl_${EDLAD}.json` : 'shorts/edl.json').then(r => r.json()).then(j => { EDL = j; });
const SH_KANCA = () => EDL.kanca || { satir: ['İDAMINA', 'KIRMIZI GİYDİ'], bitis: 2 };
const SH_UST = () => EDL.ust || { baslik: 'MARY STUART', alt: 'Fotheringhay · 8 Şubat 1587' };
const SH_SON = () => ({ satir: ['KALBİNLE Mİ,', 'AKLINLA MI?'], alt: 'Tam hikâye kanalda: Mary Stuart ve I. Elizabeth', ...EDL.son });
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
  sg.font = '700 58px "Cinzel"'; sg.textAlign = 'left'; sg.textBaseline = 'middle'; const txt = grp.map(i => toks[i]).join(' '), w = sg.measureText(txt).width, x0 = 540 - w / 2, y = k.altY ?? 1500;
  sg.fillStyle = 'rgba(10,9,8,.72)'; sg.fillRect(x0 - 30, y - 56, w + 60, 112);
  let x = x0; for (const i of grp) { const s2 = toks[i] + ' '; sg.fillStyle = i === cur ? '#f6efe0' : 'rgba(236,229,213,.55)'; sg.fillText(s2, x, y); x += sg.measureText(s2).width; }
}
window.renderShortFrame = t => {
  sg.setTransform(1, 0, 0, 1, 0, 0); sg.fillStyle = '#0b0a09'; sg.fillRect(0, 0, 1080, 1920);
  if (!EDL) return SC;
  const k = EDL.kesit.slice().reverse().find(x => t >= x.t0);
  if (t < EDL.son.t0 && k) {
    const src = (k.vsrc0 ?? k.src0) + (t - k.t0), fc = renderFrame(src);   // vsrc0: görüntü sesten başka bir andan (ör. tamamlanmış soy ağacı)
    sg.drawImage(fc, 240 + (k.cx ?? 720) - 405, 0, 810, 1080, 0, 330, 1080, 1440);
    // üst/alt karartma; kesit başına fadeUst/fadeAlt ile sınırı kayar (alttaki ya da üstteki yazı okunsun)
    const vg = sg.createLinearGradient(0, 330, 0, 1770); vg.addColorStop(0, 'rgba(11,10,9,.9)'); vg.addColorStop(k.fadeUst ?? .12, 'rgba(11,10,9,0)'); vg.addColorStop(k.fadeAlt ?? .85, 'rgba(11,10,9,0)'); vg.addColorStop(1, 'rgba(11,10,9,.95)'); sg.fillStyle = vg; sg.fillRect(0, 330, 1080, 1440);
    shortsYazi(t, k);
    if (k.kunye) { sg.font = 'italic 500 30px "Cormorant Garamond"'; sg.textAlign = 'center'; sg.fillStyle = 'rgba(236,229,213,.8)'; sg.fillText(k.kunye, 540, 372); }
  } else {
    const u = clamp((t - EDL.son.t0) / .6); sg.globalAlpha = u; sg.textAlign = 'center'; sg.textBaseline = 'middle';
    const so = SH_SON(); sg.fillStyle = '#ece5d5'; sg.font = '400 120px "Bebas Neue"'; sg.fillText(so.satir[0], 540, 820); sg.fillText(so.satir[1], 540, 950);
    sg.font = 'italic 600 52px "Cormorant Garamond"'; sg.fillText(so.alt, 540, 1110);
    sg.font = '700 40px "Cinzel"'; sg.fillStyle = 'rgba(236,229,213,.8)'; sg.fillText('ZAMAN KURYESİ', 540, 1240); sg.globalAlpha = 1;
  }
  // kanca (birinci Shorts'ta kapak B'nin sözü) ilk kesitler boyunca; sonra başlık
  sg.textAlign = 'center'; sg.textBaseline = 'alphabetic';
  if (t < EDL.son.t0) {
    const ka = SH_KANCA(), us = SH_UST(), bitis = ka.bitis < EDL.kesit.length ? EDL.kesit[ka.bitis].t0 : EDL.son.t0;
    if (t < bitis) { sg.font = `400 ${ka.boy || 128}px "Bebas Neue"`; sg.fillStyle = '#ece5d5'; sg.fillText(ka.satir[0], 540, 150); sg.fillStyle = 'rgb(206,34,40)'; sg.fillText(ka.satir[1], 540, 285); }
    else { sg.font = '700 44px "Cinzel"'; sg.fillStyle = '#ece5d5'; sg.fillText(us.baslik, 540, 140); sg.font = 'italic 600 40px "Cormorant Garamond"'; sg.fillStyle = 'rgba(236,229,213,.85)'; sg.fillText(us.alt, 540, 200); }
  }
  return SC;
};
window.ready.then(async () => { while (!EDL || !Object.keys(ALT).length) await new Promise(r => setTimeout(r, 50)); await document.fonts.load('400 120px "Bebas Neue"', SH_KANCA().satir.join('') + SH_SON().satir.join('')); window.SHORTS_HAZIR = true; window.READY = true; });
