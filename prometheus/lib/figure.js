// Siyah figür karakter rigi: profil gövde, ters kinematik bacak/kol, kazıma (incision) çizgileri.
// Figür yerel birimi: boy ≈ 100 birim, köken leğen kemiği, y aşağı, yüz +x yönüne bakar.
'use strict';
const BL = { torso: 30, neck: 5, up: 16, fo: 14, th: 23, sh: 22, ank: 3 };
const FIG_CV = { sil: null, fig: null };
// ara tuvaller hedef tuval kadar büyür (amfora şeridi ekran genişliğinden geniştir)
function figCanvases(w = DW, h = DH) {
  if (!FIG_CV.sil || FIG_CV.sil.width < w || FIG_CV.sil.height < h) {
    const cw = Math.max(w, FIG_CV.sil ? FIG_CV.sil.width : DW), ch = Math.max(h, FIG_CV.sil ? FIG_CV.sil.height : DH);
    FIG_CV.sil = makeCanvas(cw, ch); FIG_CV.fig = makeCanvas(cw, ch);
  }
  return FIG_CV;
}

// İki kemikli ters kinematik: kök r, hedef g, uzunluklar a,b; bend=+1 diz öne, -1 dirsek arkaya
function ik2(r, g, a, b, bend) {
  let dx = g[0] - r[0], dy = g[1] - r[1], d = Math.hypot(dx, dy);
  const dmax = (a + b) * .9995, dmin = Math.abs(a - b) + .01;
  const dd = clamp(d, dmin, dmax);
  const phi = Math.atan2(dy, dx);
  const al = Math.acos(clamp((a * a + dd * dd - b * b) / (2 * a * dd), -1, 1));
  const ua = phi - bend * al; // birinci kemik yönü (açı, standart)
  const j = [r[0] + Math.cos(ua) * a, r[1] + Math.sin(ua) * a];
  const e = [r[0] + Math.cos(phi) * dd, r[1] + Math.sin(phi) * dd];
  return { j, e, ua, la: Math.atan2(e[1] - j[1], e[0] - j[0]) };
}
// standart açı (atan2) -> "aşağıdan ileri" açı
const fwdA = a => PI / 2 - a;
const dirF = a => [Math.sin(a), Math.cos(a)]; // ileri-açıdan yön vektörü

// Uzuv profilleri: [t, ön genişlik, arka genişlik]
const PROF = {
  thigh: [[0, 5.4, 5.8], [.28, 6.0, 5.5], [.6, 4.9, 4.8], [.86, 3.6, 3.7], [1, 3.25, 3.3]],
  shin: [[0, 3.3, 3.3], [.13, 3.1, 4.5], [.32, 3.0, 5.0], [.58, 2.5, 3.3], [.86, 1.9, 2.0], [1, 1.75, 1.85]],
  up: [[0, 3.6, 3.7], [.18, 4.3, 3.6], [.55, 3.3, 3.2], [1, 2.45, 2.45]],
  fo: [[0, 2.45, 2.45], [.25, 3.0, 2.75], [.7, 2.0, 2.05], [1, 1.6, 1.7]],
  // ince (kadın / genç) gövde için çarpanlar ayrıca uygulanır
};
function limbPts(prof, L, k = 1) {
  const f = prof.map(([t, a]) => [a * k, t * L]);
  const b = prof.slice().reverse().map(([t, , c]) => [-c * k, t * L]);
  return f.concat(b);
}
const TORSO = [
  [3.0, -31.6], [6.4, -29.6], [9.5, -25.6], [9.7, -21.6], [7.3, -18.6], [6.3, -12.6], [6.9, -6.2], [5.3, -1.2],
  [2.6, 2.6], [-2.0, 3.8], [-6.6, 1.6], [-8.4, -3.0], [-6.4, -9.0], [-6.2, -15.0], [-7.6, -21.0], [-7.4, -27.0], [-4.6, -30.5], [-2.2, -31.8]];
// düz göğüslü erkek gövdesi (Prometheus): göğüs altı girintisi yumuşak, kadın göğsü konturu oluşmaz
const TORSO_M = [
  [3.0, -31.6], [6.4, -29.8], [9.0, -25.6], [9.1, -21.8], [7.8, -18.4], [6.5, -12.6], [6.9, -6.2], [5.3, -1.2],
  [2.6, 2.6], [-2.0, 3.8], [-6.6, 1.6], [-8.4, -3.0], [-6.4, -9.0], [-6.2, -15.0], [-7.6, -21.0], [-7.4, -27.0], [-4.6, -30.5], [-2.2, -31.8]];
const TORSO_F = [ // kadın gövdesi (göğüs, ince bel)
  [2.6, -31.4], [5.6, -29.4], [7.4, -26.4], [9.0, -23.0], [7.6, -19.6], [5.4, -15.6], [5.8, -9.6], [6.4, -4.2], [4.8, .2],
  [2.2, 3.0], [-2.2, 3.8], [-7.2, 1.2], [-8.0, -3.6], [-5.6, -10.0], [-5.4, -15.4], [-6.4, -21.0], [-6.6, -27.0], [-4.2, -30.4], [-2.0, -31.6]];
const FOOT = [[-2.7, .2], [-2.9, 2.2], [-2.0, 3.0], [9.4, 3.0], [11.0, 2.5], [10.4, 1.5], [6.0, .5], [2.2, -1.6], [-1.6, -1.8]];
const HAND = {
  open: [[-1.7, 0], [1.7, 0], [2.3, 2.6], [2.0, 5.6], [.7, 7.0], [-.9, 6.7], [-1.9, 4.2]],
  fist: [[-1.8, 0], [1.8, 0], [2.6, 2.2], [2.5, 4.4], [.8, 5.0], [-1.6, 4.7], [-2.3, 2.6]],
  flat: [[-1.6, 0], [1.6, 0], [2.0, 2.6], [1.7, 6.0], [.6, 7.8], [-.6, 7.6], [-1.6, 4.4]],
  point: [[-1.8, 0], [1.8, 0], [2.4, 2.2], [2.5, 4.2], [1.2, 4.6], [1.3, 8.6], [.4, 8.8], [-.2, 4.8], [-1.6, 4.6], [-2.3, 2.6]],
  // yüzeye bastıran avuç: yandan ince görünür, iki parmak ucu ayrık (el sallama gibi okunmaz)
  press: [[-1.3, 0], [1.3, 0], [1.7, 2.4], [2.0, 5.2], [1.4, 7.4], [.7, 6.0], [.3, 7.7], [-.5, 7.3], [-1.3, 4.2]],
};
const CUFF = G => { G.part(c => c.rect(-3.0, -3.2, 6.0, 3.4), { fill: C.ink, cutW: .3 }); G.paint(c => { c.moveTo(-2.8, -1.5); c.lineTo(2.8, -1.5); }, typeof PC !== 'undefined' ? PC.clayR : C.clay, .35, false); };
// yazılı kelepçe: yazı bandın içine, bilek ekseninde kazınır (P130 ΔΕΣΜΩΤΗΣ); harf ≈ 1 birim, 1,5 px kil çizgi
const CUFF_TXT = str => G => { CUFF(G); if (G.pass === 'fig') dipinto(G.g, str, 0, -1.45, 1.0, { col: typeof PC !== 'undefined' ? PC.clayRL : C.clay, w: .09 }); };
const THUMB = [[1.5, .8], [3.6, 2.6], [3.4, 3.8], [1.4, 3.0]];

// --- Kafa şekilleri ---
function headOutline(lk) {
  const top = [[5.75, -9.5], [4.9, -11.5], [3.2, -13.1], [.6, -13.9], [-2.6, -13.5], [-5.2, -11.6], [-6.4, -8.8]];
  const nose = lk.fem
    ? [[5.6, -3.0], [5.95, -3.4], [5.75, -3.85], [6.0, -4.2], [5.9, -4.7], [6.2, -5.0], [7.0, -5.15], [7.05, -5.45], [6.0, -7.6], [5.7, -8.5]]
    : [[5.95, -3.45], [5.7, -3.9], [6.0, -4.25], [5.9, -4.8], [6.3, -5.05], [7.35, -5.15], [7.45, -5.5], [6.2, -7.6], [5.8, -8.5]];
  let chin;
  if (lk.beard === 'pointed') chin = [[2.0, .9], [3.0, 2.2], [5.0, 3.9], [6.1, 1.6], [6.35, -.8], [6.05, -2.7]];
  else if (lk.beard === 'long') chin = [[1.6, 1.4], [3.2, 4.4], [5.0, 6.0], [6.2, 3.0], [6.4, -.6], [6.05, -2.7]];
  else if (lk.beard === 'full') chin = [[.9, 2.2], [2.4, 6.6], [4.6, 8.9], [6.7, 5.6], [7.1, 1.4], [6.7, -1.4], [6.05, -2.7]]; // Zeus: dolgun, uzun, kıvırcık sakal
  else if (lk.beard === 'short') chin = [[2.0, .8], [3.6, 1.2], [5.6, .6], [6.3, -1.0], [6.05, -2.7]];
  else chin = lk.fem ? [[2.3, .6], [3.6, -.7], [4.9, -1.4], [5.4, -2.2], [5.5, -2.7]] : [[2.2, .8], [3.4, -.6], [5.0, -1.4], [5.6, -2.2], [5.55, -2.95]];
  let back;
  if (lk.hair === 'long') back = [[-7.0, -5.6], [-7.7, -1.5], [-7.6, 3.4], [-7.0, 6.4], [-4.6, 6.2], [-3.9, 2.6], [-2.8, .8]];
  else if (lk.hair === 'nape') back = [[-7.0, -5.6], [-7.7, -2.4], [-7.4, .8], [-6.2, 2.4], [-4.2, 2.2], [-2.8, .8]]; // ense hizasında bukleli saç (Sert üslup)
  else back = [[-6.3, -5.8], [-5.1, -3.2], [-3.6, -1.0], [-2.8, .8]];
  return chin.concat(nose, top, back);
}
// kırmızı figür (ve beyaz zemin) erkek saçı: siyah sır kütle; kulak saçın altında kalır
const HAIR_RF = [[5.0, -10.1], [5.9, -11.0], [5.0, -12.1], [3.2, -13.7], [.6, -14.5], [-2.7, -14.1], [-5.6, -12.2], [-7.0, -9.1], [-7.5, -5.6],
  [-8.1, -1.8], [-8.0, 2.2], [-7.4, 5.2], [-6.5, 4.0], [-5.7, 5.6], [-4.6, 4.2], [-3.7, 4.7], [-3.3, 2.2], [-2.0, .2], [-.7, -2.6], [.1, -5.6], [.7, -8.1], [2.6, -9.7]];
// sivri sakal (bıyıkla): kulak altından çene ucuna, ağız kil çizgisiyle ayrılır
// ense hizasında, alt kenarı bukleli saç: Mısır başlığı (nemes) gibi okunan düz, uzun saç yerine
const HAIR_RF_N = [[5.0, -10.1], [5.9, -11.0], [5.0, -12.1], [3.2, -13.7], [.6, -14.5], [-2.7, -14.1], [-5.6, -12.2], [-7.1, -9.1], [-7.7, -5.6],
  [-8.3, -2.6], [-8.0, .6], [-7.3, 2.6], [-6.4, 1.7], [-5.6, 3.2], [-4.6, 2.0], [-3.7, 2.7], [-3.0, 1.1], [-1.9, .0], [-.7, -2.6], [.1, -5.6], [.7, -8.1], [2.6, -9.7]];
const BEARD_RF = [[5.95, -3.55], [4.6, -3.75], [2.4, -4.15], [.1, -4.7], [-.6, -2.2], [.2, .2], [1.4, 1.2], [2.4, 2.6], [3.5, 3.6], [4.7, 4.9],
  [6.1, 6.3], [6.9, 3.4], [6.6, .2], [6.15, -2.6]];
const HAIR_F = [[5.3, -10.3], [4.6, -12.1], [2.8, -13.7], [0, -14.5], [-3.3, -14.1], [-5.8, -12.4], [-8.3, -12.9], [-10.3, -10.7],
  [-9.9, -7.6], [-7.7, -6.5], [-6.6, -5.0], [-5.4, -2.4], [-3.9, -1.0], [-3.0, -3.4], [-2.2, -6.6], [.2, -9.7], [2.6, -10.6], [4.4, -10.4]];
// miğfer tepeliği: başın tepesindeki ayak üstünde, alından enseye uzanan at kılı yay (eklenmiş kırmızı), kuyruğu enseye sarkar
function helmetCrest(G, det, sty) {
  G.part(c => { c.rect(-2.6, -16.6, 2.2, 2.6); }, {});
  G.part(c => spline(c, [[4.6, -16.6], [2.0, -19.4], [-2.4, -20.6], [-7.0, -19.4], [-10.4, -16.0], [-11.8, -11.4], [-12.2, -7.4], [-10.6, -7.8], [-9.9, -11.4],
    [-8.2, -14.8], [-5.0, -16.8], [-1.4, -17.2], [2.0, -16.6]]), { fill: sty.red });
  for (let i = 0; i < 7; i++) det(c => { const a = -.25 - i * .32, r0 = 3.2, r1 = 5.6; c.moveTo(-2.2 + Math.cos(a + PI / 2 + 1.1) * r0, -14.6 - Math.sin(a + PI / 2 + 1.1) * r0); c.lineTo(-2.2 + Math.cos(a + PI / 2 + 1.1) * r1, -14.6 - Math.sin(a + PI / 2 + 1.1) * r1); }, .22);
}
const HELMET = [[6.4, -4.6], [6.9, -7.0], [6.0, -9.8], [4.4, -12.6], [1.0, -14.6], [-3.2, -14.3], [-6.2, -12.0], [-7.2, -8.2],
  [-7.0, -3.4], [-5.8, .6], [-3.4, 1.8], [-2.6, -1.6], [-.4, -2.0], [1.2, -.6], [2.6, 1.6], [4.6, 1.2], [3.8, -2.4], [2.6, -5.0], [5.2, -5.6]];

// Figür çizimi
// f = { x, y, s, dir, sty, lk:{...görünüm}, p:{...poz}, ik:{hN,hF,fN,fF}, alpha, hold:{N(g),F(g)}, extra }
function figure(ctx, f) {
  const sty = f.sty || STY.black, lk = f.lk || {};
  let p = f.p || {};
  // canlılık (animatör geçişi): her figür duruşta hafifçe nefes alır, başı oynar ve doğal aralıklarla göz kırpar
  if (!f.still && typeof idleOffsets === 'function') {
    const sd = f.seed ?? ((Math.round((f.s || 5) * 10) * 7 + (lk.fem ? 3 : 0) + (lk.beard ? lk.beard.length * 5 : 0) + (lk.hair ? lk.hair.length * 3 : 0) + (f.dir || 1) * 2 + (f.sty === STY.red ? 11 : 0)) % 97);
    const io = idleOffsets(window.FIG_T || 0, sd, f.idle ?? 1);
    p = { ...p, torso: (p.torso || 0) + io.torso, neck: (p.neck || 0) + io.neck, head: (p.head || 0) + io.head,
      breath: p.breath ?? io.breath, blink: p.blink ?? blinkAt(window.FIG_T || 0, sd) };
    f = { ...f, p };
  }
  const s = f.s || 5, dir = f.dir || 1;
  const T = p.torso || 0;
  const base = ctx.getTransform();
  const M = base.translate(f.x, f.y).scale(dir * s, s);
  const Mi = M.inverse();
  const toL = q => { const r = Mi.transformPoint(new DOMPoint((q[0] - 0) , q[1])); return [r.x, r.y]; };
  // ctx koordinatından figür yereline: önce ctx->ekran (base) sonra M^-1
  const w2l = q => { const sp = base.transformPoint(new DOMPoint(q[0], q[1])); const r = Mi.transformPoint(sp); return [r.x, r.y]; };

  const tor = lk.fem ? TORSO_F : lk.flatChest ? TORSO_M : TORSO;
  const breath = (p.breath || 0);
  const tP = q => rot([q[0] * (1 + breath * .025), q[1] * (1 - breath * .01)], T);
  const neckB = tP([.4, -30.2]), shoulder = tP([.6, -26.6]);
  const hipJ = [.3, -.6];
  // bacaklar
  const leg = (side) => {
    const tg = f.ik && f.ik[side === 'N' ? 'fN' : 'fF'];
    const L1 = BL.th, L2 = BL.sh;
    let knee, ank, thA, shA, footA;
    if (tg) {
      const g = w2l(tg);
      const r = ik2(hipJ, [g[0], g[1]], L1, L2, 1);
      knee = r.j; ank = r.e; thA = fwdA(r.ua); shA = fwdA(r.la);
      footA = tg[2] || 0;
    } else {
      const hA = p['hip' + side] || 0, kn = p['kn' + side] || 0;
      thA = hA; knee = add(hipJ, scl(dirF(hA), L1));
      shA = hA - kn; ank = add(knee, scl(dirF(shA), L2));
      footA = p['ank' + side] || 0;
    }
    return { knee, ank, thA, shA, footA };
  };
  const arm = (side) => {
    const tg = f.ik && f.ik[side === 'N' ? 'hN' : 'hF'];
    let elb, wr, upA, foA, haA;
    if (tg) {
      const g = w2l(tg);
      const r = ik2(shoulder, g, BL.up, BL.fo, -1);
      elb = r.j; wr = r.e; upA = fwdA(r.ua); foA = fwdA(r.la);
      haA = foA + (p['wr' + side] || 0);
    } else {
      upA = (p['sh' + side] || 0) - T; elb = add(shoulder, scl(dirF(upA), BL.up));
      foA = upA + (p['el' + side] || 0); wr = add(elb, scl(dirF(foA), BL.fo));
      haA = foA + (p['wr' + side] || 0);
    }
    return { elb, wr, upA, foA, haA };
  };
  const LN = leg('N'), LF = leg('F'), AN = arm('N'), AF = arm('F');
  const neckA = T + (p.neck || 0), headA = neckA + (p.head || 0);
  const neckT = add(neckB, rot([0, -BL.neck], neckA));
  const J = { pelvis: [0, 0], neckB, neckT, shoulder, hip: hipJ, LN, LF, AN, AF, T, headA };
  if (f.onJoints) f.onJoints(J, M);

  // ekran sınır kutusu
  const pts = [[0, 0], neckT, LN.ank, LF.ank, AN.wr, AF.wr, LN.knee, LF.knee];
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const q of pts) { const r = M.transformPoint(new DOMPoint(q[0], q[1])); x0 = Math.min(x0, r.x); x1 = Math.max(x1, r.x); y0 = Math.min(y0, r.y); y1 = Math.max(y1, r.y); }
  const sc = Math.hypot(M.a, M.b), mg = (f.margin || 34) * sc;
  // çizgi kalınlığı: figürün ekrandaki ölçeği (birim başına piksel) 8,2'yi aşınca çizgi ölçeğin karekökü kadar büyür (yakın plan çizgi filme dönmesin)
  const LWK = f.lineK ?? (() => { const q = sc / RS; return q > 8.2 ? Math.sqrt(8.2 / q) : 1; })();
  const TW = ctx.canvas.width, TH = ctx.canvas.height;
  x0 = Math.max(0, Math.floor(x0 - mg)); y0 = Math.max(0, Math.floor(y0 - mg)); x1 = Math.min(TW, Math.ceil(x1 + mg)); y1 = Math.min(TH, Math.ceil(y1 + mg));
  if (x1 <= x0 || y1 <= y0) return J;
  const bw = x1 - x0, bh = y1 - y0;
  const cv = figCanvases(TW, TH);
  const cutW = (f.cutW || .55) * LWK;
  for (const pass of ['sil', 'fig']) {
    const g = cv[pass].getContext('2d');
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.clearRect(x0, y0, bw, bh);
    g.setTransform(M);
    g.lineJoin = 'round'; g.lineCap = 'round';
    const G = {
      g, pass, sty, s, LWK,
      // dolu parça: önce çevresine kesik (arka parçalardan ayırmak için), sonra dolgu
      part(path, o = {}) {
        if (pass === 'fig' && o.cut !== false) { g.save(); g.globalCompositeOperation = 'destination-out'; g.lineWidth = o.cutW ? o.cutW * LWK : cutW; g.beginPath(); path(g); g.stroke(); g.restore(); }
        g.fillStyle = pass === 'sil' ? '#000' : (o.fill || sty.fill);
        g.beginPath(); path(g); g.fill();
        if (pass === 'fig' && o.outline) { g.strokeStyle = o.outline; g.lineWidth = (o.olW || .35) * LWK; g.beginPath(); path(g); g.stroke(); }
      },
      // kazıma çizgisi (alttaki kil rengini açığa çıkarır)
      cut(path, w = .42, fillToo = false) {
        if (pass !== 'fig') return;
        g.save(); g.globalCompositeOperation = 'destination-out'; g.lineWidth = w * LWK;
        g.beginPath(); path(g); fillToo ? g.fill() : g.stroke(); g.restore();
      },
      // boyalı çizgi / dolgu (beyaz ten üstüne çizgi, kırmızı süs vb.)
      paint(path, col, w = 0, fill = true) {
        if (pass !== 'fig') { if (fill && w === 0) { g.fillStyle = '#000'; g.beginPath(); path(g); g.fill(); } return; }
        g.beginPath(); path(g);
        if (fill) { g.fillStyle = col; g.fill(); } else { g.strokeStyle = col; g.lineWidth = w * LWK; g.stroke(); }
      },
      at(pos, ang, fn) { g.save(); g.translate(pos[0], pos[1]); g.rotate(ang); fn(); g.restore(); },
    };
    drawBody(G, f, J, tor, tP);
  }
  // birleştir: önce siluet kazıma rengiyle, sonra figür
  const sg = cv.sil.getContext('2d');
  sg.setTransform(1, 0, 0, 1, 0, 0);
  sg.globalCompositeOperation = 'source-in'; sg.fillStyle = f.cutCol || sty.cut; sg.fillRect(x0, y0, bw, bh);
  sg.globalCompositeOperation = 'source-over';
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalAlpha = (f.alpha ?? 1) * ctx.globalAlpha;
  if (f.shadowBlur) { ctx.shadowColor = f.shadowCol || 'rgba(0,0,0,.5)'; ctx.shadowBlur = f.shadowBlur; }
  // beyaz zemin figürleri: ekranda sabit kalınlıkta sepya dış kontur (sty.contourPx); telefonda kâğıtta kaybolmasınlar
  const stR = f.stripe ? f.stripe * sc * LWK : (sty.contourPx && f.contour !== false ? sty.contourPx * RS : 0);
  if (stR) { const r = stR; for (let k = 0; k < 12; k++) { const a = k * TAU / 12; ctx.drawImage(cv.sil, x0, y0, bw, bh, x0 + Math.cos(a) * r, y0 + Math.sin(a) * r, bw, bh); } }
  ctx.drawImage(cv.sil, x0, y0, bw, bh, x0, y0, bw, bh);
  ctx.shadowBlur = 0;
  ctx.drawImage(cv.fig, x0, y0, bw, bh, x0, y0, bw, bh);
  ctx.restore();
  return J;
}

function drawBody(G, f, J, tor, tP) {
  const lk = f.lk || {}, p = f.p || {}, sty = G.sty, g = G.g;
  const skin = lk.fem ? { fill: sty.white, outline: sty.line, olW: .3, cut: false } : {};
  const skinCut = lk.fem ? {} : {};
  const lineCol = sty.line;
  const thin = lk.fem ? .86 : (lk.thin || 1);
  // ince çizgi: siyah tende kazıma, beyaz tende boyalı çizgi
  const det = (path, w = .4) => lk.fem ? G.paint(path, lineCol, w * .8, false) : G.cut(path, w);

  // bir uzvun parçalarını birleşik çiz: önce hepsinin dış hattını kes, sonra hepsini doldur
  const limb = (shapes, o) => {
    // eklem diskleri (4. öğe true) kazıma/dış hat almaz: yalnız dolgu, raptiye gibi halka görünmez
    if (G.pass === 'fig' && o.cut !== false) for (const [pos, ang, path, nc] of shapes) if (!nc) G.at(pos, ang, () => G.cut(path, o.cutW || .55));
    if (o.outline) {
      // dış hat önce, dolgular sonra: parçaların birleştiği yerde iç çizgi (dikiş) görünmez
      if (G.pass === 'fig') for (const [pos, ang, path, nc] of shapes) if (!nc) G.at(pos, ang, () => { g.strokeStyle = o.outline; g.lineWidth = (o.olW || .35) * 2 * (G.LWK || 1); g.beginPath(); path(g); g.stroke(); });
      for (const [pos, ang, path] of shapes) G.at(pos, ang, () => G.part(path, { ...o, cut: false, outline: null }));
    } else for (const [pos, ang, path] of shapes) G.at(pos, ang, () => G.part(path, { ...o, cut: false }));
  };
  const drawLeg = (L, near) => {
    const shapes = [
      [L.knee, -L.shA, c => spline(c, limbPts(PROF.shin, BL.sh, thin))],
      [L.ank, -L.footA, c => spline(c, FOOT.map(q => [q[0] * (lk.fem ? .9 : 1), q[1]]))],
      [J.hip, -L.thA, c => spline(c, limbPts(PROF.thigh, BL.th, thin))],
      [L.knee, -L.shA, c => c.ellipse(.35, .5, 3.6 * thin, 3.35 * thin, 0, 0, TAU), true], // diz eklemi: uyluk-baldır birleşiminde çentik kalmaz, diz kapağı öne çıkar
    ];
    limb(shapes, lk.fem ? skin : {});
    if (!lk.fem) {
      // diz kapağı ve baldır kası kazıması
      G.at(L.knee, -L.shA, () => {
        det(c => { c.moveTo(1.6, -1.6); c.quadraticCurveTo(3.0, .2, 1.8, 2.0); });
        det(c => { c.moveTo(-3.6, 3.2); c.quadraticCurveTo(-1.6, 7.5, -2.6, 12.0); });
      });
      // ayak bileği
      G.at(L.ank, -L.footA, () => { det(c => c.arc(0, -.2, .7, PI * .15, PI * 1.05), .26); det(c => { c.moveTo(8.2, 1.2); c.lineTo(10.2, 1.9); }, .22); });
      // ayak prangası: bileğin üstünde siyah demir bant (Aiskhylos: bacaklar da bağlanır)
      if (lk.legIrons) G.at(L.ank, -L.shA, () => { G.part(c => c.rect(-3.1, -3.4, 6.2, 2.8), { fill: C.ink, cutW: .3 }); G.paint(c => { c.moveTo(-2.9, -2.0); c.lineTo(2.9, -2.0); }, PC.clayR, .3, false); });
      if (lk.greaves) G.at(L.knee, -L.shA, () => { G.part(c => spline(c, [[3.7, .5], [3.6, 6], [3.2, 14], [2.4, 19.5], [-2.4, 19.5], [-4.6, 9], [-4.4, 1.5]]), { fill: sty.fill, cutW: .45 }); det(c => { c.moveTo(-1.6, 4); c.quadraticCurveTo(.4, 9, -.6, 16); }, .3); });
      if (lk.wingedFeet) G.at(L.ank, -L.footA, () => bootWing(G, f.p && f.p.flap));
    }
  };
  const drawArm = (A, near) => {
    const hs = p['hand' + (near ? 'N' : 'F')] || 'open';
    const shapes = [
      [A.wr, -A.haA, c => spline(c, HAND[hs] || HAND.open)],
      [A.elb, -A.foA, c => spline(c, limbPts(PROF.fo, BL.fo, thin))],
      [J.shoulder, -A.upA, c => spline(c, limbPts(PROF.up, BL.up, thin)), near && lk.rf],
      [A.elb, 0, c => c.arc(0, 0, 2.45 * thin, 0, TAU), true], // dirsek eklemi
    ];
    if (hs === 'open' || hs === 'flat' || hs === 'press') shapes.unshift([A.wr, -A.haA, c => spline(c, THUMB)]);
    limb(shapes, lk.fem ? skin : {});
    if (near && !lk.fem && lk.rf) G.at(J.shoulder, -A.upA, () => G.part(c => c.ellipse(0, .2, 4.2, 4.0, 0, 0, TAU), { cut: false }));
    G.at(A.wr, -A.haA, () => {
      if (!lk.fem && hs === 'fist') det(c => { c.moveTo(1.6, 2.4); c.lineTo(-.6, 2.6); c.moveTo(1.8, 3.6); c.lineTo(-.4, 3.8); }, .3);
      if (!lk.fem && (hs === 'open' || hs === 'flat')) det(c => { c.moveTo(1.4, 3.2); c.lineTo(.2, 6.4); c.moveTo(.2, 3.0); c.lineTo(-.7, 6.2); }, .26);
      if (!lk.fem && hs === 'press') det(c => { c.moveTo(.9, 3.4); c.lineTo(.6, 6.0); }, .24);
      if (lk.fem && (hs === 'open' || hs === 'flat')) G.paint(c => { c.moveTo(1.4, 3.2); c.lineTo(.2, 6.4); }, sty.line, .2, false);
    });
    if (!lk.fem && near && lk.rf) {
      // kesiksiz üst kolun dış hatları (dirseğe doğru) ve deltoid kavisi: omuz zırh levhası gibi okunmasın
      G.at(J.shoulder, -A.upA, () => { det(c => { c.moveTo(3.4, BL.up * .35); c.quadraticCurveTo(3.3, BL.up * .7, 2.6, BL.up); c.moveTo(-3.2, BL.up * .4); c.quadraticCurveTo(-3.0, BL.up * .72, -2.5, BL.up); }, .36);
        det(c => { c.moveTo(-3.4, -.5); c.quadraticCurveTo(1.5, -1.6, 3.6, 3.2); c.quadraticCurveTo(2.0, 6.5, -.6, 7.2); }, .3); });
    }
    if (!lk.fem && near) {
      G.at(A.elb, -A.foA, () => det(c => { c.moveTo(-2.2, -.6); c.quadraticCurveTo(-.2, 1.4, 1.6, .2); }, .33));
      if (!lk.rf) G.at(J.shoulder, -A.upA, () => det(c => { c.moveTo(-3.2, 1.5); c.quadraticCurveTo(.4, 4.6, 3.8, 2.2); }, .33));
    }
    const hold = f.hold && f.hold[near ? 'N' : 'F'];
    if (hold) G.at(A.wr, -A.haA, () => { G.handA = A.haA; hold(G); });
  };

  // arka plan katmanları: pelerin/kanat
  if (lk.wings) G.at(J.shoulder, J.T, () => bigWing(G, lk.wings, p.wingF ?? .6, p.wingSpread ?? .5));
  if (lk.cape) G.at(J.neckB, J.T, () => G.part(c => spline(c, [[-2, -1], [-8.5, 4], [-12, 18], [-10, 30], [-4, 28], [-3.5, 14], [-.5, 6]]), {}));
  drawArm(J.AF, false);
  drawLeg(J.LF, false);
  // gövde
  G.at([0, 0], J.T, () => {
    G.part(c => spline(c, tor.map(q => [q[0] * (1 + (p.breath || 0) * .025), q[1]])), lk.fem ? { ...skin, outline: lk.robe ? null : lineCol } : {});
    // çıplak erkek gövdesinde kırmızı figür anatomi çizgileri: göğüs, karın kasları, göbek, kasık
    if (lk.anat && !lk.fem) {
      const b = 1 + (p.breath || 0) * .025, X = x => x * b;
      if (lk.flatChest) det(c => { c.moveTo(X(3.0), -21.2); c.quadraticCurveTo(X(6.0), -18.6, X(8.7), -20.4); }, .36);
      else det(c => { c.moveTo(X(2.4), -26.6); c.quadraticCurveTo(X(6.4), -19.6, X(9.2), -20.6); }, .36);
      const dil = (path, w = .24) => sty.dilute ? G.paint(path, sty.dilute, w, false) : det(path, w);
      det(c => { c.moveTo(X(6.2), -17.6); c.quadraticCurveTo(X(5.5), -12, X(6.0), -7.6); }, .3);
      dil(c => { c.moveTo(X(3.6), -14.6); c.quadraticCurveTo(X(5.2), -14.1, X(6.5), -14.8); c.moveTo(X(3.8), -11.0); c.quadraticCurveTo(X(5.2), -10.5, X(6.3), -11.2); });
      dil(c => { c.moveTo(X(1.4), -19.4); c.lineTo(X(3.0), -18.4); c.moveTo(X(1.2), -16.8); c.lineTo(X(2.9), -16.0); }, .22);
      if (lk.flatChest) dil(c => { c.moveTo(X(2.6), -28.4); c.quadraticCurveTo(X(5.2), -27.6, X(7.4), -28.6); }, .24);
      det(c => c.arc(X(5.0), -6.9, .45, 0, TAU), .22);
      det(c => { c.moveTo(X(5.6), -4.6); c.quadraticCurveTo(X(3.0), -1.6, X(.6), .4); }, .3);
    }
  });
  // boyun
  G.at(J.neckB, J.headA - (p.head || 0), () => G.part(c => spline(c, [[2.8, .6], [2.6, -5.6], [-2.2, -5.4], [-2.4, .8]]), lk.fem ? skin : { cut: false }));
  drawLeg(J.LN, true);
  drawGarment(G, f, J, tP, det);
  drawHead(G, f, J, det);
  drawArm(J.AN, true);
  if (f.extra) f.extra(G, J);
}

// Giysiler
function drawGarment(G, f, J, tP, det) {
  const lk = f.lk || {}, p = f.p || {}, sty = G.sty;
  const gm = lk.garment;
  if (!gm) return;
  const kneeN = J.LN.knee, kneeF = J.LF.knee;
  const hipPt = (L, t) => add(J.hip, scl(dirF(L.thA), BL.th * t));
  if (gm === 'short' || gm === 'loin') {
    const tt = gm === 'short' ? .55 : .3;
    const a = hipPt(J.LN, tt), b = hipPt(J.LF, tt);
    const fr = a[0] > b[0] ? a : b, bk = a[0] > b[0] ? b : a;
    const top = gm === 'short' ? -27.5 : -6;
    const pts = gm === 'short'
      ? [tP([3.6, -31.0]), tP([9.9, -24.2]), tP([7.0, -15.0]), tP([7.6, -9]), add(fr, [6.2, 1.2]), add(lerp2(fr, bk, .5), [0, 2.4]), add(bk, [-6.4, .8]), tP([-8.8, -5]), tP([-7.0, -15]), tP([-7.8, -24]), tP([-3.0, -31.2])]
      : [tP([7.0, -8]), add(fr, [6.0, 1]), add(lerp2(fr, bk, .5), [0, 2]), add(bk, [-6.2, .6]), tP([-8.6, -6])];
    G.part(c => spline(c, pts, true, .9), {});
    // kemer (kırmızı) ve kıvrımlar
    if (gm === 'short') G.paint(c => { c.moveTo(...tP([7.2, -14.6])); c.lineTo(...tP([-6.6, -14.8])); }, sty.red, 1.5, false);
    else G.paint(c => { c.moveTo(...tP([7.0, -6.6])); c.lineTo(...tP([-8.4, -6.8])); }, sty.red, 1.3, false); // peştamal: kemer bel hizasında
    for (let i = 0; i < 5; i++) {
      const u = (i + .5) / 5;
      const st = tP([lerp(-6, 6.4, u), gm === 'short' ? -13.4 : -5.6]);
      const en = add(lerp2(bk, fr, u), [lerp(-5, 5, u), 0]);
      det(c => { c.moveTo(st[0], st[1]); c.quadraticCurveTo(lerp(st[0], en[0], .5) + .6, lerp(st[1], en[1], .5), en[0], en[1]); }, .32);
    }
    if (gm === 'short') {
      det(c => { const q = tP([3.4, -30.6]), r = tP([-2.6, -30.2]); c.moveTo(q[0], q[1]); c.quadraticCurveTo(...tP([.6, -27.4]), r[0], r[1]); }, .4);
      // nokta deseni
      for (let i = 0; i < 6; i++) { const q = tP([lerp(-4, 6, (i * .37) % 1), lerp(-26, -17, (i * .61) % 1)]); G.cut(c => { c.arc(q[0], q[1], .55, 0, TAU); }, .3); }
      if (lk.torn) det(c => { const q = add(fr, [5, 1]); c.moveTo(q[0], q[1]); c.lineTo(q[0] - 2, q[1] - 3); c.lineTo(q[0] - 3.5, q[1] + .5); }, .35);
    }
  } else if (gm === 'hipwrap') {
    // kalçaya sarılı kısa himation: bel rulosu, etek ucu öndeki kalçadan arkadaki dize çapraz iner;
    // kıvrımlar bütün bel boyunca hafif S kavisle iner (arp teli gibi tek noktada birleşmez)
    const a = hipPt(J.LN, .22), b = hipPt(J.LF, .22), c2 = hipPt(J.LN, .78), d2 = hipPt(J.LF, .78);
    const frHi = a[0] > b[0] ? a : b, bkLo = a[0] > b[0] ? d2 : c2;
    const wF = tP([7.6, -8.2]), wB = tP([-7.4, -9.4]), wM = tP([-.4, -9.9]);
    const LB = a[0] > b[0] ? J.LF : J.LN, pr = [-Math.cos(LB.thA), Math.sin(LB.thA)], bt = u => add(hipPt(LB, u), scl(pr, 6.3 - u * 1.6));
    // rüzgâr arka etek ucunu dalgalandırır (orta nokta yarı genlikle, faz farkıyla)
    const wdG = p.wind || 0, ftG = window.FIG_T || 0;
    const hemA = add(frHi, [6.0, .8]), hemB = add(add(bkLo, [-6.2, .6]), [-wdG * (1 + .5 * Math.sin(ftG * 3.4)), .4 * wdG * Math.sin(ftG * 2.7 + 1)]);
    const hemM = add(lerp2(hemA, hemB, .5).map((v, i) => v + (i ? 1.4 : .6)), [-.5 * wdG * (1 + .5 * Math.sin(ftG * 3.4 - .6)), .2 * wdG * Math.sin(ftG * 2.7 + .4)]);
    const pts = [wF, tP([7.9, -6.4]), hemA, hemM, hemB, bt(.5), bt(.22), tP([-8.9, -2.6]), wB, wM];
    G.part(c => spline(c, pts, true, .75), {});
    // bel rulosu: iki paralel çizgi ve kısa çapraz bükülmeler
    det(c => { c.moveTo(...wF); c.quadraticCurveTo(...wM.map((v, i) => v + (i ? 1.1 : 0)), ...wB); }, .3);
    det(c => { const o = [0, 1.2]; c.moveTo(...add(wF, o)); c.quadraticCurveTo(...add(wM, [0, 2.3]), ...add(wB, o)); }, .26);
    for (let i = 0; i < 4; i++) { const q = lerp2(wF, wB, (i + .5) / 4); det(c => { c.moveTo(q[0] - .5, q[1] + .3); c.lineTo(q[0] + .4, q[1] + 1.4); }, .22); }
    const dil = (path, w) => sty.dilute ? G.paint(path, sty.dilute, w, false) : det(path, w);
    for (let i = 0; i < 7; i++) {
      const u = i / 6, st = add(lerp2(wF, wB, u), [0, 1.6]), en = lerp2(hemA, hemB, (i + .5) / 7);
      const mid = lerp2(st, en, .5), cp = [mid[0] + (i % 2 ? 1.2 : -1.2), mid[1] + .8];
      (i % 2 ? dil : det)(c => { c.moveTo(...st); c.quadraticCurveTo(cp[0], cp[1], en[0], en[1] - .8); }, i % 2 ? .22 : .3);
    }
    // etek ucu bordürü (kenarda) ve nokta motif
    G.paint(c => { c.moveTo(...hemA); c.quadraticCurveTo(...hemM, ...hemB); }, sty.line, 1.1, false);
    for (let i = 0; i < 5; i++) { const q = lerp2(hemA, hemB, (i + .5) / 5); G.paint(c => c.arc(q[0], q[1] - 2.4 + Math.sin((i + .5) / 5 * PI) * 1.2, .42, 0, TAU), sty.line); }
  } else if (gm === 'coat') {
    const kn = kneeN[0] > kneeF[0] ? kneeN : kneeF, kb = kneeN[0] > kneeF[0] ? kneeF : kneeN;
    const pts = [tP([3.4, -31.4]), tP([9.8, -24]), tP([8.0, -14]), tP([7.6, -4]), add(kn, [4.8, -1.5]), add(lerp2(kn, kb, .5), [0, .5]), add(kb, [-5.4, -1.5]), tP([-8.8, -4]), tP([-7.6, -15]), tP([-8.0, -24]), tP([-3.0, -31.4])];
    G.part(c => spline(c, pts, true, .85), {});
    det(c => { c.moveTo(...tP([2.8, -30.6])); c.lineTo(...tP([6.2, -21])); c.lineTo(...tP([5.6, -2])); }, .36);
    det(c => { c.moveTo(...tP([2.8, -30.6])); c.lineTo(...tP([7.4, -27])); c.lineTo(...tP([6.6, -22.4])); }, .3);
    for (const yy of [-17, -11]) G.cut(c => { const q = tP([6.4, yy]); c.arc(q[0], q[1], .5, 0, TAU); }, .3, true);
    det(c => { c.moveTo(...tP([-1, -12])); c.lineTo(...tP([4, -12.6])); }, .3);
  } else if (gm === 'robe') {
    const aN = J.LN.ank, aF = J.LF.ank;
    const fr = aN[0] > aF[0] ? aN : aF, bk = aN[0] > aF[0] ? aF : aN;
    const kneeFr = kneeN[0] > kneeF[0] ? kneeN : kneeF, kneeBk = kneeN[0] > kneeF[0] ? kneeF : kneeN;
    const hem = Math.max(fr[1], bk[1]) - (lk.fem ? -0.6 : 1.2);
    // adım açılınca etek yelken gibi şişmesin: etek ucu ve diz hizası kalçadan belli bir genişliği aşmaz (bacak eteğin altından çıkar)
    const hF = Math.min(fr[0] + 6.6, 12.5), hB = Math.max(bk[0] - 5.2, -11.5);
    const kF = [Math.min(kneeFr[0] + 5.2, 12.8), kneeFr[1]], kB = [Math.max(kneeBk[0] - 6.2, -12), kneeBk[1]];
    const pts = [tP([3.6, -31.2]), tP([lk.fem ? 9.4 : 10.2, -24]), tP([7.4, -15]), tP([7.4, -6]), kF, [hF, hem], [lerp(hF, hB, .5), hem + .8], [hB, hem], kB, tP([-9.0, -4]), tP([-7.2, -15]), tP([-8.2, -24]), tP([-3.0, -31.2])];
    G.part(c => spline(c, pts, true, .85), lk.robeCol ? { fill: lk.robeCol } : {});
    // etek bordürü: kırmızı bant (etek poligonunun alt kenarından) + meander noktaları
    const hb = c => { c.moveTo(hB + 1.2, hem - 1.6); c.lineTo(hF - 1.2, hem - 1.6); };
    G.paint(hb, sty.red, 1.6, false);
    for (let i = 0; i < 7; i++) {
      const u = (i + .5) / 7, st = tP([lerp(-6.6, 7, u), -14]);
      const en = [lerp(hB + 1.2, hF - 1.1, u), hem - 2.8];
      det(c => { c.moveTo(st[0], st[1]); c.bezierCurveTo(st[0] + 1, lerp(st[1], en[1], .4), en[0] - 1, lerp(st[1], en[1], .7), en[0], en[1]); }, .3);
    }
    G.paint(c => { c.moveTo(...tP([7.4, -15])); c.lineTo(...tP([-7, -15.2])); }, sty.red, 1.2, false);
    if (lk.robeDots) for (let i = 0; i < 14; i++) {
      const u = hash(i * 3.1), v = hash(i * 7.7);
      const qy = lerp(kneeFr[1] - 2, hem - 6.5, v), w_ = clamp((qy - (kneeFr[1] - 2)) / Math.max(1, hem - kneeFr[1])); // etek konturu içinde (dizden etek ucuna genişler)
      const q = [lerp(lerp(kB[0], hB, w_) + 2.8, lerp(kF[0], hF, w_) - 2.8, u), qy];
      G.paint(c => c.arc(q[0], q[1], .55, 0, TAU), sty.red);
    }
    if (lk.himation) { // omuz şalı (çapraz)
      G.part(c => spline(c, [tP([4.8, -29]), tP([10.4, -22]), tP([8.4, -12]), tP([-8.6, -11]), tP([-8.6, -22]), tP([-4.8, -30.4])], true, .9), { fill: lk.himCol || sty.fill });
      det(c => { c.moveTo(...tP([7, -26])); c.lineTo(...tP([-6, -14])); }, .32);
      det(c => { c.moveTo(...tP([8.6, -21])); c.lineTo(...tP([-3, -12])); }, .32);
      G.paint(c => { c.moveTo(...tP([8.6, -12.4])); c.lineTo(...tP([-8.4, -11.4])); }, sty.red, 1.1, false);
    }
  }
}
function lerp2(a, b, t) { return [lerp(a[0], b[0], t), lerp(a[1], b[1], t)]; }

function drawHead(G, f, J, det) {
  const lk = f.lk || {}, p = f.p || {}, sty = G.sty;
  G.at(J.neckT, J.headA, () => {
    const g = G.g;
    // geriye bakış: gövde bir yöne giderken baş ters yöne döner (vazo uylaşımı; "bile bile" geriye bakan Titan)
    if (p.headBack) { g.scale(-1, 1); g.rotate(p.headBackA ?? .15); }
    if (lk.fem && lk.headgear !== 'helmet') {
      G.part(c => spline(c, headOutline(lk)), { fill: sty.white, outline: sty.line, olW: .3, cut: false });
      G.part(c => spline(c, HAIR_F), { cut: false });
      G.paint(c => { c.moveTo(4.8, -11.2); c.quadraticCurveTo(0, -13.6, -6.4, -11.4); }, sty.red, 1.0, false);
      if (lk.crown) { G.part(c => { c.moveTo(4.6, -11.8); c.lineTo(4.2, -15.6); c.lineTo(2.2, -13.4); c.lineTo(0, -16.6); c.lineTo(-2.2, -13.6); c.lineTo(-4.4, -16.0); c.lineTo(-5.6, -11.6); c.quadraticCurveTo(0, -14, 4.6, -11.8); }, { fill: C.gold, outline: sty.line, olW: .25, cut: false }); }
      // göz (siyah çizgi), kaş
      const bl = clamp(1 - (p.blink || 0));
      G.paint(c => { c.moveTo(2.4, -7.0); c.quadraticCurveTo(3.6, -7.0 - .75 * bl, 4.8, -7.25); c.quadraticCurveTo(3.6, -6.4, 2.4, -7.0); }, sty.line, .28, false);
      if (bl > .3) G.paint(c => c.arc(3.9, -7.05, .42, 0, TAU), sty.line);
      G.paint(c => { c.moveTo(2.6, -8.3); c.quadraticCurveTo(4.0, -9.0, 5.4, -8.5); }, sty.line, .28, false);
      const sm = p.smile || 0;
      G.paint(c => { c.moveTo(5.7, -3.95); c.quadraticCurveTo(5.1, -3.8 - sm * .2, 4.7, -3.9 - sm * .45); }, sty.line, .25, false);
      if (lk.earring) G.paint(c => c.arc(-1.2, -3.2, .6, 0, TAU), sty.red);
      return;
    }
    const hb = lk.headgear;
    if (hb === 'helmet') {
      if (lk.fem) G.part(c => spline(c, [[-5.6, -4], [-7.6, -1.2], [-8.6, 3.6], [-8.0, 8.2], [-6.2, 9.0], [-5.4, 5.0], [-5.0, .6]]), {});
      G.part(c => spline(c, headOutline({ ...lk, fem: false, hair: 'short' })), {});
      G.part(c => spline(c, HELMET), {});
      helmetCrest(G, det, sty);
      // göz deliği
      G.cut(c => { c.moveTo(2.0, -6.4); c.quadraticCurveTo(4.6, -8.4, 6.2, -6.6); c.quadraticCurveTo(4.0, -6.0, 2.0, -6.4); }, .5, true);
      G.part(c => { c.moveTo(3.3, -6.95); c.arc(3.7, -6.95, .5, 0, TAU); }, { cut: false });
      det(c => { c.moveTo(-6.2, -11.6); c.quadraticCurveTo(-.5, -10, 5.6, -10.4); }, .4);
      return;
    }
    G.part(c => spline(c, headOutline(lk)), {});
    const rf = lk.rf && sty !== STY.black;
    if (rf) {
      // saç ve sakal siyah sır; çevresinde ince ayrılmış kil şerit (zeminden ayrılsın)
      // rüzgâr: ensedeki bukleler ve sakal ucu geriye savrulur, uca doğru gecikmeyle dalgalanır
      const wd = p.wind || 0, ft = window.FIG_T || 0;
      const blow = (P, y0, k) => wd ? P.map(([x, y], i) => { const u = clamp((y - y0) / 8); return [x - wd * k * u + .9 * wd * u * Math.sin(ft * 3.1 + i * .7) + .35 * wd * u * Math.sin(ft * 5.3 + i * 1.3), y - wd * .2 * u + .25 * wd * u * Math.sin(ft * 2.2 + i)]; }) : P;
      const jut = p.beardJut ?? lk.beardJut ?? 0, BRD = jut ? BEARD_RF.map(([x, y]) => [x + jut * clamp((y + 1) / 6.9), y]) : BEARD_RF;
      for (const P of [blow(lk.hair === 'nape' ? HAIR_RF_N : HAIR_RF, -4, 1.1), lk.beard ? blow(BRD, 0, .7) : null]) if (P) {
        G.paint(c => spline(c, P, true, .9), sty.fill, .55, false);
        G.paint(c => spline(c, P, true, .9), sty.line);
      }
      // boncuklu ense saçı (arkaik): siyah saçın üstünde kil noktalar sıra sıra
      if (lk.beadHair) for (let i = 0; i < 3; i++) { const x = -6.8 + i * 1.3, P0 = [x + .5, -6.4], P1 = [x - 1.4, -3.4], P2 = [x + 1.4, -.8], P3 = [x - .2, 1.2];
        for (let k = 0; k < 7; k++) { const u = (k + .5) / 7, v = 1 - u, bx = v * v * v * P0[0] + 3 * v * v * u * P1[0] + 3 * v * u * u * P2[0] + u * u * u * P3[0], by = v * v * v * P0[1] + 3 * v * v * u * P1[1] + 3 * v * u * u * P2[1] + u * u * u * P3[1];
          G.paint(c => c.arc(bx, by, .3, 0, TAU), sty.fill); } }
      // iç bukleler: kil rengi ince S eğrileri
      const hl = lk.hair === 'nape' ? 1.2 : 2.6;
      for (let i = 0; i < 3; i++) G.paint(c => { const x = -6.8 + i * 1.3, sw = wd * 1.2 + .3 * wd * Math.sin(ft * 3.1 + i); c.moveTo(x + .5, -6.4); c.bezierCurveTo(x - 1.4, -3.4, x + 1.4, -.8, x - .2 - sw, hl); }, sty.fill, .2, false);
      if (lk.beard) for (let i = 0; i < 3; i++) G.paint(c => { const u = i / 2, x0 = lerp(1.0, 4.6, u), y0 = -2.2, x1 = lerp(2.6, 6.0, u) + jut * .5 - wd * .5 * u, y1 = lerp(1.6, 5.0, u); c.moveTo(x0, y0); c.bezierCurveTo(x0 + 1.2, lerp(y0, y1, .33), x1 - 1.0, lerp(y0, y1, .66), x1, y1); }, sty.fill, .2, false);
      // ağız: bıyık ile sakal arasında kil çizgi
      const mo = p.mouthOpen || 0;
      G.paint(c => { c.moveTo(6.2 + jut * .3, -2.75); c.quadraticCurveTo(5.3, -2.5 - mo * .35, 4.1, -2.95); }, sty.fill, .34 + mo * .25, false);
      // alın bukleleri: saç çizgisi boyunca kabartma noktalar
      for (let i = 0; i < 5; i++) { const x = lerp(5.1, 2.5, i / 4), y = lerp(-9.75, -10.5, i / 4); G.paint(c => c.arc(x, y, .62, 0, TAU), sty.fill); G.paint(c => c.arc(x, y, .4, 0, TAU), sty.line); }
      // bıyık lülesi ve alt dudak
      if (lk.beard) { G.paint(c => { c.moveTo(5.9, -4.35); c.quadraticCurveTo(4.4, -4.0, 3.2, -2.9); c.quadraticCurveTo(4.6, -3.5, 5.9, -3.9); c.closePath(); }, sty.line); G.paint(c => { c.moveTo(5.75, -3.15); c.quadraticCurveTo(5.2, -2.9, 4.7, -3.05); }, sty.fill, .32, false); }
    }
    // göz
    const FW = f.faceW || 1; // yüz çizgisi kalınlık çarpanı (küçük boyutta okunan kapak gibi yakın planlar için)
    const bl = clamp(1 - (p.blink || 0));
    const ey = lk.eyeY ?? -7.0;
    if (lk.whiteEye) {
      G.paint(c => { c.moveTo(2.2, ey); c.quadraticCurveTo(3.5, ey - .9 * bl, 4.9, ey - .2); c.quadraticCurveTo(3.5, ey + .55 * bl, 2.2, ey); }, sty.white);
      if (bl > .3) G.paint(c => c.arc(3.9, ey - .15, .45, 0, TAU), sty.fill);
    } else {
      // gülümsemede alt kapak yükselir (göz hilal olur), göz kenarında kaz ayağı, elmacık çizgisi belirir
      const smE = clamp((p.smile || 0) / 2);
      if (smE > .55) {
        // gülen göz: tek kavis (^), uçlarda kaz ayağı
        det(c => { c.moveTo(2.1, ey + .2); c.quadraticCurveTo(3.5, ey - 1.15, 4.95, ey + .05); }, .42 * FW);
        det(c => { c.moveTo(1.85, ey - .1); c.lineTo(.95, ey - .55); c.moveTo(1.85, ey + .35); c.lineTo(.95, ey + .6); }, .26 * FW);
      } else if (lk.sevEye) {
        // Sert üslup (İÖ 480-450) profil göz: buruna açılan V, bebek açık uçta; kapak yavaşça iner
        det(c => { c.moveTo(1.9, ey - .1); c.lineTo(4.75, ey - .9 * bl - .05); c.moveTo(1.9, ey - .1); c.lineTo(4.55, ey + .42 * bl); }, .36 * FW);
        if (bl > .3) G.cut(c => c.arc(4.0, ey - .22, .46, 0, TAU), .3, true);
      } else {
        const es = lk.eyeS || 1, ex = x => 3.55 + (x - 3.55) * es, eY = y => ey + (y - ey) * es; // lk.eyeS: daha iri göz (karakter ayrımı)
        det(c => { c.moveTo(ex(2.2), eY(ey)); c.quadraticCurveTo(ex(3.5), eY(ey - .9 * bl), ex(4.9), eY(ey - .2)); c.quadraticCurveTo(ex(3.5), eY(ey + .6 * bl), ex(2.2), eY(ey)); }, .36 * Math.sqrt(es));
        if (bl > .3 && !lk.blind) G.cut(c => c.arc(ex(3.75), eY(ey - .12), .5 * es, 0, TAU), .3, true); // lk.blind: açık ama boş göz (bebeksiz)
      }
    }
    // kaş
    const br = (p.brow || 0) + (lk.brow || 0); // lk.brow: karakterin kalıcı kaş açısı (Zeus sert)
    const sc = (p.scowl || 0) + (lk.scowl || 0);
    const by0 = -8.45 - br * .3 - sc * .45, by1 = -8.6 + br * .45 + sc * .75, bf = p.browFlat ?? lk.browFlat ?? 0;
    det(c => { c.moveTo(2.0, by0); c.quadraticCurveTo(3.8, lerp(-9.3 - br * .6 - sc * .05, (by0 + by1) / 2 - .05, bf), 5.6, by1); }, (.34 + sc * .08) * FW * (1 + bf * .25));
    if (sc > .3) det(c => { c.moveTo(5.6, -8.6 + br * .45 + sc * .75); c.lineTo(6.0, -7.5); }, .26 * FW);
    // kulak
    if (!lk.earHidden) det(c => { c.moveTo(-.4, -7.8); c.bezierCurveTo(-2.4, -7.6, -2.4, -4.6, -.6, -4.6); c.moveTo(-1.0, -6.8); c.quadraticCurveTo(-1.6, -6, -1.0, -5.4); }, .32);
    // ağız
    const sm = p.smile || 0;
    if (!rf) { // siyah sakallı kırmızı figürde ağız ve sakal yukarıda boyandı
    // ağız: gülümsedikçe köşe yanağa doğru yükselir ve çizgi kalınlaşır; yanakta gülme çizgisi
    det(c => { c.moveTo(5.75, -3.9); c.quadraticCurveTo(4.9, -3.6 - sm * .1, 4.0 - sm * .15, -4.1 - sm * .55); }, (.3 + clamp(sm / 2) * .14) * FW);
    if (p.mouthOpen) G.cut(c => { c.moveTo(5.8, -3.95); c.quadraticCurveTo(5.0, -3.2 - p.mouthOpen * .6, 4.6, -3.7); c.closePath(); }, .3, true);
    // sakal ve saç kazımaları
    if (lk.beard) {
      det(c => { c.moveTo(-.2, -4.4); c.quadraticCurveTo(2.2, -3.0, 4.6, -3.6); }, .34);
      if (lk.beard === 'full') {
        // sıra sıra kıvırcık bukleler (siyah figür Zeus sakalı)
        for (let r = 0; r < 4; r++) for (let i = 0; i < 4 - (r > 2 ? 1 : 0); i++) {
          const x = lerp(1.6, 6.0, i / 3) - r * .2 + (r % 2) * .5, y = -2.0 + r * 2.4 + i * .5;
          det(c => { c.moveTo(x - .7, y); c.arc(x, y, .7, PI, TAU * .95); }, .24);
        }
      } else {
        const n = lk.beard === 'long' ? 5 : 4;
        for (let i = 0; i < n; i++) {
          const u = i / (n - 1);
          det(c => { c.moveTo(lerp(.6, 4.6, u), lerp(-3.2, -3.4, u)); c.quadraticCurveTo(lerp(1.4, 5.4, u), lerp(-.5, -.8, u), lerp(2.6, 5.2, u) - .3, lerp(1.6, 3.4, u) + (lk.beard === 'long' ? 2 : 0)); }, .26);
        }
      }
      if (lk.old) for (let i = 0; i < 6; i++) G.paint(c => { const u = i / 5; c.moveTo(lerp(1, 5, u), -2.6); c.quadraticCurveTo(lerp(2, 5.6, u), 0, lerp(2.8, 5.1, u), lerp(1.4, 3.2, u)); }, sty.white, .3, false);
    }
    }
    if (lk.hair === 'long' && !rf) for (let i = 0; i < 4; i++) det(c => { const x = -6.6 + i * 1.0; c.moveTo(x + .3, -5.2); c.bezierCurveTo(x - .6, -2, x + .6, 1.5, x - .2, 5.4); }, .26);
    if (hb === 'diadem' || hb === 'wreath' || !hb) {
      // saç bandı / taç
      if (hb === 'diadem') {
        G.paint(c => { c.moveTo(5.2, -11.0); c.quadraticCurveTo(.2, -13.6, -6.4, -10.8); }, sty.red, 1.4, false);
        for (let i = 0; i < 4; i++) G.paint(c => { const u = i / 3, x = lerp(4.2, -4.8, u), y = lerp(-12.0, -11.9, u) - Math.sin(u * PI) * 1.4; c.moveTo(x - .8, y + .2); c.lineTo(x, y - 2.2); c.lineTo(x + .8, y + .2); c.closePath(); }, sty.red);
      } else if (hb === 'wreath') {
        // yaprak çelengi: eklenmiş kırmızı sap ve çift sıra yapraklar (taç bandından ayrı okunur)
        G.paint(c => { c.moveTo(5.0, -11.2); c.quadraticCurveTo(-.2, -13.8, -6.2, -10.4); }, sty.red, .5, false);
        for (let i = 0; i < 9; i++) { const u = i / 8, x = lerp(4.6, -5.8, u), y = lerp(-11.5, -10.6, u) - Math.sin(u * PI) * 2.1;
          for (const sg of [-1, 1]) G.paint(c => c.ellipse(x + sg * .35, y + sg * .55, .42, 1.15, (-.6 + u * 1.2) + sg * .9, 0, TAU), sty.red); }
      } else if (rf) G.paint(c => { c.moveTo(5.0, -11.2); c.quadraticCurveTo(.2, -13.4, -6.0, -10.2); }, sty.red, .9, false);
      else det(c => { c.moveTo(5.0, -11.1); c.quadraticCurveTo(.2, -13.2, -5.8, -10.0); }, .34);
      // alın üstü bukleler
      if (!lk.modern && !rf) for (let i = 0; i < 3; i++) det(c => c.arc(4.8 - i * .9, -10.2 - i * .45, .42, 0, TAU), .24);
      else {
        // modern saç: belirgin saç çizgisi, taranmış saç telleri ve favori
        det(c => { c.moveTo(5.2, -10.2); c.quadraticCurveTo(1.6, -11.6, -1.6, -10.6); c.quadraticCurveTo(-3.8, -9.6, -4.4, -6.6); c.lineTo(-2.6, -5.6); }, .42);
        for (let i = 0; i < 5; i++) det(c => { const u = i / 4; c.moveTo(lerp(4.4, -5.4, u), lerp(-11.6, -10.0, u) - Math.sin(u * PI) * 1.8); c.quadraticCurveTo(lerp(2.6, -6.6, u), lerp(-12.6, -9.0, u) - Math.sin(u * PI) * 1.2, lerp(.6, -6.8, u), lerp(-12.4, -6.6, u)); }, .2);
      }
    }
    if (hb === 'petasos') {
      G.part(c => { c.ellipse(-.6, -12.3, 10.4, 1.7, -.08, 0, TAU); }, {});
      G.part(c => spline(c, [[5, -12.6], [3.6, -16.4], [-1, -17.6], [-5.6, -16], [-6.4, -12.2]]), {});
      wingShape(G, [-4.2, -15.2], -2.6, 6.2);
    }
    if (hb === 'attic') {
      // açık yüzlü Attika miğferi: kafatası başlığı, kısa siper, ense kanadı, kulağı örten yanak siperi; tepelik ayak üstünde
      G.part(c => spline(c, [[6.5, -9.1], [5.7, -10.8], [4.4, -12.7], [1.0, -14.5], [-3.2, -14.3], [-6.4, -12.0], [-7.5, -8.2], [-7.7, -4.6], [-9.2, -2.6], [-6.6, -2.4],
        [-5.0, -4.8], [-2.8, -6.2], [-1.2, -6.0], [-.8, -3.4], [.8, -1.9], [1.7, -3.2], [1.5, -6.6], [2.4, -8.6], [4.6, -9.1]]), {});
      det(c => { c.moveTo(6.0, -9.6); c.quadraticCurveTo(3.4, -9.9, 1.6, -9.2); }, .36);
      det(c => { c.moveTo(-.6, -7.0); c.quadraticCurveTo(.6, -5.0, .6, -3.0); }, .26);
      helmetCrest(G, det, sty);
    }
    if (hb === 'pilos') {
      // pilos: sivri keçe külah (zanaatkâr başlığı); kenarında ince kırmızı bant
      G.part(c => spline(c, [[5.8, -10.2], [3.6, -14.0], [.6, -17.6], [-2.8, -20.2], [-4.4, -17.4], [-6.4, -12.6], [-7.2, -9.6], [-1, -11.0]]), {});
      G.paint(c => { c.moveTo(5.6, -10.4); c.quadraticCurveTo(-1, -12.2, -7.0, -9.8); }, sty.red, .9, false);
      det(c => { c.moveTo(3.0, -13.0); c.quadraticCurveTo(-1, -14.6, -5.4, -12.2); }, .24);
    }
    if (hb === 'hood') G.part(c => spline(c, [[5.8, -10.6], [4.6, -14.2], [.4, -15.6], [-5, -14.6], [-8.4, -10], [-8.8, -3], [-7.6, 3], [-4.2, 4.2], [-3.4, -2], [-1.6, -7], [2.6, -10.4]]), {});
  });
}

// Küçük kanat (Hermes)
// çizme kanadı: bileğe takılı, geriye ve ~30° yukarı açılan üç tüy (siyah, kil kazıma eksen); flap: hafif çırpma
function bootWing(G, flap = 0) {
  const fl = flap ? .12 * Math.sin((window.FIG_T || 0) * 14) * flap : 0;
  G.at([-1.2, -2.2], 0, () => {
    [[PI + .62, 4.8], [PI + .42, 4.1], [PI + .2, 3.3]].forEach(([a, L], i) => {
      const aa = a + fl * (1 + i * .3), dx = Math.cos(aa), dy = Math.sin(aa), nx = -dy, ny = dx, w = .62 - i * .08;
      G.paint(c => { c.moveTo(nx * w * .5, ny * w * .5); c.quadraticCurveTo(dx * L * .55 + nx * w, dy * L * .55 + ny * w, dx * L, dy * L); c.quadraticCurveTo(dx * L * .55 - nx * w, dy * L * .55 - ny * w, -nx * w * .5, -ny * w * .5); c.closePath(); }, C.ink);
      G.paint(c => { c.moveTo(dx * .4, dy * .4); c.lineTo(dx * L * .8, dy * L * .8); }, C.clay, .16, false);
    });
    G.paint(c => c.ellipse(0, 0, 1.1, .7, 0, 0, TAU), C.ink);
  });
}
function wingShape(G, at, a, L) {
  G.at(at, a, () => {
    G.part(c => spline(c, [[0, 0], [-L * .5, -L * .35], [-L, -L * .3], [-L * .75, -L * .05], [-L * 1.05, .1], [-L * .7, .35], [-L * .9, .7], [-L * .3, .5]]), {});
    G.cut(c => { c.moveTo(-L * .2, .05); c.lineTo(-L * .75, -.12); c.moveTo(-L * .25, .3); c.lineTo(-L * .7, .45); }, .25);
  });
}
// Büyük kanatlar (Thanatos): omuzdan geriye/yukarı açılan iki kanat. flap faz, spread 0 kapalı .. 1 açık
function bigWing(G, kind, flap, spread) {
  const sty = G.sty;
  const open = clamp(spread), fl = Math.sin(flap * TAU);
  const one = (A, Lw, far) => G.at([-1, 0], A, () => {
    G.g.scale(1, -1); // tüyler kanat kolunun arka/alt tarafına sarksın
    // birincil tüyler (kanat ucu, geriye doğru)
    for (let i = 10; i >= 0; i--) {
      const u = i / 10, base = [lerp(Lw * .42, Lw * 1.0, u), lerp(-3, 3, u)];
      const fa = lerp(1.9, .35, u) + (1 - open) * .35;
      const fLen = lerp(22, 40, Math.sin(u * PI * .85 + .2));
      G.at(base, fa, () => G.part(c => spline(c, [[-2, 0], [2, 0], [1.6, fLen * .72], [0, fLen], [-1.6, fLen * .72]]), { cutW: .5 }));
    }
    // örtü tüyleri ve kemik
    G.part(c => spline(c, [[-3, -3], [Lw * .32, -7], [Lw * .7, -4], [Lw * 1.04, 2], [Lw * .82, 10], [Lw * .5, 16], [Lw * .2, 18], [-4, 10]]), {});
    for (let r = 0; r < 3; r++) for (let i = 0; i < 8; i++) {
      const u = i / 7, x = lerp(3, Lw * .9, u), y = lerp(3, 5, u) + r * 4.6;
      G.cut(c => { c.moveTo(x - 2.6, y - 1); c.quadraticCurveTo(x, y + 2.4, x + 2.6, y - 1); }, .3);
    }
    if (!far) G.paint(c => { c.moveTo(0, -2); c.quadraticCurveTo(Lw * .4, -7, Lw * .98, 1); }, sty.red, 1.8, false);
  });
  const Lw = kind === 'huge' ? 44 : 34;
  // uzak kanat daha yukarıda, yakın kanat daha geride/aşağıda
  one(lerp(-1.9, -2.05, open) + fl * .2 * open, Lw * .92, true);
  one(lerp(-2.2, -2.75, open) - fl * .25 * open, Lw, false);
}
