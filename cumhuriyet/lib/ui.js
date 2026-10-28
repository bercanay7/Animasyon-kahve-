// İzleyici katmanı (Latin harfli): bölüm kartı, isim levhası, tarih/yer damgası, alıntı, sayaç, telgraf şeridi
'use strict';
const FONT = {
  title: s => `400 ${s}px "Abril Fatface"`,
  slab: s => `400 ${s}px "Alfa Slab One"`,
  mono: s => `700 ${s}px "Courier Prime"`,
  quote: s => `italic 600 ${s}px "Cormorant Garamond"`,
};
// görünürlük zarfı: a giriş, b çıkış (saniye, yerel zaman)
const env = (lt, a0, a1, b0 = 1e9, b1 = 1e9) => ramp(lt, a0, a1) * (1 - ramp(lt, b0, b1));

// alt bant doluluğu: kuşak şeridi (x ≥ ~1120) yalnız yazının sağ ucu 1100'ü geçerse gizlenir
function lowband(x1) {
  if (window.LOWBAND_AT !== window.FIG_T) { window.LOWBAND_AT = window.FIG_T; window.LOWBAND_X1 = x1; }
  else window.LOWBAND_X1 = Math.max(window.LOWBAND_X1 ?? 0, x1);
}
// Yazı (NOTEXT ile Shorts'ta kapatılabilir); print.js'teki txt'nin görünürlüklü sürümü
function label(ctx, s, x, y, font, o = {}) {
  if (NOTEXT && !o.force) return;
  const a = o.a ?? 1; if (a <= 0) return;
  if (y > 1000 && (o.base || 'alphabetic') === 'alphabetic') y = 1000; // güvenli alan
  if (y > 900) {
    ctx.save(); ctx.font = font; if (o.ls) ctx.letterSpacing = o.ls + 'px'; const w = ctx.measureText(s).width; ctx.restore();
    lowband(o.align === 'center' ? x + w / 2 : o.align === 'right' ? x : x + w);
  }
  ctx.save(); ctx.globalAlpha = a; txt(ctx, s, x, y, font, o); ctx.restore();
}
// çıkış: 0,25 sn'de söner ve 8 px yukarı kalkar (koyu zeminde yarı saydam hayalet kalmaz)
const outK = (lt, d) => ramp(lt, d - .25, d);
// Kâğıt künye kutusu (bölüm kartı): numara + başlık + alt satır. lt: kutunun yerel zamanı
function chapterCard(ctx, num, title, sub, lt, d = 3.6, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .25, d - .25, d); if (a <= 0) return;
  // tipografi kurulu: herkes için Abril 84 / Courier 40; standart yer sol alt (sağa yaslı: side:'right'), güvenli alan içinde
  const fsz = 84, ssz = 40;
  ctx.save(); ctx.font = FONT.title(fsz); ctx.letterSpacing = '2px';
  const tw = ctx.measureText(num + ' · ' + title).width;
  ctx.font = FONT.mono(ssz); ctx.letterSpacing = '3px'; const sw = sub ? ctx.measureText(sub).width : 0; ctx.restore();
  const w = Math.max(tw + 70, sw + 76, 420), h = 196, x0 = o.side === 'right' ? 1824 - w : 96, y0 = 1026 - h;
  const drop = (1 - E.out3(ramp(lt, 0, .35))) * -26 - 8 * outK(lt, d);
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, drop);
  plate(ctx, 'ink', PL([[x0 + 10, y0 + 12], [x0 + w + 10, y0 + 12], [x0 + w + 10, y0 + h + 12], [x0 + 10, y0 + h + 12]]), { a: .4 });
  const box = PL(rough([[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]], 1, title.length));
  knock(ctx, box); inkStroke(ctx, box, 3.6); inkStroke(ctx, PL([[x0 + 12, y0 + 12], [x0 + w - 12, y0 + 12], [x0 + w - 12, y0 + h - 12], [x0 + 12, y0 + h - 12]]), 1.4);
  txt(ctx, num + ' · ' + title, x0 + 34, y0 + 102, FONT.title(fsz), { ls: 2 });
  const rl = (w - 68) * E.out3(ramp(lt, .2, .8));
  plate(ctx, 'red', PL([[x0 + 36, y0 + 118], [x0 + 36 + rl, y0 + 118], [x0 + 36 + rl, y0 + 125], [x0 + 36, y0 + 125]]));
  if (sub) txt(ctx, sub, x0 + 36, y0 + 168, FONT.mono(ssz), { ls: 3 });
  ctx.restore();
}
// İsim levhası: ad (Abril) + yaş/görev satırı (Courier); kırmızı alt çizgi
function nameTag(ctx, x, y, name, sub, lt, d = 3.4, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .2, d - .25, d); if (a <= 0) return;
  // tipografi kurulu alt sınırları: ad Abril ≥64, alt satır Courier ≥40 (telefonda okunur)
  const fs = Math.max(o.size || 64, 64), ss = Math.max(o.sub || 40, 40);
  ctx.save(); ctx.font = FONT.title(fs); ctx.letterSpacing = '1px'; ctx.wordSpacing = '0.1em'; const w1 = ctx.measureText(name).width; ctx.font = FONT.mono(ss); ctx.letterSpacing = '0px'; ctx.wordSpacing = '0px'; const w2 = ctx.measureText(sub || '').width; ctx.restore();
  const w = Math.max(w1, w2) + 48, h = fs + ss + 44;
  // güvenli alan (x 96–1824, y 54–1026): levha kenarda kesilmez
  const x0 = clamp(o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x, 96, 1824 - w);
  y = clamp(y, 54, 1026 - h);
  // kuşak şeridi görünürken sağ alt köşeye düşen levha şeridin üstüne çıkar
  if (typeof kusakVisible === 'function' && kusakVisible(window.FIG_T) && x0 + w > 1110 && y + h > 912) y = 912 - h - 14;
  const sl = (1 - E.out3(ramp(lt, 0, .3))) * 18 - 8 * outK(lt, d);
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, sl);
  plate(ctx, 'ink', PL([[x0 + 7, y + 9], [x0 + w + 7, y + 9], [x0 + w + 7, y + h + 9], [x0 + 7, y + h + 9]]), { a: .35 });
  const box = PL(rough([[x0, y], [x0 + w, y], [x0 + w, y + h], [x0, y + h]], .8, name.length + 3));
  knock(ctx, box, o.bg || P.paper); inkStroke(ctx, box, 3.2);
  plate(ctx, o.accent || 'red', PL([[x0, y + h - 7], [x0 + w, y + h - 7], [x0 + w, y + h], [x0, y + h]]));
  txt(ctx, name, x0 + 24, y + 14 + fs * .8, FONT.title(fs), { ls: 1, ws: '0.1em' });
  if (sub) txt(ctx, sub, x0 + 24, y + 26 + fs + ss * .72, FONT.mono(ss));
  ctx.restore();
}
// Yer/tarih damgası: Courier, kırmızı çerçeveli lastik damga; daktilo gibi harf harf
function stamp(ctx, s, x, y, lt, d = 4, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .05, d - .25, d); if (a <= 0) return;
  // daktilo en çok 0,4 sn sürer; 2 sn'den kısa görünen damga yazılmadan, bütün olarak basılır
  const ty = Math.min(o.typing ?? .4, .4), n = d < 2 ? s.length : Math.floor(clamp(lt / ty) * s.length);
  const fs = Math.max(o.size || 48, 48);
  ctx.save(); ctx.font = FONT.mono(fs); ctx.letterSpacing = '3px'; const w = ctx.measureText(s).width; ctx.restore();
  x = clamp(x, 114, 1806 - w); y = clamp(y, 54 + fs + 10, 1008);
  if (y > 900) lowband(x + w + 18);
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, -8 * outK(lt, d));
  if (o.box !== false) {
    const box = PL(rough([[x - 18, y - fs - 10], [x + w + 18, y - fs - 10], [x + w + 18, y + 18], [x - 18, y + 18]], .9, 7));
    knock(ctx, box, o.bg || P.paper); inkStroke(ctx, box, 2.6, { col: o.col || P.ink });
  }
  txt(ctx, s.slice(0, n), x, y, FONT.mono(fs), { ls: 3, col: o.col || P.ink });
  ctx.restore();
}
// Alıntı: Cormorant italik; A sınıfı kâğıt kutu (çift çerçeve + gölge), dengeli satır bölme, asılı tırnak, künye kutunun içinde
function quote(ctx, s, x, y, lt, d = 5, o = {}) {
  if (NOTEXT) return;
  const fs = Math.max(o.size || 80, 72), lh = fs * 1.16, maxW = o.maxW || 1400;
  ctx.save(); ctx.font = FONT.quote(fs);
  const words = s.split(' '), mw = q => ctx.measureText(q).width;
  // en az satır sayısı, sonra en dengeli bölme (son satırda tek kelime kalmaz)
  let lines = [s];
  if (mw(s) > maxW) {
    let best = null;
    for (let k = 2; k <= 4 && !best; k++) {
      const rec = (i, left) => { if (left === 1) return [[words.slice(i).join(' ')]]; const out = []; for (let j = i + 1; j <= words.length - left + 1; j++) for (const r of rec(j, left - 1)) out.push([words.slice(i, j).join(' '), ...r]); return out; };
      for (const c of rec(0, k)) { const ws = c.map(mw); if (Math.max(...ws) > maxW || c[c.length - 1].split(' ').length < 2 && words.length > k) continue; const sc = Math.max(...ws) - Math.min(...ws); if (!best || sc < best.sc) best = { c, sc }; }
    }
    if (best) lines = best.c;
  }
  // asılı tırnak: açılış tırnağı ortalamaya katılmaz
  const hang = q => /^[“"«]/.test(q) ? mw(q[0]) : 0;
  const ww = Math.max(...lines.map(l => mw(l) - hang(l))); ctx.restore();
  const a = env(lt, 0, .35, d - .25, d); if (a <= 0) return;
  const y0 = y - (lines.length - 1) * lh / 2, citeH = o.cite ? 52 : 0;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, -8 * outK(lt, d));
  if (o.band !== false) {
    const bx0 = x - ww / 2 - 70, bx1 = x + ww / 2 + 70, by0 = y0 - fs * .98, by1 = y0 + (lines.length - 1) * lh + fs * .45 + citeH + 16;
    plate(ctx, 'ink', PL([[bx0 + 10, by0 + 12], [bx1 + 10, by0 + 12], [bx1 + 10, by1 + 12], [bx0 + 10, by1 + 12]]), { a: .4 });
    const band = PL(rough([[bx0, by0], [bx1, by0], [bx1, by1], [bx0, by1]], 1.2, 5)); knock(ctx, band); inkStroke(ctx, band, 3.6);
    inkStroke(ctx, PL([[bx0 + 12, by0 + 12], [bx1 - 12, by0 + 12], [bx1 - 12, by1 - 12], [bx0 + 12, by1 - 12]]), 1.4);
    if (o.cite) { ctx.save(); ctx.globalAlpha = a * ramp(lt, .6, 1.0); txt(ctx, o.cite, bx1 - 34, by1 - 30, FONT.mono(36), { align: 'right' }); ctx.restore(); }
  }
  lines.forEach((ln, i) => {
    const q = ramp(lt, .1 + i * .3, .6 + i * .3), hx = hang(ln) / 2;
    ctx.save(); ctx.globalAlpha = a * q; txt(ctx, ln, x - hx, y0 + i * lh + (1 - q) * 10, FONT.quote(fs), { align: 'center' }); ctx.restore();
  });
  ctx.restore();
}
// Büyük sayı/kelime damgası (ör. "600+", "SAVAŞ"): basılma darbesiyle gelir
function bigStamp(ctx, s, x, y, lt, d = 3, o = {}) {
  if (NOTEXT && !o.force) return;
  const a = env(lt, 0, .06, d - .4, d); if (a <= 0) return;
  const k = 1 + (1 - E.out3(ramp(lt, 0, .18))) * .25;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(k, k); ctx.rotate(o.rot || 0);
  if (o.knock) { // kâğıt zemin + 16 px pay (koyu ya da desenli zeminde kontrast)
    const f = (o.font || FONT.title)(o.size || 150); ctx.save(); ctx.font = f; ctx.letterSpacing = (o.ls || 2) + 'px'; const tw = ctx.measureText(s).width; ctx.restore();
    const hh = (o.size || 150) * .62, bx = PL(rough([[-tw / 2 - 16, -hh - 16], [tw / 2 + 16, -hh - 16], [tw / 2 + 16, hh + 16], [-tw / 2 - 16, hh + 16]], 1, s.length));
    knock(ctx, bx); inkStroke(ctx, bx, 2.6);
  }
  txt(ctx, s, 0, 0, (o.font || FONT.title)(o.size || 150), { align: 'center', base: 'middle', plate: o.plate, col: o.col, ls: o.ls || 2 });
  ctx.restore();
}
// Telgraf şeridi: altta akan Courier şerit (bölüm araları)
function tickerTape(ctx, s, y, lt, d = 3.5, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .2, d - .25, d); if (a <= 0) return;
  // tipografi kurulu: bant güvenli alanda (934–1010), taban 980, Courier 40; alt bant dolu iken kuşak şeridi gizlenir
  y = 976; lowband(W);
  ctx.save(); ctx.globalAlpha = a;
  const band = PL([[-20, y - 42], [W + 20, y - 40], [W + 20, y + 34], [-20, y + 32]]);
  knock(ctx, band, '#F4ECD8'); inkStroke(ctx, band, 2.4);
  const n = Math.floor(clamp(lt / (o.typing ?? 1.0)) * s.length);
  txt(ctx, s.slice(0, n) + (n < s.length && Math.floor(lt * 8) % 2 ? '▌' : ''), Math.max(o.x ?? 110, 110), y + 14, FONT.mono(Math.max(o.size || 40, 40)), { ls: 4 });
  ctx.restore();
}

// Durağan katman önbelleği: çekim boyunca değişmeyen zemin (harita, oda, yarım ton) bir kez çizilir.
// Kullanım: const bg = layerCache('B03-zemin', g => { paperBG(g); ... }); ctx.drawImage(bg, 0, 0, W, H);
// (çizim fonksiyonuna verilen g, baseT uygulanmış W×H mantıksal koordinatlı bir bağlamdır; kayık baskı o anki setReg'e göre sabitlenir)
const LCACHE = {};
function layerCache(key, draw, w = W, h = H) {
  // anahtara kayık baskı tohumu da girer: aynı anahtarı kullanan iki çekim birbirinin önbelleğini almaz,
  // görüntü hangi render işçisinin önce kurduğuna bağlı kalmaz
  key = key + '@' + REG.seed + ':' + REG.amt;
  if (!LCACHE[key]) {
    const c = makeCanvas(Math.ceil(w * RS), Math.ceil(h * RS)), g = c.getContext('2d');
    // geçişin kayık baskısı (REG.boost) önbelleğe donmasın: katman her zaman yerine oturmuş hâliyle çizilir
    const b = REG.boost; REG.boost = 1;
    g.setTransform(RS, 0, 0, RS, 0, 0); try { draw(g); } finally { REG.boost = b; } LCACHE[key] = c;
  }
  return LCACHE[key];
}

// ekran yazıları sahnenin kamera hareketine (film.js drawShot, window.DRIFT) katılmaz: güvenli alanda, ekrana sabit kalır
function undrift(ctx) { const d = window.DRIFT; ctx.translate(W / 2 + d.px, H / 2 + d.py); ctx.scale(1 / d.z, 1 / d.z); ctx.translate(-W / 2, -H / 2); }
for (const fn of ['label', 'chapterCard', 'nameTag', 'stamp', 'quote', 'bigStamp', 'tickerTape']) {
  const f = window[fn];
  window[fn] = function (ctx, ...a) {
    if (!window.DRIFT || window.__undrift) return f(ctx, ...a);
    window.__undrift = true; ctx.save(); undrift(ctx);
    try { return f(ctx, ...a); } finally { ctx.restore(); window.__undrift = false; }
  };
}
// txt() ile doğrudan çizilen izleyici yazıları (başlık, künye, sayı) için: kamera hareketini geri alıp ekrana sabit çizer
function onScreen(ctx, fn) {
  if (!window.DRIFT || window.__undrift) return fn(ctx);
  window.__undrift = true; ctx.save(); undrift(ctx);
  try { return fn(ctx); } finally { ctx.restore(); window.__undrift = false; }
}
