// Planlar (planlar.js): her plan bir gravür levhası; portreli planlarda renkli tuval impasto ile bindirilir. Klasik betik.
// Kurallar (planlar_kaynak.py başı): Dorian'ın yüzü yalnız portrede; renk yalnız portrede; şiddet gölgeyle, kan yok.
'use strict';
const PS = window.PLAN;
const CAM = (cx, cy, z = 1) => ({ cx, cy, z });
// ── ön katman: figürler portrenin önünde kalsın diye ayrı basılır; maske = arka plan yaması dışındaki pikseller
const _on = makeCanvas(DW, DH), _onx = _on.getContext('2d'), _mk = makeCanvas(DW, DH), _mkx = _mk.getContext('2d');
function onKatman(ctx, cam, fn) {
  GR.begin(.5, 0, 0, camOf(cam)); fn();
  const d = GR.px.getImageData(0, 0, DW, DH), md = _mkx.createImageData(DW, DH);
  for (let i = 0; i < d.data.length; i += 4) md.data[i + 3] = (d.data[i] | d.data[i + 1]) ? 255 : 0;
  _mkx.putImageData(md, 0, 0);
  GR.engrave(_onx);
  _onx.save(); _onx.setTransform(1, 0, 0, 1, 0, 0); _onx.globalCompositeOperation = 'destination-in'; _onx.drawImage(_mk, 0, 0); _onx.restore();
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(_on, 0, 0); ctx.restore();
}
// levha + (isteğe bağlı) portre + (isteğe bağlı) ön katman
function sahne(ctx, st, o) {
  const cam = o.cam;
  let Mf = null;
  levha(ctx, cam, () => { Mf = o.arka(st) || null; }, o.bg || [.05, 0, 0]);
  if (Mf && o.portre) PORTRE.ciz(ctx, { M: Mf(cam), durum: o.portre, t: st.t, gecis: o.gecis, expo: o.expo, maske: o.maske });
  if (o.on) onKatman(ctx, cam, () => o.on(st));
}
// ── ekran yazıları (plan 'yazi' alanı): alıntı “…” üstte panelli; etiket (büyük harf) sol üstte
function yaziOver(id, o = {}) {
  const y = (PS[id] || {}).yazi; if (!y) return undefined;
  if (y.startsWith('“')) return (ctx, st) => quote(ctx, y, o.x ?? W / 2, o.y ?? 190, st.lt, { px: o.px || 66, t0: o.t0 ?? .4, maxW: 1300, kaynak: o.kaynak });
  return (ctx, st) => etiket(ctx, y, o.x ?? 150, o.y ?? 120, st.lt, Math.min(st.d, o.d ?? 5), { align: 'left', px: o.px || 46 });
}
function P(id, draw, o = {}) { plan(id, draw, { over: o.over === undefined ? yaziOver(id, o.yazi) : o.over, ...o }); }
const p01 = (st, a, b) => clamp((st.lt - a) / (b - a));
const io = t => E.io2(clamp(t));

// ═════ ODA (kilitli eski okul odası) ═════
const ODA_FR = { x: 1090, y: 120, s: 1 };
const ODA_LAMBA = { x: 905, y: 650 };
function odaArka(st, o = {}) {
  SET.oda();
  const lx = o.lamba || ODA_LAMBA;
  if (o.lambaVar !== false) SET.lamba(lx.x, lx.y, st.t);
  const Mf = o.cerceveYok ? null : SET.cerceve(ODA_FR.x, ODA_FR.y, ODA_FR.s);
  if (o.lambaVar !== false) SET.isik({ x: lx.x, y: lx.y, r1: o.r1 || 640, a: o.isik ?? 1 });
  return Mf;
}
// mor perde (yerel 0..540 × 0..760): dünyada (x, y), düşüş/çekiliş dönüşümüyle
function perde(x, y, a = 0, sy = 1, sx = 1) {
  GR.save(); GR.frame(x, y, a, 1, 1);
  GR.tx.save(); GR.px.save(); GR.tx.scale(sx, sy); GR.px.scale(sx, sy);
  INSAN.fill(INSAN.F([[0, 0], [540, 0], [546, 760], [-8, 760]]), .14, { th: Math.PI / 2, id: 9 });
  for (let i = 0; i < 7; i++) { const xx = 40 + i * 74 + (i % 2) * 12, w = 22 + (i % 3) * 9; INSAN.fill(INSAN.Sm([[xx, 0], [xx + w, 0], [xx + w + 10, 380], [xx + w + 18, 760], [xx - 4, 760], [xx + 4, 380]]), i % 2 ? .05 : .3, { th: Math.PI / 2, id: 9 }); }
  INSAN.fill(INSAN.F([[-8, 714], [546, 714], [546, 760], [-8, 760]]), .62, { th: 0, id: 9 });
  for (let xx = 6; xx < 540; xx += 34) INSAN.fill(SET.E2(xx + 10, 737, 9, 9), .2, { th: 0, id: 9 });
  GR.tx.restore(); GR.px.restore(); GR.restore();
}
// yerdeki yığılmış perde (koparılıp atılmış)
function perdeYigin(x, y, w = 560) { INSAN.fill(INSAN.Sm([[x, y], [x + w * .3, y - 70], [x + w * .55, y - 40], [x + w * .8, y - 90], [x + w, y], [x + w * .9, y + 40], [x + w * .1, y + 44]]), .16, { type: 'bend', ox: x, oy: y - 60, a: 0, k: .002, id: 9 }); INSAN.fill(INSAN.F([[x + 20, y + 20], [x + w * .9, y + 18], [x + w * .88, y + 36], [x + 26, y + 38]]), .6, { th: 0, id: 9 }); }
const DOR = (x, o = {}) => INSAN.adam({ x, y: 997, h: 790, yon: 1, arka: true, kenar: .4, kenarYan: 1, ...o });

// P001 A01: lamba alevi + perdenin kenarını tutan el (kapak A)
P('P001', (ctx, st) => sahne(ctx, st, { cam: CAM(1010, 470, 1.9), arka: () => { const _M = odaArka(st); perde(1070 + 10 * io(p01(st, 1, 6)), 100 - 18 * io(p01(st, 1.5, 6)), -.02 * io(p01(st, 1, 6)));  return _M; } ,
  on: () => { const a = -.4 - .25 * io(p01(st, 1, 6)); INSAN.adam({ x: 820, y: 1160, h: 900, yon: 1, arka: true, kenar: .45, kolOn: { a: 1.7 + a, b: .2 }, kolArka: { a: -.1, b: .2 } }); } }), { yazi: {} });
// P002 A01@kimse: oda geniş, sırtı dönük Dorian, perdeli çerçeve
P('P002', (ctx, st) => { const c = camLerp(CAM(1000, 520, 1), CAM(1060, 520, 1.05), st.p);
  sahne(ctx, st, { cam: c, arka: () => { const _M = odaArka(st); perde(1070, 100);  return _M; }, on: () => DOR(700 + 4 * Math.sin(st.t), { kolOn: { a: .1, b: .1 } }) }); });
// P005 A03: kapalı perde yakın, işleme; 'göreceğiz'de ürperme
P('P005', (ctx, st) => { const s = Wd('A03', 'göreceğiz'), u = Math.max(0, st.t - s), tit = Math.sin(u * 14) * Math.exp(-u * 2.5) * (st.t > s ? 1 : 0);
  sahne(ctx, st, { cam: CAM(1340, 600, 1.55 + .04 * st.p), arka: () => { const _M = odaArka(st); perde(1070 + tit * 6, 100, tit * .004);  return _M; } }); });

// ═════ BELGE (Sarony, Lippincott, Önsöz) ═════
function kagitArka() { INSAN.fill(SET.R(-400, -400, 2800, 1900), .07, { th: 0, id: 0 }); }
// P003 A02: Sarony 23 gravüre çevrilmiş
P('P003', (ctx, st) => levha(ctx, CAM(960, 540 - 30 * st.p, 1 + .05 * st.p), () => { kagitArka(); INSAN.fill(SET.R(640, 40, 640, 1000), .92, { th: 0, id: 10 });
  SET.fotoGravur('sarony23', 680, 70, 560, { kirp: [140, 80, 1880, 3150], kontrast: 1.6 }); }, [.07, 0, 0]),
  { over: (ctx, st) => etiket(ctx, 'OSCAR WILDE · 1890', 150, 120, st.lt, st.d, { align: 'left' }) });
// P004 A02@sordu: Lippincott başlık sayfası
P('P004', (ctx, st) => { SET.belge(ctx, 'lippBaslik', CAM(960, 520 - 40 * st.p, 1.12 + .06 * st.p), 600, 40, 720, { kirp: [40, 40, 940, 1300] }); }, { over: null });
// P017 B07: Lippincott s.19, dilek paragrafı (intihar satırı kadraj dışında)
P('P017', (ctx, st) => { const sx = [60, 330, 920, 330]; SET.belge(ctx, 'lippDilek', CAM(960, 470, 1.0 + .06 * st.p), 160, 300, 1600, { kirp: sx });
  const u = io(p01(st, .8, 4)); ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = 'rgba(40,30,20,.35)';
  ctx.fillRect(0, 0, DW, DH); ctx.globalCompositeOperation = 'screen'; ctx.fillStyle = `rgba(255,240,200,${.35 * u})`; ctx.fillRect(160 * RS, 560 * RS, 1600 * RS * u, 110 * RS); ctx.restore(); }, { over: null });
// P018 B07@Vayld: 1890 / 1891 iki satır
P('P018', (ctx, st) => { levha(ctx, CAM(960, 540, 1), () => { kagitArka(); INSAN.fill(SET.R(260, 220, 1400, 640), .9, { th: 0, id: 10 }); }, [.07, 0, 0]); }, {
  over: (ctx, st) => { const c = `rgb(${GR.INK})`; txt(ctx, '1890', 520, 420, { px: 72, col: c, a: clamp(st.lt / .5) }); quote(ctx, '“…her şeyi verirdim!”', 1080, 420, st.lt, { px: 64, col: c, panel: false });
    txt(ctx, '1891', 520, 640, { px: 72, col: c, a: clamp((st.lt - 1.6) / .5) }); quote(ctx, '“…ruhumu verirdim!”', 1080, 640, st.lt, { px: 64, col: '#7a1e14', panel: false, t0: 1.6 }); } });

// ═════ STÜDYO ═════
const STU_SV = { x: 1060, y: 150, s: .92 };
function stuArka(st, o = {}) { SET.studyo({ isik: o.isik ?? 1 }); const Mf = SET.sovale(STU_SV.x, STU_SV.y, STU_SV.s); return Mf; }
const BASIL = (x, o = {}) => INSAN.adam({ x, y: 1000, h: 760, yon: o.yon ?? 1, arka: false, ton: .12, kenar: .55, kenarYan: 1, yuzTon: .2, ...o });
const HENRY = (x, o = {}) => INSAN.adam({ x, y: 1000, h: 800, yon: o.yon ?? 1, arka: false, ton: .05, kenar: .5, kenarYan: 1, biyik: true, ...o });
// P006 B01: stüdyo geniş
P('P006', (ctx, st) => { const c = camLerp(CAM(960, 540, 1), CAM(1000, 540, 1.04), st.p);
  sahne(ctx, st, { cam: c, arka: () => stuArka(st), portre: 'G', on: () => { BASIL(880, { kolOn: { a: 1.6 + .25 * Math.sin(st.t * 2.2), b: -.4 }, egim: .03 }); DOR(1660, { h: 600, y: 860, yon: -1, kenarYan: -1 }); } }); }, { yazi: {} });
// P007 B01@Ressam: Basil fırçayla (yan)
P('P007', (ctx, st) => sahne(ctx, st, { cam: CAM(1100, 560, 1.4), arka: () => stuArka(st), portre: 'G', on: () => BASIL(860, { kolOn: { a: 1.5 + .3 * Math.sin(st.t * 3), b: -.5 }, egim: .04 }) }));
// P008 B01@Dorian: tuvalde genç yüz darbe darbe tamamlanır
P('P008', (ctx, st) => sahne(ctx, st, { cam: CAM(1290, 400, 2.1 + .1 * st.p), arka: () => stuArka(st), portre: 'G', gecis: { dan: 'Z', t0: st.at + .2 } }));
// P009 B02: Basil geri çekilir
P('P009', (ctx, st) => sahne(ctx, st, { cam: CAM(1080, 560, 1.25), arka: () => stuArka(st), portre: 'G', on: () => BASIL(760 - 40 * io(p01(st, 0, 2)), { kolOn: { a: .2, b: .1 }, bas: -.08 }) }), { yazi: { y: 150 } });
// P010 B03: ters açı, divanda Henry, duman
function duman(x, y, t, uz = 1, yon = 1) { for (let k = 0; k < 6; k++) { const u = ((t * .25 + k / 6) % 1), xx = x + yon * u * 260 * uz + Math.sin(u * 7 + k) * 30, yy = y - u * 420 * uz; INSAN.fill(SET.E2(xx, yy, 14 + u * 60, 6 + u * 22, .4), .75 - u * .5, { type: 'bend', ox: xx - 40, oy: yy, a: 0, k: .006, id: 2 }); } }
P('P010', (ctx, st) => levha(ctx, CAM(700, 600, 1.15), () => { SET.studyo({ isik: .6 }); const h = HENRY(420, { yon: 1, egim: -.35, kolOn: { a: 2.2, b: -1.6 }, sigara: true, h: 760 }); duman(h.el[0] + 20, h.el[1] - 10, st.t, 1, 1); }));
// P011 B03@etkilemek: duman Dorian'ın kulağına
P('P011', (ctx, st) => levha(ctx, CAM(1250, 380, 2.2), () => { SET.studyo({ isik: .8 }); DOR(1300, { y: 1000, h: 760 }); const u = io(p01(st, 0, st.d)); for (let k = 0; k < 14; k++) { const q = k / 14; if (q > u) break; const x = 900 + q * 400, y = 330 + Math.sin(q * 6 + st.t) * 18 - q * 20; INSAN.fill(SET.E2(x, y, 22, 8, .2), .8, { type: 'bend', ox: x - 20, oy: y, a: 0, k: .006, id: 2 }); } }));

// ═════ BAHÇE ═════
P('P012', (ctx, st) => SET.dore(ctx, 'dore169', CAM(960, 500 + 120 * st.p, 1.0), 1920), { over: null });
P('P013', (ctx, st) => levha(ctx, CAM(960, 560, 1.1), () => { SET.bahce({ t: st.t }); const h = HENRY(760, { yon: 1, kolOn: { a: .9 + .3 * Math.sin(st.t * 1.6), b: -.6 }, sigara: false, sapka: true }); DOR(1180, { yon: -1, kenarYan: -1, kenar: .5 }); }), { yazi: { y: 160 } });
P('P014', (ctx, st) => levha(ctx, CAM(960, 520, 1.6), () => { SET.bahce({ t: st.t }); for (let k = 0; k < 18; k++) { const t0 = k * .35, u = clamp((st.lt - t0) / 3); if (u <= 0) continue; const x = 700 + (k * 97) % 520 + Math.sin(u * 6 + k) * 40, y = 300 + u * 700; INSAN.fill(SET.E2(x, y, 9, 5, u * 6 + k), .75, { th: 0, id: 6 }); } }));

// ═════ STÜDYO (dilek, bıçak) ═════
P('P015', (ctx, st) => sahne(ctx, st, { cam: CAM(1200, 520, 1.3), arka: () => stuArka(st), portre: 'G', on: () => DOR(1040, { h: 780, bas: .1 * io(p01(st, 0, 3)) }) }));
P('P016', (ctx, st) => sahne(ctx, st, { cam: CAM(1290, 420, 1.9 + .12 * st.p), arka: () => stuArka(st), portre: 'G', on: () => DOR(1040, { h: 1100, y: 1400 }) }), { yazi: { y: 160 } });
P('P019', (ctx, st) => { const u = io(p01(st, .3, 1.2)), y = io(p01(st, Wd('B08', 'Dorian') - st.at, Wd('B08', 'Dorian') - st.at + .5));
  sahne(ctx, st, { cam: CAM(1150, 540, 1.3), arka: () => stuArka(st), portre: 'G', on: () => { BASIL(900, { kolOn: { a: .3 + 2.0 * u - .6 * y, b: -.2 } }); DOR(640 + 140 * y, { yon: 1, arka: false, yuzTon: .04, ton: .03, kolOn: { a: .4 + 1.6 * y, b: -.3 }, kenar: .35 }); } }); }, { yazi: { y: 150 } });

// ═════ LONDRA ═════
P('P020', (ctx, st) => SET.dore(ctx, 'dore245', CAM(960, 400 + 200 * st.p, 1.0), 1920), { yazi: {} });
P('P033', (ctx, st) => levha(ctx, CAM(960, 540, 1.05 - .04 * st.p), () => { // opera: localar, avize
  INSAN.fill(SET.R(-400, -400, 2800, 1900), .04, { th: 0, id: 0 });
  for (let r = 0; r < 3; r++) for (let k = 0; k < 7; k++) { const x = 60 + k * 280, y = 260 + r * 230; INSAN.fill(SET.R(x, y, 230, 170), .02, { th: 0, id: 0 }); INSAN.fill(SET.R(x - 6, y + 160, 242, 22), .4, { th: 0, id: 9 }); for (let s = 0; s < 3; s++) INSAN.fill(SET.E2(x + 50 + s * 64, y + 120, 18, 22), .2 + .05 * s, { th: .9, id: 6 }); }
  const t = st.t; for (let k = 0; k < 12; k++) { const a = k / 12 * Math.PI * 2, x = 960 + Math.cos(a) * 160, y = 130 + Math.sin(a) * 40; INSAN.fill(SET.E2(x, y, 7, 14 + 3 * Math.sin(t * 8 + k)), 1, { th: Math.PI / 2, id: 3 }); }
  SET.isik({ x: 960, y: 130, r1: 700, a: .7 }); }));
P('P039', (ctx, st) => SET.dore(ctx, 'dore263', CAM(960, 520 - 60 * st.p, 1.0 + .06 * st.p), 1920), { over: null });
P('P040', (ctx, st) => levha(ctx, CAM(960, 560, 1), () => { // kalabalık döner
  INSAN.fill(SET.R(-400, -400, 2800, 1900), .1, { th: 0, id: 0 }); SET.isik({ x: 980, y: 300, r1: 900, a: .8 });
  const u = io(p01(st, Wd('D02', 'gören') - st.at, Wd('D02', 'gören') - st.at + 1));
  for (let k = 0; k < 9; k++) { const x = 120 + k * 210 + (k % 2) * 40; if (Math.abs(x - 980) < 160) continue; INSAN.adam({ x, y: 960 + (k % 3) * 20, h: 560 + (k % 3) * 40, yon: x < 980 ? 1 : -1, arka: false, ton: .05 + (k % 3) * .02, bas: u * (x < 980 ? .25 : .25), sapka: k % 2 === 0, kenar: .3 }); }
  DOR(980, { h: 640, y: 980, kenar: .6 }); }));
P('P045', (ctx, st) => SET.dore(ctx, 'dore275', CAM(960, 500 + 60 * st.p, 1.0), 1920), { yazi: {} });
P('P046', (ctx, st) => { const u = io(p01(st, 0, st.d * .7)); levha(ctx, CAM(960, 560, 1.15), () => {
  INSAN.fill(SET.R(-400, -400, 2800, 1900), .05, { th: 0, id: 0 });
  INSAN.fill(SET.R(930, 120, 14, 760), .02, { th: Math.PI / 2, id: 9 }); SET.alev(937, 140, st.t, 1.2); SET.isik({ x: 937, y: 150, r1: 760, a: .9 });
  for (let k = 0; k < 3; k++) INSAN.fill(SET.E2(960, 300 + k * 120, 900, 60), .5, { type: 'bend', ox: 0, oy: 300 + k * 120, a: 0, k: .0003, id: 2 });   // sis bantları
  DOR(700, { arka: false, yon: 1, kenar: .4, yuzTon: .04, ton: .03, sapka: true });
  INSAN.adam({ x: 1500 - 300 * u, y: 1000, h: 760, yon: -1, ton: .08, kenar: .5, kenarYan: -1, sapka: true, adim: u < 1 ? st.t * .8 : null, kolOn: { a: .05, b: .1 } });
  INSAN.fill(SET.R(1500 - 300 * u - 120, 760, 90, 70), .1, { th: 0, id: 9 });   // çanta
}); });
// G09: dışarıdan ev, gece
P('P076', (ctx, st) => levha(ctx, CAM(960, 520, 1.05), () => { INSAN.fill(SET.R(-400, -400, 2800, 1900), .03, { th: 0, id: 0 });
  INSAN.fill(SET.R(500, 80, 900, 900), .1, { th: 0, id: 9 }); for (let r = 0; r < 3; r++) for (let k = 0; k < 4; k++) INSAN.fill(SET.R(560 + k * 220, 140 + r * 260, 120, 180), (r === 0 && k === 2) ? .96 : .02, { th: Math.PI / 2, id: 10 });
  SET.isik({ x: 1060, y: 230, r1: 420, a: .8 });
  for (const [x, yn] of [[260, 1], [380, 1]]) INSAN.adam({ x: x + 40 * io(p01(st, 0, 1.2)), y: 1040, h: 560, yon: yn, sapka: true, ton: .04, bas: -.3 * io(p01(st, 1, 2)), kenar: null }); }));

// ═════ TİYATRO ═════
const SIB = (o = {}) => INSAN.kadin({ x: 1200, y: 920, h: 600, yon: -1, elbise: .8, ...o });
P('P021', (ctx, st) => levha(ctx, CAM(1000, 520, 1.05 + .03 * st.p), () => { SET.tiyatro({ t: st.t }); SIB({ kol: { a: .6 + .4 * Math.sin(st.t * .8), b: 1.4 } }); }), { yazi: {} });
P('P022', (ctx, st) => levha(ctx, CAM(700, 700, 1.5), () => { SET.tiyatro({ t: st.t, isik: .8 }); SIB({ h: 420, x: 1250, y: 900 }); SET.loca(); DOR(420, { y: 1300, h: 900, egim: .08 * io(p01(st, 0, 2)), kenar: .45 }); }));
P('P023', (ctx, st) => levha(ctx, CAM(960, 540, .82), () => { SET.tiyatro({ t: st.t }); SIB({ kol: { a: .05, b: .1 } }); SET.loca();
  for (const [x, o] of [[160, { sapka: false }], [330, { arka: true }], [500, { biyik: true }]]) INSAN.adam({ x, y: 1120, h: 520, yon: 1, ton: .04, kenar: .3, ...o }); }));
P('P024', (ctx, st) => levha(ctx, CAM(1180, 380, 2.0), () => { SET.tiyatro({ t: st.t }); SIB({ kol: { a: 2.4, b: .9 }, bas: .15 * io(p01(st, 0, 3)) }); }));
P('P025', (ctx, st) => { const u = io(p01(st, 0, st.d)); levha(ctx, CAM(960, 560, 1.15), () => { INSAN.fill(SET.R(-400, -400, 2800, 1900), .06, { th: 0, id: 0 }); SET.isik({ x: 1300, y: 300, r1: 700, a: .7 });
  for (let k = 0; k < 4; k++) INSAN.fill(SET.R(1400 + k * 90, 100, 60, 800), .2, { th: Math.PI / 2, id: 9 });   // kulis kulisleri
  INSAN.kadin({ x: 1150, y: 980, h: 620, yon: -1, kol: { a: 1.9, b: .3 }, elbise: .78 }); DOR(800 - 260 * u, { yon: -1, arka: false, ton: .03, yuzTon: .03, kenar: .35, kenarYan: 1, adim: u > 0 && u < 1 ? st.t * .9 : null }); }); }, { yazi: { y: 160 } });

// ═════ EV (hol, şafak) ═════
const EV_FR = { x: 1150, y: 150, s: .9 };
function evArka(st, o = {}) { SET.ev({ safak: o.safak ?? .3, panjur: o.panjur ?? 0 }); return SET.cerceve(EV_FR.x, EV_FR.y, EV_FR.s); }
P('P026', (ctx, st) => { const u = io(p01(st, 0, st.d * .7)); sahne(ctx, st, { cam: CAM(1000, 540, 1), arka: () => evArka(st, { safak: .2 }), portre: 'G', expo: .7, on: () => DOR(300 + 600 * u, { adim: u < 1 ? st.t * .9 : null, h: 740, bas: u > .95 ? .12 : 0 }) }); });
P('P027', (ctx, st) => sahne(ctx, st, { cam: CAM(EV_FR.x + 205, EV_FR.y + 330, 3.2), arka: () => evArka(st), portre: 'Z', gecis: { dan: 'G', t0: Wd('C07', 'çizgi') - .6 }, expo: .85 }));
P('P028', (ctx, st) => levha(ctx, CAM(960, 540, 1.6), () => { SET.ev({ safak: .4 }); INSAN.fill(SET.E2(1060, 520, 180, 240), .02, { th: .9, id: 6 });   // aynaya bakan baş (arkadan)
  const k = io(p01(st, 0, 1.2)); GR.save(); GR.frame(860, 640 - 60 * k, 0, 1, 1); INSAN.fill(SET.E2(0, 0, 170, 220), .45, { type: 'rad', cx: 0, cy: 0, id: 9 }); INSAN.fill(SET.E2(0, 0, 140, 190), .9, { th: 0, id: 10 }); GR.restore(); }));
P('P029', (ctx, st) => sahne(ctx, st, { cam: CAM(1300, 500, 1.4), arka: () => evArka(st, { safak: .6, panjur: io(p01(st, 0, 2.5)) }), portre: 'Z', expo: .9 + .2 * io(p01(st, 0, 2.5)) }));
P('P030', (ctx, st) => levha(ctx, CAM(960, 620, 1.7), () => { SET.ev({ safak: .5 }); INSAN.fill(SET.R(300, 700, 1300, 40), .25, { th: 0, id: 9 }); INSAN.fill(SET.R(700, 560, 520, 150), .9, { th: 0, id: 10 });
  const u = p01(st, 0, st.d); for (let k = 0; k < 6; k++) { const w = 460 * clamp(u * 6 - k); if (w > 0) INSAN.fill(SET.R(730, 585 + k * 20, w, 3), .2, { th: 0, id: 9 }); }
  const x = 730 + 460 * ((u * 6) % 1), y = 585 + Math.floor(u * 6) * 20; INSAN.fill(INSAN.F([[x, y], [x + 120, y - 160], [x + 132, y - 150], [x + 6, y + 6]]), .05, { th: 1, id: 9 }); }));
P('P031', (ctx, st) => { const u = io(p01(st, 0, 1.5)); levha(ctx, CAM(960, 540, 1), () => { SET.ev({ safak: .5 }); INSAN.fill(SET.R(1400, 120, 280 * (1 - u * .9), 780), .04, { th: Math.PI / 2, id: 9 }); SET.isik({ x: 1600, y: 500, r1: 500, a: .5 * u });
  HENRY(1560, { yon: -1, kenarYan: -1, sapka: true, kolOn: { a: .1, b: .1 } }); }); });

// ═════ SALON ═════
P('P032', (ctx, st) => levha(ctx, CAM(1200, 520, 1.6), () => { SET.salon({ t: st.t }); const h = HENRY(1180, { yon: -1, kenarYan: 1, egim: -.12, sigara: true, kolOn: { a: 2.0, b: -1.4 } }); duman(h.el[0] - 10, h.el[1], st.t, .8, -1); }), { yazi: { y: 160 } });
P('P038', (ctx, st) => levha(ctx, CAM(960, 640, 2.2), () => { SET.salon({ t: st.t }); INSAN.fill(SET.R(600, 700, 720, 30), .3, { th: 0, id: 9 });
  INSAN.fill(INSAN.F([[760, 560], [1160, 560], [1180, 700], [740, 700]]), .62, { th: 0, id: 9 }); const pg = (st.t * 1.5) % 1; INSAN.fill(INSAN.F([[960, 560], [960 + 200 * Math.cos(pg * Math.PI), 560 - 40 * Math.sin(pg * Math.PI)], [960 + 210 * Math.cos(pg * Math.PI), 700], [960, 700]]), .85, { th: 0, id: 10 }); }));
P('P047', (ctx, st) => levha(ctx, CAM(960, 560, 1.1), () => { SET.salon({ t: st.t }); BASIL(700, { yon: 1, kolOn: { a: 1.1 + .2 * Math.sin(st.t * 2), b: -.5 }, kolArka: { a: .8, b: -.3 } }); DOR(1500, { yon: -1, kenarYan: 1, kenar: .55 }); }), { yazi: { y: 160 } });
P('P048', (ctx, st) => levha(ctx, CAM(1500, 330, 2.4), () => { SET.salon({ t: st.t }); DOR(1500, { yon: -1, kenarYan: 1, kenar: .6, egim: .02 * Math.sin(st.t * 9) * io(p01(st, 0, 1.5)) }); }), { yazi: { y: 160 } });
P('P057', (ctx, st) => levha(ctx, CAM(960, 560, 1), () => { SET.salon({ t: st.t }); DOR(520, { h: 660, y: 940, egim: .25, kolOn: { a: 1.25 + .1 * Math.sin(st.t * 6), b: -.2 } }); HENRY(1140, { yon: -1, egim: -.3, kolOn: { a: .6, b: .2 }, sigara: true }); }), { yazi: {} });
P('P059', (ctx, st) => { const u = io(p01(st, 0, 1)); levha(ctx, CAM(700, 520, 1.4), () => { SET.salon({ t: st.t }); DOR(560, { h: 660, y: 940, egim: .25 - .25 * u, arka: u < .5, yon: u < .5 ? 1 : -1, ton: .03, yuzTon: .03, kenar: .35 }); HENRY(1140, { yon: -1, egim: -.3, kolOn: { a: .6, b: .2 }, sigara: true }); }); }, { yazi: { y: 150 } });
P('P060', (ctx, st) => levha(ctx, CAM(1150, 380, 2.0), () => { SET.salon({ t: st.t }); const h = HENRY(1140, { yon: -1, egim: -.3 + .03 * Math.sin(st.t * 7), kolOn: { a: 2.1, b: -1.5 }, sigara: true }); duman(h.el[0], h.el[1], st.t, .7, -1); }), { yazi: { y: 160 } });
P('P061', (ctx, st) => levha(ctx, CAM(520, 680, 2.4), () => { SET.salon({ t: st.t }); INSAN.fill(INSAN.F([[380, 590], [640, 590], [650, 600], [372, 600]]), .62, { th: 0, id: 9 }); INSAN.fill(SET.R(390, 540, 230, 50), .62, { th: 0, id: 9 });
  GR.save(); GR.frame(560, 470 + 20 * io(p01(st, 0, 1)), .2, 1, 1); INSAN.fill(INSAN.Sm([[-70, -20], [70, -30], [90, 30], [-60, 40]]), .5, { th: 0, id: 5 }); GR.restore(); }), { yazi: { y: 150 } });
P('P062', (ctx, st) => { const u = io(p01(st, 0, 1.5)); levha(ctx, CAM(960, 560, 1.05), () => { SET.salon({ t: st.t }); DOR(520, { h: 660, y: 940, egim: .25 }); HENRY(1140 - 60 * u, { yon: -1, egim: -.3 * (1 - u), kolOn: { a: .4, b: .3 } }); }); }, { yazi: { y: 150 } });

P('P058', (ctx, st) => { const u = io(p01(st, 0, st.d)); levha(ctx, CAM(960, 560, 1.2), () => { SET.bahce({ t: st.t }); for (let k = 0; k < 24; k++) { const q = ((st.lt * .3 + k / 24) % 1), x = 300 + (k * 131) % 1300, y = 200 + q * 760; INSAN.fill(SET.E2(x, y, 8, 5, q * 6 + k), .9, { th: 0, id: 6 }); }
  INSAN.kadin({ x: 1100 + 260 * u, y: 900, h: 420 - 80 * u, yon: 1, elbise: .7, kol: { a: .1, b: .1 } }); }); });
// ═════ ODA (taşıma, örtü, kilit, yıllar, ayna) ═════
P('P034', (ctx, st) => { const u = p01(st, 0, st.d); levha(ctx, CAM(960, 520, 1), () => { odaArka(st, { cerceveYok: true, lambaVar: false }); SET.isik({ x: 300, y: 300, r1: 900, a: .5 });
  const x = 200 + 900 * u; GR.save(); GR.frame(x, 330, -.05, 1, .8); INSAN.fill(SET.R(0, 0, 500, 720), .3, { th: Math.PI / 2, id: 9 }); GR.restore();
  for (const [dx, yn] of [[-60, 1], [520, 1]]) INSAN.adam({ x: x + dx, y: 1000, h: 640, yon: yn, arka: dx < 0, ton: .05, adim: st.t * .7, kolOn: { a: 2.6, b: .2 }, kenar: .3 }); }); });
P('P035', (ctx, st) => sahne(ctx, st, { cam: CAM(1340, 560, 1.5), arka: () => { const _M = odaArka(st); perde(1070, 100 - 760 * (1 - io(p01(st, 0, 1.0))));  return _M; } }));
P('P036', (ctx, st) => levha(ctx, CAM(960, 560, 2.6), () => { odaArka(st, { cerceveYok: true }); INSAN.fill(SET.R(700, 200, 520, 800), .2, { th: Math.PI / 2, id: 9 }); INSAN.fill(SET.E2(960, 600, 40, 40), .05, { th: 0, id: 9 }); INSAN.fill(INSAN.F([[952, 600], [968, 600], [972, 660], [948, 660]]), .02);
  const a = -1.5 * io(p01(st, 0, 1.2)); GR.save(); GR.frame(960, 600, a, 1, 1); INSAN.fill(INSAN.F([[-8, -10], [140, -10], [140, 10], [-8, 10]]), .7, { th: 0, id: 9 }); INSAN.fill(SET.E2(160, 0, 26, 26), .7, { th: 0, id: 9 }); GR.restore(); }));
P('P037', (ctx, st) => sahne(ctx, st, { cam: CAM(1340, 470, 2.0), arka: () => odaArka(st), portre: 'Y', gecis: { dan: 'Z', t0: st.at + .3 } }));
P('P041', (ctx, st) => { const u = io(p01(st, 0, 2)); levha(ctx, CAM(960, 540, 1), () => { odaArka(st, { lamba: { x: 500 + 300 * u, y: 640 }, cerceveYok: false }); perde(1070, 100); DOR(380 + 300 * u, { adim: u < 1 ? st.t : null, kolOn: { a: .9, b: -.4 } }); }); });
P('P042', (ctx, st) => sahne(ctx, st, { cam: CAM(1300, 420, 2.2), arka: () => odaArka(st), portre: 'Y', expo: .95, on: () => { GR.save(); GR.frame(1010, 520 + 10 * Math.sin(st.t), .3, 1, 1); INSAN.fill(SET.E2(0, 0, 70, 95), .45, { type: 'rad', cx: 0, cy: 0, id: 9 }); INSAN.fill(SET.E2(0, 0, 56, 80), .96, { th: 0, id: 10 }); GR.restore(); } }));
P('P043', (ctx, st) => sahne(ctx, st, { cam: CAM(1040, 540, 1.15), arka: () => odaArka(st), portre: 'C', gecis: { dan: 'Y', t0: st.at }, on: () => { const r = DOR(820, { bas: .3 * Math.sin(st.t * .9), kolOn: { a: 1.4, b: -.6 } }); GR.save(); GR.frame(r.el[0], r.el[1] - 30, .3, 1, 1); INSAN.fill(SET.E2(0, 0, 50, 68), .45, { type: 'rad', cx: 0, cy: 0, id: 9 }); INSAN.fill(SET.E2(0, 0, 40, 56), .96, { th: 0, id: 10 }); GR.restore(); } }));
P('P044', (ctx, st) => { const u = io(p01(st, 0, st.d)); levha(ctx, CAM(960, 540, 1), () => { odaArka(st, { isik: 1 - u }); perde(1070, 100); }); });

// ═════ ODA (Basil) ═════
P('P049', (ctx, st) => { const u = io(p01(st, 0, Math.min(st.d, 2.6))); levha(ctx, CAM(960, 540, 1), () => { odaArka(st, { lamba: { x: 300 + 605 * u, y: 1000 - 350 * u }, r1: 500 + 200 * u }); perde(1070, 100);
  INSAN.fill(INSAN.F([[200, 1100], [600, 700], [640, 720], [240, 1120]]), .04);   // merdiven gölgesi
  if (u < .98) INSAN.adam({ x: 240 + 600 * u, y: 1000, h: 720, yon: 1, arka: true, kenar: .4, adim: st.t, ton: .06 }); }); });
P('P050', (ctx, st) => { const d = Wd('E05', 'Basil') - st.at, u = io(p01(st, 0, 1.0));
  sahne(ctx, st, { cam: CAM(1100, 540, 1.1), arka: () => { const _M = odaArka(st); if (u < 1) perde(1070 - 120 * u, 100 + 400 * u * u, -.3 * u); else perdeYigin(820, 960);  return _M; }, portre: 'C',
    maske: u < 1 ? (mx => { const c = camOf(CAM(1100, 540, 1.1)), z = c.s; mx.setTransform(z, 0, 0, z, -c.x * z, -c.y * z); mx.translate(1070 - 120 * u, 100 + 400 * u * u); mx.rotate(-.3 * u); mx.fillRect(-8, 0, 556, 760); }) : null,
    on: () => { BASIL(560, { kolOn: { a: .2, b: .1 }, egim: .05 * io(p01(st, d, d + 1)) }); } }); });
P('P051', (ctx, st) => sahne(ctx, st, { cam: CAM(1250, 720, 4.0 - .4 * st.p), arka: () => odaArka(st), portre: 'C' }));
P('P052', (ctx, st) => levha(ctx, CAM(900, 540, 1.15), () => { odaArka(st); perdeYigin(820, 960); BASIL(1100, { yon: -1, kenarYan: 1, kolOn: { a: .8, b: -.3 }, kolArka: { a: .6, b: -.2 } }); DOR(560, { kenar: .3 }); }), { yazi: { y: 160 } });
P('P053', (ctx, st) => sahne(ctx, st, { cam: CAM(1300, 470, 2.4 + .3 * st.p), arka: () => odaArka(st), portre: 'C', on: () => DOR(1020, { h: 1200, y: 1500, kenar: .2 }) }));
P('P054', (ctx, st) => levha(ctx, CAM(1760, 790, 3.2), () => { odaArka(st); GR.save(); GR.frame(1780, 790, -.1, 1, 1); INSAN.fill(INSAN.F([[-90, -6], [40, -6], [46, 0], [40, 6], [-90, 6]]), .85, { th: 0, id: 9 }); INSAN.fill(SET.R(40, -10, 70, 20), .1, { th: 0, id: 9 }); GR.restore();
  SET.isik({ x: 1760, y: 790, r1: 80 + 30 * Math.sin(st.t * 5), a: .6 }); }));
P('P055', (ctx, st) => { const u = p01(st, 0, 1.4); levha(ctx, CAM(960, 540, 1), () => { odaArka(st, { isik: u < .7 ? 1 : 0 });
  GR.tx.save(); GR.tx.globalCompositeOperation = 'multiply'; GR.tx.fillStyle = 'rgba(0,0,0,.0)'; GR.tx.restore();
  // duvarda iki gölge: biri yükselir
  const gx = 600, gy = 260; INSAN.fill(INSAN.Sm([[gx, gy + 400], [gx + 80, gy + 60 - 120 * io(u)], [gx + 200, gy - 40 - 140 * io(u)], [gx + 260, gy + 380]]), .02); INSAN.fill(INSAN.Sm([[gx + 420, gy + 420], [gx + 460, gy + 180], [gx + 560, gy + 140], [gx + 600, gy + 420]]), .03); }); });
P('P056', (ctx, st) => levha(ctx, CAM(960, 540, 1), () => { odaArka(st, { lambaVar: false }); perde(1070, 100); SET.huzme([[0, 0], [400, 0], [1200, 1080], [500, 1080]], .25); }));

// ═════ EV (ayna, suç) ═════
P('P063', (ctx, st) => levha(ctx, CAM(960, 560, 1.05), () => { SET.salon({ t: st.t }); DOR(980, { h: 700, kenar: .55, kenarYan: 1 }); }));
P('P064', (ctx, st) => { const d = Wd('G01', 'çalar') - st.at; levha(ctx, CAM(960, 520, 1.5), () => { SET.salon({ t: st.t, ates: true }); INSAN.fill(SET.E2(1060, 560, 190, 250), .02, { th: .9, id: 6 });
  GR.save(); GR.frame(820, 560 - 30 * io(p01(st, 0, 1)), .05, 1, 1); INSAN.fill(SET.E2(0, 0, 180, 230), .5, { type: 'rad', cx: 0, cy: 0, id: 9 }); INSAN.fill(SET.E2(0, 0, 148, 196), .95, { th: 0, id: 10 }); for (const a of [-2.4, -.7, .7, 2.4]) INSAN.fill(SET.E2(Math.cos(a) * 170, Math.sin(a) * 215, 26, 30), .7, { type: 'rad', cx: Math.cos(a) * 170, cy: Math.sin(a) * 215, id: 6 }); GR.restore(); }); }, { yazi: { y: 160 } });
P('P065', (ctx, st) => levha(ctx, CAM(960, 760, 1.6), () => { SET.salon({ t: st.t }); for (let k = 0; k < 40; k++) { const u = clamp(st.lt / .8), a = k * 2.399, r = 30 + (k * 37) % 300 * u, x = 900 + Math.cos(a) * r, y = 880 + Math.sin(a) * r * .25 - 120 * (1 - u) * (k % 2); INSAN.fill(INSAN.F([[x, y], [x + 18 + (k % 5) * 6, y - 4], [x + 8, y + 10]]), .95, { th: 0, id: 10 }); } }));
P('P066', (ctx, st) => { const ks = [Wd('G02', 'her') , Wd('G02', 'Basil'), Wd('G02', 'Henri')].map(w => w - st.at); levha(ctx, CAM(960, 560, 1.05), () => { SET.salon({ t: st.t, ates: false }); DOR(960, { h: 720, kenar: .4 });
  const xs = [380, 960, 1540]; ks.forEach((k, i) => { const a = clamp((st.lt - k) / .6); if (a > 0) SET.isik({ x: xs[i], y: 520, r1: 300, a: .8 * a }); });
  INSAN.fill(SET.R(260, 300, 240, 340), .12, { th: Math.PI / 2, id: 9 });   // perdeli tablo (küçük)
  INSAN.fill(SET.E2(1540, 560, 110, 70), .35, { th: 0, id: 9 }); }); });
P('P067', (ctx, st) => levha(ctx, CAM(1400, 500, 2.2), () => { SET.salon({ t: st.t }); INSAN.fill(INSAN.F([[1300, 520], [1520, 520], [1530, 560], [1290, 560]]), .62, { th: 0, id: 9 }); SET.isik({ x: 1410, y: 520, r1: 260, a: .9 }); }));
P('P068', (ctx, st) => { const u = io(p01(st, 0, Math.min(st.d, 2.6))); levha(ctx, CAM(960, 540, 1), () => { odaArka(st, { lamba: { x: 300 + 605 * u, y: 1000 - 350 * u }, r1: 500 + 200 * u }); perde(1070, 100); }); });

// ═════ ODA (son) ═════
P('P069', (ctx, st) => { const u = io(p01(st, .2, 1.2));
  sahne(ctx, st, { cam: CAM(1060, 540, 1.05), arka: () => { const _M = odaArka(st); if (u < 1) perde(1070 - 140 * u, 100 + 420 * u * u, -.3 * u); else perdeYigin(820, 960);  return _M; }, portre: 'C',
    maske: u < 1 ? (mx => { const c = camOf(CAM(1060, 540, 1.05)), z = c.s; mx.setTransform(z, 0, 0, z, -c.x * z, -c.y * z); mx.translate(1070 - 140 * u, 100 + 420 * u * u); mx.rotate(-.3 * u); mx.fillRect(-8, 0, 556, 760); }) : null,
    on: () => DOR(700, { kolOn: { a: 1.0 - .6 * u, b: -.2 } }) }); });
P('P070', (ctx, st) => sahne(ctx, st, { cam: CAM(1310, 420, 2.6), arka: () => odaArka(st), portre: 'I', gecis: { dan: 'C', t0: Wd('G04', 'sinsilik') - .3 } }));
P('P071', (ctx, st) => sahne(ctx, st, { cam: CAM(1200, 560, 1.4), arka: () => odaArka(st), portre: 'I', on: () => DOR(1580, { yon: -1, kenarYan: -1, h: 840, arka: false, ton: .02, yuzTon: .02, kenar: .4, bas: -.1 }) }));
P('P072', (ctx, st) => sahne(ctx, st, { cam: CAM(1000, 560, 1.15), arka: () => odaArka(st), portre: 'I', on: () => DOR(720, { egim: .02 * Math.sin(st.t * 10) * (1 - p01(st, 0, st.d)), kolOn: { a: .2, b: .1 } }) }));
P('P073', (ctx, st) => sahne(ctx, st, { cam: CAM(1340, 420, 2.2 + .5 * st.p), arka: () => odaArka(st), portre: 'I' }));
P('P074', (ctx, st) => levha(ctx, CAM(1760, 790, 3.6), () => { odaArka(st); GR.save(); GR.frame(1780, 790, -.1, 1, 1); INSAN.fill(INSAN.F([[-90, -6], [40, -6], [46, 0], [40, 6], [-90, 6]]), .95, { th: 0, id: 9 }); INSAN.fill(SET.R(40, -10, 70, 20), .1, { th: 0, id: 9 }); GR.restore(); SET.isik({ x: 1730, y: 790, r1: 60 + 40 * Math.abs(Math.sin(st.t * 4)), a: .8 }); }));
P('P075', (ctx, st) => { const u = io(p01(st, 0, Math.max(.5, st.d - .3))); sahne(ctx, st, { cam: CAM(1160, 520, 1.25), arka: () => odaArka(st), portre: 'I',
  on: () => { const r = DOR(820, { kolOn: { a: .3 + 1.2 * u, b: -.3 - .4 * u }, egim: .05 * u }); GR.save(); GR.frame(r.el[0], r.el[1], -1.2 + 1.6 * u, 1, 1); INSAN.fill(INSAN.F([[0, -5], [130, -5], [136, 0], [130, 5], [0, 5]]), .95, { th: 0, id: 9 }); GR.restore(); } }); });
P('P079', (ctx, st) => levha(ctx, CAM(960, 760, 2.4), () => { odaArka(st, { isik: .7 }); GR.save(); GR.frame(940, 930, .1, 1, 1);
  INSAN.fill(INSAN.Sm([[-160, -40], [40, -50], [120, -30], [170, -10], [160, 20], [40, 30], [-160, 40]]), .55, { th: .2, id: 5 });   // buruşmuş el (gravür)
  for (const [x, y] of [[60, -50], [100, -46], [134, -34], [150, -16]]) INSAN.fill(INSAN.F([[x, y], [x + 50, y + 4], [x + 52, y + 16], [x, y + 12]]), .5, { th: .2, id: 5 });
  INSAN.fill(SET.E2(80, -38, 12, 16), .92, { th: 0, id: 10 }); INSAN.fill(SET.E2(112, -32, 12, 15), .92, { th: 0, id: 10 });   // yüzükler
  for (let k = 0; k < 7; k++) INSAN.fill(INSAN.F([[-140 + k * 30, -30], [-110 + k * 30, -24], [-112 + k * 30, -22]]), .2, { th: 0, id: 5 }); GR.restore(); }));
P('P080', (ctx, st) => sahne(ctx, st, { cam: CAM(1100, 560, 1.0 + .04 * st.p), arka: () => { const _M = odaArka(st, { isik: .6 }); INSAN.fill(INSAN.Sm([[760, 990], [1000, 950], [1200, 990], [1180, 1030], [780, 1030]]), .02);  return _M; }, portre: 'G', expo: .9 }));
P('P077', (ctx, st) => { const u = io(p01(st, 0, 1.6)); sahne(ctx, st, { cam: CAM(1100, 540, 1.05), arka: () => { const _M = odaArka(st, { isik: .5 + .5 * u });  return _M; }, portre: 'G', gecis: { dan: 'I', t0: st.at - 1.0 }, on: () => { for (const [x, yn] of [[260, 1], [420, 1]]) INSAN.adam({ x: x + 120 * u, y: 1000, h: 700, yon: yn, ton: .05, kenar: .35, arka: false, kolOn: { a: .5, b: .2 } }); } }); });
P('P078', (ctx, st) => sahne(ctx, st, { cam: CAM(1300, 470, 2.0 + .25 * st.p), arka: () => odaArka(st, { isik: 1 }), portre: 'G' }));

// ═════ MAHKEME ve iksir ═════
P('P081', (ctx, st) => levha(ctx, CAM(960, 540 - 30 * st.p, 1 + .05 * st.p), () => { kagitArka(); INSAN.fill(SET.R(600, 30, 720, 1020), .92, { th: 0, id: 10 }); SET.fotoGravur('sarony18', 640, 60, 640, { kirp: [120, 160, 2040, 3360], kontrast: 1.5 }); }, [.07, 0, 0]), { yazi: {} });
P('P082', (ctx, st) => levha(ctx, CAM(960, 540, 1.0 + .03 * st.p), () => SET.mahkeme()), { yazi: { px: 40 } });
P('P083', (ctx, st) => levha(ctx, CAM(1000, 520, 1.4), () => { SET.mahkeme(); const h = INSAN.adam({ x: 820, y: 1000, h: 800, yon: 1, ton: .06, kenar: .45, kolOn: { a: 1.4, b: -.9 }, sakal: false });
  INSAN.fill(SET.E2(820 + 8, 1000 - 800 * .92, 70, 50), .85, { type: 'bend', ox: 760, oy: 230, a: 0, k: .01, id: 6 });   // peruk
  GR.save(); GR.frame(h.el[0] + 10, h.el[1] - 20, -.2, 1, 1); INSAN.fill(SET.R(0, -110, 150, 200), .88, { th: 0, id: 10 }); for (let k = 0; k < 8; k++) INSAN.fill(SET.R(14, -90 + k * 22, 120, 3), .3, { th: 0, id: 9 }); GR.restore(); }));
P('P084', (ctx, st) => levha(ctx, CAM(960, 540, 1), () => { kagitArka(); INSAN.fill(SET.R(360, 80, 1200, 920), .92, { th: 0, id: 10 }); }, [.07, 0, 0]), { over: (ctx, st) => {
  const c = `rgb(${GR.INK})`; txt(ctx, 'THE PREFACE', W / 2, 200, { px: 46, col: c, ls: 8, a: clamp(st.lt / .6) });
  ctx.save(); ctx.font = FONT.alinti(52); ctx.fillStyle = c; ctx.textAlign = 'center'; ctx.globalAlpha = clamp((st.lt - .4) / .8); ctx.fillText('There is no such thing as a moral or an immoral book.', W / 2, 330); ctx.fillText('Books are well written, or badly written. That is all.', W / 2, 400); ctx.restore();
  quote(ctx, (PS.P084 || {}).yazi, W / 2, 640, st.lt, { px: 60, col: '#7a1e14', panel: false, t0: 1.6, maxW: 1100 }); } });
P('P085', (ctx, st) => levha(ctx, CAM(960, 540, 1.15), () => { SET.mahkeme(); INSAN.fill(SET.R(1150, 600, 360, 400), .08, { th: 0, id: 9 }); SET.isik({ x: 1330, y: 300, r1: 500, a: .7 });
  INSAN.adam({ x: 1330, y: 900, h: 640, yon: -1, ton: .05, kenar: .6, kenarYan: -1, kolOn: { a: .1, b: .1 } }); }), { yazi: { y: 160 } });
P('P086', (ctx, st) => sahne(ctx, st, { cam: CAM(1100, 520, 1.05), arka: () => { const _M = odaArka(st); perde(1070, 100);  return _M; } }));
P('P087', (ctx, st) => { const u = io(p01(st, 1.5, st.d)); levha(ctx, CAM(960, 540, 1.05), () => { kagitArka(); INSAN.fill(SET.R(640, 40, 640, 1000), .92, { th: 0, id: 10 }); SET.fotoGravur('sarony23', 680, 70, 560, { kirp: [140, 80, 1880, 3150], kontrast: 1.6, parlak: 1.05 - .7 * u }); }, [.07, 0, 0]); }, { yazi: {} });
P('P088', (ctx, st) => { const ks = ['Basil', 'Henri', 'Dorian'].map((w, i) => Wd('G15', w, i === 2 ? 0 : 0) - st.at);
  levha(ctx, CAM(960, 560, 1), () => { kagitArka(); const xs = [440, 960, 1480]; ks.forEach((k, i) => { const a = clamp((st.lt - k) / .7); if (a > 0) SET.isik({ x: xs[i], y: 520, r1: 360, a: .9 * a }); });
    BASIL(440, { h: 600, y: 880 }); HENRY(960, { h: 640, y: 880, sapka: true, sigara: true }); DOR(1480, { h: 600, y: 880 }); }); }, { over: (ctx, st) => {
  const ks = ['Basil', 'Henri', 'Dorian'].map(w => Wd('G15', w) - st.at), ls = [['BASIL', 'olduğumu sandığım'], ['LORD HENRY', 'dünyanın beni sandığı'], ['DORIAN', 'olmak istediğim']], xs = [440, 960, 1480];
  ks.forEach((k, i) => { const a = clamp((st.lt - k) / .6); if (a <= 0) return; txt(ctx, ls[i][0], xs[i], 150, { px: 44, ls: 6, a }); ctx.save(); ctx.globalAlpha *= a; ctx.font = FONT.alinti(44); ctx.fillStyle = `rgb(${GR.PAPER})`; ctx.textAlign = 'center'; ctx.fillText(ls[i][1], xs[i], 210); ctx.restore(); }); } });
P('P089', (ctx, st) => sahne(ctx, st, { cam: CAM(1340, 470, 1.9), arka: () => odaArka(st), portre: 'G' }));
P('P090', (ctx, st) => sahne(ctx, st, { cam: CAM(1250, 500, 1.5 + .1 * st.p), arka: () => odaArka(st), portre: 'G' }), { over: (ctx, st) => etiket(ctx, 'GÜZELLİK BİR LANET Mİ?', 560, 300, st.lt, st.d, { px: 58 }) });
P('P091', (ctx, st) => sahne(ctx, st, { cam: CAM(1100, 540, 1 + .03 * st.p), arka: () => stuArka(st, { isik: .8 }), portre: 'G' }), { yazi: { y: 160 } });
P('P092', (ctx, st) => sahne(ctx, st, { cam: CAM(1340, 470, 2.0), arka: () => odaArka(st), portre: 'C', gecis: { dan: 'G', t0: Wd('G16', 'Ama') - .2 } }));
P('P093', (ctx, st) => levha(ctx, CAM(1000, 520, 1.05 - .03 * st.p), () => { odaArka(st); perde(1070, 100); }), { over: (ctx, st) => etiket(ctx, 'KİMSE GÖRMESEYDİ?', 560, 300, st.lt, st.d, { px: 58 }) });
P('P094', (ctx, st) => levha(ctx, CAM(1500, 540, 1.0), () => { odaArka(st, { isik: .7 }); perde(1070, 100); }), { over: null });   // bitiş ekranı: sol yarı boş (YouTube öğeleri)

// eksik plan kimlikleri (taslakta çizilmemiş) uyarısı
window.initScenes = () => { const var_ = new Set(SHOTS.map(s => s.id)); const eksik = Object.keys(PS).filter(k => !var_.has(k)); if (eksik.length) console.warn('çizilmemiş planlar: ' + eksik.join(' ')); };
