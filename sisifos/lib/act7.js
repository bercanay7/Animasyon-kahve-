// KAPANIŞ: hikâye bir amforanın üzerindeymiş; herkesin kayası
'use strict';
// Friz şeridi (amforanın gövdesine sarılır): Sisifos + günümüz insanları kayalarıyla
let STRIP = null;
function buildStrip() {
  if (STRIP) return STRIP;
  const SW = 3600, SH = 520, cv = makeCanvas(SW, SH), x = cv.getContext('2d');
  x.fillStyle = '#C8693D'; x.fillRect(0, 0, SW, SH);
  meander(x, 0, SW, 8, 46, C.ink); tongues(x, 0, SW, SH - 52, 46, C.ink);
  const gy = SH - 58;
  x.fillStyle = C.ink; x.fillRect(0, gy, SW, 5);
  const seg = SW / 6;
  const scenes = [
    { lk: LK.sis, rock: 64, hold: null },
    { lk: LK.modern, rock: 0, hold: { N: HOLD.bag() }, label: 'iş' },
    { lk: LK.woman, rock: 0, label: 'aile' },
    { lk: LK.modern, rock: 0, hold: { N: HOLD.book() }, label: 'hayal' },
    { lk: { ...LK.sis, old: true, beard: 'long' }, rock: 0, label: 'yaş' },
    { empty: true },
  ];
  // figür ara tuvali W×H olduğundan her sahne kendi küçük tuvalinde çizilip şeride kopyalanır
  const tmp = makeCanvas(seg, SH), tx = tmp.getContext('2d');
  scenes.forEach((sc, i) => {
    tx.setTransform(1, 0, 0, 1, 0, 0); tx.clearRect(0, 0, seg, SH);
    const cx = seg * .5, xr = cx + 110, R = 118;
    const g = groundOf(() => gy);
    if (sc.empty) {
      // boş yer: soluk siluet + kaya (izleyicinin yeri)
      pushScene(tx, null, xr, R, 3.3, 7.3, { noCam: true, ground: g, dist: xr + 70, lk: LK.modern, light: -2.3, cutCol: '#C8693D', T: 1.1, hA: .85, hB: .85, alpha: .22 });
      tx.save(); tx.globalAlpha = .55; boulder(tx, xr, gy - R, R, .4, { shadow: false }); tx.restore();
      txt(tx, '?', cx - 40, gy - 330, { font: '700 84px Cinzel', col: C.ink });
      txt(tx, 'sen?', xr, gy - R + 4, { font: 'italic 700 46px "Cormorant Garamond"', col: C.ink, a: .8 });
    } else {
      // her biri kendi "kayası"nı iter
      const P = pushScene(tx, null, xr, R, 3.3, 1.3 + i, { noCam: true, ground: g, dist: xr + i * 13, lk: sc.lk, light: -2.3, cutCol: '#C8693D', T: 1.1, hA: .85, hB: .85, hold: sc.hold });
      if (sc.label) txt(tx, sc.label, P.cx, P.cy + 4, { font: 'italic 700 46px "Cormorant Garamond"', col: C.ink });
    }
    x.drawImage(tmp, seg * i, 0);
  });
  STRIP = { cv, SW, SH };
  return STRIP;
}
// Amfora profili: [y, yarıçap] (birim yükseklik 1000)
const VASE = [[0, 175], [26, 168], [40, 132], [170, 118], [240, 210], [300, 318], [380, 372], [470, 385], [560, 370], [650, 320], [760, 230], [850, 160], [890, 150], [910, 190], [950, 196], [985, 180], [1000, 175]];
function vaseR(y) { for (let i = 1; i < VASE.length; i++) if (y <= VASE[i][0]) { const [y0, r0] = VASE[i - 1], [y1, r1] = VASE[i]; const u = (y - y0) / (y1 - y0); return lerp(r0, r1, smooth(u)); } return 175; }
function drawVase(ctx, x, y, s, rot, o = {}) {
  const S = buildStrip();
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
// H1–H2 — Tartaros'tan amforaya geri çekiliş, dönen friz
shot(S('H01') - .45, (ctx, st) => {
  const t = st.t, lt = st.lt;
  museum(ctx, t);
  const z = lerp(3.0, .92, ramp(lt, 0, 4.6, E.io3));
  const rot = .118 - lt * .03;
  // başta bant (Sisifos) ekran ortasında, sonra amfora görünür
  const vy = lerp(553, 600, ramp(lt, 0, 4.2, E.io3));
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2);
  drawVase(ctx, W / 2, vy, .9, rot);
  ctx.restore();
}, { tr: { type: 'clay', dur: 1.2 }, post: { tex: .35, vig: 1, grain: .05 } });

// H3 — boş yer: "Senin kayan ne?"
shot(S('H03') - .4, (ctx, st) => {
  const t = st.t, lt = st.lt;
  museum(ctx, t);
  // boş sahnenin öne geleceği dönüş
  const rot = lerp(.75, .9, ramp(lt, 0, 1.6, E.io3)) + Math.max(0, lt - 1.6) * .002;
  const z = lerp(.92, 1.9, ramp(lt, .2, 2.0, E.io3));
  ctx.save(); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-W / 2, -H / 2 - lerp(0, -40, ramp(lt, .2, 2))); drawVase(ctx, W / 2, 600, .9, rot); ctx.restore();
  quote(ctx, 'Senin kayan ne?', W / 2, 980, 1400, t - Wd('H03', 'senin') + .1, { font: 'italic 600 84px "Cormorant Garamond"', col: '#FFF0D0', shadow: 'rgba(0,0,0,.7)', blur: 16 });
}, { tr: { type: 'fade', dur: .6 }, post: { tex: .35, vig: 1, grain: .05 } });

// H4 — bitiş kartı (sağ taraf YouTube bitiş ekranı öğeleri için boş)
shot(S('H04') - .3, (ctx, st) => {
  const t = st.t, lt = st.lt;
  museum(ctx, t, .7);
  const a = ramp(lt, 0, 1.2, E.io2);
  drawVase(ctx, lerp(W / 2, 470, a), lerp(600, 560, a), lerp(1.0, .78, a), .6 - lt * .02);
  ctx.save(); ctx.globalAlpha = ramp(lt, .6, 1.6);
  txt(ctx, 'SİSİFOS', 470, 975, { font: '900 64px Cinzel', col: '#F3E2BC', ls: 16 });
  ctx.restore();
  quote(ctx, 'Senin kayan neyse, yorumlarda anlat.', 470, 1040, 900, lt - .6, { font: 'italic 500 38px "Cormorant Garamond"', col: '#E9D3AE' });
  // sağ taraf YouTube bitiş ekranı öğeleri için boş bırakılır
}, { tr: { type: 'fade', dur: .8 }, post: { tex: .35, vig: 1, grain: .05 } });
