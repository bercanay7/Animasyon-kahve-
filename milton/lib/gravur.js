// Gravür motoru v2: ton, çizgi kalınlığıyla; çizgiler nesnenin biçimini izler.
// Sahne iki katmana çizilir:
//   ton katmanı (tx): gri değer (beyaz = kâğıt, siyah = tam mürekkep); ışık ve gölge burada boyanır;
//   yama katmanı (px): her dolgu bir "yama" kimliğiyle boyanır. Yama, o bölgedeki tarama alanını tanımlar:
//     lin  : düz paralel çizgiler (doğrultu th)
//     rad  : bir merkez çevresinde eş merkezli yaylar (bulut kümesi, küre, kubbe)
//     bend : bir eksen boyunca akan, parabolik kavisli çizgiler (tüy, alev dili, uzuv)
//     buf  : piksel başına evre (FG.sculpt'un yazdığı yükseklik alanı; bedeni saran çizgiler)
// GR.engrave(out) iki katmanı okuyup basar: koyuluk arttıkça çizgi kalınlaşır, eşik aşılınca çapraz tarama girer;
// çok açık ton temiz kâğıt, çok koyu ton düz siyah olur (sakin kütleler).
// İlkeler (kullanıcı kararı ve üslup kurulu tur 1): göz yormayan seyrek ve kalın çizgi; benek yok; çizgi biçimi izler;
// çizgiler dünya koordinatındadır (kamera kayınca sahneyle kayar), hareketli nesne kendi çapasına (anchor) bağlıdır.
'use strict';
const GR = (() => {
  const w = DW, h = DH;
  const tc = makeCanvas(w, h), tx = tc.getContext('2d', { willReadFrequently: true });
  const pc = makeCanvas(w, h), px = pc.getContext('2d', { willReadFrequently: true });
  // üst katman (ox): basmadan sonra çıktıya bindirilen keskin çizgiler (kontur, beyaz çizgi, göz ışığı)
  const oc = makeCanvas(w, h), ox = oc.getContext('2d');
  const PAPER = [230, 223, 207], INK = [26, 23, 21];
  // pürüzsüz 1B gürültü tablosu (çizgi titreşimi), 1024 örnek, dairesel
  const NZ = new Float32Array(1024);
  { const r = rng(7), raw = Array.from({ length: 128 }, () => r() * 2 - 1);
    for (let i = 0; i < 1024; i++) { const f = i / 8, k = Math.floor(f), u = f - k, s = u * u * (3 - 2 * u); NZ[i] = raw[k % 128] * (1 - s) + raw[(k + 1) % 128] * s; } }
  // üslup tablosu (P mantıksal px): cr = çapraz doğrultu farkı (radyan), ct = çapraz eşik (koyuluk),
  // wv = el titreşimi genliği (periyot), wf = titreşim sıklığı (1/px), g = ton eğrisi üssü, lo/hi = temiz kâğıt ve düz siyah eşikleri
  const STY = [];
  function sty(id, o) { STY[id] = Object.assign({ P: 9, cr: .9, ct: .8, wv: .05, wf: 1 / 60, g: 1, lo: .07, hi: .93, f0: .1, f1: .88, ph: id * 137 }, o); const S = STY[id]; if (!o.cross) S.ct = 9;
    if (o.f1 == null) S.f1 = Math.min(.88, 1 - 3 / S.P); if (o.f0 == null) S.f0 = Math.max(.1, 1.7 / S.P); }   // beyaz aralık ≥ 3 px, siyah çizgi ≥ 1,7 px (telefon boyunda kaybolmasın)   // f0–f1: en ince ve en kalın çizgi oranı (kıl gibi siyah ya da beyaz çizgi kalmaz; kırık çizgi ve küçük boyda benek olmaz)
  sty(0, {});                                            // genel
  sty(1, { P: 12.0, wv: .03, wf: 1 / 90, ct: .9 });       // gökyüzü: sakin, seyrek
  sty(2, { P: 11.0, wv: .06, wf: 1 / 50, ct: .72 });      // bulut, duman: kavisli, koyuda çapraz
  sty(3, { P: 9.5, wv: .04, wf: 1 / 40, ct: 1.1, lo: .14 }); // alev: içi temiz kâğıt, çapraz yok
  sty(4, { P: 9.0, wv: .09, wf: 1 / 30, ct: .55, cr: 1.1 }); // kaya: çapraz taramalı
  sty(5, { P: 5.6, wv: .02, wf: 1 / 70, ct: .8 });       // ten
  sty(6, { P: 9.0, wv: .02, wf: 1 / 70, ct: .86, cr: .6, lo: .12 }); // tüy
  sty(7, { P: 12.0, wv: .02, wf: 1 / 90, ct: 1.1 });      // ışık huzmesi
  sty(8, { P: 12.5, wv: .08, wf: 1 / 46, ct: .88 });      // su, göl yüzeyi
  sty(9, { P: 5.8, wv: .03, wf: 1 / 60, ct: .7, cr: 1.0 }); // zırh, kumaş
  sty(10, { P: 20, wv: .02, wf: 1 / 120, lo: .05 });  // açık gök (cennet, Aden gündüzü): çok seyrek, ince çizgi; açık zeminde göz yormaz
  // ton baytı → ham oran r = (koyuluk − lo) / (hi − lo); kırpılmaz. r ≤ 0 kâğıt, r ≥ 1 düz siyah; arası çizgi kalınlığı f0…f1.
  const DL = () => STY.map(s => { const a = new Float32Array(256); for (let i = 0; i < 256; i++) { const d = Math.pow(1 - i / 255, s.g); a[i] = (d - s.lo) / (s.hi - s.lo); } return a; });

  // ── yama tablosu ──
  // Renk kodu: R,G = kimlik; B = kimliğin sağlaması (kenar yumuşatmasının karıştırdığı pikseller geçersiz sayılır, soldaki yamayı sürdürür)
  const HB = new Uint8Array(65536); { const r = rng(99); for (let i = 0; i < 65536; i++) HB[i] = (r() * 256) | 0; }
  let patches = [], cache = new Map();
  let fm = new DOMMatrix(), fRot = 0, fFlip = false; // yerel çizim çerçevesi (GR.frame)
  const wpt = (x, y) => { const p = fm.transformPoint(new DOMPoint(x, y)); return [p.x, p.y]; };
  const wang = a => (fFlip ? PI - a : a) + fRot;
  function reg(p) {
    const id = patches.length; patches.push(p);
    return `rgb(${id & 255},${id >> 8},${HB[id]})`;
  }
  // tarama tanımı → yama rengi. Koordinat ve açılar geçerli çerçevede (GR.frame) verilir.
  //  {th, ph, id}                      düz çizgi (th = çizgi doğrultusu, radyan)
  //  {type:'rad', cx, cy, ph, id}      (cx, cy) çevresinde yaylar
  //  {type:'bend', ox, oy, a, k, id}   (ox, oy)'den a doğrultusunda akan çizgiler; k > 0 ise akış yönünde sola kavis (1/px)
  //  {type:'buf', id}                  evre arabelleği (FG.sculpt)
  //  anchor: [x, y]                    nesnenin çapa noktası; nesne kayınca çizgiler onunla kayar
  function hatch(o = {}) {
    const id = o.id || 0, P = STY[id].P, an = o.anchor ? wpt(o.anchor[0], o.anchor[1]) : null;
    if (o.type === 'rad') { const [cx, cy] = wpt(o.cx, o.cy); return reg({ t: 1, id, cx, cy, ph: o.ph || 0 }); }
    if (o.type === 'bend') { const [ox, oy] = wpt(o.ox, o.oy), a = wang(o.a || 0); return reg({ t: 2, id, ox, oy, ca: Math.cos(a), sa: Math.sin(a), k: (o.k || 0) * (fFlip ? -1 : 1), ph: o.ph || 0 }); }
    if (o.type === 'buf') return reg({ t: 3, id });
    // ışınsal tarama: (cx, cy) merkezinden çıkan n ışın çizgisi; aralık merkezden uzaklaştıkça açılır, merkez yakınında (aralık < 6 px) çizgi yok
    if (o.type === 'ray') { const [cx, cy] = wpt(o.cx, o.cy); return reg({ t: 5, id, cx, cy, n: Math.round(o.n || 90), ph: o.ph || 0, w: o.w }); }
    // perspektifli yatay tarama (su, zemin): aralık y0'da p0, y0 + D'de p1 (uzakta sık, yakında seyrek)
    if (o.type === 'persp') { const y0 = wpt(0, o.y0)[1], k = o.D / Math.max(.01, o.p1 - o.p0); return reg({ t: 4, id, y0, k, c: o.p0 * k, ph: o.ph || 0 }); }
    const th = wang(o.th || 0), c = Math.cos(th), s = Math.sin(th);
    let ph = o.ph || 0; if (an) ph -= (an[1] * c - an[0] * s) / P;
    const key = an ? null : `${id}|${Math.round(th * 4096)}|${Math.round(ph * 4096)}`;
    if (key && cache.has(key)) return cache.get(key);
    const col = reg({ t: 0, id, c, s, ph });
    if (key) cache.set(key, col);
    return col;
  }
  // eski arayüz: düz çizgi
  const pat = (th, ph = 0, id = 0) => hatch({ th, ph, id });
  const phaseOf = (th, dx, dy, id) => -(dy * Math.cos(th) - dx * Math.sin(th)) / STY[id].P;
  // (x0,y0)→(x1,y1) ekseni boyunca akan, doğrultusu th0'dan th1'e dönen çizgiler: kavisli akış (bend) olarak kurulur
  function patGrad(x0, y0, x1, y1, stops, ph = 0, id = 0) {
    const th0 = stops[0][1], th1 = stops[stops.length - 1][1], L = Math.hypot(x1 - x0, y1 - y0) || 1;
    return hatch({ type: 'bend', ox: x0, oy: y0, a: th0, k: Math.tan(th1 - th0) / (2 * L), ph, id });
  }
  const tone = (v, a = 1) => { const b = Math.round(clamp(v) * 255); return a < 1 ? `rgba(${b},${b},${b},${a})` : `rgb(${b},${b},${b})`; };
  const PHB = new Float32Array(w * h); // evre arabelleği (buf yamaları)
  let cam = { x: 0, y: 0, s: 1 }, camM = new DOMMatrix([RS, 0, 0, RS, 0, 0]);
  function begin(bgTone = 1, bgTh = 0, bgId = 1, c = null) {
    cam = c || { x: 0, y: 0, s: 1 };
    patches = []; cache = new Map(); fm = new DOMMatrix(); fRot = 0; fFlip = false;
    // kamera: cam.x, cam.y ekranın sol üst köşesine gelen dünya noktası, cam.s yakınlık. Çizim dünya koordinatında yapılır;
    // tarama çizgileri dünyaya bağlıdır (kamera kayınca resimle birlikte kayar, yaklaşınca kalınlaşır).
    const k = RS * cam.s; camM = new DOMMatrix([k, 0, 0, k, -cam.x * k, -cam.y * k]);
    for (const cx of [tx, px, ox]) { cx.setTransform(camM); cx.globalAlpha = 1; cx.globalCompositeOperation = 'source-over'; cx.filter = 'none'; }
    ox.save(); ox.setTransform(1, 0, 0, 1, 0, 0); ox.clearRect(0, 0, w, h); ox.restore();
    tx.fillStyle = tone(bgTone); tx.fillRect(cam.x - 2, cam.y - 2, W / cam.s + 4, H / cam.s + 4);
    px.fillStyle = hatch({ th: bgTh, id: bgId }); px.fillRect(cam.x - 2, cam.y - 2, W / cam.s + 4, H / cam.s + 4);
  }
  // bir yolu iki katmana birden doldur. toneStyle: renk ya da gradyan; hs: tarama tanımı (hatch) ya da {fill: hazır yama rengi}
  function fill(path, toneStyle, hs, rule = 'nonzero') {
    if (toneStyle != null) { tx.fillStyle = toneStyle; tx.fill(path, rule); }
    if (hs) { px.fillStyle = hs.fill || hatch(hs); px.fill(path, rule); }
  }
  function setT(a, b, c, d, e, f) { tx.setTransform(a, b, c, d, e, f); px.setTransform(a, b, c, d, e, f); ox.setTransform(a, b, c, d, e, f); }
  // yerel çizim çerçevesi: dünya (x,y)'de, ang radyan dönük, side = ±1 aynalı, k ölçekli
  function frame(x, y, ang = 0, side = 1, k = 1) {
    fm = new DOMMatrix().translate(x, y).rotate(ang * 180 / PI).scale(side * k, k); fRot = ang; fFlip = side < 0;
    const d = camM.multiply(fm);
    setT(d.a, d.b, d.c, d.d, d.e, d.f);
    return fm;
  }
  function unframe() { setT(camM.a, camM.b, camM.c, camM.d, camM.e, camM.f); fm = new DOMMatrix(); fRot = 0; fFlip = false; }
  function save() { tx.save(); px.save(); ox.save(); }
  function restore() { tx.restore(); px.restore(); ox.restore(); }

  // oyma titremesi alanı: 512×512, döşenebilir (tam sayı frekanslı sinüslerin toplamı), örnek aralığı 2 dünya pikseli.
  // Dalga boyu 40–120 px; JX/JY kenar sapması (±1), JT çizgi kalınlığı dalgası (±1).
  const JS = .5, JIT = { amp: 1.2, th: .06 };
  const JX = new Float32Array(262144), JY = new Float32Array(262144), JT = new Float32Array(262144);
  { const r = rng(4242), mk = (A, n) => { const C = []; for (let k = 0; k < n; k++) { const a = r() * TAU, f = 9 + r() * 17; C.push([Math.round(Math.cos(a) * f), Math.round(Math.sin(a) * f), r() * TAU, .5 + r()]); }
      let mx = 0; for (let y = 0; y < 512; y++) for (let x = 0; x < 512; x++) { let v = 0; for (const c of C) v += c[3] * Math.sin(TAU * (c[0] * x + c[1] * y) / 512 + c[2]); A[y * 512 + x] = v; if (Math.abs(v) > mx) mx = Math.abs(v); }
      for (let i = 0; i < 262144; i++) A[i] /= mx; };
    mk(JX, 7); mk(JY, 7); mk(JT, 5); }
  // ── basma ──
  const SG = .2, TW = .025;                       // kademe genişliği ve uç sivrilmesi (ham oran biriminde)
  const HSH = new Float32Array(256); { const r = rng(977); for (let i = 0; i < 256; i++) HSH[i] = r(); }
  let img = null;
  function engrave(out, camArg = null) {
    if (camArg) cam = camArg;
    const T = tx.getImageData(0, 0, w, h).data, Pd = px.getImageData(0, 0, w, h).data;
    if (!img || img.width !== w) img = out.createImageData(w, h);
    const O = img.data, D = DL();
    const pr = PAPER[0], pg = PAPER[1], pb = PAPER[2], ir = INK[0] - pr, ig = INK[1] - pg, ib = INK[2] - pb;
    const kk = 1 / (RS * cam.s), ox = cam.x, oy = cam.y, devPer = RS * cam.s;
    const nP = patches.length, ja = JIT.amp * devPer, w4 = w * 4;
    for (let y = 0; y < h; y++) {
      let i = y * w * 4, lastKey = -1, p = patches[0], st = STY[p.id], dl = D[p.id], invP = 1 / st.P, Pdv = st.P * devPer;
      const wy = y * kk + oy;
      const jy = ((wy * JS) | 0) & 511;
      for (let x = 0; x < w; x++, i += 4) {
        // oyma titremesi: her piksel, dünyaya bağlı sabit bir sapma alanından okunur (kenarlar ve çizgiler matematik pürüzsüzlüğünü yitirir;
        // alan zamanla değişmez, kamera kayınca resimle birlikte kayar: titreşim yaratmaz)
        const ji = ((((x * kk + ox) * JS) | 0) & 511) | (jy << 9);
        let fx = x + JX[ji] * ja, fy = y + JY[ji] * ja;
        if (fx < 0) fx = 0; else if (fx > w - 1.001) fx = w - 1.001; if (fy < 0) fy = 0; else if (fy > h - 1.001) fy = h - 1.001;
        const x0 = fx | 0, y0 = fy | 0, ax = fx - x0, ay = fy - y0, i0 = (y0 * w + x0) * 4, ip = (((fy + .5) | 0) * w + ((fx + .5) | 0)) * 4;
        const tv = (T[i0] * (1 - ax) + T[i0 + 4] * ax) * (1 - ay) + (T[i0 + w4] * (1 - ax) + T[i0 + w4 + 4] * ax) * ay;
        const key = Pd[ip] | (Pd[ip + 1] << 8);
        if (key !== lastKey || Pd[ip + 2] !== HB[key]) {
          if (key < nP && Pd[ip + 2] === HB[key]) { p = patches[key]; st = STY[p.id]; dl = D[p.id]; invP = 1 / st.P; Pdv = st.P * devPer; lastKey = key; }
        }
        const r = dl[(tv + .5) | 0];
        let ink = 0, d = 0;
        if (r >= 1) ink = 1;
        else if (r > 0) {
          const wx = x * kk + ox, t = p.t;
          let U, along, Pl = Pdv, fade = 1, capW = 9;
          if (t === 0) { U = (wy * p.c - wx * p.s) * invP + p.ph; along = wx * p.c + wy * p.s; }
          else if (t === 1) { const dx = wx - p.cx, dy = wy - p.cy; U = Math.sqrt(dx * dx + dy * dy) * invP + p.ph; along = wx * .8 + wy * .6; }
          else if (t === 2) { const dx = wx - p.ox, dy = wy - p.oy, pp = dx * p.ca + dy * p.sa, qq = dy * p.ca - dx * p.sa; U = (qq + p.k * pp * pp) * invP + p.ph; along = pp; }
          else if (t === 4) { const q = Math.max(1, wy - p.y0 + p.c); U = p.k * Math.log(q / p.c) + p.ph; along = wx; Pl = q / p.k * devPer; }
          else if (t === 5) { const dx = wx - p.cx, dy = wy - p.cy, rr = Math.sqrt(dx * dx + dy * dy), per = TAU * rr / p.n; U = Math.atan2(dy, dx) * p.n / TAU + p.ph + p.n; along = rr; Pl = per * devPer; fade = per < 6 ? 0 : per < 12 ? (per - 6) / 6 : 1; capW = (p.w || 3.2) / per; }
          else { U = PHB[y * w + x]; along = wx * .8 + wy * .6; }
          const ai = along * st.wf + st.ph + 65536, a0 = ai | 0, af = ai - a0;
          U += (NZ[a0 & 1023] * (1 - af) + NZ[(a0 + 1) & 1023] * af) * st.wv + 8192;
          const u = U - (U | 0);
          // Çizgiler kâğıda ve siyaha aynı hizada değil, kademeli girer (her çizginin eşiği ayrı; uçlar sivrilir):
          // ton geçişlerinde düz bir sınır çizgisi ya da daire izi kalmaz.
          const hb = HSH[(U | 0) & 255], hg = HSH[((U + .5) | 0) + 97 & 255];
          const rb = r - SG * hb, rg = r + SG * hg;          // siyah çizgi en erken r = 0'da başlar; beyaz aralık en geç r = 1'de kapanır
          const f0 = st.f0, f1 = st.f1;
          d = f0 + (f1 - f0) * r;
          if (rb < 0) d = rb < -TW ? 0 : f0 * (1 + rb / TW);
          else if (rg > 1) d = rg > 1 + TW ? 1.2 : d + (1.2 - d) * (rg - 1) / TW;
          if (d < 1) d *= 1 + JT[ji] * JIT.th;
          if (d > capW && d < 1) d = capW;   // ışınsal taramada çizgi kalınlığı sabit kalır (uzakta kalınlaşıp hız çizgisine dönmez)
          ink = (d * .5 - (u > .5 ? u - .5 : .5 - u)) * Pl + .5;
          if (ink < 0) ink = 0; else if (ink > 1) ink = 1;
          if (fade < 1) ink *= fade;
          const ct = st.ct;
          if (d > ct) { // çapraz tarama: düz ikinci aile
            const cc = p.t === 0 ? p.c * Math.cos(st.cr) - p.s * Math.sin(st.cr) : Math.cos(st.cr - .5), ss = p.t === 0 ? p.s * Math.cos(st.cr) + p.c * Math.sin(st.cr) : Math.sin(st.cr - .5);
            let u2 = (wy * cc - wx * ss) * invP * 1.06 + .31 + 8192; u2 -= u2 | 0;
            const d2 = (d - ct) / (1 - ct);
            let k2 = (d2 * .5 - (u2 > .5 ? u2 - .5 : .5 - u2)) * Pdv * 1.06 + .5;
            if (k2 > 0) { if (k2 > 1) k2 = 1; ink = ink + k2 - ink * k2; }
          }
        }
        O[i] = pr + ir * ink; O[i + 1] = pg + ig * ink; O[i + 2] = pb + ib * ink; O[i + 3] = 255;
      }
    }
    out.save(); out.setTransform(1, 0, 0, 1, 0, 0);
    out.putImageData(img, 0, 0);
    out.drawImage(oc, 0, 0);
    out.restore();
  }
  // evre arabelleğine yazan modüller (FG.sculpt) için: yama rengi baytları
  function bufBytes(id) { const n = patches.length; patches.push({ t: 3, id }); return [n & 255, n >> 8, HB[n]]; }
  return { tc, tx, pc, px, oc, ox, STY, PAPER, INK, PHB, tone, pat, hatch, patGrad, phaseOf, begin, fill, getCam: () => cam, bufBytes,
    setT, frame, unframe, save, restore, engrave, JIT, inkCol: `rgb(${INK})`, paperCol: `rgb(${PAPER})` };
})();
