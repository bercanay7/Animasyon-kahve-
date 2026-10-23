// KAPANIŞ: hikâye bir amforanın üzerindeymiş; herkesin kayası
'use strict';
// Friz şeridi (amforanın gövdesine sarılır): Sisifos + günümüz insanları kayalarıyla; her karede canlı çizilir
const STRIP_N = 7, SEG = 600, SW = SEG * STRIP_N, SH = 520;
const STRIP_SCENES = [
  { lk: LK.sis },
  { lk: LK.modern, label: 'iş' },
  { lk: LK.woman, label: 'sorumluluk' },
  { lk: LK.modern, label: 'hayal' },
  { lk: LK.citizen, label: 'her sabah' },
  { lk: { ...LK.sis, old: true, beard: 'long' } },
  { empty: true },
];
const segRot = k => (k + .5) / STRIP_N; // k. sahne vazonun önüne gelir
let STRIP = null;
function buildStrip(t = 0, reveal = 1) {
  if (!STRIP) { const cv = makeCanvas(SW, SH); STRIP = { cv, x: cv.getContext('2d'), tmp: makeCanvas(SEG, SH), SW, SH }; STRIP.tx = STRIP.tmp.getContext('2d'); }
  const x = STRIP.x, tx = STRIP.tx;
  x.setTransform(1, 0, 0, 1, 0, 0);
  x.fillStyle = '#C8693D'; x.fillRect(0, 0, SW, SH);
  meander(x, 0, SW, 8, 46, C.ink); tongues(x, 0, SW, SH - 52, 46, C.ink);
  const gy = SH - 58;
  x.fillStyle = C.ink; x.fillRect(0, gy, SW, 5);
  // figür ara tuvali W×H olduğundan her sahne kendi küçük tuvalinde çizilip şeride kopyalanır
  STRIP_SCENES.forEach((sc, i) => {
    tx.setTransform(1, 0, 0, 1, 0, 0); tx.clearRect(0, 0, SEG, SH);
    const cx = SEG * .5, xr = cx + 110, R = 118, g = groundOf(() => gy);
    if (sc.empty) {
      // boş yer: soru sorulana kadar boş kil; sonra soluk siluet + kaya + "sen?"
      if (reveal > 0) {
        tx.save(); tx.globalAlpha = reveal;
        pushScene(tx, null, xr, R, 3.3, t, { noCam: true, ground: g, dist: xr + 70, lk: LK.modern, light: -2.3, cutCol: '#C8693D', T: 1.1, hA: .85, hB: .85, alpha: .25 });
        tx.globalAlpha = reveal * .6; boulder(tx, xr, gy - R, R, .4, { shadow: false }); tx.globalAlpha = reveal;
        txt(tx, '?', cx - 40, gy - 330, { font: '700 96px Cinzel', col: C.ink, force: true });
        txt(tx, 'sen?', xr, gy - R + 6, { font: 'italic 700 84px "Cormorant Garamond"', col: C.ink, force: true });
        tx.restore();
      }
    } else {
      const P = pushScene(tx, null, xr, R, 3.3, t + i * 1.3, { noCam: true, ground: g, dist: xr + i * 13 + t * 12, lk: sc.lk, light: -2.3, cutCol: '#C8693D', T: 1.1, hA: .85, hB: .85 });
      if (sc.label) { tx.font = 'italic 700 84px "Cormorant Garamond"'; const fs = Math.floor(Math.min(84, 84 * 1.62 * R / tx.measureText(sc.label).width)); txt(tx, sc.label, P.cx, P.cy + 6, { font: `italic 700 ${fs}px "Cormorant Garamond"`, col: C.ink, force: true }); }
    }
    x.drawImage(STRIP.tmp, SEG * i, 0);
  });
  return STRIP;
}
// Amfora profili: [y, yarıçap] (birim yükseklik 1000)
const VASE = [[0, 175], [26, 168], [40, 132], [170, 118], [240, 210], [300, 318], [380, 372], [470, 385], [560, 370], [650, 320], [760, 230], [850, 160], [890, 150], [910, 190], [950, 196], [985, 180], [1000, 175]];
// pürüzsüz profil: düğümlerde eğimi sürekli kübik Hermite (düğümlerde düzlük/çıkıntı olmaz)
const VASE_M = VASE.map((q, i) => { const a = VASE[Math.max(0, i - 1)], b = VASE[Math.min(VASE.length - 1, i + 1)]; return (b[1] - a[1]) / Math.max(1, b[0] - a[0]); });
function vaseR(y) {
  for (let i = 1; i < VASE.length; i++) if (y <= VASE[i][0]) {
    const [y0, r0] = VASE[i - 1], [y1, r1] = VASE[i], h = y1 - y0, u = (y - y0) / h, u2 = u * u, u3 = u2 * u;
    return (2 * u3 - 3 * u2 + 1) * r0 + (u3 - 2 * u2 + u) * h * VASE_M[i - 1] + (-2 * u3 + 3 * u2) * r1 + (u3 - u2) * h * VASE_M[i];
  }
  return 175;
}
function drawVase(ctx, x, y, s, rot, o = {}) {
  const S = buildStrip(o.t || 0, o.reveal ?? 1);
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s); ctx.translate(0, -500);
  // gölge
  ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.beginPath(); ctx.ellipse(0, 1004, 260, 26, 0, 0, TAU); ctx.fill();
  // kulplar
  ctx.strokeStyle = C.ink; ctx.lineWidth = 26; ctx.lineCap = 'round';
  for (const sg of [-1, 1]) { ctx.beginPath(); ctx.moveTo(sg * 122, 70); ctx.bezierCurveTo(sg * 300, 40, sg * 330, 170, sg * 250, 260); ctx.stroke(); }
  // gövde silueti
  const path = () => { ctx.beginPath(); ctx.moveTo(-VASE[0][1], 0); for (let yy = 0; yy <= 1000; yy += 10) ctx.lineTo(-vaseR(yy), yy); for (let yy = 1000; yy >= 0; yy -= 10) ctx.lineTo(vaseR(yy), yy); ctx.closePath(); };
  path(); ctx.fillStyle = C.ink; ctx.fill();
  ctx.save(); path(); ctx.clip();
  // friz bandı (silindirik izdüşüm)
  const by0 = 330, by1 = 640, Rb = 378, step = 3;
  for (let px = -Rb; px < Rb; px += step) {
    const th = Math.asin(clamp(px / Rb, -1, 1)), th2 = Math.asin(clamp((px + step) / Rb, -1, 1));
    const u0 = (th / TAU + rot) , u1 = (th2 / TAU + rot);
    const sx = ((u0 % 1) + 1) % 1 * S.SW, sw = Math.max(1, (u1 - u0) * S.SW);
    if (sx + sw <= S.SW) ctx.drawImage(S.cv, sx, 0, sw, S.SH, px, by0, step + .6, by1 - by0);
    else ctx.drawImage(S.cv, 0, 0, sw, S.SH, px, by0, step + .6, by1 - by0);
  }
  // ince kil bantlar (üst/alt)
  ctx.fillStyle = '#C8693D'; ctx.fillRect(-400, 230, 800, 10); ctx.fillRect(-400, 700, 800, 10);
  rays(ctx, -400, 400, 770, 90, '#C8693D'); ctx.fillStyle = C.ink;
  // hacim gölgesi + parlama
  const g = ctx.createLinearGradient(-400, 0, 400, 0);
  g.addColorStop(0, 'rgba(0,0,0,.75)'); g.addColorStop(.28, 'rgba(0,0,0,.15)'); g.addColorStop(.5, 'rgba(0,0,0,0)'); g.addColorStop(.62, 'rgba(255,240,210,.10)'); g.addColorStop(.72, 'rgba(255,240,210,.0)'); g.addColorStop(1, 'rgba(0,0,0,.8)');
  ctx.fillStyle = g; ctx.fillRect(-400, 0, 800, 1000);
  const hg = ctx.createLinearGradient(80, 0, 170, 0); hg.addColorStop(0, 'rgba(255,245,225,0)'); hg.addColorStop(.5, 'rgba(255,245,225,.13)'); hg.addColorStop(1, 'rgba(255,245,225,0)'); ctx.fillStyle = hg; ctx.fillRect(80, 40, 90, 920);
  ctx.restore();
  ctx.restore();
}
// Müze zemini
function museum(ctx, t, warm = 1) {
  const g = ctx.createRadialGradient(W / 2, H * .38, 60, W / 2, H * .5, W * .75);
  g.addColorStop(0, mixCol('#3A2416', '#5A3418', warm)); g.addColorStop(1, '#0B0605');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  motes(ctx, t, 40, 61, 'rgba(255,220,160,.5)', [0, 0, W, H], 8, 1.6, .4);
}
// H1–H2 — Tartaros'tan amforaya geri çekiliş; friz anlatılan kelimelerle adım adım döner
function closingRot(t) {
  // her etiketli kaya, adı söylenirken öne gelir; H02 boyunca tam tur tamamlanır
  const steps = [[Wd('H01', 'iş') - .45, 1], [Wd('H01', 'sorumluluk') - .45, 2], [Wd('H01', 'hayal') - .45, 3], [Wd('H01', 'her') - .1, 4]];
  let k = 0;
  for (const [ts, kk] of steps) k = lerp(k, kk, ramp(t, ts, ts + .5, E.io3));
  k = lerp(k, STRIP_N, ramp(t, S('H02') - .3, Se('H02') + .2, E.io2));
  return (k + .5) / STRIP_N;
}
shot(S('H01') - .45, (ctx, st) => {
  const t = st.t, lt = st.lt;
  museum(ctx, t);
  const z = lerp(3.0, 1.38, ramp(lt, 0, 2.6, E.io3)) - ramp(t, S('H02') - .2, Se('H02'), E.io2) * .46;
  const vy = lerp(553, 600, ramp(lt, 0, 2.6, E.io3));
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  drawVase(ctx, W / 2, vy, .9, closingRot(t), { t, reveal: 0 });
  ctx.restore();
}, { tr: { type: 'clay', dur: 1.2 }, post: { tex: .35, vig: 1, grain: .05 }, mb: 8 });

// H2b — "Ona omuz verirken, nasıl biri olacağımızı seçmektir": Tartaros'a geri dönüş, omuz kayada, gülümseme
shot(Wd('H02', 'ona') - .15, (ctx, st) => {
  const t = st.t, lt = st.lt, tc = Wd('H02', 'seçmektir');
  const xr = 300 + lt * 10, sm = ramp(t, tc - .4, tc + .9, E.io2);
  const po = { dist: xr, smile: sm * 1.6, strain: .35 * (1 - sm), look: -.15 - .15 * sm, reach: 19, T: 1.12 };
  const P = pushScene(ctx, null, xr, 150, 4.0, t, { ...po, dry: true });
  const z = lerp(1.5, 2.1, E.io2(clamp(lt / st.d)));
  const c = { x: P.head[0] + 120, y: P.head[1] + 60, z };
  tartarosBG(ctx, t, c, { warm: 1, diskX: P.head[0] + 300, diskY: P.head[1] - 280, diskR: 300 });
  tartarosHill(ctx, c, { groove: .9, warm: 1 });
  pushScene(ctx, c, xr, 150, 4.0, t, po);
  motes(ctx, t, 50, 71, 'rgba(255,225,160,.8)', [0, 0, W, H], 12, 2.2, .7);
}, { tr: { type: 'cut' }, post: { tex: .5, vig: .9, grain: .05 } });

// H3 — boş yer: "Peki ya sen? Senin kayan ne?" — bir sahne geri döner, siluet belirir
shot(S('H03') - .4, (ctx, st) => {
  const t = st.t, lt = st.lt;
  museum(ctx, t);
  const rot = lerp(segRot(STRIP_N), segRot(STRIP_N - 1), ramp(lt, 0, 1.4, E.io3)) + Math.max(0, lt - 1.4) * .0015;
  const z = lerp(.92, 1.9, ramp(lt, .2, 2.0, E.io3));
  const rv = ramp(t, Wd('H03', 'sen') - .1, Wd('H03', 'sen') + .6, E.io2);
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2 - lerp(0, -40, ramp(lt, .2, 2))); drawVase(ctx, W / 2, 600, .9, rot, { t, reveal: rv }); ctx.restore();
  quote(ctx, 'Senin kayan ne?', W / 2, 120, 1400, t - Wd('H03', 'senin') + .1, { font: 'italic 600 88px "Cormorant Garamond"', col: '#FFF0D0', shadow: 'rgba(0,0,0,.8)', blur: 18 });
}, { tr: { type: 'cut' }, post: { tex: .35, vig: 1, grain: .05 } });

// H4 — bitiş kartı (sağ taraf YouTube bitiş ekranı öğeleri için boş)
shot(S('H04') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt;
  museum(ctx, t, .7);
  const a = ramp(lt, 0, 1.2, E.io2);
  drawVase(ctx, lerp(W / 2, 470, a), lerp(600, 610, a), lerp(1.0, .7, a), segRot(STRIP_N - 1) + Math.sin(lt * .5) * .005, { t });
  ctx.save(); ctx.globalAlpha = ramp(lt, .6, 1.6);
  txt(ctx, 'SİSİFOS', 470, 120, { font: '900 68px Cinzel', col: '#F3E2BC', ls: 16 });
  ctx.restore();
  quote(ctx, 'Senin kayan neyse, yorumlarda anlat.', 470, 192, 900, lt - .6, { font: 'italic 600 46px "Cormorant Garamond"', col: '#E9D3AE' });
  // sağ taraf YouTube bitiş ekranı öğeleri için boş bırakılır
}, { tr: { type: 'cut' }, post: { tex: .35, vig: 1, grain: .05 } });
