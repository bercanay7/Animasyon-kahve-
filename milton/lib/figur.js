// Figür: eklem noktalarından hacimli, gravür diliyle gölgelenen insan bedeni (Doré'nin akademik çıplakları).
// Uzuv = kemik boyunca yarıçap profiliyle örülen kapsül; gölge = ışık yönüne göre silindir gölgesi (ton), tarama = uzvu saran çizgiler.
// Eklemler dünya koordinatında verilir: J = {hd, nk, shL, shR, elL, elR, wrL, wrR, hpL, hpR, knL, knR, anL, anR}
// L/R figürün kendi sol/sağı. near: 'L' ya da 'R' (kameraya yakın taraf; uzak taraf önce ve daha koyu çizilir).
'use strict';
const FG = (() => {
  const { tx, px, tone, pat, fill } = GR;
  // kemik boyunca kapsül: p0→p1, yarıçap profili rf(f) (f 0..1), uç yuvarlak
  function capsule(p0, p1, rf, n = 14) {
    const dx = p1[0] - p0[0], dy = p1[1] - p0[1], L = Math.hypot(dx, dy) || 1, ux = dx / L, uy = dy / L, nx = -uy, ny = ux;
    const A = [], B = [];
    for (let i = 0; i <= n; i++) {
      const f = i / n, r = rf(f), x = p0[0] + dx * f, y = p0[1] + dy * f;
      A.push([x + nx * r, y + ny * r]); B.push([x - nx * r, y - ny * r]);
    }
    const r0 = rf(0), r1 = rf(1), cap = (c, r, a0) => { const o = []; for (let k = 1; k < 8; k++) { const a = a0 - k / 8 * PI; o.push([c[0] + Math.cos(a) * r, c[1] + Math.sin(a) * r]); } return o; };
    const a1 = Math.atan2(ny, nx), pts = [...A, ...cap(p1, r1, a1), ...B.slice().reverse(), ...cap(p0, r0, a1 + PI)];
    const P = new Path2D(); spline(P, pts, true, .8);
    return { P, ux, uy, nx, ny, L, A, B };
  }
  // silindir gölgesi: ışık (lx, ly) ile uzvun normali arasındaki açıya göre enlemesine gradyan
  // v: {hi, mid, lo, refl} ton değerleri; ışık tarafı → gölge tarafı, en dışta yansıyan ışık
  function cylShade(c, p0, p1, rmax, lit, v) {
    const mx = (p0[0] + p1[0]) / 2, my = (p0[1] + p1[1]) / 2;
    const side = Math.sign(lit[0] * c.nx + lit[1] * c.ny) || 1;
    const ax = c.nx * side, ay = c.ny * side; // ışığa bakan normal
    const g = tx.createLinearGradient(mx + ax * rmax, my + ay * rmax, mx - ax * rmax, my - ay * rmax);
    g.addColorStop(0, tone(v.hi)); g.addColorStop(.18, tone(v.hi)); g.addColorStop(.55, tone(v.mid));
    g.addColorStop(.8, tone(v.lo)); g.addColorStop(1, tone(v.refl ?? v.lo));
    return g;
  }
  // uzvu saran tarama: çizgiler kemiğe dik, enine kavisli (doğrultu gradyanı ile)
  function wrapPat(c, p0, p1, rmax, bend = .22, ph = 0, id = 5) {
    const th = Math.atan2(c.ny, c.nx);
    const mx = (p0[0] + p1[0]) / 2, my = (p0[1] + p1[1]) / 2;
    return GR.patGrad(mx + c.nx * rmax, my + c.ny * rmax, mx - c.nx * rmax, my - c.ny * rmax, [[0, th + bend], [.5, th], [1, th - bend]], ph, id);
  }
  function limb(p0, p1, rf, rmax, lit, v, o = {}) {
    const c = capsule(p0, p1, rf);
    fill(c.P, cylShade(c, p0, p1, rmax, lit, v), { fill: wrapPat(c, p0, p1, rmax, o.bend ?? .25, o.ph || 0, o.id ?? 5) });
    return c.P;
  }
  // kas profilleri (f: 0 proksimal → 1 distal), yarıçap birimi: baş yüksekliği h
  const PROF = {
    upperArm: h => f => h * (.27 + .07 * Math.sin(PI * Math.min(1, f * 1.3)) - .06 * f),
    foreArm: h => f => h * (.235 - .09 * f + .05 * Math.sin(PI * Math.min(1, f * 2))),
    thigh: h => f => h * (.33 - .15 * f + .04 * Math.sin(PI * f)),
    shin: h => f => h * (.2 - .1 * f + .06 * Math.sin(PI * Math.min(1, f * 1.8))),
  };
  // gövde: omuzlar, kalça; göğüs kafesi ve bel. dönüş: Path2D
  function torso(J, h, lit, v, o = {}) {
    const { shL, shR, hpL, hpR, nk } = J;
    const sc = [(shL[0] + shR[0]) / 2, (shL[1] + shR[1]) / 2], hc = [(hpL[0] + hpR[0]) / 2, (hpL[1] + hpR[1]) / 2];
    const up = [sc[0] - hc[0], sc[1] - hc[1]], L = Math.hypot(up[0], up[1]), u = [up[0] / L, up[1] / L], n = [-u[1], u[0]];
    const sw = Math.hypot(shR[0] - shL[0], shR[1] - shL[1]), hw = Math.hypot(hpR[0] - hpL[0], hpR[1] - hpL[1]);
    // yan çizgiler: koltuk altından (kafes) bele (içe) kalçaya
    const at = (base, along, side, wdt) => [base[0] + u[0] * along + n[0] * side * wdt, base[1] + u[1] * along + n[1] * side * wdt];
    const sL = Math.sign((shL[0] - sc[0]) * n[0] + (shL[1] - sc[1]) * n[1]) || -1;
    const P = new Path2D();
    const pts = [
      at(sc, h * .08, sL, sw * .5), at(sc, -L * .18, sL, sw * .47), at(sc, -L * .42, sL, sw * .4 * (o.waist ?? 1)),
      at(hc, L * .2, sL, hw * .5), at(hc, -h * .12, sL, hw * .52),
      at(hc, -h * .12, -sL, hw * .52), at(hc, L * .2, -sL, hw * .5),
      at(sc, -L * .42, -sL, sw * .4 * (o.waist ?? 1)), at(sc, -L * .18, -sL, sw * .47), at(sc, h * .08, -sL, sw * .5),
      at(sc, h * .22, 0, 0),
    ];
    spline(P, pts, true, .9);
    // gölge: gövde enlemesine silindir + göğüs/karın kabartıları
    const side = Math.sign(lit[0] * n[0] + lit[1] * n[1]) || 1;
    const mid = [(sc[0] + hc[0]) / 2, (sc[1] + hc[1]) / 2];
    const g = tx.createLinearGradient(mid[0] + n[0] * side * sw * .55, mid[1] + n[1] * side * sw * .55, mid[0] - n[0] * side * sw * .55, mid[1] - n[1] * side * sw * .55);
    g.addColorStop(0, tone(v.hi)); g.addColorStop(.3, tone(v.hi)); g.addColorStop(.62, tone(v.mid)); g.addColorStop(.86, tone(v.lo)); g.addColorStop(1, tone(v.refl ?? v.lo));
    const thN = Math.atan2(n[1], n[0]);
    fill(P, g, { fill: GR.patGrad(mid[0] + n[0] * sw * .5, mid[1] + n[1] * sw * .5, mid[0] - n[0] * sw * .5, mid[1] - n[1] * sw * .5, [[0, thN + .35], [.5, thN], [1, thN - .35]], o.ph || 0, 5) });
    // kabartılar: göğüs, karın, kaburga (ton katmanına, gövdeye kırpılı)
    tx.save(); tx.clip(P);
    const bump = (cx, cy, rx, ry, a, val, alpha) => {
      const bx = cx + lit[0] * rx * .3, by = cy + lit[1] * ry * .3;
      const rg = tx.createRadialGradient(bx, by, 1, cx, cy, Math.max(rx, ry));
      rg.addColorStop(0, tone(val, alpha)); rg.addColorStop(1, tone(val, 0));
      tx.save(); tx.translate(cx, cy); tx.rotate(a); tx.scale(1, ry / rx); tx.translate(-cx, -cy);
      tx.fillStyle = rg; tx.fillRect(cx - rx, cy - rx, rx * 2, rx * 2); tx.restore();
    };
    const tA = Math.atan2(n[1], n[0]);
    for (const s of [-1, 1]) { // göğüs kasları
      const c = at(sc, -L * .2, s, sw * .22);
      bump(c[0], c[1], sw * .26, sw * .16, tA, v.hi, .55);
      const sh = at(sc, -L * .33, s, sw * .22); bump(sh[0], sh[1], sw * .24, sw * .06, tA, v.lo, .5); // göğüs altı gölgesi
    }
    for (let k = 0; k < 3; k++) for (const s of [-1, 1]) { // karın
      const c = at(sc, -L * (.5 + k * .13), s, sw * .1);
      bump(c[0], c[1], sw * .1, sw * .075, tA, v.hi, .35);
    }
    const ln = at(sc, -L * .62, 0, 0), ln2 = at(sc, -L * .25, 0, 0);
    tx.strokeStyle = tone(v.lo, .45); tx.lineWidth = h * .025; tx.beginPath(); tx.moveTo(ln2[0], ln2[1]); tx.lineTo(ln[0], ln[1]); tx.stroke(); // orta çizgi
    tx.restore();
    return P;
  }
  // baş (¾ ya da profil): yüz bakış açısı face (-1 sol profil … 0 ön … 1 sağ profil), eğim tilt
  function head(J, h, lit, v, o = {}) {
    const [cx, cy] = J.hd, face = o.face ?? .5, tilt = o.tilt ?? 0;
    tx.save(); px.save();
    for (const c of [tx, px]) { c.translate(cx, cy); c.rotate(tilt); }
    const rw = h * .37, rh = h * .5;
    // kafatası + çene
    const P = new Path2D();
    P.ellipse(0, -h * .05, rw, rh * .9, 0, 0, TAU);
    const jx = face * rw * .45;
    P.moveTo(-rw * .85 + jx * .5, h * .05);
    P.quadraticCurveTo(-rw * .6 + jx, h * .42, jx * 1.1, h * .48);
    P.quadraticCurveTo(rw * .6 + jx, h * .42, rw * .85 + jx * .5, h * .05);
    P.closePath();
    const g = tx.createLinearGradient(lit[0] * rw, lit[1] * rh, -lit[0] * rw, -lit[1] * rh);
    g.addColorStop(0, tone(v.hi)); g.addColorStop(.45, tone(v.mid)); g.addColorStop(1, tone(v.lo));
    fill(P, g, { th: PI / 2 - .3 * face, id: 5, ph: o.ph || 0 });
    // yüz düzlemi: göz çukuru gölgesi, burun, ağız (ton)
    tx.save(); tx.clip(P);
    const ex = jx * .9, ey = -h * .02;
    for (const s of [-1, 1]) {
      const w = s * (s === Math.sign(face || 1) ? .5 : 1) * rw * .42;
      const eg = tx.createRadialGradient(ex + w, ey, 1, ex + w, ey, rw * .32);
      eg.addColorStop(0, tone(v.lo * .7, .9)); eg.addColorStop(1, tone(v.lo, 0));
      tx.fillStyle = eg; tx.fillRect(ex + w - rw * .4, ey - rw * .4, rw * .8, rw * .8);
    }
    // burun gölgesi (ışığın karşı tarafında)
    tx.fillStyle = tone(v.lo, .7);
    tx.beginPath(); tx.moveTo(ex + face * rw * .25, ey + h * .02); tx.lineTo(ex + face * rw * .4 - lit[0] * rw * .25, ey + h * .2); tx.lineTo(ex + face * rw * .2, ey + h * .22); tx.closePath(); tx.fill();
    // kaş çizgisi ve ağız
    tx.strokeStyle = tone(v.lo * .6, .85); tx.lineWidth = h * .035; tx.lineCap = 'round';
    tx.beginPath(); tx.moveTo(ex - rw * .55, ey - h * .07 + (o.brow ?? 0)); tx.quadraticCurveTo(ex, ey - h * .12, ex + rw * .45 + face * rw * .2, ey - h * .08 - (o.brow ?? 0)); tx.stroke();
    tx.lineWidth = h * .025;
    tx.beginPath(); tx.moveTo(ex - rw * .22 + face * rw * .2, ey + h * .3); tx.quadraticCurveTo(ex + face * rw * .3, ey + h * .3 + (o.mouth ?? 0), ex + rw * .22 + face * rw * .35, ey + h * .29); tx.stroke();
    tx.restore();
    // saç: kıvırcık kütle, başın arkasında ve üstünde
    if (o.hair !== false) {
      const HP = new Path2D(), r = rng(o.seed || 9);
      for (let i = 0; i < 16; i++) {
        const a = -PI * .05 - i / 15 * PI * 1.1 - face * .5, rr = rw * (1.0 + r() * .15);
        const hx = Math.cos(a) * rr * .95 - face * rw * .25, hy = -h * .05 + Math.sin(a) * rh * .95;
        HP.moveTo(hx + h * .1, hy); HP.arc(hx, hy, h * (.09 + r() * .05), 0, TAU);
      }
      const hg = tx.createLinearGradient(lit[0] * rw, lit[1] * rh - h * .3, -lit[0] * rw, -lit[1] * rh);
      hg.addColorStop(0, tone(v.hair ?? .45)); hg.addColorStop(1, tone(.06));
      fill(HP, hg, { th: -.6, id: 4, ph: .3 });
    }
    tx.restore(); px.restore();
    return P;
  }
  // el: yumruk ya da açık el (basit kütle)
  function hand(p, dir, h, lit, v, open = .5) {
    const P = new Path2D(), r = h * .14;
    P.ellipse(p[0] + Math.cos(dir) * r * .8, p[1] + Math.sin(dir) * r * .8, r * (1.2 + open * .5), r * .8, dir, 0, TAU);
    const g = tx.createLinearGradient(p[0] + lit[0] * r, p[1] + lit[1] * r, p[0] - lit[0] * r, p[1] - lit[1] * r);
    g.addColorStop(0, tone(v.hi)); g.addColorStop(1, tone(v.lo));
    fill(P, g, { th: dir + PI / 2, id: 5 });
    return P;
  }
  // ── heykel gölgeleme ──
  // drawMask(c): beden parçalarını beyazla doldurur; drawBumps(c): kas kabartmalarını (beyaz = tümsek, koyu yok) çizer.
  // bb: [x0,y0,x1,y1] dünya; o: {lit:[lx,ly], lz, amb, lo, hi, rim, rimDir:[x,y], infl (şişirme yarıçapı), bump, id, edge}
  const _sc = { m: makeCanvas(8, 8), b: makeCanvas(8, 8) };
  function blurF(src, w, h, r, passes = 3) {
    let a = src, t = new Float32Array(w * h);
    for (let p = 0; p < passes; p++) {
      const o = new Float32Array(w * h);
      for (let y = 0; y < h; y++) { // yatay
        let acc = 0, row = y * w; const win = 2 * r + 1;
        for (let x = -r; x <= r; x++) acc += a[row + Math.min(w - 1, Math.max(0, x))];
        for (let x = 0; x < w; x++) { t[row + x] = acc / win; acc += a[row + Math.min(w - 1, x + r + 1)] - a[row + Math.max(0, x - r)]; }
      }
      for (let x = 0; x < w; x++) { // dikey
        let acc = 0; const win = 2 * r + 1;
        for (let y = -r; y <= r; y++) acc += t[Math.min(h - 1, Math.max(0, y)) * w + x];
        for (let y = 0; y < h; y++) { o[y * w + x] = acc / win; acc += t[Math.min(h - 1, y + r + 1) * w + x] - t[Math.max(0, y - r) * w + x]; }
      }
      a = o;
    }
    return a;
  }
  function sculpt(bb, drawMask, drawBumps, o = {}) {
    const x0 = Math.floor(bb[0]), y0 = Math.floor(bb[1]);
    const w = Math.ceil((bb[2] - x0) * RS), h = Math.ceil((bb[3] - y0) * RS);
    if (w < 4 || h < 4) return;
    for (const k of ['m', 'b']) { const c = _sc[k]; if (c.width !== w || c.height !== h) { c.width = w; c.height = h; } }
    const mc = _sc.m.getContext('2d', { willReadFrequently: true }), bc = _sc.b.getContext('2d', { willReadFrequently: true });
    for (const c of [mc, bc]) { c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, w, h); c.setTransform(RS, 0, 0, RS, -x0 * RS, -y0 * RS); c.fillStyle = '#fff'; c.strokeStyle = '#fff'; }
    drawMask(mc); if (drawBumps) { bc.globalCompositeOperation = 'lighter'; drawBumps(bc); bc.globalCompositeOperation = 'source-over'; }
    const md = mc.getImageData(0, 0, w, h).data, bd = bc.getImageData(0, 0, w, h).data;
    const N = w * h, M = new Float32Array(N), Bm = new Float32Array(N);
    for (let i = 0; i < N; i++) { M[i] = md[i * 4 + 3] / 255; Bm[i] = bd[i * 4] / 255 * bd[i * 4 + 3] / 255; }
    const rI = Math.max(2, Math.round((o.infl ?? 14) * RS));
    const Hm = blurF(M, w, h, rI, 3), Bb = blurF(Bm, w, h, Math.max(1, Math.round(rI * .35)), 2), Ms = blurF(M, w, h, Math.max(1, Math.round(RS * 1.2)), 1);
    const Hf = new Float32Array(N), bump = o.bump ?? .5;
    for (let i = 0; i < N; i++) Hf[i] = Math.sqrt(Math.max(0, Hm[i])) * M[i] + Bb[i] * bump * M[i];
    const T = tx.getImageData(x0 * RS, y0 * RS, w, h), Pd = px.getImageData(x0 * RS, y0 * RS, w, h);
    const td = T.data, pd = Pd.data;
    const lit = o.lit || [-.5, -.8], lzz = o.lz ?? .55;
    let lx = lit[0], ly = lit[1], lz = lzz; const ln = Math.hypot(lx, ly, lz); lx /= ln; ly /= ln; lz /= ln;
    const amb = o.amb ?? .12, lo = o.lo ?? .08, hi = o.hi ?? .95, rim = o.rim ?? 0, rd = o.rimDir || [-lit[0], -lit[1]];
    const kz = (o.depth ?? 26) * RS * 3, id = o.id ?? 5, edge = o.edge ?? .9, ph = Math.round(((o.ph || 0) % 1 + 1) % 1 * 256) & 255;
    // tarama alanı: düz çizgiler (θ0) formun yüksekliğiyle bükülür → bedeni saran kavisler. Evre, GR.PHB arabelleğine yazılır.
    // anchor: nesnenin çapa noktası (dünya); nesne kayınca çizgiler onunla kayar.
    const th0 = o.axis ?? 0, Pst = GR.STY[id].P, K = o.wrap ?? 2.2, Kb = o.wrapB ?? .6;
    const cs0 = Math.cos(th0), sn0 = Math.sin(th0), cm = GR.getCam(), kk = 1 / (RS * cm.s), an = o.anchor || [0, 0];
    const Hb = new Float32Array(N); for (let i = 0; i < N; i++) Hb[i] = Math.sqrt(Math.max(0, Hm[i])) + Bb[i] * Kb / K;
    const bytes = GR.bufBytes(id), PHB = GR.PHB, gx0 = x0 * RS, gy0 = y0 * RS;
    for (let y = 1; y < h - 1; y++) for (let x = 1; x < w - 1; x++) {
      const i = y * w + x, m = M[i];
      if (m < .003) continue;
      const gx = (Hf[i + 1] - Hf[i - 1]) * kz, gy = (Hf[i + w] - Hf[i - w]) * kz;
      let nx = -gx, ny = -gy, nz = 1; const nl = Math.hypot(nx, ny, nz); nx /= nl; ny /= nl; nz /= nl;
      let d = nx * lx + ny * ly + nz * lz; d = d < 0 ? 0 : d;
      let v = amb + (1 - amb) * d;
      if (rim > 0) { const f = 1 - nz, rr = o.rimAll ? Math.max(o.rimAll, nx * rd[0] + ny * rd[1]) : nx * rd[0] + ny * rd[1]; if (rr > 0) v += rim * f * f * rr * 1.6; }
      v = lo + (hi - lo) * Math.min(1, v);
      const e = Math.max(0, Ms[i] < .999 ? (1 - Ms[i]) * 2.2 : 0) * edge * (d < .35 ? 1.2 : .7);
      v *= 1 - Math.min(.92, e);
      const k = i * 4, a = m;
      const tv = v * 255;
      td[k] = td[k] * (1 - a) + tv * a; td[k + 1] = td[k]; td[k + 2] = td[k];
      if (a > .5) {
        const X = x + gx0, Y = y + gy0;
        if (X >= 0 && X < DW && Y >= 0 && Y < DH) {
          const wx = X * kk + cm.x - an[0], wy = Y * kk + cm.y - an[1];
          PHB[Y * DW + X] = (wy * cs0 - wx * sn0) / Pst + K * Hb[i] + (o.ph || 0);
        }
        pd[k] = bytes[0]; pd[k + 1] = bytes[1]; pd[k + 2] = bytes[2];
      }
    }
    tx.putImageData(T, x0 * RS, y0 * RS); px.putImageData(Pd, x0 * RS, y0 * RS);
  }
  // bütün beden. o: {h (baş yüksekliği), lit, v (ton), near, face, tilt, legs (false: belden yukarı), clip (Path2D: görünür bölge)}
  function body(J, o) {
    const h = o.h, lit = o.lit || [-.5, -.8], near = o.near || 'R', far = near === 'R' ? 'L' : 'R';
    const v = Object.assign({ hi: .92, mid: .55, lo: .14, refl: .3 }, o.v || {});
    const vf = { hi: v.hi * .78, mid: v.mid * .7, lo: v.lo * .8, refl: v.refl * .8 };
    const parts = [];
    const arm = (s, vv) => {
      parts.push(limb(J['sh' + s], J['el' + s], PROF.upperArm(h), h * .27, lit, vv));
      parts.push(limb(J['el' + s], J['wr' + s], PROF.foreArm(h), h * .24, lit, vv));
      parts.push(hand(J['wr' + s], Math.atan2(J['wr' + s][1] - J['el' + s][1], J['wr' + s][0] - J['el' + s][0]), h, lit, vv, o['open' + s] ?? .5));
    };
    const leg = (s, vv) => {
      parts.push(limb(J['hp' + s], J['kn' + s], PROF.thigh(h), h * .38, lit, vv));
      parts.push(limb(J['kn' + s], J['an' + s], PROF.shin(h), h * .25, lit, vv));
    };
    if (o.legs !== false) leg(far, vf);
    arm(far, vf);
    // boyun
    parts.push(limb(J.nk, J.hd, f => h * .2, h * .2, lit, v, { bend: .1 }));
    parts.push(torso(J, h, lit, v, o));
    if (o.legs !== false) leg(near, v);
    parts.push(head(J, h, lit, v, o));
    arm(near, v);
    return parts;
  }
  // mürekkep kontur: parçaların dış hatları (çıktıya, basmadan sonra)
  function contour(ctx, parts, w = 1.4, a = .9) {
    ctx.save(); ctx.setTransform(RS, 0, 0, RS, 0, 0); ctx.strokeStyle = `rgba(${GR.INK},${a})`; ctx.lineWidth = w; ctx.lineJoin = 'round';
    for (const P of parts) ctx.stroke(P);
    ctx.restore();
  }
  // profil baş yolu: merkez (cx,cy), baş yüksekliği h, dir = +1 sağa bakar, tilt radyan (+ arkaya yatık)
  function profilePath(cx, cy, h, dir = 1, tilt = 0) {
    const U = [[-.4, -.08], [-.3, -.38], [-.02, -.52], [.24, -.42], [.34, -.24], [.33, -.12], [.37, -.05], [.49, .09], [.39, .14], [.41, .2], [.36, .245], [.4, .29], [.34, .36], [.37, .45], [.24, .53], [-.02, .44], [-.14, .36], [-.2, .62], [-.42, .62], [-.42, .2]];
    const c = Math.cos(tilt * dir), s = Math.sin(tilt * dir), P = new Path2D();
    spline(P, U.map(([x, y]) => { x *= dir * h; y *= h; return [cx + x * c - y * s, cy + x * s + y * c]; }), true, .55);
    return P;
  }
  // gövde dış hattı (omuzlar, bel, kalça)
  function torsoPath(J, h, k = 1) {
    const { shL, shR, hpL, hpR, nk } = J, P = new Path2D();
    const mid = [(shL[0] + shR[0] + hpL[0] + hpR[0]) / 4, (shL[1] + shR[1] + hpL[1] + hpR[1]) / 4];
    const wc = (p, q) => [lerp(mid[0], p[0], q * k), lerp(mid[1], p[1], q)];
    const wst = (sh, hp) => [lerp(sh[0], hp[0], .5) + (mid[0] - lerp(sh[0], hp[0], .5)) * .16, lerp(sh[1], hp[1], .5)];
    spline(P, [wc(shL, 1.12), wst(shL, hpL), wc(hpL, 1.06), [lerp(hpL[0], hpR[0], .5), lerp(hpL[1], hpR[1], .5) + h * .15],
      wc(hpR, 1.06), wst(shR, hpR), wc(shR, 1.12), [nk[0], nk[1] + h * .1]], true, .9);
    return P;
  }
  // zırh: göğüslük (orta sırtlı, karında yatay levhalar), omuzluklar, boyunluk. Doré'nin Şeytan'ındaki gibi; çıplaklık çağrışımı bırakmaz.
  function armor(J, h, sh = {}) {
    const { shL, shR, hpL, hpR, nk } = J;
    const sc = [(shL[0] + shR[0]) / 2, (shL[1] + shR[1]) / 2], hc = [(hpL[0] + hpR[0]) / 2, (hpL[1] + hpR[1]) / 2];
    const L = Math.hypot(hc[0] - sc[0], hc[1] - sc[1]), ux = (hc[0] - sc[0]) / L, uy = (hc[1] - sc[1]) / L, nx = -uy, ny = ux;
    const sw = Math.hypot(shR[0] - shL[0], shR[1] - shL[1]), at = (al, sd) => [sc[0] + ux * al + nx * sd, sc[1] + uy * al + ny * sd];
    const ta = Math.atan2(ny, nx);
    const xs = [shL[0], shR[0], hpL[0], hpR[0]], ys = [shL[1], shR[1], hpL[1], hpR[1], nk[1]];
    const bb = [Math.min(...xs) - h, Math.min(...ys) - h, Math.max(...xs) + h, Math.max(...ys) + h];
    const TP = torsoPath(J, h, 1.04);
    sculpt(bb, c => {
      c.fill(TP);
      for (const s of [shL, shR]) { c.beginPath(); c.ellipse(s[0], s[1] + h * .04, h * .46, h * .36, ta, 0, TAU); c.fill(); } // omuzluklar
      c.beginPath(); c.ellipse(nk[0], nk[1] + h * .12, h * .3, h * .16, ta, 0, TAU); c.fill();                            // boyunluk
    }, c => {
      const blob = (x, y, rx, ry, a, v) => { c.save(); c.translate(x, y); c.rotate(a); c.scale(1, ry / rx); const g = c.createRadialGradient(0, 0, 0, 0, 0, rx); g.addColorStop(0, `rgba(255,255,255,${v})`); g.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = g; c.fillRect(-rx, -rx, rx * 2, rx * 2); c.restore(); };
      let q = at(L * .26, 0); blob(q[0], q[1], sw * .52, L * .3, ta, .7);                    // göğüs kubbesi
      for (const s of [shL, shR]) blob(s[0], s[1], h * .4, h * .32, ta, .95);                // omuzluk kubbeleri
      c.lineCap = 'round'; c.strokeStyle = 'rgba(255,255,255,.75)';
      c.lineWidth = h * .07; c.beginPath(); let a0 = at(L * .06, 0), a1 = at(L * .62, 0); c.moveTo(a0[0], a0[1]); c.lineTo(a1[0], a1[1]); c.stroke(); // orta sırt
      c.lineWidth = h * .075;
      for (let k = 0; k < 3; k++) { const f = .66 + k * .13, hw = sw * (.4 - k * .01); const p0 = at(L * f, -hw), p1 = at(L * f, hw), pm = at(L * (f + .05), 0); c.beginPath(); c.moveTo(p0[0], p0[1]); c.quadraticCurveTo(pm[0], pm[1], p1[0], p1[1]); c.stroke(); } // karın levhaları
    }, Object.assign({ id: 9, infl: h * .2, bump: .55, depth: 30, axis: .5, wrap: 2.0, lo: .03, hi: .8, edge: .6 }, sh));
    return TP;
  }
  // profil baş (yüz gölgede, ön hatta kenar ışığı), geriye savrulan saç, tek göz ışığı
  function headProfile(cx, cy, hh, dir = 1, tilt = 0, o = {}) {
    const HP = profilePath(cx, cy, hh, dir, tilt), sh = o.sh || {}, t = o.t || 0;
    const c0 = Math.cos(tilt * dir), s0 = Math.sin(tilt * dir), loc = (x, y) => [cx + (x * dir * c0 - y * s0) * hh, cy + (x * dir * s0 + y * c0) * hh];
    // saç: tepeden enseye, arkaya ve yukarı savrulan tutamlar (kafanın arkasında; önce çizilir)
    const strands = [];
    const r = rng(o.seed || 11);
    for (let i = 0; i < 9; i++) {
      const f = i / 8, b = loc(lerp(.12, -.36, f), lerp(-.5, .12, f)), ang = lerp(-2.2, -3.5, f) + Math.sin(t * .9 + i) * .05 * (o.wind ?? 1);
      const Ln = hh * (lerp(.55, .8, Math.sin(f * PI)) + r() * .15) * (o.hair ?? 1), wd = hh * (.2 + r() * .06);
      const a = (dir > 0 ? ang : PI - ang) + tilt * dir, tip = [b[0] + Math.cos(a) * Ln, b[1] + Math.sin(a) * Ln];
      const nx = -Math.sin(a), ny = Math.cos(a), cv = (r() - .3) * Ln * .35 * dir;
      const P = new Path2D(); P.moveTo(b[0] + nx * wd * .5, b[1] + ny * wd * .5);
      P.quadraticCurveTo((b[0] + tip[0]) / 2 + nx * (wd * .6 + cv), (b[1] + tip[1]) / 2 + ny * (wd * .6 + cv), tip[0], tip[1]);
      P.quadraticCurveTo((b[0] + tip[0]) / 2 + nx * (cv - wd * .3), (b[1] + tip[1]) / 2 + ny * (cv - wd * .3), b[0] - nx * wd * .5, b[1] - ny * wd * .5); P.closePath();
      strands.push(P);
    }
    const bbH = [cx - hh * 1.6, cy - hh * 1.5, cx + hh * 1.6, cy + hh * 1.2];
    sculpt(bbH, c => { for (const P of strands) c.fill(P); const k = loc(-.12, -.2); c.beginPath(); c.arc(k[0], k[1], hh * .34, 0, TAU); c.fill(); }, null,
      Object.assign({ id: 5, infl: hh * .05, depth: 30, lo: .02, hi: .5, amb: .03, rim: 1.0, axis: (dir > 0 ? -.5 : .5), wrap: 1.4, edge: .3 }, sh, o.hairSh || {}));
    sculpt(bbH, c => c.fill(HP), null,
      Object.assign({ id: 5, infl: hh * .07, depth: 40, lo: .02, hi: .4, amb: .02, rim: 1.5, axis: .9 * dir, wrap: 1.2, edge: .25 }, sh, o.faceSh || {}));
    const eo = o.eye ?? 1;
    if (eo > 0) { const e = loc(.2, -.07); tx.fillStyle = tone(1); tx.beginPath(); tx.ellipse(e[0], e[1], hh * .06, hh * .026 * eo, tilt * dir, 0, TAU); tx.fill(); }
    return HP;
  }
  // bütün Şeytan: uzak kol ve bacaklar, zırh, baş, yakın kol. o: {h, hh (baş), near, dir (yüzün baktığı yön), tilt, sh (ortak ışık), anchor, legs, eye, t}
  function satan(J, o) {
    const h = o.h, sh = Object.assign({ lit: [.75, -.55], lz: .2, lo: .03, hi: .8, amb: .04, rim: 1.0, rimDir: [.75, -.6], anchor: o.anchor }, o.sh || {});
    sbody(J, { h, near: o.near || 'L', noHead: true, noTorso: true, legs: o.legs !== false, sh: Object.assign({ axis: -.45, wrap: 1.6, bump: .3, edge: .5, depth: 30 }, sh) });
    armor(J, h, Object.assign({}, sh, { hi: Math.min(.85, sh.hi + .05) }));
    headProfile(J.hd[0], J.hd[1], o.hh || h * 1.15, o.dir || 1, o.tilt ?? -.25, { sh: { lit: sh.lit, lz: sh.lz, rimDir: sh.rimDir, anchor: o.anchor }, eye: o.eye, t: o.t, seed: o.seed, wind: o.wind });
  }
  // heykel yoluyla beden: parçalar maskeye, kaslar tümseğe; gölge + eş-yükselti tarama
  function sbody(J, o) {
    const h = o.h, near = o.near || 'R', far = near === 'R' ? 'L' : 'R';
    const pts = Object.values(J); let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (const [x, y] of pts) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y); }
    const bb = [x0 - h * 1.2, y0 - h * 1.2, x1 + h * 1.2, y1 + h * 1.2];
    const caps = [];
    const L = (a, b, prof, side) => caps.push({ c: capsule(J[a], J[b], prof(h)), side });
    const legs = o.legs !== false;
    if (legs) { for (const s of [far, near]) { L('hp' + s, 'kn' + s, PROF.thigh, s); L('kn' + s, 'an' + s, PROF.shin, s); } }
    for (const s of [far, near]) { L('sh' + s, 'el' + s, PROF.upperArm, s); L('el' + s, 'wr' + s, PROF.foreArm, s); }
    const drawTorso = c => { // gövde, boyun, baş
      const { nk, hd } = J;
      if (!o.noTorso) c.fill(torsoPath(J, h));
      c.fill(capsule(nk, [lerp(nk[0], hd[0], .6), lerp(nk[1], hd[1], .6)], f => h * .21).P);
      if (o.noHead) return;
      if (o.profile) c.fill(profilePath(hd[0], hd[1], h, o.profile, o.tilt || 0));
      else { const Hh = new Path2D(); Hh.ellipse(hd[0], hd[1], h * .38, h * .5, o.tilt || 0, 0, TAU); c.fill(Hh); }
    };
    const mask = c => { drawTorso(c); for (const k of caps) c.fill(k.c.P); for (const s of ['L', 'R']) { const w = J['wr' + s], e = J['el' + s]; const a = Math.atan2(w[1] - e[1], w[0] - e[0]); c.beginPath(); c.ellipse(w[0] + Math.cos(a) * h * .16, w[1] + Math.sin(a) * h * .16, h * .24, h * .16, a, 0, TAU); c.fill(); } };
    const bumps = c => {
      const blob = (x, y, rx, ry, a, v) => { c.save(); c.translate(x, y); c.rotate(a); c.scale(1, ry / rx); const g = c.createRadialGradient(0, 0, 0, 0, 0, rx); g.addColorStop(0, `rgba(255,255,255,${v})`); g.addColorStop(1, 'rgba(255,255,255,0)'); c.fillStyle = g; c.fillRect(-rx, -rx, rx * 2, rx * 2); c.restore(); };
      const { shL, shR, hpL, hpR } = J, sw = Math.hypot(shR[0] - shL[0], shR[1] - shL[1]);
      const ta = Math.atan2(shR[1] - shL[1], shR[0] - shL[0]);
      if (o.noTorso) { for (const sd of ['L', 'R']) { const sh = J['sh' + sd], el = J['el' + sd]; blob(lerp(sh[0], el[0], .5), lerp(sh[1], el[1], .5), h * .3, h * .2, Math.atan2(el[1] - sh[1], el[0] - sh[0]), .6); if (legs) { const hp = J['hp' + sd], kn = J['kn' + sd]; blob(lerp(hp[0], kn[0], .4), lerp(hp[1], kn[1], .4), h * .4, h * .26, Math.atan2(kn[1] - hp[1], kn[0] - hp[0]), .5); } } return; }
      if (o.back) { // sırt: kürek kemikleri, omurga yanı kas sütunları, deltoidler, bel çukuru
        const scx = (shL[0] + shR[0]) / 2, scy = (shL[1] + shR[1]) / 2, hcx = (hpL[0] + hpR[0]) / 2, hcy = (hpL[1] + hpR[1]) / 2, Lb = Math.hypot(hcx - scx, hcy - scy);
        const ux = (hcx - scx) / Lb, uy = (hcy - scy) / Lb, nx = -uy, ny = ux, at = (al, sd) => [scx + ux * al + nx * sd, scy + uy * al + ny * sd];
        for (const sd of [-1, 1]) {
          const sh = sd < 0 ? shR : shL; blob(sh[0], sh[1] + h * .08, h * .36, h * .3, ta, .9);
          let q = at(Lb * .2, sd * sw * .27); blob(q[0], q[1], sw * .2, sw * .26, ta + sd * .35, .85);   // kürek kemiği
          q = at(Lb * .55, sd * sw * .1); blob(q[0], q[1], sw * .09, Lb * .34, ta, .6);                    // omurga yanı
          q = at(Lb * .5, sd * sw * .36); blob(q[0], q[1], sw * .14, Lb * .26, ta - sd * .12, .45);        // kanat kası (lat)
          const el = J['el' + (sd < 0 ? 'R' : 'L')]; blob(lerp(sh[0], el[0], .55), lerp(sh[1], el[1], .55), h * .3, h * .2, Math.atan2(el[1] - sh[1], el[0] - sh[0]), .6);
        }
        const tq = at(-h * .05, 0); blob(tq[0], tq[1], sw * .3, h * .22, ta, .7);                         // trapez
        return;
      }
      for (const [s, sh, hp] of [['L', shL, hpL], ['R', shR, hpR]]) {
        blob(sh[0], sh[1] + h * .05, h * .32, h * .26, ta, .9); // deltoid
        blob(lerp(sh[0], hp[0], .22) + (shL[0] + shR[0] - 2 * sh[0]) * .2, lerp(sh[1], hp[1], .22), sw * .26, sw * .17, ta, .8); // göğüs
        const el = J['el' + s]; blob(lerp(sh[0], el[0], .5), lerp(sh[1], el[1], .5), h * .26, h * .17, Math.atan2(el[1] - sh[1], el[0] - sh[0]), .6); // pazı
        if (legs) { const kn = J['kn' + s]; blob(lerp(hp[0], kn[0], .4), lerp(hp[1], kn[1], .4), h * .4, h * .26, Math.atan2(kn[1] - hp[1], kn[0] - hp[0]), .5); }
      }
      const sc = [(shL[0] + shR[0]) / 2, (shL[1] + shR[1]) / 2], hc = [(hpL[0] + hpR[0]) / 2, (hpL[1] + hpR[1]) / 2];
      for (let k = 0; k < 3; k++) for (const s of [-1, 1]) { const f = .48 + k * .14; blob(lerp(sc[0], hc[0], f) + s * sw * .09, lerp(sc[1], hc[1], f), sw * .1, sw * .075, ta, .45); }
      // yüz: burun, kaş kemiği, elmacık, çene
      const hd = J.hd, fc = o.face ?? .4;
      if (o.profile) { blob(hd[0] + o.profile * h * .12, hd[1] + h * .12, h * .2, h * .16, 0, .7); blob(hd[0] - o.profile * h * .05, hd[1] - h * .2, h * .28, h * .2, 0, .6); return; }
      blob(hd[0] + fc * h * .22, hd[1] + h * .05, h * .08, h * .16, 0, .9);
      blob(hd[0] + fc * h * .12, hd[1] - h * .12, h * .26, h * .07, 0, .7);
      blob(hd[0] + fc * h * .14, hd[1] + h * .34, h * .14, h * .1, 0, .6);
    };
    sculpt(bb, mask, bumps, Object.assign({ infl: h * .22, bump: .45, depth: 30, axis: PI / 2 }, o.sh || {}));
    return { bb, mask };
  }
  function test(t) {
    const J = {
      hd: [960, 300], nk: [960, 360], shL: [870, 395], shR: [1050, 395], elL: [820, 520], elR: [1110, 510], wrL: [850, 630], wrR: [1150, 620],
      hpL: [905, 640], hpR: [1020, 640], knL: [890, 800], knR: [1040, 800], anL: [880, 950], anR: [1060, 950],
    };
    sbody(J, { h: 120, near: 'R', face: .45, tilt: -.1, sh: { lit: [-.6, -.7], lo: .1, hi: .95, rim: .5, axis: .15, wrap: 2.6 } });
    FG._last = [];
  }
  return { capsule, limb, torso, head, hand, body, sbody, profilePath, torsoPath, armor, headProfile, satan, contour, test, PROF, sculpt, blurF };
})();
