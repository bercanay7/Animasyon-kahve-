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

// Yazı (NOTEXT ile Shorts'ta kapatılabilir); print.js'teki txt'nin görünürlüklü sürümü
function label(ctx, s, x, y, font, o = {}) {
  if (NOTEXT && !o.force) return;
  const a = o.a ?? 1; if (a <= 0) return;
  ctx.save(); ctx.globalAlpha = a; txt(ctx, s, x, y, font, o); ctx.restore();
}
// Kâğıt künye kutusu (bölüm kartı): numara + başlık + alt satır. lt: kutunun yerel zamanı
function chapterCard(ctx, num, title, sub, lt, d = 3.6, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .25, d - .5, d); if (a <= 0) return;
  ctx.save(); ctx.font = FONT.title(o.size || 80); ctx.letterSpacing = '2px';
  const tw = ctx.measureText(num + ' · ' + title).width;
  // alt satır da ölçülür: uzun alt satır kutudan taşmasın
  ctx.font = FONT.mono(30); ctx.letterSpacing = '3px'; const sw = sub ? ctx.measureText(sub).width : 0; ctx.restore();
  const w = Math.max(tw + 70, sw + 76, 420), h = 176, x0 = o.x ?? 76, y0 = o.y ?? (H - h - 40);
  const drop = (1 - E.out3(ramp(lt, 0, .35))) * -26;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, drop);
  plate(ctx, 'ink', PL([[x0 + 10, y0 + 12], [x0 + w + 10, y0 + 12], [x0 + w + 10, y0 + h + 12], [x0 + 10, y0 + h + 12]]), { a: .4 });
  const box = PL(rough([[x0, y0], [x0 + w, y0], [x0 + w, y0 + h], [x0, y0 + h]], 1, title.length));
  knock(ctx, box); inkStroke(ctx, box, 3.6); inkStroke(ctx, PL([[x0 + 12, y0 + 12], [x0 + w - 12, y0 + 12], [x0 + w - 12, y0 + h - 12], [x0 + 12, y0 + h - 12]]), 1.4);
  txt(ctx, num + ' · ' + title, x0 + 34, y0 + 94, FONT.title(o.size || 80), { ls: 2 });
  const rl = (w - 68) * E.out3(ramp(lt, .2, .8));
  plate(ctx, 'red', PL([[x0 + 36, y0 + 110], [x0 + 36 + rl, y0 + 110], [x0 + 36 + rl, y0 + 117], [x0 + 36, y0 + 117]]));
  if (sub) txt(ctx, sub, x0 + 36, y0 + 152, FONT.mono(30), { ls: 3 });
  ctx.restore();
}
// İsim levhası: ad (Abril) + yaş/görev satırı (Courier); kırmızı alt çizgi
function nameTag(ctx, x, y, name, sub, lt, d = 3.4, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .2, d - .4, d); if (a <= 0) return;
  const fs = o.size || 46, ss = o.sub || 30;
  ctx.save(); ctx.font = FONT.title(fs); const w1 = ctx.measureText(name).width; ctx.font = FONT.mono(ss); const w2 = ctx.measureText(sub || '').width; ctx.restore();
  const w = Math.max(w1, w2) + 48, h = fs + ss + 38;
  // güvenli alan (x 96–1824, y 54–1026): levha kenarda kesilmez
  const x0 = clamp(o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x, 96, 1824 - w);
  y = clamp(y, 54, 1026 - h);
  // kuşak şeridi görünürken sağ alt köşeye düşen levha şeridin üstüne çıkar
  if (typeof kusakVisible === 'function' && kusakVisible(window.FIG_T) && x0 + w > 1020 && y + h > 935) y = 935 - h - 14;
  const sl = (1 - E.out3(ramp(lt, 0, .3))) * 18;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(0, sl);
  plate(ctx, 'ink', PL([[x0 + 7, y + 9], [x0 + w + 7, y + 9], [x0 + w + 7, y + h + 9], [x0 + 7, y + h + 9]]), { a: .35 });
  const box = PL(rough([[x0, y], [x0 + w, y], [x0 + w, y + h], [x0, y + h]], .8, name.length + 3));
  knock(ctx, box, o.bg || P.paper); inkStroke(ctx, box, 3.2);
  plate(ctx, o.accent || 'red', PL([[x0, y + h - 7], [x0 + w, y + h - 7], [x0 + w, y + h], [x0, y + h]]));
  txt(ctx, name, x0 + 24, y + 14 + fs * .8, FONT.title(fs), { ls: 1 });
  if (sub) txt(ctx, sub, x0 + 24, y + 22 + fs + ss * .72, FONT.mono(ss));
  ctx.restore();
}
// Yer/tarih damgası: Courier, kırmızı çerçeveli lastik damga; daktilo gibi harf harf
function stamp(ctx, s, x, y, lt, d = 4, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .05, d - .4, d); if (a <= 0) return;
  // daktilo en çok 0,4 sn sürer; 2 sn'den kısa görünen damga yazılmadan, bütün olarak basılır
  const ty = Math.min(o.typing ?? .4, .4), n = d < 2 ? s.length : Math.floor(clamp(lt / ty) * s.length);
  const fs = o.size || 34;
  ctx.save(); ctx.font = FONT.mono(fs); ctx.letterSpacing = '4px'; const w = ctx.measureText(s).width; ctx.restore();
  ctx.save(); ctx.globalAlpha = a;
  if (o.box !== false) {
    const box = PL(rough([[x - 18, y - fs - 10], [x + w + 18, y - fs - 10], [x + w + 18, y + 18], [x - 18, y + 18]], .9, 7));
    knock(ctx, box, o.bg || P.paper); inkStroke(ctx, box, 2.6, { col: o.col || P.ink });
  }
  txt(ctx, s.slice(0, n), x, y, FONT.mono(fs), { ls: 4, col: o.col || P.ink });
  ctx.restore();
}
// Alıntı: Cormorant italik, satır satır; kâğıt şerit zemin (okunurluk)
function quote(ctx, s, x, y, lt, d = 5, o = {}) {
  if (NOTEXT) return;
  const fs = o.size || 66, lh = fs * 1.18, maxW = o.maxW || 1300;
  ctx.save(); ctx.font = FONT.quote(fs);
  const words = s.split(' '), lines = []; let cur = '';
  for (const w of words) { const tt = cur ? cur + ' ' + w : w; if (ctx.measureText(tt).width > maxW && cur) { lines.push(cur); cur = w; } else cur = tt; }
  if (cur) lines.push(cur);
  const ww = Math.max(...lines.map(l => ctx.measureText(l).width)); ctx.restore();
  const a = env(lt, 0, .35, d - .5, d); if (a <= 0) return;
  const y0 = y - (lines.length - 1) * lh / 2;
  ctx.save(); ctx.globalAlpha = a;
  if (o.band !== false) {
    const bx0 = x - ww / 2 - 50, bx1 = x + ww / 2 + 50, by0 = y0 - fs * .95, by1 = y0 + (lines.length - 1) * lh + fs * .5;
    const band = PL(rough([[bx0, by0], [bx1, by0], [bx1, by1], [bx0, by1]], 1.4, 5)); knock(ctx, band); inkStroke(ctx, band, 2.4);
  }
  lines.forEach((ln, i) => {
    const q = ramp(lt, .1 + i * .3, .6 + i * .3);
    ctx.save(); ctx.globalAlpha = a * q; txt(ctx, ln, x, y0 + i * lh + (1 - q) * 10, FONT.quote(fs), { align: 'center' }); ctx.restore();
  });
  if (o.cite) { ctx.save(); ctx.globalAlpha = a * ramp(lt, .8, 1.3); txt(ctx, o.cite, x + ww / 2, y0 + (lines.length - 1) * lh + fs * .5 + 44, FONT.mono(26), { align: 'right' }); ctx.restore(); }
  ctx.restore();
}
// Büyük sayı/kelime damgası (ör. "600+", "SAVAŞ"): basılma darbesiyle gelir
function bigStamp(ctx, s, x, y, lt, d = 3, o = {}) {
  if (NOTEXT && !o.force) return;
  const a = env(lt, 0, .06, d - .4, d); if (a <= 0) return;
  const k = 1 + (1 - E.out3(ramp(lt, 0, .18))) * .25;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.scale(k, k); ctx.rotate(o.rot || 0);
  txt(ctx, s, 0, 0, (o.font || FONT.title)(o.size || 150), { align: 'center', base: 'middle', plate: o.plate, col: o.col, ls: o.ls || 2 });
  ctx.restore();
}
// Telgraf şeridi: altta akan Courier şerit (bölüm araları)
function tickerTape(ctx, s, y, lt, d = 3.5, o = {}) {
  if (NOTEXT) return;
  const a = env(lt, 0, .2, d - .4, d); if (a <= 0) return;
  ctx.save(); ctx.globalAlpha = a;
  const band = PL([[-20, y - 34], [W + 20, y - 30], [W + 20, y + 22], [-20, y + 18]]);
  knock(ctx, band, '#F4ECD8'); inkStroke(ctx, band, 2.4);
  const n = Math.floor(clamp(lt / (o.typing ?? 1.4)) * s.length);
  txt(ctx, s.slice(0, n) + (n < s.length && Math.floor(lt * 8) % 2 ? '▌' : ''), o.x ?? 60, y + 4, FONT.mono(o.size || 30), { ls: 6 });
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
