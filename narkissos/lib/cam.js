// Telefon camı (bugünün genci) ve cam ↔ havuz dönüşümü. ORTAK DOSYA: yalnız başkan değiştirir.
// Kapı kodundan (kapi/vazo/nark.js, plan A/E, tur 3 = PH3) ayrıldı; davranış aynı. Zamanlar çağırandan gelir (Wd/A), burada sabit saniye yok.
//
// phoneScene(ctx, t, o): kareyi baştan çizer (zemin dahil); döner: figür nesnesi f.
//   o.m        0 telefon camı … 1 havuz (morphPts ile biçim dönüşümü; cam ayrıntıları ve el söner)
//   o.cam      [fx, fy, z] sahne kamerası (PH3 için tipik: [720, 650, .82] → yaklaşma .86; havuza inerken [1000, 760, 1.3])
//   o.light    ekran ışığı 0..1 (alttan, nötr; çene altında sıcak parıltı yok)
//   o.refA     yansıma saydamlığı (camda .2, havuzda .42)
//   o.thumb    başparmak kaydırma 0..1 (thumbFlick ile)   o.feed / o.feedA: akış kartlarının kayması (birim) ve görünürlüğü
//   o.headNod  baş eğimi ekleri   o.rings: (pcx, wy, eye) => [halka…] ya da dizi   o.blink
//   ...PH3     kapı tur 3 geometrisi (yansıma tam altta, cam yüzden uzak, nötr yüz, cam parlaması, el sol alt köşede)
// Örnek (P001'in kapıdaki karşılığı, sözcük zamanlarıyla):
//   const fl = [A('A01')-.4, A('A01@camda'), …]; const th = thumbFlick(t, fl); const feed = feedOffset(t, fl);
//   phoneScene(ctx, t, { ...PH3, m: ramp(t, a0, a1, E.io2), thumb: th, feed, feedA: 1 - ramp(t, k0, k1), cam: [...], light: .8, refA: .2 });
'use strict';
// kapı tur 3 geometrisi
const PH3 = { refDx: 0, phDx: 140, pw: 230, wy: 630, armToPhone: true, headA: .3, neckA: .3, neutral: true, glare: 1, handY: 480, eyeCalm: 55 };
// başparmak kaydırması: flicks = kaydırma başlangıç zamanları (sn); 0..1
function thumbFlick(t, flicks) { return flicks.reduce((v, f0) => Math.max(v, ramp(t, f0, f0 + .24, E.io2) * (1 - ramp(t, f0 + .3, f0 + .58, E.io2))), 0); }
// akış kartlarının toplam kayması (her kaydırmada 330 birim)
function feedOffset(t, flicks) { return flicks.reduce((v, f0) => v + 330 * E.out3(ramp(t, f0 + .1, f0 + .5, E.lin)), 0); }
function phoneScene(ctx, t, o) {
  const m = o.m; // 0 telefon camı, 1 havuz
  baseT(ctx);
  glaze(ctx, 1100, 820, 1100, `rgba(${lerp(80, 120, m) | 0},${lerp(42, 48, m) | 0},${lerp(28, 22, m) | 0},.45)`);
  const p = { torso: .3, neck: o.neckA ?? .42, head: (o.headA ?? .55) + (o.headNod || 0), shN: .38, elN: .5, shF: .32, elF: .55, handN: 'fist', handF: 'fist', smile: 0, brow: .15, mouthOpen: 0, blink: o.blink,
    mouthFlat: !!o.neutral, eyeWide: o.neutral ? .3 : 0 }; // tur 3: nötr ağız, açık göz
  let f = { x: 0, y: 0, s: 20.5, dir: 1, sty: STY.red, lk: LK_MOD, seed: 31, idle: .6, p, faceW: 1.35, stripe: .35 };
  f = placeNeck(ctx, f, o.neck || [640, 370]);
  const { J: J0, M: M0 } = joints(ctx, f), e = headPt(ctx, J0, M0, [3.7, -6.75]);
  // küçük telefon camı (yüzün iki katı kadar), eğik tutulduğu için yansıma camın ortasına kayar (dxR)
  // tur 3: yansıma gerçek başın tam altında (dx = 0), cam yüzden uzak (wy), cam başın altında; iki yüz çapraz 'öpüşme' çizgisi kurmasın
  const wy = o.wy ?? 600, pcx = e[0] + (o.phDx ?? 330), pw = o.pw ?? 270;
  const dxR = o.refDx != null ? o.refDx : o.dxFixed ? pcx - e[0] - 20 : lerp(pcx - e[0] - 20, 0, m);
  const hy = o.handY ?? 340;
  if (o.armToPhone) { f.ik = { hN: [pcx - pw - 70, wy + hy + 120 + 420 * m] }; f.noFarArm = true; } // tur 3: yakın kol telefonu tutan ele uzanır (kamera geniş; sarkan yumruk görünmesin)
  if (o.auto) o.cam = [pcx - 120, wy + 40, o.cam[2]];
  camAt(ctx, ...o.cam);
  const phone = roundRectPts(pcx - pw, wy, pcx + pw, wy + 900, 56, 56);
  const pool = ellipsePts(pcx - 100, wy + 360, 1300, 360);
  const shape = morphPts(phone, pool, m);
  const clip = c => poly(c, shape);

  // figür: omuz başı solda kadraj kenarında, başı ekrana eğik; ekran ışığı alttan

  waterBody(ctx, clip, wy, t, { a: .2 * m, seed: 6, span: [300, 2100], n: 40 });
  if (o.feedA > .005) phoneFeed(ctx, clip, pcx, pw, wy, o.feed || 0, o.feedA * (1 - m));
  // eğik cam: yansıma camın ortasına kayar (dx)
  const rings = typeof o.rings === 'function' ? o.rings(pcx, wy, e) : o.rings;
  mirror(ctx, c => figure(c, f), wy, clip, t, { a: o.refA ?? .42, rings, calm: lerp(.15, 1.2, m), dx: dxR, calmAt: o.eyeCalm ? { x: e[0] + dxR, y: 2 * wy - e[1], r: o.eyeCalm } : null });
  const ph = 1 - m;
  if (o.glare && ph > .01) glassGlare(ctx, clip, pcx, wy, pw, ph * o.glare, t);
  if (ph > .01) { // cam parıltısı ve telefon ayrıntıları: havuza dönerken söner
    ctx.save(); ctx.beginPath(); clip(ctx); ctx.clip();
    const g = ctx.createLinearGradient(pcx - 200, wy, pcx + 250, wy + 600); g.addColorStop(0, 'rgba(255,240,215,0)'); g.addColorStop(.45, `rgba(255,240,215,${.07 * ph})`); g.addColorStop(.55, `rgba(255,240,215,${.07 * ph})`); g.addColorStop(1, 'rgba(255,240,215,0)');
    ctx.fillStyle = g; ctx.fillRect(600, wy, 1100, 900);
    ctx.restore();
    ctx.save(); ctx.globalAlpha = ph; ctx.fillStyle = '#21160f';
    ctx.beginPath(); ctx.roundRect(pcx - 50, wy + 20, 100, 13, 6.5); ctx.fill();
    ctx.beginPath(); ctx.arc(pcx + 78, wy + 26, 7, 0, TAU); ctx.fill();
    ctx.restore();
  }
  ctx.save(); ctx.beginPath(); poly(ctx, shape); ctx.lineWidth = lerp(4.5, 6, m); ctx.strokeStyle = mixCol('#B9653A', '#C9703F', m); ctx.lineJoin = 'round'; ctx.stroke(); ctx.restore();
  if (o.light > 0) { ctx.save(); ctx.globalCompositeOperation = 'lighter'; glow(ctx, pcx - 120, wy, 420, `rgba(255,220,170,${.14 * o.light})`); ctx.restore(); }
  litFigure(ctx, f, { x: e[0] + 120, y: wy + 20, r: 430, c: 'rgba(255,226,186,A)', a: .34 * o.light, dark: .25 + .25 * o.light });
  if (ph > .02) phoneHand(ctx, pcx - pw, wy, t, ph, o.thumb || 0, o.light, hy);
  return f;
}
// tur 3: çapraz cam parlaması: yansımanın üstünden geçen iki paralel, yumuşak kenarlı şerit (sağ üstten sol alta); 'cam' okunsun, yansıma camın içinde kalsın
function glassGlare(ctx, clip, pcx, wy, pw, a, t) {
  ctx.save(); ctx.beginPath(); clip(ctx); ctx.clip();
  const ang = -.62, ca = Math.cos(ang), sa = Math.sin(ang), drift = 6 * Math.sin(t * .5);
  for (const [off, w, k] of [[-40, 110, 1], [120, 38, .7]]) {
    const cx = pcx + off + drift, cy = wy + 330;
    // şeridin ekseni yönü (ca, sa); dik yönde (−sa, ca) yumuşak profil
    const nx = -sa, ny = ca;
    const g = ctx.createLinearGradient(cx - nx * w, cy - ny * w, cx + nx * w, cy + ny * w);
    g.addColorStop(0, 'rgba(255,236,210,0)'); g.addColorStop(.35, `rgba(255,236,210,${.13 * k * a})`); g.addColorStop(.5, `rgba(255,240,220,${.17 * k * a})`); g.addColorStop(.65, `rgba(255,236,210,${.13 * k * a})`); g.addColorStop(1, 'rgba(255,236,210,0)');
    ctx.fillStyle = g; ctx.beginPath();
    const L = 1400;
    ctx.moveTo(cx - ca * L - nx * w, cy - sa * L - ny * w); ctx.lineTo(cx + ca * L - nx * w, cy + sa * L - ny * w); ctx.lineTo(cx + ca * L + nx * w, cy + sa * L + ny * w); ctx.lineTo(cx - ca * L + nx * w, cy - sa * L + ny * w); ctx.closePath(); ctx.fill();
  }
  ctx.restore();
}
// ekran içeriği (akış): camın arkasında soluk kartlar; her kaydırmada yukarı kayar (tur 2: kaydırma görünür olsun)
function phoneFeed(ctx, clip, pcx, pw, wy, off, a) {
  ctx.save(); ctx.beginPath(); clip(ctx); ctx.clip();
  const x0 = pcx - pw + 46, w = 2 * pw - 92, H = 330;
  for (let k = -1; k < 6; k++) {
    const y = wy + 80 + k * H - off; if (y > wy + 1000 || y + H < wy) continue;
    ctx.globalAlpha = a;
    ctx.fillStyle = 'rgba(255,226,186,.09)'; ctx.beginPath(); ctx.roundRect(x0, y, w, 210, 18); ctx.fill();
    ctx.fillStyle = 'rgba(255,226,186,.1)';
    ctx.beginPath(); ctx.arc(x0 + 26, y + 238, 18, 0, TAU); ctx.fill();
    ctx.beginPath(); ctx.roundRect(x0 + 56, y + 228, w * (.45 + .2 * ((k * 7 + 3) % 3) / 2), 12, 6); ctx.fill();
    ctx.beginPath(); ctx.roundRect(x0 + 56, y + 252, w * .3, 10, 5); ctx.fill();
  }
  ctx.restore();
}
// telefonu tutan el (tur 2): avuç camın sol kenarının arkasında, alt köşede; başparmak kısa (iki boğum + tırnak), camın sol alt kenarında
// th 0..1: kaydırma (başparmak yukarı süpürür, uç ~60 birim yol alır); yüzün yansımasına (ağız, çene) hiç yaklaşmaz
function phoneHand(ctx0, X0, wy, t, a, th, light, hy = 340) {
  const T = ctx0.getTransform(), ctx = layer('hand'); ctx.setTransform(T);
  ctx.save(); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  const Y = wy + hy, ink = C.ink, skin = '#C9703F';
  // kol (ceket kolu) alttan sola
  ctx.beginPath(); ctx.moveTo(X0 - 300, Y + 420); ctx.quadraticCurveTo(X0 - 210, Y + 190, X0 - 110, Y + 105); ctx.lineTo(X0 - 30, Y + 175); ctx.quadraticCurveTo(X0 - 110, Y + 260, X0 - 140, Y + 440); ctx.closePath();
  ctx.fillStyle = '#6E331B'; ctx.fill(); ctx.strokeStyle = ink; ctx.lineWidth = 4; ctx.stroke();
  ctx.beginPath(); ctx.moveTo(X0 - 118, Y + 116); ctx.lineTo(X0 - 40, Y + 186); ctx.lineWidth = 2.4; ctx.stroke(); // kol ağzı
  // başparmak: kök avuçta (X0-26, Y+40); iki boğum; kaydırırken yukarı döner ve düzleşir
  const B = [X0 - 26, Y + 40], aP = lerp(.1, -1.1, th), bend = lerp(.45, .1, th), L1 = 40, L2 = 32, W1 = 13, W2 = 11.5;
  const K = [B[0] + Math.cos(aP) * L1, B[1] + Math.sin(aP) * L1], aD = aP - bend, P = [K[0] + Math.cos(aD) * L2, K[1] + Math.sin(aD) * L2];
  const nrm = a0 => [-Math.sin(a0), Math.cos(a0)], n1 = nrm(aP), n2 = nrm(aD), nk = nrm((aP + aD) / 2);
  ctx.beginPath();
  ctx.moveTo(B[0] - n1[0] * W1, B[1] - n1[1] * W1);
  ctx.lineTo(K[0] - nk[0] * W1 * .95, K[1] - nk[1] * W1 * .95);
  ctx.lineTo(P[0] - n2[0] * W2, P[1] - n2[1] * W2);
  ctx.arc(P[0], P[1], W2, aD - PI / 2, aD + PI / 2);
  ctx.lineTo(K[0] + nk[0] * W1 * 1.05, K[1] + nk[1] * W1 * 1.05);
  ctx.lineTo(B[0] + n1[0] * W1 * 1.15, B[1] + n1[1] * W1 * 1.15);
  ctx.closePath(); ctx.fillStyle = skin; ctx.fill(); ctx.lineWidth = 3.6; ctx.strokeStyle = ink; ctx.stroke();
  // boğum çizgisi ve tırnak (üst yüzde, uca yakın)
  ctx.beginPath(); ctx.moveTo(K[0] - nk[0] * W1 * .7, K[1] - nk[1] * W1 * .7); ctx.lineTo(K[0] - nk[0] * W1 * .05, K[1] - nk[1] * W1 * .05); ctx.lineWidth = 2.2; ctx.stroke();
  const dn = [Math.cos(aD), Math.sin(aD)], nc = [P[0] - dn[0] * 9 - n2[0] * 4.5, P[1] - dn[1] * 9 - n2[1] * 4.5];
  ctx.save(); ctx.translate(...nc); ctx.rotate(aD); ctx.beginPath(); ctx.roundRect(-8, -5.5, 17, 11, [3, 5.5, 5.5, 3]); ctx.fillStyle = '#DE9564'; ctx.fill(); ctx.lineWidth = 2; ctx.stroke(); ctx.restore();
  // avuç: camın sol kenarını arkadan kavrar; iki parmak ucu camın kenarında
  ctx.beginPath(); ctx.moveTo(X0 - 112, Y + 108); ctx.quadraticCurveTo(X0 - 92, Y + 30, X0 - 30, Y + 4); ctx.lineTo(X0 + 6, Y + 14); ctx.lineTo(X0 + 8, Y + 150); ctx.quadraticCurveTo(X0 - 20, Y + 186, X0 - 36, Y + 180); ctx.closePath();
  ctx.fillStyle = skin; ctx.fill(); ctx.lineWidth = 4; ctx.stroke();
  for (const yy of [92, 130]) { ctx.beginPath(); ctx.moveTo(X0 - 8, Y + yy); ctx.quadraticCurveTo(X0 + 14, Y + yy - 2, X0 + 16, Y + yy + 14); ctx.quadraticCurveTo(X0 + 8, Y + yy + 26, X0 - 6, Y + yy + 24); ctx.fillStyle = skin; ctx.fill(); ctx.lineWidth = 3; ctx.stroke(); }
  // ekran ışığı elin üstünde
  ctx.globalCompositeOperation = 'source-atop';
  const g = ctx.createRadialGradient(X0 + 80, Y - 80, 0, X0 + 80, Y - 80, 340); g.addColorStop(0, `rgba(255,226,186,${.3 * light})`); g.addColorStop(1, 'rgba(255,226,186,0)');
  ctx.fillStyle = g; ctx.fillRect(X0 - 600, Y - 400, 1200, 1200);
  ctx.restore();
  ctx0.save(); ctx0.setTransform(1, 0, 0, 1, 0, 0); ctx0.globalAlpha = a; ctx0.drawImage(LY.hand, 0, 0); ctx0.restore();
}
