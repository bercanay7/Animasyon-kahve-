// Tablo sahne yöneticisi: bir videonun planları (film.js shot/plan) içinde yağlıboya sahne çizmek için.
// - Sahne = sıralı katmanlar: durağan (Ref resmi → paintRef → önbellek) ya da canlı (her çizimde darbe üretir).
// - Durağan katmanlar sahne ilk çizildiğinde kurulur (senkron, sahne başına ~10–30 sn); bellekte en çok `enCok` sahne tutulur (LRU).
//   render.js işçileri bitişik parçaları çizdiği için her işçi bir sahneyi genellikle bir kez kurar.
// - Belirlenimci: Math.random yok; paintRef tohumlu.
// Kullanım (ES modülü; film.js klasik betikten window.TABLO_MOTOR ile erişir):
//   const M = motor({ ss: 1.5 });
//   M.tanimla('tarla', { zemin, kamera: t => ({x, y, z}), bitir: t => ({...finish ayarı}), katmanlar: [
//     { ad: 'gok', d: 0, ciz: R => {...}, R: [30, 15, 7.5, 3.6, 1.8], T: 10 },          // durağan
//     { ad: 'gunes', d: .05, canli: (t, S, cam) => S.push({...}) },                       // canlı
//     { ad: 'agac', d: .5, ciz: T.agac, cam: (kam, t) => M.camDon(M.camK(kam, .5), [x, y], aci(t)) } ] });
//   plan('P04', (ctx, st) => M.ciz(ctx, 'tarla', st.lt));
import { Impasto, Strokes } from './impasto.js';
import { Ref, paintRef } from './plate.js';

export function motor({ W = 1920, H = 1080, ss = 1.5, enCok = 2, log = false } = {}) {
  const glc = document.createElement('canvas');
  const E = new Impasto(glc, { W, H, ss });
  const SAH = {}, KUR = new Map();      // ad → { katlar: {ad: önbellek}, sure, kullanim }
  let saat = 0;
  // katmanın kamerası: derinliğe göre kayma ve yaklaşma; görüş resmin içinde tutulur (kenarın ötesi boş)
  const camK = (k, d) => { const zoom = 1 + (k.z - 1) * (.35 + d * .9), hw = W / 2 / zoom, hh = H / 2 / zoom;
    const cl = (v, a, b) => (a > b ? (a + b) / 2 : Math.max(a, Math.min(b, v)));
    return { x: cl(W / 2 + (k.x - W / 2) * (.4 + d * .7), hw, W - hw), y: cl(H / 2 + (k.y - H / 2) * (.4 + d * .7), hh, H - hh), zoom, rot: 0 }; };
  // bir nokta çevresinde döndürülmüş kamera (ağaç rüzgârda dibinden eğilir)
  const camDon = (c, P, th) => { const cr = Math.cos(th), sr = Math.sin(th), vx = c.x - P[0], vy = c.y - P[1]; return { ...c, x: P[0] + cr * vx + sr * vy, y: P[1] - sr * vx + cr * vy, rot: th }; };

  function katmanKur(k) {
    const Rf = new Ref(W, H, k.olcek ?? .5);
    const R = { fill: (pf, c, p) => Rf.fill(pf, c, { seed: 1, ...p }), line: (pf, c, w, p) => Rf.line(pf, c, w, p || {}), text: (s, x, y, f, c, p) => Rf.text(s, x, y, f, c, p || {}), ref: Rf };
    k.ciz(R);
    const st = paintRef(Rf, { R: k.R || [26, 13, 6.5, 3.2, 1.7], T: k.T ?? 12, seed: k.seed ?? 3 });
    const b = E.batch(st.data()), tex = E.texture(Rf.ctx.canvas, 1.2);
    const on = E.onbellek(() => { E.under(tex, W, H, { t: 10 }); E.draw(b, { t: 10, wet: k.wet ?? .35 }); });
    const gl = E.gl; gl.deleteBuffer(b.buf); gl.deleteVertexArray(b.vao); gl.deleteTexture(tex);
    return { on, n: st.n };
  }
  function bosalt(ad) {
    const s = KUR.get(ad); if (!s) return; const gl = E.gl;
    for (const k of Object.values(s.katlar)) { gl.deleteTexture(k.on.c); gl.deleteTexture(k.on.h); }
    KUR.delete(ad); if (log) console.log('[tablo] boşaltıldı:', ad);
  }
  function hazirla(ad) {
    let s = KUR.get(ad);
    if (!s) {
      const tn = SAH[ad]; if (!tn) throw new Error('tablo sahnesi yok: ' + ad);
      while (KUR.size >= enCok) { let eski = null; for (const [a, v] of KUR) if (!eski || v.kullanim < KUR.get(eski).kullanim) eski = a; bosalt(eski); }
      const t0 = performance.now(), katlar = {}; let n = 0;
      for (const k of tn.katmanlar) if (k.ciz) { katlar[k.ad] = katmanKur(k); n += katlar[k.ad].n; }
      if (tn.hazir) tn.hazir();
      s = { katlar, n, sure: performance.now() - t0 }; KUR.set(ad, s);
      if (log) console.log(`[tablo] kuruldu: ${ad} (${n} darbe, ${Math.round(s.sure)} ms)`);
    }
    s.kullanim = ++saat; return s;
  }
  function tanimla(ad, tanim) { SAH[ad] = tanim; if (KUR.has(ad)) bosalt(ad); }
  // sahneyi ctx'e çiz (t: sahnenin yerel zamanı). o.kamera: sahnenin kamera işlevini geçersiz kılar.
  // o.durum: plana özgü durum (canlı katmanlara ve başlangıca 5./3. bağımsız değişken olarak geçer); o.bitir: bitiş ayarına eklenir (ör. maske, ışık)
  function ciz(ctx, ad, t, o = {}) {
    const tn = SAH[ad], s = hazirla(ad);
    const kam = o.kamera || (tn.kamera ? tn.kamera(t) : { x: W / 2, y: H / 2, z: 1 });
    E.begin(tn.zemin || [.1, .08, .12]);
    const ctxS = tn.baslangic ? tn.baslangic(t, kam, o.durum) : null;     // kare başı hesap (canlı katmanlar arası paylaşılan durum)
    for (const k of tn.katmanlar) {
      const cam = k.cam ? k.cam(kam, t, ctxS) : camK(kam, k.d ?? 0);
      if (k.ciz) { const al = k.alfa ? k.alfa(t, o.durum) : 1; if (al > .002) E.bas(s.katlar[k.ad].on, { cam, mul: k.mul ? k.mul(t, o.durum) : 1, alpha: al }); }
      else if (k.canli) { const S = new Strokes(k.kap || 256); k.canli(t, S, cam, ctxS, o.durum); if (S.n) E.drawNow(S.data(), { cam, t: 10, wet: k.wet ?? .3, run: k.run ?? 1 }); }
    }
    E.finish({ ...(tn.bitir ? tn.bitir(t, o.durum) : {}), ...(typeof o.bitir === 'function' ? o.bitir(t) : o.bitir || {}) });
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(glc, 0, 0, ctx.canvas.width, ctx.canvas.height); ctx.restore();
  }
  const bitir = () => { const px = new Uint8Array(4); E.gl.readPixels(0, 0, 1, 1, E.gl.RGBA, E.gl.UNSIGNED_BYTE, px); };
  const durum = () => [...KUR].map(([a, v]) => ({ ad: a, darbe: v.n, ms: Math.round(v.sure) }));
  const kameraAl = (ad, t) => { const tn = SAH[ad]; return tn.kamera ? tn.kamera(t) : { x: W / 2, y: H / 2, z: 1 }; };
  return { E, W, H, kameraAl, tanimla, hazirla, ciz, bosalt, camK, camDon, bitir, durum, Strokes };
}
if (typeof window !== 'undefined') window.TABLO_MOTOR = { motor };
