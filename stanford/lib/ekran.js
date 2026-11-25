// Gözetim monitörü + belge kâğıdı motoru (Stanford, 1971). ORTAK DOSYA: yalnız başkan değiştirir.
// cernobil/lib/baski.js'in arayüzü korunur (BASKI = EKRAN): sahneler üç plakaya çizer, gölgelendirici "gösterir".
//   B.k  TON plakası   (gri tonlu çizim: siyah = koyu)        → monitörde gri video, kâğıtta yumuşak mürekkep yıkaması
//   B.l  ÇİZGİ plakası (dizgi, çizgi, düz siluet: siyah = koyu) → düz, sert koyu
//   B.c  RENK plakası  (B.renk(yoğunluk, ton): R yoğunluk, G ton 0 kehribar → 1 kırmızı)
// Görüntünün kuralları (uretim_plani.md §4):
//   1. Bodrum yalnız gözetim monitöründe görünür (o.mod 'video'): siyah-beyaz, tarama çizgili, renksiz.
//   2. Renk yalnız belgede ve kayıtta: kâğıt (o.mod 'kagit') sıcak; teybin kehribar ışığı ve kırmızı kayıt lambası.
//   3. Kâğıt sahnenin içinde monitör: B.ekranMaske(yol) (renk plakasının mavi kanalı) ya da o.ekran {x, y, w, h}; içi video basılır.
// DİKKAT: plakada silmek için beyaz boya (B.k, B.l) ya da siyah boya (B.c); destination-out kullanılmaz (saydam piksel tam mürekkep sayılır).
// Gren ve tarama gürültüsü iki karede bir değişir (dosya boyu); tarama çizgileri ekrana sabit.
'use strict';
const EKRAN = (() => {
  const B = {};
  let cK, cL, cC, gl, glc, prog, tex = [], U = {};
  B.KARA = '#000'; B.MUR = '#1E1A16'; B.KAGIT = '#EDE4CF';
  B.renk = (d = 1, ton = 0, a = 1) => `rgba(${Math.round(clamp(d) * 255)},${Math.round(clamp(ton) * 255)},0,${a})`;
  B.cay = B.renk;
  B.ton = (d, a = 1) => { const v = Math.round((1 - clamp(d)) * 255); return `rgba(${v},${v},${v},${a})`; };
  const VS = `#version 300 es
in vec2 p; out vec2 uv; void main(){ uv = p * .5 + .5; gl_Position = vec4(p, 0., 1.); }`;
  const FS = `#version 300 es
precision highp float;
in vec2 uv; out vec4 o;
uniform sampler2D tK, tL, tC; uniform vec2 res; uniform float rs, seed, kagitA, bantY, bantA, parlak, sarsinti;
uniform vec4 ekr; uniform float ekrA;
float h21(vec2 p){ p = fract(p * vec2(123.34, 456.21)); p += dot(p, p + 45.32); return fract(p.x * p.y); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
  return mix(mix(h21(i), h21(i + vec2(1, 0)), f.x), mix(h21(i + vec2(0, 1)), h21(i + vec2(1, 1)), f.x), f.y); }
float lum(vec4 c){ return dot(c.rgb, vec3(.299, .587, .114)); }
// video parlaklığı (1 = beyaz) bir noktada: ton × çizgi
float vid(vec2 st){ return lum(texture(tK, st)) * lum(texture(tL, st)); }
void main(){
  vec2 fc = gl_FragCoord.xy; vec2 st = vec2(uv.x, 1. - uv.y);
  vec2 px = 1. / res;
  // ekran dikdörtgeni (st uzayında): içi video
  vec2 e0 = ekr.xy, e1 = ekr.zw;
  float iceri = step(e0.x, st.x) * step(st.x, e1.x) * step(e0.y, st.y) * step(st.y, e1.y);
  float vmod = ekrA < .5 ? 1. : max(iceri, step(.5, texture(tC, st).b));
  vec3 col;
  // renk plakası
  vec4 cc = texture(tC, st); float dC = cc.r, tn = cc.g;
  vec3 kehr = vec3(.86, .55, .18), kirm = vec3(.80, .12, .08);
  vec3 rk = mix(kehr, kirm, tn);
  if (vmod > .5) {
    // ── gözetim monitörü ──
    vec2 q = st;
    if (ekrA > .5) q = st; // kâğıt içindeki monitör: görüntü plakada zaten yerinde
    // satır titremesi (tarama bandı yakınında yatay kayma)
    float sat = floor(fc.y / (3. * rs));
    float bd = bantA * exp(-pow((st.y - bantY) * 18., 2.));
    q.x += (h21(vec2(sat, seed)) - .5) * (.004 * bd + .0006 * sarsinti);
    // yatay yumuşaklık (1971 video bandı): 5 dokunuş
    float v = vid(q) * .36 + (vid(q + vec2(px.x * 1.6, 0)) + vid(q - vec2(px.x * 1.6, 0))) * .22 + (vid(q + vec2(px.x * 3.4, 0)) + vid(q - vec2(px.x * 3.4, 0))) * .10;
    // ışıma: parlak alanlar çevresine taşar
    float gl = 0.;
    for (int i = 0; i < 6; i++) { float a = float(i) * 1.0472; gl += vid(q + vec2(cos(a), sin(a)) * px * 9.); }
    gl = smoothstep(.55, 1., gl / 6.);
    v = v + gl * .12 * parlak;
    // video siyahı ve kontrast
    v = .055 + .9 * pow(clamp(v, 0., 1.), 1.08);
    // gren (iki karede bir) + tarama bandı karlanması
    float g = h21(floor(fc / (2. * rs)) + seed * 17.13);
    v += (g - .5) * (.07 + .5 * bd);
    v += bd * .25 * step(.82, h21(vec2(floor(fc.x / (6. * rs)), sat + seed)));
    // tarama çizgileri (3 px)
    float sc = .80 + .20 * (.5 + .5 * cos(6.2831853 * fc.y / (3. * rs)));
    v *= sc;
    // fosfor rengi: hafif soğuk
    col = mix(vec3(.03, .045, .05), vec3(.90, .96, .97), clamp(v, 0., 1.1));
    // renk plakası monitörde ışık olarak (yalnız kayıt lambası ve teyp ışığı için)
    col = mix(col, rk * 1.05, dC * .9);
    // köşe kararması (tüp)
    vec2 ce = ekrA < .5 ? (st - .5) : (st - (e0 + e1) * .5) / max(e1 - e0, vec2(.01));
    float vg = smoothstep(.78, .42, length(ce * vec2(1.05, 1.25)));
    col *= mix(.55, 1., vg);
  } else {
    // ── belge kâğıdı ──
    float mot = vn(fc / (200. * rs)) * .6 + vn(fc / (55. * rs)) * .4;
    float lif = vn(vec2(fc.x / (2.2 * rs), fc.y / (70. * rs)) + 7.) * .6 + vn(fc / (9. * rs) + 3.) * .4;
    float gr = h21(floor(fc / max(1., rs)));
    vec3 kagit = vec3(.93, .895, .815) * (1. - kagitA * (.05 * mot + .022 * lif + .03 * gr));
    kagit *= 1. - .12 * kagitA * smoothstep(.55, 1.05, length((st - .5) * vec2(1.2, 1.)));
    vec3 mur = vec3(.118, .102, .086);
    float dK = 1. - lum(texture(tK, st));
    dK = clamp(dK * (1. + (mot - .5) * .18) + (gr - .5) * .05 * step(.02, dK), 0., 1.);
    float dL = 1. - lum(texture(tL, st));
    float cL = smoothstep(.32 + (gr - .5) * .18, .6, dL);
    col = kagit;
    col = mix(col, col * rk, dC * .9);
    col *= mix(vec3(1.), mur / .93, dK * .92);
    col *= mix(vec3(1.), mur, cL * .97);
  }
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
    for (const n of ['tK', 'tL', 'tC', 'res', 'rs', 'seed', 'kagitA', 'bantY', 'bantA', 'parlak', 'sarsinti', 'ekr', 'ekrA']) U[n] = gl.getUniformLocation(prog, n);
    gl.uniform1i(U.tK, 0); gl.uniform1i(U.tL, 1); gl.uniform1i(U.tC, 2);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
  };
  // begin(o): o.mod 'video' (varsayılan) | 'kagit' · o.ekran {x,y,w,h} kâğıt sahnede monitör · o.bant [y 0..1, güç] tarama bandı
  //   o.parlak ışıma (varsayılan 1) · o.sarsinti satır titremesi (0..1) · o.kagit kâğıt dokusu (0..1)
  let O = {};
  B.begin = (o = {}) => {
    O = o;
    for (const [g, bg] of [[B.k, '#fff'], [B.l, '#fff'], [B.c, '#000']]) { g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = 'source-over'; g.filter = 'none'; g.fillStyle = bg; g.fillRect(0, 0, DW, DH); baseT(g); }
  };
  B.cam = (x = W / 2, y = H / 2, z = 1, r = 0) => {
    for (const g of [B.k, B.l, B.c]) { baseT(g); g.translate(W / 2, H / 2); if (r) g.rotate(r); g.scale(z, z); g.translate(-x, -y); }
  };
  B.save = () => { B.k.save(); B.l.save(); B.c.save(); };
  B.restore = () => { B.k.restore(); B.l.restore(); B.c.restore(); };
  B.each = fn => { for (const g of [B.k, B.l, B.c]) fn(g); };
  B.siluet = (yol, o = {}) => { const g = o.ton ? B.k : B.l; g.save(); g.globalAlpha = o.a ?? 1; g.beginPath(); yol(g); g.fillStyle = o.ton ? B.ton(o.ton) : '#000'; g.fill(o.kural || 'nonzero'); g.restore(); };
  B.renkBoya = (yol, d = 1, ton = 0, a = 1) => { const g = B.c; g.save(); g.globalAlpha = a; g.beginPath(); yol(g); g.fillStyle = B.renk(d, ton); g.fill(); g.restore(); };
  B.cayBoya = B.renkBoya;
  // monitör maskesi (kâğıt sahnede): renk plakasının mavi kanalı; içi video basılır. Öndeki nesne B.renkOrt ile maskeyi siler.
  B.ekranMaske = (yol) => { const g = B.c; g.save(); g.beginPath(); yol(g); g.fillStyle = 'rgb(0,0,255)'; g.fill(); g.restore(); };
  B.renkOrt = (yol) => { const g = B.c; g.save(); g.beginPath(); yol(g); g.fillStyle = '#000'; g.fill(); g.restore(); };
  B.cayOrt = B.renkOrt;
  B.compose = (ctx) => {
    const srcs = [cK, cL, cC];
    for (let i = 0; i < 3; i++) { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, tex[i]); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, srcs[i]); }
    gl.viewport(0, 0, DW, DH);
    const fi = Math.floor(Math.round((window.FIG_T || 0) * 30) / 2);
    gl.uniform2f(U.res, DW, DH); gl.uniform1f(U.rs, RS); gl.uniform1f(U.seed, (fi % 97) + 1);
    gl.uniform1f(U.kagitA, O.kagit ?? 1); gl.uniform1f(U.parlak, O.parlak ?? 1); gl.uniform1f(U.sarsinti, O.sarsinti ?? 0);
    const bt = O.bant || [0, 0]; gl.uniform1f(U.bantY, bt[0]); gl.uniform1f(U.bantA, bt[1]);
    const kag = O.mod === 'kagit';
    if (kag && O.ekran) { const e = O.ekran; gl.uniform4f(U.ekr, e.x / W, e.y / H, (e.x + e.w) / W, (e.y + e.h) / H); gl.uniform1f(U.ekrA, 1); }
    else if (kag) { gl.uniform4f(U.ekr, 2, 2, 2, 2); gl.uniform1f(U.ekrA, 1); }   // yalnız maske
    else { gl.uniform4f(U.ekr, 0, 0, 1, 1); gl.uniform1f(U.ekrA, 0); }
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    ctx.drawImage(glc, 0, 0); ctx.restore();
  };
  return B;
})();
const BASKI = EKRAN;
