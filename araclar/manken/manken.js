// araclar/manken/manken.js: 3B manken + çizim gölgelendiricisi (WebGL2, kütüphanesiz). Tek global: MANKEN.
// Kural (başvuru r8/r1, kanal/motorlar/manken-cizim.md): biçimi ışık kurar, çizgi değil. Ton iki-üç sert basamak; geçişi
// yumuşatma değil fırça sürtmesi verir. Karanlık kütleler birbirine karışır; kenar yalnız ışığın değdiği yerde belirir.
// Işık bir kama ya da konidir; sınırı keskin.
//
// Geçişler (SwiftShader bütçesi: tek ışık, tek gölge haritası, tek son işlem):
//   1. gölge haritası (ışıktan derinlik, 1024²)
//   2. ana geçiş (ölçekli tuval): ışık × gölge × koni → fırçayla bozulmuş eşikle basamak; R = basamak, G = nesne kimliği, B = parıltı
//      Fırça dokusu NESNE UZAYINDA hesaplanır: kamera ya da figür kayınca doku yüzeye yapışık gider, ekrana yapışmaz.
//      Tohum iki karede bir değişir (15 çizim/sn); eşik yalnız basamak sınırında iş gördüğü için kaynama kenar bandında kalır.
//   3. son işlem (tam boy): palet, kontur (yalnız ışıklı yanda), plakalar (2B: k koyu, l mürekkep/yazı, a ışık), gren.
// Plakalar cernobil/lib/baski.js ve stanford/lib/ekran.js ile aynı sözleşmede (beyaz zemine siyah = mürekkep); 3B katman
// plakaların ALTINDA basılır: sahneyi model kurar, 2B ekler (yazı, ek gölge, ışık hüzmesi) üstüne biner.
//
// Kullanım (film.js çekimi içinde):
//   MANKEN.init(1920, 1080, {rs})               bir kez
//   plan('P04', (ctx, st) => {
//     const M = MANKEN; M.begin({palet: 'r8', isik: {...}, kamera: {...}, t: st.t});
//     M.kutu([0, .38, 0], [1.4, .04, .7], {ton: .5});   M.figur(ISKELET.POZ.dur([0, 0], 0), {gozluk: true});
//     M.k.fillRect(...)   (isteğe bağlı 2B plakalar, M.ekran([x,y,z]) ile 3B noktaya iğnelenir)
//     M.ciz(ctx);
//   });
// Belirlenimci: Math.random yok; doku tohumu t'den (floor(t·15)). Aynı t her işçide aynı kareyi verir.
'use strict';
const MANKEN = (() => {
  const M = {};
  const I = () => (typeof ISKELET !== 'undefined' ? ISKELET : null);
  let W, H, RS, DWp, DHp, OLC, glc, gl, P = {}, fbo, fboTex, smFbo, smTex, smN = 1024, quad, cK, cL, cA, texP = [];
  let SAH = null;                     // geçerli sahne
  const MESH = {};
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));

  // ---------------- matris (sütun öncelikli, Float32Array 16) ----------------
  const m4 = {
    mul(a, b) { const o = new Float32Array(16); for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) { let s = 0; for (let k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k]; o[c * 4 + r] = s; } return o; },
    persp(fovy, asp, n, f) { const t = 1 / Math.tan(fovy / 2), o = new Float32Array(16); o[0] = t / asp; o[5] = t; o[10] = (f + n) / (n - f); o[11] = -1; o[14] = 2 * f * n / (n - f); return o; },
    orto(l, r, b, t, n, f) { const o = new Float32Array(16); o[0] = 2 / (r - l); o[5] = 2 / (t - b); o[10] = -2 / (f - n); o[12] = -(r + l) / (r - l); o[13] = -(t + b) / (t - b); o[14] = -(f + n) / (f - n); o[15] = 1; return o; },
    bak(e, c, up) {
      const z = nrm(sub(e, c)); let x = nrm(crs(up, z)); if (!isFinite(x[0]) || len(x) < 1e-6) x = [1, 0, 0]; const y = crs(z, x);
      const o = new Float32Array(16); o[0] = x[0]; o[4] = x[1]; o[8] = x[2]; o[1] = y[0]; o[5] = y[1]; o[9] = y[2]; o[2] = z[0]; o[6] = z[1]; o[10] = z[2];
      o[12] = -dot(x, e); o[13] = -dot(y, e); o[14] = -dot(z, e); o[15] = 1; return o;
    },
    cer(c) { const o = new Float32Array(16); o.set([c.x[0], c.x[1], c.x[2], 0, c.y[0], c.y[1], c.y[2], 0, c.z[0], c.z[1], c.z[2], 0, c.o[0], c.o[1], c.o[2], 1]); return o; },
    tx(m, v) { const x = v[0], y = v[1], z = v[2]; return [m[0] * x + m[4] * y + m[8] * z + m[12], m[1] * x + m[5] * y + m[9] * z + m[13], m[2] * x + m[6] * y + m[10] * z + m[14], m[3] * x + m[7] * y + m[11] * z + m[15]]; },
  };
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]], dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const crs = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  const len = a => Math.hypot(a[0], a[1], a[2]), nrm = a => { const l = len(a) || 1; return [a[0] / l, a[1] / l, a[2] / l]; };
  M.m4 = m4;

  // ---------------- geometri üreticileri ----------------
  // Izgara (halkalar × dilimler) → düz dizi; köşe normali yüz normallerinin ortalaması. ek: köşe başına [oyuk, tonÇarpanı]
  function izgara(halkalar, kapakAlt, kapakUst, ters = false) {
    const nH = halkalar.length, nS = halkalar[0].length, pos = [], ek = [];
    const P_ = [], E_ = [];
    for (const h of halkalar) for (const v of h) { P_.push(v.p); E_.push([v.oyuk || 0, v.ton ?? 1]); }
    const N_ = P_.map(() => [0, 0, 0]);
    const tri = [];
    const ekle = (a, b, c) => { if (ters) [b, c] = [c, b]; tri.push([a, b, c]); const n = crs(sub(P_[b], P_[a]), sub(P_[c], P_[a])); for (const i of [a, b, c]) { N_[i][0] += n[0]; N_[i][1] += n[1]; N_[i][2] += n[2]; } };
    for (let i = 0; i < nH - 1; i++) for (let j = 0; j < nS; j++) {
      const a = i * nS + j, b = i * nS + (j + 1) % nS, c = (i + 1) * nS + j, d = (i + 1) * nS + (j + 1) % nS;
      ekle(a, b, c); ekle(b, d, c);
    }
    // kapaklar: merkez noktaya yelpaze
    const kapak = (hi, ust, o) => { const m = P_.length; P_.push(o); E_.push([0, 1]); N_.push([0, 0, 0]);
      for (let j = 0; j < nS; j++) { const a = hi * nS + j, b = hi * nS + (j + 1) % nS; if (ust) ekle(a, b, m); else ekle(b, a, m); } };
    if (kapakAlt) kapak(0, false, kapakAlt);
    if (kapakUst) kapak(nH - 1, true, kapakUst);
    const nor = [];
    for (const t of tri) for (const i of t) { pos.push(...P_[i]); const n = nrm(N_[i]); nor.push(...n); ek.push(...E_[i]); }
    return { pos: new Float32Array(pos), nor: new Float32Array(nor), ek: new Float32Array(ek) };
  }
  // Yuvarlatılmış uzuv (kemik uzayı: +Y boyunca 0..L), elips kesit (rx, rz), uçlar yarım küre benzeri
  function uzuv(L, r0, r1, o = {}) {
    const nS = o.dilim || 9, sx = o.sx || 1, sz = o.sz || 1, halk = [];
    const kesit = (y, r, cz = 0) => { const h = []; for (let j = 0; j < nS; j++) { const a = j / nS * Math.PI * 2; h.push({ p: [Math.sin(a) * r * sx, y, Math.cos(a) * r * sz + cz] }); } return h; };
    const uc = 4;
    for (let k = uc; k >= 1; k--) { const a = k / uc * Math.PI / 2; halk.push(kesit(-Math.sin(a) * r0 * .8, Math.cos(a) * r0)); }
    const orta = o.orta || [[0, 1], [1, 1]];          // [u, yarıçap çarpanı]
    for (const [u, k] of orta) halk.push(kesit(u * L, (r0 + (r1 - r0) * u) * k, (o.egri || 0) * Math.sin(Math.PI * u) * L));
    for (let k = 1; k <= uc; k++) { const a = k / uc * Math.PI / 2; halk.push(kesit(L + Math.sin(a) * r1 * .8, Math.cos(a) * r1)); }
    return izgara(halk, [0, -r0 * .8, 0], [0, L + r1 * .8, 0]);
  }
  // Kesitlerden gövde (kemik uzayı): [{y, rx, rz, cz}] — ön (+z) biraz basık, sırt yuvarlak
  function govde(kes, o = {}) {
    const nS = o.dilim || 12, halk = [];
    for (const k of kes) { const h = []; for (let j = 0; j < nS; j++) { const a = j / nS * Math.PI * 2, s = Math.sin(a), c = Math.cos(a);
      const on = c > 0 ? (k.onBasik ?? .9) : 1; h.push({ p: [s * k.rx, k.y, c * k.rz * on + (k.cz || 0)] }); } halk.push(h); }
    return izgara(halk, [0, kes[0].y, kes[0].cz || 0], [0, kes[kes.length - 1].y, kes[kes.length - 1].cz || 0]);
  }
  // Düzlemli baş (baş uzayı: y 0 çene altı .. ~.25 tepe; +z yüz). Elipsoit + çıkıntı/göçük (Asaro baş şeması gibi düzlemler):
  // kaş kemeri, göz çukuru (oyuk: gölgede kalır), elmacık, burun kaması, ağız çevresi, çene, kulak; çene altı boyuna çekilir.
  // Düz gölgeleme + sert basamak: yüz ayrıntıyla değil düzlemle okunur. Göz, ağız, kaş ÇİZİLMEZ.
  const BAS_MERKEZ = [0, .072, .028];   // boyun ucu çene hizasının üstünde, kafatası öne
  function bas() {
    const nS = 36, nR = 28, ax = .072, ay = .116, az = .095, C = BAS_MERKEZ, halk = [];
    const g = (p, c, s) => Math.exp(-((p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2 + (p[2] - c[2]) ** 2) / (s * s));
    for (let i = 0; i <= nR; i++) {
      const ph = -Math.PI / 2 + Math.PI * (i / nR) * .985 + .02, h = [];
      for (let j = 0; j < nS; j++) {
        const th = j / nS * Math.PI * 2, d = [Math.cos(ph) * Math.sin(th), Math.sin(ph), Math.cos(ph) * Math.cos(th)];
        let p = [d[0] * ax, d[1] * ay, d[2] * az];
        // alt yarı: çene daralır (V), ense boyuna çekilir
        if (p[1] < -.02) { const u = Math.min(1, (-.02 - p[1]) / .09); p[0] *= 1 - .3 * u; if (p[2] < 0) p[2] *= 1 - .55 * u; }
        if (p[2] > 0 && Math.abs(p[0]) < .06) p[2] *= .93;                       // yüz düzlüğü
        let k = 0, oyuk = 0, ton = 1;
        k += .011 * g(p, [0, .034, .085], .03) + .009 * g(p, [.03, .03, .075], .02) + .009 * g(p, [-.03, .03, .075], .02);   // kaş kemeri
        for (const sx of [1, -1]) { const e = g(p, [sx * .031, .01, .082], .019); k -= .019 * e; oyuk = Math.max(oyuk, Math.min(1, e * 1.6)); } // göz çukuru
        k += .01 * g(p, [.052, -.01, .06], .019) + .01 * g(p, [-.052, -.01, .06], .019);                                  // elmacık
        const by = (.03 - p[1]) / .058;                                                     // 0 kök (kaş arası) → 1 uç
        const burun = p[2] > .04 && by > 0 && by < 1.12 ? Math.max(0, 1 - Math.abs(p[0]) / (.011 + .007 * by)) * Math.min(1, by * 1.1) * (by > 1 ? 1 - (by - 1) / .12 : 1) : 0;
        k += .03 * burun;
        k -= .006 * g(p, [0, -.04, .085], .012);                                              // burun altı (dudak üstü çukuru)                                                                                                      // burun kaması
        k += .005 * g(p, [0, -.056, .08], .024) - .003 * g(p, [0, -.075, .085], .012);                                        // ağız çevresi + çene çukuru
        k += .011 * g(p, [0, -.098, .07], .02) + .006 * g(p, [.045, -.085, .03], .02) + .006 * g(p, [-.045, -.085, .03], .02); // çene + çene köşeleri
        k += .012 * g(p, [.074, .0, -.008], .017) + .012 * g(p, [-.074, .0, -.008], .017);                                    // kulak
        if ((p[1] > .045 && (p[2] < .055 || p[1] > .085)) || (p[2] < -.005 && p[1] > -.075) || (p[2] < .03 && Math.abs(p[0]) > .05 && p[1] > -.01 && p[1] < .06)) { k += .008; ton = .32; }   // saç: tepe, ense ve şakaklar (arkadan bakınca ten yüz gibi okunmasın)
        if (p[1] < -.06 && p[2] < .02) ton = .9;
        const n = [d[0] / ax, d[1] / ay, d[2] / az], nl = Math.hypot(...n);
        p = [p[0] + n[0] / nl * k + C[0], p[1] + n[1] / nl * k + C[1], p[2] + n[2] / nl * k + C[2]];
        h.push({ p, oyuk, ton });
      }
      halk.push(h);
    }
    return izgara(halk, [C[0], C[1] - ay * 1.02, C[2]], [C[0], C[1] + ay + .008, C[2] - .005]);
  }
  // kutu (yerel merkezli), yüz normalli
  function kutu(sx, sy, sz) {
    const x = sx / 2, y = sy / 2, z = sz / 2, pos = [], nor = [], ek = [];
    const yuz = (n, a, b, c, d) => { for (const p of [a, b, c, a, c, d]) { pos.push(...p); nor.push(...n); ek.push(0, 1); } };
    yuz([0, 0, 1], [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]); yuz([0, 0, -1], [x, -y, -z], [-x, -y, -z], [-x, y, -z], [x, y, -z]);
    yuz([1, 0, 0], [x, -y, z], [x, -y, -z], [x, y, -z], [x, y, z]); yuz([-1, 0, 0], [-x, -y, -z], [-x, -y, z], [-x, y, z], [-x, y, -z]);
    yuz([0, 1, 0], [-x, y, z], [x, y, z], [x, y, -z], [-x, y, -z]); yuz([0, -1, 0], [-x, -y, -z], [x, -y, -z], [x, -y, z], [-x, -y, z]);
    return { pos: new Float32Array(pos), nor: new Float32Array(nor), ek: new Float32Array(ek) };
  }
  // ayakkabı (ayak uzayı: bilek kökte, +z ileri, y yukarı); bilek .03 m yüksekte: taban y = -.03
  function ayakkabi() {
    const kes = [], nS = 8;
    for (const [z, w, hT, hB] of [[-.07, .035, .035, -.031], [-.03, .045, .05, -.031], [.04, .05, .03, -.031], [.11, .045, .018, -.031], [.15, .03, .012, -.031]]) {
      const h = []; for (let j = 0; j < nS; j++) { const a = j / nS * Math.PI * 2, s = Math.sin(a), c = Math.cos(a);
        h.push({ p: [s * w, c > 0 ? hB + (hT - hB) * (.5 + .5 * c) * 1 : hB + (hT - hB) * .5 * (1 + c), z] }); } kes.push(h);
    }
    // halkalar z boyunca: izgara y yerine z ile çalışır, sorun değil (kapak merkezleri ver)
    return izgara(kes, [0, -.01, -.075], [0, -.012, .155], true);
  }
  // gözlük: ince çerçeve + cam (cam yalnız parıltı olarak görünür; ek.x = 1 cam işareti). Opak koyu cam güneş/aynalı gözlük okunur.
  function gozluk() {
    const yc = BAS_MERKEZ[1] + .012, zc = BAS_MERKEZ[2] + .097, parca = [];
    const tasi = (g, d, cam) => { const p = g.pos.slice(), e = g.ek.slice(); for (let i = 0; i < p.length; i += 3) { p[i] += d[0]; p[i + 1] += d[1]; p[i + 2] += d[2]; } if (cam) for (let i = 0; i < e.length; i += 2) e[i] = 1; return { pos: p, nor: g.nor, ek: e }; };
    for (const sx of [1, -1]) {
      const cx = sx * .025;
      parca.push(tasi(kutu(.034, .022, .002), [cx, yc, zc], true));
      parca.push(tasi(kutu(.036, .003, .004), [cx, yc + .0115, zc]), tasi(kutu(.036, .003, .004), [cx, yc - .0115, zc]));
      parca.push(tasi(kutu(.003, .022, .004), [cx + .0175, yc, zc]), tasi(kutu(.003, .022, .004), [cx - .0175, yc, zc]));
      parca.push(tasi(kutu(.003, .003, .085), [sx * .043, yc + .008, zc - .045]));          // sap
    }
    parca.push(tasi(kutu(.016, .003, .004), [0, yc + .006, zc + .001]));
    const cat = f => { const n = parca.reduce((s, g) => s + g[f].length, 0), o = new Float32Array(n); let i = 0; for (const g of parca) { o.set(g[f], i); i += g[f].length; } return o; };
    return { pos: cat('pos'), nor: cat('nor'), ek: cat('ek') };
  }
  // ---------------- gölgelendiriciler ----------------
  const GURULTU = `
float h21(vec2 p){ p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
  return mix(mix(h21(i), h21(i + vec2(1, 0)), f.x), mix(h21(i + vec2(0, 1)), h21(i + vec2(1, 1)), f.x), f.y); }`;
  const VS_G = `#version 300 es
in vec3 aP; uniform mat4 uM, uL; void main(){ gl_Position = uL * uM * vec4(aP, 1.); }`;
  const FS_G = `#version 300 es
precision mediump float; out vec4 o; void main(){ o = vec4(1.); }`;
  const VS_A = `#version 300 es
in vec3 aP; in vec3 aN; in vec2 aE;
uniform mat4 uM, uVP, uL;
out vec3 vW, vN, vO; out vec4 vL; out vec2 vE;
void main(){ vec4 w = uM * vec4(aP, 1.); vW = w.xyz; vO = aP; vN = mat3(uM) * aN; vE = aE; vL = uL * w; gl_Position = uVP * w; }`;
  const FS_A = `#version 300 es
precision highp float;
in vec3 vW, vN, vO; in vec4 vL; in vec2 vE;
out vec4 o;
uniform sampler2D tS;
uniform vec3 uLp, uLd, uKam; uniform float uSpot, uCos, uOrtam, uTon, uKim, uDuz, uTohum, uFirca, uCam, uSert, uIlk, uBir;
uniform vec3 uEs; uniform float uDis, uKaz, uCamY, uYan;
${GURULTU}
void main(){
  vec3 n = normalize(uDuz > .5 ? cross(dFdx(vW), dFdy(vW)) : vN);
  if (!gl_FrontFacing && uDuz < .5) n = -n;
  vec3 L = uSpot > .5 ? normalize(uLp - vW) : -uLd;
  float nl = max(dot(n, L), 0.);
  // gölge haritası (tek örnek: sert kenar)
  vec3 lc = vL.xyz / vL.w * .5 + .5;
  float sd = texture(tS, lc.xy).r;
  float yan = uYan * (1. + 2.5 * (1. - nl));
  float gol = (lc.x < 0. || lc.x > 1. || lc.y < 0. || lc.y > 1. || lc.z > 1.) ? uDis : step(lc.z - yan, sd);
  // fırça: nesne uzayında düşey kıl (genişlik ~1,5 cm, boy ~25 cm) + iri leke; tohum iki karede bir
  vec3 q = vO * uEs;
  float tt = uTohum * 7.31;
  float kil = vn(vec2((q.x + q.z) * 26. + tt, q.y * 2.6 + tt * .37)) * .62 + vn(vec2((q.x - q.z) * 60. - tt, q.y * 5. + 3.1)) * .38;
  float lek = vn(q.xy * 9. + q.zy * 7. + tt * .2);
  float br = (kil - .5) * .85 + (lek - .5) * .35;
  // koni: kenar keskin, fırçayla hafif tırtıklı
  float koni = 1.;
  if (uSpot > .5) { float ca = dot(normalize(vW - uLp), uLd); koni = step(uCos + br * .004 * uFirca, ca); }
  float isik = nl * gol * koni;
  // ışık basamağı: ışığın değdiği yer tek düz değer (sert); yarı açık geçiş fırçayla kırılır
  float ac = smoothstep(.0, .22 + br * .25 * uFirca, isik * uSert);
  // sıyıran ışık (düzlem ışığa yan bakıyor) orta tona düşer: yüz düzlemleri üç basamakta okunur
  float yuzey = mix(.42, 1., smoothstep(.22 + br * .1, .42 + br * .1, nl));
  float oy = uCam > .5 ? 0. : vE.x;
  float v = uTon * vE.y * (uOrtam * (1. - oy * .85) + ac * yuzey * uKaz * (1. - oy * .9));
  v += br * .07 * uFirca * ac * (1. - smoothstep(.6, .9, v));     // kuru fırça yalnız ışığın değdiği yerde; ışıksız kütle tek parça
  // basamaklar (uIlk: ilk eşikler) → 0 kara, 1 koyu, 2 orta, 3 ışık
  float b = v < uIlk ? 0. : (v < uBir ? 1. : (v < uBir * 2.6 ? 2. : 3.));
  // parıltı (gözlük camı): ışığın yansıdığı yerde küçük çapraz şerit
  float par = 0.;
  if (uCam > .5) { vec3 Vv = normalize(uKam - vW); vec3 Rr = reflect(-L, n); float sp = pow(max(dot(Rr, Vv), 0.), 6.) * gol * koni;
    float lx = vO.x - sign(vO.x) * .025, ly = vO.y - uCamY; float ser = step(abs(lx * .9 + ly - .003), .0014) * step(abs(lx + .004), .008);   // iki camda aynı yön, kısa
    par = step(.2, sp) * ser;
    if (vE.x > .5 && par < .5) discard; }
  // B kanalı: parıltı = 1; değilse kuru fırça izi (nesne uzayında; son işlem orta tonları bununla koyulaştırır, eşik değişmez)
  o = vec4(b / 3., uKim / 255., par > .5 ? 1. : kil * .9, 1.);
}`;
  const VS_Q = `#version 300 es
in vec2 p; out vec2 uv; void main(){ uv = p * .5 + .5; gl_Position = vec4(p, 0., 1.); }`;
  const FS_Q = `#version 300 es
precision highp float;
in vec2 uv; out vec4 o;
uniform sampler2D tM, tK, tL, tA; uniform vec2 res, mres; uniform float rs, seed, gren, kontur, vin, surt, kuru;
uniform vec3 p0, p1, p2, p3, pM, pP;
${GURULTU}
float lum(vec4 c){ return dot(c.rgb, vec3(.299, .587, .114)); }
void main(){
  vec2 fc = gl_FragCoord.xy; vec2 st = vec2(uv.x, 1. - uv.y);
  // kuru fırça saçağı: örnekleme noktası seyrek düşey şeritlerde yukarı kayar (üstteki kütle aşağı sarkar) ve yana titrer
  float sut = floor(fc.x / (2.5 * rs));
  float sx = h21(vec2(sut, seed * 1.7));
  float boy = pow(h21(vec2(sut + 31., floor(fc.y / (90. * rs)) + seed)), 4.) * step(.8, sx);
  vec2 uvb = uv + vec2((vn(vec2(fc.y / (9. * rs), seed * 3.)) - .5) * 2.2 / mres.x * rs, boy * surt * 16. * rs / res.y);
  vec4 m = texture(tM, uvb);
  float b = floor(m.r * 3. + .5);
  vec3 col = b < .5 ? p0 : (b < 1.5 ? p1 : (b < 2.5 ? p2 : p3));
  // kontur: nesne sınırı ya da iki basamak atlayan sınır; yalnız ışıklı yanda görünür (karanlıkta zaten erir)
  vec2 d = 1. / mres;
  float ek = 0., bmax = b;
  for (int i = 0; i < 4; i++) {
    vec2 o2 = i == 0 ? vec2(d.x, 0) : (i == 1 ? vec2(-d.x, 0) : (i == 2 ? vec2(0, d.y) : vec2(0, -d.y)));
    vec4 n = texture(tM, uvb + o2 * 1.2);
    float nb = floor(n.r * 3. + .5);
    bmax = max(bmax, nb);
    ek = max(ek, step(.5 / 255., abs(n.g - m.g)) + step(1.5, abs(nb - b)));
  }
  float kes = step(.32, h21(floor(fc / (5. * rs)) + seed * 3.1));   // çizgi kesik kesik (kuru fırça ucu)
  float cz = clamp(ek, 0., 1.) * step(1.5, bmax) * kes * kontur;
  col = mix(col, pM, cz * .9);
  // ışık plakası (a): siyah zemine beyaz = ışık; fırçalı eşikle açılır
  float dA = lum(texture(tA, st));
  float kilA = vn(vec2(fc.x / (2.2 * rs), fc.y / (120. * rs)) + seed * .7) ;
  float hz = step(.18 + (kilA - .5) * .22, dA) * step(.02, dA);
  col = mix(col, max(col, p2), hz);
  col = mix(col, p3, step(.62 + (kilA - .5) * .4, dA));
  // ton plakası (k) ve çizgi plakası (l): beyaz zemine siyah = mürekkep
  float dK = 1. - lum(texture(tK, st)); col = mix(col, p0, smoothstep(.2, .8, dK + (kilA - .5) * .25 * step(.02, dK)));
  float dL = 1. - lum(texture(tL, st)); col = mix(col, pM, smoothstep(.35, .62, dL));
  // orta tonlarda kuru fırça izi: düşey kıl lekeleri bir alt basamağa yaklaşır (koyu gri → kara, orta → koyu gri)
  float kz = m.b < .95 ? smoothstep(.58, .66, m.b) : 0.;
  col = mix(col, b > 1.5 ? p1 : p0, kz * kuru * step(.5, b) * step(b, 2.5));
  // parıltı: küçük, sıcak
  col = mix(col, pP, step(.95, m.b));
  // gren (iki karede bir) + hafif vinyet
  float g = h21(floor(fc / (1.5 * rs)) + seed * 17.13);
  col += (g - .5) * gren;
  col *= 1. - vin * smoothstep(.5, 1.05, length((st - .5) * vec2(1.25, 1.)));
  o = vec4(col, 1.);
}`;
  function sh(t, s) { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(x)); return x; }
  function prog(vs, fs, attrs) {
    const p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fs));
    attrs.forEach((a, i) => gl.bindAttribLocation(p, i, a)); gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
    const U = {}; const n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS);
    for (let i = 0; i < n; i++) { const u = gl.getActiveUniform(p, i); U[u.name] = gl.getUniformLocation(p, u.name); }
    return { p, U };
  }
  function vao(g) {
    const v = gl.createVertexArray(); gl.bindVertexArray(v);
    [[g.pos, 3], [g.nor, 3], [g.ek, 2]].forEach(([d, n], i) => { const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, d, gl.STATIC_DRAW); gl.enableVertexAttribArray(i); gl.vertexAttribPointer(i, n, gl.FLOAT, false, 0, 0); });
    gl.bindVertexArray(null); return { v, n: g.pos.length / 3 };
  }
  M.mesh = (ad, g) => { MESH[ad] = vao(g); };

  // ---------------- kurulum ----------------
  // o.olcek: ana geçişin çözünürlük çarpanı (1 = tam boy; .5 = yarım, büyütülür). o.smN: gölge haritası boyu
  M.init = (w = 1920, h = 1080, o = {}) => {
    W = w; H = h; RS = o.rs || 1; OLC = o.olcek ?? 1; smN = o.smN || 1024;
    DWp = Math.round(W * RS); DHp = Math.round(H * RS);
    glc = document.createElement('canvas'); glc.width = DWp; glc.height = DHp;
    gl = glc.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false, premultipliedAlpha: false, depth: true });
    if (!gl) throw new Error('WebGL2 yok');
    P.g = prog(VS_G, FS_G, ['aP']); P.a = prog(VS_A, FS_A, ['aP', 'aN', 'aE']); P.q = prog(VS_Q, FS_Q, ['p']);
    // ana geçiş hedefi
    const mw = Math.round(DWp * OLC), mh = Math.round(DHp * OLC);
    fboTex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, fboTex); gl.texStorage2D(gl.TEXTURE_2D, 1, gl.RGBA8, mw, mh);
    for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.NEAREST], [gl.TEXTURE_MAG_FILTER, gl.NEAREST], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v);
    const rb = gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER, rb); gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT24, mw, mh);
    fbo = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, fboTex, 0); gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, rb);
    fbo.w = mw; fbo.h = mh;
    // gölge haritası: derinlik dokusu
    smTex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, smTex); gl.texStorage2D(gl.TEXTURE_2D, 1, gl.DEPTH_COMPONENT24, smN, smN);
    for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.NEAREST], [gl.TEXTURE_MAG_FILTER, gl.NEAREST], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v);
    smFbo = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, smFbo); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.TEXTURE_2D, smTex, 0);
    gl.drawBuffers([gl.NONE]); gl.readBuffer(gl.NONE);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    // tam ekran dörtgen
    quad = gl.createVertexArray(); gl.bindVertexArray(quad); const qb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, qb);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0); gl.bindVertexArray(null);
    // 2B plakalar
    const mk = () => { const c = document.createElement('canvas'); c.width = DWp; c.height = DHp; return c; };
    cK = mk(); cL = mk(); cA = mk(); M.k = cK.getContext('2d'); M.l = cL.getContext('2d'); M.a = cA.getContext('2d');
    for (let i = 0; i < 3; i++) { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
      for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v);
      texP.push(t); }
    // manken parçaları (ölçüler ISKELET.OLCU ile aynı)
    const O = I().OLCU;
    M.mesh('kutu1', kutu(1, 1, 1));
    M.mesh('karin', govde([{ y: -.09, rx: .15, rz: .1 }, { y: -.03, rx: .165, rz: .108 }, { y: .06, rx: .148, rz: .1 }, { y: .15, rx: .14, rz: .098 }, { y: .24, rx: .15, rz: .1 }]));
    M.mesh('gogus', govde([{ y: 0, rx: .15, rz: .1 }, { y: .1, rx: .168, rz: .112 }, { y: .2, rx: .19, rz: .11, onBasik: .85 }, { y: .255, rx: .175, rz: .095 }, { y: .29, rx: .07, rz: .055 }]));
    M.mesh('boyun', uzuv(O.boyun + .03, .046, .041, { dilim: 8 }));
    M.mesh('bas', bas());
    M.mesh('uyluk', uzuv(O.uyluk, .078, .056, { orta: [[0, 1], [.35, 1.04], [1, 1]] }));
    M.mesh('baldir', uzuv(O.baldir, .054, .04, { orta: [[0, 1], [.3, 1.08], [1, 1]] }));
    M.mesh('pazu', uzuv(O.pazu, .044, .04, { dilim: 8 }));
    M.mesh('onkol', uzuv(O.onkol, .042, .033, { dilim: 8 }));
    M.mesh('el', uzuv(O.el * .72, .03, .022, { dilim: 6, sx: 1.25, sz: .6 }));
    M.mesh('ayak', ayakkabi());
    M.mesh('gozluk', gozluk());
  };

  // ---------------- sahne ----------------
  const PALET = {
    // r8: nötr gri, karenin onda yedisi koyu, beyaz yalnız ışığın değdiği yerde
    r8: { p: ['#0b0b0b', '#2b2b2b', '#6b6b6b', '#e9e7e2'], m: '#050505', par: '#f2b866' },
    // r1'den: tek sıcak aile, saf siyah ve saf beyaz yok
    r1: { p: ['#3a2429', '#5f3b36', '#a86d3c', '#f0bd62'], m: '#2a181c', par: '#fff0c0' },
  };
  M.PALET = PALET;
  const hex = h => [parseInt(h.slice(1, 3), 16) / 255, parseInt(h.slice(3, 5), 16) / 255, parseInt(h.slice(5, 7), 16) / 255];
  // begin(o): o.palet 'r8'|'r1'|{p:[4], m, par} · o.isik {tip:'spot'|'yon', konum, hedef, aci (derece, koni yarı açısı), alan (yön ışığı için orto yarı boy)}
  //   o.kamera {konum, hedef, fov (derece)} · o.ortam (0..1, karanlığın içi) · o.t saniye (doku tohumu) · o.firca (0..1) · o.esik [kara, koyu]
  M.begin = (o = {}) => {
    SAH = { o, ciz: [] };
    for (const [g, bg] of [[M.k, '#fff'], [M.l, '#fff'], [M.a, '#000']]) { g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.fillStyle = bg; g.fillRect(0, 0, DWp, DHp); g.setTransform(RS, 0, 0, RS, 0, 0); }
    const k = o.kamera || {}, kon = k.konum || [0, 1.6, 4], hed = k.hedef || [0, 1, 0];
    SAH.V = m4.bak(kon, hed, [0, 1, 0]); SAH.P = m4.persp((k.fov || 40) * Math.PI / 180, W / H, k.yakin || .05, k.uzak || 60); SAH.VP = m4.mul(SAH.P, SAH.V); SAH.kam = kon;
    const L = o.isik || { tip: 'yon', konum: [3, 6, 2], hedef: [0, 0, 0] }; SAH.L = L;
    const ld = nrm(sub(L.hedef, L.konum));
    if (L.tip === 'spot') SAH.LVP = m4.mul(m4.persp(Math.min(170, 2 * (L.aci || 30) + 6) * Math.PI / 180, 1, L.yakin || .1, L.uzak || 30), m4.bak(L.konum, L.hedef, Math.abs(ld[1]) > .95 ? [0, 0, 1] : [0, 1, 0]));
    else { const a = L.alan || 6; SAH.LVP = m4.mul(m4.orto(-a, a, -a, a, .1, L.uzak || 40), m4.bak(L.konum, L.hedef, Math.abs(ld[1]) > .95 ? [0, 0, 1] : [0, 1, 0])); }
    SAH.ld = ld;
  };
  // nesne kimliği: kontur nesne sınırında çizilir. Aynı kütle sayılacak parçalar aynı kimliği paylaşır (figürün bütün parçaları).
  let kimSay = 1;
  // ekle(mesh, matris, {ton, duz, cam, kim, es})
  // boya kipinde: o.renk [r,g,b] (0..1, yoksa ton gri), o.isima (ışık saçan yüzey: kapı, pencere, lamba; 0..)
  M.ekle = (mesh, mat, o = {}) => { SAH.ciz.push({ mesh, mat, ton: o.ton ?? .6, renk: o.renk || null, isima: o.isima || 0, duz: o.duz ? 1 : 0, cam: o.cam ? 1 : 0, kim: o.kim ?? (kimSay = kimSay % 250 + 1), es: o.es || [1, 1, 1], golgeYok: o.golgeYok }); };
  // kutu: merkez, boyut [x,y,z], {don: yaw rad, ton, kim}
  M.kutu = (c, s, o = {}) => {
    const a = o.don || 0, ca = Math.cos(a), sa = Math.sin(a), m = new Float32Array(16);
    m.set([ca * s[0], 0, -sa * s[0], 0, 0, s[1], 0, 0, sa * s[2], 0, ca * s[2], 0, c[0], c[1], c[2], 1]);
    M.ekle('kutu1', m, { duz: 1, es: s, ...o });
  };
  // figür: poz (ISKELET) → parçalar. o.ton (giysi, koyu), o.yuz (ten), o.gozluk
  M.figur = (poz, o = {}) => {
    const K = I().kemikler(poz), kim = o.kim ?? 251, gt = o.ton ?? .07, yt = o.yuz ?? .19, f = m4.cer;
    // boya kipinde renkler: o.giysi (palto), o.ten, o.pantolon
    const GR = o.giysi || [.16, .13, .16], TN = o.ten || [.62, .45, .36], PN = o.pantolon || GR.map(x => x * .8);
    const kemik = (c, ad, t = gt, ek = {}) => M.ekle(ad, f(c), { ton: t, kim, renk: GR, ...ek });
    kemik(K.pelvis, 'karin', gt, { renk: PN }); kemik(K.gogus, 'gogus');
    kemik(K.boyun, 'boyun', yt * .8, { renk: TN });
    kemik(K.bas, 'bas', yt, { renk: TN });
    if (o.gozluk) M.ekle('gozluk', f(K.bas), { ton: .08, kim, cam: 1, duz: 1 });
    for (const b of K.bacak) { kemik(b.uyluk, 'uyluk', gt, { renk: PN }); kemik(b.baldir, 'baldir', gt, { renk: PN }); kemik(b.ayak, 'ayak', gt * .6, { renk: PN.map(x => x * .6) }); }
    for (const k of K.kol) { kemik(k.pazu, 'pazu'); kemik(k.onkol, 'onkol'); kemik(k.el, 'el', yt * .85, { renk: TN.map(x => x * .9) }); }
    return K;
  };
  // dünya noktası → ekran (W×H piksel; 2B plakalara iğnelemek için)
  M.ekran = p => { const c = m4.tx(SAH.VP, p); return [(c[0] / c[3] * .5 + .5) * W, (1 - (c[1] / c[3] * .5 + .5)) * H, c[3]]; };

  // ---------------- çizim ----------------
  M.ciz = (ctx) => {
    if (SAH.o.kip === 'boya') return cizBoya(ctx);
    const o = SAH.o, L = SAH.L;
    const pal = typeof o.palet === 'object' ? o.palet : PALET[o.palet || 'r8'];
    const tohum = Math.floor((o.t || 0) * 15) % 97 + 1;     // iki karede bir (30 fps)
    gl.enable(gl.DEPTH_TEST); gl.depthFunc(gl.LEQUAL);
    // 1. gölge haritası
    gl.bindFramebuffer(gl.FRAMEBUFFER, smFbo); gl.viewport(0, 0, smN, smN); gl.clear(gl.DEPTH_BUFFER_BIT);
    gl.useProgram(P.g.p); gl.uniformMatrix4fv(P.g.U.uL, false, SAH.LVP);
    gl.enable(gl.POLYGON_OFFSET_FILL); gl.polygonOffset(1.5, 3);
    for (const d of SAH.ciz) { if (d.golgeYok) continue; const m = MESH[d.mesh]; gl.uniformMatrix4fv(P.g.U.uM, false, d.mat); gl.bindVertexArray(m.v); gl.drawArrays(gl.TRIANGLES, 0, m.n); }
    gl.disable(gl.POLYGON_OFFSET_FILL);
    // 2. ana geçiş
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo); gl.viewport(0, 0, fbo.w, fbo.h);
    gl.clearColor(clamp(Math.round(o.gok || 0) / 3), 0, 0, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);   // gök: basamak 0..3
    const U = P.a.U; gl.useProgram(P.a.p);
    gl.uniformMatrix4fv(U.uVP, false, SAH.VP); gl.uniformMatrix4fv(U.uL, false, SAH.LVP);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, smTex); gl.uniform1i(U.tS, 0);
    gl.uniform3fv(U.uLp, L.konum); gl.uniform3fv(U.uLd, SAH.ld); gl.uniform3fv(U.uKam, SAH.kam);
    gl.uniform1f(U.uSpot, L.tip === 'spot' ? 1 : 0); gl.uniform1f(U.uDis, L.tip === 'spot' ? 1 : 0); gl.uniform1f(U.uKaz, L.kazanc ?? 2); gl.uniform1f(U.uCamY, BAS_MERKEZ[1] + .012); gl.uniform1f(U.uYan, L.tip === 'spot' ? .00012 : .006 / ((L.uzak || 40) - .1)); gl.uniform1f(U.uCos, Math.cos((L.aci || 30) * Math.PI / 180));
    gl.uniform1f(U.uOrtam, o.ortam ?? .1); gl.uniform1f(U.uTohum, tohum); gl.uniform1f(U.uFirca, o.firca ?? 1); gl.uniform1f(U.uSert, L.guc ?? 1);
    const es = o.esik || [.045, .16]; gl.uniform1f(U.uIlk, es[0]); gl.uniform1f(U.uBir, es[1]);
    for (const d of SAH.ciz) {
      const m = MESH[d.mesh];
      gl.uniformMatrix4fv(U.uM, false, d.mat); gl.uniform1f(U.uTon, d.ton); gl.uniform1f(U.uKim, d.kim); gl.uniform1f(U.uDuz, d.duz); gl.uniform1f(U.uCam, d.cam);
      gl.uniform3fv(U.uEs, d.es);
      gl.bindVertexArray(m.v); gl.drawArrays(gl.TRIANGLES, 0, m.n);
    }
    gl.disable(gl.DEPTH_TEST);
    // 3. son işlem
    gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, DWp, DHp);
    const Q = P.q.U; gl.useProgram(P.q.p);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, fboTex); gl.uniform1i(Q.tM, 0);
    [cK, cL, cA].forEach((c, i) => { gl.activeTexture(gl.TEXTURE1 + i); gl.bindTexture(gl.TEXTURE_2D, texP[i]); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, c); });
    gl.uniform1i(Q.tK, 1); gl.uniform1i(Q.tL, 2); gl.uniform1i(Q.tA, 3);
    gl.uniform2f(Q.res, DWp, DHp); gl.uniform2f(Q.mres, fbo.w, fbo.h); gl.uniform1f(Q.rs, RS); gl.uniform1f(Q.seed, tohum);
    gl.uniform1f(Q.gren, o.gren ?? .045); gl.uniform1f(Q.surt, o.surtme ?? 1); gl.uniform1f(Q.kuru, o.kuru ?? .55); gl.uniform1f(Q.kontur, o.kontur ?? 1); gl.uniform1f(Q.vin, o.vinyet ?? .25);
    pal.p.forEach((h, i) => gl.uniform3fv(Q['p' + i], hex(h))); gl.uniform3fv(Q.pM, hex(pal.m)); gl.uniform3fv(Q.pP, hex(pal.par));
    gl.bindVertexArray(quad); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); gl.bindVertexArray(null);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    ctx.drawImage(glc, 0, 0, ctx.canvas.width, ctx.canvas.height); ctx.restore();
  };
  // boya kipinde son çizilen ana geçişi oku (resim motoruna referans olarak vermek için):
  // { w, h, renk: Uint8Array RGBA (renk hedefi), ek: Uint8Array RGBA (R derinlik, G nesne kimliği) }; satırlar alttan üste (GL düzeni)
  M.oku = () => {
    const w = fboB.w, h = fboB.h, renk = new Uint8Array(w * h * 4), ek = new Uint8Array(w * h * 4);
    gl.bindFramebuffer(gl.FRAMEBUFFER, fboB);
    gl.readBuffer(gl.COLOR_ATTACHMENT0); gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, renk);
    gl.readBuffer(gl.COLOR_ATTACHMENT1); gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, ek);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    return { w, h, renk, ek };
  };
  // yalnız ana geçişi çiz (son işlem ve tuvale basma yok): M.oku ile okunacak
  M.cizHam = () => { const c = { canvas: { width: 1, height: 1 }, save() {}, restore() {}, setTransform() {}, drawImage() {} }; cizBoya(c); };
  // ölçüm: GPU işini bitir (kare süresi ölçerken)
  M.bitir = () => { const px = new Uint8Array(4); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); };

  // =====================================================================================================
  // BOYA KİPİ (o.kip = 'boya'): kullanıcının örneklerinden (26 Kasım): renkli ışık, hava, boya izi, toz.
  //   Sıcak ışık / soğuk gölge; ışık hüzmesi gölge haritasında yürüyerek (gerçek: pencereden geçen ışık şerit şerit);
  //   sis derinlikle; ışık saçan yüzeylerin çevresinde parıltı; hüzmede yanan toz zerreleri; nesne uzayında fırça darbesi.
  //   Geçişler: gölge haritası → ana geçiş (2 hedef: renk, [derinlik, kimlik, parıltı]) → toz noktaları → son işlem.
  // =====================================================================================================
  const FS_B = `#version 300 es
precision highp float;
in vec3 vW, vN, vO; in vec4 vL; in vec2 vE;
layout(location = 0) out vec4 o0; layout(location = 1) out vec4 o1;
uniform sampler2D tS;
uniform mat4 uL;
uniform vec3 uLp, uLd, uKam, uEs, uRenk, uIsikR, uGolR, uSisR;
uniform float uSpot, uCos, uOrtam, uKim, uDuz, uTohum, uFirca, uCam, uKaz, uDis, uYan, uCamY, uIsima, uSisY, uHuzme, uUzak, uAdim;
uniform vec4 uNk[8]; uniform vec3 uNr[8]; uniform int uNn;   // gölgesiz renkli nokta ışıklar (kapı, lamba): konum + yarıçap, renk
${GURULTU}
float golge(vec3 p){ vec4 l = uL * vec4(p, 1.); vec3 c = l.xyz / l.w * .5 + .5;
  if (c.x < 0. || c.x > 1. || c.y < 0. || c.y > 1. || c.z > 1.) return uDis;
  float s = step(c.z - uYan * 2., texture(tS, c.xy).r);
  if (uSpot > .5) s *= step(uCos, dot(normalize(p - uLp), uLd));
  return s; }
void main(){
  vec3 n = normalize(uDuz > .5 ? cross(dFdx(vW), dFdy(vW)) : vN);
  if (!gl_FrontFacing && uDuz < .5) n = -n;
  vec3 L = uSpot > .5 ? normalize(uLp - vW) : -uLd;
  float nl = max(dot(n, L), 0.);
  vec3 lc = vL.xyz / vL.w * .5 + .5;
  float yan = uYan * (1. + 2.5 * (1. - nl));
  float gol = (lc.x < 0. || lc.x > 1. || lc.y < 0. || lc.y > 1. || lc.z > 1.) ? uDis : step(lc.z - yan, texture(tS, lc.xy).r);
  vec3 q = vO * uEs; float tt = uTohum * 7.31;
  // fırça darbesi: nesne uzayında yönlü (yatay yüzeyde uzun, dikeyde düşey), iki ölçek
  float kil = vn(vec2((q.x + q.z) * 18. + tt * .3, q.y * 2.2 + tt * .11)) * .6 + vn(vec2((q.x - q.z) * 7. - tt * .2, q.y * 1.1 + 3.1)) * .4;
  float yat = vn(vec2(q.x * 2.4 + tt * .1, q.z * 16. + q.y * 9.));
  float darbe = mix(kil, yat, step(.7, abs(n.y)));
  float lek = vn(q.xy * 3. + q.zy * 2.5 + 5.);
  float br = (darbe - .5);
  float koni = 1.;
  if (uSpot > .5) koni = step(uCos + br * .004 * uFirca, dot(normalize(vW - uLp), uLd));
  float isik = nl * gol * koni;
  float ac = smoothstep(.0, .2 + br * .35 * uFirca, isik);
  float yuzey = mix(.45, 1., smoothstep(.2 + br * .12, .5 + br * .12, nl));
  vec3 alb = uRenk * vE.y * (1. + br * .38 * uFirca);
  alb *= mix(vec3(.94, .98, 1.08), vec3(1.07, 1., .9), lek);           // darbe darbe sıcak-soğuk kayması
  float oy = uCam > .5 ? 0. : vE.x;
  // gölge ışıkla aynı yüzeyde: soğuk ortam + tabandan hafif sıcak sekme
  vec3 gol_ = uGolR * uOrtam * (1. - oy * .8) * (1. + .35 * max(-n.y, 0.));
  vec3 nok = vec3(0.);
  for (int i = 0; i < 8; i++) { if (i >= uNn) break; vec3 dv = uNk[i].xyz - vW; float dd = length(dv);
    float a = max(dot(n, dv / dd), 0.) / (1. + dd * dd / (uNk[i].w * uNk[i].w)) * (1. - smoothstep(uNk[i].w * 2.2, uNk[i].w * 3., dd));
    nok += uNr[i] * smoothstep(.0, .12 + br * .1 * uFirca, a) * (.55 + .45 * smoothstep(.15, .5, a)); }
  vec3 c = alb * (gol_ + uIsikR * ac * yuzey * uKaz * (1. - oy * .9) + nok * (1. - oy * .6));
  if (uIsima > 0.) c = uRenk * uIsima * (1. + br * .3 + (lek - .5) * .25);   // ışık saçan yüzey ışık almaz, kendisi ışıktır
  // parıltı (gözlük)
  float par = 0.;
  if (uCam > .5) { vec3 Vv = normalize(uKam - vW); vec3 Rr = reflect(-L, n); float sp = pow(max(dot(Rr, Vv), 0.), 6.) * gol * koni;
    float lx = vO.x - sign(vO.x) * .025, ly = vO.y - uCamY; par = step(.2, sp) * step(abs(lx * .9 + ly - .003), .0014) * step(abs(lx + .004), .008);
    if (vE.x > .5 && par < .5) discard; }
  // hava: sis + ışık hüzmesi (kameradan yüzeye 14 adım; adım başı titreşim tanecik verir, iki karede bir değişir)
  vec3 Vw = vW - uKam; float D = length(Vw);
  float sis = 1. - exp(-D * uSisY);
  float hz = 0.;
  if (uHuzme > 0.) {
    float j = h21(gl_FragCoord.xy * .73 + uTohum * 1.37);
    float Dm = min(D, uAdim);
    for (int i = 0; i < 9; i++) { float u = (float(i) + j) / 9.; hz += golge(uKam + Vw / D * Dm * u); }
    hz = hz / 9. * Dm;
  }
  c = mix(c, uSisR, sis) + uIsikR * hz * uHuzme;
  o0 = vec4(c, 1.);
  o1 = vec4(clamp(D / uUzak, 0., 1.), uKim / 255., par, 1.);
}`;
  // toz zerreleri: noktalar; yalnız ışığın içindekiler görünür (gölge haritası), yuvarlak, sıcak
  const VS_T = `#version 300 es
in vec3 aP;
uniform mat4 uVP, uL; uniform float uT, uBoy;
out vec3 vW; out vec4 vL; out float vH;
void main(){
  vec3 b = aP;
  vec3 p = b + vec3(sin(uT * .23 + b.z * 2.1 + b.y), sin(uT * .17 + b.x * 3.3) * .7 - uT * .015, cos(uT * .19 + b.y * 2.7 + b.x)) * .22;
  vW = p; vL = uL * vec4(p, 1.); vH = fract(sin(dot(b, vec3(12.9898, 78.233, 37.719))) * 43758.5453);
  gl_Position = uVP * vec4(p, 1.);
  gl_PointSize = clamp(uBoy * (.6 + vH) / gl_Position.w, 1., 9.);
}`;
  const FS_T = `#version 300 es
precision highp float;
in vec3 vW; in vec4 vL; in float vH;
layout(location = 0) out vec4 o0; layout(location = 1) out vec4 o1;
uniform sampler2D tS; uniform vec3 uIsikR, uKam, uLp, uLd; uniform float uDis, uSpot, uCos, uUzak, uParla;
void main(){
  vec2 d = gl_PointCoord - .5; if (dot(d, d) > .25) discard;
  vec3 c = vL.xyz / vL.w * .5 + .5;
  float s = (c.x < 0. || c.x > 1. || c.y < 0. || c.y > 1. || c.z > 1.) ? uDis : step(c.z - .002, texture(tS, c.xy).r);
  if (uSpot > .5) s *= step(uCos, dot(normalize(vW - uLp), uLd));
  if (s < .5) discard;
  o0 = vec4(uIsikR * uParla * (.55 + vH * .9), 1.);
  o1 = vec4(clamp(length(vW - uKam) / uUzak, 0., 1.), 254. / 255., 0., 1.);
}`;
  const FS_QB = `#version 300 es
precision highp float;
in vec2 uv; out vec4 o;
uniform sampler2D tM, tX, tK, tL, tA; uniform vec2 res, mres; uniform float rs, seed, gren, kontur, vin, surt, pariltiG, doy;
uniform vec3 pGol, pIsik, pM, pP;
${GURULTU}
float lum(vec3 c){ return dot(c, vec3(.299, .587, .114)); }
void main(){
  vec2 fc = gl_FragCoord.xy; vec2 st = vec2(uv.x, 1. - uv.y);
  // kuru fırça saçağı (seyrek, kısa)
  float sut = floor(fc.x / (2.5 * rs));
  float boy = pow(h21(vec2(sut + 31., floor(fc.y / (90. * rs)) + seed)), 4.) * step(.82, h21(vec2(sut, seed * 1.7)));
  vec2 uvb = uv + vec2((vn(vec2(fc.y / (9. * rs), seed * 3.)) - .5) * 2. / mres.x * rs, boy * surt * 12. * rs / res.y);
  vec3 c = texture(tM, uvb).rgb; vec4 x = texture(tX, uvb);
  // ışık saçan yerlerin çevresinde parıltı (12 dokunuş, iki halka)
  vec3 g = vec3(0.);
  for (int i = 0; i < 12; i++) { float a = float(i) * .5236 + seed * .1; float r = (i < 6 ? 10. : 26.) * rs; vec3 s = texture(tM, uv + vec2(cos(a), sin(a)) * r / res).rgb; g += max(s - .62, 0.) * (i < 6 ? 1. : .6); }
  c += g / 12. * pariltiG;
  // ince koyu kenar: yalnız nesne sınırında ve derinlik sıçramasında (siluet), kesik kesik
  vec2 d = 1. / mres; float ek = 0.;
  for (int i = 0; i < 4; i++) { vec2 o2 = i == 0 ? vec2(d.x, 0) : (i == 1 ? vec2(-d.x, 0) : (i == 2 ? vec2(0, d.y) : vec2(0, -d.y)));
    vec4 n = texture(tX, uvb + o2 * 1.3); ek = max(ek, step(.5 / 255., abs(n.g - x.g)) * step(.015, abs(n.r - x.r))); }
  c = mix(c, c * pM, ek * kontur * step(.3, h21(floor(fc / (5. * rs)) + seed * 3.1)) * .8);
  // ton ayarı: gölgeler mora, ışıklar altına (bölünmüş tonlama); doygunluk
  float l = lum(c);
  c = mix(c, c * pGol * 1.6, (1. - smoothstep(.0, .45, l)) * .35);
  c = mix(c, c * pIsik * 1.15, smoothstep(.5, 1., l) * .3);
  c = mix(vec3(lum(c)), c, doy);
  // plakalar (2B ekler): a ışık (siyah zemine beyaz), k koyu, l mürekkep
  float dA = lum(texture(tA, st).rgb); c += pIsik * dA * .9;
  float dK = 1. - lum(texture(tK, st).rgb); c = mix(c, c * .25, dK);
  float dL = 1. - lum(texture(tL, st).rgb); c = mix(c, pM * .4, smoothstep(.35, .62, dL));
  c = mix(c, pP, x.b);
  // gren (iki karede bir) + vinyet
  c += (h21(floor(fc / (1.5 * rs)) + seed * 17.13) - .5) * gren;
  c *= 1. - vin * smoothstep(.45, 1.05, length((st - .5) * vec2(1.25, 1.)));
  o = vec4(c, 1.);
}`;
  let PB = null, fboB = null, texB0, texB1, tozVao = null, tozN = 0;
  function kurBoya() {
    PB = { a: prog(VS_A, FS_B, ['aP', 'aN', 'aE']), t: prog(VS_T, FS_T, ['aP']), q: prog(VS_Q, FS_QB, ['p']) };
    const mw = Math.round(DWp * (SAH.o.olcek ?? 1)), mh = Math.round(DHp * (SAH.o.olcek ?? 1));
    const tx = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texStorage2D(gl.TEXTURE_2D, 1, gl.RGBA8, mw, mh);
      for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v); return t; };
    texB0 = tx(); texB1 = tx();
    const rb = gl.createRenderbuffer(); gl.bindRenderbuffer(gl.RENDERBUFFER, rb); gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_COMPONENT24, mw, mh);
    fboB = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, fboB);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texB0, 0); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT1, gl.TEXTURE_2D, texB1, 0);
    gl.framebufferRenderbuffer(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT, gl.RENDERBUFFER, rb);
    gl.drawBuffers([gl.COLOR_ATTACHMENT0, gl.COLOR_ATTACHMENT1]);
    fboB.w = mw; fboB.h = mh;
    gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  }
  // toz: kutu [min, max] içinde n zerre (tohumlu, bir kez); boy piksel ölçeği
  M.toz = (kutuA, kutuB, n = 900, tohum = 7) => {
    let s = tohum; const r = () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
    const a = new Float32Array(n * 3); for (let i = 0; i < n; i++) for (let k = 0; k < 3; k++) a[i * 3 + k] = kutuA[k] + (kutuB[k] - kutuA[k]) * r();
    tozVao = gl.createVertexArray(); gl.bindVertexArray(tozVao); const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, a, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0); gl.bindVertexArray(null); tozN = n;
  };
  function cizBoya(ctx) {
    const o = SAH.o, L = SAH.L; if (!PB) kurBoya();
    const tohum = Math.floor((o.t || 0) * 15) % 97 + 1, R = o.renkler || {};
    const isikR = R.isik || [1.0, .78, .5], golR = R.golge || [.36, .32, .62], sisR = R.sis || [.09, .07, .13];
    gl.enable(gl.DEPTH_TEST); gl.depthFunc(gl.LEQUAL);
    // 1. gölge haritası
    gl.bindFramebuffer(gl.FRAMEBUFFER, smFbo); gl.viewport(0, 0, smN, smN); gl.clear(gl.DEPTH_BUFFER_BIT);
    gl.useProgram(P.g.p); gl.uniformMatrix4fv(P.g.U.uL, false, SAH.LVP);
    gl.enable(gl.POLYGON_OFFSET_FILL); gl.polygonOffset(1.5, 3);
    for (const d of SAH.ciz) { if (d.golgeYok) continue; const m = MESH[d.mesh]; gl.uniformMatrix4fv(P.g.U.uM, false, d.mat); gl.bindVertexArray(m.v); gl.drawArrays(gl.TRIANGLES, 0, m.n); }
    gl.disable(gl.POLYGON_OFFSET_FILL);
    // 2. ana geçiş
    gl.bindFramebuffer(gl.FRAMEBUFFER, fboB); gl.viewport(0, 0, fboB.w, fboB.h);
    gl.clearBufferfv(gl.COLOR, 0, new Float32Array([...sisR, 1])); gl.clearBufferfv(gl.COLOR, 1, new Float32Array([1, 0, 0, 1])); gl.clear(gl.DEPTH_BUFFER_BIT);
    const U = PB.a.U; gl.useProgram(PB.a.p);
    gl.uniformMatrix4fv(U.uVP, false, SAH.VP); gl.uniformMatrix4fv(U.uL, false, SAH.LVP);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, smTex); gl.uniform1i(U.tS, 0);
    gl.uniform3fv(U.uLp, L.konum); gl.uniform3fv(U.uLd, SAH.ld); gl.uniform3fv(U.uKam, SAH.kam);
    const spot = L.tip === 'spot' ? 1 : 0, cosA = Math.cos((L.aci || 30) * Math.PI / 180), yanV = spot ? .00012 : .006 / ((L.uzak || 40) - .1);
    gl.uniform1f(U.uSpot, spot); gl.uniform1f(U.uCos, cosA); gl.uniform1f(U.uDis, spot); gl.uniform1f(U.uYan, yanV);
    gl.uniform1f(U.uOrtam, o.ortam ?? .35); gl.uniform1f(U.uTohum, tohum); gl.uniform1f(U.uFirca, o.firca ?? 1); gl.uniform1f(U.uKaz, L.kazanc ?? 1.6);
    gl.uniform1f(U.uCamY, BAS_MERKEZ[1] + .012);
    gl.uniform3fv(U.uIsikR, isikR); gl.uniform3fv(U.uGolR, golR); gl.uniform3fv(U.uSisR, sisR);
    const NK = (o.noktalar || []).slice(0, 8), nk = new Float32Array(32), nr = new Float32Array(24);
    NK.forEach((n, i) => { nk.set([...n.konum, n.yaricap || 2], i * 4); nr.set(n.renk.map(x => x * (n.guc ?? 1)), i * 3); });
    gl.uniform4fv(U['uNk[0]'], nk); gl.uniform3fv(U['uNr[0]'], nr); gl.uniform1i(U.uNn, NK.length);
    gl.uniform1f(U.uSisY, o.sis ?? .035); gl.uniform1f(U.uHuzme, o.huzme ?? .03); gl.uniform1f(U.uUzak, (o.kamera || {}).uzak || 60); gl.uniform1f(U.uAdim, o.huzmeBoy ?? 18);
    for (const d of SAH.ciz) {
      const m = MESH[d.mesh], rk = d.renk || [d.ton, d.ton, d.ton];
      gl.uniformMatrix4fv(U.uM, false, d.mat); gl.uniform3fv(U.uRenk, rk); gl.uniform1f(U.uIsima, d.isima); gl.uniform1f(U.uKim, d.kim); gl.uniform1f(U.uDuz, d.duz); gl.uniform1f(U.uCam, d.cam);
      gl.uniform3fv(U.uEs, d.es); gl.bindVertexArray(m.v); gl.drawArrays(gl.TRIANGLES, 0, m.n);
    }
    // 3. toz
    if (tozVao && (o.toz ?? 1) > 0) {
      const T = PB.t.U; gl.useProgram(PB.t.p);
      gl.uniformMatrix4fv(T.uVP, false, SAH.VP); gl.uniformMatrix4fv(T.uL, false, SAH.LVP); gl.uniform1f(T.uT, o.t || 0); gl.uniform1f(T.uBoy, (o.tozBoy ?? 14) * RS * (SAH.o.olcek ?? 1));
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, smTex); gl.uniform1i(T.tS, 0);
      gl.uniform3fv(T.uIsikR, isikR); gl.uniform3fv(T.uKam, SAH.kam); gl.uniform3fv(T.uLp, L.konum); gl.uniform3fv(T.uLd, SAH.ld);
      gl.uniform1f(T.uDis, spot); gl.uniform1f(T.uSpot, spot); gl.uniform1f(T.uCos, cosA); gl.uniform1f(T.uUzak, (o.kamera || {}).uzak || 60); gl.uniform1f(T.uParla, o.toz ?? 1);
      gl.bindVertexArray(tozVao); gl.drawArrays(gl.POINTS, 0, tozN);
    }
    gl.disable(gl.DEPTH_TEST);
    // 4. son işlem
    gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, DWp, DHp);
    const Q = PB.q.U; gl.useProgram(PB.q.p);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, texB0); gl.uniform1i(Q.tM, 0);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, texB1); gl.uniform1i(Q.tX, 1);
    [cK, cL, cA].forEach((c, i) => { gl.activeTexture(gl.TEXTURE2 + i); gl.bindTexture(gl.TEXTURE_2D, texP[i]); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, c); });
    gl.uniform1i(Q.tK, 2); gl.uniform1i(Q.tL, 3); gl.uniform1i(Q.tA, 4);
    gl.uniform2f(Q.res, DWp, DHp); gl.uniform2f(Q.mres, fboB.w, fboB.h); gl.uniform1f(Q.rs, RS); gl.uniform1f(Q.seed, tohum);
    gl.uniform1f(Q.gren, o.gren ?? .05); gl.uniform1f(Q.kontur, o.kontur ?? .6); gl.uniform1f(Q.vin, o.vinyet ?? .35); gl.uniform1f(Q.surt, o.surtme ?? .6);
    gl.uniform1f(Q.pariltiG, o.parilti ?? 2.2); gl.uniform1f(Q.doy, o.doygunluk ?? 1.05);
    gl.uniform3fv(Q.pGol, golR); gl.uniform3fv(Q.pIsik, isikR); gl.uniform3fv(Q.pM, R.murekkep || [.35, .25, .4]); gl.uniform3fv(Q.pP, R.parilti || [1, .85, .55]);
    gl.bindVertexArray(quad); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); gl.bindVertexArray(null);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    ctx.drawImage(glc, 0, 0, ctx.canvas.width, ctx.canvas.height); ctx.restore();
  }
  return M;
})();
if (typeof window !== 'undefined') window.MANKEN = MANKEN;
