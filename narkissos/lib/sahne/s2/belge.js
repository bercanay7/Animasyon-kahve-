// BELGE seti, SAHİP-2: P077, P078, P079, P080, P085. Bu dosyayı yalnız bu sahip değiştirir.
// Gerçek görsel araları (kaynak/gorsel, lisans kaynak/GORSELLER.md) beyaz zemin lekythos çerçevesi içinde. Çerçevenin sağ alt köşesinde her belgede aynı küçük sepya Narkissos.
// Kurallar: lib/sahne/KILAVUZ.md. Ortak yardımcılar (s2_cerceve, s2_sepNark, s2_gorselKirp) SAHİP-2'nin yazı setinde (P081) de kullanılır.
'use strict';
// beyaz zemin pano (siyah sır zemin üstünde lekythos gövdesi gibi): dünya koordinatı; p 0..1 meander bordürü kendini çizer
const S2B = { x0: 300, y0: 110, x1: 1620, y1: 860, nx: 1452, ny: 806, ns: 1.55 };
function s2_cerceve(ctx, p = 1, o = {}) {
  const { x0, y0, x1, y1 } = S2B;
  ctx.save(); ctx.fillStyle = '#EFE4CC'; ctx.fillRect(x0, y0, x1 - x0, y1 - y0);
  const g = ctx.createRadialGradient((x0 + x1) / 2, (y0 + y1) / 2, 100, (x0 + x1) / 2, (y0 + y1) / 2, 900); g.addColorStop(0, 'rgba(255,250,236,.4)'); g.addColorStop(1, 'rgba(170,140,100,.28)'); ctx.fillStyle = g; ctx.fillRect(x0, y0, x1 - x0, y1 - y0);
  if (p > 0) { // bordür: üstte ve altta meander, soldan sağa çizilir
    const xe = lerp(x0, x1, clamp(p));
    ctx.save(); ctx.beginPath(); ctx.rect(x0, y0 - 60, xe - x0, y1 - y0 + 120); ctx.clip();
    meander(ctx, x0, x1, y0 + 8, 30, '#9A3B25', null); meander(ctx, x0, x1, y1 - 38, 30, '#9A3B25', null);
    ctx.restore();
  }
  ctx.strokeStyle = 'rgba(59,42,30,.55)'; ctx.lineWidth = 3; ctx.strokeRect(x0, y0, x1 - x0, y1 - y0);
  ctx.restore();
}
// küçük sepya Narkissos (beyaz zemin vazo çizgisi): havuz başında yüzüstü uzanmış. o: {lean 0..1 suya eğilir, a, s}
function s2_sepNark(ctx, t, x, y, o = {}) {
  const s = o.s ?? S2B.ns, lean = o.lean || 0;
  ctx.save(); ctx.globalAlpha *= o.a ?? 1;
  // havuz: sepya kontur, soluk sepya su çizgileri
  ctx.strokeStyle = C.sepia; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.ellipse(x + 46 * s, y + 4 * s, 44 * s, 6 * s, 0, 0, TAU); ctx.stroke();
  ctx.strokeStyle = 'rgba(59,42,30,.35)'; ctx.lineWidth = 1.4; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.moveTo(x + (24 + k * 18) * s, y + (3 + k) * s); ctx.lineTo(x + (34 + k * 18) * s, y + (3 + k) * s); ctx.stroke(); }
  const f = proneFig(x - 30 * s, y, s, { ...pPose({ head: .25 * lean, neck: .2 * lean, handN: 'flat' }), hemPerp: true, hemT: .62 }, { hN: [x + 2 * s, y], hF: [x - 1 * s, y], flatFeet: -2.9, sty: STY.white, idle: .3, stripe: 0 });
  f.sty = STY.white; f.contour = false;
  const { J } = joints(ctx, f); f.p = { ...f.p, wrN: .12 - J.AN.foA, wrF: .12 - J.AF.foA };
  withFigT(t, () => figure(ctx, f));
  ctx.restore();
  return f;
}
// görselin bir bölümünü (u0,v0,u1,v1: 0..1) dünya kutusuna sığdırarak basar; döner [x0,y0,w,h]
function s2_gorselKirp(ctx, ad, cx, cy, w, h, k = [0, 0, 1, 1], o = {}) {
  const im = gorsel(ad); if (!im) return null;
  const sx = im.width * k[0], sy = im.height * k[1], sw = im.width * (k[2] - k[0]), sh = im.height * (k[3] - k[1]);
  const sc = Math.min(w / sw, h / sh), dw = sw * sc, dh = sh * sc, x0 = cx - dw / 2, y0 = cy - dh / 2;
  ctx.save(); ctx.globalAlpha *= o.a ?? 1; ctx.drawImage(im, sx, sy, sw, sh, x0, y0, dw, dh);
  if (o.mult) { ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha *= o.mult; ctx.fillStyle = '#C9A27A'; ctx.fillRect(x0, y0, dw, dh); }
  if (o.line !== false) { ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = (o.a ?? 1); ctx.strokeStyle = 'rgba(59,42,30,.6)'; ctx.lineWidth = 2; ctx.strokeRect(x0, y0, dw, dh); }
  ctx.restore();
  return [x0, y0, dw, dh];
}
// belge sahnesinin zemini: siyah sır + pano; kamera
function s2_belgeZemin(ctx, cam, bp = 1) { baseT(ctx); glaze(ctx, 960, 500, 1200, 'rgba(110,44,20,.35)'); camAt(ctx, ...cam); s2_cerceve(ctx, bp); }
// 1646 ahlak satırının sepya Narkissos'un gövdesindeki yeri (P078 sonu, P079, P080 başı)
const S2_SATIR = { cx: S2B.nx + 20, cy: S2B.ny - 26, w: 330, rot: -.2 };
function s2_satirCiz(ctx, cx, cy, w, rot, a = 1, wipe = 0) {
  const im = gorsel('callot1646_satir.jpg'); if (!im) return;
  const h = w * im.height / im.width;
  ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot); ctx.globalAlpha *= a;
  if (wipe > 0) { ctx.beginPath(); ctx.rect(-w / 2 + w * wipe, -h, w, 3 * h); ctx.clip(); }
  ctx.globalCompositeOperation = 'multiply'; ctx.drawImage(im, -w / 2, -h / 2, w, h); ctx.restore();
}

(() => {
  const POST = { tex: .25, vig: .55 };
  // P077 · geniş · F02 · Tempesta 1606 beyaz zemin çerçevede; bordür kendini çizer; köşedeki sepya Narkissos suya eğilir; köşede yıl
  plan('P077', (ctx, st) => {
    const t = st.t, tA = PE('P077', 0), tB = PE('P077', 1);
    s2_belgeZemin(ctx, s2_cam(st, [960, 490, .98], [990, 500, 1.06]), ramp(t, tA - .3, tA + 1.4, E.io2));
    s2_gorselKirp(ctx, 'tempesta1606.jpg', 860, 470, 860, 640, [0, 0, 1, 1], { mult: .12 });
    s2_sepNark(ctx, t, S2B.nx, S2B.ny, { lean: ramp(t, tA, tA + 1.2, E.io2) });
    txtDipinto(ctx, '1606', 1490, 700, 40, ramp(t, tB - .1, tB + .7, E.lin), { col: C.sepia });
  }, { post: POST, over: (ctx, st) => kunye(ctx, 'Antonio Tempesta, 1606 · The Met, CC0', st.lt - .4, st.d) });

  // P078 · orta · F02@basılan · Callot / 1646 levhası (yalnız üst satır ve ağaç tepesi; diz üstü figür kadraj dışında: hassasiyet). Satır levhadan kalkar, sepya Narkissos'un gövdesine çapraz iner
  plan('P078', (ctx, st) => {
    const t = st.t, tK = PE('P078', 0), tG = PE('P078', 1);
    s2_belgeZemin(ctx, s2_cam(st, [1000, 520, 1.12], [1060, 470, 1.16]));
    const ot = ramp(t, tK - .4, tK + .3, E.out2);
    const box = s2_gorselKirp(ctx, 'callot1646_resim_satir.jpg', 860 + 0 * ot, 420 + 30 * (1 - ot), 900, 600, [0, .1, 1, .46], { mult: .1, a: ot });
    // üst satır: levhanın üstünden kalkar ve köşeye uçar
    const u = ramp(t, tG - .2, tG + 1.6, E.io2), w0 = 900, a0 = [860, box ? box[1] - 34 : 260];
    s2_satirCiz(ctx, lerp(a0[0], S2_SATIR.cx, u), lerp(a0[1], S2_SATIR.cy, u) - Math.sin(PI * u) * 120, lerp(w0, S2_SATIR.w, u), lerp(0, S2_SATIR.rot, u), ot);
    s2_sepNark(ctx, t, S2B.nx, S2B.ny, { lean: 1 });
  }, { post: POST, over: (ctx, st) => kunye(ctx, 'Jacques Callot, Lux Claustri · 1646 baskısı · The Met, CC0', st.lt - .3, st.d) });

  // P079 · ayrıntı · F02@aşırı · LEVHA · Satırın yakını, altında sepya Narkissos'un gövdesi; satırın altı vazo kırmızısıyla çizilir; Türkçe çeviri
  plan('P079', (ctx, st) => {
    const t = st.t, tK = PE('P079', 0);
    const cx = S2_SATIR.cx, cy = S2_SATIR.cy;
    s2_belgeZemin(ctx, [lerp(cx - 70, cx + 40, E.sine(st.p)), cy + 40, 3.0]);
    s2_sepNark(ctx, t, S2B.nx, S2B.ny, { lean: 1 });
    s2_satirCiz(ctx, cx, cy, S2_SATIR.w, S2_SATIR.rot);
    const u = ramp(t, tK - .1, tK + 1.0, E.io2); // satırın altı kırmızı fırça
    if (u > 0) { ctx.save(); ctx.translate(cx, cy); ctx.rotate(S2_SATIR.rot); ctx.strokeStyle = '#B23A22'; ctx.lineWidth = 3.2; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(-S2_SATIR.w / 2 + 4, 14); for (let k = 1; k <= 30 * u; k++) ctx.lineTo(-S2_SATIR.w / 2 + 4 + (S2_SATIR.w - 8) * k / 30, 14 + Math.sin(k * 1.3) * 1.2); ctx.stroke(); ctx.restore(); }
  }, { post: POST, over: (ctx, st) => quote(ctx, '“Aşırı öz-sevgi, kendi yıkımının sebebidir.” (çevirimiz)', W / 2, 220, st.t - PE('P079', 1) + .1, { px: 64, maxW: 1400 }) });

  // P080 · orta · F03 · Sepya Narkissos köşeden ortaya büyür; ahlak satırı silinir; kenar notu; Ellis 1898 kırpması yerine oturur; "Narcissus-like" kırmızı halka
  plan('P080', (ctx, st) => {
    const t = st.t, tS = PE('P080', 0), tT = PE('P080', 1), tI = PE('P080', 2), tN = PE('P080', 3), tE = PE('P080', 4);
    const grow = ramp(t, st.at, tS + 1.6, E.io2), wipe = ramp(t, tS - .1, tS + 1.0, E.io2);
    s2_belgeZemin(ctx, camMix(s2_cam({ p: ramp(t, st.at, tI, E.lin) }, [1030, 500, 1.0], [990, 505, 1.04]), [960, 520, 1.12], ramp(t, tI, st.end, E.sine)));
    const nx = lerp(S2B.nx, 700, grow), ny = lerp(S2B.ny, 640, grow), ns = lerp(S2B.ns, 4.2, grow);
    s2_sepNark(ctx, t, nx, ny, { s: ns, lean: 1 });
    if (wipe < 1) { const c2 = [lerp(S2_SATIR.cx, nx + 20 * ns / S2B.ns, grow), lerp(S2_SATIR.cy, ny - 26 * ns / S2B.ns, grow)]; s2_satirCiz(ctx, c2[0], c2[1], S2_SATIR.w * ns / S2B.ns, S2_SATIR.rot, 1, wipe); }
    // kenar notu (okunmaz el yazısı çizgileri) → Ellis kırpması
    const nt = ramp(t, tT - .1, tT + 1.2, E.lin) * (1 - ramp(t, tI - .1, tI + .3));
    if (nt > 0) { ctx.save(); ctx.strokeStyle = C.sepia; ctx.lineWidth = 2.4; ctx.lineCap = 'round'; for (let l = 0; l < 4; l++) { const L = clamp(nt * 4 - l); if (L <= 0) continue; ctx.beginPath(); for (let k = 0; k <= 40 * L; k++) { const x = 1080 + k * 11, y = 360 + l * 46 + Math.sin(k * 1.9 + l) * 6 + Math.sin(k * .7) * 3; k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); } ctx.restore(); }
    const ea = ramp(t, tI - .1, tI + .5, E.out2);
    if (ea > 0) { const b = s2_gorselKirp(ctx, 'ellis1898_satir.png', 1260, 420, 640, 60, [0, 0, 1, 1], { a: ea, mult: .1 });
      const hr = ramp(t, tN - .1, tE + .2, E.io2); // "Narcissus-like" kırmızı halka (elle çizilmiş, kırpmanın içinde)
      if (b && hr > 0) { const hx = b[0] + b[2] * .605, hy = b[1] + b[3] * .5, rx = b[2] * .15, ry = b[3] * .95; ctx.save(); ctx.strokeStyle = '#B23A22'; ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.beginPath(); ctx.ellipse(hx, hy, rx, ry, -.04, PI * .8, PI * .8 + TAU * hr * 1.03); ctx.stroke(); ctx.restore(); } }
  }, { post: POST, over: (ctx, st) => kunye(ctx, 'Havelock Ellis · 1898', st.t - PE('P080', 2) - .3, 99) });

  // P085 · yakın · F05 · Freud 1914 ilk sayfa beyaz zemin çerçevede; başlık kırmızıyla çizilir; kamera geri kayar; sepya Narkissos'un yanında başlığın sorusu kırmızı fırçayla; altında boş şerit
  plan('P085', (ctx, st) => {
    const t = st.t, tF = PE('P085', 0), tB = PE('P085', 1), tS = PE('P085', 2), tC = PE('P085', 3);
    const back = ramp(t, tB - .2, tB + 1.8, E.io2);
    s2_belgeZemin(ctx, camMix(s2_cam({ p: ramp(t, st.at, tB, E.lin) }, [820, 330, 1.7], [820, 320, 1.8]), [960 + 40 * ramp(t, tB, st.end, E.lin), 490, 1.0 + .05 * ramp(t, tB, st.end, E.lin)], back));
    const b = s2_gorselKirp(ctx, 'freud1914_s1_baslik.jpg', 820, 330, 900, 330, [0, 0, 1, 1], { mult: .1 });
    const u = ramp(t, tF - .1, tF + 1.0, E.io2); // başlığın altı kırmızı
    if (b && u > 0) { ctx.save(); ctx.strokeStyle = '#B23A22'; ctx.lineWidth = 4; ctx.lineCap = 'round'; const x0 = b[0] + b[2] * .27, x1 = b[0] + b[2] * .73, y = b[1] + b[3] * .215; ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(lerp(x0, x1, u), y + Math.sin(u * 9) * 1.5); ctx.stroke(); ctx.restore(); }
    s2_sepNark(ctx, t, S2B.nx, S2B.ny, { lean: 1 });
    txtDipinto(ctx, 'narsisizm', S2B.nx + 40, S2B.ny + 30, 22, 1, { col: C.sepia, w: 600, ls: 3 });
    // başlığın sorusu: sepya Narkissos'un yanında kırmızı fırçayla (sahnenin parçası)
    const q = ramp(t, tS - .1, tS + 2.0, E.lin);
    if (q > 0) { ctx.save(); ctx.font = FONT.alinti(54, 600); ctx.fillStyle = '#B23A22'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
      const L1 = 'Kendini sevmek ne zaman', L2 = 'narsisizme döner?', n1 = [...L1].length, n2 = [...L2].length, k = Math.round((n1 + n2) * q);
      ctx.fillText([...L1].slice(0, Math.min(n1, k)).join(''), 1590, 600); if (k > n1) ctx.fillText([...L2].slice(0, k - n1).join(''), 1590, 664); ctx.restore(); }
    const sp = ramp(t, tC - .1, tC + .8, E.io2); // cevap yeri: boş şerit
    if (sp > 0) { ctx.save(); ctx.strokeStyle = 'rgba(178,58,34,.8)'; ctx.lineWidth = 2.5; ctx.setLineDash([10, 8]); ctx.strokeRect(1590 - 460 * sp, 704, 460 * sp, 48); ctx.restore(); }
  }, { post: POST, over: (ctx, st) => kunye(ctx, 'Sigmund Freud · Narsisizm Üzerine, 1914', st.lt - .4, st.d) });
})();
