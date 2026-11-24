// Gazete baskısı motoru (Çernobil'in çayı). ORTAK DOSYA: yalnız başkan değiştirir.
// Her kare 1986 gazete kâğıdına basılır. Sahneler üç plakaya çizer, gölgelendirici basar:
//   B.k  TON plakası   (gri tonlu çizim: siyah = tam mürekkep) → 45°'lik kaba tram (gazete fotoğrafı)
//   B.l  ÇİZGİ plakası (dizgi, çizgi, düz siluet: siyah = mürekkep) → tramsız, düz mürekkep
//   B.c  ÇAY plakası   (renk B.cay(yoğunluk, ton): R = yoğunluk, G = ton 0 yeşil → .5 bakır → 1 kehribar) → 15°'lik tram, siyahın üstüne kayık basılır
// Görüntünün kuralları (uretim_plani.md §4): radyasyon hiç çizilmez (yalnız sayı); renk yalnız çayda; her söz bir kupür.
// Dünya koordinatı W×H (1920×1080). B.cam(x, y, z, r): kamera (x,y görüntünün ortasına gelen dünya noktası, z yakınlık) üç plakaya birden.
// Tram ızgarası ekrana sabittir (kamera kayınca görüntü ızgaranın altından geçer: her kare yeniden basılmış gibi).
'use strict';
const BASKI = (() => {
  const B = {};
  let cK, cL, cC, gl, glc, prog, tex = [], U = {};
  B.KARA = '#000'; B.MUR = '#221C17'; B.KAGIT = '#ECE2C9';
  B.cay = (d = 1, ton = .5, a = 1) => `rgba(${Math.round(clamp(d) * 255)},${Math.round(clamp(ton) * 255)},0,${a})`;
  B.ton = (d, a = 1) => { const v = Math.round((1 - clamp(d)) * 255); return `rgba(${v},${v},${v},${a})`; }; // d: mürekkep yoğunluğu 0..1
  const VS = `#version 300 es
in vec2 p; out vec2 uv; void main(){ uv = p * .5 + .5; gl_Position = vec4(p, 0., 1.); }`;
  const FS = `#version 300 es
precision highp float;
in vec2 uv; out vec4 o;
uniform sampler2D tK, tL, tC; uniform vec2 res; uniform vec2 kay; uniform float per, rs, gate, gateA, kagitA;
float h21(vec2 p){ p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
  return mix(mix(h21(i), h21(i + vec2(1, 0)), f.x), mix(h21(i + vec2(0, 1)), h21(i + vec2(1, 1)), f.x), f.y); }
float tram(vec2 fc, float ang, float d, float P){
  float c = cos(ang), s = sin(ang); vec2 q = mat2(c, -s, s, c) * fc / P;
  float sp = .5 - .25 * (cos(6.2831853 * q.x) + cos(6.2831853 * q.y));
  float aa = .5 * fwidth(sp) + .02;
  return smoothstep(sp - aa, sp + aa, d);
}
void main(){
  vec2 fc = gl_FragCoord.xy; vec2 st = vec2(uv.x, 1. - uv.y);
  float P = per * rs;
  // kâğıt: geniş lekeler + lif + ince gren (ekrana sabit, karede değişmez)
  float mot = vn(fc / (180. * rs)) * .6 + vn(fc / (60. * rs)) * .4;
  float lif = vn(vec2(fc.x / (3. * rs), fc.y / (40. * rs)) + 7.) * vn(vec2(fc.x / (40. * rs), fc.y / (3. * rs)) + 3.);
  float gr = h21(floor(fc / max(1., rs)));
  vec3 kagit = vec3(.925, .886, .788) * (1. - kagitA * (.05 * mot + .04 * lif + .025 * gr));
  vec3 kenar = vec3(1.) - .10 * kagitA * smoothstep(.55, 1.05, length((st - .5) * vec2(1.2, 1.)));
  kagit *= kenar;
  vec3 mur = vec3(.133, .110, .090);
  // geçit (merdane): gate > x olan yer basılı
  float g = gateA < .5 ? 1. : step(st.x, gate);
  // TON plakası: 45°
  float dK = 1. - dot(texture(tK, st).rgb, vec3(.299, .587, .114));
  dK = clamp(dK + (gr - .5) * .07 * step(.02, dK), 0., 1.);
  float cK = dK > .955 ? 1. : tram(fc, .7853982, dK, P);
  // ÇİZGİ plakası: düz mürekkep, kenarı hafif yenik
  float dL = 1. - dot(texture(tL, st).rgb, vec3(.299, .587, .114));
  float cL = smoothstep(.35 + (gr - .5) * .2, .62, dL);
  // ÇAY plakası: 15°, kayık
  vec4 cc = texture(tC, st + kay * rs / res);
  float dC = cc.r; float tn = cc.g;
  float cC = dC > .95 ? 1. : tram(fc + vec2(2.3, 1.7), .2617994, dC, P * .92);
  vec3 yesil = vec3(.36, .58, .24), bakir = vec3(.66, .38, .17), kehr = vec3(.70, .24, .12);
  vec3 cay = tn < .5 ? mix(yesil, bakir, tn * 2.) : mix(bakir, kehr, (tn - .5) * 2.);
  vec3 col = kagit;
  col *= mix(vec3(1.), cay, cC * .92 * g);
  col *= mix(vec3(1.), mur, cK * .94 * g);
  col *= mix(vec3(1.), mur, cL * .97 * g);
  o = vec4(col, 1.);
}`;
  function sh(type, src) { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
  B.init = () => {
    cK = makeCanvas(DW, DH); cL = makeCanvas(DW, DH); cC = makeCanvas(DW, DH);
    B.k = cK.getContext('2d'); B.l = cL.getContext('2d'); B.c = cC.getContext('2d');
    glc = document.createElement('canvas'); glc.width = DW; glc.height = DH;
    gl = glc.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false, premultipliedAlpha: false });
    prog = gl.createProgram(); gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
    gl.useProgram(prog);
    const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    for (let i = 0; i < 3; i++) { const t = gl.createTexture(); gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); tex.push(t); }
    for (const n of ['tK', 'tL', 'tC', 'res', 'kay', 'per', 'rs', 'gate', 'gateA', 'kagitA']) U[n] = gl.getUniformLocation(prog, n);
    gl.uniform1i(U.tK, 0); gl.uniform1i(U.tL, 1); gl.uniform1i(U.tC, 2);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
  };
  // begin(o): o.kay [x,y] çay plakasının kayması (px; varsayılan [3,2]) · o.per tram aralığı (px, 1080'de; varsayılan 7) · o.kagit kâğıt dokusu (0..1)
  let O = {};
  B.begin = (o = {}) => {
    O = o;
    for (const [g, bg] of [[B.k, '#fff'], [B.l, '#fff'], [B.c, '#000']]) { g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.filter = 'none'; g.fillStyle = bg; g.fillRect(0, 0, DW, DH); baseT(g); }
  };
  // kamera: (x, y) dünyada görüntünün ortası, z büyütme, r dönme (radyan). Üç plakaya birden uygulanır.
  B.cam = (x = W / 2, y = H / 2, z = 1, r = 0) => {
    for (const g of [B.k, B.l, B.c]) { baseT(g); g.translate(W / 2, H / 2); if (r) g.rotate(r); g.scale(z, z); g.translate(-x, -y); }
  };
  B.save = () => { B.k.save(); B.l.save(); B.c.save(); };
  B.restore = () => { B.k.restore(); B.l.restore(); B.c.restore(); };
  B.each = fn => { for (const g of [B.k, B.l, B.c]) fn(g); };   // ör. B.each(g => g.translate(...))
  // kısayollar
  B.siluet = (yol, o = {}) => { const g = o.ton ? B.k : B.l; g.save(); g.globalAlpha = o.a ?? 1; g.beginPath(); yol(g); g.fillStyle = o.ton ? B.ton(o.ton) : '#000'; g.fill(o.kural || 'nonzero'); g.restore(); };
  B.cayBoya = (yol, d = 1, ton = .5, a = 1) => { const g = B.c; g.save(); g.globalAlpha = a; g.beginPath(); yol(g); g.fillStyle = B.cay(d, ton); g.fill(); g.restore(); };
  // çay plakasında bir alanı sil (öndeki siyah nesne çayı örtsün diye; çarpma boyası katman sırası bilmez)
  B.cayOrt = (yol) => { const g = B.c; g.save(); g.beginPath(); yol(g); g.fillStyle = '#000'; g.fill(); g.restore(); };
  B.compose = (ctx) => {
    const srcs = [cK, cL, cC];
    for (let i = 0; i < 3; i++) { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, tex[i]); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, srcs[i]); }
    gl.viewport(0, 0, DW, DH);
    const k = O.kay || [3, 2];
    gl.uniform2f(U.res, DW, DH); gl.uniform2f(U.kay, k[0], k[1]); gl.uniform1f(U.per, O.per || 7); gl.uniform1f(U.rs, RS);
    gl.uniform1f(U.gate, O.gate ?? 1); gl.uniform1f(U.gateA, O.gate == null ? 0 : 1); gl.uniform1f(U.kagitA, O.kagit ?? 1);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    ctx.drawImage(glc, 0, 0); ctx.restore();
  };
  return B;
})();
