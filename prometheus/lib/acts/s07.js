// VII. TANIKLAR VE “İNEK GEÇİDİ” (H01–H10): Zeus'un evreni (kurbanlar, uşaklar, dalkavuk), tanık listesi, Okeanos'un öğüdü ve Prometheus'un alayı,
// perilerin "dilin fazla özgür"ü, kör umutlar, İo ve atsineği, inek geçidi haritası, "ben ölemem bile", İo'nun soyundan on üç kuşak ve okçu
'use strict';

// --- yardımcılar (H_ öneki) ---
const H_SKY = 'ikindi';
const H_rf = (c, x, gy, s, dir, lk, p = {}, o = {}) => figure(c, { x, y: gy - 44.5 * s, s, dir, sty: o.sty || STY.red, lk: { ...lk, rf: true, earHidden: true }, seed: o.seed ?? ((x * 7) | 0), stripe: .4, p: { breath: Math.sin((window.FIG_T || 0) * 1.5 + x) * .5, ...p }, ...o });
const H_lek = (c, x, gy, s, dir, lk, p = {}, o = {}) => figure(c, { x, y: gy - 44.5 * s, s, dir, sty: o.sty || STY.lek, lk, seed: o.seed ?? ((x * 3) | 0), p: { breath: Math.sin((window.FIG_T || 0) * 1.4 + x) * .4, ...p }, ...o });
// mahkeme şeridinde tek tanık satırı ve kırmızı onay işareti
function H_tanik(ctx, t, name, t0, d = 2.8) {
  const a = ramp(t, t0 - .2, t0 + .3) * (1 - ramp(t, t0 + d, t0 + d + .4)); if (a <= 0) return;
  F_court(ctx, t, [['TANIK', name, t0]], a);
  ctx.save(); baseT(ctx); ctx.globalAlpha = a; ctx.font = '600 46px Cinzel'; const x = 110 + ctx.measureText(L(name)).width + name.length * 1 + 40;
  inkPoly(ctx, [[x, 140], [x + 18, 162], [x + 58, 106]], ramp(t, t0 + .6, t0 + 1.0, E.lin), { col: '#D9583A', w: 7, jit: .3 }); ctx.restore();
}
// İo'nun boynuzları: baş yerel koordinatında iki küçük hilal
function H_horns(ctx, J, M, s) {
  const P = q => jointPt(ctx, M, add(J.neckT, rot(q, J.headA)));
  for (const [b, m, e, w] of [[[.9, -11.4], [.2, -14.6], [-2.2, -15.8], 1.0], [[-.6, -11.2], [-1.6, -13.9], [-3.8, -14.4], .8]]) {
    const B = P(b), Mi = P(m), Ee = P(e);
    ctx.lineCap = 'round'; ctx.strokeStyle = C.ink; ctx.lineWidth = w * 1.7 * s; ctx.beginPath(); ctx.moveTo(...B); ctx.quadraticCurveTo(...Mi, ...Ee); ctx.stroke();
    ctx.strokeStyle = STY.red.fill; ctx.lineWidth = w * .85 * s; ctx.stroke();
  }
}
// atsineği: titrek kanatlı küçük koyu böcek, arkasında parlak iz
function H_fly(ctx, x, y, t, s = 1, o = {}) {
  const pos = u => [x + Math.cos(u * 7.1) * 70 * s + Math.sin(u * 3.3) * 30 * s, y + Math.sin(u * 11.3) * 34 * s];
  if (o.trail !== false) { ctx.save(); ctx.lineCap = 'round'; for (let k = 1; k < 16; k++) { const a = pos(t - k * .018), b = pos(t - (k - 1) * .018); ctx.strokeStyle = `rgba(242,214,170,${.55 * (1 - k / 16)})`; ctx.lineWidth = 3 * s * (1 - k / 20); ctx.beginPath(); ctx.moveTo(...a); ctx.lineTo(...b); ctx.stroke(); } ctx.restore(); }
  const [px, py] = pos(t); ctx.save(); ctx.translate(px, py); ctx.scale(s, s);
  ctx.fillStyle = 'rgba(242,214,170,.5)'; const w = Math.abs(Math.sin(t * 90)); ctx.beginPath(); ctx.ellipse(-2, -7, 9, 3 + 3 * w, -.5, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.ellipse(3, -7, 8, 2.5 + 2.5 * w, .5, 0, TAU); ctx.fill();
  ctx.fillStyle = '#0A0605'; ctx.beginPath(); ctx.ellipse(0, 0, 9, 4.5, 0, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.arc(8, -1, 3.5, 0, TAU); ctx.fill();
  ctx.restore();
  return [px, py];
}
// İo: boynuzlu genç kız (kırmızı figür); koşar ya da çöker; atsineği başının çevresinde
function H_io(ctx, x, gy, s, t, o = {}) {
  const sty = { ...STY.red, white: STY.red.fill };
  let J = null, M = null; const cb = (j, m) => { J = j; M = m; };
  if (o.run !== undefined && o.run > 0) walkScene(ctx, null, x, s, t, o.dir || 1, { noCam: true, ground: FLAT(gy), stride: 52, lean: .26 * o.run, dist: x, sty, lk: { ...LK.io, rf: true, earHidden: true }, p: { head: -.05, wind: .4, ...(o.p || {}) }, onJoints: cb });
  else { const k = o.sink || 0, hy = lerp(44.5, 26, k) * s;
    figure(ctx, { x, y: gy - hy, s, dir: o.dir || 1, sty, lk: { ...LK.io, rf: true, earHidden: true }, seed: 61, stripe: .4,
      p: { torso: .15 + .55 * k, neck: .2 + .3 * k, head: .15 + .35 * k, shN: lerp(.3, 1.1, k), elN: lerp(.6, 1.8, k), shF: lerp(-.2, .9, k), elF: lerp(.5, 1.6, k), handN: 'open', handF: 'open', breath: Math.sin(t * 2.4) * (.5 + k), ...(o.p || {}) },
      ik: { fN: [x + (o.dir || 1) * 10 * s, gy - 1.5 * s, 0], fF: [x - (o.dir || 1) * lerp(10, 22, k) * s, gy - 1.5 * s, .3 * k] }, onJoints: cb }); }
  if (J) { H_horns(ctx, J, M, s); const h = jointPt(ctx, M, add(J.neckT, rot([1, -6], J.headA))); if (o.fly !== false) H_fly(ctx, h[0] - (o.dir || 1) * 30 * s, h[1] - 8 * s, t, s / 4.5); return h; }
}
// Okeanos: balık kuyruklu yaşlı deniz tanrısı (Sophilos deinosundaki gibi); y: bel hizası
// Okeanos'un elindeki balık (kırmızı figür, kazıma pullar)
const H_FISH = G => G.at([0, 1.5], .25, () => {
  G.part(c => { c.moveTo(-6.5, 0); c.quadraticCurveTo(-1, -3.4, 5.5, -.6); c.lineTo(9.2, -3.2); c.lineTo(8.4, 0); c.lineTo(9.2, 3.2); c.lineTo(5.5, .6); c.quadraticCurveTo(-1, 3.4, -6.5, 0); c.closePath(); }, { cutW: .28 });
  G.cut(c => { c.moveTo(-3.2, -1.4); c.quadraticCurveTo(-2.6, 0, -3.2, 1.4); for (let i = 0; i < 3; i++) { c.moveTo(-1 + i * 1.8, -1.2); c.lineTo(-.2 + i * 1.8, 0); c.lineTo(-1 + i * 1.8, 1.2); } }, .2);
  G.paint(c => c.arc(-4.8, -.5, .45, 0, TAU), C.ink);
});
function H_okeanos(ctx, x, y, s, t, o = {}) {
  const dir = o.dir || 1;
  ctx.save(); ctx.beginPath(); ctx.rect(x - 60 * s, y - 80 * s, 120 * s, 82 * s); ctx.clip();
  let J = null, M = null;
  // Sophilos'taki Okeanos: düz göğüs, sol omuzda himation, elinde balık, alnının üstünde küçük boğa boynuzları
  figure(ctx, { x, y, s, dir, sty: STY.red, lk: { beard: 'full', hair: 'long', anat: true, flatChest: true, himation: true, rf: true, earHidden: true }, seed: 71, stripe: .4,
    p: { torso: o.torso ?? .05, neck: .05, head: .05, shN: o.shN ?? .3, elN: o.elN ?? .8, shF: -.1, elF: .7, handN: o.handN || 'open', breath: Math.sin(t * 1.3) * .6 },
    onJoints: (j, m) => { J = j; M = m; } });
  ctx.restore();
  // himation: sol (yakın) omuzdan karşı kalçaya çapraz şal, siyah bordürlü; balık uzak elde (bel kırpmasının dışında çizilir)
  if (J) { const sh = jointPt(ctx, M, J.shoulder), hp = jointPt(ctx, M, J.hip), d = sub(hp, sh), nn = scl([-d[1], d[0]], 1 / (len(d) || 1)), w = 4.2 * s;
    ctx.save(); ctx.fillStyle = '#B55E33'; ctx.strokeStyle = C.ink; ctx.lineWidth = .7 * s; ctx.beginPath();
    ctx.moveTo(sh[0] + nn[0] * w - d[0] * .08, sh[1] + nn[1] * w - d[1] * .08); ctx.lineTo(hp[0] + nn[0] * w * .6 + dir * 3 * s, hp[1] + nn[1] * w * .6); ctx.lineTo(hp[0] - nn[0] * w * .6 + dir * 3 * s, hp[1] - nn[1] * w * .6); ctx.lineTo(sh[0] - nn[0] * w - d[0] * .08, sh[1] - nn[1] * w - d[1] * .08); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = C.red; ctx.lineWidth = .9 * s; ctx.beginPath(); ctx.moveTo(sh[0] + nn[0] * w * .55, sh[1] + nn[1] * w * .55); ctx.lineTo(hp[0] + nn[0] * w * .3 + dir * 3 * s, hp[1] + nn[1] * w * .3); ctx.stroke();
    ctx.strokeStyle = C.ink; ctx.lineWidth = .35 * s; for (let k = 1; k < 4; k++) { const q = lerp2(sh, hp, k / 4); ctx.beginPath(); ctx.moveTo(q[0] - nn[0] * w * .7, q[1] - nn[1] * w * .7); ctx.quadraticCurveTo(q[0] + d[0] * .05, q[1] + d[1] * .05, q[0] + nn[0] * w * .7, q[1] + nn[1] * w * .7); ctx.stroke(); }
    ctx.restore();
    const [fx, fy] = jointPt(ctx, M, J.AF.wr), L = 13 * s;
    ctx.save(); ctx.translate(fx + dir * L * .35, fy + 1.5 * s); ctx.scale(dir, 1); ctx.rotate(.35); ctx.fillStyle = STY.red.fill; ctx.strokeStyle = C.ink; ctx.lineWidth = .6 * s; ctx.lineJoin = 'round';
    ctx.beginPath(); ctx.moveTo(-L * .6, 0); ctx.quadraticCurveTo(0, -L * .32, L * .45, -L * .06); ctx.lineTo(L * .75, -L * .3); ctx.lineTo(L * .66, 0); ctx.lineTo(L * .75, L * .3); ctx.lineTo(L * .45, L * .06); ctx.quadraticCurveTo(0, L * .32, -L * .6, 0); ctx.closePath(); ctx.fill(); ctx.stroke();
    ctx.lineWidth = .35 * s; ctx.beginPath(); ctx.moveTo(-L * .3, -L * .14); ctx.quadraticCurveTo(-L * .24, 0, -L * .3, L * .14); for (let k = 0; k < 3; k++) { ctx.moveTo(-L * .1 + k * L * .15, -L * .1); ctx.lineTo(k * L * .15, 0); ctx.lineTo(-L * .1 + k * L * .15, L * .1); } ctx.stroke();
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(-L * .45, -L * .04, .5 * s, 0, TAU); ctx.fill(); ctx.restore(); }
  if (J) { const hornB = (dx) => jointPt(ctx, M, add(J.neckT, rot([dx, -12.6], J.headA)));
    ctx.save(); ctx.fillStyle = '#EBD9B4'; ctx.strokeStyle = C.ink; ctx.lineWidth = .5 * s; ctx.lineJoin = 'round';
    for (const [dx, k] of [[1.8, 1], [-1.2, .8]]) { const [bx, by] = hornB(dx), L = 5.2 * s * k;
      ctx.beginPath(); ctx.moveTo(bx - 1.1 * s, by); ctx.quadraticCurveTo(bx - dir * 2.4 * s * k, by - L * .7, bx + dir * 1.4 * s * k, by - L); ctx.quadraticCurveTo(bx - dir * .6 * s * k, by - L * .55, bx + 1.1 * s, by); ctx.closePath(); ctx.fill(); ctx.stroke(); }
    ctx.restore(); }
  // kuyruk: belden aşağı inip arkaya kıvrılır; pullar ve iki loblu yüzgeç
  const sw = Math.sin(t * 1.6) * 2.2, P = [[0, -2], [-1 * dir, 12], [-7 * dir, 24 + sw * .3], [-19 * dir, 28 + sw * .6], [-31 * dir, 22 + sw], [-38 * dir, 12 + sw]].map(q => [x + q[0] * s, y + q[1] * s]);
  const Wd = [8.6, 8.2, 7, 5.2, 3.4, 1.8].map(v => v * s);
  const L = [], R = [];
  for (let i = 0; i < P.length; i++) { const a = P[Math.max(0, i - 1)], b = P[Math.min(P.length - 1, i + 1)], d = sub(b, a), n = scl([-d[1], d[0]], 1 / (len(d) || 1)); L.push(add(P[i], scl(n, Wd[i]))); R.push(add(P[i], scl(n, -Wd[i]))); }
  ctx.save(); ctx.lineJoin = 'round';
  ctx.beginPath(); spline(ctx, [...L, ...R.reverse()], true, .9); ctx.fillStyle = STY.red.fill; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 1.1 * s; ctx.stroke();
  ctx.strokeStyle = 'rgba(14,9,7,.75)'; ctx.lineWidth = .45 * s;
  for (let i = 1; i < P.length - 1; i++) for (let k = -1; k <= 1; k++) { const q = lerp2(P[i], P[i + 1], .5); ctx.beginPath(); ctx.arc(q[0] + k * 2.6 * s * .5, q[1] + k * 2.6 * s, 2.2 * s, 0, PI); ctx.stroke(); }
  const E1 = P[P.length - 1]; ctx.fillStyle = STY.red.fill; ctx.lineWidth = 1 * s; ctx.strokeStyle = C.ink;
  for (const sg of [-1, 1]) { ctx.beginPath(); ctx.moveTo(...E1); ctx.quadraticCurveTo(E1[0] - dir * 4 * s, E1[1] + sg * 9 * s, E1[0] - dir * 12 * s, E1[1] + sg * 11 * s); ctx.quadraticCurveTo(E1[0] - dir * 7 * s, E1[1] + sg * 3 * s, E1[0], E1[1]); ctx.fill(); ctx.stroke(); }
  ctx.restore();
  return J ? jointPt(ctx, M, add(J.neckT, rot([5, -3.5], J.headA))) : [x, y - 50 * s];
}
// vazo haritası: kara kil, denizler sır siyahı, boğazlar dar sır yarıkları (dünya birimi; kamera dışarıdan)
// Karadeniz yatay (kuzeyinde Kırım yarımadası), kuzeydoğuda Azak, güneybatıda Marmara; boğazlar kısa ve kavisli çoklu çizgi
const H_SEAS = [[1486, 802, 903, 264, 3], [2010, 365, 240, 100, 7], [604, 1080, 118, 70, 11]];
const H_STR = { kerc: [[1815, 405], [1765, 476], [1727, 552]], ist: [[676, 1046], [708, 992], [762, 960]] };
const H_CRIMEA = [[1475, 470], [1530, 470], [1548, 560], [1606, 596], [1706, 572], [1690, 612], [1630, 628], [1606, 690], [1524, 744], [1432, 712], [1366, 676], [1330, 628], [1392, 618], [1452, 590]];
// İo'nun yolu: kayadan (İskit) doğuya, Kırım'ın kuzeyinden Kerç'i batıdan doğuya geçer, Kafkasya'ya
const H_ROUTE = [[1360, 330], [1470, 400], [1560, 452], [1660, 500], [1752, 500], [1860, 520], [2060, 560], [2280, 580], [2470, 560]];
function H_seaPath(c, s) { const [x, y, rx, ry, sd] = s; c.beginPath(); for (let k = 0; k <= 90; k++) { const a = k / 90 * TAU, w = 1 + .06 * noise1(a * 2.2, sd) + .035 * Math.sin(a * 7 + sd); const px = x + Math.cos(a) * rx * w, py = y + Math.sin(a) * ry * w; k ? c.lineTo(px, py) : c.moveTo(px, py); } c.closePath(); }
function H_map(ctx, t, o = {}) {
  ctx.fillStyle = '#B9663A'; ctx.fillRect(-2000, -2000, 7000, 6000);
  for (let i = 0; i < 260; i++) { const r = rng(i + 5); ctx.fillStyle = `rgba(90,40,20,${.08 + r() * .08})`; ctx.beginPath(); ctx.arc(-300 + r() * 3600, -200 + r() * 1900, 2 + r() * 5, 0, TAU); ctx.fill(); }
  // Skythia'daki kaya (Prometheus): küçük sır tepeler
  ctx.fillStyle = PC.glaze; ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(1360, 300); ctx.lineTo(1420, 200); ctx.lineTo(1450, 240); ctx.lineTo(1490, 170); ctx.lineTo(1560, 300); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(1490, 170); ctx.lineTo(1500, 230); ctx.moveTo(1420, 200); ctx.lineTo(1428, 250); ctx.stroke();
  ctx.lineCap = 'round';
  const strait = (w, col) => { for (const k in H_STR) { const P = H_STR[k]; ctx.strokeStyle = col; ctx.lineWidth = w; ctx.lineJoin = 'round'; ctx.beginPath(); ctx.moveTo(...P[0]); ctx.quadraticCurveTo(...P[1], ...P[2]); ctx.stroke(); } };
  strait(58, C.ink);
  for (const s of H_SEAS) { H_seaPath(ctx, s); ctx.fillStyle = PC.glaze; ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 8; ctx.stroke(); }
  strait(44, PC.glaze);
  // Kafkasya: doğu kıyısında sır tepeler, kil kazıma sırtlar
  for (const [px, py, h] of [[2440, 640, 150], [2540, 600, 210], [2640, 650, 160], [2590, 520, 120]]) { ctx.fillStyle = PC.glaze; ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(px - 90, py + 40); ctx.lineTo(px, py - h + 40); ctx.lineTo(px + 90, py + 40); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.strokeStyle = PC.clayR; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(px, py - h + 40); ctx.lineTo(px + 18, py - h * .4 + 40); ctx.stroke(); }
  // dalga çizgileri: her denizin içinde kıpırdayan kil çizgileri, boğazlarda kısa akıntı çizgileri
  for (const s of H_SEAS) { ctx.save(); H_seaPath(ctx, s); ctx.clip(); ctx.strokeStyle = 'rgba(201,112,63,.45)'; ctx.lineWidth = 3;
    for (let yy = s[1] - s[3]; yy < s[1] + s[3]; yy += 46) { ctx.beginPath(); for (let xx = s[0] - s[2]; xx <= s[0] + s[2]; xx += 24) { const wy = yy + Math.sin(xx * .03 + t * 1.4 + yy) * 6; xx > s[0] - s[2] ? ctx.lineTo(xx, wy) : ctx.moveTo(xx, wy); } ctx.stroke(); }
    ctx.restore(); }
  // Kırım: kuzeyden inen kil yarımada (denizin üstünde)
  // dolgu kıyı çizgisini örter (berzah kara ile birleşir); kontur yalnız denizin içinde
  ctx.fillStyle = '#B9663A'; ctx.beginPath(); spline(ctx, H_CRIMEA, true, .45); ctx.fill();
  ctx.save(); H_seaPath(ctx, H_SEAS[0]); ctx.clip(); ctx.strokeStyle = C.ink; ctx.lineWidth = 8; ctx.lineJoin = 'round'; ctx.beginPath(); spline(ctx, H_CRIMEA, true, .45); ctx.stroke(); ctx.restore();
  // antik adlar (dipinto): ülke adı yok
  if ((o.z || 1) < 1.5) for (const [n, x, y] of [['ΣΚΥΘΙΑ', 980, 300], ['ΚΑΥΚΑΣΟΣ', 2530, 1000], ['ΕΥΡΩΠΗ', 420, 930], ['ΑΣΙΑ', 1340, 1230]]) dipinto(ctx, n, x, y, 64, { col: C.ink });
  // İo'nun yolu: eklenmiş beyaz toynak izleri (çift nokta, eşit aralık); ucunda madalyon içinde boynuzlu kız profili
  const rp = o.route || 0;
  if (rp > 0) { const seg = H_ROUTE.slice(1).map((q, i) => len(sub(q, H_ROUTE[i]))), tot = seg.reduce((a, b) => a + b, 0), at = d => { let k = 0; while (k < seg.length - 1 && d > seg[k]) { d -= seg[k]; k++; } return [lerp2(H_ROUTE[k], H_ROUTE[k + 1], clamp(d / seg[k])), sub(H_ROUTE[k + 1], H_ROUTE[k])]; };
    const step = 30, n = Math.floor(tot * rp / step);
    ctx.fillStyle = C.white; ctx.strokeStyle = 'rgba(14,9,7,.6)'; ctx.lineWidth = 1.5;
    for (let k = 0; k <= n; k++) { const [q, d] = at(k * step), nn = scl([-d[1], d[0]], 1 / (len(d) || 1)), sg = k % 2 ? 1 : -1; ctx.beginPath(); ctx.arc(q[0] + nn[0] * 7 * sg, q[1] + nn[1] * 7 * sg, 6.5, 0, TAU); ctx.fill(); ctx.stroke(); }
    const [tip] = at(tot * rp);
    // madalyon yolun ucunun üstünde (Kerç'in kanalını örtmez); kadrajın tepesine yaklaşınca yana kayar
    if (o.head !== false) { const hy = tip[1] - 238, top = hy < 210; H_ioMapHead(ctx, tip[0] + (top ? 170 : 0), top ? 230 : hy, 8.4, t); } }
}
// haritada İo: madalyon içinde P200'deki boynuzlu kız profili (kırmızı figür, sır zemin)
function H_ioMapHead(ctx, x, y, s, t) {
  const lk = { ...LK.io, rf: true, earHidden: true }, sty = { ...STY.red, white: STY.red.fill }, p = { torso: 0, neck: .08, head: .05, breath: 0 };
  let J = null, M = null;
  figure(ctx, { x: 0, y: 0, s, dir: 1, sty, lk, seed: 61, still: true, p, alpha: 0, onJoints: (j, m) => { J = j; M = m; } });
  const h = jointPt(ctx, M, add(J.neckT, rot([1, -6], J.headA))), R = 15 * s;
  ctx.save(); ctx.fillStyle = PC.glaze; ctx.strokeStyle = C.ink; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(x, y, R, 0, TAU); ctx.fill(); ctx.stroke();
  ctx.strokeStyle = PC.clayR; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(x, y, R - 8, 0, TAU); ctx.stroke();
  ctx.beginPath(); ctx.arc(x, y, R - 11, 0, TAU); ctx.clip();
  let J2 = null, M2 = null;
  figure(ctx, { x: x - h[0], y: y - h[1] + 3 * s, s, dir: 1, sty, lk, seed: 61, still: true, p, stripe: .4, onJoints: (j, m) => { J2 = j; M2 = m; } });
  if (J2) H_horns(ctx, J2, M2, s);
  ctx.restore();
}
function H_ioHead(ctx, x, y, s, t) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.ellipse(-6, 4, 16, 22, .3, 0, TAU); ctx.fill();
  ctx.fillStyle = STY.red.fill; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.beginPath(); ctx.ellipse(4, 0, 14, 17, 0, 0, TAU); ctx.fill(); ctx.stroke();
  ctx.lineCap = 'round'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(0, -14); ctx.quadraticCurveTo(-4, -30, -16, -34); ctx.moveTo(8, -15); ctx.quadraticCurveTo(8, -30, -2, -36); ctx.stroke();
  ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(10, -2, 2.4, 0, TAU); ctx.fill();
  ctx.restore();
}
// yüzen inek: profil, bacakları su çizgisinin altında (sır + dalga)
function H_cowSwim(ctx, x, y, s, t, dir = 1) {
  const bob = Math.sin(t * 2.6) * 3 * s, wl = u => y + Math.sin(u * 22 + t * 4) * 2.5 * s;
  ctx.save(); ctx.beginPath(); ctx.moveTo(x - 140 * s, y - 200 * s); ctx.lineTo(x + 140 * s, y - 200 * s);
  for (let u = 1; u >= 0; u -= .04) ctx.lineTo(x + (u - .5) * 280 * s, wl(u)); ctx.closePath(); ctx.clip();
  cow(ctx, x, y + 34 * s + bob, s, dir, t * .9, { col: STY.red.fill, inc: C.ink, walk: .6 });
  ctx.restore();
  ctx.save(); ctx.lineCap = 'round';
  ctx.strokeStyle = 'rgba(242,214,170,.8)'; ctx.lineWidth = 1.8 * s; ctx.beginPath(); for (let u = .15; u <= .85; u += .03) { const xx = x + (u - .5) * 280 * s; u > .15 ? ctx.lineTo(xx, wl(u)) : ctx.moveTo(xx, wl(u)); } ctx.stroke();
  for (let k = 1; k <= 3; k++) { ctx.strokeStyle = `rgba(242,214,170,${.5 / k})`; ctx.lineWidth = 1.4 * s; ctx.beginPath(); ctx.ellipse(x - dir * (30 + k * 34) * s, y + (3 + k * 2) * s, (26 + k * 20) * s, 4 * s, 0, PI * .1, PI * .9); ctx.stroke(); }
  ctx.restore();
}
// yandan boğaz geçidi (kırmızı figür friz): iki kil kıyı, aradaki su; inek soldan sağa yüzer. u: geçişin ilerleyişi
function H_crossing(ctx, t, u, o = {}) {
  glazeBG(ctx, t, { gx: 960, gy: 640, gr: 1100, stars: false, warm: o.warm || 'rgba(150,62,28,.42)' });
  const wy = 700;
  ctx.save(); cam(ctx, o.c || { x: 960, y: 540, z: 1 }, 1);
  const bank = (pts, sd) => { ctx.fillStyle = STY.red.fill; ctx.strokeStyle = C.ink; ctx.lineWidth = 5; ctx.beginPath(); spline(ctx, pts, true, .8); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = 'rgba(14,9,7,.5)'; ctx.lineWidth = 2.5; for (let k = 0; k < 5; k++) { const r = rng(sd + k), x = pts[1][0] + (pts[2][0] - pts[1][0]) * r(), y = wy - 40 - r() * 150; ctx.beginPath(); ctx.arc(x, y, 18 + r() * 26, PI * 1.1, PI * 1.9); ctx.stroke(); } };
  // kıyılar: suya eğimle iner (dibi su çizgisinin altında kalır); su önden kıyı eteklerini örter
  bank([[-200, 1000], [-200, 470], [260, 430], [520, 600], [640, wy + 60], [560, 1000]], 3);
  bank([[1380, 1000], [1290, wy + 60], [1420, 590], [1700, 400], [2200, 420], [2200, 1000]], 9);
  ctx.fillStyle = PC.glaze; ctx.beginPath(); ctx.moveTo(-200, 1300); for (let x = -200; x <= 2200; x += 20) ctx.lineTo(x, wy + 22 + Math.sin(x * .02 + t * 1.6) * 4); ctx.lineTo(2200, 1300); ctx.closePath(); ctx.fill();
  ctx.strokeStyle = 'rgba(201,112,63,.5)'; ctx.lineWidth = 3;
  for (let k = 0; k < 6; k++) { ctx.beginPath(); for (let x = -200; x <= 2200; x += 16) { const y = wy + 46 + k * 46 + Math.sin(x * .028 + t * 2 + k) * 6; x > -200 ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); }
  const x = lerp(470, 1460, u);
  H_cowSwim(ctx, x, wy + 18, o.s || 5.2, t, 1);
  ctx.restore();
}
// ovadaki insanlar ve göğüslerindeki soluk umut ışıkları (ELPİS)
function H_plain(ctx, t, lt, lights = 1) {
  glazeBG(ctx, t, { gx: 960, gy: 900, gr: 900, stars: false, warm: 'rgba(150,62,28,.4)' });
  ctx.save(); cam(ctx, { x: 960 + lt * 6, y: 540, z: 1.0 }, 1);
  const gy = 820; ctx.strokeStyle = 'rgba(201,112,63,.6)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(-200, gy); ctx.lineTo(2200, gy); ctx.stroke();
  glow(ctx, 960, gy - 40, 380, 'rgba(255,170,80,.3)'); flame(ctx, 960, gy, 1.5, t, { haloR: 200 }); ctx.fillStyle = PC.clayR; ctx.fillRect(920, gy - 4, 80, 10);
  for (let i = 0; i < 6; i++) { const x = 380 + i * 230 + (i > 2 ? 120 : 0), dir = x < 960 ? 1 : -1;
    H_rf(ctx, x, gy, 3.8, dir, i % 2 ? LK.humanF : LK.human, { torso: .1, head: .05 }, { sty: { ...STY.red, white: STY.red.fill } });
    const fl = .75 + .25 * noise1(t * 3 + i * 7, 4), hx = x + dir * 8, hy = gy - 245;
    if (lights > 0) { glow(ctx, hx, hy, 60, `rgba(205,218,235,${.4 * fl * lights})`); ctx.fillStyle = `rgba(226,234,242,${.9 * fl * lights})`; ctx.beginPath(); ctx.arc(hx, hy, 8 * fl, 0, TAU); ctx.fill(); } }
  ctx.restore();
}
// söz anında Okeanos ile Prometheus'un ikili planı
const H_IKI = { x: 880, y: 600, z: 1.3 };
const H_OKX = 600;
const H_scr = (c, p) => [(p[0] - c.x) * c.z + W / 2, (p[1] - c.y) * c.z + H / 2];

// --- P186: bölüm kartı; bir inek silueti bir boğazı yüzerek geçer (merak: hangi boğaz?) ---
shot(PA('P186'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  H_crossing(ctx, t, E.io2(clamp((lt - .8) / (st.d - 1.2))), { c: { x: 960 + lt * 4, y: 560, z: 1.06 - lt * .004 }, s: 4.6, warm: 'rgba(170,70,30,.5)' });
  kayaFrame(ctx, t);
}, { tr: { type: 'clay', dur: .8, end: true }, post: { tex: .6, vig: 1, grain: .06 },
  over: (ctx, st) => chapterCard(ctx, 'BÖLÜM VII', 'TANIKLAR VE “İNEK GEÇİDİ”', st.lt - .15, 3.3, { y: 170 }) });

// --- P187–P190: sayfa: Zeus'un evreni; boş tahtın çevresinde üç küme; hepsi domino gibi tahta eğilir; tek dik kalan Prometheus; tanık listesi ---
const H_UNI = [ // [x, yön, görünüş, küme, gönüllü mü]
  [230, 1, LK.humanF, 0, 0], [330, 1, LK.human, 0, 0], [430, 1, LK.io, 0, 0],
  [600, 1, LK.kratos, 1, 1], [700, 1, LK.bia, 1, 1], [800, 1, LK.hephaistos, 1, 0],
  [1130, -1, { beard: 'full', hair: 'long', garment: 'robe' }, 2, 1],
];
shot(PA('P187'), (ctx, st) => {
  const t = st.t, lt = st.lt, tH = A('H02@hepsi'), tT = A('H02@tek'), tU = A('H02@uşakları#1');
  // itme: eğilişte kümelere (z 1,6), 'tek'te dik kalan Prometheus'a (z 1,8; alıntının altında): jest taşıyan figürler ≥ 480 px
  const c = F_cam(t, [[PA('P187'), { x: 900, y: 540, z: 1.0 }], [tH, { x: 760, y: 560, z: 1.6 }], [tT, { x: 1400, y: 520, z: 1.8 }], [tU + .2, { x: 2200, y: 520, z: 1.0 }]], 1.0, 3);
  ctx.save(); cam(ctx, c, 1);
  ctx.save(); ctx.translate(c.x - W / 2, c.y - H / 2); paperBG(ctx, t, { book: false, seed: 77 }); ctx.restore();
  const gy = 700;
  inkPoly(ctx, [[120, gy], [1560, gy]], ramp(lt, 0, 1.2), { w: 3, jit: .6 });
  // boş taht: mürekkep, ortada
  ctx.save(); ctx.globalAlpha = ramp(lt, .3, 1.0); throne(ctx, 965, gy, 2.4, -1, PW.line, PW.paper, { high: true }); ctx.restore();
  // kümeler: sırayla çizilir; H02@hepsi'den sonra tahta doğru domino gibi eğilir (kimi isteyerek: derin ve çabuk; kimi istemeyerek: sığ ve geç)
  const draw = [A('H02@kurbanları'), A('H02@uşakları'), A('H02@dalkavuklarıyla')];
  H_UNI.forEach(([x, dir, lk, k, will], i) => {
    const a = ramp(t, draw[k] - .2, draw[k] + .4); if (a <= 0) return;
    const del = (1 - Math.abs(x - 965) / 800) * .9 + (will ? 0 : .5), b = E.out2(ramp(t, tH + del, tH + del + (will ? .5 : 1.1))) * (will ? 1 : .55);
    ctx.save(); ctx.globalAlpha = a; H_lek(ctx, x, gy, 3.2, dir, lk, { torso: .55 * b, neck: .25 * b, head: .2 * b, shN: .2 + .3 * b, elN: .4 }); ctx.restore();
  });
  // Prometheus: ayrı, sağda; eğilmez; H02@tek'te kırmızı vurgu
  const pr = ramp(t, A('H02@hepsi') - .4, A('H02@hepsi') + .2), red = ramp(t, tT, tT + .4);
  if (pr > 0) { ctx.save(); ctx.globalAlpha = pr; H_lek(ctx, 1430, gy, 3.4, -1, LK.promFree, { torso: -.05, neck: -.1, head: -.12 }, { sty: red > .5 ? { ...STY.lek, line: PW.red, cut: PW.red } : STY.lek }); ctx.restore();
    if (red > 0) circleMark(ctx, 1430, gy - 140, 110, 170, ramp(t, tT + .1, tT + .9)); } // elips kaynak satırının altında kalır
  // küme adları
  [['kurbanlar', 330, 0], ['uşaklar', 700, 1], ['dalkavuk', 1130, 2]].forEach(([s, x, k]) => txt(ctx, s, x, 345, { font: 'italic 600 54px "Cormorant Garamond"', col: PW.line, a: ramp(t, draw[k], draw[k] + .5) * (1 - ramp(t, tT - .4, tT + .1)) }));
  // tanık listesi: sayfanın sağ kenarında
  const lx = 1940, l0 = ramp(t, tU - .4, tU + .3);
  if (l0 > 0) { ctx.save(); ctx.globalAlpha = l0;
    txt(ctx, 'TANIKLAR', lx, 330, { font: '700 56px Cinzel', col: PW.line, align: 'left', ls: 6 });
    inkPoly(ctx, [[lx, 372], [lx + 560, 372]], l0, { w: 3, jit: .5 });
    const rows = ['KRATOS', 'BİA', 'HEPHAİSTOS', 'OKEANOS', 'PERİLER', 'İO'], ck = [0, .3, .6].map(d => A('H02@gördük') + d);
    rows.forEach((s, i) => { const y = 430 + i * 58; txt(ctx, s, lx, y, { font: '600 46px Cinzel', col: PW.line, align: 'left', ls: 3 });
      if (i < 3) inkPoly(ctx, [[lx + 420, y - 4], [lx + 438, y + 16], [lx + 476, y - 30]], ramp(t, ck[i], ck[i] + .3, E.lin), { col: PW.red, w: 6, jit: .3 });
      if (i === 3) circleMark(ctx, lx + 125, y, 160, 34, ramp(t, A('H02@dalkavuk#1'), A('H02@dalkavuk#1') + .6));
      if (i === 5) { ctx.save(); ctx.translate(lx + 120, y - 6); ctx.strokeStyle = PW.line; ctx.lineWidth = 4; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(0, 10); ctx.quadraticCurveTo(-4, -14, -18, -18); ctx.moveTo(14, 10); ctx.quadraticCurveTo(18, -14, 32, -18); ctx.stroke(); ctx.restore(); txt(ctx, '?', lx + 175, y, { font: '700 46px Cinzel', col: PW.red }); }
    }); ctx.restore(); }
  ctx.restore();
}, { tr: { type: 'ink', dur: .6, end: true }, post: { tex: .35, vig: .55, grain: .045 },
  over: (ctx, st) => {
    const t = st.t, q = A('H02@tek');
    erhatTag(ctx, t - A('H02'), 'ERHAT · ZEUS’UN EVRENİ · S. XIV', { d: A('H02@hepsi') - A('H02') });
    if (t > q - .2) { ctx.save(); ctx.globalAlpha = 1 - ramp(t, A('H02@sırada') - .1, A('H02@sırada') + .4); quoteCard(ctx, 'Tek başkaldıran Prometheus’tur.', 'A. ERHAT · ÖNSÖZ · S. XIII', 820, 160, 1300, t - q, { font: 'italic 500 80px "Cormorant Garamond"', lh: 90 }); ctx.restore(); }
  } });

// --- P191–P194: sert kesme: Okeanos dalga kuşağından yükselir; öğüt verir (KENDİNİ BİL · DİLİNE SAHİP OL); Prometheus'un alayı; Okeanos rahatlayıp dalgaya batar ---
shot(PA('P191'), (ctx, st) => {
  const t = st.t, lt = st.lt, tO = A('H04@okeanos'), tK = A('H04@kendini'), tP = A('H04@prometeus'), tB = A('H04@kendi#1');
  const c = F_cam(t, [[PA('P191'), { ...CAMS.genis, x: 820, y: 600 }], [tK - .3, H_IKI], [tP, { ...G_YK, z: 3.0 }], [tB - .05, { ...H_IKI, z: 1.25 }]], .8, 3);
  const { wind } = kayaWorld(ctx, t, c, { sky: H_SKY });
  ctx.save(); cam(ctx, c, 1);
  const up = E.out3(ramp(t, tO - .4, tO + 1.4)) * (1 - E.in2(ramp(t, tB + .3, tB + 1.8)));
  const wag = ramp(t, tK - .1, tK + .3) * (1 - ramp(t, tK + 1.6, tK + 2.0)) + ramp(t, A('H04@diline') - .1, A('H04@diline') + .3) * (1 - ramp(t, A('H04@ol') + .4, A('H04@ol') + .8));
  if (up > 0) { const m = H_okeanos(ctx, H_OKX, lerp(1180, 730, up), 5.0, t, { shN: lerp(.3, 2.2, wag) + Math.sin(t * 9) * .12 * wag, elN: lerp(.8, .5, wag), handN: wag > .3 ? 'point' : 'open', torso: lerp(.05, -.12, ramp(t, tB, tB + .6)) });
    window.H_OKM = H_scr(c, m); }
  promChained(ctx, t, { wind, look: t > tP && t < tB ? .05 : -.08, pose: t > tP && t < tB ? 'alay' : 'direnis', p: t > tP && t < tB ? { head: -.15 + .1 * Math.sin(ramp(t, tP + .3, tP + 1.6) * PI) } : {} });
  ctx.restore();
  // dalga kuşağından yükseliş: köpük
  if (up > 0 && up < 1) { ctx.save(); cam(ctx, c, 1); ctx.strokeStyle = `rgba(242,214,170,${.6 * (1 - up)})`; ctx.lineWidth = 4; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.ellipse(H_OKX, 900 - k * 10, 120 + k * 50 + up * 60, 14, 0, 0, TAU); ctx.stroke(); } ctx.restore(); }
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tO = A('H04@okeanos');
    H_tanik(ctx, t, 'OKEANOS', tO);
    const n = ramp(t, tO + .4, tO + 1.0) * (1 - ramp(t, A('H04@kendini') - .4, A('H04@kendini')));
    if (n > 0) dipinto(ctx, 'ΩΚΕΑΝΟΣ', 520, 560, 54, { col: PC.clayRL, a: n });
    const m = window.H_OKM || [700, 380], sea = '#EBD9B4'; // deniz sesleri: sıcak krem (Zeus'un soğuk beyazından ayrı)
    const k1 = A('H04@kendini'), k2 = A('H04@diline'), fa = 1 - ramp(t, A('H04@prometeus') - .3, A('H04@prometeus'));
    if (t > k1 && fa > 0) { ctx.save(); ctx.globalAlpha = fa; speechFlow(ctx, 'KENDİNİ BİL', u => [lerp(m[0] + 30, m[0] + 520, u), m[1] - 40 - Math.sin(u * PI) * 40], ramp(t, k1, A('H04@bil') + .4, E.lin), { font: '700 60px Cinzel', col: sea, glow: 'rgba(110,52,22,.65)' });
      if (t > k2) speechFlow(ctx, 'DİLİNE SAHİP OL', u => [lerp(m[0] + 30, m[0] + 640, u), m[1] + 50 - Math.sin(u * PI) * 30], ramp(t, k2, A('H04@ol') + .4, E.lin), { font: '700 56px Cinzel', col: sea, glow: 'rgba(110,52,22,.65)' }); ctx.restore(); }
    const s1 = A('H04@seni'), fb = 1 - ramp(t, A('H04@kendi#1') - .1, A('H04@kendi#1') + .3);
    if (t > s1 && fb > 0) { ctx.save(); ctx.globalAlpha = fb; speechFlow(ctx, 'SENİ KISKANIYORUM', u => [lerp(800, 60, u), 380 - Math.sin(u * PI) * 40], ramp(t, s1, A('H04@kıskanıyorum') + .5, E.lin), { font: '700 60px Cinzel' }); ctx.restore(); }
  } });

// --- P195–P197: periler konuşur (Yunanca söz denizden kayaya akar); kenar şeridi: “dilin fazla özgür”; GURUR? KİBİR? etiketleri üstü çizilir; BİLİNÇ parlar, söz zinciri çözülür ---
shot(PA('P195'), (ctx, st) => {
  const t = st.t, lt = st.lt, tB = A('H05@başkaları'), tO = A('H05@oysa');
  const c = F_cam(t, [[PA('P195'), { x: 640, y: 600, z: 1.3 }], [tB, { x: 1180, y: 480, z: 1.4 }], [tO, { x: 1170, y: 470, z: 1.5 }]], 1.0, 3);
  const { wind } = kayaWorld(ctx, t, c, { sky: H_SKY });
  ctx.save(); cam(ctx, c, 1);
  G_nymphs(ctx, t, 1, { wind });
  promChained(ctx, t, { wind, look: t < tB ? .08 : -.05, pose: t > tO ? 'direnis' : 'sessiz', p: t > tO ? { blink: 0 } : {} });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tP = A('H05'), tE = A('H05@erhata'), tB = A('H05@başkaları'), tO = A('H05@oysa');
    H_tanik(ctx, t, 'PERİLER', tP, 2.6);
    // perilerin sözü: Yunanca, denizden kayaya doğru akar
    const g = ramp(t, A('H05@ona'), A('H05@der') + .3, E.lin);
    if (g > 0) { ctx.save(); ctx.globalAlpha = 1 - ramp(t, tB - .4, tB); speechFlow(ctx, 'ΑΓΑΝ ΕΛΕΥΘΕΡΟΣΤΟΜΕΙΣ', u => [lerp(560, 1500, u), 470 - Math.sin(u * PI) * 110], g, { font: '600 54px Cinzel', col: '#EBD9B4', glow: 'rgba(110,52,22,.65)' }); ctx.restore(); }
    erhatStrip(ctx, t - tE, tB - tE - .3, '“dilin fazla özgür”', 'xiii');
    erhatStrip(ctx, t - tB, tO - tB - .2, '“hiçbir umuda yer vermeden”', 'xii');
    erhatStrip(ctx, t - tO, st.end - tO - .4, 'bilinç = özgürlük', 'xiii', { icon: (c, p) => { const k = ramp(t, A('H05@bilincidir'), A('H05@bilincidir') + .6); c.save(); c.globalAlpha = p; glow(c, 0, 20, 70, `rgba(255,200,120,${.6 * k})`); c.strokeStyle = mixCol(PW.line, '#E8A04C', k); c.lineWidth = 8; const o = 22 * k; c.beginPath(); c.ellipse(-30 - o, 20, 28, 40, 0, PI * .55, PI * 2.45); c.stroke(); c.beginPath(); c.ellipse(30 + o, 20, 28, 40, 0, -PI * .45, PI * 1.45); c.stroke(); c.restore(); } });
    // başkalarının adlandırması: GURUR? KİBİR? belirir, üstü çizilir
    [['GURUR?', 430, 470, A('H05@gurur')], ['KİBİR?', 560, 600, A('H05@kibir')]].forEach(([s, x, y, t0]) => {
      const a = ramp(t, t0 - .1, t0 + .3) * (1 - ramp(t, tO + 1.2, tO + 1.8)); if (a <= 0) return;
      txt(ctx, s, x, y, { font: '700 76px Cinzel', col: '#F1E4C8', a, ls: 6, shadow: 'rgba(0,0,0,.8)', blur: 12 });
      ctx.save(); ctx.globalAlpha = a; strike(ctx, x - 170, y + 4, x + 170, y - 6, ramp(t, tO - .1, tO + .5, E.lin), { col: '#D9583A', w: 8 }); ctx.restore(); });
    // söz zinciri: ağzın önünde üç halka; H05@oysa'da ortadaki halka açılır, Yunanca 'özgür' harfleri serbest kalır
    const ch = ramp(t, tO - .3, tO + .2) * (1 - ramp(t, st.end - .6, st.end)); if (ch > 0) {
      const op = E.out3(ramp(t, A('H05@özgürlüğü') - .2, A('H05@özgürlüğü') + .5));
      ctx.save(); ctx.globalAlpha = ch; ctx.lineWidth = 12; ctx.strokeStyle = mixCol(PC.clayR, PC.glaze, .35);
      ctx.lineWidth = 16; for (let k = 0; k < 3; k++) { const x = 790 - k * 96 - (k === 2 ? op * 80 : 0), y = 420 + (k === 2 ? op * 50 : 0) - (k === 0 ? op * 30 : 0), r = k === 1 ? op * .9 : 0; ctx.save(); ctx.translate(x, y); ctx.rotate(r + (k % 2 ? PI / 2 : 0) * (1 - op)); ctx.strokeStyle = C.ink; ctx.beginPath(); ctx.ellipse(0, 0, 56, 30, 0, k === 1 ? op * 1.2 : 0, TAU - (k === 1 ? op * 1.2 : 0)); ctx.stroke(); ctx.strokeStyle = mixCol(PC.clayR, PC.glaze, .2); ctx.lineWidth = 5; ctx.stroke(); ctx.lineWidth = 16; ctx.restore(); }
      if (op > 0) speechFlow(ctx, 'ΕΛΕΥΘΕΡΟΣ', u => [lerp(700, 150, u), 400 - u * 90 - Math.sin(u * PI) * 40], op, { font: '600 60px Cinzel' });
      ctx.restore(); }
  } });

// --- P198–P199: sert kesme: ovada göğüslerinde soluk umut ışıklarıyla insanlar; kayada ışığı olmayan tek figür: Prometheus, ovanın ateş yansımasıyla aydınlanır, gözleri açık ---
shot(PA('P198'), (ctx, st) => H_plain(ctx, st.t, st.lt, ramp(st.t, A('H05b@kör') - .3, A('H05b@umutlar'))), { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });
shot(PA('P199'), (ctx, st) => {
  const t = st.t, lt = st.lt, tG = A('H05b@görüyordu');
  const c = { ...CAMS.orta, x: 1240 - lt * 3, z: 1.55 + lt * .03 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'gunbatimi', fires: true, fireA: 1 });
  ctx.save(); cam(ctx, c, 1);
  // ovanın ateş yansıması: soldan alttan gelen sıcak, titrek ışık
  const fl = .7 + .3 * noise1(t * 2.6, 9); glow(ctx, 1050, 760, 520, `rgba(255,150,70,${.22 * fl})`);
  promChained(ctx, t, { wind, look: lerp(0, -.12, ramp(t, tG - .3, tG + .6)), pose: 'direnis', p: { blink: t > tG - .3 ? 0 : undefined } });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P200: İo koşarak gelir: boynuzlu genç kız, atsineği vızıldar; ΙΩ ---
shot(PA('P200'), (ctx, st) => {
  const t = st.t, lt = st.lt, tI = A('H06@iyo');
  const c = { ...CAMS.genis, x: 860 + lt * 6, y: 560, z: 1.05 };
  const { wind } = kayaWorld(ctx, t, c, { sky: 'gunbatimi' });
  ctx.save(); cam(ctx, c, 1);
  const x = lerp(-120, 760, E.out2(ramp(t, PA('P200'), A('H06@kız') + .6, E.lin))), run = 1 - ramp(t, A('H06@kız'), A('H06@kız') + .8);
  window.H_IOP = H_io(ctx, x, 868, 4.6, t, { run: run > .05 ? run : 0, dir: 1, p: run < .05 ? { torso: .1, head: -.1 } : {} });
  promChained(ctx, t, { wind, look: .12 * ramp(t, A('H06@boynuzlu'), A('H06@boynuzlu') + .8) });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const t = st.t, tI = A('H06@iyo'); H_tanik(ctx, t, 'İO', A('H06@kurban'), 3.2); const a = ramp(t, tI, tI + .5); if (a > 0) dipinto(ctx, 'ΙΩ', 620, 430, 64, { col: PC.clayRL, a }); } });

// --- P201: madalyon (kadraj boyunun %80'i): gözlü bir bulut (Zeus'un arzusu, soğuk göz); H06@heranın'da tavus gözleri açılır ---
shot(PA('P201'), (ctx, st) => {
  const t = st.t, lt = st.lt, tH = A('H06@heranın');
  glazeBG(ctx, t, { gx: 960, gy: 540, gr: 900, stars: false, warm: 'rgba(120,50,22,.4)' });
  G_medal(ctx, t, 960, 540, 440, Math.sin(t * .3) * .03, (c, t, r) => {
    // bulut: kil kontürlü sarmal bulut, ortasında soğuk beyaz göz açılır
    for (let i = 0; i < 4; i++) cloud(c, -200 + i * 130, -120 + (i % 2) * 40, 2.0, '#2A170F', 'rgba(201,112,63,.8)', i + 51);
    const eo = ramp(t, A('H06@zeusun'), A('H06@gönlü') + .3), lk = Math.sin(t * .8) * 6;
    if (eo > 0) { glow(c, 0, -110, 120, `rgba(230,236,255,${.35 * eo})`); c.fillStyle = '#E6ECFF'; c.beginPath(); c.ellipse(0, -110, 70, 26 * eo, 0, 0, TAU); c.fill(); c.fillStyle = PC.glaze; c.beginPath(); c.arc(lk + 18, -110, 15 * eo, 0, TAU); c.fill(); }
    // altta küçük İo: bakışın hedefi
    G_rf(c, 120, r * .62, 2.6, -1, LK.io, { torso: .15, head: .1 }, { seed: 61 });
    // Hera'nın tavus gözleri: kenar boyunca sırayla açılır
    const h = ramp(t, tH - .1, tH + 1.4, E.lin);
    for (let k = 0; k < 14; k++) { const q = clamp(h * 14 - k * .6); if (q <= 0) continue; const a = -PI / 2 + k / 14 * TAU, x = Math.cos(a) * (r - 60), y = Math.sin(a) * (r - 60);
      c.save(); c.translate(x, y); c.rotate(a + PI / 2); c.fillStyle = PC.clayR; c.beginPath(); c.ellipse(0, 0, 26, 34 * q, 0, 0, TAU); c.fill(); c.fillStyle = PC.glaze; c.beginPath(); c.ellipse(0, 2, 15, 20 * q, 0, 0, TAU); c.fill(); c.fillStyle = PC.clayRL; c.beginPath(); c.arc(0, 4, 6 * q, 0, TAU); c.fill(); c.restore(); }
  }, ramp(lt, 0, .4));
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 } });

// --- P202: kupa: dünya diski; atsineği İo'yu diskin kenarında kovalar, parlak bir iz bırakır ---
shot(PA('P202'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  ctx.fillStyle = '#120B08'; ctx.fillRect(0, 0, W, H);
  kylix(ctx, t, 960, 540, 440, lt * .05, (c, t, r) => {
    c.fillStyle = PC.glaze; c.beginPath(); c.arc(0, 0, r, 0, TAU); c.fill();
    // dünya diski: kil kara, çevresinde Okeanos ırmağı
    // kırmızı figür kuralı: kara diski koyu sır, kenarı kil çizgi; kil renkli İo üstünde seçilir
    c.fillStyle = '#2A1610'; c.beginPath(); c.arc(0, 0, r * .67, 0, TAU); c.fill(); c.strokeStyle = PC.clayR; c.lineWidth = 5; c.stroke();
    c.strokeStyle = 'rgba(201,112,63,.55)'; c.lineWidth = 3; for (let k = 0; k < 3; k++) { c.beginPath(); for (let a = 0; a <= TAU + .01; a += .05) { const rr = r * (.75 + k * .07) + Math.sin(a * 18 + t * 2 + k) * 4; a ? c.lineTo(Math.cos(a) * rr, Math.sin(a) * rr) : c.moveTo(Math.cos(a) * rr, Math.sin(a) * rr); } c.stroke(); }
    // İo diskin iç kenarında koşar (ayakları kenarda, başı merkeze dönük; dönen kovalamaca); atsineği hemen arkasında, parlak iz
    const ang = lt * .9, R = r * .69, pt = (a, rr) => [-rr * Math.sin(a), rr * Math.cos(a)];
    c.save(); c.rotate(ang); c.translate(0, R); H_io(c, 0, 0, 3.1, t, { run: 1, dir: -1, fly: false }); c.restore();
    c.save(); c.lineCap = 'round'; for (let k = 1; k < 34; k++) { const p0 = pt(ang - .34 - k * .02, R - 185 + Math.sin(t * 14 + k * .7) * 10), p1 = pt(ang - .34 - (k - 1) * .02, R - 185 + Math.sin(t * 14 + (k - 1) * .7) * 10); c.strokeStyle = `rgba(242,214,170,${.75 * (1 - k / 34)})`; c.lineWidth = 5 * (1 - k / 40); c.beginPath(); c.moveTo(...p0); c.lineTo(...p1); c.stroke(); }
    const fp = pt(ang - .34, R - 185 + Math.sin(t * 14) * 10); H_fly(c, fp[0], fp[1], t, 1.5, { trail: false }); c.restore();
  });
}, { tr: { type: 'cut' }, post: { tex: .7, vig: .9, grain: .055 } });

// --- P203–P206: vazo haritası: İo'nun yolu; BOS · POROS (inek geçidi); Kerç'e sıkı kadraj; kesme: İstanbul ve kendi ineği ---
shot(PA('P203'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  const c = { x: 1500 + lt * 8, y: 760, z: .72 };
  ctx.save(); cam(ctx, c, 1); H_map(ctx, t, { z: c.z, route: ramp(t, A('H07@yolculuğunu'), A('H07@bosporos') - .1, E.io2), lw: 12 }); ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .6, vig: 1, grain: .06 } });
shot(PA('P204'), (ctx, st) => {
  const t = st.t, lt = st.lt;
  H_crossing(ctx, t, E.io2(clamp(lt / (st.d + .4))), { c: { x: 960, y: 600, z: 1.12 + lt * .02 }, s: 5.6 });
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .6, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, tB = A('H07@bosporos'), tY = A('H07@yani'), sp = E.io3(ramp(t, tY - .1, tY + .5));
    const a = ramp(t, tB - .1, tB + .3);
    txt(ctx, 'BOS', 960 - 170 - sp * 90, 170, { font: '700 96px Cinzel', col: '#F1E4C8', ls: 6, a, shadow: 'rgba(0,0,0,.85)', blur: 14 });
    txt(ctx, 'POROS', 960 + 130 + sp * 90, 170, { font: '700 96px Cinzel', col: '#F1E4C8', ls: 6, a, shadow: 'rgba(0,0,0,.85)', blur: 14 });
    txt(ctx, '·', 902, 170, { font: '700 96px Cinzel', col: '#F1E4C8', a: a * sp });
    txt(ctx, 'inek', 960 - 170 - sp * 90, 270, { font: 'italic 600 64px "Cormorant Garamond"', col: '#F2D6AA', a: ramp(t, A('H07@inek') - .1, A('H07@inek') + .3), shadow: 'rgba(0,0,0,.85)', blur: 12 });
    txt(ctx, 'geçit', 960 + 130 + sp * 90, 270, { font: 'italic 600 64px "Cormorant Garamond"', col: '#F2D6AA', a: ramp(t, A('H07@geçidi') - .1, A('H07@geçidi') + .3), shadow: 'rgba(0,0,0,.85)', blur: 12 });
  } });
shot(PA('P205'), (ctx, st) => {
  const t = st.t, lt = st.lt, m = H_STR.kerc[1];
  const c = { x: m[0] - lt * 4, y: m[1], z: 3.7 };
  ctx.save(); cam(ctx, c, 1); H_map(ctx, t, { z: c.z, route: 1, head: false, lw: 12 }); ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .6, vig: 1, grain: .06 },
  over: (ctx, st) => txt(ctx, 'Kerç Boğazı', 960, 170, { font: '700 76px Cinzel', col: '#F1E4C8', ls: 4, a: ramp(st.t, A('H07@kerç') - .2, A('H07@kerç') + .3), shadow: 'rgba(0,0,0,.85)', blur: 14 }) });
shot(PA('P206'), (ctx, st) => {
  const t = st.t, lt = st.lt, m = H_STR.ist[1], n = [.7, .72];
  const c = { x: m[0] + lt * 3, y: m[1], z: 2.7 };
  ctx.save(); cam(ctx, c, 1); H_map(ctx, t, { z: c.z });
  const u = E.io2(clamp(lt / (st.d + .5)));
  H_cowSwim(ctx, m[0] + lerp(-60, 50, u) * n[0], m[1] + lerp(-60, 50, u) * n[1] - 6, .9, t, 1);
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .6, vig: 1, grain: .06 },
  over: (ctx, st) => txt(ctx, 'İstanbul Boğazı', 960, 170, { font: '700 76px Cinzel', col: '#F1E4C8', ls: 4, a: ramp(st.t, A('H07@istanbul') - .2, A('H07@istanbul') + .3), shadow: 'rgba(0,0,0,.85)', blur: 14 }) });

// --- P207–P208: İo yere çöker, ölmeyi diler; yakın: "Ben ölemem bile."; kartal gölgesi yok, kamera göğe kalkar: boş tahtın ilk çatlağı ---
shot(PA('P207'), (ctx, st) => {
  const t = st.t, lt = st.lt, tP = A('H09@prometeusun'), tI = A('H09@işkencem'), tY = A('H09@yıkılmadıkça');
  const c = F_cam(t, [[PA('P207'), { ...CAMS.genis, x: 880, y: 600, z: 1.15 }], [tP, { ...G_YK, z: 3.1 }], [tI + .2, { x: 1180, y: -260, z: 1.25 }]], 1.0, 2);
  const { wind } = kayaWorld(ctx, t, c, { sky: 'gunbatimi', skyChain: true });
  ctx.save(); cam(ctx, c, 1);
  // gökte boş taht: soğuk ışık; H09@yıkılmadıkça'da ayağında ilk çatlak ilerler
  const ta = ramp(t, tI - .2, tI + .8);
  if (ta > 0) { ctx.save(); ctx.globalAlpha = ta; glow(ctx, 1150, -330, 340, 'rgba(230,236,255,.16)'); F_throne(ctx, 1110, -300, 3.0, 1, t); crackLine(ctx, 1150, -302, 120, ramp(t, tY, tY + 1.6, E.lin), { col: '#E6ECFF', w: 4 }); ctx.restore(); }
  H_io(ctx, 760, 868, 4.6, t, { sink: E.io2(ramp(t, PA('P207') + .2, A('H09@ölmeyi') + .3)), dir: 1 });
  promChained(ctx, t, { wind, look: t > tI ? lerp(.05, -.4, ramp(t, tI, tI + .8)) : .1, pose: t > tI ? 'gok' : 'sessiz' });
  ctx.restore();
  kayaFront(ctx, t, c, wind);
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => { const t = st.t, tB = A('H09@ben'); if (t > tB) { ctx.save(); ctx.globalAlpha = 1 - ramp(t, A('H09@işkencem') - .1, A('H09@işkencem') + .5); speechFlow(ctx, 'BEN ÖLEMEM BİLE.', u => [lerp(790, 120, u), 380 - Math.sin(u * PI) * 40], ramp(t, tB, A('H09@bile') + .5, E.lin), { font: '700 66px Cinzel' }); ctx.restore(); } } });

// --- P209–P210: eşleşen kesme: zincir halkaları → meander şeridi; İo'nun soyundan on üç kuşak koşar (sayaç); on üçüncü: aslan postlu okçu yayını gerer ---
shot(PA('P209'), (ctx, st) => {
  const t = st.t, lt = st.lt, t1 = A('H10@iyonun'), tO = A('H10@okçu');
  const gy = 870, push = E.io2(ramp(t, tO - .1, st.end + 1.0, E.lin));
  const pan = E.io2(clamp((t - t1 + .5) / 5)), c = { x: lerp(lerp(760, 1060, pan), 1650, push), y: lerp(660, 600, push), z: lerp(1.3, 2.2, push) };
  glazeBG(ctx, t, { gx: 900, gy: 760, gr: 1000, stars: false, warm: 'rgba(150,62,28,.42)' });
  ctx.save(); cam(ctx, c, 1);
  const mo = ramp(lt, .25, .9);
  // zincir halkaları şeride dönüşür (eşleşen kesme)
  if (mo < 1) { ctx.save(); ctx.globalAlpha = 1 - mo; ironChain(ctx, [-200, gy + 10], [2200, gy + 10], { w: 12, link: 60 }); ctx.restore(); }
  ctx.save(); ctx.globalAlpha = mo; meanderSaltire(ctx, -400, 2600, gy, 34, mixCol(PC.clayR, PC.glaze, .25), PC.glaze); ctx.restore();
  // on iki koşucu: sırayla soldan girer ve sağa akar; on üçüncü okçu
  const sty = { ...STY.red, white: STY.red.fill };
  for (let k = 0; k < 12; k++) { const t0 = t1 + k * .36, a = ramp(t, t0, t0 + .3); if (a <= 0) continue;
    const x = 120 + (t - t0) * 250;
    ctx.save(); ctx.globalAlpha = a * (1 - push * .85); walkScene(ctx, null, x, 3.2, t, 1, { noCam: true, ground: FLAT(gy - 18), stride: 52, lean: .22, dist: x, sty, lk: k % 3 === 2 ? LK.humanF : LK.human }); ctx.restore(); }
  const ta = ramp(t, tO - .15, tO + .25);
  if (ta > 0) { ctx.save(); ctx.globalAlpha = ta; const A1 = L_archer(ctx, 1560 - 40 * (1 - ta), gy, 4.4, t, ramp(t, tO, tO + .9, E.io2), 0); L_arrow(ctx, A1.bow[0] + 16, A1.nock[1] - 1, -.02, 4.4 * .9, .5 + .3 * Math.sin(t * 4)); ctx.restore(); }
  ctx.restore();
  kayaFrame(ctx, t);
}, { tr: { type: 'cut' }, post: { tex: .55, vig: 1, grain: .06 },
  over: (ctx, st) => {
    const t = st.t, t1 = A('H10@iyonun'), n = clamp(Math.floor((t - t1) / .36) + 1, 0, 12) + (t > A('H10@okçu') - .1 ? 1 : 0);
    if (n > 0) { txt(ctx, String(n), 1760, 240, { font: '700 110px Cinzel', col: n === 13 ? '#FFC867' : '#F1E4C8', a: 1 - ramp(t, st.end - .3, st.end), shadow: 'rgba(0,0,0,.8)', blur: 14 }); txt(ctx, 'KUŞAK', 1760, 320, { font: '600 40px Cinzel', col: PC.clayRL, ls: 6, a: 1 - ramp(t, st.end - .3, st.end) }); }
  } });
