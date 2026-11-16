// comp_hizli.js (Ran): LemoLab ink-wash birleştiricisinin (lib/vendor/ink-wash/comp.js, MIT) hızlı sürümü.
// Fark yalnız hesaplama sırası: kâğıt rengi ve bütün durağan gürültü alanları (fbm/vn) yalnız konuma bağlı olduğundan
// bir kez ön geçişte dokulara yazılır; her karede yalnız okunur. Görünüm aynı (gürültü 8 bit nicemlenir).
// Kullanılmayan özellikler (A/B mürekkep geçişi, "rev" açılışı) çıkarıldı. Yazılımsal WebGL'de (SwiftShader) kare süresi ~10 kat kısalır.
const VS = `#version 300 es
in vec2 p; void main(){ gl_Position = vec4(p,0,1); }`;
const NOISE = `
float h21(vec2 p){ p = fract(p*vec2(123.34, 456.21)); p += dot(p, p+45.32); return fract(p.x*p.y); }
float vn(vec2 p){ vec2 i = floor(p), f = fract(p); f = f*f*(3.-2.*f);
  return mix(mix(h21(i), h21(i+vec2(1,0)), f.x), mix(h21(i+vec2(0,1)), h21(i+vec2(1,1)), f.x), f.y); }
float fbm(vec2 p){ float a = 0., w = .5; for(int i=0;i<5;i++){ a += w*vn(p); p = p*2.03 + 17.1; w *= .5; } return a; }
float fiber(vec2 p, float ang){ float c = cos(ang), s = sin(ang); vec2 q = vec2(c*p.x + s*p.y, -s*p.x + c*p.y);
  float n = vn(vec2(q.x*.018, q.y*.9)); return smoothstep(.78, .95, n); }`;
// ön geçiş: mode 0 kâğıt rengi, 1 disp/feather, 2 g1/g2/j, 3 tooth/sp
const PRE = `#version 300 es
precision highp float; out vec4 o;
uniform vec2 res; uniform int mode; uniform vec3 paperCol; uniform vec3 X;
${NOISE}
void main(){
  vec2 fc = gl_FragCoord.xy; fc.y = res.y - fc.y;
  vec2 p = (fc + X.xy) / X.z;
  if (mode == 0) {
    float fine = clamp(X.z*1.2, 0., 1.);
    float cloud = fbm(p*.0028) - .5, cloud2 = fbm(p*.011 + 3.) - .5;
    float fb = fiber(p, .35) + fiber(p + 91., 2.1) * .8 + fiber(p*1.7 + 13., 1.2) * .6;
    float grain = vn(p*.9) - .5;
    vec3 c = paperCol * (1. + cloud*.07 + cloud2*.03*fine + grain*.035*fine);
    c += vec3(.018,.016,.012) * fb * fine;
    c -= vec3(.012,.014,.018) * smoothstep(.65,.9, vn(p*.05 + 7.)) * fine;
    o = vec4(c, 1.);
  } else if (mode == 1) {
    o = vec4(fbm(p*.012), fbm(p*.012 + 31.), vn(p*.21), vn(p*.21 + 7.));
  } else if (mode == 2) {
    o = vec4(vn(p*.35), fbm(p*.06), vn(p*.7), vn(p*.7 + 5.));
  } else {
    float tooth = smoothstep(.62, .9, vn(p*.55 + 3.));
    float sp = smoothstep(.2, .45, vn(p*.8 + 11.));
    o = vec4(tooth, sp, 0., 1.);
  }
}`;
const FS = `#version 300 es
precision highp float; out vec4 o;
uniform sampler2D wA, dA, cA, NP, N1, N2, N3;
uniform vec2 res; uniform vec2 shake; uniform float flash, fade, vig, warm, bleed, rimK; uniform vec3 paperCol;
const vec2 PD[12] = vec2[](vec2(-.326,-.406), vec2(-.840,-.074), vec2(-.696,.457), vec2(-.203,.621), vec2(.962,-.195), vec2(.473,-.480),
  vec2(.519,.767), vec2(.185,-.893), vec2(.507,.064), vec2(.896,.412), vec2(-.322,-.933), vec2(-.792,-.598));
void main(){
  vec2 fc = gl_FragCoord.xy; fc.y = res.y - fc.y; fc += shake;
  vec2 uvn = clamp(fc, vec2(0.), res - 1.) / res;
  vec3 pc = texture(NP, uvn).rgb;
  vec4 n1 = texture(N1, uvn), n2 = texture(N2, uvn), n3 = texture(N3, uvn);
  float R = bleed;
  vec2 disp = n1.xy - .5, feather = n1.zw - .5;
  vec2 q = fc + disp * R * 1.1 + feather * R * .35;
  float a = 0., b = 0.;
  for (int i = 0; i < 12; i++) { a += texture(wA, (q + PD[i] * R * .5) / res).a; b += texture(wA, (q + PD[i] * R * 1.35) / res).a; }
  a /= 12.; b /= 12.;
  float s0 = texture(wA, q / res).a;
  float edge = max(0., a - b);
  float wet = mix(s0, a, .72) * (.86 + .22*n2.y) + edge * rimK * (.8 + .5*n2.x) + b * .10;
  vec2 j = n2.zw - .5;
  float dry = texture(dA, (fc + j * 1.6) / res).a;
  float tooth = n3.x * .45;
  dry *= 1. - tooth * (1. - dry*.5);
  float D = clamp(1. - (1. - clamp(wet,0.,1.)) * (1. - clamp(dry,0.,1.)), 0., 1.);
  vec3 inkc = mix(vec3(.52,.55,.58), vec3(.075,.068,.062), smoothstep(.0, .85, D));
  vec3 c = pc * mix(vec3(1.), inkc, clamp(D*1.05, 0., 1.));
  vec4 col = texture(cA, fc / res);
  float sp = n3.y * .25 + .75;
  c = mix(c, col.rgb * (pc / paperCol), col.a * sp);
  vec2 uv = gl_FragCoord.xy / res - .5;
  c *= 1. - vig * dot(uv*vec2(1.,.9), uv*vec2(1.,.9)) * 1.2;
  c = mix(c, c * vec3(1.02, .99, .94), warm);
  c = mix(c, paperCol, flash);
  c = mix(c, vec3(0.), fade);
  o = vec4(clamp(c, 0., 1.), 1.);
}`;

export function makeComp(canvas) {
  const gl = canvas.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false });
  if (!gl) throw new Error('no webgl2');
  const W = canvas.width, H = canvas.height;
  const sh = (t, s) => { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(x)); return x; };
  const prog = fs => { const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, fs)); gl.linkProgram(pr); if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr)); return pr; };
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const bindAttr = pr => { const loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0); };
  const mkTex = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE); return t; };
  // ön geçiş: dört durağan doku
  const pre = prog(PRE); gl.useProgram(pre); bindAttr(pre);
  const PU = n => gl.getUniformLocation(pre, n);
  gl.uniform2f(PU('res'), W, H); gl.uniform3f(PU('paperCol'), .95, .925, .87); gl.uniform3f(PU('X'), 0, 0, 1);
  const fb = gl.createFramebuffer(), noise = [];
  for (let m = 0; m < 4; m++) {
    const t = mkTex(); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, W, H, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    gl.bindFramebuffer(gl.FRAMEBUFFER, fb); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
    gl.viewport(0, 0, W, H); gl.uniform1i(PU('mode'), m); gl.drawArrays(gl.TRIANGLES, 0, 3); noise.push(t);
  }
  gl.bindFramebuffer(gl.FRAMEBUFFER, null);
  // ana geçiş
  const pr = prog(FS); gl.useProgram(pr); bindAttr(pr);
  const U = n => gl.getUniformLocation(pr, n);
  const tex = ['wA', 'dA', 'cA'].map((n, i) => { gl.activeTexture(gl.TEXTURE0 + i); const t = mkTex(); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4)); gl.uniform1i(U(n), i); return t; });
  ['NP', 'N1', 'N2', 'N3'].forEach((n, k) => { gl.activeTexture(gl.TEXTURE3 + k); gl.bindTexture(gl.TEXTURE_2D, noise[k]); gl.uniform1i(U(n), 3 + k); });
  const up = (i, cv) => { gl.activeTexture(gl.TEXTURE0 + i); gl.bindTexture(gl.TEXTURE_2D, tex[i]); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cv); };
  return function composite(A, B, o = {}) {
    gl.useProgram(pr); gl.viewport(0, 0, W, H);
    up(0, A.wet); up(1, A.dry); up(2, A.col);
    gl.uniform2f(U('res'), W, H);
    gl.uniform1f(U('bleed'), o.bleed ?? 6); gl.uniform1f(U('rimK'), o.rim ?? .8);
    const sk = o.shake || [0, 0]; gl.uniform2f(U('shake'), sk[0], sk[1]);
    gl.uniform1f(U('flash'), o.flash ?? 0); gl.uniform1f(U('fade'), o.fade ?? 0);
    gl.uniform1f(U('vig'), o.vig ?? .22); gl.uniform1f(U('warm'), o.warm ?? .5);
    gl.uniform3f(U('paperCol'), .95, .925, .87);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
}

export function layerSet(W = 1920, H = 1080) {
  const mk = () => { const c = document.createElement('canvas'); c.width = W; c.height = H; return c; };
  const wet = mk(), dry = mk(), col = mk();
  const L = { wet, dry, col, W, H, cw: wet.getContext('2d'), cd: dry.getContext('2d'), cc: col.getContext('2d') };
  L.ink = { wet: L.cw, dry: L.cd, col: L.cc };
  L.clear = () => { for (const c of [L.cw, L.cd, L.cc]) { c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.clearRect(0, 0, W, H); } };
  L.xf = (s, tx, ty) => { for (const c of [L.cw, L.cd, L.cc]) c.setTransform(s, 0, 0, s, tx, ty); };
  return L;
}
