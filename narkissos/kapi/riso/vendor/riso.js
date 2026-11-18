// Lemo-Opuscar (lemomo-ai/lemo-opuscar) 3a7132b, MIT — styles/risograph/demo/riso.js
// Zaman Kuryesi (Narkissos üslup kapısı) değişiklikleri:
//  - su bölgesi artık tam genişlikte bant değil, ayrı bir MASKE dokusu (R = su/cam, G = piksel ızgarası payı, B = parıltı: mürekkepsiz kâğıt)
//  - yansımada plaka başına ayrı kayma (uRSep: "başkası" → "benim" anında yerine oturur)
//  - analitik gözyaşı halkası (her plaka kendi evresinde; Date.now/rAF yok, yalnız zaman parametresi)
//  - sabit kodlu beyaz dalga kırıkları uGap ile ayarlanır (varsayılan 0: yansıma tek parça)
//  - suyun kendi mürekkebi uWInk (plaka başına yoğunluk)
//  - yarım ton → piksel ızgarası: maskenin G kanalında nokta açısı 0'a, biçimi kareye, periyodu uPixP'ye döner
// Girdi: plaka tuvali (R = 1. mürekkep, G = 2., B = 3.; 0 = mürekkep yok, 255 = tam).
export const PAPER = [244, 238, 226];

const VS = `#version 300 es
in vec2 p; void main(){ gl_Position = vec4(p, 0., 1.); }`;

const FS = `#version 300 es
precision highp float;
uniform sampler2D uTex;
uniform sampler2D uMask;
uniform vec2 uRes;
uniform vec2 uOff[3];
uniform float uRot[3];
uniform float uAng[3];
uniform vec3 uInk[3];
uniform vec3 uPaper;
uniform float uSeed;
uniform float uBoil;
uniform float uSheet;
uniform float uPeriod;
uniform float uGate[3];
uniform float uGrain;
uniform float uWaterY;     // yansıma ekseni (px); <0: su yok
uniform float uWaterAmp;   // salınım genliği (px)
uniform float uWaterT;
uniform float uRefl;       // yansıma gücü
uniform float uGap;        // dalga kırıkları (0 = yok)
uniform vec2 uRSep[3];     // yansımada plaka başına kayma (px)
uniform vec3 uWInk;        // suyun kendi mürekkebi (plaka başına)
uniform vec4 uRing;        // halka: merkez x, y, yarıçap, genlik (px)
uniform vec3 uRingP;       // dalga boyu, y basıklığı, plaka başına yarıçap farkı
uniform float uPixP;       // piksel ızgarası periyodu (px)
out vec4 o;

float h21(vec2 p){ vec3 p3 = fract(vec3(p.xyx) * .1031); p3 += dot(p3, p3.yzx + 33.33); return fract((p3.x + p3.y) * p3.z); }
float h21s(vec2 p, float s){ return h21(p + s * 17.13); }
float vn(vec2 p, float s){
  vec2 i = floor(p), f = fract(p); vec2 u = f * f * (3. - 2. * f);
  float a = h21s(i, s), b = h21s(i + vec2(1, 0), s), c = h21s(i + vec2(0, 1), s), d = h21s(i + vec2(1, 1), s);
  return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
vec2 rot(vec2 v, float a){ float c = cos(a), s = sin(a); return vec2(c * v.x - s * v.y, s * v.x + c * v.y); }

float dens(int i, vec2 q, vec4 m){
  float d = texture(uTex, q / uRes)[i];
  if (m.r > .004 && uWaterY > 0. && q.y > uWaterY) {
    float fi = float(i);
    float depth = q.y - uWaterY;
    float w = sin(q.y * .09 + uWaterT * 2.3 + fi * 2.1) * (1. + depth * .004) + sin(q.y * .031 - uWaterT * 1.3 + fi) * .6;
    vec2 rq = vec2(q.x + w * uWaterAmp, 2. * uWaterY - q.y) + uRSep[i];
    float crest = 0.;
    if (uRing.w > 0.) {
      vec2 dv = (q - uRing.xy) * vec2(1., uRingP.y);
      float dd = length(dv);
      float ph = dd - (uRing.z + (fi - 1.) * uRingP.z);
      float env = exp(-ph * ph / (uRingP.x * uRingP.x * 2.2));
      float s = sin(ph * 6.2831853 / uRingP.x);
      rq += normalize(dv + 1e-4) * s * env * uRing.w * vec2(1., 1. / uRingP.y);
      crest = smoothstep(.55, .95, s) * env * clamp(uRing.w / 8., 0., 1.);
    }
    float r = (rq.y > 0. && rq.y < uWaterY + 2.) ? texture(uTex, rq / uRes)[i] : 0.;
    float gap = step(.72, vn(vec2(q.x * .012, q.y * .35) + uWaterT * vec2(.8, 0), 3.));
    r *= uRefl * (1. - gap * .85 * uGap);
    float dw = 1. - (1. - r) * (1. - uWInk[i]);
    d = mix(d, 1. - (1. - d) * (1. - dw), m.r);
    d *= 1. - crest * .75;
  }
  return d;
}

void main(){
  vec2 px = vec2(gl_FragCoord.x, uRes.y - gl_FragCoord.y);
  float fib = vn(px * vec2(.9, .25), 7.) * .5 + vn(px * .05, 9.) * .5;
  vec3 col = uPaper * (.975 + .03 * fib);
  for (int i = 0; i < 3; i++) {
    if (uGate[i] <= 0.001) continue;
    vec2 q = rot(px - uRes * .5, uRot[i]) + uRes * .5 - uOff[i];
    vec4 m = texture(uMask, q / uRes);
    float d = dens(i, q, m);
    if (d < .002) continue;
    float pk = m.g;
    float ang = mix(uAng[i], 0., pk);
    float per = mix(uPeriod, uPixP, pk);
    vec2 g = rot(q, ang) / per;
    float spot = 1. - (cos(6.2831853 * g.x) + cos(6.2831853 * g.y) + 2.) * .25;
    float n1 = mix(h21s(floor(q * .9), uSheet + float(i) * 3.1), h21s(floor(q * .9), uSeed + float(i) * 3.1), uBoil);
    float n2 = vn(q * .33, uSheet * .7 + float(i));
    float thr = spot + (n1 - .5) * .16 * uGrain + (n2 - .5) * .12;
    float dd = d * 1.06;
    float covDot = smoothstep(thr - .07, thr + .07, dd);
    covDot = max(covDot, smoothstep(.9, 1., d) * .96);
    // piksel ızgarası: eksene hizalı kare hücre, tam yoğunlukta bile ince aralık kalır
    vec2 f = abs(fract(g) - .5) * 2.;
    float sq = max(f.x, f.y);
    float edge = sqrt(d) * .84;
    float covSq = 1. - smoothstep(edge - .06, edge + .06, sq + (n1 - .5) * .05);
    float cov = mix(covDot, covSq, pk);
    float sp = h21s(floor(q * .55), uSheet * 1.3 + float(i) * 7.7);
    cov *= 1. - step(.955 - .03 * uGrain, sp) * .75 * smoothstep(.4, 1., d) * (1. - pk);
    cov *= 1. - m.b;   // parıltı: kâğıt
    float streak = vn(vec2(q.x * .025, q.y * .0022), 11. + float(i) + uSheet * .37);
    float blot = vn(q * .004, 5. + float(i) * 2. + uSheet * .13);
    float k = clamp(.80 + .14 * streak + .08 * blot, 0., 1.);
    float c = clamp(cov * k, 0., 1.) * uGate[i];
    col *= mix(vec3(1.), uInk[i], c);
  }
  o = vec4(col, 1.);
}`;

export function makeRiso(out, W, H) {
  const gl = out.getContext('webgl2', { preserveDrawingBuffer: true, antialias: false, alpha: false });
  const sh = (t, s) => { const x = gl.createShader(t); gl.shaderSource(x, s); gl.compileShader(x); if (!gl.getShaderParameter(x, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(x)); return x; };
  const pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr));
  gl.useProgram(pr);
  const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const mkTex = unit => {
    gl.activeTexture(gl.TEXTURE0 + unit);
    const tex = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    return tex;
  };
  const tex = mkTex(0), mtex = mkTex(1);
  gl.pixelStorei(gl.UNPACK_COLORSPACE_CONVERSION_WEBGL, gl.NONE);
  gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
  const U = n => gl.getUniformLocation(pr, n);
  const u = {}; for (const n of ['uTex', 'uMask', 'uRes', 'uOff', 'uRot', 'uAng', 'uInk', 'uPaper', 'uSeed', 'uBoil', 'uSheet', 'uPeriod', 'uGate', 'uGrain',
    'uWaterY', 'uWaterAmp', 'uWaterT', 'uRefl', 'uGap', 'uRSep', 'uWInk', 'uRing', 'uRingP', 'uPixP']) u[n] = U(n);
  gl.viewport(0, 0, W, H);
  return function print(plate, mask, o = {}) {
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, plate);
    gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, mtex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, mask);
    gl.uniform1i(u.uTex, 0); gl.uniform1i(u.uMask, 1);
    gl.uniform2f(u.uRes, W, H);
    gl.uniform2fv(u.uOff, (o.off || [[0, 0], [0, 0], [0, 0]]).flat());
    gl.uniform1fv(u.uRot, o.rot || [0, 0, 0]);
    gl.uniform1fv(u.uAng, o.ang || [0.2618, 0, 1.309]);
    gl.uniform3fv(u.uInk, o.inks.map(c => c.map(v => v / 255)).flat());
    gl.uniform3fv(u.uPaper, (o.paper || PAPER).map(v => v / 255));
    gl.uniform1f(u.uSeed, o.seed ?? 0);
    gl.uniform1f(u.uSheet, o.sheet ?? 0);
    gl.uniform1f(u.uBoil, o.boil ?? .35);
    gl.uniform1f(u.uPeriod, o.period ?? 7);
    gl.uniform1fv(u.uGate, o.gate || [1, 1, 1]);
    gl.uniform1f(u.uGrain, o.grain ?? 1);
    const w = o.water || null;
    gl.uniform1f(u.uWaterY, w ? w.y : -1);
    gl.uniform1f(u.uWaterAmp, w ? w.amp : 0);
    gl.uniform1f(u.uWaterT, w ? w.t : 0);
    gl.uniform1f(u.uRefl, w ? w.refl : 0);
    gl.uniform1f(u.uGap, w ? (w.gap ?? 0) : 0);
    gl.uniform2fv(u.uRSep, (w && w.sep ? w.sep : [[0, 0], [0, 0], [0, 0]]).flat());
    gl.uniform3fv(u.uWInk, w && w.ink ? w.ink : [0, 0, 0]);
    const r = w && w.ring ? w.ring : null;
    gl.uniform4fv(u.uRing, r ? [r.x, r.y, r.r, r.amp] : [0, 0, 0, 0]);
    gl.uniform3fv(u.uRingP, r ? [r.wl ?? 34, r.sq ?? 1, r.step ?? 7] : [34, 1, 7]);
    gl.uniform1f(u.uPixP, o.pixP ?? 12);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  };
}
