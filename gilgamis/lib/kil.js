// Kil kabartma motoru (Gılgamış). ORTAK DOSYA: yalnız başkan değiştirir.
// Sahne üç tuvale çizilir, sonra ışıkla birleştirilir:
//   R.b  yükseklik (taban): gri değer = yükseklik (0 zemin derinliği … 1 en yüksek kabartma). Bütünü yumuşatılır → yuvarlak kenarlı kabartma.
//   R.d  ayrıntı: 128 nötr; koyu = oyuk (kazınmış çizgi), açık = ince kabarık çizgi. Az yumuşatılır.
//   R.m  malzeme rengi (albedo). Varsayılan yaş kil. Lacivert taş, pişmiş tuğla, zift burada boyanır.
// Işık: R.L = {dir:[x,y,z] (yüzeyden ışığa), int, amb, col:[r,g,b], pts:[{x,y,z,r,i,col}] (meşale; ekran koordinatı), sh (gölge gücü)}
// Kamera: R.cam(cx, cy, z) üç tuvale aynı dönüşümü uygular; yükseklik ve yumuşatma yakınlaşmayla ölçeklenir (eğim sabit kalır).
// Sonra: R.after(ctx => …) ışıklandırılmış karenin üstüne (ateş parıltısı, su ışıltısı) çizilir; kamera dönüşümü R.T ile.
'use strict';
const makeCanvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
const gv = v => { const k = Math.max(0, Math.min(255, Math.round(v * 255))); return `rgb(${k},${k},${k})`; };   // yükseklik rengi
const dv = v => { const k = Math.max(0, Math.min(255, Math.round(128 + v * 127))); return `rgb(${k},${k},${k})`; }; // ayrıntı: -1 oyuk … +1 kabarık
const KIL = (() => {
  const w = DW, h = DH, N = w * h;
  const mk = () => { const c = makeCanvas(w, h); return [c, c.getContext('2d', { willReadFrequently: true })]; };
  const [cB, xB] = mk(), [cD, xD] = mk(), [cM, xM] = mk();
  const fB = new Float32Array(N), fA = new Float32Array(N), fT = new Float32Array(N), fD = new Float32Array(N), fH = new Float32Array(N);
  const out = new ImageData(w, h), O = out.data;
  // ---- dokular (dünya koordinatında desen: kamera ile birlikte kayar) ----
  const T = {};
  function dokular() {
    const S = 512;
    // kil rengi: büyük ölçekli lekeler + ince gren
    const c = makeCanvas(S, S), x = c.getContext('2d'), id = x.createImageData(S, S), d = id.data;
    const n = makeCanvas(S, S), nx = n.getContext('2d'), nd = nx.createImageData(S, S), q = nd.data;
    const r = rng(7);
    for (let y = 0; y < S; y++) for (let X = 0; X < S; X++) {
      // döşenebilir gürültü: periyodik örnekleme
      const per = (fx, fy, s) => { let v = 0, a = .55, f = fx; for (let o = 0; o < 4; o++) { const u = X / S * f, vv = y / S * f; v += a * tileN(u, vv, f, s + o); a *= .5; f *= 2; } return v; };
      const big = per(3, 3, 11), fine = per(24, 24, 31), k = (X + y * S) * 4;
      const t = .5 + (big - .5) * .9 + (fine - .5) * .35;
      d[k] = 176 + t * 46; d[k + 1] = 128 + t * 36; d[k + 2] = 86 + t * 24; d[k + 3] = 255;
      const bump = (per(12, 12, 51) - .5) * 1.1 + (r() - .5) * .25 + (per(48, 48, 71) - .5) * .6;
      const b = 128 + bump * 26; q[k] = q[k + 1] = q[k + 2] = b; q[k + 3] = 255;
    }
    x.putImageData(id, 0, 0); nx.putImageData(nd, 0, 0);
    T.kil = xM.createPattern(c, 'repeat'); T.kilPd = xD.createPattern(n, 'repeat');
    T.kilC = c; T.kilN = n;
  }
  // döşenebilir değer gürültüsü (periyot p)
  function tileN(u, v, p, s) {
    const i = Math.floor(u), j = Math.floor(v), fu = u - i, fv = v - j;
    const hh = (a, b) => hash2(((a % p) + p) % p, ((b % p) + p) % p, s);
    const su = fu * fu * (3 - 2 * fu), sv = fv * fv * (3 - 2 * fv);
    return lerp(lerp(hh(i, j), hh(i + 1, j), su), lerp(hh(i, j + 1), hh(i + 1, j + 1), su), sv);
  }
  // ---- kutu bulanıklığı (yerinde; iki yön) ----
  function blur(a, r, pass) {
    r = Math.max(1, Math.round(r)); const iw = 1 / (2 * r + 1);
    for (let p = 0; p < pass; p++) {
      for (let y = 0; y < h; y++) { // yatay a → fT
        const o = y * w; let s = a[o] * (r + 1);
        for (let x = 1; x <= r; x++) s += a[o + Math.min(x, w - 1)];
        for (let x = 0; x < w; x++) { fT[o + x] = s * iw; s += a[o + Math.min(x + r + 1, w - 1)] - a[o + Math.max(x - r, 0)]; }
      }
      for (let x = 0; x < w; x++) { // dikey fT → a
        let s = fT[x] * (r + 1);
        for (let y = 1; y <= r; y++) s += fT[Math.min(y, h - 1) * w + x];
        for (let y = 0; y < h; y++) { a[y * w + x] = s * iw; s += fT[Math.min(y + r + 1, h - 1) * w + x] - fT[Math.max(y - r, 0) * w + x]; }
      }
    }
  }
  // ---- sahne arayüzü ----
  const R = { b: xB, d: xD, m: xM, T, z: 1, L: null, _after: [], W: w, H: h };
  R.cam = (cx = W / 2, cy = H / 2, z = 1) => {
    R.z = z; R.cx = cx; R.cy = cy;
    for (const c of [xB, xD, xM]) { c.setTransform(RS * z, 0, 0, RS * z, RS * (W / 2 - cx * z), RS * (H / 2 - cy * z)); }
  };
  R.after = f => R._after.push(f);
  // dünya → ekran (mantıksal 1920×1080)
  R.scr = (x, y) => [W / 2 + (x - R.cx) * R.z, H / 2 + (y - R.cy) * R.z];
  R.begin = (o = {}) => {
    R._after = []; R.renk = null; R.z = 1; R.cx = W / 2; R.cy = H / 2;
    for (const c of [xB, xD, xM]) { c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.filter = 'none'; c.lineCap = 'round'; c.lineJoin = 'round'; }
    xB.fillStyle = gv(o.zemin ?? .18); xB.fillRect(0, 0, w, h);
    xD.fillStyle = 'rgb(128,128,128)'; xD.fillRect(0, 0, w, h);
    xM.fillStyle = o.renk || '#C08A5E'; xM.fillRect(0, 0, w, h);
    R.L = { dir: [-.55, -.6, .58], int: 1.0, amb: .34, col: [1, .97, .9], pts: [], sh: .75, spec: .08, ...(o.L || {}) };
    R.yb = o.yb ?? 9;      // taban yumuşatma yarıçapı (px, z=1)
    R.yh = o.yh ?? 120;    // yükseklik ölçeği (px, z=1)
    R.dh = o.dh ?? 5;      // ayrıntı derinliği
  };
  // dünya koordinatında kil dokusu: taban zemini, malzeme ve kabarcıklar bir dikdörtgene
  R.kilZemin = (x0, y0, x1, y1, o = {}) => {
    xM.save(); xM.fillStyle = T.kil; xM.globalAlpha = o.a ?? 1; xM.fillRect(x0, y0, x1 - x0, y1 - y0); xM.restore();
    xD.save(); xD.fillStyle = T.kilPd; xD.globalAlpha = o.pd ?? .9; xD.fillRect(x0, y0, x1 - x0, y1 - y0); xD.restore();
  };
  // ---- birleştirme ----
  function compose(ctx) {
    const z = R.z, L = R.L;
    const bd = xB.getImageData(0, 0, w, h).data, dd = xD.getImageData(0, 0, w, h).data, md = xM.getImageData(0, 0, w, h).data;
    for (let i = 0, k = 0; i < N; i++, k += 4) { fB[i] = bd[k] * (1 / 255); fD[i] = (dd[k] - 128) * (1 / 128); }
    blur(fB, R.yb * z * RS * .5, 2);
    fA.set(fB); blur(fA, R.yb * z * RS * 2.2, 1);   // oyuk gölgesi (ortam örtmesi) için geniş ortalama
    blur(fD, Math.max(1, .9 * z * RS), 1);
    const HS = R.yh * z * RS, DS = R.dh * Math.sqrt(z) * RS;
    for (let i = 0; i < N; i++) fH[i] = fB[i] * HS + fD[i] * DS;
    // yönlü ışık
    let [lx, ly, lz] = L.dir; const ln = Math.hypot(lx, ly, lz); lx /= ln; ly /= ln; lz /= ln;
    const pl = Math.hypot(lx, ly) || 1e-6, tanE = lz / pl, ux = lx / pl, uy = ly / pl;
    const st = [5, 12, 24].map(s => s * Math.max(.6, z) * RS), sx = st.map(s => Math.round(ux * s)), sy = st.map(s => Math.round(uy * s));
    const so = st.map((s, j) => sy[j] * w + sx[j]), rise = st.map(s => s * tanE);
    const hx = lx, hy = ly, hz = lz + 1, hn = Math.hypot(hx, hy, hz), Hx = hx / hn, Hy = hy / hn, Hz = hz / hn;
    const I = L.int, A = L.amb, [cr, cg, cb] = L.col, SH = L.sh, SP = L.spec * 255;
    const pts = (L.pts || []).map(p => ({ x: p.x * RS, y: p.y * RS, z: (p.z ?? 160) * RS, r2: Math.pow((p.r ?? 700) * RS, 2), i: p.i ?? 1, c: p.col || [1, .7, .4] }));
    for (let y = 1; y < h - 1; y++) {
      const row = y * w;
      for (let x = 1; x < w - 1; x++) {
        const i = row + x, k = i * 4, hc = fH[i];
        let nx = (fH[i - 1] - fH[i + 1]) * .5, ny = (fH[i - w] - fH[i + w]) * .5;
        const inl = 1 / Math.sqrt(nx * nx + ny * ny + 1); nx *= inl; ny *= inl; const nz = inl;
        let dif = nx * lx + ny * ly + nz * lz; if (dif < 0) dif = 0;
        // kabartma gölgesi: ışık yönünde üç örnek
        let sh = 0;
        for (let j = 0; j < 3; j++) {
          const xx = x + sx[j], yy = y + sy[j];
          if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue;
          const dlt = fH[i + so[j]] - hc - rise[j];
          if (dlt > 0) { const v = dlt / (3 + rise[j] * .5); if (v > sh) sh = v > 1 ? 1 : v; }
        }
        const lit = dif * (1 - sh * SH);
        let sp = nx * Hx + ny * Hy + nz * Hz; sp = sp > 0 ? sp * sp : 0; sp = sp * sp; sp = sp * sp * SP * (1 - sh);
        let cav = (fA[i] - fB[i]) * 3.2; cav = cav < 0 ? 0 : cav > .55 ? .55 : cav;
        const ao = (.86 + .14 * fB[i] + (fD[i] < 0 ? fD[i] * .25 : 0)) * (1 - cav);
        let r = A + I * lit * ao, g = r, b = r;
        r *= cr; g *= cg; b *= cb;
        for (const p of pts) { // meşale: noktasal ışık
          let px = p.x - x, py = p.y - y, pz = p.z - hc; const d2 = px * px + py * py;
          if (d2 > p.r2) continue;
          const il = 1 / Math.sqrt(d2 + pz * pz); px *= il; py *= il; pz *= il;
          let dd2 = nx * px + ny * py + nz * pz; if (dd2 <= 0) continue;
          const att = 1 - d2 / p.r2, e = dd2 * att * att * p.i * ao;
          r += e * p.c[0]; g += e * p.c[1]; b += e * p.c[2];
        }
        O[k] = md[k] * r + sp; O[k + 1] = md[k + 1] * g + sp * .92; O[k + 2] = md[k + 2] * b + sp * .8; O[k + 3] = 255;
      }
    }
    for (let x = 0; x < w; x++) { for (let c = 0; c < 4; c++) { O[x * 4 + c] = O[(w + x) * 4 + c]; O[((h - 1) * w + x) * 4 + c] = O[((h - 2) * w + x) * 4 + c]; } }
    for (let y = 0; y < h; y++) { for (let c = 0; c < 4; c++) { O[y * w * 4 + c] = O[(y * w + 1) * 4 + c]; O[(y * w + w - 1) * 4 + c] = O[(y * w + w - 2) * 4 + c]; } }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.putImageData(out, 0, 0); ctx.restore();
    for (const f of R._after) { ctx.save(); ctx.setTransform(RS * z, 0, 0, RS * z, RS * (W / 2 - R.cx * z), RS * (H / 2 - R.cy * z)); f(ctx); ctx.restore(); }
  }
  R.compose = compose;
  R.init = () => dokular();
  return R;
})();
