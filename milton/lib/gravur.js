// Gravür motoru: Doré'nin ağaç baskı diline yakın, tonu çizgi kalınlığıyla veren tarama.
// Sahne iki katmana çizilir:
//   ton katmanı (tx): gri değer (beyaz = kâğıt, siyah = tam mürekkep); ışık ve gölge burada boyanır,
//   desen katmanı (px): R = çizgi doğrultusu θ (0..255 → 0..π), G = çizgi evresi (0..255 → 0..1 periyot),
//                       B = üslup kimliği (GR.STY: periyot, çapraz tarama, dalga, kesiklik, titreşim).
// GR.engrave(out, cam) iki katmanı okuyup çıktıya paralel çizgilerle basar:
//   - koyuluk arttıkça çizgi kalınlaşır, eşik aşılınca çapraz tarama girer;
//   - açık ve orta tonlarda çizgiler her çizgiye özgü bir desenle kesik kesik kırılır (ağaç baskının imzası);
//   - çizgiler dünya koordinatındadır: kamera kayınca çizgiler sahneyle birlikte kayar (cam: {x, y, s});
//   - hareket eden nesneler evrelerini GR.phaseOf ile kaydırır, çizgiler nesneye yapışık kalır.
'use strict';
const GR = (() => {
  const w = DW, h = DH;
  const tc = makeCanvas(w, h), tx = tc.getContext('2d', { willReadFrequently: true });
  const pc = makeCanvas(w, h), px = pc.getContext('2d', { willReadFrequently: true });
  // kâğıt ve mürekkep (Doré baskıları: krem kâğıt, sıcak siyah)
  const PAPER = [234, 227, 211], INK = [20, 17, 15];
  const COS = new Float32Array(256), SIN = new Float32Array(256);
  for (let i = 0; i < 256; i++) { const a = i / 256 * Math.PI; COS[i] = Math.cos(a); SIN[i] = Math.sin(a); }
  // pürüzsüz 1B gürültü tablosu (çizgi titreşimi ve kesiklik), 1024 örnek, dairesel
  const NZ = new Float32Array(1024);
  { const r = rng(7), raw = Array.from({ length: 128 }, () => r() * 2 - 1);
    for (let i = 0; i < 1024; i++) { const f = i / 8, k = Math.floor(f), u = f - k, s = u * u * (3 - 2 * u); NZ[i] = raw[k % 128] * (1 - s) + raw[(k + 1) % 128] * s; } }
  // 2B gürültü dokusu 256×256 (yön titreşimi ve benek), dairesel, [-1, 1]
  const N2 = new Float32Array(65536);
  { for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) {
      let v = 0, a = .55, f = 1 / 32;
      for (let o = 0; o < 4; o++) { v += a * (noise2(x * f, y * f, 11 + o) * 2 - 1); a *= .5; f *= 2; }
      N2[y * 256 + x] = v; } }
  // üslup tablosu (P mantıksal px):
  //   cr = çapraz doğrultu farkı (θ birimi /256·π), ct = çapraz eşik (koyuluk), wv = dalga genliği (periyot), wf = dalga sıklığı,
  //   g = ton eğrisi üssü, ds = kesiklik (0..1), df = kesik sıklığı (1/px), jt = doğrultu titreşimi (θ birimi), ph = gürültü evresi
  const STY = [];
  function sty(id, o) { STY[id] = Object.assign({ P: 5.2, cr: 64, ct: .62, wv: .06, wf: 1 / 38, g: 1, ds: .5, df: 1 / 9, jt: 0, ph: id * 137 }, o); }
  sty(0, {});                                                   // genel
  sty(1, { P: 4.6, wv: .04, wf: 1 / 60, ct: .80, g: 1.1, ds: .55, df: 1 / 11 }); // gökyüzü: ince yatay çizgi, açıkta kırılır
  sty(2, { P: 4.8, wv: .12, wf: 1 / 30, ct: .70, ds: .85, df: 1 / 7, jt: 6 });   // bulut, duman: dalgalı, benekli
  sty(3, { P: 5.4, wv: .20, wf: 1 / 22, ct: .60, g: .9, ds: .45, df: 1 / 12 }); // alev: akan, kıvrak
  sty(4, { P: 4.0, wv: .08, wf: 1 / 20, ct: .45, cr: 84, ds: .9, df: 1 / 6, jt: 18 }); // kaya: benekli, çapraz
  sty(5, { P: 3.3, wv: .03, wf: 1 / 50, ct: .70, g: 1.05, ds: .25, df: 1 / 14 }); // ten: ince, yuvarlak
  sty(6, { P: 2.9, wv: .02, ct: .74, cr: 40, ds: .2, df: 1 / 16 });              // tüy, kanat zarı: çok ince
  sty(7, { P: 6.0, wv: .03, wf: 1 / 80, ct: .70, ds: .35, df: 1 / 14 });         // ışık huzmesi
  sty(8, { P: 4.4, wv: .14, wf: 1 / 26, ct: .64, ds: .7, df: 1 / 8 });          // su, göl yüzeyi
  sty(9, { P: 3.8, wv: .05, ct: .66, cr: 70, ds: .4, df: 1 / 10 });             // kumaş, zırh
  const DL = STY.map(s => { const a = new Float32Array(256); for (let i = 0; i < 256; i++) a[i] = Math.pow(1 - i / 255, s.g); return a; });

  // ── çizim yardımcıları ──
  const tone = (v, a = 1) => { const b = Math.round(clamp(v) * 255); return a < 1 ? `rgba(${b},${b},${b},${a})` : `rgb(${b},${b},${b})`; };
  // desen rengi: θ = çizgi doğrultusu (radyan), ph = evre (periyot), id = üslup
  // çizim dönüşümü açı durumu: yerel θ → dünya θ (döndürme, aynalama). setAng ile kurulur.
  let angRot = 0, angFlip = false;
  const setAng = (rot = 0, flip = false) => { angRot = rot; angFlip = flip; };
  const pat = (th, ph = 0, id = 0) => {
    if (angFlip) th = PI - th;
    th += angRot;
    const a = Math.round(((th % PI) + PI) % PI / PI * 256) & 255;
    const g = Math.round((((ph % 1) + 1) % 1) * 256) & 255;
    return `rgb(${a},${g},${id})`;
  };
  // nesne (dx, dy) kayınca çizgilerin de kayması için gereken evre
  const phaseOf = (th, dx, dy, id) => -(dy * Math.cos(th) - dx * Math.sin(th)) / STY[id].P;
  // θ doğrultusunda değişen doğrultu gradyanı (çizgileri kavislendirmek için): (x0,y0)→(x1,y1) boyunca θ0→θ1
  function patGrad(x0, y0, x1, y1, stops, ph = 0, id = 0) {
    const g = px.createLinearGradient(x0, y0, x1, y1);
    for (const [o, th] of stops) g.addColorStop(o, pat(th, ph, id));
    return g;
  }
  let cam = { x: 0, y: 0, s: 1 };
  function begin(bgTone = 1, bgTh = 0, bgId = 1, c = null) {
    cam = c || { x: 0, y: 0, s: 1 };
    for (const c of [tx, px]) { c.setTransform(RS, 0, 0, RS, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.filter = 'none'; }
    tx.fillStyle = tone(bgTone); tx.fillRect(0, 0, W, H);
    px.fillStyle = pat(bgTh, 0, bgId); px.fillRect(0, 0, W, H);
  }
  // bir yolu iki katmana birden doldur. toneStyle: renk ya da gradyan; hs: {th, ph, id} ya da {fill: hazır desen stili}
  function fill(path, toneStyle, hs, rule = 'nonzero') {
    if (toneStyle != null) { tx.fillStyle = toneStyle; tx.fill(path, rule); }
    if (hs) { px.fillStyle = hs.fill || pat(hs.th || 0, hs.ph || 0, hs.id || 0); px.fill(path, rule); }
  }
  // iki katmana aynı dönüşümü uygula
  function setT(a, b, c, d, e, f) { tx.setTransform(a, b, c, d, e, f); px.setTransform(a, b, c, d, e, f); }
  // yerel çizim çerçevesi: dünya (x,y)'de, ang radyan dönük, side = ±1 aynalı, k ölçekli. Dönüş: DOMMatrix (çıktı için RS'siz)
  function frame(x, y, ang = 0, side = 1, k = 1) {
    const m = new DOMMatrix().translate(x, y).rotate(ang * 180 / PI).scale(side * k, k);
    const d = new DOMMatrix().scale(RS).multiply(m);
    setT(d.a, d.b, d.c, d.d, d.e, d.f); setAng(ang, side < 0);
    return m;
  }
  function unframe() { setT(RS, 0, 0, RS, 0, 0); setAng(0, false); }
  function save() { tx.save(); px.save(); }
  function restore() { tx.restore(); px.restore(); }

  // ── basma ──
  let img = null;
  const nS = 256, invP = new Float32Array(nS), WF = new Float32Array(nS), PH = new Float32Array(nS), WV = new Float32Array(nS),
    CT = new Float32Array(nS), CR = new Uint8Array(nS), DS = new Float32Array(nS), DF = new Float32Array(nS), JT = new Float32Array(nS), PW = new Float32Array(nS);
  function prep(cs) {
    for (let k = 0; k < nS; k++) {
      const st = STY[k] || STY[0];
      PW[k] = st.P; invP[k] = 1 / st.P; WF[k] = st.wf; PH[k] = st.ph + 65536; WV[k] = st.wv; CT[k] = st.ct; CR[k] = st.cr;
      DS[k] = st.ds; DF[k] = st.df; JT[k] = st.jt;
    }
  }
  // cam: kamera (dünya → ekran) {x, y, s}: ekran = (dünya - [x,y]) * s. Çizgiler dünya biriminde (s ile büyür).
  function engrave(out, camArg = null) {
    if (camArg) cam = camArg;
    const T = tx.getImageData(0, 0, w, h).data, Pd = px.getImageData(0, 0, w, h).data;
    if (!img || img.width !== w) img = out.createImageData(w, h);
    const O = img.data;
    prep();
    const pr = PAPER[0], pg = PAPER[1], pb = PAPER[2], ir = INK[0] - pr, ig = INK[1] - pg, ib = INK[2] - pb;
    const k = 1 / (RS * cam.s), ox = cam.x, oy = cam.y, devPer = RS * cam.s; // 1 dünya birimi = devPer cihaz pikseli
    for (let y = 0; y < h; y++) {
      let i = y * w * 4;
      const wy = y * k + oy;
      for (let x = 0; x < w; x++, i += 4) {
        const id = Pd[i + 2];
        const d = DL[id] ? DL[id][T[i]] : DL[0][T[i]];
        let ink = 0;
        if (d > .004) {
          const wx = x * k + ox;
          let a = Pd[i];
          const jt = JT[id];
          let nz = 0;
          if (jt > 0) { nz = N2[((wy * .5) & 255) * 256 + ((wx * .5) & 255)]; a = (a + nz * jt + 256) & 255; }
          const c = COS[a], s = SIN[a];
          const along = wx * c + wy * s;
          const ai = along * WF[id] + PH[id], a0 = ai | 0, af = ai - a0;
          const wob = (NZ[a0 & 1023] * (1 - af) + NZ[(a0 + 1) & 1023] * af) * WV[id];
          let u = (wy * c - wx * s) * invP[id] + Pd[i + 1] * .00390625 + wob + 4096;
          const line = u | 0; u -= line;
          let hw = d * .5;
          const ds = DS[id];
          if (ds > 0) {
            // her çizginin kendi kesik deseni (çizgi sırası ile ayrışır); orta tonlarda en güçlü
            const di = along * DF[id] + line * 37.17 + PH[id], d0 = di | 0, dfr = di - d0;
            const dn = NZ[d0 & 1023] * (1 - dfr) + NZ[(d0 + 1) & 1023] * dfr;
            hw += ds * (dn * .5 - .08) * (d < .5 ? d * 1.1 + .12 : (1 - d) * 1.1 + .12) * .5;
          }
          const Pdv = PW[id] * devPer;
          ink = (hw - (u > .5 ? u - .5 : .5 - u)) * Pdv + .5;
          if (ink < 0) ink = 0; else if (ink > 1) ink = 1;
          const ct = CT[id];
          if (d > ct) {
            const b = (a + CR[id]) & 255, c2 = COS[b], s2 = SIN[b];
            let u2 = (wy * c2 - wx * s2) * invP[id] * 1.07 + .31 + wob * .7 + 4096;
            u2 -= u2 | 0;
            const d2 = (d - ct) / (1 - ct);
            let k2 = (d2 * .5 - (u2 > .5 ? u2 - .5 : .5 - u2)) * Pdv * 1.07 + .5;
            if (k2 > 0) { if (k2 > 1) k2 = 1; ink = ink + k2 - ink * k2; }
          }
        }
        O[i] = pr + ir * ink; O[i + 1] = pg + ig * ink; O[i + 2] = pb + ib * ink; O[i + 3] = 255;
      }
    }
    out.save(); out.setTransform(1, 0, 0, 1, 0, 0);
    out.putImageData(img, 0, 0);
    out.restore();
  }
  return { tc, tx, pc, px, STY, PAPER, INK, N2, tone, pat, setAng, patGrad, phaseOf, begin, fill, getCam: () => cam, COS, SIN, setT, frame, unframe, save, restore, engrave,
    inkCol: `rgb(${INK})`, paperCol: `rgb(${PAPER})` };
})();
