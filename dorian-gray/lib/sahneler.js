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
P('P017', (ctx, st) => { const sx = [60, 512, 920, 190]; SET.belge(ctx, 'lippDilek', CAM(960, 540, 1.0 + .05 * st.p), 160, 375, 1600, { kirp: sx });
  // dilek: "For this—for this—I would give / everything!" (Lippincott 1890, s.19); "kill myself" satırı kadraj dışında
  const u = io(p01(st, .6, 2.6)), v = io(p01(st, 2.6, 3.2)); ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalCompositeOperation = 'multiply'; ctx.fillStyle = 'rgba(40,30,20,.35)'; ctx.fillRect(0, 0, DW, DH);
  ctx.fillStyle = 'rgb(255,214,130)'; ctx.fillRect(845 * RS, 610 * RS, 695 * u * RS, 48 * RS); ctx.fillRect(176 * RS, 660 * RS, 228 * v * RS, 48 * RS); ctx.restore(); }, { over: null });
// P018 B07@Vayld: 1890 / 1891 iki satır
P('P018', (ctx, st) => { levha(ctx, CAM(960, 540, 1), () => { kagitArka(); INSAN.fill(SET.R(260, 220, 1400, 640), .9, { th: 0, id: 10 }); }, [.07, 0, 0]); }, {
  over: (ctx, st) => { const c = `rgb(${GR.INK})`; txt(ctx, '1890', 520, 420, { px: 72, col: c, a: clamp(st.lt / .5) }); quote(ctx, '“…her şeyi verirdim!”', 1080, 420, st.lt, { px: 64, col: c, panel: false });
    txt(ctx, '1891', 520, 640, { px: 72, col: c, a: clamp((st.lt - 1.6) / .5) }); quote(ctx, '“…ruhumu verirdim!”', 1080, 640, st.lt, { px: 64, col: '#7a1e14', panel: false, t0: 1.6 }); } });

// ═════ STÜDYO ═════
const STU_SV = { x: 1060, y: 150, s: .92 };
function stuArka(st, o = {}) { SET.studyo({ isik: o.isik ?? 1 }); const Mf = SET.sovale(STU_SV.x, STU_SV.y, STU_SV.s); return Mf; }
const BASIL = (x, o = {}) => INSAN.adam({ x, y: 1000, h: 760, yon: o.yon ?? 1, arka: false, ton: .04, kenar: .6, kenarYan: 1, sakal: false, ...o });
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

// P011 B03@etkilemek: duman Dorian'ın kulağına
P('P011', (ctx, st) => levha(ctx, CAM(1250, 380, 2.2), () => { SET.studyo({ isik: .8 }); DOR(1300, { y: 1000, h: 760 }); const u = io(p01(st, 0, st.d)); for (let k = 0; k < 14; k++) { const q = k / 14; if (q > u) break; const x = 900 + q * 400, y = 330 + Math.sin(q * 6 + st.t) * 18 - q * 20; INSAN.fill(SET.E2(x, y, 22, 8, .2), .8, { type: 'bend', ox: x - 20, oy: y, a: 0, k: .006, id: 2 }); } }));

// ═════ BAHÇE ═════
P('P012', (ctx, st) => SET.dore(ctx, 'dore169', CAM(960, 500 + 120 * st.p, 1.0), 1920), { over: null });
P('P013', (ctx, st) => { const c = CAM(960, 760, 1.25); SET.dore(ctx, 'dore169', c, 1920); onKatman(ctx, c, () => { HENRY(760, { y: 1400, h: 900, yon: 1, kolOn: { a: .9 + .3 * Math.sin(st.t * 1.6), b: -.6 }, sapka: true, kenar: .7 }); DOR(1180, { y: 1400, h: 880, yon: -1, kenarYan: -1, kenar: .7 }); }); }, { yazi: { y: 160 } });


// ═════ STÜDYO (dilek, bıçak) ═════
P('P015', (ctx, st) => sahne(ctx, st, { cam: CAM(1200, 520, 1.3), arka: () => stuArka(st), portre: 'G', on: () => DOR(1040, { h: 780, bas: .1 * io(p01(st, 0, 3)) }) }));
P('P016', (ctx, st) => sahne(ctx, st, { cam: CAM(1290, 420, 1.9 + .12 * st.p), arka: () => stuArka(st), portre: 'G', on: () => DOR(1040, { h: 1100, y: 1400 }) }), { yazi: { y: 160 } });


// ═════ LONDRA ═════
P('P020', (ctx, st) => SET.dore(ctx, 'dore245', CAM(960, 400 + 200 * st.p, 1.0), 1920), { yazi: {} });



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

P('P062', (ctx, st) => { const u = io(p01(st, 0, 1.5)); levha(ctx, CAM(960, 560, 1.05), () => { SET.salon({ t: st.t }); DOR(520, { h: 660, y: 940, egim: .25 }); HENRY(1140 - 60 * u, { yon: -1, egim: -.3 * (1 - u), kolOn: { a: .4, b: .3 } }); }); }, { yazi: { y: 150 } });


// ═════ ODA (taşıma, örtü, kilit, yıllar, ayna) ═════
P('P034', (ctx, st) => { const u = p01(st, 0, st.d); levha(ctx, CAM(960, 520, 1), () => { odaArka(st, { cerceveYok: true, lambaVar: false }); SET.isik({ x: 300, y: 300, r1: 900, a: .5 });
  const x = 200 + 900 * u; GR.save(); GR.frame(x, 330, -.05, 1, .8); INSAN.fill(SET.R(0, 0, 500, 720), .3, { th: Math.PI / 2, id: 9 }); GR.restore();
  for (const [dx, yn] of [[-60, 1], [520, 1]]) INSAN.adam({ x: x + dx, y: 1000, h: 640, yon: yn, arka: dx < 0, ton: .05, adim: st.t * .7, kolOn: { a: 2.6, b: .2 }, kenar: .3 }); }); });
P('P035', (ctx, st) => sahne(ctx, st, { cam: CAM(1340, 560, 1.5), arka: () => { const _M = odaArka(st); perde(1070, 100 - 760 * (1 - io(p01(st, 0, 1.0))));  return _M; } }));

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

P('P075', (ctx, st) => { const u = io(p01(st, 0, Math.max(.5, st.d - .3))); sahne(ctx, st, { cam: CAM(1160, 520, 1.25), arka: () => odaArka(st), portre: 'I',
  on: () => { const r = DOR(820, { kolOn: { a: .3 + 1.2 * u, b: -.3 - .4 * u }, egim: .05 * u }); GR.save(); GR.frame(r.el[0], r.el[1], -1.2 + 1.6 * u, 1, 1); INSAN.fill(INSAN.F([[0, -5], [130, -5], [136, 0], [130, 5], [0, 5]]), .95, { th: 0, id: 9 }); GR.restore(); } }); });

P('P080', (ctx, st) => sahne(ctx, st, { cam: CAM(1100, 560, 1.0 + .04 * st.p), arka: () => { const _M = odaArka(st, { isik: .6 }); INSAN.fill(INSAN.Sm([[760, 990], [1000, 950], [1200, 990], [1180, 1030], [780, 1030]]), .02);  return _M; }, portre: 'G', expo: .9 }));
P('P077', (ctx, st) => { const u = io(p01(st, 0, 1.6)); sahne(ctx, st, { cam: CAM(1100, 540, 1.05), arka: () => { const _M = odaArka(st, { isik: .5 + .5 * u });  return _M; }, portre: 'G', gecis: { dan: 'I', t0: st.at - 1.0 }, on: () => { for (const [x, yn] of [[260, 1], [420, 1]]) INSAN.adam({ x: x + 120 * u, y: 1000, h: 700, yon: yn, ton: .05, kenar: .35, arka: false, kolOn: { a: .5, b: .2 } }); } }); });
P('P078', (ctx, st) => sahne(ctx, st, { cam: CAM(1300, 470, 2.0 + .25 * st.p), arka: () => odaArka(st, { isik: 1 }), portre: 'G' }));

// ═════ MAHKEME ve iksir ═════
P('P081', (ctx, st) => levha(ctx, CAM(960, 540 - 30 * st.p, 1 + .05 * st.p), () => { kagitArka(); INSAN.fill(SET.R(600, 30, 720, 1020), .92, { th: 0, id: 10 }); SET.fotoGravur('sarony18', 640, 60, 640, { kirp: [120, 160, 2040, 3360], kontrast: 1.5 }); }, [.07, 0, 0]), { yazi: {} });
P('P082', (ctx, st) => levha(ctx, CAM(960, 540, 1.0 + .03 * st.p), () => SET.mahkeme()), { yazi: { px: 40 } });

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

// ═════ düzeltilmiş planlar (kurgu özeti 1) ═════
// Henry: divanın kenarında yarı oturur, sigara; duman tavana
P('P010', (ctx, st) => levha(ctx, CAM(760, 600, 1.15), () => { SET.studyo({ isik: .6 }); const h = HENRY(480, { yon: 1, egim: -.08, h: 820, kolOn: { a: 2.3, b: -1.7 }, kolArka: { a: -.2, b: .4 }, sigara: true, kenar: .65 }); duman(h.el[0] + 10, h.el[1] - 10, st.t, 1, 1); }), { yazi: {} });
// leylak yerine Doré bahçesinin yakın yaprakları + düşen yapraklar
P('P014', (ctx, st) => { const c = CAM(700, 1300, 2.0 + .1 * st.p); SET.dore(ctx, 'dore169', c, 1920); onKatman(ctx, c, () => { for (let k = 0; k < 22; k++) { const t0 = k * .25, u = clamp((st.lt - t0) / 3); if (u <= 0) continue; const x = 520 + (k * 97) % 380 + Math.sin(u * 6 + k) * 30, y = 1060 + u * 520; INSAN.fill(SET.E2(x, y, 9, 5, u * 6 + k), .95, { th: 0, id: 6 }); } }); }, { over: null });
P('P058', (ctx, st) => { const u = io(p01(st, 0, st.d)), c = CAM(1300, 900, 1.3); SET.dore(ctx, 'dore169', c, 1920); onKatman(ctx, c, () => INSAN.kadin({ x: 1240 + 220 * u, y: 1380, h: 520 - 90 * u, yon: 1, elbise: .85, kol: { a: .1, b: .1 } })); }, { over: null });
// bıçak: Basil sağda, Dorian soldan gelir; eller tuvalin önünde buluşur
P('P019', (ctx, st) => { const u = io(p01(st, .3, 1.2)), w0 = Wd('B08', 'Dorian') - st.at, y = io(p01(st, w0, w0 + .5));
  sahne(ctx, st, { cam: CAM(1150, 540, 1.3), arka: () => stuArka(st), portre: 'G', on: () => { const b = BASIL(1500, { yon: -1, kenarYan: -1, kolOn: { a: .3 + 1.9 * u, b: -.3 } }); GR.save(); GR.frame(b.el[0], b.el[1], -1.2 + .4 * u, 1, 1); INSAN.fill(INSAN.F([[0, -4], [-120, -4], [-126, 0], [-120, 4], [0, 4]]), .95, { th: 0, id: 9 }); GR.restore();
    DOR(560 + 420 * y, { arka: true, kenar: .5, kolOn: { a: .4 + 1.5 * y, b: -.4 }, adim: y > 0 && y < 1 ? st.t * 1.4 : null }); } }); }, { yazi: { y: 150 } });
// Doré gece: levhanın alt yarısı (insanlar)

// kalabalık: üç sıra derinlik, boy ve yön çeşitli, üst üste biner; Dorian ışıkta, sırtı dönük
P('P040', (ctx, st) => levha(ctx, CAM(960, 560, 1), () => { INSAN.fill(SET.R(-400, -400, 2800, 1900), .1, { th: 0, id: 0 }); SET.isik({ x: 960, y: 260, r1: 1000, a: .85 });
  const g = Wd('D02', 'gören') - st.at, u = io(p01(st, g, g + 1.2));
  const K = [[180, 880, 470, 1, .1], [420, 900, 500, -1, .3], [1500, 885, 480, -1, .2], [1720, 905, 520, -1, .05], [80, 1010, 640, 1, .25], [300, 1040, 700, 1, .05], [1640, 1030, 690, -1, .15], [1880, 1060, 740, -1, .3]];
  K.forEach(([x, y, h, yn, dl], i) => INSAN.adam({ x, y, h, yon: yn, arka: i % 3 === 2, ton: .03, kenar: .4, kenarYan: x < 960 ? 1 : -1, sapka: i % 2 === 0, bas: (x < 960 ? .22 : .22) * io(p01(st, g + dl, g + dl + 1)), kolOn: { a: .05 + .1 * (i % 2), b: .1 } }));
  DOR(960, { h: 620, y: 960, kenar: .7 }); }), { over: null });
// anahtar: kilitte ışık havuzu, döner ve çıkar
P('P036', (ctx, st) => levha(ctx, CAM(960, 560, 2.4), () => { INSAN.fill(SET.R(-400, -400, 2800, 1900), .06, { th: Math.PI / 2, id: 9 }); SET.isik({ x: 960, y: 580, r1: 420, a: .9 });
  INSAN.fill(SET.R(860, 480, 200, 260), .45, { th: 0, id: 9 }); INSAN.fill(SET.E2(960, 560, 22, 22), .02); INSAN.fill(INSAN.F([[952, 560], [968, 560], [972, 610], [948, 610]]), .02);
  const a = -1.57 * io(p01(st, .2, 1.4)), dx = 120 * io(p01(st, 2.6, 3.6)); GR.save(); GR.frame(960 + dx, 575, a, 1, 1);
  INSAN.fill(INSAN.F([[-6, -5], [110, -5], [110, 5], [-6, 5]]), .82, { th: 0, id: 9 }); INSAN.fill(SET.E2(140, 0, 30, 30), .82, { th: 0, id: 9 }); INSAN.fill(SET.E2(140, 0, 14, 14), .06); INSAN.fill(SET.R(20, 5, 14, 18), .82, { th: 0, id: 9 }); GR.restore(); }), { over: null });
// bıçak (sandık üstünde): büyük, ışıkta parlar
function bicakPlan(ctx, st, z) { levha(ctx, CAM(1760, 780, z), () => { SET.oda(); SET.isik({ x: 1700, y: 760, r1: 380, a: .85 });
  GR.save(); GR.frame(1760, 790, -.12, 1, 1); INSAN.fill(INSAN.F([[-150, -9], [60, -9], [72, 0], [60, 9], [-150, 9]]), .95, { th: 0, id: 9 }); INSAN.fill(INSAN.F([[60, -16], [74, -16], [74, 16], [60, 16]]), .1, { th: 0, id: 9 }); INSAN.fill(INSAN.F([[74, -9], [200, -11], [206, 0], [200, 11], [74, 9]]), .08, { th: 0, id: 9 }); GR.restore();
  const g = .6 + .4 * Math.sin(st.t * 3); INSAN.fill(INSAN.F([[1650, 782], [1700, 778], [1650, 786]]), 1, { th: 0, id: 10 }); SET.isik({ x: 1660, y: 782, r1: 60 * g, a: .8 }); }); }
P('P054', (ctx, st) => bicakPlan(ctx, st, 3.0), { over: null });
P('P074', (ctx, st) => bicakPlan(ctx, st, 3.4), { over: null });
// duvardaki gölgeler: lamba alçakta, iki büyük gölge duvarda; biri ötekinin üstüne kalkar; lamba söner (kan yok)

// sarı kitap: yakın, ışık havuzunda (gravür: renk yok)



// yerdeki el: koyu kol yeninin ucunda kırışık el (gravür çizgileri), iki parlak yüzük; yüz yok, kan yok

// ═════ düzeltilmiş planlar (kurgu özeti 2) ═════
// opera: at nalı biçiminde üç kat loca; içleri ışıklı, seyircilerin başları siluet; büyük avize
P('P033', (ctx, st) => levha(ctx, CAM(960, 540, 1.05 - .04 * st.p), () => {
  INSAN.fill(SET.R(-400, -400, 2800, 1900), .03, { th: 0, id: 0 });
  for (let r = 0; r < 3; r++) for (let k = -4; k <= 4; k++) { const a = k / 4.6, x = 960 + Math.sin(a) * 1050, sc = .62 + .38 * Math.abs(Math.sin(a)), y = 300 + r * 250 - 60 * Math.cos(a) * (1 - r * .2), w = 200 * sc, h = 150;
    INSAN.fill(SET.R(x - w / 2, y, w, h), .55, { th: 0, id: 10 }); INSAN.fill(SET.R(x - w / 2 - 8, y + h - 6, w + 16, 30), .3, { th: 0, id: 9 }); INSAN.fill(SET.R(x - w / 2 - 12, y - 14, 14, h + 44), .12, { th: 0, id: 9 });
    for (let q = 0; q < 3; q++) { const hx = x - w * .3 + q * w * .3, hy = y + h - 34 - (q % 2) * 10; INSAN.fill(SET.E2(hx, hy, 15 * sc + 3, 19), .02); INSAN.fill(SET.R(hx - 22 * sc, hy + 14, 44 * sc, 30), .02); } }
  const t = st.t; INSAN.fill(SET.E2(960, 120, 210, 46), .6, { th: 0, id: 10 }); for (let k = 0; k < 16; k++) { const a = k / 16 * Math.PI * 2, x = 960 + Math.cos(a) * 200, y = 120 + Math.sin(a) * 44; INSAN.fill(SET.E2(x, y - 18, 6, 12 + 3 * Math.sin(t * 8 + k)), 1, { th: Math.PI / 2, id: 3 }); }
  SET.isik({ x: 960, y: 140, r1: 820, a: .75 }); }), { over: null });
// Doré gece: figürlerden aya doğru yükselen kamera (levha karanlık; aylı üst yarı ışık verir)
P('P039', (ctx, st) => SET.dore(ctx, 'dore263', CAM(960, 1250 - 330 * io(st.p), 1.0), 1920), { over: null });
// ev dışarıdan: Georgian cephe, basamaklı kapı, parmaklık, gaz lambası; üst katta tek ışıklı pencere; geçen iki beyefendi durup bakar
P('P076', (ctx, st) => { const yur = io(p01(st, 0, 1.6)), bak = io(p01(st, 1.4, 2.3)); levha(ctx, CAM(960, 540, 1.0 + .03 * st.p), () => {
  INSAN.fill(SET.R(-400, -400, 2800, 1900), .04, { th: 0, id: 0 }); INSAN.fill(SET.R(-400, -400, 2800, 420), .08, { th: .2, id: 6 });
  INSAN.fill(SET.R(120, 40, 1680, 900), .16, { th: 0, id: 9 }); for (let y = 90; y < 900; y += 34) INSAN.fill(SET.R(120, y, 1680, 3), .08, { th: 0, id: 9 });
  INSAN.fill(SET.R(100, 30, 1720, 26), .35, { th: 0, id: 9 });
  for (let r = 0; r < 2; r++) for (let k = 0; k < 5; k++) { const x = 220 + k * 330, y = 120 + r * 300, isikli = (r === 0 && k === 3);
    INSAN.fill(SET.R(x - 10, y - 10, 160, 250), .3, { th: 0, id: 9 }); INSAN.fill(SET.R(x, y, 140, 230), isikli ? .97 : .03, { th: Math.PI / 2, id: 10 });
    if (isikli) { INSAN.fill(SET.R(x + 66, y, 8, 230), .3); INSAN.fill(SET.R(x, y + 110, 140, 8), .3); } INSAN.fill(SET.R(x - 16, y + 240, 172, 14), .4, { th: 0, id: 9 }); }
  INSAN.fill(SET.R(860, 640, 200, 300), .02); INSAN.fill(SET.E2(960, 640, 100, 60), .3, { th: 0, id: 9 }); INSAN.fill(SET.E2(960, 640, 84, 50), .75, { th: 0, id: 10 }); for (let k = -2; k <= 2; k++) INSAN.fill(INSAN.F([[960, 640], [960 + k * 40 - 3, 592], [960 + k * 40 + 3, 592]]), .1); INSAN.fill(SET.R(850, 640, 220, 300), .02);
  for (let k = 0; k < 3; k++) INSAN.fill(SET.R(820 - k * 30, 940 + k * 22, 280 + k * 60, 22), .3 - k * .06, { th: 0, id: 9 });
  INSAN.fill(SET.R(-400, 1000, 2800, 200), .1, { th: 0, id: 9 });
  for (let x = -40; x < 1960; x += 40) if (x < 780 || x > 1140) INSAN.fill(SET.R(x, 860, 6, 140), .02); INSAN.fill(SET.R(-40, 870, 820, 6), .02); INSAN.fill(SET.R(1140, 870, 820, 6), .02);
  INSAN.fill(SET.R(1600, 560, 12, 460), .02); INSAN.fill(INSAN.F([[1570, 520], [1642, 520], [1630, 570], [1582, 570]]), .9, { th: 0, id: 10 }); SET.isik({ x: 1606, y: 545, r1: 360, a: .75 });
  SET.isik({ x: 1280, y: 240, r1: 520, a: .7 });
  for (const [x, dx] of [[200, 0], [330, 30]]) INSAN.adam({ x: x + dx + 260 * yur, y: 1080, h: 600, yon: 1, sapka: true, ton: .03, bas: -.35 * bak, adim: yur < 1 ? st.t * 1.3 : null, kenar: .35, kenarYan: 1 }); }); }, { over: null });
// avukat: dergiyi kaldırmış, okur (peruk yok: siluet yeter)
P('P083', (ctx, st) => levha(ctx, CAM(1000, 520, 1.4), () => { SET.mahkeme(); const h = INSAN.adam({ x: 820, y: 1000, h: 800, yon: 1, ton: .06, kenar: .45, kolOn: { a: 1.4, b: -.9 }, sakal: false });
  GR.save(); GR.frame(h.el[0] + 10, h.el[1] - 20, -.2, 1, 1); INSAN.fill(SET.R(0, -110, 150, 200), .88, { th: 0, id: 10 }); for (let k = 0; k < 8; k++) INSAN.fill(SET.R(14, -90 + k * 22, 120, 3), .3, { th: 0, id: 9 });
  const cev = io(p01(st, 1, 1.8)); if (cev > 0 && cev < 1) INSAN.fill(INSAN.F([[150, -110], [150 - 150 * (1 - cev), -110 - 30 * Math.sin(cev * Math.PI)], [150 - 150 * (1 - cev), 90 - 30 * Math.sin(cev * Math.PI)], [150, 90]]), .95, { th: 0, id: 10 }); GR.restore(); }), { over: null });
// duvardaki gölgeler: aydınlık duvar, yerdeki lamba; iki büyük gölge; biri ötekine kalkar; lamba söner (kan yok)
P('P055', (ctx, st) => { const u = io(p01(st, .2, 1.6)), sondu = io(p01(st, st.d - 1.2, st.d - .6)); levha(ctx, CAM(960, 520, 1), () => {
  INSAN.fill(SET.R(-400, -400, 2800, 1900), .45 * (1 - sondu) + .03, { th: 0, id: 9 }); INSAN.fill(SET.R(-400, 960, 2800, 400), .12 * (1 - sondu) + .02, { th: .1, id: 9 });
  if (sondu < 1) SET.isik({ x: 960, y: 1000, r1: 1300, a: .8 * (1 - sondu) });
  INSAN.adam({ x: 700, y: 980, h: 800, yon: 1, ton: .02, kolOn: { a: .5 - .3 * u, b: .2 }, kenar: null, egim: -.05 - .1 * u });
  INSAN.adam({ x: 1180, y: 980, h: 830 + 140 * u, yon: -1, ton: .02, arka: true, kolOn: { a: 1.2 + 1.7 * u, b: -.6 }, kenar: null, egim: .12 * u });
  if (sondu < 1) SET.lamba(960, 1000, st.t, 1.4); }); }, { over: null });
// sarı kitap: piyanonun üstünde açık kitap; sayfalar ışıkta, satırlar; Dorian'ın eli üstüne bastırır (gravür: renk yok)
function kitapPlan(ctx, st, el) { levha(ctx, CAM(960, 600, 2.0 + .06 * st.p), () => { INSAN.fill(SET.R(-400, -400, 2800, 1900), .04, { th: 0, id: 9 });
  INSAN.fill(SET.R(-400, 700, 2800, 500), .12, { th: .04, id: 9 }); INSAN.fill(SET.R(-400, 690, 2800, 14), .4, { th: 0, id: 9 }); SET.isik({ x: 960, y: 600, r1: 560, a: .85 });
  INSAN.fill(INSAN.F([[700, 700], [952, 676], [968, 676], [1220, 700], [1210, 720], [710, 720]]), .25, { th: 0, id: 9 });
  INSAN.fill(INSAN.Sm([[720, 520], [840, 500], [950, 512], [956, 690], [840, 678], [712, 698]]), .9, { th: 0, id: 10 }); INSAN.fill(INSAN.Sm([[970, 512], [1080, 500], [1200, 520], [1208, 698], [1080, 678], [964, 690]]), .9, { th: 0, id: 10 });
  INSAN.fill(SET.R(952, 508, 16, 184), .2, { th: 0, id: 9 });
  for (let k = 0; k < 9; k++) { const y = 540 + k * 16; INSAN.fill(SET.R(746, y - (k < 1 ? 0 : 0), 186 - (k === 8 ? 80 : 0), 3), .3); INSAN.fill(SET.R(990, y, 186 - (k === 4 ? 70 : 0), 3), .3); }
  if (el) { const b = io(p01(st, .3, 1.3)); GR.save(); GR.frame(1200 - 60 * b, 660 - 40 * b, Math.PI + .55, 1, 1); INSAN.fill(INSAN.F([[-30, -40], [-300, -56], [-300, 50], [-30, 40]]), .02);
    INSAN.fill(INSAN.Sm([[-34, -40], [40, -46], [100, -30], [118, -6], [100, 22], [40, 34], [-34, 38]]), .55, { th: .5, id: 5 });
    for (const [y, l] of [[-34, 60], [-12, 70], [10, 64], [30, 48]]) INSAN.fill(INSAN.Sm([[100, y - 7], [100 + l, y - 5], [106 + l, y + 1], [100 + l, y + 7], [100, y + 7]]), .5, { th: .5, id: 5 }); GR.restore(); } }); }
P('P061', (ctx, st) => kitapPlan(ctx, st, true), { yazi: { y: 150 } });
P('P067', (ctx, st) => kitapPlan(ctx, st, false), { over: null });
// yerdeki el: koyu döşeme, kol yeni, kırışık el ve ayrık parmaklar; iki parlak yüzük; yüz yok, kan yok
P('P079', (ctx, st) => levha(ctx, CAM(960, 570, 2.3 + .06 * st.p), () => { INSAN.fill(SET.R(-400, -400, 2800, 1900), .03, { th: 0, id: 0 }); for (let y = 300; y < 900; y += 70) INSAN.fill(SET.R(-400, y, 2800, 3), .1, { th: 0, id: 9 });
  SET.isik({ x: 1000, y: 570, r1: 300, a: .5 });
  GR.save(); GR.frame(900, 580, .1, 1, 1); INSAN.fill(INSAN.F([[-600, -56], [-150, -62], [-130, 60], [-600, 64]]), .015); INSAN.fill(INSAN.F([[-160, -64], [-132, -64], [-118, 62], [-146, 62]]), .55, { th: 0, id: 10 });
  INSAN.fill(INSAN.Sm([[-122, -52], [-20, -60], [56, -50], [70, 0], [56, 40], [-122, 50]]), .62, { th: 1.2, id: 5 });
  for (const [y, l, a] of [[-44, 100, -.14], [-16, 116, -.03], [12, 108, .07], [38, 84, .18]]) { GR.save(); GR.frame(60, y, a, 1, 1); INSAN.fill(INSAN.Sm([[-6, -10], [l * .5, -9], [l, -6], [l + 8, 0], [l, 7], [l * .5, 9], [-6, 10]]), .62, { th: a + 1.2, id: 5 }); INSAN.fill(SET.R(l * .45, -9, 4, 18), .15); INSAN.fill(SET.R(l * .8, -7, 3, 14), .15); GR.restore(); }
  INSAN.fill(INSAN.Sm([[-40, 46], [10, 60], [60, 86], [76, 100], [60, 106], [10, 82], [-40, 58]]), .62, { th: .8, id: 5 });
  INSAN.fill(SET.R(104, -34, 14, 26), .98, { th: 0, id: 10 }); INSAN.fill(SET.R(100, -6, 14, 26), .98, { th: 0, id: 10 }); SET.isik({ x: 1010, y: 570, r1: 60, a: .7 }); GR.restore(); }), { over: null });
// eksik plan kimlikleri (taslakta çizilmemiş) uyarısı
window.initScenes = () => { const var_ = new Set(SHOTS.map(s => s.id)); const eksik = Object.keys(PS).filter(k => !var_.has(k)); if (eksik.length) console.warn('çizilmemiş planlar: ' + eksik.join(' ')); };
