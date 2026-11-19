// Ortak çizim ilkelleri (Narkissos; kapı kodu kapi/vazo/nark.js'ten ayrıldı). ORTAK DOSYA: yalnız başkan değiştirir.
// Bağımlılık: lib/vazo/* (core, style, anim, figure, dipinto, walk, env, world). Belirlenimci: rastgelelik yalnız rng(tohum), hash, noise.
// Koordinatlar mantıksal 1920×1080 (sahne/dünya); cihaz tuvali DW×DH (RS ölçeği: ?rs=0.5 animatik, ?rs=2 4K).
'use strict';
const CW = DW, CH = DH; // çıktı tuvali (cihaz pikseli)

// ---- kamera ----
// camAt: sahne noktası (fx, fy) ekranda (sx, sy)'ye, z yakınlaşmayla. Çağırmadan önce baseT(ctx).
function camAt(ctx, fx, fy, z = 1, sx = W / 2, sy = H / 2) { ctx.translate(sx, sy); ctx.scale(z, z); ctx.translate(-fx, -fy); }
// iki kamera durumu arasında yumuşak geçiş: c = [fx, fy, z]
function camMix(a, b, u, e = E.io2) { const k = e(clamp(u)); return [lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k)]; }
// varsayılan yavaş hareket (donuk plan yok): st.p (0..1) boyunca z0 → z1, merkez sabit
function slowZoom(ctx, st, fx = W / 2, fy = H / 2, z0 = 1, z1 = 1.05) { camAt(ctx, fx, fy, lerp(z0, z1, E.sine(clamp(st.p)))); }

// ---- ara katmanlar (çıktı tuvali boyunda; her çağrıda temizlenir) ----
const LY = {};
function layer(n) {
  if (!LY[n]) LY[n] = makeCanvas(CW, CH);
  const x = LY[n].getContext('2d');
  x.setTransform(1, 0, 0, 1, 0, 0); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; x.filter = 'none';
  x.clearRect(0, 0, CW, CH);
  return x;
}
function jointPt(ctx, M, q) { const sp = M.transformPoint(new DOMPoint(q[0], q[1])); const r = ctx.getTransform().inverse().transformPoint(sp); return [r.x, r.y]; }

// ---- zemin: siyah sır + alttan (sudan) gelen sıcak ışık; başın arkasında ışık yok (hale okunmasın) ----
function glaze(ctx, gx, gy, gr, warm = 'rgba(120,48,22,.5)') {
  ctx.fillStyle = PC.glaze; ctx.fillRect(-3000, -3000, 9000, 9000);
  const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, gr);
  g.addColorStop(0, warm); g.addColorStop(.55, 'rgba(60,24,12,.22)'); g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g; ctx.fillRect(-3000, -3000, 9000, 9000);
}
// beyaz zemin (lekythos) hatıra paleti: krem zemin + solgun sepya çizgi için STY.white / C.sepia
function whiteGround(ctx, o = {}) {
  ctx.fillStyle = o.col || '#EFE4CC'; ctx.fillRect(-3000, -3000, 9000, 9000);
  if (o.warm !== false) { const g = ctx.createRadialGradient(o.x ?? W / 2, o.y ?? H * .45, 0, o.x ?? W / 2, o.y ?? H * .45, o.r ?? 1100); g.addColorStop(0, 'rgba(255,250,236,.5)'); g.addColorStop(1, 'rgba(180,150,110,.25)'); ctx.fillStyle = g; ctx.fillRect(-3000, -3000, 9000, 9000); }
}

// ---- su gövdesi: koyu sır + yatay ayrılmış kısa çizgiler (vazo ressamının suyu) ----
function waterBody(ctx, clipFn, wy, t, o = {}) {
  ctx.save(); ctx.beginPath(); clipFn(ctx); ctx.clip();
  ctx.fillStyle = o.fill || '#050302'; ctx.fillRect(-3000, wy, 9000, 4000);
  const r = rng(o.seed || 4), a = o.a ?? .2;
  ctx.strokeStyle = o.lineCol || `rgba(201,112,63,${a})`; ctx.lineCap = 'round';
  const [x0, x1] = o.span || [-200, 2200], n = o.n || 34;
  for (let i = 0; i < n; i++) {
    const y = wy + 14 + Math.pow(r(), 1.5) * (o.depth || 420), x = x0 + r() * (x1 - x0), L = 40 + r() * 170, dr = Math.sin(t * .6 + i) * 6;
    ctx.lineWidth = 1.6 + r() * 1.4; ctx.beginPath(); ctx.moveTo(x + dr, y); ctx.lineTo(x + L + dr, y); ctx.stroke();
  }
  ctx.restore();
}
// kıyı ve ufuk çizgisi: suyun yüzeyi açık kil, kalın (yan görünüşte suyu okutan çizgi)
function shoreLine(ctx, x0, wy, o = {}) {
  ctx.save(); ctx.strokeStyle = o.col || 'rgba(232,160,104,.92)'; ctx.lineWidth = o.w || 3.6; ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x0, wy); ctx.lineTo(o.x1 || 6000, wy); ctx.stroke(); ctx.restore();
}
// karşı kıyı: suyun ufkunda alçak, seyreltik sır şerit + ot
function farBank(ctx, x0, x1, wy, t, seed, o = {}) {
  const r = rng(seed), h = o.h || 46;
  ctx.save();
  ctx.beginPath(); ctx.moveTo(x0, wy);
  for (let x = x0; x <= x1 + 40; x += 40) ctx.lineTo(x, wy - h * (.55 + .45 * noise1(x * .004, seed)));
  ctx.lineTo(x1 + 40, wy); ctx.closePath(); ctx.fillStyle = o.fill || '#2A130A'; ctx.fill();
  ctx.strokeStyle = 'rgba(201,112,63,.35)'; ctx.lineWidth = 2; ctx.stroke();
  for (let i = 0; i < (o.grass ?? 10); i++) grass(ctx, x0 + 30 + r() * (x1 - x0 - 60), wy - h * .55 + 4, 1.2, t, seed + i);
  ctx.restore();
}
// kaya kenarı (dirseklerin dayandığı çıkıntı) suyun içine iner
function ledge(ctx, xe, gy, wy) {
  crag(ctx, [[-2600, gy + 4], [xe - 260, gy - 6], [xe - 40, gy - 2], [xe + 4, gy + 14], [xe - 6, wy + 30], [xe - 40, wy + 700], [-2600, wy + 700]], { fill: '#5A2C16', seed: 9, flat: [0, 5, 6], wob: 4, strata: 4, lobes: 3 });
}

// ---- figür: ayrı katmanda çizip alttan ışıkla boyama (kaynak: su ya da ekran); ışık yalnız figürün üstünde ----
// light: {x, y, r, c: 'rgba(…,A)', a, dark}
function litFigure(ctx, f, light) {
  const T = ctx.getTransform(), lx = layer('fig');
  lx.setTransform(T); const J = figure(lx, f);
  if (light && light.a > 0) {
    lx.globalCompositeOperation = 'source-atop';
    const g = lx.createRadialGradient(light.x, light.y, 0, light.x, light.y, light.r);
    g.addColorStop(0, light.c.replace('A', light.a.toFixed(3))); g.addColorStop(1, light.c.replace('A', '0'));
    lx.fillStyle = g; lx.fillRect(-3000, -3000, 9000, 9000);
    if (light.dark) {
      const g2 = lx.createLinearGradient(0, light.y - light.r, 0, light.y);
      g2.addColorStop(0, `rgba(20,8,4,${light.dark})`); g2.addColorStop(1, 'rgba(20,8,4,0)');
      lx.fillStyle = g2; lx.fillRect(-3000, -3000, 9000, 9000);
    }
    lx.globalCompositeOperation = 'source-over';
  }
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha *= (f.layerA ?? 1); ctx.drawImage(LY.fig, 0, 0); ctx.restore();
  return J;
}
// figür eklemleri (çizmeden): {J, M}
function joints(ctx, f) { let J = null, M = null; figure(ctx, { ...f, alpha: 0, jointsOnly: true, onJoints: (j, m) => { J = j; M = m; } }); return { J, M }; }
function headPt(ctx, J, M, q) { return jointPt(ctx, M, add(J.neckT, rot(q, J.headA))); }
const EYE_Q = [3.7, -6.75]; // baş yerelinde göz noktası (headPt ile)
// figürü boyun noktası target'a gelecek biçimde taşır (IK hedefleri de kayar)
function placeNeck(ctx, f, target) {
  const { J, M } = joints(ctx, f); const q = jointPt(ctx, M, J.neckT), dx = target[0] - q[0], dy = target[1] - q[1];
  const ik = f.ik ? Object.fromEntries(Object.entries(f.ik).map(([k, v]) => [k, [v[0] + dx, v[1] + dy, ...v.slice(2)]])) : f.ik;
  return { ...f, x: f.x + dx, y: f.y + dy, ik };
}

// ---- Narkissos ve bugünün genci: görünüm ayarları (kapı tur 1–3 sonucu) ----
// efeb başı (kısa bukleli saç, kulak açık, köşeli çene) ve görünür khiton (seyreltik sır, koyu sır kenar; nokta deseni ve kemer yok)
const KHITON = { col: '#93492A', edge: 1.3, sleeve: false };
const LK_NK = { hair: 'short', rf: true, garment: 'short', noCurls: true, efeb: true, hairPts: HAIR_EF, jaw: true, khiton: KHITON, noBelt: true };
// bugünün genci: kısa saç, seyreltik sır ceket, uzun kol; büyük baş ve iri göz (genç)
const LK_MOD = { jaw: true, modern: true, rf: true, hairPts: HAIR_MOD, garment: 'coat', coatCol: '#6E331B', sleeveCol: '#6E331B', earHidden: false, headS: 1.45, eyeS: 1.12 };
// yüzüstü uzanmış genç (gövde yatay, göğüs aşağı, bacaklar geriye, dirsekler kaya kenarında; diz çökme ve alın yere değme yok)
// px: kalça x, gy: zemin y, s: ölçek. o: {hN, hF (el hedefleri), flatFeet (ayak açısı; bacaklar düz ve yerde), idle, stripe, faceW}
function proneFig(px, gy, s, p, o = {}) {
  return { x: px, y: gy - 6.5 * s, s, dir: o.dir || 1, sty: o.sty || STY.red, lk: o.lk || LK_NK, seed: o.seed ?? 23, idle: o.idle ?? .4, p, stripe: o.stripe ?? .5, faceW: o.faceW || 1.2,
    ik: { fN: o.flatFeet ? [px - 47 * s, gy - 1.7 * s, o.flatFeet] : [px - 41 * s, gy - 2.5 * s, PI / 2 - .25], fF: o.flatFeet ? [px - 47.6 * s, gy - 2.0 * s, o.flatFeet] : [px - 43 * s, gy - 4.5 * s, PI / 2 - .35],
      hF: o.hF || [px + 31 * s, gy - 1.5 * s], hN: o.hN || [px + 33 * s, gy - 1.2 * s] } };
}
// uzanma pozu; o: {neck, head (ek eğim), handN, wrN, smile, brow, mouthOpen, browUp, eyeWide, blink}
function pPose(o = {}) {
  return { torso: 1.33, neck: -.5 + (o.neck || 0), head: .38 + (o.head || 0), handN: o.handN || 'flat', handF: 'flat', wrN: o.wrN || 0, wrF: 0,
    smile: o.smile || 0, brow: o.brow ?? .2, mouthOpen: o.mouthOpen || 0, browUp: o.browUp || 0, eyeWide: o.eyeWide || 0, blink: o.blink };
}

// ---- biçim dönüşümü (cam ↔ havuz, beden → nergis …): aynı başlangıç noktası ve yön, eşit yay aralığı ----
function resample(pts, n) {
  const L = [0]; for (let i = 1; i <= pts.length; i++) L.push(L[i - 1] + len(sub(pts[i % pts.length], pts[i - 1])));
  const tot = L[pts.length], out = []; let j = 0;
  for (let k = 0; k < n; k++) { const s = tot * k / n; while (L[j + 1] < s) j++; const u = (s - L[j]) / (L[j + 1] - L[j] || 1); out.push(lerp2(pts[j], pts[(j + 1) % pts.length], u)); }
  return out;
}
function roundRectPts(x0, y0, x1, y1, rTop, rBot, bulge = 0) { // üst kenarın ortasından saat yönünde
  const P = [], arc = (cx, cy, r, a0, a1) => { for (let i = 0; i <= 10; i++) { const a = lerp(a0, a1, i / 10); P.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } };
  P.push([(x0 + x1) / 2, y0]);
  arc(x1 - rTop, y0 + rTop, rTop, -PI / 2, 0);
  arc(x1 - rBot + bulge, y1 - rBot, rBot, 0, PI / 2);
  arc(x0 + rBot - bulge, y1 - rBot, rBot, PI / 2, PI);
  arc(x0 + rTop, y0 + rTop, rTop, PI, PI * 1.5);
  return P;
}
function ellipsePts(cx, cy, rx, ry) { const P = []; for (let i = 0; i < 64; i++) { const a = -PI / 2 + i / 64 * TAU; P.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]); } return P; }
function morphPts(A, B, m, n = 120) { const a = resample(A, n), b = resample(B, n); return a.map((p, i) => lerp2(p, b[i], m)); }

// ---- doğa ----
// vazo ağacı: ince gövde, kıvrık dallar, dal boyunca çift sıra zeytin yaprağı (kil dolgu, siyah kontur)
function vaseTree(ctx, x, y, s, seed, t, o = {}) {
  const r = rng(seed), sway = Math.sin(t * .7 + seed) * .012;
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.rotate(sway);
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  const fill = o.fill || PC.clayR, ink = o.ink || C.ink;
  const trunk = [[0, 0], [-4, -60], [6, -130], [-2, -200], [4, -260]];
  ctx.beginPath(); spline(ctx, trunk, false); ctx.strokeStyle = ink; ctx.lineWidth = 15; ctx.stroke();
  ctx.strokeStyle = fill; ctx.lineWidth = 9; ctx.stroke();
  const leaf = (px, py, a, L) => { ctx.save(); ctx.translate(px, py); ctx.rotate(a); ctx.beginPath(); ctx.ellipse(L / 2, 0, L / 2, L * .17, 0, 0, TAU); ctx.fillStyle = fill; ctx.fill(); ctx.lineWidth = 1.8; ctx.strokeStyle = ink; ctx.stroke(); ctx.beginPath(); ctx.moveTo(L * .1, 0); ctx.lineTo(L * .85, 0); ctx.lineWidth = 1.2; ctx.stroke(); ctx.restore(); };
  const nb = o.branches || 6;
  for (let b = 0; b < nb; b++) {
    const u = .25 + .75 * (b / (nb - 1)), side = b % 2 ? 1 : -1, by = -260 * u, bx = Math.sin(u * 5) * 4;
    const L = (o.reach || 90) * (1.15 - u * .5) * (.8 + r() * .4), ph = Math.sin(t * 1.1 + b + seed) * 2.5;
    const P = [[bx, by], [bx + side * L * .5, by - 22 - r() * 14], [bx + side * L, by - 30 - r() * 30 + ph]];
    ctx.beginPath(); spline(ctx, P, false); ctx.strokeStyle = ink; ctx.lineWidth = 6; ctx.stroke(); ctx.strokeStyle = fill; ctx.lineWidth = 3; ctx.stroke();
    for (let k = 1; k <= 7; k++) {
      const v = k / 7.5, q = lerp2(lerp2(P[0], P[1], v), lerp2(P[1], P[2], v), v), da = Math.atan2(P[2][1] - P[0][1], P[2][0] - P[0][0]);
      leaf(q[0], q[1], da - side * (.9 - v * .4), 26 - v * 6);
      leaf(q[0], q[1], da + side * (.9 - v * .4), 24 - v * 6);
    }
  }
  ctx.restore();
}
function groundBand(ctx, y, x0 = -400, x1 = 2400, o = {}) {
  ctx.save(); ctx.fillStyle = o.edge || PC.clayR; ctx.fillRect(x0, y, x1 - x0, 7);
  ctx.fillStyle = o.fill || '#5A2C16'; ctx.fillRect(x0, y + 7, x1 - x0, o.h || 300);
  ctx.restore();
}
function grass(ctx, x, y, s, t, seed, o = {}) {
  ctx.save(); ctx.strokeStyle = o.col || PC.clayR; ctx.lineWidth = 2.6; ctx.lineCap = 'round';
  const r = rng(seed);
  for (let i = 0; i < 5; i++) { const a = -PI / 2 + (i - 2) * .28 + Math.sin(t * 1.3 + i + seed) * .04, L = s * (14 + r() * 10); ctx.beginPath(); ctx.moveTo(x + (i - 2) * 3, y); ctx.quadraticCurveTo(x + (i - 2) * 3 + Math.cos(a) * L * .4, y + Math.sin(a) * L * .6, x + (i - 2) * 6 + Math.cos(a) * L, y + Math.sin(a) * L); ctx.stroke(); }
  ctx.restore();
}
// mızrak: a noktasından ang yönünde L boyunda (avcı Narkissos)
// o.dip: dip ucunun a'dan geriye uzunluğu (L'nin kesri; varsayılan .45). o.dip = 0: dip ucu a'da biter (a yerdeyse mızrak yerin altına inmez)
function spear(ctx, a, ang, L, s, o = {}) {
  const dk = o.dip ?? .45;
  const b = add(a, [Math.cos(ang) * L, Math.sin(ang) * L]), c0 = add(a, [-Math.cos(ang) * L * dk, -Math.sin(ang) * L * dk]);
  ctx.save(); ctx.lineCap = 'round';
  ctx.strokeStyle = C.ink; ctx.lineWidth = 1.9 * s; ctx.beginPath(); ctx.moveTo(...c0); ctx.lineTo(...b); ctx.stroke();
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = .8 * s; ctx.stroke();
  ctx.translate(...b); ctx.rotate(ang); ctx.beginPath(); ctx.moveTo(0, -1.6 * s); ctx.lineTo(7 * s, 0); ctx.lineTo(0, 1.6 * s); ctx.closePath(); ctx.fillStyle = PC.clayR; ctx.fill(); ctx.lineWidth = .5 * s; ctx.strokeStyle = C.ink; ctx.stroke();
  ctx.restore();
}
// nergis (Narcissus poeticus): beyaz, düzensiz oval taç yapraklar (yandan basık: altı köşeli yıldız okunmasın), safran göbek, kırmızı kenarlı kadeh
// (x, y): sapın dibi; s ölçek; o: {dir (suya doğru eğik), h (sap boyu), tilt, open (0..1 açılma; 0 tomurcuk)}
function narcissus(ctx, x, y, s, t, seed, o = {}) {
  const r = rng(seed), dir = o.dir ?? 1, H0 = (o.h || 70) * (.85 + r() * .3), sway = Math.sin(t * .9 + seed * 1.7) * .035, op = o.open ?? 1;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s); ctx.rotate(sway);
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  for (const [a, L] of [[-.32, H0 * .62], [.22, H0 * .5]]) {
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(Math.sin(a) * L * .5 - 2, -L * .6, Math.sin(a) * L * 1.1, -L);
    ctx.strokeStyle = C.ink; ctx.lineWidth = 4.2; ctx.stroke(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 2.2; ctx.stroke();
  }
  const top = [7, -H0], head = [16, -H0 + 8];
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(-2, -H0 * .6, top[0], top[1]); ctx.quadraticCurveTo(13, -H0 - 2, head[0], head[1]);
  ctx.strokeStyle = C.ink; ctx.lineWidth = 3.4; ctx.stroke(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 1.5; ctx.stroke();
  ctx.translate(head[0] + 3, head[1] + 2); ctx.rotate(.55 + (o.tilt || 0));
  ctx.scale(.52, 1);
  const n = 6, a0 = r() * TAU;
  for (let i = 0; i < n; i++) {
    const a = a0 + i * TAU / n + (r() - .5) * .45, L = 11 * (.8 + r() * .35) * (.25 + .75 * op), w = L * (.42 + r() * .12);
    ctx.save(); ctx.rotate(a * op); ctx.beginPath(); ctx.ellipse(0, -L * .55, w * .5, L * .55, (r() - .5) * .3, 0, TAU);
    ctx.fillStyle = C.white; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.6; ctx.stroke(); ctx.restore();
  }
  ctx.beginPath(); ctx.ellipse(0, 0, 4.2 * op + .5, 4.2 * op + .5, 0, 0, TAU); ctx.fillStyle = '#E2A33A'; ctx.fill(); ctx.strokeStyle = '#8E2F1F'; ctx.lineWidth = 1.6; ctx.stroke();
  ctx.beginPath(); ctx.arc(0, 0, 1.6 * op, 0, TAU); ctx.fillStyle = '#6E4A12'; ctx.fill();
  ctx.restore();
}
// ışık noktaları (polen gibi; P065 incelme): belirlenimci, t ile yavaş süzülür
function motesN(ctx, t, n, seed, cx, cy, rx, ry, a = .8, col = '255,226,170') {
  const r = rng(seed);
  ctx.save(); ctx.globalCompositeOperation = 'lighter';
  for (let i = 0; i < n; i++) {
    const x = cx + (r() * 2 - 1) * rx + Math.sin(t * .4 + i) * 8, y = cy + (r() * 2 - 1) * ry - ((t * (6 + r() * 10)) % (ry * 2)) * .3, s = 1.5 + r() * 2.5, k = .5 + .5 * Math.sin(t * 1.7 + i * 2.1);
    ctx.fillStyle = `rgba(${col},${(a * k).toFixed(3)})`; ctx.beginPath(); ctx.arc(x, y, s, 0, TAU); ctx.fill();
  }
  ctx.restore();
}
