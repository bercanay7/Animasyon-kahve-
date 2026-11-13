// Hayvanlar: inek/sığır, kartal, koç. Siyah figür üslubu, kazıma detaylar.
'use strict';
// İnek: x,y yer çizgisi (gövde ortası altında), s ölçek, dir yön, ph yürüyüş fazı (0..1 döngü), o: {col, inc, head, tail}
function cow(ctx, x, y, s, dir, ph, o = {}) {
  const col = o.col || C.ink, inc = o.inc || C.clay, walk = o.walk ?? 1;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
  ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  const bob = Math.sin(ph * TAU * 2) * 1.2 * walk;
  ctx.translate(0, bob);
  const legs = [
    { hip: [26, -38], ph: .25, front: true, far: true },
    { hip: [-34, -40], ph: 0, front: false, far: true },
    { hip: [24, -38], ph: .75, front: true, far: false },
    { hip: [-36, -40], ph: .5, front: false, far: false },
  ];
  legs.forEach((L, i) => L.id = i);
  const drawLeg = (L, fill) => {
    const u = ((ph + L.ph) % 1 + 1) % 1;
    const stride = 22 * walk;
    let fx, lift;
    if (u < .62) { fx = lerp(stride / 2, -stride / 2, u / .62); lift = 0; }
    else { const v = (u - .62) / .38; fx = lerp(-stride / 2, stride / 2, E.sine(v)); lift = Math.sin(v * PI) * 9 * walk; }
    let foot = [L.hip[0] + fx + (L.front ? 2 : -2), -3 - lift - bob];
    if (o.legOverride && o.legOverride[L.id] && L.id !== undefined) foot = o.legOverride[L.id];
    const r = ik2(L.hip, foot, L.front ? 19 : 21, L.front ? 19 : 18, L.front ? -1 : 1);
    ctx.fillStyle = fill; ctx.strokeStyle = fill;
    const seg = (a, b, w0, w1) => { const d = sub(b, a), n = scl([-d[1], d[0]], 1 / len(d)); ctx.beginPath(); ctx.moveTo(a[0] + n[0] * w0, a[1] + n[1] * w0); ctx.lineTo(b[0] + n[0] * w1, b[1] + n[1] * w1); ctx.lineTo(b[0] - n[0] * w1, b[1] - n[1] * w1); ctx.lineTo(a[0] - n[0] * w0, a[1] - n[1] * w0); ctx.fill(); ctx.beginPath(); ctx.arc(b[0], b[1], w1, 0, TAU); ctx.fill(); };
    seg(L.hip, r.j, L.front ? 7 : 9, 3.4); seg(r.j, r.e, 3.2, 2.4);
    // toynak
    ctx.beginPath(); ctx.moveTo(r.e[0] - 3, r.e[1]); ctx.lineTo(r.e[0] + 4.5, r.e[1]); ctx.lineTo(r.e[0] + 4, r.e[1] + 4); ctx.lineTo(r.e[0] - 3.5, r.e[1] + 4); ctx.fill();
    if (o.hoofMark && !L.far) o.hoofMark(ctx, [r.e[0], r.e[1] + 4], lift);
    return r;
  };
  const farCol = o.farCol || col;
  for (const L of legs.filter(l => l.far)) drawLeg(L, farCol);
  // kuyruk
  const tw = Math.sin(ph * TAU + 1) * .3 + (o.tailWag || 0);
  ctx.strokeStyle = col; ctx.lineWidth = 2.6;
  const tb = [-46, -46], tm = add(tb, rot([-6, 18], tw)), te = add(tm, rot([-2, 16], tw * 1.6));
  ctx.beginPath(); ctx.moveTo(...tb); ctx.quadraticCurveTo(tm[0], tm[1], te[0], te[1]); ctx.stroke();
  ctx.fillStyle = col; ctx.beginPath(); ctx.ellipse(te[0], te[1] + 3, 3, 6, tw, 0, TAU); ctx.fill();
  // gövde
  ctx.fillStyle = col;
  ctx.beginPath(); spline(ctx, [[-47, -50], [-34, -58], [-10, -58], [14, -60], [28, -63], [38, -57], [47, -49], [47, -39], [37, -30], [30, -23], [10, -26], [-14, -25], [-34, -28], [-45, -35], [-49, -44]]); ctx.fill();
  // kazıma: kaburga, gerdan, but
  if (inc) {
    ctx.strokeStyle = inc; ctx.lineWidth = 1.1;
    ctx.beginPath(); ctx.moveTo(-34, -48); ctx.quadraticCurveTo(-26, -36, -34, -29); ctx.stroke();
    for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.moveTo(-6 + k * 8, -50); ctx.quadraticCurveTo(-2 + k * 8, -40, -6 + k * 8, -30); ctx.stroke(); }
    for (let k = 0; k < 4; k++) { ctx.beginPath(); ctx.moveTo(32 + k * 2, -34 + k * 1.5); ctx.lineTo(38 + k * 2, -40 + k * 1.5); ctx.stroke(); }
  }
  if (o.spots) { ctx.fillStyle = o.spots; for (const [sx, sy, sr] of [[-20, -46, 7], [4, -40, 6], [-30, -36, 5], [18, -50, 5]]) { ctx.beginPath(); ctx.ellipse(sx, sy, sr * 1.3, sr, .3, 0, TAU); ctx.fill(); } }
  // baş
  const ha = (o.head || 0) + Math.sin(ph * TAU * 2 + .5) * .05 * walk;
  ctx.save(); ctx.translate(44, -50); ctx.rotate(ha);
  ctx.fillStyle = col;
  ctx.beginPath(); spline(ctx, [[-2, -6], [8, -10], [18, -8], [26, 2], [28, 9], [22, 13], [14, 11], [5, 8], [-3, 6]]); ctx.fill();
  // boynuz ve kulak
  ctx.beginPath(); ctx.moveTo(6, -8); ctx.quadraticCurveTo(6, -22, 16, -24); ctx.quadraticCurveTo(10, -20, 10, -9); ctx.fill();
  ctx.beginPath(); ctx.moveTo(2, -6); ctx.quadraticCurveTo(-10, -12, -12, -6); ctx.quadraticCurveTo(-6, -3, 2, -2); ctx.fill();
  if (inc) {
    ctx.strokeStyle = inc; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.ellipse(13, -3, 2.6, 1.6, -.2, 0, TAU); ctx.stroke();
    ctx.fillStyle = inc; ctx.beginPath(); ctx.arc(13.4, -3, .9, 0, TAU); ctx.fill();
    ctx.beginPath(); ctx.moveTo(23, 7); ctx.quadraticCurveTo(25, 9, 24, 11); ctx.stroke();
  }
  ctx.restore();
  for (const L of legs.filter(l => !l.far)) drawLeg(L, col);
  ctx.restore();
}

// Kartal: x,y gövde merkezi, s ölçek, dir yön, fl kanat fazı (0..1), o: {col, inc, talon:fn(ctx)}
function eagle(ctx, x, y, s, dir, fl, o = {}) {
  const col = o.col || C.ink, inc = o.inc || C.clay;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s); ctx.rotate(o.tilt || 0);
  ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  const k = o.k ?? (.62 + .38 * Math.cos(fl * TAU)); // kanatlar hep görünür, yukarı-aşağı çırpar
  const wing = (sx, far) => {
    ctx.save(); ctx.translate(sx, -6);
    const sy = far ? k * .8 : k;
    ctx.scale(1, sy === 0 ? .01 : sy);
    ctx.fillStyle = far ? (o.farCol || col) : col;
    // kanat: kök (0,0) -> bilek -> uç tüyler
    ctx.beginPath();
    ctx.moveTo(14, 2); ctx.bezierCurveTo(22, -40, 18, -82, 4, -118);
    // birincil tüyler (parmaklar)
    const tips = [[-4, -150], [-18, -152], [-32, -146], [-44, -134], [-54, -118]];
    let prev = [4, -118];
    for (const [tx, ty] of tips) { ctx.quadraticCurveTo(prev[0] - 2, ty + 6, tx, ty); ctx.lineTo(tx - 4, ty + 14); prev = [tx - 4, ty + 14]; }
    ctx.bezierCurveTo(-64, -80, -56, -30, -40, 2); ctx.closePath(); ctx.fill();
    if (inc && !far) {
      ctx.strokeStyle = inc; ctx.lineWidth = 1.4 / Math.max(.3, Math.abs(sy));
      ctx.lineWidth = 1.4;
      ctx.save(); ctx.scale(1, 1);
      for (let r = 0; r < 3; r++) for (let i = 0; i < 6; i++) {
        const u = i / 5, bx = lerp(8, -44, u), by = -26 - r * 26 - Math.sin(u * PI) * 8;
        ctx.beginPath(); ctx.moveTo(bx + 6, by); ctx.quadraticCurveTo(bx, by + 8, bx - 6, by); ctx.stroke();
      }
      for (let i = 0; i < 5; i++) { const u = i / 4; ctx.beginPath(); ctx.moveTo(lerp(-2, -40, u), -100 + u * 8); ctx.lineTo(lerp(-6, -50, u), -140 + u * 20); ctx.stroke(); }
      ctx.restore();
    }
    ctx.restore();
  };
  wing(-4, true);
  // kuyruk
  ctx.fillStyle = col;
  ctx.beginPath(); ctx.moveTo(-30, -6); ctx.lineTo(-74, -16); ctx.lineTo(-78, -4); ctx.lineTo(-76, 8); ctx.lineTo(-30, 6); ctx.closePath(); ctx.fill();
  if (inc) { ctx.strokeStyle = inc; ctx.lineWidth = 1.2; for (let i = 0; i < 4; i++) { ctx.beginPath(); ctx.moveTo(-36, -2 + i); ctx.lineTo(-74, -12 + i * 6); ctx.stroke(); } }
  // pençeler
  if (o.talon) { ctx.save(); ctx.translate(4, 14); o.talon(ctx); ctx.restore(); }
  ctx.strokeStyle = col; ctx.lineWidth = 5;
  ctx.beginPath(); ctx.moveTo(0, 8); ctx.lineTo(6, 26); ctx.moveTo(-8, 8); ctx.lineTo(-4, 26); ctx.stroke();
  ctx.lineWidth = 2.6;
  for (const fx of [6, -4]) { ctx.beginPath(); ctx.moveTo(fx, 26); ctx.lineTo(fx + 8, 30); ctx.moveTo(fx, 26); ctx.lineTo(fx - 4, 32); ctx.moveTo(fx, 26); ctx.lineTo(fx + 3, 34); ctx.stroke(); }
  // gövde
  ctx.fillStyle = col;
  ctx.beginPath(); spline(ctx, [[-34, -4], [-14, -14], [12, -16], [30, -14], [38, -10], [36, 0], [22, 10], [0, 13], [-24, 8]]); ctx.fill();
  // baş ve gaga
  ctx.beginPath(); spline(ctx, [[28, -14], [36, -22], [46, -22], [52, -17], [50, -12], [40, -6], [30, -4]]); ctx.fill();
  ctx.beginPath(); ctx.moveTo(49, -20); ctx.quadraticCurveTo(60, -20, 60, -10); ctx.quadraticCurveTo(56, -14, 50, -13); ctx.closePath(); ctx.fill();
  if (inc) {
    ctx.fillStyle = o.eye || C.white; ctx.beginPath(); ctx.arc(45, -17, 2.4, 0, TAU); ctx.fill();
    ctx.fillStyle = col; ctx.beginPath(); ctx.arc(45.6, -17, 1.1, 0, TAU); ctx.fill();
    ctx.strokeStyle = inc; ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(48, -14); ctx.lineTo(57, -12); ctx.stroke();
    for (let i = 0; i < 5; i++) { ctx.beginPath(); ctx.moveTo(18 - i * 9, -12); ctx.quadraticCurveTo(14 - i * 9, -4, 18 - i * 9, 4); ctx.stroke(); }
  }
  wing(8, false);
  ctx.restore();
}
// Koç (kurban hayvanı) — inek gövdesi küçültülmüş + kıvrık boynuz
function ram(ctx, x, y, s, dir, o = {}) {
  const col = o.col || C.ink, inc = o.inc || C.clay;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * dir, s);
  ctx.fillStyle = col;
  for (const lx of [-22, -14, 16, 22]) { ctx.fillRect(lx - 2, -24, 4.4, 24); }
  ctx.beginPath(); spline(ctx, [[-30, -30], [-18, -42], [6, -44], [24, -40], [32, -30], [24, -20], [0, -18], [-24, -20]]); ctx.fill();
  ctx.save(); ctx.translate(30, -38); ctx.rotate(o.head || 0);
  ctx.beginPath(); spline(ctx, [[-4, -6], [6, -10], [16, -4], [18, 4], [10, 6], [0, 4]]); ctx.fill();
  ctx.strokeStyle = col; ctx.lineWidth = 4;
  ctx.beginPath(); for (let a = 0; a < TAU * 1.1; a += .2) { const r = 7 - a * .9; const px = 2 + Math.cos(a - PI / 2) * r, py = -4 + Math.sin(a - PI / 2) * r; a ? ctx.lineTo(px, py) : ctx.moveTo(px, py); } ctx.stroke();
  if (inc) { ctx.fillStyle = inc; ctx.beginPath(); ctx.arc(10, -3, 1.2, 0, TAU); ctx.fill(); }
  ctx.restore();
  if (inc) { ctx.strokeStyle = inc; ctx.lineWidth = 1; for (let i = 0; i < 14; i++) { const px = -24 + (i % 7) * 7, py = -38 + Math.floor(i / 7) * 9; ctx.beginPath(); ctx.arc(px, py, 2.4, 0, PI); ctx.stroke(); } }
  ctx.restore();
}
